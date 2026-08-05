#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorta as 4 imagens de apoio da cartografia (fundo CREME uniforme).

O fundo nao e preto (como o do Gemini) e sim um creme claro: usar limiar de
brilho aqui apagaria a lousa clara e o piso da sala. Entao a mascara nasce de
um FLOOD FILL a partir das bordas — so o creme que ENCOSTA na moldura vira
transparencia; creme que estiver DENTRO do objeto (um reflexo, um vao) fica.

Uso: python3 _mapa/cortar_props.py
"""
import io
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ORIG = "_novo"
DEST = "_mapa/img"


def fundo_das_bordas(arr, tol=26):
    """Mascara True onde e FUNDO (creme ligado a alguma borda)."""
    h, w = arr.shape[:2]
    cantos = np.array([arr[2, 2], arr[2, w - 3], arr[h - 3, 2], arr[h - 3, w - 3]],
                      dtype=np.int16)
    cor = cantos.mean(axis=0)
    perto = (np.abs(arr.astype(np.int16) - cor).max(axis=2) <= tol)
    lab, n = ndimage.label(perto)
    borda = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) \
        | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    borda.discard(0)
    return np.isin(lab, list(borda))


def tira_moldura_preta(im):
    """O celular do Marcos salva as fotos com uma tarja PRETA em volta.

    ⚠️ Isso quase custou o recorte: a amostragem de cor pega os CANTOS, os
    cantos estavam pretos, e o flood fill saiu limpando a tarja em vez do
    creme — as quatro imagens vieram inteiras, com o fundo todo. Tirar a
    tarja ANTES de qualquer coisa.
    """
    arr = np.asarray(im)
    claro = arr.max(axis=2) > 18
    ys, xs = np.where(claro)
    if not len(ys):
        return im
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def recorta(origem, destino, margem=8, larg=520):
    """Recorta o prop e deixa a SOMBRA suave em vez de um halo creme opaco.

    ⚠️ Mascara binaria (dentro/fora) devolve a sombra do desenho como um
    pedaco de creme SOLIDO — na tela vira uma mancha feia embaixo do objeto.
    Aqui o alfa e uma RAMPA sobre a distancia da cor do fundo: o creme puro
    some, a sombra fica translucida (parece sombra de verdade) e o objeto
    fica cheio. A rampa so vale PERTO do objeto; longe dele, zero.
    """
    im = tira_moldura_preta(Image.open(os.path.join(ORIG, origem)).convert("RGB"))
    arr = np.asarray(im).astype(np.int16)
    h, w = arr.shape[:2]
    cor = np.array([arr[2, 2], arr[2, w - 3], arr[h - 3, 2], arr[h - 3, w - 3]]).mean(axis=0)
    d = np.abs(arr - cor).max(axis=2)

    nucleo = ndimage.binary_fill_holes(d > 55)
    lab, n = ndimage.label(nucleo)
    if n > 1:
        areas = ndimage.sum(np.ones_like(lab), lab, index=range(1, n + 1))
        nucleo = (lab == (int(np.argmax(areas)) + 1))
    perto = ndimage.binary_dilation(nucleo, np.ones((3, 3)), iterations=12)

    rampa = np.clip((d - 20.0) / 40.0, 0, 1)
    alfa = (np.maximum(rampa * perto, nucleo) * 255).astype(np.uint8)
    alfa = ndimage.gaussian_filter(alfa.astype(np.float32), 0.7).astype(np.uint8)

    ys, xs = np.where(alfa > 8)
    y0 = max(0, ys.min() - margem); y1 = min(h, ys.max() + margem + 1)
    x0 = max(0, xs.min() - margem); x1 = min(w, xs.max() + margem + 1)
    out = Image.fromarray(np.dstack([arr.astype(np.uint8), alfa])[y0:y1, x0:x1], "RGBA")
    if out.width > larg:
        out = out.resize((larg, int(out.height * float(larg) / out.width)), Image.LANCZOS)
    # PC da escola: PNG de 400 KB pesa. Paleta de 160 cores + alfa proprio
    # deixa em ~1/4 do tamanho sem diferenca visivel nestes desenhos chapados.
    rgb = out.convert("RGB").quantize(colors=160, method=Image.MEDIANCUT).convert("RGB")
    out = Image.merge("RGBA", list(rgb.split()) + [out.split()[3]])
    out.save(os.path.join(DEST, destino), optimize=True)
    print("%-16s -> %-22s %dx%d  %d KB"
          % (origem, destino, out.width, out.height,
             os.path.getsize(os.path.join(DEST, destino)) // 1024))


def cena(origem, destino, larg=760):
    """CENA larga (fica .jpg): so redimensiona e comprime."""
    im = tira_moldura_preta(Image.open(os.path.join(ORIG, origem)).convert("RGB"))
    # ⚠️ a planta vem com uma tarja creme larga em volta. Se ela ficar, as
    # coordenadas dos moveis (x/y em %) caem em cima da PAREDE em vez do
    # chao — a lousa a 12% de altura pousava fora da sala. Corta no comodo.
    arr = np.asarray(im).astype(np.int16)
    h, w = arr.shape[:2]
    cor = np.array([arr[2, 2], arr[2, w - 3], arr[h - 3, 2], arr[h - 3, w - 3]]).mean(axis=0)
    ys, xs = np.where(np.abs(arr - cor).max(axis=2) > 26)
    im = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    im = im.resize((larg, int(im.height * float(larg) / im.width)), Image.LANCZOS)
    im.save(os.path.join(DEST, destino), quality=86, optimize=True, progressive=True)
    print("%-16s -> %-22s %dx%d  %d KB"
          % (origem, destino, im.width, im.height,
             os.path.getsize(os.path.join(DEST, destino)) // 1024))


if __name__ == "__main__":
    # a bussola aparece num quadro de 250px; 380 ja e o dobro do necessario
    recorta("IMG_3053.jpeg", "mp_rosa.png", larg=380)
    cena("IMG_3054.jpeg", "mp_planta_sala.jpg")
    # os moveis da planta aparecem em 44px na tela: 520px de largura era
    # doze vezes mais pixel do que o PC da escola precisa baixar.
    recorta("IMG_3055.jpeg", "mp_lousa_c.png", larg=240)
    recorta("IMG_3056.jpeg", "mp_armario_c.png", larg=240)
