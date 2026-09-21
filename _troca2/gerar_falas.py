# -*- coding: utf-8 -*-
u"""
============================================================
 ESQUELETO — gerador das falas da folha viva

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️ UMA FONTE SÓ. As palavras, as frases e os textos moram no bloco
    `/*DADOS-INI*/` do `index.html` e são LIDOS daqui. Nada de segunda lista
    para desencontrar: já custou caro nesta casa um relatório sair zero com a
    folha inteira respondida.

 ⚠️ TODA TELA É NARRADA, e o alto-falante entra também em CADA RESPOSTA que a
    criança toca. Regra do Marcos: *"o alto-falante nas respostas também, para
    ajudar os alunos que não sabem ler"*. Sem isso a criança que ainda soletra
    escolhe pelo tamanho da palavra e a folha vira sorteio.

 ⚠️ A DICA NUNCA DIZ A RESPOSTA. Ela manda olhar uma pista, ou faz outra
    pergunta. Responder no segundo erro não é ajudar: é tirar da criança a única
    chance de pensar de novo.

 ⚠️ PALAVRAS QUE A VOZ ERRA (medido, e o portão `_qa/falas.py` reprova):
    "complete" vira "complite" — usar "preencha". Letra solta ("som S") sai como
    o NOME da letra: ancorar num exemplo ("o som de SAPO").

 Uso:  python3 <pasta>/gerar_falas.py
 Saída: reescreve os blocos FALAS e VOZOK do index.html, o `falas.json` e o
        `voz.txt`.
============================================================
"""
from __future__ import print_function

import collections
import io
import json
import os
import re
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"mq_"                     # <- o prefixo desta atividade
VOZ = u"pt-BR-AntonioNeural"

D = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    u"""Lê um objeto do bloco DADOS do index.html. Uma fonte só.

    ⚠️ ELE CONTA AS CHAVES, e isso foi conserto de 15/set/2026. O esqueleto
       procurava o fim do objeto por uma marca de texto (`\n});`) — e QUALQUER
       objeto que não terminasse exatamente assim fazia a leitura passar
       adiante e engolir o bloco seguinte. No primeiro caderno do 2º ano os
       vinte e três blocos falharam de uma vez, todos com o mesmo erro, e a
       mensagem do json não dizia nada sobre a causa. Contar chave por chave
       (pulando as que estão DENTRO de texto) acha o fim de qualquer objeto.
    """
    i = D.find(u"var " + nome + u" = ")
    if i < 0:
        raise SystemExit(u"nao achei o bloco `var %s` no index.html" % nome)
    i = D.index(u"{", i)
    nivel, j, dentro, escapa = 0, i, False, False
    while j < len(D):
        c = D[j]
        if dentro:
            if escapa:
                escapa = False
            elif c == u"\\":
                escapa = True
            elif c == u'"':
                dentro = False
        else:
            if c == u'"':
                dentro = True
            elif c == u"{":
                nivel += 1
            elif c == u"}":
                nivel -= 1
                if nivel == 0:
                    j += 1
                    break
        j += 1
    txt = D[i:j]
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r'"\s*\+\s*\n\s*"', "", txt)                 # junta "a" + "b"
    txt = re.sub(r'([\{,]\s*)"?([A-Za-zÀ-ÿ_0-9]+)"?\s*:', r'\1"\2":', txt)
    txt = re.sub(r",(\s*[\}\]])", r"\1", txt)
    return json.loads(txt)


# ⚠️⚠️ A ENTIDADE HTML TAMBÉM É MARCAÇÃO, e isto foi lição paga (15/set/2026,
#    caderno de inglês do 8º ano). O `lp` tirava as TAGS e deixava as
#    ENTIDADES, então a lista de ingredientes da pizza — escrita com `&middot;`
#    para virar o ponto que separa os itens — ia para a fila de gravação como
#    *"Oil and middot Tomato sauce and middot Some onions"*. O portão
#    `_qa/revisor.py` pegou; se não pegasse, a voz teria dito isso à criança.
_ENT = {u"&middot;": u",", u"&nbsp;": u" ", u"&amp;": u" e ", u"&mdash;": u" ",
        u"&ndash;": u" ", u"&hellip;": u" ", u"&quot;": u'"', u"&lt;": u"",
        u"&gt;": u"", u"&#39;": u"'", u"&apos;": u"'"}


