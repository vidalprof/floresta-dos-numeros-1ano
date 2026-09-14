# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DO ARMAZÉM SAEM DAS FOLHAS DE PAPEL — e não do banco

 ⚠️ O QUE ESTAVA ERRADO. O caderno foi montado com 19 figuras vindas do BANCO
    DE IMAGENS, e o portão **1i5** reprova por isso, com razão:

      "ha colheita em _sequencias/folhas_mult e NENHUMA das 20 figuras foi
       recortada dela"

    A regra da casa (CLAUDE.md) é que a figura venha da MESMA folha de onde veio
    o gesto, *"para a criança reconhecer a atividade que a professora dá no
    papel"*. No `_mult3` eu cumpri metade: os 25 gestos saíram do comando
    impresso das folhas, as figuras não. O crivo (`POTE-MULT.md`) nem fala em
    figura — foi por essa fresta que a regra escapou.

 ⚠️ ISTO AQUI É DIFERENTE DO RECORTE DOS CINCO REINOS, e a diferença importa.
    Lá, cada caixa da folha tinha UMA figura e eu queria todas. Aqui a folha
    desenha o MESMO objeto repetido (é folha de multiplicação: cinco sóis, seis
    bolas, dez vasos), e eu quero **um exemplar**. Então a regra é: dentro da
    faixa declarada, fico com a **maior ilha de tinta colorida** — um objeto
    inteiro, não um pedaço nem o grupo todo.

 ⚠️ AS FAIXAS FORAM MEDIDAS, NÃO ESTIMADAS NO OLHO. Rodei o perfil de tinta
    COLORIDA por linha em cada folha (o texto preto não conta, senão o enunciado
    entra junto) e li as bandas que o próprio papel forma. O que continua sendo
    julgamento meu é o recorte lateral (x), e é por isso que existe o `--ver`:
    ele desenha a ilha escolhida por cima da folha, para eu OLHAR antes de
    aceitar. Foi conferir em miniatura que me custou os cinco reinos.

 As ferramentas de limpeza vêm de `_padrao/recorte_folha.py` — as mesmas que
 passaram pela banca dos reinos, sem reescrever nenhuma.

 Uso:  python3 _mult3/recortar_das_folhas.py [--ver d11]
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
sys.path.insert(0, os.path.join(RAIZ, u"_padrao"))
from recorte_folha import (LIM, limpa_fundo, tira_halo, aperta,          # noqa: E402
                           tira_linha_impressa)

FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_mult")
SAIDA = os.path.join(AQUI, u"img")
PREFIXO = u"mu_"

# ============================================================
#  OS 19 OBJETOS, e de qual folha cada um sai.
#  faixa = (y0, y1, x0, x1) em FRAÇÃO da folha.
#  O y saiu do perfil de tinta colorida (medido); o x é o recorte lateral, que
#  é julgamento meu e por isso passa pelo `--ver`.
# ============================================================
CAIXAS = [
    # --- d11 "Responda fazendo multiplicação": cinco linhas, uma por bicho.
    #     As cinco bandas de tinta colorida bateram com as cinco perguntas.
    (u"passarinho", u"d11", (0.190, 0.287, 0.03, 0.40)),
    (u"borboleta",  u"d11", (0.332, 0.449, 0.03, 0.40)),
    (u"sorvete",    u"d11", (0.490, 0.607, 0.03, 0.40)),
    (u"abelha",     u"d11", (0.651, 0.781, 0.03, 0.40)),
    (u"sol",        u"d11", (0.828, 0.947, 0.03, 0.40)),

    # --- d15 "Escreva a adição e a multiplicação": bola de basquete (exemplo),
    #     apontador e patinho. ⚠️ o x corta o COPO DE LÁPIS decorativo da margem
    #     esquerda, que é enfeite da folha e não objeto de contar.
    (u"bola",       u"d15", (0.210, 0.290, 0.20, 0.60)),
    (u"apontador",  u"d15", (0.386, 0.478, 0.13, 0.60)),
    (u"pato",       u"d15", (0.615, 0.720, 0.25, 0.80)),

    # --- d30 "Represente as adições por meio de uma multiplicação".
    #     ⚠️ a banda 0.036-0.074 é o LOGO do site e fica de fora de propósito.
    (u"buque",      u"d30", (0.230, 0.374, 0.05, 0.50)),
    (u"joaninha",   u"d30", (0.400, 0.520, 0.05, 0.50)),
    (u"vaso",       u"d30", (0.554, 0.675, 0.05, 0.50)),

    # --- d38 "Cada bandeja tem 6 brigadeiros" / "em cada fila há 9 cadeiras".
    (u"bandeja",    u"d38", (0.155, 0.250, 0.20, 0.60)),
    (u"cadeira",    u"d38", (0.508, 0.580, 0.10, 0.70)),

    # --- d05 grupos de objetos de escola e de casa.
    (u"cola",       u"d05", (0.132, 0.297, 0.13, 0.45)),
    (u"coracao",    u"d05", (0.340, 0.520, 0.13, 0.45)),
    (u"banana",     u"d05", (0.540, 0.643, 0.13, 0.70)),
    (u"laco",       u"d05", (0.690, 0.860, 0.30, 0.50)),

    # --- d21 "Adição de parcelas iguais" (pinguins do exemplo) e os 10 vasos.
    (u"pinguim",    u"d21", (0.212, 0.290, 0.04, 0.45)),
    (u"roseira",    u"d21", (0.458, 0.560, 0.05, 0.95)),
]


