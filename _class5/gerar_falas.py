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
PREFIXO = u"cl5_"                     # <- o prefixo desta atividade
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
p(u"capa", u"Classes de palavras. Trinta e cinco folhas sobre substantivo, adjetivo, verbo, aumentativo, diminutivo, singular e plural. Escreva o seu nome ali embaixo e toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora você sabe o lugar de cada palavra. E fica a pergunta: você lembra qual era a palavra que mudava de classe conforme a frase?")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por folha, lendo os DADOS
#
#   FOO = bloco(u"FOO")
#   p(u"p1enun", u"Folha um: o que ela pede.")
#   for k, X in FOO.items():
#       p(u"diz_" + k, X[u"p"] + u".")
#       p(u"certo1_" + k, u"Isso! …")
#       p(u"dica1_" + k, u"… uma pista, NUNCA a resposta.")
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
#  AS FALAS DAS FOLHAS — uma seção por folha, lendo os DADOS.
#  ⚠️ A DICA NUNCA ENTREGA A RESPOSTA: ela diz ONDE OLHAR. Regra da casa.
# ---------------------------------------------------------------------------
# ⚠️ o `bloco()` procura `var <nome>`; as listas deste caderno moram DENTRO
#    de `var D`, entao o bloco que se le e o D e as listas saem dele.
DADOS = bloco(u"D")
FIG = DADOS[u"FIG"]
GAVB = bloco(u"GAV")

ENUN = {
 1: u"Folha um. Estas coisas existem. Escreva o nome de cada uma.",
 2: u"Folha dois. Todo substantivo dá nome a alguma coisa. Ponha cada um na gaveta: gente, coisa ou lugar.",
 3: u"Folha três. Agora olhe a letra do começo. Qual das duas é nome próprio?",
 4: u"Folha quatro. De uma palavra nasce outra. Monte a palavra derivada com as sílabas.",
 5: u"Folha cinco. Agora duas palavras viram uma. Qual é a palavra composta certa?",
 6: u"Folha seis. Os substantivos estão escondidos na frase. Toque em cada um deles.",
 7: u"Folha sete. Ache todos os substantivos, e só eles.",
 8: u"Folha oito. Agora não é o nome: é como a coisa é. Escreva uma característica.",
 9: u"Folha nove. Qual adjetivo combina com a coisa?",
 10: u"Folha dez. Agora as duas classes juntas na mesma frase.",
 11: u"Folha onze. Agora a mesma palavra. O que ela é nesta frase?",
 12: u"Folha doze. Às vezes o adjetivo vem em duas palavras. Ligue cada uma ao adjetivo que vale o mesmo.",
 13: u"Folha treze. O adjetivo tem graus. Em que grau está o adjetivo desta frase?",
 14: u"Folha catorze. Escreva o adjetivo que a dica pede.",
 15: u"Folha quinze. O verbo diz o que se faz. Preencha a frase com o verbo.",
 16: u"Folha dezesseis. Nem todo verbo é ação. Ponha cada um na gaveta certa.",
 17: u"Folha dezessete. Agora ache os verbos escondidos na frase.",
 18: u"Folha dezoito. A mesma ação em três tempos. Qual forma cabe em cada um?",
 19: u"Folha dezenove. Agora passe a frase para ontem.",
 20: u"Folha vinte. Agora para amanhã.",
 21: u"Folha vinte e um. Quem faz a ação manda no verbo. Preencha.",
 22: u"Folha vinte e dois. Toda palavra pode ficar pequena ou grande. Qual destas é o aumentativo?",
 23: u"Folha vinte e três. Escreva a palavra no diminutivo.",
 24: u"Folha vinte e quatro. Agora no aumentativo.",
 25: u"Folha vinte e cinco. Ache todas as palavras que estão no diminutivo.",
 26: u"Folha vinte e seis. São as terminações que fazem o grau. Ponha cada uma na gaveta.",
 27: u"Folha vinte e sete. Cuidado: nem tudo que acaba em inho é diminutivo!",
 28: u"Folha vinte e oito. Escreva a palavra que a dica descreve.",
 29: u"Folha vinte e nove. Uma coisa vira muitas. Escreva no plural.",
 30: u"Folha trinta. Agora as palavras terminadas em ão. E elas não fazem todas igual.",
 31: u"Folha trinta e um. Agora as terminadas em L.",
 32: u"Folha trinta e dois. Cada palavra faz o plural de um jeito. Ponha cada uma no seu.",
 33: u"Folha trinta e três. No plural, a frase inteira muda, não só o substantivo.",
 34: u"Folha trinta e quatro. Última gaveta: esta palavra está no singular ou no plural?",
 35: u"Folha trinta e cinco. Uma frase, três classes. Toque em cada palavra e diga o que ela é.",
}
for _n, _txt in ENUN.items():
    p(u"p%denun" % _n, _txt)

