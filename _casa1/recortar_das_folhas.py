# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DE DENTRO DAS FOLHAS DE PROFESSOR

 ⭐ ORDEM DO MARCOS (13/set/2026), dita quatro vezes em duas mensagens:
    *"Lembre-se de aproveitar as imagens das atividades"* · *"Se puder aproveite
    das próprias atividades da internet"* · *"Aproveite das atividades da
    internet as imagens"* · *"O que falta busque essas imagens na internet"*.

    É o mesmo caminho do Bando das Rimas, onde 37 das 56 figuras foram
    RECORTADAS das folhas de papel. Vale mais que desenhar do zero por três
    motivos: a arte é de editora (bonita e coerente), ela é FIEL à folha que deu
    origem à atividade, e não depende da loteria do gerador — que nesta
    atividade já voltou em mancha uma vez.

 ⚠️ A CAIXA É GENEROSA DE PROPÓSITO. Quem aperta é o PIXEL, não o meu olho:
    caixa chutada corta o telhado ou deixa uma faixa de papel colada.

 ⚠️ TRÊS LIMPEZAS QUE A FOLHA DE PAPEL EXIGE, e cada uma foi paga com um corte
    errado antes de virar código:
      1. **o rótulo impresso** — "BARRO" e "PALHA" ficam escritos EMBAIXO do
         desenho e entraram junto na primeira tentativa. A caixa para acima dele.
      2. **a moldura da célula** — as folhas de recortar desenham um retângulo
         preto em volta de cada figura. A primeira versão do `tira_moldura` comia
         a beirada só enquanto ela fosse escura, e parava de cara, porque entre a
         beirada e a moldura há papel BRANCO. Agora ela PROCURA a linha escura
         dentro da faixa externa e corta logo depois dela.
      3. **o número do exercício** — a folha dos profissionais numera cada um
         para a criança ligar na lista. Levado junto, vira um algarismo solto
         boiando ao lado do desenho. Ele é apagado antes do corte.

 ⚠️ O FUNDO SAI POR VIZINHANÇA, entrando pela BORDA. O branco que está DENTRO da
    figura (a janela, o brilho, a parede clara) a água nunca alcança. E apaga com
    degradê: corte seco serrilha a borda.

 DE ONDE VEIO CADA UMA — o crédito fica aqui e no `_sequencias/POTE-MORADIA.md`:
   folhas_moradia/d01 · mundoindica.com        — barraco, casa, prédio, oca, palafita, casa de barro
   folhas_moradia/d22 · pequenolobato.com.br   — tijolo, madeira, palha, barro
   folhas_moradia/d09 · minhasatividades.com   — tenda, casa de madeira
   folhas_moradia/d18 · livro didático (p. 29) — iglu
   mor_extra/d17 · educador.com.br             — castelo
   mor_extra/d18 · educador.com.br             — sobrado
   mor_vistas/d05 · pequenolobato.com.br       — a caneca e o carro nas TRÊS visões
   mor_vistas/d10 · Colégio Dinâmico           — prédio oblíquo, prédio vertical, praça vista de cima
   mor_comodos/d02 · (folha de recortar)       — vaso, cama, banheira, fogão, geladeira, tv, armário, sofá
   mor_obra/d03 · CPR Emprego Integra          — arquiteto, eletricista, encanador, pedreiro, pintor
   mor_lugares/d03 · mundoindica.com           — cidade, campo, beira do rio, deserto (as CENAS do lugar)
   mor_bairro/d13 · livro didático (A. Aguiar) — bairro oblíquo, bairro vertical, os dois meninos do
                                                 ponto de vista
   mor_bairro/d05 · (atividade de geografia)   — a rua de hoje

 ⚠️ UMA FOLHA DA COLHEITA FICOU DE FORA DE PROPÓSITO: a `mor_tempo/d06` traz a
    tira "A Short History of America", de **Robert Crumb** — doze quadros do
    mesmo lugar virando cidade, que seria a figura perfeita da folha 20. É obra
    assinada de autor vivo: a folha de professor pode reproduzi-la, eu não posso
    republicá-la num app. É a mesma linha que já tracei no poema (§POEMA do
    index.html). Arte de banco de imagens genérica eu recorto; obra assinada, não.

 Uso:  python3 _casa1/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import glob
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SEQ = os.path.join(RAIZ, u"_sequencias")
DEST = os.path.join(AQUI, u"img")

