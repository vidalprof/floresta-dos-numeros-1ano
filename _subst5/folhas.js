/* ============================================================
   A FÁBRICA DE NOMES — as vinte e cinco folhas.

   Substantivos no 5º ano: comum e próprio · simples e composto · primitivo e
   derivado · coletivo — e tudo desembocando num TEXTO, porque a professora
   pediu *"leitura e interpretação de textos"* junto com a gramática.

   Cada folha nasceu de um VERBO impresso numa das 30 folhas de papel colhidas
   por workflow. O crivo, folha a folha, com o comando VERBATIM e o motivo das
   três recusas (uma em galego, uma que ensina "chaves = penca" e uma que chama
   "bom" de substantivo), está em `_sequencias/POTE-SUBST5.md`. Nenhuma mecânica
   foi escolhida do nosso cardápio: o papel é que manda.

   ⚠️ A POSIÇÃO É A IDENTIDADE: a folha da posição 7 usa o pote `p7`, grava os
      ids `n7_*` e fala `p7enun`. Não há segunda lista para desencontrar — isso
      já fez o relatório sair ZERO com a folha inteira respondida.
   ============================================================ */

var livro = document.getElementById("livro"), PAGEL = [], TIRAS = [];
/* ⚠️ AS FOLHAS DE LIGAR SE DECLARAM AQUI — são as únicas cujos ids não nascem
   de `n<pi>_`, e sim dentro do `montaLigar` (`l<pi>g<i>_<chave>`). */
var LIGAR = [15, 18, 23];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou (o mesmo ser com dois nomes · a maiúscula · simples e composto ·
   primitivo e derivado · o coletivo · o texto) */
var CORES = ["c1","c1","c1","c1","c1", "c2","c2","c2","c2",
             "c3","c3","c3","c3","c3","c3",
             "c4","c4","c4","c4","c4","c4","c4",
             "c5", "c2","c3"];

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

function monta(){
  livro.innerHTML = ""; PAGEL = []; RESP = {}; TIRAS = [];
  var caps = [f0,
    f01, f02, f03, f04, f05,       /*  1-5   o mesmo ser tem dois nomes        */
    f06, f07, f08, f09,            /*  6-9   a maiúscula, e o nome que é MEU   */
    f10, f11, f12, f13, f14, f15,  /* 10-15  uma palavra ou duas juntas        */
    f16, f17, f18, f19, f20, f21, f22, /* 16-22 de onde veio esta palavra      */
    f23,                           /* 23     um nome para muitos               */
    f24, f25], i;                  /* 24-25  no texto, e o cartaz que eu levo  */
  for(i = 0; i < caps.length; i++){
    var d = el("div", "pagina" + (i > 0 ? " " + CORES[i - 1] : "")); d.setAttribute("data-pag", i);
    caps[i](d, i);
    if(i > 0) d.appendChild(el("div", "carimbo", "FOLHA<br>PRONTA"));
    livro.appendChild(d); PAGEL.push(d);
  }
}

/* ---------- capa ----------
   O tema sai do problema: TUDO tem nome, e alguns nomes são só daquele um. A
   fábrica é isso — de um lado entra a coisa, do outro sai o nome dela, e às
   vezes sai com letra maiúscula.
   ⚠️ CAPA CLONADA = TROCAR A CENA, SEMPRE. Numa capa herdada desta casa ficou
      um `img()` de outra atividade: o app abria com um quadradinho vazio e um
      404 no console, e nenhum portão de texto viu. Esta capa não usa figura
      nenhuma — as palavras SÃO o desenho. */
