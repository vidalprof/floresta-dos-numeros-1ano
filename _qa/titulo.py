# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 0b13 — "o TÍTULO diz o que a criança vai aprender?"

 ⭐ ORDEM DO MARCOS (20/set/2026), depois de abrir o caderno do corpo humano:
    ***"mude o título, sempre coloque algo como APRENDENDO O SISTEMA DIGESTÓRIO
    etc"***.

    O caderno chamava-se *"A Viagem Dentro de Você"*. Bonito, e não dizia nada.
    Ele abre o painel com 99 atividades na escola, na frente da turma, e precisa
    saber **o que é** antes de clicar — e a criança também, para reconhecer no
    dia seguinte que já fez aquela. Título figurado obriga os dois a adivinhar.

 O QUE ELE MEDE:
   1. **RESTO DO ESQUELETO** — `<title>` com "Nº ano" (o molde vazio que ninguém
      trocou). Achado ao escrever este portão: CINCO atividades estavam assim, e
      a aba do navegador da escola mostrava literalmente "Nº ano".
   2. **O TÍTULO NOMEIA O ASSUNTO** — pelo menos uma palavra de conteúdo do
      título aparece nos objetivos/conceitos declarados no `curriculo.json`.
      É a forma medível do pedido dele: "aprendendo o sistema digestório" bate
      (digestório está no objetivo); "A Viagem Dentro de Você" não bate nada.

 ⚠️ O QUE ELE **NÃO** MEDE, e não é modéstia: se o título é BOM. "Rimas" no
    título faz "O Bando das Rimas" passar, e esse título continua sendo mais
    figurado do que o Marcos pediu. O portão pega o caso extremo — título que
    não tem NENHUMA palavra do que se aprende. O gosto continua sendo dele.

 ⚠️ Palavra de conteúdo = fora da lista de palavras vazias e com 3+ letras; a
    comparação é pelos 6 primeiros caracteres sem acento, para "sílaba/sílabas"
    e "digestório/digestivo" baterem.

 Atividade sem `curriculo.json`: mede só a regra 1 (o resto do esqueleto).

 Uso:  python3 _qa/titulo.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys
import unicodedata

VAZIAS = set(u"""a o as os um uma uns umas de do da dos das e em no na nos nas com por
para que se ao aos pelo pela pelos pelas seu sua meu minha dia jogo grande pequeno
ano anos atividade caderno folha folhas""".split())


def _tira(s):
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn").lower()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    if os.path.isfile(pasta):
        pasta = os.path.dirname(os.path.abspath(pasta))
    ih = os.path.join(pasta, u"index.html")
    if not os.path.exists(ih):
        print(u"%s -> NAO MEDI: sem index.html." % pasta)
        return 2
    h = io.open(ih, encoding=u"utf-8").read()
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if not m:
        print(u"%s -> REPROVADO: a pagina nao tem <title>." % pasta)
        return 1
    bruto = re.sub(r"\s+", u" ", m.group(1)).strip()

    erros = []
    # 1) resto do esqueleto
    if re.search(u"N[ºo°]\\s*ano", bruto):
        erros.append(u'o <title> ainda tem "Nº ano", do molde vazio: '
                     u"a aba do navegador mostra isso na escola")

    tit = re.sub(u"\\s*[—–-]\\s*[^—–-]*ano\\s*$", u"", bruto).strip()

    # 2) o titulo nomeia o assunto
    cj = os.path.join(pasta, u"curriculo.json")
    bate = []
    if os.path.exists(cj):
        try:
            C = json.load(io.open(cj, encoding=u"utf-8"))
        except Exception as e:                                 # noqa: BLE001
            print(u"%s -> NAO MEDI: curriculo.json ilegivel (%s)." % (pasta, e))
            return 2
        alvo = u" ".join(u"%s %s %s" % (o.get(u"objetivo", u""),
                                        o.get(u"habilidade", u""),
                                        o.get(u"objeto", u""))
                         for o in C.get(u"objetivos", []))
        alvo += u" " + u" ".join(C.get(u"conceitos") or [])
        alvo = _tira(alvo)
        pal = [w for w in re.findall(u"[A-Za-zÀ-ÿ]{3,}", tit)
               if _tira(w) not in VAZIAS]
        bate = [w for w in pal if _tira(w)[:6] in alvo]
        if not bate:
            erros.append(u'nenhuma palavra do titulo aparece nos objetivos do '
                         u'curriculo.json: ele nao diz o que a crianca vai aprender '
                         u'(ordem do Marcos: "sempre coloque algo como aprendendo o '
                         u'sistema digestorio")')

    if erros:
        print(u"%s -> REPROVADO: «%s»" % (pasta, bruto))
        for e in erros:
            print(u"    - %s" % e)
        return 1
    if bate:
        print(u"%s -> titulo ok: «%s» (diz o assunto: %s)"
              % (pasta, bruto, u", ".join(bate)))
    else:
        print(u"%s -> titulo sem resto de esqueleto: «%s». "
              u"NAO MEDI se ele diz o assunto (sem curriculo.json)." % (pasta, bruto))
        return 2
    print(u"   ⚠️ o portao pega o titulo que nao diz NADA do assunto; se ele e BOM, "
          u"quem decide e o Marcos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
