/* ============================================================
   A LOTERIA DO S — as vinte e duas folhas.

   Segundo caderno da sequência: o primeiro (`_ort5`) percorre TODAS as duplas
   que soam igual; este MERGULHA na que mais derruba o 5º ano — o som de S e as
   cinco letras que o escrevem (S, SS, C, Ç e SC), mais o S com som de Z e o X
   de exame.

   Cada folha nasceu de um VERBO impresso numa das 30 folhas de papel colhidas
   por workflow. O crivo, folha a folha, com o comando VERBATIM e o motivo das
   três recusas, está em `_sequencias/POTE-ORTO5.md`. Nenhuma mecânica foi
   escolhida do nosso cardápio: o papel é que manda.

   ⚠️ A POSIÇÃO É A IDENTIDADE: a folha da posição 7 usa o pote `p7`, grava os
      ids `n7_*` e fala `p7enun`. Não há segunda lista para desencontrar — isso
      já fez o relatório sair ZERO com a folha inteira respondida.
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI — são as únicas cujos ids não nascem
   de `n<pi>_`, e sim dentro do `montaLigar` (`l<pi>g<i>_<chave>`). Guardar um
   número onde há duas posições faria uma folha sumir do relatório sem erro
   nenhum na tela. */
var LIGAR = [7];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou (o ouvido · as gavetas do som · o detetive · as regras · os gêneros ·
   usar · o cartaz) */
var CORES = ["c1", "c2","c2","c2","c2", "c3","c3","c3","c3",
             "c4","c4","c4", "c5","c5","c5", "c2","c2","c1","c1", "c3","c3", "c4"];

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
/* a palavra com a lacuna, com a FIGURA quando houver e a inteira guardada
   ⚠️ TRÊS FORMATOS NA MESMA PEÇA, e é de propósito: a folha 2 mostra a figura
      recortada do papel ao lado da palavra; as folhas 3 a 9 mostram só a
      palavra, grande; as folhas 16 e 17 põem a lacuna DENTRO de uma frase, e
      aí o texto não pode ser gigante nem centralizado como uma palavra solta. */
function palavraLac(k, id){
  var L = LAC[k], c = el("div", "figsil");
  var frase = L.m.indexOf(" ") > -1;
  if(L.f) c.innerHTML = img(L.f, "figgrande", "Figura da folha de papel");
  c.appendChild(el("div", frase ? "frasel" : "pgrande",
                   L.m.replace("_", '<i class="lacuna"></i>')));
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
    f01,                              /*  1    o susto: qual está escrita certa */
    f02, f03, f04, f05,               /*  2-5  S ou SS, pela POSIÇÃO            */
    f06, f07, f08, f09,               /*  6-9  C, Ç, o dígrafo SC, e S/X/Z      */
    f10, f11, f12,                    /* 10-12 a loteria, e as quatro gavetas   */
    f13, f14, f15,                    /* 13-15 a palavra por dentro             */
    f16, f17, f18, f19,               /* 16-19 na frase, no texto e no ditado   */
    f20, f21,                         /* 20-21 caçar e cruzar                   */
    f22], i;                          /* 23    o cartaz do detetive              */
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
   que fazem o MESMO som — e cinco delas escrevem o som de S sozinho. A loteria
   é isso: a criança já sabe FALAR a palavra, e tem de acertar em qual das cinco
   casas ela se escreve.
   ⚠️ CAPA CLONADA = TROCAR A CENA, SEMPRE. Numa capa herdada desta casa ficou um
      `img("sapo")` de outra atividade: o app abria com um quadradinho vazio e um
      404 no console, e nenhum portão de texto viu. Esta capa não usa figura
      nenhuma — as letras SÃO o desenho. */
