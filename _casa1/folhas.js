/* ============================================================
   A RUA DO MUNDO — as vinte e cinco folhas.

   Cada folha nasceu de um VERBO impresso numa folha real de Geografia de 2º ano
   (as 30 de `_sequencias/folhas_moradia/`). O crivo, folha a folha, com o motivo
   de cada recusa, está em `_sequencias/POTE-MORADIA.md`. Nenhuma mecânica foi
   escolhida do nosso cardápio: a folha de papel é que manda — e, onde o papel
   parava num degrau abaixo do ano, quem mandou foi o currículo da rede.

   ⚠️ A POSIÇÃO É A IDENTIDADE: a folha da posição 7 usa o pote `p7`, grava os
      ids `n7_*` e fala `p7enun`. Não há segunda lista para desencontrar — isso
      já fez o relatório sair ZERO com a folha inteira respondida.
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI — são as únicas cujos ids não nascem
   de `n<pi>_`, e sim dentro do `montaLigar` (`l<pi>g<i>_<chave>`). São DUAS
   neste caderno; no caderno anterior era uma só e a constante era um número.
   Guardar um número onde agora há duas posições faria a folha 22 sumir do
   relatório sem erro nenhum na tela. */
var LIGAR = [8, 22];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou (nomear · material · lugar · de cima · tempo · fecho) */
var CORES = ["c1","c1","c1","c1","c1", "c2","c2","c2","c2","c2",
             "c3","c3","c3","c3","c3","c3", "c4","c4","c4",
             "c5","c5","c5","c5", "c3","c1"];

function faixa(d, i, titulo){ d.appendChild(el("div", "faixa", '<div class="num">' + i + '</div><h2>' + titulo + '</h2>')); }
function aoAbrir(d, fn){ if(!d._aoAbrir) d._aoAbrir = []; d._aoAbrir.push(fn); }
/* ---------- O ALTO-FALANTE ----------
   Regra da casa: no 2º ano boa parte da turma ainda soletra. Tudo o que a
   criança PRECISA LER tem que poder ser OUVIDO, senão ela responde pelo desenho
   e a folha vira loteria. O desenho é CSS puro — nada de emoji (vira
   quadradinho nos PCs da escola) e nada de SVG solto. */
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
/* ⚠️⚠️ O NOME DA MORADIA NÃO PODE APARECER ANTES DA RESPOSTA.
   Este defeito já esteve NO AR em cinco cadernos desta casa: a figura vinha com
   a legenda por baixo e, dois centímetros abaixo, a pergunta "que moradia é
   esta?". Quem já lê um pouco resolvia copiando, e a folha media zero.
   ⚠️ E ELE ESTÁ NUMA DAS FOLHAS DE ORIGEM: a d03 manda "escreva o nome dos
      tipos de moradia" com CASA, PRÉDIO, OCA, PALAFITA e IGLU já impressos
      dentro dos retângulos.
   A legenda não some — fica INVISÍVEL (`visibility`, para o espaço ficar
   guardado e a folha não pular) e aparece no instante do acerto. */
function nomeSecreto(txt, id){
  var b = el("b", "segredo" + (ST.resp[id] ? " revelado" : ""), txt);
  b.setAttribute("data-nome", id);
  return b;
}
/* a figura da moradia com o alto-falante ao lado e o nome guardado */
function figMor(k, id, cls){
  var c = el("div", "figsil" + (cls ? " " + cls : ""));
  c.innerHTML = img(k, "figgrande", "Uma moradia");
  var lin = el("div", "chamlin");
  lin.appendChild(id ? nomeSecreto(MOR[k].n, id) : el("b", "", MOR[k].n));
  lin.appendChild(botaoSom("Ouvir a descrição desta moradia", function(){ falar("olhe_" + k); }));
  c.appendChild(lin);
  return c;
}

function monta(){
  livro.innerHTML = ""; PAGEL = []; RESP = {}; TIRAS = [];
  var caps = [f0,
    f01, f02, f03, f04, f05,          /* 1-5   nomear (retomada do 1º ano)      */
    f06, f07, f08, f09, f10,          /* 6-10  de que é feita (habilidade E)    */
    f11, f12, f13, f14, f15, f16,     /* 11-16 em que lugar, e por quê (A)      */
    f17, f18, f19,                    /* 17-19 vista de cima (B)                */
    f20, f21, f22, f23,               /* 20-23 antes e hoje, a obra (C)         */
    f24, f25], i;                     /* 24-25 respeito (D) e o mural (F)       */
  for(i = 0; i < caps.length; i++){
    var d = el("div", "pagina" + (i > 0 ? " " + CORES[i - 1] : "")); d.setAttribute("data-pag", i);
    caps[i](d, i);
    if(i > 0) d.appendChild(el("div", "carimbo", "FOLHA<br>PRONTA"));
    livro.appendChild(d); PAGEL.push(d);
  }
}

/* ---------- capa ----------
   A capa não é enfeite: é a primeira coisa que a criança vê, e é ela que diz
   "isto aqui é um lugar bom". O tema sai do nome — uma RUA em que as casas do
   mundo inteiro são vizinhas, que é exatamente a ideia da habilidade D.
   ⚠️ CAPA CLONADA = TROCAR A CENA, SEMPRE. Numa capa herdada desta casa ficou
      um `img("sapo")` de outra atividade: o app abria com um quadradinho vazio
      e um 404 no console, e nenhum portão de texto viu. */
function f0(d){
  var c = el("div", "capa"), nome = "A RUA DO MUNDO", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  var cena = "";
  ["oca", "palafita", "casa", "predio", "iglu"].forEach(function(m){
    cena += img(m, "", MOR[m].n);
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Geografia &middot; 2º ano &middot; vinte e cinco folhas sobre onde a gente mora</div>' +
    '<div class="esteira">' +
      '<div class="cena">' + cena + "</div>" +
      '<div class="cinta"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>' +
    "</div>" +
    '<div class="chamada">Escreva o seu nome ali embaixo e toque em <b>Começar</b>.</div>';
  d.appendChild(c);
}

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

/* ============ 1 — PARA QUE SERVE UMA CASA? (marcar VÁRIAS certas) ============
   Da folha d18 (livro didático, p. 29): *"Leia a frase e marque com um x as
   alternativas corretas — A moradia serve..."*.

   ⭐ POR QUE ELA ABRE O CADERNO: é o PROBLEMA antes do conceito. Antes de saber
   que existe iglu e palafita, a criança precisa perceber para que serve uma
   casa — é isso que faz as outras vinte e quatro folhas terem pergunta.
   ⚠️ E é a única mecânica em que MAIS DE UMA resposta está certa. As folhas de
   papel do pote quase sempre têm resposta única; esta não, e é de propósito. */
function f01(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Marque <b>todas</b> as que estiverem certas. Depois toque em <b>Conferir</b>.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MARCAR[k], id = "n" + pi + "_" + i;
    registra(id, pi, M.c.join(","));
    var box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", M.q));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("perg1_" + k); }));
    box.appendChild(lin);
    var cx = el("div", "marcax"), marcadas = {}, bts = {};
    baralha(M.c.concat(M.e)).forEach(function(fr){
      var b = el("button", "lx", '<span class="cx"></span><span>' + fr + "</span>");
      b.setAttribute("aria-label", fr);
      b.setAttribute("data-qa", "mc-" + id + "-" + fr);
      bts[fr] = b;
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(marcadas[fr]){ delete marcadas[fr]; b.className = "lx"; b.querySelector(".cx").textContent = ""; }
        else { marcadas[fr] = 1; b.className = "lx marcada"; b.querySelector(".cx").textContent = "X"; }
      };
      cx.appendChild(b);
    });
    box.appendChild(cx);
    var bt = el("button", "bt pronto", "Conferir");
    bt.setAttribute("data-qa", "conf-" + id);
    bt.onclick = function(){
      if(ST.resp[id]) return;
      var erro = 0, fr;
      for(fr in bts){
        var deve = M.c.indexOf(fr) > -1, tem = !!marcadas[fr];
        if(deve !== tem) erro++;
      }
      if(erro){
        for(fr in bts) if(marcadas[fr] && M.c.indexOf(fr) < 0) bts[fr].className = "lx errada";
        setTimeout(function(){ var g; for(g in bts) if(marcadas[g]) bts[g].className = "lx marcada"; }, 900);
        errou(id, "dica1_" + k);
        return;
      }
      for(fr in bts) if(M.c.indexOf(fr) > -1) bts[fr].className = "lx certa";
      bt.style.display = "none";
      acertou(id, "certo1_" + k);
    };
    if(ST.resp[id]){
      M.c.forEach(function(fr){ if(bts[fr]){ bts[fr].className = "lx certa"; bts[fr].querySelector(".cx").textContent = "X"; } });
      bt.style.display = "none";
    }
    box.appendChild(bt);
    fechaItem(d, box, id);
  });
}

/* ============ 2 e 3 — QUE MORADIA É ESTA? (escolher o nome) ============
   Da d01 e da d09: *"escreva nos retângulos os tipos de moradias
   correspondentes"*, com o banco de nomes fechado em cima.

   ⚠️ ISTO É RETOMADA DO 1º ANO, E ESTÁ DECLARADO ASSIM. Vinte e duas das trinta
   folhas colhidas param aqui — nomear. Em Blumenau, "descrever e comparar
   diferentes tipos de moradia" é habilidade do 1º ano; o 2º ano pergunta o
   PORQUÊ. Estas quatro folhas existem para pôr o vocabulário na mesa, não para
   ser o caderno.
   A folha 2 traz as moradias que a criança vê no caminho da escola; a 3, as de
   outros lugares — que é o que abre a porta da habilidade A. */
