# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DESTE CADERNO SAEM DAS FOLHAS DE PAPEL

 ⭐ Regra do Marcos (14/set/2026): *"procure na internet, nada de imagem gerada
    por IA, utilize das atividades"*. Cada figura aqui foi RECORTADA de uma
    folha que a professora usa no papel — a MESMA folha que deu o gesto.

 Folhas de origem (colhidas em 24/set/2026 por `buscar-fotos.yml`):
   · `d06` — "DIVISÃO. REPARTA EM PARTES IGUAIS. CLIQUE E ARRASTE. 8 CENOURAS
     PARA 2 COELHOS / 6 PEIXES EM 2 AQUÁRIOS" — é o papel pedindo ARRASTAR com
     todas as letras, e traz cenoura, coelho, peixe e aquário coloridos.
   · `d15` — quatro problemas com figura: balas, cédulas, flores e cubinhos.
   · `d26` — "QUANTOS PARA CADA UM? CALCULE E COMPLETE", tabela com gato,
     pote de ração, criança, carrinho, vaso, flor, maçã, cenoura e coelho.

 ⚠️⚠️ POR QUE AQUI O RECORTE NÃO É UMA GRADE CALCULADA, como foi no `_sil3`.
    Naquele caderno a folha tinha uma grade DESENHADA (linhas pretas que
    atravessam a página) e as bordas saíam da projeção de tinta. Estas cinco
    não têm grade nenhuma: são molduras arredondadas, caixas lilás e desenhos
    soltos. Tentei achar as figuras pela COR (pixel saturado, já que o texto é
    preto e o fundo é branco) e o método **acha seis das nove** da d04 — os
    óculos, o robô e o dominó são CINZA e PRETO, e ficam invisíveis para ele.
    **Medida que só enxerga metade não é medida.** Por isso o caminho aqui é
    outro: a caixa de cada figura é MARCADA, uma a uma, lendo a folha ampliada,
    e depois CRESCE até a tinta acabar (`cresce_caixa`) — o mesmo guarda de
    60% de contenção do `_dinheiro5`, que impede a moldura de arrastar a caixa.

 ⚠️ A CAIXA SE CONFERE NA FOLHA DE ORIGEM, nunca no PNG (lição de 21/set/2026):
    o `aperta()` tira o branco de sobra e o recorte SEMPRE sai com cara de
    figura inteira, mesmo com metade do desenho cortada. O `img/RECORTE.json`
    guarda a folha e a caixa, e o portão `1i7` volta lá para medir.

 Uso: python3 _tonica3/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "_padrao"))
from recorte_folha import (limpa_fundo, tira_halo, aperta,        # noqa: E402
                           tira_linha_impressa, tira_fundo_claro)

IMG = os.path.join(AQUI, "img")
COLHEITA = os.path.join(RAIZ, "_sequencias", "colheita", "div3")


def folha(pref):
    u"""O nome do arquivo traz um sufixo de hash que muda a cada colheita; o
    PREFIXO (`d04b1`) é o que não muda. Fixar o nome inteiro faria o script
    quebrar na próxima vez que alguém recolhesse as folhas."""
    g = sorted(glob.glob(os.path.join(COLHEITA, pref + "_*")))
    if not g:
        raise SystemExit(u"nao achei a folha %s em %s" % (pref, COLHEITA))
    return g[0]


