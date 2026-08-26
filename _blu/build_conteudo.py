# -*- coding: utf-8 -*-
u"""Gera _blu/conteudo.json — BLUMENAU, A NOSSA CIDADE (3º ano, Geografia).

Molde ESQUELETO (mesmas mecânicas provadas do _subs), em BLOCOS (repetição
seguida). Temas do Marcos: público×privado · povos indígenas (Xokleng) ·
economia · pontos turísticos · mapa · representações cartográficas (legenda).

Fatos conferidos (_pesquisa/web/blumenau-3ano.md):
  fundada 2/9/1850 por Dr. Hermann Blumenau + 17 imigrantes alemães; rio
  Itajaí-Açu; antes viviam os Xokleng; economia têxtil/malhas, informática,
  cervejarias (Oktoberfest); turísticos: Vila Germânica, Ponte dos Arcos,
  Teatro Carlos Gomes, Castelinho da Moellmann, Prefeitura (enxaimel).
BNCC 3º ano: EF03GE02/05/06/07/09.
"""
import io, json, os
PASTA = os.path.dirname(os.path.abspath(__file__))
HAB = (u"Reconhecer lugares e serviços públicos e privados; identificar atividades "
       u"econômicas e pontos de referência do município; ler mapas simples com legenda. "
       u"EF03GE02/05/06/07/09 (3º ano).")

C = {
 u"titulo": u"Blumenau, a Nossa Cidade", u"sub": u"Geografia · 3º ano · A cidade e o mapa",
 u"ano": u"3º ano", u"prefixo": u"bl", u"mascote": u"capivara", u"mascoteNome": u"Bruna",
 u"crachas": 6, u"mesa": u"Pedagogo do 3º ano + especialista em Geografia (município/cartografia).",
 u"fundo": u"bl_fundo.png", u"voz": u"feminina",
 u"abertura": (u"Oi! Eu sou a Bruna, a capivara guia. Moro aqui em Blumenau, à beira do rio "
              u"Itajaí-Açu. Vem conhecer a nossa cidade: os lugares, o trabalho das pessoas e o mapa!"),
 u"fim": (u"Que passeio! Você já conhece os lugares de Blumenau, quem morava aqui antes, o que a "
          u"cidade produz e como ler um mapa com legenda. Você é guia de verdade!"),
 u"conceitos": {
   u"objetivo1": u"Lugares PÚBLICOS (de todos) × PRIVADOS (de um)",
   u"objetivo2": u"A cidade: povos indígenas, economia e pontos turísticos",
   u"objetivo3": u"Mapa e representação cartográfica (legenda e nomes)",
 },
 u"curriculo": {
   u"objetivo1": u"Identificar lugares e serviços públicos e privados do município. EF03GE02.",
   u"objetivo2": u"Reconhecer atividades econômicas e a formação cultural do lugar. EF03GE05/06.",
   u"objetivo3": u"Ler e representar o espaço com mapas simples e legenda. EF03GE07/09.",
 },
 u"fases": [],
}
fases=[]
def add(**k): fases.append(k)
def esc(img,p,c,cvoz,erradas,dicas,cimg=None,eimgs=None):
    cop={u"t":c,u"voz":cvoz}
    if cimg: cop[u"img"]=cimg
    es=[]
    for i,(t,v) in enumerate(erradas):
        o={u"t":t,u"voz":v}
        if eimgs and i<len(eimgs) and eimgs[i]: o[u"img"]=eimgs[i]
        es.append(o)
    return {u"img":img,u"p":p,u"c":cop,u"e":es,u"d":dicas}
DPUB=[u"Público é de TODOS: qualquer um pode usar.",u"É da cidade, para todo mundo? É público.",u"Isso! Lugar <b>público</b>. Toque para seguir."]
DPRI=[u"Privado é de UMA pessoa ou família.",u"Tem dono? Nem todos entram? É privado.",u"Isso! Lugar <b>privado</b>. Toque para seguir."]