function nomeia(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe a moradia e toque no <b>nome</b> dela.", "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  pool.forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(figMor(k, id));
    /* os distratores são as OUTRAS moradias do caderno, nunca palavras inventadas */
    var outras = [], j;
    for(j in MOR) if(j !== k) outras.push(j);
    var lista = baralha([k].concat(pega(outras, 3))).map(function(m){
      return {v: m, rot: MOR[m].n, aria: MOR[m].n, fala: "chamar_" + m};
    });
    opcoes(box, pi, id, lista, k, "curta", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f02(d, pi){ nomeia(d, pi); }
function f03(d, pi){ nomeia(d, pi); }

/* ============ 4 — ARRASTE O NOME ATÉ A CASA ============
   Da d10 (liveworksheets): *"arraste os nomes e coloque em suas respectivas
   moradias"*. É o único gesto do pote em que a criança move a PALAVRA ESCRITA —
   e por isso ele entra inteiro, sem virar "escolher entre quatro".
   ⚠️ AS DUAS PORTAS: arrastar (PC) e tocar-na-etiqueta-depois-na-casa (celular).
   Guardar só o arrasto deixaria metade da turma de fora. */
function f04(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leve cada <b>nome</b> até a moradia certa. Dá para arrastar ou " +
            "tocar no nome e depois na casa.", "p" + pi + "enun");
  var pool = ST.folha["p" + pi], grelha = el("div", "grelha"), banco = el("div", "banconome");
  var alvos = {}, etiqs = {}, marcada = null;
  pool.forEach(function(k, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, k);
    var cel = el("div", "celmor");
    cel.innerHTML = img(k, "figop", "Uma moradia");
    cel.setAttribute("data-qa", "item-" + id);
    var alvo = el("div", "alvonome" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? MOR[k].n : "?");
    alvo.setAttribute("data-alvo", "1");
    alvo._k = k; alvo._id = id;
    alvos[k] = alvo;
    var lin = el("div", "chamlin");
    lin.appendChild(botaoSom("Ouvir a descrição desta moradia", function(){ falar("olhe_" + k); }));
    cel.appendChild(lin);
    cel.appendChild(alvo);
    grelha.appendChild(cel);
  });
  function larga(alvo, k){
    var id = alvo._id;
    if(ST.resp[id]) return;
    if(alvo._k === k){
      alvo.className = "alvonome cheia"; alvo.textContent = MOR[k].n;
      etiqs[k].className = "etiq usada";
      if(marcada){ marcada.className = "etiq"; marcada = null; }
      acertou(id, "certo" + pi + "_" + k);
    } else {
      alvo.className = "alvonome"; errou(id, "dica" + pi + "_" + k);
    }
  }
  var listaAlvos = [];
  pool.forEach(function(k){ listaAlvos.push(alvos[k]); });
  baralha(pool).forEach(function(k){
    var e = el("button", "etiq" + (ST.resp["n" + pi + "_" + pool.indexOf(k)] ? " usada" : ""), MOR[k].n);
    e.setAttribute("data-qa", "etiq-" + k);
    e.setAttribute("aria-label", MOR[k].n);
    etiqs[k] = e;
    e.onclick = function(){
      if(e._arrastou){ e._arrastou = false; return; }
      sPasso(); falar("chamar_" + k);
      if(marcada === e){ e.className = "etiq"; marcada = null; return; }
      if(marcada) marcada.className = "etiq";
      e.className = "etiq marcada"; marcada = e;
    };
    puxavel(e, listaAlvos, function(alvo){ larga(alvo, k); });
    banco.appendChild(e);
  });
  listaAlvos.forEach(function(alvo){
    alvo.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_etiqueta"); return; }
      var k, achou = null;
      for(k in etiqs) if(etiqs[k] === marcada) achou = k;
      if(achou) larga(alvo, achou);
    };
  });
  d.appendChild(grelha); d.appendChild(banco);
}

/* ============ 5 — JUNTE AS SÍLABAS E DESCUBRA ============
   Da d18, exercício 4: *"descubra os tipos de moradia juntando as sílabas"*,
   com a tabela numerada. No papel a criança escreve "5-8"; aqui ela TOCA nos
   pedaços, na ordem, e a palavra se monta na frente dela.
   ⚠️ A tabela é a mesma para os quatro itens (como no papel), e traz sílabas de
      todas as palavras misturadas — é isso que torna a tarefa uma tarefa. */
function f05(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque nas sílabas <b>na ordem</b> e descubra a moradia.", "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  /* a tabela: todas as sílabas das palavras da folha, embaralhadas e numeradas */
  var todas = [], k;
  pool.forEach(function(m){ MOR[m].s.forEach(function(s){ if(todas.indexOf(s) < 0) todas.push(s); }); });
  todas = baralha(todas);
  var tab = el("div", "tabsil"), celulas = {};
  todas.forEach(function(s, i){
    var c = el("button", "tsc", '<span class="tsn">' + (i + 1) + '</span><span class="tss">' + s + "</span>");
    c.setAttribute("aria-label", "Sílaba " + s);
    c.setAttribute("data-qa", "sil-" + s);
    celulas[s] = c;
    tab.appendChild(c);
  });
  d.appendChild(tab);
  pool.forEach(function(m, i){
    var id = "n" + pi + "_" + i, alvo = MOR[m].s;
    registra(id, pi, MOR[m].n);
    var box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Moradia " + (i + 1) + ": tem <b>" + alvo.length + "</b> sílabas."));
    lin.appendChild(botaoSom("Ouvir a dica desta moradia", function(){ falar("pistasil_" + m); }));
    box.appendChild(lin);
    var mont = el("div", "montada"), feito = !!ST.resp[id];
    var posto = feito ? alvo.slice(0) : [];
    function pinta(){
      mont.innerHTML = "";
      if(!posto.length){ mont.appendChild(el("span", "vazio", "toque as sílabas…")); return; }
      posto.forEach(function(s){ mont.appendChild(el("span", "mped", s)); });
    }
    pinta();
    box.appendChild(mont);
    var ativa = el("button", "bt pronto", feito ? "Pronto!" : "Montar esta");
    ativa.setAttribute("data-qa", "montar-" + id);
    if(feito) ativa.disabled = true;
    ativa.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); posto = []; pinta();
      falar("montenesta");
      var s2;
      for(s2 in celulas){
        (function(s3){
          celulas[s3].className = "tsc";
          celulas[s3].onclick = function(){
            if(ST.resp[id]) return;
            sTecla();
            posto.push(s3); pinta();
            celulas[s3].className = "tsc usada";
            if(posto.length >= alvo.length){
              if(posto.join("") === alvo.join("")){
                acertou(id, "certo" + pi + "_" + m);
                ativa.disabled = true; ativa.textContent = "Pronto!";
              } else {
                errou(id, "dica" + pi + "_" + m);
                posto = []; pinta();
                var s4; for(s4 in celulas) celulas[s4].className = "tsc";
              }
            }
          };
        })(s2);
      }
    };
    box.appendChild(ativa);
    fechaItem(d, box, id);
  });
}

/* ============ 6 e 7 — DE QUE É FEITA ESTA MORADIA? ============
   Da d06, d11 (questão 1) e d20 (questão 10): *"qual o principal material usado
   na fabricação das moradias abaixo?"* — no papel, dois parênteses para marcar.

   ⭐ ESTE É O DEGRAU DE CIÊNCIAS DO 2º ANO: *"identificar de que materiais
   (metal, madeira, vidro etc.) são feitos os objetos que fazem parte da vida
   cotidiana"*. A folha 6 dá DUAS opções (como o papel) e a 7 dá QUATRO, com a
   figura do material — mesmo gesto, um degrau acima, colados um no outro.
   ⚠️ REPETIÇÃO SEGUIDA, NÃO ESPAÇADA: as crianças dizem "isso eu já fiz" quando
      a mesma mecânica volta lá na frente. Em bloco, ela sente que subiu. */
