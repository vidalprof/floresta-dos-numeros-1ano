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
PREFIXO = u"dd3_"                     # <- o prefixo desta atividade
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
    # ⚠️ SEM O `"?` DOS DOIS LADOS, e isso foi conserto de 20/set/2026.
    #    Esta linha normaliza chave sem aspas (`chave:` -> `"chave":`). Com o
    #    `"?` ela também casava DENTRO de uma string: a opção
    #        ["b", "Não: é um MÚSCULO que ajuda o ar a entrar"]
    #    virava  ["b", "Não": é um MÚSCULO ...]  e o json.loads morria com
    #    "Expecting ',' delimiter", sem dizer uma palavra sobre a causa.
    #    Qualquer caderno com DOIS-PONTOS dentro de um texto caía nisso.
    #    Chave já entre aspas não precisa de conserto nenhum — então a regex
    #    só olha as SEM aspas, e string nenhuma é tocada.
    txt = re.sub(r'([\{,]\s*)([A-Za-zÀ-ÿ_0-9]+)\s*:', r'\1"\2":', txt)
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
p(u"capa", u"Aprendendo a divisão: repartir em partes iguais, medir e o "
           u"resto. Trinta e cinco folhas para repartir com a mão, medir em "
           u"grupos e descobrir o que sobra. Escreva o seu nome ali embaixo e "
           u"toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"toque_palavra", u"Primeiro toque numa peça ali embaixo. Depois toque no pote.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora você reparte, mede, sabe o que sobra e "
          u"faz a conta de volta. E fica a pergunta: quantos dias tem a quarta "
          u"parte de um mês de vinte e oito dias?")

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


# (este caderno nao fala silaba solta: a chamada do `_mapeia` mora no fim
#  da secao das folhas, e vai vazia de proposito)


# ---------------------------------------------------------------------------
# A SAÍDA
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por bloco, LENDO OS DADOS do index.html.
#
# ⚠️ UMA FONTE SÓ. Se a frase da tela morasse aqui e lá, a voz diria uma coisa
#    e a folha mostraria outra.
# ⚠️ A DICA NUNCA ENTREGA A RESPOSTA. Ela diz o que FAZER — *"ponha uma peça em
#    cada pote e dê a volta"* —, nunca *"são quatro"*. Quem mede é o portão `0j`.
# ---------------------------------------------------------------------------

EXT = {0: u"zero", 1: u"um", 2: u"dois", 3: u"três", 4: u"quatro", 5: u"cinco",
       6: u"seis", 7: u"sete", 8: u"oito", 9: u"nove", 10: u"dez",
       11: u"onze", 12: u"doze"}


def nu(n):
    return EXT.get(n, unicode(n) if str is bytes else str(n))


def umSo(w):
    return w[:-1] if w.endswith(u"s") else w


# ---- os números que a criança escolhe, e as contas que ela ouve ------------
# ⚠️ ATÉ 30, não até 12: o leque de opções ANDA quando a resposta passa do teto
#    (ver `opNumeros` no folhas.js), e opção sem voz é alto-falante mudo. A maior
#    resposta deste caderno é 24 (48 bolinhos de 2 em 2), e a janela dela vai até
#    29 — daí o 30, que é a margem. Gravar até 99 seria setenta mp3 que ninguém
#    ouve.
for _n in range(0, 31):
    p(u"num_%d" % _n, nu(_n) + u".")

_CONTAS = set()


def conta(a, b):
    if (a, b) in _CONTAS:
        return
    _CONTAS.add((a, b))
    p(u"conta_%d_%d" % (a, b), u"%d dividido por %d." % (a, b))


# ---- 1 a 3, 12, 13 e 24 — repartir arrastando ------------------------------
REP = bloco(u"REP")
p(u"p1enun", u"Folha um. Arraste cada peça para um pote, até todos ficarem "
             u"iguais. No computador dá para arrastar; no celular, toque na peça "
             u"e depois no pote.")
p(u"p2enun", u"Folha dois. Mesmo gesto, e agora são três e quatro potes. Vá "
             u"pondo uma peça em cada um, dando a volta, até acabarem.")
p(u"p3enun", u"Folha três. Agora os potes são só caixas, sem figura. O gesto é o "
             u"mesmo: repartir até ficarem iguais.")
p(u"p12enun", u"Folha doze. Agora é outra pergunta. O tamanho do pote está dito: "
              u"encha um, depois outro, e veja quantos potes você precisou.")
