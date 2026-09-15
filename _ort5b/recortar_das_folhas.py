# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DAS FOLHAS DE PAPEL — A Loteria do S (5º ano)

 ⭐ A REGRA QUE MANDA AQUI (Marcos, 14/set/2026): *"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"*. As dezoito figuras deste
    caderno saem da MESMA folha de papel que a professora usa em sala — a d14
    (alunoseprofessores.com), cujo comando impresso é *"1) Complete as palavras
    com S ou SS."* e que traz cada palavra dentro de um quadradinho com o
    desenho ao lado. A criança reencontra na tela o desenho do papel.

 ⚠️ A GRADE NÃO FOI CHUTADA: as bordas pretas dos quadradinhos foram MEDIDAS na
    própria imagem (varredura de linhas escuras longas). Nove linhas por duas
    colunas, e os números abaixo são o que a varredura devolveu — não um palpite
    meu sobre onde a caixa deveria estar.

 ⚠️ E A ORDEM DAS PALAVRAS É A DA FOLHA, lida de cima para baixo e da esquerda
    para a direita. Trocar um nome aqui não dá erro nenhum: só faz a criança ver
    um pêssego onde a palavra diz OSSO. Conferir OLHANDO a folha de contato.

 Uso:  python3 _ort5b/recortar_das_folhas.py
 Saída: _ort5b/img/ls_*.png (fundo transparente) + a folha de conferência em
        /tmp/conferir_ls.png, que é para OLHAR, não para confiar.
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
FOLHA = os.path.join(RAIZ, u"_sequencias", u"folhas_orto5", u"d14_3b3663.png")
DEST = os.path.join(AQUI, u"img")
ID_FOLHA = u"d14"

# as mesmas réguas do recortador da casa — a água entra acima de 210 e o alfa
# zera em 226 (o `_qa/halo.py` chama de quase-branco tudo acima de 225)
LIM_AGUA = 210
FADE_LO = 210.0
FADE_HI = 226.0
LIM = 200        # o que conta como "massa preta" do desenho
FOLGA = 3
MAIOR = 260

# MEDIDOS na imagem (1414 x 2000): as bordas dos quadradinhos
LIN = [(409, 559), (586, 736), (763, 914), (940, 1091), (1117, 1268),
       (1295, 1445), (1472, 1623), (1649, 1800), (1826, 1977)]
COLX = [(29, 244), (742, 957)]
NOMES = [[u"osso", u"pessego"], [u"casaco", u"saia"], [u"bussola", u"cassino"],
         [u"sino", u"passaro"], [u"tesoura", u"serpente"], [u"dinossauro", u"salsicha"],
         [u"casa", u"pulseira"], [u"girassol", u"sapo"], [u"sorvete", u"assado"]]


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


def tira_borda(c):
    u"""Apaga a LINHA do quadradinho que sobrou colada na beirada.

    ⚠️ MEDIDO, não suposto (15/set/2026): o `_qa/sobra_da_folha.py` acusou a
       tesoura de ter "linha impressa de 145x1 px atravessando a figura" — uma
       fileira inteira, de ponta a ponta, na primeira linha do recorte. É a
       borda preta da caixa, que a folga de 4 px não alcançou naquele quadro
       (a linha do papel não está perfeitamente reta: ela entra e sai da caixa).
       No tamanho de tela ninguém vê; ampliada, é um risco preto pendurado.
    ⚠️ E a regra é DE BEIRADA, não de figura inteira: só apaga fileira que
       encosta na borda e que está quase toda escura. Uma fileira escura no MEIO
       é desenho — a haste da tesoura, por exemplo — e essa fica.
    """
    a = np.asarray(c.convert(u"RGB")).astype(np.int16)
    escuro = (a.min(axis=2) < LIM)
    h, w = escuro.shape
    corta = [0, h, 0, w]            # y1, y2, x1, x2
    while corta[0] < corta[1] and escuro[corta[0], :].mean() > 0.9:
        corta[0] += 1
    while corta[1] > corta[0] and escuro[corta[1] - 1, :].mean() > 0.9:
        corta[1] -= 1
    while corta[2] < corta[3] and escuro[:, corta[2]].mean() > 0.9:
        corta[2] += 1
    while corta[3] > corta[2] and escuro[:, corta[3] - 1].mean() > 0.9:
        corta[3] -= 1
    if corta == [0, h, 0, w]:
        return c
    return c.crop((corta[2], corta[0], corta[3], corta[1]))


