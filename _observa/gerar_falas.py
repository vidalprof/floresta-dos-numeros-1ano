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
PREFIXO = u"ob_"                     # <- o prefixo desta atividade
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
p(u"capa", u"Aprendendo a observar. Catorze folhas para olhar com atenção: achar as iguais, achar a sombra, achar o diferente, descobrir o que vem depois, pintar e jogar a memória. Escreva o seu nome ali embaixo e toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa figura do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora olhe em volta da sala: dá para achar duas coisas iguais? E alguma coisa que não é da família das outras?")

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
# AS FALAS DAS FOLHAS — o Pre NAO LE: tudo o que a folha pede e DITO.
# ⚠️ A dica nunca diz a resposta; ela manda olhar uma pista.
# ---------------------------------------------------------------------------
FIG  = bloco(u"FIG")
DIF1 = bloco(u"DIF1"); DIF2 = bloco(u"DIF2")
SEQ1 = bloco(u"SEQ1"); SEQ2 = bloco(u"SEQ2")
COR1 = bloco(u"COR1"); COR2 = bloco(u"COR2")
BAL1 = bloco(u"BAL1"); BAL2 = bloco(u"BAL2")
ITENS = bloco(u"ITENS")

# o artigo de cada figura: a fala do Pre e FRASE INTEIRA, nao palavra solta
_ART = {u"bic": u"a", u"bic2": u"a", u"mot": u"a", u"ska": u"o", u"pat": u"o",
        u"lim": u"o", u"bet": u"a", u"amo": u"a", u"mel": u"a", u"tom": u"o",
        u"lar": u"a"}


def _nome(k):
    return _ART.get(k, u"o") + u" " + FIG[k][u"n"]


# o nome de cada figura — a crianca toca e OUVE o que e
for _k, _F in FIG.items():
    # clipe de meio segundo e o pior caso para qualquer reconhecedor, e frase
    # inteira e melhor fala para quem tem cinco anos
    p(u"fig_" + _k, u"Esta figura é " + _nome(_k) + u".")
    p(u"memok_" + _k, u"Achou o par! São duas vezes " + _nome(_k) + u".")

ENUN = {
 1:  u"Folha um. Toque numa figura e depois na figura igual a ela.",
 2:  u"Folha dois. Agora sao seis. Ligue cada figura a sua igual.",
 3:  u"Folha tres. A sombra e a figura sem a cor. Ligue cada uma a sua sombra.",
 4:  u"Folha quatro. Agora as sombras sao mais parecidas. Olhe bem o formato.",
 5:  u"Folha cinco. Tres sao iguais e um e diferente. Toque no diferente.",
 6:  u"Folha seis. Agora pense: tres sao da mesma familia e um nao e. Qual?",
 7:  u"Folha sete. Olhe a fila e veja o que se repete. O que vem depois?",
 8:  u"Folha oito. Agora a fila repete de tres em tres. O que vem depois?",
 9:  u"Folha nove. Pegue a canetinha da cor certa e toque no balao com aquele numero.",
 10: u"Folha dez. Agora sao cinco cores. Olhe a legenda antes de pintar.",
 11: u"Folha onze. Vire duas cartas e ache as duas iguais. Sao cinco pares.",
 12: u"Folha doze. Agora o par e a figura e a sombra dela. Sao quatro pares.",
 13: u"Folha treze. Toque no numero um, depois no dois, e va ate o dez. Veja o que aparece!",
 14: u"Folha catorze. Voce aprendeu a olhar com atencao. Toque em cada figura para ouvir o nome dela.",
}
for _i, _t in ENUN.items():
    p(u"p%denun" % _i, _t)

# 1 a 4 — ligar (iguais e sombra)
_DICAS_LIG = {
 1: u"Olhe o desenho com calma e procure ele do outro lado.",
 2: u"Va uma de cada vez. Qual delas ainda nao tem par?",
 3: u"A sombra tem o mesmo formato, so que toda escura.",
 4: u"Olhe o contorno: onde ele e redondo e onde ele e comprido?",
}
for _pi in (1, 2, 3, 4):
    for _k in ITENS[u"p%d" % _pi][0]:
        p(u"certo%d_%s" % (_pi, _k), u"Isso! É " + _nome(_k) + u".")
        p(u"dica%d_%s" % (_pi, _k), _DICAS_LIG[_pi])

# 5 e 6 — o diferente
for _pi, _D, _dica in ((5, DIF1, u"Tres deles sao o mesmo desenho. Ache o que nao e."),
                       (6, DIF2, u"Pense no que eles sao: o que se come e o que anda na rua.")):
    for _k, _X in _D.items():
        _certo = _X[u"pecas"][_X[u"r"]]
        p(u"certo%d_%s" % (_pi, _k),
          u"Isso! O diferente era " + _nome(_certo) + u".")
        p(u"dica%d_%s" % (_pi, _k), _dica)

# 7 e 8 — o que vem depois
for _pi, _S, _dica in ((7, SEQ1, u"Diga a fila em voz alta, do comeco. O que vem sempre depois?"),
                       (8, SEQ2, u"Conte de tres em tres: um, dois, tres, e comeca de novo.")):
    for _k, _X in _S.items():
        p(u"certo%d_%s" % (_pi, _k),
          u"Isso! Depois vem " + _nome(_X[u"r"]) + u".")
        p(u"dica%d_%s" % (_pi, _k), _dica)

# 9 e 10 — pintar pela legenda
for _k, _C in COR2.items():
    p(u"lapis_" + _k, _C[u"n"][0].upper() + _C[u"n"][1:] + u".")
p(u"pegue_lapis", u"Primeiro pegue uma canetinha ali em cima. Depois toque no balao.")
_NUM = {1: u"um", 2: u"dois", 3: u"tres", 4: u"quatro", 5: u"cinco", 6: u"seis"}
for _pi, _B, _C in ((9, BAL1, COR1), (10, BAL2, COR2)):
    _cor = dict((k2, v2[u"n"]) for k2, v2 in _C.items())
    for _k, _X in _B.items():
        p(u"certo%d_%s" % (_pi, _k),
          u"Isso! O numero " + _NUM[_X[u"num"]] + u" e " + _cor[_X[u"cor"]] + u".")
        p(u"dica%d_%s" % (_pi, _k),
          u"Olhe a legenda: procure o numero deste balao e veja a cor do lado.")

# 13 — ligar os pontos de 1 a 10
_DEZ = [u"um", u"dois", u"tres", u"quatro", u"cinco",
        u"seis", u"sete", u"oito", u"nove", u"dez"]
for _i, _n in enumerate(_DEZ, 1):
    p(u"num_%d" % _i, _n[0].upper() + _n[1:] + u".")
p(u"certo13_q1", u"Voce conseguiu! Os dez pontos na ordem certa formaram uma estrela.")
p(u"dica13_q1", u"Este nao e o proximo. Procure o numero que vem logo depois do ultimo que voce tocou.")

# 11 — a memoria
p(u"memdica", u"Nao era o par. Guarde onde estavam e tente outra vez.")
p(u"memfim", u"Voce achou os quatro pares! Que memoria boa.")

# 12 — o cartaz
p(u"certo14_z1", u"Parabens! Voce olhou com muita atencao o caderno inteiro.")
p(u"dica14_z1", u"Toque nas figuras e depois em Terminei.")


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