# ⚠️ AS CAIXAS SÃO EM FRAÇÃO DA FOLHA e foram MEDIDAS abrindo cada folha
#    ampliada — nunca escritas de cabeça. **Fração chutada não é medida**: no
#    `_sil3` isso custou duas rodadas de conserto (o tatu saiu com 86x19 px).
#    (nome, folha, x0, y0, x1, y1)
PECAS = [
    # ---- d06: "8 CENOURAS PARA 2 COELHOS" e "6 PEIXES EM 2 AQUÁRIOS" ----
    #  ⚠️ estas foram achadas MEDINDO (mancha colorida dilatada) e depois
    #     conferidas na folha de contato — nunca escritas de cabeça.
    (u"dd3_cenoura",  u"d06b1", 0.017, 0.243, 0.145, 0.335),
    (u"dd3_coelho",   u"d06b1", 0.076, 0.380, 0.216, 0.540),
    (u"dd3_peixe",    u"d06b1", 0.028, 0.690, 0.180, 0.756),
    (u"dd3_aquario",  u"d06b1", 0.316, 0.706, 0.614, 0.910),
    # ---- d15: as figuras dos quatro problemas ----
    #  ⚠️ AS BALAS E AS CÉDULAS VÊM EM MONTE NA FOLHA, e a primeira medida
    #     pegou o monte inteiro (com um pedaço da pergunta escrita por cima).
    #     Aqui se recorta UMA de cada: a criança precisa de uma peça para
    #     repetir quantas vezes a conta pedir, não de um punhado pronto.
    #  ⚠️ `veu=1`: o papel em volta desta bala chegou ao scan AMARELADO (252,
    #     244, 231) e o `limpa_fundo` nao o alcanca — 17% da figura saia como
    #     papel opaco e o portao 0o6 via 5,66% de halo branco. Ver
    #     `tira_fundo_claro` em _padrao/recorte_folha.py.
    (u"dd3_bala",     u"d15b1", 0.733, 0.185, 0.868, 0.238, 1, 1, 1),
    (u"dd3_nota",     u"d15b1", 0.770, 0.386, 0.915, 0.489),
    #  ⚠️ a borda da caixa do problema passa logo abaixo das flores e entrava
    #     como uma barra preta; o corte para antes dela.
    (u"dd3_flor",     u"d15b1", 0.339, 0.650, 0.478, 0.719),
    (u"dd3_cubinho",  u"d15b1", 0.404, 0.828, 0.486, 0.888),
    # ---- d26: a tabela "QUANTOS PARA CADA UM? CALCULE E COMPLETE" ----
    #  ⚠️ A CÉLULA DESTA TABELA TEM DOIS GATOS E SEIS POTES DE RAÇÃO, e o corte
    #     antigo trazia os dois gatos mais a BORDA DE CIMA dos potes de baixo —
    #     que no PNG viravam duas meias-luas pontilhadas penduradas embaixo do
    #     desenho (foi o que o portão 1i6 viu: 20 px, 0,55% do corpo). O corte
    #     agora é de UM gato só, medido na folha ampliada: a tinta forte do gato
    #     da esquerda vai de x 86 a 149 e de y 253 a 356, e os potes só começam
    #     em y 358. Mesma regra das balas: a criança repete a peça quantas vezes
    #     a conta pedir. E `cresce=0`, porque a caixa foi medida na tinta e
    #     crescer daqui só reencontraria o vizinho.
    (u"dd3_gato",     u"d26b1", 0.1157, 0.2410, 0.2005, 0.3390, 1, 0),
    #  ⚠️ O POTE DE RAÇÃO É A PEÇA QUE SE REPARTE no problema dos gatos, e
    #     ele estava faltando: a folha mostra DOIS gatos e SEIS potes, e a
    #     pergunta impressa é "quantos potes para cada gato?". Sem o pote, a
    #     tela repetia o GATO dez vezes para dizer "dez potes" — figura que
    #     contradiz o enunciado. Medido na folha ampliada com régua: o pote
    #     de baixo à esquerda vai de x 93 a 146 e de y 364 a 394 — medido no
    #     perfil de tinta coluna a coluna e linha a linha, não a olho: a
    #     primeira medida saiu 5 px curta à direita e o portão 1i7 pegou o pote
    #     partido. A caixa leva 1 px de folga e NÃO cresce, porque o pote do
    #     meio começa em x 153 e a linha da tabela em y 399.
    (u"dd3_pote",     u"d26b1", 0.1252, 0.3467, 0.1978, 0.3762, 1, 0),
]


def cresce_caixa(im, cx, teto=1.6, lim=232):
    u"""A caixa marcada a olho CORTA — a mancha de tinta que encosta na borda
    continua para fora dela. Aqui a caixa cresce até a tinta acabar.

    ⚠️ A mancha só conta se 60% dela estiver DENTRO da caixa inicial (lição paga
       no `_dinheiro5`): sem isso, a MOLDURA da folha, que atravessa tudo,
       arrastaria a caixa até engolir a página inteira."""
    import numpy as np
    from scipy import ndimage

    x0, y0, x1, y1 = cx
    W, H = im.size
    mx, my = int((x1 - x0) * (teto - 1) / 2), int((y1 - y0) * (teto - 1) / 2)
    ax0, ay0 = max(0, x0 - mx), max(0, y0 - my)
    ax1, ay1 = min(W, x1 + mx), min(H, y1 + my)
    a = np.asarray(im.convert("L").crop((ax0, ay0, ax1, ay1)))
    marca, n = ndimage.label(a < lim)
    if not n:
        return cx
    jan = marca[y0 - ay0:y1 - ay0, x0 - ax0:x1 - ax0]
    dentro = set()
    for i in np.unique(jan):
        if not i:
            continue
        if (jan == i).sum() >= 0.60 * (marca == i).sum():
            dentro.add(int(i))
    if not dentro:
        return cx
    ys, xs = np.where(np.isin(marca, list(dentro)))
    return (ax0 + int(xs.min()), ay0 + int(ys.min()),
            ax0 + int(xs.max()) + 1, ay0 + int(ys.max()) + 1)


