# -*- coding: utf-8 -*-
u"""
============================================================
 1q2 · TODA FALA DO `falas.json` TEM O SEU MP3?

 ⭐ POR QUE ESTE PORTÃO EXISTE — o defeito de 23/set/2026, que o carimbo NÃO
    pegou. Eu entreguei o `_sil2` duas vezes em quatro minutos (01:10 e 01:14),
    e o site foi ao ar com o texto novo e **catorze falas sem mp3**.
    ⚠️ **A CAUSA eu NÃO confirmei, e não vou inventá-la.** O que está medido: o
       commit de áudio que chegou ao repositório trazia as vozes da versão
       ANTERIOR, e as catorze do texto novo não vieram. Duas corridas do
       `entregar.yml` no ar ao mesmo tempo é a explicação provável — ler os logs
       das duas diria. **O que eu consertei não foi a causa: foi a MEDIDA.**
    e o carimbo `_status/entrega-<repo>.json` dizia `"noar":1` com o sha certo,
    porque o sha do `index.html` estava certo mesmo. **O carimbo mede a PÁGINA,
    não a voz.**

 ⚠️ E O SILÊNCIO É O DEFEITO QUE NÃO DEIXA MARCA: `new Audio(...)` de um arquivo
    que não existe não estoura, não aparece em print, não derruba portão nenhum.
    A criança toca o alto-falante e não acontece nada. Quem descobre é ela.

 ⚠️ ISTO NÃO É O PORTÃO `0i` (`_qa/vozfalta.py`). Aquele vai do CÓDIGO para o
    `falas.json` ("a chave que o app pede tem texto?"). Este vai do `falas.json`
    para o DISCO ("o texto que eu mandei gravar virou arquivo?"). São os dois
    sentidos da mesma relação, e o defeito morava no que ninguém perguntava.

 ⚠️ O MP3 ÓRFÃO NÃO REPROVA — só é contado. Texto que mudou deixa para trás o
    arquivo antigo, e nesta casa nada do antigo se apaga.

 Códigos: 0 = todas gravadas · 1 = há fala muda · 2 = não consegui medir.

 Uso: python3 _qa/voz_gravada.py <pasta>
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    cam = os.path.join(pasta, "falas.json")
    audio = os.path.join(pasta, "audio")
    if not os.path.isfile(cam):
        print(u"%s -> NAO MEDI: nao ha falas.json (atividade sem voz gravada?)." % pasta)
        return 2
    try:
        falas = json.loads(io.open(cam, encoding=u"utf-8").read())
    except Exception as e:
        print(u"%s -> NAO MEDI: o falas.json nao abriu (%s)." % (pasta, e))
        return 2
    if not isinstance(falas, list):
        print(u"%s -> NAO MEDI: o falas.json nao e uma lista." % pasta)
        return 2
    if not os.path.isdir(audio):
        print(u"%s -> REPROVADO: ha %d fala(s) no falas.json e a pasta `audio/` "
              u"nem existe. TODAS estao mudas." % (pasta, len(falas)))
        return 1

    tem = set(a[:-4] for a in os.listdir(audio) if a.endswith(u".mp3"))
    # ⚠️ arquivo de 0 byte conta como AUSENTE: uma gravacao que morreu no meio
    #    deixa o arquivo criado, e `new Audio` de um mp3 vazio tambem e silencio.
    vazios = set()
    for k in list(tem):
        try:
            if os.path.getsize(os.path.join(audio, k + u".mp3")) < 500:
                vazios.add(k)
                tem.discard(k)
        except OSError:
            tem.discard(k)

    mudas = [f for f in falas if f.get(u"id") not in tem]
    orfaos = len(tem) - (len(falas) - len(mudas))

    print(u"%s -> %d fala(s) no falas.json, %d mp3 gravado(s)"
          % (pasta, len(falas), len(tem)))
    if orfaos > 0:
        print(u"   · %d mp3 que nenhuma fala pede (texto trocado; nao se apaga "
              u"nada do antigo)" % orfaos)
    if vazios:
        print(u"   ⚠️ %d mp3 com menos de 500 bytes (gravacao que morreu no meio): %s"
              % (len(vazios), u", ".join(sorted(vazios)[:6])))
    if not mudas:
        print(u"   voz ok: toda fala do arquivo tem o seu mp3.")
        return 0

    print(u"   %d FALA(S) MUDA(S) — o alto-falante nao toca, e NAO da erro nenhum:"
          % len(mudas))
    for f in mudas[:14]:
        print(u"    - %s  %s" % (f.get(u"id"), (f.get(u"texto") or u"")[:66]))
    if len(mudas) > 14:
        print(u"    ... e mais %d" % (len(mudas) - 14))
    print(u"   conserto: acionar o `entregar.yml` para esta pasta (ele grava o que "
          u"falta). ⚠️ E NAO entregar a mesma pasta duas vezes em poucos minutos: "
          u"as duas corridas brigam pelo push e uma perde o commit de audio calada.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
