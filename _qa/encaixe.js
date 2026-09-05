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
const path=require('path');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu']});
 const telas=process.argv.slice(3);
 const url='file://'+path.resolve(process.argv[2]);
 const ruins=[];
 /* ⚠️⚠️ LICAO PAGA (ago/2026), a mesma do leiaute e do jogador: este portao so
    sabia abrir tela pelo NOME, e as fases da atividade montada nao sao funcoes
    globais — quem as desenha e o motor, `montaFase(i)`. Ou seja: numa atividade
    montada ele nunca tinha olhado UMA figura de fase. Aqui ele anda pelo motor
    tambem, e conta quantas telas abriu de verdade. */
 const p0=await b.newPage({viewport:{width:412,height:820}});
 await p0.goto(url); await p0.waitForTimeout(400);
 const nfases=await p0.evaluate(()=>
   (typeof montaFase==="function" && typeof FASES!=="undefined") ? FASES.length : 0);
 await p0.close();
 const alvos=telas.map(t=>({nome:t}));
 for(let i=0;i<nfases;i++) alvos.push({fase:i});
 let medidas=0, puladas=0;
 /* ⚡ MEDIDO (set/2026): abria um NAVEGADOR NOVO (newPage + goto de 700 KB) para
    cada uma das 40 telas — 56s. Uma pagina so; a fase e desenhada em cima dela
    por `montaFase(i)` (o `limpa()` do motor zera a anterior). Recarrega so nas
    telas COM NOME, que leem o estado salvo e mudariam sem recarga. */
 const p=await b.newPage({viewport:{width:412,height:820}});
 p.on('pageerror',()=>{});
 let carregada=false;
 for(const alvo of alvos){
   const t = (alvo.nome!==undefined) ? alvo.nome : ("fase"+(alvo.fase+1));
   if(!carregada || alvo.nome!==undefined){ await p.goto(url); await p.waitForTimeout(300); carregada=true; }
   const ok=await p.evaluate(a=>{window.falar=function(){};window.depoisDaFala=function(i,m,c){setTimeout(c,50);};
     if(a.fase!==undefined){ try{ montaFase(a.fase,function(){}); return true; }catch(e){ return false; } }
     if(typeof window[a.nome]!=="function")return false; window[a.nome](); return true;},alvo);
   if(!ok){puladas++; continue;}
   medidas++;
   await p.waitForTimeout(900);
   const r=await p.evaluate((tela)=>{
     const out=[];
     document.querySelectorAll("#app img").forEach(im=>{
       const b=im.getBoundingClientRect();
       if(b.width<2||b.height<2) return;
       const cs=getComputedStyle(im);
       /* ⚠️ O QUE A CRIANCA NAO VE NAO TEM TAMANHO A JULGAR (medido, ago/2026).
          A vitrine desenha a vaga AINDA NAO CONQUISTADA com `opacity:0` e
          `scale(.4)` — ela e o fantasma do que vai chegar. Medindo o retangulo
          desse fantasma, o portao anunciou "PEQUENA DEMAIS 11x11" dezenas de
          vezes numa tela correta, e eu fui procurar o defeito na largura da
          vaga, que estava certa. Elemento invisivel sai da conta — inclusive
          quando quem apaga e um ANTECESSOR dele. */
       let invisivel=false;
       for(let a=im; a && a.nodeType===1; a=a.parentElement){
         const c=getComputedStyle(a);
         if(parseFloat(c.opacity||"1")<0.05||c.visibility==="hidden"){ invisivel=true; break; }
       }
       if(invisivel) return;
       /* ⚠️ A VITRINE E A BARRA DE PROGRESSO desta casa (o motor a usa NO LUGAR
          da barra fina): ela mostra PICTOGRAMA do que a crianca ja juntou, nao
          ilustracao para olhar de perto. Medir a miniatura dela com a regua da
          ilustracao (44px) e cobrar de um elemento o que ele nunca prometeu.
          O que vale ali — figura reconhecivel — se resolve na largura da vaga,
          e essa conta mora no motor. */
       if(im.closest && im.closest(".vitrine")) return;
       /* ⚠️ LICAO PAGA (Museu, ago/2026): a MARCA D'AGUA da gaveta (`.gwater`,
          opacity .12, pointer-events none, z-index 0) e uma REFERENCIA fraca
          atras do NOME da gaveta — o Marcos pediu "so pra ser uma referencia,
          nao pode aparecer tao otica". Um bicho largo e baixo (o jacare deitado)
          vira uma marca d'agua 98x35, e o portao a media com a regua da
          ilustracao (44px) e reprovava "PEQUENA DEMAIS". Ela nao e a figura que
          a crianca olha — a gaveta se le pelo nome + alto-falante. Fora da conta,
          como a vitrine. (Opacity .12 escapa do corte .05 la de cima de proposito:
          o desenhista quis a marca visivel, so nao PROTAGONISTA.) */
       if(im.closest && im.closest(".gwater")) return;
       const nat=im.naturalWidth/Math.max(1,im.naturalHeight);
       const ren=b.width/Math.max(1,b.height);
       const dif=Math.abs(nat-ren)/Math.max(nat,ren);
       const pai=im.parentElement?im.parentElement.getBoundingClientRect():null;
       const ocupa=pai&&pai.width>0? (b.width*b.height)/(pai.width*pai.height):1;
       const cls="."+String(im.className||"img").split(" ")[0];
       if(cs.objectFit==="cover"&&dif>0.10) out.push(tela+" | "+cls+" CORTADA: object-fit cover e proporcao "+Math.round(dif*100)+"% diferente");
       else if(cs.objectFit!=="contain"&&dif>0.12) out.push(tela+" | "+cls+" ESTICADA "+Math.round(dif*100)+"%");
       if(b.width<44||b.height<44) out.push(tela+" | "+cls+" PEQUENA DEMAIS "+Math.round(b.width)+"x"+Math.round(b.height));
       /* ⚠️ LICAO PAGA (ago/2026): a regra "ocupa < 16% da caixa" existe para
          pegar FIGURA PERDIDA NUMA MOLDURA — uma so figura numa caixa grande
          demais para ela. Mas ela acusava a MEDALHA (190px) e a FOTO do cracha
          (62px) da telaFim, porque o pai delas e a COLUNA `.centro`/`.cracha`,
          que segura a tela inteira (medalha + titulo + boletim + botoes). Uma
          coluna de leiaute nao e uma moldura: e natural a figura ocupar pouco
          da area dela. So e "moldura" quando a figura esta SOZINHA na caixa —
          se tem irmaos, o pai e leiaute, e a conta de ocupacao nao vale. */
       const soFilho=im.parentElement&&im.parentElement.children.length<=1;
       if(pai&&ocupa<0.16&&pai.width>90&&soFilho) out.push(tela+" | "+cls+" ocupa so "+Math.round(ocupa*100)+"% da caixa dela");
     });
     return out;
   },t);
   ruins.push(...r);
 }
 await p.close();
 await b.close();
 /* o numero honesto de cobertura, pela mesma regra dos outros: o que foi
    MEDIDO, nunca o que foi tentado. */
 console.log(process.argv[2]+" -> encaixe conferido em "+medidas+" tela(s) ("
   +telas.length+" por nome + "+nfases+" fase(s) pelo motor)"
   +(puladas? " | "+puladas+" nao abriram" : ""));
 if(!medidas){ console.log("   NAO MEDI NENHUMA TELA — isto nao e \"passou\"."); await b.close(); process.exit(2); }
 console.log(ruins.length? ruins.join("\n") : "encaixe ok");
})();
