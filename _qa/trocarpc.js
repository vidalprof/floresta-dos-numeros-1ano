// -*- coding: utf-8 -*-
/* ============================================================
 PORTAO DO "TROCAR NUMERO" A DISTANCIA — o interruptor da sala.

 Pedido do Marcos (set/2026): primeiro *"remova a opcao de trocar computador,
 para o aluno nao trocar e dar problema"*; depois, com uma maquina errada na
 frente dele: *"volte a opcao de trocar computador no pc dos alunos, pois tenho
 que trocar o de um, deixe essa opcao no painel, dai eu habilito quando quero e
 desabilito quando quero"*.

 O que ele cobra, medindo de verdade num Chromium com o Firebase SIMULADO (o
 container nao alcanca a rede, e nem deveria: o que importa aqui e a LOGICA):

  CONTROLE  1. a caixa aparece e o botao e alvo de dedo (>= 40px);
            2. no antigo, SEM o campo `trocarpc`, le como TRANCADO
               (compatibilidade: e o que esta no ar hoje);
            3. clicar TRANCA e PRESERVA o comando que estava no canal — este e o
               ponto perigoso: o `PUT` troca o no inteiro, e um descuido aqui
               apagaria o "auto-retomar" de quem reiniciar a maquina;
            4. liberar usa o campo "Enviar para" (so a maquina que ele digitou);
            5. mandar um comando normal NAO apaga o interruptor.

  ALUNO     6. sem campo / vazio -> link escondido; "todos" -> aparece;
            7. lista "7" so libera a maquina 7 (a 3 continua trancada);
            8. "07" casa com 7 (zero a esquerda, como o resto do controle);
            9. liga e desliga AO VIVO em menos de 3,2s, sem recarregar a pagina;
           10. o link, quando aparece, ABRE mesmo o campo do numero.

 ⚠️ POR QUE UM PORTAO E NAO "eu testei": porque isto e um interruptor de sala de
 aula. Se ele ligar e nao aparecer, ele fica de pe na frente da maquina sem poder
 consertar; se ele desligar e continuar aparecendo, a crianca troca o numero e a
 maquina some do controle. Os dois lados tem que ser MEDIDOS, e sempre que o
 canal `/lab/<sala>` mudar de formato, este arquivo tem que voltar a passar.

 Uso:  python3 -m http.server 8099   (na raiz do repositorio)
       node _qa/trocarpc.js
 Sai 0 se tudo passou, 1 se alguma medicao falhou.
 ============================================================ */

const {chromium}=require(require('path').join(__dirname,'..','node_modules','playwright'));
const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const BASE='http://127.0.0.1:8099/_lab/';

// stub de XMLHttpRequest: responde o NÓ do Firebase que a gente quiser e
// registra tudo que a página tentou gravar.
function stub(no){
  return `
  window.__REQ=[];
  (function(){
    var NO=${JSON.stringify(no)};
    function Fake(){ this.readyState=0; this.status=0; this.responseText=""; }
    Fake.prototype.open=function(m,u){ this._m=m; this._u=u; };
    Fake.prototype.setRequestHeader=function(){};
    Fake.prototype.abort=function(){};
    Fake.prototype.send=function(body){
      var self=this;
      window.__REQ.push({metodo:self._m,url:self._u,corpo:body||null});
      setTimeout(function(){
        self.readyState=4; self.status=200;
        if(self._m==="GET" && /\\/lab\\//.test(self._u)) self.responseText=JSON.stringify(NO);
        else if(self._m==="GET" && /labstatus/.test(self._u)) self.responseText="null";
        else self.responseText="{}";
        if(self.onreadystatechange) self.onreadystatechange();
      }, 10);
    };
    window.XMLHttpRequest=Fake;
  })();`;
}

async function abre(b, arquivo, no, extra){
  const ctx=await b.newContext({viewport:{width:700,height:900}});
  const pg=await ctx.newPage();
  const erros=[];
  pg.on('pageerror',e=>erros.push(String(e).slice(0,140)));
  await pg.addInitScript(stub(no));
  await pg.goto(BASE+arquivo+(extra||''));
  await pg.waitForTimeout(900);
  return {pg,ctx,erros};
}