def acha(cod):
    a = sorted(glob.glob(os.path.join(FOLHAS, cod + u"_*")))
    return a[0] if a else None


def maior_ilha(cam, faixa, cola=6, piso=0.0006):
    u"""A MAIOR ilha de tinta COLORIDA dentro da faixa — um exemplar do objeto.

    ⚠️ POR QUE TINTA COLORIDA E NÃO TINTA ESCURA: a folha de multiplicação é
       cheia de texto preto (o enunciado, os tracinhos da resposta, a moldura da
       caixa). Medindo só o que tem COR, o desenho aparece sozinho — foi assim
       que as cinco bandas da d11 saíram batendo com as cinco perguntas dela.

    ⚠️ E POR QUE A MAIOR E NÃO TODAS: a folha repete o mesmo objeto muitas vezes
       (é disso que a multiplicação trata). Eu quero UM. A maior ilha é um objeto
       inteiro; ilhas menores dentro da mesma faixa são o mesmo objeto cortado
       pela beirada da faixa, ou um vizinho encostado."""
    im = Image.open(cam).convert(u"RGB")
    a = np.asarray(im).astype(np.int16)
    H, W = a.shape[0], a.shape[1]
    mx, mn = a[..., :3].max(axis=2), a[..., :3].min(axis=2)
    tinta = (mx < LIM) & ((mx - mn) > 40)
    y0, y1 = int(faixa[0] * H), int(faixa[1] * H)
    x0, x1 = int(faixa[2] * W), int(faixa[3] * W)
    m = np.zeros_like(tinta)
    m[y0:y1, x0:x1] = tinta[y0:y1, x0:x1]
    rot, n = nd.label(nd.binary_dilation(m, np.ones((cola, cola), bool)))
    melhor, cx = 0, None
    for i, sl in enumerate(nd.find_objects(rot), start=1):
        if sl is None:
            continue
        dentro = (rot[sl] == i) & m[sl]
        q = int(dentro.sum())
        if q < piso * H * W or q <= melhor:
            continue
        yy, xx = np.where(dentro)
        melhor = q
        cx = (sl[0].start + yy.min(), sl[0].start + yy.max(),
              sl[1].start + xx.min(), sl[1].start + xx.max())
    return cx, im, melhor


def recorta(im, caixa, nome):
    y0, y1, x0, x1 = caixa
    folga = 3
    c = im.crop((max(0, x0 - folga), max(0, y0 - folga), x1 + folga, y1 + folga))
    c = limpa_fundo(c.convert(u"RGBA"))
    c = aperta(tira_halo(aperta(c)))
    for _ in range(4):                       # ver a lição no `recorte_folha.py`
        antes = c.size
        c = aperta(tira_linha_impressa(c))
        if c.size == antes:
            break
    if c.width < 14 or c.height < 14:
        return None
    c.save(os.path.join(SAIDA, PREFIXO + nome + u".png"), optimize=True)
    return c


