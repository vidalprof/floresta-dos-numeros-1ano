# -*- coding: utf-8 -*-
u"""RECORTE PROFISSIONAL de peças (rembg / isnet-general-use).

Por que existe (pedido do Marcos, ago/2026: "use ferramentas profissionais para
recortar, tudo perfeito e lindo, sem mancha, tudo sem fundo"): o recorte por
flood-fill de cor NÃO separa peça PRETA em fundo PRETO (a cartola saía manchada
de branco). O rembg é um modelo treinado: recorta qualquer objeto — inclusive
preto-no-preto — com borda limpa e alfa suave.

Instalação (uma vez, funciona pelo proxy): pip install rembg onnxruntime
Modelo: 'isnet-general-use' (baixa sozinho na 1ª vez; melhor que u2netp, que
deixava um halo cinza). Depois de recortar, o alfa < 60 é zerado (mata sombra
fraca) e a peça é aparada pela bbox.

USO — cartela em GRADE (uma peça por célula; pares ficam juntos):
  python3 _padrao/recortar.py grade <folha.png> LxC nome1,nome2,... --dest <pasta>
USO — imagem de UM objeto só (mascote, cena com 1 personagem):
  python3 _padrao/recortar.py um <arquivo.png> <nome> --dest <pasta>
USO — MASCOTE (3 poses alinhadas na MESMA bbox p/ não tremer):
  python3 _padrao/recortar.py mascote <feliz.png> <fala.png> <pisca.png> <prefixo>_<mascote> --dest <pasta>
"""
import os, sys
from PIL import Image
import numpy as np
from rembg import remove, new_session

_S = None
def sess():
    global _S
    if _S is None: _S = new_session("isnet-general-use")
    return _S

def limpa(img, thr=60, trim=True):
    a = np.array(remove(img.convert("RGB"), session=sess()).convert("RGBA"))
    al = a[:, :, 3]; al[al < thr] = 0; a[:, :, 3] = al
    o = Image.fromarray(a)
    if trim:
        bb = o.getbbox()
        if bb: o = o.crop(bb)
    return o

def grade(folha, l, c, nomes, dest):
    im = Image.open(folha).convert("RGB"); W, H = im.size
    cw, ch = W/float(c), H/float(l)
    if len(nomes) != l*c:
        print("!! grade %dx%d = %d celulas, mas %d nomes" % (l, c, l*c, len(nomes))); return 1
    if not os.path.isdir(dest): os.makedirs(dest)
    for i, nome in enumerate(nomes):
        r, k = i//c, i % c
        cell = im.crop((int(k*cw), int(r*ch), int((k+1)*cw), int((r+1)*ch)))
        out = limpa(cell); out.save(os.path.join(dest, nome+".png"), optimize=True)
        print("  %-18s %dx%d" % (nome, out.width, out.height))
    return 0

def um(arq, nome, dest):
    if not os.path.isdir(dest): os.makedirs(dest)
    out = limpa(Image.open(arq)); out.save(os.path.join(dest, nome+".png"), optimize=True)
    print("  %-18s %dx%d" % (nome, out.width, out.height)); return 0

def mascote(feliz, fala, pisca, base, dest):
    u"""3 poses -> <base>_feliz/_fala/_pisca.png, TODAS na mesma bbox de uniao
    (senao o boneco treme: o motor cruza as camadas ~60x/s)."""
    if not os.path.isdir(dest): os.makedirs(dest)
    cortes = {"feliz": limpa(Image.open(feliz), trim=False),
              "fala":  limpa(Image.open(fala),  trim=False),
              "pisca": limpa(Image.open(pisca), trim=False)}
    bb = None
    for o in cortes.values():
        b = o.getbbox()
        if bb is None: bb = list(b)
        else:
            bb[0]=min(bb[0],b[0]); bb[1]=min(bb[1],b[1]); bb[2]=max(bb[2],b[2]); bb[3]=max(bb[3],b[3])
    for k, o in cortes.items():
        c = o.crop(tuple(bb)); c.save(os.path.join(dest, "%s_%s.png" % (base, k)), optimize=True)
        print("  %s_%s %dx%d" % (base, k, c.width, c.height))
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    dest = "_novo/rec"
    if "--dest" in sys.argv: dest = sys.argv[sys.argv.index("--dest")+1]
    cmd = sys.argv[1]
    if cmd == "grade":
        l, c = [int(x) for x in sys.argv[3].lower().split("x")]
        nomes = [n.strip() for n in sys.argv[4].split(",") if n.strip()]
        sys.exit(grade(sys.argv[2], l, c, nomes, dest))
    if cmd == "um":
        sys.exit(um(sys.argv[2], sys.argv[3], dest))
    if cmd == "mascote":
        sys.exit(mascote(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], dest))
    print(__doc__); sys.exit(2)
