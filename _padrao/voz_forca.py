# -*- coding: utf-8 -*-
u"""
============================================================
 O CONSERTO DA FALA QUE SAI BAIXA — ganho puro, só nas que destoam

 ⭐ Par do portão `_qa/voz_forca.py` (0v). Ele mede; este levanta.

 ⚠️ GANHO PURO, E ISSO NÃO É DETALHE. Nada de `loudnorm`, nada de compressor:
    em áudio de menos de 400 ms o `loudnorm` do ffmpeg vira um normalizador de
    PICO (a janela de integração dele é maior que o áudio, e o gate não tem o
    que gatear) — lição já paga nos 882 recortes de sílaba, registrada no
    `_qa/kvoz.py`. Aqui é uma multiplicação: `volume=<delta>dB`. A fala continua
    com a mesma forma, só mais perto das irmãs.

 ⚠️ SÓ AS QUE DESTOAM. Normalizar as 700 reescreveria 700 arquivos binários a
    cada rodada e o `.git` incharia — e o histórico inchado é justamente o que
    faz o build do Pages engasgar (está no `CLAUDE.md`). Tocar em 2 ou 3 por
    caderno resolve o que a criança ouve e não mexe no resto.

 ⚠️ E NUNCA ATÉ O TETO: o alvo é a MEDIANA do caderno, não 0 dB. Empurrar para
    0 satura a voz, e voz saturada é pior que voz baixa.

 Uso:  python3 _padrao/voz_forca.py <pasta> [<pasta2> ...]
       python3 _padrao/voz_forca.py --todas        (todos os cadernos com audio/)
============================================================
"""
from __future__ import print_function

import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, u"_qa"))
from voz_forca import mede, TOLERANCIA_DB                  # noqa: E402


def levanta(cam, ganho_db):
    u"""multiplica o arquivo por um ganho fixo, mantendo o resto igual."""
    tmp = tempfile.mktemp(suffix=u".mp3")
    r = subprocess.run([u"ffmpeg", u"-hide_banner", u"-loglevel", u"error",
                        u"-i", cam, u"-af", u"volume=%.2fdB" % ganho_db,
                        u"-codec:a", u"libmp3lame", u"-q:a", u"4", tmp],
                       capture_output=True, text=True)
    if r.returncode or not os.path.exists(tmp) or os.path.getsize(tmp) < 500:
        if os.path.exists(tmp):
            os.remove(tmp)
        return False
    shutil.move(tmp, cam)
    return True


def uma(pasta):
    pasta = pasta.rstrip(u"/")
    med, vals = mede(pasta)
    if med is None:
        print(u"%-10s NAO MEDI: %s" % (pasta, vals))
        return 0
    baixas = [v for v in vals if v[0] < med - TOLERANCIA_DB]
    if not baixas:
        print(u"%-10s ok (mediana %.1f dB, %d mp3) — nada a levantar"
              % (pasta, med, len(vals)))
        return 0
    feitas = 0
    for p, ident, texto in baixas:
        cam = os.path.join(pasta, u"audio", ident + u".mp3")
        ganho = med - p
        if levanta(cam, ganho):
            feitas += 1
            print(u"%-10s %-12s %5.1f dB -> %5.1f dB (+%.1f)  %r"
                  % (pasta, ident, p, med, ganho, texto[:40]))
        else:
            print(u"%-10s %-12s FALHOU ao levantar" % (pasta, ident))
    return feitas


def main():
    alvos = sys.argv[1:]
    if not alvos:
        print(u"uso: python3 _padrao/voz_forca.py <pasta> [...]  |  --todas")
        return 2
    if alvos == [u"--todas"]:
        alvos = sorted(d for d in os.listdir(RAIZ)
                       if d.startswith(u"_") and os.path.isdir(os.path.join(RAIZ, d, u"audio"))
                       and os.path.exists(os.path.join(RAIZ, d, u"falas.json")))
    total = 0
    for a in alvos:
        total += uma(a)
    print(u"\n%d fala(s) levantada(s). Reconferir com `python3 _qa/voz_forca.py <pasta>`."
          % total)
    return 0


if __name__ == u"__main__":
    sys.exit(main())
