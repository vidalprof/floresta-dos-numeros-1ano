# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DESTE CADERNO SAEM DAS FOLHAS DE PAPEL

 ⭐ Regra do Marcos (14/set/2026): *"procure na internet, nada de imagem gerada
    por IA, utilize das atividades"*. Cada figura aqui foi RECORTADA de uma
    folha colhida em 26/set/2026 (`buscar-fotos.yml`) — a MESMA folha que deu o
    gesto, sempre que a folha tinha figura.

 Folhas de origem (o crivo inteiro está em `_sequencias/POTE-DIVH4.md`):
   · `A10` (colheita/divh4a d10) — *"QUEBRA-CABEÇA DE DIVISÃO. Resolva as
     divisões do final da página. Depois, recorte as figuras de cada quadro e
     cole-as sobre o resultado de cada operação"*: as NOVE PEÇAS coloridas e o
     tabuleiro cinza com os números. Na tela a peça vai para o número e a cena
     se monta, como no papel.
   · `A31` (divh4a d31) — *"DESCUBRA O CAMINHO … traçando o caminho somente
     pelas casas em que as divisões sobram resto"*: o cachorro e a casinha.
   · `A32` (divh4a d32) — os problemas da festa junina: o balão, os pirulitos
     e a pipoca do cinema.
   · `F08` (divh4fig d08) — *"Faça seu próprio relógio. Recorte o relógio abaixo
     e fixe os ponteiros"*: o MOSTRADOR e os DOIS PONTEIROS. É o gesto da folha
     (girar os ponteiros) e a peça dele, juntos.
   · `D02` (divh4d d02) — *"O GRUPO DE BEATRIZ ORGANIZOU SEUS HORÁRIOS"*: as
     quatro cenas da rotina (limpar a sala, lições, lanche, higiene).
   · `C11` (divh4c d11) — o problema do filme da Maria: a família no sofá.

 ⚠️ PEÇA RETANGULAR NÃO PASSA PELO `limpa_fundo` (lição do `_dinheiro5`, as
    cédulas): as peças do quebra-cabeça e as cenas da rotina são QUADROS, e a
    água entraria pela borda comendo o céu e a flor branca. Elas se cortam
    por dentro da borda tracejada e ficam como estão (`quadro=1`).
 ⚠️ A CAIXA SE CONFERE NA FOLHA DE ORIGEM, nunca no PNG: o `img/RECORTE.json`
    guarda folha e caixa, e o portão `1i7` volta lá para medir.

 Uso: python3 _divh4/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "_padrao"))
from recorte_folha import (limpa_fundo, tira_halo, aperta,        # noqa: E402
                           tira_linha_impressa)

IMG = os.path.join(AQUI, "img")
COL = os.path.join(RAIZ, "_sequencias", "colheita")
PASTA = {"A": "divh4a", "B": "divh4b", "C": "divh4c", "D": "divh4d", "F": "divh4fig",
         "E": "divh4e", "G": "divh4g"}


def folha(cod):
    u"""`A10` -> a folha d10 da colheita divh4a. O sufixo de hash muda a cada
    colheita; o número não."""
    g = sorted(glob.glob(os.path.join(COL, PASTA[cod[0]], "d%sb1_*" % cod[1:])))
    if not g:
        raise SystemExit(u"nao achei a folha %s" % cod)
    return g[0]


