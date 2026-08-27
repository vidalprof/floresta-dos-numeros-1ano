# -*- coding: utf-8 -*-
u"""Gera _por4/conteudo.json — A OFICINA DAS PALAVRAS (4º ano, Português).

Molde ESQUELETO (mecânicas provadas + as dedicadas de sílaba do _trem e a
linha-do-tempo do _detetive), em BLOCOS (repetição seguida). Mascote REUSADO do
banco: o castor Téo (carpinteiro das palavras). Cenário: a oficina do Téo.

Temas do Marcos (4º ano):
  1) Aumentativo e diminutivo (a palavra cresce ou encolhe)
  2) Separação silábica (dividir a palavra em sílabas)
  3) Verbos no passado e no futuro (tempos verbais)
BNCC 4º ano: EF04LP03/EF35LP08 (morfologia: aumentativo/diminutivo); EF04LP01
(sílaba); EF04LP07/EF35LP10 (verbos e tempos verbais).
"""
import io, json, os
PASTA = os.path.dirname(os.path.abspath(__file__))
HAB = (u"Formar e reconhecer aumentativo e diminutivo; separar palavras em sílabas e "
       u"contar sílabas; identificar e empregar verbos no passado e no futuro. "
       u"EF04LP01/EF04LP03/EF04LP07 (4º ano).")

C = {
 u"titulo": u"A Oficina das Palavras", u"sub": u"Português · 4º ano · Palavras que crescem, encolhem, se dividem e viajam no tempo",
 u"ano": u"4º ano", u"prefixo": u"pw", u"mascote": u"robo", u"mascoteNome": u"Léxi",
 u"crachas": 6, u"mesa": u"Pedagogo do 4º ano + especialista em Língua Portuguesa (morfologia e verbos).",
 u"fundo": u"pw_fundo.png", u"fundoSuave": True, u"voz": u"masculina",
 u"abertura": (u"Olá! Eu sou o Léxi, o robô das palavras. Bem-vindo ao laboratório! "
              u"Aqui a gente faz a palavra CRESCER, ENCOLHER, corta ela em pedacinhos e até "
              u"faz ela viajar no tempo. Vamos brincar com as palavras?"),
 u"fim": (u"Que trabalho incrível! Você já sabe deixar a palavra grande e pequena, cortar em "
          u"sílabas e fazer o verbo ir para o passado e para o futuro. Você é um mestre das "
          u"palavras de verdade!"),
 u"conceitos": {
   u"objetivo1": u"Aumentativo e diminutivo (a palavra grande × pequena)",
   u"objetivo2": u"Separação silábica (os pedaços da palavra)",
   u"objetivo3": u"Verbos no passado e no futuro (tempos verbais)",
 },
 u"curriculo": {
   u"objetivo1": u"Formar e reconhecer aumentativo e diminutivo. EF04LP03/EF35LP08.",
   u"objetivo2": u"Separar palavras em sílabas e contar sílabas. EF04LP01.",
   u"objetivo3": u"Reconhecer e empregar verbos no passado e no futuro. EF04LP07/EF35LP10.",
 },
 u"fases": [],
}
fases=[]
def add(**k): fases.append(k)
def esc(img,p,c,cvoz,erradas,dicas,cimg=None,eimgs=None):
    # Neste Português as OPÇÕES são TEXTO (casinha, gatão, "2"...). A resposta é a
    # palavra TRANSFORMADA — que nunca casa com a figura da base. Por isso NÃO se
    # põe figura nas opções (o portão 1i reprovaria "CASINHA" com o desenho da
    # casa). A figura fica só no TOPO, ilustrando a palavra-base da pergunta.
    cop={u"t":c,u"voz":cvoz}
    es=[{u"t":t,u"voz":v} for (t,v) in erradas]
    return {u"img":img,u"p":p,u"c":cop,u"e":es,u"d":dicas}
DDIM=[u"Diminutivo deixa a palavra PEQUENA: -inho, -inha.",u"A casa pequena é a casinha; o gato pequeno é o gatinho.",u"Isso! É o <b>diminutivo</b>. Toque para seguir."]
DAUM=[u"Aumentativo deixa a palavra GRANDE: -ão.",u"A casa grande é o casarão; o gato grande é o gatão.",u"Isso! É o <b>aumentativo</b>. Toque para seguir."]
DSIL=[u"Bata uma palma para cada pedaço da palavra.",u"Diga devagar e conte os pedaços.",u"Isso! Toque para seguir."]
DTMP=[u"Passado é o que JÁ aconteceu (ontem); futuro é o que VAI acontecer (amanhã).",u"Ouça o verbo: ele já foi feito ou ainda vai ser?",u"Isso! Toque para seguir."]

# ============ BLOCO 1 — ESCOLHER (aum/dim · sílabas · verbo) ============
add(id=u"f01", mec=u"escolher", selo=u"PEQUENININHO", conceito=u"objetivo1",
    enunciado=u"O <b>diminutivo</b> deixa a palavra pequena. Ache o diminutivo.",
    dica=u"Diminutivo termina em -inho, -inha.",
    dados=[
     esc(u"pw_casa",u"Qual é o <b>diminutivo</b> de CASA (a casa pequena)?",u"CASINHA",u"casinha",[(u"CASARÃO",u"casarão"),(u"CASEBRE",u"casebre")],DDIM,cimg=u"pw_casa"),
     esc(u"pw_gato",u"Qual é o <b>diminutivo</b> de GATO?",u"GATINHO",u"gatinho",[(u"GATÃO",u"gatão"),(u"GATO",u"gato")],DDIM,cimg=u"pw_gato"),
     esc(u"pw_flor",u"Qual é o <b>diminutivo</b> de FLOR?",u"FLORZINHA",u"florzinha",[(u"FLORÃO",u"florão"),(u"FLORES",u"flores")],DDIM,cimg=u"pw_flor"),
    ])
