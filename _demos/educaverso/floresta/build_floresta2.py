# -*- coding: utf-8 -*-
# EducaVerso — "A Floresta do Byte" (Etapa 1, versão incrível)
# Labirinto de pedra REAL. Chão = grama (IA). Paredes = muro de pedra (IA).
# Nimbo (vilão-nuvem) prende 3 amiguinhos; a criança poe SETAS de madeira no
# chao para guiar o Byte pelo labirinto ate a jaula. 3 missoes + 1 alivio.
import base64, os
S=os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f:
        return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
NM={"grama":"grama.png","muro":"muro.png","arvore":"arvore.png","byte":"byte.png",
    "gato":"gato.png","coelho":"coelho.png","passaro":"passarinho.png","nimbo":"nimbo.png",
    "jaula":"jaula.png","chave":"chave.png","seta":"seta.png","cabana":"cabana.png"}
A={("__%s__"%k.upper()):b64(v) for k,v in NM.items()}

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EducaVerso - A Floresta do Byte</title>
<style>
 html,body{margin:0;height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow:hidden;}
 #wrap{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;}
 h1{font-size:15px;margin:4px 0 0;letter-spacing:.3px;} .sub{font-size:11px;color:#9fb6df;margin:0 0 4px;}
 #frame{padding:7px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;}
 canvas{display:block;border-radius:10px;background:#3f7a34;max-width:96vw;height:auto;cursor:pointer;}
 #painel{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:6px;}
 .bt{font-family:inherit;font-weight:bold;border:0;border-radius:14px;cursor:pointer;padding:9px 16px;font-size:15px;color:#0a1120;-webkit-transition:transform .05s;transition:transform .05s;}
 .bt.vai{background:-webkit-linear-gradient(#bff7d6,#4fcf8e);background:linear-gradient(#bff7d6,#4fcf8e);box-shadow:0 3px 0 #2f9463;}
 .bt.vai:active{transform:translateY(2px);box-shadow:0 1px 0 #2f9463;}
 .bt.lp{background:linear-gradient(#ffd0d0,#f08a8a);box-shadow:0 3px 0 #b04d4d;}
 .bt.vz{background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;}
 .bt:disabled{opacity:.5;filter:grayscale(.5);cursor:default;}
</style></head><body><div id="wrap">
 <h1>&#127795; A Floresta do Byte</h1>
 <p class="sub">clique no ch&#227;o p/ p&#245;r as setas de madeira &#183; aperte VAI &#183; guie o Byte pelo labirinto at&#233; a jaula!</p>
 <div id="frame"><canvas id="tela" width="720" height="500"></canvas></div>
 <div id="painel">
   <button class="bt vai" id="bVai" onclick="vai()">&#9654; VAI!</button>
   <button class="bt lp" id="bLp" onclick="limpar()">&#128465; Limpar setas</button>
   <button class="bt vz" id="bSom" onclick="toggleSom()">&#128266; Som e Voz</button>
 </div>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC={grama:"__GRAMA__",muro:"__MURO__",arvore:"__ARVORE__",byte:"__BYTE__",gato:"__GATO__",
 coelho:"__COELHO__",passaro:"__PASSARO__",nimbo:"__NIMBO__",jaula:"__JAULA__",chave:"__CHAVE__",
 seta:"__SETA__",cabana:"__CABANA__"};
var IMG={},patG=null,patM=null,carreg=0,NN=0;for(var kk in SRC)NN++;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===NN)iniciar();};im.src=SRC[key];})(k);}

/* ---------- LABIRINTO ---------- */
var GW=9,GH=7,CELL=62,OX=(VW-GW*CELL)/2,OY=40,LIFT=13;
function cellPx(gx,gy){return [OX+gx*CELL+CELL/2, OY+gy*CELL+CELL/2];}
var MIS=[
 {friend:"gato", nome:"o Gato Pigo",
  maze:["#########","#S......#","#######.#","#.......#","#.#######","#......J#","#########"],
  intro:"O Gato Pigo está preso na jaula de pedra! Ponha as setas no chão, uma de cada vez, para o Byte seguir até ele.",
  livre:"Você me libertou! Obrigado, Byte!"},
 {friend:"coelho", nome:"a Coelha Nina",
  maze:["#########","#S..#..J#","#.#.#.#.#","#.#...#.#","#.#####.#","#.......#","#########"],
  intro:"A Coelha Nina está do outro lado! Cuidado: alguns caminhos não levam a lugar nenhum. Desvie das paredes!",
  livre:"Consegui sair! Que alegria!"},
 {friend:"passaro", nome:"o Passarinho Tuim",
  maze:["#########","#S......#","#######.#","#..J###.#","#.#####.#","#.......#","#########"],
  intro:"O Passarinho Tuim está no coração do labirinto! É uma volta comprida: vá repetindo as setas na mesma direção.",
  livre:"Livre pra voar! Muito obrigado!"}
];
// estado do labirinto atual
var wall={},start=[1,1],jaula={gx:5,gy:5};
function parseMaze(m){wall={};for(var y=0;y<m.length;y++){var row=m[y];for(var x=0;x<row.length;x++){var c=row[x];
  if(c==="#")wall[x+","+y]=1; else if(c==="S")start=[x,y]; else if(c==="J")jaula={gx:x,gy:y};}}}
function ehMuro(gx,gy){return gx<0||gy<0||gx>=GW||gy>=GH||wall[gx+","+gy]===1;}

var fase="hist",mi=0,hitos=0;
var byte={gx:1,gy:1,px:0,py:0,dir:1,resp:0,passo:0,mov:false,tremor:0};
var signs={},salvos=0;
var exec={ativo:false,de:null,para:null,nx:0,ny:0,t:0,steps:0};
var lib={ativo:false,t:0},balaoTxt=null,balaoT=0,balaoQuem="byte",som=false;
var estrelas=[],vagalumes=[],alivioAlvo=6,alivioPegos=0;
var DIRS=[undefined,"dir","baixo","esq","cima"],ROT={dir:0,baixo:Math.PI/2,esq:Math.PI,cima:-Math.PI/2};
var arvDeco=[[OX-40,OY+70],[OX+GW*CELL+40,OY+120],[OX-30,OY+GH*CELL-30],[OX+GW*CELL+34,OY+GH*CELL-24]];
var vagasDeco=[];for(var i=0;i<12;i++)vagasDeco.push({x:(i*151)%VW,y:(i*97)%VH,f:i});

/* ---------- AUDIO ---------- */
var AC=null,ventoG=null;
function initAudio(){if(AC)return;try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return;}
 var n=Math.floor(AC.sampleRate*2),buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);
 for(var i=0;i<n;i++)d[i]=(Math.random()*2-1);
 var s=AC.createBufferSource();s.buffer=buf;s.loop=true;var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=470;
 ventoG=AC.createGain();ventoG.gain.value=0;s.connect(f);f.connect(ventoG);ventoG.connect(AC.destination);s.start();}
function bip(fr,dur,tp,vol,del){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();o.type=tp||"sine";o.frequency.value=fr;
 var t=AC.currentTime+(del||0);g.gain.setValueAtTime(vol||.16,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+dur);}
function somPasso(){bip(170,.05,"square",.045);}
function somErro(){bip(200,.18,"sawtooth",.10,0);bip(150,.22,"sawtooth",.10,.09);}
function somChave(){bip(880,.09,"sine",.15,0);bip(1175,.09,"sine",.15,.1);bip(1568,.14,"sine",.15,.2);}
function somFaisca(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();var t=AC.currentTime;o.type="sine";o.frequency.setValueAtTime(600,t);o.frequency.exponentialRampToValueAtTime(2200,t+.25);g.gain.setValueAtTime(.11,t);g.gain.exponentialRampToValueAtTime(.001,t+.3);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.32);}
function somMiau(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain(),f=AC.createBiquadFilter();var t=AC.currentTime;o.type="sawtooth";f.type="bandpass";f.frequency.value=1100;o.frequency.setValueAtTime(520,t);o.frequency.linearRampToValueAtTime(920,t+.12);o.frequency.linearRampToValueAtTime(430,t+.34);g.gain.setValueAtTime(.001,t);g.gain.linearRampToValueAtTime(.13,t+.05);g.gain.exponentialRampToValueAtTime(.001,t+.36);o.connect(f);f.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.38);}
function somPio(){bip(1300,.08,"sine",.12,0);bip(1760,.09,"sine",.12,.09);bip(1500,.10,"sine",.12,.19);}
function somTwinkle(){bip(1400+Math.floor(hitos%3)*180,.12,"sine",.14,0);bip(2100,.10,"triangle",.10,.06);}
function somTrovao(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain(),f=AC.createBiquadFilter();var t=AC.currentTime;o.type="triangle";f.type="lowpass";f.frequency.value=180;o.frequency.setValueAtTime(90,t);o.frequency.exponentialRampToValueAtTime(40,t+.7);g.gain.setValueAtTime(.001,t);g.gain.linearRampToValueAtTime(.22,t+.05);g.gain.exponentialRampToValueAtTime(.001,t+.8);o.connect(f);f.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.82);}
function somVitoria(){bip(523,.13,"sine",.15,0);bip(659,.13,"sine",.15,.13);bip(784,.13,"sine",.15,.26);bip(1047,.24,"sine",.15,.39);}

