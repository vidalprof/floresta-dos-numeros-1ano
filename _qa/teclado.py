# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — O TECLADO TEM TODAS AS LETRAS?  (1t)

 ⭐ O DEFEITO QUE ELE PAGA (15/set/2026, caderno de ortografia do 5º ano).
    O teclado da folha viva vinha com o alfabeto escrito à mão numa string:
        "ABCDEFGHIJLMNOPQRSTUVXZÇÁÉÍÓÚ"
    Falta K, falta W, falta Y — e faltam Ê, Â, Ã, Ô, Õ, À e Ü.

    O que isso faz com a criança: ela abre a folha "escreva a palavra certa",
    ouve PÊSSEGO, digita P... e o Ê não entra. Nem no teclado da tela (a tecla
    não existe) nem no teclado de verdade (o filtro do `keydown` recusa a letra).
    Ela fica com "PSSEGO", a folha não fecha, e NÃO HÁ ERRO NENHUM no console:
    o app está funcionando exatamente como foi escrito. A criança tenta de novo
    até desistir, e o professor vê uma folha "que travou".

    ⚠️ E NENHUM PORTÃO VIA. O `node --check` passa, o leiaute passa, o revisor
       de texto passa, o andarilho passa (ele ABRE a folha, não a resolve). Quem
       pegou foi o jogador da banca, e só porque a palavra sorteada naquele dia
       tinha acento — com outra semente, passava batido.

 O QUE ELE MEDE, e as duas coisas são diferentes:

 1. **O alfabeto está completo.** As 26 letras do alfabeto mais os treze sinais
    do português: Á À Â Ã É Ê Í Ó Ô Õ Ú Ü Ç. Não é gosto meu — é a lista do que
    uma criança de 5º ano precisa para escrever qualquer palavra da aula.

 2. **O teclado da TELA e o filtro do teclado DE VERDADE usam o MESMO alfabeto.**
    São dois lugares no código, e é a regra das duas portas do Marcos: *"seria
    interessante se o aluno além de teclar no teclado virtual funcionasse se ele
    tocasse no teclado de verdade, as duas opções"*. Dois alfabetos diferentes é
    o mesmo defeito com uma porta só — e essa é a porta que o PC da escola usa.

 ⚠️ O QUE ELE NÃO MEDE: se a tecla, existindo, CABE na tela. Isso é o
    `_qa/leiaute_mao.js`, que mede alvo menor que 40 px.

 Uso:  python3 _qa/teclado.py <pasta-ou-arquivo.js>
 Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# as 26 do alfabeto + os treze sinais do português
PRECISA = (u"ABCDEFGHIJKLMNOPQRSTUVWXYZ" u"ÁÀÂÃÉÊÍÓÔÕÚÜÇ")


def alfabetos(js):
    u"""Devolve [(onde, letras)] de cada alfabeto de teclado achado no arquivo.

    São dois desenhos diferentes no código, e por isso duas buscas:
      · o teclado da TELA monta os botões de uma string (`var letras = "..."`);
      · o teclado DE VERDADE filtra a tecla com `"...".indexOf(k) > -1`.
    ⚠️ A string de ENCHER o caça-palavras também é um alfabeto e NÃO é teclado:
       ela é lida de `var enche`, e fica de fora de propósito — reprovar por ela
       seria o portão acusando o que não é a peça dele.
    """
    fora = []
    for m in re.finditer(r"var\s+letras\s*=\s*\"([^\"]+)\"", js):
        fora.append((u"teclado da tela", m.group(1)))
    for m in re.finditer(r"\"([A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ]{10,})\"\s*\.indexOf\(", js):
        fora.append((u"filtro do teclado de verdade", m.group(1)))
    return fora


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/teclado.py <pasta-ou-arquivo.js>")
        return 2
    alvo = sys.argv[1].rstrip(u"/")
    cam = alvo if alvo.endswith(u".js") else os.path.join(alvo, u"folhas.js")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: nao achei %s (nao e caderno de folha viva)."
              % (alvo, cam))
        return 2
    js = io.open(cam, encoding=u"utf-8").read()
    achados = alfabetos(js)
    if not achados:
        print(u"%s -> NAO SE APLICA: este caderno nao tem teclado de letras." % alvo)
        return 2

    print(u"%s -> teclado: %d alfabeto(s) conferido(s)" % (alvo, len(achados)))
    erros = []
    for onde, letras in achados:
        falta = [c for c in PRECISA if c not in letras]
        if falta:
            erros.append(u"o %s nao tem: %s" % (onde, u" ".join(falta)))
    # os alfabetos têm de ser o MESMO conjunto
    conj = set(frozenset(l) for _, l in achados)
    if len(conj) > 1:
        erros.append(u"o teclado da tela e o filtro do teclado de verdade usam "
                     u"alfabetos DIFERENTES — a criança consegue por uma porta e "
                     u"nao pela outra")
    if erros:
        print(u"   REPROVADO — ha letra que a crianca NAO CONSEGUE escrever:")
        for e in erros:
            print(u"    x %s" % e)
        print(u"   conserto: usar o alfabeto completo nos DOIS lugares —")
        print(u"   \"%s\"" % PRECISA)
        print(u"   (sem isso a folha de escrever nao fecha, e sem erro nenhum na tela)")
        return 1
    print(u"   ok: as 26 letras e os 13 sinais do portugues, nas duas portas.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
