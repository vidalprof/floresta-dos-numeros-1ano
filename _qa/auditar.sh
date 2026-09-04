#!/usr/bin/env bash
# ============================================================
#  A BANCA — roda TODOS os auditores antes de entregar
#  Pedido do Marcos (ago/2026): "precisamos de auditores antes de
#  entregar a atividade". Cada auditor e um profissional com uma
#  obsessao só. Nenhum deles confia no outro.
#
#  Uso:  bash _qa/auditar.sh _doceria/index.html telaCapa dMonta dSoma ...
#        (sem lista de telas, ele descobre sozinho quem chama limpa())
#
#  Sai 0 se a banca inteira aprovar; 1 se algum reprovar.
# ============================================================
set -uo pipefail
# ⚠️ LICAO PAGA (ago/2026): editei este arquivo ENQUANTO ele rodava e a banca
#    morreu com "syntax error near unexpected token" na linha 101 — o bash le o
#    script em pedacos, entao trocar o arquivo no meio o corrompe. O erro parece
#    defeito da atividade e nao e: e do relogio. A banca agora roda de uma COPIA,
#    e continua inteira mesmo que eu mexa no original no meio.
if [ "${QA_COPIA:-}" != "1" ]; then
  _COPIA="$(mktemp -t qabanca.XXXXXX.sh)"
  cp "$0" "$_COPIA"
  QA_COPIA=1 bash "$_COPIA" "$@"; _ST=$?
  rm -f "$_COPIA"; exit $_ST
fi
# ⚡ MODO REPARO (`--reparo`) — pedido pelo RELOGIO, nao pelo gosto.
#    A banca inteira leva ~25 min porque abre o Chromium em 6 tamanhos x 40
#    telas e ainda joga a atividade ate a medalha. Isso esta certo para
#    ENTREGAR, e esta errado para CONSERTAR: quem acabou de trocar uma frase
#    espera 25 minutos para saber que trocou errado, e a esteira para.
#    O modo reparo roda so os portoes de TEXTO (segundos) e diz, com todas as
#    letras, que NAO e aprovacao. A banca inteira continua obrigatoria antes de
#    o Marcos ver. ⚠️ Ele NUNCA sai com "APROVOU": passar aqui e "ainda nao
#    reprovou no barato".
REPARO=0
if [ "${1:-}" = "--reparo" ]; then REPARO=1; shift || true; fi
ARQ="${1:-}"
if [ -z "$ARQ" ]; then echo "uso: bash _qa/auditar.sh [--reparo] <arquivo.html> [tela1 tela2 ...]"; exit 2; fi
shift || true
TELAS="$*"
# a pasta da atividade (alguns portoes medem a PASTA, nao o arquivo)
PASTA="$(dirname "$ARQ")"

if [ -z "$TELAS" ]; then
  TELAS=$(python3 - "$ARQ" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
js="".join(re.findall(r"<script>(.*?)</script>",h,re.S))
# ⚠️ LICAO PAGA (ago/2026): numa atividade MONTADA este detector listava as
#    funcoes INTERNAS das pecas como se fossem telas — o integrador inlina o
#    corpo da peca na coluna zero, entao `^function pecaIntruso(` casa com o
#    regex. So que elas vivem dentro do fechamento `MEC[...]` e NAO sao globais:
#    todo portao de navegador tentava abri-las por nome, `window[t]` vinha
#    `undefined`, e o portao pulava EM SILENCIO. Na _prova30 eram 28 de 38
#    nomes — e o leiaute ainda imprimia "38 telas", que parecia cobertura.
#    As fases de verdade nao se abrem por nome: quem as desenha e `montaFase(i)`,
#    e os portoes ja sabem disso. Entao o que esta dentro de um MEC sai da lista.
def fora_das_pecas(t):
    saida, i = [], 0
    for m in re.finditer(r'MEC\["[a-z0-9\-]+"\]\s*=\s*function', t):
        j = t.find("{", m.end())
        if j < 0: continue
        prof, k = 0, j
        while k < len(t):
            if t[k] == "{": prof += 1
            elif t[k] == "}":
                prof -= 1
                if prof == 0: break
            k += 1
        saida.append(t[i:m.start()]); i = k + 1
    saida.append(t[i:])
    return "".join(saida)
js = fora_das_pecas(js)
# tela = funcao que chama limpa() (mesma regra do _qa/fluxo.py)
nomes=[]
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    n=m.group(1); i=m.end()
    prof=0; j=js.find("{",i); k=j
    while k<len(js):
        if js[k]=="{": prof+=1
        elif js[k]=="}":
            prof-=1
            if prof==0: break
        k+=1
    # ⚠️ `montaFase` chama `limpa()` e entrava na lista como se fosse uma TELA.
    #    Os portoes a chamavam SEM indice (`window["montaFase"]()`), o motor
    #    desenhava sabe-se la o que, e saiu ate um achado de mentira no encaixe
    #    ("montaFase | .medal ocupa so 10%"). Ela e o DESENHISTA das fases, nao
    #    uma fase — e os portoes ja a chamam do jeito certo, com o indice.
    if n in ("montaFase", "montaBarra", "limpa"): continue
    if re.search(r"\blimpa\(\)", js[j:k]): nomes.append(n)
print(" ".join(nomes))
PY
)
fi

echo "==================================================="
echo " BANCA DE AUDITORIA — $ARQ"
echo " telas: $(echo $TELAS | wc -w)"
echo "==================================================="
# ⚠️ CORRIDA ENTRE BANCADAS (ago/2026). O caminho era FIXO (`/tmp/_peca.js`).
#    Com dois profissionais rodando a bancada ao mesmo tempo, um sobrescrevia o
#    JS do outro e AS DUAS pecas reprovavam no portao 1 com erro de sintaxe
#    FALSO. Reprovacao fantasma e o pior estrago: faz consertar o que nao esta
#    quebrado. Cada corrida agora tem o seu arquivo.
JSTMP="$(mktemp -t qajs.XXXXXX.js)"
FALHOU=0

