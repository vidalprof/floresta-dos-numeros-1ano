# -*- coding: utf-8 -*-
u"""
============================================================
 A FÁBRICA DE NOMES — gerador das falas (substantivos, 5º ano)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️ UMA FONTE SÓ. As palavras, as frases e o texto moram no bloco
    `/*DADOS-INI*/` do `index.html` e são LIDOS daqui. Nada de segunda lista
    para desencontrar: já custou caro nesta casa um relatório sair zero com a
    folha inteira respondida.

 ⚠️⚠️ E NESTE CADERNO A VOZ NÃO É ENFEITE. A folha 7 pede para achar a palavra
    com a letra do começo trocada num trecho de história; a 24 é um texto para
    LER e interpretar. No 5º ano ainda há quem soletre — sem o alto-falante em
    cada frase e em cada resposta, a criança escolhe pelo tamanho da palavra e
    a folha vira sorteio. É a regra do Marcos: *"o alto-falante nas respostas
    também, para ajudar os alunos que não sabem ler"*.

 ⚠️ A DICA NUNCA DIZ A RESPOSTA. Ela manda olhar a primeira letra, ou perguntar
    se existe mais de um daquilo no mundo. Responder no segundo erro não é
    ajudar: é tirar da criança a única chance de pensar de novo.

 Uso:  python3 _subst5/gerar_falas.py
 Saída: reescreve os blocos FALAS e VOZOK do index.html, o `falas.json` e o
        `voz.txt`.
============================================================
"""
from __future__ import print_function

import collections
import io
import json
import os
import re
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"sb_"
VOZ = u"pt-BR-AntonioNeural"

D = io.open(CAM, encoding="utf-8").read()

def bloco(nome):
    m = re.search(r"var " + nome + r" = (\{.*?\n\});", D, re.S)
    txt = m.group(1)
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r'"\s*\+\s*\n\s*"', "", txt)          # junta "a" + "b"
    txt = re.sub(r'([\{,]\s*)"?([A-Za-zÀ-ÿ_0-9]+)"?\s*:', r'\1"\2":', txt)
    txt = re.sub(r",(\s*[\}\]])", r"\1", txt)
    return json.loads(txt)

PAR, FIG, GAV, JULGA = bloco("PAR"), bloco("FIG"), bloco("GAV"), bloco("JULGA")
ERRADO, GENT, MEU = bloco("ERRADO"), bloco("GENT"), bloco("MEU")
FIGC, COMPOR, GRIFA = bloco("FIGC"), bloco("COMPOR"), bloco("GRIFA")
GRUDA, SIGN, PARDER = bloco("GRUDA"), bloco("SIGN"), bloco("PARDER")
MAQ, PRIM, VEIO = bloco("MAQ"), bloco("PRIM"), bloco("VEIO")
FAM, DUPLA, INTRUSA = bloco("FAM"), bloco("DUPLA"), bloco("INTRUSA")
COLE, TEXTO, CARTAZ = bloco("COLE"), bloco("TEXTO"), bloco("CARTAZ")

def lp(s):
    u"""tira marcação e deixa o texto do jeito que a voz vai dizer"""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

def ch(w):
    return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", w.lower())
                  .encode("ascii", "ignore").decode())

F = collections.OrderedDict()
def p(k, v): F[k] = v

# ---------- as falas do motor ----------
p("capa", u"A Fábrica de Nomes. Vinte e cinco folhas sobre os nomes das coisas. "
          u"Tudo tem nome — e alguns nomes são só de um. Escreva o seu nome ali "
          u"embaixo e toque em Começar.")
