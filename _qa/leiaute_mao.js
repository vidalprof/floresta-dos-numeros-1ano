/* ============================================================
   AUDITOR DE LEIAUTE DOS APPS A MAO — "a figura esta inteira e da para tocar?"

   Pedido do Marcos (ago/2026): *"ainda acontecem imagens cortadas"*. Os
   portoes `leiaute.js` e `encaixe.js` so sabem medir atividade MONTADA pelo
   motor (`montaFase(i)`, `FASES`). Os apps escritos a mao — Batata, Mat2,
   Pixel, UNO, SC5, os paineis, o hub — nunca passaram por medicao nenhuma, e
   e justamente ali que a imagem cortada continuava escapando (tarefa #49).

   O que ele faz: abre o app em 6 tamanhos de tela reais (celular pequeno ao PC
   da escola), mede a PRIMEIRA tela e depois anda pelas telas que um botao de
   "comecar/jogar/proximo/continuar" alcanca (ate 6 passos), e em cada uma:
     1. ESTOURO NA HORIZONTAL — a pagina rola de lado (a crianca perde o que
        ficou a direita);                                              REPROVA
     2. FIGURA ESTICADA — `<img>` desenhada com proporcao > 12% diferente da
        do arquivo (object-fit fill/none deforma);                    REPROVA
     3. FIGURA CORTADA — `object-fit:cover` com proporcao > 10% diferente
        (some pedaco), ou a figura saindo do pai que tem overflow:hidden
        em mais de 6%, ou saindo da propria tela de lado;             REPROVA
     4. FUNDO ESTICADO — `background-size:100% 100%` com proporcao diferente
        da do arquivo (a cena toda deformada);                        REPROVA
     5. ALVO PEQUENO — botao/link/onclick visivel com menos de 40 px;  REPROVA
     6. TEXTO CORTADO — caixa com `overflow:hidden` cujo texto nao cabe. AVISO
   Rolagem vertical nao e defeito.

   ⚠️ Ele NAO clica em qualquer coisa: so em botoes cujo texto e de ANDAR
      (comecar, jogar, iniciar, entrar, proximo, continuar, vamos, ok). Nos
      paineis do professor ha botoes que apagam — e nao se mede apagando.

   Uso: node _qa/leiaute_mao.js _batata/index.html [--passos N]
   Codigos: 0 passou · 1 REPROVOU · 2 NAO MEDI (Playwright/arquivo/pagina morta)
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + ').');
  process.exit(2);
}
const path=require('path'), fs=require('fs');
const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const TAMANHOS=[
  {w:320,h:568,n:'celular pequeno'},
  {w:360,h:640,n:'celular comum'},
  {w:412,h:820,n:'celular grande'},
  {w:1366,h:640,n:'PC 1366 com barras'},
  {w:1366,h:768,n:'PC 1366 tela cheia'},
  {w:1024,h:420,n:'janela baixa'},
];
const ANDAR=/^(come[cç]ar|jogar|iniciar|entrar|pr[óo]xim[oa]|continuar|vamos|ok|avan[cç]ar|seguir|start|play|come[cç]a|bora|pronto|abrir)\b/i;

(async()=>{
  const args=process.argv.slice(2);
  const arquivo=args.find(a=>!a.startsWith('--'));
  let passos=6; const ip=args.indexOf('--passos'); if(ip>=0) passos=parseInt(args[ip+1]||'6',10)||6;
  if(!arquivo||!fs.existsSync(arquivo)){ console.log("uso: node _qa/leiaute_mao.js <app/index.html> [--passos N]"); process.exit(2); }
  const url='file://'+path.resolve(arquivo);
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const falhas=[], avisos=[]; let medidas=0, mortas=0;

  /* a medicao de UMA tela, no tamanho atual */
  const MEDE=async(p,rot)=>{
    const r=await p.evaluate(async()=>{
      const out=[], av=[];
      const W=innerWidth, H=innerHeight;
      const se=document.scrollingElement||document.documentElement;
      if(se && se.scrollWidth>W+2) out.push("estoura na horizontal ("+se.scrollWidth+"px numa tela de "+W+"px)");
      const vis=e=>{ const cs=getComputedStyle(e); if(cs.display==="none"||cs.visibility==="hidden"||parseFloat(cs.opacity)===0) return false; const r=e.getBoundingClientRect(); return r.width>1&&r.height>1; };
      const nome=e=>(e.id?"#"+e.id:"")+(e.className&&typeof e.className==="string"?"."+e.className.trim().split(/\s+/)[0]:"")||e.tagName.toLowerCase();
      /* 2/3 — as <img> */
      for(const im of document.images){
        if(!vis(im)||!im.naturalWidth||!im.naturalHeight) continue;
        const r=im.getBoundingClientRect(); if(r.bottom<0||r.top>H) continue;   // fora da dobra: rola ate ela
        const cs=getComputedStyle(im), fit=cs.objectFit||"fill";
        const an=im.naturalWidth/im.naturalHeight, ar=r.width/r.height, dif=Math.abs(ar-an)/an;
        const src=String(im.getAttribute("src")||"").split("/").slice(-1)[0].slice(0,40);
        if((fit==="fill"||fit==="none")&&dif>0.12&&r.width>24&&r.height>24) out.push("figura ESTICADA "+Math.round(dif*100)+"% ("+src+" em "+nome(im)+", object-fit:"+fit+")");
        if(fit==="cover"&&dif>0.10&&r.width>24&&r.height>24) out.push("figura CORTADA por object-fit:cover, "+Math.round(dif*100)+"% de diferenca ("+src+" em "+nome(im)+")");
        if(r.left<-2||r.right>W+2) out.push("figura saindo pela lateral da tela ("+src+")");
        for(let a=im.parentElement;a&&a!==document.body;a=a.parentElement){
          const ov=getComputedStyle(a).overflow+getComputedStyle(a).overflowX+getComputedStyle(a).overflowY;
          if(/hidden|clip/.test(ov)){ const ra=a.getBoundingClientRect();
            const fora=Math.max(0,ra.left-r.left)+Math.max(0,r.right-ra.right)+Math.max(0,ra.top-r.top)+Math.max(0,r.bottom-ra.bottom);
            if(fora>0.06*(r.width+r.height)&&r.width>24) out.push("figura CORTADA pela caixa "+nome(a)+" ("+src+", "+Math.round(fora)+"px fora)"); break; }
        }
      }
      /* 4 — fundos esticados */
      const bgs=[]; for(const e of document.querySelectorAll("*")){ if(!vis(e)) continue; const cs=getComputedStyle(e); const m=/url\(["']?([^"')]+)["']?\)/.exec(cs.backgroundImage||""); if(m&&!/^data:image\/svg/.test(m[1])) bgs.push({e,u:m[1],s:cs.backgroundSize}); }
      const carrega=u=>new Promise(res=>{ const i=new Image(); i.onload=()=>res(i); i.onerror=()=>res(null); i.src=u; setTimeout(()=>res(null),1500); });
      for(const g of bgs.slice(0,40)){
        const r=g.e.getBoundingClientRect(); if(r.width<40||r.height<40) continue;
        const im=await carrega(g.u); if(!im||!im.naturalWidth) continue;
        const an=im.naturalWidth/im.naturalHeight, ar=r.width/r.height, dif=Math.abs(ar-an)/an;
        if(/100%\s+100%/.test(g.s)&&dif>0.12) out.push("fundo ESTICADO "+Math.round(dif*100)+"% (background-size:100% 100% em "+nome(g.e)+")");
        else if(/cover/.test(g.s)&&dif>0.6&&r.width>200) av.push("fundo em cover com proporcao muito diferente ("+Math.round(dif*100)+"%) em "+nome(g.e)+": some mais da metade da cena");
      }
      /* 5 — alvos pequenos */
      let peq=0, ex="";
      /* alvo = botao/link/input/onclick E TAMBEM qualquer coisa com cursor:pointer (os
         apps a mao ligam o clique por JS, sem atributo — as bolinhas de cor do Pixel
         Art, 20px, escapavam por isso). Filho de alvo nao conta duas vezes. */
      const ehAlvo=e=>e.matches('button,a[href],[onclick],input:not([type=hidden]),select,[role=button],.btn')||getComputedStyle(e).cursor==="pointer";
      for(const e of document.querySelectorAll("*")){
        if(!ehAlvo(e)||!vis(e)) continue;
        let pai=e.parentElement, dentro=false; while(pai&&pai!==document.body){ if(ehAlvo(pai)){ dentro=true; break; } pai=pai.parentElement; }
        if(dentro) continue;
        const r=e.getBoundingClientRect(); if(r.bottom<0||r.top>H) continue;
        if(r.width<40||r.height<40){ peq++; if(!ex) ex=nome(e)+" "+Math.round(r.width)+"x"+Math.round(r.height); }
      }
      if(peq) out.push(peq+" alvo(s) menor(es) que 40px (ex.: "+ex+")");
      /* 6 — texto cortado */
      let tc=0;
      for(const e of document.querySelectorAll("*")){ if(!vis(e)) continue; const cs=getComputedStyle(e); if(!/hidden|clip/.test(cs.overflow+cs.overflowX)) continue; if(cs.textOverflow==="ellipsis") continue; if(e.children.length) continue; if(e.scrollWidth>e.clientWidth+6&&e.textContent.trim().length>2){ tc++; } }
      if(tc) av.push(tc+" caixa(s) com texto que nao cabe (overflow:hidden sem reticencias)");
      return {out,av};
    });
    medidas++;
    for(const x of r.out) falhas.push(rot+": "+x);
    for(const x of r.av) avisos.push(rot+": "+x);
  };

  for(const vp of TAMANHOS){
    const p=await b.newPage({viewport:{width:vp.w,height:vp.h}});
    let morta=false; p.on('pageerror',()=>{ morta=true; });
    /* rede travada no container: Firebase/CDN nao respondem — nao pode segurar a medicao */
    await p.route('**/*',route=>{ const u=route.request().url(); if(u.startsWith('file://')) route.continue(); else route.abort(); });
    try{ await p.goto(url,{waitUntil:'load',timeout:15000}); }catch(e){ mortas++; await p.close(); continue; }
    await p.waitForTimeout(900);
    await MEDE(p,vp.n+" / tela 1");
    const vistas=new Set([await p.evaluate(()=>document.body.innerText.slice(0,400))]);
    for(let k=2;k<=passos+1;k++){
      const clicou=await p.evaluate((re)=>{
        const R=new RegExp(re,'i');
        const cands=[...document.querySelectorAll('button,a,[onclick],[role=button],.btn')].filter(e=>{
          const cs=getComputedStyle(e); const r=e.getBoundingClientRect();
          return cs.display!=="none"&&cs.visibility!=="hidden"&&r.width>1&&r.height>1&&r.top<innerHeight&&r.bottom>0&&R.test((e.textContent||"").trim());
        });
        if(!cands.length) return false;
        cands[0].click(); return true;
      },ANDAR.source);
      if(!clicou) break;
      await p.waitForTimeout(900);
      const marca=await p.evaluate(()=>document.body.innerText.slice(0,400));
      if(vistas.has(marca)) break;       // nao andou: nao insistir
      vistas.add(marca);
      await MEDE(p,vp.n+" / tela "+k);
    }
    if(morta) mortas++;
    await p.close();
  }
  await b.close();

  console.log(arquivo+" -> leiaute a mao: "+medidas+" tela(s) medidas em "+TAMANHOS.length+" tamanhos"+(mortas?" ("+mortas+" com erro de JS/carga)":""));
  if(!medidas){ console.log("  NAO MEDI NENHUMA TELA — a pagina nao abriu aqui."); process.exit(2); }
  const uniq=a=>[...new Set(a)];
  for(const a of uniq(avisos)) console.log("   aviso: "+a);
  const f=uniq(falhas);
  if(f.length){ console.log("  "+f.length+" DEFEITO(S) DE LEIAUTE:"); for(const x of f) console.log("   - "+x); process.exit(1); }
  console.log("  leiaute ok: nenhuma figura esticada/cortada, nada estourando de lado, alvos >= 40px");
  process.exit(0);
})();
