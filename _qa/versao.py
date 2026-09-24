# -*- coding: utf-8 -*-
u"""
============================================================
 O CARIMBO DE VERSAO NAO PODE MENTIR — portao e ferramenta ao mesmo tempo

 ⚠️ POR QUE ISTO EXISTE. Numa tarde so (24/set/2026) o Marcos relatou TRES
    vezes um defeito que ja estava consertado, porque o navegador dele servia a
    pagina guardada. Sem um numero a vista, nem ele nem eu tinhamos como saber
    se estavamos falando do mesmo programa — e cada volta dessas custa uma hora.
    Por isso a Oficina de Video passou a mostrar `var VERSAO` na barra de cima.

 ⚠️⚠️ E UM CARIMBO ERRADO E PIOR QUE CARIMBO NENHUM: se ele nao mudar quando o
    arquivo muda, ele vira uma PROVA FALSA de que a pagina esta velha (ou nova),
    e a pessoa passa a nao acreditar nele — que e o mesmo que nao ter.
    Como o numero e o sha do proprio arquivo, basta eu editar e esquecer de
    recalcular para ele mentir. Entao isto aqui faz as duas coisas:

      python3 _qa/versao.py <pasta>            confere (0 bate, 1 mente)
      python3 _qa/versao.py <pasta> --gravar   recalcula e grava

 A conta: sha1 do arquivo COM o campo da versao esvaziado — senao seria um
 gato mordendo o proprio rabo (o numero entra no arquivo e muda o sha).
 Codigos: 0 bate · 1 MENTE · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import datetime
import hashlib
import io
import os
import re
import sys

MARCA = re.compile(u'var VERSAO = "([^"]*)";')


def calcula(texto):
    vazio = MARCA.sub(u'var VERSAO = "";', texto)
    return hashlib.sha1(vazio.encode(u"utf-8")).hexdigest()[:6]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith(u"--")]
    gravar = u"--gravar" in sys.argv
    if not args:
        print(u"uso: python3 _qa/versao.py <pasta> [--gravar]")
        return 2
    alvo = args[0]
    cam = alvo if alvo.endswith(u".html") else os.path.join(alvo, u"index.html")
    if not os.path.exists(cam):
        print(u"versao: NAO MEDI (nao achei %s)" % cam)
        return 2

    txt = io.open(cam, encoding=u"utf-8").read()
    m = MARCA.search(txt)
    if not m:
        print(u"%s -> versao: NAO MEDI (esta pagina nao tem carimbo `var VERSAO`)" % cam)
        return 2

    devia = calcula(txt)
    hoje = datetime.date.today().strftime(u"%d/%m")
    atual = m.group(1)
    tem = atual.split(u"-")[-1] if u"-" in atual else atual

    if tem == devia and not gravar:
        print(u"%s -> versao: o carimbo (%s) bate com o arquivo." % (cam, atual))
        return 0

    novo = hoje + u"-" + devia
    if gravar:
        io.open(cam, u"w", encoding=u"utf-8").write(
            MARCA.sub(u'var VERSAO = "%s";' % novo, txt, count=1))
        print(u"%s -> versao gravada: %s (era %s)" % (cam, novo, atual or u"vazia"))
        return 0

    print(u"%s -> versao: O CARIMBO MENTE" % cam)
    print(u"   na pagina: %s" % (atual or u"(vazio)"))
    print(u"   devia ser: %s" % novo)
    print(u"   conserte com: python3 _qa/versao.py %s --gravar" % alvo)
    return 1


if __name__ == "__main__":
    sys.exit(main())
