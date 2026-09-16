/* ============================================================
   ESQUELETO DA FOLHA VIVA — as folhas.

   ⚠️ ESTE ARQUIVO É A CASCA. As folhas (`f01`, `f02`, …) se escrevem abaixo, e
   cada uma nasce de um VERBO impresso numa folha de papel colhida. O crivo —
   comando VERBATIM e veredito de cada uma das trinta — vai em
   `_sequencias/POTE-<assunto>.md`, e é DELE que sai o roteiro.

   ⚠️ A POSIÇÃO É A IDENTIDADE: a folha da posição 7 usa o pote `p7`, grava os
      ids `n7_*` e fala `p7enun`. Não há segunda lista para desencontrar.

   O QUE JÁ VEM PRONTO AQUI (clonar destas peças, não reescrever):
     · `faixa` · `enunciado` · `item` · `fechaItem` · `nomeSecreto`
     · `opcoes` (a fileira de escolhas, com arrastar de brinde)
     · `puxavel` (arrastar com mouse, dedo e caneta — três lições pagas dentro)
     · `gavetas` (classificar em colunas, nas duas portas)
     · `montaLigar` (ligar com linha curva)
     · o teclado (`abreCruz`/`digitaCruz`/`confereCruz`/`rolaParaCruz`)
     · navegação, boletim, relatório do professor, dossiê, retomar 55 min
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI, e o número errado quebra DUAS
   folhas de uma vez — medido no `_rima1`, que estava no ar: a folha que liga
   NUNCA fechava (a criança ligava tudo e continuava faltando) e a folha
   apontada por engano FECHAVA SOZINHA, sem ninguém tocar nela. São as únicas
   cujos ids não nascem de `n<pi>_`, e sim dentro do `montaLigar`
   (`l<pi>g<i>_<chave>`). Conferir com `node _qa/conta_folha.js <pasta>`. */
var LIGAR = [];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
var CORES = ["c1", "c1", "c1", "c1", "c1", "c2", "c2", "c2", "c3", "c3", "c3", "c3", "c3", "c3", "c4", "c4", "c4", "c4", "c4", "c5", "c5", "c5", "c5", "c5", "c1", "c1", "c1", "c2", "c2", "c2", "c2", "c3", "c3", "c3", "c3"];


function faixa(d, i, titulo){ d.appendChild(el("div", "faixa", '<div class="num">' + i + '</div><h2>' + titulo + '</h2>')); }
function aoAbrir(d, fn){ if(!d._aoAbrir) d._aoAbrir = []; d._aoAbrir.push(fn); }
/* ---------- O ALTO-FALANTE ----------
   Regra da casa: tudo o que a criança PRECISA LER tem que poder ser OUVIDO.
   O desenho do botão é CSS puro: nada de emoji (vira quadradinho nos PCs da
   escola). */
function botaoSom(rot, aoTocar){
  var b = el("button", "som");
  b.innerHTML = '<i class="cone"></i><i class="onda o1"></i><i class="onda o2"></i>';
  b.setAttribute("aria-label", rot || "Ouvir");
  b.onclick = function(ev){ ev.stopPropagation(); sPasso(); aoTocar(); };
  return b;
}
function enunciado(d, pi, texto, chave){
  var cx = el("div", "enunlin");
  cx.appendChild(el("div", "enun", texto));
  cx.appendChild(botaoSom("Ouvir o que a folha pede", function(){ falar(chave); }));
  d.appendChild(cx);
}
function item(n){ return el("div", "item", n ? '<span class="n">' + n + '.</span>' : ""); }
function fechaItem(d, box, id){
  if(ST.resp[id]) box.className = "item feito";
  box.setAttribute("data-qa", "item-" + id);
  d.appendChild(box);
}
/* ⚠️ A RESPOSTA NÃO PODE APARECER ANTES DE A CRIANÇA RESPONDER. A palavra não
   some: fica INVISÍVEL (`visibility`, para o espaço ficar guardado e a folha não
   pular) e aparece no instante do acerto. É o que o `_qa/resposta_impressa.py`
   mede. */
function nomeSecreto(txt, id){
  var b = el("b", "segredo" + (ST.resp[id] ? " revelado" : ""), txt);
  b.setAttribute("data-nome", id);
  return b;
}
function chaveQuadro(w){ return String(w).toLowerCase().replace(/[^a-z]/g, ""); }

/* ---------- fileira de opções (a peça que mais se repete) ----------
   `soltarEm` (opcional) liga o ARRASTAR: a criança pode puxar a peça até o
   alvo em vez de só tocar nela. AS DUAS PORTAS, SEMPRE — no PC da escola ela
   usa o mouse e arrastar é o gesto natural; no celular, tocar é. */
function opcoes(pai, pi, id, lista, certa, cls, falaCerto, falaDica, aoAcertar, soltarEm){
  registra(id, pi, certa);
  var box = el("div", "ops"), feito = !!ST.resp[id];
  function responde(o, b){
    if(ST.resp[id]) return;
    sPasso(); if(o.fala) falar(o.fala);
    if(o.v === certa){
      b.className = "op" + (cls ? " " + cls : "") + " certa";
      if(aoAcertar) aoAcertar(b);
      setTimeout(function(){ acertou(id, falaCerto); }, aoAcertar ? 620 : 240);
    } else {
      b.className = "op" + (cls ? " " + cls : "") + " erro";
      setTimeout(function(){ b.className = "op" + (cls ? " " + cls : ""); }, 500);
      errou(id, falaDica);
    }
  }
  lista.forEach(function(o){
    var b = el("button", "op" + (cls ? " " + cls : "") + (feito && o.v === certa ? " certa" : ""), o.rot);
    b.setAttribute("data-qa", "op-" + id + "-" + o.v);
    b.setAttribute("aria-label", o.aria || o.v);
    b.onclick = function(){ if(b._arrastou){ b._arrastou = false; return; } responde(o, b); };
    if(soltarEm) puxavel(b, soltarEm, function(){ responde(o, b); });
    box.appendChild(b);
  });
  pai.appendChild(box);
}

/* ---------- PUXAR uma peça até um alvo (mouse, dedo e caneta) ----------
   ⚠️ Pointer Events e não mouse+touch separados: no celular o navegador dispara
   eventos de mouse FANTASMA depois do toque, e foi assim que o arrastar já
   quebrou duas vezes nesta casa.
   ⚠️ E nada de `preventDefault` no início: isso mataria o toque. Só depois de o
   dedo ANDAR 8 px é que vira arrasto — antes disso continua sendo um toque
   normal e o `onclick` responde igual. */
var PUXA = null;

function puxavel(bt, alvos, aoSoltar){
  if(!alvos.push) alvos = [alvos];
  bt.style.touchAction = "none";
  bt.addEventListener("pointerdown", function(ev){
    if(ev.button && ev.button !== 0) return;
    PUXA = {bt: bt, alvos: alvos, aoSoltar: aoSoltar,
            x0: ev.clientX, y0: ev.clientY,
            lx: ev.clientX, ly: ev.clientY,
            andando: false, fantasma: null};
  });
}
/* ⚠️⚠️ TRÊS LIÇÕES PAGAS AQUI, e nenhuma delas dava erro na tela — o arrasto
   simplesmente não acontecia:
   1. ouvir o `pointermove` no PRÓPRIO botão: só o primeiro movimento chegava.
      O padrão certo é ouvir no DOCUMENTO — o dedo precisa poder SAIR de cima da
      peça, que é justamente o que ele faz ao levá-la.
   2. o navegador FUNDE os movimentos: num teste com oito passos chegou UM
      `pointermove`. Quem manda é a SOLTURA, não a contagem de movimentos.
   3. o `pointercancel` chega ANTES do `pointerup` e vem com clientX/clientY
      = 0,0 — quem usasse a coordenada dele concluiria que a criança soltou no
      canto da tela. Por isso o último ponto REAL fica guardado. */
function _puxaAnda(ev){
  var P = PUXA; if(!P) return;
  P.lx = ev.clientX; P.ly = ev.clientY;
  var dx = ev.clientX - P.x0, dy = ev.clientY - P.y0;
  if(!P.andando){
    if(dx * dx + dy * dy < 64) return;
    P.andando = true; P.bt._arrastou = true;
    var f = P.bt.cloneNode(true);
    f.className = "fantasma " + P.bt.className;
    var r = P.bt.getBoundingClientRect();
    f.style.width = r.width + "px"; f.style.height = r.height + "px";
    f._ox = r.left; f._oy = r.top;
    document.body.appendChild(f); P.fantasma = f;
    P.bt.className = P.bt.className + " puxada";
  }
  if(ev.cancelable) ev.preventDefault();
  P.fantasma.style.left = (P.fantasma._ox + dx) + "px";
  P.fantasma.style.top = (P.fantasma._oy + dy) + "px";
  P.alvos.forEach(function(a){
    a.className = a.className.replace(/ ?perto/, "") + (sobre(ev, a) ? " perto" : "");
  });
}
function _puxaSolta(ev){
  var P = PUXA; if(!P) return;
  PUXA = null;
  P.alvos.forEach(function(a){ a.className = a.className.replace(/ ?perto/, ""); });
  P.bt.className = P.bt.className.replace(/ ?puxada/, "");
  if(P.fantasma && P.fantasma.parentNode) P.fantasma.parentNode.removeChild(P.fantasma);
  var px = ev.clientX, py = ev.clientY;
  if(!px && !py){ px = P.lx; py = P.ly; }
  var onde = {clientX: px, clientY: py};
  var andou = (px - P.x0) * (px - P.x0) + (py - P.y0) * (py - P.y0) >= 64;
  if(!andou) return;
  P.bt._arrastou = true;
  var i;
  for(i = 0; i < P.alvos.length; i++){
    if(sobre(onde, P.alvos[i])){ P.aoSoltar(P.alvos[i], i); break; }
  }
  setTimeout(function(){ P.bt._arrastou = false; }, 60);
}
document.addEventListener("dragstart", function(ev){ ev.preventDefault(); });
document.addEventListener("pointermove", _puxaAnda);
document.addEventListener("pointerup", _puxaSolta);
document.addEventListener("pointercancel", _puxaSolta);
function sobre(ev, alvo){
  var r = alvo.getBoundingClientRect(), m = 14;
  return ev.clientX >= r.left - m && ev.clientX <= r.right + m &&
         ev.clientY >= r.top - m && ev.clientY <= r.bottom + m;
}

function monta(){
  livro.innerHTML = ""; PAGEL = []; RESP = {}; TIRAS = [];
  /* ⚠️ UMA ENTRADA POR FOLHA, na ordem, começando pela capa `f0`. */
  var caps = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14,
             f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27,
             f28, f29, f30, f31, f32, f33, f34, f35], i;
  for(i = 0; i < caps.length; i++){
    var d = el("div", "pagina" + (i > 0 ? " " + CORES[i - 1] : "")); d.setAttribute("data-pag", i);
    caps[i](d, i);
    if(i > 0) d.appendChild(el("div", "carimbo", "FOLHA<br>PRONTA"));
    livro.appendChild(d); PAGEL.push(d);
  }
}

/* ---------- capa ----------
   A capa não é enfeite: é a primeira coisa que a criança vê, e é ela que diz
   "isto aqui é um lugar bom". O tema sai do PROBLEMA do caderno.
   ⚠️ CAPA CLONADA = TROCAR A CENA, SEMPRE. Numa capa herdada desta casa ficou um
      `img()` de outra atividade: o app abria com um quadradinho vazio e um 404
      no console, e nenhum portão de texto viu. */