def tira_moldura(im):
    u"""Apaga a MOLDURA ARREDONDADA dos quadros da folha — e ela sai da folha
    INTEIRA, antes de qualquer caixa ser medida.

    ⚠️⚠️ **QUANDO DUAS COISAS SE GRUDAM, QUEM TEM DE SAIR SAI ANTES DE GRUDAR.**
       O robô encosta a antena na linha de cima do quadro: as duas viram UMA
       mancha só, o `cresce_caixa` segue a mancha e a caixa engole a moldura.
       Eu tentei duas vezes separá-las DEPOIS — por formato (a moldura ocupa a
       caixa toda e é oca) e por linha fina (atravessa 70% da caixa com branco
       em cima e embaixo). As duas falharam pelo mesmo motivo: depois de
       grudadas não há regra de forma que as separe, porque elas são uma coisa
       só. A régua certa vem antes.

    ⚠️ E a moldura se reconhece pelo QUE ELA É: uma mancha da cor lilás desta
       folha, GRANDE (mais de 300 px de lado). A bolinha da antena do robô é
       quase da mesma cor e tem 20 px — por isso o piso de tamanho, e não a cor
       sozinha."""
    import numpy as np
    from scipy import ndimage

    a = np.asarray(im).astype(int)
    lilas = ((a[:, :, 2] > 170) & (a[:, :, 0] > 110) &
             (a[:, :, 0] < 190) & (a[:, :, 1] < 140))
    if not lilas.any():
        return im
    # ⚠️ SEM DILATAR ANTES DE ROTULAR, e isto foi conserto medido: a bolinha
    #    da antena do robô é quase da cor da moldura e encosta nela. Dilatando
    #    2 px antes, as duas viram uma mancha só, a mancha passa do piso de
    #    300 px de lado e a bolinha é apagada junto — o portão `1i7` acusou o
    #    robô cortado em 19 px. Rotula-se a tinta CRUA; só o que for moldura
    #    de verdade é que engorda, na hora de virar branco.
    marca, n = ndimage.label(lilas)
    fora = np.zeros_like(lilas)
    for i, sl in enumerate(ndimage.find_objects(marca)):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h > 300 and w > 300:
            fora |= (marca == i + 1)
    if not fora.any():
        return im
    arr = np.asarray(im).copy()
    arr[ndimage.binary_dilation(fora, iterations=2)] = 255
    return Image.fromarray(arr)


