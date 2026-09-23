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
PREFIXO = u"gv_"                     # <- o prefixo desta atividade
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
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"monte", u"Toque nas letras embaralhadas para montar a palavra.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"A narração está ligada!")


# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por folha, lendo os DADOS do index.html.
#
# ⚠️ A DICA NUNCA DIZ A RESPOSTA. Ela manda olhar uma pista ou faz outra
#    pergunta. Responder no segundo erro é tirar da criança a única chance de
#    pensar de novo.
# ⚠️ E EM 2º ANO A DICA É CURTA: sete anos não sustentam frase comprida vinda
#    de um alto-falante enquanto olham a tela.
# ---------------------------------------------------------------------------
BAT = bloco(u"BAT")
COR_ = bloco(u"COR")
VOG = bloco(u"VOG")
LET = bloco(u"LET")
QZ = bloco(u"QZ")
GAV = bloco(u"GAV")
FLOR = bloco(u"FLOR")
LIGA = bloco(u"LIGA")
ORD = bloco(u"ORD")
FAL = bloco(u"FAL")
JUN = bloco(u"JUN")
MAR = bloco(u"MAR")
CACA = bloco(u"CACA")
TRI = bloco(u"TRI")
CRZ = bloco(u"CRZ")
CON = bloco(u"CON")
DIT = bloco(u"DIT")
FRAS = bloco(u"FRAS")
TXT = bloco(u"TXT")
CANT = bloco(u"CANT")
BANCO = bloco(u"BANCO")
DESA = bloco(u"DESA")
CART = bloco(u"CART")

NCL = {u"m": u"uma sílaba", u"d": u"duas sílabas",
       u"t": u"três sílabas", u"p": u"quatro ou mais sílabas"}
NUM = {1: u"uma", 2: u"duas", 3: u"três", 4: u"quatro", 5: u"cinco"}


def ple(n):
    u"""'1 sílaba' x '2 sílabas' — a voz erra se o número vier solto."""
    return NUM.get(n, unicode(n) if str is bytes else str(n)) + \
        (u" sílaba" if n == 1 else u" sílabas")


# ---- o motor, com o conteúdo deste caderno ----
p(u"capa", u"O Armário das Quatro Gavetas. Trinta e cinco folhas sobre a "
           u"sílaba. Escreva o seu nome ali embaixo e toque em Começar.")
p(u"fim", u"Você chegou ao fim! Agora olhe para o seu nome: quantas vezes a "
          u"sua boca abre para dizer ele? E o nome da pessoa que está do seu "
          u"lado, é maior ou menor que o seu?")
p(u"pegue_lapis", u"Primeiro pegue uma canetinha ali em cima. Depois toque na "
                  u"palavra.")
p(u"caca_toque", u"Toque primeiro na casa do começo da palavra.")
for _n in (1, 2, 3, 4, 5):
    p(u"num_%d" % _n, ple(_n) + u".")
for _k, _t in NCL.items():
    p(u"gavn_" + _k, _t[0].upper() + _t[1:] + u".")
    p(u"lapis_" + _k, u"Canetinha de " + _t + u".")

# ---- 1 e 2 — bater palma ----
p(u"p1enun", u"Folha um. Toque no alto-falante e diga a palavra em voz alta. "
             u"Pinte uma bolinha cada vez que a sua boca abrir.")
p(u"p2enun", u"Folha dois. Agora as palavras são maiores. Diga em voz alta e "
             u"pinte uma bolinha para cada vez que a boca abre.")
for k, B in BAT.items():
    p(u"diz_" + k, u", ".join(B[u"s"]) + u". " + B[u"p"] + u".")
    n = len(B[u"s"])
    pg = u"1" if k[0] == u"b" else u"2"
    p(u"certo" + pg + u"_" + k, u"Isso! " + B[u"p"] + u" tem " + ple(n) + u".")
    p(u"dica" + pg + u"_" + k, u"Diga de novo bem devagar, com a mão embaixo do "
                               u"queixo. Cada vez que o queixo desce é uma palma.")

# ---- 3 e 4 — cortar ----
p(u"p3enun", u"Folha três. Diga a palavra devagar e toque na fresta onde ela "
             u"se parte em dois pedaços.")