def tira_fantasma(c):
    u"""Apaga a FILEIRA CINZENTA que sobra na beirada depois de limpar o fundo.

    ⚠️ MEDIDO, e só apareceu porque o portão mede com OUTRA régua (15/set/2026).
       O `tira_borda` acima olha o que é ESCURO (tinta abaixo de 200); esta
       fileira não é escura — é um cinza claro que o degrau da transparência
       deixou meio opaco, alfa por volta de 60. Invisível para mim, visível para
       o `_qa/sobra_da_folha.py`, que conta pixel com alfa acima de 40: ele
       achou na tesoura um pedaço de 145 por 1, a largura inteira da figura.
       Lição: quando duas peças medem a mesma coisa com réguas diferentes, é a
       régua do PORTÃO que manda — foi assim no halo, e é assim aqui.
    ⚠️ E a regra é de BEIRADA e de contraste: a fileira só sai se ela estiver
       cheia e a fileira de dentro estiver quase vazia. Assim a borda do
       quadradinho sai e a moldura do desenho (que continua para dentro) fica.
    """
    a = np.asarray(c.convert(u"RGBA"))
    op = a[:, :, 3] > 40
    h, w = op.shape
    y1, y2, x1, x2 = 0, h, 0, w
    for _ in range(3):
        if y2 - y1 > 4 and op[y1, x1:x2].mean() > 0.8 and op[y1 + 1, x1:x2].mean() < 0.3:
            y1 += 1
        if y2 - y1 > 4 and op[y2 - 1, x1:x2].mean() > 0.8 and op[y2 - 2, x1:x2].mean() < 0.3:
            y2 -= 1
        if x2 - x1 > 4 and op[y1:y2, x1].mean() > 0.8 and op[y1:y2, x1 + 1].mean() < 0.3:
            x1 += 1
        if x2 - x1 > 4 and op[y1:y2, x2 - 1].mean() > 0.8 and op[y1:y2, x2 - 2].mean() < 0.3:
            x2 -= 1
    if (y1, y2, x1, x2) == (0, h, 0, w):
        return c
    return c.crop((x1, y1, x2, y2))


def main():
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    if not os.path.exists(FOLHA):
        print(u"nao achei a folha colhida: %s" % FOLHA)
        return 2
    im = Image.open(FOLHA).convert(u"RGBA")

    origem, feitas = {}, []
    for r, (y1, y2) in enumerate(LIN):
        for c, (x1, x2) in enumerate(COLX):
            nome = NOMES[r][c]
            # ⚠️ +4 / -3: a borda preta do quadradinho NÃO é desenho. Sem esta
            #    folga ela entra no recorte e vira uma moldura preta na tela.
            cx = im.crop((x1 + 4, y1 + 4, x2 - 3, y2 - 3))
            cx = aperta(cx)
            if cx is None:
                print(u"  ! %s: caixa vazia" % nome)
                continue
            cx = tira_borda(cx)
            cx = aperta(cx) or cx
            cx = limpa_fundo(cx)
            bb = cx.getbbox()
            if bb:
                cx = cx.crop(bb)
            cx = tira_fantasma(cx)
            if max(cx.size) > MAIOR:
                k = MAIOR / float(max(cx.size))
                cx = cx.resize((max(1, int(cx.width * k)), max(1, int(cx.height * k))),
                               Image.LANCZOS)
            cx.save(os.path.join(DEST, u"ls_%s.png" % nome), optimize=True)
            origem[u"ls_%s.png" % nome] = u"folha:%s" % ID_FOLHA
            feitas.append((nome, cx))
            print(u"  ok %-12s %dx%d" % (nome, cx.width, cx.height))

    # ⚠️ O TROFÉU E AS ESTRELAS SÃO SELOS DA CASA, não conteúdo da folha: vêm do
    #    banco de imagens e precisam estar declarados aqui, senão o portão
    #    `_qa/figura_da_folha.py` reprova "figura no disco que ninguém declarou"
    #    toda vez que este script rodar (ele REESCREVE o ORIGEM.json inteiro).
    for selo, de in ((u"ls_trofeu.png", u"banco:trofeu"),
                     (u"ls_selo.png", u"banco:selo"),
                     (u"ls_selo_off.png", u"banco:selo")):
        if os.path.exists(os.path.join(DEST, selo)):
            origem[selo] = de

    with io.open(os.path.join(DEST, u"ORIGEM.json"), u"w", encoding=u"utf-8") as f:
        f.write(json.dumps(origem, indent=1, sort_keys=True, ensure_ascii=False))

    # ⚠️ A FOLHA DE CONFERÊNCIA É PARA OLHAR. Nenhum portão vê se o recorte ficou
    #    bonito, nem se o NOME bate com o desenho; quem vê é o olho.
    larg, alt, porlin = 170, 190, 6
    fl = Image.new(u"RGB", (larg * porlin, alt * 3), u"#f6f2e6")
    for i, (nome, c) in enumerate(feitas):
        d = c.copy()
        d.thumbnail((150, 150))
        fl.paste(d, ((i % porlin) * larg + 12, (i // porlin) * alt + 20), d)
    fl.save(u"/tmp/conferir_ls.png")
    print(u"\nfolha de conferencia: /tmp/conferir_ls.png  (OLHAR, nao confiar)")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