function f0(d){
  var c = el("div", "capa"), nome = "A Casinha dos Três Pontos", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.04 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 2º ano &middot; 35 folhas sobre pontuação</div>' +
    '<div class="chamada">Escreva o seu nome ali embaixo e toque em <b>Começar</b>.</div>';
  d.appendChild(c);
}
function gavetas(d, pi, gk, pede){
  faixa(d, pi, NOMES[pi - 1]);
  var G = GAV[gk];
  enunciado(d, pi, pede, "p" + pi + "enun");
  var cols = el("div", "colunas"), caixas = {}, listaC = [];
  G.cols.forEach(function(C){
    var c = el("div", "coluna");
    var t = el("div", "ctit", C.n);
    t.setAttribute("data-alvo", "1");
    /* ⚠️ o alvo é COMPARTILHADO pela folha inteira, então ele se declara no
       nível da página — e com o número da folha no nome, porque as 22 folhas
       moram no mesmo HTML e o jogador da banca busca por `document.querySelector`. */
    c.setAttribute("data-qa", "alvo-gav" + pi + "_" + C.k);
    t.appendChild(botaoSom("Ouvir a regra desta gaveta", function(){ falar("gav_" + gk + "_" + C.k); }));
    c.appendChild(t);
    var dentro = el("div", "cdentro");
    c.appendChild(dentro);
    c._v = C.k; c._dentro = dentro;
    caixas[C.k] = c; listaC.push(c);
    cols.appendChild(c);
  });
  d.appendChild(cols);
  var banco = el("div", "figbanco"), marcada = null;
  ST.folha["p" + pi].forEach(function(n, i){
    var P = G.pal[n], id = "n" + pi + "_" + i;
    registra(id, pi, ">gav" + pi + "_" + P.c);
    var b = el("button", "op pal" + (ST.resp[id] ? " usada" : ""), P.p);
    b.setAttribute("aria-label", P.p);
    b.setAttribute("data-qa", "item-" + id);
    /* a palavra escrita é a PEÇA que a criança pega, não a resposta entregue */
    b.setAttribute("data-alvo", "1");
    if(ST.resp[id]) caixas[P.c]._dentro.appendChild(el("span", "fdentro", P.p));
    function larga(col){
      if(ST.resp[id]) return;
      if(col._v === P.c){
        b.className = "op pal usada";
        col._dentro.appendChild(el("span", "fdentro", P.p));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + n);
      } else {
        col.className = "coluna erro";
        setTimeout(function(){ col.className = "coluna"; }, 500);
        errou(id, "dica" + pi + "_" + n);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("diz2_" + gk + "_" + n);
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
    };
    puxavel(b, listaC, function(col){ larga(col); });
    banco.appendChild(b);
  });
  listaC.forEach(function(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_palavra"); return; }
      marcada._larga(col);
    };
  });
  d.appendChild(banco);
}

/* ============================================================
   AS FOLHAS — escrever daqui para baixo, uma função por folha.

   O MOLDE de uma folha de escolher:

     function f01(d, pi){
       faixa(d, pi, NOMES[pi - 1]);
       enunciado(d, pi, "O que a criança tem de fazer.", "p" + pi + "enun");
       ST.folha["p" + pi].forEach(function(k, i){
         var D = MEUDADO[k], id = "n" + pi + "_" + i, box = item(i + 1);
         // … desenhar a peça …
         opcoes(box, pi, id, lista, certa, "pal",
                "certo" + pi + "_" + k, "dica" + pi + "_" + k);
         fechaItem(d, box, id);
       });
     }

   ⚠️ E CADA PEÇA TEM DE SER ALCANÇÁVEL PELO JOGADOR DA BANCA, senão a folha sai
      como dívida e ninguém a mede. Os contratos, em `_qa/joga_folha.js`:
        `esc-<id>`            → campo de teclado
        `op-<id>-<valor>`     → uma escolha
        `item-<id>` + `>gav`  → pegar a peça e largar na gaveta
        `pinta-<id>-<x>` + `data-lapis="<x>"` e o estojo `lapis-<x>` → pintar
        `cp-<id>-a` / `cp-<id>-z` → as duas pontas da palavra no caça-palavras
        `conferir-<id>`       → marque vários e confirme
   ============================================================ */
/* ---------- o teclado da palavra: uma por vez, letra a letra ----------
   ⚠️ UMA PEÇA SÓ PARA A CRUZADINHA (22) E PARA O REESCREVA (19). As duas
   escrevem palavra letra a letra; escrever dois teclados seria arrumar lugar
   para um segundo defeito. O que muda entre elas é só o rótulo da tarja —
   daí o `E.rot`. */
var CRUZ = null;
/* ---------- ROLAR A PALAVRA PARA CIMA DO TECLADO ----------
   ⚠️⚠️ O TECLADO TAPAVA A ATIVIDADE, e o Marcos viu no celular (15/set/2026):
      *"ele preenche a tela e não dá para ver a atividade"*. Medido: na
      cruzadinha de 360x640 o teclado ocupava 368 px de 640 e a grade ficava
      INTEIRA por baixo dele — a criança escrevia às cegas.
   ⚠️ E A REGRA TEM DOIS DEGRAUS, porque medir só um não bastou:
      1. se a PALAVRA inteira cabe na faixa que sobra, ela sobe inteira;
      2. se não cabe (palavra em pé, tela de 320x568 — medido), sobe a CASINHA
         QUE ESTÁ SENDO ESCRITA, centrada na faixa. É o que um campo de texto
         faz: mantém à vista a letra que a pessoa está digitando.
   Por isso ela é chamada duas vezes: ao abrir o teclado e a cada letra.
   ⚠️⚠️ E ELA ATENDE OS DOIS TECLADOS DA CASA, o que é a lição paga aqui
      (15/set/2026): há dois desenhos de teclado nos cadernos de folha viva —
      o da CRUZADINHA, que escreve numa fila de casinhas (`CRUZ.E.cels`), e o
      da SÍLABA/PALAVRA, que escreve numa quadra só (`ATIVA.q`). Eu escrevi
      esta função ancorada no primeiro e a enfiei nos dezoito cadernos pelo
      `function abreCruz(` — que só existe em TRÊS. Nos outros quinze ficou a
      CHAMADA sem a função: `setTimeout(rolaParaCruz, 60)` estourava
      ReferenceError e matava o resto de `ativa()`, que era justamente quem
      escrevia a dica e falava com a criança. O teclado abria mudo.
      O `node --check` não vê isso (a sintaxe está perfeita); quem vê é o
      `_qa/funcoes.py`, o portão "função que não existe" — que eu não rodei. */
function rolaParaCruz(){
  /* ⚠️ VAZIA DE PROPÓSITO, e ela fica aqui em vez de sumir. Enquanto o
     teclado era uma barra fixa nossa, esta função levava a palavra para
     a faixa que sobrava acima dele. Agora quem abre é o teclado do
     aparelho, e o navegador já rola a página sozinho para o campo com
     foco. Apagá-la quebraria as chamadas que ainda existem por aí. */
}
function abreCruz(E, pi){
  /* ⚠️ SEM BARRA FIXA, SEM ROLAGEM FORÇADA. O teclado da casa era fixo no pé da
     tela e tapava a palavra que a criança escrevia — daí existir o `comtec` e o
     `rolaParaCruz`. Agora quem abre é o teclado do APARELHO, que o próprio
     navegador já trata: ele rola a página para deixar o campo com foco à vista.
     Foi por isso que as duas peças saíram daqui juntas. */
  if(CRUZ) fechaCruz();
  CRUZ = {E: E, val: "", pi: pi};
  if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista ativa";
  pintaCruz();
  var grade = E.cels && E.cels[0] ? E.cels[0].parentNode : null;
  var c = poeCampoSobre(grade);
  c.value = "";
  c.setAttribute("maxlength", String(E.aceita ? E.cels.length : E.w.length));
  c.setAttribute("aria-label", E.rot || "Escreva a palavra");
  try{ c.focus({preventScroll: false}); }catch(e){ c.focus(); }
  falar("escreva");
}
function fechaCruz(){
  if(!CRUZ) return;
  var E = CRUZ.E;
  if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista";
  CRUZ = null;
  if(TECIN){ TECIN.value = ""; try{ TECIN.blur(); }catch(e){} }
  pintaCruz();
}
function pintaCruz(){
  var E = CRUZ.E, v = CRUZ.val;
  E.cels.forEach(function(c, i){
    if(!c) return;
    var n = c.querySelector(".cn");
    c.textContent = v.charAt(i) || "";
    if(n) c.appendChild(n);
    c.className = "ccel viva" + (i === v.length ? " ativa" : "");
  });
}
function digitaCruz(ch){
  if(!CRUZ) return;
  sTecla();
  var E = CRUZ.E;
  /* ⚠️ NA FOLHA DE PRODUÇÃO O TAMANHO NÃO É O DO GABARITO: as palavras aceitas
     têm tamanhos diferentes, e o teto é a maior delas (`E.cels.length`). E ela
     NÃO se confere sozinha ao encher — a criança é que diz quando acabou, no
     botão OK. Conferir sozinho recusaria "GATO" no meio de "GATOS". */
  var teto = E.aceita ? E.cels.length : E.w.length;
  if(ch === "ap") CRUZ.val = CRUZ.val.slice(0, -1);
  else if(ch === "ok"){ confereCruz(); return; }
  else { if(CRUZ.val.length >= teto) return; CRUZ.val += ch; }
  pintaCruz(); rolaParaCruz();
  if(!E.aceita && CRUZ.val.length >= E.w.length) setTimeout(confereCruz, 380);
}
/* ⚠️⚠️ O ACENTO NÃO PODE REPROVAR QUEM ACERTOU A PALAVRA (ordem do Marcos,
   15/set/2026, com a turma na sala: *"faça que tanto com o sem dê certo"*).
   O gabarito de BACTERIAS estava sem acento e o teclado da tela TEM os acentos:
   a criança que escrevia BACTÉRIAS — que é o certo em português — era recusada,
   e ficava olhando para uma palavra certa marcada como errada. O contrário
   também acontecia, em caderno cujo gabarito vinha acentuado.
   ⚠️ E ONDE O ACENTO É O CONTEÚDO, ele continua contando: a folha declara
      `exigeAcento` e aí a comparação é letra por letra, acento incluído. */
function semAcento(s){
  s = String(s || "").toUpperCase();
  var de = "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ", para = "AAAAAEEEEIIIIOOOOOUUUUC", i, o = "";
  for(i = 0; i < s.length; i++){
    var n = de.indexOf(s.charAt(i));
    o += n > -1 ? para.charAt(n) : s.charAt(i);
  }
  return o;
}
function mesmaPalavra(a, b, exigeAcento){
  if(exigeAcento) return String(a).toUpperCase() === String(b).toUpperCase();
  return semAcento(a) === semAcento(b);
}
function confereCruz(){
  if(!CRUZ || !CRUZ.val) return;
  var E = CRUZ.E, pi = CRUZ.pi;
  /* ⚠️⚠️ A FOLHA DE PRODUÇÃO (34) ACEITA MUITAS RESPOSTAS, e sem isto ela seria
     uma armadilha: a criança escreveria uma palavra CERTA e o app diria que
     está errada. Quando `E.aceita` existe, vale qualquer palavra da lista —
     e a que fica escrita nas casas é a que ELA escreveu, não a do gabarito.
     ⚠️ E o gabarito continua existindo (`E.w` = a primeira da lista), porque é
        ele que o jogador da banca digita. */
  var vale = E.aceita
    ? E.aceita.some(function(w){ return mesmaPalavra(CRUZ.val, w, E.exigeAcento); })
    : mesmaPalavra(CRUZ.val, E.w, E.exigeAcento);
  var escrita = E.aceita ? CRUZ.val : E.w;
  if(vale){
    E.cels.forEach(function(c, i){
      if(!c) return;
      var n = c.querySelector(".cn");
      c.textContent = escrita.charAt(i); if(n) c.appendChild(n);
      c.className = "ccel viva" + (i < escrita.length ? " ok" : "");
    });
    if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista feita";
    CRUZ = null;
    if(TECIN){ TECIN.value = ""; try{ TECIN.blur(); }catch(e){} }
    acertou(E.id, "certo" + pi + "_" + E.k);
  } else {
    CRUZ.val = ""; pintaCruz();
    errou(E.id, "dica" + pi + "_" + E.k);
  }
}
function montaLigar(caixa, pi, tag, pares, pagina){
  var box = el("div", "ligar"), ce = el("div", "col"), cd = el("div", "col");
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("class", "linhas");
  box.appendChild(ce); box.appendChild(cd); box.appendChild(svg); caixa.appendChild(box);
  var ordem = baralha(pares.map(function(_, i){ return i; }));
  var E = {}, D = {}, marcada = null;
  pares.forEach(function(P){ registra("l" + pi + tag + "_" + P.k, pi, P.k); });
  function centro(e, lado){
    var r = e.getBoundingClientRect(), b = box.getBoundingClientRect();
    return {x: (lado === "e" ? r.right : r.left) - b.left, y: r.top + r.height / 2 - b.top};
  }
  function linha(a, b2, cor){
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    var dx = Math.max(28, Math.abs(b2.x - a.x) * 0.45);
    var dd = "M" + a.x + "," + a.y + " C" + (a.x + dx) + "," + a.y + " " +
             (b2.x - dx) + "," + b2.y + " " + b2.x + "," + b2.y;
    var halo = document.createElementNS("http://www.w3.org/2000/svg", "path");
    halo.setAttribute("d", dd); halo.setAttribute("fill", "none");
    halo.setAttribute("stroke", "#ffffff"); halo.setAttribute("stroke-width", 11);
    halo.setAttribute("stroke-linecap", "round");
    var l = document.createElementNS("http://www.w3.org/2000/svg", "path");
    l.setAttribute("d", dd); l.setAttribute("fill", "none");
    l.setAttribute("stroke", cor); l.setAttribute("stroke-width", 6);
    l.setAttribute("stroke-linecap", "round");
    g.appendChild(halo); g.appendChild(l);
    [a, b2].forEach(function(p){
      var c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      c.setAttribute("cx", p.x); c.setAttribute("cy", p.y); c.setAttribute("r", 6);
      c.setAttribute("fill", cor); c.setAttribute("stroke", "#fff"); c.setAttribute("stroke-width", 2.5);
      g.appendChild(c);
    });
    svg.appendChild(g); return g;
  }
  function desmarca(){ if(marcada) marcada.el.className = marcada.el.className.replace(" marcada", ""); marcada = null; }
  function redesenha(){
    while(svg.firstChild) svg.removeChild(svg.firstChild);
    for(var k in E) if(ST.lig["l" + pi + tag + "_" + k]) linha(centro(E[k].el, "e"), centro(D[k].el, "d"), "#15a34a");
  }
  aoAbrir(pagina, redesenha);
  window.addEventListener("resize", function(){ if(pagina.className.indexOf("viva") > -1) redesenha(); });
  function fecha(Re, Rd){
    var id = "l" + pi + tag + "_" + Re.k;
    if(Rd.k === Re.k){
      ST.lig[id] = 1; tentativa(id, true); ST.resp[id] = 1; salvar();
      Re.el.className += " feita"; Rd.el.className += " feita"; desmarca(); redesenha(); sCerto();
      falar(Re.fc); setTimeout(function(){ confereFolha(pi); }, 850);
    } else {
      tentativa(id, false); sErro();
      Rd.el.className += " treme";
      setTimeout(function(){ Rd.el.className = Rd.el.className.replace(" treme", ""); }, 500);
      falar(ST.tent[id].erros >= 2 ? Re.dica : "quase");
      if(ST.tent[id].erros >= 2 && D[Re.k].el.className.indexOf("feita") < 0) D[Re.k].el.className += " mostra";
    }
  }
  pares.forEach(function(P){
    var e = el("div", "ponta" + (ST.lig["l" + pi + tag + "_" + P.k] ? " feita" : ""), P.esq);
    e.setAttribute("role", "button"); e.setAttribute("tabindex", "0");
    e.setAttribute("data-qa", "lig" + tag + "-e-" + P.k);
    e.setAttribute("aria-label", P.ariaE);
    var R = {k: P.k, el: e, fc: P.fc, dica: P.dica};
    E[P.k] = R;
    e.addEventListener("pointerdown", function(ev){
      if(e.className.indexOf("feita") > -1) return;
      ev.preventDefault(); desmarca(); marcada = R; e.className += " marcada"; sPasso(); falar(P.fe);
    });
    e.onkeydown = function(ev){ if(ev.key === "Enter" || ev.key === " "){ ev.preventDefault(); desmarca(); marcada = R; e.className += " marcada"; falar(P.fe); } };
    ce.appendChild(e);
  });
  ordem.forEach(function(j){
    var P = pares[j];
    var e = el("div", "ponta" + (ST.lig["l" + pi + tag + "_" + P.k] ? " feita" : ""), P.dir);
    e.setAttribute("role", "button"); e.setAttribute("tabindex", "0");
    e.setAttribute("data-qa", "lig" + tag + "-d-" + P.k);
    e.setAttribute("aria-label", P.ariaD);
    var R = {k: P.k, el: e}; D[P.k] = R;
    e.addEventListener("pointerdown", function(ev){
      if(e.className.indexOf("feita") > -1) return;
      ev.preventDefault();
      if(marcada) fecha(marcada, R); else { sPasso(); falar(P.fd); falarDepois("ligue", 900); }
    });
    e.onkeydown = function(ev){ if((ev.key === "Enter" || ev.key === " ") && marcada){ ev.preventDefault(); fecha(marcada, R); } };
    cd.appendChild(e);
  });
}

