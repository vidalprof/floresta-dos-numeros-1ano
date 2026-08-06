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
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
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
/* o que a crianca precisa TOCAR para a fase andar */
const RESPOSTA='.opt,.tecl,.lig,.cel,.bandeja,.mcard,.bin,.gbt,.btn,.pc,.peca';
/* tudo que a crianca pode TOCAR — inclui os botoes de apoio (dica, ouvir,
   alto-falante) e os alvos das mecanicas. Usado so na regra 5.            */
const CLICAVEL=RESPOSTA+',button,.marca,.cam,.mbt,.ajudabtn,.zap,.dbt';

(async()=>{
  const arquivo=process.argv[2];
  const telas=process.argv.slice(3);
  if(!arquivo||!telas.length){ console.log("uso: node _qa/leiaute.js <arquivo.html> <tela...>"); process.exit(2); }
  const b=await chromium.launch({executablePath:CROMO,args:['--no-sandbox','--disable-gpu']});
  const url='file://'+path.resolve(arquivo);
  let falhas=[];

  for(const vp of TAMANHOS){
    const p=await b.newPage({viewport:{width:vp.w,height:vp.h}});
    p.on('pageerror',()=>{});
    for(const t of telas){
      await p.goto(url); await p.waitForTimeout(280);
      const ok=await p.evaluate(t=>{
        window.falar=function(){}; window.depoisDaFala=function(i,m,cb){setTimeout(cb,60);};
        if(typeof window[t]!=="function") return false; window[t](); return true;
      },t);
      if(!ok) continue;
      await p.waitForTimeout(650);
      const r=await p.evaluate(({sel,clic})=>{
        const out=[];
        const barra=document.getElementById("barra");
        const topoBarra=barra&&barra.getBoundingClientRect().height? barra.getBoundingClientRect().top : innerHeight;
        const tela=document.querySelector(".tela");
        /* se a tela ROLA, o que esta embaixo continua alcancavel — nao e defeito.
           O defeito da foto do Marcos era outro: nao rolava e a resposta sumia.  */
        const rola=tela? (tela.scrollHeight>tela.clientHeight+4) : false;
        const els=[...document.querySelectorAll("#app "+sel)].filter(e=>e.offsetParent!==null);
        let forams=0, atras=0, pequenos=0, grade=0;
        for(const e of els){
          const b=e.getBoundingClientRect();
          if(b.width<1||b.height<1) continue;
          if(b.left<-1||b.right>innerWidth+1) out.push("estoura na horizontal: ."+String(e.className).split(" ")[0]);
          if(!rola){
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
           cima; quem cuida dela e a regra 3, que sabe perdoar quando a tela rola. */
        const cl=[...document.querySelectorAll(clic)]
          .filter(e=>e.offsetParent!==null && !e.closest("#barra"));
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
          const rb=b.getBoundingClientRect(); if(rb.width<8) continue;
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
        return out;
      },{sel:RESPOSTA,clic:CLICAVEL});
      for(const m of r) falhas.push(vp.n+" | "+t+" | "+m);
    }
    await p.close();
  }
  await b.close();

  console.log(arquivo+" -> leiaute conferido em "+TAMANHOS.length+" tamanhos x "+telas.length+" telas");
  if(!falhas.length){ console.log("  leiaute ok: nada fora da tela, nada atras da barra, alvos grandes"); process.exit(0); }
  console.log("  "+falhas.length+" PROBLEMA(S):");
  for(const f of falhas) console.log("   "+f);
  process.exit(1);
})();
