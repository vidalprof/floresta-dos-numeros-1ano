# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "cor de texto cravada na peça briga com o tema"

 ⚠️ LIÇÃO PAGA (ago/2026), e ela me mordeu DUAS VEZES no mesmo dia, o que é o
 sinal de que faltava portão e não faltava cuidado.

 A dica da peça `digitar` era clara (`#f4efe6`). Na Padaria, cujo tema é claro,
 ela dava 2,56:1 — invisível. Escureci para `#241d12` e a Padaria passou.
 Horas depois, na Central, cujo tema é ESCURO, a mesma dica dava 1,06:1 — de
 novo invisível, agora pelo outro lado.

 **Não existe cor fixa certa.** A peça não sabe em que atividade vai cair, e as
 atividades da casa vão do azul-céu ao galpão à noite. Quem sabe a cor é o TEMA.

 A REGRA, e ela é fina: cor cravada não é proibida — é proibida quando o
 elemento **não pinta o próprio fundo**. Um `.opt` creme com tinta escura está
 certo: ele carrega a mesa dele junto. Um `.hint` com tinta clara e sem fundo
 nenhum herda o fundo da atividade, e aí é loteria.

 O QUE ESTE PORTÃO FAZ: procura, no CSS da peça, regras que definem `color:`
 num tom extremo (quase branco ou quase preto) **sem** definir `background` na
 mesma regra. Essas são as que brigam com o tema. O conserto é `var(--texto)`,
 o token que o motor define e cada atividade redefine.

 ⚠️ O que ele NÃO faz: medir contraste. Isso é do `_qa/contraste.js`, que roda
 no navegador e mede o pixel. Este aqui é o aviso BARATO, na peça, antes de ela
 entrar em qualquer atividade — pega a causa, não o sintoma.

 Uso: python3 _qa/cor_fixa.py <peca.html>
============================================================
"""
import io
import re
import sys

# um tom é "extremo" quando quase não sobra margem para o outro lado: texto
# assim só funciona sobre um fundo do lado oposto, e a peça não escolhe o fundo.
CLARO, ESCURO = 200, 70


def luz(cor):
    u"""luminância grosseira de um #rgb ou #rrggbb (0 a 255)."""
    c = cor.lstrip("#")
    if len(c) == 3:
        c = "".join(x * 2 for x in c)
    if len(c) != 6:
        return None
    try:
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    except ValueError:
        return None
    return 0.299 * r + 0.587 * g + 0.114 * b, max(r, g, b) - min(r, g, b)


_KF = re.compile(r"@(?:-webkit-|-moz-|-o-)?keyframes\s+[\w-]+\s*\{", re.I)


def sem_keyframes(css):
    u"""tira os blocos de animacao INTEIROS antes de ler as regras.

    ⚠️ ULTIMO FALSO DESTE PORTAO, e da mesma familia do defeito que engoliu as
    animacoes no integrador: dentro de um `@keyframes`, `from` e `to` NAO sao
    seletores — sao marcos de tempo. O portao leu `to{color:#fff8e2}` como se
    fosse um elemento sem fundo e acusou a bussola, que estava certa."""
    saida, i = [], 0
    for m in _KF.finditer(css):
        if m.start() < i:
            continue
        prof, k = 0, m.end() - 1
        while k < len(css):
            if css[k] == "{":
                prof += 1
            elif css[k] == "}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        saida.append(css[i:m.start()])
        i = k + 1
    saida.append(css[i:])
    return "".join(saida)


