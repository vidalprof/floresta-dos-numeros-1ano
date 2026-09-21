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
PREFIXO = u"dn5_"                     # <- o prefixo desta atividade
VOZ = u"pt-BR-AntonioNeural"

D = io.open(CAM, encoding=u"utf-8").read()


def bloco(nome):
    u"""Lê um objeto do bloco DADOS do index.html. Uma fonte só.

    ⚠️ ELE CONTA AS CHAVES, e isso foi conserto de 15/set/2026. O esqueleto
       procurava o fim do objeto por uma marca de texto (`\n});`) — e QUALQUER
       objeto que não terminasse exatamente assim fazia a leitura passar
       adiante e engolir o bloco seguinte. No primeiro caderno do 2º ano os
       vinte e três blocos falharam de uma vez, todos com o mesmo erro, e a
       mensagem do json não dizia nada sobre a causa. Contar chave por chave
       (pulando as que estão DENTRO de texto) acha o fim de qualquer objeto.
    """
    i = D.find(u"var " + nome + u" = ")
    if i < 0:
        raise SystemExit(u"nao achei o bloco `var %s` no index.html" % nome)
    i = D.index(u"{", i)
    nivel, j, dentro, escapa = 0, i, False, False
    while j < len(D):
        c = D[j]
        if dentro:
            if escapa:
                escapa = False
            elif c == u"\\":
                escapa = True
            elif c == u'"':
                dentro = False
        else:
            if c == u'"':
                dentro = True
            elif c == u"{":
                nivel += 1
            elif c == u"}":
                nivel -= 1
                if nivel == 0:
                    j += 1
                    break
        j += 1
    txt = D[i:j]
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r'"\s*\+\s*\n\s*"', "", txt)                 # junta "a" + "b"
    # ⚠️ SEM O `"?` DOS DOIS LADOS, e isso foi conserto de 20/set/2026.
    #    Esta linha normaliza chave sem aspas (`chave:` -> `"chave":`). Com o
    #    `"?` ela também casava DENTRO de uma string: a opção
    #        ["b", "Não: é um MÚSCULO que ajuda o ar a entrar"]
    #    virava  ["b", "Não": é um MÚSCULO ...]  e o json.loads morria com
    #    "Expecting ',' delimiter", sem dizer uma palavra sobre a causa.
    #    Qualquer caderno com DOIS-PONTOS dentro de um texto caía nisso.
    #    Chave já entre aspas não precisa de conserto nenhum — então a regex
    #    só olha as SEM aspas, e string nenhuma é tocada.
    txt = re.sub(r'([\{,]\s*)([A-Za-zÀ-ÿ_0-9]+)\s*:', r'\1"\2":', txt)
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


def p(k, v):
    F[k] = v


# ---------------------------------------------------------------------------
# AS FALAS DO MOTOR — estas toda folha viva tem
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# AS FALAS DESTE CADERNO
#
# ⚠️ A VOZ NÃO LÊ "R$" NEM A VÍRGULA. Entregue "R$ 12,30" ao Edge TTS e ele diz
#    "erre cifrão doze vírgula trinta". Por isso TODO valor vira texto por
#    `rsf()`, que é o gêmeo do `rs()`/`rsFala()` do app — a tela mostra
#    R$ 12,30 e a voz diz "doze reais e trinta centavos".
#
# ⚠️ E A DICA NUNCA DIZ A RESPOSTA. Num caderno de contas isso é fácil de
#    esquecer: "são doze reais" resolveria o item. A dica manda olhar de novo,
#    lembra da regra, ou faz outra pergunta.
# ---------------------------------------------------------------------------
def rsf(c):
    u"""o valor do jeito que a voz diz — o gêmeo do `rsFala()` do app"""
    r, ct = c // 100, c % 100
    s = u""
    if r:
        s += u"%d %s" % (r, u"real" if r == 1 else u"reais")
    if r and ct:
        s += u" e "
    if ct:
        s += u"%d %s" % (ct, u"centavo" if ct == 1 else u"centavos")
    return s or u"zero real"


PROD = bloco(u"PROD")
DIN = bloco(u"DIN")
PUNHO = bloco(u"PUNHO")
SOMAV = bloco(u"SOMAV")
CEM = bloco(u"CEM")
COMPARA = bloco(u"COMPARA")
ORDENA = bloco(u"ORDENA")
DIZER = bloco(u"DIZER")
ESCUTA = bloco(u"ESCUTA")
UNIT = bloco(u"UNIT")
UNITC = bloco(u"UNITC")
CARRO = bloco(u"CARRO")
CARROB = bloco(u"CARROB")
NOTA = bloco(u"NOTA")
QUALCONTA = bloco(u"QUALCONTA")
TROCO = bloco(u"TROCO")
TROCOC = bloco(u"TROCOC")
TROCO4 = bloco(u"TROCO4")
TROCOP = bloco(u"TROCOP")
SEMTROCO = bloco(u"SEMTROCO")
FALTA = bloco(u"FALTA")
TROCA = bloco(u"TROCA")
MOEDAS = bloco(u"MOEDAS")
DIVCOM = bloco(u"DIVCOM")
PRESTA = bloco(u"PRESTA")
VENDIDOS = bloco(u"VENDIDOS")
GAV = bloco(u"GAV")
RESTO = bloco(u"RESTO")
PROVA = bloco(u"PROVA")
LUCRO = bloco(u"LUCRO")
ATACADO = bloco(u"ATACADO")
METADE = bloco(u"METADE")
PARTE = bloco(u"PARTE")
DUAS = bloco(u"DUAS")
MERCADO = bloco(u"MERCADO")
COMBO = bloco(u"COMBO")
CARTAZ = bloco(u"CARTAZ")

