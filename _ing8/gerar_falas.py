# -*- coding: utf-8 -*-
u"""
============================================================
 ESQUELETO — gerador das falas da folha viva

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.
    Texto mudou = voz regravada (o `entregar.yml` compara o carimbo sha1). É isto
    que acaba com "a tela diz uma coisa e a voz diz outra" — e atividade sem
    `falas.json` NÃO TEM COMO SER CONFERIDA, porque mp3 não se lê.

 ⚠️ UMA FONTE SÓ. As palavras, as frases e os textos moram no bloco
    `/*DADOS-INI*/` do `index.html` e são LIDOS daqui. Nada de segunda lista
    para desencontrar: já custou caro nesta casa um relatório sair zero com a
    folha inteira respondida.

 ⚠️ TODA TELA É NARRADA, e o alto-falante entra também em CADA RESPOSTA que a
    criança toca. Regra do Marcos: *"o alto-falante nas respostas também, para
    ajudar os alunos que não sabem ler"*. Sem isso a criança que ainda soletra
    escolhe pelo tamanho da palavra e a folha vira sorteio.

 ⚠️ A DICA NUNCA DIZ A RESPOSTA. Ela manda olhar uma pista, ou faz outra
    pergunta. Responder no segundo erro não é ajudar: é tirar da criança a única
    chance de pensar de novo.

 ⚠️ PALAVRAS QUE A VOZ ERRA (medido, e o portão `_qa/falas.py` reprova):
    "complete" vira "complite" — usar "preencha". Letra solta ("som S") sai como
    o NOME da letra: ancorar num exemplo ("o som de SAPO").

 Uso:  python3 <pasta>/gerar_falas.py
 Saída: reescreve os blocos FALAS e VOZOK do index.html, o `falas.json` e o
        `voz.txt`.
============================================================
"""
from __future__ import print_function

import collections
import io
import json
import os
import re
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"lf_"                     # <- o prefixo desta atividade
VOZ = u"pt-BR-AntonioNeural"

D = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    u"""Lê um objeto do bloco DADOS do index.html. Uma fonte só."""
    m = re.search(r"var " + nome + r" = (\{.*?\n\});", D, re.S)
    if not m:
        raise SystemExit(u"nao achei o bloco `var %s` no index.html" % nome)
    txt = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
    txt = re.sub(r'"\s*\+\s*\n\s*"', "", txt)                 # junta "a" + "b"
    txt = re.sub(r'([\{,]\s*)"?([A-Za-zÀ-ÿ_0-9]+)"?\s*:', r'\1"\2":', txt)
    txt = re.sub(r",(\s*[\}\]])", r"\1", txt)
    return json.loads(txt)


# ⚠️⚠️ A ENTIDADE HTML TAMBÉM É MARCAÇÃO, e isto foi lição paga (15/set/2026,
#    caderno de inglês do 8º ano). O `lp` tirava as TAGS e deixava as
#    ENTIDADES, então a lista de ingredientes da pizza — escrita com `&middot;`
#    para virar o ponto que separa os itens — ia para a fila de gravação como
#    *"Oil and middot Tomato sauce and middot Some onions"*. O portão
#    `_qa/revisor.py` pegou; se não pegasse, a voz teria dito isso à criança.
_ENT = {u"&middot;": u",", u"&nbsp;": u" ", u"&amp;": u" e ", u"&mdash;": u" ",
        u"&ndash;": u" ", u"&hellip;": u" ", u"&quot;": u'"', u"&lt;": u"",
        u"&gt;": u"", u"&#39;": u"'", u"&apos;": u"'"}


def lp(s):
    u"""tira a marcação e deixa o texto do jeito que a voz vai dizer"""
    t = re.sub(r"<[^>]+>", " ", s or u"")
    for _e, _v in _ENT.items():
        t = t.replace(_e, _v)
    t = re.sub(r"\s+", u" ", t)
    # ⚠️ e a tag que vira espaco deixa um vao ANTES da pontuacao ("o cinema ."),
    #    que o `_qa/revisor.py` acusa — com razao: a voz faz a pausa no lugar
    #    errado. Cola a pontuacao de volta na palavra.
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    # ⚠️ E A VIRGULA DA PAUSA PODE ENCOSTAR NUMA QUE JA EXISTIA (15/set/2026):
    #    a frase "My dad, ___ travels a lot" virou "My dad,, travels a lot" —
    #    duas virgulas coladas, que o Edge TTS le como uma pausa estranha e
    #    longa demais. Uma so, sempre.
    t = re.sub(r",\s*,+", u",", t)
    return t.strip()


