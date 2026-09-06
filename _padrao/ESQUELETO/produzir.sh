#!/usr/bin/env bash
# ============================================================
#  produzir.sh — A ESTEIRA DE UMA CORRIDA SO (do conteudo.json ao AR)
#
#  Nasceu do pedido do Marcos (ago/2026: "preciso entregar atividades mais
#  rapido; reparo nao precisa de banca") e cresceu com o de set/2026: "faca tudo
#  que pedi para deixar tudo mais rapido, moderno, agil, por isso voce fez as
#  pesquisas". O que se perdia de relogio antes: montar aqui, pre-voo ali, banca
#  acola, commit a mao, acionar o workflow no MCP, esperar sem saber. Agora e
#  UM comando, e cada etapa so roda se a anterior passou.
#
#  Uso:
#    bash _padrao/ESQUELETO/produzir.sh <pasta>                    # monta + PRE-VOO (segundos)
#    bash _padrao/ESQUELETO/produzir.sh <pasta> --banca            # + banca inteira (minutos)
#    bash _padrao/ESQUELETO/produzir.sh <pasta> --entregar <repo>  # + banca + commit + push
#                                                                  #   [entregar pasta:repo] + espera o carimbo
#    ... --entregar <repo> --reparo   # ajuste pequeno (texto, cor, um dado): pula a banca
#                                     # inteira — regra da casa; a banca grande e para
#                                     # fase/atividade nova ou mudanca de motor.
#    ... --msg "texto do commit"      # (opcional) a primeira linha vira o assunto; o resto, corpo.
#    ... --msg-arquivo <arq>          # (opcional) mensagem lida de um arquivo (para os trailers).
#
#  O que acontece no --entregar:
#    1. montar -> 2. pre-voo (30 portoes de texto) -> 3. banca inteira (a menos
#    que --reparo) -> 4. portao do catalogo com o DESTINO (a pasta esta no
#    ATIVIDADES.md apontando para ESSE repo?) -> 5. commit da pasta + catalogo +
#    painel, com a marca [entregar pasta:repo] no assunto -> 6. push -> 7. o
#    entregar.yml acorda pela marca, grava a voz que falta, publica e deixa
#    _status/entrega-<repo>.json -> 8. este script espera o carimbo e diz se
#    ficou no ar (noar=1) e se o sha bate com o index.html local.
#
#  ⚠️ NUNCA pula portao: se o pre-voo ou a banca reprovar, para ali (codigo 1) e
#     nada e commitado. "Pode sempre publicar" (Marcos) vale so com a banca 0.
#  Codigos: 0 tudo ok · 1 algum portao reprovou / entrega falhou · 2 uso errado.
# ============================================================
set -uo pipefail
P="${1:-}"; if [ -z "$P" ]; then echo "uso: produzir.sh <pasta> [--banca] [--entregar <repo> [--reparo]] [--msg ... | --msg-arquivo ...]"; exit 2; fi
shift || true
P="${P%/}"
BANCA=0; REPO=""; REPARO=0; MSG=""; MSGARQ=""
while [ $# -gt 0 ]; do
  case "$1" in
    --banca) BANCA=1 ;;
    --entregar) REPO="${2:-}"; shift ;;
    --reparo) REPARO=1 ;;
    --msg) MSG="${2:-}"; shift ;;
    --msg-arquivo) MSGARQ="${2:-}"; shift ;;
    *) echo "opcao desconhecida: $1"; exit 2 ;;
  esac
  shift
done
if [ -n "$REPO" ] && [ "$REPARO" = "0" ]; then BANCA=1; fi
AQUI="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$AQUI"
[ -f "$P/conteudo.json" ] || { echo "nao achei $P/conteudo.json"; exit 2; }
T0=$SECONDS

echo "== 1) MONTAR (conteudo.json -> index.html/falas/arte) =="
python3 _padrao/ESQUELETO/montar.py "$P" || { echo ">> o montador reprovou o conteudo — leia a linha acima."; exit 1; }

echo "== 2) PRE-VOO (30 portoes de texto, segundos) =="
if ! bash _qa/previo.sh "$P"; then
  echo ">> o barato ja pegou. Conserte e rode de novo. Nada foi commitado."; exit 1
fi

if [ "$BANCA" = "1" ]; then
  echo "== 3) BANCA INTEIRA (navegador + jogador) =="
  # ⚠️ o portao 0b7 (invisivel) reprova trabalho nao commitado: a banca precisa
  #    ver o que vai subir. Commit provisorio local, sem push, so da pasta.
  if [ -n "$REPO" ]; then
    git add -A "$P" >/dev/null 2>&1 || true
    if ! git diff --cached --quiet; then git commit -q -m "wip: $P antes da banca" || true; fi
  fi
  if ! bash _qa/auditar.sh "$P/index.html"; then
    echo ">> a banca reprovou. Consertar antes de entregar (o commit provisorio fica local; nada foi ao ar)."; exit 1
  fi
