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
PREFIXO = u"cs_"                     # <- o prefixo desta atividade
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
p(u"capa", u"A Casinha dos Três Pontos. Trinta e cinco folhas sobre o ponto "
           u"final, o ponto de interrogação e o ponto de exclamação. Escreva o "
           u"seu nome ali embaixo e toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora olhe o caderno de qualquer matéria e "
          u"procure: quantas frases da página de hoje acabam com ponto de "
          u"interrogação? E quantas acabam com ponto de exclamação?")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por bloco da escada, LENDO os DADOS
#
# ⚠️ O QUE A VOZ DIZ TEM DE CARREGAR O PONTO. Este caderno é sobre pontuação, e
#    é o sinal que faz o Edge TTS subir a voz na pergunta e encurtar a
#    exclamação. Frase mandada para a fila sem o sinal é gravada lisa — e a
#    folha 6, que É a voz, deixaria de existir.
# ⚠️ E A DICA NUNCA DIZ O PONTO. Ela manda ESCUTAR de novo.
# ---------------------------------------------------------------------------
SINAL = {u"inter": (u"?", u"ponto de interrogação"),
         u"excl": (u"!", u"ponto de exclamação"),
         u"final": (u".", u"ponto final")}


def cq(w):
    u"""o mesmo `chaveQuadro` do app: minúscula e só as letras de a a z (o
    acento cai junto, porque em JS `[^a-z]` não poupa o é)."""
    return re.sub(r"[^a-z]", u"", (w or u"").lower())


def fecha(frase, k):
    u"""a frase com o sinal dela — é assim que a voz aprende a entonação"""
    return frase.rstrip(u" .!?") + SINAL[k][0]


p(u"nom_inter", u"Ponto de interrogação.")
p(u"nom_excl", u"Ponto de exclamação.")
p(u"nom_final", u"Ponto final.")
p(u"cacatoque", u"Toque primeiro na primeira letra da palavra.")

ENUN = [
 u"Estes são os três moradores do caderno. Leve cada nome até o desenho dele.",
 u"Ouça a frase. Ela conta uma coisa, ou pergunta uma coisa?",
 u"Agora é susto e alegria contra pergunta. Ouça o jeito de falar.",
 u"Os três juntos. Ouça a frase e escolha o ponto que fecha ela.",
 u"Mais seis frases. Diga cada uma em voz alta antes de escolher.",
 u"A frase é a mesma. O que muda é o jeito de falar. Ouça e escolha o ponto daquele jeito.",
 u"De novo a mesma frase, com outra voz. Escute com atenção.",
 u"A frase já vem pontuada. Ela conta, pergunta, ou se espanta?",
 u"Cada ponto tem a sua casinha. Leve a frase para a casa do ponto que fecha ela.",
 u"Mais frases para achar a casa. Leia cada uma em voz alta.",
 u"Agora as frases são mais compridas. Mas o fim delas continua entregando a casa.",
 u"Puxe o sinal certo até o quadradinho do fim da frase. Tocar nele também vale.",
 u"Mais três frases esperando o sinal delas.",
 u"Estas são mais difíceis. Leia com calma e escute a sua própria voz.",
 u"Toda pergunta começa com uma palavra que pede uma coisa. Qual é a desta?",
 u"Mais perguntas. Repare no que a frase está querendo saber.",
 u"Toda pergunta tem a sua resposta. Leve cada resposta até a pergunta dela.",
 u"Olhe a figura e responda. Repare: a resposta termina em ponto final.",
 u"Mais perguntas com figura. A pergunta acaba em ponto de interrogação e a "
 u"resposta em ponto final.",
 u"Toque nas palavras na ordem e monte a frase. No fim, não esqueça do ponto.",
 u"Frases mais compridas. Ouça a frase pronta antes de começar.",
 u"Esta frase saiu errada. Qual é a certa? Olhe a primeira letra e o fim dela.",
 u"Mais três para consertar. Numas falta a letra maiúscula, noutras falta o ponto.",
 u"Escreva a palavra tocando nas letras, ou digite no seu teclado.",
 u"Leia a lengalenga e toque nas palavras que terminam com ponto de "
 u"interrogação. Depois confira.",
 u"Agora ache as que terminam com ponto de exclamação.",
 u"Ache cada palavra: toque na primeira letra e depois na última.",
 u"As duas frases têm as mesmas palavras. Só uma está com o ponto certo.",
 u"Mais quatro para revisar. Leia cada uma do jeito que o ponto manda.",
 u"Esta história ficou sem pontos. Feche cada frase.",
 u"O fim da história. Escute o jeito de falar de cada frase.",
 u"Agora é a sua vez de inventar. Escreva uma palavra que sirva para cada pedido.",
 u"Olhe a cena e a frase. Qual ponto combina com ela?",
 u"Mais três cenas. A mesma figura pode pedir pontos diferentes: quem manda é a frase.",
 u"Você já sabe tudo isto. Agora os três nomes: leve cada frase para a linha dela."]
