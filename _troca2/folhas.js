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
/* ⚠️ NENHUMA folha deste caderno é de LIGAR — e por isso a lista fica vazia.
   Se um dia entrar uma, o número dela vem AQUI, senão os ids `l<pi>g<i>_` não
   batem com o pote e a folha nunca fecha (já aconteceu no `_rima1`, no ar). */
var LIGAR = [];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o
   assunto mudou de lugar.
   A máquina MONTA (1-9) · ACHA (10-12) · TIRA (13-14) · TROCA (15-19) ·
   INVERTE (20-22) · ACRESCENTA (23-24) · RECORTA (25-26) ·
   o CÓDIGO (27-30) · a palavra no MUNDO (31-35). */
var CORES = ["c1", "c1", "c1", "c1", "c1", "c2", "c2", "c2", "c2", "c3", "c3", "c3", "c4", "c4", "c5", "c5", "c5", "c5", "c5", "c1", "c1", "c1", "c2", "c2", "c3", "c3", "c4", "c4", "c4", "c4", "c5", "c5", "c5", "c5", "c5"];


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
  var c = el("div", "capa"), nome = "A Máquina de Trocar Sílabas", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.04 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 2º ano &middot; 35 folhas sobre trocar sílabas</div>' +
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
    est += '<img src="img/mq_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
     se divergirem — nome por nome e folha por folha. É ela que o relatório do
     professor mede e que o dossiê mostra ao lado da habilidade citada. */
  {n: "Juntar sílabas e formar a palavra", f: [1, 2, 3, 4, 5, 9]},
  {n: "Pôr as sílabas na ordem certa da palavra", f: [6, 7, 8]},
  {n: "Achar, entre muitas, só as sílabas da palavra", f: [10, 11, 12, 31]},
  {n: "Remover uma letra ou sílaba e formar outra palavra", f: [13, 14, 25, 26]},
  {n: "Substituir uma letra ou sílaba e formar outra palavra", f: [15, 16, 17, 18, 19]},
  {n: "Inverter as sílabas e descobrir a palavra que nasce", f: [20, 21, 22]},
  {n: "Acrescentar uma sílaba no começo ou no fim", f: [23, 24]},
  {n: "Ler por blocos: achar a sílaba pelo número no quadro", f: [27, 28, 29, 30]},
  {n: "Reconhecer a sílaba inicial, medial e final", f: [32, 34]},
  {n: "Levar a palavra montada para dentro de uma frase", f: [33, 35]}
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

/* ============================================================
   AS PEÇAS NOVAS DESTE CADERNO
   ⚠️ Cada uma nasceu de um COMANDO IMPRESSO numa folha de papel — a marca `T##`
      diz qual. O crivo das 40 está em `_sequencias/POTE-TROCA2.md`.
   ============================================================ */

/* ⚠️⚠️ TODA SÍLABA QUE A CRIANÇA TOCA FALA POR AQUI, E POR NENHUM OUTRO CAMINHO.
   O sintetizador não lê SOM, lê PALAVRA: dê "SA" a ele e ele soletra "esse-á".
   O pedaço é RECORTADO de dentro da gravação da palavra inteira
   (`silabas.json` + `_padrao/silabas_voz.py`, no `entregar.yml`). */
function falaDaSilaba(sb){
  return function(){
    var s = String(sb).toUpperCase();
    /* ⚠️ PEDAÇO DE DUAS SÍLABAS NÃO PRECISA DE RECORTE: a voz lê "LADO", "MATE"
       e "COLA" como leria qualquer palavra, porque têm duas vogais e desenho de
       palavra. Quem soletra é o pedaço de UMA sílaba — e esse está no SILMAP,
       recortado. Sem esta linha, o botão dos pedaços compridos ficava MUDO. */
    if(SILMAP[s]) falarSilaba(null, 0, s);
    else falar("pal_" + chaveQuadro(s));
  };
}
function figOu(f, cls){ return f ? img("mq_" + f + ".png", cls || "fig", "") : ""; }

/* PEÇA — MARQUE VÁRIAS E SÓ DEPOIS CONFIRA (T24/T29)
   ⭐ Marcar quantas quiser e confirmar depois é o que deixa a criança se
      corrigir sozinha. Numa folha de sete anos isso vale mais que acertar de
      primeira (dificuldade desejável, Bjork). */
function marqueConfira(box, id, pi, pecas, fCerto, fDica){
  var feito = !!ST.resp[id], marcadas = {}, bts = [];
  registra(id, pi, pecas.filter(function(p){ return p.ok; })
                        .map(function(p){ return p.k; }).join(" "));
  var cx = el("div", "sils");
  pecas.forEach(function(P){
    var b = el("button", "sil" + (feito && P.ok ? " ok" : ""), P.t);
    b.setAttribute("aria-label", P.t);
    b.setAttribute("data-qa", (P.ok ? "op-" : "no-") + id + "-" + P.k);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      falaDaSilaba(P.t)();
      if(marcadas[P.k]){ delete marcadas[P.k]; b.className = "sil"; }
      else { marcadas[P.k] = 1; b.className = "sil marcada"; }
    };
    cx.appendChild(b); bts.push({b: b, P: P});
  });
  box.appendChild(cx);
  var cf = el("button", "bt verde pronto", "Conferir");
  cf.setAttribute("data-qa", "conferir-" + id);
  cf.onclick = function(){
    if(ST.resp[id]) return;
    var certo = true;
    bts.forEach(function(x){ if(!!marcadas[x.P.k] !== !!x.P.ok) certo = false; });
    if(certo){
      bts.forEach(function(x){ if(x.P.ok) x.b.className = "sil ok"; });
      acertou(id, fCerto); box.className = "item feito"; cf.style.display = "none";
    } else {
      sErro(); cx.className = "sils erro";
      setTimeout(function(){ cx.className = "sils"; }, 480);
      errou(id, fDica);
    }
  };
  if(feito) cf.style.display = "none";
  box.appendChild(cf);
}

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

