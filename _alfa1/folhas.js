/* ============================================================
   A FÁBRICA DE PALAVRAS — as dez folhas.

   Cada folha nasceu de um VERBO impresso numa folha real de alfabetização
   (as 41 de `_pesquisa/fotos/ddg-alfa-1ano/`). O catálogo desses verbos é o
   `_padrao/INTERATIVIDADES-FOLHA.md`. Nenhuma mecânica foi escolhida do nosso
   cardápio: a folha é que manda.
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [];

function faixa(d, i, titulo){ d.appendChild(el("div", "faixa", '<div class="num">' + i + '</div><h2>' + titulo + '</h2>')); }
function aoAbrir(d, fn){ if(!d._aoAbrir) d._aoAbrir = []; d._aoAbrir.push(fn); }
function item(n){ return el("div", "item", n ? '<span class="n">' + n + '.</span>' : ""); }

function monta(){
  livro.innerHTML = ""; PAGEL = []; RESP = {};
  var caps = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10], i;
  for(i = 0; i < caps.length; i++){
    var d = el("div", "pagina" + (i > 0 ? " " + CORES[i - 1] : "")); d.setAttribute("data-pag", i);
    caps[i](d, i);
    if(i > 0) d.appendChild(el("div", "carimbo", "FOLHA<br>PRONTA"));
    livro.appendChild(d); PAGEL.push(d);
  }
}

/* ---------- capa ----------
   Pedido do Marcos (set/2026): *"essas atividades deveriam ter uma capa bem
   legal e bonita"*. A capa não é enfeite: é a primeira coisa que a criança de
   seis anos vê, e é ela que diz "isto aqui é um lugar bom".

   A ideia vem do nome: uma FÁBRICA de palavras. Então há uma esteira, e da
   esteira saem as letras que formam o título; embaixo, as figuras que ela vai
   encontrar nas folhas, como se tivessem acabado de ser fabricadas.
   Tudo em CSS e PNG — nada de SVG, nada de emoji (regra do Marcos).
   As letras entram uma a uma; quem pediu menos movimento recebe tudo parado. */
function f0(d){
  var c = el("div", "capa"), nome = "FÁBRICA DE PALAVRAS", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i></div>' +
    '<div class="chapeu">A</div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Alfabetização &middot; 1º ano &middot; dez folhas para brincar</div>' +
    '<div class="esteira">' +
      '<div class="cena">' + img("bola") + img("gato") + img("casa") + img("sapo") + img("uva") + '</div>' +
      '<div class="cinta"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>' +
    '</div>' +
    '<div class="chamada">Escreva o seu nome ali embaixo e toque em <b>Começar</b>.</div>';
  d.appendChild(c);
}

/* ---------- fileira de opções (usada em várias folhas) ----------
   `soltarEm` (opcional) liga o ARRASTAR: a criança pode puxar a figura até o
   quadro vazio em vez de só tocar nela. Pedido do Marcos, set/2026:
   *"da atividade o que vem depois a criança pode tanto clicar como arrastar a
   imagem até o local"*. As DUAS portas, sempre — no PC da escola ela usa o
   mouse e arrastar é o gesto natural; no celular, tocar é. */
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
   quebrou duas vezes nesta casa. Aqui o `setPointerCapture` prende o ponteiro
   no botão e o mesmo código serve para os três.
   ⚠️ E nada de `preventDefault` no início: isso mataria o toque. Só depois de
   o dedo ANDAR 8 px é que vira arrasto — antes disso continua sendo um toque
   normal, e o `onclick` responde igual. */
var PUXA = null;   /* o arrasto em andamento (um de cada vez) */

function puxavel(bt, alvos, aoSoltar){
  if(!alvos.push) alvos = [alvos];
  bt.style.touchAction = "none";
  bt.addEventListener("pointerdown", function(ev){
    if(ev.button && ev.button !== 0) return;
    PUXA = {bt: bt, alvos: alvos, aoSoltar: aoSoltar,
            x0: ev.clientX, y0: ev.clientY,
            lx: ev.clientX, ly: ev.clientY,   /* último lugar onde o dedo esteve */
            andando: false, fantasma: null};
  });
}

/* ⚠️⚠️ DUAS LIÇÕES PAGAS AQUI (set/2026), as duas achadas por teste e nenhuma
   delas dava erro na tela — o arrasto simplesmente não acontecia:

   1. `setPointerCapture` no próprio botão + `pointermove` NELE: só o primeiro
      movimento chegava. O padrão certo é ouvir no DOCUMENTO — o dedo precisa
      poder SAIR de cima da peça, que é justamente o que ele faz ao levá-la.

   2. O navegador FUNDE os movimentos (coalescing). Num teste com 8 passos
      chegou UM `pointermove`, de 5 px. Se eu decidir "isto é um arrasto" pela
      contagem de movimentos, perco a jogada. Então quem MANDA é a SOLTURA:
      apertou na peça e soltou em cima do alvo = soltou ali, tenham chegado dez
      movimentos ou um. O fantasma que segue o dedo é enfeite útil; a resposta
      não depende dele.

   E um só par de ouvintes no documento, não um por peça: com 18 figuras numa
   folha eram 18 cópias do mesmo tratador rodando a cada movimento. */
