# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DAS FOLHAS DE PAPEL — A Fábrica de Nomes (5º ano)

 ⭐ A REGRA QUE MANDA AQUI (Marcos, 14/set/2026): *"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"*. Toda figura deste caderno sai
    da MESMA folha de papel que deu origem à folha da tela — assim a criança
    reencontra o desenho que a professora entrega impresso.

 DE ONDE VEM CADA GRUPO, e o comando impresso daquela folha:
   · d04 (tudoportugues) — *"4. Circule as imagens cujos nomes são substantivos
     compostos."* → pão, couve-flor, livros, beija-flor, tênis, guarda-chuva.
     São as seis do exercício, coloridas e sobre branco.
   · d26 (cartaz "Substantivo primitivo ou derivado?") → dente, dentadura,
     chute, chuteira: os dois pares que o cartaz mostra lado a lado.
   · d25 (clickescolar) — o cartaz mostra o MESMO pato como *pato* e como
     *Patolino*, e a MESMA menina como *menina* e como *Marcela*. É o conceito
     de comum × próprio numa imagem só, e é a folha 1 deste caderno.
   · d28 (Atividades Suzano) — *"Pinte o retângulo de acordo com o substantivo
     indicado"* → cavalo, igreja, casa e o cão Pluto, em traço preto.

 ⚠️ AS CAIXAS FORAM MEDIDAS, NÃO CHUTADAS: cada grupo vem de uma varredura das
    linhas escuras da própria imagem (ver `_grade()`), e os números abaixo são o
    que a varredura devolveu. Onde a folha não tem moldura (a d04), a caixa é a
    área do exercício, também medida, e as seis peças saem por ILHAS DE TINTA.

 ⚠️ E O NOME TEM DE BATER COM O DESENHO. Trocar um nome aqui não dá erro nenhum:
    só faz a criança ver uma chuteira onde a palavra diz DENTADURA. Conferir
    OLHANDO a folha de contato em /tmp/conferir_subst5.png.

 Uso:  python3 _subst5/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys
from collections import deque

try:
    from PIL import Image
    import numpy as np
except ImportError as e:                                   # pragma: no cover
    print(u"preciso de Pillow+numpy (%s)" % e)
    sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_subst5")
DEST = os.path.join(AQUI, u"img")

# as réguas da casa: a água entra acima de 210 e o alfa zera em 226
LIM_AGUA = 210
FADE_LO = 210.0
FADE_HI = 226.0
LIM = 200          # o que conta como "massa" do desenho
FOLGA = 4
MAIOR = 300        # ⚠️ 300 e não 260: a regra de resolução do `leiaute_mao.js`
                   #    reprova figura mostrada acima de 1,35x da propria altura,
                   #    e estas aparecem grandes (a folha 1 mostra o par lado a
                   #    lado). Guardar maior custa alguns KB e evita o borrao.