p(u"p4enun", u"Folha quatro. Estas são mais difíceis. Algumas se partem em "
             u"três pedaços: toque em todas as frestas.")
for k, C in COR_.items():
    pg = u"3" if k[0] == u"d" else u"4"
    p(u"cor_" + k, C[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso mesmo! " + C[u"p"] + u" se parte em "
                                + ple(len(C[u"g"]) + 1) + u".")
    p(u"dica" + pg + u"_" + k, u"Diga a palavra bem devagar. Onde a sua boca "
                               u"para um pouquinho, é ali que ela se parte.")

# ---- 5 — a vogal ----
p(u"p5enun", u"Folha cinco. Em cada pedaço há uma vogal: é ela que faz a boca "
             u"abrir. Toque na vogal de cada pedaço.")
for k, V in VOG.items():
    # ⚠️ A PALAVRA INTEIRA, não a lista de pedaços: "BO, LA." sai da voz
    #    como "bê-ó, éle-á". Os pedaços, quem os diz é o `falarSilaba`.
    p(u"vog_" + k, u"".join(V[u"s"]) + u".")
    p(u"certo5_" + k, u"Isso! Toda sílaba tem uma vogal dentro.")
    p(u"dica5_" + k, u"As vogais são A, E, I, O e U. Procure uma delas nesse "
                     u"pedaço.")

# ---- 6 e 7 — letra x sílaba ----
p(u"p6enun", u"Folha seis. Quantas letras tem a palavra? E quantas sílabas? "
             u"Repare: o número não é o mesmo.")
p(u"p7enun", u"Folha sete. A mesma palavra em duas linhas: em cima as letras, "
             u"embaixo as sílabas. Quantas caixas tem a linha de baixo?")
for k, L in LET.items():
    p(u"let_" + k, L[u"p"] + u".")
    for pg in (u"6", u"7", u"27"):
        p(u"certo" + pg + u"_" + k,
          u"Isso! " + L[u"p"] + u" tem %d letras e " % L[u"L"] + ple(L[u"S"]) + u".")
        p(u"dica" + pg + u"_" + k, u"Conte batendo palma, não olhando as "
                                   u"letras. Letra e sílaba não são a mesma coisa.")

# ---- 8 — qual está certo ----
p(u"p8enun", u"Folha oito. Três jeitos de partir a mesma palavra. Só um está "
             u"certo: qual?")
for k, Q in QZ.items():
    p(u"qz_" + k, Q[u"p"] + u".")
    for n, t in enumerate(Q[u"ops"]):
        p(u"qzop_%s_%d" % (k, n), t.replace(u"-", u", ") + u".")
    p(u"certo8_" + k, u"Isso! " + Q[u"ops"][Q[u"r"]].replace(u"-", u", ") + u".")
    p(u"dica8_" + k, u"Diga cada um deles em voz alta. Um vai soar estranho na "
                     u"sua boca.")

# ---- 9 a 12 — as gavetas ----
p(u"p9enun", u"Folha nove. Diga a palavra e bata palma. Guarde cada uma na "
             u"gaveta do número de palmas que você bateu.")
p(u"p10enun", u"Folha dez. Agora o armário tem quatro gavetas. A última é das "
              u"palavras mais compridas: quatro ou mais palmas.")
p(u"p11enun", u"Folha onze. Este é o armário de roupa. Guarde cada peça na "
              u"gaveta certa.")
p(u"p12enun", u"Folha doze. E este é o da mochila. Atenção: uma delas tem "
              u"cinco sílabas, e cinco também é quatro ou mais.")
_PG = {u"gA": u"9", u"gB": u"10", u"gC": u"11", u"gD": u"12"}
for gk, G in GAV.items():
    for C in G[u"cols"]:
        p(u"gav_%s_%s" % (gk, C[u"k"]), u"Gaveta de " + NCL[C[u"k"]] + u".")
    for n, P in G[u"pal"].items():
        p(u"diz2_%s_%s" % (gk, n), P[u"p"] + u".")
        p(u"certo" + _PG[gk] + u"_" + n,
          u"Isso! " + P[u"p"] + u", " + NCL[P[u"c"]] + u".")
        p(u"dica" + _PG[gk] + u"_" + n,
          u"Diga a palavra batendo palma e conte as palmas antes de escolher "
          u"a gaveta.")

# ---- 13 — a flor ----
p(u"p13enun", u"Folha treze. Pegue uma canetinha e pinte a pétala da cor "
              u"certa, conforme a legenda.")
for k, FL in FLOR.items():
    p(u"certo13_" + k, u"Isso! " + FL[u"p"] + u", " + NCL[FL[u"c"]] + u".")
    p(u"dica13_" + k, u"Conte as palmas de " + FL[u"p"] + u" e depois olhe a "
                      u"legenda para ver a cor.")

# ---- 14 — ligar ----
p(u"p14enun", u"Folha catorze. Toque numa palavra da esquerda e depois na "
              u"gaveta dela, à direita.")
for k, L in LIGA.items():
    p(u"lig_" + k, L[u"p"] + u".")
    p(u"ligc_" + k, L[u"c"] + u".")
    p(u"certo14_" + k, u"Isso! " + L[u"p"] + u" tem " + L[u"c"].replace(u"4 ou mais", u"quatro ou mais") + u".")
    p(u"dica14_" + k, u"Bata palma dizendo a palavra e conte.")

# ---- 15 e 16 — montar ----
p(u"p15enun", u"Folha quinze. As sílabas se embaralharam. Toque nelas na ordem "
              u"para a palavra voltar.")
p(u"p16enun", u"Folha dezesseis. Agora são palavras compridas. Diga a palavra "
              u"baixinho antes de começar: ajuda a achar o primeiro pedaço.")
for k, O in ORD.items():
    pg = u"15" if k[0] == u"q" else u"16"
    p(u"ord_" + k, O[u"r"] + u".")
    # ⚠️ A FALA CURTA DEMAIS SAI TORTA, e o ouvido da entrega pegou: de
    #   "Isso! CAVALO." ele ouviu só "isso". Duas palavras soltas não dão
    #   à voz contexto nenhum, e a criança também ganha pouco com elas.
    #   A frase inteira diz o que ela FEZ.
    p(u"certo" + pg + u"_" + k, u"Isso! Você montou a palavra " + O[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute a palavra de novo e pense em qual "
                               u"pedaço ela começa.")

# ---- 17, 18 e 19 — a sílaba que falta ----
p(u"p17enun", u"Folha dezessete. Falta o pedaço do começo. Ouça a palavra "
              u"inteira e escolha.")
p(u"p18enun", u"Folha dezoito. Agora falta o pedaço do meio, o mais difícil de "
              u"ouvir. Diga a palavra devagar.")
p(u"p19enun", u"Folha dezenove. E agora falta o pedaço do fim.")
_ONDE = {u"s": (u"17", u"começo"), u"t": (u"18", u"meio"), u"u": (u"19", u"fim")}
for k, FA in FAL.items():
    pg, onde = _ONDE[k[0]]
    p(u"fal_" + k, FA[u"q"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! A palavra é " + FA[u"q"] + u".")
    p(u"dica" + pg + u"_" + k, u"Diga a palavra inteira e pare no pedaço do " +
                               onde + u". Qual é o som que sai?")
    # ⚠️ AS OPÇÕES NÃO TÊM MAIS FALA SINTETIZADA. Era daqui que saía o
    #    "esse-á" no lugar de SA (Marcos, 16/set/2026). Quem as diz agora é
    #    o `falaDaSilaba`, com o pedaço recortado da palavra inteira.

# ---- 20 — uma sílaba, três palavras ----
p(u"p20enun", u"Folha vinte. Um pedaço só serve para três palavras. Junte-o a "
              u"cada final e veja o que aparece.")
for k, J in JUN.items():
    for n, r in enumerate(J[u"r"]):
        p(u"junr_%s_%d" % (k, n), r + u".")
    p(u"certo20_" + k, u"Olhe só: com esse pedaço saíram três palavras. " +
                       u", ".join(J[u"r"]) + u".")
    p(u"dica20_" + k, u"Toque nos três, um de cada vez.")

# ---- 21 e 22 — achar as sílabas ----
p(u"p21enun", u"Folha vinte e um. Marque só os pedaços que formam a palavra. "
              u"Depois toque em Conferir.")
p(u"p22enun", u"Folha vinte e dois. Agora há muitos pedaços parecidos. Diga a "
              u"palavra devagar e ache os certos.")
for k, M in MAR.items():
    pg = u"21" if k[0] == u"x" else u"22"
    p(u"mar_" + k, u", ".join(M[u"g"]) + u". " + M[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! " + u", ".join(M[u"g"]) + u", " +
                                M[u"p"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute a palavra e marque um pedaço de cada "
                               u"vez, na ordem em que você ouve.")

# ---- 23 — caça-palavras ----
p(u"p23enun", u"Folha vinte e três. Aqui cada casa é uma sílaba. Ache o nome "
              u"de cada cor: toque na primeira casa e depois na última.")
for k, C in CACA[u"pal"].items():
    p(u"caca_" + k, C[u"p"] + u".")
    p(u"certo23_" + k, u"Achou! A cor " + C[u"p"] + u" estava ali.")
    p(u"dica23_" + k, u"Procure a casa que tem o começo dessa palavra.")

# ---- 24 — a trilha ----
p(u"p24enun", u"Folha vinte e quatro. Leve o pato até a lagoa. Em cada passo, "
              u"toque só na palavra de três sílabas.")
for P in TRI[u"passos"]:
    certa = [o for o in P[u"ops"] if o[u"ok"]][0]
    p(u"certo24_" + P[u"c"], u"Boa! " + certa[u"p"] + u" tem três sílabas. O "
                             u"pato andou mais um passo.")
    p(u"dica24_" + P[u"c"], u"Bata palma em cada uma das três antes de "
                            u"escolher.")
    for o in P[u"ops"]:
        p(u"pal_" + ch(o[u"p"]), o[u"p"] + u".")

# ---- 25 — escrever o nome da figura ----
p(u"p25enun", u"Folha vinte e cinco. Olhe a figura e monte o nome dela: as "
              u"letras estão embaralhadas ali embaixo. No computador dá para "
              u"digitar.")
for k, C in CRZ.items():
    p(u"crz_" + k, C[u"d"] + u".")
    p(u"certo25_" + k, u"Isso! Você escreveu " + C[u"r"] + u".")
    p(u"dica25_" + k, u"Diga o nome da figura em voz alta e escreva a primeira "
                      u"letra que você ouvir.")

# ---- 26 e 27 — contar de novo ----
p(u"p26enun", u"Folha vinte e seis. Lembra do começo? Diga a palavra e pinte "
              u"uma bolinha para cada palma.")
p(u"p27enun", u"Folha vinte e sete. E lembra que letra não é sílaba? Diga "
              u"quantas sílabas tem cada palavra.")
for k, C in CON.items():
    p(u"con_" + k, C[u"p"] + u".")
    p(u"certo26_" + k, u"Isso! " + C[u"p"] + u" tem " + ple(C[u"n"]) + u".")
    p(u"dica26_" + k, u"Diga devagar, com a mão no queixo.")

# ---- 28 e 29 — o ditado ----
p(u"p28enun", u"Folha vinte e oito. Agora é ditado. Ouça a palavra, conte as "
              u"palmas de cabeça e escolha a gaveta.")
p(u"p29enun", u"Folha vinte e nove. O ditado das quatro gavetas. Ouça quantas "
              u"vezes quiser.")
for k, D2 in DIT.items():
    pg = u"28" if k[:2] == u"ac" else u"29"
    p(u"dit_" + k, D2[u"p"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! A palavra era " + D2[u"p"] + u", " +
                                NCL[D2[u"c"]] + u".")
    p(u"dica" + pg + u"_" + k, u"Ouça de novo e bata palma com a palavra na "
                               u"cabeça.")

# ---- 30 — a frase grudada ----
p(u"p30enun", u"Folha trinta. Estas frases vieram sem espaço nenhum. Toque nas "
              u"frestas para separar as palavras.")
for k, FR in FRAS.items():
    p(u"fra_" + k, FR[u"r"] + u".")
    p(u"certo30_" + k, u"Isso! " + FR[u"r"] + u".")
    p(u"dica30_" + k, u"Escute a frase e conte quantas palavras ela tem. Cada "
                      u"palavra precisa do seu espaço.")

# ---- 31 — achar no texto ----
p(u"p31enun", u"Folha trinta e um. Leia a história. Depois ache no texto a "
              u"palavra que cada pergunta pede.")
p(u"txt_tudo", u" ".join(TXT[u"linhas"]))
for k, P in TXT[u"pede"].items():
    p(u"txtq_" + k, u"Ache no texto " + lp(P[u"q"]) + u" e toque nela.")
    p(u"certo31_" + k, u"Isso mesmo! Essa palavra serve.")
    p(u"dica31_" + k, u"Leia a história de novo batendo palma em cada palavra.")
    for w in P[u"alvo"]:
        p(u"pal_" + ch(w), w + u".")

# ---- 32 — a cantiga ----
p(u"p32enun", u"Folha trinta e dois. Cante baixinho e pinte cada palavra da "
              u"cor do número de sílabas dela.")
for cl in (u"m", u"d"):
    p(u"certo32_" + cl, u"Isso! Você achou todas as de " + NCL[cl] + u".")
    p(u"dica32_" + cl, u"Cante o verso e bata palma junto. A batida marca a "
                       u"sílaba sozinha.")
for w in CANT[u"gab"].keys():
    p(u"pal_" + ch(w), w + u".")

# ---- 33 — o banco de sílabas ----
p(u"p33enun", u"Folha trinta e três. Neste banco há sílabas de várias "
              u"palavras. Monte a que se pede, tocando nos pedaços na ordem.")
for k, B in BANCO[u"pal"].items():
    p(u"ban_" + k, B[u"r"] + u".")
    p(u"certo33_" + k, u"Isso! Do banco saiu a palavra " + B[u"r"] + u".")
    p(u"dica33_" + k, u"Ouça a palavra e procure o pedaço em que ela começa.")

# ---- 34 — o desafio ----
p(u"p34enun", u"Folha trinta e quatro. Agora é a sua vez de inventar. Escreva "
              u"uma palavra que sirva para cada pedido.")
for k, X in DESA.items():
    p(u"des_" + k, u"Escreva " + lp(X[u"q"]) + u".")
    p(u"certo34_" + k, u"Muito bem! A sua palavra serve.")
    p(u"dica34_" + k, u"Pense numa palavra e bata palma nela antes de "
                      u"escrever. O número de palmas tem que bater com o pedido.")

# ---- 📝 OS LEMBRETES (o post-it) ----
# ⚠️ SAEM DO PROPRIO `var LEMB` do index.html — uma fonte so. Escritos a mao
#    aqui, uma frase corrigida na tela deixaria o mp3 gravado sob a chave velha
#    e o alto-falante ficaria MUDO, sem erro nenhum no console. E o "silencio",
#    o unico defeito desta casa que nao deixa marca.
# ⚠️ SAO DUAS COISAS POR LEMBRETE, e esquecer uma deixa um botao mudo:
#      · `lemb_<k>`       -> o lembrete inteiro (titulo + frases), que e o que
#                            toca quando ele ABRE, na mao ou sozinho;
#      · `lembl_<k>_<i>`  -> cada frase sozinha, o alto-falante ao lado dela.
LEMB = bloco(u"LEMB")
for _k in sorted(LEMB):
    _L = LEMB[_k]
    p(u"lemb_" + _k, _L[u"t"] + u". " + u" ".join(_L[u"l"]))
    for _i, _ln in enumerate(_L[u"l"]):
        p(u"lembl_%s_%d" % (_k, _i), _ln)

# ---- 35 — o cartaz ----
p(u"p35enun", u"Folha trinta e cinco. Você já sabe fazer tudo isto. Agora monte o "
              u"cartaz: leve cada palavra para a linha do número de sílabas dela.")
for L in CART[u"linhas"]:
    p(u"cart_" + L[u"k"], L[u"t"] + u": " + L[u"d"] + u". Por exemplo, " +
                          L[u"e"].replace(u"-", u", ") + u".")
for k, X in CART[u"exem"].items():
    p(u"pal_" + ch(X[u"p"]), X[u"p"] + u".")
    p(u"certo35_" + k, u"Isso! " + X[u"p"] + u" é " +
                       {u"m": u"monossílaba", u"d": u"dissílaba",
                        u"t": u"trissílaba", u"p": u"polissílaba"}[X[u"c"]] + u".")
    p(u"dica35_" + k, u"Bata palma na palavra e conte. Depois olhe qual linha "
                      u"pede esse número.")





# ==============================================================================
#  O MAPA DAS SÍLABAS — quem recorta o quê, de qual palavra
#
#  ⚠️⚠️ SEGUNDA VEZ QUE A CASA PAGA POR ISTO. Marcos, 16/set/2026: *"veja nas
#     sílabas não está bom, ao invés de falar SÁ ele fala S-A em SAPO"* — e ele
#     já tinha ouvido o mesmo em set/2026 (*"ele está dizendo 'v a' ao invés de
#     'va'"*). A ferramenta que conserta existe desde então
#     (`_padrao/silabas_voz.py`, no `entregar.yml`): ela grava a PALAVRA
#     INTEIRA, alinha letra a letra e CORTA a sílaba de dentro dela.
#     O que faltou foi ligá-la: o ESQUELETO da folha viva nasceu sem esse
#     pedaço, e este caderno — que fala sílaba em oito folhas — nasceu mudo
#     para ele. Consertado aqui E no esqueleto, no mesmo commit.
#
#  ⚠️ POR QUE NÃO DÁ PARA SINTETIZAR A SÍLABA SOLTA: a voz não lê SOM, lê
#     PALAVRA. "SA" sozinho ela soletra "esse-á"; "VA", "vê-á"; "ÇÃ" ela nem
#     tenta, porque ç não começa palavra em português. Escrever a sílaba "como
#     se fala" conserta um caso e nunca fecha a família.
#
#  ⚠️ E NÃO HÁ FALA DE RESERVA POR SÍLABA. Se o recorte faltar, o app diz a
#     PALAVRA INTEIRA. Uma reserva sintetizada seria o defeito voltando pela
#     porta dos fundos — e calada, que é pior.
# ==============================================================================
_SIL_DE = {}          # palavra -> [sílabas]
_MAPA_SIL = {}        # sílaba  -> [palavra, posição]

# ⚠️⚠️ O RECORTE SÓ FUNCIONA SE A LISTA ESTIVER NA ORDEM DA PALAVRA. O
#    `ctc-forced-aligner` alinha a gravação LETRA A LETRA e corta pelos limites;
#    se a lista vier ["RO","CAR"] para CARRO, ele corta "ro" no lugar de "car" e
#    a criança ouve o pedaço errado — calada, sem erro nenhum na tela.
#    Foi exatamente o que ia acontecer: a folha 15/16 guarda as sílabas
#    EMBARALHADAS (é esse o exercício dela), e eu as registrei como se fossem a
#    ordem da palavra. Este guarda recusa qualquer lista cuja junção não dê a
#    palavra — nenhuma lista torta entra no `silabas.json`.
_RECUSADAS = []

def _reg(palavra, silabas):
    silabas = list(silabas)
    if u"".join(silabas).upper() != palavra.upper():
        _RECUSADAS.append((palavra, silabas))
        return
    # ⚠️ E GANHA SEMPRE A PARTIÇÃO MAIS FINA. A folha 17/18/19 guarda a palavra
    #    em TRÊS PEDAÇOS (o começo, a lacuna e o fim) — e "PIPO"+"CA" fecha
    #    PIPOCA sem ser separação silábica nenhuma. Se ela sobrescrevesse a de
    #    MAR (PI-PO-CA), a sílaba PI ficava sem casa e o botão dela emudecia.
    velha = _SIL_DE.get(palavra.lower())
    if velha and len(velha) >= len(silabas):
        return
    _SIL_DE[palavra.lower()] = silabas

def _ordena(palavra, embaralhadas):
    u"""devolve as mesmas sílabas na ORDEM em que formam a palavra — sem
    inventar nenhuma: só encaixa as que já existem, da esquerda para a
    direita, e desiste se não fechar exato."""
    resto, saida, alvo = list(embaralhadas), [], palavra.upper()
    while alvo:
        for _i, _sb in enumerate(resto):
            if alvo.startswith(_sb.upper()):
                saida.append(_sb)
                alvo = alvo[len(_sb):]
                resto.pop(_i)
                break
        else:
            return None
    return saida if not resto else None

# as palavras deste caderno que já vêm com as sílabas escritas nos DADOS
for _B in BAT.values():
    _reg(_B[u"p"], _B[u"s"])
for _V in VOG.values():
    _reg(u"".join(_V[u"s"]), _V[u"s"])
for _O in ORD.values():
    _ord = _ordena(_O[u"r"], _O[u"s"])
    if _ord:
        _reg(_O[u"r"], _ord)
for _M in MAR.values():
    _reg(_M[u"p"], _M[u"g"])
for _Bp in BANCO[u"pal"].values():
    _reg(_Bp[u"r"], _Bp[u"s"])
for _C in CART[u"linhas"]:
    if u"-" in _C[u"e"]:
        _reg(_C[u"e"].replace(u"-", u""), _C[u"e"].split(u"-"))

# ⚠️ AS SÍLABAS SOLTAS DAS FOLHAS 17, 18 e 19 — são as opções que a criança
#    toca, e eram elas que saíam soletradas. Cada uma precisa de uma palavra de
#    onde ser recortada, e a palavra da própria folha é a melhor: a criança
#    ouve o pedaço no lugar em que ele mora.
for _k, _F in FAL.items():
    _q = _F[u"q"]
    _partes = []
    if _F[u"a"]:
        _partes.append(_F[u"a"])
    _partes.append(_F[u"r"])
    if _F[u"z"]:
        _partes.append(_F[u"z"])
    # a palavra inteira, partida nos pedaços que a folha mostra
    if u"".join(_partes) == _q:
        _reg(_q, _partes)
    for _sb in _F[u"ops"]:
        if _sb in _partes:
            continue
        # a opção errada também fala — e ela tem de sair de ALGUMA palavra
        for _w, _ss in list(_SIL_DE.items()):
            if _sb in _ss:
                break

def _achaSilaba(s):
    u"""a palavra de onde a sílaba será recortada. Entre as candidatas, ganha a
    MAIS CURTA: quanto menos letras a gravação tem, menos o alinhador tem onde
    errar, e o pedaço sai mais limpo."""
    cand = [_w for _w in sorted(_SIL_DE) if s in _SIL_DE[_w]]
    if not cand:
        return None
    _w = min(cand, key=lambda w: (len(_SIL_DE[w]), len(w), w))
    return [_w, _SIL_DE[_w].index(s)]

# toda sílaba que o app pode falar sozinha
_soltas = set()
for _F in FAL.values():
    _soltas.update(_F[u"ops"])
for _M in MAR.values():
    _soltas.update(_M[u"g"])
    _soltas.update(_M[u"d"])
for _O in ORD.values():
    _soltas.update(_O[u"s"])
_soltas.update(BANCO[u"sil"])
for _J in JUN.values():
    _soltas.add(_J[u"i"])

# ⚠️ SÍLABA SEM PALAVRA DE ORIGEM É SÍLABA QUE VAI SAIR SOLETRADA. Em vez de
#    deixar passar calada, este laço INVENTA a palavra onde ela mora — usando
#    as palavras que o próprio caderno já tem — e, se não achar nenhuma, a
#    sílaba fica FORA do mapa e o app diz a palavra inteira.
# ⚠️ AS SÍLABAS DISTRATORAS NÃO MORAM EM NENHUMA PALAVRA DO CADERNO — e são
#    justamente as que a criança toca para DESCARTAR ("MI não está em TUCANO").
#    Sem casa, o botão delas ficava MUDO, que é o pior dos mundos: a folha 21
#    tem sete distratoras por item e metade da turma não lê o que está escrito
#    nelas. Então cada uma ganha aqui uma PALAVRA-CARREGADORA: uma palavra de
#    verdade, escolhida curta e com a sílaba no começo, que existe só para ser
#    gravada e cortada. A criança nunca ouve a palavra inteira — ouve o pedaço.
_CARREGADORAS = {
    u"CÃO": [u"CÃO"],                 u"DEDO": [u"DE", u"DO"],
    u"DIA": [u"DI", u"A"],            u"FEVEREIRO": [u"FE", u"VE", u"REI", u"RO"],
    u"LUA": [u"LU", u"A"],            u"MINUTO": [u"MI", u"NU", u"TO"],
    u"MOLA": [u"MO", u"LA"],          u"PENA": [u"PE", u"NA"],
    u"RIO": [u"RI", u"O"],            u"SINO": [u"SI", u"NO"],
    u"TIJOLO": [u"TI", u"JO", u"LO"], u"VIDRO": [u"VI", u"DRO"],
}
for _cw in sorted(_CARREGADORAS):
    _reg(_cw, _CARREGADORAS[_cw])

_ORFAS = []
for _s in sorted(_soltas):
    _achou = _achaSilaba(_s)
    if _achou:
        _MAPA_SIL[_s] = _achou
    else:
        _ORFAS.append(_s)

# e a PALAVRA INTEIRA de cada uma precisa existir como fala, porque é dela que
# o recorte sai — e é ela que o app diz quando o recorte falta
for _w in sorted(_SIL_DE):
    p(u"pal_" + ch(_w), _w.upper() + u".")

# ⚠️⚠️ O GUARDA DO `F` (15/set/2026, e este erro já tinha sido pago uma vez).
#    `F` é o dicionário das falas. Basta um `for k, F in ALGO.items()` para ele
#    virar um item solto, e a partir dali tudo o que foi escrito some — sem erro
#    nenhum, até a saída estourar com uma mensagem que não fala de `F`. Aqui ele
#    é conferido antes de gravar: se não for mais um dicionário de textos, para.
if not isinstance(F, dict):
    raise SystemExit(u"⛔ o `F` deixou de ser o dicionario das falas — alguma "
                     u"variavel de laco se chamou F e apagou tudo.")
_ruins = [k for k, v in F.items() if not isinstance(v, type(u""))]
if _ruins:
    raise SystemExit(u"⛔ falas que nao sao texto: %s" % u", ".join(_ruins[:6]))


# ⚠️⚠️ FALA DE DUAS PALAVRAS SAI TORTA — e isto foi medido pelo OUVIDO da
#    entrega, não deduzido: de "Isso! CAVALO." ele ouviu só "isso", e de
#    "Isso! PATO." também. Duas palavras soltas não dão contexto nenhum à voz,
#    e a criança também ganha pouco: "Isso!" já é o som de acerto, e o que
#    ensina é a frase que diz O QUE ELA FEZ.
#    Este guarda existe para eu não descobrir isso de novo pelo ouvido, que
#    custa dezesseis minutos de workflow por rodada.
# ⚠️ AS EXCEÇÕES SÃO NOMEADAS, e cada uma tem razão: são as falas que a criança
#    ouve ao TOCAR numa peça, e que por isso têm de dizer a peça e MAIS NADA.
#    O alto-falante de uma opção que dissesse uma frase inteira atrapalharia a
#    escolha em vez de ajudar. Elas não são "curtas por descuido": são curtas
#    de propósito, e por isso ficam de fora da conta.
_SO_A_PECA = (u"num_", u"sil_", u"pal_", u"op_", u"gavn_", u"diz2_", u"ord_",
              u"let_", u"con_", u"dit_", u"cor_", u"mar_", u"caca_", u"ban_",
              u"jun_", u"lig_", u"ligc_", u"crz_", u"vog_", u"qz_", u"qzop_",
              u"fal_", u"diz_", u"junr_", u"lapis_", u"cart_")
_curtas = [(k, v) for k, v in F.items()
           if len(v.split()) < 3 and not k.startswith(_SO_A_PECA)]
if _curtas:
    raise SystemExit(u"⛔ %d fala(s) com menos de 3 palavras — o ouvido nao as "
                     u"entende e a crianca ganha pouco:\n   %s"
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
#    dentro do mp3 da palavra inteira, e o `SILMAP` é o que o app usa para
#    saber de qual palavra veio cada pedaço. Uma fonte só para os dois.
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
# ⚠️ NADA DISTO SAI CALADO. Sílaba órfã não é erro — ela simplesmente faz o app
#    dizer a palavra inteira — mas se eu não a vir impressa, nunca vou saber que
#    aquele botão não fala o pedaço.
if _ORFAS:
    print(u"   ⚠️ %d silaba(s) SEM palavra de origem (o app dira a palavra "
          u"inteira): %s" % (len(_ORFAS), u", ".join(_ORFAS)))
if _RECUSADAS:
    print(u"   ⚠️ %d lista(s) recusada(s) por nao formarem a palavra: %s"
          % (len(_RECUSADAS), u", ".join(
              u"%s=%s" % (w, u"-".join(s)) for w, s in _RECUSADAS[:8])))
