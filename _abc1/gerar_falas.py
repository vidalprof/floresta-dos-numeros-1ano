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
# ⚠️ COMO A VOZ DIZ CADA PALAVRA. O pote guarda o nome SEM acento (é chave de
#    arquivo); a voz precisa do acento, senão o Edge TTS lê "leao" como "lê-ão"
#    e "xicara" como "xicára". Palavra nova no pote = linha nova aqui.
DIZ = {u"hipopotamo": u"hipopótamo", u"leao": u"leão", u"xicara": u"xícara",
       u"maca": u"maçã", u"abelha": u"abelha",
       # as palavras que entraram com as folhas 18, 19 e 21
       u"abacaxi": u"abacaxi", u"girafa": u"girafa", u"moeda": u"moeda",
       u"telha": u"telha", u"tijolo": u"tijolo", u"ninho": u"ninho",
       # os nomes de criança da folha 23 (a chamada da turma)
       u"joao": u"João", u"heloisa": u"Heloísa", u"zeze": u"Zezé",
       u"kaua": u"Kauã", u"olivia": u"Olívia", u"vitor": u"Vítor",
       u"yasmin": u"Iasmin", u"emily": u"Emili", u"noah": u"Noá",
       u"gabi": u"Gabi", u"rafa": u"Rafa", u"nina": u"Nina"}


def diz(w):
    return DIZ.get(w, w)


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"O Desfile das Letras. Vinte e cinco folhas para conhecer o alfabeto "
              u"e a ordem das letras. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim do Desfile das Letras! Agora você conhece a fila "
             u"do alfabeto. Olhe o seu alfabeto ali embaixo.")
F[u"escreva"] = u"Escreva a letra."
F[u"vozOn"] = u"Narração ligada!"

# ⚠️ ESTA FALA FALTAVA E O APP A PEDIA — medido em 21/set/2026, depois de o
#    Marcos trazer da sala *"as palavras estão sendo ditas erradas"*. O
#    `falar()` volta CALADO quando a chave não existe: era silêncio no lugar
#    exato em que a criança espera ser elogiada.
F[u"folhaPronta"] = u"Folha pronta! Muito bem."

# ---- os enunciados das 25 folhas ---------------------------------------------
# ⚠️ O texto aqui tem que dizer O MESMO que o `enunciado(...)` da folha em
#    `folhas.js`. Se a tela disser uma coisa e a voz outra, a criança que não lê
#    obedece a voz e erra por causa da nossa desatenção.
F[u"p1enun"]  = u"Toque nas letras na ordem, do começo ao fim. Ouça o nome de cada uma."
F[u"p2enun"]  = u"Ouça o poema. Depois ache na fila a letra que a voz pedir."
F[u"p3enun"]  = u"Ouça o nome da letra e toque nela."
F[u"p4enun"]  = u"Uma letra fugiu da fila. Qual é?"
F[u"p5enun"]  = u"Agora a fila está em letra pequena. Qual letrinha fugiu?"
F[u"p6enun"]  = u"Ligue cada letra grande à mesma letra pequena."
F[u"p7enun"]  = u"Qual letra vem depois desta?"
F[u"p8enun"]  = u"Qual letra vem antes desta?"
F[u"p9enun"]  = u"Preencha os dois lados: quem vem antes e quem vem depois."
F[u"p10enun"] = u"Qual letra mora entre estas duas?"
F[u"p11enun"] = u"Agora escreva você a letra que falta. Toque no quadro vazio."
F[u"p12enun"] = u"Esta grade perdeu três letras. Puxe cada uma para o lugar dela."
F[u"p13enun"] = (u"No teclado do computador as letras não estão na ordem do alfabeto. "
                 u"Toque nelas na ordem certa.")
F[u"p14enun"] = u"Estas letras embaralharam. Toque nelas na ordem certa do alfabeto."
F[u"p15enun"] = u"Uma letra entrou no lugar errado. Circule quem saiu da fila."
F[u"p16enun"] = (u"Estas palavras estão em ordem alfabética, menos uma. "
                 u"Circule a que está fora da ordem.")
F[u"p17enun"] = (u"Estas palavras estão fora de ordem. Toque nelas na ordem do alfabeto, "
                 u"olhando a primeira letra.")
F[u"p18enun"] = (u"Estas palavras começam com a mesma letra. Olhe a segunda e ponha em ordem.")
F[u"p19enun"] = u"Qual das duas vem primeiro no dicionário? Pinte ela."
F[u"p20enun"] = u"Com que letra começa o nome da figura?"
F[u"p21enun"] = u"Puxe cada figura para a gaveta da letra com que ela começa."
F[u"p22enun"] = (u"Toque nas figuras na ordem do alfabeto. Use o alto-falante para ouvir "
                 u"o nome de cada uma.")
