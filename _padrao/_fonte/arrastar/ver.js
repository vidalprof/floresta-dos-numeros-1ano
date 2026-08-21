
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const fs=require('fs'),path=require('path');
(async()=>{
  const orig=process.argv[2], fase=process.argv[3], dest=process.argv[4];
  const tmp=path.join(dest,'palco.html');
  let h=fs.readFileSync(orig,'utf8');
  h=h.replace('</body>','<script>window.addEventListener("load",function(){setTimeout(function(){try{'+fase+'();}catch(e){document.title="ERRO:"+e.message;}},220);});</script></body>');
  fs.writeFileSync(tmp,h);
  const b=await chromium.launch({args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:640,height:940}});
  await p.goto('file://'+tmp); await p.waitForTimeout(2600);
  await p.screenshot({path:path.join(dest,'1-entrada.png'),fullPage:true});
  const antes=await p.evaluate(()=>document.body.innerHTML.length);
  // toca no primeiro alvo clicavel da fase e fotografa a REACAO
  const clicou=await p.evaluate(()=>{
    const a=[...document.querySelectorAll('.tela .opt,.tela .lig,.tela .peca,.tela .tec,.tela .bin,.tela .pal,.tela .mcarta,.tela .cel')]
      .filter(e=>e.getBoundingClientRect().height>0);
    if(!a.length) return null; a[0].click(); return a[0].className;
  });
  await p.waitForTimeout(900);
  await p.screenshot({path:path.join(dest,'2-depois-do-toque.png'),fullPage:true});
  const depois=await p.evaluate(()=>document.body.innerHTML.length);
  console.log(JSON.stringify({clicou:clicou, mudou: depois!==antes}));
  await b.close();
})();