def ch(w):
    return re.sub(r"[^a-z]", "",
                  unicodedata.normalize("NFKD", w.lower())
                  .encode("ascii", "ignore").decode())


F = collections.OrderedDict()
EN = set()                    # as chaves cujo texto e INGLES


def p(k, v):
    F[k] = v


def pe(k, v):
    u"""⭐ FALA EM INGLES — e ela e gravada com VOZ INGLESA, nao com voz
    portuguesa lendo ingles (ordem do Marcos, ago/2026: *"voz inglesa no
    ingles"*). O `entregar.yml` le o campo `lang` do falas.json e troca o
    `pt-BR-AntonioNeural` pelo `en-US-GuyNeural` so nessas.
    ⚠️ E ISSO NAO E ENFEITE NUM CADERNO DE INGLES: a crianca que ainda le
       devagar escolhe pelo SOM, e voz portuguesa dizendo *"whose"* ensina a
       pronuncia errada para a turma inteira."""
    F[k] = v
    EN.add(k)


# ---------------------------------------------------------------------------
# AS FALAS DO MOTOR — estas toda folha viva tem
# ---------------------------------------------------------------------------
p(u"capa", u"Lost and Found: o balcão dos achados e perdidos. Inglês, oitavo ano, "
           u"trinta e cinco folhas sobre some, any, much, many e os pronomes "
           u"relativos. Você vai atender o balcão de um aeroporto. Escreva o seu "
           u"nome ali embaixo e toque em Começar.")
p(u"quase", u"Quase! Olhe de novo e tente outra.")
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque numa palavra do lado esquerdo e depois na do lado direito.")
p(u"toque_palavra", u"Primeiro toque numa palavra ali embaixo. Depois toque na "
                    u"gaveta dela.")
p(u"vozOn", u"Narração ligada!")
# ⭐ O FECHO TEM GANCHO (regra da casa): a atividade termina deixando uma
#    pergunta ABERTA, que a crianca leva para fora da tela. Aqui ela e a ponte
#    para o caderno de papel, onde acontece a escrita que a tela nao corrige.
# ⚠️ o gancho TINHA reticencias soltas ("I lost a ... which ...") e o portao
#    novo `_qa/ingles.py` acusou o espaco antes da pontuacao — a voz faria a
#    pausa no lugar errado. Escrito como se fala.
p(u"fim", u"Você chegou ao fim do balcão! Agora você sabe dizer quanto tem "
          u"dentro da mala e de quem ela é. E fica a pergunta: o que é que "
          u"mais se perde na sua casa? Escreva no caderno uma frase em inglês "
          u"que comece com: I lost a.")

# ---------------------------------------------------------------------------
# AS FALAS DAS FOLHAS — uma seção por folha, lendo os DADOS do index.html.
#
# ⚠️ REGRA DAS FALAS EM INGLÊS: usa-se `pe()` para tudo o que está ESCRITO em
#    inglês na tela (a frase, a palavra da gaveta, a opção do botão) e `p()`
#    para o que é explicação em português. Voz portuguesa lendo inglês ensina a
#    pronúncia errada; voz inglesa lendo português sai incompreensível.
# ⚠️ A DICA NUNCA DIZ A RESPOSTA — manda olhar uma pista ou faz outra pergunta.
#
# ⚠️⚠️ OS NÚMEROS DE FOLHA VÊM DO MAPA `POS`, E NÃO ESCRITOS À MÃO. O caderno já
#    mudou de 22 para 35 folhas uma vez (o piso novo do Marcos, 15/set), e as
#    chaves de fala carregam o número da folha (`certo14_n1`, `p14enun`).
#    Com os números soltos pelo arquivo, remontar a ordem seria caçar duzentas
#    ocorrências à mão — e bastaria errar UMA para a folha ficar muda sem erro
#    nenhum no console. Mudou a ordem? Mexe-se no `POS`, e só.
# ---------------------------------------------------------------------------
POS = {
    u"quant": 1, u"cp1": 2, u"cp2": 3, u"ligafig": 4, u"artigo": 5,
    u"plural": 6, u"dupla": 7,
    u"someany": 8, u"mala": 9, u"bilhete": 10, u"pizza": 11, u"mochila": 12,
    u"julga": 13,
    u"muchmany": 14, u"dialogo": 15, u"cardapio": 16, u"pergunta": 17,
    u"respcurta": 18,
    u"acha": 19, u"whowhich": 20, u"tres": 21, u"posse": 22, u"quiz": 23,
    u"cultura": 24, u"metades": 25, u"define": 26,
    u"julgap": 27, u"oracao": 28, u"anat": 29, u"junta": 30, u"junta2": 31,
    u"escreve": 32, u"texto": 33, u"marcar": 34, u"cartaz": 35,
}


