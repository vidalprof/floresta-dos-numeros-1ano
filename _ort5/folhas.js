/* ============================================================
   O CASO DOS SONS IGUAIS — as vinte e três folhas.

   Cada folha nasceu de um VERBO impresso numa folha real de 5º ano. O crivo,
   fonte a fonte, com o comando VERBATIM e o motivo da única recusa, está em
   `_sequencias/POTE-ORTO5.md`. Nenhuma mecânica foi escolhida do nosso
   cardápio: o papel é que manda — e, onde o papel não alcançava o que a
   professora pediu (ler e interpretar gêneros), quem mandou foi o currículo da
   rede, e isso está DECLARADO folha por folha aqui embaixo.

   ⚠️ A POSIÇÃO É A IDENTIDADE: a folha da posição 7 usa o pote `p7`, grava os
      ids `n7_*` e fala `p7enun`. Não há segunda lista para desencontrar — isso
      já fez o relatório sair ZERO com a folha inteira respondida.
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI — são as únicas cujos ids não nascem
   de `n<pi>_`, e sim dentro do `montaLigar` (`l<pi>g<i>_<chave>`). Guardar um
   número onde há duas posições faria uma folha sumir do relatório sem erro
   nenhum na tela. */
var LIGAR = [12, 13];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou (o ouvido · as gavetas do som · o detetive · as regras · os gêneros ·
   usar · o cartaz) */
var CORES = ["c1","c1","c1", "c2","c2","c2", "c3","c3", "c4","c4","c4",
             "c5","c5", "c3","c3","c3","c3","c3", "c2","c2","c1","c1", "c4"];

function faixa(d, i, titulo){ d.appendChild(el("div", "faixa", '<div class="num">' + i + '</div><h2>' + titulo + '</h2>')); }
function aoAbrir(d, fn){ if(!d._aoAbrir) d._aoAbrir = []; d._aoAbrir.push(fn); }
/* ---------- O ALTO-FALANTE ----------
   Regra da casa: tudo o que a criança PRECISA LER tem que poder ser OUVIDO.
   ⚠️ E NESTE CADERNO ELE NÃO É APOIO: É A TAREFA. A folha 9 pergunta se a
      palavra leva H, e o H não tem som — se a criança não puder OUVIR a
      palavra, ela não tem como nem começar. O desenho do botão é CSS puro:
      nada de emoji (vira quadradinho nos PCs da escola). */
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
/* ⚠️⚠️ A PALAVRA INTEIRA NÃO PODE APARECER ANTES DA RESPOSTA — e num caderno de
   ORTOGRAFIA isso é a atividade toda. Se `PADARIA` estiver escrito dois
   centímetros acima de `PA_ARIA`, a criança copia a letra e a folha mede zero.
   A palavra não some: fica INVISÍVEL (`visibility`, para o espaço ficar
   guardado e a folha não pular) e aparece no instante do acerto. É o mesmo
   defeito que o `_qa/resposta_impressa.py` mede. */
function nomeSecreto(txt, id){
  var b = el("b", "segredo" + (ST.resp[id] ? " revelado" : ""), txt);
  b.setAttribute("data-nome", id);
  return b;
}
/* a palavra com a lacuna, grande, com o alto-falante ao lado e a inteira guardada */
function palavraLac(k, id){
  var L = LAC[k], c = el("div", "figsil");
  c.appendChild(el("div", "pgrande", L.m.replace("_", '<i class="lacuna"></i>')));
  var lin = el("div", "chamlin");
  lin.appendChild(nomeSecreto(L.p, id));
  lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
  c.appendChild(lin);
  return c;
}

/* ⚠️ O SLUG DA PALAVRA DO QUADRO MORA AQUI, e em nenhum outro lugar. Ele
   aparece em TRÊS sítios (o `data-qa` do botão, a chave da fala e a resposta
   declarada do item) e antes estava escrito à mão em cada um. Em IMPORTÂNCIA o
   resultado é "importncia" — o Â some, porque não é a-z —, e bastava um dos
   três escrever "importancia" para aquele botão ficar mudo sem erro nenhum na
   tela. Uma fonte só. */
function chaveQuadro(w){ return String(w).toLowerCase().replace(/[^a-z]/g, ""); }

function monta(){
  livro.innerHTML = ""; PAGEL = []; RESP = {}; TIRAS = [];
  var caps = [f0,
    f01, f02, f03,                    /*  1-3  o ouvido: a letra que falta      */
    f04, f05, f06,                    /*  4-6  as gavetas de cada som           */
    f07, f08,                         /*  7-8  o detetive circula a certa       */
    f09, f10, f11,                    /*  9-11 as regras que se explicam        */
    f12, f13,                         /* 12-13 amarrar erro, certo e regra      */
    f14, f15, f16, f17, f18,          /* 14-18 ler gêneros e achar o erro neles */
    f19, f20, f21, f22,               /* 19-22 usar: reescrever, completar...   */
    f23], i;                          /* 23    o cartaz do detetive              */
  for(i = 0; i < caps.length; i++){
    var d = el("div", "pagina" + (i > 0 ? " " + CORES[i - 1] : "")); d.setAttribute("data-pag", i);
    caps[i](d, i);
    if(i > 0) d.appendChild(el("div", "carimbo", "FOLHA<br>PRONTA"));
    livro.appendChild(d); PAGEL.push(d);
  }
}

/* ---------- capa ----------
   A capa não é enfeite: é a primeira coisa que a criança vê, e é ela que diz
   "isto aqui é um lugar bom". O tema sai do problema: existem letras DIFERENTES
   que fazem o MESMO som, e é por isso que a gente erra. O detetive é quem
   investiga esses casos.
   ⚠️ CAPA CLONADA = TROCAR A CENA, SEMPRE. Numa capa herdada desta casa ficou um
      `img("sapo")` de outra atividade: o app abria com um quadradinho vazio e um
      404 no console, e nenhum portão de texto viu. Esta capa não usa figura
      nenhuma — as letras SÃO o desenho. */
