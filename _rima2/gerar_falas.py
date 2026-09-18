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
PREFIXO = u"qd_"                     # <- o prefixo desta atividade
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
    u"""⚠️ TODA fala passa por aqui LIMPA. Não é enfeite: quando a frase perde o
    travessão do discurso direto (`— Socorro! — gritou`), sobram dois espaços; a
    pista `ele ___ (correr)` vira `ele lacuna , verbo correr`; e um texto que já
    acaba em ponto ganha outro e sai `ela..`. Os TRÊS aconteceram neste caderno e
    quem pegou foi o portão `0o` (`_qa/revisor.py`) — a criança OUVIRIA isso."""
    t = re.sub(r"\s+", u" ", (v or u"")).strip()
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)     # espaço antes da pontuação
    t = re.sub(r"([,.;:!?])\1+", r"\1", t)     # ".." e ",,"
    t = re.sub(r"\.\s*\.", u".", t)
    F[k] = t






# ---------------------------------------------------------------------------
# AS FALAS DO MOTOR — estas toda folha viva tem
# ---------------------------------------------------------------------------
p(u"capa", u"A Parlenda que Rima. Trinta e cinco folhas sobre as parlendas e as quadrinhas: "
           u"as palavras que terminam com o mesmo pedacinho. Escreva o seu nome ali embaixo e toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa peça do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na gaveta dela.")
p(u"quase", u"Quase! Tente de novo.")
p(u"cacatoque", u"Toque primeiro na primeira letra da palavra.")
p(u"pegue_lapis", u"Primeiro pegue uma canetinha ali em cima. Depois toque na palavra.")
p(u"novoCaderno", u"Caderno novo! Escreva o seu nome e toque em Começar.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora um desafio para levar: pergunte em casa qual parlenda a sua família sabe de cor. Tem a do Uni duni tê, a do Corre cutia, a do Um, dois, feijão com arroz. Escute e descubra onde está a rima de cada uma.")


def semLacuna(s):
    u"""⚠️ A LACUNA NÃO SE NARRA (regra da casa, `SEQUENCIAS-DIDATICAS §2c`), e
    neste caderno ela some com reticências: o verso fica em suspenso, que é
    exatamente como um adulto o leria em voz alta para a criança completar —
    *"O cachimbo é de barro, bate no…"*. A correção diz o verso INTEIRO."""
    return re.sub(r"\s*_{2,}\s*\.?", u"…", lp(s))


ENUN = [
 u"Diga o nome da figura em voz alta. Depois toque na palavra que termina com o mesmo pedacinho.",
 u"Agora sem desenho: só o ouvido. Diga a palavra e cada opção em voz alta.",
 u"Toque numa figura e depois na palavra que rima com ela.",
 u"A parlenda perdeu a última palavra de cada verso. A figura ajuda: toque na palavra que rima.",
 u"Agora sem figura, em três parlendas diferentes. Diga o verso em voz alta antes de escolher.",
 u"Cada verso está sem o fim. Puxe a palavra até o verso dela, ou toque numa e depois no outro.",
 u"Leia a parlenda e toque nas palavras que terminam com o mesmo pedacinho. Depois confira.",
 u"Nesta, toque só nas palavras que terminam como VOVÓ. Depois confira.",
 u"Esta tem três pares escondidos. Toque em todas as palavras que rimam. Depois confira.",
 u"A parlenda foi fatiada. Puxe cada verso para o lugar dele, do primeiro ao último.",
 u"Cada verso está partido ao meio. Ligue o começo ao fim que rima com ele.",
 u"Só uma das três fecha o verso rimando. As outras cabem no sentido, mas não no som.",
 u"Agora você escreve. As casinhas dizem quantas letras tem a palavra que fecha o verso.",
 u"Outras quatro parlendas, o mesmo trabalho: escreva a palavra do fim.",
 u"Olhe o desenho e escreva o nome dele. A pista diz com qual palavra ele rima.",
 u"Agora não há lista: a rima é sua. Pense numa palavra que termine igual e escreva.",
 u"Mais quatro. Vale qualquer palavra de verdade que termine com o mesmo pedacinho.",
 u"Nestas três, duas terminam igual e uma não. Toque na que não combina.",
 u"No lugar da última palavra tem um desenho. Toque na palavra que ele quer dizer.",
 u"O desenho está dentro do verso, no lugar da palavra. Escreva o nome dele.",
 u"Sem desenho agora: só o verso e a pista. Escreva a palavra que falta.",
 u"Você já leu esta parlenda na folha 8. Agora responda: o que ela conta?",
 u"Leia com atenção: O macaco foi à feira, não teve o que comprar. Comprou uma cadeira pra comadre "
 u"se sentar. A cadeira esborrachou, coitada da comadre, foi parar no corredor.",
 u"Leia a quadrinha: Rato Luca rói o queijo, a vaca faz angu. O gato chama o pato pra festa do tatu.",
 u"Ache na grade a palavra que a pista pede: toque na primeira letra e depois na última.",
 u"Outra grade. Nela as palavras estão sem acento: procure CHAO, não chão.",
 u"Toque numa pista, escute e escreva a palavra que rima.",
 u"Leia o par em voz alta. As duas palavras terminam igual, ou não? Leve para a gaveta certa.",
 u"Agora são três gavetas, uma para cada fim. Leia a palavra e escute o fim dela.",
 u"Em cada grupo há três que rimam e três que não. Marque as três e toque em Conferir.",
 u"E se a gente trocar a palavra do fim? A parlenda tem que continuar rimando. Qual serve?",
 u"Agora a palavra do fim é nova: não é a da parlenda de sempre. Mas ainda rima. "
 u"Puxe cada uma para o seu verso.",
 u"Agora a palavra nova é sua para escrever. Ela tem que rimar igual à antiga.",
 u"Agora a quadrinha é sua. Escreva a palavra que fecha o seu verso, rimando.",
 u"Você já fez tudo isto sem saber os nomes. Agora eles: leve cada exemplo para a linha dele."]
