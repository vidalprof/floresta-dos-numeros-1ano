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
 await p.evaluate((t)=>{ (window[t]||telaCapa)(); }, process.env.INICIO||'telaCapa');
 let visto=[], ultimo='', paradas=0;
 const SEL='#bcta,.btn,.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.pc,.peca,.dsolto,.marca,.moeda,.linhac,.qcel'+',.ferr,.vaso,.carta,.zona,.tec,.slot,.mcarta,.gfoto,.pal,.fichaP,.cx,.tlin,.vaga,.relcard,.alim,.rpos,.moeda'+',.pt,.plb,.fs,.errow,.gav,.ficha,.achado,.teclafc';
 for(let i=0;i<5200;i++){
   const est=await p.evaluate(()=>{
     const s=document.querySelector('.selo'), h1=document.querySelector('h1');
     const bn=document.getElementById('banner');
     const pr=document.querySelector('.prog i');
     return ((s&&s.textContent)||(h1&&h1.textContent)||'?')+' ['+((pr&&pr.style.width)||'-')+']|'+((bn&&bn.className.indexOf('show')>=0)?'BANNER':'');
   });
   if(est!==ultimo){ visto.push(i+' '+est); ultimo=est; paradas=0; } else paradas++;
   if(paradas>420){ visto.push('>>> PRESO em '+est); break; }
   const n=await p.evaluate((sel)=>{
     const bn=document.getElementById('banner');
     if(bn&&bn.className.indexOf('show')>=0){ document.getElementById('bcta').click(); return 1; }
     /* caca-palavras: clicando ao acaso o jogador NUNCA acha (1a e ultima letra
        numa grade de 49 casas). A tela publica em data-qa onde cada palavra
        ficou, so para o auditor — assim ele confere de verdade que a fase
        termina e avanca, em vez de reprovar por burrice dele. */
     const g=document.querySelector('.grade[data-qa]');
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
         const d=pos[falta[0].textContent.trim()];
         if(d){
           const N=Math.round(Math.sqrt(g.children.length));
           const r2=d.h? d.r : d.r+d.n-1, c2=d.h? d.c+d.n-1 : d.c;
           g.children[d.r*N+d.c].click(); g.children[r2*N+c2].click(); return 1;
         }
       }
     }
     /* levar-o-item-ate-o-lugar (arrastar OU tocar): peca e destino publicam o
        mesmo valor em data-qa. O jogador usa o caminho do TOQUE (peca, depois
        destino), que e o que a crianca sem arrasto usa. */
     const peca=[...document.querySelectorAll('.pc[data-qa]')].find(e=>e.offsetParent!==null&&e.className.indexOf('usada')<0);
     if(peca){
       if(peca.className.indexOf('sel')<0){ peca.click(); return 1; }
       const dest=[...document.querySelectorAll('.cam[data-qa]')].find(e=>e.getAttribute('data-qa')===peca.getAttribute('data-qa')&&e.className.indexOf('ok')<0);
       if(dest){ dest.click(); return 1; }
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
     const e=els[Math.floor(Math.random()*els.length)];
     e.click(); return 1;
   },SEL);
   await p.waitForTimeout(230);
   if(await p.evaluate(()=>!!document.querySelector('.medal'))){ visto.push(i+' >>> CHEGOU NO FIM'); break; }
 }
 console.log(visto.join('\n'));
 /* o barulho do file:// nao conta: service worker so existe em http(s) */
 const reais=erros.filter(e=>!/ServiceWorker|protocol of the current origin/i.test(e));
 console.log('ERROS JS:', reais.length? reais.slice(0,8).join(' || '):'nenhum');
 const chegou=visto.length&&/CHEGOU NO FIM/.test(visto[visto.length-1]);
 if(!chegou) console.log('  !! O JOGADOR NAO CHEGOU NA MEDALHA — a crianca pode empacar aqui');
 if(reais.length) console.log('  !! '+reais.length+' ERRO(S) DE JS durante a partida');
 await b.close();
 /* ⚠️ ate ago/2026 este portao NAO reprovava nada: a saida ia para um `tail -4`
    e o codigo de saida se perdia no cano. Ou seja, o auditor jogava a partida
    inteira e o resultado dele era decorativo. Agora ele vota como os outros. */
 process.exit(chegou&&!reais.length ? 0 : 1);
})();
