# -*- coding: utf-8 -*-
u"""GERA O POTE E AS FALAS DA COROA DOS CINCO REINOS (seres vivos, 4º ano).

⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada;
   texto mudou = voz regravada. MP3 não se lê, então é este arquivo que permite
   conferir o que a criança OUVE.

⚠️ ESTE SCRIPT GERA TAMBÉM O POTE (`/*ITENS-INI*/`), e isso é de propósito: com
   dois donos (pote no `index.html`, falas aqui) os dois já divergiram mais de
   uma vez, e item no pote sem fala = a criança toca e o app fica mudo.

⭐ DE ONDE VEM CADA FIGURA, E POR QUE ISSO É O CORAÇÃO DESTE ARQUIVO:
   as 45 figuras deste caderno foram RECORTADAS DAS PRÓPRIAS FOLHAS DE PAPEL
   (`recortar_das_folhas.py`, e o `img/ORIGEM.json` diz de qual folha veio cada
   uma). A d26 deu as vinte coloridas, a d20 e a d22 as vinte de traço, e a d07
   — a folha da COROA — deu a figura-emblema de cada reino. Nenhuma veio do
   banco. É a ordem do Marcos de 14/set/2026 (*"aproveite as imagens"*) e a
   regra que o portão 1i5 passou a medir no mesmo dia.

⚠️ O QUE ESTE CADERNO **NÃO** TEM, e está dito para não virar mentira por
   omissão: das 40 folhas colhidas, só a d07 traz figura de FUNGO, de ALGA e de
   BACTÉRIA — uma de cada. Então os três reinos microscópicos aparecem sempre
   com a MESMA figura, a da coroa. Reino com uma figura só não dá para montar
   "ache o intruso" nem "cinco gavetas cheias" — por isso esses gestos usam
   ANIMAIS e PLANTAS, que a colheita tem de sobra, e a folha 20 leva um ser de
   cada reino, não vários.

⚠️ E O TETO DA REDE: Blumenau, 4º ano, manda *"Seres unicelulares e
   multicelulares"*, *"Seres microscópicos (uso de lupa e microscópio)"* e
   *"Relacionar a participação de fungos e bactérias no processo de
   decomposição"*. O critério do NÚCLEO (procarionte × eucarionte) **não** está
   no currículo do ano: entrou por encargo do Marcos, e por isso entra em
   linguagem de criança (o "cofrinho da receita"), nunca como palavra a decorar.
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"rn_"
VOZ = u"pt-BR-AntonioNeural"

# ============================================================
#  OS CINCO REINOS — a mesma tabela que o `folhas.js` carrega em `REINOS`.
#  ⚠️ Se mudar aqui, muda lá: é a única duplicação do caderno, e ela existe
#     porque a fala precisa do dado em Python e a tela precisa dele em JS.
# ============================================================
REINOS = {
    u"animais":   {u"dia": u"ANIMAIS",   u"ap": u"Animalia", u"fig": u"reino_animal",
                   u"cel": u"muitas", u"com": u"come",    u"cof": u"tem",
                   u"quem": u"o cachorro, a borboleta, o peixe e você"},
    u"plantas":   {u"dia": u"PLANTAS",   u"ap": u"Plantae",  u"fig": u"reino_plantae",
                   u"cel": u"muitas", u"com": u"fabrica", u"cof": u"tem",
                   u"quem": u"a árvore, o milho, a rosa e o tomateiro"},
    u"fungos":    {u"dia": u"FUNGOS",    u"ap": u"Fungi",    u"fig": u"reino_fungi",
                   u"cel": u"muitas", u"com": u"come",    u"cof": u"tem",
                   u"quem": u"o cogumelo, o bolor do pão e o fermento do bolo"},
    u"algas":     {u"dia": u"ALGAS",     u"ap": u"Protista", u"fig": u"reino_protista",
                   u"cel": u"uma",    u"com": u"fabrica", u"cof": u"tem",
                   u"quem": u"a ameba, o paramécio e as algas do mar"},
    u"bacterias": {u"dia": u"BACTÉRIAS", u"ap": u"Monera",   u"fig": u"reino_monera",
                   u"cel": u"uma",    u"com": u"come",    u"cof": u"nao",
                   u"quem": u"as bactérias, que só se veem no microscópio"},
}
ORDEM = [u"animais", u"plantas", u"fungos", u"algas", u"bacterias"]
# como a voz diz o nome do reino dentro de uma frase (a tela escreve em caixa alta)
DIZR = {u"animais": u"animais", u"plantas": u"plantas", u"fungos": u"fungos",
        u"algas": u"algas", u"bacterias": u"bactérias"}

# ============================================================
#  AS FIGURAS — o nome falado, o artigo e a que reino pertencem.
#  ⚠️ O NOME NÃO É A CHAVE DO ARQUIVO. `urso_pelucia` é o PNG; o que a criança
#     lê e o leitor de tela anuncia é "o urso de pelúcia". Este mapa vai junto
#     com o pote (`FIGNOME`) para a tela.
#  ⚠️ A COLUNA `vida`: "vivo" · "foi" (já foi vivo: era madeira, era trigo) ·
#     "nunca". Ela sai das PRÓPRIAS folhas — a d26 e a d22 já dizem quem é vivo
#     e quem não é, e a d40 é a que abre a terceira gaveta.
# ============================================================
FIG = [
    # chave            nome falado            vida     reino
    (u"arvore",        u"a árvore",           u"vivo",  u"plantas"),
    (u"arvore2",       u"a árvore",           u"vivo",  u"plantas"),
    (u"arvore3",       u"a árvore",           u"vivo",  u"plantas"),
    (u"rosa",          u"a rosa",             u"vivo",  u"plantas"),
    (u"milho",         u"o pé de milho",      u"vivo",  u"plantas"),
    (u"tomateiro",     u"o pé de tomate",     u"vivo",  u"plantas"),
    (u"reino_plantae", u"as folhas",          u"vivo",  u"plantas"),
    (u"sapo",          u"o sapo",             u"vivo",  u"animais"),
    (u"passarinho",    u"o passarinho",       u"vivo",  u"animais"),
    (u"borboleta",     u"a borboleta",        u"vivo",  u"animais"),
    (u"borboleta2",    u"a borboleta",        u"vivo",  u"animais"),
    (u"borboleta3",    u"a mariposa",         u"vivo",  u"animais"),
    (u"formiga",       u"a formiga",          u"vivo",  u"animais"),
    (u"cavalo",        u"o cavalo",           u"vivo",  u"animais"),
    (u"cachorro",      u"o cachorro",         u"vivo",  u"animais"),
    (u"elefante",      u"o elefante",         u"vivo",  u"animais"),
    (u"tubarao",       u"o tubarão",          u"vivo",  u"animais"),
    (u"menino",        u"o menino",           u"vivo",  u"animais"),
    (u"bebe",          u"o bebê",             u"vivo",  u"animais"),
    (u"reino_animal",  u"a borboleta",        u"vivo",  u"animais"),
    (u"reino_fungi",   u"os cogumelos",       u"vivo",  u"fungos"),
    (u"reino_protista", u"a ameba",           u"vivo",  u"algas"),
    (u"reino_monera",  u"a bactéria",         u"vivo",  u"bacterias"),
    # já foram vivos — a terceira gaveta da d40
    (u"lapis",         u"o lápis",            u"foi",   None),
    (u"lanche",        u"o lanche",           u"foi",   None),
    (u"cupcake",       u"o cupcake",          u"foi",   None),
    # nunca viveram
    (u"agua",          u"a água",             u"nunca", None),
    (u"areia",         u"a areia",            u"nunca", None),
    (u"pedras",        u"as pedras",          u"nunca", None),
    (u"pedras2",       u"as pedras",          u"nunca", None),
    (u"terra",         u"a terra",            u"nunca", None),
    (u"sol",           u"o sol",              u"nunca", None),
    (u"sol2",          u"o sol",              u"nunca", None),
    (u"nuvem",         u"a nuvem",            u"nunca", None),
    (u"vento",         u"o vento",            u"nunca", None),
    (u"fogo",          u"o fogo",             u"nunca", None),
    (u"carro",         u"o carro",            u"nunca", None),
    (u"casa",          u"a casa",             u"nunca", None),
    (u"tijolos",       u"os tijolos",         u"nunca", None),
    (u"celular",       u"o celular",          u"nunca", None),
    (u"bola",          u"a bola",             u"nunca", None),
    (u"urso_pelucia",  u"o urso de pelúcia",  u"nunca", None),
    (u"urso_pelucia2", u"o ursinho de pano",  u"nunca", None),
]
# ⚠️ `gelo` e `sapo2` SAÍRAM do pote, e está dito para não parecer esquecimento:
#    as duas foram recortadas e estão em `img/`, mas o desenho original é de
#    traço claríssimo (a geleira da d26 e o sapo da d22) e, na tela do PC da
#    escola, viram um rabisco que a criança não reconhece. Figura que não se
#    reconhece não é ilustração: é adivinhação.

NOMEF = dict((f[0], f[1]) for f in FIG)
VIDA = dict((f[0], f[2]) for f in FIG)
DEQUEM = dict((f[0], f[3]) for f in FIG)
VIVOS = [f[0] for f in FIG if f[2] == u"vivo"]
FOI = [f[0] for f in FIG if f[2] == u"foi"]
NUNCA = [f[0] for f in FIG if f[2] == u"nunca"]
NAOVIVO = FOI + NUNCA
DOREINO = dict((k, [f[0] for f in FIG if f[3] == k]) for k in ORDEM)
# os que a criança vê a olho nu e reconhece: servem de peça em qualquer folha
BICHOS = [w for w in DOREINO[u"animais"] if w != u"reino_animal"]
PLANTAS = [w for w in DOREINO[u"plantas"] if w != u"reino_plantae"]


def cap(t):
    return t[:1].upper() + t[1:] if t else t


def semart(w):
    u"""o nome sem o artigo — para entrar depois de "do", "da", "no"…"""
    n = NOMEF[w]
    for a in (u"o ", u"a ", u"os ", u"as "):
        if n.startswith(a):
            return n[len(a):]
    return n


# ============================================================
#  O POTE — item por item, folha por folha
# ============================================================
IT = {}


def gira(lista, i, n):
    u"""pega n da lista começando em i, dando a volta (potes sem repetição
    dentro do mesmo item e sem sempre a mesma ordem entre itens)."""
    return [lista[(i + k) % len(lista)] for k in range(n)]


# ---- folha 1: circule os seres vivos (d39) ------------------------------
IT[u"p1"] = []
for i in range(10):
    viv = gira(VIVOS, i * 2, 2)
    nao = gira(NUNCA, i * 3, 4)
    IT[u"p1"].append({u"vivos": viv, u"todos": viv + nao})

# ---- folha 2: ache os seres vivos na cena (d33) -------------------------
IT[u"p2"] = []
for i in range(10):
    viv = gira(VIVOS, i * 3 + 1, 3)
    nao = gira(NAOVIVO, i * 4, 5)
    IT[u"p2"].append({u"vivos": viv, u"todos": viv + nao})

# ---- folha 3: duas gavetas, vivo × não vivo (d20, d22, d26) -------------
IT[u"p3"] = []
for i in range(10):
    pe = [[w, u"vivo"] for w in gira(VIVOS, i * 3, 3)]
    pe += [[w, u"nao"] for w in gira(NUNCA, i * 2, 3)]
    IT[u"p3"].append({u"pecas": pe})

# ---- folha 4: três gavetas (d40) ---------------------------------------
IT[u"p4"] = []
for i in range(8):
    pe = [[w, u"vivo"] for w in gira(VIVOS, i * 5, 2)]
    pe += [[w, u"foi"] for w in gira(FOI, i, 2)]
    pe += [[w, u"nunca"] for w in gira(NUNCA, i * 3, 2)]
    IT[u"p4"].append({u"pecas": pe})

# ---- folha 5: o ciclo de vida (d16) ------------------------------------
CICLOS = [
    (u"planta", u"da planta", [u"semente", u"broto", u"planta_com_flor", u"semente_nova"]),
    (u"sapo", u"do sapo", [u"ovo", u"girino", u"girino_com_pernas", u"sapo_adulto"]),
    (u"borboleta", u"da borboleta", [u"ovo", u"lagarta", u"casulo", u"borboleta_adulta"]),
    (u"passarinho", u"do passarinho", [u"ovo", u"filhote", u"passaro_adulto", u"ninho_novo"]),
    (u"menino", u"do ser humano", [u"bebe", u"crianca", u"adulto", u"idoso"]),
    (u"cachorro", u"do cachorro", [u"filhote", u"cachorro_jovem", u"cachorro_adulto", u"cachorro_velho"]),
    (u"milho", u"do pé de milho", [u"semente", u"broto", u"pe_de_milho", u"espiga_com_sementes"]),
    (u"formiga", u"da formiga", [u"ovo", u"larva", u"pupa", u"formiga_adulta"]),
]
IT[u"p5"] = [{u"ser": c[0], u"rot": c[1], u"fases": c[2]} for c in CICLOS]

# ---- folha 6: quantas células (d29, d15) -------------------------------
#     ⚠️ os microscópicos entram pela figura da COROA (é a única que existe)
IT[u"p6"] = []
for i, w in enumerate(gira(BICHOS, 0, 5) + gira(PLANTAS, 0, 4)):
    IT[u"p6"].append({u"w": w, u"r": DEQUEM[w]})
for k in (u"bacterias", u"algas", u"fungos"):
    IT[u"p6"].append({u"w": REINOS[k][u"fig"], u"r": k})

# ---- folha 7: o microscópio (CURRÍCULO) --------------------------------
#     "certo" = dá para ver SEM o microscópio?  sim / nao
IT[u"p7"] = [
    {u"r": u"bacterias", u"rot": u"uma gota de água do lago", u"certo": u"nao"},
    {u"r": u"algas", u"rot": u"uma gota de água do lago", u"certo": u"nao"},
    {u"r": u"fungos", u"rot": u"um cogumelo do quintal", u"certo": u"sim"},
    {u"r": u"plantas", u"rot": u"uma folha da árvore", u"certo": u"sim"},
    {u"r": u"animais", u"rot": u"uma borboleta do jardim", u"certo": u"sim"},
]

# ---- folha 8: de onde vem o alimento (d15, d29) ------------------------
IT[u"p8"] = []
for w in gira(PLANTAS, 0, 4) + gira(BICHOS, 3, 5):
    IT[u"p8"].append({u"w": w, u"r": DEQUEM[w]})
for k in (u"fungos", u"algas", u"bacterias"):
    IT[u"p8"].append({u"w": REINOS[k][u"fig"], u"r": k})

# ---- folha 9: duas gavetas do alimento ---------------------------------
IT[u"p9"] = []
for i in range(8):
    pe = [[w, u"fabrica"] for w in gira(PLANTAS, i, 3)]
    pe += [[w, u"come"] for w in gira(BICHOS, i * 2, 3)]
    IT[u"p9"].append({u"pecas": pe})

# ---- folha 10: o cofrinho da receita (encargo do Marcos) ---------------
IT[u"p10"] = [
    {u"r": u"bacterias", u"rot": u"da bactéria"},
    {u"r": u"animais", u"rot": u"do cachorro"},
    {u"r": u"plantas", u"rot": u"da folha da árvore"},
    {u"r": u"fungos", u"rot": u"do cogumelo"},
    {u"r": u"algas", u"rot": u"da ameba"},
    {u"r": u"bacterias", u"rot": u"do leite azedo"},
    {u"r": u"animais", u"rot": u"da borboleta"},
    {u"r": u"plantas", u"rot": u"do pé de milho"},
]

# ---- folha 11: pinte por legenda (d05) ---------------------------------
#     as cores SÃO as da folha: PLANTAS verde · ANIMAIS vermelho · ALGAS azul ·
#     FUNGOS amarelo · BACTÉRIAS rosa (índices do estojo, na mesma ordem)
CORDOREINO = {u"plantas": 0, u"animais": 1, u"algas": 2, u"fungos": 3, u"bacterias": 4}
IT[u"p11"] = [{u"r": k, u"cor": CORDOREINO[k]} for k in ORDEM]

# ---- folhas 12 e 13: qual é o reino desta figura (d04, d03) ------------
def parescolha(pool, i):
    w = pool[i % len(pool)]
    r = DEQUEM[w]
    outros = [k for k in ORDEM if k != r]
    op = [r, outros[i % len(outros)], outros[(i + 2) % len(outros)]]
    return {u"w": w, u"r": r, u"op": sorted(op, key=lambda k: ORDEM.index(k))}


IT[u"p12"] = [parescolha(BICHOS + PLANTAS, i) for i in range(10)]
IT[u"p13"] = [parescolha(PLANTAS + BICHOS, i + 5) for i in range(7)]
for i, k in enumerate((u"fungos", u"algas", u"bacterias")):
    outros = [x for x in ORDEM if x != k]
    IT[u"p13"].append({u"w": REINOS[k][u"fig"], u"r": k,
                       u"op": sorted([k, outros[i], outros[(i + 2) % len(outros)]],
                                     key=lambda x: ORDEM.index(x))})

# ---- folhas 14 e 15: ligue o ser ao reino (d09, d08, d25) --------------
# ⚠️ CADA ITEM LEVA REINOS DIFERENTES, e isso não é capricho: a primeira versão
#    montava três BICHOS num item só, e a coluna da direita saía com "ANIMAIS"
#    escrito três vezes. A criança que ligasse o cachorro na segunda caixa
#    "ANIMAIS" levaria ERRO por acertar — o motor casa por chave de figura, não
#    por texto. Item de ligar com rótulo repetido é armadilha, não exercício.
MICRO = [u"fungos", u"algas", u"bacterias"]
IT[u"p14"] = []
for i in range(6):
    k = MICRO[i % 3]
    IT[u"p14"].append({u"g": [
        [BICHOS[(i * 2) % len(BICHOS)], u"animais"],
        [PLANTAS[i % len(PLANTAS)], u"plantas"],
        [REINOS[k][u"fig"], k],
    ]})
IT[u"p15"] = []
for i in range(6):
    a, b = MICRO[i % 3], MICRO[(i + 1) % 3]
    terceiro = ([BICHOS[(i * 3) % len(BICHOS)], u"animais"] if i % 2
                else [PLANTAS[(i + 2) % len(PLANTAS)], u"plantas"])
    IT[u"p15"].append({u"g": [
        [REINOS[a][u"fig"], a],
        [REINOS[b][u"fig"], b],
        terceiro,
    ]})

# ---- folhas 16 e 17: a coroa (d07) -------------------------------------
IT[u"p16"] = [{u"r": k} for k in (u"animais", u"plantas", u"fungos")]
IT[u"p17"] = [{u"r": k} for k in (u"algas", u"bacterias", u"plantas", u"animais")]

# ---- folha 18: case o reino com a descrição (d01, d19) -----------------
DESCR = {
    u"animais": u"Tem muitas células, precisa comer outros seres vivos e guarda "
                u"a receita no cofrinho. Anda, nada ou voa.",
    u"plantas": u"Tem muitas células, fabrica o próprio alimento com o Sol e "
                u"guarda a receita no cofrinho. Fica no mesmo lugar.",
    u"fungos": u"Tem muitas células e guarda a receita no cofrinho, mas não "
               u"fabrica alimento: come o que está apodrecendo.",
    u"algas": u"É feito de uma célula só, guarda a receita no cofrinho e quase "
              u"sempre mora na água.",
    u"bacterias": u"É feito de uma célula só e nem cofrinho tem: a receita fica "
                  u"solta dentro dela. É o menor ser vivo de todos.",
}
IT[u"p18"] = []
for i, k in enumerate(ORDEM + [u"fungos", u"plantas", u"bacterias"]):
    outros = [x for x in ORDEM if x != k]
    IT[u"p18"].append({u"r": k, u"txt": DESCR[k],
                       u"op": sorted([k, outros[i % len(outros)],
                                      outros[(i + 2) % len(outros)]],
                                     key=lambda x: ORDEM.index(x))})

# ---- folha 19: complete o quadro (d29) ---------------------------------
IT[u"p19"] = []
for i, k in enumerate(ORDEM + ORDEM):
    IT[u"p19"].append({u"r": k, u"falta": (u"cel", u"com", u"cof")[i % 3]})

# ---- folha 20: as cinco gavetas dos reinos (d06) -----------------------
IT[u"p20"] = []
for i in range(6):
    pe = [[BICHOS[i % len(BICHOS)], u"animais"],
          [PLANTAS[i % len(PLANTAS)], u"plantas"],
          [REINOS[u"fungos"][u"fig"], u"fungos"],
          [REINOS[u"algas"][u"fig"], u"algas"],
          [REINOS[u"bacterias"][u"fig"], u"bacterias"]]
    IT[u"p20"].append({u"pecas": pe, u"gav": list(ORDEM)})

# ---- folha 21: o intruso -----------------------------------------------
IT[u"p21"] = []
for i in range(5):
    todos = gira(BICHOS, i * 2, 3) + [PLANTAS[i % len(PLANTAS)]]
    IT[u"p21"].append({u"r": u"animais", u"todos": todos,
                       u"intruso": PLANTAS[i % len(PLANTAS)]})
for i in range(5):
    todos = gira(PLANTAS, i, 3) + [BICHOS[(i * 3) % len(BICHOS)]]
    IT[u"p21"].append({u"r": u"plantas", u"todos": todos,
                       u"intruso": BICHOS[(i * 3) % len(BICHOS)]})

# ---- folha 22: produtor, consumidor, decompositor (d30) ---------------
TRIO = [u"produtores", u"consumidores", u"decompositores"]
IT[u"p22"] = [
    {u"k": u"planta", u"certo": u"produtores",
     u"txt": u"As plantas fabricam o próprio alimento com a luz do Sol. "
             u"Por isso elas são chamadas de ___."},
    {u"k": u"animal", u"certo": u"consumidores",
     u"txt": u"Os animais não fabricam alimento: eles comem plantas ou outros "
             u"animais. Por isso são chamados de ___."},
    {u"k": u"fungo", u"certo": u"decompositores",
     u"txt": u"Os fungos e as bactérias comem restos de folhas e de bichos "
             u"mortos e devolvem tudo para a terra. Eles são os ___."},
    {u"k": u"tronco", u"certo": u"decompositores",
     u"txt": u"Um tronco caído some devagarinho no meio do mato. Quem faz esse "
             u"trabalho são os ___."},
    {u"k": u"alga", u"certo": u"produtores",
     u"txt": u"As algas do mar também usam a luz do Sol para fabricar alimento. "
             u"Elas são ___."},
    {u"k": u"pao", u"certo": u"decompositores",
     u"txt": u"O bolor que aparece no pão velho é um fungo. Fungos que comem "
             u"restos são ___."},
]
for it in IT[u"p22"]:
    it[u"op"] = list(TRIO)

# ---- folha 23: escreva o nome do reino (d01, d03) ---------------------
# ⚠️ A PISTA NAO PODE CONTER O NOME DO REINO, e isso custou uma rodada de banca
#    (portao 1i4, 14/set/2026): a primeira versao mostrava "o reino de a ameba, o
#    paramecio e as ALGAS do mar" — com a resposta impressa dois centimetros
#    acima do quadro onde a crianca ia escreve-la. Folha de escrever vira folha
#    de copiar, e o relatorio passa a dizer "dominou" sobre copia.
PISTA = {
    u"animais": u"quem precisa comer outros seres vivos e se mexe pelo mundo",
    u"plantas": u"quem fica parado no mesmo lugar e fabrica o alimento com o Sol",
    u"fungos": u"quem come o que está apodrecendo — o cogumelo e o bolor do pão",
    u"algas": u"quem é feito de uma célula só, mora na água e fabrica o alimento",
    u"bacterias": u"quem é feito de uma célula só e nem cofrinho tem",
}
IT[u"p23"] = [{u"r": k, u"pista": PISTA[k]} for k in ORDEM]

# ---- folha 24: do menor ao maior (CURRÍCULO) --------------------------
IT[u"p24"] = [
    {u"ordem": [u"reino_monera", u"reino_protista", u"formiga", u"cachorro"]},
    {u"ordem": [u"reino_monera", u"reino_protista", u"borboleta", u"cavalo"]},
    {u"ordem": [u"reino_protista", u"formiga", u"passarinho", u"elefante"]},
    {u"ordem": [u"reino_monera", u"formiga", u"sapo", u"tubarao"]},
    {u"ordem": [u"reino_protista", u"reino_fungi", u"rosa", u"arvore"]},
    {u"ordem": [u"reino_monera", u"borboleta", u"menino", u"cavalo"]},
]

# ---- folha 25: a minha coroa (o mural do fecho) -----------------------
IT[u"p25"] = []
for i, k in enumerate(ORDEM):
    if k == u"animais":
        ws = gira(BICHOS, 0, 4)
    elif k == u"plantas":
        ws = gira(PLANTAS, 0, 4)
    else:
        ws = [REINOS[k][u"fig"]]
    for w in ws:
        IT[u"p25"].append({u"r": k, u"w": w})


# ============================================================
#  AS FALAS
# ============================================================
F = {}

F[u"capa"] = (u"A Coroa dos Cinco Reinos. Vinte e cinco folhas para descobrir "
              u"como os cientistas separam todos os seres vivos do mundo em "
              u"cinco grandes grupos.")
F[u"quase"] = u"Quase! Olhe de novo e tente outra vez."
F[u"escreva"] = u"Escreva o nome do reino."
F[u"folhaPronta"] = u"Folha pronta! Pode virar a página."
F[u"ligue"] = u"Agora toque no reino a que ele pertence."
F[u"novoCaderno"] = u"Caderno novo! As figuras mudaram."
F[u"vozOn"] = u"Narração ligada!"
F[u"fim"] = (u"Você chegou ao fim da Coroa dos Cinco Reinos! Agora você sabe "
             u"olhar um ser vivo e perguntar três coisas: quantas células ele "
             u"tem, de onde vem o alimento dele e onde a receita fica guardada. "
             u"Com essas três perguntas, qualquer ser vivo do mundo encontra o "
             u"reino dele.")

# ---- o nome de cada ser (o alto-falante de toda peça que a criança toca)
for w in NOMEF:
    F[u"ser_" + w] = cap(NOMEF[w]) + u"."
# ---- o nome de cada reino
for k in ORDEM:
    F[u"reino_" + k] = (u"Reino das %s. São %s."
                        % (DIZR[k], REINOS[k][u"quem"]))

# ---- as opções que se repetem em várias folhas
F[u"op_uma"] = u"Uma célula só."
F[u"op_muitas"] = u"Muitas células."
F[u"op_fabrica"] = u"Fabrica o alimento com o Sol."
F[u"op_come"] = u"Precisa comer."
F[u"op_cofre"] = u"Tem cofrinho."
F[u"op_solta"] = u"A receita fica solta."
F[u"op_tem"] = u"Guardada no cofrinho."
F[u"op_nao"] = u"Solta na célula."
F[u"op_sonomic"] = u"Só dá para ver no microscópio."
F[u"op_semmic"] = u"Dá para ver sem o microscópio."

# ---- enunciados
ENUN = {
    1: u"Circule, ou toque, só os seres vivos.",
    2: u"Nesta cena, toque em tudo que está vivo.",
    3: u"Puxe cada figura para a gaveta certa: seres vivos ou não vivos.",
    4: u"Agora são três gavetas. Olhe bem antes de puxar.",
    5: u"Toque nas fases na ordem, do começo ao fim.",
    6: u"Este ser é feito de uma célula só, ou de muitas?",
    7: u"Olhe no microscópio. Toque na lente para focar.",
    8: u"Ele fabrica o próprio alimento com o Sol, ou precisa comer?",
    9: u"Puxe cada um para a gaveta do seu alimento.",
    10: u"A receita dele fica guardada num cofrinho, ou fica solta?",
    11: u"Pinte cada reino na cor da legenda.",
    12: u"Olhe a figura. De qual reino ela é?",
    13: u"Olhe a figura. De qual reino ela é?",
    14: u"Ligue cada ser vivo ao reino dele.",
    15: u"Ligue cada ser vivo ao reino dele.",
    16: u"Marque as três características deste reino.",
    17: u"Marque as três características deste reino.",
    18: u"Leia a descrição e toque no reino que ela descreve.",
    19: u"Uma casinha do quadro está vazia. Qual é?",
    20: u"Puxe cada ser vivo para a gaveta do reino dele.",
    21: u"Um deles não é deste reino. Ache o intruso.",
    22: u"Preencha a frase. Toque na palavra que falta.",
    23: u"Agora escreva o nome do reino. Toque no quadro vazio.",
    24: u"Toque do menor para o maior.",
    25: u"Escolha um ser vivo para cada reino. A coroa fica no fim.",
}
for n in ENUN:
    F[u"p%denun" % n] = ENUN[n]

# ---- folha 1
F[u"certo1"] = u"Isso! Todos esses nascem, crescem e um dia morrem: estão vivos."
for w in set(sum([it[u"todos"] for it in IT[u"p1"]], [])):
    if VIDA[w] != u"vivo":
        F[u"dica1_" + w] = (u"%s não nasce nem cresce sozinho. Procure quem "
                            u"nasce, cresce e pode ter filhos." % cap(NOMEF[w]))

# ---- folha 2
F[u"certo2"] = u"Você achou todos! Olho de cientista."
for w in set(sum([it[u"todos"] for it in IT[u"p2"]], [])):
    if VIDA[w] == u"foi":
        F[u"dica2_" + w] = (u"%s já foi de um ser vivo, mas agora não nasce nem "
                            u"cresce mais. Procure quem ainda está vivo."
                            % cap(NOMEF[w]))
    elif VIDA[w] == u"nunca":
        F[u"dica2_" + w] = (u"%s nunca esteve vivo. Procure quem nasce, cresce e "
                            u"se alimenta." % cap(NOMEF[w]))

# ---- folhas 3, 4, 9 e 20 (as gavetas)
F[u"certo3"] = u"Gavetas certas! Ser vivo nasce, cresce, se alimenta e morre."
F[u"dica3"] = (u"Pergunte assim: isso nasce e cresce sozinho? Se nasce, é vivo. "
               u"Se alguém fabricou, não é.")
F[u"certo4"] = (u"Três gavetas certas! Tem coisa que está viva, tem coisa que já "
                u"foi viva e virou outra coisa, e tem coisa que nunca viveu.")
F[u"dica4"] = (u"Pense de onde veio: o lápis veio da madeira da árvore, então já "
               u"foi vivo. A pedra não veio de ser vivo nenhum.")
F[u"certo9"] = (u"Isso! Quem tem folha verde fabrica o alimento com o Sol. Quem "
                u"não tem precisa comer.")
F[u"dica9"] = (u"Olhe se ele tem folhas verdes. Folha verde é a fábrica de "
               u"alimento que usa a luz do Sol.")
F[u"certo20"] = u"Cinco gavetas, cinco reinos! Você classificou como um cientista."
F[u"dica20"] = (u"Faça as três perguntas: quantas células, de onde vem o alimento "
                u"e se a receita tem cofrinho.")

# ---- folha 5
FASE = {
    u"semente": u"semente", u"broto": u"broto", u"planta_com_flor": u"planta com flor",
    u"semente_nova": u"semente nova", u"ovo": u"ovo", u"girino": u"girino",
    u"girino_com_pernas": u"girino com pernas", u"sapo_adulto": u"sapo adulto",
    u"lagarta": u"lagarta", u"casulo": u"casulo", u"borboleta_adulta": u"borboleta adulta",
    u"filhote": u"filhote", u"passaro_adulto": u"pássaro adulto", u"ninho_novo": u"ninho novo",
    u"bebe": u"bebê", u"crianca": u"criança", u"adulto": u"adulto", u"idoso": u"idoso",
    u"cachorro_jovem": u"cachorro jovem", u"cachorro_adulto": u"cachorro adulto",
    u"cachorro_velho": u"cachorro velho", u"pe_de_milho": u"pé de milho",
    u"espiga_com_sementes": u"espiga com sementes", u"larva": u"larva", u"pupa": u"pupa",
    u"formiga_adulta": u"formiga adulta",
}
for f in FASE:
    F[u"fase_" + f] = cap(FASE[f]) + u"."
for c in CICLOS:
    F[u"certo5_" + c[0]] = (u"Na ordem certa! O ciclo de vida %s é assim: %s. "
                            u"Nascer, crescer e um dia morrer é o que todo ser "
                            u"vivo faz." % (c[1], u", ".join(FASE[x] for x in c[2])))
F[u"dica5"] = u"Comece pelo começo de tudo: o menorzinho, aquele que ainda vai crescer."

# ---- folha 6
for k in ORDEM:
    R = REINOS[k]
    if R[u"cel"] == u"uma":
        F[u"certo6_" + k] = (u"Certo! Os seres do reino das %s são feitos de uma "
                             u"célula só. Um ser vivo inteiro numa célula."
                             % DIZR[k])
        F[u"dica6_" + k] = (u"Este é tão pequeno que só se vê no microscópio. "
                            u"Quem é assim costuma ter uma célula só.")
    else:
        F[u"certo6_" + k] = (u"Certo! Os seres do reino das %s são feitos de "
                             u"muitas células, milhões delas juntas."
                             % DIZR[k])
        F[u"dica6_" + k] = (u"Este a gente vê sem microscópio nenhum. Quem é "
                            u"grande assim é feito de muitas células.")

# ---- folha 7
F[u"focando"] = u"Ainda está embaçado. Toque de novo para focar melhor."
F[u"dica7_nao"] = (u"Pense no tamanho: se você nunca viu um desses andando por "
                   u"aí, é porque ele é pequeno demais para o olho.")
F[u"dica7_sim"] = (u"Este você já viu de verdade, sem aparelho nenhum. Então dá "
                   u"para ver sem o microscópio.")
for it in IT[u"p7"]:
    k = it[u"r"]
    F[u"foco_" + k] = (u"Focou! Apareceu %s." % NOMEF[REINOS[k][u"fig"]])
    if it[u"certo"] == u"nao":
        F[u"certo7_" + k] = (u"Isso! Os seres do reino das %s são microscópicos: "
                             u"eles existem, mas o olho sozinho não alcança. "
                             u"Foi por isso que o microscópio foi inventado."
                             % DIZR[k])
    else:
        F[u"certo7_" + k] = (u"Isso! Os seres do reino das %s a gente vê sem "
                             u"aparelho nenhum. Nem todo ser vivo é "
                             u"microscópico." % DIZR[k])

# ---- folha 8
F[u"dica8_fabrica"] = (u"Procure a cor verde: é nela que a luz do Sol vira "
                       u"alimento dentro da folha.")
F[u"dica8_come"] = (u"Ele não tem folha verde, então não consegue fabricar "
                    u"alimento. Quem não fabrica precisa comer.")
for it in IT[u"p8"]:
    w, k = it[u"w"], it[u"r"]
    if REINOS[k][u"com"] == u"fabrica":
        F[u"certo8_" + w] = (u"Certo! %s fabrica o próprio alimento usando a luz "
                             u"do Sol. Quem faz isso é chamado de produtor."
                             % cap(NOMEF[w]))
    else:
        F[u"certo8_" + w] = (u"Certo! %s não fabrica alimento: precisa comer "
                             u"outros seres vivos." % cap(NOMEF[w]))

# ---- folha 10
F[u"dica10_tem"] = (u"Quase todo ser vivo guarda a receita num cofrinho dentro "
                    u"da célula. Só um reino não guarda.")
F[u"dica10_nao"] = (u"Este é o menor de todos e o mais simples de todos: nem "
                    u"cofrinho ele tem.")
for k in ORDEM:
    if REINOS[k][u"cof"] == u"tem":
        F[u"certo10_" + k] = (u"Isso! A célula dos seres do reino das %s guarda "
                              u"a receita num cofrinho. Gente grande chama esse "
                              u"cofrinho de núcleo." % DIZR[k])
    else:
        F[u"certo10_" + k] = (u"Isso! A célula das bactérias não tem cofrinho: a "
                              u"receita fica solta lá dentro. É o único reino "
                              u"assim, e é por isso que ele fica separado dos "
                              u"outros quatro.")

# ---- folha 11
for it in IT[u"p11"]:
    k = it[u"r"]
    F[u"certo11_" + k] = (u"Pintado! O reino das %s ficou com a cor da legenda."
                          % DIZR[k])
CORNOME = [u"verde", u"vermelha", u"azul", u"amarela", u"rosa"]
for i, c in enumerate(CORNOME):
    F[u"dica11_%d" % i] = (u"A legenda pede a canetinha %s. Escolha ela no "
                           u"estojo antes de pintar." % c)

# ---- folhas 12 e 13
for pote in (u"p12", u"p13"):
    for it in IT[pote]:
        w, k = it[u"w"], it[u"r"]
        F[u"certo12_" + w] = (u"Certo! %s é do reino das %s."
                              % (cap(NOMEF[w]), DIZR[k]))
for k in ORDEM:
    F[u"dica12_" + k] = (u"Faça as três perguntas: quantas células, de onde vem "
                         u"o alimento e se a receita tem cofrinho. Este aqui "
                         u"tem %s, %s o alimento e %s cofrinho."
                         % (u"uma célula só" if REINOS[k][u"cel"] == u"uma" else u"muitas células",
                            u"fabrica" if REINOS[k][u"com"] == u"fabrica" else u"precisa comer",
                            u"tem" if REINOS[k][u"cof"] == u"tem" else u"não tem"))

# ---- folhas 14 e 15
for pote in (u"p14", u"p15"):
    for it in IT[pote]:
        for par in it[u"g"]:
            F[u"certo14_" + par[0]] = (u"Ligado! %s mora no reino das %s."
                                       % (cap(NOMEF[par[0]]), DIZR[par[1]]))
for k in ORDEM:
    F[u"dica14_" + k] = (u"Este é o reino das %s: %s."
                         % (DIZR[k], REINOS[k][u"quem"]))

# ---- folhas 16 e 17 (a coroa)
for k in ORDEM:
    R = REINOS[k]
    F[u"certocoroa_" + k] = (
        u"Ponta da coroa pronta! O reino das %s: %s, %s o alimento e %s."
        % (DIZR[k],
           u"uma célula só" if R[u"cel"] == u"uma" else u"muitas células",
           u"fabrica" if R[u"com"] == u"fabrica" else u"precisa comer",
           u"a receita fica no cofrinho" if R[u"cof"] == u"tem" else u"a receita fica solta"))
    F[u"dicacoroa_cel_" + k] = (
        u"Pense no tamanho: %s"
        % (u"este é tão pequeno que só se vê no microscópio."
           if R[u"cel"] == u"uma" else u"este a gente vê sem aparelho nenhum."))
    F[u"dicacoroa_com_" + k] = (
        u"Pense na cor verde: %s"
        % (u"este tem verde, então fabrica alimento com o Sol."
           if R[u"com"] == u"fabrica" else u"este não tem verde, então precisa comer."))
    F[u"dicacoroa_cof_" + k] = (
        u"Pense no cofrinho: %s"
        % (u"só as bactérias ficam sem ele."
           if R[u"cof"] == u"tem" else u"este é o único reino sem cofrinho."))

# ---- folha 18
for k in ORDEM:
    F[u"descr_" + k] = DESCR[k]
    F[u"certo18_" + k] = (u"Isso mesmo! Essa descrição é a do reino das %s."
                          % DIZR[k])
    F[u"dica18_" + k] = (u"Volte na primeira frase da descrição: ela diz quantas "
                         u"células o ser tem. Depois veja o alimento.")

# ---- folha 19 (o quadro)
DIZC = {u"cel": {u"uma": u"uma célula só", u"muitas": u"muitas células"},
        u"com": {u"fabrica": u"fabrica com o Sol", u"come": u"precisa comer"},
        u"cof": {u"tem": u"a receita no cofrinho", u"nao": u"a receita solta"}}
ROTC = {u"cel": u"as células", u"com": u"o alimento", u"cof": u"a receita"}
for it in IT[u"p19"]:
    k, c = it[u"r"], it[u"falta"]
    F[u"certoquadro_%s_%s" % (k, c)] = (
        u"Quadro completo! No reino das %s, %s: %s."
        % (DIZR[k], ROTC[c], DIZC[c][REINOS[k][c]]))
    F[u"dicaquadro_%s_%s" % (c, k)] = (
        u"Olhe as duas casinhas que já estão preenchidas: elas contam quem é "
        u"este reino. Agora pense %s dele." % ROTC[c])

# ---- folha 21 (o intruso)
for it in IT[u"p21"]:
    w = it[u"intruso"]
    F[u"certo21_" + w] = (u"Achou o intruso! %s é do reino das %s, e os outros "
                          u"são do reino das %s."
                          % (cap(NOMEF[w]), DIZR[DEQUEM[w]], DIZR[it[u"r"]]))
for k in (u"animais", u"plantas"):
    F[u"dica21_" + k] = (u"Olhe um por um e pergunte: este fabrica o alimento "
                         u"com o Sol ou precisa comer? O intruso responde "
                         u"diferente dos outros.")

# ---- folha 22
for p in TRIO:
    F[u"pal_" + p] = cap(p) + u"."
for it in IT[u"p22"]:
    F[u"frase_" + it[u"k"]] = it[u"txt"].replace(u"___", u"que palavra?")
    F[u"certo22_" + it[u"k"]] = {
        u"produtores": u"Isso! Quem fabrica o próprio alimento com a luz do Sol "
                       u"é produtor. Toda a comida do mundo começa neles.",
        u"consumidores": u"Isso! Quem precisa comer outro ser vivo é consumidor.",
        u"decompositores": u"Isso! Os fungos e as bactérias são os "
                           u"decompositores: eles desmancham os restos e "
                           u"devolvem tudo para a terra, para as plantas usarem "
                           u"de novo. Sem eles o mundo ficaria entulhado.",
    }[it[u"certo"]]
    F[u"dica22_" + it[u"k"]] = (u"Pergunte: ele fabrica o alimento, ele come "
                                u"outro ser vivo, ou ele desmancha o que já "
                                u"morreu?")

# ---- folha 23
for k in ORDEM:
    F[u"pista_" + k] = cap(PISTA[k]) + u"."
    F[u"certo23_" + k] = (u"Você escreveu certo: %s! É o reino de %s."
                          % (REINOS[k][u"dia"].capitalize(), REINOS[k][u"quem"]))
    F[u"dica23_" + k] = (u"Olhe a figura e escute de novo: é o reino das %s."
                         % DIZR[k])

# ---- folha 24
F[u"certo24"] = (u"Do menor ao maior, na ordem certa! Tem ser vivo que não cabe "
                 u"no olho e ser vivo que não cabe na sala.")
F[u"dica24"] = (u"Comece pelo que só se vê no microscópio. Depois vá subindo "
                u"de tamanho.")

# ---- folha 25
for k in ORDEM:
    F[u"certo25_" + k] = (u"A ponta do reino das %s está na sua coroa!" % DIZR[k])


# ============================================================
#  GRAVAR
# ============================================================
def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    t = F[k]
    if not t:
        continue
    c = chave(t)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": t, u"voz": VOZ})

io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")

html = io.open(CAM, encoding=u"utf-8").read()
blocoI = (u"/*ITENS-INI*/\nvar ITENS = "
          + json.dumps(IT, ensure_ascii=False, indent=1, sort_keys=True)
          + u";\n/* o nome de gente de cada figura (o PNG chama-se `urso_pelucia`;"
            u" a criança ouve \"o urso de pelúcia\") */\nvar FIGNOME = "
          + json.dumps(NOMEF, ensure_ascii=False, indent=1, sort_keys=True)
          + u";\n/*ITENS-FIM*/")
blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*ITENS-INI\*/.*?/\*ITENS-FIM\*/", lambda m: blocoI, html, flags=re.S)
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, novo, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/",
              lambda m: u"/*SILMAP-INI*/var SILMAP = {};/*SILMAP-FIM*/", novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

itens = sum(len(v) for v in IT.values())
print(u"ITENS: %d item(ns) em %d potes; FALAS: %d chaves; falas.json: %d fala(s)"
      % (itens, len(IT), len(F), len(falas)))
