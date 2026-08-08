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

# ---------- 5) VISUAL: botao esticado (a opcao que virou fita) ----------
# Este e o defeito que eu consertei TRES vezes na mao (escolher, completar,
# intruso) antes de a conta subir para o motor: opcao de 400x55 = 7,3 vezes
# mais larga que alta. O teto do diretor de arte e 6.
molde(){ # molde(<largura>, <altura-minima>) -> html de tres opcoes empilhadas
cat <<H
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
body{margin:0;background:#2b2118;font-family:Arial,sans-serif}
#app{max-width:520px;margin:0 auto;padding:12px}
.opts{display:flex;flex-direction:column;align-items:center;gap:10px;width:100%;max-width:$1}
.opt{width:100%;background:#fffdf6;color:#221a12;border:2px solid #6b5a3a;border-radius:18px;
     padding:14px 16px;min-height:$2;font-size:16px;font-weight:600;text-align:center}
</style></head><body><div id="app"><div class="opts">
<div class="opt">massa</div><div class="opt">forno</div><div class="opt">farinha</div>
</div></div></body></html>
H
}
molde 400px 0   > "$T/v_ruim.html"
molde 360px 62px > "$T/v_bom.html"
pega "visual   · opcao esticada (fita)"   PEGA  node _qa/visual.js "$T/v_ruim.html"
pega "visual   · opcao no molde do motor" DEIXA node _qa/visual.js "$T/v_bom.html"

# ---------- 6) IMAGENS: a figura que a crianca nao ve ----------
# ESTE e o portao que comecou tudo: rodava cego (dependia de `srcDe`, que nunca
# existiu no motor) e imprimia "imagens ok" enquanto duas poses do mascote
# davam 404. Agora ele tem prova — nos tres caminhos que ele confere:
# a pre-carga (IMGS), o <img> da tela e o fundo por CSS.
mkdir -p "$T/_fig/img"
# um PNG 1x1 de verdade, para o caso CERTO ter o que carregar
python3 - "$T/_fig/img/pd_pao.png" <<'PY'
import base64,sys
open(sys.argv[1],"wb").write(base64.b64decode(
 "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="))
PY
fig(){ # fig(<nome-na-pre-carga>, <src-do-img>, <fundo-css>)
cat <<H
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
#app{width:300px;height:200px;background-image:url("$3");background-size:cover}
</style></head><body><div id="app"><img src="$2" alt="pao"></div><script>
var IMGS=["$1"];
function telaCapa(){ document.getElementById("app").innerHTML='<img src="$2" alt="pao">'; }
</script></body></html>
H
}
fig pd_pao      img/pd_pao.png    img/pd_pao.png    > "$T/_fig/bom.html"
fig pd_naoexiste img/pd_pao.png   img/pd_pao.png    > "$T/_fig/ruim_pre.html"
fig pd_pao      img/pd_sumiu.png  img/pd_pao.png    > "$T/_fig/ruim_img.html"
fig pd_pao      img/pd_pao.png    img/pd_fundo.png  > "$T/_fig/ruim_css.html"
pega "imagens  · pre-carga com 404"      PEGA  node _qa/imagens.js "$T/_fig/ruim_pre.html" telaCapa
pega "imagens  · <img> que nao carrega"  PEGA  node _qa/imagens.js "$T/_fig/ruim_img.html" telaCapa
pega "imagens  · fundo CSS que nao vem"  PEGA  node _qa/imagens.js "$T/_fig/ruim_css.html" telaCapa
pega "imagens  · tudo no lugar"          DEIXA node _qa/imagens.js "$T/_fig/bom.html"      telaCapa

# ---------- 7) PROGRESSAO: a barra que anda para tras ----------
# Defeito medido em TRES atividades no ar (Legenda 68%->48%, Redacao 50%->46%,
# Doceria 92%->91%): fase inserida depois, ninguem renumerou as vizinhas.
barra(){ # barra(<prog da 1a>, <prog da 2a>)
cat <<H
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function faseA(){ limpa(); var t=el("div","tela"); setProg(t,$1); mostraBanner("boa!", faseB); }
function faseB(){ limpa(); var t=el("div","tela"); setProg(t,$2); }
</script></body></html>
H
}
barra 68 48 > "$T/b_ruim.html"
barra 48 68 > "$T/b_bom.html"
pega "progress.· barra volta para tras" PEGA  python3 _qa/progressao.py "$T/b_ruim.html"
pega "progress.· barra so avanca"       DEIXA python3 _qa/progressao.py "$T/b_bom.html"

# ---------- 8) TELA VAZIA: o fundo falando sozinho ----------
# Palavras do Marcos: *"quando conclui, fica so a tela de fundo e falando, fica
# feio"*. Eram 23 fases com o mesmo molde.
cat > "$T/tv_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function passo(){
  limpa();
  if(idx>=LISTA.length){
    depoisDaFala("pd_revela",13000,function(){ mostraBanner("Muito bem!", proxima); });
    return;
  }
}
</script></body></html>
H
cat > "$T/tv_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function passo(){
  limpa();
  if(idx>=LISTA.length){
    fechaFase("A PADARIA","Voce leu todas as placas!","pd_revela",13000,proxima,60);
    return;
  }
}
</script></body></html>
H
pega "telavazia· fundo falando sozinho" PEGA  python3 _qa/telavazia.py "$T/tv_ruim.html"
pega "telavazia· fecho com fechaFase"   DEIXA python3 _qa/telavazia.py "$T/tv_bom.html"

# ---------- 9) CLASSES: classe que so existe dentro de @media ----------
# Foi o `.pchip` do caca-palavras: na tela normal a lista virou texto solto.
# O caso CERTO tem o comentario que ja derrubou este portao (um comentario de
# CSS terminando com a palavra @media engolia a regra de baixo).
cat > "$T/c_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
.tela{display:block}
@media (max-width:400px){ .pchip{display:inline-block;padding:4px 8px} }
</style></head><body><script>
function desenha(){ var x=el("div","pchip","MASSA"); }
</script></body></html>
H
cat > "$T/c_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
.tela{display:block}
/* a lista de palavras achadas; encolhe no celular, ver o @media */
.pchip{display:inline-block;padding:4px 8px}
@media (max-width:400px){ .pchip{padding:3px 6px} }
</style></head><body><script>
function desenha(){ var x=el("div","pchip","MASSA"); }
</script></body></html>
H
pega "classes  · so dentro de @media"   PEGA  python3 _qa/classes.py "$T/c_ruim.html"
pega "classes  · comentario com @media" DEIXA python3 _qa/classes.py "$T/c_bom.html"

# ---------- 10) FALAS: a palavra que a voz erra ----------
# O Marcos OUVIU "complite" duas vezes (Redacao e Doceria). A voz so da para
# conferir depois de publicada — este portao pega antes de gravar.
echo '[{"id":"pd_f01","texto":"Complete a palavra com a letra que falta."}]' > "$T/fl_ruim.json"
echo '[{"id":"pd_f01","texto":"Preencha a palavra com a letra que falta."}]' > "$T/fl_bom.json"
pega "falas    · palavra que a voz erra" PEGA  python3 _qa/falas.py "$T/fl_ruim.json"
pega "falas    · texto ja trocado"       DEIXA python3 _qa/falas.py "$T/fl_bom.json"

echo "-----------------------------------------------------------"
if [ "$falhou" = "0" ]; then
  echo " OS PORTOES PROVAM O QUE DIZEM — cada um reprovou o seu defeito."
else
  echo " ⛔ HA PORTAO CEGO (ou gritando a toa). Conserte ANTES de confiar num codigo 0."
fi
exit "$falhou"
