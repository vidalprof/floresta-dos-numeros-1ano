#!/usr/bin/env bash
# ============================================================
#  produzir.sh — O CAMINHO RAPIDO (pedido do Marcos, ago/2026:
#  "preciso entregar atividades mais rapido; reparo nao precisa de banca").
#
#  Uso:
#    bash _padrao/ESQUELETO/produzir.sh <pasta>            # monta + reparo (segundos)
#    bash _padrao/ESQUELETO/produzir.sh <pasta> --banca    # + banca inteira (antes de entregar)
#
#  A ideia: no dia a dia voce fica no BARATO (montar + reparo, segundos). So
#  quando a atividade esta pronta para o Marcos ver e que roda a banca inteira,
#  UMA vez. Nunca mais 15 min de banca a cada frase trocada.
# ============================================================
set -uo pipefail
P="${1:-}"; if [ -z "$P" ]; then echo "uso: produzir.sh <pasta> [--banca]"; exit 2; fi
shift || true
BANCA=0; [ "${1:-}" = "--banca" ] && BANCA=1
AQUI="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$AQUI"

echo "== 1) MONTAR (conteudo.json -> index.html/falas/arte) =="
python3 _padrao/ESQUELETO/montar.py "$P" || { echo "montar reprovou o conteudo — leia a linha acima."; exit 1; }

echo "== 2) REPARO (portoes de TEXTO, segundos) =="
if ! bash _qa/auditar.sh --reparo "$P/index.html"; then
  echo ">> o barato ja pegou. Conserte e rode de novo."; exit 1
fi

if [ "$BANCA" = "1" ]; then
  echo "== 3) BANCA INTEIRA (navegador + jogador) =="
  bash _qa/auditar.sh "$P/index.html"; exit $?
else
  echo "== OK no BARATO. Antes de entregar ao Marcos: produzir.sh $P --banca =="
fi
