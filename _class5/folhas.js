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

/* ⚠️⚠️ LICAO PAGA AO MONTAR ESTE CADERNO: os desenhos estavam no FIM do
   arquivo, como `var DES = {...}`, e o caderno abria com ZERO folhas.
   `function` e icada; `var` NAO — o motor chama `monta()` la em cima, a capa
   pede o desenho, e naquele instante `DES` ainda e `undefined`. Estourava
   "Cannot read properties of undefined" e a pagina ficava VAZIA, sem nada na
   tela que dissesse o porque — o pior tipo de defeito. Peca que a CAPA usa se
   declara ANTES do motor. */
/* ---------- as quatro figuras do caderno ---------- */
var DES = {
  casa: '<path d="M8 30 L24 14 L40 30" fill="none" stroke="#7a3b16" stroke-width="3.5" stroke-linejoin="round"/>' +
        '<rect x="13" y="29" width="22" height="15" rx="1.5" fill="#f3d9b1" stroke="#7a3b16" stroke-width="3"/>' +
        '<rect x="21" y="35" width="7" height="9" fill="#7a3b16"/>',
  gato: '<circle cx="24" cy="30" r="12" fill="#c9c2bb" stroke="#4a4340" stroke-width="3"/>' +
        '<path d="M14 21 L12 11 L21 16 Z M34 21 L36 11 L27 16 Z" fill="#c9c2bb" stroke="#4a4340" stroke-width="3" stroke-linejoin="round"/>' +
        '<circle cx="20" cy="29" r="1.8" fill="#4a4340"/><circle cx="28" cy="29" r="1.8" fill="#4a4340"/>' +
        '<path d="M24 33 l-3 3 M24 33 l3 3" stroke="#4a4340" stroke-width="2.4" fill="none" stroke-linecap="round"/>',
  flor: '<path d="M24 30 V44" stroke="#3f7d3a" stroke-width="3" stroke-linecap="round"/>' +
        '<path d="M24 38 q7 -1 9 -6 q-7 -1 -9 6Z" fill="#3f7d3a"/>' +
        '<circle cx="24" cy="15" r="5.5" fill="#f0b429"/>' +
        '<circle cx="15" cy="22" r="5.5" fill="#e0607e"/><circle cx="33" cy="22" r="5.5" fill="#e0607e"/>' +
        '<circle cx="19" cy="31" r="5.5" fill="#e0607e"/><circle cx="29" cy="31" r="5.5" fill="#e0607e"/>' +
        '<circle cx="24" cy="24" r="5" fill="#f0b429" stroke="#8a5a00" stroke-width="2"/>',
  livro:'<path d="M7 13 h15 a3 3 0 0 1 2 3 v24 a3 3 0 0 0 -2 -3 H7Z" fill="#5c8fd6" stroke="#22406e" stroke-width="2.6" stroke-linejoin="round"/>' +
        '<path d="M41 13 h-15 a3 3 0 0 0 -2 3 v24 a3 3 0 0 1 2 -3 h15Z" fill="#8fb6ec" stroke="#22406e" stroke-width="2.6" stroke-linejoin="round"/>' +
        '<path d="M24 16 V40" stroke="#22406e" stroke-width="2.6"/>'
};
/* ⚠️ O ROTULO MORA COM O DESENHO, e isto e conserto de um defeito real: o
   `fig()` lia o nome em `D.FIG`, e na CAPA ele roda antes de esse bloco estar
   pronto — a pagina estourava com "Cannot read properties of undefined" e o
   caderno abria com ZERO folhas. Peca de desenho nao deve depender do bloco de
   dados das folhas: sao coisas de tempos diferentes. */
var DESNOME = {casa: "CASA", gato: "GATO", flor: "FLOR", livro: "LIVRO"};
function fig(k, cls){
  /* ⚠️ A FIGURA VEM DO NOSSO BANCO (regra do Marcos: consultar o banco antes de
     qualquer arte nova). O `img()` traz junto o `naoAmplia`, que trava a figura
     no tamanho do arquivo — foi o que resolveu o borrado dos Cinco Reinos. */
  return img("cl5_" + k + ".png", cls || "figdes", DESNOME[k] || k);
}


