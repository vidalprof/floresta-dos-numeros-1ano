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
 u"voz": u"masculina",
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
# BLOCO 1 — ESCOLHER (f01 comum, f02 próprio) — 6 rodadas cada
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
     esc(u"sn_bola", u"Qual palavra vale para <b>qualquer</b> uma dessas?",
         u"BOLA", u"bola", [(u"PIPOCA", u"pipoca"), (u"NINA", u"nina")], D_COM),
     esc(u"sn_arvore", u"Qual palavra serve para <b>qualquer</b> uma?",
         u"ÁRVORE", u"árvore", [(u"IPÊ", u"ipê"), (u"FLORA", u"flora")], D_COM),
     esc(u"sn_casa", u"Qual palavra vale para <b>qualquer</b> uma?",
         u"CASA", u"casa", [(u"LAR", u"lar"), (u"VILA", u"vila")], D_COM),
     esc(u"sn_papagaio", u"Qual palavra vale para <b>qualquer</b> um deles?",
         u"PAPAGAIO", u"papagaio", [(u"LOURO", u"louro"), (u"ZÉ", u"zé")], D_COM),
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
     esc(u"sn_cachorro", u"Qual é o nome <b>próprio</b> do cachorro?",
         u"REX", u"rex", [(u"cachorro", u"cachorro"), (u"bicho", u"bicho")], D_PRO),
     esc(u"sn_gato", u"Qual é o nome <b>próprio</b> da gata?",
         u"MIMI", u"mimi", [(u"gata", u"gata"), (u"bichana", u"bichana")], D_PRO),
     esc(u"sn_casa", u"Qual é o nome <b>próprio</b> do país?",
         u"BRASIL", u"brasil", [(u"país", u"país"), (u"lugar", u"lugar")], D_PRO),
     esc(u"sn_menina", u"Qual é o nome <b>próprio</b> desta menina?",
         u"LIA", u"lia", [(u"menina", u"menina"), (u"garota", u"garota")], D_PRO),
    ])

add(id=u"f02b", mec=u"escolher", selo=u"PRÓPRIO OU COMUM?", conceito=u"objetivo3",
    enunciado=u"Agora misturado: ache o nome <b>próprio</b> (o de UM só, letra grande).",
    dica=u"Próprio é de um só e começa com letra MAIÚSCULA.",
    dados=[
     esc(u"sn_cachorro", u"Qual é o nome <b>próprio</b> deste cachorro?",
         u"BIDU", u"bidu", [(u"cachorro", u"cachorro"), (u"bicho", u"bicho")], D_PRO),
     esc(u"sn_cidade", u"Qual é o nome <b>próprio</b> deste lugar?",
         u"RECIFE", u"recife", [(u"cidade", u"cidade"), (u"praia", u"praia")], D_PRO),
     esc(u"sn_menino", u"Qual é o nome <b>próprio</b> deste menino?",
         u"GAEL", u"gael", [(u"menino", u"menino"), (u"colega", u"colega")], D_PRO),
     esc(u"sn_gato", u"Qual é o nome <b>próprio</b> desta gata?",
         u"NINA", u"nina", [(u"gata", u"gata"), (u"bichana", u"bichana")], D_PRO),
    ])

# ============================================================
# BLOCO 2 — LIGAR (f03/f03b próprio, f04/f04b comum) — 4 pares cada
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

add(id=u"f03b", mec=u"ligar", selo=u"DÊ UM NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"De novo: ligue cada figura ao seu <b>nome próprio</b>.",
    dica=u"O nome próprio é de UM só e tem letra grande.",
    dados=[{u"k":u"m0", u"img":u"sn_menina",  u"voz":u"menina",  u"s":u"DUDA"},
           {u"k":u"m1", u"img":u"sn_cidade",  u"voz":u"cidade",  u"s":u"BLUMENAU"},
           {u"k":u"m2", u"img":u"sn_cachorro",u"voz":u"cachorro",u"s":u"BIDU"},
           {u"k":u"m3", u"img":u"sn_gato",    u"voz":u"gato",    u"s":u"NINA"}],
    dadosExtra={u"ENUN":u"De novo: ligue cada figura ao seu <b>nome próprio</b>.",
                u"DICAS":[u"Nome de um só, com letra grande.",
                          u"Duda é a menina, Blumenau é a cidade, Bidu é o cachorro, Nina é a gata."],
                u"FECHO":u"Cada um com o seu nome próprio!"})

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

