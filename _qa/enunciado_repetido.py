# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 0b14 — DUAS FOLHAS QUE DIZEM A MESMA FRASE

 ⭐ DE ONDE ELE NASCEU (20/set/2026), lendo A Coroa dos Cinco Reinos folha a
    folha para escrever o parecer pedagógico. Três pares de folhas — 12/13,
    14/15 e 16/17 — tinham a narração **idêntica, palavra por palavra**:

      12: "Olhe a figura. De qual reino ela é?"
      13: "Olhe a figura. De qual reino ela é?"

    O nome na faixa do topo era diferente ("De qual reino é este ser?" e "Os
    reinos que não se veem"), e a folha 13 de fato SOBE um degrau — ela traz
    justamente os reinos que só o microscópio mostra.

 ⚠️ POR QUE ISSO É SÉRIO, E NÃO CHATICE: **para quem ainda não lê, a folha É a
    narração.** A criança do 1º e do 2º ano não lê a faixa do topo; ela escuta.
    Duas folhas seguidas dizendo a mesma frase são, para ela, a mesma folha
    outra vez — o *"isso eu já fiz, tô fazendo de novo"* que o Marcos ouve da
    turma e que já virou regra da casa (a repetição vem em BLOCO, e a segunda
    folha do par SOBE UM DEGRAU). O degrau existia nos três pares; o que
    faltava era avisar a criança dele.

 ⚠️ E NENHUM PORTÃO VIA. O `_qa/duplicata.py` compara ITENS, o `_qa/falas.py`
    mede pronúncia, o `_qa/leque_folha.py` conta GESTOS — e dois gestos iguais
    com conteúdos diferentes são legítimos. Ninguém comparava o TEXTO que a
    criança ouve.

 O QUE ELE MEDE: lê o bloco `FALAS` do `index.html` e compara os `pNenun` entre
 si. Reprova quando duas folhas têm o mesmo enunciado.
   · O prefixo "Folha tal." é descontado antes de comparar (ele já diferencia
     por número, e não é o que a criança usa para saber o que mudou).
   · As marcas de negrito e os espaços repetidos também.

 ⚠️ REPETIR DE PROPÓSITO EXISTE: há folha de AQUECIMENTO que repete o comando
    de propósito, a vinte folhas de distância. Quando for o caso, declare em
    `<pasta>/ENUNCIADO-OK.json`:
        {"iguais": [{"folhas": [15, 16], "porque": "..."}]}
    Declarado é decisão — o portão imprime o motivo em toda rodada. Desligar
    sem declarar, não.

 Uso:  python3 _qa/enunciado_repetido.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica / não deu para medir
============================================================
"""
from __future__ import print_function

import collections
import io
import json
import os
import re
import sys


def limpa(t):
    u"""o que a criança de fato ouve de DIFERENTE: sem o "Folha tal.", sem
    negrito, sem espaço repetido."""
    t = re.sub(r"<[^>]+>", u"", t or u"")
    t = re.sub(r"^\s*folha\s+[a-zãáéíóúâêôç\s]+?\s*[.:]\s*", u"", t, flags=re.I)
    t = re.sub(r"\s+", u" ", t).strip().lower()
    return t


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/enunciado_repetido.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam) or not os.path.exists(os.path.join(pasta, u"folhas.js")):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva." % pasta)
        return 2
    s = io.open(cam, encoding=u"utf-8").read()

    enun = {}
    for k, t in re.findall(r'"p(\d+)enun"\s*:\s*"((?:[^"\\]|\\.)*)"', s):
        enun[int(k)] = t.replace(u'\\"', u'"')
    if not enun:
        print(u"%s -> NAO MEDI: nao achei nenhum `pNenun` no bloco FALAS." % pasta)
        return 2

    liberados = {}
    cam_ok = os.path.join(pasta, u"ENUNCIADO-OK.json")
    if os.path.exists(cam_ok):
        try:
            d = json.load(io.open(cam_ok, encoding=u"utf-8"))
            for c in d.get(u"iguais", []):
                liberados[tuple(sorted(c.get(u"folhas", [])))] = c.get(u"porque", u"")
        except Exception as e:
            print(u"%s -> NAO MEDI: %s nao e JSON valido (%s)." % (pasta, cam_ok, e))
            return 2

    inv = collections.defaultdict(list)
    for n, t in enun.items():
        c = limpa(t)
        if c:
            inv[c].append(n)

    erros, olhados = [], []
    for texto, folhas in sorted(inv.items(), key=lambda x: x[1]):
        if len(folhas) < 2:
            continue
        folhas = tuple(sorted(folhas))
        if folhas in liberados:
            olhados.append((folhas, texto, liberados[folhas]))
        else:
            erros.append((folhas, texto))

    print(u"%s -> enunciado: %d folha(s) com narracao, %d frase(s) diferente(s)"
          % (pasta, len(enun), len(inv)))
    for folhas, texto, porque in olhados:
        print(u"   declarado em ENUNCIADO-OK.json — folhas %s: “%s”  (%s)"
              % (u", ".join(str(x) for x in folhas), texto[:60], porque))
    if erros:
        print(u"   REPROVADO — a crianca ouve a mesma frase duas vezes:")
        for folhas, texto in erros[:12]:
            print(u"    x folhas %s dizem, palavra por palavra: “%s”"
                  % (u", ".join(str(x) for x in folhas), texto[:70]))
        print(u"   Para quem ainda nao le, a folha E a narracao: duas folhas")
        print(u"   seguidas com a mesma frase sao, para a crianca, a mesma folha")
        print(u"   de novo. Conserto: a segunda do par NOMEIA o que mudou")
        print(u"   (“agora os saltos sao maiores”, “agora sem figura”).")
        print(u"   Se a repeticao for de proposito, declare em %s." % cam_ok)
        return 1
    print(u"   ok: nenhuma folha repete a narracao de outra.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
