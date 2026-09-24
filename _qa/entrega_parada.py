# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 0x — TEM ENTREGA PARADA NO MEIO?

 ⭐ ORDEM DO MARCOS (24/set/2026): ***"esses erros nao podem acontecer"*** — e
    ele lembrou, com razao, que **ja tinha mencionado antes**. A regra da casa
    diz: *"toda vez que um defeito escapar ate o Marcos, o conserto tem DUAS
    partes: arrumar o codigo E criar/estender o portao que o pega sozinho"*. O
    que faltava era a segunda parte, e faltou tres vezes no mesmo dia.

 O QUE ACONTECIA, e nao era nenhum dos defeitos em si:
 o carimbo `_status/entrega-<repo>.json` nasce `"estado":"rodando"` no comeco da
 corrida e so e reescrito NO FIM. Corrida que morre no meio — um portao
 reprovando, um `bash -e` derrubando um passo — deixa o carimbo **"rodando"
 para sempre**. Quem o le conclui *"ainda esta publicando"* e espera uma corrida
 que ja morreu. Em 24/set isso aconteceu com os dois cadernos do 3o ano, com o
 caderno da divisao e com a PROVA de Ed. Fisica, e nas quatro vezes eu so
 descobri indo cavar o log do Actions — que e caro de ler e por isso eu nao lia.

 O CONSERTO TEM DOIS LADOS, e este arquivo e o desta beirada:
   · no `entregar.yml`, um passo `if: failure()` reescreve todo carimbo ainda
     "rodando" como `"estado":"falhou"`, com o endereco da corrida e o motivo;
   · AQUI, um portao que le os carimbos e **reprova** se houver entrega parada.
     Ele roda no pre-voo, entao eu esbarro nele antes de qualquer entrega nova,
     sem depender de lembrar.

 ⚠️ E ELE CONTA O RELOGIO, porque "rodando" tambem e o estado LEGITIMO de uma
    corrida que esta mesmo acontecendo agora. Uma entrega leva 3 a 25 minutos
    (o passo caro e ouvir a voz: 16min30 medidos em 11/set com nove alvos).
    Abaixo de MADURA a saida diz "esta rodando AGORA" e devolve 0; acima,
    reprova. ⚠️ PALPITE DECLARADO: os 45 minutos nao saem de medida de
    distribuicao, saem de 25 min medidos + folga — remedir se a corrida crescer.

 Uso:  python3 _qa/entrega_parada.py [--minutos 45]
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import datetime
import io
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(AQUI, u"_status")

MADURA = 45          # minutos — ver o PALPITE DECLARADO no topo


def agora():
    return datetime.datetime.utcnow()


def quando(t):
    for f in (u"%Y-%m-%dT%H:%M:%SZ", u"%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.datetime.strptime(t, f)
        except Exception:                                        # noqa: BLE001
            pass
    return None


def main():
    lim = MADURA
    if u"--minutos" in sys.argv:
        lim = int(sys.argv[sys.argv.index(u"--minutos") + 1])
    if not os.path.isdir(STATUS):
        print(u"NAO MEDI: nao achei a pasta _status.")
        return 2

    falhou, presas, andando, lidos = [], [], [], 0
    for f in sorted(os.listdir(STATUS)):
        if not (f.startswith(u"entrega-") and f.endswith(u".json")):
            continue
        try:
            d = json.load(io.open(os.path.join(STATUS, f), encoding=u"utf-8"))
        except Exception:                                        # noqa: BLE001
            continue
        lidos += 1
        est = d.get(u"estado")
        if est == u"falhou":
            falhou.append(d)
        elif est == u"rodando":
            t = quando(d.get(u"quando") or u"")
            mins = None if t is None else int((agora() - t).total_seconds() // 60)
            (presas if (mins is None or mins > lim) else andando).append((d, mins))

    print(u"entregas: %d carimbo(s) lido(s)" % lidos)
    print(u"   PALPITE DECLARADO: corrida com mais de %d min em \"rodando\" esta "
          u"parada (25 min medidos + folga, nao distribuicao)." % lim)
    for d, m in andando:
        print(u"   · %s esta rodando AGORA (ha %s min) — isso e normal"
              % (d.get(u"destino"), m))
    if not falhou and not presas:
        print(u"   ok: nenhuma entrega parada no meio.")
        return 0

    for d in falhou:
        print(u"   x %-30s A CORRIDA FALHOU: %s"
              % (d.get(u"destino"), d.get(u"motivo") or u"(sem motivo)"))
        if d.get(u"corrida"):
            print(u"        %s" % d[u"corrida"])
    for d, m in presas:
        print(u"   x %-30s carimbo parado em \"rodando\" ha %s min — a corrida "
              u"morreu sem contar" % (d.get(u"destino"),
                                      u"?" if m is None else m))
    cam = os.path.join(STATUS, u"FALHA-ENTREGA.json")
    if os.path.exists(cam):
        try:
            F = json.load(io.open(cam, encoding=u"utf-8"))
            print(u"   ⚠️ o ultimo portao pre-entrega reprovou em %s:"
                  % F.get(u"quando"))
            for lin in (F.get(u"motivo") or u"").strip().split(u"; "):
                if lin.strip():
                    print(u"        %s" % lin.strip())
        except Exception:                                        # noqa: BLE001
            pass
    print(u"   conserto: abrir o motivo acima, arrumar, e rodar o entregar.yml "
          u"de novo para aquele alvo. O carimbo so volta a ficar limpo quando a "
          u"corrida chegar ao fim e conferir o sha no ar.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