def N(nome):
    return unicode(POS[nome]) if str is bytes else str(POS[nome])


QUANT = bloco(u"QUANT")
GAV = bloco(u"GAV")
LIGAFIG = bloco(u"LIGAFIG")
ARTIGO = bloco(u"ARTIGO")
PLURAL = bloco(u"PLURAL")
DUPLA = bloco(u"DUPLA")
SOMEANY = bloco(u"SOMEANY")
MALA = bloco(u"MALA")
BILHETE = bloco(u"BILHETE")
PIZZA = bloco(u"PIZZA")
MOCHILA = bloco(u"MOCHILA")
JULGA = bloco(u"JULGA")
MUCHMANY = bloco(u"MUCHMANY")
DIALOGO = bloco(u"DIALOGO")
CARDAPIO = bloco(u"CARDAPIO")
PERGUNTA = bloco(u"PERGUNTA")
RESPCURTA = bloco(u"RESPCURTA")
ACHA = bloco(u"ACHA")
WHOWHICH = bloco(u"WHOWHICH")
TRES = bloco(u"TRES")
POSSE = bloco(u"POSSE")
QUIZ = bloco(u"QUIZ")
CULTURA = bloco(u"CULTURA")
METADES = bloco(u"METADES")
DEFINE = bloco(u"DEFINE")
JULGAP = bloco(u"JULGAP")
ORACAO = bloco(u"ORACAO")
JUNTA = bloco(u"JUNTA")
JUNTA2 = bloco(u"JUNTA2")
ESCREVE = bloco(u"ESCREVE")
TEXTO = bloco(u"TEXTO")
MARCAR = bloco(u"MARCAR")
CARTAZ = bloco(u"CARTAZ")


def lac(s):
    u"""A LACUNA NAO E NARRADA: a voz le a frase COM O QUE ELA TEM, pulando o
    buraco.

    ⭐ DECISAO DO MARCOS (15/set/2026), em duas mensagens. Primeiro:
       *"o blank de vazio nao precisa ser narrado, melhor uma pausa curta e
       depois dizer a frase toda em ingles na correcao nao?"*. Eu fiz a pausa
       com virgula — e ela QUEBROU nas frases que ja tinham virgula: *"My dad,
       ___ travels a lot"* virava *"My dad, travels a lot"*, uma frase que soa
       COMPLETA e esconde o buraco. Ele entao resolveu melhor do que eu:
       ***"ao invez da pausa e so nao falar nada, falar a frase com o que tem"***.

    ⭐ E ISTO E MELHOR POR TRES RAZOES, nao so por ser mais simples:
       1. funciona SEMPRE — nao depende de a frase ter ou nao pontuacao ali;
       2. nao inventa som nenhum (a palavra `blank` so ensinava `blank`);
       3. faz o PAR QUE ENSINA: a crianca ouve a frase SEM a palavra e, ao
          acertar, ouve a frase COM ela (ver `certa()`). A diferenca entre as
          duas e exatamente o conteudo da folha — e e ela que fica no ouvido.

    ⚠️ E O BURACO CONTINUA A VISTA: ele esta na TELA, desenhado. O audio e
       apoio, nao enunciado unico."""
    return lp(lp(s).replace(u"___", u" "))


def certa(frase, resposta):
    u"""A FRASE COMPLETA, com a resposta no lugar do buraco — e ela e a fala do
    ACERTO. E o modelo de pronuncia que a crianca leva: ela tentou, acertou, e
    ouve como a frase soa inteira, em ingles, dita por voz inglesa.
    ⚠️ O PORQUE EM PORTUGUES NAO SE PERDE: ele continua ESCRITO na tela (o
       `nomeSecreto`, que aparece no instante do acerto), e a DICA do erro
       continua falada em portugues — que e onde a explicacao pesa de verdade."""
    return lp(frase).replace(u"___", resposta)