function material(d, pi, quantas, comFigura){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, quantas === 2
    ? "De que esta moradia é feita? Toque no <b>material</b>."
    : "Agora são <b>quatro</b> materiais. Olhe bem a moradia e escolha.",
    "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(figMor(k, id));
    var certo = MOR[k].mat, outros = [], j;
    for(j in MAT) if(j !== certo) outros.push(j);
    var lista = baralha([certo].concat(pega(outros, quantas - 1))).map(function(m){
      return comFigura
        ? {v: m, rot: img(m, "figop", MAT[m].n) + '<span class="rotop">' + MAT[m].n + "</span>",
           aria: MAT[m].n, fala: "mat_" + m}
        : {v: m, rot: MAT[m].n, aria: MAT[m].n, fala: "mat_" + m};
    });
    opcoes(box, pi, id, lista, certo, comFigura ? "figbt" : "curta",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f06(d, pi){ material(d, pi, 2, false); }
function f07(d, pi){ material(d, pi, 4, true); }

/* ============ 8 — LIGUE A MORADIA AO MATERIAL ============
   Da d22 (Pequeno Lobato): *"ligue cada moradia ao material principal"*.
   ⚠️ Os ids desta folha nascem dentro do `montaLigar` e não em `n8_`: por isso a
      posição 8 está declarada lá em cima, na constante `LIGAR`. */
function f08(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque numa <b>moradia</b> e depois no <b>material</b> de que ela é feita.",
            "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: MOR[k].mat,
            esq: img(k, "", MOR[k].n),
            dir: img(MOR[k].mat, "", MAT[MOR[k].mat].n) ,
            ariaE: MOR[k].n, ariaD: MAT[MOR[k].mat].n,
            fe: "olhe_" + k, fd: "mat_" + MOR[k].mat,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  /* ⚠️ dois materiais iguais na coluna da direita fariam duas casas certas
     apontarem para a MESMA caixa, e o traço de uma apagaria o da outra. Como o
     `montaLigar` casa por chave, o sorteio do `novaFolha` já evita repetir
     material — mas se um dia repetir, o pedagogo vê aqui o porquê. */
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 9 — ACHE OS MATERIAIS NO DIAGRAMA (caça-palavras) ============
   Da d02 (livro de 2º ano, p. 30): *"procure, no diagrama, os nomes de cinco
   materiais que podem ser usados na construção de moradias"*.
   ⚠️ A GRADE É MONTADA NA HORA e as palavras entram só na horizontal e na
      vertical (nunca de trás para a frente, nunca na diagonal): no 2º ano ler
      ao contrário não é dificuldade desejável, é outra tarefa.
   ⚠️ Achar uma palavra ENSINA: ao fechar, a voz diz de que moradia aquele
      material é. Caça-palavras que só dá "parabéns" é passatempo. */
function f09(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Arraste o dedo sobre as letras para achar os <b>materiais</b>. " +
            "Eles estão deitados ou em pé.", "p" + pi + "enun");
  var palavras = ST.folha["p" + pi].map(function(m){ return MAT[m].n; });
  var N = 9, g = [], y, x;
  for(y = 0; y < N; y++){ g[y] = []; for(x = 0; x < N; x++) g[y][x] = ""; }
  var postas = {};
  palavras.forEach(function(w){
    var t, ok = false;
    for(t = 0; t < 260 && !ok; t++){
      var hor = rnd(2) === 0;
      var lx = hor ? rnd(N - w.length + 1) : rnd(N);
      var ly = hor ? rnd(N) : rnd(N - w.length + 1);
      var i, bate = true;
      for(i = 0; i < w.length; i++){
        var cy = ly + (hor ? 0 : i), cx2 = lx + (hor ? i : 0);
        if(g[cy][cx2] && g[cy][cx2] !== w.charAt(i)){ bate = false; break; }
      }
      if(!bate) continue;
      var cels = [];
      for(i = 0; i < w.length; i++){
        var cy2 = ly + (hor ? 0 : i), cx3 = lx + (hor ? i : 0);
        g[cy2][cx3] = w.charAt(i); cels.push(cy2 * N + cx3);
      }
      postas[w] = cels; ok = true;
    }
  });
  var enche = "ABCDEFGHIJLMNOPQRSTUVXZ";
  for(y = 0; y < N; y++) for(x = 0; x < N; x++) if(!g[y][x]) g[y][x] = enche.charAt(rnd(enche.length));
  var dia = el("div", "diagrama"); dia.style.gridTemplateColumns = "repeat(" + N + ",1fr)";
  var cels = [];
  for(y = 0; y < N; y++) for(x = 0; x < N; x++){
    var c = el("button", "dcel", g[y][x]);
    c.setAttribute("aria-label", "Letra " + g[y][x]);
    c._i = y * N + x; cels.push(c); dia.appendChild(c);
  }
  var lista = el("div", "listamat"), chips = {};
  ST.folha["p" + pi].forEach(function(m, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, MAT[m].n);
    var ch = el("span", "pmat" + (ST.resp[id] ? " achada" : ""), MAT[m].n);
    ch.setAttribute("data-qa", "item-" + id);
    /* ⚠️ ALVO DECLARADO: a lista do que procurar é o próprio enunciado do
       caça-palavras — sem ela não há o que achar. A folha impressa de origem
       (d02) também a imprime. */
    ch.setAttribute("data-alvo", "1");
    chips[MAT[m].n] = {el: ch, id: id, m: m};
    if(ST.resp[id] && postas[MAT[m].n])
      postas[MAT[m].n].forEach(function(k){ cels[k].className = "dcel achada"; });
    /* ⚠️ AS DUAS PONTAS SE DECLARAM (`cp-<id>-a` na primeira letra, `cp-<id>-z`
       na última) para o JOGADOR DA BANCA poder resolver esta folha. Sem elas ele
       dizia "não sei jogar esta peça" e saía como dívida — e foi exatamente por
       isso que o beco sem saída desta folha ficou no ar até o Marcos tropeçar
       nele na sala. Folha que o jogador não alcança é folha que ninguém mede.
       Só se a célula ainda não tiver dono: duas palavras podem cruzar numa
       ponta, e sobrescrever faria o jogador acusar de defeito uma folha boa. */
    var pp = postas[MAT[m].n];
    if(pp && pp.length){
      var ca = cels[pp[0]], cz = cels[pp[pp.length - 1]];
      if(ca && !ca.getAttribute("data-qa")) ca.setAttribute("data-qa", "cp-" + id + "-a");
      if(cz && !cz.getAttribute("data-qa")) cz.setAttribute("data-qa", "cp-" + id + "-z");
    }
    lista.appendChild(ch);
  });
  d.appendChild(lista); d.appendChild(dia);
  /* o traço: aperta numa letra, arrasta até a última, solta */
  var indo = null;
  function limpa(){ cels.forEach(function(c){ if(c.className === "dcel tracando") c.className = "dcel"; }); }
  function caminho(a, b){
    var ay = Math.floor(a / N), ax = a % N, by = Math.floor(b / N), bx = b % N, out = [], i;
    if(ay === by){ var p = Math.min(ax, bx), q = Math.max(ax, bx); for(i = p; i <= q; i++) out.push(ay * N + i); if(ax > bx) out.reverse(); return out; }
    if(ax === bx){ var r = Math.min(ay, by), s = Math.max(ay, by); for(i = r; i <= s; i++) out.push(i * N + ax); if(ay > by) out.reverse(); return out; }
    return null;
  }
  function conclui(cam){
    limpa();
    if(!cam) return;
    var w = cam.map(function(k){ return cels[k].textContent; }).join(""), ch = chips[w];
    if(!ch || ST.resp[ch.id]){ return; }
    cam.forEach(function(k){ cels[k].className = "dcel achada"; });
    ch.el.className = "pmat achada";
    acertou(ch.id, "certo" + pi + "_" + ch.m);
  }
  /* ⚠️⚠️ AS DUAS PORTAS ESTAVAM QUEBRADAS — E O MARCOS PEGOU NA SALA
     (15/set/2026): *"a atividade do diagrama, a número 9 não funciona"*. Eu já
     tinha MEDIDO este mesmo defeito no `_ort5b` no dia anterior e avisado que o
     código gêmeo estava aqui e no `_jogo1`; ficou esperando decisão, e quem
     pagou a espera foi a criança. Lição: código gêmeo com defeito medido se
     conserta na mesma rodada, nos três lugares.
     O que estava errado: o `pointerdown` zerava o começo do traço em TODA letra
     tocada. Com isso:
       · o toque-toque (primeira letra, última letra) nunca fechava — o segundo
         toque virava um novo começo;
       · o arrastar também não, porque quem fechava era o `onclick`, e num
         arrasto de A até Z o clique não cai em Z.
     Ou seja: a folha inteira era um beco sem saída.
     O conserto: o toque só COMEÇA se não houver começo, e o arrasto FECHA no
     `pointerup`, na letra em que o dedo parou. */
  var puloClique = false;
  function celDoPonto(ev){
    var e = document.elementFromPoint(ev.clientX, ev.clientY);
    while(e && e !== document.body){
      if(e._i !== undefined && e._i !== null) return e;
      e = e.parentNode;
    }
    return null;
  }
  function fecha(ate){
    conclui(caminho(indo, ate));
    indo = null; puloClique = true;
    setTimeout(function(){ puloClique = false; }, 80);
  }
  cels.forEach(function(c){
    c.addEventListener("pointerdown", function(ev){
      ev.preventDefault();
      if(indo !== null && indo !== c._i) return;   /* já há começo: este toque FECHA */
      indo = c._i; limpa(); c.className = "dcel tracando";
    });
    c.addEventListener("pointerenter", function(){
      if(indo === null) return;
      var cam = caminho(indo, c._i);
      limpa();
      if(cam) cam.forEach(function(k){ if(cels[k].className === "dcel") cels[k].className = "dcel tracando"; });
    });
    /* ⚠️ NO CELULAR o `pointerenter` não dispara ao arrastar (o ponteiro fica
       preso no primeiro alvo). Por isso o toque também fecha por TOQUE-TOQUE:
       primeira letra, última letra. Duas portas, sempre. */
    c.onclick = function(){
      if(puloClique) return;
      if(indo === null || indo === c._i){ indo = c._i; limpa(); c.className = "dcel tracando"; return; }
      fecha(c._i);
    };
  });
  document.addEventListener("pointerup", function(ev){
    if(indo === null) return;
    var c = celDoPonto(ev);
    if(c && c._i !== indo && caminho(indo, c._i)){ fecha(c._i); return; }
    limpa();
  });
}

/* ============ 10 — POR QUE É FEITA DESSE MATERIAL? ============
   Esta folha NÃO existe no pote — e é por isso que ela existe.
   Trinta folhas de "tipos de moradia" mostram iglu e palafita lado a lado e
   nenhuma pergunta o PORQUÊ. O 2º ano de Blumenau pede *"propor o uso de
   diferentes materiais... tendo em vista algumas propriedades desses materiais
   (flexibilidade, dureza, transparência etc.)"* — que é exatamente o porquê.
   ⚠️ As opções são FRASES, e frase não cabe em botão quadrado: `.op.frase` é
      largura cheia, alinhada à esquerda, para se LER. */
function f10(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Por que esta moradia é feita assim? Toque na <b>resposta certa</b>.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(figMor(k, id));
    var outros = [], j;
    for(j in MOR) if(j !== k && MOR[j].por !== MOR[k].por) outros.push(j);
    var lista = baralha([k].concat(pega(outros, 2))).map(function(m){
      return {v: m, rot: MOR[m].por, aria: MOR[m].por, fala: "por_" + m};
    });
    opcoes(box, pi, id, lista, k, "frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 11 — EM QUE LUGAR FICA CADA UMA? ============
   Da d09 (Minhas Atividades): *"dê onde são essas moradias"*.
   ⚠️ A FOLHA DE ORIGEM ERRA NA EXECUÇÃO: o comando é ótimo (é a habilidade A
      inteira) mas ela não oferece lugar nenhum para escolher — "onde" aceita
      "no Brasil", "na rua", "na foto". Aqui os lugares são seis, com a cena de
      cada um, e a criança escolhe entre três.
   ⭐ A partir daqui o caderno deixa de perguntar o NOME e passa a perguntar o
      LUGAR: é onde ele vira 2º ano. */
function f11(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Em que <b>lugar</b> a gente encontra esta moradia?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(figMor(k, id));
    var certo = MOR[k].lug, outros = [], j;
    for(j in LUG) if(j !== certo) outros.push(j);
    var lista = baralha([certo].concat(pega(outros, 2))).map(function(l){
      return {v: l, rot: img(LUG[l].f, "figop", LUG[l].n) + '<span class="rotop">' + LUG[l].n + "</span>",
              aria: LUG[l].n, fala: "lug_" + l};
    });
    opcoes(box, pi, id, lista, certo, "figbt", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 12 — POR QUE A CASA É ASSIM ALI? ============
   Segunda folha do bloco do LUGAR, um degrau acima: não é mais "onde fica", é
   "por que fica assim ali". A criança já tem o lugar; agora precisa amarrar o
   lugar ao jeito da casa. É a habilidade A escrita por extenso:
   *"reconhecer semelhanças e diferenças nos hábitos, nas relações com a natureza
   e no modo de viver de pessoas em diferentes lugares"*. */
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta moradia fica <b>neste lugar</b>. Por quê? Toque na resposta certa.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var par = el("div", "grelha");
    var a = el("div", "celmor"); a.innerHTML = img(k, "figop", "Uma moradia");
    var b = el("div", "celmor"); b.innerHTML = img(LUG[MOR[k].lug].f, "figop", LUG[MOR[k].lug].n);
    var rot = el("div", "alvonome cheia"); rot.setAttribute("data-alvo", "1");
    rot.textContent = LUG[MOR[k].lug].n; b.appendChild(rot);
    var lin = el("div", "chamlin");
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("perg12_" + k); }));
    a.appendChild(lin);
    par.appendChild(a); par.appendChild(b);
    box.appendChild(par);
    var outros = [], j;
    for(j in MOR) if(j !== k && MOR[j].por !== MOR[k].por) outros.push(j);
    var lista = baralha([k].concat(pega(outros, 2))).map(function(m){
      return {v: m, rot: MOR[m].por, aria: MOR[m].por, fala: "por_" + m};
    });
    opcoes(box, pi, id, lista, k, "frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 13 — ESTA CASA COMBINA COM ESTE LUGAR? ============
   O terceiro degrau do bloco, e o mais difícil: agora a criança JULGA. Alguns
   pares estão certos e outros não (uma casa de palha na terra do gelo), e ela
   precisa dizer sim ou não — que é o que mostra se entendeu ou se decorou.
   ⚠️ O sorteio GARANTE pelo menos dois pares errados (ver o remendo do
      `novaFolha` no index.html). Sem essa garantia, cinco "sim" seguidos
      ensinariam a criança a acertar sem olhar. */
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe a moradia e o lugar. Eles <b>combinam</b>?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(P, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var par = el("div", "grelha");
    var a = el("div", "celmor"); a.innerHTML = img(P.m, "figop", "Uma moradia");
    var b = el("div", "celmor"); b.innerHTML = img(LUG[P.l].f, "figop", LUG[P.l].n);
    var rot = el("div", "alvonome cheia"); rot.setAttribute("data-alvo", "1");
    rot.textContent = LUG[P.l].n; b.appendChild(rot);
    var lin = el("div", "chamlin");
    lin.appendChild(botaoSom("Ouvir esta dupla", function(){ falar("dupla_" + P.m + "_" + P.l); }));
    a.appendChild(lin);
    par.appendChild(a); par.appendChild(b);
    box.appendChild(par);
    var certo = P.ok ? "sim" : "nao";
    var lista = [{v: "sim", rot: "SIM, combina", aria: "Sim, combina", fala: "op_sim"},
                 {v: "nao", rot: "NÃO combina", aria: "Não combina", fala: "op_nao"}];
    opcoes(box, pi, id, lista, certo, "curta",
           "certo" + pi + "_" + P.m + "_" + certo, "dica" + pi + "_" + P.m);
    fechaItem(d, box, id);
  });
}

/* ============ 14 — QUAL FRASE EXPLICA A MORADIA? ============
   Da d04 (Pequeno Lobato): *"relacione a segunda coluna de acordo com a
   primeira"* — figura de um lado, FRASE QUE DEFINE do outro ("a palafita é uma
   casa construída sobre estacas de madeira"). Sobe o degrau do nome: não é mais
   reconhecer a palavra, é ler a explicação inteira e ver se ela serve. */
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Qual frase <b>explica</b> esta moradia? Leia as três com calma.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(figMor(k, id));
    var outros = [], j;
    for(j in MOR) if(j !== k) outros.push(j);
    var lista = baralha([k].concat(pega(outros, 2))).map(function(m){
      return {v: m, rot: MOR[m].def, aria: MOR[m].def, fala: "def_" + m};
    });
    opcoes(box, pi, id, lista, k, "frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 15 — COMPLETE A FRASE ============
   Da d23: *"complete as frases com as palavras do quadro"*. A lacuna obriga a
   LER a frase inteira — não dá para responder pela figura, porque não há figura.
   É o degrau simbólico do bloco (concreto → figural → simbólico). */
function f15(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leia a frase e toque na <b>palavra</b> que falta.", "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  var banco = pool.map(function(k){ return FRASES[k].r; });
  pool.forEach(function(k, i){
    var id = "n" + pi + "_" + i, F = FRASES[k], box = item(i + 1);
    var lin = el("div", "enunlin");
    var fr = el("div", "frasel");
    fr.appendChild(document.createTextNode(F.a));
    var lac = el("span", "lacuna" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? F.r : "______");
    lac.setAttribute("data-alvo", "1");
    fr.appendChild(lac);
    fr.appendChild(document.createTextNode(F.b));
    lin.appendChild(fr);
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("frase_" + k); }));
    box.appendChild(lin);
    var outras = banco.filter(function(w){ return w !== F.r; });
    var lista = baralha([F.r].concat(pega(outras, 2))).map(function(w){
      return {v: w, rot: w, aria: w, fala: "pal_" + w.toLowerCase()};
    });
    opcoes(box, pi, id, lista, F.r, "curta", "certo" + pi + "_" + k, "dica" + pi + "_" + k,
      function(){ lac.className = "lacuna cheia"; lac.textContent = F.r; });
    fechaItem(d, box, id);
  });
}

