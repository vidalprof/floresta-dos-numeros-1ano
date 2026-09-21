# -*- coding: utf-8 -*-
u"""
============================================================
 AS FIGURAS DO CADERNO DO PRE SAEM DAS FOLHAS DE PAPEL

 ⭐ Regra do Marcos (14/set/2026): *"procure na internet, nada de imagem gerada
    por IA, utilize das atividades"*. Cada figura aqui foi RECORTADA de uma
    folha que a professora usa no papel — a mesma folha que deu o gesto.

 Folhas de origem (colhidas em 21/set/2026 por `buscar-fotos.yml`):
   · `c_veic` = `_sequencias/colheita/pre2/d06b1_b83e08.jpg` (2482x3509)
       "MINHA ATIVIDADE — 1. LIGUE CADA FIGURA A SUA SOMBRA" (Tudo Sala de Aula)
   · `c_frut` = `_sequencias/colheita/pre2/d01b1_8295b9.png` (1600x2263)
       "Combinar sombras — QUAL E A SOMBRA CERTA?" (pontodoconhecimento.com)

 ⚠️⚠️ A SOMBRA E DERIVADA DA PROPRIA FIGURA, e isto e uma ESCOLHA, nao preguica.
    As duas folhas trazem as sombras desenhadas do lado direito — mas elas sao de
    OUTRAS poses (a sombra de bicicleta da folha dos veiculos e um quadro de
    homem, e a figura colorida e de mulher). Recortar as duas separadamente
    daria pares que NAO batem, e o caderno estaria ensinando errado justamente
    na folha que pede "ache a sombra DESTA figura".
    Escurecer o recorte colorido garante que a silhueta e exatamente a daquela
    figura — que e o que a folha de papel promete. Fica declarado no
    `img/ORIGEM.json` com o sufixo `_sombra` e o motivo.

 ⚠️ A CAIXA SE CONFERE NA FOLHA DE ORIGEM, nunca no PNG (licao de 21/set/2026):
    o `aperta()` tira o branco de sobra e o recorte SEMPRE sai com cara de
    figura inteira, mesmo com metade do desenho cortada. Por isso o
    `img/RECORTE.json`, que o portao `1i7` le para voltar a folha e medir se a
    tinta continua para fora da caixa.

 Uso: python3 _observa/recortar_das_folhas.py
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
sys.path.insert(0, os.path.join(RAIZ, "_padrao"))
from recorte_folha import limpa_fundo, tira_halo, aperta          # noqa: E402

IMG = os.path.join(AQUI, "img")
FOLHAS = {
    "c_veic": os.path.join(RAIZ, "_sequencias/colheita/pre2/d06b1_b83e08.jpg"),
    "c_frut": os.path.join(RAIZ, "_sequencias/colheita/pre2/d01b1_8295b9.png"),
}

# (nome, folha, x0, y0, x1, y1) — em FRACAO da folha, medidos na folha aberta.
PECAS = [
    # --- os cinco veiculos, coluna da esquerda da folha `c_veic`
    (u"ob_bicicleta",  "c_veic", 0.060, 0.205, 0.285, 0.303),
    (u"ob_bicicleta2", "c_veic", 0.068, 0.363, 0.285, 0.455),
    (u"ob_moto",       "c_veic", 0.082, 0.528, 0.282, 0.618),
    (u"ob_skate",      "c_veic", 0.078, 0.695, 0.278, 0.805),
    (u"ob_patinete",   "c_veic", 0.082, 0.840, 0.278, 0.945),
    # --- as seis frutas e legumes, coluna da esquerda da folha `c_frut`
    (u"ob_limao",      "c_frut", 0.118, 0.272, 0.254, 0.379),
    (u"ob_beterraba",  "c_frut", 0.104, 0.384, 0.258, 0.501),
    (u"ob_amora",      "c_frut", 0.125, 0.504, 0.243, 0.604),
    (u"ob_melancia",   "c_frut", 0.097, 0.627, 0.272, 0.694),
    (u"ob_tomate",     "c_frut", 0.129, 0.727, 0.272, 0.816),
    (u"ob_laranja",    "c_frut", 0.129, 0.839, 0.250, 0.926),
]
# de quais figuras nasce a sombra (folhas 3 e 4)
SOMBRAS = [u"ob_bicicleta", u"ob_moto", u"ob_skate", u"ob_patinete",
           u"ob_limao", u"ob_beterraba", u"ob_melancia", u"ob_tomate",
           u"ob_laranja", u"ob_amora"]


def cresce_caixa(im, cx, teto=2.2, lim=244):
    u"""A caixa marcada a olho CORTA — a mancha de tinta que encosta na borda
    continua para fora dela. Aqui a caixa cresce ate a tinta acabar.

    ⚠️ A mancha so conta se 60% dela estiver DENTRO da caixa inicial (licao paga
       no `_dinheiro5`): sem isso, o contorno do cartao da folha arrasta a caixa
       ate engolir o titulo da atividade."""
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


def vira_sombra(c):
    u"""A silhueta: tudo o que e opaco vira um cinza-escuro so. E o que a folha
    de papel mostra do lado direito — a figura sem a cor."""
    import numpy as np
    a = np.array(c.convert("RGBA"))
    op = a[:, :, 3] > 120
    a[:, :, 0][op] = 58
    a[:, :, 1][op] = 62
    a[:, :, 2][op] = 78
    a[:, :, 3][~op] = 0
    return Image.fromarray(a, "RGBA")


def main():
    if not os.path.isdir(IMG):
        os.makedirs(IMG)
    abertas, origem, recorte = {}, {}, {}
    for nome, folha, fx0, fy0, fx1, fy1 in PECAS:
        cam = FOLHAS[folha]
        if folha not in abertas:
            abertas[folha] = Image.open(cam).convert("RGB")
        f = abertas[folha]
        W, H = f.size
        cx = (int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H))
        cx = cresce_caixa(f, cx)
        c = limpa_fundo(f.crop(cx).convert("RGBA"))
        c = tira_halo(c, voltas=2)
        c = aperta(c)
        c.thumbnail((400, 400))
        c.save(os.path.join(IMG, nome + ".png"))
        origem[nome + ".png"] = u"folha:%s" % folha
        recorte[nome + ".png"] = {
            u"folha": os.path.relpath(cam, RAIZ),
            u"caixa": list(cx),
            u"caixa_fracao": [fx0, fy0, fx1, fy1],
            u"tamanho": list(c.size),
        }
        print(u"  %-16s %s  %dx%d" % (nome, folha, c.size[0], c.size[1]))
        if nome in SOMBRAS:
            s = vira_sombra(c)
            s.save(os.path.join(IMG, nome + "_sombra.png"))
            origem[nome + "_sombra.png"] = (
                u"derivada de %s.png (a mesma figura, sem a cor) — as sombras "
                u"desenhadas na folha sao de OUTRAS poses e dariam par errado" % nome)
            print(u"  %-16s sombra derivada" % (nome + "_sombra"))

    for arq, dado in ((u"ORIGEM.json", origem), (u"RECORTE.json", recorte)):
        io.open(os.path.join(IMG, arq), "w", encoding="utf-8").write(
            json.dumps(dado, ensure_ascii=False, indent=1) + u"\n")
    print(u"\n%d figura(s) + %d sombra(s) em %s" % (len(PECAS), len(SOMBRAS), IMG))


if __name__ == "__main__":
    main()
