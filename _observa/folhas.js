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
var LIGAR = [1, 2, 3, 4];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
var CORES = ["c1", "c1", "c2", "c2", "c3", "c3", "c4", "c4", "c5", "c5", "c1", "c1", "c3", "c2"];


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
  var caps = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14], i;
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
  /* ⚠️ A PALAVRA ANIMADA E O TITULO DE VERDADE (licao paga em 20/set/2026):
     quatro cadernos trocaram de nome e continuaram estampando o antigo em
     letras grandes porque o `var nome` ficou para tras. */
  var c = el("div", "capa"),
      nome = "Aprendendo a observar",
      k, letras = "", pos = 0;
  var V = typeof VIMG !== "undefined" ? VIMG : 2;
  nome.split(" ").forEach(function(pal, w){
    var s = "";
    for(k = 0; k < pal.length; k++, pos++){
      s += '<span class="lt" style="animation-delay:' + (0.05 * pos).toFixed(2) + 's">' +
           pal.charAt(k) + '</span>';
    }
    pos++;
    letras += (w ? '<span class="esp"></span>' : '') + '<span class="tpal">' + s + '</span>';
  });
  /* a cena: a figura ao lado da propria sombra — o assunto do caderno numa imagem.
     ⚠️ SEM SORTEIO: a capa tem de sair igual em toda foto, senao o portao das
        fotos (5c) acusa mudanca que nao houve. */
  var cena = [["ob_tomate.png", 0], ["ob_tomate_sombra.png", 0.3],
              ["ob_bicicleta.png", 0.6], ["ob_bicicleta_sombra.png", 0.9]], cx = "";
  cena.forEach(function(P){
    cx += '<div class="cart" style="-webkit-animation-delay:' + P[1] + 's;animation-delay:' + P[1] + 's">' +
          '<img draggable="false" onload="naoAmplia(this)" src="img/' + P[0] + '?v=' + V + '" alt="">' +
          '</div>';
  });
  c.innerHTML =
    '<div class="ceu"><i></i><i></i><i></i></div>' +
    '<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">Pr\u00e9 &middot; 14 folhas: as iguais, a sombra, o diferente e o que vem depois</div>' +
    '<div class="cena">' + cx + '</div>' +
    '<i class="lupa"></i>' +
    '<div class="chamada">Escreva o seu nome ali embaixo e toque em <b>Come\u00e7ar</b>.</div>';
  d.appendChild(c);
}

/* ⚠️ A PECA `gavetas` DO ESQUELETO FOI REMOVIDA: este caderno nao classifica
   em gavetas, e ela usava um `GAV` que nunca existiu aqui — o ESLint (portao
   0a2) reprovava com razao. Codigo morto que referencia dado inexistente nao e
   inofensivo: e a proxima sessao achando que a peca funciona. */
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
    if(P.ariaE) e.setAttribute("aria-label", P.ariaE);
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
    if(P.ariaD) e.setAttribute("aria-label", P.ariaD);
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
    est += '<img src="img/ob_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
  {n: "Achar a figura igual a outra", f: [1, 2],
   ok: "acha a figura igual entre várias parecidas"},
  {n: "Achar a sombra da figura, sem a cor", f: [3, 4],
   ok: "reconhece a figura pelo formato, quando a cor não ajuda"},
  {n: "Achar o que não é igual aos outros", f: [5, 6],
   ok: "separa o que destoa, por desenho e por família"},
  {n: "Descobrir o que vem depois na fila", f: [7, 8],
   ok: "reconhece o padrão que se repete e diz o próximo"},
  {n: "Pintar seguindo a legenda das cores", f: [9, 10],
   ok: "casa o número com a cor que a legenda manda"},
  {n: "Lembrar onde estava a figura", f: [11, 12],
   ok: "acha os quatro pares do jogo da memória"},
  /* ⚠️ O TEXTO DESTE OBJETIVO AVISA O QUE ELE NÃO MEDE, e de propósito: o
     professor lê isto no relatório, ao lado da nota. Na tela o risco sai pronto,
     então esta folha mede a ORDEM DOS NÚMEROS, nunca o traçado. */
  {n: "Tocar os números na ordem, de 1 a 10", f: [13],
   ok: "toca os números de 1 a 10 na ordem (ATENÇÃO: isto mede a ORDEM DOS NÚMEROS, não o traçado — na tela o risco sai pronto)"}
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
   AS DOZE FOLHAS DO PRÉ

   ⭐ Pedido do Marcos (21/set/2026): *"preciso de cadernos de atividades para o
      pré — ligar pontos, selecionar, pintar, memória, ligar figuras, sombras…
      e que a criança consiga fazer no computador o que é pedido nas
      atividades"*, e depois: *"pode ser, é só uma experiência, uma exceção
      dessa vez"* (a cara vem do estilo que ele gostou no LogicLike).

   ⚠️ PISO DE FOLHAS: 10 a 15 no PRÉ, não 35 (decisão dele no mesmo dia). A
      criança do Pré não sustenta trinta minutos na mesma atividade.
   ⚠️ A CRIANÇA DO PRÉ NÃO LÊ. Tudo o que a folha pede é DITO; o texto na tela
      existe para o adulto que está do lado. Cada opção tem o alto-falante irmão.
   ============================================================ */