/* PEÇA — TIRE UMA LETRA (T02: "Elimine uma letra na primeira sílaba")
   A palavra aparece letra a letra; a criança toca na que sobra. */
function tiraLetra(box, id, pi, X, fCerto, fDica){
  registra(id, pi, "x" + X.tira);
  var cx = el("div", "cortar");
  X.de.split("").forEach(function(L, n){
    var b = el("button", "clt lt", L);
    b.setAttribute("aria-label", "Letra " + L);
    b.setAttribute("data-qa", (n === X.tira ? "op-" : "no-") + id + "-x" + n);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      if(n !== X.tira){
        b.className = "clt lt nao";
        setTimeout(function(){ b.className = "clt lt"; }, 420);
        errou(id, fDica); return;
      }
      b.className = "clt lt fora";
      var saida = el("div", "palgrande nova", X.r);
      box.appendChild(saida);
      falar("pal_" + chaveQuadro(X.r));
      acertou(id, fCerto); box.className = "item feito";
    };
    cx.appendChild(b);
  });
  box.appendChild(cx);
}

/* PEÇA — TROQUE OS PEDAÇOS DE LUGAR (T10: "MUDA-SÍLABAS")
   ⭐⭐⭐ O coração do degrau, e o que dá nome ao caderno.
   ⚠️ E AQUI O GESTO É ARRASTAR, não tocar: a criança PUXA o pedaço de trás para
      a frente. É o que a máquina faz, e é o que a mão dela sente. O toque
      simples também funciona (regra das duas portas). */
function inverte(box, id, pi, X, fCerto, fDica){
  registra(id, pi, "inv");
  var cx = el("div", "vagas2");
  var vagas = [el("div", "vg"), el("div", "vg")], ordem = X.s.slice();
  vagas[0].setAttribute("data-alvo", "1");
  vagas[1].setAttribute("data-alvo", "1");
  vagas[0].setAttribute("data-qa", "alvo-" + id + "-v0");
  vagas[1].setAttribute("data-qa", "alvo-" + id + "-v1");
  function desenha(){
    vagas.forEach(function(v, n){
      v.innerHTML = "";
      var b = el("button", "sil", ordem[n]);
      b.setAttribute("aria-label", ordem[n]);
      /* ⚠️ UM clique já resolve (as duas peças trocam), então o alvo do jogador
         é sempre a segunda vaga. */
      b.setAttribute("data-qa", n === 1 ? "op-" + id + "-inv" : "no-" + id + "-p0");
      b.onclick = function(){
        if(b._arrastou){ b._arrastou = false; return; }
        troca();
      };
      puxavel(b, vagas, function(){ troca(); });
      v.appendChild(b);
    });
  }
  function troca(){
    if(ST.resp[id]) return;
    sPasso();
    ordem = [ordem[1], ordem[0]];
    desenha();
    var agora = ordem.join("");
    if(agora === X.r.toUpperCase()){
      var saida = el("div", "palgrande nova", X.r);
      box.appendChild(saida);
      falar("pal_" + chaveQuadro(X.r));
      acertou(id, fCerto); box.className = "item feito";
    }
  }
  desenha();
  vagas.forEach(function(v){ cx.appendChild(v); });
  box.appendChild(cx);
}

/* PEÇA — O CÓDIGO DAS SÍLABAS (T19/T25/T26/T22)
   ⭐⭐ A sílaba vira NÚMERO e a criança decifra. O quadro numerado fica no alto
      da folha e vale para todos os itens, como na folha de papel. */
function quadroCodigo(d, Q){
  var g = el("div", "quadro");
  Q.quadro.forEach(function(sb, n){
    var c = el("div", "qcel");
    c.innerHTML = '<span class="qn">' + (n + 1) + '</span><span class="qs">' + sb + "</span>";
    g.appendChild(c);
  });
  d.appendChild(g);
}
function decodifica(box, id, pi, Q, P, fCerto, fDica){
  /* ⚠️⚠️ A RESPOSTA É A SEQUÊNCIA DE CÉLULAS, e uma célula pode entrar DUAS
     vezes (BANANA = 6-7-7). Por isso o nome de cada peça é a CÉLULA (`c5`), não
     a posição (`s0`): com o nome pela posição eu precisaria trocar o `data-qa`
     no meio do caminho, e o jogador da banca lê o nome UMA vez, no começo. */
  registra(id, pi, P.n.map(function(c){ return "c" + (c - 1); }).join(" "));
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "numeros", P.n.join(" &middot; ")));
  box.appendChild(lin);
  var vaga = el("div", "vagas"), cxs = [], t, feitas = 0;
  for(t = 0; t < P.n.length; t++){
    var c = el("span", "cxs2" + (ST.resp[id] ? " cheia" : ""),
               ST.resp[id] ? Q.quadro[P.n[t] - 1] : "");
    cxs.push(c); vaga.appendChild(c);
  }
  box.appendChild(vaga);
  var cx = el("div", "sils");
  /* o banco é o QUADRO INTEIRO, como na folha de papel: a criança procura o
     número, não a sílaba. */
  Q.quadro.forEach(function(sb, n){
    var serve = P.n.indexOf(n + 1) > -1;
    var b = el("button", "sil num", '<span class="qn">' + (n + 1) + "</span>" + sb);
    b.setAttribute("aria-label", "Número " + (n + 1) + ", " + sb);
    b.setAttribute("data-qa", (serve ? "op-" + id + "-c" + n : "no-" + id + "-q" + n));
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      falaDaSilaba(sb)();
      if(P.n[feitas] !== n + 1){
        b.className = "sil num nao";
        setTimeout(function(){ b.className = "sil num"; }, 420);
        errou(id, fDica); return;
      }
      cxs[feitas].innerHTML = sb; cxs[feitas].className = "cxs2 cheia";
      feitas++;
      if(feitas === P.n.length){ acertou(id, fCerto); box.className = "item feito"; }
    };
    cx.appendChild(b);
  });
  box.appendChild(cx);
}