p(u"p13enun", u"Folha treze. Mesma pergunta nova, com mais peças. Encha um pote "
              u"de cada vez, sem misturar.")
p(u"p24enun", u"Folha vinte e quatro. Uma parada para respirar: o gesto da "
              u"primeira folha, com contas novas. Arraste até os potes ficarem iguais.")
p(u"toque_peca", u"Primeiro toque numa peça ali embaixo. Depois toque no pote.")
_FOREP = {u"a": 1, u"b": 2, u"c": 3, u"m": 12, u"r": 24}
for _k, _R in REP.items():
    _fo = _FOREP[_k[0]]
    if _k in (u"m3", u"m4"):
        _fo = 13
    _cada = _R.get(u"medida") or (_R[u"n"] // _R[u"k"])
    if _R.get(u"medida"):
        p(u"rep%d_%s" % (_fo, _k),
          u"São %d %s e em cada %s cabem %d. Encha os %s."
          % (_R[u"n"], _R[u"q"], umSo(_R[u"w"]), _R[u"medida"], _R[u"w"]))
        p(u"certorep%d_%s" % (_fo, _k),
          u"Isso! Deu para encher %d %s. %d dividido por %d é %d."
          % (_R[u"k"], _R[u"w"], _R[u"n"], _R[u"medida"], _R[u"k"]))
    else:
        p(u"rep%d_%s" % (_fo, _k),
          u"%d %s para %d %s. Reparta em partes iguais."
          % (_R[u"n"], _R[u"q"], _R[u"k"], _R[u"w"]))
        p(u"certorep%d_%s" % (_fo, _k),
          u"Isso! Cada %s ficou com %d. %d dividido por %d é %d."
          % (umSo(_R[u"w"]), _cada, _R[u"n"], _R[u"k"], _cada))
    p(u"dicarep%d_%s" % (_fo, _k),
      u"Esse pote já está cheio. Ponha uma peça em cada pote e vá dando a "
      u"volta: assim eles acabam iguais sem você precisar contar antes.")

# ---- 4 e 5 — contar os grupos já feitos -----------------------------------
GRUP = bloco(u"GRUP")
p(u"p4enun", u"Folha quatro. As peças já estão repartidas. Conte quantas há em "
             u"cada grupo: é esse o resultado da conta.")
p(u"p5enun", u"Folha cinco. Mesmo gesto, e agora os montes são maiores. Conte um "
             u"grupo só: os outros têm o mesmo tanto.")
for _k, _G in GRUP.items():
    _fo = 4 if _k[0] == u"d" else 5
    conta(_G[u"a"], _G[u"b"])
    p(u"gr%d_%s" % (_fo, _k), u"%d dividido por %d." % (_G[u"a"], _G[u"b"]))
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! São %d em cada grupo." % (_G[u"a"] // _G[u"b"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"Conte as peças de UM grupo só, com o dedo. Os outros grupos têm o mesmo "
      u"tanto — é para isso que eles estão separados.")

# ---- 6 e 7 — da figura para o fato ----------------------------------------
FATO = bloco(u"FATO")
p(u"p6enun", u"Folha seis. Olhe o problema, termine a frase de cabeça e escreva "
             u"o resultado na conta. No computador dá para digitar.")
p(u"p7enun", u"Folha sete. Agora sem a frase de apoio: só o problema e a conta. "
             u"Escreva o resultado.")
p(u"escreva", u"Escreva o resultado usando o teclado.")
for _k, _F in FATO.items():
    _fo = 6 if _k[0] == u"f" else 7
    conta(_F[u"a"], _F[u"b"])
    p(u"ft%d_%s" % (_fo, _k),
      u"Reparta %d %s em %d %s." % (_F[u"a"], _F[u"q"], _F[u"b"], _F[u"w"]))
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! Em cada %s ficam %d %s. O fato é %d dividido por %d igual a %d."
      % (umSo(_F[u"w"]), _F[u"a"] // _F[u"b"], _F[u"q"], _F[u"a"], _F[u"b"],
         _F[u"a"] // _F[u"b"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"Pense: quantas vezes o número de baixo cabe no de cima? Se ajudar, "
      u"desenhe os grupos num papel.")

