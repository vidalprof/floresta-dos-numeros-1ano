# -*- coding: utf-8 -*-
u"""Gera _detetive/conteudo.json — A AGÊNCIA DOS DETETIVES DAS PALAVRAS (5º ano, Português).

REVISÃO / REFORÇO de assuntos já estudados (pedido do Marcos):
  · PRONOMES (pessoais, possessivos, demonstrativos, de tratamento);
  · INTERPRETAÇÃO de textos NARRATIVOS (quem, o quê, quando, sequência, causa);
  · INTERPRETAÇÃO de textos INJUNTIVOS (finalidade, passos, verbos de comando);
  · MAU (com U = adjetivo, o contrário de BOM) × MAL (com L = advérbio, o
    contrário de BEM).

ENREDO (o "porquê" — EDUVERSE): a criança é um(a) DETETIVE JÚNIOR da agência da
raposa Vera. Cada caso só se resolve LENDO o texto e usando as palavras certas —
o problema vem ANTES do conceito; a gramática é ferramenta do detetive, nunca
prova. Fecho com gancho (um novo caso na caixa de correio).

PIPELINE (padrão ESQUELETO — vale para QUALQUER atividade; ver CLAUDE.md):
  1) este build_conteudo.py escreve conteudo.json (CONTEUDO + fases DADO);
  2) python3 _padrao/ESQUELETO/integrar.py --escrever  (compila as peças);
  3) python3 _padrao/ESQUELETO/montar.py _detetive      (gera index.html,
     falas.json, arte.json, sw.js — o motor blindado já vem embutido);
  4) gerar a ARTE (o Marcos gera pelos prompts; o Claude consulta o _banco antes
     e só pede o que faltar — REGRA DO BANCO, CLAUDE.md);
  5) bancada (bash _qa/auditar.sh) + revisor + publicar por entregar.yml.

⚠️ REGRA DO BANCO (nova, ago/2026): antes de pedir arte, CONSULTAR o _banco
   (o montador reporta no_banco × gerar); reusar o que existe; o que faltar, o
   Marcos gera pelos prompts abaixo. Mascote/cenário/medalha desta atividade são
   NOVOS (o Marcos autorizou gerar).
"""
import io, json, os

PASTA = os.path.dirname(os.path.abspath(__file__))

# ---- BNCC 5º ano (revisão) — habilidades-âncora do parecer do professor ----
HAB = (u"Reconhecer e usar pronomes (pessoais, possessivos, demonstrativos e de "
       u"tratamento) na coesão do texto; localizar informações e inferir sentidos "
       u"em textos narrativos e injuntivos; e empregar corretamente MAU/MAL "
       u"conforme a classe (adjetivo × advérbio). EF05LP a EF35LP (revisão).")

CONTEUDO = {
 u"titulo": u"A Agência dos Detetives das Palavras",
 u"sub": u"Português · 5º ano · Pronomes, interpretação (narrativo/injuntivo), mau × mal",
 u"ano": u"5º ano",
 u"prefixo": u"dp",
 u"mascote": u"raposa",
 u"mascoteNome": u"Detetive Vera",
 u"crachas": 6,
 # quem planejou (até o 5º ano manda o PEDAGOGO; ver _padrao/RECEITA.md)
 u"mesa": u"Pedagogo do 5º ano + especialista em Língua Portuguesa (revisão de reforço).",
 u"fundo": u"dp_fundo",
 u"voz": u"feminina",
 u"abertura": (u"Bem-vindo(a) à Agência! Sou a detetive Vera. Cada caso só se "
               u"resolve LENDO com atenção e usando as palavras certas. Vamos?"),
 u"fim": u"Caso encerrado, detetive! Você lê como quem enxerga o que os outros não veem.",
 # os rótulos que o RELATÓRIO do professor mostra (conceito -> nome de criança)
 u"conceitos": {
   u"objetivo1": u"Pronomes (pessoais, possessivos, demonstrativos, tratamento)",
   u"objetivo2": u"Interpretar texto narrativo (quem, o quê, sequência)",
   u"objetivo3": u"Interpretar texto injuntivo (finalidade e passos)",
   u"objetivo4": u"Mau (adjetivo) × Mal (advérbio)",
 },
 # curriculo = mapa conceito -> habilidade BNCC (o montador confere que cada
 # objetivo diz QUE habilidade trabalha; é o que vai ao parecer do professor).
 u"curriculo": {
   u"objetivo1": u"Reconhecer e usar pronomes (pessoais, possessivos, demonstrativos, de tratamento) na coesão do texto. EF05LP (revisão).",
   u"objetivo2": u"Localizar informações explícitas e inferir sentidos em textos NARRATIVOS. EF35LP03/EF05LP (revisão).",
   u"objetivo3": u"Identificar finalidade e ordenar passos em textos INJUNTIVOS (receita, regras). EF05LP (revisão).",
   u"objetivo4": u"Empregar corretamente MAU (adjetivo, = bom) e MAL (advérbio, = bem). EF05LP (revisão).",
 },
 u"fases": [],   # <- preenchido pelos blocos abaixo (em construção)
}

