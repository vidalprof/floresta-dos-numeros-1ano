# -*- coding: utf-8 -*-
u"""
A CIDADE DOS SÓLIDOS — 2º ano — build do conteudo.json (motor ESQUELETO).

6 sólidos (BNCC EF02MA14): cubo, esfera, cilindro, cone, pirâmide, bloco retangular.
Progressão: (1) conhecer/nomear -> (2) rola x fica firme -> (3) no dia a dia + faces.
O problema vem ANTES do conceito (EDUVERSE-FILOSOFIA). Concreto->figural->simbólico.

Imagens (o Marcos gera; eu recorto das cartelas):
  VIDRO (vitrine): sg_cubo_v sg_esfera_v sg_cilindro_v sg_cone_v sg_piramide_v sg_bloco_v
  OBJETOS: sg_dado sg_presente sg_bola sg_laranja sg_lata sg_copo sg_sorvete sg_chapeu
           sg_monumento sg_telhado sg_sapato sg_tijolo
  QUEBRA-CABECA: sg_puzzle1 sg_puzzle2   FUNDO: sg_fundo
"""
import json, io, os

# --- os 6 sólidos: nome, artigo, imagem de vidro, rola?, objetos do dia a dia, face ---
SOL = {
 "cubo":     {"nome":"CUBO","art":"o","v":"sg_cubo_v","rola":False,"face":"quadrado",
              "obj":[("sg_dado","DADO"),("sg_presente","CAIXA DE PRESENTE")]},
 "esfera":   {"nome":"ESFERA","art":"a","v":"sg_esfera_v","rola":True,"face":None,
              "obj":[("sg_bola","BOLA"),("sg_laranja","LARANJA")]},
 "cilindro": {"nome":"CILINDRO","art":"o","v":"sg_cilindro_v","rola":True,"face":"círculo",
              "obj":[("sg_lata","LATA"),("sg_copo","COPO")]},
 "cone":     {"nome":"CONE","art":"o","v":"sg_cone_v","rola":True,"face":"círculo",
              "obj":[("sg_sorvete","SORVETE"),("sg_chapeu","CHAPÉU DE FESTA")]},
 "piramide": {"nome":"PIRÂMIDE","art":"a","v":"sg_piramide_v","rola":False,"face":"triângulo",
              "obj":[("sg_monumento","PIRÂMIDE"),("sg_telhado","TELHADO")]},
 "bloco":    {"nome":"BLOCO RETANGULAR","art":"o","v":"sg_bloco_v","rola":False,"face":"retângulo",
              "obj":[("sg_sapato","CAIXA DE SAPATO"),("sg_tijolo","TIJOLO")]},
}
ORD = ["cubo","esfera","cilindro","cone","piramide","bloco"]

fases = []
def add(**k): fases.append(k)
def artigo(s): return SOL[s]["art"]
def elenome(s):
    d=SOL[s]; return ("%s %s" % (d["art"].upper(), d["nome"]))

# ============================================================
# BLOCO 1 — CONHECER E NOMEAR (objetivo1): concreto -> nome
# ============================================================

# 1) VITRINE — a vitrine de vidro apresenta os 6 (reconhecer/nomear)
add(id="f01", mec="vitrine", selo="VITRINE", conceito="objetivo1",
    enunciado="Olhe cada <b>sólido</b> colorido. Toque para ouvir o nome dele.",
    dica="Toque num sólido: eu falo o nome e para que serve.",
    dados=[{"img":SOL[s]["v"], "nome":SOL[s]["nome"],
            "grupo":("ROLA" if SOL[s]["rola"] else "FICA FIRME"),
            "info":("É %s. Parece %s." % (SOL[s]["nome"].lower(), SOL[s]["obj"][0][1].lower())),
            "voz":("Este é %s %s. Ele parece %s." % (SOL[s]["art"], SOL[s]["nome"].lower(), SOL[s]["obj"][0][1].lower())
                   if SOL[s]["art"]=="o" else
                   "Esta é %s %s. Ela parece %s." % (SOL[s]["art"], SOL[s]["nome"].lower(), SOL[s]["obj"][0][1].lower()))}
           for s in ORD])

# 2) ESCOLHER — qual objeto tem a forma pedida (concreto)
add(id="f02", mec="escolher", selo="ESCOLHA", conceito="objetivo1",
    enunciado="Ache o objeto que tem a forma do <b>sólido</b>.",
    dica="Pense no formato: é redondo de rolar ou tem cantos?",
    dados=[
      # ⭐ opções em IMAGEM (não texto): fase concreta -> a criança escolhe pelo
      #    desenho do objeto. E a pergunta não entrega a resposta (nada de "(bola)").
      {"p":"Qual objeto tem a forma de uma <b>esfera</b>?",
       "c":{"t":"BOLA","img":"sg_bola","voz":"bola"},
       "e":[{"t":"DADO","img":"sg_dado","voz":"dado"},
            {"t":"LATA","img":"sg_lata","voz":"lata"},
            {"t":"CAIXA DE PRESENTE","img":"sg_presente","voz":"caixa de presente"}],
       "d":["A esfera é toda redondinha, sem nenhum canto.",
            "É a que rola para todo lado, igual a uma bolinha.",
            "É a BOLA. Ela está acesa aí: toque nela para seguir."]},
      {"p":"Qual objeto tem a forma de um <b>cubo</b>?",
       "c":{"t":"DADO","img":"sg_dado","voz":"dado"},
       "e":[{"t":"BOLA","img":"sg_bola","voz":"bola"},
            {"t":"SORVETE","img":"sg_sorvete","voz":"sorvete"},
            {"t":"LATA","img":"sg_lata","voz":"lata"}],
       "d":["O cubo tem 6 lados iguais, todos quadrados.",
            "Pense num dado de jogar: quadradinho de todos os lados.",
            "É o DADO. Ele está aceso aí: toque nele para seguir."]},
      {"p":"Qual objeto tem a forma de um <b>cilindro</b>?",
       "c":{"t":"LATA","img":"sg_lata","voz":"lata"},
       "e":[{"t":"DADO","img":"sg_dado","voz":"dado"},
            {"t":"SORVETE","img":"sg_sorvete","voz":"sorvete"},
            {"t":"CAIXA DE SAPATO","img":"sg_sapato","voz":"caixa de sapato"}],
       "d":["O cilindro é reto e redondo, igual a um cano.",
            "Pense numa lata de comida: redonda em cima e embaixo.",
            "É a LATA. Ela está acesa aí: toque nela para seguir."]},
    ], dadosExtra={"TITULO":"QUE FORMA É ESSA?","FECHO":"Você já reconhece os sólidos pelos objetos!",
                   "SOIMG":True})

