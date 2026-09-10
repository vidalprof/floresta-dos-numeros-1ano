# -*- coding: utf-8 -*-
u"""
============================================================
 BATE-PALMA DAS PALAVRAS — gerador das falas

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ E NESTE CADERNO A VOZ **É** O CONTEÚDO, não apoio.
    Segmentar em sílabas é consciência FONOLÓGICA: mora no ouvido e na boca. Uma
    folha de sílaba sem voz não ensina a ouvir pedaço nenhum — ensina a contar
    quadradinhos desenhados, que é outra coisa e não serve para ler.

 ⚠️⚠️ CADA PALMA DIZ A SUA SÍLABA, E ELA É RECORTADA DA PRÓPRIA PALAVRA.
    Beco já pago nesta casa: escrever a sílaba "como se fala" (ÇÃ -> "sã") e
    mandar o TTS ler solto NUNCA fecha, porque a MESMA sílaba escrita tem sons
    diferentes conforme a palavra ("BO" é [bɔ] em BOLA e [bo] em BOLO). O
    `_padrao/silabas_voz.py` manda o Edge TTS ler `bo, ne, ca`, recebe do próprio
    serviço os marcadores de tempo e CORTA o mp3 neles. A criança ouve a sílaba
    na voz, no ritmo e na altura daquela palavra. O que sai daqui é o mapa que
    aquela ferramenta lê (`silabas.json`) e o `SILMAP` que o app usa.

 Lê do próprio `index.html` os dois blocos que são a verdade do conteúdo:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `var PAL = { bola:["BOLA",["BO","LA"]], ... }` — a escrita e as SÍLABAS.

 Uso:  python3 _sil1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"sl_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\]', bloco):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])


def esc(w):
    return PAL[w][0] if w in PAL else w.upper()


def sil(w):
    return PAL[w][1] if w in PAL else [w.upper()]


# ⚠️ A palavra COMO SE FALA. A voz lê a minúscula melhor que a caixa alta, e
#    algumas o TTS erra na forma escrita — aqui elas vão consertadas, uma a uma.
DIZ = {u"maca": u"maçã", u"balao": u"balão", u"leao": u"leão", u"limao": u"limão",
       u"onibus": u"ônibus", u"xicara": u"xícara", u"jacare": u"jacaré",
       u"chapeu": u"chapéu", u"pao": u"pão", u"navio": u"navio"}


def falado(w):
    return DIZ.get(w, esc(w).lower())


def empedacos(w):
    u"""'ba... na... na' — as reticências fazem a voz separar de verdade"""
    return u"... ".join(s.lower() for s in sil(w))


def palmas(n):
    return u"uma palma" if n == 1 else u"%d palmas" % n


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"Bate-Palma das Palavras. Dez folhas para descobrir que toda palavra "
              u"tem pedaços. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim do Bate-Palma! Agora você sabe ouvir os pedaços de "
             u"qualquer palavra. Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva o número."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Escute de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois no número de palmas dela."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram."

F[u"p1enun"] = (u"Folha um: bata palma em cada pedaço. Toque nos pedaços na ordem e "
                u"escute cada um.")
F[u"p2enun"] = u"Folha dois: fale a palavra batendo palma. Quantas palmas você bateu?"
F[u"p3enun"] = (u"Folha três: pinte um pedacinho para cada palma da palavra. "
                u"Depois toque em Pronto.")
F[u"p4enun"] = u"Folha quatro: bata palma nas duas. Qual delas tem mais pedaços?"
F[u"p5enun"] = u"Folha cinco: ponha cada pedaço no seu quadradinho, na ordem."
F[u"p6enun"] = u"Folha seis: ligue cada figura ao número de palmas dela."
F[u"p7enun"] = u"Folha sete: ponha cada figura na gaveta certa. Uma, duas ou três palmas."
F[u"p8enun"] = (u"Folha oito: conte as letras e depois bata as palmas. "
                u"Você vai ver: não é o mesmo número!")
F[u"p9enun"] = u"Folha nove: bata palma e escreva o número de pedaços da palavra."
F[u"p10enun"] = u"Folha dez: toque nas palavras que você quer no seu mural."

# ---- os números (a voz do teclado e das opções) ------------------------------
for k in range(1, 7):
    F[u"num_%d" % k] = u"%d." % k

# ---- toda palavra que aparece no caderno --------------------------------------
usadas = set()
for chave, lista in IT.items():
    for x in lista:
        if isinstance(x, list):
            usadas.update(x)
        else:
            usadas.add(x)
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: bater palma em cada pedaço --------------------------------------
for w in IT[u"p1"]:
    n = len(sil(w))
    F[u"certo1_%s" % w] = (u"Muito bem! %s: %s. %s."
                           % (falado(w).capitalize(), empedacos(w), palmas(n).capitalize()))
    # ⚠️ pular NÃO é "errou": a voz diz qual é o próximo, sem a palavra errado
    F[u"volte1_%s" % w] = u"Espere! Comece pelo primeiro pedaço e vá seguindo."

# ---- folha 2: quantas palmas --------------------------------------------------
for w in IT[u"p2"]:
    n = len(sil(w))
    F[u"certo2_%s" % w] = (u"Isso! %s tem %s: %s."
                           % (falado(w).capitalize(), palmas(n), empedacos(w)))
    F[u"dica2_%s" % w] = (u"Escute e bata junto: %s. Quantas palmas você bateu?"
                          % empedacos(w))

# ---- folha 3: pintar os pedacinhos --------------------------------------------
for w in IT[u"p3"]:
    n = len(sil(w))
    F[u"certo3_%s" % w] = u"Muito bem! %s, %s pintadas." % (falado(w).capitalize(), palmas(n))
    F[u"dica3_%s" % w] = (u"Conte de novo batendo palma: %s. Pinte um pedacinho para "
                          u"cada palma." % empedacos(w))

# ---- folha 4: qual tem MAIS ---------------------------------------------------
for par in IT[u"p4"]:
    a, b = par
    maior = a if len(sil(a)) > len(sil(b)) else b
    menor = b if maior == a else a
    F[u"certo4_%s" % maior] = (u"Isso! %s tem %s e %s tem só %s."
                               % (falado(maior).capitalize(), palmas(len(sil(maior))),
                                  falado(menor), palmas(len(sil(menor)))))
    # ⭐ a dica ENSINA O TRUQUE: não é o desenho maior, é a palma
    F[u"dica4_%s" % maior] = (u"Não olhe o tamanho do desenho: bata palma nas duas. "
                              u"%s. E agora: %s."
                              % (empedacos(a), empedacos(b)))

# ---- folha 5: pôr os pedaços no lugar ------------------------------------------
for w in IT[u"p5"]:
    F[u"certo5_%s" % w] = u"Muito bem! %s: %s." % (falado(w).capitalize(), empedacos(w))
    F[u"dica5_%s" % w] = (u"Escute a palavra devagar: %s. Qual é o pedaço que vem agora?"
                          % empedacos(w))

# ---- folha 6: ligar ao número --------------------------------------------------
for g in IT[u"p6"]:
    for w in g:
        n = len(sil(w))
        F[u"certo6_%s" % w] = u"Isso! %s tem %s." % (falado(w).capitalize(), palmas(n))
        F[u"dica6_%s" % w] = (u"Bata palma junto: %s. Agora procure esse número."
                              % empedacos(w))

# ---- folha 7: as gavetas -------------------------------------------------------
for w in IT[u"p7"]:
    n = len(sil(w))
    F[u"certo7_%s" % w] = u"Boa! %s vai na gaveta de %s." % (falado(w).capitalize(), palmas(n))
    F[u"dica7_%s" % w] = (u"Escute: %s. Conte as palmas e procure a gaveta com esse "
                          u"número." % empedacos(w))

# ---- folha 8: letra não é sílaba -----------------------------------------------
for w in IT[u"p8"]:
    n, nl = len(sil(w)), len(esc(w))
    F[u"certo8_%s" % w] = (u"Muito bem! %s tem %d letras e só %s. Letra não é pedaço!"
                           % (falado(w).capitalize(), nl, palmas(n)))
    F[u"dica8_%s" % w] = (u"São duas contas diferentes. As letras você conta olhando; "
                          u"os pedaços você conta batendo palma: %s." % empedacos(w))

# ---- folha 9: escrever o número ------------------------------------------------
for w in IT[u"p9"]:
    n = len(sil(w))
    F[u"certo9_%s" % w] = u"Isso! %s: %s." % (falado(w).capitalize(), palmas(n))
    F[u"dica9_%s" % w] = (u"Fale a palavra devagar batendo palma: %s. Escreva quantas "
                          u"palmas deu." % empedacos(w))

# ---- folha 10: o mural ----------------------------------------------------------
for w in IT[u"p10"]:
    n = len(sil(w))
    F[u"certo10_%s" % w] = (u"%s, %s. Foi para o seu mural!"
                            % (falado(w).capitalize(), palmas(n)))

# ==============================================================================
#  O MAPA DAS SÍLABAS — quem recorta o quê de qual palavra
#  As folhas 1 e 5 falam sílaba por sílaba. Toda sílaba que o app pode falar
#  sozinha precisa de uma palavra de onde ser RECORTADA; entre as candidatas,
#  prefere aquela em que ela está na MESMA posição.
# ==============================================================================
PALAVRAS_SIL = {}
MAPA_SIL = {}
silabas = set()
for w in IT[u"p1"] + IT[u"p5"]:
    PALAVRAS_SIL[w] = sil(w)
    silabas.update(sil(w))
INTRUSOS = re.search(r"var INTRUSO = (\{[^}]*\});",
                     io.open(os.path.join(AQUI, u"folhas.js"), encoding=u"utf-8").read())
for s in json.loads(INTRUSOS.group(1)).values():
    silabas.add(s)

for s in sorted(silabas):
    achou = None
    for w in sorted(PALAVRAS_SIL) + sorted(set(PAL) - set(PALAVRAS_SIL)):
        ss = sil(w)
        if s in ss:
            achou = (w, ss.index(s))
            break
    if not achou:
        continue
    MAPA_SIL[s] = [achou[0], achou[1]]
    PALAVRAS_SIL[achou[0]] = sil(achou[0])

# ⚠️ a fala de RESERVA (quando o mp3 recortado não existir): o app cai para a
#    voz do navegador com este texto. É rede de segurança, não o caminho normal.
COMO_SE_FALA = {u"ÇÃ": u"sã", u"XÍ": u"chi", u"ÃO": u"ão", u"Ô": u"ô"}
for s in sorted(silabas):
    F[u"sb_%s" % s] = COMO_SE_FALA.get(s, s.lower()) + u"."


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
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ, u"palavras": PALAVRAS_SIL},
               ensure_ascii=False, indent=1))

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
blocoS = (u"/*SILMAP-INI*/var SILMAP = "
          + json.dumps(MAPA_SIL, ensure_ascii=False, sort_keys=True) + u";/*SILMAP-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/", lambda m: blocoS, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d palavra(s) com sílaba recortada"
      % (len(F), len(falas), len(PALAVRAS_SIL)))
