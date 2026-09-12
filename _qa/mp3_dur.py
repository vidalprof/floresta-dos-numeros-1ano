# -*- coding: utf-8 -*-
u"""
============================================================
 QUANTO TEMPO DE VOZ EXISTE, DE VERDADE — lendo os quadros do próprio mp3.

 ⚠️ POR QUE ISTO EXISTE (12/set/2026). Ordem do Marcos, em quatro palavras:
    **"Nunca chute nunca invente"**.

    O `_qa/duracao.py` calculava o tempo de voz assim:

        PAL_POR_S = 2.6      # passo da voz da casa
        segundos = palavras / PAL_POR_S

    Esse 2,6 é um número que **eu inventei**. Nunca foi cronometrado, nunca teve
    fonte, e ainda assim saía impresso no log com cara de medida — e eu o repeti
    para o Marcos como se fosse. Os mp3 estão no disco, com a duração exata
    dentro deles. Não havia nada para estimar.

 COMO ELE MEDE, sem biblioteca nenhuma
    Um mp3 é uma fila de QUADROS. Cada quadro tem um cabeçalho de 4 bytes que
    diz a versão do MPEG, a taxa de bits e a frequência; e cada quadro carrega
    um número fixo de amostras (1152 no MPEG-1, 576 no MPEG-2/2.5). Então a
    duração é `quadros × amostras / frequência`, somada quadro a quadro — o que
    também funciona em arquivo de taxa variável, onde multiplicar tamanho por
    taxa erraria.

 ⚠️ Pula a etiqueta ID3 do começo (os 4 bytes de tamanho são de 7 bits cada,
    "synchsafe" — ler como 8 bits dá um tamanho errado e o primeiro quadro se
    perde).

 Uso:  python3 _qa/mp3_dur.py <pasta/audio>     (imprime o total e a média)
       from mp3_dur import duracao, total_da_pasta
============================================================
"""
from __future__ import print_function

import os
import sys

# tabelas do padrão MPEG audio Layer III
_KBPS = {1: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0],
         2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]}
_HZ = {3: [44100, 48000, 32000],     # MPEG-1
       2: [22050, 24000, 16000],     # MPEG-2
       0: [11025, 12000, 8000]}      # MPEG-2.5


def duracao(cam):
    u"""Segundos de áudio no arquivo, contando quadro a quadro. 0.0 se não der."""
    try:
        with open(cam, "rb") as f:
            d = f.read()
    except Exception:
        return 0.0
    i = 0
    if d[:3] == b"ID3" and len(d) > 10:
        # ⚠️ synchsafe: sete bits úteis por byte
        tam = ((d[6] & 0x7F) << 21 | (d[7] & 0x7F) << 14 |
               (d[8] & 0x7F) << 7 | (d[9] & 0x7F))
        i = 10 + tam
    seg, n = 0.0, len(d)
    while i < n - 4:
        if d[i] != 0xFF or (d[i + 1] & 0xE0) != 0xE0:
            i += 1
            continue
        ver = (d[i + 1] >> 3) & 3      # 3=MPEG1 · 2=MPEG2 · 0=MPEG2.5 · 1=reservado
        camada = (d[i + 1] >> 1) & 3   # 1 = Layer III
        bi = (d[i + 2] >> 4) & 15
        fi = (d[i + 2] >> 2) & 3
        pad = (d[i + 2] >> 1) & 1
        if camada != 1 or ver == 1 or bi in (0, 15) or fi == 3:
            i += 1
            continue
        kbps = _KBPS[1 if ver == 3 else 2][bi]
        hz = _HZ[ver][fi]
        amostras = 1152 if ver == 3 else 576
        tamq = int((amostras // 8) * kbps * 1000 / hz) + pad
        if tamq <= 4:
            i += 1
            continue
        seg += amostras / float(hz)
        i += tamq
    return seg


def total_da_pasta(pasta):
    u"""(segundos somados, quantos arquivos) de todos os mp3 da pasta."""
    if not os.path.isdir(pasta):
        return 0.0, 0
    seg, n = 0.0, 0
    for f in sorted(os.listdir(pasta)):
        if f.lower().endswith(".mp3"):
            s = duracao(os.path.join(pasta, f))
            if s > 0:
                seg += s
                n += 1
    return seg, n


def por_id(pasta):
    u"""{nome do arquivo sem .mp3: segundos} — para casar com o falas.json."""
    fora = {}
    if not os.path.isdir(pasta):
        return fora
    for f in sorted(os.listdir(pasta)):
        if f.lower().endswith(".mp3"):
            fora[f[:-4]] = duracao(os.path.join(pasta, f))
    return fora


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/mp3_dur.py <pasta/audio>")
        return 2
    alvo = sys.argv[1].rstrip("/")
    if os.path.isfile(alvo):
        print(u"%s -> %.2f s" % (alvo, duracao(alvo)))
        return 0
    seg, n = total_da_pasta(alvo)
    if not n:
        print(u"%s -> nenhum mp3. NAO MEDI." % alvo)
        return 2
    print(u"%s -> %d mp3, %.1f s de voz (%.1f min); media %.2f s por fala"
          % (alvo, n, seg, seg / 60.0, seg / n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