# ---------------------------------------------------------------------------
# AS CAIXAS, MEDIDAS NA IMAGEM
# ---------------------------------------------------------------------------
# d04 (1809 x 2560) — o bloco das seis figuras do exercicio 4, em duas fileiras
D04 = {
    u"arquivo": u"d04_a3befd.jpg",
    u"area": (940, 1330, 1720, 1800),
    u"linhas": [(0, 250), (250, 470)],
    u"colunas": [(0, 265), (265, 520), (520, 780)],
    u"nomes": [[u"pao", u"couveflor", u"livros"],
               [u"beijaflor", u"tenis", u"guardachuva"]],
}
# ⚠️ AS TRÊS CAIXAS ABAIXO NASCERAM ERRADAS E FORAM MEDIDAS DE NOVO OLHANDO A
#    FOLHA DE CONTATO (15/set/2026). Na primeira passada elas trouxeram junto:
#      · na d26, o cabeçalho "primitivo / derivado" e a barra verde do cartaz;
#      · na d25, a palavra `pato` e a palavra `menina` escritas sob o desenho;
#      · na d28, a moldura da caixa, o nome CAVALO/PLUTO/IGREJA/CASA em letra de
#        forma e os dois botões COMUM/PRÓPRIO.
#    As duas últimas são o defeito grave: a RESPOSTA vinha impressa dentro da
#    própria figura, e a folha da tela que pede "comum ou próprio?" já entregava
#    o nome. Nenhum portão vê isso — quem viu foi o olho, na folha de contato,
#    que é exatamente para isto. Por isso agora cada grupo diz quanto cortar.
#    (`so_desenho` = fica só com as ilhas de tinta do desenho — ver `so_o_desenho`.)
#
# d26 (1131 x 1600) — os dois pares do cartaz. A barra verde foi MEDIDA (pixel
#     verde > 100 com vermelho e azul < 110): colunas 566 a 584. As caixas param
#     antes dela de um lado e começam depois dela do outro.
D26 = {
    u"arquivo": u"d26_e9ff3d.jpg",
    u"area": (105, 690, 1065, 1330),
    u"linhas": [(0, 240), (390, 640)],
    u"colunas": [(0, 440), (490, 960)],
    u"nomes": [[u"dente", u"dentadura"], [u"chute", u"chuteira"]],
}
# d25 (1086 x 1536) — o pato e a menina do cartaz, SEM a palavra embaixo
D25 = {
    u"arquivo": u"d25_71eb29.jpg",
    u"area": (95, 730, 500, 868),
    u"linhas": [(0, 138)],
    u"colunas": [(0, 170), (170, 405)],
    u"nomes": [[u"pato", u"menina"]],
}
# d28 (1131 x 1600) — quatro das nove figuras. As linhas da grade foram MEDIDAS
#     (fileiras escuras em 9, 373, 738 e 1027; colunas em 339, 670 e 1000). Fica
#     só a metade esquerda de cada caixa (o nome está à direita) e o pé sai
#     fora (é onde moram os botões COMUM/PRÓPRIO).
D28 = {
    u"arquivo": u"d28_2cceb6.jpg",
    u"area": (72, 395, 1060, 1500),
    u"linhas": [(12, 370), (377, 735), (742, 1024)],
    u"colunas": [(0, 325), (330, 655), (660, 985)],
    u"so_desenho": True,
    u"nomes": [[u"cavalo", None, u"pluto"],
               [None, None, u"igreja"],
               [None, u"casa", None]],
}
# d27 (743 x 1050) — a grade de oito do *"RECORTE OS SUBSTANTIVOS E COLE NA
#     COLUNA CORRETA"*. É a folha mais BAIXA da colheita, e por isso dela só
#     saem as figuras que faltam nas outras: Ana, Davi e o mapa do Brasil — os
#     três únicos nomes PRÓPRIOS com desenho de toda a colheita. Sem eles a
#     folha 3 teria três comuns para cada próprio e a criança acertaria no
#     chute.
# ⚠️ E ELAS FICAM PEQUENAS DE PROPÓSITO: a régua de resolução do
#    `_qa/leiaute_mao.js` reprova figura mostrada acima de 1,35x da própria
#    altura. Guardadas em ~95 px, elas aparecem em ~95 px na tela. A saída
#    honesta para uma folha de baixa resolução é mostrar no tamanho dela —
#    nunca ampliar, e (regra do Marcos, 14/set) nunca gerar por IA.
#    A grade foi MEDIDA: linhas escuras em 204, 312 e 420; colunas em 67, 218,
#    371 e 677, com o passo de 153 px dando a coluna que faltava em 524.
D27 = {
    u"arquivo": u"d27_2bd7a7.jpg",
    u"area": (67, 204, 677, 420),
    u"linhas": [(2, 106), (110, 214)],
    u"colunas": [(2, 149), (155, 302), (308, 455), (461, 608)],
    u"so_desenho": True,
    # ⚠️ O NOME FICA À DIREITA DO DESENHO EM TODAS AS OITO CAIXAS DESTA FOLHA, e
    #    nesta resolução as letras são grossas o bastante para passarem pela
    #    regra de densidade do `so_o_desenho` — o mapa do Brasil saiu com um
    #    "RAS" pendurado ao lado. Vista na folha de contato, corrigida cortando
    #    a faixa da direita antes das ilhas.
    u"corta_dir": 0.62,
    u"maior": 110,
    u"nomes": [[None, None, u"ana", None],
               [None, u"davi", None, u"brasil"]],
}
GRUPOS = [D04, D26, D25, D28, D27]

