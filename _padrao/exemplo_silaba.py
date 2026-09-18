# -*- coding: utf-8 -*-
u"""
============================================================
 O EXEMPLO PARA O MARCOS OUVIR — a palavra inteira e ela dividida

 PEDIDO DELE (17/set/2026): *"então faça um exemplo para eu ver, uma palavra
 toda, e ela dividida em sílaba"*.

 ⭐ ESTE ARQUIVO NAO REIMPLEMENTA NADA. Ele chama as MESMAS funcoes que gravam
    os cadernos (`_grava` e `_recorta` do `_padrao/silabas_voz.py`). Se eu
    escrevesse uma versao "so para a demonstracao", o que ele ouviria nao seria
    o que a crianca ouve — e demonstracao que nao e a coisa e propaganda.

 O que sai em `_pesquisa/exemplo-silaba/`, por palavra:

   <palavra>_1_palavra-inteira.mp3   a gravacao crua, como a voz leu (a FONTE)
   <palavra>_2_silabas.mp3           os recortes tocados em fila, com pausa
   <palavra>_3_<i>_<SILABA>.mp3      cada recorte sozinho, como o app toca
   <palavra>_4_COMO-ERA-ERRADO.mp3   o mesmo, do jeito que saiu SOLETRADO em
                                     16:06 — so quando ha o arquivo guardado

 Uso:  python3 _padrao/exemplo_silaba.py [palavra:SI-LA-BA ...]
 Codigos: 0 gravou · 2 nao consegui rodar (falta edge-tts: roda no workflow)
============================================================
"""
from __future__ import print_function

import asyncio
import importlib.util
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SAIDA = os.path.join(RAIZ, u"_pesquisa", u"exemplo-silaba")
GUARDADO = os.path.join(RAIZ, u"_pesquisa", u"silabas-soletradas")

# ⚠️ As tres escolhidas nao sao ao acaso:
#    BOLA   — a que o Marcos ouviu errada ("bo" virando "be-o"), e a que tem o
#             recorte SOLETRADO guardado para comparar;
#    CAVALO — tres silabas, e a palavra da prova de bancada do alinhamento;
#    ESCOLA — a que ele reclamou em 16/set: *"e falado e s co la e nao es"*.
#             Silaba fechada (ES) e a armadilha da divisao.
PADRAO = [(u"bola", [u"BO", u"LA"]),
          (u"cavalo", [u"CA", u"VA", u"LO"]),
          (u"escola", [u"ES", u"CO", u"LA"])]
VOZ = u"pt-BR-AntonioNeural"