# ---- 8 a 11 e 14 a 15 — os problemas --------------------------------------
PROB = bloco(u"PROB")
p(u"p8enun", u"Folha oito. Leia ou ouça o problema e escolha quantos ficam para "
             u"cada um.")
p(u"p9enun", u"Folha nove. Mesmos problemas, agora com números maiores. Se "
             u"travar, pense na tabuada ao contrário.")
p(u"p10enun", u"Folha dez. Agora quatro problemas seguidos. Leia cada um até o "
              u"fim antes de escolher: o número grande nem sempre é o de repartir.")
p(u"p11enun", u"Folha onze. Os últimos da repartição. Todos perguntam a mesma "
              u"coisa: quantos para cada um?")
p(u"p14enun", u"Folha catorze. Agora só o problema escrito. Repare: ele não "
              u"pergunta quantos para cada um. Pergunta quantos grupos dão. A "
              u"conta é a mesma.")
p(u"p15enun", u"Folha quinze. Os últimos de medida. Leia com cuidado qual é a "
              u"pergunta: ela mudou, e a conta não.")
for _k, _P in PROB.items():
    conta(_P[u"a"], _P[u"b"])
    p(u"pb_" + _k, _P[u"t"])
    for _fo in (8, 9, 10, 11, 14, 15):
        p(u"certo%d_%s" % (_fo, _k),
          u"Isso! %d dividido por %d é %d."
          % (_P[u"a"], _P[u"b"], _P[u"a"] // _P[u"b"]))
        if _P[u"tipo"] == u"m":
            p(u"dica%d_%s" % (_fo, _k),
              u"Esta pergunta é das outras: ela quer saber QUANTOS GRUPOS dão, "
              u"não quantos para cada um. Vá tirando o tamanho do grupo do total "
              u"e conte quantas vezes deu.")
        else:
            p(u"dica%d_%s" % (_fo, _k),
              u"Leia de novo quem reparte e para quantos. Depois pense: que "
              u"número vezes esse dá o total?")

# ---- 16 e 17 — a conta de volta -------------------------------------------
INV = bloco(u"INV")
p(u"p16enun", u"Folha dezesseis. A conta de volta. Se a multiplicação está aí em "
              u"cima, a divisão já está respondida. Olhe bem.")
p(u"p17enun", u"Folha dezessete. Agora sem a multiplicação à vista. Pense: que "
              u"número vezes esse dá o total? Esse número é a resposta.")
for _k, _I in INV.items():
    _fo = 16 if _k[0] == u"n" else 17
    _pr = _I[u"x"] * _I[u"y"]
    conta(_pr, _I[u"y"])
    p(u"iv%d_%s" % (_fo, _k),
      u"%d vezes %d é %d, então %d dividido por %d."
      % (_I[u"x"], _I[u"y"], _pr, _pr, _I[u"y"]))
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! %d vezes %d é %d, então %d dividido por %d é %d."
      % (_I[u"x"], _I[u"y"], _pr, _pr, _I[u"y"], _I[u"x"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"Use a tabuada que você já sabe, de trás para a frente: que número vezes "
      u"esse dá o total?")

# ---- 18 e 19 — treino -----------------------------------------------------
CONTAB = bloco(u"CONTA")
p(u"p18enun", u"Folha dezoito. Treino de contas, e os cubinhos estão aí para "
              u"contar se você quiser. Contar é uma estratégia, não é trapaça.")
p(u"p19enun", u"Folha dezenove. Agora sem os cubinhos. Use a tabuada ao "
              u"contrário: que número vezes esse dá o total?")
for _k, _C in CONTAB.items():
    _fo = 18 if _k[0] == u"p" else 19
    conta(_C[u"a"], _C[u"b"])
    p(u"tr%d_%s" % (_fo, _k), u"%d dividido por %d." % (_C[u"a"], _C[u"b"]))
    p(u"certo%d_%s" % (_fo, _k), u"Isso! Deu %d." % (_C[u"a"] // _C[u"b"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"Pense na tabuada do número de baixo e vá subindo até chegar no de cima.")

# ---- 20 a 23 — o resto ----------------------------------------------------
RESTO = bloco(u"RESTO")
TRILHA = bloco(u"TRILHA")
p(u"p20enun", u"Folha vinte. Nem toda divisão fica certinha. Reparta o que dá e "
              u"veja o que sobra. Sobrar não é errar: é a resposta.")
p(u"p21enun", u"Folha vinte e um. Agora sem as figuras. Reparta de cabeça o "
              u"máximo que der e diga o que sobrou. Esse número tem nome: resto.")
p(u"p22enun", u"Folha vinte e dois. Cuidado: metade destas fecha certinho e "
              u"metade sobra. Marque só as que sobram alguma coisa e toque em "
              u"Conferir.")
p(u"certo22marca", u"Isso! Você achou todas as que sobram — e deixou de fora as "
                   u"que fecham certinho.")
p(u"dica22marca", u"Confira uma de cada vez: reparta em partes iguais e veja se "
                  u"ficou alguma coisa de fora. Só as que deixam alguma coisa de "
                  u"fora entram.")
p(u"p23enun", u"Folha vinte e três. Leve a chave até o cofre andando só pelas "
              u"casas em que a conta sobra resto. Em cada passo há três casas e "
              u"só uma sobra.")
for _k, _R in RESTO.items():
    _fo = {u"s": 20, u"t": 21, u"u": 22}[_k[0]]
    conta(_R[u"a"], _R[u"b"])
    p(u"rs%d_%s" % (_fo, _k),
      u"%d para %d: quanto sobra?" % (_R[u"a"], _R[u"b"]))
    _s = _R[u"a"] % _R[u"b"]
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! Cada um fica com %d e sobra%s."
      % (_R[u"a"] // _R[u"b"], u" zero, não sobra nada" if _s == 0 else u"m %d" % _s))
    p(u"dica%d_%s" % (_fo, _k),
      u"Reparta o máximo que der em partes iguais e conte só o que ficou de fora. "
      u"Se não ficar nada de fora, o resto é zero.")
for _k, _T in TRILHA.items():
    for _o in _T[u"ops"]:
        conta(_o[u"a"], _o[u"b"])
    p(u"certo23_" + _k, u"Boa! Essa sobra resto — a chave avançou um passo.")
    p(u"dica23_" + _k,
      u"Essa fecha certinho, sem sobrar nada. Procure a casa em que ainda fica "
      u"alguma coisa de fora depois de repartir.")

# ---- 25 a 27 — pintar e decifrar ------------------------------------------
PINT = bloco(u"PINT")
SEGREDO = bloco(u"SEGREDO")
p(u"p25enun", u"Folha vinte e cinco. Cada cor é um resultado. Pegue a canetinha "
              u"e pinte as contas que dão aquele número.")
p(u"p26enun", u"Folha vinte e seis. Agora com contas maiores, e as mesmas quatro "
              u"cores. Se a conta não der nenhum desses números, confira outra vez.")
p(u"p27enun", u"Folha vinte e sete. Resolva cada conta e a letra aparece. No "
              u"fim, a frase se monta sozinha.")
p(u"pegue_lapis", u"Antes de pintar, pegue uma canetinha ali em cima.")
for _n in (2, 3, 4, 5):
    p(u"lapis_c%d" % _n, u"Canetinha do resultado que deu %s." % nu(_n))
for _k, _P in PINT.items():
    _fo = 25 if _k[0] == u"w" else 26
    conta(_P[u"a"], _P[u"b"])
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! %d dividido por %d é %d."
      % (_P[u"a"], _P[u"b"], _P[u"a"] // _P[u"b"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"Essa canetinha não é a dessa conta. Faça a conta primeiro e depois "
      u"procure a cor do resultado.")
for _i, _C in enumerate(SEGREDO[u"contas"]):
    conta(_C[u"a"], _C[u"b"])
    _key = u"S%d" % (_i + 1)
    p(u"certo27_" + _key,
      u"Isso! Deu %d, e a letra apareceu." % (_C[u"a"] // _C[u"b"]))
    p(u"dica27_" + _key,
      u"Refaça a conta com calma: cada resultado abre uma letra da frase.")

# ---- 28 a 30 — metade, terça e quarta parte -------------------------------
PARTE = bloco(u"PARTE")
p(u"p28enun", u"Folha vinte e oito. Metade é dividir por dois. É a mesma conta, "
              u"com outro nome — e este nome você vai ouvir a vida toda.")
p(u"p29enun", u"Folha vinte e nove. Terça parte é dividir por três; quarta "
              u"parte, por quatro. Repare no nome: ele já diz por quanto dividir.")
p(u"p30enun", u"Folha trinta. Quinta parte é por cinco e décima parte é por dez. "
              u"Agora você sabe as cinco. E aqui a resposta é escrita, sem lista.")
for _k, _P in PARTE.items():
    conta(_P[u"a"], _P[u"b"])
    p(u"pt_" + _k, u"Qual é a %s de %d?" % (_P[u"nome"].lower(), _P[u"a"]))
    _fo = {u"z": 28, u"A": 29, u"B": 30}[_k[0]]
    p(u"certo%d_%s" % (_fo, _k),
      u"Isso! A %s de %d é %d, porque %d dividido por %d é %d."
      % (_P[u"nome"].lower(), _P[u"a"], _P[u"a"] // _P[u"b"], _P[u"a"],
         _P[u"b"], _P[u"a"] // _P[u"b"]))
    p(u"dica%d_%s" % (_fo, _k),
      u"O nome já diz por quanto dividir: metade é por dois, terça parte é por "
      u"três, quarta parte é por quatro, quinta por cinco e décima por dez.")

# ---- 31 a 34 — brincar e inventar -----------------------------------------
PUZ = bloco(u"PUZ")
CRZ = bloco(u"CRZ")
MEM = bloco(u"MEM")
ELAB = bloco(u"ELAB")
p(u"p31enun", u"Folha trinta e um. Cada peça só encaixa no lugar do seu "
              u"resultado. Arraste a conta até o número certo, ou toque nos dois.")
p(u"p32enun", u"Folha trinta e dois. Resolva a conta da pista e escreva o "
              u"resultado por extenso na cruzadinha. No computador dá para digitar.")
p(u"p33enun", u"Folha trinta e três. Vire duas cartas e ache a conta e o "
              u"resultado dela.")
p(u"p34enun", u"Folha trinta e quatro. Agora é você quem faz o problema. Escolha "
              u"quantas peças e quantos grupos, e depois responda o seu próprio "
              u"problema.")
for _k, _P in PUZ.items():
    conta(_P[u"a"], _P[u"b"])
    p(u"certo31_" + _k, u"Encaixou! %d dividido por %d é %d."
                        % (_P[u"a"], _P[u"b"], _P[u"a"] // _P[u"b"]))
    p(u"dica31_" + _k, u"Faça a conta primeiro e só então procure a casa do "
                       u"resultado.")
for _k, _C in CRZ.items():
    p(u"crz_" + _k, _C[u"d"])
    p(u"certo32_" + _k, u"Isso!")
    p(u"dica32_" + _k, u"Faça a conta da pista e escreva o número por extenso, "
                       u"com letras.")
for _k, _M in MEM.items():
    conta(_M[u"a"], _M[u"b"])
    p(u"memok_" + _k, u"Par! %d dividido por %d é %d."
                      % (_M[u"a"], _M[u"b"], _M[u"a"] // _M[u"b"]))
p(u"memfim", u"Tabuleiro limpo! Você lembrou de todas.")
p(u"memdica", u"Guarde onde cada carta estava: elas voltam para baixo no mesmo lugar.")
for _k, _E in ELAB.items():
    conta(_E[u"a"], _E[u"b"])
    p(u"el_" + _k, u"O seu problema: %d %s para %d %s. Quantos para cada um?"
                   % (_E[u"a"], _E[u"q"], _E[u"b"], _E[u"w"]))
    p(u"certo34_" + _k, u"Isso! O seu problema tem resposta %d."
                        % (_E[u"a"] // _E[u"b"]))
    p(u"dica34_" + _k, u"Você mesmo escolheu os números: reparta %d em %d grupos "
                       u"iguais." % (_E[u"a"], _E[u"b"]))

# ---- 35 — o cartaz --------------------------------------------------------
CARTAZ = bloco(u"CARTAZ")
p(u"p35enun", u"Folha trinta e cinco. Este cartaz é seu. Em cada linha, escolha "
              u"o exemplo que cabe naquele nome, e leve os quatro na cabeça.")
for _k, _C in CARTAZ.items():
    p(u"cartaz_" + _k, u"%s. %s" % (_C[u"n"].capitalize(), _C[u"d"]))
    p(u"ex_" + _k, _C[u"ex"] + u".")
    p(u"certo35_" + _k, u"Isso! %s" % _C[u"d"])
    p(u"dica35_" + _k, u"Leia a linha outra vez: ela conta a história, e o "
                       u"exemplo é a conta dessa história.")

_ORFAS = _mapeia([])


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
