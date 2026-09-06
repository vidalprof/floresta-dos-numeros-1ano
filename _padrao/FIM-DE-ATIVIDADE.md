# PADRAO DO FIM DE ATIVIDADE — colar em TODA atividade nova

> Decisao do Marcos (ago/2026): *"coloque isso para as novas que criarmos ja ter essas regras"*.
> **Nao e opcional.** Toda atividade premium nova nasce com as quatro coisas abaixo.
> O codigo aqui foi EXTRAIDO da Doceria do Cacau, ja rodando nas 4 atividades — copie, nao reescreva.

## O que toda atividade precisa ter no fim

1. **BOLETIM ANIMADO (a crianca ve).** Aparece sozinho na tela da medalha: estrelas que acendem
   uma a uma, barra que cresce por objetivo, acertos subindo contando com som, tempo trabalhado e
   uma frase de incentivo. **NUNCA mostra nota nem a palavra "errou"** — e a LEI do EduVerse (nao
   e prova disfarcada). O parecer seco fica so no relatorio do professor.
2. **RELATORIO DO PROFESSOR, invisivel para o aluno.** Sem botao na tela. Abre **segurando a
   medalha por 2 segundos**. (`?painel` no endereco continua valendo.) Pedido literal do Marcos:
   *"nao quero botao ou o painel do professor aparecendo para os alunos"*.
3. **PARECER EM PALAVRAS no relatorio.** Porcentagem nao serve para o diario. Cada objetivo sai
   como **Dominou / Esta construindo / Precisa retomar**, mais uma linha de resumo dizendo o que
   fazer ("pode seguir" / "vale retomar" / "recomendo repetir").
4. **TREINAR SO O QUE FALTOU.** Botao que aparece **apenas** para quem tem objetivo abaixo de 75%.
   Monta um percurso curto so com as fases dos objetivos fracos e volta para a medalha. Quem
   dominou tudo nao ve o botao e nao repete o que ja sabe — e isso que evita o enjoo.
5. **O QUE ELA FEZ, A VISTA (set/2026 — regra 11 da pesquisa, `JOGOS-EDUCACIONAIS-REFERENCIAS.md`
   §3, reconhecimento ENDOGENO).** Embaixo da medalha aparece a **galeria** do que a crianca
   produziu na atividade: a pintura, o desenho colorido, a letra tracada. Ja esta no motor
   (`ARTEFATOS` + `guardaArtefato(rotulo, dataURL)` + `.galeria` na `telaFim`) — a peca de
   producao so precisa CHAMAR `guardaArtefato` ao fechar (pintar-canvas, pintar-desenho e
   tracar-letra ja chamam; o `_qa/dinamicas.py` reprova peca de producao que nao chama).
   Atividade sem peca de producao nao mostra galeria nenhuma — nada de placeholder.
   ⚠️ canvas com figura de OUTRA origem (ou `file://` na bancada) e "manchado": o
   `toDataURL` estoura e a foto e pulada em silencio — por isso na banca a galeria so aparece
   com pintar-desenho/tracar-letra (SVG), e no ar aparece com as tres.

## Como colar (so 3 coisas mudam por atividade)

- **`ROTCRI`** — nome de cada objetivo em **linguagem de crianca**. O mapa `CONC*` do painel e
  linguagem de professor ("Formar grupos iguais (material manipulavel)") e nao serve no boletim.
- **`TREINO`** — objetivo -> **funcao da fase** que o treina. Descobrir assim:
  `grep -o 'reg("[a-z_]*"' arquivo.html` e ver em qual fase cada conceito e registrado.
- **`TELAFIM`** — a funcao da tela final daquela atividade (`dFim`, `telaFim`, `nFim`, ...).

### Armadilhas ja pagas (nao repetir)

- A funcao de salvar **muda de nome entre apps**: `salva()` no Doceria/Legenda/Redacao,
  `salvaEstado()` no Jardim. Conferir antes de colar o `proximoTreino`.
