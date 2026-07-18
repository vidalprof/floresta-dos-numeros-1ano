#!/usr/bin/env python3
# Monta a FOLHA DE SPRITE do Byte a partir dos quadros gerados (idle + walk_a + walk_b).
# Recorta o fundo branco (imagem INTEIRA, sem cortar membro), normaliza todos no MESMO
# tamanho de quadro com os PES na mesma linha (evita o "travado"/pulo entre quadros),
# e cola lado a lado numa unica PNG. Saida: _kit/img/byte_sheet.png (3 quadros FWxFH).
import os
from collections import deque
from PIL import Image
import numpy as np

RAIZ = '/home/user/floresta-dos-numeros-1ano'
FW, FH, ALT, BASE_Y = 200, 240, 208, 232   # quadro, altura do personagem, linha do chao

def recorta_branco(path, tol=42):
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(np.int16); h, w, _ = a.shape
    dist = np.sqrt(((a - np.array([255, 255, 255])) ** 2).sum(2)); white = dist < tol
    rem = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if white[y, x] and not rem[y, x]: rem[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x] and not rem[y, x]: rem[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and white[ny, nx] and not rem[ny, nx]:
                rem[ny, nx] = True; q.append((ny, nx))
    alpha = np.where(rem, 0, 255).astype(np.uint8)
    img = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA')
    bb = img.getbbox()
    return img.crop(bb) if bb else img

def quadro(path):
    r = recorta_branco(path)
    r = r.resize((max(1, int(r.width * ALT / r.height)), ALT), Image.LANCZOS)
    canvas = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    x = (FW - r.width) // 2
    y = BASE_Y - r.height
    canvas.alpha_composite(r, (x, max(0, y)))   # PES na BASE_Y em todos = sem pulo
    return canvas

def main():
    fontes = [('_novo/byte2d.png'), ('_novo/byte_walk_a.png'), ('_novo/byte_walk_b.png')]
    quadros = [quadro(os.path.join(RAIZ, f)) for f in fontes]
    sheet = Image.new('RGBA', (FW * len(quadros), FH), (0, 0, 0, 0))
    for i, q in enumerate(quadros):
        sheet.alpha_composite(q, (i * FW, 0))
    out = os.path.join(RAIZ, '_kit/img/byte_sheet.png')
    sheet.save(out, optimize=True)
    print('OK folha:', out, sheet.size, '(%d quadros %dx%d) %.0fKB' % (len(quadros), FW, FH, os.path.getsize(out) / 1024))

if __name__ == '__main__':
    main()
