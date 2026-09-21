# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — DIGITAR NÃO PODE DEPENDER DO ENTER  (1r)

 ⭐ ORDEM DO MARCOS (21/set/2026), sobre o caderno dos sistemas do 5º ano:
    ***"tem uma atividade onde o estudante digita e tem que clicar enter para
    confirmar, melhor não precisar do enter"*** — e, logo depois:
    ***"corrija isso em qualquer atividade que tenha isso"***.

 ⚠️ O QUE ERA. A grade de tamanho FIXO já fechava sozinha ao encher a última
    casa. A grade LIVRE — a das folhas de produção (*"escreva a SUA palavra"*,
    *"a sua manchete"*, *"o seu título"*) — não tem como saber quando a criança
    terminou, e o **único** jeito de confirmar era o ENTER. No celular essa
    tecla tem nome diferente em cada aparelho; no PC, a criança de dez anos não
    adivinha que precisa dela. Ela escrevia a resposta certa e a folha ficava
    parada, como se ela não tivesse feito nada.

 ⚠️ E ERA CÓDIGO GÊMEO: a mesma peça estava em OITO cadernos no ar
    (`_aumdim2`, `_corpo5`, `_narra2`, `_not2`, `_rima2`, `_seg2`, `_sinon2`,
    `_verbo4`). É a terceira vez nesta casa que um defeito mora em código
    clonado; por isso este portão olha TODOS, não o que ele reclamou.

 O QUE ELE MEDE, para o caderno que tem grade de escrever:
   1. existe a função `fechaSozinho()` — a que decide fechar sem tecla nenhuma;
   2. ela é quem manda nos DOIS pontos de fechamento automático (o do campo do
      aparelho e o do teclado de verdade) — nenhum deles pode ter voltado a
      perguntar só pelo tamanho da palavra;
   3. toda grade LIVRE (a que recebe a lista de respostas aceitas) desenha o
      botão **PRONTO**, para quem escreveu uma palavra que não está na lista.

 ⚠️ O QUE ELE NÃO MEDE: se o botão está VISÍVEL e alcançável na tela — isso é
    do `_qa/leiaute_mao.js`, que abre o navegador e mede os 40 px. Aqui é o
    pré-voo: pega o erro barato antes de gastar os dez minutos da banca.

 ⚠️ O Enter continua valendo, e isso é de propósito: a regra das DUAS PORTAS
    manda aceitar o teclado de verdade. O que se proíbe é ele ser o ÚNICO.

 Uso:  python3 _qa/sem_enter.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/sem_enter.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva." % pasta)
        return 2
    js = io.open(cam, encoding=u"utf-8").read()
    if u"function abreCruz" not in js:
        print(u"%s -> NAO SE APLICA: este caderno nao tem grade de escrever."
              % pasta)
        return 2

    faltas = []

    # ⚠️ A GRADE LIVRE É QUEM TEM O PROBLEMA, e isto foi conserto do próprio
    #    portão: na primeira versão eu cobrava a `fechaSozinho()` de TODO
    #    caderno e ele reprovou DEZENOVE que não têm grade livre nenhuma — nos
    #    quais a grade de tamanho fixo já fecha sozinha ao encher a última casa
    #    e o Enter nunca foi a única saída. Portão que manda consertar o que não
    #    está quebrado gasta o dia e ensina a ignorar a saída.
    livres = re.findall(r"gradeEscrever\([^)]*,\s*[A-Za-z_$][\w.$\[\]]*\.(?:ok|ac|aceita)\s*\)", js)
    autos_novo = len(re.findall(r"fechaSozinho\((?:CRUZ\.)?E,\s*CRUZ\.val\)", js))
    autos_velho = len(re.findall(r"CRUZ\.val\.length\s*>=\s*(?:CRUZ\.)?E\.w\.length", js))

    print(u"%s -> digitar nao depende do Enter: %d grade(s) livre(s)"
          % (pasta, len(livres)))

    # ⚠️ E O FECHAMENTO AUTOMÁTICO TEM MAIS DE UMA FORMA ESCRITA nesta casa —
    #    segunda correção do próprio portão. Os cadernos de alfabetização fecham
    #    com `ATIVA.val.length >= ATIVA.certa.length`, não com `CRUZ`/`E.w`, e
    #    procurar só uma das formas reprovava catorze cadernos que fecham
    #    sozinhos há meses. O que importa é a PERGUNTA — "alguma coisa fecha a
    #    palavra sem tecla?" — e ela se responde procurando a CHAMADA, não a
    #    condição: `setTimeout(confere…)`.
    fecha_qualquer = len(re.findall(r"setTimeout\(\s*confere\w*\s*,", js))
    if fecha_qualquer < 1:
        faltas.append(u"nada fecha a palavra sozinho: nao achei nenhum "
                      u"`setTimeout(confere…)`, entao a crianca so sai dali "
                      u"pelo Enter")

    if livres:
        if u"function fechaSozinho" not in js:
            faltas.append(u"ha grade LIVRE e nao existe a `fechaSozinho()`: numa "
                          u"grade livre o tamanho da palavra nunca fecha nada, "
                          u"entao so o Enter confirma")
        elif autos_novo < 2:
            faltas.append(u"a `fechaSozinho()` existe mas so manda em %d dos DOIS "
                          u"caminhos de digitacao — o outro continua preso ao "
                          u"Enter" % autos_novo)
        if not (u'"prontobt"' in js or u"'prontobt'" in js):
            faltas.append(u"%d folha(s) chamam a grade LIVRE e o construtor nao "
                          u"desenha o botao PRONTO: quem escrever uma palavra "
                          u"fora da lista nao tem como confirmar sem o Enter"
                          % len(livres))

    if not faltas:
        if livres:
            print(u"   ok: fecha sozinho quando a palavra bate, tem o botao "
                  u"PRONTO para a palavra de fora da lista, e o Enter e so a "
                  u"terceira porta.")
        else:
            print(u"   ok: so ha grade de tamanho fixo, e ela fecha sozinha ao "
                  u"encher a ultima casa — o Enter nunca foi a unica saida aqui.")
        return 0
    print(u"   REPROVADO:")
    for f in faltas:
        print(u"   - %s" % f)
    print(u"   Conserto: copiar a `fechaSozinho()` e o bloco do botao PRONTO do "
          u"`_corpo5/folhas.js` (funcao `gradeEscrever`), e o `.prontobt` do "
          u"`_corpo5/index.html`.")
    return 1


if __name__ == u"__main__":
    sys.exit(main())
