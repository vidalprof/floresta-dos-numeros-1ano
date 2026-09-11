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
/* ---------- O ALTO-FALANTE (pedido do Marcos, set/2026) ----------
   Palavras dele: *"os enunciados podem ter o botão de som para a criança clicar
   e ouvir"* e *"assim como as palavras"*.

   É regra da casa e tem motivo: no 1º ano metade da turma ainda soletra. Tudo o
   que a criança PRECISA LER tem que poder ser OUVIDO, senão ela responde pelo
   desenho e a folha vira loteria.

   ⚠️ O desenho do alto-falante é CSS puro — caixinha + triângulo + duas ondas
   feitas com borda arredondada. Nada de emoji (vira quadradinho nos PCs da
   escola) e nada de SVG (ordem dele). */
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
function palavraComSom(w){
  var cx = el("div", "palin");
  cx.appendChild(el("span", "pal", esc(w)));
  cx.appendChild(botaoSom("Ouvir a palavra " + esc(w), function(){ falar("pal_" + w); }));
  return cx;
}
function item(n){ return el("div", "item", n ? '<span class="n">' + n + '.</span>' : ""); }
/* fecha o item e o prega na folha — o padrão que o `_alfa1` repetia à mão em
   cada uma das onze folhas (marca o `feito`, o `data-qa` do jogador e anexa) */
function fechaItem(d, box, id){
  if(ST.resp[id]) box.className = "item feito";
  box.setAttribute("data-qa", "item-" + id);
  d.appendChild(box);
}

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

   ⚠️ RESTO DE CLONE, E ELE QUASE PASSOU: a capa herdada da Fábrica de Palavras
   trazia `img("sapo")` — uma figura que existe LÁ e não existe aqui. O app abria
   com um quadradinho vazio e um 404 no console, e nenhum portão de texto via
   isso. Foi o navegador que pegou. Regra: capa clonada = trocar a CENA, sempre.

   A ideia agora vem do nome: um BANDO — as palavras andam em dupla, e é isso
   que a criança vai aprender a ouvir. Então a cena da capa são PARES QUE RIMAM,
   lado a lado, com o sinal de igual entre eles. O movimento conta a atividade:
   cada letra entra depois da outra, como num desfile. */