var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI, e o número errado quebra DUAS
   folhas de uma vez — medido no `_rima1`, que estava no ar: a folha que liga
   NUNCA fechava (a criança ligava tudo e continuava faltando) e a folha
   apontada por engano FECHAVA SOZINHA, sem ninguém tocar nela. São as únicas
   cujos ids não nascem de `n<pi>_`, e sim dentro do `montaLigar`
   (`l<pi>g<i>_<chave>`). Conferir com `node _qa/conta_folha.js <pasta>`. */
var LIGAR = [12];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
var CORES = ["c1", "c1", "c1", "c1", "c1", "c1", "c1", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c3", "c3", "c3", "c3", "c3", "c3", "c3", "c4", "c4", "c4", "c4", "c4", "c4", "c4", "c5", "c5", "c5", "c5", "c5", "c5", "c5"];


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
  var caps = [f0,
    f01, f02, f03, f04, f05, f06, f07,        /*  1-7   o substantivo   */
    f08, f09, f10, f11, f12, f13, f14,        /*  8-14  o adjetivo      */
    f15, f16, f17, f18, f19, f20, f21,        /* 15-21  o verbo         */
    f22, f23, f24, f25, f26, f27, f28,        /* 22-28  grande e pequeno*/
    f29, f30, f31, f32, f33, f34,             /* 29-34  um e muitos     */
    f35], i;                                  /* 35     o cartaz        */
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
  /* CAPA DE ESQUELETO — por desenhar. `python3 _padrao/identidade_capa.py <pasta>` a
     substitui pela capa com identidade própria (cor, cena, animação do assunto). */
  var c = el("div", "capa"), nome = "Aprendendo substantivos, adjetivos, verbos e a flexão das palavras", k, letras = "";
  nome.split(" ").forEach(function(pal, w){
    var s = "";
    for(k = 0; k < pal.length; k++) s += '<span class="lt">' + pal.charAt(k) + '</span>';
    letras += (w ? '<span class="esp"></span>' : '') + '<span class="tpal">' + s + '</span>';
  });
  c.innerHTML =
    '<div class="ceu"></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Componente &middot; Nº ano &middot; N folhas sobre ASSUNTO</div>' +
    '<div class="cena">capa por desenhar: _padrao/identidade_capa.py</div>' +
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
    est += '<img src="img/cl5_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  {n: "Reconhecer e classificar o substantivo", f: [1, 2, 3, 4, 5, 6, 7],
   ok: "separa gente, coisa e lugar, vê a letra maiúscula do nome próprio e monta palavra derivada e composta",
   nao: "ainda não separa o nome próprio do comum nem vê de onde a palavra nasceu"},
  {n: "Usar o adjetivo e descobrir a classe pelo uso", f: [8, 9, 10, 11, 12, 13, 14],
   ok: "dá característica ao substantivo, troca a locução pelo adjetivo e percebe que a MESMA palavra muda de classe conforme a frase",
   nao: "ainda decide a classe pela palavra sozinha, sem olhar a frase em que ela está"},
  {n: "Reconhecer o verbo e mudar o tempo", f: [15, 16, 17, 18, 19, 20, 21],
   ok: "acha o verbo na frase, separa ação de estado e de fenômeno da natureza e passa a frase para ontem e para amanhã",
   nao: "ainda troca o tempo do verbo sem olhar quando a ação acontece"},
  {n: "Formar o aumentativo e o diminutivo", f: [22, 23, 24, 25, 26, 27, 28],
   ok: "forma o grau pelas terminações e não cai na armadilha das palavras que terminam em -inho sem ser diminutivo",
   nao: "ainda marca como diminutivo toda palavra terminada em -inho"},
  {n: "Flexionar em número e fazer a concordância", f: [29, 30, 31, 32, 33, 34],
   ok: "forma o plural pelas terminações -ão e -l e faz a frase INTEIRA concordar, com artigo e adjetivo",
   nao: "ainda põe o s só no substantivo e deixa o resto da frase no singular"},
  {n: "Amarrar as classes de palavras num quadro", f: [35],
   ok: "desmonta uma frase em substantivo, adjetivo e verbo",
   nao: "ainda não separa as classes dentro de uma frase inteira"}
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
   AS 35 FOLHAS DO `_class5`

   O roteiro e o crivo estão em `_sequencias/POTE-CLASS5.md`: cada folha nasce
   de um VERBO que apareceu impresso numa das 123 folhas de papel colhidas.
   Cinco blocos colados, cada um subindo um degrau, e o conceito sempre DEPOIS
   do problema.

   ⚠️ AS FIGURAS SÃO DESENHO PRÓPRIO, em vetor, dentro do arquivo. Não há PNG
      para carregar (nenhum 404 possível), não borra em tela nenhuma e não
      depende de recorte. Foram feitas para este caderno.
   ============================================================ */

