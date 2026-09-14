# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 1i6 — "sobrou pauta da folha dentro da figura?"

 ⚠️ O DEFEITO, e quem o viu foi o MARCOS, não um portão (14/set/2026):
    *"a atividade do reino, tem resto de outras imagens nas imagens, e imagens
    que faltam partes, resolva por favor"*.

    As figuras dos cadernos de folha viva são RECORTADAS de folhas de papel de
    verdade (regra da origem: o gesto vem do comando impresso, a figura vem da
    MESMA folha). E a folha de papel não traz só o desenho: traz o quadradinho
    de marcar ao lado dele, a moldura tracejada de recortar, a linha que separa
    as colunas da tabela. Quando o recorte pega um pedaço dessa PAUTA, a criança
    vê um risco solto pendurado no passarinho — e ninguém mediu isso, porque
    todos os portões de imagem da casa olhavam outra coisa (o halo branco, a
    figura que não carrega, a duplicata, a origem declarada).

    Na estreia deste portão, rodado nas figuras do commit ANTERIOR dos cinco
    reinos, ele reprovou: arvore2 (44 riscos da moldura tracejada), reino_animal
    (11 riscos + a linha da coluna, de 87% da altura), milho, bola e nuvem.

 O QUE ELE MEDE (e os números saíram das 44 figuras dos cinco reinos, não de
 cabeça — cada limiar abaixo tem, do lado, o que caiu e o que ficou):

  1. RESTO DA PAUTA — pedaço solto de até 0,5% da tinta do corpo, encostado na
     beirada (até 3 px).
       · o que ISSO pega : riscos da moldura tracejada, de 0,13% a 0,19%
       · o que fica de pé: a antena da BORBOLETA (0,79%), a chama do FOGO
                           (1,19%), o raio do SOL2 (1,83%), as pedrinhas do
                           monte de PEDRAS2 (3,96% a 13,82%)
     A folga é de 2,6x para baixo e 1,6x para cima — não é fio de navalha.

  2. LINHA IMPRESSA — traço de até 4 px de espessura que atravessa 90% de um
     dos lados da figura.
       · o que ISSO pega : a divisória da tabela da coroa (2 px x 110 px, que é
                           a altura INTEIRA do recorte do reino_animal)
       · nenhum desenho das 44 tem traço assim: o mais fino que atravessa a
         figura toda é a haste da ROSA, com 9 px.

 ⚠️ O QUE ELE **NÃO** MEDE, e isto não é modéstia, é medida:

  a) QUADRADINHO FUNDIDO NO DESENHO. Quando o quadradinho de marcar ENCOSTA na
     figura, os dois viram um componente só e nada aqui os separa. Tentei duas
     assinaturas e as DUAS se confundem com figura limpa:
       · maior corrida vertical de pixel sem cor: passarinho SUJO deu 8 px, e o
         passarinho LIMPO dá 8 px também (a nuvem limpa dá 45);
       · coluna mais carregada de pixel sem cor: passarinho sujo 13%, limpo 13%
         (a casa limpa dá 69%).
     A defesa desse caso não é este portão: é o `apaga_quadradinhos` do
     recortador, que mata o quadradinho na FOLHA, onde ele ainda é um dos vinte
     quadrados iguais de uma grade — e a folha de contato, para OLHAR.

  b) FIGURA CORTADA ("imagens que faltam partes") — e esta é a metade DOLOROSA,
     porque foi metade da queixa do Marcos. Tentei duas assinaturas e medi as
     duas contra as figuras que estavam MESMO cortadas no commit anterior:
       · corrida reta de tinta na beirada: o URSO_PELUCIA cortado deu 23%; a
         ÁGUA, que é um retângulo INTEIRO, dá 100%;
       · tinta total na beirada (melhor das duas): o URSO_PELUCIA cortado deu
         67% — e o MENINO, inteiro, dá 67% também. A CASA inteira dá 90%.
     Não há corte que separe os dois grupos, então não há portão: figura de
     apoio reto (a água, o celular, a casa, o cachorro sentado) encosta na
     beirada por desenho, não por corte. Deixar isso como "aviso" seria pior que
     nada — uma lista em que a água e a casa aparecem toda vez é uma lista que a
     gente aprende a pular.
     A defesa desse caso é OLHAR a folha de contato que o recortador salva ao
     fim de cada corte, e é por isso que ele passou a salvá-la sempre.

 Exceção declarada: `<pasta>/img/SOBRA-OK.json` = {"rn_x.png": "por que fica"}.

 Uso:  python3 _qa/sobra_da_folha.py <pasta>
 Código 0 = limpo · 1 = REPROVADO · 2 = não se aplica / não deu para medir
