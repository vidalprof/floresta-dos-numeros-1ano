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
  # ⭐ 1s) o folhas.js sobe com versao no endereco? Sem isso o navegador serve
  #     uma copia velha para sempre e a crianca ve so a faixa de cima — foi o
  #     que o Marcos pegou no Chrome dele em 14/set/2026.
  "1s versao do folhas.js|python3 _qa/versao_script.py $PASTA"
  # ⭐ 1t) o teclado tem TODAS as letras? Faltavam K, W, Y e sete acentos, e a
  #     crianca que tentava escrever PÊSSEGO ficava com "PSSEGO" — a folha nunca
  #     fechava, e sem erro nenhum na tela (medido em 15/set/2026).
  "1t teclado completo|python3 _qa/teclado.py $PASTA"
  "0z pre-voo (46 portoes de texto)|bash _qa/previo.sh $PASTA"
  "1z boot (abre limpa?)|node _qa/boot.js $ARQ"
  "1w andar folha (anda as 25, item por item)|node _qa/andar_folha.js $PASTA"
  "1y conta da folha (o pote bate com os itens?)|node _qa/conta_folha.js $PASTA"
  # ⭐ O JOGADOR DA FOLHA VIVA (13/set/2026, pergunta do Marcos: "a outra banca
  #    seria uma boa para essas sequencias?"). O `andar_folha` mede o caderno
  #    ABRINDO; este mede o caderno FECHANDO — ele le a resposta declarada em
  #    RESP e resolve item por item. Na estreia achou tres defeitos, dois deles
  #    em sete cadernos ja no ar (a folha de circular nao fechava por caminho
  #    nenhum, e o teclado nao tinha K, W nem Y). Os dois na banca, porque
  #    medem coisas diferentes.
  "1v jogador (resolve item por item)|node _qa/joga_folha.js $PASTA 8794"
  "4b leiaute a mao (6 tamanhos, alvo >= 40px)|node _qa/leiaute_mao.js $ARQ"
  "1i4 resposta impressa no enunciado|python3 _qa/resposta_impressa.py $PASTA"
  "0b9 pedagogo (curriculo verbatim)|python3 _qa/pedagogo_curriculo.py $PASTA"
  "0i2 voz do pote (tudo que sorteia fala?)|python3 _qa/voz_do_pote.py $PASTA"
  "0b7 leque e escada (gesto declarado)|python3 _qa/leque_folha.py $PASTA"
  "0p duracao (enche a aula?)|python3 _qa/duracao.py $PASTA"
  "0o6 halo branco no recorte|python3 _qa/halo.py $PASTA"
  "1i5 figura veio da folha de papel|python3 _qa/figura_da_folha.py $PASTA"
  "1i6 sobra da pauta da folha|python3 _qa/sobra_da_folha.py $PASTA"
  # ⭐ 0r2) a criança OUVE o que está escrito no falas.json. O revisor (0r) pega
  #    digitação; a concordância de artigo e de verbo, ninguém media — e os Cinco
  #    Reinos foram ao ar com 54 falas erradas ("do reino DAS animais").
  "0r2 concordancia nas falas|python3 _qa/concordancia.py $PASTA"
  "1c resto de clone|python3 _qa/clone.py $ARQ"
  "1c2 duplicatas (mesma figura, dois nomes)|python3 _qa/duplicatas.py $PASTA"
  "1l2 ligar com rotulo repetido|python3 _qa/ligar_rotulo.py $PASTA"
  "0r revisor (texto, concordancia, digitacao)|python3 _qa/revisor.py $PASTA"
  "1n lingua estrangeira (lacuna, correcao, grafia)|python3 _qa/ingles.py $PASTA"
  # ⭐ 1o) sem voz na opcao, a crianca que ainda nao le escolhe pelo tamanho do
  #    botao — e a folha vira sorteio para justamente quem ela deveria ajudar.
  "1o alto-falante da resposta|python3 _qa/voz_opcao.py $PASTA"
  "0b6 catalogo + painel|python3 _qa/catalogo.py $PASTA"
)

# ------------------------------------------------------------------
#  OS DO MOTOR, COM O MOTIVO. Não são rodados: são DECLARADOS, para que a
#  ausência deles seja visível em vez de silenciosa.
# ------------------------------------------------------------------
FORA=(
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
# ⚠️ SILENCIO NAO E APROVACAO — e este arquivo passou a primeira semana de vida
#    se contradizendo: imprimia "NAO MEDIU — isto nao e passou" em cima e
#    "BANCA APROVOU" embaixo, na mesma tela. Quem le a ultima linha (e é ela que
#    o script chamador le, pelo codigo de saida) levava um portao cego embrulhado
#    como aprovacao. Agora portao que nao mediu segura o veredito em 2, e quem
#    quiser publicar assim tem que dizer, com todas as letras, que conferiu na mao
#    que o caderno nao tem aquilo. É a mesma regra do CLAUDE.md: portao que
#    imprime NADA nao e "passou", e "nao medi" e divida, nao carimbo.
if [ -n "$CEGO" ]; then
  echo
  echo " BANCA NAO CONCLUIU — $OK portao(oes) passaram, mas estes nao mediram:$CEGO"
  echo " Isto NAO e aprovacao. Conferir na mao se o caderno realmente nao tem"
  echo " aquilo (ai a divida e legitima) ou se o portao ficou cego (ai e defeito)."
  echo "==================================================="
  rm -rf "$TMP"; exit 2
fi
echo
echo " BANCA APROVOU (nos portoes que alcancam este formato)."
echo "==================================================="
rm -rf "$TMP"; exit 0
