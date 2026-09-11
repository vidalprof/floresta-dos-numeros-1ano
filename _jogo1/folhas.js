/* ============================================================
   O GRANDE JOGO DAS PALAVRAS — a casa das dez folhas.

   Aqui moram as peças que TODAS as folhas usam (o alto-falante, a fileira de
   opções, o arrastar, o ligar, o teclado) e, mais abaixo, as dez folhas.
   O catálogo dos verbos de folha impressa é o `_padrao/INTERATIVIDADES-FOLHA.md`.

   ⚠️ ESTE ARQUIVO NASCEU CLONADO da Tecla do Espaço (degrau 7) — e é o único da
   escada que GUARDA o que veio de lá de propósito: as frases e o gesto de
   cortar voltam nas folhas 7 e 8, porque este caderno é a REVISÃO. O que não
   volta (a folha de contar palavras, a de ordenar, a palavra que falta) foi
   ARRANCADO, não deixado inerte.
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
  var c = el("div", "capa"), nome = "O GRANDE JOGO DAS PALAVRAS", k = 0, letras = "";
  nome.split(" ").forEach(function(pal, pi2){
    if(pi2) letras += '<span class="esp"></span>';
    letras += '<span class="pv">';
    for(var j = 0; j < pal.length; j++, k++)
      letras += '<span class="lt" style="animation-delay:' + (0.05 * k).toFixed(2) + 's">' + pal.charAt(j) + '</span>';
    letras += '</span>';
  });
  /* ⭐ A CENA É A ESCADA INTEIRA: oito degraus acendendo um depois do outro,
     e o último com a taça. É o único caderno que pode contar essa história,
     porque é o único que vem depois de todos. */
  var passos = "";
  for(k = 1; k <= 8; k++)
    passos += '<span class="degrau d' + k + '">' + k + "</span>";
  c.innerHTML =
    '<div class="ceu"><i class="nv n1"></i><i class="nv n2"></i><i class="nv n3"></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Alfabetização &middot; 1º ano &middot; a revisão dos oito degraus</div>' +
    '<div class="esteira">' +
      '<div class="cena cenaescada">' + passos + '<span class="taca"></span></div>' +
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
function figComSom(w, cls){
  var c = el("div", "figsil" + (cls ? " " + cls : ""));
  c.innerHTML = img(w, "figgrande");
  var lin = el("div", "chamlin");
  lin.appendChild(el("b", "", esc(w)));
  lin.appendChild(botaoSom("Ouvir " + esc(w), function(){ falar("pal_" + w); }));
  c.appendChild(lin);
  return c;
}
/* ============================================================
   AS DEZ FOLHAS DO DEGRAU 6 — "a letra que muda tudo".

   ⭐ O QUE MUDA DO DEGRAU 5 PARA CÁ. Lá a peça era a SÍLABA: BO + LA = BOLA.
   Aqui a peça encolheu até a menor de todas — a LETRA. E a descoberta do degrau
   é a que dá nome ao caderno: **trocar UMA letra troca a palavra inteira**.
   BOLA, BOTA, BOCA. GATO, PATO, RATO. Quem entendeu isso entendeu para que serve
   o alfabeto; quem não entendeu vai ler CASA onde está escrito CAMA a vida
   inteira, porque "quase igual" ainda parece igual.

   ⚠️ AQUI A VOZ DIZ O NOME DA LETRA — e isto NÃO contradiz o degrau 4.
   No degrau 4 (O Som que Abre) dizer "bê" era o erro, porque lá o assunto era o
   SOM /b/ e o nome da letra o esconde. Aqui o assunto É a letra: o currículo de
   Blumenau pede *"nomear as letras do alfabeto"*, e o nome é como a criança vai
   pedir a letra ao professor e achá-la no teclado. Nome de letra é palavra de
   verdade ("éle", "ême") e o sintetizador diz certo — por isso este caderno não
   precisa de recorte de sílaba e o `silabas.json` dele sai vazio, de propósito.
   ============================================================ */

