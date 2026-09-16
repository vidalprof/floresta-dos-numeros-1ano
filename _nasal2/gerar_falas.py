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
PREFIXO = u"nz_"                     # <- o prefixo desta atividade
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



NUM = {1: u"uma", 2: u"duas", 3: u"três", 4: u"quatro", 5: u"cinco"}


def ple(n):
    u"""'1 sílaba' x '2 sílabas' — a voz erra se o número vier solto."""
    return NUM.get(n, str(n)) + (u" sílaba" if n == 1 else u" sílabas")


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
p(u"cacatoque", u"Toque primeiro na letra do começo da palavra.")
p(u"trilhaordem", u"Esta casa ainda não chegou. Preencha primeiro a casa que "
                  u"está piscando.")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — lendo os DADOS do index.html. Uma fonte só.
# ⚠️ A DICA NUNCA DIZ A RESPOSTA, e em 2º ano ela é curta.
# ---------------------------------------------------------------------------
NAS = bloco(u"NAS")
GAV = bloco(u"GAV")
ESCR = bloco(u"ESCR")
MN = bloco(u"MN")
REG = bloco(u"REG")
FIMM = bloco(u"FIMM")
CNT = bloco(u"CNT")
ERR = bloco(u"ERR")
DIF = bloco(u"DIF")
PAR = bloco(u"PAR")
FRAS = bloco(u"FRAS")
CRZ = bloco(u"CRZ")
CACA = bloco(u"CACA")
TRI = bloco(u"TRI")
ORD = bloco(u"ORD")
LIGA = bloco(u"LIGA")
CENA = bloco(u"CENA")
TXT = bloco(u"TXT")
ACH = bloco(u"ACH")
CART = bloco(u"CART")

p(u"capa", u"As Três Marcas do Nariz. Trinta e cinco folhas sobre o som que "
           u"sai pelo nariz. Escreva o seu nome ali embaixo e toque em Começar.")

# ---- 1, 2 e 5 — tem som de nariz? ----
p(u"p1enun", u"Folha um. Ponha a mão no nariz e diga cada palavra. Marque as "
             u"que fazem o nariz tremer, e toque em Conferir.")
p(u"p2enun", u"Folha dois. Agora é ao contrário: marque as intrusas, as que não "
             u"têm marca de nariz.")
p(u"p5enun", u"Folha cinco. Estas trazem o til, o chapeuzinho ondulado. Marque "
             u"só as que têm som de nariz.")
_PGNAS = {u"a": u"1", u"b": u"2", u"e": u"5"}
for k, N in NAS.items():
    pg = _PGNAS[k[0]]
    alvo = N[u"nao"] if pg == u"2" else N[u"sim"]
    p(u"certo" + pg + u"_" + k, u"Isso mesmo! As três são " +
                                u", ".join(alvo) + u".")
    p(u"dica" + pg + u"_" + k, u"Diga cada palavra com a mão no nariz. Onde ele "
                               u"treme, a marca está lá.")

# ---- 3, 4, 26, 27 e 29 — as gavetas ----
p(u"p3enun", u"Folha três. Qual marca faz o som de nariz nesta palavra? Leve "
             u"cada uma para a gaveta dela.")
p(u"p4enun", u"Folha quatro. Mais palavras para separar. Diga cada uma devagar "
             u"antes de escolher a gaveta.")
p(u"p26enun", u"Folha vinte e seis. Agora olhe a vogal que vem antes da marca. "
              u"Leve cada palavra para a gaveta dela.")
p(u"p27enun", u"Folha vinte e sete. E estas? Cuidado: algumas não são nem O M "
              u"nem U M.")
p(u"p29enun", u"Folha vinte e nove. O M aparece em três lugares diferentes. Em "
              u"qual deles ele está, nesta palavra?")
_NOMEGAV = {
 u"til": u"Nesta gaveta vão as palavras marcadas pelo til, o chapeuzinho ondulado.",
 u"m": u"Nesta gaveta vão as palavras marcadas pela letra M.",
 u"n": u"Nesta gaveta vão as palavras marcadas pela letra N.",
 u"mp": u"Nesta gaveta vão as palavras em que o M vem antes da letra P.",
 u"mb": u"Nesta gaveta vão as palavras em que o M vem antes da letra B.",
 u"mf": u"Nesta gaveta vão as palavras em que o M fecha a palavra.",
 u"am": u"Nesta gaveta vão as palavras com A antes da marca.",
 u"em": u"Nesta gaveta vão as palavras com E antes da marca.",
 u"im": u"Nesta gaveta vão as palavras com I antes da marca.",
 u"om": u"Nesta gaveta vão as palavras com O antes da marca.",
 u"um": u"Nesta gaveta vão as palavras com U antes da marca.",
 u"outra": u"Nesta gaveta vão as palavras que não são de nenhuma das duas acima."}
