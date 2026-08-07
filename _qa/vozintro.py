#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA INTRO QUE CALA A PERGUNTA — "a primeira pergunta é falada?"

Cobrança do Marcos (ago/2026): *"no mapa do bairro o símbolo escola não é
falado"*. Ele achou UMA fase. Quando fui medir, eram **27** — quase todas as
fases das duas atividades, sempre a PRIMEIRA rodada.

O molde do defeito:

    function passo(){
      ...
      falaDaTela("x_q0");              // toca a pergunta...
      ...
      if(idx===0) falar("x_intro");    // ...e a introducao entra por cima
    }

`falar()` dá `narr.pause()` antes de tocar o novo áudio. Então, na primeira
rodada, a criança ouve só a introdução — a pergunta nunca é dita. Quem lê nem
percebe, porque o texto está na tela. Quem NÃO lê fica sem instrução nenhuma —
e o alto-falante existe exatamente para essa criança.

O conserto é o `introEPergunta(id)` do motor: a intro toca e, quando acaba, a
pergunta vem em seguida.

REGRA: dentro de uma mesma função, `falar("..._intro")` não pode vir DEPOIS de
um `falaDaTela(...)`. Se vier, a intro está calando a pergunta.

Uso:  python3 _qa/vozintro.py _mapa/index.html
Sai com 1 se achar.
"""
import io
import re
import sys


def corpos(js):
    for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
        j = js.find("{", m.end())
        k = j
        prof = 0
        while k < len(js):
            if js[k] == "{":
                prof += 1
            elif js[k] == "}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        yield m.group(1), js[j:k]


def dentro_de_gatilho(corpo, pos):
    u"""⚠️ LICAO PAGA (ago/2026): ORDEM DE ARQUIVO NAO E ORDEM DE TEMPO.

    Este portao dizia que a intro do "Monte seu prato" calava a pergunta, porque
    o `falaDaTela` aparecia ANTES do `falar(intro)` no arquivo. So que aquele
    `falaDaTela` esta DENTRO de um `onclick`: ele so toca quando a crianca enche
    o prato — muito DEPOIS de a tela abrir e a intro tocar. Eu quase "consertei"
    uma atividade que esta no ar e funciona.

    Uma chamada dentro de `onclick`/`onkeydown`/`addEventListener`/`setTimeout`
    acontece por causa de um GESTO da crianca ou do relogio, nunca na abertura da
    tela. Para esta pergunta, ela nao conta."""
    trecho = corpo[:pos]
    # conta as chaves abertas dentro de um gatilho ainda nao fechado
    prof = 0
    i = 0
    dentro = []
    while i < len(trecho):
        if re.match(r"on\w+\s*=\s*function|addEventListener\s*\(|setTimeout\s*\(|setInterval\s*\(",
                    trecho[i:i + 40]):
            dentro.append(prof)
        if trecho[i] == "{":
            prof += 1
        elif trecho[i] == "}":
            prof -= 1
            dentro = [d for d in dentro if d < prof]
        i += 1
    return bool(dentro)


def primeira_na_abertura(corpo):
    u"""o primeiro `falaDaTela` que toca QUANDO A TELA ABRE (fora de gatilho)."""
    for m in re.finditer(r'falaDaTela\("([a-z0-9_]+)"', corpo):
        if not dentro_de_gatilho(corpo, m.start()):
            return m
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)

    if "falaDaTela" not in js:
        print(u"%s -> nenhuma fase usa falaDaTela. Nada a conferir." % alvo)
        return 0

    caladas, ok = [], 0
    for nome, corpo in corpos(js):
        q = primeira_na_abertura(corpo)
        if not q:
            continue
        ok += 1
        intro = re.search(r'\bfalar\("([a-z0-9_]+_intro)"\)', corpo)
        if intro and intro.start() > q.start():
            caladas.append((nome, q.group(1), intro.group(1)))

    print(u"%s -> %d fase(s) com pergunta falada" % (alvo, ok))
    if caladas:
        print(u"   %d FASE(S) EM QUE A INTRO CALA A PERGUNTA (na primeira rodada a "
              u"crianca que nao le fica sem instrucao):" % len(caladas))
        for nome, q, i in caladas[:10]:
            print(u"    - %s: falaDaTela(\"%s\") e depois falar(\"%s\")" % (nome, q, i))
        print(u"   conserto: `introEPergunta(\"<intro>\")` no lugar do `falar(\"<intro>\")` "
              u"— a intro toca e a pergunta vem logo atras.")
        return 1
    print(u"   voz ok: nenhuma introducao passa por cima da pergunta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
