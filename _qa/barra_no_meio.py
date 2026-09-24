# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 4c — A BARRA DE ROLAGEM NO MEIO DA TELA

 ⭐ ACHADO PELO MARCOS (24/set/2026), na prova de Ed. Fisica, com a turma a
    caminho: ***"vi que nessa prova a barra de rolagem fica no meio da prova,
    favor concertar e jogar la no canto"***.

 A RECEITA DO DEFEITO, e ela cabe numa linha de CSS:

     #app{ max-width:820px; margin:0 auto; height:100vh; overflow-y:auto; }

 As duas metades sao inocentes sozinhas. Juntas, quem rola e a CAIXA, nao a
 pagina — e a barra de uma caixa CENTRADA de 820 px nasce na borda DELA. Numa
 tela de 1366 px isso da **x = 1093**, ou seja, 273 px para dentro: uma barra
 cinza no meio do desenho. A pagina, essa, nunca rola, entao nao ha barra
 nenhuma na beirada da janela. MEDIDO nas duas versoes do `_efjogos`:
     antes  -> a caixa rola, barra em x=1093 de 1366
     depois -> a pagina rola, barra em x=1366

 ⚠️⚠️ E NAO E SO ESTETICA — sao TRES estragos, e o terceiro e o pior:
    1. no PC da escola a crianca procura a barra onde ela sempre esta (na
       beirada) e nao acha;
    2. a roda do mouse so rola se o ponteiro estiver DENTRO da caixa;
    3. ⭐ **o `scrollTop` da caixa deixa de subir a tela quando a caixa deixa
       de rolar** — e o contrario tambem: enquanto a caixa rola, um
       `window.scrollTo(0,0)` nao faz nada. Quem troca um pelo outro sem
       trocar o outro deixa a crianca vendo a pergunta seguinte ja rolada
       pela metade. Por isso este portao cobra OS DOIS: o CSS e o comando que
       sobe a tela.

 ⚠️ O QUE ELE **NAO** ACUSA, de proposito:
    · caixa que rola e NAO e centrada (uma coluna colada na beirada, um painel
      lateral): ali a barra ja esta no canto;
    · caixa de rolagem LOCAL e pequena (uma lista, uma tabela larga, o
      `overflow-x` de um tabuleiro): a barra dela e parte da peca;
    · `position:fixed; inset:0` (o motor do `_central` e do `_rightnow9`), que
      ocupa a janela inteira — a borda da caixa E a beirada da janela.
    O corte esta em LARGURA_MAX: caixa mais estreita que isto, centrada e da
    altura da janela, e conteiner de pagina, nao peca.

 Uso:  python3 _qa/barra_no_meio.py <pasta ou arquivo.html>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# ⚠️ PALPITE DECLARADO — nao saiu de medida com crianca: e o juizo de onde
#    acaba "caixa de pagina" e comeca "peca". 1200 px porque as telas da escola
#    tem 1366, e uma caixa de 1200 centrada ja poe a barra a 83 px da beirada,
#    que ninguem chama de "no meio".
LARGURA_MAX = 1200

ROLA = re.compile(r"overflow(-y)?\s*:\s*(auto|scroll)")
ALTURA_CHEIA = re.compile(r"(?<!min-)height\s*:\s*(100vh|100dvh|100%)")
CENTRADA = re.compile(r"margin\s*:\s*0\s+auto|margin\s*:\s*[^;]*\bauto\b"
                      r"|margin-left\s*:\s*auto")
LARGURA = re.compile(r"max-width\s*:\s*(\d+)px")
FIXA = re.compile(r"position\s*:\s*fixed")


def regras(css):
    u"""[(seletor, corpo)] — quebra boba, serve para achar o bloco do container."""
    saida = []
    for m in re.finditer(r"([^{}@/]+)\{([^}]*)\}", css):
        sel = m.group(1).strip().split(u"\n")[-1].strip()
        if sel:
            saida.append((sel, m.group(2)))
    return saida