# ---- as falas que se repetem em várias folhas -----------------------------
VALORES = set()
def _v(c):
    VALORES.add(int(c))
NUMEROS = set()
def _n(x):
    NUMEROS.add(int(x))

# ⚠️⚠️ NUNCA CHAMAR UMA VARIÁVEL DE LAÇO DE `F` NEM DE `D` NESTE ARQUIVO, e
#    isto foi medido na primeira rodada: `F` é o OrderedDict que guarda TODAS as
#    falas e `D` é o texto do index.html que o `bloco()` lê. Escrevi
#    `for k, F in PARTE.items()` e `for F in CARTAZ["frases"]`, e a partir dali
#    todo `p()` passou a escrever DENTRO de um item do PARTE em vez de no
#    dicionário das falas. Resultado: o gerador não reclamou de nada, disse
#    "110 chaves" com ar de sucesso, e o caderno teria ido ao ar com os 38
#    enunciados MUDOS. É o mesmo silêncio do `falar()` com chave que não existe,
#    só que um andar acima. Quem pegou foi eu conferindo a lista de chaves — não
#    houve erro nenhum para pegar.
for k, DD in DIN.items():
    p(u"din_" + k, DD[u"n"].capitalize() + u".")

# ---- capa e motor ---------------------------------------------------------
p(u"folhaPronta", u"Folha pronta! Muito bem.")
p(u"digite", u"Escreva o valor com os algarismos. A vírgula anda sozinha.")
# ⚠️ O MOTOR AINDA TEM O TECLADO DE LETRAS (`abreCruz`), que este caderno não
#    usa em folha nenhuma — mas a chamada `falar("escreva")` continua no código
#    do motor. Sem este texto, o portão 1q reprova com razão: chave pedida que
#    não existe é voz que volta calada.
p(u"escreva", u"Escreva a palavra usando o teclado.")
p(u"ligue", u"Toque de um lado e depois no que combina com ele do outro lado.")
p(u"toque_palavra", u"Primeiro toque numa peça ali embaixo. Depois toque na gaveta dela.")
p(u"vozOn", u"Narração ligada!")
p(u"fim", u"Você chegou ao fim! Agora olhe o preço de alguma coisa que a sua família "
          u"compra sempre. Se a loja desse metade de desconto, quanto ficaria? E se você "
          u"pagasse com uma nota de cinquenta reais, quanto viria de troco? Leve essa "
          u"pergunta para casa.")

# ---- folha 1 — quanto tem na mão ------------------------------------------
p(u"p1enun", u"Folha um. Conte o dinheiro de cada mão e toque no valor certo.")
for k, Q in PUNHO.items():
    for v in Q[u"o"]:
        _v(v)
    p(u"certo_" + k, u"Isso! São " + rsf(Q[u"v"]) + u".")
    p(u"dica_" + k, u"Conte outra vez, e comece pelas notas maiores. Não esqueça as "
                    u"moedas do fim: elas são os centavos.")

# ---- folha 2 — só com o valor escrito -------------------------------------
p(u"p2enun", u"Folha dois. Agora sem figura de dinheiro: some os valores escritos e "
             u"preencha o total.")
for k, E in SOMAV.items():
    p(u"soma_" + k, u"Some: " + u", ".join(rsf(v) for v in E[u"v"]) + u".")
    p(u"certo_" + k, u"Isso! Dá " + rsf(E[u"r"]) + u".")
    p(u"dica_" + k, u"Junte primeiro as moedas que fecham um real. Depois some o resto.")

# ---- folha 3 — cem centavos fazem um real ---------------------------------
p(u"p3enun", u"Folha três. Marque todos os grupos de moedas que juntas dão um real. "
             u"Depois toque em Conferir.")
for S in CEM[u"s"]:
    p(u"grupo_" + S[u"k"], u"Grupo com " + str(len(S[u"pc"])) + u" moedas.")
p(u"certo_cem", u"Isso! Cem centavos fazem um real, e há mais de um jeito de juntar "
                u"cem centavos.")
p(u"dica_cem", u"Some as moedas de cada grupo antes de marcar. Um grupo só serve se "
               u"der cem centavos certinhos, nem mais nem menos.")

# ---- folha 4 — qual vale mais ---------------------------------------------
p(u"p4enun", u"Folha quatro. Olhe bem a vírgula: toque no preço que vale mais.")
for k, C in COMPARA.items():
    _v(C[u"a"]); _v(C[u"b"])
    maior = C[u"a"] if C[u"c"] == u"a" else C[u"b"]
    p(u"certo_" + k, u"Isso! " + rsf(maior).capitalize() + u" vale mais.")
    p(u"dica_" + k, u"Compare primeiro os reais, antes da vírgula. Se os reais forem "
                    u"iguais, aí sim olhe os centavos.")

# ---- folha 5 — ordenar ----------------------------------------------------
p(u"p5enun", u"Folha cinco. Ponha os preços em ordem, do mais barato para o mais caro: "
             u"toque no número do lugar de cada um.")
for i, v in enumerate(ORDENA[u"v"]):
    _v(v); _n(i + 1)
    p(u"certo_ord_" + str(v), u"Isso! " + rsf(v).capitalize() + u" fica no lugar " +
                              str(i + 1) + u".")
    p(u"dica_ord_" + str(v), u"Olhe quantos reais tem antes da vírgula. Quem tem menos "
                             u"reais vem primeiro.")