elif [ -n "$REPO" ]; then
  echo "== 3) BANCA PULADA (--reparo: ajuste pequeno; portoes de texto ja passaram) =="
fi

if [ -z "$REPO" ]; then
  echo "== OK em $((SECONDS-T0))s. Para publicar: produzir.sh $P --entregar <repo> =="
  exit 0
fi

echo "== 4) CATALOGO/PAINEL com o destino ($P -> $REPO) =="
python3 _painel/montar_painel.py >/dev/null 2>&1 || true
if ! python3 _qa/catalogo.py "$P" "$REPO"; then
  echo ">> a pasta $P nao esta no ATIVIDADES.md apontando para https://vidalprof.github.io/$REPO/ (ou o painel esta atrasado). Corrija o catalogo e rode de novo."
  exit 1
fi

echo "== 5) COMMIT + PUSH com a marca [entregar $P:$REPO] =="
BR="$(git rev-parse --abbrev-ref HEAD)"
TIT="$(python3 -c "import json,sys;print(json.load(open('$P/conteudo.json',encoding='utf-8')).get('titulo','$P'))" 2>/dev/null || echo "$P")"
git add -A "$P" ATIVIDADES.md _painel/index.html >/dev/null 2>&1 || true
if [ -n "$MSGARQ" ]; then MSG="$(cat "$MSGARQ")"; fi
if [ -z "$MSG" ]; then MSG="$TIT: atualiza e publica"; fi
ASSUNTO="$(printf '%s\n' "$MSG" | head -1)"
CORPO="$(printf '%s\n' "$MSG" | tail -n +2)"
ASSUNTO="$ASSUNTO [entregar $P:$REPO]"
if git diff --cached --quiet && ! git log -1 --pretty=%s | grep -q "^wip: $P antes da banca"; then
  # nada mudou desde o ultimo commit: cria um commit vazio so para carregar a marca
  git commit -q --allow-empty -m "$ASSUNTO" -m "$CORPO" || { echo "commit falhou"; exit 1; }
else
  # junta o wip provisorio (se houve) ao commit final
  if git log -1 --pretty=%s | grep -q "^wip: $P antes da banca"; then git reset -q --soft HEAD~1; git add -A "$P" ATIVIDADES.md _painel/index.html >/dev/null 2>&1 || true; fi
  git commit -q -m "$ASSUNTO" -m "$CORPO" || { echo "commit falhou"; exit 1; }
fi
ANTES="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ok=0; for tent in 1 2 3 4 5; do
  if git push -u origin "$BR" 2>&1 | tail -2; then ok=1; break; fi
  s=$((2**tent)); echo "push falhou; tento de novo em ${s}s"; sleep $s
done
[ "$ok" = "1" ] || { echo ">> push nao foi. O commit esta local; empurre a mao (git push -u origin $BR)."; exit 1; }
echo "   commit: $(git log -1 --pretty=%h) — o entregar.yml acorda sozinho pela marca."

echo "== 6) ESPERANDO O CARIMBO _status/entrega-$REPO.json (ate 25 min) =="
LOCAL_SHA="$(sha1sum "$P/index.html" | cut -c1-12)"
CAR="_status/entrega-$REPO.json"
for i in $(seq 1 75); do
  sleep 20
  git fetch -q origin "$BR" 2>/dev/null || continue
  J="$(git show "origin/$BR:$CAR" 2>/dev/null || true)"
  [ -z "$J" ] && continue
  QUANDO="$(printf '%s' "$J" | python3 -c "import json,sys;print(json.load(sys.stdin).get('quando',''))" 2>/dev/null || true)"
  if [ -n "$QUANDO" ] && [[ "$QUANDO" > "$ANTES" ]]; then
    NOAR="$(printf '%s' "$J" | python3 -c "import json,sys;print(json.load(sys.stdin).get('noar',0))" 2>/dev/null || echo 0)"
    IDX="$(printf '%s' "$J" | python3 -c "import json,sys;print(json.load(sys.stdin).get('index',''))" 2>/dev/null || true)"
    git merge -q --ff-only "origin/$BR" 2>/dev/null || true
    echo "   carimbo: $J"
    if [ "$NOAR" = "1" ] && [ "$IDX" = "$LOCAL_SHA" ]; then
      echo "== NO AR em $((SECONDS-T0))s: https://vidalprof.github.io/$REPO/  (sha $IDX bate com o local) =="; exit 0
    fi
    echo ">> o carimbo chegou mas nao confirma (noar=$NOAR, index=$IDX, local=$LOCAL_SHA). Leia o log do entregar.yml (get_job_logs, tail pequeno)."; exit 1
  fi
done
echo ">> 25 min sem carimbo novo. O workflow pode ter reprovado no portao pre-entrega (nada sobe) ou estar na fila. Conferir: git fetch + $CAR, ou get_job_logs."
exit 1
