# -*- coding: utf-8 -*-
u"""
============================================================
 AS MÃOS SAEM DA FOLHA DE PAPEL — Contando nos Dedinhos (1º ano)

 ⭐ A ORDEM DO MARCOS (19/set/2026), e ela REVOGA a decisão anterior deste
    caderno: *"para a atividade de contar nos dedinhos, [quero] essas imagens
    das mãos, dos dedos na internet, pois na atividade está feio"*.

    O que havia antes: a mão era DESENHADA EM CÓDIGO (`maoSVG`), retângulos
    arredondados de SVG. Passava em todo portão — e era feia ao lado do Sr.
    Batata, que é arte de verdade. O `PROMPTS-MAOS.md` guardava o plano antigo
    (8/set): gerar as mãos por IA, com ele aprovando. Esse plano está
    CANCELADO por esta ordem; o arquivo fica como registro do caminho que não
    seguimos.

 ⚠️ E O NÚMERO DE DEDOS É O CONTEÚDO. Numa atividade de contar, a figura de "3"
    com quatro dedos não é um defeito de arte: é a atividade ENSINANDO ERRADO.
    Por isso cada caixa abaixo foi CONFERIDA OLHANDO a folha ampliada, uma a
    uma, antes de virar código — e a folha de contato existe para que a próxima
    sessão confira de novo em dez segundos.

 De onde vem, e por que é justamente esta folha entre as quarenta colhidas:

   · d11 (980×980) — seis mãos numa grade 3×2: **punho, 1, 2, 3, 4 e 5**. É a
     ÚNICA da colheita que traz a série inteira, inclusive o ZERO (o punho
     fechado), com a MESMA mão, o mesmo traço e sem marca d'água. Isso importa
     mais do que parece: as seis se alternam na mesma caixa da tela quando a
     criança levanta e abaixa os dedos — se cada número viesse de uma folha
     diferente, a mão trocaria de dono a cada toque.

   · E a ORDEM em que ela levanta bate com a do código (`upDe`): indicador →
     médio → anelar → mínimo → polegar. Não foi arranjo meu; a folha foi
     desenhada assim, que é como a criança pequena conta.

 ⛔ AS QUE FICARAM DE FORA, e o motivo de cada uma — para ninguém refazer a
    escolha do zero daqui a um mês:
      · d12, d05, d16 — a mesma família, porém com a marca d'água da dreamstime
        atravessada; d40, com a da alamy. Marca d'água de banco de imagens não
        entra em folha de criança.
      · d14, d08, d22, d19, d20 — bonitas e limpas, mas começam no 1: não têm
        o punho, e sem o zero a peça "quantos faltam" não fecha.
      · d13, d21, d23, d29 — traço preto sem cor; ficariam pálidas ao lado do
        Sr. Batata.
      · d28, d30, d31, d34 — são folhas de TAREFA inteiras (com pauta, moldura
        e enunciado impresso); as mãos delas são pequenas dentro da página.

 🎨 OS TRÊS TONS DE PELE: a folha traz um tom só, e o caderno variava a pele a
    cada folha. Em vez de perder isso, os dois tons mais escuros saem por
    RECOLORAÇÃO da própria figura — não é desenho novo, é a mesma mão com o
    preenchimento da pele trocado, que neste traço achatado é um campo de cor
    chapada. O contorno preto, as unhas brancas e as linhas da palma não se
    tocam (a máscara só pega o que é pele). Confira na folha de contato: as
    três fileiras têm que ser a MESMA mão.

 Uso:  python3 _dedos/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError as e:                                   # pragma: no cover
    print(u"preciso de Pillow e numpy (%s)" % e)
    sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, u"_padrao"))
from recorte_folha import limpa_fundo, tira_halo, aperta       # noqa: E402

FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_maos")
DEST = os.path.join(AQUI, u"img")
PREFIXO = u"dd_"
MAIOR = 420                       # a maior mão na tela tem 190 px (.maos2)

D11 = u"d11_9e2fa2.jpg"

# nome, folha, x1, y1, x2, y2   — a grade 3×2 da d11, na ordem de contar
PECAS = [
    (u"mao0", D11,  47, 176, 243, 425),
    (u"mao1", D11, 355,  80, 551, 425),
    (u"mao2", D11, 706,  62, 914, 425),
    (u"mao3", D11,  33, 555, 254, 918),
    (u"mao4", D11, 339, 560, 601, 918),
    (u"mao5", D11, 618, 560, 964, 918),
]

DE_ONDE = {
    D11: u"d11 — seis mãos contando de zero a cinco (punho, 1, 2, 3, 4, 5)",
}

# ⚠️ QUANTOS DEDOS CADA UMA TEM — a conferência que a atividade não pode errar.
#    Conferido OLHANDO a d11 ampliada em 19/set/2026. Está aqui em código para
#    que o portão `_qa/dedos_contam.py` possa cobrar a cada rodada.
DEDOS_ESPERADOS = {u"mao0": 0, u"mao1": 1, u"mao2": 2,
                   u"mao3": 3, u"mao4": 4, u"mao5": 5}

# ---------------------------------------------------------------------------
# OS TONS DE PELE
#
# ⚠️ PALPITE DECLARADO: o tom da folha é medido (é a cor mais frequente dentro
#    da máscara de pele, impressa a cada rodada), mas os DOIS destinos são
#    escolha minha de paleta — os mesmos dois que o caderno já usava no vetor,
#    `#c68642` e `#8d5524`, que vêm da escala Fitzpatrick usada no projeto
#    desde o primeiro mascote. Não há medição por trás deles.
TONS = [
    (u"a", None),                 # o tom da própria folha, intocado
    (u"b", (0xC6, 0x86, 0x42)),
    (u"c", (0x8D, 0x55, 0x24)),
]


def mascara_pele(a):
    u"""Onde é PELE nesta figura: nem contorno preto, nem unha/papel branco.

    A conta, e por que ela não precisa de fio de navalha aqui: o traço é chapado
    e só tem quatro famílias de cor — preto do contorno (escuro), branco do papel
    e das unhas (claro e sem cor), o bege da pele e o bege um tom abaixo das
    dobras. Pele = pixel com alguma cor (max-min acima de 25), com o vermelho na
    frente do azul, e longe das duas pontas. Entre a dobra mais escura da folha
    e o contorno preto sobra um vão largo, então o corte de 60 não encosta em
    nenhum dos dois.
    """
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    return (mx - mn > 25) & (r > b) & (mx > 60) & (mn < 250)


def pinta(c, alvo):
    u"""Troca o tom da pele mantendo a SOMBRA: cada pixel guarda a sua distância
    relativa ao tom base, então as dobras continuam sendo dobras."""
    if alvo is None:
        return c
    a = np.asarray(c).astype(np.float32)
    m = mascara_pele(a)
    if not m.any():
        return c
    base = np.median(a[m][:, :3], axis=0)          # o tom mais comum da pele
    base = np.maximum(base, 1.0)
    fator = np.array(alvo, dtype=np.float32) / base
    saida = a.copy()
    corpo = a[m][:, :3] * fator
    saida[m, :3] = np.clip(corpo, 0, 255)
    return Image.fromarray(saida.astype(np.uint8), c.mode)


def recorta(folha, x1, y1, x2, y2):
    c = folha.crop((x1, y1, x2, y2))
    c = limpa_fundo(c)
    c = tira_halo(c)
    return aperta(c)


def mesma_tela(pecas):
    u"""Põe as seis mãos na MESMA tela, encostadas no pulso (embaixo, ao centro).

    ⚠️ ISTO É CONSERTO DE LEIAUTE FEITO NA FIGURA, E DE PROPÓSITO. Recortadas
       justas, as seis têm alturas bem diferentes — o punho tem 242 px e a mão
       de um dedo tem 339. Na linha da soma, o navegador centraliza cada uma
       pela metade e os PULSOS ficam em alturas diferentes: as mãos parecem
       flutuar, cada uma num nível. Dá para empurrar isso com CSS (caixa de
       altura fixa, `align-items:flex-end`), e foi o que fiz primeiro — mas aí
       a regra tem de ser repetida em cada lugar que desenha uma mão (a linha
       da soma, o ligar, a capa, a mão viva), e basta esquecer um para o defeito
       voltar. Com as seis do mesmo tamanho, o alinhamento vem de graça em
       TODO lugar, inclusive nos que ainda não existem.

    A tela é a maior largura por a maior altura do conjunto, com uma folga de
    2%: nada é redimensionado nem cortado, só ganha transparente em volta.
    """
    larg = max(c.width for c in pecas)
    alt = max(c.height for c in pecas)
    larg, alt = int(larg * 1.02), int(alt * 1.02)
    saida = []
    for c in pecas:
        tela = Image.new(u"RGBA", (larg, alt), (0, 0, 0, 0))
        tela.paste(c, ((larg - c.width) // 2, alt - c.height), c)
        saida.append(tela)
    return saida


def main():
    if not os.path.isdir(FOLHAS):
        print(u"⛔ não achei %s" % FOLHAS)
        return 2
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    folha = Image.open(os.path.join(FOLHAS, D11)).convert(u"RGB")
    origem, feitas = {}, []
    cam = os.path.join(DEST, u"ORIGEM.json")
    if os.path.exists(cam):
        origem = json.load(io.open(cam, encoding=u"utf-8"))
    cruas, nomes = [], []
    for nome, arq, x1, y1, x2, y2 in PECAS:
        c = recorta(folha, x1, y1, x2, y2)
        if c is None:
            print(u"  ⚠️  %-6s saiu VAZIA" % nome)
            continue
        if max(c.size) > MAIOR:
            f = float(MAIOR) / max(c.size)
            c = c.resize((max(1, int(c.width * f)), max(1, int(c.height * f))),
                         Image.LANCZOS)
        cruas.append(c)
        nomes.append((nome, arq, c.size))
    postas = mesma_tela(cruas)
    for (nome, arq, justo), c in zip(nomes, postas):
        for sufixo, alvo in TONS:
            p = pinta(c, alvo)
            saida = u"%s%s%s.png" % (PREFIXO, nome, sufixo)
            p.save(os.path.join(DEST, saida), optimize=True)
            origem[saida] = u"folha:%s" % DE_ONDE[arq]
            feitas.append((saida, p.size))
        print(u"  ✓ %-6s recorte %3dx%-3d -> tela %3dx%-3d  %d dedos  (3 tons)  <- %s"
              % (nome, justo[0], justo[1], c.width, c.height,
                 DEDOS_ESPERADOS[nome], arq[:3]))
    io.open(cam, u"w", encoding=u"utf-8").write(
        json.dumps(origem, indent=1, sort_keys=True, ensure_ascii=False))
    print(u"\n%d arquivos (6 mãos × 3 tons), todos recortados de folha de papel."
          % len(feitas))
    folha_de_contato(feitas)
    return 0


def folha_de_contato(feitas):
    from PIL import ImageDraw
    COLS, CEL, LAB = 6, 190, 26
    linhas = (len(feitas) + COLS - 1) // COLS
    p = Image.new(u"RGB", (COLS * (CEL + 10) + 10, linhas * (CEL + LAB + 10) + 10),
                  (250, 250, 248))
    d = ImageDraw.Draw(p)
    # a ordem da folha de contato é por TOM (uma fileira por tom), para a
    # conferência que interessa: a mesma mão de 0 a 5, lado a lado.
    ordem = sorted(feitas, key=lambda x: (x[0][-5], x[0]))
    for i, (alvo, _) in enumerate(ordem):
        im = Image.open(os.path.join(DEST, alvo)).convert(u"RGBA")
        im.thumbnail((CEL, CEL))
        x = 10 + (i % COLS) * (CEL + 10)
        y = 10 + (i // COLS) * (CEL + LAB + 10)
        d.rectangle([x, y, x + CEL, y + CEL], outline=(215, 215, 210))
        fundo = Image.new(u"RGBA", im.size, (255, 255, 255, 255))
        fundo.alpha_composite(im)
        p.paste(fundo.convert(u"RGB"), (x + (CEL - im.width) // 2,
                                        y + (CEL - im.height) // 2))
        d.text((x + 3, y + CEL + 6), alvo[len(PREFIXO):-4], fill=(40, 44, 52))
    cam = os.path.join(AQUI, u"_contato.png")
    p.save(cam, optimize=True)
    print(u"folha de contato: %s  — OLHAR antes de seguir" % cam)


if __name__ == u"__main__":
    sys.exit(main())