function f0(d){
  var c = el("div", "capa"), nome = "A LOTERIA DO S", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.04 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  var cena = "";
  ["S", "SS", "C", "Ç", "SC"].forEach(function(l){
    cena += '<span class="dupla"><b>' + l + "</b></span>";
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 5º ano &middot; vinte e duas folhas sobre o som de S e as cinco letras que o escrevem</div>' +
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

/* ============ 1 — PINTE SÓ AS ESCRITAS CERTAS ============
   Da d05 (alunoseprofessores), VERBATIM: *"1) Pinte as fichas que têm as
   palavras escritas de forma correta."*

   ⭐ POR QUE ELA ABRE O CADERNO: é o PROBLEMA antes do conceito. A criança olha
   oito fichas que ela sabe FALAR todas e descobre que não sabe ESCREVER metade.
   Sem esse susto, as vinte folhas seguintes não têm pergunta.
   ⚠️ A ficha ERRADA só mostra a forma certa DEPOIS que a criança responde —
      senão a resposta está impressa ao lado do enunciado. */
function f01(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Marque as fichas que estão escritas <b>certas</b>. " +
            "Depois toque em <b>Conferir</b>.", "p" + pi + "enun");
  var id = "n" + pi + "_0", fichas = ST.folha["p" + pi][0];
  var certas = [];
  fichas.forEach(function(k){ if(FICHA[k].ok) certas.push(k); });
  registra(id, pi, certas.join(" "));
  var box = item(0);
  var cx = el("div", "marcax fichas"), marcadas = {}, bts = {};
  baralha(fichas.slice(0)).forEach(function(k){
    var F = FICHA[k];
    var b = el("button", "lx ficha",
               '<span class="cx"></span>' + img(F.f, "figmini", F.c) +
               '<span class="ft">' + F.t + "</span>");
    b.setAttribute("aria-label", F.t);
    b.setAttribute("data-qa", "mc-" + id + "-" + k);
    bts[k] = b;
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); falar("diz_" + k);
      if(marcadas[k]){ delete marcadas[k]; b.className = "lx ficha"; b.querySelector(".cx").textContent = ""; }
      else { marcadas[k] = 1; b.className = "lx ficha marcada"; b.querySelector(".cx").textContent = "X"; }
    };
    cx.appendChild(b);
  });
  box.appendChild(cx);
  function revela(){
    var kk;
    for(kk in bts){
      if(FICHA[kk].ok){ bts[kk].className = "lx ficha certa"; bts[kk].querySelector(".cx").textContent = "X"; }
      else {
        bts[kk].className = "lx ficha erroficha";
        bts[kk].querySelector(".ft").innerHTML =
          '<s>' + FICHA[kk].t + "</s> <b>" + FICHA[kk].c + "</b>";
      }
    }
  }
  var bt = el("button", "bt pronto", "Conferir");
  bt.setAttribute("data-qa", "conferir-" + id);
  bt.onclick = function(){
    if(ST.resp[id]) return;
    var erro = 0, kk;
    for(kk in bts) if(!!FICHA[kk].ok !== !!marcadas[kk]) erro++;
    if(erro){
      for(kk in bts) if(marcadas[kk] && !FICHA[kk].ok) bts[kk].className = "lx ficha errada";
      setTimeout(function(){ var g; for(g in bts) if(marcadas[g]) bts[g].className = "lx ficha marcada"; }, 900);
      errou(id, "dica" + pi);
      return;
    }
    revela(); bt.style.display = "none";
    acertou(id, "certo" + pi);
  };
  if(ST.resp[id]){ revela(); bt.style.display = "none"; }
  box.appendChild(bt);
  fechaItem(d, box, id);
}

/* ============ 2, 3, 6, 8, 9, 16 e 17 — A LETRA QUE FALTA ============
   Sete folhas do mesmo gesto, e elas vêm em BLOCOS, não espalhadas — mas os
   blocos sobem de degrau, e é o conteúdo que sobe, não a tela:
     2 e 3  — S ou SS (d14 e d06/d21): duas opções, e a folha 2 tem FIGURA
     6      — C ou Ç (d02)
     8      — C ou SC (d28): o dígrafo
     9      — S, X ou Z (d24): três opções, e o X com som de Z
     16     — dentro de FRASES, com quatro opções (d07)
     17     — dentro do TEXTO de um passeio de domingo (d01)
   ⚠️ A PALAVRA INTEIRA FICA ESCONDIDA até o acerto: num caderno de ortografia,
      imprimir a resposta ao lado da lacuna é a atividade inteira jogada fora. */
