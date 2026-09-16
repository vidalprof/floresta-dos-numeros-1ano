# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1v — GLOBAL ATROPELADO (folha viva)

 Ele pega DUAS armadilhas da mesma familia, e as duas aconteceram no mesmo dia
 (16/set/2026, caderno "A Casinha dos Tres Pontos"). Nenhuma das duas da erro
 de sintaxe, nenhuma aparece no `node --check`, e as duas derrubam o caderno
 INTEIRO na primeira folha — com um `TypeError` so, num console que ninguem
 abre.

 1) NOME REPETIDO. O bloco DADOS do `index.html` declarou `var RESP` para as
    perguntas com figura. So que o motor JA TEM um `var RESP` (id -> resposta
    certa) e o `monta()` o ZERA a cada montagem:

        livro.innerHTML = ""; PAGEL = []; RESP = {}; TIRAS = [];

    Resultado: os dados somem na primeira folha montada. O `node --check`
    passa, o app abre, e a folha 18 estoura.

 2) DECLARADO DEPOIS DO `boot()`. O `folhas.js` termina com um
    `(function boot(){ ... monta(); ... })()` que roda na hora em que o
    navegador acaba de ler o arquivo. Tudo o que for declarado DEPOIS dessa
    linha ainda vale `undefined` nesse instante — o `var` sobe por icamento,
    o VALOR nao sobe. Foi assim que `var SINAL`, escrito junto das pecas no
    fim do arquivo, chegou vazio na folha 2.

 ⚠️ ISTO NAO E TEORIA: a banca ja pegava o estrago (o `conta_folha.js` diz
    "houve erro de JS"), mas so depois de ligar o navegador — e "NAO MEDI" nao
    e "reprovou". Este portao e de TEXTO e roda no pre-voo, em milissegundos.

 Uso:  python3 _qa/global_atropelado.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# `var X = ` no comeco da linha (coluna zero) = global de verdade. Dentro de
# funcao o `var` vem indentado, e ali a repeticao nao atropela ninguem.
_VAR = re.compile(r"^var\s+([A-Za-z_$][\w$]*)\s*=", re.M)
_BOOT = re.compile(r"^\(function\s+boot\s*\(", re.M)


def _globais(texto):
    u"""nome -> [posicoes], so os declarados na coluna zero"""
    achados = {}
    for m in _VAR.finditer(texto):
        achados.setdefault(m.group(1), []).append(m.start())
    return achados


def _scripts(html):
    u"""o JS que mora dentro do proprio index.html"""
    return u"\n".join(re.findall(r"<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>",
                                 html, re.S))


def confere(pasta):
    ih = os.path.join(pasta, u"index.html")
    fj = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(ih) or not os.path.exists(fj):
        return 2, [u"   nao e um caderno de folha viva (sem index.html + folhas.js): NAO MEDI"]

    html = io.open(ih, encoding=u"utf-8").read()
    js = io.open(fj, encoding=u"utf-8").read()
    dentro = _scripts(html)
    gh, gj = _globais(dentro), _globais(js)
    L, ruim = [], 0

    # ---- 1. o mesmo nome declarado duas vezes -------------------------------
    repetidos = []
    for nome in sorted(set(gh) | set(gj)):
        quantas = len(gh.get(nome, [])) + len(gj.get(nome, []))
        if quantas > 1:
            onde = []
            if gh.get(nome):
                onde.append(u"index.html x%d" % len(gh[nome]))
            if gj.get(nome):
                onde.append(u"folhas.js x%d" % len(gj[nome]))
            repetidos.append((nome, u" + ".join(onde)))
    if repetidos:
        ruim = 1
        L.append(u"   REPROVADO 1: o mesmo nome global declarado duas vezes — a "
                 u"segunda declaracao apaga a primeira, e quem escreve o valor "
                 u"por ultimo ganha:")
        for nome, onde in repetidos:
            L.append(u"      • var %s  (%s)" % (nome, onde))
        L.append(u"   conserto: renomeie o bloco de DADOS (o motor veio antes). "
                 u"Foi assim que `RESP` dos dados morreu no `RESP = {}` do monta().")
    else:
        L.append(u"   ✓ nenhum nome global declarado duas vezes (%d no index.html, "
                 u"%d no folhas.js)" % (len(gh), len(gj)))

    # ---- 2. declarado DEPOIS do boot() e usado durante ele ------------------
    mb = _BOOT.search(js)
    if not mb:
        L.append(u"   ⚠️ nao achei o `(function boot(` no folhas.js: NAO MEDI a "
                 u"ordem das declaracoes")
        ruim = max(ruim, 2)
    else:
        corte = mb.start()
        antes = js[:corte]
        tarde, slots = [], []
        for nome, poss in gj.items():
            if min(poss) < corte:
                continue                       # ja nasce antes do boot
            if re.search(r"\b%s\b" % re.escape(nome), antes):
                tarde.append((nome, u"lido por codigo que roda no proprio boot"))
                continue
            # ⭐ A LINHA QUE SEPARA O ERRO DA GAVETA VAZIA: o que esta declaracao
            #   CARREGA. `var ATIVO_LETRAS = null` e uma gaveta — quem escreve
            #   nela so roda quando a crianca toca em alguma coisa, muito depois
            #   do boot. `var SINAL = {inter: {...}}` e DADO, e dado tem de estar
            #   pronto antes, porque o `monta()` do boot desenha as 35 folhas de
            #   uma vez e todas elas leem daqui.
            m2 = re.compile(r"^var\s+%s\s*=\s*(.{0,40})" % re.escape(nome),
                            re.M | re.S).search(js[min(poss):])
            valor = (m2.group(1).strip() if m2 else u"")
            if re.match(r"^(null|false|true|0|\"\"|''|\{\s*\}|\[\s*\])\s*;", valor):
                slots.append(nome)
            else:
                tarde.append((nome, u"carrega DADO: " + valor.split(u"\n")[0][:34]))
        if tarde:
            ruim = 1
            L.append(u"   REPROVADO 2: global declarado DEPOIS do `boot()`. O boot "
                     u"roda na hora em que o navegador acaba de ler o arquivo e o "
                     u"`monta()` dele desenha as 35 folhas de uma vez — o `var` sobe "
                     u"por icamento, mas o VALOR nao sobe, e ali ele ainda e "
                     u"`undefined`:")
            for nome, por in sorted(tarde):
                L.append(u"      • var %s  (%s)" % (nome, por))
            L.append(u"   conserto: leve a declaracao para o bloco DADOS do "
                     u"index.html, que o navegador le antes do folhas.js.")
        else:
            if slots:
                L.append(u"   ✓ %d gaveta(s) vazia(s) depois do boot (%s): quem "
                         u"escreve nelas so roda no toque da crianca"
                         % (len(slots), u", ".join(sorted(slots))))
            L.append(u"   ✓ nada de valor e lido antes de existir")

    return ruim, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/global_atropelado.py <pasta>")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, L = confere(pasta.rstrip(u"/"))
        cabec = {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]
        print(u"%s -> global atropelado: %s" % (pasta.rstrip(u"/"), cabec))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