/* ============ 16 — A CRUZADINHA DAS CASAS ============
   Da d08 / d27: *"complete a cruzadinha"*, com as pistas por definição.
   ⚠️⚠️ DUAS PISTAS DA FOLHA DE ORIGEM FORAM REESCRITAS, e isto não é detalhe de
   estilo: ela diz *"casa de ciganos (tenda)"* e *"casa de índios (oca)"*. A
   habilidade D do 2º ano de Blumenau é *"reconhecendo a importância do respeito
   às diferenças"* — ensinar a palavra junto com o apelido é ensinar o contrário
   do que a rede pede. As pistas daqui estão no `PISTAS`, no index.html.
   ⚠️ E a folha de origem traz o GABARITO impresso ao lado de cada pista. Aqui a
      resposta só aparece quando a criança escreve.
   ⚠️ AS DUAS PORTAS: o teclado da tela E o teclado de verdade (`onkeydown`).
      No PC da escola tem teclado e a criança vai digitar; no celular, não tem. */
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque numa <b>pista</b>, escute e escreva a palavra na cruzadinha.",
            "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  /* a grade: a primeira palavra fica deitada e as outras se penduram nela pela
     letra que tiverem em comum. Se nenhuma letra bater, a palavra vai para uma
     linha livre embaixo — nunca some. */
  var mapa = {}, maxX = 0, maxY = 0, entradas = [];
  function poe(w, x, y, hor){
    var i;
    for(i = 0; i < w.length; i++){
      var cx = x + (hor ? i : 0), cy = y + (hor ? 0 : i);
      mapa[cx + "," + cy] = w.charAt(i);
      if(cx > maxX) maxX = cx;
      if(cy > maxY) maxY = cy;
    }
  }
  function cabe(w, x, y, hor){
    var i;
    /* ⚠️ AQUI HAVIA UM `if(x < 0 || y < 0) return false` — e ele quebrava a
       cruzadinha inteira (achado na foto, 13/set/2026). A primeira palavra
       entra em 0,0; qualquer palavra que cruze por uma letra ADIANTE da
       primeira letra dela cai em coordenada negativa, que é perfeitamente
       válida: a grade é normalizada no fim (`minX`/`minY`). Com a guarda, só
       cruzava quem tivesse a letra comum na posição 0 — e as outras iam para a
       "linha livre", soltas, sem cruzar nada. Cruzadinha sem cruzamento é lista
       de palavras com quadradinho. */
    for(i = 0; i < w.length; i++){
      var cx = x + (hor ? i : 0), cy = y + (hor ? 0 : i);
      var q = mapa[cx + "," + cy];
      if(q && q !== w.charAt(i)) return false;
      /* nada de palavra colada na outra em paralelo */
      if(!q){
        var a = hor ? mapa[cx + "," + (cy - 1)] : mapa[(cx - 1) + "," + cy];
        var b = hor ? mapa[cx + "," + (cy + 1)] : mapa[(cx + 1) + "," + cy];
        if(a || b) return false;
      }
    }
    var antes = hor ? mapa[(x - 1) + "," + y] : mapa[x + "," + (y - 1)];
    var dep = hor ? mapa[(x + w.length) + "," + y] : mapa[x + "," + (y + w.length)];
    return !antes && !dep;
  }
  var linhaLivre = 0;
  pool.forEach(function(k, n){
    var w = MOR[k].n.replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, ""), col = null;
    if(!entradas.length){ col = {x: 0, y: 0, hor: true}; }
    else {
      var i, j, achou = null;
      for(i = 0; i < w.length && !achou; i++)
        for(j = 0; j < entradas.length && !achou; j++){
          var E = entradas[j], p;
          for(p = 0; p < E.w.length; p++){
            if(E.w.charAt(p) !== w.charAt(i)) continue;
            var hor = !E.hor;
            var x = hor ? E.x - i : E.x + p;
            var y = hor ? E.y + p : E.y - i;
            if(cabe(w, x, y, hor)){ achou = {x: x, y: y, hor: hor}; break; }
          }
        }
      col = achou || {x: 0, y: maxY + 2 + (linhaLivre++), hor: true};
    }
    poe(w, col.x, col.y, col.hor);
    entradas.push({k: k, w: w, x: col.x, y: col.y, hor: col.hor, n: n + 1});
  });
  /* normaliza para não haver coordenada negativa */
  var minX = 0, minY = 0, key;
  for(key in mapa){
    var pxy = key.split(","), px = +pxy[0], py = +pxy[1];
    if(px < minX) minX = px;
    if(py < minY) minY = py;
  }
  var env = el("div", "cruzenv"), grade = el("div", "cruz");
  var larg = maxX - minX + 1, alt = maxY - minY + 1;
  grade.style.gridTemplateColumns = "repeat(" + larg + ",-webkit-max-content)";
  grade.style.gridTemplateColumns = "repeat(" + larg + ",max-content)";
  var celula = {};
  var yy, xx;
  for(yy = 0; yy < alt; yy++) for(xx = 0; xx < larg; xx++){
    var ch = mapa[(xx + minX) + "," + (yy + minY)];
    if(!ch){ grade.appendChild(el("span", "ccel")); continue; }
    var c = el("button", "ccel viva", "");
    c.setAttribute("aria-label", "Casa da cruzadinha");
    c._x = xx + minX; c._y = yy + minY;
    celula[c._x + "," + c._y] = c;
    grade.appendChild(c);
  }
  env.appendChild(grade); d.appendChild(env);
  var pistas = el("div", "pistas");
  entradas.forEach(function(E, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, E.w);
    E.id = id;
    E.cels = [];
    var t;
    for(t = 0; t < E.w.length; t++){
      var cc = celula[(E.x + (E.hor ? t : 0)) + "," + (E.y + (E.hor ? 0 : t))];
      E.cels.push(cc);
      if(t === 0 && cc && !cc.querySelector(".cn")) cc.appendChild(el("span", "cn", E.n));
    }
    if(ST.resp[id]) E.cels.forEach(function(c, t2){ if(c){ c.className = "ccel viva ok"; c.firstChild && 0; c.textContent = E.w.charAt(t2); if(t2 === 0) c.appendChild(el("span", "cn", E.n)); } });
    var p = el("button", "pista" + (ST.resp[id] ? " feita" : ""),
               '<span class="pn">' + E.n + ".</span><span>" + PISTAS[E.k].p + "</span>");
    p.setAttribute("data-qa", "item-" + id);
    p.setAttribute("aria-label", PISTAS[E.k].p);
    E.bt = p;
    p.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); falar("pista_" + E.k);
      abreCruz(E, pi);
    };
    pistas.appendChild(p);
    E.cels.forEach(function(c){
      if(!c) return;
      c.addEventListener("click", function(){ if(!ST.resp[id]) abreCruz(E, pi); });
    });
  });
  d.appendChild(pistas);
}
/* o teclado da cruzadinha: uma palavra por vez, letra a letra */
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
  /* ⚠️ Toque na casinha dispara o `onclick` da casinha E o da grade: a mesma
     palavra pede para abrir duas vezes. Se já está aberta, só devolve o foco —
     fechar e reabrir era o que apagava a letra e (antes do conserto acima)
     estourava. */
  if(CRUZ && CRUZ.E === E){ try{ TECIN && TECIN.focus(); }catch(e){} return; }
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
  /* ⚠️⚠️ LIÇÃO PAGA — "O ALUNO NÃO CONSEGUIA DIGITAR" (Marcos, 18/set/2026, na
     folha 8 d'A Fábrica de Nomes). Aqui estava `CRUZ = null; pintaCruz();` — e
     `pintaCruz` começa lendo `CRUZ.E`. Estourava TypeError toda vez que se
     fechava a caneta. Como a casinha E a grade tinham `onclick`, um toque na
     casinha chamava `abreCruz` duas vezes: a segunda fechava a primeira, o
     fecho estourava, e o `abreCruz` morria ANTES de reabrir. Resultado: a
     criança tocava, nada abria, digitava e nada acontecia — sem erro na tela.
     O jogador da banca não pegou porque clicava na GRADE (um `onclick` só);
     agora ele clica na CASINHA, como a criança. Aqui: pintar com o E guardado
     ANTES de zerar, e nunca ler CRUZ depois de zerá-lo. */
  if(!CRUZ) return;
  var E = CRUZ.E;
  if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista";
  CRUZ = null;
  if(TECIN){ TECIN.value = ""; try{ TECIN.blur(); }catch(e){} }
  limpaCruz(E);
}
function limpaCruz(E){
  (E && E.cels || []).forEach(function(c){
    if(!c || c.className.indexOf(" ok") > -1) return;
    var n = c.querySelector(".cn");
    c.textContent = ""; if(n) c.appendChild(n);
    c.className = "ccel viva";
  });
}
function pintaCruz(){
  if(!CRUZ) return;                       /* nunca ler CRUZ.E sem CRUZ */
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
  if(ch === "ap") CRUZ.val = CRUZ.val.slice(0, -1);
  else if(ch === "ok"){ confereCruz(); return; }
  else { if(CRUZ.val.length >= E.w.length) return; CRUZ.val += ch; }
  pintaCruz(); rolaParaCruz();
  if(CRUZ.val.length >= E.w.length) setTimeout(confereCruz, 380);
}
/* ---------- COM OU SEM ACENTO, AS DUAS VALEM ----------
   ⚠️ PEDIDO DO MARCOS (15/set/2026): *"na cruzadinha da atividade rua do mundo
      pode aceitar tanto com acento como sem, corrija"*. E ele está certo pelo
      conteúdo: esta é uma cruzadinha de GEOGRAFIA — o que está sendo medido é
      se a criança sabe que a casa sobre estacas se chama PALAFITA, não se ela
      acerta o acento. Um Ó recusado num caderno de moradia reprova a criança
      por uma coisa que a folha não ensina nem pergunta.
   ⚠️ E POR ISSO ISTO NÃO É REGRA DA CASA, é regra DESTE caderno: nos cadernos
      de ORTOGRAFIA (`_ort5`, `_ort5b`) o acento e o cedilha SÃO a matéria —
      aceitar CACA por CAÇA lá seria jogar a atividade inteira fora. Se um dia
      isto virar peça do motor, vem com uma chave por caderno, nunca ligada
      para todos.
   ⚠️ A GRADE CONTINUA MOSTRANDO A FORMA CERTA no acerto (`E.w`, com acento):
      aceitar sem acento é não castigar, não é ensinar errado. */