function completaLetra(d, pi, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, L = LAC[k], box = item(i + 1);
    box.appendChild(palavraLac(k, id));
    var lista = L.o.map(function(x){
      return {v: x, rot: x, aria: "Letra " + x, fala: "letra_" + x.toLowerCase()};
    });
    opcoes(box, pi, id, lista, L.r, "curta letra", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f02(d, pi){ completaLetra(d, pi, "Complete as palavras com <b>S</b> ou <b>SS</b>. Toque no alto-falante para ouvir."); }
function f03(d, pi){ completaLetra(d, pi, "Complete com <b>S</b> ou <b>SS</b>. Agora sem figura: só o ouvido e a regra."); }
function f06(d, pi){ completaLetra(d, pi, "Complete com <b>C</b> ou <b>Ç</b>. Olhe a <b>vogal</b> que vem logo depois do buraco."); }
function f08(d, pi){ completaLetra(d, pi, "Complete com <b>C</b> ou <b>SC</b>. O SC são duas letras para um som só."); }
function f09(d, pi){ completaLetra(d, pi, "Complete com <b>S</b>, <b>X</b> ou <b>Z</b>. Cuidado: aqui o X soa como Z."); }
function f16(d, pi){ completaLetra(d, pi, "Complete as palavras das frases com <b>S</b>, <b>SS</b>, <b>C</b> ou <b>Ç</b>."); }
function f17(d, pi){ completaLetra(d, pi, "Este é o passeio de domingo. Complete o texto com <b>S</b> ou <b>SS</b>."); }

/* ============ 4, 5 e 12 — AS GAVETAS ============
   folha 4  — da d15: *"Complete o seguinte quadro com palavras que tenham: S no
              início · S no meio · S no final · Palavras com SS"*
   folha 5  — da d30, que tem as colunas *"S (som de Z)"* e *"SS"*
   folha 12 — da d04 e da d12: *"escrevendo-as na coluna certa"*, quatro colunas
   ⚠️ AS DUAS PORTAS: arrastar a palavra até a gaveta (PC) e tocar na palavra e
      depois na gaveta (celular). A gaveta tem alto-falante que diz a REGRA
      dela, nunca a resposta. */
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
function f04(d, pi){ gavetas(d, pi, "onde",
  "Em que <b>lugar</b> da palavra está o S? Ponha cada uma na gaveta certa."); }
function f05(d, pi){ gavetas(d, pi, "somz",
  "Ouça cada palavra. O som do meio é de <b>Z</b> ou de <b>S</b>?"); }
function f12(d, pi){ gavetas(d, pi, "quatro",
  "Todas têm o mesmo som. Ponha cada uma na gaveta da <b>letra</b> que o escreve."); }

/* ============ 7 — LIGUE A PALAVRA À REGRA ============
   ⚠️ AS SEIS REGRAS ESTÃO COPIADAS DA d02, palavra por palavra — é o texto que
   a professora tem impresso e que a criança vai reencontrar no papel. Reescrevê-las
   "mais bonito" afastaria a tela da folha, que é o contrário do que este formato faz.
   ⭐ E é o degrau que fecha o bloco: até aqui ela ACERTAVA a letra; aqui ela tem
   de DIZER POR QUÊ. Saber a regra é o que a faz acertar uma palavra nova. */
function f07(d, pi){
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

/* ============ 10 — A LOTERIA: MARQUE A LETRA QUE FALTA ============
   Da d25 (vacaamarela) e da d27, VERBATIM: *"Leia a palavra, marque um 'X' na
   letra que falta e depois reescreva."* Esta é a primeira metade do comando; a
   segunda é a folha 11.
   ⭐ E é a folha que JUNTA tudo: as quatro letras na mesma tabela, misturadas.
      Até aqui cada folha avisava qual era a dupla; aqui não avisa nenhuma. */
function f10(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leia a palavra e marque um <b>X</b> na letra que falta.",
            "p" + pi + "enun");
  var tab = el("div", "loteria");
  var cab = el("div", "lotlin lotcab");
  cab.appendChild(el("span", "lotpal", "PALAVRA"));
  ["S", "SS", "C", "Ç"].forEach(function(L){ cab.appendChild(el("span", "lotcel", L)); });
  cab.setAttribute("data-alvo", "1");
  tab.appendChild(cab);
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, L = LOT[k];
    registra(id, pi, L.r);
    var lin = el("div", "lotlin");
    lin.setAttribute("data-qa", "item-" + id);
    var pal = el("span", "lotpal", L.m.replace("_", '<i class="lacuna"></i>'));
    pal.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
    lin.appendChild(pal);
    ["S", "SS", "C", "Ç"].forEach(function(letra){
      var b = el("button", "lotcel viva" + (ST.resp[id] && letra === L.r ? " certa" : ""),
                 ST.resp[id] && letra === L.r ? "X" : "");
      b.setAttribute("aria-label", "Marcar " + letra + " em " + L.m.replace("_", " "));
      b.setAttribute("data-qa", "op-" + id + "-" + letra);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(letra === L.r){
          b.className = "lotcel viva certa"; b.textContent = "X";
          acertou(id, "certo" + pi + "_" + k);
        } else {
          b.className = "lotcel viva erro";
          setTimeout(function(){ b.className = "lotcel viva"; }, 500);
          errou(id, "dica" + pi + "_" + k);
        }
      };
      lin.appendChild(b);
    });
    tab.appendChild(lin);
  });
  d.appendChild(tab);
}