# ---- o alto-falante de CADA resposta que a criança toca (regra do Marcos:
#      *"o alto-falante nas respostas também, para ajudar os alunos que não
#      sabem ler"*). Em inglês, com voz inglesa.
for _w in [u"a", u"an", u"some", u"any", u"much", u"many",
           u"who", u"which", u"whose", u"that", u"whom", u"where", u"when"]:
    pe(u"op_" + _w, _w + u".")
p(u"op_nada", u"Nenhum artigo.")
p(u"op_certa", u"Está certa.")
p(u"op_erro", u"Tem erro.")
p(u"marca_c", u"Marca do que se conta.")
p(u"marca_u", u"Marca do que não se conta.")
p(u"toque_marca", u"Primeiro escolha uma das duas marcas ali em cima.")

# ============ BLOCO 1 — o que se conta (folhas 1 a 7) ============
p(u"p" + N(u"quant") + u"enun",
  u"Leia a frase e escolha a palavra que falta: a, ou some.")
for k, Q in QUANT.items():
    pe(u"frase_" + k, lp(Q[u"a"] + u" " + Q[u"b"]))
    pe(u"certo" + N(u"quant") + u"_" + k,
       lp(Q[u"a"] + u" " + Q[u"r"] + u" " + Q[u"b"]))
    p(u"dica" + N(u"quant") + u"_" + k,
      u"Pense: dá para contar um, dois, três dessa coisa?")

p(u"p" + N(u"cp1") + u"enun",
  u"Uma gaveta é do que se pode contar. A outra é do que não se conta em unidades.")
p(u"p" + N(u"cp2") + u"enun",
  u"Agora são três gavetas. Olhe se a palavra está no singular, no plural, ou se nem tem plural.")
p(u"p" + N(u"anat") + u"enun",
  u"Estas frases foram desmontadas em pedaços. Ponha cada pedaço na gaveta dele.")
for _gk, _G in GAV.items():
    for _C in _G[u"cols"]:
        pe(u"gav_" + _gk + u"_" + _C[u"k"], _C[u"n"] + u".")
    for _n, _P in _G[u"pal"].items():
        pe(u"diz2_" + _gk + u"_" + _n, _P[u"p"] + u".")
for k in GAV[u"cp1"][u"pal"]:
    p(u"certo" + N(u"cp1") + u"_" + k, u"Isso! Gaveta certa.")
    p(u"dica" + N(u"cp1") + u"_" + k,
      u"Tente dizer dois desses em inglês. Se soar estranho, é a outra gaveta.")
for k in GAV[u"cp2"][u"pal"]:
    p(u"certo" + N(u"cp2") + u"_" + k, u"Isso! Gaveta certa.")
    p(u"dica" + N(u"cp2") + u"_" + k,
      u"Olhe o fim da palavra: tem s de plural? E tem o a ou o an na frente?")
for k in GAV[u"anat"][u"pal"]:
    p(u"certo" + N(u"anat") + u"_" + k, u"Isso! Peça no lugar certo.")
    p(u"dica" + N(u"anat") + u"_" + k,
      u"Este pedaço é o nome de quem a frase fala, é a palavrinha que liga, ou "
      u"é o que explica esse nome?")

p(u"p" + N(u"ligafig") + u"enun",
  u"Toque na figura e depois no nome dela em inglês.")
for k, I in LIGAFIG.items():
    p(u"ligafige_" + k, lp(I[u"alt"]) + u".")
    pe(u"ligafigd_" + k, lp(I[u"p"]) + u".")
    p(u"certo" + N(u"ligafig") + u"_" + k, u"Isso! É essa mesmo.")
    p(u"dica" + N(u"ligafig") + u"_" + k,
      u"Olhe bem o desenho e leia os nomes devagar, um por um.")

p(u"p" + N(u"artigo") + u"enun",
  u"O que vem antes desta palavra: a, an, ou nada?")
for k, T in ARTIGO.items():
    pe(u"art_" + k, lp(T[u"p"]) + u".")
    p(u"certo" + N(u"artigo") + u"_" + k, u"Isso mesmo!")
    p(u"dica" + N(u"artigo") + u"_" + k,
      u"Duas perguntas: essa coisa se conta? E ela começa com som de vogal?")

p(u"p" + N(u"plural") + u"enun",
  u"Escreva a palavra do parêntese no plural.")