function f0(d){
  var c = el("div", "capa"), nome = "O CASO DOS SONS IGUAIS", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.04 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  var cena = "";
  [["S","Z"], ["X","CH"], ["C","Ç"], ["G","J"], ["M","N"]].forEach(function(par){
    cena += '<span class="dupla"><b>' + par[0] + '</b><i>=</i><b>' + par[1] + '</b></span>';
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 5º ano &middot; vinte e três folhas sobre as letras que soam igual</div>' +
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

/* ============ 1, 2 e 3 — A LETRA QUE FALTA (escolher) ============
   As três vêm INTEIRAS de folha de papel, e o comando delas está copiado no
   `_sequencias/POTE-ORTO5.md`:
     folha 1 — d01: *"COMPLETE COM T OU D:"*
     folha 2 — d03, item 5: *"Complete com l, r ou s e descubra palavras conhecidas:"*
     folha 3 — d03, item 6: *"Complete com u ou l:"*

   ⭐ POR QUE ELAS ABREM O CADERNO, e não o som do S (que é o assunto de
   verdade do 5º ano): porque aqui a criança ainda pode RESOLVER PELO OUVIDO —
   T e D soam diferente, L e R soam diferente. É o degrau em que a orelha basta.
   Da folha 4 em diante a orelha deixa de bastar, e é aí que a ortografia
   começa. Abrir pelo difícil seria abrir pela derrota.

   ⚠️ A PALAVRA INTEIRA FICA ESCONDIDA até o acerto (ver o `nomeSecreto`): num
      caderno de ortografia, imprimir a resposta ao lado da lacuna é a atividade
      inteira jogada fora. */
function completaLetra(d, pi, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, L = LAC[k], box = item(i + 1);
    box.appendChild(palavraLac(k, id));
    var lista = L.o.map(function(x){
      return {v: x, rot: x, aria: "Letra " + x, fala: "letra_" + x};
    });
    opcoes(box, pi, id, lista, L.r, "curta letra", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f01(d, pi){ completaLetra(d, pi, "Complete com <b>T</b> ou <b>D</b>. Toque no alto-falante para ouvir a palavra."); }
function f02(d, pi){ completaLetra(d, pi, "Complete com <b>L</b>, <b>R</b> ou <b>S</b> e descubra palavras conhecidas."); }
function f03(d, pi){ completaLetra(d, pi, "Complete com <b>U</b> ou <b>L</b>. As duas terminam a sílaba do mesmo jeitinho."); }

/* ============ 4, 5 e 6 — AS GAVETAS DE CADA SOM (classificar) ============
   Do exemplo que a professora mandou: *"Classificando os Erros — Organize as
   palavras na coluna correta"*, com as colunas Ç · X · C · H inicial · MB.

   ⚠️ VIROU TRÊS FOLHAS, E NÃO UMA, e o motivo está no `POTE`: cinco colunas num
      celular são cinco colunas de um dedo de largura, e misturam problemas
      diferentes (o som do S com o H mudo). Aqui cada folha fica com UM som e as
      caras dele — que é exatamente o que a professora pediu por escrito:
      *"diferenciando o uso das letras com o mesmo som"*.
   ⚠️ AS DUAS PORTAS: arrastar a palavra até a gaveta (PC) e tocar na palavra e
      depois na gaveta (celular). Guardar só o arrasto deixaria metade da turma
      de fora — e a gaveta tem alto-falante que diz a REGRA dela, não a resposta. */
function gavetas(d, pi, gk){
  faixa(d, pi, NOMES[pi - 1]);
  var G = GAV[gk];
  enunciado(d, pi, "Todas estas palavras têm <b>" + G.t + "</b>. Ponha cada uma na gaveta " +
            "da letra que escreve esse som.", "p" + pi + "enun");
  var cols = el("div", "colunas"), caixas = {}, listaC = [];
  G.cols.forEach(function(C){
    var c = el("div", "coluna");
    var t = el("div", "ctit", C.n);
    t.setAttribute("data-alvo", "1");
    /* ⚠️ O ALVO COMPARTILHADO SE DECLARA NO NÍVEL DA FOLHA, e não do item: a
       mesma gaveta recebe seis palavras, então `gav-<id>` não serviria. O
       contrato `alvo-<chave>` + resposta `">chave"` é o que o jogador da banca
       (`_qa/joga_folha.js`) lê para resolver a folha sozinho. Sem isto ele diz
       "não conheço a peça" — e isso é dívida, não aprovação. */
    c.setAttribute("data-qa", "alvo-gav" + pi + "_" + C.k);
    t.appendChild(botaoSom("Ouvir a regra da gaveta " + C.n, function(){ falar("gav_" + gk + "_" + C.k); }));
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
    /* ⚠️ A PALAVRA ESCRITA É A PEÇA, não a resposta entregue: é ela que a
       criança pega e leva até a gaveta. Sem esta declaração o portão 1i4
       reprova doze itens dizendo que a tela mostra a resposta — e teria razão
       em qualquer outra folha. */
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
function f04(d, pi){ gavetas(d, pi, "som_s"); }
function f05(d, pi){ gavetas(d, pi, "som_z"); }
function f06(d, pi){ gavetas(d, pi, "som_x"); }

/* ============ 7 e 8 — O DETETIVE CIRCULA A CERTA ============
   Do exemplo da professora, VERBATIM: *"Desafio do Detetive Ortográfico —
   Observe as palavras e circule apenas as corretas."*

   ⚠️ AS TRAPAÇAS DA FOLHA 7 SÃO AS DELA, copiadas uma a uma (licho, anbiente,
      reflecsão, dedicasão, sertesa). Inventar trapaça é fácil e é pior: a
      trapaça boa é a que a criança de verdade escreve, e essas ela já viu na
      sala.
   ⚠️ E AQUI A PALAVRA CERTA ESTÁ À VISTA, de propósito — é uma folha de
      RECONHECER, não de completar. A criança compara três grafias e escolhe. É
      o degrau em que ela deixa de ser guiada pela lacuna. */
function detetive(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Só <b>uma</b> de cada linha está escrita certa. Circule a certa.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var D = DET[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Qual está certa?"));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
    box.appendChild(lin);
    var lista = baralha([D.c].concat(D.e)).map(function(w){
      return {v: w, rot: w, aria: w};
    });
    opcoes(box, pi, id, lista, D.c, "circ", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f07(d, pi){ detetive(d, pi); }
function f08(d, pi){ detetive(d, pi); }

/* ============ 9 — TEM H NO COMEÇO? (julgar) ============
   O H inicial é uma das colunas do exemplo da professora, e nenhuma folha de
   papel o TREINA. Ele entrou pelo currículo: Blumenau pede, no 5º ano,
   *"palavras de uso frequente com correspondências irregulares"* — e não há
   irregularidade mais pura do que uma letra que não tem som nenhum.

   ⚠️⚠️ SEM O ALTO-FALANTE ESTA FOLHA NÃO EXISTE. A palavra aparece com a lacuna
      no lugar do H; a única forma de saber qual é a palavra é OUVI-LA. Se ela
      viesse escrita inteira, a resposta estaria impressa no enunciado. É o
      caso mais claro de "a voz é a tarefa, não o apoio" deste caderno. */
function f09(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque no alto-falante, <b>ouça</b> a palavra e diga se ela começa com H.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var H = HAG[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var c = el("div", "figsil");
    c.appendChild(el("div", "pgrande", H.m.replace("_", '<i class="lacuna"></i>')));
    var lin = el("div", "chamlin");
    lin.appendChild(nomeSecreto(H.p, id));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
    c.appendChild(lin);
    box.appendChild(c);
    var lista = [{v: "sim", rot: "COM H", aria: "Começa com H"},
                 {v: "nao", rot: "SEM H", aria: "Não começa com H"}];
    opcoes(box, pi, id, lista, H.r ? "sim" : "nao", "curta",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 10 — M OU N ANTES DE P E DE B? (escolher) ============
   "MB" é uma das colunas do exemplo da professora; treiná-la é decisão do
   currículo (*"regras de correspondência fonema-grafema... contextuais"*), e
   esta é a regra contextual mais clássica que existe em português.
   ⚠️ A DICA NÃO DÁ A LETRA: ela manda a criança OLHAR A VIZINHA
      ("depois da lacuna vem um B"). Regra contextual se aprende olhando o
      contexto — dizer "é M" seria responder no lugar dela. */
function f10(d, pi){ completaLetra(d, pi, "Complete com <b>M</b> ou <b>N</b>. Olhe bem a letra que vem <b>depois</b> da lacuna."); }

/* ============ 11 — G OU J? (escolher) ============
   Não aparece em fonte nenhuma da colheita, e entrou pelo currículo: é o outro
   lado das *"correspondências irregulares"* da rede. Em -AGEM há regra (e a
   dica a diz); no resto, não há — e a dica então dá o SENTIDO da palavra e
   avisa, com todas as letras, que esta é das que se guardam de cor. Fingir
   regra onde não há seria ensinar errado. */
function f11(d, pi){ completaLetra(d, pi, "Complete com <b>G</b> ou <b>J</b>. Os dois fazem o mesmo som antes de E e de I."); }

/* ============ 12 — LIGUE O ERRADO AO CERTO ============
   Do exemplo da professora: *"Caça-palavras Ortográfico — Encontre no texto as
   palavras corretas correspondentes aos erros"*, que no papel é uma tabela de
   duas colunas: o erro à esquerda, a palavra certa à direita. Os cinco erros
   são os dela.
   ⚠️ Primeira folha de LIGAR do caderno — a posição 12 está declarada lá em
      cima, na constante `LIGAR`, junto com a 13. */
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque na palavra <b>errada</b> e depois na <b>certa</b> que corresponde a ela.",
            "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: '<span class="rotop errada">' + PARERR[k].e + "</span>",
            dir: '<span class="rotop">' + PARERR[k].c + "</span>",
            ariaE: PARERR[k].e, ariaD: PARERR[k].c,
            fe: "err_" + k, fd: "cert_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 13 — LIGUE A PALAVRA À REGRA ============
   É o degrau que fecha o bloco das regras: até aqui a criança ACERTAVA a letra;
   aqui ela tem de DIZER POR QUÊ. Saber a regra é o que faz a criança acertar
   uma palavra que ela nunca viu — decorar dez palavras não faz.
   ⚠️ Segunda folha de LIGAR, declarada na constante `LIGAR`. */
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque na <b>palavra</b> e depois na <b>regra</b> que explica como ela se escreve.",
            "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: '<span class="rotop">' + REGRA[k].p + "</span>",
            dir: REGRA[k].r,
            ariaE: REGRA[k].p, ariaD: REGRA[k].r,
            fe: "pal_" + k, fd: "reg_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 14 — O RECADO (ler e interpretar) ============
   ⚠️ ESTA FOLHA NÃO VEIO DA COLHEITA, e dizer que veio seria mentir no lugar
      mais fácil de mentir. Ela veio do PEDIDO DA PROFESSORA (*"Ler e
      interpretar diferentes gêneros do discurso"*) e da lista que a rede
      escreve por extenso no 5º ano: *"recado, aviso, cartaz, panfleto..."*.
      Nenhuma das quatro fontes de papel tem texto de gênero para interpretar.
   ⚠️ E O TEXTO É NOSSO. Recado de escola de verdade traz nome de gente real.
   ⭐ POR QUE O RECADO VEM ANTES DA RECEITA E DA NOTÍCIA: é o gênero mais curto
      e o único que a criança de 5º ano já escreveu com as próprias mãos. */
function textoLido(d, titulo, linhas, chaveFala, cls){
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "enun", "<b>" + titulo + "</b>"));
  lin.appendChild(botaoSom("Ouvir o texto", function(){ falar(chaveFala); }));
  d.appendChild(lin);
  var cx = el("div", cls || "poema");
  linhas.forEach(function(t){ cx.appendChild(el("div", "tl", t)); });
  cx.setAttribute("data-alvo", "1");
  d.appendChild(cx);
  return cx;
}
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leia o recado e responda. Dá para voltar e ler de novo quantas vezes quiser.",
            "p" + pi + "enun");
  textoLido(d, BILHETE.titulo, BILHETE.linhas, "bilhete", "poema recado");
  ST.folha["p" + pi].forEach(function(n, i){
    var P = BILHETE.perg[n], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", P.q));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("perg14_" + n); }));
    box.appendChild(lin);
    /* ⚠️ O VALOR DA OPÇÃO É UMA CHAVE CURTA, e o texto vai no rótulo. Com a
       frase inteira como valor, o `data-qa` do botão virava uma linha de
       sessenta letras com espaços — e o jogador da banca, que procura o alvo
       pelo fim do `data-qa`, não achava nada. */
    var todas = [{v: "cert", t: P.c}];
    P.e.forEach(function(t, j){ todas.push({v: "err" + j, t: t}); });
    var lista = baralha(todas).map(function(o){
      return {v: o.v, rot: o.t, aria: o.t};
    });
    opcoes(box, pi, id, lista, "cert", "frase", "certo" + pi + "_" + n, "dica" + pi + "_" + n);
    fechaItem(d, box, id);
  });
}

/* ============ 15 — OS ERROS DENTRO DO RECADO (marca-texto) ============
   É a mecânica da d02 (*"encontre os erros de ortografia"*) aplicada ao MESMO
   recado da folha 14 — agora escrito com cinco erros.
   ⭐ E o degrau é este: achar a palavra errada SOZINHA, numa lista, é uma coisa;
      achá-la ESCONDIDA DENTRO DE UM TEXTO que a criança está lendo por sentido
      é outra, bem mais difícil. As cinco palavras são as que ela acabou de
      aprender nas folhas 4 a 13 — ela já sabe a regra; falta usá-la lendo.
   ⚠️ Tocar numa palavra CERTA não conta erro contra a criança em item nenhum:
      ela está LENDO, e ler não é errar. */
function marcaTexto(d, pi, T, pergunta, falaTexto){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pergunta, "p" + pi + "enun");
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "enun", "<b>" + T.titulo + "</b>"));
  lin.appendChild(botaoSom("Ouvir o texto", function(){ falar(falaTexto); }));
  d.appendChild(lin);
  var cx = el("div", "poema");
  var alvo = {};
  ST.folha["p" + pi].forEach(function(w, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, T.erradas[w]);
    alvo[w] = id;
  });
  var placar = el("div", "placar", "");
  function conta(){
    var n = 0, w;
    for(w in alvo) if(ST.resp[alvo[w]]) n++;
    placar.textContent = "Achou " + n + " de " + ST.folha["p" + pi].length + ".";
  }
  T.linhas.forEach(function(v){
    var p = el("div", "");
    v.forEach(function(w){
      var id = alvo[w];
      var b = el("button", "pw" + (id && ST.resp[id] ? " achada" : ""), w);
      b.setAttribute("aria-label", w);
      if(id){
        b.setAttribute("data-qa", "item-" + id);
        /* ⚠️ ALVO DECLARADO: achar a palavra DENTRO do texto é a tarefa — o
           texto tem de estar escrito, senão não há onde procurar. */
        b.setAttribute("data-alvo", "1");
      }
      b.onclick = function(){
        sPasso();
        if(id){
          if(ST.resp[id]) return;
          b.className = "pw achada";
          conta();
          acertou(id, "certo" + pi);
          return;
        }
        b.className = "pw nao";
        setTimeout(function(){ b.className = "pw"; }, 400);
        sErro(); falar("estacerta");
      };
      p.appendChild(b);
      p.appendChild(document.createTextNode(" "));
    });
    cx.appendChild(p);
  });
  d.appendChild(cx);
  conta();
  d.appendChild(placar);
}
function f15(d, pi){
  marcaTexto(d, pi, BILERR,
             "Toque nas <b>cinco</b> palavras escritas errado neste recado.", "bilerr");
}

/* ============ 16 — A RECEITA (ordenar) ============
   ⚠️ TAMBÉM NÃO VEIO DA COLHEITA — veio do pedido da professora e da lista de
      gêneros da rede, que nomeia a *"receita"* com todas as letras.
   ⭐ E O GESTO VEM DO GÊNERO, não do nosso cardápio: uma receita é uma ordem de
      passos, e trocar dois deles estraga o suco. Perguntar "qual é o assunto da
      receita?" seria tratar a receita como se fosse um conto. */
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Os passos da receita estão fora de ordem. Ponha cada um no seu lugar.",
            "p" + pi + "enun");
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "enun", "<b>" + RECEITA.titulo + "</b>"));
  lin.appendChild(botaoSom("Ouvir o nome da receita", function(){ falar("receita"); }));
  d.appendChild(lin);
  var pool = ST.folha["p" + pi];
  var trilha = el("div", "trilhaord passos"), slots = [], listaS = [];
  pool.forEach(function(_, i){
    var s = el("div", "slot"); s.setAttribute("data-alvo", "1");
    s.setAttribute("data-qa", "alvo-slot" + pi + "_" + (i + 1));
    s.innerHTML = '<span class="sn">' + (i + 1) + "º</span>";
    s._i = i + 1; slots.push(s); listaS.push(s); trilha.appendChild(s);
  });
  d.appendChild(trilha);
  var banco = el("div", "figbanco"), marcada = null;
  pool.forEach(function(n, i){
    var id = "n" + pi + "_" + i, P = RECEITA.passos[n];
    /* o mesmo contrato das gavetas: o lugar da fila é alvo COMPARTILHADO */
    registra(id, pi, ">slot" + pi + "_" + P.i);
    if(ST.resp[id]){
      var s0 = slots[P.i - 1];
      s0.className = "slot cheia";
      s0.innerHTML = '<span class="sn">' + P.i + "º</span><span class=\"rot\">" + P.t + "</span>";
    }
  });
  baralha(pool.slice(0)).forEach(function(n){
    var i = pool.indexOf(n), id = "n" + pi + "_" + i, P = RECEITA.passos[n];
    if(ST.resp[id]) return;
    var b = el("button", "op frase", P.t);
    b.setAttribute("aria-label", P.t);
    b.setAttribute("data-qa", "item-" + id);
    function larga(s){
      if(ST.resp[id]) return;
      if(s._i === P.i){
        s.className = "slot cheia";
        s.innerHTML = '<span class="sn">' + P.i + "º</span><span class=\"rot\">" + P.t + "</span>";
        b.className = "op frase usada";
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + n);
      } else {
        s.className = "slot"; errou(id, "dica" + pi + "_" + n);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      sPasso(); falar("passo_" + n);
      if(marcada === b){ b.className = "op frase"; marcada = null; return; }
      if(marcada) marcada.className = "op frase";
      b.className = "op frase marcada"; marcada = b;
    };
    puxavel(b, listaS, function(s){ larga(s); });
    banco.appendChild(b);
  });
  listaS.forEach(function(s){
    s.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_passo"); return; }
      marcada._larga(s);
    };
  });
  d.appendChild(banco);
}

/* ============ 17 — A NOTÍCIA (marcar várias) ============
   ⚠️ A terceira que veio do pedido da professora e da lista da rede
      (*"notícia (curta)"*), não da colheita.
   ⭐ O gesto de novo sai do gênero: uma notícia se lê procurando O QUE, QUANDO,
      ONDE e QUEM. Duas das seis opções NÃO estão no texto — e é aí que a folha
      ensina, porque obriga a criança a voltar ao texto para ter certeza de que
      não está lá. Achar que "deve estar" é o erro de leitura mais comum do 5º ano.
   ⚠️ Esta é a única folha do caderno em que mais de uma resposta está certa ao
      mesmo tempo, e é de propósito. */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Marque <b>todas</b> as perguntas que esta notícia responde. " +
            "Depois toque em <b>Conferir</b>.", "p" + pi + "enun");
  textoLido(d, NOTICIA.titulo, NOTICIA.linhas, "noticia", "poema recado");
  var id = "n" + pi + "_0";
  /* o pote desta folha vem embrulhado: uma posição só, com as seis perguntas
     dentro — ver o comentário do `novaFolha` no index.html */
  var perguntas = ST.folha["p" + pi][0], certas = [], k;
  perguntas.forEach(function(kk){ if(NOTICIA.marcar[kk].v) certas.push(kk); });
  /* ⚠️ A RESPOSTA DECLARADA É A LISTA DE CHAVES, e não os rótulos: é assim que
     o jogador da banca acha os botões (`mc-<id>-<chave>`) e o Conferir. */
  registra(id, pi, certas.join(" "));
  var box = item(0);
  var cx = el("div", "marcax"), marcadas = {}, bts = {};
  baralha(perguntas.slice(0)).forEach(function(kk){
    var M = NOTICIA.marcar[kk];
    var b = el("button", "lx", '<span class="cx"></span><span>' + M.t + "</span>");
    b.setAttribute("aria-label", M.t);
    b.setAttribute("data-qa", "mc-" + id + "-" + kk);
    bts[kk] = b;
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); falar("pnot_" + kk);
      if(marcadas[kk]){ delete marcadas[kk]; b.className = "lx"; b.querySelector(".cx").textContent = ""; }
      else { marcadas[kk] = 1; b.className = "lx marcada"; b.querySelector(".cx").textContent = "X"; }
    };
    cx.appendChild(b);
  });
  box.appendChild(cx);
  var bt = el("button", "bt pronto", "Conferir");
  bt.setAttribute("data-qa", "conferir-" + id);
  bt.onclick = function(){
    if(ST.resp[id]) return;
    var erro = 0, kk;
    for(kk in bts) if(!!NOTICIA.marcar[kk].v !== !!marcadas[kk]) erro++;
    if(erro){
      for(kk in bts) if(marcadas[kk] && !NOTICIA.marcar[kk].v) bts[kk].className = "lx errada";
      setTimeout(function(){ var g; for(g in bts) if(marcadas[g]) bts[g].className = "lx marcada"; }, 900);
      errou(id, "dica" + pi);
      return;
    }
    for(kk in bts) if(NOTICIA.marcar[kk].v) bts[kk].className = "lx certa";
    bt.style.display = "none";
    acertou(id, "certo" + pi);
  };
  if(ST.resp[id]){
    for(k in bts) if(NOTICIA.marcar[k].v){ bts[k].className = "lx certa"; bts[k].querySelector(".cx").textContent = "X"; }
    bt.style.display = "none";
  }
  box.appendChild(bt);
  fechaItem(d, box, id);
}

