# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DAS FOLHAS DE PAPEL — O Caso dos Sons Iguais (5º ano)

 ⭐ A REGRA QUE MANDA AQUI (Marcos, 14/set/2026): *"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"*. As seis figuras deste
    caderno saem da MESMA folha de papel que a professora usa em sala — a d03
    (SóEscola), item 7: *"Complete a cruzadinha com palavras que têm sílaba
    terminada em l"*. A criança reencontra na tela o desenho do papel.

 ⚠️ POR QUE SÓ SEIS. Este é um caderno de ORTOGRAFIA: o conteúdo dele é
    PALAVRA, não figura. As três folhas colhidas são listas de palavras e um
    texto; desenho, só na cruzadinha da d03. Enfiar figura onde o papel não tem
    seria inventar — e inventar é o que a regra zero proíbe.

 ⚠️ A SOBRA DA PAUTA. O desenho no papel vem colado na SETA e no quadradinho da
    cruzadinha. Recorte largo traz esses restos junto, e o portão
    `_qa/sobra_da_folha.py` reprova (com razão: na tela vira um risco preto sem
    sentido ao lado da figura). As caixas abaixo foram apertadas À MÃO, olhando
    a folha de conferência, até sobrar só o desenho.

 Uso:  python3 _ort5/recortar_das_folhas.py
 Saída: _ort5/img/o5_*.png (fundo transparente) + a folha de conferência em
        /tmp/conferir_o5.png, que é para OLHAR, não para confiar.
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys
from collections import deque

try:
    from PIL import Image
    import numpy as np
except ImportError as e:                                   # pragma: no cover
    print(u"preciso de Pillow+numpy (%s)" % e)
    sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
COLHEITA = os.path.join(RAIZ, u"_sequencias", u"folhas_orto5")
DEST = os.path.join(AQUI, u"img")

# as mesmas réguas do recortador da casa — água entra acima de 210, alfa zera em
# 226 (o portão do halo chama de quase-branco tudo acima de 225)
LIM_AGUA = 210
FADE_LO = 210.0
FADE_HI = 226.0
LIM = 200        # o que conta como "massa preta" do desenho
FOLGA = 3
MAIOR = 260      # ninguém precisa de mais que isto na tela

# ⚠️ AS CAIXAS, na folha d03 (1170 x 1679). Apertadas à mão contra a folha de
#    conferência: a do barril começa em x=712 para deixar de fora a seta que
#    aponta para o quadradinho "b", e vai até 818 porque a 800 ela CORTAVA a
#    aduela da direita (visto ampliando o PNG a 4x — no tamanho de tela não
#    aparecia); a do anzol termina em x=470 pelo mesmo motivo da seta. Largar
#    20 px a mais em qualquer uma traz pauta junto; apertar 20 px corta o
#    desenho. As duas coisas só se veem OLHANDO.
CAIXAS = {
    u"carretel": (425, 1155, 535, 1250),
    u"barril":   (712, 1088, 818, 1212),
    u"sal":      (265, 1245, 430, 1385),
    u"anzol":    (435, 1360, 470, 1445),
    u"anel":     (250, 1430, 337, 1535),
    u"sol":      (665, 1485, 765, 1600),
}
FOLHA = u"d03"


def papel_de(px, x, y):
    r, g, b, al = px[x, y]
    return al < 16 or (r >= LIM_AGUA and g >= LIM_AGUA and b >= LIM_AGUA)


def limpa_fundo(c):
    u"""Fundo transparente por vizinhança, entrando pelas bordas, com degradê."""
    w, h = c.size
    px = c.load()
    vis = [[False] * h for _ in range(w)]
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if papel_de(px, x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if papel_de(px, x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    while fila:
        x, y = fila.popleft()
        r, g, b, al = px[x, y]
        if al:
            claro = (min(r, g, b) - FADE_LO) / (FADE_HI - FADE_LO)
            px[x, y] = (r, g, b, int(al * (1.0 - max(0.0, min(1.0, claro)))))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vis[nx][ny] and papel_de(px, nx, ny):
                vis[nx][ny] = True
                fila.append((nx, ny))
    return c


def aperta(c):
    a = np.asarray(c.convert(u"RGB")).astype(np.int16)
    massa = (a.min(axis=2) < LIM)
    ys, xs = np.where(massa)
    if not len(xs):
        return None
    x1, x2 = max(0, xs.min() - FOLGA), min(c.width, xs.max() + 1 + FOLGA)
    y1, y2 = max(0, ys.min() - FOLGA), min(c.height, ys.max() + 1 + FOLGA)
    return c.crop((int(x1), int(y1), int(x2), int(y2)))


def main():
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    cam = os.path.join(COLHEITA, u"d03_l_r_s_cruzadinha.jpg")
    if not os.path.exists(cam):
        print(u"nao achei a folha colhida: %s" % cam)
        return 2
    im = Image.open(cam).convert(u"RGBA")

    origem, feitas = {}, []
    for nome, box in sorted(CAIXAS.items()):
        c = im.crop(box)
        c = aperta(c)
        if c is None:
            print(u"  ! %s: caixa vazia" % nome)
            continue
        c = limpa_fundo(c)
        bb = c.getbbox()
        if bb:
            c = c.crop(bb)
        if max(c.size) > MAIOR:
            k = MAIOR / float(max(c.size))
            c = c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
        saida = os.path.join(DEST, u"o5_%s.png" % nome)
        c.save(saida, optimize=True)
        origem[u"o5_%s.png" % nome] = u"folha:%s" % FOLHA
        feitas.append((nome, c))
        print(u"  ok %-10s %dx%d" % (nome, c.width, c.height))

    # ⚠️ O TROFÉU E AS ESTRELAS SÃO SELOS DA CASA, não conteúdo da folha: eles
    #    vêm do banco de imagens (a regra do reuso, do Marcos, ago/2026) e
    #    precisam estar declarados aqui, senão o portão `_qa/figura_da_folha.py`
    #    reprova "figura no disco que ninguém declarou" — e reprova de novo toda
    #    vez que este script rodar, porque ele REESCREVE o ORIGEM.json inteiro.
    for selo, de in ((u"o5_trofeu.png", u"banco:trofeu"),
                     (u"o5_selo.png", u"banco:selo"),
                     (u"o5_selo_off.png", u"banco:selo")):
        if os.path.exists(os.path.join(DEST, selo)):
            origem[selo] = de

    with io.open(os.path.join(DEST, u"ORIGEM.json"), u"w", encoding=u"utf-8") as f:
        f.write(json.dumps(origem, indent=1, sort_keys=True, ensure_ascii=False))

    # ⚠️ A FOLHA DE CONFERÊNCIA É PARA OLHAR. Nenhum portão vê se o recorte
    #    ficou bonito; quem vê é o olho.
    larg = 170
    fl = Image.new(u"RGB", (larg * max(1, len(feitas)), 200), u"#f6f2e6")
    for i, (nome, c) in enumerate(feitas):
        d = c.copy()
        d.thumbnail((150, 150))
        fl.paste(d, (i * larg + 10, 20), d)
    fl.save(u"/tmp/conferir_o5.png")
    print(u"\nfolha de conferencia: /tmp/conferir_o5.png  (OLHAR, nao confiar)")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