/* ---------- o teclado da tela, e o teclado DE VERDADE ----------
   ⚠️⚠️ O ALFABETO ESTAVA INCOMPLETO, E ISSO TRANCAVA A CRIANÇA (15/set/2026).
   Faltavam K, W e Y — e, pior, faltavam Ê, Â, Ã, Ô, Õ, À e Ü. Quem tentasse
   escrever PÊSSEGO no teclado da tela ou no teclado de verdade ficava com
   "PSSEGO": a tecla não existia, a letra não entrava, e a folha NUNCA FECHAVA.
   Não havia erro nenhum no console; a criança só tentava de novo até desistir.
   Medido com o navegador de verdade, letra por letra, antes deste conserto.
   ⚠️ Quem fecha esta família agora é o portão `_qa/teclado.py`: ele confere que
      o alfabeto tem as 26 letras e os treze acentos do português, e que o
      teclado da tela e o filtro do teclado de verdade usam o MESMO alfabeto —
      porque dois alfabetos diferentes é o mesmo defeito com uma porta só.
   ⚠️ REGRA DAS DUAS PORTAS (Marcos, ago/2026): *"seria interessante se o aluno
   além de teclar no teclado virtual funcionasse se ele tocasse no teclado de
   verdade, as duas opções"*. No PC da escola tem teclado e a criança vai
   digitar; no celular, não tem. Nunca só uma porta. */
/* ============================================================
   O TECLADO DO APARELHO — substitui o teclado de 41 teclas da casa.

   ⭐ ORDEM DO MARCOS (15/set/2026): *"pode remover o teclado das atividades,
      melhor digitar com teclado normal"*. O nosso ocupava 53% de um celular de
      640 px, e mesmo redistribuído para 4 fileiras ainda comia 40%.

   ⚠️ O QUE ELE RESOLVE E O QUE NÃO RESOLVE, dito por inteiro: no PC da escola o
      teclado físico já funcionava (as duas portas são regra da casa desde
      ago/2026) — o campo abaixo não muda nada lá. Ele existe pelo CELULAR, que
      não tem teclado físico: sem um campo de verdade para focar, o aparelho não
      abre teclado nenhum e a criança fica trancada.
   ============================================================ */
var TECIN = null;
function campoTeclado(){
  if(TECIN) return TECIN;
  TECIN = document.createElement("input");
  TECIN.id = "tecIn";
  TECIN.type = "text";
  TECIN.setAttribute("autocomplete", "off");
  TECIN.setAttribute("autocorrect", "off");
  TECIN.setAttribute("autocapitalize", "characters");
  TECIN.setAttribute("spellcheck", "false");
  TECIN.setAttribute("aria-label", "Escreva a palavra");
  TECIN.setAttribute("inputmode", "text");
  /* ⚠️ O EVENTO É `input`, NÃO `keydown`: no celular o teclado do sistema não
     dispara keydown com a letra (ele "compõe" o texto), e um caderno que só
     ouvisse keydown seria mudo justamente no aparelho para o qual este campo
     existe. */
  TECIN.addEventListener("input", function(){
    if(!CRUZ) return;
    var v = (TECIN.value || "").toUpperCase();
    var teto = CRUZ.E.aceita ? CRUZ.E.cels.length : CRUZ.E.w.length;
    if(v.length > teto) v = v.slice(0, teto);
    CRUZ.val = v; TECIN.value = v;
    pintaCruz();
    if(!CRUZ.E.aceita && CRUZ.val.length >= CRUZ.E.w.length) setTimeout(confereCruz, 380);
  });
  TECIN.addEventListener("keydown", function(ev){
    if(ev.key === "Enter"){ ev.preventDefault(); confereCruz(); }
    else if(ev.key === "Escape"){ fechaCruz(); }
  });
  TECIN.addEventListener("blur", function(){
    /* sair do campo não perde o que já foi escrito — só fecha a caneta */
    setTimeout(function(){ if(CRUZ && document.activeElement !== TECIN) fechaCruz(); }, 120);
  });
  document.body.appendChild(TECIN);
  return TECIN;
}
function poeCampoSobre(grade){
  var c = campoTeclado();
  if(grade && grade.parentNode){
    if(c.parentNode !== grade) grade.appendChild(c);
    c.style.left = "0"; c.style.top = "0";
    c.style.width = "100%"; c.style.height = "100%";
  }
  return c;
}
document.addEventListener("keydown", function(ev){
  if(!CRUZ) return;
  if(document.activeElement && document.activeElement.id === "nomeIn") return;
  var k = (ev.key || "").toUpperCase();
  if(k.length === 1 && "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ".indexOf(k) > -1){ ev.preventDefault(); digitaCruz(k); }
  else if(ev.key === "Backspace"){ ev.preventDefault(); digitaCruz("ap"); }
  else if(ev.key === "Enter"){ ev.preventDefault(); digitaCruz("ok"); }
  else if(ev.key === "Escape"){ fechaCruz(); }
});

/* ---------- folha pronta e navegação ---------- */
function idsDaPagina(pi){
  /* ⚠️⚠️ ISTO JÁ MENTIU DUAS VEZES NESTA CASA. Antes, cada folha gravava `n6_0`
     à mão e esta função dizia à mão que a página 6 tinha ids `n6_`. Eram DOIS
     lugares a combinar, os dois sintaticamente corretos, e quando a ordem das
     folhas mudava o relatório saía ZERO com a folha toda respondida — sem erro
     nenhum no console. Agora o id NASCE DA POSIÇÃO e aqui se lê a mesma
     posição; a única forma diferente é o LIGAR, que se declara na constante. */
  var ids = [], i, k, L = (ST.folha["p" + pi] || []);
  if(LIGAR.indexOf(pi) > -1){
    for(i = 0; i < L.length; i++)
      for(k = 0; k < L[i].length; k++) ids.push("l" + pi + "g" + i + "_" + L[i][k]);
    return ids;
  }
  for(i = 0; i < L.length; i++) ids.push("n" + pi + "_" + i);
  return ids;
}
function pendentes(pi){
  var ids = idsDaPagina(pi), n = 0, i;
  for(i = 0; i < ids.length; i++) if(!ST.resp[ids[i]]) n++;
  return n;
}
function confereFolha(pi){
  if(pendentes(pi) > 0 || ST.prontas[pi]) return;
  ST.prontas[pi] = 1; salvar();
  PAGEL[pi].className += " pronta"; sFesta(); confete(24);
  if(pi < PAGEL.length - 1){ falar("folhaPronta"); setTimeout(function(){ if(ST.pag === pi) vaiPara(pi + 1); }, 2400); }
  else setTimeout(fim, 1400);
  atualizaNav();
}
function espelhaNome(t){
  var i = document.getElementById("nomeIn"); if(i && i.value !== t) i.value = t;
}
function vaiPara(pi){
  calar(); fechaCruz();
  document.getElementById("barraCapa").className = pi === 0 ? "aberta" : "";
  if(pi === 0) espelhaNome(ST.nome || "");
  document.getElementById("fim").style.display = "none";
  document.getElementById("retomar").style.display = "none";
  document.getElementById("nav").style.display = pi === 0 ? "none" : "flex";
  for(var i = 0; i < PAGEL.length; i++) PAGEL[i].className = PAGEL[i].className.replace(" viva", "");
  ST.pag = pi; salvar();
  /* ⚠️ GUARDA DO ESQUELETO VAZIO: enquanto o caderno ainda não tem folha
     nenhuma, o "Começar" pede a folha 1 e `PAGEL[1]` não existe — estourava
     `TypeError` e o portão do boot reprovava. Não é defeito do caderno em
     construção; é o esqueleto tendo de abrir limpo ANTES de ter conteúdo, que é
     justamente o que torna o pré-voo útil no primeiro minuto. Num caderno com
     folhas esta guarda nunca dispara. */
  var d = PAGEL[pi];
  if(!d){ atualizaNav(); return; }
  d.className += " viva";
  if(pi > 0) window.scrollTo(0, 0);
  if(d._aoAbrir) for(var z = 0; z < d._aoAbrir.length; z++) (function(fn){ setTimeout(fn, 60); })(d._aoAbrir[z]);
  atualizaNav();
  falarDepois(pi === 0 ? "capa" : "p" + pi + "enun", 280);
}
function atualizaNav(){
  var pi = ST.pag, total = PAGEL.length;
  document.getElementById("pg").textContent = pi === 0 ? "Capa" : "Folha " + pi + " de " + (total - 1);
  var feitas = 0, k; for(k in ST.prontas) feitas++;
  document.getElementById("progI").style.width = (feitas / (total - 1) * 100) + "%";
  document.getElementById("bAnt").disabled = pi === 0;
  var prox = document.getElementById("bProx");
  prox.style.visibility = pi === 0 ? "hidden" : "visible";
  var pend = pi > 0 ? pendentes(pi) : 0;
  prox.innerHTML = pi === total - 1 ? (pend ? "Faltam " + pend : "Ver o resultado")
    : (pend ? "Faltam " + pend + '<i class="seta dir"></i>' : 'Próxima<i class="seta dir"></i>');
  prox.className = pend ? "bt cinza" : "bt verde";
  document.getElementById("navTxt").textContent = pi === 0 ? "" : NOMES[pi - 1];
}