# ============================================================
#  ⭐ O PORTAO QUE OLHA OS PORTOES — "aprovou" ou "rodou cego"?
#
#  ⚠️ LICAO PAGA (ago/2026). Na atividade montada, TRES portoes disseram "ok"
#  tendo medido ZERO: "0 alvo(s) conferido(s)", "0 fase(s) com pergunta falada",
#  "0 dica(s) conferida(s)". Zero medido nao e aprovacao — e o portao nao ter
#  olhado nada. E aprovacao vazia da CONFIANCA FALSA, que e pior do que reprovar:
#  eu leio "ok" e sigo em frente.
#
#  O `_qa/dinamicas.py` ja tinha aprendido isso sozinho ("NENHUMA mecanica
#  reconhecida — este portao NAO mediu nada"). Aqui a licao vira regra da BANCA,
#  para todos: portao que sai com 0 medido entra na lista dos CEGOS, e a banca
#  avisa em separado. Nao reprova sozinho — pode ser que a atividade realmente
#  nao tenha aquilo (nem toda atividade tem 'ache na cena') — mas nunca mais
#  passa despercebido.
# ============================================================
CEGOS=""
portao(){
  local nome="$1"; shift
  local saida
  saida="$("$@" 2>&1)"; local st=$?
  printf '%s\n' "$saida"
  # ⚠️ LICAO PAGA (ago/2026, no Jardim do Broto): a casa tem TRES codigos —
  #    0 = mediu e passou · 1 = REPROVOU · 2 = nao consegui medir. A banca lia
  #    "qualquer coisa != 0" como reprovacao, entao o `vozresposta`, que sai com
  #    2 nas atividades escritas a mao (elas nao tem o motor de FASES para
  #    percorrer), derrubava a atividade inteira dizendo "NAO MEDI". Isso e o
  #    contrario do que o codigo 2 significa e ensina a ignorar a banca.
  #    Agora: 1 (ou um estouro, >2) reprova; 2 vai para a lista dos CEGOS, que
  #    aparece no fim para ninguem confundir "nao medi" com "passou".
  if [ "$st" = "2" ]; then
    CEGOS="$CEGOS
   · $nome (o portao disse NAO MEDI)"
  elif [ "$st" != "0" ]; then FALHOU=1; fi
  # ⚠️ LICAO PAGA (ago/2026), e a ironia de sempre: ESTE portao, que existe para
  #    pegar portao cego, passou a acusar INOCENTE. "10 dica(s) conferida(s)"
  #    contem "0 dica(s)" como pedaco de texto — e o `vozdica`, que tinha medido
  #    DEZ dicas e aprovado, entrou na lista dos cegos. Portao que acusa o
  #    inocente ensina a ignorar portao, e a lista dos cegos e justamente a que
  #    nao pode virar ruido. Agora o zero tem que ser o numero INTEIRO zero.
  if printf '%s' "$saida" | grep -qE '(^|[^0-9])0 (fase|dica|alvo|texto|palavra|imagem)\(s\)|\-> *0 ([a-z]|$)|[Nn]ada a conferir'; then
    CEGOS="$CEGOS
   · $nome"
  fi
}

