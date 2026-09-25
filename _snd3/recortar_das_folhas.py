# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DO `_snd3` SAEM DAS PROPRIAS FOLHAS COLHIDAS

 Regra do Marcos (14/set/2026): ***"procure na internet, nada de imagem gerada
 por IA, utilize das atividades"***. As quatro pecas do material dourado deste
 caderno — o cubinho, a barra, a placa e o cubo — sao recortadas da folha
 **d52**, que e um cartaz de material (nao um cartaz-com-tarefa) com as quatro
 em amarelo, grandes e limpas.

 ⚠️ A MARCA-D'AGUA DA FOLHA FICA DE FORA, e isso nao e sorte: ela esta impressa
    no RODAPE da pagina (y ~0,96), longe das quatro pecas. Recortando so as
    pecas, ela nao entra. Se um dia alguem trocar a folha de origem, conferir
    isso de novo — figura com marca-d'agua nao vai ao ar (licao de
    `_sequencias/COLHEITA-FIGURAS-21SET.md`).

 ⚠️⚠️ AS CAIXAS FORAM MEDIDAS, NAO ESCRITAS DE CABECA. A tinta das pecas e
    AMARELA e o resto da folha e preto-e-branco, entao a medida saiu de procurar
    as manchas SATURADAS (max-min dos canais > 60) e ler a caixa de cada uma.
    *Fracao chutada nao e medida* — no `_sil3` isso custou duas rodadas de
    conserto (o tatu saiu com 86x19 px).

 ⚠️ O CUBINHO VEM EM DUAS MANCHAS, e a primeira leitura pegaria so uma: a face
    de cima e amarelo-claro e a da frente e laranja, entao o detector as separa.
    A caixa aqui e a UNIAO das duas — conferida na folha ampliada.

 ⚠️ E A CAIXA AINDA CRESCE ate a tinta acabar (`cresce_caixa`), porque o
    contorno PRETO das pecas nao e saturado e ficaria de fora da medida da cor.
    A caixa se confere na FOLHA DE ORIGEM, nunca no PNG: o `aperta()` tira o
    branco de sobra e o recorte sempre sai com cara de figura inteira, mesmo
    com metade do desenho cortada (licao de 21/set/2026). O `img/RECORTE.json`
    guarda a folha e a caixa, e o portao `1i7` volta la para medir.

 Uso: python3 _snd3/recortar_das_folhas.py
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
from recorte_folha import (limpa_fundo, tira_halo, aperta,          # noqa: E402
                           tira_linha_impressa)

IMG = os.path.join(AQUI, "img")
COLHEITA = os.path.join(RAIZ, "_sequencias", "colheita", "snd3")


def folha(pref):
    u"""O nome do arquivo traz um sufixo de hash que muda a cada colheita; o
    PREFIXO (`d52b3`) e o que nao muda."""
    g = sorted(glob.glob(os.path.join(COLHEITA, pref + "_*")))
    if not g:
        raise SystemExit(u"nao achei a folha %s em %s" % (pref, COLHEITA))
    return g[0]


def cresce_caixa(im, cx, teto=2.0, lim=200):
    u"""Abre a caixa ate a TINTA acabar — sem engolir a folha.

    ⚠️ A mancha so conta se estiver 60% DENTRO da caixa inicial. Sem esse
    guarda, a linha divisoria do cartaz (que atravessa a pagina inteira)
    arrastaria a caixa ate engolir o texto da legenda. Mesmo guarda do
    `_dinheiro5`, onde o contorno arredondado de um cartao fez exatamente isso.
    """
    import numpy as np
    from scipy import ndimage as nd
    x0, y0, x1, y1 = cx
    m = 40
    ax0, ay0 = max(0, x0 - m), max(0, y0 - m)
    ax1, ay1 = min(im.width, x1 + m), min(im.height, y1 + m)
    sub = np.asarray(im.crop((ax0, ay0, ax1, ay1)).convert(u"RGB")).mean(axis=2)
    marca, quantas = nd.label(sub < lim)
    if not quantas:
        return cx
    ladox, ladoy = x1 - x0, y1 - y0
    nx0, ny0, nx1, ny1 = x0, y0, x1, y1
    for i in range(1, quantas + 1):
        ys, xs = np.where(marca == i)
        if len(ys) < 60:
            continue
        gx0, gy0 = xs.min() + ax0, ys.min() + ay0
        gx1, gy1 = xs.max() + ax0, ys.max() + ay0
        dentro = ((xs + ax0 >= x0) & (xs + ax0 <= x1) &
                  (ys + ay0 >= y0) & (ys + ay0 <= y1)).sum()
        if dentro < 0.60 * len(ys):
            continue                       # a mancha e da folha, nao da peca
        if (gx1 - gx0) > teto * ladox or (gy1 - gy0) > teto * ladoy:
            continue                       # linha que atravessa a pagina
        nx0, ny0 = min(nx0, gx0), min(ny0, gy0)
        nx1, ny1 = max(nx1, gx1), max(ny1, gy1)
    return (nx0, ny0, nx1, ny1)


# ⚠️ (nome, folha, x0, y0, x1, y1) em FRACAO da folha — MEDIDOS pela mancha de
#    cor, nunca escritos de cabeca. A folha d52 tem 1600x2263.
PECAS = [
    # ---- d52: o cartaz das quatro pecas do material dourado ----
    #  o cubinho vem em DUAS manchas (face de cima clara + face da frente
    #  laranja): esta caixa e a UNIAO das duas.
    (u"sn3_cubinho", u"d52b3", 0.176, 0.160, 0.332, 0.274),
    (u"sn3_barra",   u"d52b3", 0.838, 0.064, 0.907, 0.370),
    (u"sn3_placa",   u"d52b3", 0.094, 0.635, 0.415, 0.865),
    (u"sn3_cubo",    u"d52b3", 0.521, 0.612, 0.879, 0.865),
]


def main():
    if not os.path.isdir(IMG):
        os.makedirs(IMG)
    origem, recorte = {}, {}
    print(u"recortando %d peca(s) das folhas colhidas\n" % len(PECAS))
    for nome, pref, fx0, fy0, fx1, fy1 in PECAS:
        cam = folha(pref)
        f = Image.open(cam)
        W, H = f.size
        cx = (int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H))
        cx = cresce_caixa(f, cx)
        c = limpa_fundo(f.crop(cx).convert("RGBA"))
        c = tira_halo(c, voltas=2)
        c = tira_linha_impressa(c)
        c = aperta(c)
        c.thumbnail((400, 400))
        c.save(os.path.join(IMG, nome + ".png"))
        origem[nome + ".png"] = u"folha:%s (%s)" % (pref, os.path.basename(cam))
        recorte[nome + ".png"] = {
            u"folha": os.path.relpath(cam, RAIZ),
            u"caixa": list(cx),
            u"tamanho": list(c.size),
        }
        print(u"  %-14s %s  %dx%d" % (nome, pref, c.size[0], c.size[1]))

    for arq, dado in ((u"ORIGEM.json", origem), (u"RECORTE.json", recorte)):
        io.open(os.path.join(IMG, arq), "w", encoding="utf-8").write(
            json.dumps(dado, ensure_ascii=False, indent=1) + u"\n")
    print(u"\n%d figura(s) em %s" % (len(PECAS), IMG))


if __name__ == "__main__":
    main()
