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
    """Remove os blocos @media (inclusive com regras aninhadas).

    ⚠️ Tirar os COMENTARIOS antes e obrigatorio. Ja aconteceu (ago/2026, na
    Maquina do Tempo): um comentario de CSS terminava com a palavra "@media",
    o regex daqui achou que aquilo era o comeco de um bloco e engoliu a regra
    logo abaixo dele — o portao acusou ".forca sem estilo" com a regra bem ali,
    escrita. Alarme falso custa tanto quanto defeito passado: manda consertar
    o que nao esta quebrado.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
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
    # ⚠️ classe passada como ARGUMENTO de funcao (cenaImg(nome,"jimg"),
    #    imgEl(nome,"pecaimg")). O portao so olhava el(...) e className= — e
    #    deixou passar a .jimg sem regra: a figura do mapa vinha no tamanho
    #    natural e a fase ficava com 1900px de altura.
    #    (cenaEl fica de fora: o 2o argumento dela e a LEGENDA, nao a classe)
    for m in re.finditer(r'(?:cenaImg|imgEl)\(\s*[^,()]+,\s*"([a-z][\w \-]*)"', js):
        for c in m.group(1).split():
            usadas.setdefault(c, 0)
    # ⚠️ NAO BASTA `className = "..."`. A classe tambem chega por TERNARIO
    #    (`q.className = tem ? "cquad" : "cquad mark"`) e por CONCATENACAO
    #    (`"cquad ok "+cor`). Foi assim que `.mark` e `.ok` do caca-palavras
    #    passaram sem CSS nenhum: a crianca tocava na letra e a tela nao
    #    respondia NADA, e a palavra achada nao acendia. O portao existia e
    #    olhou para o outro lado. Agora ele le a INSTRUCAO INTEIRA, ate o `;`,
    #    e recolhe todo texto entre aspas que aparecer ali.
    for m in re.finditer(r'className\s*=', js):
        trecho = js[m.end():m.end() + 200].split(";")[0].split("\n")[0]
        # ⚠️ FALSO ALARME PAGO (ago/2026): a instrucao
        #    `x.className = (x.getAttribute("data-qa")==="1") ? "a" : "b"`
        #    fazia o portao ler `"data-qa"` como se fosse nome de classe e
        #    acusar `SEM CSS: .data-qa`. O texto entre aspas que esta DENTRO de
        #    uma chamada de funcao (getAttribute, indexOf, split...) nao e
        #    classe: e argumento. Some com esses antes de recolher.
        trecho = re.sub(r'\.\s*\w+\s*\([^)]*\)', ' ', trecho)
        for lit in re.findall(r'"([^"]*)"', trecho):
            for c in lit.split():
                usadas.setdefault(c, 0)
    for m in re.finditer(r'class="([^"]+)"', js):
        for c in m.group(1).split():
            usadas.setdefault(c, 0)

    # as camadas do mascote ("lay base" / "lay fala" / "lay pisca") sao
    # estilizadas pela classe .lay; o nome da pose e so um seletor de JS.
    for c in ("base", "fala", "pisca"):
        usadas.pop(c, None)

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