/* ============ 11 — E AGORA REESCREVA ============
   A segunda metade do comando da d25: *"e depois reescreva"*.
   ⭐ É o degrau mais alto do caderno: na folha 10 a criança RECONHECIA a letra
      entre quatro à vista; aqui não há nada à vista, e ela escreve a palavra
      inteira, letra por letra.
   ⚠️ O teclado é o MESMO da cruzadinha (`abreCruz`/`digitaCruz`), e o teclado
      DE VERDADE funciona junto — no PC da escola a criança vai digitar. */
function f11(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora <b>escreva</b> cada palavra inteira, do jeito certo.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var L = LOT[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, L.p);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Escreva a palavra que você ouvir."));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
    box.appendChild(lin);
    var grade = el("div", "cruz uma"), cels = [], t;
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < L.p.length; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? L.p.charAt(t) : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    var E = {k: k, w: L.p, id: id, cels: cels, n: i + 1,
             rot: "Escreva a palavra que você ouviu", bt: el("span", "pista oculta", "")};
    cels.forEach(function(c){ c.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); }; });
    grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
    box.appendChild(grade);
    fechaItem(d, box, id);
  });
}

/* ============ 13 — ORDENE AS SÍLABAS ============
   Da d11, item 3, VERBATIM: *"Ordene as sílabas e forme palavras."* As seis
   palavras são as dela.
   ⚠️ E A SEPARAÇÃO É A DO PAPEL: a d11 traz a regra impressa no cartaz do
      coelho — *"Na separação de sílabas, ss e rr separam-se"* —, por isso
      OS-SO e PAS-SA-GEM, e nunca O-SSO. */
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As sílabas estão embaralhadas. Toque nelas na <b>ordem certa</b> e forme a palavra.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var S = SIL[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Que palavra se forma?"));
    lin.appendChild(botaoSom("Ouvir a dica", function(){ falar("pistasil_" + k); }));
    box.appendChild(lin);
    var mostra = el("div", "montada"), feito = "";
    var certa = S.p.replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, "");
    mostra.appendChild(nomeSecreto(S.p, id));
    var linha = el("div", "ops sils");
    var ordem = [];
    /* a ordem certa sai da palavra: a sílaba que encaixa é a que continua o que
       já está montado — assim não há segunda lista para desencontrar */
    (function(){
      var resto = certa, i2, achou;
      while(resto.length){
        achou = null;
        for(i2 = 0; i2 < S.s.length; i2++){
          var sl = S.s[i2].replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, "");
          if(ordem.indexOf(i2) < 0 && resto.indexOf(sl) === 0){ achou = i2; break; }
        }
        if(achou === null) break;
        ordem.push(achou);
        resto = resto.slice(S.s[achou].replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, "").length);
      }
    })();
    /* ⚠️ A RESPOSTA DECLARADA É A FILA DE SÍLABAS NA ORDEM, e não a palavra
       pronta. Com "SUSTO" ninguém — nem o jogador da banca, nem o relatório —
       sabia em que ordem tocar; ele dizia "não conheço a peça" e a folha ficava
       sem medida nenhuma. Agora a declaração é o próprio caminho: "sus to". */
    registra(id, pi, ordem.map(function(j){ return S.s[j].toLowerCase(); }).join(" "));
    var passo = 0, bts = [];
    S.s.forEach(function(sl, j){
      var b = el("button", "op curta sil", sl);
      b.setAttribute("aria-label", "Sílaba " + sl);
      b.setAttribute("data-qa", "op-" + id + "-" + sl.toLowerCase());
      bts.push(b);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(ordem[passo] === j){
          b.className = "op curta sil usada";
          feito += sl; passo++;
          mostra.setAttribute("data-feito", feito);
          if(passo >= ordem.length) acertou(id, "certo" + pi + "_" + k);
        } else {
          b.className = "op curta sil erro";
          setTimeout(function(){ b.className = "op curta sil"; }, 500);
          errou(id, "dica" + pi + "_" + k);
        }
      };
      linha.appendChild(b);
    });
    if(ST.resp[id]) bts.forEach(function(b){ b.className = "op curta sil usada"; });
    box.appendChild(mostra); box.appendChild(linha);
    fechaItem(d, box, id);
  });
}