============================================================
"""
from __future__ import print_function

import glob
import io
import json
import os
import sys

try:
    import numpy as np
    from PIL import Image
    from scipy import ndimage as nd
except Exception as e:                                   # pragma: no cover
    print(u"NAO MEDI: falta biblioteca (%s)" % e)
    sys.exit(2)

PARTE_SOLTA = 0.005        # 0,5% da tinta do corpo — ver o quadro de medidas acima
BEIRADA = 3                # px: "encostado na beirada"
# ⚠️ PALPITE DECLARADO — o piso do que a CRIANÇA ENXERGA. Não saiu de medida
#    nenhuma: é um juízo meu sobre visibilidade, e por isso está marcado assim e
#    sai impresso na tela do portão. A conta por trás: a figura tem ~190 px de
#    lado no arquivo e aparece com ~100 px na tela da criança, então um ponto de
#    2x2 px do arquivo vira menos de um pixel — não existe para ela. Acusar isso
#    seria transformar o portão em ruído, e portão que acusa inocente é portão
#    que a gente aprende a pular (lição já paga no `silaba_fonte.py`, que
#    reprovou 21 recortes legítimos). Quem quiser apertar, aperte — mas medindo.
VISIVEL = 3                # px: lado mínimo do pedaço para ele contar
LINHA_FINA = 4             # px de espessura máxima de uma linha impressa
LINHA_LONGA = 0.90         # fração do lado que ela atravessa


def corrida(v):
    u"""maior sequência contígua de True"""
    m = n = 0
    for x in v:
        n = n + 1 if x else 0
        if n > m:
            m = n
    return m


def olha(caminho):
    u"""Devolve (restos da pauta, linhas impressas) de uma figura."""
    im = Image.open(caminho).convert(u"RGBA")
    a = np.asarray(im)
    H, W = a.shape[0], a.shape[1]
    alfa = a[..., 3] > 24
    if not alfa.any():
        return [], []
    rot, n = nd.label(alfa, np.ones((3, 3), bool))
    pedacos = []
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        if sl is None:
            continue
        ys, xs = sl
        pedacos.append((int((rot[sl] == i).sum()), xs.stop - xs.start,
                        ys.stop - ys.start,
                        min(xs.start, ys.start, W - xs.stop, H - ys.stop)))
    corpo = max(p[0] for p in pedacos)
    restos, linhas = [], []
    for tam, w, h, borda in pedacos:
        if tam == corpo:
            continue
        if max(w, h) < VISIVEL:
            continue                      # pontinho de escaneamento: ver VISIVEL
        if tam <= corpo * PARTE_SOLTA and borda <= BEIRADA:
            restos.append((tam, 100.0 * tam / corpo, w, h))
        elif min(w, h) <= LINHA_FINA and (w >= W * LINHA_LONGA or h >= H * LINHA_LONGA):
            linhas.append((tam, w, h))
    return restos, linhas


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/sobra_da_folha.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    dimg = os.path.join(pasta, u"img")
    cam_org = os.path.join(dimg, u"ORIGEM.json")
    if not os.path.exists(cam_org):
        print(u"%s -> NAO SE APLICA: sem img/ORIGEM.json (nao e figura recortada "
              u"de folha de papel)." % pasta)
        return 2
    try:
        org = json.load(io.open(cam_org, encoding=u"utf-8"))
    except Exception as e:
        print(u"%s -> NAO MEDI: ORIGEM.json nao e JSON valido (%s)." % (pasta, e))
        return 2
    daspastas = [f for f, v in org.items() if str(v).startswith(u"folha:")]
    if not daspastas:
        print(u"%s -> NAO SE APLICA: nenhuma figura declarada como recortada de "
              u"folha de papel." % pasta)
        return 2

    perdao = {}
    cam_ok = os.path.join(dimg, u"SOBRA-OK.json")
    if os.path.exists(cam_ok):
        try:
            perdao = json.load(io.open(cam_ok, encoding=u"utf-8"))
        except Exception as e:
            print(u"%s -> NAO MEDI: SOBRA-OK.json nao e JSON valido (%s)." % (pasta, e))
            return 2

    reprova, perdoadas, vistas = [], [], 0
    for f in sorted(daspastas):
        p = os.path.join(dimg, f)
        if not os.path.exists(p):
            continue
        vistas += 1
        restos, linhas = olha(p)
        if not (restos or linhas):
            continue
        if f in perdao:
            perdoadas.append((f, perdao[f]))
            continue
        reprova.append((f, restos, linhas))

    print(u"%s -> sobra da folha: %d figura(s) recortada(s) de papel conferida(s)"
          % (pasta, vistas))
    print(u"   PALPITE DECLARADO: pedaco com menos de %d px de lado nao conta "
          u"(juizo meu sobre o que a crianca enxerga, nao medida)." % VISIVEL)
    if perdoadas:
        print(u"   %d perdoada(s) por SOBRA-OK.json (declaradas com motivo):" % len(perdoadas))
        for f, por in perdoadas:
            print(u"    - %-24s %s" % (f, por))
    if reprova:
        print(u"   %d FIGURA(S) COM PAUTA DA FOLHA DENTRO — a crianca ve um risco "
              u"solto pendurado no desenho:" % len(reprova))
        for f, restos, linhas in reprova:
            if restos:
                pior = max(restos, key=lambda z: z[0])
                print(u"    x %-24s %d resto(s) da pauta, o maior com %d px "
                      u"(%.2f%% do corpo, %dx%d)"
                      % (f, len(restos), pior[0], pior[1], pior[2], pior[3]))
            for tam, w, h in linhas:
                print(u"    x %-24s linha impressa de %dx%d px atravessando a figura"
                      % (f, w, h))
        print(u"   conserto: o recortador da atividade tem que apagar a pauta — ver")
        print(u"   `tira_linha_impressa` e `apaga_quadradinhos` em")
        print(u"   _reinos/recortar_das_folhas.py, que e o modelo da casa. Se algum")
        print(u"   pedaco for DESENHO mesmo, declare em img/SOBRA-OK.json com o motivo.")
        return 1

    print(u"   ok: nenhum resto de pauta e nenhuma linha impressa nas figuras")
    print(u"   ⚠️ DUAS COISAS ELE NAO VE, e nao adianta ler este 'ok' como se visse:")
    print(u"      · o quadradinho de marcar FUNDIDO no desenho (as duas assinaturas")
    print(u"        que medi se confundem com figura limpa: 8 px e 13% nas duas);")
    print(u"      · a figura CORTADA — o urso truncado deu 67% de tinta na beirada e o")
    print(u"        menino INTEIRO tambem da 67%. Nao ha corte que os separe.")
    print(u"      Para os dois, a defesa e OLHAR a folha de contato do recortador.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
