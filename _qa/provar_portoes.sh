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
# e o caso certo: o degrau 2 mostra mesmo o apoio concreto
cat > "$T/p_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
window.ajuda = function(n, ops){
  ops = ops || {};
  if(n === 1){ if(ops.dica) mostraDica(ops.dica); }
  else if(n === 2){ falar("dc_ajuda2"); if(ops.concreto) ops.concreto(); }
};
function fase1(){ ajuda(2, {dica:"olhe bem", concreto:function(){ mostraApoio(); }}); }
</script></body></html>
H
pega "promessa · a tela cumpre o prometido" DEIXA python3 _qa/promessa.py "$T/p_bom.html"

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
# e o defeito de verdade dele: quiz com as opcoes SEMPRE na mesma ordem — a
# crianca decora a posicao em vez do conteudo (armadilha registrada no
# `_padrao/DINAMICAS.md`).
cat > "$T/d_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
.opts{display:block}.opt{display:block;min-height:48px}
</style></head><body><script>
function quiz(f,cen,fim){
  var ops=f.opcoes, box=el("div","opts"), i;
  for(i=0;i<ops.length;i++){
    var o=el("div","opt",ops[i].n);
    o.onclick=function(){ if(this.certo){ sCerto(); fim(); } else { sErro(); ajuda(1); } };
    box.appendChild(o);
  }
  cen.appendChild(box);
}
</script></body></html>
H
pega "dinamicas· quiz sem embaralhar"     PEGA  python3 _qa/dinamicas.py "$T/d_ruim.html"

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
# e o caso certo: so o prefixo da propria pasta
cat > "$T/_ativ/limpo.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
var ID = {pre:"pd", mascote:"fuba"};
var IMGS = ["pd_pao","pd_bolo","pd_mel"];
</script></body></html>
H
pega "clone    · so a arte da propria pasta" DEIXA python3 _qa/clone.py "$T/_ativ/limpo.html"

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

# ---------- 11) FLUXO: a crianca presa e a tela orfa ----------
# Aconteceu no gLigar (ago/2026): `mostraBanner(..., gLigar)` em vez de
# `gBanca` — a fase voltava para si mesma e a missao inteira de Generos ficou
# inalcancavel atras dela.
cat > "$T/fx_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function telaCapa(){ limpa(); mostraBanner("vamos!", gLigar); }
function gLigar(){ limpa(); mostraBanner("boa!", gLigar); }
function gBanca(){ limpa(); mostraBanner("fim", telaCapa); }
</script></body></html>
H
cat > "$T/fx_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function telaCapa(){ limpa(); mostraBanner("vamos!", gLigar); }
function gLigar(){ limpa(); mostraBanner("boa!", gBanca); }
function gBanca(){ limpa(); mostraBanner("fim", telaCapa); }
</script></body></html>
H
pega "fluxo    · presa em si + orfa"   PEGA  python3 _qa/fluxo.py "$T/fx_ruim.html" telaCapa
pega "fluxo    · caminho ate o fim"    DEIXA python3 _qa/fluxo.py "$T/fx_bom.html"  telaCapa

