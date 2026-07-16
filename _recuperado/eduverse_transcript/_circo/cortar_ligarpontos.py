#!/usr/bin/env python3
# Recorta cartola + gravata de IMG_2957 e extrai 10 pontos do contorno (Moore tracing).
import numpy as np, math, os
from PIL import Image
from collections import deque
import scipy.ndimage as nd

BASE=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(BASE,"img")
SRC=os.path.join(BASE,"img","originais","ligarpontos-cartola-gravata-original.png")

def limpar_bolinhas_brancas(cut):
    # gravata: troca as bolinhas brancas (miolo claro + anel) pela cor vermelha do laco
    a=np.array(cut); r,g,b,al=a[:,:,0].astype(int),a[:,:,1].astype(int),a[:,:,2].astype(int),a[:,:,3]
    op=al>128; mn=np.minimum(np.minimum(r,g),b)
    core=nd.binary_dilation(op&(mn>185),iterations=5)  # miolo + anel
    preto=op&(mn<70)
    alvo=core&op&(~preto)
    red=op&(r>180)&(g<95)&(b<95)
    if red.sum()<50: return cut
    rc=[int(np.median(a[:,:,0][red])),int(np.median(a[:,:,1][red])),int(np.median(a[:,:,2][red]))]
    for c in range(3):
        ch=a[:,:,c]; ch[alvo]=rc[c]; a[:,:,c]=ch
    return Image.fromarray(a,"RGBA")

def ink_mask(arr):
    r,g,b=arr[:,:,0].astype(int),arr[:,:,1].astype(int),arr[:,:,2].astype(int)
    return np.minimum(np.minimum(r,g),b)<232

def flood_transp(cell):
    px=cell.load(); w,h=cell.size
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

def moore(mask):
    H,W=mask.shape
    start=None
    for y in range(H):
        row=np.where(mask[y])[0]
        if len(row): start=(int(row[0]),y); break
    if not start: return []
    mo=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    def isf(x,y): return 0<=x<W and 0<=y<H and mask[y,x]
    def didx(c,p):
        dx=p[0]-c[0]; dy=p[1]-c[1]
        for i,(mx,my) in enumerate(mo):
            if mx==dx and my==dy: return i
        return 4
    contour=[start]; prev=(start[0]-1,start[1]); curr=start
    it=0; mx=8*(H+W)+5000
    while it<mx:
        it+=1; di=didx(curr,prev); found=False
        for k in range(1,9):
            ni=(di+k)%8; nx=curr[0]+mo[ni][0]; ny=curr[1]+mo[ni][1]
            if isf(nx,ny):
                prev=curr; curr=(nx,ny); contour.append(curr); found=True; break
        if not found: break
        if curr==start and len(contour)>3: break
    return contour

def resample(pts,n=10):
    d=[0.0]
    for i in range(1,len(pts)):
        d.append(d[-1]+math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]))
    total=d[-1]; out=[]
    if total==0: return [pts[0]]*n
    for i in range(n):
        tgt=total*i/n; j=0
        while j<len(d)-1 and d[j+1]<tgt: j+=1
        if j>=len(pts)-1: out.append(pts[-1]); continue
        seg=d[j+1]-d[j]; t=0 if seg==0 else (tgt-d[j])/seg
        out.append((pts[j][0]+t*(pts[j+1][0]-pts[j][0]), pts[j][1]+t*(pts[j+1][1]-pts[j][1])))
    return out

def wrapcoords(pts01, ar, fill=0.72):
    # ar = w/h da figura; contain num quadrado, centralizado
    if ar>=1: wn=fill; hn=fill/ar
    else: hn=fill; wn=fill*ar
    left=(1-wn)/2.0; top=(1-hn)/2.0
    return [[round(left+fx*wn,4), round(top+fy*hn,4)] for (fx,fy) in pts01]

im=Image.open(SRC).convert("RGBA"); arr=np.array(im); mask=ink_mask(arr); H,W=mask.shape
dil=nd.binary_dilation(mask,iterations=14); lbl,n=nd.label(dil)
boxes=[]
for i in range(1,n+1):
    oy,ox=np.where(mask&(lbl==i))
    if len(oy)<200: continue
    boxes.append((ox.min(),oy.min(),ox.max()+1,oy.max()+1))
boxes.sort(key=lambda b:b[0])  # esquerda->direita: cartola, gravata
nomes=["cartola","gravata"]
res={}
for idx,(x0,y0,x1,y1) in enumerate(boxes[:2]):
    nome=nomes[idx]
    pad=8; box=(max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad))
    cut=flood_transp(im.crop(box))
    if nome=="gravata": cut=limpar_bolinhas_brancas(cut)
    # salva colorido otimizado
    cw,ch=cut.size
    if ch>240: cut=cut.resize((int(round(cw*240.0/ch)),240),Image.LANCZOS)
    a=cut.split()[3].point(lambda v:255 if v>128 else 0); cut.putalpha(a)
    q=cut.quantize(colors=48,method=Image.FASTOCTREE,dither=Image.NONE)
    q.save(os.path.join(IMG,"lp-%s.png"%nome),optimize=True)
    # contorno na mascara alpha
    m2=(np.array(cut)[:,:,3]>128)
    cont=moore(m2)
    pts=resample(cont,10)
    w2,h2=cut.size
    pts01=[(px/float(w2),py/float(h2)) for (px,py) in pts]
    wc=wrapcoords(pts01,w2/float(h2))
    res[nome]={"ar":round(w2/float(h2),3),"pts":wc,"sz":cut.size}
    print("lp-%s.png"%nome, cut.size, "%dB"%os.path.getsize(os.path.join(IMG,"lp-%s.png"%nome)))
    print("  pts:", wc)
import json
open("/tmp/lp_pts.json","w").write(json.dumps(res))
print("OK")
