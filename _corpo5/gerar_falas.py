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
PREFIXO = u"vd_"                     # <- o prefixo desta atividade
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
        raise SystemExit(u"não achei o bloco `var %s` no index.html" % nome)
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
p(u"capa", u"A Viagem Dentro de Você. Trinta e seis folhas sobre o caminho que o alimento, "
           u"o ar e o sangue fazem dentro do seu corpo. Escreva o seu nome ali embaixo e "
           u"toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim da viagem! Agora você sabe o caminho do alimento, do ar e "
          u"do sangue. E fica uma pergunta para você pensar: enquanto você lia esta "
          u"frase, o seu coração bateu umas dez vezes e você respirou umas duas. "
          u"Quantas vezes será que ele bate enquanto você dorme a noite inteira?")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — lidas dos DADOS, uma fonte só
# ---------------------------------------------------------------------------

ORG = bloco(u"ORG")
PERG = bloco(u"PERG")
LIGPARES = bloco(u"LIGPARES")
GAV = bloco(u"GAV")
ORDEM = bloco(u"ORDEM")
ESCR = bloco(u"ESCR")
CACA1 = bloco(u"CACA1")
CACA2 = bloco(u"CACA2")
CRZ1 = bloco(u"CRZ1")
CRZ2 = bloco(u"CRZ2")
ITENS = bloco(u"ITENS")

NOMES = [
 u"Onde tudo começa", u"Os órgãos da digestão", u"Os órgãos da digestão, de novo",
 u"O caminho do alimento", u"O que cada órgão faz", u"O que cada órgão faz, de novo",
 u"Preencha o caminho", u"Caça-órgãos da digestão",
 u"Para que serve respirar", u"Os órgãos da respiração", u"O caminho do ar",
 u"O caminho do ar, de novo", u"O que cada órgão do ar faz", u"Nariz ou boca?",
 u"Puxo o ar, solto o ar", u"Cruza-respiração",
 u"A bomba do corpo", u"O que o sangue leva", u"Coração, veia e artéria",
 u"Os vasos e o que fazem", u"Preencha: o sangue", u"O caminho do sangue",
 u"É verdade ou é falso?", u"Caça-palavras da circulação",
 u"Respirar enquanto come", u"Do prato até a célula", u"Preencha: a viagem do nutriente",
 u"Onde o nutriente entra", u"Por onde sai o que não serve", u"Os rins e a água",
 u"De que sistema é cada um?",
 u"Pedro correu no recreio", u"O que acontece quando corro", u"O alimento é o combustível",
 u"Ache o órgão na grade", u"Cruzadinha dos três sistemas"]

