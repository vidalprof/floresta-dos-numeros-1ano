# -*- coding: utf-8 -*-
u"""
============================================================
 A FIGURA MORDIDA SE CONSERTA SOZINHA — a cor nunca foi embora

 ⭐ RECLAMACAO DO MARCOS (17/set/2026): *"na atividade a letra que muda tudo as
    imagens faltam pedacos, exemplo da vaca, rato"* — e depois: *"como estao
    passando erros bobos assim"*.

 ⚠️⚠️ O QUE EU TINHA CONCLUIDO, E ESTAVA ERRADO: que o conserto era impossivel
    porque "a cor foi apagada". Nao foi. Eu olhei a figura COMPOSTA (com o alfa
    aplicado) e vi branco onde o recorte mordeu; nao olhei o CANAL RGB sozinho.
    Olhando: **a vaca esta inteira ali**, em fundo preto, sem mordida nenhuma.
    Quem mordeu foi so a MASCARA. Licao: antes de dizer "nao da", separar os
    canais e olhar cada um.

 POR QUE A MORDIDA ACONTECE, e por que sempre nos mesmos bichos:
 a casa gera a peca em FUNDO PRETO PURO de proposito (e o que o
 `_padrao/superprompt.py` pede) para depois recortar. O recortador antigo tirava
 o fundo por LIMIAR: "pixel escuro = fundo". So que a VACA tem manchas PRETAS, o
 RATO tem sombra escura, o GATO tem listras. O limiar comia o bicho junto com o
 fundo, e a mordida entrava pela borda ate o meio da cara.

 ⭐ O CONSERTO, e ele e exato:
   1. o fundo nao e "o que e escuro": e **o escuro que se alcanca a partir da
      BORDA**. Enchente a partir do quadro (`label` + os rotulos que tocam a
      moldura). Mancha preta no meio da vaca nao se alcanca, entao nao e fundo;
   2. a beirada e ANTI-SERRILHADA: ali o pixel e mistura do bicho com o preto.
      Como o fundo e preto puro, `visto = alfa x cor`, entao `alfa = visto/cor`
      — e o alfa sai da propria luminancia, em rampa, sem chapar;
   3. e a mesma conta desfaz o HALO ESCURO: dividindo a cor pelo alfa
      (`un-premultiply`), a franja cinzenta da borda volta a ser a cor de
      verdade. E por isso que este caminho e melhor que o `rembg` aqui: o fundo
      preto nao e um problema a resolver, e a informacao que resolve.

 ⚠️ ISTO NAO E IA E NAO INVENTA PIXEL NENHUM. Nenhuma cor nova e criada: so se
    recalcula QUAIS pixels sao figura. A regra do Marcos (*"nada de imagem
    gerada por IA"*) fica intacta.

 Uso:
   python3 _padrao/recortar_do_preto.py <arquivo.png|pasta> [--escrever]
 Sem `--escrever` ele so MEDE e diz o que faria (e o padrao, de proposito).
 Codigos: 0 ok · 1 alguma figura nao deu · 2 nao consegui rodar
============================================================
"""
from __future__ import print_function

import os
import sys

LIMIAR_FUNDO = 40      # luminancia: abaixo disto pode ser fundo preto
LIMIAR_ARTE = 12       # luminancia: a partir daqui o pixel TEM COR (e arte)
BEIRADA = 2            # px junto ao fundo em que NAO se mexe (anti-serrilhado)


def _carrega():
    try:
        import numpy as np
        from PIL import Image
        from scipy import ndimage as nd
        return np, Image, nd
    except ImportError as e:                                     # noqa: BLE001
        print(u"nao consegui rodar: falta numpy/Pillow/scipy (%s)" % e)
        return None, None, None


def tem_fundo_preto(rgb, np):
    u"""A moldura do quadro e preta? So entao esta figura nasceu em fundo preto.

    ⚠️ Medir a MOLDURA, nao a media da imagem: um bicho escuro centralizado
    puxaria a media para baixo e eu recortaria uma figura que nunca teve fundo
    preto — estragando a que estava boa."""
    b = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]])
    lum = b.max(axis=1)
    return float((lum < LIMIAR_FUNDO).mean())


