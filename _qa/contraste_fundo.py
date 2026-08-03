# -*- coding: utf-8 -*-
# Auxiliar do _qa/contraste.js: le o print SO DO FUNDO e devolve, para cada
# retangulo de texto, a cor MEDIANA do fundo naquele pedaco (em JSON).
# Mediana (e nao media) porque o fundo e foto: a media inventa uma cor que
# nao existe na tela; a mediana devolve a cor que a crianca realmente ve.
import sys, json
from PIL import Image

png, dados = sys.argv[1], sys.argv[2]
im = Image.open(png).convert("RGB")
W, H = im.size
itens = json.load(open(dados, encoding="utf-8"))
# o print sai em pixels de dispositivo; o retangulo vem em pixels CSS
esc = W / 412.0

saida = []
for it in itens:
    x0 = int(it["x"] * esc); y0 = int(it["y"] * esc)
    x1 = int((it["x"] + it["w"]) * esc); y1 = int((it["y"] + it["h"]) * esc)
    x0 = max(0, min(W - 1, x0)); x1 = max(x0 + 1, min(W, x1))
    y0 = max(0, min(H - 1, y0)); y1 = max(y0 + 1, min(H, y1))
    corte = im.crop((x0, y0, x1, y1))
    px = list(corte.getdata())  # noqa
    if not px:
        saida.append(None); continue
    r = sorted(p[0] for p in px); g = sorted(p[1] for p in px); b = sorted(p[2] for p in px)
    m = len(px) // 2
    saida.append([r[m], g[m], b[m]])

print(json.dumps(saida))
