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
var LIGAR = [13, 14, 25];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
var CORES = ["c1", "c1", "c1", "c1", "c1", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c3", "c3", "c3", "c3", "c3", "c4", "c4", "c4", "c4", "c4", "c4", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5"];


function faixa(d, i, titulo){ d.appendChild(el("div", "faixa", '<div class="num">' + i + '</div><h2>' + titulo + '</h2>')); }
function aoAbrir(d, fn){ if(!d._aoAbrir) d._aoAbrir = []; d._aoAbrir.push(fn); }
/* ---------- O ALTO-FALANTE ----------
   Regra da casa: tudo o que a criança PRECISA LER tem que poder ser OUVIDO.
   O desenho do botão é CSS puro: nada de emoji (vira quadradinho nos PCs da
   escola). */
function botaoSom(rot, aoTocar, cls){
  var b = el("button", cls || "som");
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
/* ⚠️⚠️ O ACENTO TEM DE SUMIR DO MESMO JEITO NOS DOIS LADOS (21/set/2026,
   defeito que chegou à sala: *"as palavras estão sendo ditas erradas"*).
   Quem grava a voz (`gerar_falas.py`, função `ch`) tira o acento por NFKD:
   ã vira A, ç vira C — e arquiva a fala em `pal_aviao`, `pal_laco`.
   Esta função APAGAVA a letra acentuada em vez de trocá-la, então o app pedia
   `pal_avio` e `pal_lao`, que não existem. O `falar()` volta calado quando a
   chave não existe: a criança tocava o alto-falante de AVIÃO, CAMALEÃO,
   CARROÇA, CHORÃO, DOMINÓ, DRAGÃO, LAÇO, LEÃO, POÇO e NÃO OUVIA NADA.
   ⚠️ E JÁ TINHA SIDO CONSERTADO UMA VEZ — no `_aumdim2`, com outro nome
   (`chavePal`) e até com o comentario certo: *"as pontas têm de casar, senão a
   voz procura um mp3 que não existe"*. Consertei num caderno e não levei aos
   outros dezesseis. Defeito medido em código gêmeo se conserta em TODOS os
   lugares na mesma rodada — esta é a segunda vez que a casa paga por isso. */
var SEMACENTO = {"á":"a","à":"a","â":"a","ã":"a","ä":"a","é":"e","è":"e","ê":"e","ë":"e",
  "í":"i","ì":"i","î":"i","ï":"i","ó":"o","ò":"o","ô":"o","õ":"o","ö":"o",
  "ú":"u","ù":"u","û":"u","ü":"u","ç":"c","ñ":"n"};
function chaveQuadro(w){
  return String(w).toLowerCase().replace(/[^a-z]/g, function(c){ return SEMACENTO[c] || ""; });
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
    /* ⚠️ O ALTO-FALANTE DA RESPOSTA, e ele é DISCRETO e vem ANTES da escolha.
       Pergunta do Marcos (20/set/2026): *"a atividade tem áudio para ajudar os
       que não sabem ler? O alto-falante discreto para clicar caso o estudante
       queira ouvir"*. A resposta era NÃO: a opção tinha `fala`, mas o motor só
       a tocava DEPOIS do clique — ou seja, a criança tinha de ESCOLHER para
       ouvir, e aí já tinha respondido. O portão `1o` media a metade errada
       (cobrava o campo `fala` existir, não a criança poder ouvir antes).
       Quem não lê agora ouve cada resposta quantas vezes quiser e só então
       escolhe — que é a regra da casa de ago/2026, enfim cumprida.
       ⚠️ Botão IRMÃO, nunca dentro do outro: botão dentro de botão é HTML
       inválido e o clique vaza para a resposta. O `botaoSom` já faz
       `stopPropagation`. */
    if(o.fala){
      var w = el("div", "opw" + (cls && cls.indexOf("frase") > -1 ? " larga" : ""));
      w.appendChild(b);
      w.appendChild(botaoSom("Ouvir esta resposta",
        (function(f){ return function(){ falar(f); }; })(o.fala), "som somop"));
      box.appendChild(w);
    } else {
      box.appendChild(b);
    }
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
  var caps = [f0, f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35], i;
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
  /* ⭐ A CAPA É UMA CENA COM AS FIGURAS DO PRÓPRIO CADERNO (regra 0b11): o
     relógio da F08 marcando a hora da aula e o material dourado do G06
     repartido em dois grupos — os dois assuntos do caderno numa olhada. */
  var c = el("div", "capa"), nome = "APRENDENDO A DIVISÃO E AS HORAS", k, letras = "";
  nome.split(" ").forEach(function(pal, w){
    var s = "";
    for(k = 0; k < pal.length; k++) s += '<span class="lt">' + pal.charAt(k) + '</span>';
    letras += (w ? '<span class="esp"></span>' : '') + '<span class="tpal">' + s + '</span>';
  });
  var grupo = img("dh4_barra.png", "cbarra", "") + img("dh4_barra.png", "cbarra", "") +
              img("dh4_cubo.png", "ccubo", "") + img("dh4_cubo.png", "ccubo", "") + img("dh4_cubo.png", "ccubo", "");
  c.innerHTML =
    '<div class="ceu"></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Matemática &middot; 4º ano &middot; 35 folhas para dividir com o ' +
      'material dourado e na chave, e para ler e contar as horas</div>' +
    '<div class="cena capdh4">' +
      '<div class="capgrupo">' + grupo + '<b>23</b></div>' +
      '<div class="caprel">' + relogioHTML(10, 10, "rcapa") + '</div>' +
      '<div class="capgrupo">' + grupo + '<b>23</b></div>' +
    '</div>' +
    '<div class="chamada">46 ÷ 2 = 23: duas barras e três cubinhos em cada grupo. ' +
      'E o relógio? Marca <b>10h10</b>. Escreva o seu nome ali embaixo e toque em ' +
      '<b>Começar</b>.</div>';
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
   AS PEÇAS DESTE CADERNO — as que já existiam vêm COPIADAS do `_div3` (o
   caderno da divisão do 3º ano, que passou pela banca e pelo parecer):
   `reparte`/`montaReparte`, `escreveNum`, `marqueConfira`, `opNumeros`,
   `figs`, a trilha e a memória. As NOVAS são o relógio de ponteiros e a
   chave armada, e cada uma diz de qual folha de papel nasceu.
   ============================================================ */

/* ---------- utilidades de número e de hora ---------- */
function dois(n){ return (n < 10 ? "0" : "") + n; }
function hhmm(h, m){ return dois(h) + ":" + dois(m); }
function hmin(h, m){ return h + ":" + dois(m); }
/* a fala de um horário ou de uma conta — a CHAVE é a mesma que o gerador grava */
function fHora(h, m){ return "hora_" + h + "_" + m; }
function fConta(a, b){ return "conta_" + a + "_" + b; }
function fNum(n){ return "num_" + n; }

/* ---------- a fileira de números (do `_div3`) ----------
   ⚠️ O LEQUE TEM DE CONTER A RESPOSTA (lição do `_div3`, 24/set/2026): quando
      a resposta passa do teto, as mesmas casas aparecem numa JANELA em volta
      dela. Aqui as respostas vão até 143, então a janela é a regra, não a
      exceção. */
function opNumeros(certo, ate){
  var lista = [], n, quantas = ate || 10;
  var r = parseInt(String(certo).replace(/^r/, ""), 10);
  var de = 1;
  if(r > quantas) de = Math.max(1, r - Math.floor(quantas / 2));
  for(n = de; n < de + quantas; n++)
    lista.push({v: "r" + n, rot: String(n), aria: String(n), fala: fNum(n)});
  return lista;
}
function figs(f, q, quantas){
  var s = "", n;
  for(n = 0; n < quantas; n++) s += img(f, "figmicro", q);
  return s;
}
/* opções que são FRASES: a primeira do dado é a certa; a tela embaralha.
   A fala de cada uma é `<pref><i>` (gravada pelo gerador na ordem do dado). */
function opFrases(lista, pref){
  return baralha(lista.map(function(t, i){
    return {v: "o" + i, rot: t, aria: t, fala: pref + i};
  }));
}

/* ============================================================
   ⭐ O RELÓGIO DE PONTEIROS — a peça da folha F08 (= C40)
   *"Faça seu próprio relógio. Instruções: Imprima em papelão. Recorte o
   relógio abaixo e fixe os ponteiros do relógio com um prendedor de papel."*
   O mostrador e os DOIS ponteiros são os da folha, recortados; na tela eles
   giram. Nada de ponteiro desenhado em CSS.

   ⚠️ A GEOMETRIA FOI MEDIDA NO PNG, não no olho (`_divh4/recortar_das_folhas.py`
      e a medida que está no POTE): o centro do mostrador é 49,9% × 49,9%; o
      PINO de cada ponteiro (a bolinha da ponta de trás) fica a 12,9% (hora) e
      15,7% (minuto) da largura, na metade da altura. O ponteiro é posto com o
      PINO no centro do mostrador — `translate(-pino)` — e gira em volta do
      pino: `transform-origin` no mesmo ponto.
   ⚠️ O PONTEIRO DAS HORAS ANDA JUNTO. Duas folhas colhidas (C03, C15) desenham
      o ponteiro das horas cravado no número em hora quebrada — 3:30 com o
      ponteiro EXATAMENTE no 3. Aqui ele anda meio grau por minuto, como num
      relógio de verdade: às 3:30 ele está no meio entre o 3 e o 4.
   ============================================================ */
var PINO = {h: [12.86, 49.54], m: [15.71, 49.62]};
function ponteiro(tipo, graus){
  var p = PINO[tipo], tr = "translate(-" + p[0] + "%,-" + p[1] + "%) rotate(" + (graus - 90) + "deg)";
  return '<div class="pont pont' + tipo + '" style="-webkit-transform-origin:' + p[0] + '% ' + p[1] +
         '%;transform-origin:' + p[0] + '% ' + p[1] + '%;-webkit-transform:' + tr + ';transform:' + tr + '">' +
         img(tipo === "h" ? "dh4_ponthora.png" : "dh4_pontmin.png", "pontimg", "") + "</div>";
}
function relogioHTML(h, m, cls){
  var gh = (h % 12) * 30 + m * 0.5, gm = m * 6;
  return '<div class="relog' + (cls ? " " + cls : "") + '" aria-label="relógio marcando ' + hmin(h, m) + '">' +
         img("dh4_mostrador.png", "mostr", "mostrador do relógio") +
         ponteiro("h", gh) + ponteiro("m", gm) + '<i class="pino"></i></div>';
}
/* ⭐⭐ O RELÓGIO QUE A CRIANÇA GIRA (folhas 23 e 24). AS TRÊS PORTAS:
      · ARRASTAR o ponteiro dos minutos com o dedo ou o mouse (o gesto da F08);
      · os BOTÕES de 5 minutos e de 1 hora (quem não consegue arrastar);
      · a RÉGUA de baixo (teclado e leitor de tela).
   ⚠️ SÓ O BOTÃO CONFERIR DIZ SE ESTÁ CERTO. Conferir a cada movimento daria o
      acerto a quem passou pelo horário sem querer, girando. O jogador da banca
      (família SIMULADOR: `sim-<id>` + `data-vai`) mexe na régua com um evento
      que não é da criança (`isTrusted` falso) — e só esse confere sozinho. */
function relogioGira(box, pi, id, k, h, m){
  var alvo = (h % 12) * 60 + m;
  registra(id, pi, String(alvo));
  var t = ST.resp[id] ? alvo : 0;           /* começa no 12:00 */
  var cx = el("div", "relgira");
  var rel = el("div", "relcx");
  cx.appendChild(rel);
  var mostra = el("div", "reldig");
  cx.appendChild(mostra);
  function desenha(){
    var hh = Math.floor(t / 60), mm = t % 60;
    rel.innerHTML = relogioHTML(hh === 0 ? 12 : hh, mm, "grande");
    mostra.innerHTML = "O seu relógio: <b>" + hmin(hh === 0 ? 12 : hh, mm) + "</b>";
    reg.value = String(t);
  }
  function anda(d){ if(ST.resp[id]) return; t = (t + d + 720) % 720; desenha(); }
  var bts = el("div", "relbts");
  [["−1 h", -60, "Voltar uma hora"], ["−5 min", -5, "Voltar cinco minutos"],
   ["+5 min", 5, "Avançar cinco minutos"], ["+1 h", 60, "Avançar uma hora"]].forEach(function(B){
    var b = el("button", "bt cinza relbt", B[0]);
    b.setAttribute("aria-label", B[2]);
    b.onclick = function(){ sTecla(); anda(B[1]); };
    bts.appendChild(b);
  });
  var reg = document.createElement("input");
  reg.type = "range"; reg.min = "0"; reg.max = "715"; reg.step = "5";
  reg.className = "relreg";
  reg.setAttribute("aria-label", "Girar o relógio");
  reg.setAttribute("data-qa", "sim-" + id);
  reg.setAttribute("data-vai", String(alvo));
  reg.addEventListener("input", function(ev){
    if(ST.resp[id]) return;
    t = parseInt(reg.value, 10) || 0; desenha();
    if(ev.isTrusted === false) confere();
  });
  var cf = el("button", "bt verde pronto", "Conferir");
  cf.onclick = function(){ sPasso(); confere(); };
  function confere(){
    if(ST.resp[id]) return;
    if(t === alvo){ cf.style.display = "none"; acertou(id, "certo" + pi + "_" + k); box.className = "item feito"; }
    else errou(id, "dica" + pi + "_" + k);
  }
  /* o arrasto: o ângulo do dedo em volta do centro vira o ponteiro dos minutos,
     de 5 em 5; se ele passa pelo 12, a hora anda junto — para a frente ou
     para trás, como no relógio de verdade. */
  var pega = false;
  function ang(ev){
    var r = rel.getBoundingClientRect();
    var x = ev.clientX - (r.left + r.width / 2), y = ev.clientY - (r.top + r.height / 2);
    var a = Math.atan2(x, -y) * 180 / Math.PI; if(a < 0) a += 360;
    return a;
  }
  rel.style.touchAction = "none";
  rel.addEventListener("pointerdown", function(ev){
    if(ST.resp[id]) return; pega = true;
    try{ rel.setPointerCapture(ev.pointerId); }catch(e){}
  });
  rel.addEventListener("pointermove", function(ev){
    if(!pega) return;
    var novo = (Math.round(ang(ev) / 30) % 12) * 5, velho = t % 60, d = novo - velho;
    if(d > 30) d -= 60; if(d < -30) d += 60;
    if(d){ t = (t + d + 720) % 720; desenha(); }
  });
  function solta(){ pega = false; }
  rel.addEventListener("pointerup", solta);
  rel.addEventListener("pointercancel", solta);
  cx.appendChild(bts);
  cx.appendChild(reg);
  box.appendChild(cx);
  box.appendChild(cf);
  if(ST.resp[id]) cf.style.display = "none";
  desenha();
}

/* ============================================================
   ⭐ A CHAVE — a conta armada do jeito que o papel brasileiro a arma
   (A01, A11, A16, A37, A39, B04…): dividendo à esquerda, divisor dentro da
   chave, o quociente escrito EMBAIXO do divisor e o resto embaixo do
   dividendo. ⚠️ B22 usa a notação americana (a "casinha") e ficou de fora
   justamente por isso: a criança de Blumenau arma a conta assim.
   A criança escreve o quociente — e, quando a folha pede, o resto — nas
   casinhas, pelo teclado da tela ou o de verdade (as duas portas).
   ============================================================ */
function escreveChave(box, pi, id, k, a, b, comResto){
  var q = Math.floor(a / b), r = a % b;
  var alvo = String(q) + (comResto ? String(r) : "");
  registra(id, pi, alvo);
  var ch = el("div", "chave");
  ch.appendChild(el("div", "chdiv", String(a)));
  ch.appendChild(el("div", "chdsr", String(b)));
  var cRes = el("div", "chres"), cQuo = el("div", "chquo");
  ch.appendChild(cRes); ch.appendChild(cQuo);
  var cels = [], t, feito = !!ST.resp[id];
  function casa(pai, ch2){
    var c = el("button", "ccel viva" + (feito ? " ok" : ""), feito ? ch2 : "");
    c.setAttribute("aria-label", "Casa do resultado");
    cels.push(c); pai.appendChild(c);
  }
  cQuo.setAttribute("data-qa", "esc-" + id);
  for(t = 0; t < String(q).length; t++) casa(cQuo, String(q).charAt(t));
  if(comResto){
    cRes.appendChild(el("span", "chrot", "resto"));
    for(t = 0; t < String(r).length; t++) casa(cRes, String(r).charAt(t));
  }
  box.appendChild(ch);
  var E = {id: id, w: alvo, cels: cels, bt: null, k: k,
           rot: comResto ? "Escreva o quociente e depois o resto" : "Escreva o quociente"};
  function abre(){ if(!ST.resp[id]) abreCruz(E, pi); }
  cQuo.onclick = abre; cRes.onclick = abre;
}

/* ---------- a casinha de escrever um número (do `_div3`) ----------
   `grupos` separa as casinhas com um sinal entre elas — o `:` das horas. */
function escreveNum(box, pi, id, k, alvo, contaHTML, rot, grupos){
  var conta = el("div", "contafato");
  conta.innerHTML = contaHTML || "";
  var grade = el("div", "cruz uma"), cels = [], t;
  grade.setAttribute("data-qa", "esc-" + id);
  alvo = String(alvo);
  registra(id, pi, alvo);
  for(t = 0; t < alvo.length; t++){
    if(grupos && grupos.indexOf(t) > -1) grade.appendChild(el("span", "doisp", ":"));
    var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""),
               ST.resp[id] ? alvo.charAt(t) : "");
    c.setAttribute("aria-label", "Casa do resultado");
    cels.push(c); grade.appendChild(c);
  }
  conta.appendChild(grade);
  box.appendChild(conta);
  var E = {id: id, w: alvo, cels: cels, bt: null, rot: rot, k: k};
  grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
  cels.forEach(function(c2){
    c2.addEventListener("click", function(){ if(!ST.resp[id]) abreCruz(E, pi); });
  });
}

