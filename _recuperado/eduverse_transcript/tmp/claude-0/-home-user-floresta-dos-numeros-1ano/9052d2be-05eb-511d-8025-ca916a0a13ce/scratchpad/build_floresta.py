# -*- coding: utf-8 -*-
import base64, os
S=os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
NM={"grama":"grama.png","arvore":"arvore.png","byte":"byte.png","gato":"gato.png","jaula":"jaula.png","chave":"chave.png","cabana":"cabana.png","seta":"seta.png"}
A={("__%s__"%k.upper()):b64(v) for k,v in NM.items()}

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EducaVerso - A Floresta do Byte</title>
<style>
 html,body{margin:0;height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow:hidden;}
 #wrap{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;}
 h1{font-size:15px;margin:4px 0 0;} .sub{font-size:11px;color:#9fb6df;margin:0 0 4px;}
 #frame{padding:7px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;}
 canvas{display:block;border-radius:10px;background:#4a8a3a;max-width:96vw;height:auto;cursor:pointer;}
 #painel{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:6px;}
 .bt{font-family:inherit;font-weight:bold;border:0;border-radius:14px;cursor:pointer;padding:9px 16px;font-size:15px;color:#0a1120;}
 .bt.vai{background:linear-gradient(#bff7d6,#4fcf8e);box-shadow:0 3px 0 #2f9463;} .bt.vai:active{transform:translateY(2px);box-shadow:0 1px 0 #2f9463;}
 .bt.lp{background:linear-gradient(#ffd0d0,#f08a8a);box-shadow:0 3px 0 #b04d4d;}
 .bt.vz{background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;}
 .bt:disabled{opacity:.5;filter:grayscale(.5);}
</style></head><body><div id="wrap">
 <h1>&#127795; A Floresta do Byte</h1>
 <p class="sub">clique no ch&#227;o p/ p&#245;r as setas &#183; aperte VAI &#183; guie o Byte at&#233; a jaula e liberte o amiguinho!</p>
 <div id="frame"><canvas id="tela" width="720" height="470"></canvas></div>
 <div id="painel">
   <button class="bt vai" id="bVai" onclick="vai()">&#9654; VAI!</button>
   <button class="bt lp" onclick="limpar()">&#128465; Limpar</button>
   <button class="bt vz" id="bSom" onclick="toggleSom()">&#128266; Som e Voz</button>
 </div>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC={grama:"__GRAMA__",arvore:"__ARVORE__",byte:"__BYTE__",gato:"__GATO__",jaula:"__JAULA__",chave:"__CHAVE__",cabana:"__CABANA__",seta:"__SETA__"};
var IMG={},patG,carreg=0,NN=8;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===NN)iniciar();};im.src=SRC[key];})(k);}

var GW=6,GH=4,CELL=98,OX=(VW-GW*CELL)/2,OY=42;
function cellPx(gx,gy){return [OX+gx*CELL+CELL/2, OY+gy*CELL+CELL/2];}
var MIS=[
 {start:[0,3],jaula:[5,0],obst:[[2,2],[3,1]],fala:"Um amiguinho está preso na jaula! Coloque as setas para o Byte chegar lá e soltar ele."},
 {start:[0,0],jaula:[5,3],obst:[[2,1],[3,3],[4,1]],fala:"Mais um amiguinho preso! Guie o Byte desviando das árvores."}
];
var fase="jogo",mi=0,byte={gx:0,gy:3,px:0,py:0,dir:1,resp:0,passo:0,mov:false},jaula={gx:5,gy:0},obst=[],signs={},salvos=0;
var exec={ativo:false,de:null,para:null,nx:0,ny:0,t:0,steps:0};
var lib={ativo:false,t:0},balaoTxt=null,balaoT=0,som=false,estrelas=[],fumaca=[];
var vagas=[];for(var i=0;i<14;i++)vagas.push({x:(i*151)%VW,y:(i*89)%VH,f:i});
var arvDeco=[[OX-34,OY+28],[OX+GW*CELL+34,OY+66],[OX-26,OY+GH*CELL],[OX+GW*CELL+28,OY+GH*CELL-28]];
var DIRS=[undefined,"dir","baixo","esq","cima"],ROT={dir:0,baixo:Math.PI/2,esq:Math.PI,cima:-Math.PI/2};

/* ---- AUDIO ---- */
var AC=null,ventoG=null;
function initAudio(){if(AC)return;try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return;}
 var n=Math.floor(AC.sampleRate*2),buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);
 for(var i=0;i<n;i++)d[i]=(Math.random()*2-1);
 var s=AC.createBufferSource();s.buffer=buf;s.loop=true;var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=480;
 ventoG=AC.createGain();ventoG.gain.value=0;s.connect(f);f.connect(ventoG);ventoG.connect(AC.destination);s.start();}
