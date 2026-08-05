# -*- coding: utf-8 -*-
# ============================================================
#  ONDE ESTA CADA COISA NA ARTE — para nao chutar coordenada
#
#  Nasceu na cartografia (ago/2026): eu punha o alvo da fase "ache no mapa" numa
#  posicao ESTIMADA, e ele caia AO LADO da igreja. A crianca tocava no lugar
#  certo e levava "errado" — o pior tipo de defeito, porque ensina o contrario.
#
#  Este medidor abre a arte e diz, em % da largura e da altura, onde esta o
#  centro de cada mancha de cor. E so copiar o numero para o codigo.
#
#  Uso:  python3 _qa/pontos.py _mapa/img/mp_mapa.jpg
#        python3 _qa/pontos.py _mapa/img/mp_mapa.jpg vermelho verde azul
# ============================================================
import sys
try:
    from PIL import Image
    import numpy as np
except Exception:
    print("precisa de Pillow e numpy"); sys.exit(2)

CORES = {
    "vermelho": lambda R, G, B: (R > 140) & (R > G + 45) & (R > B + 45),
    "verde":    lambda R, G, B: (G > 90) & (G > R + 18) & (G > B + 18),
    "azul":     lambda R, G, B: (B > 100) & (B > R + 25) & (B > G + 5),
    "amarelo":  lambda R, G, B: (R > 160) & (G > 140) & (B < 110),
    "marrom":   lambda R, G, B: (R > 90) & (R < 190) & (R > G + 20) & (G > B + 10),
    "branco":   lambda R, G, B: (R > 205) & (G > 200) & (B > 190) & (abs(R - G) < 18),
    "escuro":   lambda R, G, B: (R + G + B) < 260,
}

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    arq = sys.argv[1]
    quais = sys.argv[2:] or list(CORES.keys())
    im = Image.open(arq).convert("RGB")
    w, h = im.size
    a = np.asarray(im).astype(int)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    print("%s  (%d x %d)" % (arq, w, h))
    for nome in quais:
        f = CORES.get(nome)
        if not f:
            print("  cor desconhecida: %s" % nome); continue
        m = f(R, G, B)
        # ignora a moldura: mancha colada na borda costuma ser o fundo
        m[:3, :] = False; m[-3:, :] = False; m[:, :3] = False; m[:, -3:] = False
        ys, xs = np.where(m)
        # mancha que ocupa mais de um quarto da arte e o FUNDO, nao um lugar
        if len(xs) > 0.25 * w * h:
            print("  %-9s - (e o fundo: %d%% da arte)" % (nome, round(100.0 * len(xs) / (w * h))))
            continue
        if len(xs) < max(150, (w * h) // 4000):
            print("  %-9s -" % nome); continue
        # separa em ate 3 grupos pela posicao horizontal, para achar manchas distintas
        ordem = np.argsort(xs)
        xs, ys = xs[ordem], ys[ordem]
        cortes = [0, len(xs)]
        saltos = np.where(np.diff(xs) > w * 0.12)[0]
        if len(saltos):
            cortes = [0] + [int(s) + 1 for s in saltos[:2]] + [len(xs)]
        for i in range(len(cortes) - 1):
            gx, gy = xs[cortes[i]:cortes[i + 1]], ys[cortes[i]:cortes[i + 1]]
            if len(gx) < 120: continue
            print("  %-9s x=%2.0f%%  y=%2.0f%%   (%d px%s)"
                  % (nome, 100.0 * gx.mean() / w, 100.0 * gy.mean() / h, len(gx),
                     "" if len(cortes) == 2 else ", mancha %d" % (i + 1)))
    return 0

sys.exit(main())
