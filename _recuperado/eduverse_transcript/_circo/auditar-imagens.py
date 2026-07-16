#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITOR DE IMAGENS — pega "restos de outras imagens" (fragmentos soltos) nos
recortes embutidos, ANTES de publicar. Foi o buraco que deixou passar as ilhas
com pedaços de outras cenas grudados (o fundo escuro escondia).

Para cada imagem `data:image...base64` com transparência, conta os blocos
conectados (componentes) de pixels opacos. Se, além do bloco principal, houver
um bloco secundário "significativo" (>= X% do maior) e **separado** dele por um
vão (fragmento solto), REPROVA aquela imagem. Ícones pequenos/uniformes passam.

Uso:  python3 _circo/auditar-imagens.py <arquivo.html> [--min-frac 0.05] [--gap 5]
Saída: lista das imagens suspeitas. Código != 0 se reprovar.
"""
import sys, re, base64, io

def carregar_np():
    try:
        import numpy as np
        from scipy import ndimage
        from PIL import Image
        return np, ndimage, Image
    except Exception as e:
        print("::error:: precisa de numpy+scipy+Pillow: %s" % e); sys.exit(2)

def analisar(uri, np, ndimage, Image, min_frac, gap):
    try:
        b = base64.b64decode(uri.split(",", 1)[1])
        im = Image.open(io.BytesIO(b)).convert("RGBA")
    except Exception:
        return None
    a = np.array(im)
    if a.shape[2] < 4:
        return None
    alpha = a[:, :, 3]
    mask = alpha > 40
    if mask.sum() < 30:
        return None
    # sem transparência real (fundo sólido) -> não é recorte, ignora
    if (alpha < 250).sum() < 0.02 * alpha.size:
        return None
    lbl, n = ndimage.label(mask)
    if n <= 1:
        return None
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    maior = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lbl == maior)
    mx0, mx1, my0, my1 = xs.min(), xs.max(), ys.min(), ys.max()
    suspeitos = []
    for c in range(1, n + 1):
        if c == maior:
            continue
        frac = sizes[c - 1] / sizes[maior - 1]
        if frac < min_frac:
            continue
        cys, cxs = np.where(lbl == c)
        cx0, cx1, cy0, cy1 = cxs.min(), cxs.max(), cys.min(), cys.max()
        gx = max(0, cx0 - mx1, mx0 - cx1)   # vão horizontal até o bloco maior
        gy = max(0, cy0 - my1, my0 - cy1)   # vão vertical
        if gx >= gap or gy >= gap:
            suspeitos.append((round(frac * 100), int(max(gx, gy))))
    return suspeitos if suspeitos else None

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("uso: python3 _circo/auditar-imagens.py <arquivo.html> [--min-frac 0.05] [--gap 5]"); sys.exit(2)
    src = args[0]
    def opt(name, d):
        for i, a in enumerate(sys.argv):
            if a == name and i + 1 < len(sys.argv):
                return float(sys.argv[i + 1])
        return d
    min_frac = opt("--min-frac", 0.05)
    gap = int(opt("--gap", 5))
    np, ndimage, Image = carregar_np()
    h = open(src, encoding="utf-8").read()
    # nome da variavel/chave mais proxima, p/ ajudar a localizar
    pares = re.findall(r'"([A-Za-z0-9_]{1,30})"\s*:\s*"(data:image/[a-z]+;base64,[^"]+)"', h)
    total = len(pares)
    reprovadas = 0
    for nome, uri in pares:
        r = analisar(uri, np, ndimage, Image, min_frac, gap)
        if r:
            reprovadas += 1
            frags = ", ".join("%d%% (vão %dpx)" % (f, g) for f, g in r)
            print("  REPROVADA  \"%s\": %d fragmento(s) solto(s) -> %s" % (nome, len(r), frags))
    print("== RESUMO IMAGENS: %s (%d imagens checadas) ==" %
          ("APROVADO (sem restos soltos)" if reprovadas == 0 else "REPROVADO — %d imagem(ns) com restos" % reprovadas, total))
    sys.exit(0 if reprovadas == 0 else 1)

if __name__ == "__main__":
    main()
