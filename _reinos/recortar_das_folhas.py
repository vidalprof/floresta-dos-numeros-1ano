# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DE DENTRO DAS FOLHAS DE PROFESSOR — cinco reinos

 ⭐ ORDEM DO MARCOS (14/set/2026): *"Aproveite as imagens e preste atenção no
    que as atividades pedem para criar as interatividades"*. E, antes dela, a
    pergunta que deu origem ao portão 1i5: *"por que você não cumpre o que
    combinamos?"* — porque a regra da origem da figura estava em prosa e não
    em medida. Agora está nas duas.

 A REGRA: a figura vem da MESMA folha de onde veio o gesto. Gesto e desenho
 nascem juntos, e a criança reconhece na tela a atividade que a professora dá
 no papel.

 ⚠️ A CAIXA É GENEROSA DE PROPÓSITO, e quem aperta é o PIXEL: depois do corte
    o `aperta()` anda de fora para dentro até achar tinta. Caixa apertada no
    olho corta a asa da borboleta; caixa larga o `aperta` resolve sozinho.

 ⚠️ TRÊS LIMPEZAS QUE ESTA COLHEITA EXIGE:
    1. **o quadradinho de marcar** — na d26 cada figura vem com um [ ] ao lado,
       e ele entrava junto. A caixa para antes dele.
    2. **a linha tracejada de recortar** — na d20 e na d22 cada figura está
       dentro de um retângulo pontilhado. O `tira_moldura` come a beirada até
       passar da linha.
    3. **o fundo branco** — vira transparente por vizinhança (a água entra pela
       BORDA), nunca por semelhança: o branco de DENTRO da figura (a barriga do
       cachorro, o miolo do cogumelo) a água não alcança.

 Uso: python3 _reinos/recortar_das_folhas.py [--contato]
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_reinos")
SAIDA = os.path.join(AQUI, u"img")
PREFIXO = u"rn_"
LIM = 238          # acima disto conta como "papel branco"

# ============================================================
#  AS CAIXAS, folha por folha. Cada uma em FRAÇÃO da imagem
#  (x0, y0, x1, y1) — assim o corte não depende do tamanho do arquivo.
# ============================================================

# --- d26: "CLASSIFIQUE EM SERES VIVOS E NÃO VIVOS" — 20 figuras coloridas numa
#     grade de 4 colunas x 5 linhas, cada uma com um quadradinho de marcar à
#     direita (que a caixa NÃO pega: ela para em 0.72 da largura da célula).
# ⚠️ O GELO SAIU DA LISTA, e por medida: o desenho dele na folha e branco
#    com um fio azul claro, e some em qualquer recorte (a ilha de tinta nem
#    chega a existir). Ficava um PNG vazio na pasta. Quatro figuras da linha
#    1, nao cinco — e a folha d26 passa a dar 19, nao 20.
D26 = [u"terra", u"vento", u"sapo",
       u"arvore", u"pedras", u"sol", u"rosa",
       u"agua", u"passarinho", u"carro", u"borboleta",
       u"areia", u"formiga", u"casa", u"tijolos",
       u"menino", u"fogo", u"cavalo", u"nuvem"]

# --- d20: "Recorte as figuras e cole na coluna de seres vivos e não vivos"
#     8 ícones de traço, grade 4 x 2, dentro de moldura tracejada.
D20 = [u"borboleta2", u"celular", u"sol2", u"arvore2",
       u"urso_pelucia", u"cachorro", u"elefante", u"lapis"]

# --- d22: "Recorte e cole separando: SERES VIVOS / SERES NÃO VIVOS"
#     12 figuras de traço, grade 3 x 4.
D22 = [u"pedras2", u"arvore3", u"milho",
       u"borboleta3", u"cupcake", u"sapo2",
       u"lanche", u"tubarao", u"urso_pelucia2",
       u"tomateiro", u"bebe", u"bola"]

# --- d07: a COROA — uma figura por reino, traço limpo, na faixa das colunas.
D07 = [u"reino_monera", u"reino_plantae", u"reino_protista",
       u"reino_fungi", u"reino_animal"]

# ⚠️ A FAIXA ONDE MORAM AS FIGURAS (y0,y1,x0,x1 em fração da folha) e em quantas
#    LINHAS elas estão. Só isto é declarado à mão — e é grosso de propósito: a
#    faixa só precisa excluir o cabeçalho e o rodapé, porque quem acha a caixa
#    de cada figura é a tinta dela. Errar a faixa em 2% não muda nada; errar a
#    grade antiga em 2% cortava a asa da borboleta.
CAIXAS_POR_FOLHA = [
    # cod, nomes, faixa(y0,y1,x0,x1), linhas, colorida, moldura impressa
    (u"d26", D26, (0.36, 0.96, 0.00, 0.98), 5, True,  False),
    (u"d20", D20, (0.66, 0.95, 0.04, 0.97), 2, False, True),
    (u"d22", D22, (0.24, 0.94, 0.07, 0.92), 4, False, True),
    # ⚠️ a faixa da d07 foi MEDIDA, nao estimada: as cinco figuras ficam entre
    #    y 0,640 e 0,720; os rotulos ("REINO ANIMAL") entre 0,603 e 0,636 e o
    #    "CARACTERISTICAS:" logo abaixo. Faixa larga trazia os dois junto.
    (u"d07", D07, (0.638, 0.725, 0.10, 0.90), 1, False, False),
]