assert len(ENUN) == 35, len(ENUN)
for _i, _t in enumerate(ENUN):
    p(u"p%denun" % (_i + 1), _t)

# ⭐ o elogio muda de folha em folha: repetir a mesma frase trinta e cinco vezes
#   é o "isso eu já ouvi" da voz.
ELOGIO = [u"Isso mesmo!", u"Muito bem!", u"Você acertou!", u"Boa!",
          u"Exatamente!", u"É isso aí!"]
PEDE_ESCUTA = [
 u"Diga a frase em voz alta. A sua voz sobe no fim, ou desce?",
 u"Escute de novo: é uma pergunta, um susto, ou só uma coisa contada?",
 u"Toque no alto-falante e ouça o fim da frase mais uma vez.",
 u"Repare no começo da frase: tem alguma palavra que pergunta?"]


def elogio(n):
    return ELOGIO[n % len(ELOGIO)]


def escuta(n):
    return PEDE_ESCUTA[n % len(PEDE_ESCUTA)]


def porFolha(pi, chaves, diz):
    u"""o certo e a dica de cada item de uma folha, na ordem do pote"""
    for _n, _k in enumerate(chaves):
        p(u"certo%d_%s" % (pi, _k), diz(_k, _n))
        p(u"dica%d_%s" % (pi, _k), escuta(_n + pi))


ITENS = bloco(u"ITENS")


def pote(pi):
    v = ITENS[u"p%d" % pi]
    return v[0] if v and isinstance(v[0], list) else v


# --- 1: quem é quem --------------------------------------------------------
LIGA = bloco(u"LIGA")
for _k, _L in LIGA.items():
    p(u"certo1_" + _k, elogio(0) + u" " + _L[u"p"] + u". " + _L[u"d"])
    p(u"dica1_" + _k, u"Olhe bem o desenho: qual dos três sinais ele é?")

# --- 2 a 5: qual ponto fecha a frase --------------------------------------
PON = bloco(u"PON")
for _pi in (2, 3, 4, 5):
    for _n, _k in enumerate(pote(_pi)):
        _P = PON[_k]
        p(u"fra_" + _k, fecha(_P[u"f"], _P[u"r"]))
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + fecha(_P[u"f"], _P[u"r"])
          + u" Termina com " + SINAL[_P[u"r"]][1] + u".")
        p(u"dica%d_%s" % (_pi, _k), escuta(_n + _pi))

# --- 6 e 7: a mesma frase, três vozes -------------------------------------
VOZES = bloco(u"VOZ")
for _pi in (6, 7):
    for _n, _k in enumerate(pote(_pi)):
        _V = VOZES[_k]
        p(u"voz_" + _k, fecha(_V[u"b"], _V[u"pede"]))
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" Do jeito que eu falei, a "
          u"frase pede " + SINAL[_V[u"pede"]][1] + u".")
        p(u"dica%d_%s" % (_pi, _k), u"Ouça de novo, só o fim. A minha voz sobe, "
          u"desce, ou dá um susto?")

# --- 8: que tipo de frase é? ----------------------------------------------
TIPO = bloco(u"TIPO")
for _n, _k in enumerate(pote(8)):
    _T = TIPO[_k]
    p(u"tip_" + _k, _T[u"f"])
    p(u"certo8_" + _k, elogio(_n) + u" Ela acaba com " + SINAL[_T[u"r"]][1] + u".")
    p(u"dica8_" + _k, u"Olhe o último sinal da frase, depois da última palavra.")

# --- 9, 10 e 11: a casinha da pontuação -----------------------------------
GAV = bloco(u"GAV")
for _gk, _G in GAV.items():
    for _C in _G[u"cols"]:
        p(u"gav_%s_%s" % (_gk, _C[u"k"]),
          u"Casa do " + SINAL[_C[u"k"]][1] + u".")
for _pi, _gk in ((9, u"gA"), (10, u"gB"), (11, u"gC")):
    for _n, _k in enumerate(pote(_pi)):
        _X = GAV[_gk][u"pal"][_k]
        p(u"diz2_%s_%s" % (_gk, _k), _X[u"p"])
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _X[u"p"] + u" Mora na "
          u"casa do " + SINAL[_X[u"c"]][1] + u".")
        p(u"dica%d_%s" % (_pi, _k), u"Leia a frase em voz alta e escute o fim dela.")