for k, L in PLURAL.items():
    pe(u"plu_" + k, lp(L[u"a"] + u" " + L[u"b"]))
    pe(u"certo" + N(u"plural") + u"_" + k,
       lp(L[u"a"] + u" " + L[u"r"].lower() + u" " + L[u"b"]))
    p(u"dica" + N(u"plural") + u"_" + k,
      u"Olhe a última letra da palavra. Algumas palavras do inglês ganham um "
      u"e antes do s no plural — diga em voz baixa e veja se soa bem sem ele.")

p(u"p" + N(u"dupla") + u"enun",
  u"Escolha a marca e toque na palavra: o que se conta, ou o que não se conta.")
for k, DU in DUPLA.items():
    pe(u"dupla_" + k, u" ".join(DU[u"palavras"]))
    p(u"certo" + N(u"dupla") + u"_" + k + u"_c", u"Isso! Essa dá para contar.")
    p(u"certo" + N(u"dupla") + u"_" + k + u"_u", u"Isso! Essa não se conta em unidades.")
    p(u"dica" + N(u"dupla") + u"_" + k,
      u"Nesta frase há uma de cada. Leia devagar e ache os nomes das coisas.")

# ============ BLOCO 2 — some e any (folhas 8 a 13) ============
p(u"p" + N(u"someany") + u"enun",
  u"Olhe se a frase diz que tem, se ela nega ou se ela pergunta. Depois escolha.")
_PQT = {u"a": u"A frase diz que TEM.", u"n": u"A frase NEGA.",
        u"p": u"A frase PERGUNTA.", u"e": u"Esta é a exceção."}
for k, S in SOMEANY.items():
    pe(u"sa_" + k, lac(S[u"f"]))
    pe(u"certo" + N(u"someany") + u"_" + k, certa(S[u"f"], S[u"r"]))
    p(u"dica" + N(u"someany") + u"_" + k,
      _PQT.get(S[u"t"], u"Leia a frase de novo.") + u" Olhe o começo dela outra vez.")

p(u"p" + N(u"mala") + u"enun", u"Olhe a figura e escolha: a, an, some ou any.")
for k, V in MALA.items():
    pe(u"malafr_" + k, lp(V[u"a"] + u" " + V[u"b"]))
    pe(u"certo" + N(u"mala") + u"_" + k,
       lp(V[u"a"] + u" " + V[u"r"] + u" " + V[u"b"]))
    p(u"dica" + N(u"mala") + u"_" + k,
      u"Duas perguntas: essa coisa se conta? E a frase nega ou pergunta?")

p(u"p" + N(u"bilhete") + u"enun", u"Preencha o bilhete: some ou any?")
p(u"biltit", lp(BILHETE[u"titulo"]))
for _i, _L in enumerate(BILHETE[u"linhas"]):
    pe(u"bil_" + str(_i), lac(_L[u"t"]))
for k, C in BILHETE[u"lac"].items():
    pe(u"certo" + N(u"bilhete") + u"_" + k,
       certa([_l[u"t"] for _l in BILHETE[u"linhas"] if _l[u"g"] == k][0], C[u"r"]))
    p(u"dica" + N(u"bilhete") + u"_" + k,
      u"Esta linha diz que tem, nega, ou pergunta?")

p(u"p" + N(u"pizza") + u"enun", u"Olhe a receita e responda.")
pe(u"rec_" + PIZZA[u"k"], lp(PIZZA[u"corpo"]))
for _i, _P in enumerate(PIZZA[u"perg"]):
    pe(u"pizq_" + str(_i), lp(_P[u"q"]))
    for _j, _o in enumerate(_P[u"o"]):
        pe(u"pizr_" + str(_i) + u"_" + str(_j), lp(_o))
    p(u"certo" + N(u"pizza") + u"_" + str(_i), u"Isso! " + lp(_P[u"pq"]))
    p(u"dica" + N(u"pizza") + u"_" + str(_i),
      u"Volte à lista de ingredientes e procure essa palavra lá.")

p(u"p" + N(u"mochila") + u"enun",
  u"Marque tudo o que não se conta. Depois toque em Conferir.")
for k, W in MOCHILA.items():
    pe(u"moc_" + k, W[u"n"] + u".")
p(u"certo" + N(u"mochila"), u"Você marcou todas, e só as certas!")
p(u"dica" + N(u"mochila"),
  u"Sobrou alguma marcada que dá para contar, ou faltou marcar alguma que não "
  u"dá. Confira uma por uma.")

p(u"p" + N(u"julga") + u"enun",
  u"Esta frase em inglês está certa, ou tem alguma coisa errada?")