# 3) LIGAR — sólido -> objeto do dia a dia
add(id="f03", mec="ligar", selo="LIGUE", conceito="objetivo1",
    enunciado="Ligue cada <b>objeto</b> ao nome do sólido que tem a forma dele.",
    dica="Toque no objeto para ouvir. Pense na forma dele.",
    dados=[{"k":"p0","img":"sg_bola","voz":"BOLA","s":"ESFERA"},
           {"k":"p1","img":"sg_dado","voz":"DADO","s":"CUBO"},
           {"k":"p2","img":"sg_lata","voz":"LATA","s":"CILINDRO"},
           {"k":"p3","img":"sg_sorvete","voz":"sorvete","s":"CONE"}],
    dadosExtra={"DICAS":[
      "Pense no formato de cada objeto.",
      "A bola é esfera, o dado é cubo, a lata é cilindro, a casquinha é cone. Siga a linha tracejada.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue cada sólido ao seu objeto.",
      "FECHO":"Você ligou todos os sólidos aos objetos!"})

# 4) MEMORIA — sólido <-> objeto (par)
add(id="f04", mec="memoria", selo="MEMÓRIA", conceito="objetivo1",
    enunciado="Ache a <b>palavra</b> e o <b>desenho que combina</b>.",
    dica="Vire duas cartas: uma tem o nome, a outra o desenho. Combinaram? É par!",
    dados=[
      {"k":"cubo","pal":"CUBO","voz":"cubo","imgsen":"sg_cubo_v","vozsen":"cubo"},
      {"k":"esf","pal":"ESFERA","voz":"esfera","imgsen":"sg_esfera_v","vozsen":"esfera"},
      {"k":"cil","pal":"CILINDRO","voz":"cilindro","imgsen":"sg_cilindro_v","vozsen":"cilindro"},
      {"k":"cone","pal":"CONE","voz":"cone","imgsen":"sg_cone_v","vozsen":"cone"}])

# 5) QUEM-SOU-EU — adivinha o sólido pela pista
add(id="f05", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo1",
    enunciado="Ouça as pistas e descubra <b>qual sólido</b> sou eu.",
    dica="Cada pista conta uma parte. Junte todas antes de responder.",
    dados=[
      {"resp":"ESFERA","pistas":[
         "Eu sou todo <b>redondo</b>, não tenho nenhum canto.",
         "Eu <b>rolo</b> para qualquer lado que você me empurrar.",
         "Você me chuta no jogo de futebol: sou a <b>bola</b>."],
       "outros":["CUBO","PIRÂMIDE","BLOCO"]},
      {"resp":"CUBO","pistas":[
         "Eu tenho <b>6 lados iguais</b>, todos quadrados.",
         "Eu <b>fico firme</b> e dá para me empilhar.",
         "Você me joga para ver o número: sou o <b>dado</b>."],
       "outros":["ESFERA","CONE","CILINDRO"]},
      {"resp":"CONE","pistas":[
         "Eu tenho uma <b>ponta</b> em cima e sou redondo embaixo.",
         "De cabeça para baixo, eu seguro o <b>sorvete</b>.",
         "Na festa, eu viro o <b>chapéu</b> pontudo."],
       "outros":["CUBO","ESFERA","BLOCO"]},
    ])

# 6) ESCOLHER — nomear o sólido a partir do vidro
add(id="f06", mec="escolher", selo="ESCOLHA", conceito="objetivo1",
    enunciado="Olhe o <b>sólido</b> e escolha o nome certo.",
    dica="Conte os cantos e veja se é redondo de rolar.",
    dados=[
      {"img":"sg_cilindro_v","p":"Qual é o nome deste sólido?",
       "c":"CILINDRO","e":["CUBO","CONE","ESFERA"],
       "d":["Ele é reto e redondo, como um cano ou uma lata.",
            "Tem um círculo em cima e um embaixo.",
            "É o CILINDRO. Toque nele para seguir."]},
      {"img":"sg_piramide_v","p":"Qual é o nome deste sólido?",
       "c":"PIRÂMIDE","e":["CUBO","CILINDRO","ESFERA"],
       "d":["Ela tem uma ponta em cima e lados de triângulo.",
            "Parece o telhado de uma casa ou um monumento antigo.",
            "É a PIRÂMIDE. Toque nela para seguir."]},
      {"img":"sg_bloco_v","p":"Qual é o nome deste sólido?",
       "c":"BLOCO RETANGULAR","e":["CUBO","CONE","ESFERA"],
       "d":["Ele tem 6 lados, mas são retângulos (mais compridos).",
            "Parece uma caixa de sapato ou um tijolo.",
            "É o BLOCO RETANGULAR. Toque nele para seguir."]},
    ], dadosExtra={"TITULO":"O NOME DO SÓLIDO","FECHO":"Você já sabe o nome dos sólidos!"})

# 6b) DIGITAR — escrever o nome do sólido (nomes CURTOS) — as DUAS PORTAS:
#     teclado na tela E teclado de verdade (document.onkeydown). Apoio visual
#     com a figura do sólido. `palavra` vai SEM ACENTO (o teclado não tem acento).
add(id="f06b", mec="digitar", selo="ESCREVA O NOME", conceito="objetivo1",
    enunciado="Agora <b>escreva</b> o nome do sólido, letra por letra.",
    dica="Diga o nome devagar e ache cada letra no teclado.",
    dados=[
      {"palavra":"CUBO","img":"sg_cubo_v",
       "pista":"Ele tem 6 lados quadrados, igual a um dado. Escreva o nome dele.",
       "dic":"Diga devagar: <b>CU-BO</b>."},
      {"palavra":"CONE","img":"sg_cone_v",
       "pista":"Tem uma ponta em cima, igual à casquinha de sorvete. Escreva o nome.",
       "dic":"Diga devagar: <b>CO-NE</b>."},
    ], dadosExtra={"ENUN":"Escreva o nome do sólido, letra por letra.",
                   "FECHO":"Você escreveu os nomes!"})

# ============================================================
# BLOCO 2 — ROLA x FICA FIRME (objetivo2): a propriedade concreta
# ============================================================

# 7) LIGAR — cada sólido ao que ele faz (rola x fica firme)
add(id="f07", mec="ligar", selo="LIGUE", conceito="objetivo2",
    enunciado="Ligue cada <b>sólido</b> ao que ele faz na rampa.",
    dica="Redondo escorrega rolando; lado reto fica parado, firme.",
    # ⭐ grupos p/ muitos-para-um (Marcos): esfera e cilindro ROLAM (qualquer
    #    destino "rola" serve); cubo e pirâmide FICAM FIRMES (idem). O gênero da
    #    frase (parado/parada) deixa de reprovar a criança.
    dados=[{"k":"p0","img":"sg_esfera_v","voz":"esfera","s":"Rola pela rampa","g":"rola"},
           {"k":"p1","img":"sg_cubo_v","voz":"cubo","s":"Fica firme, parado","g":"firme"},
           {"k":"p2","img":"sg_cilindro_v","voz":"cilindro","s":"Rola deitado","g":"rola"},
           {"k":"p3","img":"sg_piramide_v","voz":"pirâmide","s":"Fica firme, parada","g":"firme"}],
    dadosExtra={"DICAS":[
      "Pergunte de cada um: se eu soltar na rampa, ele rola ou fica parado?",
      "Esfera e cilindro têm parte redonda: rolam. Cubo e pirâmide têm lados retos: ficam firmes. Siga a linha tracejada.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue cada sólido ao que ele faz.",
      "FECHO":"Você ligou cada sólido ao seu jeito de se mexer!"})

# 8) CLASSIFICAR — rola / fica firme
add(id="f08", mec="classificar", selo="SEPARE", conceito="objetivo2",
    enunciado="Cada sólido numa gaveta: <b>ROLA</b> ou <b>FICA FIRME</b>?",
    dica="Redondo de rolar vai numa gaveta; com lados retos vai na outra.",
    dados=[{"k":"rola","n":"ROLA<br>(redondo)","img":"","voz":"rola","rot":False},
           {"k":"firme","n":"FICA FIRME<br>(lados retos)","img":"","voz":"fica firme","rot":False}],
    dadosExtra={"FICHAS":[
      {"t":"ESFERA","alvo":"rola","img":"sg_esfera_v"},
      {"t":"CILINDRO","alvo":"rola","img":"sg_cilindro_v"},
      {"t":"CONE","alvo":"rola","img":"sg_cone_v"},
      {"t":"CUBO","alvo":"firme","img":"sg_cubo_v"},
      {"t":"PIRÂMIDE","alvo":"firme","img":"sg_piramide_v"},
      {"t":"BLOCO","alvo":"firme","img":"sg_bloco_v"}],
      "DICAS":[
        "Pergunte: se eu empurrar, ele rola ou fica parado?",
        "Esfera, cilindro e cone têm parte redonda: rolam. Cubo, pirâmide e bloco têm lados retos: ficam firmes.",
        "Olhe a gaveta com a borda amarela: é ali que esta ficha mora."],
      "ENUN":"Toque no <b>sólido</b>. Depois toque na gaveta certa: <b>ROLA</b> ou <b>FICA FIRME</b>?"})

# 9) ESCOLHER — qual rola / qual empilha
add(id="f09", mec="escolher", selo="ESCOLHA", conceito="objetivo2",
    enunciado="Responda sobre <b>rolar</b> e <b>empilhar</b>.",
    dica="Pense no formato: redondo rola; lado reto empilha.",
    dados=[
      {"img":"","p":"Qual destes <b>rola</b> pela rampa?",
       "c":"ESFERA","e":["CUBO","BLOCO","PIRÂMIDE"],
       "d":["Procure o que é redondo, sem cantos.",
            "É o que foge rolando quando você empurra.",
            "É a ESFERA. Toque nela para seguir."]},
      {"img":"","p":"Para fazer uma <b>torre firme</b>, qual é melhor empilhar?",
       "c":"CUBO","e":["ESFERA","CONE","CILINDRO deitado"],
       "d":["A torre precisa de lados retos, que não escorregam.",
            "A bola rolaria e cairia; escolha o que tem faces planas.",
            "É o CUBO. Toque nele para seguir."]},
      {"img":"","p":"Qual sólido <b>rola</b> mas também <b>fica em pé</b>?",
       "c":"CILINDRO","e":["ESFERA","CUBO","PIRÂMIDE"],
       "d":["Deitado ele rola; em pé ele para, apoiado no círculo.",
            "Pense numa lata: rola no chão, mas fica em pé na mesa.",
            "É o CILINDRO. Toque nele para seguir."]},
    ], dadosExtra={"TITULO":"ROLA OU FICA FIRME?","FECHO":"Você entende como cada sólido se mexe!"})

# 10) ARRASTAR-SOMBRA — sólido -> silhueta
add(id="f10", mec="arrastar-sombra", selo="CADA UM, SUA SOMBRA", conceito="objetivo2",
    enunciado="Leve cada <b>sólido</b> até a sombra com o mesmo contorno.",
    dica="Compare o contorno: a sombra tem o mesmo formato do sólido.",
    # pool + n = sorteio a cada jogada (aleatoriedade, Marcos); semSom = encaixe
    #   só visual (imagem limpa na sombra limpa, "bem profissional").
    dados=[{"selo":"CADA UM, SUA SOMBRA","semSom":True,
            "pool":["circ","quad","tri","cil"],"n":3,"quais":["circ","quad","tri"]},
           {"selo":"OLHE BEM O CONTORNO","semSom":True,
            "pool":["quad","circ","tri","ret","cil","con"],"n":4,"quais":["quad","circ","tri","ret"]}],
    dadosExtra={"FORMAS":{
      "quad":{"n":"CUBO","voz":"CUBO","img":"sg_cubo_v"},
      "circ":{"n":"ESFERA","voz":"ESFERA","img":"sg_esfera_v"},
      "tri":{"n":"PIRÂMIDE","voz":"PIRÂMIDE","img":"sg_piramide_v"},
      "ret":{"n":"BLOCO","voz":"BLOCO","img":"sg_bloco_v"},
      "cil":{"n":"CILINDRO","voz":"CILINDRO","img":"sg_cilindro_v"},
      "con":{"n":"CONE","voz":"CONE","img":"sg_cone_v"}},
      "DICAS":[
        "Compare o <b>contorno</b>: a sombra tem o mesmo formato.",
        "A sombra certa está <b>piscando</b>. Leve o sólido até ela.",
        "Deixa comigo: eu levo esta e você continua."]})

# 11) INTRUSO — qual não pertence
add(id="f11", mec="intruso", selo="QUAL NÃO É?", conceito="objetivo2",
    enunciado="Três fazem a mesma coisa. <b>Qual é o diferente?</b>",
    dica="Descubra o que três têm em comum e ache o diferente.",
    dados=[
      {"selo":"OS QUE ROLAM","tipo":"texto",
       "enun":"Três destes rolam. <b>Qual NÃO rola?</b>",
       "itens":[{"k":"esfera","n":"ESFERA","img":"sg_esfera_v"},
                {"k":"cilindro","n":"CILINDRO","img":"sg_cilindro_v"},
                {"k":"cone","n":"CONE","img":"sg_cone_v"},
                {"k":"cubo","n":"CUBO","img":"sg_cubo_v"}],
       "fora":"cubo","nomeFora":"CUBO",
       "d1":"Imagine empurrar cada um. Qual NÃO sai rolando?",
       "d2":"Esfera, cilindro e cone têm parte redonda e rolam. Um tem só lados retos.",
       "d3":"O que não pertence é o CUBO: ele fica firme, os outros rolam.",
       "razoes":[{"t":"Os outros três rolam; o cubo fica firme.","ok":1},
                 {"t":"Porque o cubo é o maior.","ok":0},
                 {"t":"Porque o cubo é azul.","ok":0},
                 {"t":"Porque o cubo é de brincar.","ok":0}],
       "enunPorque":"O <b>cubo</b> n&#227;o rola como os outros tr&#234;s. <b>Por qu&#234;</b> isso deixa ele de fora?",
       "p1":"O que você tocou até pode ser verdade. Mas olhe o que os OUTROS três fazem.",
       "p2":"Cor e tamanho não decidem. O que decide é <b>rolar ou não</b>.",
       "p3":"Esfera, cilindro e cone rolam. O cubo <b>não rola</b>: fica firme — por isso ele é o diferente.",
       "regra":"esfera, cilindro e cone rolam; o cubo fica firme"},
      {"selo":"OS QUE FICAM FIRMES","tipo":"texto",
       "enun":"Três ficam firmes. <b>Qual NÃO fica firme?</b>",
       "itens":[{"k":"cubo","n":"CUBO","img":"sg_cubo_v"},
                {"k":"bloco","n":"BLOCO","img":"sg_bloco_v"},
                {"k":"piramide","n":"PIRÂMIDE","img":"sg_piramide_v"},
                {"k":"esfera","n":"ESFERA","img":"sg_esfera_v"}],
       "fora":"esfera","nomeFora":"ESFERA",
       "d1":"Qual deles NÃO dá para deixar parado sem rolar?",
       "d2":"Cubo, bloco e pirâmide têm lados retos e ficam firmes. Um é todo redondo.",
       "d3":"A que não pertence é a ESFERA: ela rola, os outros ficam firmes.",
       "razoes":[{"t":"Os outros três ficam firmes; a esfera rola.","ok":1},
                 {"t":"Porque a esfera é a menor.","ok":0},
                 {"t":"Porque a esfera é laranja.","ok":0},
                 {"t":"Porque a esfera é de futebol.","ok":0}],
       "enunPorque":"A <b>esfera</b> n&#227;o fica firme como os outros tr&#234;s. <b>Por qu&#234;</b> isso deixa ela de fora?",
       "p1":"Pode ser verdade, mas olhe o que os outros três têm em comum.",
       "p2":"O que junta os três é <b>ficar firme</b>, não a cor nem o tamanho.",
       "p3":"Cubo, bloco e pirâmide ficam firmes. A esfera <b>não fica firme</b>: ela rola — por isso ela é a diferente.",
       "regra":"cubo, bloco e pirâmide ficam firmes; a esfera rola"},
    ])

# 12) VITRINE — agrupar por rola x fica firme
add(id="f12", mec="vitrine", selo="VITRINE", conceito="objetivo2",
    enunciado="Toque em cada <b>sólido</b> e ouça: ele <b>rola</b> ou <b>fica firme</b>?",
    dica="Redondo rola; lados retos ficam firmes.",
    dados=[{"img":SOL[s]["v"], "nome":SOL[s]["nome"],
            "grupo":("ROLA" if SOL[s]["rola"] else "FICA FIRME"),
            "info":("Rola, porque é redondo." if SOL[s]["rola"] else "Fica firme, porque tem lados retos."),
            "voz":(("%s %s rola, porque é redondo." if SOL[s]["art"]=="o" else "%s %s rola, porque é redonda.") % (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower())
                   if SOL[s]["rola"] else
                   ("%s %s fica firme, porque tem lados retos." % (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower())))}
           for s in ORD])

# ============================================================
# BLOCO 3 — NO DIA A DIA + FACES (objetivo3)
# ============================================================

# 13) LIGAR — face plana -> sólido
add(id="f13", mec="ligar", selo="LIGUE", conceito="objetivo3",
    enunciado="Ligue cada <b>sólido</b> à forma da face dele.",
    dica="Olhe o lado do sólido: que figura plana aparece ali?",
    dados=[{"k":"p0","img":"sg_cubo_v","voz":"cubo","s":"Faces QUADRADAS"},
           {"k":"p1","img":"sg_bloco_v","voz":"bloco","s":"Faces RETÂNGULOS"},
           {"k":"p2","img":"sg_piramide_v","voz":"pirâmide","s":"Faces de TRIÂNGULO"},
           {"k":"p3","img":"sg_cilindro_v","voz":"cilindro","s":"Base em CÍRCULO"}],
    dadosExtra={"DICAS":[
      "Olhe UM lado do sólido de cada vez.",
      "O cubo tem lados quadrados; o bloco, retângulos; a pirâmide, triângulos; o cilindro tem círculo embaixo.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue cada face ao sólido dela.",
      "FECHO":"Você achou as faces dos sólidos!"})

# 14) CLASSIFICAR — objeto do dia a dia -> sólido (2 gavetas)
add(id="f14", mec="classificar", selo="SEPARE", conceito="objetivo3",
    enunciado="Cada objeto na gaveta do <b>sólido</b> dele.",
    dica="Pense na forma do objeto: é redondo de rolar ou tem cantos?",
    # rot:True -> a gaveta mostra o sólido NÍTIDO + o nome (não a marca d'água
    #   quase invisível): a criança vê claramente onde cada objeto mora.
    dados=[{"k":"esfera","n":"ESFERA","img":"sg_esfera_v","voz":"esfera","rot":True},
           {"k":"cubo","n":"CUBO","img":"sg_cubo_v","voz":"cubo","rot":True}],
    dadosExtra={"FICHAS":[
      {"t":"BOLA","alvo":"esfera","img":"sg_bola"},
      {"t":"LARANJA","alvo":"esfera","img":"sg_laranja"},
      {"t":"DADO","alvo":"cubo","img":"sg_dado"},
      {"t":"CAIXA DE PRESENTE","alvo":"cubo","img":"sg_presente"}],
      "DICAS":[
        "A bola e a laranja são redondas; o dado e a caixa têm cantos.",
        "Objeto redondo é esfera; objeto quadradinho é cubo.",
        "Olhe a gaveta com a borda amarela: é ali que este objeto mora."],
      "ENUN":"Toque no <b>objeto</b>. Depois toque na <b>gaveta do sólido</b> dele."})

# 15) QUEBRA-CABECA — a casinha de sólidos
add(id="f15", mec="quebra-cabeca", selo="QUEBRA-CABEÇA", conceito="objetivo3",
    enunciado="Monte a <b>casinha</b> feita de sólidos.",
    dica="Comece pelos cantos e olhe as cores que combinam.",
    dados={"img":"sg_puzzle1","cols":3,"lins":2,"w":360,"h":360,"fundo":False})

# 16) ESCOLHER — achar o sólido no objeto (dia a dia)
add(id="aquecimento", mec="escolher", selo="AQUECIMENTO", conceito="objetivo3",
    enunciado="<b>Aquecimento!</b> Que sólido tem a forma deste objeto?",
    dica="Compare o objeto com os sólidos que você já conhece.",
    dados=[
      {"img":"sg_lata","p":"A <b>lata</b> tem a forma de qual sólido?",
       "c":"CILINDRO","e":["CUBO","ESFERA","PIRÂMIDE"],
       "d":["Ela é reta e redonda, com círculo em cima e embaixo.",
            "Pense num cano ou num copo.",
            "É o CILINDRO. Toque para seguir."]},
      {"img":"sg_sorvete","p":"A <b>casquinha de sorvete</b> tem a forma de qual sólido?",
       "c":"CONE","e":["CILINDRO","CUBO","ESFERA"],
       "d":["Ela tem uma ponta embaixo e é redonda em cima.",
            "É a mesma forma do chapéu de festa.",
            "É o CONE. Toque para seguir."]},
      {"img":"sg_sapato","p":"A <b>caixa de sapato</b> tem a forma de qual sólido?",
       "c":"BLOCO RETANGULAR","e":["CUBO","CILINDRO","CONE"],
       "d":["Ela tem 6 lados, mas são retângulos compridos.",
            "Parece um tijolo ou um livro fechado.",
            "É o BLOCO RETANGULAR. Toque para seguir."]},
    ], dadosExtra={"TITULO":"O SÓLIDO ESCONDIDO","FECHO":"Você acha sólidos em tudo agora!"})

# 17) QUEM-SOU-EU — pistas de dia a dia + face
add(id="f17", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo3",
    enunciado="Ouça as pistas e descubra o <b>sólido</b>.",
    dica="Junte todas as pistas antes de escolher.",
    dados=[
      {"resp":"CILINDRO","pistas":[
         "Eu sou reto e tenho um <b>círculo</b> em cima e embaixo.",
         "Deitado eu <b>rolo</b>; em pé eu fico firme.",
         "Na cozinha eu sou a <b>lata</b> de comida."],
       "outros":["CUBO","ESFERA","PIRÂMIDE"]},
      {"resp":"BLOCO RETANGULAR","pistas":[
         "Eu tenho 6 lados, mas eles são <b>retângulos</b>.",
         "Eu <b>fico firme</b> e dá para me empilhar.",
         "Eu sou a <b>caixa de sapato</b> e também o tijolo."],
       "outros":["CUBO","CONE","ESFERA"]},
      {"resp":"PIRÂMIDE","pistas":[
         "Eu tenho lados de <b>triângulo</b> e uma <b>ponta</b> em cima.",
         "Eu <b>fico firme</b>, apoiada na minha base.",
         "No Egito antigo, eu sou gigante no deserto."],
       "outros":["CILINDRO","ESFERA","CUBO"]},
    ])

# 17b) DIGITAR — escrever o nome do sólido (nomes LONGOS: o degrau simbólico).
#      Progressão em relação à f06b (nomes curtos). `palavra` SEM acento; a `voz`
#      guarda a pronúncia certa (PIRAMIDE escrita -> "pirâmide" falada).
add(id="f17b", mec="digitar", selo="ESCREVA O NOME", conceito="objetivo3",
    enunciado="Escreva o nome destes sólidos, letra por letra.",
    dica="São nomes maiores: diga por partes e ache cada letra.",
    dados=[
      {"palavra":"CILINDRO","img":"sg_cilindro_v","voz":"cilindro",
       "pista":"Rola deitado e fica firme em pé, igual a uma lata. Escreva o nome.",
       "dic":"Vá por partes: <b>CI-LIN-DRO</b>."},
      {"palavra":"PIRAMIDE","img":"sg_piramide_v","voz":"pirâmide",
       "pista":"Tem base quadrada e sobe até uma ponta. Escreva o nome.",
       "dic":"Diga por partes: <b>PI-RÂ-MI-DE</b>."},
    ], dadosExtra={"ENUN":"Escreva o nome do sólido, letra por letra.",
                   "FECHO":"Você escreveu os nomes grandes!"})

# 18) VITRINE — a vitrine dos objetos (sólido no dia a dia)
add(id="f18", mec="vitrine", selo="VITRINE", conceito="objetivo3",
    enunciado="Toque em cada sólido e descubra <b>onde ele mora</b> no seu dia.",
    dica="Cada sólido lembra um objeto que você conhece.",
    dados=[{"img":SOL[s]["v"], "nome":SOL[s]["nome"], "grupo":SOL[s]["obj"][0][1],
            "info":("Parece %s e %s." % (SOL[s]["obj"][0][1].lower(), SOL[s]["obj"][1][1].lower())),
            "voz":("%s %s aparece %s: parece %s e %s." %
                   (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower(), "no seu dia",
                    SOL[s]["obj"][0][1].lower(), SOL[s]["obj"][1][1].lower()))}
           for s in ORD])

# 19) [REMOVIDA] — classificar face->sólido: o enunciado "toque na face e na gaveta
#     do sólido" confundia (Marcos, ago/2026: "não me pareceu fazer sentido").

# 20) ESCOLHER — revisão misturada (aquecimento leve)
add(id="f20", mec="caca-palavras", selo="CAÇA-PALAVRAS", conceito="objetivo1",
    enunciado="Ache os <b>nomes dos sólidos</b> escondidos no quadro.",
    dica="Os nomes estão deitados (→) e em pé (↓). Ache um de cada vez.",
    dados=["CUBO","ESFERA","CONE","BLOCO"],
    dadosExtra={
      "MODO":"lista",
      "TITULO":"CAÇA-PALAVRAS DOS SÓLIDOS",
      "LETRAS":"ABCDEFGHIJLMNOPRSTUVZ",
      "DIFICIL":"",
      "CORP":["p1","p2","p3","p4"]})

# 21) LIGAR — objeto -> nome do sólido
add(id="f21", mec="ligar", selo="LIGUE", conceito="objetivo3",
    enunciado="Ligue o <b>objeto</b> ao nome do sólido dele.",
    dica="Pense na forma de cada objeto.",
    dados=[{"k":"p0","img":"sg_sorvete","voz":"sorvete","s":"CONE"},
           {"k":"p1","img":"sg_sapato","voz":"CAIXA DE SAPATO","s":"BLOCO RETANGULAR"},
           {"k":"p2","img":"sg_bola","voz":"BOLA","s":"ESFERA"},
           {"k":"p3","img":"sg_lata","voz":"LATA","s":"CILINDRO"}],
    dadosExtra={"DICAS":[
      "Pense na forma de cada objeto.",
      "Casquinha é cone; caixa de sapato é bloco; bola é esfera; lata é cilindro. Siga a linha.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue o objeto ao nome do sólido.",
      "FECHO":"Você ligou todos!"})

# 22) QUEM SOU EU — descobrir o sólido pelas pistas de rolar x ficar firme
add(id="f22", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo2",
    enunciado="Ouça as pistas de como eu me mexo e descubra <b>qual sólido</b> sou.",
    dica="Cada pista conta se eu rolo ou fico firme. Junte todas antes de responder.",
    dados=[
      {"resp":"ESFERA","pistas":[
         "Eu não tenho nenhum lado reto: sou todo <b>redondo</b>.",
         "Se você me solta na rampa, eu <b>rolo</b> para qualquer lado.",
         "Nunca fico parado num lugar: sou a <b>bola</b>."],
       "outros":["CUBO","PIRÂMIDE","BLOCO"]},
      {"resp":"CUBO","pistas":[
         "Eu tenho <b>lados retos e planos</b>, sem nada redondo.",
         "Na rampa eu <b>fico firme</b> e não saio rolando.",
         "Dá para me <b>empilhar</b> sem cair: sou o dado."],
       "outros":["ESFERA","CONE","CILINDRO"]},
      {"resp":"CILINDRO","pistas":[
         "Eu tenho dois <b>círculos</b>, um em cada ponta.",
         "Deitado eu <b>rolo</b>; em pé eu <b>fico firme</b>.",
         "Pareço uma <b>lata</b> de comida."],
       "outros":["CUBO","ESFERA","PIRÂMIDE"]},
    ])

# 23) INTRUSO — objetos: qual não tem a mesma forma
add(id="f23", mec="intruso", selo="QUAL NÃO É?", conceito="objetivo3",
    enunciado="Três fazem a mesma coisa. <b>Qual é o diferente?</b>",
    dica="Pense na forma de cada objeto: rola ou fica firme?",
    dados=[
      {"selo":"OS QUE ROLAM","tipo":"texto",
       "enun":"Três destes rolam. <b>Qual NÃO rola?</b>",
       "itens":[{"k":"bola","n":"BOLA","img":"sg_bola"},
                {"k":"laranja","n":"LARANJA","img":"sg_laranja"},
                {"k":"lata","n":"LATA","img":"sg_lata"},
                {"k":"dado","n":"DADO","img":"sg_dado"}],
       "fora":"dado","nomeFora":"DADO",
       "d1":"Qual deles NÃO rola de todo jeito?",
       "d2":"Bola e laranja são esferas; a lata é cilindro (rola deitada). O dado tem só cantos.",
       "d3":"O que não pertence é o DADO: é cubo e fica firme.",
       "razoes":[{"t":"Os outros três rolam; o dado fica firme.","ok":1},
                 {"t":"Porque o dado tem números.","ok":0},
                 {"t":"Porque o dado é pequeno.","ok":0},
                 {"t":"Porque o dado é de jogar.","ok":0}],
       "enunPorque":"O <b>dado</b> n&#227;o rola como os outros tr&#234;s. <b>Por qu&#234;</b> isso deixa ele de fora?",
       "p1":"O número no dado não decide a forma. Olhe o que os outros fazem.",
       "p2":"O que junta os três é a forma <b>redonda de rolar</b>.",
       "p3":"Bola, laranja e lata rolam. O dado <b>não rola</b>: fica firme — por isso ele é o diferente.",
       "regra":"bola, laranja e lata rolam; o dado fica firme"},
    ])

# 24) QUEBRA-CABECA — a torre de sólidos
add(id="f24", mec="quebra-cabeca", selo="QUEBRA-CABEÇA", conceito="objetivo3",
    enunciado="Monte a <b>torre</b> de sólidos empilhados.",
    dica="Comece de baixo: o que fica firme vai embaixo.",
    dados={"img":"sg_puzzle2","cols":3,"lins":2,"w":360,"h":360,"fundo":False})

# 25) MEMORIA — sólido <-> objeto (segundo conjunto)
add(id="f25", mec="memoria", selo="MEMÓRIA", conceito="objetivo3",
    enunciado="Ache a <b>palavra</b> e o <b>desenho que combina</b>.",
    dica="Vire duas cartas: uma tem o nome, a outra o desenho. Combinaram? É par!",
    dados=[
      {"k":"pir","pal":"PIRÂMIDE","voz":"pirâmide","imgsen":"sg_piramide_v","vozsen":"pirâmide"},
      {"k":"bloco","pal":"BLOCO","voz":"bloco","imgsen":"sg_bloco_v","vozsen":"bloco"},
      {"k":"cone","pal":"CONE","voz":"cone","imgsen":"sg_cone_v","vozsen":"cone"},
      {"k":"cil","pal":"CILINDRO","voz":"cilindro","imgsen":"sg_cilindro_v","vozsen":"cilindro"}])

# 26) ARRASTAR-SOMBRA — sólido -> silhueta (segundo)
add(id="f26", mec="arrastar-sombra", selo="CADA UM, SUA SOMBRA", conceito="objetivo2",
    enunciado="Leve cada <b>objeto</b> até a sombra da forma dele.",
    dica="Compare o contorno da sombra com o objeto.",
    # f26 usa OBJETOS DO DIA A DIA (não os sólidos de vidro do f10) — silhuetas
    #   bem distintas: bola=círculo, lata=cilindro, dado=quadrado, sorvete=cone.
    #   Assim as duas fases de sombra não são a mesma coisa (menos repetição).
    dados=[{"selo":"CADA UM, SUA SOMBRA","semSom":True,
            "pool":["bola","lata","dado","sorvete"],"n":3,"quais":["bola","lata","dado"]},
           {"selo":"OLHE BEM O CONTORNO","semSom":True,
            "pool":["bola","lata","dado","sorvete"],"n":4,"quais":["bola","lata","dado","sorvete"]}],
    dadosExtra={"FORMAS":{
      "bola":{"n":"BOLA","voz":"BOLA","img":"sg_bola"},
      "lata":{"n":"LATA","voz":"LATA","img":"sg_lata"},
      "dado":{"n":"DADO","voz":"DADO","img":"sg_dado"},
      "sorvete":{"n":"SORVETE","voz":"SORVETE","img":"sg_sorvete"}},
      "DICAS":[
        "Compare o <b>contorno</b>: a sombra tem o mesmo formato.",
        "A sombra certa está <b>piscando</b>. Leve até ela.",
        "Deixa comigo: eu levo esta e você continua."]})

# 27) ESCOLHER — problema do dia a dia (construir)
add(id="f27", mec="escolher", selo="ESCOLHA", conceito="objetivo2",
    enunciado="Ajude o Bloco a <b>construir</b>: escolha a forma certa.",
    dica="Pense se a peça precisa ficar firme ou rolar.",
    dados=[
      {"img":"","p":"Para a <b>base de uma torre</b> bem firme, qual sólido usar?",
       "c":"BLOCO RETANGULAR","e":["ESFERA","CONE","CILINDRO deitado"],
       "d":["A base não pode rolar nem escorregar.","Precisa de lados retos e planos embaixo.","É o BLOCO RETANGULAR. Toque para seguir."]},
      {"img":"","p":"Para o <b>telhado pontudo</b> da casa, qual sólido combina?",
       "c":"PIRÂMIDE","e":["CILINDRO","ESFERA","CUBO"],
       "d":["O telhado tem uma ponta em cima.","Lados de triângulo que sobem até o topo.","É a PIRÂMIDE. Toque para seguir."]},
      {"img":"","p":"Para um <b>rolo que desce a ladeira</b>, qual sólido escolher?",
       "c":"CILINDRO","e":["CUBO","PIRÂMIDE","BLOCO"],
       "d":["Precisa rolar reto, sem sair do caminho.","A esfera rolaria torto; escolha o que rola em linha.","É o CILINDRO. Toque para seguir."]},
    ], dadosExtra={"TITULO":"MÃO NA MASSA","FECHO":"Você escolheu as formas certas para construir!"})

# 28) CLASSIFICAR — empilha / não empilha
add(id="f28", mec="classificar", selo="SEPARE", conceito="objetivo2",
    enunciado="Dá para <b>empilhar</b> firme ou <b>escorrega</b>?",
    dica="Lados retos empilham; parte redonda escorrega.",
    dados=[{"k":"empilha","n":"EMPILHA FIRME","img":"","voz":"empilha firme","rot":False},
           {"k":"escorrega","n":"ESCORREGA / ROLA","img":"","voz":"escorrega","rot":False}],
    dadosExtra={"FICHAS":[
      {"t":"CUBO","alvo":"empilha","img":"sg_cubo_v"},
      {"t":"BLOCO","alvo":"empilha","img":"sg_bloco_v"},
      {"t":"ESFERA","alvo":"escorrega","img":"sg_esfera_v"},
      {"t":"CONE","alvo":"escorrega","img":"sg_cone_v"}],
      "DICAS":[
        "Imagine empilhar dois iguais: fica em pé ou cai?",
        "Cubo e bloco têm topo plano: empilham. Esfera e cone têm parte redonda: escorregam.",
        "Olhe a gaveta com a borda amarela: é ali que esta ficha mora."],
      "ENUN":"Toque no <b>sólido</b>. Depois toque na gaveta: <b>EMPILHA FIRME</b> ou <b>ESCORREGA</b>?"})

# 29) QUEM-SOU-EU — fecho conceitual
add(id="f29", mec="quem-sou-eu", selo="QUEM SOU EU?", conceito="objetivo1",
    enunciado="Última rodada de pistas: qual <b>sólido</b> sou eu?",
    dica="Junte as três pistas antes de responder.",
    dados=[
      {"resp":"CUBO","pistas":[
         "Tenho <b>6 faces</b>, todas quadradas e iguais.",
         "Fico <b>firme</b> e sou fácil de empilhar.",
         "Você me joga no jogo de tabuleiro: sou o <b>dado</b>."],
       "outros":["ESFERA","CILINDRO","CONE"]},
      {"resp":"ESFERA","pistas":[
         "Não tenho <b>nenhum canto</b> nem lado reto.",
         "Eu <b>rolo</b> para qualquer lado.",
         "Sou a <b>bola</b> e também a laranja."],
       "outros":["CUBO","PIRÂMIDE","BLOCO"]},
    ])

# 30b) LIGAR — objeto -> sólido (mais uma rodada, enche a aula)
add(id="f31", mec="ligar", selo="LIGUE", conceito="objetivo3",
    enunciado="Ligue o <b>objeto</b> ao sólido dele.",
    dica="Pense na forma de cada objeto.",
    dados=[{"k":"p0","img":"sg_telhado","voz":"telhado","s":"PIRÂMIDE"},
           {"k":"p1","img":"sg_presente","voz":"presente","s":"CUBO"},
           {"k":"p2","img":"sg_copo","voz":"copo","s":"CILINDRO"},
           {"k":"p3","img":"sg_tijolo","voz":"tijolo","s":"BLOCO RETANGULAR"}],
    dadosExtra={"DICAS":[
      "Pense na forma de cada objeto.",
      "Telhado é pirâmide; presente é cubo; copo é cilindro; tijolo é bloco. Siga a linha.",
      "A resposta certa está acesa, no fim da linha. Toque nela."],
      "FEITOS":[], "ENUN":"Ligue o objeto ao sólido.",
      "FECHO":"Você ligou todos!"})

# 30c) VITRINE — as faces planas (ponte para EF02MA15)
add(id="f32", mec="vitrine", selo="VITRINE", conceito="objetivo3",
    enunciado="Toque em cada sólido e descubra a <b>figura plana</b> da face dele.",
    dica="Olhe um lado do sólido: que figura aparece?",
    dados=[{"img":SOL[s]["v"], "nome":SOL[s]["nome"],
            "grupo":(SOL[s]["face"].upper() if SOL[s]["face"] else "SEM FACE PLANA"),
            "info":(("A face é um %s." % SOL[s]["face"]) if SOL[s]["face"] else "É toda redonda, não tem face plana."),
            "voz":((("%s %s tem face de %s." if SOL[s]["art"]=="o" else "%s %s tem face de %s.")
                    % (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower(), SOL[s]["face"]))
                   if SOL[s]["face"] else
                   ("%s %s é toda redonda, não tem face plana." % (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower())))}
           for s in ORD])

# 30d) ESCOLHER — mais uma rodada do dia a dia
add(id="f33", mec="escolher", selo="ESCOLHA", conceito="objetivo3",
    enunciado="Mais uma! Que <b>sólido</b> tem a forma do objeto?",
    dica="Compare com os sólidos que você conhece.",
    dados=[
      {"img":"sg_presente","p":"A <b>caixa de presente</b> quadrada tem a forma de qual sólido?",
       "c":"CUBO","e":["ESFERA","CILINDRO","CONE"],
       "d":["Tem 6 lados iguais, todos quadrados.","É a mesma forma do dado.","É o CUBO. Toque para seguir."]},
      {"img":"sg_laranja","p":"A <b>laranja</b> tem a forma de qual sólido?",
       "c":"ESFERA","e":["CUBO","BLOCO","PIRÂMIDE"],
       "d":["É toda redonda, sem cantos.","É a mesma forma da bola.","É a ESFERA. Toque para seguir."]},
      {"img":"sg_chapeu","p":"O <b>chapéu de festa</b> tem a forma de qual sólido?",
       "c":"CONE","e":["CILINDRO","CUBO","ESFERA"],
       "d":["Tem ponta em cima e é redondo embaixo.","É a mesma forma da casquinha de sorvete.","É o CONE. Toque para seguir."]},
    ], dadosExtra={"TITULO":"MAIS FORMAS NO DIA A DIA","FECHO":"Você reconhece os sólidos em tudo!"})

# 30e) CLASSIFICAR — objetos por sólido (2 gavetas novas)
add(id="f34", mec="classificar", selo="SEPARE", conceito="objetivo3",
    enunciado="Cada objeto na gaveta do <b>sólido</b> dele.",
    dica="Redondo de rolar ou com cantos retos?",
    dados=[{"k":"cilindro","n":"CILINDRO","img":"sg_cilindro_v","voz":"cilindro","rot":True},
           {"k":"cone","n":"CONE","img":"sg_cone_v","voz":"cone","rot":True}],
    dadosExtra={"FICHAS":[
      {"t":"LATA","alvo":"cilindro","img":"sg_lata"},
      {"t":"COPO","alvo":"cilindro","img":"sg_copo"},
      {"t":"SORVETE","alvo":"cone","img":"sg_sorvete"},
      {"t":"CHAPÉU","alvo":"cone","img":"sg_chapeu"}],
      "DICAS":[
        "Lata e copo são retos e redondos (cilindro); casquinha e chapéu têm ponta (cone).",
        "Cilindro é reto com círculo em cima e embaixo; cone tem uma ponta.",
        "Olhe a gaveta com a borda amarela: é ali que este objeto mora."],
      "ENUN":"Toque no <b>objeto</b>. Depois toque na <b>gaveta do sólido</b> dele."})

# 30) VITRINE — a grande vitrine final (fecho + gancho)
add(id="f30", mec="vitrine", selo="A GRANDE VITRINE", conceito="objetivo1",
    enunciado="A cidade ficou pronta! Toque nos <b>6 sólidos</b> e ouça o que você aprendeu.",
    dica="Toque em cada um e ouça o resumo.",
    dados=[{"img":SOL[s]["v"], "nome":SOL[s]["nome"],
            "grupo":("ROLA" if SOL[s]["rola"] else "FICA FIRME"),
            "info":("%s — %s; parece %s." % (SOL[s]["nome"].lower(), ("rola" if SOL[s]["rola"] else "fica firme"), SOL[s]["obj"][0][1].lower())),
            "voz":("%s %s: %s e parece %s." %
                   (SOL[s]["art"].capitalize(), SOL[s]["nome"].lower(),
                    ("rola" if SOL[s]["rola"] else "fica firme"), SOL[s]["obj"][0][1].lower()))}
           for s in ORD])

# ---- monta o conteudo.json preservando o header já preenchido ----
P = os.path.join(os.path.dirname(__file__), "conteudo.json")
c = json.load(io.open(P, encoding="utf-8"))
c["fases"] = fases
json.dump(c, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("conteudo.json: %d fases" % len(fases))
import collections
print(collections.Counter(f["mec"] for f in fases))