def sem_comentario(s):
    u"""Apaga comentarios de JS/CSS e o miolo de <!-- -->.

    ⚠️⚠️ LICAO JA PAGA NESTA CASA, no portao `1i9` (*"portao que le o proprio
       comentario nao mede nada"*), e eu a repeti no mesmo dia: este portao
       contava os `$("app").scrollTop = 0` e achou UM — dentro do comentario
       que EXPLICA por que eles sairam. Reprovava o arquivo ja consertado."""
    s = re.sub(r"/\*.*?\*/", u" ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", u" ", s, flags=re.S)
    s = re.sub(r"(?m)^\s*//.*$", u" ", s)
    return s


def olha(cam):
    s = sem_comentario(io.open(cam, encoding=u"utf-8").read())
    css = u"\n".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S | re.I))
    if not css:
        return None, None
    culpadas = []
    for sel, corpo in regras(css):
        if FIXA.search(corpo):
            continue                      # ocupa a janela: a borda e a beirada
        if not (ROLA.search(corpo) and ALTURA_CHEIA.search(corpo)):
            continue
        if not CENTRADA.search(corpo):
            continue                      # colada na beirada: a barra ja esta la
        mw = LARGURA.search(corpo)
        if not mw or int(mw.group(1)) > LARGURA_MAX:
            continue
        culpadas.append((sel, int(mw.group(1)), corpo.strip()[:100]))
    return culpadas, s


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/barra_no_meio.py <pasta ou arquivo.html>")
        return 2
    alvo = sys.argv[1].rstrip(u"/")
    cam = alvo if alvo.endswith(u".html") else os.path.join(alvo, u"index.html")
    if not os.path.exists(cam):
        print(u"NAO MEDI: nao achei %s." % cam)
        return 2
    culpadas, s = olha(cam)
    if culpadas is None:
        print(u"%s -> NAO MEDI: a pagina nao tem <style> proprio." % cam)
        return 2

    print(u"%s -> barra de rolagem: conferido" % cam)
    print(u"   PALPITE DECLARADO: caixa centrada mais estreita que %d px conta "
          u"como conteiner de pagina (juizo meu, nao medida)." % LARGURA_MAX)
    if not culpadas:
        # a outra metade: quem sobe a tela sem caixa que role
        soltos = re.findall(r'\$\("(\w+)"\)\.scrollTop\s*=\s*0', s)
        soltos += re.findall(r'getElementById\("(\w+)"\)\.scrollTop\s*=\s*0', s)
        if soltos:
            print(u"   ⚠️ %d comando(s) `.scrollTop = 0` numa caixa que NAO rola "
                  u"(%s) — eles nao sobem nada. Quem sobe a tela agora e "
                  u"`window.scrollTo(0,0)`; ver o `aoTopo()` do `_efjogos`."
                  % (len(soltos), u", ".join(sorted(set(soltos)))))
            return 1
        print(u"   ok: quem rola e a pagina, e a barra fica na beirada da janela.")
        return 0

    print(u"   %d CAIXA(S) COM A BARRA NO MEIO DA TELA:" % len(culpadas))
    for sel, larg, corpo in culpadas:
        meio = (1366 - larg) // 2 + larg
        print(u"    x %-12s max-width %d px, centrada, com altura de janela e "
              u"overflow proprio" % (sel, larg))
        print(u"        numa tela de 1366 px a barra nasce em x=%d — %d px para "
              u"dentro da beirada" % (meio, 1366 - meio))
        print(u"        %s" % corpo)
    print(u"   conserto: tirar `height:100vh` e `overflow-y:auto` do container "
          u"(deixar so o `min-height`), para quem rolar ser a PAGINA — e trocar")
    print(u"   os `$(\"app\").scrollTop = 0` por um `aoTopo()` que sobe a JANELA, "
          u"senao a crianca ve a tela seguinte ja rolada pela metade.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
