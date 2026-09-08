# -*- coding: utf-8 -*-
u"""
============================================================
 A FÁBRICA DE PALAVRAS — gerador das falas

 Enumera TODAS as frases que a atividade pode dizer, para que nenhuma fique sem
 mp3. Lê do próprio `index.html` os dois blocos que são a verdade do conteúdo:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `var PAL = { bola:["BOLA",["BO","LA"]], ... }` — a escrita e as SÍLABAS.

 ⚠️ As sílabas são LIDAS dali, nunca recalculadas aqui. Separar sílaba por regra
 erra em português (na-vi-o, a-be-lha, li-mão) — e sílaba errada numa folha de
 alfabetização não é defeito de tela: ensina errado.

 Escreve:
   · o bloco /*FALAS-INI*/ dentro do index.html
   · o bloco /*VOZOK-INI*/ (o mapa de quais falas têm mp3)
   · falas.json (o que o entregar.yml grava) e voz.txt

 Uso:  python3 _alfa1/gerar_falas.py
============================================================
"""
import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"al_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()

# ---- o que cada folha sorteia -------------------------------------------------
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS\s*=\s*(\{.*?\})\s*;\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))

# ---- a escrita e as sílabas de cada palavra ----------------------------------
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
for m in re.finditer(r'(\w+)\s*:\s*\[\s*"([^"]+)"\s*,\s*\[([^\]]*)\]\s*\]', bloco):
    PAL[m.group(1)] = (m.group(2), [s.strip().strip(u'"') for s in m.group(3).split(u",")])

def esc(w):
    return PAL[w][0] if w in PAL else w.upper()

def sil(w):
    return PAL[w][1] if w in PAL else [w.upper()]

def falado(w):
    u"""a palavra como se FALA (a voz lê a minúscula melhor que a caixa alta)"""
    return esc(w).lower()

def emsilabas(w):
    u"""'ba... na... na' — as reticências fazem a voz separar de verdade"""
    return u"... ".join(s.lower() for s in sil(w))

F = {}

# ---- as fixas ----------------------------------------------------------------
F.update({
 u"capa": u"A Fábrica de Palavras. Dez folhas para brincar com as letras e as sílabas. Escreva o seu nome ali embaixo e toque em Começar.",
 u"p1enum": u"",  # (reservado)
 u"p1enun": u"Folha um: a letra escondida. Uma letra fugiu da palavra. Olhe a figura, ouça a palavra e toque na letra certa.",
 u"p2enun": u"Folha dois: quantas sílabas. Fale a palavra batendo uma palma em cada pedaço. Depois toque em Pronto.",
 u"p3enun": u"Folha três: o que vem depois. Olhe a fila de figuras, descubra a ordem que se repete e escolha a que vem depois.",
 u"p4enun": u"Folha quatro: circule quem começa igual. Toque em todos os desenhos que começam com a sílaba mostrada. Depois toque em Conferir.",
 u"p5enun": u"Folha cinco: pinte a sílaba inicial. Toque na sílaba com que a palavra começa.",
 u"p6enun": u"Folha seis: ligue à sílaba final. Toque na figura e depois na sílaba com que ela termina.",
 u"p7enun": u"Folha sete: marque a sílaba do meio. Toque na sílaba que fica no meio da palavra.",
 u"p8enun": u"Folha oito: escreva a sílaba que falta. Toque no quadradinho e escreva a sílaba, no teclado da tela ou no teclado de verdade.",
 u"p9enun": u"Folha nove: ordene e forme a palavra. As sílabas embaralharam. Toque nelas na ordem certa.",
 u"p10enun": u"Folha dez: recorte e cole. Puxe cada sílaba para debaixo da figura certa, ou toque na sílaba e depois na figura.",
 u"quase": u"Quase! Escute de novo e tente outra vez.",
 u"ligue": u"Toque primeiro na figura e depois na sílaba.",
 u"escreva": u"Escreva a sílaba que falta.",
 u"folhaPronta": u"Folha pronta! Muito bem.",
 u"fim": u"Você terminou o caderno inteiro! Olhe quanta palavra você montou hoje.",
 u"novoCaderno": u"Caderno novo, com palavras novas. Vamos de novo!",
 u"vozOn": u"Narração ligada!",
 u"dica3": u"Olhe a fila com calma: as figuras se repetem sempre na mesma ordem. Qual delas vem agora?",
})
del F[u"p1enum"]

# ---- as letras ---------------------------------------------------------------
for L in u"ABCDEFGHIJLMNOPQRSTUVXZ":
    F[u"letra_%s" % L] = u"A letra %s." % L

# ---- as palavras e as sílabas usadas -----------------------------------------
usadas, silabas = set(), set()

def usa(w):
    usadas.add(w)
    for s in sil(w):
        silabas.add(s)

for it in IT[u"p1"]:
    usa(it[u"p"])
for w in IT[u"p2"]:
    usa(w)
for it in IT[u"p3"]:
    usa(it[u"a"]); usa(it[u"b"])
for it in IT[u"p4"]:
    for w in it[u"sim"] + it[u"nao"]:
        usa(w)
for it in IT[u"p5"]:
    usa(it[u"p"])
    for s in it[u"op"]:
        silabas.add(s)
for g in IT[u"p6"]:
    for w in g:
        usa(w)
for it in IT[u"p7"]:
    usa(it[u"p"])
    for s in it[u"op"]:
        silabas.add(s)
for it in IT[u"p8"]:
    usa(it[u"p"])
