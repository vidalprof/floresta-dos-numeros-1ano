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
  var c = el("div", "capa"), nome = "O DESFILE DAS LETRAS", k, letras = "";
  for(k = 0; k < nome.length; k++){
    var ch = nome.charAt(k);
    letras += ch === " " ? '<span class="esp"></span>'
      : '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + ch + '</span>';
  }
  /* ⭐ A CENA CONTA A ATIVIDADE: as primeiras letras do alfabeto entram em fila,
     uma depois da outra, como num desfile — que é exatamente o que a criança vai
     aprender a fazer. Nada de figura aqui: neste caderno o conteúdo É a letra. */
  var cena = "";
  "ABCDEFG".split("").forEach(function(L, i){
    cena += '<span class="ltcapa" style="animation-delay:' + (0.45 + i * 0.13).toFixed(2) + 's">' +
            esc(L) + "</span>";
  });
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Alfabetização &middot; 1º ano &middot; dez folhas do alfabeto</div>' +
    '<div class="esteira">' +
      '<div class="cena">' + cena + '</div>' +
      '<div class="cinta"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>' +
    '</div>' +
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
   força olhar a ordem em vez de reconhecer a forma. *//* ============================================================
   O DESFILE DAS LETRAS — as dez folhas

   ⭐ Degrau 0 da sequência de alfabetização (`_sequencias/SD-MONTADA-DE-FOLHAS-SOLTAS.md`).
   Cada folha veio de uma FOLHA REAL de professor — as 45 em `_sequencias/folhas_d0/`
   — e é fiel ao comando impresso. O que muda é só o GESTO.

   ⚠️ O CRIVO DO PEDAGOGO CORTOU MAIS DA METADE, e o motivo importa: sete das 24
   folhas da primeira colheita pediam ORDENAR PALAVRAS alfabeticamente (BANANA,
   XÍCARA, CEBOLA…) e várias mandavam ESCREVER a lista inteira. Isso é 2º/3º ano:
   supõe que a criança já lê e escreve com fluência. No 1º ano ela ainda está
   NOMEANDO as letras. Ordenar palavra pela 1ª letra só faz sentido depois que a
   ordem das letras está automática — que é justamente o que este caderno constrói.

   ⚠️ E TUDO EM LETRA BASTÃO MAIÚSCULA. Foi uma professora que apontou isso nos
   comentários de uma das folhas: *"por que não usar as letras em bastão
   maiúsculas tanto no comando quanto nos exercícios?"*. Ela tem razão — a
   criança que está aprendendo o alfabeto lê bastão, não cursiva nem minúscula.
   Duas folhas da colheita foram descartadas por isso (uma em minúscula, uma com
   teclado QWERTY, que não é ordem alfabética coisa nenhuma).

   ⚠️ A ESCADA É DE DIFICULDADE, não a ordem das folhas de papel:
     reconhecer a letra → nomear → achar a que falta → DEPOIS (fácil: recita-se
     para frente) → ANTES (difícil: obriga a voltar) → as duas juntas →
     ordenar → achar o intruso → a letra da palavra → o mural.
   ============================================================ */

var ALFA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

/* a letra grande, com o alto-falante — a peça que se repete em quase toda folha.
   ⚠️ ALTO-FALANTE EM TODA LETRA: no 1º ano a criança está justamente aprendendo
   o NOME da letra. Sem a voz, ela reconhece o desenho e não aprende o nome. */
function letraSom(L, cls){
  var c = el("div", "ltbox" + (cls ? " " + cls : ""));
  c.appendChild(el("span", "ltg", esc(L)));
  c.appendChild(botaoSom("Ouvir a letra " + esc(L), function(){ falar("let_" + L); }));
  return c;
}
function opsLetra(lista){
  return lista.map(function(L){
    return {v: L, rot: '<span class="ltop">' + esc(L) + "</span>", aria: "letra " + L,
            fala: "let_" + L};
  });
}

