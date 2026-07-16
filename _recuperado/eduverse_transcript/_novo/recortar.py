#!/usr/bin/env python3
# Recorte de cartelas em fundo PRETO (Gemini) -> PNGs transparentes individuais.
# Componente conectado (scipy), alpha da mascara, margem, suavizacao. Sem white-fringe (fundo e preto).
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

REC="_novo/rec"
os.makedirs(REC, exist_ok=True)

def recortar_cartela(nome, nesperado, thr=34, min_frac=0.004):
    im = Image.open("_novo/%s.png"%nome).convert("RGB")
    arr = np.asarray(im)
    H,W = arr.shape[:2]
    mx = arr.max(axis=2)                      # canal maximo: fundo preto ~0
    mask = mx > thr
    mask = ndimage.binary_closing(mask, iterations=2)
    lab, n = ndimage.label(mask)
    areas = ndimage.sum(np.ones_like(lab), lab, index=range(1,n+1))
    minA = min_frac*H*W
    comps = [(i+1, areas[i]) for i in range(n) if areas[i] >= minA]
    comps.sort(key=lambda t:-t[1])
    comps = comps[:nesperado] if nesperado else comps
    # centroides p/ ordenar row-major
    info=[]
    for cid,_ in comps:
        ys,xs = np.where(lab==cid)
        cy,cx = ys.mean(), xs.mean()
        info.append((cid,cy,cx,ys.min(),ys.max(),xs.min(),xs.max()))
    # agrupa em linhas por cy (tolerancia = 8% da altura)
    info.sort(key=lambda t:t[1])
    linhas=[]; tol=0.08*H
    for it in info:
        if linhas and abs(it[1]-linhas[-1][0]) < tol:
            linhas[-1][1].append(it)
        else:
            linhas.append([it[1],[it]])
    ordenado=[]
    for _,row in linhas:
        row.sort(key=lambda t:t[2])
        ordenado += row
    saidas=[]
    for idx,(cid,cy,cx,y0,y1,x0,x1) in enumerate(ordenado):
        m = (lab==cid)
        m = ndimage.binary_fill_holes(m)
        # margem
        pad = int(0.09*max(y1-y0, x1-x0))
        yy0=max(0,y0-pad); yy1=min(H,y1+pad+1); xx0=max(0,x0-pad); xx1=min(W,x1+pad+1)
        sub = arr[yy0:yy1, xx0:xx1]
        sm = m[yy0:yy1, xx0:xx1].astype(np.uint8)*255
        # suaviza + erode 1px p/ tirar anel escuro do antialias
        sm = ndimage.grey_erosion(sm, size=(2,2))
        sm = ndimage.gaussian_filter(sm, sigma=0.6)
        sm = np.where(sm>128,255,0).astype(np.uint8)
        rgba = np.dstack([sub, sm])
        out = Image.fromarray(rgba,"RGBA")
        p = "%s/%s_%d.png"%(REC,nome,idx)
        out.save(p)
        saidas.append((p, out.size))
    print("%s: %d recortes"%(nome, len(saidas)))
    return [s[0] for s in saidas]

def mosaico_numerado(nome, paths, th=180, cols=4):
    ims=[Image.open(p).convert("RGBA") for p in paths]
    cell=th+40
    rows=(len(ims)+cols-1)//cols
    W=cols*cell; Hh=rows*cell
    mos=Image.new("RGB",(W,Hh),(24,22,30)); d=ImageDraw.Draw(mos)
    for i,im in enumerate(ims):
        w,h=im.size; nw=int(w*th/h) if h>th else w
        im2=im.resize((nw,th)) if h>th else im
        r=i//cols; c=i%cols
        x=c*cell+(cell-im2.size[0])//2; y=r*cell+30
        # xadrez leve atras
        mos.paste(im2,(x,y),im2)
        d.text((c*cell+6, r*cell+6), "%d"%i, fill=(255,220,150))
    out="/tmp/rec_%s.png"%nome
    mos.save(out); print("mosaico:",out, mos.size)
    return out

PLANO={"chef-confeito":6,"objetos":8,"medalhas":8,"emblemas":5,"selos":6,"extras":4}
for nome,nesp in PLANO.items():
    ps=recortar_cartela(nome,nesp)
    mosaico_numerado(nome,ps)
print("FIM")