function bip(fr,dur,tp,vol,del){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();o.type=tp||"sine";o.frequency.value=fr;
 var t=AC.currentTime+(del||0);g.gain.setValueAtTime(vol||.18,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+dur);}
function somPasso(){bip(180,.05,"square",.05);}
function somChave(){bip(880,.09,"sine",.16,0);bip(1175,.09,"sine",.16,.1);bip(1568,.14,"sine",.16,.2);}
function somFaisca(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();var t=AC.currentTime;o.type="sine";o.frequency.setValueAtTime(600,t);o.frequency.exponentialRampToValueAtTime(2200,t+.25);g.gain.setValueAtTime(.12,t);g.gain.exponentialRampToValueAtTime(.001,t+.3);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.32);}
function somMiau(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain(),f=AC.createBiquadFilter();var t=AC.currentTime;o.type="sawtooth";f.type="bandpass";f.frequency.value=1100;o.frequency.setValueAtTime(520,t);o.frequency.linearRampToValueAtTime(920,t+.12);o.frequency.linearRampToValueAtTime(430,t+.34);g.gain.setValueAtTime(.001,t);g.gain.linearRampToValueAtTime(.14,t+.05);g.gain.exponentialRampToValueAtTime(.001,t+.36);o.connect(f);f.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.38);}
function somVitoria(){bip(523,.13,"sine",.16,0);bip(659,.13,"sine",.16,.13);bip(784,.13,"sine",.16,.26);bip(1047,.22,"sine",.16,.39);}