# ============ BLOCO 1 — ESCOLHER (público, privado, mapa) ============
add(id=u"f01", mec=u"escolher", selo=u"DE TODOS", conceito=u"objetivo1",
    enunciado=u"Lugar <b>público</b> é de <b>todos</b>. Ache o público.",
    dica=u"Público: qualquer pessoa pode usar.",
    dados=[
     esc(u"bl_praca",u"Qual é <b>público</b>, de todos?",u"A PRAÇA",u"a praça",[(u"A CASA",u"a casa"),(u"A LOJA",u"a loja")],DPUB,cimg=u"bl_praca",eimgs=[u"bl_casa",u"bl_loja"]),
     esc(u"bl_hospital",u"E qual é <b>público</b>?",u"O HOSPITAL",u"o hospital",[(u"A PADARIA",u"a padaria"),(u"O MERCADO",u"o mercado")],DPUB,cimg=u"bl_hospital",eimgs=[u"bl_padaria",u"bl_mercado"]),
     esc(u"bl_escola",u"Qual lugar é de <b>todos</b>?",u"A ESCOLA",u"a escola",[(u"A CASA",u"a casa"),(u"A LOJA",u"a loja")],DPUB,cimg=u"bl_escola",eimgs=[u"bl_casa",u"bl_loja"]),
     esc(u"bl_prefeitura",u"Qual prédio <b>público</b> cuida da cidade?",u"A PREFEITURA",u"a prefeitura",[(u"A CASA",u"a casa"),(u"O MERCADO",u"o mercado")],DPUB,cimg=u"bl_prefeitura",eimgs=[u"bl_casa",u"bl_mercado"]),
    ])
add(id=u"f02", mec=u"escolher", selo=u"DE UM DONO", conceito=u"objetivo1",
    enunciado=u"Lugar <b>privado</b> é de <b>uma pessoa ou família</b>. Ache o privado.",
    dica=u"Privado: tem dono, nem todos entram.",
    dados=[
     esc(u"bl_casa",u"Qual é <b>privado</b>, de uma família?",u"A CASA",u"a casa",[(u"A PRAÇA",u"a praça"),(u"O HOSPITAL",u"o hospital")],DPRI,cimg=u"bl_casa",eimgs=[u"bl_praca",u"bl_hospital"]),
     esc(u"bl_loja",u"Qual é <b>privado</b>, tem dono?",u"A LOJA",u"a loja",[(u"A ESCOLA",u"a escola"),(u"A PRAÇA",u"a praça")],DPRI,cimg=u"bl_loja",eimgs=[u"bl_escola",u"bl_praca"]),
     esc(u"bl_mercado",u"Qual lugar é <b>privado</b>?",u"O MERCADO",u"o mercado",[(u"A PREFEITURA",u"a prefeitura"),(u"A ESCOLA",u"a escola")],DPRI,cimg=u"bl_mercado",eimgs=[u"bl_prefeitura",u"bl_escola"]),
     esc(u"bl_padaria",u"Qual é <b>privado</b>, de um dono?",u"A PADARIA",u"a padaria",[(u"O HOSPITAL",u"o hospital"),(u"A PRAÇA",u"a praça")],DPRI,cimg=u"bl_padaria",eimgs=[u"bl_hospital",u"bl_praca"]),
    ])
DMAP=[u"O mapa mostra a cidade vista de cima.",u"Ele ajuda a encontrar o caminho.",u"Isso! Toque para seguir."]
add(id=u"f03", mec=u"escolher", selo=u"O MAPA", conceito=u"objetivo3",
    enunciado=u"O <b>mapa</b> mostra a cidade vista de <b>cima</b>. Responda:",
    dica=u"Pense para que a gente usa um mapa.",
    dados=[
     esc(u"bl_mapa",u"Para que serve um <b>mapa</b> da cidade?",u"PARA ACHAR OS LUGARES",u"para achar os lugares",[(u"PARA COMER",u"para comer"),(u"PARA DORMIR",u"para dormir")],DMAP,cimg=u"bl_mapa"),
     esc(u"bl_mapa",u"No mapa, a <b>linha azul</b> que corta a cidade é o quê?",u"O RIO ITAJAÍ",u"o rio Itajaí",[(u"UMA RUA",u"uma rua"),(u"UM MURO",u"um muro")],DMAP,cimg=u"bl_mapa"),
     esc(u"bl_mapa",u"O que explica os <b>símbolos</b> do mapa?",u"A LEGENDA",u"a legenda",[(u"A CAPA",u"a capa"),(u"O TÍTULO",u"o título")],DMAP,cimg=u"bl_mapa"),
    ])
