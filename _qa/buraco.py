#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO BURACO DE FUNDO — "sobrou preto dentro da peça?"

⭐ NASCEU DE UM DEFEITO QUE CHEGOU AO MARCOS TRÊS VEZES (set/2026):
   *"a xícara está com magenta entre a alça"*, depois *"a xícara ficou com
   ponto preto dentro da alça"*, depois *"a imagem da caneca aparece o preto
   dentro da parte entre a alça e a caneca"*. E, quando fui varrer, a tesoura
   tinha o mesmo defeito nos dois furos dos dedos — ninguém tinha visto.

   A CAUSA é sempre a mesma e é de RECORTE, não de desenho: a peça saiu de uma
   cartela de fundo preto (ou magenta) e o recorte por cor só alcança o fundo
   que está por FORA. Todo buraco FECHADO — a alça de uma caneca, o furo de uma
   tesoura, o vão de uma janela — guarda o fundo lá dentro. Na tela, a criança
   vê uma mancha preta boiando no meio do desenho.

   Achar isso a olho é impossível: são 60 figuras por atividade e o defeito é
   pequeno. Então virou MEDIDA.

⚠️ COMO ELE NÃO REPROVA DESENHO LEGÍTIMO. A primeira versão deste portão
   acusou 42 das 62 figuras — a bola de futebol (pentágonos pretos), o dado
   (pintas), o olho do gato, a base do troféu. Preto de verdade NÃO é o defeito.
   A assinatura do fundo é outra: além de fechado, o buraco é **chapado** —
   luminância média quase zero e desvio quase nulo, porque é uma cor de fundo,
   não uma superfície com luz. Arte tem sombreado; fundo não tem. Com essa
   regra o mesmo lote acusou UMA figura, e ela estava mesmo defeituosa.

Uso:
    python3 _qa/buraco.py <pasta-ou-arquivo> [...]      # mede e reprova (1)
    python3 _qa/buraco.py <pasta> --consertar           # apaga os buracos

Códigos: 0 limpo · 1 há buraco de fundo · 2 não consegui medir.
"""
from __future__ import print_function

import os
import sys
from collections import deque

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print(u"nao consegui medir: falta Pillow/numpy")
    sys.exit(2)

MIN_PIXELS = 120     # menor que isto e sujeira de recorte, nao mancha visivel
LUM_MEDIA = 26       # o fundo e quase preto puro
LUM_DESVIO = 7       # ... e CHAPADO: arte sombreada passa disto
CERCA = 0.93         # quase todo o anel em volta e peca opaca


def _blobs(cam):
    u"""Devolve (lista de blobs, imagem, matriz). Blob = lista de pixels de um
    buraco de fundo fechado."""
    im = Image.open(cam).convert("RGBA")
    a = np.array(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    lum = (r * 299 + g * 587 + b * 114) // 1000
    escuro = (lum < 45) & (al > 120)
    achados = []
    if not escuro.any():
        return achados, im, a
    vis = np.zeros(escuro.shape, bool)
    H, W = escuro.shape
    for y0, x0 in zip(*np.nonzero(escuro)):
        if vis[y0, x0]:
            continue
        fila = deque([(y0, x0)])
        vis[y0, x0] = True
        pix = []
        toca_borda = False
        while fila:
            y, x = fila.popleft()
            pix.append((y, x))
            if y in (0, H - 1) or x in (0, W - 1):
                toca_borda = True
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and escuro[ny, nx] and not vis[ny, nx]:
                    vis[ny, nx] = True
                    fila.append((ny, nx))
        if len(pix) < MIN_PIXELS or toca_borda:
            continue
        P = np.array(pix)
        L = lum[P[:, 0], P[:, 1]]
        if L.mean() > LUM_MEDIA or L.std() > LUM_DESVIO:
            continue                      # tem sombreado: e desenho, nao fundo
        y1, y2 = max(0, P[:, 0].min() - 3), min(H - 1, P[:, 0].max() + 3)
        x1, x2 = max(0, P[:, 1].min() - 3), min(W - 1, P[:, 1].max() + 3)
        if (al[y1:y2 + 1, x1:x2 + 1] > 120).mean() < CERCA:
            continue                      # nao esta cercado por peca
        achados.append(P)
    return achados, im, a


def conserta(cam):
    u"""Apaga SÓ os buracos medidos — o preto legítimo do desenho fica."""
    blobs, im, a = _blobs(cam)
    if not blobs:
        return 0
    novo = a.copy()
    total = 0
    for P in blobs:
        novo[P[:, 0], P[:, 1], 3] = 0
        total += len(P)
        # ⚠️ a beirada: os pixels vizinhos são mistura do preto com a peça e
        #    deixariam um aro escuro. Some com eles por meio-tom.
        for dy in (-2, -1, 0, 1, 2):
            for dx in (-2, -1, 0, 1, 2):
                ys = np.clip(P[:, 0] + dy, 0, a.shape[0] - 1)
                xs = np.clip(P[:, 1] + dx, 0, a.shape[1] - 1)
                lum = (novo[ys, xs, 0] * 299 + novo[ys, xs, 1] * 587 +
                       novo[ys, xs, 2] * 114) // 1000
                fraco = lum < 120
                novo[ys[fraco], xs[fraco], 3] = (
                    novo[ys[fraco], xs[fraco], 3] * np.clip(lum[fraco] / 120.0, 0, 1)
                ).astype(novo.dtype)
    Image.fromarray(novo.astype("uint8"), "RGBA").save(cam, optimize=True)
    return total


def arquivos(alvos):
    saida = []
    for t in alvos:
        if os.path.isdir(t):
            for raiz, _, fs in os.walk(t):
                for f in sorted(fs):
                    if f.lower().endswith(".png"):
                        saida.append(os.path.join(raiz, f))
        elif t.lower().endswith(".png"):
            saida.append(t)
    return saida


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    consertar = "--consertar" in sys.argv
    if not args:
        print(__doc__)
        return 2
    alvos = arquivos(args)
    if not alvos:
        print(u"nao consegui medir: nenhum .png em %s" % ", ".join(args))
        return 2
    maus = []
    for cam in alvos:
        try:
            if consertar:
                n = conserta(cam)
                if n:
                    maus.append((cam, n))
            else:
                blobs, _, _ = _blobs(cam)
                if blobs:
                    maus.append((cam, sum(len(P) for P in blobs)))
        except Exception as e:                                   # noqa: BLE001
            print(u"   nao consegui abrir %s: %s" % (cam, e))
            return 2
    if not maus:
        print(u"%d figura(s) conferida(s) -> buraco ok: nenhum fundo preso "
              u"dentro da peca." % len(alvos))
        return 0
    if consertar:
        print(u"CONSERTADAS %d figura(s):" % len(maus))
        for cam, n in maus:
            print(u"   %-40s %d px de fundo apagados" % (cam, n))
        return 0
    print(u"REPROVADO: %d figura(s) com FUNDO PRESO dentro da peca "
          u"(a crianca ve uma mancha preta):" % len(maus))
    for cam, n in sorted(maus, key=lambda x: -x[1]):
        print(u"   %-40s %6d px" % (cam, n))
    print(u"   conserto: python3 _qa/buraco.py <pasta> --consertar")
    return 1


if __name__ == "__main__":
    sys.exit(main())
