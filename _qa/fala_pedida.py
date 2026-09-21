# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — A FALA QUE O CÓDIGO PEDE EXISTE?  (1q)

 ⭐ DEFEITO QUE CHEGOU À SALA (21/set/2026), trazido pelo Marcos:
    ***"tem palavras sendo ditas diferente do que é mostrado"*** ·
    ***"isso não pode acontecer em atividade nenhuma"***.

 ⚠️ HAVIA UM PORTÃO PARA A METADE ERRADA. O `_qa/vozfalta.py` (0i) pergunta:
    *"esta fala, que tem texto, ganhou mp3?"* — vai do TEXTO para o ÁUDIO.
    Ninguém perguntava o contrário: *"esta chave, que o código PEDE, tem
    texto?"*. E é aí que mora o silêncio, porque o `falar()` faz exatamente
    isto:

        function falar(k){ var t = FALAS[k]; if(!t) return; ... }

    Chave que não existe → **volta calado**. Sem erro no console, sem 404, sem
    nada num print. Medido em 21/set/2026, com o código já no ar:
      · `_troca2` e `_nasal2` pediam `fim` — a criança termina o caderno
        inteiro, vem o confete, e a festa é MUDA;
      · `_abc1` e `_rima1` pediam `folhaPronta` — o elogio ao fechar CADA
        folha nunca existiu.

 ⚠️ O QUE ELE MEDE: toda chave LITERAL — `falar("xxx")` — tem de existir no
    `var FALAS`. Chave montada (`falar("pal_" + w)`) ele não alcança, e é
    honesto dizer: dessa família cuida o `_qa/voz_da_palavra.py` (1p).

 ⚠️ E ELE CONHECE UMA EXCEÇÃO DE VERDADE: quando o `falar()` do caderno
    intercepta uma família antes de olhar o `FALAS` — o `_roda1` faz isso com
    `sb1_`, que vai para o recorte de sílaba e nunca para o dicionário de
    textos. Sem essa leitura o portão acusaria uma folha correta.

 Uso:  python3 _qa/fala_pedida.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/fala_pedida.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    if pasta.endswith(u".html"):
        pasta = os.path.dirname(pasta) or u"."
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: nao achei o index.html." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()
    m = re.search(r"var FALAS = (\{.*?\});", html, re.S)
    if not m:
        print(u"%s -> NAO SE APLICA: esta atividade nao tem `var FALAS`." % pasta)
        return 2
    try:
        falas = json.loads(m.group(1))
    except Exception as e:                                   # noqa: BLE001
        print(u"%s -> NAO MEDI: o `var FALAS` nao le (%s)." % (pasta, e))
        return 2

    js = html
    outro = os.path.join(pasta, u"folhas.js")
    if os.path.exists(outro):
        js += io.open(outro, encoding=u"utf-8").read()

    # as familias que o proprio `falar()` intercepta ANTES do FALAS
    atalhos = re.findall(r'indexOf\("([A-Za-z0-9_]+)"\)\s*===?\s*0', html)

    chaves = sorted(set(re.findall(r'falar\(\s*"([^"+]+)"\s*\)', js)))
    faltam = [k for k in chaves
              if k not in falas and not any(k.startswith(a) for a in atalhos)]

    print(u"%s -> a fala que o codigo pede existe: %d chave(s) literal(is)"
          % (pasta, len(chaves)))
    if atalhos:
        print(u"   (o `falar()` deste caderno atende sozinho: %s)"
              % u", ".join(sorted(set(atalhos))))
    if not faltam:
        print(u"   ok: toda chave pedida tem texto no FALAS.")
        return 0
    print(u"   REPROVADO: %d chave(s) que o app PEDE e que nao existem —" % len(faltam))
    print(u"   o `falar()` volta calado, e o silencio nao aparece em print nenhum:")
    for k in faltam:
        onde = []
        for arq in (u"index.html", u"folhas.js"):
            c = os.path.join(pasta, arq)
            if not os.path.exists(c):
                continue
            t = io.open(c, encoding=u"utf-8").read()
            i = t.find(u'falar("%s")' % k)
            if i >= 0:
                onde.append(u"%s:%d" % (arq, t[:i].count(u"\n") + 1))
        print(u"   - `%s`%s" % (k, (u"  (%s)" % u", ".join(onde)) if onde else u""))
    print(u"   Conserto: escrever a fala no `<pasta>/gerar_falas.py` e rodar")
    print(u"   `python3 <pasta>/gerar_falas.py` — o `entregar.yml` grava o mp3.")
    return 1


if __name__ == u"__main__":
    sys.exit(main())