/* --- 1 e 2 · LIGAR AS IGUAIS --------------------------------
   O degrau mais fácil que existe: a figura da direita é A MESMA da esquerda,
   só mudou de lugar. É a porta de entrada do gesto de ligar. */
function fIguais(d, pi, lista, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var box = item(0);
  montaLigar(box, pi, "g0", ST.folha["p" + pi][0].map(function(k){
    var F = FIG[k];
    return {k: k, ariaE: F.n, ariaD: F.n,
            esq: img(F.f, "figl", F.n),
            dir: img(F.f, "figl", F.n),
            fala: "fig_" + k, fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  }), d);
  d.appendChild(box);
}
function f1(d, pi){ fIguais(d, pi, null, "Toque numa figura e depois na figura <b>igual</b> a ela."); }
function f2(d, pi){ fIguais(d, pi, null, "Agora são seis. Ligue cada figura à sua <b>igual</b>."); }

/* --- 3 e 4 · LIGAR A FIGURA À SUA SOMBRA --------------------
   O degrau sobe: a figura da direita perdeu a COR, e a criança tem de decidir
   pelo FORMATO. É o comando impresso na folha, palavra por palavra:
   "LIGUE CADA FIGURA À SUA SOMBRA". */
function fSombra(d, pi, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var box = item(0);
  montaLigar(box, pi, "g0", ST.folha["p" + pi][0].map(function(k){
    var F = FIG[k];
    /* ⚠️ A SOMBRA DIZ DE QUEM ELA E. Quatro sombras chamadas so "sombra" sao,
       para quem ouve a tela, quatro coisas iguais — e o portao 1l2 reprova com
       razao. O nome tambem e o que a crianca cega ouve. */
    return {k: k, ariaE: F.n, ariaD: "sombra da " + F.n,
            esq: img(F.f, "figl", F.n),
            dir: img(SOM[k], "figl", "sombra da " + F.n),
            fala: "fig_" + k, fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  }), d);
  d.appendChild(box);
}
function f3(d, pi){ fSombra(d, pi, "A sombra é a figura <b>sem a cor</b>. Ligue cada uma à sua sombra."); }
function f4(d, pi){ fSombra(d, pi, "Agora as sombras são mais parecidas. Olhe o <b>formato</b>."); }

/* --- 5 e 6 · QUAL É O DIFERENTE? ----------------------------
   A folha de papel manda CIRCULAR; na tela a criança TOCA e a peça acende —
   o mesmo gesto, sem perda (ver o POTE).
   ⚠️ As opções são as FIGURAS, não palavras: quem faz esta folha não lê. */
function fDiferente(d, pi, dados, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var D = dados[k];
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var lista = D.pecas.map(function(p, n){
      var F = FIG[p];
      return {v: "o" + n, rot: img(F.f, "figop", F.n), aria: F.n, fala: "fig_" + p};
    });
    opcoes(box, pi, id, lista, "o" + D.r, "fig",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f5(d, pi){ fDiferente(d, pi, DIF1, "Três são iguais e <b>um</b> é diferente. Toque no diferente."); }
function f6(d, pi){ fDiferente(d, pi, DIF2, "Agora pense: três são da <b>mesma família</b> e um não é. Qual?"); }

/* --- 7 e 8 · O QUE VEM DEPOIS? ------------------------------
   A fila mostra o padrão e o último quadrado está vazio. A criança PUXA a peça
   certa até ele — ou toca nela, que é a segunda porta (regra das duas portas). */
function fSequencia(d, pi, dados, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var S = dados[k];
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var fila = el("div", "fila");
    S.fila.forEach(function(p){
      var F = FIG[p], c = el("span", "fcx");
      c.innerHTML = img(F.f, "figfila", F.n);
      fila.appendChild(c);
    });
    var vazio = el("span", "fcx vazio", "?");
    vazio.setAttribute("aria-label", "o lugar vazio da fila");
    fila.appendChild(vazio);
    box.appendChild(fila);
    var lista = S.ops.map(function(p){
      var F = FIG[p];
      return {v: p, rot: img(F.f, "figop", F.n), aria: F.n, fala: "fig_" + p};
    });
    opcoes(box, pi, id, lista, S.r, "fig",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k,
           function(b){
             var im = b.querySelector("img");
             vazio.innerHTML = im ? im.outerHTML : "";
             vazio.className = "fcx cheio";
           }, [vazio]);
    fechaItem(d, box, id);
  });
}
function f7(d, pi){ fSequencia(d, pi, SEQ1, "Olhe a fila e veja o que se repete. O que vem <b>depois</b>?"); }
function f8(d, pi){ fSequencia(d, pi, SEQ2, "Agora a fila repete de <b>três em três</b>. O que vem depois?"); }

/* --- 9 e 10 · PINTE PELA LEGENDA ----------------------------
   Clonada do `_aumdim2` (peça `estojo` + `pintavel`), que é a versão já
   lapidada: dois toques — pega a canetinha, toca no que vai pintar.
   ⚠️ O DESENHO AQUI É VETOR, e é a única peça do caderno que não sai de
      recorte: a região precisa TROCAR DE COR ao vivo, e figura recortada não
      troca. É a exceção que a casa já aceita ("o CSS entra só no que precisa
      se mexer em tempo real"). O desenho copia os balões da folha colhida. */
var LAPIS = null;
function estojo(d, cores){
  var cx = el("div", "estojo");
  var kk;
  for(kk in cores) if(cores.hasOwnProperty(kk)) (function(ck, C){
    var b = el("button", "cnt", C.n);
    b.style.background = C.c;
    b.setAttribute("data-qa", "lapis-" + ck);
    b.setAttribute("aria-label", "canetinha " + C.n);
    b.onclick = function(){
      sPasso(); LAPIS = ck;
      var t = cx.querySelectorAll(".cnt"), i;
      for(i = 0; i < t.length; i++) t[i].className = t[i].className.replace(" pega", "");
      b.className += " pega";
      falar("lapis_" + ck);
    };
    cx.appendChild(b);
    cx.appendChild(botaoSom("Ouvir o nome da cor",
                            function(){ falar("lapis_" + ck); }, "som somop"));
  })(kk, cores[kk]);
  d.appendChild(cx);
  return cx;
}
function fPintar(d, pi, cores, baloes, pede){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var leg = el("div", "legenda"), nn = 0, kc;
  for(kc in cores) if(cores.hasOwnProperty(kc)){
    var L = el("span", "legit");
    L.innerHTML = '<i class="legcor" style="background:' + cores[kc].c + '"></i>' +
                  '<b>' + (++nn) + '</b>';
    leg.appendChild(L);
  }
  d.appendChild(leg);
  estojo(d, cores);
  var box = item(0), cena = el("div", "baloes");
  ST.folha["p" + pi].forEach(function(k, i){
    var B = baloes[k];
    var id = "n" + pi + "_" + i, cx = el("div", "bal");
    registra(id, pi, B.cor);
    cx.innerHTML = '<svg viewBox="0 0 90 130" aria-hidden="true">' +
      '<ellipse class="bcor" cx="45" cy="50" rx="38" ry="46"></ellipse>' +
      '<path d="M45 96 L38 108 L52 108 Z" fill="#c9bfae"></path>' +
      '<path d="M45 108 q10 12 -2 20 q-10 8 2 16" stroke="#8a8172" stroke-width="3" fill="none"></path>' +
      '<text x="45" y="60" class="bnum">' + B.num + '</text></svg>';
    pintavel(cx, id, pi, B.cor, "certo" + pi + "_" + k, "dica" + pi + "_" + k, null);
    cena.appendChild(cx);
  });
  box.appendChild(cena);
  d.appendChild(box);
}
function pintavel(el2, id, pi, cor, fCerto, fDica, box){
  el2.setAttribute("data-qa", "pinta-" + id + "-0");
  el2.setAttribute("data-lapis", cor);
  if(ST.resp[id]) el2.className += " pin pin-" + cor;
  el2.onclick = function(){
    if(ST.resp[id]) return;
    if(!LAPIS){ sPasso(); falar("pegue_lapis"); return; }
    sPasso();
    if(LAPIS === cor){
      el2.className += " pin pin-" + cor;
      acertou(id, fCerto); if(box) box.className = "item feito";
    } else {
      el2.className += " sacode";
      setTimeout(function(){ el2.className = el2.className.replace(" sacode", ""); }, 420);
      errou(id, fDica);
    }
  };
}
function f9(d, pi){ fPintar(d, pi, COR1, BAL1, "Pegue a canetinha da cor certa e toque no balão com aquele número."); }
function f10(d, pi){ fPintar(d, pi, COR2, BAL2, "Agora são cinco cores. Olhe bem a legenda antes de pintar."); }

/* --- 11 · JOGO DA MEMÓRIA -----------------------------------
   Clonado do `_corpo5` f37. Aqui o par é FIGURA↔FIGURA (a mesma), porque quem
   faz esta folha não lê — par figura↔nome seria outra habilidade.
   ⚠️ O ITEM É O TABULEIRO: ele fecha quando os quatro pares caem. O id é
      `n<pi>_<i>` porque é isso que o `idsDaPagina` deduz da posição no pote. */
function fMemoria(d, pi, banco, pede, sombra){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, pede, "p" + pi + "enun");
  var id = "n" + pi + "_0", box = item(0);
  var PARES = banco[ST.folha["p" + pi][0]];
  var abertas = [], travado = false, faltam = PARES.length, k;
  registra(id, pi, PARES.join(" "));
  /* ordem FIXA (o jogador da banca precisa de resultado estável) e nunca com o
     par lado a lado: as figuras, e depois as mesmas ao contrário */
  var lista = [];
  for(k = 0; k < PARES.length; k++) lista.push({k: PARES[k], lado: "fig"});
  for(k = PARES.length - 1; k >= 0; k--) lista.push({k: PARES[k], lado: "nome"});
  var grade = el("div", "mcartas");
  lista.forEach(function(c){
    var F = FIG[c.k], feito = !!ST.resp[id];
    var ct = el("div", "mcarta" + (feito ? " achada" : ""));
    ct.setAttribute("data-qa", "mem-" + id + "-" + c.k + "-" + c.lado);
    ct.setAttribute("aria-label", feito ? esch(F.n) : "carta virada para baixo");
    ct.innerHTML =
      '<div class="mgira">' +
        '<div class="mface mverso"><i class="mbrilho"></i><span class="minterro">?</span></div>' +
        '<div class="mface mfrente">' +
          img(sombra && c.lado === "nome" ? SOM[c.k] : F.f, "mfig", F.n) +
        '</div>' +
      '</div>';
    ct.onclick = function(){
      if(travado || ST.resp[id] || ct.className.indexOf("achada") > -1 ||
         ct.className.indexOf("aberta") > -1) return;
      sTecla(); ct.className = "mcarta aberta";
      falar("fig_" + c.k);
      abertas.push({el: ct, c: c});
      if(abertas.length < 2) return;
      travado = true;
      var a = abertas[0], b = abertas[1];
      setTimeout(function(){
        if(a.c.k === b.c.k && a.el !== b.el){
          a.el.className = "mcarta achada"; b.el.className = "mcarta achada";
          sCerto(); falar("memok_" + a.c.k);
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
}

function f11(d, pi){
  fMemoria(d, pi, MEM, "Vire duas cartas e ache as <b>duas iguais</b>. São cinco pares.", false);
}
/* --- 12 · A MEMÓRIA DAS SOMBRAS -----------------------------
   ⭐ O degrau que fecha o caderno: o par agora é a figura E A SOMBRA dela, ou
      seja, as duas coisas que ele ensinou, juntas. Vem COLADA na folha 11 e não
      espalhada — mecânica que repete vem em bloco, e a segunda sobe um degrau
      (regra da casa; espaçada, a criança sente que voltou).
   ⚠️ BLOCO NOVO, DECLARADO: nenhuma folha de papel colhida traz memória de
      sombra. Elas trazem memória de iguais E sombra de ligar, separadas. */
function f12(d, pi){
  fMemoria(d, pi, MEMS, "Agora o par é a figura e a <b>sombra</b> dela. São quatro pares.", true);
}

/* --- 13 · LIGAR OS PONTOS, DE 1 A 10 ------------------------
   ⚠️⚠️ ESTA FOLHA ENTROU DECLARADA PELO QUE ELA MEDE, e nao pelo que a folha de
      papel mede. No papel o valor esta no LAPIS atravessando a folha — é
      coordenação motora fina; aqui a criança toca e o traço aparece pronto.
      O que ela treina é a ORDEM DOS NÚMEROS até dez, que é do Pré e está no
      currículo, e é isso (e só isso) que o relatório do professor diz.
   ⚠️ Por isso vai de 1 a 10. As folhas colhidas pedem de 1 a 23, 1 a 33 e até
      1 a 50 — fora do Pré. */
function f13(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Toque no <b>1</b>, depois no <b>2</b>, e vá até o <b>10</b>. " +
            "Veja o que aparece!", "p" + pi + "enun");
  var id = "n" + pi + "_0", box = item(0);
  var pts = PONTOS[ST.folha["p" + pi][0]], feito = !!ST.resp[id];
  /* a resposta declarada são os dez pedaços na ordem — o contrato que o jogador
     da banca conhece (ele toca um a um, na ordem escrita). */
  registra(id, pi, pts.map(function(_, i){ return "p" + (i + 1); }).join(" "));

  var cx = el("div", "pontos");
  var ns = "http://www.w3.org/2000/svg";
  var svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", "0 0 200 200");
  svg.setAttribute("aria-hidden", "true");
  var linha = document.createElementNS(ns, "path");
  linha.setAttribute("class", "ptraco");
  linha.setAttribute("fill", "none");
  svg.appendChild(linha);
  cx.appendChild(svg);

  var proximo = 0, bolas = [];
  function desenha(ate){
    var dd = "", i;
    for(i = 0; i < ate; i++) dd += (i ? " L" : "M") + pts[i][0] + "," + pts[i][1];
    if(ate >= pts.length) dd += " Z";
    linha.setAttribute("d", dd);
  }
  /* ⚠️ BOTÃO DE VERDADE, não `<circle>`: o dedo de cinco anos precisa de 48 px,
     e o clique num `<g>` de SVG não é confiável (o jogador da banca não fechava
     a folha). O SVG fica só para desenhar o traço. */
  pts.forEach(function(P, i){
    var b = el("button", "pbola" + (feito ? " ok" : ""), String(i + 1));
    b.style.left = (P[0] / 2) + "%";
    b.style.top = (P[1] / 2) + "%";
    b.setAttribute("data-qa", "op-" + id + "-p" + (i + 1));
    b.setAttribute("aria-label", "ponto " + (i + 1));
    b.onclick = function(){
      if(ST.resp[id]) return;
      if(i !== proximo){
        sErro();
        b.className = "pbola treme";
        setTimeout(function(){ b.className = "pbola"; }, 450);
        errou(id, "dica" + pi + "_q1");
        return;
      }
      sPasso(); falar("num_" + (i + 1));
      b.className = "pbola ok";
      proximo++; desenha(proximo);
      if(proximo === pts.length){
        bolas.forEach(function(x){ x.className = "pbola ok"; });
        acertou(id, "certo" + pi + "_q1");
      }
    };
    bolas.push(b);
    cx.appendChild(b);
  });
  if(feito){ proximo = pts.length; desenha(proximo); }
  box.appendChild(cx);
  fechaItem(d, box, id);
}

/* --- 14 · O CARTAZ ------------------------------------------
   ⭐ O FECHO TEM DE SER ALCANÇÁVEL A QUALQUER MOMENTO (regra do formato): ele
      não pede nada novo, só junta o que a criança já viu. Assim o tamanho do
      caderno não castiga quem vai devagar. */
function f14(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Você aprendeu a olhar com atenção! Toque em cada figura para ouvir o nome dela.",
            "p" + pi + "enun");
  var box = item(0), mural = el("div", "mural");
  var id = "n" + pi + "_0", lista = CARTAZ[ST.folha["p" + pi][0]];
  /* ⚠️ A RESPOSTA DECLARADA E UM NUMERO (quantas figuras), porque e assim que o
     jogador da banca reconhece a familia "marque e confirme". Contrato inventado
     e folha que ninguem mede. */
  registra(id, pi, String(lista.length));
  lista.forEach(function(k, n){
    var F = FIG[k], b = el("button", "mit");
    b.innerHTML = img(F.f, "figmural", F.n);
    b.setAttribute("aria-label", F.n);
    b.setAttribute("data-qa", "mur-" + id + "-" + n);
    b.onclick = function(){ sPasso(); falar("fig_" + k); b.className = "mit vista"; };
    mural.appendChild(b);
  });
  box.appendChild(mural);
  var bt = el("button", "bt verde pronto", "Terminei!");
  bt.setAttribute("data-qa", "pronto-" + id);
  bt.onclick = function(){ if(!ST.resp[id]) acertou(id, "certo" + pi + "_z1"); };
  if(ST.resp[id]) bt.style.display = "none";
  box.appendChild(bt);
  fechaItem(d, box, id);
}
