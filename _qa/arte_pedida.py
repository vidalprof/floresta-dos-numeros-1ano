# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a arte que a atividade pede foi mesmo desenhada?"

 ⚠️ LIÇÃO PAGA (ago/2026), e das que custariam a manhã do Marcos.
 Montei a atividade de teste do esqueleto e o montador anunciou, satisfeito:
 *"0 figura(s): 0 já no banco, 0 a gerar"*. Logo depois, a banca achou **DEZ
 imagens que não carregam** — as três camadas do mascote, os seis crachás e a
 medalha. Ou seja: o `arte.json`, que é a LISTA DE COMPRAS da atividade, vinha
 VAZIA, porque o montador só olhava o formato antigo (`itens`/`opcoes`) e nunca
 a arte que o próprio MOTOR exige em toda atividade.

 O estrago que isso faria: quem montasse uma atividade de manhã geraria as
 figuras das fases (que o `arte.json` listasse), publicaria, e a criança abriria
 o app com o mascote, as figurinhas de crachá e a medalha em quadradinho vazio.
 Nada acusaria antes — nem `node --check`, nem print, porque o HTML está certo:
 a figura simplesmente não existe.

 O conserto do montador é uma parte. A outra é esta: um portão que compara a
 LISTA DE COMPRAS com o que está de fato na pasta `img/`. Ele responde a
 pergunta que ninguém estava fazendo — *"a arte pedida chegou?"* — e é o último
 aviso antes de publicar.

 Diferença para o `_qa/imagens.js`: aquele abre a atividade no navegador e vê o
 que não carrega (é o teste de campo, caro). Este é estático e barato, e pega o
 caso ANTES: a figura nem foi pedida ao gerador. Os dois se completam.

 Uso: python3 _qa/arte_pedida.py <pasta-da-atividade>
============================================================
"""
import io
import json
import os
import sys

EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")


def main():
    pasta = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")
    if not pasta:
        print(u"uso: python3 _qa/arte_pedida.py <pasta-da-atividade>")
        return 2

    cam = os.path.join(pasta, "arte.json")
    if not os.path.exists(cam):
        # atividade escrita à mão (não saiu do esqueleto) não tem lista de
        # compras — e portão que não mede tem que DIZER que não mediu.
        print(u"%s -> sem arte.json (atividade que não saiu do esqueleto). "
              u"Nada a conferir." % pasta)
        return 0

    arte = json.load(io.open(cam, encoding="utf-8"))
    pedidos = arte.get("pedidos") or []
    if not pedidos:
        print(u"%s -> o arte.json esta VAZIO." % pasta)
        print(u"   ⚠️ isto quase nunca esta certo: toda atividade precisa, no minimo,")
        print(u"   das tres camadas do mascote, dos crachas e da medalha. Lista de")
        print(u"   compras vazia foi exatamente o defeito que deixou dez figuras de")
        print(u"   fora sem ninguem perceber.")
        return 1

    dimg = os.path.join(pasta, "img")
    tem = set()
    if os.path.isdir(dimg):
        for n in os.listdir(dimg):
            raiz, ext = os.path.splitext(n)
            if ext.lower() in EXT:
                tem.add(raiz)

    falta = [p for p in pedidos if os.path.splitext(p)[0] not in tem]

    print(u"%s -> %d figura(s) pedida(s), %d na pasta img/"
          % (pasta, len(pedidos), len(tem)))
    if not falta:
        print(u"   arte ok: tudo o que a atividade pede esta desenhado")
        return 0

    print(u"   %d FIGURA(S) PEDIDA(S) QUE NAO EXISTEM (a crianca ve quadradinho vazio):"
          % len(falta))
    for f in falta:
        print(u"    %s" % f)
    print(u"   gere em CARTELA (`python3 _padrao/cartela.py plano`) e depois")
    print(u"   `gerar-imagens.yml` — uma a uma custa ate 6x mais.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
