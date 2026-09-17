# -*- coding: utf-8 -*-
u"""
============================================================
 TIRAR O FUNDO BRANCO DA FIGURA COLHIDA — sem morder o bicho

 ⭐ PEDIDO DO MARCOS (17/set/2026): *"acho legal elas serem sem fundo nas
    atividades"*, logo depois de escolher colher as figuras da internet
    (*"procure na internet, nada de imagem gerada por IA"*).

 ⚠️⚠️ ESTE ARQUIVO EXISTE POR CAUSA DE UM DEFEITO QUE CHEGOU NA CRIANCA. O
    recortador antigo tirava fundo por LIMIAR — "pixel parecido com o fundo sai"
    — e por isso comeu o cabelo preto da vaca e o corpo cinza do rato, que sao
    escuros como o fundo preto em que elas foram geradas. O Marcos viu:
    *"na atividade a letra que muda tudo as imagens faltam pedacos, exemplo da
    vaca, rato"*.

 ⭐ A REGRA QUE NAO REPETE O ERRO, e vale para fundo de qualquer cor:
    **fundo nao e "o que parece com o fundo" — e o que parece com o fundo E SE
    ALCANCA A PARTIR DA BORDA DO QUADRO.** Enchente, nunca limiar. A mancha
    branca no meio de uma vaca malhada nao se alcanca de fora, entao fica.

 ⚠️ O PERIGO PROPRIO DO FUNDO BRANCO (e por isso o limiar e apertado, 245):
    bicho claro sobre fundo claro. Se a figura nao tiver contorno escuro, a
    enchente vaza para dentro da barriga da vaca e come metade dela. O
    `--olhar` grava um contato ANTES/DEPOIS justamente para isso ser visto, e
    o relatorio avisa quando o recorte tirou mais de 70% do quadro (sinal de
    vazamento) ou menos de 5% (sinal de que nao havia fundo branco).

 ⚠️ E O QUE NAO SE FAZ AQUI: inventar pixel. So se decide QUAIS pixels sao
    figura. Nenhuma cor nova entra.

 Uso:
   python3 _padrao/recortar_do_branco.py <arquivo|pasta> [--escrever] [--dest X]
 Sem `--escrever` ele so MEDE. Codigos: 0 ok · 1 alguma falhou · 2 nao rodei
============================================================
"""
from __future__ import print_function

import os
import sys

BRANCO = 245           # min(R,G,B) a partir daqui o pixel e "branco de fundo"
MEIO = 200             # abaixo disto ja e figura cheia; entre os dois, rampa
BEIRADA = 2            # px de transicao suave


def _carrega():
    try:
        import numpy as np
        from PIL import Image
        from scipy import ndimage as nd
        return np, Image, nd
    except ImportError as e:                                     # noqa: BLE001
        print(u"nao consegui rodar: falta numpy/Pillow/scipy (%s)" % e)
        return None, None, None


def recorta(rgb, np, nd):
    u"""Devolve (alfa 0..255, aviso). Ver o cabecalho."""
    claro = rgb.min(axis=2) >= BRANCO
    lab, n = nd.label(claro)
    if not n:
        return None, u"nao achei fundo branco nenhum"
    borda = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) \
        | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    borda.discard(0)
    if not borda:
        return None, u"o branco nao encosta na borda: nao e fundo"
    fundo = np.isin(lab, sorted(borda))

    # ⭐ A BEIRADA EM RAMPA: no anti-serrilhado o pixel e mistura do bicho com o
    #   branco. Quanto mais escuro, mais bicho. So vale perto do fundo — longe
    #   dele isto apagaria as partes claras legitimas (a cara branca da vaca).
    lum = rgb.min(axis=2).astype(float)
    rampa = np.clip((BRANCO - lum) / float(BRANCO - MEIO), 0.0, 1.0)
    alfa = np.ones(lum.shape, dtype=float)
    perto = nd.binary_dilation(fundo, iterations=BEIRADA) & ~fundo
    alfa[perto] = rampa[perto]
    alfa[fundo] = 0.0

    tirado = float(fundo.mean())
    aviso = u""
    if tirado > 0.70:
        aviso = u"TIROU %.0f%% do quadro — pode ter vazado para dentro" % (tirado * 100)
    elif tirado < 0.05:
        aviso = u"tirou so %.0f%% — provavelmente nao tinha fundo branco" % (tirado * 100)
    return (alfa * 255).astype("uint8"), aviso


def uma(caminho, dest, escrever, np, Image, nd):
    im = Image.open(caminho).convert(u"RGB")
    rgb = np.array(im)
    alfa, aviso = recorta(rgb, np, nd)
    nome = os.path.basename(caminho)
    if alfa is None:
        print(u"   %-22s %s" % (nome, aviso))
        return 1
    print(u"   %-22s %dx%d  %s" % (nome, im.width, im.height, aviso or u"ok"))
    if not escrever:
        return 0
    saida = np.dstack([rgb, alfa])
    fora = os.path.join(dest, os.path.splitext(nome)[0] + u".png")
    if not os.path.isdir(dest):
        os.makedirs(dest)
    img = Image.fromarray(saida.astype("uint8"), u"RGBA")
    # ⚠️ APARAR O QUADRO: figura colhida vem com margem, e margem transparente
    #    faz a peca aparecer pequena dentro da caixa dela no app.
    bb = img.getbbox()
    if bb:
        img = img.crop(bb)
    img.save(fora, optimize=True)
    return 0


def main():
    np, Image, nd = _carrega()
    if np is None:
        return 2
    escrever = u"--escrever" in sys.argv
    dest = u"_novo/recortadas"
    if u"--dest" in sys.argv:
        dest = sys.argv[sys.argv.index(u"--dest") + 1]
    alvos = []
    pular = False
    for a in sys.argv[1:]:
        if pular:
            pular = False
            continue
        if a == u"--dest":
            pular = True
            continue
        if not a.startswith(u"--"):
            alvos.append(a)
    if not alvos:
        print(u"uso: python3 _padrao/recortar_do_branco.py <arquivo|pasta> "
              u"[--escrever] [--dest <pasta>]")
        return 2
    arquivos = []
    for a in alvos:
        if os.path.isdir(a):
            arquivos += [os.path.join(a, f) for f in sorted(os.listdir(a))
                         if f.lower().endswith((u".png", u".jpg", u".jpeg"))]
        else:
            arquivos.append(a)
    pior = 0
    for f in arquivos:
        try:
            pior = max(pior, uma(f, dest, escrever, np, Image, nd))
        except Exception as e:                                   # noqa: BLE001
            print(u"   %-22s ERRO: %s" % (os.path.basename(f), e))
            pior = 1
    return pior


if __name__ == u"__main__":
    sys.exit(main())
