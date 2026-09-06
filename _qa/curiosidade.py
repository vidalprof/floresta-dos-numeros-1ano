#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA CURIOSIDADE — a atividade abre a lacuna antes de explicar?

De onde veio: `_pesquisa/REGRAS-NEUROCIENCIA.md`, tabela "O QUE DÁ PARA MEDIR
SOZINHO", itens 10, 11 e 12, e o Portão 0 do `EDUVERSE-FILOSOFIA.md` ("o
problema vem primeiro e o conceito por ÚLTIMO"). Pedido do Marcos (set/2026):
*"faça tudo que pedi para deixar tudo mais rápido, moderno, ágil, por isso você
fez as pesquisas"*.

Lê o `FASES = [...]` que o montador escreve no index.html.

O que ele REPROVA (código 1):
  R11 o CONCEITO vem antes do problema: a 1ª fase abre com definição ("X é...",
      "Lembre-se:", "Regra:", "significa") em vez de com uma falta concreta.
  R10 a 1ª fase é tela de leitura (mecânica passiva) — a criança tem que TOCAR
      em algo nas duas primeiras telas.

O que ele AVISA:
  R10b enunciado longo nas duas primeiras fases (> 160 caracteres de texto):
       carga cognitiva na abertura, quando a lacuna ainda nem abriu;
  R12  a última fase que conta (fora do respiro: pintar/vitrine/criar) é só
       figural — a escada CPA pede fechar no SIMBÓLICO.

Códigos: 0 passou · 1 REPROVOU · 2 não se aplica (não é atividade montada).
Uso: python3 _qa/curiosidade.py <pasta>/index.html
"""
import io
import json
import re
import sys

PASSIVAS = set(["passo-a-passo"])
RESPIRO = set(["pintar", "pintar-canvas", "pintar-desenho", "criar-desafio", "vitrine"])
FIGURAIS = set(["memoria", "arrastar-sombra", "quebra-cabeca", "tangram", "achar-na-cena",
                "sombra", "ligar-pontos", "sete-erros", "labirinto", "tracar-caminho",
                "andar-ate", "simetria", "girar"])
DEFINICAO = re.compile(
    u"^\\s*(<b>)?\\s*(o|a|os|as|um|uma)\\s+[\\wçãõáéíóúâêô-]+\\s*(</b>)?\\s+(é|são|significa|quer dizer|serve para)\\b"
    u"|\\b(lembre-se|lembrem-se|regra|definição|conceito)\\s*:", re.I)


def _texto(s):
    return re.sub(r"<[^>]+>", "", s or u"")


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/curiosidade.py <index.html>")
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8", errors="replace").read()
    m = re.search(r"\nFASES = (\[.*?\]);", html, re.S)
    if not m:
        print(u"%s -> nao se aplica (nao e atividade montada: sem FASES)" % alvo)
        return 2
    try:
        fases = json.loads(m.group(1))
    except Exception as e:
        print(u"%s -> NAO MEDI: FASES nao e JSON (%s)" % (alvo, e))
        return 2
    if not fases:
        print(u"%s -> nao se aplica (FASES vazio)" % alvo)
        return 2

    ruins, avisos = [], []

    # R10 — a criança faz algo nas duas primeiras telas
    for i, f in enumerate(fases[:2]):
        if (f.get("mec") or "") in PASSIVAS:
            ruins.append(u"R10 fase %d (%s) e de leitura/observacao (%s): a abertura precisa de um "
                         u"gesto da crianca, nao de uma tela para ler" % (i + 1, f.get("id") or "?", f.get("mec")))
        txt = _texto(f.get("enunciado"))
        if len(txt) > 160:
            avisos.append(u"R10b fase %d (%s): enunciado com %d caracteres na abertura — uma ideia "
                          u"por tela, a lacuna ainda nem abriu" % (i + 1, f.get("id") or "?", len(txt)))

    # R11 — o conceito por último
    f0 = fases[0]
    txt0 = (f0.get("enunciado") or u"") + u" " + (f0.get("selo") or u"")
    if DEFINICAO.search(txt0) or DEFINICAO.search(_texto(f0.get("enunciado"))):
        ruins.append(u"R11 a 1a fase (%s) abre com DEFINICAO (\"%s\"): o problema vem primeiro, "
                     u"o conceito por ultimo (Portao 0)" % (f0.get("id") or "?", _texto(f0.get("enunciado"))[:70]))

    # R12 — a última fase que conta fecha no simbólico
    ult = None
    for f in reversed(fases):
        if (f.get("mec") or "") not in RESPIRO and not f.get("aquecimento"):
            ult = f
            break
    if ult is not None:
        mec = ult.get("mec") or ""
        figural = mec in FIGURAIS
        if mec == "escolher" or mec == "intruso":
            dados = ult.get("dados") or []
            opts = []
            for d in dados if isinstance(dados, list) else []:
                for o in (d.get("opts") or d.get("opcoes") or []) if isinstance(d, dict) else []:
                    opts.append(o)
            if opts and all(isinstance(o, dict) and o.get("img") and not _texto(o.get("t") or o.get("txt") or o.get("texto")).strip() for o in opts):
                figural = True
        if figural:
            avisos.append(u"R12 a ultima fase que conta (%s, %s) e FIGURAL: a escada concreto -> "
                          u"figural -> simbolico pede fechar no simbolico (numero, palavra, frase)"
                          % (ult.get("id") or "?", mec))

    print(u"%s -> curiosidade: %d fase(s) lidas, %d reprova(s), %d aviso(s)"
          % (alvo, len(fases), len(ruins), len(avisos)))
    for a in avisos:
        print(u"   aviso: %s" % a)
    if ruins:
        for r in ruins:
            print(u"   - %s" % r)
        return 1
    print(u"   lacuna ok: gesto nas duas primeiras telas, nenhuma definicao antes do problema")
    return 0


if __name__ == "__main__":
    sys.exit(main())