/* PEÇA — O FIM DE DUAS, UMA NOVA (T30) ⭐⭐⭐ a melhor folha das 40.
   A criança toca na sílaba FINAL de cada palavra; quando as duas estão
   marcadas, a palavra nova aparece. */
function fimDeDuas(box, id, pi, X, fCerto, fDica){
  registra(id, pi, "za zb");
  var pegou = {};
  var cx = el("div", "duplas");
  function bloco(pal, fig, sils, tag){
    var w = el("div", "dupla");
    w.innerHTML = figOu(fig, "figp");
    var sb = el("div", "sils min");
    sils.forEach(function(s, n){
      var b = el("button", "sil", s);
      b.setAttribute("aria-label", s);
      var ultima = (n === sils.length - 1);
      b.setAttribute("data-qa", (ultima ? "op-" + id + "-" + tag : "no-" + id + "-" + tag + n));
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falaDaSilaba(s)();
        if(!ultima){
          b.className = "sil nao";
          setTimeout(function(){ b.className = "sil"; }, 420);
          errou(id, fDica); return;
        }
        b.className = "sil ok"; pegou[tag] = s;
        if(pegou.za && pegou.zb){
          var saida = el("div", "resultado");
          saida.innerHTML = figOu(X.fr, "figp") + '<div class="palgrande nova">' + X.r + "</div>";
          box.appendChild(saida);
          falar("pal_" + chaveQuadro(X.r));
          acertou(id, fCerto); box.className = "item feito";
        }
      };
      sb.appendChild(b);
    });
    w.appendChild(sb);
    w.appendChild(el("div", "palpeq", pal));
    return w;
  }
  cx.appendChild(bloco(X.a, X.fa, X.sa, "za"));
  cx.appendChild(el("div", "mais", "+"));
  cx.appendChild(bloco(X.b, X.fb, X.sb, "zb"));
  box.appendChild(cx);
}

/* ============================================================
   AS 35 FOLHAS — e a ordem É a escada.
   A máquina MONTA (1-9) → a máquina ACHA (10-12) → a máquina TIRA (13-14) →
   a máquina TROCA (15-19) → a máquina INVERTE (20-22) → a máquina ACRESCENTA
   (23-24) → a máquina RECORTA (25-26) → o código (27-30) → a palavra no mundo
   (31-35).
   ⚠️ E A REPETIÇÃO VEM EM BLOCO, colada, subindo um degrau — nunca espalhada
      (regra do Marcos: *"as crianças me dizem 'isso eu já fiz'"*).
   ============================================================ */

/* ===== BLOCO A — A MÁQUINA MONTA (1 a 9) ===== */

/* 1 e 2 — QUAL FINAL FORMA A PALAVRA (T07, VERBATIM: "FORMANDO AS PALAVRAS")
   ⚠️ O DISTRATOR É PALAVRA DE VERDADE (BOCA para BOLA) — e tem de ser: quem
      desempata é a FIGURA, exatamente como na folha de papel. A 2 é o par e
      sobe: três finais em vez de duas. */
function montaEscolha(d, pi) {
  ST.folha["p" + pi].forEach(function(k, i){
    var E = ESC[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(E.f);
    lin.appendChild(el("div", "palgrande", '<span class="pd forte">' + E.i + '</span><i class="lacuna"></i>'));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("esc_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(E.ops.map(function(sb){
      return {v: sb.toLowerCase(), rot: sb, aria: sb, fala: falaDaSilaba(sb)};
    })), E.r.toLowerCase(), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f1(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe a figura e ouça. Qual dos dois pedaços termina a " +
            "palavra?", "p" + pi + "enun");
  montaEscolha(d, pi);
}
function f2(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora são <b>três</b> pedaços para escolher. Diga a palavra " +
            "baixinho antes.", "p" + pi + "enun");
  montaEscolha(d, pi);
}

/* 3 e 4 — UM PEDAÇO, TRÊS PALAVRAS (T06, VERBATIM: "JUNTE AS SÍLABAS E FORME
   PALAVRAS")
   ⭐ A ideia grande: a sílaba não pertence a uma palavra — é peça solta que
      serve em muitos lugares. A 4 é o par e sobe: palavras compridas. */
function montaJuntar(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var J = JUN[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var alvos = [], n;
    for(n = 0; n < J.f.length; n++) alvos.push("j" + n);
    registra(id, pi, alvos.join(" "));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "palgrande", '<span class="pd forte">' + J.i + "</span>"));
    lin.appendChild(botaoSom("Ouvir o pedaço", falaDaSilaba(J.i)));
    box.appendChild(lin);
    var cx = el("div", "juntas"), feitos = 0;
    J.f.forEach(function(fim, n){
      var linha = el("div", "juntalin");
      var b = el("button", "sil" + (ST.resp[id] ? " usada" : ""), J.i + " + " + fim);
      b.setAttribute("aria-label", J.i + " mais " + fim);
      b.setAttribute("data-qa", "op-" + id + "-j" + n);
      var saida = el("span", "saida", ST.resp[id] ? J.r[n] : "");
      b.onclick = function(){
        if(ST.resp[id] || b.className.indexOf("usada") > -1) return;
        sPasso(); b.className = "sil usada"; saida.innerHTML = J.r[n];
        falar("pal_" + chaveQuadro(J.r[n]));
        feitos++;
        if(feitos === J.f.length){ acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
      };
      linha.appendChild(b);
      linha.appendChild(el("span", "seta", "&rarr;"));
      linha.appendChild(saida);
      cx.appendChild(linha);
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}
function f3(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Um pedaço só serve para <b>três</b> palavras. Junte-o a " +
            "cada final e veja o que aparece.", "p" + pi + "enun");
  montaJuntar(d, pi);
}
function f4(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As palavras agora são compridas — mas o pedaço da frente " +
            "continua sendo o mesmo.", "p" + pi + "enun");
  montaJuntar(d, pi);
}

