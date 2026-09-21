# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DAS FOLHAS DE PAPEL — _dinheiro5

 ⚠️ REGRA DA ORIGEM (Marcos, 14/set/2026): ***"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"***. Toda figura deste caderno
    sai de uma das 120 folhas colhidas em `_sequencias/folhas_dinheiro5*`, e o
    crivo que as julgou é o `_sequencias/POTE-DINHEIRO5.md`.

 ⚠️ AS CAIXAS SÃO EM FRAÇÃO da imagem (x0, y0, x1, y1), nunca em pixels: assim
    o corte não depende do tamanho do arquivo e continua valendo se a folha for
    recolhida maior.

 ⚠️ O DINHEIRO É O MATERIAL DESTE CADERNO, e por isso ele sai da folha que o
    mostra melhor: a **c30** (`d30_cb999e.png`, 1500x1900) traz as cinco moedas
    e as sete cédulas da família em curso, coloridas, de frente, numa página só.
    ⭐ A cédula de **R$ 200** só existe nela e na a10 — e a de **R$ 1,00** (c31,
    c40) ficou de FORA de propósito: não circula mais, e pôr na caixa
    registradora da escola o que a criança não vê no mercado seria ensinar
    errado (ver POTE §6).

 Uso: python3 _dinheiro5/recortar_das_folhas.py
 Mede o resultado: portões 1i5 (`figura_da_folha.py`) e 1i6 (`sobra_da_folha.py`)
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, u"_padrao"))
from recorte_folha import limpa_fundo, tira_halo, aperta     # noqa: E402

SAIDA = os.path.join(AQUI, u"img")
PREFIXO = u"dn5_"

# ============================================================
#  AS FOLHAS DE ONDE SAI CADA COISA
# ============================================================
F = {
    u"c30": u"folhas_dinheiro5c/d30_cb999e.png",   # o dinheiro (5 moedas + 7 cédulas)
    u"c32": u"folhas_dinheiro5c/d32_452d99.jpg",   # sapatinho, bolo, cofrinho, brinquedos
    u"c01": u"folhas_dinheiro5c/d01_61d6b5.jpg",   # a prateleira do supermercado
    u"c35": u"folhas_dinheiro5c/d35_0e3299.png",   # o mercadinho e cinco produtos
    u"c24": u"folhas_dinheiro5c/d24_a9de57.jpg",   # oito brinquedos com etiqueta
    u"c28": u"folhas_dinheiro5c/d28_35181f.jpg",   # a cesta da lojinha da Júlia
    u"c11": u"folhas_dinheiro5c/d11_fb3f87.jpg",   # o pote de vidro (cofrinho)
}