_PGGAV = {u"gA": u"3", u"gB": u"4", u"gC": u"29", u"gD": u"26", u"gE": u"27"}
for gk, G in GAV.items():
    for C in G[u"cols"]:
        p(u"gav_" + gk + u"_" + C[u"k"], _NOMEGAV[C[u"k"]])
    pg = _PGGAV[gk]
    for k, Pl in G[u"pal"].items():
        p(u"diz2_" + gk + u"_" + k, Pl[u"p"] + u".")
        p(u"certo" + pg + u"_" + k, u"Isso mesmo! Essa palavra mora ali.")
        p(u"dica" + pg + u"_" + k, u"Diga a palavra devagar e olhe bem a marca "
                                   u"que ela usa.")

# ---- 6, 13 e 34 — escrever a palavra ----
p(u"p6enun", u"Folha seis. Escreva a palavra tocando nas letras. O til já vem "
             u"junto com a letra, e no computador dá para digitar.")
p(u"p13enun", u"Folha treze. Estas palavras terminam com M. Escreva cada uma "
              u"inteira.")
p(u"p34enun", u"Folha trinta e quatro. Olhe a figura e escreva o nome dela. "
              u"Pense na regra antes de pôr o M ou o N.")
for k, X in ESCR.items():
    pg = u"6" if k[0] == u"h" else u"34"
    p(u"esc_" + k, X[u"w"] + u".")
    p(u"certo" + pg + u"_" + k, u"Muito bem! A palavra é " + X[u"w"] + u".")
    p(u"dica" + pg + u"_" + k, u"Escute a palavra de novo e comece pela primeira "
                               u"letra dela.")
for k, X in FIMM.items():
    p(u"fim_" + k, X[u"r"] + u".")
    p(u"certo13_" + k, u"Isso! Quem fecha essa palavra é a letra M.")
    p(u"dica13_" + k, u"No fim da palavra, quase sempre quem fecha é o M.")

# ---- 7, 8, 9, 11 e 12 — M ou N ----
p(u"p7enun", u"Folha sete. Olhe a figura, ouça a palavra e escolha: M ou N?")
p(u"p8enun", u"Folha oito. Mais figuras. Repare bem na letra que vem depois da "
             u"lacuna.")
p(u"p9enun", u"Folha nove. Agora sem figura nenhuma: só a palavra e o seu ouvido.")
p(u"p11enun", u"Folha onze. Nestas, depois da lacuna vem P ou B. Você já sabe "
              u"qual letra entra.")
