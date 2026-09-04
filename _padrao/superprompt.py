# -*- coding: utf-8 -*-
u"""
============================================================
 SUPER-PROMPT — escrever para o POLLINATIOS como se escreve para o GEMINI.

 ⭐ ORDEM DO MARCOS (set/2026): *"Pode gerar em Pollinations, mas terá que fazer
 super prontos para ele gerar igual Gemini"* e, logo depois, com todas as letras:
 *"Preciso que vc faça super prompts para o Pollinations conseguir gerar igual
 Gemini, só assim para substituir"*.

 O contexto: a arte deixou de ser gerada por ele e passou a ser gerada por mim
 (o Gemini está sem cota desde 2026-08-12; o caminho grátis é o Pollinations).
 Só que trocar de gerador NÃO é trocar o endereço da chamada — os dois leem o
 prompt de jeitos diferentes, e o prompt que ajuda num ATRAPALHA no outro.

 ─────────────────────────────────────────────────────────────
 A DESCOBERTA QUE ORIGINOU ESTE ARQUIVO

 O molde da casa (`_padrao/cartela.py`) termina assim:

     "... No text, no letters, no numbers, no labels, no frames, no background
      scenery."

 Isso é excelente para o **Gemini**, que entende instrução e obedece à negação.
 E é ruim para o **Pollinations/Flux**, que em boa medida NÃO entende negação:
 ele vê as palavras `text`, `letters`, `numbers`, `labels`, `frames` e tende a
 DESENHAR justamente isso. É o velho "não pense num elefante".

 Ou seja: parte do "a arte grátis sai pior" nunca foi o gerador — era o prompt
 estar escrito no idioma do gerador errado.

 ─────────────────────────────────────────────────────────────
 AS SEIS REGRAS DO SUPER-PROMPT (é isto que este módulo aplica)

 1. **DIGA O QUE HÁ, NUNCA O QUE NÃO HÁ.** Em vez de "no text", descreva a
    superfície: *"the surface is smooth, blank and unmarked"*. O resultado é o
    mesmo e o modelo não é induzido a desenhar letra nenhuma.
 2. **O ASSUNTO NA FRENTE.** As primeiras palavras pesam mais. Começa pelo
    objeto e pelo que o distingue — não pelo estilo.
 3. **FRASE INTEIRA, NÃO SOPA DE PALAVRAS-CHAVE.** O Flux lê por um codificador
    de texto de verdade (T5): frase bem formada rende melhor que
    "cute, 3d, clay, 8k, masterpiece". Adjetivo empilhado é herança de modelos
    antigos e hoje só suja.
 4. **BLOCO DE ESTILO IDÊNTICO, LETRA POR LETRA, EM TODAS AS PEÇAS.** É o que
    faz as figuras parecerem da mesma família. Mudar uma vírgula entre duas
    peças já muda o traço.
 5. **SEMENTE FIXA POR CARTELA.** Sem `seed`, cada chamada sorteia um mundo
    novo — foi por isso que peças da mesma atividade saíam com luz e escala
    diferentes. (O `gerar-imagens.yml` passou a aceitar o campo `semente`;
    antes ele nem mandava esse parâmetro.)
 6. **COMPOSIÇÃO EXPLÍCITA.** Enquadramento, ângulo, se o objeto está inteiro
    dentro do quadro e quanto de folga tem em volta. O modelo não adivinha.

 ⚠️ O QUE ESTE MÓDULO **NÃO** RESOLVE: se o desenho ficou feio por gosto, é
 gosto — quem aprova é o Marcos. Aqui só se garante que o pedido foi feito no
 idioma certo, com estilo e luz iguais aos das 500+ figuras que já temos.

 ─────────────────────────────────────────────────────────────
 ⭐⭐ A RECEITA QUE SAIU DO TESTE — "A SEMENTE DE PROVA"

 O teste de 6 imagens (2 sementes x 3 versões de prompt, em `_novo/prova_*.png`)
 mostrou o que nenhum prompt resolve sozinho: **a semente carrega um jeito de
 desenhar**. Com a v2 do prompt, a semente 20260904 deu massinha fosca perfeita
 e a 20260905 insistiu em penas realistas — mesmo texto, mesmo motor.

 Então parar de brigar com isso e usar a favor. Ao começar uma atividade:

   1. Escolher UMA peça de referência (o mascote, de preferência).
   2. Gerar essa peça em **3 sementes diferentes**, mesmo prompt.
   3. **O Marcos escolhe a família** — uma aprovação só, não uma por figura.
   4. Essa semente TRAVA a atividade inteira: todas as outras peças usam ela.

 Por que isto vale mais que um prompt perfeito:
   · a irmandade deixa de ser sorte e vira garantia;
   · ele aprova UMA vez, no começo, em vez de reprovar peça por peça no fim —
     que era o atrito que fazia a arte custar dias;
   · peça que sair torta se refaz IGUAL (mesma semente), mudando só o que se
     quer, em vez de sortear tudo de novo e perder a família.

 Uso:
     from superprompt import peca, cena, cartela
     peca(u"a red apple with a green leaf")
     cartela([u"a red apple", u"a yellow banana"], semente=4242)
============================================================
"""