/* ---------- REPARTIR ARRASTANDO (do `_div3`, sem a medida) ---------- */
function reparte(d, pi, texto, fonte){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, idx){
    var R = fonte[k], cada = R.n / R.k;
    var id = "n" + pi + "_" + idx, box = item(idx + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", "<b>" + R.n + " " + R.q + "</b> para <b>" + R.k + " " +
      R.w + "</b>. Reparta em partes iguais."));
    lin.appendChild(botaoSom("Ouvir o que a folha pede", function(){ falar("rep" + pi + "_" + k); }));
    box.appendChild(lin);
    var cols = el("div", "colunas potes"), listaC = [], p;
    for(p = 0; p < R.k; p++){
      var c = el("div", "coluna pote");
      var tt = el("div", "ctit", "CAIXA " + (p + 1));
      tt.setAttribute("data-alvo", "1");
      c.setAttribute("data-qa", "pote-" + id + "-" + p);
      c.appendChild(tt);
      var dentro = el("div", "cdentro"); c.appendChild(dentro);
      c._dentro = dentro; c._tem = 0;
      listaC.push(c); cols.appendChild(c);
    }
    box.appendChild(cols);
    var banco = el("div", "figbanco");
    box.appendChild(banco);
    montaReparte(pi, idx, k, R, cada, listaC, banco, box);
    fechaItem(d, box, id);
  });
}
function montaReparte(pi, idx, k, R, cada, listaC, banco, box){
  var id = "n" + pi + "_" + idx, postas = 0, n, marcada = null;
  registra(id, pi, "rep:" + R.k + "x" + cada);
  function larga(col){
    if(ST.resp[id] || !marcada) return;
    if(col._tem >= cada){
      col.className = "coluna pote erro";
      setTimeout(function(){ col.className = "coluna pote"; }, 500);
      errou(id, "dicarep" + pi + "_" + k);
      return;
    }
    col._tem++;
    col._dentro.appendChild(el("span", "fdentro", img(R.f, "figmicro", R.q)));
    marcada.parentNode.removeChild(marcada); marcada = null;
    postas++;
    if(postas === R.n){ acertou(id, "certorep" + pi + "_" + k); box.className = "item feito"; }
    else sPasso();
  }
  for(n = 0; n < R.n; n++){
    (function(n){
      var b = el("button", "op figbt", img(R.f, "figmini", R.q));
      b.setAttribute("aria-label", "pirulito " + (n + 1));
      b.setAttribute("data-qa", "item-" + id + "-" + n);
      b.setAttribute("data-alvo", "1");
      b.onclick = function(){
        if(b._arrastou){ b._arrastou = false; return; }
        if(ST.resp[id]) return;
        sPasso();
        if(marcada === b){ b.className = "op figbt"; marcada = null; return; }
        if(marcada) marcada.className = "op figbt";
        b.className = "op figbt marcada"; marcada = b;
      };
      puxavel(b, listaC, function(col){ marcada = b; larga(col); });
      banco.appendChild(b);
    })(n);
  }
  listaC.forEach(function(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_peca"); return; }
      larga(col);
    };
  });
  if(ST.resp[id]){
    banco.innerHTML = "";
    listaC.forEach(function(col){
      var t;
      for(t = 0; t < cada; t++) col._dentro.appendChild(el("span", "fdentro", img(R.f, "figmicro", R.q)));
    });
    box.className = "item feito";
  }
}