add(id=u"f02", mec=u"escolher", selo=u"GRANDÃO", conceito=u"objetivo1",
    enunciado=u"O <b>aumentativo</b> deixa a palavra grande. Ache o aumentativo.",
    dica=u"Aumentativo termina em -ão.",
    dados=[
     esc(u"pw_gato",u"Qual é o <b>aumentativo</b> de GATO (o gato grande)?",u"GATÃO",u"gatão",[(u"GATINHO",u"gatinho"),(u"GATO",u"gato")],DAUM,cimg=u"pw_gato"),
     esc(u"pw_rato",u"Qual é o <b>aumentativo</b> de RATO?",u"RATÃO",u"ratão",[(u"RATINHO",u"ratinho"),(u"RATOS",u"ratos")],DAUM,cimg=u"pw_rato"),
     esc(u"pw_casa",u"Qual é o <b>aumentativo</b> de CASA?",u"CASARÃO",u"casarão",[(u"CASINHA",u"casinha"),(u"CASA",u"casa")],DAUM,cimg=u"pw_casa"),
    ])
add(id=u"f03", mec=u"escolher", selo=u"CONTE OS PEDAÇOS", conceito=u"objetivo2",
    enunciado=u"Cada <b>sílaba</b> é um pedaço da palavra. Quantas sílabas?",
    dica=u"Bata uma palma para cada pedaço: bo-la.",
    dados=[
     esc(u"pw_bola",u"Quantas sílabas tem <b>BOLA</b> (bo-la)?",u"2",u"duas",[(u"1",u"uma"),(u"3",u"três")],DSIL,cimg=u"pw_bola"),
     esc(u"pw_sapo",u"Quantas sílabas tem <b>SAPO</b> (sa-po)?",u"2",u"duas",[(u"3",u"três"),(u"1",u"uma")],DSIL,cimg=u"pw_sapo"),
     esc(u"pw_elefante",u"Quantas sílabas tem <b>ELEFANTE</b> (e-le-fan-te)?",u"4",u"quatro",[(u"3",u"três"),(u"2",u"duas")],DSIL,cimg=u"pw_elefante"),
    ])
add(id=u"f04", mec=u"escolher", selo=u"JÁ FOI OU VAI SER?", conceito=u"objetivo3",
    enunciado=u"O verbo no <b>passado</b> já aconteceu; no <b>futuro</b> vai acontecer.",
    dica=u"Passado = ontem. Futuro = amanhã.",
    dados=[
     esc(u"",u"“O menino <b>correu</b>.” Esse verbo está no...",u"PASSADO",u"passado, já aconteceu",[(u"FUTURO",u"futuro"),(u"NÃO É VERBO",u"não é verbo")],DTMP),
     esc(u"",u"“Amanhã eu <b>vou viajar</b>.” Esse verbo está no...",u"FUTURO",u"futuro, vai acontecer",[(u"PASSADO",u"passado"),(u"NÃO É VERBO",u"não é verbo")],DTMP),
     esc(u"",u"Qual verbo está no <b>passado</b>?",u"BRINCOU",u"brincou",[(u"VAI BRINCAR",u"vai brincar"),(u"BRINCAR",u"brincar")],DTMP),
    ])

add(id=u"f04b", mec=u"escolher", selo=u"GRANDÃO", conceito=u"objetivo1",
    enunciado=u"Ache o <b>aumentativo</b> (o grande).",
    dica=u"Aumentativo termina em -ão.",
    dados=[
     esc(u"pw_bola",u"Qual é o <b>aumentativo</b> de BOLA?",u"BOLÃO",u"bolão",[(u"BOLINHA",u"bolinha"),(u"BOLA",u"bola")],DAUM,cimg=u"pw_bola"),
     esc(u"pw_pato",u"Qual é o <b>aumentativo</b> de PATO?",u"PATÃO",u"patão",[(u"PATINHO",u"patinho"),(u"PATO",u"pato")],DAUM,cimg=u"pw_pato"),
     esc(u"pw_sapo",u"Qual é o <b>aumentativo</b> de SAPO?",u"SAPÃO",u"sapão",[(u"SAPINHO",u"sapinho"),(u"SAPO",u"sapo")],DAUM,cimg=u"pw_sapo"),
    ])
add(id=u"f04c", mec=u"escolher", selo=u"CONTE OS PEDAÇOS", conceito=u"objetivo2",
    enunciado=u"Quantas <b>sílabas</b> tem a palavra?",
    dica=u"Bata uma palma para cada pedaço.",
    dados=[
     esc(u"pw_pato",u"Quantas sílabas tem <b>PATO</b> (pa-to)?",u"2",u"duas",[(u"1",u"uma"),(u"3",u"três")],DSIL,cimg=u"pw_pato"),
     esc(u"pw_navio",u"Quantas sílabas tem <b>NAVIO</b> (na-vi-o)?",u"3",u"três",[(u"2",u"duas"),(u"4",u"quatro")],DSIL,cimg=u"pw_navio"),
     esc(u"pw_vaca",u"Quantas sílabas tem <b>VACA</b> (va-ca)?",u"2",u"duas",[(u"3",u"três"),(u"1",u"uma")],DSIL,cimg=u"pw_vaca"),
    ])

# ============ BLOCO 2 — CLASSIFICAR (aum×dim · passado×futuro) ============
def classif(idf,selo,ka,na,kb,nb,fichas,dicas,conc):
    return dict(id=idf, mec=u"classificar", selo=selo, conceito=conc,
      enunciado=u"Coloque cada palavra na caixa <b>%s</b> ou <b>%s</b>."%(na,nb),
      dica=u"Leia a palavra e pense em que caixa ela mora.",
      dados=[{u"k":ka,u"n":na,u"img":u"",u"voz":na.lower(),u"rot":False},
             {u"k":kb,u"n":nb,u"img":u"",u"voz":nb.lower(),u"rot":False}],
      dadosExtra={u"ENUN":u"Cada palavra na sua caixa: <b>%s</b> ou <b>%s</b>?"%(na,nb),u"FICHAS":fichas,u"DICAS":dicas})