add(id=u"f04b", mec=u"ligar", selo=u"QUAL É O NOME COMUM?", conceito=u"objetivo1",
    enunciado=u"Mais uma: ligue cada figura ao seu <b>nome comum</b>.",
    dica=u"Pergunte: o que é isso? É o tipo da coisa.",
    dados=[{u"k":u"d0", u"img":u"sn_cachorro",u"voz":u"cachorro",u"s":u"CACHORRO"},
           {u"k":u"d1", u"img":u"sn_gato",    u"voz":u"gato",    u"s":u"GATO"},
           {u"k":u"d2", u"img":u"sn_papagaio",u"voz":u"papagaio",u"s":u"PAPAGAIO"},
           {u"k":u"d3", u"img":u"sn_menina",  u"voz":u"menina",  u"s":u"MENINA"}],
    dadosExtra={u"ENUN":u"Mais uma: ligue cada figura ao seu <b>nome comum</b>.",
                u"DICAS":[u"O nome comum vale para qualquer um do tipo.",
                          u"Cachorro, gato, papagaio, menina — todos são nomes comuns."],
                u"FECHO":u"Todo mundo tem um nome comum!"})

# ============================================================
# BLOCO 3 — CLASSIFICAR (f05, f06, f06b) — 6 fichas cada
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
add(**classif(u"f05b", [{u"t":u"Lia",u"alvo":u"pro"},{u"t":u"amiga",u"alvo":u"com"},
                        {u"t":u"Louro",u"alvo":u"pro"},{u"t":u"papagaio",u"alvo":u"com"},
                        {u"t":u"Bidu",u"alvo":u"pro"},{u"t":u"cachorro",u"alvo":u"com"}]))
add(**classif(u"f06", [{u"t":u"Brasil",u"alvo":u"pro"},{u"t":u"país",u"alvo":u"com"},
                       {u"t":u"Maria",u"alvo":u"pro"},{u"t":u"professora",u"alvo":u"com"},
                       {u"t":u"Louro",u"alvo":u"pro"},{u"t":u"papagaio",u"alvo":u"com"}]))
add(**classif(u"f06b", [{u"t":u"Bento",u"alvo":u"pro"},{u"t":u"menino",u"alvo":u"com"},
                        {u"t":u"Mimi",u"alvo":u"pro"},{u"t":u"gato",u"alvo":u"com"},
                        {u"t":u"Duda",u"alvo":u"pro"},{u"t":u"amiga",u"alvo":u"com"}]))
add(**classif(u"f06c", [{u"t":u"Nina",u"alvo":u"pro"},{u"t":u"gata",u"alvo":u"com"},
                        {u"t":u"Recife",u"alvo":u"pro"},{u"t":u"cidade",u"alvo":u"com"},
                        {u"t":u"Gael",u"alvo":u"pro"},{u"t":u"colega",u"alvo":u"com"}]))

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
     esc(u"sn_papagaio", u"Qual palavra vale para <b>qualquer</b> um?",
         u"PAPAGAIO", u"papagaio", [(u"LOURO", u"louro"), (u"VERDE", u"verde")], D_COM),
    ])

# ============================================================
# BLOCO 4 — COMPLETAR (f07, f07b, f08) — a letra grande
# ============================================================
add(id=u"f07", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"No nome próprio, <b>só a primeira letra é maiúscula</b>. Escolha o certo.",
    dica=u"Só a PRIMEIRA letra é grande.",
    dados=[{u"img":u"", u"ante":u"O cachorro se chama ", u"dep":u".", u"cer":u"Rex", u"out":[u"rex", u"REX"], u"dic":u"Só o R é grande: Rex."},
           {u"img":u"", u"ante":u"A menina se chama ",   u"dep":u".", u"cer":u"Lia", u"out":[u"lia", u"LIA"], u"dic":u"Só o L é grande: Lia."},
           {u"img":u"", u"ante":u"A gata se chama ",      u"dep":u".", u"cer":u"Mimi", u"out":[u"mimi", u"MIMI"], u"dic":u"Só o M é grande: Mimi."},
           {u"img":u"", u"ante":u"O menino se chama ",    u"dep":u".", u"cer":u"Bento", u"out":[u"bento", u"BENTO"], u"dic":u"Só o B é grande: Bento."}],
    dadosExtra={u"ENUN":u"No nome próprio, <b>só a primeira letra é maiúscula</b>. Escolha o certo.",
                u"FECHO":u"Você acertou a letra grande em todos!"})

