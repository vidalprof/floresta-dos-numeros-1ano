#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""CARTELA — várias peças numa folha só (1 chamada paga em vez de N).

Regra registrada no MANUAL-MESTRE §"REGRA FIXA": *"SEMPRE tentar gerar em
CARTELA (várias peças numa folha só)... Gerar em cartela = mesmo estilo,
proporção e luz para todas as peças (elas saem IRMÃS) e 1 chamada só. Nunca
gerar pose por pose separada"*. E a regra de custo: *"a atividade INTEIRA sai
por centavos — quase tudo no Pollinations grátis, e no máximo 1–2 cartelas
pagas"*.

Estava escrito e mesmo assim se perdeu: na cartografia saíram **45 imagens
geradas UMA A UMA** (~R$9,00) onde 5 cartelas + 3 edições do mascote (~R$1,60)
davam o mesmo — 82% do dinheiro pela janela, e ainda por cima com as peças
saindo cada uma de um jeito. Regra que só vive na memória de quem lê o manual
não é regra: é sorte. Por isso virou ferramenta.

  plano  — agrupa um lote de imagens em CARTELAS e escreve os prompts prontos
  cortar — recorta a folha que voltou, com os NOMES certos, e monta a folha
           de conferência para olhar antes de embutir. Espera fundo PRETO
           (é o que o prompt da cartela pede ao Gemini). Se a folha vier do
           ChatGPT, o fundo costuma ser CREME: aí o recorte é o de
           `_mapa/cortar_props.py`, que trata sombra e tarja do celular.

USO
  python3 _padrao/cartela.py plano  _gerar_imagens.json
  python3 _padrao/cartela.py cortar _novo/cart_simbolos.png \\
          mp_sim_igreja,mp_sim_escola,... --dest _mapa/img

⚠️ O QUE **NÃO** VAI EM CARTELA (aprendido caro):
  • as camadas do MASCOTE (falar/piscar) — têm que ser EDIÇÃO da pose parada,
    senão o boneco treme (ver `_qa/mascote.py`);
  • as CENAS largas (fundo, voo, escala) — não precisam de recorte, então vão
    no Pollinations, que é de graça.
