# -*- coding: utf-8 -*-
u"""
O TREM DO ALFABETO — 1º ano — build do conteudo.json (motor ESQUELETO).

Conteúdo (BNCC 1º ano, Língua Portuguesa):
  obj1 — O ALFABETO: nomear e pôr as letras na ordem (EF01LP10 / EF01LP04)
  obj2 — SÍLABAS: inicial, medial e final (EF01LP09 / EF01LP08)
  obj3 — FORMAR PALAVRAS SIMPLES: montar e escrever (EF01LP02 / EF01LP13)

Filosofia EDUVERSE: o problema vem ANTES do conceito (o trem embaralhou, sem as
letras na ordem ele não anda). Concreto -> figural -> simbólico. Andaime que
cresce. Mascote Coru (corujinha maquinista), voz masculina (Antonio).

Arte (já recortada em _trem/img/): 26 figuras de letra (tr_abelha ... tr_zebra),
6 crachás (tr_cr1..6), tr_coru_feliz/fala/pisca, tr_medalha, tr_trem, tr_fundo.
"""
import json, io, os, collections

# ---- o alfabeto ilustrado: letra -> (palavra com acento, figura) ----
ALFA = [
 ("A","ABELHA","tr_abelha"),   ("B","BOLA","tr_bola"),      ("C","CASA","tr_casa"),
 ("D","DADO","tr_dado"),       ("E","ELEFANTE","tr_elefante"),("F","FLOR","tr_flor"),
 ("G","GATO","tr_gato"),       ("H","HIPOPÓTAMO","tr_hipopotamo"),("I","IGREJA","tr_igreja"),
 ("J","JACARÉ","tr_jacare"),   ("K","KIWI","tr_kiwi"),      ("L","LEÃO","tr_leao"),
 ("M","MAÇÃ","tr_maca"),       ("N","NAVIO","tr_navio"),    ("O","OVO","tr_ovo"),
 ("P","PATO","tr_pato"),       ("Q","QUEIJO","tr_queijo"),  ("R","RATO","tr_rato"),
 ("S","SAPO","tr_sapo"),       ("T","TREM","tr_trem"),      ("U","UVA","tr_uva"),
 ("V","VACA","tr_vaca"),       ("W","WAFFLE","tr_waffle"),  ("X","XÍCARA","tr_xicara"),
 ("Y","YOYO","tr_yoyo"),       ("Z","ZEBRA","tr_zebra"),
]
FIG = {l: img for (l, p, img) in ALFA}      # letra -> figura
PAL = {l: p   for (l, p, img) in ALFA}      # letra -> palavra
# ⚠️ LIÇÃO PAGA (Marcos ouviu, ago/2026): o edge-tts lê a VOGAL solta como
# PALAVRA — "E" vira a conjunção "e" (=i) e "O" vira o artigo "o" (=u). Assim
# "Letra E. E de elefante." saía "i de elefante" e "Letra O..." saía "u de ovo".
# O conserto é gravar o NOME FONÉTICO da letra (o que a criança deve OUVIR),
# mantendo a letra de verdade só no que aparece na tela (info/nome).
NOME_LETRA = {
 "A":"Á","B":"Bê","C":"Cê","D":"Dê","E":"É","F":"Éfe","G":"Gê","H":"Agá",
 "I":"Í","J":"Jóta","K":"Cá","L":"Éle","M":"Ême","N":"Ene","O":"Ó","P":"Pê",
 "Q":"Quê","R":"Érre","S":"Ésse","T":"Tê","U":"Ú","V":"Vê","W":"Dáblio",
 "X":"Xis","Y":"Ípsilon","Z":"Zê",
}
def nome_letra(l): return NOME_LETRA.get(l, l)
def img_de(letra): return FIG[letra]
def pal_de(letra): return PAL[letra]

fases = []
def add(**k): fases.append(k)

# ⭐ as 3 fases de PINTAR (pintar-canvas) só entram quando as line-arts de colorir
#    chegarem (tr_pintar_letra/trem/coru) — o Marcos gera pelos prompts em
#    PROMPTS-ARTE.md. Sem elas, a atividade fecha código 0 com as mecânicas
#    jogáveis; com elas, o build já as inclui automaticamente.
IMGDIR = os.path.join(os.path.dirname(__file__), "img")
def tem_pintar(n): return os.path.exists(os.path.join(IMGDIR, n + ".png"))
INCLUIR_PINTAR = tem_pintar("tr_pintar_letra") and tem_pintar("tr_pintar_trem") and tem_pintar("tr_pintar_coru")
def add_pintar(**k):
    if INCLUIR_PINTAR: fases.append(k)

# ============================================================
# BLOCO 1 — O ALFABETO (obj1): conhecer, nomear e ordenar
# ============================================================

# f01 — VITRINE: os vagões de A a M (toca, ouve o nome e a palavra)
add(id="f01", mec="vitrine", selo="O TREM CHEGOU", conceito="objetivo1",
    enunciado="Toque em cada <b>letra</b> e ouça o nome dela e a figura.",
    dica="Cada vagão leva uma letra. Toque para ouvir o nome dela.",
    dados=[{"img":FIG[l], "nome":l, "grupo":"VOGAL" if l in "AEIOU" else "CONSOANTE",
            "info":("%s de %s." % (l, PAL[l].lower())),
            "voz":("Letra %s. %s de %s." % (nome_letra(l), nome_letra(l), PAL[l].lower()))}
           for l in "ABCDEFGHIJKLM"])

# f02 — ORDENAR: os 5 primeiros vagões na ordem do alfabeto
add(id="f02", mec="ordenar", selo="EM ORDEM", conceito="objetivo1",
    enunciado="Coloque os <b>vagões</b> na ordem do alfabeto.",
    dica="Cante o ABC baixinho: qual letra vem primeiro?",
    dados=["A","B","C","D","E"],
    dadosExtra={"ORDTXT":{
      "selo":"O ABC DO TREM",
      "balao":"Ponha as letras na <b>ordem do alfabeto</b>: A, B, C...",
      "hint":"Toque na letra ou arraste até a fila do trem.",
      "d":["Cante o comecinho do ABC e ache a letra que vem AGORA.",
           "A que vem agora está piscando. Toque nela.",
           "Era esta! Vamos juntos: eu ponho e você continua."],
      "fim":"O trem ficou em ordem: A, B, C, D, E!"}})