# os selos da casa (troféu e estrelas) NÃO são conteúdo da folha: vêm do banco
# e precisam estar declarados, senão o `_qa/figura_da_folha.py` reprova "figura
# no disco que ninguém declarou" toda vez que este script rodar.
SELOS = ((u"sb_trofeu.png", u"banco:trofeu"),
         (u"sb_selo.png", u"banco:selo"),
         (u"sb_selo_off.png", u"banco:selo"))


def papel_de(px, x, y):
    r, g, b, al = px[x, y]
    return al < 16 or (r >= LIM_AGUA and g >= LIM_AGUA and b >= LIM_AGUA)


def limpa_fundo(c):
    u"""Fundo transparente por vizinhança, entrando pelas bordas, com degradê."""
    w, h = c.size
    px = c.load()
    vis = [[False] * h for _ in range(w)]
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if papel_de(px, x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if papel_de(px, x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    while fila:
        x, y = fila.popleft()
        r, g, b, al = px[x, y]
        if al:
            claro = (min(r, g, b) - FADE_LO) / (FADE_HI - FADE_LO)
            px[x, y] = (r, g, b, int(al * (1.0 - max(0.0, min(1.0, claro)))))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vis[nx][ny] and papel_de(px, nx, ny):
                vis[nx][ny] = True
                fila.append((nx, ny))
    return c


def aperta(c):
    a = np.asarray(c.convert(u"RGB")).astype(np.int16)
    ys, xs = np.where(a.min(axis=2) < LIM)
    if not len(xs):
        return None
    x1, x2 = max(0, xs.min() - FOLGA), min(c.width, xs.max() + 1 + FOLGA)
    y1, y2 = max(0, ys.min() - FOLGA), min(c.height, ys.max() + 1 + FOLGA)
    return c.crop((int(x1), int(y1), int(x2), int(y2)))


def tira_fantasma(c):
    u"""Apaga a FILEIRA que sobra colada na beirada (moldura, barra do cartaz).

    ⚠️ MEDIDO na Loteria do S (15/set/2026) e herdado daqui: o
       `_qa/sobra_da_folha.py` conta pixel com alfa acima de 40 e acusa
       "linha impressa atravessando a figura". A régua dele é OUTRA — não é a
       tinta escura, é a opacidade —, e quando duas peças medem a mesma coisa
       com réguas diferentes, quem manda é a régua do PORTÃO.
    ⚠️ A regra é de BEIRADA e de contraste: a fileira só sai se ela estiver
       cheia e a de dentro estiver quase vazia. Assim a moldura sai e o desenho
       (que continua para dentro) fica.
    """
    a = np.asarray(c.convert(u"RGBA"))
    op = a[:, :, 3] > 40
    h, w = op.shape
    y1, y2, x1, x2 = 0, h, 0, w
    for _ in range(4):
        if y2 - y1 > 4 and op[y1, x1:x2].mean() > 0.8 and op[y1 + 1, x1:x2].mean() < 0.3:
            y1 += 1
        if y2 - y1 > 4 and op[y2 - 1, x1:x2].mean() > 0.8 and op[y2 - 2, x1:x2].mean() < 0.3:
            y2 -= 1
        if x2 - x1 > 4 and op[y1:y2, x1].mean() > 0.8 and op[y1:y2, x1 + 1].mean() < 0.3:
            x1 += 1
        if x2 - x1 > 4 and op[y1:y2, x2 - 1].mean() > 0.8 and op[y1:y2, x2 - 2].mean() < 0.3:
            x2 -= 1
    if (y1, y2, x1, x2) == (0, h, 0, w):
        return c
    return c.crop((x1, y1, x2, y2))


def so_o_desenho(c, guarda=0.09):
    u"""Fica só com as ILHAS DE TINTA do desenho, jogando fora o resto da caixa.

    ⚠️ ESTA PEÇA SUBSTITUIU UM CORTE FIXO, e a razão é medida (15/set/2026): na
       d28 cada caixa traz a figura, o NOME em letra de forma ao lado e dois
       botões COMUM/PRÓPRIO no pé. Tentei cortar por fração ("fica 56% da
       largura, sai 19% da altura") e não deu: as três fileiras têm alturas
       diferentes (358, 358 e 282 px medidos) e a figura não está no mesmo lugar
       em cada uma — ou sobrava um pedaço de botão, ou a casa era decepada.
    ⚠️ E o que sobrava era GRAVE, não feio: o nome vinha impresso DENTRO da
       figura, e a folha da tela que pergunta "comum ou próprio?" já entregava a
       resposta ao lado do desenho.
       A régua certa não é geométrica, é de MASSA: o desenho é a maior mancha de
       tinta da caixa; o nome e os botões são manchas pequenas e separadas dela.
       Ficam as ilhas com pelo menos `guarda` da área da maior — assim as folhas
       soltas ao lado do cavalo e os risquinhos do cão continuam, e a palavra e
       os botões saem.
    """
    a = np.array(c.convert(u"RGBA"))      # cópia: o `asarray` vem só de leitura
    tinta = (a[:, :, 3] > 40) & (a[:, :, :3].min(axis=2) < 235)
    h, w = tinta.shape
    dono = np.zeros((h, w), dtype=np.int32)
    areas, cx, n = [0], [None], 0
    for y0 in range(h):
        for x0 in range(w):
            if not tinta[y0, x0] or dono[y0, x0]:
                continue
            n += 1
            fila = deque([(y0, x0)])
            dono[y0, x0] = n
            area = 0
            x1 = x2 = x0
            y1 = y2 = y0
            while fila:
                y, x = fila.popleft()
                area += 1
                if x < x1: x1 = x
                if x > x2: x2 = x
                if y < y1: y1 = y
                if y > y2: y2 = y
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1),
                               (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and tinta[ny, nx] and not dono[ny, nx]:
                        dono[ny, nx] = n
                        fila.append((ny, nx))
            areas.append(area)
            cx.append((x1, y1, x2, y2))
    if n < 2:
        return c
    # ⚠️ A ÁREA SOZINHA NÃO BASTA: o botão vazio da d28 é um RETÂNGULO OCO, e a
    #    borda dele tem tanto pixel de tinta quanto um desenho pequeno — o cavalo
    #    saiu com o botão pendurado embaixo. Um retângulo oco é quase todo vazio
    #    por dentro; um desenho, não. Por isso entra a DENSIDADE: tinta da ilha
    #    dividida pela área do retângulo que a envolve. Abaixo de 12% é moldura.
    def densa(i):
        x1, y1, x2, y2 = cx[i]
        return areas[i] / float(max(1, (x2 - x1 + 1) * (y2 - y1 + 1))) >= 0.12
    maior = max((i for i in range(1, n + 1) if densa(i)),
                key=lambda i: areas[i], default=None)
    if maior is None:
        return c
    fica = [i for i in range(1, n + 1)
            if areas[i] >= areas[maior] * guarda and densa(i)]
    a[:, :, 3] = np.where(np.isin(dono, fica), a[:, :, 3], 0)
    saida = Image.fromarray(a)
    bb = saida.getbbox()
    return saida.crop(bb) if bb else saida


def main():
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    origem, feitas = {}, []
    for G in GRUPOS:
        cam = os.path.join(FOLHAS, G[u"arquivo"])
        if not os.path.exists(cam):
            print(u"  ! nao achei %s" % cam)
            continue
        base = Image.open(cam).convert(u"RGBA").crop(G[u"area"])
        marca = G[u"arquivo"].split(u"_")[0]
        for r, (y1, y2) in enumerate(G[u"linhas"]):
            for c, (x1, x2) in enumerate(G[u"colunas"]):
                nome = G[u"nomes"][r][c]
                if not nome:
                    continue
                cx = base.crop((x1, y1, x2, y2))
                # o corte que tira o nome impresso e os botoes da caixa
                if G.get(u"corta_dir") or G.get(u"corta_baixo"):
                    cx = cx.crop((0, 0,
                                  int(cx.width * G.get(u"corta_dir", 1.0)),
                                  cx.height - int(cx.height * G.get(u"corta_baixo", 0))))
                cx = aperta(cx)
                if cx is None:
                    print(u"  ! %s: caixa vazia" % nome)
                    continue
                cx = limpa_fundo(cx)
                bb = cx.getbbox()
                if bb:
                    cx = cx.crop(bb)
                cx = tira_fantasma(cx)
                # ⚠️ VALE PARA TODOS OS GRUPOS desde 15/set/2026: o
                #    `_qa/sobra_da_folha.py` acusou a dentadura (resto de 8x1 px)
                #    e o tênis (3x4) de terem "pauta da folha dentro". São pedaços
                #    da linha impressa do papel que sobreviveram ao recorte, e a
                #    régua dele (alfa acima de 40) os enxerga mesmo eu não vendo.
                #    A mesma peça que tirava o NOME de dentro da figura tira
                #    estes: eles são ilhas de tinta minúsculas, longe do desenho.
                cx = so_o_desenho(cx)
                teto = G.get(u"maior", MAIOR)
                if max(cx.size) > teto:
                    k = teto / float(max(cx.size))
                    cx = cx.resize((max(1, int(cx.width * k)), max(1, int(cx.height * k))),
                                   Image.LANCZOS)
                cx.save(os.path.join(DEST, u"sb_%s.png" % nome), optimize=True)
                origem[u"sb_%s.png" % nome] = u"folha:%s" % marca
                feitas.append((nome, cx))
                print(u"  ok %-13s %dx%d   (%s)" % (nome, cx.width, cx.height, marca))

    for selo, de in SELOS:
        if os.path.exists(os.path.join(DEST, selo)):
            origem[selo] = de
    with io.open(os.path.join(DEST, u"ORIGEM.json"), u"w", encoding=u"utf-8") as f:
        f.write(json.dumps(origem, indent=1, sort_keys=True, ensure_ascii=False))

    # ⚠️ A FOLHA DE CONFERÊNCIA É PARA OLHAR. Nenhum portão vê se o recorte ficou
    #    bonito, nem se o NOME bate com o desenho; quem vê é o olho.
    larg, alt, porlin = 190, 210, 6
    linhas = (len(feitas) + porlin - 1) // porlin
    fl = Image.new(u"RGB", (larg * porlin, alt * max(1, linhas)), u"#f6f2e6")
    for i, (nome, c) in enumerate(feitas):
        d = c.copy()
        d.thumbnail((165, 165))
        fl.paste(d, ((i % porlin) * larg + 12, (i // porlin) * alt + 20), d)
    fl.save(u"/tmp/conferir_subst5.png")
    print(u"\n%d figuras. folha de conferencia: /tmp/conferir_subst5.png "
          u"(OLHAR, nao confiar)" % len(feitas))
    return 0


if __name__ == u"__main__":
    sys.exit(main())