def so_o_desenho(im, cx):
    u"""Dentro da caixa marcada, fica SÓ o desenho — a palavra escrita ao lado
    é apagada.

    ⚠️ **DESCARTAR A MANCHA NÃO BASTA, porque o corte é retângulo** (lição paga
       no `_sil3` em 23/set/2026): a letra que sobra dentro do retângulo aparece
       na tela como um risquinho solto. Por isso o descartado é APAGADO da
       folha antes de cortar, e a mancha se engorda 3 px antes de virar branco —
       apagar só o preto deixa o cinza da borda do scan.

    ⚠️ E o critério não é a cor: **três das nove figuras desta folha são
       PRETAS OU CINZAS** (os óculos, o dominó, o robô). Quem procura figura por
       saturação acha seis de nove — medida que só enxerga metade não é medida.
       O critério é o TAMANHO E A VIZINHANÇA: o desenho é a maior mancha da
       caixa, mais tudo o que encosta nela; a palavra escrita é letra solta.
    """
    import numpy as np
    from scipy import ndimage

    x0, y0, x1, y1 = cx
    peca = im.crop((x0, y0, x1, y1)).convert("RGB")
    a = np.asarray(peca)
    tinta = (np.asarray(peca.convert("L")) < 225) | ((a.max(2).astype(int) - a.min(2)) > 40)
    marca, n = ndimage.label(ndimage.binary_dilation(tinta, iterations=3))
    if n < 2:
        return peca
    tam = ndimage.sum(tinta, marca, range(1, n + 1))
    ordem = list(np.argsort(tam)[::-1] + 1)
    # ⚠️ A MOLDURA DO QUADRO É MAIOR QUE O DESENHO, e ela entrou no robô —
    #    cujo antena encosta nela. Uma moldura se reconhece sem saber a cor
    #    dela: ocupa quase toda a caixa nos DOIS lados e é OCA (a tinta enche
    #    menos de 15% da própria área). Um desenho é o contrário.
    A, L = tinta.shape
    maior = None
    for c in ordem:
        sl = ndimage.find_objects((marca == c).astype(int))[0]
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        cheio = (tinta & (marca == c)).sum() / float(max(1, w * h))
        if h > 0.85 * A and w > 0.85 * L and cheio < 0.15:
            continue                      # é moldura, não é o desenho
        maior = int(c)
        break
    if maior is None:
        maior = int(ordem[0])
    sobra = (marca != maior) & tinta
    if sobra.any():
        arr = a.copy()
        arr[ndimage.binary_dilation(marca != maior, iterations=2) & tinta] = 255
        peca = Image.fromarray(arr)
    return peca


def main():
    if not os.path.isdir(IMG):
        os.makedirs(IMG)
    # ⚠️ AS TRÊS PEÇAS DE INTERFACE VÊM DO ESQUELETO e não saem de folha de
    #    papel nenhuma. Declaram-se `banco:`, senão o portão 1i5 diz, com razão,
    #    que há figura no disco sem procedência.
    abertas, recorte = {}, {}
    origem = {u"dd3_selo.png": u"banco:selo",
              u"dd3_selo_off.png": u"banco:selo",
              u"dd3_trofeu.png": u"banco:trofeu"}
    for peca in PECAS:
        nome, pref, fx0, fy0, fx1, fy1 = peca[:6]
        so_maior = peca[6] if len(peca) > 6 else 1
        cresce = peca[7] if len(peca) > 7 else 1
        veu = peca[8] if len(peca) > 8 else 0
        cam = folha(pref)
        if pref not in abertas:
            abertas[pref] = tira_moldura(Image.open(cam).convert("RGB"))
        f = abertas[pref]
        W, H = f.size
        cx = (int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H))
        if cresce:
            cx = cresce_caixa(f, cx)
        peca_img = so_o_desenho(f, cx) if so_maior else f.crop(cx)
        c = limpa_fundo(peca_img.convert("RGBA"))
        if veu:
            c = tira_fundo_claro(c)
        c = tira_halo(c, voltas=2)
        # ⚠️ O RISCO DA PAUTA SOBRA DEPOIS DE TUDO, e o portão 1i6 o vê: na bala
        #    (6x6 px) e nos gatos (5x2 px) o que ficava pendurado na beirada era
        #    o tracejado impresso da folha, não desenho. A régua que separa os
        #    dois já está medida em `_padrao/recorte_folha.py` (0,50% da tinta do
        #    corpo e 3 px de beirada) — aqui é só usá-la. E vem ANTES do
        #    `aperta`, porque é o cisco que estava definindo a borda do corte.
        c = tira_linha_impressa(c)
        c = aperta(c)
        c.thumbnail((400, 400))
        c.save(os.path.join(IMG, nome + ".png"))
        origem[nome + ".png"] = u"folha:%s (%s)" % (pref, os.path.basename(cam))
        recorte[nome + ".png"] = {
            u"folha": os.path.relpath(cam, RAIZ),
            u"caixa": list(cx),
            u"tamanho": list(c.size),
        }
        print(u"  %-14s %s  %dx%d" % (nome, pref, c.size[0], c.size[1]))

    for arq, dado in ((u"ORIGEM.json", origem), (u"RECORTE.json", recorte)):
        io.open(os.path.join(IMG, arq), "w", encoding="utf-8").write(
            json.dumps(dado, ensure_ascii=False, indent=1) + u"\n")
    print(u"\n%d figura(s) em %s" % (len(PECAS), IMG))


if __name__ == "__main__":
    main()
