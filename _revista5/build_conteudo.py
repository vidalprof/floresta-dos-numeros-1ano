# -*- coding: utf-8 -*-
u"""Gera _revista5/conteudo.json — A REVISTA DAS PALAVRAS (5º ano, Português).

FORMATO (escolha do Marcos, set/2026): "Revista de Gêneros + Marca-Classes".
A criança é repórter/editora da REVISTA DAS PALAVRAS. Cada MATÉRIA é um GÊNERO
textual (bilhete, convite, e-mail, poema, receita, tirinha, anúncio, notícia,
fábula). Para a matéria "fechar", ela precisa (1) LER e INTERPRETAR o texto e
(2) MARCAR as palavras que são SUBSTANTIVO, ADJETIVO e VERBO — retiradas do
PRÓPRIO texto. O problema (fechar a revista) vem ANTES do conceito (as classes).

OBJETIVOS (o que a criança treina):
  · objetivo1 — LER e INTERPRETAR diferentes GÊNEROS textuais;
  · objetivo2 — identificar SUBSTANTIVO (nomes de seres, coisas e lugares);
  · objetivo3 — identificar ADJETIVO (as qualidades);
  · objetivo4 — identificar VERBO (as ações).

PROGRESSÃO (concreto → figural → simbólico; uma classe por vez e depois juntar):
  1) SUBSTANTIVO sozinho, nos gêneros mais simples (bilhete, convite, e-mail);
  2) ADJETIVO (poema, tirinha, anúncio);
  3) VERBO (receita, notícia);
  4) AS TRÊS JUNTAS — classificar em 3 gavetas (fábula, notícia) = clímax.
  AQUECIMENTO (revisão espaçada) no MEIO (~45%), revendo SUBSTANTIVO por um
  gesto diferente (ligar).

REPETIÇÃO SEGUIDA, NÃO ESPAÇADA (regra do Marcos): cada mecânica vem em BLOCO
contíguo, subindo um degrau. Único reuso fora do bloco = o AQUECIMENTO.

  idx  gênero        gesto          o que treina
   0   bilhete       escolher       interpretar (obj1)
   1   bilhete       escolher       marcar SUBSTANTIVO (obj2)
   2   convite       escolher       interpretar (obj1)
   3   convite       escolher       marcar SUBSTANTIVO (obj2)
   4   poema         escolher       interpretar (obj1)
   5   poema         escolher       marcar ADJETIVO (obj3)
   6   e-mail        caca-palavras  achar os SUBSTANTIVOS (obj2)
   7   notícia       caca-palavras  achar os SUBSTANTIVOS (obj2)
   8   —             ligar (AQUEC)  revisão: substantivo -> tipo (obj2)
   9   receita       completar      marcar o VERBO/ação (obj4)
  10   receita(suco) completar      marcar o VERBO/ação (obj4)
  11   notícia       completar      marcar o VERBO/ação (obj4)
  12   poema         ligar          adjetivo -> substantivo que descreve (obj3)
  13   tirinha       ligar          adjetivo -> substantivo (obj3)
  14   anúncio       ligar          adjetivo -> substantivo (obj3)
  15   receita       intruso        qual NÃO é verbo (obj4)
  16   fábula        intruso        qual NÃO é verbo (obj4)
  17   fábula        classificar    3 gavetas: subst/adj/verbo (obj2)
  18   fábula        classificar    3 gavetas (obj3)
  19   notícia       classificar    3 gavetas — clímax (obj4)

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
 u"mascoteNome": u"Filó",   # MESMO mascote/arte da Detetive (raposa Filó), reaproveitado (regra do banco). Sem o título "Detetive" (aqui ela é a editora), o que também deixa o clone.py verde.
 u"crachas": 6,
 u"mesa": (u"Pedagogo do 5º ano + especialista em Língua Portuguesa (leitura de "
           u"gêneros textuais e classes de palavras: substantivo, adjetivo e verbo)."),
 u"fundo": u"rv_fundo.png",
 u"voz": u"feminina",
 u"abertura": (u"Bem-vindo(a) à redação da Revista das Palavras! Sou a Filó, a "
               u"editora-chefe. Cada matéria só fecha quando lemos com atenção e "
               u"marcamos as palavras certas. Vamos preparar a próxima edição?"),
 u"fim": (u"Edição fechada, repórter! Você lê cada gênero e sabe achar os "
          u"substantivos, os adjetivos e os verbos onde eles se escondem."),
 u"conceitos": {
   u"objetivo1": u"Ler e entender bilhete, convite, e-mail, receita, notícia, poema, tirinha e fábula",
   u"objetivo2": u"Achar os SUBSTANTIVOS (nomes de seres, coisas e lugares)",
   u"objetivo3": u"Achar os ADJETIVOS (as qualidades)",
   u"objetivo4": u"Achar os VERBOS (as ações)",
 },
 u"curriculo": {
   u"objetivo1": (u"Ler e compreender, com autonomia, textos de diferentes gêneros "
                  u"(bilhete, convite, e-mail, receita, notícia, poema, tirinha e fábula), "
                  u"localizando informações explícitas e inferindo sentidos. EF35LP03/EF35LP04/EF05LP01."),
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
# BLOCO 1 — escolher (idx 0-5): SUBSTANTIVO e ADJETIVO, uma classe por vez,
#           nos gêneros mais simples. Interpretar (obj1) + marcar a classe.
# ============================================================

# --- BILHETE ---
BILHETE = u"<i>“Mãe, guardei o bolo de chocolate na geladeira. Não conte para a Bia! Volto às cinco horas. Beijos, Léo.”</i>"

add(id=u"f01", mec=u"escolher", selo=u"MATÉRIA 1: O BILHETE", conceito=u"objetivo1",
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

add(id=u"f02", mec=u"escolher", selo=u"MATÉRIA 1: MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
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

# --- CONVITE ---
CONVITE = u"<i>“Você está convidado para a minha festa de aniversário! Vai ser no sábado, às três horas da tarde, no salão do prédio. Vamos ter bolo, música e muitas brincadeiras. Não falte! Duda.”</i>"

add(id=u"f03", mec=u"escolher", selo=u"MATÉRIA 2: O CONVITE", conceito=u"objetivo1",
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

add(id=u"f04", mec=u"escolher", selo=u"MATÉRIA 2: MARQUE O SUBSTANTIVO", conceito=u"objetivo2",
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

# --- POEMA ---
POEMA = (u"<i>“O sol dourado acorda o dia. / A flor pequena abre o sorriso. / "
         u"O vento leve conta segredos / e a tarde calma vira poesia.”</i>")

add(id=u"f05", mec=u"escolher", selo=u"MATÉRIA 3: O POEMA", conceito=u"objetivo1",
    enunciado=u"Leia o <b>poema</b> e responda sobre o que ele conta.",
    dica=u"O poema descreve com imagens bonitas. Leia devagar e imagine.",
    dados=[
      esc(u"Leia o poema: " + POEMA + u" Sobre o que o poema fala?",
          u"Um dia bonito na natureza", [u"Uma festa de aniversário", u"Uma viagem de carro"],
          [u"Ele fala de sol, flor, vento e tarde.", u"Tudo isso é a <b>natureza</b> num dia bonito.",
           u"É <b>um dia bonito na natureza</b>. Toque para seguir."]),
      esc(u"No poema, quem “acorda o dia”?",
          u"O sol", [u"A flor", u"O vento"],
          [u"Leia o primeiro verso.", u"“O <b>sol</b> dourado acorda o dia.”",
           u"É <b>o sol</b>. Toque para seguir."]),
      esc(u"O que a flor faz no poema?",
          u"Abre o sorriso", [u"Conta segredos", u"Vira poesia"],
          [u"Leia o segundo verso.", u"“A flor pequena <b>abre o sorriso</b>.”",
           u"É <b>abre o sorriso</b>. Toque para seguir."]),
      esc(u"Que sentimento o poema passa?",
          u"Calma e alegria", [u"Medo e susto", u"Raiva e pressa"],
          [u"Pense no clima das palavras: leve, calma, sorriso.", u"São palavras de <b>paz e alegria</b>.",
           u"É <b>calma e alegria</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"O POEMA", u"FECHO": u"Você sentiu o poema por dentro!"})

add(id=u"f06", mec=u"escolher", selo=u"MATÉRIA 3: MARQUE O ADJETIVO", conceito=u"objetivo3",
    enunciado=u"No poema, marque as palavras que são <b>ADJETIVO</b> (dizem uma qualidade).",
    dica=u"Adjetivo diz COMO é: bonito, pequeno, leve, calmo.",
    dados=[
      esc(u"“O sol <b>dourado</b> acorda o dia.” Qual palavra é ADJETIVO (diz como é o sol)?",
          u"dourado", [u"sol", u"acorda"],
          [u"Qual palavra diz a COR/qualidade do sol?",
           u"<b>sol</b> é o nome (substantivo); <b>acorda</b> é a ação (verbo).",
           u"É <b>dourado</b> — a qualidade do sol. Toque para seguir."]),
      esc(u"“A flor <b>pequena</b> abre o sorriso.” Qual é o ADJETIVO?",
          u"pequena", [u"flor", u"abre"],
          [u"Qual palavra diz o TAMANHO da flor?",
           u"<b>flor</b> é o nome; <b>abre</b> é a ação.",
           u"É <b>pequena</b> — a qualidade da flor. Toque para seguir."]),
      esc(u"“O vento <b>leve</b> conta segredos.” Qual palavra descreve o vento (adjetivo)?",
          u"leve", [u"vento", u"conta"],
          [u"Qual palavra diz como é o vento?",
           u"<b>vento</b> é o nome; <b>conta</b> é a ação.",
           u"É <b>leve</b> — a qualidade do vento. Toque para seguir."]),
      esc(u"“E a tarde <b>calma</b> vira poesia.” Qual é o ADJETIVO?",
          u"calma", [u"tarde", u"vira"],
          [u"Qual palavra diz como está a tarde?",
           u"<b>tarde</b> é o nome; <b>vira</b> é a ação.",
           u"É <b>calma</b> — a qualidade da tarde. Toque para seguir."]),
    ], dadosExtra={u"TITULO": u"OS ADJETIVOS DO POEMA", u"FECHO": u"Você achou as qualidades do poema!"})

# ============================================================
# BLOCO 2 — caca-palavras (idx 6-7): achar os SUBSTANTIVOS (obj2), gêneros
#           e-mail e notícia. Grade de letras sem acento (a peça normaliza).
# ============================================================
LETRAS = u"ACDEHILMNOPRSTUV"

add(id=u"f07", mec=u"caca-palavras", selo=u"MATÉRIA 4: O E-MAIL", conceito=u"objetivo2",
    enunciado=(u"Leia o <b>e-mail</b>: <i>“Assunto: Passeio da turma. Olá! Confirmem se "
               u"vão ao museu na sexta. Levem lanche e caderno.”</i> Ache no quadro os "
               u"<b>SUBSTANTIVOS</b> da mensagem."),
    dica=u"Substantivos = nomes de coisas e lugares. Estão deitados (→) e em pé (↓).",
    dados=[u"MUSEU", u"LANCHE", u"CADERNO", u"TURMA", u"PASSEIO"],
    dadosExtra={u"MODO": u"lista", u"TITULO": u"OS SUBSTANTIVOS DA MENSAGEM",
                u"LETRAS": LETRAS, u"DIFICIL": u"",
                u"CORP": [u"p1", u"p2", u"p3", u"p4", u"p5"]})

add(id=u"f07b", mec=u"caca-palavras", selo=u"MATÉRIA 5: A NOTÍCIA", conceito=u"objetivo2",
    enunciado=(u"Leia a <b>notícia</b>: <i>“A chuva forte alagou a rua do centro ontem. "
               u"A prefeitura pediu ao povo para evitar a ponte.”</i> Ache no quadro os "
               u"<b>SUBSTANTIVOS</b> da notícia."),
    dica=u"Substantivos = nomes de coisas, lugares e gente. Deitados (→) e em pé (↓).",
    dados=[u"CHUVA", u"RUA", u"CENTRO", u"PONTE", u"POVO"],
    dadosExtra={u"MODO": u"lista", u"TITULO": u"OS SUBSTANTIVOS DA NOTÍCIA",
                u"LETRAS": LETRAS, u"DIFICIL": u"",
                u"CORP": [u"p1", u"p2", u"p3", u"p4", u"p5"]})

# ============================================================
# AQUECIMENTO (idx 8, ~45%) — revisão espaçada do SUBSTANTIVO por um gesto
#   diferente (ligar). ÚNICO reuso fora de bloco (regra do Marcos).
# ============================================================
add(id=u"aquecimento", mec=u"ligar", selo=u"AQUECIMENTO DA REDAÇÃO", conceito=u"objetivo2",
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
# BLOCO 3 — completar (idx 9-11): marcar o VERBO (a ação) que falta (obj4),
#           gêneros receita (injuntivo) e notícia. As opções erradas são de
#           OUTRAS classes, para a criança escolher a AÇÃO = o verbo.
# ============================================================
add(id=u"f08", mec=u"completar", selo=u"MATÉRIA 6: A RECEITA DO BOLO", conceito=u"objetivo4",
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

add(id=u"f08b", mec=u"completar", selo=u"MATÉRIA 6: A RECEITA DO SUCO", conceito=u"objetivo4",
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

add(id=u"f08c", mec=u"completar", selo=u"MATÉRIA 7: A NOTÍCIA DA CIDADE", conceito=u"objetivo4",
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

# ============================================================
# BLOCO 4 — ligar (idx 12-14): cada ADJETIVO ao SUBSTANTIVO que ele descreve
#           (obj3), gêneros poema, tirinha e anúncio.
# ============================================================
add(id=u"f09", mec=u"ligar", selo=u"MATÉRIA 3: LIGUE O ADJETIVO", conceito=u"objetivo3",
    enunciado=u"De volta ao <b>poema</b>: ligue cada <b>adjetivo</b> ao substantivo que ele descreve.",
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

add(id=u"f09b", mec=u"ligar", selo=u"MATÉRIA 8: A TIRINHA", conceito=u"objetivo3",
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

add(id=u"f09c", mec=u"ligar", selo=u"MATÉRIA 9: O ANÚNCIO", conceito=u"objetivo3",
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
# BLOCO 5 — intruso (idx 15-16): qual palavra NÃO é VERBO (obj4), gêneros
#           receita e fábula. Três são ações; uma é de outra classe.
# ============================================================
add(id=u"f10", mec=u"intruso", selo=u"MATÉRIA 6: A PALAVRA INTRUSA", conceito=u"objetivo4",
    enunciado=u"Três palavras da receita são <b>VERBOS</b> (ações). <b>Qual NÃO é verbo?</b>",
    dica=u"Verbo é ação: misture, corte, asse. O que não é ação é intruso.",
    dados=[
      {u"selo": u"AS PALAVRAS DA RECEITA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"MISTURE"}, {u"k": u"b", u"n": u"CORTE"},
                  {u"k": u"c", u"n": u"ASSE"}, {u"k": u"d", u"n": u"FARINHA"}],
       u"fora": u"d", u"nomeFora": u"FARINHA",
       u"d1": u"Leia as quatro. Três MANDAM fazer algo; uma é só o nome de uma coisa.",
       u"d2": u"MISTURE, CORTE e ASSE são ações. FARINHA é o nome de um ingrediente.",
       u"d3": u"A de fora é <b>FARINHA</b>: é um substantivo (nome de coisa), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta é nome de coisa (substantivo).", u"ok": 1},
                   {u"t": u"Porque ela é a mais comprida.", u"ok": 0},
                   {u"t": u"Porque ela é usada no bolo.", u"ok": 0},
                   {u"t": u"Porque ela começa com F.", u"ok": 0}],
       u"enunPorque": u"O que <b>FARINHA</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três mandam fazer.",
       u"p2": u"Misture, corte, asse são AÇÕES. Farinha é uma COISA.",
       u"p3": u"“Farinha” nomeia uma coisa (substantivo); as outras são verbos.",
       u"regra": u"verbo é ação; substantivo é nome de coisa"},
      {u"selo": u"AS PALAVRAS DA RECEITA", u"tipo": u"texto",
       u"enun": u"Três destas palavras são ações (verbos). <b>Qual NÃO é?</b>",
       u"itens": [{u"k": u"a", u"n": u"BATA"}, {u"k": u"b", u"n": u"DESPEJE"},
                  {u"k": u"c", u"n": u"TIGELA"}, {u"k": u"d", u"n": u"PROVE"}],
       u"fora": u"c", u"nomeFora": u"TIGELA",
       u"d1": u"Leia as quatro. Três MANDAM fazer algo; uma é só o nome de um objeto.",
       u"d2": u"BATA, DESPEJE e PROVE são ações. TIGELA é o nome de um objeto.",
       u"d3": u"A de fora é <b>TIGELA</b>: é um substantivo (nome de objeto), não uma ação.",
       u"razoes": [{u"t": u"As outras são ações (verbos); esta é nome de objeto (substantivo).", u"ok": 1},
                   {u"t": u"Porque ela é a única redonda.", u"ok": 0},
                   {u"t": u"Porque ela é a mais curta.", u"ok": 0},
                   {u"t": u"Porque ela termina em A.", u"ok": 0}],
       u"enunPorque": u"O que <b>TIGELA</b> tem de diferente das outras três? Toque na razão certa.",
       u"p1": u"Olhe o que as OUTRAS três mandam fazer.",
       u"p2": u"Bata, despeje, prove são AÇÕES. Tigela é uma COISA.",
       u"p3": u"“Tigela” nomeia um objeto (substantivo); as outras são verbos.",
       u"regra": u"verbo é ação; substantivo é nome de objeto"},
    ])

add(id=u"f10b", mec=u"intruso", selo=u"MATÉRIA 10: A FÁBULA", conceito=u"objetivo4",
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

# ============================================================
# BLOCO 6 — classificar (idx 17-19): AS TRÊS CLASSES JUNTAS em 3 gavetas
#           (SUBSTANTIVO / ADJETIVO / VERBO) — o clímax. Palavras retiradas
#           do texto de cada gênero (fábula, fábula, notícia). Cada palavra é
#           inequívoca (sem "limpa/canta" que servem a duas classes).
# ============================================================
GAVETAS = [{u"k": u"sub", u"n": u"SUBSTANTIVO", u"img": u"", u"voz": u"substantivo", u"rot": False},
           {u"k": u"adj", u"n": u"ADJETIVO", u"img": u"", u"voz": u"adjetivo", u"rot": False},
           {u"k": u"verb", u"n": u"VERBO", u"img": u"", u"voz": u"verbo", u"rot": False}]

DICAS_CLASS = [u"Nome de coisa/ser vai em SUBSTANTIVO; qualidade em ADJETIVO; ação em VERBO.",
               u"Pergunte: é o nome de algo? é como algo é? ou é o que alguém faz?",
               u"Olhe a gaveta com a borda amarela: é ali que esta palavra mora."]

add(id=u"f11", mec=u"classificar", selo=u"EDIÇÃO ESPECIAL: A FÁBULA (1)", conceito=u"objetivo2",
    enunciado=(u"Leia a <b>fábula</b>: <i>“O leão forte dormia. O rato pequeno correu "
               u"e roeu a rede.”</i> Cada palavra na sua gaveta: substantivo, adjetivo ou verbo?"),
    dica=u"Substantivo = nome; adjetivo = qualidade; verbo = ação.",
    dados=GAVETAS,
    dadosExtra={u"FICHAS": [
      {u"t": u"LEÃO", u"alvo": u"sub"}, {u"t": u"RATO", u"alvo": u"sub"},
      {u"t": u"FORTE", u"alvo": u"adj"}, {u"t": u"PEQUENO", u"alvo": u"adj"},
      {u"t": u"DORMIA", u"alvo": u"verb"}, {u"t": u"CORREU", u"alvo": u"verb"}],
      u"DICAS": DICAS_CLASS,
      u"ENUN": u"Toque na <b>palavra</b>. Depois toque na <b>gaveta da classe</b> dela."})

add(id=u"f11b", mec=u"classificar", selo=u"EDIÇÃO ESPECIAL: A FÁBULA (2)", conceito=u"objetivo3",
    enunciado=(u"Continue a <b>fábula</b>: <i>“A formiga esperta guardou comida. A cigarra "
               u"alegre cantou o verão inteiro.”</i> Cada palavra na sua gaveta."),
    dica=u"Substantivo = nome; adjetivo = qualidade; verbo = ação.",
    dados=GAVETAS,
    dadosExtra={u"FICHAS": [
      {u"t": u"FORMIGA", u"alvo": u"sub"}, {u"t": u"CIGARRA", u"alvo": u"sub"},
      {u"t": u"ESPERTA", u"alvo": u"adj"}, {u"t": u"ALEGRE", u"alvo": u"adj"},
      {u"t": u"GUARDOU", u"alvo": u"verb"}, {u"t": u"CANTOU", u"alvo": u"verb"}],
      u"DICAS": DICAS_CLASS,
      u"ENUN": u"Toque na <b>palavra</b>. Depois toque na <b>gaveta da classe</b> dela."})

add(id=u"f11c", mec=u"classificar", selo=u"CAPA DA REVISTA: A NOTÍCIA", conceito=u"objetivo4",
    enunciado=(u"Última matéria, a <b>notícia</b> de capa: <i>“A cidade bonita ganhou uma "
               u"praça. As crianças felizes plantaram árvores.”</i> Cada palavra na sua gaveta."),
    dica=u"Substantivo = nome; adjetivo = qualidade; verbo = ação. Você já é editor(a)!",
    dados=GAVETAS,
    dadosExtra={u"FICHAS": [
      {u"t": u"CIDADE", u"alvo": u"sub"}, {u"t": u"CRIANÇAS", u"alvo": u"sub"},
      {u"t": u"BONITA", u"alvo": u"adj"}, {u"t": u"FELIZES", u"alvo": u"adj"},
      {u"t": u"GANHOU", u"alvo": u"verb"}, {u"t": u"PLANTARAM", u"alvo": u"verb"}],
      u"DICAS": DICAS_CLASS,
      u"ENUN": u"Toque na <b>palavra</b>. Depois toque na <b>gaveta da classe</b> dela."})


CONTEUDO[u"fases"] = fases
io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8").write(
    json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
print(u"conteudo.json: %d fases (6 gestos distintos, cada um contíguo)" % len(fases))