"""
import io
import json
import re
import os
import sys

# quantas peças cabem numa folha sem a IA embolar (medido: acima disso ela
# começa a fundir os objetos e a errar a contagem)
MAX_POR_CARTELA = 8

ESTILO = (u"Soft matte clay 3D illustration, children's storybook style, "
          u"rich saturated colours, soft shadows.")
MOLDE = (u"A SHEET of %(n)d separate objects arranged in a clean %(l)dx%(c)d GRID "
         u"on a PLAIN PURE BLACK background (#000000), each object fully inside its "
         u"own cell, well separated from the others, none touching, all at the SAME "
         u"scale and the SAME lighting. %(estilo)s No text, no letters, no numbers, "
         u"no labels, no frames, no background scenery. The objects, in reading "
         u"order (left to right, top to bottom), are:\n%(itens)s")


def e_cena(x):
    u"""CENA larga: vai inteira e no Pollinations (de graca) — fora da cartela.

    ⚠️ a primeira versao disto perguntava se o prompt tinha "room" para decidir
    se era um comodo — e "classROOM board" (a lousa) casou. Peca virou cena e a
    conta saiu errada. Regra que decide dinheiro nao pode adivinhar: aqui olha
    so o ENQUADRAMENTO que o proprio prompt pediu.
    """
    p = (x.get("prompt") or "").lower()
    nome = x.get("nome", "")
    return ("wide image" in p or "wide horizontal" in p
            or nome.endswith(("_fundo", "_cena"))
            or x.get("modelo") == "pollinations")


def e_edicao(x):
    u"""camada do mascote: TEM que ser edicao da pose parada, senao ele treme."""
    return bool(x.get("base")) or x.get("nome", "").endswith(("_fala", "_pisca"))


def grade(n):
    u"""linhas x colunas mais quadrada possível para n peças."""
    c = 1
    while c * c < n:
        c += 1
    l = (n + c - 1) // c
    return l, c


def prompt_da_cartela(itens):
    l, c = grade(len(itens))
    lista = u"\n".join(u"  %d. %s" % (i + 1, it["desc"]) for i, it in enumerate(itens))
    return MOLDE % {"n": len(itens), "l": l, "c": c, "estilo": ESTILO, "itens": lista}


def plano(caminho):
    lote = json.load(io.open(caminho, encoding="utf-8"))
    # separa o que precisa de RECORTE (vai em cartela, no pago) do que é CENA
    # larga (vai inteiro, no Pollinations de graça).
    cenas = [x for x in lote if e_cena(x)]
    edicoes = [x for x in lote if not e_cena(x) and e_edicao(x)]
    recorta = [x for x in lote if not e_cena(x) and not e_edicao(x)]

    # ⚠️ AGRUPAR POR TEMA, nao pela ordem em que eu escrevi o lote. A cartela
    #    promete que as pecas saem IRMAS — "mesma escala, mesma luz". Juntar
    #    numa folha so a arara, seis retratos de crianca e uma mandioca pede
    #    justamente o contrario: a IA obedece o "mesma escala" e devolve a
    #    mandioca do tamanho da arara. Cada folha e UMA familia de coisas.
    #    O campo "grupo" do lote manda; sem ele, cai na ordem de escrita.
    ordem, familias = [], {}
    for x in recorta:
        g = x.get("grupo", "_solto")
        if g not in familias:
            familias[g] = []; ordem.append(g)
        # ⚠️ LICAO PAGA (ago/2026): o embrulho da cartela manda "PLAIN PURE BLACK
        #    background" (e o preto que vira transparencia no recorte), mas o
        #    prompt de CADA peca costuma trazer "plain flat WHITE background" —
        #    porque sozinha ela seria gerada em branco. As duas ordens iam na
        #    mesma folha, contradizendo uma a outra. A cartela dos crachas
        #    simplesmente NAO voltou, e eu perdi uma rodada inteira por isso.
        #    Aqui a instrucao de fundo da peca e removida: quem manda no fundo
        #    da folha e a folha.
        _d = (x.get("prompt") or "").strip()
        _d = re.sub(r",?\s*(plain (flat )?|pure |solid )?"
                    r"(white|black|transparent|plain)\s+back(ground|drop)[^,.]*", "", _d, flags=re.I)
        _d = re.sub(r"\s{2,}", " ", _d).replace(" ,", ",").strip()
        familias[g].append({"nome": x["nome"], "desc": _d})

    grupos, nomes = [], []
    for g in ordem:
        itens = familias[g]
        for i in range(0, len(itens), MAX_POR_CARTELA):
            grupos.append(itens[i:i + MAX_POR_CARTELA])
            nomes.append(g if len(itens) <= MAX_POR_CARTELA
                         else "%s%d" % (g, i // MAX_POR_CARTELA + 1))

    saida = []
    for i, g in enumerate(grupos):
        saida.append({"nome": "cart_%s" % nomes[i],
                      "pecas": [it["nome"] for it in g],
                      "prompt": prompt_da_cartela(g)})
    json.dump(saida, io.open("_lote_cartelas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(u"%s -> %d imagens" % (caminho, len(lote)))
    print(u"   %d precisam de recorte  ->  %d CARTELA(S) paga(s)"
          % (len(recorta), len(grupos)))
    print(u"   %d sao cenas largas     ->  Pollinations (de graca)" % len(cenas))
    if edicoes:
        print(u"   %d edicao(oes) do mascote -> uma a uma MESMO (senao ele treme)"
              % len(edicoes))
    print(u"   economia: %d chamadas pagas viram %d  (%.0f%% a menos)"
          % (len(recorta), len(grupos),
             100.0 * (len(recorta) - len(grupos)) / max(1, len(recorta))))
    print(u"   prompts escritos em _lote_cartelas.json")
    for c in saida:
        print(u"     %s: %s" % (c["nome"], ", ".join(c["pecas"])))
    return 0


def cortar(folha, nomes, dest, larg=520):
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    nomes = [n.strip() for n in nomes.split(",") if n.strip()]
    im = Image.open(folha).convert("RGB")
    arr = np.asarray(im)
    H, W = arr.shape[:2]
    # ⚠️ FUNDO PRETO ENGOLE O QUE É ESCURO. Um limiar só (>34) achava o
    #    objeto mas comia o CABELO PRETO e a sombra da roupa: os avatares da
    #    Terra dos Papagaios saíram com buracos vazados no cabelo e no ombro,
    #    e `fill_holes` não salva — o buraco encosta na borda da figura, então
    #    não é buraco "fechado". A cura é limiar DUPLO (histerese): o forte
    #    (>34) diz onde o objeto está; o fraco (>10) só é aceito se estiver
    #    GRUDADO no forte. Assim o cabelo entra e o chuvisco do JPEG no fundo,
    #    que é solto, fica de fora.
    forte = arr.max(axis=2) > 34
    fraco = arr.max(axis=2) > 10
    lf, nf = ndimage.label(fraco)
    vivos = set(np.unique(lf[forte])); vivos.discard(0)
    mask = np.isin(lf, list(vivos))
    mask = ndimage.binary_closing(mask, np.ones((3, 3)), iterations=2)
    lab, n = ndimage.label(mask)
    areas = ndimage.sum(np.ones_like(lab), lab, index=range(1, n + 1))
    minA = 0.004 * H * W
    comps = sorted([(i + 1, areas[i]) for i in range(n) if areas[i] >= minA],
                   key=lambda t: -t[1])[:len(nomes)]
    if len(comps) != len(nomes):
        print(u"!! a folha tem %d peca(s) e voce nomeou %d — NAO vou cortar no escuro."
              % (len(comps), len(nomes)))
        print(u"   confira a cartela: pecas coladas contam como uma so.")
        return 1

    # ordem de leitura: agrupa por linha (tolerancia 8% da altura), depois x
    info = []
    for cid, _ in comps:
        ys, xs = np.where(lab == cid)
        info.append((cid, ys.mean(), xs.mean(), ys.min(), ys.max(), xs.min(), xs.max()))
    info.sort(key=lambda t: t[1])
    linhas, tol = [], 0.08 * H
    for it in info:
        if linhas and abs(it[1] - linhas[-1][0]) < tol:
            linhas[-1][1].append(it)
        else:
            linhas.append([it[1], [it]])
    ordem = []
    for _, row in linhas:
        row.sort(key=lambda t: t[2])
        ordem += row

    if not os.path.isdir(dest):
        os.makedirs(dest)
    feitos = []
    for nome, (cid, cy, cx, y0, y1, x0, x1) in zip(nomes, ordem):
        m = ndimage.binary_fill_holes(lab == cid)
        pad = int(0.08 * max(y1 - y0, x1 - x0))
        yy0 = max(0, y0 - pad); yy1 = min(H, y1 + pad + 1)
        xx0 = max(0, x0 - pad); xx1 = min(W, x1 + pad + 1)
        a = (m[yy0:yy1, xx0:xx1] * 255).astype(np.uint8)
        # erode 1px + suaviza: tira o anel escuro do antialias contra o preto
        a = ndimage.grey_erosion(a, size=(2, 2))
        a = ndimage.gaussian_filter(a.astype(np.float32), 0.6).astype(np.uint8)
        out = Image.fromarray(np.dstack([arr[yy0:yy1, xx0:xx1], a]), "RGBA")
        if out.width > larg:
            out = out.resize((larg, int(out.height * float(larg) / out.width)),
                             Image.LANCZOS)
        cam = os.path.join(dest, nome + ".png")
        out.save(cam, optimize=True)
        feitos.append(cam)
        # buraco vazado no meio da figura: mede o quanto do INTERIOR ficou
        # transparente. Uma peca sadia fica perto de 0%.
        al = np.asarray(out)[:, :, 3]
        cheio = ndimage.binary_fill_holes(al > 40)
        vazio = float((cheio & (al <= 40)).sum()) / max(1, cheio.sum())
        if vazio > 0.01:
            print(u"     !! %.1f%% do interior de %s ficou VAZADO — olhe a folha "
                  u"de conferencia antes de embutir" % (100 * vazio, nome))
        print(u"  %-18s %dx%d  %d KB" % (nome, out.width, out.height,
                                         os.path.getsize(cam) // 1024))

    # folha de conferencia: xadrez atras, para eu OLHAR antes de embutir
    cel = 240
    cols = 4
    linhasM = (len(feitos) + cols - 1) // cols
    mos = Image.new("RGB", (cols * cel, linhasM * cel), (255, 255, 255))
    for y in range(0, linhasM * cel, 20):
        for x in range(0, cols * cel, 20):
            if (x // 20 + y // 20) % 2:
                mos.paste((205, 215, 225), (x, y, x + 20, y + 20))
    for i, cam in enumerate(feitos):
        p = Image.open(cam).convert("RGBA")
        p.thumbnail((cel - 16, cel - 16))
        mos.paste(p, ((i % cols) * cel + 8, (i // cols) * cel + 8), p)
    conf = os.path.join(dest, "_conferencia.png")
    mos.save(conf)
    print(u"  folha de conferencia: %s  (OLHAR antes de embutir)" % conf)
    return 0


#  ⭐ CARTELA DE CENAS (ago/2026) — a exceção que virou regra
#
#  O cabeçalho aqui em cima dizia: "cena larga não vai em cartela, vai no
#  Pollinations, que é de graça". Estava certo enquanto o Pollinations dava
#  conta. Só que ele NÃO dá: pedimos barro e ele devolveu foto; pedimos uma
#  caravela e veio desenho de aplicativo de bebê. As cenas da Terra dos
#  Papagaios ficaram com QUATRO estilos brigando na mesma atividade.
#
#  Cena boa, então, é paga — e aí a cartela volta a valer, com uma diferença:
#  cena não se recorta por silhueta, se recorta por GEOMETRIA. Duas cenas
#  largas EMPILHADAS numa folha 1024x1024 dão 1024x512 cada uma: metade do
#  preço e, de quebra, mais nitidez do que as nossas cenas de 820px de hoje.
#  Quatro numa grade 2x2 dão 512x512 — que serve para figura de moldura
#  pequena (a série da escala), onde o que importa mais é serem IRMÃS.
#
#  ⚠️ O QUE CONTINUA FORA: as camadas do mascote (têm que ser EDIÇÃO da pose
#     parada, senão ele treme) e qualquer cena que precise de 1024 de LARGURA
#     inteira (aí é uma folha só para ela).
MOLDE_CENAS = (
    u"ONE image divided into a clean %(l)dx%(c)d GRID of %(n)d SEPARATE "
    u"illustrations, like a page of a picture book. Each cell is a complete "
    u"scene that fills its own cell edge to edge, with a thin gap between "
    u"cells. ALL %(n)d scenes share the SAME art style, the SAME lighting and "
    u"the SAME colour palette. %(estilo)s No text, no letters, no numbers, no "
    u"labels, no captions. The scenes, in reading order (left to right, top to "
    u"bottom), are:\n%(itens)s")


def prompt_cenas(itens):
    u"""o prompt de uma cartela de CENAS (recorte por geometria)."""
    l, c = grade(len(itens))
    return MOLDE_CENAS % {"n": len(itens), "l": l, "c": c, "estilo": ESTILO,
                          "itens": "\n".join(u"%d. %s" % (i + 1, t)
                                             for i, t in enumerate(itens))}


def cortar_grade(folha, nomes, dest, linhas, colunas, borda=0.018, larg=None):
    u"""recorta a folha de CENAS pela grade, na ordem de leitura.

    `borda` tira a moldurinha/gap que a IA deixa entre as celulas — sem isso
    sobra um filete escuro na beirada de cada cena, e ele aparece como uma
    listra na tela da crianca.
    """
    from PIL import Image
    nomes = [n.strip() for n in nomes.split(",") if n.strip()]
    if len(nomes) != linhas * colunas:
        print(u"!! a grade e %dx%d (%d celulas) e voce nomeou %d — NAO vou cortar "
              u"no escuro." % (linhas, colunas, linhas * colunas, len(nomes)))
        return 1
    im = Image.open(folha).convert("RGB")
    W, H = im.size
    cw, ch = W / float(colunas), H / float(linhas)
    mx, my = cw * borda, ch * borda
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for i, nome in enumerate(nomes):
        x, y = (i % colunas) * cw, (i // colunas) * ch
        p = im.crop((int(x + mx), int(y + my), int(x + cw - mx), int(y + ch - my)))
        if larg and p.width != larg:
            p = p.resize((larg, int(p.height * larg / float(p.width))), Image.LANCZOS)
        cam = os.path.join(dest, nome + ".jpg")
        p.save(cam, quality=84, optimize=True, progressive=True)
        print(u"  -> %-16s %dx%d  %d KB" % (nome, p.width, p.height,
                                            os.path.getsize(cam) // 1024))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "plano":
        sys.exit(plano(sys.argv[2]))
    if sys.argv[1] == "cortar":
        dest = "_novo/rec"
        if "--dest" in sys.argv:
            dest = sys.argv[sys.argv.index("--dest") + 1]
        sys.exit(cortar(sys.argv[2], sys.argv[3], dest))
    if sys.argv[1] == "cortar-cenas":
        # cortar-cenas <folha> <nomes> --grade LxC [--dest pasta] [--larg N]
        dest, g, larg = "_novo/rec", "2x1", None
        if "--dest" in sys.argv: dest = sys.argv[sys.argv.index("--dest") + 1]
        if "--grade" in sys.argv: g = sys.argv[sys.argv.index("--grade") + 1]
        if "--larg" in sys.argv: larg = int(sys.argv[sys.argv.index("--larg") + 1])
        l, c = [int(x) for x in g.lower().split("x")]
        sys.exit(cortar_grade(sys.argv[2], sys.argv[3], dest, l, c, larg=larg))
    print(__doc__)
    sys.exit(2)
