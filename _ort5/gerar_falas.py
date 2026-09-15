# -*- coding: utf-8 -*-
u"""
============================================================
 O CASO DOS SONS IGUAIS — gerador das falas (ortografia e leitura, 5º ano)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️⚠️ E NESTE CADERNO A VOZ NÃO É ACESSÓRIO: EM UMA FOLHA ELA É A TAREFA. A
    folha 9 mostra a palavra com um buraco no lugar do H e pergunta se ela leva
    H. O H não tem som; a palavra escrita inteira entregaria a resposta. A única
    forma de a criança saber QUAL É A PALAVRA é ouvi-la. Sem mp3, aquela folha
    não existe — vira adivinhação.

 ⚠️ UMA FONTE SÓ. Os dados (as palavras, as regras, os textos dos três gêneros,
    a história dos dez erros) moram no bloco `/*DADOS-INI*/` do `index.html` e
    são LIDOS daqui. Se eu os repetisse neste arquivo, seriam duas listas para
    combinar à mão — que é exatamente o defeito que já fez o relatório sair zero
    com a folha inteira respondida.

 ⚠️ A DICA NUNCA DIZ A LETRA. Ela dá o SENTIDO da palavra, ou manda olhar a
    letra vizinha. Dizer "é com Ç" no segundo erro não é ajudar: é responder no
    lugar da criança, e a folha seguinte cobra o mesmo de novo.

 Uso:  python3 _ort5/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"o5_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    m = re.search(r"var %s = (\{.*?\n\});" % nome, html, re.S)
    if not m:
        raise SystemExit(u"NAO ACHEI o bloco `var %s` no index.html" % nome)
    return json.loads(m.group(1))


IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
LAC = bloco(u"LAC")
GAV = bloco(u"GAV")
DET = bloco(u"DET")
HAG = bloco(u"HAG")
PARERR = bloco(u"PARERR")
REGRA = bloco(u"REGRA")
BILHETE = bloco(u"BILHETE")
BILERR = bloco(u"BILERR")
RECEITA = bloco(u"RECEITA")
NOTICIA = bloco(u"NOTICIA")
HISTORIA = bloco(u"HISTORIA")
REESC = bloco(u"REESC")
BANCO = bloco(u"BANCO")
CACA = bloco(u"CACA")
CRUZP = bloco(u"CRUZP")
CARTAZ = bloco(u"CARTAZ")

F = {}

# ---- `diz_<chave>`: UMA fonte por chave, e o conflito REPROVA aqui mesmo -------
#      Quatro blocos diferentes trazem a mesma palavra (HÁBITO está no detetive e
#      na folha do H; CERTEZA está no detetive e no reescreva). A fala é a mesma,
#      e tem de ser: se duas fontes discordassem, a criança ouviria uma palavra
#      na folha 7 e outra na folha 19 com o mesmo botão. O assert abaixo é o que
#      impede isso de passar calado.
PAL = {}


def diz(chave, palavra):
    if chave in PAL and PAL[chave] != palavra:
        raise SystemExit(u"CONFLITO: `diz_%s` vale '%s' e '%s' ao mesmo tempo"
                         % (chave, PAL[chave], palavra))
    PAL[chave] = palavra


for k, L in LAC.items():
    diz(k, L[u"p"])
for k, D in DET.items():
    diz(k, D[u"c"])
for k, H in HAG.items():
    diz(k, H[u"p"])
for k, R in REESC.items():
    diz(k, R[u"p"])
for k in sorted(PAL):
    F[u"diz_%s" % k] = PAL[k].lower() + u"."

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"O Caso dos Sons Iguais. Vinte e três folhas para resolver um caso: "
              u"existem letras diferentes que fazem exatamente o mesmo som, e é por isso "
              u"que a gente erra. Escreva o seu nome ali embaixo e toque em Começar.")
# ⭐ O FECHO COM GANCHO: a atividade termina deixando uma pergunta aberta, que é
#    o que faz a criança querer mais.
F[u"fim"] = (u"Você chegou ao fim! Agora você já sabe fazer a pergunta de detetive: esta "
             u"palavra soa assim, mas com que letra ela se escreve? Olhe o seu cartaz ali "
             u"embaixo. E hoje, na primeira página que você ler, procure uma palavra com o "
             u"som de SAPO. Com qual das quatro letras ela está escrita?")
F[u"escreva"] = u"Escreva a palavra usando o teclado."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Olhe de novo com calma e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa palavra do lado esquerdo e depois na do lado direito."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram de ordem."
F[u"toque_palavra"] = u"Primeiro toque numa palavra ali embaixo. Depois toque na gaveta dela."
F[u"toque_passo"] = u"Primeiro toque no passo que você quer pôr na fila. Depois toque no lugar dele."
F[u"toque_quadro"] = u"Primeiro toque numa palavra do quadro. Depois toque no buraco da frase."
F[u"estacerta"] = u"Essa palavra está escrita certa. Procure as que estão erradas."
for L in u"TDLRSUMNGJ":
    F[u"letra_%s" % L] = u"Letra %s." % L

# ---- o que cada folha pede (a ordem É a identidade: p7enun = folha 7) -------
ENUN = [
 (1,  u"folha um: em cada palavra falta uma letra. Toque no alto-falante para ouvir a "
      u"palavra e preencha com T ou com D. Estas duas soam diferente: o ouvido resolve."),
 (2,  u"folha dois: agora são três letras. Ouça a palavra e preencha com L, com R ou com S."),
 (3,  u"folha três: preencha com U ou com L. Estas duas terminam a sílaba quase do mesmo "
      u"jeito, então ouça com atenção antes de escolher."),
 (4,  u"folha quatro: atenção, o caso muda aqui. Todas estas palavras têm o mesmo som — "
      u"o do começo de SAPO — mas cada uma escreve esse som com uma letra diferente. "
      u"Ponha cada palavra na gaveta certa: S, dois SS, C ou cê-cedilha. O ouvido "
      u"sozinho já não resolve mais."),
 (5,  u"folha cinco: agora o som do começo de ZEBRA. Ele se escreve com Z, mas também "
      u"com S quando o S fica entre duas vogais. Ponha cada palavra na sua gaveta."),
 (6,  u"folha seis: o som do começo de CHUVA. Às vezes ele se escreve com X, às vezes "
      u"com C agá. Ponha cada palavra na gaveta certa."),
 (7,  u"folha sete: o desafio do detetive. Em cada linha, só uma palavra está escrita "
      u"certa. Circule a certa."),
 (8,  u"folha oito: o detetive de novo, e agora as palavras são mais compridas. Leia com "
      u"calma e circule a que está certa."),
 (9,  u"folha nove: esta folha só dá para fazer de ouvido. Toque no alto-falante, escute a "
      u"palavra e diga se ela começa com agá. O agá não tem som nenhum, então é preciso "
      u"lembrar de cada palavra."),
 (10, u"folha dez: preencha com M ou com N. Aqui existe uma regra, e ela nunca falha: "
      u"olhe a letra que vem DEPOIS do buraco."),
 (11, u"folha onze: preencha com G ou com J. Antes de E e de I os dois fazem o mesmo som. "
      u"Algumas têm regra; outras a gente guarda de cor."),
 (12, u"folha doze: de um lado estão palavras escritas errado, do outro as mesmas palavras "
      u"escritas certo. Toque na errada e depois na certa que corresponde a ela."),
 (13, u"folha treze: agora a pergunta é POR QUÊ. Toque na palavra e depois na regra que "
      u"explica como ela se escreve."),
 (14, u"folha catorze: leia o recado da direção da escola e responda as três perguntas. "
      u"Dá para voltar e ler o recado de novo quantas vezes você quiser."),
 (15, u"folha quinze: é o mesmo recado, mas agora alguém o digitou com pressa. Toque nas "
      u"cinco palavras escritas errado."),
 (16, u"folha dezesseis: os passos desta receita estão fora de ordem. Ponha cada um no seu "
      u"lugar, do primeiro ao último."),
 (17, u"folha dezessete: leia a notícia e marque TODAS as perguntas que ela responde. "
      u"Cuidado: duas delas a notícia não responde. Depois toque em Conferir."),
 (18, u"folha dezoito: leia a história com atenção. Existem dez palavras escritas errado "
      u"escondidas nela. Toque em cada uma que você achar."),
 (19, u"folha dezenove: agora não há nenhuma palavra certa na tela para você copiar. Toque "
      u"nas casinhas e escreva cada palavra do jeito certo, letra por letra."),
 (20, u"folha vinte: preencha as frases usando as palavras do quadro. Você pode arrastar a "
      u"palavra até o buraco, ou tocar na palavra e depois no buraco."),
 (21, u"folha vinte e um: na grade estão escondidas seis palavras. Arraste o dedo sobre as "
      u"letras, ou toque na primeira e na última. Elas estão deitadas ou em pé."),
 (22, u"folha vinte e dois: toque numa figura, escute e escreva a palavra na cruzadinha. "
      u"Todas elas têm uma sílaba que termina em L."),
 (23, u"folha vinte e três: escolha as regras que você quer levar no seu cartaz. Pode "
      u"escolher quantas quiser — e depois copie o cartaz no seu caderno."),
]
for n, t in ENUN:
    F[u"p%denun" % n] = t

# ---- folhas 1, 2, 3, 10 e 11: a letra que falta ------------------------------
for n in (1, 2, 3, 10, 11):
    for k in IT[u"p%d" % n]:
        L = LAC[k]
        F[u"certo%d_%s" % (n, k)] = u"Isso! %s, com %s." % (L[u"p"].lower().capitalize(), L[u"r"])
        F[u"dica%d_%s" % (n, k)] = L[u"d"]

# ---- folhas 4, 5 e 6: as gavetas de cada som --------------------------------
GK = {4: u"som_s", 5: u"som_z", 6: u"som_x"}
for n, gk in GK.items():
    G = GAV[gk]
    for C in G[u"cols"]:
        F[u"gav_%s_%s" % (gk, C[u"k"])] = C[u"d"]
    for i in IT[u"p%d" % n]:
        P = G[u"pal"][i]
        nome = dict((c[u"k"], c[u"n"]) for c in G[u"cols"])[P[u"c"]]
        F[u"diz2_%s_%d" % (gk, i)] = P[u"p"].lower() + u"."
        F[u"certo%d_%d" % (n, i)] = (u"Isso! %s se escreve com %s."
                                     % (P[u"p"].lower().capitalize(), nome))
        F[u"dica%d_%d" % (n, i)] = (u"Escute a regra de cada gaveta antes de escolher. "
                                    u"Olhe também que letra vem antes e que letra vem depois "
                                    u"desse som na palavra.")

# ---- folhas 7 e 8: o detetive ----------------------------------------------
for n in (7, 8):
    for k in IT[u"p%d" % n]:
        D = DET[k]
        F[u"certo%d_%s" % (n, k)] = u"Isso! %s." % D[u"c"].lower().capitalize()
        F[u"dica%d_%s" % (n, k)] = D[u"d"]

# ---- folha 9: tem H no começo? ---------------------------------------------
for k in IT[u"p9"]:
    H = HAG[k]
    F[u"certo9_%s" % k] = (u"Isso! %s se escreve %s agá."
                           % (H[u"p"].lower().capitalize(), u"com" if H[u"r"] else u"sem"))
    F[u"dica9_%s" % k] = H[u"d"]

# ---- folha 12: ligar o errado ao certo --------------------------------------
for k in IT[u"p12"]:
    P = PARERR[k]
    F[u"err_%s" % k] = P[u"e"].lower() + u", escrito errado."
    F[u"cert_%s" % k] = P[u"c"].lower() + u"."
    F[u"certo12_%s" % k] = u"Isso! O certo é %s. %s" % (P[u"c"].lower(), P[u"d"])
    F[u"dica12_%s" % k] = (u"Leia a palavra errada em voz alta e procure do outro lado a "
                           u"mesma palavra, só que bem escrita.")

# ---- folha 13: ligar a palavra à regra --------------------------------------
for k in IT[u"p13"]:
    R = REGRA[k]
    F[u"pal_%s" % k] = R[u"p"].lower() + u"."
    F[u"reg_%s" % k] = R[u"r"]
    F[u"certo13_%s" % k] = u"Isso! %s. %s" % (R[u"p"].lower().capitalize(), R[u"r"])
    F[u"dica13_%s" % k] = (u"Olhe a palavra letra por letra e pergunte: qual dessas regras "
                           u"fala justamente do pedaço difícil dela?")

# ---- folha 14: o recado -----------------------------------------------------
F[u"bilhete"] = u"%s. %s" % (BILHETE[u"titulo"], u" ".join(BILHETE[u"linhas"]))
for i in IT[u"p14"]:
    P = BILHETE[u"perg"][i]
    F[u"perg14_%d" % i] = P[u"q"]
    F[u"certo14_%d" % i] = u"Isso! %s" % P[u"c"]
    F[u"dica14_%d" % i] = P[u"d"]

# ---- folha 15: os erros dentro do recado ------------------------------------
F[u"bilerr"] = (u"%s. %s" % (BILERR[u"titulo"],
                             u" ".join(u" ".join(v) for v in BILERR[u"linhas"])))
F[u"certo15"] = u"Achou uma palavra escrita errado! Continue procurando."

# ---- folha 16: a receita ----------------------------------------------------
F[u"receita"] = u"%s." % RECEITA[u"titulo"]
for i in IT[u"p16"]:
    P = RECEITA[u"passos"][i]
    F[u"passo_%d" % i] = P[u"t"]
    F[u"certo16_%d" % i] = u"Isso! O %sº passo é este: %s" % (P[u"i"], P[u"t"].lower())
    F[u"dica16_%d" % i] = (u"Pense na cozinha de verdade: dá para espremer o limão antes de "
                           u"cortar? Dá para mexer o suco antes de a água entrar?")

# ---- folha 17: a notícia ----------------------------------------------------
F[u"noticia"] = u"%s. %s" % (NOTICIA[u"titulo"], u" ".join(NOTICIA[u"linhas"]))
for k in IT[u"p17"]:
    M = NOTICIA[u"marcar"][k]
    F[u"pnot_%s" % k] = M[u"t"] + u"."
F[u"certo17"] = (u"Isso! Uma notícia conta o que aconteceu, quando, onde e quem estava lá. "
                 u"O resto, ela pode simplesmente não dizer.")
F[u"dica17"] = (u"Volte ao texto e procure com o dedo. Se a informação não estiver escrita "
                u"em lugar nenhum, não marque: notícia não é adivinhação.")

# ---- folha 18: os dez erros da história -------------------------------------
F[u"historia"] = (u"%s. %s" % (HISTORIA[u"titulo"],
                               u" ".join(u" ".join(v) for v in HISTORIA[u"linhas"])))
F[u"certo18"] = u"Achou uma palavra escrita errado! Continue procurando."

# ---- folha 19: reescreva do jeito certo -------------------------------------
for k in IT[u"p19"]:
    R = REESC[k]
    F[u"certo19_%s" % k] = u"Isso! %s. %s" % (R[u"p"].lower().capitalize(), R[u"d"])
    F[u"dica19_%s" % k] = R[u"d"]

# ---- folha 20: o banco de palavras ------------------------------------------
for i in IT[u"p20"]:
    Fr = BANCO[u"frases"][i]
    # ⚠️ O BURACO DA FRASE FALADA É "…", UM CARACTERE SÓ, e não três pontos.
    #    Com "...", o revisor lia FIM DE FRASE e acusava "espaço antes de
    #    pontuação" em "do meio ... ." e "minúscula depois de ponto" em
    #    "... para todos". As reticências de um caractere só não são ponto para
    #    ninguém — nem para o revisor, nem para a voz, que faz a pausa igual.
    F[u"frase_%s" % Fr[u"k"]] = ((Fr[u"a"] + u"…" + Fr[u"b"]).replace(u"  ", u" ")
                                 + u" Que palavra entra no buraco?")
    F[u"certo20_%d" % i] = u"Isso! %s%s%s" % (Fr[u"a"], Fr[u"r"].lower(), Fr[u"b"])
    F[u"dica20_%d" % i] = Fr[u"d"]
# ⚠️ A CHAVE DO BOTÃO DO QUADRO É A QUE O JAVASCRIPT MONTA, e não uma minha:
#    `w.toLowerCase().replace(/[^a-z]/g, "")`. Em IMPORTÂNCIA isso dá "importncia"
#    (o Â some, porque não é a-z). Escrever "importancia" aqui deixaria aquele
#    botão mudo, e nenhum portão de sintaxe veria.
for w in BANCO[u"quadro"]:
    ch = re.sub(u"[^a-z]", u"", w.lower())
    F[u"quadro_%s" % ch] = w.lower() + u"."

# ---- folha 21: o caça-palavras ----------------------------------------------
#  ⚠️ Achar a palavra ENSINA: a fala de acerto diz a REGRA daquela palavra.
#     Caça-palavras que só dá "parabéns" é passatempo.
for k in IT[u"p21"]:
    C = CACA[k]
    F[u"certo21_%s" % k] = u"Achou %s! %s" % (C[u"p"].lower(), C[u"d"])

# ---- folha 22: a cruzadinha -------------------------------------------------
for k in IT[u"p22"]:
    P = CRUZP[k]
    F[u"pista_%s" % k] = P[u"d"]
    F[u"certo22_%s" % k] = (u"Isso! %s. Olhe a sílaba do fim: ela termina em L."
                            % P[u"p"].lower().capitalize())
    F[u"dica22_%s" % k] = (u"Escute a pista de novo e conte as casinhas da cruzadinha: "
                           u"a palavra tem esse tanto de letras.")

# ---- folha 23: o cartaz do detetive ------------------------------------------
for k in IT[u"p23"]:
    C = CARTAZ[k]
    F[u"certo23_%s" % k] = u"%s Por exemplo: %s." % (C[u"t"], C[u"ex"].lower())


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
