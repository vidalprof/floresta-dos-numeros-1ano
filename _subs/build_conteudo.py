# -*- coding: utf-8 -*-
u"""Gera _subs/conteudo.json — AS PLAQUINHAS DA DONA CORUJA (2º ano, Português).
    Diferenciar SUBSTANTIVO PRÓPRIO × COMUM.

ENREDO (o "porquê" — EDUVERSE): a Dona Coruja tem uma lojinha de PLAQUINHAS.
Toda coisa tem um nome COMUM (cachorro, cidade, menina) — serve para qualquer um.
Mas quando a coisa é UMA só e querida, ela ganha um nome PRÓPRIO, escrito com
LETRA GRANDE (Rex, Blumenau, Ana). A criança ajuda a Coruja a fazer e separar as
plaquinhas. O problema (dar nome) vem ANTES da regra; a gramática é a ferramenta.

REGRA-CHAVE (2º ano, concreto → símbolo):
  · COMUM  = nomeia QUALQUER um do mesmo tipo (um cachorro, uma cidade).
  · PRÓPRIO = nomeia UM só, e começa com LETRA MAIÚSCULA (Rex, Blumenau, Ana).

⭐ REPETIÇÃO SEGUIDA (RECEITA.md): cada gesto em BLOCO contíguo. Aquecimento no
meio (revisão). Fecho com gancho (uma plaquinha nova na caixa de correio).

PIPELINE: build → integrar --escrever → montar.py _subs → ARTE (prompts p/ Marcos)
→ voz → banca → publicar.
"""
import io, json, os
PASTA = os.path.dirname(os.path.abspath(__file__))

HAB = (u"Diferenciar substantivos COMUNS (nomeiam qualquer ser de uma classe) de "
       u"substantivos PRÓPRIOS (nomeiam um ser específico), e empregar a LETRA "
       u"MAIÚSCULA no início dos nomes próprios (pessoas, lugares, animais de "
       u"estimação). EF02LP (2º ano).")