for k, J in JULGA.items():
    pe(u"jul_" + k, lp(J[u"f"]))
    p(u"certo" + N(u"julga") + u"_" + k, u"Isso! " + lp(J[u"pq"]))
    p(u"dica" + N(u"julga") + u"_" + k,
      u"Olhe o fim das palavras: tem s onde não devia, ou falta s onde devia?")

# ============ BLOCO 3 — quanto (folhas 14 a 18) ============
p(u"p" + N(u"muchmany") + u"enun",
  u"Olhe a palavra que vem depois da lacuna: ela se conta ou não?")
for k, M in MUCHMANY.items():
    pe(u"mm_" + k, lac(M[u"f"]))
    pe(u"certo" + N(u"muchmany") + u"_" + k, certa(M[u"f"], M[u"r"]))
    p(u"dica" + N(u"muchmany") + u"_" + k,
      u"Se dá para contar, é uma. Se não dá, é a outra.")

p(u"p" + N(u"dialogo") + u"enun",
  u"Preencha a conversa: some, any, much ou many.")
p(u"dlgtit", lp(DIALOGO[u"titulo"]))
for _i, _L in enumerate(DIALOGO[u"linhas"]):
    pe(u"dlg_" + str(_i), _L[u"q"] + u": " + lac(_L[u"t"]))
for k, C in DIALOGO[u"lac"].items():
    pe(u"certo" + N(u"dialogo") + u"_" + k, (lambda _L: certa(
        _L[u"t"].replace(u"___", C[u"r"], 1) if _L.get(u"g2") else _L[u"t"], C[u"r"]))(
        [_x for _x in DIALOGO[u"linhas"] if k in (_x.get(u"g"), _x.get(u"g2"))][0]))
    p(u"dica" + N(u"dialogo") + u"_" + k,
      u"Quem está falando: quem pergunta, quem diz que tem, ou quem nega?")

p(u"p" + N(u"cardapio") + u"enun",
  u"Esta é a resposta do garçom. Qual foi a pergunta?")
pe(u"menu_" + CARDAPIO[u"k"], lp(CARDAPIO[u"corpo"]))
for _i, _P in enumerate(CARDAPIO[u"perg"]):
    pe(u"menq_" + str(_i), lp(_P[u"q"]).replace(u"—", u" ").strip())
    for _j, _o in enumerate(_P[u"o"]):
        pe(u"menr_" + str(_i) + u"_" + str(_j), lp(_o))
    p(u"certo" + N(u"cardapio") + u"_" + str(_i), u"Isso! " + lp(_P[u"pq"]))
    p(u"dica" + N(u"cardapio") + u"_" + str(_i),
      u"A resposta é um preço, um número de coisas, ou um sim e não?")

p(u"p" + N(u"pergunta") + u"enun",
  u"Esta é a resposta. Monte a pergunta tocando nos pedaços na ordem certa.")
for k, W in PERGUNTA.items():
    pe(u"perg_" + k, lp(W[u"resp"]))
    p(u"certo" + N(u"pergunta") + u"_" + k, u"Perfeito! A pergunta ficou de pé.")
    p(u"dica" + N(u"pergunta") + u"_" + k,
      u"Toda pergunta destas começa igual. E o que vem no fim é o verbo com there.")

p(u"p" + N(u"respcurta") + u"enun",
  u"Toque na pergunta e depois na resposta que combina com ela.")
for k, R in RESPCURTA.items():
    pe(u"rp_" + k, lp(R[u"p"]))
    pe(u"rd_" + k, lp(R[u"s"]))
    p(u"certo" + N(u"respcurta") + u"_" + k, u"Isso! A pergunta e a resposta combinam.")
    p(u"dica" + N(u"respcurta") + u"_" + k,
      u"A pergunta é de uma coisa só ou de várias? A resposta tem de ser do mesmo jeito.")

# ============ BLOCO 4 — qual pronome (folhas 19 a 26) ============
p(u"p" + N(u"acha") + u"enun",
  u"Em cada frase há um pronome relativo. Toque nele.")
for k, A in ACHA.items():
    pe(u"acha_" + k, u" ".join(A[u"palavras"]))
    p(u"certo" + N(u"acha") + u"_" + k, u"Achou!")
    p(u"dica" + N(u"acha") + u"_" + k,
      u"Ele fica logo depois do nome da pessoa ou da coisa que a frase está explicando.")

p(u"p" + N(u"whowhich") + u"enun",
  u"Olhe a palavra que vem antes da lacuna: é gente ou é coisa?")
