# -*- coding: utf-8 -*-
u"""
RECORTE DE FUNDO BRANCO — sem adivinhar nada.

⚠️ POR QUE NÃO USAR O `rembg` AQUI (set/2026): foi ele quem comeu a bola, o
elefante e a zebra da Oficina das Palavras. O rembg é uma rede neural que ADIVINHA
o que é figura pixel a pixel, e erra onde o desenho tem cor parecida com o fundo —
a base branca da bola, a barriga clara entre as patas do elefante.

Quando a arte vem com FUNDO BRANCO LIMPO (que é o caso de tudo que o Marcos gera),
não há nada a adivinhar: basta inundar o branco a partir das BORDAS. O branco que
está DENTRO da figura — o brilho do olho, a pata creme, o dente — a água nunca
alcança, e por isso fica intacto. É a diferença entre decidir por semelhança e
decidir por vizinhança, e é ela que evita a mordida.

Uso: python3 _padrao/recortar_fundo_branco.py <entrada> <saida.png> [--lim 238]
"""
import sys
from collections import deque
from PIL import Image, ImageFilter


def recorta(ent, sai, lim=238, suave=1):
    im = Image.open(ent).convert("RGBA")
    w, h = im.size
    px = im.load()

    def claro(x, y):
        r, g, b, _ = px[x, y]
        return r >= lim and g >= lim and b >= lim

    # a água entra pelas 4 bordas e só corre por pixel claro
    fora = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if claro(x, y) and not fora[y * w + x]:
                fora[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if claro(x, y) and not fora[y * w + x]:
                fora[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not fora[ny * w + nx] and claro(nx, ny):
                fora[ny * w + nx] = 1; q.append((nx, ny))

    alfa = Image.new("L", (w, h), 255)
    ap = alfa.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if fora[base + x]:
                ap[x, y] = 0
    if suave:                      # tira o serrilhado da borda
        alfa = alfa.filter(ImageFilter.GaussianBlur(0.7))
    im.putalpha(alfa)
    im = im.crop(im.getbbox())     # sem margem morta
    im.save(sai, optimize=True)
    return im.size


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    lim = 238
    if "--lim" in sys.argv:
        lim = int(sys.argv[sys.argv.index("--lim") + 1])
    print("  %s -> %s  %s" % (sys.argv[1], sys.argv[2],
                              recorta(sys.argv[1], sys.argv[2], lim)))