/* ============================================================
   AS DEZ FOLHAS DO DEGRAU 7 — "a tecla do espaço quebrou".

   ⭐ O PROBLEMA VEM PRIMEIRO E O CONCEITO POR ÚLTIMO (Portão 0 da filosofia da
   casa, e a lacuna de curiosidade de Loewenstein). O caderno não abre dizendo
   "hoje vamos aprender que as palavras se separam por espaços". Abre com uma
   DESGRAÇA: a professora foi digitar e a tecla do espaço quebrou. Saiu
   OGATOCOMEUOPEIXE. Agora ninguém consegue ler — e a criança é quem vai
   consertar. O conceito ("é o espaço que separa uma palavra da outra") ela
   descobre no meio do conserto, não antes dele.
   ⚠️ A premissa é da folha d20 da colheita, que dizia exatamente isso: *"a
   professora foi digitar a parlenda do macaco, mas a tecla do espaço não
   funcionou"*. A ideia é da folha, não nossa.

   ⚠️ POR QUE A CRIANÇA TOCA NA LETRA QUE COMEÇA A PALAVRA, E NÃO NO ESPAÇO.
   No papel a folha manda *"passar um traço"* entre as palavras. Na tela o traço
   viraria um alvo de 20 px de largura — abaixo do piso da casa (40 px), que é o
   dedo de uma criança de seis anos. Então o gesto foi virado do avesso, sem
   perder o conceito: ela toca na LETRA QUE COMEÇA a próxima palavra, e o corte
   nasce ali, antes dela. O alvo é a letra inteira, grande, e a pergunta fica
   até mais honesta: "onde COMEÇA a próxima palavra?".
   ============================================================ */

/* ============================================================
   AS DEZ FOLHAS DO DEGRAU 8 — "o grande jogo das palavras".

   ⭐ ESTE É O CADERNO DE REVISÃO, e ele é o ÚNICO da escada que não sobe um
   degrau novo: ele volta e passa por TODOS. Rima (degrau 1), palmas (2), como
   começa (3 e 4), montar a palavra (5 e 6), cortar a frase (7). Tudo o que ela
   aprendeu, agora em forma de JOGO — que é o que a revisão espaçada (Roediger,
   Bjork) precisa para não virar prova disfarçada.

   ⭐ E É AQUI QUE ENTRAM OS TRÊS CLÁSSICOS QUE O MARCOS NOMEOU e que a sequência
   ainda não tinha usado: **memória**, **caça-palavras** e **forca**. Eles não
   entram por enfeite: cada um mede um degrau anterior por um caminho diferente —
   a memória mede a RIMA sem perguntar nada, o caça-palavras mede a PALAVRA
   ESCRITA, e a forca mede a LETRA com a palavra escondida.
   ============================================================ */

/* ---------- as opções de NÚMERO (1 a 4) — a folha das palmas ---------- */
function opsNum(ate){
  var l = [], k;
  for(k = 1; k <= (ate || 4); k++)
    l.push({v: String(k), rot: '<span class="ltop">' + k + "</span>",
            aria: k + (k === 1 ? " palma" : " palmas"), fala: "num_" + k});
  return l;
}

/* 1 — O JOGO DA MEMÓRIA DAS RIMAS (revisão do degrau 1)
   ⭐ A CARTA É GRANDE, E ISSO É REGRA PERMANENTE DA CASA (Marcos, ago/2026:
   *"quando fizer jogo da memória faça cartas maiores, registre para sempre fazer
   isso"*). A carta de memória é o alvo mais difícil de qualquer atividade: a
   criança precisa VER a figura, LER a palavra e ainda LEMBRAR onde ela estava.
   Carta pequena mata as três de uma vez. O piso medido é 130 × 88 px.
   ⚠️ E AQUI O PAR NÃO É A CARTA IGUAL: é a carta que RIMA. GATO casa com PATO,
   BOLA com MOLA. Memória de par idêntico não ensina nada de língua — só treina
   memória visual. Assim ela tem que dizer as duas palavras na cabeça e comparar
   o FIM delas, que é o degrau 1 inteiro. */
