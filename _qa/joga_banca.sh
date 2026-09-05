#!/usr/bin/env bash
# ============================================================
#  O JOGADOR DA BANCA — em TRECHOS, com ARBITRO serial
#
#  ⚡ MEDIDO (set/2026, banca da Bancada da Divisao, 32 fases): o jogador serial
#  levou 215s e era, com o leiaute, o dono do relogio. O `jogador-par.js` joga a
#  atividade em K trechos ao mesmo tempo (a cobaia ja o usa: 84 fases em 6
#  trechos, 70s) — mas a banca nao o adotava por uma lembranca legitima: num
#  container apertado um trecho CAIA por contencao e reprovava atividade
#  impecavel. Portao que reprova por lentidao do proprio auditor e pior que
#  portao nenhum.
#
#  A saida aqui e nao escolher entre rapido e confiavel: os dois, na ordem certa.
#    1. joga em K trechos (rapido). Passou -> acabou, codigo 0.
#    2. reprovou? NAO se confia: o serial (o antigo, o que sempre valeu) joga
#       a atividade inteira e da a palavra final. Reprova de verdade continua
#       reprova; queda por contencao vira aprovacao — e o custo do arbitro so e
#       pago quando algo deu errado.
#  Pior caso = o tempo antigo + o trecho que falhou. Caso comum = um terco.
#
#  K = CPUs - 1 (entre 2 e 4). Atividade sem fases em conteudo.json (escrita a
#  mao) nao tem como partir: vai direto no serial, como sempre foi.
#
#  Uso:  bash _qa/joga_banca.sh <index.html>
# ============================================================
set -uo pipefail
ARQ="${1:?uso: joga_banca.sh <index.html>}"
cd "$(dirname "$0")/.." || exit 2
PASTA="$(dirname "$ARQ")"
N="$(python3 -c "import json;print(len(json.load(open('$PASTA/conteudo.json'))['fases']))" 2>/dev/null || echo 0)"
NCPU=$(nproc 2>/dev/null || echo 2)
K=$((NCPU-1)); [ $K -lt 2 ] && K=2; [ $K -gt 4 ] && K=4
if [ "$N" -lt 6 ]; then
  echo "jogador: $N fase(s) em conteudo.json — jogador serial direto"
  exec node _qa/jogador.js "$ARQ"
fi
echo "jogador: $N fases em $K trechos paralelos (arbitro serial se reprovar)"
T0=$SECONDS
node _qa/jogador-par.js "$ARQ" "$K"; ST=$?
echo "   trechos: codigo $ST em $((SECONDS-T0))s"
if [ "$ST" = "0" ]; then exit 0; fi
echo "--- os trechos reprovaram: o ARBITRO serial joga a atividade inteira ---"
T1=$SECONDS
node _qa/jogador.js "$ARQ"; ST2=$?
echo "   arbitro serial: codigo $ST2 em $((SECONDS-T1))s"
exit $ST2
