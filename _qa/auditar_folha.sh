#!/usr/bin/env bash
# ============================================================
#  A BANCA DA FOLHA VIVA — a que faltava.
#
#  ⭐ PERGUNTA DO MARCOS (13/set/2026): *"Mas tem banca para esse tipo de
#     atividade?"* — feita depois de eu dizer a ele que a `auditar.sh` tinha
#     REPROVADO o caderno de moradia e que metade das reprovações "não era deste
#     formato". A resposta honesta na hora era **NÃO**.
#
#     O que existia: a banca do MOTOR (`auditar.sh`), que em folha viva reprova
#     ou diz "NÃO MEDI" em meia dúzia de portões porque procura `FASES`,
#     `telaCapa` e abre telas por nome — e uma lista escrita no
#     `SEQUENCIAS-DIDATICAS.md §7` dizendo quais portões alcançam. Ou seja: a
#     escolha de quais rodar dependia de eu LEMBRAR daquela lista. Toda vez.
#     Isso é exatamente o "esquecimento" que este projeto inteiro combate, e é
#     pior que portão nenhum: leva a chamar de "aprovado" o que ninguém mediu.
#
#     Agora é código. Um comando, a lista dentro dele, e um veredito que só diz
#     APROVOU com 0 em todos.
#
#  ⚠️ ELE IMPRIME OS TRÊS GRUPOS, SEMPRE — e o do meio é o mais importante:
#       1. PASSOU        — código 0, medido de verdade.
#       2. NÃO MEDIU     — o portão rodou e não achou o que medir. **Isto não é
#                          "passou".** Aparece na tela para ninguém confundir
#                          silêncio com aprovação.
#       3. NÃO ALCANÇA   — portão do motor, com o MOTIVO escrito ao lado. Não é
#                          defeito da atividade nem mérito dela: é dívida da
#                          casa (tarefa #104), e fica à vista para não sumir.
#
#  ⚠️ O QUE ELE AINDA NÃO MEDE, e que nenhum portão mede hoje: se as 25 folhas
#     SOBEM de verdade (a escada didática) e se um gesto passa de 40% do
#     caderno. Enquanto isso não existir, quem responde por isso é o crivo
#     escrito do `_sequencias/POTE-*.md` — que é meu, e não é medida. Está dito
#     no rodapé toda vez que a banca roda.
#
#  Códigos: 0 aprovou · 1 REPROVOU (lista quem) · 2 não deu para medir.
#  Uso: bash _qa/auditar_folha.sh _casa1        (ou _casa1/index.html)
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2
ALVO="${1:-}"
[ -z "$ALVO" ] && { echo "uso: bash _qa/auditar_folha.sh <pasta|arquivo.html>"; exit 2; }
if [ -d "$ALVO" ]; then PASTA="${ALVO%/}"; ARQ="$PASTA/index.html"; else ARQ="$ALVO"; PASTA="$(dirname "$ARQ")"; fi
[ -f "$ARQ" ] || { echo "nao achei $ARQ"; exit 2; }

# ⚠️ ISTO AQUI É O PORTÃO DO PRÓPRIO PORTÃO. Rodar a banca da folha viva num app
#    do motor daria uma enxurrada de "não medi" e alguém acabaria lendo como
#    aprovação. Caderno de folha viva tem `PAGEL` e `folhas.js`; app do motor
#    tem `FASES`. Na dúvida, ele PARA e manda usar a outra banca.
if ! grep -q "PAGEL" "$ARQ" 2>/dev/null && [ ! -f "$PASTA/folhas.js" ]; then
  echo "$ARQ nao parece caderno de folha viva (sem PAGEL nem folhas.js)."
  echo " -> se for app do motor, a banca dele e: bash _qa/auditar.sh $ARQ"
  exit 2
fi

T0=$SECONDS
TMP="$(mktemp -d /tmp/bancafolha.XXXXXX)"

# ------------------------------------------------------------------
#  OS PORTÕES QUE ALCANÇAM A FOLHA VIVA.
#  nome|comando — cada linha é um portão que MEDE este formato. Portão novo que
#  passe a alcançar folha viva entra AQUI no mesmo commit em que for escrito;
#  senão ele existe e ninguém roda.
# ------------------------------------------------------------------
PORTOES=(
  "1a engenheiro (node --check)|node --check $PASTA/folhas.js"
  "0z pre-voo (39 portoes de texto)|bash _qa/previo.sh $PASTA"
  "1z boot (abre limpa?)|node _qa/boot.js $ARQ"
  "1w andar folha (anda as 25, item por item)|node _qa/andar_folha.js $PASTA"
  "4b leiaute a mao (6 tamanhos, alvo >= 40px)|node _qa/leiaute_mao.js $ARQ"
  "1i4 resposta impressa no enunciado|python3 _qa/resposta_impressa.py $PASTA"
  "0b9 pedagogo (curriculo verbatim)|python3 _qa/pedagogo_curriculo.py $PASTA"
  "0i2 voz do pote (tudo que sorteia fala?)|python3 _qa/voz_do_pote.py $PASTA"
  "0b7 leque e escada (gesto declarado)|python3 _qa/leque_folha.py $PASTA"
  "0p duracao (enche a aula?)|python3 _qa/duracao.py $PASTA"
  "0o6 halo branco no recorte|python3 _qa/halo.py $PASTA"
  "1c resto de clone|python3 _qa/clone.py $ARQ"
  "1c2 duplicatas (mesma figura, dois nomes)|python3 _qa/duplicatas.py $PASTA"
  "0r revisor (texto, concordancia, digitacao)|python3 _qa/revisor.py $PASTA"
  "0b6 catalogo + painel|python3 _qa/catalogo.py $PASTA"
)

