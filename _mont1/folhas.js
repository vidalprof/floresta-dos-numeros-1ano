/* ============================================================
   A MÁQUINA DE JUNTAR PALAVRAS — a casa das dez folhas.

   Aqui moram as peças que TODAS as folhas usam (o alto-falante, a fileira de
   opções, o arrastar, o ligar, o teclado) e, mais abaixo, as dez folhas.
   O catálogo dos verbos de folha impressa é o `_padrao/INTERATIVIDADES-FOLHA.md`.

   ⚠️ ESTE ARQUIVO NASCEU CLONADO do Bate-Palma (degrau 2). Tudo o que era
   CONTEÚDO de lá — as opções de número, o estojo de canetinhas, o rabisco de
   circular, a fila do alfabeto — foi ARRANCADO, não deixado inerte: código
   morto de outro caderno não dá erro nenhum, e é exatamente por isso que ele
   sobrevive de clone em clone até alguém achar que faz parte.
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
  var c = el("div", "capa"), nome = "A MÁQUINA DE JUNTAR PALAVRAS", k = 0, letras = "";
  /* ⚠️ uma PALAVRA por bloco: o título entra letra a letra, e sem isto o
     navegador quebra a linha no meio de "PALAVRAS" (visto no contato-folha) */
  nome.split(" ").forEach(function(pal, pi2){
    if(pi2) letras += '<span class="esp"></span>';
    letras += '<span class="pv">';
    for(var j = 0; j < pal.length; j++, k++)
      letras += '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + pal.charAt(j) + '</span>';
    letras += '</span>';
  });
  /* ⭐ A CENA CONTA A ATIVIDADE, e ela é o contrário da capa do Bate-Palma: lá
     a palavra se PARTIA em pedaços; aqui os pedaços correm um para o outro e
     viram palavra. BO + LA = BOLA, na esteira da oficina. */
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Alfabetização &middot; 1º ano &middot; dez folhas de juntar pedaços</div>' +
    '<div class="esteira">' +
      '<div class="cena cenajunta">' +
        '<span class="pedcapa pj1">BO</span>' +
        '<span class="maiscapa">+</span>' +
        '<span class="pedcapa pj2">LA</span>' +
        '<span class="igualcapa">=</span>' +
        '<span class="palcapa">BOLA</span>' +
      "</div>" +
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

/* a fileira de pedaços da palavra, um por sílaba — a peça que se repete.
   ⚠️ ALTO-FALANTE EM TODA PALAVRA: sem ouvir, a criança que ainda não lê conta
   as sílabas do que ELA acha que a figura é ("cachorro" ou "cão"?), e a folha
   vira loteria. A figura tem que ter um nome só, e a voz é quem o diz. */
/* ⚠️⚠️ A LEGENDA DA FIGURA ENTREGAVA A RESPOSTA — set/2026, e estava NO AR.
   Achado por um portão novo (`_qa/resposta_impressa.py`), que nasceu quando a
   mesma coisa apareceu numa foto da Roda das Sílabas: a figura da mola vinha
   com "MOLA" escrito por baixo e, logo abaixo, os quadradinhos para a criança
   escrever MO. Quem lê um pouco resolvia COPIANDO.

   Aqui o portão encontrou o mesmo, em quatro cadernos de uma vez — sendo o pior
   deles uma FORCA com a palavra impressa na tela.

   ⚠️ A legenda não some: fica INVISÍVEL (`visibility`, para o espaço não pular)
      e aparece no instante do acerto. Assim a criança que chama a luneta de
      "telescópio" continua protegida — pelo alto-falante antes, pela palavra
      escrita depois, que é o melhor momento para ela aparecer. */