add(**classif(u"f05",u"GRANDE OU PEQUENO",u"aum",u"AUMENTATIVO",u"dim",u"DIMINUTIVO",
    [{u"t":u"casinha",u"alvo":u"dim"},{u"t":u"gatão",u"alvo":u"aum"},
     {u"t":u"livrinho",u"alvo":u"dim"},{u"t":u"narigão",u"alvo":u"aum"},
     {u"t":u"florzinha",u"alvo":u"dim"},{u"t":u"ratão",u"alvo":u"aum"}],
    [u"Termina em -inho/-inha? É diminutivo.",u"Termina em -ão? É aumentativo.",u"Muito bem! Toque para seguir."],u"objetivo1"))
add(**classif(u"f05b",u"GRANDE OU PEQUENO",u"aum",u"AUMENTATIVO",u"dim",u"DIMINUTIVO",
    [{u"t":u"patinho",u"alvo":u"dim"},{u"t":u"casarão",u"alvo":u"aum"},
     {u"t":u"bolinha",u"alvo":u"dim"},{u"t":u"bocão",u"alvo":u"aum"},
     {u"t":u"sapinho",u"alvo":u"dim"},{u"t":u"cachorrão",u"alvo":u"aum"}],
    [u"Pequeno: -inho/-inha.",u"Grande: -ão.",u"Você separa muito bem! Toque para seguir."],u"objetivo1"))
add(**classif(u"f06",u"ONTEM OU AMANHÃ",u"pas",u"PASSADO",u"fut",u"FUTURO",
    [{u"t":u"brincou",u"alvo":u"pas"},{u"t":u"vai pular",u"alvo":u"fut"},
     {u"t":u"comeu",u"alvo":u"pas"},{u"t":u"vai correr",u"alvo":u"fut"},
     {u"t":u"estudou",u"alvo":u"pas"},{u"t":u"vai cantar",u"alvo":u"fut"}],
    [u"Já aconteceu (ontem)? PASSADO.",u"Ainda vai acontecer (amanhã)? FUTURO.",u"Isso mesmo! Toque para seguir."],u"objetivo3"))

add(**classif(u"f06b",u"ONTEM OU AMANHÃ",u"pas",u"PASSADO",u"fut",u"FUTURO",
    [{u"t":u"cantou",u"alvo":u"pas"},{u"t":u"vai dançar",u"alvo":u"fut"},
     {u"t":u"dormiu",u"alvo":u"pas"},{u"t":u"vai viajar",u"alvo":u"fut"},
     {u"t":u"jogou",u"alvo":u"pas"},{u"t":u"vai ler",u"alvo":u"fut"}],
    [u"Já aconteceu (ontem)? PASSADO.",u"Ainda vai acontecer (amanhã)? FUTURO.",u"Você separa muito bem! Toque para seguir."],u"objetivo3"))

# ============ BLOCO 3 — BATER-SÍLABAS ============
add(id=u"f07", mec=u"bater-silabas", selo=u"BATA AS SÍLABAS", conceito=u"objetivo2",
    enunciado=u"<b>Bata 1 vez</b> para cada sílaba e depois toque em <b>Pronto</b>.",
    dica=u"Ponha a mão no queixo: ele desce a cada sílaba.",
    dados=[
     {u"pal":u"BOLA",u"sil":[u"BO",u"LA"],u"voz":u"bo... la",u"fig":u"pw_bola",
      u"d":[u"Diga <b>BOLA</b> devagar e bata uma vez para cada pedaço.",u"Escute o ritmo: bo... la.",u"São <b>2</b> pedaços: bo... la. Toque em Pronto."]},
     {u"pal":u"CASA",u"sil":[u"CA",u"SA"],u"voz":u"ca... sa",u"fig":u"pw_casa",
      u"d":[u"Mão no queixo e diga CASA. Ele desce a cada pedaço.",u"Conte as batidas: ca... sa.",u"São <b>2</b> pedaços: ca... sa. Toque em Pronto."]},
     {u"pal":u"GATO",u"sil":[u"GA",u"TO"],u"voz":u"ga... to",u"fig":u"pw_gato",
      u"d":[u"Diga GATO devagar e bata palma a cada pedaço.",u"São dois pulinhos da boca.",u"São <b>2</b> pedaços: ga... to. Toque em Pronto."]},
    ])
add(id=u"f07b", mec=u"bater-silabas", selo=u"BATA AS SÍLABAS", conceito=u"objetivo2",
    enunciado=u"<b>Bata 1 vez</b> para cada sílaba e toque em <b>Pronto</b>.",
    dica=u"Diga a palavra devagar e bata uma vez a cada pedaço.",
    dados=[
     {u"pal":u"SAPO",u"sil":[u"SA",u"PO"],u"voz":u"sa... po",u"fig":u"pw_sapo",
      u"d":[u"Diga <b>SAPO</b> devagar e bata a cada pedaço.",u"Conte: sa... po.",u"São <b>2</b> pedaços: sa... po. Toque em Pronto."]},
     {u"pal":u"ABELHA",u"sil":[u"A",u"BE",u"LHA"],u"voz":u"a... be... lha",u"fig":u"pw_abelha",
      u"d":[u"Diga <b>ABELHA</b> devagar: a... be... lha.",u"Conte as batidas com o queixo.",u"São <b>3</b> pedaços: a... be... lha. Toque em Pronto."]},
     {u"pal":u"JACARÉ",u"sil":[u"JA",u"CA",u"RÉ"],u"voz":u"ja... ca... ré",u"fig":u"pw_jacare",
      u"d":[u"Diga <b>JACARÉ</b> bem devagar.",u"São três pulinhos: ja... ca... ré.",u"São <b>3</b> pedaços: ja... ca... ré. Toque em Pronto."]},
    ])

