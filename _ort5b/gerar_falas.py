# -*- coding: utf-8 -*-
u"""
============================================================
 A LOTERIA DO S — gerador das falas (ortografia, 5º ano)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️⚠️ E NESTE CADERNO A VOZ É A TAREFA EM DUAS FOLHAS. Na 5 a criança decide se
    o S do meio soa como Z ou como S — e isso só se resolve OUVINDO. Na 19, o
    ditado, ela não vê a palavra em lugar nenhum: o alto-falante dita e ela
    procura no quadro. Sem mp3 essas duas folhas não existem.

 ⚠️ UMA FONTE SÓ. As palavras, as regras e os textos moram no bloco
    `/*DADOS-INI*/` do `index.html` e são LIDOS daqui.

 ⚠️ A DICA NUNCA DIZ A LETRA. Ela manda olhar a vogal seguinte, ou dá o sentido
    da palavra. Dizer "é com Ç" no segundo erro não é ajudar: é responder no
    lugar da criança.

 Uso:  python3 _ort5b/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"ls_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    m = re.search(r"var %s = (\{.*?\n\});" % nome, html, re.S)
    if not m:
        raise SystemExit(u"NAO ACHEI o bloco `var %s` no index.html" % nome)
    return json.loads(m.group(1))


IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
FICHA = bloco(u"FICHA")
LAC = bloco(u"LAC")
GAV = bloco(u"GAV")
REGRA = bloco(u"REGRA")
LOT = bloco(u"LOT")
SIL = bloco(u"SIL")
NSIL = bloco(u"NSIL")
ALFA = bloco(u"ALFA")
GRUDADA = bloco(u"GRUDADA")
DITADO = bloco(u"DITADO")
CACA = bloco(u"CACA")
CRUZP = bloco(u"CRUZP")
CARTAZ = bloco(u"CARTAZ")

F = {}


def slug(w):
    u"""o MESMO slug que o `chaveQuadro` do folhas.js: minúsculo, só a-z.
    ⚠️ Em BÚSSOLA isso dá "bssola" (o Ú some, porque não é a-z). Escrever
    "bussola" aqui deixaria aquele botão mudo, e nenhum portão de sintaxe veria.
    """
    return re.sub(u"[^a-z]", u"", w.lower())


# ---- `diz_<chave>`: UMA fonte por chave, e o conflito REPROVA aqui mesmo -----
PAL = {}


def diz(chave, palavra):
    if chave in PAL and PAL[chave] != palavra:
        raise SystemExit(u"CONFLITO: `diz_%s` vale '%s' e '%s' ao mesmo tempo"
                         % (chave, PAL[chave], palavra))
    PAL[chave] = palavra


for k, Fi in FICHA.items():
    diz(k, Fi[u"c"])           # a voz diz sempre a forma CERTA
for k, L in LAC.items():
    diz(k, L[u"p"])
for k, Lo in LOT.items():
    diz(k, Lo[u"p"])
for k in sorted(PAL):
    F[u"diz_%s" % k] = PAL[k].lower() + u"."

# ---- a casa -----------------------------------------------------------------
F[u"capa"] = (u"A Loteria do S. Vinte e duas folhas sobre um som só: o som de SAPO. "
              u"Acontece que ele se escreve de cinco jeitos diferentes, e é aí que a "
              u"gente erra. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim! Agora você tem o seu quadro de regras ali embaixo — "
             u"copie ele no seu caderno. E hoje, no primeiro texto que você ler, ache uma "
             u"palavra com o som de SAPO e pergunte: por que ela se escreve assim, e não "
             u"de outro jeito?")
F[u"escreva"] = u"Escreva a palavra usando o teclado."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Olhe de novo com calma e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa palavra do lado esquerdo e depois na do lado direito."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram de ordem."
F[u"toque_palavra"] = u"Primeiro toque numa palavra ali embaixo. Depois toque na gaveta dela."
F[u"toque_alfa"] = u"Primeiro toque numa palavra. Depois toque no lugar dela na fila."
F[u"toque_numero"] = u"Primeiro toque num número para ouvir a palavra ditada."
F[u"naoditada"] = u"Essa palavra não foi ditada agora. Ouça de novo e procure outra."
for L in (u"s", u"ss", u"c", u"ç", u"sc", u"x", u"z"):
    F[u"letra_%s" % L] = (u"Letra %s." % L.upper()) if len(L) == 1 else (u"%s." % L.upper())

# ---- o que cada folha pede (a ordem É a identidade: p7enun = folha 7) -------
ENUN = [
 (1,  u"folha um: leia as oito fichas com atenção. Metade delas está escrita ERRADA. "
      u"Marque só as que estão certas e toque em Conferir. Se você errar alguma, não "
      u"tem problema: é justamente para isso que servem as vinte folhas seguintes."),
 (2,  u"folha dois: em cada palavra falta uma letra. Toque no alto-falante, ouça, e "
      u"preencha com um S ou com dois SS."),
 (3,  u"folha três: as mesmas duas opções, e agora sem figura nenhuma. Só o ouvido e a "
      u"regra: dois SS só entram entre duas vogais, e nunca no começo da palavra."),
 (4,  u"folha quatro: olhe em que LUGAR da palavra está o S. No começo? No meio, entre "
      u"duas vogais? No fim? Ou são dois SS? Ponha cada palavra na gaveta certa."),
 (5,  u"folha cinco: esta folha só dá para fazer de ouvido. Ouça cada palavra e diga se "
      u"o som do meio é de Z, como em casa, ou de S, como em osso."),
 (6,  u"folha seis: agora o cê-cedilha. Existe uma regra que nunca falha: olhe a vogal "
      u"que vem logo DEPOIS do buraco."),
 (7,  u"folha sete: agora a pergunta é POR QUÊ. Toque na palavra e depois na regra que "
      u"explica como ela se escreve. As seis regras são as mesmas da folha de papel."),
 (8,  u"folha oito: preencha com C ou com o par S mais C. Esse par são duas letras para "
      u"um som só, e ele aparece em palavras da mesma família: nascer, nascimento."),
 (9,  u"folha nove: agora são três letras, e uma delas engana. Em exame e em exemplo, o "
      u"X soa como Z — mas quem se escreve ali é o X."),
 (10, u"folha dez: a loteria. Aqui as quatro letras estão misturadas na mesma tabela, e "
      u"ninguém avisa qual é a dupla. Leia a palavra e marque um X na letra que falta."),
 (11, u"folha onze: as mesmas palavras da loteria, e agora não há nada na tela para "
      u"copiar. Ouça e escreva a palavra inteira, letra por letra."),
 (12, u"folha doze: as quatro gavetas juntas. Todas estas palavras têm o mesmo som — o "
      u"do começo de SAPO — e cada uma o escreve com uma letra diferente."),
 (13, u"folha treze: as sílabas estão embaralhadas. Toque nelas na ordem certa e forme a "
      u"palavra. Lembre: os dois SS se separam, um fica numa sílaba e o outro na seguinte."),
 (14, u"folha catorze: bata palma para cada pedaço da palavra e diga quantas sílabas ela "
      u"tem."),
 (15, u"folha quinze: ponha as palavras em ordem alfabética, da primeira para a última. É "
      u"a mesma ordem que você usa para achar uma palavra no dicionário."),
 (16, u"folha dezesseis: agora a palavra está dentro de uma frase, e você tem quatro "
      u"letras para escolher. Leia a frase inteira antes de responder."),
 (17, u"folha dezessete: este é o passeio de domingo. Preencha o texto com um S ou com "
      u"dois SS."),
 (18, u"folha dezoito: esta frase está toda grudada, sem espaço nenhum. Toque ENTRE as "
      u"letras, no lugar onde entra o espaço, e separe as palavras."),
 (19, u"folha dezenove: o ditado. Toque num número para ouvir a palavra e depois ache "
      u"essa palavra no quadro. Aqui a palavra não está escrita em lugar nenhum antes: "
      u"você só tem o ouvido."),
 (20, u"folha vinte: na grade estão escondidas seis palavras. Arraste o dedo sobre as "
      u"letras, ou toque na primeira e na última."),
 (21, u"folha vinte e um: toque numa figura, escute e escreva a palavra na cruzadinha."),
 (22, u"folha vinte e dois: escolha as regras que você quer levar no seu quadro. Pode "
      u"escolher quantas quiser — e depois copie o quadro no seu caderno de papel."),
]
for n, t in ENUN:
    F[u"p%denun" % n] = t

# ---- folha 1: pinte só as escritas certas -----------------------------------
F[u"certo1"] = (u"Isso! Você achou todas. Repare: o que engana é o som — todas elas se "
                u"falam igual, certas ou erradas. Quem decide é a regra da escrita.")
F[u"dica1"] = (u"Olhe palavra por palavra e pergunte: esse som está entre duas vogais? "
               u"Então são dois SS. Está no começo, ou depois de consoante? Então é um S só.")

# ---- folhas 2, 3, 6, 8, 9, 16 e 17: a letra que falta ----------------------
for n in (2, 3, 6, 8, 9, 16, 17):
    for k in IT[u"p%d" % n]:
        L = LAC[k]
        F[u"certo%d_%s" % (n, k)] = u"Isso! %s, com %s." % (L[u"p"].lower().capitalize(), L[u"r"])
        F[u"dica%d_%s" % (n, k)] = L[u"d"]

# ---- folhas 4, 5 e 12: as gavetas ------------------------------------------
GK = {4: u"onde", 5: u"somz", 12: u"quatro"}
for n, gk in GK.items():
    G = GAV[gk]
    for C in G[u"cols"]:
        F[u"gav_%s_%s" % (gk, C[u"k"])] = C[u"d"]
    nomes = dict((c[u"k"], c[u"n"]) for c in G[u"cols"])
    for i in IT[u"p%d" % n]:
        P = G[u"pal"][i]
        F[u"diz2_%s_%d" % (gk, i)] = P[u"p"].lower() + u"."
        F[u"certo%d_%d" % (n, i)] = (u"Isso! %s: %s."
                                     % (P[u"p"].lower().capitalize(), nomes[P[u"c"]].lower()))
        F[u"dica%d_%d" % (n, i)] = (u"Ouça a palavra de novo e escute a regra de cada gaveta "
                                    u"antes de escolher.")

# ---- folha 7: ligar a palavra à regra --------------------------------------
for k in IT[u"p7"]:
    R = REGRA[k]
    F[u"pal_%s" % k] = R[u"p"].lower() + u"."
    # ⚠️ `rf` é a mesma regra escrita como a VOZ tem de dizer: "som de Z" vira
    #    "som de zê". A frase da tela continua a da folha de papel, palavra por
    #    palavra; o que muda é só a pronúncia da letra, e é o que o portão
    #    `_qa/falas.py` manda fazer.
    F[u"reg_%s" % k] = R.get(u"rf") or R[u"r"]
    F[u"certo7_%s" % k] = u"Isso! %s. %s" % (R[u"p"].lower().capitalize(), R.get(u"rf") or R[u"r"])
    F[u"dica7_%s" % k] = (u"Olhe a palavra letra por letra e pergunte: qual dessas regras "
                          u"fala justamente do pedaço difícil dela?")

# ---- folhas 10 e 11: a loteria ---------------------------------------------
for n in (10, 11):
    for k in IT[u"p%d" % n]:
        L = LOT[k]
        F[u"certo%d_%s" % (n, k)] = u"Isso! %s. %s" % (L[u"p"].lower().capitalize(), L[u"d"])
        F[u"dica%d_%s" % (n, k)] = L[u"d"]

# ---- folha 13: ordene as sílabas -------------------------------------------
for k in IT[u"p13"]:
    S = SIL[k]
    F[u"pistasil_%s" % k] = S[u"d"]
    F[u"certo13_%s" % k] = u"Isso! %s." % S[u"p"].lower().capitalize()
    F[u"dica13_%s" % k] = (u"Escute a dica de novo e vá devagar: qual pedaço começa a "
                           u"palavra? Diga ela em voz alta, bem separadinha.")

# ---- folha 14: quantas sílabas ---------------------------------------------
for k in IT[u"p14"]:
    N = NSIL[k]
    F[u"sil_%s" % k] = u"... ".join(s.lower() for s in N[u"s"]) + u"."
    F[u"certo14_%s" % k] = (u"Isso! %s tem %d sílabas: %s."
                            % (N[u"p"].lower().capitalize(), N[u"n"],
                               u", ".join(s.lower() for s in N[u"s"])))
    F[u"dica14_%s" % k] = (u"Diga a palavra batendo uma palma em cada pedaço. Cada palma "
                           u"é uma sílaba.")

# ---- folha 15: ordem alfabética --------------------------------------------
for lk in ALFA:
    lista = ALFA[lk][u"lista"]
    ordenada = sorted(lista)
    for w in lista:
        F[u"alfa_%s" % slug(w)] = w.lower() + u"."
        F[u"certo15_%s" % slug(w)] = (u"Isso! %s é a %dª da fila."
                                      % (w.lower().capitalize(), ordenada.index(w) + 1))
        F[u"dica15_%s" % slug(w)] = (u"Olhe a PRIMEIRA letra de cada palavra e siga a ordem "
                                     u"do alfabeto. Se as primeiras forem iguais, olhe a segunda.")

# ---- folha 18: separe as palavras ------------------------------------------
for k in IT[u"p18"]:
    G = GRUDADA[k]
    F[u"grud_%s" % k] = u" ".join(G[u"p"]).lower() + u"."
    F[u"certo18_%s" % k] = (u"Isso! A frase é: %s. E ela tem %d palavras."
                            % (u" ".join(G[u"p"]).lower(), len(G[u"p"])))
    F[u"dica18_%s" % k] = (u"Leia a frase em voz alta e escute onde uma palavra acaba e a "
                           u"outra começa. Toque bem no vão entre as duas letras.")

# ---- folha 19: o ditado -----------------------------------------------------
for i in IT[u"p19"]:
    w = DITADO[u"ditar"][i]
    F[u"dit_%s" % slug(w)] = w.lower() + u"."
    F[u"certo19_%d" % i] = u"Isso! %s." % w.lower().capitalize()
    F[u"dica19_%d" % i] = (u"Ouça de novo com calma e procure no quadro a palavra que "
                           u"começa com esse som.")

# ---- folha 20: o caça-palavras ---------------------------------------------
for k in IT[u"p20"]:
    C = CACA[k]
    F[u"certo20_%s" % k] = u"Achou %s! %s" % (C[u"p"].lower(), C[u"d"])

# ---- folha 21: a cruzadinha -------------------------------------------------
for k in IT[u"p21"]:
    P = CRUZP[k]
    F[u"pista_%s" % k] = P[u"d"]
    F[u"certo21_%s" % k] = u"Isso! %s." % P[u"p"].lower().capitalize()
    F[u"dica21_%s" % k] = (u"Escute a pista de novo e conte as casinhas da cruzadinha: "
                           u"a palavra tem esse tanto de letras.")

# ---- folha 22: o quadro de regras -------------------------------------------
for k in IT[u"p22"]:
    C = CARTAZ[k]
    F[u"certo22_%s" % k] = u"%s Por exemplo: %s." % (C[u"t"], C[u"ex"].lower())


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
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s) para gravar" % (len(F), len(falas)))