# ---- folha 6 — o preço e o jeito de dizer ---------------------------------
p(u"p6enun", u"Folha seis. Toque num preço de um lado e no jeito de dizer ele do outro lado.")
for k, D in DIZER.items():
    _v(D[u"v"])
    p(u"diz_" + k, D[u"t"].capitalize() + u".")
    p(u"certo6_" + k, u"Isso! " + rsf(D[u"v"]).capitalize() + u".")
    p(u"dica6_" + k, u"Conte as casas depois da vírgula: a primeira é dos dez centavos "
                     u"e a segunda é do centavo sozinho.")

# ---- folha 7 — escreva o preço que você ouve ------------------------------
p(u"p7enun", u"Folha sete. Ouça o preço e escreva com algarismos. A vírgula anda sozinha.")
for k, W in ESCUTA.items():
    p(u"ouca_" + k, W[u"t"].capitalize() + u".")
    p(u"certo_" + k, u"Isso! " + rsf(W[u"v"]).capitalize() + u".")
    p(u"dica_" + k, u"Escreva primeiro os centavos e depois os reais — a vírgula anda "
                    u"sozinha enquanto você escreve.")

# ---- folhas 8 e 9 — preço de um vezes a quantidade ------------------------
p(u"p8enun", u"Folha oito. Multiplique o preço de um produto pela quantidade e escreva "
             u"o total a pagar.")
p(u"p9enun", u"Folha nove. Agora os preços têm centavos. Toque na compra de um lado e "
             u"no total dela do outro.")
for k, U in UNIT.items():
    P = PROD[U[u"p"]]
    p(u"uni_" + k, P[u"n"] + u", cada um custa " + rsf(P[u"p"]) + u". Levar " +
                   str(U[u"q"]) + u".")
    p(u"certo_" + k, u"Isso! " + str(U[u"q"]) + u" vezes " + rsf(P[u"p"]) + u" dá " +
                     rsf(U[u"v"]) + u".")
    p(u"dica_" + k, u"Some o preço de um tantas vezes quantas forem as unidades — ou "
                    u"multiplique de uma vez só.")
for k, U in UNITC.items():
    P = PROD[U[u"p"]]
    _v(U[u"v"])
    p(u"unic_" + k, str(U[u"q"]) + u" vezes " + P[u"n"] + u", a " + rsf(P[u"p"]) + u" cada.")
    p(u"certo9_" + k, u"Isso! Dá " + rsf(U[u"v"]) + u".")
    p(u"dica9_" + k, u"Multiplique os centavos também. Se der cem centavos ou mais, "
                     u"eles viram reais.")

# ---- folha 10 e 11 — o carrinho -------------------------------------------
p(u"p10enun", u"Folha dez. Some o que está em cada carrinho e toque no total certo.")
p(u"p11enun", u"Folha onze. Puxe o total certo até o carrinho, ou toque nele, se preferir.")
for k, C in CARRO.items():
    for v in C[u"o"]:
        _v(v)
    p(u"carr_" + k, u"Carrinho com " + u", ".join(
        PROD[x][u"n"] + u" a " + rsf(PROD[x][u"p"]) for x in C[u"p"]) + u".")
    p(u"certo_" + k, u"Isso! O carrinho custa " + rsf(C[u"v"]) + u".")
    p(u"dica_" + k, u"Some de dois em dois: junte os dois primeiros e depois acrescente "
                    u"o que falta.")
for k, C in CARROB.items():
    _v(C[u"v"])
    p(u"certo_" + k, u"Isso! São " + rsf(C[u"v"]) + u".")
    p(u"dica_" + k, u"Olhe o preço de cada produto do carrinho e some. Cuidado com o "
                    u"produto que aparece duas vezes.")

# ---- folha 12 — a nota fiscal ---------------------------------------------
p(u"p12enun", u"Folha doze. Leia a compra, faça as contas e escreva quanto foi gasto ao todo.")
for k, N in NOTA.items():
    p(u"nota_" + k, N[u"fr"])
    p(u"certo_" + k, u"Isso! Dá " + rsf(N[u"v"]) + u".")
    p(u"dica_" + k, u"Faça uma multiplicação de cada vez e só depois some as duas.")

# ---- folha 13 — qual é a conta --------------------------------------------
p(u"p13enun", u"Folha treze. Antes de calcular: toque na conta que descobre o troco.")
for k, Y in QUALCONTA.items():
    p(u"conta_" + k, u"A compra custou " + rsf(Y[u"preco"]) + u" e você pagou com " +
                     rsf(Y[u"pago"]) + u".")
    p(u"opc_" + k + u"_sub", rsf(Y[u"pago"]) + u" menos " + rsf(Y[u"preco"]) + u".")
    p(u"opc_" + k + u"_som", rsf(Y[u"pago"]) + u" mais " + rsf(Y[u"preco"]) + u".")
    p(u"opc_" + k + u"_inv", rsf(Y[u"preco"]) + u" menos " + rsf(Y[u"pago"]) + u".")
    p(u"certo_" + k, u"Isso! O troco é o que SOBRA: tira-se o preço do que foi pago.")
    p(u"dica_" + k, u"Pense no caixa: o dinheiro que você deu é maior que o preço. "
                    u"O troco pode ser maior que o que você deu?")