# --- 12, 13 e 14: arraste o sinal -----------------------------------------
ARR = bloco(u"ARR")
for _pi in (12, 13, 14):
    for _n, _k in enumerate(pote(_pi)):
        _A = ARR[_k]
        p(u"arr_" + _k, fecha(_A[u"f"], _A[u"r"]))
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" O quadradinho era do "
          + SINAL[_A[u"r"]][1] + u".")
        p(u"dica%d_%s" % (_pi, _k), escuta(_n + _pi))

# --- 15 e 16: a palavra que abre a pergunta -------------------------------
QUE = bloco(u"QUE")
for _pi in (15, 16):
    for _n, _k in enumerate(pote(_pi)):
        _Q = QUE[_k]
        p(u"que_" + _k, u"Falta a palavra do começo. " + _Q[u"z"])
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _Q[u"r"] + u" " + _Q[u"z"])
        p(u"dica%d_%s" % (_pi, _k), u"Pense no que a pergunta quer saber: uma "
          u"pessoa, um lugar, um dia, ou um jeito?")
        for _w in _Q[u"ops"]:
            p(u"pal_" + cq(_w), _w + u".")

# --- 17: ligue a pergunta à resposta --------------------------------------
PAR = bloco(u"PAR")
for _n, _k in enumerate(pote(17)):
    _P = PAR[_k]
    p(u"prg_" + _k, _P[u"p"])
    p(u"res_" + _k, _P[u"r"])
    p(u"certo17_" + _k, elogio(_n) + u" " + _P[u"p"] + u" " + _P[u"r"])
    p(u"dica17_" + _k, u"Ouça a pergunta de novo e veja de que ela está falando.")

# --- 18 e 19: responda olhando a figura -----------------------------------
RESP = bloco(u"RESPF")
for _pi in (18, 19):
    for _n, _k in enumerate(pote(_pi)):
        _R = RESP[_k]
        p(u"rsp_" + _k, _R[u"p"])
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _R[u"r"] + u" A resposta "
          u"acabou em ponto final.")
        p(u"dica%d_%s" % (_pi, _k), u"Olhe bem a figura antes de escolher.")
        for _w in _R[u"ops"]:
            p(u"pal_" + cq(_w), _w)

# --- 20 e 21: as palavras se embaralharam ---------------------------------
ORD = bloco(u"ORD")
for _pi in (20, 21):
    for _n, _k in enumerate(pote(_pi)):
        _O = ORD[_k]
        p(u"ord_" + _k, fecha(_O[u"r"], _O[u"p"]))
        # ⚠️ a fala de cada palavra nasce da POSIÇÃO: "não" e "no" moram na
        #    mesma frase e a chave da grafia devolveria a mesma para as duas.
        for _j, _w in enumerate(_O[u"r"].split(u" ")):
            p(u"ord_%s_w%d" % (_k, _j), _w)
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + fecha(_O[u"r"], _O[u"p"]))
        p(u"dica%d_%s" % (_pi, _k), u"Ouça a frase pronta e veja qual palavra "
          u"vem primeiro.")

# --- 22 e 23: conserte a frase --------------------------------------------
COR = bloco(u"COR_")
for _pi in (22, 23):
    for _n, _k in enumerate(pote(_pi)):
        _C = COR[_k]
        p(u"cor_" + _k, _C[u"certa"])
        p(u"pal_" + cq(_C[u"certa"]), _C[u"certa"])
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _C[u"certa"] +
          (u" Começa com letra maiúscula." if _C[u"falta"] == u"maius"
           else u" E termina com o ponto certo."))
        p(u"dica%d_%s" % (_pi, _k), u"Compare as duas: uma coisa muda do começo "
          u"para o fim. Onde é?")

# --- 24: escreva a palavra da pergunta ------------------------------------
ESCR = bloco(u"ESCR")
for _n, _k in enumerate(pote(24)):
    _X = ESCR[_k]
    p(u"esc_" + _k, _X[u"d"])
    p(u"certo24_" + _k, elogio(_n) + u" " + _X[u"w"] + u".")
    p(u"dica24_" + _k, u"Escute a pista de novo e pense na primeira letra.")