add(id=u"f01b", mec=u"escolher", selo=u"DE TODOS", conceito=u"objetivo1",
    enunciado=u"De novo: ache o lugar <b>público</b> (de todos).",
    dica=u"Público é de todo mundo.",
    dados=[
     esc(u"bl_hospital",u"Qual é <b>público</b>?",u"O HOSPITAL",u"o hospital",[(u"A LOJA",u"a loja"),(u"A CASA",u"a casa")],DPUB,cimg=u"bl_hospital",eimgs=[u"bl_loja",u"bl_casa"]),
     esc(u"bl_praca",u"Qual lugar é de <b>todos</b>?",u"A PRAÇA",u"a praça",[(u"O MERCADO",u"o mercado"),(u"A PADARIA",u"a padaria")],DPUB,cimg=u"bl_praca",eimgs=[u"bl_mercado",u"bl_padaria"]),
     esc(u"bl_escola",u"Qual é <b>público</b>?",u"A ESCOLA",u"a escola",[(u"A LOJA",u"a loja"),(u"O MERCADO",u"o mercado")],DPUB,cimg=u"bl_escola",eimgs=[u"bl_loja",u"bl_mercado"]),
     esc(u"bl_prefeitura",u"Qual prédio é <b>público</b>?",u"A PREFEITURA",u"a prefeitura",[(u"A PADARIA",u"a padaria"),(u"A CASA",u"a casa")],DPUB,cimg=u"bl_prefeitura",eimgs=[u"bl_padaria",u"bl_casa"]),
    ])
add(id=u"f02b", mec=u"escolher", selo=u"DE UM DONO", conceito=u"objetivo1",
    enunciado=u"De novo: ache o lugar <b>privado</b> (de um dono).",
    dica=u"Privado tem dono; nem todos entram.",
    dados=[
     esc(u"bl_loja",u"Qual é <b>privado</b>?",u"A LOJA",u"a loja",[(u"A PRAÇA",u"a praça"),(u"A ESCOLA",u"a escola")],DPRI,cimg=u"bl_loja",eimgs=[u"bl_praca",u"bl_escola"]),
     esc(u"bl_padaria",u"Qual é <b>privado</b>?",u"A PADARIA",u"a padaria",[(u"O HOSPITAL",u"o hospital"),(u"A PREFEITURA",u"a prefeitura")],DPRI,cimg=u"bl_padaria",eimgs=[u"bl_hospital",u"bl_prefeitura"]),
     esc(u"bl_casa",u"Qual é <b>privado</b>, de uma família?",u"A CASA",u"a casa",[(u"A PRAÇA",u"a praça"),(u"A ESCOLA",u"a escola")],DPRI,cimg=u"bl_casa",eimgs=[u"bl_praca",u"bl_escola"]),
     esc(u"bl_mercado",u"Qual é <b>privado</b>?",u"O MERCADO",u"o mercado",[(u"O HOSPITAL",u"o hospital"),(u"A PRAÇA",u"a praça")],DPRI,cimg=u"bl_mercado",eimgs=[u"bl_hospital",u"bl_praca"]),
    ])

# ============ BLOCO 2 — CLASSIFICAR (público × privado) ============
def classif(idf,fichas,dicas):
    return dict(id=idf, mec=u"classificar", selo=u"SEPARE OS LUGARES", conceito=u"objetivo1",
      enunciado=u"Cada lugar na sua caixa: é <b>PÚBLICO</b> (de todos) ou <b>PRIVADO</b> (de um)?",
      dica=u"De todos = público. De um dono = privado.",
      dados=[{u"k":u"pub",u"n":u"PÚBLICO",u"img":u"",u"voz":u"público",u"rot":False},
             {u"k":u"pri",u"n":u"PRIVADO",u"img":u"",u"voz":u"privado",u"rot":False}],
      dadosExtra={u"ENUN":u"Cada lugar na sua caixa: é <b>PÚBLICO</b> ou <b>PRIVADO</b>?",u"FICHAS":fichas,u"DICAS":dicas})
add(**classif(u"f04",[{u"t":u"praça",u"alvo":u"pub"},{u"t":u"casa",u"alvo":u"pri"},
    {u"t":u"hospital",u"alvo":u"pub"},{u"t":u"loja",u"alvo":u"pri"},
    {u"t":u"escola",u"alvo":u"pub"},{u"t":u"mercado",u"alvo":u"pri"}],
    [u"Qualquer um usa? Público.",u"Tem um dono? Privado.",u"Boa! Toque para seguir."]))
