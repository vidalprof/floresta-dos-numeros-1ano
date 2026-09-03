# -*- coding: utf-8 -*-
u"""Gera _revista5/conteudo.json — A REVISTA DAS PALAVRAS (5º ano, Português).

FORMATO (escolha do Marcos, set/2026): "Revista de Gêneros + Marca-Classes".
A criança é repórter/editora da REVISTA DAS PALAVRAS. Cada MATÉRIA é um GÊNERO
textual. Para a matéria "fechar", ela precisa (1) LER e INTERPRETAR o texto e
(2) MARCAR as palavras que são SUBSTANTIVO, ADJETIVO e VERBO — retiradas do
PRÓPRIO texto. O problema (fechar a revista) vem ANTES do conceito (as classes).

OBJETIVOS:
  · objetivo1 — LER e INTERPRETAR diferentes GÊNEROS textuais;
  · objetivo2 — identificar SUBSTANTIVO (nomes de seres, coisas e lugares);
  · objetivo3 — identificar ADJETIVO (as qualidades);
  · objetivo4 — identificar VERBO (as ações).

PROGRESSÃO (concreto → figural → simbólico; UMA classe por vez e depois as TRÊS):
  1) SUBSTANTIVO sozinho, nos gêneros simples (bilhete, convite, lista, aviso,
     e-mail, carta);
  2) reconhecer o GÊNERO (quem-sou-eu) — revisão de leitura;
  3) ADJETIVO (poema, tirinha, anúncio);
  4) VERBO (receita, notícia, regras de jogo);
  5) ORDENAR a sequência (dobradura, fábula) — interpretação;
  6) AS TRÊS CLASSES JUNTAS — classificar em 3 gavetas (fábula, notícia, diário,
     carta) = clímax "Edição Especial".
  DOIS AQUECIMENTOS (revisão espaçada): um no meio da 1ª metade (~32%, revê
  SUBSTANTIVO por 'ligar') e um no meio da 2ª metade (~68%, revê ADJETIVO por
  'caça-palavras').

REPETIÇÃO SEGUIDA, NÃO ESPAÇADA (regra do Marcos): cada mecânica vem em BLOCO
contíguo, subindo um degrau. Únicos reusos fora de bloco = os 2 AQUECIMENTOS.

  idx  gênero (MATÉRIA)     gesto           o que treina
   0   bilhete    (M1)      escolher        interpretar (obj1)
   1   bilhete    (M1)      escolher        marcar SUBSTANTIVO (obj2)
   2   convite    (M2)      escolher        interpretar (obj1)
   3   convite    (M2)      escolher        marcar SUBSTANTIVO (obj2)
   4   lista      (M3)      escolher        interpretar (obj1)
   5   lista      (M3)      escolher        marcar SUBSTANTIVO (obj2)
   6   aviso      (M4)      escolher        interpretar (obj1)
   7   aviso      (M4)      escolher        marcar SUBSTANTIVO (obj2)
   8   e-mail     (M5)      caca-palavras   achar os SUBSTANTIVOS (obj2)
   9   carta      (M6)      caca-palavras   achar os SUBSTANTIVOS (obj2)
  10   —                    AQUEC 1 (ligar) revisão: substantivo -> tipo (obj2)
  11   —                    quem-sou-eu     reconhecer o GÊNERO (obj1)
  12   —                    quem-sou-eu     reconhecer o GÊNERO (obj1)
  13   —                    quem-sou-eu     reconhecer o GÊNERO (obj1)
  14   poema      (M7)      ligar           adjetivo -> substantivo (obj3)
  15   tirinha    (M8)      ligar           adjetivo -> substantivo (obj3)
  16   anúncio    (M9)      ligar           adjetivo -> substantivo (obj3)
  17   receita/bolo (M10)   completar       marcar o VERBO/ação (obj4)
  18   receita/suco (M11)   completar       marcar o VERBO/ação (obj4)
  19   notícia    (M12)     completar       marcar o VERBO/ação (obj4)
  20   regras jogo (M13)    completar       marcar o VERBO/ação (obj4)
  21   dobradura  (M14)     linha-do-tempo  ordenar os PASSOS (obj1)
  22   fábula     (M15)     linha-do-tempo  ordenar os FATOS (obj1)
  23   —                    AQUEC 2 (caça)  revisão: achar ADJETIVOS (obj3)
  24   propaganda (M16)     intruso         qual NÃO é verbo (obj4)
  25   fábula     (M17)     intruso         qual NÃO é verbo (obj4)
  26   verbete    (M18)     intruso         qual NÃO é substantivo (obj2)
  27   quadrinha  (M19)     digitar         escrever o SUBSTANTIVO (obj2)
  28   trava-língua (M20)   digitar         escrever o VERBO (obj4)
  29   fábula     (M21)     classificar     3 gavetas (obj2)
  30   fábula     (M22)     classificar     3 gavetas (obj3)
  31   notícia    (M23)     classificar     3 gavetas (obj4)
  32   diário     (M24)     classificar     3 gavetas (obj2)
  33   carta      (M25)     classificar     3 gavetas — clímax (obj3)

PIPELINE (ESQUELETO): este arquivo escreve conteudo.json; depois
  python3 _padrao/ESQUELETO/montar.py _revista5
gera index.html + falas.json + arte.json + sw.js (o motor blindado — capa,
crachá, boletim animado, relatório do professor e RETOMAR de 55 min já vêm
embutidos no motor).
"""
import io, json, os

PASTA = os.path.dirname(os.path.abspath(__file__))

CONTEUDO = {
 u"titulo": u"A Revista das Palavras",
 u"sub": u"Português · 5º ano · Gêneros textuais + substantivo, adjetivo e verbo",
 u"ano": u"5º ano",
 u"prefixo": u"rv",
 u"mascote": u"raposa",
 u"mascoteNome": u"Filó",   # MESMO mascote/arte da Detetive (raposa Filó), reaproveitado (regra do banco). Sem o título "Detetive" (aqui ela é a editora) — o que também deixa o clone.py verde.
 u"crachas": 6,
 u"mesa": (u"Pedagogo do 5º ano + especialista em Língua Portuguesa (leitura de "
           u"gêneros textuais e classes de palavras: substantivo, adjetivo e verbo)."),
 u"fundo": u"rv_fundo.jpg",
 u"voz": u"feminina",
 u"abertura": (u"Bem-vindo(a) à redação da Revista das Palavras! Sou a Filó, a "
               u"editora-chefe. Cada matéria só fecha quando lemos com atenção e "
               u"marcamos as palavras certas. Vamos preparar a próxima edição?"),
 u"fim": (u"Edição fechada, repórter! Você lê cada gênero e sabe achar os "
          u"substantivos, os adjetivos e os verbos onde eles se escondem."),
 u"conceitos": {
   u"objetivo1": u"Ler e entender bilhete, convite, lista, aviso, e-mail, carta, poema, tirinha, receita, notícia, fábula e mais",
   u"objetivo2": u"Achar os SUBSTANTIVOS (nomes de seres, coisas e lugares)",
   u"objetivo3": u"Achar os ADJETIVOS (as qualidades)",
   u"objetivo4": u"Achar os VERBOS (as ações)",
 },
 u"curriculo": {
   u"objetivo1": (u"Ler e compreender, com autonomia, textos de diferentes gêneros "
                  u"(bilhete, convite, lista, aviso, e-mail, carta, poema, tirinha, receita, "
                  u"notícia, fábula), localizando informações explícitas e inferindo sentidos. EF35LP03/EF35LP04/EF05LP01."),
   u"objetivo2": (u"Reconhecer a classe SUBSTANTIVO — nomes de seres, coisas, lugares e "
                  u"sentimentos — em textos de diferentes gêneros. EF04LP07/EF05LP08 (classes de palavras)."),
   u"objetivo3": (u"Reconhecer a classe ADJETIVO e a qualidade que ele atribui ao "
                  u"substantivo, em textos de diferentes gêneros. EF04LP07/EF05LP08."),
   u"objetivo4": (u"Reconhecer a classe VERBO — a ação ou o estado — em textos de "
                  u"diferentes gêneros, inclusive no imperativo dos textos injuntivos. EF04LP07/EF05LP08."),
 },
 u"fases": [],
}

