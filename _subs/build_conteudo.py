# -*- coding: utf-8 -*-
u"""Gera _subs/conteudo.json — AS PLAQUINHAS DA DONA CORUJA (2º ano, Português).
    Diferenciar SUBSTANTIVO PRÓPRIO × COMUM.  (VERSÃO LONGA)

ENREDO (EDUVERSE): a Dona Coruja tem uma lojinha de PLAQUINHAS. Toda coisa tem
um nome COMUM (cachorro, cidade, menina) — serve para qualquer um. Quando é UMA
só e querida, ganha nome PRÓPRIO, com LETRA GRANDE (Rex, Blumenau, Ana).

⭐ MAIS TEMPO / REPETIÇÃO SEGUIDA (pedido do Marcos, ago/2026: "para a atividade
   levar mais tempo" + "repetição de umas 4 vezes cada na sequência"): cada
   dinâmica vem num BLOCO com ~4 rodadas seguidas, subindo um degrau. Aquecimento
   no meio (revisão). Fecho com caça-palavras.

REGRA-CHAVE (2º ano, concreto → símbolo):
  · COMUM  = nomeia QUALQUER um do mesmo tipo.
  · PRÓPRIO = nomeia UM só, começa com LETRA MAIÚSCULA.
"""
import io, json, os
PASTA = os.path.dirname(os.path.abspath(__file__))

HAB = (u"Diferenciar substantivos COMUNS de PRÓPRIOS e empregar a LETRA MAIÚSCULA "
       u"no início dos nomes próprios (pessoas, lugares, animais de estimação). EF02LP (2º ano).")

CONTEUDO = {
 u"titulo": u"As Plaquinhas do Téo",
 u"sub": u"Português · 2º ano · Substantivos próprios e comuns",
 u"ano": u"2º ano",
 u"prefixo": u"sn",
 u"mascote": u"castor",
 u"mascoteNome": u"Téo",
 u"crachas": 6,
 u"mesa": u"Pedagogo do 2º ano + especialista em Língua Portuguesa (alfabetização).",
 u"fundo": u"sn_fundo.png",
 u"voz": u"feminina",
 u"abertura": (u"Oi! Eu sou o Téo, o castor, e faço as plaquinhas desta loja. "
              u"Cada coisa tem um nome. Vamos descobrir quando o nome é de QUALQUER "
              u"um e quando é de UM só? Vem comigo!"),
 u"fim": (u"Que caprichado! Você já sabe: o nome COMUM é de qualquer um, e o nome "
          u"PRÓPRIO é de UM só, com letra grande. Você é o melhor ajudante da loja!"),
 u"conceitos": {
   u"objetivo1": u"Substantivo COMUM (nomeia qualquer um)",
   u"objetivo2": u"Substantivo PRÓPRIO (nomeia UM; letra maiúscula)",
   u"objetivo3": u"Diferenciar próprio × comum e usar a maiúscula",
 },
 u"curriculo": {
   u"objetivo1": u"Reconhecer o substantivo COMUM: nomeia qualquer ser de uma mesma classe. EF02LP (2º ano).",
   u"objetivo2": u"Reconhecer o substantivo PRÓPRIO: nomeia UM ser e começa com LETRA MAIÚSCULA. EF02LP (2º ano).",
   u"objetivo3": u"Diferenciar próprio × comum e empregar a maiúscula no início do nome próprio. EF02LP (2º ano).",
 },
 u"fases": [],
}
fases = []
def add(**k): fases.append(k)

def esc(img, p, c, cvoz, erradas, dicas, cimg=None, eimgs=None):
    cop = {u"t": c, u"voz": cvoz}
    if cimg: cop[u"img"] = cimg
    es = []
    for i,(t,v) in enumerate(erradas):
        o={u"t":t, u"voz":v}
        if eimgs and i<len(eimgs) and eimgs[i]: o[u"img"]=eimgs[i]
        es.append(o)
    return {u"img":img, u"p":p, u"c":cop, u"e":es, u"d":dicas}

D_COM = [u"O nome comum serve para QUALQUER um do tipo.",
         u"Nome de um só, com letra grande, é próprio; o do tipo é comum.",
         u"Isso! Esse é o nome <b>comum</b>. Toque para seguir."]
