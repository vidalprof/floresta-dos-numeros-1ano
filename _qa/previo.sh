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
              "1s versao do folhas.js|python3 _qa/versao_script.py $PASTA" \
              "1u elemento que nao existe|python3 _qa/elemento.py $PASTA" \
              "1v global atropelado|python3 _qa/global_atropelado.py $PASTA" \
              "1w silaba x dicionario pt_BR|python3 _qa/silaba_dicionario.py $PASTA" \
              "1x som da silaba (o recorte tem voz?)|python3 _qa/silaba_audio.py $PASTA" \
              "1y a voz se conferiu sozinha?|python3 _qa/silaba_conferida.py $PASTA" \
              "1z2 bateria: a regua da soletracao tem faro?|python3 _qa/silaba_bateria.py" \
              "1t teclado completo|python3 _qa/teclado.py $PASTA" \
              "0b2 dinamicas|python3 _qa/dinamicas.py $ARQ" "4 classes sem estilo|python3 _qa/classes.py $ARQ" \
              "3b beco na peca|python3 _qa/beco_peca.py $ARQ" "4b cor cravada|python3 _qa/cor_fixa.py $ARQ" \
              "0b3 espera|python3 _qa/espera.py $ARQ" "0p game-feel|python3 _qa/gamefeel.py $ARQ"; do
    nome="${item%%|*}"; cmd="${item#*|}"
    out="$(eval "$cmd" 2>&1)"; st=$?
    if [ "$st" != "0" ] && [ "$st" != "2" ]; then FALHOU="$FALHOU
   · $nome (codigo $st)"; echo "--- $nome ---"; echo "$out" | tail -8; fi
  done
  echo "==================================================="
  echo " PRE-VOO DA PECA $ARQ — 8 portoes de texto em $((SECONDS-T0))s"
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
  "0w bash -e derruba o passo (cmd; rc=$?)|python3 _qa/bash_e.py"
  "1q3 fala curta demais / mp3 repetido|python3 _qa/fala_curta.py $PASTA"
  # ⭐ o PEDAGOGO virou medida (set/2026): habilidade citada existe mesmo no
  #    curriculo da rede, os objetivos do relatorio batem com ela um a um, e o
  #    professor ve o dossie DENTRO da atividade. Em pasta que nao e caderno de
  #    folha viva ele sai com 2 ("nao medi"), que o previo trata como aviso.
  # ⚠️ O ESLINT FALTAVA AQUI, e custou uma entrega inteira (set/2026).
  #    `node --check` so olha SINTAXE: um nome que nunca foi declarado passa
  #    por ele liso e so estoura no clique da crianca. Eu deixei um `anel`
  #    orfao ao refazer a roda, o pre-voo disse "nenhum erro barato", e quem
  #    pegou foi o portao pre-entrega do workflow — DEPOIS do push, travando
  #    a publicacao da voz. O portao ja existia; so nao estava no caminho
  #    rapido. Agora esta.
  "0a2 estatico (nome nao declarado)|bash _qa/estatico.sh $ARQ"
  "0b9 pedagogo (curriculo)|python3 _qa/pedagogo_curriculo.py $PASTA"
  "0b12 parecer do pedagogo (assinado?)|python3 _qa/parecer.py $PASTA"
  "0b13 titulo diz o assunto|python3 _qa/titulo.py $PASTA"
  "0b14 duas folhas com a mesma narracao|python3 _qa/enunciado_repetido.py $PASTA"
  # ⚠️ O `1s` MORAVA SO NA BANCA, e por isso me escapou (20/set/2026). Eu
  #    mexi no `folhas.js` de DEZESSETE cadernos, rodei o pre-voo em todos,
  #    publiquei — e o carimbo `?v=` do endereco continuou o velho. Quem
  #    nunca abriu o caderno recebe o arquivo novo; quem JA abriu recebe a
  #    copia do cache, e o conserto nao chega justamente a quem esta no meio
  #    da sequencia. Portao de texto, roda em milissegundos: nao ha motivo
  #    para ele esperar a banca de quatro minutos.
  "1s versao do folhas.js|python3 _qa/versao_script.py $PASTA"
  # ⚠️ nasceu de "cita laranja e aparece lata": a silaba saia da palavra errada
  "0b10 fonte da silaba|python3 _qa/silaba_fonte.py $PASTA"
  # ⭐ 1i2) palavra do pote SEM figura no disco — a familia do dia em que o
  #    selo da medalha foi renomeado e a PALAVRA "estrela" ficou sem desenho.
  "1i2 figura do pote|python3 _qa/figura_pote.py $PASTA"
  # ⭐ 1i5) a figura veio da FOLHA DE PAPEL? (14/set/2026, pergunta do Marcos:
  #    "por que você não cumpre o que combinamos?"). A regra existia desde
  #    set/2026 e era só lembrete; lembrete depende da minha memória, que comeca
  #    do zero a cada sessao. Agora e medida.
  "1i5 figura veio da folha|python3 _qa/figura_da_folha.py $PASTA"
  # ⭐ 1i6) a figura trouxe PAUTA da folha junto? (14/set/2026, queixa do Marcos:
  #    "tem resto de outras imagens nas imagens"). O 1i5 pergunta se a figura veio
  #    da folha certa; este pergunta se veio SO a figura, sem o quadradinho de
  #    marcar, sem a moldura tracejada e sem a linha da coluna.
  "1i6 sobra da pauta da folha|python3 _qa/sobra_da_folha.py $PASTA"
  # ⭐ 1i7) o recorte CORTOU o desenho? (19/set/2026, o Marcos abrindo o
  #    *Jornalista por um Dia*: *"na imagem de a irmã deu um presente ao irmão
  #    está cortada aparecendo parte do irmão. Esse tipo de erro não pode
  #    acontecer"*). Estava só na banca de folha viva; aqui custa dois segundos
  #    e pega o defeito antes de eu gastar os dez minutos da banca inteira.
  "1i7 recorte cortou o desenho|python3 _qa/recorte_cortado.py $PASTA"
  # ⭐ 1i8) a mão de N dedos é a de N dedos? (19/set/2026, com a troca do vetor
  #    pela figura recortada no `_dedos`). Numa atividade de CONTAR, o número de
  #    dedos é o conteúdo: a figura de "três" com quatro dedos ensina errado.
  #    Ele NAO conta dedo (impossível: na de 4 e na de 5 os dedos se encostam);
  #    mede o que dá — a tinta crescendo de 0 a 5, nenhuma figura repetida, os
  #    tons sendo a mesma mão. Quem confere a contagem é o olho, na folha de
  #    contato. Nos outros cadernos ele sai com "NAO SE APLICA".
  "1i8 a mao de N dedos|python3 _qa/dedos_contam.py $PASTA"
  # ⭐ 0r2) a criança OUVE o que está escrito no falas.json. O revisor (0r) pega
  #    digitação; a concordância de artigo e de verbo, ninguém media — e os Cinco
  #    Reinos foram ao ar com 54 falas erradas ("do reino DAS animais").
  "0r2 concordancia nas falas|python3 _qa/concordancia.py $PASTA"
  "1l2 ligar com rotulo repetido|python3 _qa/ligar_rotulo.py $PASTA"
  "0b11 identidade propria (cor, capa, animacao)|python3 _qa/identidade.py $PASTA"
  # ⭐ so responde em jogo de UNO (nos outros ele sai com 2 = "nao medi")
  "3u regra da compra (UNO)|node _qa/uno.js $ARQ"
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
  # ⭐ 4c3) a regra-@ que some do CSS (14/set/2026): o Desfile foi ao ar com 36
  #    `@keyframes`/`@media` sem o arroba — animacao morta e celular sem as
  #    regras de tela pequena, sem uma linha de erro em lugar nenhum.
  "4c3 regra-@ do CSS|python3 _qa/css_atregra.py $ARQ"
  "4c4 regra de CSS que nao fecha|python3 _qa/css_fechado.py $ARQ"
  "4c2 design (catraca)|python3 _qa/design.py"
  "0b8 peso (orcamento)|python3 _qa/peso.py $ARQ"
  "0p game-feel|python3 _qa/gamefeel.py $ARQ"
  "0q curiosidade|python3 _qa/curiosidade.py $ARQ"
  "falas (narracao)|python3 _qa/falas.py $PASTA/falas.json"
  "1n lingua estrangeira (lacuna, correcao, grafia)|python3 _qa/ingles.py $PASTA"
  # ⭐ 1o) o alto-falante da RESPOSTA (15/set/2026, Marcos: "precisamos por audio
  #    nas opcoes de resposta para quem nao sabe ler, principalmente para os
  #    menores"). Era regra da casa desde ago/2026 e NAO era medida — quando ele
  #    pediu de novo, eu contei 9 opcoes mudas em quatro cadernos, tres de
  #    alfabetizacao. A pior: `_rima1`, do 1o ano, com os botoes RIMA / NAO RIMA.
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
  # ⭐⭐ 1q2) E O TEXTO QUE EU MANDEI GRAVAR VIROU ARQUIVO? (23/set/2026). O 0i
  #    vai do CODIGO para o falas.json; o 1q do falas.json para o CODIGO. Faltava
  #    o terceiro lado: do falas.json para o DISCO. O `_sil2` foi ao ar com o
  #    texto novo e CATORZE falas sem mp3 — entreguei a mesma pasta duas vezes em
  #    quatro minutos e as corridas se atropelaram. E o carimbo disse `noar:1`
  #    com o sha certo, porque o carimbo mede a PAGINA e nao a VOZ.
  # ⚠️ AQUI ELE E AVISO, NAO PORTAO, e de proposito: no meio do trabalho a ordem
  #    normal e gerar as falas e so depois entregar, entao ficar vermelho aqui
  #    seria ficar vermelho sempre. Quem REPROVA e o mesmo portao dentro do
  #    `entregar.yml`, logo antes de publicar — que e onde o defeito mordeu.
  "1q2 toda fala tem mp3 (aviso)|python3 _qa/voz_gravada.py $PASTA || true"
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