# ---- folhas 14 e 15 — o troco ---------------------------------------------
p(u"p14enun", u"Folha catorze. Veja o preço do brinquedo e o que foi dado na mão do "
              u"caixa. Escreva o troco.")
p(u"p15enun", u"Folha quinze. Agora os preços têm centavos. Escreva o troco de cada compra.")
for k, T in TROCO.items():
    P = PROD[T[u"p"]]
    p(u"tro_" + k, P[u"n"] + u", " + rsf(P[u"p"]) + u". Pagou com " + rsf(T[u"pago"]) + u".")
    p(u"certo_" + k, u"Isso! O troco é " + rsf(T[u"v"]) + u".")
    p(u"dica_" + k, u"Tire o preço do que foi pago. Se ajudar, conte de cabeça do preço "
                    u"até o valor pago.")
for k, Z in TROCOC.items():
    p(u"troc_" + k, Z[u"fr"])
    p(u"certo_" + k, u"Isso! O troco é " + rsf(Z[u"v"]) + u".")
    p(u"dica_" + k, u"Os centavos também entram na conta. Se faltar centavo para tirar, "
                    u"empreste um real: ele vale cem centavos.")

# ---- folha 16 — a pegadinha da soma ---------------------------------------
p(u"p16enun", u"Folha dezesseis. Cuidado: uma das respostas é a soma, não o troco. "
              u"Toque no troco certo.")
for k, K in TROCO4.items():
    for v in K[u"o"]:
        _v(v)
    p(u"q4_" + k, u"Comprou " + K[u"nome"] + u" por " + rsf(K[u"preco"]) +
                  u" e pagou com " + rsf(K[u"pago"]) + u".")
    p(u"certo_" + k, u"Isso! O troco é " + rsf(K[u"v"]) + u".")
    p(u"dica_" + k, u"Olhe bem: o troco é menor que o dinheiro que você deu. Uma das "
                    u"respostas é maior — essa é a soma.")

# ---- folha 17 — qual punhado é o troco ------------------------------------
p(u"p17enun", u"Folha dezessete. O troco foi este valor. Puxe para a mão o punhado de "
              u"dinheiro que vale o mesmo, ou toque nele.")
for k, H in TROCOP.items():
    for j, gr in enumerate(H[u"o"]):
        p(u"pun_" + k + u"_" + str(j), u", ".join(DIN[x][u"n"] for x in gr) + u".")
    p(u"certo_" + k, u"Isso! Esse punhado dá " + rsf(H[u"v"]) + u".")
    p(u"dica_" + k, u"Some cada punhado antes de escolher. Um deles passa do troco e "
                    u"outro não chega.")

# ---- folha 18 — pagar sem troco -------------------------------------------
p(u"p18enun", u"Folha dezoito. Marque as notas e as moedas que juntas dão o valor exato "
              u"da compra, sem sobrar troco. Depois toque em Conferir.")
for k, X in SEMTROCO.items():
    p(u"ex_" + k, u"A compra custou " + rsf(X[u"alvo"]) + u".")
    p(u"certo_" + k, u"Isso! Juntas elas dão " + rsf(X[u"alvo"]) + u" certinhos.")
    p(u"dica_" + k, u"Comece pela maior que ainda cabe e vá completando. Se passar do "
                    u"valor, tire uma e tente outra.")

# ---- folha 19 — quanto falta ----------------------------------------------
p(u"p19enun", u"Folha dezenove. Toque na cédula que dá exatamente o que falta para a compra.")
for k, G in FALTA.items():
    p(u"fal_" + k, u"Tem " + rsf(G[u"tem"]) + u" e precisa de " + rsf(G[u"quer"]) + u".")
    p(u"certo_" + k, u"Isso! Faltavam " + rsf(G[u"quer"] - G[u"tem"]) + u".")
    p(u"dica_" + k, u"Tire o que ela já tem do que ela precisa. A cédula certa é a que "
                    u"dá esse tanto exato, sem sobrar.")

# ---- folha 20 — trocar a cédula -------------------------------------------
p(u"p20enun", u"Folha vinte. Puxe o número certo até a cédula trocada, ou toque nele.")
for k, R in TROCA.items():
    for n in R[u"o"]:
        _n(n)
    p(u"trc_" + k, u"Trocou a " + DIN[R[u"de"]][u"n"] + u" por " + DIN[R[u"por"]][u"n"] +
                   u". Quantas recebeu?")
    p(u"certo_" + k, u"Isso! " + str(R[u"v"]) + u" cédulas.")
    p(u"dica_" + k, u"Quantas vezes a cédula menor cabe dentro da maior? É uma divisão.")

# ---- folha 21 — quantas moedas --------------------------------------------
p(u"p21enun", u"Folha vinte e um. Só há moedas desta: quantas são precisas para dar o valor?")
for k, A in MOEDAS.items():
    for n in A[u"o"]:
        _n(n)
    p(u"moe_" + k, rsf(A[u"total"]).capitalize() + u", só com " + DIN[A[u"moeda"]][u"n"] + u".")
    p(u"certo_" + k, u"Isso! São " + str(A[u"v"]) + u" moedas.")
    p(u"dica_" + k, u"Quantas moedas dessas cabem em um real? Agora veja quantos reais "
                    u"você precisa juntar.")

# ---- folha 22 — a divisão no comércio -------------------------------------
p(u"p22enun", u"Folha vinte e dois. Quantos pacotes, caixas ou sacos dá para fazer? "
              u"Escreva o número.")
