/* ============================================================
   AUDITOR DE LEIAUTE — "cabe na tela e da para tocar?"
   Nasceu de um erro pago (foto do Marcos, ago/2026): numa janela
   baixa (~360px de altura) as OPCOES DE RESPOSTA ficavam FORA da
   tela. A crianca via so o enunciado e nao sabia que havia o que
   responder. O print de uma tela so nao pega isso — tem que medir
   em VARIOS tamanhos.

   O que ele reprova:
     1. algo que estoura na HORIZONTAL (a tela nao rola de lado);
     2. RESPOSTA fora da area visivel (o pior: parece que acabou);
     3. resposta ESCONDIDA atras da barra de baixo (Ouvir/Dica);
     4. alvo de toque pequeno demais (<40px) para dedo de crianca;
     5. BOTAO SOBRE BOTAO (pedido do Marcos, ago/2026): dois alvos que
        se cobrem — a crianca mira num e o dedo aciona o outro;
     6. CARTA DE MEMORIA pequena (regra permanente do Marcos, ago/2026):
        toda .mcarta tem que ter no minimo 130 x 88 px;
     7. FIGURA MAIOR QUE O LUGAR DELA (ago/2026): <img> que estoura o pai
        posicionado — foi a lousa gigante em cima da planta da sala;
     8. BOTAO EM CIMA DO TEXTO (ago/2026): o alto-falante da pergunta cobrindo
        a ultima palavra do enunciado;
     9. COISA ENCOSTANDO NO ENUNCIADO (ago/2026, cobrado DUAS vezes): o que
        vem logo abaixo do balao precisa de 6px de folga — colado, entra na
        sombra do balao e parece um bloco so;
    10. FIGURA CORTADA NA CAIXA (ago/2026): `object-fit:cover` numa peca cuja
        proporcao nao bate com a da caixa — o topo do barril sumia.
   Rolagem vertical NAO e erro por si so — so e erro quando o que
   se toca fica fora.

   Uso: node _qa/leiaute.js _doceria/index.html tela1 tela2 ...
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

const CROMO='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
/* tamanhos reais: celular velho, celular comum, celular grande, PC da escola
   (janela com barras), PC em tela cheia, projetor/janela baixa */
const TAMANHOS=[
  {w:320,h:568,n:'celular pequeno'},
  {w:360,h:640,n:'celular comum'},
  {w:412,h:820,n:'celular grande'},
  {w:1366,h:640,n:'PC 1366 com barras'},
  {w:1366,h:768,n:'PC 1366 tela cheia'},
  {w:1024,h:420,n:'janela baixa'},
];
/* o que a crianca precisa TOCAR para a fase andar
   ⚠️ `.reta` entrou em ago/2026 (o Marcos pegou: "nao vi a regua como funcional").
   A regua da reta-numerica tem TODOS os filhos position:absolute, entao o div
   nao tem largura propria; dentro do motor (coluna flex align-center) ela
   COLAPSAVA para ~4px — uma tirinha invisivel que a crianca nao conseguia tocar.
   O jogador-robo passava (crava pelo data-alvo, sem coordenada) e o leiaute nao
   media a regua porque ela nao estava nesta lista. Agora esta: a regra 4 reprova
   a superficie interativa que encolheu abaixo de 40px. */
const RESPOSTA='.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.btn,.pc,.peca,.reta';
/* tudo que a crianca pode TOCAR — inclui os botoes de apoio (dica, ouvir,
   alto-falante) e os alvos das mecanicas. Usado so na regra 5.            */
const CLICAVEL=RESPOSTA+',button,.marca,.cam,.mbt,.ajudabtn,.zap,.dbt';

