// Abre CADA uma das 32 fases e confere se o marcador ZZ<MEC>nZZ aparece na tela.
// Se aparecer, o conteudo da fase entrou de verdade; se nao, a peca esta
// rodando com o exemplo dela — que e o defeito que nao da erro nenhum.
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu']});
 const p=await b.newPage({viewport:{width:1366,height:640}});
 await p.goto('file://'+require('path').resolve(process.argv[2])); await p.waitForTimeout(800);
 const n=await p.evaluate(()=>FASES.length);
 const ruins=[];
 for(let i=0;i<n;i++){
   const r=await p.evaluate(async(i)=>{
     perfil.nome="T"; abreFase(i);
     await new Promise(r=>setTimeout(r,650));
     const f=FASES[i];
     const txt=(document.getElementById('app').innerText||"")+
       (document.getElementById('app').innerHTML||"");
     const marca=f.mec==="caca-palavras"?"ZZCACA":("ZZ"+f.mec.toUpperCase().replace(/-/g,""));
     // ⚠️ nem toda mecanica MOSTRA TEXTO do conteudo. O "ache o que mudou"
     //    desenha FORMAS: o conteudo dele se prova pela CONTAGEM de diferencas,
     //    que sai do `MUDA` injetado (3, e nao as 5 do exemplo).
     if(f.mec==="sete-erros") return {mec:f.mec, tem:/\b3 diferen/.test(txt)};
     // o `ordenar` guarda NUMEROS, entao o marcador dele e um numero do conteudo
     if(f.mec==="ordenar") return {mec:f.mec, tem:/\b(7|13|21|34|55)\b/.test(txt)};
     return {mec:f.mec, tem:txt.indexOf(marca)>=0};
   }, i);
   if(!r.tem) ruins.push((i+1)+" "+r.mec);
 }
 console.log(ruins.length? "NAO MOSTRARAM O CONTEUDO DA FASE ("+ruins.length+"/"+n+"): "+ruins.join(", ")
                         : "TODAS AS "+n+" FASES MOSTRARAM O CONTEUDO DELAS");
 await b.close();
 process.exit(ruins.length?1:0);
})();