/* ---------- MARCAR VÁRIOS + CONFERIR (do `_div3`) ---------- */
function marqueConfira(box, id, pi, pecas, fCerto, fDica, aoAcertar){
  var feito = !!ST.resp[id], marcadas = {}, bts = [];
  registra(id, pi, pecas.filter(function(p){ return p.ok; })
                        .map(function(p){ return p.k; }).join(" "));
  var cx = el("div", "sils");
  pecas.forEach(function(P){
    var b = el("button", "sil" + (feito && P.ok ? " ok" : ""), P.t);
    b.setAttribute("aria-label", P.aria || P.t);
    b.setAttribute("data-qa", (P.ok ? "op-" : "no-") + id + "-" + P.k);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      if(P.fala) P.fala();
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
      if(aoAcertar) aoAcertar();
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
/* ⚠️ `bt: null` DE PROPÓSITO (26/set/2026): o `abreCruz` do motor troca a
   classe do `E.bt` para "pista ativa" — ele foi escrito para a PISTA da
   cruzadinha. No `_div3` o `bt` era a própria grade de casinhas, e abrir o
   teclado apagava a classe `cruz uma` dela. Aqui a casinha não tem pista. */

/* ============================================================
   ⭐⭐ A MESA DO MATERIAL DOURADO — pedido do Marcos (26/set/2026):
   *"Divisão com ajuda do material dourado"*.
   As peças (placa = 100, barra = 10, cubinho = 1) são RECORTADAS das folhas
   de papel colhidas (`_divh4/recortar_das_folhas.py`); nada é desenhado.

   O GESTO É O DA SALA: a criança leva cada peça para um grupo, dando a volta,
   até os grupos ficarem iguais. E quando sobra uma BARRA que não dá para pôr
   inteira em todos os grupos, ela a leva para a CASA DA TROCA — a barra vira
   DEZ CUBINHOS, que se repartem também. É o "abaixa" da conta armada, feito
   com a mão ANTES de ser feito com o lápis (concreto → figural → simbólico).

   ⚠️ O GRUPO NÃO ACEITA ALÉM DA SUA PARTE de cada peça: passar é o erro que a
      folha existe para mostrar ("esse grupo já tem as barras dele").
   ⚠️ A TROCA SÓ VALE QUANDO É PRECISA: trocar uma barra que ainda cabia inteira
      em cada grupo é desmanchar à toa — a dica diz isso.
   ⚠️ O JOGADOR DA BANCA não tem como deduzir esta ordem, então ela é
      DECLARADA (`seq:` — família nova em `_qa/joga_folha.js`, mesmo commit).
   ============================================================ */
function cdu(n){ return {c: Math.floor(n / 100), d: Math.floor(n / 10) % 10, u: n % 10}; }
var PECA = {p: {f: "dh4_placa.png", n: "placa", v: 100},
            b: {f: "dh4_barra.png", n: "barra", v: 10},
            u: {f: "dh4_cubo.png", n: "cubinho", v: 1}};
function materialHTML(n){
  var p = cdu(n), s = "", i;
  for(i = 0; i < p.c; i++) s += img(PECA.p.f, "mdplaca", "placa");
  for(i = 0; i < p.d; i++) s += img(PECA.b.f, "mdbarra", "barra");
  for(i = 0; i < p.u; i++) s += img(PECA.u.f, "mdcubo", "cubinho");
  return '<div class="mdmat">' + s + "</div>";
}
function mesaDourado(box, pi, id, k, a, b){
  var q = a / b, P = cdu(a), Q = cdu(q);
  var sobraB = P.d - b * Q.d;                 /* barras que precisam de troca */
  var quer = {p: Q.c, b: Q.d, u: Q.u};        /* a parte de cada grupo */
  /* o plano declarado: placas, depois barras, depois as trocas, depois cubinhos */
  var plano = [], g, t, n = {p: 0, b: 0, u: 0};
  ["p", "b"].forEach(function(tp){
    for(g = 0; g < b; g++) for(t = 0; t < quer[tp]; t++)
      plano.push("item-" + id + "-" + tp + (n[tp]++), "pote-" + id + "-g" + g);
  });
  for(t = 0; t < sobraB; t++) plano.push("item-" + id + "-b" + (n.b++), "troca-" + id);
  var cubos = [];
  for(t = 0; t < P.u; t++) cubos.push("u" + t);
  for(t = 0; t < sobraB * 10; t++) cubos.push("t" + t);
  var ci = 0;
  for(g = 0; g < b; g++) for(t = 0; t < Q.u; t++) plano.push("item-" + id + "-" + cubos[ci++], "pote-" + id + "-g" + g);
  registra(id, pi, "seq:" + plano.join(" "));

  var feito = !!ST.resp[id], marcada = null, postas = 0, total = P.c + (P.d - sobraB) + P.u + sobraB * 10;
  var mesa = el("div", "mdmesa");
  var grupos = el("div", "colunas potes mdgrupos"), listaG = [];
  for(g = 0; g < b; g++){
    var c = el("div", "coluna pote");
    var tt = el("div", "ctit", "GRUPO " + (g + 1)); tt.setAttribute("data-alvo", "1");
    c.appendChild(tt);
    c.setAttribute("data-qa", "pote-" + id + "-g" + g);
    var dentro = el("div", "cdentro"); c.appendChild(dentro);
    c._dentro = dentro; c._tem = {p: 0, b: 0, u: 0};
    listaG.push(c); grupos.appendChild(c);
  }
  var troca = null;
  if(sobraB){
    troca = el("div", "coluna pote mdtroca", '<div class="ctit">CASA DA TROCA<br><small>1 barra = 10 cubinhos</small></div>');
    troca.setAttribute("data-qa", "troca-" + id);
  }
  var banco = el("div", "figbanco mdbanco");
  function peca(tp, nome){
    var bt = el("button", "op figbt md" + tp, img(PECA[tp].f, "md" + tp + "img", PECA[tp].n));
    bt.setAttribute("aria-label", PECA[tp].n);
    bt.setAttribute("data-qa", "item-" + id + "-" + nome);
    bt.setAttribute("data-alvo", "1");
    bt._tp = tp;
    bt.onclick = function(){
      if(bt._arrastou){ bt._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("pc_" + tp);
      if(marcada === bt){ bt.className = "op figbt md" + tp; marcada = null; return; }
      if(marcada) marcada.className = "op figbt md" + marcada._tp;
      bt.className = "op figbt md" + tp + " marcada"; marcada = bt;
    };
    puxavel(bt, troca ? listaG.concat([troca]) : listaG, function(alvo){ marcada = bt; larga(alvo); });
    banco.appendChild(bt);
    return bt;
  }
  var nt = 0;
  function larga(alvo){
    if(ST.resp[id] || !marcada) return;
    var tp = marcada._tp;
    if(alvo === troca){
      /* só barra se troca, e só quando cada grupo já tem as barras dele */
      var cheias = listaG.every(function(G){ return G._tem.b >= quer.b; });
      if(tp !== "b" || !cheias){
        alvo.className = "coluna pote mdtroca erro";
        setTimeout(function(){ alvo.className = "coluna pote mdtroca"; }, 500);
        errou(id, tp !== "b" ? "dicatroca1_" + pi : "dicatroca2_" + pi);
        return;
      }
      marcada.parentNode.removeChild(marcada); marcada = null;
      sCerto(); falar("trocou");
      for(var z = 0; z < 10; z++) peca("u", "t" + (nt++));
      alvo.className = "coluna pote mdtroca feita";
      setTimeout(function(){ alvo.className = "coluna pote mdtroca"; }, 700);
      return;
    }
    if(alvo._tem[tp] >= quer[tp]){
      alvo.className = "coluna pote erro";
      setTimeout(function(){ alvo.className = "coluna pote"; }, 500);
      errou(id, "dicamd" + pi + "_" + tp + (tp === "b" && sobraB && quer.b === 0 ? "0" : ""));
      return;
    }
    alvo._tem[tp]++;
    alvo._dentro.appendChild(el("span", "fdentro", img(PECA[tp].f, "md" + tp + "mini", PECA[tp].n)));
    marcada.parentNode.removeChild(marcada); marcada = null;
    postas++;
    if(postas === total){
      acertou(id, "certomd" + pi + "_" + k);
      box.className = "item feito";
    } else sPasso();
  }
  listaG.concat(troca ? [troca] : []).forEach(function(G){
    G.onclick = function(){ if(!marcada){ sPasso(); falar("toque_peca"); return; } larga(G); };
  });
  mesa.appendChild(grupos);
  if(troca) mesa.appendChild(troca);
  box.appendChild(mesa);
  box.appendChild(banco);
  var rev = el("div", "ajuda cent");
  rev.appendChild(nomeSecreto("Cada grupo ficou com " +
    (Q.c ? Q.c + (Q.c > 1 ? " placas, " : " placa, ") : "") +
    Q.d + (Q.d === 1 ? " barra" : " barras") + " e " + Q.u + (Q.u === 1 ? " cubinho" : " cubinhos") +
    ": " + a + " ÷ " + b + " = " + q + ".", id));
  box.appendChild(rev);
  if(feito){
    listaG.forEach(function(G){
      ["p", "b", "u"].forEach(function(tp){
        for(var z = 0; z < quer[tp]; z++) G._dentro.appendChild(el("span", "fdentro", img(PECA[tp].f, "md" + tp + "mini", "")));
      });
    });
    box.className = "item feito";
    return;
  }
  for(t = 0; t < P.c; t++) peca("p", "p" + t);
  for(t = 0; t < P.d; t++) peca("b", "b" + t);
  for(t = 0; t < P.u; t++) peca("u", "u" + t);
}


/* ============================================================
   AS 35 FOLHAS. Cada bloco diz de qual folha de papel nasceu e o comando
   impresso VERBATIM. O crivo das 190 está em `_sequencias/POTE-DIVH4.md`.

   ⚠️ A ESCADA, EM UMA LINHA: repartir com a mão (1) → os problemas das duas
      perguntas (2-3) → julgar e nomear (4-5) → ⭐ O MATERIAL DOURADO: conhecer
      as peças, repartir, a casa da troca (6-8) → A CHAVE: com o material ao
      lado, com troca, com resto (9-11) → estimar e o divisor de dois
      algarismos (12-14) → exata ou não (15) → a multiplicação que confere (16)
      → os RESTOS IGUAIS (17-18) → o quebra-cabeça e elaborar (19-20) → LER AS
      HORAS: os minutos, ler, girar, ligar, as partes do dia (21-26) → hora,
      minuto, segundo e a PONTE: minutos em horas é dividir por 60 (27-28) →
      QUANTO TEMPO PASSOU (29-33) → a memória e o cartaz (34-35).
   ============================================================ */

/* ===== BLOCO A — DIVIDIR: O QUE JÁ SABEMOS (1 a 5) ===== */
function f01(d, pi){
  reparte(d, pi, "Arraste cada pirulito para uma caixa, <b>até todas ficarem " +
    "iguais</b>. No computador dá para arrastar; no celular, toque no pirulito e " +
    "depois na caixa.", REP);
}
/* 2 e 3 — os problemas. ⭐ O PAR DAS DUAS PERGUNTAS: na 2 se sabe quantos grupos
   e se quer o tamanho de cada um (REPARTIR); na 3 se sabe o tamanho e se quer
   quantos grupos (MEDIR). A conta é a mesma; a pergunta, não. */
function folhaProblema(d, pi, texto, fonte, pref){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1), r = P.a / P.b;
    var lin = el("div", "enunlin");
    if(P.f) lin.appendChild(el("div", "figcx", img(P.f, "fig", "")));
    lin.appendChild(el("div", "perg", P.t));
    lin.appendChild(botaoSom("Ouvir o problema", function(){ falar(pref + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opNumeros("r" + r, 10), "r" + r, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f02(d, pi){
  folhaProblema(d, pi, "Leia (ou ouça) cada problema e escolha <b>quantos ficam " +
    "para cada um</b>. Os números são maiores que no 3º ano: vale fazer a conta " +
    "num papel.", REPT, "pb_");
}
function f03(d, pi){
  folhaProblema(d, pi, "⭐ <b>Agora a pergunta mudou.</b> O problema já diz quanto " +
    "vai em cada grupo e pergunta <b>quantos grupos dão</b>. A conta continua " +
    "sendo de dividir.", MED, "pm_");
}
/* 4 — ⭐⭐ o raciocínio da Bia (A32) e as contas erradas de propósito (B40) */
function f04(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cada criança fez uma divisão e disse o resultado. <b>Está certo " +
    "ou está errado?</b> Confira com a multiplicação antes de responder.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var J = JULG[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", J.t));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("jg_" + k); }));
    box.appendChild(lin);
    var certa = J.ok ? "c" : "e";
    opcoes(box, pi, id, [{v: "c", rot: "Está certo", fala: "op_certo"},
                         {v: "e", rot: "Está errado", fala: "op_errado"}],
           certa, "pal frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
/* 5 — os nomes (B13). O conceito chega DEPOIS de a criança ter repartido,
   medido e julgado — nunca antes. */
var NOMEPARTE = ["DIVIDENDO", "DIVISOR", "QUOCIENTE", "RESTO"];
function f05(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toda divisão tem quatro números com nome. Em <b>35 ÷ 8 = 4 e " +
    "sobram 3</b>: 35 é o <b>dividendo</b> (o que se divide), 8 é o <b>divisor</b>, " +
    "4 é o <b>quociente</b> (o resultado) e 3 é o <b>resto</b>. Agora toque no " +
    "número que tem o nome pedido.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var T = TERM[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var q = Math.floor(T.a / T.b), r = T.a % T.b, partes = [T.a, T.b, q, r];
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", T.a + " ÷ " + T.b + " = " + q + (r ? " e sobram " + r : " e não sobra nada") +
      ". Toque no <b>" + NOMEPARTE[T.p] + "</b>."));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("tm_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, partes.map(function(n, j){
      return {v: "p" + j, rot: String(n), aria: String(n), fala: fNum(n)};
    }), "p" + T.p, "num", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ===== BLOCO B — O MATERIAL DOURADO E A CONTA ARMADA (6 a 15) =====
   ⭐ Pedido do Marcos (26/set/2026): *"Divisão com ajuda do material dourado"*.
   A escada é a do concreto para o símbolo: CONHECER as peças (6) → REPARTIR
   as peças com a mão (7) → a TROCA da barra por dez cubinhos (8) → a MESMA
   conta na chave, com o material ao lado (9) → a chave com troca (10) → com
   resto (11). Só então o divisor de dois algarismos (12 a 14). */
function f06(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ <b>O material dourado.</b> O <b>cubinho</b> vale 1, a <b>barra</b> " +
    "vale 10 (são dez cubinhos) e a <b>placa</b> vale 100 (são dez barras). Conte as " +
    "peças e escreva o número que elas formam.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var N = MDN[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "mdcx", materialHTML(N.n)));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("mdn_" + k); }));
    box.appendChild(lin);
    escreveNum(box, pi, id, k, N.n, '<span class="cf">O número é</span>', "Escreva o número");
    fechaItem(d, box, id);
  });
}
function folhaMesa(d, pi, texto, fonte){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var M = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", "<b>" + M.a + " ÷ " + M.b + "</b>: reparta as peças em <b>" +
      M.b + " grupos iguais</b>."));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("md_" + k); }));
    box.appendChild(lin);
    mesaDourado(box, pi, id, k, M.a, M.b);
    fechaItem(d, box, id);
  });
}
function f07(d, pi){
  folhaMesa(d, pi, "Leve cada peça para um grupo, <b>dando a volta</b>, até os grupos " +
    "ficarem iguais. Comece pelas peças grandes: placas, depois barras, depois cubinhos. " +
    "No computador dá para arrastar; no celular, toque na peça e depois no grupo.", MDS);
}
function f08(d, pi){
  folhaMesa(d, pi, "⭐ <b>Agora sobra uma barra</b> que não dá para pôr inteira em todos " +
    "os grupos. Leve essa barra para a <b>casa da troca</b>: ela vira <b>dez cubinhos</b>, " +
    "e aí dá para repartir.", MDT);
}

