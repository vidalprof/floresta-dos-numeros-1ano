#!/usr/bin/env bash
# ============================================================
#  joga_par.sh — o JOGADOR paralelo por SEGMENTO (pedido do Marcos, ago/2026).
#  Divide as fases da atividade em K trechos e joga os K AO MESMO TEMPO.
#  Cada trecho e jogado de verdade (fase a fase); o ultimo exige a MEDALHA.
#  So vale para atividade MONTADA (tem conteudo.json com as fases). Sem ele,
#  quem chama deve cair no jogador serial.
#  Uso: bash _qa/joga_par.sh <index.html> [K]   (K padrao 3)
#  Sai 0 se TODOS os trechos passarem.
# ============================================================
set -uo pipefail
ARQ="${1:?uso: joga_par.sh <index.html> [K]}"; K="${2:-3}"
PASTA="$(dirname "$ARQ")"
N="$(python3 -c "import json,sys;print(len(json.load(open('$PASTA/conteudo.json'))['fases']))" 2>/dev/null || echo 0)"
if [ "$N" -lt 6 ]; then echo "  (poucas/sem fases em conteudo.json — use o jogador serial)"; exit 2; fi
[ "$K" -gt "$N" ] && K="$N"
TMP="$(mktemp -d)"; PIDS=(); LABELS=()
i=0
while [ "$i" -lt "$K" ]; do
  s=$(( i*N/K )); e=$(( (i+1)*N/K ))
  f="$TMP/seg$i.txt"
  if [ "$i" -eq $((K-1)) ]; then
    # ultimo trecho: sem JSTOP -> tem que chegar na MEDALHA
    ( JSTART="$s" node _qa/jogador.js "$ARQ" > "$f" 2>&1; echo $? > "$f.st" ) & 
  else
    ( JSTART="$s" JSTOP="$e" node _qa/jogador.js "$ARQ" > "$f" 2>&1; echo $? > "$f.st" ) &
  fi
  PIDS+=($!); LABELS+=("fases $s..$e")
  i=$((i+1))
done
FALHOU=0
i=0
for pid in "${PIDS[@]}"; do
  wait "$pid" || true
  st="$(cat "$TMP/seg$i.st" 2>/dev/null || echo 1)"
  echo "--- trecho $((i+1))/$K (${LABELS[$i]}) ---"
  tail -3 "$TMP/seg$i.txt"
  [ "$st" != "0" ] && FALHOU=1
  i=$((i+1))
done
rm -rf "$TMP"
if [ "$FALHOU" = "0" ]; then echo ">>> JOGADOR PARALELO: todos os $K trechos passaram."; else echo ">>> JOGADOR PARALELO: algum trecho reprovou."; fi
exit $FALHOU
