# -*- coding: utf-8 -*-
u"""
============================================================
 A RUA DO MUNDO — gerador das falas (tipos de moradia, 2º ano)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️⚠️ E AQUI A VOZ NÃO É ACESSÓRIO. Boa parte da turma de 2º ano ainda soletra;
    metade das folhas deste caderno tem FRASE como resposta (o porquê, a
    definição, a pista da cruzadinha). Sem o alto-falante em cada opção, a
    criança escolheria pelo tamanho do texto — e a folha viraria loteria.

 ⚠️ UMA FONTE SÓ. Os dados (moradias, materiais, lugares, pistas, poema) moram
    no bloco `/*DADOS-INI*/` do `index.html` e são LIDOS daqui. Se eu os
    repetisse neste arquivo, seriam duas listas para combinar à mão — que é
    exatamente o defeito que já fez o relatório sair zero com a folha inteira
    respondida.

 Uso:  python3 _casa1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"mo_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    m = re.search(r"var %s = (\{.*?\n\});" % nome, html, re.S)
    if not m:
        raise SystemExit(u"NAO ACHEI o bloco `var %s` no index.html" % nome)
    return json.loads(m.group(1))


IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
MOR = bloco(u"MOR")
MAT = bloco(u"MAT")
LUG = bloco(u"LUG")
FRASES = bloco(u"FRASES")
PISTAS = bloco(u"PISTAS")
MAPA = bloco(u"MAPA")
VISTA = bloco(u"VISTA")
VISTAS = bloco(u"VISTAS")
TEMPO = bloco(u"TEMPO")
OBRA = bloco(u"OBRA")
PROF = bloco(u"PROF")
COMODO = bloco(u"COMODO")
OBJ = bloco(u"OBJ")
MARCAR = bloco(u"MARCAR")
POEMA = bloco(u"POEMA")

F = {}


def dizNome(k):
    u"""o nome da moradia como a VOZ deve dizê-lo (minúsculo, sem caixa alta)."""
    return MOR[k][u"n"].lower()


# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"A Rua do Mundo. Vinte e cinco folhas para descobrir uma coisa: não existe "
              u"um jeito certo de fazer casa. Existe o jeito que combina com o lugar. "
              u"Escreva o seu nome ali embaixo e toque em Começar.")
# ⭐ O FECHO COM GANCHO: a atividade termina deixando uma pergunta aberta, que é
#    o que faz a criança querer mais.
F[u"fim"] = (u"Você chegou ao fim! Agora você já sabe olhar uma casa e perguntar: de que ela "
             u"é feita, e por que ela é assim neste lugar? Olhe a sua rua ali embaixo. "
             u"E, no caminho de casa hoje, repare: quantos tipos de moradia você consegue "
             u"achar no seu bairro?")
F[u"escreva"] = u"Escreva a palavra usando o teclado."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Olhe de novo com calma e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura do lado esquerdo e depois na do lado direito."
F[u"novoCaderno"] = u"Caderno novo! As moradias mudaram de ordem."
F[u"toque_etiqueta"] = u"Primeiro toque num nome ali embaixo. Depois toque na casa dele."
F[u"toque_figura"] = u"Primeiro toque numa figura ali embaixo. Depois toque na coluna."
F[u"toque_objeto"] = u"Primeiro toque num objeto ali embaixo. Depois toque no cômodo."
F[u"toque_cena"] = u"Primeiro toque em quem você quer pôr na fila. Depois toque no lugar dela."
F[u"montenesta"] = u"Agora toque nas sílabas desta moradia, uma de cada vez, na ordem certa."
F[u"boa_metade"] = u"Boa! Falta a outra."
F[u"vistacima"] = u"Uma vista de cima."
F[u"naoemoradia"] = u"Essa palavra não é uma moradia. Procure os nomes de casa no poema."
F[u"poema"] = (u"%s. %s"
               % (POEMA[u"titulo"],
                  u" ".join(u" ".join(v) for v in POEMA[u"versos"])))

# ---- o que cada folha pede (a ordem É a identidade: p7enun = folha 7) -------
ENUN = [
 (1,  u"folha um: antes de conhecer as casas do mundo, uma pergunta. Para que serve uma "
      u"moradia? Marque TODAS as respostas certas, porque aqui é mais de uma. Depois toque "
      u"em Conferir."),
 (2,  u"folha dois: olhe a moradia e toque no nome dela. Estas são as que você vê no "
      u"caminho da escola."),
 (3,  u"folha três: agora são moradias de outros lugares do mundo. Olhe com atenção e "
      u"toque no nome de cada uma."),
 (4,  u"folha quatro: leve cada nome escrito até a moradia certa. Você pode arrastar o "
      u"nome, ou tocar no nome e depois na casa."),
 (5,  u"folha cinco: as sílabas estão embaralhadas na tabela lá em cima. Toque nelas na "
      u"ordem certa e descubra que moradia aparece."),
 (6,  u"folha seis: agora a pergunta muda. Não é mais o nome: é de QUE a casa é feita. "
      u"Toque no material certo."),
 (7,  u"folha sete: mesma pergunta, mas agora são quatro materiais para escolher. Olhe "
      u"bem a moradia antes de responder."),
 (8,  u"folha oito: ligue cada moradia ao material de que ela é feita. Toque na moradia e "
      u"depois no material."),
 (9,  u"folha nove: no diagrama estão escondidos cinco materiais de construção. Arraste o "
      u"dedo sobre as letras para achar cada um. Eles estão deitados ou em pé."),
 (10, u"folha dez: esta é a pergunta mais importante do caderno. Por que esta moradia é "
      u"feita desse material? Leia as três frases e toque na certa."),
 (11, u"folha onze: em que lugar do mundo a gente encontra esta moradia? Toque no lugar."),
 (12, u"folha doze: a moradia está no lugar dela. Agora diga por quê: o que existe naquele "
      u"lugar que fez a casa ficar assim?"),
 (13, u"folha treze: aqui algumas duplas estão trocadas. Olhe a moradia e o lugar e diga: "
      u"eles combinam, ou não combinam?"),
 (14, u"folha catorze: leia as três frases com calma. Só uma explica esta moradia."),
 (15, u"folha quinze: agora não tem figura nenhuma para ajudar. Leia a frase inteira e "
      u"toque na palavra que falta."),
 (16, u"folha dezesseis: a cruzadinha das casas. Toque numa pista, escute, e escreva a "
      u"palavra na cruzadinha. Dá para usar o teclado da tela ou o teclado de verdade."),
 (17, u"folha dezessete: imagine que você está num avião, bem em cima da casa. Qual destas "
      u"figuras é esta mesma moradia vista de cima?"),
 (18, u"folha dezoito: este é um bairro visto de cima, como o avião vê. Ache no mapa o que "
      u"a folha pedir, e toque ali."),
 (19, u"folha dezenove: a mesma casa e a mesma escola aparecem de três jeitos. De lado, de "
      u"cima, ou de esguelha? Ponha cada figura na coluna certa."),
 (20, u"folha vinte: as duas figuras são do mesmo lugar, mas em tempos diferentes. Ponha "
      u"uma no ANTES e a outra no HOJE."),
 (21, u"folha vinte e um: uma casa não nasce pronta. Ponha as cenas da construção na ordem "
      u"em que elas acontecem."),
 (22, u"folha vinte e dois: muita gente trabalha para uma casa ficar de pé. Ligue cada "
      u"profissional ao que ele faz na obra."),
 (23, u"folha vinte e três: agora entramos na casa. Em que cômodo fica cada coisa?"),
 (24, u"folha vinte e quatro: neste poema estão escondidas várias moradias. Toque em todas "
      u"as que você achar."),
 (25, u"folha vinte e cinco: agora é a sua rua. Escolha as moradias que você quer nela — "
      u"pode ser quantas você quiser, do mundo inteiro."),
]
for _n, _t in ENUN:
    F[u"p%denun" % _n] = _t[0].upper() + _t[1:]

# ---- toda moradia, todo material, todo lugar ---------------------------------
for k, M in MOR.items():
    # `olhe_` é a descrição falada: nunca diz o NOME, senão o alto-falante
    # entregaria a resposta das folhas 2, 3, 4 e 14.
    F[u"olhe_%s" % k] = M[u"def"]
    F[u"chamar_%s" % k] = dizNome(k) + u"."
    F[u"por_%s" % k] = M[u"por"]
    F[u"def_%s" % k] = M[u"def"]
for k, M in MAT.items():
    F[u"mat_%s" % k] = M[u"n"].lower() + u"."
for k, L in LUG.items():
    F[u"lug_%s" % k] = L[u"n"].lower() + u"."

# ---- folha 1: para que serve uma casa ----------------------------------------
for k, Q in MARCAR.items():
    F[u"perg1_%s" % k] = Q[u"q"] + u" " + u"; ".join(Q[u"c"] + Q[u"e"]) + u"."
    F[u"certo1_%s" % k] = (u"Isso mesmo! %s %s." % (Q[u"q"], u", ".join(Q[u"c"])))
    F[u"dica1_%s" % k] = (u"Falta alguma, ou sobrou alguma. Leia de novo uma por uma e "
                          u"pergunte: isto é mesmo coisa de casa?")

# ---- folhas 2 e 3: que moradia é esta -----------------------------------------
for n in (2, 3):
    for k in IT[u"p%d" % n]:
        F[u"certo%d_%s" % (n, k)] = u"Isso! É %s." % dizNome(k)
        F[u"dica%d_%s" % (n, k)] = (u"Escute a descrição de novo, no alto-falante: %s"
                                    % MOR[k][u"def"])

# ---- folha 4: arraste o nome ---------------------------------------------------
for k in IT[u"p4"]:
    F[u"certo4_%s" % k] = u"Muito bem! %s é esta." % dizNome(k).capitalize()
    F[u"dica4_%s" % k] = (u"Esse nome é de outra casa. Ouça a descrição desta aqui antes "
                          u"de escolher.")

# ---- folha 5: juntar as sílabas -------------------------------------------------
for k in IT[u"p5"]:
    sil = MOR[k][u"s"]
    F[u"pistasil_%s" % k] = MOR[k][u"def"]
    F[u"certo5_%s" % k] = (u"Isso! %s. %s."
                           % (u"... ".join(s.lower() for s in sil), dizNome(k).capitalize()))
    F[u"dica5_%s" % k] = (u"Escute a dica de novo e vá devagar: a primeira sílaba primeiro, "
                          u"depois a segunda.")

# ---- folhas 6 e 7: de que é feita -----------------------------------------------
for n in (6, 7):
    for k in IT[u"p%d" % n]:
        F[u"certo%d_%s" % (n, k)] = (u"Isso! %s é feita de %s."
                                     % (dizNome(k).capitalize(), MAT[MOR[k][u"mat"]][u"n"].lower()))
        F[u"dica%d_%s" % (n, k)] = (u"Olhe a parede e o telhado da figura. %s"
                                    % MOR[k][u"def"])

# ---- folha 8: ligar moradia ao material ------------------------------------------
for k in IT[u"p8"]:
    F[u"certo8_%s" % k] = (u"Isso! %s é de %s."
                           % (dizNome(k).capitalize(), MAT[MOR[k][u"mat"]][u"n"].lower()))
    F[u"dica8_%s" % k] = (u"Escute de novo: %s" % MOR[k][u"def"])

# ---- folha 9: o caça-palavras dos materiais ----------------------------------------
#  ⚠️ Achar a palavra ENSINA: a fala de acerto diz de que moradia aquele material é.
#     Caça-palavras que só dá "parabéns" é passatempo.
for k in IT[u"p9"]:
    quem = [dizNome(m) for m in MOR if MOR[m][u"mat"] == k]
    F[u"certo9_%s" % k] = (u"Achou: %s! É o material %s."
                           % (MAT[k][u"n"].lower(),
                              u"d%s %s" % (u"a" if quem and quem[0][0] in u"ao" else u"o", quem[0])
                              if quem else u"de muitas casas"))

# ---- folhas 10 e 12: o porquê --------------------------------------------------------
for n in (10, 12):
    for k in IT[u"p%d" % n]:
        F[u"certo%d_%s" % (n, k)] = u"Isso mesmo! %s" % MOR[k][u"por"]
        F[u"dica%d_%s" % (n, k)] = (u"Pense no lugar onde essa casa fica. O que existe lá "
                                    u"para construir? E o que NÃO existe?")
for k in IT[u"p12"]:
    F[u"perg12_%s" % k] = (u"Esta moradia fica %s. Por quê?"
                           % LUG[MOR[k][u"lug"]][u"n"].lower())

# ---- folha 11: em que lugar ------------------------------------------------------------
for k in IT[u"p11"]:
    F[u"certo11_%s" % k] = (u"Isso! A gente encontra %s %s."
                            % (dizNome(k), LUG[MOR[k][u"lug"]][u"n"].lower()))
    F[u"dica11_%s" % k] = (u"Olhe o chão e o que está em volta da casa na figura. %s"
                           % MOR[k][u"por"])

# ---- folha 13: combina ou não combina -----------------------------------------------------
F[u"op_sim"] = u"Sim, combina."
F[u"op_nao"] = u"Não combina."
for k in IT[u"p13"]:
    F[u"certo13_%s_sim" % k] = (u"Isso! %s combina com esse lugar. %s"
                                % (dizNome(k).capitalize(), MOR[k][u"por"]))
    F[u"certo13_%s_nao" % k] = (u"Isso! Esta dupla está trocada. %s %s"
                                % (dizNome(k).capitalize(), MOR[k][u"por"].lower()))
    F[u"dica13_%s" % k] = (u"Pergunte duas coisas: esse material existe naquele lugar? E "
                           u"essa casa aguenta o tempo que faz lá?")
    for l in LUG:
        F[u"dupla_%s_%s" % (k, l)] = (u"%s, %s." % (dizNome(k).capitalize(),
                                                    LUG[l][u"n"].lower()))

# ---- folha 14: qual frase explica ------------------------------------------------------------
for k in IT[u"p14"]:
    F[u"certo14_%s" % k] = u"Isso! %s" % MOR[k][u"def"]
    F[u"dica14_%s" % k] = (u"Leia as três de novo. Olhe a figura e veja qual frase fala do "
                           u"que você está vendo.")

# ---- folha 15: completar a frase -------------------------------------------------------------
for k in IT[u"p15"]:
    Fr = FRASES[k]
    F[u"frase_%s" % k] = (Fr[u"a"] + u"... " + Fr[u"b"]).replace(u"  ", u" ")
    F[u"certo15_%s" % k] = (u"Isso! %s" % (Fr[u"a"] + Fr[u"r"].lower() + Fr[u"b"]))
    F[u"dica15_%s" % k] = (u"Escute a frase inteira de novo e veja qual das palavras faz "
                           u"sentido no buraco.")
    F[u"pal_%s" % Fr[u"r"].lower()] = Fr[u"r"].lower() + u"."

# ---- folha 16: a cruzadinha -------------------------------------------------------------------
for k in IT[u"p16"]:
    F[u"pista_%s" % k] = PISTAS[k][u"p"]
    F[u"certo16_%s" % k] = (u"Isso! %s. %s" % (dizNome(k).capitalize(), MOR[k][u"def"]))
    F[u"dica16_%s" % k] = (u"Escute a pista de novo e conte as casinhas da cruzadinha: "
                           u"a palavra tem esse tanto de letras.")

# ---- folha 17: a mesma coisa vista de cima -----------------------------------------------------------
CIMA = bloco(u"CIMA")
for k, C in CIMA.items():
    F[u"certo17_%s" % k] = u"Isso! Esta é %s vista de cima. %s" % (C[u"n"], C[u"d"])
    F[u"dica17_%s" % k] = (u"De cima a gente não vê a frente das coisas: vê o formato delas "
                           u"por cima. %s" % C[u"d"])

# ---- folha 18: achar na praça vista de cima ----------------------------------------------------------
for k, A in MAPA[u"alvos"].items():
    F[u"mapa_%s" % k] = u"Ache %s na praça." % A[u"n"]
    F[u"mapadica_%s" % k] = A[u"d"]
    F[u"certo18_%s" % k] = u"Achou! %s %s" % (A[u"n"].capitalize(), A[u"d"].lower())

# ---- folha 19: frontal, vertical ou oblíqua ----------------------------------------------------------
for k, V in VISTAS.items():
    F[u"vista_%s" % k] = V[u"d"]
for k, V in VISTA.items():
    F[u"fig_%s" % k] = u"%s." % V[u"n"]
    F[u"certo19_%s" % k] = (u"Isso! Aqui está %s na %s. %s"
                            % (V[u"n"], VISTAS[V[u"v"]][u"n"].lower(), VISTAS[V[u"v"]][u"d"]))
    F[u"dica19_%s" % k] = (u"Pergunte: dá para ver a frente? Então é visão frontal. Só o de "
                           u"cima? É visão vertical. Um pouco dos dois, meio inclinado? "
                           u"É visão oblíqua.")

# ---- folha 20: antes e hoje -------------------------------------------------------------------------------
for k, T in TEMPO.items():
    F[u"tempo_%s" % k] = (u"Aqui é %s. Antes: %s Hoje: %s" % (T[u"n"], T[u"qa"], T[u"qh"]))
    F[u"certo20_%s" % k] = (u"Isso! %s mudou: antes, %s Hoje, %s"
                            % (T[u"n"].capitalize(), T[u"qa"].lower(), T[u"qh"].lower()))
    F[u"dica20_%s" % k] = (u"Procure as coisas que só existem hoje: asfalto, poste, carro. "
                           u"Onde elas não aparecem, é o ANTES.")
    F[u"fig_%s" % T[u"antes"]] = T[u"qa"]
    F[u"fig_%s" % T[u"hoje"]] = T[u"qh"]

# ---- folha 21: a ordem da construção -----------------------------------------------------------------------
for k, O in OBRA.items():
    F[u"obra_%s" % k] = O[u"d"]
    F[u"certo21_%s" % k] = u"Isso! %sº: %s %s" % (O[u"i"], O[u"n"], O[u"d"].lower())
    F[u"dica21_%s" % k] = (u"Pense na ordem de verdade: dá para levantar a parede antes de "
                           u"alguém desenhar a casa? Dá para pintar antes de a parede existir?")

# ---- folha 22: quem faz o quê ------------------------------------------------------------------------------
for k, P in PROF.items():
    F[u"prof_%s" % k] = P[u"n"].lower() + u"."
    F[u"tarefa_%s" % k] = P[u"t"]
    F[u"certo22_%s" % k] = u"Isso! %s: %s" % (P[u"n"].lower().capitalize(), P[u"t"].lower())
    F[u"dica22_%s" % k] = (u"Escute de novo o que está escrito do outro lado e procure a "
                           u"palavra que combina com o nome do trabalho.")

# ---- folha 23: cada coisa no seu cômodo ----------------------------------------------------------------------
for k, C in COMODO.items():
    F[u"comodo_%s" % k] = C[u"n"].lower() + u"."
for k, O in OBJ.items():
    F[u"obj_%s" % k] = O[u"n"] + u"."
    F[u"certo23_%s" % k] = u"Isso! %s fica n%s %s." % (
        O[u"n"].capitalize(), u"o" if COMODO[O[u"c"]][u"n"] in (u"QUARTO", u"BANHEIRO") else u"a",
        COMODO[O[u"c"]][u"n"].lower())
    F[u"dica23_%s" % k] = (u"Pense na sua casa: em que cômodo essa coisa fica? É onde a "
                           u"gente dorme, come, toma banho, ou fica junto?")

# ---- folha 24: as casas dentro do poema ------------------------------------------------------------------------
F[u"certo24"] = u"Achou uma moradia! Continue procurando."

# ---- folha 25: a rua do mundo -------------------------------------------------------------------------------------
for k in IT[u"p25"]:
    F[u"certo25_%s" % k] = (u"%s entrou na sua rua! %s"
                            % (dizNome(k).capitalize(), MOR[k][u"por"]))


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
