# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — O ALTO-FALANTE DA RESPOSTA  (1o)

 ⭐ ORDEM DO MARCOS, ago/2026 e repetida em 15/set/2026:
    ***"o alto-falante nas respostas também, para ajudar os alunos que não
    sabem ler"*** · ***"precisamos pôr áudio nas opções de resposta para quem
    não sabe ler, principalmente para os menores"***.

 ⚠️ ERA REGRA DA CASA E NÃO ERA MEDIDA — que é a mesma coisa que não ser regra.
    Quando ele pediu de novo, em 15/set, eu fui contar: **9 opções mudas** em
    quatro cadernos, e três deles de alfabetização. A pior era o `_rima1`, do
    **1º ano**, onde os dois botões são `RIMA` e `NÃO RIMA` — uma criança de
    seis anos não lê isso, e sem voz ela escolhe pelo tamanho do botão. A
    atividade virava sorteio para justamente quem ela deveria ajudar.

 O QUE ELE MEDE: toda opção desenhada por `opcoes(...)` tem de carregar o campo
 `fala`. É esse campo que o motor toca quando a criança encosta no botão — sem
 ele, o botão é mudo, e nenhum outro portão vê, porque o app funciona
 perfeitamente.

 ⚠️ O QUE ELE NÃO MEDE: se a fala DIZ a coisa certa (isso é do `_qa/falas.py` e
    do ouvido) e se o mp3 existe (o `entregar.yml` grava). Ele mede o mudo.

 ⚠️ E HÁ UMA EXCEÇÃO LEGÍTIMA, escrita para ninguém "consertá-la" depois: numa
    folha de ORTOGRAFIA a voz **não distingue** as opções — *"abito"* e
    *"hábito"* soam igual, e é exatamente por isso que a folha existe. A voz
    continua obrigatória ali, mas para a criança **saber o que está escrito**,
    não para escolher por ela. Quem decide é a letra, que ela lê.

 Uso:  python3 _qa/voz_opcao.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# uma opção é um objeto `{v: …, rot: …}` passado a `opcoes(...)`
_OPCAO = re.compile(r"\{\s*v\s*:\s*[^{}]*\}")


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/voz_opcao.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: nao ha folhas.js (nao e folha viva)." % pasta)
        return 2
    js = io.open(cam, encoding=u"utf-8").read()
    if u"opcoes(" not in js:
        print(u"%s -> NAO SE APLICA: este caderno nao usa `opcoes()`." % pasta)
        return 2

    mudas, total = [], 0
    for m in _OPCAO.finditer(js):
        t = m.group(0)
        if u"rot" not in t:                 # não é uma opção da tela
            continue
        total += 1
        if u"fala" not in t:
            linha = js[:m.start()].count(u"\n") + 1
            mudas.append((linha, u" ".join(t.split())[:88]))

    print(u"%s -> alto-falante da resposta: %d opcao(oes) na tela" % (pasta, total))
    if not total:
        print(u"   NAO SE APLICA: nenhuma opcao desenhada.")
        return 2
    if not mudas:
        print(u"   ok: toda opcao carrega o campo `fala` — nenhuma e muda.")
        return 0

    print(u"   REPROVADO — %d opcao(oes) MUDAS:" % len(mudas))
    for linha, trecho in mudas:
        print(u"    x %s:%d" % (cam, linha))
        print(u"      %s" % trecho)
    print(u"   A crianca que ainda nao le escolhe pelo tamanho do botao, e a")
    print(u"   folha vira sorteio para justamente quem ela deveria ajudar.")
    print(u"   Conserto: `fala: \"<chave>\"` na opcao + a chave no gerar_falas.py.")
    return 1


if __name__ == u"__main__":
    sys.exit(main())