# (f03 TRAÇAR-LETRA REMOVIDA — Marcos, ago/2026: "não ficou bom, não ficou igual
#  a fase de seguir as luzes do Circo do Teo". Idem f11.)

# f04 — ESCOLHER (imagens): qual figura começa com a letra?
add(id="f04", mec="escolher", selo="COMEÇA COM...", conceito="objetivo1",
    enunciado="Ache a <b>figura</b> que começa com a letra.",
    dica="Diga o nome de cada figura e escute o primeiro som.",
    dados=[
      {"p":"Qual figura começa com a letra <b>B</b>?",
       "c":{"t":"BOLA","img":"tr_bola","voz":"bola"},
       "e":[{"t":"GATO","img":"tr_gato","voz":"gato"},
            {"t":"SAPO","img":"tr_sapo","voz":"sapo"},
            {"t":"UVA","img":"tr_uva","voz":"uva"}],
       "d":["Diga o nome de cada figura e escute como ela COMEÇA.",
            "B faz o som /b/, como no comecinho de <b>bola</b>.",
            "É a BOLA. Ela está acesa: toque nela para seguir."]},
      {"p":"Qual figura começa com a letra <b>G</b>?",
       "c":{"t":"GATO","img":"tr_gato","voz":"gato"},
       "e":[{"t":"PATO","img":"tr_pato","voz":"pato"},
            {"t":"BOLA","img":"tr_bola","voz":"bola"},
            {"t":"OVO","img":"tr_ovo","voz":"ovo"}],
       "d":["Fale o nome de cada uma e escute o primeiro pedacinho.",
            "G começa com o mesmo som de <b>gato</b>: /g/... gato.",
            "É o GATO. Ele está aceso: toque nele para seguir."]},
      {"p":"Qual figura começa com a letra <b>S</b>?",
       "c":{"t":"SAPO","img":"tr_sapo","voz":"sapo"},
       "e":[{"t":"DADO","img":"tr_dado","voz":"dado"},
            {"t":"VACA","img":"tr_vaca","voz":"vaca"},
            {"t":"RATO","img":"tr_rato","voz":"rato"}],
       "d":["Diga cada nome devagar e ouça o comecinho.",
            "S faz o som /s/, como a cobra: <b>ssss</b>apo.",
            "É o SAPO. Ele está aceso: toque nele para seguir."]},
    ], dadosExtra={"TITULO":"A LETRA DO COMEÇO","SOIMG":True,
                   "FECHO":"Você já acha a figura pela letra do começo!"})

