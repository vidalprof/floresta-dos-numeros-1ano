#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA PERGUNTA AMBÍGUA — "tem mais de um na figura?"

Cobrança do Marcos (ago/2026): *"a mesma coisa a ponte, fica confuso porque tem
DUAS pontes"* — e antes: *"quando pede o quarteirão de casas tem muitas casas,
fica confuso; o morro tem vários com árvores"*. E o recado que fecha:
**"esses erros não podem passar"**.

Ele tem razão, e o defeito tem uma marca MEDÍVEL. Numa fase de "ache na cena",
o código declara quantos lugares valem como resposta. Se eu escrevo **"a
ponte"** — artigo definido, singular, ou seja *aquela, a única* — e declaro
DUAS zonas, a própria tela está confessando que há duas pontes na figura. A
criança lê "a ponte", vê duas, e não sabe qual. Não é questão de gosto: é
contradição entre o que a voz promete e o que a figura mostra.

REGRA QUE ESTE PORTÃO APLICA
  • pergunta no DEFINIDO SINGULAR ("a ponte", "o morro", "o mercado")
    -> só pode ter UMA zona. Duas ou mais = REPROVA.
  • pergunta no INDEFINIDO ou coletivo ("uma ponte", "alguma rua", "a mata em
    volta", "as casas") -> pode ter várias. É assim que se pede uma coisa
    repetida sem confundir.
  • zona única com pergunta indefinida passa (pedir "uma ponte" havendo uma só
    não confunde ninguém).
  • ⚠️ COISA COMPRIDA ≠ COISA REPETIDA. O rio é UM só — as oito zonas dele são
    pedaços do MESMO rio, e pedir "o rio" está certíssimo. Já a ponte são duas
    pontes de verdade. Quem sabe a diferença é quem escreve a fase, então ela
    se declara: `unico:1` no item diz "as zonas são partes de uma coisa só".
    Sem esse campo, o portão entende que são ocorrências diferentes — o padrão
    seguro, porque errar para o lado de perguntar demais não machuca ninguém.

O conserto de verdade, quando a figura tem várias, é DUPLO e está registrado no
MEMORIA-DO-PROJETO: ou a pergunta muda de artigo e a fase aceita todas as
ocorrências, ou — melhor — se gera uma figura em que a coisa apareça **uma vez
só**. Uma boa figura de ensino não repete o que ela quer ensinar a achar.

Uso:  python3 _qa/ambiguo.py _mapa/index.html
Sai com 1 se achar pergunta ambígua.
"""
import io
import re
import sys

# artigo definido singular = "aquela, a única"
DEF = re.compile(r"\b(?:o|a)\s+<b>", re.I)
# indefinido / coletivo / plural = pode haver várias
IND = re.compile(r"\b(?:um|uma|algum|alguma|uns|umas|os|as)\s+<b>|"
                 r"<b>[^<]*</b>\s*(?:em volta|do bairro|da cidade)", re.I)


def blocos(js):
    u"""acha as tabelas de 'ache na cena': listas com q: e z: [{x,y}...]."""
    achados = []
    for m in re.finditer(r"\{\s*q:\s*\"((?:[^\"\\]|\\.)*)\"(.*?)\}\s*(?=,\s*\{\s*q:|\]\s*;)",
                         js, re.S):
        pergunta = m.group(1)
        corpo = m.group(2)
        zonas = len(re.findall(r"\{\s*x:\s*-?\d+", corpo))
        if zonas == 0 and re.search(r"\bx:\s*-?\d+", corpo):
            zonas = 1          # alvo de ponto único (x/y direto no item)
        unico = re.search(r"\bunico\s*:\s*(?:1|true)", corpo) is not None
        achados.append((pergunta, zonas, unico))
    return achados


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    h = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", h, re.S))

    itens = blocos(js)
    problemas = []
    for pergunta, zonas, unico in itens:
        if zonas <= 1 or unico:
            continue
        # ⚠️ o indefinido manda: "uma ponte" com 2 zonas esta CERTO, e e
        #    justamente o conserto. So reprova quem pede no definido singular.
        if IND.search(pergunta):
            continue
        if DEF.search(pergunta):
            limpo = re.sub(r"</?b>", "", pergunta)
            problemas.append(u'pede "%s" (o/a = a UNICA) mas a fase aceita %d '
                             u'lugares — entao ha %d na figura e a crianca nao '
                             u'sabe qual' % (limpo, zonas, zonas))

    print(u"%s -> %d alvo(s) de 'ache na cena' conferido(s)" % (alvo, len(itens)))
    for p in problemas:
        print(u"  !! " + p)
    if not problemas:
        print(u"   pergunta ok: nada pedido no singular tendo varios na figura")
    else:
        print(u"   conserto: ou a pergunta vira INDEFINIDA (\"uma ponte\", \"alguma "
              u"rua\", \"a mata em volta\") ou se gera uma figura com UM so.")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