assert len(ENUN) == 35, len(ENUN)
for _i, _t in enumerate(ENUN):
    p(u"p%denun" % (_i + 1), _t)

ELOGIO = [u"Isso mesmo!", u"Muito bem!", u"Você acertou!", u"Boa!", u"Exatamente!", u"É isso aí!"]
DICAS = [u"Diga as duas palavras em voz alta, bem devagar, e escute só o fim.",
         u"Tape o começo da palavra com o dedo e leia só o pedacinho do fim.",
         u"Rimar é terminar com o mesmo som. Olhe as últimas letras de cada uma.",
         u"Cante o verso como se fosse uma música: a palavra certa cai sozinha."]


def elogio(n):
    return ELOGIO[n % len(ELOGIO)]


def dica(n):
    return DICAS[n % len(DICAS)]


ITENS = bloco(u"ITENS")


def pote(pi):
    v = ITENS[u"p%d" % pi]
    return v[0] if v and isinstance(v[0], list) else v


def palavras(*ws):
    u"""⚠️ A CHAVE TRANSLITERA O ACENTO (`ch`), não o apaga — num caderno de RIMA
    isso é o que separa `po` de `pe` e `mao` de `mae`."""
    for _w in ws:
        if _w:
            _t = lp(_w)
            _t = _t[0].upper() + _t[1:]
            p(u"pal_" + ch(_w), _t if _t[-1:] in u".!?" else _t + u".")


# --- 1, 2 e 18: qual rima ----------------------------------------------------
for _pi, _nome in ((1, u"RIMFIG"), (2, u"RIMPAL"), (18, u"INTRUSO")):
    _D = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _X = _D[_k]
        palavras(*_X[u"ops"])
        if _pi == 18:
            p(u"prg_" + _k, u"Qual é a intrusa?")
            p(u"certo18_" + _k, elogio(_n) + u" %s não termina como as outras duas." % _X[u"r"].capitalize())
            p(u"dica18_" + _k, u"Diga as três em voz alta, uma depois da outra. Duas soam parecidas no fim.")
        else:
            p(u"prg_" + _k, u"Qual rima com %s?" % _X[u"n"])
            p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" %s e %s terminam igual."
              % (_X[u"n"].capitalize(), _X[u"r"]))
            p(u"dica%d_%s" % (_pi, _k), dica(_n))

# --- 3: ligar a figura à palavra que rima ------------------------------------
LIGR = bloco(u"LIGR")
for _n, _k in enumerate(pote(3)):
    _L = LIGR[_k]
    palavras(_L[u"b"], _L[u"n"])
    p(u"fig_" + _k, _L[u"n"].capitalize() + u".")
    p(u"certo3_" + _k, elogio(_n) + u" %s e %s terminam igual."
      % (_L[u"n"].capitalize(), _L[u"b"]))
    p(u"dica3_" + _k, u"Diga o nome da figura e depois cada palavra do lado direito. Só uma acaba igual.")