# f05 — LIGAR: figura -> letra inicial
add(id="f05", mec="ligar", selo="LIGUE", conceito="objetivo1",
    enunciado="Ligue cada <b>figura</b> à letra com que ela começa.",
    dica="Toque na figura para ouvir. Qual é o primeiro som dela?",
    dados=[{"k":"p0","t":"PATO","img":"tr_pato","voz":"pato","s":"Começa com P"},
           {"k":"p1","t":"UVA","img":"tr_uva","voz":"uva","s":"Começa com U"},
           {"k":"p2","t":"DADO","img":"tr_dado","voz":"dado","s":"Começa com D"},
           {"k":"p3","t":"VACA","img":"tr_vaca","voz":"vaca","s":"Começa com V"}],
    dadosExtra={"DICAS":[
      "Diga o nome da figura e escute a primeira letra.",
      "Pato começa com P, uva com U, dado com D, vaca com V. Siga a linha tracejada.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue cada figura à sua letra inicial.",
      "FECHO":"Você ligou cada figura à letra do começo!"})

# f06 — MEMÓRIA: letra <-> figura
add(id="f06", mec="memoria", selo="MEMÓRIA", conceito="objetivo1",
    enunciado="Ache a <b>letra</b> e a <b>figura</b> que combinam.",
    dica="Vire duas cartas: uma tem a letra, a outra a figura. Combinaram? É par!",
    dados=[
      {"k":"a","pal":"A","voz":"letra á","sen":"ABELHA","imgsen":"tr_abelha","vozsen":"abelha"},
      {"k":"c","pal":"C","voz":"letra cê","sen":"CASA","imgsen":"tr_casa","vozsen":"casa"},
      {"k":"o","pal":"O","voz":"letra ó","sen":"OVO","imgsen":"tr_ovo","vozsen":"ovo"},
      {"k":"p","pal":"P","voz":"letra pê","sen":"PATO","imgsen":"tr_pato","vozsen":"pato"}])

# f06c — PINTAR: colorir a letra grande (pausa criativa, obj1)
add_pintar(id="f06c", mec="pintar-canvas", selo="HORA DE PINTAR", conceito="objetivo1",
    enunciado="<b>Pinte</b> a letra do jeito que você quiser.",
    dica="Escolha uma cor e toque dentro do desenho para pintar.",
    dados=[{"selo":"PINTE A LETRA A","nome":"a letra A da abelha","voz":"a letra á, da abelha",
            "img":"tr_pintar_letra"}])

# f07 — ORDENAR: mais 5 vagões (F a J)
add(id="f07", mec="ordenar", selo="EM ORDEM", conceito="objetivo1",
    enunciado="Coloque estes <b>vagões</b> na ordem do alfabeto.",
    dica="Depois do E vem o F. Continue cantando o ABC.",
    dados=["F","G","H","I","J"],
    dadosExtra={"ORDTXT":{
      "selo":"MAIS VAGÕES",
      "balao":"Continue o alfabeto: <b>F, G, H...</b>",
      "hint":"Toque na letra ou arraste até a fila do trem.",
      "d":["Cante do F em diante e ache a letra que vem AGORA.",
           "A próxima letra está piscando. Toque nela.",
           "Era esta! Vamos juntos: eu ponho e você segue."],
      "fim":"Ficou em ordem: F, G, H, I, J!"}})

# f08 — ESCOLHER (texto): qual letra começa a palavra da figura
add(id="f08", mec="escolher", selo="QUE LETRA?", conceito="objetivo1",
    enunciado="Olhe a figura e escolha a <b>letra do começo</b>.",
    dica="Diga o nome da figura bem devagar e escute a primeira letra.",
    dados=[
      {"img":"tr_casa","p":"Com que letra começa <b>CASA</b>?",
       "c":"C","e":["S","A","D"],
       "d":["Diga: <b>ca</b>-sa. Que som vem primeiro?",
            "É o som /k/, que a letra C faz aqui.",
            "É o C. Ele está aceso: toque nele para seguir."]},
      {"img":"tr_navio","p":"Com que letra começa <b>NAVIO</b>?",
       "c":"N","e":["M","V","A"],
       "d":["Diga: <b>na</b>-vi-o. Escute o comecinho.",
            "É o som /n/, do nariz: nnn... navio.",
            "É o N. Ele está aceso: toque nele para seguir."]},
      {"img":"tr_zebra","p":"Com que letra começa <b>ZEBRA</b>?",
       "c":"Z","e":["S","B","R"],
       "d":["Diga: <b>ze</b>-bra. Ouça a primeira letra.",
            "É o som /z/, da abelhinha: zzz... zebra.",
            "É o Z. Ele está aceso: toque nele para seguir."]},
    ], dadosExtra={"TITULO":"A LETRA INICIAL","FECHO":"Você acha a letra do começo de cada palavra!"})

# (f09 LIGAR-PONTOS REMOVIDA — Marcos, ago/2026: "ficaram ruins/feias, remover".)

# f10 — VITRINE: os vagões de N a Z
add(id="f10", mec="vitrine", selo="O TREM CHEGOU", conceito="objetivo1",
    enunciado="Toque em cada <b>letra</b>, de N até Z, e ouça o nome dela.",
    dica="Toque em cada letra para ouvir o nome dela e a figura.",
    dados=[{"img":FIG[l], "nome":l, "grupo":"VOGAL" if l in "AEIOU" else "CONSOANTE",
            "info":("%s de %s." % (l, PAL[l].lower())),
            "voz":("Letra %s. %s de %s." % (nome_letra(l), nome_letra(l), PAL[l].lower()))}
           for l in "NOPQRSTUVWXYZ"])

# ============================================================
# BLOCO 2 — AS SÍLABAS (obj2): começo, meio e fim
# ============================================================

# f12 — BATER-SÍLABAS: contar os pedaços (2 sílabas)
add(id="f12", mec="bater-silabas", selo="BATA AS SÍLABAS", conceito="objetivo2",
    enunciado="<b>Bata 1 vez</b> para cada sílaba e depois toque em <b>Pronto</b>.",
    dica="Ponha a mão no queixo: ele desce a cada sílaba da palavra.",
    dados=[
      {"pal":"BOLA","sil":["BO","LA"],"voz":"bo... la","fig":"tr_bola",
       "d":["Diga <b>BOLA</b> bem devagar e bata uma vez para cada pedaço.",
            "Escute o ritmo: eu bato junto com você. Conte comigo.",
            "São <b>2</b> pedaços: bo... la. As batidas já estão aí: toque em Pronto."]},
      {"pal":"CASA","sil":["CA","SA"],"voz":"ca... sa","fig":"tr_casa",
       "d":["Ponha a mão no queixo e diga CASA. O queixo desce a cada pedaço.",
            "Escute o ritmo da palavra e conte as batidas.",
            "São <b>2</b> pedaços: ca... sa. As batidas já estão aí: toque em Pronto."]},
      {"pal":"SAPO","sil":["SA","PO"],"voz":"sa... po","fig":"tr_sapo",
       "d":["Diga SAPO devagar e bata palma a cada pedaço.",
            "Conte comigo: são dois pulinhos da boca.",
            "São <b>2</b> pedaços: sa... po. As batidas já estão aí: toque em Pronto."]},
    ])

# f12b — ESCOLHER (imagens): começa com a letra (variando figuras M, V, L)
add(id="f12b", mec="escolher", selo="COMEÇA COM...", conceito="objetivo1",
    enunciado="Ache a <b>figura</b> que começa com a letra.",
    dica="Diga o nome de cada figura e escute o primeiro som.",
    dados=[
      {"p":"Qual figura começa com a letra <b>M</b>?",
       "c":{"t":"MAÇÃ","img":"tr_maca","voz":"maçã"},
       "e":[{"t":"GATO","img":"tr_gato","voz":"gato"},
            {"t":"UVA","img":"tr_uva","voz":"uva"},
            {"t":"BOLA","img":"tr_bola","voz":"bola"}],
       "d":["Diga o nome de cada figura e escute como ela COMEÇA.",
            "M faz o som /m/, como no começo de <b>maçã</b>.",
            "É a MAÇÃ. Ela está acesa: toque nela para seguir."]},
      {"p":"Qual figura começa com a letra <b>V</b>?",
       "c":{"t":"VACA","img":"tr_vaca","voz":"vaca"},
       "e":[{"t":"SAPO","img":"tr_sapo","voz":"sapo"},
            {"t":"DADO","img":"tr_dado","voz":"dado"},
            {"t":"OVO","img":"tr_ovo","voz":"ovo"}],
       "d":["Fale cada nome e ouça o comecinho.",
            "V faz o som /v/, como em <b>vaca</b>.",
            "É a VACA. Ela está acesa: toque nela para seguir."]},
      {"p":"Qual figura começa com a letra <b>L</b>?",
       "c":{"t":"LEÃO","img":"tr_leao","voz":"leão"},
       "e":[{"t":"RATO","img":"tr_rato","voz":"rato"},
            {"t":"MAÇÃ","img":"tr_maca","voz":"maçã"},
            {"t":"PATO","img":"tr_pato","voz":"pato"}],
       "d":["Diga cada nome devagar e ouça o começo.",
            "L faz o som /l/, como em <b>leão</b>.",
            "É o LEÃO. Ele está aceso: toque nele para seguir."]},
    ], dadosExtra={"TITULO":"A LETRA DO COMEÇO","SOIMG":True,
                   "FECHO":"Você acha a figura pela letra do começo!"})

# f13 — JUNTAR-SÍLABAS: qual pedaço vem PRIMEIRO (sílaba inicial)
add(id="f13", mec="juntar-silabas", selo="O COMEÇO DA PALAVRA", conceito="objetivo2",
    enunciado="Monte a palavra: qual <b>pedaço</b> vem primeiro?",
    dica="Diga a palavra devagar: qual pedaço a boca fala primeiro?",
    dados=[
      {"pal":"PATO","sil":["PA","TO"],"img":"tr_pato","iscas":["MA","LO"],"lento":"PA... TO",
       "d":["Diga a palavra devagar: que pedaço a boca fala PRIMEIRO?",
            "A palavra começa com o som <b>pa</b>. Esse pedaço está pulsando aí embaixo.",
            "É o <b>PA</b>. Ele está aceso: toque nele para seguir."]},
      {"pal":"DADO","sil":["DA","DO"],"img":"tr_dado","iscas":["BO","TE"],"lento":"DA... DO",
       "d":["Fale a palavra bem devagar e escute o começo.",
            "O primeiro pedaço é <b>DA</b>. Ele está pulsando.",
            "É o <b>DA</b>. Ele está aceso: toque nele para seguir."]},
      {"pal":"VACA","sil":["VA","CA"],"img":"tr_vaca","iscas":["FA","LO"],"lento":"VA... CA",
       "d":["Ponha a mão no queixo e diga VA-CA. Qual vem primeiro?",
            "O começo é <b>VA</b>. Ele está pulsando aí.",
            "É o <b>VA</b>. Ele está aceso: toque nele para seguir."]},
    ])

# f14 — ESCOLHER (imagens): qual palavra começa com a sílaba pedida
add(id="f14", mec="escolher", selo="MESMA SÍLABA", conceito="objetivo2",
    enunciado="Ache a <b>figura</b> que começa com a sílaba.",
    dica="Diga cada palavra e escute o primeiro pedaço dela.",
    dados=[
      {"p":"Qual figura começa com a sílaba <b>SA</b>?",
       "c":{"t":"SAPO","img":"tr_sapo","voz":"sapo"},
       "e":[{"t":"GATO","img":"tr_gato","voz":"gato"},
            {"t":"BOLA","img":"tr_bola","voz":"bola"},
            {"t":"PATO","img":"tr_pato","voz":"pato"}],
       "d":["Diga cada nome e escute o PRIMEIRO pedaço.",
            "SA-po começa com <b>SA</b>, o mesmo pedaço da pergunta.",
            "É o SAPO. Ele está aceso: toque nele para seguir."]},
      {"p":"Qual figura começa com a sílaba <b>CA</b>?",
       "c":{"t":"CASA","img":"tr_casa","voz":"casa"},
       "e":[{"t":"DADO","img":"tr_dado","voz":"dado"},
            {"t":"VACA","img":"tr_vaca","voz":"vaca"},
            {"t":"OVO","img":"tr_ovo","voz":"ovo"}],
       "d":["Escute o comecinho de cada palavra.",
            "CA-sa começa com <b>CA</b>. Cuidado: va-CA tem o CA no fim!",
            "É a CASA. Ela está acesa: toque nela para seguir."]},
    ], dadosExtra={"TITULO":"A SÍLABA DO COMEÇO","SOIMG":True,
                   "FECHO":"Você acha figuras pela sílaba do começo!"})

# f15 — LETRAS-ESCONDIDAS: falta a letra do COMEÇO
add(id="f15", mec="letras-escondidas", selo="A LETRA QUE FALTA", conceito="objetivo2",
    enunciado="Falta a <b>primeira letra</b>. Descubra qual é.",
    dica="Diga a palavra da figura e escute como ela começa.",
    dados=[
      {"pal":"SAPO","esc":"_APO","extra":["F","L"],"img":"tr_sapo","voz":"sapo",
       "d":["Olhe a figura e diga o nome dela: <b>sapo</b>. Que letra vem antes de APO?",
            "É o som /s/, da cobrinha: <b>ssss</b>apo.",
            "É o <b>S</b>: S de SAPO. Ele está aceso — toque nele para seguir."]},
      {"pal":"BOLA","esc":"_OLA","extra":["D","P"],"img":"tr_bola","voz":"bola",
       "d":["Diga o nome da figura: <b>bola</b>. Qual é a primeira letra?",
            "É o som /b/: <b>b</b>ola.",
            "É o <b>B</b>: B de BOLA. Ele está aceso — toque nele para seguir."]},
      {"pal":"DADO","esc":"_ADO","extra":["B","T"],"img":"tr_dado","voz":"dado",
       "d":["Olhe a figura e diga: <b>dado</b>. Que letra começa?",
            "É o som /d/: <b>d</b>ado.",
            "É o <b>D</b>: D de DADO. Ele está aceso — toque nele para seguir."]},
    ])

# f16 — AQUECIMENTO (escolher, texto): revisão do alfabeto (no meio da aula)
add(id="aquecimento", mec="escolher", selo="AQUECIMENTO", conceito="objetivo1",
    enunciado="<b>Aquecimento!</b> Vamos lembrar o alfabeto.",
    dica="Cante o ABC baixinho para ajudar a lembrar.",
    dados=[
      {"img":"","p":"Qual letra vem <b>depois</b> do C?",
       "c":"D","e":["B","F","A"],
       "d":["Cante: A, B, C... e escute qual vem em seguida.",
            "Depois do C vem o D.",
            "É o D. Ele está aceso: toque nele para seguir."]},
      {"img":"","p":"Qual destas é uma <b>vogal</b>?",
       "c":"E","e":["M","T","B"],
       "d":["As vogais são A, E, I, O, U.",
            "Procure entre elas: A, <b>E</b>, I, O, U.",
            "É o E. Ele está aceso: toque nele para seguir."]},
      {"img":"","p":"Qual letra vem <b>antes</b> do P?",
       "c":"O","e":["Q","R","N"],
       "d":["Cante até o P e pare no que vem logo antes.",
            "...N, O, <b>P</b>. Antes do P vem o O.",
            "Essa é a letra <b>O</b>, que está acesa. Toque nela para seguir."]},
    ], dadosExtra={"TITULO":"LEMBRANDO O ALFABETO","FECHO":"Sua memória do alfabeto está afiada!"})

# f17 — BATER-SÍLABAS: palavras de 3 pedaços
add(id="f17", mec="bater-silabas", selo="BATA AS SÍLABAS", conceito="objetivo2",
    enunciado="Palavras <b>maiores</b>: bata 1 vez para cada sílaba e toque em <b>Pronto</b>.",
    dica="Diga bem devagar e conte quantas sílabas a boca fala.",
    dados=[
      {"pal":"NAVIO","sil":["NA","VI","O"],"voz":"na... vi... o","fig":"tr_navio",
       "d":["Diga <b>NAVIO</b> devagar e bata a cada pedaço.",
            "Escute com atenção: são mais de dois pulinhos.",
            "São <b>3</b> pedaços: na... vi... o. Toque em Pronto."]},
      {"pal":"JACARÉ","sil":["JA","CA","RÉ"],"voz":"jacaré","fig":"tr_jacare",
       "d":["Ponha a mão no queixo e diga JA-CA-RÉ.",
            "Conte as vezes que o queixo desce.",
            "São <b>3</b> pedaços. Diga comigo: jacaré. Toque em Pronto."]},
    ])

# f18 — JUNTAR-SÍLABAS: montar a palavra inteira (2 sílabas na ordem)
add(id="f18", mec="juntar-silabas", selo="MONTE A PALAVRA", conceito="objetivo2",
    enunciado="Junte os <b>pedaços</b> na ordem certa e forme a palavra.",
    dica="Diga a palavra devagar: qual pedaço vem primeiro e qual vem depois?",
    dados=[
      {"pal":"GATO","sil":["GA","TO"],"img":"tr_gato","iscas":["MA","LO"],"lento":"GA... TO",
       "d":["Diga <b>GA-TO</b>. Qual pedaço vem primeiro?",
            "Começa com <b>GA</b>; depois vem <b>TO</b>.",
            "A ordem é GA, depois TO. O pedaço certo está aceso: toque nele."]},
      {"pal":"RATO","sil":["RA","TO"],"img":"tr_rato","iscas":["BO","SA"],"lento":"RA... TO",
       "d":["Diga <b>RA-TO</b> devagar. Qual vem no começo?",
            "Primeiro <b>RA</b>, depois <b>TO</b>.",
            "A ordem é RA, depois TO. O pedaço certo está aceso: toque nele."]},
      {"pal":"UVA","sil":["U","VA"],"img":"tr_uva","iscas":["BO","LA"],"lento":"U... VA",
       "d":["Diga <b>U-VA</b>. Qual pedaço abre a palavra?",
            "Começa só com <b>U</b>; depois vem <b>VA</b>.",
            "A ordem é U, depois VA. O pedaço certo está aceso: toque nele."]},
    ])

# f18b — PINTAR: colorir o trenzinho (pausa criativa, obj3)
add_pintar(id="f18b", mec="pintar-canvas", selo="HORA DE PINTAR", conceito="objetivo3",
    enunciado="<b>Pinte</b> o trenzinho do alfabeto com as suas cores.",
    dica="Escolha uma cor e toque dentro de cada parte do trem.",
    dados=[{"selo":"PINTE O TREM","nome":"o trem do alfabeto","voz":"o trem do alfabeto",
            "img":"tr_pintar_trem"}])

# f19 — LETRAS-ESCONDIDAS: falta a letra do FIM
add(id="f19", mec="letras-escondidas", selo="A LETRA DO FIM", conceito="objetivo2",
    enunciado="Agora falta a <b>última letra</b>. Descubra qual é.",
    dica="Diga a palavra e segure o final dela na boca.",
    dados=[
      {"pal":"BOLA","esc":"BOL_","extra":["O","E"],"img":"tr_bola","voz":"bola",
       "d":["Diga <b>bola</b> e escute como ela TERMINA.",
            "Termina com o som /a/: bol... <b>A</b>.",
            "É o <b>A</b>: bol-A. Ele está aceso — toque nele para seguir."]},
      {"pal":"SAPO","esc":"SAP_","extra":["A","U"],"img":"tr_sapo","voz":"sapo",
       "d":["Diga <b>sapo</b> e segure o finalzinho.",
            "Termina com o som /o/: sap... <b>O</b>.",
            "É a letra <b>O</b>: sap-O. Ela está acesa — toque nela para seguir."]},
      {"pal":"VACA","esc":"VAC_","extra":["O","E"],"img":"tr_vaca","voz":"vaca",
       "d":["Diga <b>vaca</b> e escute a última letra.",
            "Termina com o som /a/: vac... <b>A</b>.",
            "É o <b>A</b>: vac-A. Ele está aceso — toque nele para seguir."]},
    ])

# f20 — QUEM-SOU-EU: descobrir a palavra pelas pistas
add(id="f20", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo2",
    enunciado="Ouça as pistas e descubra <b>qual palavra</b> sou eu.",
    dica="Cada pista conta uma parte. Junte todas antes de responder.",
    dados=[
      {"resp":"GATO","pistas":[
         "Eu começo com a sílaba <b>GA</b>.",
         "Eu tenho <b>dois</b> pedaços: ga... to.",
         "Eu <b>mio</b> e gosto de dormir no sol."],
       "outros":["PATO","BOLA","SAPO"]},
      {"resp":"SAPO","pistas":[
         "Eu começo com a sílaba <b>SA</b>.",
         "Eu termino com o som <b>po</b>.",
         "Eu <b>pulo</b> e vivo perto da água."],
       "outros":["GATO","VACA","DADO"]},
    ])

# ============================================================
# BLOCO 3 — FORMAR PALAVRAS SIMPLES (obj3)
# ============================================================

# f20c — LETRAS-ESCONDIDAS: falta a 1ª letra (mais figuras: gato, vaca)
add(id="f20c", mec="letras-escondidas", selo="A LETRA QUE FALTA", conceito="objetivo2",
    enunciado="Falta a <b>primeira letra</b>. Descubra qual é.",
    dica="Diga a palavra da figura e escute como ela começa.",
    dados=[
      {"pal":"GATO","esc":"_ATO","extra":["P","R"],"img":"tr_gato","voz":"gato",
       "d":["Olhe a figura e diga: <b>gato</b>. Que letra vem antes de ATO?",
            "É o som /g/: <b>g</b>ato.",
            "É o <b>G</b>: G de GATO. Ele está aceso — toque nele para seguir."]},
      {"pal":"VACA","esc":"_ACA","extra":["F","L"],"img":"tr_vaca","voz":"vaca",
       "d":["Diga o nome da figura: <b>vaca</b>. Qual é a primeira letra?",
            "É o som /v/: <b>v</b>aca.",
            "É o <b>V</b>: V de VACA. Ele está aceso — toque nele para seguir."]},
    ])

# f21 — JUNTAR-SÍLABAS: formar palavras (fixando a ordem)
add(id="f21", mec="juntar-silabas", selo="MONTE A PALAVRA", conceito="objetivo3",
    enunciado="Forme a palavra da figura juntando os <b>pedaços</b>.",
    dica="Olhe a figura, diga o nome e monte pedaço por pedaço.",
    dados=[
      {"pal":"CASA","sil":["CA","SA"],"img":"tr_casa","iscas":["BO","TE"],"lento":"CA... SA",
       "d":["Diga <b>CA-SA</b>. Qual pedaço abre a palavra?",
            "Primeiro <b>CA</b>, depois <b>SA</b>.",
            "A ordem é CA, depois SA. O pedaço certo está aceso: toque nele."]},
      {"pal":"PATO","sil":["PA","TO"],"img":"tr_pato","iscas":["MA","LO"],"lento":"PA... TO",
       "d":["Diga <b>PA-TO</b> devagar. Qual vem primeiro?",
            "Primeiro <b>PA</b>, depois <b>TO</b>.",
            "A ordem é PA, depois TO. O pedaço certo está aceso: toque nele."]},
      {"pal":"DADO","sil":["DA","DO"],"img":"tr_dado","iscas":["BO","SA"],"lento":"DA... DO",
       "d":["Diga <b>DA-DO</b>. Escute os dois pedaços.",
            "Primeiro <b>DA</b>, depois <b>DO</b>.",
            "A ordem é DA, depois DO. O pedaço certo está aceso: toque nele."]},
    ])

# f21b — QUEM-SOU-EU: mais adivinhas (pato, vaca)
add(id="f21b", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo2",
    enunciado="Ouça as pistas e descubra <b>qual palavra</b> sou eu.",
    dica="Cada pista conta uma parte. Junte todas antes de responder.",
    dados=[
      {"resp":"PATO","pistas":[
         "Eu começo com a sílaba <b>PA</b>.",
         "Eu tenho <b>dois</b> pedaços: pa... to.",
         "Eu faço <b>quá-quá</b> e nado na lagoa."],
       "outros":["GATO","BOLA","SAPO"]},
      {"resp":"VACA","pistas":[
         "Eu começo com a sílaba <b>VA</b>.",
         "Eu termino com o som <b>ca</b>.",
         "Eu faço <b>muuu</b> e dou leite."],
       "outros":["MAÇÃ","RATO","DADO"]},
    ])

# f22 — DIGITAR: escrever a palavra (teclado na tela E teclado de verdade)
add(id="f22", mec="digitar", selo="ESCREVA A PALAVRA", conceito="objetivo3",
    enunciado="Olhe a figura e <b>escreva</b> o nome dela, letra por letra.",
    dica="Diga a palavra devagar e ache cada letra no teclado.",
    dados=[
      {"img":"tr_bola","palavra":"BOLA","pista":"Ela é redonda e rola quando você chuta.",
       "dic":"Diga devagar: <b>BO-LA</b>."},
      {"img":"tr_casa","palavra":"CASA","pista":"É o lugar onde a gente mora e dorme.",
       "dic":"Diga devagar: <b>CA-SA</b>."},
    ], dadosExtra={"ENUN":"Escreva o nome da figura, letra por letra.",
                   "FECHO":"Você escreveu as palavras!"})

# f24 — CAÇA-PALAVRAS: achar 4 palavras
add(id="f24", mec="caca-palavras", selo="CAÇA-PALAVRAS", conceito="objetivo3",
    enunciado="Ache as <b>palavras</b> escondidas no quadro.",
    dica="As palavras estão deitadas (→) e em pé (↓). Ache uma de cada vez.",
    dados=["GATO","BOLA","SAPO","PATO"],
    dadosExtra={
      "MODO":"lista",
      "TITULO":"CAÇA-PALAVRAS DO TREM",
      "LETRAS":"ABCDEGHILMNOPRSTU",
      "DIFICIL":"","FACIL":True,
      "CORP":["p1","p2","p3","p4"]})

# f24b — MEMÓRIA: letra <-> figura (mais figuras: M, N, R, Z)
add(id="f24b", mec="memoria", selo="MEMÓRIA", conceito="objetivo3",
    enunciado="Ache a <b>letra</b> e a <b>figura</b> que combinam.",
    dica="Vire duas cartas: a letra e a figura que começa com ela.",
    dados=[
      {"k":"m","pal":"M","voz":"letra ême","sen":"MAÇÃ","imgsen":"tr_maca","vozsen":"maçã"},
      {"k":"n","pal":"N","voz":"letra ene","sen":"NAVIO","imgsen":"tr_navio","vozsen":"navio"},
      {"k":"r","pal":"R","voz":"letra érre","sen":"RATO","imgsen":"tr_rato","vozsen":"rato"},
      {"k":"z","pal":"Z","voz":"letra zê","sen":"ZEBRA","imgsen":"tr_zebra","vozsen":"zebra"}])

# f25 — ESCOLHER (texto): qual palavra é a da figura
add(id="f25", mec="escolher", selo="QUE PALAVRA É?", conceito="objetivo3",
    enunciado="Olhe a figura e escolha a <b>palavra certa</b>.",
    dica="Leia cada palavra devagar e compare com a figura.",
    dados=[
      {"img":"tr_pato","p":"Qual é o nome desta figura?",
       "c":"PATO","e":["GATO","RATO","BOLA"],
       "d":["Comece pela PRIMEIRA letra da figura: <b>p</b>ato.",
            "Cuidado com gato e rato: mudam só a primeira letra!",
            "É PATO, com P no começo. Toque para seguir."]},
      {"img":"tr_uva","p":"Qual é o nome desta figura?",
       "c":"UVA","e":["OVO","VACA","OVA"],
       "d":["Diga o nome da figura: <b>uva</b>.",
            "Começa com U e termina com A: U-VA.",
            "É UVA. Toque para seguir."]},
      {"img":"tr_sapo","p":"Qual é o nome desta figura?",
       "c":"SAPO","e":["SAPÉ","SABO","SOPA"],
       "d":["Diga devagar: <b>sa</b>-po.",
            "Começa com SA e termina com PO: SA-PO.",
            "É SAPO. Toque para seguir."]},
    ], dadosExtra={"TITULO":"LEIA E ESCOLHA","FECHO":"Você já lê o nome das figuras!"})

# f26 — DIGITAR: mais palavras (dificuldade sobe dentro da mecânica)
add(id="f26", mec="digitar", selo="ESCREVA A PALAVRA", conceito="objetivo3",
    enunciado="Mais palavras para <b>escrever</b>: olhe a figura e digite.",
    dica="Diga a palavra em pedaços e ache cada letra.",
    dados=[
      {"img":"tr_vaca","palavra":"VACA","pista":"Faz muuu e dá o leite que a gente bebe.",
       "dic":"Diga devagar: <b>VA-CA</b>."},
      {"img":"tr_rato","palavra":"RATO","pista":"Bichinho pequeno de rabo comprido, que rói.",
       "dic":"Diga devagar: <b>RA-TO</b>."},
    ], dadosExtra={"ENUN":"Escreva o nome da figura, letra por letra.",
                   "FECHO":"Você escreveu mais palavras!"})

# f28 — LIGAR: palavra -> letra inicial (fecho da leitura)
add(id="f28", mec="ligar", selo="LIGUE", conceito="objetivo3",
    enunciado="Ligue cada <b>palavra</b> à letra com que ela começa.",
    dica="Leia a palavra e escute o primeiro som dela.",
    dados=[{"k":"p0","t":"CASA","s":"Letra C"},
           {"k":"p1","t":"OVO","s":"Letra O"},
           {"k":"p2","t":"TREM","s":"Letra T"},
           {"k":"p3","t":"ZEBRA","s":"Letra Z"}],
    dadosExtra={"DICAS":[
      "Leia a palavra e escute a primeira letra.",
      "Casa começa com C, ovo com O, trem com T, zebra com Z. Siga a linha.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue cada palavra à sua letra inicial.",
      "FECHO":"Você ligou todas as palavras à letra do começo!"})

# f28b — DIGITAR: mais palavras (gato, sapo)
add(id="f28b", mec="digitar", selo="ESCREVA A PALAVRA", conceito="objetivo3",
    enunciado="Olhe a figura e <b>escreva</b> o nome dela, letra por letra.",
    dica="Diga a palavra devagar e ache cada letra no teclado.",
    dados=[
      {"img":"tr_gato","palavra":"GATO","pista":"Bichinho que faz miau e gosta de dormir.",
       "dic":"Diga devagar: <b>GA-TO</b>."},
      {"img":"tr_sapo","palavra":"SAPO","pista":"Verdinho, pula e vive perto da água.",
       "dic":"Diga devagar: <b>SA-PO</b>."},
    ], dadosExtra={"ENUN":"Escreva o nome da figura, letra por letra.",
                   "FECHO":"Você escreveu mais palavras!"})

# f29 — MEMÓRIA: letra <-> figura (segundo conjunto)
add(id="f29", mec="memoria", selo="MEMÓRIA", conceito="objetivo3",
    enunciado="Mais uma <b>memória</b>: ache a letra e a figura que combinam.",
    dica="Vire duas cartas: a letra e a figura que começa com ela.",
    dados=[
      {"k":"s","pal":"S","voz":"letra ésse","sen":"SAPO","imgsen":"tr_sapo","vozsen":"sapo"},
      {"k":"g","pal":"G","voz":"letra gê","sen":"GATO","imgsen":"tr_gato","vozsen":"gato"},
      {"k":"v","pal":"V","voz":"letra vê","sen":"VACA","imgsen":"tr_vaca","vozsen":"vaca"},
      {"k":"u","pal":"U","voz":"letra u","sen":"UVA","imgsen":"tr_uva","vozsen":"uva"}])

# f29b — PINTAR: colorir o maquinista Coru (pausa criativa, obj3)
add_pintar(id="f29b", mec="pintar-canvas", selo="HORA DE PINTAR", conceito="objetivo3",
    enunciado="<b>Pinte</b> o Coru, o maquinista do trem.",
    dica="Escolha as cores e toque dentro do desenho do Coru.",
    dados=[{"selo":"PINTE O CORU","nome":"o maquinista Coru","voz":"o maquinista Coru",
            "img":"tr_pintar_coru"}])

# f30 — QUEBRA-CABEÇA: montar o trenzinho
add(id="f30", mec="quebra-cabeca", selo="QUEBRA-CABEÇA", conceito="objetivo3",
    enunciado="Monte o <b>trenzinho</b> do alfabeto.",
    dica="Comece pelos cantos e olhe as cores que combinam.",
    dados={"img":"tr_trem","cols":3,"lins":2,"w":360,"h":360,"fundo":False})

# f31 — VITRINE: a grande estação (fecho + gancho de curiosidade)
add(id="f31", mec="vitrine", selo="A GRANDE ESTAÇÃO", conceito="objetivo1",
    enunciado="O trem ficou pronto! Toque nas <b>letras</b> e ouça o que você aprendeu.",
    dica="Toque em cada vagão e ouça o resumo.",
    dados=[{"img":FIG[l], "nome":l, "grupo":"VOGAL" if l in "AEIOU" else "CONSOANTE",
            "info":("%s de %s." % (l, PAL[l].lower())),
            "voz":("Letra %s, de %s. Você já sabe!" % (nome_letra(l), PAL[l].lower()))}
           for l in "ABCDEFGHIJ"])

# ---- header (preenche o esboço) + fases ----
P = os.path.join(os.path.dirname(__file__), "conteudo.json")
c = json.load(io.open(P, encoding="utf-8"))

c["sub"] = "Língua Portuguesa · 1º ano · Alfabeto, sílabas e palavras"
c["mascoteNome"] = "Coru"
c["fundo"] = "tr_fundo.png"
c["crachas"] = 6
c["voz"] = "masculina"
c["convite"] = "<b>Quem vai pilotar</b> o trem hoje?"
c["abertura"] = ("Piiii! O Trem do Alfabeto vai partir, mas os vagões se "
  "embaralharam e as letras se perderam pelo caminho! Sem elas na ordem certa, "
  "o trem não anda e as palavras não se formam. Vem comigo pôr cada letra no seu vagão?")
c["fim"] = ("Você arrumou o trem inteiro e formou um montão de palavras! Piiii! "
  "Agora olhe à sua volta: quantas palavras você consegue ler nas placas da rua? "
  "Amanhã tem mais estação para descobrir!")
c["mesa"] = ("Sentou o PEDAGOGO alfabetizador (1º ano) com roteirista, game designer, "
  "especialista em interatividade, web designer, diretor de arte, engenheiro e o PhD de "
  "testes que auto-aprende (ver _padrao/RECEITA.md). Base: consciência fonológica e "
  "princípio alfabético — o som antes da letra, a letra antes da palavra.")
c["conceitos"] = {
  "objetivo1": "O alfabeto: conhecer as letras e pô-las em ordem",
  "objetivo2": "As sílabas: o começo, o meio e o fim das palavras",
  "objetivo3": "Formar e escrever palavras simples",
}
# Currículo de Blumenau (1º ano, LP), citado VERBATIM — formato que o portão
# _qa/curriculo_verbatim.py mede (HABILIDADE: "..." com palavras do blumenau.txt).
c["curriculo"] = {
  "objetivo1": (u"Blumenau, 1º ano, Língua Portuguesa — Todos os campos de atuação · "
    u"Análise linguística/semiótica (alfabetização) · objeto de conhecimento: Conhecimento "
    u"do alfabeto do português do Brasil — HABILIDADE: “Nomear as letras do alfabeto e "
    u"ordená-las.” Conceitos/conteúdos: ordem alfabética."),
  "objetivo2": (u"Blumenau, 1º ano, Língua Portuguesa — Todos os campos de atuação · "
    u"Análise linguística/semiótica (alfabetização) · objeto de conhecimento: Construção do "
    u"sistema alfabético — HABILIDADE: “Comparar palavras, identificando semelhanças e "
    u"diferenças entre sons de sílabas iniciais, mediais e finais.” Conceitos/conteúdos: "
    u"fonema/grafema, separação silábica, palavra."),
  "objetivo3": (u"Blumenau, 1º ano, Língua Portuguesa — Campo artístico-literário · "
    u"Análise linguística/semiótica (alfabetização) · objeto de conhecimento: Construção do "
    u"sistema alfabético e da ortografia — HABILIDADE: “Relacionar elementos sonoros "
    u"(sílabas, fonemas, partes de palavras) com sua representação escrita.” "
    u"Conceitos/conteúdos: alfabeto, fonema/grafema, sílaba."),
}
c["arte"] = {
  "cenario": ("the cozy interior of a colorful toy steam-train wagon, a big round window "
    "showing sunny green hills rolling by, warm wooden benches, storybook 3D style, no text"),
  "mascote": ("Coru, a cheerful little owl train conductor with a red-and-cream striped "
    "engineer cap and a blue neckerchief, big friendly eyes, soft 3D storybook render, "
    "full body, plain background"),
}
# ⭐ (Marcos, ago/2026) as fases de PINTAR (pausa criativa) vão para o FINAL da
#    atividade — a criança primeiro trabalha o alfabeto/sílabas/palavras e só no
#    fim relaxa colorindo. Mas o motor não deixa DUAS do mesmo gesto coladas;
#    então intercalo: as 3 fases de pintar ficam no trecho final, separadas
#    pelas 2 últimas fases de conteúdo (a ÚLTIMA fase da atividade é pintar).
_pint  = [f for f in fases if f.get("mec") == "pintar-canvas"]
_resto = [f for f in fases if f.get("mec") != "pintar-canvas"]
if len(_pint) >= 3 and len(_resto) >= 2:
    fases = _resto[:-2] + [_pint[0], _resto[-2], _pint[1], _resto[-1], _pint[2]]
else:
    fases = _resto + _pint
c["fases"] = fases

json.dump(c, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("conteudo.json: %d fases" % len(fases))
cnt = collections.Counter(f["mec"] for f in fases)
print("mecanicas (%d):" % len(cnt), dict(cnt))
mx = max(cnt.values()); print("gesto mais frequente: %d/%d = %.0f%%" % (mx, len(fases), 100*mx/len(fases)))