/* ---------- escrever a resposta (as DUAS portas) ----------
   ⚠️ Teclado de verdade e teclado do aparelho, regra da casa desde ago/2026: no
      PC da escola a criança digita; no celular não há teclado físico, e sem um
      campo de VERDADE para focar o aparelho não abre teclado nenhum. Este é um
      <input> comum — o navegador cuida das duas portas sozinho. */
function escreve(box, pi, id, gabarito, falaCerto, falaDica, dica){
  registra(id, pi, gabarito);
  var cx = el("div", "escrevelin");
  var inp = document.createElement("input");
  inp.type = "text"; inp.className = "escreve";
  inp.setAttribute("autocomplete", "off"); inp.setAttribute("autocorrect", "off");
  inp.setAttribute("autocapitalize", "characters"); inp.setAttribute("spellcheck", "false");
  inp.setAttribute("aria-label", dica || "Escreva a palavra");
  inp.setAttribute("data-qa", "esc-" + id);
  inp.setAttribute("data-resp", gabarito);
  if(ST.resp[id]){ inp.value = gabarito; inp.disabled = true; inp.className = "escreve ok"; }
  var bt = el("button", "bt mini conf", "Conferir");
  bt.setAttribute("data-qa", "conf-" + id);
  function confere(){
    if(ST.resp[id]) return;
    var v = (inp.value || "").toUpperCase().replace(/\s+/g, "");
    if(!v) return;
    if(v === gabarito.toUpperCase()){
      inp.value = gabarito; inp.disabled = true; inp.className = "escreve ok";
      acertou(id, falaCerto);
    } else {
      inp.className = "escreve erro";
      setTimeout(function(){ inp.className = "escreve"; }, 600);
      errou(id, falaDica);
    }
  }
  /* ⚠️ FOCO EXPLICITO NO CLIQUE. Um toque de dedo foca o campo sozinho; um
     clique PROGRAMATICO (o do jogador da banca, e o de qualquer leitor de tela
     que dispare click) NAO foca — e aí a letra digitada nao vai para lugar
     nenhum e a folha nunca fecha. Foi assim que as folhas de escrever passaram
     no navegador e REPROVARAM na banca: o defeito estava na porta, nao no
     campo. */
  inp.onclick = function(){ try{ inp.focus(); }catch(e){} };
  /* ⚠️⚠️ AS DUAS PORTAS, e esta faltava. Palavras como CASARÃO e NARIGÃO têm Ã —
     e o Ã não é uma TECLA: no teclado brasileiro ele sai de til + A, e o
     navegador de teste responde "Unknown key". Resultado: as folhas de escrever
     com til REPROVAVAM na banca e, na sala, qualquer criança num teclado que
     não ajude ficaria trancada do mesmo jeito. Então as letras que o teclado não
     alcança ganham botão — é a mesma solução que o motor já usa (`.letrabt`), e
     é regra da casa desde ago/2026: nunca uma porta só. */
  var dificeis = [];
  gabarito.toUpperCase().split("").forEach(function(ch){
    if(!/[A-Z0-9\- ]/.test(ch) && dificeis.indexOf(ch) < 0) dificeis.push(ch);
  });
  if(dificeis.length){
    var fila = el("div", "letras");
    dificeis.forEach(function(ch){
      var lb = el("button", "letrabt", ch);
      lb.setAttribute("data-qa", "letra-" + id + "-" + ch);
      lb.setAttribute("aria-label", "Letra " + ch);
      lb.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); inp.value = (inp.value || "") + ch;
        try{ inp.focus(); }catch(e){}
        if(inp.dispatchEvent) inp.dispatchEvent(new Event("input", {bubbles: true}));
      };
      fila.appendChild(lb);
    });
    box._filaLetras = fila;      /* anexada logo depois do campo, abaixo */
  }
  bt.onclick = confere;
  inp.onkeydown = function(ev){ if(ev.key === "Enter"){ ev.preventDefault(); confere(); } };
  /* ⚠️ CONFERIR SOZINHO quando a palavra fica do tamanho certo — e isto e
     conserto de defeito que o jogador da banca pegou: ele DIGITA e nao aperta
     botao nenhum, entao as folhas de escrever nunca fechavam para ele. E nao e
     so a regua: a criança tambem escreve e fica olhando, esperando. O botao
     Conferir continua ali para quem quiser, e o Enter tambem. */
  inp.addEventListener("input", function(){
    if(ST.resp[id]) return;
    var v = (inp.value || "").toUpperCase().replace(/\s+/g, "");
    if(v.length >= gabarito.replace(/\s+/g, "").length) setTimeout(confere, 320);
  });
  cx.appendChild(inp); cx.appendChild(bt);
  box.appendChild(cx);
  if(box._filaLetras){ box.appendChild(box._filaLetras); box._filaLetras = null; }
}

