# -*- coding: utf-8 -*-
u"""
============================================================
 O CADERNO INTEIRO NUMA FOLHA SÓ — para quem vai escrever o PARECER (0b12)

 ⭐ POR QUE ELE EXISTE (20/set/2026). O portão `_qa/parecer.py` cobra que alguém
    tenha ASSINADO que o caderno é adequado ao ano. Mas quem assina precisa ter
    LIDO — e ler um caderno de 35 folhas abrindo `folhas.js`, `falas.json` e
    `curriculo.json` de um lado para o outro leva meia hora e ainda assim deixa
    passar o que mais importa: a folha 9 dizendo o contrário da folha 31.

    ⚠️ Foi exatamente esse o defeito do `_corpo5`: o portão 0b9 passou com nota
       cheia (as citações existiam palavra por palavra) e o caderno ensinava, em
       duas folhas diferentes, coisas que se contradiziam. Quem pegou foi o olho
       humano, lendo as folhas EM ORDEM, uma embaixo da outra.

 O que ele imprime, na ordem em que a criança encontra:
   · o título (os cinco lugares onde ele mora), o ano e o componente;
   · cada objetivo declarado, com as folhas que ele diz medir;
   · folha a folha: o número, o nome, o enunciado que a criança ouve, e qual
     objetivo diz cobri-la;
   · no fim, o que NÃO fecha: folha sem objetivo, objetivo sem folha, folha
     cujo número não existe.

 ⚠️ Ele NÃO julga nada — não é portão, não tem código de reprovação. É a mesa
    posta para o pedagogo. O julgamento é de quem assina o parecer.

 Uso: python3 _qa/folha_a_folha.py <pasta>
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys


def enunciados(pasta):
    u"""{numero da folha: texto que a criança ouve}.

    ⚠️ A fonte é o bloco `/*FALAS-INI*/ var FALAS = {...}` do `index.html`, e
       NÃO o `falas.json`: no `falas.json` cada fala é gravada com um `id`
       embaralhado (`gv_38njv4`), que serve ao gravador de voz e não diz de que
       folha é. Quem guarda a chave legível (`p14enun`) é o bloco do HTML."""
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam):
        return {}
    s = io.open(cam, encoding=u"utf-8").read()
    fora = {}
    for chave, texto in re.findall(r'"p(\d+)enun"\s*:\s*"((?:[^"\\]|\\.)*)"', s):
        fora[int(chave)] = texto.replace(u'\\"', u'"').replace(u"\\n", u" ").strip()
    return fora


def nomes(pasta):
    u"""a lista `var NOMES` — o nome de cada folha, na ordem."""
    for arq in (u"index.html", u"folhas.js"):
        cam = os.path.join(pasta, arq)
        if not os.path.exists(cam):
            continue
        s = io.open(cam, encoding=u"utf-8").read()
        m = re.search(r"var\s+NOMES\s*=\s*(\[.*?\])\s*;", s, re.S)
        if not m:
            continue
        try:
            return json.loads(m.group(1))
        except ValueError:
            bruto = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            if bruto:
                return [b.replace(u'\\"', u'"') for b in bruto]
    return []


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/folha_a_folha.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam_html = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam_html):
        print(u"%s -> não achei o index.html." % pasta)
        return 2
    html = io.open(cam_html, encoding=u"utf-8").read()
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = (m.group(1).strip() if m else u"(sem <title>)")

    cur = {}
    cam_cur = os.path.join(pasta, u"curriculo.json")
    if os.path.exists(cam_cur):
        try:
            cur = json.load(io.open(cam_cur, encoding=u"utf-8"))
        except Exception as e:
            print(u"   aviso: curriculo.json ilegível (%s)" % e)

    NOM = nomes(pasta)
    ENU = enunciados(pasta)
    objs = cur.get(u"objetivos") or []

    print(u"=" * 70)
    print(u"%s — %s" % (pasta, titulo))
    print(u"   %sº ano · %s · %d folha(s)"
          % (cur.get(u"ano", u"?"), cur.get(u"componente", u"?"), len(NOM)))
    if cur.get(u"conceitos"):
        print(u"   conceitos declarados: %s" % u"; ".join(cur[u"conceitos"]))
    if cur.get(u"fora_do_curriculo"):
        print(u"   FORA DO CURRÍCULO (declarado): %s" % cur[u"fora_do_curriculo"])
    print(u"=" * 70)

    print(u"\n--- OS OBJETIVOS QUE O CADERNO DECLARA ---")
    dono = {}
    for i, o in enumerate(objs):
        fs = o.get(u"folhas") or []
        print(u" %2d. %s" % (i + 1, o.get(u"objetivo", u"(sem nome)")))
        print(u"     folhas: %s" % (u", ".join(str(f) for f in fs) or u"(nenhuma)"))
        hab = (o.get(u"habilidade") or u"").replace(u"\n", u" ")
        if hab:
            print(u"     %s" % hab[:200])
        for f in fs:
            dono.setdefault(f, []).append(i + 1)

    print(u"\n--- FOLHA A FOLHA, NA ORDEM EM QUE A CRIANÇA ENCONTRA ---")
    for n in range(1, len(NOM) + 1):
        marca = u",".join(str(x) for x in dono.get(n, [])) or u"—"
        print(u" %2d [obj %s] %s" % (n, marca, NOM[n - 1]))
        if ENU.get(n):
            print(u"      “%s”" % ENU[n])

    print(u"\n--- O QUE NÃO FECHA ---")
    sobrando = [n for n in range(1, len(NOM) + 1) if n not in dono]
    print(u" folha(s) que nenhum objetivo diz medir: %s"
          % (u", ".join(str(x) for x in sobrando) or u"nenhuma"))
    fantasma = sorted(f for f in dono if f < 1 or f > len(NOM))
    print(u" objetivo apontando folha que não existe: %s"
          % (u", ".join(str(x) for x in fantasma) or u"nenhum"))
    vazios = [i + 1 for i, o in enumerate(objs) if not (o.get(u"folhas") or [])]
    print(u" objetivo(s) sem folha nenhuma: %s"
          % (u", ".join(str(x) for x in vazios) or u"nenhum"))
    mudas = [n for n in range(1, len(NOM) + 1) if not ENU.get(n)]
    print(u" folha(s) sem enunciado no falas.json: %s"
          % (u", ".join(str(x) for x in mudas) or u"nenhuma"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
