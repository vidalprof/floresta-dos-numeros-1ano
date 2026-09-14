# -*- coding: utf-8 -*-
u"""CARIMBA A VERSAO NO `folhas.js` DE UM CADERNO DE FOLHA VIVA.

⚠️⚠️ POR QUE ISTO EXISTE — 14/set/2026, e o Marcos viu antes de qualquer portao.
   Ele abriu O Armazem do Mesmo Tanto e disse: *"so aparece a faixa de cima mais
   nada"*. E, logo depois, a medida que resolveu o caso: *"no edge abriu no
   chrome nao"*.

   Navegador diferente, mesmo arquivo => o arquivo no ar esta BOM (o carimbo de
   entrega dizia `noar:1` e o mesmo sha do index). O que estava velho era a
   copia guardada no Chrome DELE.

   E por que isso derruba a atividade inteira: no caderno de folha viva o
   `index.html` e so a casca (o cabecalho, a faixa, o estilo). Quem DESENHA as
   folhas e o `folhas.js`. Ele era carregado assim:

       <script src="folhas.js"></script>          <- sem versao nenhuma

   Sem `?v=`, o endereco nunca muda; entao uma copia velha, truncada ou de uma
   publicacao pela metade fica no cache do navegador e ele nunca vai buscar
   outra. Resultado exato: a casca abre, as folhas nao.

   Estavam assim os DEZESSEIS cadernos de folha viva.

Uso:  python3 _padrao/versionar.py <pasta> [<pasta> ...]
      python3 _padrao/versionar.py --todos
"""
from __future__ import print_function
import hashlib
import io
import os
import re
import sys


def sha(cam):
    h = hashlib.sha1()
    h.update(io.open(cam, "rb").read())
    return h.hexdigest()[:10]


def carimba(pasta):
    pasta = pasta.rstrip("/")
    ih, fj = os.path.join(pasta, "index.html"), os.path.join(pasta, "folhas.js")
    if not (os.path.exists(ih) and os.path.exists(fj)):
        return None
    v = sha(fj)
    s = io.open(ih, encoding="utf-8").read()
    novo = re.sub(r'<script src="folhas\.js(\?v=[0-9a-f]+)?"></script>',
                  '<script src="folhas.js?v=%s"></script>' % v, s)
    if novo == s:
        return (pasta, v, False)
    io.open(ih, "w", encoding="utf-8").write(novo)
    return (pasta, v, True)


def main():
    alvos = sys.argv[1:]
    if not alvos:
        print(__doc__.split("Uso:")[-1]); return 2
    if alvos[0] == "--todos":
        alvos = sorted(d for d in os.listdir(".")
                       if os.path.isdir(d) and os.path.exists(os.path.join(d, "folhas.js")))
    n = 0
    for a in alvos:
        r = carimba(a)
        if not r:
            print(u"   %-10s (nao e caderno de folha viva)" % a); continue
        pasta, v, mudou = r
        print(u"   %-10s folhas.js?v=%s %s" % (pasta, v, u"<- carimbado" if mudou else u"(ja estava)"))
        n += 1 if mudou else 0
    print(u"carimbados: %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