/* 5 — A COR MOSTRA O PAR (T08: cada sílaba tem uma bolinha colorida)
   ⭐ E O ANDAIME SOME SOZINHO: os três primeiros itens trazem a bolinha; os três
      últimos, não. É o que a folha de papel faz, e é dificuldade desejável. */
function f5(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Nos primeiros, a <b>bolinha da mesma cor</b> mostra o par. " +
            "Depois a bolinha some — e você já vai saber.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = COR_[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(C.f);
    lin.appendChild(el("div", "palgrande",
      '<span class="pd forte">' + C.i + (C.c ? '<i class="bol ' + C.c + '"></i>' : "") +
      '</span><i class="lacuna"></i>'));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("cor_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(C.ops.map(function(sb){
      return {v: sb.toLowerCase(), rot: sb + (C.c && sb === C.r ? '<i class="bol ' + C.c + '"></i>' : ""),
              aria: sb, fala: falaDaSilaba(sb)};
    })), C.r.toLowerCase(), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* 6 e 7 — PONHA AS SÍLABAS NA ORDEM (T12, VERBATIM: "ENUMERE NA SEQUÊNCIA
   CORRETA, AS SÍLABAS QUE FORMAM O NOME DE CADA DESENHO" · T40, VERBATIM:
   "Desembaralhe as sílabas, forme as palavras e faça a correspondência")
   ⚠️ A posição CERTA de cada peça é a ordem dela DENTRO DA PALAVRA, não a ordem
      em que está desenhada. */
function montaOrdenar(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var O = ORD[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var certo = [], n, ordem = [], resto = O.r.toUpperCase(), achou;
    /* ⚠️ a ordem verdadeira sai da PALAVRA: encaixa da esquerda para a direita. */
    while(resto.length){
      achou = -1;
      for(n = 0; n < O.s.length; n++){
        if(ordem.indexOf(n) < 0 && resto.indexOf(O.s[n]) === 0){ achou = n; break; }
      }
      if(achou < 0) break;
      ordem.push(achou); resto = resto.slice(O.s[achou].length);
    }
    for(n = 0; n < O.s.length; n++) certo.push("s" + n);
    registra(id, pi, certo.join(" "));
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(O.f);
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("ord_" + k); }));
    box.appendChild(lin);
    var vaga = el("div", "vagas"), cxs = [], t, feitas = 0;
    for(t = 0; t < O.s.length; t++){
      var c = el("span", "cxs2" + (ST.resp[id] ? " cheia" : ""),
                 ST.resp[id] ? O.s[ordem[t]] : "");
      cxs.push(c); vaga.appendChild(c);
    }
    box.appendChild(vaga);
    var cx = el("div", "sils");
    baralha(O.s.map(function(sb, n){ return {sb: sb, n: ordem.indexOf(n)}; })).forEach(function(P){
      var b = el("button", "sil", P.sb);
      b.setAttribute("aria-label", P.sb);
      b.setAttribute("data-qa", "op-" + id + "-s" + P.n);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falaDaSilaba(P.sb)();
        if(P.n !== feitas){
          b.className = "sil nao";
          setTimeout(function(){ b.className = "sil"; }, 420);
          errou(id, "dica" + pi + "_" + k); return;
        }
        b.className = "sil usada";
        cxs[feitas].innerHTML = P.sb; cxs[feitas].className = "cxs2 cheia";
        feitas++;
        if(feitas === O.s.length){ acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
      };
      cx.appendChild(b);
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}
function f6(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As sílabas se embaralharam. Toque nelas <b>na ordem</b> " +
            "para a palavra voltar.", "p" + pi + "enun");
  montaOrdenar(d, pi);
}
function f7(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora são três pedaços. A figura confere para você.",
            "p" + pi + "enun");
  montaOrdenar(d, pi);
}

/* 8 — DUAS ORDENS, UMA SÓ É PALAVRA (T15: o par LI-TO-PA × LI-PA-TO)
   ⭐ A descoberta: as MESMAS sílabas em outra ordem não são nada. */
