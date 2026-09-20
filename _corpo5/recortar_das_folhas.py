# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DESTE CADERNO SAEM DAS FOLHAS DE PAPEL COLHIDAS

 ⚠️ REGRA DA ORIGEM (Marcos, 14/set/2026): *"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"*. Gesto e desenho nascem na
    MESMA folha: a criança reconhece na tela a atividade que a professora dá no
    papel. Nenhuma figura deste caderno foi desenhada por IA.

 ⚠️ UMA FAMÍLIA DE ARTE SÓ — e a escolha custou uma folha boa. A **d44** traz
    oito órgãos em ícones COLORIDOS e isolados (estômago, boca, intestinos,
    pulmão, fígado, coração), que seria o recorte mais fácil das 78. Ficou de
    fora por duas medidas:
      · cada célula da grade dela tem **86 × 86 px** — na tela, a 120 px, já
        passaria do teto de 1,35× do portão de resolução;
      · e ela é colorida, enquanto as folhas de maior resolução (d29 com
        2895 × 4096) são a TRAÇO PRETO. Misturar as duas deixaria o caderno com
        duas famílias de arte — a lição que ficou escrita no `_sinon2`.
    Então: **tudo a traço preto**, das folhas de maior resolução.

 DE ONDE VEM CADA FIGURA, e por que aquela folha:
   · **d29** (2895 × 4096, a maior das 78) — *"SISTEMA DIGESTÓRIO"*, com as seis
     fichas laterais recortáveis: intestino grosso, intestino delgado, esôfago,
     estômago, fígado e pâncreas. Na folha de papel elas são para recortar e
     colar no menino — que é exatamente o gesto que a tela dá.
   · **d25** (1146 × 1600) — *"O CAMINHO DO AR"*: o tronco com o percurso
     inteiro e, no canto, os alvéolos ampliados. É o esquema mais limpo do
     respiratório das 78.
   · **c08** (1136 × 1600) — *"TUM TUM BATE CORAÇÃO"*: o coração a traço, em
     tamanho grande. A folha é cartaz (não tem tarefa) e por isso não virou
     folha nenhuma — mas a figura dela é a melhor do circulatório.
   · **c26** (1179 × 1600) — o esquema PULMÃO ↔ CORAÇÃO ↔ CORPO, que é a
     INTEGRAÇÃO dos três sistemas num desenho só.

 Uso:  python3 _corpo5/recortar_das_folhas.py
 Quem mede: portões 1i5 (`figura_da_folha.py`) e 1i7 (`recorte_cortado.py`).
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_padrao"))
from recorte_folha import limpa_fundo, tira_halo, aperta   # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..")
FOLHAS = os.path.join(BASE, "_sequencias", "folhas_corpo5")
CIRC = os.path.join(BASE, "_sequencias", "folhas_corpo5circ")
DEST = os.path.join(AQUI, "img")

# ⚠️ APAGAR — caixas que sao PINTADAS DE BRANCO na folha ANTES do recorte.
#    Nasceu do coracao: a folha c08 tem nove rotulos em volta do orgao ("Veia
#    cava superior", "Atrio direito", "Ventriculo esquerdo"...), ligados por
#    linhas finas. Recortar por fora deles pegava meia palavra ("...riculo",
#    "esq..."); recortar por dentro CORTAVA O PROPRIO CORACAO. A saida e apagar
#    o texto e ficar com o desenho inteiro e limpo.
#    ⚠️ E ha um motivo pedagogico junto: esses nove rotulos sao todos da faixa
#       FORA DO ANO do crivo (atrio, ventriculo, aorta). A figura do 5o ano e o
#       orgao, nao a legenda de anatomia.
#    ⚠️ E A CAIXA DO RECORTE VEIO DEPOIS DAS CAIXAS DE APAGAR, nao antes. Na
#       primeira tentativa eu apertei o recorte para fugir dos rotulos e o
#       coracao saiu CORTADO: faltava a veia cava inferior inteira, o atrio
#       direito pela metade e a ponta de baixo, que aparecia solta como um
#       risco pendurado (foi assim que o portao 1i6 acusou "pauta da folha
#       dentro" — nao era pauta, era o proprio orgao decepado). O certo e o
#       contrario: primeiro a caixa que pega o DESENHO inteiro, depois tantas
#       caixas de apagar quantas forem precisas para os rotulos que caem
#       dentro dela.
APAGAR = {
    # ⚠️ A d25 desenha os alvéolos DENTRO DE UMA MOLDURA, com a palavra
    #    "Alvéolos" escrita embaixo e a seta de chamada entrando por cima. A
    #    moldura foi medida (x 723..1008, y 1223..1524) e o recorte entra 3 px
    #    para dentro dela; a palavra SAI, porque o caderno pede justamente que a
    #    criança nomeie essa parte — figura com o nome escrito é gabarito de
    #    graça (a lição que a prova de Ed. Física deixou). A seta sai junto: sem
    #    o resto da folha ela vira um risco apontando para nada.
    #    As duas caixas foram conferidas contra o desenho: nenhuma encosta nele.
    # ⚠️ A d13 é uma folha de NOMEAR: em volta do menino há nove retângulos
    #    vazios para a criança escrever. Recortados junto, viram caixas soltas
    #    penduradas na figura. Estes três são os pedaços que caem dentro da
    #    caixa do recorte; os outros seis ficam fora dela.
    "vd_corpores": [(798, 896, 872, 976), (848, 715, 872, 796), (848, 1395, 872, 1424)],
    "vd_alveolos": [(762, 1226, 800, 1264),    # a ponta da seta de chamada
                    (729, 1466, 862, 1510)],   # a palavra "Alvéolos"
    "vd_coracao": [(262, 250, 408, 316),    # "Veia cava superior"
                   (264, 420, 358, 492),    # "Atrio direito"
                   (432, 236, 586, 302),    # "Arteria pulmonar"
                   (793, 250, 890, 296),    # "Aorta"
                   (773, 355, 862, 428),    # "Veias pulmonares"
                   (768, 596, 880, 684),    # "Atrio esquerdo"
                   (230, 540, 292, 632),    # "Veia cava inferior"
                   # ⚠️ ESTAS DUAS ENCOSTAM NA PONTA DE BAIXO DO CORACAO. Na
                   #    tentativa de cima elas comecavam em y=906 e COMERAM um
                   #    pedaco do contorno: a curva do apice sobra solta, e o
                   #    portao 1i6 acusa (com razao) "risco pendurado". Medido
                   #    na folha: em x=492 a curva passa em y=911 e o texto so
                   #    comeca em y=924 — a caixa cabe entre os dois, em 918.
                   (352, 918, 500, 980),    # "Ventriculo direito"
                   (628, 920, 800, 984)],   # "Ventriculo esquerdo"
}