- O bloco inteiro entra **antes de `function pct(x)`** — ou seja, depois de todas as fases
  existirem. Se entrar antes, `TREINO` aponta para funcao ainda nao declarada.
- Atividade com **mais de uma missao** (Redacao) volta para o **menu**, nao para uma tela final.
- Na tela final: chamar **`resumoAnimado(c)`** logo antes do botao "Jogar de novo" e ligar
  **`segredoRelatorio(med)`** na imagem da medalha (guardar a imagem numa variavel primeiro,
  `var med=imgEl(...); c.appendChild(med); segredoRelatorio(med);`).
- A tela final fica **mais alta** com o boletim. Rodar `bash _qa/auditar.sh` depois de colar:
  ja aconteceu de a resposta cair atras da barra de baixo em janela baixa.
- O primeiro rascunho mostrou os **nomes internos** dos conceitos ("grupos", "vezes") porque o
  mapa do painel e uma variavel LOCAL do `telaPainel`. Por isso existe o `ROTCRI` global.

---

## 1) JS — boletim animado (a crianca ve)

```js
/* nomes em linguagem de crianca — ADAPTAR por atividade */
var ROTCRI={conceito1:"Nome que a crianca entende",conceito2:"Outro nome simples"};

/* ---------- BOLETIM ANIMADO DO FIM (para a CRIANCA ver) ----------
   Pedido do Marcos (ago/2026): "um final bem legal com animacoes mostrando o
   desempenho". Regra da casa: NUNCA e prova disfarcada — aqui nao existe nota
   nem "voce errou". Mostra o que ela APRENDEU, com estrela que acende uma a
   uma e barra que cresce. O parecer seco (Dominou / Precisa retomar) fica so
   no relatorio do professor, atras do gesto secreto.                        */
/* nomes em linguagem de crianca para o boletim do fim */
var ROTCRI={grupos:"Formar grupos iguais",soma:"Somar parcelas iguais",
  vezes:"Fazer a multiplica&#231;&#227;o",problema:"Resolver problemas",criar:"Criar o meu pedido"};
function resumoAnimado(pai){
  var R=(typeof ROTCRI!=="undefined")?ROTCRI:{};
  var cx=el("div","boletim");
  cx.appendChild(el("div","btit","O QUE VOC&#202; APRENDEU HOJE"));
  var k,barras=[],i=0;
  for(k in DOM){ if(!DOM.hasOwnProperty(k)) continue;
    var p=DOM[k]||0, n=(p>=0.75)?3:((p>=0.5)?2:1);
    var nome=String(R[k]||k).replace(/\s*\([^)]*\)/g,"");
    var ln=el("div","blin");
    var top=el("div","btop");
    top.appendChild(el("div","bnome",nome));
    var est=el("div","bestrelas"),s;
    for(s=0;s<3;s++){
      var e=el("i","estrela"+(s<n?" on":""));
      e.style.webkitAnimationDelay=(320+i*260+s*150)+"ms";
      e.style.animationDelay=(320+i*260+s*150)+"ms";
      est.appendChild(e);
    }
    top.appendChild(est); ln.appendChild(top);
    var bar=el("div","bbar"),fi=el("i"); bar.appendChild(fi); ln.appendChild(bar);
    barras.push([fi,Math.max(8,Math.round(p*100)),320+i*260]);
    cx.appendChild(ln); i++;
  }
  /* acertos subindo de 0 ate o total */
  var tot=MED.ev.length,acc=0,z;
  for(z=0;z<MED.ev.length;z++) acc+=MED.ev[z].ok;
  var mins=Math.max(1,Math.round(((new Date()).getTime()-MED.ini)/60000));
  var pl=el("div","bplacar","<b>0</b> acertos");
  cx.appendChild(pl);
  cx.appendChild(el("div","btempo","Voc&#234; trabalhou <b>"+mins+"</b> minuto"+(mins===1?"":"s")+" sem desistir."));
  var frase=(acc>=tot*0.8)?"Voc&#234; foi <b>muito bem</b> do come&#231;o ao fim!":
            ((acc>=tot*0.5)?"Voc&#234; <b>aprendeu bastante</b> hoje. Continua assim!":
                            "Voc&#234; <b>chegou at&#233; o fim</b>. Isso &#233; o que vale!");
  cx.appendChild(el("div","bfrase",frase));
  pai.appendChild(cx);
  /* as barras crescem depois de entrar na tela (senao nao anima) */
  setTimeout(function(){ var q;
    for(q=0;q<barras.length;q++){ (function(b){
      setTimeout(function(){ b[0].style.width=b[1]+"%"; },b[2]);
    })(barras[q]); }
  },60);
  /* o numero de acertos sobe contando */
  if(tot>0){ var v=0,pa=Math.max(28,Math.round(1400/Math.max(1,acc)));
    var tm=setInterval(function(){
      if(!cx.parentNode){ clearInterval(tm); return; }
      v++; if(v>acc){ clearInterval(tm); return; }
      pl.innerHTML="<b>"+v+"</b> acerto"+(v===1?"":"s");
      try{ tom(520+v*8,0.05,"triangle",0.07); }catch(e){}
    },pa);
  }
}
```