function folhaChave(d, pi, texto, fonte, comResto, dicaOrdem, comMat){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", C.a + " &divide; " + C.b +
      (dicaOrdem ? '<span class="sussurro">(centenas ÷ ' + C.b + ', depois dezenas ÷ ' +
                   C.b + ', depois unidades ÷ ' + C.b + ')</span>' : "")));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar(fConta(C.a, C.b)); }));
    box.appendChild(lin);
    if(comMat) box.appendChild(el("div", "mdcx cent", materialHTML(C.a)));
    escreveChave(box, pi, id, k, C.a, C.b, comResto);
    fechaItem(d, box, id);
  });
  d.appendChild(el("div", "ajuda cent", "Toque nas casinhas embaixo do divisor para escrever. " +
    "No computador, é só digitar."));
}
function f09(d, pi){
  folhaChave(d, pi, "⭐ <b>A mesma divisão, agora na chave.</b> O material está ali: divida " +
    "as placas, depois as barras, depois os cubinhos — uma ordem de cada vez — e escreva " +
    "o quociente embaixo do divisor.", ORD, 0, 1, 1);
}
function f10(d, pi){
  folhaChave(d, pi, "<b>Agora com troca, e sem o material:</b> quando a barra não dá para repartir, ela " +
    "vira dez cubinhos e se junta aos outros — igual à casa da troca. Escreva o quociente.", TROC, 0, 0);
}
function f11(d, pi){
  folhaChave(d, pi, "<b>Agora a conta sobra.</b> Escreva o quociente embaixo do divisor " +
    "e, depois, o <b>resto</b> embaixo do dividendo. O resto é sempre menor que o divisor.",
    REST, 1, 0);
}
/* 12 — estimar (A28): o divisor de dois algarismos, arredondado */
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ <b>O divisor agora tem dois algarismos.</b> Antes de fazer a " +
    "conta, estime: arredonde o divisor para a dezena mais perto e pense <b>quantas " +
    "vezes ele cabe</b> no dividendo.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = EST[k], id = "n" + pi + "_" + i, box = item(i + 1), r = C.a / C.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", C.a + " &divide; " + C.b + " = ?" +
      '<span class="sussurro">(quantas vezes o ' + C.b + ' cabe no ' + C.a + '?)</span>'));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar(fConta(C.a, C.b)); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opNumeros("r" + r, 9), "r" + r, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
