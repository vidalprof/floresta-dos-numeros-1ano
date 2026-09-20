# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 0b12 — "o PEDAGOGO assinou esta atividade?"

 ⭐ POR QUE ELE EXISTE (20/set/2026), e a história é curta e feia. O Marcos
    pediu o crivo do pedagogo TRÊS vezes na mesma semana. Nas duas primeiras eu
    mostrei o crivo da COLHEITA (`_sequencias/POTE-*.md`), que é outra coisa. Na
    terceira ele foi direto: *"mas veja, por isso eu pedi o crivo do pedagogo,
    para ver se está adequado e o currículo, SEMPRE FIZEMOS ASSIM"*.

    Ele estava certo, e a conta é esta: havia **onze** `PARECER-PEDAGOGICO.md`
    no repositório, um por atividade, desde as de alfabetização do 1º ano — e
    **trinta e quatro** atividades declarando currículo em `curriculo.json`.
    Ou seja: a prática existia, era dele, e foi se perdendo à medida que eu
    entregava cada vez mais rápido. Vinte e quatro atividades foram ao ar sem
    ninguém assinar que o conteúdo é do ano.

 ⚠️ E NÃO É O PORTÃO 0b9. O `pedagogo_curriculo.py` confere que a CITAÇÃO existe
    palavra por palavra e que os conceitos declarados cabem no bloco do ano —
    coisas que se medem. O PARECER é o que nenhuma conta alcança: **contradição
    entre folhas**, título que promete o que a folha não entrega, degrau que não
    sobe, vocabulário acima do ano. No `_corpo5` o 0b9 passou com NOTA CHEIA
    enquanto a folha 9 ensinava o contrário da folha 31.

 O QUE ELE MEDE (e o que NÃO mede):
   1. a atividade que declara currículo (`curriculo.json`) tem
      `PARECER-PEDAGOGICO.md`;
   2. esse parecer CITA o documento da rede (`_curriculo/blumenau.txt`) — senão
      não foi conferido contra nada;
   3. tem a seção do VEREDITO, com a palavra ADEQUADA ou NÃO ADEQUADA escrita;
   4. tem a data da conferência.
   ⚠️ Ele **não** lê o conteúdo do parecer nem julga se o julgamento está certo.
      Isso é trabalho de quem assina. O portão garante que ALGUÉM assinou, e não
      que assinou bem — é a mesma honestidade do `curriculo.json`.

 Atividade ANTIGA, sem `curriculo.json`: NAO MEDI (código 2), que não é
 "passou" — é "esta é de antes do padrão".

 Uso:  python3 _qa/parecer.py <pasta>
 Código 0 = assinado · 1 = REPROVADO · 2 = não se aplica / não deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

NOME = u"PARECER-PEDAGOGICO.md"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    if os.path.isfile(pasta):
        pasta = os.path.dirname(os.path.abspath(pasta))
    if not os.path.isdir(pasta):
        print(u"%s -> NAO MEDI: nao e uma pasta." % pasta)
        return 2

    tem_cur = os.path.exists(os.path.join(pasta, u"curriculo.json"))
    cam = os.path.join(pasta, NOME)
    if not os.path.exists(cam):
        if not tem_cur:
            print(u"%s -> NAO SE APLICA: atividade sem curriculo.json (de antes "
                  u"do padrao). Isso NAO e 'passou'." % pasta)
            return 2
        print(u"%s -> REPROVADO: declara curriculo e NAO tem %s." % (pasta, NOME))
        print(u"   O portao 0b9 confere a CITACAO; o parecer e quem olha o que a")
        print(u"   crianca faz na tela e diz se e do ano. Sao duas coisas.")
        print(u"   Molde: `_rima1/PARECER-PEDAGOGICO.md` (objetivo verbatim, a")
        print(u"   escada folha a folha, o crivo do conteudo, ressalvas, parecer).")
        return 1

    txt = io.open(cam, encoding=u"utf-8").read()
    faltas = []
    if u"blumenau" not in txt.lower():
        faltas.append(u"nao cita o documento da rede (_curriculo/blumenau.txt): "
                      u"conferido contra o que?")
    if not re.search(u"(?i)\\bN[AÃ]O ADEQUADA\\b|\\bADEQUADA\\b|\\bADEQUADO\\b", txt):
        faltas.append(u"nao tem o VEREDITO escrito (a palavra ADEQUADA / NAO ADEQUADA)")
    if not re.search(u"(?i)conferid[oa] em|conferid[oa]:", txt):
        faltas.append(u"nao diz QUANDO foi conferido")
    if len(txt.split()) < 150:
        faltas.append(u"tem menos de 150 palavras: parecer de uma linha nao e parecer")

    if faltas:
        print(u"%s -> REPROVADO: o %s existe mas esta incompleto:" % (pasta, NOME))
        for f in faltas:
            print(u"    - %s" % f)
        return 1

    m = re.search(u"(?i)conferid[oa] em ([^,\\.]{4,40})", txt)
    quando = m.group(1).strip() if m else u"(data no corpo)"
    print(u"%s -> parecer pedagogico assinado (%d palavras, conferido em %s)"
          % (pasta, len(txt.split()), quando))
    print(u"   ⚠️ o portao le se ALGUEM assinou, nao se assinou bem: o julgamento")
    print(u"      continua sendo de quem escreve o parecer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
