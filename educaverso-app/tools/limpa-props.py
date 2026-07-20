#!/usr/bin/env python3
# FERRAMENTA DO DIRETOR DE ARTE — extrai props de cenário LIMPOS do atlas mundo.png.
# Problema: props de floresta densa (pinheiro/cerejeira/carvalho/pedra) trazem
# fragmentos da árvore vizinha no recorte retangular (o "halo de foto colada").
# Solução: recorta, mantém só o MAIOR BLOB conectado (o objeto principal), apaga as
# ilhas vizinhas soltas, apara franja de 1px e autocrop. Salva PNG individual limpo.
from PIL import Image
from collections import deque
im = Image.open('public/rpg/mundo.png').convert('RGBA')
PROPS = {
 'arvore':[0,160,32,32], 'pinheiro':[140,146,45,46], 'carvalho':[176,131,35,44],
 'cerejeira':[97,240,52,48], 'pedra_g':[190,166,42,27], 'pedra_p':[269,142,21,20],
 'toco':[97,292,30,26], 'cogumelo':[14,338,18,15], 'flor':[304,464,16,16],
 'margarida':[222,146,20,15], 'arbusto':[0,336,17,18], 'pinheiro_neve':[48,337,46,46],
 'bola_neve':[109,384,20,17], 'carroca':[82,130,28,28],
}
def flood_cantos(c):
    # remove VIZINHOS opacos (tiles de terra/grama colados no atlas) por floodfill dos
    # 4 cantos: espalha por cor parecida e PARA no contorno preto do sprite. Trava: se
    # a região do canto passar de 40% da imagem, é o próprio objeto -> não remove.
    w,h = c.size; px = c.load()
    def alike(p,q): return abs(p[0]-q[0])+abs(p[1]-q[1])+abs(p[2]-q[2]) < 90 and p[3]>0
    for cx,cy in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
        base = px[cx,cy]
        if base[3]==0: continue
        seen=set(); q=deque([(cx,cy)])
        while q:
            a,b=q.popleft()
            if (a,b) in seen: continue
            seen.add((a,b))
            for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                na,nb=a+da,b+db
                if 0<=na<w and 0<=nb<h and (na,nb) not in seen and alike(px[na,nb],base):
                    q.append((na,nb))
        if len(seen) < 0.40*w*h:                      # é fundo/vizinho -> apaga
            for a,b in seen: px[a,b]=(0,0,0,0)

def limpa(nome, box, keep_blob=True):
    x,y,w,h = box
    c = im.crop((x,y,x+w,y+h)).copy()
    flood_cantos(c)
    px = c.load()
    op = [[px[i,j][3] > 40 for i in range(w)] for j in range(h)]
    if keep_blob:
        # rotula componentes conectados (4-viz) e acha o maior
        lab = [[-1]*w for _ in range(h)]; comps=[]
        for j in range(h):
            for i in range(w):
                if op[j][i] and lab[j][i]==-1:
                    q=deque([(i,j)]); lab[j][i]=len(comps); cells=[]
                    while q:
                        a,b=q.popleft(); cells.append((a,b))
                        for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                            na,nb=a+da,b+db
                            if 0<=na<w and 0<=nb<h and op[nb][na] and lab[nb][na]==-1:
                                lab[nb][na]=len(comps); q.append((na,nb))
                    comps.append(cells)
        if comps:
            comps.sort(key=len, reverse=True)
            main=comps[0]
            # se o 2º maior tiver >=45% do maior, é parte do objeto (ex.: copa+tronco separados) -> mantém
            keep=set(main)
            for comp in comps[1:]:
                if len(comp) >= 0.45*len(main): keep.update(comp)
            for j in range(h):
                for i in range(w):
                    if op[j][i] and (i,j) not in keep: px[i,j]=(0,0,0,0)
    bb=c.getbbox()
    if bb: c=c.crop(bb)
    c.save(f'public/rpg/cen/{nome}.png')
    return c.size
for n,b in PROPS.items():
    print(n, limpa(n,b))

# CEREJEIRA = o arbusto redondo LIMPO RECOLORIDO de verde->rosa (flor). Recolorir de
# verdade (HSV) fica rosa, ao contrário do setTint multiplicativo que só embaça. Mantém
# a sombra/forma do arbusto (que já é limpo e bonito como a fase 1) e o tronco marrom.
import colorsys
def recolore(entrada, saida, hue_alvo, sat=0.55):
    c = Image.open(entrada).convert('RGBA'); px = c.load(); w,h = c.size
    for y in range(h):
        for x in range(w):
            r,g,bl,a = px[x,y]
            if a < 40: continue
            hh,ss,vv = colorsys.rgb_to_hsv(r/255,g/255,bl/255)
            if 0.20 < hh < 0.47 and ss > 0.15:            # só a COPA verde (tronco marrom fica)
                nr,ng,nb = colorsys.hsv_to_rgb(hue_alvo, min(1,ss*0.9+sat*0.3), vv)
                px[x,y] = (int(nr*255),int(ng*255),int(nb*255),a)
    c.save(saida)
    return c.size
print('cerejeira(rosa)', recolore('public/rpg/cen/arvore.png','public/rpg/cen/cerejeira.png', 0.92))