function f0(d){
  var c = el("div", "capa"), nome = "A FÁBRICA DE NOMES", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.04 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  var cena = "";
  [["cachorro", "Bob"], ["menina", "Ana"], ["cidade", "Blumenau"]].forEach(function(p){
    cena += '<span class="dupla"><b>' + p[0] + "</b><i>" + p[1] + "</i></span>";
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i><i class="sol"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Língua Portuguesa &middot; 5º ano &middot; vinte e cinco folhas sobre os nomes das coisas</div>' +
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

/* ============ 1 — O MESMO SER TEM DOIS NOMES ============
   ⭐ ESTA FOLHA NÃO EXISTE EM NENHUMA DAS TRINTA. Ela nasce de uma coisa que a
      d20 e a d25 MOSTRAM sem pedir nada: o mesmo menino é *menino* e é *Pedro*;
      o mesmo pato é *pato* e é *Patolino*. As duas folhas imprimem isso como
      cartaz, para a criança olhar. Aqui vira tarefa — e é a única folha do
      caderno que faz a pergunta que interessa antes de dar qualquer nome à
      resposta: *"qual destes dois nomes serve para TODOS os patos do mundo?"*
   ⭐ É O PROBLEMA ANTES DO CONCEITO (Portão 0): as palavras "comum" e "próprio"
      não aparecem nesta folha. Elas entram na folha 2, quando a criança já
      separou as duas coisas com a mão.
   ⚠️ A FIGURA VEM DA PRÓPRIA FOLHA DE PAPEL (d25 e d28), pela regra do Marcos
      de 14/set: *"nada de imagem gerada por IA, utilize das atividades"*. */
function f01(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe o desenho. Um destes nomes serve para <b>todos</b> " +
            "os que são assim. Qual é?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PAR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var c = el("div", "figsil");
    c.innerHTML = img(P.f, "figgrande", P.alt);
    var lin = el("div", "chamlin");
    lin.appendChild(el("span", "ajuda", "Este aqui se chama " + P.p + "."));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("par_" + k); }));
    c.appendChild(lin);
    box.appendChild(c);
    /* as duas fichas embaralhadas: o nome da espécie e o nome de batismo */
    var lista = baralha([{v: "c", rot: P.c, aria: P.c, fala: "diz_" + k + "_c"},
                         {v: "p", rot: P.p, aria: P.p, fala: "diz_" + k + "_p"}]);
    opcoes(box, pi, id, lista, "c", "pal",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 2, 4 e 5 — AS GAVETAS DO COMUM E DO PRÓPRIO ============
   folha 2 — da d02, VERBATIM: *"1 – Classifique os substantivos conforme a
             legenda: (P) substantivo próprio (C) substantivo comum"*
   folha 4 — da d27, VERBATIM: *"1) RECORTE OS SUBSTANTIVOS E COLE NA COLUNA
             CORRETA"*. Recortar e colar É a gaveta: o gesto do papel, na tela.
   folha 5 — da d07 e da d16: *"Leia e escreva cada substantivo no quadro
             correspondente"* / *"Organize nas tabelas os substantivos próprios
             e comuns"*. Aqui sem figura nenhuma: só a palavra e a maiúscula.
   ⭐ E ELAS VÊM EM BLOCO, COLADAS, subindo um degrau de cada vez (Marcos,
      ago/2026: *"as repetições das interatividades têm que ser seguidas e não
      espaçadas — as crianças me dizem 'isso eu já fiz'"*). O que sobe não é a
      tela: é o apoio que some. Na 2 a palavra vem com a inicial à mostra; na 4
      a criança tem a figura ao lado; na 5 não tem nada além da palavra.
   ⚠️ AS DUAS PORTAS: arrastar a palavra até a gaveta (PC) e tocar na palavra e
      depois na gaveta (celular). */
function f02(d, pi){ gavetas(d, pi, "cp1",
  "Uma gaveta é dos nomes que servem para <b>muitos</b>. A outra é dos nomes de <b>um só</b>."); }
function f04(d, pi){ gavetas(d, pi, "cp2",
  "Recorte e cole: leve cada palavra para a coluna certa."); }
function f05(d, pi){ gavetas(d, pi, "cp3",
  "Agora sem desenho nenhum. Olhe a <b>primeira letra</b> de cada palavra."); }

/* ============ 3 — PINTE O RETÂNGULO: COMUM OU PRÓPRIO? ============
   Da d28 (Atividades Suzano), VERBATIM: *"Pinte o retângulo de acordo com o
   substantivo indicado:"*. A folha impressa mostra nove desenhos, cada um com o
   seu nome e dois retângulos — COMUM e PRÓPRIO — para pintar.
   ⭐ Ela entra entre a 2 e a 4 porque o degrau dela é a FIGURA: aqui a criança
      vê a coisa e o nome dela ao mesmo tempo, e é assim que se percebe que
      *cavalo* é o nome do bicho e *Pluto* é o nome daquele cão.
   ⚠️ O NOME FOI CORTADO FORA DA FIGURA no recorte (`so_o_desenho`): na folha de
      papel ele vem impresso ao lado do desenho, e trazê-lo junto entregaria a
      resposta. Quem viu isso foi o olho, na folha de contato. */
function f03(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Este nome serve para <b>muitos</b> ou é de <b>um só</b>? " +
            "Toque na resposta.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var F = FIG[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var c = el("div", "figsil");
    c.innerHTML = img(F.f, "figgrande", F.alt);
    var lin = el("div", "chamlin");
    /* ⚠️ ALVO DECLARADO: aqui o NOME é a pergunta, não a resposta. A criança
       precisa LER "cavalo" para decidir se aquele nome serve para muitos — é o
       comando impresso da d28 ("Pinte o retângulo de acordo com o substantivo
       indicado"). Sem o `data-alvo`, o portão `_qa/resposta_impressa.py` o toma
       por resposta entregue, e escondê-lo deixaria a folha sem enunciado. */
    var _nm = el("div", "pgrande", F.n);
    _nm.setAttribute("data-alvo", "1");
    lin.appendChild(_nm);
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("diz_" + k); }));
    c.appendChild(lin);
    box.appendChild(c);
    opcoes(box, pi, id,
           [{v: "c", rot: "COMUM", aria: "Comum", fala: "op_comum"},
            {v: "p", rot: "PRÓPRIO", aria: "Próprio", fala: "op_proprio"}],
           F.r, "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 6 — POR QUE UNS COMEÇAM COM LETRA GRANDE? ============
   ⭐ BLOCO NOVO, DECLARADO: nenhuma das trinta folhas EXPLICA a maiúscula. A
      d08 pede para achar o erro e a d20 diz, num cartaz, *"é sempre iniciado
      com letra maiúscula"* — mas nenhuma faz a criança decidir. E é justamente
      aqui que o 5º ano erra: escreve *"fui à Escola"* e *"meu amigo pedro"*.
   ⭐ E O CONCEITO VEM POR ÚLTIMO, que é a lei da casa: só agora, depois de a
      criança ter separado as palavras com a mão em três folhas, é que aparece a
      regra — e ela aparece como JULGAMENTO, não como texto para ler. */
function f06(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta frase está escrita <b>certa</b> ou tem alguma letra " +
            "grande no lugar errado?", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var J = JULGA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasel", J.f));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("frase_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id,
           [{v: "s", rot: "Está certa", aria: "Está certa", fala: "op_certa"},
            {v: "n", rot: "Tem erro", aria: "Tem erro", fala: "op_erro"}],
           J.r, "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k,
           function(){ var a = el("div", "ajuda"); a.appendChild(nomeSecreto(J.pq, id)); box.appendChild(a); });
    fechaItem(d, box, id);
  });
}

/* ============ 7 — ACHE O QUE NÃO ESTÁ CORRETO ============
   Da d08 (Educando), VERBATIM: *"3º) Leia um trecho da história Aventuras de
   Buscapé. Descubra o que não está correto e escreva novamente sem cometer as
   mesmas falhas"*. O trecho dela vem com as maiúsculas todas trocadas:
   *"buscapé é um Cãozinho vira-lata muito sapeca que um dia foi morar na Casa
   do joão, Motorista de táxi…"*.
   ⭐ É A FOLHA MAIS DIFÍCIL DO BLOCO e é de propósito: até aqui a criança
      decidia sobre uma palavra por vez, apresentada sozinha. Aqui as palavras
      estão dentro de um texto corrido, que é onde o erro acontece de verdade.
   ⚠️ O texto do papel pede REESCREVER, que é produção escrita — a tela não
      corrige isso. O que a tela mede é ACHAR: toque em cada palavra que está
      com a letra errada. O reescrever fica para o caderno de papel, e o dossiê
      do professor diz isso. */
