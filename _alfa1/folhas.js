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

/* ---------- capa ---------- */
function f0(d){
  var c = el("div", "capa");
  c.innerHTML = '<h1>A Fábrica de Palavras</h1><div class="sub">Alfabetização · 1º ano · 10 folhas</div>' +
    '<div class="cena">' + img("bola") + img("gato") + img("casa") + img("sapo") + '</div>' +
    '<div class="nomef vazio" id="nomef">escreva o seu nome ali embaixo</div>';
  d.appendChild(c);
}

/* ---------- fileira de opções (usada em várias folhas) ---------- */
function opcoes(pai, pi, id, lista, certa, cls, falaCerto, falaDica){
  registra(id, pi, certa);
  var box = el("div", "ops"), feito = !!ST.resp[id];
  lista.forEach(function(o){
    var b = el("button", "op" + (cls ? " " + cls : "") + (feito && o.v === certa ? " certa" : ""), o.rot);
    b.setAttribute("data-qa", "op-" + id + "-" + o.v);
    b.setAttribute("aria-label", o.aria || o.v);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); if(o.fala) falar(o.fala);
      if(o.v === certa){
        b.className = "op" + (cls ? " " + cls : "") + " certa";
        setTimeout(function(){ acertou(id, falaCerto); }, 240);
      } else {
        b.className = "op" + (cls ? " " + cls : "") + " erro";
        setTimeout(function(){ b.className = "op" + (cls ? " " + cls : ""); }, 500);
        errou(id, falaDica);
      }
    };
    box.appendChild(b);
  });
  pai.appendChild(box);
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
      var lin = el("div", "escondida");
      for(var k = 0; k < w.length; k++){
        if(k === it.pos) lin.appendChild(el("div", "buraco" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? certa : "?"));
        else lin.appendChild(el("span", "lt", w.charAt(k)));
      }
      b.appendChild(lin);
      var outras = "ABCDEFGHIJLMNOPRSTUVZ".split("").filter(function(x){ return x !== certa; });
      var ops = baralha([certa, outras[rnd(outras.length)], outras[rnd(outras.length)]]).map(function(x){
        return {v: x, rot: x, fala: "letra_" + x, aria: "Letra " + x};
      });
      opcoes(b, pi, id, ops, certa, null, "certo1_" + it.p, "dica1_" + it.p);
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
  d.appendChild(el("div", "enun", "Fale a palavra batendo palma em cada pedaço. Depois toque em <b>Pronto</b>."));
  var L = ST.folha.p2;
  for(var i = 0; i < L.length; i++){
    (function(p, i){
      var id = "r2_" + i, alvo = sil(p).length, n = 0;
      registra(id, pi, alvo);
      var b = item(i + 1), cx = el("div", "bater");
      cx.appendChild(el("div", null, img(p)));
      cx.appendChild(el("div", "pal", esc(p)));
      var cont = el("div", "contab", "palmas: <b>0</b>");
      var bt = el("button", "palma", "👏 BATER");
      bt.setAttribute("data-qa", "bater-" + id);
      var ok = el("button", "bt verde", "Pronto");
      ok.setAttribute("data-qa", "pronto-" + id);
      bt.onclick = function(){ if(ST.resp[id]) return; n++; sPalma(); cont.innerHTML = "palmas: <b>" + n + "</b>"; };
      ok.onclick = function(){
        if(ST.resp[id]) return;
        if(n === alvo){ acertou(id, "certo2_" + p); b.className = "item feito"; }
        else { errou(id, "dica2_" + p); n = 0; cont.innerHTML = "palmas: <b>0</b>"; }
      };
      var ouv = el("button", "bt cinza", "🔊 ouvir em pedaços");
      ouv.onclick = function(){ sPasso(); falar("sil_" + p); };
      cx.appendChild(bt); cx.appendChild(cont);
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
      fila.appendChild(el("div", "q vaga", ST.resp[id] ? img(it.a) : "?"));
      b.appendChild(fila);
      var erradas = ["casa", "mala", "gato", "roda", "vaca", "sino", "faca"].filter(function(x){ return x !== it.a && x !== it.b; });
      var ops = baralha([it.a, it.b, erradas[rnd(erradas.length)]]).map(function(w){
        return {v: w, rot: img(w), fala: "pal_" + w, aria: esc(w)};
      });
      opcoes(b, pi, id, ops, it.a, "fig", "certo3_" + it.a + "_" + it.b, "dica3");
      b.setAttribute("data-qa", "item-" + id); d.appendChild(b);
    })(L[i], i);
  }
}

/* ============ 4 — CIRCULE QUEM COMEÇA IGUAL (sílaba inicial) ============
   Da folha: *"circule os desenhos que se iniciam com a sílaba CA"* (d12/d02). */
