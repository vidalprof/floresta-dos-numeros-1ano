from PIL import Image
import numpy as np
from scipy import ndimage
import os

SRC = "img/imagensparaprojeto.png"
OUT = "img"

im = Image.open(SRC).convert("RGBA")
arr = np.array(im)
H, W = arr.shape[0], arr.shape[1]
r, g, b = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)

# pixels quase brancos
whiteish = (r > 236) & (g > 236) & (b > 236)
lbl, n = ndimage.label(whiteish)
border = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
border.discard(0)
bg = np.isin(lbl, list(border))

alpha = np.where(bg, 0, 255).astype(np.uint8)

# defringe leve: onde NAO e fundo mas e quase branco e vizinho de fundo, suaviza alpha
arr[..., 3] = alpha

# corta franja branca: reduz um pouco as bordas do conteudo (erosao de 1px do alpha)
mask = alpha > 0
eroded = ndimage.binary_erosion(mask, iterations=1)
# mantem opaco no miolo, suaviza so a borda
edge = mask & (~eroded)
a2 = arr[..., 3].astype(int)
a2[edge] = (a2[edge] * 0.5).astype(int)
arr[..., 3] = a2.astype(np.uint8)

clean = Image.fromarray(arr, "RGBA")

# grade 2 linhas x 3 colunas
names = [
    ["ilha-tesouro", "ilha-exploradores", "ilha-aventureiros"],
    ["mascote-tesouro", "mascote-exploradores", "mascote-aventureiros"],
]
cw, ch = W / 3.0, H / 2.0

def keep_main(cell):
    a = np.array(cell)
    solid = a[..., 3] > 40
    lb, nn = ndimage.label(solid)
    if nn <= 1:
        return cell
    sizes = ndimage.sum(np.ones_like(lb), lb, range(1, nn + 1))
    keep = int(np.argmax(sizes)) + 1
    drop = (lb != keep) & (lb != 0)
    a[drop, 3] = 0
    return Image.fromarray(a, "RGBA")

def autocrop(cell):
    cell = keep_main(cell)
    a = np.array(cell)[..., 3]
    ys, xs = np.where(a > 12)
    if len(xs) == 0:
        return cell
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pad = 6
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(cell.width - 1, x1 + pad); y1 = min(cell.height - 1, y1 + pad)
    return cell.crop((x0, y0, x1 + 1, y1 + 1))

for rrow in range(2):
    for ccol in range(3):
        left = int(ccol * cw); right = int((ccol + 1) * cw)
        top = int(rrow * ch); bot = int((rrow + 1) * ch)
        cell = clean.crop((left, top, right, bot))
        cell = autocrop(cell)
        out = os.path.join(OUT, names[rrow][ccol] + ".png")
        cell.save(out)
        print(names[rrow][ccol], "->", cell.size)
print("OK")
