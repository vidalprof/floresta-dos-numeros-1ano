# -*- coding: utf-8 -*-
u"""
============================================================
 A TECLA DO ESPAÇO QUEBROU — gerador das falas (degrau 7)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ NESTE CADERNO A VOZ É O ANDAIME INTEIRO.
    O conteúdo é a FRASE — e ler a frase é justamente o que a criança de 1º ano
    ainda não faz sozinha. Sem a voz, ela só veria um paredão de letras e
    responderia pelo desenho. Toda frase do caderno é gravada, inclusive as
    DISTRATORAS da folha 7 (cada opção tem o seu alto-falante): se só a certa
    falasse, a criança aprenderia a escolher "a que fala", não a que lê.

 ⚠️ AS FRASES VÃO À VOZ EM MINÚSCULA E COM PONTO.
    A tela mostra CAIXA ALTA porque é assim que o 1º ano lê; o sintetizador lê
    melhor a minúscula, e o ponto final é o que lhe dá a entonação de frase
    terminada em vez de lista.

 Lê do próprio `index.html` os dois blocos que são a verdade do conteúdo:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `/*FRASES-INI*/ var FRASES = {...}` — o texto de cada frase.

 Uso:  python3 _fra1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"fr_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
FR = json.loads(re.search(r"/\*FRASES-INI\*/\s*var FRASES = (\{.*?\});\s*/\*FRASES-FIM\*/",
                          html, re.S).group(1))


def dita(c):
    u"""a frase como a voz a diz: minúscula e com ponto final"""
    return FR[c][0].lower() + u"."


def sem_ponto(c):
    u"""a frase dita SEM o ponto final — para quando a frase entra no meio de
    outra frase e o ponto viraria '..' (o revisor de texto pega isso)"""
    return dita(c)[:-1]


def quantas(c):
    n = len(FR[c][0].split(u" "))
    return u"uma palavra" if n == 1 else u"%d palavras" % n


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"A Tecla do Espaço Quebrou. A professora foi digitar e a tecla do "
              u"espaço parou de funcionar: as palavras saíram todas grudadas! "
              u"Dez folhas para você consertar. Escreva o seu nome ali embaixo e "
              u"toque em Começar.")
F[u"fim"] = (u"Você consertou tudo! Agora você sabe que é o espaço em branco que "
             u"separa uma palavra da outra. Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva a palavra que falta."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Escute a frase de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois na frase que fala dela."
F[u"novoCaderno"] = u"Caderno novo! As frases mudaram."

F[u"p1enun"] = (u"Folha um: a tecla do espaço quebrou! Toque na letra que começa "
                u"cada palavra nova.")
F[u"p2enun"] = u"Folha dois: agora são quatro palavras grudadas. Ache todos os começos!"
F[u"p3enun"] = u"Folha três: cinco palavras. Escute a frase antes de cortar."
F[u"p4enun"] = (u"Folha quatro: pinte uma bolinha para cada palavra da frase. "
                u"Depois toque em Pronto.")
F[u"p5enun"] = u"Folha cinco: as palavras saíram fora de ordem. Monte a frase."
F[u"p6enun"] = (u"Folha seis: agora uma palavra sobra! Monte a frase e deixe a "
                u"intrusa de fora.")
F[u"p7enun"] = (u"Folha sete: olhe a figura e escolha a frase certa. Elas são "
                u"parecidas!")
F[u"p8enun"] = u"Folha oito: ligue cada figura à frase que fala dela."
F[u"p9enun"] = u"Folha nove: escute a frase e escreva a palavra que falta."
F[u"p10enun"] = u"Folha dez: toque nas frases que você consertou e quer no seu mural."

# ---- TODA frase do caderno, inclusive as distratoras ---------------------------
for c in sorted(FR):
    F[u"fr_%s" % c] = dita(c)

# ---- folhas 1, 2 e 3: cortar a frase --------------------------------------------
for tag, n in ((u"p1", 1), (u"p2", 2), (u"p3", 3)):
    for c in IT[tag]:
        ps = FR[c][0].split(u" ")
        F[u"certo%d_%s" % (n, c)] = (u"Consertado! %s. São %s, e agora dá para ler."
                                     % (sem_ponto(c).capitalize(), quantas(c)))
        # ⚠️ errar aqui NÃO é "errou": a voz diz o que escutar, sem a palavra errado
        F[u"dica%d_%s" % (n, c)] = (u"Escute a frase devagar: %s. Agora pense: onde "
                                    u"COMEÇA a próxima palavra?" % sem_ponto(c))

# ---- folha 4: quantas palavras ---------------------------------------------------
for c in IT[u"p4"]:
    ps = FR[c][0].split(u" ")
    lista = u", ".join(p.lower() for p in ps)
    F[u"certo4_%s" % c] = (u"Isso! %s tem %s: %s."
                           % (sem_ponto(c).capitalize(), quantas(c), lista))
    # ⭐ a dica ENSINA A ARMADILHA: o "o" e o "a" também são palavras
    F[u"dica4_%s" % c] = (u"Conte uma por uma, apontando: %s. Cuidado: o \"o\" e o "
                          u"\"a\" também são palavras!" % lista)

# ---- folhas 5 e 6: pôr as palavras na ordem ---------------------------------------
for c in IT[u"p5"]:
    F[u"certo5_%s" % c] = u"Muito bem! %s" % dita(c).capitalize()
    F[u"dica5_%s" % c] = (u"Escute a frase inteira: %s. Qual é a palavra que vem "
                          u"agora?" % sem_ponto(c))
for reg in IT[u"p6"]:
    c, extra = reg[0], reg[1]
    F[u"certo6_%s" % c] = (u"Muito bem! %s E a palavra %s não era desta frase."
                           % (dita(c).capitalize(), extra.lower()))
    F[u"dica6_%s" % c] = (u"Uma das palavras do banco não é desta frase. Escute de "
                          u"novo: %s" % dita(c))

# ---- folha 7: qual é a frase da figura ---------------------------------------------
for reg in IT[u"p7"]:
    c = reg[0]
    F[u"certo7_%s" % c] = (u"Isso! A figura mostra exatamente isto: %s" % dita(c))
    F[u"dica7_%s" % c] = (u"As três frases são quase iguais e mudam uma palavra só. "
                          u"Aperte o alto-falante de cada uma e olhe bem a figura.")

# ---- folha 8: ligar a figura à frase ------------------------------------------------
for g in IT[u"p8"]:
    for c in g:
        F[u"certo8_%s" % c] = u"Isso! %s" % dita(c).capitalize()
        F[u"dica8_%s" % c] = (u"Escute as frases uma por uma e procure a que fala "
                              u"desta figura.")

# ---- folha 9: escrever a palavra que falta --------------------------------------------
for reg in IT[u"p9"]:
    c, onde = reg[0], reg[1]
    pal = FR[c][0].split(u" ")[onde]
    F[u"certo9_%s" % c] = (u"Muito bem! %s A palavra que faltava era %s."
                           % (dita(c).capitalize(), pal.lower()))
    F[u"dica9_%s" % c] = (u"Escute a frase com o buraco e depois inteira: %s. "
                          u"Escreva só a palavra que está faltando." % sem_ponto(c))

# ---- folha 10: o mural ------------------------------------------------------------------
for c in IT[u"p10"]:
    F[u"certo10_%s" % c] = u"%s Foi para o seu mural!" % dita(c).capitalize()


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
# ⚠️ VAZIO DE PROPÓSITO: este caderno não recorta sílaba nenhuma — o conteúdo é
#    a FRASE, e a voz diz frase inteira
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

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d frase(s) gravadas"
      % (len(F), len(falas), len(FR)))
