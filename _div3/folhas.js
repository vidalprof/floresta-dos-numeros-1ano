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
var LIGAR = [];
/* a cor da faixa por BLOCO da escada, não por folha: a criança vê que o assunto
   mudou. Uma entrada por folha, de c1 a c5. */
var CORES = ["c1", "c1", "c1", "c1", "c1", "c1", "c1", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c2", "c3", "c3", "c3", "c3", "c4", "c4", "c4", "c4", "c4", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5", "c5"];


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

/* ---------- A CAPA: A BANCADA DOS POTES ----------
   ⭐ A cena É a ideia do caderno: doze peças repartidas em três potes, e os
      três ficando com o mesmo tanto. A criança entende o gesto antes de ler o
      título — e é o gesto das 35 folhas.
   ⚠️ O título diz o ASSUNTO, não uma metáfora bonita (regra do Marcos,
      20/set/2026), e a PALAVRA ANIMADA da capa tem de dizer o mesmo que o
      `<title>` — quem confere é o portão 0b11. */
var BANCADA = [4, 4, 4];
function f0(d){
  var c = el("div", "capa"), nome = "APRENDENDO A DIVISÃO", k, letras = "";
  nome.split(" ").forEach(function(pal, w){
    var s2 = "";
    for(k = 0; k < pal.length; k++) s2 += '<span class="lt">' + pal.charAt(k) + '</span>';
    letras += (w ? '<span class="esp"></span>' : '') + '<span class="tpal">' + s2 + '</span>';
  });
  var cena = "";
  BANCADA.forEach(function(q, i){
    var bolas = "", n;
    for(n = 0; n < q; n++) bolas += '<i class="pbola"></i>';
    cena += '<div class="potec"><div class="pfila">' + bolas + "</div>" +
            '<div class="prot">' + q + "</div></div>";
  });
  c.innerHTML =
    '<div class="ceu"></div>' +
    '<h1 class="titu">' + letras + "</h1>" +
    '<div class="sub">Matemática &middot; 3º ano &middot; 35 folhas para repartir em ' +
      'partes iguais, medir em grupos e saber o que sobra</div>' +
    '<div class="cena"><div class="bancada">' + cena + "</div></div>" +
    '<div class="chamada">Doze peças, três potes, <b>quatro em cada um</b>. ' +
      "É isso que você vai fazer com a mão. Escreva o seu nome ali embaixo e " +
      "toque em <b>Começar</b>.</div>";
  d.appendChild(c);
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
    est += '<img src="img/dd3_selo' + (ke < cheias ? "" : "_off") + '.png?v=' + VIMG + '" alt="" draggable="false">';
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
     se divergirem — nome por nome e folha por folha. */
  {n: "Repartir em partes iguais, com a mão e com a conta", f: [1, 2, 3, 4, 5, 24]},
  {n: "Escrever o fato: da figura para a conta", f: [6, 7]},
  {n: "Resolver problemas de REPARTIÇÃO: quantos para cada um?", f: [8, 9, 10, 11, 34]},
  {n: "Resolver problemas de MEDIDA: quantos grupos dão?", f: [12, 13, 14, 15]},
  {n: "Usar a multiplicação para achar a divisão", f: [16, 17]},
  /* ⚠️ AS FOLHAS 31 E 32 MORAVAM NOS OBJETIVOS 1 E 2, e o relatório do
     professor dizia por causa delas uma coisa que não aconteceu. Na 31 a
     criança arrasta a CONTA até o resultado e na 32 escreve o resultado
     por extenso na cruzadinha: nas duas ela CALCULA, não reparte com a
     mão nem escreve o fato a partir da figura. Achado lendo folha a folha
     para o parecer — nenhum portão vê isto, porque os dois nomes batem
     nos dois lugares e toda folha tem objetivo. */
  {n: "Calcular a divisão por 2 a 10", f: [18, 19, 25, 26, 27, 31, 32, 33]},
  {n: "Saber o que sobra: o resto", f: [20, 21, 22, 23]},
  {n: "Reconhecer a metade, a terça, a quarta, a quinta e a décima parte", f: [28, 29, 30]},
  {n: "Levar o cartaz: os quatro sentidos da divisão", f: [35]}
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
   AS PEÇAS DESTE CADERNO.

   ⚠️ AS DE TEXTO NÃO FORAM REESCRITAS (regra da casa): `marqueConfira`,
      `estojo`/`pintavel` e a `cruzadinha` vêm dos cadernos de sílaba e do
      `_corpo5`. O que nasceu aqui é a peça central do assunto — a `reparte`,
      que não existia em casa nenhuma.
   ============================================================ */

/* ---------- ⭐ A PEÇA NOVA: REPARTIR ARRASTANDO ----------
   Ela nasce do comando da folha d06, VERBATIM: *"DIVISÃO. REPARTA EM PARTES
   IGUAIS. **CLIQUE E ARRASTE**. 8 CENOURAS PARA 2 COELHOS"* — é o papel
   pedindo arrastar com todas as letras.

   ⭐ E ELA É O MOTIVO DE ESTE CADERNO EXISTIR. O currículo do 3º ano diz, com
      todas as letras, *"por meio de estratégias e registros pessoais"* — ou
      seja, **NÃO pede o algoritmo formal da divisão**. Pede que a criança
      REPARTA. No papel ela desenha bolinhas nos potes e apaga quando erra;
      aqui ela move a peça de verdade e o pote conta sozinho.

   ⚠️ CADA PEÇA É UM ITEM, e o destino declarado é um pote que serve — não o
      ÚNICO que serve. Qualquer pote com vaga é aceito, porque repartir não tem
      ordem certa; o que se declara é um caminho válido, para o jogador
      automático da banca ter o que seguir. Registrar "só este pote" seria
      inventar uma regra que a matemática não tem.
   ⚠️ E O POTE NÃO ACEITA ALÉM DA CONTA: passar de `n/k` é o erro que a folha
      existe para mostrar. */
function reparte(d, pi, texto, fonte){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, idx){
    var R = fonte[k];
    /* ⚠️ `medida` MUDA A PERGUNTA, não a conta: com ele o tamanho do pote é
       dado e o que se conta é QUANTOS POTES; sem ele, os potes são dados e o
       que se conta é QUANTAS PEÇAS em cada um. São os dois significados que o
       currículo nomeia — *"repartição equitativa e de medida"* — e a criança
       que só viu o primeiro não reconhece o segundo como divisão. */
    var cada = R.medida || (R.n / R.k);
    var id = "n" + pi + "_" + idx, box = item(idx + 1);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", R.medida
      ? "São <b>" + R.n + " " + R.q + "</b> e em cada " + umSo(R.w) +
        " cabem <b>" + R.medida + "</b>. Encha os " + R.w + "."
      : "<b>" + R.n + " " + R.q + "</b> para <b>" + R.k + " " + R.w + "</b>. " +
        "Reparta em partes iguais."));
    lin.appendChild(botaoSom("Ouvir o que a folha pede",
      function(){ falar("rep" + pi + "_" + k); }));
    box.appendChild(lin);

    /* ⚠️⚠️ O POTE SE CHAMA PELO ID DO ITEM, não pelo número da folha. A folha
       tem TRÊS problemas e cada um monta os seus potes; com o nome antigo
       (`alvo-gav12_p0`) os três problemas da mesma folha publicavam a MESMA
       chave, e o contrato do jogador manda a chave ser única no documento
       inteiro — ele clicaria sempre no pote do primeiro problema. */
    var cols = el("div", "colunas potes"), listaC = [], p;
    function fazPote(p){
      var c = el("div", "coluna pote");
      var t = el("div", "ctit", R.pote ? img(R.pote, "figmini", R.w)
                                       : umSo(R.w).toUpperCase() + " " + (p + 1));
      t.setAttribute("data-alvo", "1");
      c.setAttribute("data-qa", "pote-" + id + "-" + p);
      c.appendChild(t);
      var dentro = el("div", "cdentro");
      c.appendChild(dentro);
      c._v = "p" + p; c._dentro = dentro; c._cabe = cada; c._tem = 0;
      listaC.push(c); cols.appendChild(c);
      return c;
    }
    /* ⭐⭐ NA MEDIDA, O POTE NASCE VAZIO E SOZINHO — e é isso que faz a pergunta
       ser outra. Com os quatro saquinhos já desenhados na tela, o enunciado
       *"veja quantos potes você precisou"* estava mentindo: bastava CONTAR os
       potes antes de tocar em nada. Agora aparece UM; quando ele enche, nasce o
       seguinte. A criança descobre o número enchendo, que é o gesto que o
       currículo chama de divisão por medida. Na repartição é o contrário: os
       potes são DADOS (é isso que a pergunta diz) e todos aparecem de uma vez. */
    if(R.medida) fazPote(0);
    else for(p = 0; p < R.k; p++) fazPote(p);
    box.appendChild(cols);
    var banco = el("div", "figbanco");
    box.appendChild(banco);
    montaReparte(pi, idx, k, R, cada, listaC, banco, box, fazPote);
    fechaItem(d, box, id);
  });
}
function umSo(w){
  /* "aquários" -> "aquário": o enunciado fala de UM pote, não de todos */
  return w.replace(/s$/, "").replace(/õe$/, "ão");
}
function montaReparte(pi, idx, k, R, cada, listaC, banco, box, fazPote){
  var id = "n" + pi + "_" + idx, postas = 0, n, marcada = null;
  /* ⚠️⚠️ A RESPOSTA DECLARADA É A DISTRIBUIÇÃO INTEIRA, não um toque só.
     Estava `">gav" + pi + "_p0"`, que é a família de DOIS TOQUES do motor: o
     jogador da banca pegava uma peça, soltava no primeiro pote e dava o item
     por fechado — e o item só fecha quando as R.n peças estão repartidas. Seis
     folhas deste caderno apareciam como "não fecha nem com a resposta certa",
     e a peça estava certa: quem não sabia jogar era o portão.
     O formato `rep:<potes>x<cada>` é lido pela família "REPARTE" do
     `_qa/joga_folha.js`, escrita no mesmo commit que esta peça. */
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
    col._dentro.appendChild(el("span", "fdentro",
      R.f ? img(R.f, "figmicro", R.q) : "&bull;"));
    marcada.parentNode.removeChild(marcada); marcada = null;
    postas++;
    /* o pote encheu: na MEDIDA nasce o seguinte, e é assim que a criança
       descobre quantos precisou (ver o comentário em `reparte`). */
    if(R.medida && col._tem >= cada && listaC.length < R.k && postas < R.n)
      ouveOPote(fazPote(listaC.length));
    if(postas === R.n){
      acertou(id, "certorep" + pi + "_" + k);
      box.className = "item feito";
    } else sPasso();
  }
  function ouveOPote(col){
    col.onclick = function(){
      if(!marcada){ sPasso(); falar("toque_peca"); return; }
      larga(col);
    };
  }
  for(n = 0; n < R.n; n++){
    (function(n){
      var b = el("button", "op figbt", R.f ? img(R.f, "figmini", R.q) : "&bull;");
      b.setAttribute("aria-label", umSo(R.q) + " " + (n + 1));
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
  listaC.forEach(ouveOPote);
  if(ST.resp[id]){
    banco.innerHTML = "";
    /* quem volta à folha já respondida vê os potes TODOS cheios — inclusive os
       que na medida ainda não tinham nascido. */
    while(listaC.length < R.k) ouveOPote(fazPote(listaC.length));
    listaC.forEach(function(col){
      var t;
      for(t = 0; t < cada; t++)
        col._dentro.appendChild(el("span", "fdentro",
          R.f ? img(R.f, "figmicro", R.q) : "&bull;"));
    });
    box.className = "item feito";
  }
}

/* ---------- MARCAR VÁRIOS + CONFERIR — do `_sil2` ---------- */
function marqueConfira(box, id, pi, pecas, fCerto, fDica){
  var feito = !!ST.resp[id], marcadas = {}, bts = [];
  registra(id, pi, pecas.filter(function(p){ return p.ok; })
                        .map(function(p){ return p.k; }).join(" "));
  var cx = el("div", "sils");
  pecas.forEach(function(P){
    var b = el("button", "sil larga" + (feito && P.ok ? " ok" : ""), P.t);
    b.setAttribute("aria-label", P.aria || P.t);
    b.setAttribute("data-qa", (P.ok ? "op-" : "no-") + id + "-" + P.k);
    b.onclick = function(){
      if(ST.resp[id]) return;
      sPasso();
      if(P.fala) P.fala();
      if(marcadas[P.k]){ delete marcadas[P.k]; b.className = "sil larga"; }
      else { marcadas[P.k] = 1; b.className = "sil larga marcada"; }
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
      bts.forEach(function(x){ if(x.P.ok) x.b.className = "sil larga ok"; });
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

/* ---------- PINTAR PELA LEGENDA — do `_sil2` ---------- */
var LAPIS = null;
function estojo(d, cores){
  var cx = el("div", "estojo");
  cores.forEach(function(C){
    var b = el("button", "cnt cnt-" + C.k, C.n);
    b.setAttribute("data-qa", "lapis-" + C.k);
    b.setAttribute("aria-label", "canetinha do resultado que " + C.n);
    b.onclick = function(){
      sPasso(); LAPIS = C.k;
      var t = cx.querySelectorAll(".cnt"), i;
      for(i = 0; i < t.length; i++) t[i].className = t[i].className.replace(" pega", "");
      b.className += " pega";
      falar("lapis_" + C.k);
    };
    cx.appendChild(b);
  });
  d.appendChild(cx);
  return cx;
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

/* ---------- A CRUZADINHA — do `_corpo5` ---------- */
function cruzadinha(d, pi, DADOSC, prefFala){
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
    var w = DADOSC[k].p.replace(/[^A-ZÁÂÃÉÊÍÓÔÕÚÇ]/g, ""), col = null;
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
    E.id = id; E.cels = []; E.rot = "Escreva a palavra " + E.n;
    var t;
    for(t = 0; t < E.w.length; t++){
      var cc = celula[(E.x + (E.hor ? t : 0)) + "," + (E.y + (E.hor ? 0 : t))];
      E.cels.push(cc);
      if(t === 0 && cc && !cc.querySelector(".cn")) cc.appendChild(el("span", "cn", E.n));
    }
    if(ST.resp[id]) E.cels.forEach(function(c2, t2){
      if(c2){ c2.className = "ccel viva ok"; c2.textContent = E.w.charAt(t2);
              if(t2 === 0) c2.appendChild(el("span", "cn", E.n)); } });
    var p = el("button", "pista" + (ST.resp[id] ? " feita" : ""),
               '<span class="pn">' + E.n + ".</span> " + DADOSC[E.k].d);
    p.setAttribute("data-qa", "esc-" + id);
    p.setAttribute("aria-label", "Pista " + E.n + " da cruzadinha");
    E.bt = p;
    p.onclick = function(){
      if(ST.resp[id]) return;
      sPasso(); falar(prefFala + E.k);
      abreCruz(E, pi);
    };
    pistas.appendChild(p);
    E.cels.forEach(function(c2){
      if(!c2) return;
      c2.addEventListener("click", function(){ if(!ST.resp[id]) abreCruz(E, pi); });
    });
  });
  d.appendChild(pistas);
}

/* ---------- peças pequenas que este caderno usa várias vezes ---------- */
/* a fileira de números 1 a 10, para responder "quanto deu?" sem teclado.
   ⚠️ O ALTO-FALANTE VEM DE GRAÇA no `opcoes` (regra do Marcos, 20/set/2026):
      a criança OUVE cada número antes de escolher, e não depois. */
/* ⚠️⚠️ O LEQUE TEM DE CONTER A RESPOSTA, e isto quase foi ao ar (24/set/2026).
   O leque ia sempre de 1 a 12, e o problema verbatim da folha d03 — *"a
   merendeira separou 48 bolinhos e colocou 2 em cada caixa"* — tem resposta
   24. A criança podia ler, entender e resolver: a resposta não estava na
   tela. Trocar os números do problema seria perder a folha de papel; então
   quem se move é o LEQUE. Quando a resposta passa do teto, as mesmas doze
   casas aparecem numa JANELA em volta dela (24 -> de 18 a 29), que é um leque
   mais difícil e mais honesto: os vizinhos do resultado são distratores
   melhores do que 1, 2 e 3.
   Quem mede é o jogador da banca, com a regra "a resposta declarada não está
   entre as opções" (`_qa/joga_folha.js`), escrita no mesmo dia. */
function opNumeros(certo, ate){
  var lista = [], n, quantas = ate || 10;
  var r = parseInt(String(certo).replace(/^r/, ""), 10);
  var de = 1;
  if(r > quantas) de = Math.max(1, r - Math.floor(quantas / 2));
  for(n = de; n < de + quantas; n++)
    lista.push({v: "r" + n, rot: String(n), aria: String(n), fala: "num_" + n});
  return lista;
}
function figs(f, q, quantas){
  var s = "", n;
  for(n = 0; n < quantas; n++) s += img(f, "figmicro", q);
  return s;
}

/* ============================================================
   AS 35 FOLHAS. Cada bloco diz de qual folha de papel nasceu e o comando
   impresso VERBATIM. O crivo das quarenta está em `_sequencias/POTE-DIV3.md`.

   ⚠️ A ESCADA, EM UMA LINHA: repartir com a mão (1-3) → contar o que já está
      repartido (4-5) → escrever o FATO (6-7) → os problemas de repartição
      (8-11) → ⭐ os de MEDIDA, que são o outro significado (12-15) → a conta
      de volta (16-17) → treinar (18-19) → ⭐ O QUE SOBRA (20-23) → aquecer
      (24) → pintar e decifrar (25-27) → metade, terça e quarta parte (28-30)
      → brincar (31-33) → inventar um problema (34) → levar o cartaz (35).
   ============================================================ */

/* ===== BLOCO A — REPARTIR COM A MÃO (1 a 3) ===== */
function f01(d, pi){
  reparte(d, pi, "Arraste cada peça para um pote, <b>até todos ficarem iguais</b>. " +
    "No computador dá para arrastar; no celular, toque na peça e depois no pote.", REP);
}
function f02(d, pi){
  reparte(d, pi, "Mesmo gesto, e <b>agora são três e quatro potes</b>. Vá pondo " +
    "uma peça em cada um, dando a volta, até acabarem.", REP);
}
function f03(d, pi){
  reparte(d, pi, "<b>Agora os potes são só caixas</b>, sem figura. O gesto é o " +
    "mesmo: repartir até ficarem iguais.", REP);
}

/* ===== BLOCO B — CONTAR O QUE JÁ ESTÁ REPARTIDO (4 e 5) ===== */
/* ⭐ A d02 é a folha mais fácil das quarenta: os desenhos já vêm agrupados e a
      criança só conta. Ela vem logo depois de repartir com a mão porque é a
      mesma coisa vista de fora — a criança reconhece o que acabou de fazer. */
function folhaGrupos(d, pi, texto, ate){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var G = GRUP[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var porGrupo = G.a / G.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", G.a + " &divide; " + G.b + " = ?"));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar("gr" + pi + "_" + k); }));
    box.appendChild(lin);
    var cx = el("div", "grupos"), g;
    for(g = 0; g < G.b; g++)
      cx.appendChild(el("div", "grupo", figs(G.f, "peça", porGrupo)));
    box.appendChild(cx);
    opcoes(box, pi, id, opNumeros("r" + porGrupo, ate), "r" + porGrupo, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f04(d, pi){
  folhaGrupos(d, pi, "As peças já estão repartidas. <b>Conte quantas há em cada " +
    "grupo</b> — é esse o resultado da conta.", 10);
}
function f05(d, pi){
  folhaGrupos(d, pi, "Mesmo gesto, e <b>agora os montes são maiores</b>. Conte " +
    "um grupo só: os outros têm o mesmo tanto.", 10);
}

/* ===== BLOCO C — DA FIGURA PARA O FATO (6 e 7) ===== */
/* ⭐⭐ A d25 manda, VERBATIM: *"Observe as ilustrações, complete a frase e
      escreva o fato correspondente… Fato: 12 ÷ 4 = ___"*. É a ponte entre o
      desenho e a conta escrita, e nenhuma outra das quarenta a faz tão bem.
   ⚠️ NA 6 A FRASE VEM PRONTA e a criança só escreve o número; na 7 ela escreve
      o fato inteiro. É o degrau. */
/* ⭐⭐ A CASINHA DE ESCREVER O RESULTADO — a mesma peça das folhas 6 e 7,
   agora num lugar só. Ela nasceu presa dentro do `folhaFato`, e quando o
   portão 0b7 mostrou que ESCOLHER tomava 49% das folhas a saída era trocar o
   leque pela escrita em algumas — o que não dava para fazer sem repetir a peça
   quatro vezes. Peça repetida é peça que desencontra.
   ⚠️ E ESCREVER NÃO É SÓ VARIEDADE: no leque de doze a criança pode ir
      tentando; na casinha ela tem de SABER. As duas portas continuam abertas —
      o teclado da tela e o de verdade (`abreCruz`). */
function escreveNum(box, pi, id, k, alvo, contaHTML, rot){
  var conta = el("div", "contafato");
  conta.innerHTML = contaHTML;
  var grade = el("div", "cruz uma"), cels = [], t;
  grade.setAttribute("data-qa", "esc-" + id);
  alvo = String(alvo);
  registra(id, pi, alvo);
  for(t = 0; t < alvo.length; t++){
    var c = el("button", "ccel viva" + (ST.resp[id] ? " ok" : ""),
               ST.resp[id] ? alvo.charAt(t) : "");
    c.setAttribute("aria-label", "Casa do resultado");
    cels.push(c); grade.appendChild(c);
  }
  conta.appendChild(grade);
  box.appendChild(conta);
  var E = {id: id, w: alvo, cels: cels, bt: grade, rot: rot,
           fc: "certo" + pi + "_" + k, dica: "dica" + pi + "_" + k};
  grade.onclick = function(){ if(!ST.resp[id]) abreCruz(E, pi); };
  cels.forEach(function(c2){
    c2.addEventListener("click", function(){ if(!ST.resp[id]) abreCruz(E, pi); });
  });
}

function folhaFato(d, pi, texto, comFrase){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var F = FATO[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = F.a / F.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg",
      "Reparta <b>" + F.a + " " + F.q + "</b> em <b>" + F.b + " " + F.w + "</b>."));
    lin.appendChild(botaoSom("Ouvir o problema", function(){ falar("ft" + pi + "_" + k); }));
    box.appendChild(lin);
    if(comFrase){
      var fr = el("div", "frasefato",
        "Em cada " + umSo(F.w) + " haverá <b>____</b> " + F.q + ".");
      box.appendChild(fr);
    }
    escreveNum(box, pi, id, k, r,
      '<span class="cf">' + F.a + '</span><span class="cf">&divide;</span>' +
      '<span class="cf">' + F.b + '</span><span class="cf">=</span>',
      "Escreva o resultado de " + F.a + " dividido por " + F.b);
    fechaItem(d, box, id);
  });
}
function f06(d, pi){
  folhaFato(d, pi, "Olhe o problema, termine a frase de cabeça e <b>escreva o " +
    "resultado</b> na conta. No computador dá para digitar.", 1);
}
function f07(d, pi){
  folhaFato(d, pi, "<b>Agora sem a frase de apoio</b>: só o problema e a conta. " +
    "Escreva o resultado.", 0);
}

/* ===== BLOCO D — OS PROBLEMAS DE REPARTIÇÃO (8 a 11) ===== */
/* ⭐ Da d03, d15, d17, d30 e d32. E o CAMPO `tipo` separa os dois significados
      que o currículo nomeia — o relatório do professor os mede em separado. */
function folhaProblema(d, pi, texto){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PROB[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = P.a / P.b;
    var lin = el("div", "enunlin");
    if(P.f) lin.appendChild(el("div", "figcx", img(P.f, "fig", "")));
    lin.appendChild(el("div", "perg", P.t));
    lin.appendChild(botaoSom("Ouvir o problema", function(){ falar("pb_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opNumeros("r" + r, 12), "r" + r, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f08(d, pi){
  folhaProblema(d, pi, "Leia (ou ouça) o problema e escolha <b>quantos ficam " +
    "para cada um</b>.");
}
function f09(d, pi){
  folhaProblema(d, pi, "Mesmos problemas, <b>agora com números maiores</b>. " +
    "Se travar, pense na tabuada ao contrário.");
}
function f10(d, pi){
  folhaProblema(d, pi, "<b>Agora quatro problemas seguidos.</b> Leia cada um " +
    "até o fim antes de escolher: o número grande nem sempre é o de repartir.");
}
function f11(d, pi){
  folhaProblema(d, pi, "Os últimos da repartição. <b>Todos perguntam a mesma " +
    "coisa</b>: quantos para cada um?");
}

/* ===== BLOCO E — ⭐ A DIVISÃO POR MEDIDA (12 a 15) ===== */
/* ⚠️⚠️ BLOCO DECLARADO, e é o maior buraco das quarenta folhas: **só UMA
      delas** (a d03) pergunta *"quantas caixas ela utilizou?"*. As outras
      trinta e nove perguntam sempre *"quantos para cada um?"*.
      O currículo pede os DOIS significados — *"repartição equitativa E DE
      MEDIDA"* —, e a criança que só viu o primeiro não reconhece o segundo
      como divisão: ela vê *"quantos cabem"* e pensa em subtrair.
   ⚠️ A CONTA É A MESMA E A PERGUNTA É OUTRA, e é isso que as folhas 12 a 15
      fazem a criança sentir: nas duas primeiras ela ENCHE os potes (o tamanho
      do pote é dado) e CONTA quantos usou. */
function f12(d, pi){
  reparte(d, pi, "⭐ <b>Agora é outra pergunta.</b> O tamanho do pote está dito: " +
    "encha um, depois outro, e veja <b>quantos potes você precisou</b>.", REP, 1);
}
function f13(d, pi){
  reparte(d, pi, "Mesma pergunta nova, <b>com mais peças</b>. Encha um pote de " +
    "cada vez, sem misturar.", REP, 1);
}
function f14(d, pi){
  folhaProblema(d, pi, "⭐ Agora só o problema escrito. Repare: ele <b>não " +
    "pergunta quantos para cada um</b> — pergunta <b>quantos grupos dão</b>. " +
    "A conta é a mesma.");
}
function f15(d, pi){
  folhaProblema(d, pi, "Os últimos de medida. <b>Leia com cuidado qual é a " +
    "pergunta</b>: ela mudou, e a conta não.");
}

/* ===== BLOCO F — A CONTA DE VOLTA (16 e 17) ===== */
/* ⭐⭐ A d23 manda, VERBATIM: *"Vamos fazer de acordo com o modelo:
      **5 × 3 = 15, então 15 ÷ 3 = 5**"*. O currículo nomeia: *"Compreender a
      ideia de operação inversa entre as operações de multiplicação e divisão."*
   ⚠️ A 16 MOSTRA A MULTIPLICAÇÃO E A 17 NÃO — é o degrau inteiro. */
function folhaInversa(d, pi, texto, mostra){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var I = INV[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var prod = I.x * I.y;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", mostra
      ? "<b>" + I.x + " &times; " + I.y + " = " + prod + "</b>, então " +
        prod + " &divide; " + I.y + " = ?"
      : prod + " &divide; " + I.y + " = ? <span class=\"sussurro\">(pense: " +
        "quantas vezes " + I.y + " cabe em " + prod + "?)</span>"));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar("iv" + pi + "_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opNumeros("r" + I.x, 10), "r" + I.x, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f16(d, pi){
  folhaInversa(d, pi, "⭐ <b>A conta de volta.</b> Se a multiplicação está aí em " +
    "cima, a divisão já está respondida — olhe bem.", 1);
}
function f17(d, pi){
  folhaInversa(d, pi, "<b>Agora sem a multiplicação à vista.</b> Pense: que " +
    "número vezes esse dá o total? Esse número é a resposta.", 0);
}

/* ===== BLOCO G — TREINAR (18 e 19) ===== */
/* ⚠️ `escreve` TROCA O GESTO, não o conteúdo: a folha 18 oferece o leque (e os
   cubinhos para contar), a 19 pede a conta escrita. É o degrau do apoio que
   some — e foi também o que tirou ESCOLHER de 49% para 37% das folhas, que o
   portão 0b7 cobrava com razão: *"as crianças me dizem 'isso eu já fiz, tô
   fazendo de novo'"* (Marcos). */
function folhaTreino(d, pi, texto, comFig, escreve){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CONTA[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = C.a / C.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", C.a + " &divide; " + C.b + " = ?"));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar("tr" + pi + "_" + k); }));
    box.appendChild(lin);
    if(comFig){
      var cx = el("div", "grupos"), g;
      for(g = 0; g < C.b; g++)
        cx.appendChild(el("div", "grupo", figs("dd3_cubinho.png", "cubinho", r)));
      box.appendChild(cx);
    }
    if(escreve)
      escreveNum(box, pi, id, k, r,
        '<span class="cf">' + C.a + '</span><span class="cf">&divide;</span>' +
        '<span class="cf">' + C.b + '</span><span class="cf">=</span>',
        "Escreva o resultado de " + C.a + " dividido por " + C.b);
    else
      opcoes(box, pi, id, opNumeros("r" + r, 12), "r" + r, "num",
             "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
}
function f18(d, pi){
  folhaTreino(d, pi, "Treino de contas, e <b>os cubinhos estão aí para contar</b> " +
    "se você quiser. Contar é uma estratégia, não é trapaça.", 1);
}
function f19(d, pi){
  folhaTreino(d, pi, "<b>Agora sem os cubinhos e sem a lista de números</b>: " +
    "a conta é sua. Use a tabuada ao contrário — que número vezes esse dá o " +
    "total? — e <b>escreva o resultado</b>.", 0, 1);
}

/* ===== BLOCO H — ⭐ O QUE SOBRA (20 a 23) ===== */
/* ⚠️⚠️ BLOCO DECLARADO. Trinta e seis das quarenta folhas só trazem divisão
      EXATA — e o currículo diz, com todas as letras, *"com resto zero **E COM
      RESTO DIFERENTE DE ZERO**"*. A criança que só viu conta exata acha que
      sobrar é ERRAR, e é o contrário: sobrar é a resposta.
   ⚠️ O NOME «RESTO» ENTRA porque o currículo o nomeia. «Dividendo» e «divisor»
      NÃO entram: não estão no texto do 3º ano, e dar quatro nomes técnicos a
      quem ainda está entendendo o gesto é trocar entendimento por vocabulário. */
function folhaResto(d, pi, texto, fonte, soSobra, escreve){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var R = fonte[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var q = Math.floor(R.a / R.b), s = R.a % R.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg",
      "<b>" + R.a + "</b> para <b>" + R.b + "</b>: " +
      (soSobra ? "quanto <b>sobra</b>?" : "quanto sobra?")));
    lin.appendChild(botaoSom("Ouvir a conta", function(){ falar("rs" + pi + "_" + k); }));
    box.appendChild(lin);
    if(R.f){
      var cx = el("div", "grupos"), g;
      for(g = 0; g < R.b; g++) cx.appendChild(el("div", "grupo", figs(R.f, "peça", q)));
      if(s) cx.appendChild(el("div", "grupo sobra", figs(R.f, "peça", s)));
      box.appendChild(cx);
    }
    if(escreve){
      escreveNum(box, pi, id, k, s,
        '<span class="cf">' + R.a + '</span><span class="cf">&divide;</span>' +
        '<span class="cf">' + R.b + '</span><span class="cf">sobra</span>',
        "Escreva quanto sobra de " + R.a + " dividido por " + R.b);
    } else {
      var lista = [], n;
      for(n = 0; n <= Math.max(9, R.b); n++)
        lista.push({v: "s" + n, rot: String(n), aria: String(n), fala: "num_" + n});
      opcoes(box, pi, id, lista, "s" + s, "num",
             "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    }
    fechaItem(d, box, id);
  });
}
function f20(d, pi){
  folhaResto(d, pi, "⭐ <b>Nem toda divisão fica certinha.</b> Reparta o que dá " +
    "e veja <b>o que sobra</b> — sobrar não é errar, é a resposta.", RESTO, 0);
}
function f21(d, pi){
  folhaResto(d, pi, "<b>Agora sem as figuras e sem a lista.</b> Reparta de cabeça " +
    "o máximo que der e <b>escreva o que sobrou</b>. Esse número tem nome: " +
    "<b>resto</b>.", RESTO, 1, 1);
}
/* ⭐⭐ A 22 MUDA DE GESTO, e a razão é da folha de papel: o comando impresso
   das folhas de resto é *"circule as divisões que não são exatas"* — marcar
   VÁRIAS de uma vez e conferir, não responder uma a uma. Era o verbo que
   faltava trazer do crivo (`_sequencias/POTE-DIV3.md`), e é também a folha em
   que a criança tem de decidir CADA conta antes de confirmar: quem chuta uma,
   erra a folha inteira e volta a olhar as seis.
   ⚠️ A FOLHA INTEIRA É UM ITEM SÓ — por isso o pote da 22 vai EMBRULHADO no
      `ITENS` (`[[...]]`): o `idsDaPagina` conta pelo tamanho do pote, e com
      seis itens soltos a folha se daria por pronta com uma marcação só. */
function f22(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "<b>Cuidado: metade destas fecha certinho e metade sobra.</b> " +
    "Marque <b>só as que sobram alguma coisa</b> e toque em Conferir.",
    "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(grupo, i){
    var id = "n" + pi + "_" + i, box = item(i + 1);
    var pecas = grupo.map(function(k){
      var R = RESTO[k];
      return {k: k, t: R.a + " ÷ " + R.b,
              aria: R.a + " dividido por " + R.b,
              ok: (R.a % R.b) !== 0,
              fala: function(){ falar("rs" + pi + "_" + k); }};
    });
    marqueConfira(box, id, pi, pecas, "certo22marca", "dica22marca");
    fechaItem(d, box, id);
  });
}
/* 23 — a trilha do resto, da d38 */
function f23(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Leve a chave até o cofre andando <b>só pelas casas em que a " +
    "conta SOBRA resto</b>. Em cada passo há três casas e só uma sobra.",
    "p" + pi + "enun");
  var tri = el("div", "trilha");
  ST.folha["p" + pi].forEach(function(k, i){
    var T = TRILHA[k], id = "n" + pi + "_" + i, certa = null;
    T.ops.forEach(function(o, j){ if(o.a % o.b) certa = "t" + j; });
    registra(id, pi, certa);
    var passo = el("div", "passo" + (ST.resp[id] ? " andado" : ""));
    passo.appendChild(el("div", "pnum", "passo " + (i + 1)));
    var cx = el("div", "sils");
    T.ops.forEach(function(o, j){
      var w = el("div", "opw");
      var sobra = o.a % o.b;
      var b = el("button", "sil larga" + (ST.resp[id] && sobra ? " ok" : ""),
                 o.a + " &divide; " + o.b);
      b.setAttribute("aria-label", o.a + " dividido por " + o.b);
      b.setAttribute("data-qa", (sobra ? "op-" : "no-") + id + "-t" + j);
      b.onclick = function(){
        if(ST.resp[id]) return;
        sPasso(); falar("conta_" + o.a + "_" + o.b);
        if(sobra){ b.className = "sil larga ok"; passo.className = "passo andado";
                   acertou(id, "certo" + pi + "_" + k); }
        else { b.className = "sil larga nao";
               setTimeout(function(){ b.className = "sil larga"; }, 420);
               errou(id, "dica" + pi + "_" + k); }
      };
      w.appendChild(b);
      w.appendChild(botaoSom("Ouvir esta conta",
        (function(oo){ return function(){ falar("conta_" + oo.a + "_" + oo.b); }; })(o),
        "som somop"));
      cx.appendChild(w);
    });
    passo.appendChild(cx);
    tri.appendChild(passo);
  });
  d.appendChild(tri);
  d.appendChild(el("div", "ajuda cent", "O cofre está no fim da trilha."));
}

/* ===== 24 — AQUECIMENTO ===== */
/* ⚠️ Única folha que repete um gesto fora do bloco, e é de propósito: revisão
   espaçada (Roediger, Bjork). O gesto é o da folha 1 e as contas são novas. */
function f24(d, pi){
  reparte(d, pi, "Uma parada para respirar: o gesto da <b>primeira folha</b>, com " +
    "contas novas. Arraste até os potes ficarem iguais.", REP);
}

/* ===== BLOCO I — PINTAR E DECIFRAR (25 a 27) ===== */
/* ⭐ Da d35 (*"Pinte a resposta correta de cada divisão"*) e da d37 (*"Resolva
      as divisões e descubra a mensagem"*). */
function folhaPintar(d, pi, texto){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  estojo(d, LEG);
  var cx = el("div", "sils");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PINT[k], id = "n" + pi + "_" + i;
    registra(id, pi, P.c);
    var w = el("div", "opw");
    var b = el("span", "sil larga", P.a + " &divide; " + P.b);
    b.setAttribute("aria-label", P.a + " dividido por " + P.b);
    pintavel(b, id, pi, P.c, "certo" + pi + "_" + k, "dica" + pi + "_" + k, null);
    w.appendChild(b);
    w.appendChild(botaoSom("Ouvir esta conta",
      (function(pp){ return function(){ falar("conta_" + pp.a + "_" + pp.b); }; })(P),
      "som somop"));
    cx.appendChild(w);
  });
  d.appendChild(cx);
  d.appendChild(el("div", "ajuda cent",
    "Pegue a canetinha do resultado ali em cima e depois toque na conta."));
}
function f25(d, pi){
  folhaPintar(d, pi, "Cada cor é um resultado. Pegue a canetinha e pinte as " +
    "contas que dão aquele número.");
}
function f26(d, pi){
  folhaPintar(d, pi, "<b>Agora com contas maiores</b>, e as mesmas quatro cores. " +
    "Se a conta não der nenhum desses números, confira outra vez.");
}
function f27(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Resolva cada conta e <b>a letra aparece</b>. No fim, a frase " +
    "se monta sozinha.", "p" + pi + "enun");
  var mural = el("div", "segredo");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = SEGREDO.contas[i], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = C.a / C.b;
    registra(id, pi, "r" + r);
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "perg", C.a + " &divide; " + C.b + " = ?"));
    lin.appendChild(botaoSom("Ouvir a conta",
      (function(cc){ return function(){ falar("conta_" + cc.a + "_" + cc.b); }; })(C)));
    box.appendChild(lin);
    var vaga = el("span", "letrasec" + (ST.resp[id] ? " cheia" : ""),
                  ST.resp[id] ? SEGREDO.letra[String(r)] : "?");
    mural.appendChild(vaga);
    opcoes(box, pi, id, opNumeros("r" + r, 10), "r" + r, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k, function(){
      vaga.className = "letrasec cheia";
      vaga.innerHTML = SEGREDO.letra[String(r)];
    });
    fechaItem(d, box, id);
  });
  d.appendChild(mural);
}

/* ===== BLOCO J — METADE, TERÇA E QUARTA PARTE (28 a 30) ===== */
/* ⚠️ BLOCO DECLARADO: o currículo pede *"Associar o quociente de uma divisão
      com resto zero por 2, 3, 4, 5 e 10 às ideias de metade, terça, quarta,
      quinta e décima partes"* — e só UMA das quarenta folhas (a d08) pede a
      METADE. As outras quatro ideias não aparecem em folha nenhuma. */
function folhaParte(d, pi, texto, escreve){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, texto, "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var P = PARTE[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = P.a / P.b;
    var lin = el("div", "enunlin");
    if(P.f) lin.appendChild(el("div", "figcx", img(P.f, "fig", "")));
    lin.appendChild(el("div", "perg",
      "Qual é a <b>" + P.nome + "</b> de <b>" + P.a + "</b>?"));
    lin.appendChild(botaoSom("Ouvir a pergunta", function(){ falar("pt_" + k); }));
    box.appendChild(lin);
    if(escreve){
      escreveNum(box, pi, id, k, r,
        '<span class="cf">' + P.a + '</span><span class="cf">&divide;</span>' +
        '<span class="cf">' + P.b + '</span><span class="cf">=</span>',
        "Escreva a " + P.nome.toLowerCase() + " de " + P.a);
      /* ⚠️ A EXPLICAÇÃO NÃO PRECISA DE GANCHO: o `nomeSecreto` só se revela
         quando o `acertou` marca `[data-nome=<id>]`, então ela pode ser
         montada agora e ficar escondida até a criança acertar. */
      var x = el("div", "ajuda cent");
      x.appendChild(nomeSecreto("A " + P.nome.toLowerCase() + " é dividir por " +
                                P.b + ": " + P.a + " ÷ " + P.b + " = " + r + ".", id));
      box.appendChild(x);
    } else {
      opcoes(box, pi, id, opNumeros("r" + r, 12), "r" + r, "num",
             "certo" + pi + "_" + k, "dica" + pi + "_" + k, function(){
        var y = el("div", "ajuda cent");
        y.appendChild(nomeSecreto("A " + P.nome.toLowerCase() + " é dividir por " +
                                  P.b + ": " + P.a + " ÷ " + P.b + " = " + r + ".", id));
        box.appendChild(y);
      });
    }
    fechaItem(d, box, id);
  });
}
function f28(d, pi){
  folhaParte(d, pi, "⭐ <b>Metade é dividir por 2.</b> É a mesma conta, com outro " +
    "nome — e este nome você vai ouvir a vida toda.");
}
function f29(d, pi){
  folhaParte(d, pi, "<b>Terça parte é dividir por 3; quarta parte, por 4.</b> " +
    "Repare no nome: ele já diz por quanto dividir.");
}
function f30(d, pi){
  folhaParte(d, pi, "<b>Quinta parte é por 5 e décima parte é por 10.</b> " +
    "Agora você sabe as cinco — e aqui <b>a resposta é escrita</b>, sem lista.",
    1);
}

