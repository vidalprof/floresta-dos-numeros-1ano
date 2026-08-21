#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO CUSTO — "isto ia sair uma a uma?"

Nasceu de uma cobrança do Marcos (ago/2026): *"tem como otimizar as imagens em
cartela para não gastar tanto? Tem até isso registrado nos manuais"*. Tinha
mesmo — MANUAL-MESTRE, "REGRA FIXA": *"SEMPRE tentar gerar em CARTELA... Nunca
gerar pose por pose separada"*. E mesmo assim a cartografia saiu com **45
imagens geradas uma a uma**: ~R$9,00 onde ~R$1,60 bastava, e as peças ainda
saindo cada uma com uma luz.

O manual já dizia. Faltava alguém MEDIR antes de gastar. É o que este portão
faz: roda em cima do lote ANTES de acionar o workflow e reprova quando há peças
recortáveis suficientes para virar cartela.

Uso:  python3 _qa/cartela.py _gerar_imagens.json
Sai com 1 se estiver desperdiçando.
"""
import io
import json
import os
import sys

# a partir daqui uma cartela ja compensa (3 chamadas -> 1)
LIMITE = 3
PRECO = 0.20  # R$ por chamada paga do Gemini (registrado no MANUAL-MESTRE)


# ⚠️ UM CEREBRO SO. A classificacao (cena / edicao / peca) mora no
#    _padrao/cartela.py e e importada aqui. Ter a mesma regra escrita em dois
#    lugares e garantia de que um dia elas discordam — e ja discordaram: numa
#    primeira versao o portao contou 3 pecas e o planejador contou 2.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_padrao"))
from cartela import e_cena, e_edicao  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    lote = json.load(io.open(sys.argv[1], encoding="utf-8"))
    cenas = [x for x in lote if e_cena(x)]
    edicoes = [x for x in lote if not e_cena(x) and e_edicao(x)]
    pecas = [x for x in lote if not e_cena(x) and not e_edicao(x)]
    # ⚠️ ESTE PORTAO SO SABIA CONTAR DINHEIRO DO GEMINI (ago/2026). Com o
    #    credito esgotado, a casa passou a desenhar TUDO pelo caminho gratis
    #    (`gerar-imagens.yml` com `lote=`: Pollinations desenha, o rembg
    #    recorta) — e ali cartela nao economiza nada, porque nao ha chamada
    #    paga. O portao reprovava um lote de 23 pecas prometendo "economia de
    #    R$ 4,00" que nao existia. Quem diz por onde vai e o LOTE, no campo
    #    `modelo`; portao que adivinha o caminho cobra a conta errada.
    gratis = [x for x in pecas if (x.get("modelo") or "").lower() == "pollinations"]
    if gratis and len(gratis) == len(pecas):
        print(u"   custo ok: as %d peca(s) vao pelo caminho GRATIS "
              u"(modelo=pollinations) — cartela nao economiza chamada paga."
              % len(pecas))
        print(u"   ⚠️ mas a IRMANDADE continua valendo: peca gerada uma a uma sai")
        print(u"      com luz e escala diferentes das outras. Olhe a folha de")
        print(u"      conferencia antes de embutir.")
        return 0

    print(u"%s -> %d imagem(ns) no lote" % (sys.argv[1], len(lote)))
    print(u"   %d cena(s) larga(s)  (Pollinations, de graca)" % len(cenas))
    print(u"   %d edicao(oes) do mascote  (uma a uma e o certo aqui)" % len(edicoes))
    print(u"   %d peca(s) recortavel(is)" % len(pecas))

    if len(pecas) < LIMITE:
        print(u"   custo ok: pouca peca solta, cartela nao compensa")
        return 0

    # ⚠️ LICAO PAGA (ago/2026) — O PORTAO CONTAVA UMA FOLHA QUE NAO EXISTE.
    #    Ele fazia `ceil(n/8)` e ignorava o campo `grupo`, que e justamente o
    #    que o PLANEJADOR usa: cada folha e UMA familia de coisas (seis
    #    retratos numa; o mascote noutra), senao a IA obedece o "mesma escala"
    #    e devolve a medalha do tamanho da pessoa. Com o lote do 6o ano ja
    #    planejado do jeito certo — 2 folhas — o portao anunciava "cabem em 1"
    #    e prometia uma economia impossivel. Portao que pede o errado ensina a
    #    desobedecer portao. Agora ele conta por familia, igual ao planejador.
    familias = {}
    for x in pecas:
        familias.setdefault(x.get("grupo", "_solto"), []).append(x)
    cartelas = sum((len(v) + 7) // 8 for v in familias.values())

    if cartelas >= len(pecas):
        print(u"   custo ok: as %d peca(s) estao em %d familia(s) diferentes — "
              u"juntar familia com familia estraga a escala, nao economiza."
              % (len(pecas), len(familias)))
        return 0

    print(u"   !! %d PECA(S) INDO UMA A UMA — cabem em %d cartela(s) (%d familia(s))."
          % (len(pecas), cartelas, len(familias)))
    print(u"      gasto assim: R$ %.2f   |   em cartela: R$ %.2f   (economia R$ %.2f)"
          % (len(pecas) * PRECO, cartelas * PRECO,
             (len(pecas) - cartelas) * PRECO))
    print(u"      e nao e so dinheiro: peca gerada junto sai IRMA das outras")
    print(u"      (mesma luz, mesma escala). Uma a uma, cada uma sai de um jeito.")
    print(u"      conserto:  python3 _padrao/cartela.py plano %s" % sys.argv[1])
    return 1


if __name__ == "__main__":
    sys.exit(main())
