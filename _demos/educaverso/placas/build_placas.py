# -*- coding: utf-8 -*-
import base64, os
S=os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
A={"__GRAMA__":b64("grama.png"),"__ARVORE__":b64("arvore.png"),"__BYTE__":b64("byte.png"),"__GATO__":b64("gato.png")}

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EducaVerso - Ajude o Gatinho a Voltar pra Casa</title>
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
 <h1>&#128049; Ajude o gatinho a voltar pra casa!</h1>
 <p class="sub">clique nas pedras para colocar plaquinhas de seta &#183; aperte VAI &#183; o gatinho segue as placas at&#233; em casa</p>
 <div id="frame"><canvas id="tela" width="720" height="470"></canvas></div>
 <div id="painel">
   <button class="bt vai" id="bVai" onclick="vai()">&#9654; VAI!</button>
   <button class="bt lp" onclick="limpar()">&#128465; Limpar placas</button>
   <button class="bt vz" id="bVoz" onclick="toggleVoz()">&#128266; Ouvir</button>
 </div>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC={grama:"__GRAMA__",arvore:"__ARVORE__",byte:"__BYTE__",gato:"__GATO__"};
var IMG={},patG,carreg=0;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===4)iniciar();};im.src=SRC[key];})(k);}

var GW=6,GH=4,CELL=98,OX=(VW-GW*CELL)/2,OY=40;
function cellPx(gx,gy){return [OX+gx*CELL+CELL/2, OY+gy*CELL+CELL/2];}
var MIS=[
 {start:[0,3],home:[5,0],obst:[[2,2]],fala:"Ajude o gatinho a chegar em casa! Coloque plaquinhas mostrando o caminho."},
 {start:[0,0],home:[5,3],obst:[[2,1],[3,3],[4,0]],fala:"Mais um caminho! Desvie das pedras com as plaquinhas."}
];
var mi=0,gato={gx:0,gy:3,px:0,py:0,dir:1,resp:0,passo:0,mov:false},home={gx:5,gy:0},obst=[],signs={};
var byte={x:0,y:0,resp:0};
var exec={ativo:false,de:null,para:null,nx:0,ny:0,t:0,steps:0};
var balaoTxt=null,balaoT=0,audioOn=false,festa=0,estrelas=[];
var vagas=[];for(var i=0;i<14;i++)vagas.push({x:(i*151)%VW,y:(i*89)%VH,f:i});
var arvDeco=[[OX-36,OY+30],[OX+GW*CELL+36,OY+70],[OX-28,OY+GH*CELL],[OX+GW*CELL+30,OY+GH*CELL-30]];
var DIRS=[undefined,"dir","baixo","esq","cima"];

function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;
 for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falar(t){if(!audioOn||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}
 var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.98;u.pitch=1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,n){balaoTxt=t;balaoT=5;if(n!==false)falar(t);}
function toggleVoz(){audioOn=!audioOn;var b=document.getElementById("bVoz");if(audioOn){b.textContent="🔊 Ouvir";balao(MIS[mi].fala);}else{b.textContent="🔇";try{speechSynthesis.cancel();}catch(e){}}}

function setMissao(i){mi=i;var m=MIS[i];gato.gx=m.start[0];gato.gy=m.start[1];var p=cellPx(gato.gx,gato.gy);gato.px=p[0];gato.py=p[1];
 home.gx=m.home[0];home.gy=m.home[1];obst=m.obst;signs={};exec.ativo=false;balao(m.fala);}