/* ===== 31 — O QUEBRA-CABEÇA (da d05) ===== */
/* ⭐ VERBATIM: *"QUEBRA-CABEÇA DE DIVISÃO"*. A peça só encaixa se a conta
      fechar, e é isso que faz a criança conferir antes de largar. */
function f31(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Cada peça só encaixa no lugar do seu resultado. <b>Arraste a " +
    "conta até o número certo</b>, ou toque nos dois.", "p" + pi + "enun");
  var cols = el("div", "colunas"), listaC = [], usados = {};
  var pool = ST.folha["p" + pi];
  pool.forEach(function(k){ usados[PUZ[k].a / PUZ[k].b] = 1; });
  var nums = Object.keys(usados).sort(function(a, b){ return a - b; });
  nums.forEach(function(v){
    var c = el("div", "coluna");
    var t = el("div", "ctit", v);
    t.setAttribute("data-alvo", "1");
    c.setAttribute("data-qa", "alvo-gav" + pi + "_v" + v);
    c.appendChild(t);
    var dentro = el("div", "cdentro"); c.appendChild(dentro);
    c._v = "v" + v; c._dentro = dentro;
    listaC.push(c); cols.appendChild(c);
  });
  d.appendChild(cols);
  var banco = el("div", "figbanco"), marcada = null;
  pool.forEach(function(k, i){
    var P = PUZ[k], id = "n" + pi + "_" + i, v = "v" + (P.a / P.b);
    registra(id, pi, ">gav" + pi + "_" + v);
    var b = el("button", "op pal" + (ST.resp[id] ? " usada" : ""),
               P.a + " &divide; " + P.b);
    b.setAttribute("aria-label", P.a + " dividido por " + P.b);
    b.setAttribute("data-qa", "item-" + id);
    b.setAttribute("data-alvo", "1");
    if(ST.resp[id]) listaC.forEach(function(c){
      if(c._v === v) c._dentro.appendChild(el("span", "fdentro", P.a + " ÷ " + P.b));
    });
    function larga(col){
      if(ST.resp[id]) return;
      if(col._v === v){
        b.className = "op pal usada";
        col._dentro.appendChild(el("span", "fdentro", P.a + " ÷ " + P.b));
        if(marcada === b) marcada = null;
        acertou(id, "certo" + pi + "_" + k);
      } else {
        col.className = "coluna erro";
        setTimeout(function(){ col.className = "coluna"; }, 500);
        errou(id, "dica" + pi + "_" + k);
      }
    }
    b._larga = larga;
    b.onclick = function(){
      if(b._arrastou){ b._arrastou = false; return; }
      if(ST.resp[id]) return;
      sPasso(); falar("conta_" + P.a + "_" + P.b);
      if(marcada === b){ b.className = "op pal"; marcada = null; return; }
      if(marcada) marcada.className = "op pal";
      b.className = "op pal marcada"; marcada = b;
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

/* ===== 32 — A CRUZADINHA DOS RESULTADOS ===== */
function f32(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Resolva a conta da pista e <b>escreva o resultado por " +
    "extenso</b> na cruzadinha. No computador dá para digitar.", "p" + pi + "enun");
  cruzadinha(d, pi, CRZ, "crz_");
}

/* ===== 33 — A MEMÓRIA ===== */
/* ⚠️ CARTA GRANDE, regra permanente do Marcos. E o ITEM É O TABULEIRO INTEIRO,
      não o par: o `idsDaPagina` deduz o id da POSIÇÃO no pote. */
function f33(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Vire duas cartas e ache <b>a conta e o resultado dela</b>.",
    "p" + pi + "enun");
  var L = ST.folha["p" + pi];
  for(var g = 0; g < L.length; g++){
    (function(grupo, g2){
      var id = "n" + pi + "_" + g2, box = item(g2 + 1);
      var abertas = [], travado = false, faltam = grupo.length, k;
      registra(id, pi, grupo.join(" "));
      var lista = [];
      for(k = 0; k < grupo.length; k++) lista.push({k: grupo[k], lado: "conta"});
      for(k = grupo.length - 1; k >= 0; k--) lista.push({k: grupo[k], lado: "res"});
      var grade = el("div", "mcartas");
      lista.forEach(function(c){
        var M = MEM[c.k], feito = !!ST.resp[id];
        var txt = c.lado === "conta" ? (M.a + " ÷ " + M.b) : String(M.a / M.b);
        var ct = el("div", "mcarta" + (feito ? " achada" : ""));
        ct.setAttribute("data-qa", "mem-" + id + "-" + c.k + "-" + c.lado);
        ct.setAttribute("aria-label", feito ? esch(txt) : "carta virada para baixo");
        ct.innerHTML =
          '<div class="mgira">' +
            '<div class="mface mverso"><i class="mbrilho"></i><span class="minterro">?</span></div>' +
            '<div class="mface mfrente"><span class="mrot">' + esch(txt) + "</span></div>" +
          "</div>";
        ct.onclick = function(){
          if(travado || ST.resp[id] || ct.className.indexOf("achada") > -1 ||
             ct.className.indexOf("aberta") > -1) return;
          sTecla(); ct.className = "mcarta aberta";
          falar(c.lado === "conta" ? "conta_" + M.a + "_" + M.b
                                   : "num_" + (M.a / M.b));
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
    })(L[g], g);
  }
}

/* ===== 34 — ELABORAR UM PROBLEMA ===== */
/* ⭐ O currículo diz *"Resolver **E ELABORAR** problemas de divisão"*, e nenhuma
      das quarenta folhas manda a criança INVENTAR um. Aqui ela escolhe as
      peças do problema e o caderno o lê de volta para ela — e só então
      pergunta a resposta. */
function f34(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Agora é você quem faz o problema. <b>Escolha quantas peças e " +
    "quantos grupos</b>, e depois responda o seu próprio problema.",
    "p" + pi + "enun");
  ST.folha["p" + pi].forEach(function(k, i){
    var E = ELAB[k], id = "n" + pi + "_" + i, box = item(i + 1);
    var r = E.a / E.b;
    var lin = el("div", "enunlin");
    lin.appendChild(el("div", "figcx", img(E.f, "fig", E.q)));
    lin.appendChild(el("div", "perg",
      "O seu problema: <b>" + E.a + " " + E.q + "</b> para <b>" + E.b + " " +
      E.w + "</b>. Quantos para cada um?"));
    lin.appendChild(botaoSom("Ouvir o seu problema", function(){ falar("el_" + k); }));
    box.appendChild(lin);
    opcoes(box, pi, id, opNumeros("r" + r, 10), "r" + r, "num",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    fechaItem(d, box, id);
  });
  d.appendChild(el("div", "ajuda cent",
    "Conte este problema para alguém em casa e veja se a pessoa acerta."));
}

/* ===== 35 — O CARTAZ QUE A CRIANÇA LEVA ===== */
/* ⚠️ O FECHO É ALCANÇÁVEL A QUALQUER MOMENTO (regra da folha viva): não pede
      nada que as 34 anteriores não tenham ensinado, e não pede velocidade. */
function f35(d, pi){
  faixa(d, pi, NOMES[pi - 1]);
  enunciado(d, pi, "Este cartaz é seu. Em cada linha, escolha <b>o exemplo</b> " +
    "que cabe naquele nome — e leve os quatro na cabeça.", "p" + pi + "enun");
  var cx = el("div", "cartaz");
  ST.folha["p" + pi].forEach(function(k, i){
    var C = CARTAZ[k], id = "n" + pi + "_" + i;
    var lin = el("div", "cartlin");
    var tit = el("div", "cartit", "<b>" + C.n + "</b><span>" + C.d + "</span>");
    tit.appendChild(botaoSom("Ouvir", (function(kk){
      return function(){ falar("cartaz_" + kk); }; })(k)));
    lin.appendChild(tit);
    var box = el("div", "cartalvo");
    var ops = ["G1", "G2", "G3", "G4"].map(function(ck){
      return {v: ck, rot: CARTAZ[ck].ex, aria: CARTAZ[ck].ex, fala: "ex_" + ck};
    });
    opcoes(box, pi, id, ops, k, "pal frase",
           "certo" + pi + "_" + k, "dica" + pi + "_" + k);
    lin.appendChild(box);
    cx.appendChild(lin);
  });
  d.appendChild(cx);
  d.appendChild(el("div", "ajuda cent",
    "Pronto: agora você reparte, mede, sabe o que sobra e faz a conta de volta. " +
    "E fica a pergunta: <b>quantos dias tem a quarta parte de um mês de 28 dias?</b>"));
}
