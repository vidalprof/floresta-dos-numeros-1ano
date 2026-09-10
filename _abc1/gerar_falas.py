# -*- coding: utf-8 -*-
u"""GERA AS FALAS DO DESFILE DAS LETRAS (degrau 0 da sequência).

⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

⚠️ E AQUI A VOZ É O CONTEÚDO, não apoio. O objetivo do currículo é *"NOMEAR as
   letras do alfabeto e ordená-las"* — nomear é dizer o nome. Uma folha de
   alfabeto sem voz ensina a reconhecer o desenho da letra e não o nome dela.
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"ab_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
A = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ⚠️⚠️ O NOME DE CADA LETRA, ESCRITO COMO SE FALA — e este é o coração do arquivo.
#    O Edge TTS lendo a letra "B" sozinha diz "bê"? Nem sempre: ele hesita entre
#    soletrar e ler como palavra, e em algumas ele erra feio ("H" vira "agá" com
#    som de "rá", "X" vira "xis" ou "chis" conforme o contexto). Numa atividade
#    cujo OBJETIVO é nomear a letra, uma letra mal dita ensina errado.
#    Por isso o nome vai ESCRITO por extenso, conferido um a um.
NOME_LETRA = {
    u"A": u"á", u"B": u"bê", u"C": u"cê", u"D": u"dê", u"E": u"é", u"F": u"éfe",
    u"G": u"gê", u"H": u"agá", u"I": u"i", u"J": u"jota", u"K": u"cá",
    u"L": u"éle", u"M": u"ême", u"N": u"êne", u"O": u"ó", u"P": u"pê",
    u"Q": u"quê", u"R": u"érre", u"S": u"ésse", u"T": u"tê", u"U": u"u",
    u"V": u"vê", u"W": u"dábliu", u"X": u"xis", u"Y": u"ípsilon", u"Z": u"zê",
}
DIZ = {u"hipopotamo": u"hipopótamo", u"leao": u"leão", u"xicara": u"xícara",
       u"maca": u"maçã", u"abelha": u"abelha"}


def diz(w):
    return DIZ.get(w, w)


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"O Desfile das Letras. Dez folhas para conhecer o alfabeto e a "
              u"ordem das letras. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim do Desfile das Letras! Agora você conhece a fila "
             u"do alfabeto. Olhe o seu alfabeto ali embaixo.")
F[u"escreva"] = u"Escreva a letra."
F[u"vozOn"] = u"Narração ligada!"

F[u"p1enun"] = u"Toque nas letras na ordem, do começo ao fim. Ouça o nome de cada uma."
F[u"p2enun"] = u"Ouça o nome da letra e toque nela."
F[u"p3enun"] = u"Uma letra fugiu da fila. Qual é?"
F[u"p4enun"] = u"Qual letra vem depois desta?"
F[u"p5enun"] = u"Qual letra vem antes desta?"
F[u"p6enun"] = u"Preencha os dois lados: quem vem antes e quem vem depois."
F[u"p7enun"] = u"Estas letras embaralharam. Toque nelas na ordem certa do alfabeto."
F[u"p8enun"] = u"Uma letra entrou no lugar errado. Circule quem saiu da fila."
F[u"p9enun"] = u"Com que letra começa o nome da figura?"
F[u"p10enun"] = (u"Toque nas letras que você quer no seu alfabeto. "
                 u"Ele fica guardado no fim.")

# ---- o nome de TODA letra do alfabeto ----------------------------------------
for L in A:
    F[u"let_%s" % L] = NOME_LETRA[L] + u"."

# ---- folha 1: o desfile ------------------------------------------------------
for it in IT[u"p1"]:
    k = it[u"i"]
    seq = [A[j] for j in range(k, min(k + 5, 26))]
    F[u"certo1_%s" % seq[0]] = (u"Muito bem! %s. Essa é a ordem certa."
                                % u", ".join(NOME_LETRA[x] for x in seq))
    F[u"dica1_%s" % seq[0]] = u"Comece pela primeira e vá seguindo a fila, uma de cada vez."
for L in A:
    # ⚠️ pular NÃO é "errou": a voz diz qual é a próxima, sem a palavra errado
    F[u"volte_%s" % L] = u"Espere! A próxima da fila é o %s." % NOME_LETRA[L]

# ---- folha 2: nomear ---------------------------------------------------------
for it in IT[u"p2"]:
    L = it[u"L"]
    F[u"certo2_%s" % L] = u"Isso! Esta é a letra %s." % NOME_LETRA[L]
    F[u"dica2_%s" % L] = (u"Toque no alto-falante e escute de novo: %s. "
                          u"Qual delas é?" % NOME_LETRA[L])

# ---- folha 3: a letra que fugiu ----------------------------------------------
for it in IT[u"p3"]:
    k = it[u"i"]; L = A[k]
    ant = A[k - 1] if k > 0 else None
    F[u"certo3_%s" % L] = (u"Muito bem! Depois do %s vem o %s."
                           % (NOME_LETRA[ant], NOME_LETRA[L]) if ant
                           else u"Muito bem! O %s abre o alfabeto." % NOME_LETRA[L])
    F[u"dica3_%s" % L] = (u"Fale as letras da fila em voz alta e continue: "
                          u"qual vem depois do %s?" % NOME_LETRA[ant] if ant
                          else u"Esta é a primeira letra de todas.")

# ---- folhas 4 e 5: depois e antes --------------------------------------------
for it in IT[u"p4"]:
    L, c = it[u"L"], it[u"c"]
    F[u"certo4_%s" % L] = u"Isso! Depois do %s vem o %s." % (NOME_LETRA[L], NOME_LETRA[c])
    F[u"dica4_%s" % L] = (u"Comece a falar o alfabeto e pare no %s. "
                          u"Qual vem logo em seguida?" % NOME_LETRA[L])
for it in IT[u"p5"]:
    L, c = it[u"L"], it[u"c"]
    F[u"certo5_%s" % L] = u"Muito bem! Antes do %s vem o %s." % (NOME_LETRA[L], NOME_LETRA[c])
    # ⭐ a dica ENSINA O TRUQUE, que é o que falta a quem só recita para frente
    F[u"dica5_%s" % L] = (u"Fale o alfabeto desde o começo e vá com atenção: a letra "
                          u"que você diz logo ANTES do %s é a resposta." % NOME_LETRA[L])

# ---- folha 6: os dois lados --------------------------------------------------
for it in IT[u"p6"]:
    L = it[u"L"]; k = A.index(L)
    F[u"certo6_%s" % L] = (u"Isso! %s, %s, %s."
                           % (NOME_LETRA[A[k - 1]], NOME_LETRA[L], NOME_LETRA[A[k + 1]]))
    F[u"dica6_%s" % L] = (u"Uma das duas vagas ainda não é essa. Fale o alfabeto até o %s "
                          u"e escute quem está de cada lado." % NOME_LETRA[L])

# ---- folha 7: ordenar --------------------------------------------------------
for it in IT[u"p7"]:
    g = sorted(it[u"g"])
    F[u"certo7_%s" % g[0]] = u"Muito bem! %s." % u", ".join(NOME_LETRA[x] for x in g)
    F[u"dica7_%s" % g[0]] = (u"Qual destas vem primeiro no alfabeto? Comece por ela e "
                             u"vá seguindo a fila.")

# ---- folha 8: o intruso ------------------------------------------------------
for it in IT[u"p8"]:
    c = it[u"c"]
    ordem = [x for x in it[u"g"] if x != c]
    F[u"certo8_%s" % c] = (u"Isso! O %s não é dessa parte da fila. Sem ele fica %s."
                           % (NOME_LETRA[c], u", ".join(NOME_LETRA[x] for x in ordem)))
    F[u"dica8_%s" % c] = (u"Fale as quatro em voz alta na ordem do alfabeto. "
                          u"Uma delas não encaixa — qual atrapalha a fila?")

# ---- folha 9: a letra que abre a palavra -------------------------------------
for it in IT[u"p9"]:
    w, c = it[u"w"], it[u"c"]
    F[u"pal_%s" % w] = diz(w) + u"."
    F[u"certo9_%s" % w] = (u"Muito bem! %s começa com %s."
                           % (diz(w).capitalize(), NOME_LETRA[c]))
    F[u"dica9_%s" % w] = (u"Fale o nome da figura devagar: %s. Escute só o "
                          u"comecinho." % diz(w))

# ---- folha 10: o mural -------------------------------------------------------
for it in IT[u"p10"]:
    L, w = it[u"L"], it[u"w"]
    F[u"pal_%s" % w] = diz(w) + u"."
    F[u"certo10_%s" % L] = (u"%s de %s foi para o seu alfabeto!"
                            % (NOME_LETRA[L].capitalize(), diz(w)))


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

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/",
              lambda m: u"/*SILMAP-INI*/var SILMAP = {};/*SILMAP-FIM*/", novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); VOZOK gravado" % (len(F), len(falas)))