(async()=>{
  const arquivo=process.argv[2];
  const telas=process.argv.slice(3);
  if(!arquivo||!telas.length){ console.log("uso: node _qa/leiaute.js <arquivo.html> <tela...>"); process.exit(2); }
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const url='file://'+path.resolve(arquivo);
  let falhas=[], avisos=[];

  /* ⚠️⚠️ LICAO PAGA (ago/2026), e da familia do jogador cego: este portao —
     o que mede se CABE NA TELA e se DA PARA TOCAR — nunca tinha medido uma
     unica fase de atividade montada. Ele so sabe chamar tela pelo NOME
     (`window[t]()`), e as 32 fases nao sao funcoes globais: quem as desenha e
     o motor, com `montaFase(i)`. Os nomes que a banca passa incluem as funcoes
     internas das pecas (o integrador as inlina na coluna zero), e `window[t]`
     e `undefined` para todas elas — o portao pulava EM SILENCIO e ainda
     imprimia "38 telas", que parecia cobertura e era so a conta dos nomes
     tentados. Numero que parece medicao e nao e: a mesma aprovacao vazia de
     sempre.
     O `contraste.js` e o `imagens.js` ja tinham aprendido isso; aqui vai o
     mesmo caminho, e o relatorio passa a dizer quantas foram PULADAS. */
  const p0=await b.newPage({viewport:{width:412,height:820}});
  await p0.goto(url); await p0.waitForTimeout(400);
  const nfases=await p0.evaluate(()=>
    (typeof montaFase==="function" && typeof FASES!=="undefined") ? FASES.length : 0);
  await p0.close();
  const alvos=telas.map(t=>({nome:t}));
  for(let i=0;i<nfases;i++) alvos.push({fase:i});
  let puladas=0, medidas=0;

  for(const vp of TAMANHOS){
    const p=await b.newPage({viewport:{width:vp.w,height:vp.h}});
    p.on('pageerror',()=>{});
    /* ⚡ MEDIDO (set/2026, banca da Bancada da Divisao): este portao levava 239s
       porque RECARREGAVA a pagina inteira (700 KB + figuras) para CADA uma das
       6 x 40 telas — 240 recargas. A fase nao precisa de recarga: o motor a
       desenha por `montaFase(i)` em cima da pagina viva, e o proprio `limpa()`
       zera a tela anterior (e, desde set/2026, mata os relogios dela). So as
       telas COM NOME (capa, quem joga, fim) recarregam: elas leem o estado
       salvo (a retomada de 55 min) e sem recarga apareceriam diferentes do que
       a crianca ve ao abrir. */
    let carregada=false;
    for(const alvo of alvos){
      const t = (alvo.nome!==undefined) ? alvo.nome : ("fase"+(alvo.fase+1));
      if(!carregada || alvo.nome!==undefined){ await p.goto(url); await p.waitForTimeout(280); carregada=true; }
      const ok=await p.evaluate(a=>{
        window.falar=function(){}; window.depoisDaFala=function(i,m,cb){setTimeout(cb,60);};
        if(a.fase!==undefined){ try{ montaFase(a.fase,function(){}); return true; }
                                catch(e){ return false; } }
        if(typeof window[a.nome]!=="function") return false; window[a.nome](); return true;
      },alvo);
      if(!ok){ puladas++; continue; }
      medidas++;
      await p.waitForTimeout(650);
      const r=await p.evaluate(({sel,clic})=>{
        const out=[];
        const barra=document.getElementById("barra");
        const topoBarra=barra&&barra.getBoundingClientRect().height? barra.getBoundingClientRect().top : innerHeight;
        const tela=document.querySelector(".tela");
        /* se a tela ROLA, o que esta embaixo continua alcancavel — nao e defeito.
           O defeito da foto do Marcos era outro: nao rolava e a resposta sumia.  */
        /* ⚠️ (set/2026, lote das 88 pecas) na BANCADA da peca nao ha barra fixa
           (#barra) e quem rola e a PAGINA (body) — a linha-do-tempo era acusada
           de "3 respostas presas atras da barra" numa tela sem barra, so porque
           a pagina precisava rolar 60px. Pagina que rola, sem barra por cima,
           deixa tudo alcancavel. Com barra fixa a regra continua estrita: rolar
           a pagina nao tira a resposta de baixo da barra. */
        const semBarra=!(barra&&barra.getBoundingClientRect().height);
        const se=document.scrollingElement||document.documentElement;
        const paginaRola=semBarra && se && se.scrollHeight>innerHeight+4 &&
                         !/hidden/.test(getComputedStyle(document.body).overflowY+getComputedStyle(document.documentElement).overflowY);
        const rola=(tela? (tela.scrollHeight>tela.clientHeight+4) : false) || paginaRola;
        /* ⚠️ MEDICAO INCOMPLETA DO PROPRIO PORTAO (ago/2026): ele so perguntava
           se a TELA INTEIRA rola. Mas uma lista de respostas pode rolar POR
           DENTRO (`.opts{max-height;overflow-y:auto}`) — e ai o que esta embaixo
           continua alcancavel, que e o que importa. Sem isto o portao obrigava a
           deixar a tela inteira rolando, mesmo quando o desenho certo era a
           lista rolar dentro do seu lugar. Portao nao pode empurrar para um
           desenho pior. Agora ele olha CADA elemento e pergunta: existe algum
           pai meu que rola de verdade? */
        function paiRola(e){
          for(let a=e.parentElement; a && a.id!=="app"; a=a.parentElement){
            const c=getComputedStyle(a);
            if(/(auto|scroll)/.test(c.overflowY) && a.scrollHeight>a.clientHeight+4) return true;
          }
          return false;
        }
        /* ⚠️ DEFEITO DO PROPRIO PORTAO (ago/2026): estava `"#app "+sel`, e como
           `sel` e uma LISTA separada por virgula, so o PRIMEIRO seletor ficava
           preso ao #app — todo o resto varria a pagina inteira, inclusive o
           banner escondido la embaixo. Resultado: "resposta FORA da tela" numa
           tela que esta perfeita. Portao que acusa o inocente faz a gente
           desconfiar do certo, que e o pior estrago possivel.                */
        const els=[...document.querySelectorAll(sel.split(",").map(x=>"#app "+x.trim()).join(","))]
                    .filter(e=>e.offsetParent!==null);
        let forams=0, atras=0, pequenos=0, grade=0;
        for(const e of els){
          const b=e.getBoundingClientRect();
          if(b.width<1||b.height<1) continue;
          if(b.left<-1||b.right>innerWidth+1) out.push("estoura na horizontal: ."+String(e.className).split(" ")[0]);
          if(!rola && !paiRola(e)){
            if(b.top>=innerHeight-2) forams++;
            else if(b.bottom>topoBarra+2 && b.top<topoBarra) atras++;
          }
          /* quadro de letras/numeros: a grade INTEIRA precisa caber na tela, entao
             a celula nao pode ter 40px sempre. Piso menor, so para a grade.       */
          const naGrade=e.parentNode&&String(e.parentNode.className).indexOf("grade")>=0;
          if(naGrade){ if(b.height<30||b.width<30) grade++; }
          else if(b.height<40||b.width<40) pequenos++;
        }
        if(forams) out.push(forams+" resposta(s) FORA da tela SEM ROLAGEM (a crianca nao ve o que tocar)");
        if(atras) out.push(atras+" resposta(s) presa(s) atras da barra, sem rolagem");
        if(pequenos) out.push(pequenos+" alvo(s) menor(es) que 40px");
        if(grade) out.push(grade+" celula(s) de grade menor(es) que 30px");

        /* 5. BOTAO SOBRE BOTAO. Nao adianta comparar retangulos: botao dentro de
           caixa que ROLA tem retangulo fora da caixa mesmo estando escondido, e
           dava alarme falso. O teste honesto e o do DEDO — quem recebe o toque no
           centro do alvo? Se quem recebe nao e o proprio alvo (nem filho/pai
           dele), a crianca mira num botao e aciona outro.
           A barra de baixo (Ouvir/Dica) e camada FIXA de proposito e fica por
           cima; quem cuida dela e a regra 3, que sabe perdoar quando a tela rola.
           ⚠️ LICAO PAGA (ago/2026, pego no Detetive): o `#banner` (o "Continuar"
           do fim da fase) e overlay FIXO que fica `visibility:hidden` ate a fase
           acabar — mas escondido assim ele AINDA tem offsetParent, entao o botao
           dele passava o filtro e o `elementFromPoint` batia na `.tela` atras
           (banner tem pointer-events:none escondido). Resultado: "cta2 tapado por
           .tela" em TODA tela de moldura, um alarme falso. A regra 3 (resposta
           fora da tela) ja pulava `#banner`; a regra 5 tinha que pular tambem. */
        const cl=[...document.querySelectorAll(clic)]
          .filter(e=>e.offsetParent!==null && !e.closest("#barra") && !e.closest("#banner"));
        let sobre=0, exemplo="";
        for(const A of cl){
          const ra=A.getBoundingClientRect();
          if(ra.width<2||ra.height<2) continue;
          const cx=ra.left+ra.width/2, cy=ra.top+ra.height/2;
          if(cx<0||cy<0||cx>innerWidth||cy>innerHeight) continue;   // fora da tela: regra 2/3
          /* rolado para fora de uma caixa que rola: esta escondido, nao tapado */
          let clipado=false;
          for(let a=A.parentNode; a&&a.nodeType===1; a=a.parentNode){
            const ov=getComputedStyle(a).overflowY;
            if(ov==="auto"||ov==="scroll"||ov==="hidden"){
              const rc=a.getBoundingClientRect();
              if(cy<rc.top-1||cy>rc.bottom+1||cx<rc.left-1||cx>rc.right+1){ clipado=true; break; }
            }
          }
          if(clipado) continue;
          const hit=document.elementFromPoint(cx,cy);
          if(!hit) continue;                                        // escondido/clipado
          if(hit===A||A.contains(hit)||hit.contains(A)) continue;   // o dedo chega: ok
          if(hit.closest&&hit.closest("#barra")) continue;          // barra fixa: regra 3
          sobre++;
          if(!exemplo) exemplo="."+String(A.className).split(" ")[0]
                              +" tapado por ."+String(hit.className||hit.tagName).split(" ")[0];
        }
        if(sobre) out.push(sobre+" alvo(s) com BOTAO SOBRE BOTAO ("+exemplo+")");

        /* 6. CARTA DE MEMORIA GRANDE (regra permanente do Marcos, ago/2026:
           "quando fizer jogo da memoria faca cartas maiores"). A carta de
           memoria e o alvo mais dificil da atividade: a crianca tem que ver a
           figura, ler a palavra e ainda lembrar ONDE estava. Carta pequena
           mata as tres coisas. Piso: 130 x 88.                              */
        const mem=[...document.querySelectorAll(".mcarta")].filter(e=>e.offsetParent!==null);
        let pequenas=0, menor="";
        for(const m of mem){ const r=m.getBoundingClientRect();
          if(r.width<130||r.height<88){ pequenas++;
            if(!menor) menor=Math.round(r.width)+"x"+Math.round(r.height); } }
        if(pequenas) out.push(pequenas+" carta(s) de memoria pequena(s) demais, menor "+menor+" (minimo 130x88)");

        /* 7. FIGURA MAIOR QUE O LUGAR DELA (defeito que o Marcos fotografou,
           ago/2026: a planta da sala com a lousa e a mesa GIGANTES por cima do
           desenho). A causa nao e "classe sem CSS" — a classe TEM regra, so
           que dentro de outro pai; no pai novo ela fica sem tamanho e a <img>
           entra no tamanho natural. Nenhum portao via isso: o de classes acha
           a regra e aprova, e o de leiaute so olhava a TELA, nao o encaixe.
           Aqui: toda <img> dentro de um pai POSICIONADO (a vaga, o alvo) tem
           que caber nele. 15% de folga por causa de padding e sombra.      */
        const imgs=[...document.querySelectorAll("img")].filter(e=>e.offsetParent!==null);
        let estoura=0, qual="";
        for(const im of imgs){
          const pai=im.parentElement; if(!pai) continue;
          const ps=getComputedStyle(pai);
          if(ps.position!=="absolute"&&ps.position!=="relative") continue;
          if(ps.overflow==="hidden") continue;
          const a=im.getBoundingClientRect(), b2=pai.getBoundingClientRect();
          if(!b2.width||!b2.height) continue;
          if(a.width>b2.width*1.15||a.height>b2.height*1.15){
            estoura++;
            if(!qual) qual="."+String(im.className||"img").split(" ")[0]+" ("+Math.round(a.width)+"x"+Math.round(a.height)
                       +") dentro de ."+String(pai.className).split(" ")[0]+" ("+Math.round(b2.width)+"x"+Math.round(b2.height)+")";
          }
        }
        if(estoura) out.push(estoura+" figura(s) MAIOR(ES) que o lugar delas: "+qual);

        /* 8. BOTAO TAPANDO O TEXTO (ago/2026). O alto-falante da pergunta, que
           existe para ajudar quem NAO LE, pousou no canto do balao e cobriu a
           ultima palavra: "Toque na RAI[z]", "Que parte da planta e esta[?]".
           Botao de acessibilidade que esconde o texto e o contrario do que ele
           serve. A regra 5 so via botao sobre BOTAO; esta ve botao sobre LETRA.
           Mede o retangulo real das linhas de texto (Range), nao a caixa toda. */
        const tapa=[];
        for(const b of [...document.querySelectorAll(clic)]){
          if(b.offsetParent===null) continue;
          /* ⚠️ a BARRA FIXA de baixo (Ouvir/Dica) nao entra aqui: ela e camada
             fixa de proposito, e o texto que passa por baixo dela volta a
             aparecer com a rolagem. Quem cuida disso e a regra 3, que so
             reclama quando NAO ha rolagem. Esta regra e para o botao que anda
             JUNTO com o texto — como o alto-falante dentro do balao, que a
             rolagem nunca resolve.                                          */
          /* o BANNER de fim de fase e uma camada modal: cobrir o que esta
             atras dele e o trabalho dele, nao um defeito. */
          if(b.closest&&(b.closest("#barra")||b.closest("#banner"))) continue;
          /* ⚠️ LICAO PAGA (ago/2026): esta regra acusou `.opt tapando o texto de
             .hint` numa peca CERTA. O cartao estava dentro de uma lista que
             ROLA e, naquele momento, ROLADO PARA FORA — o navegador nao pinta
             um pixel dele ali. `getBoundingClientRect` devolve a posicao que o
             elemento TERIA; quem recorta e o pai que rola.
             Entao: antes de comparar, corta o retangulo do botao pelo recorte
             de cada pai que rola. Se nao sobra nada visivel, nao ha o que tapar.
             (Mesma familia do `paiRola`, que ja curou a regra 3.) */
          let rb=b.getBoundingClientRect(); if(rb.width<8) continue;
          for(let a=b.parentElement; a && a.id!=="app"; a=a.parentElement){
            const c=getComputedStyle(a);
            if(!/(auto|scroll|hidden)/.test(c.overflowY+" "+c.overflowX)) continue;
            const ra=a.getBoundingClientRect();
            rb={left:Math.max(rb.left,ra.left), right:Math.min(rb.right,ra.right),
                top:Math.max(rb.top,ra.top),   bottom:Math.min(rb.bottom,ra.bottom)};
            rb.width=rb.right-rb.left; rb.height=rb.bottom-rb.top;
          }
          if(!(rb.width>0&&rb.height>0)) continue;
          for(const cx of [...document.querySelectorAll(".balao,.hint,.selo,.pergunta,h1,h2")]){
            if(cx.offsetParent===null||cx.contains(b)===false&&b.contains(cx)) continue;
            for(const no of [...cx.childNodes]){
              if(no.nodeType!==3||!String(no.nodeValue).trim()) continue;
              const rg=document.createRange(); rg.selectNodeContents(no);
              for(const rt of rg.getClientRects()){
                const w=Math.min(rb.right,rt.right)-Math.max(rb.left,rt.left);
                const h=Math.min(rb.bottom,rt.bottom)-Math.max(rb.top,rt.top);
                if(w>0&&h>0&&w*h>120){
                  const q="."+String(b.className).split(" ")[0]+" tapando o texto de ."+String(cx.className).split(" ")[0];
                  if(tapa.indexOf(q)<0) tapa.push(q);
                }
              }
            }
          }
        }
        if(tapa.length) out.push(tapa.length+" BOTAO(OES) EM CIMA DO TEXTO: "+tapa[0]);

        /* 9. O ENUNCIADO ENCOSTANDO NO QUE VEM DEPOIS (ago/2026).
           Cobranca do Marcos DUAS vezes — a segunda com a paciencia curta, e
           com razao: *"na fase monte a legenda as opcoes de resposta estao
           encostando no enunciado"* e depois *"esse encosto no enunciado eu ja
           tinha comentado antes e pedido para nao acontecer"*.

           Da primeira vez eu consertei A FASE. Errado: a causa nao era da
           fase, era do motor — o balao tem sombra e nenhuma margem por baixo,
           entao QUALQUER coisa colada nele nasce grudada, e o defeito ia
           reaparecer na proxima tela que alguem montasse. Consertar o caso e
           deixar a causa e o mesmo que nao consertar.

           Agora e MEDIDO: o retangulo do enunciado tem que ter pelo menos 6px
           de folga ate o vizinho de baixo. Vale em toda fase e em todo tamanho
           de tela — inclusive nas atividades que ainda nem existem.          */
        const cola=[];
        for(const bl of [...document.querySelectorAll(".balao")]){
          if(bl.offsetParent===null) continue;
          const rb=bl.getBoundingClientRect(); if(rb.height<6) continue;
          let ir=bl.nextElementSibling;
          while(ir&&ir.offsetParent===null) ir=ir.nextElementSibling;
          if(!ir) continue;
          const ri=ir.getBoundingClientRect(); if(ri.height<6) continue;
          const folga=ri.top-rb.bottom;
          if(folga<6){
            const q="."+String(ir.className||ir.tagName).split(" ")[0]+
                    (folga<0?" SOBRE":" colado n")+"o enunciado (folga "+Math.round(folga)+"px)";
            if(cola.indexOf(q)<0) cola.push(q);
          }
        }
        if(cola.length) out.push(cola.length+" COISA(S) ENCOSTANDO NO ENUNCIADO: "+cola.join(" ; "));

        /* 10. FIGURA CORTADA DENTRO DO QUADRADO (ago/2026). Cobranca do Marcos:
           *"as imagens nao podem ficar cortadas dentro dos quadrados, precisam
           ser ajustadas"* — no porao do navio o topo do barril e a borda da
           bussola sumiam. A culpa e do `object-fit:cover`, que enche a caixa
           cortando o que sobra.

           Nao basta procurar `cover` no CSS: numa CENA que preenche a moldura
           (o mapa do vale, o fundo) o `cover` esta CERTO. O que decide e se a
           figura esta sendo REALMENTE cortada — isto e, se a proporcao dela
           bate com a da caixa. Por isso a regra MEDE, em vez de adivinhar:
           `cover` + proporcao diferente em mais de 12% = pedaco perdido.

           Cenas largas (>=300px de largura) ficam de fora: ali cortar a borda
           e o trabalho da moldura, nao um defeito.                          */
        const cortadas=[];
        for(const im of [...document.querySelectorAll("img")]){
          if(im.offsetParent===null) continue;
          const st=getComputedStyle(im);
          if(st.objectFit!=="cover") continue;
          const r=im.getBoundingClientRect();
          if(r.width<20||r.height<20||r.width>=300) continue;
          if(!im.naturalWidth||!im.naturalHeight) continue;
          const pn=im.naturalWidth/im.naturalHeight, pc=r.width/r.height;
          const perda=1-Math.min(pn,pc)/Math.max(pn,pc);
          if(perda>0.12){
            const q="."+String(im.className||"img").split(" ")[0]+" perde "+Math.round(perda*100)+"% da figura";
            if(cortadas.indexOf(q)<0) cortadas.push(q);
          }
        }
        if(cortadas.length) out.push(cortadas.length+" FIGURA(S) CORTADA(S) NA CAIXA: "+cortadas.join(" ; "));

        /* ============================================================
           REGRAS 11-14 — vieram da PESQUISA DAS CASAS DE REFERENCIA (set/2026,
           `_pesquisa/JOGOS-EDUCACIONAIS-REFERENCIAS.md` §3, aprovadas pelo
           Marcos: "pode fazer tudo"). Nascem como AVISO (o prefixo "AVISO"
           nao derruba a banca): primeiro se mede a casa inteira, depois a
           regra que nao acusa inocente vira reprovacao. Portao novo que ja
           nasce reprovando acusa inocente na primeira rodada — e portao que
           acusa inocente ensina a ignorar portao.                          */
        const tudo=[...document.querySelectorAll("#app *")].filter(e=>e.offsetParent!==null);
        const eAlvo=e=>{ try{ return e.matches(clic)||!!e.closest(clic); }catch(x){ return false; } };
        /* o nome da classe, tambem para SVG (la `className` e um objeto, nao texto) */
        const nomeDe=e=>"."+String((e.getAttribute&&e.getAttribute("class"))||e.tagName||"?").split(" ")[0];

        /* 11. ALVO RESPONDE AO PRESSIONAR (PBS KIDS "squish"; NN/g: a crianca
           precisa ver que o toque "pegou" em <=150 ms). Mede: o alvo (ou um
           pai proximo) casa com alguma regra CSS `:active`. Sem isso, no PC
           da escola sem som a crianca toca duas vezes, achando que nao foi. */
        const selsAct=[];
        for(const ss of [...document.styleSheets]){
          let rules; try{ rules=ss.cssRules; }catch(e){ continue; }
          for(const rr of [...rules]){
            if(!rr.selectorText||!/:active/.test(rr.selectorText)) continue;
            for(const s of rr.selectorText.split(",")){
              if(/:active/.test(s)){ const q=s.replace(/:active/g,"").trim(); if(q) selsAct.push(q); }
            }
          }
        }
        function temPressao(e){
          for(let a=e,n=0;a&&n<5&&a.id!=="app";a=a.parentElement,n++){
            if(a.tagName==="INPUT"||a.tagName==="SELECT"||a.tagName==="TEXTAREA") return true;
            for(const s of selsAct){ try{ if(a.matches(s)) return true; }catch(err){} }
          }
          return false;
        }
        const semPressao=new Set();
        for(const e of tudo){
          if(e.closest("#barra")||e.closest("#banner")) continue;
          const cs=getComputedStyle(e);
          if(!(eAlvo(e)||cs.cursor==="pointer")) continue;
          if(e.parentElement&&eAlvo(e.parentElement)&&!e.matches(clic)) continue;   // filho de alvo: quem responde e o pai
          const r=e.getBoundingClientRect(); if(r.width<20||r.height<20) continue;
          if(!temPressao(e)) semPressao.add(nomeDe(e));
        }
        if(semPressao.size) out.push("AVISO regra11: "+semPressao.size+" tipo(s) de alvo SEM resposta ao pressionar (:active): "+[...semPressao].slice(0,5).join(" "));

        /* 12. NADA ANIMA SEM FUNCAO (pilar "engajado", Hirsh-Pasek 2015: o que
           pisca e nao e alvo rouba atencao do que ensina). Mede: animacao
           INFINITA em coisa que nao e alvo, mascote, barra, progresso nem
           alto-falante. Animacao de entrada (uma vez) e ok.               */
        const anima=new Set();
        for(const e of tudo){
          const cs=getComputedStyle(e);
          if(!cs.animationName||cs.animationName==="none") continue;
          if(!/infinite/.test(cs.animationIterationCount)) continue;
          /* a barra de progresso (pgfill/pgcomet) e o mascote sao FUNCAO: mostram onde a
             crianca esta e quem fala com ela. O resto que pisca sem parar e enfeite. */
          if(e.closest("#mascote,.mascote,.masc,#masc,#barra,#banner,.prog,.pgbar,.pgfill,.pgcomet,#prog,.zap,.selo,.dica")) continue;
          if(eAlvo(e)||cs.cursor==="pointer") continue;
          /* o painel que PULSA enquanto a voz fala (`.falando`/`.tocando`) e o gemeo
             visual do som — funcao, nao enfeite */
          if(/falando|tocando/.test(String(e.getAttribute("class")||""))) continue;
          /* o que PULSA para dizer "e aqui" — a zona de soltar que esta na vez (.mira),
             o premio do labirinto (.prem), a casa acesa — e o andaime apontando, funcao */
          if(/\b(mira|prem|alvo|acesa|pisca|meta|agora)\b/.test(String(e.getAttribute("class")||""))) continue;
          anima.add(nomeDe(e));
        }
        if(anima.size) out.push("AVISO regra12: "+anima.size+" coisa(s) animando SEM funcao (nao e alvo nem mascote): "+[...anima].slice(0,5).join(" "));

        /* 13. FIGURA GRANDE RESPONDE AO TOQUE (NN/g: criancas tocam em TUDO e
           esperam resposta; a figura de >=80px que fica muda ensina que tocar
           nao adianta). Cena larga (>60% da tela) fica de fora: e fundo.    */
        const surdas=new Set();
        for(const im of [...document.querySelectorAll("#app img,#app svg,#app canvas")]){
          if(im.offsetParent===null) continue;
          const r=im.getBoundingClientRect();
          if(r.width<80||r.height<80||r.width>innerWidth*0.6) continue;
          if(im.closest("#mascote,.mascote,.masc,#masc,#banner")) continue;
          let ok=false;
          for(let a=im,n=0;a&&n<4&&a.id!=="app";a=a.parentElement,n++){
            if(a.onclick||a.getAttribute("onclick")||a.getAttribute("data-alvo")||a.getAttribute("draggable")==="true"
               ||eAlvo(a)||getComputedStyle(a).cursor==="pointer"||a.tagName==="CANVAS"||a.onpointerdown||a.ontouchstart||a.onmousedown){ ok=true; break; }
          }
          if(!ok) surdas.add(nomeDe(im));
        }
        if(surdas.size) out.push("AVISO regra13: "+surdas.size+" figura(s) grande(s) que NAO respondem ao toque: "+[...surdas].slice(0,5).join(" "));

        /* 14. NENHUMA RESPOSTA SO PELA COR (UDL / daltonismo). Irmaos de
           resposta sem figura e com o MESMO texto (ou nenhum) so se distinguem
           pela cor de fundo. Paleta de pintar fica de fora: ali escolher a cor
           E o conteudo.                                                     */
        const grupos=new Map();
        for(const o of [...document.querySelectorAll("#app .opt,#app .pc,#app .bin,#app .lig")]){
          if(o.offsetParent===null) continue;
          if(/cor|tinta|palet|swatch/i.test(String(o.className)+" "+String(o.parentElement&&o.parentElement.className))) continue;
          const k=o.parentElement; if(!grupos.has(k)) grupos.set(k,[]); grupos.get(k).push(o);
        }
        const soCor=[];
        for(const [pai,lista] of grupos){
          if(lista.length<2) continue;
          const vistos={}, cores={};
          for(const o of lista){
            if(o.querySelector("img,svg,canvas")) continue;
            const t=(o.textContent||"").replace(/\s+/g," ").trim().toLowerCase();
            vistos[t]=(vistos[t]||0)+1;
            (cores[t]=cores[t]||new Set()).add(getComputedStyle(o).backgroundColor+"|"+getComputedStyle(o).borderColor);
          }
          /* ⚠️ pecas IGUAIS (mesma cor, sem texto) sao MANIPULAVEIS — os blocos da
             base-dez, as fichas de contar — nao respostas a distinguir. So e "so
             pela cor" quando irmaos iguais no texto DIFEREM na cor. */
          for(const t in vistos){ if(vistos[t]>=2&&cores[t].size>=2){ soCor.push(nomeDe(lista[0])+(t?" texto repetido \""+t.slice(0,14)+"\"":" sem texto nem figura, so a cor muda")); break; } }
        }
        if(soCor.length) out.push("AVISO regra14: "+soCor.length+" grupo(s) de resposta que so se distinguem pela COR: "+soCor.slice(0,3).join(" ; "));
        return out;
      },{sel:RESPOSTA,clic:CLICAVEL});
      for(const m of r){ if(/^AVISO /.test(m)) avisos.push(vp.n+" | "+t+" | "+m); else falhas.push(vp.n+" | "+t+" | "+m); }
    }
    await p.close();
  }
  await b.close();

  /* o numero honesto: quantas telas ele ABRIU de verdade, e quantas nao
     conseguiu. "38 telas" contando nome tentado escondia 28 pulos. */
  const porTam = Math.round(medidas / TAMANHOS.length);
  console.log(arquivo+" -> leiaute conferido em "+TAMANHOS.length+" tamanhos x "
    +porTam+" tela(s) ("+telas.length+" por nome + "+nfases+" fase(s) pelo motor)");
  if(puladas){
    console.log("   "+Math.round(puladas/TAMANHOS.length)+" tela(s) por tamanho eu NAO consegui abrir "
      +"(nome que nao e funcao global — as funcoes internas das pecas entram na lista da banca).");
  }
  if(!medidas){
    console.log("   NAO MEDI NENHUMA TELA — isto nao e \"passou\".");
    await b.close(); process.exit(2);
  }
  /* os AVISOS (regras 11-14, da pesquisa) saem resumidos: uma linha por regra e
     por tela, nao por tamanho — e nao mudam o codigo de saida. */
  if(avisos.length){
    const porRegra={};
    for(const a of avisos){
      const m=a.match(/\| ([^|]+) \| AVISO (regra\d+): (.*)$/); if(!m) continue;
      const k=m[2]; (porRegra[k]=porRegra[k]||new Set()).add(m[1].trim()+": "+m[3]);
    }
    const ks=Object.keys(porRegra).sort();
    console.log("  "+avisos.length+" AVISO(S) das regras da pesquisa (nao reprovam ainda; ver JOGOS-EDUCACIONAIS-REFERENCIAS §3):");
    for(const k of ks){
      const l=[...porRegra[k]];
      /* quais TIPOS (classes) aparecem, somando as telas — e o que diz onde consertar */
      const tipos={};
      for(const x of l){ const m=x.match(/:\s*(.*)$/); if(!m) continue;
        for(const c of (m[1].split(": ").pop()||"").split(/[ ;]+/)){ if(/^\./.test(c)) tipos[c]=(tipos[c]||0)+1; } }
      const top=Object.keys(tipos).sort((x,y)=>tipos[y]-tipos[x]).slice(0,12).map(c=>c+"x"+tipos[c]);
      const telasK=[...new Set(l.map(x=>x.split(":")[0]))];
      console.log("   "+k+" em "+l.length+" tela(s) ["+telasK.slice(0,8).join(" ")+(telasK.length>8?" ...":"")+"]; tipos: "+top.join(" ")+"  | ex.: "+l[0]);
    }
  }
  if(!falhas.length){ console.log("  leiaute ok: nada fora da tela, nada atras da barra, alvos grandes"); process.exit(0); }
  console.log("  "+falhas.length+" PROBLEMA(S):");
  for(const f of falhas) console.log("   "+f);
  process.exit(1);
})();
