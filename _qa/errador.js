/* ERRADOR 2 — erra de proposito, com a receita CERTA de cada peca. */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');
const RECEITA={
 /* OUCA E ACHE: a peca marca a resposta certa com data-qa="1" e as erradas com
    "0". Errar de proposito e clicar numa "0" — e o portao confere se, depois de
    tres erros, o andaime cresceu e a crianca CONSEGUE seguir. Sem esta receita
    o portao dizia "nao sei jogar esta peca" e a bancada reprovava por falta de
    medicao, que e o certo: portao que nao mede nao aprova. */
 'ouvir-achar':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt'))
     .filter(function(e){ return e.getAttribute('data-qa')==='0' &&
       e.className.indexOf('ok')<0 && e.className.indexOf('no')<0; });
   if(!op.length) return null;
   op[0].click();
   return 'clicou a opcao errada "'+(op[0].textContent||'').replace(/\s+/g,' ').trim().slice(0,24)+'"';
 },
 // clica uma peca do banco e depois uma VAGA que nao e a dela
 'quebra-cabeca':()=>{
   var pcs=[].slice.call(document.querySelectorAll('.qcpc')).filter(function(e){return e.className.indexOf('usada')<0;});
   var vgs=[].slice.call(document.querySelectorAll('.qcvaga')).filter(function(e){return e.className.indexOf('cheia')<0;});
   if(!pcs.length||!vgs.length) return null;
   var sel=null,i;
   for(i=0;i<pcs.length;i++) if(pcs[i].className.indexOf('sel')>=0) sel=pcs[i];
   var p=sel||pcs[0], v=null;
   for(i=0;i<vgs.length;i++) if(!(vgs[i].li===p.li&&vgs[i].co===p.co)){v=vgs[i];break;}
   if(!v) return null;
   if(!sel) p.click(); v.click(); return 'peca '+p.li+'_'+p.co+' -> vaga '+v.li+'_'+v.co;
 },
 'arrastar-lugar':()=>{
   var pcs=[].slice.call(document.querySelectorAll('.pc')).filter(function(e){return e.className.indexOf('usada')<0&&e.className.indexOf('ok')<0;});
   var vgs=[].slice.call(document.querySelectorAll('.cam')).filter(function(e){return e.className.indexOf('ok')<0;});
   if(!pcs.length||!vgs.length) return null;
   var sel=null,i;
   for(i=0;i<pcs.length;i++) if(pcs[i].className.indexOf('sel')>=0) sel=pcs[i];
   var p=sel||pcs[0], v=null, pk=p.getAttribute('data-qa');
   for(i=0;i<vgs.length;i++) if(vgs[i].getAttribute('data-qa')!==pk){v=vgs[i];break;}
   if(!v) return null;
   if(!sel) p.click(); v.click(); return 'peca '+pk+' -> vaga '+v.getAttribute('data-qa');
 },
 'sombra':()=>{
   var ls=[].slice.call(document.querySelectorAll('.lig')).filter(function(e){return e.className.indexOf('feita')<0;});
   var e=null,d=null,i;
   for(i=0;i<ls.length;i++){ if(ls[i].className.indexOf('sel')>=0) e=ls[i]; }
   for(i=0;i<ls.length;i++){ if(ls[i]._lado==='e'&&!e) e=ls[i]; }
   for(i=0;i<ls.length;i++){ if(ls[i]._lado==='d'&&ls[i]._k!==(e&&e._k)) {d=ls[i];break;} }
   if(!e||!d) return null;
   if(e.className.indexOf('sel')<0) e.click(); d.click(); return 'liga '+e._k+' com '+d._k;
 },
 'simulador':()=>{
   var r=document.querySelector('input[type=range]');
   if(r){ var v=Number(r.value); r.value=String(v+1>10?0:v+1); r.oninput&&r.oninput(); r.onchange&&r.onchange();
          if(!r.oninput&&!r.onchange){ var ev=document.createEvent('HTMLEvents'); ev.initEvent('input',true,false); r.dispatchEvent(ev);} }
   var a=[].slice.call(document.querySelectorAll('.opt')).filter(function(e){return e.getAttribute('data-qa')==='0'&&e.className.indexOf('fora')<0;});
   if(!a.length) return null; a[0].click(); return 'opcao errada';
 },
 'coordenadas':()=>{
   var a=[].slice.call(document.querySelectorAll('[data-qa="0"]')).filter(function(e){var r=e.getBoundingClientRect();return r.width>4&&r.top<innerHeight&&e.className.indexOf('ok')<0;});
   if(!a.length) return null; a[0].click(); return 'errada';
 },
 // toca num pedaco que NAO e o proximo da palavra (isca, ou silaba fora de ordem)
 'juntar-silabas':()=>{
   var bs=[].slice.call(document.querySelectorAll('.jsSil')).filter(function(e){
     return e.className.indexOf('usada')<0 && e.getAttribute('data-qa')==='0';});
   if(!bs.length) return null; bs[0].click(); return 'pedaco '+bs[0].textContent;
 },
 // responde com a contagem ERRADA: apaga tudo e aperta Pronto com zero batidas
 'bater-silabas':()=>{
   var pr=document.querySelector('.bsPronto'); if(!pr) return null;
   if(pr.getAttribute('data-qa')==='1'){
     var lp=document.querySelector('.bsLimpa'); if(lp) lp.click();
   }
   pr.click(); return 'Pronto com a conta errada';
 },
 'bussola':()=>{
   var a=[].slice.call(document.querySelectorAll('[data-qa="0"]')).filter(function(e){var r=e.getBoundingClientRect();return r.width>4&&r.top<innerHeight&&e.className.indexOf('ok')<0;});
   if(!a.length) return null; a[0].click(); return 'errada';
 }
};
(async()=>{
 const arq=process.argv[2];
 const nome=path.basename(arq,'.html');
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--disable-gpu','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage({viewport:{width:412,height:820}});
 const jse=[]; p.on('pageerror',e=>jse.push(e.message));
 await p.goto('file://'+path.resolve(arq));
 await p.waitForTimeout(700);
 // simulador: precisa MEXER antes de responder (>=3 vezes)
 if(nome==='simulador'){
   await p.evaluate(()=>{ var r=document.querySelector('input[type=range]');
     for(var i=0;i<4;i++){ r.value=String(i+1); var ev=document.createEvent('HTMLEvents'); ev.initEvent('input',true,false); r.dispatchEvent(ev); } });
   await p.waitForTimeout(400);
 }
 let genericaUsada = null;
 console.log('ARQUIVO: '+arq);
 /* ⚠️⚠️ LICAO PAGA (ago/2026), e das que quase estragou a banca inteira: este
    portao so sabe jogar UMA PECA — ele escolhe a receita pelo NOME DO ARQUIVO
    (`_padrao/pecas/memoria.html` -> RECEITA['memoria']). Eu o liguei na banca da
    ATIVIDADE, cujo arquivo se chama `index.html`: nao ha receita com esse nome,
    `p.evaluate(undefined)` nao faz nada, e ele imprimia "erro 1 (undefined) ->
    (sem dica)" e "chegou na MEDALHA: NAO" para TODA atividade — inclusive o
    Jardim do Broto, que esta no ar e tem o andaime certo. Se eu o tivesse
    deixado bloquear, ele reprovaria tudo, sempre, por nao saber medir.
    Portao sem receita nao "reprova": ele DIZ que nao sabe. */
 /* ⭐⭐ RECEITA GENERICA — porque 59 das 65 pecas rodavam CEGAS aqui.
    Medido (ago/2026): a bancada das pecas dava codigo 0 em 65 pecas, e em 59
    delas ESTE portao — o do ANDAIME, que e a coisa mais pedagogica que a
    bancada mede — nao tinha medido NADA, por falta de receita. Codigo 0 com o
    portao mais importante cego e a "aprovacao vazia" que a casa ja aprendeu a
    nao aceitar.
    Escrever 59 receitas a mao seria trabalho de dias e envelheceria. Mas as
    pecas da casa erram de tres jeitos so, e os tres se reconhecem pelo DOM:
      · TOCAR a resposta errada  (data-qa="0", ou uma opcao que nao e a certa);
      · LEVAR a peca para a vaga errada (peca + vaga com data-qa diferente);
      · LIGAR o par errado.
    A generica tenta os tres, nesta ordem. Se nenhum casar, ai sim ela diz que
    nao sabe — e continua sem reprovar, porque portao sem receita nao reprova:
    ele DIZ que nao sabe. */
 if(typeof RECEITA[nome]!=='function'){
   /* ⚠️ ESTA funcao roda DENTRO da pagina — nada de `p` aqui. A primeira
      versao guardava o embrulho (que chama `p.evaluate`) dentro de RECEITA, e
      o harness o injetava na pagina: "ReferenceError: p is not defined". */
   const genericaNaPagina = () => {
     const viva = e => e && e.offsetParent !== null &&
       e.className.indexOf('ok') < 0 && e.className.indexOf('usada') < 0;
     /* 1. tocar a resposta ERRADA */
     const ops = [...document.querySelectorAll('.opt,.oaf,.escolha,.bin,.chip,.cubo,.coisa,.carta')].filter(viva);
     const marcadas = ops.filter(o => o.getAttribute('data-qa') !== null);
     if (marcadas.length > 1) {
       const erradas = marcadas.filter(o => o.getAttribute('data-qa') === '0');
       const alvo = erradas[0] || marcadas[marcadas.length - 1];
       alvo.click();
       return 'tocou a resposta errada "' +
         (alvo.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 22) + '"';
     }
     /* 2. levar a peca para a VAGA errada */
     const pcs = [...document.querySelectorAll('.pc,.qcpc,.pchip,.peca')].filter(viva);
     const vgs = [...document.querySelectorAll('.cam,.qcvaga,.vaga,.zona')].filter(viva);
     if (pcs.length && vgs.length) {
       const p0 = pcs.find(x => x.className.indexOf('sel') >= 0) || pcs[0];
       const k = p0.getAttribute('data-qa');
       const v0 = vgs.find(x => x.getAttribute('data-qa') !== k) || vgs[vgs.length - 1];
       if (v0 && v0 !== p0) {
         if (p0.className.indexOf('sel') < 0) p0.click();
         v0.click();
         return 'levou a peca para a vaga errada';
       }
     }
     /* 3. ligar o par ERRADO */
     const ls = [...document.querySelectorAll('.lig,.par')].filter(viva);
     if (ls.length > 2) {
       ls[0].click(); ls[ls.length - 1].click();
       return 'ligou o par errado';
     }
     return null;
   };
   const provou = await p.evaluate(genericaNaPagina);
   if (provou !== null) {
     RECEITA[nome] = genericaNaPagina; genericaUsada = genericaNaPagina;
     console.log('  (sem receita propria — usando a GENERICA: ' + provou + ')');
   } else {
   console.log('  ✋ NAO SEI JOGAR "'+nome+'": nao tenho receita para esta peca.');
   console.log('     Este portao e da BANCADA DA PECA (_qa/peca.sh), nao da banca');
   console.log('     da atividade. Receita nova = uma entrada em RECEITA{}.');
   await b.close(); process.exit(2);
   }
 }
 const dicas=[];
 for(let n=1;n<=3;n++){
   const q=await p.evaluate(RECEITA[nome]);
   await p.waitForTimeout(500);
   const d=await p.evaluate(()=>{var e=document.getElementById('dicaP');return e?e.innerText.trim():'(sem dica)';});
   console.log('  erro '+n+' ('+q+') -> '+JSON.stringify(d));
   dicas.push(d);
 }
 console.log('  dicas distintas: '+new Set(dicas).size+' de '+dicas.length);
 // depois do 3o erro, da para chegar na medalha?
 let fim=false;
 for(let g=0; g<200 && !fim; g++){
   await p.evaluate(()=>{
     var b=document.getElementById('banner');
     if(/show/.test(b.className)){ document.getElementById('bcta').click(); return; }
     var a=document.querySelectorAll('.opt,.lig,.pc,.vaga,.qcpc,.qcvaga,.cel,.bin,.btn,.rosa,.dirb,[data-qa]'), i,r,vis=[];
     for(i=0;i<a.length;i++){ r=a[i].getBoundingClientRect();
       if(r.width>4&&r.height>4&&r.top>=-2&&r.top<innerHeight) vis.push(a[i]); }
     if(vis.length) vis[Math.floor(Math.random()*vis.length)].click();
   });
   await p.waitForTimeout(160);
   fim=await p.evaluate(()=>!!document.querySelector('.medal'));
 }
 console.log('  chegou na MEDALHA depois de errar: '+(fim?'SIM':'NAO'));
 /* ⚠️ LICAO PAGA (ago/2026), no mesmo dia em que a generica nasceu: com a
    receita GENERICA, "nao chegou na medalha" NAO e defeito da peca — e limite
    do auditor. A generica sabe ERRAR de proposito (e o andaime, que e o que
    importa aqui, ela mede muito bem), mas nao sabe RESOLVER a peca depois.
    Medido no `arrastar-sombra`: 3 dicas distintas e crescentes — dica, "a
    sombra certa esta piscando", "deixa comigo: eu levo esta" — andaime
    exemplar, e mesmo assim "MEDALHA: NAO", porque o auditor continuou errando.
    Reprovar por isso seria mandar consertar o que esta certo.
    Entao: com receita propria, a medalha CONTA; com a generica, ela e
    INCONCLUSIVA e o veredito sai do andaime, que e o que foi medido de fato. */
 const usouGenerica = RECEITA[nome] === genericaUsada;
 if(usouGenerica && !fim){
   console.log('  (medalha INCONCLUSIVA: a receita generica sabe errar, nao sabe');
   console.log('   resolver. O veredito sai do ANDAIME, que foi medido de verdade.)');
 }
 /* o barulho do file:// nao conta: service worker so existe em http(s) */
 const reais=jse.filter(e=>!/ServiceWorker|protocol of the current origin/i.test(e));
 console.log('  ERROS JS: '+(reais.length?reais.join(' | '):'nenhum'));
 await b.close();
 /* ⚠️⚠️ LICAO PAGA, e das piores: este portao NAO TINHA `process.exit`. Ele
    imprimia "chegou na MEDALHA depois de errar: NAO" e saia com codigo ZERO —
    ou seja, RELATAVA A FALHA E A BANCA APROVAVA POR CIMA. Portao que nao reprova
    nao e portao, e comentario. E este e justamente o que existe para garantir o
    andaime da casa: errar tres vezes e AINDA ASSIM conseguir seguir.
    A regra que fica: todo portao novo precisa de um teste que o veja REPROVAR.
    So ver "passou" nao prova nada — pode ser que ele nunca reprove. */
 /* o andaime tem que CRESCER: ao menos duas ajudas diferentes em tres erros */
 const ajudas = new Set(dicas.filter(d => d && d !== '(sem dica)'));
 /* ⚠️ LICAO PAGA: a generica reprovou o `passo-a-passo` por "1 de 3 dicas" — e a
    peca TEM andaime de tres degraus, escrito no codigo. O que aconteceu foi que
    o gesto generico ("levar a peca para a vaga errada") nao conta como ERRO
    naquela mecanica: o auditor nao errou, entao nao havia ajuda a mostrar.
    Portao que nao consegue PRODUZIR a condicao que mede nao pode reprovar por
    nao te-la visto — tem que dizer que nao mediu. */
 if(usouGenerica && ajudas.size === 0){
   console.log('  ⚠️ A GENERICA NAO CONSEGUIU ERRAR nesta peca: nenhuma ajuda');
   console.log('     apareceu. Isso NAO quer dizer que falta andaime — quer dizer');
   console.log('     que este portao nao mediu. Receita propria em RECEITA{}.');
   process.exit(2);
 }
 const andaimeOk = ajudas.size >= 2;
 const passou = usouGenerica ? (andaimeOk && !reais.length)
                             : (fim && !reais.length);
 process.exit(passou ? 0 : 1);
})();
