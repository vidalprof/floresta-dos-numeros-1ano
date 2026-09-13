# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — O LEQUE E A ESCADA DO CADERNO DE FOLHA VIVA  (0b7)

 ⭐ A DÍVIDA QUE ESTE ARQUIVO PAGA (tarefa #104). Até 13/set/2026, **nenhum
    portão media** se as folhas de um caderno de folha viva sobem de verdade,
    nem se um gesto toma conta do caderno. Quem respondia por isso era o crivo
    escrito do `_sequencias/POTE-*.md` — que é do Claude, e crivo não é medida.
    A banca chegava a imprimir isso toda vez, em letras grandes, e imprimir uma
    dívida não é pagá-la.

 ⚠️ POR QUE O PORTÃO DO MOTOR (`_qa/padrao.py`, 0b) NÃO SERVIA: ele conta FASES
    e lê o `conteudo.json`. Folha viva não tem nem uma coisa nem outra — tem
    folhas, e o gesto de cada uma está escrito no corpo da função `fN`.

 O QUE ELE MEDE — e as duas coisas são diferentes:

 1. **O LEQUE** (a regra da casa, do Marcos): *"variedade de dinâmicas para o
    estudante não se cansar"*. Nenhum gesto acima de **40%** das folhas, e no
    mínimo **4 gestos** diferentes. Conta GESTO, não conteúdo: duas folhas podem
    ensinar coisas diferentes e ainda ser, para a criança, *a mesma tela pela
    terceira vez*.

 2. **A ESCADA**: a criança faz coisas **mais difíceis no fim** do que no começo.
    Medida como o peso do gesto (os segundos por item) do **terço final** contra
    o do **terço inicial**. Reprova só a DESCIDA clara — o caderno que começa
    pedindo para escrever e termina pedindo para tocar.

 ⚠️ O QUE ELE NÃO MEDE, E EU NÃO VOU FINGIR QUE MEDE: se o CONTEÚDO sobe. Sílaba
    simples antes de sílaba complexa, palavra curta antes de comprida, o degrau
    do currículo — nada disso está no código de forma que dê para ler. O peso do
    gesto é um PROXY honesto (mais difícil de fazer ≈ degrau mais alto) e está
    dito assim na tela. Quem responde pelo resto continua sendo o crivo e o
    professor. Portão que promete o que não mede é pior que portão nenhum.

 ⚠️⚠️ O GESTO É **DECLARADO** PELO CADERNO, NÃO ADIVINHADO DO CÓDIGO — e esta
    é a lição mais cara deste arquivo, paga na primeira hora de vida dele.

    A primeira versão lia o gesto do corpo da `fN`, reusando o classificador do
    `_qa/duracao.py`. Parecia elegante (uma régua só) e o resultado era falso: na
    Roda das Sílabas, *"Ligue cada figura ao seu pedaço"* saía como **arrastar**
    e *"Pinte só os balões deste pedacinho"* saía como **ligar**. A causa é que
    aquele classificador procura pedaços de código (`puxavel(`, `coluna`,
    `.tec`) que aparecem numa folha por acessório, sem serem o gesto principal.
    Para o RELÓGIO isso não importa — erra 5 s numa folha e a soma continua na
    ordem certa. Para dizer QUAL é o gesto, importa tudo.

    E aí o portão reprovava três cadernos por conta do PRÓPRIO erro. O
    `CLAUDE.md` diz que portão que aprova por causa do próprio erro é pior que
    portão nenhum; reprovar por causa dele é a mesma coisa com outro sinal.

    Então o gesto agora vem escrito no `/*GESTOS-INI*/` do `index.html`, uma
    palavra por folha, pela mão de quem monta — como já são o `LIGAR` e o
    `curriculo.json`. O portão não adivinha: ele confere a conta e cobra a
    declaração. Sem declaração ele diz **NÃO MEDI**, que aparece na banca como
    dívida e não como aprovação.

 ⚠️ O PESO (os segundos) continua vindo do `_qa/duracao.py`, importado e não
    copiado — ali ele é confiável, e é PALPITE DECLARADO, nunca cronometrado.

 Uso:  python3 _qa/leque_folha.py <pasta>
 Código 0 = leque e escada ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import json
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from duracao import gesto_da_folha
except Exception as e:                                    # pragma: no cover
    print(u"NAO MEDI: nao consegui importar o classificador do duracao.py (%s)" % e)
    sys.exit(2)

TETO = 0.40      # nenhum gesto acima disto (regra da casa, medida em fases)
MIN_GESTOS = 4   # idem


def declarados(html):
    u"""O bloco `/*GESTOS-INI*/ var GESTOS = {...}` do index.html: folha -> gesto."""
    # ⚠️ entre a marca e o `var` mora um COMENTÁRIO (o que explica a declaração),
    #    e `\s*` não casa comentário — foi o que fez o portão dizer "não medi"
    #    nos doze cadernos que eu acabara de declarar.
    m = re.search(r"/\*GESTOS-INI\*/.*?var GESTOS = (\{.*?\})\s*;", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def folhas_do_js(js):
    u"""[(numero, corpo)] de cada `function fN(...)`, na ordem do caderno."""
    fora = []
    pedacos = re.split(r"\nfunction f(\d+)\s*\(", u"\n" + js)
    for i in range(1, len(pedacos) - 1, 2):
        n = int(pedacos[i])
        if n == 0:
            continue          # f0 é a CAPA: não é folha de trabalho
        fora.append((n, pedacos[i + 1]))
    return sorted(fora)


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/leque_folha.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam_js = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(cam_js):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva (sem folhas.js)." % pasta)
        return 2
    js = io.open(cam_js, encoding=u"utf-8").read()
    folhas = folhas_do_js(js)
    if len(folhas) < 4:
        print(u"%s -> NAO MEDI: achei %d folha(s) no folhas.js." % (pasta, len(folhas)))
        return 2

    cam_html = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam_html):
        print(u"%s -> NAO MEDI: sem index.html." % pasta)
        return 2
    html = io.open(cam_html, encoding=u"utf-8").read()
    nomes = []
    m = re.search(r"var NOMES = \[(.*?)\];", html, re.S)
    if m:
        nomes = re.findall(r'"([^"]*)"', m.group(1))

    GES = declarados(html)
    if GES is None:
        print(u"%s -> NAO MEDI: o caderno nao DECLARA o gesto de cada folha." % pasta)
        print(u"   (isto nao e 'passou'. Escrever no index.html, entre")
        print(u"    /*GESTOS-INI*/ e /*GESTOS-FIM*/, um `var GESTOS = {\"f1\":\"...\"}`")
        print(u"    com UMA palavra por folha — o gesto que a crianca FAZ ali.)")
        return 2

    linhas, semDeclarar = [], []
    for n, corpo in folhas:
        custo, _ = gesto_da_folha(corpo)          # o PESO vem do duracao.py
        gesto = GES.get(u"f%d" % n)               # o GESTO vem da declaração
        if not gesto:
            semDeclarar.append(n)
            continue
        nome = nomes[n - 1] if n - 1 < len(nomes) else u""
        linhas.append((n, gesto, custo, nome))
    if semDeclarar:
        print(u"%s -> NAO MEDI: %d folha(s) sem gesto declarado (%s)."
              % (pasta, len(semDeclarar),
                 u", ".join(u"f%d" % n for n in semDeclarar)))
        return 2

    total = len(linhas)
    conta = {}
    for _, g, _, _ in linhas:
        conta[g] = conta.get(g, 0) + 1

    print(u"%s -> leque e escada: %d folha(s) de trabalho" % (pasta, total))
    for g, q in sorted(conta.items(), key=lambda x: -x[1]):
        print(u"   %-14s %2d folha(s)  %3d%%" % (g, q, round(100.0 * q / total)))

    # ---- a ESCADA, em terços
    t = max(1, total // 3)
    inicio = sum(c for _, _, c, _ in linhas[:t]) / float(t)
    fim = sum(c for _, _, c, _ in linhas[-t:]) / float(t)
    print(u"   escada (peso do gesto, PALPITE DECLARADO — nunca cronometrado):")
    print(u"      primeiro terco: %.1f s/item   ultimo terco: %.1f s/item" % (inicio, fim))
    print(u"   a folha a folha:")
    for n, g, c, nome in linhas:
        print(u"      %2d. %-14s %4.0f s   %s" % (n, g, c, nome[:42]))

    erros = []
    for g, q in conta.items():
        if q > TETO * total:
            erros.append(u'o gesto "%s" toma %d de %d folhas (%d%%) — o teto e %d%%'
                         % (g, q, total, round(100.0 * q / total), round(TETO * 100)))
    if len(conta) < MIN_GESTOS:
        erros.append(u"so %d gesto(s) diferente(s) no caderno inteiro — o minimo e %d"
                     % (len(conta), MIN_GESTOS))
    # ⚠️ só a DESCIDA CLARA reprova. Caderno que termina no mesmo peso não é
    #    defeito: há assunto que não tem degrau de gesto para subir, e reprovar
    #    isso seria obrigar a enfiar uma folha de digitar no fim só para passar.
    if fim < inicio * 0.75:
        erros.append(u"a ESCADA DESCE: o ultimo terco (%.1f s/item) e bem mais leve "
                     u"que o primeiro (%.1f) — a crianca termina fazendo menos do "
                     u"que comecou fazendo" % (fim, inicio))

    if erros:
        print(u"   REPROVADO:")
        for e in erros:
            print(u"    - %s" % e)
        print(u"   conserto: o gesto de cada folha vem do COMANDO IMPRESSO na folha")
        print(u"   de papel (regra do Marcos, 13/set/2026) — reler o crivo em")
        print(u"   _sequencias/POTE-*.md e trazer os verbos que ficaram de fora.")
        return 1
    print(u"   ok: nenhum gesto passa de %d%%, sao %d gestos, e a escada nao desce"
          % (round(TETO * 100), len(conta)))
    print(u"   ⚠️ ele NAO mede se o CONTEUDO sobe (silaba simples antes da complexa,")
    print(u"      o degrau do curriculo). Isso continua com o crivo e o professor.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