for k, N in DIVCOM.items():
    p(u"pro_" + k, N[u"fr"])
    p(u"certo_" + k, u"Isso! São " + str(N[u"v"]) + u".")
    p(u"dica_" + k, u"Divida o total pelo tanto que cabe em cada um. Pense: quantas "
                    u"vezes esse tanto cabe no total?")

# ---- folha 23 — as prestações ---------------------------------------------
p(u"p23enun", u"Folha vinte e três. O preço foi dividido em prestações iguais. Escreva "
              u"quanto é cada prestação.")
for k, B in PRESTA.items():
    p(u"pre_" + k, u"Comprou " + B[u"o"] + u" por " + rsf(B[u"total"]) + u", em " +
                   str(B[u"n"]) + u" prestações iguais.")
    p(u"certo_" + k, u"Isso! Cada prestação é " + rsf(B[u"v"]) + u".")
    p(u"dica_" + k, u"Reparta o preço todo pelo número de prestações. É o contrário de "
                    u"multiplicar.")

# ---- folha 24 — quantos foram vendidos ------------------------------------
p(u"p24enun", u"Folha vinte e quatro. Sabendo o preço de um e quanto foi arrecadado, "
              u"toque em quantos foram vendidos.")
for k, S in VENDIDOS.items():
    for n in S[u"o"]:
        _n(n)
    p(u"ven_" + k, u"Cada um custa " + rsf(S[u"preco"]) + u". A venda arrecadou " +
                   rsf(S[u"total"]) + u".")
    p(u"certo_" + k, u"Isso! Foram " + str(S[u"v"]) + u" " + S[u"coisa"] + u".")
    p(u"dica_" + k, u"Divida tudo o que entrou pelo preço de um só. O resultado é "
                    u"quantos foram vendidos.")

# ---- folhas 25, 28 e 30 — as gavetas --------------------------------------
GPEDE = {
  u"resto": (25, u"Folha vinte e cinco. Leia cada divisão e ponha na gaveta certa: dá "
                 u"certinho, ou sobra alguma coisa?"),
  u"partes": (28, u"Folha vinte e oito. Cada palavra é o nome de uma parte da conta. "
                  u"Ponha na gaveta da operação dela."),
  u"ganho": (30, u"Folha trinta. Compare o que pagou com o que recebeu e ponha cada "
                 u"venda na gaveta certa."),
}
GCERTO = {
  u"resto": (u"Isso! Nesta a divisão fecha sem sobrar nada.",
             u"Isso! Nesta sobra alguma coisa: é o resto."),
  u"partes": (u"Isso! Essa palavra é da multiplicação.",
              u"Isso! Essa palavra é da divisão."),
}
for gk, G in GAV.items():
    pi, pede = GPEDE[gk]
    p(u"p%denun" % pi, pede)
    for C in G[u"cols"]:
        p(u"gav_" + gk + u"_" + C[u"k"], C[u"n"] + u".")
    for n, P in G[u"pal"].items():
        p(u"diz2_" + gk + u"_" + n, P[u"p"] + u".")
        if gk == u"resto":
            p(u"certo%d_%s" % (pi, n), u"Isso! " + (
                u"Essa divisão dá certinho." if P[u"c"] == u"cert"
                else u"Nessa sobra alguma coisa."))
            p(u"dica%d_%s" % (pi, n), u"Faça a divisão de cabeça e veja se termina sem "
                                      u"sobrar. Se sobrar, é a outra gaveta.")
        elif gk == u"partes":
            p(u"certo%d_%s" % (pi, n), u"Isso! " + (
                u"Essa palavra é da multiplicação." if P[u"c"] == u"mult"
                else u"Essa palavra é da divisão."))
            p(u"dica%d_%s" % (pi, n), u"Pergunte-se: essa palavra aparece quando eu junto "
                                      u"parcelas iguais, ou quando eu reparto?")
        else:
            p(u"certo%d_%s" % (pi, n), u"Isso! " + {
                u"lucro": u"Vendeu por mais do que pagou: teve lucro.",
                u"prej": u"Vendeu por menos do que pagou: teve prejuízo.",
                u"igual": u"Vendeu pelo mesmo preço: não ganhou nem perdeu."}[P[u"c"]])
            p(u"dica%d_%s" % (pi, n), u"Compare os dois valores: o que ele recebeu é "
                                      u"maior, menor ou igual ao que ele pagou?")

# ---- folha 26 — e quanto sobra --------------------------------------------
p(u"p26enun", u"Folha vinte e seis. Estas divisões não dão certinho. Escreva quanto "
              u"sobra em cada uma.")
for k, O in RESTO.items():
    p(u"res_" + k, O[u"fr"] + u". " + str(O[u"a"]) + u" dividido por " + str(O[u"b"]) +
                   u" dá " + str(O[u"q"]) + u" para cada um.")
    p(u"certo_" + k, u"Isso! Sobram " + str(O[u"r"]) + u".")
    p(u"dica_" + k, u"Multiplique o que cada um recebeu pelo número de pessoas. O que "
                    u"faltar para o total é o que sobra.")

# ---- folha 27 — a prova real ----------------------------------------------
p(u"p27enun", u"Folha vinte e sete. Toque numa divisão de um lado e, do outro, na "
              u"multiplicação que prova que ela está certa.")