function f07(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Neste pedaço da história há palavras com a letra do começo " +
            "trocada. Toque em <b>cada uma</b> que está errada.", "p" + pi + "enun");
  var id = "n" + pi + "_0", T = ERRADO[ST.folha["p" + pi][0]];
  /* ⚠️ A CONTA É POR POSIÇÃO, NÃO POR PALAVRA, e isto foi um defeito de verdade
     que o jogador da banca pegou: o trecho da d08 tem "joão" DUAS vezes, as duas
     com a letra errada. Contando por palavra havia nove nomes na lista e DEZ
     botões que fechavam — a folha fecharia com a segunda "joão" ainda errada na
     tela, e o relatório diria que a criança acertou tudo.
     ⚠️ E É A POSIÇÃO QUE VAI DECLARADA (`w0 w3 w13 …`), porque é dela que o
     jogador precisa: com o nome da palavra ele não saberia em qual das duas
     "joão" tocar. */
  var _ruins = [];
  T.palavras.forEach(function(w, n){
    var pura = chaveQuadro(w.replace(/[^A-Za-zÀ-ÿ]/g, ""));
    if(T.erradas.indexOf(pura) > -1) _ruins.push(n);
  });
  registra(id, pi, _ruins.map(function(n){ return "w" + n; }).join(" "));
  var box = item(0);
  var lin = el("div", "enunlin");
  lin.appendChild(el("div", "ajuda", T.titulo));
  lin.appendChild(botaoSom("Ouvir o trecho", function(){ falar("trecho_" + T.k); }));
  box.appendChild(lin);
  var cx = el("div", "textinho"), faltam = _ruins.length, achadas = {};
  T.palavras.forEach(function(w, n){
    var pura = w.replace(/[^A-Za-zÀ-ÿ]/g, ""), cha = chaveQuadro(pura);
    var ruim = _ruins.indexOf(n) > -1;
    var b = el("button", "tp", w);
    b.setAttribute("aria-label", pura);
    b.setAttribute("data-qa", (ruim ? "op-" + id + "-w" + n : "no-" + id + "-" + cha + n));
    b.onclick = function(){
      if(ST.resp[id] || achadas[n]) return;
      sPasso();
      if(ruim){
        achadas[n] = 1; b.className = "tp achada";
        b.textContent = w.charAt(0) === w.charAt(0).toUpperCase()
          ? w.charAt(0).toLowerCase() + w.slice(1)
          : w.charAt(0).toUpperCase() + w.slice(1);
        faltam--;
        if(!faltam) acertou(id, "certo" + pi);
      } else {
        b.className = "tp nao";
        setTimeout(function(){ b.className = "tp"; }, 420);
        errou(id, "dica" + pi);
      }
    };
    cx.appendChild(b);
    cx.appendChild(document.createTextNode(" "));
  });
  box.appendChild(cx);
  fechaItem(d, box, id);
}

/* ============ 8 — DE ONDE ELE É? ============
   Da d02, VERBATIM: *"2 – Complete as frases, usando substantivos próprios.
   Siga o exemplo: Ele é espanhol. Nasceu na Espanha."*
   ⭐ Aqui a criança não escolhe entre opções: ela ESCREVE o nome próprio, com a
      maiúscula na mão. É o degrau que fecha o bloco — reconhecer é uma coisa,
      escrever com a letra certa é outra.
   ⚠️ O teclado é o mesmo da casa e o teclado DE VERDADE funciona junto: no PC
      da escola a criança vai digitar. E ele aceita a palavra com ou sem acento
      (ver `confereCruz`), porque o que se mede aqui é o nome próprio e a
      maiúscula, não o acento. */
function f08(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Complete a frase com o <b>nome do lugar</b>. " +
            "Ele começa com letra grande.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var G = GENT[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, G.r);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "frasel", G.a + ' <i class="lacuna"></i>' + G.b));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("gent_" + k); }));
    box.appendChild(lin);
    var grade = el("div", "cruz uma"), cels = [], t;
    grade.setAttribute("data-qa", "esc-" + id);
    for(t = 0; t < G.r.length; t++){
      var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? G.r.charAt(t) : "");
      c.setAttribute("aria-label", "Casa da palavra");
      cels.push(c); grade.appendChild(c);
    }
    var E = {k: k, w: G.r, id: id, cels: cels, n: i + 1,
             rot: "Escreva o nome do lugar", bt: el("span", "pista oculta", "")};
    cels.forEach(function(c){ c.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); }; });
    grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
    box.appendChild(grade);
    fechaItem(d, box, id);
  });
}

/* ============ 9 — OS NOMES QUE SÃO MEUS ============
   Da d18 (Atividades Suzano), VERBATIM: *"Complete o quadro abaixo: Seu nome ·
   Sua escola · Sua professora · Sua cidade · Seu Estado · Seu bairro…"* e, logo
   abaixo, *"No quadro acima, pinte os substantivos próprios de azul e de
   vermelho os comuns"*. A d27 pede a mesma coisa: *"2) ESCREVA SOBRE VOCÊ E
   DESTAQUE A LETRA MAIÚSCULA DOS SUBSTANTIVOS PRÓPRIOS"*.
   ⭐ É A FOLHA MAIS PESSOAL DO CADERNO, e por isso ela fecha o bloco: depois de
      nove folhas decidindo sobre patos e cavalos, a criança descobre que ELA
      tem um nome próprio, e a escola dela, e a cidade dela. A gramática vira
      uma coisa que fala dela.
   ⚠️ O NOME DA CRIANÇA JÁ ESTÁ ALI: ele vem do crachá da capa (`ST.nome`), e é
      por isso que a primeira linha já vem preenchida e valendo. */
