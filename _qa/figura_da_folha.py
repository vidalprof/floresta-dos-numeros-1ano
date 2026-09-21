# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO — A FIGURA VEIO DA FOLHA DE PAPEL?  (1i5)

 ⭐ A PERGUNTA DO MARCOS QUE DEU ORIGEM A ELE (14/set/2026):
    *"Por que você não cumpre o que combinamos?"*

    A regra existe desde set/2026 e está escrita no `CLAUDE.md` com todas as
    letras: *"A figura vem da MESMA folha (`recortar_das_folhas.py`): gesto e
    desenho nascem juntos, e a criança reconhece a atividade que a professora dá
    no papel."* No caderno de multiplicação eu colhi 40 folhas, li as 40, tirei o
    gesto de cada uma delas — **e fui buscar as 22 figuras no banco**. Todos os
    defeitos de imagem daquela entrega vieram daí: um balão que era folha de
    colorir em preto e branco, halo branco em cinco figuras, a forminha de papel
    do brigadeiro que custou uma volta inteira de banca.

 ⚠️ E A CAUSA NAO FOI FALTA DE REGRA: foi a regra ter ficado como LEMBRETE em
    vez de MEDIDA. Nesta casa o que não é medido depende da minha memória, e a
    minha memória começa do zero a cada sessão — é para isso que os portões
    existem. A lição já estava escrita no `CLAUDE.md` ("o conserto tem DUAS
    partes: arrumar o código E criar o portão"); este arquivo é a segunda parte,
    atrasada.

 O QUE ELE MEDE:

 1. **Declaração.** Todo caderno de folha viva tem `<pasta>/img/ORIGEM.json`
    dizendo, figura por figura, de onde ela veio:
       "folha:d29"   recortada da folha de papel d29 da colheita
       "banco:uva"   reaproveitada do banco de imagens
       "gerada:..."  desenhada por IA
    Sem isso ele diz NAO MEDI — que não é "passou".
 2. **A declaração bate com o disco:** nada declarado que não exista, nada no
    disco que não esteja declarado.
 3. **A REGRA DA ORIGEM:** se existe colheita para este caderno (um
    `_sequencias/POTE-*.md` que cita a pasta e aponta uma pasta de folhas), e
    **nenhuma** figura foi recortada dela, REPROVA.

 ⚠️ ELE NAO INVENTA PORCENTAGEM. "Tem colheita e você não usou nenhuma" é uma
    linha dura, que não depende de palpite meu. Quanto do caderno deve vir do
    papel é decisão do Marcos, não de um número que eu escolhesse aqui.

 ⚠️ E ELE NAO MEDE SE O RECORTE FICOU BONITO. Isso é o olho, e o `_qa/halo.py`.

 Uso:  python3 _qa/figura_da_folha.py <pasta>
 Codigo 0 = ok · 1 = REPROVADO · 2 = nao deu para medir
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import re
import sys

FORA = (u"trofeu", u"estrela_off")   # selos da casa, não são conteúdo da folha


def crivo_da_pasta(pasta):
    u"""Acha o crivo que fala DESTA pasta e a colheita que ele cita.

    Devolve (caminho do crivo, pasta das folhas) ou (None, None)."""
    nome = os.path.basename(pasta.rstrip(u"/"))
    for cam in sorted(glob.glob(os.path.join(u"_sequencias", u"POTE-*.md"))):
        try:
            txt = io.open(cam, encoding=u"utf-8").read()
        except Exception:
            continue
        if u"`%s`" % nome not in txt and nome not in txt:
            continue
        for m in re.finditer(r"_sequencias/(folhas[\w-]*)", txt):
            d = os.path.join(u"_sequencias", m.group(1))
            if os.path.isdir(d):
                return cam, d
        return cam, None
    return None, None


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/figura_da_folha.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    if not os.path.exists(os.path.join(pasta, u"folhas.js")):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva (sem folhas.js)." % pasta)
        return 2
    dimg = os.path.join(pasta, u"img")
    if not os.path.isdir(dimg):
        print(u"%s -> NAO MEDI: nao achei a pasta img." % pasta)
        return 2

    no_disco = sorted(os.path.basename(f) for f in glob.glob(os.path.join(dimg, u"*.png")))
    no_disco = [f for f in no_disco if not any(f[:-4].endswith(x) for x in FORA)]
    cam_org = os.path.join(dimg, u"ORIGEM.json")
    crivo, colheita = crivo_da_pasta(pasta)

    if not os.path.exists(cam_org):
        print(u"%s -> NAO MEDI: as %d figura(s) nao dizem de onde vieram."
              % (pasta, len(no_disco)))
        print(u"   (isto nao e 'passou'. Escrever %s com uma linha por figura:" % cam_org)
        print(u'    {"mu_maca.png": "folha:d29"} · "banco:maca" · "gerada:pollinations")')
        if colheita:
            print(u"   ⚠️ e ha colheita para este caderno em %s — a regra da casa manda"
                  % colheita)
            print(u"      a figura vir da MESMA folha de onde veio o gesto.")
        return 2

    try:
        org = json.load(io.open(cam_org, encoding=u"utf-8"))
    except Exception as e:
        print(u"%s -> NAO MEDI: %s nao e JSON valido (%s)." % (pasta, cam_org, e))
        return 2

    erros, contas = [], {}
    for f in no_disco:
        de = org.get(f)
        if not de:
            erros.append(u"a figura %s esta no disco e nao foi declarada" % f)
            continue
        # ⚠️ DECLARAÇÃO QUE NÃO É TEXTO NÃO PODE MATAR O PORTÃO (21/set/2026).
        #    O `_dinheiro5` escreveu aqui um objeto com a caixa do recorte
        #    dentro — o que era erro dele — e este portão estourou com
        #    AttributeError, derrubando a linha inteira do pré-voo em vez de
        #    dizer o que estava errado. Portão que morre não mede, e ainda leva
        #    junto a informação de que havia algo a consertar.
        if not isinstance(de, type(u"")):
            erros.append(u"a figura %s foi declarada com um objeto; aqui o valor "
                         u"tem de ser texto, como \"folha:d26\"" % f)
            continue
        tipo = de.split(u":")[0]
        contas[tipo] = contas.get(tipo, 0) + 1
    for f in org:
        if f not in no_disco and not os.path.exists(os.path.join(dimg, f)):
            erros.append(u"%s foi declarada e nao existe no disco" % f)

    print(u"%s -> origem das figuras: %d no disco" % (pasta, len(no_disco)))
    for t in sorted(contas, key=lambda x: -contas[x]):
        rot = {u"folha": u"recortada da folha de papel", u"banco": u"do banco de imagens",
               u"gerada": u"gerada por IA"}.get(t, t)
        print(u"   %-28s %3d" % (rot, contas[t]))
    if crivo:
        print(u"   colheita deste caderno: %s%s"
              % (crivo, u" -> %s" % colheita if colheita else u" (sem pasta de folhas)"))

    if colheita and not contas.get(u"folha"):
        erros.append(
            u"ha colheita em %s e NENHUMA das %d figuras foi recortada dela — a regra "
            u"da casa (CLAUDE.md) manda a figura vir da MESMA folha de onde veio o gesto, "
            u"para a crianca reconhecer a atividade que a professora da no papel"
            % (colheita, len(no_disco)))

    if erros:
        print(u"   REPROVADO:")
        for e in erros:
            print(u"    - %s" % e)
        return 1
    print(u"   ✓ toda figura diz de onde veio, e a regra da origem esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
