#!/usr/bin/env bash
# ============================================================
#  PRE-VOO — os portoes de TEXTO, em segundos, logo depois do montar.
#
#  Pedido do Marcos (set/2026): *"quero as atividades melhores, mais rapidas e
#  com muito menos erros"*. O relogio da fabrica se perdia assim: montar ->
#  banca inteira (10 min) -> um portao de texto reprova por uma virgula ->
#  consertar -> banca inteira de novo. A banca grande e necessaria (Chromium,
#  jogador, leiaute, contraste), mas ela nao precisa ser a PRIMEIRA a ver o
#  arquivo. Tudo o que e Python puro — sintaxe, funcao que nao existe, resto de
#  clone, duplicata, falas, revisor, dinamicas, padrao, duracao, progressao,
#  beco, promessa, catalogo — roda aqui em PARALELO e responde em segundos.
#
#  Regra: montou -> `bash _qa/previo.sh <pasta>` -> so com 0 aqui e que vale
#  gastar os 10 minutos da banca (`bash _qa/auditar.sh <pasta>/index.html`).
#  ⚠️ Pre-voo 0 NAO e "a banca aprovou": e "nao ha erro barato". A banca
#  continua obrigatoria antes de publicar.
#
#  Codigos: 0 passou · 1 REPROVOU (lista quem) · 2 nao mediu nada.
#  Uso: bash _qa/previo.sh _padaria      (ou _padaria/index.html)
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2
ALVO="${1:-}"
[ -z "$ALVO" ] && { echo "uso: bash _qa/previo.sh <pasta|arquivo.html>"; exit 2; }
if [ -d "$ALVO" ]; then PASTA="${ALVO%/}"; ARQ="$PASTA/index.html"; else ARQ="$ALVO"; PASTA="$(dirname "$ARQ")"; fi
[ -f "$ARQ" ] || { echo "nao achei $ARQ"; exit 2; }

