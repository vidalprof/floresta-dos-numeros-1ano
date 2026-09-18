# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 4c4 — "REGRA DE CSS QUE NÃO FECHA": chave `{` sem `}` mata o CSS inteiro
 dali para baixo, EM SILÊNCIO.

 ⚠️ LIÇÃO PAGA — 18/set/2026, `_sinon2` (O Espelho e o Contrário), antes de ir ao ar.
    Ao colar o bloco de CSS das peças, DEZENOVE regras de duas linhas perderam a
    segunda linha: ficaram assim —

        .cpcel{width:clamp(44px,9vw,50px);height:clamp(44px,9vw,50px);min-width:44px;
        .cpcel.pega{background:#fff0c2;border-color:#f5c542}

    O navegador não reclama: ele engole a regra seguinte como se fosse parte da
    anterior, e TODO o CSS dali para baixo morre. O `node --check` não olha CSS; o
    `_qa/classes.py` viu as classes DECLARADAS (elas estavam lá, só não fechavam);
    o `4c3` só conta `@keyframes`. Quem viu foram a FOTO (três folhas sem estilo) e
    o `leiaute_mao` (64 alvos de 21 px). Este portão pega a CAUSA, em segundos.

 O QUE ELE MEDE (reprova, código 1), em cada bloco <style> e em cada `.css` da pasta:
   1. o saldo de chaves, sem comentários e sem strings — tem que dar zero;
   2. toda linha que ABRE uma regra (`seletor{...;`) e termina em `;` sem fechar,
      quando a linha seguinte começa outro seletor / `@` / `}` / fim de bloco —
      é a assinatura exata da linha perdida, e diz a linha e o seletor.

 Uso: python3 _qa/css_fechado.py <arquivo.html | pasta>
============================================================
"""
from __future__ import print_function
import io
import signal
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass
import os
import re
import sys


def sem_comentario(css):
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


def sem_strings(css):
    return re.sub(r"(\"[^\"\n]*\"|'[^'\n]*')", "\"\"", css)


def mede(css, nome, base_linha=1):
    erros = []
    limpo = sem_strings(sem_comentario(css))
    saldo = limpo.count("{") - limpo.count("}")
    if saldo != 0:
        erros.append("%s: saldo de chaves = %+d (tem que ser 0)" % (nome, saldo))
    linhas = limpo.split("\n")
    for i, l in enumerate(linhas):
        t = l.rstrip()
        if "{" not in t or t.endswith("}") or t.endswith("{"):
            continue
        depois = t.split("{", 1)[1]
        if "}" in depois or not t.endswith(";"):
            continue
        prox = ""
        for j in range(i + 1, min(i + 3, len(linhas))):
            if linhas[j].strip():
                prox = linhas[j].strip()
                break
        if not prox:
            continue
        # a linha seguinte e' OUTRA REGRA quando comeca por seletor (. # @ * }) ou,
        # comecando por letra, abre `{` sem nenhum `;` antes (`a:hover{`, `html,body{`).
        # `box-shadow:0 2px 14px;padding:8px}` e' CONTINUACAO (propriedade), nao regra.
        e_regra = prox[0] in ".#@}*" or ("{" in prox and ";" not in prox.split("{", 1)[0] and re.match(r"^[a-zA-Z]", prox))
        if e_regra:
            # a linha seguinte e' um seletor novo: a continuacao desta regra sumiu
            sel = t.split("{", 1)[0].strip()
            erros.append("%s linha %d: `%s{` abre e nao fecha — a linha seguinte ja e outra regra (`%s`)"
                         % (nome, base_linha + i, sel[:60], prox[:50]))
    return erros


def arquivos(alvo):
    if os.path.isdir(alvo):
        out = []
        for f in sorted(os.listdir(alvo)):
            if f.endswith(".html") or f.endswith(".css"):
                out.append(os.path.join(alvo, f))
        return out
    return [alvo]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1].rstrip("/")
    arqs = arquivos(alvo)
    if not arqs:
        print("%s -> NAO MEDI: nenhum .html/.css" % alvo)
        return 2
    erros = []
    blocos = 0
    for cam in arqs:
        try:
            s = io.open(cam, encoding="utf-8").read()
        except IOError:
            continue
        if cam.endswith(".css"):
            blocos += 1
            erros += mede(s, cam)
            continue
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", s, re.S):
            blocos += 1
            base = s[:m.start(1)].count("\n") + 1
            erros += mede(m.group(1), cam, base)
    print("%s -> css fechado: %d bloco(s) de CSS conferido(s)" % (alvo, blocos))
    if blocos == 0:
        print("   NAO MEDI: nenhum <style> nem .css")
        return 2
    if erros:
        print("   REPROVADO — regra de CSS sem fechar mata tudo dali para baixo, em silencio:")
        for e in erros[:40]:
            print("    - " + e)
        if len(erros) > 40:
            print("    ... e mais %d" % (len(erros) - 40))
        print("   conserto: completar a linha perdida (copiar da atividade de origem) ate o `}`.")
        return 1
    print("   ok: toda regra fecha; saldo de chaves zero em todo bloco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