# ⚡⚡ OTIMIZACAO (ago/2026, pedido do Marcos "a banca tem que ser mais rapida"):
#    ANTES so 4 portoes de navegador saiam em paralelo; os outros ~8 (vozigual,
#    vozresposta, fala_o_escrito, vaza, voz_dupla, encaixe, visual, selo) rodavam
#    UM DE CADA VEZ no meio da banca, e cada um abre o Chromium do zero (~1-2s de
#    partida + render). Somados, eram minutos. Agora TODOS saem na MESMA largada,
#    escondidos atras do jogador (o mais lento): o tempo deles cabe na sombra dele.
#    `larga` dispara em segundo plano guardando saida + codigo; `colhe` le no
#    lugar certo e faz a MESMA contabilidade do `portao` (cego / reprovou). Nenhum
#    portao foi enfraquecido — so pararam de esperar uns aos outros.
# ⚡⚡ LICAO PAGA (Museu, ago/2026): a banca largava 12 navegadores DE UMA VEZ
#    (contraste, leiaute, imagens, jogador + 8 portoes de `larga`). Num container
#    apertado isso ESTOURA a memoria: uns caem no meio (reprova falsa) e as vezes
#    a banca inteira morre no arranque, sem imprimir nada. Agora um SEMAFORO
#    segura o numero de navegadores ao mesmo tempo (QA_MAX_PAR, default 3): eles
#    entram em fila, a banca fica um pouco mais lenta, mas TERMINA sempre. Menos
#    briga por CPU tambem deixa cada portao mais rapido. (reliability > pressa.)
QA_MAX_PAR="${QA_MAX_PAR:-2}"
_LARGA_PIDS=""
_espera_vaga(){
  while :; do
    local vivos="" p
    for p in $_LARGA_PIDS; do kill -0 "$p" 2>/dev/null && vivos="$vivos $p"; done
    _LARGA_PIDS="$vivos"
    [ "$(printf '%s\n' $vivos | grep -c .)" -lt "$QA_MAX_PAR" ] && break
    sleep 1
  done
}
larga(){  # larga <arquivo_base> <cmd...>
  local f="$1"; shift
  _espera_vaga
  printf '%q ' "$@" > "$f.cmd"          # comando re-executavel (ver colhe)
  ( "$@" > "$f" 2>&1; echo $? > "$f.st" ) &
  _LARGA_PIDS="$_LARGA_PIDS $!"
}
colhe(){  # colhe <nome> <arquivo_base>   (mesma regra do `portao`)
  local nome="$1" f="$2" saida st
  # ⚠️⚠️ LICAO PAGA (Museu, ago/2026), a mesma familia do "jogador lento":
  #    os portoes de `larga` rodam em paralelo e o `.st` (codigo de saida) so
  #    existe QUANDO o portao termina. Em atividade grande (36 fases), com a CPU
  #    disputada por 8 navegadores, o `voz_dupla` levava ~100s e ainda NAO tinha
  #    terminado quando o `colhe` foi ler — o `.st` vinha vazio, o default 1
  #    entrava, e a banca REPROVAVA uma atividade impecavel (todos os outros
  #    portoes "ok", este SEM SAIDA nenhuma no relatorio). Portao que reprova por
  #    lentidao do proprio auditor e pior que portao nenhum. Agora o colhe ESPERA
  #    o portao acabar (o .st aparecer) antes de julgar.
  local _e=0
  while [ ! -f "$f.st" ] && [ $_e -lt 240 ]; do sleep 1; _e=$((_e+1)); done
  saida="$(cat "$f" 2>/dev/null)"; st="$(cat "$f.st" 2>/dev/null || echo 1)"
  # ⚠️⚠️ LICAO PAGA (Museu, ago/2026): o NAVEGADOR do portao CAIU. Com 8 Chromium
  #    disputando um container apertado, um deles morre no meio e sai != 0 com a
  #    saida VAZIA — nao mediu nada, so caiu. Isso NAO e "reprovou", e "nao medi"
  #    (a mesma regra da casa). Antes de julgar, se caiu sem imprimir nada, o
  #    colhe RE-RODA o portao UMA vez, agora SOZINHO (sem a briga por CPU). Se
  #    passar, vale; se cair de novo sem medir, vira CEGO (olho do professor),
  #    nunca uma reprova falsa que trava a entrega.
  if [ "$st" != "0" ] && [ "$st" != "2" ] \
     && [ -z "$(printf '%s' "$saida" | tr -d '[:space:]')" ] && [ -f "$f.cmd" ]; then
    eval "$(cat "$f.cmd")" > "$f" 2>&1; st=$?
    saida="$(cat "$f" 2>/dev/null)"
  fi
  printf '%s\n' "$saida"
  if [ "$st" = "2" ]; then CEGOS="$CEGOS
   · $nome (o portao disse NAO MEDI)"
  elif [ "$st" != "0" ]; then
    if [ -z "$(printf '%s' "$saida" | tr -d '[:space:]')" ]; then
      CEGOS="$CEGOS
   · $nome (o navegador CAIU sem medir — rodar de novo na mao)"
    else FALHOU=1; fi
  fi
  if printf '%s' "$saida" | grep -qE '(^|[^0-9])0 (fase|dica|alvo|texto|palavra|imagem)\(s\)|\-> *0 ([a-z]|$)|[Nn]ada a conferir'; then
    CEGOS="$CEGOS
   · $nome"
  fi
}



# ⚡ OS TRES PORTOES DE NAVEGADOR SAIEM NA FRENTE, EM PARALELO.
#    Eles abrem o Chromium em 6 tamanhos x N telas e sozinhos levam quase todo
#    o relogio da banca; os portoes de texto (python) levam segundos. Rodando
#    junto, a banca inteira passou a caber no tempo do mais lento em vez da
#    SOMA de todos. Cada um escreve num arquivo e vota no fim, na ordem certa.
#    ⚠️ Nada de `2>/dev/null` aqui: portao que imprime NADA nao e "passou", e
#    "rodou cego". O erro vai para o mesmo arquivo e aparece na tela.
TMPQ="$(mktemp -d)"
if [ "$REPARO" = "1" ]; then
  echo "==================================================="
  echo " MODO REPARO: so os portoes de TEXTO (segundos)."
  echo " Fica de FORA tudo que abre o navegador — contraste, leiaute, imagem,"
  echo " acabamento, o jogador que joga ate a medalha e a colheita da voz."
  echo " Passar aqui NAO e aprovacao: e 'ainda nao reprovou no barato'."
  echo " Antes de mostrar ao Marcos, rodar a banca INTEIRA (sem --reparo)."
  echo "==================================================="
