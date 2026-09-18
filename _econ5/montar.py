# -*- coding: utf-8 -*-
u"""
============================================================
 MONTADOR DO SITE — "Santa Catarina que Produz" (5º ano, Geografia)

 O MOLDE e o site de pesquisa + quiz `_vale4` (A Viagem no Tempo do Vale):
 capa com nome/turma/avatar, revista com fotos reais, narracao por parada,
 quiz com voz em cada pergunta e em cada opcao, medalha, envio ao painel.
 O `index.html` desta pasta NASCEU como copia daquele; o que muda mora em
 `conteudo.py` (as secoes, as 25 questoes, os textos fixos) e este script
 injeta tudo no HTML, gera `falas.json` (a VERDADE da voz, mesma chave djb2
 que o app usa em `_chaveVoz`) e `creditos.json` (autor e licenca de cada
 foto, porque foto de acervo publico se credita).

 ⚠️ REGRA ZERO vale para o conteudo: todo numero e fato em `conteudo.py` tem
    a fonte ao lado (`_pesquisa/web/econ5-*.md`, colhidos em 18/set/2026).

 Uso:  python3 _econ5/montar.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import conteudo as C                                             # noqa: E402

INI = u"/* ====== CONFIG ====== */"
FIM = u"/* embaralha as opções de cada questão"


def chave_voz(t):
    u"""A MESMA conta do `_chaveVoz` do app (djb2 em base 36, prefixo v)."""
    s = re.sub(r"\s+", u" ", u"" + t).strip()
    h = 5381
    for c in s:
        h = ((h * 33) + ord(c)) & 0xFFFFFFFF
    return u"v0" if h == 0 else u"v" + _b36(h)


def _b36(n):
    d = u"0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return u"0"
    s = u""
    while n:
        s = d[n % 36] + s
        n //= 36
    return s


def js(v):
    return json.dumps(v, ensure_ascii=False)


def bloco_config():
    L = []
    L.append(INI)
    L.append(u"var TURMAS=%s;" % js(C.TURMAS))
    L.append(u"var AVATARES=%s;" % js([{u"id": a} for a in C.AVATARES]))
    L.append(u'var SLUG=%s;  /* Firebase: /provas/<SLUG> */' % js(C.SLUG))
    L.append(u'var FIREBASE_DB="https://atividades-educativas-16860-default-rtdb.firebaseio.com";')
    L.append(u"var GUIA=%s;   /* mascote-guia */" % js(u"img/" + C.GUIA))
    L.append(u"var HISTORIA=%s;" % js(C.HISTORIA))
    L.append(u"var _histTocada=false;")
    L.append(u"")
    L.append(u"/* ====== falas fixas (também lidas pelo gerador de voz) ====== */")
    L.append(u"var TXT_PORTAL_INTRO=%s;" % js(C.TXT_PORTAL_INTRO))
    L.append(u"var TXT_FINAL=%s;" % js(C.TXT_FINAL))
    L.append(u'var MSG_NOME="Escreva o seu nome para começar.";')
    L.append(u'var MSG_TURMA="Escolha a sua turma.";')
    L.append(u'var MSG_AVATAR="Escolha o seu personagem.";')
    L.append(u"var FRASES_NEXT=%s;" % js(C.FRASES_NEXT))
    L.append(u"function falaPergunta(q,n){")
    L.append(u'  return "Pergunta "+n+". "+q.pergunta+" Ouça as respostas e toque na certa.";')
    L.append(u"}")
    L.append(u"")
    L.append(u"/* ====== SEÇÕES DO PORTAL (revista) ====== */")
    secs = []
    for s in C.SECOES:
        secs.append({u"cls": s[u"cls"], u"tag": s[u"tag"], u"img": s[u"img"],
                     u"titulo": s[u"titulo"], u"texto": s[u"texto"],
                     u"fatos": s[u"fatos"], u"fala": s[u"fala"],
                     u"credito": s.get(u"credito", u"")})
    L.append(u"var SECOES=%s;" % json.dumps(secs, ensure_ascii=False, indent=1))
    L.append(u"")
    L.append(u"/* ====== QUIZ (múltipla escolha, resposta controlada aqui) ====== */")
    qs = []
    for q in C.QUESTOES:
        d = {u"sec": q[u"sec"], u"pergunta": q[u"pergunta"], u"opcoes": q[u"opcoes"],
             u"correta": q[u"correta"]}
        if q.get(u"img"):
            d[u"img"] = q[u"img"]
        qs.append(d)
    L.append(u"var QUESTOES=%s;" % json.dumps(qs, ensure_ascii=False, indent=1))
    L.append(u"var SECNOME=%s;" % js(C.SECNOME))
    L.append(u"")
    return u"\n".join(L) + u"\n"


def falas():
    textos = [C.HISTORIA, C.TXT_PORTAL_INTRO, C.TXT_FINAL,
              u"Escreva o seu nome para começar.", u"Escolha a sua turma.",
              u"Escolha o seu personagem."] + list(C.FRASES_NEXT)
    for s in C.SECOES:
        textos.append(s[u"fala"])
    for n, q in enumerate(C.QUESTOES):
        textos.append(u"Pergunta %d. %s Ouça as respostas e toque na certa." % (n + 1, q[u"pergunta"]))
        textos.extend(q[u"opcoes"])
    vistos, out = set(), []
    for t in textos:
        k = chave_voz(t)
        if k in vistos:
            continue
        vistos.add(k)
        out.append({u"id": k, u"texto": t})
    return out


def main():
    cam = os.path.join(AQUI, u"index.html")
    h = io.open(cam, encoding=u"utf-8").read()
    a, b = h.find(INI), h.find(FIM)
    if a < 0 or b < 0:
        print(u"nao achei os marcadores CONFIG/embaralha no index.html")
        return 1
    h = h[:a] + bloco_config() + h[b:]
    for velho, novo in C.TROCAS_NO_MOLDE:
        if velho not in h:
            print(u"   aviso: troca nao achou %r" % velho[:50])
        h = h.replace(velho, novo)
    io.open(cam, u"w", encoding=u"utf-8").write(h)
    F = falas()
    io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
        json.dumps(F, ensure_ascii=False, indent=1))
    cred = [{u"arquivo": s[u"img"], u"legenda": s[u"titulo"], u"credito": s.get(u"credito", u"")}
            for s in C.SECOES if s.get(u"credito")]
    io.open(os.path.join(AQUI, u"creditos.json"), u"w", encoding=u"utf-8").write(
        json.dumps(cred, ensure_ascii=False, indent=1))
    # o que cada imagem citada precisa existir
    faltam = [s[u"img"] for s in C.SECOES if not os.path.exists(os.path.join(AQUI, u"img", s[u"img"]))]
    faltam += [q[u"img"] for q in C.QUESTOES if q.get(u"img") and not os.path.exists(os.path.join(AQUI, u"img", q[u"img"]))]
    print(u"montado: %d secoes, %d questoes, %d falas, %d creditos%s"
          % (len(C.SECOES), len(C.QUESTOES), len(F), len(cred),
             u"; FALTAM IMAGENS: %s" % u", ".join(sorted(set(faltam))) if faltam else u""))
    return 0


if __name__ == u"__main__":
    sys.exit(main())
