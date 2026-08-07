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
ARQ="${1:-}"
if [ -z "$ARQ" ]; then echo "uso: bash _qa/auditar.sh <arquivo.html> [tela1 tela2 ...]"; exit 2; fi
shift || true
TELAS="$*"

if [ -z "$TELAS" ]; then
  TELAS=$(python3 - "$ARQ" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
js="".join(re.findall(r"<script>(.*?)</script>",h,re.S))
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
  if [ "$st" != "0" ]; then FALHOU=1; fi
  if printf '%s' "$saida" | grep -qE '\-> *0 |0 fase\(s\)|0 dica\(s\)|0 alvo\(s\)|[Nn]ada a conferir'; then
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
node _qa/contraste.js "$ARQ" $TELAS > "$TMPQ/contraste.txt" 2>&1 & PID_CON=$!
node _qa/leiaute.js   "$ARQ" $TELAS > "$TMPQ/leiaute.txt"   2>&1 & PID_LEI=$!
node _qa/imagens.js   "$ARQ" $TELAS > "$TMPQ/imagens.txt"   2>&1 & PID_IMG=$!

echo
echo "--- 1) ENGENHEIRO (o codigo roda?) -----------------"
python3 - "$ARQ" > "$JSTMP" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
if node --check "$JSTMP" >/dev/null 2>&1; then echo "  JS ok (node --check)"; else echo "  ERRO DE SINTAXE NO JS"; node --check "$JSTMP"; FALHOU=1; fi

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
if grep -q "pecabox" "$ARQ" && grep -q "MEC\[" "$ARQ"; then
  echo "--- 0f2) VOZ DA RODADA, MEDIDA JOGANDO (atividade montada) -"
  python3 _padrao/ESQUELETO/colher.py "$(dirname "$ARQ")" --so-ver || FALHOU=1
fi
echo "--- 0g) VOZ IGUAL AO TEXTO (o audio diz o que esta escrito?) -"
portao "0g voz igual ao texto" node _qa/vozigual.js "$ARQ"
echo "--- 0h) INTRO CALANDO A PERGUNTA (a 1a rodada e falada?) -"
portao "0h intro calando a pergunta" python3 _qa/vozintro.py "$ARQ"
echo "--- 0i) VOZ SEM MP3 (a fase ficou muda de vez?) -"
portao "0i voz sem mp3" python3 _qa/vozfalta.py "$ARQ"
echo "--- 0j) VOZ DA DICA (a dica fala o que esta escrito?) -"
portao "0j voz da dica" python3 _qa/vozdica.py "$ARQ"

echo
echo "--- 1b) FUNCAO QUE NAO EXISTE (estoura na mao da crianca?) -"
portao "1b funcao que nao existe" python3 _qa/funcoes.py "$ARQ"

echo
echo "--- 1c) RESTO DE CLONE (sobrou coisa da origem?) --"
portao "1c resto de clone" python3 _qa/clone.py "$ARQ"

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

echo
echo "--- 4) ACESSIBILIDADE (a crianca ENXERGA o texto?) -"
wait $PID_CON || FALHOU=1
cat "$TMPQ/contraste.txt"

echo
echo "--- 1f) ENCAIXE DA IMAGEM (esticada? cortada? perdida?) -"
node _qa/encaixe.js "$ARQ" $TELAS || FALHOU=1

echo "--- 1e) IMAGEM QUEBRADA (a figura aparece mesmo?) --"
wait $PID_IMG || FALHOU=1
cat "$TMPQ/imagens.txt"

echo
echo "--- 4b) NARRACAO (a voz fala direito?) -------------"
if [ -f _lote_falas.json ]; then python3 _qa/falas.py _lote_falas.json || FALHOU=1; else echo "  (sem _lote_falas.json)"; fi

echo
echo "--- 5) LEIAUTE (cabe na tela? da para tocar?) ------"
wait $PID_LEI || FALHOU=1
cat "$TMPQ/leiaute.txt"

echo
echo "--- 6) JOGADOR (joga sozinho ate a medalha) --------"
# ⚠️ este roda SOZINHO, no fim. Ele joga a partida inteira com pausas de 230ms
# entre os toques; disputando o processador com os outros tres navegadores, a
# tela nao acompanhava e ele dava "preso" numa fase que funciona (ago/2026).
# Portao que reprova por lentidao do proprio auditor e pior que portao nenhum.
node _qa/jogador.js "$ARQ" > "$TMPQ/jogador.txt" 2>&1 || FALHOU=1
tail -6 "$TMPQ/jogador.txt"

echo
echo "--- 7) ERRADOR (erra de proposito: da para seguir?) -"
# ⚠️ ESTE PORTAO EXISTIA E NAO ESTAVA NA BANCA. Ele joga cada mecanica ERRANDO
#    de proposito 3 vezes e confere que a medalha continua alcancavel — que e o
#    andaime da casa (dica -> apoio -> revela, e nunca travar). Os cinco piores
#    defeitos de um dia inteiro passaram pelos outros oito portoes e so ele viu.
node _qa/errador.js "$ARQ" > "$TMPQ/errador.txt" 2>&1 || FALHOU=1
tail -8 "$TMPQ/errador.txt"

echo
if [ -n "$CEGOS" ]; then
  echo "--- ⚠️ PORTOES QUE RODARAM CEGOS (mediram ZERO) ------"
  echo "  aprovacao vazia da confianca falsa. Conferir se a atividade realmente"
  echo "  nao tem aquilo — ou se o portao deixou de enxergar:$CEGOS"
fi

echo "==================================================="
if [ "$FALHOU" = "0" ]; then
  echo " BANCA APROVOU. Falta so o PROFESSOR (portao final)."
else
  echo " BANCA REPROVOU — conserte antes de mostrar ao Marcos."
fi
echo "==================================================="
rm -rf "$TMPQ"
exit $FALHOU