function f09(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora é sobre <b>você</b>. Escreva e depois diga se cada " +
            "resposta é um nome de um só.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MEU[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", M.p));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("meu_" + k); }));
    box.appendChild(lin);
    /* ⚠️ AQUI NÃO HÁ RESPOSTA CERTA: o nome da escola da criança é o nome da
       escola dela. O que se mede é a DECISÃO — este nome é de um só ou serve
       para muitos? — e essa tem gabarito. */
    var dado = el("div", "montada");
    dado.setAttribute("data-feito", M.ex === "nome" ? (ST.nome || "o seu nome") : M.ex);
    box.appendChild(dado);
    opcoes(box, pi, id,
           [{v: "c", rot: "serve para muitos", aria: "Serve para muitos", fala: "op_comum"},
            {v: "p", rot: "é de um só", aria: "É de um só", fala: "op_proprio"}],
           M.r, "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
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
/* ============ 10 — UMA PALAVRA SÓ, OU DUAS COLADAS? ============
   Da d23 (educador), VERBATIM: *"Classifique os substantivos em simples ou
   compostos:"*, e da d29: *"Indique quais palavras abaixo são substantivos
   simples e compostos"*.
   ⭐ Ela abre o bloco pelo GESTO QUE A CRIANÇA JÁ SABE (a gaveta das folhas 2, 4
      e 5) com conteúdo NOVO. Isso é de propósito: quando o assunto muda, a tela
      não muda junto — senão a criança gasta a cabeça aprendendo a tela em vez
      de aprender a matéria (carga cognitiva, Sweller). */
function f10(d, pi){ gavetas(d, pi, "sc",
  "Quantas palavras estão escondidas dentro de cada uma? <b>Uma</b> ou <b>duas</b>?"); }

/* ============ 11 — CIRCULE AS QUE TÊM NOME DE DUAS PALAVRAS ============
   Da d04 (tudoportugues), VERBATIM: *"4. Circule as imagens cujos nomes são
   substantivos compostos."*
   ⭐ E AS SEIS FIGURAS SÃO AS DELA — pão, couve-flor, livros, beija-flor, tênis,
      guarda-chuva —, recortadas daquela mesma folha. A criança reencontra na
      tela o desenho que está no papel que a professora entrega.
   ⚠️ A PALAVRA NÃO APARECE ANTES DA RESPOSTA em três delas de propósito: se
      "couve-flor" estiver escrito com o hífen embaixo do desenho, não há nada
      para pensar — o hífen entrega tudo. O nome aparece no acerto. */
function f11(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Marque as figuras cujo nome tem <b>duas palavras</b> " +
            "juntas. Depois toque em <b>Conferir</b>.", "p" + pi + "enun");
  var id = "n" + pi + "_0", lista = ST.folha["p" + pi][0], certas = [];
  lista.forEach(function(k){ if(FIGC[k].comp) certas.push(k); });
  registra(id, pi, certas.join(" "));
  var box = item(0);
  var cx = el("div", "marcax fichas"), marcadas = {}, bts = {};
  baralha(lista.slice(0)).forEach(function(k){
    var F = FIGC[k];
    var b = el("button", "lx ficha",
               '<span class="cx"></span>' + img(F.f, "figmini", F.alt) +
               '<span class="ft"></span>');
    b.setAttribute("aria-label", F.alt);
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
      bts[kk].className = "lx ficha " + (FIGC[kk].comp ? "certa" : "erroficha");
      if(FIGC[kk].comp) bts[kk].querySelector(".cx").textContent = "X";
      bts[kk].querySelector(".ft").innerHTML = "<b>" + FIGC[kk].n + "</b>";
    }
  }
  var bt = el("button", "bt pronto", "Conferir");
  bt.setAttribute("data-qa", "conferir-" + id);
  bt.onclick = function(){
    if(ST.resp[id]) return;
    var erro = 0, kk;
    for(kk in bts) if(!!FIGC[kk].comp !== !!marcadas[kk]) erro++;
    if(erro){
      for(kk in bts) if(marcadas[kk] && !FIGC[kk].comp) bts[kk].className = "lx ficha errada";
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

/* ============ 12 — JUNTE AS DUAS E FORME UMA ============
   Da d04, VERBATIM: *"2. Reescreva os substantivos compostos abaixo de forma
   correta."* — e a folha traz "Arco + íris", "Guarda + Chuva", "Micro + ondas",
   "Bate + papo", "Água + ardente", "Flor + cultura".
   ⭐ É ONDE O HÍFEN VIRA CONTEÚDO: *guarda-chuva* leva hífen e *microondas*
      virou *micro-ondas*, mas *aguardente* não leva nada e perde letra. A
      criança monta tocando nos pedaços, e o que ela descobre é que juntar não é
      só encostar uma palavra na outra.
   ⚠️ A RESPOSTA DECLARADA É A FILA DE PEDAÇOS NA ORDEM, não a palavra pronta —
      lição paga na Loteria do S: com a palavra pronta, ninguém (nem o jogador
      da banca, nem o relatório) sabia em que ordem tocar, e a folha ficava sem
      medida nenhuma. */
function f12(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Junte as duas palavras e forme uma só. Toque nos pedaços " +
            "na <b>ordem certa</b>.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = COMPOR[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "pgrande", C.a + " + " + C.b));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("comp_" + k); }));
    box.appendChild(lin);
    var mostra = el("div", "montada"), feito = "";
    mostra.appendChild(nomeSecreto(C.r, id));
    registra(id, pi, C.pedacos.map(function(p){ return chaveQuadro(p) || "hifen"; }).join(" "));
    var linha = el("div", "ops sils"), passo = 0, bts = [];
    baralha(C.pedacos.map(function(p, j){ return j; })).forEach(function(j){
      var p = C.pedacos[j];
      var b = el("button", "op curta sil", p === "-" ? "–" : p);
      b.setAttribute("aria-label", p === "-" ? "Traço de união" : "Pedaço " + p);
      b.setAttribute("data-qa", "op-" + id + "-" + (chaveQuadro(p) || "hifen"));
      bts.push(b);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(passo === j){
          b.className = "op curta sil usada";
          feito += p; passo++;
          mostra.setAttribute("data-feito", feito);
          if(passo >= C.pedacos.length) acertou(id, "certo" + pi + "_" + k);
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

/* ============ 13 — GRIFE NA FRASE ============
   Da d17, VERBATIM: *"1– Grife os substantivos compostos em cada frase:"* — e
   as frases são as dela: *"O arco-íris estava lindo!"*, *"Eu amo comer
   cachorro-quente!"*, *"Mamãe fez couve-flor para o almoço."*, *"Havia um
   sapo-boi no quintal."*, *"O beija-flor pousou na minha mão."*
   ⭐ O degrau: nas folhas 10 a 12 a palavra vinha sozinha, em destaque. Aqui ela
      está escondida no meio de uma frase, que é onde ela mora de verdade. */
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Em cada frase há <b>uma</b> palavra feita de duas. " +
            "Toque nela.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var F = GRIFA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    registra(id, pi, chaveQuadro(F.alvo));
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Leia a frase e ache a palavra."));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("grifa_" + k); }));
    box.appendChild(lin);
    var cx = el("div", "textinho");
    F.palavras.forEach(function(w, n){
      var pura = w.replace(/[^A-Za-zÀ-ÿ-]/g, "");
      var certa = chaveQuadro(pura) === chaveQuadro(F.alvo);
      var b = el("button", "tp", w);
      b.setAttribute("aria-label", pura);
      b.setAttribute("data-qa", (certa ? "op-" + id + "-" + chaveQuadro(F.alvo) : "no-" + id + "-" + n));
      if(ST.resp[id] && certa) b.className = "tp achada";
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso();
        if(certa){ b.className = "tp achada"; acertou(id, "certo" + pi + "_" + k); }
        else {
          b.className = "tp nao";
          setTimeout(function(){ b.className = "tp"; }, 420);
          errou(id, "dica" + pi + "_" + k);
        }
      };
      cx.appendChild(b);
      cx.appendChild(document.createTextNode(" "));
    });
    box.appendChild(cx);
    fechaItem(d, box, id);
  });
}

/* ============ 14 — TUDO GRUDADO ============
   Da d22, VERBATIM: *"2) Encontre substantivos e copie-os nas colunas
   adequadas, colocando hífen quando necessário."* — e a folha dela traz a linha
   toda colada: *"GIRASSOLPORTARETRATOSALSICHATELEVISÃOPENSAMENTOBOMBOMGOIABA
   GUARDACHUVABEIJAFLOR"*.
   ⭐ É A FOLHA QUE MAIS JUNTA LEITURA E GRAMÁTICA do caderno: para saber onde
      uma palavra acaba, a criança precisa RECONHECER a palavra escrita — o som
      não ajuda, porque na fala a gente também não separa.
   ⚠️ O gesto é tocar ENTRE duas letras, no lugar onde entra o corte. É o único
      gesto deste caderno em que o alvo não é uma coisa, e sim um vão.
   ⚠️ A RESPOSTA DECLARADA SÃO OS CORTES, não a linha separada: o jogador da
      banca precisa do CAMINHO, não do resultado. */
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Estas palavras estão todas grudadas. Toque <b>entre as " +
            "letras</b>, onde uma acaba e a outra começa.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var G = GRUDA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", "Quantas palavras estão escondidas aqui?"));
    lin.appendChild(botaoSom("Ouvir as palavras", function(){ falar("gruda_" + k); }));
    box.appendChild(lin);
    var cortes = {}, soma = 0, j, lista = [];
    for(j = 0; j < G.p.length - 1; j++){ soma += G.p[j].length; cortes[soma] = 1; lista.push("c" + soma); }
    registra(id, pi, lista.join(" "));
    var faltam = G.p.length - 1, feitos = {};
    var cx = el("div", "grudada"), letras = G.p.join("").split("");
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
    resp.appendChild(nomeSecreto(G.certo, id));
    box.appendChild(resp);
    fechaItem(d, box, id);
  });
}