add(id=u"f07c", mec=u"bater-silabas", selo=u"BATA AS SÍLABAS", conceito=u"objetivo2",
    enunciado=u"<b>Bata 1 vez</b> para cada sílaba e toque em <b>Pronto</b>.",
    dica=u"Quanto mais pedaços tem a palavra, mais vezes você bate.",
    dados=[
     {u"pal":u"RATO",u"sil":[u"RA",u"TO"],u"voz":u"ra... to",u"fig":u"pw_rato",
      u"d":[u"Diga <b>RATO</b> devagar: ra... to.",u"Bata a cada pedaço.",u"São <b>2</b> pedaços: ra... to. Toque em Pronto."]},
     {u"pal":u"NAVIO",u"sil":[u"NA",u"VI",u"O"],u"voz":u"na... vi... o",u"fig":u"pw_navio",
      u"d":[u"Diga <b>NAVIO</b> devagar: na... vi... o.",u"São três pulinhos.",u"São <b>3</b> pedaços: na... vi... o. Toque em Pronto."]},
     {u"pal":u"ELEFANTE",u"sil":[u"E",u"LE",u"FAN",u"TE"],u"voz":u"e... le... fan... te",u"fig":u"pw_elefante",
      u"d":[u"Diga <b>ELEFANTE</b> bem devagar: e... le... fan... te.",u"Conte os quatro pedaços.",u"São <b>4</b> pedaços: e... le... fan... te. Toque em Pronto."]},
    ])

# ============ BLOCO 4 — JUNTAR-SÍLABAS (monte a palavra) ============
add(id=u"f08", mec=u"juntar-silabas", selo=u"MONTE A PALAVRA", conceito=u"objetivo2",
    enunciado=u"Junte os <b>pedaços</b> na ordem certa e forme a palavra.",
    dica=u"Diga a palavra devagar: qual pedaço vem primeiro?",
    dados=[
     {u"pal":u"PATO",u"sil":[u"PA",u"TO"],u"img":u"pw_pato",u"iscas":[u"MA",u"LO"],u"lento":u"PA... TO",
      u"d":[u"Diga <b>PA-TO</b>. Qual pedaço vem primeiro?",u"Começa com <b>PA</b>; depois vem <b>TO</b>.",u"A ordem é PA, depois TO. Toque no pedaço aceso."]},
     {u"pal":u"VACA",u"sil":[u"VA",u"CA"],u"img":u"pw_vaca",u"iscas":[u"FA",u"LO"],u"lento":u"VA... CA",
      u"d":[u"Diga <b>VA-CA</b> devagar. Qual vem no começo?",u"Primeiro <b>VA</b>, depois <b>CA</b>.",u"A ordem é VA, depois CA. Toque no pedaço aceso."]},
     {u"pal":u"RATO",u"sil":[u"RA",u"TO"],u"img":u"pw_rato",u"iscas":[u"BO",u"SA"],u"lento":u"RA... TO",
      u"d":[u"Diga <b>RA-TO</b>. Qual pedaço abre a palavra?",u"Começa com <b>RA</b>; depois vem <b>TO</b>.",u"A ordem é RA, depois TO. Toque no pedaço aceso."]},
    ])
add(id=u"f08b", mec=u"juntar-silabas", selo=u"MONTE A PALAVRA", conceito=u"objetivo2",
    enunciado=u"Junte os <b>três pedaços</b> na ordem certa.",
    dica=u"Fale a palavra devagar e escute os três pedaços.",
    dados=[
     {u"pal":u"NAVIO",u"sil":[u"NA",u"VI",u"O"],u"img":u"pw_navio",u"iscas":[u"LO",u"MI"],u"lento":u"NA... VI... O",
      u"d":[u"Diga <b>NA-VI-O</b> devagar.",u"Começa com <b>NA</b>, depois <b>VI</b>, depois <b>O</b>.",u"A ordem é NA, VI, O. Toque no pedaço aceso."]},
     {u"pal":u"ZEBRA",u"sil":[u"ZE",u"BRA"],u"img":u"pw_zebra",u"iscas":[u"TU",u"LO"],u"lento":u"ZE... BRA",
      u"d":[u"Diga <b>ZE-BRA</b> devagar. Qual pedaço vem primeiro?",u"Começa com <b>ZE</b>, depois <b>BRA</b>.",u"A ordem é ZE, BRA. Toque no pedaço aceso."]},
    ])

add(id=u"f08c", mec=u"juntar-silabas", selo=u"MONTE A PALAVRA", conceito=u"objetivo2",
    enunciado=u"Junte os <b>pedaços</b> na ordem certa e forme a palavra.",
    dica=u"Diga a palavra devagar e escute os pedaços.",
    dados=[
     {u"pal":u"ABELHA",u"sil":[u"A",u"BE",u"LHA"],u"img":u"pw_abelha",u"iscas":[u"MO",u"TU"],u"lento":u"A... BE... LHA",
      u"d":[u"Diga <b>A-BE-LHA</b> devagar.",u"Começa com <b>A</b>, depois <b>BE</b>, depois <b>LHA</b>.",u"A ordem é A, BE, LHA. Toque no pedaço aceso."]},
     {u"pal":u"JACARÉ",u"sil":[u"JA",u"CA",u"RÉ"],u"img":u"pw_jacare",u"iscas":[u"BO",u"LI"],u"lento":u"JA... CA... RÉ",
      u"d":[u"Diga <b>JA-CA-RÉ</b> devagar.",u"Começa com <b>JA</b>, depois <b>CA</b>, depois <b>RÉ</b>.",u"A ordem é JA, CA, RÉ. Toque no pedaço aceso."]},
    ])