/* ---------- fim: boletim, medalha e relatório ---------- */
/* ⭐⭐ O FECHO A QUALQUER MOMENTO.
   O Marcos fixou a sequência em no mínimo 20 folhas (o piso era 25 e ele o
   baixou em 14/set/2026, por velocidade de produção). Este caderno tem 22, e o
   número saiu do inventário de verbos do `POTE`, não de uma meta. Só que a
   criança DEVAGAR leva bem mais nas mesmas 22 folhas — ela não termina. Se o boletim, o parecer e a
   medalha só existissem DEPOIS da última folha, quem mais precisa do elogio
   seria a única a nunca vê-lo.
   ⚠️ E o boletim conta só o que ela TENTOU. Folha que ela não chegou a abrir
      aparece como "ainda não" — jamais como 0 de 6. */
function fim(){
  /* ⭐⭐ AVISA O CONTROLE DA SALA QUE ESTA CRIANÇA TERMINOU.
     Pedido do Marcos (15/set/2026): *"preciso que essas atividades sequências
     didáticas me avisem quando termino no painel de atividades, aquele que tem
     o controle da sala, assim como as atividades que fazíamos antes"*.

     ⚠️ E ELAS NÃO AVISAVAM POR CAMINHO NENHUM — conferido no código do
     laboratório antes de escrever isto. A tela do aluno (`_lab/index.html`)
     reconhece o fim de DOIS jeitos, e a folha viva escapava dos dois:
       1. A ESPIADA — ela olha dentro do quadro e procura a MEDALHA do fim pela
          CLASSE `.medal`. A folha viva chama a dela de `#medalha`, por id, e
          portanto a espiada nunca a via;
       2. O AVISO — o motor manda `postMessage({eduverse:"terminou"})` ao chegar
          no fim. A folha viva não mandava nada, porque nasceu sem essa peça.
     Agora ela manda o aviso aqui, e a medalha ganhou também a classe `medal`
     no HTML: dois caminhos, um cobrindo o buraco do outro, que é a razão pela
     qual o laboratório tem os dois.

     ⚠️ FORA DO LABORATÓRIO NÃO HÁ PAI NENHUM ESCUTANDO e a linha não faz nada —
     por isso ela é segura em qualquer lugar (em casa, no celular, aberta
     direto pelo link). O `try` existe para o caso de a janela de cima ser de
     outro domínio, quando o navegador recusa a leitura de `window.parent`. */
  try{ if(window.parent && window.parent !== window)
         window.parent.postMessage({eduverse: "terminou"}, "*"); }catch(e){}
  calar();
  var abertas = 0, naoAbertas = [], pp;
  for(pp = 1; pp <= NOMES.length; pp++){
    var idp = idsDaPagina(pp), algum = false, z;
    for(z = 0; z < idp.length; z++) if(ST.tent[idp[z]]) { algum = true; break; }
    if(algum) abertas++; else naoAbertas.push(pp);
  }
  var completo = naoAbertas.length === 0;
  var tf = document.getElementById("fimTit");
  if(tf) tf.textContent = completo ? "Caderno completo!" : "O seu boletim de hoje";
  var bv = document.getElementById("bVoltar");
  if(bv) bv.style.display = completo ? "none" : "";
  for(var i = 0; i < PAGEL.length; i++) PAGEL[i].className = PAGEL[i].className.replace(" viva", "");
  document.getElementById("nav").style.display = "none";
  var f = document.getElementById("fim"); f.style.display = "block";
  var tot = 0, prim = 0, pi;
  for(pi = 1; pi <= NOMES.length; pi++){
    var ids = idsDaPagina(pi);
    for(var j = 0; j < ids.length; j++){
      var t = ST.tent[ids[j]];
      if(!t) continue;
      tot++;
      if(t.erros === 0 && t.ok) prim++;
    }
  }
  var pc = tot ? prim / tot : 0;
  var cheias = pc >= .85 ? 3 : pc >= .6 ? 2 : 1, est = "", ke;
  for(ke = 0; ke < 3; ke++)
    est += '<img src="img/cs_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
  document.getElementById("estrelas").innerHTML = est;
  document.getElementById("estrelas").setAttribute("aria-label", cheias + " de 3 estrelas");
  var bar = document.getElementById("barras"); bar.innerHTML = "";
  for(pi = 1; pi <= NOMES.length; pi++){
    (function(pi){
      var ids = idsDaPagina(pi), p = 0, nt = 0, j;
      for(j = 0; j < ids.length; j++){
        var tt = ST.tent[ids[j]];
        if(tt) nt++;
        if(tt && tt.erros === 0 && tt.ok) p++;
      }
      if(nt === 0){
        bar.appendChild(el("div", "barra naoabriu",
          "<span>" + NOMES[pi - 1] + "</span><div class='tr'></div><b>ainda não</b>"));
        return;
      }
      var b = el("div", "barra", "<span>" + NOMES[pi - 1] + "</span><div class='tr'><i></i></div><b>" + p + "/" + nt + "</b>");
      bar.appendChild(b);
      setTimeout(function(){ b.querySelector("i").style.width = (nt ? p / nt * 100 : 0) + "%"; }, 400);
    })(pi);
  }
  /* ⭐ O PARECER DA CRIANÇA. O currículo de Blumenau diz que a avaliação orienta
     *"o professor E O ESTUDANTE acerca de quais objetivos foram alcançados"*, e
     que *"mostrar o que sabe ou o que não sabe é pertinente, faz parte do
     crescimento e não da exclusão"*. Então ela vê o que já sabe — na linguagem
     dela, sem número, sem a palavra "errou" e sem porcentagem.
     ⚠️ A ORDEM IMPORTA: primeiro o que ela JÁ SABE; o "vale treinar" vem depois
     e no máximo dois, senão a lista vira boletim de defeitos. */
  var jaSabe = [], treinar = [], q;
  for(q = 0; q < OBJETIVOS.length; q++){
    var Oq = OBJETIVOS[q], mq = mede(Oq.f);
    if(mq.tot === 0 || !mq.tent) continue;
    var pcq = Math.round(100 * mq.prim / mq.tent);
    (pcq >= 75 ? jaSabe : treinar).push(pcq >= 75 ? Oq.ok : Oq.n.toLowerCase());
  }
  var txt = "";
  if(jaSabe.length) txt = "Você já " + jaSabe.slice(0, 3).join("; ") + ".";
  else txt = "Você começou a reparar que o mesmo som pode se escrever de cinco jeitos — e isso é o principal!";
  if(treinar.length) txt += " Vale treinar mais: " + treinar.slice(0, 2).join(" e ") + ".";
  if(!completo)
    txt = "você fez " + abertas + " de " + NOMES.length + " folhas hoje — e olhe o "
        + "que já dá para ver: " + txt.charAt(0).toLowerCase() + txt.slice(1);
  /* ⚠️ SEM NOME, SEM PREFIXO. Com o prefixo fixo saía "Você, você já…" para a
     criança que não escreve o nome na capa — que é justamente a que mais precisa
     que a tela fale direito com ela. */
  var quem = (ST.nome || "").replace(/^\s+|\s+$/g, "");
  document.getElementById("resumo").innerHTML = quem
    ? "<b>" + esch(quem) + "</b>, " + txt.charAt(0).toLowerCase() + txt.slice(1)
    : txt.charAt(0).toUpperCase() + txt.slice(1);
  sFesta(); confete(40); falar("fim");
}
(function(){
  var m = document.getElementById("medalha"), t = null;
  function segura(){ t = setTimeout(function(){ abreRelatorio(); }, 2000); }
  function larga(){ if(t){ clearTimeout(t); t = null; } }
  m.addEventListener("pointerdown", segura);
  m.addEventListener("pointerup", larga);
  m.addEventListener("pointerleave", larga);
  m.addEventListener("pointercancel", larga);
})();

/* ============================================================
   O QUE A ATIVIDADE MEDE — e como isso vira PARECER e NOTA

   ⚠️ A NOTA FICA COM O PROFESSOR. A Instrução Normativa SEMED nº 1/2017, art.
   3º, citada no currículo de Blumenau, manda avaliar *"com preponderância dos
   aspectos qualitativos sobre os quantitativos"*. O parecer vai para a criança;
   o número fica só aqui.
   ⚠️ E NÃO SE CONTA TUDO IGUAL: acerto de primeira vale 1,0 e acerto com ajuda
   vale 0,6 — o relatório mostra os dois lado a lado, para o professor ver a
   nota E o esforço que ela custou. O critério sai impresso por exigência da
   mesma Instrução (*"a exposição de critérios utilizados"*).
   ============================================================ */
var PESO_PRIMEIRA = 1.0, PESO_COM_AJUDA = 0.6;

/* ⚠️ ESTA LISTA E O `curriculo.json` SÃO A MESMA COISA, ditas para dois
   leitores: aqui em palavras que o professor lê no relatório, lá no vocabulário
   do currículo da rede. O portão `_qa/pedagogo_curriculo.py` reprova se os nomes
   e as folhas não baterem um a um. Os números são POSIÇÕES de folha: mudou a
   ordem, mudam aqui e no `curriculo.json`, no mesmo commit. *//* ⚠️ ESTA LISTA E O `curriculo.json` SÃO A MESMA COISA, ditas para dois
   leitores: aqui em palavras que o professor lê no relatório, lá no vocabulário
   do currículo da rede. O portão `_qa/pedagogo_curriculo.py` reprova se os
   nomes e as folhas não baterem um a um, e também se alguma folha de trabalho
   ficar sem objetivo que a meça. Os números são POSIÇÕES de folha.
   Ex.: {n: "Distinguir X de Y", f: [1, 2, 3],
         ok:  "faz o que o objetivo pede, em palavras do professor",
         nao: "o que ainda não faz — sem a palavra 'errou'"}  */
var OBJETIVOS = [
  /* ⚠️ ESTA LISTA E O `curriculo.json` SÃO A MESMA COISA, e o portão 0b9 reprova
     se divergirem — nome por nome e folha por folha. */
  {n: "Reconhecer os três sinais de pontuação pelo nome", f: [1]},
  {n: "Escolher o ponto final ou o de pergunta ao fim da frase", f: [2, 5]},
  {n: "Escolher entre a pergunta e o susto", f: [3, 4]},
  {n: "Ouvir a entonação e dizer qual sinal a frase pede", f: [6, 7, 8]},
  {n: "Guardar cada frase na casinha do sinal dela", f: [9, 10, 11]},
  {n: "Arrastar o sinal certo para o fim da frase", f: [12, 13, 14]},
  {n: "Reconhecer as palavras que abrem uma pergunta", f: [15, 16]},
  {n: "Responder uma pergunta com uma frase de ponto final", f: [17, 18, 19]},
  {n: "Ordenar as palavras para formar a frase e fechá-la", f: [20, 21]},
  {n: "Escrever a letra maiúscula que abre a frase e o ponto que a fecha", f: [22, 23]},
  {n: "Escrever a palavra que abre a pergunta", f: [24, 32]},
  {n: "Achar frases pelo sinal dentro de um texto", f: [25, 26, 27]},
  {n: "Reconhecer a frase pontuada certa e consertar a errada", f: [28, 29]},
  {n: "Pontuar um texto inteiro do começo ao fim", f: [30, 31]},
  {n: "Escolher o sinal que a cena pede", f: [33, 34, 35]}
];

function mede(folhas){
  var prim = 0, ajuda = 0, tot = 0, tentados = 0, k, j;
  for(k = 0; k < folhas.length; k++){
    var ids = idsDaPagina(folhas[k]);
    tot += ids.length;
    for(j = 0; j < ids.length; j++){
      var t = ST.tent[ids[j]];
      if(t) tentados++;
      if(!t || !t.ok) continue;
      if(t.erros === 0) prim++; else ajuda++;
    }
  }
  return {prim: prim, ajuda: ajuda, tot: tot, tent: tentados,
          pontos: prim * PESO_PRIMEIRA + ajuda * PESO_COM_AJUDA,
          pc: tot ? Math.round(100 * prim / tot) : 0};
}

