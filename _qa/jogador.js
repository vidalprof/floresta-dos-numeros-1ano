/* ============================================================
   AUDITOR JOGADOR — "da para terminar a atividade?"
   Joga a atividade CLICANDO AO ACASO, do comeco ao fim, e conta
   se chega na medalha. Pega o que print nenhum pega:
     - fase que TRAVA (a crianca fica presa para sempre);
     - fase ORFA (ninguem chega nela);
     - erro de JS no meio do caminho;
     - toque duplo que pula pergunta (foi assim que achamos o bug
       da Encomenda Rapida, ago/2026).
   ⚠️ Duas licoes de como ESTE auditor mente, se mal feito:
     1. `.click()` do Playwright IGNORA hit-test: ele clicava o botao
        do banner ESCONDIDO (fora da tela) e reiniciava a fase — falso
        "PRESO". Por isso filtra por getBoundingClientRect na viewport.
     2. a assinatura de estado precisa incluir a BARRA DE PROGRESSO:
        so o titulo da fase repete entre rodadas e parece travado.
   Uso: node _qa/jogador.js  (aponte o caminho no ARQUIVO abaixo)
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage({viewport:{width:412,height:820}});
 const erros=[];
 p.on('pageerror',e=>{erros.push(e.message);});
 await p.goto((process.argv[2]? 'file://'+require('path').resolve(process.argv[2]) : 'file:///home/user/floresta-dos-numeros-1ano/_doceria/index.html'));
 await p.waitForTimeout(600);
 // pula narracoes: falar() vira no-op
 await p.evaluate(()=>{ window.falar=function(){}; window.depoisDaFala=function(id,ms,cb){setTimeout(cb,120);}; });
 /* ⭐ COLHEITA DE VOZES (ago/2026). Enquanto ele joga, anota TODO texto que a
    crianca poderia tocar (`.opt/.pc/.lig/.bin`) e todo enunciado (`.balao`).
    Nasceu de uma cobranca do Marcos: *"lembre-se que nas respostas precisa do
    som para ajudar os estudantes que nao sabem ler"* — e a pergunta seguinte,
    *"verifique nas atividades do broto QUAIS nao tem o som nas respostas"*,
    nao tinha resposta possivel sem jogar a atividade inteira: as respostas de
    uma rodada so existem naquela rodada. Ler o codigo nao acha; jogar acha.
    Ligue com COLHEITA=<arquivo.json>. */
 if(process.env.COLHEITA) await p.evaluate(()=>{
   window.__colh={op:{},bal:{}};
   var SELC=".opt,.lig,.pc,.bin,.alim,.ficha,.pt,.gav,.carta,.rmc,.sic";
   function varre(){
     /* ⚠️ LICAO PAGA (ago/2026): a colheita trouxe a fala "Dcerto" — e nao
        existe fala nenhuma assim. A peca `escolher` CARIMBA a resposta acertada
        com um `<span class="marca">certo</span>` dentro da propria opcao; o
        colhedor lia a opcao DEPOIS do carimbo e juntava a letra "D" com o
        rotulo "certo". O alto-falante nunca diz isso (a chave dele e feita
        quando a opcao nasce), mas a fala ia para o falas.json e o Edge TTS
        gravaria "dêcerto" para ninguem ouvir.
        Carimbo de estado ("certo", "nao funcionou", "ja tentamos") e ROTULO,
        nao frase: sai da conta, como o `.zap` ja saia. */
     function limpo(e){
       /* ⚠️ LICAO PAGA (ago/2026, ingles 9o ano): a ficha da `montar-frase` de
          apoio junta a palavra com a ETIQUETA da classe ("Is"+"am/is/are"). O
          colhedor anotava "Isam/is/are" — uma frase-monstro que ia para a fila
          de gravacao. Quando a peca DECLARA a voz (`data-voz`), e ela que vale —
          a mesma regra que o motor (`poeZap`) e o portao (`vozresposta`) ja usam. */
       if(e.getAttribute && e.getAttribute("data-voz")) return e.getAttribute("data-voz");
       var c=e.cloneNode(true), i, fora=c.querySelectorAll(".marca,.fmarca,.zap,.zapb,.tent,.inmarca");
       for(i=0;i<fora.length;i++) if(fora[i].parentNode) fora[i].parentNode.removeChild(fora[i]);
       return (c.textContent||"").replace(/\s+/g," ").replace(/^ | $/g,"");
     }
     var i,e,t,a=document.querySelectorAll(SELC);
     for(i=0;i<a.length;i++){ e=a[i]; t=limpo(e);
       if(t&&t.length<90) window.__colh.op[t]=1; }
     a=document.getElementsByClassName("balao");
     for(i=0;i<a.length;i++){ t=(a[i].textContent||"").replace(/\s+/g," ").replace(/^ | $/g,"");
       if(t) window.__colh.bal[t]=1; }
   }
   varre();
   if(window.MutationObserver) new MutationObserver(varre).observe(
     document.getElementById("app"),{childList:true,subtree:true,characterData:true});
 });
 await p.evaluate((t)=>{ (window[t]||telaCapa)(); }, process.env.INICIO||'telaCapa');
 /* ⚡ JOGADOR PARALELO POR SEGMENTO (ago/2026, pedido do Marcos "paralelizar o
    jogador"): varios trabalhadores jogam TRECHOS diferentes ao mesmo tempo.
    JSTART = pula para a fase (abreFase); JSTOP = ao chegar nesta fase, o trecho
    fechou (sucesso). O ultimo trecho vai sem JSTOP e exige a MEDALHA. A uniao
    dos trechos cobre todas as fases; cada uma continua sendo jogada de verdade.
    Em modo serial (sem JSTART/JSTOP) NADA muda. */
 let segOk=false;
 if(process.env.JSTART){
   await p.evaluate((s)=>{ if(typeof abreFase==='function') abreFase(+s); }, process.env.JSTART);
   await p.waitForTimeout(350);
 }
 let visto=[]; const encaixe=[]; let ultimo='', paradas=0;
 /* ⭐ MODO "JOGAR CERTO" (ago/2026, a classe do "Monte o seu prato" que o Marcos
    pegou): o jogo ao ACASO e cego para CORRECAO — numa fase onde a opcao ERRADA
    esta declarada como certa, ou onde a regra de fechamento nao aceita a resposta
    declarada, o acaso ainda tropeca noutra saida e diz "jogavel". Aqui a garantia
    e outra: a peca de escolha PUBLICA a resposta que serve AGORA em `data-qa="1"`
    (a MESMA marca que ela ja usa por dentro — nao invento detector), o loop ja a
    prioriza (ramo generico, `return 2`), e o `data-qa` PERSISTE na opcao mesmo
    depois de tocada. Logo: se clicar a resposta DECLARADA certa NAO faz a fase
    andar, o estado CONGELA. Quando congela com o ultimo clique sendo o da resposta
    declarada, e contradicao entre a resposta do conteudo e a regra de fechamento —
    REPROVA, e mais rapido e mais preciso que esperar o "PRESO" generico (420).
    So a familia de escolha (escolher/completar/comparar/intruso/relampago/estimar/
    quem-sou-eu) chega ao `return 2`; as mecanicas que NAO expoem qual e a certa de
    forma legivel (memoria/ordenar/arrastar/...) tem solucionador proprio ANTES e
    retornam 1 — ficam de fora em silencio, como manda a ordem (cobrir bem as claras
    em vez de reprovar por engano). CUSTO: zero por iteracao (reusa `est`/`paradas`
    e o retorno do clique); so 1 evaluate barato na hora de reprovar. */
 let ultCerto=false, certoQuebrado=false;
 const LIMCERTO=70; /* ~16s frozen: bem acima da espera entre rodadas (rede de voz
    de 4s = ~20 iter), bem abaixo do PRESO generico (420 = ~96s). */
 /* ⚠️ LICAO PAGA (ago/2026): o "Proximo" que o Marcos pediu ("tem que ter o
    botao de proximo como no Broto") PRENDEU o auditor — ele nao sabia clica-lo
    e dava "PRESO em OUCA E ACHE [4%]" numa fase que a crianca passa sem
    dificuldade. Botao novo na atividade = seletor novo aqui, no MESMO commit.
    E o `.oaprox` vem PRIMEIRO na lista: quando ele esta na tela, e ele que faz
    a fase andar. */
 const SEL='.oaprox,#bcta,.btn,.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.pc,.peca,.dsolto,.marca,.moeda,.linhac,.qcel'+',.ferr,.vaso,.carta,.zona,.tec,.slot,.mcarta,.gfoto,.pal,.fichaP,.cx,.tlin,.vaga,.relcard,.alim,.rpos,.moeda'+',.pt,.plb,.fs,.errow,.gav,.ficha,.achado,.teclafc'
   /* ⚠️ mecanica nova = alvo novo AQUI. A rosa dos ventos (.vento) e a
      paleta de pintar (.tcor/.tinta) nasceram na cartografia e o jogador
      deu "PRESO" numa fase que funcionava: ele simplesmente nao enxergava
      onde tocar. Toda dinamica nova entra nesta lista no mesmo commit. */
   +',.vento,.tcor,.tinta,.palvo,.qcpc,.qcvaga,.seta'
   /* ⚠️⚠️ A RAIZ DE TODA ESTA FAMILIA (ago/2026): esta lista e de NOMES DE
      CLASSE das pecas — e o INTEGRADOR RENOMEIA as classes que colidem com o
      motor (`.seta` vira `lb_seta`, `.grade` vira `cp_grade`). Dentro da
      atividade montada o auditor deixava de enxergar onde tocar e dava
      "PRESO" em fases que a crianca fecha. Cada nome novo que eu acrescentava
      aqui resolvia UMA peca e deixava a proxima igual.
      O conserto que vale para todas: qualquer coisa que publique `data-qa` e
      alvo legitimo — e `data-qa` e justamente o que as pecas escrevem PARA o
      auditor. Nome de classe a fabrica troca; o `data-qa` nao. */
   +',[data-qa]'
   /* ⚠️ LICAO PAGA, e a MESMA de sempre (ago/2026): peca nova com CLASSE nova
      = seletor novo AQUI, no mesmo commit. As `caixas-de-som` nasceram com a
      classe `.cx` e o jogador as via; renomeei para `.csb` (porque `.cx` colide
      com a caixa de largar da ponte de estilo) e o portao passou a dizer
      "PRESO — a peca TRAVA". A peca estava perfeita: cego era o auditor.
      `.fichaq` entra junto — e por ela que se pega a ficha antes de empurrar. */
   +',.csb,.fichaq'
   /* Terra dos Papagaios (ago/2026): o marca-texto (`.pal`, a palavra dentro
      do paragrafo) e a lupa do mapa antigo (`.lupamira`) repetiram a mesma
      historia — fases que funcionam, auditor cego, "PRESO". A lista e o
      unico lugar onde isso se conserta. */
   +',.pal,.lupamira'
   /* juntar-silabas (ago/2026): a peca nova entra na lista NO MESMO COMMIT —
      sem isto o jogador nao enxerga onde tocar e da "PRESO" numa peca que
      funciona. Foi assim com a rosa dos ventos e com o marca-texto. */
   +',.jsSil,.jsVaga,.bsBatida,.bsPronto'
   /* rima (ago/2026): a carta do tabuleiro de rimas. Peca nova = alvo novo AQUI,
      no mesmo commit — mesma historia da rosa dos ventos e do marca-texto. */
   +',.rmc'
   /* som-inicial (ago/2026): a carta e a casa do som. Alvo novo no mesmo commit. */
   +',.sic,.sicasa';
 for(let i=0;i<5200;i++){
   const est=await p.evaluate(()=>{
     const s=document.querySelector('.selo'), h1=document.querySelector('h1');
     const bn=document.getElementById('banner');
     const pr=document.querySelector('.prog i');
     /* ⚠️ LICAO PAGA (ago/2026, esqueleto): a assinatura do estado so olhava o
        SELO e a barra da atividade — ou seja, so notava quando a FASE trocava.
        Numa fase longa com progresso de verdade (o jogo da memoria fechando
        par por par) ela ficava identica a uma tela congelada, e o auditor dava
        "PRESO" numa fase que a crianca fecha. Pior: era intermitente — passava
        quando a sorte do clique ao acaso ajudava, reprovava quando nao. Agora
        entra tambem o progresso DE DENTRO da fase, que so anda para a frente:
        quantas pecas ja estao resolvidas e a barrinha da propria mecanica.
        Sinal monotono nao esconde travamento: so zera o contador quem
        realmente avancou.                                                   */
     const feitos=document.querySelectorAll(
       '.par,.feito,.ok,.certo,.achou,.resolvido,.preenchida,.on,.sel').length;
     const pp=document.querySelector('.progpeca i');
     /* ⚠️ LICAO PAGA (ago/2026, no relampago da Oficina da Lina): fase que
        acaba PELO RELOGIO nao muda de estado enquanto a crianca joga — o
        placar pode ficar igual, e a tela e a mesma. O auditor contava as
        paradas e desistia gritando "PRESO" numa fase que termina sozinha,
        so porque ela dura mais que a paciencia dele. A barra de TEMPO
        (`.tbar i`) encolhe sem parar: pondo a largura dela no estado, o
        auditor enxerga que a fase esta ANDANDO e espera o fim. */
     const tb=document.querySelector('.tbar i');
     return ((s&&s.textContent)||(h1&&h1.textContent)||'?')
       +' ['+((pr&&pr.style.width)||'-')+']'
       +'{'+feitos+'/'+((pp&&pp.style.width)||'-')+'}'
       +(tb?'<'+Math.round(parseFloat(tb.style.width||'0'))+'>':'')
       +'|'+((bn&&bn.className.indexOf('show')>=0)?'BANNER':'');
   });
   if(est!==ultimo){ visto.push(i+' '+est.replace(/\{[^}]*\}/,'').replace(/<\d+>/,'')); ultimo=est; paradas=0; } else paradas++;
   /* ⭐ resposta DECLARADA certa nao fecha a fase: o ultimo clique foi na opcao
      marcada `data-qa="1"` (return 2) e o estado esta congelado ha LIMCERTO
      iteracoes. Reprova com o motivo exato ANTES do PRESO generico. */
   if(ultCerto && paradas>LIMCERTO){
     const info=await p.evaluate(()=>{
       var f=(typeof IFASE==='number')?IFASE:-1;
       var fs=(typeof FASES!=='undefined'&&FASES[f])?FASES[f]:null;
       return {f:f, mec:(fs&&fs.mec)||'?', selo:(fs&&fs.selo)||''};
     });
     const sel=String(info.selo).replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();
     visto.push(i+' >>> RESPOSTA DECLARADA CERTA NAO FECHOU: fase '+(info.f+1)
       +' ('+info.mec+(sel?' / '+sel:'')+') — clicar a resposta declarada certa'
       +' nao fechou a fase (resposta declarada != regra de fechamento)');
     certoQuebrado=true; break;
   }
   if(paradas>420){ visto.push('>>> PRESO em '+est); break; }
   /* fim do TRECHO paralelo: cheguei na fase-limite deste trabalhador */
   if(process.env.JSTOP){
     const fx=await p.evaluate(()=>typeof IFASE!=='undefined'?IFASE:-1);
     if(fx>=+process.env.JSTOP){ visto.push(i+' >>> SEGMENTO OK (ate a fase '+fx+')'); segOk=true; break; }
   }
   /* ⚠️ LICAO PAGA (ago/2026, Terra dos Papagaios): havia rolagem SO quando nao
      sobrava NADA clicavel na parte visivel. No porao do navio ficavam 4 fichas
      a vista e 2 abaixo da dobra: o jogador clicava eternamente nas 4 de cima,
      nunca via as outras duas, e reprovava uma fase que a crianca fecha rolando
      a tela com o dedo. Entao, quando o estado nao anda ha um tempo, ele ROLA —
      que e exatamente o que a crianca faz quando acha que ja tocou em tudo. */
   if(paradas&&paradas%60===0){
     await p.evaluate(()=>{
       const t=document.querySelector('.tela');
       if(!t||t.scrollHeight<=t.clientHeight+4) return;
       const fim=t.scrollTop+t.clientHeight>=t.scrollHeight-6;
       t.scrollTop = fim ? 0 : t.scrollTop+Math.round(t.clientHeight*0.5);
     });
   }
   const n=await p.evaluate((sel)=>{
     /* ⚠️ PRIORIDADE ao "Proximo": quando ele esta na tela, e ELE que faz a
        rodada andar — clicar em qualquer outra coisa nao muda nada, e o auditor
        conclui "PRESO" numa fase que a crianca passa sem dificuldade. Medido:
        com o botao, as rodadas andam 1 -> 2 -> 3 -> fim de fase. O mesmo
        tratamento que o `#bcta` do banner ja tinha. */
     /* o Proximo generico da ponte tem prioridade igual ao da peca */
     const px=document.querySelector('.pxprox,.oaprox');
     if(px&&px.offsetParent!==null){ px.click(); return 1; }
     const bn=document.getElementById('banner');
     if(bn&&bn.className.indexOf('show')>=0){ document.getElementById('bcta').click(); return 1; }
     /* caca-palavras: clicando ao acaso o jogador NUNCA acha (1a e ultima letra
        numa grade de 49 casas). A tela publica em data-qa onde cada palavra
        ficou, so para o auditor — assim ele confere de verdade que a fase
        termina e avanca, em vez de reprovar por burrice dele. */
     /* ⚠️⚠️ LICAO PAGA (ago/2026): este solucionador procurava `.grade[data-qa]`
        — e o INTEGRADOR RENOMEIA as classes que colidem com o motor, entao na
        atividade montada a grade se chama `cp_grade`. O auditor ficava cego
        justo na mecanica que ele so consegue jogar com a ajuda do `data-qa`, e
        dava "PRESO" numa fase que a crianca fecha. Ninguem tinha notado porque
        ele parava antes, na 3a fase.
        Regra que fica: procurar pelo CONTEUDO do `data-qa` (o JSON das
        posicoes), nunca pelo nome da classe — nome de classe a fabrica troca. */
     const _todas=[].slice.call(document.querySelectorAll('[data-qa]')).filter(
       e=>e.offsetParent!==null && e.children.length>=8);
     const g=_todas.filter(e=>/^\{/.test(e.getAttribute('data-qa')||''))[0]
          || _todas.filter(e=>/^\d+$/.test(e.getAttribute('data-qa')||''))[0]
          || document.querySelector('.grade[data-qa]');
     /* quadro de numeros (ache o total): o data-qa e SO um numero — clicar ao
        acaso numa grade de 36 quase nunca acha. */
     if(g&&g.offsetParent!==null&&/^\d+$/.test(g.getAttribute('data-qa')||'')){
       const alvo=g.getAttribute('data-qa');
       const c=[...g.children].find(e=>e.textContent.trim()===alvo&&e.className.indexOf('ok')<0);
       if(c){ c.click(); return 1; }
     }
     if(g&&g.offsetParent!==null){
       const pos=JSON.parse(g.getAttribute('data-qa'));
       const falta=[...document.querySelectorAll('.pchip')].filter(c=>c.className.indexOf('feito')<0);
       if(falta.length){
         /* ⚠️ MODO DEFINICOES (ago/2026, vindo do EdiLIM): o chip pode mostrar a
            PISTA em vez da palavra ("Amarelinho, em fileiras na espiga..."). Lendo
            o texto, o auditor procurava essa frase no mapa das posicoes, nao achava
            e dava "PRESO" numa fase que a crianca fecha. O chip publica a palavra
            em `data-qa` SO para o auditor; o texto continua valendo no modo lista. */
         const chave=(falta[0].getAttribute('data-qa')||falta[0].textContent||'').trim();
         const d=pos[chave];
         if(d){
           const N=Math.round(Math.sqrt(g.children.length));
           /* ⚠️ EXISTEM DOIS MOLDES DE CACA-PALAVRAS NA CASA, e o auditor tem
              que servir aos dois (ago/2026):
                (a) por EXTREMOS — toca na 1a letra, ela fica "sel", e a 2a
                    fecha a palavra (Maquina do Tempo);
                (b) LETRA POR LETRA — cada letra vira "mark" e a fase confere
                    quando todas estao marcadas (cartografia).
              Trocar um pelo outro reprova uma fase que funciona. Entao: toca na
              primeira e PERGUNTA a tela em qual molde ela esta.              */
           /* ⚠️ TERCEIRO MOLDE, ago/2026: a DIAGONAL. O Marcos pediu que o
              caca-palavras tivesse palavras na diagonal; a fase publica o passo
              em `dl`/`dc`, mas o auditor so sabia somar na linha OU na coluna e
              ficava clicando as celulas erradas para sempre — "PRESO em
              CACA-PALAVRAS DO MAR" numa fase que a crianca fecha. Portao que
              nao conhece a mecanica nova reprova o que funciona, e isso e pior
              que portao nenhum: faz a gente desconfiar do certo.              */
           const dl = (typeof d.dl==='number') ? d.dl : (d.h?0:1);
           const dc = (typeof d.dc==='number') ? d.dc : (d.h?1:0);
           const prim=g.children[d.r*N+d.c];
           const r2=d.r+dl*(d.n-1), c2=d.c+dc*(d.n-1);
           if(prim.className.indexOf('sel')<0&&prim.className.indexOf('mark')<0) prim.click();
           if(prim.className.indexOf('sel')>=0){ g.children[r2*N+c2].click(); return 1; }
           let tocou=false;
           for(let k=1;k<d.n;k++){
             const rr=d.r+dl*k, cc=d.c+dc*k;
             const cel=g.children[rr*N+cc];
             if(cel&&cel.className.indexOf('ok')<0&&cel.className.indexOf('mark')<0){ cel.click(); tocou=true; }
           }
           /* ⚠️ palavras que se CRUZAM: as letras desta ja podiam estar marcadas
              por causa da palavra anterior. Ai o jogador nao clicava em nada, a
              tela nao mudava, e ele dava "PRESO" numa fase que a crianca fecha
              sem esforco. Nesse caso desmarca e remarca a ultima letra, so para
              a tela refazer a conferencia. */
           if(!tocou){
             const rz=d.r+dl*(d.n-1), cz=d.c+dc*(d.n-1);
             const ult=g.children[rz*N+cz];
             if(ult&&ult.className.indexOf('ok')<0){ ult.click(); ult.click(); }
           }
           return 1;
         }
       }
     }
     /* levar-o-item-ate-o-lugar (arrastar OU tocar): peca e destino publicam o
        mesmo valor em data-qa. O jogador usa o caminho do TOQUE (peca, depois
        destino), que e o que a crianca sem arrasto usa. */
     /* ⚠️ LICAO PAGA (ago/2026, cartografia): nem toda .pc e peca de arrastar.
        No roteiro de setas a .pc e um BOTAO de acao, e a tela publica em
        data-qa="1" qual serve AGORA. O jogador pegava sempre a PRIMEIRA da
        ordem do DOM, clicava na seta errada para sempre e dava "preso" numa
        fase que funciona. Agora, quando ha uma marcada, e nela que ele toca. */
     const pcs=[...document.querySelectorAll('.pc[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('usada')<0);
     const peca=pcs.find(e=>e.getAttribute('data-qa')==='1')||pcs[0];
     if(peca){
       if(peca.className.indexOf('sel')<0){ peca.click(); return 1; }
       const dest=[...document.querySelectorAll('.cam[data-qa]')].find(e=>e.getAttribute('data-qa')===peca.getAttribute('data-qa')&&e.className.indexOf('ok')<0);
       if(dest){ dest.click(); return 1; }
     }
     /* LIGAR (duas colunas): os dois lados publicam a MESMA chave em data-qa
        (`p0`, `p1`...). Sem esta parte o jogador tocava ao acaso de um lado e do
        outro e, no molde do 4o ano, ficava PRESO: la o lado direito publicava o
        numero cru do par, e o `data-qa="1"` batia com a convencao "1 = serve
        agora" — ele tocava eternamente no mesmo. Aqui ele faz o que a crianca
        faz: escolhe um da esquerda e procura o par dele na direita. */
     const ligs=[...document.querySelectorAll('.lig[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('feita')<0&&e.className.indexOf('ok')<0);
     if(ligs.length>1){
       const sel=ligs.find(e=>e.className.indexOf('sel')>=0);
       if(!sel){ ligs[0].click(); return 1; }
       const par=ligs.find(e=>e!==sel&&e.getAttribute('data-qa')===sel.getAttribute('data-qa'));
       if(par){ par.click(); return 1; }
     }
     /* SOM INICIAL (a casa do som): a carta `.sic` publica em data-qa a casa
        certa, e a casa `.sicasa` publica a mesma chave. E o "levar ao lugar" por
        toque: toca na carta e depois na casa. Peca nova = solucionador novo AQUI,
        no mesmo commit. */
     const sics=[...document.querySelectorAll('.sic[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('usada')<0);
     if(sics.length){
       const sc=sics[0];
       if(sc.className.indexOf('sel')<0){ sc.click(); return 1; }
       const casa=[...document.querySelectorAll('.sicasa[data-qa]')]
         .find(e=>e.getAttribute('data-qa')===sc.getAttribute('data-qa'));
       if(casa){ casa.click(); return 1; }
     }
     /* RIMA (tabuleiro de cartas viradas): mesmo par por data-qa que o LIGAR, so
        que num tabuleiro so (`.rmc`). Peca nova = solucionador novo AQUI, no
        mesmo commit — senao o jogador toca ao acaso e da "PRESO" numa fase que
        a crianca fecha. */
     const rms=[...document.querySelectorAll('.rmc[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('feita')<0);
     if(rms.length>1){
       const sel=rms.find(e=>e.className.indexOf('sel')>=0);
       if(!sel){ rms[0].click(); return 1; }
       const par=rms.find(e=>e!==sel&&e.getAttribute('data-qa')===sel.getAttribute('data-qa'));
       if(par){ par.click(); return 1; }
     }
     /* a mesma ideia com .peca -> linha de destino que publica data-vaga
        (e o molde de "monte a legenda"): toca na peca e depois na linha certa. */
     const pcs2=[...document.querySelectorAll('.peca[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('usada')<0);
     const pe2=pcs2.find(e=>e.getAttribute('data-qa')==='1')||pcs2[0];
     if(pe2){
       if(pe2.className.indexOf('sel')<0){ pe2.click(); return 1; }
       const d2=[...document.querySelectorAll('[data-vaga]')]
         .find(e=>e.getAttribute('data-vaga')===pe2.getAttribute('data-qa')&&e.className.indexOf('cheia')<0);
       if(d2){ d2.click(); return 1; }
     }
     /* DESLIZAR (simulador): o jogador nao sabe arrastar um controle. A tela
        publica em data-qa o valor que a fase espera. Algumas fases (a janela do
        tempo) so liberam quando a crianca VIU todas as posicoes, entao aqui ele
        percorre uma por uma, do menor ate o alvo, disparando 'input' em cada. */
     const rg=[...document.querySelectorAll('input[type=range][data-qa]')]
       .find(e=>e.offsetParent!==null);
     if(rg){
       const alvoV=parseInt(rg.getAttribute('data-qa'),10);
       const mn=parseInt(rg.min||'0',10), mx=parseInt(rg.max||'0',10);
       const at=parseInt(rg.value,10);
       if(rg._passo===undefined) rg._passo=mn;
       if(rg._passo<=mx){
         /* percorre TODAS as posicoes, do menor ao maior. Ir so "um passo para
            o lado" ficava indo e voltando entre as duas ultimas e nunca via a
            primeira — a fase exige ter visto todas. */
         rg.value=''+rg._passo; rg._passo++;
         rg.dispatchEvent(new Event('input',{bubbles:true}));
         return 1;
       }
       if(at!==alvoV){ rg.value=''+alvoV; rg.dispatchEvent(new Event('input',{bubbles:true})); return 1; }
     }
     /* producao escrita: o jogador nao sabe redigir. A tela publica em data-qa
        uma resposta que serve, so para o auditor conferir que o botao aceita e
        a fase avanca. */
     const ip=document.querySelector('input[data-qa]:not([type=range]),textarea[data-qa]');
     if(ip&&ip.offsetParent!==null){
       if(ip.value!==ip.getAttribute('data-qa')){
         ip.value=ip.getAttribute('data-qa');
         ip.dispatchEvent(new Event('input',{bubbles:true}));
         return 1;
       }
     }
     /* monte a palavra: as letras estao embaralhadas e so valem NA ORDEM. No
        acaso o jogador nunca escreve ESTRELA. A tela publica a palavra da vez
        em data-qa, so para o auditor. */
     const lt=document.querySelector('.letras[data-qa]');
     if(lt&&lt.offsetParent!==null){
       const pal=lt.getAttribute('data-qa')||'';
       const tec=[...lt.children];
       const passo=tec.filter(b=>b.className.indexOf('usada')>=0).length;
       if(passo<pal.length){
         const alvo=tec.find(b=>b.className.indexOf('usada')<0&&b.textContent.trim()===pal.charAt(passo));
         if(alvo){ alvo.click(); return 1; }
       }
     }
     /* digitar-numero (calcular e digitar o resultado): o teclado numerico
        publica a RESPOSTA em data-qa, so para o auditor. Bate digito por
        digito, na ORDEM — o passo e quantas VAGAS ja estao cheias, nao da para
        contar tecla "usada" (a mesma tecla serve dois digitos, tipo o "5" de
        55). Cada digito certo preenche uma vaga; ao completar, a peca confere e
        avanca sozinha. */
     const nt=document.querySelector('.numtecs[data-qa]');
     if(nt&&nt.offsetParent!==null){
       const rp=nt.getAttribute('data-qa')||'';
       const feitas=document.querySelectorAll('.dnvagas .vaga.cheia').length;
       if(feitas<rp.length){
         const alvo=[...nt.children].find(b=>b.textContent.trim()===rp.charAt(feitas));
         if(alvo){ alvo.click(); return 1; }
       }
     }
     /* ⚠️ o botao do banner (#bcta) fica SEMPRE no DOM: o banner se esconde por
        transform, nao por display, entao offsetParent nao e null. Fora do banner
        aberto ele guarda o onclick do banner ANTERIOR — clicar nele jogava o
        jogador de volta para a fase passada, em loop. So vale quando o banner
        esta aberto (classe show). */
     const els=[...document.querySelectorAll(sel)].filter(e=>{
       if(e.offsetParent===null) return false;
       /* campo de texto nunca faz a fase andar — e o teclado que faz. A carta do
          Vale usava a classe .carta (a mesma das cartas do Orbi) e o jogador
          ficava clicando no campo em vez de apertar Enviar. */
       if(e.tagName==='TEXTAREA'||e.tagName==='INPUT') return false;
       if(e.id==='bcta'){ const bn=document.getElementById('banner');
         if(!bn||bn.className.indexOf('show')<0) return false; }
       const r=e.getBoundingClientRect();
       return r.width>0&&r.top<innerHeight&&r.bottom>0;});
     if(!els.length){
       /* nada clicavel NA PARTE VISIVEL — mas pode haver logo abaixo. Uma
          crianca rolaria a tela; o jogador nao rolava, e dava "preso" numa fase
          que funciona (a carta do Vale: o botao Enviar fica abaixo da dobra).
          Entao rola e tenta de novo; se ja estiver no fim, volta ao topo. */
       const tela=document.querySelector('.tela');
       if(tela&&tela.scrollHeight>tela.clientHeight+4){
         const fim=tela.scrollTop+tela.clientHeight>=tela.scrollHeight-6;
         tela.scrollTop = fim ? 0 : tela.scrollTop+Math.round(tela.clientHeight*0.6);
         return 1;
       }
       return 0;
     }
     /* quebra-cabeca: a peca publica em data-qa a POSICAO dela (li_co) e a vaga
        publica a mesma coisa em data-vaga. E o mesmo par do "levar ate o lugar",
        so que com classe propria — sem isto o jogador ficava tocando na peca e
        nunca na vaga, e dava PRESO numa fase que funciona. */
     const qp=[...document.querySelectorAll('.qcpc[data-qa]')]
       .filter(e=>e.offsetParent!==null&&e.className.indexOf('usada')<0);
     if(qp.length){
       const pe=qp[0]; pe.click();
       const dv=[...document.querySelectorAll('.qcvaga[data-vaga]')]
         .find(e=>e.getAttribute('data-vaga')===pe.getAttribute('data-qa')&&e.className.indexOf('cheia')<0);
       if(dv){ dv.click(); return 1; }
     }
     /* passo-a-passo (ordenar a receita): a vaga publica data-vaga INTEIRO (1..N)
        = a posicao certa, e a fonte publica o MESMO numero em data-qa. Distingue
        do quebra-cabeca, cujo data-vaga e "li_co" (tem "_"). O jogo e por PARES
        toque->vaga (fonte, depois a vaga vazia), e no fim o botao "Comecar".
        So atributos de dado (nao classe): o integrador renomeia .cam, nao o
        data-vaga. Sem isto o jogador clicava ao acaso, a ordem saia errada e ele
        ficava em LACO ate o timeout (defeito do proprio auditor, ago/2026). */
     const ppV=[...document.querySelectorAll('[data-vaga]')]
       .filter(v=>/^\d+$/.test(v.getAttribute('data-vaga')||'')&&v.offsetParent!==null);
     if(ppV.length){
       const vazia=ppV.find(v=>!v.querySelector('.pc'));
       if(vazia){
         const pos=vazia.getAttribute('data-vaga');
         const fonte=[...document.querySelectorAll('[data-qa]')].find(s=>
           s.getAttribute('data-qa')===pos&&!s.hasAttribute('data-vaga')&&
           s.tagName!=='BUTTON'&&s.offsetParent!==null);
         if(fonte){ fonte.click(); vazia.click(); return 1; }
       }
       const bcomeca=[...document.querySelectorAll('button[data-qa]')]
         .find(x=>x.offsetParent!==null);
       if(bcomeca){ bcomeca.click(); return 1; }
     }
     /* ⚠️ a tela publica em data-qa="1" a resposta que serve AGORA (so para o
        auditor). Escolher SEMPRE ao acaso deixava a partida na sorte: num quiz
        de 3 opcoes ele as vezes rodava os 420 giros sem fechar a rodada e
        reprovava uma fase perfeita — ainda mais quando os outros portoes
        estavam disputando o processador. Se ha resposta marcada, e nela que
        ele toca; no resto continua ao acaso, que e o teste honesto.        */
     const marcado=els.find(e=>e.getAttribute&&e.getAttribute('data-qa')==='1');
     /* ⭐ resposta DECLARADA certa (data-qa="1") -> clica ELA e avisa (return 2),
        para o portao acima poder cobrar que fechou a fase. So no acaso quando a
        peca nao declara resposta (botao "continuar", etc.). */
     if(marcado){ marcado.click(); return 2; }
     const e=els[Math.floor(Math.random()*els.length)];
     e.click(); return 1;
   },SEL);
   ultCerto=(n===2);
   await p.waitForTimeout(230);
   /* ⚠️ FIGURA MAIOR QUE O LUGAR DELA — e so DEPOIS de jogar que da para ver.
      A planta da sala so mostra os moveis quando a crianca ja os colocou; o
      auditor de leiaute abre a fase VAZIA e aprova, e o defeito (a lousa
      gigante em cima do desenho, foto do Marcos ago/2026) passa batido. Aqui,
      que e o unico portao que chega ao estado final de cada fase, a conta e
      barata: toda <img> dentro de um pai posicionado tem que caber nele.   */
   const estouro=await p.evaluate(()=>{
     const fora=[];
     for(const im of document.querySelectorAll('img')){
       if(im.offsetParent===null) continue;
       /* ⚠️ LICAO PAGA (Museu, ago/2026): este check dava reprova FALSA e FLAKY no
          jogador PARALELO. Estado PASSAGEIRO nao vale: (a) imagem ainda CARREGANDO
          (naturalWidth 0) mede um retangulo qualquer; (b) carta em ANIMACAO
          (scale 1.08 do `clchega`/`clcaiu`/virada) estoura o pai por um instante;
          (c) a marca d'agua `.gwater` (o portao encaixe.js ja a ignora). Fora da
          conta — o defeito REAL (lousa gigante em cima do desenho) e PERSISTENTE,
          nao some no quadro seguinte. */
       if(!im.complete || !im.naturalWidth) continue;
       if(im.closest && im.closest('.gwater')) continue;
       const ci=getComputedStyle(im);
       if(ci.transform && ci.transform!=='none') continue;
       const pai=im.parentElement; if(!pai) continue;
       const ps=getComputedStyle(pai);
       if(ps.position!=='absolute'&&ps.position!=='relative') continue;
       if(ps.overflow==='hidden') continue;
       if(ps.transform && ps.transform!=='none') continue;
       const a=im.getBoundingClientRect(), b=pai.getBoundingClientRect();
       if(!b.width||!b.height) continue;
       if(a.width>b.width*1.15||a.height>b.height*1.15)
         fora.push('.'+String(im.className||'img').split(' ')[0]+' '+Math.round(a.width)+'x'+Math.round(a.height)
                   +' dentro de .'+String(pai.className).split(' ')[0]+' '+Math.round(b.width)+'x'+Math.round(b.height));
     }
     return fora;
   });
   for(const e of estouro) if(encaixe.indexOf(e)<0) encaixe.push(e);
   /* ⚠️⚠️ LICAO PAGA (ago/2026), e das piores desta serie inteira: este portao
      existe para JOGAR A ATIVIDADE ATE A MEDALHA, e ele parava na TERCEIRA
      FASE de trinta e duas — dizendo "CHEGOU NO FIM", com codigo 0.
      Motivo: cada peca do catalogo e uma mini-atividade que termina na propria
      medalha (`div.medal`), e dentro da atividade montada essa tela vira o
      FECHO DA FASE — bonita, correta, com o gancho de curiosidade. O portao
      via a classe `medal`, dava a partida por encerrada, e as 29 fases
      seguintes NUNCA foram jogadas por ninguem. Todas as atividades montadas
      passaram assim.
      A medalha DA ATIVIDADE e outra coisa: e a imagem que o motor poe
      (`imgEl("med_"+ID.pre,"medal")`). Entao, quando ha motor de fases, so ela
      encerra a partida; sem motor (a bancada da peca avulsa), qualquer
      `.medal` vale, como sempre valeu. */
   {
     const acabou = await p.evaluate(()=>{
       var m=[].slice.call(document.querySelectorAll('.medal')).filter(function(e){
         return e.offsetParent!==null; });
       if(!m.length) return false;
       var temMotor = (typeof FASES!=='undefined' && typeof montaFase==='function');
       if(!temMotor) return true;
       for(var i=0;i<m.length;i++)
         if(m[i].tagName==='IMG' && /med_/.test(m[i].getAttribute('src')||'')) return true;
       return false;
     });
     if(acabou){ visto.push(i+' >>> CHEGOU NO FIM'); break; }
   }
 }
 if(process.env.COLHEITA){
   const c=await p.evaluate(()=>window.__colh||{op:{},bal:{}});
   const antes=require('fs').existsSync(process.env.COLHEITA)
     ? JSON.parse(require('fs').readFileSync(process.env.COLHEITA,'utf8')) : {op:{},bal:{}};
   for(const k in c.op) antes.op[k]=1;
   for(const k in c.bal) antes.bal[k]=1;
   require('fs').writeFileSync(process.env.COLHEITA,JSON.stringify(antes,null,1));
   console.log('COLHEITA: '+Object.keys(antes.op).length+' resposta(s) e '
               +Object.keys(antes.bal).length+' enunciado(s) vistos ate agora');
 }
 console.log(visto.join('\n'));
 /* o barulho do file:// nao conta: service worker so existe em http(s) */
 const reais=erros.filter(e=>!/ServiceWorker|protocol of the current origin/i.test(e));
 console.log('ERROS JS:', reais.length? reais.slice(0,8).join(' || '):'nenhum');
 if(encaixe.length){
   console.log('  !! '+encaixe.length+' FIGURA(S) MAIOR(ES) QUE O LUGAR DELAS (so aparece com a fase jogada):');
   for(const e of encaixe.slice(0,6)) console.log('     '+e);
 }
 const chegou=segOk || (visto.length&&/CHEGOU NO FIM/.test(visto[visto.length-1]));
 /* ⚠️ LICAO PAGA (Museu, ago/2026): no modo SEGMENTO/PARALELO (JSTART) rodam 3
    jogadores ao mesmo tempo; a briga por CPU faz a imagem carregar/animar mais
    devagar e o check in-play acusa "figura maior" que SOME sozinho no quadro
    seguinte — reprova FLAKY. O portao encaixe.js (estatico, por fase) ja cobre
    isso de forma confiavel na banca. Entao, EM SEGMENTO, o achado in-play vira
    AVISO (nao reprova). No modo SERIAL (um so, tela assentada) ele continua
    valendo, que e onde pegou a "lousa gigante" do Marcos. */
 const encaixeOk = process.env.JSTART ? true : (encaixe.length===0);
 if(encaixe.length && process.env.JSTART)
   console.log('  (segmento/paralelo: encaixe in-play e so AVISO — quem reprova e o encaixe.js)');
 if(certoQuebrado) console.log('  !! RESPOSTA DECLARADA CERTA NAO FECHOU A FASE — o conteudo diz uma resposta e a regra de fechamento cobra outra (a crianca acerta e nada acontece)');
 if(!chegou && !certoQuebrado) console.log('  !! O JOGADOR NAO CHEGOU '+(process.env.JSTOP?'AO FIM DO TRECHO':'NA MEDALHA')+' — a crianca pode empacar aqui');
 if(reais.length) console.log('  !! '+reais.length+' ERRO(S) DE JS durante a partida');
 await b.close();
 /* ⚠️ ate ago/2026 este portao NAO reprovava nada: a saida ia para um `tail -4`
    e o codigo de saida se perdia no cano. Ou seja, o auditor jogava a partida
    inteira e o resultado dele era decorativo. Agora ele vota como os outros. */
 process.exit(chegou&&!reais.length&&encaixeOk&&!certoQuebrado ? 0 : 1);
})();