## 2) JS — treinar so o que faltou

```js
/* fases que treinam cada objetivo — ADAPTAR por atividade */
var TREINO={conceito1:faseQueTreina1,conceito2:faseQueTreina2};
function TELAFIM(){ nomeDaTelaFinalDestaAtividade(); }

/* ---------- TREINAR SO O QUE FALTOU ----------
   Pergunta do Marcos (ago/2026): "se ela nao domina, ela consegue fazer so as
   atividades que nao domina?". Da: o app ja mede cada objetivo (DOM). Aqui ele
   monta um percurso CURTO so com as fases dos objetivos fracos e volta para a
   medalha no fim. A crianca nao repete o que ja sabe — isso e o que mantem ela
   na tarefa em vez de enjoar.
   Truque para nao mexer em nenhuma fase: enquanto o treino roda, o mostraBanner
   ignora o "proximo" original e chama a proxima fase da fila.               */
var FILATREINO=null;
var _bannerOriginal=mostraBanner;
mostraBanner=function(msg,cb){ _bannerOriginal(msg, FILATREINO ? proximoTreino : cb); };
function fracos(){
  var k,out=[];
  for(k in DOM){ if(DOM.hasOwnProperty(k)&&(DOM[k]||0)<0.75&&TREINO[k]) out.push(k); }
  return out;
}
function proximoTreino(){
  if(!FILATREINO||!FILATREINO.length){ FILATREINO=null; salva(); TELAFIM(); return; }
  var f=FILATREINO.shift();
  try{ f(); }catch(e){ proximoTreino(); }
}
function treinarFracos(){
  var f=fracos(),i,fila=[];
  for(i=0;i<f.length;i++) fila.push(TREINO[f[i]]);
  if(!fila.length){ TELAFIM(); return; }
  FILATREINO=fila; proximoTreino();
}
```

## 3) JS — relatorio secreto + parecer em palavras

