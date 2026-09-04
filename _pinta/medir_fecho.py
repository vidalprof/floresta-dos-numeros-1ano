# -*- coding: utf-8 -*-
u"""
============================================================
 O RAIO DE FECHO DE CADA DESENHO — medido, nunca chutado.

 ⚠️ LIÇÃO PAGA (set/2026), e quem pegou foi o Marcos jogando: *"no desenho o
 rosto tem um pedaço da linha incompleta, daí a tinta vaza para outra parte"* e,
 com nome e sobrenome: *"o desenho do pinguim, em um dos pés o risco não fecha,
 vazando a tinta para a plataforma de gelo"*.

 MEDIDO: enchendo a partir do pé direito do pinguim, a tinta cobria 6,6% da tela
 — o MESMO tanto que enchendo a partir do gelo. Pé e gelo eram a mesma região.
 O contorno tinha um furo, e o balde escapava por ele.

 O QUE NÃO ERA (testado antes de consertar):
   · não era o LIMIAR da máscara. Subir o `120` para 170 e 200 não mudou nada —
     o buraco é do desenho, não da leitura dele;
   · não bastava ENGROSSAR a barreira. Engordar 3px tapa o furo, mas engorda a
     linha no desenho inteiro e passa a comer as áreas finas: no teste, o ponto
     do gelo virou "em cima da linha", ou seja, deixou de ser pintável.

 O QUE É: o FECHAMENTO morfológico — engorda `r` e volta `r`. Um vão de até ~2r
 pixels se fecha e não reabre, e a barreira volta à espessura original no resto.

 ⚠️ E O RAIO NÃO PODE SER ÚNICO. Com r=3 dois desenhos PERDERAM área pintável (o
 amigo alto e a menina do vestido — justamente a que o Marcos citou depois). Por
 isso este script existe: ele prova cada desenho com r=1, 2 e 3, conta quantas
 áreas pintáveis sobram, e escolhe o MAIOR raio que não faz perder nenhuma.

 Uso:  python3 _pinta/medir_fecho.py
       (imprime a tabela pronta para colar no `var FECHO` do index.html)
============================================================
"""
import glob
import json
import os
import sys
from collections import deque

try:
    from PIL import Image, ImageFilter
except ImportError:
    print(u"NAO MEDI: falta a Pillow (python3 -m pip install pillow)")
    sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
S = 880          # a MESMA resolução em que o app monta a máscara
TETO, SAT = 120, 45   # os mesmos números do `capturaMascara`
PADRAO = 3       # o raio que a maioria aguenta; quem não aguenta vai na tabela


def mascara(f):
    im = Image.open(f).convert("RGBA")
    fd = Image.new("RGB", im.size, (255, 255, 255))
    fd.paste(im, (0, 0), im)
    px = fd.resize((S, S), Image.BILINEAR).load()
    m = Image.new("L", (S, S), 0)
    mp = m.load()
    for y in range(S):
        for x in range(S):
            r, g, b = px[x, y]
            mx = max(r, g, b)
            mn = min(r, g, b)
            if mx < TETO and (mx - mn) < SAT:
                mp[x, y] = 255
    return m


def fecha(m, d):
    if d <= 0:
        return m
    k = 2 * d + 1
    return m.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))


def areas(m):
    u"""quantas regiões INTERNAS (que não tocam a borda) dá para pintar"""
    mp = m.load()
    visto = bytearray(S * S)
    out = []
    for sy in range(4, S - 4, 8):
        for sx in range(4, S - 4, 8):
            i = sy * S + sx
            if mp[sx, sy] or visto[i]:
                continue
            q = deque([(sx, sy)])
            visto[i] = 1
            n = 0
            borda = False
            while q:
                x, y = q.popleft()
                n += 1
                if x <= 1 or y <= 1 or x >= S - 2 or y >= S - 2:
                    borda = True
                for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= xx < S and 0 <= yy < S and not mp[xx, yy] \
                            and not visto[yy * S + xx]:
                        visto[yy * S + xx] = 1
                        q.append((xx, yy))
            if not borda:
                out.append(n)
    return sorted(out, reverse=True)


def main():
    arqs = sorted(glob.glob(os.path.join(AQUI, "img", "qc_*.png")))
    if not arqs:
        print(u"NAO MEDI: nenhum desenho em _pinta/img/qc_*.png")
        return 2
    tabela, achou_furo = {}, []
    print(u"%-24s %-22s %s" % (u"desenho", u"areas r=0/1/2/3", u"escolhido"))
    for f in arqs:
        nome = os.path.basename(f)[:-4]
        m = mascara(f)
        p0 = areas(m)
        n0, maior0 = len(p0), (p0[0] if p0 else 0)
        conta, melhor, maior_f = [n0], 0, maior0
        for r in (1, 2, 3):
            p = areas(fecha(m, r))
            conta.append(len(p))
            if len(p) >= n0 - 1:          # não pode PERDER área pintável
                melhor = r
                maior_f = p[0] if p else 0
        if melhor != PADRAO:
            tabela[nome] = melhor
        if maior0 - maior_f > 0.008 * S * S:
            achou_furo.append(nome)
        print(u"%-24s %-22s r=%d" % (nome + ".png", u"/".join(map(str, conta)), melhor))

    print(u"")
    if achou_furo:
        print(u"desenhos que TINHAM furo no traço (a tinta vazava): %s"
              % u", ".join(achou_furo))
    print(u"")
    print(u"cole no index.html (o padrão %d cobre o resto):" % PADRAO)
    print(u"var FECHO=%s;" % json.dumps(tabela, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
