# -*- coding: utf-8 -*-
u"""
============================================================
 A CAIXA DE FERRAMENTAS DO RECORTE — tirar a figura da FOLHA DE PAPEL

 ⚠️ POR QUE ELA EXISTE (14/set/2026). Estas funções nasceram uma a uma dentro do
    `_reinos/recortar_das_folhas.py`, e cada uma é um defeito que chegou ao
    Marcos: *"tem resto de outras imagens nas imagens, e imagens que faltam
    partes"*. Deixá-las lá dentro significava que o próximo caderno começaria de
    novo do zero e pagaria as mesmas lições — que é exatamente o vício que o
    `_padrao/DINAMICAS.md` combate: **a mecânica já existe, copie, não reescreva**.

 ⚠️ O CÓDIGO AQUI É CÓPIA VERBATIM do que já passou pela banca dos cinco reinos.
    Se precisar mudar alguma regra, mude AQUI e volte a olhar a folha de contato
    dos cadernos que a usam — os números foram medidos em 44 figuras reais e
    estão explicados nos comentários de cada função.

 Quem usa: `_reinos/recortar_das_folhas.py`, `_mult3/recortar_das_folhas.py`.
 Quem mede o resultado: portões **1i5** (`figura_da_folha.py`, a origem) e
 **1i6** (`sobra_da_folha.py`, a pauta da folha que veio junto).
============================================================
"""
from __future__ import print_function

import numpy as np
from PIL import Image
from scipy import ndimage as nd

LIM = 238          # acima disto conta como "papel branco"


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
    # ⚠️ `.copy()`: imagem que vem de `Image.fromarray` é SOMENTE LEITURA, e
    #    aqui se escreve pixel a pixel. Sem isto o recorte morre com
    #    "ValueError: image is readonly" — e morreu duas vezes no mesmo dia,
    #    no _dinheiro5, porque as peças novas (o corte circular da moeda e o
    #    corte por contorno) passam por numpy antes de chegar aqui. A correção
    #    é na FERRAMENTA, não em cada caderno: o próximo que usar numpy não
    #    paga de novo.
    c = c.copy()
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
