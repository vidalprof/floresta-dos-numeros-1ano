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
 const SEL='#bcta,.btn,.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.pc,.peca,.dsolto,.marca,.moeda,.linhac,.qcel'+',.ferr,.vaso,.carta,.zona,.tec,.slot,.mcarta,.gfoto,.pal,.fichaP,.cx,.tlin,.vaga,.relcard,.alim,.rpos,.moeda'+',.pt,.plb,.fs';
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
     const els=[...document.querySelectorAll(sel)].filter(e=>{if(e.offsetParent===null)return false;const r=e.getBoundingClientRect();return r.width>0&&r.top<innerHeight&&r.bottom>0;});
     if(!els.length) return 0;
     const e=els[Math.floor(Math.random()*els.length)];
     e.click(); return 1;
   },SEL);
   await p.waitForTimeout(230);
   if(await p.evaluate(()=>!!document.querySelector('.medal'))){ visto.push(i+' >>> CHEGOU NO FIM'); break; }
 }
 console.log(visto.join('\n'));
 console.log('ERROS JS:', erros.length? erros.slice(0,8).join(' || '):'nenhum');
 await b.close();
})();