function _puxaAnda(ev){
  var P = PUXA; if(!P) return;
  P.lx = ev.clientX; P.ly = ev.clientY;
  var dx = ev.clientX - P.x0, dy = ev.clientY - P.y0;
  if(!P.andando){
    if(dx * dx + dy * dy < 64) return;            /* menos de 8 px: ainda é toque */
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
  /* ⚠️ TERCEIRA LIÇÃO PAGA: o `pointercancel` chega ANTES do `pointerup` e vem
     com clientX/clientY = 0,0. Quem usasse a coordenada dele concluiria que a
     criança soltou no canto superior esquerdo da tela — e a peça nunca cairia
     no lugar. Por isso o último ponto REAL fica guardado (`lx`,`ly`) e é ele
     que manda quando o evento chega sem posição. */
  var px = ev.clientX, py = ev.clientY;
  if(!px && !py){ px = P.lx; py = P.ly; }
  var onde = {clientX: px, clientY: py};
  var andou = (px - P.x0) * (px - P.x0) + (py - P.y0) * (py - P.y0) >= 64;
  if(!andou) return;                              /* foi toque, o onclick resolve */
  P.bt._arrastou = true;
  var i;
  for(i = 0; i < P.alvos.length; i++){
    if(sobre(onde, P.alvos[i])){ P.aoSoltar(P.alvos[i], i); break; }
  }
  setTimeout(function(){ P.bt._arrastou = false; }, 60);
}
/* e o arrasto NATIVO do navegador fica desligado na atividade inteira: era ele
   que disparava o `pointercancel` e matava o nosso. */
document.addEventListener("dragstart", function(ev){ ev.preventDefault(); });
document.addEventListener("pointermove", _puxaAnda);
document.addEventListener("pointerup", _puxaSolta);
document.addEventListener("pointercancel", _puxaSolta);

function sobre(ev, alvo){
  var r = alvo.getBoundingClientRect(), m = 14;
  return ev.clientX >= r.left - m && ev.clientX <= r.right + m &&
         ev.clientY >= r.top - m && ev.clientY <= r.bottom + m;
}

/* ---------- a letra VOA para o buraco (pedido do Marcos, set/2026) ----------
   Palavras dele: *"ao clicar na letra certa ele completar a palavra de cima,
   saindo o ponto de interrogação, uma animação bem legal"*.

   Por que isto não é enfeite: a criança de 6 anos precisa VER a ligação entre
   o que ela tocou e o buraco lá em cima. O voo é a linha que liga as duas
   coisas — sem ele, o "?" simplesmente vira letra e metade da turma não repara
   que foi a escolha dela que fez aquilo.

   ⚠️ O clone voa em `position:fixed` por cima de tudo: assim ele não empurra
   nada do leiaute e atravessa a rolagem sem entortar. E quem não quer animação
   (`prefers-reduced-motion`) recebe o resultado na hora, sem voo. */
function voaLetra(botao, buraco, letra, linha){
  function pousa(){
    buraco.className = "buraco ok";
    buraco.innerHTML = letra;
    linha.className = "escondida completa";
    sPalma();
  }
  var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(quieto || !botao.getBoundingClientRect){ pousa(); return; }
  var de = botao.getBoundingClientRect(), pra = buraco.getBoundingClientRect();
  var v = el("div", "voa", letra);
  v.style.left = de.left + "px"; v.style.top = de.top + "px";
  v.style.width = de.width + "px"; v.style.height = de.height + "px";
  document.body.appendChild(v);
  buraco.className = "buraco indo";
  setTimeout(function(){
    v.style.transform = "translate(" + (pra.left - de.left + (pra.width - de.width) / 2) + "px," +
                        (pra.top - de.top + (pra.height - de.height) / 2) + "px) scale(1.25)";
  }, 20);
  setTimeout(function(){
    if(v.parentNode) v.parentNode.removeChild(v);
    pousa();
  }, 520);
}

/* ============ 1 — A LETRA ESCONDIDA ============
   Da folha: *"descubra qual é a letra escondida e complete"* (d06) e
   *"complete cada palavra com as letras inicial e final"* (d17/d19). */
function f1(d, pi){
  faixa(d, pi, NOMES[0]);
  d.appendChild(el("div", "enun", "Uma letra se escondeu. Toque na letra <b>certa</b> para ela voltar."));
  var L = ST.folha.p1;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var w = esc(it.p), certa = w.charAt(it.pos), id = "r1_" + i;
      var b = item(i + 1);
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(it.p) + '</div>'));
      var lin = el("div", "escondida"), buraco = null;
      for(var k = 0; k < w.length; k++){
        if(k === it.pos){
          buraco = el("div", "buraco" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? certa : "?");
          lin.appendChild(buraco);
        } else lin.appendChild(el("span", "lt", w.charAt(k)));
      }
      if(ST.resp[id]) lin.className = "escondida completa";
      b.appendChild(lin);
      var outras = "ABCDEFGHIJLMNOPRSTUVZ".split("").filter(function(x){ return x !== certa; });
      var ops = baralha([certa, outras[rnd(outras.length)], outras[rnd(outras.length)]]).map(function(x){
        return {v: x, rot: x, fala: "letra_" + x, aria: "Letra " + x};
      });
      opcoes(b, pi, id, ops, certa, null, "certo1_" + it.p, "dica1_" + it.p, function(botao){
        voaLetra(botao, buraco, certa, lin);
      });
      b.setAttribute("data-qa", "item-" + id);
      d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 2 — QUANTAS SÍLABAS ============
   Da folha: *"conte quantas sílabas há em cada palavra"* (d07/d09).
   O currículo pede SEGMENTAR ORALMENTE: então ela BATE, uma vez por pedaço. */