p(u"p12enun", u"Folha doze. E nestas vem outra consoante. A letra é a outra.")
_PGMN = {u"i": u"7", u"j": u"8", u"k": u"9", u"m": u"11", u"n": u"12"}
for k, X in MN.items():
    pg = _PGMN[k[0]]
    inteira = X[u"a"] + X[u"r"] + X[u"z"]
    p(u"mn_" + k, inteira + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! A palavra fica " + inteira + u".")
    p(u"dica" + pg + u"_" + k, u"Olhe a letra que vem logo depois da lacuna. Ela "
                               u"é quem manda.")
for L in (u"m", u"n"):
    p(u"let_" + L, u"Letra " + L.upper() + u".")

# ---- 10 — a regra descoberta pela criança ----
p(u"p10enun", u"Folha dez. Você já completou três folhas inteiras. Agora é você "
              u"quem descobre a regra: olhe o que acabou de fazer.")
for k, R in REG.items():
    p(u"reg_" + k, lp(R[u"q"]))
    p(u"certo10_" + k, u"Isso mesmo! Você descobriu sozinho.")
    p(u"dica10_" + k, u"Volte na folha de antes e olhe as palavras que você já "
                      u"completou.")

# ---- 14 e 24 — ordenar as sílabas ----
p(u"p14enun", u"Folha catorze. Bata uma palma para cada pedaço e toque nas "
              u"sílabas na ordem.")
p(u"p24enun", u"Folha vinte e quatro. As sílabas se embaralharam. Toque nelas na "
              u"ordem.")
for k, O in CNT.items():
    p(u"ord_" + k, O[u"r"] + u".")
    p(u"certo14_" + k, u"Isso! A palavra tem " + ple(len(O[u"s"])) + u".")
    p(u"dica14_" + k, u"Diga a palavra devagar. Qual é o pedaço que começa?")
for k, O in ORD.items():
    p(u"ord_" + k, O[u"r"] + u".")
    p(u"certo24_" + k, u"Isso! A palavra montada é " + O[u"r"] + u".")
    p(u"dica24_" + k, u"Diga a palavra devagar e procure o primeiro pedaço.")

# ---- 15, 16 e 17 — o olho de revisor ----
p(u"p15enun", u"Folha quinze. Agora você é o revisor. Uma das duas está errada: "
              u"ache a certa.")
p(u"p16enun", u"Folha dezesseis. Mais seis para revisar. Olhe a letra que vem "
              u"depois da marca.")
p(u"p17enun", u"Folha dezessete. Três destas combinam entre si e uma não. Ache a "
              u"estranha.")
for k, E in ERR.items():
    pg = u"15" if k[0] == u"q" else u"16"
    p(u"err_" + k, E[u"r"] + u".")
    p(u"certo" + pg + u"_" + k, u"Muito bem! A escrita certa é " + E[u"r"] + u".")
    p(u"dica" + pg + u"_" + k, u"Olhe a letra que vem depois da marca e lembre "
                               u"da regra.")
for k, T in DIF.items():
    p(u"dif_" + k, u", ".join(T[u"ops"]) + u".")
    p(u"certo17_" + k, u"Isso! A estranha é " + T[u"r"] + u", porque " + T[u"pq"] + u".")
    p(u"dica17_" + k, u"Leia as quatro em voz alta e procure a que não combina "
                      u"com as outras.")

# ---- 18, 19, 20 e 33 — o par mínimo e a frase ----
p(u"p18enun", u"Folha dezoito. Duas palavras quase iguais, e só uma tem a marca "
              u"do nariz. Qual das figuras é a palavra escrita?")
p(u"p19enun", u"Folha dezenove. Mais pares. Diga as duas em voz alta e escute a "
              u"diferença.")
p(u"p20enun", u"Folha vinte. Qual das duas cabe na frase? Uma delas deixa a "
              u"frase sem sentido.")
p(u"p33enun", u"Folha trinta e três. Agora as duas escritas são parecidas, mas "
              u"só uma está certa.")
for k, P_ in PAR.items():
    pg = u"18" if k[0] == u"u" else u"19"
    p(u"par_" + k, P_[u"a"] + u". " + P_[u"b"] + u".")
    p(u"certo" + pg + u"_" + k, u"Isso! Uma letra a mais e " + P_[u"a"] +
                                u" virou " + P_[u"b"] + u".")
    p(u"dica" + pg + u"_" + k, u"Leia a palavra escrita ali em cima, letra por "
                               u"letra, e olhe se ela tem a marca.")
for k, F_ in FRAS.items():
    pg = u"20" if k[0] == u"w" else u"33"
    p(u"fra_" + k, lp(F_[u"a"]) + u" " + F_[u"w"] + u" " + lp(F_[u"z"]))
    p(u"certo" + pg + u"_" + k, u"Isso! " + lp(F_[u"a"]) + u" " + F_[u"w"] +
                                u" " + lp(F_[u"z"]))
    p(u"dica" + pg + u"_" + k, u"Escute a frase inteira outra vez e veja qual "
                               u"das duas faz sentido.")

# ---- 21 — a cruzadinha ----
p(u"p21enun", u"Folha vinte e um. Leia a pista e escreva a palavra. Todas têm M "
              u"antes de P ou de B.")
for k, C in CRZ.items():
    p(u"crz_" + k, lp(C[u"d"]))
    p(u"certo21_" + k, u"Isso mesmo! A palavra é " + C[u"w"] + u".")
    p(u"dica21_" + k, u"Escute a pista de novo e pense numa palavra com M antes "
                      u"de P ou de B.")

# ---- 22 — o caça-palavras ----
p(u"p22enun", u"Folha vinte e dois. Ache cada palavra: toque na primeira letra e "
              u"depois na última.")
for k, C in CACA[u"pal"].items():
    p(u"certo22_" + k, u"Achou! A palavra era " + C[u"p"] + u".")
    p(u"dica22_" + k, u"Procure a primeira letra da palavra e siga a linha dela.")

# ---- 23 — a trilha ----
p(u"p23enun", u"Folha vinte e três. Ande pela trilha: preencha cada casa com M "
              u"ou N e ganhe os pontos dela.")
p(u"certo23_t", u"Trilha inteira! Você completou as dez casas e ganhou todos os "
                u"pontos.")
p(u"dica23_t", u"Olhe a letra que vem depois da lacuna desta casa.")

# ---- 25 — ligar a palavra à figura ----
p(u"p25enun", u"Folha vinte e cinco. Leve cada palavra até a figura dela.")
for k, L in LIGA.items():
    p(u"certo25_" + k, u"Isso! " + L[u"p"] + u" é essa figura mesmo.")
    p(u"dica25_" + k, u"Escute a palavra e olhe as figuras uma por uma.")

# ---- 28 — ache na cena ----
p(u"p28enun", u"Folha vinte e oito. Olhe tudo o que está espalhado aqui. Marque "
              u"só o que tem som de nariz no nome, e depois confira.")
p(u"certo28_c", u"Isso mesmo! Você achou todas as que têm marca de nariz.")
p(u"dica28_c", u"Diga o nome de cada coisa com a mão no nariz. Onde ele treme, "
               u"a marca está lá.")

# ---- 30 e 31 — ache no texto ----
p(u"p30enun", u"Folha trinta. Leia a história e toque nas palavras que têm M "
              u"antes de P ou de B. Depois confira.")
p(u"p31enun", u"Folha trinta e um. O fim da história. Ache as que têm M P ou M B.")
p(u"certo30_t", u"Muito bem! Você achou todas as palavras da regra no texto.")
p(u"dica30_t", u"Leia devagar e procure o M grudado num P ou num B.")
p(u"certo31_t", u"Isso! Achar a regra dentro de um texto é o degrau mais alto.")
p(u"dica31_t", u"Leia devagar e procure o M grudado num P ou num B.")

# ---- 32 — ache na frase ----
p(u"p32enun", u"Folha trinta e dois. Em cada frase há uma palavra com a marca "
              u"pedida. Toque nela.")
for k, A in ACH.items():
    # ⚠️ a frase dos DADOS já termina na última palavra; juntar um ponto
    #    aqui dava ".." quando ela vinha pontuada (o revisor pegou).
    p(u"ach_" + k, (u" ".join(A[u"fr"]).rstrip(u".") + u"."))
    p(u"certo32_" + k, u"Isso! A palavra era " + A[u"ok"] + u".")
    p(u"dica32_" + k, u"Leia a frase palavra por palavra e escute qual delas faz "
                      u"o nariz tremer.")

# ---- 35 — o cartaz ----
p(u"p35enun", u"Folha trinta e cinco. Você já sabe tudo isto. Agora as regras "
              u"por escrito: leve cada exemplo para a linha dele.")
for L in CART[u"linhas"]:
    p(u"cart_" + L[u"k"], L[u"t"] + u", " + L[u"d"] + u". Por exemplo: " +
                          L[u"e"] + u".")
for k, X in CART[u"exem"].items():
    p(u"certo35_" + k, u"Isso mesmo! Esse é um exemplo daquela linha.")
    p(u"dica35_" + k, u"Leia a linha de novo e veja qual regra ela conta.")

# ==============================================================================
#  AS SÍLABAS FALADAS — só as folhas 14 e 24 falam sílaba solta, e mesmo assim
#  elas SE RECORTAM da palavra inteira. A voz não lê SOM, lê PALAVRA.
# ==============================================================================
_RECUSADAS = []
_SIL_DE = {}
_MAPA_SIL = {}


def _reg(palavra, silabas):
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


for _C in CNT.values():
    _reg(_C[u"r"], _C[u"s"])
for _O in ORD.values():
    _o = _ordena(_O[u"r"], _O[u"s"])
    if _o:
        _reg(_O[u"r"], _o)

# ⚠️ carregadoras: as sílabas que não moram em palavra nenhuma deste caderno
_CARREGADORAS = {u"SENTE": [u"SEN", u"TE"], u"PREGO": [u"PRE", u"GO"],
                 u"BORDA": [u"BOR", u"DA"], u"CAMA": [u"CA", u"MA"],
                 u"PATO": [u"PA", u"TO"], u"BOLA": [u"BO", u"LA"],
                 u"TAPA": [u"TA", u"PA"], u"BOMBA": [u"BOM", u"BA"],
                 u"MEIA": [u"MEI", u"A"], u"JARRA": [u"JAR", u"RA"],
                 u"DIA": [u"DI", u"A"], u"HORA": [u"HO", u"RA"],
                 u"MEDO": [u"ME", u"DO"], u"VIDA": [u"VI", u"DA"],
                 u"AMOR": [u"A", u"MOR"], u"MENINO": [u"ME", u"NI", u"NO"],
                 u"TAMPA": [u"TAM", u"PA"], u"BEBIDA": [u"BE", u"BI", u"DA"]}
for _cw in sorted(_CARREGADORAS):
    _reg(_cw, _CARREGADORAS[_cw])


def _achaSilaba(s):
    cand = [_w for _w in sorted(_SIL_DE) if s in _SIL_DE[_w]]
    if not cand:
        return None
    _w = min(cand, key=lambda w: (len(_SIL_DE[w]), len(w), w))
    return [_w, _SIL_DE[_w].index(s)]


def _grupos_de_vogal(s):
    v, n, antes = u"AEIOUÁÀÂÃÉÊÍÓÔÕÚ", 0, False
    for c in s.upper():
        agora = c in v
        if agora and not antes:
            n += 1
        antes = agora
    return n


_soltas = set()
for _C in CNT.values():
    _soltas.update(_C[u"s"])
for _O in ORD.values():
    _soltas.update(_O[u"s"])
_soltas = set(s for s in _soltas if s and u" " not in s)

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

# toda palavra que o app pode dizer inteira
_TODAS = set(_SIL_DE.keys())
for _N in NAS.values():
    _TODAS.update([w.lower() for w in _N[u"sim"] + _N[u"nao"]])
for _G in GAV.values():
    _TODAS.update([Pl[u"p"].lower() for Pl in _G[u"pal"].values()])
for _X in ESCR.values():
    _TODAS.add(_X[u"w"].lower())
for _X in FIMM.values():
    _TODAS.add(_X[u"r"].lower())
for _E in ERR.values():
    _TODAS.update([w.lower() for w in _E[u"ops"]])
for _T in DIF.values():
    _TODAS.update([w.lower() for w in _T[u"ops"]])
for _P2 in PAR.values():
    _TODAS.add(_P2[u"a"].lower()); _TODAS.add(_P2[u"b"].lower())
for _F in FRAS.values():
    _TODAS.update([w.lower() for w in _F[u"ops"]])
for _C in CRZ.values():
    _TODAS.add(_C[u"w"].lower())
for _C in CACA[u"pal"].values():
    _TODAS.add(_C[u"p"].lower())
for _L in LIGA.values():
    _TODAS.add(_L[u"p"].lower())
for _I in CENA[u"itens"]:
    _TODAS.add(_I[u"p"].lower())
for _T in TXT.values():
    for _l in _T[u"linhas"]:
        _TODAS.update([w.lower() for w in _l])
for _A in ACH.values():
    _TODAS.update([w.lower() for w in _A[u"fr"]])
for _X in CART[u"exem"].values():
    _TODAS.add(_X[u"p"].lower())
# ⚠️ AS PALAVRAS DO TEXTO VÊM COM A PONTUAÇÃO GRUDADA ("combinado.", "rampa."),
#    porque é assim que a criança as vê na tela. Na FALA a pontuação sai, senão
#    o texto vira "COMBINADO.." — que foi o que o `_qa/revisor.py` pegou.
for _w in sorted(_TODAS):
    _lim = _w.strip(u".,;:!?")
    if _lim:
        p(u"pal_" + ch(_lim), _lim.upper() + u".")

if not isinstance(F, dict):
    raise SystemExit(u"⛔ o `F` deixou de ser o dicionario das falas.")
_ruins = [k for k, v in F.items() if not isinstance(v, type(u""))]
if _ruins:
    raise SystemExit(u"⛔ falas que nao sao texto: %s" % u", ".join(_ruins[:6]))

# ⚠️⚠️ FALA DE DUAS PALAVRAS SAI TORTA. As exceções são NOMEADAS: são as falas
#    que a criança ouve ao TOCAR numa peça, e que têm de dizer a peça e mais nada.
_SO_A_PECA = (u"pal_", u"esc_", u"fim_", u"mn_", u"ord_", u"err_", u"dif_",
              u"par_", u"crz_", u"let_", u"diz2_", u"fra_", u"ach_", u"reg_")
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
