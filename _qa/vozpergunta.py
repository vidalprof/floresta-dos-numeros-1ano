#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA VOZ DA PERGUNTA — "o alto-falante fala o que está escrito?"

Duas cobranças do Marcos no mesmo dia (ago/2026):

  *"na fase o navio por dentro… o texto lá em cima fica a explicação correta,
   mas se clica para ouvir ele narra a introdução da fase e não a explicação da
   foto que se clicou"*

  *"o botão de som ao lado do enunciado não fala exatamente o que diz o texto
   do enunciado, isso é problema?"*

**É problema, sim** — e o pior tipo: o botão existe **exatamente** para quem não
lê saber o que a tela está pedindo. Se a tela diz "ache a roça" e a voz conta a
história da aldeia, o botão não serve para o que foi feito.

A causa é que muitas fases TROCAM o texto do balão a cada rodada (a pergunta
muda, a explicação da peça aparece) e continuam com a narração da abertura, que
foi tocada uma vez só, lá no começo.

REGRA QUE ESTE PORTÃO APLICA
  toda vez que a fase escreve CONTEÚDO no balão (`bal.innerHTML=`), tem que
  trocar também a voz da tela — `falaDaTela("id")` — logo ali.

  ⚠️ CONTADOR NÃO É PERGUNTA. "Faltam 3", "Já achou 2 de 5", "Já são 4 de 8
  móveis no lugar" são placares: mudam o tempo todo, não pedem nada de novo e
  não precisam de voz. Narrar cada um seria ruído. Por isso eles ficam de fora.

Uso:  python3 _qa/vozpergunta.py _naveg/index.html
Sai com 1 se achar pergunta escrita sem voz.
"""
import io
import re
import sys

# placares e contadores — mudam o número, não o pedido
CONTADOR = re.compile(r"Faltam?\b|J&#225; achou|J&#225; s&#227;o|J&#225; est&#227;o|J&#225; tem|"
                      r"Ja achou|Ja sao|de <b>\"\+|acertos|pontos|encheu com", re.I)
# aviso de "faca isto primeiro" — nao e a pergunta da tela, e um empurraozinho
# depois de um toque fora de ordem. Some sozinho no toque seguinte.
AVISO = re.compile(r"Primeiro toque|Toque primeiro|Escolha primeiro", re.I)


def montada(html):
    u"""⭐ A ATIVIDADE MONTADA RESOLVE ISTO DE OUTRO JEITO — e este portao, que
    le o CODIGO, nao tem como enxergar.

    Aqui a regra e "todo texto de balao que muda tem que chamar `falaDaTela` na
    mesma hora". No esqueleto ninguem chama: um OLHEIRO no balao percebe a troca
    e fala sozinho, se houver voz gravada para aquele texto (a conta e o sha do
    proprio texto). Lendo o codigo, este portao acusava 16 perguntas "sem voz"
    numa atividade com 79 vozes gravadas.

    E a medicao de verdade existe, e e melhor que a estatica: o `colher.py` JOGA
    a atividade inteira e anota TODO texto que aparece; quando ele diz "nada a
    acrescentar", e porque nao ha tela sem voz. Por isso, em atividade montada,
    este portao aponta para la em vez de adivinhar pelo codigo."""
    return bool(re.search(r"\bMEC\[", html) and re.search(r"\bFASES\s*=", html)
                and "pecabox" in html)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    if montada(html):
        print(u"%s -> atividade MONTADA: a voz da rodada e do olheiro do balao, "
              u"nao de uma chamada no codigo." % alvo)
        print(u"   a medicao de verdade e jogando: "
              u"python3 _padrao/ESQUELETO/colher.py <pasta> --so-ver")
        return 0
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)

    if "falaDaTela" not in js and "bal.innerHTML=" not in js:
        print(u"%s -> nenhuma fase troca o enunciado. Nada a conferir." % alvo)
        return 0

    faltam, ok = [], 0
    # ⚠️ BURACO QUE O MARCOS ACHOU (ago/2026): este portao so olhava
    #    `bal.innerHTML=`. Mas ha fases que montam o balao DE NOVO a cada
    #    rodada — `el("div","balao","Na maquete voce ve "+it.q+"...")` dentro
    #    do `passo()`. Ali o texto muda igual, e a voz ficava na abertura: na
    #    "maquete ao mapa" a palavra PONTE nunca era falada. Um portao que so
    #    conhece UMA maneira de escrever a mesma coisa da uma falsa aprovacao,
    #    que e pior do que nao ter portao.
    #    Agora conta as duas formas: o balao REESCRITO e o balao CRIADO com um
    #    pedaco variavel (`"+it.` / `"+fila[` / `"+PINTAS[`...).
    ALVOS = [r"\bbal\.innerHTML\s*=\s*(.{0,160})",
             r'el\("div","balao",\s*("[^"]*"\s*\+\s*\w+[^)]{0,160})']
    for m in [mm for pad in ALVOS for mm in re.finditer(pad, js)]:
        texto = m.group(1)
        if CONTADOR.search(texto) or AVISO.search(texto):
            continue
        # ⚠️ texto MONTADO PELA CRIANCA (a frase que ela escreveu) nao tem como
        #    ter audio pronto. A fase declara isso com a linha
        #    `"sem voz: ...";` logo antes — e uma instrucao de verdade, nao um
        #    comentario, porque comentario este portao apaga antes de olhar.
        #    Declarar e melhor que adivinhar.
        if "sem voz:" in js[max(0, m.start() - 400):m.start()]:
            continue
        # ⚠️ o proprio trecho capturado pode ja trazer a troca da voz (quando as
        #    duas coisas estao na MESMA linha) — senao o portao acusa a si mesmo
        if "falaDaTela(" in texto:
            ok += 1
            continue
        # a troca da voz tem que vir logo depois (mesma linha ou a seguinte)
        volta = js[m.end():m.end() + 240]
        if "falaDaTela(" in volta or "falaDaTela(" in js[max(0, m.start() - 120):m.start()]:
            ok += 1
            continue
        limpo = re.sub(r"\s+", " ", texto)[:64]
        faltam.append(limpo)

    print(u"%s -> %d enunciado(s) trocado(s) em tempo de jogo" % (alvo, ok + len(faltam)))
    if faltam:
        print(u"   %d PERGUNTA(S) QUE MUDAM NA TELA SEM MUDAR A VOZ (quem nao le "
              u"aperta o alto-falante e ouve outra coisa):" % len(faltam))
        for f in faltam[:8]:
            print(u"    - %s" % f)
        print(u"   conserto: `falaDaTela(\"<id da fala desta pergunta>\")` na mesma hora "
              u"em que o texto e escrito.")
        return 1
    print(u"   voz ok: toda pergunta que muda na tela muda tambem na voz")
    return 0


if __name__ == "__main__":
    sys.exit(main())
