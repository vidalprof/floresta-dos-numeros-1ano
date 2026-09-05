# -*- coding: utf-8 -*-
"""
PORTAO — O HALO BRANCO (recorte sujo).

Defeito real que chegou ao Marcos (ago/2026, Museu 3o ano): varias figuras
recortadas de um fundo branco ficaram com um ANEL BRANCO opaco em volta. No card
claro ninguem ve; na CHAPA ESCURA do raio-X (e em todo fundo escuro) o anel salta
como "partes brancas do fundo". O `arte_propria.py` cuida de copia; este cuida de
LIMPEZA de recorte.

Como mede (sem navegador, so Pillow): para cada PNG com transparencia, faz
flood-fill a partir da BORDA passando por {pixel transparente OU quase-branco
opaco}. O quase-branco alcancado por esse caminho e HALO (fundo que sobrou
grudado na silhueta) — porque o branco LEGITIMO do bicho (barriga do pinguim,
faixa do peixe) fica cercado pelo contorno colorido e o flood nao chega nele.

Reprova so halo GROSSO (casca fina >1.5% e razao casca/halo alta). Fio de
borda legitimo (barriga branca na silhueta) fica para o olho do professor.

Uso:  python3 _qa/halo.py <pasta-ou-arquivo> [limiar_percent]
Sai 0 se limpo; 1 se achou halo; 2 se nao teve o que medir.
"""
import sys, os, glob
from collections import deque

try:
    from PIL import Image
    import numpy as np
except Exception as e:
    print("halo: preciso de Pillow+numpy (%s). NAO MEDI." % e); sys.exit(2)

THR = 225  # r,g,b acima disso = "quase-branco"

def halo_frac(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.int16)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    H, W = al.shape
    if (al < 250).mean() < 0.002:   # imagem sem transparencia: nao e recorte
        return -1.0, 0.0, H * W
    nearwhite = (r > THR) & (g > THR) & (b > THR)
    transp = al < 40
    passable = transp | (nearwhite & (al >= 40))
    seen = np.zeros((H, W), bool)
    dq = deque()
    for x in range(W):
        for y in (0, H - 1):
            if passable[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if passable[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and passable[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; dq.append((ny, nx))
    halo = seen & nearwhite & (al >= 40)
    # HALO e uma CASCA FINA colada na silhueta; branco LEGITIMO grande (jaleco do
    # mascote, gato branco) e um BLOCO grosso. Erode 3px: a casca some, o bloco
    # sobrevive. So a casca fina (halo - erodido) conta — mata o falso-positivo.
    m = halo.copy()
    for _ in range(3):
        e = m.copy()
        e[1:, :] &= m[:-1, :]; e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]; e[:, :-1] &= m[:, 1:]
        m = e
    casca = halo & (~m)
    ha = int(halo.sum()); ca = int(casca.sum())
    razao = (ca / ha) if ha else 0.0   # ~1 = quase tudo casca (halo real fino);
                                       # baixo = bloco grosso (jaleco/gato branco)
    return casca.mean() * 100.0, razao, H * W

def main():
    if len(sys.argv) < 2:
        print("uso: python3 _qa/halo.py <pasta-ou-arquivo> [limiar_%]"); return 2
    alvo = sys.argv[1]
    lim = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    if os.path.isdir(alvo):
        # ⚠️ CEGO EM TODA ATIVIDADE (set/2026): as figuras moram em `<pasta>/img/`,
        #    e este portao so olhava a RAIZ da pasta — "nenhum .png, NAO MEDI" em
        #    100% das atividades, todos os dias, sem ninguem estranhar. Agora
        #    olha a raiz E a `img/`.
        arqs = sorted(glob.glob(os.path.join(alvo, "*.png")) +
                      glob.glob(os.path.join(alvo, "img", "*.png")))
    elif os.path.isfile(alvo):
        arqs = [alvo]
    else:
        print("halo: nao achei %s" % alvo); return 2
    if not arqs:
        print("halo: nenhum .png em %s. NAO MEDI." % alvo); return 2
    ruins, medidas = [], 0
    for p in arqs:
        bn = os.path.basename(p)
        if bn.endswith("_xray.png"):
            continue  # chapa de raio-X e arte por luminancia, nao recorte de branco
        try:
            f, razao, _ = halo_frac(p)
        except Exception as e:
            print("   ! nao consegui abrir %s (%s)" % (bn, e)); continue
        if f < 0:
            continue  # sem transparencia, fora do teste
        medidas += 1
        # so reprova se a maior parte for CASCA FINA (razao alta) — branco
        # LEGITIMO grande (jaleco do mascote, gato/urso branco) tem razao baixa.
        if f > lim and razao >= 0.55:
            ruins.append((f, bn))
    print("halo: %d figura(s) com transparencia conferida(s) (limiar %.2f%%)" % (medidas, lim))
    if medidas == 0:
        print("   nenhuma figura recortada para medir. NAO MEDI."); return 2
    if not ruins:
        print("   ok: nenhum halo branco de recorte."); return 0
    ruins.sort(reverse=True)
    print("   %d figura(s) com HALO BRANCO (o fundo grudou na silhueta):" % len(ruins))
    for f, n in ruins[:30]:
        print("    x %6.2f%%  %s" % (f, n))
    print("   conserto: flood-fill da borda por {transparente OU quase-branco} e")
    print("   apagar o quase-branco alcancado (ver _padrao/ESQUELETO/CONTRATO.md).")
    return 1

if __name__ == "__main__":
    sys.exit(main())
