# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1w — A SILABA CONFERIDA CONTRA UM DICIONARIO DE VERDADE

 ⭐ PERGUNTA DO MARCOS (17/set/2026): *"existe algum banco de audio em portugues,
    para vc comparar e checar se as silabas e palavras estao corretas na
    atividade?"*

 A resposta honesta era: as divisoes do `silabas.json` saiam da MINHA cabeca.
 Nada as conferia. E divisao silabica errada nao da erro em lugar nenhum — o
 app abre, a voz sai, e a crianca ouve o pedaco errado com toda a naturalidade
 do mundo. E exatamente o tipo de defeito que a REGRA ZERO proibe.

 O BANCO QUE EXISTE E DA PARA USAR DAQUI: o dicionario de hifenizacao pt_BR do
 LibreOffice/OpenOffice, empacotado no `pyphen` (PyPI alcanca do chat; o
 HuggingFace e o alphacephei nao — medido em 17/set/2026). Nao e um banco de
 AUDIO: e um banco de TEXTO, publicado, usado por todo editor de texto em
 portugues ha vinte anos.

 ⚠️⚠️ E ELE TEM UM LIMITE QUE PRECISA ESTAR ESCRITO, senao o portao vira medida
    falsa: um dicionario de HIFENIZACAO serve para quebrar linha, e por isso ele
    DE PROPOSITO cala alguns cortes validos — nunca deixa uma letra sozinha na
    ponta. Para `amor`, cuja divisao e A-MOR, ele nao oferece corte nenhum.

    Entao a regra deste portao e de MAO UNICA:
      · o dicionario ACUSA um corte que eu nao tenho  -> isso e forte, reprova;
      · o dicionario tem MENOS cortes do que eu       -> isso nao diz nada.
    Ele so acusa; nunca manda.

 O QUE ELE MEDE, exatamente: cada pedaco que o app FALA SOZINHO (o `SILMAP` do
 `index.html`, que e o que vira botao para a crianca). Se o dicionario ainda
 corta aquele pedaco, ele nao e uma silaba — e um pedaco de exercicio. Isso
 pode ser legitimo (a folha de papel manda juntar CAMA + LEAO), mas tem de
 estar DECLARADO em `<pasta>/silabas-ok.json`, com o motivo, do mesmo jeito que
 o `img/SOBRA-OK.json`.

 ⚠️ O QUE ELE NAO MEDE: se o mp3 diz o que esta escrito. Isso e ASR (voz ->
    texto) e o modelo mora no HuggingFace, que o chat nao alcanca — tem de ser
    no runner do Actions. Enquanto isso, este portao NAO e "o audio conferido".

 Uso:  python3 _qa/silaba_dicionario.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys


def _silmap(pasta):
    ih = os.path.join(pasta, u"index.html")
    if not os.path.exists(ih):
        return None
    h = io.open(ih, encoding=u"utf-8").read()
    m = re.search(r"/\*SILMAP-INI\*/\s*var SILMAP = (\{.*?\});", h, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def confere(pasta):
    try:
        import pyphen
    except ImportError:
        return 2, [u"   sem o `pyphen` (pip install pyphen): NAO MEDI — e isto "
                   u"NAO e 'passou'. O dicionario pt_BR vem dentro dele."]
    if u"pt_BR" not in pyphen.LANGUAGES:
        return 2, [u"   o `pyphen` instalado nao traz o dicionario pt_BR: NAO MEDI"]

    S = _silmap(pasta)
    if S is None:
        return 2, [u"   sem `SILMAP` no index.html: este caderno nao fala silaba "
                   u"sozinha, ou nao e folha viva. NAO MEDI"]
    if not S:
        return 0, [u"   ok: este caderno nao fala nenhuma silaba sozinha "
                   u"(SILMAP vazio), entao nao ha o que conferir"]

    hif = pyphen.Pyphen(lang=u"pt_BR")
    ok_dec = {}
    fok = os.path.join(pasta, u"silabas-ok.json")
    if os.path.exists(fok):
        try:
            ok_dec = json.load(io.open(fok, encoding=u"utf-8"))
        except ValueError:
            pass

    L = [u"   ⚠️ MAO UNICA, e isto e parte da medida: o dicionario de "
         u"hifenizacao cala cortes de uma letra so (para `amor` ele nao oferece "
         u"corte). Ele so ACUSA corte a mais; nunca exige."]
    maus, declarados = [], []
    for pedaco in sorted(S):
        partes = hif.inserted(pedaco.lower()).split(u"-")
        if len(partes) <= 1:
            continue
        de = S[pedaco][0] if isinstance(S[pedaco], list) and S[pedaco] else u"?"
        if pedaco in ok_dec:
            declarados.append((pedaco, de, u"-".join(partes), ok_dec[pedaco]))
        else:
            maus.append((pedaco, de, u"-".join(partes)))

    if maus:
        L.append(u"   REPROVADO: %d pedaco(s) que o app fala como se fossem "
                 u"UMA silaba, e o dicionario pt_BR ainda corta por dentro:"
                 % len(maus))
        for pedaco, de, corte in maus:
            L.append(u"      • %-12s (recortado de %s) -> o dicionario divide %s"
                     % (pedaco, de, corte))
        L.append(u"   conserto: ou divida a palavra certo no `gerar_falas.py` "
                 u"(`_reg`), ou — se o pedaco for da FOLHA DE PAPEL, como o "
                 u"CAMA + LEAO de camaleao — declare em %s/silabas-ok.json "
                 u"com o motivo." % pasta)
        return 1, L

    L.append(u"   ✓ os %d pedaco(s) falados sozinhos conferem com o dicionario "
             u"pt_BR: nenhum esconde um corte por dentro" % len(S))
    if declarados:
        # ⚠️ o que foi perdoado sai IMPRESSO em toda rodada, senao vira gaveta
        #    onde se esconde defeito.
        L.append(u"   %d pedaco(s) DECLARADO(S) como pedaco de exercicio, e nao "
                 u"como silaba:" % len(declarados))
        for pedaco, de, corte, por in declarados:
            L.append(u"      · %-12s (%s, dicionario: %s) — %s"
                     % (pedaco, de, corte, por))
    return 0, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/silaba_dicionario.py <pasta>")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, L = confere(pasta.rstrip(u"/"))
        cabec = {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]
        print(u"%s -> silaba x dicionario: %s" % (pasta.rstrip(u"/"), cabec))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