# ============================================================
#  PLANO DE FASES (o roteiro — variedade de gestos, ~4 blocos)
#  Cada fase é DADO; ~2–3 rodadas para encher a aula sem arte nova.
#  Gestos previstos (leque grande, nenhum > 40%): escolher, ligar,
#  classificar, completar, ordenar, quem-sou-eu, caca-palavras, intruso,
#  memoria, digitar/forca.
#
#  BLOCO 1 — PRONOMES (objetivo1)
#   f01 escolher     — qual pronome substitui o nome grifado
#   f02 ligar        — pronome ↔ palavra que ele substitui
#   f03 classificar  — gavetas: pessoal / possessivo / demonstrativo / tratamento
#   f04 completar    — preencher a lacuna com o pronome certo (coesão)
#   f05 caca-palavras— achar pronomes escondidos
#
#  BLOCO 2 — TEXTO NARRATIVO (objetivo2)
#   f06 (texto curto) escolher — quem/o quê/quando
#   f07 ordenar      — pôr os fatos na ordem em que aconteceram
#   f08 quem-sou-eu  — descobrir o personagem pelas pistas do texto
#   f09 escolher     — inferência (por que o personagem fez X)
#
#  BLOCO 3 — TEXTO INJUNTIVO (objetivo3)  [receita / regras / manual]
#   f10 escolher     — qual a FINALIDADE do texto (para que serve)
#   f11 ordenar      — pôr os PASSOS na ordem certa
#   f12 intruso      — qual frase NÃO é uma instrução (verbo de comando)
#   f13 completar    — completar o passo com o verbo no imperativo
#
#  BLOCO 4 — MAU × MAL (objetivo4)
#   f14 escolher     — mau ou mal na frase (troca por bom/bem para decidir)
#   f15 classificar  — gavetas MAU (adjetivo, = bom) / MAL (advérbio, = bem)
#   f16 completar    — preencher com mau/mal
#   f17 digitar/forca— escrever mau/mal certo
#   AQUECIMENTO      — revisão espaçada no meio (mistura pronome + mau/mal)
#
#  FIM: boletim animado + relatório do professor (FIM-DE-ATIVIDADE.md) +
#       gancho (um novo caso na caixa de correio).
# ============================================================

fases = []
def add(**k): fases.append(k)

def esc(p, c, e, d):
    u"""escolher só de texto (gramática): sem imagem."""
    return {u"img":u"", u"p":p, u"c":c, u"e":e, u"d":d}

# ============================================================
# BLOCO 1 — PRONOMES (objetivo1)
# ============================================================

