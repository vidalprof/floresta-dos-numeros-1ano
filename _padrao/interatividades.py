#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Gera o `_padrao/INTERATIVIDADES.md` a partir do que EXISTE — não da memória.

O arquivo dizia "gerado a partir das atividades reais", mas não havia gerador:
era mantido à mão e envelhecia (dizia 84 peças quando havia 88; contava a
`_agora` como atividade). Agora ele nasce daqui:
  · as peças = `_padrao/pecas/*.html` (menos o MOLDE);
  · "em quantas atividades" = os `_*/conteudo.json` das atividades montadas
    (as pastas que o `_qa/pastas.py` não considera atividade ficam fora);
  · o gesto (toque/arrastar) = o censo do código da peça;
  · a coluna "bancada" = o último resultado de `bash _qa/peca.sh` guardado em
    `_padrao/_bancada.json` (quem roda o lote inteiro atualiza esse arquivo).

Uso:  python3 _padrao/interatividades.py            (escreve o .md)
      python3 _padrao/interatividades.py --bancada <RESUMO.txt>   (importa o lote)
"""
import glob
import io
import json
import os
import re
import sys
import time
import collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PECAS = os.path.join(RAIZ, "_padrao", "pecas")
SAIDA = os.path.join(RAIZ, "_padrao", "INTERATIVIDADES.md")
BANCADA = os.path.join(RAIZ, "_padrao", "_bancada.json")
NAO_ATIVIDADE = {u"_cobaia", u"_colecao", u"_agora", u"_novo", u"_padrao", u"_qa",
                 u"_site", u"_status", u"_pesquisa", u"_painel", u"_banco"}


def pecas():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(PECAS, "*.html"))
                  if not p.endswith("MOLDE.html"))


def gesto(nome):
    h = io.open(os.path.join(PECAS, nome + ".html"), encoding="utf-8").read()
    sc = re.findall(r"<script[^>]*>(.*?)</script>", h, re.S)
    js = sc[1] if len(sc) > 1 else (sc[0] if sc else u"")
    if re.search(r"touchmove|pointermove|mousemove", js):
        return u"arrastar"
    if re.search(r"onkeydown|keydown", js):
        return u"toque + teclado"
    return u"toque"


def uso():
    onde = collections.defaultdict(set)
    for cj in glob.glob(os.path.join(RAIZ, "_*", "conteudo.json")):
        pasta = os.path.basename(os.path.dirname(cj))
        if pasta in NAO_ATIVIDADE:
            continue
        try:
            d = json.load(io.open(cj, encoding="utf-8"))
        except Exception:
            continue
        for f in d.get("fases", d if isinstance(d, list) else []):
            if isinstance(f, dict) and f.get("mec"):
                onde[f["mec"]].add(pasta.lstrip(u"_"))
    return onde


def importa_bancada(resumo):
    d = {}
    for l in io.open(resumo, encoding="utf-8"):
        m = re.match(r"(\S+)\s+rc=(\d+)\s+(PECA PRONTA|PECA REPROVADA|TEMPO ESGOTADO[^\d]*|SEM VEREDITO)\s+(\d+)s", l)
        if m:
            d[m.group(1)] = {u"veredito": m.group(3).strip(), u"segundos": int(m.group(4))}
    io.open(BANCADA, "w", encoding="utf-8").write(json.dumps(
        {u"quando": time.strftime("%Y-%m-%d"), u"pecas": d}, ensure_ascii=False, indent=1))
    print(u"bancada importada: %d peca(s) -> %s" % (len(d), BANCADA))


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--bancada":
        importa_bancada(sys.argv[2])
    ps = pecas()
    onde = uso()
    banc = {}
    if os.path.exists(BANCADA):
        banc = json.load(io.open(BANCADA, encoding="utf-8"))
    bp = banc.get(u"pecas", {})

    def selo(n):
        v = bp.get(n, {}).get(u"veredito")
        if not v:
            return u"—"
        return u"✅" if v == u"PECA PRONTA" else u"⛔ " + v

    prontas = [n for n in ps if onde.get(n)]
    lapidar = [n for n in ps if not onde.get(n)]
    prontas.sort(key=lambda n: (-len(onde[n]), n))

    L = []
    L.append(u"# 🎛️ INTERATIVIDADES — o que JÁ FUNCIONA (clone daqui) × o que falta lapidar")
    L.append(u"")
    L.append(u"> **⭐ LEIA ANTES DE MONTAR UMA ATIVIDADE.** Cada interatividade (mecânica do")
    L.append(u"> motor) tem aqui **de qual atividade real clonar a versão que já funciona** — para")
    L.append(u"> COPIAR, não reescrever (regra do Marcos, set/2026: *\"não redesenhar, temos várias")
    L.append(u"> atividades boas, copiar a interatividade pronta\"*). As armadilhas de cada uma e a")
    L.append(u"> versão mais corrigida ficam no `_padrao/DINAMICAS.md`; aqui é o ÍNDICE rápido.")
    L.append(u">")
    L.append(u"> **Este arquivo é GERADO** por `python3 _padrao/interatividades.py` — não editar à")
    L.append(u"> mão (envelhece). Peça nova, atividade nova ou lote novo da bancada → rodar de novo.")
    L.append(u"")
    L.append(u"Gerado em %s a partir das peças (`_padrao/pecas/`), das atividades reais (`_*/conteudo.json`)"
             % time.strftime("%Y-%m-%d"))
    if banc:
        L.append(u"e da bancada da peça (`bash _qa/peca.sh`, lote de %s: coluna **bancada**)." % banc.get(u"quando"))
    L.append(u"")
    L.append(u"## ✅ PRONTAS — provadas em atividade (clone da atividade indicada)")
    L.append(u"")
    L.append(u"| Interatividade | Gesto | Em quantas | Clonar de (atividades que já usam) | bancada |")
    L.append(u"|---|---|---:|---|:-:|")
    for n in prontas:
        ats = sorted(onde[n])
        txt = u", ".join(ats[:8]) + (u" …" if len(ats) > 8 else u"")
        L.append(u"| **%s** | %s | %d | %s | %s |" % (n, gesto(n), len(ats), txt, selo(n)))
    L.append(u"")
    L.append(u"## 🛠️ FALTAM LAPIDAR — existem no motor, ainda NÃO usadas numa atividade")
    L.append(u"")
    L.append(u"_Estas %d peças existem em `_padrao/pecas/` e no `pecas.js` mas nunca entraram numa"
             u" atividade publicada. Passaram na cobaia (todas as 88 rodam dentro do motor) e na"
             u" bancada da peça (coluna), mas \"provada em jogo\" só quando o Marcos aprovar numa"
             u" atividade. Ao usar uma, ela sobe para a tabela de cima sozinha (rodar o gerador)._"
             % len(lapidar))
    L.append(u"")
    L.append(u"| Interatividade | Gesto | bancada |")
    L.append(u"|---|---|:-:|")
    for n in lapidar:
        L.append(u"| `%s` | %s | %s |" % (n, gesto(n), selo(n)))
    L.append(u"")
    L.append(u"## 📊 Resumo")
    L.append(u"")
    L.append(u"- Banco do motor: **%d** interatividades (a cobaia `_cobaia` roda as %d)." % (len(ps), len(ps)))
    L.append(u"- **Prontas (provadas em atividade): %d.**" % len(prontas))
    L.append(u"- Faltam lapidar: **%d.**" % len(lapidar))
    if bp:
        ok = sum(1 for n in ps if bp.get(n, {}).get(u"veredito") == u"PECA PRONTA")
        L.append(u"- Bancada da peça (`_qa/peca.sh`, 9 portões + toque medido): **%d de %d PRONTAS**%s."
                 % (ok, len(ps), u"" if ok == len(ps) else u" — ver coluna"))
    L.append(u"")
    L.append(u"> Fonte de armadilhas e detalhes por mecânica: `_padrao/DINAMICAS.md`.")
    L.append(u"> Catálogo das atividades (com links): `ATIVIDADES.md`.")
    io.open(SAIDA, "w", encoding="utf-8").write(u"\n".join(L) + u"\n")
    print(u"escrito: %s (%d pecas: %d prontas, %d a lapidar)" % (SAIDA, len(ps), len(prontas), len(lapidar)))


if __name__ == "__main__":
    main()
