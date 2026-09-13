# -*- coding: utf-8 -*-
u"""
============================================================
 TIRAR O HALO BRANCO DAS FIGURAS DE UMA ATIVIDADE

 ⭐ O DEFEITO, em uma frase: quando se recorta um desenho de cima do papel
    branco, sobra em volta dele uma casca de branco SUJO — nem tinta nem papel —
    de dois ou três pixels. Ela fica opaca, gruda na silhueta, e a figura passa a
    parecer adesivo cortado com tesoura. No creme da folha quase não se nota; em
    fundo escuro ela salta (foi assim que apareceu, na chapa de raio-X do Museu).

 ⚠️ A LIÇÃO QUE ESTE ARQUIVO EXISTE PARA NÃO DEIXAR REPETIR (13/set/2026):
    eu MEDIA o recorte com uma régua e APAGAVA com outra. O portão `_qa/halo.py`
    chama de "quase-branco" tudo acima de **225** e só perdoa o que estiver com
    alfa abaixo de **40**. O meu apagador trabalhava de 236 para cima: a faixa
    225–236 a água nem alcançava (ficava 100% opaca) e a de cima saía com alfa
    200 e tanto. Ou seja, eu deixava exatamente o que o portão vigiava.
    Aqui as duas réguas são a MESMA, de propósito, e é por isso que o resultado
    dá zero no portão: a água entra por tudo acima de `LIM_AGUA` (210) e o alfa
    chega a zero em `FADE_HI` (226) — um pixel abaixo do 225 do portão. Sobra o
    degradê 210→226 para o contorno não serrilhar.
    **Mexeu num destes números? Rode o `_qa/halo.py` depois. Sempre.**

 ⚠️ O QUE ELE NÃO FAZ, e é de propósito:
    · não toca em imagem SEM transparência (foto, fundo de tela) — ali não há
      recorte, e a água comeria o céu pela borda até esburacar a foto;
    · não entra por dentro: a água só anda a partir da BORDA, então o branco
      LEGÍTIMO de dentro da figura (a barriga do pinguim, a janela da casa, o
      jaleco do mascote) nunca é alcançado;
    · não redesenha nada. É reprocessar o PNG que já existe.

 ⚠️ E A TROCA CONSCIENTE: com a água entrando até 210, um cinza-claro do PRÓPRIO
    desenho que ENCOSTE na silhueta pode ser comido junto. É caso raro e é
    preferível ao halo, que estava em 43 de 57 figuras numa atividade e nas onze
    de folha viva. Por isso o `--folha` monta um contato-folha: o olho confere.

 Uso:
   python3 _padrao/limpar_halo.py <pasta> [...]        limpa e salva
   python3 _padrao/limpar_halo.py <pasta> --ensaio     só diz o que mudaria
   python3 _padrao/limpar_halo.py <pasta> --folha out.png   contato-folha antes|depois
============================================================
"""
from __future__ import print_function

import glob
import os
import sys
from collections import deque

from PIL import Image

# as duas réguas, iguais às do `_qa/halo.py` (ver a lição no cabeçalho)
LIM_AGUA = 210
FADE_LO, FADE_HI = 210, 226
CREME = (253, 241, 233, 255)   # o fundo da folha viva, para o contato-folha


def limpa_fundo(c):
    u"""Apaga o papel POR VIZINHANÇA, entrando pela borda, com degradê."""
    c = c.convert(u"RGBA").copy()
    w, h = c.size
    px = c.load()

    def papel(x, y):
        r, g, b, al = px[x, y]
        return al < 16 or (r >= LIM_AGUA and g >= LIM_AGUA and b >= LIM_AGUA)

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
            claro = (min(r, g, b) - FADE_LO) / float(FADE_HI - FADE_LO)
            px[x, y] = (r, g, b, int(al * (1.0 - max(0.0, min(1.0, claro)))))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vis[nx][ny] and papel(nx, ny):
                vis[nx][ny] = True
                fila.append((nx, ny))
    return c


def tem_recorte(im):
    u"""Só quem tem transparência é recorte. Foto e fundo de tela ficam de fora."""
    al = im.convert(u"RGBA").split()[-1]
    return al.getextrema()[0] < 250


def pngs(pasta):
    return sorted(glob.glob(os.path.join(pasta, u"*.png")) +
                  glob.glob(os.path.join(pasta, u"img", u"*.png")))


def contato(pares, saida):
    u"""ANTES | DEPOIS lado a lado, sobre o creme da folha — para o olho conferir."""
    from PIL import ImageDraw, ImageFont
    try:
        ft = ImageFont.truetype(u"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        ft = ImageFont.load_default()
    cel, cols = 124, 8
    linhas = (len(pares) + cols - 1) // cols
    f = Image.new(u"RGB", (cel * 2 * cols + 10, (cel + 16) * linhas + 10), (246, 244, 242))
    d = ImageDraw.Draw(f)
    for i, (nome, a, b) in enumerate(pares):
        cx = (i % cols) * cel * 2 + 5
        cy = (i // cols) * (cel + 16) + 5
        for j, im in enumerate((a, b)):
            m = im.copy()
            m.thumbnail((cel - 8, cel - 8))
            bg = Image.new(u"RGBA", (cel - 4, cel - 4), CREME)
            bg.alpha_composite(m, ((cel - 4 - m.width) // 2, (cel - 4 - m.height) // 2))
            f.paste(bg.convert(u"RGB"), (cx + j * cel, cy))
        d.text((cx + 2, cy + cel - 2), nome[:30], fill=(70, 50, 40), font=ft)
    f.save(saida, optimize=True)


def main():
    args = [a for a in sys.argv[1:]]
    ensaio = u"--ensaio" in args
    folha = None
    if u"--folha" in args:
        i = args.index(u"--folha")
        folha = args[i + 1]
        del args[i:i + 2]
    args = [a for a in args if not a.startswith(u"--")]
    if not args:
        print(u"uso: python3 _padrao/limpar_halo.py <pasta> [--ensaio] [--folha out.png]")
        return 2

    pares, total, mexidas = [], 0, 0
    for pasta in args:
        arqs = pngs(pasta.rstrip(u"/"))
        if not arqs:
            print(u"%s -> nenhum .png. NAO MEDI." % pasta)
            continue
        n = 0
        for cam in arqs:
            im = Image.open(cam).convert(u"RGBA")
            total += 1
            if not tem_recorte(im):
                continue
            novo = limpa_fundo(im)
            bb = novo.getbbox()
            if bb:
                novo = novo.crop(bb)
            antes = list(im.convert(u"RGBA").split()[-1].getdata())
            depois = list(novo.split()[-1].getdata())
            if antes == depois and novo.size == im.size:
                continue
            n += 1
            mexidas += 1
            if folha is not None and len(pares) < 96:
                pares.append((os.path.basename(cam)[:-4], im, novo))
            if not ensaio:
                novo.save(cam, optimize=True)
        print(u"%s -> %d de %d figura(s) %s" % (pasta, n, len(arqs),
                                                u"mudariam" if ensaio else u"limpas"))
    if folha is not None and pares:
        contato(pares, folha)
        print(u"contato-folha (ANTES | DEPOIS) em %s" % folha)
    print(u"total: %d figura(s) %s de %d conferida(s)"
          % (mexidas, u"a limpar" if ensaio else u"limpas", total))
    print(u"⚠️ agora rode o portao: python3 _qa/halo.py <pasta>  — sem 0 la, nao terminou.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