# ⚠️ IDÊNTICO ao `ESTILO` do `_padrao/cartela.py`, de propósito e letra por
#    letra: é o que mantém a arte nova parente das 500+ que já estão no banco.
#    Se um dia mudar, tem que mudar NOS DOIS — senão a casa passa a ter dois
#    estilos brigando, que foi o defeito dos Papagaios (ver cartela.py).
ESTILO = (u"Soft matte clay 3D illustration, children's storybook style, "
          u"rich saturated colours, soft shadows.")

# a luz também é fixa: luz diferente é o que mais denuncia peça de outra família
LUZ = (u"Soft even studio light coming from the upper left, gentle contact "
       u"shadow directly under the object.")

# ⭐ o lugar das antigas negações — agora dito pelo lado positivo (regra 1)
LIMPO = (u"Every surface is smooth, blank and unmarked. The image contains only "
         u"the object itself.")

FUNDO_RECORTE = (u"The object floats alone on a plain, perfectly flat, pure "
                 u"black background (#000000), with clear empty margin on all "
                 u"four sides.")

ENQUADRA_PECA = (u"The whole object is inside the frame, centred, seen from a "
                 u"slight three-quarter angle, filling about three quarters of "
                 u"the image height.")


def _limpa(t):
    u"""tira espaço dobrado e junta em uma linha só (a URL do Pollinations não
    gosta de quebra de linha)."""
    return u" ".join((t or u"").split())


def peca(descricao, enquadramento=None):
    u"""PEÇA recortável (vai para o `rembg` e assenta na cena com fundo
    transparente). `descricao` é uma frase em inglês descrevendo o objeto —
    o resto vem pronto e é sempre igual.

    ⚠️⚠️ A ORDEM AQUI FOI PAGA COM UM TESTE (set/2026). A primeira versão punha
    o ESTILO só depois do enquadramento, e a coruja de prova saiu quase
    REALISTA — penas, olho de bicho — em vez de massinha fosca. Nestes modelos
    o começo da frase pesa mais: ao empilhar composição e luz antes do estilo,
    eu diluí justamente o que segura a identidade da casa.
    Agora o ESTILO vem COLADO no assunto (2ª posição, onde ainda pesa) e é
    REPETIDO no fim como âncora. Composição e luz ficam no meio, que é onde
    elas bastam. Ver as 4 imagens de prova em `_novo/prova_*.png`."""
    d = descricao.strip().rstrip(u".")
    return _limpa(u" ".join([
        d + u".", ESTILO,
        enquadramento or ENQUADRA_PECA,
        LUZ, FUNDO_RECORTE, LIMPO,
        u"Modelled in soft matte clay, like a children's storybook toy.",
    ]))


