#!/usr/bin/env bash
# ============================================================================
# COBAIA DO MOTOR — testa TODAS as mecânicas integradas, de uma vez.
#
# Rode DEPOIS de mexer no MOTOR (pecas.js, pecas.css, montar.py, integrar.py):
# ela gera uma atividade-fixture com uma fase de CADA mecânica (modo exemplo),
# monta e roda leiaute (layout/colapso) + jogador-par (joga tudo, erro de JS).
# Assim o defeito "passou na bancada, quebrou integrado" (o pote virando barra,
# o texto de dinheiro na fruta) é pego AQUI, sem depender de sorte.
#
# Uso:  bash _qa/cobaia.sh
# Sai 0 se leiaute E jogador passarem em todas as mecânicas.
# ============================================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2
ARQ="_cobaia/index.html"

echo "===== COBAIA: gerar + montar ====="
python3 _qa/cobaia.py || { echo "cobaia: gerador falhou"; exit 2; }
python3 _padrao/ESQUELETO/montar.py _cobaia >/tmp/cob_montar.txt 2>&1
if ! grep -q "escrito: _cobaia/index.html" /tmp/cob_montar.txt; then
  echo "⛔ cobaia: MONTAR nao gerou o index — o motor quebrou ao montar TODAS as mecanicas:"
  tail -20 /tmp/cob_montar.txt
  exit 1
fi
echo "  montar ok ($(grep -oE '[0-9]+ fase' /tmp/cob_montar.txt | head -1))"

# fases (telas) p/ o leiaute — mesma deteccao do auditar.sh
TELAS=$(python3 - "$ARQ" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
js="".join(re.findall(r"<script>(.*?)</script>",h,re.S))
def fp(t):
    s,i=[],0
    for m in re.finditer(r'MEC\["[a-z0-9\-]+"\]\s*=\s*function',t):
        j=t.find("{",m.end())
        if j<0: continue
        p,k=0,j
        while k<len(t):
            if t[k]=="{":p+=1
            elif t[k]=="}":
                p-=1
                if p==0:break
            k+=1
        s.append(t[i:m.start()]);i=k+1
    s.append(t[i:]);return "".join(s)
js=fp(js);nm=[]
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(",js,re.M):
    n=m.group(1);i=m.end();p=0;j=js.find("{",i);k=j
    while k<len(js):
        if js[k]=="{":p+=1
        elif js[k]=="}":
            p-=1
            if p==0:break
        k+=1
    if "limpa()" in js[j:k]: nm.append(n)
print(" ".join(nm))
PY
)

echo "===== COBAIA: leiaute (6 tamanhos x todas as fases) ====="
node _qa/leiaute.js "$ARQ" $TELAS >/tmp/cob_leiaute.txt 2>/dev/null
LEI=$?
tail -3 /tmp/cob_leiaute.txt
echo "  leiaute exit=$LEI"

echo "===== COBAIA: jogador-par (joga TODAS as mecanicas) ====="
node _qa/jogador-par.js "$ARQ" 6 >/tmp/cob_jogador.txt 2>/dev/null
JOG=$?
tail -8 /tmp/cob_jogador.txt
echo "  jogador exit=$JOG"

echo "===== COBAIA: veredito ====="
if [ "$LEI" = "0" ] && [ "$JOG" = "0" ]; then
  echo "✅ cobaia: o motor passou em TODAS as mecanicas (leiaute + jogador)."
  exit 0
fi
echo "⛔ cobaia: o motor REPROVOU. Veja /tmp/cob_leiaute.txt e /tmp/cob_jogador.txt"
exit 1
