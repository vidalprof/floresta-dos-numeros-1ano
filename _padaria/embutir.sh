#!/usr/bin/env bash
# ============================================================
#  A PADARIA DAS LETRAS — do lote gerado até a arte no lugar.
#
#  ⚠️ POR QUE ISTO É UM SCRIPT E NÃO "eu lembro os comandos": porque a próxima
#  atividade vai precisar dos MESMOS passos, e comando que só vive na memória de
#  quem leu o manual não é processo — é sorte. (É a mesma lição que fez a
#  cartela virar ferramenta.)
#
#  O que ele faz, em ordem:
#   1. recorta as 3 cartelas com os NOMES certos, na ordem de leitura da grade.
#      O fundo PRETO da folha vira ALFA de verdade — é daí que sai o "sem fundo"
#      que o Marcos pediu, e não de CSS;
#   2. traz as camadas do mascote e o fundo (que não vão em cartela);
#   3. traz do BANCO o que já estava desenhado (nesta atividade, `biscoito`);
#   4. confere que toda figura pedida no arte.json existe de verdade.
#
#  Uso:  bash _padaria/embutir.sh
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/.."
DEST="_padaria/img"
mkdir -p "$DEST"

falta=0
for f in _novo/cart_crachas.png _novo/cart_objetos1.png _novo/cart_objetos2.png \
         _novo/pd_miga_feliz.png _novo/pd_miga_fala.png _novo/pd_miga_pisca.png \
         _novo/pd_fundo.png; do
  [ -f "$f" ] || { echo "  falta: $f"; falta=1; }
done
if [ "$falta" = "1" ]; then
  echo "!! o lote ainda nao chegou inteiro — nao vou recortar pela metade."
  exit 1
fi

echo "== 1) recortando as cartelas (fundo preto -> transparente) =="
python3 _padrao/cartela.py cortar _novo/cart_crachas.png \
  pd_cr1,pd_cr2,pd_cr3,pd_cr4,pd_cr5,pd_cr6,med_pd --dest "$DEST"
python3 _padrao/cartela.py cortar _novo/cart_objetos1.png \
  pd_pao,pd_bolo,pd_bolacha,pd_bolinho,pd_biscoito,pd_queijo,pd_leite,pd_mel --dest "$DEST"
python3 _padrao/cartela.py cortar _novo/cart_objetos2.png \
  pd_sal,pd_acucar,pd_massa,pd_mamao,pd_mala,pd_pato,pd_sapato --dest "$DEST"

echo "== 2) o mascote (fora da cartela, senao ele treme) e o fundo =="
python3 - <<'PY'
from PIL import Image
import os
# as tres camadas saem com a MESMA bbox: e isso que impede o tremor no lip-sync
nomes = ["pd_miga_feliz", "pd_miga_fala", "pd_miga_pisca"]
ims = [Image.open("_novo/%s.png" % n).convert("RGBA") for n in nomes]
def corta_fundo(im):
    px = im.load()
    l, a = im.size
    fundo = px[0, 0][:3]
    for y in range(a):
        for x in range(l):
            r, g, b, _ = px[x, y]
            if abs(r-fundo[0]) < 34 and abs(g-fundo[1]) < 34 and abs(b-fundo[2]) < 34:
                px[x, y] = (r, g, b, 0)
    return im
ims = [corta_fundo(i) for i in ims]
bb = None
for i in ims:
    b = i.getbbox()
    bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]),
                               max(bb[2], b[2]), max(bb[3], b[3]))
for n, i in zip(nomes, ims):
    r = i.crop(bb)
    r.thumbnail((520, 520), Image.LANCZOS)
    r.save("_padaria/img/%s.png" % n, optimize=True)
    print("  -> %-16s %dx%d" % (n, r.width, r.height))
# o fundo e cena larga: nao se recorta, so se encolhe
f = Image.open("_novo/pd_fundo.png").convert("RGB")
f.thumbnail((1280, 1280), Image.LANCZOS)
f.save("_padaria/img/pd_fundo.jpg", quality=84, optimize=True, progressive=True)
print("  -> pd_fundo.jpg %dx%d" % (f.width, f.height))
PY

echo "== 3) o que ja estava no BANCO (nao se paga de novo) =="
python3 - <<'PY'
import json, io, os, shutil
arte = json.load(io.open("_padaria/arte.json", encoding="utf-8"))
for n in arte.get("no_banco") or []:
    for ext in (".png", ".jpg"):
        o = os.path.join("_banco", "img", n + ext)
        if os.path.exists(o):
            shutil.copy(o, os.path.join("_padaria", "img", "pd_" + n + ext))
            print("  -> do banco: %s" % n)
            break
PY

echo "== 4) conferindo: toda figura pedida existe? =="
python3 _qa/arte_pedida.py _padaria