# f01 — ESCOLHER: qual pronome PESSOAL substitui o nome
add(id=u"f01", mec=u"escolher", selo=u"CASO 1: O PRONOME CERTO", conceito=u"objetivo1",
    enunciado=u"Leia a pista e escolha o <b>pronome</b> que substitui a palavra grifada.",
    dica=u"Pronome pessoal troca o nome: ele, ela, nós, eles...",
    dados=[
      esc(u"<b>Ana</b> achou a pista. ___ sorriu.", u"ELA", [u"ELE", u"NÓS"],
          [u"Ana é uma menina, no singular.", u"Uma pessoa, feminino: qual serve?",
           u"É <b>ELA</b>. Toque para seguir."]),
      esc(u"<b>Os detetives</b> voltaram. ___ resolveram o caso.", u"ELES", [u"ELE", u"ELA"],
          [u"São vários, no masculino.", u"Vários homens: plural masculino.",
           u"É <b>ELES</b>. Toque para seguir."]),
      esc(u"<b>Eu e você</b> vamos investigar. ___ formamos a dupla.", u"NÓS", [u"ELES", u"VOCÊS"],
          [u"Eu + você = a gente, juntos.", u"Quem inclui quem fala: nós.",
           u"É <b>NÓS</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"O PRONOME CERTO", u"FECHO":u"Você trocou os nomes pelos pronomes certos!"})

# f02 — LIGAR: pronome <-> a palavra que ele substitui
add(id=u"f02", mec=u"ligar", selo=u"CASO 1: LIGUE AS PISTAS", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>pronome</b> à palavra que ele substitui.",
    dica=u"Veja o número (singular/plural) e o gênero (masculino/feminino).",
    dados=[{u"k":u"p0", u"t":u"ELA", u"s":u"a menina"},
           {u"k":u"p1", u"t":u"ELE", u"s":u"o cachorro"},
           {u"k":u"p2", u"t":u"ELES", u"s":u"os meninos"},
           {u"k":u"p3", u"t":u"NÓS", u"s":u"eu e você"}],
    dadosExtra={u"DICAS":[u"Pense em quantos são e se é menino ou menina.",
                          u"ELA = uma menina; ELES = vários; NÓS = eu + você.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS":[], u"ENUN":u"Ligue o pronome à palavra que ele substitui.",
                u"FECHO":u"Cada pronome no lugar certo!"})

# f03 — CLASSIFICAR: os TIPOS de pronome (gavetas)
add(id=u"f03", mec=u"classificar", selo=u"CASO 1: SEPARE OS PRONOMES", conceito=u"objetivo1",
    enunciado=u"Cada <b>pronome</b> na sua gaveta: pessoal, possessivo ou demonstrativo?",
    dica=u"Pessoal = quem fala/ouve (eu, tu, ele); possessivo = de quem é (meu, teu); demonstrativo = onde está (este, esse, aquele).",
    dados=[{u"k":u"pes", u"n":u"PESSOAL", u"img":u"", u"voz":u"pessoal", u"rot":False},
           {u"k":u"pos", u"n":u"POSSESSIVO", u"img":u"", u"voz":u"possessivo", u"rot":False},
           {u"k":u"dem", u"n":u"DEMONSTRATIVO", u"img":u"", u"voz":u"demonstrativo", u"rot":False}],
    dadosExtra={u"FICHAS":[
      {u"t":u"EU", u"alvo":u"pes"}, {u"t":u"ELE", u"alvo":u"pes"},
      {u"t":u"MEU", u"alvo":u"pos"}, {u"t":u"NOSSO", u"alvo":u"pos"},
      {u"t":u"ESTE", u"alvo":u"dem"}, {u"t":u"AQUELE", u"alvo":u"dem"}],
      u"DICAS":[u"EU e ELE dizem QUEM; MEU e NOSSO dizem DE QUEM; ESTE e AQUELE dizem ONDE.",
                u"Possessivo combina com 'é meu, é nosso'. Demonstrativo com 'este aqui, aquele lá'.",
                u"Olhe a gaveta com a borda amarela: é ali que esta ficha mora."],
      u"ENUN":u"Toque no <b>pronome</b>. Depois toque na <b>gaveta do tipo</b> dele."})

# f04 — COMPLETAR: o pronome que dá coesão à frase
add(id=u"f04", mec=u"completar", selo=u"CASO 1: COMPLETE A PISTA", conceito=u"objetivo1",
    enunciado=u"Preencha a frase com o <b>pronome</b> que falta.",
    dica=u"O pronome tem que combinar com a palavra que ele substitui.",
    dados=[{u"img":u"", u"ante":u"Cadê o meu caderno? ", u"dep":u" está na mochila.",
            u"cer":u"Ele", u"out":[u"Ela", u"Eles"], u"dic":u"Caderno é 'o' — masculino, singular."},
           {u"img":u"", u"ante":u"As lupas são novas. ", u"dep":u" brilham.",
            u"cer":u"Elas", u"out":[u"Ele", u"Eles"], u"dic":u"Lupas são 'as' — feminino, plural."},
           {u"img":u"", u"ante":u"Esta é a casa de vocês? Sim, ", u"dep":u" é nossa.",
            u"cer":u"ela", u"out":[u"ele", u"eles"], u"dic":u"Casa é 'a' — feminino, singular."}],
    dadosExtra={u"ENUN":u"Toque no pedaço que <b>falta</b> na frase.",
                u"DEPOIS":u"Leia a frase inteira antes de escolher.",
                u"FECHO":u"Você completou as pistas com os pronomes!"})

# f05 — CAÇA-PALAVRAS: achar pronomes escondidos
add(id=u"f05", mec=u"caca-palavras", selo=u"CASO 1: PRONOMES ESCONDIDOS", conceito=u"objetivo1",
    enunciado=u"Ache os <b>pronomes</b> escondidos no quadro.",
    dica=u"Estão deitados (→) e em pé (↓): EU, ELE, ELA, MEU, ESTE.",
    dados=[u"EU", u"ELE", u"ELA", u"MEU", u"ESTE"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"PRONOMES ESCONDIDOS",
                u"LETRAS":u"ABCDEHILMNOPRSTU", u"DIFICIL":u"",
                u"CORP":[u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
# BLOCO 2 — INTERPRETAÇÃO: TEXTO NARRATIVO (objetivo2)
# ============================================================

# f06 — ESCOLHER: quem/o quê (texto curto embutido na pergunta)
add(id=u"f06", mec=u"escolher", selo=u"CASO 2: O QUE O TEXTO CONTA", conceito=u"objetivo2",
    enunciado=u"Leia com atenção de detetive e responda o que o texto conta.",
    dica=u"A resposta está NO texto. Volte e leia de novo se precisar.",
    dados=[
      esc(u"Leia: <i>“Bidu, o gato, subiu no telhado atrás de um pássaro e ficou preso.”</i> Quem ficou preso?",
          u"O gato Bidu", [u"O pássaro", u"O telhado"],
          [u"Quem é o personagem que subiu?", u"O texto diz que <b>Bidu</b> ficou preso.",
           u"É <b>o gato Bidu</b>. Toque para seguir."]),
      esc(u"Leia a mesma cena: por que Bidu subiu no telhado?",
          u"Atrás de um pássaro", [u"Para dormir", u"Fugindo da chuva"],
          [u"Procure o motivo no texto.", u"Ele subiu <b>atrás de um pássaro</b>.",
           u"É <b>atrás de um pássaro</b>. Toque para seguir."]),
      esc(u"Leia: <i>“De manhã, os bombeiros resgataram o gato do telhado.”</i> Quando o gato foi resgatado?",
          u"De manhã", [u"À noite", u"Na hora do almoço"],
          [u"Procure a palavra de TEMPO no texto.", u"O texto começa com <b>De manhã</b>.",
           u"É <b>de manhã</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"O QUE O TEXTO CONTA", u"FECHO":u"Você achou as informações no texto!"})

# f07 — LINHA DO TEMPO: pôr os fatos na ordem em que aconteceram
add(id=u"f07", mec=u"linha-do-tempo", selo=u"CASO 2: A ORDEM DOS FATOS", conceito=u"objetivo2",
    enunciado=u"Coloque os fatos da história na <b>ordem</b> em que aconteceram.",
    dica=u"Pense: o que veio primeiro? O que aconteceu por último?",
    dados=[{u"t":1, u"n":u"O menino perdeu o cachorro no parque."},
           {u"t":2, u"n":u"A detetive Vera achou pegadas na lama."},
           {u"t":3, u"n":u"As pegadas levaram at&#233; uma &#225;rvore."},
           {u"t":4, u"n":u"O cachorro estava l&#225;, assustado."},
           {u"t":5, u"n":u"O menino abra&#231;ou o cachorro, feliz."}])

# f08 — QUEM SOU EU: descobrir o personagem pelas pistas
add(id=u"f08", mec=u"quem-sou-eu", selo=u"CASO 2: QUEM É O PERSONAGEM?", conceito=u"objetivo2",
    enunciado=u"Ouça as pistas do texto e descubra <b>quem é o personagem</b>.",
    dica=u"Junte as três pistas antes de responder.",
    dados=[
      {u"resp":u"O CARTEIRO", u"pistas":[
         u"Eu levo <b>cartas</b> de casa em casa.",
         u"Uso um <b>bon&#233;</b> e uma bolsa grande a tiracolo.",
         u"Fui eu que trouxe a <b>carta misteriosa</b> para a agência."],
       u"outros":[u"O PADEIRO", u"O M&#201;DICO", u"O PROFESSOR"]},
      {u"resp":u"A VIZINHA", u"pistas":[
         u"Eu moro na casa <b>ao lado</b> da agência.",
         u"Estou sempre na <b>janela</b>, vendo tudo o que passa.",
         u"Eu <b>vi</b> quem deixou a carta na porta."],
       u"outros":[u"A PROFESSORA", u"A M&#195;E", u"A DELEGADA"]},
    ])

# f09 — ESCOLHER: inferência (o que dá para concluir)
add(id=u"f09", mec=u"escolher", selo=u"CASO 2: LENDO NAS ENTRELINHAS", conceito=u"objetivo2",
    enunciado=u"Às vezes o texto não diz tudo: descubra pela pista.",
    dica=u"O texto não fala direto, mas dá para concluir pelo que conta.",
    dados=[
      esc(u"Leia: <i>“Ana pegou o guarda-chuva e as botas antes de sair.”</i> Como estava o tempo?",
          u"Estava chovendo", [u"Estava um sol quente", u"Estava nevando"],
          [u"Por que alguém pega guarda-chuva e botas?", u"Guarda-chuva + botas = <b>chuva</b>.",
           u"É <b>estava chovendo</b>. Toque para seguir."]),
      esc(u"Leia: <i>“O prato estava vazio e o gato lambia os bigodes.”</i> O que aconteceu?",
          u"O gato comeu a comida", [u"O gato dormiu", u"O gato fugiu"],
          [u"Prato vazio + gato lambendo os bigodes...", u"Ele <b>comeu</b> tudo.",
           u"É <b>o gato comeu a comida</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"LENDO NAS ENTRELINHAS", u"FECHO":u"Você leu até o que estava escondido!"})

# AQUECIMENTO — revisão espaçada NO MEIO (~50%): revê PRONOMES (já treinados) por
# um gesto diferente (ligar), quebrando a sequência de 'escolher'.
add(id=u"aquecimento", mec=u"ligar", selo=u"AQUECIMENTO DO DETETIVE", conceito=u"objetivo1",
    enunciado=u"<b>Aquecimento!</b> Ligue cada <b>pronome</b> à palavra que ele substitui.",
    dica=u"Revisão rápida: veja número (singular/plural) e gênero.",
    dados=[{u"k":u"p0", u"t":u"ELE", u"s":u"o carteiro"},
           {u"k":u"p1", u"t":u"ELA", u"s":u"a vizinha"},
           {u"k":u"p2", u"t":u"ELES", u"s":u"os detetives"},
           {u"k":u"p3", u"t":u"NÓS", u"s":u"eu e a Vera"}],
    dadosExtra={u"DICAS":[u"Quantos são? Menino ou menina?",
                          u"ELE = um; ELA = uma; ELES = vários; NÓS = eu + você.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS":[], u"ENUN":u"Ligue o pronome à palavra que ele substitui.",
                u"FECHO":u"Aquecido! Agora os últimos casos."})

# ============================================================
# BLOCO 3 — INTERPRETAÇÃO: TEXTO INJUNTIVO (receita / instruções)
# ============================================================

# f10 — ESCOLHER: qual a FINALIDADE do texto
add(id=u"f10", mec=u"escolher", selo=u"CASO 3: PARA QUE SERVE?", conceito=u"objetivo3",
    enunciado=u"O texto injuntivo <b>ensina a fazer</b> algo. Descubra para que ele serve.",
    dica=u"Texto injuntivo dá ordens/instruções: receita, regra de jogo, manual.",
    dados=[
      esc(u"Leia: <i>“Misture a farinha, quebre os ovos e leve ao forno por 30 minutos.”</i> Este texto serve para...",
          u"Ensinar a fazer um bolo", [u"Contar uma história", u"Descrever um lugar"],
          [u"Ele manda FAZER passos, um atrás do outro.", u"Farinha + ovos + forno = uma <b>receita</b>.",
           u"É <b>ensinar a fazer um bolo</b>. Toque para seguir."]),
      esc(u"Leia: <i>“Não corra. Aperte o botão. Espere a luz verde para atravessar.”</i> Este texto serve para...",
          u"Ensinar a atravessar com segurança", [u"Vender um carro", u"Contar uma piada"],
          [u"São ordens para você fazer certo.", u"Botão + luz verde = <b>atravessar a rua</b>.",
           u"É <b>ensinar a atravessar com segurança</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"PARA QUE SERVE?", u"FECHO":u"Você descobriu a finalidade dos textos!"})

# f11 — LINHA DO TEMPO: pôr os PASSOS na ordem certa
add(id=u"f11", mec=u"linha-do-tempo", selo=u"CASO 3: A ORDEM DOS PASSOS", conceito=u"objetivo3",
    enunciado=u"Coloque os <b>passos</b> da receita na ordem certa.",
    dica=u"O que se faz primeiro? Não dá para assar antes de misturar.",
    dados=[{u"t":1, u"n":u"Separe os ingredientes."},
           {u"t":2, u"n":u"Misture a farinha e os ovos."},
           {u"t":3, u"n":u"Bata bem a massa."},
           {u"t":4, u"n":u"Leve ao forno."},
           {u"t":5, u"n":u"Espere esfriar e sirva."}])

# f12 — INTRUSO: qual frase NÃO é uma instrução (não tem verbo de comando)
add(id=u"f12", mec=u"intruso", selo=u"CASO 3: A FRASE INTRUSA", conceito=u"objetivo3",
    enunciado=u"Três frases dão <b>ordens</b>. <b>Qual NÃO é uma instrução?</b>",
    dica=u"Instrução manda fazer (verbo de comando): misture, corte, ligue.",
    dados=[
      {u"selo":u"AS INSTRUÇÕES", u"tipo":u"texto",
       u"enun":u"Três frases mandam fazer algo. <b>Qual NÃO manda?</b>",
       u"itens":[{u"k":u"a", u"n":u"MISTURE OS OVOS"}, {u"k":u"b", u"n":u"CORTE O PAPEL"},
                 {u"k":u"c", u"n":u"LIGUE A LUZ"}, {u"k":u"d", u"n":u"O BOLO É GOSTOSO"}],
       u"fora":u"d", u"nomeFora":u"O BOLO É GOSTOSO",
       u"d1":u"Qual frase NÃO manda você fazer nada?",
       u"d2":u"Misture, corte, ligue são ORDENS. Uma só conta uma coisa.",
       u"d3":u"A de fora é <b>O BOLO É GOSTOSO</b>: ela apenas afirma, não manda fazer.",
       u"razoes":[{u"t":u"As outras mandam fazer (verbo de comando); esta só afirma.", u"ok":1},
                  {u"t":u"Porque ela fala de bolo.", u"ok":0},
                  {u"t":u"Porque ela é a mais curta.", u"ok":0},
                  {u"t":u"Porque ela tem a letra O.", u"ok":0}],
       u"enunPorque":u"O que <b>O BOLO É GOSTOSO</b> faz de diferente das outras três? Toque na razão certa.",
       u"p1":u"Pode ser verdade, mas olhe o que as OUTRAS três fazem.",
       u"p2":u"As outras começam com um verbo que MANDA: misture, corte, ligue.",
       u"p3":u"“O bolo é gostoso” só AFIRMA; as outras dão ORDEM — por isso ela é a diferente.",
       u"regra":u"instrução manda fazer (verbo de comando); afirmação só conta"},
    ])

# f13 — COMPLETAR: o verbo de comando (imperativo) que falta
add(id=u"f13", mec=u"completar", selo=u"CASO 3: COMPLETE A INSTRUÇÃO", conceito=u"objetivo3",
    enunciado=u"Preencha a instrução com o <b>verbo de comando</b> certo.",
    dica=u"Verbo de comando manda fazer: misture, aperte, espere.",
    dados=[{u"img":u"", u"ante":u"Para o bolo crescer, ", u"dep":u" bem a massa.",
            u"cer":u"bata", u"out":[u"batia", u"batendo"], u"dic":u"Uma ORDEM curta e direta: 'bata!'"},
           {u"img":u"", u"ante":u"Antes de atravessar, ", u"dep":u" a luz verde.",
            u"cer":u"espere", u"out":[u"esperava", u"esperando"], u"dic":u"Comando: 'espere!'"},
           {u"img":u"", u"ante":u"Para acender, ", u"dep":u" o botão.",
            u"cer":u"aperte", u"out":[u"apertava", u"apertei"], u"dic":u"Comando direto: 'aperte!'"}],
    dadosExtra={u"ENUN":u"Toque no pedaço que <b>falta</b> na instrução.",
                u"DEPOIS":u"Leia a instrução inteira antes de escolher.",
                u"FECHO":u"Você completou as instruções!"})

# ============================================================
# BLOCO 4 — MAU (adjetivo) × MAL (advérbio)
# ============================================================

# f14 — ESCOLHER: mau ou mal? (trocar por bom/bem para decidir)
add(id=u"f14", mec=u"escolher", selo=u"CASO 4: MAU OU MAL?", conceito=u"objetivo4",
    enunciado=u"Truque de detetive: se trocar por <b>BOM</b>, é MAU; se trocar por <b>BEM</b>, é MAL.",
    dica=u"MAU (com U) = adjetivo, o contrário de BOM. MAL (com L) = advérbio, o contrário de BEM.",
    dados=[
      esc(u"O lobo da história era um lobo ___ . (troque por BOM/BEM para decidir)",
          u"MAU", [u"MAL"],
          [u"Cabe 'bom' ou 'bem'? 'Um lobo BOM' faz sentido.", u"Combina com BOM = <b>MAU</b> (adjetivo).",
           u"É <b>MAU</b> (o contrário de bom). Toque para seguir."]),
      esc(u"Ele dormiu ___ e acordou cansado. (troque por BOM/BEM)",
          u"MAL", [u"MAU"],
          [u"Cabe 'bom' ou 'bem'? 'Dormiu BEM' faz sentido.", u"Combina com BEM = <b>MAL</b> (advérbio).",
           u"É <b>MAL</b> (o contrário de bem). Toque para seguir."]),
      esc(u"Que cheiro ___ ! (troque por BOM/BEM)",
          u"MAU", [u"MAL"],
          [u"'Que cheiro BOM!' faz sentido.", u"Combina com BOM = <b>MAU</b>.",
           u"É <b>MAU</b> (o contrário de bom). Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"MAU OU MAL?", u"FECHO":u"Você desvendou o mau e o mal!"})

# f15 — CLASSIFICAR: gavetas MAU (=bom) / MAL (=bem)
add(id=u"f15", mec=u"classificar", selo=u"CASO 4: SEPARE MAU E MAL", conceito=u"objetivo4",
    enunciado=u"Cada palavra na gaveta certa: <b>MAU</b> (= bom) ou <b>MAL</b> (= bem)?",
    dica=u"Se dá para trocar por BOM, vai em MAU. Se dá para trocar por BEM, vai em MAL.",
    dados=[{u"k":u"mau", u"n":u"MAU<br>(= bom)", u"img":u"", u"voz":u"mau", u"rot":False},
           {u"k":u"mal", u"n":u"MAL<br>(= bem)", u"img":u"", u"voz":u"mal", u"rot":False}],
    dadosExtra={u"FICHAS":[
      {u"t":u"um cão MAU", u"alvo":u"mau"}, {u"t":u"um dia MAU", u"alvo":u"mau"},
      {u"t":u"um filme MAU", u"alvo":u"mau"},
      {u"t":u"escreve MAL", u"alvo":u"mal"}, {u"t":u"passou MAL", u"alvo":u"mal"},
      {u"t":u"fez MAL a lição", u"alvo":u"mal"}],
      u"DICAS":[u"Troque por bom/bem: 'um cão BOM' → MAU; 'escreve BEM' → MAL.",
                u"MAU descreve uma COISA (adjetivo); MAL diz COMO se faz (advérbio).",
                u"Olhe a gaveta com a borda amarela: é ali que esta ficha mora."],
      u"ENUN":u"Toque na <b>ficha</b>. Depois toque na gaveta: <b>MAU</b> ou <b>MAL</b>?"})

# f16 — COMPLETAR: mau/mal na frase
add(id=u"f16", mec=u"completar", selo=u"CASO 4: COMPLETE COM MAU/MAL", conceito=u"objetivo4",
    enunciado=u"Preencha a frase com <b>mau</b> (com U) ou <b>mal</b> (com L).",
    dica=u"Troca-BOM = mau; troca-BEM = mal.",
    dados=[{u"img":u"", u"ante":u"Ele teve um ", u"dep":u" pensamento.",
            u"cer":u"mau", u"out":[u"mal"], u"dic":u"'Um BOM pensamento' → mau."},
           {u"img":u"", u"ante":u"A porta range porque foi ", u"dep":u" instalada.",
            u"cer":u"mal", u"out":[u"mau"], u"dic":u"'Foi BEM instalada' → mal."},
           {u"img":u"", u"ante":u"Não seja ", u"dep":u" com os colegas.",
            u"cer":u"mau", u"out":[u"mal"], u"dic":u"'Seja BOM' → mau."}],
    dadosExtra={u"ENUN":u"Toque no pedaço que <b>falta</b> na frase.",
                u"DEPOIS":u"Troque por bom/bem para conferir.",
                u"FECHO":u"Você nunca mais confunde mau e mal!"})

# f17 — DIGITAR: escrever mau/mal certo (fixa a grafia)
add(id=u"f17", mec=u"digitar", selo=u"CASO 4: ESCREVA CERTO", conceito=u"objetivo4",
    enunciado=u"Escreva a palavra certa, letra por letra.",
    dica=u"Diga a frase trocando por bom/bem e escolha U ou L no fim.",
    dados=[{u"palavra":u"MAU", u"img":u"", u"voz":u"mau",
            u"pista":u"O contrário de BOM (um lobo ___). Escreva com U no fim.",
            u"dic":u"Troca por BOM: então é <b>MAU</b>."},
           {u"palavra":u"MAL", u"img":u"", u"voz":u"mal",
            u"pista":u"O contrário de BEM (dormiu ___). Escreva com L no fim.",
            u"dic":u"Troca por BEM: então é <b>MAL</b>."}],
    dadosExtra={u"ENUN":u"Escreva a palavra, letra por letra.",
                u"FECHO":u"Você escreveu mau e mal do jeito certo!"})


CONTEUDO[u"fases"] = fases
io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8").write(
    json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
print(u"conteudo.json: %d fases (EM CONSTRUÇÃO)" % len(fases))