# (arquivo-fonte, código da folha, nome, caixa (x1,y1,x2,y2), o que é)
RECORTES = [
    # ---- DIGESTÓRIO: as seis fichas da d29 ----
    # ⚠️ AS CAIXAS ENTRAM ~25 px PARA DENTRO do tracejado. Na primeira tentativa
    #    eu recortei de tracejado a tracejado e as BOLINHAS PRETAS da linha de
    #    recorte da folha vieram junto, em cima e embaixo de cinco figuras.
    #    Isso é "sobra da folha" — o papel aparecendo na tela.
    (FOLHAS, "d29", "vd_intgrosso", (1512, 402, 1975, 888), u"intestino grosso"),
    (FOLHAS, "d29", "vd_intdelgado", (1512, 972, 1975, 1478), u"intestino delgado"),
    (FOLHAS, "d29", "vd_esofago", (1512, 1520, 1975, 2042), u"esôfago"),
    (FOLHAS, "d29", "vd_estomago", (1512, 2116, 1975, 2612), u"estômago"),
    (FOLHAS, "d29", "vd_figado", (1512, 2702, 1975, 3158), u"fígado"),
    (FOLHAS, "d29", "vd_pancreas", (1495, 3258, 1995, 3688), u"pâncreas"),
    (FOLHAS, "d29", "vd_corpodig", (352, 1818, 1442, 3712), u"o corpo com o digestório"),
    # ---- RESPIRATÓRIO ----
    # ⚠️ A FIGURA NÃO PODE ENTREGAR A RESPOSTA. A primeira versão saía da d25,
    #    que é o esquema ROTULADO ("Fossas nasais", "Laringe", "Traquéia"…) — e
    #    as folhas deste caderno pedem justamente que a criança ponha esses
    #    nomes. A figura daria o gabarito de graça, que é o defeito que a prova
    #    de Ed. Física me ensinou dois dias atrás. A **d13** tem o mesmo corpo
    #    com as caixas VAZIAS: é dela que sai.
    # ⚠️ E ESTA CAIXA JÁ ESTEVE ERRADA TAMBÉM, pelo mesmo motivo do coração: eu
    #    a apertei em x=652 para fugir das caixinhas de escrever da folha, e o
    #    MENINO SAIU PARTIDO AO MEIO — metade da cabeça de fora, com um corte
    #    reto no lugar do rosto. Aparecia assim na CAPA do caderno, que é a
    #    primeira coisa que a criança vê. Medido: o desenho vai de x=335 a
    #    x=835 (a caixinha ampliada dos alvéolos) e de y=583 a y=1409.
    (FOLHAS, "d13", "vd_corpores", (300, 572, 866, 1420), u"o corpo com o respiratório, sem nomes"),
    (FOLHAS, "d25", "vd_alveolos", (726, 1226, 1006, 1522), u"os alvéolos"),
    # ---- CIRCULATÓRIO ----
    # ⚠️ Só o DESENHO do coração: na primeira tentativa vieram os rótulos da
    #    folha ("Artéria pulmonar", "Átrio esquerdo"…) pela metade, cortados na
    #    borda. Além de feio, são termos da faixa FORA DO ANO do crivo.
    # ⚠️ E DEPOIS EU APERTEI DEMAIS e cortei o próprio coração — o desenho saía
    #    sem a ponta de baixo. A caixa certa é a que pega o órgão INTEIRO e
    #    aceita as linhas finas de chamada da folha: elas fazem parte do
    #    desenho de papel que a criança conhece; um órgão cortado, não.
    (CIRC, "d08", "vd_coracao", (268, 232, 860, 948), u"o coração"),
    (CIRC, "d26", "vd_integra", (524, 152, 1118, 770), u"pulmão ↔ coração ↔ corpo"),
    # ---- A GRADE DE COORDENADAS (folha 35) ----
    # ⚠️ AQUI A d44 VOLTA — e a volta tem explicação, porque lá em cima está
    #    escrito que ela ficou de fora. O que ficou de fora foram as OITO FICHAS
    #    dela recortadas UMA A UMA (86 × 86 px cada, coloridas, ao lado de um
    #    caderno todo a traço preto). O que entra aqui é OUTRA coisa: a GRADE
    #    INTEIRA, num pedaço só, com as letras A–E e os números 1–5 — que não é
    #    uma ilustração de órgão, é o TABULEIRO do exercício. Sem ele a folha 35
    #    pergunta "em qual quadrinho está o estômago?" para uma criança que não
    #    tem quadrinho nenhum na tela: pergunta sem resposta possível.
    #    Medida: 491 × 496 px no arquivo, mostrada com 440 px de largura (0,9×),
    #    dentro do teto de 1,35× do portão de resolução.
    (FOLHAS, "d44", "vd_grade", (36, 98, 527, 594), u"a grade A–E × 1–5 com os órgãos"),
]

