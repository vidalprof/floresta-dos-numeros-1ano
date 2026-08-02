#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere o FLUXO de telas de uma atividade (1 HTML autossuficiente).

Pega dois erros que o auditor de sobreposicao NAO pega, porque ele so
olha cada tela isolada:

  1) TELA QUE VOLTA PRA SI MESMA  -> a crianca fica presa, repetindo a
     mesma fase para sempre. (Foi o que aconteceu no gLigar, agosto/2026:
     `mostraBanner(..., gLigar)` em vez de `gBanca`.)
  2) TELA ORFA -> existe no codigo mas ninguem chega nela. Era o caso de
     gBanca, gAquec, gTrocado, gMonta, gEnsinar e gFim: a missao inteira
     de Generos estava inalcancavel depois do gLigar.

Uso:
    python3 _qa/fluxo.py _redacao/index.html gAbertura vAbertura
    python3 _qa/fluxo.py _jardim/index.html telaCapa

Sai com codigo 1 se achar problema (da para usar em workflow).
"""
import io
import re
import sys


def telas_e_saidas(html):
    """Devolve {nome_da_tela: set(telas para onde ela leva)}."""
    marcas = [(m.group(1), m.start()) for m in re.finditer(r"\nfunction ([A-Za-z_]\w*)\(", html)]
    marcas.append(("__fim__", len(html)))
    # TODAS as funcoes viram no do grafo: uma tela pode ser chamada de dentro
    # de um ajudante (ex.: `function avancar(){ ... telaFinal(); }`) e sem isso
    # ela pareceria orfa sem estar.
    todas = [n for n, _ in marcas if n != "__fim__"]
    nomes = todas
    saidas = {}
    for i in range(len(marcas) - 1):
        nome, ini = marcas[i]
        if nome not in nomes:
            continue
        corpo = html[ini:marcas[i + 1][1]]
        corpo = corpo[corpo.find("{"):]
        alvos = set()
        for t in nomes:
            if t == nome:
                continue
            # qualquer mencao ao nome da outra tela conta como caminho:
            # t(), setTimeout(t,900), mostraBanner("...",t), prox:t ...
            if re.search(r"\b%s\b" % t, corpo):
                alvos.add(t)
        # auto-referencia so conta se for chamada/callback de verdade
        if re.search(r"\b%s\(\)" % nome, corpo) or re.search(r",\s*%s\s*\)" % nome, corpo):
            alvos.add(nome)
        saidas[nome] = alvos
    return saidas


def mesa_de_paradas(html, nomes):
    """Telas chamadas de dentro de uma TABELA de paradas (ex.: a Fabrica de
    Estrelas usa `{id:..., fn:function(){telaSoma();}}`). Elas nao aparecem
    no corpo de outra tela, entao entram aqui como alcancaveis."""
    fora = set()
    for m in re.finditer(r"fn\s*:\s*function\s*\(\)\s*\{(.*?)\}", html, re.S):
        for t in nomes:
            if re.search(r"\b%s\b" % t, m.group(1)):
                fora.add(t)
    return fora


def alcancaveis(saidas, raizes):
    vistas, pilha = set(), list(raizes)
    while pilha:
        x = pilha.pop()
        if x in vistas:
            continue
        vistas.add(x)
        pilha.extend(saidas.get(x, ()))
    return vistas


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    caminho, raizes = sys.argv[1], sys.argv[2:]
    html = io.open(caminho, encoding="utf-8").read()
    saidas = telas_e_saidas(html)

    problemas = []

    # telaPainel se redesenha de proposito (imprimir/voltar) -> nao e "presa"
    presas = sorted(n for n, al in saidas.items() if n in al and n != "telaPainel"
                    and re.match(r"^(v[A-Z]|g[A-Z]|tela)", n))
    for n in presas:
        problemas.append("TELA PRESA: %s leva de volta para ela mesma" % n)

    extras = mesa_de_paradas(html, list(saidas))
    vistas = alcancaveis(saidas, list(raizes) + sorted(extras))
    # telaPainel abre pelo ?painel; *Base sao helpers, nao telas
    ignorar = set(n for n in saidas if n.endswith("Base")) | {"telaPainel", "telaPainelPin"}  # abrem pelo ?painel, nao pelo fluxo
    so_telas = set(n for n in saidas if re.match(r"^(v[A-Z]|g[A-Z]|tela)", n))
    orfas = sorted(so_telas - vistas - ignorar)
    for n in orfas:
        problemas.append("TELA ORFA: ninguem chega em %s" % n)

    print("%s -> %d telas, %d alcancaveis a partir de %s"
          % (caminho, len(so_telas), len(so_telas & vistas), ", ".join(raizes)))
    for p in problemas:
        print("  !! " + p)
    if not problemas:
        print("  fluxo ok: nenhuma tela presa, nenhuma orfa")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