# ⭐ MODO PECA (set/2026): `bash _qa/previo.sh _padrao/pecas/x.html` roda em segundos os
#    portoes de texto que valem para UMA peca — sintaxe, funcao que nao existe,
#    dinamicas, classes, beco, cor cravada, espera. Nasceu no dia em que um
#    `if/else` partido pelo meio por uma edicao passou por mim porque eu so
#    "grepava" a bancada em vez de ler a secao 1. A bancada inteira (`peca.sh`,
#    Chromium) continua obrigatoria antes de guardar a peca no catalogo.
case "$ARQ" in _padrao/pecas/*.html)
  TMP="$(mktemp -d /tmp/previo.XXXXXX)"; T0=$SECONDS
  python3 - "$ARQ" "$TMP/app.js" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
open(sys.argv[2],"w",encoding="utf-8").write("\n".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
  FALHOU=""
  for item in "1a sintaxe|node --check $TMP/app.js" "1b funcao que nao existe|python3 _qa/funcoes.py $ARQ" \
              "0b2 dinamicas|python3 _qa/dinamicas.py $ARQ" "4 classes sem estilo|python3 _qa/classes.py $ARQ" \
              "3b beco na peca|python3 _qa/beco_peca.py $ARQ" "4b cor cravada|python3 _qa/cor_fixa.py $ARQ" \
              "0b3 espera|python3 _qa/espera.py $ARQ"; do
    nome="${item%%|*}"; cmd="${item#*|}"
    out="$(eval "$cmd" 2>&1)"; st=$?
    if [ "$st" != "0" ] && [ "$st" != "2" ]; then FALHOU="$FALHOU
   · $nome (codigo $st)"; echo "--- $nome ---"; echo "$out" | tail -8; fi
  done
  echo "==================================================="
  echo " PRE-VOO DA PECA $ARQ — 7 portoes de texto em $((SECONDS-T0))s"
  rm -rf "$TMP"
  if [ -n "$FALHOU" ]; then echo "   REPROVARAM:$FALHOU"; exit 1; fi
  echo " -> nenhum erro barato. Agora sim: bash _qa/peca.sh $ARQ"; exit 0 ;;
esac

TMP="$(mktemp -d /tmp/previo.XXXXXX)"
T0=$SECONDS

# nome | comando  (os mesmos portoes da banca, os que nao precisam de navegador)
PORTOES=(
  "1a sintaxe|node --check __JS__"
  "1b funcao que nao existe|python3 _qa/funcoes.py $ARQ"
  "1c resto de clone|python3 _qa/clone.py $ARQ"
  "1c2 duplicata igual|python3 _qa/duplicatas.py $ARQ"
  "1g beco sem saida|python3 _qa/beco.py $ARQ"
  "1g2 beco na peca|python3 _qa/beco_peca.py $ARQ"
  "1d promessa|python3 _qa/promessa.py $ARQ"
  "1j voz-robo|python3 _qa/vozrobo.py $ARQ"
  "1m toque|python3 _qa/toque.py $ARQ"
  "0b padrao da casa|python3 _qa/padrao.py $ARQ"
  "0b2 dinamicas|python3 _qa/dinamicas.py $ARQ"
  "0b6 catalogo/painel|python3 _qa/catalogo.py $PASTA"
  "0c pergunta ambigua|python3 _qa/ambiguo.py $ARQ"
  "0d voz da tela|python3 _qa/voztela.py $ARQ"
  "0e tela vazia|python3 _qa/telavazia.py $ARQ"
  "0f voz da pergunta|python3 _qa/vozpergunta.py $ARQ"
  "0i voz sem mp3|python3 _qa/vozfalta.py $ARQ"
  "0j voz da dica|python3 _qa/vozdica.py $ARQ"
  "0j2 acento na grade|python3 _qa/acento.py $PASTA"
  "0o revisor de texto|python3 _qa/revisor.py $PASTA"
  "0o2 resposta entregue|python3 _qa/entrega.py $PASTA"
  "0o3 enunciado bate|python3 _qa/enunciado_bate.py $PASTA"
  "0e texto de exemplo|python3 _qa/exemplo.py $PASTA"
  "0l arte pedida|python3 _qa/arte_pedida.py $PASTA"
  "1i figura combina|python3 _qa/figura_certa.py $PASTA"
  "3b progressao|python3 _qa/progressao.py $ARQ"
  "3f pares da memoria|python3 _qa/memoria_pares.py $PASTA"
  "3g duracao|python3 _qa/duracao.py $PASTA"
  "4c cor cravada|python3 _qa/cor_fixa.py $ARQ"
  "falas (narracao)|python3 _qa/falas.py $PASTA/falas.json"
)

[ -f "$PASTA/falas.json" ] || echo "AVISO: $PASTA nao tem falas.json — a narracao nao tem como ser conferida (criar o arquivo e parte do trabalho)."
# o JS extraido, para o `node --check` (mesmo criterio da banca)
python3 - "$ARQ" "$TMP/app.js" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
open(sys.argv[2],"w",encoding="utf-8").write("\n".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY

i=0
for item in "${PORTOES[@]}"; do
  nome="${item%%|*}"; cmd="${item#*|}"; cmd="${cmd/__JS__/$TMP/app.js}"
  prog="$(echo "$cmd" | awk '{print ($1=="python3")?$2:$1}')"
  # portao que nao existe nesta copia nao e reprovacao: e "nao mediu"
  if [[ "$prog" == _qa/* && ! -f "$prog" ]]; then echo "2" > "$TMP/$i.st"; echo "(nao existe aqui: $prog)" > "$TMP/$i.out"; i=$((i+1)); continue; fi
  ( eval "$cmd" > "$TMP/$i.out" 2>&1; echo $? > "$TMP/$i.st" ) &
  i=$((i+1))
done
wait

REPROVOU=""; CEGO=""; OK=0; NSA=0
i=0
for item in "${PORTOES[@]}"; do
  nome="${item%%|*}"; st="$(cat "$TMP/$i.st" 2>/dev/null || echo 9)"
  if [ "$st" = "0" ]; then OK=$((OK+1))
  elif [ "$st" = "2" ]; then
    if grep -qi "nao se aplica\|nada a conferir\|nao existe aqui\|NAO MEDI: nenhuma\|sem falas.json" "$TMP/$i.out"; then NSA=$((NSA+1)); else CEGO="$CEGO
   · $nome"; fi
  elif [ "$nome" = "0i voz sem mp3" ]; then
    # ⚠️ antes de PUBLICAR e normal faltar mp3: quem grava a voz e o entregar.yml
    #    (lendo o falas.json). Aqui isso e INFORMACAO, nao reprovacao — reprovar
    #    ensinaria a ignorar o pre-voo. Na banca de verdade continua sendo portao.
    GRAVAR="$(grep -c '^    - op_' "$TMP/$i.out" 2>/dev/null || echo ?)"
    echo "   (voz sem mp3 ainda: $GRAVAR — o entregar.yml grava ao publicar; texto ja esta no falas.json)"
  else
    REPROVOU="$REPROVOU
   · $nome (codigo $st)"
    echo "--- $nome ---"; tail -14 "$TMP/$i.out"; echo
  fi
  i=$((i+1))
done

echo "==================================================="
echo " PRE-VOO $ARQ — ${#PORTOES[@]} portao(oes) de texto em $((SECONDS-T0))s"
echo "   passaram: $OK   nao se aplicam: $NSA"
[ -n "$CEGO" ] && echo "   NAO MEDIRAM (rodar na mao, sem 2>/dev/null):$CEGO"
if [ -n "$REPROVOU" ]; then
  echo "   REPROVARAM:$REPROVOU"
  echo " -> consertar ANTES de gastar a banca inteira."
  rm -rf "$TMP"; exit 1
fi
echo " -> nenhum erro barato. Agora sim: bash _qa/auditar.sh $ARQ"
rm -rf "$TMP"; exit 0
