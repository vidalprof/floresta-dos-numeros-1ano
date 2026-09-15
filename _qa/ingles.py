# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — CADERNO DE LÍNGUA ESTRANGEIRA  (1n)

 ⭐ POR QUE ELE EXISTE. Ordem do Marcos, 15/set/2026, depois de uma rodada em
    que ele mesmo achou três coisas que nenhum portão media:
    ***"todo erro corrigido ou melhorado não pode voltar mais"***.

    As três coisas foram:
      1. a voz dizia **"blank"** no lugar da lacuna — *"o blank de vazio não
         precisa ser narrado"*;
      2. a **frase completa em inglês** só existia na tela, nunca no ouvido —
         *"depois de acertar ele fala a frase toda"*;
      3. o caderno misturava **neighbor** e **neighbour** na mesma atividade.

    Nenhuma delas dá erro de JS, nenhuma aparece num print, e as três chegariam
    à criança. Este portão é a segunda metade do conserto — sem ela, o trabalho
    não está feito (regra do CONSERTO DUPLO, `SEQUENCIAS-DIDATICAS.md §2`).

 ⚠️ O QUE ELE NÃO MEDE: se o inglês está CERTO. Concordância, tempo verbal e
    naturalidade continuam com o especialista da disciplina e com o professor.
    Ele mede o que é mecânico e regride sozinho.

 Uso:  python3 _qa/ingles.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica (caderno sem fala inglesa)
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

# ⚠️ AS PALAVRAS QUE NÃO PODEM SER NARRADAS NO LUGAR DA LACUNA. `blank` foi a
#    que o Marcos ouviu; as outras são as que eu tentei antes dela, e que
#    voltariam pelo mesmo caminho se alguém "consertasse" a lacuna de novo.
LACUNA_FALADA = (u"blank", u"mmm", u"hmm", u"underscore", u"underline",
                 u"lacuna", u"espaço em branco", u"espaco em branco")

# ⚠️ GRAFIA BRITÂNICA × AMERICANA. Não existe uma "certa" — existe a MESMA em
#    todo o caderno. Duas grafias da mesma palavra, sem explicação, é erro para
#    quem está aprendendo. (Achado real: `neighbor` na folha 19 e `neighbour`
#    nas folhas 25 e 28, na MESMA frase.)
PARES_GRAFIA = [
    (u"neighbour", u"neighbor"), (u"colour", u"color"),
    (u"favourite", u"favorite"), (u"behaviour", u"behavior"),
    (u"flavour", u"flavor"), (u"labour", u"labor"),
    (u"centre", u"center"), (u"theatre", u"theater"),
    (u"metre", u"meter"), (u"litre", u"liter"),
    (u"realise", u"realize"), (u"organise", u"organize"),
    (u"apologise", u"apologize"), (u"practise", u"practice"),
    (u"travelling", u"traveling"), (u"cancelled", u"canceled"),
    (u"grey", u"gray"), (u"jewellery", u"jewelry"),
]


