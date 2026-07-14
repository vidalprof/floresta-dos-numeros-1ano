# -*- coding: utf-8 -*-
# SCRIPT OFICIAL DE CORTE DE SPRITES do Mundo Vivo (copia permanente no repo).
# Origem: cortar_td3.py (v5) da sessao do proto top-down — os caminhos R/S abaixo
# eram da sessao original; ajuste-os ao usar. NAO mude os limiares sem atualizar
# o manual MUNDO-VIVO-SPRITES.md.
# v5: recorta TODOS os sprites com CANVAS COMUM POR CONJUNTO (escala 1:1, pes alinhados)
# — a cura do "piscar": nenhum quadro muda de tamanho dentro do conjunto.
import numpy as np, os, io, base64, json
from PIL import Image
from scipy import ndimage
R='/home/user/floresta-dos-numeros-1ano/_novo'
S='/tmp/claude-0/-home-user-floresta-dos-numeros-1ano/9052d2be-05eb-511d-8025-ca916a0a13ce/scratchpad'

def recorta_raw(cel):
    a=np.asarray(cel.convert('RGB')).astype(int)
    mx=a.max(2); mn=a.min(2)
    fundo=(mn>240)&((mx-mn)<14)
    lab,n=ndimage.label(fundo)
    borda=set()
    for v in (lab[0,:],lab[-1,:],lab[:,0],lab[:,-1]): borda.update(np.unique(v))
    borda.discard(0)
    obj=~np.isin(lab,list(borda))
    obj=ndimage.binary_opening(obj,iterations=2)
    obj=ndimage.binary_fill_holes(obj)
    lab2,n2=ndimage.label(obj)
    if n2==0: return None
    tam=ndimage.sum(obj,lab2,range(1,n2+1))
    keep=(lab2==(int(np.argmax(tam))+1))
    ys,xs=np.where(keep)
    er=ndimage.binary_erosion(keep,iterations=2)
    keep2=keep&~((keep&~er)&(mn>232))
    rgba=np.dstack([np.asarray(cel.convert('RGB')),(keep2*255).astype(np.uint8)]).astype(np.uint8)
    return Image.fromarray(rgba).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))

def normaliza_set(frames, alt):
    """frames 1:1 da mesma cartela -> canvas comum, pes na base, centro x; depois resize p/ alt"""
    maxh=max(f.height for f in frames); maxw=max(f.width for f in frames)
    CH,CW=maxh+4,maxw+6
    outs=[]
    for f in frames:
        cv=Image.new('RGBA',(CW,CH),(0,0,0,0))
        cv.paste(f,((CW-f.width)//2,CH-f.height),f)
        fw=int(CW*alt/CH)
        outs.append(cv.resize((fw,alt),Image.LANCZOS))
    return outs

def uri(im):
    q=im.convert('RGBA').quantize(colors=255,method=Image.FASTOCTREE)
    b=io.BytesIO(); q.save(b,'PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

out=json.load(open(S+'/td_assets2.json'))  # mantem salao/itens ja prontos

# ---- CHEF ----
c2=Image.open(R+'/td_chef2.png'); W2,H2=c2.size
c4=Image.open(R+'/td_chef4.png'); W4,H4=c4.size
def cel2(c,r): return recorta_raw(c2.crop((c*W2//4+8,r*H2//2+8,(c+1)*W2//4-8,(r+1)*H2//2-8)))
def cel4(c,r): return recorta_raw(c4.crop((c*W4//4+12,r*H4//3+12,(c+1)*W4//4-12,(r+1)*H4//3-12)))
# baixo: 2 quadros do chef2 + parado + feliz (mesma cartela = mesmo set p/ nao pular na transicao)
setA=normaliza_set([cel2(0,0),cel2(1,0),cel2(2,1),cel2(3,1)],118)
out['chef_baixo0'],out['chef_baixo1'],out['chef_parado'],out['chef_feliz']=[uri(x) for x in setA]
# cima: 4 quadros (chef4 linha 2)
setC=normaliza_set([cel4(i,1) for i in range(4)],118)
for i,x in enumerate(setC): out['chef_cima%d'%i]=uri(x)
# lado: 4 quadros (chef4 linha 3)
setL=normaliza_set([cel4(i,2) for i in range(4)],118)
for i,x in enumerate(setL): out['chef_lado%d'%i]=uri(x)
print('chef ok: baixo2+parado+feliz, cima4, lado4')

# ---- CLIENTES ----
tags=[('td_anda_coelho','coelho'),('td_anda_urso','urso'),('td_anda_menina','menina')]
lado=Image.open(R+'/td_anda_lado.png'); WL,HL=lado.size
for idx,(arq,tag) in enumerate(tags):
    img=Image.open(R+'/%s.png'%arq); W,H=img.size
    cels=[recorta_raw(img.crop((c*W//3+8,r*H//2+8,(c+1)*W//3-8,(r+1)*H//2-8))) for r in range(2) for c in range(3)]
    # ordem: costas0,costas1,costasP,frente0,frente1,frenteP — UM canvas para os 6
    st=normaliza_set(cels,100)
    nomes=['costas0','costas1','costasP','frente0','frente1','frenteP']
    for n,x in zip(nomes,st): out[tag+'_'+n]=uri(x)
    # lado: 2 quadros (cartela separada, canvas proprio)
    l2=[recorta_raw(lado.crop((idx*WL//3+8,r*HL//2+8,(idx+1)*WL//3-8,(r+1)*HL//2-8))) for r in range(2)]
    stl=normaliza_set(l2,100)
    out[tag+'_lado0'],out[tag+'_lado1']=uri(stl[0]),uri(stl[1])
    print(tag,'ok (6+2 normalizados)')

# sentados (se ja chegou)
p=R+'/td_sentados.png'
if os.path.exists(p):
    img=Image.open(p); W,H=img.size
    for i,tag in enumerate(['coelho','urso','menina']):
        c=recorta_raw(img.crop((i*W//3+8,8,(i+1)*W//3-8,H-8)))
        st=normaliza_set([c],86)
        out[tag+'_sentado']=uri(st[0])
    print('sentados ok')
else:
    print('sentados: cartela ainda nao chegou')

json.dump(out,open(S+'/td_assets3.json','w'))
tot=sum(len(v) for v in out.values())
print('TOTAL: %.0fKB | chaves: %d'%(tot/1024,len(out)))