/* ============ 14 — QUANTAS SÍLABAS? ============
   Da d18 (Elisângela Terra), que traz a coluna *"Nº de sílabas"* com o exemplo
   já resolvido: *"se - ma - na / 3"*.
   ⭐ Ela vem DEPOIS da 13 de propósito: a criança acabou de montar as sílabas
      com a mão, então contá-las é o mesmo trabalho um degrau acima — e é aqui
      que a regra do SS que se separa vira número. */
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Bata palma para cada pedaço da palavra. <b>Quantas sílabas</b> ela tem?",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var N = NSIL[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var c = el("div", "figsil");
    c.appendChild(el("div", "pgrande", N.p));
    var lin = el("div", "chamlin");
    lin.appendChild(nomeSecreto(N.s.join(" - "), id));
    lin.appendChild(botaoSom("Ouvir a palavra em pedaços", function(){ falar("sil_" + k); }));
    c.appendChild(lin);
    box.appendChild(c);
    var lista = [2, 3, 4].map(function(n){
      return {v: String(n), rot: String(n), aria: n + " sílabas"};
    });
    opcoes(box, pi, id, lista, String(N.n), "curta letra",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 15 — ORDEM ALFABÉTICA ============
   Da d10, da d16 e da d30 — as três pedem a mesma coisa: *"escreva-as em ordem
   alfabética"*. É trabalho de dicionário, e a rede pede, no 5º ano,
   *"Conhecimento do alfabeto do português do Brasil/ordem alfabética"*.
   ⚠️ AS DUAS PORTAS: arrastar a palavra até o lugar, ou tocar na palavra e
      depois no lugar. */
function f15(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ponha as palavras em <b>ordem alfabética</b>, da primeira para a última.",
            "p" + pi + "enun");
  /* ⚠️⚠️ O POTE TRAZIA UMA POSIÇÃO SÓ (qual das duas listas de alfabeto saiu) e
     a folha registra UM ID POR PALAVRA — cinco. Como o `idsDaPagina` conta pelo
     tamanho do pote, esta folha se dava por PRONTA com a PRIMEIRA palavra posta
     no lugar e pulava para a seguinte com as outras quatro ainda na trilha; o
     relatório contava um de cinco. Medido em 15/set/2026 pelo portão novo
     `_qa/conta_folha.js`, com o caderno já no ar.
     O conserto é ler a lista aqui e devolver ao pote uma posição por palavra —
     o pote continua sorteando QUAL lista sai, que é o que ele existe para
     fazer, mas passa a ter o tamanho certo. */
  var pool = ST.folha["p" + pi], lista = ALFA[pool[0]].lista;
  if(pool.length !== lista.length){
    ST.folha["p" + pi] = lista.map(function(){ return pool[0]; });
    pool = ST.folha["p" + pi];
  }
  var ordenada = lista.slice(0).sort();
  var trilha = el("div", "trilhaord passos"), listaS = [];
  ordenada.forEach(function(_, i){
    var s = el("div", "slot"); s.setAttribute("data-alvo", "1");
    s.setAttribute("data-qa", "alvo-slot" + pi + "_" + (i + 1));
    s.innerHTML = '<span class="sn">' + (i + 1) + "º</span>";
    s._i = i + 1; listaS.push(s); trilha.appendChild(s);
  });
  d.appendChild(trilha);
  var banco = el("div", "figbanco"), marcada = null;
  lista.forEach(function(w, i){
    var id = "n" + pi + "_" + i, pos = ordenada.indexOf(w) + 1;
    registra(id, pi, ">slot" + pi + "_" + pos);
    if(ST.resp[id]){
      listaS[pos - 1].className = "slot cheia";
      listaS[pos - 1].innerHTML = '<span class="sn">' + pos + "º</span><span class=\"rot\">" + w + "</span>";
    }
  });
  baralha(lista.slice(0)).forEach(function(w){
    var i = lista.indexOf(w), id = "n" + pi + "_" + i, pos = ordenada.indexOf(w) + 1;
    if(ST.resp[id]) return;
    var b = el("button", "op pal", w);
    b.setAttribute("aria-label", w);
    b.setAttribute("data-qa", "item-" + id);
    function larga(s){
      if(ST.resp[id]) return;
      if(s._i === pos){
        s.className = "slot cheia";
        s.innerHTML = '<span class="sn">' + pos + "º</span><span class=\"rot\">" + w + "</span>";
        b.className = "op pal usada";
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + chaveQuadro(w));
      } else {
        s.className = "slot"; errou(id, "dica" + pi + "_" + chaveQuadro(w));
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      sPasso(); falar("alfa_" + chaveQuadro(w));
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
    };
    puxavel(b, listaS, function(s){ larga(s); });
    banco.appendChild(b);
  });
  listaS.forEach(function(s){
    s.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_alfa"); return; }
      marcada._larga(s);
    };
  });
  d.appendChild(banco);
}

