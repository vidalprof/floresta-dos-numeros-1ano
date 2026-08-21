#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO ACOPLAMENTO — a gaveta de conteúdo sobrevive ao `dados` JSON?

Nasceu de uma família inteira de defeitos (ago/2026, lotes 2–3 do
`_padrao/ESQUELETO/PECAS-A-FECHAR.md`): 7 peças (calendario, camadas-mapa,
mapa-conceitual, teia-alimentar, criar-desafio, passo-a-passo, intruso)
travavam o jogador SÓ montadas. A raiz é sempre a mesma: uma gaveta de CONTEÚDO
(a que o esboço garbla e o `dadosExtra` injeta como JSON) guardava algo que não
sobrevive à viagem:

  (1) uma FUNÇÃO  (`monta:function(){...}`, um mapa de efeitos) → morre no
      JSON.stringify e vira `undefined` → "x is not a function".
  (2) uma CHAVE DE ACOPLAMENTO (`fora:"cenoura"`, `pede:["rios"]`, `a:"sol"`)
      que aponta para o `k` de OUTRO item → o esboço garbla o valor p/ «...»,
      a comparação `item.k === ref` nunca casa → 0 alvos, jogador preso em 0%.

O conserto de todas foi o mesmo: marcar a gaveta com `/*TECNICA*/` (o esboço
para de garblá-la e o `var` da própria peça, intacto, fica valendo).

Este portão pega os DOIS casos ANTES da criança:
  · FUNÇÃO em gaveta de conteúdo  → ERRO (reprova; é sempre defeito).
  · CHAVE de acoplamento garblável → AVISO (rodar o jogador montado; pode ser
    conteúdo legítimo que só precisa de `/*TECNICA*/`).

⚠️ só o JOGADOR montado prova de fato; este portão é o alerta barato e estático.
Uso:  python3 _qa/acoplamento.py         (todas as peças do pecas.json)
Sai 1 se alguma peça tem FUNÇÃO em gaveta de conteúdo; senão 0.
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PECAS = os.path.join(RAIZ, "_padrao", "pecas")
GAV = os.path.join(RAIZ, "_padrao", "ESQUELETO", "pecas.json")

# as chaves que o `marca()` do esboco NÃO garbla (ver esboco.py LIGACAO).
# valor guardado nelas sobrevive intacto — não é risco.
LIGACAO = set("k alvo sp i id ref para de".split())
# propriedades de EXIBIÇÃO: garblá-las é o certo (viram «...» p/ o professor).
# não são acoplamento, mesmo que o texto por acaso repita uma chave.
DISPLAY = set(("n nome selo enun voz dica dicas d d1 d2 d3 fecha p c e por "
               "palavra som txt label titulo sub s novo t hint aviso msg "
               "cta pergunta legenda").split())


def var_body(js, name):
    m = re.search(r"\bvar\s+" + re.escape(name) + r"\s*=", js)
    if not m:
        return ""
    i = js.index("=", m.start()) + 1
    depth = 0
    j = i
    instr = None
    while j < len(js):
        c = js[j]
        if instr:
            if c == instr and js[j - 1] != "\\":
                instr = None
        elif c in "\"'":
            instr = c
        elif c in "[{(":
            depth += 1
        elif c in "]})":
            depth -= 1
        elif c == ";" and depth == 0:
            break
        j += 1
    return js[i:j]


def confere(nome, info):
    path = os.path.join(PECAS, nome + ".html")
    if not os.path.exists(path):
        return [], []
    js = "".join(re.findall(r"<script>(.*?)</script>",
                            io.open(path, encoding="utf-8").read(), re.S))
    keys = set(re.findall(r'\bk\s*:\s*"([^"]+)"', js)) \
        | set(re.findall(r"\bk\s*:\s*'([^']+)'", js))
    principal = info.get("var")
    tec = set(info.get("tecnicas") or [])
    todas = info.get("gavetas") or []
    conteudo = [principal] + [v for v in todas if v != principal]
    conteudo = [v for v in conteudo if v and v not in tec]
    erros, avisos = [], []
    for g in conteudo:
        body = var_body(js, g)
        if re.search(r"\bfunction\b", body):
            erros.append((g, "function"))
            continue
        if not keys:
            continue
        # propriedade ESCALAR (string) cujo valor é a chave de OUTRO item,
        # fora das chaves protegidas e das de exibição.
        for prop, val in re.findall(r'(\w+)\s*:\s*"([^"]+)"', body):
            if prop in LIGACAO or prop in DISPLAY or prop == "k":
                continue
            if val in keys:
                avisos.append((g, prop, val))
                break
    return erros, avisos


def main():
    G = json.load(io.open(GAV, encoding="utf-8"))["gavetas"]
    n_err = 0
    linhas_err, linhas_avi = [], []
    for nome in sorted(G):
        erros, avisos = confere(nome, G[nome])
        for g, _ in erros:
            n_err += 1
            linhas_err.append(u"   ✗ %s: gaveta de conteúdo '%s' guarda uma "
                              u"FUNÇÃO — morre no dados JSON. Marque-a "
                              u"/*TECNICA*/." % (nome, g))
        for g, prop, val in avisos:
            linhas_avi.append(u"   · %s: '%s.%s' = \"%s\" aponta para a chave "
                              u"de um item — se garblar, o jogador trava. "
                              u"Rodar o jogador montado; se for config, "
                              u"/*TECNICA*/." % (nome, g, prop, val))
    print(u"PORTÃO DO ACOPLAMENTO — %d peça(s)" % len(G))
    if linhas_err:
        print(u"  %d ERRO(S) — função em gaveta de conteúdo:" % n_err)
        for ln in linhas_err:
            print(ln)
    if linhas_avi:
        print(u"  %d AVISO(S) — possível acoplamento (conferir no jogador):"
              % len(linhas_avi))
        for ln in linhas_avi:
            print(ln)
    if not n_err:
        print(u"  ok: nenhuma FUNÇÃO em gaveta de conteúdo "
              u"(os avisos, se houver, são só p/ conferir no jogador).")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