function figComSom(w, cls, id){
  var c = el("div", "figsil" + (cls ? " " + cls : ""));
  c.innerHTML = img(w, "figgrande");
  var lin = el("div", "chamlin");
  if(id){
    var b = el("b", "segredo" + (ST.resp[id] ? " revelado" : ""), esc(w));
    b.setAttribute("data-nome", id);
    lin.appendChild(b);
  } else lin.appendChild(el("b", "", esc(w)));
  lin.appendChild(botaoSom("Ouvir " + esc(w), function(){ falar("pal_" + w); }));
  c.appendChild(lin);
  return c;
}
/* ============================================================
   AS DEZ FOLHAS DA MÁQUINA — degrau 5 da sequência de alfabetização.

   ⭐ O QUE MUDA DO DEGRAU 2 PARA CÁ. No Bate-Palma a criança PARTIA a palavra
   (análise): ouvia BO-LA e dizia "duas palmas". Aqui ela faz o caminho de
   volta — recebe os pedaços SOLTOS e tem que JUNTAR (síntese). É o gesto que
   está por baixo da leitura: quem lê BOLA está juntando BO com LA na cabeça,
   depressa. Sem este degrau, a criança soletra a vida inteira.

   ⚠️ E É POR ISSO QUE A VOZ MANDA AQUI. Juntar pedaços é operação de OUVIDO.
   Toda peça deste caderno fala o pedaço RECORTADO da palavra inteira
   (`falarSilaba` / `falarPedacos`) — nunca a sílaba lida solta pelo
   sintetizador, que soletra "vê-á" no lugar de VA. O portão `_qa/silabas.py`
   não deixa publicar sem os recortes.
   ============================================================ */

/* ---------- os pedaços DISTRATORES, declarados um a um ----------
   ⚠️ NADA DE SORTEIO. Sorteando o pedaço errado, mais cedo ou mais tarde cai um
   que TAMBÉM serve (LA em PANELA, TA em BOTA) e a criança leva um "errou" numa
   resposta que estava certa. Cada distrator abaixo foi conferido contra a
   palavra da linha. */
var SOBRA = {"boneca": "TO", "panela": "CO", "banana": "TE", "tomate": "LU",
             "sapato": "NE", "cavalo": "PI", "macaco": "NE", "girafa": "TO",
             "coruja": "PA", "janela": "BO"};

/* ---------- o botão de um pedaço ----------
   O pedaço é botão de verdade (fala quando tocado) e alvo grande: no 1º ano o
   dedo é gordo e a peça pequena tira a criança da tarefa e a põe na mira. */
function pedaco(s, w, k, cls){
  var b = el("button", "sil" + (cls ? " " + cls : ""), esc(s));
  b.setAttribute("aria-label", "pedaço " + s + (w ? " de " + esc(w) : ""));
  return b;
}
/* 1 — JUNTE OS DOIS PEDAÇOS (a folha que ENSINA, não a que mede)
   ⭐ Aqui não há pergunta nenhuma nas primeiras vezes: a criança toca no
   primeiro pedaço e ouve BO, toca no segundo e ouve LA, e então aperta JUNTAR —
   as duas peças correm uma para a outra, viram uma palavra só e a voz diz BOLA.
   É a demonstração física do que "juntar" quer dizer, e é dela que saem as
   outras nove folhas.
   ⚠️ NA ORDEM: tocar no segundo antes do primeiro não acende. Juntar pedaços é
   uma operação com ORDEM — LA-BO não é BOLA, e a criança precisa sentir isso na
   mão antes de ouvir na regra. */