/* ============ 15 — O QUE É CADA UMA? ============
   Da d22, VERBATIM: *"3) Relacione cada substantivo composto à sua
   explicação."* — obra-prima, porta-malas, criado-mudo, desmancha-prazeres,
   bate-papo, com as explicações dela.
   ⭐ E ELA FECHA O BLOCO PELO SIGNIFICADO, que é o que faltava: a criança já
      sabe reconhecer duas palavras coladas; agora descobre que *criado-mudo*
      não é um criado nem é mudo — o composto ganha um sentido novo, que não é a
      soma dos dois. É a ideia mais difícil do bloco e vem por último. */
function f15(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque na <b>palavra</b> e depois no que ela <b>quer " +
            "dizer</b>.", "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: '<span class="rotop">' + SIGN[k].p + "</span>",
            dir: SIGN[k].s,
            ariaE: SIGN[k].p, ariaD: SIGN[k].s,
            fe: "sign_" + k, fd: "sigd_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 16 — DE ONDE SAIU ESSA PALAVRA? ============
   Do cartaz d26, que mostra lado a lado **dente → dentadura** e
   **chute → chuteira**, com a foto de cada um.
   ⭐ ABRE O BLOCO PELO PAR QUE SE VÊ. Antes de qualquer regra, a criança olha
      duas figuras e percebe que a segunda palavra tem a primeira dentro dela.
      É o problema antes do conceito, outra vez: as palavras "primitivo" e
      "derivado" não aparecem aqui — entram na folha 18.
   ⚠️ AS QUATRO FIGURAS SÃO AS DO CARTAZ, recortadas dele. */
function f16(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Olhe as duas figuras. Qual palavra <b>nasceu da outra</b>?",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PARDER[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var cx = el("div", "marcax fichas");
    [["a", P.a], ["b", P.b]].forEach(function(lado){
      var F = lado[1];
      cx.appendChild(el("div", "ficha vitrine",
        img(F.f, "figmini", F.alt) + '<span class="ft">' + F.n + "</span>"));
    });
    box.appendChild(cx);
    var lin = el("div", "chamlin");
    lin.appendChild(el("div", "enun", "Qual delas veio da outra?"));
    lin.appendChild(botaoSom("Ouvir as duas palavras", function(){ falar("pard_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id,
           [{v: "a", rot: P.a.n, aria: P.a.n, fala: "diz_" + chaveQuadro(P.a.n)},
            {v: "b", rot: P.b.n, aria: P.b.n, fala: "diz_" + chaveQuadro(P.b.n)}],
           "b", "pal", "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 17 — A MÁQUINA DE FAZER PALAVRAS ============
   Da d09, VERBATIM: *"01 Forme os substantivos derivados abaixo:"* — e a folha
   dela mostra o radical de um lado (sapat, pedr, fog) e três terminações do
   outro (aria / eiro / ilha), ligadas por riscos.
   ⭐ É AQUI QUE A FÁBRICA DO TÍTULO APARECE DE VERDADE: a criança pega um
      pedaço de palavra e encaixa uma terminação, e sai uma palavra nova que ela
      já conhecia sem saber de onde vinha. *Pedr* + *eiro* = quem trabalha com
      pedra.
   ⚠️ AS TERMINAÇÕES SÃO AS DA FOLHA DE PAPEL: -eiro (quem faz), -aria (o lugar
      onde se faz), -ada (um monte). Inventar outras aqui seria trocar o que foi
      usado em sala por um palpite meu. */
function f17(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escolha a terminação que forma a palavra que a frase pede.",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var M = MAQ[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", M.pede));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("maq_" + k); }));
    box.appendChild(lin);
    var mostra = el("div", "montada");
    mostra.setAttribute("data-feito", M.parte);
    mostra.appendChild(nomeSecreto(M.parte + M.r, id));
    box.appendChild(mostra);
    var lista = M.o.map(function(s){
      return {v: s, rot: "-" + s, aria: "Terminação " + s, fala: "sufixo_" + s};
    });
    opcoes(box, pi, id, lista, M.r, "curta",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k,
           function(){ mostra.setAttribute("data-feito", M.parte + M.r); });
    fechaItem(d, box, id);
  });
}

/* ============ 18 — LIGUE A PALAVRA-MÃE À PALAVRA-FILHA ============
   Da d01, VERBATIM: *"4-Ligue os substantivos primitivos com seus substantivos
   derivados."* — cadeira/cadeirante, vento/ventilador, gelo/gelado,
   agulha/agulhada, grama/gramado, caixa/caixote. São os pares dela.
   ⭐ E É AQUI QUE OS DOIS NOMES ENTRAM. Até a folha 17 a criança fez tudo sem
      ouvir "primitivo" e "derivado"; agora, com o gesto já na mão, o nome vem —
      e vem como rótulo das duas colunas, que é onde ele serve para alguma
      coisa. É a lei da casa: o conceito por último. */