# ---- o enunciado de cada folha ----
PEDE = {
 1: u"Leia a pergunta e toque na resposta certa.",
 2: u"Puxe o nome certo para cada órgão, ou toque no órgão e depois no nome.",
 3: u"De novo os órgãos da digestão. Agora sem a ajuda da primeira vez.",
 4: u"Ponha o caminho do alimento em ordem: para cada órgão, toque no número do lugar dele.",
 5: u"Toque no órgão de um lado e no que ele faz do outro.",
 6: u"Ligue de novo. Agora entram o fígado e o pâncreas, que ajudam a digestão.",
 7: u"Preencha a palavra que falta. Dá para usar o teclado da tela ou o de verdade.",
 8: u"Ache na grade o nome de cada órgão da digestão.",
 9: u"Leia a pergunta sobre a respiração e toque na resposta certa.",
 10: u"Leia o que cada parte da respiração faz e puxe o nome certo.",
 11: u"Ponha em ordem o caminho do ar, de onde ele entra até onde ele chega.",
 12: u"O caminho do ar de novo, agora até os alvéolos, lá no fundo do pulmão.",
 13: u"Ligue cada órgão do ar ao que ele faz.",
 14: u"Preencha as frases sobre o ar que entra no corpo.",
 15: u"Cada frase é de quando o ar ENTRA ou de quando o ar SAI? Leve para a gaveta certa.",
 16: u"Leia a pista e preencha a palavra na cruzadinha da respiração.",
 17: u"Leia a pergunta sobre o coração e o sangue e toque na resposta certa.",
 18: u"Preencha as frases sobre o que o sangue faz.",
 19: u"Leia o que cada parte do sistema circulatório faz e puxe o nome certo.",
 20: u"Ligue cada vaso ao que ele faz.",
 21: u"Preencha as frases sobre a energia e o que o sangue carrega.",
 22: u"Ponha em ordem o caminho do sangue, saindo do coração e voltando para ele.",
 23: u"Leia cada frase e leve para a gaveta: é verdade ou é falso?",
 24: u"Ache na grade as palavras da circulação.",
 25: u"Agora os três sistemas juntos. Leia e toque na resposta certa.",
 26: u"Ponha em ordem a viagem do nutriente, do prato até a célula.",
 27: u"Preencha as frases sobre a viagem do nutriente.",
 28: u"Onde cada coisa entra no sangue? Toque na resposta certa.",
 29: u"E o que o corpo não quer mais, por onde sai? Toque na resposta certa.",
 30: u"Pense no que acontece quando falta água no corpo.",
 31: u"De que sistema é cada órgão? Leve cada um para a gaveta dele.",
 32: u"Pedro correu no recreio. Leia e toque na resposta certa.",
 33: u"Ligue o que acontece no corpo de quem corre ao motivo disso.",
 34: u"De onde vem a energia do corpo? Toque na resposta certa.",
 35: u"Olhe a grade de quadrinhos e diga onde está cada órgão.",
 36: u"A cruzadinha do fim: pistas dos três sistemas juntos."}
for i in range(1, 37):
    p(u"p%denun" % i, u"Folha %d: %s. %s" % (i, NOMES[i - 1], PEDE[i]))

# ---- os órgãos: o nome e o que ele faz ----
# ⚠️ A FAMÍLIA É `org_`, NÃO `nome_`: o `_anim` já usa `nome_` para os mp3 dos
#    nomes das crianças (nome_agatha, nome_alexandre...), e o portão 1c acusou
#    com razão — duas atividades brigando pela mesma família de arquivo.
for k, O in ORG.items():
    p(u"org_" + k, O[u"n"] + u".")
    p(u"faz_" + k, O[u"n"] + u": " + O[u"faz"] + u".")
    p(u"certo_org_" + k, u"Isso! " + O[u"n"] + u": " + O[u"faz"] + u".")
    p(u"dica_org_" + k, u"Leia de novo a pista embaixo da figura. Ela diz o que esse órgão FAZ.")

# ---- as perguntas de escolher ----
for k, Q in PERG.items():
    p(u"perg_" + k, Q[u"p"])
    certa = u""
    for o in Q[u"o"]:
        p(u"op_%s_%s" % (k, o[0]), o[1])
        if o[0] == Q[u"c"]:
            certa = o[1]
    p(u"certo_" + k, u"Isso mesmo! " + certa)
    p(u"dica_" + k, u"Ainda não. Leia a pergunta de novo com calma e pense no que aquele órgão FAZ.")

# ---- numerar o caminho ----
for n in range(1, 8):
    p(u"num_" + str(n), u"Número %d." % n)
for kO, O in ORDEM.items():
    for k in O[u"v"]:
        # ⚠️ AQUI NAO HA SAIDA DE EMERGENCIA, de proposito: todo item de um
        #    caminho TEM de estar no ORG (e a mesma regra do `fNumerar`, que
        #    deixou vazar a chave `cora2` para a voz quando tinha fallback).
        #    Se faltar, este gerador quebra alto — que e o que se quer.
        nm = ORG[k][u"n"]
        art = ORG[k][u"art"].upper()
        p(u"certo_ord_" + k, u"Isso! " + art + u" " + nm + u" está no lugar certo.")
        p(u"dica_ord_" + k, u"Pense: o que vem ANTES dele nesse caminho? Comece pelo começo.")