function abreRelatorio(){
  var r = document.getElementById("relatorio");
  var linhas = "", domina = [], retomar = [], k;
  var pontos = 0, total = 0, primG = 0, ajudaG = 0, tentG = 0;
  var naoAlcancou = [];
  var folhasFeitas = 0, fz;
  for(fz = 1; fz <= NOMES.length; fz++){
    var idf = idsDaPagina(fz), tocou = false, y;
    for(y = 0; y < idf.length; y++) if(ST.tent[idf[y]]) { tocou = true; break; }
    if(tocou) folhasFeitas++;
  }
  var inteiro = folhasFeitas >= NOMES.length;

  for(k = 0; k < OBJETIVOS.length; k++){
    var O = OBJETIVOS[k], m = mede(O.f);
    pontos += m.pontos; total += m.tot; primG += m.prim; ajudaG += m.ajuda;
    tentG += m.tent;
    /* ⚠️⚠️ O QUE DECIDE É O QUE ELA FEZ. Antes, num caderno não terminado, o
       objetivo cujas folhas ela nem alcançou entrava em "retomar" com 0% — e o
       parecer dizia "precisa retomar" de uma criança que tinha ido bem no que
       deu tempo de fazer. Um julgamento errado com cara de medida, contra a
       criança. Objetivo não tocado não entra em lista nenhuma. */
    var pcObj = m.tent ? Math.round(100 * m.prim / m.tent) : -1;
    if(pcObj < 0) naoAlcancou.push(O.n.toLowerCase());
    else if(pcObj >= 75) domina.push(O.ok);
    else retomar.push(O.n.toLowerCase() + " (" + pcObj + "%)");
    var pcf = m.tent ? Math.round(100 * m.prim / m.tent) : 0;
    linhas += "<tr><td>" + esch(O.n) + "</td><td>" + m.prim + "/" + m.tot +
      "</td><td><b>" + m.pc + "%</b></td><td>" +
      (m.tent ? "<b>" + pcf + "%</b> <small>(" + m.prim + "/" + m.tent + ")</small>"
              : "<small>não fez</small>") + "</td><td>" + m.ajuda + "</td></tr>";
  }

  /* ⚠️ A NOTA DE UM CADERNO NÃO TERMINADO SE MEDE NO QUE FOI FEITO. Dividir
     pelos itens que ela nunca viu dá uma nota que não fala dela — fala do
     relógio. Com o caderno completo, os dois denominadores são o mesmo número. */
  var baseNota = inteiro ? total : tentG;
  var nota = baseNota ? Math.round(100 * pontos / baseNota) / 10 : 0;
  var pc = baseNota ? Math.round(100 * primG / baseNota) : 0;
  var conceito = !baseNota ? "Sem dados" :
    nota >= 8.5 ? "Dominou" : nota >= 6 ? "Está construindo" : "Precisa retomar";
  if(!inteiro) conceito += " (parcial)";

  var nome = esch(ST.nome || "O aluno");
  var parecer = nome + " ";
  if(domina.length && !retomar.length && !naoAlcancou.length)
    parecer += "domina os objetivos avaliados: " + domina.join("; ") + ".";
  else if(domina.length)
    parecer += "já " + domina.join("; ") + ". Ainda precisa retomar: " + retomar.join(", ") + ".";
  else
    parecer += "está começando a perceber que letras diferentes fazem o mesmo som. Nenhum " +
      "objetivo chegou a 75% de acerto de primeira — vale retomar ORALMENTE, ditando cinco " +
      "palavras por dia e perguntando POR QUE se escreve com aquela letra, antes de voltar " +
      "à tela. A regra dita em voz alta fixa mais do que a palavra copiada dez vezes.";
  if(naoAlcancou.length)
    parecer += " Ainda não chegou a fazer (a aula acabou antes): " + naoAlcancou.join(", ") + ".";

  var h = "<b>Relatório do professor</b> &mdash; " + nome + " &middot; " +
    Math.round((Date.now() - (ST.inicio || Date.now())) / 60000) + " min" +
    "<div class='notao'><span class='nn'>" + nota.toFixed(1).replace(".", ",") + "</span>" +
    "<span class='nl'><b>" + conceito + "</b><br>" + primG + " de " + baseNota +
    " de primeira (" + pc + "%)<br>" + ajudaG + " com ajuda</span></div>" +
    "<p class='parecer'>" + parecer + "</p>" +
    (inteiro ? "" :
      "<p class='avisoparcial'><b>Caderno não terminado:</b> " + folhasFeitas +
      " de " + NOMES.length + " folhas. A coluna <b>%</b> conta o caderno inteiro; " +
      "a coluna <b>do que fez</b> conta só o que a criança chegou a responder — " +
      "é esta que diz como ela foi.</p>") +
    "<table><tr><th>Objetivo</th><th>De primeira</th><th>%</th>" +
    "<th>do que fez</th><th>Com ajuda</th></tr>" + linhas + "</table>" +
    "<p class='comonota'>Nota de 0 a 10: acerto de primeira vale 1,0 e acerto com ajuda vale 0,6. " +
    "A criança não vê este número — ele fica só aqui.</p>" +
    "<p class='comonota'><b>O que este caderno NÃO mede:</b> várias das folhas de papel que " +
    "deram origem a ele terminam em <b>&ldquo;copie no seu caderno&rdquo;</b> e " +
    "<b>&ldquo;classifique no caderno&rdquo;</b> &mdash; e a tela não corrige o que a criança " +
    "escreve à mão. O que dá para medir aqui é reconhecer, marcar e escrever com o teclado. " +
    "<b>A cópia e o ditado no papel continuam sendo do professor</b>, e a folha 22 existe para " +
    "isso: a criança sai daqui com o quadro de regras dela para copiar no caderno.</p>";
  r.innerHTML = h; r.style.display = "block"; sPasso();
}
function esch(t){
  return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* ---------- retomar, chave mestra e a partida ---------- */
var CHAVE_MESTRA = "1275@";
function abreMenuProf(){
  var cx = document.getElementById("mpFolhas");
  if(!cx.childNodes.length){
    var mk = function(rot, alvo){
      var b = el("button", null, rot);
      b.onclick = function(){ fechaMenuProf(); vaiPara(alvo); };
      cx.appendChild(b);
    };
    mk("Capa", 0);
    /* ⚠️ `NOMES.length` e não um número cravado: com "10" escrito aqui, um
       caderno de 25 folhas mostrava só as dez primeiras no menu do professor —
       e as quinze restantes ficavam sem como conferir. */
    for(var k = 1; k <= NOMES.length; k++) mk(k + ". " + NOMES[k - 1], k);
  }
  calar(); document.getElementById("menuProf").className = "aberto";
}
function fechaMenuProf(){ document.getElementById("menuProf").className = ""; }
document.getElementById("mpFechar").onclick = fechaMenuProf;
document.getElementById("menuProf").onclick = function(ev){ if(ev.target === this) fechaMenuProf(); };
document.getElementById("nomeIn").oninput = function(){
  if(this.value.indexOf(CHAVE_MESTRA) > -1){ this.value = ST.nome || ""; abreMenuProf(); return; }
  ST.nome = this.value.slice(0, 24); espelhaNome(ST.nome); salvar();
};
document.getElementById("nomeIn").onkeydown = function(ev){ if(ev.key === "Enter"){ ev.preventDefault(); this.blur(); } };
document.getElementById("bComecar").onclick = function(){ ac(); sPasso(); if(!ST.inicio) ST.inicio = Date.now(); vaiPara(1); };
document.getElementById("bAnt").onclick = function(){ sPasso(); vaiPara(Math.max(0, ST.pag - 1)); };
document.getElementById("bProx").onclick = function(){
  sPasso();
  if(ST.pag === PAGEL.length - 1 && pendentes(ST.pag) === 0) return fim();
  vaiPara(Math.min(PAGEL.length - 1, ST.pag + 1));
};
document.getElementById("bOuvir").onclick = function(){ ac(); if(ultimaFala) falar(ultimaFala); };
document.getElementById("bVoz").onclick = function(){
  vozLigada = !vozLigada; this.className = vozLigada ? "zap" : "zap off";
  if(!vozLigada) calar(); else falar("vozOn");
};
document.getElementById("bRever").onclick = function(){ sPasso(); vaiPara(1); };
document.getElementById("bRecomecar").onclick = function(){
  sPasso(); try{ localStorage.removeItem(CHAVE_LS); }catch(e){}
  ST = {pag: 0, nome: ST.nome, folha: novaFolha(), resp: {}, lig: {}, tent: {}, prontas: {}, inicio: 0};
  monta(); vaiPara(0); falarDepois("novoCaderno", 400);
};
document.getElementById("bContinuar").onclick = function(){ ac(); sPasso(); vaiPara(ST.pag || 1); };
document.getElementById("bZerar").onclick = function(){ document.getElementById("bRecomecar").onclick(); };

(function boot(){
  var velho = carregar();
  if(velho && velho.folha){
    ST = velho;
    if(!ST.resp) ST.resp = {}; if(!ST.lig) ST.lig = {}; if(!ST.tent) ST.tent = {}; if(!ST.prontas) ST.prontas = {};
    /* ⚠️ TRAVA 2 — A REDE DE SEGURANÇA. Se montar a partir da memória estourar
       por qualquer motivo que eu não previ, o caderno joga a memória fora e
       abre LIMPO. Perder o "continuar de onde parou" é ruim; ficar com uma tela
       morta a aula toda é muito pior. */
    try{ monta(); }
    catch(erroMemoria){
      try{ localStorage.removeItem(CHAVE_LS); }catch(e3){}
      ST = {pag: 0, nome: ST.nome, folha: novaFolha(), resp: {}, lig: {}, tent: {}, prontas: {}, inicio: 0};
      monta(); vaiPara(0); return;
    }
    document.getElementById("retomar").style.display = "block";
    document.getElementById("retTxt").textContent =
      (ST.nome ? ST.nome + ", você" : "Você") + " parou na folha " + (ST.pag || 1) + ": " + NOMES[(ST.pag || 1) - 1] + ".";
    document.getElementById("nav").style.display = "none";
  } else {
    ST.folha = novaFolha(); monta(); vaiPara(0);
  }
})();

/*<dossie-js>*/
/* ============================================================
   DOSSIÊ PEDAGÓGICO — o que o PROFESSOR vê quando abre a atividade

   ⭐ PEDIDO DO MARCOS (set/2026): *"preciso que quando um professor olhe e
      analise a atividade ele veja que está ótima"*.

   O buraco que isto fecha: o parecer pedagógico de cada caderno existia — mas
   morava num arquivo `.md` DENTRO DO REPOSITÓRIO, que nenhum professor abre.
   Quem olhava a atividade via um joguinho bonito e não tinha como saber se
   aquilo estava alinhado ao currículo da rede. Agora o alinhamento está DENTRO
   da atividade, a um toque — e a qualquer momento, não só no fim.

   ⚠️ E não é texto solto: cada habilidade citada aqui vem do
   `<pasta>/curriculo.json`, e o portão `_qa/pedagogo_curriculo.py` reprova se a frase
   citada não existir, palavra por palavra, no `_curriculo/blumenau.txt`, ou se
   os objetivos do relatório e os do currículo não baterem um a um. Citação de
   currículo é a única coisa que o professor NÃO tem como conferir sozinho sem
   abrir 440 páginas de PDF — por isso ela é medida.

   Abre por dois caminhos: o botão no menu do professor (chave mestra 1275@,
   vale a qualquer hora) e o botão dentro do relatório, no fim.

   Este arquivo é a FONTE: `python3 _padrao/dossie_professor.py <pasta>` injeta o CSS, o
   trecho de tela e este código no caderno. Não editar a cópia injetada.
   ============================================================ */
function dossieCita(s){
  var m = String(s || "").match(/[“"]([^”"]+)[”"]/);
  return m ? m[1] : String(s || "");
}
function dossieHTML(){
  var C = (typeof CURRICULO === "object" && CURRICULO) ? CURRICULO : null;
  if(!C) return "<p>Este caderno ainda não declarou o currículo.</p>";
  var h = "", k, o;
  h += "<p class='dfonte'><b>" + esch(C.componente) + " &middot; " + C.ano +
       "º ano.</b> " + esch(C.rede) + ". As habilidades abaixo estão " +
       "<b>copiadas do documento oficial, palavra por palavra</b> &mdash; nenhuma " +
       "foi reescrita nem resumida.</p>";
  h += "<table><tr><th>O que a atividade mede</th><th>Folhas</th>" +
       "<th>Habilidade do currículo da rede</th></tr>";
  for(k = 0; k < C.objetivos.length; k++){
    o = C.objetivos[k];
    h += "<tr><td>" + esch(o.objetivo) + "</td><td>" + o.folhas.join(", ") +
         "</td><td>&ldquo;" + esch(dossieCita(o.habilidade)) + "&rdquo;" +
         "<span class='dobj'>" + esch(o.pratica) + " &middot; " +
         esch(o.objeto) + "</span></td></tr>";
  }
  h += "</table>";

  h += "<p class='dsub'><b>A escada didática</b> &mdash; uma folha por degrau, e " +
       "nenhuma repete o gesto da anterior:</p><ol class='descada'>";
  for(k = 0; k < NOMES.length; k++) h += "<li>" + esch(NOMES[k]) + "</li>";
  h += "</ol>";

  h += "<p class='dsub'><b>Como a criança é avaliada</b></p>" +
       "<p class='dtxt'>O relatório do professor (no fim, segurando a medalha por " +
       "2 segundos) traz, por objetivo: quantos itens ela acertou <b>de primeira</b>, " +
       "quantos precisou de ajuda e a porcentagem. A partir de 75% de acerto de " +
       "primeira o objetivo conta como dominado. Sai também um parecer em palavras " +
       "&mdash; do jeito que se escreve no bimestral &mdash; e uma nota de 0 a 10 " +
       "que <b>a criança não vê</b>. Dentro da atividade não há nota, nem ranking, " +
       "nem a palavra &ldquo;errou&rdquo;: o erro responde na hora e diz o que " +
       "olhar, e a ajuda cresce a cada tentativa (dica &rarr; apoio concreto &rarr; " +
       "revelar).</p>";

  if(C.evidencia && C.evidencia.length){
    h += "<p class='dsub'><b>O que foi medido antes de publicar</b></p><ul class='dev'>";
    for(k = 0; k < C.evidencia.length; k++) h += "<li>" + esch(C.evidencia[k]) + "</li>";
    h += "</ul>";
  }
  return h;
}
function abreDossie(){
  var cx = document.getElementById("dsCorpo");
  if(!cx) return;
  if(typeof calar === "function") calar();
  cx.innerHTML = dossieHTML();
  document.getElementById("dossie").className = "aberto";
  cx.scrollTop = 0;
}
function fechaDossie(){ document.getElementById("dossie").className = ""; }
(function(){
  var b = document.getElementById("bDossie"), f = document.getElementById("dsFechar"),
      cx = document.getElementById("dossie");
  if(b) b.onclick = function(){ fechaMenuProf(); abreDossie(); };
  if(f) f.onclick = fechaDossie;
  if(cx) cx.onclick = function(ev){ if(ev.target === this) fechaDossie(); };

  /* o segundo caminho: o botão nasce DENTRO do relatório, quando ele abre.
     Fica ali e não na tela final porque o relatório é a parte que a criança
     não vê — e o dossiê é conversa de adulto. */
  if(typeof abreRelatorio === "function"){
    var antes = abreRelatorio;
    abreRelatorio = function(){
      antes.apply(this, arguments);
      var r = document.getElementById("relatorio");
      if(r && !r.querySelector(".bdossie")){
        var bt = document.createElement("button");
        bt.className = "bt bdossie";
        bt.textContent = "Dossiê pedagógico (currículo da rede)";
        bt.onclick = abreDossie;
        r.appendChild(bt);
      }
    };
  }
}());
/*</dossie-js>*/

/* ⭐ o botão "Terminar" e o "Voltar para o caderno" — ver o comentário do fim() */
(function(){
  var bt = document.getElementById("bTerminar");
  if(bt) bt.onclick = function(){
    var falta = 0, pz;
    for(pz = 1; pz <= NOMES.length; pz++) falta += pendentes(pz);
    if(falta && !confirm("Quer fechar o caderno e ver o seu boletim?\n\nVocê pode voltar depois e continuar de onde parou."))
      return;
    fim();
  };
  var bv = document.getElementById("bVoltar");
  if(bv) bv.onclick = function(){
    document.getElementById("fim").style.display = "none";
    vaiPara(ST.pag || 1);
  };
})();

function figOu(f, cls){ return f ? img("cs_" + f + ".png", cls || "fig", "") : ""; }

/* ============================================================
   PEÇA — A FILEIRA DE LETRAS EMBARALHADAS (ideia do Marcos, 15/set/2026:
   *"ou somente colocar as letras das palavras selecionadas, embaralhadas... daí
   ocupa menos espaço e pode ser tudo na horizontal"*). Ela substituiu a barra de
   41 teclas, que comia meia tela.
   ⚠️⚠️ ONDE ELA NÃO PODE ENTRAR: em folha de ORTOGRAFIA as letras SÃO a
      pergunta, e pôr o Ç na fileira é DAR a resposta. Aqui ela entra na folha 33
      porque o desafio é ESCREVER a palavra que a frase pede, não escolher entre
      grafias parecidas.
   ⚠️ E O TECLADO DE VERDADE CONTINUA VALENDO em cima dela — as duas portas são
      regra da casa, e no PC da escola a criança vai digitar.
   ⚠️ COPIADA DO `_sil2`, onde ela já passou pelo jogador e pelo Marcos. A minha
      primeira versão aqui era reescrita e não fechava nenhum item: o `_digita`
      não voltava, então o `ATIVO_LETRAS` nunca apontava para a fileira.
   ============================================================ */
function fileiraLetras(box, id, pi, palavra, cels, fCerto, fDica){
  var val = "", feito = !!ST.resp[id];
  function pinta(){
    cels.forEach(function(c, i){
      c.textContent = feito ? palavra.charAt(i) : (val.charAt(i) || "");
      c.className = "ccel viva" + (feito ? " ok" : (val.charAt(i) ? " cheia" : ""));
    });
  }
  function confere(){
    if(mesmaPalavra(val, palavra)){
      feito = true; pinta();
      cx.className = "letrasfila pronta";
      acertou(id, fCerto); box.className = "item feito";
    } else {
      val = ""; pinta();
      cx.className = "letrasfila erro";
      setTimeout(function(){ cx.className = "letrasfila"; }, 480);
      bts.forEach(function(x){ x.b.className = "letrabt"; x.usada = false; });
      errou(id, fDica);
    }
  }
  var cx = el("div", "letrasfila"), bts = [];
  /* ⚠️ AS LETRAS REPETIDAS APARECEM REPETIDAS (RATO tem um A; VOVÓ tem dois O):
     dar uma letra só para duas posições deixaria a palavra impossível de
     montar — foi o defeito que o jogador pegou no banco de sílabas, e a lição
     serve igual aqui. */
  baralha(palavra.split("")).forEach(function(L, n){
    var b = el("button", "letrabt", L);
    b.setAttribute("aria-label", "Letra " + L);
    b.setAttribute("data-qa", "ltr-" + id + "-" + n);
    var reg = {b: b, L: L, usada: false};
    b.onclick = function(){
      if(feito || reg.usada) return;
      sTecla();
      reg.usada = true; b.className = "letrabt usada";
      val += L; pinta();
      if(val.length >= palavra.length) setTimeout(confere, 320);
    };
    cx.appendChild(b); bts.push(reg);
  });
  var ap = el("button", "letrabt apagar", "apagar");
  ap.setAttribute("aria-label", "Apagar a última letra");
  ap.onclick = function(){
    if(feito || !val.length) return;
    sTecla();
    var ult = val.charAt(val.length - 1), i;
    val = val.slice(0, -1);
    for(i = bts.length - 1; i >= 0; i--)
      if(bts[i].usada && bts[i].L === ult){ bts[i].usada = false; bts[i].b.className = "letrabt"; break; }
    pinta();
  };
  cx.appendChild(ap);
  box.appendChild(cx);
  pinta();
  /* a outra porta: o teclado de verdade escreve na mesma fileira */
  box._digita = function(ch){
    if(feito) return;
    if(ch === "ap"){ ap.onclick(); return; }
    if(ch === "ok"){ if(val.length) confere(); return; }
    var i;
    for(i = 0; i < bts.length; i++)
      if(!bts[i].usada && mesmaPalavra(bts[i].L, ch)){ bts[i].b.onclick(); return; }
  };
  return box._digita;
}

/* PEÇA — ACHAR DENTRO DO TEXTO (d35, VERBATIM: "Circule, no texto, as palavras
   com MP, MB e M final e copie-as abaixo")
   ⭐⭐⭐ O DEGRAU MAIS ALTO DO CADERNO: até aqui a palavra vinha sozinha; agora
      ela está escondida num texto e a criança tem de achá-la LENDO.
   ⚠️ O TEXTO É NOSSO. O da folha de papel é de Graça Batituci e tem direitos —
      o gesto entra, o texto não. */
function noTexto(d, pi, T, fCerto, fDica){
  var id = "n" + pi + "_0", box = item(0);
  registra(id, pi, T.ok.map(function(w){ return "w" + chaveQuadro(w); }).join(" "));
  var marcadas = {}, bts = [];
  var cx = el("div", "texto");
  cx.appendChild(el("h3", "ttit", T.titulo));
  var nw = 0;
  T.linhas.forEach(function(lin){
    var l = el("p", "tlin");
    lin.forEach(function(w) {
      var ok = T.ok.indexOf(w) > -1, meu = nw;
      var b = el("button", "palav", w);
      b.setAttribute("aria-label", w);
      /* ⚠️ só a palavra-RESPOSTA leva a chave do texto: as outras levam a
         POSIÇÃO, porque o travessão aparece quatro vezes e a chave dele sai
         vazia — seriam quatro `data-qa` iguais na mesma folha. */
      b.setAttribute("data-qa", ok ? ("op-" + id + "-w" + chaveQuadro(w))
                                   : ("no-" + id + "-x" + meu));
      nw++;
      b.onclick = function(){
        if(ST.resp[id]) return;
        /* ⚠️ pela POSIÇÃO: na lengalenga o "é" e o travessão dão os dois a
           chave VAZIA, e "Que" aparece duas vezes. */
        sPasso(); falar("tx" + pi + "_" + meu);
        if(marcadas[w]){ delete marcadas[w]; b.className = "palav"; }
        else { marcadas[w] = 1; b.className = "palav marcada"; }
      };
      l.appendChild(b); l.appendChild(document.createTextNode(" "));
      bts.push({b: b, w: w, ok: ok});
    });
    cx.appendChild(l);
  });
  box.appendChild(cx);
  var cf = el("button", "bt verde pronto", "Conferir");
  cf.setAttribute("data-qa", "conferir-" + id);
  cf.onclick = function(){
    if(ST.resp[id]) return;
    var certo = true;
    bts.forEach(function(x){ if(!!marcadas[x.w] !== !!x.ok) certo = false; });
    if(certo){
      bts.forEach(function(x){ if(x.ok) x.b.className = "palav ok"; });
      acertou(id, fCerto); box.className = "item feito"; cf.style.display = "none";
    } else {
      sErro(); cx.className = "texto erro";
      setTimeout(function(){ cx.className = "texto"; }, 480);
      errou(id, fDica);
    }
  };
  if(ST.resp[id]) cf.style.display = "none";
  box.appendChild(cf);
  fechaItem(d, box, id);
}

/* ⚠️ A FILEIRA DE LETRAS TAMBÉM OUVE O TECLADO DE VERDADE — as duas portas são
   regra da casa, e no PC da escola a criança vai digitar. `ATIVO_LETRAS` é a
   fileira que está esperando letra; tocar na grade do item a aponta para ele. */
var ATIVO_LETRAS = null;
document.addEventListener("keydown", function(ev){
  if(!ATIVO_LETRAS || CRUZ) return;
  if(document.activeElement && document.activeElement.id === "nomeIn") return;
  var t = (ev.key || "").toUpperCase();
  if(t.length === 1){ ev.preventDefault(); ATIVO_LETRAS(t); return; }
  if(ev.key === "Backspace"){ ev.preventDefault(); ATIVO_LETRAS("ap"); return; }
  if(ev.key === "Enter"){ ev.preventDefault(); ATIVO_LETRAS("ok"); return; }
});

/* ============================================================
   PEÇAS PRÓPRIAS DESTE CADERNO
   ============================================================ */

/* ⚠️ `SINAL` e `ORDEM3` moram no bloco DADOS do index.html, e não aqui: o
   `boot()` deste arquivo monta a primeira folha na hora em que o script
   termina de ler, e tudo o que estiver declarado DEPOIS dele ainda vale
   `undefined` nesse instante. Foi assim que as trinta e cinco folhas abriram
   em branco com um só `TypeError` no console. */

/* PEÇA — ESCOLHER O PONTO QUE FECHA A FRASE. Três botões grandes com o sinal
   DESENHADO (não a letra), porque é o desenho que a criança vai reconhecer na
   folha de papel depois. */
function escolhePonto(box, id, pi, certo, fCerto, fDica, quais){
  opcoes(box, pi, id, (quais || ORDEM3).map(function(k){
    return {v: k, rot: '<span class="sinalbt">' + SINAL[k].s + "</span>",
            aria: SINAL[k].n, fala: "nom_" + k};
  }), certo, "pal sin", fCerto, fDica);
}

/* PEÇA — A MESMA FRASE, TRÊS VOZES (D13)
   ⭐⭐⭐ O CORAÇÃO DO DEGRAU, e a única folha do caderno em que a VOZ é a
      pergunta: a criança ouve a frase dita de um jeito e diz qual ponto fecha
      aquele jeito. Sem o áudio esta folha não existe — por isso o botão de
      ouvir é grande e fica no meio. */
function tresVozes(box, id, pi, V, k, fCerto, fDica){
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "frasegrande", V.b + '<i class="lacuna peq"></i>'));
  box.appendChild(lin);
  var ouvir = el("button", "bt grande ouvir", "🔊 Ouvir como eu falei");
  ouvir.setAttribute("aria-label", "Ouvir a frase");
  ouvir.onclick = function(){ sPasso(); falar("voz_" + k); };
  box.appendChild(ouvir);
  escolhePonto(box, id, pi, V.pede, fCerto, fDica);
}

