const { chromium } = require('/home/user/floresta-dos-numeros-1ano/node_modules/playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu']});
  const c=await b.newContext({viewport:{width:700,height:900}}); const p=await c.newPage();
  const erros=[]; p.on('pageerror',e=>erros.push(''+e));
  for(const u of ['/controle.html','/controle.html?v=83c95a34c7']){
    await p.goto('http://127.0.0.1:8771'+u,{waitUntil:'load'}); await p.waitForTimeout(1200);
    const r = await p.evaluate(()=>{
      const cx=document.getElementById('cxTerm'), lt=document.getElementById('listaTerm'), ul=document.getElementById('urllab');
      return {cxTerm: cx?getComputedStyle(cx).display:'AUSENTE', lista: lt?lt.textContent.trim():'-',
              urlDoAluno: ul?ul.textContent.trim().slice(0,90):'-'};
    });
    console.log(u, JSON.stringify(r), 'erros:', erros.length? erros: 'nenhum');
  }
  await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