# ---------- 12) CONTRASTE: o texto que some no fundo ----------
# Pedido do Marcos: *"sempre verificar se nao ha um contraste nas cores, para
# que nao aconteca de a crianca nao conseguir enxergar"*. Ele mede o PIXEL
# atras do texto, nao o CSS — por isso o fixture pinta o fundo de verdade.
cor(){ # cor(<cor do texto>)
cat <<H
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
body{margin:0;background:#fdf6e3}
#app{padding:24px}
.balao{background:#fdf6e3;color:$1;font-size:17px;font-weight:600;padding:14px}
</style></head><body><div id="app"></div><script>
function telaCapa(){ document.getElementById("app").innerHTML=
  '<div class="balao">Escolha a placa que tem o som do P.</div>'; }
telaCapa();
</script></body></html>
H
}
cor "#f6efdc" > "$T/k_ruim.html"     # creme sobre creme: 1,1:1 — a crianca nao le
cor "#241c0c" > "$T/k_bom.html"      # marrom escuro sobre creme
pega "contraste· texto que some no fundo" PEGA  node _qa/contraste.js "$T/k_ruim.html" telaCapa
pega "contraste· texto legivel"           DEIXA node _qa/contraste.js "$T/k_bom.html"  telaCapa

# ---------- 13) LEIAUTE: o alvo pequeno demais para o dedo ----------
# Regra da casa: alvo de toque >= 44px (>= 40 dentro de grade). Abaixo disso a
# crianca de 6 anos erra o botao e culpa a si mesma.
alvo(){ # alvo(<altura>)
cat <<H
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
body{margin:0;background:#2b2118}
#app{padding:16px}
.opts{display:flex;flex-direction:column;align-items:center;gap:10px;max-width:360px}
.opt{width:100%;background:#fffdf6;color:#221a12;border-radius:16px;text-align:center;
     font-size:15px;height:$1;line-height:$1}
</style></head><body><div id="app"></div><script>
function telaCapa(){ document.getElementById("app").innerHTML=
  '<div class="opts"><div class="opt">massa</div><div class="opt">forno</div></div>'; }
telaCapa();
</script></body></html>
H
}
alvo 26px > "$T/a_ruim.html"
alvo 62px > "$T/a_bom.html"
pega "leiaute  · alvo pequeno para o dedo" PEGA  node _qa/leiaute.js "$T/a_ruim.html" telaCapa
pega "leiaute  · alvo do tamanho da casa"  DEIXA node _qa/leiaute.js "$T/a_bom.html"  telaCapa

# ---------- 14) VOZFALTA: o texto escrito e o mp3 que ninguem gravou ----------
# Palavras do Marcos: *"na cruzadinha do 3º ano os audios e o botao 'ouvir de
# novo' nao funcionam"*. O 404 do mp3 e SILENCIOSO: o motor segue em frente e a
# fase inteira fica muda para quem ainda nao le.
mkdir -p "$T/_voz/audio" "$T/_vozb/audio"
for d in _voz _vozb; do
cat > "$T/$d/index.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function fase1(){ falaDaTela("pd_f01"); }
</script></body></html>
H
echo '[{"id":"pd_f01","texto":"Escolha a placa que comeca com P."}]' > "$T/$d/falas.json"
done
: > "$T/_vozb/audio/pd_f01.mp3"          # o certo: a voz foi gravada
pega "vozfalta· texto escrito, mp3 ausente" PEGA  python3 _qa/vozfalta.py "$T/_voz/index.html"
pega "vozfalta· voz gravada"                DEIXA python3 _qa/vozfalta.py "$T/_vozb/index.html"

# ---------- 15) VOZDICA: a dica falada nao e a dica escrita ----------
# Pedido do Marcos: *"o som que e falado tem que ser o mesmo do texto"*. Ja
# aconteceu de a dica dizer "de cima voce ve o telhado" numa tela sem telhado.
mkdir -p "$T/_dic" "$T/_dicb"
for d in _dic _dicb; do
cat > "$T/$d/index.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function fase1(){ montaBarra("pd_d01","Olhe a primeira letra da palavra."); }
</script></body></html>
H
done
echo '[{"id":"pd_d01","texto":"De cima voce ve o telhado, nunca a porta."}]' > "$T/_dic/falas.json"
echo '[{"id":"pd_d01","texto":"Olhe a primeira letra da palavra."}]'        > "$T/_dicb/falas.json"
pega "vozdica · a voz diz outra coisa"  PEGA  python3 _qa/vozdica.py "$T/_dic/index.html"
pega "vozdica · voz igual ao escrito"   DEIXA python3 _qa/vozdica.py "$T/_dicb/index.html"

# ---------- 16) ARTE PROPRIA: o avatar emprestado ----------
# O Marcos pegou no olho: os avatares do Observatorio do Orbi eram os brotinhos
# verdes do Jardim, no meio de um ceu estrelado. Clonar o MOTOR e obrigatorio;
# clonar a ARTE e proibido.
# ⚠️ este portao varre as pastas irmas a partir do diretorio ATUAL — por isso o
#    fixture roda com o cwd DENTRO da area de teste, senao ele compararia com as
#    atividades de verdade do repositorio.
RAIZ="$PWD"
mkdir -p "$T/_uma/img" "$T/_outraA/img" "$T/_soa/img"
: > "$T/_uma/index.html"; : > "$T/_outraA/index.html"; : > "$T/_soa/index.html"
python3 - "$T/_uma/img/av1.png" "$T/_outraA/img/broto.png" "$T/_soa/img/av1.png" <<'PY'
import base64,sys
mesmo = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
outro = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
open(sys.argv[1],"wb").write(mesmo)   # _uma  : avatar
open(sys.argv[2],"wb").write(mesmo)   # _outraA: MESMOS bytes = copiado
open(sys.argv[3],"wb").write(outro)   # _soa  : arte propria
PY
pega "arte     · avatar copiado de outra"  PEGA  bash -c 'cd "$1" && python3 "$2/_qa/arte_propria.py" _uma'  _ "$T" "$RAIZ"
pega "arte     · arte propria"             DEIXA bash -c 'cd "$1" && python3 "$2/_qa/arte_propria.py" _soa'  _ "$T" "$RAIZ"

# ---------- 17) AMBIGUO: "a ponte" quando ha DUAS pontes ----------
# Palavras do Marcos: *"fica confuso porque tem DUAS pontes"* — e o recado que
# fecha: *"esses erros nao podem passar"*. Artigo definido singular declarando
# duas zonas e a propria tela confessando que ha duas.
cat > "$T/am_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
var ACHE = [
  { q:"a <b>ponte</b>", z:[{x:120,y:80},{x:260,y:150}] },
  { q:"Toque na <b>igreja</b>", z:[{x:40,y:40},{x:90,y:70}] }
];
</script></body></html>
H
cat > "$T/am_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
var ACHE = [
  { q:"uma <b>ponte</b>", z:[{x:120,y:80},{x:260,y:150}] },
  { q:"o <b>rio</b>", unico:1, z:[{x:10,y:20},{x:60,y:90}] }
];
</script></body></html>
H
pega "ambiguo · 'a ponte' com duas pontes" PEGA  python3 _qa/ambiguo.py "$T/am_ruim.html"
pega "ambiguo · 'uma ponte' com duas"      DEIXA python3 _qa/ambiguo.py "$T/am_bom.html"

# ---------- 18) VOZINTRO: a intro que cala a primeira pergunta ----------
# O Marcos achou UMA fase (*"no mapa do bairro o simbolo escola nao e falado"*).
# Quando fui medir, eram 27 — sempre a PRIMEIRA rodada.
# ⚠️ o caso CERTO tem o `falaDaTela` dentro de um onclick, que foi o falso
#    alarme pago: ordem de arquivo nao e ordem de tempo.
cat > "$T/vi_ruim.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function passo(){
  var t=el("div","tela");
  falaDaTela("pd_q0");
  if(idx===0) falar("pd_intro");
}
</script></body></html>
H
cat > "$T/vi_bom.html" <<'H'
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function passo(){
  var t=el("div","tela");
  if(idx===0) introEPergunta("pd_q0"); else falaDaTela("pd_q0");
  t.onclick=function(){ falaDaTela("pd_q0"); };
}
</script></body></html>
H
pega "vozintro· intro por cima da pergunta" PEGA  python3 _qa/vozintro.py "$T/vi_ruim.html"
pega "vozintro· introEPergunta + onclick"   DEIXA python3 _qa/vozintro.py "$T/vi_bom.html"

# ---------- 19) PADRAO DA CASA: o leque de gestos ----------
# Cobranca do Marcos na Legenda do Clique: *"tem muita dinamica parecida...
# temos um leque bem grande de interatividade"*. La eram 8 das 19 fases com o
# MESMO gesto. A regua: nenhum gesto acima de 40%, minimo de 4 gestos, e
# nenhuma fase muda.
# ⚠️ o caso CERTO aqui e uma atividade DE VERDADE (a _prova30, montada pela
#    esteira). Fixture de mentira nao prova que o portao funciona no que ele
#    vai medir amanha.
python3 - "$T/pd_ruim.html" <<'PYX'
import io, json, sys
fases = [{"id": "f%02d" % i, "mec": "escolher", "selo": "PASSO",
          "enunciado": "Qual e?", "vozIntro": "pd_f%02d" % i} for i in range(1, 11)]
io.open(sys.argv[1], "w", encoding="utf-8").write(
    '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>\n'
    'var FASES = ' + json.dumps(fases, ensure_ascii=False) + ';\n'
    '</script></body></html>\n')
PYX
pega "padrao   · um gesto so (10 de 10)"  PEGA  python3 _qa/padrao.py "$T/pd_ruim.html"
pega "padrao   · leque da _prova30"       DEIXA python3 _qa/padrao.py _prova30/index.html

# ---------- 20) EXPLICA: a fase exige um atributo e nao diz qual ----------
# Palavras do Marcos, no "Monte o seu prato": *"mesmo colocando os cinco
# alimentos que se pede, nao passa a fase"*. A regra da fase estava certa (5
# PARTES diferentes da planta); o enunciado e que nao dizia "parte" — e 82% das
# crianças que faziam o que a tela parecia pedir ficavam paradas.
mkdir -p "$T/_exp" "$T/_expb"
prato(){ # prato(<enunciado>)
cat <<H
<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><script>
function telaPrato(){
  limpa();
  var b = el("div","balao","$1");
  falar("jd_prato_intro");
  function conta(){
    var vis={}, n=0, z;
    for(z=0;z<noPrato.length;z++){
      if(!vis[noPrato[z].it.parte]){ vis[noPrato[z].it.parte]=1; n++; }
    }
    if(n>=5) fim();
  }
}
</script></body></html>
H
}
prato "Monte o seu prato com 5 alimentos." > "$T/_exp/index.html"
prato "Ponha no prato 5 partes diferentes da planta." > "$T/_expb/index.html"
echo '[{"id":"jd_prato_intro","texto":"Monte o seu prato com cinco alimentos."}]' > "$T/_exp/falas.json"
echo '[{"id":"jd_prato_intro","texto":"Ponha no prato cinco partes diferentes da planta."}]' > "$T/_expb/falas.json"
pega "explica · exige atributo sem dizer"  PEGA  python3 _qa/explica.py "$T/_exp/index.html"
pega "explica · enunciado e voz explicam"  DEIXA python3 _qa/explica.py "$T/_expb/index.html"

# ---------- 21) "NAO MEDI" NAO E "PASSOU" ----------
# A regra da casa, escrita depois de tres portoes cegos no mesmo dia: portao
# que nao conseguiu medir REPROVA e diz isso. Zero tela medida com codigo 0 e
# o jeito mais silencioso de mentir.
cat > "$T/nada.html" <<'H'
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"></head>
<body><div id="app"></div><script>
var x = 1;   /* nem telaCapa, nem montaFase, nem FASES: nada para abrir */
</script></body></html>
H
pega "imagens  · nao mediu nada = reprova"   PEGA node _qa/imagens.js   "$T/nada.html" telaCapa
pega "contraste· nao mediu nada = reprova"   PEGA node _qa/contraste.js "$T/nada.html" telaCapa

echo "-----------------------------------------------------------"
if [ "$falhou" = "0" ]; then
  echo " OS PORTOES PROVAM O QUE DIZEM — cada um reprovou o seu defeito."
else
  echo " ⛔ HA PORTAO CEGO (ou gritando a toa). Conserte ANTES de confiar num codigo 0."
fi
exit "$falhou"