fi
if [ "$REPARO" != "1" ]; then
_espera_vaga; node _qa/contraste.js "$ARQ" $TELAS > "$TMPQ/contraste.txt" 2>&1 & PID_CON=$!; _LARGA_PIDS="$_LARGA_PIDS $PID_CON"
_espera_vaga; node _qa/leiaute.js   "$ARQ" $TELAS > "$TMPQ/leiaute.txt"   2>&1 & PID_LEI=$!; _LARGA_PIDS="$_LARGA_PIDS $PID_LEI"
_espera_vaga; node _qa/imagens.js   "$ARQ" $TELAS > "$TMPQ/imagens.txt"   2>&1 & PID_IMG=$!; _LARGA_PIDS="$_LARGA_PIDS $PID_IMG"
fi
# ⚠️ O JOGADOR TAMBEM SAI NA FRENTE (ago/2026). Ele rodava sozinho, no FIM, e
#    virou o dono do relogio: quando passou a jogar a atividade INTEIRA (antes
#    parava na 3a fase achando que a medalha da peca era o fim), a banca subiu
#    de 4m30 para 15m14 — MEDIDO. Ele nao depende de nenhum outro portao, entao
#    fica na mesma largada dos tres de navegador e o tempo dele se esconde
#    atras deles. O resultado continua sendo lido na hora certa, la embaixo.
# ⚡ O JOGADOR sai na frente, pela FILA do semaforo (como os outros navegadores).
#    ⚠️ LICAO PAGA (Museu, ago/2026): tentei o jogador PARALELO (joga_par, 3
#    trechos) como padrao para acelerar, mas neste container apertado um trecho
#    caia por CONTENCAO (processo morto) e reprovava atividade impecavel — cada
#    trecho passa quando roda SOZINHO. Confiabilidade > pressa: a banca usa o
#    jogador SERIAL (um so, escondido atras dos outros portoes pelo semaforo, que
#    ja da o codigo 0 confiavel). O `joga_par.sh` fica como FERRAMENTA avulsa para
#    validar rapido em runner folgado (`bash _qa/joga_par.sh <index.html>`).
if [ "$REPARO" != "1" ]; then
_espera_vaga; node _qa/jogador.js "$ARQ" > "$TMPQ/jogador.txt" 2>&1 & PID_JOG=$!; _LARGA_PIDS="$_LARGA_PIDS $PID_JOG"
fi
# ⚡ e os OUTROS portoes de navegador tambem largam agora, na sombra do jogador
#    (que e o mais lento). Colhidos mais abaixo, cada um no seu lugar, com a mesma
#    contabilidade de cego/reprovou. Sem $TELAS onde o portao mede a PASTA.
if [ "$REPARO" != "1" ]; then
larga "$TMPQ/g_vozigual.txt"   node _qa/vozigual.js      "$ARQ"
larga "$TMPQ/g_vozresp.txt"    node _qa/vozresposta.js   "$ARQ"
larga "$TMPQ/g_falaescr.txt"   node _qa/fala_o_escrito.js "$PASTA"
larga "$TMPQ/g_vaza.txt"       node _qa/vaza.js          "$ARQ" $TELAS
larga "$TMPQ/g_vozdupla.txt"   node _qa/voz_dupla.js     "$PASTA"
larga "$TMPQ/g_selo.txt"       node _qa/selo.js          "$ARQ"
larga "$TMPQ/g_encaixe.txt"    node _qa/encaixe.js       "$ARQ" $TELAS
larga "$TMPQ/g_visual.txt"     node _qa/visual.js        "$ARQ" $TELAS
fi

echo
echo "--- 1) ENGENHEIRO (o codigo roda?) -----------------"
python3 - "$ARQ" > "$JSTMP" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
if node --check "$JSTMP" >/dev/null 2>&1; then echo "  JS ok (node --check)"; else echo "  ERRO DE SINTAXE NO JS"; node --check "$JSTMP"; FALHOU=1; fi

# ⭐ 1y) O ESTATICO (ESLint) — o `ReferenceError` SEM abrir o navegador.
#    Complementa o boot: o boot ve FUNDO um caminho so (o que ele percorre);
#    este ve RASO todos os caminhos, inclusive o codigo que so roda na fase 28.
#    Foi ele que achou, em 1 segundo cada: `sTira` chamado e nunca declarado na
#    Grande Expedicao, `FECHO` na peca ensinar-mascote do RIGHT NOW, e
#    `gradeStars` no Climas do Mundo — as tres NO AR, as tres estourando na cara
#    da crianca, as tres invisiveis para os 65 portoes que ja existiam.
echo
echo "--- 1y) ESTATICO (nome usado que nunca foi declarado) -"
portao "1y estatico" bash _qa/estatico.sh "$ARQ"

# ⭐ 1x) O PC RUIM — "e se o enfeite falhar, a crianca ainda passa de fase?"
#    Nasceu com a turma do 1o ano jogando (set/2026): *"nas fases de ligar em
#    alguns pcs esta travando, o botao de proximo nao aparece"* e *"sinto nas
#    atividades que as vezes esse botao demora muito a aparecer ou nao aparece"*.
#    Era o motor: o fim de fase rodava festa/som/mascote SEM guarda, e a ACAO do
#    botao so era atribuida DEPOIS. Um enfeite tropecando (PC sem canvas, audio
#    bloqueado) matava a funcao e a crianca ficava presa. Nenhum portao pegava
#    porque todos rodam num Chromium saudavel, onde enfeite nunca falha.
echo
echo "--- 1x) PC RUIM (enfeite quebrado nao pode prender a crianca) -"
portao "1x pc ruim" node _qa/pcruim.js "$ARQ"

# ⭐ 1z) O PORTAO MAIS BURRO DA BANCA — "isso ABRE?" — e o mais importante.
#    Nasceu do Tangram (03/set/2026): o Marcos clicou e viu SO O FUNDO. Era um
#    `ReferenceError` no boot (uma `var` que eu apaguei sem querer). O
#    `node --check` aprovou (sintaxe estava certa), e TODOS os portoes de
#    navegador ficaram calados — quando o boot morre, eles nao acham as telas
#    por nome e nao medem NADA, que na tela imprime igual a "aprovou".
#    Por isso ele roda em SEGUNDO lugar, logo depois da sintaxe: se a atividade
#    nao abre, medir contraste de texto que nunca foi desenhado e teatro.
echo
echo "--- 1z) BOOT (a atividade abre e a capa leva adiante?) -"
portao "1z boot" node _qa/boot.js "$ARQ"

echo
echo "--- 0a) PEDAGOGO (a escada didatica sobe de verdade?) -"
portao "0a pedagogo" python3 _qa/pedagogo.py "$ARQ"
echo "--- 0b) PADRAO DA CASA (didatica, ilustrada, sonora, variada) -"
portao "0b padrao da casa" python3 _qa/padrao.py "$ARQ"