function semAcento(s){
  return String(s)
    .replace(/[ÁÀÂÃÄ]/g, "A").replace(/[ÉÈÊË]/g, "E").replace(/[ÍÌÎÏ]/g, "I")
    .replace(/[ÓÒÔÕÖ]/g, "O").replace(/[ÚÙÛÜ]/g, "U").replace(/Ç/g, "C");
}
function confereCruz(){
  if(!CRUZ || !CRUZ.val) return;
  var E = CRUZ.E, pi = CRUZ.pi;
  if(semAcento(CRUZ.val) === semAcento(E.w)){
    E.cels.forEach(function(c, i){
      if(!c) return;
      var n = c.querySelector(".cn");
      c.textContent = E.w.charAt(i); if(n) c.appendChild(n);
      c.className = "ccel viva ok";
    });
    E.bt.className = "pista feita";
    CRUZ = null;
    if(TECIN){ TECIN.value = ""; try{ TECIN.blur(); }catch(e){} }
    acertou(E.id, "certo" + pi + "_" + E.k);
  } else {
    CRUZ.val = ""; pintaCruz();
    errou(E.id, "dica" + pi + "_" + E.k);
  }
}

/* ============ 17 — ESTA CASA VISTA DE CIMA ============
   ⚠️ NENHUMA DAS TRINTA FOLHAS COLHIDAS FAZ ISTO — e é a única habilidade do 2º
   ano de Blumenau que traz a palavra *moradia* escrita dentro dela:
   *"identificar objetos e lugares de vivência (escola e moradia) em imagens
   aéreas e mapas (visão vertical) e fotografias (visão oblíqua)"*.
   A criança vê a moradia de lado — como ela conhece — e escolhe qual das três
   figuras é a MESMA moradia vista lá de cima. */
