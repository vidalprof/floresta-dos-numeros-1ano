# -*- coding: utf-8 -*-
u"""
============================================================
 O GRANDE JOGO DAS PALAVRAS — gerador das falas (degrau 8)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ ESTE É O CADERNO DE REVISÃO, e a voz dele tem um trabalho a mais: em cada
    acerto ela LEMBRA de qual degrau aquilo veio ("as duas acabam igual — isso é
    rima!", "o começo das duas é o mesmo pedaço"). Revisão que não diz o nome do
    que está revisando vira só mais uma rodada de exercícios.

 ⚠️ A FORCA NÃO ENFORCA NINGUÉM: quando o balão pousa, a palavra se revela e a
    voz diz o nome dela sem nenhuma palavra de derrota. A criança perde a rodada,
    não um boneco — e a folha continua.

 Lê do próprio `index.html`:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `/*FRASES-INI*/ var FRASES = {...}` — as frases das folhas 7 e 8;
   · `var PAL = {...}` — a escrita e as sílabas das palavras.

 Uso:  python3 _jogo1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"jg_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
FR = json.loads(re.search(r"/\*FRASES-INI\*/\s*var FRASES = (\{.*?\});\s*/\*FRASES-FIM\*/",
                          html, re.S).group(1))
PAL = {}
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\]',
                     re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])

DIZ = {u"maca": u"maçã", u"balao": u"balão", u"leao": u"leão", u"limao": u"limão",
       u"onibus": u"ônibus", u"xicara": u"xícara", u"jacare": u"jacaré",
       u"chapeu": u"chapéu", u"pao": u"pão", u"navio": u"navio"}


def esc(w):
    return PAL[w][0]


def sil(w):
    return PAL[w][1]


def falado(w):
    return DIZ.get(w, esc(w).lower())


def empedacos(w):
    return u"... ".join(x.lower() for x in sil(w))


def soletrado(w):
    return u", ".join(esc(w))


def palmas(n):
    return u"uma palma" if n == 1 else u"%d palmas" % n


def dita(c):
    return FR[c][0].lower() + u"."


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"O Grande Jogo das Palavras. Você já subiu oito degraus: rima, "
              u"pedaços, começo, som, sílaba, letra e frase. Agora é hora de jogar "
              u"com tudo o que aprendeu! Escreva o seu nome ali embaixo e toque em "
              u"Começar.")
F[u"fim"] = (u"Você chegou ao fim da sequência inteira! Rima, pedaços, letras e "
             u"frases: tudo isso já é seu. Olhe o seu mural de campeão ali embaixo.")
F[u"escreva"] = u"Escreva o nome da figura."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Olhe de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois na frase que fala dela."
F[u"novoCaderno"] = u"Jogo novo! As palavras mudaram."

F[u"p1enun"] = (u"Folha um: memória das rimas. Vire duas cartas e ache as palavras "
                u"que rimam. Elas acabam igual!")
F[u"p2enun"] = u"Folha dois: fale a palavra batendo palma. Quantas palmas você bateu?"
F[u"p3enun"] = u"Folha três: qual delas começa igual à figura de cima?"
F[u"p4enun"] = (u"Folha quatro: o caça-palavras. Ache as palavras na grade. Toque na "
                u"primeira e na última letra de cada uma.")
F[u"p5enun"] = (u"Folha cinco: a forca do balão. Olhe a figura e adivinhe as letras. "
                u"O balão desce a cada erro!")
F[u"p6enun"] = u"Folha seis: as letras saíram fora de ordem. Monte o nome da figura."
F[u"p7enun"] = (u"Folha sete: a tecla do espaço quebrou de novo! Toque na letra que "
                u"começa cada palavra.")
F[u"p8enun"] = u"Folha oito: ligue cada figura à frase que fala dela."
F[u"p9enun"] = (u"Folha nove: olhe a figura, escute e escreva o nome dela inteiro. "
                u"Sem nenhuma letra dada!")
F[u"p10enun"] = u"Folha dez: toque nas palavras que você quer no seu mural de campeão."

# ---- os números do bate-palma ---------------------------------------------------
for k in range(1, 7):
    F[u"num_%d" % k] = u"%d." % k

# ---- toda palavra e toda frase que aparecem ------------------------------------
usadas = set()
for tag in (u"p2", u"p5", u"p6", u"p9", u"p10"):
    usadas.update(IT[tag])
for tab in IT[u"p1"]:
    for par in tab:
        usadas.update(par)
for reg in IT[u"p3"]:
    usadas.update(reg)
for grade, grupo, onde in IT[u"p4"]:
    usadas.update(grupo)
for c in IT[u"p7"]:
    usadas.update(FR[c][1])
for g in IT[u"p8"]:
    for c in g:
        usadas.update(FR[c][1])
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."
frases = set(IT[u"p7"])
for g in IT[u"p8"]:
    frases.update(g)
for c in sorted(frases):
    # ⚠️ `frase_`, NÃO `fr_` (set/2026). A chave de fala do degrau 7 chamava-se
    #    `fr_<frase>` — e `fr_` é exatamente o PREFIXO DE PASTA do `_fra1`. Ao
    #    clonar para cá, o portão `_qa/clone.py` leu `fr_f_abelha` como "asset da
    #    atividade de origem vazando" e reprovou. Chave de fala nunca deve ter a
    #    forma de um prefixo de pasta (duas ou três letras e um traço baixo).
    F[u"frase_%s" % c] = dita(c)

# ---- folha 1: memória das rimas -------------------------------------------------
# ⚠️ a fala é a da carta que ela virou PRIMEIRO — e pode ser qualquer uma das
#    duas. Por isso as duas palavras do par ganham o mesmo par de falas.
for tab in IT[u"p1"]:
    for par in tab:
        a, b = par
        for w, outra in ((a, b), (b, a)):
            F[u"certo1_%s" % w] = (u"Par! %s e %s acabam igual: %s. Isso é RIMA."
                                   % (falado(w).capitalize(), falado(outra),
                                      sil(w)[-1].lower()))
            F[u"dica1_%s" % w] = (u"Estas duas não acabam igual. Fale as duas em voz "
                                  u"alta e escute o FIM de cada uma.")

# ---- folha 2: quantas palmas ----------------------------------------------------
for w in IT[u"p2"]:
    n = len(sil(w))
    F[u"certo2_%s" % w] = (u"Isso! %s tem %s: %s."
                           % (falado(w).capitalize(), palmas(n), empedacos(w)))
    F[u"dica2_%s" % w] = (u"Escute e bata junto: %s. Quantas palmas você bateu?"
                          % empedacos(w))

# ---- folha 3: quem começa igual -------------------------------------------------
for reg in IT[u"p3"]:
    alvo, certa = reg[0], reg[1]
    F[u"certo3_%s" % certa] = (u"Isso! %s e %s começam com o mesmo pedaço: %s."
                               % (falado(alvo).capitalize(), falado(certa),
                                  sil(alvo)[0].lower()))
    F[u"dica3_%s" % certa] = (u"Fale a figura de cima devagar: %s. Agora fale cada "
                              u"uma das três e escute o COMEÇO." % empedacos(alvo))

# ---- folha 4: o caça-palavras ----------------------------------------------------
for grade, grupo, onde in IT[u"p4"]:
    for w in grupo:
        F[u"certo4_%s" % w] = (u"Achou! %s: %s."
                               % (falado(w).capitalize(), soletrado(w)))
        F[u"dica4_%s" % w] = (u"Procure a primeira letra de %s na grade. As palavras "
                              u"estão deitadas ou em pé, nunca de lado nem de trás "
                              u"para frente." % falado(w))

# ---- folha 5: a forca do balão ----------------------------------------------------
for w in IT[u"p5"]:
    F[u"certo5_%s" % w] = (u"Você descobriu! %s: %s."
                           % (falado(w).capitalize(), soletrado(w)))
    F[u"dica5_%s" % w] = (u"Esta letra não está na palavra. Olhe bem a figura e pense "
                          u"em qual letra tentar agora.")
    # ⚠️ pousar não é derrota: a palavra se revela e a folha segue
    F[u"pousou_%s" % w] = (u"O balão pousou! A palavra era %s: %s. Na próxima você "
                           u"pega." % (falado(w), soletrado(w)))

# ---- folha 6: montar a palavra ------------------------------------------------------
for w in IT[u"p6"]:
    F[u"certo6_%s" % w] = u"Isso! %s: %s." % (falado(w).capitalize(), soletrado(w))
    F[u"dica6_%s" % w] = (u"Fale o nome da figura devagar: %s. Qual é a letra que vem "
                          u"agora?" % falado(w))

# ---- folhas 7 e 8: a frase -----------------------------------------------------------
for c in IT[u"p7"]:
    F[u"certo7_%s" % c] = (u"Consertado! %s São %d palavras."
                           % (dita(c).capitalize(), len(FR[c][0].split(u" "))))
    F[u"dica7_%s" % c] = (u"Escute a frase devagar: %s Agora pense: onde COMEÇA a "
                          u"próxima palavra?" % dita(c))
for g in IT[u"p8"]:
    for c in g:
        F[u"certo8_%s" % c] = u"Isso! %s" % dita(c).capitalize()
        F[u"dica8_%s" % c] = (u"Escute as frases uma por uma e procure a que fala "
                              u"desta figura.")

# ---- folha 9: escrever o nome inteiro --------------------------------------------------
for w in IT[u"p9"]:
    F[u"certo9_%s" % w] = (u"Muito bem! Você escreveu %s sozinha: %s."
                           % (falado(w), soletrado(w)))
    F[u"dica9_%s" % w] = (u"Olhe a figura: é %s. Fale devagar, %s, e escreva as letras "
                          u"na ordem." % (falado(w), empedacos(w)))

# ---- folha 10: o mural do campeão ---------------------------------------------------------
for w in IT[u"p10"]:
    F[u"certo10_%s" % w] = (u"%s: %s. Foi para o seu mural de campeão!"
                            % (falado(w).capitalize(), empedacos(w)))


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
# ⚠️ VAZIO DE PROPÓSITO: este caderno não recorta sílaba nenhuma
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

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d palavra(s) e %d frase(s)"
      % (len(F), len(falas), len(usadas), len(frases)))
