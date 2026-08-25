# -*- coding: utf-8 -*-
u"""Gera _edf2/conteudo.json — BRINCAR E APRENDER COM A DONA CORUJA
    (Avaliação trimestral de EDUCAÇÃO FÍSICA · 2º ano).

Pedido do Marcos (ago/2026): uma avaliação trimestral de EF para o 2º ano, nos
moldes das de 3º ano (História/Geografia/Ciências): painel do professor, imagem
para cada questão e som em tudo. Tema BEM INFANTIL, LÚDICO e COLORIDO.

⭐ EDUVERSE mesmo numa AVALIAÇÃO: a criança NÃO vê "prova". Ela é convidada pela
   Dona Coruja para BRINCAR e mostrar o que já sabe — o problema (a brincadeira)
   vem primeiro, o conceito por último, andaime que cresce a cada erro, elogio
   sempre, nota NUNCA. Quem lê a avaliação de verdade é o PROFESSOR, no painel
   invisível ao aluno (FIM-DE-ATIVIDADE.md). É o jeito da casa: o aluno brinca,
   o professor avalia.

As 10 questões (5 dadas pelo Marcos + 5 lúdicas pedidas por ele):
   Q1 pega-pega TUBARÃO       Q6 regras de convivência
   Q2 associar brincadeiras   Q7 quebra-cabeça (brincar junto)
   Q3 memória de objetos      Q8 jogo UNO (cor da carta)
   Q4 escrever a brincadeira  Q9 coelhinho sai da toca
   Q5 alongar / aquecer       Q10 partes do corpo e seus movimentos

GABARITOS confirmados pelo Marcos:
   · pega-pega tubarão: quem é pego VIRA TUBARÃO e ajuda a pegar.
   · coelhinho sai da toca: ao APITO da professora, cada criança sai da sua toca
     e corre para outra; quem ficar SEM toca espera a próxima rodada.

⭐ REPETIÇÃO SEGUIDA, NÃO ESPAÇADA (RECEITA.md): cada gesto vem em BLOCO. 6 gestos
   distintos (escolher×3, ligar×2, classificar×2, memória, quebra-cabeça,
   escrever-legenda), todos contíguos. Nenhum gesto acima de 40%.

OBJETIVOS (o que o parecer do professor mede — 4/3/3):
   obj1 Brincadeiras e jogos (regras e papéis)  → Q1,Q9,Q2,Q8
   obj2 Corpo em movimento (aquecer, mover)      → Q5,Q10,Q3
   obj3 Convivência, cooperação e registro       → Q6,Q7,Q4

PIPELINE (padrão ESQUELETO):
  1) este build escreve conteudo.json;
  2) python3 _padrao/ESQUELETO/integrar.py --escrever
  3) python3 _padrao/ESQUELETO/montar.py _edf2
  4) ARTE: o Marcos gera pelos prompts (o Claude recorta/trata e cataloga);
  5) bancada + revisor + publicar (repo novo pela fabrica.yml).
"""
import io, json, os

PASTA = os.path.dirname(os.path.abspath(__file__))

HAB = (u"Experimentar e recriar brincadeiras e jogos da cultura popular, "
       u"explicando suas regras e papéis; reconhecer o corpo em movimento "
       u"(aquecimento e partes do corpo); e respeitar regras e colegas na "
       u"brincadeira. EF12EF01, EF12EF02, EF12EF03, EF12EF09, EF12EF10 (2º ano).")

