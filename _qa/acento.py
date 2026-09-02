# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE ACENTO — "a voz vai ler a palavra CERTA?"
#
#  Nasceu de um erro bobo que se repetia SEMPRE (Marcos, set/2026:
#  *"esses erros bobos se repetem sempre"*): a grade de caça-palavras (e a
#  forca, a cruzadinha, as letras-escondidas) NAO carrega cedilha nem acento,
#  entao a palavra vinha escrita crua — "ROCA" — e o rotulo E a voz liam esse
#  texto cru: a voz dizia "roca" (a de fiar) no lugar de "roca" (o campo).
#
#  O conserto ANTIGO era uma LISTA de 15 palavras no montar.py. Lista feita a
#  mao SEMPRE fica pra tras: o proximo erro e uma palavra NOVA que nao esta
#  nela. Este portao NAO tem lista: ele APRENDE o vocabulario do proprio
#  projeto — toda palavra acentuada que qualquer atividade ja escreveu — e
#  cobra a forma acentuada quando a grade traz a versao crua.
#
#  Como a peca agora DOBRA o acento so na grade (Ç->C), a palavra DEVE ser
#  escrita acentuada: o chip mostra e a voz le com acento; a grade fica ASCII
#  sozinha. Este portao garante que ninguem esqueca de acentuar.
#
#  Uso (banca):    python3 _qa/acento.py <pasta|conteudo.json|index.html>
#  Uso (montador): from acento import checa_conteudo; checa_conteudo(conteudo)
# ============================================================
import collections
import glob
import io
import json
import os
import re
import sys
import unicodedata

# as mecanicas que tiram o acento por CONSTRUCAO (letra/grade em ASCII). So
# nelas a palavra crua e defeito — em prosa o acento e natural.
FAMILIA_GRADE = ("caca-palavras", "forca", "cruzadinha", "letras-escondidas")

_ACENTO = re.compile(u"[À-ſ]")   # tem algum caractere acentuado?
_PAL = re.compile(u"[A-Za-zÀ-ſ]{2,}")


def _tira(s):
    u"""remove acento/cedilha, mantendo a letra base."""
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn")


def _raiz():
    u"""a raiz do projeto (onde moram as pastas _*/)."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(aqui, ".."))


def constroi_vocabulario():
    u"""Le TODAS as falas/conteudos do projeto e devolve dois mapas:
       mp[ascii_maiusculo] = Counter(forma_acentuada) — o que o projeto usa;
       cru[ascii_maiusculo] = quantas vezes a palavra aparece SEM acento
       (para nao acusar palavra que tambem existe crua de verdade)."""
    raiz = _raiz()
    mp = collections.defaultdict(collections.Counter)
    cru = collections.Counter()
    arqs = (glob.glob(os.path.join(raiz, "_*", "falas.json")) +
            glob.glob(os.path.join(raiz, "_*", "conteudo.json")))
    for a in arqs:
        try:
            txt = io.open(a, encoding="utf-8").read()
        except Exception:                                      # noqa: BLE001
            continue
        for w in _PAL.findall(txt):
            wu = w.upper()
            if _ACENTO.search(w):
                mp[_tira(wu)][wu] += 1
            else:
                cru[wu] += 1
    return mp, cru


def _palavras_de_grade(fase):
    u"""as palavras que a peca de grade poe letra a letra (o campo `dados`)."""
    out = []
    dados = fase.get("dados")
    if isinstance(dados, list):
        for x in dados:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, dict):
                for k in ("palavra", "p", "w", "resp", "resposta"):
                    if isinstance(x.get(k), str):
                        out.append(x[k])
                        break
    return out


def checa_conteudo(conteudo, mp=None, cru=None):
    u"""Confere um conteudo.json (dict ou lista de fases) e devolve os achados
    como tuplas (fase_id, mec, crua, acentuada). Lista vazia = ok. E a MESMA
    funcao que o montar.py chama, fonte unica de verdade."""
    if mp is None or cru is None:
        mp, cru = constroi_vocabulario()
    fases = conteudo.get("fases", conteudo) if isinstance(conteudo, dict) else conteudo
    if not isinstance(fases, list):
        return []
    achados = []
    for f in fases:
        if not isinstance(f, dict) or f.get("mec") not in FAMILIA_GRADE:
            continue
        for w in _palavras_de_grade(f):
            if _ACENTO.search(w):
                continue                        # ja acentuada
            wu = w.upper()
            cand = mp.get(_tira(wu))
            if not cand:
                continue
            acent = cand.most_common(1)[0][0]
            if acent == wu:
                continue
            n_ac = sum(cand.values())
            n_cru = cru.get(wu, 0)
            # so acusa quando a forma acentuada e a REGRA no projeto (>=2 usos)
            # e a crua nao e mais comum que ela (senao e palavra ambigua legitima)
            if n_ac >= 2 and n_ac >= n_cru:
                achados.append((f.get("id", "?"), f.get("mec"), wu, acent))
    return achados


def _acha_conteudo(alvo):
    u"""aceita pasta, conteudo.json ou index.html e devolve o conteudo.json."""
    if os.path.isdir(alvo):
        return os.path.join(alvo, "conteudo.json")
    if alvo.endswith("conteudo.json"):
        return alvo
    # index.html -> conteudo.json ao lado
    c = os.path.join(os.path.dirname(os.path.abspath(alvo)), "conteudo.json")
    return c


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/acento.py <pasta|conteudo.json|index.html>")
        return 2
    cj = _acha_conteudo(sys.argv[1])
    if not os.path.exists(cj):
        # sem conteudo.json (atividade fora do padrao) — nao ha o que medir
        print(u"acento: sem conteudo.json em %s — NAO MEDI (fora do padrao)." % sys.argv[1])
        return 2
    try:
        conteudo = json.load(io.open(cj, encoding="utf-8"))
    except Exception as e:                                     # noqa: BLE001
        print(u"acento: nao consegui ler %s (%s)" % (cj, str(e)[:80]))
        return 2
    achados = checa_conteudo(conteudo)
    if not achados:
        print(u"   acento ok: toda palavra de grade que a voz le esta acentuada")
        return 0
    print(u"   %d PALAVRA(S) DE GRADE SEM ACENTO — a VOZ vai ler errado:" % len(achados))
    for fid, mec, crua, acent in achados:
        print(u'      fase %s (%s): "%s" -> escreva "%s" '
              u"(a grade dobra o acento sozinha)" % (fid, mec, crua, acent))
    return 1


if __name__ == "__main__":
    sys.exit(main())