/* 13 e 14 — ligar ao quociente (A39, A13). O par sobe: o divisor ganha um algarismo. */
function folhaLiga(d, pi, texto, fonte, tagFala){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(grupo, g){
    var box = item(0), pares = grupo.map(function(k){
      var C = fonte[k], q = C.a / C.b;
      return {k: k, esq: C.a + " ÷ " + C.b, dir: String(q),
              ariaE: C.a + " dividido por " + C.b, ariaD: String(q),
              fe: fConta(C.a, C.b), fd: fNum(q),
              fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
    });
    montaLigar(box, pi, "g" + g, pares, d);
    d.appendChild(box);
  });
}
function f13(d, pi){
  folhaLiga(d, pi, "Resolva cada divisão (num papel, se quiser) e <b>ligue a conta ao " +
    "seu quociente</b>: toque na conta e depois no número.", LIG1);
}
function f14(d, pi){
  folhaLiga(d, pi, "<b>Agora o divisor tem dois algarismos.</b> Estime primeiro, " +
    "confira com a multiplicação e ligue cada conta ao seu quociente.", LIG2);
}
/* 15 — exata ou não exata (B40, B31): a gaveta do esqueleto */
function f15(d, pi){
  gavetas(d, pi, "ex", "Faça cada conta e ponha na gaveta certa: <b>exata</b>, quando " +
    "não sobra nada, ou <b>não exata</b>, quando sobra resto. Toque na conta e depois " +
    "na gaveta — ou arraste.");
}