for k, V in PROVA.items():
    p(u"div_" + k, str(V[u"a"]) + u" dividido por " + str(V[u"b"]) + u" é igual a " +
                   str(V[u"q"]) + u".")
    p(u"mul_" + k, str(V[u"q"]) + u" vezes " + str(V[u"b"]) + u" é igual a " +
                   str(V[u"a"]) + u".")
    p(u"certo27_" + k, u"Isso! Multiplicar de volta devolve o número de onde a gente "
                       u"partiu — é a prova real.")
    p(u"dica27_" + k, u"Pegue o resultado da divisão e multiplique pelo número que "
                      u"dividiu. Tem de voltar ao mesmo lugar.")

# ---- folha 29 — o lucro ---------------------------------------------------
p(u"p29enun", u"Folha vinte e nove. O lucro é o que sobra: o que vendeu menos o que "
              u"pagou. Escreva o lucro de cada venda.")
for k, L in LUCRO.items():
    p(u"luc_" + k, u"Comprou " + L[u"coisa"] + u" por " + rsf(L[u"c"]) + u" e vendeu "
                   u"por " + rsf(L[u"v"]) + u".")
    p(u"certo_" + k, u"Isso! O lucro foi " + rsf(L[u"r"]) + u".")
    p(u"dica_" + k, u"Tire o que ele pagou do que ele recebeu. O que sobra é o lucro.")

# ---- folha 31 — comprei para vender ---------------------------------------
p(u"p31enun", u"Folha trinta e um. Comprei " + str(ATACADO[u"quantos"]) + u" pacotes de "
              u"suspiro por " + rsf(ATACADO[u"custo"]) + u" e vou vender cada pacote por " +
              rsf(ATACADO[u"venda"]) + u". Responda as perguntas, uma de cada vez.")
_ATA = {
  u"c1": (u"Vendendo todos os " + str(ATACADO[u"quantos"]) + u" pacotes, quanto vou receber?",
          ATACADO[u"c1"][u"v"],
          u"Multiplique o preço de um pacote pelo número de pacotes."),
  u"c2": (u"Quanto eu já tinha gastado na compra?", ATACADO[u"c2"][u"v"],
          u"Esse número já está escrito no começo da folha: é o que eu paguei pelos "
          u"pacotes todos."),
  u"c3": (u"Então, qual foi o lucro?", ATACADO[u"c3"][u"v"],
          u"Compare o que entrou com o que saiu. O lucro é a diferença."),
  u"c4": (u"E se cada pacote fosse vendido por " + rsf(ATACADO[u"vendabaixa"]) +
          u", quanto eu receberia?", ATACADO[u"c4"][u"v"],
          u"Multiplique de novo, agora pelo preço menor. Repare se ainda sobra alguma "
          u"coisa depois de pagar a compra."),
}
for k, (t, v, dc) in _ATA.items():
    p(u"ata_" + k, t)
    p(u"certo_" + k, u"Isso! " + rsf(v).capitalize() + u".")
    p(u"dica_" + k, dc)

# ---- folha 32 — metade do preço -------------------------------------------
p(u"p32enun", u"Folha trinta e dois. Hoje a loja dá metade de desconto. Escreva quanto "
              u"se paga agora.")
for k, M in METADE.items():
    p(u"met_" + k, u"Sem desconto, " + M[u"coisa"] + u" custa " + rsf(M[u"p"]) + u".")
    p(u"certo_" + k, u"Isso! Com metade de desconto, paga-se " + rsf(M[u"v"]) + u".")
    p(u"dica_" + k, u"Metade é o preço repartido em duas partes iguais. Divida por dois.")

# ---- folha 33 — a quarta parte e a décima parte ---------------------------
p(u"p33enun", u"Folha trinta e três. Cada etiqueta diz quanto de desconto. Toque no "
              u"preço que a pessoa vai pagar.")
for k, PT in PARTE.items():
    for v in PT[u"o"]:
        _v(v)
    p(u"par_" + k, PT[u"coisa"].capitalize() + u" custa " + rsf(PT[u"p"]) + u", com " +
                   PT[u"pc"].replace(u"%", u" por cento") + u" de desconto, que é " +
                   PT[u"nome"] + u" do preço.")
    p(u"certo_" + k, u"Isso! O desconto é " + rsf(PT[u"desc"]) + u", então paga-se " +
                     rsf(PT[u"v"]) + u".")
    p(u"dica_" + k, u"Ache primeiro quanto vale o desconto. Só depois tire ele do preço "
                    u"— a resposta é o que SOBRA para pagar.")

# ---- folha 34 — desconto e depois o troco ---------------------------------
p(u"p34enun", u"Folha trinta e quatro. Duas contas, uma de cada vez: tire o desconto e "
              u"depois descubra o troco.")
for k, E in DUAS.items():
    p(u"dua_" + k, E[u"coisa"].capitalize() + u" custa " + rsf(E[u"p"]) + u" e tem " +
                   rsf(E[u"desc"]) + u" de desconto. Pagou com " + rsf(E[u"pago"]) + u".")
    p(u"certo_" + k, u"Isso! Com o desconto ficou " + rsf(E[u"novo"]) + u", então o "
                     u"troco é " + rsf(E[u"v"]) + u".")
    p(u"dica_" + k, u"Uma conta de cada vez: primeiro tire o desconto do preço. O novo "
                    u"preço é que entra na conta do troco.")

# ---- folhas 35 e 36 — os dois mercados ------------------------------------
p(u"p35enun", u"Folha trinta e cinco. A Bia vai fazer um bolo. Some a lista dela nos "
              u"dois mercados e responda.")
p(u"p36enun", u"Folha trinta e seis. Agora a conta da economia: escreva quanto a Bia "
              u"deixa de gastar em cada coisa.")