function f4(d, pi){
  faixa(d, pi, NOMES[3]);
  d.appendChild(el("div", "enun", "Circule <b>todos</b> os desenhos que começam com a sílaba mostrada."));
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
function f5(d, pi){
  faixa(d, pi, NOMES[4]);
  d.appendChild(el("div", "enun", "Pinte a sílaba com que a palavra <b>começa</b>."));
  var L = ST.folha.p5;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "r5_" + i, certa = sil(it.p)[0], b = item(i + 1);
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(it.p) +
        '<div class="pal">' + esc(it.p) + '</div></div>'));
      var ops = baralha(it.op).map(function(s){ return {v: s, rot: s, fala: "sb_" + s, aria: "Sílaba " + s}; });
      opcoes(b, pi, id, ops, certa, "pinta", "certo5_" + it.p, "dica5_" + it.p);
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
          '<span class="cx">' + (ST.resp[id] && o === certa ? "✕" : "") + '</span><span>' + o + '</span>');
        l.setAttribute("role", "button"); l.setAttribute("tabindex", "0");
        l.setAttribute("data-qa", "x-" + id + "-" + o);
        l.setAttribute("aria-label", "Sílaba " + o);
        l.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("sb_" + o);
          if(o === certa){
            l.className = "lx certa"; l.querySelector(".cx").textContent = "✕";
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
  d.appendChild(el("div", "enun", "As sílabas embaralharam! Toque nelas <b>na ordem certa</b>."));
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    (function(p, i){
      var id = "r9_" + i, s = sil(p), posto = 0, b = item(i + 1);
      registra(id, pi, s.join(""));
      b.appendChild(el("div", null, '<div style="text-align:center">' + img(p) + '</div>'));
      var vagas = el("div", "vagas"), caixas = [];
      s.forEach(function(x, k){
        var v = el("div", "vaga" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? x : "");
        caixas.push(v); vagas.appendChild(v);
      });
      b.appendChild(vagas);
      var tira = el("div", "tira");
      baralha(s.map(function(x, k){ return {x: x, k: k}; })).forEach(function(o){
        var c = el("button", "sil" + (ST.resp[id] ? " usada" : ""), o.x);
        c.setAttribute("data-qa", "sil-" + id + "-" + o.k);
        c.setAttribute("aria-label", "Sílaba " + o.x);
        c.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("sb_" + o.x);
          if(o.k === posto){
            caixas[posto].className = "vaga cheia"; caixas[posto].textContent = o.x;
            c.className = "sil usada"; posto++;
            if(posto === s.length){ acertou(id, "certo9_" + p); b.className = "item feito"; }
          } else { c.className = "sil"; errou(id, "dica9_" + p); }
        };
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
  function linha(a, b2, cor){
    var l = document.createElementNS("http://www.w3.org/2000/svg", "line");
    l.setAttribute("x1", a.x); l.setAttribute("y1", a.y); l.setAttribute("x2", b2.x); l.setAttribute("y2", b2.y);
    l.setAttribute("stroke", cor); l.setAttribute("stroke-width", 7); l.setAttribute("stroke-linecap", "round");
    svg.appendChild(l); return l;
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
  var ap = el("button", "ap", "⌫ apagar"); ap.setAttribute("aria-label", "Apagar");
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
function espelhaNome(t){
  var n = document.getElementById("nomef");
  if(n){ n.textContent = t || "escreva o seu nome ali embaixo"; n.className = t ? "nomef" : "nomef vazio"; }
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
  prox.textContent = pi === total - 1 ? (pend ? "Faltam " + pend : "Ver o resultado ★") : (pend ? "Faltam " + pend + " ▶" : "Próxima ▶");
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
  document.getElementById("estrelas").textContent = pc >= .85 ? "★★★" : pc >= .6 ? "★★☆" : "★☆☆";
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
function abreRelatorio(){
  var r = document.getElementById("relatorio");
  var h = "<b>Relatório do professor</b> — " + (ST.nome || "(sem nome)") + " · " +
    Math.round((Date.now() - (ST.inicio || Date.now())) / 60000) + " min" +
    "<table><tr><th>Folha</th><th>De primeira</th><th>Precisou de dica</th></tr>";
  var fracas = [], pi;
  for(pi = 1; pi <= 10; pi++){
    var ids = idsDaPagina(pi), t = ids.length, p = 0, ruins = 0, j;
    for(j = 0; j < ids.length; j++){
      var tt = ST.tent[ids[j]];
      if(tt && tt.erros === 0) p++;
      if(tt && tt.erros >= 2) ruins++;
    }
    if(ruins) fracas.push(NOMES[pi - 1]);
    h += "<tr><td>" + pi + ". " + NOMES[pi - 1] + "</td><td>" + p + "/" + t + "</td><td>" + ruins + "</td></tr>";
  }
  h += "</table><p style='margin:10px 0 0'><b>Parecer:</b> " +
    (fracas.length === 0 ? "Dominou o conteúdo das dez folhas." :
     fracas.length <= 2 ? "Está construindo. Retomar: " + fracas.join(", ") + "." :
     "Precisa retomar com apoio: " + fracas.join(", ") + ".") + "</p>";
  r.innerHTML = h; r.style.display = "block"; sPasso();
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
