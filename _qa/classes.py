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
import os
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


def recolhe(usadas, txt):
    u"""Recolhe nomes de classe dos literais de `txt` (uma EXPRESSAO de classe).

    ⚠️ LITERAL QUE TERMINA COLADO NUM `+` E PREFIXO, NAO CLASSE — e este foi o
       falso alarme que apareceu quando o portao passou a ler o `folhas.js`
       (20/set/2026). Em `el("button", "op curta lapiz marca" + m[0], ...)` as
       classes de verdade sao `marcaA` e `marcaB`; o pedaco `marca` sozinho nao
       existe em CSS nenhum, e o portao mandava escrever uma regra para ele. O
       mesmo em `"lente foco" + Math.min(focos,3)` (as reais sao `foco1..3`).
       Quatro dos seis cadernos acusados eram so isto.

    ⚠️ MAS NEM TODO `+` COLA: em `"cruz uma" + (aceita ? " livre" : "")` o que
       vem depois COMECA COM ESPACO, entao `uma` e classe inteira e `livre`
       tambem. A regra que separa os dois casos e olhar o PROXIMO literal: se
       ele comeca com espaco (ou esta vazio), o pedaco anterior esta fechado.
       Sem isto o portao perderia `.cruz.livre` — que era um buraco de verdade,
       herdado do clone da cruzadinha.
    """
    lits = [(m.group(1), m.end()) for m in re.finditer(r'"([^"]*)"', txt)]
    for i, (lit, fim) in enumerate(lits):
        partes = lit.split()
        if partes and not lit.endswith(" "):
            resto = txt[fim:].lstrip()
            if resto.startswith("+"):
                # ⚠️ SÓ CONTINUA A PALAVRA SE O QUE VEM DEPOIS DO `+` FOR OUTRO
                #    LITERAL, coladinho. Com uma VARIÁVEL no meio —
                #    `"... lapiz marca" + m[0] + " marcada"` — o pedaço `marca`
                #    É prefixo (as classes reais são `marcaA`, `marcaB`), e olhar
                #    só "o próximo literal do trecho" fazia o portão achar o
                #    `" marcada"` lá adiante, ver o espaço e manter `marca`.
                #    Foi assim que `.marca` apareceu como classe sem CSS no
                #    `_ing8` e no `_subst5` (20/set/2026).
                dep = resto[1:].lstrip()
                colado = not (dep.startswith('"') and
                              (dep[1:2] == " " or dep[1:2] == '"'))
                if colado:
                    partes = partes[:-1]
        for c in partes:
            usadas.setdefault(c, 0)


def arg2(js, i):
    u"""Devolve o SEGUNDO ARGUMENTO de uma chamada, a partir da posicao `i`.

    ⚠️ Janela de N caracteres nao serve. Na primeira tentativa eu li 24 letras
       depois do literal e a janela entrava na chamada SEGUINTE — o portao
       recolheu `div` (o nome da tag do `el("div", ...)` de baixo) e mandou
       escrever `.div` no CSS. Aqui o argumento e lido de verdade: conta
       parenteses e colchetes e para na virgula de nivel zero.
    """
    d, ini, n = 0, i, len(js)
    while i < n:
        c = js[i]
        if c in '"\'':
            i += 1
            while i < n and js[i] != c:
                i += 2 if js[i] == "\\" else 1
        elif c in "([{":
            d += 1
        elif c in ")]}":
            if d == 0:
                return js[ini:i]
            d -= 1
        elif c == "," and d == 0:
            return js[ini:i]
        elif c in ";\n" and d == 0:
            return js[ini:i]
        i += 1
    return js[ini:i]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    h = io.open(sys.argv[1], encoding="utf-8").read()
    js = "\n".join(re.findall(r"<script>(.*?)</script>", h, re.S))
    # ⚠️ O JS DE FORA DO HTML TAMBEM CONTA — e esta linha custou caro
    #    (20/set/2026). Em CADERNO DE FOLHA VIVA metade do codigo mora no
    #    `folhas.js` ao lado do index, carregado por <script src="folhas.js">.
    #    O portao lia so o que estava DENTRO das tags e anunciava, todo
    #    contente, "4 classes usadas no JS, todas tem regra" — enquanto o
    #    `_corpo5` tinha DOZE classes sem uma linha de CSS: a grade inteira do
    #    caca-palavras de duas folhas, os alvos de outra, a caixa do orgao (que
    #    sem regra mostrava a figura do estomago com os 454 px do arquivo
    #    dentro do item). Portao que le metade do codigo aprova por ignorancia.
    aqui = os.path.dirname(os.path.abspath(sys.argv[1]))
    for src in re.findall(r'<script[^>]+src="([^"?]+\.js)', h):
        if src.startswith("http") or src.startswith("/"):
            continue
        cam = os.path.join(aqui, src)
        if os.path.exists(cam):
            js += "\n" + io.open(cam, encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
    base = sem_media(css)

    usadas = {}
    # ⚠️ COM ESPAÇO DEPOIS DA VÍRGULA TAMBÉM. O regex antigo exigia `el("div","x"`
    #    coladinho, e em caderno de folha viva o estilo da casa é `el("div", "x")`
    #    — o portão simplesmente não via essas classes.
    for m in re.finditer(r'el\(\s*"[a-z0-9]+"\s*,\s*(?=")', js):
        recolhe(usadas, arg2(js, m.end()))
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
        # ⚠️ SEGUNDO FALSO ALARME DA MESMA FAMILIA (set/2026, Bancada da Divisao):
        #    `elGrupos.className = "grupos" + (fase==="repartir" ? " alvo" : "")`
        #    fazia o portao ler `"repartir"` como nome de classe e acusar
        #    `SEM CSS: .repartir` — mas "repartir" e o valor de uma VARIAVEL DE
        #    ESTADO, comparada ali para decidir a classe. O que esta do lado
        #    direito de uma COMPARACAO nunca e classe: e o valor comparado.
        #    Some com eles antes de recolher (o mesmo remedio do `getAttribute`).
        trecho = re.sub(r'[=!]==?\s*"[^"]*"', ' ', trecho)
        recolhe(usadas, trecho)
    # ⚠️ `class="..."` DENTRO DE UM TEXTO MONTADO não acaba na aspa: em
    #    `'<span class="lt' + (pos < meio ? " q" : "") + '">'` o que vem depois
    #    do `lt` é CÓDIGO, não classe. O portão lia a expressão inteira e
    #    recolhia `meio` (uma variável de contagem) como se fosse classe — e
    #    acusava `.meio` sem CSS no `_sinon2` (20/set/2026). Corta no primeiro
    #    sinal de que o literal acabou.
    for m in re.finditer(r'class=[\\]?"([^"\\]+)', js):
        lit = re.split(r"['+<>?{}]", m.group(1))[0]
        for c in lit.split():
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