D_PRO = [u"O nome próprio é de UM só e começa com letra GRANDE.",
         u"Os outros servem para qualquer um; só este é de um só.",
         u"Isso! Esse é o nome <b>próprio</b>. Toque para seguir."]

# ============================================================
# BLOCO 1 — ESCOLHER (f01 comum, f02 próprio) — 4 rodadas cada
# ============================================================
add(id=u"f01", mec=u"escolher", selo=u"NOME DE QUALQUER UM", conceito=u"objetivo1",
    enunciado=u"O nome <b>comum</b> serve para <b>qualquer um</b>. Ache o nome comum.",
    dica=u"Comum é o nome do tipo da coisa, não de um só.",
    dados=[
     esc(u"sn_cachorro", u"Qual palavra nomeia <b>qualquer</b> um deles?",
         u"CACHORRO", u"cachorro", [(u"REX", u"rex"), (u"BIDU", u"bidu")], D_COM),
     esc(u"sn_gato", u"E qual palavra vale para <b>qualquer</b> gato?",
         u"GATO", u"gato", [(u"MIMI", u"mimi"), (u"NINA", u"nina")], D_COM),
     esc(u"", u"Qual palavra serve para <b>qualquer</b> uma?",
         u"MENINA", u"menina", [(u"LIA", u"lia"), (u"DUDA", u"duda")], D_COM),
     esc(u"", u"Qual palavra vale para <b>qualquer</b> lugar assim?",
         u"CIDADE", u"cidade", [(u"BLUMENAU", u"blumenau"), (u"BRASIL", u"brasil")], D_COM),
    ])

add(id=u"f02", mec=u"escolher", selo=u"NOME DE UM SÓ", conceito=u"objetivo2",
    enunciado=u"O nome <b>próprio</b> é de <b>um só</b> e começa com <b>letra grande</b>.",
    dica=u"Procure a palavra que começa com letra MAIÚSCULA.",
    dados=[
     esc(u"sn_menina", u"Qual é o nome <b>próprio</b> da menina?",
         u"DUDA", u"duda", [(u"menina", u"menina"), (u"amiga", u"amiga")], D_PRO),
     esc(u"sn_menino", u"Qual é o nome <b>próprio</b> do menino?",
         u"BENTO", u"bento", [(u"menino", u"menino"), (u"colega", u"colega")], D_PRO),
     esc(u"sn_cidade", u"Qual é o nome <b>próprio</b> de uma cidade?",
         u"BLUMENAU", u"blumenau", [(u"cidade", u"cidade"), (u"lugar", u"lugar")], D_PRO),
     esc(u"sn_papagaio", u"Qual é o nome <b>próprio</b> do papagaio?",
         u"LOURO", u"louro", [(u"papagaio", u"papagaio"), (u"ave", u"ave")], D_PRO),
    ])

# ============================================================
# BLOCO 2 — LIGAR (f03 próprio, f04 comum) — 4 pares cada
# ============================================================
add(id=u"f03", mec=u"ligar", selo=u"DÊ UM NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"Ligue cada bichinho ao seu <b>nome próprio</b> (com letra grande).",
    dica=u"O nome próprio começa com letra MAIÚSCULA.",
    dados=[{u"k":u"n0", u"img":u"sn_cachorro", u"voz":u"cachorro", u"s":u"REX"},
           {u"k":u"n1", u"img":u"sn_gato",     u"voz":u"gato",     u"s":u"MIMI"},
           {u"k":u"n2", u"img":u"sn_papagaio", u"voz":u"papagaio", u"s":u"LOURO"},
           {u"k":u"n3", u"img":u"sn_menino",   u"voz":u"menino",   u"s":u"BENTO"}],
    dadosExtra={u"ENUN":u"Ligue cada bichinho ao seu <b>nome próprio</b> (com letra grande).",
                u"DICAS":[u"O nome próprio começa com letra MAIÚSCULA.",
                          u"Rex é o cachorro, Mimi é a gata, Louro é o papagaio, Bento é o menino."],
                u"FECHO":u"Você deu um nome próprio para cada um!"})