/* ============ 18 — OS DEZ ERROS DA HISTÓRIA (marca-texto) ============
   ⚠️ ESTE TEXTO É O DA FOLHA d02 (toda matéria), COPIADO PALAVRA POR PALAVRA,
      com os dez erros que ela plantou. O comando impresso lá é *"Leia o texto e
      encontre 10 erros de ortografia. Reescreva-o corretamente."* — as DUAS
      metades dele viraram as folhas 18 e 19 deste caderno, porque são duas
      tarefas de tamanhos muito diferentes e juntas numa tela só nenhuma das
      duas caberia.
   ⭐ É o ponto mais alto da leitura no caderno: dez erros num texto de doze
      linhas, e nenhum deles marcado. */
function f18(d, pi){
  marcaTexto(d, pi, HISTORIA,
             "Leia o texto e ache as <b>dez</b> palavras escritas errado.", "historia");
}

/* ============ 19 — REESCREVA CERTO (digitar) ============
   A segunda metade do comando da d02: *"Reescreva-o corretamente."*
   ⚠️ SÃO OITO DAS DEZ, e está dito no `index.html` por quê: escrever letra a
      letra custa uns vinte e cinco segundos por palavra, e dez seguidas fariam
      esta folha sozinha passar de quatro minutos numa ideia só.
   ⚠️ O TECLADO É O MESMO DA CRUZADINHA — a mesma peça, o mesmo `digitaCruz`, o
      mesmo teclado DE VERDADE funcionando junto. Escrever uma segunda seria
      arrumar lugar para um segundo defeito.
   ⭐ E ESTE É O DEGRAU MAIS ALTO DO CADERNO: até aqui ela RECONHECIA a forma
      certa entre as que estavam à vista; aqui não há nada à vista. */
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cada palavra está errada. Toque nela e <b>escreva do jeito certo</b>.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var R = REESC[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, R.p);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", 'Está escrito <b class="errada">' + R.e + "</b>."));
    lin.appendChild(botaoSom("Ouvir a palavra certa", function(){ falar("diz_" + k); }));
    box.appendChild(lin);
    var grade = el("div", "cruz uma"), cels = [], t;
    /* ⚠️ `esc-<id>` é o contrato da casa para "aqui se escreve no teclado":
       é por ele que o jogador da banca abre o teclado e digita a resposta
       declarada, pelo teclado DE VERDADE. */
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < R.p.length; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? R.p.charAt(t) : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    var E = {k: k, w: R.p, id: id, cels: cels, n: i + 1,
             rot: "Escreva a palavra certa", bt: el("span", "pista oculta", "")};
    cels.forEach(function(c){
      c.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
    });
    grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
    box.appendChild(grade);
    fechaItem(d, box, id);
  });
}