for k, P in WHOWHICH.items():
    pe(u"ww_" + k, lac(P[u"f"]))
    pe(u"certo" + N(u"whowhich") + u"_" + k, certa(P[u"f"], P[u"r"]))
    p(u"dica" + N(u"whowhich") + u"_" + k,
      u"Um dos dois é só para gente. O outro é para coisa e para bicho.")

p(u"p" + N(u"tres") + u"enun",
  u"Agora são três. Se a coisa depois da lacuna é de alguém, o pronome é outro.")
for k, T in TRES.items():
    pe(u"tres_" + k, lac(T[u"f"]))
    pe(u"certo" + N(u"tres") + u"_" + k, certa(T[u"f"], T[u"r"]))
    p(u"dica" + N(u"tres") + u"_" + k,
      u"Depois da lacuna vem um verbo, ou vem uma coisa que é de alguém?")

p(u"p" + N(u"posse") + u"enun",
  u"Olhe a palavra que vem depois da lacuna: se for uma coisa de alguém, é whose.")
for k, O in POSSE.items():
    pe(u"po_" + k, lac(O[u"f"]))
    pe(u"certo" + N(u"posse") + u"_" + k, certa(O[u"f"], O[u"r"]))
    p(u"dica" + N(u"posse") + u"_" + k,
      u"Depois de whose vem sempre o nome de uma coisa. Depois de who vem sempre um verbo.")

p(u"p" + N(u"quiz") + u"enun", u"Agora são quatro opções. Só uma cabe.")
for k, C in QUIZ.items():
    pe(u"quiz_" + k, lac(C[u"f"]))
    pe(u"certo" + N(u"quiz") + u"_" + k, certa(C[u"f"], C[u"r"]))
    p(u"dica" + N(u"quiz") + u"_" + k,
      u"Leia as quatro em voz baixa, uma por uma, dentro da frase. Uma delas soa certa.")

p(u"p" + N(u"cultura") + u"enun",
  u"Coisas da Inglaterra. Qual pronome cabe em cada frase?")
for k, C in CULTURA.items():
    pe(u"cult_" + k, lac(C[u"f"]))
    pe(u"certo" + N(u"cultura") + u"_" + k, certa(C[u"f"], C[u"r"]))
    p(u"dica" + N(u"cultura") + u"_" + k,
      u"É gente, é coisa, ou é uma coisa que pertence a alguém?")

p(u"p" + N(u"metades") + u"enun",
  u"Cada frase foi cortada ao meio. Toque no começo e depois no fim dela.")
for k, H in METADES.items():
    pe(u"mete_" + k, lp(H[u"a"]))
    pe(u"metd_" + k, lp(H[u"b"]))
    p(u"certo" + N(u"metades") + u"_" + k, u"Isso! As duas metades são da mesma frase.")
    p(u"dica" + N(u"metades") + u"_" + k,
      u"Leia o começo e pergunte: o que falta dizer sobre essa pessoa ou coisa?")

p(u"p" + N(u"define") + u"enun", u"Toque no nome e depois na explicação dele.")
for k, E in DEFINE.items():
    pe(u"def_" + k, lp(E[u"p"]) + u".")
    pe(u"defd_" + k, lp(E[u"s"]) + u".")
    p(u"certo" + N(u"define") + u"_" + k, u"Isso! A explicação é dessa mesmo.")
    p(u"dica" + N(u"define") + u"_" + k,
      u"A explicação começa dizendo se é pessoa, animal, prédio ou máquina. Comece por aí.")

# ============ BLOCO 5 — juntar as duas frases (folhas 27 a 35) ============
p(u"p" + N(u"julgap") + u"enun",
  u"Olhe o pronome em negrito. Ele está no lugar certo?")
for k, U in JULGAP.items():
    pe(u"julp_" + k, lp(U[u"f"]))
    p(u"certo" + N(u"julgap") + u"_" + k, u"Isso! " + lp(U[u"pq"]))
    p(u"dica" + N(u"julgap") + u"_" + k,
      u"Pergunte: o que vem logo depois do pronome é uma coisa DE alguém?")

p(u"p" + N(u"oracao") + u"enun",
  u"Toque em todas as palavras da parte que explica, do pronome até onde ela acaba.")
for k, O in ORACAO.items():
    pe(u"orac_" + k, u" ".join(O[u"palavras"]))
    p(u"certo" + N(u"oracao") + u"_" + k, u"Isso! Você marcou a parte que explica, inteira.")
    p(u"dica" + N(u"oracao") + u"_" + k,
      u"Ela começa no pronome. E acaba quando a frase volta a falar do assunto principal.")