add(**classif(u"f04b",[{u"t":u"prefeitura",u"alvo":u"pub"},{u"t":u"padaria",u"alvo":u"pri"},
    {u"t":u"biblioteca",u"alvo":u"pub"},{u"t":u"farmácia",u"alvo":u"pri"},
    {u"t":u"posto de saúde",u"alvo":u"pub"},{u"t":u"restaurante",u"alvo":u"pri"}],
    [u"Biblioteca e posto de saúde são de todos.",u"Farmácia e restaurante têm dono.",u"Muito bem! Toque para seguir."]))
add(**classif(u"f04c",[{u"t":u"parque",u"alvo":u"pub"},{u"t":u"cinema",u"alvo":u"pri"},
    {u"t":u"correios",u"alvo":u"pub"},{u"t":u"salão",u"alvo":u"pri"},
    {u"t":u"delegacia",u"alvo":u"pub"},{u"t":u"oficina",u"alvo":u"pri"}],
    [u"Parque, correios e delegacia são da cidade, de todos.",u"Cinema, salão e oficina têm dono.",u"Boa! Toque para seguir."]))
add(**classif(u"f04d",[{u"t":u"rua",u"alvo":u"pub"},{u"t":u"fazenda",u"alvo":u"pri"},
    {u"t":u"ponte",u"alvo":u"pub"},{u"t":u"fábrica",u"alvo":u"pri"},
    {u"t":u"posto de gasolina",u"alvo":u"pri"},{u"t":u"museu",u"alvo":u"pub"}],
    [u"Rua, ponte e museu são de todos.",u"Fazenda, fábrica e posto têm dono.",u"Muito bem! Toque para seguir."]))
add(**classif(u"f04e",[{u"t":u"praça",u"alvo":u"pub"},{u"t":u"padaria",u"alvo":u"pri"},
    {u"t":u"escola",u"alvo":u"pub"},{u"t":u"mercado",u"alvo":u"pri"},
    {u"t":u"hospital",u"alvo":u"pub"},{u"t":u"loja",u"alvo":u"pri"}],
    [u"Praça, escola e hospital: de todos.",u"Padaria, mercado e loja: têm dono.",u"Você já sabe separar! Toque para seguir."]))

# ============ BLOCO 3 — LIGAR (economia; legenda do mapa) ============
add(id=u"f05", mec=u"ligar", selo=u"O TRABALHO DA CIDADE", conceito=u"objetivo2",
    enunciado=u"Ligue cada coisa ao <b>trabalho</b> que a faz em Blumenau.",
    dica=u"Pense onde cada coisa é feita.",
    dados=[{u"k":u"e0",u"img":u"bl_camiseta",u"voz":u"camiseta",u"s":u"MALHARIA"},
           {u"k":u"e1",u"img":u"bl_caneca",u"voz":u"caneca",u"s":u"CERVEJARIA"},
           {u"k":u"e2",u"img":u"bl_computador",u"voz":u"computador",u"s":u"INFORMÁTICA"},
           {u"k":u"e3",u"img":u"bl_verduras",u"voz":u"verduras",u"s":u"ROÇA"}],
    dadosExtra={u"ENUN":u"Ligue cada coisa ao <b>trabalho</b> que a faz em Blumenau.",
                u"DICAS":[u"Camiseta vem da malharia; caneca, da cervejaria.",u"Computador é da informática; verduras, da roça."],
                u"FECHO":u"Blumenau trabalha com malhas, cerveja, informática e roça!"})
add(id=u"f06", mec=u"ligar", selo=u"A LEGENDA DO MAPA", conceito=u"objetivo3",
    enunciado=u"Ligue cada <b>símbolo</b> da legenda ao que ele significa.",
    dica=u"A legenda explica os desenhinhos do mapa.",
    dados=[{u"k":u"s0",u"img":u"bl_sim_hospital",u"voz":u"símbolo de cruz",u"s":u"HOSPITAL"},
           {u"k":u"s1",u"img":u"bl_sim_escola",u"voz":u"símbolo de livro",u"s":u"ESCOLA"},
           {u"k":u"s2",u"img":u"bl_sim_ponte",u"voz":u"símbolo de arco",u"s":u"PONTE"},
           {u"k":u"s3",u"img":u"bl_sim_rio",u"voz":u"linha azul",u"s":u"RIO"}],
    dadosExtra={u"ENUN":u"Ligue cada <b>símbolo</b> da legenda ao que ele significa.",
                u"DICAS":[u"Cruz = hospital; livro = escola.",u"Arco = ponte; linha azul = rio."],
                u"FECHO":u"Você leu a legenda do mapa!"})