/* 1 — O DESFILE DO ALFABETO (o degrau mais baixo: só SEGUIR a ordem)
   ⭐ Antes de qualquer pergunta, a criança PERCORRE a ordem com o dedo e ouve o
   nome de cada letra. É o "cante o alfabeto" da sequência de 10 aulas, virado em
   gesto: cinco letras em fila, e ela toca uma a uma NA ORDEM. Se pular, não
   acende — e é isso que ensina que a fila tem um caminho só. */
function f1(d, pi){
  faixa(d, pi, NOMES[0]);
  enunciado(d, pi, "Toque nas letras <b>na ordem</b>, do começo ao fim. Ouça o nome de cada uma.", "p1enun");
  var L = ST.folha.p1;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var k = it.i, id = "a1_" + i, box = item(i + 1);
      var seq = [], j;
      for(j = k; j < k + 5 && j < 26; j++) seq.push(ALFA.charAt(j));
      registra(id, pi, seq.join(""));
      var fila = el("div", "desfile"), bts = [], passo = 0;
      seq.forEach(function(Lt, n){
        var b = el("button", "ltdesf", '<span class="ltop">' + esc(Lt) + "</span>");
        b.setAttribute("data-qa", "desf-" + id + "-" + Lt);
        b.setAttribute("aria-label", "letra " + Lt);
        b.onclick = function(){
          if(ST.resp[id]) return;
          if(n !== passo){
            /* ⚠️ pular NÃO é "errou": é a folha ensinando o caminho. A voz diz
               qual é a próxima, sem a palavra "errado". */
            sErro(); falar("volte_" + seq[passo]);
            errou(id, "dica1_" + seq[passo]);
            return;
          }
          sPasso(); falar("let_" + Lt);
          b.className = "ltdesf aceso"; passo++;
          if(passo === seq.length) setTimeout(function(){ acertou(id, "certo1_" + seq[0]); }, 520);
        };
        fila.appendChild(b); bts.push(b);
      });
      if(ST.resp[id]) bts.forEach(function(b){ b.className = "ltdesf aceso"; });
      box.appendChild(fila);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 2 — QUE LETRA É ESTA? (nomear, que é o objetivo A do currículo)
   A voz diz o nome; a criança acha a letra. É o caminho SOM → SÍMBOLO, que é o
   mais difícil dos dois e o que a escrita vai exigir. */
function f2(d, pi){
  faixa(d, pi, NOMES[1]);
  enunciado(d, pi, "Ouça o nome da letra e toque nela.", "p2enun");
  var L = ST.folha.p2;
  for(var i = 0; i < L.length; i++){
    var it = L[i], id = "a2_" + i, box = item(i + 1);
    var lin = el("div", "pergls");
    lin.appendChild(el("b", "", "Onde está a letra…"));
    lin.appendChild(botaoSom("Ouvir a letra", (function(x){ return function(){ falar("let_" + x); }; })(it.L)));
    box.appendChild(lin);
    /* ⚠️ a letra NÃO aparece escrita no enunciado — se aparecesse, a criança
       casaria os desenhos sem nunca ouvir o nome, e a folha viraria outra coisa. */
    opcoes(box, pi, id, opsLetra(it.op), it.L, "figbt", "certo2_" + it.L, "dica2_" + it.L);
    fechaItem(d, box, id);
  }
}

/* 3 — A LETRA QUE FUGIU (a fila com um buraco)
   ⚠️ OS DISTRATORES NÃO PODEM ESTAR NA FILA — defeito já pago na Fábrica de
   Palavras: a fila mostrava "M N ? P" e uma das opções era o próprio M, que
   estava ali à vista. A criança acertava olhando, não pensando. */
function f3(d, pi){
  faixa(d, pi, NOMES[2]);
  enunciado(d, pi, "Uma letra <b>fugiu</b> da fila. Qual é?", "p3enun");
  var L = ST.folha.p3;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var k = it.i, certa = ALFA.charAt(k), id = "a3_" + i, box = item(i + 1);
      var fila = el("div", "filalfa");
      [k - 2, k - 1, k, k + 1].forEach(function(x){
        if(x < 0 || x >= 26) return;
        if(x === k) fila.appendChild(el("div", "buraco" + (ST.resp[id] ? " ok" : ""),
                                        ST.resp[id] ? certa : "?"));
        else fila.appendChild(el("span", "lt", ALFA.charAt(x)));
      });
      box.appendChild(fila);
      opcoes(box, pi, id, opsLetra(it.op), certa, "figbt", "certo3_" + certa, "dica3_" + certa);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 4 — QUEM VEM DEPOIS (o mais FÁCIL dos dois, e por isso vem antes)
   ⭐ A criança recita o alfabeto PARA A FRENTE. Perguntar o sucessor é pedir que
   ela continue de onde está — cabe no que ela já faz. */
function f4(d, pi){
  faixa(d, pi, NOMES[3]);
  enunciado(d, pi, "Qual letra vem <b>depois</b> desta?", "p4enun");
  var L = ST.folha.p4;
  for(var i = 0; i < L.length; i++){
    var it = L[i], id = "a4_" + i, box = item(i + 1);
    var lin = el("div", "vizinha");
    lin.appendChild(letraSom(it.L, "grandona"));
    lin.appendChild(el("i", "setacss"));
    lin.appendChild(el("div", "vaga", "?"));
    box.appendChild(lin);
    opcoes(box, pi, id, opsLetra(it.op), it.c, "figbt", "certo4_" + it.L, "dica4_" + it.L);
    fechaItem(d, box, id);
  }
}

/* 5 — QUEM VEM ANTES (o degrau que quase nenhuma folha separa, e devia)
   ⭐ ESTE É O PULO. Achar o ANTECESSOR obriga a criança a VOLTAR na fila, e ela
   só sabe recitar para frente. Muita gente trata "antes e depois" como uma coisa
   só; são duas, e esta é bem mais difícil. Por isso tem folha própria — e a dica
   ensina o truque: recitar do começo até chegar na letra. */
function f5(d, pi){
  faixa(d, pi, NOMES[4]);
  enunciado(d, pi, "Qual letra vem <b>antes</b> desta?", "p5enun");
  var L = ST.folha.p5;
  for(var i = 0; i < L.length; i++){
    var it = L[i], id = "a5_" + i, box = item(i + 1);
    var lin = el("div", "vizinha");
    lin.appendChild(el("div", "vaga", "?"));
    lin.appendChild(el("i", "setacss"));
    lin.appendChild(letraSom(it.L, "grandona"));
    box.appendChild(lin);
    opcoes(box, pi, id, opsLetra(it.op), it.c, "figbt", "certo5_" + it.L, "dica5_" + it.L);
    fechaItem(d, box, id);
  }
}

/* 6 — ANTES E DEPOIS ao mesmo tempo (as duas na mesma cabeça)
   ⚠️ AS DUAS VAGAS SÃO O MESMO ITEM: só fecha quando as duas estão certas. É
   isso que faz o degrau ser maior que a soma das folhas 4 e 5 — a criança tem
   que segurar a fila inteira, não meia fila. */
function f6(d, pi){
  faixa(d, pi, NOMES[5]);
  enunciado(d, pi, "<b>Preencha</b> os dois lados: quem vem antes e quem vem depois.", "p6enun");
  var L = ST.folha.p6;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var k = ALFA.indexOf(it.L), id = "a6_" + i, box = item(i + 1);
      var ant = ALFA.charAt(k - 1), dep = ALFA.charAt(k + 1);
      registra(id, pi, ant + dep);
      var lin = el("div", "vizinha"), feito = {a: !!ST.resp[id], d: !!ST.resp[id]};
      var vA = el("div", "vaga" + (feito.a ? " ok" : ""), feito.a ? ant : "?");
      var vD = el("div", "vaga" + (feito.d ? " ok" : ""), feito.d ? dep : "?");
      lin.appendChild(vA); lin.appendChild(letraSom(it.L, "grandona")); lin.appendChild(vD);
      box.appendChild(lin);
      var pool = [ant, dep, ALFA.charAt(Math.max(0, k - 3)), ALFA.charAt(Math.min(25, k + 3))];
      var vistos = {}, ops = [];
      pool.forEach(function(x){ if(x && !vistos[x]){ vistos[x] = 1; ops.push(x); } });
      ops.sort();
      var box2 = el("div", "ops");
      ops.forEach(function(x){
        var b = el("button", "op figbt", '<span class="ltop">' + esc(x) + "</span>");
        b.setAttribute("data-qa", "op-" + id + "-" + x);
        b.setAttribute("aria-label", "letra " + x);
        b.onclick = function(){
          if(ST.resp[id]) return;
          sPasso(); falar("let_" + x);
          if(x === ant && !feito.a){ feito.a = 1; vA.className = "vaga ok"; vA.textContent = ant; }
          else if(x === dep && !feito.d){ feito.d = 1; vD.className = "vaga ok"; vD.textContent = dep; }
          else { b.className = "op figbt erro"; setTimeout(function(){ b.className = "op figbt"; }, 480);
                 errou(id, "dica6_" + it.L); return; }
          if(feito.a && feito.d) setTimeout(function(){ acertou(id, "certo6_" + it.L); }, 380);
        };
        box2.appendChild(b);
      });
      box.appendChild(box2);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 7 — PONHA NA ORDEM (arrastar, e tocar também vale)
   Da folha: *"coloque as letras abaixo em ordem alfabética"*. No papel ela
   recorta e cola; aqui ela PUXA — e quem não consegue arrastar, toca. */
function f7(d, pi){
  faixa(d, pi, NOMES[6]);
  enunciado(d, pi, "Estas letras <b>embaralharam</b>. Toque nelas na ordem certa do alfabeto.", "p7enun");
  var L = ST.folha.p7;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "a7_" + i, box = item(i + 1), certa = it.g.slice().sort();
      registra(id, pi, certa.join(""));
      var emb = certa.slice(), tmp;
      /* ⚠️ embaralhar SEM sorteio: o portão do jogador precisa de resultado
         estável, e a criança não vê diferença. Trocar as pontas basta. */
      tmp = emb[0]; emb[0] = emb[emb.length - 1]; emb[emb.length - 1] = tmp;
      tmp = emb[1]; emb[1] = emb[2]; emb[2] = tmp;
      var trilha = el("div", "trilhalt"), k, vagas = [];
      for(k = 0; k < certa.length; k++){
        var v = el("div", "vaga" + (ST.resp[id] ? " ok" : ""), ST.resp[id] ? certa[k] : "");
        trilha.appendChild(v); vagas.push(v);
      }
      box.appendChild(trilha);
      var banco = el("div", "ops"), posto = 0;
      emb.forEach(function(Lt){
        var b = el("button", "op figbt", '<span class="ltop">' + esc(Lt) + "</span>");
        b.setAttribute("data-qa", "ord-" + id + "-" + Lt);
        b.setAttribute("aria-label", "letra " + Lt);
        function poe(){
          if(ST.resp[id] || b.className.indexOf("usada") > -1) return;
          if(Lt !== certa[posto]){
            sErro(); b.className = "op figbt erro";
            setTimeout(function(){ b.className = "op figbt"; }, 480);
            errou(id, "dica7_" + certa[0]); return;
          }
          sPasso(); falar("let_" + Lt);
          vagas[posto].className = "vaga ok"; vagas[posto].textContent = Lt;
          b.className = "op figbt usada"; posto++;
          if(posto === certa.length) setTimeout(function(){ acertou(id, "certo7_" + certa[0]); }, 420);
        }
        b.onclick = function(){ if(b._arrastou){ b._arrastou = false; return; } poe(); };
        puxavel(b, vagas, poe);
        banco.appendChild(b);
      });
      if(ST.resp[id]) banco.querySelectorAll("button").forEach
        ? Array.prototype.forEach.call(banco.querySelectorAll("button"), function(b){ b.className = "op figbt usada"; })
        : 0;
      box.appendChild(banco);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 8 — QUEM SAIU DA FILA (o intruso na ordem) ⭐ da folha 16
   ⭐ ACHAR O INTRUSO É MAIS DIFÍCIL QUE ORDENAR, e é por isso que vem depois: em
   vez de construir a ordem, a criança tem que CONFERIR uma ordem que já está
   pronta — e conferir exige ter a fila na cabeça, não no papel. */
function f8(d, pi){
  faixa(d, pi, NOMES[7]);
  enunciado(d, pi, "Uma letra <b>entrou no lugar errado</b>. Circule quem saiu da fila.", "p8enun");
  var L = ST.folha.p8;
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "a8_" + i, box = item(i + 1);
      registra(id, pi, it.c);
      var grade = el("div", "gradecirc filaerr"), bts = [];
      it.g.forEach(function(Lt){
        var b = el("button", "figcirc", '<span class="ltop">' + esc(Lt) + "</span>");
        b.setAttribute("data-qa", "int-" + id + "-" + Lt);
        b.setAttribute("aria-label", "letra " + Lt);
        b._w = Lt; grade.appendChild(b); bts.push(b);
      });
      box.appendChild(grade);
      riscoDeCircular(grade, bts, function(b){
        if(ST.resp[id]) return;
        sPasso(); falar("let_" + b._w);
        if(b._w === it.c){ b.className = "figcirc marcada"; acertou(id, "certo8_" + it.c); }
        else { b.className = "figcirc erro";
               setTimeout(function(){ b.className = "figcirc"; }, 480);
               errou(id, "dica8_" + it.c); }
      });
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 9 — COM QUE LETRA COMEÇA (a ponte para o degrau 4 da sequência)
   ⚠️ AQUI A LETRA VIRA SOM, e é a primeira vez no caderno. Até agora ela era um
   NOME ("esta é o bê"); agora ela é o começo de uma palavra ("BOLA começa com
   bê"). É o degrau que liga o alfabeto à alfabetização, e por isso fecha o
   caderno — daqui em diante a sequência trabalha o som. */
function f9(d, pi){
  faixa(d, pi, NOMES[8]);
  enunciado(d, pi, "Com que letra <b>começa</b> o nome da figura?", "p9enun");
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    var it = L[i], id = "a9_" + i, box = item(i + 1);
    var cx = el("div", "chamrima");
    cx.innerHTML = img(it.w, "figgrande");
    var lin = el("div", "chamlin");
    lin.appendChild(el("b", "", esc(it.w.toUpperCase())));
    lin.appendChild(botaoSom("Ouvir " + esc(it.w), (function(w){ return function(){ falar("pal_" + w); }; })(it.w)));
    cx.appendChild(lin); box.appendChild(cx);
    opcoes(box, pi, id, opsLetra(it.op), it.c, "figbt", "certo9_" + it.w, "dica9_" + it.w);
    fechaItem(d, box, id);
  }
}

/* 10 — O ALFABETO DA TURMA (o fecho, e ele GUARDA o que ela fez)
   ⭐ Regra 11 da pesquisa: a tela final mostra o que a CRIANÇA fez. Aqui ela
   monta o próprio alfabeto ilustrado — a letra e uma palavra que começa com ela
   — e o painel fica no relatório. É também a ideia da aula 10 da sequência de
   professor: um cartaz coletivo que fica exposto na sala. */
function f10(d, pi){
  faixa(d, pi, NOMES[9]);
  enunciado(d, pi, "Toque nas letras que você quer no <b>seu alfabeto</b>. Ele fica guardado no fim.", "p10enun");
  var L = ST.folha.p10, mural = el("div", "mural");
  for(var i = 0; i < L.length; i++){
    (function(it, i){
      var id = "a10_" + i;
      registra(id, pi, it.L);
      var c = el("button", "cartaorima cartalt",
        '<span class="ltop grande">' + esc(it.L) + "</span>" +
        img(it.w, "figop") + '<span class="rotop">' + esc(it.w.toUpperCase()) + "</span>");
      c.setAttribute("data-qa", "mural-" + id);
      c.setAttribute("aria-label", "letra " + it.L + ", " + it.w);
      c.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falar("let_" + it.L);
        setTimeout(function(){ falar("pal_" + it.w); }, 620);
        c.className = "cartaorima cartalt escolhido";
        acertou(id, "certo10_" + it.L);
      };
      if(ST.resp[id]) c.className = "cartaorima cartalt escolhido";
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
  /* ⚠️ OS IDS TÊM QUE BATER COM O QUE AS FOLHAS GRAVAM (prefixo `a`, deste
     caderno). Ver a lição no topo — este é o ponto onde um caderno clonado
     mente no relatório sem dar erro nenhum. */
  var ids = [], i, F = ST.folha;
  if(pi === 1) for(i = 0; i < F.p1.length; i++) ids.push("a1_" + i);
  if(pi === 2) for(i = 0; i < F.p2.length; i++) ids.push("a2_" + i);
  if(pi === 3) for(i = 0; i < F.p3.length; i++) ids.push("a3_" + i);
  if(pi === 4) for(i = 0; i < F.p4.length; i++) ids.push("a4_" + i);
  if(pi === 5) for(i = 0; i < F.p5.length; i++) ids.push("a5_" + i);
  if(pi === 6) for(i = 0; i < F.p6.length; i++) ids.push("a6_" + i);
  if(pi === 7) for(i = 0; i < F.p7.length; i++) ids.push("a7_" + i);
  if(pi === 8) for(i = 0; i < F.p8.length; i++) ids.push("a8_" + i);
  if(pi === 9) for(i = 0; i < F.p9.length; i++) ids.push("a9_" + i);
  if(pi === 10) for(i = 0; i < F.p10.length; i++) ids.push("a10_" + i);
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
    est += '<img src="img/ab_estrela' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você começou a conhecer a fila das letras — e ela é comprida!";
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
  {n: "Seguir a ordem do alfabeto", f: [1],
   ok: "percorre a fila das letras na ordem certa, sem pular",
   nao: "ainda não segura o caminho da fila do começo ao fim"},
  {n: "Nomear a letra pelo som do nome", f: [2],
   ok: "ouve o nome da letra e acha qual é",
   nao: "ainda liga o nome ouvido ao desenho da letra com dificuldade"},
  {n: "Achar a letra que falta na fila", f: [3],
   ok: "descobre qual letra fugiu do lugar",
   nao: "ainda não usa as letras vizinhas como pista"},
  {n: "Quem vem DEPOIS (sucessor)", f: [4],
   ok: "diz qual letra vem depois de uma dada",
   nao: "ainda precisa recitar o alfabeto inteiro para chegar lá"},
  {n: "Quem vem ANTES (antecessor)", f: [5, 6],
   ok: "diz qual letra vem antes — o degrau mais difícil da ordem",
   nao: "ainda só recita para a frente, e voltar na fila custa"},
  {n: "Ordenar e conferir a ordem", f: [7, 8],
   ok: "põe letras embaralhadas em ordem e enxerga quem saiu da fila",
   nao: "ainda constrói a ordem, mas não a confere sozinha"},
  {n: "A letra que abre a palavra", f: [9],
   ok: "sabe com que letra começa o nome da figura",
   nao: "ainda não liga a letra ao som que ela faz na palavra"}
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
    parecer += "domina a ordem do alfabeto em todos os degraus avaliados: " +
      domina.join("; ") + ".";
  else if(domina.length)
    parecer += "já " + domina.join("; ") + ". Ainda precisa retomar: " + retomar.join(", ") + ".";
  else
    parecer += "está começando a construir a ordem do alfabeto. Nenhum objetivo chegou a " +
      "75% de acerto de primeira — vale retomar oralmente, cantando o alfabeto e apontando " +
      "as letras no varal da sala, antes de voltar à tela.";

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