echo "--- 0b2) DINAMICAS (cada mecanica e as armadilhas DELA) -"
portao "0b2 dinamicas" python3 _qa/dinamicas.py "$ARQ"

echo "--- 0c) PERGUNTA AMBIGUA (pede 'a ponte' e tem duas?) -"
portao "0c pergunta ambigua" python3 _qa/ambiguo.py "$ARQ"

echo "--- 0d) VOZ DA TELA (o botao repete a PERGUNTA?) -"
portao "0d voz da tela" python3 _qa/voztela.py "$ARQ"
echo "--- 0e) TELA VAZIA (sobrou o fundo falando sozinho?) -"
portao "0e tela vazia" python3 _qa/telavazia.py "$ARQ"
echo "--- 0f) VOZ DA PERGUNTA (o botao fala o que esta escrito?) -"
portao "0f voz da pergunta" python3 _qa/vozpergunta.py "$ARQ"
# ⭐ 0f2) SO PARA ATIVIDADE MONTADA: a voz da rodada nao se confere lendo o
#    codigo (quem fala e um olheiro no balao). Confere-se JOGANDO: o colher.py
#    atravessa a atividade e anota todo texto que aparece; se sobrar algum sem
#    voz gravada, ele diz quantos e quais. "nada a acrescentar" = nenhuma tela
#    muda. E medicao, nao heuristica.
if [ "$REPARO" != "1" ]; then
if grep -q "pecabox" "$ARQ" && grep -q "MEC\[" "$ARQ"; then
  echo "--- 0f2) VOZ DA RODADA, MEDIDA JOGANDO (atividade montada) -"
  python3 _padrao/ESQUELETO/colher.py "$(dirname "$ARQ")" --so-ver || FALHOU=1
fi
fi
if [ "$REPARO" != "1" ]; then
echo "--- 0g) VOZ IGUAL AO TEXTO (o audio diz o que esta escrito?) -"
colhe "0g voz igual ao texto" "$TMPQ/g_vozigual.txt"
fi
echo "--- 0h) INTRO CALANDO A PERGUNTA (a 1a rodada e falada?) -"
portao "0h intro calando a pergunta" python3 _qa/vozintro.py "$ARQ"
echo "--- 0i) VOZ SEM MP3 (a fase ficou muda de vez?) -"
portao "0i voz sem mp3" python3 _qa/vozfalta.py "$ARQ"
echo "--- 0j) VOZ DA DICA (a dica fala o que esta escrito?) -"
portao "0j voz da dica" python3 _qa/vozdica.py "$ARQ"
echo "--- 0j2) ACENTO NA GRADE (a voz le a palavra CERTA?) -"
portao "0j2 acento na grade" python3 _qa/acento.py "$PASTA"
# ⭐ 0k — O ALTO-FALANTE DA RESPOSTA (defeito que o Marcos OUVIU, ago/2026: "os
#    botoes de som nao estao funcionando... somente o som do enunciado"). Os
#    portoes de voz conferiam enunciado, dica e a EXISTENCIA dos mp3; ninguem
#    conferia se o botao da RESPOSTA toca. Ver o cabecalho do arquivo.
if [ "$REPARO" != "1" ]; then
colhe "0k alto-falante da resposta" "$TMPQ/g_vozresp.txt"
fi
echo "--- 0k) A FASE DIZ O QUE ELA QUER? (regra escondida no enunciado) -"
portao "0k explica a regra" python3 _qa/explica.py "$ARQ"

echo "--- 0o) O REVISOR (testador humano de TEXTO: digitacao, concordancia) -"
# ⭐ o olho de TEXTO do "testador humano" que o Marcos pediu: pega o que chega
#    no OLHO dele — "o jiboia"/"a tucano" (concordancia), palavra repetida, espaco
#    duplo, HTML vazando na fala. Roda sobre a PASTA (falas.json + conteudo.json).
portao "0o revisor de texto" python3 _qa/revisor.py "$PASTA"

# ⭐ 0o2) A RESPOSTA ENTREGUE — nasceu da PRIMEIRA foto do Revisor Final
#     (set/2026): a pergunta destacava em negrito e laranja exatamente a palavra
#     que era a resposta ("Guardei o **bolo**..." / "Qual e o SUBSTANTIVO?").
#     Eram 16 perguntas assim, e a fase que existe para ENSINAR substantivo
#     virava um jogo de achar a cor. Nenhum dos 65 portoes pegou, porque o
#     CODIGO estava certo: a resposta declarada batia, a dica crescia, a voz
#     dizia o escrito, o jogador chegava na medalha. So olhando a TELA aparece.
echo "--- 0o2) RESPOSTA ENTREGUE (a pergunta da a resposta de graca?) -"
portao "0o2 resposta entregue" python3 _qa/entrega.py "$PASTA"

# ⭐ 0o3) O ENUNCIADO BATE? — nasceu de uma foto do Marcos (set/2026): a fase
#     "QUE TEMPO SOU EU?" pedia o TEMPO DO VERBO e, na terceira rodada, cobrava
#     DIMINUTIVO. Cada peca isolada estava certa (a resposta batia, as pistas
#     descreviam o diminutivo direito, o jogador chegava na medalha) — errado
#     era o CASAMENTO entre o que o enunciado promete e o que a fase cobra.
echo "--- 0o3) ENUNCIADO BATE (promete um assunto, cobra outro?) -"
portao "0o3 enunciado bate" python3 _qa/enunciado_bate.py "$PASTA"

