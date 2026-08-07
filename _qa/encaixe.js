/* ============================================================
   AUDITOR DE ENCAIXE DA IMAGEM — "a figura entrou bem na página?"

   Cobrança do Marcos (ago/2026): *"as imagens sem fundo ficam mais profissionais,
   e sempre verificar a PROPORÇÃO dela na página: se não fica pequena, se não fica
   grande, se ela não corta nos quadrados. Tem que ficar profissional a inserção.
   Na atividade do 5º ano percebo que esse ponto tinha que melhorar."*

   Ele estava certo, e a medição provou: no 5º ano havia uma figura **esticada
   16%** (`object-fit:fill`, que deforma para preencher) e as figuras do jogo da
   memória ocupando **13% da carta** — perdidas no meio do vazio, numa carta que é
   grande justamente para a criança VER.

   Nenhum portão pegava: o de imagem quebrada só pergunta se a figura CARREGOU; o
   de leiaute mede retângulo. Figura deformada e figura minúscula carregam e cabem
   — e mesmo assim ficam feias e atrapalham.

   O QUE ELE MEDE, com a fase aberta de verdade no navegador:
     · ESTICADA  — a proporção na tela difere da proporção do arquivo (>12%);
     · CORTADA   — `object-fit:cover` com proporção diferente (>10%): some pedaço;
     · PEQUENA   — menor que 44px de lado;
     · PERDIDA   — ocupa menos de 16% da caixa em que está.

   ⚠️ O jeito certo é `object-fit:contain` (cabe inteira, sem deformar).
      `fill` DEFORMA. `cover` CORTA. Só use `cover` de propósito, em fundo.

   Uso: node _qa/encaixe.js _naveg/index.html tela1 tela2 ...
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu']});
 const telas=process.argv.slice(3);
 const url='file://'+path.resolve(process.argv[2]);
 const ruins=[];
 for(const t of telas){
   const p=await b.newPage({viewport:{width:412,height:820}});
   p.on('pageerror',()=>{});
   await p.goto(url); await p.waitForTimeout(300);
   const ok=await p.evaluate(t=>{window.falar=function(){};window.depoisDaFala=function(i,m,c){setTimeout(c,50);};
     if(typeof window[t]!=="function")return false; window[t](); return true;},t);
   if(!ok){await p.close();continue;}
   await p.waitForTimeout(900);
   const r=await p.evaluate((tela)=>{
     const out=[];
     document.querySelectorAll("#app img").forEach(im=>{
       const b=im.getBoundingClientRect();
       if(b.width<2||b.height<2) return;
       const cs=getComputedStyle(im);
       const nat=im.naturalWidth/Math.max(1,im.naturalHeight);
       const ren=b.width/Math.max(1,b.height);
       const dif=Math.abs(nat-ren)/Math.max(nat,ren);
       const pai=im.parentElement?im.parentElement.getBoundingClientRect():null;
       const ocupa=pai&&pai.width>0? (b.width*b.height)/(pai.width*pai.height):1;
       const cls="."+String(im.className||"img").split(" ")[0];
       if(cs.objectFit==="cover"&&dif>0.10) out.push(tela+" | "+cls+" CORTADA: object-fit cover e proporcao "+Math.round(dif*100)+"% diferente");
       else if(cs.objectFit!=="contain"&&dif>0.12) out.push(tela+" | "+cls+" ESTICADA "+Math.round(dif*100)+"%");
       if(b.width<44||b.height<44) out.push(tela+" | "+cls+" PEQUENA DEMAIS "+Math.round(b.width)+"x"+Math.round(b.height));
       if(pai&&ocupa<0.16&&pai.width>90) out.push(tela+" | "+cls+" ocupa so "+Math.round(ocupa*100)+"% da caixa dela");
     });
     return out;
   },t);
   ruins.push(...r); await p.close();
 }
 await b.close();
 console.log(ruins.length? ruins.join("\n") : "encaixe ok");
})();