function f8(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Os mesmos pedaços, em duas ordens. Só <b>uma</b> é palavra " +
            "de verdade — qual?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var D = DUAS[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(D.f);
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("dua_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(D.ops.map(function(w){
      return {v: w.toLowerCase(), rot: w, aria: w, fala: "pal_" + chaveQuadro(w)};
    })), D.r.toLowerCase(), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* 9 — AS GOTAS DE CHUVA (T31, VERBATIM: "JUNTE AS SÍLABAS DAS GOTINHAS E FORME
   PALAVRAS")
   ⚠️ O BANCO É O MESMO PARA TODOS OS ITENS, como na folha de papel: cada sílaba
      certa aparece UMA vez e as outras são distratoras de verdade. */
function f9(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "As sílabas caíram como gotas de chuva. Pegue as que formam " +
            "cada palavra, <b>na ordem</b>.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var B = BANCO.pal[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var certo = [], n;
    for(n = 0; n < B.s.length; n++) certo.push("s" + n);
    registra(id, pi, certo.join(" "));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Monte uma palavra de <b>" + B.s.length +
                                       " sílabas</b>. Ouça qual é."));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("ban_" + k); }));
    box.appendChild(lin);
    var vaga = el("div", "vagas"), cxs = [], t, feitas = 0;
    for(t = 0; t < B.s.length; t++){
      var c = el("span", "cxs2" + (ST.resp[id] ? " cheia" : ""),
                 ST.resp[id] ? B.s[t] : "");
      cxs.push(c); vaga.appendChild(c);
    }
    box.appendChild(vaga);
    var cx = el("div", "gotas"), usados = {};
    baralha(BANCO.sil.slice(0)).forEach(function(sb){
      var pos = -1, q;
      for(q = 0; q < B.s.length; q++) if(B.s[q] === sb && !usados[q]) { pos = q; break; }
      var b = el("button", "gota", sb);
      b.setAttribute("aria-label", sb);
      b.setAttribute("data-qa", (pos >= 0 ? "op-" + id + "-s" + pos
                                          : "no-" + id + "-g" + chaveQuadro(sb)));
      if(pos >= 0) usados[pos] = 1;
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falaDaSilaba(sb)();
        if(pos !== feitas){
          b.className = "gota nao";
          setTimeout(function(){ b.className = "gota"; }, 420);
          errou(id, "dica" + pi + "_" + k); return;
        }
        b.className = "gota usada";
        cxs[feitas].innerHTML = sb; cxs[feitas].className = "cxs2 cheia";
        feitas++;
        if(feitas === B.s.length){ acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
      };
      cx.appendChild(b);
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}

/* ===== BLOCO B — A MÁQUINA ACHA (10 a 12) ===== */

/* 10, 11 e 12 — ACHE OS PEDAÇOS CERTOS (T24, VERBATIM: "CIRCULE AS SÍLABAS DO
   NOME DAS FIGURAS E ESCREVA" · T29, VERBATIM: "Pinte os quadradinhos das
   sílabas que precisamos para formar as palavras de cada desenho")
   ⚠️ O par sobe de verdade: 10 tem UMA armadilha por item, 11 tem SEIS, e 12
      tem seis PARECIDAS (BAR para BOR, CRE para CLE) — que é o degrau difícil. */
function montaMarcar(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MAR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(M.f);
    lin.appendChild(el("div", "palgrande", M.p));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("mar_" + k); }));
    box.appendChild(lin);
    var pecas = [];
    M.g.forEach(function(sb, n){ pecas.push({k: "g" + n, t: sb, ok: 1}); });
    M.d.forEach(function(sb, n){ pecas.push({k: "d" + n, t: sb, ok: 0}); });
    marqueConfira(box, id, pi, baralha(pecas),
                  "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f10(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "São três pedaços e só <b>dois</b> servem. Marque os certos " +
            "e toque em Conferir.", "p" + pi + "enun");
  montaMarcar(d, pi);
}
function f11(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora há muitos pedaços sobrando. Diga a palavra devagar e " +
            "marque só os que você ouvir.", "p" + pi + "enun");
  montaMarcar(d, pi);
}
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cuidado: agora os pedaços errados são <b>parecidos</b> com " +
            "os certos.", "p" + pi + "enun");
  montaMarcar(d, pi);
}

/* ===== BLOCO C — A MÁQUINA TIRA (13 e 14) ===== */

/* 13 e 14 — TIRE UMA LETRA (T02, VERBATIM: "Elimine uma letra na primeira
   sílaba de cada palavra e escreva o nome dos desenhos")
   ⭐⭐ É o verbo REMOVER, que o currículo nomeia por extenso e que nenhuma outra
      folha da colheita pede. E o que sai é CCV → CV, que amarra no degrau de
      trás: a sílaba perde a segunda consoante e vira simples. */
function montaRemover(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var X = REM[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(X.f);
    lin.appendChild(botaoSom("Ouvir as duas palavras", function(){ falar("rem_" + k); }));
    box.appendChild(lin);
    tiraLetra(box, id, pi, X, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Tire <b>uma letra</b> do começo e aparece outra palavra. " +
            "Toque na letra que sai.", "p" + pi + "enun");
  montaRemover(d, pi);
}
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Tem sempre uma palavra escondida dentro da outra. Ache a " +
            "letra que está sobrando.", "p" + pi + "enun");
  montaRemover(d, pi);
}

/* ===== BLOCO D — A MÁQUINA TROCA (15 a 19) ===== */

/* 15 e 16 — TROQUE A PRIMEIRA LETRA (T28, VERBATIM: "Troca LETRAS forma
   PALAVRAS" — B/M/C + OLA → BOLA, MOLA, COLA)
   ⭐⭐⭐ A terminação fica PARADA e a letra da frente muda. É o degrau mais
      concreto do caderno: a criança vê a palavra nascer debaixo do dedo. */
function montaTrocaLetra(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var T = TRO[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var alvos = [], n;
    for(n = 0; n < T.ls.length; n++) alvos.push("t" + n);
    registra(id, pi, alvos.join(" "));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "palgrande", '<i class="lacuna peq"></i><span class="pd forte">' + T.fim + "</span>"));
    box.appendChild(lin);
    var cx = el("div", "juntas"), feitos = 0;
    T.ls.forEach(function(L, n){
      var linha = el("div", "juntalin");
      var b = el("button", "sil" + (ST.resp[id] ? " usada" : ""), L + " + " + T.fim);
      b.setAttribute("aria-label", "letra " + L + " mais " + T.fim);
      b.setAttribute("data-qa", "op-" + id + "-t" + n);
      var saida = el("span", "saida", ST.resp[id] ? T.r[n] : "");
      b.onclick = function(){
        if(ST.resp[id] || b.className.indexOf("usada") > -1) return;
        sPasso(); b.className = "sil usada"; saida.innerHTML = T.r[n];
        falar("pal_" + chaveQuadro(T.r[n]));
        feitos++;
        if(feitos === T.ls.length){ acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
      };
      linha.appendChild(b);
      linha.appendChild(el("span", "seta", "&rarr;"));
      linha.appendChild(saida);
      cx.appendChild(linha);
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}
function f15(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "O fim da palavra fica <b>parado</b>. Troque só a letra da " +
            "frente e veja quantas palavras saem.", "p" + pi + "enun");
  montaTrocaLetra(d, pi);
}
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Outra terminação parada, e de novo três palavras dentro " +
            "dela.", "p" + pi + "enun");
  montaTrocaLetra(d, pi);
}

