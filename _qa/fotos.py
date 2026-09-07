# -*- coding: utf-8 -*-
u"""PORTAO 5c — FOTOS: o que a crianca VE, jogando, comparado com a ultima versao aprovada.

Por que existe (set/2026): o pilar verde. A barrinha da peca virou `static`, o
preenchimento passou a medir a tela inteira e crescia a cada letra colocada — e
NENHUM portao viu, porque todos mediam a fase no comeco (progresso 0). O Marcos viu
no celular. A unica coisa que enxerga um defeito que so aparece jogando e uma FOTO
tirada jogando, comparada com a foto de antes.

Como funciona:
  · o `jogador.js` (com QA_FOTOS=_qa/_fotos/<pasta>) tira ate 3 fotos por fase —
    inicio, meio, fim — com o acaso semeado e as animacoes congeladas no clique;
  · este portao compara cada foto com `_qa/_fotos_ok/<pasta>/<mesmo nome>.png`
    (a versao APROVADA, guardada em 206x410 para nao pesar o repo);
  · diferenca > LIMIAR% dos pixels = REPROVA, e sai um contato-folha
    `_qa/_dossie/fotos-<pasta>.png` com ANTES | DEPOIS | DIFERENCA de cada uma;
  · fase sem foto aprovada = ESTREIA: a foto de agora vira a aprovada (aviso, 0) —
    e por isso a estreia pede OLHAR o contato-folha `_qa/_dossie/fotos-<pasta>-estreia.png`.

Codigos: 0 passou · 1 REPROVOU · 2 nao consegui medir (sem fotos novas).
Uso:  python3 _qa/fotos.py <pasta> [--aprovar]      (--aprovar: a versao de agora
      passa a ser a aprovada — SO depois de olhar o contato-folha e concordar)
"""
import io, os, sys, glob, json
from PIL import Image, ImageChops, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIAR = 1.5          # % de pixels diferentes que reprova
TOL = 40              # diferenca minima por canal para contar o pixel
MINI = (206, 410)     # tamanho guardado da foto aprovada (celular 412x820 / 2)
JPGQ = 78             # aprovada em JPEG: 94 fotos = ~1,5 MB (em PNG eram 9,4 MB por atividade)


def carrega(p):
    return Image.open(p).convert("RGB").resize(MINI, Image.LANCZOS)


def diferenca(a, b):
    d = ImageChops.difference(a, b).convert("L")
    # pixel conta se algum canal passou de TOL: usa o maximo dos canais
    da = ImageChops.difference(a, b)
    m = Image.merge("RGB", [ch.point(lambda v: 255 if v > TOL else 0) for ch in da.split()])
    mask = m.convert("L").point(lambda v: 255 if v > 0 else 0)
    hist = mask.histogram()
    ruins = sum(hist[1:])
    return 100.0 * ruins / float(MINI[0] * MINI[1]), mask