for w in IT[u"p9"]:
    usa(w)
for g in IT[u"p10"]:
    for w in g:
        usa(w)
# a folha 3 sorteia distratores desta lista fixa (ver f3 no folhas.js)
for w in [u"casa", u"mala", u"gato", u"roda", u"vaca", u"copo", u"sino", u"faca"]:
    usa(w)

for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."
    F[u"sil_%s" % w] = u"%s. %s." % (emsilabas(w), falado(w))
for s in sorted(silabas):
    F[u"sb_%s" % s] = s.lower() + u"."

# ---- folha 1: a letra escondida ----------------------------------------------
for it in IT[u"p1"]:
    w = it[u"p"]
    L = esc(w)[it[u"pos"]]
    onde = u"começa" if it[u"pos"] == 0 else u"termina"
    F[u"certo1_%s" % w] = u"Isso! %s %s com a letra %s." % (falado(w).capitalize(), onde, L)
    F[u"dica1_%s" % w] = u"Fale a palavra bem devagar: %s. Qual é o som com que ela %s?" % (emsilabas(w), onde)

# ---- folha 2: quantas sílabas -------------------------------------------------
NUM = {1: u"uma", 2: u"duas", 3: u"três", 4: u"quatro"}
for w in IT[u"p2"]:
    n = len(sil(w))
    F[u"certo2_%s" % w] = u"Isso! %s tem %s %s: %s." % (
        falado(w).capitalize(), NUM.get(n, unicode(n) if str is bytes else str(n)),
        u"pedaço" if n == 1 else u"pedaços", emsilabas(w))
    F[u"dica2_%s" % w] = u"Escute e bata junto: %s. Quantas palmas você bateu?" % emsilabas(w)

# ---- folha 3: o que vem depois ------------------------------------------------
for it in IT[u"p3"]:
    F[u"certo3_%s_%s" % (it[u"a"], it[u"b"])] = u"Isso! A fila é %s, %s, %s, %s, e agora %s de novo." % (
        falado(it[u"a"]), falado(it[u"b"]), falado(it[u"a"]), falado(it[u"b"]), falado(it[u"a"]))

# ---- folha 4: circule quem começa igual ---------------------------------------
for it in IT[u"p4"]:
    s = it[u"sil"]
    nomes = u", ".join(falado(w) for w in it[u"sim"])
    F[u"certo4_%s" % s] = u"Isso! %s começam com %s." % (nomes.capitalize(), s.lower())
    F[u"dica4_%s" % s] = u"Fale cada palavra devagar e escute só o começo. Qual delas começa com %s?" % s.lower()

# ---- folha 5: pinte a sílaba inicial ------------------------------------------
for it in IT[u"p5"]:
    w = it[u"p"]; s = sil(w)
    F[u"certo5_%s" % w] = u"Isso! %s começa com %s." % (falado(w).capitalize(), s[0].lower())
    F[u"dica5_%s" % w] = u"Escute o começo: %s. O primeiro pedaço é %s." % (emsilabas(w), s[0].lower())

# ---- folha 6: ligue à sílaba final --------------------------------------------
for g in IT[u"p6"]:
    for w in g:
        s = sil(w)
        F[u"certo6_%s" % w] = u"Isso! %s termina com %s." % (falado(w).capitalize(), s[-1].lower())
        F[u"dica6_%s" % w] = u"Escute o fim da palavra: %s. O último pedaço é %s." % (emsilabas(w), s[-1].lower())

# ---- folha 7: a sílaba do meio ------------------------------------------------
for it in IT[u"p7"]:
    w = it[u"p"]; s = sil(w)
    F[u"certo7_%s" % w] = u"Isso! No meio de %s fica %s." % (falado(w), s[1].lower())
    F[u"dica7_%s" % w] = u"São três pedaços: %s. O do meio é o segundo." % emsilabas(w)

# ---- folha 8: escreva a sílaba que falta -------------------------------------
for it in IT[u"p8"]:
    w = it[u"p"]; s = sil(w); k = it[u"falta"]
    F[u"certo8_%s" % w] = u"Isso! A palavra é %s: %s." % (falado(w), emsilabas(w))
    F[u"dica8_%s" % w] = u"Fale a palavra inteira e escute o pedaço que falta: %s. O que falta é %s." % (
        emsilabas(w), s[k].lower())

# ---- folha 9: ordene e forme a palavra ----------------------------------------
for w in IT[u"p9"]:
    F[u"certo9_%s" % w] = u"Isso! %s: %s." % (falado(w).capitalize(), emsilabas(w))
    F[u"dica9_%s" % w] = u"Comece pelo primeiro pedaço. A palavra é %s." % emsilabas(w)

# ---- folha 10: recorte e cole -------------------------------------------------
for g in IT[u"p10"]:
    for w in g:
        F[u"certo10_%s" % w] = u"Isso! %s começa com %s." % (falado(w).capitalize(), sil(w)[0].lower())
        F[u"dica10_%s" % w] = u"Olhe a figura e fale o nome dela: %s. Com que pedaço ela começa?" % emsilabas(w)


# ---- a chave da casa (igual à do JS) ------------------------------------------
def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        r = d % 36
        out = (u"0123456789abcdefghijklmnopqrstuvwxyz"[r]) + out
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

blocoF = u"/*FALAS-INI*/\nvar FALAS = " + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/"
blocoV = u"/*VOZOK-INI*/var VOZOK = " + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/"
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); VOZOK gravado" % (len(F), len(falas)))