/* ===== BLOCO C — A DIVISÃO E A MULTIPLICAÇÃO, OS RESTOS, MONTAR E ELABORAR (16 a 20) ===== */
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ <b>A conta de volta</b>, do jeito do modelo: <b>5 × 3 = 15, " +
    "então 15 ÷ 3 = 5</b>. Descubra o número que falta — ele é a resposta das " +
    "duas contas.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var I = INV[k], id = "n" + pi + "_" + i, box = item(i + 1), p = I.x * I.y;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", I.y + " × ___ = " + p + ", então " + p + " ÷ " + I.y + " = ___"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("iv_" + k); }));
    box.appendChild(lin);
    escreveNum(box, pi, id, k, I.x,
      '<span class="cf">' + p + '</span><span class="cf">&divide;</span>' +
      '<span class="cf">' + I.y + '</span><span class="cf">=</span>',
      "Escreva o número que falta");
    fechaItem(d, box, id);
  });
}
/* 17 — o caminho do resto (A31), com o degrau do 4º ano: sobrar EXATAMENTE 1 */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "O cachorro Hulk quer chegar à casinha. Em cada passo há três " +
    "casas; ele só pisa na casa em que a divisão <b>sobra exatamente 1</b>.", "p" + pi + "enun");
  var tri = el("div", "trilha");
  tri.appendChild(el("div", "trpont", img("dh4_cachorro.png", "fig", "o cachorro Hulk")));
  ST.folha["p" + pi].forEach(function(k, i){
    var T = TRILHA[k], id = "n" + pi + "_" + i, certa = null;
    T.ops.forEach(function(o, j){ if(o.a % o.b === 1) certa = "t" + j; });
    registra(id, pi, certa);
    var passo = el("div", "passo" + (ST.resp[id] ? " andado" : ""));
    passo.appendChild(el("div", "pnum", "passo " + (i + 1)));
    var cx = el("div", "sils");
    T.ops.forEach(function(o, j){
      var w = el("div", "opw"), um = o.a % o.b === 1;
      var b = el("button", "sil larga" + (ST.resp[id] && um ? " ok" : ""), o.a + " &divide; " + o.b);
      b.setAttribute("aria-label", o.a + " dividido por " + o.b);
      b.setAttribute("data-qa", (um ? "op-" : "no-") + id + "-t" + j);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(um){ b.className = "sil larga ok"; passo.className = "passo andado";
                acertou(id, "certo" + pi + "_" + k); }
        else { b.className = "sil larga nao";
               setTimeout(function(){ b.className = "sil larga"; }, 420);
               errou(id, "dica" + pi + "_" + k); }
      };
      w.appendChild(b);
      w.appendChild(botaoSom("Ouvir esta conta",
        (function(oo){ return function(){ falar(fConta(oo.a, oo.b)); }; })(o), "som somop"));
      cx.appendChild(w);
    });
    passo.appendChild(cx);
    tri.appendChild(passo);
  });
  tri.appendChild(el("div", "trpont", img("dh4_casinha.png", "fig", "a casinha")));
  d.appendChild(tri);
}
/* 18 — ⭐⭐ os restos iguais (declarado: Álgebra do 4º ano) */
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ <b>Uma investigação.</b> Marque <b>todos</b> os números que, " +
    "divididos pelo número pedido, deixam o resto pedido. Depois toque em Conferir — " +
    "e repare na distância entre eles.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MESMO[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", "Divididos por <b>" + M.b + "</b>, quais sobram <b>" + M.r + "</b>?"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("ms_" + k); }));
    box.appendChild(lin);
    var bons = M.nums.filter(function(n){ return n % M.b === M.r; });
    var pecas = M.nums.map(function(n){
      return {k: "n" + n, t: String(n), aria: String(n), ok: n % M.b === M.r,
              fala: function(){ falar(fNum(n)); }};
    });
    var rev = el("div", "ajuda cent");
    rev.appendChild(nomeSecreto("Eles vão de " + M.b + " em " + M.b + ": " + bons.join(", ") +
      ". Somar " + M.b + " não muda o resto!", id));
    marqueConfira(box, id, pi, pecas, "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    box.appendChild(rev);
    fechaItem(d, box, id);
  });
}
/* 19 — ⭐⭐ o quebra-cabeça (A10): a peça vai para o número e a cena aparece */
var QCORDEM = [8, 5, 9, 6, 10, 4, 2, 7, 3];
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Resolva a conta de cada peça e <b>leve a peça até o seu " +
    "resultado</b> no tabuleiro. No fim, a figura aparece inteira.", "p" + pi + "enun");
  var base = el("div", "qcbase");
  base.innerHTML = img("dh4_qctab.png", "qctab", "tabuleiro do quebra-cabeça");
  var casas = {}, listaC = [];
  QCORDEM.forEach(function(r, j){
    var c = el("div", "qccasa");
    c.style.left = (j % 3) * 33.333 + "%"; c.style.top = Math.floor(j / 3) * 33.333 + "%";
    c.setAttribute("data-qa", "alvo-gav" + pi + "_v" + r);
    c._v = "v" + r; casas[r] = c; listaC.push(c); base.appendChild(c);
  });
  d.appendChild(base);
  var banco = el("div", "figbanco qcbanco"), marcada = null;
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PUZ[k], id = "n" + pi + "_" + i, v = "v" + P.r;
    registra(id, pi, ">gav" + pi + "_" + v);
    var b = el("button", "op qcpeca", img("dh4_qc" + P.r + ".png", "qcmini", "") +
               '<span class="qcconta">' + P.a + " ÷ " + P.b + "</span>");
    b.setAttribute("aria-label", P.a + " dividido por " + P.b);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    function poe(){
      casas[P.r].innerHTML = img("dh4_qc" + P.r + ".png", "qcfig", "");
      casas[P.r].className = "qccasa cheia";
      b.className = "op qcpeca usada";
    }
    if(ST.resp[id]) poe();
    function larga(col){
      if(ST.resp[id]) return;
      if(col._v === v){ poe(); if(marcada === b) marcada = null; acertou(id, "certo" + pi + "_" + k); }
      else {
        col.className = "qccasa erro";
        setTimeout(function(){ col.className = "qccasa" + (col.className.indexOf("cheia") > -1 ? " cheia" : ""); }, 500);
        errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar(fConta(P.a, P.b));
      if(marcada === b){ b.className = "op qcpeca"; marcada = null; return; }
      if(marcada) marcada.className = "op qcpeca";
      b.className = "op qcpeca marcada"; marcada = b;
    };
    puxavel(b, listaC, function(col){ larga(col); });
    banco.appendChild(b);
  });
  listaC.forEach(function(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_peca"); return; }
      marcada._larga(col);
    };
  });
  d.appendChild(banco);
}
/* 20 — ⭐ elaborar: qual pergunta esta história responde? (declarado) */
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ <b>Agora o problema é seu.</b> Cada história tem os números, " +
    "mas falta a pergunta. Escolha <b>a pergunta que a divisão responde</b> — é assim " +
    "que se inventa um problema.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var E = ELAB[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", E.t));
    lin.appendChild(botaoSom("Ouvir a história", function(){ falar("el_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opFrases(E.ops, "elop_" + k + "_"), "o0", "pal frase",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ===== BLOCO D — LER AS HORAS (21 a 26) ===== */
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐ No relógio, o ponteiro <b>azul e comprido</b> marca os minutos, e " +
    "cada número vale <b>5 minutos</b>. A flor ajuda: as pétalas marcam os minutos. " +
    "Onde o ponteiro azul parou, quantos minutos são?", "p" + pi + "enun");
  var fl = el("div", "figcx cent");
  fl.innerHTML = img("dh4_flor.png", "figflor", "relógio-flor: as pétalas marcam os minutos");
  d.appendChild(fl);
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MINU[k], id = "n" + pi + "_" + i, box = item(i + 1), mm = M.n * 5;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "relcx", relogioHTML(M.h, mm)));
    lin.appendChild(el("div", "perg", "O ponteiro azul está no <b>" + M.n + "</b>. Quantos minutos?"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("mn_" + k); }));
    box.appendChild(lin);
    var ops = [], de = Math.max(5, mm - 15), n;
    if(de + 30 > 55) de = 25;
    for(n = de; n <= de + 30; n += 5) ops.push({v: "m" + n, rot: String(n), aria: n + " minutos", fala: fNum(n)});
    opcoes(box, pi, id, ops, "m" + mm, "num", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "<b>Agora sem a flor.</b> Leia o relógio: o ponteiro rosa e curto " +
    "marca a hora, o azul marca os minutos. Escreva a hora nas casinhas.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var L = LER[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var alvo = String(L.h) + dois(L.m);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "relcx", relogioHTML(L.h, L.m)));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("quehoras"); }));
    box.appendChild(lin);
    escreveNum(box, pi, id, k, alvo, '<span class="cf">São</span>',
               "Escreva a hora e os minutos", [String(L.h).length]);
    fechaItem(d, box, id);
  });
}
function folhaGira(d, pi, texto, fonte, pref){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var G = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", "Marque <b>" + hhmm(G.h, G.m) + "</b>" +
      (G.h > 12 ? ' <span class="sussurro">(' + G.h + " horas: no relógio de ponteiros é o " + (G.h - 12) + ")</span>" : "")));
    lin.appendChild(botaoSom("Ouvir", function(){ falar(pref + k); }));
    box.appendChild(lin);
    relogioGira(box, pi, id, k, G.h, G.m);
    fechaItem(d, box, id);
  });
}
function f23(d, pi){
  folhaGira(d, pi, "⭐ <b>O seu relógio de ponteiros.</b> Gire o ponteiro azul com o dedo " +
    "(ou use os botões) até marcar a hora pedida. O ponteiro rosa anda junto, como " +
    "num relógio de verdade. Depois toque em Conferir.", GIRA, "gi_");
}
function f24(d, pi){
  folhaGira(d, pi, "<b>Agora a hora da tarde e da noite.</b> O horário vem como no " +
    "relógio digital, de 0 a 23 horas. Tire 12 da hora e marque no relógio de ponteiros.",
    GIRA24, "gj_");
}
function f25(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "<b>Ligue o relógio de ponteiros ao relógio digital</b> que marca o " +
    "mesmo horário: toque no relógio e depois no horário.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(grupo, g){
    var box = item(0), pares = grupo.map(function(k){
      var H = LIG3[k];
      return {k: k, esq: relogioHTML(H.h, H.m, "mini"), dir: '<span class="dig">' + hhmm(H.h, H.m) + "</span>",
              ariaE: "relógio de ponteiros", ariaD: hhmm(H.h, H.m),
              fe: "rl_" + k, fd: fHora(H.h, H.m),
              fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
    });
    montaLigar(box, pi, "g" + g, pares, d);
    d.appendChild(box);
  });
}
function f26(d, pi){
  gavetas(d, pi, "dia", "Cada horário foi lido num relógio digital. <b>Ponha na gaveta " +
    "da parte do dia:</b> manhã (das 6 às 11h59), tarde (das 12 às 17h59), noite (das 18 " +
    "às 23h59) ou madrugada (da meia-noite às 5h59).");
}