CONTEUDO = {
 u"titulo": u"As Plaquinhas da Dona Coruja",
 u"sub": u"Português · 2º ano · Substantivos próprios e comuns",
 u"ano": u"2º ano",
 u"prefixo": u"sn",
 u"mascote": u"coruja",
 u"mascoteNome": u"Dona Coruja",
 u"crachas": 6,
 u"mesa": u"Pedagogo do 2º ano + especialista em Língua Portuguesa (alfabetização).",
 u"fundo": u"sn_fundo.png",
 u"voz": u"feminina",
 u"abertura": (u"Oi! Eu sou a Dona Coruja e esta é a minha loja de plaquinhas. "
              u"Cada coisa tem um nome. Vamos descobrir juntos quando o nome é de "
              u"QUALQUER um e quando é de UM só? Vem comigo!"),
 u"fim": (u"Que caprichado! Você já sabe: o nome COMUM é de qualquer um, e o nome "
          u"PRÓPRIO é de UM só, com letra grande. A Dona Coruja te dá a plaquinha "
          u"de melhor ajudante!"),
 u"conceitos": {
   u"objetivo1": u"Substantivo COMUM (nomeia qualquer um)",
   u"objetivo2": u"Substantivo PRÓPRIO (nomeia UM; letra maiúscula)",
   u"objetivo3": u"Diferenciar próprio × comum e usar a maiúscula",
 },
 u"curriculo": {
   u"objetivo1": u"Reconhecer o substantivo COMUM: nomeia qualquer ser de uma mesma classe (cachorro, cidade, menina). EF02LP (2º ano).",
   u"objetivo2": u"Reconhecer o substantivo PRÓPRIO: nomeia UM ser específico e começa com LETRA MAIÚSCULA (Rex, Blumenau, Ana). EF02LP (2º ano).",
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

# ============================================================
# BLOCO 1 — ESCOLHER (f01, f02, f03)
# ============================================================
add(id=u"f01", mec=u"escolher", selo=u"NOME DE QUALQUER UM", conceito=u"objetivo1",
    enunciado=u"O nome <b>comum</b> serve para <b>qualquer um</b>. Qual destes é um nome comum?",
    dica=u"Comum é o nome do tipo da coisa, não de um só.",
    dados=[esc(u"sn_cachorro",
      u"Qual palavra nomeia <b>qualquer</b> um deles?",
      u"CACHORRO", u"cachorro",
      [(u"REX", u"rex"), (u"BIDU", u"bidu")],
      [u"Pense no nome que vale para todos os cachorros.",
       u"Rex e Bidu são de UM só; cachorro é de qualquer um.",
       u"Isso! <b>Cachorro</b> é o nome comum. Toque para seguir."])])

add(id=u"f02", mec=u"escolher", selo=u"NOME DE UM SÓ", conceito=u"objetivo2",
    enunciado=u"O nome <b>próprio</b> é de <b>um só</b> e começa com <b>letra grande</b>.",
    dica=u"Procure a palavra que começa com letra MAIÚSCULA.",
    dados=[esc(u"sn_menina",
      u"Qual é o nome <b>próprio</b> da menina?",
      u"ANA", u"ana",
      [(u"menina", u"menina"), (u"amiga", u"amiga")],
      [u"O nome próprio começa com letra GRANDE.",
       u"Menina e amiga servem para qualquer uma; Ana é de UMA só.",
       u"Isso! <b>Ana</b> é o nome próprio. Toque para seguir."])])

add(id=u"f03", mec=u"escolher", selo=u"NOME DE UM SÓ", conceito=u"objetivo2",
    enunciado=u"Ache o nome <b>próprio</b> (de um só, com letra grande).",
    dica=u"Cidade é de qualquer uma; o nome da SUA cidade é próprio.",
    dados=[esc(u"sn_cidade",
      u"Qual é o nome <b>próprio</b> de uma cidade?",
      u"BLUMENAU", u"blumenau",
      [(u"cidade", u"cidade"), (u"lugar", u"lugar")],
      [u"O nome próprio da cidade começa com letra GRANDE.",
       u"Cidade e lugar são de qualquer uma; Blumenau é de UMA só.",
       u"Isso! <b>Blumenau</b> é nome próprio. Toque para seguir."])])

# ============================================================
# BLOCO 2 — LIGAR (f04, f05)
# ============================================================
# f04: a figura (comum) <-> o nome PRÓPRIO dela
add(id=u"f04", mec=u"ligar", selo=u"DÊ UM NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"Ligue cada bichinho ao seu <b>nome próprio</b> (com letra grande).",
    dica=u"Cada plaquinha de nome próprio começa com letra MAIÚSCULA.",
    dados=[{u"k":u"n0", u"img":u"sn_cachorro", u"voz":u"cachorro", u"s":u"REX"},
           {u"k":u"n1", u"img":u"sn_gato",     u"voz":u"gato",     u"s":u"MIMI"},
           {u"k":u"n2", u"img":u"sn_papagaio", u"voz":u"papagaio", u"s":u"LOURO"},
           {u"k":u"n3", u"img":u"sn_menino",   u"voz":u"menino",   u"s":u"BENTO"}],
    dadosExtra={u"ENUN":u"Ligue cada bichinho ao seu <b>nome próprio</b> (com letra grande).",
                u"DICAS":[u"O nome próprio começa com letra MAIÚSCULA.",
                          u"Rex é o cachorro, Mimi é a gata, Louro é o papagaio, Bento é o menino."],
                u"FECHO":u"Você deu um nome próprio para cada um!"})

# f05: a figura <-> o nome COMUM dela
add(id=u"f05", mec=u"ligar", selo=u"QUAL É O NOME COMUM?", conceito=u"objetivo1",
    enunciado=u"Ligue cada figura ao seu <b>nome comum</b>.",
    dica=u"O nome comum é o tipo da coisa: o que é isso?",
    dados=[{u"k":u"c0", u"img":u"sn_casa",   u"voz":u"casa",   u"s":u"CASA"},
           {u"k":u"c1", u"img":u"sn_bola",   u"voz":u"bola",   u"s":u"BOLA"},
           {u"k":u"c2", u"img":u"sn_gato",   u"voz":u"gato",   u"s":u"GATO"},
           {u"k":u"c3", u"img":u"sn_arvore", u"voz":u"árvore", u"s":u"ÁRVORE"}],
    dadosExtra={u"ENUN":u"Ligue cada figura ao seu <b>nome comum</b>.",
                u"DICAS":[u"O nome comum é o tipo da coisa.",
                          u"Pergunte: o que é isso? Casa, bola, gato, árvore."],
                u"FECHO":u"Você nomeou cada coisa!"})

# ============================================================
# BLOCO 3 — CLASSIFICAR (f06, f07)
# ============================================================
add(id=u"f06", mec=u"classificar", selo=u"SEPARE AS PLAQUINHAS", conceito=u"objetivo3",
    enunciado=u"Cada plaquinha na sua caixa: é nome <b>PRÓPRIO</b> ou <b>COMUM</b>?",
    dica=u"Começa com letra grande e é de um só? Próprio. Serve para qualquer um? Comum.",
    dados=[{u"k":u"pro", u"n":u"PRÓPRIO", u"img":u"", u"voz":u"próprio", u"rot":False},
           {u"k":u"com", u"n":u"COMUM",   u"img":u"", u"voz":u"comum",   u"rot":False}],
    dadosExtra={
      u"FICHAS":[{u"t":u"Ana",       u"alvo":u"pro"},
                 {u"t":u"menina",    u"alvo":u"com"},
                 {u"t":u"Rex",       u"alvo":u"pro"},
                 {u"t":u"cachorro",  u"alvo":u"com"},
                 {u"t":u"Blumenau",  u"alvo":u"pro"},
                 {u"t":u"cidade",    u"alvo":u"com"}],
      u"ENUN":u"Cada plaquinha na sua caixa: é nome <b>PRÓPRIO</b> ou <b>COMUM</b>?",
      u"DICAS":[u"Olhe a primeira letra: grande costuma ser próprio.",
                u"Ana, Rex e Blumenau são de UM só; menina, cachorro e cidade são de qualquer um.",
                u"Boa! Você separou as plaquinhas certinho. Toque para seguir."],
    })

add(id=u"f07", mec=u"classificar", selo=u"SEPARE AS PLAQUINHAS", conceito=u"objetivo3",
    enunciado=u"De novo: cada nome na sua caixa, <b>PRÓPRIO</b> ou <b>COMUM</b>?",
    dica=u"Nome de país, de pessoa e de bicho de estimação é próprio (letra grande).",
    dados=[{u"k":u"pro", u"n":u"PRÓPRIO", u"img":u"", u"voz":u"próprio", u"rot":False},
           {u"k":u"com", u"n":u"COMUM",   u"img":u"", u"voz":u"comum",   u"rot":False}],
    dadosExtra={
      u"FICHAS":[{u"t":u"Brasil",     u"alvo":u"pro"},
                 {u"t":u"país",       u"alvo":u"com"},
                 {u"t":u"Maria",      u"alvo":u"pro"},
                 {u"t":u"professora", u"alvo":u"com"},
                 {u"t":u"Louro",      u"alvo":u"pro"},
                 {u"t":u"papagaio",   u"alvo":u"com"}],
      u"ENUN":u"De novo: cada nome na sua caixa, <b>PRÓPRIO</b> ou <b>COMUM</b>?",
      u"DICAS":[u"País e professora servem para qualquer um; Brasil e Maria, não.",
                u"Brasil, Maria e Louro são de UM só, com letra grande.",
                u"Isso! Toque para seguir."],
    })

# ============================================================
# AQUECIMENTO (revisão espaçada) — escolher, no meio
# ============================================================
add(id=u"aquecimento", mec=u"escolher", selo=u"AQUECIMENTO", conceito=u"objetivo1",
    enunciado=u"Vamos lembrar: qual é o nome <b>comum</b>?",
    dica=u"Comum serve para qualquer um.",
    dados=[esc(u"sn_gato",
      u"Qual palavra serve para <b>qualquer</b> gato?",
      u"GATO", u"gato",
      [(u"MIMI", u"mimi"), (u"FROU-FROU", u"frou frou")],
      [u"Pense no nome do tipo do bicho.",
       u"Mimi e Frou-Frou são de um gato só; gato é de qualquer um.",
       u"Isso! <b>Gato</b> é comum. Toque para seguir."])])

# ============================================================
# BLOCO 4 — COMPLETAR (f08, f09)  — a letra maiúscula do próprio
# ============================================================
add(id=u"f08", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo2",
    enunciado=u"Todo nome próprio começa com <b>letra maiúscula</b>. Escolha o certo.",
    dica=u"Só a PRIMEIRA letra é grande.",
    dados=[{u"img":u"", u"ante":u"O cachorro se chama ", u"dep":u".",
            u"cer":u"Rex", u"out":[u"rex", u"REX"],
            u"dic":u"Nome próprio: só o R é grande."},
           {u"img":u"", u"ante":u"A menina se chama ", u"dep":u".",
            u"cer":u"Ana", u"out":[u"ana", u"ANA"],
            u"dic":u"Só a primeira letra é maiúscula: Ana."}],
    dadosExtra={u"ENUN":u"Todo nome próprio começa com <b>letra maiúscula</b>. Escolha o certo.",
                u"FECHO":u"Você escolheu os nomes com a letra grande no lugar certo!"})

add(id=u"f09", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"Preencha com o nome do lugar do jeito <b>certo</b>.",
    dica=u"Cidade e país são nomes próprios: começam com letra grande.",
    dados=[{u"img":u"", u"ante":u"Eu moro em ", u"dep":u".",
            u"cer":u"Blumenau", u"out":[u"blumenau", u"BLUMENAU"],
            u"dic":u"Nome de cidade: só o B é grande."},
           {u"img":u"", u"ante":u"Eu vivo no ", u"dep":u".",
            u"cer":u"Brasil", u"out":[u"brasil", u"BRASIL"],
            u"dic":u"Nome de país: só o B é grande."}],
    dadosExtra={u"ENUN":u"Preencha com o nome do lugar do jeito <b>certo</b>.",
                u"FECHO":u"Isso! Cidade e país são nomes próprios."})

# ============================================================
# BLOCO 5 — DIGITAR (f10, f11)  — as duas portas (tela e teclado)
# ============================================================
add(id=u"f10", mec=u"digitar", selo=u"ESCREVA O NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"Escreva o <b>nome próprio</b> do bichinho, letra por letra.",
    dica=u"Nome próprio de bicho de estimação é escrito com letra grande.",
    dados=[{u"palavra":u"BENTO", u"img":u"", u"voz":u"bento",
            u"pista":u"O nome do menino da história. Escreva: Bento.",
            u"dic":u"É um nome próprio: <b>Bento</b>."},
           {u"palavra":u"MIMI", u"img":u"", u"voz":u"mimi",
            u"pista":u"O nome da gata. Escreva: Mimi.",
            u"dic":u"É um nome próprio: <b>Mimi</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>nome próprio</b> do bichinho, letra por letra.",
                u"FECHO":u"Você escreveu os nomes próprios!"})

add(id=u"f11", mec=u"digitar", selo=u"ESCREVA O NOME DO LUGAR", conceito=u"objetivo3",
    enunciado=u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
    dica=u"Nome de cidade e de país é próprio.",
    dados=[{u"palavra":u"BLUMENAU", u"img":u"", u"voz":u"blumenau",
            u"pista":u"O nome da cidade da nossa escola. Escreva: Blumenau.",
            u"dic":u"É um nome próprio: <b>Blumenau</b>."},
           {u"palavra":u"BRASIL", u"img":u"", u"voz":u"brasil",
            u"pista":u"O nome do nosso país. Escreva: Brasil.",
            u"dic":u"É um nome próprio: <b>Brasil</b>."}],
    dadosExtra={u"ENUN":u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
                u"FECHO":u"Muito bem! Nome de lugar é próprio."})

# ============================================================
# QUEM-SOU-EU (f12)
# ============================================================
add(id=u"f12", mec=u"quem-sou-eu", selo=u"ADIVINHE O NOME", conceito=u"objetivo2",
    enunciado=u"Ouça as pistas e ache o <b>nome próprio</b>.",
    dica=u"Pense no que é de UM só e começa com letra grande.",
    dados=[{u"resp":u"BLUMENAU",
            u"pistas":[u"Sou o nome de uma <b>cidade</b>.",
                       u"Começo com <b>letra grande</b>.",
                       u"Sou a cidade onde fica a nossa <b>escola</b>."],
            u"outros":[u"CIDADE", u"LUGAR", u"RUA"]},
           {u"resp":u"REX",
            u"pistas":[u"Sou o nome de um <b>cachorro</b>.",
                       u"Começo com <b>letra grande</b>.",
                       u"Sou de UM cachorro só; o meu dono me chama assim."],
            u"outros":[u"CACHORRO", u"BICHO", u"AMIGO"]}])

# ============================================================
# INTRUSO (f13)
# ============================================================
add(id=u"f13", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo3",
    enunciado=u"Três são nomes <b>próprios</b>. Ache o que NÃO é (o comum).",
    dica=u"O intruso serve para qualquer um e começa com letra pequena.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
            u"enun":u"Três são nomes <b>próprios</b>. Qual NÃO é (o comum)?",
            u"itens":[{u"k":u"a", u"n":u"Ana"}, {u"k":u"b", u"n":u"Rex"},
                      {u"k":u"c", u"n":u"Blumenau"}, {u"k":u"d", u"n":u"menino"}],
            u"fora":u"d", u"nomeFora":u"menino",
            u"d1":u"Três nomes são de UM só; um serve para qualquer um — ache esse.",
            u"d2":u"Ana, Rex e Blumenau começam com letra grande; menino, não.",
            u"d3":u"O de fora é <b>menino</b>: ele é nome comum, serve para qualquer um.",
            u"razoes":[{u"t":u"É comum: serve para qualquer um; os outros são de um só.", u"ok":1},
                       {u"t":u"Porque é a palavra mais curta.", u"ok":0},
                       {u"t":u"Porque começa com M.", u"ok":0}],
            u"enunPorque":u"Por que <b>menino</b> é diferente dos outros três? Toque na razão certa.",
            u"p1":u"Olhe o que os OUTROS três têm em comum.",
            u"p2":u"O tamanho não importa; pense se é de um só ou de qualquer um.",
            u"p3":u"A letra não importa; pense no que o nome nomeia."},
           {u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
            u"enun":u"Três são nomes <b>próprios</b>. Qual NÃO é (o comum)?",
            u"itens":[{u"k":u"a", u"n":u"gato"}, {u"k":u"b", u"n":u"Mimi"},
                      {u"k":u"c", u"n":u"Bento"}, {u"k":u"d", u"n":u"Brasil"}],
            u"fora":u"a", u"nomeFora":u"gato",
            u"d1":u"Um dos nomes serve para qualquer um — ache esse.",
            u"d2":u"Mimi, Bento e Brasil são de um só, com letra grande; gato, não.",
            u"d3":u"O de fora é <b>gato</b>: é nome comum, serve para qualquer gato.",
            u"razoes":[{u"t":u"É comum: nomeia qualquer gato; os outros são de um só.", u"ok":1},
                       {u"t":u"Porque é um animal.", u"ok":0},
                       {u"t":u"Porque tem quatro letras.", u"ok":0}],
            u"enunPorque":u"Por que <b>gato</b> é diferente? Toque na razão certa.",
            u"p1":u"Pense se o nome é de um só ou de qualquer um.",
            u"p2":u"Mimi e Bento também são de seres vivos, e são próprios.",
            u"p3":u"O tamanho não importa aqui."}])

# ============================================================
# CAÇA-PALAVRAS (fecho) — nomes próprios
# ============================================================
add(id=u"f14", mec=u"caca-palavras", selo=u"CAÇA AOS NOMES PRÓPRIOS", conceito=u"objetivo2",
    enunciado=u"Ache os <b>nomes próprios</b> escondidos no quadro. Eles têm letra grande!",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"ANA", u"REX", u"MIMI", u"BENTO", u"BRASIL"],
    dadosExtra={u"MODO":u"lista",
                u"TITULO":u"OS NOMES PRÓPRIOS",
                u"LETRAS":u"ABEILMNORSTUX",
                u"DIFICIL":u"",
                u"CORP":[u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
CONTEUDO[u"fases"] = fases
CONTEUDO[u"habilidades"] = HAB

cam = os.path.join(PASTA, u"conteudo.json")
with io.open(cam, u"w", encoding=u"utf-8") as f:
    f.write(json.dumps(CONTEUDO, ensure_ascii=False, indent=1))

print(u"conteudo.json: %d fases (%s)" % (len(fases), CONTEUDO[u"titulo"]))
g={}; o={}
for x in fases:
    g[x[u"mec"]]=g.get(x[u"mec"],0)+1
    o[x[u"conceito"]]=o.get(x[u"conceito"],0)+1
print(u"gestos:", g)
print(u"objetivos:", o)