def contato():
    u"""A folha de contato, SEMPRE e a 300 px. Ver a lição nos cinco reinos:
    conferir em miniatura não é conferir."""
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
        g = ims[k:k + lote]
        linhas = (len(g) + cols - 1) // cols
        f = Image.new(u"RGBA", (cols * th, linhas * (th + 20)), (120, 170, 230, 255))
        d = ImageDraw.Draw(f)
        for i, cam in enumerate(g):
            im = Image.open(cam).convert(u"RGBA")
            im.thumbnail((th - 16, th - 16))
            f.alpha_composite(im, ((i % cols) * th + (th - im.width) // 2,
                                   (i // cols) * (th + 20) + 8))
            d.text(((i % cols) * th + 5, (i // cols) * (th + 20) + th),
                   os.path.basename(cam)[len(PREFIXO):-4][:22], font=ft, fill=(0, 0, 0, 255))
        nome = (u"mult-figuras.png" if k == 0
                else u"mult-figuras-%d.png" % (k // lote + 1))
        f.convert(u"RGB").save(os.path.join(dest, nome), optimize=True)
        saidas.append(u"_sequencias/crivo/" + nome)
    print(u"   contato-folha (300 px por tela, ABRIR e OLHAR):")
    for s in saidas:
        print(u"     %s" % s)


def main():
    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)

    if u"--ver" in sys.argv:
        alvo = sys.argv[sys.argv.index(u"--ver") + 1]
        cam = acha(alvo)
        if not cam:
            print(u"nao achei a folha %s" % alvo)
            return 2
        v = Image.open(cam).convert(u"RGB")
        d = ImageDraw.Draw(v)
        W, H = v.size
        for nome, cod, fx in CAIXAS:
            if cod != alvo:
                continue
            d.rectangle([int(fx[2] * W), int(fx[0] * H),
                         int(fx[3] * W), int(fx[1] * H)], outline=u"#0066ff", width=3)
            cx, _, q = maior_ilha(cam, fx)
            if cx:
                d.rectangle([cx[2], cx[0], cx[3], cx[1]], outline=u"#ff0000", width=4)
                d.text((cx[2] + 4, cx[0] + 4), nome, fill=u"#ff0000")
            print(u"   %-11s ilha de %s px" % (nome, q if cx else u"NENHUMA"))
        v.thumbnail((900, 1300))
        v.save(u"/tmp/ver_%s.png" % alvo)
        print(u"%s -> /tmp/ver_%s.png" % (alvo, alvo))
        return 0

    origem, feitos, problemas = {}, 0, []
    for nome, cod, fx in CAIXAS:
        cam = acha(cod)
        if not cam:
            problemas.append(u"%s: nao achei a folha %s" % (nome, cod))
            continue
        cx, im, q = maior_ilha(cam, fx)
        if not cx:
            # ⚠️ PARA, nao inventa. Faixa que nao devolve ilha e faixa errada, e
            #    recortar no escuro foi o que produziu o defeito que o Marcos viu.
            problemas.append(u"%s (%s): a faixa nao tem ilha de tinta colorida — "
                             u"rode com --ver %s para olhar." % (nome, cod, cod))
            continue
        if recorta(im, cx, nome) is None:
            problemas.append(u"%s (%s): a ilha saiu vazia depois de limpar o fundo"
                             % (nome, cod))
            continue
        origem[PREFIXO + nome + u".png"] = u"folha:%s" % cod
        feitos += 1

    for selo in (u"trofeu", u"estrela", u"estrela_off"):
        if os.path.exists(os.path.join(SAIDA, PREFIXO + selo + u".png")):
            origem[PREFIXO + selo + u".png"] = u"selo:casa"

    cam_org = os.path.join(SAIDA, u"ORIGEM.json")
    antes = {}
    if os.path.exists(cam_org):
        antes = json.load(io.open(cam_org, encoding=u"utf-8"))
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
    contato()
    return 1 if problemas else 0


if __name__ == u"__main__":
    sys.exit(main())