/* ===== BLOCO E — HORA, MINUTO, SEGUNDO (27 e 28) ===== */
function f27(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Complete os espaços: <b>quanto tempo cabe em quanto?</b> Escreva o " +
    "número nas casinhas.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var R = REL[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", R.t + " ___ " + R.u + "."));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("rl2_" + k); }));
    box.appendChild(lin);
    escreveNum(box, pi, id, k, R.r, '<span class="cf">' + R.t + "</span>",
               "Escreva o número", null);
    box.lastChild.appendChild(el("span", "cf", R.u));
    fechaItem(d, box, id);
  });
}
function f28(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "⭐⭐ <b>A divisão encontra o relógio.</b> 1 hora tem 60 minutos, então " +
    "para saber quantas horas cabem em muitos minutos é só <b>dividir por 60</b>. E " +
    "quando sobra, o <b>resto são os minutos</b>: 150 ÷ 60 = 2 e sobram 30.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PONT[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    if(P.f) lin.appendChild(el("div", "figcx", img(P.f, "fig", "")));
    lin.appendChild(el("div", "perg", P.t + " Quanto tempo é isso?" +
      '<span class="sussurro">(' + P.min + " ÷ 60)</span>"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("pt_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opFrases(P.ops, "ptop_" + k + "_"), "o0", "pal frase",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ===== BLOCO F — QUANTO TEMPO PASSOU? (29 a 33) ===== */
function mais(h, m, dm){ var t = ((h * 60 + m + dm) % 1440 + 1440) % 1440; return [Math.floor(t / 60), t % 60]; }
function folhaIntervalo(d, pi, texto, fonte, pref, fixo){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var A = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var dm = fixo || A.d, r = mais(A.h, A.m, dm);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", '<span class="dig">' + hhmm(A.h, A.m) + "</span> " +
      (dm > 0 ? (dm === 30 ? "Meia hora depois" : "Daqui a " + dm + " minutos") : "15 minutos antes") +
      " será:"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar(pref + k); }));
    box.appendChild(lin);
    escreveNum(box, pi, id, k, dois(r[0]) + dois(r[1]), "", "Escreva a hora", [2]);
    fechaItem(d, box, id);
  });
}
function f29(d, pi){
  folhaIntervalo(d, pi, "O relógio digital diz a hora de <b>agora</b>. Escreva que horas " +
    "serão <b>daqui a 15 minutos</b>. Cuidado quando os minutos passam de 60: a hora muda!",
    MAIS, "ma_", 15);
}
function f30(d, pi){
  folhaIntervalo(d, pi, "<b>Agora para trás e para a frente:</b> 15 minutos antes, ou meia " +
    "hora depois. Leia bem o que cada linha pede.", ANDE, "ad_", 0);
}
function folhaFrase(d, pi, texto, fonte, pref){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    if(P.f) lin.appendChild(el("div", "figcx", img(P.f, "fig", "")));
    lin.appendChild(el("div", "perg", P.t));
    lin.appendChild(botaoSom("Ouvir", function(){ falar(pref + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opFrases(P.ops, pref + "op_" + k + "_"), "o0", "pal frase",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f31(d, pi){
  folhaFrase(d, pi, "A agenda diz quando cada coisa <b>começa</b> e quando <b>termina</b>. " +
    "Quanto tempo durou? Conte do começo até o fim — primeiro até a hora cheia, depois " +
    "o resto.", DUR, "du_");
}
function f32(d, pi){
  folhaFrase(d, pi, "<b>Agora a pergunta é outra:</b> dá tempo? A que horas termina? " +
    "Some a duração ao horário de começo e depois compare.", TEMPO, "te_");
}
/* 33 — a rotina em ordem (D06, D02, D21): tocar na ordem do relógio */
function f33(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Os horários do dia estão misturados. <b>Toque em cada um na ordem " +
    "em que acontecem</b>, do mais cedo ao mais tarde.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var R = ROT[k], id = "n" + pi + "_" + i, box = item(i + 1), pos = 0, feito = !!ST.resp[id];
    registra(id, pi, R.ord.map(function(e){ return e.k; }).join(" "));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", "<b>" + R.t + "</b>"));
    lin.appendChild(botaoSom("Ouvir", function(){ falar("ro_" + k); }));
    box.appendChild(lin);
    var linha = el("div", "rotlinha"), cx = el("div", "rotchips");
    function chip(E){
      return (E.f ? img(E.f, "rotfig", "") : "") + '<span class="rotn">' + E.n + '</span><b class="dig">' +
             hhmm(E.h, E.m) + "</b>";
    }
    if(feito) R.ord.forEach(function(E){ linha.appendChild(el("div", "rotchip ok", chip(E))); });
    else baralha(R.ord).forEach(function(E){
      var w = el("div", "opw");
      var b = el("button", "rotchip", chip(E));
      b.setAttribute("aria-label", E.n + ", " + hhmm(E.h, E.m));
      b.setAttribute("data-qa", "op-" + id + "-" + E.k);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falar("roe_" + E.k);
        if(E.k === R.ord[pos].k){
          pos++; w.parentNode.removeChild(w);
          linha.appendChild(el("div", "rotchip ok", chip(E)));
          if(pos === R.ord.length) acertou(id, "certo" + pi + "_" + k);
        } else {
          b.className = "rotchip nao";
          setTimeout(function(){ b.className = "rotchip"; }, 420);
          errou(id, "dica" + pi + "_" + k);
        }
      };
      w.appendChild(b);
      w.appendChild(botaoSom("Ouvir", function(){ falar("roe_" + E.k); }, "som somop"));
      cx.appendChild(w);
    });
    box.appendChild(linha); box.appendChild(cx);
    fechaItem(d, box, id);
  });
}

/* ===== FECHO (34 e 35) ===== */
/* 34 — a memória (do `_div3`): o relógio de ponteiros e o horário digital */
function f34(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Vire duas cartas e ache <b>o relógio de ponteiros e o horário " +
    "digital</b> que marcam a mesma hora.", "p" + pi + "enun");
  var L = ST.folha["p" + pi];
  for(var g = 0; g < L.length; g++){
    (function(grupo, g2){
      var id = "n" + pi + "_" + g2, box = item(g2 + 1);
      var abertas = [], travado = false, faltam = grupo.length, k;
      registra(id, pi, grupo.join(" "));
      var lista = [];
      for(k = 0; k < grupo.length; k++) lista.push({k: grupo[k], lado: "rel"});
      for(k = grupo.length - 1; k >= 0; k--) lista.push({k: grupo[k], lado: "dig"});
      lista = baralha(lista);
      var grade = el("div", "mcartas");
      lista.forEach(function(c){
        var M = MEM[c.k], feito = !!ST.resp[id];
        var dentro = c.lado === "rel" ? relogioHTML(M.h, M.m, "mini")
                                      : '<span class="mrot dig">' + hhmm(M.h, M.m) + "</span>";
        var ct = el("div", "mcarta" + (feito ? " achada" : ""));
        ct.setAttribute("data-qa", "mem-" + id + "-" + c.k + "-" + c.lado);
        ct.setAttribute("aria-label", feito ? hhmm(M.h, M.m) : "carta virada para baixo");
        ct.innerHTML = '<div class="mgira"><div class="mface mverso"><i class="mbrilho"></i>' +
          '<span class="minterro">?</span></div><div class="mface mfrente">' + dentro + "</div></div>";
        ct.onclick = function(){
          if(travado || ST.resp[id] || ct.className.indexOf("achada") > -1 ||
             ct.className.indexOf("aberta") > -1) return;
          sTecla(); ct.className = "mcarta aberta";
          falar(fHora(M.h, M.m));
          abertas.push({el: ct, c: c});
          if(abertas.length < 2) return;
          travado = true;
          var a = abertas[0], b = abertas[1];
          setTimeout(function(){
            if(a.c.k === b.c.k && a.el !== b.el){
              a.el.className = "mcarta achada"; b.el.className = "mcarta achada";
              sCerto(); falar("memok");
              faltam--;
              if(!faltam) setTimeout(function(){ acertou(id, "memfim"); }, 700);
            } else {
              sErro(); a.el.className = "mcarta"; b.el.className = "mcarta";
              errou(id, "memdica");
            }
            abertas = []; travado = false;
          }, 1100);
        };
        grade.appendChild(ct);
      });
      box.appendChild(grade);
      fechaItem(d, box, id);
    })(L[g], g);
  }
}
/* 35 — o cartaz que a criança leva. Alcançável a qualquer momento. */
function f35(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Este cartaz é seu. Em cada linha, escolha <b>o exemplo</b> que cabe " +
    "naquele nome — e leve os seis na cabeça.", "p" + pi + "enun");
  var cx = el("div", "cartaz");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CARTAZ[k], id = "n" + pi + "_" + i;
    var lin = el("div", "cartlin");
    var tit = el("div", "cartit", "<b>" + C.n + "</b><span>" + C.d + "</span>");
    tit.appendChild(botaoSom("Ouvir", (function(kk){
      return function(){ falar("cartaz_" + kk); }; })(k)));
    lin.appendChild(tit);
    var box = el("div", "cartalvo");
    var ops = ["G1", "G2", "G3", "G4", "G5", "G6"].map(function(ck){
      return {v: ck, rot: CARTAZ[ck].ex, aria: CARTAZ[ck].ex, fala: "ex_" + ck};
    });
    opcoes(box, pi, id, ops, k, "pal frase", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    lin.appendChild(box);
    cx.appendChild(lin);
  });
  d.appendChild(cx);
  d.appendChild(el("div", "ajuda cent",
    "Pronto: agora você reparte, mede, arma a conta na chave, sabe o que sobra e lê o " +
    "relógio. E fica a pergunta: <b>quantas horas tem a semana inteira?</b> (Dica: 7 × 24.)"));
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
  /* neste caderno quase toda casinha é de NÚMERO: no celular abre o teclado de números */
  c.setAttribute("inputmode", /^[0-9]+$/.test(E.w) ? "numeric" : "text");
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
  if(fechaSozinho(E, CRUZ.val)) setTimeout(confereCruz, 380);
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
/* ⭐ SEM PRECISAR DO ENTER (ordem do Marcos, 21/set/2026, sobre o caderno dos
   sistemas do 5º ano): ***"tem uma atividade onde o estudante digita e tem que
   clicar enter para confirmar, melhor não precisar do enter"*** — e logo
   depois: ***"corrija isso em qualquer atividade que tenha isso"***.

   ⚠️ O QUE ERA: a grade de tamanho FIXO já fechava sozinha ao encher a última
      casa. A grade LIVRE (a das folhas de produção — *"escreva a SUA palavra"*,
      *"a sua manchete"*, *"o seu título"*) não tinha como saber quando a criança
      terminou, e o único jeito de confirmar era o ENTER. No celular a tecla se
      chama outra coisa em cada aparelho, e no PC a criança de 10 anos não
      adivinha que precisa dela: ela escrevia a resposta certa e a folha ficava
      parada.

   ⚠️ POR QUE NÃO FECHAR SOZINHO NUMA PAUSA: pausa de dois segundos é a criança
      PENSANDO no meio da palavra, e fechar ali contaria erro no que ela nem
      terminou de escrever. Tempo não é sinal de que acabou.

   O que entra no lugar, e são duas coisas:
     1. fecha sozinho assim que o escrito BATE com uma resposta aceita — sem
        esperar tecla nenhuma;
     2. quando ela escreve uma palavra que não está na lista (a folha de
        produção aceita isso), o botão **PRONTO**, ao lado da grade, confirma.
   O Enter continua valendo: é a terceira porta, nunca mais a única. */