# ============================================================
#  ⭐⭐ A CAIXA NÃO SE CHUTA: ELA SE MEDE PELA PRÓPRIA TINTA (14/set/2026)
#
#  ⚠️ O QUE DEU ERRADO ANTES, e o Marcos viu na tela: *"tem resto de outras
#     imagens nas imagens, e imagens que faltam partes"*. A primeira versão
#     dividia a folha numa GRADE REGULAR de frações que eu media no olho. Grade
#     chutada erra dos dois jeitos ao mesmo tempo — larga demais traz um pedaço
#     do vizinho (o bebê com um traço solto ao lado, a casa com um risco
#     embaixo), apertada demais come a figura (a bola sem a borda, o elefante
#     sem a traseira, o cupcake sem a forminha).
#
#  A MEDIDA CERTA: cada figura é uma ILHA DE TINTA. Borra-se um pouco a folha
#  (dilatação) para colar os pedaços da MESMA figura — o olho do bicho, os raios
#  do sol —, rotulam-se as ilhas, e o recorte é o retângulo da ilha. Ninguém
#  chuta nada: a figura define a própria caixa.
#
#  ⚠️ E O QUADRADINHO DE MARCAR DA d26 SAI SOZINHO, sem heurística: a folha é
#     COLORIDA e o quadradinho é PRETO. Separar por SATURAÇÃO tira o quadradinho
#     e deixa a figura — e o `tira_solto_direita`, que era um remendo, deixa de
#     ser preciso.
#
#  ⚠️⚠️ A TRAVA QUE IMPEDE O ERRO BOBO DE VOLTAR: se o número de ilhas achadas
#     não bater com o número de nomes declarados, o script **PARA** e diz o que
#     achou. Antes ele casava na ordem e seguia — e casar errado é pior que não
#     recortar, porque sai figura com o nome de outra e ninguém vê.
# ============================================================