/* ============ 20 — O BANCO DE PALAVRAS (arrastar) ============
   Do exemplo da professora, copiado: *"Banco de Palavras — Complete as frases
   usando as palavras do quadro"*, com o quadro dele (importância, lixo, hábito,
   dedicação, reflexão, ambiente) e as seis frases dele.
   ⭐ E É AQUI QUE ENTRA O QUE A FOLHA 5 DO EXEMPLO PEDIA e a tela não sabe
      fazer: *"Escreva uma frase com cada palavra"*. Escrever frase livre a tela
      não corrige — ela aceitaria qualquer coisa e diria "muito bem", que é
      teatro. O que dá para medir é USAR a palavra no lugar certo de uma frase
      pronta, e é o que esta folha faz. A produção de frases fica com o caderno
      de papel, e isso está escrito no dossiê do professor.
   ⚠️ AS DUAS PORTAS: arrastar a palavra até a lacuna (PC) e tocar-tocar (celular). */
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Complete as frases usando as palavras do <b>quadro</b>.",
            "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
  var lacunas = [], listaL = [];
  var frasesCx = el("div", "frases");
  pool.forEach(function(n, i){
    var F = BANCO.frases[n], id = "n" + pi + "_" + i;
    /* aqui o compartilhado é a PEÇA (o quadro serve as seis frases), então a
       ordem se inverte: `"<chave"` = toca no alvo primeiro, depois no item */
    registra(id, pi, "<pal" + pi + "_" + chaveQuadro(F.r));
    var fr = el("div", "frasel");
    fr.appendChild(document.createTextNode(F.a));
    var lac = el("span", "lacuna grande" + (ST.resp[id] ? " cheia" : ""),
                 ST.resp[id] ? F.r : "");
    lac.setAttribute("data-alvo", "1");
    lac.setAttribute("data-qa", "item-" + id);
    lac._r = F.r; lac._id = id; lac._n = n;
    fr.appendChild(lac);
    fr.appendChild(document.createTextNode(F.b));
    fr.appendChild(botaoSom("Ouvir a frase", function(){ falar("frase_" + F.k); }));
    lacunas.push(lac); listaL.push(lac);
    frasesCx.appendChild(fr);
  });
  d.appendChild(frasesCx);
  var quadro = el("div", "figbanco quadro"), marcada = null;
  baralha(BANCO.quadro.slice(0)).forEach(function(w){
    var b = el("button", "op pal", w);
    b.setAttribute("aria-label", w);
    b.setAttribute("data-qa", "alvo-pal" + pi + "_" + chaveQuadro(w));
    var usada = false, i;
    for(i = 0; i < lacunas.length; i++) if(lacunas[i]._r === w && ST.resp[lacunas[i]._id]) usada = true;
    if(usada) b.className = "op pal usada";
    function larga(lac){
      if(ST.resp[lac._id]) return;
      if(lac._r === w){
        lac.className = "lacuna grande cheia"; lac.textContent = w;
        b.className = "op pal usada";
        if(marcada === b) marcada = null;
        acertou(lac._id, "certo" + pi + "_" + lac._n);
      } else {
        lac.className = "lacuna grande erro";
        setTimeout(function(){ lac.className = "lacuna grande"; }, 500);
        errou(lac._id, "dica" + pi + "_" + lac._n);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(b.className.indexOf("usada") > -1) return;
      sPasso(); falar("quadro_" + chaveQuadro(w));
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
    };
    puxavel(b, listaL, function(lac){ larga(lac); });
    quadro.appendChild(b);
  });
  listaL.forEach(function(lac){
    lac.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_quadro"); return; }
      marcada._larga(lac);
    };
  });
  d.appendChild(quadro);
}