F[u"p23enun"] = u"Estes são nomes de crianças, como na chamada. Ponha em ordem alfabética."
F[u"p24enun"] = (u"Passe o dedo por cima da letra, como se estivesse escrevendo. "
                 u"Escolha a cor da canetinha.")
F[u"p25enun"] = (u"Toque nas letras que você quer no seu alfabeto. "
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

# ---- folha 2: o poema e a tira -----------------------------------------------
# ⚠️ O poema é do papel d09 da colheita (Djenane Alves), lido verso a verso.
VERSOS = [u"O alfabeto tem muitas letras,", u"todas elas importantes.",
          u"Algumas são simples,", u"e outras, muito elegantes."]
for n, v in enumerate(VERSOS):
    F[u"verso_%d" % n] = v
for it in IT[u"p2"]:
    L = it[u"L"]
    F[u"certo2_%s" % L] = u"Achou! O %s estava ali na fila." % NOME_LETRA[L]
    F[u"dica2_%s" % L] = (u"Ainda não é essa. Vá andando pela fila e dizendo os nomes "
                          u"até chegar no %s." % NOME_LETRA[L])

# ---- folha 3: nomear ---------------------------------------------------------
for it in IT[u"p3"]:
    L = it[u"L"]
    F[u"certo3_%s" % L] = u"Isso! Esta é a letra %s." % NOME_LETRA[L]
    F[u"dica3_%s" % L] = (u"Toque no alto-falante e escute de novo: %s. "
                          u"Qual delas é?" % NOME_LETRA[L])

# ---- folhas 4 e 5: a letra que fugiu (grande e pequena) ----------------------
for pote, n in ((u"p4", 4), (u"p5", 5)):
    for it in IT[pote]:
        k = it[u"i"]; L = A[k]
        ant = A[k - 1] if k > 0 else None
        peq = u" Repare que é a mesma letra, só que pequena." if n == 5 else u""
        F[u"certo%d_%s" % (n, L)] = ((u"Muito bem! Depois do %s vem o %s.%s"
                                      % (NOME_LETRA[ant], NOME_LETRA[L], peq)) if ant
                                     else u"Muito bem! O %s abre o alfabeto.%s"
                                          % (NOME_LETRA[L], peq))
        F[u"dica%d_%s" % (n, L)] = ((u"Fale as letras da fila em voz alta e continue: "
                                     u"qual vem depois do %s?" % NOME_LETRA[ant]) if ant
                                    else u"Esta é a primeira letra de todas.")

# ---- folha 6: ligar a grande com a pequena -----------------------------------
for it in IT[u"p6"]:
    for L in it[u"g"]:
        F[u"certo6_%s" % L] = (u"Isso! O %s grande e o %s pequeno são a mesma letra."
                               % (NOME_LETRA[L], NOME_LETRA[L]))
        F[u"dica6_%s" % L] = (u"Procure a letrinha pequena que tem o mesmo nome: %s."
                              % NOME_LETRA[L])

# ---- folhas 7 e 8: depois e antes --------------------------------------------
for it in IT[u"p7"]:
    L, c = it[u"L"], it[u"c"]
    F[u"certo7_%s" % L] = u"Isso! Depois do %s vem o %s." % (NOME_LETRA[L], NOME_LETRA[c])
    F[u"dica7_%s" % L] = (u"Comece a falar o alfabeto e pare no %s. "
                          u"Qual vem logo em seguida?" % NOME_LETRA[L])
for it in IT[u"p8"]:
    L, c = it[u"L"], it[u"c"]
    F[u"certo8_%s" % L] = u"Muito bem! Antes do %s vem o %s." % (NOME_LETRA[L], NOME_LETRA[c])
    # ⭐ a dica ENSINA O TRUQUE, que é o que falta a quem só recita para frente
    # ⚠️ a frase NÃO pode terminar em "do %s é a resposta": com a letra É isso
    #    vira "antes do é é a resposta" — duas vezes a mesma sílaba, e a criança
    #    que só ouve não entende nada. Ponto antes do "essa".
    F[u"dica8_%s" % L] = (u"Fale o alfabeto desde o começo e vá com atenção. A letra "
                          u"que você diz logo antes do %s. Essa é a resposta." % NOME_LETRA[L])

# ---- folha 9: os dois lados --------------------------------------------------
for it in IT[u"p9"]:
    L = it[u"L"]; k = A.index(L)
    F[u"certo9_%s" % L] = (u"Isso! %s, %s, %s."
                           % (NOME_LETRA[A[k - 1]], NOME_LETRA[L], NOME_LETRA[A[k + 1]]))
    F[u"dica9_%s" % L] = (u"Uma das duas vagas ainda não é essa. Fale o alfabeto até o %s "
                          u"e escute quem está de cada lado." % NOME_LETRA[L])

# ---- folha 10: a letra do meio -----------------------------------------------
for it in IT[u"p10"]:
    L = it[u"L"]; k = A.index(L)
    F[u"certo10_%s" % L] = (u"Isso! Entre o %s e o %s mora o %s."
                            % (NOME_LETRA[A[k - 1]], NOME_LETRA[A[k + 1]], NOME_LETRA[L]))
    F[u"dica10_%s" % L] = (u"Diga as duas em voz alta: %s… %s. Quem cabe no meio?"
                           % (NOME_LETRA[A[k - 1]], NOME_LETRA[A[k + 1]]))

# ---- folha 11: escrever a vizinha --------------------------------------------
for it in IT[u"p11"]:
    L, lado, c = it[u"L"], it[u"lado"], it[u"c"]
    F[u"certo11_%s_%s" % (L, lado)] = (u"Muito bem, você escreveu! %s vem %s do %s."
                                       % (NOME_LETRA[c].capitalize(), lado, NOME_LETRA[L]))
    F[u"dica11_%s_%s" % (L, lado)] = (u"Ainda não. Fale o alfabeto até o %s e escute qual "
                                      u"vem %s. Depois escreva essa letra."
                                      % (NOME_LETRA[L], lado))

# ---- folha 12: a grade -------------------------------------------------------
for it in IT[u"p12"]:
    k = it[u"i"]; L = A[k]
    F[u"certo12_%s" % L] = (u"Isso! A grade ficou pronta a partir do %s." % NOME_LETRA[L])
    F[u"dica12_%s" % L] = (u"Essa letra é de outra casinha. Fale a fila a partir do %s e "
                           u"conte os quadrados até achar o lugar dela." % NOME_LETRA[L])

# ---- folha 13: o teclado -----------------------------------------------------
for it in IT[u"p13"]:
    g = sorted(it[u"g"])
    # ⚠️ "a ordem é %s" grudava com o nome da letra É e virava "a ordem é é,
    #    quê, érre" — o revisor pegou como palavra repetida. Frase sem "é" antes.
    F[u"certo13_%s" % g[0]] = (u"Isso! No teclado elas estão bagunçadas, mas no alfabeto "
                               u"elas ficam assim: %s." % u", ".join(NOME_LETRA[x] for x in g))
    F[u"dica13_%s" % g[0]] = (u"Não siga a ordem do teclado. Pense na fila do alfabeto: "
                              u"qual destas vem primeiro?")

# ---- folha 14: ordenar letras ------------------------------------------------
for it in IT[u"p14"]:
    g = sorted(it[u"g"])
    F[u"certo14_%s" % g[0]] = u"Muito bem! %s." % u", ".join(NOME_LETRA[x] for x in g)
    F[u"dica14_%s" % g[0]] = (u"Qual destas vem primeiro no alfabeto? Comece por ela e "
                              u"vá seguindo a fila.")

# ---- folha 15: o intruso de letras -------------------------------------------
for it in IT[u"p15"]:
    c = it[u"c"]
    ordem = [x for x in it[u"g"] if x != c]
    F[u"certo15_%s" % c] = (u"Isso! O %s não é dessa parte da fila. Sem ele fica %s."
                            % (NOME_LETRA[c], u", ".join(NOME_LETRA[x] for x in ordem)))
    F[u"dica15_%s" % c] = (u"Fale as quatro em voz alta na ordem do alfabeto. "
                           u"Uma delas não encaixa — qual atrapalha a fila?")

# ---- folha 16: o intruso de palavras -----------------------------------------
for it in IT[u"p16"]:
    c = it[u"c"]
    for P in it[u"g"]:
        F[u"pal_%s" % P.lower()] = diz(P.lower()) + u"."
    ordem = [x for x in it[u"g"] if x != c]
    F[u"certo16_%s" % c] = (u"Isso! %s é que estava fora da ordem. As outras vão bem: %s."
                            % (diz(c.lower()).capitalize(),
                               u", ".join(diz(x.lower()) for x in ordem)))
    F[u"dica16_%s" % c] = (u"Olhe só a primeira letra de cada palavra e fale o alfabeto. "
                           u"Uma delas está no lugar errado.")

# ---- folhas 17, 18 e 23: ordenar palavras e nomes ----------------------------
for pote, n in ((u"p17", 17), (u"p18", 18), (u"p23", 23)):
    for it in IT[pote]:
        g = sorted(it[u"g"])
        for P in it[u"g"]:
            if n == 23:
                F[u"crianca_%s" % P] = diz(P.lower()).capitalize() + u"."
            else:
                F[u"pal_%s" % P.lower()] = diz(P.lower()) + u"."
        lidos = u", depois ".join(diz(x.lower()) for x in g)
        if n == 17:
            F[u"certo17_%s" % g[0]] = u"Isso! Em ordem do alfabeto: %s." % lidos
            F[u"dica17_%s" % g[0]] = (u"Olhe só a primeira letra de cada palavra. "
                                      u"Qual delas vem primeiro no alfabeto?")
        elif n == 18:
            F[u"certo18_%s" % g[0]] = (u"Muito bem! Todas começam igual, então mandou a "
                                       u"segunda letra: %s." % lidos)
            F[u"dica18_%s" % g[0]] = (u"A primeira letra é a mesma nas três, então ela não "
                                      u"decide nada. Olhe a segunda letra de cada uma.")
        else:
            F[u"certo23_%s" % g[0]] = (u"Isso! Na chamada eles ficariam assim: %s." % lidos)
            F[u"dica23_%s" % g[0]] = (u"É como na lista da professora: olhe a primeira "
                                      u"letra de cada nome e siga o alfabeto.")

# ---- folha 19: quem vem primeiro no dicionário -------------------------------
for it in IT[u"p19"]:
    a, b, c = it[u"a"], it[u"b"], it[u"c"]
    outra = b if c == a else a
    for P in (a, b):
        F[u"pal_%s" % P.lower()] = diz(P.lower()) + u"."
    F[u"certo19_%s" % c] = (u"Isso! %s vem antes de %s no dicionário."
                            % (diz(c.lower()).capitalize(), diz(outra.lower())))
    F[u"dica19_%s" % c] = (u"As duas começam com a mesma letra. Olhe a segunda letra de "
                           u"cada uma e veja qual vem primeiro no alfabeto.")

# ---- folha 20: a letra que abre a palavra ------------------------------------
for it in IT[u"p20"]:
    w, c = it[u"w"], it[u"c"]
    F[u"pal_%s" % w] = diz(w) + u"."
    F[u"certo20_%s" % w] = (u"Muito bem! %s começa com %s."
                            % (diz(w).capitalize(), NOME_LETRA[c]))
    F[u"dica20_%s" % w] = (u"Fale o nome da figura devagar: %s. Escute só o "
                           u"comecinho." % diz(w))

# ---- folha 21: as gavetas ----------------------------------------------------
for it in IT[u"p21"]:
    for w in it[u"ws"]:
        F[u"pal_%s" % w] = diz(w) + u"."
        F[u"dica21_%s" % w] = (u"Essa gaveta não é a de %s. Fale o nome devagar e escute "
                               u"com que letra ele começa." % diz(w))
    w0 = it[u"ws"][0]
    F[u"certo21_%s" % w0] = u"Isso! Cada palavra foi para a gaveta da letra dela."

# ---- folha 22: as figuras em ordem -------------------------------------------
for it in IT[u"p22"]:
    g = sorted(it[u"g"], key=lambda x: x.upper())
    for w in it[u"g"]:
        F[u"pal_%s" % w] = diz(w) + u"."
    F[u"certo22_%s" % g[0]] = (u"Isso! Em ordem do alfabeto: %s."
                               % u", depois ".join(diz(x) for x in g))
    F[u"dica22_%s" % g[0]] = (u"Diga o nome de cada figura para você mesmo e escute a "
                              u"primeira letra. Qual vem primeiro no alfabeto?")

# ---- folha 24: praticar a escrita --------------------------------------------
for it in IT[u"p24"]:
    L = it[u"L"]
    F[u"certo24_%s" % L] = u"Você escreveu o %s! Ficou muito bom." % NOME_LETRA[L]

# ---- folha 25: o mural -------------------------------------------------------
for it in IT[u"p25"]:
    L, w = it[u"L"], it[u"w"]
    F[u"pal_%s" % w] = diz(w) + u"."
    F[u"certo25_%s" % L] = (u"%s de %s foi para o seu alfabeto!"
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