/* ============ 17 — A MESMA COISA VISTA DE CIMA ============
   Primeira folha do bloco da VISÃO VERTICAL. A criança vê a coisa do jeito que
   ela conhece (de frente, ou de cima e de lado) e escolhe, entre três figuras de
   cima, qual é a MESMA coisa.
   ⚠️ As três opções são todas vistas de cima — se só uma fosse, dava para
      acertar sem olhar o objeto. E a resposta é sempre um par que existe de
      verdade na folha de origem (ver o comentário do `CIMA` no index.html). */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta é a coisa vista por fora. Qual destas é <b>ela mesma vista " +
            "de cima</b>? Isso se chama <b>visão vertical</b>.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, C = CIMA[k], box = item(i + 1);
    registra(id, pi, C.n + " de cima");
    var cab = el("div", "celmor");
    cab.innerHTML = img(C.mostra, "figop", C.n);
    box.appendChild(cab);
    var outros = [], j;
    for(j in CIMA) if(j !== k) outros.push(j);
    var lista = baralha([k].concat(pega(outros, 2))).map(function(m){
      return {v: m, rot: img(CIMA[m].cima, "figop", "Uma vista de cima"),
              aria: "Uma vista de cima", fala: "vistacima"};
    });
    opcoes(box, pi, id, lista, k, "figbt", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 18 — ACHE NA PRAÇA VISTA DE CIMA ============
   A mesma habilidade B, agora num desenho de verdade visto de cima: a praça da
   folha do Colégio Dinâmico, com a legenda dela (árvore, fonte, banco,
   bebedouro). A pergunta impressa é *"que elementos existem na praça?"*; aqui a
   criança não escreve a lista — ela ACHA cada um no desenho.
   ⚠️ AS COORDENADAS SÃO MEDIDAS NA FIGURA, não chutadas, e cada elemento tem
      TODOS os pontos dele (ver o comentário do `MAPA` no index.html). Alvo no
      lugar errado faz a criança que acertou levar erro — e ela não tem como
      saber que o errado era o app. */
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta é uma <b>praça vista de cima</b>. Ache o que a folha pedir.",
            "p" + pi + "enun");
  var cx = el("div", "aerea");
  cx.innerHTML = img(MAPA.figura, "", "Uma praça vista de cima");
  var pontos = {};
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, A = MAPA.alvos[k];
    registra(id, pi, A.n);
    pontos[k] = {els: [], id: id, k: k};
    A.pts.forEach(function(P, j){
      var b = el("button", "ponto" + (ST.resp[id] ? " certo" : ""));
      b.style.left = P.x + "%"; b.style.top = P.y + "%";
      b.setAttribute("aria-label", "Um lugar da praça");
      b.setAttribute("data-qa", "ponto-" + k + "-" + j);
      pontos[k].els.push(b);
      cx.appendChild(b);
    });
  });
  d.appendChild(cx);
  /* os pedidos, um por vez: a criança lê (e ouve) e toca no desenho */
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, A = MAPA.alvos[k], box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Ache <b>" + A.n + "</b> na praça."));
    lin.appendChild(botaoSom("Ouvir a pista", function(){ falar("mapa_" + k); }));
    box.appendChild(lin);
    box.appendChild(el("div", "ajuda", ST.resp[id] ? "Achou!" : "Toque na praça lá em cima."));
    fechaItem(d, box, id);
  });
  var j;
  for(j in pontos){
    (function(P){
      P.els.forEach(function(b){
        b.onclick = function(){
          if(ST.resp[P.id]) return;
          sPasso();
          P.els.forEach(function(o){ o.className = "ponto certo"; });
          acertou(P.id, "certo" + pi + "_" + P.k);
        };
      });
    })(pontos[j]);
  }
  /* tocar no lugar errado responde — e diz o que olhar, nunca "errou" */
  cx.addEventListener("click", function(ev){
    if(ev.target !== cx && ev.target.tagName !== "IMG") return;
    var k2, falta = null;
    for(k2 in pontos) if(!ST.resp[pontos[k2].id]){ falta = pontos[k2]; break; }
    if(!falta) return;
    sErro(); tentativa(falta.id, false);
    falar("mapadica_" + falta.k);
  });
}

/* ============ 19 — FRONTAL, VERTICAL OU OBLÍQUA? ============
   O fecho do bloco: a mesma caneca e o mesmo carro aparecem nos três pontos de
   vista, misturados, e a criança classifica. É aqui que "de cima" deixa de ser
   um truque de uma folha e vira uma palavra que ela leva para o livro.
   ⚠️ AS PALAVRAS SÃO AS DA REDE — visão frontal, vertical e oblíqua —, e a
      definição de cada coluna é a da folha do Pequeno Lobato, copiada palavra
      por palavra. O menino do livro didático aparece em cima da coluna: é o
      desenho que explica de onde se olha, sem precisar ler.
   ⚠️ AS DUAS PORTAS: arrastar a figura até a coluna (PC) ou tocar na figura e
      depois na coluna (celular). */
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "De que jeito a figura foi tirada? Ponha cada uma na coluna certa.",
            "p" + pi + "enun");
  var cols = el("div", "colunas"), caixas = {}, k;
  for(k in VISTAS){
    (function(vk){
      var c = el("div", "coluna");
      var t = el("div", "ctit", VISTAS[vk].n);
      t.setAttribute("data-alvo", "1");
      var som = botaoSom("Ouvir o que é " + VISTAS[vk].n, function(){ falar("vista_" + vk); });
      t.appendChild(som);
      c.appendChild(t);
      /* o menino mostrando de onde se olha. ⚠️ A COLUNA FRONTAL FICA COM A CAIXA
         VAZIA, e não sem caixa: o livro só desenha o menino nas duas outras
         visões, e eu não vou apontar o desenho dele para uma visão que o livro
         não nomeou assim. Sem a caixa vazia as três colunas começavam a receber
         figura em alturas diferentes. */
      var ol = el("div", "colho");
      if(VISTAS[vk].olho){
        ol.innerHTML = img(VISTAS[vk].olho, "figolho", "De onde o menino olha");
        ol.setAttribute("data-alvo", "1");
      }
      c.appendChild(ol);
      var dentro = el("div", "cdentro");
      c.appendChild(dentro);
      c._v = vk; c._dentro = dentro;
      caixas[vk] = c;
      cols.appendChild(c);
    })(k);
  }
  d.appendChild(cols);
  var banco = el("div", "figbanco"), marcada = null, listaC = [];
  for(k in caixas) listaC.push(caixas[k]);
  ST.folha["p" + pi].forEach(function(fk, i){
    var id = "n" + pi + "_" + i, V = VISTA[fk];
    registra(id, pi, VISTAS[V.v].n);
    var b = el("button", "op fig" + (ST.resp[id] ? " usada" : ""),
               img(V.f, "figmini", V.n));
    b.setAttribute("aria-label", V.n);
    b.setAttribute("data-qa", "item-" + id);
    if(ST.resp[id]) caixas[V.v]._dentro.appendChild(el("span", "fdentro", V.n));
    function larga(col){
      if(ST.resp[id]) return;
      if(col._v === V.v){
        b.className = "op fig usada";
        col._dentro.appendChild(el("span", "fdentro", V.n));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + fk);
      } else {
        col.className = "coluna erro";
        setTimeout(function(){ col.className = "coluna"; }, 500);
        errou(id, "dica" + pi + "_" + fk);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("fig_" + fk);
      if(marcada === b){ b.className = "op fig"; marcada = null; return; }
      if(marcada) marcada.className = "op fig";
      b.className = "op fig marcada"; marcada = b;
    };
    puxavel(b, listaC, function(col){ larga(col); });
    banco.appendChild(b);
  });
  listaC.forEach(function(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_figura"); return; }
      marcada._larga(col);
    };
  });
  d.appendChild(banco);
}