# --- c30: o dinheiro. Medido na folha com grade de 5% (ver POTE §6).
#     A fila de moedas está em y 0.365-0.458; as cédulas em quatro fileiras.
#
# ⚠️ AS MOEDAS E AS CÉDULAS SE RECORTAM DE DOIS JEITOS, e a primeira rodada
#    provou por quê:
#    · A MOEDA é redonda: tem de sair com fundo TRANSPARENTE, senão aparece um
#      quadrado branco em volta dela na folha colorida. Vai pelo `limpa_fundo`.
#    · A CÉDULA é um retângulo e **o miolo dela é claro**. Rodar o `limpa_fundo`
#      nela foi um erro medido: a nota de R$ 200 saiu com um BURACO no meio (a
#      água entrou pela borda cortada e comeu o papel claro da própria cédula).
#      Cédula se corta com margem folgada e se APARA pelo branco do papel, sem
#      transparência nenhuma.
# ⚠️ ESTAS FRAÇÕES NÃO FORAM ESTIMADAS NO OLHO — foram MEDIDAS no arquivo,
#    contando tinta por linha e por coluna (limiar 246 de branco). A primeira
#    rodada, feita a olho sobre uma grade de 5%, trouxe fatia da moeda vizinha
#    em três recortes e fatia da fileira de cima em quatro cédulas.
#    As faixas horizontais medidas: moedas 0.3695-0.4605 · cédulas 0.4700-0.5816,
#    0.5889-0.7011, 0.7084-0.8205 · a de R$ 200 em 0.8247-0.9300.
#
# ⚠️⚠️ AS MOEDAS SE TOCAM, E EU DEMOREI TRÊS RODADAS PARA ACEITAR ISSO.
#    1ª: perfil de tinta por coluna -> "a fila é uma mancha só" -> reparti em
#        cinco passos iguais -> lasca da vizinha em três recortes.
#    2ª: ampliei a fila a 2x e "vi" vãos de papel -> ajustei as bordas a olho ->
#        as mesmas três lascas, no mesmo lugar. O que eu tomei por vão era
#        SOMBRA CLARA; baixando o limiar até 180 a fila continuou sendo UMA
#        mancha só, ou seja, elas se encostam mesmo.
#    3ª: parei de procurar borda reta. **Moeda é círculo**, e círculo que se
#        toca se separa pelo CENTRO, não pela caixa: transformada de distância
#        na mancha, os cinco máximos locais são os cinco centros, e o valor do
#        máximo é o raio. Medido, em fração da largura da folha:
#          1 real  cx 0.2773  r 0.0580     50c  cx 0.3933  r 0.0522
#          25c     cx 0.5007  r 0.0550     10c  cx 0.6040  r 0.0453
#          5c      cx 0.7000  r 0.0500
#        ⭐ E ESSA MEDIDA SE CONFERE SOZINHA: a razão entre os raios (87:78:83:
#        68:75 px) bate com o diâmetro real das moedas (27:23:25:20:22 mm). É a
#        prova de que os círculos achados são as moedas, e não ruído.
#    **Lição: quando a peça tem forma conhecida, medir a FORMA vence medir a
#    caixa — e "eu vi no zoom" não é medida.**
# (cx, cy, r) em fração da LARGURA da folha para cx e r, e da ALTURA para cy.
MOEDAS = [
    (u"m100", 0.2773, 0.4147, 0.0580),   # 1 real
    (u"m50",  0.3933, 0.4184, 0.0522),   # 50 centavos
    (u"m25",  0.5007, 0.4168, 0.0550),   # 25 centavos
    (u"m10",  0.6040, 0.4184, 0.0453),   # 10 centavos
    (u"m05",  0.7000, 0.4184, 0.0500),   # 5 centavos
]
CEDULAS = [
    (u"c2",   0.1400, 0.4700, 0.4420, 0.5816),
    (u"c5",   0.4970, 0.4700, 0.8040, 0.5816),
    (u"c10",  0.1400, 0.5889, 0.4700, 0.7011),
    (u"c20",  0.4960, 0.5889, 0.8390, 0.7011),
    (u"c50",  0.1400, 0.7084, 0.4850, 0.8205),
    (u"c100", 0.4970, 0.7084, 0.8430, 0.8205),
    (u"c200", 0.3170, 0.8247, 0.6690, 0.9300),
]

# ============================================================
#  OS PRODUTOS — o cenário do caderno
#
#  ⚠️ TODOS SAEM DAS FOLHAS COLHIDAS, e cada bloco diz de qual e por quê.
#     Estes recortes SIM têm fundo transparente (`limpa_fundo`): são peças
#     soltas sobre papel branco, não retângulos impressos como a cédula.
# ============================================================
# --- c01 (= a26): a prateleira do supermercado. ⭐ É a única folha das 120 com
#     produto de mercado E preço COM CENTAVOS (5,30 · 4,50 · 9,00 · 6,30 · 7,00),
#     que é o degrau do 5º ano. O arquivo tem 2480x3509: dá recorte grande.
PRODUTOS = [
    (u"c01", u"arroz",     0.085, 0.2325, 0.215, 0.3236),
    (u"c01", u"macarrao",  0.255, 0.2325, 0.385, 0.3236),
    (u"c01", u"feijaolata", 0.435, 0.2325, 0.555, 0.3236),
    (u"c01", u"atum",      0.595, 0.2325, 0.730, 0.3236),
    (u"c01", u"ovos",      0.765, 0.2325, 0.905, 0.3236),
    # --- c35: o MERCADINHO e cinco produtos. A loja inteira é a cena da capa.
    (u"c35", u"mercadinho", 0.370, 0.200, 0.630, 0.318),
    (u"c35", u"feijao",    0.150, 0.330, 0.240, 0.408),
    (u"c35", u"cafe",      0.410, 0.320, 0.495, 0.412),
    (u"c35", u"leite",     0.675, 0.330, 0.750, 0.412, u"contorno"),
    (u"c35", u"margarina", 0.305, 0.450, 0.415, 0.522),
    (u"c35", u"carne",     0.580, 0.455, 0.705, 0.522),
    # --- c24: os oito brinquedos com etiqueta (a lojinha de brinquedos)
    (u"c24", u"urso",      0.100, 0.220, 0.250, 0.340),
    (u"c24", u"dado",      0.520, 0.220, 0.670, 0.330),
    (u"c24", u"piao",      0.110, 0.415, 0.260, 0.535),
    (u"c24", u"domino",    0.515, 0.420, 0.695, 0.510),
    (u"c24", u"boneca",    0.125, 0.610, 0.255, 0.725),
    (u"c24", u"peteca",    0.540, 0.600, 0.665, 0.720),
    (u"c24", u"boliche",   0.095, 0.805, 0.260, 0.925),
    (u"c24", u"bola",      0.525, 0.815, 0.665, 0.920),
]