add(id=u"f04", mec=u"ligar", selo=u"QUAL É O NOME COMUM?", conceito=u"objetivo1",
    enunciado=u"Ligue cada figura ao seu <b>nome comum</b>.",
    dica=u"O nome comum é o tipo da coisa: o que é isso?",
    dados=[{u"k":u"c0", u"img":u"sn_casa",   u"voz":u"casa",   u"s":u"CASA"},
           {u"k":u"c1", u"img":u"sn_bola",   u"voz":u"bola",   u"s":u"BOLA"},
           {u"k":u"c2", u"img":u"sn_arvore", u"voz":u"árvore", u"s":u"ÁRVORE"},
           {u"k":u"c3", u"img":u"sn_cidade", u"voz":u"cidade", u"s":u"CIDADE"}],
    dadosExtra={u"ENUN":u"Ligue cada figura ao seu <b>nome comum</b>.",
                u"DICAS":[u"O nome comum é o tipo da coisa.",
                          u"Pergunte: o que é isso? Casa, bola, árvore, cidade."],
                u"FECHO":u"Você nomeou cada coisa!"})

# ============================================================
# BLOCO 3 — CLASSIFICAR (f05, f06) — 6 fichas cada
# ============================================================
def classif(idf, fichas):
    return dict(id=idf, mec=u"classificar", selo=u"SEPARE AS PLAQUINHAS", conceito=u"objetivo3",
      enunciado=u"Cada plaquinha na sua caixa: é nome <b>PRÓPRIO</b> ou <b>COMUM</b>?",
      dica=u"Letra grande e de um só? Próprio. Serve para qualquer um? Comum.",
      dados=[{u"k":u"pro", u"n":u"PRÓPRIO", u"img":u"", u"voz":u"próprio", u"rot":False},
             {u"k":u"com", u"n":u"COMUM",   u"img":u"", u"voz":u"comum",   u"rot":False}],
      dadosExtra={u"ENUN":u"Cada plaquinha na sua caixa: é nome <b>PRÓPRIO</b> ou <b>COMUM</b>?",
                  u"FICHAS":fichas,
                  u"DICAS":[u"Olhe a primeira letra: grande costuma ser próprio.",
                            u"Nome de um só é próprio; nome do tipo é comum.",
                            u"Boa! Você separou certinho. Toque para seguir."]})
add(**classif(u"f05", [{u"t":u"Gael",u"alvo":u"pro"},{u"t":u"menina",u"alvo":u"com"},
                       {u"t":u"Rex",u"alvo":u"pro"},{u"t":u"cachorro",u"alvo":u"com"},
                       {u"t":u"Blumenau",u"alvo":u"pro"},{u"t":u"cidade",u"alvo":u"com"}]))
add(**classif(u"f06", [{u"t":u"Brasil",u"alvo":u"pro"},{u"t":u"país",u"alvo":u"com"},
                       {u"t":u"Maria",u"alvo":u"pro"},{u"t":u"professora",u"alvo":u"com"},
                       {u"t":u"Louro",u"alvo":u"pro"},{u"t":u"papagaio",u"alvo":u"com"}]))

# ============================================================
# AQUECIMENTO (revisão) — escolher, no meio
# ============================================================
add(id=u"aquecimento", mec=u"escolher", selo=u"AQUECIMENTO", conceito=u"objetivo1",
    enunciado=u"Vamos lembrar: qual é o nome <b>comum</b>?",
    dica=u"Comum serve para qualquer um.",
    dados=[
     esc(u"sn_gato", u"Qual palavra serve para <b>qualquer</b> gato?",
         u"GATO", u"gato", [(u"MIMI", u"mimi"), (u"NINA", u"nina")], D_COM),
     esc(u"sn_casa", u"Qual palavra vale para <b>qualquer</b> uma?",
         u"CASA", u"casa", [(u"BLUMENAU", u"blumenau"), (u"BRASIL", u"brasil")], D_COM),
     esc(u"", u"Qual é o nome <b>comum</b>?",
         u"MENINO", u"menino", [(u"BENTO", u"bento"), (u"PEDRO", u"pedro")], D_COM),
    ])