/* ============ 20 — COMO ERA ANTES, COMO É HOJE ============
   ⚠️ TAMBÉM NÃO EXISTE NO POTE. Trinta folhas de moradia e nenhuma tem TEMPO.
   A habilidade C do 2º ano é *"analisar mudanças e permanências, comparando
   imagens de um mesmo lugar em diferentes tempos, tendo como referência o
   espaço vivido, relacionar as mudanças as ações humanas"*.
   O gesto: as duas fotos do MESMO lugar chegam embaralhadas e a criança põe
   cada uma no seu tempo. O item só fecha quando as duas estão no lugar. */
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As duas figuras são do <b>mesmo lugar</b>, em tempos diferentes. " +
            "Ponha cada uma no seu lugar.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, T = TEMPO[k], box = item(i + 1);
    registra(id, pi, "antes e hoje de " + T.n);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Aqui é <b>" + T.n + "</b>."));
    lin.appendChild(botaoSom("Ouvir o que mudou", function(){ falar("tempo_" + k); }));
    box.appendChild(lin);
    var trilha = el("div", "trilhaord"), slots = {}, feito = !!ST.resp[id];
    ["antes", "hoje"].forEach(function(q){
      var s = el("div", "slot" + (feito ? " cheia" : ""));
      s.setAttribute("data-alvo", "1");
      s.innerHTML = '<span class="sn">' + (q === "antes" ? "ANTES" : "HOJE") + "</span>";
      if(feito){
        s.innerHTML += img(T[q], "figmini", "");
      }
      s._q = q; slots[q] = s; trilha.appendChild(s);
    });
    box.appendChild(trilha);
    var banco = el("div", "figbanco"), postos = 0, marcada = null;
    var listaS = [slots.antes, slots.hoje];
    if(!feito) baralha(["antes", "hoje"]).forEach(function(q){
      var b = el("button", "op fig", img(T[q], "figmini", ""));
      b.setAttribute("aria-label", q === "antes" ? "Uma figura" : "Outra figura");
      b.setAttribute("data-qa", "tempo-" + k + "-" + q);
      function larga(s){
        if(ST.resp[id] || b.className.indexOf("usada") > -1) return;
        if(s._q === q){
          s.className = "slot cheia"; s.innerHTML = '<span class="sn">' +
            (q === "antes" ? "ANTES" : "HOJE") + "</span>" + img(T[q], "figmini", "");
          b.className = "op fig usada";
          if(marcada === b) marcada = null;
          sCerto(); postos++;
          if(postos === 2) acertou(id, "certo" + pi + "_" + k);
          else { tentativa(id, false); ST.tent[id].erros--; falar("boa_metade"); }
        } else {
          s.className = "slot"; errou(id, "dica" + pi + "_" + k);
          setTimeout(function(){ s.className = "slot"; }, 400);
        }
      }
      b._larga = larga;
      b.onclick = function(){
        if(b._arrastou){ b._arrastou = false; return; }
        sPasso(); falar("fig_" + T[q]);
        if(marcada === b){ b.className = "op fig"; marcada = null; return; }
        if(marcada) marcada.className = "op fig";
        b.className = "op fig marcada"; marcada = b;
      };
      puxavel(b, listaS, function(s){ larga(s); });
      banco.appendChild(b);
    });
    listaS.forEach(function(s){
      s.onclick = function(){
        if(!marcada){ sPasso(); falar("toque_figura"); return; }
        marcada._larga(s);
      };
    });
    box.appendChild(banco);
    /* ⚠️ O CRÉDITO DA FOTO FICA NA TELA, embaixo do par. Só o par de Copacabana
       tem: as outras figuras são desenho de folha de professor. */
    if(T.cred) box.appendChild(el("div", "credito", T.cred));
    fechaItem(d, box, id);
  });
}

/* ============ 21 — QUEM ENTRA PRIMEIRO NA OBRA ============
   Da d11, questão 5: *"enumere as cenas abaixo na sequência correta da
   construção da moradia"*. No papel a criança escreve 1, 2, 3, 4 nos
   quadradinhos; aqui ela LEVA cada um para o seu lugar na fila.
   ⚠️ A fila é de PROFISSIONAIS, e a ordem é a que dá para defender — ver o
      comentário do `OBRA` no index.html. */
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Em que <b>ordem</b> eles trabalham na casa? Ponha cada um na fila.",
            "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  var trilha = el("div", "trilhaord"), slots = [], listaS = [];
  pool.forEach(function(_, i){
    var s = el("div", "slot"); s.setAttribute("data-alvo", "1");
    s.innerHTML = '<span class="sn">' + (i + 1) + "º</span>";
    s._i = i + 1; slots.push(s); listaS.push(s); trilha.appendChild(s);
  });
  d.appendChild(trilha);
  var banco = el("div", "figbanco"), marcada = null;
  pool.forEach(function(k, i){
    var id = "n" + pi + "_" + i, O = OBRA[k];
    registra(id, pi, O.n);
    if(ST.resp[id]){
      var s0 = slots[O.i - 1];
      s0.className = "slot cheia";
      s0.innerHTML = '<span class="sn">' + O.i + "º</span>" + img(O.f, "figmini", "") +
                     '<span class="rot">' + O.n + "</span>";
    }
  });
  baralha(pool.slice(0)).forEach(function(k){
    var i = pool.indexOf(k), id = "n" + pi + "_" + i, O = OBRA[k];
    if(ST.resp[id]) return;
    var b = el("button", "op fig", img(O.f, "figmini", ""));
    b.setAttribute("aria-label", "Um profissional da obra");
    b.setAttribute("data-qa", "item-" + id);
    function larga(s){
      if(ST.resp[id]) return;
      if(s._i === O.i){
        s.className = "slot cheia";
        s.innerHTML = '<span class="sn">' + O.i + "º</span>" + img(O.f, "figmini", "") +
                      '<span class="rot">' + O.n + "</span>";
        b.className = "op fig usada";
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + k);
      } else {
        s.className = "slot"; errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      sPasso(); falar("obra_" + k);
      if(marcada === b){ b.className = "op fig"; marcada = null; return; }
      if(marcada) marcada.className = "op fig";
      b.className = "op fig marcada"; marcada = b;
    };
    puxavel(b, listaS, function(s){ larga(s); });
    banco.appendChild(b);
  });
  listaS.forEach(function(s){
    s.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_cena"); return; }
      marcada._larga(s);
    };
  });
  d.appendChild(banco);
}

/* ============ 22 — QUEM FAZ O QUÊ NA OBRA ============
   Da d02 (*"enumere a segunda coluna com os profissionais que realizam a
   construção de uma moradia"*), da d06 e da d11, questão 3.
   ⚠️ Segunda folha de LIGAR do caderno — a posição 22 está declarada lá em cima,
      na constante `LIGAR`, junto com a 8. */
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque no <b>profissional</b> e depois no que ele faz na obra.",
            "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: img(k, "", PROF[k].n) + '<span class="rotop">' + PROF[k].n + "</span>",
            dir: PROF[k].t,
            ariaE: PROF[k].n, ariaD: PROF[k].t,
            fe: "prof_" + k, fd: "tarefa_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 23 — CADA COISA NO SEU CÔMODO ============
   Da d11, questão 4: *"ligue cada objeto para o cômodo da casa correto"*, e da
   d16 (*"quantos cômodos a sua casa possui?"*).
   ⚠️ Isto é apoio de 1º ano dentro de um caderno de 2º, e está declarado assim:
      a casa por dentro é o que a criança conhece de cor, e é a ponte para o
      fecho, onde ela monta a rua. */
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Em que <b>cômodo</b> da casa fica cada coisa?", "p" + pi + "enun");
  var cols = el("div", "colunas"), caixas = {}, listaC = [], k;
  for(k in COMODO){
    (function(ck){
      var c = el("div", "coluna");
      var t = el("div", "ctit", COMODO[ck].n);
      t.setAttribute("data-alvo", "1");
      t.appendChild(botaoSom("Ouvir " + COMODO[ck].n, function(){ falar("comodo_" + ck); }));
      c.appendChild(t);
      var dentro = el("div", "cdentro"); c.appendChild(dentro);
      c._c = ck; c._dentro = dentro;
      caixas[ck] = c; listaC.push(c); cols.appendChild(c);
    })(k);
  }
  d.appendChild(cols);
  var banco = el("div", "figbanco"), marcada = null;
  ST.folha["p" + pi].forEach(function(ok, i){
    var id = "n" + pi + "_" + i, O = OBJ[ok];
    registra(id, pi, COMODO[O.c].n);
    var b = el("button", "op fig" + (ST.resp[id] ? " usada" : ""), img(ok, "figmini", O.n));
    b.setAttribute("aria-label", O.n);
    b.setAttribute("data-qa", "item-" + id);
    if(ST.resp[id]) caixas[O.c]._dentro.appendChild(el("span", "fdentro", O.n));
    function larga(col){
      if(ST.resp[id]) return;
      if(col._c === O.c){
        b.className = "op fig usada";
        col._dentro.appendChild(el("span", "fdentro", O.n));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + ok);
      } else {
        col.className = "coluna erro";
        setTimeout(function(){ col.className = "coluna"; }, 500);
        errou(id, "dica" + pi + "_" + ok);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("obj_" + ok);
      if(marcada === b){ b.className = "op fig"; marcada = null; return; }
      if(marcada) marcada.className = "op fig";
      b.className = "op fig marcada"; marcada = b;
    };
    puxavel(b, listaC, function(col){ larga(col); });
    banco.appendChild(b);
  });
  listaC.forEach(function(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_objeto"); return; }
      marcada._larga(col);
    };
  });
  d.appendChild(banco);
}

/* ============ 24 — ACHE AS CASAS DENTRO DO POEMA ============
   Da d19: *"pinte no poema os tipos de moradias"*. O gesto é marca-texto: achar
   a palavra DENTRO de um texto corrido, que é diferente de achá-la numa lista.
   ⚠️ O POEMA É NOSSO. A folha de origem usa "O melhor lugar do mundo", de Noele
      Belger, e a d17 usa "A Casa", de Vinicius de Moraes — copiar o texto delas
      seria pegar o trabalho de outra pessoa. Este foi escrito para a folha, com
      o mesmo serviço e com o fecho da habilidade D: *"a casa do outro também é
      lugar"*. */