# ============ BLOCO 5 — LIGAR (figura -> diminutivo / aumentativo) ============
add(id=u"f09", mec=u"ligar", selo=u"CADA UM NO SEU PEQUENO", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>figura</b> ao seu <b>diminutivo</b>.",
    dica=u"Diminutivo deixa pequeno: -inho, -inha.",
    dados=[{u"k":u"d0",u"img":u"pw_casa",u"voz":u"casa",u"s":u"CASINHA"},
           {u"k":u"d1",u"img":u"pw_gato",u"voz":u"gato",u"s":u"GATINHO"},
           {u"k":u"d2",u"img":u"pw_flor",u"voz":u"flor",u"s":u"FLORZINHA"},
           {u"k":u"d3",u"img":u"pw_pato",u"voz":u"pato",u"s":u"PATINHO"}],
    dadosExtra={u"ENUN":u"Ligue cada figura ao seu <b>diminutivo</b> (o pequeno).",
                u"DICAS":[u"Casa vira casinha; gato vira gatinho.",u"Flor vira florzinha; pato vira patinho."],
                u"FECHO":u"Você formou todos os diminutivos!"})
add(id=u"f09b", mec=u"ligar", selo=u"CADA UM NO SEU GRANDE", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>figura</b> ao seu <b>aumentativo</b>.",
    dica=u"Aumentativo deixa grande: -ão.",
    dados=[{u"k":u"a0",u"img":u"pw_gato",u"voz":u"gato",u"s":u"GATÃO"},
           {u"k":u"a1",u"img":u"pw_rato",u"voz":u"rato",u"s":u"RATÃO"},
           {u"k":u"a2",u"img":u"pw_sapo",u"voz":u"sapo",u"s":u"SAPÃO"},
           {u"k":u"a3",u"img":u"pw_casa",u"voz":u"casa",u"s":u"CASARÃO"}],
    dadosExtra={u"ENUN":u"Ligue cada figura ao seu <b>aumentativo</b> (o grande).",
                u"DICAS":[u"Gato vira gatão; rato vira ratão.",u"Sapo vira sapão; casa vira casarão."],
                u"FECHO":u"Você formou todos os aumentativos!"})

add(id=u"f09c", mec=u"ligar", selo=u"CADA UM NO SEU PEQUENO", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>figura</b> ao seu <b>diminutivo</b>.",
    dica=u"Diminutivo deixa pequeno: -inho, -inha.",
    dados=[{u"k":u"e0",u"img":u"pw_bola",u"voz":u"bola",u"s":u"BOLINHA"},
           {u"k":u"e1",u"img":u"pw_sapo",u"voz":u"sapo",u"s":u"SAPINHO"},
           {u"k":u"e2",u"img":u"pw_vaca",u"voz":u"vaca",u"s":u"VAQUINHA"},
           {u"k":u"e3",u"img":u"pw_rato",u"voz":u"rato",u"s":u"RATINHO"}],
    dadosExtra={u"ENUN":u"Ligue cada figura ao seu <b>diminutivo</b> (o pequeno).",
                u"DICAS":[u"Bola vira bolinha; sapo vira sapinho.",u"Vaca vira vaquinha; rato vira ratinho."],
                u"FECHO":u"Você formou todos os diminutivos!"})

# ============ AQUECIMENTO (revisão espaçada) — no MEIO ============
add(id=u"aquecimento", mec=u"escolher", selo=u"AQUECIMENTO", conceito=u"objetivo1",
    enunciado=u"Vamos <b>lembrar</b>: qual é o <b>diminutivo</b>?",
    dica=u"Diminutivo é o pequeno: -inho, -inha.",
    dados=[
     esc(u"pw_pato",u"Qual é o <b>diminutivo</b> de PATO?",u"PATINHO",u"patinho",[(u"PATÃO",u"patão"),(u"PATO",u"pato")],DDIM,cimg=u"pw_pato"),
     esc(u"pw_rato",u"E qual é o <b>diminutivo</b> de RATO?",u"RATINHO",u"ratinho",[(u"RATÃO",u"ratão"),(u"RATOS",u"ratos")],DDIM,cimg=u"pw_rato"),
     esc(u"pw_sapo",u"Agora, o <b>diminutivo</b> de SAPO?",u"SAPINHO",u"sapinho",[(u"SAPÃO",u"sapão"),(u"SAPO",u"sapo")],DDIM,cimg=u"pw_sapo"),
    ])

# ============ BLOCO 6 — LINHA DO TEMPO (verbo: ontem/hoje/amanhã) ============
add(id=u"f10", mec=u"linha-do-tempo", selo=u"A VIAGEM DO VERBO", conceito=u"objetivo3",
    enunciado=u"Coloque as frases na <b>ordem do tempo</b>: do passado para o futuro.",
    dica=u"Ontem (passado) vem primeiro; amanhã (futuro) vem por último.",
    dados=[{u"t":1,u"n":u"Ontem eu brinquei no parque."},
           {u"t":2,u"n":u"Hoje eu brinco na escola."},
           {u"t":3,u"n":u"Amanhã eu vou brincar na praça."}])

# ============ BLOCO 7 — QUEM-SOU-EU (o tempo do verbo) ============
add(id=u"f11", mec=u"quem-sou-eu", selo=u"QUE TEMPO SOU EU?", conceito=u"objetivo3",
    enunciado=u"Ouça as pistas e descubra o <b>tempo do verbo</b>.",
    dica=u"Pense se a ação já foi feita ou ainda vai ser.",
    dados=[
     {u"resp":u"O PASSADO",u"pistas":[u"Eu falo do que <b>já aconteceu</b>.",u"Combino com a palavra <b>ontem</b>.",u"“Brincou”, “comeu” e “correu” são meus."],u"outros":[u"O FUTURO",u"O PRESENTE",u"O DESENHO"]},
     {u"resp":u"O FUTURO",u"pistas":[u"Eu falo do que <b>ainda vai acontecer</b>.",u"Combino com a palavra <b>amanhã</b>.",u"“Vai brincar” e “vou viajar” são meus."],u"outros":[u"O PASSADO",u"O PRESENTE",u"A SÍLABA"]},
     {u"resp":u"O DIMINUTIVO",u"pistas":[u"Eu deixo a palavra <b>pequena</b>.",u"Termino em <b>-inho</b> ou <b>-inha</b>.",u"Casinha e gatinho foram feitos por mim."],u"outros":[u"O AUMENTATIVO",u"A SÍLABA",u"O VERBO"]},
    ])