function f2(d, pi){
  faixa(d, pi, NOMES[1]);
  /* ⚠️ "SÍLABA", NÃO "PEDAÇO" (pedido do Marcos, set/2026: *"não tem outra
     expressão mais didática, tipo sílaba?"*). Ele tem razão e o currículo
     também: a BNCC do 1º ano (EF01LP08/EF01LP09) e o currículo de Blumenau
     dizem SÍLABA com todas as letras. "Pedacinho" serve como apoio na PRIMEIRA
     vez — é assim que a professora apresenta —, mas quem fica é a palavra
     certa; senão a criança chega no 2º ano sem o nome da coisa. */
  d.appendChild(el("div", "enun", "Fale a palavra batendo <b>uma palma em cada sílaba</b> " +
    "(cada pedacinho). Depois toque em <b>Pronto</b>."));
  var L = ST.folha.p2;
  for(var i = 0; i < L.length; i++){
    (function(p, i){
      var id = "r2_" + i, alvo = sil(p).length, n = 0;
      registra(id, pi, alvo);
      var b = item(i + 1), cx = el("div", "bater");
      cx.appendChild(el("div", null, img(p)));
      cx.appendChild(el("div", "pal", esc(p)));
      var cont = el("div", "contab", "palmas: <b>0</b>");
      var trilha = el("div", "trilhasil");   /* as sílabas acendendo, uma por palma */
      sil(p).forEach(function(s, k){
        var c = el("span", "silbox" + (ST.resp[id] ? " acesa" : ""), s);
        c.setAttribute("data-qa", "silbox-" + id + "-" + k);
        trilha.appendChild(c);
      });
      var bt = el("button", "palma", "BATER PALMA");
      bt.setAttribute("data-qa", "bater-" + id);
      var ok = el("button", "bt verde", "Pronto");
      ok.setAttribute("data-qa", "pronto-" + id);
      /* ⭐ CADA PALMA DIZ A SUA SÍLABA (pedido do Marcos, set/2026: *"depois que
         ele faça dos pedaços ele tem que pronunciar todas as sílabas, exemplo
         gi ra fa"*). É exatamente o que a professora faz na roda: bate e FALA.
         Sem a voz, a criança só conta batidas — e contar batida não é segmentar.
         Bateu além do fim da palavra, ninguém fala: o silêncio já avisa que
         passou. */
      bt.onclick = function(){
        if(ST.resp[id]) return;
        n++; sPalma(); cont.innerHTML = "palmas: <b>" + n + "</b>";
        var caixas = trilha.childNodes, k;
        for(k = 0; k < caixas.length; k++) caixas[k].className = "silbox" + (k < n ? " acesa" : "");
        if(n <= alvo) falar("sb_" + sil(p)[n - 1]);
      };
      function zera(){
        n = 0; cont.innerHTML = "palmas: <b>0</b>";
        var caixas = trilha.childNodes, k;
        for(k = 0; k < caixas.length; k++) caixas[k].className = "silbox";
      }
      ok.onclick = function(){
        if(ST.resp[id]) return;
        if(n === alvo){
          var caixas = trilha.childNodes, k;
          for(k = 0; k < caixas.length; k++) caixas[k].className = "silbox acesa";
          acertou(id, "certo2_" + p); b.className = "item feito";
        } else { errou(id, "dica2_" + p); zera(); }
      };
      var ouv = el("button", "bt cinza", "OUVIR EM SÍLABAS");
      ouv.onclick = function(){ sPasso(); falar("sil_" + p); };
      cx.appendChild(bt); cx.appendChild(cont); cx.appendChild(trilha);
      var lin = el("div", "ops"); lin.appendChild(ouv); lin.appendChild(ok);
      cx.appendChild(lin);
      if(ST.resp[id]){ b.className = "item feito"; cont.innerHTML = "palmas: <b>" + alvo + "</b>"; }
      b.appendChild(cx); b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 3 — O QUE VEM DEPOIS (sequência lógica) ============
   Pedido do Marcos, com todas as letras. Fiel ao formato da folha: a fileira
   com o último quadro vazio, e as figuras para escolher embaixo. */
function f3(d, pi){
  faixa(d, pi, NOMES[2]);
  d.appendChild(el("div", "enun", "Olhe a fila e descubra <b>o que vem depois</b>."));
  var L = ST.folha.p3;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r3_" + i, seq = [it.a, it.b, it.a, it.b], b = item(i + 1);
      var fila = el("div", "fila");
      seq.forEach(function(w){ fila.appendChild(el("div", "q", img(w))); });
      var vaga = el("div", "q vaga", ST.resp[id] ? img(it.a) : "?");
      vaga.setAttribute("data-qa", "vaga-" + id);
      fila.appendChild(vaga);
      b.appendChild(fila);
      b.appendChild(el("div", "ajuda", "Toque na figura certa <b>ou puxe</b> ela até o quadro vazio."));
      var erradas = ["casa", "mala", "gato", "roda", "vaca", "sino", "faca"].filter(function(x){ return x !== it.a && x !== it.b; });
      var ops = baralha([it.a, it.b, erradas[rnd(erradas.length)]]).map(function(w){
        return {v: w, rot: img(w), fala: "pal_" + w, aria: esc(w)};
      });
      opcoes(b, pi, id, ops, it.a, "fig", "certo3_" + it.a + "_" + it.b, "dica3", function(){
        vaga.className = "q vaga cheia"; vaga.innerHTML = img(it.a);
      }, vaga);
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ---------- RISCAR O CÍRCULO, como no papel (pedido do Marcos, set/2026) ----
   Palavras dele: *"na de circular, está sendo clicar; não seria legal fazer o
   círculo ao redor com o mouse também?"*. Ele tem razão: a folha manda CIRCULAR,
   e circular é um gesto — o dedo/mouse dá a volta. Tocar continua valendo (é o
   que serve no celular); o risco é a segunda porta.

   Como decide quem foi circulado: o traço é uma sequência de pontos; ao soltar,
   um desenho conta como circulado se o seu CENTRO ficou dentro do polígono
   fechado pelo traço (regra do número de cruzamentos). Não exige círculo bonito
   — rabisco de criança de 6 anos fecha assim mesmo.
   ⚠️ Traço curto (menos de 60 px) é descartado: senão um clique que escorrega
   dois pixels viraria "circulou tudo". */
function riscoDeCircular(grade, botoes, alterna){
  var cv = document.createElement("canvas");
  cv.className = "riscocv"; grade.appendChild(cv);
  var ctx = cv.getContext("2d"), pts = [], riscando = false;
  function tamanho(){
    var r = grade.getBoundingClientRect();
    if(!r.width) return;
    cv.width = r.width; cv.height = r.height;
    cv.style.width = r.width + "px"; cv.style.height = r.height + "px";
  }
  function pinta(){
    ctx.clearRect(0, 0, cv.width, cv.height);
    if(pts.length < 2) return;
    ctx.strokeStyle = "#e0562f"; ctx.lineWidth = 5;
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y);
    for(var k = 1; k < pts.length; k++) ctx.lineTo(pts[k].x, pts[k].y);
    ctx.stroke();
  }
  function ponto(ev){
    var r = cv.getBoundingClientRect();
    return {x: ev.clientX - r.left, y: ev.clientY - r.top};
  }
  grade.addEventListener("pointerdown", function(ev){
    if(ev.pointerType === "touch") return;      /* no dedo, tocar já resolve */
    tamanho(); riscando = true; pts = [ponto(ev)];
    cv.className = "riscocv ativo";
    try { grade.setPointerCapture(ev.pointerId); } catch(e){}
  });
  grade.addEventListener("pointermove", function(ev){
    if(!riscando) return;
    pts.push(ponto(ev)); pinta();
  });
  function fim(){
    if(!riscando) return;
    riscando = false; cv.className = "riscocv";
    var comp = 0, k;
    for(k = 1; k < pts.length; k++)
      comp += Math.abs(pts[k].x - pts[k-1].x) + Math.abs(pts[k].y - pts[k-1].y);
    if(comp > 60){
      var r0 = cv.getBoundingClientRect(), w;
      for(w in botoes){
        var rb = botoes[w].getBoundingClientRect();
        if(dentro(pts, rb.left - r0.left + rb.width / 2, rb.top - r0.top + rb.height / 2)) alterna(w);
      }
    }
    pts = []; ctx.clearRect(0, 0, cv.width, cv.height);
  }
  grade.addEventListener("pointerup", fim);
  grade.addEventListener("pointercancel", fim);
  grade.addEventListener("pointerleave", fim);
}
/* ponto dentro do rabisco: conta quantas vezes uma reta para a direita cruza o
   traço (fechando o último ponto no primeiro). Ímpar = está dentro. */
function dentro(pts, x, y){
  var n = pts.length, cruz = false, i, j;
  if(n < 3) return false;
  for(i = 0, j = n - 1; i < n; j = i++){
    var yi = pts[i].y, yj = pts[j].y, xi = pts[i].x, xj = pts[j].x;
    if(((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) cruz = !cruz;
  }
  return cruz;
}

/* ============ 4 — CIRCULE QUEM COMEÇA IGUAL (sílaba inicial) ============
   Da folha: *"circule os desenhos que se iniciam com a sílaba CA"* (d12/d02). */
function f4(d, pi){
  faixa(d, pi, NOMES[3]);
  d.appendChild(el("div", "enun", "Circule <b>todos</b> os desenhos que começam com a sílaba mostrada. " +
    "Toque no desenho <b>ou risque um círculo em volta dele</b>, como no papel."));
  var L = ST.folha.p4;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r4_" + i, marcadas = {}, b = item(i + 1);
      registra(id, pi, it.sim.length);
      b.appendChild(el("div", null, '<div style="text-align:center;margin:6px 0"><span class="chip">' + it.sil + '</span></div>'));
      var todas = baralha(it.sim.concat(it.nao)), grade = el("div", "grade"), botoes = {};
      todas.forEach(function(w){
        var e = el("button", "circ", img(w));
        e.setAttribute("data-qa", "circ-" + id + "-" + w);
        e.setAttribute("aria-label", esc(w));
        e.onclick = function(){
          if(ST.resp[id]) return;
          marcadas[w] = !marcadas[w];
          e.className = "circ" + (marcadas[w] ? " marcada" : "");
          sPasso(); falar("pal_" + w);
        };
        botoes[w] = e; grade.appendChild(e);
      });
      b.appendChild(grade);
      riscoDeCircular(grade, botoes, function(w){
        if(ST.resp[id]) return;
        marcadas[w] = !marcadas[w];
        botoes[w].className = "circ" + (marcadas[w] ? " marcada" : "");
        sPasso(); falar("pal_" + w);
      });
      var ok = el("button", "bt verde", "Conferir");
      ok.setAttribute("data-qa", "conferir-" + id);
      ok.onclick = function(){
        if(ST.resp[id]) return;
        var certo = true, w;
        for(w in botoes){ if(!!marcadas[w] !== (it.sim.indexOf(w) > -1)) certo = false; }
        if(certo){
          for(w in botoes) if(it.sim.indexOf(w) > -1) botoes[w].className = "circ certa";
          acertou(id, "certo4_" + it.sil); b.className = "item feito";
        } else {
          for(w in botoes) if(marcadas[w] && it.sim.indexOf(w) < 0) botoes[w].className = "circ errada";
          errou(id, "dica4_" + it.sil);
        }
      };
      if(ST.resp[id]){ b.className = "item feito"; it.sim.forEach(function(w){ botoes[w].className = "circ certa"; }); }
      var lin = el("div", "ops"); lin.appendChild(ok); b.appendChild(lin);
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 5 — PINTE A SÍLABA INICIAL ============
   Da folha: *"pinte a sílaba inicial do nome de cada desenho"* (d18). */
/* ---------- AS CANETINHAS (pedido do Marcos, set/2026) ----------
   Palavras dele: *"no pinte a sílaba coloque umas 3 ou quatro cores, para o
   estudante escolher qual ele quer pintar, serve tanto para clicar quanto
   pintar esfregando o ponteiro do mouse como se fosse uma canetinha"*.

   Por que isto é bom e não é enfeite: na folha de papel a criança ESCOLHE a
   cor do lápis, e essa escolha pequena é dela (autonomia — Deci & Ryan). E o
   gesto de pintar esfregando é o gesto real do exercício: "pinte", não
   "clique". Quem prefere tocar continua tocando — as duas portas, como sempre.
   A cor é só tinta: quem decide certo/errado continua sendo a sílaba. */
var LAPIS = [
  {n: "roxo",    c: "#7c3aed", claro: "#ede9fe"},
  {n: "laranja", c: "#ea580c", claro: "#ffedd5"},
  {n: "verde",   c: "#0f9d58", claro: "#dcfce7"},
  {n: "rosa",    c: "#db2777", claro: "#fce7f3"}
];
var LAPIS_ESCOLHIDO = 0;

function estojo(pai){
  var cx = el("div", "estojo");
  cx.appendChild(el("span", "rot", "Escolha a cor:"));
  LAPIS.forEach(function(L, k){
    var b = el("button", "lapis" + (k === LAPIS_ESCOLHIDO ? " esc" : ""));
    b.style.background = L.c;
    b.setAttribute("aria-label", "Canetinha " + L.n);
    b.setAttribute("data-qa", "lapis-" + L.n);
    b.onclick = function(){
      LAPIS_ESCOLHIDO = k; sPasso();
      var ir = cx.childNodes, j;
      for(j = 1; j < ir.length; j++) ir[j].className = "lapis" + (j - 1 === k ? " esc" : "");
    };
    cx.appendChild(b);
  });
  pai.appendChild(cx);
}

function f5(d, pi){
  faixa(d, pi, NOMES[4]);
  d.appendChild(el("div", "enun", "Pinte a sílaba com que a palavra <b>começa</b>. " +
    "Escolha a cor da canetinha e <b>toque ou esfregue</b> em cima da sílaba."));
  estojo(d);
  var L = ST.folha.p5;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r5_" + i, certa = sil(it.p)[0], b = item(i + 1);
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(it.p) +
        '<div class="pal">' + esc(it.p) + '</div></div>'));
      registra(id, pi, certa);
      var box = el("div", "ops"), feito = !!ST.resp[id];
      baralha(it.op).forEach(function(s){
        var e = el("button", "op pinta" + (feito && s === certa ? " certa" : ""), s);
        e.setAttribute("data-qa", "op-" + id + "-" + s);
        e.setAttribute("aria-label", "Sílaba " + s);
        function pinta(){
          if(ST.resp[id] || e._pintada) return;
          e._pintada = true;
          var L2 = LAPIS[LAPIS_ESCOLHIDO];
          e.style.background = L2.claro; e.style.borderColor = L2.c; e.style.color = L2.c;
          sPasso(); falar("sb_" + s);
          if(s === certa){
            setTimeout(function(){
              e.className = "op pinta certa"; e.style.background = ""; e.style.borderColor = ""; e.style.color = "";
              acertou(id, "certo5_" + it.p);
            }, 380);
          } else {
            errou(id, "dica5_" + it.p);
            setTimeout(function(){
              e._pintada = false;
              e.style.background = ""; e.style.borderColor = ""; e.style.color = "";
            }, 700);
          }
        }
        e.onclick = pinta;
        /* esfregar: o dedo/mouse APERTADO passando por cima já pinta */
        e.addEventListener("pointerenter", function(ev){ if(ev.buttons === 1) pinta(); });
        e.addEventListener("pointerdown", function(){ pinta(); });
        box.appendChild(e);
      });
      b.appendChild(box);
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 6 — LIGUE À SÍLABA FINAL ============
   Da folha: *"ligue cada figura à sua sílaba final"* (d08). É o nosso LIGAR. */
function f6(d, pi){
  faixa(d, pi, NOMES[5]);
  d.appendChild(el("div", "enun", "Ligue cada figura à sílaba com que ela <b>termina</b>."));
  var L = ST.folha.p6;
  for(var i = 0; i < L.length; i++){
    (function(grupo, i){
      var b = item(i + 1);
      montaLigar(b, pi, "g" + i, grupo.map(function(w, k){
        var s = sil(w); return {k: "k" + k, w: w, esq: img(w), dir: s[s.length - 1],
          fe: "pal_" + w, fd: "sb_" + s[s.length - 1], fc: "certo6_" + w, dica: "dica6_" + w};
      }), d);
      b.setAttribute("data-qa", "item-lig" + i); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 7 — MARQUE A SÍLABA DO MEIO ============
   Da folha: *"marque um X nas respostas certas: qual é a sílaba mediana"* (d09). */
function f7(d, pi){
  faixa(d, pi, NOMES[6]);
  d.appendChild(el("div", "enun", "Marque um <b>X</b> na sílaba que fica <b>no meio</b> da palavra."));
  var L = ST.folha.p7;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r7_" + i, s = sil(it.p), certa = s[1], b = item(i + 1);
      registra(id, pi, certa);
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(it.p) + '</div>'));
      var cx = el("div", "silbox");
      s.forEach(function(x, k){ cx.appendChild(el("div", "sq" + (k === 1 ? " vaga" : ""), k === 1 && !ST.resp[id] ? "?" : x)); });
      b.appendChild(cx);
      var lista = el("div", "marcax");
      baralha(it.op).forEach(function(o){
        var l = el("div", "lx" + (ST.resp[id] && o === certa ? " certa" : ""),
          '<span class="cx">' + (ST.resp[id] && o === certa ? "X" : "") + '</span><span>' + o + '</span>');
        l.setAttribute("role", "button"); l.setAttribute("tabindex", "0");
        l.setAttribute("data-qa", "x-" + id + "-" + o);
        l.setAttribute("aria-label", "Sílaba " + o);
        l.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("sb_" + o);
          if(o === certa){
            l.className = "lx certa"; l.querySelector(".cx").textContent = "X";
            cx.childNodes[1].className = "sq ok"; cx.childNodes[1].textContent = certa;
            setTimeout(function(){ acertou(id, "certo7_" + it.p); b.className = "item feito"; }, 240);
          } else {
            l.className = "lx erro"; setTimeout(function(){ l.className = "lx"; }, 500);
            errou(id, "dica7_" + it.p);
          }
        };
        l.onkeydown = function(ev){ if(ev.key === "Enter" || ev.key === " "){ ev.preventDefault(); l.onclick(); } };
        lista.appendChild(l);
      });
      b.appendChild(lista);
      if(ST.resp[id]) b.className = "item feito";
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 8 — COMPLETE A SÍLABA QUE FALTA ============
   Da folha: *"complete o nome das figuras com as sílabas faltosas e escreva"*
   (d01/d20/d12). Teclado de letras na tela E o teclado de verdade: a regra das
   DUAS PORTAS. No PC da escola tem teclado e a criança vai digitar. */
function f8(d, pi){
  faixa(d, pi, NOMES[7]);
  d.appendChild(el("div", "enun", "Falta um pedaço! Toque no quadradinho e <b>escreva</b> a sílaba."));
  var L = ST.folha.p8;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r8_" + i, s = sil(it.p), certa = s[it.falta], b = item(i + 1);
      registra(id, pi, certa);
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(it.p) + '</div>'));
      var cx = el("div", "silbox");
      s.forEach(function(x, k){
        if(k !== it.falta){ cx.appendChild(el("div", "sq", x)); return; }
        var q = el("div", "sq vaga" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? certa : "");
        q.id = id; q.setAttribute("role", "button"); q.setAttribute("tabindex", "0");
        q.setAttribute("data-qa", "vaga-" + id);
        q.setAttribute("aria-label", "Escreva a sílaba que falta em " + esc(it.p));
        q.onclick = function(){ if(ST.resp[id]) return; sPasso(); ativa(q, certa, id, "certo8_" + it.p, "dica8_" + it.p); };
        q.onkeydown = function(ev){ if(ev.key === "Enter" || ev.key === " "){ ev.preventDefault(); q.onclick(); } };
        cx.appendChild(q);
      });
      b.appendChild(cx);
      if(ST.resp[id]) b.className = "item feito";
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 9 — ORDENE E FORME A PALAVRA ============
   Da folha: *"ordene as sílabas e forme a palavra: CA-MA-CO"* (d16/d03). */
function f9(d, pi){
  faixa(d, pi, NOMES[8]);
  d.appendChild(el("div", "enun", "As sílabas embaralharam! Toque nelas <b>na ordem certa</b>, " +
    "ou <b>puxe cada uma</b> para o seu quadradinho."));
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    (function(p, i){
      var id = "r9_" + i, s = sil(p), posto = 0, b = item(i + 1);
      registra(id, pi, s.join(""));
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(p) + '</div>'));
      var vagas = el("div", "vagas"), caixas = [];
      s.forEach(function(x, k){
        var v = el("div", "vaga" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? x : "");
        v.setAttribute("data-qa", "vaga-" + id + "-" + k);
        caixas.push(v); vagas.appendChild(v);
      });
      b.appendChild(vagas);
      var tira = el("div", "tira");
      baralha(s.map(function(x, k){ return {x: x, k: k}; })).forEach(function(o){
        var c = el("button", "sil" + (ST.resp[id] ? " usada" : ""), o.x);
        c.setAttribute("data-qa", "sil-" + id + "-" + o.k);
        c.setAttribute("aria-label", "Sílaba " + o.x);
        function poe(){
          if(ST.resp[id]) return;
          sPasso(); falar("sb_" + o.x);
          if(o.k === posto){
            caixas[posto].className = "vaga cheia"; caixas[posto].textContent = o.x;
            c.className = "sil usada"; posto++;
            if(posto === s.length){ acertou(id, "certo9_" + p); b.className = "item feito"; }
          } else { c.className = "sil"; errou(id, "dica9_" + p); }
        }
        c.onclick = function(){ if(c._arrastou){ c._arrastou = false; return; } poe(); };
        /* ⭐ PUXAR TAMBÉM (pedido do Marcos, set/2026: *"na 9, de ordenar a
           palavra, seria legal o estudante poder arrastar também"*). Soltar em
           QUALQUER quadradinho vale — a peça vai para o lugar dela na ordem, e
           se a sílaba não era a da vez a resposta é a mesma de tocar: a dica.
           Assim a criança que arrasta e a que toca recebem exatamente o mesmo
           ensino. */
        puxavel(c, caixas, function(){ poe(); });
        tira.appendChild(c);
      });
      b.appendChild(tira);
      if(ST.resp[id]) b.className = "item feito";
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 10 — RECORTE E COLE ============
   Da folha: *"recorte as sílabas iniciais e cole de acordo com o nome das
   figuras"* (d11). É o nosso ARRASTAR — e, pela regra das duas portas, o
   TOQUE SIMPLES também resolve (no celular a criança não arrasta bem). */
function f10(d, pi){
  faixa(d, pi, NOMES[9]);
  d.appendChild(el("div", "enun", "Puxe cada sílaba para <b>debaixo da figura certa</b> — ou toque na sílaba e depois na figura."));
  var L = ST.folha.p10;
  for(var i = 0; i < L.length; i++){
    (function(grupo, i){
      var b = item(i + 1), pego = null;
      var cels = el("div", "colar"), alvos = {};
      grupo.forEach(function(w){
        var id = "r10_" + i + "_" + w, s0 = sil(w)[0];
        registra(id, pi, s0);
        var c = el("div", "cel", img(w));
        var a = el("div", "alvo" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? s0 : "");
        a.setAttribute("data-qa", "alvo-" + id);
        a.setAttribute("role", "button"); a.setAttribute("tabindex", "0");
        a.setAttribute("aria-label", "Cole aqui a sílaba de " + esc(w));
        a.onclick = function(){ if(pego) solta(w, pego); };
        a.onkeydown = function(ev){ if((ev.key === "Enter" || ev.key === " ") && pego){ ev.preventDefault(); solta(w, pego); } };
        alvos[w] = {el: a, sil: s0, id: id, w: w};
        c.appendChild(a); cels.appendChild(c);
      });
      b.appendChild(cels);
      var tira = el("div", "tira"), chips = {};
      baralha(grupo).forEach(function(w){
        var s0 = sil(w)[0], id = "r10_" + i + "_" + w;
        var c = el("button", "sil" + (ST.resp[id] ? " usada" : ""), s0);
        c.setAttribute("data-qa", "peca-" + i + "-" + s0);
        c.setAttribute("aria-label", "Sílaba " + s0);
        chips[s0] = c;
        c.addEventListener("pointerdown", function(ev){
          if(c.className.indexOf("usada") > -1) return;
          ev.preventDefault(); try{ c.setPointerCapture(ev.pointerId); }catch(x){}
          pego = s0; c.className = "sil arrastando"; sPasso(); falar("sb_" + s0);
        });
        c.addEventListener("pointermove", function(ev){
          if(pego !== s0) return;
          var w2, r;
          for(w2 in alvos){
            r = alvos[w2].el.getBoundingClientRect();
            alvos[w2].el.className = "alvo" + (ST.resp[alvos[w2].id] ? " cheia" : "") +
              (ev.clientX > r.left - 14 && ev.clientX < r.right + 14 && ev.clientY > r.top - 14 && ev.clientY < r.bottom + 14 ? " perto" : "");
          }
        });
        c.addEventListener("pointerup", function(ev){
          if(pego !== s0) return;
          var achou = null, w2, r;
          for(w2 in alvos){
            r = alvos[w2].el.getBoundingClientRect();
            if(ev.clientX > r.left - 14 && ev.clientX < r.right + 14 && ev.clientY > r.top - 14 && ev.clientY < r.bottom + 14) achou = w2;
            alvos[w2].el.className = "alvo" + (ST.resp[alvos[w2].id] ? " cheia" : "");
          }
          if(achou) solta(achou, s0);
          else c.className = "sil";              /* soltou no vazio: a peça volta e ela CONTINUA marcada */
        });
        tira.appendChild(c);
      });
      b.appendChild(tira);

      function solta(w, s0){
        var A = alvos[w];
        if(ST.resp[A.id]){ pego = null; if(chips[s0]) chips[s0].className = "sil"; return; }
        if(A.sil === s0){
          A.el.className = "alvo cheia"; A.el.textContent = s0;
          chips[s0].className = "sil usada"; pego = null;
          acertou(A.id, "certo10_" + w);
        } else {
          chips[s0].className = "sil"; pego = null;
          A.el.className = "alvo"; errou(A.id, "dica10_" + w);
        }
      }
      b.setAttribute("data-qa", "item-colar" + i); d.appendChild(b);
    })(L[i], i);
  }
}

/* ---------- ligar (folha 6) ---------- */
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
  /* ⭐ O TRAÇO (pedido do Marcos, set/2026: *"melhore o traço que liga para
     parecer mais profissional"*). Antes era um segmento reto de ponta a ponta.
     Agora é uma CURVA suave — sai na horizontal de cada caixa e vira no meio,
     como o cabo de um painel — com um halo branco por baixo (para o traço não
     sumir quando passa por cima de outra caixa) e um pontinho cheio em cada
     ponta, que é o que dá o acabamento de "ligado". */
  function linha(a, b2, cor){
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    var dx = Math.max(28, Math.abs(b2.x - a.x) * 0.45);
    var d = "M" + a.x + "," + a.y +
            " C" + (a.x + dx) + "," + a.y +
            " " + (b2.x - dx) + "," + b2.y +
            " " + b2.x + "," + b2.y;
    var halo = document.createElementNS("http://www.w3.org/2000/svg", "path");
    halo.setAttribute("d", d); halo.setAttribute("fill", "none");
    halo.setAttribute("stroke", "#ffffff"); halo.setAttribute("stroke-width", 11);
    halo.setAttribute("stroke-linecap", "round");
    var l = document.createElementNS("http://www.w3.org/2000/svg", "path");
    l.setAttribute("d", d); l.setAttribute("fill", "none");
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
    e.setAttribute("aria-label", esc(P.w));
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
    e.setAttribute("aria-label", "Sílaba " + P.dir);
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

/* ---------- teclado de letras (folha 8) ---------- */
function ativa(q, certa, id, fc, fd){
  if(ATIVA) fechaAtiva();
  ATIVA = {q: q, val: "", certa: certa, id: id, fc: fc, fd: fd};
  q.className = "sq vaga ativa";
  q.innerHTML = '<span class="v"></span><span class="cursor"></span>';
  document.getElementById("teclado").className = "aberto";
  document.getElementById("tkDica").textContent = "Escreva a sílaba que falta";
  falar("escreva");
}
function fechaAtiva(){
  if(!ATIVA) return;
  if(!ST.resp[ATIVA.id]){ ATIVA.q.className = "sq vaga"; ATIVA.q.textContent = ""; }
  ATIVA = null; document.getElementById("teclado").className = "";
}
function digita(ch){
  if(!ATIVA) return;
  sTecla();
  if(ch === "ap") ATIVA.val = ATIVA.val.slice(0, -1);
  else if(ch === "ok") return confereSil();
  else { if(ATIVA.val.length >= 4) return; ATIVA.val += ch; }
  var v = ATIVA.q.querySelector(".v"); if(v) v.textContent = ATIVA.val;
  if(ATIVA.val.length >= ATIVA.certa.length) setTimeout(confereSil, 380);
}
function confereSil(){
  if(!ATIVA || !ATIVA.val) return;
  var A = ATIVA;
  if(A.val === A.certa){
    A.q.className = "sq ok"; A.q.textContent = A.certa;
    ATIVA = null; document.getElementById("teclado").className = "";
    acertou(A.id, A.fc);
    var it = A.q.parentNode.parentNode; if(it) it.className = "item feito";
  } else {
    A.val = ""; var v = A.q.querySelector(".v"); if(v) v.textContent = "";
    errou(A.id, A.fd);
  }
}
(function(){
  var tk = document.getElementById("tk");
  var letras = "ABCDEFGHIJLMNOPQRSTUVXZÇÃ".split("");
  letras.forEach(function(L){
    var b = el("button", null, L);
    b.setAttribute("aria-label", "Letra " + L);
    b.onclick = function(){ digita(L); };
    tk.appendChild(b);
  });
  var ap = el("button", "ap", "apagar"); ap.setAttribute("aria-label", "Apagar");
  ap.onclick = function(){ digita("ap"); }; tk.appendChild(ap);
  var ok = el("button", "ok", "OK"); ok.setAttribute("aria-label", "Confirmar");
  ok.onclick = function(){ digita("ok"); }; tk.appendChild(ok);
})();
document.addEventListener("keydown", function(ev){
  if(!ATIVA) return;
  if(document.activeElement && document.activeElement.id === "nomeIn") return;
  var k = (ev.key || "").toUpperCase();
  if(k.length === 1 && "ABCDEFGHIJLMNOPQRSTUVXZÇÃ".indexOf(k) > -1){ ev.preventDefault(); digita(k); }
  else if(ev.key === "Backspace"){ ev.preventDefault(); digita("ap"); }
  else if(ev.key === "Enter"){ ev.preventDefault(); digita("ok"); }
  else if(ev.key === "Escape"){ fechaAtiva(); }
});

/* ---------- folha pronta e navegação ---------- */
function idsDaPagina(pi){
  var ids = [], i, k, F = ST.folha;
  if(pi === 1) for(i = 0; i < F.p1.length; i++) ids.push("r1_" + i);
  if(pi === 2) for(i = 0; i < F.p2.length; i++) ids.push("r2_" + i);
  if(pi === 3) for(i = 0; i < F.p3.length; i++) ids.push("r3_" + i);
  if(pi === 4) for(i = 0; i < F.p4.length; i++) ids.push("r4_" + i);
  if(pi === 5) for(i = 0; i < F.p5.length; i++) ids.push("r5_" + i);
  if(pi === 6) for(i = 0; i < F.p6.length; i++) for(k = 0; k < F.p6[i].length; k++) ids.push("l6g" + i + "_k" + k);
  if(pi === 7) for(i = 0; i < F.p7.length; i++) ids.push("r7_" + i);
  if(pi === 8) for(i = 0; i < F.p8.length; i++) ids.push("r8_" + i);
  if(pi === 9) for(i = 0; i < F.p9.length; i++) ids.push("r9_" + i);
  if(pi === 10) for(i = 0; i < F.p10.length; i++) for(k = 0; k < F.p10[i].length; k++) ids.push("r10_" + i + "_" + F.p10[i][k]);
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
/* ⚠️ O nome NÃO se repete na capa (pedido do Marcos, set/2026: *"o nome ao
   digitar não precisa aparecer lá em cima na capa"*). Ele já aparece dentro do
   campo onde a criança digita; escrever de novo lá em cima era eco, e ainda
   empurrava a capa para baixo. Aqui só se mantém o campo em dia com o estado
   (importa ao retomar de onde parou). */
function espelhaNome(t){
  var i = document.getElementById("nomeIn"); if(i && i.value !== t) i.value = t;
}
function vaiPara(pi){
  calar(); fechaAtiva();
  document.getElementById("barraCapa").className = pi === 0 ? "aberta" : "";
  if(pi === 0) espelhaNome(ST.nome || "");
  document.getElementById("fim").style.display = "none";
  document.getElementById("retomar").style.display = "none";
  document.getElementById("nav").style.display = pi === 0 ? "none" : "flex";
  for(var i = 0; i < PAGEL.length; i++) PAGEL[i].className = PAGEL[i].className.replace(" viva", "");
  ST.pag = pi; salvar();
  var d = PAGEL[pi]; d.className += " viva";
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
function fim(){
  calar();
  for(var i = 0; i < PAGEL.length; i++) PAGEL[i].className = PAGEL[i].className.replace(" viva", "");
  document.getElementById("nav").style.display = "none";
  var f = document.getElementById("fim"); f.style.display = "block";
  var tot = 0, prim = 0, pi;
  for(pi = 1; pi <= 10; pi++){
    var ids = idsDaPagina(pi);
    tot += ids.length;
    for(var j = 0; j < ids.length; j++){ var t = ST.tent[ids[j]]; if(t && t.erros === 0 && t.ok) prim++; }
  }
  var pc = tot ? prim / tot : 0;
  var cheias = pc >= .85 ? 3 : pc >= .6 ? 2 : 1, est = "", ke;
  for(ke = 0; ke < 3; ke++)
    est += '<img src="img/al_estrela' + (ke < cheias ? "" : "_off") + '.png?v=4" alt="" draggable="false">';
  document.getElementById("estrelas").innerHTML = est;
  document.getElementById("estrelas").setAttribute("aria-label", cheias + " de 3 estrelas");
  var bar = document.getElementById("barras"); bar.innerHTML = "";
  for(pi = 1; pi <= 10; pi++){
    (function(pi){
      var ids = idsDaPagina(pi), t = ids.length, p = 0, j;
      for(j = 0; j < ids.length; j++){ var tt = ST.tent[ids[j]]; if(tt && tt.erros === 0 && tt.ok) p++; }
      var b = el("div", "barra", "<span>" + NOMES[pi - 1] + "</span><div class='tr'><i></i></div><b>" + p + "/" + t + "</b>");
      bar.appendChild(b);
      setTimeout(function(){ b.querySelector("i").style.width = (t ? p / t * 100 : 0) + "%"; }, 400);
    })(pi);
  }
  document.getElementById("resumo").textContent =
    (ST.nome || "Você") + ", você acertou de primeira " + prim + " de " + tot + " itens.";
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
/* O QUE CADA FOLHA MEDE — é isto que vira a frase do "dominou".
   ⚠️ O relatório é do PROFESSOR, não da criança: aqui pode haver porcentagem e
   o nome técnico da habilidade. Na tela da criança, nunca (§FIM-DE-ATIVIDADE). */
var HABILIDADE = [
  "reconhecer a letra que falta na palavra",
  "contar as sílabas da palavra batendo palma",
  "descobrir a ordem que se repete numa sequência",
  "identificar a sílaba inicial",
  "marcar a sílaba com que a palavra começa",
  "identificar a sílaba final",
  "identificar a sílaba do meio",
  "escrever a sílaba que falta",
  "ordenar as sílabas e formar a palavra",
  "juntar a sílaba inicial à figura certa"
];
function abreRelatorio(){
  var r = document.getElementById("relatorio");
  var linhas = "", fracas = [], dominou = [], pi, geralAcertos = 0, geralTotal = 0;
  for(pi = 1; pi <= 10; pi++){
    var ids = idsDaPagina(pi), t = ids.length, p = 0, ruins = 0, feitos = 0, j;
    for(j = 0; j < ids.length; j++){
      var tt = ST.tent[ids[j]];
      if(tt && tt.ok) feitos++;
      if(tt && tt.erros === 0 && tt.ok) p++;
      if(tt && tt.erros >= 2) ruins++;
    }
    geralAcertos += p; geralTotal += t;
    /* ⚠️ AS DUAS LISTAS SÃO COMPLEMENTARES — 75% é a única linha que decide.
       Na primeira versão a folha entrava em "Retomar" se tivesse UM item com
       duas tentativas, e aí a mesma folha aparecia em "Já domina" e em
       "Retomar" ao mesmo tempo. Para o professor isso não é informação: é
       ruído. Quem precisou de dica já está na coluna da tabela. */
    var pcf = t ? Math.round(100 * p / t) : 0;
    if(pcf >= 75) dominou.push(HABILIDADE[pi - 1]);
    else fracas.push(NOMES[pi - 1] + " (" + pcf + "%)");
    linhas += "<tr><td>" + pi + ". " + NOMES[pi - 1] + "</td><td>" + p + "/" + t +
      "</td><td><b>" + pcf + "%</b></td><td>" + ruins + "</td></tr>";
  }
  var pc = geralTotal ? Math.round(100 * geralAcertos / geralTotal) : 0;
  var conceito = pc >= 85 ? "Dominou" : pc >= 60 ? "Está construindo" : "Precisa retomar";
  var h = "<b>Relatório do professor</b> &mdash; " + esch(ST.nome || "(sem nome)") + " &middot; " +
    Math.round((Date.now() - (ST.inicio || Date.now())) / 60000) + " min" +
    "<div class='notao'><span class='nn'>" + pc + "%</span>" +
    "<span class='nl'>" + geralAcertos + " de " + geralTotal + " acertos de primeira<br><b>" +
    conceito + "</b></span></div>" +
    "<table><tr><th>Folha</th><th>De primeira</th><th>%</th><th>Precisou de dica</th></tr>" +
    linhas + "</table>";
  h += "<p style='margin:10px 0 0'><b>Já domina:</b> " +
    (dominou.length ? dominou.join("; ") + "." : "ainda nenhuma habilidade com 75% ou mais.") + "</p>";
  h += "<p style='margin:6px 0 0'><b>Retomar:</b> " +
    (fracas.length ? fracas.join(", ") + "." : "nada — foi bem nas dez folhas.") + "</p>";
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
    for(var k = 1; k <= 10; k++) mk(k + ". " + NOMES[k - 1], k);
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
    monta();
    document.getElementById("retomar").style.display = "block";
    document.getElementById("retTxt").textContent =
      (ST.nome ? ST.nome + ", você" : "Você") + " parou na folha " + (ST.pag || 1) + ": " + NOMES[(ST.pag || 1) - 1] + ".";
    document.getElementById("nav").style.display = "none";
  } else {
    ST.folha = novaFolha(); monta(); vaiPara(0);
  }
})();