function f24(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque em <b>todas as moradias</b> escondidas no poema.", "p" + pi + "enun");
  var cx = el("div", "poema");
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "enun", "<b>" + POEMA.titulo + "</b>"));
  lin.appendChild(botaoSom("Ouvir o poema", function(){ falar("poema"); }));
  d.appendChild(lin);
  var alvo = {}, pos = {};
  ST.folha["p" + pi].forEach(function(w, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, w.replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, ""));
    alvo[w] = id;
  });
  var placar = el("div", "placar", "");
  function conta(){
    var n = 0, w;
    for(w in alvo) if(ST.resp[alvo[w]]) n++;
    placar.textContent = "Achou " + n + " de " + ST.folha["p" + pi].length + ".";
  }
  POEMA.versos.forEach(function(v){
    var p = el("div", "");
    v.forEach(function(w){
      var id = alvo[w];
      var b = el("button", "pw" + (id && ST.resp[id] ? " achada" : ""), w);
      b.setAttribute("aria-label", w);
      if(id){ b.setAttribute("data-qa", "item-" + id);
        /* ⚠️ ALVO DECLARADO: achar a palavra DENTRO do texto é a tarefa —
           o poema tem de estar escrito, senão não há onde procurar. */
        b.setAttribute("data-alvo", "1"); }
      b.onclick = function(){
        sPasso();
        if(id){
          if(ST.resp[id]) return;
          b.className = "pw achada";
          conta();
          acertou(id, "certo" + pi);
          return;
        }
        /* palavra que não é moradia: responde, mas não conta erro contra a
           criança em item nenhum — ela está LENDO, e ler não é errar */
        b.className = "pw nao";
        setTimeout(function(){ b.className = "pw"; }, 400);
        sErro(); falar("naoemoradia");
      };
      p.appendChild(b);
      p.appendChild(document.createTextNode(" "));
    });
    cx.appendChild(p);
  });
  cx.appendChild(el("span", "aut", "poema da Rua do Mundo"));
  d.appendChild(cx);
  conta();
  d.appendChild(placar);
}

/* ============ 25 — A RUA DO MUNDO (o fecho com gancho) ============
   Da d15, d21 e d28, que fecham pedindo *"desenhe a sua casa"* — gesto que a
   folha viva não tem. O que ela tem é MONTAR: a criança escolhe as moradias que
   quer na rua dela e a rua se desenha embaixo, com as casas lado a lado.
   ⭐ É a habilidade F (*"identificar e elaborar diferentes formas de
      representação... para representar componentes da paisagem dos lugares de
      vivência"*) e é o "quero mais": ela sai da atividade com uma rua onde o
      iglu é vizinho da oca. */
function f25(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escolha as moradias que você quer na <b>sua rua</b>. " +
            "Pode escolher quantas quiser.", "p" + pi + "enun");
  var rua = el("div", "rua");
  function pintaRua(){
    rua.innerHTML = "";
    var n = 0, i;
    ST.folha["p" + pi].forEach(function(k, j){
      if(ST.resp["n" + pi + "_" + j]){ rua.innerHTML += img(k, "", MOR[k].n); n++; }
    });
    if(!n) rua.appendChild(el("span", "ajuda", "a sua rua ainda está vazia…"));
  }
  var mural = el("div", "mural");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, MOR[k].n);
    var c = el("button", "cartaocasa" + (ST.resp[id] ? " escolhido" : ""),
               img(k, "figop", MOR[k].n) + '<span class="rotop">' + MOR[k].n + "</span>");
    c.setAttribute("aria-label", MOR[k].n);
    c.setAttribute("data-qa", "item-" + id);
    /* ⚠️ ALVO DECLARADO: aqui não há resposta certa nem errada — a criança
       escolhe as casas da rua dela, e o nome tem de estar à vista. */
    c.setAttribute("data-alvo", "1");
    c.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); c.className = "cartaocasa escolhido";
      pintaRua();
      acertou(id, "certo" + pi + "_" + k);
    };
    mural.appendChild(c);
  });
  d.appendChild(mural);
  d.appendChild(el("div", "ajuda", "A sua rua:"));
  d.appendChild(rua);
  pintaRua();
}

/* ---------- LIGAR: as duas colunas e o traço ----------
   ⭐ O TRAÇO é uma CURVA suave — sai na horizontal de cada caixa e vira no meio,
   como o cabo de um painel — com um halo branco por baixo (para não sumir ao
   passar por cima de outra caixa) e um pontinho cheio em cada ponta.
   ⚠️ AS DUAS COLUNAS TÊM A MESMA CAIXA (altura fixa e igual). Com `min-height`,
   a da esquerda crescia com a figura e a da direita ficava no mínimo: duas
   alturas diferentes lado a lado, e o Marcos pegou isso na tela. */
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
  /* ⚠️⚠️ PERDER O FOCO NÃO FECHA MAIS A PALAVRA (18/set/2026). Aqui havia um
     `blur -> fechaCruz()`. Medido no navegador com o gesto da criança: ela toca
     na casinha, toca em "Ouvir a frase" para escutar de novo (o que a folha
     CONVIDA a fazer) e o foco vai para o botão — a palavra fechava, e o que ela
     digitava em seguida caía no vazio. No PC a digitação nem precisa do foco
     (o teclado é ouvido no documento); no celular, tocar de novo na casinha
     devolve o foco e reabre o teclado do aparelho. Então o blur não faz nada. */
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
  if(document.activeElement && document.activeElement.id === "nomeIn") return;
  var k = (ev.key || "").toUpperCase();
  /* ⭐ DIGITAR SEM TER CLICADO ABRE A PRIMEIRA PALAVRA VAZIA DA FOLHA
     (18/set/2026). A criança do 5º ano vê as casinhas e começa a digitar —
     nada dizia "toque nas casinhas primeiro". As DUAS PORTAS valem para o
     gesto também: no PC, o teclado tem de funcionar sem clique. */
  if(!CRUZ && k.length === 1 && "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ".indexOf(k) > -1){
    var alvo = null, todos = document.querySelectorAll('.pagina.viva [data-qa^="esc-"]');
    for(var i = 0; i < todos.length && !alvo; i++){
      var idq = todos[i].getAttribute("data-qa").slice(4);
      if(!ST.resp[idq]) alvo = todos[i];
    }
    if(alvo){ alvo.click(); }
  }
  if(!CRUZ) return;
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
/* ⭐⭐ O FECHO A QUALQUER MOMENTO.
   O Marcos fixou a sequência em no mínimo 25 folhas, e a medida deu razão a ele:
   é o que enche os 55 min da criança RÁPIDA. Só que a criança DEVAGAR leva bem
   mais nas mesmas 25 folhas — ela não termina. Se o boletim, o parecer e a
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
    est += '<img src="img/mo_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você começou a reparar que cada lugar pede uma casa diferente — e isso é o principal!";
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
   ordem, mudam aqui e no `curriculo.json`, no mesmo commit. */
var OBJETIVOS = [
  {n: "Entender para que serve uma moradia", f: [1],
   ok: "sabe dizer para que serve uma casa e o que ela precisa ter",
   nao: "ainda não separa o que uma casa serve do que ela não serve"},
  {n: "Reconhecer e nomear os tipos de moradia", f: [2, 3, 4, 5],
   ok: "reconhece e nomeia oca, palafita, iglu, tenda, prédio e sobrado",
   nao: "ainda troca os nomes das moradias entre si"},
  {n: "Identificar de que material a moradia é feita", f: [6, 7, 8, 9],
   ok: "olha a moradia e diz de que material ela é feita",
   nao: "ainda não liga a moradia ao material dela"},
  {n: "Explicar por que a moradia é feita daquele jeito", f: [10, 12, 13, 14],
   ok: "explica por que cada casa é feita assim, e não de outro jeito",
   nao: "ainda decora o nome sem explicar o porquê"},
  {n: "Relacionar a moradia ao lugar onde ela fica", f: [11, 15, 16],
   ok: "sabe em que lugar cada moradia aparece, e por quê",
   nao: "ainda não relaciona a casa ao lugar dela"},
  {n: "Reconhecer a visão frontal, a vertical e a oblíqua", f: [17, 18, 19],
   ok: "reconhece a mesma coisa na visão frontal, na vertical e na oblíqua",
   nao: "ainda não reconhece as coisas vistas de cima"},
  {n: "Comparar como era antes e como é hoje, e quem constrói", f: [20, 21, 22, 23],
   ok: "compara o mesmo lugar em dois tempos e conhece quem faz a obra",
   nao: "ainda não compara o antes e o depois do mesmo lugar"},
  {n: "Achar as moradias no poema e montar a rua do mundo", f: [24, 25],
   ok: "acha as moradias dentro de um texto e monta a própria rua",
   nao: "ainda não achou as moradias dentro do poema"}
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
    parecer += "está começando a perceber que cada lugar pede uma casa diferente. Nenhum " +
      "objetivo chegou a 75% de acerto de primeira — vale retomar ORALMENTE, olhando com " +
      "a turma as casas do caminho da escola e perguntando de que elas são feitas, antes " +
      "de voltar à tela.";
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
    "<p class='comonota'><b>O que este caderno NÃO mede:</b> quatro das folhas de papel que " +
    "deram origem a ele pedem <b>desenhar a própria casa</b>, e a tela não tem onde desenhar. " +
    "Vale pedir esse desenho no caderno de papel depois — é ali que a criança conta onde ela " +
    "mora, e nenhuma tela substitui isso.</p>";
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