CONTEUDO = {
 u"titulo": u"Brincar e Aprender com a Dona Coruja",
 u"sub": u"Educação Física · 2º ano · Avaliação trimestral (brincadeiras, corpo e convivência)",
 u"ano": u"2º ano",
 u"prefixo": u"ef",
 u"mascote": u"coruja",
 u"mascoteNome": u"Dona Coruja",
 u"crachas": 6,
 u"mesa": u"Pedagogo do 2º ano + professor de Educação Física (avaliação trimestral, tom lúdico).",
 u"fundo": u"ef_fundo.png",
 u"voz": u"feminina",
 u"tipo": u"avaliacao",
 u"abertura": (u"Oi! Eu sou a Dona Coruja. Hoje a gente vai BRINCAR bastante e "
              u"você vai me mostrar tudo o que já aprendeu. Vamos começar?"),
 u"fim": (u"Que time! Você brincou, pensou e mostrou o que sabe. A Dona Coruja "
          u"está muito orgulhosa de você!"),
 u"conceitos": {
   u"objetivo1": u"Brincadeiras e jogos (regras e papéis)",
   u"objetivo2": u"O corpo em movimento (aquecer e mover as partes)",
   u"objetivo3": u"Convivência, cooperação e registro",
 },
 u"curriculo": {
   u"objetivo1": u"Experimentar, recriar e explicar brincadeiras e jogos da cultura popular, com suas regras e papéis. EF12EF01/EF12EF02 (2º ano).",
   u"objetivo2": u"Reconhecer o corpo em movimento: aquecer/alongar e identificar partes do corpo e seus movimentos (ginástica geral). EF12EF09/EF12EF10 (2º ano).",
   u"objetivo3": u"Respeitar regras e colegas, cooperar na brincadeira e registrar o que se viveu. EF12EF03 (2º ano).",
 },
 u"fases": [],
}

fases = []
def add(**k): fases.append(k)

# ============================================================
# BLOCO 1 — ESCOLHER (Q1, Q9, Q5)  — gesto contíguo
# ============================================================

# Q1 — pega-pega TUBARÃO (obj1)
add(id=u"ef01", mec=u"escolher", selo=u"BRINCADEIRA: PEGA TUBARÃO", conceito=u"objetivo1",
    enunciado=u"No <b>pega-pega tubarão</b>, o que acontece com quem é pego?",
    dica=u"Pense: no tubarão, quem é pego vira ajudante do pegador.",
    dados=[{
      u"img": u"ef_pega_tubarao",
      u"p": u"No <b>pega-pega tubarão</b>, o que acontece com quem é pego?",
      u"c": {u"t": u"VIRA TUBARÃO E AJUDA A PEGAR", u"voz": u"vira tubarão e ajuda a pegar"},
      u"e": [{u"t": u"SAI DO JOGO E VAI SENTAR", u"voz": u"sai do jogo e vai sentar"},
             {u"t": u"GANHA UM PONTO E FOGE", u"voz": u"ganha um ponto e foge"}],
      u"d": [u"No tubarão, ninguém fica de fora: quem é pego continua brincando.",
             u"Quem é pego ajuda o pegador — o time de tubarões cresce.",
             u"Isso! Quem é pego <b>vira tubarão e ajuda a pegar</b>. Toque para seguir."],
    }])

# Q9 — coelhinho sai da toca (obj1) — 2 rodadas cobrem o gabarito inteiro
add(id=u"ef02", mec=u"escolher", selo=u"BRINCADEIRA: COELHINHO SAI DA TOCA", conceito=u"objetivo1",
    enunciado=u"No <b>coelhinho sai da toca</b>, quando a professora apita, o que cada criança faz?",
    dica=u"O apito é o sinal: cada coelhinho troca de casa.",
    dados=[{
      u"img": u"ef_coelhinho",
      u"p": u"Quando a professora <b>apita</b>, o que cada coelhinho faz?",
      u"c": {u"t": u"SAI DA SUA TOCA E CORRE PARA OUTRA", u"voz": u"sai da sua toca e corre para outra"},
      u"e": [{u"t": u"FICA PARADO NA MESMA TOCA", u"voz": u"fica parado na mesma toca"},
             {u"t": u"SENTA NO CHÃO E ESPERA", u"voz": u"senta no chão e espera"}],
      u"d": [u"O apito quer dizer: todo mundo troca de toca!",
             u"Cada coelhinho sai correndo para uma toca diferente.",
             u"Isso! Cada um <b>sai da sua toca e corre para outra</b>. Toque para seguir."],
     },{
      u"img": u"ef_coelhinho",
      u"p": u"E quem ficar <b>sem toca</b>, o que faz?",
      u"c": {u"t": u"ESPERA A PRÓXIMA RODADA PARA PEGAR UMA TOCA", u"voz": u"espera a próxima rodada para pegar uma toca"},
      u"e": [{u"t": u"SAI DA BRINCADEIRA PARA SEMPRE", u"voz": u"sai da brincadeira para sempre"},
             {u"t": u"EMPURRA UM COLEGA PARA ENTRAR", u"voz": u"empurra um colega para entrar"}],
      u"d": [u"Ninguém sai da brincadeira e ninguém empurra ninguém.",
             u"Quem ficou sem toca só aguarda o próximo apito.",
             u"Isso! Ele <b>espera a próxima rodada</b> para pegar uma toca. Toque para seguir."],
    }])

