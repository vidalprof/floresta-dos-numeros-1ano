# -*- coding: utf-8 -*-
u"""
============================================================
 A LETRA QUE MUDA TUDO — gerador das falas (degrau 6)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ AQUI A VOZ DIZ O NOME DA LETRA — e isto NÃO contradiz o degrau 4.
    No degrau 4 (O Som que Abre) dizer "bê" era o ERRO: lá o assunto era o SOM
    /b/, e o nome da letra esconde o som. Aqui o assunto É a letra — o currículo
    de Blumenau pede *"nomear as letras do alfabeto"* —, e o nome é como a
    criança vai pedir a letra ao professor e achá-la no teclado.

 ⚠️⚠️ E POR ISSO ESTE CADERNO NÃO TEM RECORTE DE SÍLABA.
    Nome de letra é PALAVRA de verdade ("éle", "ême", "érre"), e o sintetizador
    diz palavra certo — o beco da sílaba soletrada ("vê-á" no lugar de VA) não
    existe aqui. O `silabas.json` sai vazio de propósito, e o portão
    `_qa/silabas.py` confere isso sozinho.
    ⚠️ Mas os nomes vão ESCRITOS COMO SE FALAM, um a um: mandar o TTS ler a
    letra "F" sozinha devolve coisa errada; "éfe" devolve certo. É o mesmo
    princípio — a voz não lê símbolo, lê palavra.

 Lê do próprio `index.html` os dois blocos que são a verdade do conteúdo:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `var PAL = { bola:["BOLA",["BO","LA"]], ... }` — a escrita das palavras.

 Uso:  python3 _let1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"le_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\]', bloco):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])

# os nomes das letras, escritos como se falam (o mesmo mapa do folhas.js)
NOMELETRA = {u"A": u"á", u"B": u"bê", u"C": u"cê", u"D": u"dê", u"E": u"é",
             u"F": u"éfe", u"G": u"gê", u"H": u"agá", u"I": u"i", u"J": u"jota",
             u"K": u"cá", u"L": u"éle", u"M": u"ême", u"N": u"êne", u"O": u"ó",
             u"P": u"pê", u"Q": u"quê", u"R": u"érre", u"S": u"ésse", u"T": u"tê",
             u"U": u"u", u"V": u"vê", u"W": u"dábliu", u"X": u"xis",
             u"Y": u"ípsilon", u"Z": u"zê"}


def esc(w):
    return PAL[w][0] if w in PAL else w.upper()


DIZ = {u"maca": u"maçã", u"balao": u"balão", u"leao": u"leão", u"limao": u"limão",
       u"onibus": u"ônibus", u"xicara": u"xícara", u"jacare": u"jacaré",
       u"chapeu": u"chapéu", u"pao": u"pão", u"navio": u"navio"}


def falado(w):
    return DIZ.get(w, esc(w).lower())


def soletrado(w):
    u"""'bê, ó, éle, á' — a palavra letra por letra, com o NOME de cada uma"""
    return u", ".join(NOMELETRA.get(ch, ch) for ch in esc(w))


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"A Letra que Muda Tudo. Dez folhas para descobrir que trocar uma "
              u"letra troca a palavra inteira. Escreva o seu nome ali embaixo e "
              u"toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim! Agora você sabe que cada letra conta: uma letra "
             u"só já vira outra palavra. Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva a letra que falta."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Olhe a figura e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois no nome dela."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram."

F[u"p1enun"] = (u"Folha um: a letra que muda tudo. Toque em cada letra e veja a "
                u"palavra mudar. Experimente todas!")
F[u"p2enun"] = u"Folha dois: qual letra falta no começo do nome da figura?"
F[u"p3enun"] = u"Folha três: agora o buraco anda. No meio, e depois no fim da palavra."
F[u"p4enun"] = (u"Folha quatro: escute a palavra. As duas figuras são quase iguais! "
                u"Qual delas é?")
F[u"p5enun"] = (u"Folha cinco: marque todas as figuras cujo nome tem esta letra. "
                u"Depois toque em Pronto.")
F[u"p6enun"] = u"Folha seis: as letras saíram fora de ordem. Monte o nome da figura."
F[u"p7enun"] = (u"Folha sete: agora uma letra sobra! Monte o nome e deixe a intrusa "
                u"de fora.")
F[u"p8enun"] = u"Folha oito: ligue cada figura ao nome dela. Cuidado: são quase iguais!"
F[u"p9enun"] = u"Folha nove: escute a palavra e escreva a letra que falta."
F[u"p10enun"] = u"Folha dez: toque nas palavras que você quer no seu mural."

# ---- o nome de cada letra ------------------------------------------------------
for L in sorted(NOMELETRA):
    F[u"ltr_%s" % L] = NOMELETRA[L] + u"."

# ---- toda palavra que aparece no caderno ----------------------------------------
usadas = set()


def colhe(x):
    if isinstance(x, list):
        for y in x:
            colhe(y)
    elif isinstance(x, (str, type(u""))) and x in PAL:
        usadas.add(x)


for chave in IT:
    colhe(IT[chave])
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: a letra que muda tudo ----------------------------------------------
for reg in IT[u"p1"]:
    molde, onde, ws = reg[0], reg[1], reg[2]
    lista = u", ".join(falado(w) for w in ws[:-1]) + u" e " + falado(ws[-1])
    F[u"certo1_%s" % ws[0]] = (u"Viu? Uma letra só, e a palavra virou outra: %s. "
                               u"É sempre a letra que manda!" % lista)

# ---- folhas 2 e 3: a letra que falta ----------------------------------------------
for tag, n in ((u"p2", 2), (u"p3", 3), (u"p3b", 3)):
    for reg in IT[tag]:
        w, onde = reg[0], reg[1]
        letra = esc(w)[onde]
        onde_diz = (u"no começo" if onde == 0
                    else (u"no fim" if onde == len(esc(w)) - 1 else u"no meio"))
        F[u"certo%d_%s" % (n, w)] = (u"Isso! %s, com %s %s. %s."
                                     % (falado(w).capitalize(), NOMELETRA[letra],
                                        onde_diz, soletrado(w)))
        F[u"dica%d_%s" % (n, w)] = (u"Olhe a figura: é %s. Agora escute a palavra "
                                    u"devagar e pense na letra que falta %s."
                                    % (falado(w), onde_diz))

# ---- folha 4: duas palavras quase iguais -------------------------------------------
for par in IT[u"p4"]:
    a, b = par
    ta, tb = esc(a), esc(b)
    k = [i for i in range(len(ta)) if ta[i] != tb[i]][0]
    F[u"certo4_%s" % a] = (u"Isso! %s e %s mudam uma letra só: %s e %s. "
                           u"Você viu a diferença!"
                           % (falado(a).capitalize(), falado(b),
                              NOMELETRA[ta[k]], NOMELETRA[tb[k]]))
    # ⭐ a dica ENSINA O TRUQUE: não é a palavra parecida, é a letra que muda
    F[u"dica4_%s" % a] = (u"As duas são quase iguais! A diferença é uma letra só. "
                          u"Uma é %s e a outra é %s. Escute de novo."
                          % (soletrado(a), soletrado(b)))

# ---- folha 5: ache todas com esta letra ---------------------------------------------
for reg in IT[u"p5"]:
    letra, lista = reg[0], reg[1]
    certas = [w for w in lista if letra in esc(w)]
    nomes = u", ".join(falado(w) for w in certas[:-1]) + u" e " + falado(certas[-1])
    F[u"certo5_%s" % letra] = (u"Muito bem! A letra %s está em %s."
                               % (NOMELETRA[letra], nomes))
    F[u"dica5_%s" % letra] = (u"Procure a letra %s dentro do nome de cada figura — "
                              u"ela pode estar no começo, no meio ou no fim. "
                              u"Sobrou alguma, ou marcou uma a mais?" % NOMELETRA[letra])

# ---- folhas 6 e 7: montar com as letras ---------------------------------------------
for w in IT[u"p6"]:
    F[u"certo6_%s" % w] = u"Isso! %s: %s." % (falado(w).capitalize(), soletrado(w))
    F[u"dica6_%s" % w] = (u"Fale o nome da figura devagar: %s. Qual é a letra que "
                          u"vem agora?" % falado(w))
for reg in IT[u"p7"]:
    w, extra = reg[0], reg[1]
    F[u"certo7_%s" % w] = (u"Muito bem! %s: %s. E a letra %s não era desta palavra."
                           % (falado(w).capitalize(), soletrado(w), NOMELETRA[extra]))
    F[u"dica7_%s" % w] = (u"Uma das letras do banco não é desta palavra. Fale o nome "
                          u"da figura devagar: %s." % falado(w))

# ---- folha 8: ligar a figura ao nome --------------------------------------------------
for g in IT[u"p8"]:
    for w in g:
        F[u"certo8_%s" % w] = (u"Isso! %s se escreve %s."
                               % (falado(w).capitalize(), soletrado(w)))
        F[u"dica8_%s" % w] = (u"Os três nomes começam quase igual. Leia até o FIM "
                              u"antes de ligar: %s é %s."
                              % (falado(w), soletrado(w)))

# ---- folha 9: escrever a letra que falta ------------------------------------------------
for reg in IT[u"p9"]:
    w, onde = reg[0], reg[1]
    letra = esc(w)[onde]
    F[u"certo9_%s" % w] = (u"Muito bem! %s, com %s. %s."
                           % (falado(w).capitalize(), NOMELETRA[letra], soletrado(w)))
    F[u"dica9_%s" % w] = (u"Olhe a figura: é %s. Escreva só a letra que está faltando "
                          u"no quadradinho." % falado(w))

# ---- folha 10: o mural --------------------------------------------------------------------
for w in IT[u"p10"]:
    F[u"certo10_%s" % w] = (u"%s: %s. Foi para o seu mural!"
                            % (falado(w).capitalize(), soletrado(w)))


def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    t = F[k]
    if not t:
        continue
    c = chave(t)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": t, u"voz": VOZ})

io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
# ⚠️ VAZIO DE PROPÓSITO: este caderno não recorta sílaba nenhuma (ver o cabeçalho)
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ, u"palavras": {}},
               ensure_ascii=False, indent=1))

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); sem recorte de sílaba (de propósito)"
      % (len(F), len(falas)))