/* ============ 21 — O CAÇA-PALAVRAS ORTOGRÁFICO (procurar) ============
   Do exemplo da professora (*"Caça-palavras Ortográfico"*).
   ⚠️ SEIS PALAVRAS SEM ACENTO E SEM Ç, e é de propósito: a grade é feita de
      letras soltas, e um Ç no meio de uma fileira não se acha — ele se
      reconhece, que é outra coisa. O Ç tem a folha 4 inteira para ele.
   ⚠️ AS DUAS PORTAS: arrastar o dedo sobre as letras, ou tocar na primeira e na
      última. No celular o `pointerenter` não dispara ao arrastar (o ponteiro
      fica preso no primeiro alvo) — sem o toque-toque, metade da turma não
      conseguiria fechar esta folha. */
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ache as <b>seis palavras</b> na grade. Elas estão deitadas ou em pé.",
            "p" + pi + "enun");
  var palavras = ST.folha["p" + pi].map(function(k){ return CACA[k].p; });
  var N = 10, g = [], y, x;
  for(y = 0; y < N; y++){ g[y] = []; for(x = 0; x < N; x++) g[y][x] = ""; }
  var postas = {};
  palavras.forEach(function(w){
    var t, ok = false;
    for(t = 0; t < 400 && !ok; t++){
      var hor = rnd(2) === 0;
      var lx = hor ? rnd(N - w.length + 1) : rnd(N);
      var ly = hor ? rnd(N) : rnd(N - w.length + 1);
      var i, bate = true;
      for(i = 0; i < w.length; i++){
        var cy = ly + (hor ? 0 : i), cx2 = lx + (hor ? i : 0);
        if(g[cy][cx2] && g[cy][cx2] !== w.charAt(i)){ bate = false; break; }
      }
      if(!bate) continue;
      var cels2 = [];
      for(i = 0; i < w.length; i++){
        var cy2 = ly + (hor ? 0 : i), cx3 = lx + (hor ? i : 0);
        g[cy2][cx3] = w.charAt(i); cels2.push(cy2 * N + cx3);
      }
      postas[w] = cels2; ok = true;
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
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, C = CACA[k];
    registra(id, pi, C.p);
    var ch = el("span", "pmat" + (ST.resp[id] ? " achada" : ""), C.p);
    ch.setAttribute("data-qa", "item-" + id);
    /* ⚠️ ALVO DECLARADO: a lista do que procurar é o próprio enunciado do
       caça-palavras — sem ela não há o que achar. */
    ch.setAttribute("data-alvo", "1");
    chips[C.p] = {el: ch, id: id, k: k};
    if(ST.resp[id] && postas[C.p])
      postas[C.p].forEach(function(j){ cels[j].className = "dcel achada"; });
    /* ⚠️ AS DUAS PONTAS SE DECLARAM para o jogador da banca poder resolver a
       folha: `cp-<id>-a` na primeira letra e `cp-<id>-z` na última. Só se a
       célula ainda não tiver dono — duas palavras podem cruzar exatamente numa
       ponta, e sobrescrever faria o jogador acusar de defeito uma folha boa.
       Quando não dá, ele diz "não sei" naquele item, que é dívida honesta. */
    var pp = postas[C.p];
    if(pp && pp.length){
      var ca = cels[pp[0]], cz = cels[pp[pp.length - 1]];
      if(ca && !ca.getAttribute("data-qa")) ca.setAttribute("data-qa", "cp-" + id + "-a");
      if(cz && !cz.getAttribute("data-qa")) cz.setAttribute("data-qa", "cp-" + id + "-z");
    }
    lista.appendChild(ch);
  });
  d.appendChild(lista); d.appendChild(dia);
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
    var w = cam.map(function(j){ return cels[j].textContent; }).join(""), ch = chips[w];
    if(!ch || ST.resp[ch.id]) return;
    cam.forEach(function(j){ cels[j].className = "dcel achada"; });
    ch.el.className = "pmat achada";
    acertou(ch.id, "certo" + pi + "_" + ch.k);
  }
  /* ⚠️⚠️ AS DUAS PORTAS ESTAVAM QUEBRADAS — MEDIDO NO NAVEGADOR (15/set/2026).
     O `pointerdown` desta grade zerava o começo do traço em TODA letra tocada.
     Com isso:
       · o toque-toque (primeira letra, última letra) nunca fechava: o segundo
         toque virava um novo começo;
       · o arrastar também não, porque quem fechava era o `onclick`, e num
         arrasto de A até Z o clique não cai em Z.
     Ou seja: a folha inteira era um beco sem saída, e o comentário que estava
     aqui prometia "duas portas". Testei os dois caminhos com o navegador de
     verdade antes de escrever isto — nenhum dos dois fechava.
     ⚠️ O MESMO CÓDIGO ESTÁ EM OUTROS CADERNOS DA CASA (a folha de "procurar"
        do `_casa1` e do `_jogo1`, já no ar). Está avisado ao Marcos; o conserto
        lá é decisão dele, porque mexer em atividade publicada é outro trabalho.
     O conserto aqui: o toque só COMEÇA se não houver começo, e o arrasto FECHA
     no `pointerup`, na letra em que o dedo parou. */
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
      if(cam) cam.forEach(function(j){ if(cels[j].className === "dcel") cels[j].className = "dcel tracando"; });
    });
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