/* 17 — TROQUE A LETRA DE DENTRO (T16, VERBATIM: "FORMANDO NOVAS PALAVRAS —
   TROQUE AS LETRAS INDICADAS E ESCREVA AS NOVAS PALAVRAS") */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora a letra que muda está <b>marcada</b>. Escolha a que " +
            "entra no lugar dela.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var Q = DEN[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    var mostra = "";
    Q.de.split("").forEach(function(L, n){
      mostra += n === Q.pos ? '<span class="lt marcada">' + L + "</span>"
                            : '<span class="lt">' + L + "</span>";
    });
    lin.appendChild(el("div", "palgrande", mostra));
    lin.appendChild(botaoSom("Ouvir a palavra nova", function(){ falar("den_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(Q.ops.map(function(L){
      return {v: L.toLowerCase(), rot: L, aria: "letra " + L, fala: "let_" + L.toLowerCase()};
    })), Q.r.toLowerCase(), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k,
    function(){ box.appendChild(el("div", "palgrande nova", Q.p)); });
    fechaItem(d, box, id);
  });
}

/* 18 e 19 — A TIRA (T13, VERBATIM: "Troca-sílaba — Monte o troca-sílaba.
   Depois, anote as palavras que você formou")
   ⭐⭐ A terminação fica parada numa janela e a criança encaixa a sílaba da tira.
      É a Roda das Sílabas do 1º ano um degrau acima: lá girava a VOGAL, aqui
      encaixa a SÍLABA inteira. */
function montaTira(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var X = TIRA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, "s" + chaveQuadro(X.ini));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Ache <b>" + X.r + "</b>."));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("pal_" + chaveQuadro(X.r)); }));
    box.appendChild(lin);
    var janela = el("div", "janela");
    var vaga = el("span", "sbjan", ST.resp[id] ? X.ini : "");
    janela.appendChild(vaga);
    janela.appendChild(el("span", "sbfixo", X.fim));
    box.appendChild(janela);
    var fita = el("div", "fita");
    X.tira.forEach(function(sb){
      var b = el("button", "sil", sb);
      b.setAttribute("aria-label", sb);
      b.setAttribute("data-qa", (sb === X.ini ? "op-" + id + "-s" + chaveQuadro(sb)
                                              : "no-" + id + "-f" + chaveQuadro(sb)));
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falaDaSilaba(sb)();
        if(sb !== X.ini){
          b.className = "sil nao";
          setTimeout(function(){ b.className = "sil"; }, 420);
          errou(id, "dica" + pi + "_" + k); return;
        }
        b.className = "sil usada";
        vaga.innerHTML = sb; janela.className = "janela pisca";
        falar("pal_" + chaveQuadro(X.r));
        acertou(id, "certo" + pi + "_" + k); box.className = "item feito";
      };
      fita.appendChild(b);
    });
    box.appendChild(fita);
    fechaItem(d, box, id);
  });
}
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Na janela, o fim <b>LHA</b> está parado. Encaixe o pedaço " +
            "da tira que forma a palavra pedida.", "p" + pi + "enun");
  montaTira(d, pi);
}
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora o fim parado é <b>NHO</b>. A tira mudou; o jeito é o " +
            "mesmo.", "p" + pi + "enun");
  montaTira(d, pi);
}

/* ===== BLOCO E — A MÁQUINA INVERTE (20 a 22) ===== */

/* 20, 21 e 22 — TROQUE OS PEDAÇOS DE LUGAR (T10, VERBATIM: "MUDA-SÍLABAS —
   MUDE A SÍLABA DE LUGAR E UMA NOVA PALAVRA IRÁ FORMAR")
   ⭐⭐⭐ É O CORAÇÃO DO DEGRAU e o que dá nome ao caderno. As MESMAS duas
      sílabas, na ordem trocada, são outra palavra — e a descoberta não se
      esquece. A 22 sobe: o segundo pedaço tem três ou quatro letras. */
function montaInverter(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var X = INV[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "palpeq", X.de));
    lin.appendChild(botaoSom("Ouvir as duas palavras", function(){ falar("inv_" + k); }));
    box.appendChild(lin);
    inverte(box, id, pi, X, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Puxe o pedaço de trás para a <b>frente</b> — e olhe o que " +
            "nasce.", "p" + pi + "enun");
  montaInverter(d, pi);
}
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "De novo: os mesmos dois pedaços, na ordem trocada.",
            "p" + pi + "enun");
  montaInverter(d, pi);
}
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Estas são mais difíceis: o segundo pedaço é maior. Diga a " +
            "palavra ao contrário antes de puxar.", "p" + pi + "enun");
  montaInverter(d, pi);
}

/* ===== BLOCO F — A MÁQUINA ACRESCENTA (23 e 24) ===== */

/* 23 e 24 — ACRESCENTE UM PEDAÇO (T09, VERBATIM: "ACRESCENTE A SÍLABA,
   FORMANDO UMA NOVA PALAVRA E A ESCREVA NA LINHA ABAIXO")
   ⭐⭐ O terceiro verbo do currículo. A 23 acrescenta no FIM e a 24 no COMEÇO —
      e é assim que as três posições da habilidade ficam cobertas. */
