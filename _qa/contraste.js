/* ============================================================
   VERIFICADOR DE CONTRASTE (WCAG) — pedido do Marcos, ago/2026
   "sempre verificar se nao ha um contraste nas cores, para que
    nao acontece de a crianca nao conseguir enxergar"

   Por que existe: nas atividades o fundo e uma FOTO (imagem de IA).
   Olhar so o CSS engana — a regra diz `color:#fff` e parece certo,
   mas o pixel atras pode ser creme claro e a crianca nao le nada.
   Este script mede o PIXEL DE VERDADE:
     1) abre a tela pedida no Chromium;
     2) tira o print NORMAL;
     3) deixa TODO texto transparente e tira o print SO DO FUNDO;
     4) para cada texto, pega a cor computada e a cor mediana do
        fundo naquele retangulo -> razao de contraste WCAG.
   Reprova abaixo de 4.5:1 (texto normal) e 3.0:1 (texto grande).

   Uso:
     node _qa/contraste.js _doceria/index.html telaCapa dMonta dVezes ...
   Sai com codigo 1 se algum texto reprovar (da p/ usar em workflow).
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const fs=require('fs'), path=require('path'), os=require('os');

const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function lum(r,g,b){
  const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);};
  return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);
}
function razao(c1,c2){
  const a=lum(...c1), b=lum(...c2);
  return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
}
/* mistura cor com alfa sobre um fundo */
function sobre(cor,fundo){
  const a=cor[3]===undefined?1:cor[3];
  return [0,1,2].map(i=>Math.round(cor[i]*a+fundo[i]*(1-a)));
}
function parseCor(s){
  const m=s.match(/rgba?\(([^)]+)\)/);
  if(!m) return null;
  const p=m[1].split(",").map(x=>parseFloat(x));
  return [p[0],p[1],p[2],p.length>3?p[3]:1];
}

