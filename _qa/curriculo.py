# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR PEDAGOGO — "as contas cabem no ano?"
#  Pergunta do Marcos (ago/2026): "3º ano trabalha ate que tabuada? 5? ou menos?"
#
#  RESPOSTA COM FONTE (Curriculo de Blumenau, _curriculo/blumenau.txt):
#    3º ano  -> "Resolver e elaborar problemas de multiplicacao (POR 2, 3, 4 E 5)
#                com a ideia de adicao de parcelas iguais..."
#    4º ano  -> "(por 2, 3, 4, 5 E 10)"   <- o 10 so entra no ano seguinte
#    3º ano tambem pede: "dobro, metade, TRIPLO e terca parte".
#
#  REGRA QUE ESTE AUDITOR APLICA: numa conta a x b do 3º ano, pelo menos UM dos
#  fatores tem que estar entre 2 e 5 (e a tabuada que a crianca esta aprendendo);
#  o outro fator vai ate 10. "3 x 8" vale (tabuada do 3). "6 x 7" NAO vale.
#
#  Uso: python3 _qa/curriculo.py _doceria/index.html [ano]
# ============================================================
import re, sys

LIMITE = {3: (2, 5), 4: (2, 10), 5: (2, 10)}

arq = sys.argv[1] if len(sys.argv) > 1 else "_doceria/index.html"
ano = int(sys.argv[2]) if len(sys.argv) > 2 else 3
lo, hi = LIMITE.get(ano, (2, 10))

h = open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", h, re.S))

pares = []   # (a, b, de onde veio)

# 1) objetos com b/q (bandejas x quantidade), l/co (linhas x colunas), p/q, n/preco
for chave, campos in [("b", ("b", "q")), ("l", ("l", "co")), ("p", ("p", "q")), ("n", ("n", "preco"))]:
    for m in re.finditer(r"\{%s:(\d+),\s*%s:(\d+)" % campos, js):
        pares.append((int(m.group(1)), int(m.group(2)), "objeto %s x %s" % campos))

# 2) listas de pares [a,b]
for m in re.finditer(r"\[(\d+),(\d+)\]", js):
    pares.append((int(m.group(1)), int(m.group(2)), "lista [a,b]"))

# 3) contas escritas no texto: "3 &#215; 4"
for m in re.finditer(r"(\d+)\s*&#215;\s*(\d+)", js):
    pares.append((int(m.group(1)), int(m.group(2)), "texto a x b"))

# 4) saltos na reta: {p:2,ate:12} -> (ate/p) x p
for m in re.finditer(r"\{p:(\d+),ate:(\d+)", js):
    p, ate = int(m.group(1)), int(m.group(2))
    pares.append((ate // p, p, "salto de %d em %d" % (p, p)))

vistos, fora, maior = set(), [], 0
for a, b, origem in pares:
    if a < 2 or b < 2:
        continue
    k = (a, b)
    if k in vistos:
        continue
    vistos.add(k)
    maior = max(maior, a * b)
    if not (lo <= a <= hi or lo <= b <= hi):
        fora.append((a, b, origem))

print("%s -> %d contas diferentes, %dº ano (tabuada de %d a %d)" % (arq, len(vistos), ano, lo, hi))
print("   maior produto usado: %d" % maior)
if not fora:
    print("   pedagogo aprovou: toda conta tem um fator entre %d e %d" % (lo, hi))
    sys.exit(0)
print("   %d CONTA(S) FORA DO ANO (nenhum fator entre %d e %d):" % (len(fora), lo, hi))
for a, b, origem in sorted(fora):
    print("    %d x %d   (%s)" % (a, b, origem))
sys.exit(1)
