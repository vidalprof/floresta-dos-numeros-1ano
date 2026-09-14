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

from PIL import Image, ImageDraw, ImageFont

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
D26 = [u"terra", u"vento", u"sapo", u"gelo",
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


def grade(cod, nomes, x0, y0, x1, y1, cols, linhas, folgax=0.0, folgay=0.0):
    u"""Gera as caixas de uma grade regular, em fração da imagem."""
    fora = []
    lw = (x1 - x0) / float(cols)
    lh = (y1 - y0) / float(linhas)
    for i, nome in enumerate(nomes):
        c, l = i % cols, i // cols
        fora.append((cod, nome,
                     (x0 + c * lw + folgax, y0 + l * lh + folgay,
                      x0 + (c + 1) * lw - folgax, y0 + (l + 1) * lh - folgay)))
    return fora


# ⚠️ QUATRO FIGURAS DA d26 ENCOSTAM NO QUADRADINHO — a asa da borboleta, o raio
#    do sol, a linha do gelo e o montinho de terra chegam perto dele, e aí não há
#    coluna vazia entre os dois para o `tira_solto_direita` achar. Para essas
#    quatro a largura vai declarada, medida uma a uma. Chutar aqui é o que faz o
#    quadradinho aparecer na tela da criança.
ESTREITAS = {u"borboleta": 0.128, u"gelo": 0.120, u"sol": 0.128, u"terra": 0.132}


def cel(cod, nomes, colsx, rowsy, larg, alt):
    u"""Grade em que a figura fica à ESQUERDA e o quadradinho de marcar à
    direita (d26). A caixa para ANTES do quadradinho, de propósito: na primeira
    rodada ele veio junto em dezenove das vinte figuras."""
    fora = []
    for i, nome in enumerate(nomes):
        cx = colsx[i % len(colsx)]
        ry = rowsy[i // len(colsx)]
        w = ESTREITAS.get(nome, larg)
        fora.append((cod, nome, (cx, ry - alt, cx + w, ry + alt)))
    return fora


CAIXAS = []
# ⚠️ as colunas e linhas da d26 foram MEDIDAS desenhando a grade por cima da
#    folha e olhando o resultado — não chutadas. O quadradinho de marcar começa
#    em cx + 0,18. A caixa vai LARGA de propósito (0,185, pega o quadradinho)
#    e quem tira o quadradinho depois é o `tira_solto_direita`, por medida.
CAIXAS += cel(u"d26", D26,
              [0.026, 0.281, 0.536, 0.791], [0.415, 0.532, 0.654, 0.781, 0.903],
              0.158, 0.065)
# ⚠️ na d20 e na d22 cada figura mora dentro de um retângulo TRACEJADO. A folga
#    grande é para o corte cair DENTRO do tracejado: o `tira_moldura` sabe comer
#    linha cheia, e linha pontilhada ele deixa passar.
CAIXAS += grade(u"d20", D20, 0.060, 0.660, 0.810, 0.925, 4, 2, folgax=0.030, folgay=0.024)
CAIXAS += grade(u"d22", D22, 0.100, 0.245, 0.900, 0.905, 3, 4, folgax=0.040, folgay=0.030)
CAIXAS += [
    (u"d07", u"reino_monera",   (0.140, 0.640, 0.280, 0.716)),
    (u"d07", u"reino_plantae",  (0.285, 0.640, 0.425, 0.716)),
    (u"d07", u"reino_protista", (0.430, 0.640, 0.570, 0.716)),
    (u"d07", u"reino_fungi",    (0.575, 0.640, 0.715, 0.716)),
    (u"d07", u"reino_animal",   (0.720, 0.640, 0.860, 0.716)),
]


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


def tira_halo(c, lim=212, voltas=4):
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


def recorta(cod, nome, fr, moldura=False):
    cam = acha(cod)
    if not cam:
        return None
    im = Image.open(cam).convert(u"RGBA")
    W, H = im.size
    box = (int(fr[0] * W), int(fr[1] * H), int(fr[2] * W), int(fr[3] * H))
    if box[2] <= box[0] or box[3] <= box[1]:
        return None
    c = im.crop(box)
    if moldura:
        c = tira_moldura(c)
    c = aperta(tira_solto_direita(limpa_fundo(c)))
    c = aperta(tira_halo(tira_risco(c)))
    if c.width < 12 or c.height < 12:
        return None
    salva(c, nome)
    return cod


def main():
    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    origem = {}
    feitos, falhou = 0, []
    for cod, nome, fr in CAIXAS:
        mold = cod in (u"d20", u"d22")
        r = recorta(cod, nome, fr, moldura=mold)
        if r:
            origem[PREFIXO + nome + u".png"] = u"folha:%s" % cod
            feitos += 1
        else:
            falhou.append((cod, nome))
    # ⚠️ OS SELOS DA CASA TAMBEM SE DECLARAM. O trofeu e as estrelinhas do
    #    boletim nao vieram de folha de papel nenhuma — sao peca do motor desta
    #    casa —, e o portao 1i5 reprova qualquer PNG que esteja no disco sem
    #    dizer de onde veio. Declarar "selo:casa" e a resposta honesta; deixar de
    #    fora seria o portao aprovando por descuido.
    for selo in (u"trofeu", u"estrela", u"estrela_off"):
        if os.path.exists(os.path.join(SAIDA, PREFIXO + selo + u".png")):
            origem[PREFIXO + selo + u".png"] = u"selo:casa"
    cam_org = os.path.join(SAIDA, u"ORIGEM.json")
    antes = {}
    if os.path.exists(cam_org):
        antes = json.load(io.open(cam_org, encoding=u"utf-8"))
    antes.update(origem)
    io.open(cam_org, u"w", encoding=u"utf-8").write(
        json.dumps(antes, ensure_ascii=False, indent=1, sort_keys=True))
    print(u"recortadas %d figura(s) das folhas de papel -> %s" % (feitos, SAIDA))
    if falhou:
        print(u"   nao saiu: %s" % u", ".join(u"%s/%s" % f for f in falhou))

    if u"--contato" in sys.argv:
        ims = sorted(glob.glob(os.path.join(SAIDA, PREFIXO + u"*.png")))
        cols, th = 7, 130
        linhas = (len(ims) + cols - 1) // cols
        f = Image.new(u"RGBA", (cols * th, linhas * (th + 18)), (120, 170, 230, 255))
        d = ImageDraw.Draw(f)
        try:
            ft = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except Exception:
            ft = ImageFont.load_default()
        for i, cam in enumerate(ims):
            im = Image.open(cam).convert(u"RGBA")
            im.thumbnail((th - 12, th - 12))
            x = (i % cols) * th + (th - im.width) // 2
            y = (i // cols) * (th + 18) + 6
            f.alpha_composite(im, (x, y))
            d.text(((i % cols) * th + 4, (i // cols) * (th + 18) + th),
                   os.path.basename(cam)[len(PREFIXO):-4][:18], font=ft, fill=(0, 0, 0, 255))
        f.convert(u"RGB").save(os.path.join(RAIZ, u"_sequencias", u"crivo",
                                            u"reinos-figuras.png"), optimize=True)
        print(u"   contato-folha das figuras: _sequencias/crivo/reinos-figuras.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