def cena(descricao):
    u"""CENA larga (fundo/cenário): vai inteira, sem recorte, e por isso tem
    fundo próprio em vez do preto."""
    return _limpa(u" ".join([
        descricao.strip().rstrip(u".") + u".",
        u"Wide establishing view with generous empty space in the middle of the "
        u"frame where characters and pieces will be placed later.",
        ESTILO, LUZ,
        u"Every surface is smooth, blank and unmarked.",
    ]))


def cartela(itens, semente=None, colunas=3):
    u"""FOLHA com várias peças (a cartela — mais barata e, sobretudo, irmã:
    peças geradas juntas nascem com a mesma luz e a mesma escala).

    Devolve o dicionário no formato que o `gerar-imagens.yml` lê no `lote`,
    já com a `semente` — que é o que trava a família."""
    lista = u"\n".join(u"  %d. %s" % (i + 1, d.strip().rstrip(u"."))
                       for i, d in enumerate(itens))
    linhas = (len(itens) + colunas - 1) // colunas
    prompt = _limpa(
        u"A sheet showing %d separate objects arranged in a tidy %dx%d grid. "
        u"Each object sits alone inside its own cell, well separated from the "
        u"others, none of them touching, all drawn at the same scale and lit the "
        u"same way. %s %s The background behind every object is plain, perfectly "
        u"flat, pure black (#000000). %s The objects, in reading order from left "
        u"to right and top to bottom, are:"
        % (len(itens), linhas, colunas, ESTILO, LUZ, LIMPO)) + u"\n" + lista
    saida = {u"prompt": prompt}
    if semente is not None:
        saida[u"semente"] = semente
    return saida


# ─────────────────────────────────────────────────────────────
# O PORTÃO: um prompt do jeito antigo passa aqui e é reprovado.
def confere(prompt):
    u"""Devolve a lista de problemas de um prompt para o Pollinations.
    Vazia = está no idioma certo."""
    p = (prompt or u"").lower()
    ruins = []
    for termo in (u"no text", u"no letters", u"no numbers", u"no labels",
                  u"no frames", u"no words", u"without text", u"avoid "):
        if termo in p:
            ruins.append(
                u"negação \"%s\": o Flux não obedece negação e tende a desenhar "
                u"justamente o que ela cita. Diga pelo lado positivo "
                u"(ex.: \"the surface is smooth, blank and unmarked\")." % termo.strip())
    for termo in (u"8k", u"4k", u"masterpiece", u"best quality", u"ultra detailed",
                  u"highly detailed", u"trending on artstation"):
        if termo in p:
            ruins.append(
                u"enfeite de modelo antigo \"%s\": não melhora nada no Flux e "
                u"rouba peso do que importa." % termo)
    if ESTILO.lower() not in p:
        ruins.append(u"sem o BLOCO DE ESTILO da casa — a peça vai sair de outra "
                     u"família que as 500+ do banco.")
    if len(p.split()) < 25:
        ruins.append(u"curto demais (%d palavras): prompt curto no Pollinations "
                     u"volta genérico. O padrão da casa passa de 40." % len(p.split()))
    return ruins


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "confere":
        texto = sys.stdin.read()
        ruins = confere(texto)
        if ruins:
            print(u"REPROVOU — %d problema(s):" % len(ruins))
            for r in ruins:
                print(u"  - %s" % r)
            sys.exit(1)
        print(u"prompt no idioma do Pollinations: ok")
        sys.exit(0)
    print(u"=== PEÇA ===")
    print(peca(u"a shiny red apple with one green leaf on its stalk"))
    print(u"")
    print(u"=== CENA ===")
    print(cena(u"a bright primary school classroom with wooden desks and a big window"))
    print(u"")
    print(u"=== CARTELA (3 peças, semente travada) ===")
    import json
    print(json.dumps(cartela([u"a red apple", u"a yellow banana", u"a bunch of purple grapes"],
                             semente=4242), ensure_ascii=False, indent=1))