add(id=u"f07b", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"De novo: escolha o nome com a <b>letra grande</b> no lugar certo.",
    dica=u"Nome próprio começa com letra MAIÚSCULA.",
    dados=[{u"img":u"", u"ante":u"O papagaio se chama ", u"dep":u".", u"cer":u"Louro", u"out":[u"louro", u"LOURO"], u"dic":u"Só o L é grande: Louro."},
           {u"img":u"", u"ante":u"O outro cachorro é o ", u"dep":u".", u"cer":u"Bidu", u"out":[u"bidu", u"BIDU"], u"dic":u"Só o B é grande: Bidu."},
           {u"img":u"", u"ante":u"A colega nova é a ", u"dep":u".", u"cer":u"Duda", u"out":[u"duda", u"DUDA"], u"dic":u"Só o D é grande: Duda."},
           {u"img":u"", u"ante":u"A gatinha é a ", u"dep":u".", u"cer":u"Nina", u"out":[u"nina", u"NINA"], u"dic":u"Só o N é grande: Nina."}],
    dadosExtra={u"ENUN":u"De novo: escolha o nome com a <b>letra grande</b> no lugar certo.",
                u"FECHO":u"Todo nome próprio: letra grande no começo!"})

add(id=u"f08", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"Preencha o nome do lugar do jeito <b>certo</b>.",
    dica=u"Cidade e país são nomes próprios: letra grande.",
    dados=[{u"img":u"", u"ante":u"Eu moro em ", u"dep":u".", u"cer":u"Blumenau", u"out":[u"blumenau", u"BLUMENAU"], u"dic":u"Só o B é grande: Blumenau."},
           {u"img":u"", u"ante":u"Eu vivo no ", u"dep":u".", u"cer":u"Brasil", u"out":[u"brasil", u"BRASIL"], u"dic":u"Só o B é grande: Brasil."},
           {u"img":u"", u"ante":u"Minha amiga é a ", u"dep":u".", u"cer":u"Maria", u"out":[u"maria", u"MARIA"], u"dic":u"Só o M é grande: Maria."}],
    dadosExtra={u"ENUN":u"Preencha o nome do lugar do jeito <b>certo</b>.",
                u"FECHO":u"Isso! Nome de lugar e de pessoa é próprio."})

add(id=u"f08b", mec=u"completar", selo=u"A LETRA GRANDE", conceito=u"objetivo3",
    enunciado=u"Preencha com o nome próprio escrito do jeito <b>certo</b>.",
    dica=u"Nome de pessoa, bicho e lugar é próprio: letra grande.",
    dados=[{u"img":u"", u"ante":u"O menino novo é o ", u"dep":u".", u"cer":u"Gael", u"out":[u"gael", u"GAEL"], u"dic":u"Só o G é grande: Gael."},
           {u"img":u"", u"ante":u"A cidade da praia é ", u"dep":u".", u"cer":u"Recife", u"out":[u"recife", u"RECIFE"], u"dic":u"Só o R é grande: Recife."},
           {u"img":u"", u"ante":u"O papagaio é o ", u"dep":u".", u"cer":u"Louro", u"out":[u"louro", u"LOURO"], u"dic":u"Só o L é grande: Louro."},
           {u"img":u"", u"ante":u"A gatinha nova é a ", u"dep":u".", u"cer":u"Nina", u"out":[u"nina", u"NINA"], u"dic":u"Só o N é grande: Nina."}],
    dadosExtra={u"ENUN":u"Preencha com o nome próprio escrito do jeito <b>certo</b>.",
                u"FECHO":u"Nome próprio: sempre com letra grande no começo!"})

# ============================================================
# BLOCO 5 — DIGITAR (f09 bicho, f10 lugar, f10b nomes)
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

