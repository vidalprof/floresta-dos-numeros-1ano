# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1s — O `folhas.js` SOBE COM VERSAO NO ENDERECO?

 ⚠️ NASCEU DE UM DEFEITO QUE CHEGOU AO MARCOS (14/set/2026). Ele abriu O
    Armazem do Mesmo Tanto e viu *"so aparece a faixa de cima mais nada"* —
    e logo depois deu a medida que fechou o caso: *"no edge abriu no chrome
    nao"*. Mesmo arquivo, dois navegadores, um so quebrado: o arquivo no ar
    estava bom (carimbo `noar:1`, mesmo sha), e quem estava velho era a copia
    guardada no Chrome dele.

 POR QUE DERRUBA A ATIVIDADE INTEIRA: no caderno de folha viva o `index.html`
 e so a casca — cabecalho, faixa e estilo. Quem desenha as folhas e o
 `folhas.js`. Carregado sem `?v=`, o endereco nunca muda; entao uma copia
 velha, truncada, ou pega no meio de uma publicacao, fica no cache do
 navegador e ele nunca busca outra. A casca abre; as folhas nao.

 ESTAVAM ASSIM OS DEZESSEIS cadernos de folha viva. Nenhum portao media.

 O QUE ELE MEDE — e sao duas coisas, nao uma:
   1. o `index.html` carrega `folhas.js` COM `?v=`;
   2. e o `?v=` bate com o sha1 do `folhas.js` que esta na pasta AGORA.
      A 2a e a que importa de verdade: sem ela, alguem mexe no `folhas.js`,
      esquece de recarimbar, e o endereco continua o mesmo — o defeito volta
      inteiro, com a versao no lugar fazendo cara de resolvido.

 Conserto: `python3 _padrao/versionar.py <pasta>`

 Uso:  python3 _qa/versao_script.py <pasta> [<pasta> ...]
 Codigo 0 = passou · 1 = REPROVADO · 2 = nao deu para medir.
============================================================
"""
from __future__ import print_function
import hashlib
import io
import os
import re
import sys


def confere(pasta):
    pasta = pasta.rstrip("/")
    ih, fj = os.path.join(pasta, "index.html"), os.path.join(pasta, "folhas.js")
    if not (os.path.exists(ih) and os.path.exists(fj)):
        return 2, [u"   nao e um caderno de folha viva (sem index.html + folhas.js): NAO MEDI"]
    s = io.open(ih, encoding="utf-8").read()
    m = re.search(r'<script src="folhas\.js(\?v=([0-9a-f]+))?"></script>', s)
    if not m:
        return 2, [u"   nao achei o `<script src=\"folhas.js\">` no index.html: NAO MEDI"]
    h = hashlib.sha1(); h.update(io.open(fj, "rb").read())
    certo = h.hexdigest()[:10]
    if not m.group(2):
        return 1, [u"   REPROVADO: o index.html carrega `folhas.js` SEM versao no endereco.",
                   u"      O folhas.js e quem desenha as folhas; sem `?v=` o navegador pode",
                   u"      servir para sempre uma copia velha e a crianca ve so a faixa de cima.",
                   u"      Rode: python3 _padrao/versionar.py %s" % pasta]
    if m.group(2) != certo:
        return 1, [u"   REPROVADO: a versao no endereco esta ATRASADA — `?v=%s`, mas o"
                   u" folhas.js da pasta e `%s`." % (m.group(2), certo),
                   u"      Alguem mexeu no folhas.js e nao recarimbou: o endereco nao mudou,",
                   u"      entao o navegador continua com a copia velha.",
                   u"      Rode: python3 _padrao/versionar.py %s" % pasta]
    return 0, [u"   ✓ folhas.js sobe com versao (`?v=%s`) e ela bate com o arquivo" % certo]


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/versao_script.py <pasta> [<pasta> ...]"); return 2
    pior = 0
    for pasta in sys.argv[1:]:
        c, linhas = confere(pasta)
        print(u"%s -> %s" % (pasta.rstrip("/"),
                             u"OK" if c == 0 else (u"REPROVADO" if c == 1 else u"NAO MEDI")))
        for l in linhas:
            print(l)
        pior = 1 if (pior == 1 or c == 1) else max(pior, c)
    return pior


if __name__ == "__main__":
    sys.exit(main())
