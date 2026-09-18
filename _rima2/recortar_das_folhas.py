# -*- coding: utf-8 -*-
u"""
============================================================
 RECORTAR AS FIGURAS DAS FOLHAS DE PAPEL — A Parlenda que Rima (2º ano)

 ⭐ A REGRA QUE MANDA AQUI (Marcos, 14/set/2026): *"procure na internet, nada de
    imagem gerada por IA, utilize das atividades"*. As figuras deste caderno saem
    de três das quarenta folhas colhidas (`_sequencias/POTE-RIMA2.md` §4):

   · d31 — o cartaz ilustrado de *HOJE É DOMINGO* (Domínio Popular). Sete figuras
     coloridas, e elas NÃO são enfeite: são exatamente os pares que rimam da
     parlenda — barro/**jarro**, fino/**sino**, ouro/**touro**, valente/**gente**,
     fraco/**buraco**, fundo/**mundo**. A criança vê a cadeia inteira.
   · d12 — *"CIRCULE AS FIGURAS QUE TERMINAM COM A MESMA SÍLABA DO DESENHO"*
     (o desenho é JANELA): panela e vela rimam; bolsa, pato, bola e escova não.
     Os seis entram, porque os que NÃO rimam são metade do trabalho.
   · d15 — a galinha choca e o ninho, da parlenda *GALINHA CHOCA*.

 ⚠️ AS CAIXAS FORAM MEDIDAS, NÃO CHUTADAS: saem de uma varredura de ILHAS DE
    TINTA (`scipy.ndimage.label` sobre os pixels escuros e os coloridos), lida
    antes de dar nome a cada uma.

 ⚠️ E O NOME TEM DE BATER COM O DESENHO — trocar um nome aqui não dá erro
    nenhum, só faz a criança ver uma vela onde a palavra diz PANELA. Conferir
    OLHANDO a folha de contato que este script gera.

 ⚠️ O QUE FICOU DE FORA, de propósito:
    · a d30 e a d32, que têm figuras boas mas cada uma DENTRO de um quadradinho
      impresso com o rótulo embaixo — recortar traria a moldura e a palavra, e a
      palavra é justamente a resposta;
    · a d40, que desenha o mesmo cachimbo, jarro e touro da d31 a traço: seriam
      duas figuras diferentes com o mesmo nome, e o portão `1c2` reprova isso.

 Uso:  python3 _rima2/recortar_das_folhas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys

try:
    from PIL import Image
except ImportError as e:                                   # pragma: no cover
    print(u"preciso de Pillow (%s)" % e)
    sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, u"_padrao"))
from recorte_folha import (limpa_fundo, tira_halo, aperta,          # noqa: E402
                           tira_linha_impressa)

FOLHAS = os.path.join(RAIZ, u"_sequencias", u"folhas_rima2")
DEST = os.path.join(AQUI, u"img")
PREFIXO = u"qd_"

MAIOR = 300        # teto de resolução: o `_qa/leiaute_mao.js` reprova figura
                   # mostrada acima de 1,35× da própria altura

D31 = u"d31_462749.jpg"
D12 = u"d12_5bf4ac.jpg"
D15 = u"d15_3e2aff.jpg"

PECAS = [
    # --- d31: a cadeia de rimas de HOJE É DOMINGO --------------------------
    (u"cachimbo", D31,  794, 187,  982, 329),
    (u"jarro",    D31,   85, 361,  211, 523),
    (u"sino",     D31,  799, 532,  955, 698),
    (u"touro",    D31,  113, 678,  295, 875),
    (u"gente",    D31,  801, 897, 1015,1061),
    (u"buraco",   D31,   79,1078,  317,1241),
    (u"mundo",    D31,  815,1248, 1018,1407),

    # --- d12: as que rimam com JANELA, e as que não ------------------------
    (u"panela",   D12,  286, 700,  408, 788),
    (u"bolsa",    D12,  458, 687,  546, 784),
    (u"vela",     D12,  602, 692,  668, 788),
    (u"pato",     D12,  302, 799,  402, 898),
    (u"bola",     D12,  451, 799,  538, 898),
    (u"escova",   D12,  587, 799,  683, 898),

    # --- d15: a parlenda da galinha ---------------------------------------
    (u"galinha",  D15,  382, 207,  525, 420),
    (u"ninho",    D15,  517, 325,  652, 420),
]

DE_ONDE = {
    D31: u"d31 — cartaz ilustrado da parlenda HOJE É DOMINGO (Domínio Popular)",
    D12: u"d12 — CIRCULE AS FIGURAS QUE TERMINAM COM A MESMA SÍLABA DO DESENHO",
    D15: u"d15 — PARLENDA: GALINHA CHOCA, LEIA E RESPONDA",
}


def recorta(folha, x1, y1, x2, y2):
    c = folha.crop((x1, y1, x2, y2))
    c = limpa_fundo(c)
    c = tira_halo(c)
    c = aperta(c)
    if c is not None:
        c = aperta(tira_linha_impressa(c))
    return c


def main():
    if not os.path.isdir(FOLHAS):
        print(u"⛔ não achei %s" % FOLHAS)
        return 2
    abertas, feitas, origem = {}, [], {}
    cam = os.path.join(DEST, u"ORIGEM.json")
    if os.path.exists(cam):
        origem = json.load(io.open(cam, encoding=u"utf-8"))
    for nome, arq, x1, y1, x2, y2 in PECAS:
        if arq not in abertas:
            abertas[arq] = Image.open(os.path.join(FOLHAS, arq)).convert(u"RGB")
        c = recorta(abertas[arq], x1, y1, x2, y2)
        if c is None:
            print(u"  ⚠️  %-10s saiu VAZIA (caixa só com papel?)" % nome)
            continue
        if max(c.size) > MAIOR:
            f = float(MAIOR) / max(c.size)
            c = c.resize((max(1, int(c.width * f)), max(1, int(c.height * f))),
                         Image.LANCZOS)
        alvo = PREFIXO + nome + u".png"
        c.save(os.path.join(DEST, alvo), optimize=True)
        origem[alvo] = u"folha:%s" % DE_ONDE[arq]
        feitas.append((alvo, c.size))
        print(u"  ✓ %-16s %3dx%-3d  <- %s" % (alvo, c.width, c.height, arq[:3]))
    io.open(cam, u"w", encoding=u"utf-8").write(
        json.dumps(origem, indent=1, sort_keys=True, ensure_ascii=False))
    print(u"\n%d figuras, todas recortadas de folha de papel." % len(feitas))
    folha_de_contato(feitas)
    return 0


def folha_de_contato(feitas):
    u"""A prancha que se OLHA — é aqui que se pega o nome trocado, e esse defeito
    portão nenhum acha: ele não dá erro, só ensina errado."""
    from PIL import ImageDraw
    COLS, CEL, LAB = 5, 180, 26
    linhas = (len(feitas) + COLS - 1) // COLS
    p = Image.new(u"RGB", (COLS * (CEL + 10) + 10,
                           linhas * (CEL + LAB + 10) + 10), (250, 250, 248))
    d = ImageDraw.Draw(p)
    for i, (alvo, _) in enumerate(feitas):
        im = Image.open(os.path.join(DEST, alvo)).convert(u"RGBA")
        im.thumbnail((CEL, CEL))
        x = 10 + (i % COLS) * (CEL + 10)
        y = 10 + (i // COLS) * (CEL + LAB + 10)
        d.rectangle([x, y, x + CEL, y + CEL], outline=(215, 215, 210))
        fundo = Image.new(u"RGBA", im.size, (255, 255, 255, 255))
        fundo.alpha_composite(im)
        p.paste(fundo.convert(u"RGB"),
                (x + (CEL - im.width) // 2, y + (CEL - im.height) // 2))
        d.text((x + 3, y + CEL + 6), alvo[len(PREFIXO):-4], fill=(40, 44, 52))
    cam = os.path.join(AQUI, u"_contato.png")
    p.save(cam, optimize=True)
    print(u"folha de contato: %s  — OLHAR antes de seguir" % cam)


if __name__ == u"__main__":
    sys.exit(main())