# --- 4, 5, 12, 19, 22, 23, 24 e 31: a frase com lacuna -----------------------
for _pi, _nome in ((4, u"VERSO1"), (5, u"VERSO2"), (12, u"FECHA"), (19, u"ENIG"),
                   (22, u"PERG1"), (23, u"PERG2"), (24, u"PERG3"), (31, u"TROCA")):
    _D = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _X = _D[_k]
        palavras(*_X[u"ops"])
        p(u"fra_" + _k, semLacuna(_X[u"f"]))
        _cheia = lp(_X[u"f"]).replace(u"___", _X[u"r"]).replace(u"…", u" " + _X[u"r"]).strip()
        _cheia = _cheia[0].upper() + _cheia[1:]
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _cheia)
        if _pi in (22, 23, 24):
            p(u"dica%d_%s" % (_pi, _k), u"Leia a parlenda de novo, devagar. A resposta está dentro dela.")
        else:
            p(u"dica%d_%s" % (_pi, _k), dica(_n))

# --- 6, 10 e 32: puxar para dentro do verso ----------------------------------
for _pi, _nome in ((6, u"SOLTA1"), (32, u"SOLTA2")):
    _D = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _X = _D[_k]
        palavras(_X[u"rot"])
        p(u"vrs_" + _k, lp(_X[u"v"]))
        _v = (lp(_X[u"v"]).replace(u"…", u"").strip() + u" " + _X[u"rot"] + u".")
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _v[0].upper() + _v[1:])
        p(u"dica%d_%s" % (_pi, _k), dica(_n))
ORDEM = bloco(u"ORDEM")
for _n, _k in enumerate(pote(10)):
    _X = ORDEM[_k]
    p(u"vrs_" + _k, lp(_X[u"v"]))
    p(u"pos_" + _k, _X[u"pos"] + u".")
    p(u"certo10_" + _k, elogio(_n) + u" %s: %s." % (_X[u"pos"], _X[u"v"]))
    p(u"dica10_" + _k, u"Cante a parlenda inteira na sua cabeça. Qual verso vem primeiro?")

# --- 7, 8 e 9: dentro do texto ------------------------------------------------
TXT = bloco(u"TXT")
for _pi, _tk in ((7, u"tx1"), (8, u"tx2"), (9, u"tx3")):
    _T = TXT[_tk]
    _nw = 0
    for _lin in _T[u"linhas"]:
        for _w in _lin:
            p(u"tx%d_%d" % (_pi, _nw), _w)
            _nw += 1
    p(u"certo%d_t" % _pi, u"Muito bem! As palavras que rimam eram " + u", ".join(_T[u"ok"]) + u".")
    p(u"dica%d_t" % _pi, u"Leia o texto de novo em voz alta, verso por verso. "
                         u"A rima está quase sempre na ÚLTIMA palavra de cada verso.")

# --- 11: ligar o começo do verso ao fim ---------------------------------------
LIGV = bloco(u"LIGV")
for _n, _k in enumerate(pote(11)):
    _L = LIGV[_k]
    p(u"lg_" + _k + u"_e", lp(_L[u"a"]))
    p(u"lg_" + _k + u"_d", lp(_L[u"b"]).capitalize() + u".")
    p(u"certo11_" + _k, elogio(_n) + u" " + lp(_L[u"a"]) + u" " + _L[u"b"] + u".")
    p(u"dica11_" + _k, u"Diga o começo do verso e depois cada fim. Só um cai no ritmo e rima.")

# --- 13, 14, 15, 20, 21 e 33: escrever nas casinhas ---------------------------
for _pi, _nome in ((13, u"GRD1"), (14, u"GRD2"), (15, u"GRD3"),
                   (20, u"GRD4"), (21, u"GRD5"), (33, u"GRD6")):
    _D = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _G = _D[_k]
        p(u"grd_" + _k, semLacuna(_G[u"p"]) + u" " + lp(_G[u"d"]))
        # ⚠️ o `strip()` não é enfeite: quando a lacuna abre o verso ("… choca,
        #    comeu minhoca"), o primeiro caractere é um ESPAÇO e o `upper()` caía
        #    nele — a voz dizia "Muito bem! galinha choca", com minúscula, e o
        #    portão do revisor acusou.
        _c = lp(_G[u"p"]).replace(u"___", _G[u"w"].lower()).replace(u"…", u" " + _G[u"w"].lower()).strip()
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " + _c[0].upper() + _c[1:])
        p(u"dica%d_%s" % (_pi, _k),
          u"Conte as casinhas e diga a palavra bem devagar, letra por letra. "
          u"A pista diz com qual palavra ela rima.")