function f0(d){
  var c = el("div", "capa"), nome = "A FAMÍLIA DAS PALAVRAS", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  /* ⭐ A CENA CONTA A ATIVIDADE: quatro palavras que começam com o MESMO
     pedacinho entram uma depois da outra, e o começo delas acende junto — que
     é exatamente o que a criança vai aprender a ouvir.
     ⚠️ RESTO DE CLONE QUE QUASE PASSOU: esta capa veio do Bate-Palma e dizia
     "BOR BO LE TA". O app abria bonito e nenhum portão de texto via. Capa
     clonada = trocar o NOME e a CENA, sempre. */
  var cena = "";
  [["BO", "LA"], ["BO", "NECA"], ["BO", "TA"], ["BO", "LO"]].forEach(function(par, i){
    cena += '<span class="palcapa p' + i + '"><b>' + par[0] + "</b>" + par[1] + "</span>";
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Alfabetização &middot; 1º ano &middot; dez folhas do começo das palavras</div>' +
    '<div class="esteira">' +
      '<div class="cena cenaped">' + cena + "</div>" +
      '<div class="cinta"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>' +
    "</div>" +
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

/* ============ 1 — A FILA DO ALFABETO (sequência alfabética) ============
   Da folha impressa: *"complete a sequência do alfabeto"* / *"que letra vem
   depois?"* — está em quase toda folha de 1º ano.

   ⚠️ POR QUE ELA É A FOLHA 1 (parecer pedagógico, set/2026): o currículo de
   Blumenau abre o 1º ano com *"nomear as letras do alfabeto e ordená-las"*, e a
   atividade não tinha nenhuma folha disso — o Marcos tinha pedido no encargo
   ("sequência alfabética") e escapou. Ordenar letra é o degrau anterior a tudo
   o que vem depois; por isso ela abre o caderno.

   O ANDAIME: mostra-se um pedacinho da fila (três letras) com um buraco no
   meio, nunca o alfabeto inteiro — carga cognitiva de uma ideia por vez
   (Sweller). A criança escolhe entre três letras VIZINHAS na fila, que é o que
   força olhar a ordem em vez de reconhecer a forma. *//* os pedacinhos que servem de DISTRATOR, declarados um a um.
   ⚠️ Todos são sílaba de VERDADE, de outra palavra deste caderno. A folha
   D01 da colheita foi recusada por oferecer KO/KA/KU, que não existem na
   escrita do português: distrator inventado ensina grafia errada. */
var DISTRA = {"laranja": ["LO", "LU"], "lata": ["LE", "LU"], "leao": ["LA", "LI"], "limao": ["LE", "LO"], "lobo": ["LA", "LU"], "luneta": ["LA", "LE"], "lupa": ["LO", "LI"], "maca": ["MI", "MO"], "macaco": ["ME", "MI"], "mala": ["ME", "MO"], "mapa": ["ME", "MO"], "menina": ["MA", "MI"], "menino": ["MI", "MO"], "minhoca": ["ME", "MO"], "mola": ["MA", "MI"]};

/* ============================================================
   A FAMÍLIA DAS PALAVRAS — as dez folhas

   ⭐ Degrau 3 da sequência de alfabetização (`_sequencias/SD-MONTADA-DE-FOLHAS-SOLTAS.md`).
   Cada folha veio de uma FOLHA REAL de professor — as 24 em `_sequencias/folhas_d3/`
   — e é fiel ao comando impresso. O crivo está em `_sequencias/POTE-INICIAL.md`.

   ⚠️ SEIS DAS 24 FOLHAS COLHIDAS PEDEM A **LETRA** INICIAL, NÃO A SÍLABA
   (D04, D08, D13, D17, D22, D23: "circule a letra inicial", "pinte as figuras
   que começam com A"). Parece o mesmo exercício e é outro degrau: a LETRA é o
   degrau 4 (fonema) e o degrau 0 (alfabeto); a SÍLABA é este. Trocar um pelo
   outro é o jeito mais rápido de fazer uma criança que ainda não isola fonema
   parecer que não sabe nada.

   ⚠️ E UMA FOLHA FOI RECUSADA POR ENSINAR ERRADO: a D01 oferece como opção
   sílabas que NÃO EXISTEM na escrita da palavra (KO, KA, KU para CORUJA e
   MACACO). Distrator tem que ser sílaba de verdade — senão a criança aprende
   que "ko" é um jeito possível de escrever.

   ⚠️ A ESCADA É DE DIFICULDADE:
     ouvir o começo (aula) → dizer qual é → achar quem começa igual COM o alvo
     dado → ligar → achar o par SEM alvo dado → completar → o intruso →
     classificar → escrever → o mural.
   ============================================================ */

/* a figura com o nome e o alto-falante — a peça que se repete.
   ⚠️ ALTO-FALANTE EM TODA PALAVRA: este degrau é de SOM. Sem ouvir, a criança
   compara o desenho da palavra em vez do começo dela. */
function figComSom(w, cls){
  var c = el("div", "figsil" + (cls ? " " + cls : ""));
  c.innerHTML = img(w, "figgrande");
  var lin = el("div", "chamlin");
  lin.appendChild(el("b", "", esc(w)));
  lin.appendChild(botaoSom("Ouvir " + esc(w), function(){ falar("pal_" + w); }));
  c.appendChild(lin);
  return c;
}
function ini(w){ return sil(w)[0]; }

/* 1 — A RODA DO L (a folha que ENSINA, e a única mecânica nova do caderno)
   ============================================================
   ⭐ O QUE ELA ENSINA, e por que uma roda e não uma lista:
   numa lista (LA, LE, LI, LO, LU) a criança lê cinco coisas soltas. Na roda ela
   VÊ que é sempre o MESMO L, e que o que muda é a vogal que entra — o L fica
   parado no meio e as cinco vogais giram em volta dele. É a ideia geradora: com
   uma consoante e cinco vogais ela fabrica cinco sílabas, e com elas palavras
   que nunca viu. Sair da soletração é isso.

   ⚠️ PRIMEIRO A MÃO, DEPOIS A PERGUNTA (regra da casa, vinda da pesquisa).
   A roda começa LIVRE: a criança toca em qualquer vogal quantas vezes quiser,
   ouve a sílaba montada e vê a palavra aparecer. Só quando ela já brincou é que
   vêm os cinco pedidos ("toque na vogal que faz LU"). Perguntar antes de deixar
   mexer transforma descoberta em prova.

   ⚠️ A SÍLABA É RECORTADA DA PALAVRA, nunca sintetizada solta (`sb1_LA` sai de
   dentro de LATA falada). Voz não lê som, lê palavra: pedir "la" ao sintetizador
   devolve "éle-á". Lição paga em 10/set/2026.
   ============================================================ */
function f1(d, pi){
  faixa(d, pi, NOMES[0]);
  enunciado(d, pi, "Toque nas <b>vogais</b> e ouça. O <b>L</b> fica parado; a vogal é que muda.", "p1enun");

  var L = ST.folha.p1, R = RODAS.L;

  /* ---- a roda, livre ---- */
  var roda = el("div", "roda");
  var meio = el("div", "rmeio", "L");
  meio.setAttribute("aria-hidden", "true");
  var mostra = el("div", "rmostra");
  var msil = el("b", "rsil", "L_");
  var mfig = el("div", "rfig", "");
  mostra.appendChild(msil); mostra.appendChild(mfig);

  /* as cinco vogais em volta: ângulo fixo, começando no alto e girando no
     sentido do relógio — a mesma ordem A E I O U que ela já viu no degrau 0. */
  R.s.forEach(function(s, k){
    var voc = s.charAt(1), w = R.w[k];
    var ang = -90 + k * (360 / R.s.length), rad = ang * Math.PI / 180;
    var b = el("button", "rvog", voc);
    b.style.left = (50 + 37 * Math.cos(rad)) + "%";
    b.style.top  = (50 + 37 * Math.sin(rad)) + "%";
    b.setAttribute("data-qa", "vogal-" + voc);
    b.setAttribute("aria-label", "vogal " + voc + ", faz " + s);
    b.onclick = function(){
      sPasso();
      var els = anel.getElementsByClassName("rvog"), i;
      for(i = 0; i < els.length; i++) els[i].className = "rvog";
      b.className = "rvog acesa";
      msil.innerHTML = esc(s);
      mfig.innerHTML = img(w, "figgrande") + '<span class="rnome">' + esc(w) + "</span>";
      falar("sb1_" + s);
      /* a palavra vem logo depois da sílaba: é ela que dá sentido ao pedaço */
      setTimeout(function(){ falar("pal_" + w); }, 900);
    };
    roda.appendChild(b);
  });
  roda.appendChild(meio);
  var cx = el("div", "rodacx");
  cx.appendChild(roda); cx.appendChild(mostra);
  d.appendChild(cx);

  /* ---- os pedidos ----
     ⚠️⚠️ O PEDIDO NÃO PODE TRAZER A RESPOSTA ESCRITA. Na primeira versão eu
        escrevia "Toque na vogal que faz **LA**" e punha A, E, I, O, U embaixo:
        a criança lia a segunda letra do enunciado e tocava nela. Media zero —
        e pior, ensinava a resolver por cópia. Vi isso no print, não num portão.
     ⚠️ Agora o pedido chega por DOIS caminhos que nunca mostram a letra:
        · pelo OUVIDO (só o alto-falante: ouça o pedacinho e ache a vogal);
        · pela FIGURA (que vogal começa LUPA?).
        Os dois se alternam, o que também tira a sensação de "a mesma tela cinco
        vezes" — a queixa que as crianças fazem ao Marcos. */
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n1_" + i, box = item(i + 1), s = ini(w), voc = s.charAt(1);
      var porFigura = (i % 2 === 1);
      var lin = el("div", "chamlin");
      if(porFigura){
        /* ⚠️ AQUI A FIGURA VAI SEM O NOME ESCRITO, e é a única folha do caderno
           em que isso acontece. Nas outras o nome ajuda; aqui ele ENTREGA: as
           opções são vogais soltas, e a segunda letra de LEÃO é a resposta. Com
           só a figura e o alto-falante, a criança tem de dizer a palavra por
           dentro e ouvir o comecinho — que é o que a folha mede. */
        var fc = el("div", "figsil");
        fc.innerHTML = img(w, "figgrande");
        var fl = el("div", "chamlin");
        fl.appendChild(botaoSom("Ouvir a palavra", function(){ falar("pal_" + w); }));
        fc.appendChild(fl);
        box.appendChild(fc);
        lin.appendChild(el("span", "", "Ouça a palavra. Com que vogal ela começa?"));
      } else {
        lin.appendChild(el("span", "", "Ouça o pedacinho e toque na vogal dele."));
        lin.appendChild(botaoSom("Ouvir o pedacinho", function(){ falar("sb1_" + s); }));
      }
      box.appendChild(lin);
      var ops = R.s.map(function(x){
        return {v: x.charAt(1), rot: '<span class="ltop">' + x.charAt(1) + "</span>",
                aria: "vogal " + x.charAt(1), fala: "sb1_" + x};
      });
      opcoes(box, pi, id, ops, voc, "figbt", "certo1_" + w, "volte1_" + w, function(){
        /* ao acertar, a roda do alto mostra o que ela acabou de montar */
        msil.innerHTML = esc(s);
        mfig.innerHTML = img(w, "figgrande") + '<span class="rnome">' + esc(w) + "</span>";
      });
      fechaItem(d, box, id);
    })(L[i], i);
  }

  /* ⚠️ o pedido "por ouvido" toca a sílaba assim que a folha abre a primeira
     vez; sem isso a criança fica olhando um alto-falante sem saber que tem de
     apertar (medido com crianças no degrau 4). */
  aoAbrir(d, function(){ if(!ST.resp["n1_0"]) setTimeout(function(){ falar("sb1_" + ini(L[0])); }, 1200); });
}

