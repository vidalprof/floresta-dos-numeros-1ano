# -*- coding: utf-8 -*-
u"""Gera _feirinha/conteudo.json — A Feirinha da Dona Coruja (2º ano, matemática).
Problemas de adição e subtração pelos 5 significados: juntar, acrescentar,
separar, retirar e comparar (BNCC/Blumenau EF02MA06). Estilo padrão ESQUELETO
(motor app Broto): conteúdo é DADO; montar.py gera index.html + falas + arte.

⚠️ Formatos EXATOS de cada peça (pecas.json / exemplos reais da _lojinha).
⚠️ Cada fase tem 2–3 RODADAS para ENCHER A AULA (piso 40 min) sem arte nova —
   reaproveita as mesmas figuras/gestos (regra da casa, portão 3g)."""
import io, json, os

PASTA = os.path.dirname(os.path.abspath(__file__))

HAB = (u"Resolver e elaborar problemas de adição e de subtração, envolvendo "
       u"números de até dois algarismos, com os significados de juntar, "
       u"acrescentar, separar e retirar, com o suporte de imagens e/ou material "
       u"manipulável, utilizando diferentes estratégias, inclusive o cálculo "
       u"mental, além de formas de registro pessoais.")
HAB_COMP = (u"Resolver e elaborar problemas de adição e de subtração com os "
            u"significados de juntar, acrescentar, separar, retirar, comparar e "
            u"completar quantidades, utilizando diferentes estratégias de "
            u"cálculo, inclusive o cálculo mental.")

CONTEUDO = {
 u"titulo": u"A Feirinha da Dona Coruja",
 u"sub": u"Matemática · 2º ano · Juntar, acrescentar, separar, retirar e comparar",
 u"ano": u"2º ano",
 u"prefixo": u"fe",
 u"mascote": u"coruja",
 u"mascoteNome": u"Dona Coruja",
 u"voz": u"feminina",
 u"crachas": 6,
 u"fundo": u"fe_fundo.png",
 u"arte": {
   u"cenario": (u"a cozy open-air street market (feira) in a colourful "
     u"german-style town like Blumenau, wooden fruit and vegetable stalls with "
     u"red-and-white striped awnings, wicker baskets and crates full of fruit, "
     u"cobblestone street, warm soft morning light"),
   u"mascote": (u"a plump friendly owl greengrocer, big round amber eyes, soft "
     u"brown and cream feathers, wearing a green apron and a little straw hat, "
     u"holding a small wicker basket, warm and welcoming")
 },
 u"convite": u"<b>Quem vai ajudar a Dona Coruja</b> na feira hoje?",
 u"abertura": (u"Bom dia! A minha feirinha vai abrir e as frutas estão todas "
   u"para contar. Sozinha eu não dou conta... você me ajuda a descobrir quanto "
   u"tem em cada banca?"),
 u"fim": (u"Você salvou a feira, que alegria! Amanhã chega um caminhão cheio de "
   u"frutas novas... será que vamos precisar juntar tudo outra vez? Volte "
   u"amanhã para a gente descobrir!"),
 u"mesa": (u"PEDAGOGO na cabeceira (2º ano — até o 5º ano quem manda é o "
   u"pedagogo, ver _padrao/RECEITA.md), com roteirista, game designer, "
   u"especialista em interatividade, web designer, diretor de arte, engenheiro "
   u"e o PhD de testes que auto-aprende. Foco: EF02MA06 — problemas de adição e "
   u"subtração com os significados de juntar, acrescentar, separar, retirar e "
   u"comparar, com suporte de imagens e cálculo mental."),
 u"conceitos": {
   u"objetivo1": u"Juntar duas partes e ver quanto fica ao todo",
   u"objetivo2": u"Acrescentar: eu tinha, ganhei mais, quanto tenho agora",
   u"objetivo3": u"Separar o todo em partes e ver quanto ficou de um lado",
   u"objetivo4": u"Retirar: tirei um tanto, quanto sobrou",
   u"objetivo5": u"Comparar: quantos a mais (ou a menos) um tem que o outro",
 },
 u"curriculo": {
   u"objetivo1": HAB, u"objetivo2": HAB, u"objetivo3": HAB,
   u"objetivo4": HAB, u"objetivo5": HAB_COMP,
 },
 # falas previsíveis que a peça monta EM JOGO (o colher é aleatório e às vezes
 # não vira uma carta) — declaradas aqui para gravar 100% (memória: uma por par).
 u"falasExtra": [
   u"Ouça: maçã. Ache a figura igual.",
   u"Ouça: laranja. Ache a figura igual.",
   u"Ouça: uva. Ache a figura igual.",
   u"Ouça: banana. Ache a figura igual.",
   u"Ouça: tomate. Ache a figura igual.",
   u"Ouça: morango. Ache a figura igual.",
   u"Ouça: cenoura. Ache a figura igual.",
   u"Ouça: manga. Ache a figura igual.",
   # balão do contadores (sem o "(por extenso)") — um por alvo usado (f01/f07/f15)
   u"Ponha 5 sementes na terra.",
   u"Ponha 7 sementes na terra.",
   u"Ponha 8 sementes na terra.",
   u"Ponha 9 sementes na terra.",
   u"Ponha 10 sementes na terra.",
   u"Ponha 11 sementes na terra.",
   u"Ponha 12 sementes na terra.",
 ],
 u"fases": [],
}

def add(**f):
    CONTEUDO[u"fases"].append(f)

_EXT = {0:u"zero",1:u"um",2:u"dois",3:u"três",4:u"quatro",5:u"cinco",6:u"seis",
        7:u"sete",8:u"oito",9:u"nove",10:u"dez",11:u"onze",12:u"doze",
        13:u"treze",14:u"catorze",15:u"quinze",16:u"dezesseis",17:u"dezessete",
        18:u"dezoito",19:u"dezenove",20:u"vinte",21:u"vinte e um",
        22:u"vinte e dois",23:u"vinte e três",24:u"vinte e quatro",
        25:u"vinte e cinco",30:u"trinta"}
def N(n):
    return {u"t": str(n), u"voz": _EXT.get(n, str(n))}

def esc(img, p, c, e, d):
    return {u"img":img, u"p":p, u"c":N(c), u"e":[N(x) for x in e], u"d":d}

def reta(selo, mn, mx, alvo, num, ap1, ap2, bal, dica):
    return {u"selo":selo, u"min":mn, u"max":mx, u"alvo":alvo, u"tol":0, u"traco":1,
            u"num":num, u"ap1":ap1, u"ap2":ap2, u"bal":bal, u"dica":dica}

# ==================================================================
# AS 32 FASES (2–3 rodadas cada)
# ==================================================================

# ---------- JUNTAR (objetivo1) ----------
# ⭐ tema da contagem (Marcos): a criança PÕE a fruta que a Coruja fala (maçã),
#   não bolinhas; ao CONTAR, a fruta acende como bola numerada (a peça faz isso).
def _cnt(ini, alvo, item, pl, sing, verbo=u"Ponha", onde=u"na cesta",
         label=u"NA CESTA", selo=u"A CESTA"):
    return {u"ini":ini, u"alvo":alvo, u"item":item, u"pl":pl, u"sing":sing,
            u"verbo":verbo, u"onde":onde, u"label":label, u"selo":selo}

