# -*- coding: utf-8 -*-
u"""
============================================================
 O CONTATO-FOLHA DO CRIVO — as folhas de papel que passaram

 ⭐ ORDEM DO MARCOS (14/set/2026): *"sempre mostre as folhas das atividades que
    encontrou, que passaram pelo crivo do especialista"*. É a seção 2b do
    `SEQUENCIAS-DIDATICAS.md`: o contato-folha vai JUNTO com o caderno, na mesma
    mensagem, nunca só o link. Ele é a prova de que o gesto da tela veio do papel
    e não da minha cabeça.

 ⚠️ NADA DE EMOJI NA LEGENDA. A fonte do runner (DejaVu) não tem os desenhos
    coloridos, e eles saem como QUADRADINHOS VAZIOS — foi o que aconteceu na
    primeira folha dos reinos. Legenda é texto, e texto tem que ler.

 Uso: python3 _sequencias/contato_crivo.py <assunto> <pasta-das-folhas> \\
          [--por-folha 4] [--cols 4] [--titulo "AS %d FOLHAS COLHIDAS"]
      As legendas saem de `<assunto>.txt` ao lado (uma linha por folha:
      `d07|a COROA dos 5 reinos: marque as caracteristicas`), ou do nome do
      arquivo quando o .txt não existir.
============================================================
"""
from __future__ import print_function

