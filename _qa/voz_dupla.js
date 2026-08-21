/* ============================================================
   PORTAO — "a mesma voz esta falando DUAS VEZES?"

   ⚠️ LICAO PAGA (ago/2026), e foi o Marcos quem OUVIU, nao portao nenhum:
   *"o da padaria agora e falado duas vezes juntos, soa estranho"*.

   Nasceu de uma boa ideia: varias pecas passaram a NARRAR SOZINHAS ao abrir,
   porque na bancada — sem o motor — a fase ficava muda. Dentro da atividade,
   porem, quem narra o balao e o motor, e sempre narrou. Sao DOIS tocadores
   diferentes (`narr`, do enunciado, e `vz`, das respostas): um nao para o
   outro, entao as duas vozes partem juntas e se atropelam.

   Nenhum portao pegava: o texto estava certo, o mp3 existia, a chave batia.
   O defeito nao esta no QUE se diz — esta em QUANTAS VEZES.

   ⚠️ SEGUNDA LICAO, NO MESMO DIA, E DE NOVO PELO OUVIDO DELE:
   *"quando a crianca acha a resposta certa na primeira fase existem duas falas
   ao mesmo tempo"*. A minha primeira versao deste portao media so a ABERTURA da
   fase — e passou. O atropelo estava no ACERTO: a voz da peca (a palavra) e o
   elogio do motor (`pd_acertoN`) partiam juntos, em 11 fases. Portao que mede
   um momento so aprova a atividade nos outros momentos por omissao.

   O QUE ELE FAZ: abre a atividade e, em CADA fase, mede DOIS momentos —
   a abertura e o ACERTO (clica na resposta certa pelo `data-qa`). Conta os
   `play()` e acusa quando dois partem com menos de 700ms de diferenca.
   Mede o comportamento real do navegador, nao o codigo.

   Uso: node _qa/voz_dupla.js <pasta-da-atividade>
   ============================================================ */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
(async()=>{ const sair=async(c)=>{process.exitCode=c;}; const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu','--autoplay-policy=no-user-gesture-required']});
const p=await b.newPage({viewport:{width:1366,height:640}});
await p.addInitScript(()=>{window.__t=[];const P=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){window.__t.push([Date.now(),(this.src||'').split('/').pop()]);return P.apply(this,arguments);};});
await p.goto('file://'+require('path').resolve(process.argv[2]||'_padaria','index.html'));await p.waitForTimeout(600);
/* ⚠️ LICAO PAGA (ago/2026, na Oficina da Lina): este portao so sabia andar pela
   `FASES` da atividade MONTADA. Numa atividade ESCRITA A MAO as fases sao
   FUNCOES globais (`FASES_MESTRE`), o `p.evaluate` estourou com
   "FASES is not defined" e a bancada inteira parou no meio — sem medir nada e
   sem dizer que nao mediu. Portao que nao sabe abrir a fase sai com 2. */
const forma=await p.evaluate(()=>{
  if(typeof FASES!=='undefined'&&typeof montaFase==='function') return {tipo:'montada',n:FASES.length};
  if(typeof FASES_MESTRE!=='undefined') return {tipo:'mao',telas:FASES_MESTRE.map(f=>f[0])};
  return null;});
if(!forma){console.log('nao achei nem FASES nem FASES_MESTRE: NAO MEDI a voz dupla.');process.exitCode=2;await b.close();return;}
const n=(forma.tipo==='montada')?forma.n:forma.telas.length;
let ruim=0;
for(let i=0;i<n;i++){
 /* ⚠️ DEFEITO DO PROPRIO PORTAO (ago/2026): a lista so era zerada DEPOIS de ler
    a abertura, entao o elogio do acerto da fase ANTERIOR entrava na conta da
    abertura da seguinte e ele acusava a fase errada — duas linhas para um
    defeito so, e a de cima apontando para quem estava certo. A janela de
    medicao comeca quando a fase comeca. */
 /* ⚠️ E PRECISO DEIXAR A FASE ANTERIOR TERMINAR DE FALAR (ago/2026). O elogio
    do acerto sai com atraso (a peca comemora, mostra o banner e so entao o som
    chega); se a proxima fase for montada em cima disso, o rabo da anterior cai
    na janela da seguinte e o portao acusa uma fase INOCENTE — e acusava uma
    diferente a cada corrida, que e a assinatura de artefato de medicao. No jogo
    de verdade quem separa as duas telas e o dedo da crianca no "Continuar".
    Aqui: esvazio, deixo escoar, esvazio de novo — e so entao meco. */
 /* ⚠️ e 700ms NAO BASTAVA: medido, o elogio da fase anterior chega **2,8s**
    depois do acerto, porque ele entra na FILA atras da voz da peca (o motor
    toca uma voz por vez — e isso e o certo). Prazo fixo nao serve para esperar
    fila; espero ficar QUIETO. */
 for(let t=0;t<8;t++){
   await p.evaluate(()=>{window.__t=[];});
   await p.waitForTimeout(600);
   const sobrou=await p.evaluate(()=>window.__t.length);
   if(!sobrou) break;
 }
 await p.evaluate(()=>{window.__t=[];});
 try{await p.evaluate(([k,f])=>{try{perfil={nome:'ANA',fig:(typeof ID!=='undefined'?ID.pre:'lt')+'_cr1'};}catch(e){}
   if(f) window[f](); else montaFase(k,function(){});},[i,forma.tipo==='mao'?forma.telas[i]:null]);}catch(e){continue;}
 await p.waitForTimeout(900);
 const ab=await p.evaluate(()=>window.__t);
 let dab=[]; for(let a=1;a<ab.length;a++) if(ab[a][0]-ab[a-1][0]<700) dab.push(ab[a-1][1]+' + '+ab[a][1]);
 if(dab.length){ruim++;console.log('fase',i+1,'ABERTURA -> JUNTOS:',dab.join(' , '));}
 await p.evaluate(()=>{window.__t=[];});
 const clicou=await p.evaluate(()=>{const c=document.querySelector('[data-qa="1"]');if(!c)return false;c.click();return true;});
 if(!clicou){continue;}
 await p.waitForTimeout(1400);
 const t=await p.evaluate(()=>window.__t);
 // sobreposicao = dois play() com menos de 700ms de diferenca
 let dup=[];
 for(let a=1;a<t.length;a++) if(t[a][0]-t[a-1][0]<700) dup.push(t[a-1][1]+' + '+t[a][1]);
 if(dup.length){ruim++;} if(dup.length) console.log('fase',i+1,'ACERTO ->',t.length,'audios | JUNTOS:',dup.join(' , '));
}
if(!ruim){console.log('voz ok: nenhuma fase toca duas vozes juntas (abertura e acerto)');}
process.exitCode = ruim?1:0;
await b.close();})();