_MK = {
  u"mk1": (u"Qual é o total no Mercado do Povo?",
           u"Isso! No Mercado do Povo a lista dá " + rsf(MERCADO[u"totalPovo"]) + u".",
           u"Some os seis preços da coluna do Mercado do Povo. Cuidado com os ovos: são três."),
  u"mk2": (u"E qual é o total no Mercado Economize?",
           u"Isso! No Economize a lista dá " + rsf(MERCADO[u"totalEco"]) + u".",
           u"Some os seis preços da outra coluna, do mesmo jeito."),
  u"mk3": (u"Qual produto custa mais no Economize do que no Povo?",
           u"Isso! A manteiga é o único que fica mais caro no Economize.",
           u"Compare linha por linha. Em quase todas o Economize é mais barato — "
           u"procure a que foge disso."),
  u"mk4": (u"Onde a Bia deve comprar para economizar?",
           u"Isso! Somando a lista inteira, o Economize sai mais barato.",
           u"Não olhe um produto só: é a lista toda que decide."),
}
for k, (t, ce, dc) in _MK.items():
    p(u"mer_" + k, t)
    p(u"certo_" + k, ce)
    p(u"dica_" + k, dc)
p(u"mtx_mk3_manteiga", u"Manteiga.")
p(u"mtx_mk3_farinha", u"Farinha de trigo.")
p(u"mtx_mk3_leite", u"Leite.")
p(u"mtx_mk4_eco", u"Mercado Economize.")
p(u"mtx_mk4_povo", u"Mercado do Povo.")
_EC = {
  u"ec1": (u"Na lista inteira, quanto a Bia economiza comprando no Economize?",
           MERCADO[u"economia"],
           u"Tire o total menor do total maior. A diferença é a economia."),
  u"ec2": (u"Só nos três ovos, quanto ela economiza?", 225,
           u"Calcule quanto custam três ovos em cada mercado e compare."),
  u"ec3": (u"E na farinha de trigo?", 165,
           u"Olhe só a linha da farinha, nas duas colunas."),
  u"ec4": (u"E no litro de leite?", 240,
           u"Olhe só a linha do leite, nas duas colunas."),
  u"ec5": (u"A manteiga é mais cara no Economize. Quanto a mais?", 35,
           u"Aqui a diferença é ao contrário: o preço do Economize é o maior."),
}
for k, (t, v, dc) in _EC.items():
    p(u"eco_" + k, t)
    p(u"certo_" + k, u"Isso! São " + rsf(v) + u".")
    p(u"dica_" + k, dc)

# ---- folha 37 — os combos -------------------------------------------------
p(u"p37enun", u"Folha trinta e sete. Quantas combinações diferentes a loja consegue "
              u"oferecer? Toque no número certo.")
for k, B in COMBO.items():
    for n in B[u"o"]:
        _n(n)
    p(u"cmb_" + k, B[u"fr"])
    p(u"certo_" + k, u"Isso! São " + str(B[u"v"]) + u" combinações diferentes.")
    p(u"dica_" + k, u"Para cada escolha do primeiro grupo, quantas do segundo cabem? "
                    u"Multiplique as quantidades.")

# ---- folha 38 — o cartaz --------------------------------------------------
p(u"p38enun", u"Folha trinta e oito. Para o cartaz da lojinha da turma: marque tudo o "
              u"que é verdade sobre comprar e vender. Depois toque em Conferir.")
for FR in CARTAZ[u"frases"]:
    p(u"car_" + FR[u"k"], FR[u"t"])
p(u"certo_cartaz", u"Isso! O cartaz está pronto, e tudo o que ficou nele é verdade.")
p(u"dica_cartaz", u"Leia uma frase de cada vez e pense num exemplo. Se o exemplo não "
                  u"funcionar, a frase não entra no cartaz.")

# ---- as falas que muitas folhas compartilham ------------------------------
for v in sorted(VALORES):
    p(u"val_" + str(v), rsf(v).capitalize() + u".")
for n in sorted(NUMEROS):
    p(u"num_" + str(n), str(n) + u".")


# ==============================================================================
#  AS SÍLABAS FALADAS — e este bloco é obrigatório em caderno que fale sílaba
#
#  ⚠️⚠️ POR QUE NÃO DÁ PARA SINTETIZAR A SÍLABA SOLTA (e a casa já pagou por
#     isto DUAS vezes — set/2026 e 16/set/2026, as duas o Marcos ouvindo):
#     a voz não lê SOM, lê PALAVRA. Entregue "SA" a ela e ela soletra "esse-á";
#     "VA" vira "vê-á"; "ÇÃ" ela nem tenta, porque ç não começa palavra em
#     português. Escrever a sílaba "como se fala" conserta UM caso e nunca
#     fecha a família.
#
#  O QUE FUNCIONA é o contrário: gravar a PALAVRA INTEIRA — que a voz pronuncia
#  certo, porque é palavra de verdade — alinhar letra a letra com o
#  `ctc-forced-aligner` e CORTAR a sílaba de dentro dela. Quem faz isso é o
#  `_padrao/silabas_voz.py`, dentro do `entregar.yml`, lendo o `silabas.json`
#  que sai daqui. O portão é o `_qa/silabas.py`.
#
#  COMO SE USA: para cada palavra do caderno, uma linha
#      _reg(u"CAVALO", [u"CA", u"VA", u"LO"])
#  e, no app, a sílaba fala por `falarSilaba(null, 0, "VA")` — nunca por
#  `falar("sil_va")`. Caderno que não fala sílaba não escreve nada: o
#  `silabas.json` sai com `"palavras": {}` e o `entregar.yml` nem baixa o
#  alinhador por ele.
#
#  ⚠️ NÃO HÁ FALA DE RESERVA POR SÍLABA. Faltando o recorte, o app diz a
#     PALAVRA INTEIRA. Uma reserva sintetizada seria o defeito voltando pela
#     porta dos fundos — e calado, que é pior.
# ==============================================================================
_SIL_DE = {}          # palavra -> [sílabas, NA ORDEM da palavra]
_MAPA_SIL = {}        # sílaba  -> [palavra, posição]
_RECUSADAS = []