# --- 25 e 26: ache no texto -----------------------------------------------
TXT = bloco(u"TXT")
for _pi, _tk in ((25, u"t1"), (26, u"t2")):
    _T = TXT[_tk]
    _nw = 0
    for _lin in _T[u"linhas"]:
        for _w in _lin:
            p(u"tx%d_%d" % (_pi, _nw), _w if _w != u"—" else u"Fala.")
            _nw += 1
    p(u"certo%d_t" % _pi, u"Muito bem! Você achou as duas.")
    p(u"dica%d_t" % _pi, u"Olhe o último sinal de cada linha, depois da última "
      u"palavra dela.")

# --- 27: o caça-palavras dos sinais ---------------------------------------
CACA = bloco(u"CACA")
for _n, _k in enumerate(pote(27)):
    _C = CACA[u"pal"][_k]
    p(u"pal_" + cq(_C[u"p"]), _C[u"p"] + u".")
    p(u"certo27_" + _k, elogio(_n) + u" " + _C[u"p"] + u".")
    p(u"dica27_" + _k, u"Procure a primeira letra da palavra e siga para o lado.")

# --- 28 e 29: qual está pontuada certa? -----------------------------------
CERT = bloco(u"CERT")
for _pi in (28, 29):
    for _n, _k in enumerate(pote(_pi)):
        _C = CERT[_k]
        p(u"cer_" + _k, _C[u"r"])
        for _w in _C[u"ops"]:
            p(u"pal_" + cq(_w), _w)
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _C[u"r"])
        p(u"dica%d_%s" % (_pi, _k), u"Ouça a frase e repare no fim: a voz sobe, "
          u"desce, ou se espanta?")

# --- 30 e 31: pontue a história -------------------------------------------
HIST = bloco(u"HIST")
for _pi in (30, 31):
    for _n, _k in enumerate(pote(_pi)):
        _H = HIST[_k]
        p(u"his_" + _k, fecha(_H[u"f"], _H[u"r"]))
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + fecha(_H[u"f"], _H[u"r"]))
        p(u"dica%d_%s" % (_pi, _k), escuta(_n + _pi))

# --- 32: invente a sua palavra --------------------------------------------
DESA = bloco(u"DESA")
for _n, _k in enumerate(pote(32)):
    _X = DESA[_k]
    p(u"des_" + _k, u"Escreva " + _X[u"q"] + u".")
    p(u"certo32_" + _k, u"Essa vale! A palavra é sua.")
    p(u"dica32_" + _k, u"Pense numa palavra que caiba no pedido. Vale mais de uma.")

# --- 33 e 34: a cena pede o sinal -----------------------------------------
CENA = bloco(u"CENA")
for _pi in (33, 34):
    for _n, _k in enumerate(pote(_pi)):
        _C = CENA[_k]
        p(u"cen_" + _k, fecha(_C[u"p"], _C[u"r"]))
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + fecha(_C[u"p"], _C[u"r"]))
        p(u"dica%d_%s" % (_pi, _k), u"Olhe a cena e diga a frase do jeito que ela "
          u"pede. Escute a sua voz.")

# --- 35: o cartaz que você leva -------------------------------------------
CART = bloco(u"CART")
for _L in CART[u"linhas"]:
    p(u"cart_" + _L[u"k"], _L[u"t"] + u" " + _L[u"d"] + u". Por exemplo: " + _L[u"e"])
for _n, _k in enumerate(pote(35)):
    _X = CART[u"exem"][_k]
    p(u"pal_" + cq(_X[u"p"]), _X[u"p"])
    p(u"certo35_" + _k, elogio(_n) + u" " + _X[u"p"] + u" É do " +
      SINAL[_X[u"c"]][1] + u".")
    p(u"dica35_" + _k, u"Leia a frase até o fim e olhe o sinal que fecha ela.")


