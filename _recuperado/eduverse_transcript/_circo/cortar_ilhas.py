#!/usr/bin/env python3
# Recorta as ilhas das 2 cartelas -> _circo/img/ilha-<ch>.png (transparente).
# Segmenta por corredores brancos (linhas/colunas sem tinta), recorta cada
# celula, remove o branco A PARTIR DAS BORDAS (preserva brancos internos) e autocropa.
import numpy as np
from PIL import Image
from collections import deque
import os

BASE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(BASE, "img")

def ink_mask(arr):
    # tinta = NAO quase-branco
    r,g,b = arr[:,:,0].astype(int),arr[:,:,1].astype(int),arr[:,:,2].astype(int)
    mn = np.minimum(np.minimum(r,g),b)
    return mn < 232

def bands(profile, min_gap, min_len):
    # faixas [a,b) com tinta, unindo through gaps de branco menores que min_gap;
    # descarta faixas menores que min_len (ruido).
    on = profile > 0
    n = len(on)
    faixas=[]
    i=0
    while i < n:
        if not on[i]:
            i += 1; continue
        a = i; last_on = i; gap = 0; k = i
        while k < n:
            if on[k]:
                last_on = k; gap = 0
            else:
                gap += 1
                if gap >= min_gap:
                    break
            k += 1
        b = last_on + 1
        if b - a >= min_len:
            faixas.append((a, b))
        i = max(b + 1, k + 1)
    return faixas

def flood_transp(cell):
    px = cell.load(); w,h = cell.size
    def white(p): return p[0]>=232 and p[1]>=232 and p[2]>=232
    seen=[[False]*w for _ in range(h)]; dq=deque()
    for x in range(w):
        for y in (0,h-1):
            if white(px[x,y]) and not seen[y][x]: seen[y][x]=True; dq.append((x,y))
    for y in range(h):
        for x in (0,w-1):
            if white(px[x,y]) and not seen[y][x]: seen[y][x]=True; dq.append((x,y))
    while dq:
        x,y=dq.popleft(); r,g,b,a=px[x,y]; px[x,y]=(r,g,b,0)
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and not seen[ny][nx] and white(px[nx,ny]):
                seen[ny][nx]=True; dq.append((nx,ny))
    bb=cell.getbbox()
    return cell.crop(bb) if bb else cell

def boxes_for(mask, iters):
    import scipy.ndimage as nd
    dil = nd.binary_dilation(mask, iterations=iters)
    lbl,n = nd.label(dil)
    bxs=[]
    for i in range(1,n+1):
        ys,xs = np.where(lbl==i)
        # bbox na mascara ORIGINAL dentro do componente dilatado
        oy,ox = np.where(mask & (lbl==i))
        if len(oy)==0: continue
        y0,y1,x0,x1 = oy.min(),oy.max(),ox.min(),ox.max()
        area = (y1-y0)*(x1-x0)
        bxs.append((y0,y1+1,x0,x1+1,area))
    # descarta ruido: area minima E dimensao minima (tiras finas fora)
    tot = mask.shape[0]*mask.shape[1]
    bxs = [b for b in bxs if b[4] > tot*0.004 and (b[1]-b[0])>=55 and (b[3]-b[2])>=55]
    return bxs

def reading_order(bxs):
    # agrupa em linhas por centro-y, depois ordena por x
    if not bxs: return []
    hs = sorted([b[1]-b[0] for b in bxs])
    medh = hs[len(hs)//2]
    bxs2 = sorted(bxs, key=lambda b:(b[0]+b[1])/2.0)
    linhas=[]; atual=[bxs2[0]]
    for b in bxs2[1:]:
        cy=(b[0]+b[1])/2.0; cyprev=(atual[-1][0]+atual[-1][1])/2.0
        if abs(cy-cyprev) > medh*0.6:
            linhas.append(atual); atual=[b]
        else:
            atual.append(b)
    linhas.append(atual)
    out=[]
    for ln in linhas:
        for b in sorted(ln, key=lambda b:(b[2]+b[3])/2.0):
            out.append(b)
    return out

def segment(path, slugs):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im); mask = ink_mask(arr); H,W = mask.shape
    best=None
    for it in [22,18,15,12,10,8]:
        bxs = boxes_for(mask, it)
        if len(bxs)==len(slugs):
            best=bxs; break
        if best is None or abs(len(bxs)-len(slugs))<abs(len(best)-len(slugs)):
            best=bxs
    bxs = reading_order(best)
    print(os.path.basename(path),"-> ilhas:",len(bxs),"esperado:",len(slugs))
    out=[]
    for (y0,y1,x0,x1,area) in bxs:
        pad=10
        box=(max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad))
        out.append(flood_transp(im.crop(box)))
    return out, bxs

A_slugs=["cores","numeros","formas","sombra","luzes","vogais"]
B_slugs=["diferente","quebra1","memoria","erros","quebra2"]

_IMAGENS = os.path.join(BASE, "..", "_imagens")
resA,cA = segment(os.path.join(_IMAGENS,"IMG_2955.jpeg"), A_slugs)
resB,cB = segment(os.path.join(_IMAGENS,"IMG_2956.png"), B_slugs)

def save(res, slugs, tag):
    if len(res)!=len(slugs):
        print("!!! contagem diferente em",tag,"- revisar. Salvando por indice mesmo.")
    for i,cut in enumerate(res):
        slug = slugs[i] if i<len(slugs) else (tag+"-extra%d"%i)
        # resize p/ altura ~360 (folga p/ nitidez), otimiza depois na montagem
        w,h=cut.size
        if h>460:
            nw=int(w*460.0/h); cut=cut.resize((nw,460), Image.LANCZOS)
        cut.save(os.path.join(IMGDIR,"ilha-%s.png"%slug))
        print("  ilha-%s.png"%slug, cut.size)

save(resA,A_slugs,"A")
save(resB,B_slugs,"B")
print("OK")