import glob
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, u"crivo")
FONTES = [u"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          u"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def fonte(tam, negrito=False):
    cam = FONTES[0] if negrito else FONTES[-1]
    try:
        return ImageFont.truetype(cam, tam)
    except Exception:
        return ImageFont.load_default()


def quebra(texto, fnt, larg, dr):
    u"""quebra o texto em linhas que cabem em `larg` pixels."""
    linhas, atual = [], u""
    for pal in texto.split():
        tenta = (atual + u" " + pal).strip()
        if dr.textlength(tenta, font=fnt) <= larg:
            atual = tenta
        else:
            if atual:
                linhas.append(atual)
            atual = pal
    if atual:
        linhas.append(atual)
    return linhas


def main():
    if len(sys.argv) < 3:
        print(u"uso: python3 _sequencias/contato_crivo.py <assunto> <pasta-das-folhas>")
        return 2
    assunto = sys.argv[1]
    pasta = sys.argv[2]
    cols = 4
    por_folha = 8
    # ⭐ --titulo (15/set/2026). A ordem do Marcos ficou mais larga: *"sempre me
    #    mostre as atividades que vc colheu"* — ou seja, mostra-se a COLHEITA
    #    INTEIRA, antes de escolher, e não só as aprovadas da entrega (§2b).
    #    O título era fixo em "AS QUE PASSARAM NO CRIVO"; numa folha de contato
    #    da colheita isso seria MENTIRA na faixa verde, bem grande. Agora o
    #    chamador diz o que a folha é, e o padrão continua o de antes.
    titulo = None
    rotulo = u"aprovadas"          # entra no NOME do arquivo de saída
    if u"--titulo" in sys.argv:
        titulo = sys.argv[sys.argv.index(u"--titulo") + 1]
        rotulo = u"colheita"       # senão o arquivo se chamaria "aprovadas" também
    if u"--rotulo" in sys.argv:
        rotulo = sys.argv[sys.argv.index(u"--rotulo") + 1]
    if u"--cols" in sys.argv:
        cols = int(sys.argv[sys.argv.index(u"--cols") + 1])
    if u"--por-folha" in sys.argv:
        por_folha = int(sys.argv[sys.argv.index(u"--por-folha") + 1])

    legendas = {}
    cam_txt = os.path.join(AQUI, assunto + u".txt")
    ordem = []
    if os.path.exists(cam_txt):
        for lin in io.open(cam_txt, encoding=u"utf-8"):
            lin = lin.strip()
            if not lin or u"|" not in lin:
                continue
            cod, rot = lin.split(u"|", 1)
            legendas[cod.strip()] = rot.strip()
            ordem.append(cod.strip())
    if not ordem:
        print(u"NAO MEDI: sem %s — nao sei quais folhas passaram no crivo." % cam_txt)
        return 2

    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)

    # ⚠️ LEG_H de 74 dava 3 linhas e o veredito da colheita cortava no meio de
    #    uma palavra (medido em 15/set, contato-folha do Inglês). 4 linhas é o
    #    que cabe um veredito inteiro; o texto completo continua no POTE.
    CEL_W, CEL_H, LEG_H = 390, 560, 96
    MAX_LIN = 4
    MARG, TOPO = 14, 86
    f_tit = fonte(30, True)
    f_sub = fonte(16)
    f_cod = fonte(19, True)
    f_leg = fonte(15)

    feitas, pag = [], []
    for cod in ordem:
        achou = sorted(glob.glob(os.path.join(pasta, cod + u"_*")))
        if not achou:
            print(u"   ! nao achei a folha %s em %s" % (cod, pasta))
            continue
        pag.append((cod, achou[0]))
        if len(pag) == por_folha:
            feitas.append(pag)
            pag = []
    if pag:
        feitas.append(pag)
    if not feitas:
        print(u"NAO MEDI: nenhuma folha encontrada em %s." % pasta)
        return 2

    quantas = sum(len(p) for p in feitas)
    saidas = []
    for n, grupo in enumerate(feitas, 1):
        linhas = (len(grupo) + cols - 1) // cols
        W = MARG + cols * (CEL_W + MARG)
        H = TOPO + linhas * (CEL_H + LEG_H + MARG) + MARG
        im = Image.new(u"RGB", (W, H), u"#f2f4f8")
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, W, 70], fill=u"#1f7a4d")
        dr.text((MARG + 6, 14),
                (titulo % quantas if titulo and u"%d" in titulo
                 else titulo or
                 u"AS %d FOLHAS DE PAPEL QUE PASSARAM NO CRIVO" % quantas),
                font=f_tit, fill=u"#ffffff")
        dr.text((MARG + 8, 48),
                u"%s  ·  folha %d de %d  ·  %s"
                % (assunto.replace(u"-", u" "), n, len(feitas),
                   u"embaixo de cada uma, o VEREDITO do crivo" if titulo
                   else u"cada uma com o que ela vira no caderno"),
                font=f_sub, fill=u"#d9f0e3")
        for i, (cod, cam) in enumerate(grupo):
            cx = MARG + (i % cols) * (CEL_W + MARG)
            cy = TOPO + (i // cols) * (CEL_H + LEG_H + MARG)
            dr.rectangle([cx, cy, cx + CEL_W, cy + CEL_H], fill=u"#ffffff",
                         outline=u"#d7dbe6")
            try:
                f = Image.open(cam).convert(u"RGB")
                f.thumbnail((CEL_W - 16, CEL_H - 16), Image.LANCZOS)
                im.paste(f, (cx + (CEL_W - f.width) // 2,
                             cy + (CEL_H - f.height) // 2))
            except Exception as e:
                dr.text((cx + 10, cy + 10), u"(nao abriu: %s)" % e, font=f_leg,
                        fill=u"#b03030")
            dr.text((cx + 2, cy + CEL_H + 6), cod.upper(), font=f_cod, fill=u"#1f7a4d")
            larg = dr.textlength(cod.upper(), font=f_cod) + 10
            for k, lin in enumerate(quebra(legendas.get(cod, u""), f_leg,
                                           CEL_W - larg - 4, dr)[:MAX_LIN]):
                dr.text((cx + 2 + larg, cy + CEL_H + 8 + k * 19), lin,
                        font=f_leg, fill=u"#3b4059")
        cam_out = os.path.join(SAIDA, u"%s-%s-%d.png" % (assunto, rotulo, n))
        im.save(cam_out, optimize=True)
        saidas.append(cam_out)
        print(u"   %s" % cam_out)
    print(u"contato-folha do crivo: %d folha(s) de papel em %d imagem(ns)"
          % (quantas, len(saidas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
