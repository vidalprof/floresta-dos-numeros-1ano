# -*- coding: utf-8 -*-
u"""PORTÃO DA SÍLABA FALADA — a sílaba tem que sair da PALAVRA, não do nada.

⚠️⚠️ POR QUE ESTE PORTÃO EXISTE (set/2026 — o Marcos ouviu e cobrou):
   *"na bate palmas das palavras, as sílabas precisam ser pronunciadas
   corretamente, ele está dizendo 'v a' ao invés de 'va'"*.

   O que tinha acontecido: o `_padrao/silabas_voz.py`, que recorta cada sílaba
   de dentro do mp3 da própria palavra, **falhou em silêncio**. O passo dele no
   `entregar.yml` tem `continue-on-error`, o aviso morreu no log da execução, e
   o app caiu na FALA DE RESERVA — a sílaba sintetizada solta. E sílaba solta
   sai errada por construção: a voz não lê som, lê PALAVRA. Entregue "VA" e o
   serviço soletra "vê-á"; entregue "ÇÃ" e ele soletra também, porque ç não
   começa palavra em português.

   Descobriu-se então que NENHUMA atividade da casa tinha os recortes — nem o
   `_alfa1`, que usa sílaba falada desde agosto. O defeito estava no ar havia
   semanas e ninguém via, porque não dá erro nenhum: o app abre, joga, o portão
   de falas passa (o texto está lá) e só a CRIANÇA ouve o problema.

   Regra da casa: defeito que chegou ao Marcos vira portão. Este é o portão.

O QUE ELE MEDE
   Para toda pasta que declara `silabas.json` (ou seja: que fala sílaba solta),
   confere que **existe um mp3 recortado para cada sílaba de cada palavra**:
   `<pasta>/audio/<prefixo>sb_<palavra>_<i>.mp3`, com tamanho de arquivo de
   verdade. Falta um? REPROVA.

   Confere também o contrário, que é o mesmo defeito visto do outro lado: se o
   `index.html` chama `falarSilaba(...)` mas a pasta **não tem** `silabas.json`,
   a atividade vai falar sílaba sintetizada — reprova igual.

Uso:  python3 _qa/silabas.py <pasta>
Códigos: 0 passou · 1 REPROVADO · 2 não consegui medir
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

MIN_BYTES = 300          # abaixo disso é arquivo vazio, não é áudio


def mede(pasta):
    pasta = pasta.rstrip("/")
    cam = os.path.join(pasta, "silabas.json")
    html = os.path.join(pasta, "index.html")
    if not os.path.exists(html):
        print(u"%s: sem index.html — nada a medir" % pasta)
        return 2

    fonte = io.open(html, encoding=u"utf-8").read()
    js = os.path.join(pasta, "folhas.js")
    if os.path.exists(js):
        fonte += io.open(js, encoding=u"utf-8").read()
    # A atividade FALA sílaba solta?
    # ⚠️ A CHAMADA, nunca a DEFINIÇÃO: a casca do caderno traz
    # `function falarSilaba(palavra, i, silaba){...}` mesmo quando nenhuma folha
    # usa. Confundir os dois reprova caderno de alfabeto e de rima, que não têm
    # sílaba nenhuma — foi o primeiro resultado deste portão.
    usa = bool(re.search(r"(?<!function )\bfalarSilaba\s*\(\s*[^)\s]", fonte))

    if not usa:
        print(u"%s -> silabas ok: esta atividade nao fala silaba solta." % pasta)
        return 0

    if not os.path.exists(cam):
        print(u"%s -> REPROVADO: o app chama `falarSilaba` mas a pasta nao tem\n"
              u"   `silabas.json`. Sem ele o `_padrao/silabas_voz.py` nao recorta\n"
              u"   nada, e a crianca ouve a silaba SINTETIZADA solta ('ve-a' em vez\n"
              u"   de 'va'). Gere o mapa no `gerar_falas.py` da atividade." % pasta)
        return 1

    dados = json.load(io.open(cam, encoding=u"utf-8"))
    mapa = dados.get(u"palavras", dados)
    prefixo = dados.get(u"prefixo", u"") if isinstance(dados, dict) else u""
    audio = os.path.join(pasta, u"audio")

    faltam, total = [], 0
    for palavra in sorted(mapa):
        for i, s in enumerate(mapa[palavra]):
            if not s:
                continue
            total += 1
            f = os.path.join(audio, u"%ssb_%s_%d.mp3" % (prefixo, palavra, i))
            if not os.path.exists(f) or os.path.getsize(f) < MIN_BYTES:
                faltam.append(u"%s[%d]=%s" % (palavra, i, s))

    if faltam:
        log = os.path.join(audio, u"_silabas-log.txt")
        recado = u""
        if os.path.exists(log):
            recado = u"\n   o que a ferramenta registrou: " + \
                io.open(log, encoding=u"utf-8").read().strip()
        print(u"%s -> REPROVADO: faltam %d recorte(s) de %d.\n"
              u"   A crianca vai ouvir a silaba SINTETIZADA solta, e ela sai errada\n"
              u"   por construcao ('va' vira 've-a'; 'ca' vira 'ce-a').\n"
              u"   primeiros: %s%s\n"
              u"   conserto: rodar o `entregar.yml` (ele chama o\n"
              u"   `_padrao/silabas_voz.py`), e CONFERIR que os mp3 vieram no commit."
              % (pasta, len(faltam), total, u", ".join(faltam[:8]), recado))
        return 1

    print(u"%s -> silabas ok: %d recorte(s), um para cada silaba falada." % (pasta, total))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(mede(sys.argv[1]))