# --- 16, 17 e 34: a rima é sua ------------------------------------------------
for _pi, _nome in ((16, u"LIVRE1"), (17, u"LIVRE2"), (34, u"PROD")):
    _D = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _X = _D[_k]
        p(u"prd_" + _k, u"Escreva " + _X[u"q"] + u".")
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" A rima é sua e está certa.")
        p(u"dica%d_%s" % (_pi, _k),
          u"Fale a palavra em voz alta e vá trocando o começo dela: "
          u"sol, anzol, farol. Alguma dessas serve?")

# --- 25 e 26: os caça-rimas ---------------------------------------------------
for _pi, _nome in ((25, u"CACA"), (26, u"CACA2")):
    _C = bloco(_nome)
    for _n, _k in enumerate(pote(_pi)):
        _P = _C[u"pal"][_k]
        p(u"cp_" + _k, u"Ache a que " + _P[u"pista"].lower() + u".")
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" Achou.")

# --- 27: a cruzadinha ---------------------------------------------------------
CRZD = bloco(u"CRZD")
for _n, _k in enumerate(pote(27)):
    _P = CRZD[_k]
    p(u"crz_" + _k, lp(_P[u"d"]))
    p(u"certo27_" + _k, elogio(_n) + u" " + lp(_P[u"d"]).replace(u"…", u"") + u" " + _P[u"p"].capitalize() + u".")
    p(u"dica27_" + _k, u"Conte as casinhas e diga a palavra em voz alta, escutando o fim.")

# --- 28 e 29: as gavetas ------------------------------------------------------
GAV = bloco(u"GAV")
_GAVTXT = {u"s": u"Gaveta dos pares que rimam.", u"n": u"Gaveta dos que não rimam.",
           u"o": u"Gaveta das que terminam como vovó.",
           u"e": u"Gaveta das que terminam como panela.",
           u"a": u"Gaveta das que terminam como chão."}
for _gk, _G in GAV.items():
    for _C in _G[u"cols"]:
        p(u"gav_%s_%s" % (_gk, _C[u"k"]), _GAVTXT[_C[u"k"]])
_GAVCERTO = {u"s": u": as duas terminam igual.", u"n": u": elas não terminam igual.",
             u" ": u"", u"o": u" termina como vovó.", u"e": u" termina como panela.",
             u"a": u" termina como chão."}
_GAVDICA = {u"gA": u"Diga as duas palavras uma depois da outra e escute só o fim delas.",
            u"gB": u"Fale a palavra e pare no último pedacinho. Ele é ó, é ela, ou é ão?"}
for _pi, _gk in ((28, u"gA"), (29, u"gB")):
    for _n, _k in enumerate(pote(_pi)):
        _X = GAV[_gk][u"pal"][_k]
        p(u"diz2_%s_%s" % (_gk, _k), lp(_X[u"p"]).capitalize() + u".")
        p(u"certo%d_%s" % (_pi, _k), elogio(_n) + u" " +
          lp(_X[u"p"]).capitalize() + _GAVCERTO[_X[u"c"]])
        p(u"dica%d_%s" % (_pi, _k), _GAVDICA[_gk])

# --- 30: marque várias ---------------------------------------------------------
MARQ = bloco(u"MARQ")
for _n, _k in enumerate(pote(30)):
    _M = MARQ[_k]
    palavras(*[_q[u"t"] for _q in _M[u"pecas"]])
    _ok = [_q[u"t"] for _q in _M[u"pecas"] if _q[u"ok"]]
    p(u"certo30_" + _k, elogio(_n) + u" As que rimam são " + u", ".join(_ok) + u".")
    p(u"dica30_" + _k, u"Vá uma por uma, dizendo a palavra do alto junto com ela. "
                       u"Quando as duas acabam igual, é rima.")

# --- 35: o cartaz ⭐ os nomes vêm por último ------------------------------------
CART = bloco(u"CART")
for _L in CART[u"linhas"]:
    p(u"cart_" + _L[u"k"], u"%s: %s. Por exemplo, %s." % (_L[u"t"].capitalize(), _L[u"d"], _L[u"e"]))
_CARTCERTO = {u"v": u" é um verso: uma linha da parlenda.",
              u"e": u" é a estrofe: o grupo de versos.",
              u"r": u" é uma rima: duas palavras com o fim igual."}
for _n, _k in enumerate(pote(35)):
    _X = CART[u"exem"][_k]
    p(u"ex_" + _k, lp(_X[u"p"]).capitalize() + u".")
    p(u"certo35_" + _k, elogio(_n) + u" " + lp(_X[u"p"]).capitalize() + _CARTCERTO[_X[u"c"]])
    p(u"dica35_" + _k, u"Olhe o exemplo que já está em cada linha do cartaz e compare com este.")


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
