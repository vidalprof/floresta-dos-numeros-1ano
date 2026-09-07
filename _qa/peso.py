# -*- coding: utf-8 -*-
u"""
PORTÃO DE PESO — o orçamento de desempenho da atividade (`_padrao/DESIGN.md` §8)

Ordem do Marcos (2026-09-07): apps "leves, como os das grandes empresas". Leve não é
opinião, é número: quanto a criança baixa antes de jogar, na rede da escola. Este
portão mede o index (bruto e comprimido, que é o que a rede transporta), as imagens
(total, quantas, a maior) e o áudio (que o motor carrega por demanda), e diz o que
otimizar primeiro.

Limites (medidos em 2026-09-07 nas 6 atividades no ar: index gz 134–226 KB, imagens
2–12 MB, maior imagem 177–756 KB):
  · index comprimido  > 300 KB   REPROVA   (aviso acima de 220 KB)
  · uma imagem        > 900 KB   REPROVA   (aviso acima de 400 KB)
  · imagens no total  > 15 MB    REPROVA   (aviso acima de 6 MB)
Uso: python3 _qa/peso.py <pasta>      (0 ok · 1 reprovou · 2 não mediu)
"""
import gzip, io, os, sys

LIM = dict(gz_rep=300, gz_av=220, img1_rep=900, img1_av=400, imgs_rep=15 * 1024, imgs_av=6 * 1024)


def kb(n):
    return n / 1024.0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    if os.path.isfile(pasta):
        pasta = os.path.dirname(pasta) or "."
    idx = os.path.join(pasta, "index.html")
    if not os.path.exists(idx):
        print("%s -> NAO MEDI: sem index.html" % pasta)
        return 2
    bruto = os.path.getsize(idx)
    gz = len(gzip.compress(io.open(idx, "rb").read(), 6))
    imgs = []
    dimg = os.path.join(pasta, "img")
    if os.path.isdir(dimg):
        for f in os.listdir(dimg):
            c = os.path.join(dimg, f)
            if os.path.isfile(c):
                imgs.append((os.path.getsize(c), f))
    imgs.sort(reverse=True)
    tot_img = sum(s for s, _ in imgs)
    daud = os.path.join(pasta, "audio")
    tot_aud = sum(os.path.getsize(os.path.join(daud, f)) for f in os.listdir(daud)) if os.path.isdir(daud) else 0
    print("%s -> index %d KB (comprimido %d KB) | imagens %d KB em %d arquivo(s), maior %d KB | audio %d KB (por demanda)"
          % (pasta, kb(bruto), kb(gz), kb(tot_img), len(imgs), kb(imgs[0][0]) if imgs else 0, kb(tot_aud)))
    rep, av = [], []
    if kb(gz) > LIM["gz_rep"]:
        rep.append("index comprimido %d KB > %d KB" % (kb(gz), LIM["gz_rep"]))
    elif kb(gz) > LIM["gz_av"]:
        av.append("index comprimido %d KB (alvo <= %d KB)" % (kb(gz), LIM["gz_av"]))
    for s, f in imgs[:8]:
        if kb(s) > LIM["img1_rep"]:
            rep.append("imagem %s com %d KB > %d KB" % (f, kb(s), LIM["img1_rep"]))
        elif kb(s) > LIM["img1_av"]:
            av.append("imagem %s com %d KB (alvo <= %d KB)" % (f, kb(s), LIM["img1_av"]))
    if kb(tot_img) > LIM["imgs_rep"]:
        rep.append("imagens somam %d MB > %d MB" % (kb(tot_img) / 1024, LIM["imgs_rep"] / 1024))
    elif kb(tot_img) > LIM["imgs_av"]:
        av.append("imagens somam %.1f MB (alvo <= %d MB)" % (kb(tot_img) / 1024, LIM["imgs_av"] / 1024))
    # o que otimizar primeiro
    try:
        from PIL import Image
        dicas = []
        for s, f in imgs[:5]:
            if kb(s) < 150:
                continue
            try:
                im = Image.open(os.path.join(dimg, f))
                w, h = im.size
                alvo = 1024 if "fundo" in f or "cena" in f else 512
                if max(w, h) > alvo * 1.3:
                    dicas.append("      %s: %dx%d, %d KB -> reduzir para ~%d px no lado maior" % (f, w, h, kb(s), alvo))
                else:
                    dicas.append("      %s: %dx%d, %d KB -> recomprimir (PNG com paleta ou WebP)" % (f, w, h, kb(s)))
            except Exception:
                pass
        if dicas:
            print("   o que otimizar primeiro:")
            for d in dicas:
                print(d)
    except Exception:
        pass
    for a in av:
        print("   aviso: %s" % a)
    if rep:
        print("   %d ESTOURO(S) DO ORCAMENTO:" % len(rep))
        for r in rep:
            print("    - %s" % r)
        return 1
    print("   peso ok: dentro do orcamento (%s)" % ("com avisos" if av else "sem avisos"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