p("folhaPronta", u"Folha pronta! Muito bem.")
p("escreva", u"Escreva a palavra usando o teclado.")
p("ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p("toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na gaveta dela.")
p("toque_cor", u"Primeiro escolha uma cor ali em cima. Depois toque nas palavras da família.")
p("toque_marca", u"Primeiro escolha a marca ali em cima. Depois toque na palavra.")
p("vozOn", u"Narração ligada!")
p("fim", u"Você chegou ao fim! Agora você tem o seu cartaz ali embaixo — copie "
         u"ele no seu caderno. E hoje, no primeiro texto que você ler, ache um "
         u"nome que começa com letra grande e pergunte: por que este aqui é de "
         u"um só?")
p("op_comum", u"Serve para muitos.")
p("op_proprio", u"É de um só.")
p("op_certa", u"Está certa.")
p("op_erro", u"Tem erro.")
p("marca_p", u"A que veio primeiro.")
p("marca_d", u"A que nasceu dela.")
for s in ["eiro","aria","ada","eira","ista","ilha"]:
    p("sufixo_" + s, u"terminação %s." % s)

# ---------- 1 ----------
p("p1enun", u"Folha um: o mesmo bicho, dois nomes. Olhe o desenho. Um destes "
            u"nomes serve para todos os que são assim. Qual é?")
for k, P in PAR.items():
    p("par_" + k, u"Este aqui se chama %s. Mas qual destes dois nomes serve "
                  u"para todos?" % P["p"])
    p("diz_%s_c" % k, P["c"] + u".")
    p("diz_%s_p" % k, P["p"] + u".")
    p("certo1_" + k, u"Isso! %s serve para todos. %s é o nome só dele."
                     % (P["c"].capitalize(), P["p"]))
    p("dica1_" + k, u"%s é o nome de um só, como o seu nome é seu. Procure o "
                    u"nome que serve para todos." % P["p"])

# ---------- 2, 4, 5, 10: gavetas ----------
GN = {"cp1": (2, u"Folha dois: serve para muitos ou é de um só? Leve cada palavra "
                 u"para a gaveta certa."),
      "cp2": (4, u"Folha quatro: recorte e cole. Leve cada palavra para a coluna "
                 u"certa."),
      "cp3": (5, u"Folha cinco: agora sem desenho nenhum. Olhe a primeira letra "
                 u"de cada palavra."),
      "sc":  (10, u"Folha dez: quantas palavras estão escondidas dentro de cada "
                  u"uma? Uma ou duas?")}
GAVFALA = {
 "cp1": {"c": u"Nesta gaveta vão os nomes que servem para muitos.",
         "p": u"Nesta gaveta vão os nomes de um só, que começam com letra grande."},
 "cp2": {"c": u"Nesta coluna vão os substantivos comuns.",
         "p": u"Nesta coluna vão os substantivos próprios."},
 "cp3": {"c": u"Nesta coluna vão os substantivos comuns.",
         "p": u"Nesta coluna vão os substantivos próprios."},
 "sc":  {"s": u"Nesta gaveta vai a palavra feita de uma só.",
         "c": u"Nesta gaveta vai a palavra feita de duas juntas."}}
for gk, (pi, enun) in GN.items():
    p("p%denun" % pi, enun)
    for col, t in GAVFALA[gk].items():
        p("gav_%s_%s" % (gk, col), t)
    for n, P in GAV[gk]["pal"].items():
        p("diz2_%s_%s" % (gk, n), P["p"] + u".")
        if gk == "sc":
            um = P["c"] == "s"
            p("certo%d_%s" % (pi, n),
              u"Isso! %s é uma palavra só." % P["p"] if um
              else u"Isso! %s é feita de duas palavras juntas." % P["p"])
            p("dica%d_%s" % (pi, n),
              u"Escute devagar: %s. Dá para achar duas palavras aí dentro?" % P["p"])
        else:
            com = P["c"] == "c"
            p("certo%d_%s" % (pi, n),
              u"Isso! %s serve para muitos." % P["p"] if com
              else u"Isso! %s é o nome de um só, e começa com letra grande." % P["p"])
            p("dica%d_%s" % (pi, n),
              u"Olhe a primeira letra de %s. Letra grande é sinal de nome de um só."
              % P["p"])

# ---------- 3 ----------
p("p3enun", u"Folha três: este nome serve para muitos ou é de um só? Toque na "
            u"resposta.")
for k, G in FIG.items():
    p("diz_" + k, G["n"] + u".")
    p("certo3_" + k,
      u"Isso! %s serve para muitos." % G["n"] if G["r"] == "c"
      else u"Isso! %s é o nome de um só — repare na letra grande." % G["n"])
    p("dica3_" + k, u"Pense: existe mais de um %s no mundo? Se existe, o nome "
                    u"serve para muitos." % G["n"].lower())

# ---------- 6 ----------
p("p6enun", u"Folha seis: esta frase está escrita certa, ou tem alguma letra "
            u"grande no lugar errado?")
for k, J in JULGA.items():
    p("frase_" + k, lp(J["f"]))
    p("certo6_" + k, u"Isso! " + lp(J["pq"]))
    p("dica6_" + k, u"Leia de novo devagar e olhe a primeira letra de cada nome.")

# ---------- 7 ----------
p("p7enun", u"Folha sete: neste pedaço da história há palavras com a letra do "
            u"começo trocada. Toque em cada uma que está errada.")
for k, T in ERRADO.items():
    p("trecho_" + k, lp(u" ".join(T["palavras"])))
p("certo7", u"Isso! Você achou todas. Nome de um só começa com letra grande; "
            u"os outros, com letra pequena.")
p("dica7", u"Olhe a primeira letra. Cãozinho, Casa e Motorista servem para "
           u"muitos — deviam começar pequeno.")

# ---------- 8 ----------
p("p8enun", u"Folha oito: preencha a frase com o nome do lugar. Ele começa com "
            u"letra grande.")
for k, G in GENT.items():
    p("gent_" + k, lp(G["a"]) + u" que lugar?")
    p("certo8_" + k, u"Isso! " + G["r"].capitalize() + u", com letra grande.")
    p("dica8_" + k, u"Escute de novo a frase e pense no nome daquele lugar.")

# ---------- 9 ----------
p("p9enun", u"Folha nove: agora é sobre você. Leia e diga se cada resposta é um "
            u"nome de um só.")
for k, M in MEU.items():
    p("meu_" + k, lp(M["p"]))
    p("certo9_" + k,
      u"Isso! Serve para muitos." if M["r"] == "c"
      else u"Isso! É de um só, e começa com letra grande.")
    p("dica9_" + k, u"Pense: existe mais de um assim no mundo?")

# ---------- 11 ----------
p("p11enun", u"Folha onze: marque as figuras cujo nome tem duas palavras "
             u"juntas. Depois toque em Conferir.")
for k, F2 in FIGC.items():
    p("diz_" + k, F2["n"] + u".")
p("certo11", u"Isso! Couve-flor, beija-flor e guarda-chuva são feitas de duas "
             u"palavras cada uma.")
p("dica11", u"Fale cada nome devagar. Dá para ouvir duas palavras lá dentro?")

# ---------- 12 ----------
p("p12enun", u"Folha doze: junte as duas palavras e forme uma só. Toque nos "
             u"pedaços na ordem certa.")
for k, C in COMPOR.items():
    p("comp_" + k, u"%s mais %s." % (C["a"], C["b"]))
    p("certo12_" + k, u"Isso! " + C["r"] + u".")
    p("dica12_" + k, u"Comece pelo primeiro pedaço, o que vem antes.")

# ---------- 13 ----------
p("p13enun", u"Folha treze: em cada frase há uma palavra feita de duas. Toque "
             u"nela.")
for k, F2 in GRIFA.items():
    p("grifa_" + k, lp(u" ".join(F2["palavras"])))
    p("certo13_" + k, u"Isso! " + F2["alvo"] + u".")
    p("dica13_" + k, u"Procure a palavra com o tracinho no meio.")

# ---------- 14 ----------
p("p14enun", u"Folha catorze: estas palavras estão todas grudadas. Toque entre "
             u"as letras, onde uma acaba e a outra começa.")
for k, G in GRUDA.items():
    # ⚠️ o separador visual da tela é " · "; na VOZ ele vira vírgula, e a
    #    troca crua deixava "GIRASSOL , PORTA-RETRATO" — espaço antes da
    #    pontuação, que o revisor pega e que a voz lê com um soluço no meio.
    _fala = lp(G["certo"]).replace(u" · ", u", ")
    p("gruda_" + k, _fala)
    p("certo14_" + k, u"Isso! " + _fala + u".")
    p("dica14_" + k, u"Leia devagar e pare quando reconhecer uma palavra inteira.")

# ---------- 15 ----------
p("p15enun", u"Folha quinze: toque na palavra e depois no que ela quer dizer.")
for k, S in SIGN.items():
    p("sign_" + k, S["p"] + u".")
    p("sigd_" + k, lp(S["s"]) + u".")
    p("certo15_" + k, u"Isso! %s quer dizer: %s." % (S["p"], lp(S["s"])))
    p("dica15_" + k, u"Pense no que as duas palavras querem dizer juntas.")

# ---------- 16 ----------
p("p16enun", u"Folha dezesseis: olhe as duas figuras. Qual palavra nasceu da "
             u"outra?")
for k, P2 in PARDER.items():
    p("pard_" + k, u"%s e %s." % (P2["a"]["n"], P2["b"]["n"]))
    p("diz_" + ch(P2["a"]["n"]), P2["a"]["n"] + u".")
    p("diz_" + ch(P2["b"]["n"]), P2["b"]["n"] + u".")
    p("certo16_" + k, u"Isso! %s tem %s dentro dela. A palavra-mãe é %s."
                      % (P2["b"]["n"], P2["a"]["n"], P2["a"]["n"]))
    p("dica16_" + k, u"Procure qual das duas está escondida dentro da outra.")

# ---------- 17 ----------
p("p17enun", u"Folha dezessete: escolha a terminação que forma a palavra que a "
             u"frase pede.")
for k, M in MAQ.items():
    p("maq_" + k, lp(M["pede"]))
    p("certo17_" + k, u"Isso! " + M["parte"] + M["r"] + u".")
    p("dica17_" + k, u"Escute a frase de novo: ela diz se é quem faz, o lugar "
                     u"ou a pancada.")

# ---------- 18 ----------
p("p18enun", u"Folha dezoito: à esquerda, a palavra que veio primeiro. À "
             u"direita, a que nasceu dela. Toque numa e depois na outra.")
for k, P2 in PRIM.items():
    p("prim_" + k, P2["p"] + u".")
    p("deri_" + k, P2["d"] + u".")
    p("certo18_" + k, u"Isso! %s nasceu de %s." % (P2["d"], P2["p"]))
    p("dica18_" + k, u"Procure a palavra comprida que tem %s escondida dentro."
                     % P2["p"])

# ---------- 19 ----------
p("p19enun", u"Folha dezenove: esta palavra é filha de outra. De qual ela "
             u"nasceu?")
for k, V in VEIO.items():
    p("veio_" + k, V["d"] + u".")
    for w in V["o"]:
        p("diz_" + ch(w), w + u".")
    p("certo19_" + k, u"Isso! %s nasceu de %s." % (V["d"], V["r"]))
    p("dica19_" + k, u"Tire a terminação de %s e veja que palavra sobra." % V["d"])

# ---------- 20 ----------
p("p20enun", u"Folha vinte: escolha uma cor e pinte a palavra-mãe e as filhas "
             u"dela. Depois pegue outra cor.")
for k, F2 in FAM.items():
    p("fam_" + k, u"A família de %s." % F2["n"])
    p("certo20_" + k, u"Isso! É da família de %s." % F2["n"])
    p("dica20_" + k, u"Esta não é da família que você está pintando. Procure a "
                     u"palavra-mãe escondida dentro dela.")
    for w in F2["palavras"]:
        p("diz_" + ch(w), w.capitalize() + u".")

# ---------- 21 ----------
p("p21enun", u"Folha vinte e um: escolha a marca e toque na palavra. A que veio "
             u"primeiro, ou a que nasceu dela.")
for k, F2 in DUPLA.items():
    p("dupla_" + k, lp(u" ".join(F2["palavras"])))
    p("certo21_%s_p" % k, u"Isso! %s veio primeiro." % F2["prim"])
    p("certo21_%s_d" % k, u"Isso! %s nasceu de %s." % (F2["deri"], F2["prim"]))
    p("dica21_" + k, u"Uma das duas é mais curta e está dentro da outra: essa "
                     u"veio primeiro.")

# ---------- 22 ----------
p("p22enun", u"Folha vinte e dois: três destas palavras combinam entre si e uma "
             u"não. Ache a intrusa.")
for k, I in INTRUSA.items():
    p("intr_" + k, u", ".join(I["g"]) + u".")
    for w in I["g"]:
        p("diz_" + ch(w), w + u".")
    p("certo22_" + k, u"Isso! " + lp(I["pq"]))
    p("dica22_" + k, u"Olhe as quatro e pergunte: o que três delas têm que a "
                     u"quarta não tem?")

# ---------- 23 ----------
p("p23enun", u"Folha vinte e três: cada grupo tem um nome só. Toque no grupo e "
             u"depois no nome dele.")
for k, C in COLE.items():
    p("grupo_" + k, lp(C["g"]) + u".")
    p("cole_" + k, C["c"] + u".")
    p("certo23_" + k, u"Isso! %s é o nome de %s." % (C["c"].capitalize(), lp(C["g"])))
    p("dica23_" + k, u"Este nome é de outro grupo. Escute os dois de novo.")

# ---------- 24 ----------
p("p24enun", u"Folha vinte e quatro: agora responda sobre a história.")
for k, T in TEXTO.items():
    p("hist_" + k, lp(T["corpo"]))
    for i, P2 in enumerate(T["perg"]):
        p("perg_%s_%d" % (k, i), lp(P2["q"]))
        for j, o in enumerate(P2["o"]):
            p("resp_%s_%d_%d" % (k, i, j), lp(o) + u".")
        p("certo24_%d" % i, u"Isso! " + lp(P2.get("pq", u"")))
        p("dica24_%d" % i, u"Volte na história e leia de novo essa parte.")

# ---------- 25 ----------
p("p25enun", u"Folha vinte e cinco: escolha as regras que você quer no seu "
             u"cartaz. Pode escolher quantas quiser.")
for k, C in CARTAZ.items():
    p("certo25_" + k, lp(C["t"]) + u". Por exemplo: " + lp(C["ex"]) + u".")



# ---------------------------------------------------------------------------
# A SAÍDA
# ---------------------------------------------------------------------------
def chave(s):
    u"""O nome do mp3 sai do TEXTO, não da chave da fala — assim duas chaves que
    dizem a mesma frase gravam um arquivo só."""
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for c in s:
        hh = ((hh * 33) ^ ord(c)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    txt = F[k]
    if not txt:
        continue
    c = chave(txt)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": txt, u"voz": VOZ})

html = io.open(CAM, encoding=u"utf-8").read()
blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)
io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
print(u"FALAS: %d chaves; falas.json: %d fala(s) para gravar" % (len(F), len(falas)))