# ==============================================================================
#  AS SÍLABAS FALADAS — e este bloco é obrigatório em caderno que fale sílaba
#
#  ⚠️⚠️ POR QUE NÃO DÁ PARA SINTETIZAR A SÍLABA SOLTA (e a casa já pagou por
#     isto DUAS vezes — set/2026 e 16/set/2026, as duas o Marcos ouvindo):
#     a voz não lê SOM, lê PALAVRA. Entregue "SA" a ela e ela soletra "esse-á";
#     "VA" vira "vê-á"; "ÇÃ" ela nem tenta, porque ç não começa palavra em
#     português. Escrever a sílaba "como se fala" conserta UM caso e nunca
#     fecha a família.
#
#  O QUE FUNCIONA é o contrário: gravar a PALAVRA INTEIRA — que a voz pronuncia
#  certo, porque é palavra de verdade — alinhar letra a letra com o
#  `ctc-forced-aligner` e CORTAR a sílaba de dentro dela. Quem faz isso é o
#  `_padrao/silabas_voz.py`, dentro do `entregar.yml`, lendo o `silabas.json`
#  que sai daqui. O portão é o `_qa/silabas.py`.
#
#  COMO SE USA: para cada palavra do caderno, uma linha
#      _reg(u"CAVALO", [u"CA", u"VA", u"LO"])
#  e, no app, a sílaba fala por `falarSilaba(null, 0, "VA")` — nunca por
#  `falar("sil_va")`. Caderno que não fala sílaba não escreve nada: o
#  `silabas.json` sai com `"palavras": {}` e o `entregar.yml` nem baixa o
#  alinhador por ele.
#
#  ⚠️ NÃO HÁ FALA DE RESERVA POR SÍLABA. Faltando o recorte, o app diz a
#     PALAVRA INTEIRA. Uma reserva sintetizada seria o defeito voltando pela
#     porta dos fundos — e calado, que é pior.
# ==============================================================================
_SIL_DE = {}          # palavra -> [sílabas, NA ORDEM da palavra]
_MAPA_SIL = {}        # sílaba  -> [palavra, posição]
_RECUSADAS = []


def _reg(palavra, silabas):
    u"""⚠️ A LISTA TEM DE ESTAR NA ORDEM DA PALAVRA. O alinhador corta pelos
    limites das letras: ["RO","CAR"] para CARRO faz sair "ro" onde devia sair
    "car" — e a criança ouve o pedaço errado, sem erro nenhum na tela. Folha de
    ORDENAR guarda as sílabas EMBARALHADAS: passe-as por `_ordena` antes.
    ⚠️ E ganha sempre a partição MAIS FINA: "PIPO"+"CA" fecha PIPOCA sem ser
    separação silábica, e sobrescrevendo PI-PO-CA deixaria a sílaba PI muda."""
    silabas = list(silabas)
    if u"".join(silabas).upper() != palavra.upper():
        _RECUSADAS.append((palavra, silabas))
        return
    velha = _SIL_DE.get(palavra.lower())
    if velha and len(velha) >= len(silabas):
        return
    _SIL_DE[palavra.lower()] = silabas


def _ordena(palavra, embaralhadas):
    u"""as mesmas sílabas na ORDEM em que formam a palavra — sem inventar
    nenhuma: encaixa da esquerda para a direita e desiste se não fechar."""
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


def _achaSilaba(s):
    u"""a palavra de onde a sílaba será recortada. Ganha a MAIS CURTA: menos
    letras na gravação, menos lugar para o alinhador errar."""
    cand = [_w for _w in sorted(_SIL_DE) if s in _SIL_DE[_w]]
    if not cand:
        return None
    _w = min(cand, key=lambda w: (len(_SIL_DE[w]), len(w), w))
    return [_w, _SIL_DE[_w].index(s)]


def _mapeia(soltas):
    u"""monta o SILMAP das sílabas que o app fala sozinhas, e DEVOLVE as órfãs.
    ⚠️ Sílaba órfã não é erro — o app diz a palavra inteira — mas tem de sair
    IMPRESSA, senão aquele botão emudece sem ninguém saber. Distratora que não
    mora em palavra nenhuma do caderno pede uma PALAVRA-CARREGADORA: uma
    palavra de verdade, curta, registrada só para ser gravada e cortada."""
    orfas = []
    for _s in sorted(set(soltas)):
        _achou = _achaSilaba(_s)
        if _achou:
            _MAPA_SIL[_s] = _achou
        else:
            orfas.append(_s)
    # e a PALAVRA INTEIRA de cada uma precisa existir como fala: é dela que o
    # recorte sai, e é ela que o app diz quando o recorte falta.
    for _w in sorted(_SIL_DE):
        p(u"pal_" + ch(_w), _w.upper() + u".")
    return orfas


_ORFAS = _mapeia([])          # <- passe aqui TODA sílaba que o app fala sozinha


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
if _ORFAS:
    print(u"   \u26a0\ufe0f %d silaba(s) SEM palavra de origem (o app dira a palavra "
          u"inteira): %s" % (len(_ORFAS), u", ".join(_ORFAS)))
if _RECUSADAS:
    print(u"   \u26a0\ufe0f %d lista(s) recusada(s) por nao formarem a palavra: %s"
          % (len(_RECUSADAS), u", ".join(
              u"%s=%s" % (w, u"-".join(sl)) for w, sl in _RECUSADAS[:8])))