```js
/* ---------- RELATORIO DO FIM (so para o professor) ----------
   Pedido do Marcos (ago/2026): relatorio no fim da atividade, mas SEM botao e
   SEM o painel aparecendo para os alunos. Solucao: gesto discreto — segurar a
   MEDALHA por 2 segundos. Crianca nao descobre; o professor sabe.
   O ?painel no endereco continua funcionando.                                */
function segredoRelatorio(elm){
  if(!elm) return;
  var tmr=null;
  function comeca(){ if(tmr) clearTimeout(tmr);
    tmr=setTimeout(function(){ tmr=null; telaPainel(); },2000); }
  function para(){ if(tmr){ clearTimeout(tmr); tmr=null; } }
  elm.addEventListener("mousedown",comeca);
  elm.addEventListener("touchstart",comeca);
  elm.addEventListener("mouseup",para);
  elm.addEventListener("mouseleave",para);
  elm.addEventListener("touchend",para);
  elm.addEventListener("touchcancel",para);
}

/* parecer em PALAVRAS, nao so porcentagem — o professor precisa registrar isso
   no diario, e "72%" nao diz nada. (pedido do Marcos, ago/2026) */

function parecerDe(p){
  if(p>=0.75) return ["Dominou","dom"];
  if(p>=0.50) return ["Est&#225; construindo","cons"];
  return ["Precisa retomar","ret"];
}
/* ---------- BOLETIM ANIMADO DO FIM (para a CRIANCA ver) ----------
   Pedido do Marcos (ago/2026): "um final bem legal com animacoes mostrando o
   desempenho". Regra da casa: NUNCA e prova disfarcada — aqui nao existe nota
   nem "voce errou". Mostra o que ela APRENDEU, com estrela que acende uma a
   uma e barra que cresce. O parecer seco (Dominou / Precisa retomar) fica so
   no relatorio do professor, atras do gesto secreto.                        */
/* nomes em linguagem de crianca para o boletim do fim */
var ROTCRI={grupos:"Formar grupos iguais",soma:"Somar parcelas iguais",
  vezes:"Fazer a multiplica&#231;&#227;o",problema:"Resolver problemas",criar:"Criar o meu pedido"};
function resumoAnimado(pai){
  var R=(typeof ROTCRI!=="undefined")?ROTCRI:{};
  var cx=el("div","boletim");
  cx.appendChild(el("div","btit","O QUE VOC&#202; APRENDEU HOJE"));
  var k,barras=[],i=0;
  for(k in DOM){ if(!DOM.hasOwnProperty(k)) continue;
    var p=DOM[k]||0, n=(p>=0.75)?3:((p>=0.5)?2:1);
    var nome=String(R[k]||k).replace(/\s*\([^)]*\)/g,"");
    var ln=el("div","blin");
    var top=el("div","btop");
    top.appendChild(el("div","bnome",nome));
    var est=el("div","bestrelas"),s;
    for(s=0;s<3;s++){
      var e=el("i","estrela"+(s<n?" on":""));
      e.style.webkitAnimationDelay=(320+i*260+s*150)+"ms";
      e.style.animationDelay=(320+i*260+s*150)+"ms";
      est.appendChild(e);
    }
    top.appendChild(est); ln.appendChild(top);
    var bar=el("div","bbar"),fi=el("i"); bar.appendChild(fi); ln.appendChild(bar);
    barras.push([fi,Math.max(8,Math.round(p*100)),320+i*260]);
    cx.appendChild(ln); i++;
  }
  /* acertos subindo de 0 ate o total */
  var tot=MED.ev.length,acc=0,z;
  for(z=0;z<MED.ev.length;z++) acc+=MED.ev[z].ok;
  var mins=Math.max(1,Math.round(((new Date()).getTime()-MED.ini)/60000));
  var pl=el("div","bplacar","<b>0</b> acertos");
  cx.appendChild(pl);
  cx.appendChild(el("div","btempo","Voc&#234; trabalhou <b>"+mins+"</b> minuto"+(mins===1?"":"s")+" sem desistir."));
  var frase=(acc>=tot*0.8)?"Voc&#234; foi <b>muito bem</b> do come&#231;o ao fim!":
            ((acc>=tot*0.5)?"Voc&#234; <b>aprendeu bastante</b> hoje. Continua assim!":
                            "Voc&#234; <b>chegou at&#233; o fim</b>. Isso &#233; o que vale!");
  cx.appendChild(el("div","bfrase",frase));
  pai.appendChild(cx);
  /* as barras crescem depois de entrar na tela (senao nao anima) */
  setTimeout(function(){ var q;
    for(q=0;q<barras.length;q++){ (function(b){
      setTimeout(function(){ b[0].style.width=b[1]+"%"; },b[2]);
    })(barras[q]); }
  },60);
  /* o numero de acertos sobe contando */
  if(tot>0){ var v=0,pa=Math.max(28,Math.round(1400/Math.max(1,acc)));
    var tm=setInterval(function(){
      if(!cx.parentNode){ clearInterval(tm); return; }
      v++; if(v>acc){ clearInterval(tm); return; }
      pl.innerHTML="<b>"+v+"</b> acerto"+(v===1?"":"s");
      try{ tom(520+v*8,0.05,"triangle",0.07); }catch(e){}
    },pa);
  }
}
/* fases que treinam cada objetivo */
var TREINO={grupos:dMonta,soma:dSoma,vezes:dVezes,problema:dProblema,criar:dCria};
function TELAFIM(){ dFim(); }
/* ---------- TREINAR SO O QUE FALTOU ----------
   Pergunta do Marcos (ago/2026): "se ela nao domina, ela consegue fazer so as
   atividades que nao domina?". Da: o app ja mede cada objetivo (DOM). Aqui ele
   monta um percurso CURTO so com as fases dos objetivos fracos e volta para a
   medalha no fim. A crianca nao repete o que ja sabe — isso e o que mantem ela
   na tarefa em vez de enjoar.
   Truque para nao mexer em nenhuma fase: enquanto o treino roda, o mostraBanner
   ignora o "proximo" original e chama a proxima fase da fila.               */
var FILATREINO=null;
var _bannerOriginal=mostraBanner;
mostraBanner=function(msg,cb){ _bannerOriginal(msg, FILATREINO ? proximoTreino : cb); };
function fracos(){
  var k,out=[];
  for(k in DOM){ if(DOM.hasOwnProperty(k)&&(DOM[k]||0)<0.75&&TREINO[k]) out.push(k); }
  return out;
}
function proximoTreino(){
  if(!FILATREINO||!FILATREINO.length){ FILATREINO=null; salva(); TELAFIM(); return; }
  var f=FILATREINO.shift();
  try{ f(); }catch(e){ proximoTreino(); }
}
function treinarFracos(){
  var f=fracos(),i,fila=[];
  for(i=0;i<f.length;i++) fila.push(TREINO[f[i]]);
  if(!fila.length){ TELAFIM(); return; }
  FILATREINO=fila; proximoTreino();
}
function pct(x){return Math.round(x*100)+"%";}
```

