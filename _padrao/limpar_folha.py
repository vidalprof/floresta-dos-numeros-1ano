# -*- coding: utf-8 -*-
u"""
============================================================
 LIMPAR FOLHA — tirar cabeçalho, logotipo, marca-d'água ou etiqueta de uma folha
 de atividade SEM ESTRAGAR O DESENHO.

 ⛔ NASCEU DE UM ERRO MEU (8/set/2026). O Marcos pediu para tirar a etiqueta da
 habilidade da capa da Folha Viva. Eu pintei um RETÂNGULO BRANCO por cima — e o
 retângulo comeu o cabelo do menino que passava atrás. A cobrança dele:
 *"o que não pode acontecer... vc estragou o desenho, tem que remover certinho
 sem afetar"*. Retângulo é a ferramenta errada: a folha não é feita de caixas,
 é feita de traços que se cruzam.

 ⭐ O JEITO CERTO, E É ESTE ARQUIVO: apagar por COMPONENTE CONECTADO.
   1. o traço a remover (a moldura da etiqueta, a linha do "Nome:", o logotipo) é
      um borrão de pixels escuros LIGADOS entre si;
   2. acha-se esse borrão pelo PONTO que o operador indica (`--em x,y`);
   3. dentro da caixa dele, apaga-se tudo o que NÃO faz parte de um traço que
      CONTINUA para fora da caixa — ou seja, o desenho que só passa por ali fica
      intacto, com halo e tudo;
   4. e há trava de segurança: se a caixa achada for grande demais (a semente caiu
      no traço errado e pegou a folha inteira), o programa RECUSA e não grava.

 Uso:
   python3 _padrao/limpar_folha.py <imagem> --em 500,626 [--em x,y ...]
   opções:  --limiar 150     (o que conta como traço escuro)
            --max 400x90     (tamanho máximo aceito para o que vai sair)
            --saida arq.jpg  (padrão: grava por cima, guardando .orig.jpg)
            --folha arq.png  (contato ANTES | DEPOIS para olhar antes de aprovar)

 ⚠️ SEMPRE OLHAR O CONTATO antes de publicar. A máquina garante que nada FORA da
 caixa mudou; quem julga se o resultado ficou bonito é o professor.
============================================================
"""
import io, os, sys

try:
    from PIL import Image, ImageDraw
    import numpy as np
    from scipy import ndimage
except ImportError as e:                                    # pragma: no cover
    sys.stderr.write("faltou biblioteca: %s\n" % e)
    raise SystemExit(2)


def acha_caixa(lab, x, y, max_l, max_a):
    u"""a caixa do traço que passa pelo ponto (x, y). Devolve (X0, X1, Y0, Y1)."""
    L = int(lab[y, x])
    if not L:
        raise SystemExit(u"NAO MEDI: em (%d,%d) nao ha traço escuro. Aponte para cima "
                         u"da linha do que se quer tirar (a borda, nao o vazio)." % (x, y))
    ys, xs = np.where(lab == L)
    X0, X1, Y0, Y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    if (X1 - X0) > max_l or (Y1 - Y0) > max_a:
        raise SystemExit(
            u"RECUSEI: o traço de (%d,%d) tem %dx%d px — maior que o teto %dx%d.\n"
            u"   Isso quase sempre quer dizer que a semente caiu num traço que se liga "
            u"ao desenho (a moldura da folha, por exemplo) e apagaria meia página.\n"
            u"   Aponte para um traço isolado, ou suba o teto com --max LxA se tiver certeza."
            % (x, y, X1 - X0, Y1 - Y0, max_l, max_a))
    return X0, X1, Y0, Y1