add(id=u"f01", mec=u"contadores", selo=u"CONTE JUNTO", conceito=u"objetivo1",
    enunciado=u"A Dona Coruja tem <b>3</b> maçãs e ganhou mais <b>2</b>. Toque para juntar e conte quantas ficam.",
    dica=u"Comece do 3 e continue: 4... 5.",
    # variedade de frutas do banco (Marcos): cada rodada uma fruta diferente,
    # numa bandeja bonita. Mais rodadas ("essa fase pode ter mais fases").
    dados=[_cnt(3,5,u"fe_maca",u"maçãs",u"maçã"),
           _cnt(4,7,u"fe_morango",u"morangos",u"morango"),
           _cnt(5,9,u"fe_laranja",u"laranjas",u"laranja"),
           _cnt(2,6,u"fe_uva",u"uvas",u"uva"),
           _cnt(4,8,u"fe_banana",u"bananas",u"banana")])

add(id=u"f02", mec=u"escolher", selo=u"JUNTAR", conceito=u"objetivo1",
    enunciado=u"Numa cesta há <b>4</b> laranjas e na outra <b>3</b>. Juntando, quantas são?",
    dica=u"Conte as duas cestas de uma vez só.",
    dados=[
      esc(u"fe_laranja", u"Numa cesta há <b>4</b> laranjas e na outra <b>3</b>. Juntando, quantas são?",
          7, [6,8,5], [u"Comece nas 4 e continue nas outras 3.", u"4... 5, 6, 7.", u"São <b>7</b> laranjas. Toque para seguir."]),
      esc(u"fe_maca", u"Há <b>5</b> maçãs numa banca e <b>4</b> na outra. Juntando, quantas são?",
          9, [8,10,7], [u"Comece nas 5 e continue nas outras 4.", u"5... 6, 7, 8, 9.", u"São <b>9</b> maçãs. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTAS AO TODO", u"FECHO":u"Você juntou tudo certinho!"})

add(id=u"f03", mec=u"reta-numerica", selo=u"A RÉGUA DOS PASSOS", conceito=u"objetivo1",
    enunciado=u"Você tinha <b>5</b> e juntou mais <b>3</b>. Onde você chega na régua?",
    dica=u"Ponha o dedo no 5 e ande 3 tracinhos.",
    dados=[
      reta(u"5 + 3", 0,10,8, [0,5,10],[3,8],[1,2,4,6,7,9],
           u"Comece no <b>5</b> e ande <b>3</b>. Onde você chega?", u"A partir do 5: 6, 7, 8."),
      reta(u"6 + 4", 0,10,10, [0,5,10],[6,10],[1,2,3,4,7,8,9],
           u"Comece no <b>6</b> e ande <b>4</b>. Onde você chega?", u"A partir do 6: 7, 8, 9, 10."),
    ],
    dadosExtra={u"ERROS":[]})

add(id=u"f04", mec=u"completar", selo=u"QUANTO FALTA", conceito=u"objetivo1",
    enunciado=u"A Dona Coruja quer encher as cestas da feira. Toque no número que falta para chegar ao total.",
    dica=u"Conte de 6 até 9 nos dedos: quantos você subiu?",
    dados=[{u"img":u"fe_maca", u"ante":u"Tinha 6 maçãs, quero 9. Faltam ", u"dep":u" maçãs.",
            u"cer":u"3", u"out":[u"2", u"4"], u"dic":u"De 6 para 9: 7, 8, 9 — são 3."},
           {u"img":u"fe_uva", u"ante":u"Tinha 4 cachos, quero 10. Faltam ", u"dep":u" cachos.",
            u"cer":u"6", u"out":[u"5", u"7"], u"dic":u"De 4 até 10: 5, 6, 7, 8, 9, 10 — são 6."},
           {u"img":u"fe_laranja", u"ante":u"Tinha 7 laranjas, quero 12. Faltam ", u"dep":u".",
            u"cer":u"5", u"out":[u"4", u"6"], u"dic":u"De 7 até 12: 8, 9, 10, 11, 12 — são 5."}],
    dadosExtra={u"ENUN":u"Toque no número que <b>falta</b> para fechar a conta.",
                u"DEPOIS":u"Leia a conta inteira antes de escolher.",
                u"FECHO":u"Você fechou as contas!"})

# ---------- ACRESCENTAR (objetivo2) ----------
add(id=u"f05", mec=u"saltos-na-fita", selo=u"PULOS DE 2", conceito=u"objetivo2",
    enunciado=u"A cada cesta a Coruja guarda <b>2</b> frutas. Dê os pulos de 2 em 2 até o fim.",
    dica=u"Um pulo tem sempre 2 passinhos: conte um, dois.",
    dados=[{u"p":2, u"ate":12, u"dic":u"Um pulo tem sempre <b>2</b> passinhos. Conte a partir de onde ela está."},
           {u"p":2, u"ate":16, u"dic":u"De 2 em 2: 2, 4, 6, 8, 10, 12, 14, 16."}])

add(id=u"f06", mec=u"escolher", selo=u"ACRESCENTAR", conceito=u"objetivo2",
    enunciado=u"A Coruja tinha <b>8</b> bananas e ganhou mais <b>4</b>. Quantas tem agora?",
    dica=u"Comece do 8 e acrescente 4.",
    dados=[
      esc(u"fe_banana", u"Tinha <b>8</b> bananas e ganhou mais <b>4</b>. Quantas agora?",
          12, [11,13,10], [u"Guarde o 8 e conte mais 4.", u"8... 9, 10, 11, 12.", u"São <b>12</b> bananas. Toque para seguir."]),
      esc(u"fe_morango", u"Havia <b>6</b> morangos e você colocou mais <b>3</b>. Quantos agora?",
          9, [8,10,7], [u"Comece do 6 e conte mais 3.", u"6... 7, 8, 9.", u"São <b>9</b> morangos. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTAS AGORA", u"FECHO":u"Você acrescentou certinho!"})

add(id=u"f07", mec=u"contadores", selo=u"CONTE JUNTO", conceito=u"objetivo2",
    enunciado=u"Havia <b>6</b> morangos na tigela e você coloca mais <b>5</b>. Conte quantos ficam.",
    dica=u"Comece do 6 e continue: 7, 8...",
    dados=[_cnt(6,11,u"fe_morango",u"morangos",u"morango",onde=u"na tigela",label=u"NA TIGELA",selo=u"A TIGELA"),
           _cnt(7,10,u"fe_morango",u"morangos",u"morango",onde=u"na tigela",label=u"NA TIGELA",selo=u"A TIGELA")])

add(id=u"f08", mec=u"completar", selo=u"QUANTO FALTA", conceito=u"objetivo2",
    enunciado=u"A Coruja está enchendo a banca. Toque em quanto ela precisa acrescentar.",
    dica=u"Conte de 7 até 13.",
    dados=[{u"img":u"fe_tomate", u"ante":u"Tinha 7 tomates, quer 13. Precisa de mais ", u"dep":u".",
            u"cer":u"6", u"out":[u"5", u"7"], u"dic":u"De 7 até 13: 8, 9, 10, 11, 12, 13 — são 6."},
           {u"img":u"fe_banana", u"ante":u"Tinha 9 bananas, quer 14. Precisa de mais ", u"dep":u".",
            u"cer":u"5", u"out":[u"4", u"6"], u"dic":u"De 9 até 14: 10, 11, 12, 13, 14 — são 5."}],
    dadosExtra={u"ENUN":u"Toque no número que <b>falta</b>.",
                u"DEPOIS":u"Leia a conta inteira antes de escolher.",
                u"FECHO":u"Você completou!"})

# ---------- SEPARAR (objetivo3) ----------
# ⭐ resultados VARIADOS (Marcos: "estão sempre dando 3"): 6, 5 e 4 — nunca o mesmo;
#   3 rodadas, frutas variadas. (A peça escolher já embaralha as opções na tela.)
add(id=u"f09", mec=u"escolher", selo=u"SEPARAR", conceito=u"objetivo3",
    enunciado=u"Você tinha <b>8</b> uvas e separou <b>2</b> num pratinho. Quantas sobraram no cacho?",
    dica=u"Tire as que separou e veja quantas ficam.",
    dados=[
      esc(u"fe_uva", u"Tinha <b>8</b> uvas e separou <b>2</b>. Quantas sobraram?",
          6, [5,7,4], [u"Comece do 8 e volte 2.", u"8... 7, 6.", u"Sobraram <b>6</b> uvas. Toque para seguir."]),
      esc(u"fe_tomate", u"Tinha <b>9</b> tomates e separou <b>4</b> para o molho. Quantos sobraram?",
          5, [6,4,3], [u"Comece do 9 e volte 4.", u"9... 8, 7, 6, 5.", u"Sobraram <b>5</b> tomates. Toque para seguir."]),
      esc(u"fe_laranja", u"Tinha <b>7</b> laranjas e separou <b>3</b> na cesta. Quantas sobraram?",
          4, [3,5,6], [u"Comece do 7 e volte 3.", u"7... 6, 5, 4.", u"Sobraram <b>4</b> laranjas. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTAS SOBRARAM", u"FECHO":u"Você separou certinho!"})

add(id=u"f10", mec=u"base-dez", selo=u"CAIXA DE 10", conceito=u"objetivo3",
    enunciado=u"Junte as frutas soltas em <b>caixas de 10</b> e veja quantas caixas e soltas ficam.",
    dica=u"Cada 10 soltas enchem 1 caixa.",
    dados=[{u"selo":u"CAIXA DE 10", u"soltos":13, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
            u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
            u"fala":u"Cada <b>10 soltas</b> viram <b>1 caixa</b>. Encha a caixa e troque."},
           {u"selo":u"CAIXA DE 10", u"soltos":16, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
            u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
            u"fala":u"Encha a <b>caixa de 10</b> e veja quantas soltas sobram."}],
    dadosExtra={u"DICAS":[u"Conte 10 frutas soltas e arraste para a caixa.",
                          u"Quando a caixa enche, ela vira 1 caixa de 10.",
                          u"Deixa comigo: eu encho esta caixa e você segue."]})

add(id=u"f11", mec=u"repartir", selo=u"REPARTIR IGUAL", conceito=u"objetivo3",
    enunciado=u"Separe <b>10</b> frutas em <b>2</b> bancas iguais. Quantas em cada?",
    dica=u"Ponha uma de cada vez, uma para cada banca.",
    dados=[{u"un":10, u"n":2, u"nome":u"a <b>metade</b>", u"selo":u"REPARTIR IGUAL"},
           {u"un":8, u"n":2, u"nome":u"a <b>metade</b>", u"selo":u"REPARTIR IGUAL"}],
    dadosExtra={u"DICAS":[u"Dê uma fruta para cada banca, por vez.",
                          u"Quando acabar, conte quantas ficaram em uma banca.",
                          u"Deixa comigo: eu reparto e você confere."]})

add(id=u"f12", mec=u"reta-numerica", selo=u"A RÉGUA DOS PASSOS", conceito=u"objetivo3",
    enunciado=u"Você tinha <b>12</b> e separou <b>5</b>. Onde você chega na régua?",
    dica=u"Ponha o dedo no 12 e volte 5 tracinhos.",
    dados=[
      reta(u"12 − 5", 0,15,7, [0,5,10,15],[7,12],[2,4,6,8,9,11,13,14],
           u"Comece no <b>12</b> e volte <b>5</b>. Onde você chega?", u"Para trás do 12: 11, 10, 9, 8, 7."),
      reta(u"10 − 4", 0,15,6, [0,5,10,15],[6,10],[2,4,7,8,9,11,12,13,14],
           u"Comece no <b>10</b> e volte <b>4</b>. Onde você chega?", u"Para trás do 10: 9, 8, 7, 6."),
    ],
    dadosExtra={u"ERROS":[]})

# ---------- AQUECIMENTO (revisão espaçada) ----------
add(id=u"aquecimento", mec=u"memoria", selo=u"AQUECIMENTO", conceito=u"objetivo1",
    enunciado=u"Pare para descansar: ache os <b>pares</b> de frutas iguais.",
    dica=u"Vire duas cartas e veja se combinam.",
    dados=[{u"k":u"m", u"img":u"fe_maca", u"imgsen":u"fe_maca", u"voz":u"maçã", u"vozsen":u"maçã"},
           {u"k":u"l", u"img":u"fe_laranja", u"imgsen":u"fe_laranja", u"voz":u"laranja", u"vozsen":u"laranja"},
           {u"k":u"u", u"img":u"fe_uva", u"imgsen":u"fe_uva", u"voz":u"uva", u"vozsen":u"uva"},
           {u"k":u"b", u"img":u"fe_banana", u"imgsen":u"fe_banana", u"voz":u"banana", u"vozsen":u"banana"},
           {u"k":u"t", u"img":u"fe_tomate", u"imgsen":u"fe_tomate", u"voz":u"tomate", u"vozsen":u"tomate"},
           {u"k":u"o", u"img":u"fe_morango", u"imgsen":u"fe_morango", u"voz":u"morango", u"vozsen":u"morango"}])

# ---------- RETIRAR (objetivo4) ----------
add(id=u"f14", mec=u"escolher", selo=u"RETIRAR", conceito=u"objetivo4",
    enunciado=u"A Coruja tinha <b>8</b> limões e vendeu <b>3</b>. Quantos restaram na banca?",
    dica=u"Tire os 3 vendidos e conte o que sobra.",
    dados=[
      esc(u"fe_limao", u"Tinha <b>8</b> limões e vendeu <b>3</b>. Quantos restaram?",
          5, [6,4,11], [u"Comece do 8 e volte 3.", u"8... 7, 6, 5.", u"Restaram <b>5</b> limões. Toque para seguir."]),
      esc(u"fe_maca", u"Tinha <b>10</b> maçãs e vendeu <b>4</b>. Quantas restaram?",
          6, [5,7,14], [u"Comece do 10 e volte 4.", u"10... 9, 8, 7, 6.", u"Restaram <b>6</b> maçãs. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTOS RESTARAM", u"FECHO":u"Você retirou certinho!"})

add(id=u"f15", mec=u"contadores", selo=u"CONTE O QUE SOBRA", conceito=u"objetivo4",
    enunciado=u"Havia <b>14</b> laranjas e a Coruja tirou <b>6</b> estragadas. Conte quantas boas sobraram.",
    dica=u"Conte só as laranjas boas que ficaram.",
    dados=[_cnt(0,8,u"fe_laranja",u"laranjas",u"laranja",onde=u"na caixa",label=u"NA CAIXA",selo=u"A CAIXA"),
           _cnt(0,7,u"fe_laranja",u"laranjas",u"laranja",onde=u"na caixa",label=u"NA CAIXA",selo=u"A CAIXA")])

add(id=u"f16", mec=u"comparar", selo=u"QUANTAS A MAIS?", conceito=u"objetivo5",
    enunciado=u"Compare as duas bancas. <b>Quantas cenouras a mais</b> que tomates?",
    dica=u"Case cada cenoura com um tomate e veja quantas sobram.",
    dados=[
      {u"a":6, u"b":4, u"modo":u"blocos", u"imgA":u"fe_cenoura", u"imgB":u"fe_tomate",
       u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
       u"enun":u"Quantas <b>cenouras a mais</b> que tomates?", u"voz":u"Quantas cenouras a mais que tomates?"},
      {u"a":7, u"b":5, u"modo":u"blocos", u"imgA":u"fe_cenoura", u"imgB":u"fe_tomate",
       u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
       u"enun":u"Agora: quantas <b>cenouras a mais</b> que tomates?", u"voz":u"Quantas cenouras a mais que tomates?"},
    ],
    dadosExtra={u"D1":[u"Ponha uma cenoura em frente de cada tomate.",
                       u"As cenouras que sobram sem par são as “a mais”.",
                       u"Conte as que sobraram e toque no número."]})

add(id=u"f17", mec=u"escolher", selo=u"RETIRAR", conceito=u"objetivo4",
    enunciado=u"Havia <b>9</b> pães e a Coruja vendeu <b>4</b>. Quantos sobraram?",
    dica=u"Comece do 9 e volte 4.",
    dados=[
      esc(u"fe_pao", u"Havia <b>9</b> pães e vendeu <b>4</b>. Quantos sobraram?",
          5, [4,6,13], [u"Comece do 9 e volte 4.", u"9... 8, 7, 6, 5.", u"Sobraram <b>5</b> pães. Toque para seguir."]),
      esc(u"fe_pao", u"Havia <b>12</b> pães e vendeu <b>5</b>. Quantos sobraram?",
          7, [6,8,17], [u"Comece do 12 e volte 5.", u"12... 11, 10, 9, 8, 7.", u"Sobraram <b>7</b> pães. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTOS SOBRARAM", u"FECHO":u"Você acertou o resto!"})

add(id=u"f18", mec=u"reta-numerica", selo=u"A RÉGUA DOS PASSOS", conceito=u"objetivo4",
    enunciado=u"A caixa tinha <b>15</b> frutas e a Coruja tirou <b>3</b> estragadas. Onde você chega na régua?",
    dica=u"Comece no 15 e volte 3 tracinhos.",
    dados=[
      reta(u"15 − 3", 0,20,12, [0,5,10,15,20],[12,15],[2,4,6,8,11,14,16,18],
           u"Comece no <b>15</b> e volte <b>3</b>. Onde você chega?", u"Para trás do 15: 14, 13, 12."),
      reta(u"14 − 4", 0,20,10, [0,5,10,15,20],[10,14],[2,4,6,8,12,16,18],
           u"Comece no <b>14</b> e volte <b>4</b>. Onde você chega?", u"Para trás do 14: 13, 12, 11, 10."),
    ],
    dadosExtra={u"ERROS":[]})

# ---------- COMPARAR (objetivo5) ----------
add(id=u"f19", mec=u"comparar", selo=u"QUANTAS A MENOS?", conceito=u"objetivo5",
    enunciado=u"Uma banca tem <b>9</b> maçãs e outra <b>5</b>. <b>Quantas a menos</b> tem a segunda?",
    dica=u"Case as frutas e veja quantas faltam na banca menor.",
    dados=[
      {u"a":9, u"b":5, u"modo":u"blocos", u"imgA":u"fe_maca", u"imgB":u"fe_maca",
       u"pergunta":u"menos", u"semSinal":True, u"selo":u"QUANTAS A MENOS?",
       u"enun":u"Quantas maçãs a <b>segunda</b> banca tem a menos?", u"voz":u"Quantas maçãs a segunda banca tem a menos?"},
      {u"a":8, u"b":6, u"modo":u"blocos", u"imgA":u"fe_uva", u"imgB":u"fe_uva",
       u"pergunta":u"menos", u"semSinal":True, u"selo":u"QUANTAS A MENOS?",
       u"enun":u"Quantos cachos a <b>segunda</b> banca tem a menos?", u"voz":u"Quantos cachos a segunda banca tem a menos?"},
    ],
    dadosExtra={u"D1":[u"Case cada fruta de cima com uma de baixo.",
                       u"As que faltam embaixo são as “a menos”.",
                       u"Conte quantas faltaram e toque no número."]})

add(id=u"f20", mec=u"completar", selo=u"QUANTO FALTA", conceito=u"objetivo5",
    enunciado=u"A Coruja quer deixar as duas bancas iguais. Toque em quanto falta na banca menor.",
    dica=u"De 4 até 6, quantos faltam?",
    dados=[{u"img":u"fe_tomate", u"ante":u"Uma banca tem 6 e a outra 4. Faltam ", u"dep":u" para ficarem iguais.",
            u"cer":u"2", u"out":[u"1", u"3"], u"dic":u"De 4 até 6: 5, 6 — faltam 2."},
           {u"img":u"fe_maca", u"ante":u"Uma banca tem 8 e a outra 5. Faltam ", u"dep":u" para ficarem iguais.",
            u"cer":u"3", u"out":[u"2", u"4"], u"dic":u"De 5 até 8: 6, 7, 8 — faltam 3."}],
    dadosExtra={u"ENUN":u"Toque no número que <b>falta</b> para igualar.",
                u"DEPOIS":u"Leia a frase inteira antes de escolher.",
                u"FECHO":u"Agora as bancas estão iguais!"})

add(id=u"f21", mec=u"escolher", selo=u"COMPARAR", conceito=u"objetivo5",
    enunciado=u"Na feira há <b>13</b> laranjas e <b>8</b> limões. Quantas laranjas a mais?",
    dica=u"Quantos passos de 8 até 13?",
    dados=[
      esc(u"fe_laranja", u"Há <b>13</b> laranjas e <b>8</b> limões. Quantas laranjas a mais?",
          5, [4,6,21], [u"Case cada limão com uma laranja.", u"De 8 até 13: 9, 10, 11, 12, 13 — são 5.", u"São <b>5</b> a mais. Toque para seguir."]),
      esc(u"fe_maca", u"Há <b>15</b> maçãs e <b>9</b> mangas. Quantas maçãs a mais?",
          6, [5,7,24], [u"Case cada manga com uma maçã.", u"De 9 até 15: 10, 11, 12, 13, 14, 15 — são 6.", u"São <b>6</b> a mais. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"QUANTOS A MAIS", u"FECHO":u"Você comparou certinho!"})

add(id=u"f22", mec=u"estimar", selo=u"CHUTE ESPERTO", conceito=u"objetivo5",
    enunciado=u"Sem contar de um em um: quantas frutas você acha que tem neste pote?",
    dica=u"Olhe um punhado e imagine quantos punhados cabem.",
    dados=[{u"n":14, u"max":30, u"ini":15, u"qa":10, u"cls":u"", u"seed":41, u"ancora":1,
            u"selo":u"O POTE DE FRUTAS", u"coisa":u"frutas", u"voz":u"frutas", u"atalhos":[5,10,20]},
           {u"n":19, u"max":30, u"ini":15, u"qa":12, u"cls":u"grao", u"seed":58, u"ancora":1,
            u"selo":u"O SACO DE GRÃOS", u"coisa":u"grãos", u"voz":u"grãos", u"atalhos":[5,10,20]}],
    dadosExtra={u"ESTRAT":[u"Escolha um cantinho, conte quantas tem ali.",
                           u"Veja quantas vezes aquele cantinho cabe no pote.",
                           u"Chegou perto? Ótimo! Estimar é chegar perto sem contar tudo."]})

# ---------- REVISÃO / PROFUNDIDADE ----------
add(id=u"f23", mec=u"escolher", selo=u"JUNTAR", conceito=u"objetivo1",
    enunciado=u"De manhã a Coruja vendeu <b>12</b> frutas e de tarde <b>7</b>. Quantas no dia?",
    dica=u"Junte a manhã com a tarde.",
    dados=[
      esc(u"fe_morango", u"Vendeu <b>12</b> de manhã e <b>7</b> de tarde. Quantas no dia?",
          19, [18,20,5], [u"Comece do 12 e acrescente 7.", u"12... 13, 14, 15, 16, 17, 18, 19.", u"São <b>19</b> frutas. Toque para seguir."]),
      esc(u"fe_uva", u"Colheu <b>14</b> cachos numa parreira e <b>5</b> na outra. Quantos ao todo?",
          19, [18,20,9], [u"Comece do 14 e acrescente 5.", u"14... 15, 16, 17, 18, 19.", u"São <b>19</b> cachos. Toque para seguir."]),
    ],
    dadosExtra={u"TITULO":u"O DIA INTEIRO", u"FECHO":u"Você juntou o dia todo!"})

add(id=u"f24", mec=u"ordenar", selo=u"DO MENOR AO MAIOR", conceito=u"objetivo5",
    enunciado=u"Ponha as bancas em ordem, <b>da que tem menos à que tem mais</b>.",
    dica=u"Ache primeiro a banca com menos frutas.",
    dados=[{u"v":5, u"img":u"fe_maca", u"nome":u"5 maçãs"},
           {u"v":8, u"img":u"fe_uva", u"nome":u"8 uvas"},
           {u"v":11, u"img":u"fe_banana", u"nome":u"11 bananas"},
           {u"v":15, u"img":u"fe_laranja", u"nome":u"15 laranjas"}],
    dadosExtra={u"ORDTXT":{u"selo":u"EM ORDEM",
        u"balao":u"Ponha as bancas <b>da que tem menos à que tem mais</b>.",
        u"hint":u"Toque na banca ou arraste até a fila.",
        u"d":[u"Procure o <b>menor</b> número de frutas.",
             u"A menor que sobrou está piscando. Toque nela.",
             u"Era esta! Eu ponho e você segue."],
        u"fim":u"Fila pronta! Da que tem menos à que tem mais."}})

add(id=u"f25", mec=u"reta-numerica", selo=u"A RÉGUA DOS PASSOS", conceito=u"objetivo4",
    enunciado=u"Você tinha <b>18</b> frutas e vendeu <b>6</b>. Onde você chega na régua?",
    dica=u"Comece no 18 e volte 6.",
    dados=[
      reta(u"18 − 6", 0,20,12, [0,5,10,15,20],[12,18],[2,4,6,8,14,16],
           u"Comece no <b>18</b> e volte <b>6</b>. Onde você chega?", u"Para trás do 18: 17, 16, 15, 14, 13, 12."),
      reta(u"16 − 5", 0,20,11, [0,5,10,15,20],[11,16],[2,4,6,8,13,18],
           u"Comece no <b>16</b> e volte <b>5</b>. Onde você chega?", u"Para trás do 16: 15, 14, 13, 12, 11."),
    ],
    dadosExtra={u"ERROS":[]})

add(id=u"f26", mec=u"comparar", selo=u"QUANTAS A MAIS?", conceito=u"objetivo5",
    enunciado=u"A banca de maçãs tem <b>11</b> e a de mangas <b>7</b>. Quantas maçãs a mais?",
    dica=u"Case cada manga com uma maçã.",
    dados=[
      {u"a":11, u"b":7, u"modo":u"blocos", u"imgA":u"fe_maca", u"imgB":u"fe_manga",
       u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
       u"enun":u"Quantas <b>maçãs a mais</b> que mangas?", u"voz":u"Quantas maçãs a mais que mangas?"},
      {u"a":12, u"b":8, u"modo":u"blocos", u"imgA":u"fe_banana", u"imgB":u"fe_limao",
       u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
       u"enun":u"Quantas <b>bananas a mais</b> que limões?", u"voz":u"Quantas bananas a mais que limões?"},
    ],
    dadosExtra={u"D1":[u"Case cada fruta menor com uma da banca maior.",
                       u"As que sobram são as “a mais”.",
                       u"Conte as que sobraram e toque no número."]})

add(id=u"f27", mec=u"base-dez", selo=u"DEZ E SOLTAS", conceito=u"objetivo1",
    enunciado=u"A Coruja tem <b>1 caixa de 10</b> e <b>7</b> soltas. Junte e veja quanto dá.",
    dica=u"Uma caixa vale 10; some as soltas.",
    dados=[{u"selo":u"DEZ E SOLTAS", u"soltos":17, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
            u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
            u"fala":u"Uma <b>caixa</b> vale 10. Junte com as soltas para saber o total."},
           {u"selo":u"DEZ E SOLTAS", u"soltos":12, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
            u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
            u"fala":u"Encha a caixa de 10 e leia: dez e mais as soltas."}],
    dadosExtra={u"DICAS":[u"Encha a caixa com 10 e veja quantas soltas sobram.",
                          u"1 caixa (10) e as soltas: leia dez e mais um tanto.",
                          u"Deixa comigo: eu encho e você lê o total."]})

add(id=u"f28", mec=u"completar", selo=u"AS DUAS PARTES", conceito=u"objetivo3",
    enunciado=u"A Dona Coruja separou as frutas em dois pratos. Sabendo o que tem em um prato, descubra quantas ficaram no outro.",
    dica=u"De 8 até 12, quantos faltam?",
    dados=[{u"img":u"fe_uva", u"ante":u"12 uvas em dois pratos. Num prato há 8, no outro há ", u"dep":u".",
            u"cer":u"4", u"out":[u"3", u"5"], u"dic":u"De 8 até 12: 9, 10, 11, 12 — são 4."},
           {u"img":u"fe_maca", u"ante":u"10 maçãs em duas cestas. Numa há 7, na outra há ", u"dep":u".",
            u"cer":u"3", u"out":[u"2", u"4"], u"dic":u"De 7 até 10: 8, 9, 10 — são 3."}],
    dadosExtra={u"ENUN":u"Toque na <b>outra parte</b> que falta.",
                u"DEPOIS":u"O todo se separa em duas partes.",
                u"FECHO":u"Você achou a outra parte!"})

add(id=u"f29", mec=u"repartir", selo=u"REPARTIR IGUAL", conceito=u"objetivo3",
    enunciado=u"Separe <b>12</b> frutas em <b>3</b> caixas iguais. Quantas em cada?",
    dica=u"Uma de cada vez, uma para cada caixa.",
    dados=[{u"un":12, u"n":3, u"nome":u"<b>um terço</b>", u"selo":u"REPARTIR IGUAL"},
           {u"un":9, u"n":3, u"nome":u"<b>um terço</b>", u"selo":u"REPARTIR IGUAL"}],
    dadosExtra={u"DICAS":[u"Dê uma fruta para cada caixa, por rodada.",
                          u"No fim, conte quantas ficaram em uma caixa.",
                          u"Deixa comigo: eu reparto e você confere."]})

add(id=u"f30", mec=u"escolher", selo=u"QUAL CONTA?", conceito=u"objetivo4",
    enunciado=u"“Tinha 10 e vendeu 3.” Para achar o que sobrou, qual conta a Coruja faz?",
    dica=u"“Sobrou”, “restou” e “tirou” pedem subtração.",
    dados=[
      {u"p":u"“Tinha 10 e <b>vendeu 3</b>.” Que conta acha o que sobrou?",
       u"c":{u"t":u"10 − 3", u"voz":u"dez menos três"},
       u"e":[{u"t":u"10 + 3", u"voz":u"dez mais três"}, {u"t":u"3 + 3", u"voz":u"três mais três"}],
       u"d":[u"Ela tinha e TIROU: ficou com menos.", u"Tirar pede o sinal de menos.", u"É <b>10 − 3</b>. Toque para seguir."]},
      {u"p":u"“Tinha 6 e <b>ganhou 4</b>.” Que conta acha quanto tem agora?",
       u"c":{u"t":u"6 + 4", u"voz":u"seis mais quatro"},
       u"e":[{u"t":u"6 − 4", u"voz":u"seis menos quatro"}, {u"t":u"4 − 4", u"voz":u"quatro menos quatro"}],
       u"d":[u"Ela GANHOU: ficou com mais.", u"Ganhar pede o sinal de mais.", u"É <b>6 + 4</b>. Toque para seguir."]},
    ],
    dadosExtra={u"TITULO":u"MAIS OU MENOS?", u"FECHO":u"Você sabe escolher a conta!"})

add(id=u"f31", mec=u"saltos-na-fita", selo=u"PULOS DE 5", conceito=u"objetivo1",
    enunciado=u"A Coruja arruma as frutas em cestas de <b>5</b>. Dê os pulos de 5 em 5.",
    dica=u"Um pulo tem 5 passinhos: conte até cinco.",
    dados=[{u"p":5, u"ate":20, u"dic":u"De 5 em 5: 5, 10, 15, 20."},
           {u"p":3, u"ate":15, u"dic":u"De 3 em 3: 3, 6, 9, 12, 15."}])

add(id=u"f32", mec=u"estimar", selo=u"O TOTAL DO DIA", conceito=u"objetivo5",
    enunciado=u"Fechando a feira: sem contar tudo, quantas frutas você acha que sobraram?",
    dica=u"Olhe um punhado e imagine quantos cabem.",
    dados=[{u"n":22, u"max":40, u"ini":20, u"qa":18, u"cls":u"gude", u"seed":73, u"ancora":1,
            u"selo":u"O CESTO DO FIM DO DIA", u"coisa":u"frutas", u"voz":u"frutas", u"atalhos":[10,20,30]},
           {u"n":16, u"max":40, u"ini":20, u"qa":14, u"cls":u"", u"seed":29, u"ancora":1,
            u"selo":u"A ÚLTIMA CAIXA", u"coisa":u"frutas", u"voz":u"frutas", u"atalhos":[10,20,30]}],
    dadosExtra={u"ESTRAT":[u"Conte um cantinho do cesto.",
                           u"Veja quantas vezes ele cabe no cesto todo.",
                           u"Chegou perto? Estimar é acertar por volta, sem contar tudo!"]})

# ==================================================================
# 3ª RODADA em cada fase — enche a aula (piso 40 min) sem arte nova.
# Acrescenta um round a mais em cada fase, com números novos e progressivos,
# reaproveitando as MESMAS figuras. (portão 3g / _qa/duracao.py)
# ==================================================================
_R3 = {
 u"f01": {u"ini":6, u"alvo":10},
 u"f07": {u"ini":8, u"alvo":12},
 u"f15": {u"ini":0, u"alvo":9},
 u"f02": esc(u"fe_uva", u"Há <b>6</b> uvas num prato e <b>2</b> no outro. Juntando, quantas são?",
             8, [7,9,6], [u"Comece nas 6 e continue nas outras 2.", u"6... 7, 8.", u"São <b>8</b> uvas. Toque para seguir."]),
 u"f06": esc(u"fe_maca", u"Tinha <b>7</b> maçãs e ganhou mais <b>5</b>. Quantas agora?",
             12, [11,13,10], [u"Guarde o 7 e conte mais 5.", u"7... 8, 9, 10, 11, 12.", u"São <b>12</b> maçãs. Toque para seguir."]),
 u"f09": esc(u"fe_morango", u"Tinha <b>10</b> morangos e separou <b>7</b>. Quantos sobraram?",
             3, [4,2,5], [u"Comece do 10 e volte 7.", u"10... 9, 8, 7, 6, 5, 4, 3.", u"Sobraram <b>3</b>. Toque para seguir."]),
 u"f14": esc(u"fe_limao", u"Tinha <b>11</b> limões e vendeu <b>5</b>. Quantos restaram?",
             6, [5,7,16], [u"Comece do 11 e volte 5.", u"11... 10, 9, 8, 7, 6.", u"Restaram <b>6</b>. Toque para seguir."]),
 u"f17": esc(u"fe_pao", u"Havia <b>14</b> pães e vendeu <b>6</b>. Quantos sobraram?",
             8, [7,9,20], [u"Comece do 14 e volte 6.", u"14... 13, 12, 11, 10, 9, 8.", u"Sobraram <b>8</b>. Toque para seguir."]),
 u"f21": esc(u"fe_banana", u"Há <b>12</b> bananas e <b>7</b> limões. Quantas bananas a mais?",
             5, [4,6,19], [u"Case cada limão com uma banana.", u"De 7 até 12: 8, 9, 10, 11, 12 — são 5.", u"São <b>5</b> a mais. Toque para seguir."]),
 u"f23": esc(u"fe_laranja", u"A Coruja juntou <b>16</b> laranjas de um caixote e <b>3</b> de outro. Quantas ao todo?",
             19, [18,20,13], [u"Comece do 16 e junte mais 3.", u"16... 17, 18, 19.", u"São <b>19</b>. Toque para seguir."]),
 u"f30": {u"p":u"“Tinha 12 e <b>separou 5</b> num pote.” Que conta acha o que sobrou?",
          u"c":{u"t":u"12 − 5", u"voz":u"doze menos cinco"},
          u"e":[{u"t":u"12 + 5", u"voz":u"doze mais cinco"}, {u"t":u"5 + 5", u"voz":u"cinco mais cinco"}],
          u"d":[u"Ela SEPAROU uma parte: ficou com menos.", u"Separar/tirar pede o menos.", u"É <b>12 − 5</b>. Toque para seguir."]},
 u"f04": {u"img":u"fe_banana", u"ante":u"Tinha 8 bananas, quero 15. Faltam ", u"dep":u".",
          u"cer":u"7", u"out":[u"6", u"8"], u"dic":u"De 8 até 15: 9,10,11,12,13,14,15 — são 7."},
 u"f08": {u"img":u"fe_uva", u"ante":u"Tinha 5 cachos, quer 11. Precisa de mais ", u"dep":u".",
          u"cer":u"6", u"out":[u"5", u"7"], u"dic":u"De 5 até 11: 6,7,8,9,10,11 — são 6."},
 u"f20": {u"img":u"fe_laranja", u"ante":u"Uma banca tem 9 e a outra 5. Faltam ", u"dep":u" para ficarem iguais.",
          u"cer":u"4", u"out":[u"3", u"5"], u"dic":u"De 5 até 9: 6,7,8,9 — faltam 4."},
 u"f28": {u"img":u"fe_tomate", u"ante":u"14 tomates em duas caixas. Numa há 9, na outra há ", u"dep":u".",
          u"cer":u"5", u"out":[u"4", u"6"], u"dic":u"De 9 até 14: 10,11,12,13,14 — são 5."},
 u"f03": reta(u"7 + 2", 0,10,9, [0,5,10],[7,9],[1,2,3,4,6,8],
              u"Comece no <b>7</b> e ande <b>2</b>. Onde você chega?", u"A partir do 7: 8, 9."),
 u"f12": reta(u"11 − 4", 0,15,7, [0,5,10,15],[7,11],[2,4,6,8,9,12,13,14],
              u"Comece no <b>11</b> e volte <b>4</b>. Onde você chega?", u"Para trás do 11: 10, 9, 8, 7."),
 u"f18": reta(u"13 − 5", 0,20,8, [0,5,10,15,20],[8,13],[2,4,6,11,16,18],
              u"Comece no <b>13</b> e volte <b>5</b>. Onde você chega?", u"Para trás do 13: 12, 11, 10, 9, 8."),
 u"f25": reta(u"19 − 7", 0,20,12, [0,5,10,15,20],[12,19],[2,4,6,8,14,16,18],
              u"Comece no <b>19</b> e volte <b>7</b>. Onde você chega?", u"Para trás do 19: 18, 17, 16, 15, 14, 13, 12."),
 u"f10": {u"selo":u"CAIXA DE 10", u"soltos":18, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
          u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
          u"fala":u"Encha a <b>caixa de 10</b> e conte as soltas que sobram."},
 u"f27": {u"selo":u"DEZ E SOLTAS", u"soltos":15, u"pTipo":u"dsuni", u"tTipo":u"dsdez",
          u"vale":1, u"valeT":10, u"nomeP":u"soltas", u"nomeT":u"caixa de 10", u"nomeTs":u"caixas de 10",
          u"fala":u"Uma caixa (10) e as soltas: leia o total."},
 u"f11": {u"un":6, u"n":2, u"nome":u"a <b>metade</b>", u"selo":u"REPARTIR IGUAL"},
 u"f29": {u"un":6, u"n":3, u"nome":u"<b>um terço</b>", u"selo":u"REPARTIR IGUAL"},
 u"f16": {u"a":8, u"b":3, u"modo":u"blocos", u"imgA":u"fe_cenoura", u"imgB":u"fe_tomate",
          u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
          u"enun":u"Quantas <b>cenouras a mais</b> que tomates?", u"voz":u"Quantas cenouras a mais que tomates?"},
 u"f19": {u"a":10, u"b":6, u"modo":u"blocos", u"imgA":u"fe_maca", u"imgB":u"fe_maca",
          u"pergunta":u"menos", u"semSinal":True, u"selo":u"QUANTAS A MENOS?",
          u"enun":u"Quantas maçãs a <b>segunda</b> banca tem a menos?", u"voz":u"Quantas maçãs a segunda banca tem a menos?"},
 u"f26": {u"a":13, u"b":9, u"modo":u"blocos", u"imgA":u"fe_maca", u"imgB":u"fe_manga",
          u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
          u"enun":u"Quantas <b>maçãs a mais</b> que mangas?", u"voz":u"Quantas maçãs a mais que mangas?"},
 u"f05": {u"p":3, u"ate":18, u"dic":u"De 3 em 3: 3, 6, 9, 12, 15, 18."},
 u"f31": {u"p":2, u"ate":20, u"dic":u"De 2 em 2 até 20."},
 u"f22": {u"n":11, u"max":30, u"ini":15, u"qa":9, u"cls":u"gude", u"seed":63, u"ancora":1,
          u"selo":u"O POTE DE BOLINHAS", u"coisa":u"bolinhas", u"voz":u"bolinhas", u"atalhos":[5,10,20]},
 u"f32": {u"n":27, u"max":40, u"ini":20, u"qa":24, u"cls":u"grao", u"seed":88, u"ancora":1,
          u"selo":u"O SACO DA SOBRA", u"coisa":u"grãos", u"voz":u"grãos", u"atalhos":[10,20,30]},
}
# 4ª rodada em algumas fases, para fechar o piso de 40 min
_R4 = {
 u"f02": esc(u"fe_banana", u"Há <b>7</b> bananas numa penca e <b>5</b> em outra. Juntando, quantas?",
             12, [11,13,10], [u"Comece nas 7 e some 5.", u"7... 8, 9, 10, 11, 12.", u"São <b>12</b>. Toque para seguir."]),
 u"f06": esc(u"fe_uva", u"Tinha <b>9</b> uvas e ganhou mais <b>6</b>. Quantas agora?",
             15, [14,16,13], [u"Comece do 9 e some 6.", u"9... 10, 11, 12, 13, 14, 15.", u"São <b>15</b>. Toque para seguir."]),
 u"f09": esc(u"fe_tomate", u"Tinha <b>12</b> tomates e separou <b>8</b>. Quantos sobraram?",
             4, [5,3,6], [u"Comece do 12 e volte 8.", u"12... até 4.", u"Sobraram <b>4</b>. Toque para seguir."]),
 u"f14": esc(u"fe_maca", u"Tinha <b>13</b> maçãs e vendeu <b>6</b>. Quantas restaram?",
             7, [6,8,19], [u"Comece do 13 e volte 6.", u"13... 12, 11, 10, 9, 8, 7.", u"Restaram <b>7</b>. Toque para seguir."]),
 u"f21": esc(u"fe_laranja", u"Há <b>14</b> laranjas e <b>6</b> mangas. Quantas laranjas a mais?",
             8, [7,9,20], [u"Case cada manga com uma laranja.", u"De 6 até 14: são 8.", u"São <b>8</b> a mais. Toque para seguir."]),
 u"f16": {u"a":9, u"b":6, u"modo":u"blocos", u"imgA":u"fe_cenoura", u"imgB":u"fe_tomate",
          u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
          u"enun":u"Quantas <b>cenouras a mais</b> que tomates?", u"voz":u"Quantas cenouras a mais que tomates?"},
 u"f19": {u"a":11, u"b":7, u"modo":u"blocos", u"imgA":u"fe_uva", u"imgB":u"fe_uva",
          u"pergunta":u"menos", u"semSinal":True, u"selo":u"QUANTAS A MENOS?",
          u"enun":u"Quantos cachos a <b>segunda</b> banca tem a menos?", u"voz":u"Quantos cachos a segunda banca tem a menos?"},
 u"f17": esc(u"fe_pao", u"Havia <b>16</b> pães e vendeu <b>7</b>. Quantos sobraram?",
             9, [8,10,23], [u"Comece do 16 e volte 7.", u"16... até 9.", u"Sobraram <b>9</b>. Toque para seguir."]),
 u"f26": {u"a":14, u"b":8, u"modo":u"blocos", u"imgA":u"fe_maca", u"imgB":u"fe_manga",
          u"pergunta":u"mais", u"semSinal":True, u"selo":u"QUANTAS A MAIS?",
          u"enun":u"Quantas <b>maçãs a mais</b> que mangas?", u"voz":u"Quantas maçãs a mais que mangas?"},
 u"f30": {u"p":u"“Tinha 8 e <b>ganhou 7</b>.” Que conta acha quanto tem agora?",
          u"c":{u"t":u"8 + 7", u"voz":u"oito mais sete"},
          u"e":[{u"t":u"8 − 7", u"voz":u"oito menos sete"}, {u"t":u"7 − 7", u"voz":u"sete menos sete"}],
          u"d":[u"Ela GANHOU: ficou com mais.", u"Ganhar pede o sinal de mais.", u"É <b>8 + 7</b>. Toque para seguir."]},
 u"f28": {u"img":u"fe_banana", u"ante":u"15 bananas em duas pencas. Numa há 6, na outra há ", u"dep":u".",
          u"cer":u"9", u"out":[u"8", u"10"], u"dic":u"De 6 até 15: são 9."},
}
# 4ª régua nas retas + folga p/ passar o piso com margem
_R5 = {
 u"f03": reta(u"4 + 5", 0,10,9, [0,5,10],[4,9],[1,2,3,6,7,8],
              u"Comece no <b>4</b> e ande <b>5</b>. Onde você chega?", u"A partir do 4: 5, 6, 7, 8, 9."),
 u"f12": reta(u"13 − 6", 0,15,7, [0,5,10,15],[7,13],[2,4,6,8,9,11,12,14],
              u"Comece no <b>13</b> e volte <b>6</b>. Onde você chega?", u"Para trás do 13: 12, 11, 10, 9, 8, 7."),
 u"f18": reta(u"16 − 4", 0,20,12, [0,5,10,15,20],[12,16],[2,4,6,8,14,18],
              u"Comece no <b>16</b> e volte <b>4</b>. Onde você chega?", u"Para trás do 16: 15, 14, 13, 12."),
 u"f25": reta(u"17 − 8", 0,20,9, [0,5,10,15,20],[9,17],[2,4,6,11,13,16,18],
              u"Comece no <b>17</b> e volte <b>8</b>. Onde você chega?", u"Para trás do 17: até 9."),
}
for _f in CONTEUDO[u"fases"]:
    _add = _R3.get(_f[u"id"])
    if _add is not None:
        _f[u"dados"].append(_add)
    _a4 = _R4.get(_f[u"id"])
    if _a4 is not None:
        _f[u"dados"].append(_a4)
    _a5 = _R5.get(_f[u"id"])
    if _a5 is not None:
        _f[u"dados"].append(_a5)
# aquecimento: +2 pares (fica com 8)
for _f in CONTEUDO[u"fases"]:
    if _f[u"id"] == u"aquecimento":
        _f[u"dados"] += [
          {u"k":u"c", u"img":u"fe_cenoura", u"imgsen":u"fe_cenoura", u"voz":u"cenoura", u"vozsen":u"cenoura"},
          {u"k":u"p", u"img":u"fe_manga", u"imgsen":u"fe_manga", u"voz":u"manga", u"vozsen":u"manga"}]

# ==================================================================
# VOZ das opcoes-numero do COMPLETAR: digito puro nao tem alto-falante
# (portao 0n). Converte "3" -> {t:"3", voz:"tres"} para o VOZOK falar o
# numero por extenso (as vozes ja existem do escolher). cer e out.
# ==================================================================
def _numvoz(x):
    # completar so aceita string em cer/out; opcao-numero vira PALAVRA (padrao da
    # casa: opcao de completar e palavra, vozeada). O digito fica no enunciado.
    if isinstance(x, str) and x.isdigit():
        return _EXT.get(int(x), x)
    return x

# ==================================================================
# RETA-NUMERICA = SITUAÇÃO-PROBLEMA DA FEIRA (pedido do Marcos, ago/2026):
# a rua da feira tem bancas numeradas; a Dona Coruja CAMINHA (juntar) ou VOLTA
# (separar/retirar) bancas. A reta deixa de ser "ande 3" abstrato e vira uma
# historinha do cotidiano — a régua é a ESTRATÉGIA para resolver o problema.
# A operação de cada rodada é lida do `selo` atual ("5 + 3" / "12 − 5").
# ==================================================================
import re as _re
def _reta_historia(a, b, frente):
    if frente:
        bal = (u"A Dona Coruja está na banca <b>%d</b> e caminha <b>%d</b> bancas "
               u"para a frente, entregando frutas. Em que banca ela chega?" % (a, b))
        passos = u", ".join(str(x) for x in range(a+1, a+b+1))
        dica = u"Ande com o dedo pelas bancas: %s." % passos
    else:
        bal = (u"A Dona Coruja está na banca <b>%d</b> e volta <b>%d</b> bancas "
               u"para buscar o troco. Em que banca ela para?" % (a, b))
        passos = u", ".join(str(x) for x in range(a-1, a-b-1, -1))
        dica = u"Volte com o dedo pelas bancas: %s." % passos
    return bal, dica

for _f in CONTEUDO[u"fases"]:
    if _f.get(u"mec") != u"reta-numerica":
        continue
    _f[u"selo"] = u"A RUA DA FEIRA"
    _primeiro = None
    for _r in _f[u"dados"]:
        _m = _re.match(r"\s*(\d+)\s*([+−-])\s*(\d+)", _r.get(u"selo", u""))
        if not _m:
            continue
        _a = int(_m.group(1)); _op = _m.group(2); _bb = int(_m.group(3))
        _frente = (_op == u"+")
        _r[u"selo"] = u"A RUA DA FEIRA"
        _r[u"bal"], _r[u"dica"] = _reta_historia(_a, _bb, _frente)
        if _primeiro is None:
            _primeiro = (_a, _bb, _frente)
    if _primeiro:
        _a, _bb, _frente = _primeiro
        if _frente:
            _f[u"enunciado"] = (u"A Dona Coruja está na banca <b>%d</b> e caminha "
                u"<b>%d</b> bancas para a frente. Ajude a achar onde ela chega." % (_a, _bb))
        else:
            _f[u"enunciado"] = (u"A Dona Coruja está na banca <b>%d</b> e volta "
                u"<b>%d</b> bancas. Ajude a achar onde ela para." % (_a, _bb))
        _f[u"dica"] = u"Ponha o dedo na banca e ande de uma em uma, contando."
for _f in CONTEUDO[u"fases"]:
    if _f.get(u"mec") == u"completar":
        for _r in _f.get(u"dados", []):
            if u"cer" in _r:
                _r[u"cer"] = _numvoz(_r[u"cer"])
            if u"out" in _r:
                _r[u"out"] = [_numvoz(x) for x in _r[u"out"]]

# ------------------------------------------------------------------
if __name__ == "__main__":
    out = os.path.join(PASTA, u"conteudo.json")
    io.open(out, "w", encoding="utf-8").write(
        json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
    print(u"fases:", len(CONTEUDO[u"fases"]), u"->", out)