function f18(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "À esquerda, a palavra que veio primeiro. À direita, a que " +
            "nasceu dela. Toque numa e depois na outra.", "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: '<span class="rotop">' + PRIM[k].p + "</span>",
            dir: PRIM[k].d,
            ariaE: PRIM[k].p, ariaD: PRIM[k].d,
            fe: "prim_" + k, fd: "deri_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 19 — AO CONTRÁRIO: DE QUAL PALAVRA ELA NASCEU? ============
   Da d22, VERBATIM: *"1) Complete o quadro com os substantivos primitivos."* —
   e a coluna preenchida é a dos DERIVADOS (goiabeira, pedreira, livraria,
   criançada, dentista); o que falta é a palavra-mãe.
   ⭐ ESTA FOLHA É O MESMO CONTEÚDO DE COSTAS. Na 17 e na 18 a criança ia da mãe
      para a filha; aqui ela vai da filha para a mãe, que é muito mais difícil e
      é o que prova que ela entendeu — reconhecer o radical dentro de uma palavra
      comprida é outra coisa que acertar a terminação.
   ⚠️ E É POR ISSO QUE ELA VEM COM TRÊS OPÇÕES PARECIDAS: *livraria* vem de
      LIVRO, não de LIVRE nem de LIVREIRO. Duas opções tornariam isto sorteio. */
function f19(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Esta palavra é filha de outra. <b>De qual</b> ela nasceu?",
            "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var V = VEIO[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "pgrande", V.d));
    lin.appendChild(botaoSom("Ouvir a palavra", function(){ falar("veio_" + k); }));
    box.appendChild(lin);
    var lista = V.o.map(function(w){
      return {v: chaveQuadro(w), rot: w, aria: w, fala: "diz_" + chaveQuadro(w)};
    });
    opcoes(box, pi, id, lista, chaveQuadro(V.r), "pal",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}

/* ============ 20 — DA MESMA FAMÍLIA, DA MESMA COR ============
   Da d12 (toda matéria), VERBATIM: *"Pinte o substantivo primitivo e seu(s)
   derivado(s) com a mesma cor."* — e a folha dela espalha as palavras soltas
   pela página, sem ordem nenhuma: FERRUGEM, TELHA, BICICLETA, SAPATEIRO, SOL,
   DENTE, SAPATO, DENTADURA, SAPATARIA, CASEIRO, JORNALISTA, JORNAL, FERRO,
   TELHADO, CASA, DENTISTA, BICICLETARIA, INSOLAÇÃO.
   ⭐ É O GESTO MAIS BONITO DO CADERNO e não aparece em nenhuma outra folha das
      trinta: a criança escolhe uma cor, pinta a palavra-mãe e sai caçando as
      filhas dela na bagunça. A família de palavras deixa de ser uma lista e
      vira um grupo que ela mesma juntou.
   ⚠️ A COR É DECLARADA NO `conteudo`, não sorteada: o `_qa/cor_fixa.py` reprova
      cor que muda entre uma abertura e outra — a criança que volta depois do
      recreio tem de reencontrar a família dela da mesma cor.
   ⚠️ E O PINCEL TEM DOIS TOQUES: primeiro a criança escolhe a cor (a família),
      depois toca nas palavras. Sem isso ela pinta tudo da primeira cor sem
      decidir nada, e a folha fecharia sem medir. */
function f20(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escolha uma <b>cor</b> e pinte a palavra-mãe e as filhas " +
            "dela. Depois pegue outra cor.", "p" + pi + "enun");
  /* ⚠️⚠️ UMA POSIÇÃO DO POTE POR PALAVRA, e não por família — defeito medido em
     15/set/2026 e que NENHUM portão pegava. O pote trazia as cinco famílias e a
     folha registrava CATORZE ids (um por palavra). Como o `idsDaPagina` conta
     pelo tamanho do pote, `pendentes()` achava que a folha tinha cinco itens:
     pintadas cinco palavras, a folha se dava por PRONTA e pulava para a
     seguinte com nove palavras ainda por pintar no mural — e o relatório
     contava cinco de catorze. O jogador da banca não via (ele resolve pelo que
     está declarado e tudo fechava); quem viu foi comparar o andarilho, que
     conta os itens de verdade, com o jogador.
     É a regra "A POSIÇÃO É A IDENTIDADE" cobrando de novo: o pote é a fonte do
     número de itens, então cada item precisa de uma posição nele. */
  var pool = ST.folha["p" + pi], fams = [], ativa = null, botoes = {};
  pool.forEach(function(par){
    var fk = par.split("|")[0];
    if(fams.indexOf(fk) < 0) fams.push(fk);
  });
  var paleta = el("div", "ops lapis");
  fams.forEach(function(fk){
    var F = FAM[fk];
    var b = el("button", "op curta lapiz", F.n);
    b.style.background = F.cor; b.style.borderColor = F.cor;
    b.setAttribute("aria-label", "Pintar a família de " + F.n);
    /* ⚠️ O CONTRATO DO JOGADOR DA BANCA (`_qa/joga_folha.js`, família "pintar por
       legenda") é: a PEÇA publica `pinta-<id>-<x>` e carrega `data-lapis="<x>"`,
       e o estojo publica `lapis-<x>`. Eu tinha posto o `data-lapis` no lápis e
       com o valor da COR — o jogador procurava `lapis-#f0b429`, não achava, e
       dizia "não sei jogar esta peça", o que deixa a folha sem medida nenhuma. */
    b.setAttribute("data-qa", "lapis-" + fk);
    b.onclick = function(){
      sPasso(); falar("fam_" + fk);
      if(ativa) botoes[ativa].className = "op curta lapiz";
      ativa = fk; b.className = "op curta lapiz marcada";
    };
    botoes[fk] = b; paleta.appendChild(b);
  });
  d.appendChild(paleta);
  var mural = el("div", "espalhadas"), todas = [];
  pool.forEach(function(par, i){
    var p = par.split("|");
    todas.push({fk: p[0], w: p[1], id: "n" + pi + "_" + i});
  });
  baralha(todas.slice(0)).forEach(function(P){
    registra(P.id, pi, "pinta-" + P.fk);
    var b = el("button", "pal solta", P.w);
    b.setAttribute("aria-label", P.w);
    b.setAttribute("data-qa", "pinta-" + P.id + "-" + P.fk);
    b.setAttribute("data-lapis", P.fk);
    if(ST.resp[P.id]){ b.style.background = FAM[P.fk].cor; b.className = "pal solta pintada"; }
    b.onclick = function(){
      if(ST.resp[P.id]) return;
      sPasso();
      if(!ativa){ falar("toque_cor"); return; }
      if(ativa === P.fk){
        b.style.background = FAM[P.fk].cor; b.className = "pal solta pintada";
        falar("diz_" + chaveQuadro(P.w));
        acertou(P.id, "certo" + pi + "_" + P.fk);
      } else {
        b.className = "pal solta nao";
        setTimeout(function(){ b.className = "pal solta"; }, 420);
        errou(P.id, "dica" + pi + "_" + P.fk);
      }
    };
    mural.appendChild(b);
  });
  d.appendChild(mural);
}

/* ============ 21 — DUAS MARCAS NA MESMA FRASE ============
   Da d21 (Cantinho Ensinar), VERBATIM: *"1 - CIRCULE , NAS FRASES, OS
   SUBSTANTIVOS PRIMITIVOS E SUBLINHE OS SUBSTANTIVOS DERIVADOS:"* — com as
   frases dela: *"O rapaz comprou um livro naquela livraria do centro da
   cidade."*, *"Tomamos sorvete na sorveteria da Maria."*, *"Peguei uma flor na
   floricultura da Dona Rosa."*
   ⭐ É O DEGRAU MAIS ALTO DO BLOCO, e o comando do papel já sabia disso: são
      DUAS decisões na mesma frase, e as duas palavras estão coladas uma na
      outra (*livro* e *livraria* na mesma linha). A criança não pode ir no
      automático.
   ⚠️ SÃO DOIS TOQUES, e tem de ser: primeiro ela escolhe a marca (mãe ou
      filha), depois toca na palavra. Se bastasse tocar, ela fecharia a folha a
      esmo — foi o defeito que o ditado da Loteria do S pagou. */
function f21(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Escolha a marca e toque na palavra: a que veio " +
            "<b>primeiro</b>, ou a que <b>nasceu dela</b>.", "p" + pi + "enun");
  var marca = null, bm = {};
  var barra = el("div", "ops lapis");
  [["p", "a que veio primeiro"], ["d", "a que nasceu dela"]].forEach(function(m){
    var b = el("button", "op curta lapiz marca" + m[0], m[1]);
    b.setAttribute("aria-label", m[1]);
    /* mesmo contrato da folha 20: o estojo publica `lapis-<x>` e a peça carrega
       `data-lapis="<x>"`. Ver o comentário lá, que conta o que custou. */
    b.setAttribute("data-qa", "lapis-" + m[0]);
    b.onclick = function(){
      sPasso(); falar("marca_" + m[0]);
      if(marca) bm[marca].className = "op curta lapiz marca" + marca;
      marca = m[0]; b.className = "op curta lapiz marca" + m[0] + " marcada";
    };
    bm[m[0]] = b; barra.appendChild(b);
  });
  d.appendChild(barra);
  /* ⚠️ DUAS POSIÇÕES DO POTE POR FRASE (`livro|p` e `livro|d`), porque a criança
     faz DUAS decisões em cada uma. Com uma posição por frase, a folha se daria
     por pronta com metade das palavras marcadas — o mesmo defeito que a folha
     20 pagou, e pela mesma razão: quem conta os itens é o tamanho do pote. */
  var pool = ST.folha["p" + pi], porFrase = {}, ordem = [];
  pool.forEach(function(par, i){
    var p = par.split("|");
    if(!porFrase[p[0]]){ porFrase[p[0]] = {}; ordem.push(p[0]); }
    porFrase[p[0]][p[1]] = "n" + pi + "_" + i;
    registra("n" + pi + "_" + i, pi, "pinta-" + p[1]);
  });
  ordem.forEach(function(k, i){
    var F = DUPLA[k], box = item(i + 1), ids = porFrase[k];
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Nesta frase há as duas."));
    lin.appendChild(botaoSom("Ouvir a frase", function(){ falar("dupla_" + k); }));
    box.appendChild(lin);
    var cx = el("div", "textinho");
    F.palavras.forEach(function(w, n){
      var pura = chaveQuadro(w);
      var qual = pura === chaveQuadro(F.prim) ? "p"
               : pura === chaveQuadro(F.deri) ? "d" : null;
      var id = qual ? ids[qual] : null;
      var b = el("button", "tp", w);
      b.setAttribute("aria-label", w);
      if(id){
        b.setAttribute("data-qa", "pinta-" + id + "-" + qual);
        b.setAttribute("data-lapis", qual);
        if(ST.resp[id]) b.className = "tp marca" + qual;
      }
      b.onclick = function(){
        if(id && ST.resp[id]) return;
        sPasso();
        if(!marca){ falar("toque_marca"); return; }
        if(qual === marca){
          b.className = "tp marca" + qual;
          acertou(id, "certo" + pi + "_" + k + "_" + qual);
        } else {
          b.className = "tp nao";
          setTimeout(function(){ b.className = "tp"; }, 420);
          errou(ids[marca], "dica" + pi + "_" + k);
        }
      };
      cx.appendChild(b);
      cx.appendChild(document.createTextNode(" "));
    });
    box.appendChild(cx);
    d.appendChild(box);
  });
}