# (nome, folha, x0, y0, x1, y1 em PIXELS da folha, quadro)
#  quadro: 0 = figura (tira o papel) · 1 = quadro retangular · 2 = figura, só a maior mancha
#  ⚠️ PIXELS e não fração: as caixas foram medidas abrindo cada folha no seu
#     tamanho natural. `quadro=1` = peça retangular (não tira fundo).
PECAS = [
    # ---- F08: "Faça seu próprio relógio" ----
    (u"dh4_mostrador", u"F08", 112, 404, 1302, 1596, 0),
    (u"dh4_ponthora",  u"F08", 106, 1650, 662, 1800, 0),
    (u"dh4_pontmin",   u"F08", 834, 1650, 1290, 1800, 0),
    # ---- A10: o quebra-cabeça (peças por dentro do tracejado) ----
    (u"dh4_qctab",    u"A10", 118, 592, 815, 1183, 1),
    (u"dh4_qc6",  u"A10", 996, 611, 1219, 801, 1),
    (u"dh4_qc5",  u"A10", 997, 911, 1217, 1099, 1),
    (u"dh4_qc7",  u"A10", 113, 1229, 335, 1418, 1),
    (u"dh4_qc8",  u"A10", 398, 1229, 619, 1418, 1),
    (u"dh4_qc4",  u"A10", 704, 1229, 926, 1418, 1),
    (u"dh4_qc2",  u"A10", 990, 1229, 1212, 1418, 1),
    (u"dh4_qc9",  u"A10", 110, 1545, 330, 1734, 1),
    (u"dh4_qc3",  u"A10", 414, 1545, 635, 1734, 1),
    (u"dh4_qc10", u"A10", 707, 1545, 928, 1734, 1),
    # ---- A31: o caminho do resto ----
    (u"dh4_cachorro", u"A31", 92, 482, 275, 722, 0),
    (u"dh4_casinha",  u"A31", 806, 1230, 996, 1434, 0),
    # ---- A32: a festa junina ----
    (u"dh4_balao",    u"A32", 500, 710, 735, 1056, 0),
    (u"dh4_pirulitos", u"A32", 1255, 898, 1548, 1150, 0),
    (u"dh4_pirulito", u"A32", 1250, 948, 1319, 1060, 2),
    # dh4_pipoca (A32) saiu: as listras brancas do balde tocam a borda e o
    # portão 0o6 as lê como halo; apagá-las estragaria o desenho.
    # ---- F24: "Observe este relógio. As pétalas marcam os minutos." ----
    (u"dh4_flor", u"F24", 60, 80, 1044, 1046, 0),
    # ---- D02: a rotina da Beatriz ----
    (u"dh4_limpar",   u"D02", 42, 331, 199, 440, 1),
    (u"dh4_licoes",   u"D02", 211, 331, 367, 440, 1),
    (u"dh4_lanche",   u"D02", 379, 331, 534, 440, 1),
    (u"dh4_higiene",  u"D02", 547, 331, 702, 440, 1),
    # ---- G06: o material dourado (pedido do Marcos, 26/set/2026) ----
    #  ⭐ UNIDADE, DEZENA e CENTENA da mesma folha, no mesmo traço: a criança vê
    #     que a barra É dez cubinhos empilhados e a placa É dez barras.
    (u"dh4_cubo",  u"G06", 250, 329, 485, 560, 0),
    (u"dh4_barra", u"G06", 1218, 139, 1308, 752, 0),
    (u"dh4_placa", u"G06", 137, 1307, 600, 1765, 0),
    # ---- C11: o filme da Maria ----
    (u"dh4_familia",  u"C11", 518, 826, 722, 1014, 0),
]


def so_a_maior(c):
    u"""Fica só a MAIOR mancha — `quadro=2`. No pirulito, o pirulito laranja de
    trás encosta no canto da caixa; nenhuma caixa retangular o tira sem cortar
    a bola rosa, então quem sai é a mancha menor, pela vizinhança."""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(c).copy()
    # ⚠️ e as duas se TOCAM: a mancha laranja encosta na rosa. O laranja da
    #    folha (R alto, azul baixo) sai antes de rotular — o rosa tem azul alto.
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    a[(r > 200) & (b < 175) & (g > 100) & (g > b - 10), 3] = 0
    marca, n = ndimage.label(a[:, :, 3] > 0)
    if n < 2:
        return c
    tam = ndimage.sum(np.ones_like(marca), marca, range(1, n + 1))
    maior = int(np.argmax(tam)) + 1
    a[(marca != maior), 3] = 0
    return Image.fromarray(a)


def main():
    if not os.path.isdir(IMG):
        os.makedirs(IMG)
    origem = {u"dh4_selo.png": u"banco:selo", u"dh4_selo_off.png": u"banco:selo",
              u"dh4_trofeu.png": u"banco:trofeu"}
    recorte, abertas = {}, {}
    so = sys.argv[1:]
    for nome, cod, x0, y0, x1, y1, quadro in PECAS:
        cam = folha(cod)
        if cam not in abertas:
            abertas[cam] = Image.open(cam).convert("RGB")
        f = abertas[cam]
        cx = (x0, y0, x1, y1)
        if so and nome not in so:
            c = Image.open(os.path.join(IMG, nome + ".png"))
        else:
            c = f.crop(cx)
            if quadro != 1:
                c = limpa_fundo(c.convert("RGBA"))
                if quadro == 2:
                    c = so_a_maior(c)
                c = tira_halo(c, voltas=2)
                c = tira_linha_impressa(c)
                c = aperta(c)
            c.thumbnail((420, 420))
            c.save(os.path.join(IMG, nome + ".png"), optimize=True)
        origem[nome + ".png"] = u"folha:%s (%s)" % (cod, os.path.relpath(cam, RAIZ))
        recorte[nome + ".png"] = {u"folha": os.path.relpath(cam, RAIZ),
                                  u"caixa": list(cx), u"tamanho": list(c.size)}
        print(u"  %-14s %s  %dx%d" % (nome, cod, c.size[0], c.size[1]))
    for arq, dado in ((u"ORIGEM.json", origem), (u"RECORTE.json", recorte)):
        io.open(os.path.join(IMG, arq), "w", encoding="utf-8").write(
            json.dumps(dado, ensure_ascii=False, indent=1, sort_keys=True) + u"\n")


if __name__ == "__main__":
    main()
