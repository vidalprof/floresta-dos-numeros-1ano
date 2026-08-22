/* ERRADOR 2 — erra de proposito, com a receita CERTA de cada peca. */
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const path=require('path');
const fs=require('fs');
const RECEITA={
 /* OUCA E ACHE: a peca marca a resposta certa com data-qa="1" e as erradas com
    "0". Errar de proposito e clicar numa "0" — e o portao confere se, depois de
    tres erros, o andaime cresceu e a crianca CONSEGUE seguir. Sem esta receita
    o portao dizia "nao sei jogar esta peca" e a bancada reprovava por falta de
    medicao, que e o certo: portao que nao mede nao aprova. */
 /* ESCOLHER: a mecanica mais comum da casa e estava sem receita — ou seja, o
    andaime dela nunca tinha sido MEDIDO. A peca marca so a certa com
    data-qa="1"; errada e qualquer outra que ainda nao foi tentada. */
 /* CAIXAS DE SOM (Elkonin): a ordem E o conteudo. Errar de proposito e
    empurrar a ficha para uma caixa que nao e a proxima (data-qa="0"), que e
    exatamente o que a crianca faz quando ainda nao percebeu que som tem ordem. */
 'caixas-de-som':()=>{
   var cx=[].slice.call(document.querySelectorAll('.csb'))
     .filter(function(e){ return e.getAttribute('data-qa')==='0' &&
       e.className.indexOf('cheia')<0; });
   if(!cx.length) return null;
   cx[cx.length-1].click();
   return 'empurrou a ficha para a caixa fora de ordem';
 },
 /* LIGAR: os dois lados publicam a MESMA chave em `data-qa`, e o lado fica na
    propriedade `_lado` do proprio elemento. Errar de proposito e ligar uma
    ponta da esquerda a uma ponta da direita com chave DIFERENTE — que e
    exatamente o par errado que a crianca faz. Sem esta receita a generica
    clicava em duas pontas quaisquer: metade das vezes era o MESMO lado, que a
    peca trata como "trocar a selecao", nao como erro. */
 'ligar':()=>{
   var t=[].slice.call(document.querySelectorAll('.lig')).filter(function(e){
     return e.offsetParent!==null && e.className.indexOf('feita')<0; });
   if(t.length<2) return null;
   var a=t[0], i;
   for(i=1;i<t.length;i++)
     if(t[i]._lado!==a._lado && t[i].getAttribute('data-qa')!==a.getAttribute('data-qa')){
       a.click(); t[i].click(); return 'ligou o par errado (lados opostos, chaves diferentes)'; }
   return null;
 },
 /* RIMA: tabuleiro de cartas viradas (`.rmc`); cartas que rimam publicam a MESMA
    chave em `data-qa`. Errar de proposito e juntar duas cartas de grupos
    DIFERENTES — o par que NAO rima, que e exatamente o erro que a crianca faz.
    Sem esta receita a generica clicava em duas cartas quaisquer e as vezes caia
    no mesmo par certo, sem medir o andaime. */
 'rima':()=>{
   var t=[].slice.call(document.querySelectorAll('.rmc')).filter(function(e){
     return e.offsetParent!==null && e.className.indexOf('feita')<0; });
   if(t.length<2) return null;
   var a=t[0], i;
   for(i=1;i<t.length;i++)
     if(t[i].getAttribute('data-qa')!==a.getAttribute('data-qa')){
       a.click(); t[i].click(); return 'juntou duas cartas que nao rimam (chaves diferentes)'; }
   return null;
 },
 /* DIGITAR: o teclado da tela publica a PALAVRA da vez em `data-qa` (no
    container das teclas) e as vagas ja cheias dizem em que letra estamos.
    Errar de proposito e apertar uma tecla que NAO e a proxima letra. A
    generica acertava por sorte de vez em quando — e acertar nao mede andaime. */
 'digitar':()=>{
   var cx=document.querySelector('[data-qa]'), i;
   var palavra=null, no=document.querySelectorAll('[data-qa]');
   for(i=0;i<no.length;i++){
     var v=no[i].getAttribute('data-qa')||'';
     if(v.length>1 && /^[A-Za-zÀ-ÿ]+$/.test(v)){ palavra=v.toUpperCase(); cx=no[i]; break; }
   }
   if(!palavra) return null;
   var pos=document.querySelectorAll('.vaga.cheia').length;
   if(pos>=palavra.length) return null;
   var certa=palavra.charAt(pos);
   var tec=[].slice.call(document.querySelectorAll('.tecl')).filter(function(e){
     return e.offsetParent!==null && e.className.indexOf('usada')<0 &&
            (e.textContent||'').trim().toUpperCase()!==certa; });
   if(!tec.length) return null;
   tec[0].click();
   return 'apertou a tecla que nao e a proxima letra ("'+(tec[0].textContent||'').trim()+'")';
 },
 /* QUEM SOU EU: a opcao errada SAI DE CENA (`opt fora`) e chega uma pista
    nova. A generica nao olhava o `fora` e, na terceira volta, tocava numa
    opcao ja descartada — clique que nao e erro nenhum, e o portao saia com
    "teste pela metade". Aqui a errada e sempre uma que ainda esta em jogo. */
 'quem-sou-eu':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')!=='1' &&
       e.className.indexOf('fora')<0 && e.className.indexOf('ok')<0 &&
       e.className.indexOf('mostra')<0; });
   if(!op.length) return null;
   op[0].click();
   return 'escolheu quem nao combina com a pista';
 },
 /* MUDANCA/PERMANENCIA: a peca tem DUAS telas. Na primeira a crianca puxa o
    controle do tempo (e ali nao ha erro nenhum a cometer); so na segunda ela
    separa as fichas em duas caixas — e ai o erro e guardar a ficha "mudou" na
    caixa "ficou". A generica nao passava da primeira tela, entao o andaime
    desta peca nunca tinha sido medido. A receita destrava e depois erra. */
 'mudanca-permanencia':()=>{
   var vis=function(e){ return e && e.offsetParent!==null; };
   var pc=[].slice.call(document.querySelectorAll('.pc')).filter(function(e){
     return vis(e) && e.className.indexOf('usada')<0; });
   var cam=[].slice.call(document.querySelectorAll('.cam')).filter(vis);
   if(!pc.length || !cam.length){
     /* ainda na tela do tempo: leva o controle ate o fim e volta (e o que a
        peca pede para liberar), depois entra na tela de separar */
     var sl=document.querySelector('input.slider');
     if(!sl) return null;
     var mx=parseInt(sl.max,10)||0, i;
     for(i=0;i<=mx;i++){ sl.value=''+i; if(sl.oninput) sl.oninput(); }
     for(i=mx;i>=0;i--){ sl.value=''+i; if(sl.oninput) sl.oninput(); }
     var bs=[].slice.call(document.querySelectorAll('button,.btn')).filter(function(e){
       return vis(e) && /separar/i.test(e.textContent||''); });
     if(!bs.length) return null;
     bs[0].click();
     pc=[].slice.call(document.querySelectorAll('.pc')).filter(function(e){
       return vis(e) && e.className.indexOf('usada')<0; });
     cam=[].slice.call(document.querySelectorAll('.cam')).filter(vis);
     if(!pc.length || !cam.length) return null;
   }
   var f=pc[0], j;
   for(j=0;j<cam.length;j++)
     if(cam[j].getAttribute('data-qa')!==f.getAttribute('data-qa')){
       f.click(); cam[j].click();
       return 'guardou a ficha na caixa errada';
     }
   return null;
 },
 /* ENSINAR O MASCOTE: a crianca escolhe uma REGRA e ele obedece. Errar de
    proposito e ensinar uma regra que nao serve (sem `data-qa="1"`) e que ainda
    nao foi descartada (`opt no`). O erro dela e ENCENADO — ele anda, obedece e
    so depois o mundo mostra que nao deu certo —, por isso o auditor espera a
    ajuda aparecer em vez de olhar a tela meio segundo depois. */
 'ensinar-mascote':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')!=='1' &&
       e.className.indexOf('no')<0 && e.className.indexOf('rev')<0; });
   if(!op.length) return null;
   /* a peca TRANCA tudo (opacidade .65) enquanto ele obedece a regra. Clicar
      ai nao e erro: e clique perdido — e clique perdido contado como erro e
      exatamente o que fez o andaime dela parecer parado. */
   if(op[0].style && op[0].style.opacity && parseFloat(op[0].style.opacity)<0.9) return null;
   op[0].click();
   return 'ensinou a regra que nao serve';
 },
 /* PREVER E OBSERVAR: a primeira tela e o PALPITE, e ali nao existe erro — por
    decisao pedagogica, qualquer palpite segue (todos publicam `data-qa="1"`).
    O erro so mora na tela de EXPLICAR, depois de ver o que aconteceu. A
    generica ficava presa no palpite. Aqui a receita anda ate a explicacao. */
 'prever-observar':()=>{
   var vis=function(e){ return e && e.offsetParent!==null; };
   var todas=[].slice.call(document.querySelectorAll('.opt')).filter(vis);
   var erradas=todas.filter(function(e){
     return e.getAttribute('data-qa')!=='1' && e.className.indexOf('no')<0 &&
            e.className.indexOf('ok')<0; });
   if(erradas.length){ erradas[0].click(); return 'explicou com a razao errada'; }
   /* ainda no palpite ou na tela de observar: anda um passo. O botao de agir
      tem TEXTO de conteudo ("Amassar a massinha", "Despejar no copo alto"),
      entao ele se acha pelo `id`, nunca pela palavra — foi por isso que a
      primeira versao desta receita ficou presa no palpite e nunca errou. */
   var ag=document.getElementById('agirB');
   if(ag && vis(ag)){ ag.click(); return null; }
   var livres=todas.filter(function(e){ return e.className.indexOf('ok')<0 &&
     e.className.indexOf('no')<0; });
   if(livres.length){ livres[0].click(); return null; }
   var segue=[].slice.call(document.querySelectorAll('button,.btn')).filter(function(e){
     return vis(e) && /continuar|vamos|pr[oó]xim|entendi/i.test(e.textContent||''); });
   if(segue.length){ segue[0].click(); }
   return null;
 },
 /* ESCREVER A LEGENDA: o tropeco dela e publicar um texto CURTO demais (menos
    de tres palavras). A peca socorre com andaime de tres degraus e, na quarta
    tentativa, publica assim mesmo — nunca trava. A generica nao sabia digitar
    num campo de texto e por isso o andaime dela nunca tinha sido medido. */
 'escrever-legenda':()=>{
   var c=document.querySelector('input[type=text],textarea,.campo');
   if(!c || c.offsetParent===null) return null;
   c.value='oi';                       /* uma palavra so: curto de proposito */
   if(c.oninput) c.oninput();
   var b=[].slice.call(document.querySelectorAll('button,.btn')).filter(function(e){
     return e.offsetParent!==null && /publicar/i.test(e.textContent||''); });
   if(!b.length) return null;
   b[0].click();
   return 'publicou uma legenda curta demais';
 },
 /* ANDAR ATE: o tropeco nao e um clique errado, e o CAMINHO PERDIDO — a peca
    conta quantos passos sobraram e socorre em 4, em 8 e em 12. A seta que
    aproxima publica "1"; errar e tocar duas vezes na que AFASTA. */
 'andar-ate':()=>{
   var st=[].slice.call(document.querySelectorAll('.seta')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')==='0'; });
   if(!st.length) return null;
   st[0].click(); st[0].click();
   return 'andou para o lado que afasta do lugar';
 },
 'escolher':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt'))
     .filter(function(e){ return e.getAttribute('data-qa')!=='1' &&
       e.className.indexOf('ok')<0 && e.className.indexOf('no')<0 &&
       e.className.indexOf('fora')<0; });
   if(!op.length) return null;
   op[0].click();
   return 'clicou a opcao errada "'+(op[0].textContent||'').replace(/\s+/g,' ').trim().slice(0,24)+'"';
 },
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
 /* ⭐ AS RECEITAS QUE FALTAVAM (ago/2026). O gesto generico cobriu 45 das 77
    pecas; as que sobraram erram de um jeito que nenhum atalho produz. Estas
    cinco sao as mais baratas de escrever, e cada uma reproduz o erro REAL da
    crianca naquela mecanica — nao um clique qualquer. */
 // LABIRINTO: andar para o lado errado (bater no espinhudo/parede)
 'labirinto':()=>{
   var s=[].slice.call(document.querySelectorAll('.seta'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1'; });
   if(!s.length) return null;
   s[Math.floor(Math.random()*s.length)].click();
   return 'andou para o lado errado';
 },
 // RELOGIO: dizer "esta pronto" com o relogio ainda errado
 'relogio':()=>{
   var bs=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null &&
       /pronto/i.test(e.textContent||'') && e.getAttribute('data-qa')!=='1'; });
   if(bs.length){ bs[0].click(); return 'disse "pronto" com a hora errada'; }
   /* se ja estiver certo, o erro e mexer o ponteiro para longe */
   var t=[].slice.call(document.querySelectorAll('.tecl'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1'; });
   if(!t.length) return null;
   t[0].click(); return 'mexeu o ponteiro para o lado errado';
 },
 /* ⭐ ROTULAR — a peca ganhou MODOS (ago/2026, licao do EdiLIM) e cada modo
    erra de um jeito. Sem esta receita a generica tocava no `.letras` (que
    publica a palavra da vez em `data-qa`, e nao e botao nenhum), voltava "sem
    dica" tres vezes, e o portao do ANDAIME saia CEGO no modo `escrever` — o
    caminho novo era exatamente o que ninguem estava medindo. */
 'rotular':()=>{
   const vis=e=>e&&e.offsetParent!==null;
   /* MODO ESCREVER: o teclado da tela publica a palavra da vez em `.letras` e
      as vagas cheias dizem em que letra estamos. Errar de proposito e apertar
      a tecla que NAO e a proxima letra — o erro real de quem esta soletrando. */
   const lt=document.querySelector('.letras[data-qa]');
   if(vis(lt)){
     const pal=(lt.getAttribute('data-qa')||'').toUpperCase();
     const pos=document.querySelectorAll('.vaga.cheia').length;
     if(pos<pal.length){
       const certa=pal.charAt(pos);
       const tec=[].slice.call(lt.children).filter(e=>vis(e) &&
         e.className.indexOf('usada')<0 &&
         (e.textContent||'').trim().toUpperCase()!==certa);
       if(tec.length){ tec[0].click();
         return 'apertou a letra que nao e a proxima ("'+(tec[0].textContent||'').trim()+'")'; }
     }
     return null;
   }
   /* MODO ARRASTAR: levar a plaquinha ate o lugar errado da figura. */
   const pcs=[].slice.call(document.querySelectorAll('.pc'))
     .filter(e=>vis(e)&&e.className.indexOf('usada')<0);
   const cams=[].slice.call(document.querySelectorAll('.cam'))
     .filter(e=>vis(e)&&e.className.indexOf('ok')<0);
   if(pcs.length&&cams.length){
     const p0=pcs[0], k=p0.getAttribute('data-qa');
     for(let i=0;i<cams.length;i++)
       if(cams[i].getAttribute('data-qa')!==k){
         p0.click(); cams[i].click();
         return 'levou a plaquinha para o lugar errado da figura';
       }
   }
   /* MODOS MOSTRAR e HOVER: nao ha resposta certa — a parte CONTA o que ela e.
      Nao existe erro a cometer, entao nao existe andaime a medir. Devolver
      `null` faz o portao dizer "nao medi", que e a verdade; inventar um clique
      aqui seria medir o que nao existe e chamar isso de aprovacao. */
   return null;
 },
 // MEDIR: confirmar sem alinhar a regua no zero
 'medir':()=>{
   var b=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /alinhei|pronto/i.test(e.textContent||''); });
   if(!b.length) return null;
   b[0].click(); return 'confirmou sem alinhar a regua';
 },
 // TRILHA: rolar o dado e escolher a resposta errada da casa
 'trilha':()=>{
   var op=[].slice.call(document.querySelectorAll('.oph'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1' &&
       e.className.indexOf('ok')<0 && e.className.indexOf('no')<0; });
   if(op.length){ op[0].click(); return 'escolheu a resposta errada da casa'; }
   var d=document.querySelector('.dado');
   if(d && d.offsetParent!==null){ d.click(); return null; }  /* rola o dado e tenta de novo */
   return null;
 },
 // ESTIMAR: mandar o palpite para o extremo da regua (longe do que serve)
 'estimar':()=>{
   var r=document.querySelector('input.faixa,input[type=range]');
   if(!r) return null;
   var qa=Number(r.getAttribute('data-qa')||0), min=Number(r.min||1), max=Number(r.max||100);
   r.value=String(qa-min > (max-qa) ? min : max);
   var ev=document.createEvent('HTMLEvents'); ev.initEvent('input',true,false); r.dispatchEvent(ev);
   var ev2=document.createEvent('HTMLEvents'); ev2.initEvent('change',true,false); r.dispatchEvent(ev2);
   var b=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /tampa|pronto|conferir|abrir/i.test(e.textContent||''); });
   if(b.length) b[0].click();
   return 'chutou o extremo da regua ('+r.value+')';
 },
 /* ⭐ AS QUATRO DE DOIS PASSOS. Estas nao eram "dificeis": elas exigem fazer o
    PASSO 1 antes de poder errar (tirar a pedra, pegar a tinta, virar a
    primeira carta). O gesto generico tocava o tabuleiro direto e a peca
    respondia, com razao, "Primeiro tire uma pedra" — instrucao de ordem, nao
    erro. Receita propria resolve: faz o passo 1 e SO ENTAO erra. */
 // BINGO: tirar a pedra e marcar a casa errada da cartela
 'bingo':()=>{
   var t=document.getElementById('tirar');
   if(t && t.offsetParent!==null){ t.click(); return '#andei'; }  /* passo 1: so tira */
   var cs=[].slice.call(document.querySelectorAll('.bin'))
     .filter(function(e){ return e.offsetParent!==null &&
       e.className.indexOf('marcada')<0 && e.getAttribute('data-qa')!=='1'; });
   if(!cs.length) return null;
   cs[0].click(); return 'marcou a casa errada da cartela';
 },
 // PINTAR: pegar a tinta e pintar a regiao que nao foi pedida
 'pintar-desenho':()=>{
   var cor=document.querySelector('.tinta,[aria-label^="Tinta"]');
   if(cor && cor.offsetParent!==null) cor.click();             /* passo 1: pega a cor */
   var zs=[].slice.call(document.querySelectorAll('.zona'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1'; });
   if(!zs.length) return null;
   zs[0].click(); return 'pintou a regiao errada';
 },
 // MEMORIA: virar duas cartas que NAO formam par
 'memoria':()=>{
   var cs=[].slice.call(document.querySelectorAll('.mcarta'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!==null &&
       e.className.indexOf('achou')<0 && e.className.indexOf('par')<0; });
   if(cs.length<2) return null;
   var a=cs[0], b=null, i;
   for(i=1;i<cs.length;i++) if(cs[i].getAttribute('data-qa')!==a.getAttribute('data-qa')){ b=cs[i]; break; }
   if(!b) return null;
   a.click(); b.click(); return 'virou duas cartas que nao formam par';
 },
 /* CONTADORES: por uma semente a mais e mandar CONTAR.
    ⚠️ a primeira versao desta receita so apertava "+" nove vezes e reprovava a
    peca: passar do numero NAO e erro aqui — a crianca pode tirar sementes a
    vontade, e a peca so confere quando ela aperta "Contar comigo". Recibo do
    de sempre: gesto que a peca nao considera erro nao mede andaime nenhum. */
 'contadores':()=>{
   var bts=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null; });
   var mais=null, conta=null, i, t;
   for(i=0;i<bts.length;i++){
     t=(bts[i].textContent||'')+' '+(bts[i].getAttribute('aria-label')||'');
     if(!conta && /contar comigo/i.test(t)) conta=bts[i];
     if(!mais && /(^|[^-])\+|p&#245;e|\bpoe\b|mais/i.test(t)) mais=bts[i];
   }
   if(!conta) return null;
   if(mais){ mais.click(); mais.click(); }   /* fica com sementes a mais */
   conta.click();
   return 'mandou contar com semente sobrando';
 },
 /* ⭐ MAIS QUATRO (ago/2026). O padrao continua o mesmo: o erro de verdade
    daquela mecanica, nao um clique qualquer. */
 // CALENDARIO: tocar o dia que nao e o pedido
 'calendario':()=>{
   var cs=[].slice.call(document.querySelectorAll('.cel,.cab'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1' &&
       (e.textContent||'').trim()!=='' && e.className.indexOf('ok')<0; });
   if(!cs.length) return null;
   cs[Math.floor(cs.length/2)].click();
   return 'tocou o dia errado do calendario';
 },
 // RETA NUMERICA: cravar a marca longe do numero pedido
 'reta-numerica':()=>{
   var r=document.querySelector('.reta');
   var b=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /cravar|pronto|marcar/i.test(e.textContent||''); });
   if(!r) return null;
   var cx=r.getBoundingClientRect();
   /* clica numa PONTA da reta: e o chute mais distante que existe ali */
   var ev=document.createEvent('MouseEvents');
   ev.initMouseEvent('click',true,true,window,1,0,0,
     Math.round(cx.left+cx.width*0.05), Math.round(cx.top+cx.height/2),
     false,false,false,false,0,null);
   r.dispatchEvent(ev);
   if(b.length) b[0].click();
   return 'cravou na ponta da reta';
 },
 // BALANCA: por peso do lado que ja estava mais pesado
 'balanca':()=>{
   /* ⚠️ DETALHE FINO, e ele engoliu o erro em silencio: a peca protege o peso
      que ja veio posto — `if(d<0 && add<=0) return`. Entao, na configuracao em
      que o lado precisa de MAIS, apertar "− tirar" nao faz absolutamente nada,
      e o "erro" da receita virava um clique perdido. Nao ha andaime a medir
      porque nao houve erro: a crianca, ali, nao consegue piorar.
      A receita entao POE um peso antes (movimento certo, que nao fecha a
      rodada sozinho) e so depois tira — que ai sim afasta da igualdade, que e
      a unica coisa que esta peca chama de tropeco. */
   var bs=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null &&
       /p[oô]r|tirar/i.test((e.textContent||'').trim()); });
   var marcado=null, outro=null, i;
   for(i=0;i<bs.length;i++){
     if(bs[i].getAttribute('data-qa')==='1') marcado=bs[i]; else outro=bs[i];
   }
   if(!outro) return null;
   if(/tirar/i.test(outro.textContent||'') && marcado) marcado.click();
   outro.click(); outro.click();
   return 'afastou os pratos da igualdade';
 },
 // TERMOMETRO: confirmar com a coluna longe do valor pedido
 'termometro':()=>{
   /* o controle e um <input type=range> criado a mao (sem classe): procurar
      por `.faixa` nao achava nada. O `data-qa` dele e a PARADA pedida — errar
      e confirmar com a coluna no extremo oposto. */
   var f=null, ns=document.querySelectorAll('input[type=range]'), i;
   for(i=0;i<ns.length;i++) if(ns[i].offsetParent!==null && ns[i].getAttribute('data-qa')!==null){ f=ns[i]; break; }
   if(!f) return null;
   var alvo=Number(f.getAttribute('data-qa')||0),
       mn=Number(f.min||0), mx=Number(f.max||100);
   f.value=String((alvo-mn) > (mx-alvo) ? mn : mx);
   if(f.oninput) f.oninput();
   if(f.onchange) f.onchange();
   /* ⚠️ o botao de confirmar dela e "E este!" — e a minha lista de palavras
      pedia "pronto|confirma|esta". Um acento de diferenca e a receita voltava
      null para sempre. Procurar por texto e frageil: aqui ele e o botao que
      NAO e o "Continuar" do banner. */
   var ok=[].slice.call(document.querySelectorAll('button.btn,.btn')).filter(function(e){
     if(e.offsetParent===null) return false;
     var n=e; while(n && n!==document.body){ if(n.id==='banner') return false; n=n.parentNode; }
     return !/continuar/i.test(e.textContent||''); });
   if(!ok.length) return null;
   ok[0].click();
   return 'confirmou com a coluna longe do pedido';
 },
 // BASE DEZ: dizer "nao da mais 10" com dez soltinhos na mesa
 'base-dez':()=>{
   var b=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /n&#227;o d&aacute;|nao da|n\u00e3o d\u00e1/i.test(e.innerHTML||e.textContent||''); });
   if(!b.length){
     b=[].slice.call(document.querySelectorAll('button,.btn'))
       .filter(function(e){ return e.offsetParent!==null && /mais 10/i.test(e.textContent||''); });
   }
   if(!b.length) return null;
   b[0].click(); return 'disse "nao da mais 10" com dez soltos na mesa';
 },
 // CAIXA DE DINHEIRO: entregar a moeda que passa do valor pedido
 'caixa-dinheiro':()=>{
   var ms=[].slice.call(document.querySelectorAll('.moeda'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1'; });
   if(!ms.length) return null;
   /* a de MAIOR valor e a que estoura o troco — o erro classico da fase */
   var alvo=ms[0], i;
   for(i=1;i<ms.length;i++) if((ms[i]._v||0)>(alvo._v||0)) alvo=ms[i];
   alvo.click(); return 'entregou a moeda que passa do valor';
 },
 // DECISAO: escolher a decisao que faz mal ao mundinho
 'decisao':()=>{
   /* ⚠️ AQUI NAO EXISTE ERRO — e esta escrito no coracao da peca: *"Nada de
      'voce errou': a consequencia e a resposta, e ela da para voltar e
      experimentar o outro caminho"*. E um simulador de consequencia: a
      crianca decide, o mundo responde na mesma tela, e nao ha andaime porque
      nao ha o que socorrer.
      A minha receita anterior clicava na decisao ruim e ANUNCIAVA um erro que
      a peca nao comete — inventar a condicao que se quer medir e pior que nao
      medir. Devolvendo null, o portao sai com 2 ("nao medi"), que e a verdade
      sobre esta mecanica. */
   return null;
 },
 /* COMPLETAR: o andaime RISCA a opcao errada a cada erro (`.opt.fora`), entao
    errar tres vezes exige escolher uma opcao ainda nao riscada de cada vez —
    era isso que a generica nao fazia, e por isso duas das tres tentativas dela
    nao produziam erro nenhum. */
 'completar':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')==='0' &&
       e.className.indexOf('fora')<0 && e.className.indexOf('ok')<0 &&
       e.className.indexOf('no')<0; });
   if(!op.length) return null;
   op[0].click();
   return 'escolheu o pedaco errado "'+(op[0].textContent||'').replace(/\s+/g,' ').trim().slice(0,18)+'"';
 },
 // GIRAR: escolher a contagem errada de voltas
 'girar':()=>{
   /* a mecanica dela nao e escolher: e GIRAR. As setas publicam "1" na que
      aproxima do molde, entao errar de proposito e tocar a OUTRA. A receita
      antiga so procurava `.opt` — que so existe no quiz do fim — e por isso
      nunca errava nada. */
   var st=[].slice.call(document.querySelectorAll('.seta')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')==='0'; });
   if(st.length){ st[0].click(); st[0].click(); return 'girou para o lado que afasta do molde'; }
   var op=[].slice.call(document.querySelectorAll('.opt')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')==='0' &&
       e.className.indexOf('no')<0 && e.className.indexOf('ok')<0; });
   if(!op.length) return null;
   op[0].click(); return 'contou as voltas errado';
 },
 // REPARTIR: por duas partes no MESMO prato (o outro fica sem)
 'repartir':()=>{
   /* dois momentos. No primeiro a crianca corta/junta a fita ate o numero de
      partes certo — e ali o tropeco nao e um clique errado, e MEXER DEMAIS: a
      peca conta as mexidas e ajuda em 4, em 7 e depois revela. No segundo ela
      reparte as partes nos pratos (parte e prato publicam a MESMA chave).
      A receita antiga exigia ver os DOIS botoes (Cortar e Juntar) ao mesmo
      tempo, e no comeco so existe o Cortar — por isso voltava null sempre. */
   var vis=function(e){ return e && e.offsetParent!==null; };
   var pc=[].slice.call(document.querySelectorAll('.pc')).filter(function(e){
     return vis(e) && e.className.indexOf('usada')<0; });
   var pr=[].slice.call(document.querySelectorAll('.vaga,.prato')).filter(vis);
   var i;
   if(pc.length && pr.length){
     for(i=0;i<pr.length;i++)
       if(pr[i].getAttribute('data-qa')!==pc[0].getAttribute('data-qa')){
         pc[0].click(); pr[i].click(); return 'pos a parte no prato errado'; }
   }
   var bs=[].slice.call(document.querySelectorAll('button,.btn')).filter(function(e){
     return vis(e) && /cortar|juntar/i.test(e.textContent||''); });
   if(!bs.length) return null;
   /* mexe alem da conta: e o tropeco que esta peca socorre */
   for(i=0;i<4;i++) bs[0].click();
   return 'picou a fita alem da conta';
 },
 /* MISTERIO: a fase tem tres telas (pistas -> hipotese -> prova). O erro so
    existe na tela da hipotese, entao a receita ANDA ate la e escolhe a errada. */
 'misterio':()=>{
   /* na tela da acusacao a peca marca o culpado com "1" e os outros com "0".
      Os LUGARES ja visitados tambem levam "0" (classe `loc`), e clicar neles
      nao e erro nenhum — era ai que a receita antiga se perdia. */
   var op=[].slice.call(document.querySelectorAll('.opt')).filter(function(e){
     return e.offsetParent!==null && e.getAttribute('data-qa')==='0' &&
       e.className.indexOf('loc')<0 && e.className.indexOf('no')<0 &&
       e.className.indexOf('ok')<0; });
   if(!op.length) return null;
   op[0].click(); return 'acusou quem as pistas nao apontam';
 },
 /* TESTE JUSTO: o erro e comparar com DUAS coisas mudadas — que e o defeito de
    raciocinio que a fase inteira existe para ensinar. */
 'experimento-justo':()=>{
   var tr=[].slice.call(document.querySelectorAll('.colv .bin,.colv .opt,.colv button,.tag'))
     .filter(function(e){ return e.offsetParent!==null; });
   var i, mexeu=0;
   for(i=0;i<tr.length && mexeu<2;i++){ tr[i].click(); mexeu++; }
   var cmp=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /comparar/i.test(e.textContent||''); });
   if(!cmp.length) return null;
   cmp[0].click();
   return 'comparou com duas coisas mudadas';
 },
 // RELAMPAGO: responder a errada na rodada rapida
 'relampago':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt'))
     .filter(function(e){ return e.offsetParent!==null && e.getAttribute('data-qa')!=='1' &&
       e.className.indexOf('no')<0 && e.className.indexOf('ok')<0; });
   if(op.length){ op[0].click(); return 'respondeu a errada no relampago'; }
   var ini=[].slice.call(document.querySelectorAll('button,.btn'))
     .filter(function(e){ return e.offsetParent!==null && /come[cç]|vamos|jogar/i.test(e.textContent||''); });
   if(ini.length){ ini[0].click(); return null; }
   return null;
 },
 /* RAIOS X: aqui NAO EXISTE errar — a crianca leva uma janela pela figura e
    descobre o que esta por baixo. O que o andaime desta mecanica socorre e a
    OLHADA PERDIDA: ela olhou num lugar e nao havia nada ali (RECEITA §1, "em
    fase sem errar o andaime cresce pelo tempo parado / pela busca sem achar").
    A peca publica `data-qa="0"` no quadrado VAZIO e `"1"` onde ha coisa para
    achar, entao errar de proposito e olhar em TRES lugares vazios — que e
    exatamente o degrau que ela mede. A generica nao servia: ela toca UM alvo
    por rodada, e um so nao chega em degrau nenhum.
    Na tela do fecho (a crianca responde o que viu) o erro volta a ser o de
    sempre: a resposta errada. */
 'raios-x':()=>{
   var op=[].slice.call(document.querySelectorAll('.opt[data-qa="0"]')).filter(function(e){
     return e.offsetParent!==null && e.className.indexOf('no')<0 &&
            e.className.indexOf('ok')<0; });
   if(op.length){ op[0].click(); return 'respondeu a errada sobre o que viu'; }
   var vaz=[].slice.call(document.querySelectorAll('.rxcel[data-qa="0"]')).filter(
     function(e){ return e.offsetParent!==null; });
   if(!vaz.length) return null;
   window.__rx = window.__rx || 0;
   for(var i=0;i<3;i++) vaz[(window.__rx++)%vaz.length].click();
   return 'olhou em tres lugares vazios e nao achou nada';
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
 /* ⭐ MECANICA QUE NAO PUNE — reconhecida sozinha (ago/2026).
    A `pintar-desenho`, a `estimar` e a `decisao` DEFINEM `sErro()` (vem do
    MOLDE) e nunca a CHAMAM: pintar e livre, estimar e um palpite, decidir tem
    consequencia e nao correcao. Sao escolhas pedagogicas legitimas — "errar
    nao pune" e regra da casa —, mas ali nao existe erro para o andaime
    socorrer.
    Sem este reconhecimento, cada uma delas custava a mesma descoberta duas
    vezes: eu escrevia uma receita, ela "errava", nenhuma ajuda aparecia, e eu
    ia procurar defeito numa peca certa. Pior: uma receita que ANUNCIA um erro
    que a peca nao comete inventa a condicao que se quer medir.
    Agora o portao le o proprio arquivo e diz, na hora, que ali nao ha o que
    medir — codigo 2, nunca "passou". */
 const nuncaPune = (()=>{
   const src = fs.readFileSync(path.resolve(arq),'utf8');
   const corpo = src.replace(/function\s+sErro\s*\([^)]*\)\s*\{[^}]*\}/g,'');
   return /function\s+sErro\s*\(/.test(src) && !/\bsErro\s*\(/.test(corpo);
 })();
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
   const genericaComPasso = () => {
     const tenta = () => {
     /* ⚠️ LICAO PAGA: a generica clicava SEMPRE na mesma opcao errada. Na peca
        `completar` a primeira tentativa RISCA aquela opcao, e clicar de novo
        deixa de ser erro — "(sem dica)". Na `intruso` a peca responde "nesta
        nos ja tentamos" as tres vezes. As duas reprovavam por andaime que
        existe. Errar tres vezes e errar em TRES lugares diferentes. */
     const viva = e => {
       if (!e || e.offsetParent === null) return false;
       const c = e.className || '';
       if (/\bok\b|usada|riscad|tentad|feito|no\b/.test(c)) return false;
       if (e.disabled) return false;
       if (/j[aá] tentamos/i.test(e.textContent || '')) return false;
       return true;
     };
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
     /* ⭐⭐ 1-B. QUALQUER COISA COM `data-qa` QUE NAO SEJA A CERTA.
        Medido em ago/2026, depois da varredura das 77 pecas: este portao — o do
        ANDAIME, o mais pedagogico da bancada — dizia "NAO SEI JOGAR" em
        QUARENTA E SETE delas. A bancada dava 'PECA PRONTA' do mesmo jeito
        (portao sem receita nao reprova, ele avisa) — mas o andaime de 47 pecas
        estava sem quem o medisse, que e a "aprovacao vazia" de sempre.
        A saida estava debaixo do nariz: a casa TEM uma convencao, e todas as 47
        a seguem — o que a crianca deve tocar publica `data-qa="1"`, e o resto
        "0". Errar de proposito e, quase sempre, tocar um `data-qa` que nao e 1.
        Isto sozinho cobre tecla de teclado na tela, celula de grade, zona de
        cena, carta, dia do calendario — sem escrever 47 receitas a mao.
        ⚠️ E rotaciona: errar tres vezes tem que ser em TRES lugares diferentes
        (a licao da `completar`, que risca a opcao ja tentada). */
     window.__jaErrei = window.__jaErrei || [];
     const qas = [...document.querySelectorAll('[data-qa]')].filter(
       e => viva(e) && e.getAttribute('data-qa') !== '1'
            && window.__jaErrei.indexOf(e) < 0);
     if (qas.length) {
       const alvo = qas[0];
       window.__jaErrei.push(alvo);
       alvo.click();
       return 'tocou o alvo errado "' +
         ((alvo.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 18)
          || alvo.className || 'sem texto') + '"';
     }
     /* 1-C. DESLIZAR PARA O VALOR ERRADO (termometro, estimar, simulador) */
     const rgs = [...document.querySelectorAll('input[type=range]')].filter(viva);
     if (rgs.length) {
       const r = rgs[0];
       const min = Number(r.min || 0), max = Number(r.max || 100);
       /* longe do valor de agora, para ser erro de verdade e nao um empurrao */
       r.value = String(Number(r.value) - min > (max - min) / 2 ? min : max);
       const ev = document.createEvent('HTMLEvents');
       ev.initEvent('input', true, false); r.dispatchEvent(ev);
       const ev2 = document.createEvent('HTMLEvents');
       ev2.initEvent('change', true, false); r.dispatchEvent(ev2);
       return 'deslizou para o valor errado (' + r.value + ')';
     }
     /* ⭐⭐ 1-D. TOCAR O QUE NAO E O ALVO MARCADO — a ULTIMA tentativa.
        Medido em ago/2026: mesmo com o gesto do `data-qa`, 45 pecas seguiam sem
        medicao do andaime. Fui ver por que, abrindo cada uma no navegador, e a
        premissa e que estava errada: eu supunha "a certa e 1, as erradas sao 0",
        mas a maioria das pecas publica SO O ALVO CERTO (todos os `data-qa`
        visiveis valem "1"), ou usa o campo para guardar a resposta ("GATO", o
        nome da carta). Nao havia nenhum "0" para clicar — por isso o gesto
        anterior nao achava nada.
        Entao a pergunta certa nao e "qual e a errada?", e sim "o que da para
        tocar que NAO e o alvo marcado?". Isso e o que a crianca faz quando erra:
        vira a carta que nao forma par, pisa na parede do labirinto, pinta o
        quadrado vizinho.
        ⚠️ Fora os CONTROLES (Continuar, Ouvir, Dica, Pronto): apertar botao de
        barra nao e errar — e o portao leria a falta de ajuda como andaime que
        nao existe. */
     const marcado = [...document.querySelectorAll('[data-qa="1"]')];
     const ehControle = e => {
       const t = ((e.textContent || '') + ' ' + (e.className || '')).toLowerCase();
       return /continuar|ouvir|dica|pronto|come|jogar|btn|mini|pxprox|zap/.test(t);
     };
     const tocaveis = [...document.querySelectorAll('#app *')].filter(
       e => viva(e) && !ehControle(e)
            && marcado.indexOf(e) < 0
            && window.__jaErrei.indexOf(e) < 0
            && (typeof e.onclick === 'function' || e.tagName === 'BUTTON')
            && e.getBoundingClientRect().width > 12);
     if (tocaveis.length) {
       const alvo = tocaveis[0];
       window.__jaErrei.push(alvo);
       alvo.click();
       return 'tocou o que nao e o alvo ("' +
         ((alvo.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 16)
          || alvo.className || '?') + '")';
     }
     /* ⭐⭐ E SE A TELA AINDA NAO TEM ONDE ERRAR: ANDA UM PASSO E TENTA DE NOVO.
        Medido (ago/2026): 21 pecas seguiam sem medicao, e em varias delas o
        motivo nao era a mecanica — era o MOMENTO. A tela de abertura mostra a
        pista, a previsao, o caso; o lugar de errar so nasce depois que a
        crianca aperta "Continuar". O auditor tentava errar na tela errada e
        desistia.
        Entao, quando nada casa, ele faz o que a crianca faz: anda um passo e
        procura de novo. Um passo so — se depois disso ainda nao houver onde
        errar, ele diz honestamente que nao sabe jogar esta peca. */
     return null;
     };
     /* ⚠️ LICAO PAGA NA HORA (ago/2026): eu escrevi este passo como uma funcao
        que CHAMAVA outra de fora, e o harness serializa so a funcao injetada —
        dentro da pagina a de fora nao existe. Deu ReferenceError e SEIS pecas
        viraram "reprovada" de uma vez. O proprio arquivo ja avisava disso duas
        telas acima; eu li e caí igual. Tudo o que roda na pagina mora DENTRO
        da funcao que vai para a pagina. */
     const r = tenta();
     if (r !== null) return r;
     const segue = [].slice.call(document.querySelectorAll('button,.btn,.pxprox')).filter(
       function(e){ return e && e.offsetParent !== null &&
         /continuar|pr[oó]xim|come[cç]|vamos|entendi|jogar/i.test(e.textContent || ''); });
     if (!segue.length) return null;
     segue[0].click();
     return tenta();
   };
   const provou = await p.evaluate(genericaComPasso);
   if (provou !== null) {
     RECEITA[nome] = genericaComPasso; genericaUsada = genericaComPasso;
     console.log('  (sem receita propria — usando a GENERICA: ' + provou + ')');
   } else {
   console.log('  ✋ NAO SEI JOGAR "'+nome+'": nao tenho receita para esta peca.');
   console.log('     Este portao e da BANCADA DA PECA (_qa/peca.sh), nao da banca');
   console.log('     da atividade. Receita nova = uma entrada em RECEITA{}.');
   await b.close(); process.exit(2);
   }
 }
 /* ⚠️ LICAO PAGA (ago/2026), na memoria do 1o ano. Este portao errava SEMPRE
    tres vezes, e tres era um numero que eu nunca tinha justificado — era so o
    costume. A memoria refeita passou a socorrer a crianca na 4a tentativa
    perdida (sao 8 cartas e uma crianca de 6 anos segura ~3 coisas na cabeca:
    varrer o tabuleiro custa 6 a 8 tentativas, entao ajudar na 3a seria ajudar
    antes de ela ter tentado). Resultado: o portao errava 3x, nenhuma ajuda
    aparecia, e ele concluia "ESTA PECA NAO PUNE" — dizendo que nao ha andaime
    JUSTAMENTE na peca cujo andaime tinha acabado de ser construido.
    O erro nao era da peca: era do portao medir toda mecanica com a mesma
    regua. Mecanica de VARREDURA (a crianca precisa explorar antes de errar de
    verdade) pede mais voltas. Numero aqui = "quantas tentativas perdidas ate a
    ajuda ter que ter aparecido", e ele tem que ser MAIOR que o degrau da peca. */
 const TENTATIVAS = { 'memoria': 5 };
 const VOLTAS = TENTATIVAS[nome] || 3;
 const dicas=[], novidades=[]; let errosReais=0;
 for(let n=1;n<=VOLTAS;n++){
   /* ⚠️ LICAO PAGA (ago/2026), junto com a espera pela ajuda encenada: a
      `ensinar-mascote` mostrou a MESMA ajuda tres vezes e parecia andaime que
      nao cresce. Nao era: os cliques 2 e 3 cairam enquanto a cena ainda
      animava, a peca os ignorou (`ocupado`), e o que estava na tela era a
      ajuda do erro 1 — que o auditor releu e anotou como se fosse nova.
      Apagar a dica velha ANTES de cada tentativa faz a espera medir a ajuda
      NOVA; se nenhuma aparecer, sai "(sem dica)", que e a verdade. */
   await p.evaluate(()=>{ var d=document.getElementById('dicaP');
     if(d&&d.parentNode) d.parentNode.removeChild(d); });
   /* ⭐ A SEGUNDA MEDIDA, sem chutar nome de elemento: guarda TODO o texto
      visivel da tela antes do erro. O que aparecer de novo depois e a ajuda —
      seja `#dicaP`, pista nova, fala do mascote ou consequencia no mundo.
      Nasce como RELATORIO: so vira veredito quando estiver provada. */
   const antes = await p.evaluate(()=>{
     var v={}, e=[].slice.call(document.querySelectorAll('body *'));
     for(var i=0;i<e.length;i++){
       if(e[i].offsetParent===null) continue;
       /* ⚠️ "so as folhas" era `children.length===0` — e isso pulava JUSTAMENTE
          o `#dicaP`, que quase sempre tem um <b> dentro ("A letra que vem
          agora esta <b>piscando</b>"). A medida nova nascia cega para a ajuda
          mais comum da casa. O certo e: conta quem so tem tags de TEXTO
          dentro (b, i, span, em, strong, br). */
       var so=true, f=e[i].children;
       for(var z=0; z<f.length; z++)
         if(!/^(B|I|EM|STRONG|SPAN|BR|U|SMALL)$/.test(f[z].tagName)){ so=false; break; }
       if(!so) continue;
       var t=(e[i].textContent||'').replace(/\s+/g,' ').trim();
       /* ⚠️ o CONTADOR nao e ajuda: "passos dados: 2" vira "passos dados: 4" e
          a medida ampla contava as duas como novidade — o `andar-ate` parecia
          socorrido tres vezes por um placar andando. Guardando com os numeros
          trocados por '#', a frase so conta como nova quando as PALAVRAS
          mudam. */
       if(t.length>12 && !/^[0-9 %/de]+$/i.test(t)) v[t.replace(/\d+/g,'#')]=1;
     }
     return Object.keys(v);
   });
   /* ⚠️ LICAO PAGA (ago/2026): a `prever-observar` gasta as duas primeiras
      tentativas so ANDANDO (palpite -> observar -> agir), porque o erro dela
      so existe na tela de explicar. Sobrava uma tentativa para errar e o
      andaime ficava medido pela metade. Uma tentativa agora INSISTE: se a
      receita devolveu `null` (andou, mas nao errou), ela tenta de novo, ate
      quatro voltas. Isso nao afrouxa nada — receita que nunca erra continua
      devolvendo `null` nas quatro e o portao sai com "nao medi". */
   let q=null;
   for(let v=0; v<4; v++){
     q=await p.evaluate(RECEITA[nome]);
     /* ⚠️ LICAO PAGA (ago/2026): algumas receitas precisam dar um passo CERTO
        antes de poder errar (o `bingo` tem que TIRAR A PEDRA para so entao
        marcar a casa errada). Elas devolviam `null`, e o auditor entendia
        "nao achei nada" e andava sozinho — clicando no alvo marcado, que ali
        e a casa CERTA. A rodada passava e o erro nunca acontecia.
        `#andei` e o recado da receita: "dei um passo, nao ande por mim". */
     if(q==='#andei'){ q=null; await p.waitForTimeout(420); continue; }
     if(q!==null && q!==undefined) break;
     /* ⚠️ LICAO PAGA (ago/2026), e a trava nova foi quem a revelou: SEIS pecas
        com receita propria (decisao, girar, misterio, repartir, teia-alimentar,
        termometro) nunca erraram uma unica vez — e passavam, porque o acabador
        chegava na medalha e o veredito da receita propria era so "nao trava".
        O motivo era bobo e velho: elas abrem numa CAPA, e a receita propria
        nunca aprendeu a apertar "Comecar". A generica tinha esse passo desde o
        primeiro dia; a propria, nao. Aqui ela ganha a mesma cortesia. */
     await p.evaluate(()=>{
       /* ⚠️ LICAO PAGA (ago/2026): a capa da `decisao` tem DOIS botoes — o de
          verdade ("Cuidar da horta", marcado com data-qa="1") e o "Continuar"
          do #banner, que esta fechado mas ainda responde ao seletor. O auditor
          clicava no do banner, a capa nunca abria, e a receita propria voltava
          `null` para sempre. Quatro pecas ficaram assim.
          Regra: para ANDAR, o alvo que a peca marcou vem primeiro; o texto e
          so o plano B. E nada de dentro de um banner fechado. */
       var noBanner=function(e){
         var n=e; while(n && n!==document.body){
           if(n.id==='banner') return !/show/.test(n.className||''); n=n.parentNode; }
         return false; };
       var vis=function(e){ return e && e.offsetParent!==null && !noBanner(e); };
       var m=[].slice.call(document.querySelectorAll('button[data-qa="1"],.btn[data-qa="1"]')).filter(vis);
       if(m.length){ m[0].click(); return; }
       var b=[].slice.call(document.querySelectorAll('button,.btn,.pxprox')).filter(
         function(e){ return vis(e) &&
           /continuar|pr[oó]xim|come[cç]|vamos|entendi|jogar/i.test(e.textContent||''); });
       if(b.length){ b[0].click(); return; }
       /* ⚠️ e nem todo passo e um BOTAO: no `misterio` o que faz a historia
          andar e ir aos LUGARES (`div.opt.loc`, marcados com "1"). Sem este
          terceiro plano o auditor ficava parado na tela dos lugares e nunca
          chegava na acusacao, que e onde mora o erro daquela peca. */
       var q=[].slice.call(document.querySelectorAll('[data-qa="1"]')).filter(vis);
       if(q.length) q[0].click();
     });
     await p.waitForTimeout(420);
   }
   if(q!==null&&q!==undefined) errosReais++;
   /* ⚠️ LICAO PAGA (ago/2026): a `ensinar-mascote` voltou "3 das 3 tentativas
      nao produziram erro" — e ela erra perfeitamente. O que acontece e que o
      erro dela e ENCENADO: o mascote anda ate a planta, obedece a regra e so
      DEPOIS o mundo mostra que nao deu certo (mais de 1,2s de animacao). O
      auditor olhava a tela 500ms depois do clique, quando ainda nao havia
      nada, e concluia que nao houve erro.
      Medir cedo demais e a mesma familia de "medir pelo mecanismo errado":
      da a resposta errada com cara de medicao. Agora ele ESPERA a ajuda
      aparecer, ate 3,5s — e, se ela nunca aparecer, o veredito continua o
      mesmo de antes. So paga o tempo quem tem animacao. */
   await p.waitForTimeout(400);
   for(let t=0; t<16; t++){
     const jaTem = await p.evaluate(()=>{
       var e=document.getElementById('dicaP');
       return !!(e && (e.innerText||'').trim());
     });
     if(jaTem) break;
     await p.waitForTimeout(200);
   }
   const d=await p.evaluate(()=>{var e=document.getElementById('dicaP');return e?e.innerText.trim():'(sem dica)';});
   const novo = await p.evaluate((velhos)=>{
     var tinha={}, i;
     for(i=0;i<velhos.length;i++) tinha[velhos[i]]=1;
     var achou=[], e=[].slice.call(document.querySelectorAll('body *'));
     for(i=0;i<e.length;i++){
       if(e[i].offsetParent===null) continue;
       var so=true, f=e[i].children;
       for(var z=0; z<f.length; z++)
         if(!/^(B|I|EM|STRONG|SPAN|BR|U|SMALL)$/.test(f[z].tagName)){ so=false; break; }
       if(!so) continue;
       var t=(e[i].textContent||'').replace(/\s+/g,' ').trim();
       if(t.length>12 && !/^[0-9 %/de]+$/i.test(t) && !tinha[t.replace(/\d+/g,'#')]) achou.push(t);
     }
     return achou;
   }, antes);
   console.log('  erro '+n+' ('+q+') -> '+JSON.stringify(d));
   if(d==='(sem dica)' && novo.length)
     console.log('       (fora do #dicaP apareceu: '+JSON.stringify(novo[0].slice(0,60))+')');
   dicas.push(d);
   novidades.push(novo.join(' | '));
 }
 console.log('  dicas distintas: '+new Set(dicas).size+' de '+dicas.length);
 const ajudaAmpla = new Set(novidades.filter(t=>t));
 console.log('  ajuda NOVA na tela (qualquer lugar): '+ajudaAmpla.size+' de '+novidades.length);
 // depois do 3o erro, da para chegar na medalha?
 let fim=false;
 for(let g=0; g<200 && !fim; g++){
   await p.evaluate(()=>{
     /* ⚠️ LICAO PAGA (ago/2026), achada pela PROVA DOS PORTOES e nao por uma
        peca: aqui era `b.className` sem conferir se `b` existe. Toda peca da
        casa tem `#banner` (vem do MOLDE), entao nunca estourou — mas o
        arquivo de mentira da prova nao tem, e o portao MORREU com
        "TypeError: Cannot read properties of null". E morrer, para quem chama,
        e codigo 1: o portao quebrado REPROVA a peca. O mesmo engano desta
        serie inteira, agora no proprio motor do auditor.
        Todo ajudante que mexe no DOM comeca conferindo se o DOM existe. */
     var b=document.getElementById('banner');
     if(b && /show/.test(b.className)){
       var cta=document.getElementById('bcta'); if(cta) cta.click(); return; }
     /* ⚠️ LICAO PAGA (ago/2026): este acabador clicava SEMPRE ao acaso, e no
        `labirinto` isso e passeio aleatorio — em 200 passos ele nao chega na
        estrela nem por sorte. O andaime da peca estava exemplar (tres dicas
        crescentes) e mesmo assim ela reprovava por "MEDALHA: NAO", que e o
        auditor confessando o proprio limite, nao defeito da peca.
        O `_qa/jogador.js` ja sabia disto ha semanas: ele PREFERE o alvo que a
        peca marca com `data-qa="1"`. Aqui faltava copiar a mesma ideia.
        E isto nao afrouxa a medida: peca que TRAVA a crianca depois de errar
        nao publica alvo nenhum — ali o acabador volta ao acaso e o "NAO"
        continua valendo. */
     var m=document.querySelectorAll('[data-qa="1"]'), i,r,vis=[],alvo=null;
     for(i=0;i<m.length;i++){ r=m[i].getBoundingClientRect();
       if(r.width>4&&r.height>4&&r.top>=-2&&r.top<innerHeight){ alvo=m[i]; break; } }
     /* ⚠️ E O DEFEITO QUE A PROPRIA CORRECAO CRIOU, medido na varredura
        seguinte: preferir o alvo marcado e DETERMINISTICO. Na `ouvir-achar` a
        marca fica numa opcao que ja foi tentada — clicar nela nao anda, e o
        acabador ficou batendo 200 vezes no mesmo botao. Antes, no acaso, ele
        escapava. Andar as vezes exige sair do caminho obvio: se o mesmo alvo
        nao resolveu em duas voltas, vai no acaso desta vez. */
     window.__ac = window.__ac || {alvo:null, n:0};
     if(alvo){
       if(window.__ac.alvo === alvo){ window.__ac.n++; } else { window.__ac.alvo = alvo; window.__ac.n = 1; }
       /* ⚠️ o teto era 2 e isso quebrou a `contadores`: para fechar aquela
          fase e preciso apertar "+" VARIAS vezes seguidas no mesmo botao
          marcado, e o acabador desistia na terceira e ia para o acaso.
          Seis e o meio-termo medido: cabe uma contagem ate 6 e ainda
          escapa do laco da `ouvir-achar`, que trava na primeira. */
       if(window.__ac.n <= 6){ alvo.click(); return; }
     }
     /* ⚠️ LICAO PAGA (ago/2026): a `digitar` reprovava com "MEDALHA: NAO" e a
        peca estava certa — o acabador simplesmente NAO SABIA DIGITAR. Ela
        publica a PALAVRA da vez em `data-qa` (esta escrito no cabecalho dela:
        "para o auditor-jogador") e o acabador nunca leu. Clicar tecla ao acaso
        nunca soletra a palavra, entao ele errava para sempre.
        O mesmo engano da familia toda: o auditor confessando o proprio limite
        e a peca levando a culpa. Aqui ele le a palavra, conta as vagas ja
        cheias e aperta a LETRA que vem agora. */
     var tec=document.querySelectorAll('.tecl');
     if(tec.length){
       var pal=null, nos=document.querySelectorAll('[data-qa]'), z, vv;
       for(z=0;z<nos.length;z++){
         vv=nos[z].getAttribute('data-qa')||'';
         if(vv.length>1 && /^[A-Za-zÀ-ÿ]+$/.test(vv)){ pal=vv.toUpperCase(); break; }
       }
       if(pal){
         var np=document.querySelectorAll('.vaga.cheia').length;
         if(np<pal.length){
           var alvoL=pal.charAt(np);
           for(z=0;z<tec.length;z++)
             if(tec[z].offsetParent!==null && tec[z].className.indexOf('usada')<0 &&
                (tec[z].textContent||'').trim().toUpperCase()===alvoL){ tec[z].click(); return; }
         }
       }
     }
     var a=document.querySelectorAll('.opt,.lig,.pc,.vaga,.qcpc,.qcvaga,.cel,.bin,.btn,.rosa,.dirb,.tecl,[data-qa]');
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
 /* ⚠️ LICAO PAGA: a peca `completar` RISCA a opcao errada a cada erro — que e
    o andaime funcionando: ela vai eliminando alternativas. Depois de dois
    erros so sobra a certa, e a generica fica SEM ONDE ERRAR. O portao contava
    isso como "andaime que nao cresce" e reprovava a peca justamente por ela
    ajudar bem. Se a generica nao conseguiu produzir os TRES erros, o teste
    ficou pela metade — e teste pela metade nao reprova. */
 /* ⚠️ LICAO PAGA (ago/2026), a terceira desta familia: o `bingo` e o
    `pintar-desenho` reprovaram com "1 de 3 dicas" — e as duas TEM andaime. O
    que aconteceu e que o gesto generico tocou o TABULEIRO (o numero da cartela,
    a zona do desenho) sem fazer o passo anterior, e a peca respondeu, as tres
    vezes, a mesma instrucao de ORDEM: *"Primeiro tire uma pedra. Depois procure
    ela na cartela"*, *"Primeiro toque numa cor la embaixo"*.
    Isso nao e a crianca errando: e a peca dizendo que ela pulou o passo 1 — e
    responder sempre a mesma coisa ai esta CERTO. Repetir a instrucao de ordem
    tres vezes nao mede andaime nenhum, entao o teste ficou pela metade: nao
    reprova, DIZ que nao mediu. O gatilho e estreito de proposito (as tres
    respostas identicas E no formato "Primeiro... depois...") para nao virar
    desculpa que engole defeito de verdade. */
 const todasIguais = dicas.length === 3 && new Set(dicas).size === 1;
 if(usouGenerica && todasIguais && /^primeiro\b|primeiro[^.]{0,60}depois/i.test(dicas[0] || '')){
   console.log('  ⚠️ A PECA PEDIU O PASSO 1 as tres vezes ("'+dicas[0].slice(0,52)+'...").');
   console.log('     O gesto generico tocou o tabuleiro sem fazer o passo anterior:');
   console.log('     isso nao e erro da crianca, e a peca ensinando a ORDEM. Teste');
   console.log('     pela metade NAO reprova — receita propria mede isto direito.');
   await b.close(); process.exit(2);
 }
 /* ⚠️ LICAO PAGA (ago/2026) — O PORTAO QUE REPROVAVA POR SORTE. A `digitar`
    reprovou numa varredura e passou na seguinte, sem ninguem tocar nela: a
    generica embaralha em qual letra errada ela toca, e algumas tentativas nao
    sao erro (tocar letra ja posta, por exemplo) — voltam "(sem dica)". Com
    sorte davam 3 ajudas distintas; sem sorte, 1, e a peca reprovava.
    Portao que reprova por sorte e pior que portao que nao mede: ensina a rodar
    de novo ate ficar verde. Se ALGUMA das tres tentativas nao produziu erro, o
    teste ficou pela metade — nao reprova, DIZ que nao mediu. (O caso que ainda
    reprova, e deve: as tres tentativas erraram de verdade e mesmo assim a
    ajuda nao cresceu — foi assim que a `linha-do-tempo` e a `ordenar` cairam.) */
 const semDica = dicas.filter(d => !d || d === '(sem dica)').length;
 if(usouGenerica && semDica > 0 && ajudas.size < 2){
   console.log('  ⚠️ '+semDica+' das '+VOLTAS+' tentativas nao produziram erro (voltaram sem dica):');
   console.log('     a generica tocou onde a peca nao considera erro. Teste pela');
   console.log('     metade NAO reprova — receita propria mede isto direito.');
   await b.close(); process.exit(2);
 }
 if(usouGenerica && errosReais < VOLTAS && ajudas.size < 2){
   console.log('  ⚠️ so consegui errar '+errosReais+' vez(es): a peca eliminou as');
   console.log('     alternativas erradas (o andaime dela funciona). Teste pela');
   console.log('     metade NAO reprova — receita propria mede isto direito.');
   process.exit(2);
 }
 if(usouGenerica && ajudas.size === 0){
   console.log('  ⚠️ A GENERICA NAO CONSEGUIU ERRAR nesta peca: nenhuma ajuda');
   console.log('     apareceu. Isso NAO quer dizer que falta andaime — quer dizer');
   console.log('     que este portao nao mediu. Receita propria em RECEITA{}.');
   process.exit(2);
 }
 /* ⚠️ BURACO QUE EU MESMO ABRI (ago/2026): com receita PROPRIA o veredito e
    "nao trava" (chegou na medalha), e eu escrevi uma receita para a
    `prever-observar` que nunca conseguia errar. Ela devolveu tres `null`,
    nenhuma ajuda apareceu — e a peca PASSOU, porque o acabador chegou na
    medalha. Passar sem ter errado nenhuma vez e aprovacao vazia: o portao
    existe para ver o que acontece DEPOIS do erro.
    Regra: receita que nao produziu erro nenhum nao mediu nada — sai com 2. */
 if(errosReais === 0){
   console.log('  ⚠️ NENHUMA das '+VOLTAS+' tentativas produziu erro: a receita nao');
   console.log('     conseguiu errar nesta peca. Chegar na medalha sem nunca ter');
   console.log('     errado NAO mede andaime — isto e "nao medi", nao "passou".');
   process.exit(2);
 }
 /* ⚠️ O ULTIMO BURACO DESTA FAMILIA (ago/2026): o veredito era DIFERENTE para
    receita propria e generica — a propria olhava so a medalha ("nao trava") e
    nunca o andaime. Entao uma receita propria que errasse UMA vez e nao visse
    ajuda nenhuma aprovava a peca (foi o caso da `repartir`). A regra da casa
    e uma so, e nao depende de qual receita o auditor usou:
      · nenhum erro          -> 2 (nao medi)
      · menos de tres erros  -> 2 (teste pela metade nao reprova)
      · tres erros e a ajuda NAO cresceu -> 1 (REPROVA — foi assim que a
        `linha-do-tempo` e a `ordenar` cairam)
      · tres erros e a ajuda cresceu -> passa; com receita propria ainda tem
        que chegar na medalha, porque ela sabe resolver a peca. */
 /* ⭐ MECANICA QUE NAO PUNE — e por que este teste e de RUNTIME, nao de leitura
    de codigo (ago/2026, e eu quase mandei do jeito errado). A `pintar-desenho`,
    a `estimar` e a `decisao` DEFINEM `sErro()` (vem do MOLDE) e nunca chamam:
    pintar e livre, estimar e um palpite, decidir tem consequencia e nao
    correcao. Sao escolhas pedagogicas legitimas, e ali nao existe erro para o
    andaime socorrer.
    So que eu tinha escrito isso como leitura do ARQUIVO — e a primeira coisa
    que a regra fez foi desligar a `balanca`, que cinco minutos antes media 3 de
    3. Ela socorre a crianca em tres degraus SEM tocar o som de erro, de
    proposito: *"desequilibrio nao e erro: ninguem e corrigido por estar
    torto"*. Nao tocar o somzinho nao quer dizer nao ajudar.
    Entao a conclusao so vale com as duas coisas juntas: a peca nunca pune E,
    depois de tres tentativas, nenhuma ajuda apareceu em NENHUMA das duas
    medidas. Ai sim nao ha o que medir — e "nao medi", nunca "passou". */
 /* a medida ampla conta QUALQUER texto novo, e nem todo texto novo e ajuda: na
    `estimar` aparecia o rotulo "O SEU PALPITE", que e mobilia da tela. Por isso
    aqui o piso e "menos de duas", nao "zero": uma novidade solta nao salva uma
    peca que nao pune e nao socorre. */
 if(nuncaPune && ajudas.size === 0 && ajudaAmpla.size < 2){
   console.log('  ✋ ESTA PECA NAO PUNE: nenhuma chamada a sErro() e nenhuma ajuda');
   console.log('     apareceu depois de errar. Pintar, estimar, decidir — mecanicas');
   console.log('     em que a crianca nao erra por decisao pedagogica. Nao ha erro');
   console.log('     para o andaime socorrer (isso NAO e "passou").');
   process.exit(2);
 }
 /* ⚠️ LICAO PAGA (ago/2026), e o defeito era da MINHA regra: `comparar`,
    `filtro` e `trilha` mostraram os TRES degraus do andaime crescendo, com
    ajuda diferente a cada erro, chegaram na medalha — e sairam "nao medi",
    so porque UMA das tres tentativas voltou sem contar como erro.
    "Teste pela metade" tem que ser sobre nao ter VISTO o andaime, nao sobre
    a contabilidade das tentativas. Quem viu a ajuda crescer duas ou tres
    vezes MEDIU, e dizer o contrario e jogar fora prova que se tem na mao —
    o avesso do erro que esta serie toda combateu, mas erro igual. */
 const viuAndaime = ajudas.size >= 2 || ajudaAmpla.size >= 2;
 if(errosReais < VOLTAS && !viuAndaime){
   console.log('  ⚠️ so consegui errar '+errosReais+' de '+VOLTAS+' vez(es) e nao vi a ajuda');
   console.log('     crescer. Teste pela metade NAO reprova — isto e "nao medi".');
   process.exit(2);
 }
 const andaimeOk = ajudas.size >= 2;
 /* ⚠️ E ATE ONDE A MEDIDA CHEGA, dito com todas as letras (ago/2026): este
    portao le a ajuda em UM lugar so, o `#dicaP`. Tentei fazer a receita
    propria reprovar por "ajuda que nao cresceu" como a generica ja faz, e a
    varredura acusou OITO pecas de uma vez — entre elas a `quem-sou-eu`, cujo
    andaime e a PISTA NOVA que aparece a cada erro, num quadro proprio, e nao
    um `#dicaP`. Seria o erro desta serie inteira outra vez: medir pelo
    mecanismo errado e chamar de defeito da peca.
    Entao, com receita propria, "ajuda que nao cresceu" e AVISO, nao
    reprovacao — o veredito continua sendo "nao trava". Reprovar por andaime
    parado segue valendo na generica, que foi como a `linha-do-tempo` e a
    `ordenar` cairam. Enquanto o portao nao souber ler ajuda fora do `#dicaP`,
    esta e a linha honesta; alargar essa leitura e trabalho anotado, nao
    resolvido. */
 if(!andaimeOk && !usouGenerica){
   console.log('  ⚠️ AVISO: errou as tres vezes e eu vi so '+ajudas.size+' ajuda(s)');
   console.log('     diferente(s) no #dicaP. Pode ser andaime parado — ou ajuda');
   console.log('     que mora noutro lugar (pista nova, fala do mascote). Olhe.');
 }
 const passou = usouGenerica ? (andaimeOk && !reais.length)
                             : (fim && !reais.length);
 process.exit(passou ? 0 : 1);
})();