function f1(d, pi){
  faixa(d, pi, NOMES[0]);
  enunciado(d, pi, "Toque no <b>primeiro</b> pedaço, depois no <b>segundo</b>. Aí aperte <b>JUNTAR</b>.", "p1enun");
  var L = ST.folha.p1;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "o1_" + i, box = item(i + 1), ss = sil(w), pronto = !!ST.resp[id];
      registra(id, pi, ss.join("-"));
      box.appendChild(figComSom(w, null, id));
      var of = el("div", "oficina" + (pronto ? " junta" : "")), posto = 0;
      var fila = el("div", "pedfila");
      ss.forEach(function(s, k){
        if(k) fila.appendChild(el("span", "mais", "+"));
        var b = pedaco(s, w, k, pronto ? "acesa" : "");
        b.setAttribute("data-qa", "ped-" + id + "-" + k);
        b.onclick = function(){
          if(ST.resp[id]) return;
          if(k !== posto){
            sErro(); b.className = "sil fora";
            setTimeout(function(){ b.className = "sil"; }, 460);
            errou(id, "volte1_" + w); return;
          }
          sPasso(); falarSilaba(w, k, s);
          b.className = "sil acesa"; posto++;
          if(posto === ss.length) jt.className = "bt verde juntar liberado";
        };
        fila.appendChild(b);
      });
      of.appendChild(fila);
      var alvo = el("div", "palmontada" + (pronto ? " cheia" : ""), pronto ? esc(w) : "");
      alvo.setAttribute("data-qa", "montada-" + id);
      var jt = el("button", "bt verde juntar" + (pronto ? " sumiu" : ""), "JUNTAR");
      jt.setAttribute("data-qa", "juntar-" + id);
      jt.onclick = function(){
        if(ST.resp[id]) return;
        if(posto < ss.length){
          sErro(); errou(id, "volte1_" + w); return;
        }
        sPasso(); of.className = "oficina junta";
        alvo.className = "palmontada cheia"; alvo.textContent = esc(w);
        jt.className = "bt verde juntar sumiu";
        falar("pal_" + w);
        setTimeout(function(){ acertou(id, "certo1_" + w); }, 900);
      };
      of.appendChild(jt); of.appendChild(alvo);
      box.appendChild(of);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 2 — QUAL PEDAÇO FALTA NO FIM (e 3, o começo — as duas em BLOCO)
   ⚠️ AS DUAS SEGUIDAS, DE PROPÓSITO. Regra do Marcos (ago/2026): mecânica que
   repete vem colada e subindo um degrau, nunca espalhada pelo caderno — espaçada
   a criança sente que voltou. Aqui o degrau é o LUGAR do buraco: primeiro no
   fim (o pedaço que falta vem depois do que ela já ouviu, que é mais fácil),
   depois no começo (ela tem que segurar o fim na cabeça e procurar o que vem
   ANTES, que é o gesto da leitura de verdade). */
function f2(d, pi){ buracoNoPedaco(d, pi, "o2_", ST.folha.p2, 1, "p2enun",
  "Ouça a palavra. Qual pedaço falta no <b>fim</b>?"); }
function f3(d, pi){ buracoNoPedaco(d, pi, "o3_", ST.folha.p3, 0, "p3enun",
  "Agora o buraco muda de lugar: o <b>começo</b> &mdash; e, no fim da folha, o <b>meio</b>."); }

function buracoNoPedaco(d, pi, tag, L, qual, chaveEnun, texto){
  faixa(d, pi, NOMES[tag === "o2_" ? 1 : 2]);
  enunciado(d, pi, texto, chaveEnun);
  for(var i = 0; i < L.length; i++){
    (function(reg, i){
      var w = reg[0], id = tag + i, box = item(i + 1), ss = sil(w);
      /* ⚠️ O LUGAR DO BURACO PODE VIR DECLARADO NO PRÓPRIO ITEM (4º campo). É
         assim que o pedaço do MEIO entra no fim da folha 3 sem uma folha nova:
         `["cavalo","TO","PI",1]` = CA + [?] + LO. Sem o campo, vale o lugar
         padrão da folha. */
      var onde = (typeof reg[3] === "number") ? reg[3] : qual;
      var certa = ss[onde];
      box.appendChild(figComSom(w, null, id));
      /* a palavra com o buraco: o pedaço que ela JÁ tem, e o quadrado vazio */
      var lin = el("div", "pedfila"), k;
      for(k = 0; k < ss.length; k++){
        if(k) lin.appendChild(el("span", "mais", "+"));
        if(k === onde) lin.appendChild(el("span", "vagaped", "?"));
        else {
          (function(k){
            var b = pedaco(ss[k], w, k, "dada");
            b.onclick = function(){ sPasso(); falarSilaba(w, k, ss[k]); };
            lin.appendChild(b);
          })(k);
        }
      }
      box.appendChild(lin);
      var ops = [certa, reg[1], reg[2]];
      /* a resposta certa não fica sempre no mesmo lugar */
      var gira = i % 3;
      ops = ops.slice(gira).concat(ops.slice(0, gira));
      opcoes(box, pi, id, ops.map(function(s){
        return {v: s, rot: '<span class="ltop">' + esc(s) + "</span>",
                aria: "pedaço " + s, fala: "sb1_" + s};
      }), certa, "figbt", "certo" + (tag === "o2_" ? 2 : 3) + "_" + w,
         "dica" + (tag === "o2_" ? 2 : 3) + "_" + w);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 4 e 5 — PONHA OS PEDAÇOS NA ORDEM (o bloco do arrastar)
   No papel a criança recorta os pedaços e cola nas linhas. Aqui eles vêm
   EMBARALHADOS e ela os põe no lugar — puxando ou tocando, as duas portas.
   ⚠️ A folha 5 sobe o degrau de dois jeitos ao mesmo tempo: são TRÊS pedaços em
   vez de dois, e um deles SOBRA (é de outra palavra). Sem o pedaço que sobra a
   criança acerta por eliminação na última vaga e não escuta nada. */
function f4(d, pi){ montaOrdem(d, pi, "o4_", ST.folha.p4, false, 3, "p4enun",
  "Os pedaços saíram fora de ordem. <b>Ponha cada um no seu lugar.</b>"); }
function f5(d, pi){ montaOrdem(d, pi, "o5_", ST.folha.p5, true, 4, "p5enun",
  "Agora são três pedaços &mdash; e <b>um deles sobra</b>. Monte a palavra da figura."); }

function montaOrdem(d, pi, tag, L, comSobra, nome, chaveEnun, texto){
  faixa(d, pi, NOMES[nome]);
  enunciado(d, pi, texto, chaveEnun);
  var n = tag === "o4_" ? 4 : 5;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = tag + i, box = item(i + 1), ss = sil(w), pronto = !!ST.resp[id];
      registra(id, pi, ss.join("-"));
      box.appendChild(figComSom(w, null, id));
      var trilha = el("div", "vagas"), vagas = [], k;
      for(k = 0; k < ss.length; k++){
        var v = el("div", "vaga" + (pronto ? " ok" : ""), pronto ? esc(ss[k]) : "");
        trilha.appendChild(v); vagas.push(v);
      }
      box.appendChild(trilha);
      /* o banco vai em ordem FIXA (nada de sorteio: o portão do jogador precisa
         de resultado estável, e para a criança embaralhado é embaralhado) — mas
         nunca na ordem da palavra: o primeiro pedaço vai para o fim da fila */
      var lista = ss.slice(0);
      if(comSobra) lista.push(SOBRA[w] || "TA");
      lista = lista.slice(1).concat([lista[0]]);
      var banco = el("div", "silbanco"), posto = 0;
      lista.forEach(function(s, j){
        var b = pedaco(s, null, j, pronto ? "usada" : "");
        b.setAttribute("data-qa", "sil-" + id + "-" + j);
        function poe(){
          if(ST.resp[id] || b.className.indexOf("usada") > -1) return;
          if(s !== ss[posto]){
            sErro(); b.className = "sil erro";
            setTimeout(function(){ b.className = "sil"; }, 460);
            errou(id, "dica" + n + "_" + w); return;
          }
          sPasso(); falarSilaba(w, posto, s);
          vagas[posto].className = "vaga ok"; vagas[posto].textContent = esc(s);
          b.className = "sil usada"; posto++;
          if(posto === ss.length) setTimeout(function(){ acertou(id, "certo" + n + "_" + w); }, 560);
        }
        b.onclick = function(){ if(b._arrastou){ b._arrastou = false; return; } poe(); };
        puxavel(b, vagas, poe);
        banco.appendChild(b);
      });
      box.appendChild(banco);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 6 — QUE PALAVRA É ESTA? ⭐ A FOLHA QUE SÓ EXISTE COM VOZ
   Nenhuma folha de papel consegue fazer isto: os pedaços chegam SÓ pelo ouvido
   — não há palavra escrita, não há figura da resposta em destaque — e a criança
   junta na cabeça e aponta a figura. É a síntese silábica pura, o coração do
   degrau, e é aqui que se vê quem já lê com o ouvido.
   ⚠️ A ESCADA ESTÁ NA ORDEM DAS LINHAS: começa com três figuras que não se
   parecem em nada (GATO, SAPO, VELA) e termina com três que começam igual
   (BOLA, BOTA, BOLO) — aí de nada adianta ouvir só o primeiro pedaço. */
function f6(d, pi){
  faixa(d, pi, NOMES[5]);
  enunciado(d, pi, "Aperte o alto-falante e <b>escute os pedaços</b>. Que palavra eles formam?", "p6enun");
  var L = ST.folha.p6;
  for(var i = 0; i < L.length; i++){
    (function(reg, i){
      var w = reg[0], id = "o6_" + i, box = item(i + 1);
      var ouvir = el("button", "bt azul ouvirped", "Escutar os pedaços");
      ouvir.setAttribute("data-qa", "ouvir-" + id);
      ouvir.onclick = function(){ sPasso(); falarPedacos(w); };
      box.appendChild(ouvir);
      var ops = reg.slice(0).map(function(x){
        return {v: x, rot: img(x, "figop") + '<span class="rotop">' + esc(x) + "</span>",
                aria: esc(x), fala: "pal_" + x};
      });
      var gira = i % 3;
      ops = ops.slice(gira).concat(ops.slice(0, gira));
      opcoes(box, pi, id, ops, w, "fig", "certo6_" + w, "dica6_" + w);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 7 — LIGUE A FIGURA AOS SEUS PEDAÇOS (o degrau da carga)
   Três de uma vez: em vez de responder uma pergunta por vez, ela precisa
   segurar três palavras na cabeça e decidir qual vai com qual. Mesmo conteúdo,
   carga maior — e é a primeira folha em que ela vê a palavra ESCRITA em pedaços
   (BA·NA·NA), que é a ponte para a folha 9. */
function f7(d, pi){
  faixa(d, pi, NOMES[6]);
  enunciado(d, pi, "<b>Ligue</b> cada figura aos pedaços que formam o nome dela.", "p7enun");
  var L = ST.folha.p7;
  for(var i = 0; i < L.length; i++){
    var g = L[i], cx = el("div", "");
    montaLigar(cx, pi, "o7g" + i, g.map(function(w){
      return {k: w, w: esc(w), wd: sil(w).join("-"),
              esq: img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>",
              dir: '<span class="pedgrande">' + sil(w).join("·") + "</span>",
              fe: "pal_" + w, fd: "pal_" + w,
              fc: "certo7_" + w, dica: "dica7_" + w};
    }), d);
    d.appendChild(cx);
  }
}

/* 8 — AS DUAS PALAVRAS ⭐ A FOLHA QUE NENHUMA DAS 24 TINHA
   As duas começam com o MESMO pedaço: BO-LA e BO-LO. Quem decide pelo começo
   erra metade das vezes — e é esse erro que a folha quer provocar, porque é
   exatamente ele que faz a criança leitora trocar CASA por CAMA a vida inteira.
   Só quem escuta até o FIM acerta. */
function f8(d, pi){
  faixa(d, pi, NOMES[7]);
  enunciado(d, pi, "As duas começam igual! Escute <b>até o fim</b> e toque na certa.", "p8enun");
  var L = ST.folha.p8;
  for(var i = 0; i < L.length; i++){
    (function(par, i){
      var w = par[0], outra = par[1], id = "o8_" + i, box = item(i + 1);
      var ouvir = el("button", "bt azul ouvirped", "Escutar os pedaços");
      ouvir.setAttribute("data-qa", "ouvir-" + id);
      ouvir.onclick = function(){ sPasso(); falarPedacos(w); };
      box.appendChild(ouvir);
      var ops = [w, outra];
      if(i % 2) ops = [outra, w];
      opcoes(box, pi, id, ops.map(function(x){
        return {v: x, rot: img(x, "figop") + '<span class="rotop">' + esc(x) + "</span>",
                aria: esc(x), fala: "pal_" + x};
      }), w, "fig", "certo8_" + w, "dica8_" + w);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 9 — ESCREVA O PEDAÇO QUE FALTA (o degrau mais alto: sem opções)
   ⭐ AS DUAS PORTAS, regra da casa: teclado na tela E teclado de verdade. No PC
   da escola tem teclado e a criança vai digitar; no celular, não tem.
   ⚠️ E é a única folha do caderno que pede ESCRITA. Não é contradição com o
   degrau: a criança já ouviu esse pedaço nas oito folhas anteriores e já o viu
   escrito na folha 7 — aqui ela só fecha o circuito som → letra. */
function f9(d, pi){
  faixa(d, pi, NOMES[8]);
  enunciado(d, pi, "Escute a palavra e <b>escreva o pedaço que falta</b>.", "p9enun");
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    (function(reg, i){
      var w = reg[0], qual = reg[1], id = "o9_" + i, box = item(i + 1);
      var ss = sil(w), certa = esc(ss[qual]), feito = !!ST.resp[id];
      registra(id, pi, certa);
      box.appendChild(figComSom(w, null, id));
      var lin = el("div", "pedfila"), k, q = null;
      for(k = 0; k < ss.length; k++){
        if(k) lin.appendChild(el("span", "mais", "+"));
        if(k === qual){
          q = el("div", "sq" + (feito ? " ok" : " vaga"), feito ? certa : "");
          q.setAttribute("data-qa", "sq-" + id);
          (function(q){
            q.onclick = function(){ if(!ST.resp[id]) ativa(q, certa, id, "certo9_" + w, "dica9_" + w); };
          })(q);
          lin.appendChild(q);
        } else {
          (function(k){
            var b = pedaco(ss[k], w, k, "dada");
            b.onclick = function(){ sPasso(); falarSilaba(w, k, ss[k]); };
            lin.appendChild(b);
          })(k);
        }
      }
      box.appendChild(lin);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 10 — O MURAL DAS PALAVRAS MONTADAS (o fecho, e ele GUARDA o que ela fez)
   ⭐ Regra 11 da pesquisa: a tela final mostra o que a CRIANÇA fez. Cada palavra
   que ela escolhe entra no mural já partida em pedaços — o retrato do que este
   caderno inteiro treinou —, e o painel fica no relatório do professor. */
function f10(d, pi){
  faixa(d, pi, NOMES[9]);
  enunciado(d, pi, "Toque nas palavras que você montou e quer no <b>seu mural</b>.", "p10enun");
  var L = ST.folha.p10, mural = el("div", "mural");
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "o10_" + i;
      registra(id, pi, w);
      var c = el("button", "cartaorima cartasil",
        img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>" +
        '<span class="blin pedmural">' + sil(w).join("·") + "</span>");
      c.setAttribute("data-qa", "mural-" + id);
      c.setAttribute("aria-label", esc(w) + ", " + sil(w).join(", "));
      c.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falarPedacos(w);
        c.className = "cartaorima cartasil escolhido";
        acertou(id, "certo10_" + w);
      };
      if(ST.resp[id]) c.className = "cartaorima cartasil escolhido";
      mural.appendChild(c);
    })(L[i], i);
  }
  d.appendChild(mural);
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
  /* ⚠️⚠️ OS IDS TÊM QUE BATER COM O QUE AS FOLHAS GRAVAM (prefixo `o`, deste
     caderno). Este é o ponto exato onde um caderno CLONADO mente no relatório sem
     dar erro nenhum: os dois lados ficam sintaticamente corretos, nenhum portão de
     TEXTO vê, e a nota sai ZERO com a folha toda respondida. Aconteceu duas vezes
     nesta casa. Clonou caderno? Confira ESTA função primeiro — e só confie nela
     depois de JOGAR até o fim.
     ⚠️ A folha 7 é de LIGAR: o id dela nasce dentro do `montaLigar` e tem outra
     forma (`l<pagina><tag>_<chave>`). Esquecer isso zera a folha inteira. */
  var ids = [], i, k, F = ST.folha;
  if(pi === 1) for(i = 0; i < F.p1.length; i++) ids.push("o1_" + i);
  if(pi === 2) for(i = 0; i < F.p2.length; i++) ids.push("o2_" + i);
  if(pi === 3) for(i = 0; i < F.p3.length; i++) ids.push("o3_" + i);
  if(pi === 4) for(i = 0; i < F.p4.length; i++) ids.push("o4_" + i);
  if(pi === 5) for(i = 0; i < F.p5.length; i++) ids.push("o5_" + i);
  if(pi === 6) for(i = 0; i < F.p6.length; i++) ids.push("o6_" + i);
  if(pi === 7) for(i = 0; i < F.p7.length; i++) for(k = 0; k < F.p7[i].length; k++)
    ids.push("l7o7g" + i + "_" + F.p7[i][k]);
  if(pi === 8) for(i = 0; i < F.p8.length; i++) ids.push("o8_" + i);
  if(pi === 9) for(i = 0; i < F.p9.length; i++) ids.push("o9_" + i);
  if(pi === 10) for(i = 0; i < F.p10.length; i++) ids.push("o10_" + i);
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
    /* ⚠️ O SELO DA MEDALHA CHAMA-SE `mo_selo`, NÃO `mo_estrela` — e isto é um
       conserto, não um capricho (set/2026). O arquivo da estrelinha da medalha
       tinha o mesmo nome que teria a FIGURA da palavra ESTRELA: bastou a
       palavra entrar no pote para a criança ver o selo dourado da medalha no
       lugar do desenho. Nome de peça de interface nunca pode colidir com nome
       de palavra do pote. */
    est += '<img src="img/mo_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você começou a descobrir que os pedaços se juntam e viram palavra!";
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
  {n: "Juntar dois pedaços", f: [1],
   ok: "junta os dois pedaços na ordem e reconhece a palavra que eles formam",
   nao: "ainda não junta os pedaços — ouve BO e LA como duas coisas separadas"},
  {n: "Achar o pedaço que falta", f: [2, 3],
   ok: "descobre o pedaço que falta no fim, no começo e até no meio da palavra",
   nao: "ainda não completa a palavra quando um pedaço está faltando"},
  {n: "Pôr os pedaços na ordem", f: [4, 5],
   ok: "monta a palavra com os pedaços fora de ordem, e descarta o que sobra",
   nao: "ainda troca a ordem dos pedaços ou usa o pedaço que era de outra palavra"},
  {n: "Juntar SÓ de ouvido", f: [6],
   ok: "escuta os pedaços soltos e descobre sozinha que palavra eles formam",
   nao: "ainda precisa ver a palavra escrita para juntar os pedaços"},
  {n: "Reconhecer a palavra escrita em pedaços", f: [7],
   ok: "liga a figura ao seu nome escrito em pedaços",
   nao: "ainda não reconhece a palavra quando ela aparece partida em pedaços"},
  {n: "Escutar até o FIM", f: [8],
   ok: "escuta até o fim antes de decidir, e não se engana com duas palavras que começam igual",
   nao: "ainda decide pelo começo da palavra; vale retomar pares como BOLA e BOLO em voz alta"},
  {n: "Escrever o pedaço", f: [9],
   ok: "escreve sozinha o pedaço que falta, sem opções na tela",
   nao: "ainda depende das opções prontas para responder"}
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
    parecer += "junta pedaços para formar palavras em todos os degraus avaliados: " +
      domina.join("; ") + ".";
  else if(domina.length)
    parecer += "já " + domina.join("; ") + ". Ainda precisa retomar: " + retomar.join(", ") + ".";
  else
    parecer += "ainda está aprendendo a JUNTAR os pedaços de uma palavra. Nenhum objetivo " +
      "chegou a 75% de acerto de primeira — vale retomar ORALMENTE, falando a palavra em " +
      "pedaços devagar (bo... la...) e pedindo que ela adivinhe, antes de voltar à tela.";

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
