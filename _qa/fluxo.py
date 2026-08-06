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


CORPOS = {}


def sem_comentarios(s):
    """Troca os comentarios por espacos, mantendo o TAMANHO e os textos entre
    aspas. Sem isto, um comentario que CITA outra tela vira caminho de verdade.

    ⚠️ LICAO PAGA (ago/2026, Maquina do Tempo): eu escrevi, num comentario logo
    abaixo do hFim, a frase "as chamadas soltas (hCaca(), mostraBanner(...,hFim))
    pegam o envelope sozinhas" — explicando o gancho da retomada. O portao leu
    aquilo como codigo, achou que hFim chamava hFim e reprovou a atividade
    inteira por "TELA PRESA". Alarme falso manda consertar o que nao esta
    quebrado, e custa tanto quanto defeito passado.
    """
    fora, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            j = n if j < 0 else j + 2
            fora.append(" " * (j - i))
            i = j
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            j = s.find("\n", i)
            j = n if j < 0 else j
            fora.append(" " * (j - i))
            i = j
            continue
        if c in "\"'":
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == c or s[j] == "\n":
                    break
                j += 1
            fora.append(s[i:j + 1])
            i = j + 1
            continue
        fora.append(c)
        i += 1
    return "".join(fora)


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
        CORPOS[nome] = corpo
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
    html = sem_comentarios(io.open(caminho, encoding="utf-8").read())
    saidas = telas_e_saidas(html)
    corpos = CORPOS

    problemas = []

    # telaPainel se redesenha de proposito (imprimir/voltar) -> nao e "presa"
    presas = sorted(n for n, al in saidas.items() if n in al and n != "telaPainel"
                    and re.search(r"\blimpa\(\)", corpos.get(n, "")))
    for n in presas:
        problemas.append("TELA PRESA: %s leva de volta para ela mesma" % n)

    extras = mesa_de_paradas(html, list(saidas))
    vistas = alcancaveis(saidas, list(raizes) + sorted(extras))
    # telaPainel abre pelo ?painel; *Base sao helpers, nao telas
    ignorar = set(n for n in saidas if n.endswith("Base")) | {"telaPainel", "telaPainelPin"}  # abrem pelo ?painel, nao pelo fluxo
    # TELA = funcao que chama limpa() (limpa a area e desenha).
    # Detectar pelo COMPORTAMENTO e nao pelo nome: os prefixos mudam de app
    # para app (vXxx, gXxx, nXxx, telaXxx) e um regex de nome deixa telas de
    # fora em silencio -- foi o que aconteceu com a "Legenda do Pingo".
    so_telas = set(n for n in saidas if re.search(r"\blimpa\(\)", corpos.get(n, "")))
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