/* ============ 18 — SEPARE AS PALAVRAS ============
   Da d26, VERBATIM: *"Reescreva as frases abaixo e conte quantas palavras cada
   uma delas tem"* — e as frases dela vêm todas grudadas, sem espaço nenhum.
   ⭐ É A FOLHA QUE MAIS JUNTA LEITURA E ORTOGRAFIA do caderno: para saber onde
      uma palavra acaba, a criança precisa RECONHECER a palavra escrita — o som
      não ajuda, porque na fala a gente também não separa.
   ⚠️ O gesto é tocar ENTRE duas letras, no lugar onde entra o espaço. É o único
      gesto deste caderno em que o alvo não é uma coisa, e sim um vão. */
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta frase está toda grudada. Toque <b>entre as letras</b>, " +
            "onde entra o espaço.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var G = GRUDADA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Quantas palavras tem esta frase?"));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("grud_" + k); }));
    box.appendChild(lin);
    /* os cortes certos: as somas do tamanho de cada palavra */
    var cortes = {}, soma = 0, j, lista = [];
    for(j = 0; j < G.p.length - 1; j++){ soma += G.p[j].length; cortes[soma] = 1; lista.push("c" + soma); }
    /* ⚠️ A RESPOSTA DECLARADA SÃO OS CORTES, não a frase separada. A frase
       ("A PRINCESA ACHOU...") diz o RESULTADO; o que o jogador da banca precisa
       é do CAMINHO — em que vãos tocar. Sem isto a folha ficava sem medida. */
    registra(id, pi, lista.join(" "));
    var faltam = G.p.length - 1, feitos = {};
    var cx = el("div", "grudada");
    var letras = G.g.split("");
    letras.forEach(function(ch, n){
      cx.appendChild(el("span", "gl", ch));
      if(n < letras.length - 1){
        var v = el("button", "vao", "");
        v.setAttribute("aria-label", "Cortar depois da letra " + ch);
        v.setAttribute("data-qa", "op-" + id + "-c" + (n + 1));
        v.onclick = function(){
          if(ST.resp[id] || feitos[n + 1]) return;
          sPasso();
          if(cortes[n + 1]){
            feitos[n + 1] = 1; v.className = "vao cortado"; faltam--;
            if(!faltam) acertou(id, "certo" + pi + "_" + k);
          } else {
            v.className = "vao erro";
            setTimeout(function(){ v.className = "vao"; }, 400);
            errou(id, "dica" + pi + "_" + k);
          }
        };
        cx.appendChild(v);
      }
    });
    if(ST.resp[id]){
      var vs = cx.querySelectorAll(".vao"), z;
      for(z = 0; z < vs.length; z++) if(cortes[z + 1]) vs[z].className = "vao cortado";
    }
    box.appendChild(cx);
    var resp = el("div", "ajuda");
    resp.appendChild(nomeSecreto(G.p.join(" ") + "  —  " + G.p.length + " palavras", id));
    box.appendChild(resp);
    fechaItem(d, box, id);
  });
}