# ⭐ 0o4) A MOLDURA CORTA A FIGURA? — nasceu de uma CORRECAO do Marcos
#     (set/2026). Ele disse "as imagens bola e elefante aparecem faltando
#     partes"; eu fui medir os ARQUIVOS e mostrei; e ele me corrigiu: *"nas
#     imagens que mostrou esta certo mas NA ATIVIDADE aparecem faltando"*.
#     Eu estava consertando a coisa errada. O culpado era o CSS: figura a 84%
#     dentro de uma bolinha REDONDA que esconde o que vaza — o circulo come os
#     cantos, e e ali que ficam a cauda do rato e as orelhas do elefante.
#     Isto e geometria fechada (o quadrado inscrito no circulo e 70,7%), entao
#     da para medir sem calibrar nada.
echo "--- 0o4) MOLDURA CORTA (o container come a figura?) -"
portao "0o4 moldura corta" python3 _qa/corta_figura.py "$ARQ"

# ⭐ 1w) ELEMENTO COBERTO — pedido do Marcos com todas as letras (set/2026):
#     *"a area de pintura fica em cima das cores... tipo de erros que seria
#     legal o profissional que criamos pegar"*. Da para pegar, e sem calibrar:
#     e geometria. No centro do botao, quem responde ao toque? Se e outro, o de
#     baixo esta inalcancavel — por mais bonito que pareca no print.
#     Os portoes que ja existiam nao viam: o leiaute mede TAMANHO (e os alvos
#     tinham 40px certos), o encaixe mede se cabe (e cabia), e a foto parece boa
#     porque a cor APARECE, com a bordinha de fora. So o gesto revela.
# ⭐ 0e) TEXTO DE EXEMPLO CHEGANDO A CRIANCA — achado montando a Gincana
#     (set/2026). O motor traz um PADRAO para cada gaveta de texto, e o padrao
#     era o assunto do EXEMPLO da peca. A fase de "escolher" fechava assim:
#         "Voce ja conhece as partes da planta!"
#     numa atividade de DIVISAO do 4o ano. Estava tambem na Expedicao do 5o,
#     no ar. O montador AVISAVA; ninguem media. Agora mede.
#     ⚠️ Nao e um grep: a maioria do texto de exemplo e a voz GENERICA da
#     mecanica e esta certa em qualquer atividade ("Digite quanto da."). Ele
#     so reprova quando o padrao cita o ASSUNTO do exemplo e esse assunto NAO
#     existe nesta atividade.
echo "--- 0e) TEXTO DE EXEMPLO (a crianca le o assunto de outra atividade?) -"
portao "0e texto de exemplo" python3 _qa/exemplo.py "$(dirname "$ARQ")"

echo "--- 1w) ELEMENTO COBERTO (o dedo alcanca o que ela quer tocar?) -"
portao "1w elemento coberto" node _qa/sobreposto.js "$ARQ"

# ⭐ 0o5) O OLHO NAS FIGURAS — e este NAO e um portao que decide: e um que MOSTRA.
#     Lacuna assumida (set/2026): o defeito "o recorte comeu um pedaco do
#     desenho" NAO tem medida confiavel. Eu tentei — buraco, fragmento, mordida
#     no casco, serrilhado — e cada regua que pegava a bola acusava a raposa do
#     Atelie, que esta perfeita (o "buraco" dela sao os olhos). Portao que grita
#     no certo ensina a ignorar portao.
#     Entao a banca nao finge medir: ela MONTA a folha de contato (todas as
#     figuras numa pagina, sobre xadrez, com nome) e imprime o caminho. Dez
#     segundos de olho decidem o que nenhuma conta decidiu — foi assim que o
#     Marcos pegou a bola e o elefante, e assim que confirmei a zebra.
#     ⚠️ Sai sempre com 0: ele nao reprova, ele CONVOCA. Se eu nao olhar, o
#     defeito passa — e a responsabilidade e minha, nao do portao.
echo "--- 0o5) OLHO NAS FIGURAS (contato-folha para inspecionar) -"
python3 _qa/figura_mordida.py "$PASTA" 2>&1 | grep -E "contato-folha|olhe primeiro|✗ " || true
echo "   ⚠️ ISTO NAO E APROVACAO: e um convite para OLHAR a folha acima antes de entregar."

# ⭐ 0p) A SEGUNDA LEITURA (portao de SENTIDO). Os portoes acima medem TEXTO
#    mecanico (digitacao, concordancia, HTML vazando). NENHUM le o SIGNIFICADO:
#    a resposta marcada como CERTA esta certa? a DICA leva a ELA? a VOZ diz o
#    mesmo que o texto? Isso so um LEITOR resolve. Aqui a banca MONTA o payload
#    (conteudo.json -> um bloco por fase) e o deixa gravado, com um aviso LOUD de
#    PENDENTE — nunca finge que a revisao de sentido aconteceu (seria confianca
#    falsa). Quem fecha o veredito e o revisor (LLM no entregar.yml, ou o Claude
#    na sessao lendo o payload). Ver o cabecalho de _qa/sentido.py.
if [ -f "$PASTA/conteudo.json" ]; then
  echo "--- 0p) SEGUNDA LEITURA DE SENTIDO (payload p/ o revisor) -"
  _SENT="$(mktemp -t sentido.XXXXXX.txt)"
  if python3 _qa/sentido.py "$PASTA" --out "$_SENT" >/dev/null 2>&1; then
    echo "  payload de sentido montado: $_SENT ($(grep -c '^FASE ' "$_SENT") fase(s))."
    echo "  ⚠️ REVISAO DE SENTIDO PENDENTE — isto NAO e aprovacao. Um revisor"
    echo "     (LLM/Claude) tem que LER o payload e responder, por fase: a CERTA"
    echo "     esta certa? a DICA leva a ela? a VOZ diz o mesmo que o texto?"
  else
    echo "  (nao consegui montar o payload de sentido — conferir conteudo.json)"
  fi
