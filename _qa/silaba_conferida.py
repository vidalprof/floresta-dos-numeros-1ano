# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1y — A VOZ SE CONFERIU SOZINHA? (e o Marcos nao teve de ouvir)

 ⭐ ORDEM DO MARCOS (17/set/2026): *"eu preciso de uma ferramenta ou metodo que
    deixe tudo isso correto SEM EU TER QUE PRECISAR OUVIR"*.

 Ele esta certo, e o que havia antes era indefensavel: quem descobria que a
 silaba saiu errada era ELE, na sala, com a crianca na frente. Isso nao e
 portao — e sorte.

 O METODO, em uma linha: **a gravacao conta os pedacos falados no proprio audio
 e so aceita o que bate com o numero de silabas.** Os dois defeitos historicos
 caem na mesma peneira, sem ouvido nenhum:

     · a voz juntou tudo  -> pedacos DE MENOS   (SAPO saia como um bloco so)
     · a voz SOLETROU     -> pedacos DE MAIS    ("esse-a" no lugar de "sa")

 Quem faz isso e o `_padrao/silabas_voz.py` na hora de gravar: ele tenta os
 caminhos (`es co la` · `es ... co ... la` · `es, co, la.` · `escola`) e para no
 primeiro que se confere. O recibo fica em `<pasta>/audio/_conferencia.json`.

 ESTE PORTAO LE O RECIBO. Ele reprova quando:
   1. nao ha recibo (a voz foi gravada antes deste metodo existir);
   2. alguma palavra ficou em `nao_conferidas`;
   3. o recibo esta velho — ha palavra no `silabas.json` que ele nao menciona.

 ⚠️ O QUE ELE NAO FAZ: julgar se a pronuncia esta BONITA. Ele garante que a voz
    disse o numero certo de pedacos, nao que o timbre agrade. Para a
    alfabetizacao e o que importa: a crianca precisa ouvir TRES pedacos em
    ES-CO-LA, cada um com som.

 ⚠️ E ele depende de o runner ter `librosa` na hora da gravacao. Sem ele o
    `silabas_voz.py` escreve "sem librosa: NAO CONFERI" — e isto reprova aqui,
    de proposito: nao medir nunca e "passou".

 Uso:  python3 _qa/silaba_conferida.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys


def confere(pasta):
    sj = os.path.join(pasta, u"silabas.json")
    if not os.path.exists(sj):
        return 2, [u"   sem `silabas.json`: este caderno nao fala silaba. NAO MEDI"]
    try:
        palavras = json.load(io.open(sj, encoding=u"utf-8")).get(u"palavras") or {}
    except ValueError:
        return 2, [u"   `silabas.json` ilegivel: NAO MEDI"]
    if not palavras:
        return 0, [u"   nenhuma palavra registrada: nada a conferir"]

    rec = os.path.join(pasta, u"audio", u"_conferencia.json")
    if not os.path.exists(rec):
        if not os.path.isdir(os.path.join(pasta, u"audio")):
            return 2, [u"   a voz ainda nao foi gravada (sem pasta `audio/`): "
                       u"NAO MEDI. Ela nasce no `entregar.yml`."]
        return 1, [u"   REPROVADO: nao ha recibo de conferencia "
                   u"(`audio/_conferencia.json`).",
                   u"   Esta voz foi gravada ANTES de a gravacao passar a se "
                   u"conferir sozinha. Regrave: apague `audio/_silabas.json` e "
                   u"rode o `entregar.yml`.",
                   u"   Sem o recibo, a unica garantia de que a silaba sai certa "
                   u"e alguem OUVIR — e e exatamente isso que o Marcos pediu "
                   u"para nao precisar mais fazer."]
    try:
        R = json.load(io.open(rec, encoding=u"utf-8"))
    except ValueError:
        return 1, [u"   REPROVADO: o recibo `audio/_conferencia.json` esta ilegivel"]

    ok = {x.get(u"palavra"): x for x in (R.get(u"conferidas") or [])}
    ruins = R.get(u"nao_conferidas") or []
    faltam = [w for w in sorted(palavras)
              if w not in ok and not any(y.get(u"palavra") == w for y in ruins)]

    L = [u"   recibo: voz `%s`, rate `%s`" % (R.get(u"voz"), R.get(u"rate"))]
    por_caminho = {}
    for x in ok.values():
        c = x.get(u"caminho")
        por_caminho[c] = por_caminho.get(c, 0) + 1
    if por_caminho:
        L.append(u"   %d palavra(s) conferidas pela propria gravacao (%s)"
                 % (len(ok), u", ".join(u"`%s` x%d" % (k, v)
                                        for k, v in sorted(por_caminho.items()))))
    ruim = 0
    if ruins:
        ruim = 1
        L.append(u"   REPROVADO: %d palavra(s) que a gravacao NAO conseguiu "
                 u"conferir:" % len(ruins))
        for x in ruins[:12]:
            L.append(u"      • %-12s %s" % (str(x.get(u"palavra")).upper(),
                                            x.get(u"motivo")))
        L.append(u"   conserto: veja se a divisao esta certa (portao 1w) e "
                 u"regrave. Se a palavra for mesmo dificil para a voz, troque-a "
                 u"no caderno — entregar audio que ninguem conferiu e o que se "
                 u"quer acabar.")
    if faltam:
        ruim = 1
        L.append(u"   REPROVADO: o recibo esta VELHO — %d palavra(s) do "
                 u"`silabas.json` que ele nao menciona: %s"
                 % (len(faltam), u", ".join(w.upper() for w in faltam[:10])))
        L.append(u"   conserto: apague `audio/_silabas.json` e regrave.")
    if not ruim:
        L.append(u"   ✓ todas as %d palavras foram conferidas pela propria "
                 u"gravacao — ninguem precisou ouvir" % len(palavras))
    return ruim, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/silaba_conferida.py <pasta>")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, L = confere(pasta.rstrip(u"/"))
        print(u"%s -> voz conferida sozinha: %s"
              % (pasta.rstrip(u"/"),
                 {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