/* ============ 19 — O DITADO ============
   Da d26, VERBATIM: *"Colorir no quadro abaixo as palavras que sua professora
   ditar."* No papel quem dita é a professora; aqui quem dita é o alto-falante.
   ⭐ É A ÚNICA FOLHA DO CADERNO EM QUE A CRIANÇA NÃO VÊ A PALAVRA ANTES: ela
      ouve e procura no quadro. Sem mp3 esta folha não existe — e é por isso que
      a voz, aqui, não é apoio: é a tarefa.
   ⚠️ SÃO DOIS TOQUES, E TEM DE SER. A primeira versão fechava o item no toque
      da palavra, sem olhar qual ditado estava valendo — e assim a criança
      fechava a folha inteira tocando no quadro a esmo, sem ouvir nada. Uma
      folha que fecha sem a criança fazer o que ela pede não mede: ela mente.
      Agora o número TEM de ser escolhido primeiro; é ele que diz qual palavra
      está sendo ditada. */
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque num <b>número</b> para ouvir a palavra ditada. " +
            "Depois ache essa palavra no quadro.", "p" + pi + "enun");
  var ativo = null, botao = {};
  var fila = el("div", "ops ditados");
  ST.folha["p" + pi].forEach(function(k, i){
    var id = "n" + pi + "_" + i, w = DITADO.ditar[k];
    registra(id, pi, ">dit" + pi + "_" + chaveQuadro(w));
    var b = el("button", "op curta dit" + (ST.resp[id] ? " usada" : ""), String(i + 1) + "ª");
    b.setAttribute("aria-label", "Ouvir a palavra ditada número " + (i + 1));
    b.setAttribute("data-qa", "item-" + id);
    b._w = w; b._id = id; b._k = k;
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); falar("dit_" + chaveQuadro(w));
      if(ativo) ativo.className = "op curta dit";
      ativo = b; b.className = "op curta dit marcada";
    };
    botao[w] = b;
    fila.appendChild(b);
  });
  d.appendChild(fila);
  var quadro = el("div", "figbanco quadro");
  baralha(DITADO.quadro.slice(0)).forEach(function(w){
    var usada = botao[w] && ST.resp[botao[w]._id];
    var b = el("button", "op pal" + (usada ? " usada" : ""), w);
    b.setAttribute("aria-label", w);
    b.setAttribute("data-qa", "alvo-dit" + pi + "_" + chaveQuadro(w));
    b.onclick = function(){
      sPasso();
      if(!ativo){ falar("toque_numero"); return; }
      var A = ativo;
      if(A._w === w){
        b.className = "op pal usada"; A.className = "op curta dit usada";
        ativo = null;
        acertou(A._id, "certo" + pi + "_" + A._k);
      } else {
        b.className = "op pal nao";
        setTimeout(function(){ b.className = "op pal"; }, 420);
        errou(A._id, "dica" + pi + "_" + A._k);
      }
    };
    quadro.appendChild(b);
  });
  d.appendChild(quadro);
}
/* ============ 20 — O CAÇA-PALAVRAS DO S E SS (procurar) ============
   Do exemplo da professora (*"Caça-palavras Ortográfico"*).
   ⚠️ SEIS PALAVRAS SEM ACENTO E SEM Ç, e é de propósito: a grade é feita de
      letras soltas, e um Ç no meio de uma fileira não se acha — ele se
      reconhece, que é outra coisa. O Ç tem a folha 4 inteira para ele.
   ⚠️ AS DUAS PORTAS: arrastar o dedo sobre as letras, ou tocar na primeira e na
      última. No celular o `pointerenter` não dispara ao arrastar (o ponteiro
      fica preso no primeiro alvo) — sem o toque-toque, metade da turma não
      conseguiria fechar esta folha. */