LIM = 236        # a partir daqui o pixel conta como "papel" (para APERTAR a caixa)
# ⚠️ AS DUAS RÉGUAS DO FUNDO, e elas são as MESMAS do `_qa/halo.py` de propósito
#    (ver a lição no `limpa_fundo`): a água entra por tudo acima de LIM_AGUA, e o
#    alfa chega a zero em FADE_HI — um pixel abaixo do 225 que o portão vigia.
LIM_AGUA = 210
FADE_LO, FADE_HI = 210, 226
FOLGA = 5        # respiro em volta da figura, depois de apertar no pixel
MAIOR = 420      # lado máximo: a folha viva mostra no máximo ~128 px (256 no 2x)

# pasta/prefixo da folha -> {figura: caixa generosa}
CORTES = [
 (u"folhas_moradia", u"d01", {
   # ⚠️ o BARRACO não entra: ele está na folha de origem, mas o `MOR` deste
   #    caderno tem dez moradias e ele não é uma delas. Recortar o que não se usa
   #    enche a pasta de figura órfã — e a próxima sessão não sabe se é sobra ou
   #    se alguém esqueceu de ligar.
   u"casa":        (276, 534, 447, 692),
   u"predio":      (500, 474, 702, 690),
   u"oca":         (50, 743, 244, 934),
   u"palafita":    (240, 753, 467, 930),
   u"casabarro":   (483, 780, 672, 934)}),
 (u"folhas_moradia", u"d22", {
   u"tijolo":      (496, 342, 662, 458),
   u"madeira":     (498, 502, 662, 658),
   # ⚠️ 784 e não 800: em 800 a palavra "PALHA" entrava junto com o feixe
   u"palha":       (476, 682, 692, 784),
   u"barro":       (470, 852, 694, 935)}),
 (u"folhas_moradia", u"d09", {
   u"tenda":       (175, 626, 410, 970),
   u"casamadeira": (975, 1245, 1335, 1490)}),
 (u"folhas_moradia", u"d18", {
   u"iglu":        (1465, 490, 1690, 660)}),
 (u"mor_extra", u"d17", {
   u"castelo":     (690, 1140, 985, 1430)}),
 (u"mor_extra", u"d18", {
   u"sobrado":     (525, 1550, 900, 1810)}),
 (u"mor_vistas", u"d05", {
   u"caneca_frontal":  (120, 428, 276, 592),
   u"caneca_vertical": (292, 428, 452, 592),
   u"caneca_obliqua":  (470, 430, 624, 590),
   u"carro_frontal":   (174, 700, 284, 798),
   u"carro_vertical":  (334, 672, 392, 810),
   u"carro_obliqua":   (456, 700, 548, 812)}),
 # as CENAS do lugar, da mesma folha (mundoindica) que deu casa/prédio/oca:
 # sair todas da mesma folha é o que faz as seis parecerem irmãs no botão
 (u"mor_lugares", u"d03", {
   u"cidade":     (66, 432, 232, 562),
   u"campo":      (292, 436, 456, 562),
   u"beiradorio": (78, 724, 228, 846),
   # ⚠️ É UM OÁSIS, e está dito assim na tela: areia, palmeiras e um poço de
   #    água. Não é licença poética — é onde a tenda dos nômades para de fato.
   u"deserto":    (70, 922, 240, 1002)}),
 # a PEDRA do castelo: a colheita das folhas de moradia não tinha nenhuma (a
 # folha de materiais do Pequeno Lobato só traz tijolo, madeira, palha e barro),
 # então esta veio da busca de imagens — e entrou uma só, para ficar irmã do
 # feixe de palha e do monte de barro, que também são "um punhado do material"
 (u"mor_mat", u"d04", {
   u"pedra":           (18, 168, 242, 302)}),
 # o PANO da tenda: mesma história da pedra — a folha de materiais não traz, e
 # esta é a única do resultado da busca que é clip-art colorida como as outras
 (u"mor_pano", u"d16", {
   u"pano":            (150, 150, 830, 830)}),
 (u"mor_bairro", u"d13", {
   u"bairro_obliqua":  (14, 84, 328, 292),
   u"bairro_vertical": (14, 405, 326, 618),
   u"olho_obliqua":    (352, 92, 472, 258),
   u"olho_vertical":   (356, 450, 478, 626)}),
]
# folhas com fundo de digitalização acinzentado: o limiar precisa ser mais alto
CORTES_CLAROS = [
 (u"mor_vistas", u"d10", {
   u"predio_obliqua":  (134, 316, 302, 420),
   u"predio_vertical": (434, 302, 645, 414),
   u"praca_vertical":  (122, 648, 352, 800)}),
]
# folhas de RECORTAR: cada figura mora dentro de uma célula com moldura preta
CORTES_COM_MOLDURA = [
 (u"mor_comodos", u"d02", {
   u"vaso":      (94, 668, 222, 774),
   u"cama":      (229, 668, 394, 774),
   u"banheira":  (399, 668, 563, 774),
   u"fogao":     (566, 668, 697, 774),
   u"geladeira": (104, 796, 223, 922),
   u"tv":        (232, 796, 364, 922),
   u"armario":   (392, 796, 517, 922),
   u"sofa":      (562, 796, 699, 922)}),
]
# ⚠️ A RUA DA FERNANDA (mor_bairro/d05) traz uma TARJA LARANJA escrita "CASA DE
#    FERNANDA" colada no céu, em cima do telhado. Ela é da folha de papel, não da
#    cena: no caderno a criança vê "a rua hoje", e um nome de menina que não
#    existe na história atrapalha. Apagar de BRANCO deixaria um retângulo branco
#    no céu, então ela é PINTADA com a cor do próprio céu, colhida ao lado
#    (184,212,215). A placa "CAFETERIA" fica: rua de hoje TEM placa de loja, e é
#    justamente uma das coisas que a criança vai comparar com a rua de antes.
RUA_CEU = (184, 212, 215)
PINTA_D05 = [((338, 196, 488, 226), RUA_CEU)]
CORTES_RUA = {u"ruahoje": (336, 190, 592, 372)}