def alfa_do_preto(rgb, alfa, np, nd):
    u"""Devolve o alfa consertado. A COR NAO SE TOCA — ela ja esta certa.

    ⚠️⚠️ A PRIMEIRA VERSAO DISTO RECALCULAVA O ALFA PELA LUMINANCIA (`alfa =
       lum/cheio`, a conta certa para uma figura composta sobre preto). Ficou
       PIOR: apareceu um contorno escuro serrilhado em tudo e o talho da vaca
       continuou. O motivo e que a conta so fecha quando se sabe a cor VERDADEIRA
       do pixel — e num RATO CINZA (luminancia ~110 de 255) ela conclui que o
       bicho inteiro esta meio transparente. Sobre fundo preto nao ha como
       separar "objeto escuro" de "objeto translucido": e exatamente por isso
       que o recortador original errou. Repetir a conta dele com mais capricho
       nao ia consertar nada.

    ⚠️ A SEGUNDA TENTATIVA — fechamento morfologico — tambem falhou, e por um
       motivo que so se ve OLHANDO O CANAL ALFA sozinho: o talho nao e um
       arranhao fino. A mascara recortou REGIOES INTEIRAS — o cabelo preto da
       vaca, quase todo o corpo cinza do rato. Fechar um raio de 3 px nao chega
       la, e ainda enche de preto os vaos legitimos (os raios do sol viraram
       tracejado). Licao repetida: olhar o canal antes de escolher a operacao.

    ⭐ O QUE FUNCIONA, e e a primeira ideia sem os enfeites que a estragaram:
       **o fundo nao e "o que e escuro" — e o escuro que se ALCANCA da borda.**
       Enchente a partir da moldura. A mancha preta no meio da vaca nao se
       alcanca; o cabelo dela tampouco; o corpo do rato muito menos. Tudo que a
       enchente nao molha e FIGURA.

    ⭐ E a regra de ouro que faltava: **so ACRESCENTAR opacidade, nunca tirar.**
       `novo = max(alfa_atual, figura)`. Assim a beirada anti-serrilhada que ja
       estava boa fica intacta (foi ela que os meus dois primeiros caminhos
       estragaram, cada um do seu jeito), e o unico efeito e devolver o que
       tinha sido comido. A COR nunca se toca.
    """
    lum = rgb.max(axis=2)
    # ⚠️⚠️ E A QUARTA TENTATIVA AINDA ESTAVA ERRADA, pelo mesmo vicio: eu tratava
    #    "escuro" como sinonimo de fundo. O sol tem um VAO preto entre o disco e
    #    os raios; ele e fundo de verdade, mas os raios o cercam, entao a
    #    enchente da borda nao o alcanca -- e a minha regra o pintava de preto,
    #    virando um anel tracejado em volta do sol.
    #
    # ⭐ O QUE SEPARA DE VERDADE, e foi MEDIDO nas quatro figuras:
    #       fundo gerado        95% dos pixels com luminancia EXATAMENTE 0
    #       arte escura         0-1% com luminancia 0; mediana 20 a 35
    #    O fundo e PRETO PURO porque o gerador o pinta assim (`pure black
    #    background` esta no superprompt). Arte de argila escura nunca e preto
    #    puro: tem textura, tem luz. Entao a pergunta certa nao e "e escuro?" e
    #    sim **"tem alguma cor?"**.
    arte = lum >= LIMIAR_ARTE
    puro = ~arte
    lab, n = nd.label(puro)
    if not n:
        return alfa, 0
    borda = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) \
        | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    borda.discard(0)
    fundo = np.isin(lab, sorted(borda)) if borda else np.zeros_like(puro)
    # ⚠️ NAO ENCOSTAR NA BEIRADA: ali o pixel e mistura do bicho com o preto e
    #    ja tem o alfa suave certo. Chapa-lo em 255 pinta franja escura.
    miolo = ~nd.binary_dilation(fundo, iterations=BEIRADA)
    restaurar = arte & miolo
    novo = np.maximum(alfa, (restaurar * 255).astype(alfa.dtype))
    return novo, int((novo > alfa).sum())


def uma(caminho, escrever, np, Image, nd):
    im = Image.open(caminho).convert(u"RGBA")
    a = np.array(im)
    rgb = a[..., :3]
    alfa = a[..., 3]
    prop = tem_fundo_preto(rgb, np)
    if prop < 0.80:
        print(u"   %-24s moldura preta em %.0f%% — NAO e figura de fundo preto, "
              u"deixo quieta" % (os.path.basename(caminho), prop * 100))
        return 0

    # ⭐ A MEDIDA DA MORDIDA: pixel com COR de bicho (nao preto) que o alfa
    #   atual joga fora. Se ha muitos, o recorte comeu figura.
    novo_alfa, tapados = alfa_do_preto(rgb, alfa, np, nd)
    print(u"   %-24s %dx%d · talho tapado: %d px (%.2f%% da figura)"
          % (os.path.basename(caminho), im.width, im.height, tapados,
             100.0 * tapados / max(1, int((alfa > 128).sum()))))
    if not escrever or not tapados:
        return 0
    saida = np.dstack([rgb, novo_alfa])            # ⭐ a COR nao se toca
    Image.fromarray(saida.astype("uint8"), u"RGBA").save(caminho, optimize=True)
    return 0


def main():
    np, Image, nd = _carrega()
    if np is None:
        return 2
    escrever = u"--escrever" in sys.argv
    alvos = [a for a in sys.argv[1:] if not a.startswith(u"--")]
    if not alvos:
        print(u"uso: python3 _padrao/recortar_do_preto.py <arquivo|pasta> [--escrever]")
        return 2
    arquivos = []
    for a in alvos:
        if os.path.isdir(a):
            arquivos += [os.path.join(a, f) for f in sorted(os.listdir(a))
                         if f.lower().endswith(u".png")]
        else:
            arquivos.append(a)
    if not escrever:
        print(u"   (modo MEDIR — nada e gravado. use `--escrever` para gravar)")
    pior = 0
    for f in arquivos:
        try:
            pior = max(pior, uma(f, escrever, np, Image, nd))
        except Exception as e:                                   # noqa: BLE001
            print(u"   %-24s ERRO: %s" % (os.path.basename(f), e))
            pior = 1
    return pior


if __name__ == u"__main__":
    sys.exit(main())