function montaAcrescentar(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var A = ACR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(A.f);
    lin.appendChild(el("div", "palgrande", A.onde === "fim"
      ? '<span class="pd">' + A.base + '</span><i class="lacuna"></i>'
      : '<i class="lacuna"></i><span class="pd">' + A.base + "</span>"));
    lin.appendChild(botaoSom("Ouvir a palavra nova", function(){ falar("acr_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, baralha(A.ops.map(function(sb){
      return {v: sb.toLowerCase(), rot: sb, aria: sb, fala: falaDaSilaba(sb)};
    })), A.r.toLowerCase(), "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k,
    function(){ box.appendChild(el("div", "palgrande nova", A.p)); });
    fechaItem(d, box, id);
  });
}
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ponha um pedaço <b>no fim</b> e a palavra vira outra. " +
            "Ouça qual é.", "p" + pi + "enun");
  montaAcrescentar(d, pi);
}
function f24(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora o pedaço entra <b>no começo</b>. Ouça a palavra " +
            "inteira antes de escolher.", "p" + pi + "enun");
  montaAcrescentar(d, pi);
}

/* ===== BLOCO G — A MÁQUINA RECORTA (25 e 26) ===== */

/* 25 e 26 — O FIM DE DUAS, UMA NOVA (T30, VERBATIM: "CIRCULE A SÍLABA FINAL DE
   CADA PALAVRA PARA FORMAR NOVAS PALAVRAS E ESCREVA")
   ⭐⭐⭐ A MELHOR DAS 40 FOLHAS. Duas figuras conhecidas geram uma terceira, e
      para isso a criança tem de OUVIR o fim de cada uma. É o gesto mais alto do
      degrau — e as dezoito figuras vêm todas desta mesma folha de papel. */
function montaFimDeDuas(d, pi){
  ST.folha["p" + pi].forEach(function(k, i){
    var X = FIM[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(botaoSom("Ouvir as três palavras", function(){ falar("fim_" + k); }));
    box.appendChild(lin);
    fimDeDuas(box, id, pi, X, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f25(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Pegue o <b>último</b> pedaço de cada palavra. Os dois juntos " +
            "formam uma palavra nova.", "p" + pi + "enun");
  montaFimDeDuas(d, pi);
}
function f26(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Mais três. Diga cada palavra devagar e pare no fim dela.",
            "p" + pi + "enun");
  montaFimDeDuas(d, pi);
}

/* ===== BLOCO H — O CÓDIGO (27 a 30) ===== */

/* 27 a 30 — O CÓDIGO DAS SÍLABAS (T19, VERBATIM: "DE ACORDO COM OS NÚMEROS
   ACIMA, FORME AS PALAVRAS" · T25 · T26 · T22)
   ⭐⭐ A sílaba vira NÚMERO e a criança decifra. Os quatro sobem juntos: duas
      sílabas, três, quatro e, no fim, o quadro dos encontros consonantais, onde
      BRAVO e CRAVO diferem por UMA letra. */
function montaCodigo(d, pi, qk){
  var Q = COD[qk];
  quadroCodigo(d, Q);
  ST.folha["p" + pi].forEach(function(k, i){
    var P = Q.pal[k], id = "n" + pi + "_" + i, box = item(i + 1);
    decodifica(box, id, pi, Q, P, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f27(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cada pedaço ganhou um <b>número</b>. Siga os números e a " +
            "palavra aparece.", "p" + pi + "enun");
  montaCodigo(d, pi, "q27");
}
function f28(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Outro quadro, e agora há palavras de <b>três</b> pedaços.",
            "p" + pi + "enun");
  montaCodigo(d, pi, "q28");
}
function f29(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora as palavras são compridas: <b>quatro</b> números cada " +
            "uma.", "p" + pi + "enun");
  montaCodigo(d, pi, "q29");
}
function f30(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Neste quadro os pedaços têm <b>duas consoantes juntas</b>. " +
            "Olhe bem: BRA e CRA mudam por uma letra só.", "p" + pi + "enun");
  montaCodigo(d, pi, "q30");
}

/* ===== BLOCO I — A PALAVRA NO MUNDO (31 a 35) ===== */

/* 31 — FALTAM AS DUAS PONTAS (T23, VERBATIM: "QUAL É A SÍLABA? — ESCREVA AS
   SÍLABAS, INICIAL E FINAL, DO NOME DE CADA DESENHO")
   ⭐⭐ É o INVERSO da folha da sílaba que falta do caderno anterior: lá faltava
      a do meio, aqui faltam as duas pontas e só a do meio é dada. */
function f31(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Só o pedaço do <b>meio</b> ficou. Ponha o do começo e o do " +
            "fim, nessa ordem.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PON[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, "z0 z1");
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(P.f);
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("pon_" + k); }));
    box.appendChild(lin);
    var vaga = el("div", "vagas");
    var c0 = el("span", "cxs2" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? P.ini : "");
    var cm = el("span", "cxs2 cheia dada", P.meio);
    var c1 = el("span", "cxs2" + (ST.resp[id] ? " cheia" : ""), ST.resp[id] ? P.fim : "");
    vaga.appendChild(c0); vaga.appendChild(cm); vaga.appendChild(c1);
    box.appendChild(vaga);
    var feitas = 0, alvo = [P.ini, P.fim], cxs = [c0, c1];
    var cx = el("div", "sils");
    baralha(P.ops.slice(0)).forEach(function(sb){
      var qual = alvo.indexOf(sb);
      var b = el("button", "sil", sb);
      b.setAttribute("aria-label", sb);
      b.setAttribute("data-qa", (qual >= 0 ? "op-" + id + "-z" + qual
                                           : "no-" + id + "-p" + chaveQuadro(sb)));
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falaDaSilaba(sb)();
        if(qual !== feitas){
          b.className = "sil nao";
          setTimeout(function(){ b.className = "sil"; }, 420);
          errou(id, "dica" + pi + "_" + k); return;
        }
        b.className = "sil usada";
        cxs[feitas].innerHTML = sb; cxs[feitas].className = "cxs2 cheia";
        feitas++;
        if(feitas === 2){ acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
      };
      cx.appendChild(b);
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}

/* 32 — COMEÇO, MEIO E FIM (T37, VERBATIM: "Escreva o nome das figuras,
   separando as sílabas e identifique a sílaba inicial, medial e final")
   ⭐⭐ É a única folha da colheita que dá NOME às três posições — e são as
      palavras que o currículo usa: *"iniciais, mediais ou finais"*. */
function f32(d, pi){
  gavetas(d, pi, "gA", "Em que lugar da palavra mora cada pedaço? Leve cada um " +
          "para a gaveta dele.");
}

/* 33 — A PALAVRA ENTRA NA FRASE (T39, VERBATIM: "COMPLETE AS FRASES COM AS
   PALAVRAS DA ATIVIDADE ACIMA")
   ⭐ É o degrau que faltava em tudo o que veio antes: a palavra montada sai da
      lista e vai para DENTRO de uma frase, onde ela significa alguma coisa.
   ⚠️ AS LETRAS VÊM EMBARALHADAS, na horizontal (ideia do Marcos) — e o teclado
      de verdade continua valendo, pela regra das duas portas. */
function f33(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Qual palavra falta na frase? Monte a palavra tocando nas " +
            "letras — ou digite no seu teclado.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var F = FRAS[k], id = "n" + pi + "_" + i, box = item(i + 1);
    /* ⚠️ A RESPOSTA DECLARADA É A PALAVRA, não um rótulo: é por ela que o
       jogador da banca digita, e é ela que o relatório mede. Escrever "esc"
       aqui fez a folha inteira não fechar na primeira medição. */
    registra(id, pi, F.w);
    var lin = el("div", "enunlin");
    lin.innerHTML = figOu(F.f);
    lin.appendChild(el("div", "frase", F.a + ' <i class="lacuna"></i> ' + F.z));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("fra_" + k); }));
    box.appendChild(lin);
    var grade = el("div", "cruz uma"), cels = [], t;
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < F.w.length; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""),
                 ST.resp[id] ? F.w.charAt(t) : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    box.appendChild(grade);
    var teclar = fileiraLetras(box, id, pi, F.w, cels,
                               "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    /* a outra porta: tocar na grade marca este item como o ativo, e o teclado
       de verdade passa a escrever nele */
    grade.onclick = function(){ if(!ST.resp[id]) ATIVO_LETRAS = teclar; };
    fechaItem(d, box, id);
  });
}