add(id=u"f09b", mec=u"digitar", selo=u"ESCREVA O NOME PRÓPRIO", conceito=u"objetivo2",
    enunciado=u"Escreva mais um <b>nome próprio</b>, letra por letra.",
    dica=u"Nome próprio começa com letra grande.",
    dados=[{u"palavra":u"DUDA", u"img":u"", u"voz":u"duda", u"pista":u"O nome da menina. Escreva: Duda.", u"dic":u"Nome próprio: <b>Duda</b>."},
           {u"palavra":u"NINA", u"img":u"", u"voz":u"nina", u"pista":u"O nome da outra gata. Escreva: Nina.", u"dic":u"Nome próprio: <b>Nina</b>."},
           {u"palavra":u"BIDU", u"img":u"", u"voz":u"bidu", u"pista":u"O nome do outro cachorro. Escreva: Bidu.", u"dic":u"Nome próprio: <b>Bidu</b>."},
           {u"palavra":u"GAEL", u"img":u"", u"voz":u"gael", u"pista":u"O nome do menino novo. Escreva: Gael.", u"dic":u"Nome próprio: <b>Gael</b>."}],
    dadosExtra={u"ENUN":u"Escreva mais um <b>nome próprio</b>, letra por letra.",
                u"FECHO":u"Mais nomes próprios escritos com letra grande!"})

add(id=u"f10", mec=u"digitar", selo=u"ESCREVA O NOME DO LUGAR", conceito=u"objetivo3",
    enunciado=u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
    dica=u"Nome de cidade e de país é próprio.",
    dados=[{u"palavra":u"BLUMENAU", u"img":u"", u"voz":u"blumenau", u"pista":u"A cidade da nossa escola. Escreva: Blumenau.", u"dic":u"Nome próprio: <b>Blumenau</b>."},
           {u"palavra":u"BRASIL", u"img":u"", u"voz":u"brasil", u"pista":u"O nosso país. Escreva: Brasil.", u"dic":u"Nome próprio: <b>Brasil</b>."},
           {u"palavra":u"DUDA", u"img":u"", u"voz":u"duda", u"pista":u"O nome da menina. Escreva: Duda.", u"dic":u"Nome próprio: <b>Duda</b>."}],
    dadosExtra={u"ENUN":u"Agora escreva o <b>nome próprio</b> do lugar, letra por letra.",
                u"FECHO":u"Muito bem! Nome de lugar e de pessoa é próprio."})

# ============================================================
# QUEM-SOU-EU (f11) — 6 rodadas
# ============================================================
add(id=u"f11", mec=u"quem-sou-eu", selo=u"ADIVINHE O NOME", conceito=u"objetivo2",
    enunciado=u"Ouça as pistas e ache o <b>nome próprio</b>.",
    dica=u"Pense no que é de UM só e começa com letra grande.",
    dados=[
     {u"resp":u"BLUMENAU", u"pistas":[u"Sou o nome de uma <b>cidade</b>.", u"Começo com <b>letra grande</b>.", u"Sou a cidade da nossa <b>escola</b>."], u"outros":[u"CIDADE", u"LUGAR", u"RUA"]},
     {u"resp":u"REX", u"pistas":[u"Sou o nome de um <b>cachorro</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UM cachorro só."], u"outros":[u"CACHORRO", u"BICHO", u"AMIGO"]},
     {u"resp":u"BRASIL", u"pistas":[u"Sou o nome de um <b>país</b>.", u"Começo com <b>letra grande</b>.", u"É o país onde a gente mora."], u"outros":[u"PAÍS", u"LUGAR", u"MUNDO"]},
     {u"resp":u"DUDA", u"pistas":[u"Sou o nome de uma <b>menina</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UMA menina só."], u"outros":[u"MENINA", u"AMIGA", u"COLEGA"]},
     {u"resp":u"MIMI", u"pistas":[u"Sou o nome de uma <b>gata</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UMA gata só."], u"outros":[u"GATA", u"BICHANA", u"AMIGA"]},
     {u"resp":u"LOURO", u"pistas":[u"Sou o nome de um <b>papagaio</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UM papagaio só."], u"outros":[u"PAPAGAIO", u"AVE", u"PÁSSARO"]},
     {u"resp":u"BENTO", u"pistas":[u"Sou o nome de um <b>menino</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UM menino só."], u"outros":[u"MENINO", u"COLEGA", u"AMIGO"]},
     {u"resp":u"GAEL", u"pistas":[u"Sou o nome de outro <b>menino</b>.", u"Começo com <b>letra grande</b>.", u"Sou de UM menino só."], u"outros":[u"MENINO", u"GAROTO", u"COLEGA"]},
    ])

# ============================================================
# INTRUSO (f12, f12b) — ache o COMUM
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
add(**intruso(u"f12b", [(u"a",u"Maria"),(u"b",u"Bento"),(u"c",u"Brasil"),(u"d",u"cidade")], u"d", u"cidade",
              u"Maria, Bento e Brasil começam com letra grande; cidade, não."))

