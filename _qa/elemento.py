# -*- coding: utf-8 -*-
u"""PORTÃO DO ELEMENTO QUE NÃO EXISTE — `getElementById` de um id que sumiu.

⚠️⚠️ POR QUE ELE EXISTE (16/set/2026, e o defeito foi meu):
   quando a barra de 41 teclas saiu da casa (15/set), eu consertei os SETE
   cadernos que estavam no ar e **esqueci o ESQUELETO**. Ele continuou com
   `abreCruz`, `fechaCruz` e `rolaParaCruz` mexendo em `#teclado` e `#tkDica`,
   que não existem mais em HTML nenhum. Os dois cadernos do 2º ano nasceram
   dele já com isso dentro.

   Hoje é código morto — nada chama aquelas funções lá. Mas a primeira folha de
   DIGITAR que alguém escrever num caderno novo derruba o app **no primeiro
   toque da criança**, com `Cannot set properties of null`. E nada via:
   o `node --check` só olha sintaxe; o `_qa/funcoes.py` só cobra FUNÇÃO que não
   existe; e o `_qa/boot.js` só abre a capa, onde a peça nem é tocada.

   Regra da casa: defeito que chega perto da criança vira portão. Este é o
   portão — e ele pega a família inteira, não o caso.

O QUE ELE MEDE
   Em cada `<pasta>` (ou arquivo `.html`), lê o `index.html` e o `folhas.js` e
   procura todo `document.getElementById("X")` e `querySelector("#X")`.
   Para cada id, confere que existe um `id="X"` no HTML. Não existe? REPROVA.

   ⚠️ Ele NÃO reprova id criado em tempo de execução (`el.id = "X"` ou
   `createElement` com id): esses são procurados no JS também, e valem como
   declaração — senão o portão acusaria inocente, que é pior que portão nenhum.

Uso:  python3 _qa/elemento.py <pasta|arquivo.html>
Códigos: 0 passou · 1 REPROVADO · 2 não consegui medir
"""
from __future__ import print_function

import io
import os
import re
import sys


def mede(alvo):
    alvo = alvo.rstrip("/")
    if alvo.endswith(".html"):
        html_cam, pasta = alvo, os.path.dirname(alvo) or "."
    else:
        html_cam, pasta = os.path.join(alvo, "index.html"), alvo
    if not os.path.exists(html_cam):
        print(u"%s: sem index.html — nada a medir" % alvo)
        return 2

    html = io.open(html_cam, encoding=u"utf-8").read()
    js = html
    cam_js = os.path.join(pasta, "folhas.js")
    if os.path.exists(cam_js):
        js += u"\n" + io.open(cam_js, encoding=u"utf-8").read()

    # os ids que EXISTEM: escritos no HTML, ou postos pelo próprio JS
    tem = set(re.findall(r'\bid\s*=\s*"([^"]+)"', html))
    tem |= set(re.findall(r'\bid\s*=\s*\'([^\']+)\'', html))
    tem |= set(re.findall(r'\.id\s*=\s*"([^"]+)"', js))
    tem |= set(re.findall(r'setAttribute\(\s*"id"\s*,\s*"([^"]+)"', js))

    # os ids que o JS PROCURA
    quer = []
    for m in re.finditer(r'getElementById\(\s*"([^"]+)"\s*\)', js):
        quer.append((m.group(1), m.start()))
    for m in re.finditer(r'querySelector(?:All)?\(\s*"#([A-Za-z][\w-]*)"', js):
        quer.append((m.group(1), m.start()))

    faltam, vistos = [], set()
    for nome, pos in quer:
        if nome in tem or nome in vistos:
            continue
        vistos.add(nome)
        linha = js.count(u"\n", 0, pos) + 1
        faltam.append((nome, linha))

    if faltam:
        print(u"%s -> REPROVADO: %d id(s) que o JS procura e o HTML não tem."
              % (alvo, len(faltam)))
        for nome, linha in faltam[:8]:
            print(u"   x  #%s  (o `getElementById` devolve null e o toque estoura)"
                  % nome)
        print(u"   conserto: ou o elemento volta para o HTML, ou o código que\n"
              u"   mexe nele sai junto. Meio-caminho é uma bomba com prazo: o\n"
              u"   `node --check` passa, a capa abre, e quebra na mão da criança.")
        return 1

    print(u"%s -> elementos ok: os %d id(s) que o JS procura existem no HTML."
          % (alvo, len(set(n for n, _ in quer))))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/elemento.py <pasta|arquivo.html>")
        sys.exit(2)
    sys.exit(mede(sys.argv[1]))