fases = []
def add(**k): fases.append(k)

def esc(p, c, e, d):
    u"""escolher só de texto (gramática/interpretação): sem imagem."""
    return {u"img": u"", u"p": p, u"c": c, u"e": e, u"d": d}

# ============================================================
# BLOCO 1 — escolher (idx 0-7): SUBSTANTIVO, uma classe por vez, gêneros
#           simples. Cada matéria: 1 interpretação (obj1) + 1 marcar (obj2).
# ============================================================

# --- M1 BILHETE ---
BILHETE = u"<i>“Mãe, guardei o bolo de chocolate na geladeira. Não conte para a Bia! Volto às cinco horas. Beijos, Léo.”</i>"
add(id=u"f01", mec=u"escolher", selo=u"MATÉRIA 1 · O BILHETE", conceito=u"objetivo1",
    enunciado=u"Leia o <b>bilhete</b> e responda o que ele conta.",
    dica=u"A resposta está NO bilhete. Volte e leia de novo se precisar.",
    dados=[
      esc(u"Leia o bilhete: " + BILHETE + u" Quem escreveu o bilhete?",
          u"O Léo", [u"A Bia", u"A mãe"],
          [u"Procure a assinatura no fim do bilhete.", u"Termina com “Beijos, <b>Léo</b>”.",
           u"É <b>o Léo</b>. Toque para seguir."]),
      esc(u"No mesmo bilhete, onde o Léo guardou o bolo?",
          u"Na geladeira", [u"No forno", u"Na mochila"],
          [u"Procure o lugar do bolo.", u"“…guardei o bolo na <b>geladeira</b>.”",
           u"É <b>na geladeira</b>. Toque para seguir."]),
      esc(u"O que o Léo pediu à mãe no bilhete?",
          u"Não contar para a Bia", [u"Comprar outro bolo", u"Ligar às cinco horas"],
          [u"Procure a frase com “Não…”.", u"“<b>Não conte para a Bia!</b>”",
           u"É <b>não contar para a Bia</b>. Toque para seguir."]),
      esc(u"A que horas o Léo volta?",
          u"Às cinco horas", [u"Ao meio-dia", u"Às nove horas"],
          [u"Procure a palavra de TEMPO.", u"“Volto às <b>cinco horas</b>.”",
           u"É <b>às cinco horas</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"O BILHETE", u"FECHO": u"Você leu o bilhete como repórter!"})

add(id=u"f02", mec=u"escolher", selo=u"MATÉRIA 1 · MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
    enunciado=u"No bilhete, marque as palavras que são <b>SUBSTANTIVO</b> (nome de ser, coisa ou lugar).",
    dica=u"Substantivo dá nome: pessoas, coisas, lugares e animais.",
    dados=[
      esc(u"“Guardei o <b>bolo</b> na geladeira.” Qual palavra é um SUBSTANTIVO (nome de coisa)?",
          u"bolo", [u"guardei", u"na"],
          [u"Qual palavra é o nome de uma coisa que se come?",
           u"<b>guardei</b> é ação (verbo); <b>na</b> liga palavras. Sobra o nome.",
           u"É <b>bolo</b> — nome de uma coisa. Toque para seguir."]),
      esc(u"“Guardei o bolo na <b>geladeira</b>.” Qual palavra nomeia um LUGAR/objeto (substantivo)?",
          u"geladeira", [u"guardei", u"o"],
          [u"Qual é o nome do objeto onde o bolo ficou?",
           u"<b>guardei</b> é verbo; <b>o</b> é artigo. Sobra o nome.",
           u"É <b>geladeira</b> — nome de um objeto. Toque para seguir."]),
      esc(u"“Não conte para a <b>Bia</b>.” Qual palavra é o nome de uma PESSOA (substantivo)?",
          u"Bia", [u"conte", u"não"],
          [u"Qual é o nome de gente na frase?",
           u"<b>conte</b> é ação; <b>não</b> nega. Sobra o nome de gente.",
           u"É <b>Bia</b> — nome de pessoa. Toque para seguir."]),
      esc(u"“Volto às cinco <b>horas</b>.” Qual palavra é um SUBSTANTIVO?",
          u"horas", [u"volto", u"cinco"],
          [u"Tire a ação e o número: o que sobra é o nome.",
           u"<b>volto</b> é verbo; <b>cinco</b> é número. Sobra o nome.",
           u"É <b>horas</b> — nome de uma medida de tempo. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"OS SUBSTANTIVOS DO BILHETE", u"FECHO": u"Você achou os nomes escondidos no bilhete!"})

# --- M2 CONVITE ---
CONVITE = u"<i>“Você está convidado para a minha festa de aniversário! Vai ser no sábado, às três horas da tarde, no salão do prédio. Vamos ter bolo, música e muitas brincadeiras. Não falte! Duda.”</i>"
add(id=u"f03", mec=u"escolher", selo=u"MATÉRIA 2 · O CONVITE", conceito=u"objetivo1",
    enunciado=u"Leia o <b>convite</b> e responda o que ele avisa.",
    dica=u"Um convite diz PARA QUÊ, QUANDO e ONDE. Procure no texto.",
    dados=[
      esc(u"Leia o convite: " + CONVITE + u" Para que é o convite?",
          u"Uma festa de aniversário", [u"Um passeio à praia", u"Uma reunião da escola"],
          [u"Logo no começo o convite diz para quê.", u"“…para a minha <b>festa de aniversário</b>!”",
           u"É <b>uma festa de aniversário</b>. Toque para seguir."]),
      esc(u"No mesmo convite, quando vai ser a festa?",
          u"No sábado, às três da tarde", [u"No domingo de manhã", u"Na sexta à noite"],
          [u"Procure o DIA e a HORA.", u"“…no <b>sábado, às três horas da tarde</b>.”",
           u"É <b>no sábado, às três da tarde</b>. Toque para seguir."]),
      esc(u"Onde vai ser a festa?",
          u"No salão do prédio", [u"Na casa da Duda", u"No parque da cidade"],
          [u"Procure a palavra de LUGAR.", u"“…no <b>salão do prédio</b>.”",
           u"É <b>no salão do prédio</b>. Toque para seguir."]),
      esc(u"Quem fez o convite?",
          u"A Duda", [u"O Léo", u"A professora"],
          [u"Procure a assinatura no fim.", u"O convite termina com “<b>Duda</b>”.",
           u"É <b>a Duda</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"O CONVITE", u"FECHO": u"Você leu o convite inteirinho!"})

add(id=u"f04", mec=u"escolher", selo=u"MATÉRIA 2 · MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
    enunciado=u"No convite, marque as palavras que são <b>SUBSTANTIVO</b> (nome de coisa, lugar ou pessoa).",
    dica=u"Substantivo dá nome. Ação é verbo; ligação é preposição.",
    dados=[
      esc(u"“Vai ser no <b>salão</b> do prédio.” Qual palavra nomeia um LUGAR (substantivo)?",
          u"salão", [u"ser", u"no"],
          [u"Qual é o nome do lugar da festa?",
           u"<b>ser</b> é verbo; <b>no</b> liga palavras. Sobra o nome.",
           u"É <b>salão</b> — nome de um lugar. Toque para seguir."]),
      esc(u"“Vamos ter bolo, <b>música</b> e brincadeiras.” Qual palavra é um SUBSTANTIVO?",
          u"música", [u"vamos", u"e"],
          [u"Qual dessas é o nome de uma coisa?",
           u"<b>vamos</b> é ação; <b>e</b> liga. Sobra o nome.",
           u"É <b>música</b> — nome de uma coisa. Toque para seguir."]),
      esc(u"“É a minha <b>festa</b> de aniversário.” Qual palavra nomeia o evento (substantivo)?",
          u"festa", [u"minha", u"de"],
          [u"Qual é o nome do evento?",
           u"<b>minha</b> mostra de quem é (pronome); <b>de</b> liga. Sobra o nome.",
           u"É <b>festa</b> — nome de um evento. Toque para seguir."]),
      esc(u"“Não falte, <b>Duda</b>!” Qual palavra é o nome de uma PESSOA (substantivo)?",
          u"Duda", [u"falte", u"não"],
          [u"Qual é o nome de gente na frase?",
           u"<b>falte</b> é ação; <b>não</b> nega. Sobra o nome de gente.",
           u"É <b>Duda</b> — nome de pessoa. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"OS SUBSTANTIVOS DO CONVITE", u"FECHO": u"Você marcou os substantivos do convite!"})

# --- M3 LISTA DE COMPRAS ---
LISTA = u"<i>“Lista do mercado: arroz, feijão, dois tomates, um pão e leite. Não esquecer o sabão.”</i>"
add(id=u"f05", mec=u"escolher", selo=u"MATÉRIA 3 · A LISTA DE COMPRAS", conceito=u"objetivo1",
    enunciado=u"Leia a <b>lista de compras</b> e responda.",
    dica=u"A lista serve para não esquecer o que comprar. Procure no texto.",
    dados=[
      esc(u"Leia a lista: " + LISTA + u" Que tipo de texto é este?",
          u"Uma lista de compras", [u"Uma receita de bolo", u"Um bilhete de recado"],
          [u"Ele enumera o que comprar.", u"São itens do mercado, um atrás do outro: <b>uma lista</b>.",
           u"É <b>uma lista de compras</b>. Toque para seguir."]),
      esc(u"Quantos tomates estão na lista?",
          u"Dois", [u"Um", u"Três"],
          [u"Procure o número perto de 'tomates'.", u"“…<b>dois tomates</b>…”",
           u"É <b>dois</b>. Toque para seguir."]),
      esc(u"O que a lista lembra de não esquecer?",
          u"O sabão", [u"O arroz", u"O leite"],
          [u"Procure a frase 'Não esquecer…'.", u"“Não esquecer o <b>sabão</b>.”",
           u"É <b>o sabão</b>. Toque para seguir."]),
      esc(u"Onde vão ser feitas as compras?",
          u"No mercado", [u"Na farmácia", u"Na escola"],
          [u"O título da lista diz o lugar.", u"“Lista do <b>mercado</b>…”",
           u"É <b>no mercado</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"A LISTA DE COMPRAS", u"FECHO": u"Você entendeu a lista toda!"})

add(id=u"f06", mec=u"escolher", selo=u"MATÉRIA 3 · MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
    enunciado=u"Na lista, marque as palavras que são <b>SUBSTANTIVO</b> (nome de coisa).",
    dica=u"Quase tudo numa lista de compras é substantivo: nomes de coisas.",
    dados=[
      esc(u"“Comprar <b>arroz</b> e feijão.” Qual palavra é um SUBSTANTIVO?",
          u"arroz", [u"comprar", u"e"],
          [u"Qual é o nome do alimento?",
           u"<b>comprar</b> é ação; <b>e</b> liga. Sobra o nome.",
           u"É <b>arroz</b> — nome de um alimento. Toque para seguir."]),
      esc(u"“Não esquecer o <b>sabão</b>.” Qual palavra nomeia uma coisa (substantivo)?",
          u"sabão", [u"esquecer", u"o"],
          [u"Qual é o nome do produto?",
           u"<b>esquecer</b> é verbo; <b>o</b> é artigo. Sobra o nome.",
           u"É <b>sabão</b> — nome de uma coisa. Toque para seguir."]),
      esc(u"“Um pão e <b>leite</b>.” Qual palavra é um SUBSTANTIVO?",
          u"leite", [u"um", u"e"],
          [u"Qual é o nome da bebida?",
           u"<b>um</b> é artigo; <b>e</b> liga. Sobra o nome.",
           u"É <b>leite</b> — nome de um alimento. Toque para seguir."]),
      esc(u"“Dois <b>tomates</b> maduros.” Qual palavra é o nome (substantivo)?",
          u"tomates", [u"dois", u"maduros"],
          [u"Tire o número e a qualidade: sobra o nome.",
           u"<b>dois</b> é número; <b>maduros</b> é qualidade (adjetivo). Sobra o nome.",
           u"É <b>tomates</b> — nome de um alimento. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"OS SUBSTANTIVOS DA LISTA", u"FECHO": u"Você achou os substantivos da lista!"})

# --- M4 AVISO / CARTAZ ---
AVISO = u"<i>“ATENÇÃO! O pátio será pintado no sábado. Não pise na tinta fresca. A direção agradece.”</i>"
add(id=u"f07", mec=u"escolher", selo=u"MATÉRIA 4 · O AVISO", conceito=u"objetivo1",
    enunciado=u"Leia o <b>aviso</b> do mural e responda.",
    dica=u"Um aviso comunica algo importante a todos. Procure no texto.",
    dados=[
      esc(u"Leia o aviso: " + AVISO + u" O que o aviso comunica?",
          u"Que o pátio será pintado", [u"Que a aula foi cancelada", u"Que vai ter festa"],
          [u"Leia a primeira frase depois de 'ATENÇÃO'.", u"“O <b>pátio será pintado</b> no sábado.”",
           u"É <b>que o pátio será pintado</b>. Toque para seguir."]),
      esc(u"Quando o pátio será pintado?",
          u"No sábado", [u"No domingo", u"Na sexta"],
          [u"Procure o dia no aviso.", u"“…pintado no <b>sábado</b>.”",
           u"É <b>no sábado</b>. Toque para seguir."]),
      esc(u"O que NÃO se deve fazer, segundo o aviso?",
          u"Pisar na tinta fresca", [u"Entrar no pátio", u"Falar alto"],
          [u"Procure a frase com 'Não'.", u"“<b>Não pise na tinta fresca.</b>”",
           u"É <b>pisar na tinta fresca</b>. Toque para seguir."]),
      esc(u"Quem escreveu o aviso?",
          u"A direção", [u"A professora", u"Um aluno"],
          [u"Procure quem 'agradece' no fim.", u"“A <b>direção</b> agradece.”",
           u"É <b>a direção</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"O AVISO", u"FECHO": u"Você leu o aviso do mural!"})

add(id=u"f08", mec=u"escolher", selo=u"MATÉRIA 4 · MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
    enunciado=u"No aviso, marque as palavras que são <b>SUBSTANTIVO</b> (nome de coisa ou lugar).",
    dica=u"Substantivo dá nome. Cuidado: 'fresca' e 'pintado' são qualidades, não nomes.",
    dados=[
      esc(u"“O <b>pátio</b> será pintado.” Qual palavra nomeia um LUGAR (substantivo)?",
          u"pátio", [u"será", u"pintado"],
          [u"Qual é o nome do lugar da escola?",
           u"<b>será</b> é verbo; <b>pintado</b> é qualidade. Sobra o nome do lugar.",
           u"É <b>pátio</b> — nome de um lugar. Toque para seguir."]),
      esc(u"“Não pise na <b>tinta</b>.” Qual palavra nomeia uma coisa (substantivo)?",
          u"tinta", [u"pise", u"na"],
          [u"Qual é o nome do material?",
           u"<b>pise</b> é ação; <b>na</b> liga. Sobra o nome.",
           u"É <b>tinta</b> — nome de uma coisa. Toque para seguir."]),
      esc(u"“A <b>direção</b> agradece.” Qual palavra é um SUBSTANTIVO?",
          u"direção", [u"agradece", u"a"],
          [u"Qual é o nome de quem agradece?",
           u"<b>agradece</b> é ação; <b>a</b> é artigo. Sobra o nome.",
           u"É <b>direção</b> — nome de quem manda o aviso. Toque para seguir."]),
      esc(u"“A tinta fresca secou no <b>chão</b>.” Qual palavra nomeia um LUGAR (substantivo)?",
          u"chão", [u"secou", u"fresca"],
          [u"Qual é o nome do lugar onde a tinta secou?",
           u"<b>secou</b> é ação; <b>fresca</b> é qualidade. Sobra o nome do lugar.",
           u"É <b>chão</b> — nome de um lugar. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"OS SUBSTANTIVOS DO AVISO", u"FECHO": u"Você marcou os substantivos do aviso!"})

# ============================================================
# BLOCO 2 — caca-palavras (idx 8-9): achar os SUBSTANTIVOS (obj2), gêneros
#           e-mail e carta. Grade normaliza acentos; chips mantêm o acento.
# ============================================================
LETRAS = u"ABCDEHILMNOPRSTUV"

add(id=u"f09", mec=u"caca-palavras", selo=u"MATÉRIA 5 · A MENSAGEM", conceito=u"objetivo2",
    enunciado=(u"Leia o <b>e-mail</b>: <i>“Assunto: Passeio da turma. Olá! Confirmem se "
               u"vão ao museu na sexta. Levem lanche e caderno.”</i> Ache no quadro os "
               u"<b>SUBSTANTIVOS</b> da mensagem."),
    dica=u"Substantivos = nomes de coisas e lugares. Estão deitados (→) e em pé (↓).",
    dados=[u"MUSEU", u"LANCHE", u"CADERNO", u"TURMA", u"PASSEIO"],
    dadosExtra={u"MODO": u"lista", u"TITULO": u"OS SUBSTANTIVOS DA MENSAGEM",
                u"LETRAS": LETRAS, u"DIFICIL": u"",
                u"CORP": [u"p1", u"p2", u"p3", u"p4", u"p5"]})

add(id=u"f10", mec=u"caca-palavras", selo=u"MATÉRIA 6 · A CARTA", conceito=u"objetivo2",
    enunciado=(u"Leia a <b>carta</b>: <i>“Querida vovó, estou com saudade. A escola vai bem "
               u"e ganhei uma medalha. Um abraço, Tomás.”</i> Ache no quadro os "
               u"<b>SUBSTANTIVOS</b> da carta."),
    dica=u"Substantivos = nomes de gente e coisas. Deitados (→) e em pé (↓).",
    dados=[u"CARTA", u"VOVÓ", u"ESCOLA", u"MEDALHA", u"ABRAÇO"],
    dadosExtra={u"MODO": u"lista", u"TITULO": u"OS SUBSTANTIVOS DA CARTA",
                u"LETRAS": LETRAS, u"DIFICIL": u"",
                u"CORP": [u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
# AQUECIMENTO 1 (idx 10, ~32%) — revisão do SUBSTANTIVO por 'ligar'.
# ============================================================
add(id=u"aquecimento1", mec=u"ligar", selo=u"AQUECIMENTO 1 DA REDAÇÃO", conceito=u"objetivo2",
    enunciado=u"<b>Aquecimento!</b> Ligue cada <b>substantivo</b> ao tipo de nome que ele é.",
    dica=u"Substantivo nomeia seres, coisas, lugares e pessoas. Do que cada um é nome?",
    dados=[{u"k": u"p0", u"t": u"GATO", u"s": u"um animal"},
           {u"k": u"p1", u"t": u"ESCOLA", u"s": u"um lugar"},
           {u"k": u"p2", u"t": u"LÉO", u"s": u"uma pessoa"},
           {u"k": u"p3", u"t": u"BOLO", u"s": u"uma coisa"}],
    dadosExtra={u"DICAS": [u"Pense: isso é bicho, lugar, gente ou objeto?",
                          u"GATO é bicho; ESCOLA é lugar; LÉO é gente; BOLO é objeto.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS": [], u"ENUN": u"Ligue o substantivo ao tipo de nome que ele é.",
                u"FECHO": u"Aquecido! Os substantivos estão na ponta da língua."})

# ============================================================
# BLOCO 3 — quem-sou-eu (idx 11-13): reconhecer o GÊNERO pelas pistas (obj1).
# ============================================================
add(id=u"f11", mec=u"quem-sou-eu", selo=u"QUE GÊNERO É ESTE? (1)", conceito=u"objetivo1",
    enunciado=u"Ouça as pistas e descubra <b>qual é o gênero</b> do texto.",
    dica=u"Junte as três pistas antes de responder.",
    dados=[
      {u"resp": u"A RECEITA", u"pistas": [
         u"Eu ensino a fazer um prato, <b>passo a passo</b>.",
         u"Tenho uma lista de <b>ingredientes</b> no come&#231;o.",
         u"No fim, voc&#234; <b>prova</b> o que preparou."],
       u"outros": [u"O POEMA", u"A NOT&#205;CIA", u"O BILHETE"]},
      {u"resp": u"O BILHETE", u"pistas": [
         u"Eu sou <b>curtinho</b> e escrito &#224; m&#227;o.",
         u"Deixo um <b>recado r&#225;pido</b> para algu&#233;m da casa.",
         u"Termino com um 'beijos' e o <b>nome</b> de quem escreveu."],
       u"outros": [u"A RECEITA", u"A F&#193;BULA", u"O CARTAZ"]},
      {u"resp": u"A F&#193;BULA", u"pistas": [
         u"Eu conto uma historinha com <b>animais que falam</b>.",
         u"No fim, deixo uma <b>li&#231;&#227;o de moral</b>.",
         u"A lebre e a tartaruga est&#227;o numa das minhas."],
       u"outros": [u"O AVISO", u"A LISTA", u"O CONVITE"]},
    ])

add(id=u"f12", mec=u"quem-sou-eu", selo=u"QUE GÊNERO É ESTE? (2)", conceito=u"objetivo1",
    enunciado=u"Mais pistas! Descubra <b>qual é o gênero</b> do texto.",
    dica=u"Junte as três pistas antes de responder.",
    dados=[
      {u"resp": u"O POEMA", u"pistas": [
         u"Eu sou escrito em <b>versos</b>, um embaixo do outro.",
         u"Muitas vezes tenho <b>rimas</b> no fim das linhas.",
         u"Falo com <b>imagens bonitas</b>: o sol dourado, a tarde calma."],
       u"outros": [u"A LISTA", u"O AVISO", u"A RECEITA"]},
      {u"resp": u"O CONVITE", u"pistas": [
         u"Eu chamo voc&#234; para uma <b>festa</b>.",
         u"Digo o <b>dia, a hora e o lugar</b>.",
         u"Termino com 'n&#227;o falte!'."],
       u"outros": [u"O BILHETE", u"A CARTA", u"A NOT&#205;CIA"]},
      {u"resp": u"A NOT&#205;CIA", u"pistas": [
         u"Eu conto um <b>fato que aconteceu de verdade</b>.",
         u"Digo <b>o qu&#234;, quando e onde</b> aconteceu.",
         u"Sa&#237;o no jornal e no telejornal."],
       u"outros": [u"O POEMA", u"A F&#193;BULA", u"A ADIVINHA"]},
    ])

add(id=u"f13", mec=u"quem-sou-eu", selo=u"QUE GÊNERO É ESTE? (3)", conceito=u"objetivo1",
    enunciado=u"Últimas pistas! Descubra <b>qual é o gênero</b> do texto.",
    dica=u"Junte as três pistas antes de responder.",
    dados=[
      {u"resp": u"A LISTA", u"pistas": [
         u"Eu enumero <b>coisas</b>, uma embaixo da outra.",
         u"Sirvo para <b>n&#227;o esquecer</b> o que comprar ou levar.",
         u"Arroz, feij&#227;o, p&#227;o e leite podem estar em mim."],
       u"outros": [u"O POEMA", u"A F&#193;BULA", u"A CARTA"]},
      {u"resp": u"O AVISO", u"pistas": [
         u"Eu fico no <b>mural</b> para todos lerem.",
         u"Comunico algo <b>importante</b>: 'Aten&#231;&#227;o!'.",
         u"Costumo ser assinado pela <b>dire&#231;&#227;o</b>."],
       u"outros": [u"O BILHETE", u"O POEMA", u"A RECEITA"]},
      {u"resp": u"A ADIVINHA", u"pistas": [
         u"Eu fa&#231;o uma <b>pergunta com um enigma</b>.",
         u"Voc&#234; tem que <b>descobrir a resposta</b>.",
         u"'O que &#233;, o que &#233;?' come&#231;a comigo."],
       u"outros": [u"A NOT&#205;CIA", u"A LISTA", u"O CONVITE"]},
    ])

# ============================================================
# BLOCO 4 — ligar (idx 14-16): cada ADJETIVO ao SUBSTANTIVO que descreve
#           (obj3), gêneros poema, tirinha e anúncio.
# ============================================================
add(id=u"f14", mec=u"ligar", selo=u"MATÉRIA 7 · O POEMA", conceito=u"objetivo3",
    enunciado=(u"No <b>poema</b>: <i>“O sol dourado acorda o dia. A flor pequena abre o "
               u"sorriso. O vento leve conta segredos e a tarde calma vira poesia.”</i> "
               u"Ligue cada <b>adjetivo</b> ao substantivo que ele descreve."),
    dica=u"O adjetivo diz COMO é o substantivo. Qual palavra ele qualifica?",
    dados=[{u"k": u"p0", u"t": u"DOURADO", u"s": u"o sol"},
           {u"k": u"p1", u"t": u"PEQUENA", u"s": u"a flor"},
           {u"k": u"p2", u"t": u"LEVE", u"s": u"o vento"},
           {u"k": u"p3", u"t": u"CALMA", u"s": u"a tarde"}],
    dadosExtra={u"DICAS": [u"Diga baixinho: 'o sol é…?', 'a flor é…?'.",
                          u"Dourado combina com sol; pequena com flor; leve com vento.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS": [], u"ENUN": u"Ligue cada adjetivo ao substantivo que ele descreve.",
                u"FECHO": u"Cada qualidade no seu nome certo!"})

add(id=u"f15", mec=u"ligar", selo=u"MATÉRIA 8 · A TIRINHA", conceito=u"objetivo3",
    enunciado=(u"Na <b>tirinha</b>: <i>“O cachorro molhado entra em casa. O menino "
               u"assustado corre. A poça enorme deixa o tapete sujo.”</i> Ligue cada "
               u"<b>adjetivo</b> ao substantivo que ele descreve."),
    dica=u"O adjetivo diz como está cada um. Quem está molhado? Quem, assustado?",
    dados=[{u"k": u"p0", u"t": u"MOLHADO", u"s": u"o cachorro"},
           {u"k": u"p1", u"t": u"ASSUSTADO", u"s": u"o menino"},
           {u"k": u"p2", u"t": u"ENORME", u"s": u"a poça"},
           {u"k": u"p3", u"t": u"SUJO", u"s": u"o tapete"}],
    dadosExtra={u"DICAS": [u"Diga: 'o cachorro está…?', 'o menino está…?'.",
                          u"Molhado é do cachorro; assustado, do menino; enorme, da poça.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS": [], u"ENUN": u"Ligue cada adjetivo ao substantivo que ele descreve.",
                u"FECHO": u"Você leu a tirinha e ligou as qualidades!"})

add(id=u"f16", mec=u"ligar", selo=u"MATÉRIA 9 · O ANÚNCIO", conceito=u"objetivo3",
    enunciado=(u"No <b>anúncio</b>: <i>“Sorvete cremoso, fruta fresca e preço baixo! "
               u"Venha à sorveteria nova da esquina.”</i> Ligue cada <b>adjetivo</b> ao "
               u"substantivo que ele descreve."),
    dica=u"O anúncio usa adjetivos para elogiar. Cada qualidade é de qual coisa?",
    dados=[{u"k": u"p0", u"t": u"CREMOSO", u"s": u"o sorvete"},
           {u"k": u"p1", u"t": u"FRESCA", u"s": u"a fruta"},
           {u"k": u"p2", u"t": u"BAIXO", u"s": u"o preço"},
           {u"k": u"p3", u"t": u"NOVA", u"s": u"a sorveteria"}],
    dadosExtra={u"DICAS": [u"Diga: 'o sorvete é…?', 'a fruta é…?'.",
                          u"Cremoso é do sorvete; fresca, da fruta; baixo, do preço.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS": [], u"ENUN": u"Ligue cada adjetivo ao substantivo que ele descreve.",
                u"FECHO": u"Anúncio pronto — e os adjetivos, no lugar!"})

# ============================================================
# BLOCO 5 — completar (idx 17-20): marcar o VERBO (a ação) que falta (obj4),
#           gêneros receita, receita, notícia e regras de jogo. As opções
#           erradas são de OUTRAS classes (substantivo/adjetivo).
# ============================================================
add(id=u"f17", mec=u"completar", selo=u"MATÉRIA 10 · A RECEITA DO BOLO", conceito=u"objetivo4",
    enunciado=u"Nesta <b>receita</b>, preencha cada passo com o <b>VERBO</b> (a ação) certo.",
    dica=u"O que falta é a AÇÃO — o verbo que MANDA fazer: bata, misture, corte.",
    dados=[{u"img": u"", u"ante": u"Primeiro, ", u"dep": u" os ovos na tigela.",
            u"cer": u"bata", u"out": [u"tigela", u"doce"], u"dic": u"Falta a AÇÃO (verbo): 'bata'."},
           {u"img": u"", u"ante": u"Depois, ", u"dep": u" a farinha aos poucos.",
            u"cer": u"misture", u"out": [u"colher", u"macio"], u"dic": u"A ação de juntar: 'misture'."},
           {u"img": u"", u"ante": u"Em seguida, ", u"dep": u" a massa no forno.",
            u"cer": u"leve", u"out": [u"forno", u"quente"], u"dic": u"A ação de pôr no forno: 'leve'."},
           {u"img": u"", u"ante": u"Por fim, ", u"dep": u" o bolo em fatias.",
            u"cer": u"corte", u"out": [u"faca", u"gostoso"], u"dic": u"A ação: 'corte'."}],
    dadosExtra={u"ENUN": u"Toque no <b>verbo</b> que falta no passo.",
                u"DEPOIS": u"Leia o passo inteiro antes de escolher.",
                u"FECHO": u"Você achou as ações da receita!"})

add(id=u"f18", mec=u"completar", selo=u"MATÉRIA 11 · A RECEITA DO SUCO", conceito=u"objetivo4",
    enunciado=u"Mais uma <b>receita</b>: preencha cada passo com o <b>VERBO</b> (a ação) certo.",
    dica=u"O verbo é a AÇÃO que a receita manda fazer.",
    dados=[{u"img": u"", u"ante": u"Para o suco, ", u"dep": u" as laranjas.",
            u"cer": u"esprema", u"out": [u"copo", u"azedo"], u"dic": u"A ação de apertar a fruta: 'esprema'."},
           {u"img": u"", u"ante": u"Depois, ", u"dep": u" um pouco de água.",
            u"cer": u"adicione", u"out": [u"jarra", u"gelada"], u"dic": u"A ação de pôr mais: 'adicione'."},
           {u"img": u"", u"ante": u"Se quiser, ", u"dep": u" com açúcar.",
            u"cer": u"adoce", u"out": [u"colher", u"doce"], u"dic": u"A ação de deixar doce: 'adoce'."},
           {u"img": u"", u"ante": u"No fim, ", u"dep": u" o suco bem geladinho.",
            u"cer": u"sirva", u"out": [u"gelo", u"fresco"], u"dic": u"A ação de levar à mesa: 'sirva'."}],
    dadosExtra={u"ENUN": u"Toque no <b>verbo</b> que falta no passo.",
                u"DEPOIS": u"Leia o passo inteiro antes de escolher.",
                u"FECHO": u"Suco pronto — e os verbos, também!"})

add(id=u"f19", mec=u"completar", selo=u"MATÉRIA 12 · A NOTÍCIA DA CIDADE", conceito=u"objetivo4",
    enunciado=u"Nesta <b>notícia</b>, preencha cada frase com o <b>VERBO</b> (a ação) certo.",
    dica=u"O verbo conta o que ALGUÉM fez: consertou, plantou, salvou.",
    dados=[{u"img": u"", u"ante": u"Os moradores ", u"dep": u" a ponte quebrada ontem.",
            u"cer": u"consertaram", u"out": [u"ponte", u"estreita"], u"dic": u"O que os moradores FIZERAM: 'consertaram'."},
           {u"img": u"", u"ante": u"A prefeitura ", u"dep": u" árvores novas na praça.",
            u"cer": u"plantou", u"out": [u"praça", u"verdes"], u"dic": u"A ação da prefeitura: 'plantou'."},
           {u"img": u"", u"ante": u"A chuva forte ", u"dep": u" as ruas do centro.",
            u"cer": u"alagou", u"out": [u"ruas", u"molhadas"], u"dic": u"O que a chuva fez: 'alagou'."},
           {u"img": u"", u"ante": u"Os bombeiros ", u"dep": u" o gato do telhado.",
            u"cer": u"salvaram", u"out": [u"telhado", u"alto"], u"dic": u"A ação dos bombeiros: 'salvaram'."}],
    dadosExtra={u"ENUN": u"Toque no <b>verbo</b> que falta na frase.",
                u"DEPOIS": u"Leia a frase inteira antes de escolher.",
                u"FECHO": u"Você achou as ações da notícia!"})

add(id=u"f20", mec=u"completar", selo=u"MATÉRIA 13 · AS REGRAS DO JOGO", conceito=u"objetivo4",
    enunciado=u"Nas <b>regras do jogo</b>, preencha cada linha com o <b>VERBO</b> (a ação) certo.",
    dica=u"As regras dizem o que cada jogador FAZ: joga, vence, perde.",
    dados=[{u"img": u"", u"ante": u"Cada jogador ", u"dep": u" o dado na sua vez.",
            u"cer": u"joga", u"out": [u"dado", u"redondo"], u"dic": u"A ação do jogador: 'joga'."},
           {u"img": u"", u"ante": u"Quem chegar primeiro ", u"dep": u" a partida.",
            u"cer": u"vence", u"out": [u"partida", u"difícil"], u"dic": u"A ação de ganhar: 'vence'."},
           {u"img": u"", u"ante": u"Se errar, o jogador ", u"dep": u" uma rodada.",
            u"cer": u"perde", u"out": [u"rodada", u"curta"], u"dic": u"A ação contrária de ganhar: 'perde'."},
           {u"img": u"", u"ante": u"No fim, o vencedor ", u"dep": u" o troféu.",
            u"cer": u"ganha", u"out": [u"troféu", u"dourado"], u"dic": u"A ação de receber o prêmio: 'ganha'."}],
    dadosExtra={u"ENUN": u"Toque no <b>verbo</b> que falta na regra.",
                u"DEPOIS": u"Leia a regra inteira antes de escolher.",
                u"FECHO": u"Você achou as ações das regras!"})

# ============================================================
# BLOCO 6 — linha-do-tempo (idx 21-22): ORDENAR a sequência (obj1) — os PASSOS
#           de uma dobradura (injuntivo) e os FATOS de uma fábula (narrativo).
# ============================================================
add(id=u"f21", mec=u"linha-do-tempo", selo=u"MATÉRIA 14 · A DOBRADURA", conceito=u"objetivo1",
    enunciado=u"Estas <b>instruções</b> ensinam a dobrar um chapéu de papel. Ponha os <b>passos</b> na ordem.",
    dica=u"Texto de instrução dá os passos em ordem: o que se faz primeiro de tudo?",
    dados=[{u"t": 1, u"n": u"Pegue uma folha de papel quadrada."},
           {u"t": 2, u"n": u"Dobre a folha ao meio."},
           {u"t": 3, u"n": u"Dobre as duas pontas de cima para o centro."},
           {u"t": 4, u"n": u"Levante a aba de baixo dos dois lados."},
           {u"t": 5, u"n": u"Abra e ponha o chap&#233;u na cabe&#231;a."}])

add(id=u"f22", mec=u"linha-do-tempo", selo=u"MATÉRIA 15 · A FÁBULA", conceito=u"objetivo1",
    enunciado=u"Esta <b>fábula</b> conta a história da cigarra e da formiga. Ponha os <b>fatos</b> na ordem.",
    dica=u"Pense: o que veio primeiro? O que aconteceu por último?",
    dados=[{u"t": 1, u"n": u"A cigarra cantou o ver&#227;o inteiro."},
           {u"t": 2, u"n": u"A formiga guardou comida para o inverno."},
           {u"t": 3, u"n": u"Chegou o inverno gelado."},
           {u"t": 4, u"n": u"A cigarra, com fome, pediu ajuda."},
           {u"t": 5, u"n": u"A formiga ensinou o valor do trabalho."}])

# ============================================================
# AQUECIMENTO 2 (idx 23, ~68%) — revisão do ADJETIVO por 'caça-palavras'.
# ============================================================
add(id=u"aquecimento2", mec=u"caca-palavras", selo=u"AQUECIMENTO 2 DA REDAÇÃO", conceito=u"objetivo3",
    enunciado=u"<b>Aquecimento!</b> Ache no quadro os <b>ADJETIVOS</b> (palavras que dizem uma qualidade).",
    dica=u"Adjetivo diz COMO é: alegre, bonito, novo. Estão deitados (→) e em pé (↓).",
    dados=[u"ALEGRE", u"BONITO", u"DOCE", u"FRESCO", u"NOVO"],
    dadosExtra={u"MODO": u"lista", u"TITULO": u"OS ADJETIVOS",
                u"LETRAS": LETRAS, u"DIFICIL": u"",
                u"CORP": [u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
# BLOCO 7 — intruso (idx 24-26): qual palavra NÃO é da classe (obj4/obj2),
#           gêneros propaganda, fábula e verbete.
# ============================================================
add(id=u"f23", mec=u"intruso", selo=u"MATÉRIA 16 · A PROPAGANDA", conceito=u"objetivo4",
    enunciado=u"Três palavras da propaganda são <b>VERBOS</b> (ações). <b>Qual NÃO é verbo?</b>",
    dica=u"Verbo é ação: compre, aproveite, corra. O que não é ação é intruso.",
    dados=[
      {u"selo": u"AS PALAVRAS DA PROPAGANDA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"COMPRE"}, {u"k": u"b", u"n": u"APROVEITE"},
                  {u"k": u"c", u"n": u"CORRA"}, {u"k": u"d", u"n": u"OFERTA"}],
       u"fora": u"d", u"nomeFora": u"OFERTA",
       u"d1": u"Leia as quatro. Três MANDAM fazer algo; uma é só o nome de uma coisa.",
       u"d2": u"COMPRE, APROVEITE e CORRA são ações. OFERTA é o nome de uma promoção.",
       u"d3": u"A de fora é <b>OFERTA</b>: é um substantivo (nome de coisa), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta é nome de coisa (substantivo).", u"ok": 1},
                   {u"t": u"Porque ela é a mais curta.", u"ok": 0},
                   {u"t": u"Porque ela aparece na loja.", u"ok": 0},
                   {u"t": u"Porque ela termina em A.", u"ok": 0}],
       u"enunPorque": u"O que <b>OFERTA</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três mandam fazer.",
       u"p2": u"Compre, aproveite, corra são AÇÕES. Oferta é uma COISA.",
       u"p3": u"“Oferta” nomeia uma coisa (substantivo); as outras são verbos.",
       u"regra": u"verbo é ação; substantivo é nome de coisa"},
      {u"selo": u"AS PALAVRAS DA PROPAGANDA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"LEVE"}, {u"k": u"b", u"n": u"GANHE"},
                  {u"k": u"c", u"n": u"DESCONTO"}, {u"k": u"d", u"n": u"ECONOMIZE"}],
       u"fora": u"c", u"nomeFora": u"DESCONTO",
       u"d1": u"Leia as quatro. Três MANDAM fazer algo; uma é só o nome de uma coisa.",
       u"d2": u"LEVE, GANHE e ECONOMIZE são ações. DESCONTO é o nome de um abatimento.",
       u"d3": u"A de fora é <b>DESCONTO</b>: é um substantivo (nome de coisa), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta é nome de coisa (substantivo).", u"ok": 1},
                   {u"t": u"Porque ela fala de dinheiro.", u"ok": 0},
                   {u"t": u"Porque ela é a maior.", u"ok": 0},
                   {u"t": u"Porque ela começa com D.", u"ok": 0}],
       u"enunPorque": u"O que <b>DESCONTO</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três mandam fazer.",
       u"p2": u"Leve, ganhe, economize são AÇÕES. Desconto é uma COISA.",
       u"p3": u"“Desconto” nomeia uma coisa (substantivo); as outras são verbos.",
       u"regra": u"verbo é ação; substantivo é nome de coisa"},
    ])

add(id=u"f24", mec=u"intruso", selo=u"MATÉRIA 17 · A FÁBULA", conceito=u"objetivo4",
    enunciado=u"Na <b>fábula</b>, três palavras são <b>VERBOS</b> (ações). <b>Qual NÃO é verbo?</b>",
    dica=u"Verbo é ação: rugiu, correu, caçou. Adjetivo diz uma qualidade.",
    dados=[
      {u"selo": u"AS PALAVRAS DA FÁBULA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações do leão (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"RUGIU"}, {u"k": u"b", u"n": u"CORREU"},
                  {u"k": u"c", u"n": u"CAÇOU"}, {u"k": u"d", u"n": u"ESPERTO"}],
       u"fora": u"d", u"nomeFora": u"ESPERTO",
       u"d1": u"Leia as quatro. Três dizem o que o leão FEZ; uma diz COMO ele é.",
       u"d2": u"RUGIU, CORREU e CAÇOU são ações. ESPERTO é uma qualidade do leão.",
       u"d3": u"A de fora é <b>ESPERTO</b>: é um adjetivo (qualidade), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta diz uma qualidade (adjetivo).", u"ok": 1},
                   {u"t": u"Porque ela fala do leão.", u"ok": 0},
                   {u"t": u"Porque ela é a mais curta.", u"ok": 0},
                   {u"t": u"Porque ela termina em O.", u"ok": 0}],
       u"enunPorque": u"O que <b>ESPERTO</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três dizem: ações que o leão fez.",
       u"p2": u"Rugiu, correu, caçou são AÇÕES. Esperto é uma QUALIDADE.",
       u"p3": u"“Esperto” é adjetivo (qualidade); as outras são verbos (ações).",
       u"regra": u"verbo é ação; adjetivo é qualidade"},
      {u"selo": u"AS PALAVRAS DA FÁBULA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações do rato (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"ROEU"}, {u"k": u"b", u"n": u"FUGIU"},
                  {u"k": u"c", u"n": u"PEQUENO"}, {u"k": u"d", u"n": u"PULOU"}],
       u"fora": u"c", u"nomeFora": u"PEQUENO",
       u"d1": u"Leia as quatro. Três dizem o que o rato FEZ; uma diz COMO ele é.",
       u"d2": u"ROEU, FUGIU e PULOU são ações. PEQUENO é uma qualidade do rato.",
       u"d3": u"A de fora é <b>PEQUENO</b>: é um adjetivo (qualidade), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta diz uma qualidade (adjetivo).", u"ok": 1},
                   {u"t": u"Porque ela fala do rato.", u"ok": 0},
                   {u"t": u"Porque ela é a maior palavra.", u"ok": 0},
                   {u"t": u"Porque ela tem a letra P.", u"ok": 0}],
       u"enunPorque": u"O que <b>PEQUENO</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três dizem: ações que o rato fez.",
       u"p2": u"Roeu, fugiu, pulou são AÇÕES. Pequeno é uma QUALIDADE.",
       u"p3": u"“Pequeno” é adjetivo (qualidade); as outras são verbos (ações).",
       u"regra": u"verbo é ação; adjetivo é qualidade"},
    ])

add(id=u"f25", mec=u"intruso", selo=u"MATÉRIA 18 · O VERBETE", conceito=u"objetivo2",
    enunciado=u"Num <b>verbete</b> de dicionário, três palavras são <b>SUBSTANTIVOS</b>. <b>Qual NÃO é substantivo?</b>",
    dica=u"Substantivo é nome; adjetivo diz uma qualidade.",
    dados=[
      {u"selo": u"O VERBETE: GATO", u"tipo": u"texto",
       u"enun": u"Verbete — <i>gato: animal de pelo macio</i>. Três são nomes (substantivos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"GATO"}, {u"k": u"b", u"n": u"ANIMAL"},
                  {u"k": u"c", u"n": u"PELO"}, {u"k": u"d", u"n": u"MACIO"}],
       u"fora": u"d", u"nomeFora": u"MACIO",
       u"d1": u"Leia as quatro. Três são NOMES de coisas/seres; uma diz COMO é o pelo.",
       u"d2": u"GATO, ANIMAL e PELO são nomes. MACIO diz uma qualidade do pelo.",
       u"d3": u"A de fora é <b>MACIO</b>: é um adjetivo (qualidade), não um nome.",
       u"razoes": [{u"t": u"As outras são nomes (substantivos); esta diz uma qualidade (adjetivo).", u"ok": 1},
                   {u"t": u"Porque ela fala do gato.", u"ok": 0},
                   {u"t": u"Porque ela é a mais curta.", u"ok": 0},
                   {u"t": u"Porque ela termina em O.", u"ok": 0}],
       u"enunPorque": u"O que <b>MACIO</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três nomeiam.",
       u"p2": u"Gato, animal, pelo são NOMES. Macio é uma QUALIDADE.",
       u"p3": u"“Macio” é adjetivo (qualidade); as outras são substantivos (nomes).",
       u"regra": u"substantivo é nome; adjetivo é qualidade"},
      {u"selo": u"O VERBETE: RIO", u"tipo": u"texto",
       u"enun": u"Verbete — <i>rio: curso de água comprido</i>. Três são nomes (substantivos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"RIO"}, {u"k": u"b", u"n": u"CURSO"},
                  {u"k": u"c", u"n": u"COMPRIDO"}, {u"k": u"d", u"n": u"ÁGUA"}],
       u"fora": u"c", u"nomeFora": u"COMPRIDO",
       u"d1": u"Leia as quatro. Três são NOMES; uma diz COMO é o rio.",
       u"d2": u"RIO, CURSO e ÁGUA são nomes. COMPRIDO diz uma qualidade do rio.",
       u"d3": u"A de fora é <b>COMPRIDO</b>: é um adjetivo (qualidade), não um nome.",
       u"razoes": [{u"t": u"As outras são nomes (substantivos); esta diz uma qualidade (adjetivo).", u"ok": 1},
                   {u"t": u"Porque ela fala do rio.", u"ok": 0},
                   {u"t": u"Porque ela é a maior.", u"ok": 0},
                   {u"t": u"Porque ela começa com C.", u"ok": 0}],
       u"enunPorque": u"O que <b>COMPRIDO</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três nomeiam.",
       u"p2": u"Rio, curso, água são NOMES. Comprido é uma QUALIDADE.",
       u"p3": u"“Comprido” é adjetivo (qualidade); as outras são substantivos (nomes).",
       u"regra": u"substantivo é nome; adjetivo é qualidade"},
    ])

# ============================================================
# BLOCO 8 — digitar (idx 27-28): escrever a palavra da classe pedida,
#           letra por letra (obj2 e obj4), gêneros quadrinha e trava-língua.
# ============================================================
add(id=u"f26", mec=u"digitar", selo=u"MATÉRIA 19 · A QUADRINHA", conceito=u"objetivo2",
    enunciado=u"Na <b>quadrinha</b> <i>“A bota do bode caiu no rio fundo”</i>, escreva o <b>SUBSTANTIVO</b> pedido.",
    dica=u"Substantivo é o nome de uma coisa, um bicho ou um lugar. Escreva letra por letra.",
    dados=[{u"palavra": u"BOTA", u"img": u"", u"voz": u"bota",
            u"pista": u"O cal&#231;ado que caiu na quadrinha. Escreva o substantivo.",
            u"dic": u"É o nome de uma coisa: <b>BOTA</b>."},
           {u"palavra": u"BODE", u"img": u"", u"voz": u"bode",
            u"pista": u"O bicho dono da bota. Escreva o substantivo.",
            u"dic": u"É o nome de um animal: <b>BODE</b>."},
           {u"palavra": u"RIO", u"img": u"", u"voz": u"rio",
            u"pista": u"O lugar onde a bota caiu. Escreva o substantivo.",
            u"dic": u"É o nome de um lugar: <b>RIO</b>."}],
    dadosExtra={u"ENUN": u"Escreva o substantivo, letra por letra.",
                u"FECHO": u"Você escreveu os substantivos da quadrinha!"})

add(id=u"f27", mec=u"digitar", selo=u"MATÉRIA 20 · O TRAVA-LÍNGUA", conceito=u"objetivo4",
    enunciado=u"No <b>trava-língua</b> <i>“O pato pintou, nadou e voou”</i>, escreva o <b>VERBO</b> pedido.",
    dica=u"Verbo é a ação. Escreva letra por letra.",
    dados=[{u"palavra": u"NADOU", u"img": u"", u"voz": u"nadou",
            u"pista": u"O que o pato fez na &#225;gua. Escreva o verbo.",
            u"dic": u"É uma ação: <b>NADOU</b>."},
           {u"palavra": u"VOOU", u"img": u"", u"voz": u"voou",
            u"pista": u"O que o pato fez no ar. Escreva o verbo.",
            u"dic": u"É uma ação: <b>VOOU</b>."},
           {u"palavra": u"PINTOU", u"img": u"", u"voz": u"pintou",
            u"pista": u"O que o pato fez com a tinta. Escreva o verbo.",
            u"dic": u"É uma ação: <b>PINTOU</b>."}],
    dadosExtra={u"ENUN": u"Escreva o verbo, letra por letra.",
                u"FECHO": u"Você escreveu os verbos do trava-língua!"})

# ============================================================
# BLOCO 9 — classificar (idx 29-33): AS TRÊS CLASSES JUNTAS em 3 gavetas
#           (SUBSTANTIVO / ADJETIVO / VERBO) — o clímax "Edição Especial".
#           Palavras retiradas do texto; cada uma inequívoca.
# ============================================================
GAVETAS = [{u"k": u"sub", u"n": u"SUBSTANTIVO", u"img": u"", u"voz": u"substantivo", u"rot": False},
           {u"k": u"adj", u"n": u"ADJETIVO", u"img": u"", u"voz": u"adjetivo", u"rot": False},
           {u"k": u"verb", u"n": u"VERBO", u"img": u"", u"voz": u"verbo", u"rot": False}]
DICAS_CLASS = [u"Nome de coisa/ser vai em SUBSTANTIVO; qualidade em ADJETIVO; ação em VERBO.",
               u"Pergunte: é o nome de algo? é como algo é? ou é o que alguém faz?",
               u"Olhe a gaveta com a borda amarela: é ali que esta palavra mora."]
def classif(id_, num, genero, texto, fichas, conceito, extra_fecho=u""):
    add(id=id_, mec=u"classificar",
        selo=u"EDIÇÃO ESPECIAL " + num + u" · " + genero, conceito=conceito,
        enunciado=texto,
        dica=u"Substantivo = nome; adjetivo = qualidade; verbo = ação.",
        dados=GAVETAS,
        dadosExtra={u"FICHAS": fichas, u"DICAS": DICAS_CLASS,
                    u"ENUN": u"Toque na <b>palavra</b>. Depois toque na <b>gaveta da classe</b> dela."})

classif(u"f28", u"(1)", u"A FÁBULA",
    (u"Leia a <b>fábula</b>: <i>“O leão forte dormia. O rato pequeno correu e roeu a "
     u"rede.”</i> Cada palavra na sua gaveta: substantivo, adjetivo ou verbo?"),
    [{u"t": u"LEÃO", u"alvo": u"sub"}, {u"t": u"RATO", u"alvo": u"sub"},
     {u"t": u"FORTE", u"alvo": u"adj"}, {u"t": u"PEQUENO", u"alvo": u"adj"},
     {u"t": u"DORMIA", u"alvo": u"verb"}, {u"t": u"CORREU", u"alvo": u"verb"}],
    u"objetivo2")

classif(u"f29", u"(2)", u"A FÁBULA (parte 2)",
    (u"Continue a <b>fábula</b>: <i>“A formiga esperta guardou comida. A cigarra alegre "
     u"cantou o verão inteiro.”</i> Cada palavra na sua gaveta."),
    [{u"t": u"FORMIGA", u"alvo": u"sub"}, {u"t": u"CIGARRA", u"alvo": u"sub"},
     {u"t": u"ESPERTA", u"alvo": u"adj"}, {u"t": u"ALEGRE", u"alvo": u"adj"},
     {u"t": u"GUARDOU", u"alvo": u"verb"}, {u"t": u"CANTOU", u"alvo": u"verb"}],
    u"objetivo3")

classif(u"f30", u"(3)", u"A NOTÍCIA",
    (u"Leia a <b>notícia</b>: <i>“A cidade bonita ganhou uma praça. As crianças felizes "
     u"plantaram árvores.”</i> Cada palavra na sua gaveta."),
    [{u"t": u"CIDADE", u"alvo": u"sub"}, {u"t": u"CRIANÇAS", u"alvo": u"sub"},
     {u"t": u"BONITA", u"alvo": u"adj"}, {u"t": u"FELIZES", u"alvo": u"adj"},
     {u"t": u"GANHOU", u"alvo": u"verb"}, {u"t": u"PLANTARAM", u"alvo": u"verb"}],
    u"objetivo4")

classif(u"f31", u"(4)", u"O DIÁRIO",
    (u"Leia o <b>diário</b>: <i>“A turma animada visitou o museu antigo. A gente comprou "
     u"lembranças bonitas.”</i> Cada palavra na sua gaveta."),
    [{u"t": u"TURMA", u"alvo": u"sub"}, {u"t": u"MUSEU", u"alvo": u"sub"},
     {u"t": u"ANIMADA", u"alvo": u"adj"}, {u"t": u"ANTIGO", u"alvo": u"adj"},
     {u"t": u"VISITOU", u"alvo": u"verb"}, {u"t": u"COMPROU", u"alvo": u"verb"}],
    u"objetivo2")

classif(u"f32", u"(5)", u"A CARTA — CAPA DA EDIÇÃO",
    (u"Última matéria, a <b>carta</b> de capa: <i>“A carta carinhosa trouxe boas "
     u"notícias. A vovó querida escreveu e mandou um beijo.”</i> Cada palavra na sua gaveta."),
    [{u"t": u"CARTA", u"alvo": u"sub"}, {u"t": u"VOVÓ", u"alvo": u"sub"},
     {u"t": u"CARINHOSA", u"alvo": u"adj"}, {u"t": u"QUERIDA", u"alvo": u"adj"},
     {u"t": u"ESCREVEU", u"alvo": u"verb"}, {u"t": u"MANDOU", u"alvo": u"verb"}],
    u"objetivo3")


CONTEUDO[u"fases"] = fases
io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8").write(
    json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
print(u"conteudo.json: %d fases" % len(fases))
