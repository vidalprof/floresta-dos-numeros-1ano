/* ============================================================
   AUDITOR DE IMAGEM QUEBRADA — "toda figura aparece mesmo?"

   Nasceu de um defeito que o Marcos pegou (ago/2026), no jogo da memória da
   Máquina do Tempo: em cima das cartas aparecia um QUADRADINHO de imagem que
   não veio. A causa era resto de clone — o verso da carta apontava para
   `img/cq_base.png`, arquivo de OUTRA atividade, que nunca existiu nesta.

   Por que nenhum portão pegava: o `node --check` não abre imagem; o auditor de
   leiaute mede retângulos (e o quadradinho quebrado TEM retângulo); o de
   contraste olha texto; e o jogador clica e segue em frente — o app funciona
   inteiro com a figura faltando. Só o olho da criança via.

   Aqui a conta é a que importa: a figura CARREGOU? Um <img> que terminou de
   carregar com `naturalWidth === 0` é uma figura que a criança não vê.
   Confere as figuras de CADA tela e também a lista de pré-carga (`IMGS`),
   que é de onde saem as figuras que aparecem depois, no meio da fase.

   Palavras do Marcos: *"todas as imagens devem aparecer na atividade, inclusive
   em navegadores chrome antigo"*.

   Uso: node _qa/imagens.js _historia/index.html tela1 tela2 ...
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');

const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async()=>{
  const arquivo=process.argv[2];
  const telas=process.argv.slice(3);
  if(!arquivo){ console.log("uso: node _qa/imagens.js <arquivo.html> <tela...>"); process.exit(2); }
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const p=await b.newPage({viewport:{width:412,height:820}});
  p.on('pageerror',()=>{});
  const url='file://'+path.resolve(arquivo);
  const quebradas=new Map();   // src -> telas onde apareceu

  function anota(src,tela){
    const curto=String(src).split('/').slice(-1)[0];
    if(!quebradas.has(curto)) quebradas.set(curto,new Set());
    quebradas.get(curto).add(tela);
  }

  /* 1) a PRE-CARGA (var IMGS): sao as figuras que entram no meio da fase.
        Elas nem chegam ao DOM na abertura, entao so este teste as alcanca. */
  await p.goto(url);
  await p.waitForTimeout(500);
  /* ⚠️ LICAO PAGA (ago/2026) — ESTE PORTAO RODOU CEGO E EU SO DESCOBRI OLHANDO.
     A linha era `if(typeof IMGS==="undefined"||typeof srcDe!=="function")
     return [];`. So que `srcDe` NUNCA EXISTIU no motor — o caminho da figura e
     montado inline (`"img/"+nome+".png"`, ver `precarrega`). Ou seja: a
     condicao era sempre verdadeira, o teste devolvia lista VAZIA e o portao
     imprimia "imagens ok" com a maior tranquilidade. Duas poses do mascote
     (`_fuba_pensa` e `_fuba_festa`) davam 404 na cara da crianca e a banca
     inteira aprovava.
     Duas correcoes, e as duas importam:
       1. montar o caminho do mesmo jeito que o motor monta;
       2. se NAO der para medir, dizer "NAO MEDI" e reprovar — nunca devolver
          vazio, que o chamador le como "esta tudo certo". */
  const pre=await p.evaluate(async()=>{
    if(typeof IMGS==="undefined") return {cego:"a atividade nao publica IMGS"};
    const src = (typeof srcDe==="function") ? srcDe : (n=>"img/"+n+".png");
    const ruins=[];
    await Promise.all(IMGS.map(n=>new Promise(ok=>{
      const im=new Image();
      im.onload=()=>ok();
      im.onerror=()=>{ ruins.push(src(n)); ok(); };
      im.src=src(n);
      /* imagem que ja veio do cache nao dispara evento */
      if(im.complete){ if(!im.naturalWidth) ruins.push(src(n)); ok(); }
    })));
    return {ruins:ruins, quantas:IMGS.length};
  });
  /* ⚠️ E O FALSO-POSITIVO QUE ISTO CRIOU, no mesmo dia: PECA AVULSA nao tem
     pre-carga — `IMGS` e do MOTOR, e a peca roda sozinha. Reprovar por isso
     seria cobrar de um arquivo uma coisa que ele nao tem. "Nao existe" e
     diferente de "nao consegui medir": a primeira e informacao, a segunda e
     cegueira. So a segunda reprova. */
  if(pre.cego){
    console.log("  (sem pre-carga: "+pre.cego+" — normal em peca avulsa)");
  }
  for(const s of (pre.ruins||[])) anota(s,"pre-carga (IMGS)");

  /* 2) tela por tela: o que esta na tela carregou? */
  for(const t of telas){
    await p.goto(url); await p.waitForTimeout(280);
    const ok=await p.evaluate(t=>{
      window.falar=function(){}; window.depoisDaFala=function(i,m,cb){setTimeout(cb,60);};
      if(typeof window[t]!=="function") return false; window[t](); return true;
    },t);
    if(!ok){ console.log("  (pulei "+t+": nao e funcao)"); continue; }
    await p.waitForTimeout(900);
    /* ⚠️ LICAO PAGA (ago/2026) — O MEIO-PORTAO. Aqui havia um comentario
       dizendo "fundo por CSS tambem some sem avisar" e, LOGO ABAIXO, uma
       linha `const todos=document.querySelectorAll("#app *")` que nao era
       usada para nada. Isto e pior que nao ter a conferencia: quem le o
       arquivo (eu, semana que vem) ve o comentario e acredita que o fundo
       esta medido. Conferencia pela metade e cegueira com alibi.
       Agora ela existe de verdade: `background-image:url(...)` que nao carrega
       reprova igual a um <img> quebrado — a crianca perde a mesa da padaria,
       o ceu do observatorio, o verso da carta. */
    const ruins=await p.evaluate(async()=>{
      const fora=[];
      const ims=document.querySelectorAll("img");
      for(let i=0;i<ims.length;i++){
        const im=ims[i];
        if(im.complete && im.naturalWidth===0) fora.push(im.getAttribute("src")||"(sem src)");
      }
      /* fundo por CSS: junta os endereços de todo mundo que esta na tela e
         tenta carregar cada um uma vez so (Set), inclusive o <body>. */
      const ends=new Set();
      const todos=[document.body].concat([].slice.call(document.querySelectorAll("#app *, #app")));
      for(let i=0;i<todos.length;i++){
        const bi=getComputedStyle(todos[i]).backgroundImage;
        if(!bi||bi==="none") continue;
        const m=bi.match(/url\((['"]?)([^'")]+)\1\)/g)||[];
        for(let j=0;j<m.length;j++){
          const u=m[j].replace(/^url\((['"]?)/,"").replace(/(['"]?)\)$/,"");
          if(/^data:/.test(u)) continue;          /* SVG embutido nao tem como faltar */
          ends.add(u);
        }
      }
      await Promise.all([...ends].map(u=>new Promise(ok=>{
        const im=new Image();
        im.onload=()=>ok(); im.onerror=()=>{ fora.push("fundo CSS: "+u); ok(); };
        im.src=u;
        if(im.complete){ if(!im.naturalWidth) fora.push("fundo CSS: "+u); ok(); }
      })));
      return fora;
    });
    for(const s of ruins) anota(s,t);
  }
  await b.close();

  console.log(arquivo+" -> imagens conferidas em "+telas.length+" tela(s) + a pre-carga");
  if(!quebradas.size){ console.log("  imagens ok: toda figura da atividade carrega"); process.exit(0); }
  console.log("  "+quebradas.size+" IMAGEM(NS) QUE NAO CARREGA(M) (a crianca ve um quadradinho vazio):");
  for(const [src,onde] of quebradas)
    console.log("   "+src+"  ->  "+[...onde].slice(0,4).join(", ")+([...onde].length>4?" ...":""));
  process.exit(1);
})();
