# -*- coding: utf-8 -*-
u"""
TIRAR O HALO BRANCO — o fundo que grudou na silhueta no recorte.

⚠️ O que o portão `_qa/halo.py` mede: a orla de pixels quase-brancos que sobra
   colada no contorno quando o recorte para cedo. Na tela clara quase não se vê;
   no fundo colorido da folha vira um contorno leitoso em volta do desenho.

⚠️ POR VIZINHANÇA, NÃO POR SEMELHANÇA — é a mesma lição do
   `recortar_fundo_branco.py`, paga quando o `rembg` comeu a bola e a barriga do
   elefante: aqui a água entra pela BORDA da imagem e só atravessa pixel
   transparente ou quase-branco. O branco que está DENTRO da figura (o brilho do
   olho, o dente, a pata creme) a água nunca alcança, então fica intacto.

⚠️ E ela apaga com DEGRADÊ, não de uma vez: o pixel alcançado perde alfa na
   proporção de quão branco é. Cortar em seco deixa a borda serrilhada, que é
   trocar um defeito por outro.

Uso: python3 _padrao/tirar_halo.py <pasta/img> [--lim 232]
"""
from __future__ import print_function

import os
import sys
from collections import deque

from PIL import Image


def tira(cam, lim=232):
    im = Image.open(cam).convert("RGBA")
    w, h = im.size
    px = im.load()

    def passavel(x, y):
        r, g, b, a = px[x, y]
        if a < 16:
            return True                       # já é fundo
        return r >= lim and g >= lim and b >= lim

    vistos = [[False] * h for _ in range(w)]
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if passavel(x, y) and not vistos[x][y]:
                vistos[x][y] = True
                fila.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if passavel(x, y) and not vistos[x][y]:
                vistos[x][y] = True
                fila.append((x, y))

    mudou = 0
    while fila:
        x, y = fila.popleft()
        r, g, b, a = px[x, y]
        if a >= 16:
            # quanto mais branco, mais apaga — degradê, para não serrilhar
            claro = (min(r, g, b) - lim) / float(255 - lim)
            novo = int(a * (1.0 - max(0.0, min(1.0, claro))))
            if novo < a:
                px[x, y] = (r, g, b, novo)
                mudou += 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vistos[nx][ny] and passavel(nx, ny):
                vistos[nx][ny] = True
                fila.append((nx, ny))
    if mudou:
        im.save(cam, optimize=True)
    return mudou


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _padrao/tirar_halo.py <pasta/img> [--lim 232]")
        return 2
    alvo = sys.argv[1]
    lim = 232
    if u"--lim" in sys.argv:
        lim = int(sys.argv[sys.argv.index(u"--lim") + 1])
    arqs = ([alvo] if os.path.isfile(alvo)
            else [os.path.join(alvo, f) for f in sorted(os.listdir(alvo))
                  if f.lower().endswith(u".png")])
    total = 0
    for a in arqs:
        n = tira(a, lim)
        if n:
            total += 1
            print(u"   %s: %d pixel(s) de halo apagados" % (os.path.basename(a), n))
    print(u"%s -> halo tirado de %d figura(s) de %d" % (alvo, total, len(arqs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
