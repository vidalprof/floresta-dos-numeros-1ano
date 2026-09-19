# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 1i8 — "a mão de N dedos é mesmo a de N dedos?"

 Nasceu com a troca do desenho de código pela figura recortada da folha de
 papel, no `_dedos` (19/set/2026, ordem do Marcos: *"essas imagens das mãos,
 dos dedos na internet, pois na atividade está feio"*). Numa atividade de
 CONTAR, o número de dedos da figura não é arte: é o conteúdo. A figura de
 "três" com quatro dedos não fica feia — ela ENSINA ERRADO, e a criança que
 acerta a conta leva zero na cabeça. O `_dedos/PROMPTS-MAOS.md` já avisava
 disso em setembro; o aviso dependia de alguém lembrar de ler.

 ⛔ O QUE ESTE PORTÃO NÃO MEDE — e é importante dizer antes do que ele mede:
    ELE NÃO CONTA OS DEDOS. Eu tentei. A conta natural seria fatiar a figura
    acima dos nós e contar as corridas de tinta; medido nas seis mãos da d11,
    ela acerta 0, 1, 2 e 3 e ERRA 4 e 5, porque nesses dois desenhos os dedos
    se encostam e viram uma corrida só. Portão que erra um terço dos casos não
    é portão; chamar isso de "conferi a contagem" seria mentira medida.
    Quem confere a CONTAGEM é o olho, na folha de contato que o
    `recortar_das_folhas.py` imprime. Este portão cuida do resto.

 O QUE ELE MEDE, e por que isto vale a pena mesmo sem contar dedo: a falha de
 verdade neste tipo de trabalho não é a folha trazer um desenho errado — é a
 CAIXA sair trocada. Um copia-e-cola de coordenada e a mão de 4 vira a de 3;
 um erro de dígito e duas ficam iguais; um `tira_halo` mais faminto come um
 dedo inteiro. Todas essas aparecem numa grandeza simples e honesta:

   1. A TINTA TEM DE CRESCER. Mais dedos levantados = mais desenho. Medido nas
      seis da d11: 35.978 · 41.535 · 48.488 · 53.649 · 57.257 · 63.513 px.
      Sempre para cima, com folga confortável entre vizinhas (a menor
      diferença é 7%, entre a de 3 e a de 4). Se a ordem quebra, alguma caixa
      está no lugar errado.                                          REPROVA
   2. NENHUMA DUAS SÃO IGUAIS. Silhuetas iguais = a mesma caixa recortada
      duas vezes com nomes diferentes — foi assim que, noutro caderno, a letra
      I em pão acabou sendo o H (portão 1c2).                        REPROVA
   3. OS TONS SÃO A MESMA MÃO. A recoloração só troca a cor do preenchimento;
      se a silhueta de um tom difere da do tom base em mais de 1%, a máscara
      de pele comeu ou inventou desenho.                             REPROVA
   4. A SÉRIE ESTÁ COMPLETA e todas na MESMA TELA — sem isso os pulsos não se
      alinham e a tela pula debaixo do dedo da criança.              REPROVA

 Uso:  python3 _qa/dedos_contam.py _dedos
 Códigos: 0 passou · 1 REPROVOU · 2 NÃO DEU PARA MEDIR
============================================================
"""
from __future__ import print_function

import os
import re
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError as e:                                   # pragma: no cover
    print(u"NAO MEDI: preciso de Pillow e numpy (%s)" % e)
    sys.exit(2)

# folga mínima entre a tinta de uma mão e a da seguinte.
# ⚠️ PALPITE DECLARADO (nunca cronometrado, nunca medido com criança): o 3%
#    abaixo é escolha minha. A régua que existe é a medida real das seis mãos
#    da d11, onde a menor diferença entre vizinhas foi 7%. Pus o corte em 3%
#    — menos da metade do menor caso real — para não reprovar uma série futura
#    desenhada com dedos mais finos, e ainda assim pegar duas caixas iguais ou
#    quase iguais, que é o defeito que ele existe para achar.
FOLGA = 0.03
TOM_IGUAL = 0.01          # diferença de silhueta tolerada entre tons


def corpo(cam):
    im = Image.open(cam).convert(u"RGBA")
    a = np.array(im)
    return im.size, (a[..., 3] > 40)


def main(pasta):
    img = os.path.join(pasta, u"img")
    if not os.path.isdir(img):
        print(u"NAO MEDI: %s nao tem pasta img/" % pasta)
        return 2
    arqs = sorted(n for n in os.listdir(img)
                  if re.match(r"^dd_mao\d[a-z]?\.png$", n))
    if not arqs:
        print(u"NAO SE APLICA: %s nao tem a serie dd_mao0..5 (so o _dedos tem)"
              % pasta)
        return 0

    tons = {}
    for n in arqs:
        m = re.match(r"^dd_mao(\d)([a-z]?)\.png$", n)
        tons.setdefault(m.group(2) or u"-", {})[int(m.group(1))] = n

    problemas, telas = [], set()
    print(u"%s -> serie das maos: %d arquivo(s), %d tom(ns)"
          % (pasta, len(arqs), len(tons)))

    base_tom = sorted(tons)[0]
    silhuetas = {}
    for tom in sorted(tons):
        serie = tons[tom]
        faltam = [d for d in range(6) if d not in serie]
        if faltam:
            problemas.append(u"tom '%s': faltam as maos de %s dedo(s)"
                             % (tom, u", ".join(str(d) for d in faltam)))
            continue
        areas, sil = [], {}
        for d in range(6):
            tam, alfa = corpo(os.path.join(img, serie[d]))
            telas.add(tam)
            areas.append(int(alfa.sum()))
            sil[d] = alfa
        silhuetas[tom] = sil
        print(u"   tom '%s'  tinta: %s"
              % (tom, u" ".join(u"%d=%d" % (d, areas[d]) for d in range(6))))

        # 1) a tinta tem de crescer
        for d in range(5):
            if areas[d + 1] <= areas[d] * (1.0 + FOLGA):
                problemas.append(
                    u"tom '%s': a mao de %d dedos nao tem tinta a mais que a de "
                    u"%d (%d contra %d) — caixa trocada ou recorte comendo dedo"
                    % (tom, d + 1, d, areas[d + 1], areas[d]))

        # 2) nenhuma duas iguais
        for d in range(6):
            for e in range(d + 1, 6):
                if sil[d].shape == sil[e].shape:
                    dif = float(np.logical_xor(sil[d], sil[e]).sum())
                    if dif / max(1.0, float(sil[d].sum())) < 0.01:
                        problemas.append(
                            u"tom '%s': a mao de %d e a de %d sao a MESMA figura"
                            % (tom, d, e))

    # 3) os tons sao a mesma mao
    if base_tom in silhuetas:
        for tom in sorted(silhuetas):
            if tom == base_tom:
                continue
            for d in range(6):
                a, b = silhuetas[base_tom][d], silhuetas[tom][d]
                if a.shape != b.shape:
                    problemas.append(u"tom '%s': a mao de %d tem outra tela"
                                     % (tom, d))
                    continue
                dif = float(np.logical_xor(a, b).sum()) / max(1.0, float(a.sum()))
                if dif > TOM_IGUAL:
                    problemas.append(
                        u"tom '%s': a mao de %d nao e a mesma do tom '%s' "
                        u"(%.1f%% de silhueta diferente) — a recoloracao comeu "
                        u"ou inventou desenho" % (tom, d, base_tom, dif * 100))

    # 4) todas na mesma tela
    if len(telas) > 1:
        problemas.append(
            u"as maos vem em %d telas diferentes (%s) — assim os pulsos nao se "
            u"alinham e a tela pula debaixo do dedo da crianca; ver a funcao "
            u"`mesma_tela` em %s/recortar_das_folhas.py"
            % (len(telas), u", ".join(u"%dx%d" % t for t in sorted(telas)), pasta))

    if problemas:
        print(u"   %d PROBLEMA(S):" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1
    print(u"   ok: a tinta cresce de 0 a 5, nenhuma figura repetida, os tons "
          u"sao a mesma mao, todas na mesma tela %dx%d"
          % tuple(list(telas)[0]))
    print(u"   ⚠️ e o que ele NAO mede: a CONTAGEM em si. Olhar %s/_contato.png"
          % pasta)
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/dedos_contam.py <pasta>")
        sys.exit(2)
    sys.exit(main(os.path.relpath(sys.argv[1].rstrip(u"/"))))