/* PEÇA — ARRASTAR O SINAL ATÉ O QUADRADINHO (D18/D25)
   ⚠️ Na folha de papel é RECORTAR E COLAR; na tela é arrastar. E o toque
      simples também vale — as duas portas são regra da casa. */
function arrastaSinal(box, id, pi, A, fCerto, fDica){
  var lin = el("div", "enunlin");
  var quad = el("span", "quadrado");
  quad.setAttribute("data-alvo", "1");
  quad.setAttribute("data-qa", "alvo-" + id);
  var fr = el("div", "frasegrande", A.f + " ");
  fr.appendChild(quad);
  lin.appendChild(fr);
  lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("arr_" + k(A)); }));
  box.appendChild(lin);
  opcoes(box, pi, id, baralha(ORDEM3.slice(0)).map(function(kk){
    return {v: kk, rot: '<span class="sinalbt">' + SINAL[kk].s + "</span>",
            aria: SINAL[kk].n, fala: "nom_" + kk};
  }), A.r, "pal sin", fCerto, fDica, function(b){
    quad.innerHTML = SINAL[A.r].s; quad.className = "quadrado cheio";
  }, [quad]);
  function k(x){ return x._k; }
}

/* PEÇA — ORDENAR AS PALAVRAS E FORMAR A FRASE (D06)
   ⭐ É a SEGMENTAÇÃO ENTRE PALAVRAS que o currículo nomeia: a criança vê onde
      cada palavra começa e acaba, e só então o ponto entra no fim. */
