# -*- coding: utf-8 -*-
u"""
============================================================
 Aprendendo a divisão e as horas (4º ano) — gerador das falas

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
PREFIXO = u"dh4_"                     # <- o prefixo desta atividade
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

# ============================================================
#  AS FALAS DESTE CADERNO — Aprendendo a divisão e as horas (4º ano)
#
#  ⚠️ OS NÚMEROS VÃO EM ALGARISMO e a voz os lê por extenso; o portão do
#     ouvido (`_qa/ouvir.py`) normaliza os dois lados antes de comparar. O que
#     NÃO pode ir para a voz é o SINAL: "÷" e "×" a voz engole calada, e "7h15"
#     ela soletra. Tudo passa por `voz()` antes de gravar.
# ============================================================

EXTF = [u"zero", u"um", u"dois", u"três", u"quatro", u"cinco", u"seis", u"sete",
        u"oito", u"nove", u"dez", u"onze", u"doze", u"treze", u"catorze", u"quinze",
        u"dezesseis", u"dezessete", u"dezoito", u"dezenove", u"vinte"]


def folha(n):
    u"""'Folha vinte e três.' — o número da folha por extenso"""
    if n <= 20:
        return u"Folha %s." % EXTF[n]
    d, u = divmod(n, 10)
    dez = {2: u"vinte", 3: u"trinta"}[d]
    return u"Folha %s." % (dez if not u else dez + u" e " + EXTF[u])


def hfala(h, m):
    u"""o horário do jeito que se diz: '3 horas e 25 minutos', 'uma hora',
    'meia-noite e 30 minutos'."""
    if h == 0:
        hh = u"meia-noite"
    elif h == 1:
        hh = u"uma hora"
    else:
        hh = u"%d horas" % h
    if m == 0:
        return hh
    return hh + (u" e %d minutos" % m if m != 1 else u" e um minuto")


def voz(s):
    u"""o texto da tela virado em texto que a voz diz certo"""
    s = lp(s)
    s = s.replace(u"÷", u" dividido por ").replace(u"×", u" vezes ")
    # 7h15 · 8h00 · 19h20
    s = re.sub(r"(\d{1,2})h(\d{2})\b",
               lambda m: hfala(int(m.group(1)), int(m.group(2))), s)
    # 1 h 20 min · 2 h 30 min · 13 h 5 min
    s = re.sub(r"(\d+) h (\d+) min\b",
               lambda m: u"%s e %s minutos" % (u"uma hora" if m.group(1) == u"1" else m.group(1) + u" horas",
                                               m.group(2)), s)
    s = re.sub(r"(\d+) h\b",
               lambda m: u"uma hora" if m.group(1) == u"1" else m.group(1) + u" horas", s)
    s = re.sub(r"\b1 horas\b", u"uma hora", s)
    s = re.sub(r"\s+", u" ", s).strip()
    return s


def pv(k, v):
    p(k, voz(v))


def conta(a, b):
    p(u"conta_%d_%d" % (a, b), u"%d dividido por %d." % (a, b))


NUMS = set()


def num(n):
    NUMS.add(n)


def janela(certo, quantas):
    u"""o MESMO leque que o `opNumeros` do folhas.js desenha"""
    de = 1
    if certo > quantas:
        de = max(1, certo - quantas // 2)
    for n in range(de, de + quantas):
        num(n)


def tira_s(w):
    return w[:-1] if w.endswith(u"s") else w


# ---------- as falas de todo caderno ----------
p(u"capa", u"Aprendendo a divisão e as horas. Trinta e cinco folhas para dividir com "
           u"o material dourado e na chave, e para ler e contar as horas. Escreva o "
           u"seu nome ali embaixo e toque em Começar.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"quase", u"Quase! Olhe de novo.")
p(u"escreva", u"Escreva o número usando o teclado.")
p(u"ligue", u"Toque num item do lado esquerdo e depois no seu par do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa das fichas ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"toque_peca", u"Primeiro toque numa peça ali embaixo. Depois toque no lugar dela.")
p(u"vozOn", u"Narração ligada!")
p(u"novoCaderno", u"Caderno novo! Vamos começar.")
p(u"fim", u"Você chegou ao fim! Agora você reparte com o material dourado, arma a "
          u"conta na chave, sabe o que sobra e lê o relógio. E fica a pergunta: "
          u"quantos minutos você passa na escola numa semana inteira?")

# ---------- 1 — repartir os pirulitos ----------
REP = bloco(u"REP")
p(u"p1enun", folha(1) + u" Arraste cada pirulito para uma caixa, até todas "
             u"ficarem iguais. No computador dá para arrastar; no celular, toque no "
             u"pirulito e depois na caixa.")
for _k, _R in REP.items():
    _c = _R[u"n"] // _R[u"k"]
    p(u"rep1_" + _k, u"%d %s para %d %s. Reparta em partes iguais."
      % (_R[u"n"], _R[u"q"], _R[u"k"], _R[u"w"]))
    p(u"certorep1_" + _k, u"Isso! Cada %s ficou com %d. %d dividido por %d é %d."
      % (tira_s(_R[u"w"]), _c, _R[u"n"], _R[u"k"], _c))
    p(u"dicarep1_" + _k, u"Essa caixa já está cheia. Ponha um pirulito em cada caixa e "
                         u"vá dando a volta: assim elas acabam iguais.")

# ---------- 2 e 3 — os problemas ----------
REPT = bloco(u"REPT")
MED = bloco(u"MED")
p(u"p2enun", folha(2) + u" Leia ou ouça cada problema e escolha quantos ficam para "
             u"cada um. Os números são maiores que no terceiro ano: vale fazer a "
             u"conta num papel.")
p(u"p3enun", folha(3) + u" Agora a pergunta mudou. O problema já diz quanto vai em "
             u"cada grupo e pergunta quantos grupos dão. A conta continua sendo de "
             u"dividir.")
for _k, _P in REPT.items():
    _q = _P[u"a"] // _P[u"b"]
    pv(u"pb_" + _k, _P[u"t"])
    janela(_q, 10)
    p(u"certo2_" + _k, u"Isso! %d dividido por %d é %d." % (_P[u"a"], _P[u"b"], _q))
    p(u"dica2_" + _k, u"Descubra quem é o total e em quantas partes ele se reparte. "
                      u"Depois pense: que número, vezes o número de partes, dá o total?")
for _k, _P in MED.items():
    _q = _P[u"a"] // _P[u"b"]
    pv(u"pm_" + _k, _P[u"t"])
    janela(_q, 10)
    p(u"certo3_" + _k, u"Isso! %d dividido por %d é %d." % (_P[u"a"], _P[u"b"], _q))
    p(u"dica3_" + _k, u"Aqui o tamanho de cada grupo já está dito. Pergunte: quantas "
                      u"vezes esse tamanho cabe no total?")

# ---------- 4 — certo ou errado ----------
JULG = bloco(u"JULG")
p(u"p4enun", folha(4) + u" Cada criança fez uma divisão e disse o resultado. Está "
             u"certo ou está errado? Confira com a multiplicação antes de responder.")
p(u"op_certo", u"Está certo.")
p(u"op_errado", u"Está errado.")
for _k, _J in JULG.items():
    pv(u"jg_" + _k, _J[u"t"])
    p(u"certo4_" + _k, (u"Isso! Está certo: " if _J[u"ok"] else u"Isso! Está errado: ")
      + voz(_J[u"pq"]) + u".")
    p(u"dica4_" + _k, u"Faça a conta de volta: multiplique o resultado pelo divisor e "
                      u"some o que sobrou. Dá o número do começo? E o resto é menor "
                      u"que o divisor?")

# ---------- 5 — os nomes ----------
TERM = bloco(u"TERM")
NOMEPARTE = [u"dividendo", u"divisor", u"quociente", u"resto"]
DIZPARTE = [u"o número que se divide", u"o número que diz em quantas partes",
            u"o resultado", u"o que sobra"]
p(u"p5enun", folha(5) + u" Toda divisão tem quatro números com nome. Em 35 dividido "
             u"por 8 igual a 4 e sobram 3: 35 é o dividendo, o que se divide; 8 é o "
             u"divisor; 4 é o quociente, o resultado; e 3 é o resto. Agora toque no "
             u"número que tem o nome pedido.")
for _k, _T in TERM.items():
    _a, _b = _T[u"a"], _T[u"b"]
    _q, _r = _a // _b, _a % _b
    for _n in (_a, _b, _q, _r):
        num(_n)
    p(u"tm_" + _k, u"%d dividido por %d é %d%s. Toque no %s."
      % (_a, _b, _q, (u" e sobram %d" % _r) if _r else u" e não sobra nada",
         NOMEPARTE[_T[u"p"]]))
    p(u"certo5_" + _k, u"Isso! O %s é %d." % (NOMEPARTE[_T[u"p"]], [_a, _b, _q, _r][_T[u"p"]]))
    p(u"dica5_" + _k, u"O %s é %s. Procure esse número na conta."
      % (NOMEPARTE[_T[u"p"]], DIZPARTE[_T[u"p"]]))

# ---------- 6 a 8 — o material dourado ----------
MDN = bloco(u"MDN")
MDS = bloco(u"MDS")
MDT = bloco(u"MDT")
p(u"p6enun", folha(6) + u" O material dourado. O cubinho vale 1, a barra vale 10, "
             u"porque são dez cubinhos, e a placa vale 100, porque são dez barras. "
             u"Conte as peças e escreva o número que elas formam.")
for _k, _N in MDN.items():
    _n = _N[u"n"]
    _c, _d, _u = _n // 100, (_n // 10) % 10, _n % 10
    _pl = []
    if _c:
        _pl.append(u"%d %s" % (_c, u"placa" if _c == 1 else u"placas"))
    if _d:
        _pl.append(u"%d %s" % (_d, u"barra" if _d == 1 else u"barras"))
    if _u:
        _pl.append(u"%d %s" % (_u, u"cubinho" if _u == 1 else u"cubinhos"))
    _txt = u", ".join(_pl[:-1]) + (u" e " if len(_pl) > 1 else u"") + _pl[-1]
    p(u"mdn_" + _k, u"Quantas placas, quantas barras e quantos cubinhos? Conte e "
                    u"escreva o número.")
    p(u"certo6_" + _k, u"Isso! %s formam %d." % (_txt[0].upper() + _txt[1:], _n))
    p(u"dica6_" + _k, u"Conte primeiro as placas: cada uma vale cem. Depois as "
                      u"barras, de dez em dez. Por último os cubinhos, de um em um.")
p(u"p7enun", folha(7) + u" Leve cada peça para um grupo, dando a volta, até os "
             u"grupos ficarem iguais. Comece pelas peças grandes: placas, depois "
             u"barras, depois cubinhos. No computador dá para arrastar; no celular, "
             u"toque na peça e depois no grupo.")
p(u"p8enun", folha(8) + u" Agora sobra uma barra que não dá para pôr inteira em "
             u"todos os grupos. Leve essa barra para a casa da troca: ela vira dez "
             u"cubinhos, e aí dá para repartir.")
p(u"pc_p", u"Placa: vale cem.")
p(u"pc_b", u"Barra: vale dez.")
p(u"pc_u", u"Cubinho: vale um.")
p(u"trocou", u"Trocou! A barra virou dez cubinhos. Agora reparta os cubinhos também.")
for _pi, _blk in ((7, MDS), (8, MDT)):
    for _k, _M in _blk.items():
        _q = _M[u"a"] // _M[u"b"]
        p(u"md_" + _k, u"%d dividido por %d: reparta as peças em %d grupos iguais."
          % (_M[u"a"], _M[u"b"], _M[u"b"]))
        p(u"certomd%d_%s" % (_pi, _k), u"Isso! Cada grupo ficou com %d. %d dividido "
          u"por %d é %d." % (_q, _M[u"a"], _M[u"b"], _q))
    p(u"dicamd%d_p" % _pi, u"Esse grupo já tem as placas dele. Leve esta placa para "
                           u"um grupo que ainda tem menos.")
    p(u"dicamd%d_b" % _pi, u"Esse grupo já tem as barras dele. Olhe os outros grupos: "
                           u"se todos já têm o mesmo tanto, a barra que sobrou vai "
                           u"para a casa da troca.")
    p(u"dicamd%d_b0" % _pi, u"Uma barra só não dá para todos os grupos. Leve-a para "
                            u"a casa da troca.")
    p(u"dicamd%d_u" % _pi, u"Esse grupo já tem os cubinhos dele. Dê a volta: um "
                           u"cubinho em cada grupo.")
p(u"dicatroca1_8", u"Na casa da troca só entra a barra: é ela que vira dez cubinhos.")
p(u"dicatroca2_8", u"Ainda não! Primeiro dê as barras aos grupos, uma para cada. Só "
                   u"a barra que sobrar vai para a troca.")

# ---------- 9 a 11 — a chave ----------
for _nome, _pi in ((u"ORD", 9), (u"TROC", 10), (u"REST", 11)):
    _B = bloco(_nome)
    for _k, _C in _B.items():
        _a, _b = _C[u"a"], _C[u"b"]
        _q, _r = _a // _b, _a % _b
        conta(_a, _b)
        if _pi == 11:
            p(u"certo%d_%s" % (_pi, _k), u"Isso! %d dividido por %d dá %d e sobram %d."
              % (_a, _b, _q, _r))
            p(u"dica%d_%s" % (_pi, _k), u"Divida ordem por ordem, e no fim olhe o que "
              u"sobrou: o resto tem de ser menor que o divisor. Escreva primeiro o "
              u"quociente e depois o resto.")
        else:
            p(u"certo%d_%s" % (_pi, _k), u"Isso! %d dividido por %d é %d." % (_a, _b, _q))
            p(u"dica%d_%s" % (_pi, _k),
              u"Comece pelas centenas: quantas vezes o %d cabe? O que não coube "
              u"desce e se junta às dezenas. Depois as unidades." % _b
              if _pi == 10 else
              u"Olhe o material: divida as placas, depois as barras, depois os "
              u"cubinhos. Cada ordem dá um algarismo do quociente.")
p(u"p9enun", folha(9) + u" A mesma divisão, agora na chave. O material está ali: "
             u"divida as placas, depois as barras, depois os cubinhos, uma ordem de "
             u"cada vez, e escreva o quociente embaixo do divisor.")
p(u"p10enun", folha(10) + u" Agora com troca, e sem o material: quando a placa ou a "
              u"barra não dá para repartir, ela é trocada por dez peças menores, que se "
              u"juntam às outras, igual à casa da troca. Escreva o quociente.")
p(u"p11enun", folha(11) + u" Agora a conta sobra. Escreva o quociente embaixo do "
              u"divisor e, depois, o resto embaixo do dividendo. O resto é sempre "
              u"menor que o divisor.")

# ---------- 12 — estimar ----------
EST = bloco(u"EST")
p(u"p12enun", folha(12) + u" O divisor agora tem dois algarismos. Antes de fazer a "
              u"conta, estime: arredonde o divisor para a dezena mais perto e pense "
              u"quantas vezes ele cabe no dividendo.")
for _k, _C in EST.items():
    _q = _C[u"a"] // _C[u"b"]
    conta(_C[u"a"], _C[u"b"])
    janela(_q, 9)
    p(u"certo12_" + _k, u"Isso! %d vezes %d é %d, então %d dividido por %d é %d."
      % (_q, _C[u"b"], _C[u"a"], _C[u"a"], _C[u"b"], _q))
    p(u"dica12_" + _k, u"Arredonde o %d para a dezena mais perto e veja quantas vezes "
                       u"ela cabe no %d. Depois confira multiplicando." % (_C[u"b"], _C[u"a"]))

# ---------- 13 e 14 — ligar ----------
p(u"p13enun", folha(13) + u" Resolva cada divisão, num papel se quiser, e ligue a "
              u"conta ao seu quociente: toque na conta e depois no número.")
p(u"p14enun", folha(14) + u" Agora o divisor tem dois algarismos. Estime primeiro, "
              u"confira com a multiplicação e ligue cada conta ao seu quociente.")
for _nome, _pi in ((u"LIG1", 13), (u"LIG2", 14)):
    for _k, _C in bloco(_nome).items():
        _q = _C[u"a"] // _C[u"b"]
        conta(_C[u"a"], _C[u"b"])
        num(_q)
        p(u"certo%d_%s" % (_pi, _k), u"Isso! %d dividido por %d é %d."
          % (_C[u"a"], _C[u"b"], _q))
        p(u"dica%d_%s" % (_pi, _k), u"Multiplique o número da direita pelo divisor. "
          u"Tem de dar o dividendo, certinho.")

# ---------- 15 e 26 — as gavetas ----------
GAV = bloco(u"GAV")
p(u"p15enun", folha(15) + u" Faça cada conta e ponha na gaveta certa: exata, quando "
              u"não sobra nada, ou não exata, quando sobra resto. Toque na conta e "
              u"depois na gaveta, ou arraste.")
p(u"gav_ex_e", u"Exata: não sobra nada.")
p(u"gav_ex_n", u"Não exata: sobra resto.")
for _k, _P in GAV[u"ex"][u"pal"].items():
    _r = _P[u"a"] % _P[u"b"]
    p(u"diz2_ex_" + _k, u"%d dividido por %d." % (_P[u"a"], _P[u"b"]))
    p(u"certo15_" + _k, (u"Isso! %d dividido por %d sobra %d: não é exata."
                         % (_P[u"a"], _P[u"b"], _r)) if _r else
      (u"Isso! %d dividido por %d é %d certinho: é exata."
       % (_P[u"a"], _P[u"b"], _P[u"a"] // _P[u"b"])))
    p(u"dica15_" + _k, u"Faça a conta até o fim e olhe o que ficou: sobrou alguma "
                       u"coisa ou não sobrou nada?")
p(u"p26enun", folha(26) + u" Cada horário foi lido num relógio digital. Ponha na "
              u"gaveta da parte do dia: manhã, das 6 às 11 e 59; tarde, das 12 às 17 "
              u"e 59; noite, das 18 às 23 e 59; ou madrugada, da meia-noite às 5 e 59.")
_PARTE = {u"ma": u"manhã", u"ta": u"tarde", u"no": u"noite", u"md": u"madrugada"}
for _c in GAV[u"dia"][u"cols"]:
    p(u"gav_dia_" + _c[u"k"], _c[u"n"] + u".")
for _k, _P in GAV[u"dia"][u"pal"].items():
    p(u"diz2_dia_" + _k, hfala(_P[u"h"], _P[u"m"]) + u".")
    p(u"certo26_" + _k, u"Isso! %s é de %s." % (hfala(_P[u"h"], _P[u"m"]).capitalize(),
                                              _PARTE[_P[u"c"]]))
    p(u"dica26_" + _k, u"Olhe só a hora, antes dos dois-pontos, e procure em que faixa "
                       u"ela cabe: de 6 a 11 é manhã, de 12 a 17 é tarde, de 18 a 23 é "
                       u"noite, e de 0 a 5 é madrugada.")

# ---------- 16 — a conta de volta ----------
INV = bloco(u"INV")
p(u"p16enun", folha(16) + u" A conta de volta, do jeito do modelo: 5 vezes 3 é 15, "
              u"então 15 dividido por 3 é 5. Descubra o número que falta: ele é a "
              u"resposta das duas contas.")
for _k, _I in INV.items():
    _pr = _I[u"x"] * _I[u"y"]
    p(u"iv_" + _k, u"%d vezes quanto é %d? Então %d dividido por %d é quanto?"
      % (_I[u"y"], _pr, _pr, _I[u"y"]))
    p(u"certo16_" + _k, u"Isso! %d vezes %d é %d, então %d dividido por %d é %d."
      % (_I[u"y"], _I[u"x"], _pr, _pr, _I[u"y"], _I[u"x"]))
    p(u"dica16_" + _k, u"Vá multiplicando o %d por 10, por 11, por 12, e veja qual "
                       u"chega no %d." % (_I[u"y"], _pr))

# ---------- 17 — a trilha ----------
TRILHA = bloco(u"TRILHA")
p(u"p17enun", folha(17) + u" O cachorro Hulk quer chegar à casinha. Em cada passo há "
              u"três casas; ele só pisa na casa em que a divisão sobra exatamente 1.")
for _k, _T in TRILHA.items():
    for _o in _T[u"ops"]:
        conta(_o[u"a"], _o[u"b"])
    _bom = [o for o in _T[u"ops"] if o[u"a"] % o[u"b"] == 1][0]
    p(u"certo17_" + _k, u"Isso! %d dividido por %d sobra 1. O Hulk andou!"
      % (_bom[u"a"], _bom[u"b"]))
    p(u"dica17_" + _k, u"Faça as três contas e olhe o resto de cada uma. Uma fecha "
                       u"certinho, uma sobra 1 e uma sobra mais. O Hulk quer a do 1.")

# ---------- 18 — os restos iguais ----------
MESMO = bloco(u"MESMO")
p(u"p18enun", folha(18) + u" Uma investigação. Marque todos os números que, divididos "
              u"pelo número pedido, deixam o resto pedido. Depois toque em Conferir, e "
              u"repare na distância entre eles.")
for _k, _M in MESMO.items():
    for _n in _M[u"nums"]:
        num(_n)
    _bons = [n for n in _M[u"nums"] if n % _M[u"b"] == _M[u"r"]]
    p(u"ms_" + _k, u"Divididos por %d, quais sobram %d?" % (_M[u"b"], _M[u"r"]))
    p(u"certo18_" + _k, u"Isso! Eles vão de %d em %d: somar %d não muda o resto."
      % (_M[u"b"], _M[u"b"], _M[u"b"]))
    p(u"dica18_" + _k, u"Faça a conta de um número de cada vez. Achou um que serve? "
                       u"Some %d a ele e teste o próximo." % _M[u"b"])

# ---------- 19 — o quebra-cabeça ----------
PUZ = bloco(u"PUZ")
p(u"p19enun", folha(19) + u" Resolva a conta de cada peça e leve a peça até o seu "
              u"resultado no tabuleiro. No fim, a figura aparece inteira.")
for _k, _P in PUZ.items():
    conta(_P[u"a"], _P[u"b"])
    p(u"certo19_" + _k, u"Isso! %d dividido por %d é %d." % (_P[u"a"], _P[u"b"], _P[u"r"]))
    p(u"dica19_" + _k, u"Estime: arredonde o %d e veja quantas vezes cabe no %d. "
                       u"Depois confira multiplicando." % (_P[u"b"], _P[u"a"]))

# ---------- 20 — qual é a pergunta? ----------
ELAB = bloco(u"ELAB")
p(u"p20enun", folha(20) + u" Agora o problema é seu. Cada história tem os números, mas "
              u"falta a pergunta. Escolha a pergunta que a divisão responde: é assim "
              u"que se inventa um problema.")
for _k, _E in ELAB.items():
    pv(u"el_" + _k, _E[u"t"])
    for _i, _o in enumerate(_E[u"ops"]):
        pv(u"elop_%s_%d" % (_k, _i), _o)
    _q = _E[u"a"] // _E[u"b"]
    p(u"certo20_" + _k, u"Isso! A divisão responde: %d dividido por %d é %d %s."
      % (_E[u"a"], _E[u"b"], _q, _E[u"u"]))
    p(u"dica20_" + _k, u"Qual pergunta se responde com os números da história? As "
                       u"outras pedem coisas que a história não conta.")

# ---------- 21 — os minutos ----------
MINU = bloco(u"MINU")
p(u"p21enun", folha(21) + u" No relógio, o ponteiro azul e comprido marca os minutos, "
              u"e cada número vale 5 minutos. A flor ajuda: as pétalas marcam os "
              u"minutos. Onde o ponteiro azul parou, quantos minutos são?")
for _k, _M in MINU.items():
    _mm = _M[u"n"] * 5
    _de = max(5, _mm - 15)
    if _de + 30 > 55:
        _de = 25
    for _n in range(_de, _de + 31, 5):
        num(_n)
    p(u"mn_" + _k, u"O ponteiro azul está no %d. Quantos minutos?" % _M[u"n"])
    p(u"certo21_" + _k, u"Isso! No %d são %d minutos: %d vezes 5." % (_M[u"n"], _mm, _M[u"n"]))
    p(u"dica21_" + _k, u"Conte de 5 em 5, começando do 1: 5, 10, 15, e assim até chegar "
                       u"no número em que o ponteiro azul parou.")

# ---------- 22 — que horas são? ----------
LER = bloco(u"LER")
p(u"p22enun", folha(22) + u" Agora sem a flor. Leia o relógio: o ponteiro rosa e "
              u"curto marca a hora, o azul marca os minutos. Escreva a hora nas "
              u"casinhas.")
p(u"quehoras", u"Que horas o relógio está marcando?")
for _k, _L in LER.items():
    p(u"certo22_" + _k, u"Isso! São %s." % hfala(_L[u"h"], _L[u"m"]))
    p(u"dica22_" + _k, u"Primeiro o ponteiro rosa: ele já passou de qual número? Essa "
                       u"é a hora. Depois o azul: conte de 5 em 5.")

# ---------- 23 e 24 — girar ----------
p(u"p23enun", folha(23) + u" O seu relógio de ponteiros. Gire o ponteiro azul com o "
              u"dedo, ou use os botões, até marcar a hora pedida. O ponteiro rosa anda "
              u"junto, como num relógio de verdade. Depois toque em Conferir.")
p(u"p24enun", folha(24) + u" Agora a hora da tarde e da noite. O horário vem como no "
              u"relógio digital, de 0 a 23 horas. Tire 12 da hora e marque no relógio "
              u"de ponteiros.")
for _nome, _pi, _pref in ((u"GIRA", 23, u"gi_"), (u"GIRA24", 24, u"gj_")):
    for _k, _G in bloco(_nome).items():
        p(_pref + _k, u"Marque %s." % hfala(_G[u"h"], _G[u"m"]))
        p(u"certo%d_%s" % (_pi, _k), u"Isso! O relógio marca %s."
          % hfala(_G[u"h"] % 12 or 12, _G[u"m"]))
        p(u"dica%d_%s" % (_pi, _k),
          (u"%d horas no relógio de ponteiros é o %d. " % (_G[u"h"], _G[u"h"] - 12)
           if _G[u"h"] > 12 else u"") +
          u"Ponha primeiro o ponteiro azul nos minutos, contando de 5 em 5. Depois "
          u"acerte a hora com os botões de uma hora.")

# ---------- 25 e 34 — o relógio e o digital ----------
LIG3 = bloco(u"LIG3")
MEM = bloco(u"MEM")
p(u"p25enun", folha(25) + u" Ligue o relógio de ponteiros ao relógio digital que "
              u"marca o mesmo horário: toque no relógio e depois no horário.")
for _k, _H in LIG3.items():
    p(u"rl_" + _k, u"Relógio de ponteiros. Que horas ele marca?")
    p(u"hora_%d_%d" % (_H[u"h"], _H[u"m"]), hfala(_H[u"h"], _H[u"m"]) + u".")
    p(u"certo25_" + _k, u"Isso! Os dois marcam %s." % hfala(_H[u"h"], _H[u"m"]))
    p(u"dica25_" + _k, u"No relógio de ponteiros, o ponteiro rosa diz a hora e o "
                       u"ponteiro azul diz os minutos. Leia os dois e procure o digital igual.")
p(u"p34enun", folha(34) + u" Vire duas cartas e ache o relógio de ponteiros e o "
              u"horário digital que marcam a mesma hora.")
for _k, _H in MEM.items():
    p(u"hora_%d_%d" % (_H[u"h"], _H[u"m"]), hfala(_H[u"h"], _H[u"m"]) + u".")
p(u"memok", u"Par! Os dois marcam a mesma hora.")
p(u"memfim", u"Tabuleiro limpo! Você achou todos os pares.")
p(u"memdica", u"Guarde onde cada carta estava: elas voltam para baixo no mesmo lugar.")

# ---------- 27 — hora, minuto e segundo ----------
REL = bloco(u"REL")
p(u"p27enun", folha(27) + u" Preencha os espaços: quanto tempo cabe em quanto? "
              u"Escreva o número nas casinhas.")
for _k, _R in REL.items():
    pv(u"rl2_" + _k, u"%s quantos %s?" % (_R[u"t"], _R[u"u"]))
    pv(u"certo27_" + _k, u"Isso! %s %d %s." % (_R[u"t"], _R[u"r"], _R[u"u"]))
    p(u"dica27_" + _k, u"Lembre: uma hora tem 60 minutos, um minuto tem 60 segundos e "
                       u"um dia tem 24 horas. Quando são várias, multiplique.")

# ---------- 28 — minutos em horas ----------
PONT = bloco(u"PONT")
p(u"p28enun", folha(28) + u" A divisão encontra o relógio. Uma hora tem 60 minutos, "
              u"então para saber quantas horas cabem em muitos minutos é só dividir por "
              u"60. E quando sobra, o resto são os minutos: 150 dividido por 60 é 2 e "
              u"sobram 30.")
for _k, _P in PONT.items():
    pv(u"pt_" + _k, _P[u"t"] + u" Quanto tempo é isso?")
    for _i, _o in enumerate(_P[u"ops"]):
        pv(u"ptop_%s_%d" % (_k, _i), _o)
    _h, _m = divmod(_P[u"min"], 60)
    p(u"certo28_" + _k, u"Isso! %d dividido por 60 é %d e sobram %d: %s."
      % (_P[u"min"], _h, _m, hfala(_h, _m).replace(u"horas", u"horas", 1))
      if _m else u"Isso! %d dividido por 60 é %d: %s." % (_P[u"min"], _h,
                                                          u"uma hora" if _h == 1 else u"%d horas" % _h))
    p(u"dica28_" + _k, u"Quantas vezes o 60 cabe no %d? Esse número são as horas. O "
                       u"que sobrar são os minutos." % _P[u"min"])

# ---------- 29 e 30 — antes e depois ----------
MAIS = bloco(u"MAIS")
ANDE = bloco(u"ANDE")


def anda(h, m, d):
    t = (h * 60 + m + d) % 1440
    return t // 60, t % 60


p(u"p29enun", folha(29) + u" O relógio digital diz a hora de agora. Escreva que horas "
              u"serão daqui a 15 minutos. Cuidado quando os minutos passam de 60: a "
              u"hora muda!")
for _k, _A in MAIS.items():
    _r = anda(_A[u"h"], _A[u"m"], 15)
    p(u"ma_" + _k, u"Agora são %s. Daqui a 15 minutos, que horas serão?"
      % hfala(_A[u"h"], _A[u"m"]))
    p(u"certo29_" + _k, u"Isso! Serão %s." % hfala(*_r))
    p(u"dica29_" + _k, u"Some 15 aos minutos. Se passar de 60, tire 60 dos minutos e "
                       u"ponha uma hora a mais.")
p(u"p30enun", folha(30) + u" Agora para trás e para a frente: 15 minutos antes, ou "
              u"meia hora depois. Leia bem o que cada linha pede.")
for _k, _A in ANDE.items():
    _r = anda(_A[u"h"], _A[u"m"], _A[u"d"])
    _o = u"15 minutos antes" if _A[u"d"] < 0 else u"meia hora depois"
    p(u"ad_" + _k, u"Agora são %s. %s, que horas são?"
      % (hfala(_A[u"h"], _A[u"m"]), _o[0].upper() + _o[1:]))
    p(u"certo30_" + _k, u"Isso! %s: %s." % (_o[0].upper() + _o[1:], hfala(*_r)))
    p(u"dica30_" + _k,
      u"Tire 15 dos minutos. Se não der, a hora volta uma e os minutos ficam 60 menos "
      u"o que faltou." if _A[u"d"] < 0 else
      u"Meia hora são 30 minutos. Some aos minutos; se passar de 60, a hora anda uma.")

# ---------- 31 e 32 — duração ----------
p(u"p31enun", folha(31) + u" A agenda diz quando cada coisa começa e quando termina. "
              u"Quanto tempo durou? Conte do começo até o fim: primeiro até a hora "
              u"cheia, depois o resto.")
p(u"p32enun", folha(32) + u" Agora a pergunta é outra: dá tempo? A que horas termina? "
              u"Some a duração ao horário de começo e depois compare.")
for _nome, _pi, _pref in ((u"DUR", 31, u"du_"), (u"TEMPO", 32, u"te_")):
    for _k, _P in bloco(_nome).items():
        pv(_pref + _k, _P[u"t"])
        for _i, _o in enumerate(_P[u"ops"]):
            pv(u"%sop_%s_%d" % (_pref, _k, _i), _o)
        pv(u"certo%d_%s" % (_pi, _k), u"Isso! " + _P[u"ops"][0] + u".")
        p(u"dica%d_%s" % (_pi, _k),
          u"Conte do começo até a próxima hora cheia, e depois da hora cheia até o "
          u"fim. Some os dois pedaços." if _pi == 31 else
          u"Some a duração ao horário do começo: primeiro as horas, depois os "
          u"minutos. Se os minutos passarem de 60, a hora anda uma.")

# ---------- 33 — a rotina ----------
ROT = bloco(u"ROT")
p(u"p33enun", folha(33) + u" Os horários do dia estão misturados. Toque em cada um "
              u"na ordem em que acontecem, do mais cedo ao mais tarde.")
for _k, _R in ROT.items():
    pv(u"ro_" + _k, _R[u"t"] + u".")
    for _E in _R[u"ord"]:
        p(u"roe_" + _E[u"k"], u"%s, às %s." % (_E[u"n"], hfala(_E[u"h"], _E[u"m"])))
    p(u"certo33_" + _k, u"Isso! Tudo em ordem, do mais cedo ao mais tarde.")
    p(u"dica33_" + _k, u"Compare primeiro as horas. Se a hora for a mesma, quem tem "
                       u"menos minutos vem antes.")

# ---------- 35 — o cartaz ----------
CARTAZ = bloco(u"CARTAZ")
p(u"p35enun", folha(35) + u" Este cartaz é seu. Em cada linha, escolha o exemplo que "
              u"cabe naquele nome, e leve os seis na cabeça.")
for _k, _C in CARTAZ.items():
    pv(u"cartaz_" + _k, _C[u"n"] + u": " + _C[u"d"])
    pv(u"ex_" + _k, _C[u"ex"] + u".")
    pv(u"certo35_" + _k, u"Isso! " + _C[u"n"] + u": " + _C[u"ex"] + u".")
    p(u"dica35_" + _k, u"Leia o nome da linha de novo e procure o exemplo que faz "
                       u"exatamente isso.")

# ---------- os números das opções ----------
for _n in sorted(NUMS):
    p(u"num_%d" % _n, u"%d." % _n)

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