# ============================================================
# BLOCO 4 — COMPLETAR (f07 bicho/pessoa, f08 lugar) — a letra grande
# ============================================================
add(id=u"f07", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"Todo nome próprio começa com <b>letra maiúscula</b>. Escolha o certo.",
    dica=u"Só a PRIMEIRA letra é grande.",
    dados=[{u"img":u"", u"ante":u"O cachorro se chama ", u"dep":u".", u"cer":u"Rex", u"out":[u"rex", u"REX"], u"dic":u"Só o R é grande: Rex."},
           {u"img":u"", u"ante":u"A menina se chama ",   u"dep":u".", u"cer":u"Lia", u"out":[u"lia", u"LIA"], u"dic":u"Só o L é grande: Lia."},
           {u"img":u"", u"ante":u"A gata se chama ",      u"dep":u".", u"cer":u"Mimi", u"out":[u"mimi", u"MIMI"], u"dic":u"Só o M é grande: Mimi."},
           {u"img":u"", u"ante":u"O menino se chama ",    u"dep":u".", u"cer":u"Bento", u"out":[u"bento", u"BENTO"], u"dic":u"Só o B é grande: Bento."}],
    dadosExtra={u"ENUN":u"Todo nome próprio começa com <b>letra maiúscula</b>. Escolha o certo.",
                u"FECHO":u"Você acertou a letra grande em todos!"})

add(id=u"f08", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"Preencha o nome do lugar do jeito <b>certo</b>.",
    dica=u"Cidade e país são nomes próprios: letra grande.",
    dados=[{u"img":u"", u"ante":u"Eu moro em ", u"dep":u".", u"cer":u"Blumenau", u"out":[u"blumenau", u"BLUMENAU"], u"dic":u"Só o B é grande: Blumenau."},
           {u"img":u"", u"ante":u"Eu vivo no ", u"dep":u".", u"cer":u"Brasil", u"out":[u"brasil", u"BRASIL"], u"dic":u"Só o B é grande: Brasil."},
           {u"img":u"", u"ante":u"Minha amiga é a ", u"dep":u".", u"cer":u"Maria", u"out":[u"maria", u"MARIA"], u"dic":u"Só o M é grande: Maria."}],
    dadosExtra={u"ENUN":u"Preencha o nome do lugar do jeito <b>certo</b>.",
                u"FECHO":u"Isso! Nome de lugar e de pessoa é próprio."})

