#!/usr/bin/env bash
# ============================================================
#  A PROVA DOS PORTÕES — "quem vigia o vigia?"
#
#  Esta semana (ago/2026) TRÊS portões da casa estavam CEGOS ao mesmo tempo, e
#  os três APROVAVAM:
#    · `imagens.js`  — dependia de uma função (`srcDe`) que nunca existiu no
#      motor, então devolvia lista vazia e imprimia "imagens ok" enquanto duas
#      poses do mascote davam 404;
#    · `funcoes.py`  — contava como "função que não existe" a chamada PROTEGIDA
#      por `typeof`, que é o idioma da casa, e reprovava peça certa;
#    · `promessa.py` — procurava `function ajuda(n,ops){` (a forma do Broto) e
#      não via `window.ajuda = function(n, ops){` (a forma do esqueleto), então
#      dizia "nada a conferir" em TODA atividade montada.
#
#  A conclusão é desconfortável e é o motivo deste arquivo: **um portão que
#  aprova não prova nada enquanto não se mostrar que ele REPROVA o defeito que
#  ele existe para pegar.** Código 0 sem isso é confiança, não medida.
#
#  Como funciona: para cada portão, planta-se o defeito HISTÓRICO — o que
#  chegou até o Marcos de verdade — num arquivo de mentira, e exige-se que o
#  portão saia com código != 0. E, onde já houve falso-positivo, planta-se
#  também o caso CERTO e exige-se código 0: portão que grita à toa ensina a
#  ignorar portão.
#
#  Uso:  bash _qa/provar_portoes.sh
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/.."
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
falhou=0

# pega(<nome>, <esperado: PEGA|DEIXA>, <arquivo>, <comando...>)
pega(){
  local nome="$1" esperado="$2"; shift 2
  "$@" > "$T/saida.txt" 2>&1
  local cod=$?
  if [ "$esperado" = "PEGA" ]; then
    if [ "$cod" != "0" ]; then echo "   ok      $nome (reprovou o defeito, como devia)"
    else echo "   CEGO    $nome — o defeito passou! codigo 0"; falhou=1; fi
  else
    if [ "$cod" = "0" ]; then echo "   ok      $nome (deixou passar o codigo CERTO)"
    else echo "   GRITOU  $nome — acusou o inocente:"; sed -n '1,4p' "$T/saida.txt" | sed 's/^/           /'; falhou=1; fi
  fi
}

echo "=== A PROVA DOS PORTOES — cada um contra o defeito que ele existe para pegar"

# ---------- 1) FUNCOES: chamada de funcao que nao existe ----------
cat > "$T/f_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function comeca(){ naoExisteEmLugarNenhum(); }
</script></body></html>
H
pega "funcoes  · funcao inexistente"  PEGA  python3 _qa/funcoes.py "$T/f_ruim.html"
# o falso-positivo que ele JA deu: chamada protegida por typeof e o idioma da casa
cat > "$T/f_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function comeca(){ if(typeof sPega==="function") sPega(); }
</script></body></html>
H
pega "funcoes  · chamada protegida"   DEIXA python3 _qa/funcoes.py "$T/f_bom.html"

# ---------- 2) PROMESSA: a voz promete e a tela nao cumpre ----------
cat > "$T/p_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
window.ajuda = function(n, ops){
  ops = ops || {};
  if(n === 1){ if(ops.dica) mostraDica(ops.dica); }
  else if(n === 2){ falar("dc_ajuda2"); if(ops.concreto) ops.concreto(); }
};
function fase1(){ ajuda(2, {dica:"olhe bem"}); }
</script></body></html>
H
pega "promessa · voz promete, tela nao cumpre" PEGA python3 _qa/promessa.py "$T/p_ruim.html"

# ---------- 3) DINAMICAS: prosa em comentario nao pode virar gatilho ----------
# ⚠️ o fixture do `dinamicas` nasceu ERRADO e o portao estava certo: eu tinha
#    posto `.opt` + opcoes, entao ele reconheceu um QUIZ de verdade e cobrou o
#    embaralhamento — cobranca legitima. O que se quer provar aqui e outra
#    coisa: que uma CITACAO em comentario nao vira gatilho. Entao o arquivo nao
#    pode parecer mecanica nenhuma.
cat > "$T/d_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
/* comentario que CITA a peca `ouvir-achar` e o `tocaAlvo` dela, so isso */
.caixinha{display:block}
</style></head><body><script>
function pecaX(){ var o=document.createElement("div"); o.className="caixinha"; }
</script></body></html>
H
pega "dinamicas· citacao em comentario"  DEIXA python3 _qa/dinamicas.py "$T/d_bom.html"

# ---------- 4) CLONE: resto de outra atividade ----------
# ⚠️ o `clone` descobre o prefixo pelos ARQUIVOS de `img/` — um HTML solto nao
#    basta, e ele (agora) DIZ que nao mediu em vez de pular calado. Entao o
#    fixture monta duas pastas vizinhas, como no repositorio de verdade.
mkdir -p "$T/_ativ/img" "$T/_outra/img"
for n in pao bolo mel sal queijo; do : > "$T/_ativ/img/pd_$n.png"; done
for n in broto folha raiz terra sol;  do : > "$T/_outra/img/jd_$n.png"; done
cat > "$T/_ativ/index.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
var ID = {pre:"pd", mascote:"fuba"};
var IMGS = ["pd_pao","jd_broto_feliz"];
</script></body></html>
H
pega "clone    · prefixo de outra atividade" PEGA python3 _qa/clone.py "$T/_ativ/index.html"

echo "-----------------------------------------------------------"
if [ "$falhou" = "0" ]; then
  echo " OS PORTOES PROVAM O QUE DIZEM — cada um reprovou o seu defeito."
else
  echo " ⛔ HA PORTAO CEGO (ou gritando a toa). Conserte ANTES de confiar num codigo 0."
fi
exit "$falhou"