function f1(d, pi){
  faixa(d, pi, NOMES[0]);
  enunciado(d, pi, "Vire duas cartas e ache as palavras que <b>rimam</b>. Elas acabam igual!", "p1enun");
  var L = ST.folha.p1;
  for(var i = 0; i < L.length; i++){
    (function(pares, i){
      var box = item(i + 1), abertas = [], travado = false, k;
      /* cada PAR é um item do relatório — e ele se registra ANTES das cartas,
         para o `idsDaPagina` e a folha falarem exatamente a mesma língua */
      for(k = 0; k < pares.length; k++)
        registra("g1_" + i + "_" + k, pi, pares[k].join("-"));
      /* a ordem das cartas é FIXA (o portão do jogador precisa de resultado
         estável) mas nunca em pares vizinhos: primeiro os começos, depois os
         fins ao contrário */
      var lista = [];
      for(k = 0; k < pares.length; k++) lista.push({w: pares[k][0], p: i + "_" + k});
      for(k = pares.length - 1; k >= 0; k--) lista.push({w: pares[k][1], p: i + "_" + k});
      var grade = el("div", "mcartas");
      lista.forEach(function(c, j){
        var id = "g1_" + c.p;
        var ct = el("div", "mcarta" + (ST.resp[id] ? " achada" : ""));
        ct.setAttribute("data-qa", "mc-" + i + "-" + j);
        ct.setAttribute("aria-label", ST.resp[id] ? esc(c.w) : "carta virada para baixo");
        ct.innerHTML =
          '<div class="mgira">' +
            '<div class="mface mverso"><i class="mbrilho"></i><span class="minterro">?</span></div>' +
            '<div class="mface mfrente">' + img(c.w, "mfig") +
              '<span class="mrot">' + esc(c.w) + "</span></div>" +
          "</div>";
        ct.onclick = function(){
          if(travado || ST.resp[id] || ct.className.indexOf("aberta") > -1) return;
          sTecla(); ct.className = "mcarta aberta";
          falar("pal_" + c.w);
          abertas.push({el: ct, c: c, id: id});
          if(abertas.length < 2) return;
          travado = true;
          var a = abertas[0], b = abertas[1];
          setTimeout(function(){
            if(a.c.p === b.c.p && a.el !== b.el){
              a.el.className = "mcarta achada"; b.el.className = "mcarta achada";
              sCerto(); acertou(a.id, "certo1_" + a.c.w);
            } else {
              sErro(); a.el.className = "mcarta"; b.el.className = "mcarta";
              errou(a.id, "dica1_" + a.c.w);
            }
            abertas = []; travado = false;
          }, 1100);
        };
        grade.appendChild(ct);
      });
      box.appendChild(grade);
      box.setAttribute("data-qa", "memoria-" + i);
      d.appendChild(box);
    })(L[i], i);
  }
}

/* 2 — QUANTAS PALMAS? (revisão do degrau 2)
   Volta o gesto mais antigo da escada, agora sem andaime nenhum: a figura, a voz
   e o número. É a prática de recuperação (Roediger) fazendo o seu trabalho —
   lembrar do que aprendeu há quatro cadernos fixa mais que reaprender. */
function f2(d, pi){
  faixa(d, pi, NOMES[1]);
  enunciado(d, pi, "Fale a palavra batendo palma. <b>Quantas palmas</b> você bateu?", "p2enun");
  var L = ST.folha.p2;
  for(var i = 0; i < L.length; i++){
    var w = L[i], id = "g2_" + i, box = item(i + 1);
    box.appendChild(figComSom(w));
    opcoes(box, pi, id, opsNum(4), String(sil(w).length), "figbt",
           "certo2_" + w, "dica2_" + w);
    fechaItem(d, box, id);
  }
}

/* 3 — QUEM COMEÇA IGUAL? (revisão dos degraus 3 e 4)
   Uma figura-alvo e três candidatas: só uma começa com o mesmo pedaço. */