def _reg(palavra, silabas):
    u"""⚠️ A LISTA TEM DE ESTAR NA ORDEM DA PALAVRA. O alinhador corta pelos
    limites das letras: ["RO","CAR"] para CARRO faz sair "ro" onde devia sair
    "car" — e a criança ouve o pedaço errado, sem erro nenhum na tela. Folha de
    ORDENAR guarda as sílabas EMBARALHADAS: passe-as por `_ordena` antes.
    ⚠️ E ganha sempre a partição MAIS FINA: "PIPO"+"CA" fecha PIPOCA sem ser
    separação silábica, e sobrescrevendo PI-PO-CA deixaria a sílaba PI muda."""
    silabas = list(silabas)
    if u"".join(silabas).upper() != palavra.upper():
        _RECUSADAS.append((palavra, silabas))
        return
    velha = _SIL_DE.get(palavra.lower())
    if velha and len(velha) >= len(silabas):
        return
    _SIL_DE[palavra.lower()] = silabas


def _ordena(palavra, embaralhadas):
    u"""as mesmas sílabas na ORDEM em que formam a palavra — sem inventar
    nenhuma: encaixa da esquerda para a direita e desiste se não fechar."""
    resto, saida, alvo = list(embaralhadas), [], palavra.upper()
    while alvo:
        for _i, _sb in enumerate(resto):
            if alvo.startswith(_sb.upper()):
                saida.append(_sb)
                alvo = alvo[len(_sb):]
                resto.pop(_i)
                break
        else:
            return None
    return saida if not resto else None


def _achaSilaba(s):
    u"""a palavra de onde a sílaba será recortada. Ganha a MAIS CURTA: menos
    letras na gravação, menos lugar para o alinhador errar."""
    cand = [_w for _w in sorted(_SIL_DE) if s in _SIL_DE[_w]]
    if not cand:
        return None
    _w = min(cand, key=lambda w: (len(_SIL_DE[w]), len(w), w))
    return [_w, _SIL_DE[_w].index(s)]


def _mapeia(soltas):
    u"""monta o SILMAP das sílabas que o app fala sozinhas, e DEVOLVE as órfãs.
    ⚠️ Sílaba órfã não é erro — o app diz a palavra inteira — mas tem de sair
    IMPRESSA, senão aquele botão emudece sem ninguém saber. Distratora que não
    mora em palavra nenhuma do caderno pede uma PALAVRA-CARREGADORA: uma
    palavra de verdade, curta, registrada só para ser gravada e cortada."""
    orfas = []
    for _s in sorted(set(soltas)):
        _achou = _achaSilaba(_s)
        if _achou:
            _MAPA_SIL[_s] = _achou
        else:
            orfas.append(_s)
    # e a PALAVRA INTEIRA de cada uma precisa existir como fala: é dela que o
    # recorte sai, e é ela que o app diz quando o recorte falta.
    for _w in sorted(_SIL_DE):
        p(u"pal_" + ch(_w), _w.upper() + u".")
    return orfas


_ORFAS = _mapeia([])          # <- passe aqui TODA sílaba que o app fala sozinha


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
    falas.append({u"id": PREFIXO + c, u"texto": txt, u"voz": VOZ})

html = io.open(CAM, encoding=u"utf-8").read()
blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)

# ⭐ o `silabas.json` é o que o `entregar.yml` lê para cortar cada sílaba de
#    dentro do mp3 da palavra inteira, e o `SILMAP` é o que o app usa para saber
#    de qual palavra veio cada pedaço. Uma fonte só para os dois.
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ,
                u"palavras": dict((w, _SIL_DE[w]) for w in sorted(_SIL_DE))},
               ensure_ascii=False, indent=1))
blocoS = (u"/*SILMAP-INI*/var SILMAP = "
          + json.dumps(_MAPA_SIL, ensure_ascii=False, sort_keys=True) + u";/*SILMAP-FIM*/")
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/", lambda m: blocoS, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)
io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
print(u"FALAS: %d chaves; falas.json: %d fala(s) para gravar; "
      u"silabas: %d palavra(s) para recortar, %d silaba(s) no mapa"
      % (len(F), len(falas), len(_SIL_DE), len(_MAPA_SIL)))
if _ORFAS:
    print(u"   \u26a0\ufe0f %d silaba(s) SEM palavra de origem (o app dira a palavra "
          u"inteira): %s" % (len(_ORFAS), u", ".join(_ORFAS)))
if _RECUSADAS:
    print(u"   \u26a0\ufe0f %d lista(s) recusada(s) por nao formarem a palavra: %s"
          % (len(_RECUSADAS), u", ".join(
              u"%s=%s" % (w, u"-".join(sl)) for w, sl in _RECUSADAS[:8])))
