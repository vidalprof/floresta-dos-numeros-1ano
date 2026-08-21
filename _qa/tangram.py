# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "isto é um TANGRAM de verdade?"

 ⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem desconfiou olhando a tela:
 *"isso é tangram? é assim mesmo? nossa atividade está correta?"*. Não estava.

 Um tangram é UM jogo com SETE peças FIXAS: 2 triângulos grandes, 1 médio,
 2 pequenos, 1 quadrado e 1 paralelogramo — e TODA figura usa AS SETE.
 O "Tangram da Vovó Marta" tinha figuras com 5 e 6 peças, e — pior — figuras
 pedindo 3 triângulos pequenos ou 2/3 quadrados, que NÃO EXISTEM no tangram
 (só há 2 pequenos e 1 quadrado). Era "encaixe de formas", não tangram.

 O QUE ESTE PORTÃO FAZ: lê `var FIGURAS=[...]` do index e, para cada figura,
 confere que o conjunto de peças é EXATAMENTE {gra:2, med:1, peq:2, quad:1,
 par:1} e que a área soma 8 (a área das 7 peças). Não desenha: pega o erro de
 CONTAGEM, que é o que quebra a regra do tangram.

 Uso: python3 _qa/tangram.py _tangram/index.html
============================================================
"""
import io
import math
import os
import re
import sys

SET_CERTO = {"gra": 2, "med": 1, "peq": 2, "quad": 1, "par": 1}
# area de cada peca (unidade de grade): gra=2, med=1, peq=0.5, quad=1, par=1
AREA = {"gra": 2.0, "med": 1.0, "peq": 0.5, "quad": 1.0, "par": 1.0}
AREA_TOTAL = 8.0

# ⭐ GEOMETRIA (ago/2026): replica o `poePeca` do jogo — rotate(ang)+scaleX(-1)
#    em torno do CENTRO da peca — para conferir o LADRILHAMENTO (sem sobra nem
#    sobreposicao). So a contagem nao basta: 7 pecas certas podem se sobrepor.
#    Validado contra "A CAIXA CHEIA"/"O DESAFIO" (area 8, sobreposicao 0).
_PTS = {
    "peq": [(0, 0), (1, 0), (0, 1)],
    "med": [(0, 0), (1.414, 0), (0, 1.414)],
    "gra": [(0, 0), (2, 0), (0, 2)],
    "quad": [(0, 0), (1, 0), (1, 1), (0, 1)],
    "par": [(0, 1), (1, 1), (2, 0), (1, 0)],
}
_WH = {"peq": (1, 1), "med": (1.414, 1.414), "gra": (2, 2), "quad": (1, 1), "par": (2, 1)}


def _poly(f, x, y, ang, esp):
    w, h = _WH[f]
    cx, cy = x + w / 2.0, y + h / 2.0
    th = math.radians(ang)
    ct, st = math.cos(th), math.sin(th)
    out = []
    for (px, py) in _PTS[f]:
        wx, wy = x + px, y + py
        if esp:
            wx = 2 * cx - wx
        dx, dy = wx - cx, wy - cy
        out.append((cx + dx * ct - dy * st, cy + dx * st + dy * ct))
    return out


def _dentro(pt, poly):
    x, y = pt
    dentro = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            dentro = not dentro
        j = i
    return dentro


def ladrilha(vagas):
    u"""devolve (area_coberta, area_sobreposta) por amostragem fina."""
    polys = [_poly(v["f"], v["x"], v["y"], v.get("ang", 0), v.get("esp", 0))
             for v in vagas]
    xs = [p[0] for pl in polys for p in pl]
    ys = [p[1] for pl in polys for p in pl]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    N = 90
    dx, dy = (maxx - minx) / N, (maxy - miny) / N
    cell = dx * dy
    cob = ov = 0
    for i in range(N):
        for j in range(N):
            px, py = minx + (i + .5) * dx, miny + (j + .5) * dy
            c = 0
            for pl in polys:
                if _dentro((px, py), pl):
                    c += 1
            if c >= 1:
                cob += 1
            if c >= 2:
                ov += 1
    return cob * cell, ov * cell


def figuras_do_html(html):
    i = html.find("var FIGURAS=[")
    if i < 0:
        return None
    # fatia ate o proximo 'var ' de topo (as figuras nao tem 'var ' dentro)
    fim = html.find("\nvar ", i + 5)
    blk = html[i:fim if fim > 0 else i + 20000]
    figs = []
    for m in re.finditer(r'nome:"([^"]+)".*?vagas:(\[.*?\])\}', blk, re.S):
        nome = m.group(1)
        vtxt = m.group(2)
        fs = re.findall(r'f:"(\w+)"', vtxt)
        vagas = []
        for vm in re.finditer(
                r'\{f:"(\w+)",x:([-\d.]+),y:([-\d.]+)(?:,ang:([-\d.]+))?(?:,esp:(\d))?\}',
                vtxt):
            vagas.append({"f": vm.group(1), "x": float(vm.group(2)),
                          "y": float(vm.group(3)), "ang": float(vm.group(4) or 0),
                          "esp": int(vm.group(5) or 0)})
        figs.append((nome, fs, vagas))
    return figs


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/tangram.py <index.html do tangram>")
        return 2
    cam = sys.argv[1]
    if os.path.isdir(cam):
        cam = os.path.join(cam, "index.html")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html. NAO MEDI." % cam)
        return 2
    html = io.open(cam, encoding="utf-8").read()
    figs = figuras_do_html(html)
    if not figs:
        print(u"%s -> nao achei `var FIGURAS`. NAO MEDI." % cam)
        return 2

    ruins = []
    for nome, fs, vagas in figs:
        cont = {}
        for f in fs:
            cont[f] = cont.get(f, 0) + 1
        area = sum(AREA.get(f, 0) for f in fs)
        problemas = []
        if cont != SET_CERTO:
            problemas.append(u"peças %s (o tangram usa %s)"
                             % (cont, SET_CERTO))
        if abs(area - AREA_TOTAL) > 1e-6:
            problemas.append(u"área %.2f (tem que ser %.0f)" % (area, AREA_TOTAL))
        # ladrilhamento: so quando a contagem/area ja batem (senao nao faz sentido)
        elif cont == SET_CERTO and vagas:
            cob, ov = ladrilha(vagas)
            if ov > 0.15:
                problemas.append(u"peças se SOBREPÕEM (%.2f de área sobreposta)" % ov)
            if abs(cob - AREA_TOTAL) > 0.4:
                problemas.append(u"a figura tem BURACO/sobra (área coberta %.2f, "
                                 u"esperado ~8)" % cob)
        if problemas:
            ruins.append((nome, problemas))

    print(u"%s -> %d figura(s) conferida(s)" % (cam, len(figs)))
    if not ruins:
        print(u"   tangram ok: toda figura usa as 7 peças certas (2 gra, 1 med, "
              u"2 peq, 1 quad, 1 par)")
        return 0
    print(u"   %d FIGURA(S) QUE NAO SAO TANGRAM DE VERDADE:" % len(ruins))
    for nome, problemas in ruins:
        print(u'    - "%s": %s' % (re.sub(r"&#\d+;", "?", nome), "; ".join(problemas)))
    print(u"   conserto: cada figura tem que ser um arranjo das MESMAS 7 peças "
          u"(2 triângulos grandes, 1 médio, 2 pequenos, 1 quadrado, 1 paralelogramo).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
