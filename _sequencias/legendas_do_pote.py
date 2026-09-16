# -*- coding: utf-8 -*-
u"""
============================================================
 AS LEGENDAS DO CONTATO-FOLHA SAEM DO CRIVO — nao da minha memoria

 ⭐ ORDEM DO MARCOS (15/set/2026): *"sempre me mostre as atividades que vc
    colheu"*. Quem mostra e o `contato_crivo.py`, e ele le as legendas de um
    `_sequencias/<assunto>.txt`. Este script escreve esse arquivo LENDO a tabela
    "AS N FOLHAS, UMA A UMA" do proprio `POTE-<ASSUNTO>.md` — o crivo ja tem o
    comando VERBATIM e o veredito de cada folha, e reescrever isso a mao seria
    uma segunda lista para desencontrar.

 ⚠️ NADA DE EMOJI NA LEGENDA. A fonte do runner (DejaVu) nao tem os desenhos
    coloridos e eles saem como QUADRADINHOS VAZIOS. Cada estrela/x vira PALAVRA
    entre colchetes: [ESSENCIAL], [OTIMA], [BOA], [OK], [EM PARTE], [FORA].

 Uso:  python3 _sequencias/legendas_do_pote.py <ASSUNTO>
       (ex.: `ponto2` -> le `POTE-PONTO2.md`, escreve `ponto2.txt`)
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# a linha da tabela: | **D01** | comando | verbo | veredito |
_LINHA = re.compile(r"^\|\s*\*{0,2}([A-Za-z]\d\d)\*{0,2}\s*\|(.*?)\|([^|]*)\|([^|]*)\|\s*$",
                    re.M)

_TROCA = [(u"⭐⭐⭐", u"[ESSENCIAL]"), (u"⭐⭐", u"[OTIMA]"), (u"⭐", u"[BOA]"),
          (u"❌", u"[FORA]"), (u"⛔", u"[FORA]"), (u"⚠️", u"[EM PARTE]"),
          (u"⚠", u"[EM PARTE]"), (u"✅", u"[OK]"), (u"×", u"x")]


def limpa(t):
    t = re.sub(r"\*\*|\*|`", u"", t or u"")
    for a, b in _TROCA:
        t = t.replace(a, b)
    # o que a fonte do runner nao desenha nao entra
    t = u"".join(c for c in t if ord(c) < 0x2500 or c in u"—–“”‘’…ºª")
    return re.sub(r"\s+", u" ", t).strip()


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _sequencias/legendas_do_pote.py <assunto>")
        return 2
    assunto = sys.argv[1].strip().lower()
    pote = os.path.join(AQUI, u"POTE-%s.md" % assunto.upper())
    if not os.path.exists(pote):
        print(u"NAO MEDI: nao achei %s" % pote)
        return 2
    s = io.open(pote, encoding=u"utf-8").read()
    saida = []
    for m in _LINHA.finditer(s):
        marca, cmd, _verbo, vered = m.groups()
        v, c = limpa(vered), limpa(cmd)
        txt = v or c
        if c and len(txt) < 100:
            txt = txt + u" | " + c
        saida.append(u"%s|%s" % (marca.lower(), txt[:220]))
    if not saida:
        print(u"NAO MEDI: nao achei a tabela folha-a-folha em %s" % pote)
        return 2
    alvo = os.path.join(AQUI, u"%s.txt" % assunto)
    io.open(alvo, u"w", encoding=u"utf-8").write(u"\n".join(saida) + u"\n")
    print(u"%s: %d legenda(s) escritas do crivo" % (alvo, len(saida)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
