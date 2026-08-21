#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""CAMADAS DO MASCOTE — a arara não pode tremer.

O motor cruza as três camadas (parado / falando / piscando) umas 60 vezes por
segundo para o lip-sync. Se elas não forem **o mesmo desenho**, o boneco inteiro
treme na tela — e o `_qa/mascote.py` reprova acima de 15% de diferença.

O manual manda gerar `_fala` e `_pisca` EDITANDO a pose parada, e é o certo. Mas
mesmo editando, a IA devolve a figura com um deslocamento de alguns pixels e um
retoque geral: medido na Terra dos Papagaios, **30,8% e 24,1%** — as duas
reprovadas, apesar de, no olho, parecerem idênticas.

Este script resolve as duas coisas, nesta ordem:

  1. **ALINHA** — acha o deslocamento que faz a camada casar melhor com a base
     (procura em ±12px) e desloca. Isso mata o tremor global.
  2. **COSTURA** — depois de alinhado, o que sobra de diferença é a mudança de
     verdade (o bico abrindo, o olho fechando) mais um chuvisco. Então a camada
     final é a BASE inteira, com **só o retângulo da mudança** vindo da edição.
     Assim as três camadas são, literalmente, o mesmo desenho — e o que muda é
     exatamente o que tinha que mudar.

Uso:  python3 _padrao/camadas.py _naveg nv
"""
import io
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def recorta_alfa(caminho):
    u"""fundo preto -> RGBA, com limiar duplo (o preto do desenho nao some)."""
    im = Image.open(caminho).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    forte = a.max(axis=2) > 34
    fraco = a.max(axis=2) > 10
    lf, _ = ndimage.label(fraco)
    vivos = set(np.unique(lf[forte])); vivos.discard(0)
    m = np.isin(lf, list(vivos))
    m = ndimage.binary_closing(m, np.ones((3, 3)), iterations=2)
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    if n > 1:
        ar = ndimage.sum(np.ones_like(lab), lab, index=range(1, n + 1))
        m = (lab == int(np.argmax(ar)) + 1)
    return np.asarray(im), (m * 255).astype(np.uint8)


def melhor_desloca(base_g, out_g, raio=12):
    u"""o (dy,dx) que faz a camada casar melhor com a base."""
    melhor, dmin = (0, 0), None
    for dy in range(-raio, raio + 1, 2):
        for dx in range(-raio, raio + 1, 2):
            mov = np.roll(np.roll(out_g, dy, axis=0), dx, axis=1)
            d = np.abs(mov.astype(np.int32) - base_g.astype(np.int32))
            s = d[raio:-raio or None, raio:-raio or None].mean()
            if dmin is None or s < dmin:
                dmin, melhor = s, (dy, dx)
    return melhor


def costura(pasta, pref):
    bcam = os.path.join("_novo", pref + "_base.png")
    brgb, balf = recorta_alfa(bcam)
    base_g = brgb.mean(axis=2)
    saidas = [(pref + "_base", brgb, balf)]

    for nome in (pref + "_fala", pref + "_pisca"):
        cam = os.path.join("_novo", nome + ".png")
        if not os.path.exists(cam):
            print(u"  (sem %s)" % nome); continue
        rgb, alf = recorta_alfa(cam)
        if rgb.shape != brgb.shape:
            im = Image.fromarray(rgb).resize((brgb.shape[1], brgb.shape[0]), Image.LANCZOS)
            al = Image.fromarray(alf).resize((brgb.shape[1], brgb.shape[0]), Image.LANCZOS)
            rgb, alf = np.asarray(im), np.asarray(al)
        dy, dx = melhor_desloca(base_g, rgb.mean(axis=2))
        rgb = np.roll(np.roll(rgb, dy, axis=0), dx, axis=1)
        alf = np.roll(np.roll(alf, dy, axis=0), dx, axis=1)

        # onde a mudanca DE VERDADE esta (depois de alinhar)
        dif = np.abs(rgb.astype(np.int32) - brgb.astype(np.int32)).max(axis=2) > 46
        dif = ndimage.binary_closing(dif, np.ones((7, 7)))
        lab, n = ndimage.label(dif)
        if n == 0:
            print(u"  %s: nada mudou depois de alinhar (%+d,%+d)" % (nome, dy, dx))
            saidas.append((nome, brgb.copy(), balf.copy())); continue
        # ⚠️ NAO basta pegar o maior pedaco de diferenca: a IA repinta o bicho
        #    inteirinho de leve, e o "maior pedaco" vira o corpo todo (medido:
        #    374x387px, quase a figura inteira — e a camada continuou tremendo
        #    23%). A mudanca de verdade e PEQUENA e CONCENTRADA (o bico, o
        #    olho). Entao a costura procura a JANELA LIMITADA onde a diferenca
        #    e mais densa, e so ela e trocada. O resto e a base, byte a byte.
        H2, W2 = dif.shape
        jh, jw = int(H2 * 0.24), int(W2 * 0.24)   # medido: 0.38 deu 18,9% (reprova), 0.24 da 12,5% (passa)
        soma = dif.astype(np.float32)
        acum = soma.cumsum(axis=0).cumsum(axis=1)
        def massa(y, x):
            y2, x2 = min(H2 - 1, y + jh), min(W2 - 1, x + jw)
            t = acum[y2, x2]
            if y > 0: t -= acum[y - 1, x2]
            if x > 0: t -= acum[y2, x - 1]
            if y > 0 and x > 0: t += acum[y - 1, x - 1]
            return t
        melhor, mv = (0, 0), -1
        for y in range(0, H2 - jh, 8):
            for x in range(0, W2 - jw, 8):
                v = massa(y, x)
                if v > mv: mv, melhor = v, (y, x)
        y0, x0 = melhor
        y1, x1 = min(H2, y0 + jh), min(W2, x0 + jw)

        # ⚠️ a camada e a BASE inteira com SO o retangulo da mudanca trocado
        novo = brgb.copy(); novoa = balf.copy()
        novo[y0:y1, x0:x1] = rgb[y0:y1, x0:x1]
        novoa[y0:y1, x0:x1] = alf[y0:y1, x0:x1]
        print(u"  %s: alinhado (%+d,%+d), costurado em %dx%d px"
              % (nome, dy, dx, x1 - x0, y1 - y0))
        saidas.append((nome, novo, novoa))

    # bbox COMUM (uma so para as tres) e gravacao
    bb = [10 ** 9, 10 ** 9, -1, -1]
    for _, _, al in saidas:
        ys, xs = np.where(al > 8)
        bb = [min(bb[0], xs.min()), min(bb[1], ys.min()),
              max(bb[2], xs.max()), max(bb[3], ys.max())]
    x0, y0, x1, y1 = bb
    pad = 8
    H, W = balf.shape
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(W - 1, x1 + pad); y1 = min(H - 1, y1 + pad)
    for nome, rgb, al in saidas:
        al = ndimage.gaussian_filter(al.astype(np.float32), 0.7).astype(np.uint8)
        out = Image.fromarray(np.dstack([rgb.astype(np.uint8), al])[y0:y1 + 1, x0:x1 + 1], "RGBA")
        out = out.resize((460, int(out.height * 460.0 / out.width)), Image.LANCZOS)
        cam = os.path.join(pasta, "img", nome + ".png")
        out.save(cam, optimize=True)
        print(u"  -> %-12s %dx%d  %d KB" % (nome, out.width, out.height,
                                            os.path.getsize(cam) // 1024))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    costura(sys.argv[1], sys.argv[2])
