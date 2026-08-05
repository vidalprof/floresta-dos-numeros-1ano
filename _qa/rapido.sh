#!/usr/bin/env bash
# ============================================================
#  PRÉ-VOO — os portões RÁPIDOS, para rodar a cada mudança
#
#  A banca inteira leva ~4 minutos porque abre o navegador seis vezes. Rodar ela
#  a cada ajuste é o que fazia a criação demorar: eu descobria um erro de uma
#  linha depois de quatro minutos de espera.
#
#  Aqui estão só os portões de TEXTO — os que não abrem navegador. Levam
#  SEGUNDOS e pegam a maior parte dos defeitos: sintaxe, função que não existe,
#  resto de clone, classe sem CSS, barra que anda para trás, promessa não
#  cumprida, variedade de gestos e narração.
#
#  Regra da casa: `rapido.sh` a cada mudança; `auditar.sh` antes de entregar.
#  Um NÃO substitui o outro — o navegador é quem vê o que a criança vê.
# ============================================================
set -uo pipefail
ARQ="${1:-}"
[ -z "$ARQ" ] && { echo "uso: bash _qa/rapido.sh <arquivo.html>"; exit 2; }
FALHOU=0
echo "--- PRE-VOO: $ARQ"
python3 - "$ARQ" > /tmp/_qa_js.js <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
if node --check /tmp/_qa_js.js >/dev/null 2>&1; then echo "  [1 ] codigo roda"; else
  echo "  [1 ] ERRO DE SINTAXE:"; node --check /tmp/_qa_js.js; FALHOU=1; fi
for par in "funcoes:funcao que nao existe" "clone:resto de clone" "promessa:promessa cumprida" \
           "classes:classe sem CSS" "progressao:barra so para a frente" "padrao:padrao da casa"; do
  g="${par%%:*}"; rot="${par#*:}"
  if out=$(python3 "_qa/$g.py" "$ARQ" 2>&1); then printf "  [ok] %-24s\n" "$rot"
  else printf "  [!!] %-24s\n" "$rot"; echo "$out" | sed 's/^/       /' | tail -8; FALHOU=1; fi
done
if [ -f _lote_falas.json ]; then
  if out=$(python3 _qa/falas.py _lote_falas.json 2>&1); then echo "  [ok] narracao"
  else echo "  [!!] narracao"; echo "$out"|tail -5; FALHOU=1; fi
fi
[ "$FALHOU" = "0" ] && echo "  >>> pre-voo limpo. Falta a banca com navegador (auditar.sh)." \
                    || echo "  >>> conserte antes de gastar 4 minutos na banca."
exit $FALHOU
