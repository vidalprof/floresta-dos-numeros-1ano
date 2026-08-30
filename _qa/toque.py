# -*- coding: utf-8 -*-
u"""PORTÃO DO TOQUE — "arrastar não funciona no tablet/celular da escola".

Nasceu do erro que MAIS escapou (Marcos, ago/2026): a Feirinha usava mecânicas de
ARRASTAR (classificar, caixa-dinheiro, dominó, reta-numérica...). Elas passam no
`node --check`, no `_qa/falas.py` e no `_qa/dinamicas.py`, e o print fica lindo —
mas no iPhone/iPad o toque briga com o arrasto e a criança NÃO consegue jogar.
Nenhum portão via isso, então o defeito chegava ao professor toda vez.

Este portão reconhece as mecânicas de ARRASTO pelo nome do bloco da peça
(`/* ==== PECA: <nome> ==== */`) e REPROVA — a menos que a atividade tenha sido
CONFERIDA no dispositivo de toque real e liberada com o marcador
`<!-- TOQUE-CONFERIDO -->` no HTML (só se põe depois de testar de verdade).

Uso:  python3 _qa/toque.py <index.html>
"""
import io
import re
import sys

# mecânicas cujo gesto é ARRASTAR (falham no toque sem cuidado especial)
ARRASTO = {
    u"reta-numerica", u"classificar", u"caixa-dinheiro", u"domino", u"ligar",
    u"ordenar", u"arrastar-lugar", u"arrastar-sombra", u"grafico", u"circuito",
    u"quebra-cabeca", u"tangram", u"mapa-conceitual",
}


def mecs_de_arrasto(html):
    u"""devolve as mecânicas de arrasto presentes no HTML (pelos marcadores de peça)."""
    nomes = re.findall(r"/\*\s*====\s*PECA:\s*([\w-]+)\s*====\s*\*/", html)
    return sorted(set(n for n in nomes if n in ARRASTO))


def main():
    if len(sys.argv) < 2:
        print(u"uso: toque.py <index.html>")
        return 2
    html = io.open(sys.argv[1], encoding="utf-8").read()
    if u"TOQUE-CONFERIDO" in html:
        print(u"%s -> toque: liberado (marcador TOQUE-CONFERIDO presente)." % sys.argv[1])
        return 0
    achadas = mecs_de_arrasto(html)
    if not achadas:
        print(u"%s -> toque ok: nenhuma mecânica de arrasto (100%% toque)." % sys.argv[1])
        return 0
    print(u"%s -> %d MECÂNICA(S) DE ARRASTAR (não funcionam no toque da escola):"
          % (sys.argv[1], len(achadas)))
    for m in achadas:
        print(u"    - %s" % m)
    print(u"   Troque por mecânica de TOQUE (contar, escolher, completar, comparar, "
          u"memória, intruso, quem-sou-eu, relâmpago, estimar, base-dez, saltos...).")
    print(u"   Se ESTA atividade foi jogada num tablet/celular REAL e o arrasto "
          u"funcionou, libere pondo <!-- TOQUE-CONFERIDO --> no HTML.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