function fechaSozinho(E, val){
  if(!val) return false;
  if(!E.aceita) return val.length >= E.w.length;
  var bate = E.aceita.some(function(w){ return mesmaPalavra(val, w, E.exigeAcento); });
  if(!bate) return false;
  /* ⚠️ e ninguém CONTINUA a partir dela: se a lista tem PÃO e PÃOZINHO, fechar
     no PÃO trancaria justamente a criança que ia escrever a palavra maior. */
  var maior = E.aceita.some(function(w){
    return w.length > val.length && semAcento(w).indexOf(semAcento(val)) === 0;
  });
  return !maior;
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
    /* ⚠️ O NÚMERO DA FOLHA ENTRA NO `data-qa`, e isto foi conserto de
       20/set/2026. As 36 folhas moram no MESMO html, e o jogador da banca
       acha a ponta com `document.querySelector`. Duas folhas de LIGAR com a
       mesma etiqueta publicavam o mesmo `data-qa`: o clique ia sempre para a
       PRIMEIRA, e a segunda folha não fechava nem com a resposta certa.
       Foi o que aconteceu no `_corpo5`, folhas 5 e 6. */
    /* ⚠️ A PONTA DO LIGAR É ALVO, e por isso ela se declara. O portão 1i4
       (`resposta_impressa.py`) procura a resposta escrita na tela antes de a
       criança responder — e no LIGAR as duas colunas estão à vista de propósito:
       é o gesto. Sem esta declaração ele reprova quando a chave do par é igual
       à palavra mostrada (aconteceu na folha 20, com o par `sangue` ↔ "leva
       oxigênio": a chave é "sangue" e o rótulo diz SANGUE). Não é desligar o
       portão: é dizer o que aquele elemento é. */
    e.setAttribute("data-qa", "lig" + pi + tag + "-e-" + P.k);
    e.setAttribute("data-alvo", "1");
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
    e.setAttribute("data-qa", "lig" + pi + tag + "-d-" + P.k);
    e.setAttribute("data-alvo", "1");
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
    if(fechaSozinho(CRUZ.E, CRUZ.val)) setTimeout(confereCruz, 380);
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
  if(!CRUZ && k.length === 1 && "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ0123456789".indexOf(k) > -1){
    var alvo = null, todos = document.querySelectorAll('.pagina.viva [data-qa^="esc-"]');
    for(var i = 0; i < todos.length && !alvo; i++){
      var idq = todos[i].getAttribute("data-qa").slice(4);
      if(!ST.resp[idq]) alvo = todos[i];
    }
    if(alvo){ alvo.click(); }
  }
  if(!CRUZ) return;
  if(k.length === 1 && "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ0123456789".indexOf(k) > -1){ ev.preventDefault(); digitaCruz(k); }
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
    est += '<img src="img/dh4_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você começou a repartir em partes iguais e a ler o relógio — e isso é o principal!";
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
   do currículo da rede. O portão `_qa/pedagogo_curriculo.py` reprova se os
   nomes e as folhas não baterem um a um, e também se alguma folha de trabalho
   ficar sem objetivo que a meça. Os números são POSIÇÕES de folha.
   Ex.: {n: "Distinguir X de Y", f: [1, 2, 3],
         ok:  "faz o que o objetivo pede, em palavras do professor",
         nao: "o que ainda não faz — sem a palavra 'errou'"}  */
var OBJETIVOS = [
  {n: "Repartir e medir: as duas perguntas da divisão", f: [1, 2, 3, 20],
   ok: "reparte em partes iguais e descobre quantos grupos cabem",
   nao: "ainda não separa «quantos para cada um» de «quantos grupos dão»"},
  {n: "Dividir com o material dourado, trocando a barra", f: [6, 7, 8],
   ok: "reparte placas, barras e cubinhos e troca a barra por dez cubinhos",
   nao: "ainda não troca a barra quando ela não dá para todos os grupos"},
  {n: "Armar a divisão na chave, com e sem resto", f: [5, 9, 10, 11, 15],
   ok: "arma a conta na chave, ordem por ordem, e sabe o que é o resto",
   nao: "ainda se perde na ordem das casas da chave ou no resto"},
  {n: "Estimar e dividir por um número de dois algarismos", f: [12, 13, 14, 19],
   ok: "estima quantas vezes o divisor cabe, também com dois algarismos",
   nao: "ainda não estima com o divisor de dois algarismos"},
  {n: "Conferir a divisão com a multiplicação", f: [4, 16],
   ok: "confere a divisão com a multiplicação",
   nao: "ainda não usa a multiplicação para conferir"},
  {n: "Achar os números que deixam o mesmo resto", f: [17, 18],
   ok: "descobre os números que deixam o mesmo resto",
   nao: "ainda não vê a regularidade dos restos iguais"},
  {n: "Ler as horas no relógio de ponteiros e no digital", f: [21, 22, 23, 24, 25, 26, 34],
   ok: "lê e marca as horas nos dois relógios",
   nao: "ainda troca o ponteiro das horas com o dos minutos"},
  {n: "Relacionar horas, minutos e segundos", f: [27, 28],
   ok: "transforma minutos em horas dividindo por 60",
   nao: "ainda não relaciona hora, minuto e segundo"},
  {n: "Calcular o início, o término e a duração", f: [29, 30, 31, 32, 33],
   ok: "calcula quando termina e quanto tempo durou",
   nao: "ainda erra quando os minutos passam de 60"},
  {n: "Levar o cartaz: a divisão e as horas", f: [35],
   ok: "junta no cartaz os sentidos da divisão e as contas das horas",
   nao: "ainda não liga cada nome do cartaz ao seu exemplo"}
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
    parecer += "está começando a repartir em partes iguais e a ler o relógio. Nenhum " +
      "objetivo chegou a 75% de acerto de primeira — vale retomar com o MATERIAL DOURADO na " +
      "mesa (repartir 48 em 4 grupos, trocar a barra quando ela não dá) antes de voltar à " +
      "chave, e com um relógio de ponteiros na mão para as horas. O gesto com a peça vem " +
      "antes do registro no papel.";
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
    "<p class='comonota'><b>O que este caderno NÃO mede:</b> na conta armada na chave, " +
    "a criança escreve o <b>quociente</b> e o <b>resto</b> &mdash; as subtrações que se " +
    "escrevem embaixo do dividendo ficam no papel, e quem corrige é o professor. E o " +
    "relógio de ponteiros da tela anda de <b>5 em 5 minutos</b> (o mostrador colhido não " +
    "tem os risquinhos dos minutos): a leitura minuto a minuto continua no relógio da sala.</p>";
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