/* ---------- marcar palavras dentro da frase ---------- */
function marcaFrase(d, pi, pede, bloco, cls2){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var B = D[bloco], id = "n" + pi + "_0", box = item(0);
  registra(id, pi, B.marcar.join(" "));
  var linha = el("div", "frasemarca"), postas = {};
  B.frase.forEach(function(pal, i){
    var alvo = B.marcar.indexOf(i) > -1;
    var b = el("button", "pmarca", pal);
    b.setAttribute("data-qa", "op-" + id + "-" + i);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      if(!alvo){
        b.className = "pmarca nao";
        setTimeout(function(){ b.className = "pmarca"; }, 500);
        errou(id, "dica" + pi + "_0"); return;
      }
      if(postas[i]) return;
      postas[i] = 1; b.className = "pmarca " + (cls2 || "marcada");
      if(Object.keys(postas).length === B.marcar.length) acertou(id, "certo" + pi + "_0");
    };
    linha.appendChild(b);
  });
  box.appendChild(linha);
  fechaItem(d, box, id);
}

/* ---------- montar a palavra com as sílabas soltas ---------- */
function montaSilabas(d, pi, pede, bloco){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var B = D[bloco];
  ST.folha["p" + pi].forEach(function(k, i){
    var dado = B[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var de = dado[0], alvo = dado[1], sil = dado[2];
    /* ⚠️ A RESPOSTA DECLARADA E A ORDEM DAS SILABAS, nao a palavra inteira: e
       assim que o motor le folha de montar (pedaços separados por espaço), e foi
       so por isso que o jogador da banca saiu com "nao conheco a peca" — que NAO
       e "passou". A palavra inteira nao existe como botao; as silabas existem. */
    registra(id, pi, sil.join(" "));
    box.appendChild(el("div", "dizde", "de <b>" + de + "</b> vem…"));
    var linha = el("div", "montapal"), banco = el("div", "silbanco"), posto = [];
    function pinta(){ linha.textContent = posto.join("") || "…"; }
    pinta();
    baralha(sil.slice(0)).forEach(function(s, j){
      var b = el("button", "op sil", s);
      b.setAttribute("data-qa", "op-" + id + "-" + s);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); posto.push(s); b.className = "op sil usada"; b.disabled = true; pinta();
        if(posto.length === sil.length){
          if(posto.join("") === alvo){ acertou(id, "certo" + pi + "_" + k); }
          else {
            errou(id, "dica" + pi + "_" + k);
            posto = []; pinta();
            linha.parentNode.querySelectorAll(".op.sil").forEach(function(x){
              x.className = "op sil"; x.disabled = false; });
          }
        }
      };
      banco.appendChild(b);
    });
    box.appendChild(linha); box.appendChild(banco);
    fechaItem(d, box, id);
  });
}

/* ---------- escolher entre duas ou três (o molde mais usado) ----------
   `linhas(dado)` devolve {rot, ops:[{v,rot,fala}], certa} para cada item. */
