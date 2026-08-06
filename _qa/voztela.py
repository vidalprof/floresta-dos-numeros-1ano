#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA VOZ DA TELA — "o botão repete a PERGUNTA ou a última coisa falada?"

Defeito que o Marcos pegou (ago/2026): *"na fase da maquete ao mapa, se clica no
botão ao lado do enunciado ele não fala isso: fala da curiosidade lá embaixo.
Aliás isso está acontecendo nas fases da atividade do terceiro ano"*.

A causa é uma armadilha de nome. O motor guardava `falaAtual` = **o último áudio
tocado** — e quem toca áudio numa fase não é só a tela: é o **elogio**, o
**consolo**, a **dica** e o **post-it de curiosidade**. Bastava a criança abrir o
"Você sabia?" para o botão do enunciado passar a repetir a curiosidade. O botão
"Ouvir de novo" já tinha esse defeito havia tempo; o alto-falante no enunciado só
o tornou impossível de ignorar.

O conserto é uma variável separada — `falaTela` — que só recebe narração **da
tela**; as secundárias não a alteram. Este portão garante três coisas:

  1. existe `falaTela` (a voz da tela) e ela é declarada;
  2. `falar()` NÃO grava em `falaTela` quando a narração é secundária
     (tem que haver um guarda, tipo `if(!ehSecundaria(id))`);
  3. nenhum botão de repetir lê `falaAtual` sozinho — ou lê `falaTela`, ou lê
     `falaTela||falaAtual` (o fallback é aceitável: ele só vale quando a tela
     ainda não narrou nada).

Uso:  python3 _qa/voztela.py _mapa/index.html
Sai com 1 se achar problema.
"""
import io
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    h = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", h, re.S))

    # só vale para atividade que TEM botão de repetir a narração
    repete = re.findall(r"falar\(\s*(falaTela|falaAtual|v)\s*[,\)]", js)
    if not repete and "falaAtual" not in js:
        print(u"%s -> sem bot&#227;o de repetir narra&#231;&#227;o. Nada a conferir." % alvo)
        return 0

    problemas = []
    if "falaTela" not in js:
        problemas.append(u"nao existe `falaTela`: o botao repete a ULTIMA coisa "
                         u"falada, e o elogio/dica/curiosidade sujam isso")
    else:
        m = re.search(r"function falar\(([^)]*)\)\s*\{(.{0,400})", js, re.S)
        corpo = m.group(2) if m else ""
        if "falaTela=" in corpo and not re.search(r"if\s*\(\s*!\w+\(", corpo):
            problemas.append(u"`falar()` grava em `falaTela` SEM guarda: qualquer "
                             u"audio (elogio, dica, curiosidade) vira a voz da tela")

    # ⚠️ o que interessa e o HANDLER do botao, nao o resto do arquivo
    for m in re.finditer(r"onclick\s*=\s*function\([^)]*\)\s*\{([^}]{0,200})", js):
        c = m.group(1)
        if "falar(" not in c:
            continue
        if "falaAtual" in c and "falaTela" not in c:
            problemas.append(u"um botao repete `falaAtual` (a ultima coisa falada) "
                             u"em vez de `falaTela` (a voz desta tela)")
            break

    print(u"%s -> voz da tela conferida" % alvo)
    for p in problemas:
        print(u"  !! " + p)
    if not problemas:
        print(u"   voz ok: o botao repete a narracao DA TELA, nao a ultima tocada")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