/* ============ 22 — A PALAVRA INTRUSA ============
   Da d19, VERBATIM: *"2. Descubra a palavra intrusa em cada grupo e justifique
   a sua resposta."* — e os grupos dela: *girassol · vaivém · planalto · chuva*;
   *sobremesa · escova · pente · sabonete*; *água-viva · cachorro · olho de
   sogra · varapau*.
   ⭐ É A FOLHA DE REVISÃO DO CADERNO INTEIRO, e é a única em que a criança não
      classifica: ela COMPARA. Para achar a intrusa, ela precisa descobrir
      sozinha qual é a regra do grupo — três são compostas e uma não é. Isso é
      um degrau acima de tudo o que veio antes, e é por isso que ela fecha os
      blocos de gramática.
   ⚠️ O "justifique" do papel é texto livre, que a tela não corrige. O que a
      tela faz é dar o PORQUÊ escrito depois do acerto, para a criança conferir
      o raciocínio dela — e o dossiê avisa o professor de que a justificativa
      falada acontece na roda, não aqui. */
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Três destas palavras combinam entre si e <b>uma</b> não. " +
            "Ache a intrusa.", "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var I = INTRUSA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "ajuda", "Qual não combina com as outras três?"));
    lin.appendChild(botaoSom("Ouvir as quatro palavras", function(){ falar("intr_" + k); }));
    box.appendChild(lin);
    var lista = I.g.map(function(w){
      return {v: chaveQuadro(w), rot: w, aria: w, fala: "diz_" + chaveQuadro(w)};
    });
    opcoes(box, pi, id, baralha(lista), chaveQuadro(I.r), "pal",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k,
           function(){ var a = el("div", "ajuda"); a.appendChild(nomeSecreto(I.pq, id)); box.appendChild(a); });
    fechaItem(d, box, id);
  });
}

/* ============ 23 — UM NOME PARA MUITOS ============
   Da d06, cujo cartaz traz a definição VERBATIM — *"Substantivo coletivo é
   aquele que indica um grupo ou uma coleção de seres da mesma espécie"* — e uma
   tabela de cinquenta.
   ⭐ E AQUI ELE É UM PROBLEMA, NÃO UMA LISTA PARA DECORAR. As duas folhas de
      coletivo que vieram na colheita (d06 e d10) são tabelas gigantes, e uma
      criança de 5º ano não decora cinquenta palavras — ela entende a IDEIA: uma
      palavra no singular que nomeia muitos. Por isso a folha dá o GRUPO e pede
      a palavra, com oito dos coletivos que realmente aparecem na vida dela.
   ⚠️ E OS PARES SÃO OS DA d06, QUE ESTÁ CERTA. A d13 também traz coletivos, mas
      escreve *"CHAVES= PENCA"* (penca é de bananas; de chaves é MOLHO) e
      *"CLASSE= ALUNOS"*, que está de cabeça para baixo. Está recusada no POTE,
      com o motivo — usar a tabela dela ensinaria errado. */
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cada grupo tem um nome só. Toque no <b>grupo</b> e depois " +
            "no <b>nome</b> dele.", "p" + pi + "enun");
  var grupo = ST.folha["p" + pi][0];
  var pares = grupo.map(function(k){
    return {k: k, w: k, wd: k,
            esq: '<span class="rotop">' + COLE[k].g + "</span>",
            dir: COLE[k].c,
            ariaE: COLE[k].g, ariaD: COLE[k].c,
            fe: "grupo_" + k, fd: "cole_" + k,
            fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  });
  var cx = el("div", "");
  montaLigar(cx, pi, "g0", pares, d);
  d.appendChild(cx);
}