def lp(s):
    u"""tira a marcação e deixa o texto do jeito que a voz vai dizer"""
    t = re.sub(r"<[^>]+>", " ", s or u"")
    for _e, _v in _ENT.items():
        t = t.replace(_e, _v)
    t = re.sub(r"\s+", u" ", t)
    # ⚠️ e a tag que vira espaco deixa um vao ANTES da pontuacao ("o cinema ."),
    #    que o `_qa/revisor.py` acusa — com razao: a voz faz a pausa no lugar
    #    errado. Cola a pontuacao de volta na palavra.
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    # ⚠️ E A VIRGULA DA PAUSA PODE ENCOSTAR NUMA QUE JA EXISTIA (15/set/2026):
    #    a frase "My dad, ___ travels a lot" virou "My dad,, travels a lot" —
    #    duas virgulas coladas, que o Edge TTS le como uma pausa estranha e
    #    longa demais. Uma so, sempre.
    t = re.sub(r",\s*,+", u",", t)
    return t.strip()


def ch(w):
    return re.sub(r"[^a-z]", "",
                  unicodedata.normalize("NFKD", w.lower())
                  .encode("ascii", "ignore").decode())


F = collections.OrderedDict()


def p(k, v):
    F[k] = v


# ---------------------------------------------------------------------------
# AS FALAS DO MOTOR — estas toda folha viva tem
# ---------------------------------------------------------------------------
p(u"folhaPronta", u"Folha pronta! Muito bem.")

# ⚠️ ESTA FALA FALTAVA E O APP A PEDIA — medido em 21/set/2026, depois de o
#    Marcos trazer da sala *"as palavras estão sendo ditas erradas"*. O
#    `falar()` volta CALADO quando a chave não existe: era silêncio no lugar
#    exato em que a criança espera ser elogiada.
p(u"fim", u"Você chegou ao fim da máquina de trocar sílabas! Agora você sabe que trocar, tirar, juntar ou inverter um pedaço faz nascer uma palavra nova. Olhe as palavras à sua volta e veja quantas mudam com um pedaço só.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"monte", u"Toque nas letras embaralhadas para montar a palavra.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque num pedaço ali embaixo. Depois toque na "
                    u"gaveta dele.")
p(u"vozOn", u"A narração está ligada!")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por folha, lendo os DADOS do index.html.
#
# ⚠️ A DICA NUNCA DIZ A RESPOSTA. Ela manda olhar uma pista ou faz outra
#    pergunta. Responder no segundo erro é tirar da criança a única chance de
#    pensar de novo.
# ⚠️ E EM 2º ANO A DICA É CURTA: sete anos não sustentam frase comprida vinda de
#    um alto-falante enquanto olham a tela.
# ---------------------------------------------------------------------------
ESC = bloco(u"ESC")
JUN = bloco(u"JUN")
COR_ = bloco(u"COR_")
ORD = bloco(u"ORD")
DUAS = bloco(u"DUAS")
BANCO = bloco(u"BANCO")
MAR = bloco(u"MAR")
REM = bloco(u"REM")
TRO = bloco(u"TRO")
DEN = bloco(u"DEN")
TIRA = bloco(u"TIRA")
INV = bloco(u"INV")
ACR = bloco(u"ACR")
FIM = bloco(u"FIM")
COD = bloco(u"COD")
PON = bloco(u"PON")
GAV = bloco(u"GAV")
FRAS = bloco(u"FRAS")
DIT = bloco(u"DIT")
CART = bloco(u"CART")

p(u"capa", u"A Máquina de Trocar Sílabas. Trinta e cinco folhas para tirar, "
           u"trocar e virar pedaços de palavra. Escreva o seu nome ali embaixo "
           u"e toque em Começar.")

# ---- 1 e 2 — qual final forma a palavra ----
p(u"p1enun", u"Folha um. Olhe a figura e ouça. Qual dos dois pedaços termina a "
             u"palavra?")
p(u"p2enun", u"Folha dois. Agora são três pedaços para escolher. Diga a palavra "
             u"baixinho antes.")