fi

echo
echo "--- 0l) A ARTE PEDIDA FOI DESENHADA? (lista de compras x pasta img/) -"
# ⚠️ nasceu de um defeito medido: o montador dizia "0 figura(s) a gerar" e a
#    atividade pedia DEZ que ninguem tinha mandado desenhar. Ver _qa/arte_pedida.py.
portao "0l arte pedida" python3 _qa/arte_pedida.py "$(dirname "$ARQ")"

echo
echo "--- 0m) TUDO O QUE FOI PEDIDO FOI ATENDIDO? (cobertura por objetivo) -"
# ⚠️ nasceu do erro que o MARCOS pegou, nao um portao: silabas com 10 fases e a
#    SEQUENCIA ALFABETICA — a primeira coisa que a professora pediu — com uma
#    mecanica so. Ver _qa/cobertura.py.
portao "0m cobertura" python3 _qa/cobertura.py "$ARQ"

echo
echo "--- 0n) A VOZ DIZ O QUE ESTA ESCRITO? (fala automatica + alto-falantes) -"
# ⚠️ nasceu do que o MARCOS ouviu, nao de portao nenhum: *"os botoes nao falam
#    o que esta escrito, e nao teve fala automatica, visto que os pequinos
#    precisam"* e, depois, *"tem que falar o que esta escrito"*. Medido na
#    Padaria: 1 fase narrava de 32, e 8 alto-falantes em cima de LETRA SOLTA
#    nao tocavam nada — numa atividade de alfabeto. Ver _qa/fala_o_escrito.js.
if [ "$REPARO" != "1" ]; then
colhe "0n a voz diz o escrito" "$TMPQ/g_falaescr.txt"
fi

echo
echo "--- 1b) FUNCAO QUE NAO EXISTE (estoura na mao da crianca?) -"
portao "1b funcao que nao existe" python3 _qa/funcoes.py "$ARQ"

echo
echo "--- 1c) RESTO DE CLONE (sobrou coisa da origem?) --"
portao "1c resto de clone" python3 _qa/clone.py "$ARQ"

echo; echo "--- 1g) BECO SEM SAIDA (a fase leva para a seguinte?) -"
# ⚠️ o defeito mais grave que a fabrica ja teve: a tela de BANCADA da peca
#    ("PECA FECHADA", botao "Jogar de novo") virando fim de linha na fase 3 de
#    32. O jogador nao pegava porque parava ali achando que era a medalha.
portao "1g beco sem saida" python3 _qa/beco.py "$ARQ"

echo; echo "--- 1h) VAZAMENTO (o conteudo cabe no proprio cartao?) -"
# ⚠️ LICAO PAGA (ago/2026): este portao existe desde que o Marcos viu *"o dizer
#    da figura fica fora do quadrado branco, ficou feio"* — e NUNCA rodava
#    sozinho: nao estava na banca, nem na bancada da peca, nem na esteira. So
#    rodava se alguem lembrasse de digitar. Portao que nao roda nao e portao.
#    Ligado, achou na primeira corrida: o alto-falante escapando 18px do cartao
#    da `arrastar-lugar`, em todos os tamanhos de tela.
if [ "$REPARO" != "1" ]; then
colhe "1h vazamento" "$TMPQ/g_vaza.txt"
fi

echo; echo "--- 1i) A FIGURA COMBINA COM A PALAVRA? -----------"
# ⚠️ o Marcos, olhando a tela: *"tem figuras que e por exemplo um abacate,
#    esta escrito ovo e o som esta ovo, tudo tem que corresponder"*. Estava
#    escrito no conteudo: "nome":"OVO" com "img":"pd_mamao".
portao "1i figura combina" python3 _qa/figura_certa.py "$(dirname "$ARQ")"
# citacao de curriculo o professor NAO tem como conferir sozinho — e e ela que
# ele leva para a coordenacao. Ver a licao no cabecalho do proprio portao.
portao "1k curriculo verbatim" python3 _qa/curriculo_verbatim.py "$(dirname "$ARQ")"

echo; echo "--- 1j) VOZ-ROBO (toda voz e gravada?) ------------"
# ⚠️ o Marcos: *"onde tenho que ouvir a palavra nao funciona"*. A ponte desliga
#    a voz do navegador (defeito anterior: duas vozes juntas) e a peca usava
#    justamente essa voz para dizer A PALAVRA. Conserto de um virou defeito do
#    outro — por isso este portao existe.
portao "1j voz-robo" python3 _qa/vozrobo.py "$ARQ"
# duas vozes juntas: o texto esta certo, o mp3 existe, a chave bate — o defeito
# e QUANTAS VEZES. Ver a licao no cabecalho do portao.
if [ "$REPARO" != "1" ]; then
colhe "1l voz dupla" "$TMPQ/g_vozdupla.txt"
fi

echo
echo "--- 1d) PROMESSA (a voz promete e a tela cumpre?) --"
portao "1d promessa" python3 _qa/promessa.py "$ARQ"

echo
echo "--- 2) ARQUITETO DE FLUXO (da para chegar ao fim?) -"
python3 _qa/fluxo.py "$ARQ" telaCapa || FALHOU=1

echo
echo "--- 3) DESIGNER (toda classe tem estilo de base?) --"
python3 _qa/classes.py "$ARQ" || FALHOU=1

echo
echo "--- 3b) PROGRESSAO (a barra so anda para a frente?) -"
portao "3b progressao" python3 _qa/progressao.py "$ARQ"

echo
echo "--- 3c) ARTE PROPRIA (imagem copiada de outra atividade?) -"
portao "3c arte propria" python3 _qa/arte_propria.py "$ARQ"