# ============ BLOCO 4 — QUEM-SOU-EU (indígenas) ============
add(id=u"f07", mec=u"quem-sou-eu", selo=u"QUEM MORAVA AQUI?", conceito=u"objetivo2",
    enunciado=u"Antes da cidade, quem já morava nestas terras? Ouça as pistas.",
    dica=u"Foram os primeiros moradores, muito antes dos imigrantes.",
    dados=[
     {u"resp":u"OS XOKLENG",u"pistas":[u"Vivíamos aqui <b>antes</b> da cidade.",u"Morávamos na <b>floresta</b> e perto do <b>rio</b>.",u"Somos o povo <b>indígena</b> Xokleng."],u"outros":[u"OS ALEMÃES",u"OS TURISTAS",u"OS COLONOS"]},
     {u"resp":u"A CANOA",u"pistas":[u"Os Xokleng me usavam no rio Itajaí.",u"Sou feita de <b>madeira</b>.",u"Ando na <b>água</b>, sem motor."],u"outros":[u"O AVIÃO",u"O ÔNIBUS",u"O TREM"]},
     {u"resp":u"O RIO ITAJAÍ",u"pistas":[u"Eu corto a cidade no <b>meio</b>.",u"As canoas andavam em mim.",u"Sou o rio <b>Itajaí-Açu</b>."],u"outros":[u"A RUA",u"A PONTE",u"A PRAÇA"]},
     {u"resp":u"A FLORESTA",u"pistas":[u"Os Xokleng tiravam de mim comida e abrigo.",u"Sou cheia de <b>árvores</b>.",u"Ficava ao redor da aldeia."],u"outros":[u"O MERCADO",u"A FÁBRICA",u"A LOJA"]},
    ])

# ============ BLOCO 5 — INTRUSO (pontos turísticos) ============
add(id=u"f08", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo2",
    enunciado=u"Três são <b>pontos turísticos de Blumenau</b>. Ache o que NÃO é.",
    dica=u"Um deles não fica em Blumenau.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
      u"enun":u"Três são pontos turísticos de <b>Blumenau</b>. Qual NÃO é?",
      u"itens":[{u"k":u"a",u"n":u"Vila Germânica"},{u"k":u"b",u"n":u"Ponte dos Arcos"},{u"k":u"c",u"n":u"Teatro Carlos Gomes"},{u"k":u"d",u"n":u"Praia de Copacabana"}],
      u"fora":u"d", u"nomeFora":u"Praia de Copacabana",
      u"d1":u"Um deles fica em outra cidade, bem longe.",
      u"d2":u"Vila Germânica, Ponte dos Arcos e Teatro Carlos Gomes são de Blumenau.",
      u"d3":u"O de fora é a <b>Praia de Copacabana</b>: fica no Rio de Janeiro.",
      u"razoes":[{u"t":u"Fica em outra cidade, não em Blumenau.",u"ok":1},{u"t":u"Porque é a mais bonita.",u"ok":0},{u"t":u"Porque é a maior.",u"ok":0}],
      u"enunPorque":u"Por que a <b>Praia de Copacabana</b> é o intruso? Toque na razão certa.",
      u"p1":u"Pense onde cada lugar fica.",u"p2":u"Beleza e tamanho não importam aqui.",u"p3":u"O que importa é a cidade onde fica."}])