for k, E in ESC.items():
    pg = u"1" if k[0] == u"a" else u"2"
    p(u"esc_" + k, E[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! A palavra é " + E[u"p"] + u".")
    p(u"dica" + pg + u"_" + k, u"Diga a palavra devagar e pare no fim dela. Qual "
                               u"é o som que sai?")

# ---- 3 e 4 — um pedaço, três palavras ----
p(u"p3enun", u"Folha três. Um pedaço só serve para três palavras. Junte-o a cada "
             u"final e veja o que aparece.")
p(u"p4enun", u"Folha quatro. As palavras agora são compridas, mas o pedaço da "
             u"frente continua sendo o mesmo.")
for k, J in JUN.items():
    pg = u"3" if k[0] == u"c" else u"4"
    p(u"certo" + pg + u"_" + k, u"Olhe só: com esse pedaço saíram três palavras. "
                                + u", ".join(J[u"r"]) + u".")
    p(u"dica" + pg + u"_" + k, u"Toque em cada linha e escute o que sai. Vale "
                               u"para as três.")

# ---- 5 — a cor mostra o par ----
p(u"p5enun", u"Folha cinco. Nos primeiros, a bolinha da mesma cor mostra o par. "
             u"Depois a bolinha some, e você já vai saber.")
for k, C in COR_.items():
    p(u"cor_" + k, C[u"p"] + u".")
    p(u"certo5_" + k, u"Isso mesmo! A palavra é " + C[u"p"] + u".")
    p(u"dica5_" + k, u"Escute a palavra inteira de novo e pare no fim dela.")

# ---- 6 e 7 — ponha as sílabas na ordem ----
p(u"p6enun", u"Folha seis. As sílabas se embaralharam. Toque nelas na ordem para "
             u"a palavra voltar.")
p(u"p7enun", u"Folha sete. Agora são três pedaços. A figura confere para você.")
for k, O in ORD.items():
    pg = u"6" if k[0] == u"f" else u"7"
    p(u"ord_" + k, O[u"r"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! A palavra montada é " + O[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Diga a palavra devagar. Qual é o pedaço que "
                               u"começa?")

# ---- 8 — duas ordens, uma só é palavra ----
p(u"p8enun", u"Folha oito. Os mesmos pedaços, em duas ordens. Só uma é palavra "
             u"de verdade. Qual?")
for k, Dz in DUAS.items():
    p(u"dua_" + k, Dz[u"r"] + u".")
    p(u"certo8_" + k, u"Isso! Só " + Dz[u"r"] + u" existe de verdade.")
    p(u"dica8_" + k, u"Leia as duas em voz alta. Uma delas você nunca ouviu.")

# ---- 9 — as gotas de chuva ----
p(u"p9enun", u"Folha nove. As sílabas caíram como gotas de chuva. Pegue as que "
             u"formam cada palavra, na ordem.")
for k, B in BANCO[u"pal"].items():
    p(u"ban_" + k, B[u"r"] + u".")
    p(u"certo9_" + k, u"Isso! A palavra é " + B[u"r"] + u".")
    p(u"dica9_" + k, u"Escute a palavra de novo e procure só o primeiro pedaço.")

# ---- 10, 11 e 12 — ache os pedaços certos ----
p(u"p10enun", u"Folha dez. São três pedaços e só dois servem. Marque os certos e "
              u"toque em Conferir.")
p(u"p11enun", u"Folha onze. Agora há muitos pedaços sobrando. Diga a palavra "
              u"devagar e marque só os que você ouvir.")
p(u"p12enun", u"Folha doze. Cuidado: agora os pedaços errados são parecidos com "
              u"os certos.")
for k, M in MAR.items():
    pg = {u"j": u"10", u"k": u"11", u"l": u"12"}[k[0]]
    p(u"mar_" + k, M[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Muito bem! " + M[u"p"] + u" é feita desses "
                                u"pedaços: " + u", ".join(M[u"g"]) + u".")
    p(u"dica" + pg + u"_" + k, u"Bata uma palma para cada pedaço da palavra e "
                               u"conte quantos são.")

# ---- 13 e 14 — tire uma letra ----
p(u"p13enun", u"Folha treze. Tire uma letra do começo e aparece outra palavra. "
              u"Toque na letra que sai.")
p(u"p14enun", u"Folha catorze. Tem sempre uma palavra escondida dentro da outra. "
              u"Ache a letra que está sobrando.")
for k, X in REM.items():
    pg = u"13" if k[0] == u"m" else u"14"
    p(u"rem_" + k, X[u"de"] + u". " + X[u"r"] + u".")
    p(u"certo" + pg + u"_" + k, u"Olhe só: sem aquela letra, " + X[u"de"] +
                                u" virou " + X[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute as duas palavras de novo. Qual é o som "
                               u"que some?")

# ---- 15 e 16 — troque a primeira letra ----
p(u"p15enun", u"Folha quinze. O fim da palavra fica parado. Troque só a letra da "
              u"frente e veja quantas palavras saem.")
p(u"p16enun", u"Folha dezesseis. Outra terminação parada, e de novo três "
              u"palavras dentro dela.")
for k, T in TRO.items():
    pg = u"15" if k[0] == u"o" else u"16"
    p(u"certo" + pg + u"_" + k, u"Saíram três palavras que terminam igual: " + u", ".join(T[u"r"]) + u".")
    p(u"dica" + pg + u"_" + k, u"Toque em cada linha e escute a palavra que sai.")

# ---- 17 — troque a letra de dentro ----
p(u"p17enun", u"Folha dezessete. Agora a letra que muda está marcada. Escolha a "
              u"que entra no lugar dela.")
_LETRAS = {}
for k, Q in DEN.items():
    p(u"den_" + k, Q[u"p"] + u".")
    p(u"certo17_" + k, u"Isso! " + Q[u"de"] + u" virou " + Q[u"p"] + u".")
    p(u"dica17_" + k, u"Escute a palavra nova outra vez e repare no começo dela.")
    for L in Q[u"ops"]:
        _LETRAS[L.lower()] = 1
# ⚠️ LETRA SOLTA A VOZ DIZ PELO NOME, e é isso que se quer aqui: a criança
#    precisa saber QUE LETRA é, não que som ela faz. O portão `_qa/falas.py`
#    reclama de "som S" solto, não do nome da letra dentro de uma frase.
for L in sorted(_LETRAS):
    p(u"let_" + L, u"Letra " + L.upper() + u".")

# ---- 18 e 19 — a tira ----
p(u"p18enun", u"Folha dezoito. Na janela, o fim L H A está parado. Encaixe o "
              u"pedaço da tira que forma a palavra pedida.")
p(u"p19enun", u"Folha dezenove. Agora o fim parado é N H O. A tira mudou; o "
              u"jeito é o mesmo.")
for k, T in TIRA.items():
    pg = u"18" if k[0] == u"r" else u"19"
    p(u"certo" + pg + u"_" + k, u"Encaixou! A palavra ficou " + T[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute a palavra de novo e repare só no começo "
                               u"dela.")

# ---- 20, 21 e 22 — troque os pedaços de lugar ----
p(u"p20enun", u"Folha vinte. Puxe o pedaço de trás para a frente, e olhe o que "
              u"nasce.")
p(u"p21enun", u"Folha vinte e um. De novo: os mesmos dois pedaços, na ordem "
              u"trocada.")
p(u"p22enun", u"Folha vinte e dois. Estas são mais difíceis: o segundo pedaço é "
              u"maior. Diga a palavra ao contrário antes de puxar.")
for k, X in INV.items():
    pg = {u"t": u"20", u"u": u"21", u"v": u"22"}[k[0]]
    p(u"inv_" + k, X[u"de"] + u". " + X[u"r"] + u".")
    p(u"certo" + pg + u"_" + k, u"Que descoberta! " + X[u"de"] + u" de trás para "
                                u"frente virou " + X[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Diga os dois pedaços na ordem trocada e escute o "
                               u"que sai.")

# ---- 23 e 24 — acrescente um pedaço ----
p(u"p23enun", u"Folha vinte e três. Ponha um pedaço no fim e a palavra vira "
              u"outra. Ouça qual é.")
p(u"p24enun", u"Folha vinte e quatro. Agora o pedaço entra no começo. Ouça a "
              u"palavra inteira antes de escolher.")
for k, A in ACR.items():
    pg = u"23" if k[0] == u"w" else u"24"
    p(u"acr_" + k, A[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! " + A[u"base"] + u" com esse pedaço virou "
                                + A[u"p"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute a palavra nova e a antiga. O que foi que "
                               u"entrou?")

# ---- 25 e 26 — o fim de duas, uma nova ----
p(u"p25enun", u"Folha vinte e cinco. Pegue o último pedaço de cada palavra. Os "
              u"dois juntos formam uma palavra nova.")
p(u"p26enun", u"Folha vinte e seis. Mais três. Diga cada palavra devagar e pare "
              u"no fim dela.")
for k, X in FIM.items():
    pg = u"25" if k[0] == u"y" else u"26"
    p(u"fim_" + k, X[u"a"] + u". " + X[u"b"] + u". " + X[u"r"] + u".")
    p(u"certo" + pg + u"_" + k, u"Olhe que bonito: o fim de " + X[u"a"] + u" com o "
                                u"fim de " + X[u"b"] + u" deu " + X[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Diga a palavra devagar e segure o último pedaço "
                               u"na boca.")

# ---- 27 a 30 — o código das sílabas ----
p(u"p27enun", u"Folha vinte e sete. Cada pedaço ganhou um número. Siga os "
              u"números e a palavra aparece.")
p(u"p28enun", u"Folha vinte e oito. Outro quadro, e agora há palavras de três "
              u"pedaços.")
p(u"p29enun", u"Folha vinte e nove. Agora as palavras são compridas: quatro "
              u"números cada uma.")
p(u"p30enun", u"Folha trinta. Neste quadro os pedaços têm duas consoantes "
              u"juntas. Olhe bem: B R A e C R A mudam por uma letra só.")
_PGCOD = {u"q27": u"27", u"q28": u"28", u"q29": u"29", u"q30": u"30"}
for qk, Q in COD.items():
    pg = _PGCOD[qk]
    for k, P_ in Q[u"pal"].items():
        p(u"certo" + pg + u"_" + k, u"Decifrou! A palavra é " + P_[u"r"] + u".")
        p(u"dica" + pg + u"_" + k, u"Procure no quadro o número que vem agora, e "
                                   u"toque nele.")

# ---- 31 — faltam as duas pontas ----
p(u"p31enun", u"Folha trinta e um. Só o pedaço do meio ficou. Ponha o do começo e "
              u"o do fim, nessa ordem.")
for k, P_ in PON.items():
    p(u"pon_" + k, P_[u"r"] + u".")
    p(u"certo31_" + k, u"Isso! A palavra inteira é " + P_[u"r"] + u".")
    p(u"dica31_" + k, u"Escute a palavra de novo. Por qual pedaço ela começa?")

# ---- 32 — começo, meio e fim ----
p(u"p32enun", u"Folha trinta e dois. Em que lugar da palavra mora cada pedaço? "
              u"Leve cada um para a gaveta dele.")
_NOMEGAV = {u"ini": u"Nesta gaveta vai o pedaço que abre a palavra, o primeiro "
                    u"de todos.",
            u"mei": u"Nesta gaveta vai o pedaço do meio, o que não é nem o "
                    u"primeiro nem o último.",
            u"fim": u"Nesta gaveta vai o pedaço que fecha a palavra, o último "
                    u"de todos."}
for C in GAV[u"gA"][u"cols"]:
    p(u"gav_gA_" + C[u"k"], _NOMEGAV[C[u"k"]])
for k, Pl in GAV[u"gA"][u"pal"].items():
    p(u"diz2_gA_" + k, Pl[u"p"] + u".")
    p(u"certo32_" + k, u"Isso mesmo! Esse pedaço mora ali.")
    p(u"dica32_" + k, u"Diga a palavra inteira e bata palma em cada pedaço. Em "
                      u"qual palma ele cai?")

# ---- 33 — a palavra entra na frase ----
p(u"p33enun", u"Folha trinta e três. Qual palavra falta na frase? Monte a "
              u"palavra tocando nas letras, ou digite no seu teclado.")
for k, F_ in FRAS.items():
    # ⚠️ A LACUNA NÃO SE NARRA: a voz lê a frase inteira com a palavra dentro,
    #    senão a criança ouve um buraco e perde o sentido.
    p(u"fra_" + k, lp(F_[u"a"]) + u" " + F_[u"w"] + u" " + lp(F_[u"z"]))
    p(u"certo33_" + k, u"Isso! " + lp(F_[u"a"]) + u" " + F_[u"w"] + u" " + lp(F_[u"z"]))
    p(u"dica33_" + k, u"Escute a frase inteira de novo e pense na figura.")

# ---- 34 — o ditado dos três lugares ----
p(u"p34enun", u"Folha trinta e quatro. Ouça o pedaço ditado. Ele cabe em três "
              u"palavras da cartela: no começo, no meio e no fim. Marque as "
              u"três.")
for k, Dt in DIT.items():
    p(u"certo34_" + k, u"Muito bem! O mesmo pedaço serviu em " +
                       u", ".join([o[u"w"] for o in Dt[u"ok"]]) + u".")
    p(u"dica34_" + k, u"Ponha o pedaço no buraco e escute: deu palavra de "
                      u"verdade?")

# ---- 35 — o cartaz que você leva ----
p(u"p35enun", u"Folha trinta e cinco. Você já sabe fazer tudo isto. Agora os "
              u"nomes das quatro mexidas: leve cada exemplo para a linha dele.")
for L in CART[u"linhas"]:
    p(u"cart_" + L[u"k"], L[u"t"] + u" é " + L[u"d"] + u". Por exemplo: " +
                          L[u"e"].replace(u"→", u"vira") + u".")
for k, X in CART[u"exem"].items():
    p(u"exe_" + k, X[u"p"] + u".")
    p(u"certo35_" + k, u"Isso mesmo! Esse é um exemplo daquela linha.")
    p(u"dica35_" + k, u"Leia a linha de novo e veja o que ela manda fazer com o "
                      u"pedaço.")

# ==============================================================================
#  AS SÍLABAS FALADAS — e este bloco é a razão de o caderno não soletrar
#
#  ⚠️⚠️ A VOZ NÃO LÊ SOM, LÊ PALAVRA. Entregue "SA" a ela e ela soletra
#     "esse-á"; "VA" vira "vê-á". O que funciona é gravar a PALAVRA INTEIRA,
#     alinhar letra a letra com o `ctc-forced-aligner` e CORTAR a sílaba de
#     dentro dela — `_padrao/silabas_voz.py`, no `entregar.yml`.
#  ⚠️ E NÃO HÁ FALA DE RESERVA POR SÍLABA: faltando o recorte, o app diz a
#     PALAVRA INTEIRA. Reserva sintetizada seria o defeito voltando calado.
# ==============================================================================
_RECUSADAS = []
_SIL_DE = {}
_MAPA_SIL = {}


def _reg(palavra, silabas):
    u"""⚠️ A LISTA TEM DE ESTAR NA ORDEM DA PALAVRA (o alinhador corta pelos
    limites das letras), e ganha a partição MAIS FINA."""
    silabas = list(silabas)
    if u"".join(silabas).upper() != palavra.upper():
        _RECUSADAS.append((palavra, silabas))
        return
    velha = _SIL_DE.get(palavra.lower())
    if velha and len(velha) >= len(silabas):
        return
    _SIL_DE[palavra.lower()] = silabas


def _ordena(palavra, embaralhadas):
    resto, saida, alvo = list(embaralhadas), [], palavra.upper()
    while alvo:
        for _i, _sb in enumerate(resto):
            if alvo.startswith(_sb.upper()):
                saida.append(_sb); alvo = alvo[len(_sb):]; resto.pop(_i); break
        else:
            return None
    return saida if not resto else None


# as palavras deste caderno, com as sílabas que os DADOS já declaram
for _E in ESC.values():
    _reg(_E[u"p"], [_E[u"i"], _E[u"r"]])
for _C in COR_.values():
    _reg(_C[u"p"], [_C[u"i"], _C[u"r"]])
for _O in ORD.values():
    _o = _ordena(_O[u"r"], _O[u"s"])
    if _o:
        _reg(_O[u"r"], _o)
for _B in BANCO[u"pal"].values():
    _reg(_B[u"r"], _B[u"s"])
for _M in MAR.values():
    _reg(_M[u"p"], _M[u"g"])
for _T in TIRA.values():
    _reg(_T[u"r"], [_T[u"ini"], _T[u"fim"]])
for _I in INV.values():
    _reg(_I[u"de"], _I[u"s"])
    _reg(_I[u"r"], [_I[u"s"][1], _I[u"s"][0]])
for _F in FIM.values():
    _reg(_F[u"a"], _F[u"sa"])
    _reg(_F[u"b"], _F[u"sb"])
    _reg(_F[u"r"], [_F[u"sa"][-1], _F[u"sb"][-1]])
for _Q in COD.values():
    for _P in _Q[u"pal"].values():
        _reg(_P[u"r"], [_Q[u"quadro"][_n - 1] for _n in _P[u"n"]])
for _P2 in PON.values():
    _reg(_P2[u"r"], [_P2[u"ini"], _P2[u"meio"], _P2[u"fim"]])
for _J in JUN.values():
    for _n, _r in enumerate(_J[u"r"]):
        _reg(_r, [_J[u"i"], _J[u"f"][_n]])
for _A in ACR.values():
    _reg(_A[u"p"], [_A[u"r"], _A[u"base"]] if _A[u"onde"] == u"começo"
                   else [_A[u"base"], _A[u"r"]])

# ⚠️ AS DISTRATORAS NÃO MORAM EM PALAVRA NENHUMA DO CADERNO — e são justamente
#    as que a criança toca para DESCARTAR. Sem casa, o botão delas ficava MUDO.
#    Cada uma ganha aqui uma PALAVRA-CARREGADORA: palavra de verdade, curta, que
#    existe só para ser gravada e cortada. A criança nunca ouve a palavra
#    inteira — ouve o pedaço.
_CARREGADORAS = {
    u"DEDO": [u"DE", u"DO"],   u"DIA": [u"DI", u"A"],     u"LUA": [u"LU", u"A"],
    u"MINUTO": [u"MI", u"NU", u"TO"], u"MOLA": [u"MO", u"LA"],
    u"PENA": [u"PE", u"NA"],   u"RIO": [u"RI", u"O"],     u"SINO": [u"SI", u"NO"],
    u"TIJOLO": [u"TI", u"JO", u"LO"], u"VIDRO": [u"VI", u"DRO"],
    u"FEVEREIRO": [u"FE", u"VE", u"REI", u"RO"], u"CANECA": [u"CA", u"NE", u"CA"],
    u"MUDA": [u"MU", u"DA"],   u"SELO": [u"SE", u"LO"],   u"RUA": [u"RU", u"A"],
    u"NUVEM": [u"NU", u"VEM"], u"REDE": [u"RE", u"DE"],   u"SOPA": [u"SO", u"PA"],
    u"BARCO": [u"BAR", u"CO"], u"PORTA": [u"POR", u"TA"], u"TEIA": [u"TEI", u"A"],
    u"PARTE": [u"PAR", u"TE"], u"PRESENTE": [u"PRE", u"SEN", u"TE"],
    u"PLACA": [u"PLA", u"CA"], u"CREME": [u"CRE", u"ME"], u"DRAGÃO": [u"DRA", u"GÃO"],
    u"BRINCO": [u"BRIN", u"CO"], u"LIVRO": [u"LI", u"VRO"], u"TROCO": [u"TRO", u"CO"],
    u"GRAMA": [u"GRA", u"MA"], u"BRAVO": [u"BRA", u"VO"], u"NINHO": [u"NI", u"NHO"],
    u"CHORÃO": [u"CHO", u"RÃO"], u"NADA": [u"NA", u"DA"], u"ELEFANTE": [u"E", u"LE", u"FAN", u"TE"],
    u"SORTE": [u"SOR", u"TE"], u"NOITE": [u"NOI", u"TE"], u"TESOURO": [u"TE", u"SOU", u"RO"],
    u"BOLSA": [u"BOL", u"SA"], u"MEIA": [u"MEI", u"A"],
    u"BEBIDA": [u"BE", u"BI", u"DA"], u"BRIGA": [u"BRI", u"GA"],
    u"CADEIRA": [u"CA", u"DEI", u"RA"], u"ARANHA": [u"A", u"RA", u"NHA"],
    u"PESCA": [u"PES", u"CA"], u"TORTA": [u"TOR", u"TA"],
}
for _cw in sorted(_CARREGADORAS):
    _reg(_cw, _CARREGADORAS[_cw])


def _achaSilaba(s):
    u"""a palavra de onde a sílaba será recortada: ganha a MAIS CURTA, porque
    quanto menos letras a gravação tem, menos o alinhador tem onde errar."""
    cand = [_w for _w in sorted(_SIL_DE) if s in _SIL_DE[_w]]
    if not cand:
        return None
    _w = min(cand, key=lambda w: (len(_SIL_DE[w]), len(w), w))
    return [_w, _SIL_DE[_w].index(s)]


# toda sílaba que o app pode falar sozinha
_soltas = set()
for _E in ESC.values():
    _soltas.update(_E[u"ops"])
for _C in COR_.values():
    _soltas.update(_C[u"ops"])
for _O in ORD.values():
    _soltas.update(_O[u"s"])
for _M in MAR.values():
    _soltas.update(_M[u"g"]); _soltas.update(_M[u"d"])
for _T in TIRA.values():
    _soltas.update(_T[u"tira"])
for _A in ACR.values():
    _soltas.update(_A[u"ops"])
for _F in FIM.values():
    _soltas.update(_F[u"sa"]); _soltas.update(_F[u"sb"])
for _Q in COD.values():
    _soltas.update(_Q[u"quadro"])
for _P2 in PON.values():
    _soltas.update(_P2[u"ops"]); _soltas.add(_P2[u"meio"])
for _J in JUN.values():
    _soltas.add(_J[u"i"])
_soltas.update(BANCO[u"sil"])
for _Dt in DIT.values():
    _soltas.add(_Dt[u"sb"])
# ⚠️ sílaba com espaço ou vazia não existe — é lixo de leitura, não peça
_soltas = set(s for s in _soltas if s and u" " not in s)

# ⚠️⚠️ SÍLABA DE UM PEDAÇO SÓ TEM DE SER RECORTADA; PEDAÇO DE DOIS OU MAIS, NÃO.
#    A voz soletra "SA" porque é UMA emissão que ela não reconhece como palavra;
#    mas "LADO", "MATE", "NITO" ela lê como leria qualquer palavra, porque têm
#    duas vogais e um desenho de palavra. Então os pedaços compridos ganham fala
#    NORMAL (`pal_`) e os curtos, recorte. Quem confere que a distinção vale é a
#    2ª medida do `_qa/silabas.py`, que compara as durações.
def _grupos_de_vogal(s):
    v, n, antes = u"AEIOUÁÀÂÃÉÊÍÓÔÕÚ", 0, False
    for c in s.upper():
        agora = c in v
        if agora and not antes:
            n += 1
        antes = agora
    return n


_ORFAS, _COMPRIDAS = [], []
for _s in sorted(_soltas):
    _achou = _achaSilaba(_s)
    if _achou:
        _MAPA_SIL[_s] = _achou
    elif _grupos_de_vogal(_s) > 1:
        _COMPRIDAS.append(_s)
        p(u"pal_" + ch(_s), _s.upper() + u".")
    else:
        _ORFAS.append(_s)

# e a PALAVRA INTEIRA de cada uma precisa existir como fala: é dela que o
# recorte sai, e é ela que o app diz quando o recorte falta
for _w in sorted(_SIL_DE):
    p(u"pal_" + ch(_w), _w.upper() + u".")

# ⚠️⚠️ O GUARDA DO `F`: basta um `for k, F in ALGO.items()` para o dicionário das
#    falas virar um item solto e tudo o que foi escrito sumir, sem erro nenhum.
if not isinstance(F, dict):
    raise SystemExit(u"⛔ o `F` deixou de ser o dicionario das falas.")
_ruins = [k for k, v in F.items() if not isinstance(v, type(u""))]
if _ruins:
    raise SystemExit(u"⛔ falas que nao sao texto: %s" % u", ".join(_ruins[:6]))

# ⚠️⚠️ FALA DE DUAS PALAVRAS SAI TORTA — medido pelo OUVIDO da entrega: de
#    "Isso! CAVALO." ouviu-se só "isso". As exceções são NOMEADAS: são as falas
#    que a criança ouve ao TOCAR numa peça, e que por isso têm de dizer a peça e
#    MAIS NADA.
_SO_A_PECA = (u"pal_", u"esc_", u"cor_", u"ord_", u"dua_", u"ban_", u"mar_",
              u"rem_", u"den_", u"inv_", u"acr_", u"fim_", u"pon_", u"exe_",
              u"let_", u"diz2_", u"fra_")
_curtas = [(k, v) for k, v in F.items()
           if len(v.split()) < 3 and not k.startswith(_SO_A_PECA)]
if _curtas:
    raise SystemExit(u"⛔ %d fala(s) com menos de 3 palavras:\n   %s"
                     % (len(_curtas), u"\n   ".join(
                         u"%s -> %r" % (k, v) for k, v in _curtas[:8])))

# ---------------------------------------------------------------------------
# A SAÍDA
# ---------------------------------------------------------------------------
def chave(s):
    u"""O nome do mp3 sai do TEXTO, não da chave da fala — assim duas chaves que
    dizem a mesma frase gravam um arquivo só."""
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for c in s:
        hh = ((hh * 33) ^ ord(c)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    txt = F[k]
    if not txt:
        continue
    c = chave(txt)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": txt, u"voz": VOZ})

html = io.open(CAM, encoding=u"utf-8").read()
blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)

# ⭐ o `silabas.json` é o que o `entregar.yml` lê para cortar cada sílaba de
#    dentro do mp3 da palavra inteira, e o `SILMAP` é o que o app usa para saber
#    de qual palavra veio cada pedaço. Uma fonte só para os dois.
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ,
                u"palavras": dict((w, _SIL_DE[w]) for w in sorted(_SIL_DE))},
               ensure_ascii=False, indent=1))
blocoS = (u"/*SILMAP-INI*/var SILMAP = "
          + json.dumps(_MAPA_SIL, ensure_ascii=False, sort_keys=True) + u";/*SILMAP-FIM*/")
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/", lambda m: blocoS, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)
io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
print(u"FALAS: %d chaves; falas.json: %d fala(s) para gravar; "
      u"silabas: %d palavra(s) para recortar, %d silaba(s) no mapa"
      % (len(F), len(falas), len(_SIL_DE), len(_MAPA_SIL)))
if _COMPRIDAS:
    print(u"   %d pedaco(s) de duas silabas falam inteiros (a voz os le certo): %s"
          % (len(_COMPRIDAS), u", ".join(_COMPRIDAS)))
if _ORFAS:
    print(u"   \u26a0\ufe0f %d silaba(s) SEM palavra de origem (o app dira a palavra "
          u"inteira): %s" % (len(_ORFAS), u", ".join(_ORFAS)))
if _RECUSADAS:
    print(u"   \u26a0\ufe0f %d lista(s) recusada(s) por nao formarem a palavra: %s"
          % (len(_RECUSADAS), u", ".join(
              u"%s=%s" % (w, u"-".join(sl)) for w, sl in _RECUSADAS[:8])))