/* 34 — O DITADO DOS TRÊS LUGARES (T35, VERBATIM: "O JOGO DAS 3 PALAVRAS —
   PREENCHA ESTE PRIMEIRO QUADRO COM AS SÍLABAS QUE FOREM DITADAS E ENCONTRE 3
   PALAVRAS, NA CARTELA, QUE PODEM SER COMPLETADAS COM CADA SÍLABA, TANTO NO
   INÍCIO, NO MEIO E NO FIM DAS PALAVRAS")
   ⭐⭐⭐ É O FECHO DO CADERNO. Uma sílaba só serve em TRÊS lugares diferentes —
      a ideia grande do degrau inteiro numa folha — e ainda chega por VOZ. */
function f34(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Ouça o pedaço ditado. Ele cabe em <b>três</b> palavras da " +
            "cartela: no começo, no meio e no fim. Marque as três.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var D = DIT[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "palgrande", '<span class="pd forte">' + D.sb + "</span>"));
    lin.appendChild(botaoSom("Ouvir o pedaço ditado", falaDaSilaba(D.sb)));
    box.appendChild(lin);
    var pecas = [];
    D.ok.forEach(function(o, n){ pecas.push({k: "c" + n, t: o.l, ok: 1}); });
    D.no.forEach(function(l, n){ pecas.push({k: "e" + n, t: l, ok: 0}); });
    marqueConfira(box, id, pi, baralha(pecas),
                  "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* 35 — O CARTAZ QUE VOCÊ LEVA (T34, VERBATIM: "ESCREVA DUAS PALAVRAS INICIANDO
   COM CADA SÍLABA EM DESTAQUE")
   ⭐⭐ O CONCEITO VEM POR ÚLTIMO, e isso é a LEI da casa (`EDUVERSE-FILOSOFIA.md`,
      Portão 0): a criança passou trinta e quatro folhas tirando, trocando,
      invertendo e acrescentando — só agora ela recebe as quatro palavras que
      dão nome ao que já sabe fazer. Se este cartaz viesse na folha 1, seria
      aula de decorar nome difícil.
   ⭐ E o cartaz não chega pronto: ela o monta. O cartaz que ela leva para o
      caderno é o que ela construiu. */
function f35(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Você já sabe fazer tudo isto. Agora as palavras que dão " +
            "nome: leve cada exemplo para a linha dele.", "p" + pi + "enun");
  var cart = el("div", "cartaz"), linhas = {}, listaC = [];
  CART.linhas.forEach(function(L){
    var l = el("div", "cartlin");
    var t = el("div", "cartit");
    t.innerHTML = "<b>" + L.t + "</b><span>" + L.d + "</span>";
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
    var b = el("button", "op pal" + (ST.resp[id] ? " usada" : ""), X.p);
    b.setAttribute("aria-label", X.p);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    if(ST.resp[id]) linhas[X.c]._dentro.appendChild(el("span", "fdentro", X.p));
    function larga(l){
      if(ST.resp[id]) return;
      if(l._v === X.c){
        b.className = "op pal usada";
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
      sPasso(); falar("exe_" + k);
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
    };
    puxavel(b, listaC, function(l){ larga(l); });
    banco.appendChild(b);
  });
  listaC.forEach(function(l){
    l.onclick = function(){ if(marcada && marcada._larga) marcada._larga(l); };
  });
  d.appendChild(banco);
}