function ehObst(gx,gy){for(var i=0;i<obst.length;i++)if(obst[i][0]===gx&&obst[i][1]===gy)return true;return false;}
function destrava(){if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
cv.addEventListener("mousedown",function(e){clic(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){clic(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});
function clic(cxp,cyp){if(exec.ativo)return;var r=cv.getBoundingClientRect();var mx=(cxp-r.left)*(VW/r.width),my=(cyp-r.top)*(VH/r.height);
 var gx=Math.floor((mx-OX)/CELL),gy=Math.floor((my-OY)/CELL);if(gx<0||gy<0||gx>=GW||gy>=GH)return;if(ehObst(gx,gy))return;if(gx===home.gx&&gy===home.gy)return;
 var key=gx+","+gy;var cur=signs[key],idx=DIRS.indexOf(cur);idx=(idx+1)%DIRS.length;if(DIRS[idx]===undefined)delete signs[key];else signs[key]=DIRS[idx];destrava();}
function limpar(){if(exec.ativo)return;signs={};}
function vai(){if(exec.ativo)return;destrava();exec.ativo=true;exec.steps=0;exec.de=null;document.getElementById("bVai").disabled=true;prox();}
function prox(){
 if(gato.gx===home.gx&&gato.gy===home.gy){ganhou();return;}
 var d=signs[gato.gx+","+gato.gy];
 if(!d){errou("O gatinho não sabe pra onde ir aqui! Ponha uma plaquinha nesta pedra.");return;}
 var nx=gato.gx+(d==="dir"?1:d==="esq"?-1:0),ny=gato.gy+(d==="baixo"?1:d==="cima"?-1:0);
 if(nx<0||ny<0||nx>=GW||ny>=GH||ehObst(nx,ny)){errou("Ops! A placa apontou para a parede. Vamos arrumar?");return;}
 exec.steps++;if(exec.steps>30){errou("O gatinho está rodando em círculos! Confira as placas.");return;}
 if(d==="esq")gato.dir=-1;else if(d==="dir")gato.dir=1;
 exec.de=cellPx(gato.gx,gato.gy);exec.para=cellPx(nx,ny);exec.nx=nx;exec.ny=ny;exec.t=0;}
function ganhou(){exec.ativo=false;festa=1;for(var i=0;i<16;i++)estrelas.push({x:gato.px+(Math.random()*70-35),y:gato.py-24,vx:Math.random()*60-30,vy:-(40+Math.random()*60),a:1,r:4+Math.random()*4});
 var ult=(mi>=MIS.length-1);balao(ult?"VIVA! O gatinho chegou em casa! Você ajudou muito bem!":"Isso! Chegou em casa! Vamos ajudar de novo?");
 document.getElementById("bVai").disabled=false;setTimeout(function(){festa=0;if(!ult)setMissao(mi+1);},ult?6000:3200);}
function errou(m){exec.ativo=false;balao(m);document.getElementById("bVai").disabled=false;}

function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");var p=cellPx(0,-1);byte.x=OX-4;byte.y=OY-6;setMissao(0);ult=null;requestAnimationFrame(frame);}

function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(15,10,25,.28)";cx.shadowColor="rgba(0,0,0,.3)";cx.shadowBlur=8;cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function pedra(x,y){sombra(x,y+18,26,8);var g=cx.createRadialGradient(x-8,y-8,4,x,y,30);g.addColorStop(0,"#9aa4ad");g.addColorStop(1,"#5c666f");cx.fillStyle=g;cx.beginPath();cx.ellipse(x,y,28,24,0,0,Math.PI*2);cx.fill();cx.fillStyle="rgba(255,255,255,.18)";cx.beginPath();cx.ellipse(x-8,y-8,10,7,0,0,Math.PI*2);cx.fill();}
function estrela(x,y,r,a){cx.save();cx.globalAlpha=a;cx.fillStyle="#ffd24a";cx.shadowColor="#ffd24a";cx.shadowBlur=10;cx.beginPath();for(var i=0;i<5;i++){var an=-Math.PI/2+i*2*Math.PI/5;cx.lineTo(x+Math.cos(an)*r,y+Math.sin(an)*r);var a2=an+Math.PI/5;cx.lineTo(x+Math.cos(a2)*r*.45,y+Math.sin(a2)*r*.45);}cx.closePath();cx.fill();cx.restore();cx.shadowBlur=0;}
var SETA={cima:[0,-1],baixo:[0,1],esq:[-1,0],dir:[1,0]};
function placa(x,y,d){ // poste + placa de madeira com seta
 cx.fillStyle="#6b4a28";cx.fillRect(x-2,y-6,4,20);
 cx.save();cx.translate(x,y-14);var g=cx.createLinearGradient(0,-11,0,11);g.addColorStop(0,"#c88a4a");g.addColorStop(1,"#9c6a34");cx.fillStyle=g;
 roundR(-16,-11,32,22,4);cx.fill();cx.strokeStyle="#5e3d1e";cx.lineWidth=2;roundR(-16,-11,32,22,4);cx.stroke();
 var v=SETA[d];cx.strokeStyle="#3a2410";cx.lineWidth=4;cx.lineCap="round";var ex=v[0]*9,ey=v[1]*7;
 cx.beginPath();cx.moveTo(-ex,-ey);cx.lineTo(ex,ey);cx.stroke();
 cx.beginPath();cx.moveTo(ex,ey);cx.lineTo(ex-v[0]*7-v[1]*6,ey-v[1]*7-v[0]*6);cx.moveTo(ex,ey);cx.lineTo(ex-v[0]*7+v[1]*6,ey-v[1]*7+v[0]*6);cx.stroke();cx.restore();}
function casinha(x,y,t){ // a casa do gatinho + brilho
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(x,y-6,4,x,y-6,50);g.addColorStop(0,"rgba(255,200,120,"+(0.4+0.15*Math.sin(t*0.005))+")");g.addColorStop(1,"rgba(255,200,120,0)");cx.fillStyle=g;cx.fillRect(x-55,y-55,110,110);cx.restore();
 sombra(x,y+16,30,9);cx.fillStyle="#b56a3a";roundR(x-26,y-8,52,26,4);cx.fill();
 cx.fillStyle="#8a4c28";cx.beginPath();cx.moveTo(x-32,y-6);cx.lineTo(x,y-34);cx.lineTo(x+32,y-6);cx.closePath();cx.fill();
 cx.fillStyle="#2a1810";cx.beginPath();cx.arc(x,y+6,11,Math.PI,0);cx.fill();cx.fillRect(x-11,y+6,22,12);
 cx.fillStyle="#ff9ec4";cx.font="bold 14px Verdana";cx.textAlign="center";cx.fillText("♥",x,y-14);}
function desGato(){var im=IMG.gato,h=60,w=im.width*h/im.height;var bob=gato.mov?Math.abs(Math.sin(gato.passo*.9))*5:0;var rp=gato.mov?0:Math.sin(gato.resp)*.03;
 sombra(gato.px,gato.py+20,18,6);cx.save();cx.translate(gato.px,gato.py+20-bob);cx.scale(gato.dir*(1+rp),1-rp*.6);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
function desByte(){var im=IMG.byte,h=64,w=im.width*h/im.height;var rp=Math.sin(byte.resp)*.03;sombra(byte.x,byte.y+22,18,6);
 cx.save();cx.translate(byte.x,byte.y+22);cx.scale(1+rp,1-rp*.6);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}

var ult=null;
function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 gato.resp+=dt*3;byte.resp+=dt*2.4;if(balaoT>0)balaoT-=dt;
 if(exec.ativo&&exec.de){exec.t+=dt/0.4;gato.mov=true;gato.passo+=dt*12;
  if(exec.t>=1){gato.px=exec.para[0];gato.py=exec.para[1];gato.gx=exec.nx;gato.gy=exec.ny;gato.mov=false;exec.de=null;prox();}
  else{var e=exec.t<.5?2*exec.t*exec.t:1-Math.pow(-2*exec.t+2,2)/2;gato.px=exec.de[0]+(exec.para[0]-exec.de[0])*e;gato.py=exec.de[1]+(exec.para[1]-exec.de[1])*e;}}
 else gato.mov=false;
 for(var i=estrelas.length-1;i>=0;i--){var s=estrelas[i];s.x+=s.vx*dt;s.y+=s.vy*dt;s.vy+=120*dt;s.a-=dt*.6;if(s.a<=0)estrelas.splice(i,1);}
 cx.fillStyle=patG;cx.fillRect(0,0,VW,VH);
 for(i=0;i<arvDeco.length;i++){var im=IMG.arvore,h=110,w=im.width*h/im.height;sombra(arvDeco[i][0],arvDeco[i][1]+4,26,8);var sw=Math.sin(t*.0015+arvDeco[i][0])*0.02;cx.save();cx.translate(arvDeco[i][0],arvDeco[i][1]);cx.rotate(sw);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
 // casas do caminho
 for(var gy=0;gy<GH;gy++)for(var gx=0;gx<GW;gx++){if(ehObst(gx,gy))continue;if(gx===home.gx&&gy===home.gy)continue;var p=cellPx(gx,gy);
   cx.fillStyle="rgba(255,255,255,.12)";cx.strokeStyle="rgba(255,255,255,.2)";cx.lineWidth=2;cx.beginPath();cx.ellipse(p[0],p[1]+16,38,20,0,0,Math.PI*2);cx.fill();cx.stroke();}
 // obstaculos
 for(i=0;i<obst.length;i++){var op=cellPx(obst[i][0],obst[i][1]);pedra(op[0],op[1]);}
 // casa do gato
 var hp=cellPx(home.gx,home.gy);casinha(hp[0],hp[1],t);
 // placas colocadas
 for(var key in signs){var pp=key.split(","),px=cellPx(+pp[0],+pp[1]);placa(px[0],px[1]+6,signs[key]);}
 // gato e byte-guia
 desGato();
 desByte();
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 // camadas de tela
 var lg=cx.createLinearGradient(0,0,0,VH);lg.addColorStop(0,"rgba(60,40,95,.10)");lg.addColorStop(1,"rgba(255,170,80,.10)");cx.fillStyle=lg;cx.fillRect(0,0,VW,VH);
 var vg=cx.createRadialGradient(VW/2,VH/2,VH*.42,VW/2,VH/2,VH*.9);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,.4)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<vagas.length;j++){var va=vagas[j];var vx=va.x+Math.sin(t*.001+va.f)*15,vy=va.y+Math.cos(t*.0011+va.f)*12;var aa=.25+.35*Math.sin(t*.003+va.f*2);cx.shadowColor="#fff2a0";cx.shadowBlur=8;cx.fillStyle="rgba(255,240,150,"+aa+")";cx.beginPath();cx.arc(vx,vy,2,0,Math.PI*2);cx.fill();}cx.restore();
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";cx.fillText("Missão "+(mi+1)+" de "+MIS.length+"  —  guie o gatinho até a casinha 🏠  (clique nas pedras p/ pôr setas)",VW/2,17);
 if(balaoT>0&&balaoTxt){var bx=byte.x+40,by=byte.y-30;cx.font="bold 12px Verdana";var tw=cx.measureText(balaoTxt).width,bw=Math.min(tw+22,VW-20),bh=28;
   var lx=Math.max(8,Math.min(VW-bw-8,bx-10)),ly=Math.max(28,by-bh);cx.globalAlpha=Math.min(1,balaoT/.6);
   cx.fillStyle="rgba(255,255,255,.96)";roundR(lx,ly,bw,bh,9);cx.fill();cx.beginPath();cx.moveTo(bx-6,ly+bh);cx.lineTo(bx+8,ly+bh);cx.lineTo(bx-2,ly+bh+9);cx.closePath();cx.fill();
   cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(balaoTxt,lx+bw/2,ly+bh/2+4);cx.globalAlpha=1;}
 requestAnimationFrame(frame);
}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
open(os.path.join(S,"byte-placas.html"),"w",encoding="utf-8").write(HTML)
print("OK -> byte-placas.html (",round(len(HTML)/1024),"KB )")