# ---- ligar: a fala do acerto e do erro, por folha ----
LIGDE = {5: u"g1", 6: u"g2", 13: u"g3", 20: u"g4", 33: u"g5"}
for pi, gk in LIGDE.items():
    for par in LIGPARES[gk]:
        k, oque = par[0], par[1]
        # o 3o campo do par e o ROTULO (ver o comentario do `fLigar` no
        # folhas.js): chave e identificador, rotulo e o que a crianca le e a
        # voz diz. Sem ele saia "MUSCULO", sem acento, na tela e na voz.
        nm = ORG[k][u"n"] if k in ORG else (par[2] if len(par) > 2 else k.upper())
        p(u"certo%d_%s" % (pi, k), u"Isso! " + nm + u": " + oque + u".")
        p(u"dica%d_%s" % (pi, k), u"Ainda não. Leia de novo o que está escrito do outro lado.")
        if k not in ORG:
            p(u"org_" + k, nm + u".")
            p(u"faz_" + k, oque + u".")

# ---- escrever no teclado ----
for k, E in ESCR.items():
    p(u"fras_" + k, E[u"fr"].replace(u"…", u"que palavra?"))
    # ⚠️ A VOZ LE A FORMA ACENTUADA, a tela mostra a crua. O `w` e a palavra
    #    da GRADE DE DIGITAR, que nao carrega acento nem cedilha ("ESOFAGO",
    #    "CORACAO"). Se a confirmacao falada usasse esse `w`, a voz diria
    #    "co-ra-ca-o" — o defeito que o portao 0j2 (`acento.py`) nomeia. O campo
    #    `ac` ja traz as formas aceitas; a ACENTUADA e a que se fala.
    falada = E[u"w"]
    for forma in E.get(u"ac", []):
        if any(c in forma for c in u"ÁÀÂÃÉÊÍÓÔÕÚÜÇáàâãéêíóôõúüç"):
            falada = forma
            break
    p(u"certo_" + k, u"Isso! " + E[u"fr"].replace(u"…", falada))
    p(u"dica_" + k, u"Escute a frase inteira de novo e pense em que palavra cabe ali.")

# ---- gavetas ----
GNOME = {u"ar": u"o ar entrando e saindo", u"vf": u"verdade e mentira", u"sis": u"os três sistemas"}
for gk, G in GAV.items():
    for C in G[u"cols"]:
        p(u"gav_%s_%s" % (gk, C[u"k"]), C[u"n"] + u".")
    for n, X in G[u"pal"].items():
        p(u"diz2_%s_%s" % (gk, n), X[u"p"] + u".")
        col = [c for c in G[u"cols"] if c[u"k"] == X[u"c"]][0]
        pag = {u"ar": 15, u"vf": 23, u"sis": 31}[gk]
        p(u"certo%d_%s" % (pag, n), u"Isso! " + X[u"p"] + u": " + col[u"n"].lower() + u".")
        p(u"dica%d_%s" % (pag, n), u"Leia a frase de novo e pense em qual gaveta ela cabe.")

# ---- caça-palavras ----
p(u"cacatoque", u"Toque na primeira letra da palavra e depois na última.")
for pag, C in ((8, CACA1), (24, CACA2)):
    for k, X in C[u"pal"].items():
        p(u"cp_" + k, X[u"pista"])
        p(u"certo%d_%s" % (pag, k), u"Achou! " + X[u"pista"] + u".")
        p(u"dica%d_%s" % (pag, k), u"Olhe linha por linha. As palavras estão deitadas, da esquerda para a direita.")

# ---- cruzadinha ----
for pag, C in ((16, CRZ1), (36, CRZ2)):
    for k, X in C.items():
        p(u"crz_" + k, X[u"d"])
        p(u"certo%d_%s" % (pag, k), u"Isso! " + X[u"d"])
        p(u"dica%d_%s" % (pag, k), u"Leia a pista de novo. Conte quantas casinhas tem a palavra.")


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