# Q5 — aquecer / alongar (obj2)
add(id=u"ef03", mec=u"escolher", selo=u"ANTES DE BRINCAR", conceito=u"objetivo2",
    enunciado=u"<b>Antes</b> de correr e brincar, o que devemos fazer com o corpo?",
    dica=u"O corpo precisa ficar pronto, como um carrinho esquentando o motor.",
    dados=[{
      u"img": u"ef_aquecer",
      u"p": u"<b>Antes</b> de correr e brincar, o que devemos fazer com o corpo?",
      u"c": {u"t": u"AQUECER E ALONGAR O CORPO", u"voz": u"aquecer e alongar o corpo"},
      u"e": [{u"t": u"COMER UM DOCE", u"voz": u"comer um doce"},
             {u"t": u"FICAR SENTADO", u"voz": u"ficar sentado"}],
      u"d": [u"O corpo precisa esquentar devagarinho antes do esforço.",
             u"Alongar e aquecer deixa os músculos prontos para brincar.",
             u"Isso! A gente <b>aquece e alonga</b> o corpo. Toque para seguir."],
     },{
      u"img": u"ef_aquecer",
      u"p": u"Por que é bom <b>aquecer</b> antes?",
      u"c": {u"t": u"PARA NÃO SE MACHUCAR", u"voz": u"para não se machucar"},
      u"e": [{u"t": u"PARA FICAR COM SONO", u"voz": u"para ficar com sono"},
             {u"t": u"PARA NÃO PRECISAR BRINCAR", u"voz": u"para não precisar brincar"}],
      u"d": [u"Corpo frio se machuca mais fácil.",
             u"Aquecer protege os músculos e as juntas.",
             u"Isso! Aquecer é <b>para não se machucar</b>. Toque para seguir."],
    }])

# ============================================================
# BLOCO 2 — LIGAR (Q2, Q10)  — gesto contíguo
# ============================================================

# Q2 — associar brincadeiras (obj1): a FIGURA da brincadeira <-> o NOME
add(id=u"ef04", mec=u"ligar", selo=u"CADA BRINCADEIRA, SEU NOME", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>brincadeira</b> ao seu nome.",
    dica=u"Olhe a figura e lembre como a gente chama essa brincadeira.",
    dados=[{u"k":u"b0", u"img":u"ef_amarelinha", u"voz":u"amarelinha", u"s":u"AMARELINHA"},
           {u"k":u"b1", u"img":u"ef_corda",      u"voz":u"pular corda", u"s":u"PULAR CORDA"},
           {u"k":u"b2", u"img":u"ef_piao",       u"voz":u"pião",        u"s":u"PIÃO"},
           {u"k":u"b3", u"img":u"ef_gude",       u"voz":u"bola de gude",u"s":u"BOLA DE GUDE"}])