def regras(css):
    css = sem_keyframes(css)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css, re.S):
        sel, corpo = m.group(1).strip(), m.group(2)
        if not sel or sel.startswith("@") or "%" in sel.split("{")[0][:6]:
            continue
        yield sel, corpo


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/cor_fixa.py <peca.html>")
        return 2
    arq = sys.argv[1]
    html = io.open(arq, encoding="utf-8").read()
    st = re.findall(r"<style>(.*?)</style>", html, re.S)
    if not st:
        print(u"%s -> sem <style>. NAO MEDI." % arq)
        return 2
    css = re.sub(r"/\*.*?\*/", " ", st[0], flags=re.S)

    # ⚠️ PRIMEIRA VERSAO ACUSOU 66 DE 80, e isso nao e portao: e ruido. O erro
    #    era olhar so a PROPRIA regra. Uma dica clara dentro de um cartao que a
    #    peca ja pintou de escuro esta protegida — o fundo existe, so nao esta
    #    na mesma linha. Entao antes de julgar, junto quem pinta fundo na peca e
    #    perdoo todo seletor que desca de um deles.
    pinta = set()
    for sel, corpo in regras(css):
        if re.search(r"(?<![-\w])background(-color)?\s*:\s*(?!none|transparent)", corpo):
            for s in sel.split(","):
                s = s.strip()
                if s:
                    pinta.add(s.split(":")[0].strip())
                    # ⚠️ LICAO PAGA (set/2026): quem pinta e o ULTIMO elemento do
                    #    seletor. `.centro .pecabox{background:...}` pinta a
                    #    `.pecabox` — mas so a frase inteira entrava aqui, e o
                    #    `protegido()` compara pedaco a pedaco: `.pecabox` nao
                    #    estava, e todo texto que mora dentro dela era acusado de
                    #    nao ter fundo. Falso em toda atividade montada.
                    ult = s.split()[-1].split(":")[0].strip()
                    if ult:
                        pinta.add(ult)

    def protegido(sel):
        u"""algum ancestral do seletor pinta fundo dentro da propria peca?"""
        for s in sel.split(","):
            partes = s.strip().split()
            # o proprio elemento ja conta (ex.: `.cx.escura .dica` quando
            # `.dica` tambem tem fundo noutra regra)
            for pedaco in partes:
                base = pedaco.split(":")[0].strip()
                if base and base in pinta:
                    return True
        return False

    # ⚠️⚠️ O DEFEITO ESPELHO (ago/2026), e ele custou seis pecas reprovadas numa
    #    varredura so: `color:var(--texto)` DENTRO de uma superficie que a
    #    PROPRIA peca pinta. O token e a tinta da ATIVIDADE, escolhida para o
    #    fundo dela; o ladrilho da peca (a celula creme da cruzadinha, a pedra do
    #    domino, o mostrador do relogio) tem fundo PROPRIO e portanto precisa de
    #    tinta propria. Numa atividade de tema claro isso deu 1,05:1 — creme
    #    sobre creme — em 36 numeros do relogio de uma vez.
    #    ⚠️ E a reserva do `var()` nao protege: `var(--texto,#221a12)` so usa o
    #    #221a12 quando o token NAO EXISTE, e dentro de uma atividade ele existe
    #    sempre. Escrever a reserva da uma falsa sensacao de cuidado.
    herdadas = []
    for sel, corpo in regras(css):
        if not re.search(r"(?<![-\w])color\s*:\s*var\(\s*--texto", corpo):
            continue
        if re.search(r"(?<![-\w])background(-color)?\s*:\s*(?!none|transparent)", corpo):
            continue          # pinta o proprio fundo: sabe onde esta
        if protegido(sel):    # mora dentro de algo que a PECA pintou
            herdadas.append(" ".join(sel.split())[:44])

    ruins, ok = [], 0
    for sel, corpo in regras(css):
        m = re.search(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})", corpo)
        if not m:
            continue
        temFundo = re.search(r"(?<![-\w])background(-color)?\s*:", corpo)
        # ⭐ (set/2026, Bancada da Divisao) letra branca com SOMBRA ESCURA por baixo
        #    (`text-shadow: 0 1px 3px #000`) tem contraste PROPRIO em qualquer fundo —
        #    e a tecnica certa para texto sobre a foto do cenario, quando a tarja
        #    escura atravessando a tela foi justamente o que o Marcos mandou tirar.
        #    Quem mede o contraste real e o `contraste.js` (pixel); aqui basta saber
        #    que a regra nao esta apostando num fundo que nao pintou.
        if not temFundo and re.search(r"text-shadow\s*:\s*[^;]*(#0|#1|#2|#3|rgba\(0,\s*0,\s*0|black)", corpo):
            temFundo = True
        vv = luz(m.group(1))
        if vv is None:
            continue
        L, sat = vv
        # ⚠️ SEGUNDA APARADA (66 -> 62 -> o numero honesto): o amarelo da casa
        #    (#ffd54a) tem luminancia alta e foi acusado de "quase branco". Ele
        #    nao e: e ACENTO, escolhido de proposito, e some da conta. O que
        #    briga com o tema e a cor NEUTRA extrema — o creme e o quase-preto,
        #    que foram exatamente os dois casos que me morderam. Cor saturada
        #    tem dono; cinza claro nao tem.
        if temFundo or protegido(sel) or sat >= 45 or (ESCURO < L < CLARO):
            ok += 1
            continue
        ruins.append((" ".join(sel.split())[:44], m.group(1),
                      u"quase branco" if L >= CLARO else u"quase preto"))

    print(u"%s -> %d regra(s) com cor de texto conferida(s)" % (arq, ok + len(ruins)))
    if herdadas:
        print(u"   %d TINTA HERDADA DENTRO DE LADRILHO PROPRIO — a peca pinta o "
              u"fundo e deixa a cor da letra para a atividade decidir:" % len(herdadas))
        for h in herdadas[:10]:
            print(u"    - %s  usa `var(--texto)` morando em superficie da propria peca" % h)
        print(u"   conserto: escrever a tinta (`color:#221a12`). O token e a tinta")
        print(u"   do FUNDO DA ATIVIDADE; quem tem fundo proprio tem tinta propria.")
        return 1
    if not ruins:
        print(u"   cor ok: nenhuma cor cravada sem fundo proprio")
        return 0

    print(u"   %d COR(ES) CRAVADA(S) SEM FUNDO PROPRIO — vao brigar com o tema:"
          % len(ruins))
    for sel, cor, tom in ruins[:10]:
        print(u"    - %s  color:%s (%s) e nao pinta fundo nenhum" % (sel, cor, tom))
    print(u"   conserto: `color:var(--texto)`. O motor define o token e CADA")
    print(u"   atividade o redefine — a peca passa a seguir o tema em vez de")
    print(u"   apostar num. Se a cor for mesmo da peca, pinte o fundo junto.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