add(id=u"f08b", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo2",
    enunciado=u"Três são <b>trabalhos fortes de Blumenau</b>. Ache o que NÃO é daqui.",
    dica=u"Um deles não é típico de Blumenau.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
      u"enun":u"Três são trabalhos fortes de <b>Blumenau</b>. Qual NÃO é?",
      u"itens":[{u"k":u"a",u"n":u"malharia"},{u"k":u"b",u"n":u"cervejaria"},{u"k":u"c",u"n":u"informática"},{u"k":u"d",u"n":u"pesca no mar"}],
      u"fora":u"d", u"nomeFora":u"pesca no mar",
      u"d1":u"Blumenau não fica na praia.",
      u"d2":u"Malharia, cervejaria e informática são fortes aqui.",
      u"d3":u"O de fora é a <b>pesca no mar</b>: Blumenau fica longe do mar.",
      u"razoes":[{u"t":u"Blumenau não fica no mar; fica à beira do rio.",u"ok":1},{u"t":u"Porque é a mais difícil.",u"ok":0},{u"t":u"Porque é a mais antiga.",u"ok":0}],
      u"enunPorque":u"Por que a <b>pesca no mar</b> é o intruso? Toque na razão certa.",
      u"p1":u"Pense onde fica Blumenau.",u"p2":u"Não é sobre ser difícil.",u"p3":u"É sobre o mar estar longe daqui."}])

# ============ BLOCO 6 — COMPLETAR + DIGITAR (nomes próprios) ============
add(id=u"f09", mec=u"completar", selo=u"NOME PRÓPRIO", conceito=u"objetivo3",
    enunciado=u"Preencha com o nome próprio do jeito <b>certo</b> (letra grande).",
    dica=u"Nome de cidade e de rio é próprio: letra maiúscula.",
    dados=[{u"img":u"",u"ante":u"Eu moro em ",u"dep":u".",u"cer":u"Blumenau",u"out":[u"blumenau",u"BLUMENAU"],u"dic":u"Só o B é grande: Blumenau."},
           {u"img":u"",u"ante":u"O rio da cidade é o ",u"dep":u".",u"cer":u"Itajaí",u"out":[u"itajaí",u"ITAJAÍ"],u"dic":u"Só o I é grande: Itajaí."},
           {u"img":u"",u"ante":u"O povo indígena daqui é o ",u"dep":u".",u"cer":u"Xokleng",u"out":[u"xokleng",u"XOKLENG"],u"dic":u"Só o X é grande: Xokleng."}],
    dadosExtra={u"ENUN":u"Preencha com o nome próprio do jeito <b>certo</b> (letra grande).",u"FECHO":u"Nome de lugar e de povo: sempre com letra grande!"})
add(id=u"f09b", mec=u"completar", selo=u"NOME PRÓPRIO", conceito=u"objetivo3",
    enunciado=u"Preencha com o nome do lugar do jeito <b>certo</b>.",
    dica=u"Cidade, estado e festa têm nome próprio: letra grande.",
    dados=[{u"img":u"",u"ante":u"Blumenau fica no estado de ",u"dep":u".",u"cer":u"Santa Catarina",u"out":[u"santa catarina",u"SANTA CATARINA"],u"dic":u"S e C grandes: Santa Catarina."},
           {u"img":u"",u"ante":u"A festa da cerveja é a ",u"dep":u".",u"cer":u"Oktoberfest",u"out":[u"oktoberfest",u"OKTOBERFEST"],u"dic":u"Só o O é grande: Oktoberfest."},
           {u"img":u"",u"ante":u"A vila das festas é a Vila ",u"dep":u".",u"cer":u"Germânica",u"out":[u"germânica",u"GERMÂNICA"],u"dic":u"Só o G é grande: Germânica."}],
    dadosExtra={u"ENUN":u"Preencha com o nome do lugar do jeito <b>certo</b>.",u"FECHO":u"Muito bem! Nome próprio com letra grande."})