# Q10 — partes do corpo e seus movimentos (obj2): MOVIMENTO (figura) <-> PARTE
add(id=u"ef05", mec=u"ligar", selo=u"O CORPO SE MEXE", conceito=u"objetivo2",
    enunciado=u"Ligue cada <b>movimento</b> à parte do corpo que o faz.",
    dica=u"Pense: com o quê eu corro? Com o quê eu bato palmas?",
    dados=[{u"k":u"c0", u"img":u"ef_correr",   u"voz":u"correr",         u"s":u"PERNAS"},
           {u"k":u"c1", u"img":u"ef_arremesso",u"voz":u"arremessar a bola",u"s":u"BRAÇOS"},
           {u"k":u"c2", u"img":u"ef_palmas",   u"voz":u"bater palmas",   u"s":u"MÃOS"},
           {u"k":u"c3", u"img":u"ef_agachar",  u"voz":u"agachar",        u"s":u"JOELHOS"}])

# ============================================================
# BLOCO 3 — CLASSIFICAR (Q6, Q8)  — gesto contíguo
# ============================================================

# Q6 — regras de convivência (obj3): PODE / NÃO PODE
add(id=u"ef06", mec=u"classificar", selo=u"BRINCAR BEM COM OS AMIGOS", conceito=u"objetivo3",
    enunciado=u"Cada atitude na sua gaveta: na brincadeira, <b>PODE</b> ou <b>NÃO PODE</b>?",
    dica=u"Pense: isso deixa todo mundo feliz e seguro, ou machuca e magoa?",
    dados=[{u"k":u"pode",  u"n":u"PODE",     u"img":u"", u"voz":u"pode",     u"rot":False},
           {u"k":u"nao",   u"n":u"NÃO PODE", u"img":u"", u"voz":u"não pode", u"rot":False}],
    dadosExtra={
      u"FICHAS":[{u"t":u"ESPERAR A VEZ",    u"alvo":u"pode"},
                 {u"t":u"AJUDAR O COLEGA",  u"alvo":u"pode"},
                 {u"t":u"DIVIDIR A BOLA",   u"alvo":u"pode"},
                 {u"t":u"EMPURRAR",         u"alvo":u"nao"},
                 {u"t":u"XINGAR O AMIGO",   u"alvo":u"nao"},
                 {u"t":u"TRAPACEAR",        u"alvo":u"nao"}],
      u"DICAS":[u"Pergunte: isso deixa o colega feliz e seguro?",
                u"Esperar, ajudar e dividir cuidam do amigo; empurrar, xingar e trapacear machucam.",
                u"Boa! Brincar bem é cuidar de todo mundo. Toque para seguir."],
    })

# Q8 — jogo UNO (obj1): separar as cartas por COR (regra do UNO: combina a cor)
add(id=u"ef07", mec=u"classificar", selo=u"JOGO UNO: A COR DA CARTA", conceito=u"objetivo1",
    enunciado=u"No <b>UNO</b>, a gente junta cartas da mesma cor. Ponha cada carta na sua gaveta de cor.",
    dica=u"Olhe só a COR de cada carta e leve para a gaveta daquela cor.",
    dados=[{u"k":u"verm", u"n":u"VERMELHA", u"img":u"", u"voz":u"vermelha", u"rot":False},
           {u"k":u"azul", u"n":u"AZUL",     u"img":u"", u"voz":u"azul",     u"rot":False},
           {u"k":u"amar", u"n":u"AMARELA",  u"img":u"", u"voz":u"amarela",  u"rot":False}],
    dadosExtra={
      u"FICHAS":[{u"t":u"", u"alvo":u"verm", u"img":u"ef_uno_v1"},
                 {u"t":u"", u"alvo":u"verm", u"img":u"ef_uno_v2"},
                 {u"t":u"", u"alvo":u"azul", u"img":u"ef_uno_a1"},
                 {u"t":u"", u"alvo":u"azul", u"img":u"ef_uno_a2"},
                 {u"t":u"", u"alvo":u"amar", u"img":u"ef_uno_m1"},
                 {u"t":u"", u"alvo":u"amar", u"img":u"ef_uno_m2"}],
      u"DICAS":[u"Não importa o número: olhe a COR.",
                u"Carta vermelha vai com vermelha, azul com azul, amarela com amarela.",
                u"Isso! No UNO a gente combina pela cor. Toque para seguir."],
    })