p(u"p" + N(u"junta") + u"enun",
  u"Junte as duas frases numa só. Toque nos pedaços na ordem certa.")
for k, Z in JUNTA.items():
    pe(u"jun_" + k, lp(Z[u"a"]) + u" " + lp(Z[u"b"]))
    p(u"certo" + N(u"junta") + u"_" + k, u"Perfeito! Duas frases viraram uma.")
    p(u"dica" + N(u"junta") + u"_" + k,
      u"O pedaço com o pronome entra logo depois da pessoa ou da coisa que ele explica.")

p(u"p" + N(u"junta2") + u"enun",
  u"De novo, junte as duas. Mas agora a parte que explica entra no meio.")
for k, Y in JUNTA2.items():
    pe(u"jun2_" + k, lp(Y[u"a"]) + u" " + lp(Y[u"b"]))
    p(u"certo" + N(u"junta2") + u"_" + k, u"Perfeito! E repare nas vírgulas.")
    p(u"dica" + N(u"junta2") + u"_" + k,
      u"Comece pelo nome de quem a frase fala. A parte com vírgula vem logo depois dele.")

p(u"p" + N(u"escreve") + u"enun",
  u"Escreva o pronome que falta. Repare: toda frase aqui tem vírgula, e depois "
  u"de vírgula o inglês nunca usa that.")
for k, X in ESCREVE.items():
    pe(u"esc_" + k, lp(X[u"a"] + u" " + X[u"b"]))
    pe(u"certo" + N(u"escreve") + u"_" + k,
       lp(X[u"a"] + u" " + X[u"r"].lower() + u" " + X[u"b"]))
    p(u"dica" + N(u"escreve") + u"_" + k,
      u"Depois da lacuna vem um verbo, ou vem uma coisa que é de alguém? E "
      u"lembre: aqui nunca é that.")

p(u"p" + N(u"texto") + u"enun", u"Agora responda sobre o texto.")
pe(u"hist_" + TEXTO[u"k"], lp(TEXTO[u"corpo"]))
for _i, _P in enumerate(TEXTO[u"perg"]):
    p(u"pergh_" + str(_i), lp(_P[u"q"]))
    for _j, _o in enumerate(_P[u"o"]):
        p(u"resph_" + str(_i) + u"_" + str(_j), lp(_o))
    p(u"certo" + N(u"texto") + u"_" + str(_i),
      u"Isso! " + lp(_P.get(u"pq", u"Você leu com atenção.")))
    p(u"dica" + N(u"texto") + u"_" + str(_i),
      u"Volte ao texto e leia de novo a parte que fala disso.")

p(u"p" + N(u"marcar") + u"enun",
  u"Marque todas as palavras que não se contam. Depois toque em Conferir.")
for k, Y in MARCAR.items():
    pe(u"diz21_" + k, Y[u"n"] + u".")
p(u"certo" + N(u"marcar"), u"Você marcou todas, e só as certas!")
p(u"dica" + N(u"marcar"),
  u"Sobrou alguma marcada que dá para contar, ou faltou marcar alguma que não "
  u"dá. Confira uma por uma.")

p(u"p" + N(u"cartaz") + u"enun",
  u"Escolha as regras que você quer no seu cartaz. Pode escolher quantas quiser.")
for k in CARTAZ:
    p(u"certo" + N(u"cartaz") + u"_" + k, u"Entrou no seu cartaz!")

# ---------------------------------------------------------------------------
# A SAÍDA
# ---------------------------------------------------------------------------
def chave(s):
    u"""O nome do mp3 sai do TEXTO, não da chave da fala — assim duas chaves que
    dizem a mesma frase gravam um arquivo só."""
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for c in s:
        hh = ((hh * 33) ^ ord(c)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    txt = F[k]
    if not txt:
        continue
    c = chave(txt)
    if c in vistos:
        continue
    vistos[c] = 1
    item = {u"id": PREFIXO + c, u"texto": txt, u"voz": VOZ}
    if k in EN:
        item[u"lang"] = u"en"
        item[u"voz"] = u"en-US-GuyNeural"
    falas.append(item)

html = io.open(CAM, encoding=u"utf-8").read()
blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)
io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
print(u"FALAS: %d chaves; falas.json: %d fala(s) para gravar" % (len(F), len(falas)))