/* ============ 22 — A CRUZADINHA (cruzadinha) ============
   Da d03, item 7, VERBATIM: *"Complete a cruzadinha com palavras que têm sílaba
   terminada em l"*.
   ⭐ E É A FOLHA DAS FIGURAS. As seis palavras são os seis desenhos daquele
      papel, e as seis figuras deste caderno foram recortadas de lá
      (`recortar_das_folhas.py`): a criança reencontra na tela exatamente o
      desenho que está na folha que a professora entrega. É a regra do Marcos de
      14/set/2026: *"procure na internet, nada de imagem gerada por IA, utilize
      das atividades"*.
   ⚠️ A grade se monta sozinha: a primeira palavra fica deitada e as outras se
      penduram nela pela letra em comum. */
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque numa <b>figura</b>, escute e escreva a palavra na cruzadinha. " +
            "Todas têm sílaba terminada em <b>L</b>.", "p" + pi + "enun");
  var pool = ST.folha["p" + pi];
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
    /* ⚠️ AQUI HAVIA UM `if(x < 0 || y < 0) return false` noutro caderno desta
       casa — e ele quebrava a cruzadinha inteira. A primeira palavra entra em
       0,0; qualquer palavra que cruze por uma letra ADIANTE da primeira letra
       dela cai em coordenada negativa, que é válida: a grade é normalizada no
       fim. Com a guarda, só cruzava quem tivesse a letra comum na posição 0 —
       e cruzadinha sem cruzamento é lista de palavras com quadradinho. */
    for(i = 0; i < w.length; i++){
      var cx = x + (hor ? i : 0), cy = y + (hor ? 0 : i);
      var q = mapa[cx + "," + cy];
      if(q && q !== w.charAt(i)) return false;
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
    var w = CRUZP[k].p.replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, ""), col = null;
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
  var celula = {}, yy, xx;
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
    E.id = id; E.cels = []; E.rot = "Escreva a palavra da figura " + E.n;
    var t;
    for(t = 0; t < E.w.length; t++){
      var cc = celula[(E.x + (E.hor ? t : 0)) + "," + (E.y + (E.hor ? 0 : t))];
      E.cels.push(cc);
      if(t === 0 && cc && !cc.querySelector(".cn")) cc.appendChild(el("span", "cn", E.n));
    }
    if(ST.resp[id]) E.cels.forEach(function(c, t2){
      if(c){ c.className = "ccel viva ok"; c.textContent = E.w.charAt(t2);
             if(t2 === 0) c.appendChild(el("span", "cn", E.n)); } });
    var p = el("button", "pista" + (ST.resp[id] ? " feita" : ""),
               '<span class="pn">' + E.n + ".</span>" + img(CRUZP[E.k].f, "figmini", "Figura da cruzadinha"));
    /* a cruzadinha também é "escrever no teclado": mesmo contrato da folha 19 */
    p.setAttribute("data-qa", "esc-" + id);
    p.setAttribute("aria-label", "Figura " + E.n + " da cruzadinha");
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