def palavras(t):
    return re.findall(r"[a-z']+", (t or u"").lower())


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/ingles.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"falas.json")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: nao ha falas.json." % pasta)
        return 2
    falas = json.load(io.open(cam, encoding=u"utf-8"))
    en = [f for f in falas if f.get(u"lang") == u"en"]
    if not en:
        print(u"%s -> NAO SE APLICA: nenhuma fala em ingles." % pasta)
        return 2

    erros, avisos = [], []

    # ---- regra 1: a lacuna não se narra ------------------------------------
    for f in en:
        for m in LACUNA_FALADA:
            if re.search(r"\b" + re.escape(m) + r"\b", f.get(u"texto", u""), re.I):
                erros.append((
                    u"1 · LACUNA NARRADA",
                    f.get(u"id", u"?"),
                    f.get(u"texto", u"")[:80],
                    u'a voz diz "%s" no lugar do buraco. O Marcos pediu o '
                    u'contrario: "so nao falar nada, falar a frase com o que '
                    u'tem" — a lacuna esta DESENHADA na tela, o audio nao '
                    u'precisa anuncia-la.' % m))
                break

    # ---- regra 2: pontuação dobrada ou solta --------------------------------
    for f in falas:
        t = f.get(u"texto", u"")
        if u",," in t or re.search(r"\s+[,.;:!?]", t):
            erros.append((
                u"2 · PONTUACAO SOLTA",
                f.get(u"id", u"?"), t[:80],
                u"virgula dobrada ou espaco antes da pontuacao. A voz faz a "
                u"pausa no lugar errado — nasceu de montar a frase juntando "
                u"pedacos a mao, e o `lp()` do gerar_falas ja limpa isso."))

    # ---- regra 3: uma grafia só por caderno ---------------------------------
    todo = u" ".join(f.get(u"texto", u"") for f in en).lower()
    for br, us in PARES_GRAFIA:
        tem_br = re.search(r"\b" + br + r"\b", todo)
        tem_us = re.search(r"\b" + us + r"\b", todo)
        if tem_br and tem_us:
            erros.append((
                u"3 · DUAS GRAFIAS",
                u"(o caderno todo)", u"%s / %s" % (br, us),
                u"as duas grafias da MESMA palavra convivem neste caderno. Nao "
                u"ha uma certa — ha a mesma em todo lugar. Escolher UMA (a do "
                u"resto do caderno) e trocar a outra."))

    # ---- regra 4: o par que ensina -----------------------------------------
    # ⚠️ ESTA É A REGRA QUE GUARDA A MELHORIA DO MARCOS, e o alcance dela está
    #    declarado: ela mede que o PADRÃO existe no caderno, não que cada folha
    #    o tenha. O par é uma fala inglesa A (a frase com o buraco) e outra B
    #    que é A com uma palavra a mais no meio (a frase inteira, do acerto).
    #    Se o padrão sumir por inteiro — alguém trocou o acerto de volta por um
    #    "Isso mesmo!" —, o número cai a zero e ele reprova.
    textos = [(f.get(u"id", u""), palavras(f.get(u"texto", u""))) for f in en]
    pares = 0
    for _ida, a in textos:
        if len(a) < 3:
            continue
        for _idb, b in textos:
            if len(b) - len(a) not in (1, 2) or b == a:
                continue
            # b contém a, na ordem, com 1 ou 2 palavras a mais?
            i = 0
            for w in b:
                if i < len(a) and w == a[i]:
                    i += 1
            if i == len(a):
                pares += 1
                break
    genericas = [f for f in falas
                 if re.match(r"^certo\d+", f.get(u"id", u"") or u"")
                 and f.get(u"lang") != u"en"]

    print(u"%s -> caderno de lingua estrangeira: %d fala(s) inglesa(s) de %d"
          % (pasta, len(en), len(falas)))
    print(u"   pares 'frase com o buraco' -> 'frase inteira no acerto': %d" % pares)
    if not pares:
        erros.append((
            u"4 · O PAR QUE ENSINA SUMIU",
            u"(o caderno todo)", u"0 pares",
            u"nenhuma fala de acerto e a frase INTEIRA em ingles. Pedido do "
            u"Marcos, 15/set: \"depois de acertar ele fala a frase toda\" — e a "
            u"razao e que esse par (ouvir sem a palavra, depois com ela) e o "
            u"unico modelo de pronuncia completo que a crianca recebe."))
    if genericas:
        avisos.append(u"%d fala(s) de acerto NAO estao em ingles (pode ser folha "
                      u"sem frase inglesa, como o mural do fim): %s"
                      % (len(genericas),
                         u", ".join(g.get(u"id", u"?") for g in genericas[:4])))

    for a in avisos:
        print(u"   aviso: %s" % a)
    if not erros:
        print(u"   ok: a lacuna nao e narrada, a correcao diz a frase inteira e "
              u"a grafia e uma so.")
        print(u"   ⚠️ ele NAO mede se o ingles esta CERTO (concordancia, tempo "
              u"verbal, naturalidade) — isso e do especialista e do professor.")
        return 0

    print(u"   REPROVADO — %d achado(s):" % len(erros))
    for regra, ident, trecho, porque in erros:
        print(u"    x %s  [%s]" % (regra, ident))
        print(u"      em: %s" % trecho)
        print(u"      %s" % porque)
    return 1


if __name__ == u"__main__":
    sys.exit(main())