/* ---------- VOZ ---------- */
function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falar(t,pitch){if(!som||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.97;u.pitch=pitch||1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,quem,pitch){balaoTxt=t;balaoT=5.2;balaoQuem=quem||"byte";falar(t,pitch);}
function unlock(){initAudio();if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
function toggleSom(){unlock();som=!som;var b=document.getElementById("bSom");if(ventoG)ventoG.gain.value=som?0.05:0;
 if(som){b.innerHTML="&#128266; Som ligado";repetirFala();}else{b.innerHTML="&#128263; Mudo";try{speechSynthesis.cancel();}catch(e){}}}
function repetirFala(){if(fase==="hist")balao(HIST[histIdx].t,HIST[histIdx].q,HIST[histIdx].p);
 else if(fase==="jogo")balao(MIS[mi].intro,"byte");
 else if(fase==="alivio")balao("Hora de brincar! Toque nos vaga-lumes para pegá-los.","byte");}

/* ---------- HISTORIA (intro Nimbo) ---------- */
var HIST=[
 {t:"Esta é a Floresta do Byte. O Byte é um robô curioso e bem legal.",q:"byte",p:1.12},
 {t:"Mas o Nimbo, uma nuvem cinzenta e resmungona, prendeu os amiguinhos em jaulas de pedra dentro do labirinto!",q:"nimbo",p:0.72},
 {t:"Só você pode ajudar! Ponha setas de madeira no chão para o Byte achar o caminho e libertar todos.",q:"byte",p:1.12},
 {t:"Toque na tela para começar a aventura!",q:"byte",p:1.12}
];
var histIdx=0;

function setMissao(i){mi=i;var m=MIS[i];parseMaze(m.maze);byte.gx=start[0];byte.gy=start[1];
 var p=cellPx(byte.gx,byte.gy);byte.px=p[0];byte.py=p[1];byte.dir=1;signs={};exec.ativo=false;lib.ativo=false;fase="jogo";
 document.getElementById("bVai").disabled=false;balao(m.intro,"byte");}

/* ---------- ENTRADA ---------- */
cv.addEventListener("mousedown",function(e){clic(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){clic(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});
function xyCanvas(cxp,cyp){var r=cv.getBoundingClientRect();return [(cxp-r.left)*(VW/r.width),(cyp-r.top)*(VH/r.height)];}
function clic(cxp,cyp){unlock();var c=xyCanvas(cxp,cyp),mx=c[0],my=c[1];
 if(fase==="hist"){avancaHist();return;}
 if(fase==="alivio"){pegaVagalume(mx,my);return;}
 if(fase!=="jogo"||exec.ativo||lib.ativo)return;
 var gx=Math.floor((mx-OX)/CELL),gy=Math.floor((my-OY)/CELL);
 if(gx<0||gy<0||gx>=GW||gy>=GH)return;if(ehMuro(gx,gy))return;if(gx===jaula.gx&&gy===jaula.gy)return;
 var key=gx+","+gy,cur=signs[key],idx=(DIRS.indexOf(cur)+1)%DIRS.length;
 if(DIRS[idx]===undefined)delete signs[key];else signs[key]=DIRS[idx];bip(520,.04,"triangle",.05);}
function avancaHist(){histIdx++;if(histIdx>=HIST.length){setMissao(0);return;}
 if(HIST[histIdx].q==="nimbo")somTrovao();balao(HIST[histIdx].t,HIST[histIdx].q,HIST[histIdx].p);}

function limpar(){if(exec.ativo||lib.ativo||fase!=="jogo")return;signs={};bip(300,.08,"triangle",.08);}
function vai(){unlock();if(fase!=="jogo"||exec.ativo||lib.ativo)return;exec.ativo=true;exec.steps=0;exec.de=null;
 document.getElementById("bVai").disabled=true;prox();}
function prox(){
 if(byte.gx===jaula.gx&&byte.gy===jaula.gy){libertar();return;}
 var d=signs[byte.gx+","+byte.gy];
 if(!d){errou("O Byte parou! Falta uma seta nesta pedra para ele saber pra onde ir.");return;}
 var nx=byte.gx+(d==="dir"?1:d==="esq"?-1:0),ny=byte.gy+(d==="baixo"?1:d==="cima"?-1:0);
 if(ehMuro(nx,ny)){byte.tremor=.5;somErro();errou("Opa! A seta apontou para o muro de pedra. Vamos virar ela?");return;}
 exec.steps++;if(exec.steps>60){errou("O Byte está rodando em círculos! Confira as setas.");return;}
 if(d==="esq")byte.dir=-1;else if(d==="dir")byte.dir=1;
 exec.de=cellPx(byte.gx,byte.gy);exec.para=cellPx(nx,ny);exec.nx=nx;exec.ny=ny;exec.t=0;somPasso();}
function errou(m){exec.ativo=false;document.getElementById("bVai").disabled=false;balao(m,"byte");}
function libertar(){exec.ativo=false;lib.ativo=true;lib.t=0;somChave();salvos++;
 var jp=cellPx(jaula.gx,jaula.gy);
 for(var i=0;i<20;i++)estrelas.push({x:jp[0]+(Math.random()*70-35),y:jp[1]-24,vx:Math.random()*80-40,vy:-(45+Math.random()*80),a:1,r:3+Math.random()*4});
 var m=MIS[mi];balao(m.livre,"friend");
 setTimeout(function(){if(m.friend==="gato")somMiau();else if(m.friend==="passaro")somPio();else somFaisca();somFaisca();},430);
 var ult=(mi>=MIS.length-1);
 document.getElementById("bVai").disabled=false;
 setTimeout(function(){lib.ativo=false;
   if(ult){irFinal();}
   else if(mi===0){irAlivio();}
   else{setMissao(mi+1);}
 },2600);
}

/* ---------- ALIVIO: vaga-lumes ---------- */
function irAlivio(){fase="alivio";alivioPegos=0;vagalumes=[];
 for(var i=0;i<9;i++)vagalumes.push({x:80+Math.random()*(VW-160),y:80+Math.random()*(VH-160),
   ph:Math.random()*6.28,sp:.4+Math.random()*.6,ang:Math.random()*6.28,pego:false,pop:0});
 balao("Que tal um descanso? Toque nos vaga-lumes para pegá-los!","byte");}
function pegaVagalume(mx,my){for(var i=0;i<vagalumes.length;i++){var v=vagalumes[i];if(v.pego)continue;
  var dx=mx-v.x,dy=my-v.y;if(dx*dx+dy*dy<26*26){v.pego=true;v.pop=1;alivioPegos++;hitos++;somTwinkle();
   for(var k=0;k<8;k++)estrelas.push({x:v.x,y:v.y,vx:Math.random()*90-45,vy:Math.random()*90-45,a:1,r:2+Math.random()*3});
   if(alivioPegos>=alivioAlvo){balao("Que lindo! Agora vamos salvar os outros amiguinhos!","byte");
     setTimeout(function(){setMissao(1);},1800);}
   return;}}}

/* ---------- FINAL ---------- */
var fumaca=[];
function irFinal(){fase="final";somVitoria();
 setTimeout(function(){balao("O Nimbo viu tanta amizade que ficou bonzinho! Agora é festa na floresta!","nimbo",0.95);},400);}

/* ---------- INICIO ---------- */
function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");patM=cx.createPattern(IMG.muro,"repeat");
 parseMaze(MIS[0].maze);var p=cellPx(byte.gx,byte.gy);byte.px=p[0];byte.py=p[1];
 balao(HIST[0].t,HIST[0].q,HIST[0].p);requestAnimationFrame(frame);}

/* ---------- DESENHO ---------- */
function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(12,8,20,.30)";cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function estrela(x,y,r,a){cx.save();cx.globalAlpha=Math.max(0,a);cx.fillStyle="#ffd24a";cx.shadowColor="#ffd24a";cx.shadowBlur=10;cx.beginPath();
 for(var i=0;i<5;i++){var an=-Math.PI/2+i*2*Math.PI/5;cx.lineTo(x+Math.cos(an)*r,y+Math.sin(an)*r);var a2=an+Math.PI/5;cx.lineTo(x+Math.cos(a2)*r*.45,y+Math.sin(a2)*r*.45);}
 cx.closePath();cx.fill();cx.restore();cx.shadowBlur=0;}
function img(im,x,yBase,h){var w=im.width*h/im.height;cx.drawImage(im,x-w/2,yBase-h,w,h);}
// desenha sprite vivo: respira; "fala" (squash) se for o falante atual
function vivo(im,x,yBase,h,quem,t){var w=im.width*h/im.height;
 var talk=(balaoT>0&&balaoQuem===quem)?Math.abs(Math.sin(t*.02))*.05:0;
 var breath=Math.sin(t*.004+x)*.02;
 var sy=1+breath-talk, sx=1-breath*.5+talk*.5;
 cx.save();cx.translate(x,yBase);cx.scale(sx,sy);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
function desArvore(x,y,t){sombra(x,y+2,26,8);var sw=Math.sin(t*.0015+x)*0.02;cx.save();cx.translate(x,y);cx.rotate(sw);img(IMG.arvore,0,0,118);cx.restore();}
function desByte(t){var x=byte.px,y=byte.py,h=CELL*0.86,bob=byte.mov?Math.abs(Math.sin(byte.passo*.9))*6:0;
 var trem=byte.tremor>0?Math.sin(t*.06)*byte.tremor*4:0;var rp=byte.mov?0:Math.sin(byte.resp*1.0)*.03;
 sombra(x+trem,y+20,20,7);cx.save();cx.translate(x+trem,y+20-bob);cx.scale(byte.dir*(1+rp),1-rp*.6);img(IMG.byte,0,0,h);cx.restore();
 var kw=IMG.chave.width*20/IMG.chave.height;cx.drawImage(IMG.chave,x+13,y-44,kw,20);}
function desSeta(gx,gy,d){var p=cellPx(gx,gy),h=30,w=IMG.seta.width*h/IMG.seta.height;
 cx.save();cx.translate(p[0],p[1]+6);cx.rotate(ROT[d]);cx.globalAlpha=.96;cx.drawImage(IMG.seta,-w/2,-h/2,w,h);cx.restore();}
function desMuro(gx,gy){var x=OX+gx*CELL,y=OY+gy*CELL;
 // sombra na grama
 cx.fillStyle="rgba(8,6,14,.22)";cx.fillRect(x+3,y+CELL-LIFT+3,CELL,LIFT+2);
 // face frontal (mais escura)
 cx.fillStyle=patM;cx.fillRect(x,y,CELL,CELL);cx.fillStyle="rgba(20,14,26,.34)";cx.fillRect(x,y+CELL-LIFT,CELL,LIFT);
 // topo levantado
 cx.fillStyle=patM;cx.fillRect(x,y-LIFT,CELL,CELL);
 // luz no topo + contorno
 cx.fillStyle="rgba(255,244,225,.10)";cx.fillRect(x,y-LIFT,CELL,3);
 cx.strokeStyle="rgba(10,7,16,.45)";cx.lineWidth=1.5;cx.strokeRect(x+.5,y-LIFT+.5,CELL-1,CELL-1);}
function balaoDes(bx,by,cor){if(!(balaoT>0&&balaoTxt))return;cx.font="bold 13px Verdana";
 var words=balaoTxt.split(" "),linhas=[],cur="";
 for(var i=0;i<words.length;i++){var tt=cur?cur+" "+words[i]:words[i];if(cx.measureText(tt).width>360&&cur){linhas.push(cur);cur=words[i];}else cur=tt;}
 if(cur)linhas.push(cur);
 var bw=0;for(i=0;i<linhas.length;i++)bw=Math.max(bw,cx.measureText(linhas[i]).width);bw=Math.min(bw+26,VW-20);
 var lh=17,bh=linhas.length*lh+12;var lx=Math.max(8,Math.min(VW-bw-8,bx-bw/2)),ly=Math.max(30,by-bh);
 cx.globalAlpha=Math.min(1,balaoT/.6);
 cx.fillStyle=cor||"rgba(255,255,255,.97)";roundR(lx,ly,bw,bh,10);cx.fill();
 cx.beginPath();cx.moveTo(bx-7,ly+bh);cx.lineTo(bx+7,ly+bh);cx.lineTo(bx,ly+bh+9);cx.closePath();cx.fill();
 cx.fillStyle="#17324a";cx.textAlign="center";
 for(i=0;i<linhas.length;i++)cx.fillText(linhas[i],lx+bw/2,ly+16+i*lh);
 cx.globalAlpha=1;}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}

/* ---------- LOOP ---------- */
var ult=null;
function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 byte.resp+=dt*3;if(balaoT>0)balaoT-=dt;if(byte.tremor>0)byte.tremor=Math.max(0,byte.tremor-dt);
 if(exec.ativo&&exec.de){exec.t+=dt/0.42;byte.mov=true;byte.passo+=dt*12;
  if(exec.t>=1){byte.px=exec.para[0];byte.py=exec.para[1];byte.gx=exec.nx;byte.gy=exec.ny;byte.mov=false;exec.de=null;prox();}
  else{var e=exec.t<.5?2*exec.t*exec.t:1-Math.pow(-2*exec.t+2,2)/2;byte.px=exec.de[0]+(exec.para[0]-exec.de[0])*e;byte.py=exec.de[1]+(exec.para[1]-exec.de[1])*e;}}
 else byte.mov=false;
 if(lib.ativo)lib.t+=dt;
 for(var i=estrelas.length-1;i>=0;i--){var s=estrelas[i];s.x+=s.vx*dt;s.y+=s.vy*dt;s.vy+=120*dt;s.a-=dt*.55;if(s.a<=0)estrelas.splice(i,1);}

 cx.fillStyle=patG;cx.fillRect(0,0,VW,VH);
 if(fase==="final"){desenhaFinal(t);return;}
 if(fase==="hist"){desenhaHist(t);return;}
 if(fase==="alivio"){desenhaAlivio(t);return;}

 // arvores de fora
 for(i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 // brilho da jaula (por baixo)
 var jp=cellPx(jaula.gx,jaula.gy);
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(jp[0],jp[1],4,jp[0],jp[1],46);
 g.addColorStop(0,"rgba(120,255,170,"+(0.26+0.14*Math.sin(t*0.005))+")");g.addColorStop(1,"rgba(120,255,170,0)");
 cx.fillStyle=g;cx.fillRect(jp[0]-50,jp[1]-50,100,100);cx.restore();
 // MUROS (linha por linha, de cima p/ baixo: relevo correto entre eles)
 for(var gy=0;gy<GH;gy++)for(var gx=0;gx<GW;gx++)if(wall[gx+","+gy])desMuro(gx,gy);
 // jaula + amiguinho (sempre desenhados ANTES do Byte)
 sombra(jp[0],jp[1]+12,26,8);
 var fim=IMG[MIS[mi].friend];
 if(!lib.ativo){ img(IMG.jaula,jp[0],jp[1]+16,60);
   var fw=fim.width*26/fim.height;cx.drawImage(fim,jp[0]-fw/2,jp[1]-8,fw,26); }
 else { var hop=Math.abs(Math.sin(lib.t*6))*10; var fw2=fim.width*40/fim.height;
   cx.drawImage(fim,jp[0]-fw2/2+14,jp[1]+14-40-hop,fw2,40); img(IMG.jaula,jp[0],jp[1]+16,60); }
 // setas colocadas
 for(var key in signs){var pp=key.split(",");desSeta(+pp[0],+pp[1],signs[key]);}
 // BYTE — sempre por cima dos muros (regra: muro nunca esconde o Byte)
 desByte(t);
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 clima(t);
 // HUD
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";
 cx.fillText("Missão "+(mi+1)+" de "+MIS.length+"  —  liberte "+MIS[mi].nome+"  ·  amiguinhos salvos: "+salvos,VW/2,17);
 var bx=byte.px,by=byte.py-CELL*0.86-6;balaoDes(bx,by);
 requestAnimationFrame(frame);
}
function clima(t){
 var lg=cx.createLinearGradient(0,0,0,VH);lg.addColorStop(0,"rgba(60,40,95,.10)");lg.addColorStop(1,"rgba(255,170,80,.08)");cx.fillStyle=lg;cx.fillRect(0,0,VW,VH);
 var vg=cx.createRadialGradient(VW/2,VH/2,VH*.44,VW/2,VH/2,VH*.92);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,.42)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<vagasDeco.length;j++){var va=vagasDeco[j];
  var vx=va.x+Math.sin(t*.001+va.f)*15,vy=va.y+Math.cos(t*.0011+va.f)*12;var aa=.18+.28*Math.sin(t*.003+va.f*2);
  cx.shadowColor="#fff2a0";cx.shadowBlur=8;cx.fillStyle="rgba(255,240,150,"+Math.max(0,aa)+")";cx.beginPath();cx.arc(vx,vy,2,0,Math.PI*2);cx.fill();}cx.restore();cx.shadowBlur=0;}

