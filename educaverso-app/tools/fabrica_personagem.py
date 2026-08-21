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

def _maior_com_ponte(mask, ponte=5):
    # une a máscara por uma dilatação de 'ponte' px, acha o MAIOR bloco e
    # devolve tudo que cai nesse bloco. Membros finos (colados ao corpo, mesmo
    # que por poucos px de contorno) entram; manchas soltas e distantes saem.
    h, w = mask.shape
    d = mask.copy()
    for _ in range(ponte):
        k = d.copy()
        k[1:, :] |= d[:-1, :]; k[:-1, :] |= d[1:, :]
        k[:, 1:] |= d[:, :-1]; k[:, :-1] |= d[:, 1:]
        d = k
    # rotula na grade 2x (rápido) e escolhe o maior componente
    small = d[::2, ::2]; sh, sw = small.shape
    lab = np.zeros((sh, sw), np.int32); best = 0; bestn = 0; cur = 0
    for y in range(sh):
        for x in range(sw):
            if small[y, x] and lab[y, x] == 0:
                cur += 1; n = 0; qq = deque([(y, x)]); lab[y, x] = cur
                while qq:
                    cy, cx = qq.popleft(); n += 1
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0<=ny<sh and 0<=nx<sw and small[ny,nx] and lab[ny,nx]==0:
                            lab[ny,nx] = cur; qq.append((ny,nx))
                if n > bestn: bestn, best = n, cur
    keep_s = (lab == best); big = np.zeros((sh*2, sw*2), bool)
    for oy in (0,1):
        for ox in (0,1): big[oy::2, ox::2] = keep_s
    return big[:h, :w]

def recorta(path, tol=26):
    # ------------------------------------------------------------------
    # RECORTE SEGURO (nunca corta membro):
    #  - remove SÓ o fundo que encosta na borda (flood da borda por cor),
    #    com tolerância BAIXA -> não come o contorno escuro do desenho.
    #  - NÃO usa "maior componente": um braço/perna fino que o contorno
    #    deixa fininho continua sendo mantido (era esse passo que sumia
    #    com perna/braço no estilo limpo, de contorno escuro).
    #  - preenche buracos internos (olhos/vãos que não tocam a borda).
    # REGRA GRAVADA: personagem NUNCA pode sair com membro faltando.
    # ------------------------------------------------------------------
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]], 0)
    bg = np.median(borda, 0)
    dist = np.sqrt(((a - bg) ** 2).sum(2))
    fundo = dist < tol
    # flood a partir da borda: só o fundo CONECTADO à borda vira transparente
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
    # TUDO que não é fundo-da-borda fica (inclui membros finos e ilhotas do desenho)
    keep = ~rem
    # buracos internos de fundo que NÃO tocam a borda (ficaram presos) -> preenche
    dentro = keep.copy()
    presos = fundo & ~rem          # pixels cor-de-fundo cercados pelo desenho
    dentro |= presos
    # LIMPA manchas escuras SOLTAS (sombra que a IA às vezes desenha) SEM
    # arriscar membro: une o corpo por uma PONTE de 5px e mantém só o bloco
    # principal + tudo que estiver colado/quase colado (membros finos ficam).
    corpo = _maior_com_ponte(dentro, ponte=5)
    dentro &= corpo
    presos &= corpo
    # alpha suave só na franja de transição (anti-serrilhado), sólido no miolo
    alpha = np.clip((dist - tol * 0.4) * 10, 0, 255).astype(np.uint8)
    alpha[~dentro] = 0
    alpha[presos] = 255            # buraco interno fica opaco (parte do corpo)
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
