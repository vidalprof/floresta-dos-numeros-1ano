# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DE DENTRO DAS FOLHAS DE PROFESSOR

 ⭐ ORDEM DO MARCOS (13/set/2026), dita três vezes na mesma mensagem:
    *"Lembre-se de aproveitar as imagens das atividades, tudo bem lindo e
    profissional"* · *"Se puder aproveite das próprias atividades da internet"* ·
    *"Aproveite das atividades da internet as imagens"*.

    É o mesmo caminho do Bando das Rimas, onde 37 das 56 figuras foram
    RECORTADAS das próprias folhas de professor. Vale mais que desenhar do zero
    por três motivos: a arte é de editora (bonita e coerente), ela é FIEL à
    folha que deu origem à atividade, e não depende da loteria do gerador — que
    nesta atividade já voltou em mancha uma vez.

 ⚠️ A CAIXA É GENEROSA DE PROPÓSITO. Quem aperta é o PIXEL, não o meu olho:
    caixa chutada corta o telhado ou deixa uma faixa de papel colada. Aqui a
    caixa só diz "a figura está por aqui"; o contorno exato sai da massa de
    pixels que não é branco.

 ⚠️ E A CAIXA PARA ACIMA DO RÓTULO IMPRESSO. Na primeira tentativa as palavras
    "BARRO" e "PALHA", que a folha escreve embaixo do desenho, entraram junto
    com a figura — e iriam para a tela como parte do material. Duas rodadas até
    a caixa ficar certa.

 ⚠️ O FUNDO SAI POR VIZINHANÇA, entrando pela BORDA da caixa. O branco que está
    DENTRO da figura (a janela, o brilho, a parede clara) a água nunca alcança.
    E apaga com degradê, não em seco: corte seco deixa a borda serrilhada, que é
    trocar um defeito por outro.

 DE ONDE VEIO CADA UMA (o crédito fica aqui e no `_sequencias/POTE-MORADIA.md`):
   d01 · mundoindica.com          — barraco, casa, prédio, oca, palafita, casa de barro
   d22 · pequenolobato.com.br     — tijolo, madeira, palha, barro
   d09 · minhasatividades.com     — tenda, casa de madeira
   d18 · livro didático (p. 29)   — iglu

 Uso:  python3 _casa1/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import os
import sys
from collections import deque

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_moradia")
DEST = os.path.join(AQUI, u"img")

# figura -> (folha, caixa generosa (x1,y1,x2,y2))
CORTES = {
 u"barraco":     (u"d01_324f3d.jpg", (70, 538, 232, 694)),
 u"casa":        (u"d01_324f3d.jpg", (276, 534, 447, 692)),
 u"predio":      (u"d01_324f3d.jpg", (500, 474, 702, 690)),
 u"oca":         (u"d01_324f3d.jpg", (50, 743, 244, 934)),
 u"palafita":    (u"d01_324f3d.jpg", (240, 753, 467, 930)),
 u"casabarro":   (u"d01_324f3d.jpg", (483, 780, 672, 934)),
 u"tijolo":      (u"d22_5b9b17.jpg", (496, 342, 662, 458)),
 u"madeira":     (u"d22_5b9b17.jpg", (498, 502, 662, 658)),
 # ⚠️ 784 e não 800: em 800 a palavra "PALHA" entrava junto com o feixe
 u"palha":       (u"d22_5b9b17.jpg", (476, 682, 692, 784)),
 u"barro":       (u"d22_5b9b17.jpg", (470, 852, 694, 935)),
 u"tenda":       (u"d09_5e3e7a.jpg", (175, 626, 410, 970)),
 u"casamadeira": (u"d09_5e3e7a.jpg", (975, 1245, 1335, 1490)),
 u"iglu":        (u"d18_ebfa0e.jpg", (1465, 490, 1690, 660)),
}

LIM = 236        # a partir daqui o pixel conta como "papel"
FOLGA = 5        # respiro em volta da figura, depois de apertar no pixel
MAIOR = 420      # lado máximo: a folha viva mostra no máximo ~128 px (256 no 2x)


def recorta(cam, box, saida, lim=LIM, folga=FOLGA):
    im = Image.open(cam).convert(u"RGBA")
    c = im.crop(box)
    a = np.asarray(c.convert(u"RGB")).astype(np.int16)
    massa = (a.min(axis=2) < lim)
    ys, xs = np.where(massa)
    if not len(xs):
        print(u"   !! nada de desenho dentro da caixa %s de %s" % (box, cam))
        return None
    x1, x2 = max(0, xs.min() - folga), min(c.width, xs.max() + 1 + folga)
    y1, y2 = max(0, ys.min() - folga), min(c.height, ys.max() + 1 + folga)
    c = c.crop((x1, y1, x2, y2))
    w, h = c.size
    px = c.load()

    def papel(x, y):
        r, g, b, al = px[x, y]
        return al < 16 or (r >= lim and g >= lim and b >= lim)

    vis = [[False] * h for _ in range(w)]
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if papel(x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if papel(x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    while fila:
        x, y = fila.popleft()
        r, g, b, al = px[x, y]
        if al:
            claro = (min(r, g, b) - lim) / float(255 - lim)
            px[x, y] = (r, g, b, int(al * (1.0 - max(0.0, min(1.0, claro)))))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vis[nx][ny] and papel(nx, ny):
                vis[nx][ny] = True
                fila.append((nx, ny))
    bb = c.getbbox()
    if bb:
        c = c.crop(bb)
    if max(c.size) > MAIOR:
        k = MAIOR / float(max(c.size))
        c = c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
    c.save(saida, optimize=True)
    return c


def main():
    if not os.path.isdir(FOLHAS):
        print(u"NAO MEDI: a colheita nao esta aqui (%s)." % FOLHAS)
        return 2
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    feitas, faltam = 0, []
    for nome in sorted(CORTES):
        folha, box = CORTES[nome]
        cam = os.path.join(FOLHAS, folha)
        if not os.path.exists(cam):
            faltam.append((nome, folha))
            continue
        c = recorta(cam, box, os.path.join(DEST, u"mo_%s.png" % nome))
        if c is None:
            faltam.append((nome, folha))
            continue
        feitas += 1
        print(u"   mo_%-14s %4dx%-4d  <- %s" % (nome + u".png", c.width, c.height, folha))
    print(u"_casa1 -> %d figura(s) recortada(s) das folhas de professor" % feitas)
    if faltam:
        print(u"   NAO SAIRAM: %s" % u", ".join(u"%s (%s)" % f for f in faltam))
        return 1
    return 0


if __name__ == u"__main__":
    sys.exit(main())