CERTO = {
 1: (u"Isso! É o nome dela.", u"Olhe o desenho e diga o nome em voz alta."),
 2: (u"Isso! Está na gaveta certa.", u"Pergunte: isto é gente, é coisa ou é lugar?"),
 3: (u"Isso! Nome próprio começa com letra maiúscula.", u"Qual das duas começa com letra grande?"),
 4: (u"Isso! Uma palavra nasceu da outra.", u"Comece pelo pedaço que é igual ao da primeira palavra."),
 5: (u"Isso! Duas palavras, uma só.", u"Junte na ordem em que você ouve a palavra."),
 6: (u"Isso! Este dá nome a alguma coisa.", u"Substantivo dá NOME. Procure quem tem nome na frase."),
 7: (u"Isso! Este é substantivo.", u"Se dá para pôr o ou a na frente, é substantivo."),
 8: (u"Isso! Você disse como ela é.", u"Não é o nome: é como ela é."),
 9: (u"Isso! Combina mesmo.", u"Pense na coisa e em como ela é de verdade."),
 10: (u"Isso!", u"Substantivo dá o nome; adjetivo diz como é."),
 11: (u"Isso! Quem decide é a frase.", u"Veja se a palavra está dando o NOME ou dizendo COMO É."),
 12: (u"Isso! As duas dizem a mesma coisa.", u"Pense em que palavra cabe no lugar das duas."),
 13: (u"Isso!", u"Compara duas coisas ou diz que é o máximo?"),
 14: (u"Isso!", u"Pense no contrário do que a dica diz."),
 15: (u"Isso! Este é o verbo.", u"O que a pessoa está fazendo?"),
 16: (u"Isso! Está na gaveta certa.", u"É alguém fazendo, é um jeito de ser, ou é o tempo lá fora?"),
 17: (u"Isso! Este é verbo.", u"Verbo é o que se faz ou o que acontece."),
 18: (u"Isso! Este é o tempo certo.", u"Já aconteceu, acontece agora, ou vai acontecer?"),
 19: (u"Isso! Está no passado.", u"Ontem já passou: o verbo tem de mudar."),
 20: (u"Isso! Está no futuro.", u"Amanhã ainda não chegou: o verbo tem de mudar."),
 21: (u"Isso! O verbo foi junto com quem faz.", u"Quantos são? O verbo acompanha."),
 22: (u"Isso! Este é o maior.", u"Qual dos dois deixa a palavra GRANDE?"),
 23: (u"Isso! Ficou pequenininha.", u"Ponha inho ou zinho no fim da palavra."),
 24: (u"Isso! Ficou enorme.", u"Ponha ão, arra ou aça no fim da palavra."),
 25: (u"Isso! Está no diminutivo.", u"Procure as que deixam a coisa pequena."),
 26: (u"Isso! Esta terminação faz isso mesmo.", u"Esta terminação deixa a palavra maior ou menor?"),
 27: (u"Isso!", u"Pergunte: é um moinho pequeno, ou é outra coisa?"),
 28: (u"Isso!", u"Leia a dica de novo, devagar."),
 29: (u"Isso! Agora são muitos.", u"Muitas vezes basta o s no fim."),
 30: (u"Isso! Este ão faz assim.", u"Diga em voz alta: soa melhor de que jeito?"),
 31: (u"Isso! O L sai e entram is.", u"O L do fim não fica: pense em animais."),
 32: (u"Isso! Este é o plural dela.", u"Diga a palavra no plural em voz alta primeiro."),
 33: (u"Isso! A frase inteira foi junto.", u"O artigo e o adjetivo também mudam."),
 34: (u"Isso!", u"É uma coisa só ou são várias?"),
 35: (u"Isso! Você achou as três classes.", u"Uma dá o nome, outra diz como é, outra diz o que faz."),
}
for _n, (_c, _d) in CERTO.items():
    p(u"certo%d_0" % _n, _c)
    p(u"dica%d_0" % _n, _d)

# as chaves por ITEM, que o motor pede uma a uma
ITENSB = bloco(u"ITENS")
for _n in range(1, 36):
    _lista = ITENSB.get(u"p%d" % _n) or []
    if _lista and isinstance(_lista[0], list):
        _lista = _lista[0]
    for _k in _lista:
        p(u"certo%d_%s" % (_n, _k), CERTO[_n][0])
        p(u"dica%d_%s" % (_n, _k), CERTO[_n][1])

# as vozes das gavetas (a gaveta diz a REGRA dela, nunca a resposta)
REGRA = {
 u"gente": u"Gaveta gente: nomes de pessoas.",
 u"coisa": u"Gaveta coisa: nomes de objetos.",
 u"lugar": u"Gaveta lugar: nomes de lugares.",
 u"acao": u"Gaveta ação: o que alguém faz.",
 u"estado": u"Gaveta estado: um jeito de ser ou de estar.",
 u"natureza": u"Gaveta natureza: o que acontece no tempo lá fora.",
 u"dim": u"Gaveta diminutivo: deixa a palavra pequena.",
 u"aum": u"Gaveta aumentativo: deixa a palavra grande.",
 u"oes": u"Gaveta ões.", u"aes": u"Gaveta ães.", u"aos": u"Gaveta ãos.",
 u"sing": u"Gaveta singular: uma coisa só.",
 u"plur": u"Gaveta plural: várias coisas.",
}
for _gk, _G in GAVB.items():
    for _C in _G[u"cols"]:
        p(u"gav_%s_%s" % (_gk, _C[u"k"]), REGRA.get(_C[u"k"], _C[u"n"] + u"."))
    for _k, _P in _G[u"pal"].items():
        p(u"diz2_%s_%s" % (_gk, _k), _P[u"p"] + u".")

# a voz de cada figura e de cada resposta escrita
for _k, _X in FIG.items():
    p(u"diz_" + _k, _X[u"t"] + u".")
    p(u"diz2_" + _k, _X[u"adj"] + u".")

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