# ⚠️ FOTO NÃO SE APERTA NEM SE APAGA O FUNDO. As duas fotos do "antes e hoje"
#    são retângulos inteiros: o céu delas é claro, e o `limpa_fundo` comeria o
#    céu pela borda até a foto virar um recorte esburacado. Estas passam por um
#    caminho CRU — corta e redimensiona, mais nada.
#  · a de 1910 é de AUGUSTO MALTA (Copacabana, 1910), reproduzida na folha
#    `mor_tempo/d27` (mundoindica) e em domínio público pela idade;
#  · a de hoje veio do Wikimedia Commons em CC0 (Wilfredor), e o crédito das
#    duas aparece na tela, embaixo da figura.
CORTES_CRUS = [
 (u"mor_tempo", u"d27", # ⚠️ 538 e não 568: a legenda impressa ("Augusto Malta – Copacabana, 1910")
  #    e o endereço de onde a folha tirou a foto começam em y=545
  {u"copa1910": (90, 326, 452, 538)}),
 (u"mor_copa",  u"c12", {u"copahoje": (0, 0, 1920, 1280)}),
]

# a folha dos profissionais numera cada figura: os números são apagados antes
NUMEROS_D03 = [(40, 66, 78, 112), (366, 190, 404, 238), (238, 330, 274, 378),
               (234, 655, 270, 703), (654, 490, 692, 538)]
CORTES_PROFISSOES = {
 u"arquiteto":   (12, 66, 205, 305),
 u"eletricista": (240, 70, 395, 305),
 u"encanador":   (170, 330, 355, 520),
 u"pedreiro":    (105, 525, 265, 745),
 u"pintor":      (585, 500, 725, 735),
}


def acha(pasta, prefixo):
    fs = sorted(glob.glob(os.path.join(SEQ, pasta, prefixo + u"_*")))
    return fs[0] if fs else None


def tira_moldura(im, escuro=120, prop=0.55, faixa=0.3):
    u"""Corta DENTRO da moldura preta da célula (ver a lição 2 no cabeçalho)."""
    a = np.asarray(im.convert(u"RGB")).astype(np.int16)
    al = np.asarray(im.split()[-1]).astype(np.int16)
    dark = (a.max(axis=2) < escuro) & (al > 60)
    h, w = dark.shape
    fh, fw = max(2, int(h * faixa)), max(2, int(w * faixa))
    t, b, l, r = 0, h, 0, w
    for y in range(fh):
        if dark[y, :].mean() > prop:
            t = y + 2
    for y in range(h - 1, h - fh - 1, -1):
        if dark[y, :].mean() > prop:
            b = y - 1
    for x in range(fw):
        if dark[:, x].mean() > prop:
            l = x + 2
    for x in range(w - 1, w - fw - 1, -1):
        if dark[:, x].mean() > prop:
            r = x - 1
    if b - t < 8 or r - l < 8:
        return im
    return im.crop((l, t, r, b))