def _carrega():
    sp = importlib.util.spec_from_file_location(
        "sv", os.path.join(AQUI, "silabas_voz.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _fila(sv, ff, pecas, destino, pausa=0.35):
    u"""Toca os recortes em fila, com uma pausa entre eles — e a fila que mostra
    a divisao. A pausa e de 0,35 s porque e mais ou menos o tempo que a
    professora deixa entre uma palma e outra."""
    if not pecas:
        return False
    mudo = destino + u"_silencio.mp3"
    subprocess.call([ff, "-y", "-loglevel", "error", "-f", "lavfi",
                     "-i", "anullsrc=r=24000:cl=mono", "-t", "%.2f" % pausa,
                     "-c:a", "libmp3lame", "-q:a", "5", mudo])
    lista = destino + u"_lista.txt"
    with open(lista, "w") as fh:
        for k, p in enumerate(pecas):
            if k:
                fh.write("file '%s'\n" % os.path.abspath(mudo))
            fh.write("file '%s'\n" % os.path.abspath(p))
    subprocess.call([ff, "-y", "-loglevel", "error", "-f", "concat",
                     "-safe", "0", "-i", lista,
                     "-c:a", "libmp3lame", "-q:a", "5", destino])
    for x in (mudo, lista):
        try:
            os.remove(x)
        except OSError:
            pass
    return os.path.exists(destino)


async def _uma_palavra(sv, edge_tts, palavra, silabas):
    ff = sv._ffmpeg()
    tmp = os.path.join(SAIDA, u"_tmp_" + palavra)
    inteiro = os.path.join(SAIDA, u"%s_1_palavra-inteira.mp3" % palavra)

    # ⭐ O MESMO PEDIDO DO CADERNO: a palavra inteira, ponto final, RATE -25%.
    #    E o primeiro caminho de `CAMINHOS_DE_PEDIR`, que e o `corrida`.
    nome_cam, monta = sv.CAMINHOS_DE_PEDIR[0]
    if nome_cam != u"corrida":
        print(u"   ATENCAO: o primeiro caminho virou `%s` — o exemplo deixaria "
              u"de mostrar a esteira de verdade." % nome_cam)
    if not await sv._grava(edge_tts, monta(silabas), VOZ, inteiro):
        print(u"   %s: a voz nao devolveu audio" % palavra)
        return 0

    # ⭐ E O MESMO CORTE: alinhamento forcado sobre a palavra inteira.
    feitos = sv._recorta(ff, inteiro, silabas, SAIDA, u"", tmp_nome(palavra), True)
    if len(feitos) != len(silabas):
        print(u"   %s: sairam %d de %d recortes" % (palavra, len(feitos), len(silabas)))
        return 0

    # ⭐ A FORMA DE CITACAO, como nos cadernos (decisao do Marcos, 18/set/2026)
    apart = os.path.join(SAIDA, u"%s_1b_apartada.mp3" % palavra)
    formas = [u"palavra"] * len(silabas)
    if await sv._grava(edge_tts, u", ".join(silabas).lower() + u".", VOZ, apart):
        formas = sv._troca_por_citacao(ff, apart, silabas, feitos, SAIDA, u"", tmp_nome(palavra))
    print(u"   %s: formas %s" % (palavra.upper(), u", ".join(u"%s=%s" % (s, f) for s, f in zip(silabas, formas))))
    renomeados = []
    for i, s in enumerate(silabas):
        novo = os.path.join(SAIDA, u"%s_3_%d_%s.mp3" % (palavra, i + 1, s))
        os.replace(feitos[i], novo)
        renomeados.append(novo)
    _fila(sv, ff, renomeados, os.path.join(SAIDA, u"%s_2_silabas.mp3" % palavra))

    # O CONTRASTE, quando existe: como a mesma palavra saiu SOLETRADA em 16:06.
    ruins = []
    if os.path.isdir(GUARDADO):
        for f in sorted(os.listdir(GUARDADO)):
            if u"_sb_%s_" % palavra in f:
                ruins.append(os.path.join(GUARDADO, f))
        # so um caderno, para nao repetir a mesma peca
        if ruins:
            marca = os.path.basename(ruins[0]).split(u"__")[0]
            ruins = [f for f in ruins if os.path.basename(f).startswith(marca)]
    if len(ruins) == len(silabas):
        _fila(sv, ff, ruins,
              os.path.join(SAIDA, u"%s_4_COMO-ERA-ERRADO.mp3" % palavra))
        print(u"   %s: %d recortes + o contraste do jeito errado"
              % (palavra.upper(), len(silabas)))
    else:
        print(u"   %s: %d recortes (sem contraste guardado)"
              % (palavra.upper(), len(silabas)))
    return 1


def tmp_nome(palavra):
    return palavra


async def _tudo(alvos):
    import edge_tts
    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    sv = _carrega()
    sv._carrega_alinhador()
    n = 0
    for palavra, silabas in alvos:
        n += await _uma_palavra(sv, edge_tts, palavra, silabas)
    return 0 if n == len(alvos) else 1


def main():
    alvos = []
    for a in sys.argv[1:]:
        if u":" in a:
            w, s = a.split(u":", 1)
            alvos.append((w.strip().lower(), [x for x in s.upper().split(u"-") if x]))
    if not alvos:
        alvos = PADRAO
    try:
        import edge_tts                                          # noqa: F401
    except ImportError:
        print(u"nao consegui rodar: falta o edge-tts (isto roda no workflow)")
        return 2
    return asyncio.run(_tudo(alvos))


if __name__ == u"__main__":
    sys.exit(main())
