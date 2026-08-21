# -*- coding: utf-8 -*-
import base64, os
S=os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
A={"__GRAMA__":b64("grama.png"),"__AGUA__":b64("agua.png"),"__ARVORE__":b64("arvore.png"),"__BYTE__":b64("byte.png"),"__GATO__":b64("gato.png")}

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EducaVerso - O Jardim do Byte</title>
<style>
 html,body{margin:0;height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow:hidden;}
 #wrap{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;}
 h1{font-size:15px;margin:4px 0 0;} .sub{font-size:11px;color:#9fb6df;margin:0 0 4px;}
 #frame{padding:7px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;}
 canvas{display:block;border-radius:10px;background:#4a8a3a;max-width:96vw;height:auto;}
 #painel{display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:center;margin-top:6px;max-width:96vw;}
 #prog{display:flex;gap:3px;min-height:34px;min-width:150px;background:#0e1a30;border:2px dashed #35548a;border-radius:10px;padding:4px 8px;align-items:center;}
 .chip{width:26px;height:26px;border-radius:6px;background:#2b60a8;display:flex;align-items:center;justify-content:center;font-size:16px;color:#fff;}
 .bt{font-family:inherit;font-weight:bold;border:0;border-radius:12px;cursor:pointer;padding:8px 11px;font-size:16px;color:#0a1120;background:linear-gradient(#cfe3ff,#8fb8ef);box-shadow:0 3px 0 #4d74b8;}
 .bt:active{transform:translateY(2px);box-shadow:0 1px 0 #4d74b8;}
 .bt.vai{background:linear-gradient(#bff7d6,#4fcf8e);box-shadow:0 3px 0 #2f9463;padding:8px 16px;}
 .bt.lp{background:linear-gradient(#ffd0d0,#f08a8a);box-shadow:0 3px 0 #b04d4d;}
 .bt.vz{background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;}
 .bt:disabled{opacity:.5;filter:grayscale(.5);}
</style></head><body><div id="wrap">
 <h1>&#127793; O Jardim do Byte</h1>
 <p class="sub">monte o caminho com as setas &#183; aperte VAI &#183; leve o Byte at&#233; o gatinho!</p>
 <div id="frame"><canvas id="tela" width="720" height="470"></canvas></div>
 <div id="painel">
   <span style="font-size:11px;color:#9fb6df">Seu caminho:</span>
   <div id="prog"></div>
   <button class="bt" onclick="addSeta('cima')">&#8593;</button>
   <button class="bt" onclick="addSeta('baixo')">&#8595;</button>
   <button class="bt" onclick="addSeta('esq')">&#8592;</button>
   <button class="bt" onclick="addSeta('dir')">&#8594;</button>
   <button class="bt vai" id="bVai" onclick="vai()">&#9654; VAI!</button>
   <button class="bt lp" onclick="limpar()">&#128465;</button>
   <button class="bt vz" id="bVoz" onclick="toggleVoz()">&#128266;</button>
 </div>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC={grama:"__GRAMA__",agua:"__AGUA__",arvore:"__ARVORE__",byte:"__BYTE__",gato:"__GATO__"};
var IMG={},patG,carreg=0;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===5)iniciar();};im.src=SRC[key];})(k);}

var GW=6,GH=4,CELL=98,OX=(VW-GW*CELL)/2,OY=34;
function cellPx(gx,gy){return [OX+gx*CELL+CELL/2, OY+gy*CELL+CELL/2];}
var MISSOES=[
 {sx:1,sy:2,cx:4,sy2:2,gx2:4,gy2:2, start:[1,2], gato:[4,2], obst:[], fala:"Monte o caminho para eu chegar no gatinho!"},
 {start:[1,3], gato:[3,1], obst:[[3,3],[0,1]], fala:"Agora precisa virar! Use setas para cima e para o lado."},
 {start:[1,2], gato:[4,2], obst:[[2,2],[3,3]], fala:"Cuidado com a pedra! Contorne para chegar no gatinho."}
];
var mi=0, byte={gx:1,gy:2,px:0,py:0,dir:1,resp:0,passo:0,mov:false},gato={gx:4,gy:2},obst=[];
var programa=[],exec={ativo:false,moves:[],i:0,t:0,de:null,para:null,falhou:false};
var balaoTxt=null,balaoT=0,audioOn=false,festa=0,estrelas=[];
var vagas=[];for(var i=0;i<16;i++)vagas.push({x:(i*151)%VW,y:(i*89)%VH,f:i});
var arvDeco=[[OX-38,OY+40],[OX+GW*CELL+38,OY+80],[OX-30,OY+GH*CELL-10],[OX+GW*CELL+30,OY+GH*CELL-20]];

function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;
 for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falar(t){if(!audioOn||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}
 var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.98;u.pitch=1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,n){balaoTxt=t;balaoT=4.8;if(n!==false)falar(t);}
function toggleVoz(){audioOn=!audioOn;var b=document.getElementById("bVoz");
 if(audioOn){b.textContent="🔊";var m=MISSOES[mi];balao(m.fala);}else{b.textContent="🔇";try{speechSynthesis.cancel();}catch(e){}}}

function setMissao(i){mi=i;var m=MISSOES[i];byte.gx=m.start[0];byte.gy=m.start[1];var p=cellPx(byte.gx,byte.gy);byte.px=p[0];byte.py=p[1];
 gato.gx=m.gato[0];gato.gy=m.gato[1];obst=m.obst;programa=[];exec.ativo=false;exec.falhou=false;renderProg();
 balao(m.fala);}
var SET={cima:"↑",baixo:"↓",esq:"←",dir:"→"};
function addSeta(d){if(exec.ativo)return;if(programa.length>=12)return;programa.push(d);renderProg();}
function limpar(){if(exec.ativo)return;programa=[];renderProg();}
function renderProg(){var el=document.getElementById("prog");el.innerHTML="";for(var i=0;i<programa.length;i++){var c=document.createElement("div");c.className="chip";c.textContent=SET[programa[i]];el.appendChild(c);}}
function vai(){if(exec.ativo||!programa.length)return;destrava();exec.ativo=true;exec.moves=programa.slice();exec.i=0;exec.t=0;exec.falhou=false;exec.de=null;document.getElementById("bVai").disabled=true;prepararPasso();}
function destrava(){if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
function prepararPasso(){
 if(exec.i>=exec.moves.length){ // acabou a sequencia
   if(byte.gx===gato.gx&&byte.gy===gato.gy){ganhou();}else{errou("Quase! O caminho não chegou no gatinho. Tente de novo!");}return;}
 var d=exec.moves[exec.i];var nx=byte.gx+(d==="dir"?1:d==="esq"?-1:0),ny=byte.gy+(d==="baixo"?1:d==="cima"?-1:0);
 if(nx<0||ny<0||nx>=GW||ny>=GH||ehObst(nx,ny)){errou("Ops! O Byte bateu. Vamos arrumar o caminho?");return;}
 if(d==="esq")byte.dir=-1;else if(d==="dir")byte.dir=1;
 exec.de=cellPx(byte.gx,byte.gy);exec.para=cellPx(nx,ny);exec.nx=nx;exec.ny=ny;exec.t=0;}
function ehObst(gx,gy){for(var i=0;i<obst.length;i++)if(obst[i][0]===gx&&obst[i][1]===gy)return true;return false;}
function ganhou(){exec.ativo=false;festa=1;for(var i=0;i<16;i++)estrelas.push({x:byte.px+(Math.random()*80-40),y:byte.py-30,vy:-(40+Math.random()*60),vx:(Math.random()*60-30),a:1,r:4+Math.random()*4});
 var ultima=(mi>=MISSOES.length-1);
 balao(ultima?"VOCÊ CONSEGUIU! Salvou todos os amiguinhos! Que festa!":"Isso! O gatinho está salvo! Vamos para o próximo?");
 document.getElementById("bVai").disabled=false;
 setTimeout(function(){festa=0;if(!ultima)setMissao(mi+1);},ultima?6000:3000);}
function errou(msg){exec.ativo=false;exec.falhou=true;balao(msg);document.getElementById("bVai").disabled=false;}

function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");setMissao(0);ult=null;requestAnimationFrame(frame);}

function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(15,10,25,.28)";cx.shadowColor="rgba(0,0,0,.3)";cx.shadowBlur=8;cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function pedra(x,y){sombra(x,y+18,26,8);var g=cx.createRadialGradient(x-8,y-8,4,x,y,30);g.addColorStop(0,"#9aa4ad");g.addColorStop(1,"#5c666f");cx.fillStyle=g;
 cx.beginPath();cx.ellipse(x,y,28,24,0,0,Math.PI*2);cx.fill();cx.fillStyle="rgba(255,255,255,.18)";cx.beginPath();cx.ellipse(x-8,y-8,10,7,0,0,Math.PI*2);cx.fill();}
function estrela(x,y,r,a){cx.save();cx.globalAlpha=a;cx.fillStyle="#ffd24a";cx.shadowColor="#ffd24a";cx.shadowBlur=10;cx.beginPath();
 for(var i=0;i<5;i++){var ang=-Math.PI/2+i*2*Math.PI/5;cx.lineTo(x+Math.cos(ang)*r,y+Math.sin(ang)*r);var a2=ang+Math.PI/5;cx.lineTo(x+Math.cos(a2)*r*.45,y+Math.sin(a2)*r*.45);}
 cx.closePath();cx.fill();cx.restore();cx.shadowBlur=0;}
function desenhaByte(){var im=IMG.byte,h=76,w=im.width*h/im.height;var bob=byte.mov?Math.abs(Math.sin(byte.passo*.9))*5:0;var rp=byte.mov?0:Math.sin(byte.resp)*.03;
 sombra(byte.px,byte.py+26,22,7);cx.save();cx.translate(byte.px,byte.py+26-bob);cx.scale(byte.dir*(1+rp),1-rp*.6);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}

var ult=null;
function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 byte.resp+=dt*3;if(balaoT>0)balaoT-=dt;
 // execucao do programa
 if(exec.ativo&&exec.de){exec.t+=dt/0.42;byte.mov=true;byte.passo+=dt*12;
   if(exec.t>=1){exec.t=1;byte.px=exec.para[0];byte.py=exec.para[1];byte.gx=exec.nx;byte.gy=exec.ny;byte.mov=false;
     if(byte.gx===gato.gx&&byte.gy===gato.gy){ganhou();}else{exec.i++;exec.de=null;prepararPasso();}}
   else{var e=exec.t<.5?2*exec.t*exec.t:1-Math.pow(-2*exec.t+2,2)/2;byte.px=exec.de[0]+(exec.para[0]-exec.de[0])*e;byte.py=exec.de[1]+(exec.para[1]-exec.de[1])*e;}}
 else byte.mov=false;
 for(var i=estrelas.length-1;i>=0;i--){var s=estrelas[i];s.x+=s.vx*dt;s.y+=s.vy*dt;s.vy+=120*dt;s.a-=dt*.6;if(s.a<=0)estrelas.splice(i,1);}
 // ===== desenho =====
 cx.fillStyle=patG;cx.fillRect(0,0,VW,VH);
 // arvores decorativas nas bordas
 for(i=0;i<arvDeco.length;i++){var im=IMG.arvore,h=120,w=im.width*h/im.height;sombra(arvDeco[i][0],arvDeco[i][1]+4,28,9);var sw=Math.sin(t*.0015+arvDeco[i][0])*0.02;cx.save();cx.translate(arvDeco[i][0],arvDeco[i][1]);cx.rotate(sw);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
 // casas do caminho (pedrinhas onde da pra andar)
 for(var gy=0;gy<GH;gy++)for(var gx=0;gx<GW;gx++){if(ehObst(gx,gy))continue;var p=cellPx(gx,gy);
   cx.fillStyle="rgba(255,255,255,.13)";cx.strokeStyle="rgba(255,255,255,.22)";cx.lineWidth=2;
   cx.beginPath();cx.ellipse(p[0],p[1]+18,38,20,0,0,Math.PI*2);cx.fill();cx.stroke();}
 // destino: brilho na casa do gatinho
 var gp=cellPx(gato.gx,gato.gy);cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(gp[0],gp[1],4,gp[0],gp[1],54);
 g.addColorStop(0,"rgba(120,255,170,"+(0.35+0.15*Math.sin(t*0.005))+")");g.addColorStop(1,"rgba(120,255,170,0)");cx.fillStyle=g;cx.fillRect(gp[0]-60,gp[1]-60,120,120);cx.restore();
 // obstaculos
 for(i=0;i<obst.length;i++){var op=cellPx(obst[i][0],obst[i][1]);pedra(op[0],op[1]);}
 // gatinho (respira)
 var im2=IMG.gato,gh=64,gw=im2.width*gh/im2.height;var gr=Math.sin(t*0.002)*0.03;sombra(gp[0],gp[1]+22,20,7);
 cx.save();cx.translate(gp[0],gp[1]+22);cx.scale(1,1+gr);cx.drawImage(im2,-gw/2,-gh,gw,gh);cx.restore();
 // byte
 desenhaByte();
 // estrelas de festa
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 // ===== camadas de tela =====
 var lg=cx.createLinearGradient(0,0,0,VH);lg.addColorStop(0,"rgba(60,40,95,.10)");lg.addColorStop(1,"rgba(255,170,80,.10)");cx.fillStyle=lg;cx.fillRect(0,0,VW,VH);
 var vg=cx.createRadialGradient(VW/2,VH/2,VH*.42,VW/2,VH/2,VH*.9);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,.4)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<vagas.length;j++){var va=vagas[j];var vx=va.x+Math.sin(t*.001+va.f)*15,vy=va.y+Math.cos(t*.0011+va.f)*12;var aa=.25+.35*Math.sin(t*.003+va.f*2);cx.shadowColor="#fff2a0";cx.shadowBlur=8;cx.fillStyle="rgba(255,240,150,"+aa+")";cx.beginPath();cx.arc(vx,vy,2,0,Math.PI*2);cx.fill();}cx.restore();
 // titulo da missao
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";
 cx.fillText("Missão "+(mi+1)+" de "+MISSOES.length+"   —   leve o Byte até o gatinho 🐱",VW/2,17);
 // balao do Byte
 if(balaoT>0&&balaoTxt){var bx=byte.px,by=byte.py-58;cx.font="bold 13px Verdana";var tw=cx.measureText(balaoTxt).width,bw=Math.min(tw+24,VW-20),bh=30;
   var lx=Math.max(8,Math.min(VW-bw-8,bx-bw/2)),ly=Math.max(30,by-bh);cx.globalAlpha=Math.min(1,balaoT/.6);
   cx.fillStyle="rgba(255,255,255,.96)";roundR(lx,ly,bw,bh,9);cx.fill();cx.beginPath();cx.moveTo(bx-7,ly+bh);cx.lineTo(bx+7,ly+bh);cx.lineTo(bx,ly+bh+9);cx.closePath();cx.fill();
   cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(balaoTxt,lx+bw/2,ly+bh/2+5);cx.globalAlpha=1;}
 requestAnimationFrame(frame);
}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
open(os.path.join(S,"byte-jardim.html"),"w",encoding="utf-8").write(HTML)
print("OK -> byte-jardim.html (",round(len(HTML)/1024),"KB )")