def limpa_fundo(c, lim, alvo=None):
    u"""Fundo transparente POR VIZINHANÇA, entrando pela borda, com degradê.

    ⚠️⚠️ O HALO BRANCO — a lição mais cara deste recortador (13/set/2026).
       O `_qa/halo.py` reprovou **43 das 57 figuras**: em volta de cada silhueta
       sobrava um anel claro e OPACO — o papel da folha grudado no desenho. No
       creme da folha viva isso aparece como uma auréola em torno de tudo.

       A causa era uma conta minha que não conversava com o portão. O portão
       chama de "quase-branco" tudo acima de **225** e só perdoa o que estiver
       com alfa **abaixo de 40**. O meu degradê ia de 236 a 255: a faixa 225–236
       a água nem alcançava (ficava 100% opaca) e a faixa 236–245 saía com alfa
       200 e tanto. Ou seja: eu media o recorte com uma régua e apagava com
       outra.

       Agora as duas réguas são a mesma. A água entra por tudo o que estiver
       acima de `LIM_AGUA` (210) e o alfa vai a ZERO em `FADE_HI` (226) — o mesmo
       225 do portão, com um pixel de folga. Sobra o degradê 210→226 para o
       contorno não serrilhar. Nada que o portão chame de quase-branco sai opaco.

    ⚠️ E POR ISSO A ÁGUA ENTRA MAIS FUNDO QUE ANTES: um cinza-claro do PRÓPRIO
       desenho que encoste na silhueta pode ser comido junto. É troca consciente
       — halo em 43 figuras é defeito que a criança vê; mordida em cinza-claro
       encostado na borda é caso raro, e a folha de conferência mostra.
    """
    w, h = c.size
    px = c.load()

    def papel(x, y):
        r, g, b, al = px[x, y]
        return al < 16 or (r >= LIM_AGUA and g >= LIM_AGUA and b >= LIM_AGUA)

    vis = [[False] * h for _ in range(w)]
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if papel(x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if papel(x, y) and not vis[x][y]:
                vis[x][y] = True
                fila.append((x, y))
    while fila:
        x, y = fila.popleft()
        r, g, b, al = px[x, y]
        if al:
            claro = (min(r, g, b) - FADE_LO) / float(FADE_HI - FADE_LO)
            px[x, y] = (r, g, b, int(al * (1.0 - max(0.0, min(1.0, claro)))))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not vis[nx][ny] and papel(nx, ny):
                vis[nx][ny] = True
                fila.append((nx, ny))
    return c


def aperta(c, lim):
    a = np.asarray(c.convert(u"RGB")).astype(np.int16)
    massa = (a.min(axis=2) < lim)
    ys, xs = np.where(massa)
    if not len(xs):
        return None
    x1, x2 = max(0, xs.min() - FOLGA), min(c.width, xs.max() + 1 + FOLGA)
    y1, y2 = max(0, ys.min() - FOLGA), min(c.height, ys.max() + 1 + FOLGA)
    return c.crop((x1, y1, x2, y2))


def salva(c, saida):
    bb = c.getbbox()
    if bb:
        c = c.crop(bb)
    if max(c.size) > MAIOR:
        k = MAIOR / float(max(c.size))
        c = c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
    c.save(saida, optimize=True)
    return c


# ⚠️ DUAS CÉLULAS PEDEM FAIXA MENOR: o armário e o fogão encostam na moldura,
#    e com a faixa de 30% a busca pela linha preta avançava para DENTRO da
#    figura e cortava o topo do armário e a lateral do fogão.
MOLDURA_FAIXA = {u"armario": 0.16, u"fogao": 0.16}

# ⚠️ PÁGINA DE LIVRO ESCANEADA NÃO TEM FUNDO BRANCO. Medido no `mor_bairro/d13`:
#    o papel ao lado do menino é (241,242,244) e não 255. O degradê do
#    `limpa_fundo` ia até 255, então esse papel só apagava 26% e os dois meninos
#    saíam dentro de uma névoa cinza opaca — que aparece no creme da folha.
#    Aqui o degradê termina em 240: o papel do livro vira papel puro.
# ⚠️ OS REMENDOS POR FIGURA SUMIRAM. Os dois meninos do livro precisavam de um
#    limiar próprio porque a página de trás transparece em cinza claro (~225) ao
#    lado deles. Com LIM_AGUA=210 valendo para todo mundo, a regra geral já os
#    cobre — e uma regra só é melhor que uma exceção por figura.
ALVO_FIG = {}
LIM_FIG = {}


def recorta(im, box, saida, lim=LIM, moldura=False, faixa=0.3, alvo=255):
    c = im.crop(box)
    if moldura:
        c = tira_moldura(c, faixa=faixa)
    c = aperta(c, lim)
    if c is None:
        return None
    c = limpa_fundo(c, lim, alvo)
    return salva(c, saida)


def main():
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    feitas, faltam, feitas_nomes = 0, [], set()

    def roda(pasta, prefixo, alvos, lim=LIM, moldura=False, apagar=None, pintar=None):
        cam = acha(pasta, prefixo)
        if not cam:
            for n in alvos:
                faltam.append((n, u"%s/%s" % (pasta, prefixo)))
            return 0
        im = Image.open(cam).convert(u"RGBA")
        if apagar:
            d = ImageDraw.Draw(im)
            for bx in apagar:
                d.rectangle(bx, fill=(255, 255, 255, 255))
        if pintar:
            d = ImageDraw.Draw(im)
            for bx, cor in pintar:
                d.rectangle(bx, fill=(cor[0], cor[1], cor[2], 255))
        n = 0
        for nome in sorted(alvos):
            c = recorta(im, alvos[nome], os.path.join(DEST, u"mo_%s.png" % nome),
                        lim=LIM_FIG.get(nome, lim), moldura=moldura,
                        alvo=ALVO_FIG.get(nome, 255),
                        faixa=MOLDURA_FAIXA.get(nome, 0.3))
            if c is None:
                faltam.append((nome, u"%s/%s" % (pasta, prefixo)))
                continue
            n += 1
            feitas_nomes.add(nome)
            print(u"   mo_%-18s %4dx%-4d  <- %s/%s" % (nome + u".png", c.width, c.height,
                                                       pasta, prefixo))
        return n

    for pasta, prefixo, alvos in CORTES:
        feitas += roda(pasta, prefixo, alvos)
    for pasta, prefixo, alvos in CORTES_CLAROS:
        feitas += roda(pasta, prefixo, alvos, lim=228)
    for pasta, prefixo, alvos in CORTES_COM_MOLDURA:
        feitas += roda(pasta, prefixo, alvos, moldura=True)
    feitas += roda(u"mor_obra", u"d03", CORTES_PROFISSOES, apagar=NUMEROS_D03)
    feitas += roda(u"mor_bairro", u"d05", CORTES_RUA, pintar=PINTA_D05)
    for pasta, prefixo, alvos in CORTES_CRUS:
        cam = acha(pasta, prefixo)
        if not cam:
            for n in alvos:
                faltam.append((n, u"%s/%s" % (pasta, prefixo)))
            continue
        im = Image.open(cam).convert(u"RGB")
        for nome in sorted(alvos):
            c = im.crop(alvos[nome])
            if max(c.size) > MAIOR:
                k = MAIOR / float(max(c.size))
                c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
            saida = os.path.join(DEST, u"mo_%s.png" % nome)
            c.save(saida, optimize=True)
            feitas += 1
            feitas_nomes.add(nome)
            print(u"   mo_%-18s %4dx%-4d  <- %s/%s (foto, corte cru)"
                  % (nome + u".png", c.width, c.height, pasta, prefixo))

    # ⚠️ E AS QUE NÃO VIERAM DO RECORTE TAMBÉM PASSAM PELA ÁGUA. O selo do
    #    caderno foi desenhado pelo Pollinations e chegou com a mesma auréola
    #    clara que o portão `halo.py` reprova (3,06%). Uma regra de limpeza que
    #    vale só para metade das figuras não é regra: é costume.
    limpas = 0
    for cam in sorted(glob.glob(os.path.join(DEST, u"mo_*.png"))):
        nome = os.path.basename(cam)[3:-4]
        if nome in feitas_nomes:
            continue
        im = Image.open(cam).convert(u"RGBA")
        if np.asarray(im)[..., 3].min() > 250:
            continue            # sem transparência: não é recorte
        antes = np.asarray(im)[..., 3].copy()
        im = limpa_fundo(im, LIM)
        bb = im.getbbox()
        if bb:
            im = im.crop(bb)
        if not np.array_equal(antes, np.asarray(im)[..., 3]) or bb:
            im.save(cam, optimize=True)
            limpas += 1
    if limpas:
        print(u"   +%d figura(s) que não vieram do recorte passaram pela mesma água"
              % limpas)

    print(u"_casa1 -> %d figura(s) recortada(s) das folhas de professor" % feitas)
    if faltam:
        print(u"   NAO SAIRAM: %s" % u", ".join(u"%s (%s)" % f for f in faltam))
        return 1
    return 0


if __name__ == u"__main__":
    sys.exit(main())
