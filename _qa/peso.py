# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DO PESO — "o PC da escola aguenta?"

 ⚠️ LIÇÃO PAGA (set/2026), e quem pegou foi o Marcos, com as crianças na frente.
 Ele escreveu: *"atividade oficina das palavras travando na fase 13"*, depois
 *"essa atividade estava lenta, o que aconteceu?"*, e por fim o diagnóstico dele,
 que estava certo: *"me parece que esse modelo de atividade que estamos criando
 ultimamente está gerando muitos problemas, lentidão, travamentos e erros"*.

 Nenhum portão pegava, porque nenhum defeito EXISTIA no código. O `node --check`
 passava, o jogador atravessava a atividade inteira sem um erro de JS, o boot
 levava 160 ms e o contador marcava 60 quadros por segundo — aqui, num container
 com processador de servidor. Na sala de informática, não.

 O QUE ERA, medido: o mascote da Oficina tinha **707x1202 pixels em CADA uma das
 três camadas** (parado, falando, piscando), contra 475x708 do padrão da casa. E
 o motor **cruza as três camadas ~60 vezes por segundo** para o lip-sync — é
 assim que a boca mexe. Ou seja: 2,5 milhões de pixels compostos a cada quadro,
 2,5x o normal, o tempo inteiro, em toda tela da atividade. Num netbook de escola
 isso é a diferença entre fluido e engasgado.

 E não era só ela. A varredura achou o mesmo em cinco outras — o Museu com
 **4,7x** o orçamento (5 MB só de mascote, cruzados 60x/s).

 ⭐ POR QUE UM PORTÃO DE PESO, e não "tomar cuidado ao gerar a arte": porque a
 imagem chega PRONTA da IA, no tamanho que ela quiser, e ninguém olha o tamanho
 — olha-se o desenho. O defeito é invisível no print e invisível no código. Só
 aparece com a criança na frente, que é tarde.

 O que ele cobra:
   1. **MASCOTE** — as três camadas do lip-sync no orçamento da casa
      (475x708 = 336 mil pixels). Aqui a régua é apertada porque este é o único
      desenho que o motor recompõe a cada quadro.
   2. **FUNDO** — a tela de fundo até 1200x900. Ele é desenhado uma vez, então a
      régua é mais folgada; o que importa é o download no PC da escola.
   3. **QUALQUER FIGURA** — nenhuma peça acima de 900 KB. Uma figura sozinha que
      pesa 1,5 MB trava a fase que a usa enquanto a rede não entrega.

 ⚠️ O QUE ELE NÃO MEDE: se o desenho está bonito, se o recorte está limpo, se a
 proporção combina com o Byte. Isso é do Diretor de Arte e do Marcos. Ele mede
 o que dá para medir: se cabe no computador da escola.

 ⚠️ E A CURA NUNCA É ESTICAR: ao reduzir, manter a PROPORÇÃO (reduzir para o
 mesmo ORÇAMENTO DE PIXEL, não para as mesmas medidas) e aplicar a MESMA
 transformação nas três camadas — senão o mascote treme, que é o defeito que o
 `_qa/mascote.py` já cobra. Errei exatamente isso na primeira tentativa: escalei
 707x1202 para 475x708 e achatei o robô.

 Uso:  python3 _qa/peso.py <pasta>          (ex.: _por4)
 Sai 0 se cabe, 1 se há peça pesada demais, 2 se não deu para medir.
============================================================
"""
import glob
import math
import os
import sys

try:
    from PIL import Image
except ImportError:
    Image = None

# 475x708 — o mascote do Tato (_divisao/_gincana), que o Marcos aprovou e que
# roda liso. É a régua, não um chute.
ORCAMENTO_MASCOTE = 475 * 708
FOLGA = 1.35                    # 35% de folga: a régua pega o abuso, não o detalhe
FUNDO_MAX = 1200 * 900
PECA_MAX_KB = 900


def _mede(f):
    im = Image.open(f)
    return im.size[0], im.size[1], os.path.getsize(f) // 1024


def confere(pasta):
    pasta = pasta.rstrip("/")
    if Image is None:
        print(u"NAO MEDI: falta a Pillow (python3 -m pip install pillow)")
        return 2
    img = os.path.join(pasta, "img")
    if not os.path.isdir(img):
        print(u"%s -> sem pasta img/. Nada a conferir." % pasta)
        return 0

    problemas, medidas = [], 0

    # 1. o mascote: as tres camadas do lip-sync
    for f in sorted(glob.glob(os.path.join(img, "*_feliz.png"))):
        base = f[:-len("_feliz.png")]
        camadas = [base + s + ".png" for s in ("_feliz", "_fala", "_pisca")]
        if not all(os.path.exists(c) for c in camadas):
            continue
        medidas += 1
        w, h, kb = _mede(camadas[0])
        if w * h > ORCAMENTO_MASCOTE * FOLGA:
            vezes = (w * h) / float(ORCAMENTO_MASCOTE)
            esc = math.sqrt(ORCAMENTO_MASCOTE / float(w * h))
            problemas.append(
                u"MASCOTE %s: %dx%d (%.1fx o orcamento da casa). O motor cruza as "
                u"TRES camadas ~60x/s para o lip-sync — no PC da escola isso "
                u"engasga. Reduza as tres para %dx%d, com a MESMA transformacao."
                % (os.path.basename(base), w, h, vezes,
                   int(round(w * esc)), int(round(h * esc))))

    # 2. o fundo
    for f in sorted(glob.glob(os.path.join(img, "*fundo*.png")) +
                    glob.glob(os.path.join(img, "*fundo*.jpg"))):
        medidas += 1
        w, h, kb = _mede(f)
        if w * h > FUNDO_MAX:
            problemas.append(u"FUNDO %s: %dx%d (%d KB). Acima de 1200x900 ninguem "
                             u"ve a diferenca e a escola paga o download."
                             % (os.path.basename(f), w, h, kb))

    # 3. qualquer peca grande demais
    for f in sorted(glob.glob(os.path.join(img, "*.png")) +
                    glob.glob(os.path.join(img, "*.jpg"))):
        kb = os.path.getsize(f) // 1024
        if kb > PECA_MAX_KB:
            problemas.append(u"FIGURA %s: %d KB. Uma peca sozinha acima de %d KB "
                             u"trava a fase que a usa enquanto a rede nao entrega."
                             % (os.path.basename(f), kb, PECA_MAX_KB))

    total = sum(os.path.getsize(f) for f in glob.glob(os.path.join(img, "*")))
    print(u"%s -> peso conferido: %d figura(s), %d MB na pasta img/"
          % (pasta, len(glob.glob(os.path.join(img, "*"))), total // 1048576))

    if problemas:
        print(u"   %d PECA(S) PESADA(S) DEMAIS PARA O PC DA ESCOLA:" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1

    if not medidas:
        print(u"   NAO MEDI: nenhum mascote em camadas nem fundo nesta pasta — "
              u"isto nao e \"passou\".")
        return 2
    print(u"   peso ok: mascote no orcamento, fundo no tamanho, nenhuma peca "
          u"grande demais")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/peso.py <pasta>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1]))
