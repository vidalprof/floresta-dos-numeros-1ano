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
/* ⚠️⚠️ LICAO PAGA (set/2026, na 3a tentativa de publicar o mesmo conserto): o
   `require` do Playwright fica no TOPO, fora de qualquer try. Num lugar sem
   Playwright — o runner do GitHub, por exemplo — ele estoura na hora e o Node
   sai com codigo **1**, que a esteira le como REPROVOU. Mas o portao nao
   reprovou nada: ele nem conseguiu comecar. Isso e codigo **2** (NAO MEDI), e a
   diferenca decide se a entrega para ou segue. */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + '). ' +
              'Este portao roda na bancada local, onde ha Chromium.');
  process.exit(2);
}
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

  /* ⚠️ LICAO PAGA (ago/2026) — O MESMO BURACO DO `imagens.js`, e este e o
     portao que o Marcos pediu com todas as letras (*"sempre verificar se nao
     ha um contraste nas cores, para que nao aconteca de a crianca nao
     conseguir enxergar"*). Numa atividade montada pelo esqueleto as fases nao
     sao funcoes globais — sao fechamentos dentro de `MEC["nome"]`, desenhados
     pelo motor (`montaFase(i)`). O detector de telas da banca lista os nomes
     que vivem DENTRO das pecas e nenhum deles existe no `window`: na Padaria
     eram 25 "pulei" para 10 telas medidas, e o rodape ainda dizia "35 telas".
     Agora as fases entram pelo caminho de verdade, e o rodape diz quantas
     foram medidas mesmo. */
  await p.goto(url); await p.waitForTimeout(400);
  const nfases=await p.evaluate(()=>
    (typeof montaFase==="function" && typeof FASES!=="undefined") ? FASES.length : 0);
  const alvos=telas.map(t=>({nome:t}));
  for(let i=0;i<nfases;i++) alvos.push({fase:i});
  let puladas=0, abertas=0;

  for(const alvo of alvos){
    const tela = (alvo.nome!==undefined) ? alvo.nome : ("fase"+alvo.fase);
    await p.goto(url);
    await p.waitForTimeout(500);
    await p.evaluate(()=>{ window.falar=function(){}; window.falaDaTela=function(){};
                           window.depoisDaFala=function(i,m,cb){setTimeout(cb,80);}; });
    if(alvo.fase!==undefined){
      const ok=await p.evaluate(i=>{ try{ montaFase(i,function(){}); return true; }
                                     catch(e){ return false; } },alvo.fase);
      if(!ok){ puladas++; continue; }
    } else if(tela!=="telaCapa"){
      const ok=await p.evaluate(t=>{ if(typeof window[t]!=="function") return false; window[t](); return true; },tela);
      if(!ok){ puladas++; continue; }
    } else {
      /* ⚠️ ate aqui a capa era chamada SEM conferir se existe: num arquivo que
         nao tem `telaCapa` o `evaluate` estourava e o portao morria com um
         rastro de erro em vez de dizer "nao consegui medir". */
      const ok=await p.evaluate(()=>{ if(typeof telaCapa!=="function") return false;
                                      telaCapa(); return true; });
      if(!ok){ puladas++; continue; }
    }
    abertas++;
    await p.waitForTimeout(900);
    /* ⚠️ LICAO PAGA (ago/2026, na Oficina da Lina): a tela entra com um fade
       (`aparece .4s`). Medido no PIXEL, um balao ainda a 60% de opacidade
       deixa o FUNDO passar por baixo da letra — e o portao acusou 1,7:1 numa
       tela creme perfeita, de forma INTERMITENTE (passava numa corrida e
       reprovava na seguinte, que e a assinatura de artefato de medicao).
       Prazo fixo nao serve para esperar animacao: espero a tela ficar OPACA. */
    for (let t = 0; t < 20; t++) {
      const pronta = await p.evaluate(() => {
        const el = document.querySelector('.tela');
        if (!el) return true;
        if (parseFloat(getComputedStyle(el).opacity || '1') < 0.99) return false;
        const bal = document.querySelector('.tela .balao');
        return !bal || parseFloat(getComputedStyle(bal).opacity || '1') >= 0.99;
      });
      if (pronta) break;
      await p.waitForTimeout(150);
    }

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
        /* ⚠️ so mede o que cabe INTEIRO no print. Texto cortado na borda de
           baixo fazia o amostrador ler um pixel fora da imagem e acusar
           contraste ridiculo num botao creme perfeito — foi o que aconteceu
           com o menu do professor quando ele passou de 24 para 27 fases. */
        if(r.width<4||r.height<4||r.top<0||r.bottom>820) continue;
        /* ⚠️ e nao mede texto CORTADO por uma lista que rola. No menu do
           professor, que passou a ter 27 fases, a ultima linha fica meio para
           fora da caixa de rolagem — normal em qualquer lista. O amostrador
           lia o pixel do fundo da pagina atras da parte cortada e acusava
           "2,6:1" num botao creme perfeito. Texto que aparece pela metade nao
           se mede: ou aparece inteiro, ou fica de fora da conta.           */
        let cortado=false;
        for(let pa=e.parentElement; pa && pa!==document.body; pa=pa.parentElement){
          const ps=getComputedStyle(pa);
          if(ps.overflowY==="auto"||ps.overflowY==="scroll"||ps.overflow==="hidden"){
            const rp=pa.getBoundingClientRect();
            if(r.top<rp.top-1||r.bottom>rp.bottom+1){ cortado=true; break; }
          }
        }
        if(cortado) continue;
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

  console.log(arquivo+" -> "+total+" textos medidos em "+abertas+" tela(s)"+
    (nfases?" ("+(abertas-nfases>0?abertas-nfases:0)+" por nome + "+nfases+" fase(s) pelo motor)":""));
  if(puladas) console.log("  ("+puladas+" nome(s) da lista nao sao funcao global — "+
    "sao fases dentro das pecas, medidas acima pelo motor)");
  if(!abertas){ console.log("  NAO MEDI NENHUMA TELA — isto nao e 'passou'."); process.exit(1); }
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