function ordenaPalavras(box, id, pi, O, fCerto, fDica){
  var alvo = O.r.split(" "), certo = [], n;
  for(n = 0; n < alvo.length; n++) certo.push("w" + n);
  certo.push("p" + O.p);
  registra(id, pi, certo.join(" "));
  var vaga = el("div", "linhafrase"), feitas = 0;
  box.appendChild(vaga);
  var cx = el("div", "palavras");
  baralha(alvo.map(function(w, i2){ return {w: w, n: i2}; })).forEach(function(P){
    var b = el("button", "palav gr", P.w);
    b.setAttribute("aria-label", P.w);
    b.setAttribute("data-qa", "op-" + id + "-w" + P.n);
    b.onclick = function(){
      if(ST.resp[id]) return;
      /* ⚠️ A FALA DESTA PALAVRA NASCE DA POSIÇÃO, e isto é conserto medido:
         "não" e "no" moram na MESMA frase da folha 21 e a chave da grafia
         (`chaveQuadro`) devolve `no` para as duas — uma gravação apagaria a
         outra e a criança ouviria a palavra errada, sem erro nenhum na tela. */
      sPasso(); falar("ord_" + O._k + "_w" + P.n);
      if(P.n !== feitas){
        b.className = "palav gr nao";
        setTimeout(function(){ b.className = "palav gr"; }, 420);
        errou(id, fDica); return;
      }
      b.className = "palav gr usada";
      vaga.appendChild(el("span", "napalavra", P.w));
      feitas++;
      if(feitas === alvo.length) pontos.className = "ops pal sin";
    };
    cx.appendChild(b);
  });
  box.appendChild(cx);
  /* e o ponto no fim, que a folha de papel lembra: *"Não se esqueça de colocar
     o sinal de pontuação!"* */
  var pontos = el("div", "ops pal sin escondida");
  ORDEM3.forEach(function(kk){
    var b = el("button", "op pal sin", '<span class="sinalbt">' + SINAL[kk].s + "</span>");
    b.setAttribute("aria-label", SINAL[kk].n);
    b.setAttribute("data-qa", (kk === O.p ? "op-" + id + "-p" + kk : "no-" + id + "-p" + kk));
    b.onclick = function(){
      if(ST.resp[id] || feitas < alvo.length) return;
      sPasso(); falar("nom_" + kk);
      if(kk !== O.p){
        b.className = "op pal sin erro";
        setTimeout(function(){ b.className = "op pal sin"; }, 460);
        errou(id, fDica); return;
      }
      b.className = "op pal sin certa";
      vaga.appendChild(el("span", "napalavra ponto", SINAL[kk].s));
      acertou(id, fCerto); box.className = "item feito";
    };
    pontos.appendChild(b);
  });
  box.appendChild(pontos);
}

/* PEÇA — CONSERTAR A FRASE (D31, VERBATIM: "Corrija as frases abaixo,
   observando a letra maiúscula e a pontuação")
   ⭐⭐ A única folha da colheita que junta MAIÚSCULA e PONTO, e o currículo do
      2º ano nomeia as duas na mesma linha. */
function conserta(box, id, pi, C, fCerto, fDica){
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "frasegrande erradinha", C.errada));
  lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("cor_" + C._k); }));
  box.appendChild(lin);
  /* ⚠️ A DIFERENÇA ENTRE AS DUAS TEM DE SER EXATAMENTE O QUE FALTA: se falta a
     maiúscula, a errada já vem com o ponto certo e só a primeira letra separa
     as duas; se falta o ponto, a letra já está certa e o que separa é o fim.
     Misturar as duas coisas deixa a criança escolhendo pela diferença errada. */
  var errado = C.falta === "maius" ? C.errada + C.certa.slice(-1)
                                   : C.certa.slice(0, -1);
  var ops = [
    {v: "certa", rot: C.certa, aria: C.certa, fala: "pal_" + chaveQuadro(C.certa)},
    {v: "outra", rot: errado, aria: errado, fala: "pal_" + chaveQuadro(C.certa)}];
  opcoes(box, pi, id, baralha(ops), "certa", "pal frase", fCerto, fDica);
}

/* ============================================================
   AS 35 FOLHAS — e a ordem É a escada.
   conhecer os três (1-5) → o ponto muda a VOZ (6-8) → a casinha (9-11) →
   arrastar o sinal (12-14) → a pergunta (15-19) → a frase inteira (20-24) →
   achar (25-29) → a voz no mundo (30-35).
   ============================================================ */

/* 1 — QUEM É QUEM (D32, VERBATIM: "Una corretamente") */
function f1(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Estes são os três moradores do caderno. Leve cada nome " +
            "até o desenho dele.", "p" + pi + "enun");
  var lista = ST.folha["p" + pi], alvos = [], marcada = null;
  var linha = el("div", "figalvos");
  baralha(lista.slice(0)).forEach(function(k){
    var L = LIGA[k];
    var a = el("div", "figalvo gr");
    a.innerHTML = figOu(L.f, "figm");
    a.setAttribute("data-alvo", "1");
    a.setAttribute("data-qa", "alvo-fig" + pi + "_" + k);
    a._v = k; a._dentro = el("div", "fdentro2"); a.appendChild(a._dentro);
    alvos.push(a); linha.appendChild(a);
  });
  d.appendChild(linha);
  var banco = el("div", "figbanco");
  lista.forEach(function(k, i){
    var L = LIGA[k], id = "n" + pi + "_" + i;
    registra(id, pi, ">fig" + pi + "_" + k);
    var b = el("button", "op pal" + (ST.resp[id] ? " usada" : ""), L.p);
    b.setAttribute("aria-label", L.p);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    function larga(a){
      if(ST.resp[id]) return;
      if(a._v === k){
        b.className = "op pal usada";
        a._dentro.appendChild(el("span", "fdentro", L.p));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + k);
      } else {
        a.className = "figalvo gr erro";
        setTimeout(function(){ a.className = "figalvo gr"; }, 500);
        errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("nom_" + k.replace("a1", "inter").replace("a2", "excl").replace("a3", "final"));
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
    };
    puxavel(b, alvos, function(a){ larga(a); });
    banco.appendChild(b);
  });
  alvos.forEach(function(a){ a.onclick = function(){ if(marcada && marcada._larga) marcada._larga(a); }; });
  d.appendChild(banco);
}

/* 2, 3, 4 e 5 — QUAL PONTO FECHA A FRASE? (D10, D09, D05) */
function montaPonto(d, pi, quais){
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PON[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasegrande", P.f + '<i class="lacuna peq"></i>'));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("fra_" + k); }));
    box.appendChild(lin);
    escolhePonto(box, id, pi, P.r, "certo" + pi + "_" + k, "dica" + pi + "_" + k, quais);
    fechaItem(d, box, id);
  });
}
function f2(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ouça a frase. Ela <b>conta</b> uma coisa ou <b>pergunta</b> " +
            "uma coisa?", "p" + pi + "enun");
  montaPonto(d, pi, ["inter", "final"]);
}
function f3(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora é susto e alegria contra pergunta. Ouça o jeito de " +
            "falar.", "p" + pi + "enun");
  montaPonto(d, pi, ["inter", "excl"]);
}
function f4(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Os <b>três</b> juntos. Ouça a frase e escolha o ponto que " +
            "fecha ela.", "p" + pi + "enun");
  montaPonto(d, pi);
}
function f5(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais seis frases. Diga cada uma em voz alta antes de " +
            "escolher.", "p" + pi + "enun");
  montaPonto(d, pi);
}

/* 6 e 7 — A MESMA FRASE, TRÊS VOZES (D13) */
function montaVozes(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var V = VOZ[k], id = "n" + pi + "_" + i, box = item(i + 1);
    tresVozes(box, id, pi, V, k, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f6(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "A frase é a <b>mesma</b> — o que muda é o jeito de falar. " +
            "Ouça e escolha o ponto daquele jeito.", "p" + pi + "enun");
  montaVozes(d, pi);
}
function f7(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "De novo a mesma frase, com outra voz. Escute com atenção.",
            "p" + pi + "enun");
  montaVozes(d, pi);
}

/* 8 — QUE TIPO DE FRASE É? (D07) */
function f8(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "A frase já vem pontuada. Ela <b>conta</b>, <b>pergunta</b> " +
            "ou <b>se espanta</b>?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var T = TIPO[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasegrande", T.f));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("tip_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, [
      {v: "inter", rot: "Pergunta", aria: "pergunta", fala: "nom_inter"},
      {v: "excl", rot: "Espanto", aria: "espanto", fala: "nom_excl"},
      {v: "final", rot: "Conta", aria: "conta", fala: "nom_final"}],
      T.r, "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* 9, 10 e 11 — A CASINHA DA PONTUAÇÃO (D28) */
function f9(d, pi){ gavetas(d, pi, "gA", "Cada ponto tem a sua casinha. Leve a frase para a casa do ponto que fecha ela."); }
function f10(d, pi){ gavetas(d, pi, "gB", "Mais frases para achar a casa. Leia cada uma em voz alta."); }
function f11(d, pi){ gavetas(d, pi, "gC", "Agora as frases são mais compridas — mas o fim delas continua entregando a casa."); }

/* 12, 13 e 14 — ARRASTE O SINAL (D18/D25) */
function montaArrasta(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var A = ARR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    A._k = k;
    arrastaSinal(box, id, pi, A, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Puxe o sinal certo até o <b>quadradinho</b> do fim da " +
            "frase. Tocar nele também vale.", "p" + pi + "enun");
  montaArrasta(d, pi);
}
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais três frases esperando o sinal delas.", "p" + pi + "enun");
  montaArrasta(d, pi);
}
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Estas são mais difíceis: leia com calma e escute a sua " +
            "própria voz.", "p" + pi + "enun");
  montaArrasta(d, pi);
}

/* 15 e 16 — A PALAVRA QUE ABRE A PERGUNTA (D30 e D31) */
function montaQue(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var Q = QUE[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasegrande", '<i class="lacuna"></i> ' + Q.z));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("que_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(Q.ops.map(function(w){
      return {v: chaveQuadro(w), rot: w, aria: w, fala: "pal_" + chaveQuadro(w)};
    })), chaveQuadro(Q.r), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f15(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toda pergunta começa com uma palavra que <b>pede</b> uma " +
            "coisa. Qual é a desta?", "p" + pi + "enun");
  montaQue(d, pi);
}
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais perguntas. Repare no que a frase está querendo saber.",
            "p" + pi + "enun");
  montaQue(d, pi);
}