# ------------------------------------------------------------------
#  OS DO MOTOR, COM O MOTIVO. Não são rodados: são DECLARADOS, para que a
#  ausência deles seja visível em vez de silenciosa.
# ------------------------------------------------------------------
FORA=(
  "jogador.js|procura telaCapa/FASES — a folha viva nao tem fase, tem folha"
  "0b5 prova de sala|idem: joga a cadeia de fases do motor"
  "contraste.js|abre telas por nome (telaBase/telaFim)"
  "imagens.js|idem, e le a pre-carga IMGS que a folha viva nao publica"
  "leiaute.js|pede a lista de telas do motor (use o leiaute_mao, que roda aqui)"
  "0a pedagogo (escada didatica)|le a cadeia de fases; ver a divida abaixo"
  "0b padrao da casa (leque de gestos)|conta FASES, nao folhas; ver a divida abaixo"
  "3d mascote|folha viva nao tem mascote de 3 camadas"
  "5c fotos|as fotos aprovadas sao por fase do motor"
)

echo "==================================================="
echo " BANCA DA FOLHA VIVA — $ARQ"
echo "==================================================="

i=0
for item in "${PORTOES[@]}"; do
  cmd="${item#*|}"
  prog="$(echo "$cmd" | awk '{print ($1=="python3"||$1=="node"||$1=="bash")?$2:$1}')"
  if [[ "$prog" == _qa/* && ! -f "$prog" ]]; then
    echo "2" > "$TMP/$i.st"; echo "(nao existe nesta copia: $prog)" > "$TMP/$i.out"; i=$((i+1)); continue
  fi
  ( eval "$cmd" > "$TMP/$i.out" 2>&1; echo $? > "$TMP/$i.st" ) &
  i=$((i+1))
done
wait

REPROVOU=""; CEGO=""; OK=0
i=0
for item in "${PORTOES[@]}"; do
  nome="${item%%|*}"; st="$(cat "$TMP/$i.st" 2>/dev/null || echo 9)"
  if [ "$st" = "0" ]; then
    OK=$((OK+1)); printf '  ok   %s\n' "$nome"
  elif [ "$st" = "2" ]; then
    CEGO="$CEGO
   · $nome"
    printf '  ?    %s  (NAO MEDIU — isto nao e passou)\n' "$nome"
  else
    REPROVOU="$REPROVOU
   · $nome (codigo $st)"
    printf '  X    %s  (codigo %s)\n' "$nome" "$st"
    echo "--- $nome ---"; tail -16 "$TMP/$i.out"; echo
  fi
  i=$((i+1))
done

echo
echo "--- nao alcancam este formato (portoes do MOTOR, por desenho) ---"
for f in "${FORA[@]}"; do printf '   - %-26s %s\n' "${f%%|*}" "${f#*|}"; done

echo
echo "==================================================="
echo " ${#PORTOES[@]} portao(oes) rodados em $((SECONDS-T0))s — passaram: $OK"
[ -n "$CEGO" ] && echo " NAO MEDIRAM (conferir se a atividade nao tem aquilo):$CEGO"
echo
echo " ⚠️ O QUE NENHUM PORTAO MEDE AINDA:"
echo "    · se o CONTEUDO sobe — silaba simples antes da complexa, palavra curta"
echo "      antes da comprida, o degrau do curriculo. O 0b7 mede o LEQUE e o peso"
echo "      do GESTO (um proxy declarado), nao o conteudo."
echo "    Isso continua com o crivo do _sequencias/POTE-*.md e com o professor —"
echo "    e crivo e do Claude, nao e medida. Nao confundir com aprovacao."
if [ -n "$REPROVOU" ]; then
  echo
  echo " BANCA REPROVOU — consertar antes de mostrar ao Marcos:$REPROVOU"
  echo "==================================================="
  rm -rf "$TMP"; exit 1
fi
echo
echo " BANCA APROVOU (nos portoes que alcancam este formato)."
echo "==================================================="
rm -rf "$TMP"; exit 0