CAIXAS = [(u"c30", n, a, b, c, d, False) for (n, a, b, c, d) in CEDULAS] + \
         [(p[0], p[1], p[2], p[3], p[4], p[5], p[6] if len(p) > 6 else True)
          for p in PRODUTOS]

PAPEL = 246        # acima disto, na média dos três canais, é o branco do papel


def so_a_maior(c):
    u"""Fica só com a MAIOR ilha de tinta, e joga fora as lascas.

    ⚠️ POR QUE ELA EXISTE: a moeda é redonda e as cinco ficam lado a lado na
    folha, com **sombra** entre elas. Qualquer caixa um fio larga demais traz
    uma lasca da vizinha, e na tela a criança vê meia moeda colada na outra —
    figura errada, não enfeite. A conta certa não é de caixa, é de ILHA: a moeda
    é uma mancha conectada e grande; a lasca é outra mancha, pequena e encostada
    na borda.

    ⚠️ ELA NÃO SUBSTITUI A CAIXA CERTA, e isto foi medido: enquanto as caixas
    estavam erradas, a lasca encostava na moeda pela SOMBRA e virava a MESMA
    ilha — esta função não tinha o que jogar fora. Ela é a rede, não a régua.
    """
    import numpy as np
    from scipy import ndimage as nd
    a = np.array(c.convert(u"RGBA"))
    marca, quantas = nd.label(a[:, :, 3] > 24)
    if quantas < 2:
        return c
    tam = nd.sum(marca > 0, marca, range(1, quantas + 1))
    maior = int(np.argmax(tam)) + 1
    a[:, :, 3] = np.where(marca == maior, a[:, :, 3], 0)
    return Image.fromarray(a, u"RGBA")


def apara_papel(c):
    u"""Corta as faixas de PAPEL BRANCO das quatro bordas, sem mexer no miolo.

    ⚠️ Por que não é o `aperta`: o `aperta` trabalha na TRANSPARÊNCIA, e a
    cédula não tem nenhuma (ver o comentário das caixas). Aqui a conta é
    simples: uma linha inteira acima de `PAPEL` é papel, e papel de borda sai.
    """
    import numpy as np
    a = np.asarray(c.convert(u"RGB")).mean(axis=2)
    lin = (a > PAPEL).all(axis=1)          # linhas que são só papel
    col = (a > PAPEL).all(axis=0)          # colunas que são só papel
    y0, y1 = 0, c.height
    while y0 < y1 and lin[y0]:
        y0 += 1
    while y1 > y0 and lin[y1 - 1]:
        y1 -= 1
    x0, x1 = 0, c.width
    while x0 < x1 and col[x0]:
        x0 += 1
    while x1 > x0 and col[x1 - 1]:
        x1 -= 1
    return c.crop((x0, y0, x1, y1))


def recorta_por_contorno(c, lim=244):
    u"""Recorta uma figura de MIOLO BRANCO, pelo contorno desenhado dela.

    ⚠️ POR QUE ELA EXISTE, medido: a caixa de LEITE da folha c35 é branca com um
    traço preto em volta. O `limpa_fundo` derrama água branca a partir da borda
    e ela entrou pelo BICO da embalagem (o traço tem um vão ali) — o miolo da
    caixa foi embora e sobrou só o contorno com as manchinhas de vaca boiando.
    Na tela isso não é "figura com fundo transparente": é figura destruída.

    A conta certa para este caso é outra: fechar o contorno (`binary_closing`),
    tapar os buracos de dentro (`binary_fill_holes`) e ficar com a maior ilha.
    O branco de DENTRO passa a ser parte da figura, e o de fora continua fora.
    """
    import numpy as np
    from scipy import ndimage as nd
    a = np.array(c.convert(u"RGBA"))
    tinta = np.asarray(c.convert(u"RGB")).mean(axis=2) < lim
    tinta = nd.binary_closing(tinta, np.ones((7, 7)))
    cheio = nd.binary_fill_holes(tinta)
    marca, quantas = nd.label(cheio)
    if quantas:
        tam = nd.sum(cheio, marca, range(1, quantas + 1))
        cheio = marca == (int(np.argmax(tam)) + 1)
    a[:, :, 3] = np.where(cheio, 255, 0).astype(np.uint8)
    return Image.fromarray(a, u"RGBA")