/* ============ 23 — O CARTAZ DO DETETIVE (o fecho com gancho) ============
   ⚠️ O FECHO DAS FONTES é *"reescreva"* e *"escreva uma frase com cada
      palavra"* — texto livre, que a tela não sabe corrigir (ver o `POTE`).
      O que a tela sabe fazer é a criança MONTAR o cartaz de regras do detetive
      dela: toca na regra, a regra entra no cartaz com um exemplo, e o cartaz
      cresce embaixo.
   ⭐ É o "quero mais": ela sai daqui com um lembrete que é DELA, para colar no
      caderno de papel — e é justamente ali, no papel, que a produção de frases
      que a tela não mede vai acontecer. O dossiê diz isso ao professor. */
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escolha as regras que você quer no <b>seu cartaz</b>. " +
            "Pode escolher quantas quiser.", "p" + pi + "enun");
  var cartaz = el("div", "rua cartaz");
  function pintaCartaz(){
    cartaz.innerHTML = "";
    var n = 0;
    ST.folha["p" + pi].forEach(function(k, j){
      if(ST.resp["n" + pi + "_" + j]){
        cartaz.appendChild(el("div", "regral",
          "<b>" + CARTAZ[k].t + "</b><i>" + CARTAZ[k].ex + "</i>"));
        n++;
      }
    });
    if(!n) cartaz.appendChild(el("span", "ajuda", "o seu cartaz ainda está vazio…"));
  }
  var mural = el("div", "mural");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i;
    registra(id, pi, CARTAZ[k].t);
    var c = el("button", "cartaocasa" + (ST.resp[id] ? " escolhido" : ""),
               '<span class="rotop">' + CARTAZ[k].t + "</span>");
    c.setAttribute("aria-label", CARTAZ[k].t);
    c.setAttribute("data-qa", "item-" + id);
    /* ⚠️ ALVO DECLARADO: aqui não há resposta certa nem errada — a criança
       escolhe as regras do cartaz dela, e a regra tem de estar à vista. */
    c.setAttribute("data-alvo", "1");
    c.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); c.className = "cartaocasa escolhido";
      pintaCartaz();
      acertou(id, "certo" + pi + "_" + k);
    };
    mural.appendChild(c);
  });
  d.appendChild(mural);
  d.appendChild(el("div", "ajuda", "O seu cartaz:"));
  d.appendChild(cartaz);
  pintaCartaz();
}

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
  /* de quem é a vez: a fila da cruzadinha, ou a quadra única do outro teclado */
  /* ⚠️⚠️ LÊ AS DUAS PELO `window`, e isto NÃO é preciosismo: escrito como
     `typeof CRUZ !== "undefined" && CRUZ && CRUZ.E`, o `CRUZ` nu depois do `&&`
     é acusado de `'CRUZ' is not defined` pelo ESLint nos cadernos que não têm
     cruzadinha (ele não faz análise de fluxo, e o `typeof` só protege a
     primeira ocorrência). E esse ESLint é o portão 0a2 que roda DENTRO do
     `entregar.yml`, antes de publicar: com ele vermelho, NADA sobe. Foi assim
     que quatro publicações minhas falharam seguidas hoje, sem eu entender por
     quê — e o pré-voo daqui não pega, porque o ESLint não está instalado no
     container. Como `CRUZ` e `ATIVA` são `var` globais, elas são propriedades
     de `window`, e ler por ali funciona igual e é declarado. */
  var cs = [], i, andando = 0;
  var _cruz = window.CRUZ, _ativa = window.ATIVA;
  if(_cruz && _cruz.E && _cruz.E.cels){
    for(i = 0; i < _cruz.E.cels.length; i++)
      if(_cruz.E.cels[i] && _cruz.E.cels[i].getBoundingClientRect) cs.push(_cruz.E.cels[i]);
    andando = _cruz.val ? _cruz.val.length : 0;
  } else if(_ativa && _ativa.q && _ativa.q.getBoundingClientRect){
    cs.push(_ativa.q);
  }
  if(!cs.length) return;
  var tkel = document.getElementById("teclado");
  if(!tkel || tkel.className.indexOf("aberto") < 0) return;
  var tk = tkel.getBoundingClientRect(), topo = 56, pe = tk.top - 10;
  /* ⚠️ A RESERVA DE ROLAGEM SAI DA ALTURA REAL DO TECLADO, e não de um
     número fixo. Ela nasceu como `padding-bottom:460px` no `comtec`, que
     é certo para o teclado de LETRAS (336 px medidos a 360x640, 41
     teclas) e exagerado para o de NÚMEROS (160 px, 12 teclas): sobravam
     300 px de vazio para a criança rolar à toa enquanto digita. Como o
     `comtec` sai da tag `body` ao fechar, a variável pode ficar guardada
     sem fazer mal nenhum. */
  document.documentElement.style.setProperty("--tech", Math.ceil(tk.height + 40) + "px");
  if(pe <= topo) return;
  var cima = 1e9, baixo = -1e9;
  for(i = 0; i < cs.length; i++){
    var r = cs[i].getBoundingClientRect();
    if(r.top < cima) cima = r.top;
    if(r.bottom > baixo) baixo = r.bottom;
  }
  var d = 0;
  if(baixo - cima <= pe - topo){
    if(baixo > pe) d = baixo - pe;
    if(cima - d < topo) d = cima - topo;
  } else {
    var at = cs[Math.min(andando, cs.length - 1)].getBoundingClientRect();
    d = at.top - (topo + (pe - topo) / 2 - at.height / 2);
  }
  if(Math.abs(d) > 2) window.scrollBy(0, d);
}
function abreCruz(E, pi){
  if(CRUZ) fechaCruz();
  CRUZ = {E: E, val: "", pi: pi};
  if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista ativa";
  pintaCruz();
  document.getElementById("teclado").className = "aberto";
  /* ⚠️ ROLAR A PALAVRA PARA CIMA DO TECLADO. Sem isto a criança escreve às
     cegas: o teclado é fixo no pé da tela e a grade fica embaixo dele (medido
     em 360x640: a grade inteira por baixo). O `comtec` dá chão para a página
     poder rolar; o resto é levar a primeira casinha para a faixa que sobra. */
  document.body.className = (document.body.className.replace(/ ?comtec/, "") + " comtec").replace(/^ /, "");
  setTimeout(rolaParaCruz, 60);
  document.getElementById("tkDica").textContent = E.rot || ("Escreva a palavra da pista " + E.n);
  falar("escreva");
}
function fechaCruz(){
  if(!CRUZ) return;
  var E = CRUZ.E;
  if(!ST.resp[E.id]){
    E.cels.forEach(function(c){ if(c){ var n = c.querySelector(".cn"); c.textContent = ""; if(n) c.appendChild(n); c.className = "ccel viva"; } });
    if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista";
  }
  CRUZ = null; document.getElementById("teclado").className = "";
  document.body.className = document.body.className.replace(/ ?comtec/, "");
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
  if(ch === "ap") CRUZ.val = CRUZ.val.slice(0, -1);
  else if(ch === "ok"){ confereCruz(); return; }
  else { if(CRUZ.val.length >= E.w.length) return; CRUZ.val += ch; }
  pintaCruz(); rolaParaCruz();
  if(CRUZ.val.length >= E.w.length) setTimeout(confereCruz, 380);
}
function confereCruz(){
  if(!CRUZ || !CRUZ.val) return;
  var E = CRUZ.E, pi = CRUZ.pi;
  if(CRUZ.val === E.w){
    E.cels.forEach(function(c, i){
      if(!c) return;
      var n = c.querySelector(".cn");
      c.textContent = E.w.charAt(i); if(n) c.appendChild(n);
      c.className = "ccel viva ok";
    });
    if(E.bt) E.bt.className = E.bt.className.indexOf("oculta") > -1 ? "pista oculta" : "pista feita";
    CRUZ = null; document.getElementById("teclado").className = "";
  document.body.className = document.body.className.replace(/ ?comtec/, "");
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
(function(){
  var tk = document.getElementById("tk");
  var letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ".split("");
  letras.forEach(function(L){
    var b = el("button", null, L);
    b.setAttribute("aria-label", "Letra " + L);
    b.onclick = function(){ digitaCruz(L); };
    tk.appendChild(b);
  });
  var ap = el("button", "ap", "apagar"); ap.setAttribute("aria-label", "Apagar");
  ap.onclick = function(){ digitaCruz("ap"); }; tk.appendChild(ap);
  var ok = el("button", "ok", "OK"); ok.setAttribute("aria-label", "Confirmar");
  ok.onclick = function(){ digitaCruz("ok"); }; tk.appendChild(ok);
})();
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
   O Marcos fixou a sequência em no mínimo 20 folhas (o piso era 25 e ele o
   baixou em 14/set/2026, por velocidade de produção). Este caderno tem 23, e o
   número saiu do inventário de verbos do `POTE`, não de uma meta. Só que a
   criança DEVAGAR leva bem mais nas mesmas 23 folhas — ela não termina. Se o boletim, o parecer e a
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
    est += '<img src="img/o5_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você começou a reparar que letras diferentes podem fazer o mesmo som — e isso é o principal!";
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
  {n: "Completar a palavra com a letra que o som pede", f: [1, 2, 3],
   ok: "completa a palavra com a letra certa quando o som já separa as duas",
   nao: "ainda troca letras que soam diferente uma da outra"},
  {n: "Separar as letras que escrevem o MESMO som", f: [4, 5, 6],
   ok: "separa S, SS, C e Ç, o S e o Z, e o X e o CH pelo som e pela posição",
   nao: "ainda junta numa gaveta só letras que escrevem o mesmo som"},
  {n: "Reconhecer a grafia certa entre grafias parecidas", f: [7, 8],
   ok: "olha três grafias parecidas e reconhece qual é a certa",
   nao: "ainda escolhe a grafia pelo som, sem olhar a palavra inteira"},
  {n: "Aplicar as regras do H, do M antes de P e B e do G e J", f: [9, 10, 11],
   ok: "aplica a regra do M antes de P e B e reconhece o H que não tem som",
   nao: "ainda não usa a letra vizinha para decidir a grafia"},
  {n: "Explicar por que a palavra se escreve assim", f: [12, 13],
   ok: "liga a palavra à regra que explica como ela se escreve",
   nao: "ainda decora a palavra sem saber a regra que a explica"},
  {n: "Ler e interpretar textos de gêneros diferentes", f: [14, 16, 17],
   ok: "lê recado, receita e notícia e tira de cada um o que ele serve para dizer",
   nao: "ainda não separa o que o texto diz do que ela imagina que ele diria"},
  {n: "Achar o erro de ortografia dentro de um texto", f: [15, 18],
   ok: "acha as palavras escritas errado dentro de um texto corrido",
   nao: "ainda não enxerga o erro quando ele está no meio da leitura"},
  {n: "Escrever a palavra certa e usá-la na frase", f: [19, 20, 21, 22, 23],
   ok: "escreve a palavra certa sem modelo à vista e a usa na frase certa",
   nao: "ainda reconhece a forma certa, mas não a escreve sozinha"}
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
    "<p class='comonota'><b>O que este caderno NÃO mede:</b> a atividade que a professora " +
    "enviou termina em <b>&ldquo;Escreva uma frase com cada palavra&rdquo;</b>, e a tela não " +
    "corrige texto livre — ela aceitaria qualquer coisa e diria &ldquo;muito bem&rdquo;. O uso " +
    "da palavra em contexto está medido só até onde dá (folha 20, o banco de palavras, com " +
    "resposta certa). <b>A produção de frases continua sendo no caderno de papel</b>, e a " +
    "folha 23 existe para isso: a criança sai daqui com o cartaz de regras dela para colar lá.</p>";
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