function escolhe(d, pi, pede, bloco, linhas){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var B = D[bloco];
  ST.folha["p" + pi].forEach(function(k, i){
    var L = linhas(B[k], k), id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(el("div", "pergunta", L.rot));
    /* ⚠️ A RESPOSTA CERTA NAO PODE FICAR SEMPRE NO MESMO LUGAR. Escrevendo as
       folhas eu deixei a certa em primeiro em TODAS — e aí a criança aprende a
       posição, não o conteúdo, e o jogador da banca passa sem medir nada.
       O acaso é SEMEADO pela folha e pelo item: a mesma criança que volta
       encontra a mesma ordem (senão "continuar de onde parou" embaralharia o
       que ela já tinha visto), e folhas diferentes não ficam iguais. */
    opcoes(box, pi, id, baralha(L.ops.slice(0)), L.certa, L.cls || "curta",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ---------- escrever a palavra (folha inteira) ---------- */
function folhaEscreve(d, pi, pede, bloco, rot, gab, ajuda){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var B = D[bloco];
  ST.folha["p" + pi].forEach(function(k, i){
    var dado = B[k], id = "n" + pi + "_" + i, box = item(i + 1);
    box.appendChild(el("div", "pergunta", rot(dado, k)));
    escreve(box, pi, id, gab(dado, k), "certo" + pi + "_" + k, "dica" + pi + "_" + k,
            ajuda ? ajuda(dado, k) : "Escreva a palavra");
    fechaItem(d, box, id);
  });
}

/* ---------- marcar num banco de palavras (achar os que são) ---------- */
function achaNoBanco(d, pi, pede, certos, distratores){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var id = "n" + pi + "_0", box = item(0);
  registra(id, pi, certos.join(" "));
  var banco = el("div", "figbanco"), postas = {};
  baralha(certos.concat(distratores)).forEach(function(w, j){
    var b = el("button", "op pal", w);
    /* ⚠️ O CONTRATO DO `data-qa` E DO MOTOR, nao meu: folha de marcar varios
       publica `op-<id>-<pedaco>`, e o pedaco tem de ser o MESMO texto que o
       `registra` guardou. Eu tinha inventado `ach-<id>-<n>` e o jogador da banca
       saiu com "nao conheco a peca" — que nao e "passou". */
    b.setAttribute("data-qa", "op-" + id + "-" + w);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      if(certos.indexOf(w) < 0){
        b.className = "op pal nao";
        setTimeout(function(){ b.className = "op pal"; }, 520);
        errou(id, "dica" + pi + "_0"); return;
      }
      if(postas[w]) return;
      postas[w] = 1; b.className = "op pal usada";
      if(Object.keys(postas).length === certos.length) acertou(id, "certo" + pi + "_0");
    };
    banco.appendChild(b);
  });
  box.appendChild(banco);
  fechaItem(d, box, id);
}

/* ---------- duas cores na mesma frase ---------- */
function duasCores(d, pi, pede, bloco){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var B = D[bloco], id = "n" + pi + "_0", box = item(0);
  registra(id, pi, B.subst.concat(B.adj).join(" "));
  var aviso = el("div", "dizde", "Toque nos <b>substantivos</b> e nos <b>adjetivos</b>.");
  var linha = el("div", "frasemarca"), postas = {}, alvo = B.subst.length + B.adj.length;
  B.frase.forEach(function(pal, i){
    var eS = B.subst.indexOf(i) > -1, eA = B.adj.indexOf(i) > -1;
    var b = el("button", "pmarca", pal);
    b.setAttribute("data-qa", "op-" + id + "-" + i);
    b.onclick = function(){
      if(ST.resp[id] || postas[i]) return;
      sPasso();
      if(!eS && !eA){
        b.className = "pmarca nao";
        setTimeout(function(){ b.className = "pmarca"; }, 500);
        errou(id, "dica" + pi + "_0"); return;
      }
      postas[i] = 1; b.className = "pmarca " + (eS ? "marcada" : "marcada2");
      if(Object.keys(postas).length === alvo) acertou(id, "certo" + pi + "_0");
    };
    linha.appendChild(b);
  });
  box.appendChild(aviso); box.appendChild(linha);
  fechaItem(d, box, id);
}

/* ============================================================
   A CAPA — cena própria deste caderno, desenhada aqui.
   O problema do caderno está na cena: as MESMAS coisas do mundo, e embaixo
   delas as palavras que as nomeiam, as que dizem como elas são e as que dizem
   o que elas fazem. É disso que o caderno trata.
   ============================================================ */
function f0(d){
  var c = el("div", "capa"), nome = "CLASSES DE PALAVRAS", k, letras = "";
  nome.split(" ").forEach(function(pal, w){
    var s = "";
    for(k = 0; k < pal.length; k++) s += '<span class="lt">' + pal.charAt(k) + '</span>';
    letras += (w ? '<span class="esp"></span>' : '') + '<span class="tpal">' + s + '</span>';
  });
  c.innerHTML =
    '<div class="ceu"></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 5º ano &middot; 35 folhas</div>' +
    '<div class="cena capacena">' +
      '<div class="cpeca">' + fig("casa", "figcapa") + '<b>CASA</b><i>ALTA</i></div>' +
      '<div class="cpeca">' + fig("gato", "figcapa") + '<b>GATO</b><i>PELUDO</i></div>' +
      '<div class="cpeca">' + fig("flor", "figcapa") + '<b>FLOR</b><i>CHEIROSA</i></div>' +
      '<div class="cpeca">' + fig("livro", "figcapa") + '<b>LIVRO</b><i>GROSSO</i></div>' +
    '</div>' +
    '<div class="chamada">Toda palavra tem um lugar. Vamos descobrir o de cada uma?<br>' +
    'Escreva o seu nome ali embaixo e toque em <b>Começar</b>.</div>';
  d.appendChild(c);
}

/* ====================== BLOCO A — O SUBSTANTIVO ====================== */
function f01(d, pi){
  folhaEscreve(d, pi, "Estas coisas existem. Escreva o <b>nome</b> de cada uma.", "FIG",
    function(x, k){ return fig(k) + '<span class="qtxt">Que coisa é esta?</span>'; },
    function(x){ return x.t; }, function(x){ return "Escreva " + x.t; });
}
function f02(d, pi){
  gavetas(d, pi, "quem", "Todo substantivo dá nome a alguma coisa. Ponha cada um na gaveta: <b>gente</b>, <b>coisa</b> ou <b>lugar</b>.");
}
function f03(d, pi){
  escolhe(d, pi, "Agora olhe a <b>letra do começo</b>. Qual das duas é nome <b>próprio</b>?", "P3",
    function(x){ return {rot: "Qual é o nome PRÓPRIO?",
      ops: [{v:"pr", rot:x[1], fala:"diz_" + x[0]}, {v:"co", rot:x[2], fala:"diz2_" + x[0]}],
      certa: "pr"}; });
}
function f04(d, pi){
  montaSilabas(d, pi, "De uma palavra nasce outra. Monte a palavra <b>derivada</b> com as sílabas.", "P4");
}
function f05(d, pi){
  escolhe(d, pi, "Agora <b>duas palavras viram uma</b>. Qual é a palavra composta certa?", "P5",
    function(x, k){ return {rot: x[0] + " + " + x[1] + " = ?",
      ops: [{v:"ok", rot:x[2], fala:"diz_" + k}, {v:"x", rot:x[1] + x[0], fala:"diz2_" + k}],
      certa: "ok"}; });
}
function f06(d, pi){
  marcaFrase(d, pi, "Os substantivos estão escondidos na frase. Toque em <b>cada um</b> deles.", "P6");
}
function f07(d, pi){
  achaNoBanco(d, pi, "Ache <b>todos os substantivos</b> — e só eles.",
    D.P7, ["ALTO", "CORRER", "BONITO", "PULAR", "VERDE", "DORMIR"]);
}

/* ====================== BLOCO B — O ADJETIVO ====================== */
function f08(d, pi){
  folhaEscreve(d, pi, "Agora não é o nome: é <b>como a coisa é</b>. Escreva uma característica.", "FIG",
    function(x, k){ return fig(k) + '<span class="qtxt">Como é este(a) ' + x.t.toLowerCase() + '?</span>'; },
    function(x){ return x.adj; }, function(x){ return "Escreva " + x.adj; });
}
function f09(d, pi){
  escolhe(d, pi, "Qual adjetivo <b>combina</b> com a coisa?", "P9",
    function(x, k){ return {rot: x[0] + " …",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"},
            {v:"c", rot:x[3], fala:"diz_" + k + "c"}],
      certa: "a"}; });
}
function f10(d, pi){
  duasCores(d, pi, "Agora as <b>duas classes juntas</b> na mesma frase.", "P10");
}
function f11(d, pi){
  escolhe(d, pi, "Agora a <b>MESMA palavra</b>. O que ela é <b>nesta frase</b>?", "P11",
    function(x, k){ return {rot: x[0], cls: "frase",
      ops: [{v:"substantivo", rot:"SUBSTANTIVO", fala:"diz_subst"},
            {v:"adjetivo", rot:"ADJETIVO", fala:"diz_adj"}],
      certa: x[1]}; });
}
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Às vezes o adjetivo vem em <b>duas palavras</b>. Ligue cada uma ao adjetivo que vale o mesmo.", "p" + pi + "enun");
  /* ⚠️ O `montaLigar` le OBJETOS, nao listas: ele grava `l<pi><tag>_<P.k>` e
     desenha `P.esq` e `P.dir`. Passando lista, `P.k` sai `undefined` e a folha
     registra UM item so — ela NUNCA fecharia, e a criança ligaria tudo
     continuando a faltar. Foi o `conta_folha` que pegou, antes de ir ao ar. */
  var box = item(0), pares = [];
  ST.folha["p" + pi][0].forEach(function(k){
    var L = D.P12[k];
    pares.push({k: k, esq: L[0], dir: L[1],
                fe: "diz_" + k + "e", fd: "diz_" + k + "d",
                fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k,
                ariaE: L[0], ariaD: L[1]});
  });
  /* ⚠️ a etiqueta e "g0", nao um nome qualquer: o `idsDaPagina` monta o id como
     `l<folha>g<i>_<chave>`, e e POR ELE que o relatorio do professor conta. Com
     outra etiqueta a folha funciona na tela e sai ZERO no relatorio — defeito
     que so aparece no papel do professor, nunca na mao da crianca. */
  montaLigar(box, pi, "g0", pares, d);
  d.appendChild(box);
}
function f13(d, pi){
  escolhe(d, pi, "O adjetivo tem <b>graus</b>. Em que grau está o adjetivo desta frase?", "P13",
    function(x, k){ return {rot: x[0], cls: "frase",
      ops: [{v:"comparativo", rot:"COMPARATIVO", fala:"diz_comp"},
            {v:"superlativo", rot:"SUPERLATIVO", fala:"diz_sup"}],
      certa: x[1]}; });
}
function f14(d, pi){
  folhaEscreve(d, pi, "Escreva o adjetivo que a dica pede.", "P14",
    function(x){ return x[1]; }, function(x){ return x[0]; },
    function(x){ return "Escreva " + x[0]; });
}

/* ====================== BLOCO C — O VERBO DE AÇÃO ====================== */
function f15(d, pi){
  folhaEscreve(d, pi, "O verbo diz <b>o que se faz</b>. Complete a frase com o verbo.", "P15",
    function(x){ return x[0]; }, function(x){ return x[1]; },
    function(x){ return "Escreva " + x[1]; });
}
function f16(d, pi){
  gavetas(d, pi, "verbo", "Nem todo verbo é ação. Ponha cada um na gaveta certa.");
}
function f17(d, pi){
  marcaFrase(d, pi, "Agora ache os <b>verbos</b> escondidos na frase.", "P17", "marcada3");
}
function f18(d, pi){
  escolhe(d, pi, "A mesma ação em <b>três tempos</b>. Qual forma cabe em cada um?", "P18",
    function(x, k){ return {rot: x[0] + " …", cls: "frase",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f19(d, pi){
  escolhe(d, pi, "Agora passe a frase para <b>ontem</b>.", "P19",
    function(x, k){ return {rot: x[0] + " &rarr; ontem…", cls: "frase",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f20(d, pi){
  escolhe(d, pi, "Agora para <b>amanhã</b>.", "P20",
    function(x, k){ return {rot: x[0] + " &rarr; amanhã…", cls: "frase",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f21(d, pi){
  escolhe(d, pi, "Quem faz a ação <b>manda no verbo</b>. Complete.", "P21",
    function(x, k){ return {rot: x[0], cls: "frase",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}

/* ================ BLOCO D — AUMENTATIVO E DIMINUTIVO ================ */
function f22(d, pi){
  escolhe(d, pi, "Toda palavra pode ficar <b>pequena</b> ou <b>grande</b>. Qual destas é o aumentativo?", "P22",
    function(x, k){ return {rot: "O normal é <b>" + x[1] + "</b>. E o aumentativo?",
      ops: [{v:"a", rot:x[2], fala:"diz_" + k + "a"}, {v:"b", rot:x[0], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f23(d, pi){
  folhaEscreve(d, pi, "Escreva a palavra no <b>diminutivo</b>.", "P23",
    function(x){ return x[0] + " &rarr; pequeno(a)…"; }, function(x){ return x[1]; },
    function(x){ return "Escreva " + x[1]; });
}
function f24(d, pi){
  folhaEscreve(d, pi, "Agora no <b>aumentativo</b>.", "P24",
    function(x){ return x[0] + " &rarr; grande…"; }, function(x){ return x[1]; },
    function(x){ return "Escreva " + x[1]; });
}
function f25(d, pi){
  achaNoBanco(d, pi, "Ache <b>todas</b> as palavras que estão no diminutivo.",
    [D.P25.palavras[0], D.P25.palavras[2], D.P25.palavras[4]],
    [D.P25.palavras[1], D.P25.palavras[3], D.P25.palavras[5]]);
}
function f26(d, pi){
  gavetas(d, pi, "grau", "São as <b>terminações</b> que fazem o grau. Ponha cada uma na gaveta.");
}
function f27(d, pi){
  escolhe(d, pi, "Cuidado: nem tudo que acaba em <b>-inho</b> é diminutivo!", "P27",
    function(x, k){ return {rot: "<b>" + x[0] + "</b> é diminutivo?",
      ops: [{v:"sim", rot:"SIM", fala:"diz_sim"}, {v:"nao", rot:"NÃO", fala:"diz_nao"}],
      certa: x[1]}; });
}
function f28(d, pi){
  folhaEscreve(d, pi, "Escreva a palavra que a dica descreve.", "P28",
    function(x){ return x[1]; }, function(x){ return x[0]; },
    function(x){ return "Escreva " + x[0]; });
}

/* ================ BLOCO E — SINGULAR E PLURAL ================ */
function f29(d, pi){
  folhaEscreve(d, pi, "Uma coisa vira <b>muitas</b>. Escreva no plural.", "P29",
    function(x){ return "uma " + x[0] + " &rarr; muitas…"; }, function(x){ return x[1]; },
    function(x){ return "Escreva " + x[1]; });
}
function f30(d, pi){
  escolhe(d, pi, "Agora as palavras terminadas em <b>-ÃO</b> — e elas não fazem todas igual.", "P30",
    function(x, k){ return {rot: "um " + x[0] + " &rarr; muitos…",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f31(d, pi){
  escolhe(d, pi, "Agora as terminadas em <b>-L</b>.", "P31",
    function(x, k){ return {rot: "um " + x[0] + " &rarr; muitos…",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f32(d, pi){
  gavetas(d, pi, "plural", "Cada palavra faz o plural de um jeito. Ponha cada uma no seu.");
}
function f33(d, pi){
  escolhe(d, pi, "No plural, <b>a frase inteira muda</b> — não só o substantivo.", "P33",
    function(x, k){ return {rot: x[0] + " &rarr; no plural…", cls: "frase",
      ops: [{v:"a", rot:x[1], fala:"diz_" + k + "a"}, {v:"b", rot:x[2], fala:"diz_" + k + "b"}],
      certa: "a"}; });
}
function f34(d, pi){
  gavetas(d, pi, "numero", "Última gaveta: esta palavra está no <b>singular</b> ou no <b>plural</b>?");
}

/* ====================== O FECHO ====================== */
function f35(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Uma frase, três classes. Toque em cada palavra e diga o que ela é.", "p" + pi + "enun");
  var id = "n" + pi + "_0", box = item(0);
  var FR = [["A", null], ["FLOR", "s"], ["CHEIROSA", "a"], ["ABRIU", "v"], ["hoje", null], [".", null]];
  var alvos = [], k;
  for(k = 0; k < FR.length; k++) if(FR[k][1]) alvos.push(k);
  registra(id, pi, alvos.join(" "));
  var quadro = el("div", "cartaz",
    '<div class="cz s"><b>SUBSTANTIVO</b><span>dá o nome</span></div>' +
    '<div class="cz a"><b>ADJETIVO</b><span>diz como é</span></div>' +
    '<div class="cz v"><b>VERBO</b><span>diz o que faz</span></div>');
  var linha = el("div", "frasemarca"), postas = {};
  FR.forEach(function(par, i){
    var b = el("button", "pmarca", par[0]);
    b.setAttribute("data-qa", "op-" + id + "-" + i);
    b.onclick = function(){
      if(ST.resp[id] || postas[i]) return;
      sPasso();
      if(!par[1]){
        b.className = "pmarca nao";
        setTimeout(function(){ b.className = "pmarca"; }, 500);
        errou(id, "dica" + pi + "_0"); return;
      }
      postas[i] = 1; b.className = "pmarca cz" + par[1];
      if(Object.keys(postas).length === alvos.length) acertou(id, "certo" + pi + "_0");
    };
    linha.appendChild(b);
  });
  box.appendChild(quadro); box.appendChild(linha);
  box.appendChild(el("div", "gancho",
    "E a palavra que <b>muda de classe</b> conforme a frase — você lembra qual era?"));
  fechaItem(d, box, id);
}
