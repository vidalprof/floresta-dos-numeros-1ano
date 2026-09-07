# -*- coding: utf-8 -*-
u"""
OTIMIZAR IMAGENS — o remédio do portão de peso (`_qa/peso.py`, DESIGN.md §8)

Reduz cada imagem de `<pasta>/img` ao tamanho que a tela realmente usa e regrava
comprimida, sem trocar nome nem formato (o motor referencia `img/<nome>.png`):
  · figura de peça: lado maior <= 512 px      · fundo/cena (`fundo`, `cena`): <= 1024 px
  · PNG regravado com `optimize`; JPG com qualidade 82
  · as CAMADAS DO MASCOTE (`_feliz/_fala/_pisca`) e os crachás (`_cr`) só encolhem se as
    tres/todas tiverem o MESMO tamanho original — senao o lip-sync treme (mascote.py).
  · pula o que ja esta no tamanho e nao ganha nada (< 8% de economia)

Uso:  python3 _padrao/otimizar_img.py <pasta>            # so mostra o que faria
      python3 _padrao/otimizar_img.py <pasta> --aplicar  # regrava
Depois: remontar (o montador nao muda), rodar `_qa/peso.py` e a banca — o portao de
fotos (5c) vai acusar diferenca de pixel onde a imagem encolheu: olhar e `--aprovar`.
"""
import io, os, sys

try:
    from PIL import Image
except Exception:
    print("sem Pillow — nada feito")
    sys.exit(2)


def alvo_de(nome):
    n = nome.lower()
    return 1024 if ("fundo" in n or "cena" in n or "mapa" in n) else 512


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    aplicar = "--aplicar" in sys.argv
    d = os.path.join(pasta, "img")
    if not os.path.isdir(d):
        print("%s -> sem img/" % pasta)
        return 2
    arqs = sorted(f for f in os.listdir(d) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    # camadas do mascote: mesmo tamanho original obrigatorio
    grupos = {}
    for f in arqs:
        base = f.rsplit(".", 1)[0]
        for suf in ("_feliz", "_fala", "_pisca"):
            if base.endswith(suf):
                grupos.setdefault(base[: -len(suf)], []).append(f)
    trava = set()
    for g, fs in grupos.items():
        tams = set()
        for f in fs:
            try:
                tams.add(Image.open(os.path.join(d, f)).size)
            except Exception:
                pass
        if len(tams) > 1:
            trava.update(fs)
    antes_t, depois_t, n = 0, 0, 0
    for f in arqs:
        c = os.path.join(d, f)
        antes = os.path.getsize(c)
        antes_t += antes
        if f in trava:
            print("   %-28s pulado: camadas do mascote com tamanhos diferentes (arrumar antes)" % f)
            depois_t += antes
            continue
        try:
            im = Image.open(c)
            im.load()
        except Exception as e:
            print("   %-28s nao abriu (%s)" % (f, e))
            depois_t += antes
            continue
        w, h = im.size
        alvo = alvo_de(f)
        esc = min(1.0, alvo / float(max(w, h)))
        novo = im
        if esc < 0.97:
            novo = im.resize((max(1, int(round(w * esc))), max(1, int(round(h * esc)))), Image.LANCZOS)
        buf = io.BytesIO()
        ext = f.lower().rsplit(".", 1)[1]
        if ext == "png":
            novo.save(buf, "PNG", optimize=True)
        else:
            novo.convert("RGB").save(buf, "JPEG", quality=82, optimize=True, progressive=True)
        depois = len(buf.getvalue())
        if depois >= antes * 0.92:
            depois_t += antes
            continue
        n += 1
        depois_t += depois
        print("   %-28s %4dx%-4d -> %4dx%-4d  %5d KB -> %5d KB  (-%d%%)"
              % (f, w, h, novo.size[0], novo.size[1], antes / 1024, depois / 1024, 100 - depois * 100 // antes))
        if aplicar:
            io.open(c, "wb").write(buf.getvalue())
    print("%s -> %d imagem(ns) %s: %d KB -> %d KB (-%d%%)"
          % (pasta, n, "regravada(s)" if aplicar else "a regravar (rode com --aplicar)",
             antes_t / 1024, depois_t / 1024, (100 - depois_t * 100 // antes_t) if antes_t else 0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