function desenhaHist(t){for(var i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 var h=HIST[histIdx];
 if(h.q==="nimbo"){ // Nimbo grande no centro, trovejando
   var nx=VW/2,ny=200,fl=Math.sin(t*.03)*6;sombra(nx,ny+70,90,16);
   cx.save();cx.globalAlpha=.9;var gg=cx.createRadialGradient(nx,ny,10,nx,ny,150);gg.addColorStop(0,"rgba(90,90,120,.35)");gg.addColorStop(1,"rgba(90,90,120,0)");cx.fillStyle=gg;cx.fillRect(nx-160,ny-160,320,320);cx.restore();
   vivo(IMG.nimbo,nx,ny+70+fl*0,150,"nimbo",t);
   // Byte pequeno embaixo, tremendo
   var bx=nx,by=ny+150;sombra(bx,by+18,20,6);cx.save();cx.translate(bx+Math.sin(t*.05)*2,by);img(IMG.byte,0,0,60);cx.restore();
 } else { // Byte protagonista
   var bx=VW/2,by=250,bob=Math.sin(t*.005)*4;sombra(bx,by+20,26,8);
   cx.save();cx.translate(bx,by-bob);img(IMG.byte,0,0,150);cx.restore();
 }
 clima(t);
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";
 cx.fillText("✨ A aventura vai começar — toque para continuar ✨",VW/2,17);
 balaoDes(VW/2, VH-42, h.q==="nimbo"?"rgba(220,224,240,.97)":"rgba(255,255,255,.97)");
 requestAnimationFrame(frame);
}
function desenhaAlivio(t){
 for(var i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 // gato salvo passeia embaixo
 var gx=VW/2+Math.sin(t*.0006)*120,gy=VH-60,hop=Math.abs(Math.sin(t*.006))*6;
 sombra(gx,gy+2,18,6);var gw=IMG.gato.width*44/IMG.gato.height;cx.drawImage(IMG.gato,gx-gw/2,gy-44-hop,gw,44);
 // vaga-lumes
 for(i=0;i<vagalumes.length;i++){var v=vagalumes[i];if(v.pego){if(v.pop>0)v.pop-=.05;continue;}
   v.ang+=(Math.sin(t*.001+v.ph)*.02);v.x+=Math.cos(v.ang)*v.sp;v.y+=Math.sin(v.ang*1.3+v.ph)*v.sp*.7;
   if(v.x<40)v.x=40;if(v.x>VW-40)v.x=VW-40;if(v.y<50)v.y=50;if(v.y>VH-90)v.y=VH-90;
   var pu=.6+.4*Math.sin(t*.006+v.ph);
   cx.save();cx.globalCompositeOperation="lighter";cx.shadowColor="#fff59a";cx.shadowBlur=18;
   cx.fillStyle="rgba(255,246,150,"+pu+")";cx.beginPath();cx.arc(v.x,v.y,7,0,Math.PI*2);cx.fill();
   cx.fillStyle="rgba(255,255,220,"+pu+")";cx.beginPath();cx.arc(v.x,v.y,3,0,Math.PI*2);cx.fill();cx.restore();cx.shadowBlur=0;}
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 clima(t);
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";
 cx.fillText("⭐ Descanso: toque nos vaga-lumes  ("+alivioPegos+"/"+alivioAlvo+")",VW/2,17);
 balaoDes(VW/2,VH-90);
 requestAnimationFrame(frame);
}
function desenhaFinal(t){
 for(var i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 var cxp=VW/2,cy=260;
 if((t|0)%6===0&&fumaca.length<40)fumaca.push({x:cxp-56,y:cy-146,a:.5,r:6,vy:-14,vx:6});
 for(i=fumaca.length-1;i>=0;i--){var f=fumaca[i];f.y+=f.vy*.016;f.x+=f.vx*.016;f.r+=.12;f.a-=.004;if(f.a<=0){fumaca.splice(i,1);continue;}
   cx.fillStyle="rgba(220,220,225,"+Math.max(0,f.a)+")";cx.beginPath();cx.arc(f.x,f.y,f.r,0,Math.PI*2);cx.fill();}
 sombra(cxp,cy+8,84,16);img(IMG.cabana,cxp,cy,196);
 // Nimbo bonzinho flutuando, sorrindo (pequeno, no alto)
 var nx=cxp+150,ny=110+Math.sin(t*.003)*10;vivo(IMG.nimbo,nx,ny,72,"nimbo",t);
 // Byte + amiguinhos salvos
 var bw=IMG.byte.width*70/IMG.byte.height;sombra(cxp-96,cy+58,20,7);cx.drawImage(IMG.byte,cxp-96-bw/2,cy+58-70,bw,70);
 var fr=[IMG.gato,IMG.coelho,IMG.passaro];
 for(i=0;i<3;i++){var im=fr[i],fx=cxp-20+i*56,fh=50,fw=im.width*fh/im.height,hop=Math.abs(Math.sin(t*.005+i))*7;
   sombra(fx,cy+58,15,5);cx.drawImage(im,fx-fw/2,cy+58-fh-hop,fw,fh);}
 if((t|0)%10===0&&estrelas.length<44)estrelas.push({x:Math.random()*VW,y:-10,vx:Math.random()*20-10,vy:30+Math.random()*30,a:1,r:4+Math.random()*4});
 for(i=0;i<estrelas.length;i++){var s=estrelas[i];s.x+=s.vx*.016;s.y+=s.vy*.016;s.a-=.003;estrela(s.x,s.y,s.r,s.a);}
 estrelas=estrelas.filter(function(s){return s.a>0&&s.y<VH+20;});
 clima(t);
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 14px Verdana";cx.textAlign="center";
 cx.fillText("🎉 Todos os amiguinhos estão livres! Que festa na floresta! 🎉",VW/2,17);
 balaoDes(cxp-96,cy-30);
 requestAnimationFrame(frame);
}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
/* QA hook: resolve o labirinto atual e devolve as setas do caminho (para teste dirigido) */
function _bfsSolve(){var s=start.slice(),j=[jaula.gx,jaula.gy];var prev={},q=[s],seen={};seen[s[0]+","+s[1]]=1;
 var D=[[1,0,"dir"],[-1,0,"esq"],[0,1,"baixo"],[0,-1,"cima"]];
 while(q.length){var c=q.shift();if(c[0]===j[0]&&c[1]===j[1])break;
  for(var i=0;i<4;i++){var nx=c[0]+D[i][0],ny=c[1]+D[i][1],kk=nx+","+ny;if(ehMuro(nx,ny)||seen[kk])continue;seen[kk]=1;prev[kk]={p:c,d:D[i][2]};q.push([nx,ny]);}}
 var path=[],c=j;while(!(c[0]===s[0]&&c[1]===s[1])){var e=prev[c[0]+","+c[1]];if(!e)return null;path.unshift({gx:e.p[0],gy:e.p[1],d:e.d});c=e.p;}
 return path;}
window._qaSolve=function(){var p=_bfsSolve();if(!p)return false;signs={};for(var i=0;i<p.length;i++)signs[p[i].gx+","+p[i].gy]=p[i].d;return true;};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
out=os.path.join(S,"byte-floresta2.html")
open(out,"w",encoding="utf-8").write(HTML)
print("OK ->",out,"(",round(len(HTML)/1024),"KB )")
