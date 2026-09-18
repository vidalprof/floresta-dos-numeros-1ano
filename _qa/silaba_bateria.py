# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1z2 — A BATERIA: A REGUA DA SOLETRACAO AINDA TEM FARO?

 ⭐ POR QUE EXISTE (18/set/2026). Em 17/set eu inventei um metodo de conferir a
    silaba que APROVAVA a soletracao, e quem segurou a publicacao foi a regua
    velha de duracao. No dia seguinte a banca mediu a regua velha: ela pegava
    34 dos 47 soletrados e, num lote INTEIRO soletrado, so 4 de 52 (a mediana
    sobe junto). Regua que ninguem afere vai perdendo o faro sem avisar.

 O QUE ELE FAZ: roda as reguas de duracao de `_qa/silabas.py` (teto absoluto por
 tamanho + relativa 2,0x por posicao) sobre DOIS conjuntos que NAO MUDAM:
   · CONTROLE NEGATIVO — os recortes que sairam SOLETRADOS de verdade em
     17/set, guardados em `_pesquisa/silabas-soletradas/` (52 arquivos);
   · CONTROLE POSITIVO — os recortes BONS no ar, dos oito cadernos.
 E reprova A PROPRIA REGUA se ela pegar menos soletrados do que pegava quando
 foi aferida, ou se acusar um bom que seja.

 ⚠️ Os numeros de referencia (abaixo) sao MEDIDOS, nao escolhidos: se voz, RATE
    ou teto mudarem, o faro muda — remede e atualize aqui, com data.

 Uso:  python3 _qa/silaba_bateria.py            (usa os oito cadernos)
 Codigos: 0 a regua mantem o faro · 1 a regua PERDEU o faro · 2 nao medi
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

CADERNOS = u"_alfa1 _ini1 _mont1 _sil1 _roda1 _sil2 _troca2 _nasal2".split()
NEGATIVO = os.path.join(RAIZ, u"_pesquisa", u"silabas-soletradas")

# Aferido em 18/set/2026 (voz pt-BR-AntonioNeural, RATE -25%):
#   teto absoluto  -> pegou 33 dos 52 soletrados, 0 bons (remedido no audio v4)
#   relativa 2,0x por posicao -> +1 (34/52); 1,7x sem posicao acusava SA de SACA
MIN_TETO = 30        # abaixo disto a regua do teto perdeu o faro
MAX_FALSOS = 0       # nenhum bom pode ser acusado


def _base(w):
    s = u"".join(c for c in unicodedata.normalize(u"NFD", w.lower())
                 if unicodedata.category(c) != u"Mn")
    return re.sub(r"[^a-z0-9]", u"", s)


def main():
    try:
        import librosa
    except ImportError:
        print(u"NAO MEDI: falta librosa")
        return 2
    import silabas as S
    if not os.path.isdir(NEGATIVO):
        print(u"NAO MEDI: nao ha controle negativo em %s" % NEGATIVO)
        return 2

    # mapa (pasta, palavra, i) -> silaba escrita
    mapa = {}
    okdec = {}
    for p in CADERNOS:
        sj = os.path.join(RAIZ, p, u"silabas.json")
        if not os.path.exists(sj):
            continue
        D = json.load(io.open(sj, encoding=u"utf-8"))
        for w, sil in (D.get(u"palavras") or {}).items():
            for i, s in enumerate(sil):
                mapa[(p, _base(w), i)] = (s, D.get(u"prefixo", u""), w)
        fok = os.path.join(RAIZ, p, u"silabas-ok.json")
        if os.path.exists(fok):
            try:
                okdec[p] = {k.upper() for k in json.load(io.open(fok, encoding=u"utf-8"))}
            except ValueError:
                okdec[p] = set()

    # medianas por tamanho vem dos BONS (e a base da relativa)
    bons = []            # (L, inicial, d, rotulo)
    for (p, wb, i), (s, pref, w) in mapa.items():
        if w.upper() in okdec.get(p, set()):
            continue
        f = os.path.join(RAIZ, p, u"audio", u"%ssb_%s_%d.mp3" % (pref, wb, i))
        if os.path.exists(f):
            bons.append((len(s), i == 0, librosa.get_duration(path=f), u"%s/%s[%d]=%s" % (p, w, i, s)))
    ruins = []
    for f in sorted(glob.glob(os.path.join(NEGATIVO, u"*.mp3"))):
        nome = os.path.basename(f)[:-4]
        pasta, arq = nome.split(u"__", 1)
        m = re.match(r"(\w+?)_sb_(\w+)_(\d+)$", arq)
        if not m:
            continue
        chave = (u"_" + pasta, m.group(2), int(m.group(3)))
        if chave not in mapa:
            continue
        s = mapa[chave][0]
        ruins.append((len(s), chave[2] == 0, librosa.get_duration(path=f), u"%s=%s" % (arq, s)))
    if not bons or not ruins:
        print(u"NAO MEDI: bons=%d soletrados=%d" % (len(bons), len(ruins)))
        return 2

    porTam = {}
    for L, ini, d, _ in bons:
        porTam.setdefault((L, ini), []).append(d)

    def julga(L, ini, d):
        u"""Devolve 'teto', 'relativa' ou None — a mesma logica do silabas.py
        (mediana por tamanho E posicao, desde 18/set/2026)."""
        if L in S.TETO_S and d > S.TETO_S[L]:
            return u"teto"
        if L == 1:
            return None
        base = S._mediana(porTam.get((L, ini), []))
        if base > 0 and len(porTam.get((L, ini), [])) >= 4 and d > base * S.FATOR:
            return u"relativa"
        return None

    peg_teto = sum(1 for L, ini, d, _ in ruins if julga(L, ini, d) == u"teto")
    peg_rel = sum(1 for L, ini, d, _ in ruins if julga(L, ini, d) == u"relativa")
    peg_qq = sum(1 for L, ini, d, _ in ruins if julga(L, ini, d))
    falsos = [(r, julga(L, ini, d)) for L, ini, d, r in bons if julga(L, ini, d)]

    print(u"bateria da soletracao: %d soletrados guardados x %d recortes bons"
          % (len(ruins), len(bons)))
    print(u"   teto absoluto  pegou %d/%d" % (peg_teto, len(ruins)))
    print(u"   relativa %.1fx pegou %d/%d (dos que o teto deixou passar)"
          % (S.FATOR, peg_rel, len(ruins)))
    print(u"   as duas juntas pegam %d/%d · escapam %d (soletrados curtos, 0,32-0,46 s: "
          u"so uma comparacao com a versao anterior do MESMO recorte pegaria)"
          % (peg_qq, len(ruins), len(ruins) - peg_qq))
    print(u"   falsos (bons acusados): %d" % len(falsos))
    for r, por in falsos[:8]:
        print(u"      • %s (%s)" % (r, por))
    ruim = 0
    if peg_teto < MIN_TETO:
        ruim = 1
        print(u"   REPROVADO: o teto pegava >= %d quando foi aferido (18/set/2026) "
              u"e agora pega %d — a regua perdeu o faro (mudou voz, RATE ou teto?)"
              % (MIN_TETO, peg_teto))
    if len(falsos) > MAX_FALSOS:
        ruim = 1
        print(u"   REPROVADO: a regua acusa recorte BOM — portao que reprova inocente "
              u"e portao que se aprende a ignorar")
    if not ruim:
        print(u"   ✓ a regua mantem o faro")
    return ruim


if __name__ == u"__main__":
    sys.exit(main())
