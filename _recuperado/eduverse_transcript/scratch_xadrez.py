from PIL import Image
import numpy as np
from scipy import ndimage
import sys, os

def remove_xadrez(path, dark=True, thr=None):
    im = Image.open(path).convert("RGB")
    arr = np.array(im).astype(int)
    r,g,b = arr[...,0],arr[...,1],arr[...,2]
    lum = 0.299*r + 0.587*g + 0.114*b
    if dark:
        t = 58 if thr is None else thr
        bgish = lum < t
    else:
        t = 205 if thr is None else thr
        mx = np.maximum(np.maximum(r,g),b); mn = np.minimum(np.minimum(r,g),b)
        bgish = (lum > t) & ((mx-mn) < 28)
    lbl,n = ndimage.label(bgish)
    border = set(lbl[0,:]) | set(lbl[-1,:]) | set(lbl[:,0]) | set(lbl[:,-1])
    border.discard(0)
    bg = np.isin(lbl, list(border))
    rgba = np.dstack([arr.astype(np.uint8), np.where(bg,0,255).astype(np.uint8)])
    # defringe: suaviza 2px de borda
    mask = rgba[...,3] > 0
    er = ndimage.binary_erosion(mask, iterations=2)
    edge = mask & (~er)
    a = rgba[...,3].astype(int); a[edge] = (a[edge]*0.35).astype(int); rgba[...,3]=a.astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")

def keep_main(a):
    solid=a[...,3]>40; lb,nn=ndimage.label(solid)
    if nn<=1: return a
    sizes=ndimage.sum(np.ones_like(lb),lb,range(1,nn+1))
    keep=int(np.argmax(sizes))+1; a[(lb!=keep)&(lb!=0),3]=0; return a

def cut(img, rows, cols, names, outdir, maxw):
    W,H=img.size; cw,ch=W/cols, H/rows
    os.makedirs(outdir, exist_ok=True)
    for ri in range(rows):
        for ci in range(cols):
            cell=img.crop((int(ci*cw),int(ri*ch),int((ci+1)*cw),int((ri+1)*ch)))
            a=keep_main(np.array(cell)); cell=Image.fromarray(a,"RGBA")
            al=np.array(cell)[...,3]; ys,xs=np.where(al>14)
            if len(xs)==0:
                print("vazio", names[ri][ci]); continue
            p=6; cell=cell.crop((max(0,xs.min()-p),max(0,ys.min()-p),min(cell.width,xs.max()+1+p),min(cell.height,ys.max()+1+p)))
            if cell.width>maxw: cell=cell.resize((maxw,int(cell.height*maxw/cell.width)), Image.LANCZOS)
            outp=os.path.join(outdir,names[ri][ci]+".png"); cell.save(outp, optimize=True)
            print(names[ri][ci], cell.size, str(round(os.path.getsize(outp)/1024))+"KB")

# Teste so com Aventureiros (dark) -> pasta temporaria de teste
img = remove_xadrez("img/IMG_2832.jpeg", dark=True)
names=[["t_fenix","t_golem","t_salam","t_grifo"],["t_cb","t_cr","t_lava","t_tocha"]]
cut(img, 2, 4, names, "img/_teste", 360)
print("OK")