def limpa(img, pontos, limiar=150, max_l=400, max_a=120, folga=4):
    a = np.array(img)
    g = np.array(img.convert("L"))
    lab, _ = ndimage.label(g < limiar, structure=np.ones((3, 3)))
    caixas = []
    for (x, y) in pontos:
        X0, X1, Y0, Y1 = acha_caixa(lab, x, y, max_l, max_a)
        X0 -= folga; X1 += folga; Y0 -= folga; Y1 += folga
        cx = (slice(max(0, Y0), Y1 + 1), slice(max(0, X0), X1 + 1))
        fora = lab.copy(); fora[cx] = 0
        externos = list(set(np.unique(fora)) - {0})
        dentro = lab[cx]
        # o que CONTINUA para fora da caixa é desenho: fica (com folga para o halo)
        guarda = ndimage.binary_dilation(np.isin(dentro, externos), np.ones((5, 5)))
        bloco = a[cx].copy(); bloco[~guarda] = [255, 255, 255]; a[cx] = bloco
        caixas.append((X0, X1, Y0, Y1))
    return Image.fromarray(a), caixas


def main(argv):
    if len(argv) < 2:
        raise SystemExit(u"uso: python3 _padrao/limpar_folha.py <imagem> --em x,y [--em x,y] "
                         u"[--limiar 150] [--max 400x120] [--saida arq] [--folha contato.png]")
    arq = argv[1]
    pontos, limiar, max_l, max_a, saida, contato = [], 150, 400, 120, None, None
    i = 2
    while i < len(argv):
        o = argv[i]
        if o == "--em":
            x, y = argv[i + 1].split(","); pontos.append((int(x), int(y))); i += 2
        elif o == "--limiar":
            limiar = int(argv[i + 1]); i += 2
        elif o == "--max":
            max_l, max_a = [int(v) for v in argv[i + 1].lower().split("x")]; i += 2
        elif o == "--saida":
            saida = argv[i + 1]; i += 2
        elif o == "--folha":
            contato = argv[i + 1]; i += 2
        else:
            raise SystemExit(u"opção desconhecida: %s" % o)
    if not pontos:
        raise SystemExit(u"diga O QUE tirar: --em x,y (um ponto em cima do traço)")

    orig = Image.open(arq).convert("RGB")
    novo, caixas = limpa(orig, pontos, limiar, max_l, max_a)

    # ninguém mexe fora das caixas — isto é medido, não prometido
    d = (np.abs(np.array(novo).astype(int) - np.array(orig).astype(int)).sum(axis=2) > 24)
    yy, xx = np.where(d)
    if len(xx):
        for (X0, X1, Y0, Y1) in caixas:
            pass
        dentro_de_alguma = np.zeros_like(d)
        for (X0, X1, Y0, Y1) in caixas:
            dentro_de_alguma[max(0, Y0):Y1 + 1, max(0, X0):X1 + 1] = True
        vazou = int((d & ~dentro_de_alguma).sum())
        if vazou:
            raise SystemExit(u"RECUSEI: %d pixel(s) mudaram FORA das caixas pedidas." % vazou)

    if saida is None:
        saida = arq
        guarda = arq.rsplit(".", 1)[0] + ".orig." + arq.rsplit(".", 1)[1]
        if not os.path.exists(guarda):
            orig.save(guarda, quality=92)
            print(u"   original guardado em %s" % guarda)
    ext = saida.rsplit(".", 1)[-1].lower()
    if ext in ("jpg", "jpeg"):
        novo.save(saida, quality=85, optimize=True, progressive=True)
    else:
        novo.save(saida, optimize=True)

    if contato:
        W = 520
        def mini(im):
            c = im.copy(); c.thumbnail((W, 10000)); return c
        A, B = mini(orig), mini(novo)
        folha = Image.new("RGB", (A.width + B.width + 30, max(A.height, B.height) + 26), "#888")
        folha.paste(A, (10, 20)); folha.paste(B, (A.width + 20, 20))
        ImageDraw.Draw(folha).text((10, 4), "ANTES", fill="white")
        ImageDraw.Draw(folha).text((A.width + 20, 4), "DEPOIS", fill="white")
        folha.save(contato, quality=85)
        print(u"   contato ANTES|DEPOIS: %s" % contato)

    print(u"%s -> %d elemento(s) removido(s); %d pixel(s) alterados, todos dentro das caixas:"
          % (arq, len(caixas), len(xx)))
    for (X0, X1, Y0, Y1) in caixas:
        print(u"     x %d..%d  y %d..%d" % (X0, X1, Y0, Y1))
    print(u"   ⚠️ OLHE o contato antes de publicar: a máquina garante que nada de fora mudou, "
          u"não que ficou bonito.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