(async()=>{
  const arquivo=process.argv[2];
  const telas=process.argv.slice(3);
  if(!arquivo){ console.log("uso: node _qa/contraste.js <arquivo.html> [tela1 tela2 ...]"); process.exit(2); }
  if(!telas.length) telas.push("telaCapa");

  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const p=await b.newPage({viewport:{width:412,height:820}});
  p.on('pageerror',()=>{});
  const url='file://'+path.resolve(arquivo);
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'contraste-'));
  let reprovados=[], total=0;

  for(const tela of telas){
    await p.goto(url);
    await p.waitForTimeout(500);
    await p.evaluate(()=>{ window.falar=function(){}; window.depoisDaFala=function(i,m,cb){setTimeout(cb,80);}; });
    if(tela!=="telaCapa"){
      const ok=await p.evaluate(t=>{ if(typeof window[t]!=="function") return false; window[t](); return true; },tela);
      if(!ok){ console.log("  (pulei "+tela+": nao e funcao)"); continue; }
    } else { await p.evaluate(()=>telaCapa()); }
    await p.waitForTimeout(900);

    /* 1) lista os textos visiveis + cor computada + tamanho */
    const itens=await p.evaluate(()=>{
      const out=[];
      const todos=document.querySelectorAll("#app *");
      for(let i=0;i<todos.length;i++){
        const e=todos[i];
        /* so quem tem texto PROPRIO (nao herdado de filhos) */
        let txt="";
        for(let k=0;k<e.childNodes.length;k++)
          if(e.childNodes[k].nodeType===3) txt+=e.childNodes[k].nodeValue;
        txt=txt.replace(/\s+/g," ").trim();
        if(!txt) continue;
        const r=e.getBoundingClientRect();
        if(r.width<4||r.height<4||r.top>820||r.bottom<0) continue;
        const cs=getComputedStyle(e);
        if(cs.visibility==="hidden"||cs.opacity==="0") continue;
        const fs=parseFloat(cs.fontSize), fw=parseInt(cs.fontWeight)||400;
        /* marca o elemento para reler o retangulo na hora EXATA do print */
        e.setAttribute("data-qacon", String(out.length));
        out.push({txt:txt.substring(0,42), cls:e.className||e.tagName.toLowerCase(),
                  cor:cs.color, fs:fs, grande:(fs>=24)||(fs>=18.66&&fw>=700),
                  sombra:cs.textShadow&&cs.textShadow!=="none",
                  x:Math.round(r.left),y:Math.round(r.top),
                  w:Math.round(r.width),h:Math.round(r.height)});
      }
      return out;
    });

    /* 2) print SO DO FUNDO (texto transparente) */
    await p.addStyleTag({content:"*{color:transparent!important;text-shadow:none!important;-webkit-text-fill-color:transparent!important}"});
    await p.waitForTimeout(160);
    const fundo=path.join(tmp,tela+"-fundo.png");
    await p.screenshot({path:fundo});

    /* ⚠️ LICAO PAGA (ago/2026, Maquina do Tempo): entre a MEDIDA e o PRINT a tela
       continua se mexendo — no boletim do fim as barras crescem e as estrelas
       acendem, e a pagina inteira desce. O retangulo media um lugar e o pixel
       vinha de outro: o portao acusou "branco sobre branco" num botao azul que
       estava perfeito. Agora releio os retangulos no MESMO instante do print. */
    const agora=await p.evaluate(()=>{
      const m={},els=document.querySelectorAll("[data-qacon]");
      for(let i=0;i<els.length;i++){ const r=els[i].getBoundingClientRect();
        /* a BARRA de baixo (Ouvir/Dica) e camada FIXA: quando ela passa por cima
           de um texto, o pixel do fundo e o da barra, e o portao acusava "branco
           sobre branco" num botao azul perfeito. Nao e defeito de contraste — a
           tela rola e o texto sai de baixo dela. Quem cuida disso e o portao do
           leiaute (regra 3), que sabe perdoar quando a tela rola.             */
        const alvo=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
        const tapado=!!(alvo&&alvo.closest&&alvo.closest("#barra"));
        /* ⚠️ TEXTO QUE NAO ESTA A MOSTRA nao tem contraste ruim: ele nao esta la.
           Foi o caso das cartas do jogo da memoria — a FACE DA FRENTE existe no
           DOM desde o começo, mas fica virada para tras (backface-visibility) e
           so aparece quando a crianca vira a carta. O portao media a letra da
           frente contra o COURO do verso e reprovava oito cartas de uma vez.
           Teste honesto: quem recebe o dedo no centro deste texto e ele mesmo? */
        const escondido=!(alvo&&(alvo===els[i]||els[i].contains(alvo)||alvo.contains(els[i])));
        m[els[i].getAttribute("data-qacon")]={x:Math.round(r.left),y:Math.round(r.top),
                                              w:Math.round(r.width),h:Math.round(r.height),
                                              tapado:tapado||escondido}; }
      return m;
    });
    for(let i=0;i<itens.length;i++){ const n=agora[String(i)];
      if(!n) continue;
      if(n.tapado){ itens[i].pular=true; continue; }
      if(n.w>=4&&n.h>=4){ itens[i].x=n.x; itens[i].y=n.y; itens[i].w=n.w; itens[i].h=n.h; } }

    /* 3) mediana do fundo em cada retangulo -> via python */
    const dados=path.join(tmp,tela+".json");
    fs.writeFileSync(dados, JSON.stringify(itens));
    const {execSync}=require('child_process');
    const cores=JSON.parse(execSync("python3 "+path.join(__dirname,"contraste_fundo.py")+" "+fundo+" "+dados).toString());

    for(let i=0;i<itens.length;i++){
      const it=itens[i], bg=cores[i];
      if(!bg||it.pular) continue;
      const c=parseCor(it.cor); if(!c) continue;
      const cor=sobre(c,bg);
      const r=razao(cor,bg);
      total++;
      const minimo=it.grande?3.0:4.5;
      if(r<minimo) reprovados.push({tela:tela,...it,bg:bg,cor:cor,r:r,minimo:minimo});
    }
  }
  await b.close();

  console.log(arquivo+" -> "+total+" textos medidos em "+telas.length+" tela(s)");
  if(!reprovados.length){ console.log("  contraste ok: nenhum texto abaixo do minimo WCAG"); process.exit(0); }
  reprovados.sort((a,b)=>a.r-b.r);
  console.log("  "+reprovados.length+" TEXTO(S) COM CONTRASTE BAIXO (a crianca pode nao enxergar):");
  for(const x of reprovados){
    console.log("   ["+x.tela+"] ."+String(x.cls).split(" ")[0]+"  razao "+x.r.toFixed(2)+":1"+
                " (minimo "+x.minimo+")  texto rgb("+x.cor.join(",")+") sobre rgb("+x.bg.join(",")+")"+
                (x.sombra?"  [tem sombra]":"")+"\n        \""+x.txt+"\"");
  }
  process.exit(1);
})();
