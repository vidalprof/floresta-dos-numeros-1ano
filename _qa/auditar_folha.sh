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
  "1u elemento que nao existe|python3 _qa/elemento.py $PASTA"
  "1v global atropelado|python3 _qa/global_atropelado.py $PASTA"
  "1w silaba x dicionario pt_BR|python3 _qa/silaba_dicionario.py $PASTA"
  "1x som da silaba (o recorte tem voz?)|python3 _qa/silaba_audio.py $PASTA"
  "1y a voz se conferiu sozinha?|python3 _qa/silaba_conferida.py $PASTA"
  "1z2 bateria: a regua da soletracao tem faro?|python3 _qa/silaba_bateria.py"
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
  "0b12 parecer do pedagogo (assinado?)|python3 _qa/parecer.py $PASTA"
  "0b13 titulo diz o assunto|python3 _qa/titulo.py $PASTA"
  "0b14 duas folhas com a mesma narracao|python3 _qa/enunciado_repetido.py $PASTA"
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
  # ⭐⭐ 1p) A PALAVRA QUE A CRIANCA VE TEM VOZ, E E A DELA (21/set/2026).
  #    Defeito que chegou a SALA: "as palavras estao sendo ditas erradas" ·
  #    "tem palavras sendo ditas diferente do que e mostrado". A chave da fala
  #    e o nome da palavra sem acento, e os DOIS LADOS tiravam o acento de
  #    jeitos diferentes: o gravador trocava (a-til -> A) e o app APAGAVA.
  #    O `falar()` volta calado quando a chave nao existe -> 17 palavras MUDAS
  #    em tres cadernos no ar, todas com til ou cedilha, que sao justamente as
  #    que a crianca mais precisa ouvir. E ja tinha sido consertado no
  #    `_aumdim2` com outro nome, e eu nao levei aos outros dezesseis.
  "1p voz da palavra (as pontas casam)|python3 _qa/voz_da_palavra.py $PASTA"
  # ⭐⭐ 1q) A FALA QUE O CODIGO PEDE EXISTE? (21/set/2026). Havia portao para a
  #    metade errada: o `vozfalta.py` (0i) vai do TEXTO para o AUDIO. Ninguem
  #    perguntava o contrario, e e ai que mora o silencio: `falar(k)` faz
  #    `var t = FALAS[k]; if(!t) return;` — chave inexistente volta CALADO, sem
  #    erro, sem 404, sem aparecer em print nenhum. Medido com o codigo no ar:
  #    `_troca2` e `_nasal2` pediam `fim` (a festa do fim do caderno era muda) e
  #    `_abc1` e `_rima1` pediam `folhaPronta` (o elogio de cada folha).
  "1q fala pedida existe|python3 _qa/fala_pedida.py $PASTA"
  # ⭐⭐ 1r) DIGITAR NAO PODE DEPENDER DO ENTER (21/set/2026, o Marcos usando o
  #    caderno dos sistemas do 5o ano: "tem uma atividade onde o estudante digita
  #    e tem que clicar enter para confirmar, melhor nao precisar do enter" e
  #    "corrija isso em qualquer atividade que tenha isso"). A grade de tamanho
  #    FIXO ja fechava sozinha; a grade LIVRE (folha de producao) nao tinha como
  #    saber que a crianca terminou e so o ENTER confirmava — tecla que muda de
  #    nome em cada celular e que a crianca de 10 anos nao adivinha. Estava em
  #    OITO cadernos no ar. Hoje: fecha sozinho quando a palavra bate, botao
  #    PRONTO para a palavra de fora da lista, e o Enter como terceira porta.
  "1r digitar sem depender do Enter|python3 _qa/sem_enter.py $PASTA"
  # ⭐ 1i9) A FIGURA NUNCA E MOSTRADA MAIOR QUE O ARQUIVO (21/set/2026). Era
  #    regra da casa com CODIGO (`naoAmplia`) e sem CONTA: o guarda nasceu no
  #    esqueleto e os 23 cadernos anteriores nunca o receberam. Nove deles
  #    mostravam a mesma faca de 260x71 px esticada ate 1,80x. Quem pegava era
  #    o `leiaute_mao.js`, que abre o navegador e custa dez minutos por caderno;
  #    este le o texto e responde em milissegundos.
  "1i9 figura nunca ampliada|python3 _qa/nao_amplia.py $PASTA"
  # ⭐ 0v) A FORÇA DA VOZ (19/set/2026, cobrança do Marcos: "os áudios têm que
  #    ficarem perfeitos"). Havia portão para a fala que falta, para a voz-robô,
  #    para a palavra que a voz erra e até para a pronúncia — e nenhum media a
  #    única coisa que o ouvido sente primeiro: o VOLUME. Medido em cinco
  #    cadernos, 2 a 3 falas de cada um saem 7 dB abaixo das irmãs, sempre
  #    palavra curta e isolada ("Livros.", "e."). No PC da escola a criança
  #    aperta o alto-falante da opção e não ouve. Conserto:
  #    `python3 _padrao/voz_forca.py <pasta>`.
  "0v forca da voz (nenhuma fala abafada)|python3 _qa/voz_forca.py $PASTA"
  # ⭐ 1i7) O RECORTE CORTOU O DESENHO? (19/set/2026, o Marcos abrindo o
  #    *Jornalista por um Dia*: *"na imagem de a irmã deu um presente ao irmão
  #    está cortada aparecendo parte do irmão. Esse tipo de erro não pode
  #    acontecer"*). O arquivo sai íntegro — abre, não tem halo, não está
  #    esticado, o jogador resolve a folha — e mesmo assim falta metade do
  #    desenho. O defeito só existe comparando o recorte com a FOLHA DE PAPEL de
  #    onde ele veio, e é isso que este portão faz. Na estreia achou o caso do
  #    Marcos, mais três fotos no `_not2` e quatro peças no `_narra2`, que já
  #    estava no ar (castelo sem torre, menino sem o topo da cabeça, galinha sem
  #    a cauda, vaca sem as patas).
  "1i7 recorte cortou o desenho|python3 _qa/recorte_cortado.py $PASTA"
  # ⭐ 1i8) A MAO DE N DEDOS E A DE N DEDOS? (19/set/2026, com a troca do desenho
  #    de codigo pela figura recortada no `_dedos`). Numa atividade de CONTAR, o
  #    numero de dedos nao e arte: e o conteudo. Ele NAO conta dedo — mede a
  #    tinta crescendo de 0 a 5, figura repetida e tom que mudou a silhueta.
  #    Nos cadernos sem a serie das maos ele sai com "NAO SE APLICA".
  "1i8 a mao de N dedos|python3 _qa/dedos_contam.py $PASTA"
  # ⭐ 0b11) IDENTIDADE PROPRIA (Marcos, 18/set/2026: "cada caderno precisa ter capa
  #    diferente, cor diferente, animacoes... os estudantes acham que e a mesma
  #    atividade"). Onze cadernos no ar dividiam duas cores e duas capas.
  "0b11 identidade propria (cor, capa, animacao)|python3 _qa/identidade.py $PASTA"
  "0b6 catalogo + painel|python3 _qa/catalogo.py $PASTA"
  "0w bash -e derruba o passo (cmd; rc=$?)|python3 _qa/bash_e.py"
  "1q3 fala curta demais / mp3 repetido|python3 _qa/fala_curta.py $PASTA"
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
