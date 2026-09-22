# -*- coding: utf-8 -*-
u"""
============================================================
 ACHAR A HABILIDADE NO CURRÍCULO DE BLUMENAU — sem inventar

 ⭐ POR QUE ESTE ARQUIVO EXISTE. A regra zero do Marcos é *"nunca chute nunca
    invente"*, e a citação de currículo é **a única coisa que o professor não
    tem como conferir sozinho** sem abrir 440 páginas de PDF. Já custou caro
    nesta casa: na Padaria eu escrevi dois "verbatim" que eu mesmo tinha
    inventado. Por isso o portão `0b9` confere palavra por palavra — e por isso
    existe esta ferramenta, para eu ESCOLHER entre o que está escrito lá, em vez
    de escrever de memória.

 O QUE ELA FAZ
   · procura os termos no `_curriculo/blumenau.txt`;
   · devolve a LINHA DE MARCADOR (`•`) inteira, que é onde moram as habilidades,
     já juntada com as linhas de continuação;
   · e CONFERE cada candidata pela MESMA RÉGUA do portão (minúsculas, sem
     acento, sem pontuação) — o que não passar não aparece.

 ⚠️ O PDF VEM EM DUAS COLUNAS, então a linha seguinte pode ser da coluna
    vizinha. A conferência acima é o que protege: candidata que colou texto de
    outra coluna não existe no documento e é descartada aqui, não no portão.

 ⚠️ E O DOCUMENTO SÓ TRAZ CABEÇALHO POR ANO EM CIÊNCIAS, GEOGRAFIA E HISTÓRIA.
    Língua Portuguesa e Matemática vêm em FAIXAS (1º ao 5º), então aqui o ano
    aparece como "faixa" e quem decide se cabe naquele ano é o pedagogo — não
    esta ferramenta.

 Uso:
   python3 _curriculo/achar_habilidade.py "adição" "subtração"
   python3 _curriculo/achar_habilidade.py --bloco "CIÊNCIAS|4"
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(AQUI, u"blumenau.txt")

_CABEC = re.compile(u"^\\s*([A-Za-zÁÉÍÓÚÂÊÔÃÕÇáéíóúâêôãõç ]{4,40}?)\\s*[–—-]\\s*"
                    u"ANOS\\s+(?:INICIAIS|FINAIS)\\s*[–—-]\\s*(\\d)\\s*[ºo]?\\s*ANO\\s*$")


def achata(s):
    s = unicodedata.normalize(u"NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != u"Mn")
    return re.sub(r"[^a-z0-9]+", u" ", s.lower())


def habilidades():
    u"""Todas as candidatas do documento, cada uma com o bloco em que ela mora.

    Uma habilidade começa num marcador `•` e segue pelas linhas seguintes até a
    próxima que seja marcador, cabeçalho de página ou linha em CAIXA ALTA."""
    linhas = io.open(DOC, encoding=u"utf-8").read().split(u"\n")
    plano = achata(u"\n".join(linhas))
    fora = []
    valendo, atual, bloco_de = None, None, None
    for ln in linhas:
        m = _CABEC.match(ln.strip())
        if m:
            valendo = u"%s|%sº ano" % (m.group(1).strip(), m.group(2))
            continue
        mb = re.search(u"•\\s+(.+)$", ln)
        if mb:
            if atual:
                fora.append((atual.strip(), bloco_de))
            atual, bloco_de = mb.group(1).strip(), valendo or u"faixa"
        elif atual is not None:
            r = ln.strip()
            if not r or re.match(u"^(CURRÍCULO|S E M E D|\\d+$)", r) \
                     or re.match(u"^[A-ZÀ-Ý ]{6,}$", r):
                fora.append((atual.strip(), bloco_de))
                atual = None
            else:
                atual += u" " + r
    if atual:
        fora.append((atual.strip(), bloco_de))
    # ⚠️ so sobrevive o que EXISTE no documento pela regua do portao
    return [(h, b) for h, b in fora
            if 30 < len(h) < 420 and achata(h).strip() in plano]


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2
    todas = habilidades()
    if args[0] == u"--bloco":
        alvo = args[1] if len(args) > 1 else u""
        achadas = [(h, b) for h, b in todas if b and alvo.lower() in b.lower()]
    else:
        termos = [achata(a).strip() for a in args]
        achadas = [(h, b) for h, b in todas
                   if all(t in achata(h) for t in termos)]
    print(u"%d habilidade(s) do documento casam (de %d candidatas conferidas)\n"
          % (len(achadas), len(todas)))
    for h, b in achadas[:40]:
        print(u"[%s]" % (b or u"faixa"))
        print(u"   %s\n" % h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