function f3(d, pi){
  faixa(d, pi, NOMES[2]);
  enunciado(d, pi, "Qual delas <b>começa igual</b> à figura de cima?", "p3enun");
  var L = ST.folha.p3;
  for(var i = 0; i < L.length; i++){
    (function(reg, i){
      var alvo = reg[0], certa = reg[1], id = "g3_" + i, box = item(i + 1);
      box.appendChild(figComSom(alvo));
      var ops = reg.slice(1);
      var gira = i % 3;
      ops = ops.slice(gira).concat(ops.slice(0, gira));
      opcoes(box, pi, id, ops.map(function(x){
        return {v: x, rot: img(x, "figop") + '<span class="rotop">' + esc(x) + "</span>",
                aria: esc(x), fala: "pal_" + x};
      }), certa, "fig", "certo3_" + certa, "dica3_" + certa);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 4 — O CAÇA-PALAVRAS (revisão dos degraus 5 e 6)
   ⭐ O CAÇA-PALAVRAS DA CASA ENSINA AO ACHAR (regra da pesquisa): quando a
   criança fecha uma palavra, a voz a diz EM PEDAÇOS e a figura acende. Sem isso
   ele é só um jogo de encontrar formas, e não ensina língua nenhuma.
   ⚠️ SÓ HORIZONTAL E VERTICAL, nunca diagonal nem de trás para frente: no 1º ano
   a criança ainda está firmando a direção da leitura, e palavra de trás para
   frente ensina o contrário do que o ano inteiro ensinou.
   ⚠️ E O GESTO É TOCAR LETRA POR LETRA, não arrastar: arrastar numa grade exige
   mira fina, e o dedo de seis anos escorrega. Ela toca na primeira e na última;
   o caminho entre as duas acende sozinho. */
function f4(d, pi){
  faixa(d, pi, NOMES[3]);
  enunciado(d, pi, "Ache as palavras na grade. Toque na <b>primeira</b> e na <b>última</b> letra.", "p4enun");
  var L = ST.folha.p4;
  for(var i = 0; i < L.length; i++){
    (function(reg, i){
      var grade = reg[0], palavras = reg[1], onde = reg[2], box = item(i + 1);
      var achadas = {}, primeira = null, cels = {};
      var alvos = el("div", "cpalvos");
      palavras.forEach(function(w){
        var a = el("div", "cpalvo" + (ST.resp["g4_" + i + "_" + w] ? " achado" : ""),
          img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>");
        a.setAttribute("data-qa", "cpalvo-" + i + "-" + w);
        alvos.appendChild(a); cels["alvo_" + w] = a;
        registra("g4_" + i + "_" + w, pi, esc(w));
        if(ST.resp["g4_" + i + "_" + w]) achadas[w] = 1;
      });
      box.appendChild(alvos);
      var gr = el("div", "cpgrade"), lin, col;
      gr.style.gridTemplateColumns = "repeat(" + grade[0].length + ", 1fr)";
      for(lin = 0; lin < grade.length; lin++){
        for(col = 0; col < grade[lin].length; col++){
          (function(lin, col){
            var b = el("button", "cpcel", grade[lin][col]);
            b.setAttribute("data-qa", "cp-" + i + "-" + lin + "-" + col);
            b.setAttribute("aria-label", "letra " + grade[lin][col]);
            b.onclick = function(){
              if(!primeira){
                primeira = {l: lin, c: col, el: b};
                b.className = "cpcel marcada"; sTecla(); return;
              }
              var w = fechaCaminho(primeira, {l: lin, c: col}, grade, palavras, onde, achadas);
              primeira.el.className = "cpcel";
              if(w){
                achadas[w] = 1;
                pintaCaminho(onde[w], cels, i);
                cels["alvo_" + w].className = "cpalvo achado";
                sCerto(); falarPedacosOuPalavra(w);
                acertou("g4_" + i + "_" + w, "certo4_" + w);
              } else {
                sErro(); b.className = "cpcel errada";
                setTimeout(function(){ b.className = "cpcel"; }, 420);
                /* a tentativa errada conta para a primeira palavra que AINDA
                   falta — não para a primeira da lista, que pode já estar achada */
                var falta = palavras[0], q;
                for(q = 0; q < palavras.length; q++) if(!achadas[palavras[q]]){ falta = palavras[q]; break; }
                errou("g4_" + i + "_" + falta, "dica4_" + falta);
              }
              primeira = null;
            };
            gr.appendChild(b); cels[lin + "_" + col] = b;
          })(lin, col);
        }
      }
      box.appendChild(gr);
      /* o que já estava achado de uma sessão anterior volta pintado */
      palavras.forEach(function(w){ if(achadas[w]) pintaCaminho(onde[w], cels, i); });
      box.setAttribute("data-qa", "caca-" + i);
      d.appendChild(box);
    })(L[i], i);
  }
}
/* devolve a palavra se o caminho da primeira à última letra for exatamente o
   caminho declarado de alguma palavra que ainda falta */
function fechaCaminho(a, b, grade, palavras, onde, achadas){
  for(var k = 0; k < palavras.length; k++){
    var w = palavras[k];
    if(achadas[w]) continue;
    var cam = onde[w], p0 = cam[0], p1 = cam[cam.length - 1];
    if((a.l === p0[0] && a.c === p0[1] && b.l === p1[0] && b.c === p1[1]) ||
       (a.l === p1[0] && a.c === p1[1] && b.l === p0[0] && b.c === p0[1])) return w;
  }
  return null;
}
function pintaCaminho(cam, cels, i){
  for(var k = 0; k < cam.length; k++){
    var c = cels[cam[k][0] + "_" + cam[k][1]];
    if(c) c.className = "cpcel achada";
  }
}
/* fala a palavra em pedaços quando o caderno tem recorte; senão, inteira */
function falarPedacosOuPalavra(w){ falar("pal_" + w); }

/* 5 — A FORCA (revisão do degrau 6)
   ⭐ O clássico que o Marcos nomeou e que a escada ainda não tinha usado. Ele
   mede a LETRA por um caminho que nenhuma outra folha usa: a palavra está
   escondida e a criança tem que pensar em qual letra ARRISCAR.
   ⚠️ NA VERSÃO DA CASA NINGUÉM É ENFORCADO. O desenho da forca é violento e não
   tem nada a ver com o conteúdo; aqui o que acontece a cada erro é o BALÃO ir
   descendo — seis erros e ele pousa. A criança perde a rodada, não um boneco.
   ⚠️ E A FIGURA FICA À VISTA desde o começo: sem ela, a criança que ainda não lê
   chuta letra no escuro e a folha vira loteria. Com ela, a tarefa é a certa —
   "eu sei que palavra é, agora quais são as letras dela?". */
function f5(d, pi){
  faixa(d, pi, NOMES[4]);
  enunciado(d, pi, "Olhe a figura e <b>adivinhe as letras</b>. O balão desce a cada erro!", "p5enun");
  var L = ST.folha.p5;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "g5_" + i, box = item(i + 1), txt = esc(w), pronto = !!ST.resp[id];
      registra(id, pi, txt);
      box.appendChild(figComSom(w));
      var ceu = el("div", "ceuforca");
      ceu.innerHTML = '<i class="balao" style="top:0%"></i><i class="chao"></i>';
      box.appendChild(ceu);
      var balao = ceu.querySelector(".balao"), erros = 0;
      var fila = el("div", "letfila"), vagas = [], k;
      for(k = 0; k < txt.length; k++){
        var v = el("div", "vagalet" + (pronto ? " cheia" : ""), pronto ? txt.charAt(k) : "");
        fila.appendChild(v); vagas.push(v);
      }
      box.appendChild(fila);
      var tec = el("div", "tecforca"), usadas = {};
      "ABCDEFGHIJLMNOPQRSTUVXZ".split("").forEach(function(L2){
        var b = el("button", "tf", L2);
        b.setAttribute("data-qa", "tf-" + id + "-" + L2);
        b.setAttribute("aria-label", "letra " + L2);
        b.onclick = function(){
          if(ST.resp[id] || usadas[L2] || erros >= 6) return;
          usadas[L2] = 1; sTecla();
          var tem = false, j;
          for(j = 0; j < txt.length; j++) if(txt.charAt(j) === L2){
            vagas[j].className = "vagalet cheia"; vagas[j].textContent = L2; tem = true;
          }
          if(tem){
            b.className = "tf boa";
            var faltam = 0;
            for(j = 0; j < vagas.length; j++) if(!vagas[j].textContent) faltam++;
            if(!faltam){ falar("pal_" + w); setTimeout(function(){ acertou(id, "certo5_" + w); }, 900); }
          } else {
            b.className = "tf ruim"; erros++;
            balao.style.top = (erros * 16) + "%";
            if(erros >= 6){
              /* ⚠️ pousar NÃO trava a folha: a palavra se revela e a criança
                 segue. Deixá-la presa num item seria beco sem saída. */
              for(j = 0; j < txt.length; j++){
                vagas[j].className = "vagalet revelada"; vagas[j].textContent = txt.charAt(j);
              }
              falar("pal_" + w);
              setTimeout(function(){ acertou(id, "pousou_" + w); }, 900);
            } else errou(id, "dica5_" + w);
          }
        };
        tec.appendChild(b);
      });
      if(pronto) tec.style.display = "none";
      box.appendChild(tec);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 6 — MONTE A PALAVRA COM AS LETRAS (revisão do degrau 6) */
function f6(d, pi){
  faixa(d, pi, NOMES[5]);
  enunciado(d, pi, "As letras saíram fora de ordem. <b>Monte o nome da figura.</b>", "p6enun");
  var L = ST.folha.p6;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "g6_" + i, box = item(i + 1), txt = esc(w), pronto = !!ST.resp[id];
      registra(id, pi, txt);
      box.appendChild(figComSom(w));
      var trilha = el("div", "vagas letvagas"), vagas = [], k;
      for(k = 0; k < txt.length; k++){
        var v = el("div", "vaga vagalet2" + (pronto ? " ok" : ""), pronto ? txt.charAt(k) : "");
        trilha.appendChild(v); vagas.push(v);
      }
      box.appendChild(trilha);
      var lista = txt.split("");
      lista = lista.slice(1).concat([lista[0]]);
      var banco = el("div", "letbanco"), posto = 0;
      lista.forEach(function(L2, j){
        var b = el("button", "let" + (pronto ? " usadalet" : ""), L2);
        b.setAttribute("data-qa", "let-" + id + "-" + j);
        b.setAttribute("aria-label", "letra " + L2);
        function poe(){
          if(ST.resp[id] || b.className.indexOf("usadalet") > -1) return;
          if(L2 !== txt.charAt(posto)){
            sErro(); b.className = "let errolet";
            setTimeout(function(){ b.className = "let"; }, 460);
            errou(id, "dica6_" + w); return;
          }
          sPasso();
          vagas[posto].className = "vaga vagalet2 ok"; vagas[posto].textContent = L2;
          b.className = "let usadalet"; posto++;
          if(posto === txt.length){ falar("pal_" + w);
            setTimeout(function(){ acertou(id, "certo6_" + w); }, 900); }
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

/* 7 — CORTE A FRASE (revisão do degrau 7) */
function f7(d, pi){
  faixa(d, pi, NOMES[6]);
  enunciado(d, pi, "A tecla do espaço quebrou de novo! Toque na letra que <b>começa</b> cada palavra.", "p7enun");
  var L = ST.folha.p7;
  for(var i = 0; i < L.length; i++){
    (function(chave, i){
      var id = "g7_" + i, box = item(i + 1);
      var txt = FRASES[chave][0], cola = txt.split(" ").join(""), pronto = !!ST.resp[id];
      var ps = txt.split(" "), cortes = [], n = 0, k;
      for(k = 0; k < ps.length - 1; k++){ n += ps[k].length; cortes.push(n); }
      registra(id, pi, txt);
      var tira = el("div", "tirafig");
      FRASES[chave][1].forEach(function(f){ tira.innerHTML += img(f, "figfrase"); });
      box.appendChild(tira);
      var ouvir = el("button", "bt azul ouvirped", "Escutar a frase");
      ouvir.setAttribute("data-qa", "ouvir-" + id);
      ouvir.onclick = function(){ sPasso(); falar("frase_" + chave); };
      box.appendChild(ouvir);
      var fila = el("div", "frasefila" + (pronto ? " aberta" : "")), achados = {}, quantos = 0;
      for(k = 0; k < cola.length; k++){
        (function(k){
          var cortavel = cortes.indexOf(k) > -1;
          var b = el("button", "lfr" + (pronto && cortavel ? " cortada" : ""), cola.charAt(k));
          b.setAttribute("data-qa", "lfr-" + id + "-" + k);
          b.setAttribute("aria-label", "letra " + cola.charAt(k));
          b.onclick = function(){
            if(ST.resp[id]) return;
            if(!cortavel || achados[k]){
              sErro(); b.className = "lfr fora";
              setTimeout(function(){ b.className = "lfr"; }, 460);
              errou(id, "dica7_" + chave); return;
            }
            sTecla(); b.className = "lfr cortada"; achados[k] = 1; quantos++;
            if(quantos === cortes.length){
              fila.className = "frasefila aberta"; falar("frase_" + chave);
              setTimeout(function(){ acertou(id, "certo7_" + chave); }, 1400);
            }
          };
          fila.appendChild(b);
        })(k);
      }
      box.appendChild(fila);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 8 — LIGUE A FIGURA À FRASE (revisão do degrau 7) */
function f8(d, pi){
  faixa(d, pi, NOMES[7]);
  enunciado(d, pi, "<b>Ligue</b> cada figura à frase que fala dela.", "p8enun");
  var L = ST.folha.p8;
  for(var i = 0; i < L.length; i++){
    var g = L[i], cx = el("div", "");
    montaLigar(cx, pi, "g8g" + i, g.map(function(c){
      return {k: c, w: FRASES[c][0], wd: FRASES[c][0],
              esq: img(FRASES[c][1][0], "figop"),
              dir: '<span class="frlig">' + FRASES[c][0] + "</span>",
              fe: "frase_" + c, fd: "frase_" + c,
              fc: "certo8_" + c, dica: "dica8_" + c};
    }), d);
    d.appendChild(cx);
  }
}

/* 9 — ESCREVA O NOME DA FIGURA (o degrau mais alto de todos: sem nada)
   ⚠️ Nem opções, nem letras dadas, nem buraco: só a figura, a voz e o teclado.
   É a última folha da sequência inteira, e a única em que a criança escreve a
   palavra do começo ao fim. Por isso só entram palavras curtas e já vistas —
   o que se mede é "ela escreve sozinha", não ortografia. */
function f9(d, pi){
  faixa(d, pi, NOMES[8]);
  enunciado(d, pi, "Olhe a figura, escute e <b>escreva o nome dela</b> inteiro.", "p9enun");
  var L = ST.folha.p9;
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "g9_" + i, box = item(i + 1), certa = esc(w), feito = !!ST.resp[id];
      registra(id, pi, certa);
      box.appendChild(figComSom(w));
      var lin = el("div", "letfila");
      var q = el("div", "sq larga" + (feito ? " ok" : " vaga"), feito ? certa : "");
      q.setAttribute("data-qa", "sq-" + id);
      q.onclick = function(){ if(!ST.resp[id]) ativa(q, certa, id, "certo9_" + w, "dica9_" + w); };
      lin.appendChild(q);
      box.appendChild(lin);
      fechaItem(d, box, id);
    })(L[i], i);
  }
}

/* 10 — O MURAL DO CAMPEÃO (o fecho da SEQUÊNCIA INTEIRA)
   ⭐ Não é o mural de um caderno: é o de oito. Cada palavra que ela escolhe
   entra com os pedaços e as letras à mostra — o retrato do caminho todo. */
function f10(d, pi){
  faixa(d, pi, NOMES[9]);
  enunciado(d, pi, "Toque nas palavras que você quer no <b>seu mural de campeão</b>.", "p10enun");
  var L = ST.folha.p10, mural = el("div", "mural");
  for(var i = 0; i < L.length; i++){
    (function(w, i){
      var id = "g10_" + i;
      registra(id, pi, w);
      var c = el("button", "cartaorima cartasil",
        img(w, "figop") + '<span class="rotop">' + esc(w) + "</span>" +
        '<span class="blin pedmural">' + sil(w).join("·") + "</span>");
      c.setAttribute("data-qa", "mural-" + id);
      c.setAttribute("aria-label", esc(w));
      c.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falar("pal_" + w);
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
  /* ⚠️ O TETO É O TAMANHO DA RESPOSTA, NÃO UM NÚMERO MÁGICO (set/2026).
     Este teclado veio clonado do caderno da LETRA, onde a resposta tinha uma
     letra só e o teto de 4 nunca incomodava. Aqui a resposta é uma PALAVRA:
     PEIXE parava em "PEIX" e MACACO em "MACA", a criança digitava certo e o
     quadradinho simplesmente não aceitava a última letra — sem erro, sem som,
     sem nada na tela. Três itens da folha 9 ficaram impossíveis, e só o
     jogar-até-o-fim viu. */
  else { if(ATIVA.val.length >= ATIVA.certa.length) return; ATIVA.val += ch; }
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
  /* ⚠️⚠️ OS IDS TÊM QUE BATER COM O QUE AS FOLHAS GRAVAM (prefixo `g`, deste
     caderno). Este é o ponto exato onde um caderno CLONADO mente no relatório sem
     dar erro nenhum: os dois lados ficam sintaticamente corretos, nenhum portão de
     TEXTO vê, e a nota sai ZERO com a folha toda respondida. Aconteceu duas vezes
     nesta casa. Clonou caderno? Confira ESTA função primeiro — e só confie nela
     depois de JOGAR até o fim.
     ⚠️ A folha 8 é de LIGAR: o id dela nasce dentro do `montaLigar` e tem outra
     forma (`l<pagina><tag>_<chave>`). Esquecer isso zera a folha inteira. */
  var ids = [], i, k, F = ST.folha;
  /* \u26a0\ufe0f as folhas 1 e 4 t\u00eam MAIS DE UM item por tabuleiro: na mem\u00f3ria cada
     PAR conta, no ca\u00e7a-palavras cada PALAVRA. \u00c9 aqui que um caderno clonado
     mente no relat\u00f3rio sem dar erro nenhum. */
  if(pi === 1) for(i = 0; i < F.p1.length; i++) for(k = 0; k < F.p1[i].length; k++)
    ids.push("g1_" + i + "_" + k);
  if(pi === 2) for(i = 0; i < F.p2.length; i++) ids.push("g2_" + i);
  if(pi === 3) for(i = 0; i < F.p3.length; i++) ids.push("g3_" + i);
  if(pi === 4) for(i = 0; i < F.p4.length; i++) for(k = 0; k < F.p4[i][1].length; k++)
    ids.push("g4_" + i + "_" + F.p4[i][1][k]);
  if(pi === 5) for(i = 0; i < F.p5.length; i++) ids.push("g5_" + i);
  if(pi === 6) for(i = 0; i < F.p6.length; i++) ids.push("g6_" + i);
  if(pi === 7) for(i = 0; i < F.p7.length; i++) ids.push("g7_" + i);
  if(pi === 8) for(i = 0; i < F.p8.length; i++) for(k = 0; k < F.p8[i].length; k++)
    ids.push("l8g8g" + i + "_" + F.p8[i][k]);
  if(pi === 9) for(i = 0; i < F.p9.length; i++) ids.push("g9_" + i);
  if(pi === 10) for(i = 0; i < F.p10.length; i++) ids.push("g10_" + i);
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
    est += '<img src="img/jg_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  else txt = "Você já andou oito degraus — e cada um deles ficou com você!";
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
  {n: "Rima (degrau 1)", f: [1],
   ok: "acha, de memória, as palavras que rimam",
   nao: "ainda não compara o FIM de duas palavras"},
  {n: "Pedaços da palavra (degrau 2)", f: [2],
   ok: "conta as palmas da palavra sem ajuda nenhuma na tela",
   nao: "ainda erra a contagem dos pedaços"},
  {n: "Como a palavra começa (degraus 3 e 4)", f: [3],
   ok: "acha a figura que começa igual à figura-alvo",
   nao: "ainda não compara o começo de duas palavras"},
  {n: "A palavra escrita (degrau 6)", f: [4, 6],
   ok: "acha a palavra escondida na grade e monta o nome da figura letra por letra",
   nao: "ainda não reconhece a palavra escrita fora do lugar de sempre"},
  {n: "Arriscar a letra (a forca)", f: [5],
   ok: "descobre as letras da palavra escondida, uma tentativa de cada vez",
   nao: "ainda chuta letra sem pensar na palavra que a figura mostra"},
  {n: "O espaço entre as palavras (degrau 7)", f: [7, 8],
   ok: "separa as palavras de uma frase grudada e casa cada frase com a sua figura",
   nao: "ainda lê a frase como um bloco só"},
  {n: "Escrever sozinha", f: [9],
   ok: "escreve o nome da figura inteiro, sem letra nenhuma dada",
   nao: "ainda precisa de letras ou opções na tela para escrever"}
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
    parecer += "domina a sequência de alfabetização em todos os degraus avaliados: " +
      domina.join("; ") + ".";
  else if(domina.length)
    parecer += "já " + domina.join("; ") + ". Ainda precisa retomar: " + retomar.join(", ") + ".";
  else
    parecer += "ainda está juntando as peças da alfabetização. Nenhum objetivo chegou a 75% " +
      "de acerto de primeira — este caderno é de REVISÃO: vale voltar ao degrau em que ela " +
      "travou (a tabela abaixo diz qual) antes de insistir aqui.";

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