(async()=>{
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  let falhas=0;
  const ok=(nome,cond,detalhe)=>{ console.log((cond?'  OK   ':'  FALHOU ')+nome+(detalhe?('  -> '+detalhe):'')); if(!cond) falhas++; };

  console.log('=== CONTROLE: nó SEM o campo (como está hoje no ar) ===');
  {
    const {pg,ctx,erros}=await abre(b,'controle.html',{id:'a1',acao:'voltar',alvo:'todos'});
    const r=await pg.evaluate(()=>({
      caixa:!!document.getElementById('cxTroca') && document.getElementById('cxTroca').offsetParent!==null,
      texto:document.getElementById('estTroca').textContent.trim(),
      botao:document.getElementById('btTroca').textContent.trim(),
      altBotao:Math.round(document.getElementById('btTroca').getBoundingClientRect().height)
    }));
    ok('sem erro de JS', erros.length===0, erros.join(' | '));
    ok('a caixa aparece', r.caixa);
    ok('diz bloqueado', /bloqueado/.test(r.texto), r.texto);
    ok('botao diz Liberar', /Liberar/.test(r.botao), r.botao);
    ok('alvo do dedo >= 40px', r.altBotao>=40, r.altBotao+'px');
    await ctx.close();
  }

  console.log('=== CONTROLE: nó JÁ liberado para "7" ===');
  {
    const {pg,ctx,erros}=await abre(b,'controle.html',{id:'a1',acao:'voltar',alvo:'todos',trocarpc:'7'});
    const r=await pg.evaluate(()=>({
      texto:document.getElementById('estTroca').textContent.trim(),
      botao:document.getElementById('btTroca').textContent.trim()
    }));
    ok('sem erro de JS', erros.length===0, erros.join(' | '));
    ok('diz LIBERADO para 7', /LIBERADO para 7/.test(r.texto), r.texto);
    ok('botao diz Bloquear', /Bloquear/.test(r.botao), r.botao);
    // clicar tranca de novo, preservando o comando
    await pg.click('#btTroca'); await pg.waitForTimeout(400);
    const put=await pg.evaluate(()=>window.__REQ.filter(q=>q.metodo==='PUT').pop());
    const corpo=put?JSON.parse(put.corpo):{};
    ok('o clique gravou PUT', !!put, put?put.url:'nenhum');
    ok('trancou (trocarpc vazio)', corpo.trocarpc==='', JSON.stringify(corpo));
    ok('PRESERVOU o comando do canal', corpo.id==='a1' && corpo.acao==='voltar', JSON.stringify(corpo));
    const dep=await pg.evaluate(()=>document.getElementById('estTroca').textContent.trim());
    ok('a tela voltou a dizer bloqueado', /bloqueado/.test(dep), dep);
    await ctx.close();
  }

  console.log('=== CONTROLE: liberar usa o campo "Enviar para" ===');
  {
    const {pg,ctx}=await abre(b,'controle.html',{id:'a1',acao:'voltar',alvo:'todos'});
    await pg.fill('#alvo','7');
    await pg.click('#btTroca'); await pg.waitForTimeout(400);
    const put=await pg.evaluate(()=>window.__REQ.filter(q=>q.metodo==='PUT').pop());
    const corpo=put?JSON.parse(put.corpo):{};
    ok('liberou so para a 7', corpo.trocarpc==='7', JSON.stringify(corpo));
    ok('preservou o comando', corpo.id==='a1', JSON.stringify(corpo));
    await ctx.close();
  }

  console.log('=== CONTROLE: mandar comando NAO apaga o interruptor ===');
  {
    const {pg,ctx}=await abre(b,'controle.html',{id:'a1',acao:'voltar',alvo:'todos',trocarpc:'7'});
    await pg.fill('#link','https://vidalprof.github.io/o-trem-do-alfabeto/');
    await pg.click('#abrir'); await pg.waitForTimeout(400);
    const put=await pg.evaluate(()=>window.__REQ.filter(q=>q.metodo==='PUT').pop());
    const corpo=put?JSON.parse(put.corpo):{};
    ok('o comando levou trocarpc junto', corpo.trocarpc==='7' && corpo.acao==='abrir', JSON.stringify(corpo));
    await ctx.close();
  }

  const casos=[
    {no:{id:'a1',acao:'voltar'},                pc:'7', espera:false, nome:'sem o campo -> trancado (compatibilidade)'},
    {no:{id:'a1',acao:'voltar',trocarpc:''},    pc:'7', espera:false, nome:'vazio -> trancado'},
    {no:{id:'a1',acao:'voltar',trocarpc:'todos'},pc:'7',espera:true,  nome:'todos -> aparece'},
    {no:{id:'a1',acao:'voltar',trocarpc:'7'},   pc:'7', espera:true,  nome:'so a 7, e esta E a 7 -> aparece'},
    {no:{id:'a1',acao:'voltar',trocarpc:'7'},   pc:'3', espera:false, nome:'so a 7, e esta e a 3 -> NAO aparece'},
    {no:{id:'a1',acao:'voltar',trocarpc:'07'},  pc:'7', espera:true,  nome:'"07" casa com 7 (zero a esquerda)'},
    {no:{id:'a1',acao:'voltar',trocarpc:'3,7,9'},pc:'7',espera:true,  nome:'lista com virgula -> aparece'},
  ];
  console.log('=== ALUNO: o link "trocar numero" ===');
  for(const c of casos){
    const {pg,ctx,erros}=await abre(b,'index.html',c.no,'?sala=sala1&pc='+c.pc);
    await pg.waitForTimeout(600);
    const r=await pg.evaluate(()=>{
      const a=document.getElementById('trocarpc');
      return {tem:!!a, visivel:!!(a&&a.offsetParent!==null), rodape:(document.getElementById('rodape').textContent||'').trim()};
    });
    ok(c.nome, r.visivel===c.espera, 'visivel='+r.visivel+' | '+r.rodape+(erros.length?(' | ERRO '+erros[0]):''));
    await ctx.close();
  }

  console.log('=== ALUNO: o link ABRE mesmo o campo do numero ===');
  {
    const {pg,ctx,erros}=await abre(b,'index.html',{id:'a1',acao:'voltar',trocarpc:'todos'},'?sala=sala1&pc=7');
    await pg.waitForTimeout(500);
    await pg.click('#trocarpc'); await pg.waitForTimeout(300);
    const r=await pg.evaluate(()=>{
      const s=document.getElementById('setpc'), i=document.getElementById('inpc');
      return {campo:!!(s&&s.offsetParent!==null), valor:i?i.value:null,
              alt:i?Math.round(i.getBoundingClientRect().height):0};
    });
    ok('o campo do numero abriu', r.campo);
    ok('ja vem com o numero atual', r.valor==='7', String(r.valor));
    ok('sem erro de JS', erros.length===0, erros.join(' | '));
    await ctx.close();
  }

  console.log('=== ALUNO: liga e desliga AO VIVO, sem recarregar ===');
  {
    const ctx=await b.newContext({viewport:{width:700,height:900}});
    const pg=await ctx.newPage();
    const erros=[]; pg.on('pageerror',e=>erros.push(String(e)));
    await pg.addInitScript(`
      window.__NO={id:'a1',acao:'voltar'};
      (function(){
        function Fake(){ this.readyState=0; this.status=0; this.responseText=""; }
        Fake.prototype.open=function(m,u){ this._m=m; this._u=u; };
        Fake.prototype.setRequestHeader=function(){}; Fake.prototype.abort=function(){};
        Fake.prototype.send=function(){ var s=this; setTimeout(function(){
          s.readyState=4; s.status=200; s.responseText=JSON.stringify(window.__NO);
          if(s.onreadystatechange) s.onreadystatechange(); },10); };
        window.XMLHttpRequest=Fake;
      })();`);
    await pg.goto(BASE+'index.html?sala=sala1&pc=7');
    await pg.waitForTimeout(800);
    let vis=await pg.evaluate(()=>{const a=document.getElementById('trocarpc');return !!(a&&a.offsetParent!==null);});
    ok('comeca trancado', vis===false);
    await pg.evaluate(()=>{ window.__NO={id:'a1',acao:'voltar',trocarpc:'todos'}; });
    await pg.waitForTimeout(3200);   // o poll e de 2,5s
    vis=await pg.evaluate(()=>{const a=document.getElementById('trocarpc');return !!(a&&a.offsetParent!==null);});
    ok('LIGOU sozinho em menos de 3,2s', vis===true);
    await pg.evaluate(()=>{ window.__NO={id:'a1',acao:'voltar',trocarpc:''}; });
    await pg.waitForTimeout(3200);
    vis=await pg.evaluate(()=>{const a=document.getElementById('trocarpc');return !!(a&&a.offsetParent!==null);});
    ok('DESLIGOU sozinho em menos de 3,2s', vis===false);
    ok('sem erro de JS', erros.length===0, erros.join(' | '));
    await ctx.close();
  }

  await b.close();
  console.log(falhas? ('\n>>> '+falhas+' FALHA(S)') : '\n>>> TUDO PASSOU');
  process.exit(falhas?1:0);
})();