# ============================================================
# BLOCO 5 — DIGITAR (f09 bicho, f10 lugar)
# ============================================================
add(id=u"f09", mec=u"digitar", selo=u"ESCREVA O NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"Escreva o <b>nome próprio</b> do bichinho, letra por letra.",
    dica=u"Nome próprio de bicho de estimação é escrito com letra grande.",
    dados=[{u"palavra":u"BENTO", u"img":u"", u"voz":u"bento", u"pista":u"O nome do menino da história. Escreva: Bento.", u"dic":u"Nome próprio: <b>Bento</b>."},
           {u"palavra":u"MIMI", u"img":u"", u"voz":u"mimi", u"pista":u"O nome da gata. Escreva: Mimi.", u"dic":u"Nome próprio: <b>Mimi</b>."},
           {u"palavra":u"REX", u"img":u"", u"voz":u"rex", u"pista":u"O nome do cachorro. Escreva: Rex.", u"dic":u"Nome próprio: <b>Rex</b>."},
           {u"palavra":u"LOURO", u"img":u"", u"voz":u"louro", u"pista":u"O nome do papagaio. Escreva: Louro.", u"dic":u"Nome próprio: <b>Louro</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>nome próprio</b> do bichinho, letra por letra.",
                u"FECHO":u"Você escreveu os nomes próprios!"})

add(id=u"f10", mec=u"digitar", selo=u"ESCREVA O NOME DO LUGAR", conceito=u"objetivo3",
    enunciado=u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
    dica=u"Nome de cidade e de país é próprio.",
    dados=[{u"palavra":u"BLUMENAU", u"img":u"", u"voz":u"blumenau", u"pista":u"A cidade da nossa escola. Escreva: Blumenau.", u"dic":u"Nome próprio: <b>Blumenau</b>."},
           {u"palavra":u"BRASIL", u"img":u"", u"voz":u"brasil", u"pista":u"O nosso país. Escreva: Brasil.", u"dic":u"Nome próprio: <b>Brasil</b>."}],
    dadosExtra={u"ENUN":u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
                u"FECHO":u"Muito bem! Nome de lugar é próprio."})

# ============================================================
# QUEM-SOU-EU (f11) — 4 rodadas
# ============================================================
add(id=u"f11", mec=u"quem-sou-eu", selo=u"ADIVINHE O NOME", conceito=u"objetivo2",
    enunciado=u"Ouça as pistas e ache o <b>nome próprio</b>.",
    dica=u"Pense no que é de UM só e começa com letra grande.",
    dados=[
     {u"resp":u"BLUMENAU", u"pistas":[u"Sou o nome de uma <b>cidade</b>.", u"Começo com <b>letra grande</b>.", u"Sou a cidade da nossa <b>escola</b>."], u"outros":[u"CIDADE", u"LUGAR", u"RUA"]},
     {u"resp":u"REX", u"pistas":[u"Sou o nome de um <b>cachorro</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UM cachorro só."], u"outros":[u"CACHORRO", u"BICHO", u"AMIGO"]},
     {u"resp":u"BRASIL", u"pistas":[u"Sou o nome de um <b>país</b>.", u"Começo com <b>letra grande</b>.", u"É o país onde a gente mora."], u"outros":[u"PAÍS", u"LUGAR", u"MUNDO"]},
     {u"resp":u"DUDA", u"pistas":[u"Sou o nome de uma <b>menina</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UMA menina só."], u"outros":[u"MENINA", u"AMIGA", u"COLEGA"]},
    ])

# ============================================================
# INTRUSO (f12) — 4 rodadas (ache o COMUM)
# ============================================================
def intruso(idf, itens, fora, nomeFora, d2):
    return dict(id=idf, mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo1",
      enunciado=u"Três são nomes <b>próprios</b>. Ache o que NÃO é (o comum).",
      dica=u"O intruso serve para qualquer um e começa com letra pequena.",
      dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
              u"enun":u"Três são nomes <b>próprios</b>. Qual NÃO é (o comum)?",
              u"itens":[{u"k":k, u"n":n} for k,n in itens],
              u"fora":fora, u"nomeFora":nomeFora,
              u"d1":u"Um dos nomes serve para qualquer um — ache esse.",
              u"d2":d2,
              u"d3":u"O de fora é <b>%s</b>: é nome comum, serve para qualquer um."%nomeFora,
              u"razoes":[{u"t":u"É comum: serve para qualquer um; os outros são de um só.", u"ok":1},
                         {u"t":u"Porque é a palavra mais curta.", u"ok":0},
                         {u"t":u"Porque começa com essa letra.", u"ok":0}],
              u"enunPorque":u"Por que <b>%s</b> é diferente dos outros? Toque na razão certa."%nomeFora,
              u"p1":u"Olhe o que os OUTROS três têm em comum.",
              u"p2":u"O tamanho não importa; pense se é de um só ou de qualquer um.",
              u"p3":u"A letra não importa; pense no que o nome nomeia."}])
add(**intruso(u"f12", [(u"a",u"Gael"),(u"b",u"Rex"),(u"c",u"Blumenau"),(u"d",u"menino")], u"d", u"menino",
              u"Gael, Rex e Blumenau começam com letra grande; menino, não."))

# ============================================================
# CAÇA-PALAVRAS (fecho) — nomes próprios
# ============================================================
add(id=u"f13", mec=u"caca-palavras", selo=u"CAÇA AOS NOMES PRÓPRIOS", conceito=u"objetivo2",
    enunciado=u"Ache os <b>nomes próprios</b> escondidos no quadro. Eles têm letra grande!",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"LIA", u"REX", u"MIMI", u"BENTO", u"BRASIL"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"OS NOMES PRÓPRIOS",
                u"LETRAS":u"ABEILMNORSTUX", u"DIFICIL":u"",
                u"CORP":[u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
CONTEUDO[u"fases"] = fases
CONTEUDO[u"habilidades"] = HAB
with io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8") as f:
    f.write(json.dumps(CONTEUDO, ensure_ascii=False, indent=1))

nr = sum(len(x.get("dados")) if isinstance(x.get("dados"), list) else 1 for x in fases)
print(u"conteudo.json: %d fases, ~%d rodadas (%s)" % (len(fases), nr, CONTEUDO[u"titulo"]))
g={}; o={}
for x in fases:
    g[x[u"mec"]]=g.get(x[u"mec"],0)+1
    o[x[u"conceito"]]=o.get(x[u"conceito"],0)+1
print(u"gestos:", g); print(u"objetivos:", o)