# ============================================================
# CAÇA-PALAVRAS (fecho) — f13 nomes próprios, f13b nomes comuns
# ============================================================
add(id=u"f13", mec=u"caca-palavras", selo=u"CAÇA AOS NOMES PRÓPRIOS", conceito=u"objetivo2",
    enunciado=u"Ache os <b>nomes próprios</b> escondidos no quadro. Eles têm letra grande!",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"LIA", u"REX", u"MIMI", u"BENTO", u"BRASIL"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"OS NOMES PRÓPRIOS",
                u"LETRAS":u"ABEILMNORSTUX", u"DIFICIL":True,
                u"CORP":[u"p1", u"p2", u"p3", u"p4", u"p5"]})

add(id=u"f13b", mec=u"caca-palavras", selo=u"CAÇA AOS NOMES COMUNS", conceito=u"objetivo1",
    enunciado=u"Agora ache os <b>nomes comuns</b> escondidos no quadro.",
    dica=u"Nome comum é o tipo da coisa: gato, casa, bola...",
    dados=[u"GATO", u"CASA", u"BOLA", u"CIDADE", u"ARVORE"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"OS NOMES COMUNS",
                u"LETRAS":u"ABCDEILORSTVZ", u"DIFICIL":True,
                u"CORP":[u"c1", u"c2", u"c3", u"c4", u"c5"]})

add(id=u"f13c", mec=u"caca-palavras", selo=u"CAÇA AOS NOMES DE LUGAR", conceito=u"objetivo3",
    enunciado=u"Ache os <b>nomes próprios de lugar</b> escondidos. Eles têm letra grande!",
    dica=u"Nomes de cidade e de país são próprios: letra grande.",
    dados=[u"BRASIL", u"BLUMENAU", u"BAHIA", u"PARANA", u"RECIFE"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"OS NOMES DE LUGAR",
                u"LETRAS":u"ABCEFHILMNPRSU", u"DIFICIL":True,
                u"CORP":[u"l1", u"l2", u"l3", u"l4", u"l5"]})

# ============================================================
# ⭐ CAIXA CERTA (Marcos, ago/2026): esta lição É sobre maiúscula/minúscula. Logo,
#    nome COMUM aparece em minúsculo e nome PRÓPRIO com a Inicial Maiúscula (só a
#    1ª letra). Sem isto, tudo em CAIXA ALTA apaga a própria distinção que a
#    atividade ensina (o Marcos pegou: "no comum está tudo maiúsculo; o próprio Rex
#    fica igual ao comum; a régua não diferencia certo do errado").
#    NÃO mexe em: completar (A LETRA GRANDE — as opções Rex/rex/REX são de caso, de
#    propósito), intruso (já vem no caso certo) e caça-palavras (grade é maiúscula).
_PROPRIOS = set((u"rex bidu mimi nina lia duda bento gael louro zé ze ipê ipe flora "
                 u"pipoca blumenau brasil recife maria bahia paraná parana").split())
def _caso(w):
    s = (w or u"").strip()
    if not s:
        return w
    return (s[0].upper() + s[1:].lower()) if s.lower() in _PROPRIOS else s.lower()
for _f in fases:
    _m = _f.get(u"mec")
    if _m == u"escolher":
        for _r in _f.get(u"dados", []):
            if isinstance(_r.get(u"c"), dict) and u"t" in _r[u"c"]:
                _r[u"c"][u"t"] = _caso(_r[u"c"][u"t"])
            for _e in _r.get(u"e", []):
                if isinstance(_e, dict) and u"t" in _e:
                    _e[u"t"] = _caso(_e[u"t"])
    elif _m == u"ligar":
        for _r in _f.get(u"dados", []):
            if isinstance(_r, dict) and u"s" in _r:
                _r[u"s"] = _caso(_r[u"s"])
    elif _m == u"quem-sou-eu":
        for _r in _f.get(u"dados", []):
            if u"resp" in _r:
                _r[u"resp"] = _caso(_r[u"resp"])
            _r[u"outros"] = [_caso(x) for x in _r.get(u"outros", [])]
    elif _m == u"digitar":
        # nome próprio escrito com a Inicial Maiúscula (o motor agora respeita o
        # caso das teclas — ver digitar case-aware em pecas.js)
        for _r in _f.get(u"dados", []):
            if u"palavra" in _r:
                _r[u"palavra"] = _caso(_r[u"palavra"])

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
