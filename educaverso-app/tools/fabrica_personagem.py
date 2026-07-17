#!/usr/bin/env python3
# ============================================================================
# FÁBRICA DE PERSONAGEM (genérica, reaproveitável para QUALQUER personagem)
# Recebe a cartela de poses cruas (fundo preto, geradas por IA a partir da
# âncora) e produz um ATLAS padronizado:
#   - fundo -> transparente (flood pela borda por cor, mata franja)
#   - mantém só o maior objeto + preenche buracos
#   - MESMO tamanho de quadro (canvas fixo) com os PÉS alinhados na base
#     (assim o personagem NÃO "pula" entre as poses)
#   - otimizado (leve p/ o PC da escola)
# Uso:  python3 fabrica_personagem.py <nome>   (ex.: verso)
#   lê  _novo/<nome>_<pose>.png   (e a âncora _novo/ilha_<nome>_azul.png / _novo/<nome>.png)
#   grava educaverso-app/public/personagens/<nome>/<pose>.png  (+ manifest.json)
# ============================================================================
import os, sys, json
from collections import deque
from PIL import Image
import numpy as np

RAIZ = '/home/user/floresta-dos-numeros-1ano'
SRC = os.path.join(RAIZ, '_novo')

# conjunto-padrão de poses (a mesma cartela p/ TODO personagem)
POSES = {
    'parado':      ['ilha_{n}_azul', '{n}_parado', '{n}'],   # âncora serve de "parado"
    'passo_a':     ['{n}_passo_a'],
    'passo_b':     ['{n}_passo_b'],
    'passo_c':     ['{n}_passo_c'],
    'costas':      ['{n}_costas'],
    'costas_passo':['{n}_costas_passo'],
    'lado':        ['{n}_lado'],
    'lado_passo':  ['{n}_lado_passo'],
    'sentar':      ['{n}_sentar'],
    'deitar':      ['{n}_deitar'],
    'acenar':      ['{n}_acenar'],
    'piscar':      ['{n}_piscar'],
    'feliz':       ['{n}_feliz'],
    'triste':      ['{n}_triste'],
}

ALT = 220           # altura do recorte do personagem (px)
CANVAS_W = 260      # quadro padrão (todos iguais)
CANVAS_H = 240
BASE_Y = 232        # linha do chão dentro do quadro (pés aqui)

def acha(nome, chaves):
    for c in chaves:
        p = os.path.join(SRC, c.format(n=nome) + '.png')
        if os.path.exists(p):
            return p
    return None

def recorta(path, tol=46):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]], 0)
    bg = np.median(borda, 0)
    dist = np.sqrt(((a - bg) ** 2).sum(2))
    fundo = dist < tol
    rem = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if fundo[y, x] and not rem[y, x]: rem[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if fundo[y, x] and not rem[y, x]: rem[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = cy+dy, cx+dx
            if 0<=ny<h and 0<=nx<w and fundo[ny,nx] and not rem[ny,nx]:
                rem[ny,nx] = True; q.append((ny,nx))
    obj = ~rem
    # maior componente (grade 2x)
    small = obj[::2, ::2]; sh, sw = small.shape
    lab = np.zeros((sh, sw), np.int32); best=0; bestn=0; cur=0
    for y in range(sh):
        for x in range(sw):
            if small[y,x] and lab[y,x]==0:
                cur+=1; n=0; qq=deque([(y,x)]); lab[y,x]=cur
                while qq:
                    cy,cx=qq.popleft(); n+=1
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<sh and 0<=nx<sw and small[ny,nx] and lab[ny,nx]==0:
                            lab[ny,nx]=cur; qq.append((ny,nx))
                if n>bestn: bestn,best=n,cur
    keep_s=(lab==best); keep=np.zeros((sh*2,sw*2),bool)
    for oy in (0,1):
        for ox in (0,1): keep[oy::2,ox::2]=keep_s
    keep=keep[:h,:w] & obj
    for _ in range(2):
        k=keep.copy(); k[1:,:]|=keep[:-1,:]; k[:-1,:]|=keep[1:,:]; k[:,1:]|=keep[:,:-1]; k[:,:-1]|=keep[:,1:]; keep=k & obj
    # buracos internos
    livre=~keep; alc=np.zeros((h,w),bool); q=deque()
    for x in range(w):
        for y in (0,h-1):
            if livre[y,x]: alc[y,x]=True; q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if livre[y,x] and not alc[y,x]: alc[y,x]=True; q.append((y,x))
    while q:
        cy,cx=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<h and 0<=nx<w and livre[ny,nx] and not alc[ny,nx]:
                alc[ny,nx]=True; q.append((ny,nx))
    dentro = keep | (livre & ~alc)
    alpha = np.clip((dist - tol*0.5) * 8, 0, 255).astype(np.uint8)
    alpha[~dentro] = 0; alpha[(livre & ~alc)] = 255
    img = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA')
    bb = img.getbbox()
    return img.crop(bb) if bb else img

def enquadra(recorte):
    # redimensiona p/ ALT e cola num quadro padrão com os PÉS na BASE_Y
    r = recorte.resize((max(1, int(recorte.width * ALT / recorte.height)), ALT), Image.LANCZOS)
    quadro = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    x = (CANVAS_W - r.width) // 2
    y = BASE_Y - r.height
    quadro.alpha_composite(r, (x, max(0, y)))
    return quadro

def main(nome):
    dst = os.path.join(RAIZ, 'educaverso-app', 'public', 'personagens', nome)
    os.makedirs(dst, exist_ok=True)
    feito = {}
    for pose, chaves in POSES.items():
        p = acha(nome, chaves)
        if not p:
            print('  (falta) %s' % pose); continue
        img = enquadra(recorta(p))
        o = os.path.join(dst, pose + '.png'); img.save(o, optimize=True)
        feito[pose] = pose + '.png'
        print('  OK %-14s <- %-22s %.0fKB' % (pose, os.path.basename(p), os.path.getsize(o)/1024))
    manifest = {'nome': nome, 'quadro': [CANVAS_W, CANVAS_H], 'base_y': BASE_Y, 'poses': feito}
    json.dump(manifest, open(os.path.join(dst, 'manifest.json'), 'w'), ensure_ascii=False, indent=2)
    print('Atlas de "%s": %d poses -> %s' % (nome, len(feito), dst))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'verso')