# ============ BLOCO 8 — INTRUSO ============
add(id=u"f12", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo1",
    enunciado=u"Três são <b>diminutivos</b>. Ache o que NÃO é.",
    dica=u"Um deles é o grandão, não o pequenininho.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
      u"enun":u"Três são <b>diminutivos</b> (pequenos). Qual NÃO é?",
      u"itens":[{u"k":u"a",u"n":u"casinha"},{u"k":u"b",u"n":u"gatinho"},{u"k":u"c",u"n":u"florzinha"},{u"k":u"d",u"n":u"casarão"}],
      u"fora":u"d", u"nomeFora":u"casarão",
      u"d1":u"Três deixam a palavra pequena; um deixa grande.",
      u"d2":u"Casinha, gatinho e florzinha terminam em -inho/-inha.",
      u"d3":u"O de fora é <b>casarão</b>: termina em -ão, é aumentativo (grande).",
      u"razoes":[{u"t":u"Termina em -ão: é aumentativo, não diminutivo.",u"ok":1},{u"t":u"Porque é a maior palavra.",u"ok":0},{u"t":u"Porque começa com C.",u"ok":0}],
      u"enunPorque":u"Por que <b>casarão</b> é o intruso? Toque na razão certa.",
      u"p1":u"Olhe o final da palavra.",u"p2":u"Não é sobre o tamanho da escrita.",u"p3":u"É sobre -inho (pequeno) × -ão (grande)."}])
add(id=u"f12b", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo3",
    enunciado=u"Três são verbos no <b>passado</b>. Ache o intruso.",
    dica=u"Um deles ainda vai acontecer.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
      u"enun":u"Três verbos <b>já aconteceram</b> (passado). Qual NÃO?",
      u"itens":[{u"k":u"a",u"n":u"brincou"},{u"k":u"b",u"n":u"comeu"},{u"k":u"c",u"n":u"correu"},{u"k":u"d",u"n":u"vai pular"}],
      u"fora":u"d", u"nomeFora":u"vai pular",
      u"d1":u"Três já foram feitos; um ainda vai ser.",
      u"d2":u"Brincou, comeu e correu já aconteceram.",
      u"d3":u"O de fora é <b>vai pular</b>: ainda vai acontecer, é futuro.",
      u"razoes":[{u"t":u"Ainda não aconteceu: é futuro, não passado.",u"ok":1},{u"t":u"Porque tem duas palavras.",u"ok":0},{u"t":u"Porque começa com V.",u"ok":0}],
      u"enunPorque":u"Por que <b>vai pular</b> é o intruso? Toque na razão certa.",
      u"p1":u"Pense se a ação já foi feita.",u"p2":u"Não é sobre o número de palavras.",u"p3":u"É sobre passado (ontem) × futuro (amanhã)."}])

add(id=u"f12c", mec=u"intruso", selo=u"ACHE O INTRUSO", conceito=u"objetivo1",
    enunciado=u"Três são <b>aumentativos</b>. Ache o que NÃO é.",
    dica=u"Um deles é o pequenininho, não o grandão.",
    dados=[{u"selo":u"ACHE O INTRUSO", u"tipo":u"texto",
      u"enun":u"Três são <b>aumentativos</b> (grandes). Qual NÃO é?",
      u"itens":[{u"k":u"a",u"n":u"gatão"},{u"k":u"b",u"n":u"ratão"},{u"k":u"c",u"n":u"casarão"},{u"k":u"d",u"n":u"gatinho"}],
      u"fora":u"d", u"nomeFora":u"gatinho",
      u"d1":u"Três deixam a palavra grande; um deixa pequena.",
      u"d2":u"Gatão, ratão e casarão terminam em -ão.",
      u"d3":u"O de fora é <b>gatinho</b>: termina em -inho, é diminutivo (pequeno).",
      u"razoes":[{u"t":u"Termina em -inho: é diminutivo, não aumentativo.",u"ok":1},{u"t":u"Porque é a menor palavra.",u"ok":0},{u"t":u"Porque fala de gato.",u"ok":0}],
      u"enunPorque":u"Por que <b>gatinho</b> é o intruso? Toque na razão certa.",
      u"p1":u"Olhe o final da palavra.",u"p2":u"Não é sobre o tamanho da escrita.",u"p3":u"É sobre -ão (grande) × -inho (pequeno)."}])

# ============ BLOCO 9 — MEMÓRIA (figura ↔ diminutivo) ============
add(id=u"f13", mec=u"memoria", selo=u"MEMÓRIA DAS PALAVRAS", conceito=u"objetivo1",
    enunciado=u"Ache os pares: a <b>figura</b> e o seu <b>diminutivo</b>.",
    dica=u"Vire duas cartas e ache o par: a figura e o nome pequeno dela.",
    dados=[
     {u"k":u"casa", u"pal":u"CASINHA", u"fig":u"pw_casa", u"sen":u"a casa pequena", u"figsen":u"pw_casa"},
     {u"k":u"gato", u"pal":u"GATINHO", u"fig":u"pw_gato", u"sen":u"o gato pequeno", u"figsen":u"pw_gato"},
     {u"k":u"flor", u"pal":u"FLORZINHA", u"fig":u"pw_flor", u"sen":u"a flor pequena", u"figsen":u"pw_flor"},
     {u"k":u"pato", u"pal":u"PATINHO", u"fig":u"pw_pato", u"sen":u"o pato pequeno", u"figsen":u"pw_pato"},
    ],
    dadosExtra={u"PARES":[
     {u"k":u"casa", u"pal":u"CASINHA", u"fig":u"pw_casa", u"sen":u"a casa pequena", u"figsen":u"pw_casa"},
     {u"k":u"gato", u"pal":u"GATINHO", u"fig":u"pw_gato", u"sen":u"o gato pequeno", u"figsen":u"pw_gato"},
     {u"k":u"flor", u"pal":u"FLORZINHA", u"fig":u"pw_flor", u"sen":u"a flor pequena", u"figsen":u"pw_flor"},
     {u"k":u"pato", u"pal":u"PATINHO", u"fig":u"pw_pato", u"sen":u"o pato pequeno", u"figsen":u"pw_pato"},
    ]})

