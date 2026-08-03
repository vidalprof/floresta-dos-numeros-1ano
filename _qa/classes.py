#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere as CLASSES CSS de uma atividade (1 HTML autossuficiente).

Pega dois erros que ja custaram caro:

  1) CLASSE SEM REGRA BASE -> a classe so aparece dentro de um @media.
     Na tela normal o elemento fica SEM ESTILO. Foi o caso do `.pchip`
     (a lista do caca-palavras virou texto solto) e antes do `.txcard`.
     Procurar a classe no CSS inteiro da FALSO NEGATIVO: e preciso apagar
     os blocos @media antes de procurar.

  2) COLISAO COM O MOTOR -> a classe nova tem o mesmo nome de uma classe
     que o motor ja usa em outro lugar. Foi o caso do `.base` (fabrica de
     adjetivos) que pintou de verde a camada `lay base` do mascote.

Uso:  python3 _qa/classes.py _nomes/index.html
Sai com 1 se achar problema.
"""
import io
import re
import sys


def sem_media(css):
    """Remove os blocos @media (inclusive com regras aninhadas)."""
    return re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css, flags=re.S)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    h = io.open(sys.argv[1], encoding="utf-8").read()
    js = "\n".join(re.findall(r"<script>(.*?)</script>", h, re.S))
    css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
    base = sem_media(css)

    usadas = {}
    for m in re.finditer(r'el\("[a-z0-9]+","([^"]+)"', js):
        for c in m.group(1).split():
            usadas.setdefault(c, 0)
    for m in re.finditer(r'className\s*=\s*"([^"]+)"', js):
        for c in m.group(1).split():
            usadas.setdefault(c, 0)
    for m in re.finditer(r'class="([^"]+)"', js):
        for c in m.group(1).split():
            usadas.setdefault(c, 0)

    # descarta pedacos de template ("vida'+(k<vidas?...") que nao sao classe.
    # Tambem descarta nome de 1-2 letras: vem de concatenacao ("moeda m"+valor
    # -> o pedaco "m"), nunca de uma classe de verdade. Falso positivo pago.
    usadas = {c: v for c, v in usadas.items()
              if len(c) > 2 and re.match(r"^[a-zA-Z][-a-zA-Z0-9_]*$", c)}

    problemas = []
    for c in sorted(usadas):
        tem_base = re.search(r"\.%s[\s,{:.]" % re.escape(c), base) is not None
        tem_media = re.search(r"\.%s[\s,{:.]" % re.escape(c), css) is not None
        if not tem_base:
            if tem_media:
                problemas.append("SO DENTRO DE @media: .%s (fica sem estilo na tela normal)" % c)
            else:
                problemas.append("SEM CSS: .%s" % c)

    print("%s -> %d classes usadas no JS" % (sys.argv[1], len(usadas)))
    for p in problemas:
        print("  !! " + p)
    if not problemas:
        print("  classes ok: todas tem regra base")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
