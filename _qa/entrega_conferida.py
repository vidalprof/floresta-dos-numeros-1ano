# -*- coding: utf-8 -*-
u"""
============================================================
 CONFERIR UMA ENTREGA — e NAO conseguir confirmar o que nao aconteceu

 ⛔ NASCEU DE UM ERRO MEU, no mesmo dia em que o Marcos disse ***"esses erros
    nao podem acontecer"*** (24/set/2026). Eu disparei tres lotes de entrega,
    li os carimbos e ANUNCIEI "trinta no ar, sha conferido um por um". Nao
    estavam: as corridas tinham comecado havia SEGUNDOS. O que eu li foram os
    carimbos ANTIGOS — de 4, 6 e 19 de setembro — que dizem `"noar":1` porque
    naquele dia a entrega deu certo.

 ⚠️⚠️ E O `index` BATIA. Era essa a defesa que a casa tinha escrito (*"conferir
    o campo `index` contra o sha1 do proprio index.html, nunca so o `noar`"*),
    e ela NAO BASTA: quando a mudanca do dia nao tocou o `index.html` — um
    `curriculo.json` novo, uma figura trocada, o dossie do professor —, o sha
    do carimbo velho bate com o do arquivo de hoje. Duas medidas certas, e a
    conclusao errada.

 ⭐ O QUE FALTAVA E A DATA: **um carimbo mais velho que o disparo nao e prova
    de nada.** E a regra e geral, alem desta casa: *quem confere um trabalho
    tem de olhar se a evidencia e POSTERIOR ao trabalho — senao esta lendo o
    passado e chamando de presente.*

 Esta ferramenta existe para que eu NAO CONSIGA confirmar cedo demais. Ela so
 devolve 0 quando as TRES coisas valem, e diz qual falhou:
   1. o carimbo e mais novo que `--desde` (o instante do disparo);
   2. `"noar":1` (o proprio site respondeu com a versao nova);
   3. `index` == sha1 do `<pasta>/index.html` de agora.

 Uso:
   python3 _qa/entrega_conferida.py --desde 2026-09-24T11:10:00Z \\
       _gincana:a-bancada-da-divisao _central:a-central-de-entregas ...
   (sem `--desde`, exige so as duas ultimas e AVISA que nao olhou a data)
 Codigos: 0 todas conferidas · 1 alguma NAO conferida · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import datetime
import hashlib
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha12(cam):
    try:
        return hashlib.sha1(io.open(cam, u"rb").read()).hexdigest()[:12]
    except Exception:                                            # noqa: BLE001
        return None


def data(t):
    for f in (u"%Y-%m-%dT%H:%M:%SZ", u"%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.datetime.strptime(t, f)
        except Exception:                                        # noqa: BLE001
            pass
    return None


def main():
    args = sys.argv[1:]
    desde = None
    if u"--desde" in args:
        i = args.index(u"--desde")
        desde = data(args[i + 1])
        del args[i:i + 2]
    pares = [a for a in args if u":" in a]
    if not pares:
        print(u"uso: python3 _qa/entrega_conferida.py [--desde <ISO>] "
              u"<pasta:destino> [...]")
        return 2
    if desde is None:
        print(u"⚠️ SEM `--desde`: nao vou olhar a DATA do carimbo, e foi "
              u"exatamente isso que me fez anunciar entrega que nao aconteceu. "
              u"Passe o instante do disparo.")

    ok, ruins = 0, []
    for par in pares:
        pasta, destino = par.split(u":", 1)
        cam = os.path.join(RAIZ, u"_status", u"entrega-%s.json" % destino)
        idx = os.path.join(RAIZ, pasta, u"index.html")
        if not os.path.exists(cam):
            ruins.append((destino, u"nao ha carimbo nenhum — a corrida nao "
                                   u"chegou nem a comecar"))
            continue
        try:
            d = json.load(io.open(cam, encoding=u"utf-8"))
        except Exception as e:                                   # noqa: BLE001
            ruins.append((destino, u"carimbo ilegivel (%s)" % e))
            continue
        q = data(d.get(u"quando") or u"")
        if desde is not None and (q is None or q < desde):
            ruins.append((destino,
                          u"o carimbo e de %s, ANTES do disparo (%s) — e o "
                          u"recado da entrega ANTERIOR, nao desta"
                          % (d.get(u"quando"), desde.strftime(u"%Y-%m-%dT%H:%M:%SZ"))))
            continue
        if d.get(u"estado") == u"rodando":
            ruins.append((destino, u"ainda esta rodando (carimbo de %s)"
                          % d.get(u"quando")))
            continue
        if d.get(u"estado") == u"falhou":
            ruins.append((destino, u"A CORRIDA FALHOU: %s  %s"
                          % (d.get(u"motivo") or u"?", d.get(u"corrida") or u"")))
            continue
        if d.get(u"noar") != 1:
            ruins.append((destino, u"subiu, mas o site ainda servia a versao "
                                   u"velha quando a corrida perguntou"))
            continue
        s = sha12(idx)
        if s is None:
            ruins.append((destino, u"nao achei %s/index.html" % pasta))
            continue
        if d.get(u"index") != s:
            ruins.append((destino, u"o sha nao bate: no ar %s, aqui %s"
                          % (d.get(u"index"), s)))
            continue
        ok += 1

    print(u"entregas conferidas: %d de %d" % (ok, len(pares)))
    for destino, por in ruins:
        print(u"   x %-30s %s" % (destino, por))
    return 0 if not ruins else 1


if __name__ == "__main__":
    sys.exit(main())
