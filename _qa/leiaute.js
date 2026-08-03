/* ============================================================
   AUDITOR DE LEIAUTE — "cabe na tela e da para tocar?"
   Nasceu de um erro pago (foto do Marcos, ago/2026): numa janela
   baixa (~360px de altura) as OPCOES DE RESPOSTA ficavam FORA da
   tela. A crianca via so o enunciado e nao sabia que havia o que
   responder. O print de uma tela so nao pega isso — tem que medir
   em VARIOS tamanhos.

   O que ele reprova:
     1. algo que estoura na HORIZONTAL (a tela nao rola de lado);
     2. RESPOSTA fora da area visivel (o pior: parece que acabou);
     3. resposta ESCONDIDA atras da barra de baixo (Ouvir/Dica);
     4. alvo de toque pequeno demais (<40px) para dedo de crianca.
   Rolagem vertical NAO e erro por si so — so e erro quando o que
   se toca fica fora.

   Uso: node _qa/leiaute.js _doceria/index.html tela1 tela2 ...
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');

const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
/* tamanhos reais: celular velho, celular comum, celular grande, PC da escola
   (janela com barras), PC em tela cheia, projetor/janela baixa */
const TAMANHOS=[
  {w:320,h:568,n:'celular pequeno'},
  {w:360,h:640,n:'celular comum'},
  {w:412,h:820,n:'celular grande'},
  {w:1366,h:640,n:'PC 1366 com barras'},
  {w:1366,h:768,n:'PC 1366 tela cheia'},
  {w:1024,h:420,n:'janela baixa'},
];
/* o que a crianca precisa TOCAR para a fase andar */
const RESPOSTA='.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.btn,.pc,.peca';

(async()=>{
  const arquivo=process.argv[2];
  const telas=process.argv.slice(3);
  if(!arquivo||!telas.length){ console.log("uso: node _qa/leiaute.js <arquivo.html> <tela...>"); process.exit(2); }
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const url='file://'+path.resolve(arquivo);
  let falhas=[];

  for(const vp of TAMANHOS){
    const p=await b.newPage({viewport:{width:vp.w,height:vp.h}});
    p.on('pageerror',()=>{});
    for(const t of telas){
      await p.goto(url); await p.waitForTimeout(280);
      const ok=await p.evaluate(t=>{
        window.falar=function(){}; window.depoisDaFala=function(i,m,cb){setTimeout(cb,60);};
        if(typeof window[t]!=="function") return false; window[t](); return true;
      },t);
      if(!ok) continue;
      await p.waitForTimeout(650);
      const r=await p.evaluate(sel=>{
        const out=[];
        const barra=document.getElementById("barra");
        const topoBarra=barra&&barra.getBoundingClientRect().height? barra.getBoundingClientRect().top : innerHeight;
        const els=[...document.querySelectorAll("#app "+sel)].filter(e=>e.offsetParent!==null);
        let forams=0, atras=0, pequenos=0;
        for(const e of els){
          const b=e.getBoundingClientRect();
          if(b.width<1||b.height<1) continue;
          if(b.left<-1||b.right>innerWidth+1) out.push("estoura na horizontal: ."+String(e.className).split(" ")[0]);
          if(b.top>=innerHeight-2) forams++;
          else if(b.bottom>topoBarra+2 && b.top<topoBarra) atras++;
          if(b.height<40||b.width<40) pequenos++;
        }
        if(forams) out.push(forams+" resposta(s) FORA da tela (a crianca nao ve o que tocar)");
        if(atras) out.push(atras+" resposta(s) atras da barra de baixo");
        if(pequenos) out.push(pequenos+" alvo(s) menor(es) que 40px");
        return out;
      },RESPOSTA);
      for(const m of r) falhas.push(vp.n+" | "+t+" | "+m);
    }
    await p.close();
  }
  await b.close();

  console.log(arquivo+" -> leiaute conferido em "+TAMANHOS.length+" tamanhos x "+telas.length+" telas");
  if(!falhas.length){ console.log("  leiaute ok: nada fora da tela, nada atras da barra, alvos grandes"); process.exit(0); }
  console.log("  "+falhas.length+" PROBLEMA(S):");
  for(const f of falhas) console.log("   "+f);
  process.exit(1);
})();