/* 17 — LIGUE A PERGUNTA À RESPOSTA (D14) */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toda pergunta tem a sua resposta. Leve cada resposta até a " +
            "pergunta dela.", "p" + pi + "enun");
  var lista = ST.folha["p" + pi], alvos = [], marcada = null;
  var col = el("div", "pergcol");
  lista.forEach(function(k){
    var P = PAR[k];
    var a = el("div", "pergunta2");
    a.appendChild(el("span", "ptxt", P.p));
    a.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("prg_" + k); }));
    a.setAttribute("data-alvo", "1");
    a.setAttribute("data-qa", "alvo-prg" + pi + "_" + k);
    a._v = k; a._dentro = el("div", "fdentro2"); a.appendChild(a._dentro);
    alvos.push(a); col.appendChild(a);
  });
  d.appendChild(col);
  var banco = el("div", "figbanco");
  baralha(lista.slice(0)).forEach(function(k){
    var P = PAR[k], i = lista.indexOf(k), id = "n" + pi + "_" + i;
    registra(id, pi, ">prg" + pi + "_" + k);
    var b = el("button", "op pal frase", P.r);
    b.setAttribute("aria-label", P.r);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    function larga(a){
      if(ST.resp[id]) return;
      if(a._v === k){
        b.className = "op pal frase usada";
        a._dentro.appendChild(el("span", "fdentro", P.r));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + k);
      } else {
        a.className = "pergunta2 erro";
        setTimeout(function(){ a.className = "pergunta2"; }, 500);
        errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("res_" + k);
      if(marcada === b){ b.className = "op pal frase"; marcada = null; return; }
      if(marcada) marcada.className = "op pal frase";
      b.className = "op pal frase marcada"; marcada = b;
    };
    puxavel(b, alvos, function(a){ larga(a); });
    banco.appendChild(b);
  });
  alvos.forEach(function(a){ a.onclick = function(){ if(marcada && marcada._larga) marcada._larga(a); }; });
  d.appendChild(banco);
}

/* 18 e 19 — RESPONDA OLHANDO A FIGURA (D12) */
function montaResp(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var R = RESPF[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(R.f, "figm");
    lin.appendChild(el("div", "frasegrande", R.p));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("rsp_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(R.ops.map(function(w){
      return {v: chaveQuadro(w), rot: w, aria: w, fala: "pal_" + chaveQuadro(w)};
    })), chaveQuadro(R.r), "pal frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe a figura e responda. Repare: a resposta termina em " +
            "<b>ponto final</b>.", "p" + pi + "enun");
  montaResp(d, pi);
}
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais perguntas com figura. A pergunta acaba em <b>ponto de " +
            "interrogação</b> e a resposta em <b>ponto final</b>.", "p" + pi + "enun");
  montaResp(d, pi);
}

/* 20 e 21 — AS PALAVRAS SE EMBARALHARAM (D06) */
function montaOrdena(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var O = ORD[k], id = "n" + pi + "_" + i, box = item(i + 1);
    O._k = k;
    var lin = el("div", "enunlin");
    lin.appendChild(botaoSom("Ouvir a frase pronta", function(){ falar("ord_" + k); }));
    box.appendChild(lin);
    ordenaPalavras(box, id, pi, O, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque nas palavras <b>na ordem</b> e monte a frase. No fim, " +
            "não esqueça do ponto.", "p" + pi + "enun");
  montaOrdena(d, pi);
}
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Frases mais compridas. Ouça a frase pronta antes de " +
            "começar.", "p" + pi + "enun");
  montaOrdena(d, pi);
}

/* 22 e 23 — CONSERTE A FRASE (D31) */
function montaConserta(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var C = COR_[k], id = "n" + pi + "_" + i, box = item(i + 1);
    C._k = k;
    conserta(box, id, pi, C, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta frase saiu errada. Qual é a certa? Olhe a <b>primeira " +
            "letra</b> e o <b>fim</b> dela.", "p" + pi + "enun");
  montaConserta(d, pi);
}
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais três para consertar. Numas falta a <b>letra " +
            "maiúscula</b>, noutras falta o <b>ponto</b>.", "p" + pi + "enun");
  montaConserta(d, pi);
}

/* 24 — ESCREVA A PALAVRA DA PERGUNTA */
function f24(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escreva a palavra tocando nas letras — ou digite no seu " +
            "teclado.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var X = ESCR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, X.w);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", X.d));
    lin.appendChild(botaoSom("Ouvir a pista", function(){ falar("esc_" + k); }));
    box.appendChild(lin);
    var grade = el("div", "cruz uma"), cels = [], t;
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < X.w.length; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""),
                 ST.resp[id] ? X.w.charAt(t) : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    box.appendChild(grade);
    var teclar = fileiraLetras(box, id, pi, X.w, cels,
                               "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    grade.onclick = function(){ if(!ST.resp[id]) ATIVO_LETRAS = teclar; };
    fechaItem(d, box, id);
  });
}

/* 25 e 26 — ACHE NO TEXTO (D14) */
function f25(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leia a lengalenga e toque nas palavras que terminam com " +
            "<b>ponto de interrogação</b>. Depois confira.", "p" + pi + "enun");
  noTexto(d, pi, TXT.t1, "certo" + pi + "_t", "dica" + pi + "_t");
}
function f26(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora ache as que terminam com <b>ponto de exclamação</b>.",
            "p" + pi + "enun");
  noTexto(d, pi, TXT.t2, "certo" + pi + "_t", "dica" + pi + "_t");
}

/* 27 — O CAÇA-PALAVRAS DOS SINAIS (D08) */
function f27(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ache cada palavra: toque na <b>primeira</b> letra e depois " +
            "na <b>última</b>.", "p" + pi + "enun");
  var cels = {};
  var g = el("div", "cpgrade");
  CACA.grade.forEach(function(lin, y){
    var l = el("div", "cplin");
    lin.forEach(function(L, x){
      var b = el("button", "cpcel", L);
      b.setAttribute("aria-label", L);
      cels[y + "," + x] = b; l.appendChild(b);
    });
    g.appendChild(l);
  });
  d.appendChild(g);
  var lista = el("div", "cplista");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CACA.pal[k], id = "n" + pi + "_" + i;
    registra(id, pi, "cpa cpz");
    var rot = el("div", "cprot" + (ST.resp[id] ? " achada" : ""), C.p);
    rot.appendChild(botaoSom("Ouvir a palavra", function(){ falar("pal_" + chaveQuadro(C.p)); }));
    lista.appendChild(rot);
    var ca = cels[C.a[0] + "," + C.a[1]], cz = cels[C.z[0] + "," + C.z[1]];
    ca.setAttribute("data-qa", "cp-" + id + "-a");
    cz.setAttribute("data-qa", "cp-" + id + "-z");
    function marca(){
      var y = C.a[0], x;
      for(x = C.a[1]; x <= C.z[1]; x++) cels[y + "," + x].className = "cpcel achada";
      rot.className = "cprot achada";
    }
    if(ST.resp[id]) marca();
    var passo = 0;
    [ca, cz].forEach(function(cel, n){
      cel.addEventListener("click", function(){
        if(ST.resp[id]) return;
        sPasso();
        if(n === 0){ passo = 1; cel.className = "cpcel pega"; return; }
        if(passo !== 1){ falar("cacatoque"); return; }
        marca(); acertou(id, "certo" + pi + "_" + k);
      });
    });
  });
  d.appendChild(lista);
}

/* 28 e 29 — QUAL ESTÁ PONTUADA CERTA? (D35) */
function montaCerta(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CERT[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Qual das duas está pontuada <b>certa</b>?"));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("cer_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(C.ops.map(function(w){
      return {v: chaveQuadro(w) + (w.slice(-1) === "?" ? "i" : w.slice(-1) === "!" ? "e" : "f"),
              rot: w, aria: w, fala: "pal_" + chaveQuadro(w)};
    })), chaveQuadro(C.r) + (C.r.slice(-1) === "?" ? "i" : C.r.slice(-1) === "!" ? "e" : "f"),
    "pal frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f28(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As duas frases têm as <b>mesmas palavras</b>. Só uma está " +
            "com o ponto certo.", "p" + pi + "enun");
  montaCerta(d, pi);
}
function f29(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais quatro para revisar. Leia cada uma do jeito que o " +
            "ponto manda.", "p" + pi + "enun");
  montaCerta(d, pi);
}

/* 30 e 31 — PONTUE A HISTÓRIA (D23) */
function montaHist(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var H = HIST[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasegrande", H.f + '<i class="lacuna peq"></i>'));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("his_" + k); }));
    box.appendChild(lin);
    escolhePonto(box, id, pi, H.r, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f30(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta história ficou sem pontos. Feche cada frase.",
            "p" + pi + "enun");
  montaHist(d, pi);
}
function f31(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "O fim da história. Escute o jeito de falar de cada frase.",
            "p" + pi + "enun");
  montaHist(d, pi);
}

/* 32 — INVENTE A SUA PALAVRA (D21, VERBATIM: "Desafio criativo: escreva uma
   pergunta para um amigo")
   ⚠️ É PRODUÇÃO: vale qualquer palavra da lista, e o que fica escrito é o que a
      CRIANÇA escolheu — não o gabarito. */
function f32(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora é a sua vez de inventar. Escreva uma palavra que " +
            "sirva para cada pedido.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var X = DESA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, X.ok[0]);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Escreva " + X.q + "."));
    lin.appendChild(botaoSom("Ouvir o pedido", function(){ falar("des_" + k); }));
    box.appendChild(lin);
    var mx = 0;
    X.ok.forEach(function(w){ if(w.length > mx) mx = w.length; });
    var grade = el("div", "cruz uma livre"), cels = [], t;
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < mx; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""),
                 ST.resp[id] ? (X.ok[0].charAt(t) || "") : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    box.appendChild(grade);
    /* ⚠️ `E.aceita` é o que faz esta folha ser de PRODUÇÃO: vale qualquer
       palavra da lista, e a que fica escrita é a que ELA escreveu. */
    var E = {k: k, w: X.ok[0], aceita: X.ok, id: id, cels: cels, n: i + 1,
             rot: "Escreva a sua palavra", bt: el("span", "pista oculta", "")};
    cels.forEach(function(c){ c.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); }; });
    grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
    fechaItem(d, box, id);
  });
}

/* 33 e 34 — A CENA PEDE O SINAL (D34) */
function montaCena(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CENA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(C.f, "figm");
    lin.appendChild(el("div", "frasegrande", C.p + '<i class="lacuna peq"></i>'));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("cen_" + k); }));
    box.appendChild(lin);
    escolhePonto(box, id, pi, C.r, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f33(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe a cena e a frase. Qual ponto combina com ela?",
            "p" + pi + "enun");
  montaCena(d, pi);
}
function f34(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais três cenas. A mesma figura pode pedir pontos " +
            "diferentes — quem manda é a frase.", "p" + pi + "enun");
  montaCena(d, pi);
}

/* 35 — O CARTAZ QUE VOCÊ LEVA (D37)
   ⭐⭐ O CONCEITO VEM POR ÚLTIMO: a criança passou trinta e quatro folhas
      ouvindo a voz mudar; só agora ela recebe os três nomes por escrito. */
function f35(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Você já sabe tudo isto. Agora os três nomes: leve cada " +
            "frase para a linha dela.", "p" + pi + "enun");
  var cart = el("div", "cartaz"), linhas = {}, listaC = [];
  CART.linhas.forEach(function(L){
    var l = el("div", "cartlin");
    var t = el("div", "cartit");
    t.innerHTML = '<span class="sinalbt gr">' + SINAL[L.k].s + "</span><b>" + L.t +
                  "</b><span>" + L.d + "</span>";
    t.appendChild(botaoSom("Ouvir", function(){ falar("cart_" + L.k); }));
    l.appendChild(t);
    var alvo = el("div", "cartalvo");
    alvo.setAttribute("data-alvo", "1");
    alvo.setAttribute("data-qa", "alvo-cart" + pi + "_" + L.k);
    alvo.appendChild(el("span", "cartex", L.e));
    l.appendChild(alvo);
    l._v = L.k; l._dentro = alvo;
    linhas[L.k] = l; listaC.push(l);
    cart.appendChild(l);
  });
  d.appendChild(cart);
  var banco = el("div", "figbanco"), marcada = null;
  ST.folha["p" + pi].forEach(function(k, i){
    var X = CART.exem[k], id = "n" + pi + "_" + i;
    registra(id, pi, ">cart" + pi + "_" + X.c);
    var b = el("button", "op pal frase" + (ST.resp[id] ? " usada" : ""), X.p);
    b.setAttribute("aria-label", X.p);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    if(ST.resp[id]) linhas[X.c]._dentro.appendChild(el("span", "fdentro", X.p));
    function larga(l){
      if(ST.resp[id]) return;
      if(l._v === X.c){
        b.className = "op pal frase usada";
        l._dentro.appendChild(el("span", "fdentro", X.p));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + k);
      } else {
        l.className = "cartlin erro";
        setTimeout(function(){ l.className = "cartlin"; }, 500);
        errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("pal_" + chaveQuadro(X.p));
      if(marcada === b){ b.className = "op pal frase"; marcada = null; return; }
      if(marcada) marcada.className = "op pal frase";
      b.className = "op pal frase marcada"; marcada = b;
    };
    puxavel(b, listaC, function(l){ larga(l); });
    banco.appendChild(b);
  });
  listaC.forEach(function(l){ l.onclick = function(){ if(marcada && marcada._larga) marcada._larga(l); }; });
  d.appendChild(banco);
}