echo
echo "--- 3d) MASCOTE (ele treme ao falar ou piscar?) ---"
portao "3d mascote" python3 _qa/mascote.py "$ARQ"

echo "--- 3e) A VOZ E DA MESMA PESSOA QUE O MASCOTE? ------"
portao "3e voz do mascote" python3 _qa/voz_do_mascote.py "$PASTA"

echo "--- 3f) OS PARES DA MEMORIA FECHAM? ----------------"
portao "3f pares da memoria" python3 _qa/memoria_pares.py "$PASTA"

echo "--- 3g) A ATIVIDADE ENCHE A AULA? (pelo menos 40 min) -"
portao "3g duracao" python3 _qa/duracao.py "$PASTA"

echo "--- 3h) PLAQUINHA DUPLICADA (duas na mesma tela?) --"
if [ "$REPARO" != "1" ]; then colhe "3h selo unico" "$TMPQ/g_selo.txt"; fi

echo
if [ "$REPARO" != "1" ]; then
echo "--- 4) ACESSIBILIDADE (a crianca ENXERGA o texto?) -"
wait $PID_CON || FALHOU=1
cat "$TMPQ/contraste.txt"
fi

echo
if [ "$REPARO" != "1" ]; then
echo "--- 1f) ENCAIXE DA IMAGEM (esticada? cortada? perdida?) -"
colhe "1f encaixe" "$TMPQ/g_encaixe.txt"
fi

if [ "$REPARO" != "1" ]; then
echo "--- 1e) IMAGEM QUEBRADA (a figura aparece mesmo?) --"
wait $PID_IMG || FALHOU=1
cat "$TMPQ/imagens.txt"
fi

echo
echo "--- 4b) NARRACAO (a voz fala direito?) -------------"
# ⚠️ este portao lia SEMPRE o `_lote_falas.json` da raiz — um sobrado de outra
# atividade. Ele dizia "narracao ok" depois de conferir 34 falas alheias,
# enquanto as ~100 falas DESTA atividade passavam sem ninguem olhar. Falso
# "passou" e pior que reprovar. Agora le o falas.json DA PASTA.
if [ -f "$PASTA/falas.json" ]; then python3 _qa/falas.py "$PASTA/falas.json" || FALHOU=1
elif [ -f _lote_falas.json ]; then python3 _qa/falas.py _lote_falas.json || FALHOU=1
else echo "  (sem falas.json na pasta e sem _lote_falas.json)"; fi

echo
if [ "$REPARO" != "1" ]; then
echo "--- 5) LEIAUTE (cabe na tela? da para tocar?) ------"
wait $PID_LEI || FALHOU=1
cat "$TMPQ/leiaute.txt"
fi

echo
echo "--- 5b) DIRETOR DE ARTE (o acabamento esta impecavel?) -"
# ⚠️ nasceu do que o MARCOS pediu quatro vezes seguidas: "profissional, lindo,
#    sem erros", "maravilhoso, impecavel", "sempre subir a regua", "crie um
#    profissional especialista para isso". Os outros portoes medem se FUNCIONA;
#    este mede se esta BONITO — botao sobre palavra, quadrado branco chapado,
#    fileira torta, botao esticado, texto espremido. Ver _qa/visual.js.
if [ "$REPARO" != "1" ]; then
colhe "5b diretor de arte" "$TMPQ/g_visual.txt"
fi

echo
echo "--- 6) JOGADOR (joga sozinho ate a medalha) --------"
# ⚡ PARALELO por segmento (joga_par): agora que os outros navegadores ja
#    fecharam, os 3 trechos correm SOZINHOS — rapido (~110s no lugar de ~5min) E
#    confiavel (sem briga por CPU, que era o que fazia o jogador "empacar" numa
#    fase boa). Atividade escrita a mao (sem conteudo.json com fases) cai no
#    jogador serial (joga_par sai 2 = "nao da para segmentar").
if [ "$REPARO" != "1" ]; then
wait $PID_JOG || FALHOU=1
tail -6 "$TMPQ/jogador.txt"
fi

echo
# ⚠️ O ERRADOR NAO ENTRA AQUI. Eu o liguei nesta banca e ele reprovava TUDO,
#    inclusive as atividades no ar: ele escolhe a receita pelo NOME DO ARQUIVO, e
#    numa atividade o arquivo se chama `index.html` — receita nenhuma. Ele e da
#    BANCADA DA PECA (`_qa/peca.sh`), onde o nome do arquivo E o nome da mecanica.
#    A licao: portao no lugar errado nao e portao a mais, e portao que mente.

echo
if [ -n "$CEGOS" ]; then
  echo "--- ⚠️ PORTOES QUE RODARAM CEGOS (mediram ZERO) ------"
  echo "  aprovacao vazia da confianca falsa. Conferir se a atividade realmente"
  echo "  nao tem aquilo — ou se o portao deixou de enxergar:$CEGOS"
fi

echo "==================================================="
if [ "$REPARO" = "1" ]; then
  if [ "$FALHOU" = "0" ]; then
    echo " REPARO: os portoes de TEXTO passaram. ISTO NAO E APROVACAO —"
    echo " falta a banca inteira (navegador: contraste, leiaute, imagem,"
    echo " acabamento, jogador e a colheita da voz)."
  else
    echo " REPARO REPROVOU — e o barato ja pegou. Conserte e rode de novo."
  fi
elif [ "$FALHOU" = "0" ]; then
  echo " BANCA APROVOU. Falta so o PROFESSOR (portao final)."
else
  echo " BANCA REPROVOU — conserte antes de mostrar ao Marcos."
fi
echo "==================================================="
rm -rf "$TMPQ"
exit $FALHOU