# ============ BLOCO 10 — COMPLETAR (verbo · diminutivo) ============
add(id=u"f14", mec=u"completar", selo=u"COMPLETE O VERBO", conceito=u"objetivo3",
    enunciado=u"Preencha com o verbo no <b>passado</b> (o que já aconteceu).",
    dica=u"Passado combina com ONTEM.",
    dados=[{u"img":u"",u"ante":u"Ontem eu ",u"dep":u" com a bola.",u"cer":u"brinquei",u"out":[u"brinco",u"vou brincar"],u"dic":u"Ontem = passado: <b>brinquei</b>."},
           {u"img":u"",u"ante":u"Ontem o gato ",u"dep":u" o peixe.",u"cer":u"comeu",u"out":[u"come",u"vai comer"],u"dic":u"Ontem = passado: <b>comeu</b>."},
           {u"img":u"",u"ante":u"Ontem nós ",u"dep":u" muito no recreio.",u"cer":u"corremos",u"out":[u"corremos amanhã",u"vamos correr"],u"dic":u"Ontem = passado: <b>corremos</b>."}],
    dadosExtra={u"ENUN":u"Preencha com o verbo no <b>passado</b>.",u"FECHO":u"Muito bem! Verbo no passado é o que já aconteceu."})
add(id=u"f14b", mec=u"completar", selo=u"COMPLETE O VERBO", conceito=u"objetivo3",
    enunciado=u"Preencha com o verbo no <b>futuro</b> (o que ainda vai acontecer).",
    dica=u"Futuro combina com AMANHÃ.",
    dados=[{u"img":u"",u"ante":u"Amanhã eu ",u"dep":u" na escola.",u"cer":u"vou estudar",u"out":[u"estudei",u"estudo"],u"dic":u"Amanhã = futuro: <b>vou estudar</b>."},
           {u"img":u"",u"ante":u"Amanhã nós ",u"dep":u" um bolo.",u"cer":u"vamos fazer",u"out":[u"fizemos",u"fazemos ontem"],u"dic":u"Amanhã = futuro: <b>vamos fazer</b>."},
           {u"img":u"",u"ante":u"Amanhã o time ",u"dep":u" a partida.",u"cer":u"vai jogar",u"out":[u"jogou",u"joga ontem"],u"dic":u"Amanhã = futuro: <b>vai jogar</b>."}],
    dadosExtra={u"ENUN":u"Preencha com o verbo no <b>futuro</b>.",u"FECHO":u"Muito bem! Verbo no futuro é o que ainda vai acontecer."})
add(id=u"f14c", mec=u"completar", selo=u"GRANDE OU PEQUENO", conceito=u"objetivo1",
    enunciado=u"Preencha com o <b>diminutivo</b> ou o <b>aumentativo</b>.",
    dica=u"Pequeno: -inho/-inha. Grande: -ão.",
    dados=[{u"img":u"",u"ante":u"O gato pequeno é o ",u"dep":u".",u"cer":u"gatinho",u"out":[u"gatão",u"gato"],u"dic":u"Pequeno: <b>gatinho</b>."},
           {u"img":u"",u"ante":u"A casa grande é o ",u"dep":u".",u"cer":u"casarão",u"out":[u"casinha",u"casa"],u"dic":u"Grande: <b>casarão</b>."},
           {u"img":u"",u"ante":u"A flor pequena é a ",u"dep":u".",u"cer":u"florzinha",u"out":[u"florão",u"flor"],u"dic":u"Pequena: <b>florzinha</b>."}],
    dadosExtra={u"ENUN":u"Preencha com o diminutivo ou o aumentativo.",u"FECHO":u"Você forma o grande e o pequeno!"})

add(id=u"f14d", mec=u"completar", selo=u"GRANDE OU PEQUENO", conceito=u"objetivo1",
    enunciado=u"Preencha com o <b>diminutivo</b> ou o <b>aumentativo</b>.",
    dica=u"Pequeno: -inho/-inha. Grande: -ão.",
    dados=[{u"img":u"",u"ante":u"O rato grande é o ",u"dep":u".",u"cer":u"ratão",u"out":[u"ratinho",u"rato"],u"dic":u"Grande: <b>ratão</b>."},
           {u"img":u"",u"ante":u"O sapo pequeno é o ",u"dep":u".",u"cer":u"sapinho",u"out":[u"sapão",u"sapo"],u"dic":u"Pequeno: <b>sapinho</b>."},
           {u"img":u"",u"ante":u"A bola grande é o ",u"dep":u".",u"cer":u"bolão",u"out":[u"bolinha",u"bola"],u"dic":u"Grande: <b>bolão</b>."}],
    dadosExtra={u"ENUN":u"Preencha com o diminutivo ou o aumentativo.",u"FECHO":u"Você forma o grande e o pequeno!"})