add(id=u"f10", mec=u"digitar", selo=u"ESCREVA O NOME", conceito=u"objetivo3",
    enunciado=u"Escreva o <b>nome</b> da nossa cidade e do rio, letra por letra.",
    dica=u"Nome próprio começa com letra grande.",
    dados=[{u"palavra":u"BLUMENAU",u"img":u"",u"voz":u"blumenau",u"pista":u"O nome da nossa cidade. Escreva: Blumenau.",u"dic":u"Nome próprio: <b>Blumenau</b>."},
           {u"palavra":u"ITAJAI",u"img":u"",u"voz":u"itajaí",u"pista":u"O rio que corta a cidade. Escreva: Itajaí.",u"dic":u"Nome próprio: <b>Itajaí</b>."},
           {u"palavra":u"PONTE",u"img":u"",u"voz":u"ponte",u"pista":u"O que atravessa o rio. Escreva: Ponte.",u"dic":u"<b>Ponte</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>nome</b> da nossa cidade e do rio, letra por letra.",u"FECHO":u"Muito bem! Você escreveu os nomes da cidade."})
add(id=u"f10b", mec=u"digitar", selo=u"ESCREVA O NOME", conceito=u"objetivo3",
    enunciado=u"Escreva mais nomes da nossa cidade, letra por letra.",
    dica=u"Nome próprio começa com letra grande.",
    dados=[{u"palavra":u"XOKLENG",u"img":u"",u"voz":u"xokleng",u"pista":u"O povo indígena daqui. Escreva: Xokleng.",u"dic":u"Nome próprio: <b>Xokleng</b>."},
           {u"palavra":u"PRACA",u"img":u"",u"voz":u"praça",u"pista":u"Lugar público de todos. Escreva: Praça.",u"dic":u"<b>Praça</b>."},
           {u"palavra":u"MAPA",u"img":u"",u"voz":u"mapa",u"pista":u"Mostra a cidade de cima. Escreva: Mapa.",u"dic":u"<b>Mapa</b>."}],
    dadosExtra={u"ENUN":u"Escreva mais nomes da nossa cidade, letra por letra.",u"FECHO":u"Você escreveu tudo certinho!"})

# ============ FECHO — CAÇA-PALAVRAS ============
add(id=u"f11", mec=u"caca-palavras", selo=u"CAÇA À CIDADE", conceito=u"objetivo3",
    enunciado=u"Ache as palavras da nossa cidade escondidas no quadro.",
    dica=u"Estão deitadas (→), em pé (↓) e na diagonal.",
    dados=[u"BLUMENAU",u"ITAJAI",u"XOKLENG",u"PONTE",u"MAPA"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"A NOSSA CIDADE",u"LETRAS":u"ABEGIJKLMNOPTUX",u"DIFICIL":u"",u"CORP":[u"c1",u"c2",u"c3",u"c4",u"c5"]})
add(id=u"f11b", mec=u"caca-palavras", selo=u"CAÇA AOS LUGARES", conceito=u"objetivo1",
    enunciado=u"Ache os <b>lugares</b> da cidade escondidos no quadro.",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"ESCOLA",u"PRACA",u"HOSPITAL",u"LOJA",u"CASA"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"OS LUGARES",u"LETRAS":u"ACDEHILOPRSTUJ",u"DIFICIL":u"",u"CORP":[u"l1",u"l2",u"l3",u"l4",u"l5"]})
add(id=u"f11c", mec=u"caca-palavras", selo=u"CAÇA AO TRABALHO", conceito=u"objetivo2",
    enunciado=u"Ache os <b>trabalhos</b> de Blumenau escondidos no quadro.",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"MALHA",u"CERVEJA",u"ROCA",u"FEIRA",u"LOJA"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"O TRABALHO",u"LETRAS":u"ACEFGHIJLMORV",u"DIFICIL":u"",u"CORP":[u"t1",u"t2",u"t3",u"t4",u"t5"]})
add(id=u"f11d", mec=u"caca-palavras", selo=u"CAÇA AOS PASSEIOS", conceito=u"objetivo2",
    enunciado=u"Ache os <b>pontos turísticos</b> escondidos no quadro.",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"VILA",u"TEATRO",u"PONTE",u"PARQUE",u"MUSEU"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"OS PASSEIOS",u"LETRAS":u"AEILMNOPQRSTUV",u"DIFICIL":u"",u"CORP":[u"p1",u"p2",u"p3",u"p4",u"p5"]})

C[u"fases"]=fases; C[u"habilidades"]=HAB
with io.open(os.path.join(PASTA,u"conteudo.json"),u"w",encoding=u"utf-8") as f:
    f.write(json.dumps(C,ensure_ascii=False,indent=1))
nr=sum(len(x.get("dados")) if isinstance(x.get("dados"),list) else 1 for x in fases)
print(u"conteudo.json: %d fases, ~%d rodadas (%s)"%(len(fases),nr,C[u"titulo"]))
g={};o={}
for x in fases:
    g[x[u"mec"]]=g.get(x[u"mec"],0)+1; o[x[u"conceito"]]=o.get(x[u"conceito"],0)+1
print(u"gestos:",g); print(u"objetivos:",o)