/* ---- VOZ ---- */
function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falar(t){if(!som||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.98;u.pitch=1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,n){balaoTxt=t;balaoT=5;if(n!==false)falar(t);}
function unlock(){initAudio();if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
function toggleSom(){unlock();som=!som;var b=document.getElementById("bSom");if(ventoG)ventoG.gain.value=som?0.05:0;
 if(som){b.textContent="🔊 Som ligado";if(fase==="jogo")balao(MIS[mi].fala);}else{b.textContent="🔇 Mudo";try{speechSynthesis.cancel();}catch(e){}}}

function setMissao(i){mi=i;var m=MIS[i];byte.gx=m.start[0];byte.gy=m.start[1];var p=cellPx(byte.gx,byte.gy);byte.px=p[0];byte.py=p[1];
 jaula.gx=m.jaula[0];jaula.gy=m.jaula[1];obst=m.obst;signs={};exec.ativo=false;lib.ativo=false;balao(m.fala);}
function ehObst(gx,gy){for(var i=0;i<obst.length;i++)if(obst[i][0]===gx&&obst[i][1]===gy)return true;return false;}
cv.addEventListener("mousedown",function(e){clic(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){clic(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});
function clic(cxp,cyp){unlock();if(fase!=="jogo"||exec.ativo||lib.ativo)return;var r=cv.getBoundingClientRect();var mx=(cxp-r.left)*(VW/r.width),my=(cyp-r.top)*(VH/r.height);
 var gx=Math.floor((mx-OX)/CELL),gy=Math.floor((my-OY)/CELL);if(gx<0||gy<0||gx>=GW||gy>=GH)return;if(ehObst(gx,gy))return;if(gx===jaula.gx&&gy===jaula.gy)return;
 var key=gx+","+gy,cur=signs[key],idx=(DIRS.indexOf(cur)+1)%DIRS.length;if(DIRS[idx]===undefined)delete signs[key];else signs[key]=DIRS[idx];}
function limpar(){if(exec.ativo||lib.ativo)return;signs={};}
function vai(){unlock();if(fase!=="jogo"||exec.ativo||lib.ativo)return;exec.ativo=true;exec.steps=0;exec.de=null;document.getElementById("bVai").disabled=true;prox();}
function prox(){
 if(byte.gx===jaula.gx&&byte.gy===jaula.gy){libertar();return;}
 var d=signs[byte.gx+","+byte.gy];
 if(!d){errou("O Byte não sabe pra onde ir aqui! Ponha uma seta nesta pedra.");return;}
 var nx=byte.gx+(d==="dir"?1:d==="esq"?-1:0),ny=byte.gy+(d==="baixo"?1:d==="cima"?-1:0);
 if(nx<0||ny<0||nx>=GW||ny>=GH||ehObst(nx,ny)){errou("Ops! A seta apontou pra árvore. Vamos arrumar?");return;}
 exec.steps++;if(exec.steps>30){errou("O Byte está rodando em círculos! Confira as setas.");return;}
 if(d==="esq")byte.dir=-1;else if(d==="dir")byte.dir=1;
 exec.de=cellPx(byte.gx,byte.gy);exec.para=cellPx(nx,ny);exec.nx=nx;exec.ny=ny;exec.t=0;somPasso();}
function libertar(){exec.ativo=false;lib.ativo=true;lib.t=0;somChave();salvos++;
 for(var i=0;i<18;i++)estrelas.push({x:byte.px+(Math.random()*80-40),y:byte.py-30,vx:Math.random()*70-35,vy:-(40+Math.random()*70),a:1,r:3+Math.random()*4});
 balao("Você me salvou! Muito obrigado, Byte!");setTimeout(function(){somMiau();somFaisca();},450);
 var ult=(mi>=MIS.length-1);
 setTimeout(function(){lib.ativo=false;if(ult){fase="final";somVitoria();balao("VIVA! Todos os amiguinhos estão salvos! Vamos festejar na cabana!");}else setMissao(mi+1);},ult?2600:2600);
 document.getElementById("bVai").disabled=false;}
function errou(m){exec.ativo=false;balao(m);document.getElementById("bVai").disabled=false;}

function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");setMissao(0);ult=null;requestAnimationFrame(frame);}

function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(15,10,25,.28)";cx.shadowColor="rgba(0,0,0,.3)";cx.shadowBlur=8;cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function estrela(x,y,r,a){cx.save();cx.globalAlpha=a;cx.fillStyle="#ffd24a";cx.shadowColor="#ffd24a";cx.shadowBlur=10;cx.beginPath();for(var i=0;i<5;i++){var an=-Math.PI/2+i*2*Math.PI/5;cx.lineTo(x+Math.cos(an)*r,y+Math.sin(an)*r);var a2=an+Math.PI/5;cx.lineTo(x+Math.cos(a2)*r*.45,y+Math.sin(a2)*r*.45);}cx.closePath();cx.fill();cx.restore();cx.shadowBlur=0;}
function img(im,x,yBase,h){var w=im.width*h/im.height;cx.drawImage(im,x-w/2,yBase-h,w,h);}
function desArvore(x,y,t){sombra(x,y+4,26,8);var sw=Math.sin(t*.0015+x)*0.02;cx.save();cx.translate(x,y);cx.rotate(sw);img(IMG.arvore,0,0,116);cx.restore();}
function desByte(x,y,mov,passo,resp){var h=76,bob=mov?Math.abs(Math.sin(passo*.9))*6:0,rp=mov?0:Math.sin(resp)*.03;
 sombra(x,y+22,22,7);cx.save();cx.translate(x,y+22-bob);cx.scale(byte.dir*(1+rp),1-rp*.6);img(IMG.byte,0,0,h);cx.restore();
 // chave que o byte carrega
 var kw=IMG.chave.width*22/IMG.chave.height;cx.drawImage(IMG.chave,x+16,y-52,kw,22);}
function desSeta(x,y,d){var h=30,w=IMG.seta.width*h/IMG.seta.height;cx.save();cx.translate(x,y+4);cx.rotate(ROT[d]);cx.drawImage(IMG.seta,-w/2,-h/2,w,h);cx.restore();}

var ult=null;
function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 byte.resp+=dt*3;if(balaoT>0)balaoT-=dt;
 if(exec.ativo&&exec.de){exec.t+=dt/0.4;byte.mov=true;byte.passo+=dt*12;
  if(exec.t>=1){byte.px=exec.para[0];byte.py=exec.para[1];byte.gx=exec.nx;byte.gy=exec.ny;byte.mov=false;exec.de=null;prox();}
  else{var e=exec.t<.5?2*exec.t*exec.t:1-Math.pow(-2*exec.t+2,2)/2;byte.px=exec.de[0]+(exec.para[0]-exec.de[0])*e;byte.py=exec.de[1]+(exec.para[1]-exec.de[1])*e;}}
 else byte.mov=false;
 if(lib.ativo)lib.t+=dt;
 for(var i=estrelas.length-1;i>=0;i--){var s=estrelas[i];s.x+=s.vx*dt;s.y+=s.vy*dt;s.vy+=120*dt;s.a-=dt*.55;if(s.a<=0)estrelas.splice(i,1);}

 cx.fillStyle=patG;cx.fillRect(0,0,VW,VH);
 if(fase==="final"){desenhaFinal(t);pintarTela(t);return;}

 for(i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 // casas do caminho
 for(var gy=0;gy<GH;gy++)for(var gx=0;gx<GW;gx++){if(ehObst(gx,gy))continue;if(gx===jaula.gx&&gy===jaula.gy)continue;var p=cellPx(gx,gy);
   cx.fillStyle="rgba(255,255,255,.12)";cx.strokeStyle="rgba(255,255,255,.2)";cx.lineWidth=2;cx.beginPath();cx.ellipse(p[0],p[1]+16,38,20,0,0,Math.PI*2);cx.fill();cx.stroke();}
 // obstaculos = arvores
 for(i=0;i<obst.length;i++){var op=cellPx(obst[i][0],obst[i][1]);desArvore(op[0],op[1]+6,t);}
 // jaula + amiguinho
 var jp=cellPx(jaula.gx,jaula.gy);
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(jp[0],jp[1],4,jp[0],jp[1],52);g.addColorStop(0,"rgba(120,255,170,"+(0.3+0.15*Math.sin(t*0.005))+")");g.addColorStop(1,"rgba(120,255,170,0)");cx.fillStyle=g;cx.fillRect(jp[0]-56,jp[1]-56,112,112);cx.restore();
 sombra(jp[0],jp[1]+14,28,9);
 if(!lib.ativo){ img(IMG.jaula,jp[0],jp[1]+18,64); var gw=IMG.gato.width*30/IMG.gato.height;cx.drawImage(IMG.gato,jp[0]-gw/2,jp[1]-14,gw,30); }
 else { var hop=Math.abs(Math.sin(lib.t*6))*10; var gw2=IMG.gato.width*46/IMG.gato.height;cx.drawImage(IMG.gato,jp[0]-gw2/2+16,jp[1]+16-46-hop,gw2,46); img(IMG.jaula,jp[0],jp[1]+18,64); }
 // setas colocadas
 for(var key in signs){var pp=key.split(","),px=cellPx(+pp[0],+pp[1]);desSeta(px[0],px[1],signs[key]);}
 // byte
 desByte(byte.px,byte.py,byte.mov,byte.passo,byte.resp);
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 pintarTela(t);
 // topo
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";cx.fillText("Missão "+(mi+1)+" de "+MIS.length+"  —  guie o Byte até a jaula 🐾 (clique no chão p/ pôr setas)",VW/2,17);
 balaoDes(byte.px,byte.py-58);
 requestAnimationFrame(frame);
}
function desenhaFinal(t){
 for(var i=0;i<arvDeco.length;i++)desArvore(arvDeco[i][0],arvDeco[i][1],t);
 var cxp=VW/2,cy=250;
 // fumaca da chamine
 if((t|0)%6===0&&fumaca.length<40)fumaca.push({x:cxp-58,y:cy-150,a:.5,r:6,vy:-14,vx:6});
 for(i=fumaca.length-1;i>=0;i--){var f=fumaca[i];f.y+=f.vy*.016;f.x+=f.vx*.016;f.r+=.12;f.a-=.004;if(f.a<=0)fumaca.splice(i,1);cx.fillStyle="rgba(220,220,225,"+Math.max(0,f.a)+")";cx.beginPath();cx.arc(f.x,f.y,f.r,0,Math.PI*2);cx.fill();}
 sombra(cxp,cy+8,80,16);img(IMG.cabana,cxp,cy,200);
 // byte + gatos salvos
 var bw=IMG.byte.width*70/IMG.byte.height;sombra(cxp-70,cy+64,20,7);cx.drawImage(IMG.byte,cxp-70-bw/2,cy+64-70,bw,70);
 for(i=0;i<salvos;i++){var gx=cxp+10+i*54,gw=IMG.gato.width*54/IMG.gato.height,hop=Math.abs(Math.sin(t*.005+i))*6;sombra(gx,cy+64,16,6);cx.drawImage(IMG.gato,gx-gw/2,cy+64-54-hop,gw,54);}
 if((t|0)%10===0&&estrelas.length<40)estrelas.push({x:Math.random()*VW,y:-10,vx:Math.random()*20-10,vy:30+Math.random()*30,a:1,r:4+Math.random()*4});
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 14px Verdana";cx.textAlign="center";cx.fillText("🎉 Todos os amiguinhos estão salvos! Que festa na floresta! 🎉",VW/2,17);
 balaoDes(cxp-70,cy-20);
 requestAnimationFrame(frame);
}
function pintarTela(t){
 var lg=cx.createLinearGradient(0,0,0,VH);lg.addColorStop(0,"rgba(60,40,95,.10)");lg.addColorStop(1,"rgba(255,170,80,.10)");cx.fillStyle=lg;cx.fillRect(0,0,VW,VH);
 var vg=cx.createRadialGradient(VW/2,VH/2,VH*.42,VW/2,VH/2,VH*.9);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,.4)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<vagas.length;j++){var va=vagas[j];var vx=va.x+Math.sin(t*.001+va.f)*15,vy=va.y+Math.cos(t*.0011+va.f)*12;var aa=.25+.35*Math.sin(t*.003+va.f*2);cx.shadowColor="#fff2a0";cx.shadowBlur=8;cx.fillStyle="rgba(255,240,150,"+aa+")";cx.beginPath();cx.arc(vx,vy,2,0,Math.PI*2);cx.fill();}cx.restore();}
function balaoDes(bx,by){if(balaoT>0&&balaoTxt){cx.font="bold 13px Verdana";var tw=cx.measureText(balaoTxt).width,bw=Math.min(tw+24,VW-20),bh=30;var lx=Math.max(8,Math.min(VW-bw-8,bx-bw/2)),ly=Math.max(28,by-bh);
 cx.globalAlpha=Math.min(1,balaoT/.6);cx.fillStyle="rgba(255,255,255,.96)";roundR(lx,ly,bw,bh,9);cx.fill();cx.beginPath();cx.moveTo(bx-7,ly+bh);cx.lineTo(bx+7,ly+bh);cx.lineTo(bx,ly+bh+9);cx.closePath();cx.fill();cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(balaoTxt,lx+bw/2,ly+bh/2+5);cx.globalAlpha=1;}}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
open(os.path.join(S,"byte-floresta.html"),"w",encoding="utf-8").write(HTML)
print("OK -> byte-floresta.html (",round(len(HTML)/1024),"KB )")