def recorta_moeda(folha, nome, cx, cy, r):
    u"""Recorta UMA moeda pelo círculo dela — centro e raio, não caixa.

    A borda ganha uma casquinha de 3 px de folga (a moeda tem relevo e sombra
    própria) e sai suavizada, para não ficar serrilhada na tela.
    """
    import numpy as np
    cam = os.path.join(RAIZ, u"_sequencias", F[folha])
    im = Image.open(cam).convert(u"RGB")
    W, H = im.size
    R = r * W + 3
    cxp, cyp = cx * W, cy * H
    cx0, cy0 = int(cxp - R), int(cyp - R)
    c = im.crop((cx0, cy0, int(cxp + R), int(cyp + R))).convert(u"RGBA")
    yy, xx = np.ogrid[:c.height, :c.width]
    dist = np.sqrt((xx - (cxp - cx0)) ** 2 + (yy - (cyp - cy0)) ** 2)
    # 0 dentro do raio, 1 fora; a beirada de 1,5 px derrete para não serrilhar
    alfa = np.clip((R - dist) / 1.5, 0, 1) * 255
    a = np.array(c)
    a[:, :, 3] = alfa.astype(np.uint8)
    return Image.fromarray(a, u"RGBA")


def recorta(folha, nome, x0, y0, x1, y1, fundo=True):
    cam = os.path.join(RAIZ, u"_sequencias", F[folha])
    im = Image.open(cam).convert(u"RGB")
    W, H = im.size
    c = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if fundo == u"contorno":
        c = recorta_por_contorno(c)
        c = aperta(c)
    elif fundo:
        c = limpa_fundo(c)
        c = tira_halo(c)
        c = so_a_maior(c)
        c = aperta(c)
    else:
        c = apara_papel(c).convert(u"RGBA")
    # ⚠️ o teto de 400 px de altura é o da casa: acima disso o arquivo pesa sem
    #    a criança ver diferença, e o `naoAmplia` já impede a ampliação.
    if c.height > 400:
        c = c.resize((max(1, int(c.width * 400.0 / c.height)), 400), Image.LANCZOS)
    dest = os.path.join(SAIDA, PREFIXO + nome + u".png")
    c.save(dest, optimize=True)
    return dest, c.size


def main():
    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    # ⚠️ DOIS ARQUIVOS, E ISSO NÃO É CAPRICHO. O `ORIGEM.json` é um CONTRATO da
    #    casa que o portão 1i5 (`_qa/figura_da_folha.py`) lê: uma linha por
    #    figura, e o valor é TEXTO no formato "folha:d26" · "banco:maca" ·
    #    "gerada:pollinations". Eu escrevi um objeto ali com a caixa do recorte
    #    dentro, e o portão morreu com AttributeError em vez de medir. A caixa
    #    do recorte é informação MINHA, para refazer o corte depois; ela mora no
    #    `RECORTE.json`, que portão nenhum lê.
    origem, detalhe = {}, {}
    for nome, cx, cy, r in MOEDAS:
        c = recorta_moeda(u"c30", nome, cx, cy, r)
        dest = os.path.join(SAIDA, PREFIXO + nome + u".png")
        c.save(dest, optimize=True)
        origem[PREFIXO + nome + u".png"] = u"folha:c30"
        detalhe[PREFIXO + nome + u".png"] = {
            u"folha": F[u"c30"], u"circulo": [cx, cy, r], u"tamanho": list(c.size)}
        print(u"%-18s %s  (circulo)" % (os.path.basename(dest), c.size))
    for folha, nome, x0, y0, x1, y1, fundo in CAIXAS:
        dest, tam = recorta(folha, nome, x0, y0, x1, y1, fundo)
        origem[PREFIXO + nome + u".png"] = u"folha:" + folha
        detalhe[PREFIXO + nome + u".png"] = {
            u"folha": F[folha], u"caixa": [x0, y0, x1, y1], u"tamanho": list(tam)}
        print(u"%-18s %s" % (os.path.basename(dest), tam))
    for cam, dados in ((u"ORIGEM.json", origem), (u"RECORTE.json", detalhe)):
        cam = os.path.join(SAIDA, cam)
        ja = {}
        if os.path.exists(cam):
            ja = json.loads(io.open(cam, encoding=u"utf-8").read())
        ja.update(dados)
        io.open(cam, u"w", encoding=u"utf-8").write(
            json.dumps(ja, ensure_ascii=False, indent=1, sort_keys=True))
    print(u"\n%d figuras -> %s" % (len(origem), SAIDA))


if __name__ == u"__main__":
    main()