/* 2 — QUAL É O COMEÇO? (das folhas D07 e D10)
   O mesmo ouvido da folha 1, agora ESCOLHENDO — e os distratores são sílabas
   de verdade, tiradas de outras palavras do caderno (ver a recusa da D01). */
function f2(d, pi){
  faixa(d, pi, NOMES[1]);
  enunciado(d, pi, "Ouça a palavra. Com que <b>pedacinho</b> ela começa?", "p2enun");
  var L = ST.folha.p2;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n2_" + i, box = item(i + 1), certa = ini(w);
      box.appendChild(figComSom(w));
      var ops = (DISTRA[w] || []).concat([certa]).sort().map(function(s){
        return {v: s, rot: '<span class="ltop">' + esc(s) + "</span>",
                aria: "pedaço " + s, fala: "sb1_" + s};
      });
      opcoes(box, pi, id, ops, certa, "figbt", "certo2_" + w, "dica2_" + w);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 3 — CIRCULE QUEM COMEÇA IGUAL (das folhas D03 e D21)
   ⭐ MARCAR VÁRIOS é diferente de escolher UM: a criança tem que decidir figura
   por figura, e não pode parar na primeira que serve. O alvo é DADO aqui — na
   folha 5 ele some, e é isso que sobe o degrau. */
function f3(d, pi){
  faixa(d, pi, NOMES[2]);
  enunciado(d, pi, "Toque em <b>todas</b> as figuras que começam com este pedacinho. Depois toque em Conferir.", "p3enun");
  var L = ST.folha.p3;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "n3_" + i, box = item(i + 1), feito = !!ST.resp[id];
      var certas = it.g.filter(function(w){ return ini(w) === it.s; });
      registra(id, pi, certas.join(","));
      var alvo = el("div", "alvosil");
      alvo.appendChild(el("span", "ltop grandao", esc(it.s)));
      alvo.appendChild(botaoSom("Ouvir o pedacinho " + it.s, function(){ falar("sb1_" + it.s); }));
      box.appendChild(alvo);
      var grade = el("div", "gradecirc"), marc = {};
      it.g.forEach(function(w){
        var b = el("button", "figcirc" + (feito && ini(w) === it.s ? " marcada" : ""),
                   img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>");
        b.setAttribute("data-qa", "marc-" + id + "-" + w);
        b.setAttribute("aria-label", esc(w));
        b.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("pal_" + w);
          marc[w] = !marc[w];
          b.className = "figcirc" + (marc[w] ? " marcada" : "");
        };
        grade.appendChild(b);
      });
      box.appendChild(grade);
      var pr = el("button", "bt verde pronto", "Conferir");
      pr.setAttribute("data-qa", "conf-" + id);
      pr.onclick = function(){
        if(ST.resp[id]) return;
        var ok = certas.every(function(w){ return marc[w]; }) &&
                 it.g.every(function(w){ return ini(w) === it.s || !marc[w]; });
        if(ok){ acertou(id, "certo3_" + it.s); box.className = "item feito"; }
        else { sErro(); errou(id, "dica3_" + it.s); }
      };
      if(feito) pr.style.display = "none";
      box.appendChild(pr);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 4 — LIGUE CADA FIGURA AO SEU COMEÇO (das folhas D11 e D14)
   Quatro de uma vez, e os quatro começos são DIFERENTES: a criança tem que
   segurar quatro sons na cabeça e ainda decidir qual vai com qual. */
function f4(d, pi){
  faixa(d, pi, NOMES[3]);
  enunciado(d, pi, "<b>Ligue</b> cada figura ao pedacinho com que ela começa.", "p4enun");
  var L = ST.folha.p4;
  for(var i = 0; i < L.length; i++){
    var g = L[i], cx = el("div", "");
    montaLigar(cx, pi, "n4g" + i, g.map(function(w){
      return {k: w, w: esc(w), wd: esc(ini(w)),
              esq: img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>",
              dir: '<span class="ltop grandao">' + esc(ini(w)) + "</span>",
              fe: "pal_" + w, fd: "sb1_" + ini(w),
              fc: "certo4_" + w, dica: "dica4_" + w};
    }), d);
    d.appendChild(cx);
  }
}

/* 5 — ACHE AS DUAS QUE COMEÇAM IGUAL ⭐ O DEGRAU QUE O PAPEL NÃO OFERECE
   Todas as folhas de origem DÃO o pedacinho e mandam procurar quem combina.
   Aqui não há alvo: a criança tem que comparar todas com todas até achar o par.
   É a diferença entre reconhecer e PROCURAR — e é onde a habilidade fica dela.
   ⚠️ Os distratores são escolhidos para NÃO começarem com a mesma letra do par,
   nesta folha: a discriminação letra × sílaba tem folha própria (a 7). */
function f5(d, pi){
  faixa(d, pi, NOMES[4]);
  enunciado(d, pi, "Nesta grade há <b>duas</b> que começam com o mesmo pedacinho. Ache as duas.", "p5enun");
  var L = ST.folha.p5;
  for(var i = 0; i < L.length; i++){
    (function(g, i){
      var id = "n5_" + i, box = item(i + 1), feito = !!ST.resp[id];
      var conta = {}, par = null, k;
      g.forEach(function(w){ conta[ini(w)] = (conta[ini(w)] || 0) + 1; });
      for(k in conta) if(conta[k] === 2) par = k;
      var certas = g.filter(function(w){ return ini(w) === par; });
      registra(id, pi, certas.join(","));
      var grade = el("div", "gradecirc"), marc = [];
      g.forEach(function(w){
        var b = el("button", "figcirc" + (feito && ini(w) === par ? " marcada" : ""),
                   img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>");
        b.setAttribute("data-qa", "par-" + id + "-" + w);
        b.setAttribute("aria-label", esc(w));
        b.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("pal_" + w);
          var j = marc.indexOf(w);
          if(j > -1){ marc.splice(j, 1); b.className = "figcirc"; return; }
          if(marc.length >= 2) return;          /* só duas por vez */
          marc.push(w); b.className = "figcirc marcada";
          if(marc.length === 2){
            if(ini(marc[0]) === ini(marc[1])) acertou(id, "certo5_" + certas[0]);
            else {
              sErro();
              var todos = grade.querySelectorAll("button"), z;
              for(z = 0; z < todos.length; z++) todos[z].className = "figcirc";
              marc = []; errou(id, "dica5_" + certas[0]);
            }
          }
        };
        grade.appendChild(b);
      });
      box.appendChild(grade);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 6 — COMPLETE O COMEÇO (das folhas D06, D19 e D20, SEM recortar nem escrever)
   No papel ela recorta a sílaba e cola. Aqui ela PUXA — e quem não consegue
   arrastar, toca. Escrever a sílaba é o degrau 5 da sequência, não este. */
function f6(d, pi){
  faixa(d, pi, NOMES[5]);
  enunciado(d, pi, "Falta o <b>começo</b> da palavra. Ponha o pedacinho certo no lugar.", "p6enun");
  var L = ST.folha.p6;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n6_" + i, box = item(i + 1), ss = sil(w), certa = ss[0];
      var feito = !!ST.resp[id];
      registra(id, pi, certa);
      box.appendChild(figComSom(w));
      var lin = el("div", "vagas");
      var v = el("div", "vaga" + (feito ? " ok" : ""), feito ? esc(certa) : "");
      lin.appendChild(v);
      for(var k = 1; k < ss.length; k++)
        lin.appendChild(el("div", "sq larga", esc(ss[k])));
      box.appendChild(lin);
      var banco = el("div", "silbanco");
      var lista = (DISTRA[w] || []).concat([certa]).sort();
      lista.forEach(function(s){
        var b = el("button", "sil" + (feito && s === certa ? " usada" : ""), esc(s));
        b.setAttribute("data-qa", "põe-" + id + "-" + s);
        b.setAttribute("aria-label", "pedaço " + s);
        function poe(){
          if(ST.resp[id]) return;
          if(s !== certa){
            sErro(); b.className = "sil erro";
            setTimeout(function(){ b.className = "sil"; }, 460);
            errou(id, "dica6_" + w); return;
          }
          sPasso(); falarSilaba(w, 0, certa);
          v.className = "vaga ok"; v.textContent = esc(certa);
          b.className = "sil usada";
          setTimeout(function(){ acertou(id, "certo6_" + w); }, 560);
        }
        b.onclick = function(){ if(b._arrastou){ b._arrastou = false; return; } poe(); };
        puxavel(b, [v], poe);
        banco.appendChild(b);
      });
      box.appendChild(banco);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 7 — QUEM NÃO É DA FAMÍLIA? ⭐ E AQUI ENTRA A DISCRIMINAÇÃO QUE IMPORTA
   Três começam com o mesmo pedacinho e uma não. Achar o intruso é mais difícil
   que achar o par: em vez de procurar semelhança, a criança tem que CONFERIR
   uma família que já está montada — e para isso precisa do critério na cabeça,
   não na tela. */
function f7(d, pi){
  faixa(d, pi, NOMES[6]);
  enunciado(d, pi, "Três começam com o <b>mesmo pedacinho</b> e uma não. Circule quem não é da família.", "p7enun");
  var L = ST.folha.p7;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "n7_" + i, box = item(i + 1);
      registra(id, pi, it.c);
      var grade = el("div", "gradecirc filaerr"), bts = [];
      it.g.forEach(function(w){
        var b = el("button", "figcirc", img(w, "figop") +
                   '<span class="rotop">' + esc(w) + "</span>");
        b.setAttribute("data-qa", "int-" + id + "-" + w);
        b.setAttribute("aria-label", esc(w));
        b._w = w; grade.appendChild(b); bts.push(b);
      });
      box.appendChild(grade);
      riscoDeCircular(grade, bts, function(b){
        if(ST.resp[id]) return;
        sPasso(); falar("pal_" + b._w);
        if(b._w === it.c){ b.className = "figcirc marcada"; acertou(id, "certo7_" + it.c); }
        else { b.className = "figcirc erro";
               setTimeout(function(){ b.className = "figcirc"; }, 480);
               errou(id, "dica7_" + it.c); }
      });
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 8 — AS TRÊS GAVETAS DO COMEÇO
   ⭐ Classificar é mais difícil que comparar: a criança precisa do começo na
   cabeça E do critério fora da palavra — na gaveta. É a primeira vez neste
   caderno em que a resposta não está na figura. */
function f8(d, pi){
  faixa(d, pi, NOMES[7]);
  enunciado(d, pi, "Ponha cada figura na <b>gaveta do começo dela</b>.", "p8enun");
  var L = ST.folha.p8, gav = el("div", "gavetas"), caixas = [], vistos = [];
  L.forEach(function(w){ if(vistos.indexOf(ini(w)) < 0) vistos.push(ini(w)); });
  vistos.sort();
  vistos.forEach(function(s){
    var c = el("div", "gaveta");
    var t = el("div", "gtit");
    t.appendChild(el("span", "", esc(s)));
    t.appendChild(botaoSom("Ouvir o pedacinho " + s, function(){ falar("sb1_" + s); }));
    c.appendChild(t);
    var dentro = el("div", "gdentro");
    c.appendChild(dentro); c._dentro = dentro; c._s = s;
    c.setAttribute("data-qa", "gaveta-" + s);
    gav.appendChild(c); caixas.push(c);
  });
  var banco = el("div", "figbanco");
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n8_" + i, feito = !!ST.resp[id];
      registra(id, pi, ini(w));
      var b = el("button", "op fig" + (feito ? " usada" : ""),
                 img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>");
      b.setAttribute("data-qa", "gav-" + id + "-" + ini(w));
      b.setAttribute("aria-label", esc(w));
      function poe(alvo){
        if(ST.resp[id]) return;
        sPasso(); falar("pal_" + w);
        if(alvo._s === ini(w)){
          b.className = "op fig usada";
          alvo._dentro.appendChild(el("span", "gfig", img(w, "figmini")));
          acertou(id, "certo8_" + w);
        } else {
          alvo.className = "gaveta erro";
          setTimeout(function(){ alvo.className = "gaveta"; }, 480);
          errou(id, "dica8_" + w);
        }
      }
      /* as DUAS portas: puxar até a gaveta, ou tocar na figura e na gaveta */
      b.onclick = function(){
        if(b._arrastou){ b._arrastou = false; return; }
        if(ST.resp[id]) return;
        falar("pal_" + w);
        MARCADA = (MARCADA === b) ? null : b;
        var todos = banco.querySelectorAll("button"), j;
        for(j = 0; j < todos.length; j++)
          todos[j].className = todos[j].className.replace(/ ?marcada/, "");
        if(MARCADA) b.className = b.className + " marcada";
      };
      b._poe = poe;
      puxavel(b, caixas, function(alvo){ poe(alvo); });
      if(feito) caixas.forEach(function(c){
        if(c._s === ini(w)) c._dentro.appendChild(el("span", "gfig", img(w, "figmini")));
      });
      banco.appendChild(b);
    })(L[i], i);
  }
  caixas.forEach(function(c){
    c.onclick = function(){
      if(!MARCADA) return;
      var b = MARCADA; MARCADA = null;
      b.className = b.className.replace(/ ?marcada/, "");
      b._poe(c);
    };
  });
  d.appendChild(gav);
  d.appendChild(banco);
}
var MARCADA = null;

/* 9 — ESCREVA O COMEÇO (das folhas D09 e D18: o degrau mais alto)
   Sem opção nenhuma na tela: ela ouve e escreve. As DUAS portas, regra da casa
   — teclado na tela E teclado de verdade. */
function f9(d, pi){
  faixa(d, pi, NOMES[8]);
  enunciado(d, pi, "Ouça a palavra e <b>escreva o pedacinho</b> com que ela começa.", "p9enun");
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n9_" + i, box = item(i + 1), certa = ini(w), feito = !!ST.resp[id];
      registra(id, pi, certa);
      box.appendChild(figComSom(w));
      var lin = el("div", "vagas"), ss = sil(w);
      var q = el("div", feito ? "sq ok" : "sq vaga", feito ? esc(certa) : "");
      q.setAttribute("data-qa", "esc-" + id);
      q.onclick = function(){ if(!ST.resp[id]) ativa(q, esc(certa), id, "certo9_" + w, "dica9_" + w); };
      lin.appendChild(q);
      for(var k = 1; k < ss.length; k++)
        lin.appendChild(el("div", "sq larga", esc(ss[k])));
      box.appendChild(lin);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 10 — O MURAL DAS FAMÍLIAS (o fecho, e ele GUARDA o que ela fez)
   ⭐ Regra 11 da pesquisa: a tela final mostra o que a CRIANÇA fez. Cada palavra
   que ela escolhe entra no mural com o começo dela em destaque — e o painel
   fica no relatório. É o cartaz da família silábica, feito por ela. */
function f10(d, pi){
  faixa(d, pi, NOMES[9]);
  enunciado(d, pi, "Toque nas palavras que você quer no <b>seu mural</b>. Ele fica guardado no fim.", "p10enun");
  var L = ST.folha.p10, mural = el("div", "mural");
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "n10_" + i;
      registra(id, pi, w);
      var c = el("button", "cartaorima cartasil",
        img(w, "figop") +
        '<span class="rotop"><b class="ini">' + esc(ini(w)) + "</b>" +
        esc(w).slice(esc(ini(w)).length) + "</span>");
      c.setAttribute("data-qa", "mural-" + id);
      c.setAttribute("aria-label", esc(w) + ", começa com " + ini(w));
      c.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falarSilaba(w, 0, ini(w));
        setTimeout(function(){ falar("pal_" + w); }, 700);
        c.className = "cartaorima cartasil escolhido";
        acertou(id, "certo10_" + w);
      };
      if(ST.resp[id]) c.className = "cartaorima cartasil escolhido";
      mural.appendChild(c);
    })(L[i], i);
  }
  d.appendChild(mural);
}

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
   Da folha: *"circule os desenhos que se iniciam com a sílaba CA"* (d12/d02). */var LAPIS = [
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
    e.setAttribute("aria-label", esc(P.wd || P.k));
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

/* ---------- teclado de letras (folha 8) ---------- */function ativa(q, certa, id, fc, fd){
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
  /* ⚠️⚠️ OS IDS TÊM QUE BATER COM O QUE AS FOLHAS GRAVAM (prefixo `n`).
     É aqui que um caderno clonado mente no relatório sem dar erro nenhum: os
     dois lados ficam sintaticamente corretos e a nota sai ZERO com a folha toda
     respondida. Aconteceu duas vezes nesta casa. Conferir JOGANDO até o fim.
     ⚠️ A folha 4 é de LIGAR: o id nasce dentro do `montaLigar` e tem outra
     forma (`l<pagina><tag>_<chave>`). */
  var ids = [], i, k, F = ST.folha;
  if(pi === 1) for(i = 0; i < F.p1.length; i++) ids.push("n1_" + i);
  if(pi === 2) for(i = 0; i < F.p2.length; i++) ids.push("n2_" + i);
  if(pi === 3) for(i = 0; i < F.p3.length; i++) ids.push("n3_" + i);
  if(pi === 4) for(i = 0; i < F.p4.length; i++) for(k = 0; k < F.p4[i].length; k++)
    ids.push("l4n4g" + i + "_" + F.p4[i][k]);
  if(pi === 5) for(i = 0; i < F.p5.length; i++) ids.push("n5_" + i);
  if(pi === 6) for(i = 0; i < F.p6.length; i++) ids.push("n6_" + i);
  if(pi === 7) for(i = 0; i < F.p7.length; i++) ids.push("n7_" + i);
  if(pi === 8) for(i = 0; i < F.p8.length; i++) ids.push("n8_" + i);
  if(pi === 9) for(i = 0; i < F.p9.length; i++) ids.push("n9_" + i);
  if(pi === 10) for(i = 0; i < F.p10.length; i++) ids.push("n10_" + i);
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
  for(pi = 1; pi <= NOMES.length; pi++){
    var ids = idsDaPagina(pi);
    tot += ids.length;
    for(var j = 0; j < ids.length; j++){ var t = ST.tent[ids[j]]; if(t && t.erros === 0 && t.ok) prim++; }
  }
  var pc = tot ? prim / tot : 0;
  var cheias = pc >= .85 ? 3 : pc >= .6 ? 2 : 1, est = "", ke;
  for(ke = 0; ke < 3; ke++)
    est += '<img src="img/ro_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
  document.getElementById("estrelas").innerHTML = est;
  document.getElementById("estrelas").setAttribute("aria-label", cheias + " de 3 estrelas");
  var bar = document.getElementById("barras"); bar.innerHTML = "";
  for(pi = 1; pi <= NOMES.length; pi++){
    (function(pi){
      var ids = idsDaPagina(pi), t = ids.length, p = 0, j;
      for(j = 0; j < ids.length; j++){ var tt = ST.tent[ids[j]]; if(tt && tt.erros === 0 && tt.ok) p++; }
      var b = el("div", "barra", "<span>" + NOMES[pi - 1] + "</span><div class='tr'><i></i></div><b>" + p + "/" + t + "</b>");
      bar.appendChild(b);
      setTimeout(function(){ b.querySelector("i").style.width = (t ? p / t * 100 : 0) + "%"; }, 400);
    })(pi);
  }
  /* ⭐ O PARECER DA CRIANÇA (mudança de set/2026 — ver o bloco dos OBJETIVOS).
     O currículo de Blumenau diz que a avaliação orienta *"o professor E O
     ESTUDANTE acerca de quais objetivos foram alcançados"*, e que *"mostrar o
     que sabe ou o que não sabe é pertinente, faz parte do crescimento e não da
     exclusão"*. Então ela vê o que já sabe — na linguagem dela, sem número,
     sem a palavra "errou" e sem porcentagem.
     ⚠️ A ORDEM IMPORTA: primeiro o que ela JÁ SABE, sempre; o "vale treinar" vem
     depois e no máximo dois, senão a lista vira boletim de defeitos. */
  var jaSabe = [], treinar = [], q;
  for(q = 0; q < OBJETIVOS.length; q++){
    var Oq = OBJETIVOS[q], mq = mede(Oq.f);
    if(mq.tot === 0) continue;
    (mq.pc >= 75 ? jaSabe : treinar).push(mq.pc >= 75 ? Oq.ok : Oq.n.toLowerCase());
  }
  var txt = "";
  /* ⚠️ "Você JÁ ..." e não "Você já SABE ..." (set/2026, achado na leitura da
     tela de fim). Os textos dos OBJETIVOS estão escritos em terceira pessoa
     ("junta os dois pedaços", "conta as palmas") — que em português é a MESMA
     forma de "você". Com o "sabe" no meio saía "Você já sabe junta os dois
     pedaços", e era a PRIMEIRA frase que a criança lia no fim do caderno. */
  if(jaSabe.length) txt = "Você já " + jaSabe.slice(0, 3).join("; ") + ".";
  else txt = "Você começou a ouvir o comecinho das palavras — e ele diz muita coisa!";
  if(treinar.length) txt += " Vale treinar mais: " + treinar.slice(0, 2).join(" e ") + ".";
  document.getElementById("resumo").innerHTML =
    "<b>" + esch(ST.nome || "Você") + "</b>, " + txt.charAt(0).toLowerCase() + txt.slice(1);
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

   ⭐ PEDIDO DO MARCOS (set/2026): *"acho interessante ter um relatório, tipo uma
   avaliação descritiva sobre o que o aluno conseguiu dominar nesses objetivos
   das atividades"* e *"algo que dê para converter em nota"*.

   ⭐⭐ E A REGRA DA CASA MUDOU AQUI — o Marcos mandou conferir e ele tinha razão:
   *"essa regra pode ser alterada, consulta do pedagogo e do currículo seria
   interessante"*. Fui ao currículo de Blumenau e ele diz, com todas as letras:

     · a avaliação *"está a serviço de orientar o professor E O ESTUDANTE acerca
       de quais objetivos de aprendizagem foram alcançados"* — o estudante é
       destinatário da avaliação, não só o professor;
     · e, citado com aprovação (Pinto, 2016, p. 120): *"na perspectiva do sujeito
       histórico-cultural, MOSTRAR O QUE SABE OU O QUE NÃO SABE É PERTINENTE,
       faz parte do crescimento e NÃO DA EXCLUSÃO"*.

   Ou seja: esconder da criança o que ela domina não era exigência pedagógica —
   era escolha nossa, e o currículo aponta para o contrário. Então a criança
   PASSA A VER o parecer dela, na linguagem dela.

   ⚠️ O QUE NÃO MUDA É O NÚMERO. A Instrução Normativa SEMED nº 1/2017, art. 3º,
   citada no currículo, manda avaliar *"com PREPONDERÂNCIA DOS ASPECTOS
   QUALITATIVOS SOBRE OS QUANTITATIVOS"*. Então o parecer vai para a criança e a
   NOTA fica com o professor: não por medo do número, mas porque o currículo diz
   qual dos dois deve pesar na frente dela.

   ⚠️ E O CRITÉRIO DA NOTA É EXPOSTO POR EXIGÊNCIA, não por capricho: a mesma
   Instrução manda *"a exposição de critérios utilizados em cada um dos
   instrumentos avaliativos"*. Por isso a linha "1,0 de primeira, 0,6 com ajuda"
   aparece impressa no relatório.

   ⚠️ E NÃO SE CONTA TUDO IGUAL. Quem acerta de primeira e quem acerta depois de
   duas dicas não sabem a mesma coisa. Acerto de primeira vale 1,0; acerto com
   ajuda vale 0,6. O relatório mostra os dois números lado a lado, para o
   professor ver a nota E o esforço que ela custou.
   ============================================================ */
var PESO_PRIMEIRA = 1.0, PESO_COM_AJUDA = 0.6;

/* OS OBJETIVOS — e quais folhas medem cada um.
   ⚠️ Isto NÃO é a lista de folhas: é a lista do que a criança tem que SABER.
   Duas folhas podem medir a mesma coisa com gestos diferentes, e para o
   professor interessa o que ela domina, não em qual tela. */
var OBJETIVOS = [
  /* ⚠️ ESTA LISTA E O `curriculo.json` SÃO A MESMA COISA, ditas para dois
     leitores: aqui em palavras que o professor lê no relatório, lá no
     vocabulário do currículo da rede. O portão 0b9 reprova se os nomes e as
     folhas não baterem um a um — foi ele que me pegou ao eu deixar aqui os
     objetivos do degrau 3 depois de já ter reescrito o dossiê. */
  {n: "Montar a roda: a mesma consoante com as cinco vogais", f: [1],
   ok: "entende que o L fica parado e a vogal é que muda o pedacinho",
   nao: "ainda não liga a vogal escolhida ao pedacinho que nasce"},
  {n: "Ouvir a palavra e dizer com que pedacinho ela começa", f: [2, 3],
   ok: "ouve a palavra e acha o pedacinho do começo, escrito ou na figura",
   nao: "ainda troca o pedacinho do começo pelo de outra vogal"},
  {n: "Distinguir sílabas que só diferem na vogal", f: [4, 5],
   ok: "separa LA de LE, LI, LO e LU — a letra é a mesma, o pedacinho não",
   nao: "ainda decide pela LETRA e não pelo pedacinho inteiro"},
  {n: "Completar e classificar pelo pedacinho do começo", f: [6, 7, 8],
   ok: "põe o pedacinho que falta e separa as figuras por ele",
   nao: "ainda se perde quando as palavras começam todas com a mesma letra"},
  {n: "Escrever o pedacinho que se ouve", f: [9],
   ok: "escreve sozinha o pedacinho do começo, sem opções",
   nao: "ainda precisa das opções para escolher o pedacinho"},
  {n: "Montar o próprio mural de rodas", f: [10],
   ok: "escolhe as palavras e monta o mural das rodas",
   nao: "ainda não escolheu as palavras do mural"}
];

/* mede um objetivo: devolve acertos de primeira, com ajuda, total e pontos */
function mede(folhas){
  var prim = 0, ajuda = 0, tot = 0, k, j;
  for(k = 0; k < folhas.length; k++){
    var ids = idsDaPagina(folhas[k]);
    tot += ids.length;
    for(j = 0; j < ids.length; j++){
      var t = ST.tent[ids[j]];
      if(!t || !t.ok) continue;
      if(t.erros === 0) prim++; else ajuda++;
    }
  }
  return {prim: prim, ajuda: ajuda, tot: tot,
          pontos: prim * PESO_PRIMEIRA + ajuda * PESO_COM_AJUDA,
          pc: tot ? Math.round(100 * prim / tot) : 0};
}

function abreRelatorio(){
  var r = document.getElementById("relatorio");
  var linhas = "", domina = [], retomar = [], k;
  var pontos = 0, total = 0, primG = 0, ajudaG = 0;

  for(k = 0; k < OBJETIVOS.length; k++){
    var O = OBJETIVOS[k], m = mede(O.f);
    pontos += m.pontos; total += m.tot; primG += m.prim; ajudaG += m.ajuda;
    /* ⚠️ 75% é a ÚNICA linha que decide, e as duas listas são complementares:
       um objetivo não pode aparecer em "domina" e em "retomar" ao mesmo tempo —
       para o professor isso não é informação, é ruído. */
    if(m.pc >= 75) domina.push(O.ok);
    else retomar.push(O.n.toLowerCase() + " (" + m.pc + "%)");
    linhas += "<tr><td>" + esch(O.n) + "</td><td>" + m.prim + "/" + m.tot +
      "</td><td><b>" + m.pc + "%</b></td><td>" + m.ajuda + "</td></tr>";
  }

  /* ⭐ A NOTA. É de 0 a 10, com um decimal, e sai dos PONTOS — não dos acertos
     crus: 1,0 de primeira, 0,6 com ajuda. */
  var nota = total ? Math.round(100 * pontos / total) / 10 : 0;
  var pc = total ? Math.round(100 * primG / total) : 0;
  var conceito = nota >= 8.5 ? "Dominou" : nota >= 6 ? "Está construindo" : "Precisa retomar";

  /* ⭐ O PARECER EM PALAVRAS — a "avaliação descritiva" que o Marcos pediu.
     Não é uma frase de efeito: é a lista do que ela SABE FAZER, escrita como o
     professor escreveria no parecer bimestral. */
  var nome = esch(ST.nome || "O aluno");
  var parecer = nome + " ";
  if(domina.length === OBJETIVOS.length)
    parecer += "domina a sílaba inicial em todos os degraus avaliados: " +
      domina.join("; ") + ".";
  else if(domina.length)
    parecer += "já " + domina.join("; ") + ". Ainda precisa retomar: " + retomar.join(", ") + ".";
  else
    parecer += "está começando a ouvir o comecinho das palavras. Nenhum objetivo chegou " +
      "a 75% de acerto de primeira — vale retomar ORALMENTE, brincando de achar coisas da " +
      "sala que começam igual ao nome dela, antes de voltar à tela.";

  var h = "<b>Relatório do professor</b> &mdash; " + nome + " &middot; " +
    Math.round((Date.now() - (ST.inicio || Date.now())) / 60000) + " min" +
    "<div class='notao'><span class='nn'>" + nota.toFixed(1).replace(".", ",") + "</span>" +
    "<span class='nl'><b>" + conceito + "</b><br>" + primG + " de " + total +
    " de primeira (" + pc + "%)<br>" + ajudaG + " com ajuda</span></div>" +
    "<p class='parecer'>" + parecer + "</p>" +
    "<table><tr><th>Objetivo</th><th>De primeira</th><th>%</th><th>Com ajuda</th></tr>" +
    linhas + "</table>" +
    "<p class='comonota'>Nota de 0 a 10: acerto de primeira vale 1,0 e acerto com ajuda vale 0,6. " +
    "A criança não vê este número — ele fica só aqui.</p>";
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