# ============================================================
# BLOCO 4 — MEMÓRIA (Q3)
# ============================================================

# Q3 — memória de objetos da aula de EF (obj2)
add(id=u"ef08", mec=u"memoria", selo=u"MEMÓRIA DOS MATERIAIS", conceito=u"objetivo2",
    enunciado=u"Ache as <b>figuras iguais</b> dos materiais da Educação Física.",
    dica=u"Vire duas cartas e guarde na memória onde cada material está.",
    dados=[{u"k":u"bola",  u"img":u"ef_bola",  u"imgsen":u"ef_bola",  u"voz":u"bola",     u"vozsen":u"bola"},
           {u"k":u"arco",  u"img":u"ef_arco",  u"imgsen":u"ef_arco",  u"voz":u"arco",     u"vozsen":u"arco"},
           {u"k":u"cone",  u"img":u"ef_cone",  u"imgsen":u"ef_cone",  u"voz":u"cone",     u"vozsen":u"cone"},
           {u"k":u"apito", u"img":u"ef_apito", u"imgsen":u"ef_apito", u"voz":u"apito",    u"vozsen":u"apito"}])

# ============================================================
# BLOCO 5 — QUEBRA-CABEÇA (Q7)
# ============================================================

# Q7 — montar a cena da turma brincando junta (obj3)
add(id=u"ef09", mec=u"quebra-cabeca", selo=u"MONTE A TURMA BRINCANDO", conceito=u"objetivo3",
    enunciado=u"Monte o quebra-cabeça! É a turma brincando junta, cooperando.",
    dica=u"Olhe as bordas e as cores de cada pedaço para achar o lugar.",
    dados={u"img":u"ef_turma_puzzle", u"cols":3, u"lins":2, u"w":453, u"h":302, u"fundo":True})

# ============================================================
# BLOCO 6 — ESCREVER A LEGENDA (Q4)
# ============================================================

# Q4 — escrever o nome da brincadeira (obj3)
add(id=u"ef10", mec=u"escrever-legenda", selo=u"ESCREVA A BRINCADEIRA", conceito=u"objetivo3",
    enunciado=u"Olhe a foto e <b>escreva o nome</b> da brincadeira.",
    dica=u"Diga o nome em voz alta e escreva do jeitinho que você fala.",
    dados=[{u"sel":u"FOTO 1 DE 2",
            u"ped":u"Que brincadeira é esta? <b>Escreva o nome</b>.",
            u"apoio":[u"amarelinha", u"pula", u"casinha", u"pé", u"número"],
            u"comeco":u"É a ",
            u"img":u"ef_amarelinha"},
           {u"sel":u"FOTO 2 DE 2",
            u"ped":u"E esta brincadeira, qual é? <b>Escreva o nome</b>.",
            u"apoio":[u"cabo", u"de", u"guerra", u"corda", u"puxar", u"time"],
            u"comeco":u"É o ",
            u"img":u"ef_cabo_guerra"}])

# ============================================================
CONTEUDO[u"fases"] = fases
CONTEUDO[u"habilidades"] = HAB

cam = os.path.join(PASTA, u"conteudo.json")
with io.open(cam, u"w", encoding=u"utf-8") as f:
    f.write(json.dumps(CONTEUDO, ensure_ascii=False, indent=1))

print(u"conteudo.json escrito: %d fases (%s)" % (len(fases), CONTEUDO[u"titulo"]))
gestos = {}
for x in fases:
    gestos[x[u"mec"]] = gestos.get(x[u"mec"], 0) + 1
print(u"gestos:", gestos)
obj = {}
for x in fases:
    obj[x[u"conceito"]] = obj.get(x[u"conceito"], 0) + 1
print(u"objetivos:", obj)