def apaga_quadradinhos(im):
    u"""Apaga da FOLHA INTEIRA os quadradinhos de marcar, antes de achar as ilhas.

    ⚠️ ESTE E O CONSERTO DE RAIZ do defeito que o Marcos viu: *"tem resto de
       outras imagens nas imagens"*. Na d26 cada figura tem, a sua direita, um
       quadradinho preto para a crianca marcar. Em tres figuras o desenho
       ENCOSTA nele (medido: o rabo do PASSARINHO e o colchete sao UM UNICO
       componente, 4.972 px, nenhum vao entre os dois), entao nem "peca solta",
       nem "vao", nem "depois da ultima coluna com cor" o alcancam: o colchete
       fica DENTRO da faixa de colunas do rabo.

    ⚠️ POR QUE NA FOLHA E NAO NO RECORTE: dentro do recorte o quadradinho e um
       borrao colado na figura e nao ha como distingui-lo sem chutar. Na folha
       ele e outra coisa: um dos VINTE quadrados iguais de uma grade 4x5, todos
       com a mesma medida. Isso nao se adivinha, se mede — e e o que esta aqui.

    A MEDIDA (feita na d26, 768x1024): componente escuro e SEM COR, quase
    quadrado (razao 0,85-1,20), OCO (tinta / area da caixa entre 0,25 e 0,50 —
    e um fio de contorno, nao um bloco). Deu 19 dos 20: o 20o (o da TERRA)
    aparecia grudado no monte de terra, num componente de 172x49. Os 19 acham
    4 colunas e 5 linhas; a vigesima casa sai do CRUZAMENTO delas — interpolada
    da medida dos outros dezenove, nao de palpite.

    Apaga so o pixel SEM COR de dentro de cada casa: assim o fio preto do
    quadradinho some e a ponta colorida do rabo que entra ali fica.
    """
    a = np.asarray(im).astype(np.int16)
    mx, mn = a[..., :3].max(axis=2), a[..., :3].min(axis=2)
    sem_cor = (mx < LIM) & ((mx - mn) <= 60)
    rot, n = nd.label(sem_cor, np.ones((3, 3), bool))
    achados = []
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        if sl is None:
            continue
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        if w < 20 or h < 20:
            continue
        cheio = int((rot[sl] == i).sum()) / float(w * h)
        if 0.85 <= w / float(h) <= 1.20 and 0.25 <= cheio <= 0.50:
            achados.append((xs.start, ys.start, w, h))
    if len(achados) < 4:
        return im, 0, 0
    lw = sorted(c[2] for c in achados)
    lh = sorted(c[3] for c in achados)
    mw, mh = lw[len(lw) // 2], lh[len(lh) // 2]
    achados = [c for c in achados
               if abs(c[2] - mw) <= mw * 0.25 and abs(c[3] - mh) <= mh * 0.25]
    if len(achados) < 4:
        return im, 0, 0

    def trilhos(valores, tol):
        u"""agrupa coordenadas parecidas e devolve a mediana de cada grupo"""
        saida, grupo = [], []
        for v in sorted(valores):
            if grupo and v - grupo[0] > tol:
                saida.append(sorted(grupo)[len(grupo) // 2])
                grupo = []
            grupo.append(v)
        if grupo:
            saida.append(sorted(grupo)[len(grupo) // 2])
        return saida

    colunas = trilhos([c[0] for c in achados], mw * 0.6)
    linhas = trilhos([c[1] for c in achados], mh * 0.6)
    px = im.load()
    W, H = im.size
    casas = 0
    for cy in linhas:
        for cx in colunas:
            casas += 1
            for x in range(max(0, cx - 3), min(W, cx + mw + 3)):
                for y in range(max(0, cy - 3), min(H, cy + mh + 3)):
                    r, g, b = px[x, y]
                    if max(r, g, b) < LIM and (max(r, g, b) - min(r, g, b)) <= 60:
                        px[x, y] = (255, 255, 255)
    return im, len(achados), casas


def tira_linha_impressa(c):
    u"""Apaga o que sobrou da PAUTA da folha na beirada do recorte: o tracejado da
    moldura e a linha da coluna. Nunca o desenho.

    ⚠️ O `tira_moldura_do_recorte` nao alcanca estes, e a razao e de desenho: ele
       procura o componente que ENVOLVE o desenho, e uma moldura TRACEJADA nao
       envolve nada — ela e quarenta e quatro risquinhos soltos. Era o que ainda
       cercava a ARVORE2 (d20) depois de tudo.

    A MEDIDA que separa risco de desenho, feita nas 20 figuras das folhas com
    moldura (d20 e d22), sem chute e sem fio de navalha:
      · os riscos da moldura      -> ate 0,19% da tinta do corpo, encostados na
                                     beirada (arvore2, milho, bola)
      · a menor parte LEGITIMA solta que TAMBEM encosta na beirada
                                  -> raio do SOL2, 1,83% do corpo
    Corto com 0,50% e beirada de 3 px: 2,6x acima do maior risco e 3,7x abaixo
    do menor pedaco de desenho. Nenhuma parte de desenho e apagada — nem as
    pedrinhas soltas do monte de PEDRAS2, nem os galhos da ARVORE3, nem os raios
    do SOL2, que sao os que chegam mais perto do corte.

    ⚠️ TINHA UMA TERCEIRA CONDICAO AQUI — "espessura ate 4 px" — e ela REPROVAVA
       um risco de verdade: o CANTO da moldura, onde dois tracos se encontram,
       mede 5x5 e sobrava na arvore2 como um pontinho no canto da figura. Tirei,
       e conferi nas 20 que sem ela nada de desenho cai: continua caindo so o
       canto e um pixel solto, ambos da arvore2.

    ⚠️ A SEGUNDA REGRA, A REGUA, e da d07: a coroa dos cinco reinos e uma TABELA,
       e no REINO ANIMAL (a ultima coluna) sobrava a linha divisoria — 2 px de
       largura por 110 px de altura, que e a altura INTEIRA do recorte. Ela e
       grande demais para a regra do tamanho (6,6% do corpo), mas e obvia por
       outro lado: nenhum desenho tem um traco de 2 px atravessando a figura de
       ponta a ponta. Medido nas 44 figuras: nenhuma parte de desenho e
       `min(largura,altura) <= 4` E ao mesmo tempo ocupa 90% de um dos lados.

    ⚠️ E POR QUE RODA EM TODAS, e nao so nas de moldura: quando so rodava nas
       duas folhas de moldura, o reino_animal ficava sujo e eu "consertava" com
       uma excecao pelo nome dele numa lista. Excecao pelo nome nao e conserto,
       e uma nota para nao esquecer — e a nota estava la, da rodada anterior, e
       eu quase a repeti de olhos fechados."""
    a = np.asarray(c).astype(np.int16)
    alfa = a[..., 3] > 24
    if not alfa.any():
        return c
    H, W = alfa.shape
    rot, n = nd.label(alfa, np.ones((3, 3), bool))
    if n < 2:
        return c
    pedacos = []
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        if sl is None:
            continue
        ys, xs = sl
        pedacos.append((int((rot[sl] == i).sum()), i, xs.stop - xs.start,
                        ys.stop - ys.start,
                        min(xs.start, ys.start, W - xs.stop, H - ys.stop)))
    corpo = max(p[0] for p in pedacos)
    px = c.load()
    for tam, i, w, h, borda in pedacos:
        if tam == corpo:
            continue
        pequeno = tam <= corpo * 0.005 and borda <= 3
        regua = min(w, h) <= 4 and (w >= W * 0.90 or h >= H * 0.90)
        if not (pequeno or regua):
            continue
        for y, x in zip(*np.where(rot == i)):
            r, g, b, al = px[int(x), int(y)]
            px[int(x), int(y)] = (r, g, b, 0)
    return c


def _tinta_da_folha(cam, colorida):
    u"""Devolve (matriz de tinta, imagem RGB). `colorida` separa por saturação."""
    im = Image.open(cam).convert(u"RGB")
    if colorida:
        im, achados, casas = apaga_quadradinhos(im)
        if casas:
            print(u"   %s: apaguei %d quadradinho(s) de marcar "
                  u"(%d medidos na folha, %d na grade que eles formam)"
                  % (os.path.basename(cam), casas, achados, casas))
    a = np.asarray(im).astype(np.int16)
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = mx - mn
    escuro = mx < 205
    if colorida:
        # a figura tem cor; o quadradinho de marcar é preto puro (saturação ~0)
        return (sat > 45) | (escuro & (sat > 25)), im
    return escuro, im


def ilhas(cam, faixa, colorida=False, cola=5, piso=0.0004, teto=0.25):
    u"""As ilhas de tinta dentro de `faixa` (y0,y1,x0,x1 em fração da folha).

    `piso`/`teto` são frações da área da folha: abaixo do piso é sujeira de
    escaneamento, acima do teto é a MOLDURA que envolve tudo (a d22 tem uma).
    ⚠️ Os dois são PALPITE DECLARADO, e foram conferidos olhando as 45 figuras
       grandes numa folha de contato — não saíram de cabeça."""
    tinta, im = _tinta_da_folha(cam, colorida)
    H, W = tinta.shape
    y0, y1, x0, x1 = (int(faixa[0]*H), int(faixa[1]*H), int(faixa[2]*W), int(faixa[3]*W))
    fora_da_faixa = np.ones_like(tinta)
    fora_da_faixa[y0:y1, x0:x1] = False
    tinta = tinta & ~fora_da_faixa
    grosso = nd.binary_dilation(tinta, np.ones((cola, cola), bool))
    rot, _ = nd.label(grosso)
    cx = []
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        m = (rot[sl] == i) & tinta[sl]
        n = int(m.sum())
        if n < piso * H * W or n > teto * H * W:
            continue
        yy, xx = np.where(m)
        cx.append((sl[0].start + yy.min(), sl[0].start + yy.max(),
                   sl[1].start + xx.min(), sl[1].start + xx.max()))
    return cx, im, (H, W)


def molduras(cam, faixa, quantas, cola=9, teto=0.10):
    u"""As MOLDURAS impressas da folha — e é delas que sai a caixa de cada figura.

    ⚠️ POR QUE NÃO BASTA A ILHA DA FIGURA (medido em 14/set/2026): numa figura
       de traço com partes SOLTAS — o monte de pedras da d22, cujas pedrinhas de
       cima não encostam nas de baixo — a ilha pega só um pedaço, e a figura sai
       cortada. Foi um dos defeitos que o Marcos viu.

    ⚠️ E A FOLHA JÁ RESOLVE ISSO SOZINHA: na d20 e na d22 cada figura mora dentro
       de um retângulo impresso (cheio numa, tracejado na outra), porque a folha
       é de RECORTAR. Com uma dilatação maior o tracejado fecha e a moldura vira
       uma ilha. A caixa da figura é o INTERIOR dessa moldura — assim entra tudo
       o que é da figura e nada do vizinho, que está na moldura ao lado.

    ⚠️ A ESCOLHA NAO E POR LIMIAR DE AREA, e isso importa: medindo a d20, as
       oito molduras dao 2,20% a 2,22% da folha e o QR CODE do rodape da 1,68%
       — um limiar entre os dois seria fio de navalha, e fio de navalha quebra
       na proxima folha. Como a lista de nomes ja diz QUANTAS figuras a folha
       tem, ficam as `quantas` MAIORES: na d20 as oito molduras (o QR fica de
       fora), na d22 as doze (1,69% a 2,60%, e o resto nao passa de 1,47%).
       Se nao houver `quantas`, o chamador PARA — nunca casa no escuro."""
    tinta, im = _tinta_da_folha(cam, False)
    H, W = tinta.shape
    y0, y1, x0, x1 = (int(faixa[0]*H), int(faixa[1]*H), int(faixa[2]*W), int(faixa[3]*W))
    m = np.zeros_like(tinta)
    m[y0:y1, x0:x1] = tinta[y0:y1, x0:x1]
    cheio = nd.binary_closing(nd.binary_dilation(m, np.ones((cola, cola), bool)),
                              np.ones((cola, cola), bool))
    cheio = nd.binary_fill_holes(cheio)
    rot, _ = nd.label(cheio)
    cx = []
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        alt = sl[0].stop - sl[0].start
        lar = sl[1].stop - sl[1].start
        a = alt * lar
        if a > teto * H * W:
            continue
        # ⚠️ MOLDURA DE FIGURA E QUASE QUADRADA — a da d20 e da d22 fica entre
        #    1:1 e 1,4:1. A BARRA LATERAL da folha tambem passava no filtro de
        #    area e entrava como se fosse figura: ela virou a caixa 6, o
        #    tomateiro ficou sem caixa, e dali para a frente TODO nome deslizou
        #    um lugar (o urso virou "tomateiro", o tubarao virou "urso"). Uma
        #    tira de 1:40 nao e moldura de desenho.
        if max(alt, lar) > 3 * min(alt, lar):
            continue
        cx.append((a, sl[0].start, sl[0].stop, sl[1].start, sl[1].stop))
    cx.sort(reverse=True)
    return [c[1:] for c in cx[:quantas]], im, (H, W)


def em_ordem_de_leitura(cx, altura, linhas):
    u"""Ordena as caixas como a criança lê: linha por linha, esquerda→direita.

    ⚠️ NÃO SE DIVIDE A FOLHA EM FAIXAS IGUAIS, e foi assim que os nomes saíram
       TROCADOS na primeira tentativa (o passarinho virou "agua", a formiga
       virou "areia"). Duas razões: as figuras de uma mesma linha não têm a
       mesma altura — a rosa é alta e a água é uma tira baixa, e o topo delas
       fica a dezenas de pixels de distância —, e uma linha pode ter MENOS
       figuras que as outras (na d26 o gelo não existe como tinta), o que
       desloca tudo o que vem depois.

    O corte de linha sai da PRÓPRIA folha: ordeno pelo CENTRO vertical e abro
    linha nova quando o centro do próximo está mais de 60% de uma altura típica
    (a mediana das caixas) abaixo do primeiro da linha corrente. Assim a linha
    acompanha o tamanho real das figuras, e linha curta não empurra ninguém."""
    if not cx:
        return cx
    alt = sorted(c[1] - c[0] for c in cx)
    tipica = alt[len(alt) // 2]
    porcentro = sorted(cx, key=lambda c: (c[0] + c[1]) / 2.0)
    fora, linha, base = [], [], None
    for c in porcentro:
        meio = (c[0] + c[1]) / 2.0
        if base is None or meio - base <= tipica * 0.6:
            if base is None:
                base = meio
            linha.append(c)
        else:
            fora.extend(sorted(linha, key=lambda z: z[2]))
            linha, base = [c], meio
    fora.extend(sorted(linha, key=lambda z: z[2]))
    return fora


# ============================================================
#  AS FERRAMENTAS
# ============================================================

def acha(cod):
    achou = sorted(glob.glob(os.path.join(FOLHAS, cod + u"_*")))
    return achou[0] if achou else None


def tira_moldura(im, escuro=120, faixa=0.22):
    u"""Come a beirada até PASSAR da linha escura da moldura (tracejada ou não).

    ⚠️ A primeira versão parava de cara, porque entre a beirada da caixa e a
       moldura há papel BRANCO. Esta PROCURA a linha escura dentro da faixa
       externa e corta logo depois dela."""
    px = im.convert(u"L").load()
    W, H = im.size
    fw, fh = max(1, int(W * faixa)), max(1, int(H * faixa))

    def linha_escura_h(y):
        n = sum(1 for x in range(W) if px[x, y] < escuro)
        return n > W * 0.55

    def linha_escura_v(x):
        n = sum(1 for y in range(H) if px[x, y] < escuro)
        return n > H * 0.55

    top, bot, esq, dir_ = 0, H, 0, W
    for y in range(fh):
        if linha_escura_h(y):
            top = y + 1
    for y in range(H - 1, H - fh - 1, -1):
        if linha_escura_h(y):
            bot = y
            break
    for x in range(fw):
        if linha_escura_v(x):
            esq = x + 1
    for x in range(W - 1, W - fw - 1, -1):
        if linha_escura_v(x):
            dir_ = x
            break
    if dir_ - esq < W * 0.4 or bot - top < H * 0.4:
        return im
    return im.crop((esq, top, dir_, bot))


def tira_solto_direita(c, fatia=0.34, teto=0.38):
    u"""Apaga a PEÇA SOLTA da beirada direita — o quadradinho de marcar.

    ⚠️ POR QUE NÃO BASTA APERTAR A CAIXA: o quadradinho da d26 fica sempre no
       mesmo lugar da célula, mas a figura não — a árvore é larga e o sol é
       estreito. Caixa apertada o bastante para livrar o sol cortava a árvore.
       Então a caixa vai larga e o quadradinho sai por MEDIDA: procura-se uma
       coluna inteiramente vazia no terço direito e, se o que sobrar à direita
       dela tiver menos de um quinto da tinta, aquilo é o quadradinho."""
    W, H = c.size
    px = c.load()
    tinta = [sum(1 for y in range(H) if px[x, y][3] > 24) for x in range(W)]
    total = sum(tinta)
    if total == 0:
        return c
    ini = int(W * (1 - fatia))
    corte = None
    for x in range(W - 2, ini, -1):
        if tinta[x] == 0 and sum(tinta[x:]) > 0:
            if sum(tinta[x:]) <= total * teto:
                corte = x
            else:
                break
    if corte is None:
        return c
    for x in range(corte, W):
        for y in range(H):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 0)
    return c


def limpa_fundo(c, lim=LIM):
    u"""Branco do PAPEL vira transparente, por VIZINHANÇA (a água entra pela
    borda). O branco de dentro da figura a água nunca alcança."""
    c = c.convert(u"RGBA")
    W, H = c.size
    px = c.load()
    fila, visto = [], set()
    for x in range(W):
        fila.append((x, 0))
        fila.append((x, H - 1))
    for y in range(H):
        fila.append((0, y))
        fila.append((W - 1, y))
    while fila:
        x, y = fila.pop()
        if (x, y) in visto or not (0 <= x < W and 0 <= y < H):
            continue
        visto.add((x, y))
        r, g, b, a = px[x, y]
        if a == 0 or (r >= lim and g >= lim and b >= lim):
            px[x, y] = (r, g, b, 0)
            fila.append((x + 1, y)); fila.append((x - 1, y))
            fila.append((x, y + 1)); fila.append((x, y - 1))
    return c


def tira_halo(c, lim=228, voltas=2):
    u"""Come a FRANJA quase-branca que sobra grudada na silhueta.

    ⚠️ POR QUE O `limpa_fundo` SOZINHO NAO RESOLVE: ele so apaga o que passa de
       238 de claridade. Entre o papel (255) e o traco preto ha uma borda de
       antialiasing do escaneamento — pixels de 210 a 237 — que ficam, e na tela
       colorida do caderno viram um CONTORNO BRANCO em volta da figura. O portao
       0o6 (`_qa/halo.py`) mede isso e reprovou dez das 45 figuras.

    ⚠️ E POR QUE NAO UM SEGUNDO FLOOD-FILL, MAIS FROUXO: porque ha figuras cujo
       CORPO e quase branco — a nuvem, o gelo, o bebe de traco. Um flood a 212
       entraria pela beirada e comeria a nuvem inteira. Esta versao so morde o
       que ENCOSTA no transparente, e no maximo `voltas` pixels para dentro: a
       franja sai, o corpo fica."""
    W, H = c.size
    px = c.load()
    for _ in range(voltas):
        marcados = []
        for y in range(H):
            for x in range(W):
                r, g, b, a = px[x, y]
                if a < 24 or r < lim or g < lim or b < lim:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    vx, vy = x + dx, y + dy
                    if not (0 <= vx < W and 0 <= vy < H) or px[vx, vy][3] < 24:
                        marcados.append((x, y))
                        break
        if not marcados:
            break
        for x, y in marcados:
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 0)
    return c


def aperta(c):
    u"""anda de fora para dentro até achar tinta (usa o alfa já limpo)."""
    bb = c.getbbox()
    return c.crop(bb) if bb else c


def _risco_no_topo(c, densidade=0.30, grossura=4, vao=2):
    u"""Apaga a LINHA que sobrou colada na beirada DE CIMA — e só ela.

    ⚠️ LICAO PAGA (14/set/2026, contato-folha das 45 figuras): depois do
       `tira_moldura` e do `aperta`, doze figuras ainda saíram com um risco na
       beirada — a linha da célula da tabela (d20/d22, um traço cheio à direita)
       ou o tracejado de recortar (d26, pontinhos em cima/embaixo). No
       contato-folha eles aparecem como um risco solto ao lado do desenho, e é
       exatamente o tipo de sujeira que a criança vê e eu não vejo se olhar só a
       figura grande.

    ⚠️ E ELE NAO PODE COMER O DESENHO. Duas travas medidas, não chutadas:
       1. **GROSSURA**: risco de moldura tem 1 a 3 px; acima de `grossura` px
          a coisa é desenho e fica.
       2. **O VÃO**: entre o risco e a figura há papel BRANCO (já transparente).
          Sem pelo menos `vao` linhas vazias logo depois, não é risco solto — é
          o próprio desenho encostando na beirada, como a base do monte de terra
          (que é a linha mais larga da figura e seria comida sem esta trava)."""
    W, H = c.size
    px = c.load()

    def tinta(y):
        return sum(1 for x in range(W) if px[x, y][3] > 24)

    k = 0
    while k < grossura and k < H and tinta(k) >= W * densidade:
        k += 1
    if k == 0:
        return c
    # ⚠️ "vazio" com FOLGA, e não zero absoluto: medido em 14/set/2026, logo
    #    abaixo do traço da moldura sobram dois ou três pixelzinhos de tinta
    #    esfarelada do escaneamento (2% a 3% da largura). Exigir zero cravado
    #    fazia o portão desistir justamente nas três figuras mais sujas
    #    (elefante, lápis, urso) — o traço ficava e eu achava que a regra rodara.
    vazio = max(1, int(W * 0.03))
    g = 0
    while k + g < H and g < vao + 6 and tinta(k + g) <= vazio:
        g += 1
    if g < vao:
        return c
    for y in range(k + g):
        for x in range(W):
            r, gg, b, a = px[x, y]
            px[x, y] = (r, gg, b, 0)
    return c


def tira_risco(c):
    u"""o mesmo corte nas QUATRO beiradas — girando a figura quatro vezes."""
    for _ in range(4):
        c = _risco_no_topo(c)
        c = c.rotate(90, expand=True)
    return c


def salva(c, nome):
    if c.width > 420 or c.height > 420:
        c.thumbnail((420, 420), Image.LANCZOS)
    c.save(os.path.join(SAIDA, PREFIXO + nome + u".png"), optimize=True)


def tira_peca_solta_sem_cor(c, sat=60):
    u"""Apaga as PEÇAS SOLTAS sem cor de um recorte colorido — na d26, o
    quadradinho de marcar que encosta na figura e entra no retângulo.

    ⚠️ POR COMPONENTE, NUNCA POR PIXEL. A primeira versão apagava todo pixel
       preto-sem-cor e destruiu o desenho: sumiu a crina do cavalo, o cabelo do
       menino e o contorno da borboleta — que são pretos e são A FIGURA. O que
       distingue o quadradinho não é a cor dele: é ele ser uma peça SEPARADA,
       que não encosta no corpo colorido do desenho.

    Então: rotulam-se as peças; a que tem mais cor é a figura; some qualquer
    outra peça cuja tinta seja quase toda sem cor. O cabelo do menino sobrevive
    porque está grudado no menino — é a mesma peça."""
    a = np.asarray(c).astype(np.int16)
    alfa = a[..., 3] > 24
    if not alfa.any():
        return c
    mx = a[..., :3].max(axis=2)
    mn = a[..., :3].min(axis=2)
    cor = alfa & ((mx - mn) > sat)
    if cor.sum() < alfa.sum() * 0.15:
        return c                      # recorte sem cor: nao e o caso da d26
    rot, n = nd.label(alfa, np.ones((3, 3), bool))
    if n < 2:
        return c
    principal = np.argmax([cor[rot == i].sum() for i in range(1, n + 1)]) + 1
    px = c.load()
    W, H = c.size
    for i in range(1, n + 1):
        if i == principal:
            continue
        m = rot == i
        yy, xx = np.where(m)
        fina = (xx.max() - xx.min()) < c.size[0] * 0.15
        na_direita = xx.min() > c.size[0] * 0.70
        if fina and na_direita:
            pass                      # risco do quadradinho de marcar: sai
        elif cor[m].sum() > m.sum() * 0.25:
            continue                  # peca mesmo colorida: e da figura, fica
        # ⚠️ 25% e nao 10%, e a razao e o formato: a d26 e JPG, e a compressao
        #    poe uma franja COLORIDA em volta de todo traco preto. Com 10% o
        #    quadradinho de marcar passava por "colorido" e continuava na tela
        #    (o colchete ao lado do passarinho e da formiga).
        for y, x in zip(*np.where(m)):
            r, g, b, al = px[int(x), int(y)]
            px[int(x), int(y)] = (r, g, b, 0)
    return c


def tira_moldura_do_recorte(c):
    u"""Apaga a MOLDURA impressa que veio junto no recorte, sem tocar no desenho.

    ⚠️ COMO SE DISTINGUE UMA DA OUTRA, medindo e não chutando: a moldura é o
       componente que ENVOLVE o desenho — o retângulo dela CONTÉM o retângulo
       dele. Tentei antes "o componente que toca 3 bordas" e não funcionou: o
       `aperta` já tinha encostado tudo na beirada, e a moldura do cachorro
       aparecia tocando UMA borda só. Conter é uma relação, não uma posição:
       não depende de onde o recorte foi feito.

    O desenho nunca envolve nada (é o miolo), então nenhuma figura é apagada
    por engano — nem as de partes soltas, como o monte de pedras."""
    a = np.asarray(c).astype(np.int16)
    alfa = a[..., 3] > 24
    if not alfa.any():
        return c
    rot, n = nd.label(nd.binary_dilation(alfa, np.ones((9, 9), bool)))
    if n < 2:
        return c
    cxs = []
    for i in range(1, n + 1):
        m = (rot == i) & alfa
        if not m.any():
            continue
        yy, xx = np.where(m)
        cxs.append((i, yy.min(), yy.max(), xx.min(), xx.max(), m))
    px = c.load()
    total = float(alfa.sum())
    for i, y0, y1, x0, x1, m in cxs:
        envolve = any(j != i and y0 < jy0 and y1 > jy1 and x0 < jx0 and x1 > jx1
                      for j, jy0, jy1, jx0, jx1, _ in cxs)
        # ⚠️ ENVOLVER NAO BASTA, E ISSO QUASE ME CUSTOU UMA FIGURA: a copa da
        #    ARVORE3 envolve os galhos de dentro, e a regra apagou a arvore
        #    inteira — sobrou um risquinho. A moldura tambem e MAGRA: e um fio
        #    de contorno, nunca chega a um terco da tinta do recorte. O desenho
        #    que envolve algo e o contrario disso: ele E a tinta toda.
        if not envolve or m.sum() > total * 0.35:
            continue
        for y, x in zip(*np.where(m)):
            r, g, b, al = px[int(x), int(y)]
            px[int(x), int(y)] = (r, g, b, 0)
    return c


# ⚠️ A LISTA ENCOLHEU, E ISSO E BOA NOTICIA (14/set/2026). Ela tinha cinco nomes
#    — sol, terra, passarinho, reino_animal, arvore2 — e cada nome ali era a
#    confissao de um conserto que eu nao sabia medir: "nesta aqui, apague o
#    pedacinho da beirada e torca". Regra de casa e o contrario disso.
#
#    Os cinco viraram DUAS MEDIDAS que valem para qualquer folha:
#      · `apaga_quadradinhos` mata o quadradinho de marcar na FOLHA, pela grade
#        4x5 que os vinte formam (sol, terra, passarinho);
#      · `tira_tracejado` mata o risco da moldura tracejada pela espessura e pelo
#        tamanho medidos (arvore2 — e, de quebra, milho e bola, que ninguem tinha
#        visto porque o risco era pequeno).
#    O reino_animal saiu da lista porque, MEDIDO, ele ja esta limpo: um unico
#    componente de 3.334 px, 88x61, nada solto. A anotacao antiga era de um corte
#    anterior e eu a teria repetido de olhos fechados se nao tivesse conferido.
#
#    Fica vazia de proposito, e nao apagada: e aqui que entra a figura em que a
#    sujeira estiver colada de um jeito que NENHUMA medida alcance — com nome e
#    motivo escritos, porque limpeza que roda em tudo apagaria as pedrinhas
#    soltas do monte de PEDRAS2, que sao desenho.
SOBRA_COLADA = {}


def tira_depois_da_cor(c, sat=60):
    u"""Na folha COLORIDA, apaga o que e sem cor e fica DEPOIS do desenho.

    ⚠️ E o conserto de raiz do quadradinho de marcar da d26. As outras tentativas
       falharam todas pelo mesmo motivo: o quadradinho ENCOSTA na figura (nao ha
       coluna vazia entre os dois, medido: zero vao em sol, terra, passarinho),
       entao nem "peca solta" nem "vao" o alcancam.

       O que o distingue e simples e exato: a figura da d26 e COLORIDA e o
       quadradinho e um traco preto. Entao o desenho acaba na ultima coluna que
       tem COR; o que vier depois dela, e nao tiver cor, e o quadradinho.

    ⚠️ So vale em folha colorida — numa folha de traco o desenho inteiro e sem
       cor e isto apagaria tudo. Por isso quem chama e so o ramo `colorida`."""
    a = np.asarray(c).astype(np.int16)
    alfa = a[..., 3] > 24
    if not alfa.any():
        return c
    mx, mn = a[..., :3].max(axis=2), a[..., :3].min(axis=2)
    cor = alfa & ((mx - mn) > sat)
    if cor.sum() < alfa.sum() * 0.15:
        return c
    ate = int(np.where(cor.any(axis=0))[0].max())
    px = c.load()
    H, W = alfa.shape
    for x in range(ate + 1, W):
        for y in range(H):
            r, g, b, al = px[x, y]
            if al and (max(r, g, b) - min(r, g, b)) <= sat:
                px[x, y] = (r, g, b, 0)
    return c


def tira_sobra_colada(c, piso=0.12):
    u"""Fica com o CORPO da figura e apaga os pedacinhos de beirada.

    So roda nas figuras da lista `SOBRA_COLADA`. A regra: o corpo e o maior
    componente; some qualquer outro que tenha menos de `piso` da tinta E toque
    a borda do recorte. Pedaco pequeno no MEIO da figura (o olho, a semente)
    nao toca borda nenhuma e fica."""
    a = np.asarray(c).astype(np.int16)
    alfa = a[..., 3] > 24
    if not alfa.any():
        return c
    H, W = alfa.shape
    rot, n = nd.label(nd.binary_dilation(alfa, np.ones((3, 3), bool)))
    if n < 2:
        return c
    peso = [((rot == i) & alfa).sum() for i in range(1, n + 1)]
    corpo = int(np.argmax(peso)) + 1
    total = float(alfa.sum())
    px = c.load()
    for i in range(1, n + 1):
        if i == corpo or peso[i - 1] > total * piso:
            continue
        m = (rot == i) & alfa
        yy, xx = np.where(m)
        if not (yy.min() <= 2 or yy.max() >= H - 3 or xx.min() <= 2 or xx.max() >= W - 3):
            continue
        for y, x in zip(yy, xx):
            r, g, b, al = px[int(x), int(y)]
            px[int(x), int(y)] = (r, g, b, 0)
    return c


def recorta_ilha(im, caixa, nome, colorida=False, tem_moldura=False):
    u"""Recorta a ilha, limpa o fundo e salva. Devolve True se saiu figura."""
    y0, y1, x0, x1 = caixa
    folga = 3                      # 3 px de ar, para nao raspar o traco
    c = im.crop((max(0, x0 - folga), max(0, y0 - folga), x1 + folga, y1 + folga))
    c = limpa_fundo(c.convert(u"RGBA"))
    if tem_moldura:
        c = tira_moldura_do_recorte(c)
    if colorida:
        c = tira_peca_solta_sem_cor(c)
        c = tira_depois_da_cor(c)
    if nome in SOBRA_COLADA:
        c = tira_sobra_colada(c)
    c = aperta(tira_halo(aperta(c)))
    # ⚠️ A PAUTA SO SE MEDE DEPOIS DO `aperta`, e eu errei isto na primeira
    #    tentativa: chamei antes, e nada foi apagado. A regra diz "risco encostado
    #    na beirada (ate 3 px)" — mas ANTES do aperta a beirada ainda e o papel
    #    branco da folga do recorte, e o risco ficava a dezenas de pixels dela.
    #    Aqui a caixa ja esta apertada na tinta, que e exatamente o estado em que
    #    os numeros da regra foram medidos.
    # ⚠️ EM RODADAS, ate parar de mudar. Uma passada so nao basta: o `aperta`
    #    que vem depois da limpeza RECORTA a caixa de novo, e um pedacinho que
    #    antes estava no meio do recorte passa a estar a 1 px da beirada nova —
    #    ou seja, so vira "resto da pauta" na rodada seguinte. Com uma passada
    #    ficou 1 px solto na arvore2, e foi o portao 1i6 que me mostrou.
    for _ in range(4):
        antes = c.size
        c = aperta(tira_linha_impressa(c))
        if c.size == antes:
            break
    if c.width < 12 or c.height < 12:
        return False
    salva(c, nome)
    return True


def main():
    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    origem, feitos, problemas = {}, 0, []

    for cod, nomes, faixa, linhas, colorida, tem_moldura in CAIXAS_POR_FOLHA:
        cam = acha(cod)
        if not cam:
            problemas.append(u"%s: nao achei a folha em %s" % (cod, FOLHAS))
            continue
        if tem_moldura:
            cx, im, (H, W) = molduras(cam, faixa, len(nomes))
            # ⚠️ SO 2 px DE FOLGA AQUI. Cortar uma PORCENTAGEM para dentro (tentei
            #    9%) tira a moldura mas tambem come o desenho que ocupa a caixa
            #    inteira: sumiu o circulo da BOLA, o contorno do CUPCAKE e o
            #    traco do BEBE, e sobrou so o miolo. Quem tira a moldura e o
            #    `tira_moldura_do_recorte`, por COMPONENTE — ver ali embaixo.
            cx = [(y0 + 2, y1 - 2, x0 + 2, x1 - 2) for y0, y1, x0, x1 in cx]
        else:
            cx, im, (H, W) = ilhas(cam, faixa, colorida=colorida)
            # ⚠️ Na folha SEM moldura pode sobrar o ROTULO impresso ao lado da
            #    figura (a d07 escreve "REINO MONERA" logo acima do desenho).
            #    Quando sobra ilha, fico com as MAIORES em area — o rotulo e uma
            #    tira fina de texto, a figura e um bloco. Isto e medida, mas nao
            #    e prova: por isso a folha de contato no fim, para OLHAR.
            if len(cx) > len(nomes):
                cx = sorted(cx, key=lambda c: -((c[1]-c[0]) * (c[3]-c[2])))[:len(nomes)]
        cx = em_ordem_de_leitura(cx, H, linhas)
        if len(cx) != len(nomes):
            problemas.append(
                u"%s: achei %d caixa(s) e a lista tem %d nome(s) — NAO vou casar "
                u"no escuro. Rode com --ver %s para olhar." % (cod, len(cx), len(nomes), cod))
            continue
        for caixa, nome in zip(cx, nomes):
            if recorta_ilha(im, caixa, nome, colorida=colorida,
                            tem_moldura=tem_moldura):
                origem[PREFIXO + nome + u".png"] = u"folha:%s" % cod
                feitos += 1
            else:
                problemas.append(u"%s/%s: a ilha saiu vazia depois de limpar o fundo" % (cod, nome))

    # ⚠️ OS SELOS DA CASA TAMBEM SE DECLARAM (ver o portao 1i5).
    for selo in (u"trofeu", u"estrela", u"estrela_off"):
        if os.path.exists(os.path.join(SAIDA, PREFIXO + selo + u".png")):
            origem[PREFIXO + selo + u".png"] = u"selo:casa"

    cam_org = os.path.join(SAIDA, u"ORIGEM.json")
    antes = {}
    if os.path.exists(cam_org):
        antes = json.load(io.open(cam_org, encoding=u"utf-8"))
    # tira do ORIGEM o que nao existe mais no disco (o gelo saiu da lista)
    antes = dict((k, v) for k, v in antes.items()
                 if os.path.exists(os.path.join(SAIDA, k)))
    antes.update(origem)
    io.open(cam_org, u"w", encoding=u"utf-8").write(
        json.dumps(antes, ensure_ascii=False, indent=1, sort_keys=True))

    print(u"recortadas %d figura(s) das folhas de papel -> %s" % (feitos, SAIDA))
    if problemas:
        print(u"   PAROU EM:")
        for x in problemas:
            print(u"    x %s" % x)

    # ⭐ `--ver <cod>`: desenha as caixas achadas POR CIMA da folha e salva, para
    #    eu OLHAR em vez de adivinhar a faixa. Regra do Marcos: nao chutar.
    if u"--ver" in sys.argv:
        alvo = sys.argv[sys.argv.index(u"--ver") + 1]
        for cod, nomes, faixa, linhas, colorida, tem_moldura in CAIXAS_POR_FOLHA:
            if cod != alvo:
                continue
            cam = acha(cod)
            if tem_moldura:
                cx, im, (H, W) = molduras(cam, faixa, len(nomes))
            else:
                cx, im, (H, W) = ilhas(cam, faixa, colorida=colorida)
                if len(cx) > len(nomes):
                    cx = sorted(cx, key=lambda c: -((c[1]-c[0])*(c[3]-c[2])))[:len(nomes)]
            cx = em_ordem_de_leitura(cx, H, linhas)
            v = im.convert(u"RGB").copy()
            dr = ImageDraw.Draw(v)
            dr.rectangle([int(faixa[2]*W), int(faixa[0]*H),
                          int(faixa[3]*W), int(faixa[1]*H)], outline=u"#0066ff", width=4)
            for i, (y0, y1, x0, x1) in enumerate(cx):
                dr.rectangle([x0, y0, x1, y1], outline=u"#ff0000", width=3)
                dr.text((x0 + 3, y0 + 3), str(i), fill=u"#ff0000")
            v.thumbnail((900, 1300))
            saida = u"/tmp/ver_%s.png" % cod
            v.save(saida)
            print(u"%s: %d ilha(s) para %d nome(s) -> %s" % (cod, len(cx), len(nomes), saida))
        return

    contato()
    return 0


def contato():
    u"""A folha de contato das figuras — SEMPRE, e GRANDE o bastante para ver.

    ⚠️ ELA JA EXISTIA E MESMO ASSIM O DEFEITO PASSOU, e o motivo e constrangedor
       de tao simples: a miniatura tinha 130 px. Num quadradinho de 130 px o
       colchete colado na cauda do passarinho e a moldura tracejada em volta da
       arvore nao aparecem — eu OLHEI a folha de contato, achei tudo certo, e
       quem viu o defeito foi o Marcos, na tela da escola. Conferir em miniatura
       nao e conferir: e se tranquilizar.

    ⚠️ E ELA SO SAIA COM `--contato`. Ou seja: a unica defesa contra as duas
       coisas que NENHUM portao mede (o quadradinho fundido e a figura cortada)
       dependia de eu lembrar de pedir. Agora sai sozinha, em telas de 300 px, e
       em LOTES de 12 — porque uma folha unica com 47 figuras volta a ser
       miniatura na hora de abrir.
    """
    ims = sorted(glob.glob(os.path.join(SAIDA, PREFIXO + u"*.png")))
    dest = os.path.join(RAIZ, u"_sequencias", u"crivo")
    if not os.path.isdir(dest):
        os.makedirs(dest)
    try:
        ft = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        ft = ImageFont.load_default()
    cols, th, lote = 6, 300, 12
    saidas = []
    for k in range(0, len(ims), lote):
        grupo = ims[k:k + lote]
        linhas = (len(grupo) + cols - 1) // cols
        f = Image.new(u"RGBA", (cols * th, linhas * (th + 20)), (120, 170, 230, 255))
        d = ImageDraw.Draw(f)
        for i, cam in enumerate(grupo):
            im = Image.open(cam).convert(u"RGBA")
            im.thumbnail((th - 16, th - 16))
            x = (i % cols) * th + (th - im.width) // 2
            y = (i // cols) * (th + 20) + 8
            f.alpha_composite(im, (x, y))
            d.text(((i % cols) * th + 5, (i // cols) * (th + 20) + th),
                   os.path.basename(cam)[len(PREFIXO):-4][:22], font=ft, fill=(0, 0, 0, 255))
        nome = (u"reinos-figuras.png" if k == 0
                else u"reinos-figuras-%d.png" % (k // lote + 1))
        f.convert(u"RGB").save(os.path.join(dest, nome), optimize=True)
        saidas.append(u"_sequencias/crivo/" + nome)
    print(u"   contato-folha das figuras (300 px por tela, ABRIR e OLHAR — e a "
          u"unica defesa contra figura cortada e quadradinho fundido):")
    for s in saidas:
        print(u"     %s" % s)


if __name__ == "__main__":
    sys.exit(main())