/* ============ 24 — O SÍTIO DO LOURENÇO ============
   Da d24, e esta folha é quase inteira dela. O texto *"Lourenço, Paçoca e
   Fumaça"* vem VERBATIM, e as perguntas também: *"1 – Paçoca é substantivo
   comum ou próprio? Por quê?"*, *"2 – Escreva três substantivos próprios."*,
   *"3 – Escreva três substantivos comuns."*
   ⭐ É O FECHO DE CONTEÚDO DO CADERNO, e ele existe porque a professora pediu
      **"leitura e interpretação de textos"** junto com a ortografia e a
      gramática. Das trinta folhas colhidas, esta é a ÚNICA com um texto de
      verdade — as outras vinte e nove tratam substantivo como palavra solta
      numa lista. E é no texto que o substantivo de fato vive.
   ⭐ E A PRIMEIRA PERGUNTA É A MELHOR DA COLHEITA: *Paçoca é comum ou próprio?*
      Paçoca é um doce (comum) E é o nome do porco do Lourenço (próprio) — a
      resposta depende de quem está falando, não da palavra. É a folha inteira
      numa pergunta só.
   ⚠️ O "escreva três" é texto livre. A tela faz a criança ACHAR no texto, que é
      a mesma leitura por outro gesto; o escrever fica no papel, e o dossiê do
      professor diz isso. */
function f24(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  /* ⚠️ O POTE TRAZ UMA POSIÇÃO POR PERGUNTA (`q0`…`q4`), não o nome do texto.
     Com uma posição só, a folha registrava cinco ids e o `idsDaPagina` contava
     UM: respondida a primeira pergunta, a folha se dava por pronta e pulava com
     quatro ainda na tela — e o relatório contava um de cinco. O texto é fixo;
     quem varia é a pergunta. */
  var T = TEXTO.lourenco, pool = ST.folha["p" + pi];
  var cab = el("div", "enunlin");
  cab.appendChild(el("div", "ajuda", T.titulo));
  cab.appendChild(botaoSom("Ouvir a história", function(){ falar("hist_" + T.k); }));
  d.appendChild(cab);
  d.appendChild(el("div", "textao", T.corpo));
  enunciado(d, pi, "Agora responda sobre a história.", "p" + pi + "enun");
  pool.forEach(function(qk, i){
    var P = T.perg[parseInt(qk.slice(1), 10)];
    if(!P) return;
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "enun", P.q));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("perg_" + T.k + "_" + i); }));
    box.appendChild(lin);
    var lista = P.o.map(function(w, j){
      return {v: "o" + j, rot: w, aria: w, fala: "resp_" + T.k + "_" + i + "_" + j};
    });
    opcoes(box, pi, id, lista, "o" + P.r, "pal",
           "certo" + pi + "_" + i, "dica" + pi + "_" + i,
           P.pq ? function(){ var a2 = el("div", "ajuda"); a2.appendChild(nomeSecreto(P.pq, id)); box.appendChild(a2); } : null);
    fechaItem(d, box, id);
  });
}

/* ============ 25 — O CARTAZ QUE EU LEVO (o fecho com gancho) ============
   ⚠️ O FECHO DAS FOLHAS DE ORIGEM é *"escreva uma frase com"* e *"crie, no
      caderno, um texto"* (d17 e d18) — produção livre, que a tela não corrige.
      O que a tela sabe fazer é a criança MONTAR o cartaz dela: toca na regra, a
      regra entra no cartaz com um exemplo, e o cartaz cresce embaixo.
   ⭐ É O "QUERO MAIS": ela sai daqui com um lembrete que é DELA, para colar no
      caderno de papel — e é justamente ali, no papel, que a escrita de frases
      que a tela não mede vai acontecer. O dossiê diz isso ao professor.
   ⚠️ AQUI NÃO HÁ RESPOSTA CERTA NEM ERRADA. A criança escolhe as regras que ela
      quer levar, e o portão do "beco sem saída" precisa disso declarado: toda
      peça é alvo. */
function f25(d, pi){
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
  if(mesmaPalavra(CRUZ.val, E.w, E.exigeAcento)){
    E.cels.forEach(function(c, i){
      if(!c) return;
      var n = c.querySelector(".cn");
      c.textContent = E.w.charAt(i); if(n) c.appendChild(n);
      c.className = "ccel viva ok";
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
    est += '<img src="img/sb_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  {n: "Distinguir o nome que serve para muitos do nome de um só", f: [1, 2, 3, 4, 5],
   ok: "separa o nome que serve para muitos do nome que é de um só",
   nao: "ainda mistura o nome da espécie com o nome de batismo"},
  {n: "Escrever com letra maiúscula o nome que é de um só", f: [6, 7, 8, 9],
   ok: "usa letra grande no nome de um só e letra pequena nos outros",
   nao: "ainda põe letra grande em nome comum, ou esquece no nome próprio"},
  {n: "Diferenciar palavra simples de palavra composta", f: [10, 11, 12, 13, 14, 15],
   ok: "percebe quando há duas palavras dentro de uma, e quando leva traço",
   nao: "ainda lê a palavra composta como se fosse uma palavra só qualquer"},
  {n: "Reconhecer a palavra primitiva e a que nasceu dela", f: [16, 17, 18, 19, 20, 21, 22],
   ok: "acha a palavra-mãe dentro da palavra comprida e junta a família",
   nao: "ainda não enxerga a palavra menor escondida dentro da maior"},
  {n: "Nomear com uma palavra só um grupo inteiro", f: [23],
   ok: "usa uma palavra no singular para nomear muitos da mesma espécie",
   nao: "ainda não liga o grupo à palavra que o nomeia"},
  {n: "Achar e classificar os substantivos dentro de um texto lido", f: [24, 25],
   ok: "lê o texto e acha nele os substantivos, dizendo de que tipo são",
   nao: "classifica a palavra sozinha, mas se perde quando ela está no texto"}
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