function f20(d, pi){
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

/* ============ 21 — A CRUZADINHA LEGAL (cruzadinha) ============
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
function f21(d, pi){
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

/* ============ 22 — O QUADRO DE REGRAS QUE EU LEVO (o fecho com gancho) ============
   ⚠️ O FECHO DAS FONTES é *"reescreva"* e *"escreva uma frase com cada
      palavra"* — texto livre, que a tela não sabe corrigir (ver o `POTE`).
      O que a tela sabe fazer é a criança MONTAR o cartaz de regras do detetive
      dela: toca na regra, a regra entra no cartaz com um exemplo, e o cartaz
      cresce embaixo.
   ⭐ É o "quero mais": ela sai daqui com um lembrete que é DELA, para colar no
      caderno de papel — e é justamente ali, no papel, que a produção de frases
      que a tela não mede vai acontecer. O dossiê diz isso ao professor. */
function f22(d, pi){
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
    est += '<img src="img/ls_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
   ordem, mudam aqui e no `curriculo.json`, no mesmo commit. */
var OBJETIVOS = [
  {n: "Reconhecer a palavra escrita certa", f: [1],
   ok: "olha a palavra escrita e reconhece se ela está certa ou errada",
   nao: "ainda aceita como certa a palavra que está escrita errada"},
  {n: "Usar S ou SS pela posição na palavra", f: [2, 3, 4, 5],
   ok: "usa S ou SS olhando onde o som está na palavra, e ouve o S que soa como Z",
   nao: "ainda escolhe entre S e SS pelo som, sem olhar a posição"},
  {n: "Usar C, Ç e o dígrafo SC pela vogal que vem depois", f: [6, 8],
   ok: "olha a vogal seguinte e decide entre C, Ç e SC",
   nao: "ainda não usa a vogal seguinte para decidir a letra"},
  {n: "Explicar a regra que escreve a palavra", f: [7, 12],
   ok: "liga a palavra à regra que explica como ela se escreve",
   nao: "ainda decora a palavra sem saber a regra que a explica"},
  {n: "Escolher entre S, X e Z", f: [9],
   ok: "separa o S, o X e o Z em palavras que soam quase iguais",
   nao: "ainda troca o X de exame pelo Z"},
  {n: "Marcar a letra e escrever a palavra sem modelo à vista", f: [10, 11, 19],
   ok: "escreve a palavra inteira sem ter nenhum modelo na tela para copiar",
   nao: "ainda reconhece a forma certa, mas não a escreve sozinha"},
  {n: "Separar a palavra em sílabas, contar e pôr em ordem", f: [13, 14, 15, 18],
   ok: "separa a palavra em sílabas, conta quantas são e usa a ordem alfabética",
   nao: "ainda não separa a palavra em pedaços nem acha onde ela acaba"},
  {n: "Usar a palavra certa dentro da frase e do texto", f: [16, 17, 20, 21, 22],
   ok: "acerta a letra quando a palavra está dentro de uma frase e de um texto",
   nao: "acerta a palavra sozinha, mas erra quando ela está no meio do texto"}
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