# ============ BLOCO 11 — DIGITAR (escreva a palavra) ============
add(id=u"f15", mec=u"digitar", selo=u"ESCREVA O PEQUENO", conceito=u"objetivo1",
    enunciado=u"Escreva o <b>diminutivo</b> da figura, letra por letra.",
    dica=u"Diminutivo termina em -inho ou -inha.",
    dados=[{u"palavra":u"CASINHA",u"img":u"",u"voz":u"casinha",u"pista":u"A casa pequena. Escreva: Casinha.",u"dic":u"<b>Casinha</b>."},
           {u"palavra":u"GATINHO",u"img":u"",u"voz":u"gatinho",u"pista":u"O gato pequeno. Escreva: Gatinho.",u"dic":u"<b>Gatinho</b>."},
           {u"palavra":u"PATINHO",u"img":u"",u"voz":u"patinho",u"pista":u"O pato pequeno. Escreva: Patinho.",u"dic":u"<b>Patinho</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>diminutivo</b> da figura.",u"FECHO":u"Você escreveu os diminutivos!"})
add(id=u"f15b", mec=u"digitar", selo=u"ESCREVA O GRANDE", conceito=u"objetivo1",
    enunciado=u"Escreva o <b>aumentativo</b> da figura, letra por letra.",
    dica=u"Aumentativo termina em -ão.",
    dados=[{u"palavra":u"GATAO",u"img":u"",u"voz":u"gatão",u"pista":u"O gato grande. Escreva: Gatão.",u"dic":u"<b>Gatão</b>."},
           {u"palavra":u"RATAO",u"img":u"",u"voz":u"ratão",u"pista":u"O rato grande. Escreva: Ratão.",u"dic":u"<b>Ratão</b>."},
           {u"palavra":u"SAPAO",u"img":u"",u"voz":u"sapão",u"pista":u"O sapo grande. Escreva: Sapão.",u"dic":u"<b>Sapão</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>aumentativo</b> da figura.",u"FECHO":u"Você escreveu os aumentativos!"})
add(id=u"f15c", mec=u"digitar", selo=u"ESCREVA O VERBO", conceito=u"objetivo3",
    enunciado=u"Escreva o verbo no <b>passado</b>, letra por letra.",
    dica=u"Passado é o que já aconteceu (ontem).",
    dados=[{u"palavra":u"CORREU",u"img":u"",u"voz":u"correu",u"pista":u"O que o menino fez ontem. De correr, no passado. Escreva: Correu.",u"dic":u"<b>Correu</b>."},
           {u"palavra":u"PULOU",u"img":u"",u"voz":u"pulou",u"pista":u"O que o sapo fez ontem. De pular, no passado. Escreva: Pulou.",u"dic":u"<b>Pulou</b>."},
           {u"palavra":u"CANTOU",u"img":u"",u"voz":u"cantou",u"pista":u"O que o pássaro fez ontem. De cantar, no passado. Escreva: Cantou.",u"dic":u"<b>Cantou</b>."}],
    dadosExtra={u"ENUN":u"Escreva o verbo no <b>passado</b>.",u"FECHO":u"Você escreveu os verbos no passado!"})

add(id=u"f15d", mec=u"digitar", selo=u"ESCREVA O PEQUENO", conceito=u"objetivo1",
    enunciado=u"Escreva o <b>diminutivo</b> da figura, letra por letra.",
    dica=u"Diminutivo termina em -inho ou -inha.",
    dados=[{u"palavra":u"BOLINHA",u"img":u"",u"voz":u"bolinha",u"pista":u"A bola pequena. Escreva: Bolinha.",u"dic":u"<b>Bolinha</b>."},
           {u"palavra":u"SAPINHO",u"img":u"",u"voz":u"sapinho",u"pista":u"O sapo pequeno. Escreva: Sapinho.",u"dic":u"<b>Sapinho</b>."},
           {u"palavra":u"RATINHO",u"img":u"",u"voz":u"ratinho",u"pista":u"O rato pequeno. Escreva: Ratinho.",u"dic":u"<b>Ratinho</b>."}],
    dadosExtra={u"ENUN":u"Escreva o <b>diminutivo</b> da figura.",u"FECHO":u"Você escreveu mais diminutivos!"})

# ============ FECHO — CAÇA-PALAVRAS ============
add(id=u"f16", mec=u"caca-palavras", selo=u"CAÇA AOS PEQUENOS", conceito=u"objetivo1",
    enunciado=u"Ache os <b>diminutivos</b> escondidos no quadro.",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"GATINHO",u"PATINHO",u"BOLINHA",u"CASINHA",u"SAPINHO",u"FLORZINHA"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"OS PEQUENININHOS",u"LETRAS":u"ABCFGHIJLNOPRSTZ",u"DIFICIL":u"",u"CORP":[u"c1",u"c2",u"c3",u"c4",u"c5",u"c6"]})
add(id=u"f16b", mec=u"caca-palavras", selo=u"CAÇA AOS VERBOS", conceito=u"objetivo3",
    enunciado=u"Ache os <b>verbos no passado</b> escondidos no quadro.",
    dica=u"Estão deitados (→), em pé (↓) e na diagonal.",
    dados=[u"BRINCOU",u"COMEU",u"CORREU",u"PULOU",u"CANTOU",u"ESTUDOU"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"O QUE JÁ ACONTECEU",u"LETRAS":u"ABCDEIMNOPRSTUV",u"DIFICIL":u"",u"CORP":[u"v1",u"v2",u"v3",u"v4",u"v5",u"v6"]})
add(id=u"f16c", mec=u"caca-palavras", selo=u"CAÇA ÀS PALAVRAS", conceito=u"objetivo2",
    enunciado=u"Ache as <b>palavras</b> escondidas no quadro.",
    dica=u"Depois de achar, tente contar as sílabas de cada uma.",
    dados=[u"BOLA",u"CASA",u"GATO",u"SAPO",u"PATO",u"FLOR",u"VACA"],
    dadosExtra={u"MODO":u"lista",u"TITULO":u"A OFICINA",u"LETRAS":u"ABCFGLOPRSTUV",u"DIFICIL":u"",u"CORP":[u"p1",u"p2",u"p3",u"p4",u"p5",u"p6",u"p7"]})

C[u"fases"]=fases; C[u"habilidades"]=HAB
with io.open(os.path.join(PASTA,u"conteudo.json"),u"w",encoding=u"utf-8") as f:
    f.write(json.dumps(C,ensure_ascii=False,indent=1))
nr=sum(len(x.get("dados")) if isinstance(x.get("dados"),list) else 1 for x in fases)
print(u"conteudo.json: %d fases, ~%d rodadas (%s)"%(len(fases),nr,C[u"titulo"]))
g={};o={}
for x in fases:
    g[x[u"mec"]]=g.get(x[u"mec"],0)+1; o[x[u"conceito"]]=o.get(x[u"conceito"],0)+1
print(u"gestos:",g); print(u"objetivos:",o)