## 4) CSS

```css
/* boletim animado do fim (a crianca ve) */
.boletim{background:rgba(255,253,244,.97);border:2px solid var(--linha);border-bottom-width:6px;
  border-radius:20px;padding:13px 15px;margin-top:12px;width:100%;max-width:360px;
  -webkit-box-shadow:0 8px 20px rgba(50,40,20,.26);box-shadow:0 8px 20px rgba(50,40,20,.26);
  -webkit-animation:sobe .5s both .15s;animation:sobe .5s both .15s}
@-webkit-keyframes sobe{from{opacity:0;-webkit-transform:translateY(16px)}to{opacity:1;-webkit-transform:none}}
@keyframes sobe{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.boletim .btit{font-size:12px;font-weight:800;letter-spacing:.6px;color:#6b6252;text-align:center;margin-bottom:9px}
.blin{margin-bottom:9px}
.btop{display:-webkit-box;display:-webkit-flex;display:flex;-webkit-box-align:center;align-items:center;
  -webkit-box-pack:justify;justify-content:space-between;gap:8px;margin-bottom:3px}
.bnome{font-size:13px;font-weight:700;color:#4a4232;text-align:left;line-height:1.2}
.bestrelas{display:-webkit-box;display:-webkit-flex;display:flex;gap:3px;-webkit-flex-shrink:0;flex-shrink:0}
.estrela{display:block;width:15px;height:15px;background:#ded6c2;
  -webkit-clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);
  clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}
.estrela.on{background:#eab000;-webkit-animation:estpop .45s both;animation:estpop .45s both}
@-webkit-keyframes estpop{0%{-webkit-transform:scale(.2) rotate(-40deg);opacity:0}
  70%{-webkit-transform:scale(1.35) rotate(6deg);opacity:1}100%{-webkit-transform:none;opacity:1}}
@keyframes estpop{0%{transform:scale(.2) rotate(-40deg);opacity:0}
  70%{transform:scale(1.35) rotate(6deg);opacity:1}100%{transform:none;opacity:1}}
.bbar{height:9px;background:#ece4d2;border-radius:999px;overflow:hidden}
.bbar i{display:block;height:100%;width:0;border-radius:999px;
  background:-webkit-linear-gradient(left,#8be05a,#2f8f18);background:linear-gradient(90deg,#8be05a,#2f8f18);
  -webkit-transition:width 1.1s cubic-bezier(.2,.9,.3,1);transition:width 1.1s cubic-bezier(.2,.9,.3,1)}
.bplacar{margin-top:10px;text-align:center;font-size:19px;font-weight:800;color:#4a4232}
.bplacar b{font-size:27px;color:#2f8f18}
.btempo{text-align:center;font-size:13px;font-weight:600;color:#6b6252;margin-top:2px}
.bfrase{text-align:center;font-size:14.5px;font-weight:700;color:#4a4232;margin-top:8px;line-height:1.3}
@media (max-height:600px){
  .boletim{padding:9px 11px;margin-top:8px;max-width:330px}
  .bnome{font-size:11.5px}.estrela{width:12px;height:12px}
  .bbar{height:7px}.blin{margin-bottom:6px}
  .bplacar{font-size:16px;margin-top:7px}.bplacar b{font-size:22px}
  .btempo{font-size:11.5px}.bfrase{font-size:12.5px;margin-top:6px}
}

.btntreino{margin-top:10px;border:0;cursor:pointer;font-family:inherit;font-weight:800;font-size:17px;
  color:#fff;padding:13px 22px;border-radius:999px;
  background:-webkit-linear-gradient(top,#3f9a26,#256113);background:linear-gradient(#3f9a26,#256113);
  -webkit-box-shadow:0 5px 0 #1b4a0c,0 10px 16px rgba(0,0,0,.25);box-shadow:0 5px 0 #1b4a0c,0 10px 16px rgba(0,0,0,.25)}
.btntreino small{display:block;font-size:12px;font-weight:600;opacity:.92;margin-top:2px}

.painel .dom{color:#1e6b10;font-weight:800}
.painel .cons{color:#8a6a00;font-weight:800}
.painel .ret{color:#a33020;font-weight:800}
.painel .resumo{background:#f2f7ea;border:2px solid #cfe0b8;border-radius:12px;padding:10px 12px;margin:10px 0;font-weight:600}
```

## 🏁 JOGO TAMBÉM TERMINA — e termina de verdade (regra do Marcos, ago/2026)

Palavras dele, no meio do tangram: *"os jogos precisam ter conclusão"*.

Não é o mesmo que "a última fase acaba". **Jogo sem conclusão é jogo que some**:
a criança monta a última figura e a tela simplesmente para, sem dizer que ela
chegou ao fim, sem medalha, sem nada para levar. Vale para JOGO exatamente como
vale para atividade — os quatro itens do fim continuam obrigatórios:

1. **boletim animado** para a criança (sem nota, sem a palavra "errou");
2. **medalha** e a frase que nomeia o que ela virou ("Mestre do Tangram");
3. **relatório do professor invisível para o aluno** (segurar a medalha 2 s);
4. **"Treinar o que faltou"** — e num jogo de uma mecânica só isso quer dizer
   **refazer a figura em que ela mais errou**, não ir para outra fase.

⚠️ E tem que ser TESTADO chegando lá: no tangram eu joguei até o fim por
programa (encaixando as sete peças) para ver o banner fechar e a tela final
abrir. Fim que ninguém percorreu é fim que ninguém viu.