# ⚠️ FIGURA QUE NÃO PERDE O FUNDO. O `limpa_fundo` existe para soltar o desenho
#    do papel; a grade é um TABULEIRO — o branco das casinhas é parte dela, e
#    apagá-lo deixaria as linhas soltas no ar.
SEM_FUNDO = set(["vd_grade"])



def acha(pasta, cod):
    for f in sorted(os.listdir(pasta)):
        if f.startswith(cod + "_"):
            return os.path.join(pasta, f)
    return None


def main():
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    origem = {}
    feitos = 0
    for pasta, cod, nome, caixa, oque in RECORTES:
        f = acha(pasta, cod)
        if not f:
            print(u"  ⛔ nao achei a folha %s em %s" % (cod, pasta))
            continue
        im = Image.open(f).convert("RGBA")
        if nome in APAGAR:
            branco = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            for cx in APAGAR[nome]:
                d.rectangle(list(cx), fill=(255, 255, 255, 255))
            del branco
        if caixa[2] > im.width or caixa[3] > im.height:
            print(u"  ⛔ %s: a caixa %s nao cabe em %sx%s" % (nome, caixa, im.width, im.height))
            continue
        c = im.crop(caixa)
        if nome not in SEM_FUNDO:
            c = limpa_fundo(c)
            c = tira_halo(c)
            c = aperta(c)
        if c is None or c.width < 20 or c.height < 20:
            print(u"  ⛔ %s: sobrou quase nada depois do recorte" % nome)
            continue
        c.save(os.path.join(DEST, nome + ".png"))
        # ⚠️ O VALOR É UMA STRING "folha:<cod> — <o que é>", e não um objeto:
        #    é assim que o portão 1i5 (`figura_da_folha.py`) lê a procedência.
        #    Com um dicionário aqui ele estoura com AttributeError, que é um
        #    "não medi" disfarçado de defeito do portão.
        origem[nome + ".png"] = u"folha:%s — %s (recorte da folha de papel; caixa %s)" % (
            cod, oque, ",".join(str(x) for x in caixa))
        feitos += 1
        print(u"  ok  %-16s %4d x %-4d  (%s, folha %s)" % (nome, c.width, c.height, oque, cod))

    # ⚠️ AS PEÇAS DO MOTOR (selo, selo_off, troféu) vêm do esqueleto e também
    #    precisam de linha aqui: o portão 1i5 confere disco e declaração nos
    #    DOIS sentidos. E nada de chave `_leia`: ele a leria como o nome de uma
    #    figura que não existe no disco.
    for peca, oque in ((u"vd_selo.png", u"o selo da folha pronta"),
                       (u"vd_selo_off.png", u"o selo da folha ainda aberta"),
                       (u"vd_trofeu.png", u"o troféu do fim")):
        if os.path.exists(os.path.join(DEST, peca)):
            origem[peca] = u"motor:esqueleto — %s (peca do _padrao/FOLHA-VIVA, nao e figura de conteudo)" % oque
    io.open(os.path.join(DEST, "ORIGEM.json"), "w", encoding="utf-8").write(
        json.dumps(origem, ensure_ascii=False, indent=2) + u"\n")
    print(u"\n  %d figura(s) recortada(s); procedencia em img/ORIGEM.json" % feitos)
    return 0 if feitos else 1


if __name__ == "__main__":
    sys.exit(main())