def contato(linhas, dest, titulo):
    if not linhas: return
    w = MINI[0]; h = MINI[1]; pad = 8; cab = 26
    W = pad + 3 * (w + pad); H = cab + len(linhas) * (h + pad + 18)
    folha = Image.new("RGB", (W, H), (245, 240, 230)); dr = ImageDraw.Draw(folha)
    dr.text((pad, 6), titulo, fill=(40, 30, 20))
    y = cab
    for nome, antes, depois, mask, pct in linhas:
        dr.text((pad, y), u"%s  —  %.1f%% diferente   (ANTES | DEPOIS | DIFERENCA)" % (nome, pct), fill=(90, 30, 20))
        y += 16
        if antes: folha.paste(antes, (pad, y))
        folha.paste(depois, (pad + w + pad, y))
        if mask:
            red = Image.new("RGB", MINI, (230, 40, 40)); base = depois.copy().convert("RGB")
            base.paste(red, (0, 0), mask); folha.paste(base, (pad + 2 * (w + pad), y))
        y += h + pad + 2
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    folha.save(dest, optimize=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    pasta = sys.argv[1].rstrip("/"); nome = os.path.basename(pasta)
    aprovar = "--aprovar" in sys.argv
    novas = os.path.join(RAIZ, "_qa", "_fotos", nome)
    ok = os.path.join(RAIZ, "_qa", "_fotos_ok", nome)
    fotos = sorted(glob.glob(os.path.join(novas, "*.png")))
    if not fotos:
        print(u"%s -> fotos: NAO MEDI (nenhuma foto em %s — o jogador rodou com QA_FOTOS?)" % (nome, os.path.relpath(novas, RAIZ)))
        return 2
    os.makedirs(ok, exist_ok=True)
    estreias, reprovadas, iguais, linhas_rep, linhas_est, avisos_meio = [], [], 0, [], [], []
    for f in fotos:
        n = os.path.basename(f)
        depois = carrega(f)
        alvo = os.path.join(ok, n[:-4] + ".jpg")
        if not os.path.exists(alvo) or aprovar:
            depois.save(alvo, quality=JPGQ, optimize=True)
            if not aprovar: estreias.append(n); linhas_est.append((n, None, depois, None, 0.0))
            continue
        antes = Image.open(alvo).convert("RGB")
        if antes.size != MINI: antes = antes.resize(MINI, Image.LANCZOS)
        pct, mask = diferenca(antes, depois)
        # o INICIO da fase e deterministico (semente por fase): limiar estrito.
        # MEIO e FIM dependem do caminho que o jogador tomou (qual par abriu, qual
        # letra colocou): limiar largo — o pilar verde dava 25-42% ali, um par de
        # cartas trocado da 4-8%. As telas fora das fases (capa, cracha) ficam no meio.
        limiar = LIMIAR if n.endswith("-inicio.png") else (3.0 if n.startswith("tela") else 12.0)
        # MEDIDO (Trem, 2 corridas do mesmo codigo): inicio 34/34 iguais, fim 34/34
        # iguais, MEIO 1 diferente com 34% (a memoria estava com outro par aberto).
        # O meio e informacao, nao juiz: entra no contato-folha como aviso.
        if n.endswith("-meio.png") and pct > limiar:
            avisos_meio.append((n, pct)); linhas_rep.append((n, antes, depois, mask, pct)); continue
        if pct > limiar:
            reprovadas.append((n, pct)); linhas_rep.append((n, antes, depois, mask, pct))
        else:
            iguais += 1
    if aprovar:
        print(u"%s -> fotos: %d foto(s) de agora passaram a ser as APROVADAS" % (nome, len(fotos)))
        return 0
    print(u"%s -> fotos: %d comparada(s), %d igual(is), %d estreia(s), %d diferente(s) (limiar %.1f%%)"
          % (nome, len(fotos), iguais, len(estreias), len(reprovadas), LIMIAR))
    if estreias:
        dest = os.path.join(RAIZ, "_qa", "_dossie", "fotos-%s-estreia.png" % nome)
        contato(linhas_est, dest, u"ESTREIA %s — estas fotos viraram as aprovadas; OLHE antes de confiar" % nome)
        print(u"   aviso: %d foto(s) sem versao aprovada viraram a aprovada de agora — olhe %s"
              % (len(estreias), os.path.relpath(dest, RAIZ)))
    if avisos_meio:
        print(u"   aviso: %d foto(s) do MEIO da fase diferentes (o caminho do jogador muda o que esta aberto; nao reprova): %s"
              % (len(avisos_meio), ", ".join("%s %.0f%%" % (n, p) for n, p in avisos_meio[:6])))
    if reprovadas or avisos_meio:
        dest = os.path.join(RAIZ, "_qa", "_dossie", "fotos-%s.png" % nome)
        contato(linhas_rep, dest, u"%s — a tela MUDOU em relacao a versao aprovada" % nome)
    if reprovadas:
        print(u"   %d FOTO(S) DIFERENTES DA VERSAO APROVADA (a crianca ve outra coisa):" % len(reprovadas))
        for n, pct in reprovadas[:12]:
            print(u"    x %-22s %5.1f%% dos pixels" % (n, pct))
        if len(reprovadas) > 12: print(u"    ... e mais %d" % (len(reprovadas) - 12))
        print(u"   veja ANTES | DEPOIS | DIFERENCA em %s" % os.path.relpath(dest, RAIZ))
        print(u"   mudanca INTENCIONAL? python3 _qa/fotos.py %s --aprovar  (depois de olhar)" % nome)
        return 1
    print(u"   fotos ok: o que a crianca ve jogando e o mesmo da versao aprovada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
