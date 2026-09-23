# -*- coding: utf-8 -*-
u"""
============================================================
 TIRAR O FUNDO BRANCO DAS FIGURAS DESTE CADERNO

 ⭐ PEDIDO DO MARCOS (23/set/2026), olhando a capa nova: *"acho que se as
    imagens fosse sem fundo ficaria melhor"*. Ele tem razão, e eu já tinha
    contornado o problema em vez de resolvê-lo: na capa o quadrado branco
    virou "etiqueta", o que disfarça na capa e não conserta as 35 folhas.

 ⚠️ POR QUE ELAS NASCERAM COM FUNDO. São recortes das folhas de papel colhidas
    (regra da casa: a figura vem da MESMA folha que deu o gesto). O recorte saiu
    em RGB, sem canal alfa — então o branco do papel veio junto.

 ⚠️ A ÁGUA ENTRA PELA BORDA, e é isso que torna isto seguro: o `limpa_fundo`
    inunda a partir das quatro bordas, então o branco DE DENTRO da figura (a
    cara branca da vaca, a barriga do rato, o dente do porco) a água nunca
    alcança. Apagar "todo pixel branco" comeria o desenho.

 ⚠️ O QUE ELE NÃO CONSERTA: figura cujo desenho ENCOSTA na borda dos quatro
    lados não tem por onde a água entrar, e sai igual. O script diz quais
    mudaram e quais não, para eu olhar — e não ficar achando que fez.

 ⚠️ E DEPOIS DISTO: subir o `VIMG` no `index.html`, senão o navegador da escola
    continua servindo a figura velha do cache (o nome do arquivo não mudou).

 Uso: python3 _sil2/tirar_fundo.py [--valendo]
      sem `--valendo` ele só mede e não grava nada.
============================================================
"""
from __future__ import print_function

import glob
import os
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "_padrao"))
from recorte_folha import limpa_fundo, tira_halo, aperta          # noqa: E402


def transp(im):
    a = np.array(im.convert("RGBA"))[:, :, 3]
    return float((a < 40).mean())


def main():
    valendo = "--valendo" in sys.argv
    mudou, iguais, ja = [], [], []
    for cam in sorted(glob.glob(os.path.join(AQUI, "img", "*.png"))):
        nome = os.path.basename(cam)
        im = Image.open(cam)
        antes_tam, antes_tr = im.size, transp(im)
        if antes_tr > 0.02:
            ja.append(nome)
            continue
        c = limpa_fundo(im.convert("RGBA"))
        c = tira_halo(c, voltas=2)
        c = aperta(c)
        depois_tr = transp(c)
        if depois_tr < 0.02:
            # ⚠️ nao mudou: o desenho encosta nas quatro bordas e a agua nao entra
            iguais.append(nome)
            continue
        mudou.append((nome, antes_tam, c.size, depois_tr))
        if valendo:
            c.save(cam)

    for nome, a, d, tr in mudou:
        print(u"  %-16s %dx%d -> %dx%d   %.0f%% transparente" % (nome, a[0], a[1], d[0], d[1], 100 * tr))
    if iguais:
        print(u"\n  ⚠️ %d figura(s) NAO mudaram (o desenho encosta na borda, a agua nao "
              u"entra): %s" % (len(iguais), u", ".join(iguais)))
    if ja:
        print(u"  · %d ja estavam sem fundo: %s" % (len(ja), u", ".join(ja)))
    print(u"\n%d figura(s) %s" % (len(mudou), u"GRAVADAS" if valendo else
                                  u"seriam gravadas (rode com --valendo)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
