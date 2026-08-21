/* ============================================================
   PORTÃO — "duas plaquinhas iguais na mesma tela?"

   ⚠️ LIÇÃO PAGA (Lojinha, pintar-canvas, ago/2026). O motor SEMPRE põe a
   plaquinha (o `.selo`) em cima da fase — o texto vem do `conteudo.json`
   (`fase.selo`). As peças comuns desenham a DELAS dentro de `.pecabox`, e o
   motor esconde por CSS (`.pecabox .selo{display:none}`). Mas uma peça que
   monta a PRÓPRIA `.tela` (canvas de pintar, simulador de tela cheia) fica
   FORA de `.pecabox` — a regra do CSS não a alcança. Aí, se ela também desenha
   um `.selo`, saem DUAS plaquinhas idênticas, uma embaixo da outra, comendo a
   tela da criança (que já é curta no monitor da escola).

   Por que nenhum portão pegava: `node --check` passa (é DOM, não sintaxe);
   contraste/leiaute passam (a plaquinha é legível e cabe). É REDUNDÂNCIA, e
   redundância não estoura — só rouba espaço. Foi o olho, no print, que viu.

   Estático não dá: TODA peça monta `.tela` e `.selo`; o que muda é o embrulho
   em `.pecabox`, feito em tempo de execução. Então este portão RENDERIZA cada
   fase e conta os `.selo` VISÍVEIS: dois ou mais na mesma tela = reprova.

   Uso: node _qa/selo.js <arquivo.html>
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');
const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async()=>{
  const arquivo=process.argv[2];
  if(!arquivo){ console.log("uso: node _qa/selo.js <arquivo.html>"); process.exit(2); }
  const url='file://'+path.resolve(arquivo);
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const p=await b.newPage({viewport:{width:412,height:820}});
  p.on('pageerror',()=>{});
  await p.goto(url); await p.waitForTimeout(400);
  const nfases=await p.evaluate(()=>
    (typeof montaFase==="function" && typeof FASES!=="undefined") ? FASES.length : 0);
  if(!nfases){
    console.log(arquivo+" -> nao e atividade montada (sem montaFase/FASES). NAO MEDI.");
    await b.close(); process.exit(2);
  }
  let ruins=[], medidas=0;
  for(let i=0;i<nfases;i++){
    await p.goto(url); await p.waitForTimeout(240);
    const ok=await p.evaluate(idx=>{
      window.falar=function(){}; window.depoisDaFala=function(a,m,cb){setTimeout(cb,30);};
      try{ montaFase(idx,function(){}); return true; }catch(e){ return false; }
    }, i);
    if(!ok) continue;
    await p.waitForTimeout(500);
    const selos=await p.evaluate(()=>{
      const vis=el=>{ const c=getComputedStyle(el);
        return c.display!=="none" && c.visibility!=="hidden" && parseFloat(c.opacity||"1")>0.05
          && el.getBoundingClientRect().height>2; };
      return [...document.querySelectorAll('.selo')].filter(vis).map(s=>s.textContent.trim());
    });
    medidas++;
    if(selos.length>=2) ruins.push({fase:i+1, selos});
  }
  await b.close();
  console.log(arquivo+" -> "+medidas+" fase(s) medida(s) para plaquinha duplicada");
  if(!ruins.length){
    console.log("  selo ok: cada fase tem UMA plaquinha (a do motor)");
    process.exit(0);
  }
  console.log("  "+ruins.length+" FASE(S) COM DUAS OU MAIS PLAQUINHAS VISIVEIS (uma embaixo da outra, comendo a tela):");
  for(const r of ruins) console.log('   - fase '+r.fase+': '+r.selos.map(s=>'"'+s.slice(0,22)+'"').join(' + '));
  console.log("  conserto: o selo e do MOTOR (vem do conteudo.json). Se a peca monta a");
  console.log("  propria .tela, ela NAO pode desenhar `el(\"div\",\"selo\",...)` — apague-o.");
  process.exit(1);
})();
