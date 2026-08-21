# -*- coding: utf-8 -*-
import base64, os
S = os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
A={"__GRAMA__":b64("grama.png"),"__AGUA__":b64("agua.png"),"__AREIA__":b64("areia.png"),"__BYTE__":b64("byte.png"),"__ARVORE__":b64("arvore.png")}

HTML = r"""<!doctype html>
<html lang="pt-br"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EducaVerso - Mundo Vivo do Byte</title>
<style>
  html,body{margin:0;height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow:hidden;}
  #wrap{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;}
  h1{font-size:15px;margin:6px 0 2px;}
  .sub{font-size:11px;color:#9fb6df;margin:0 0 6px;}
  #frame{position:relative;padding:8px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;}
  canvas{display:block;border-radius:10px;background:#4a8a3a;max-width:96vw;height:auto;touch-action:none;cursor:pointer;}
  #ctrl{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center;}
  #ctrl button{font-family:inherit;font-size:13px;font-weight:bold;color:#0a1120;border:0;border-radius:20px;
    padding:8px 13px;cursor:pointer;background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;transition:transform .08s;}
  #ctrl button:active{transform:translateY(2px);box-shadow:0 1px 0 #b07d1e;}
  #ctrl button.on{background:linear-gradient(#8fe0ff,#3aa6e6);box-shadow:0 3px 0 #1f6fa0;}
  #btVoz{background:linear-gradient(#bff7d6,#5fd39a)!important;box-shadow:0 3px 0 #2f9463!important;}
  .cap{font-size:11px;color:#8fa8d4;margin-top:6px;}
  .k{display:inline-block;background:#1d335c;border:1px solid #35548a;border-radius:5px;padding:1px 6px;font-size:10px;}
</style></head><body>
<div id="wrap">
  <h1>&#127756; O Mundo Vivo do Byte</h1>
  <p class="sub">luz, nuvens, chuva, neve, raios, noite com lua, vento, ondas, colis&#227;o, poeira, fala e narra&#231;&#227;o</p>
  <div id="frame"><canvas id="tela" width="820" height="520"></canvas></div>
  <div id="ctrl">
    <button id="bSol" onclick="setClima('sol')">&#9728; Sol</button>
    <button id="bChuva" onclick="setClima('chuva')">&#127783; Chuva</button>
    <button id="bNeve" onclick="setClima('neve')">&#10052; Neve</button>
    <button id="bTemp" onclick="setClima('tempestade')">&#9928; Tempestade</button>
    <button id="bNoite" onclick="setClima('noite')">&#127769; Noite</button>
    <button id="btVoz" onclick="toggleVoz()">&#128266; Ouvir voz</button>
  </div>
  <p class="cap">Ande: <span class="k">&#8592;&#8593;&#8594;&#8595;</span>/<span class="k">WASD</span> ou <span class="k">clique</span> &#183; troque o clima nos bot&#245;es &#183; o Byte fala e narra.</p>
</div>
<script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d");
var VW=cv.width,VH=cv.height,WW=2200,WH=1500;
var SRC={grama:"__GRAMA__",agua:"__AGUA__",areia:"__AREIA__",byte:"__BYTE__",arvore:"__ARVORE__"};
var IMG={},patG,patA,patS,carreg=0;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===5)iniciar();};im.src=SRC[key];})(k);}

function edgeMar(y){return WW*0.64-(y/WH)*(WW*0.10)+Math.sin(y*0.009)*60+Math.sin(y*0.028)*18;}
var SAND=170;function edgeAreia(y){return edgeMar(y)-SAND;}
var byte={x:760,y:820,dir:1,vx:0,vy:0,mov:false,passo:0,resp:0,tx:null,ty:null};
var cam={x:0,y:0},hint=1;
var arvores=[[210,300],[420,780],[620,1120],[170,660],[330,440],[520,620],[260,1040],[660,320],[120,940],[720,780],[440,1220],[300,220],[560,980]];
var vagas=[];for(var i=0;i<26;i++)vagas.push({x:(i*151)%WW,y:(i*97)%WH,f:i});
var nuvens=[];for(i=0;i<7;i++)nuvens.push({x:Math.random()*WW,y:Math.random()*WH,r:130+Math.random()*130,a:0.09+Math.random()*0.07,s:7+Math.random()*9});
var estrelas=[];for(i=0;i<70;i++)estrelas.push({x:Math.random()*VW,y:Math.random()*VH*0.7,ph:Math.random()*6.28,r:0.6+Math.random()*1.4});
var clima="sol",vento=0.5,ventoAlvo=0.5,flash=0,proxRaio=4,raio=null;
var chuva=[],neve=[],poeira=[],ripples=[];
for(i=0;i<220;i++)chuva.push({x:Math.random()*VW,y:Math.random()*VH,l:8+Math.random()*10,s:600+Math.random()*300});
for(i=0;i<160;i++)neve.push({x:Math.random()*VW,y:Math.random()*VH,r:1.5+Math.random()*2.5,s:30+Math.random()*40,d:Math.random()*6.28});
var balaoTxt=null,balaoT=0,audioOn=false;

function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[];var best=null;
  for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");
    if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!best)best=vs[i];}return best;}
function falar(t){if(!audioOn||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}
  var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=0.98;u.pitch=1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,n){balaoTxt=t;balaoT=4.6;if(n!==false)falar(t);}
function toggleVoz(){audioOn=!audioOn;var b=document.getElementById("btVoz");
  if(audioOn){b.textContent="🔊 Voz ligada";b.classList.add("on");balao("Oi! Eu sou o Byte. Vamos explorar juntos?");}
  else{b.textContent="🔇 Voz desligada";b.classList.remove("on");try{speechSynthesis.cancel();}catch(e){}}}
var FALASCLIMA={sol:"Que dia lindo e ensolarado!",chuva:"Vai chover! Pingos de chuva!",neve:"Está nevando! Que frio gostoso!",tempestade:"Cuidado, vem tempestade com raios!",noite:"A noite chegou. Olhe a lua e as estrelas!"};
function setClima(c){clima=c;ventoAlvo=(c==="tempestade")?2.2:(c==="chuva"?1.2:(c==="neve"?0.9:0.5));
  if(c==="tempestade")proxRaio=1.2;
  ["bSol","bChuva","bNeve","bTemp","bNoite"].forEach(function(id){document.getElementById(id).classList.remove("on");});
  document.getElementById({sol:"bSol",chuva:"bChuva",neve:"bNeve",tempestade:"bTemp",noite:"bNoite"}[c]).classList.add("on");
  balao(FALASCLIMA[c]);}

var teclas={};
document.addEventListener("keydown",function(e){tc(e,1);});
document.addEventListener("keyup",function(e){tc(e,0);});
function tc(e,v){var c=e.keyCode;
  if(c===37||c===65)teclas.e=v;else if(c===39||c===68)teclas.d=v;
  else if(c===38||c===87)teclas.c=v;else if(c===40||c===83)teclas.b=v;else return;
  if(v){byte.tx=null;destrava();}if(e.preventDefault)e.preventDefault();}
function destrava(){if(!window._u&&window.speechSynthesis){window._u=1;try{var w=new SpeechSynthesisUtterance(" ");speechSynthesis.speak(w);}catch(e){}}}
function clique(px,py){var r=cv.getBoundingClientRect();var x=(px-r.left)*(VW/r.width)+cam.x,y=(py-r.top)*(VH/r.height)+cam.y;byte.tx=x;byte.ty=y;hint=0;destrava();}
cv.addEventListener("mousedown",function(e){clique(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){clique(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});

function alvoCam(){var ax=byte.x-VW/2,ay=byte.y-VH/2;ax=Math.max(0,Math.min(ax,WW-VW));ay=Math.max(0,Math.min(ay,WH-VH));return{x:ax,y:ay};}
function regAreia(){cx.beginPath();cx.moveTo(edgeAreia(0),0);for(var y=0;y<=WH;y+=10)cx.lineTo(edgeAreia(y),y);cx.lineTo(WW,WH);cx.lineTo(WW,0);cx.closePath();}
function regMar(){cx.beginPath();cx.moveTo(edgeMar(0),0);for(var y=0;y<=WH;y+=8)cx.lineTo(edgeMar(y),y);cx.lineTo(WW,WH);cx.lineTo(WW,0);cx.closePath();}
function sombra(x,y,rx,ry){var noite=clima==="noite";cx.save();cx.fillStyle=noite?"rgba(20,25,60,.34)":"rgba(20,12,30,.30)";
  cx.shadowColor="rgba(0,0,0,.35)";cx.shadowBlur=10;cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function colide(nx,ny){for(var i=0;i<arvores.length;i++){var a=arvores[i];var dx=nx-a[0],dy=ny-(a[1]-4);if(dx*dx+dy*dy<24*24)return true;}return false;}
function desenhaByte(){var im=IMG.byte,h=94,w=im.width*h/im.height;
  var bob=byte.mov?Math.abs(Math.sin(byte.passo*0.8))*6:0;var resp=byte.mov?0:Math.sin(byte.resp)*0.028;
  sombra(byte.x,byte.y,27-bob*0.5,9-bob*0.15);
  cx.save();cx.translate(byte.x,byte.y-bob);cx.scale(byte.dir*(1+resp),1-resp*0.6);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}

function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");patA=cx.createPattern(IMG.agua,"repeat");patS=cx.createPattern(IMG.areia,"repeat");
  var q=(location.search.match(/clima=(\w+)/)||[])[1];if(q){setClima(q);}else{document.getElementById("bSol").classList.add("on");}
  ult=null;requestAnimationFrame(frame);}

var ult=null,tpoeira=0;
function logica(dt,t){
  vento+=(ventoAlvo-vento)*Math.min(1,dt*1.5);
  var dx=0,dy=0;
  if(teclas.e)dx=-1;else if(teclas.d)dx=1;
  if(teclas.c)dy=-1;else if(teclas.b)dy=1;
  if(dx===0&&dy===0&&byte.tx!==null){var ax=byte.tx-byte.x,ay=byte.ty-byte.y,d=Math.sqrt(ax*ax+ay*ay);if(d>6){dx=ax/d;dy=ay/d;}else byte.tx=null;}
  var sp=185,tvx=dx*sp,tvy=dy*sp;
  byte.vx+=(tvx-byte.vx)*Math.min(1,dt*9);byte.vy+=(tvy-byte.vy)*Math.min(1,dt*9);
  var vel=Math.sqrt(byte.vx*byte.vx+byte.vy*byte.vy);byte.mov=vel>12;
  if(byte.vx<-6)byte.dir=-1;else if(byte.vx>6)byte.dir=1;
  var nx=byte.x+byte.vx*dt,ny=byte.y+byte.vy*dt;
  if(nx>edgeMar(ny)-32){nx=byte.x;byte.vx*=-0.2;byte.tx=null;}
  nx=Math.max(32,Math.min(WW-32,nx));ny=Math.max(90,Math.min(WH-20,ny));
  if(colide(nx,byte.y)){nx=byte.x;byte.vx*=-0.3;byte.tx=null;}
  if(colide(nx,ny)){ny=byte.y;byte.vy*=-0.3;byte.tx=null;}
  byte.x=nx;byte.y=ny;
  if(byte.mov){byte.passo+=dt*11;hint=Math.max(0,hint-dt*1.5);
    tpoeira-=dt;if(tpoeira<=0){tpoeira=0.11;poeira.push({x:byte.x+(Math.random()*10-5),y:byte.y,r:3,a:0.5,vx:(Math.random()*20-10)});}}
  byte.resp+=dt*3;
  for(var i=poeira.length-1;i>=0;i--){var p=poeira[i];p.r+=dt*22;p.a-=dt*1.1;p.y-=dt*6;p.x+=p.vx*dt;if(p.a<=0)poeira.splice(i,1);}
  for(i=0;i<nuvens.length;i++){var nu=nuvens[i];nu.x-=(nu.s+vento*10)*dt;if(nu.x<-nu.r)nu.x=WW+nu.r;}
  if(balaoT>0)balaoT-=dt;
  if(clima==="chuva"||clima==="tempestade"){for(i=0;i<chuva.length;i++){var r=chuva[i];r.y+=r.s*dt;r.x-=vento*30*dt;
    if(r.y>VH){r.y=-10;r.x=Math.random()*(VW+200)-100;var wx=r.x+cam.x;if(wx>edgeMar(r.y+cam.y))ripples.push({x:r.x,y:VH*Math.random(),r:1,a:0.4});}}}
  if(clima==="neve"){for(i=0;i<neve.length;i++){var s=neve[i];s.y+=s.s*dt;s.x+=Math.sin(t*0.001+s.d)*12*dt+vento*8*dt;if(s.y>VH){s.y=-6;s.x=Math.random()*VW;}}}
  for(i=ripples.length-1;i>=0;i--){var rp=ripples[i];rp.r+=dt*26;rp.a-=dt*0.9;if(rp.a<=0)ripples.splice(i,1);}
  if(clima==="tempestade"){proxRaio-=dt;if(proxRaio<=0){proxRaio=2+Math.random()*4;flash=1;
    var rx=cam.x+Math.random()*VW;raio={pts:[],t:0.35};var yy=0,xx=rx;raio.pts.push([xx,yy]);
    while(yy<WH*0.7){yy+=40+Math.random()*40;xx+=Math.random()*60-30;raio.pts.push([xx,yy]);}if(audioOn)trovao();}}
  if(flash>0)flash-=dt*2.2;if(raio){raio.t-=dt;if(raio.t<=0)raio=null;}
  var a=alvoCam();cam.x+=(a.x-cam.x)*Math.min(1,dt*7);cam.y+=(a.y-cam.y)*Math.min(1,dt*7);
}
var AC=null;
function trovao(){try{if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
  var n=AC.sampleRate*0.9,buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);
  for(var i=0;i<n;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/n,2);
  var src=AC.createBufferSource();src.buffer=buf;var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=380;
  var g=AC.createGain();g.gain.value=0.5;src.connect(f);f.connect(g);g.connect(AC.destination);src.start();}catch(e){}}
function corClima(){return clima==="tempestade"?["rgba(18,18,52,.5)","rgba(28,28,66,.46)"]:
  clima==="chuva"?["rgba(50,60,90,.30)","rgba(60,70,100,.28)"]:
  clima==="neve"?["rgba(150,170,210,.16)","rgba(180,200,230,.14)"]:
  clima==="noite"?["rgba(10,14,45,.6)","rgba(16,22,60,.55)"]:
  ["rgba(60,40,95,.14)","rgba(255,150,70,.11)"];}

function frame(ts){
  if(ult===null)ult=ts;var dt=Math.min(0.05,(ts-ult)/1000);ult=ts;var t=ts;
  logica(dt,t);
  cx.clearRect(0,0,VW,VH);
  cx.save();cx.translate(-cam.x,-cam.y);
  cx.fillStyle=patG;cx.fillRect(cam.x,cam.y,VW,VH);
  cx.save();regAreia();cx.clip();cx.fillStyle=patS;cx.fillRect(cam.x,cam.y,VW,VH);cx.restore();
  cx.save();regMar();cx.clip();cx.fillStyle=patA;cx.fillRect(cam.x,cam.y,VW,VH);
  cx.globalCompositeOperation="lighter";
  for(var s=0;s<7;s++){var yy=cam.y+((t*(0.04+vento*0.02)+s*120)%(VH+220))-110;
    var g=cx.createLinearGradient(0,yy,0,yy+64);g.addColorStop(0,"rgba(255,255,255,0)");
    g.addColorStop(.5,"rgba(255,255,255,"+(0.10+vento*0.03)+")");g.addColorStop(1,"rgba(255,255,255,0)");cx.fillStyle=g;cx.fillRect(cam.x,yy,VW,64);}
  cx.globalCompositeOperation="source-over";
  for(var i=0;i<ripples.length;i++){var rp=ripples[i];cx.strokeStyle="rgba(255,255,255,"+rp.a+")";cx.lineWidth=1.5;cx.beginPath();cx.arc(rp.x+cam.x,rp.y+cam.y,rp.r,0,Math.PI*2);cx.stroke();}
  cx.restore();
  cx.strokeStyle="rgba(255,255,255,.78)";cx.lineWidth=4;cx.beginPath();
  for(var y2=cam.y-10;y2<=cam.y+VH+10;y2+=6){var ex=edgeMar(y2)+Math.sin(t*0.004+y2*0.08)*(4+vento*3);if(y2<=cam.y-10)cx.moveTo(ex,y2);else cx.lineTo(ex,y2);}cx.stroke();
  cx.strokeStyle="rgba(255,255,255,.3)";cx.lineWidth=10;cx.stroke();
  for(i=0;i<poeira.length;i++){var p=poeira[i];cx.fillStyle="rgba(210,190,150,"+p.a+")";cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);cx.fill();}
  var elems=arvores.map(function(a){return{x:a[0],y:a[1],k:"arv"};});elems.push({x:byte.x,y:byte.y,k:"byte"});elems.sort(function(a,b){return a.y-b.y;});
  for(i=0;i<elems.length;i++){var el=elems[i];
    if(el.k==="arv"){var im=IMG.arvore,h=155,w=im.width*h/im.height;sombra(el.x,el.y,35,11);
      var ang=Math.sin(t*0.0016+el.x*0.5)*0.02*(0.6+vento);cx.save();cx.translate(el.x,el.y);cx.rotate(ang);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
    else desenhaByte();}
  /* nuvens (sombra deslizando no chao) - nao na neve */
  if(clima!=="neve"){for(i=0;i<nuvens.length;i++){var nu=nuvens[i];
    var g3=cx.createRadialGradient(nu.x,nu.y,nu.r*0.2,nu.x,nu.y,nu.r);
    g3.addColorStop(0,"rgba(15,25,40,"+nu.a+")");g3.addColorStop(1,"rgba(15,25,40,0)");
    cx.fillStyle=g3;cx.beginPath();cx.ellipse(nu.x,nu.y,nu.r,nu.r*0.6,0,0,Math.PI*2);cx.fill();}}
  cx.restore();
  /* ===== tela ===== */
  var cc=corClima();var g2=cx.createLinearGradient(0,0,0,VH);g2.addColorStop(0,cc[0]);g2.addColorStop(1,cc[1]);cx.fillStyle=g2;cx.fillRect(0,0,VW,VH);
  /* sol cintilando */
  if(clima==="sol"){var pulse=0.5+0.5*Math.sin(t*0.0009);cx.save();cx.globalCompositeOperation="lighter";
    var gs=cx.createRadialGradient(VW*0.83,VH*0.1,20,VW*0.83,VH*0.1,VH*0.95);
    gs.addColorStop(0,"rgba(255,244,200,"+(0.15+pulse*0.07)+")");gs.addColorStop(1,"rgba(255,244,200,0)");cx.fillStyle=gs;cx.fillRect(0,0,VW,VH);cx.restore();}
  /* noite: lua + estrelas */
  if(clima==="noite"){for(i=0;i<estrelas.length;i++){var st=estrelas[i];var tw=0.4+0.6*Math.abs(Math.sin(t*0.002+st.ph));
    cx.fillStyle="rgba(255,255,255,"+tw+")";cx.beginPath();cx.arc(st.x,st.y,st.r,0,Math.PI*2);cx.fill();}
    cx.save();cx.globalCompositeOperation="lighter";var gl=cx.createRadialGradient(VW*0.84,VH*0.14,8,VW*0.84,VH*0.14,110);
    gl.addColorStop(0,"rgba(220,230,255,.9)");gl.addColorStop(.25,"rgba(200,215,255,.5)");gl.addColorStop(1,"rgba(200,215,255,0)");cx.fillStyle=gl;cx.fillRect(0,0,VW,VH);
    cx.fillStyle="#eef3ff";cx.beginPath();cx.arc(VW*0.84,VH*0.14,26,0,Math.PI*2);cx.fill();
    cx.fillStyle=cc[0];cx.beginPath();cx.arc(VW*0.84+9,VH*0.14-6,24,0,Math.PI*2);cx.fill();cx.restore();}
  if(clima==="chuva"||clima==="tempestade"){cx.strokeStyle="rgba(200,220,255,.5)";cx.lineWidth=1.4;cx.beginPath();
    for(i=0;i<chuva.length;i++){var r=chuva[i];cx.moveTo(r.x,r.y);cx.lineTo(r.x-vento*4,r.y+r.l);}cx.stroke();}
  if(clima==="neve"){cx.fillStyle="rgba(255,255,255,.9)";for(i=0;i<neve.length;i++){var sn=neve[i];cx.beginPath();cx.arc(sn.x,sn.y,sn.r,0,Math.PI*2);cx.fill();}}
  if(raio){cx.strokeStyle="rgba(255,255,240,.95)";cx.lineWidth=3;cx.shadowColor="#fff";cx.shadowBlur=16;cx.beginPath();
    for(i=0;i<raio.pts.length;i++){var pt=raio.pts[i];var sx=pt[0]-cam.x,sy=pt[1]-cam.y;if(i===0)cx.moveTo(sx,sy);else cx.lineTo(sx,sy);}cx.stroke();cx.shadowBlur=0;}
  if(flash>0){cx.fillStyle="rgba(255,255,255,"+(flash*0.5)+")";cx.fillRect(0,0,VW,VH);}
  var vg=cx.createRadialGradient(VW/2,VH/2,VH*0.36,VW/2,VH/2,VH*0.85);vg.addColorStop(0,"rgba(0,0,0,0)");
  vg.addColorStop(1,(clima==="tempestade"||clima==="noite")?"rgba(3,5,16,.66)":"rgba(6,10,25,.5)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
  if(clima==="sol"||clima==="noite"){cx.save();cx.globalCompositeOperation="lighter";
    for(var j=0;j<vagas.length;j++){var va=vagas[j];var vx=va.x-cam.x+Math.sin(t*0.001+va.f)*16,vy=va.y-cam.y+Math.cos(t*0.0011+va.f*1.3)*14;
      if(vx<-20||vx>VW+20||vy<-20||vy>VH+20)continue;var aa=0.3+0.4*Math.sin(t*0.003+va.f*2);
      cx.shadowColor="#fff2a0";cx.shadowBlur=9;cx.fillStyle="rgba(255,240,150,"+aa+")";cx.beginPath();cx.arc(vx,vy,2.2,0,Math.PI*2);cx.fill();}cx.restore();}
  if(balaoT>0&&balaoTxt){var bx=byte.x-cam.x,by=byte.y-cam.y-100;cx.font="bold 14px Verdana";var tw2=cx.measureText(balaoTxt).width,bw=tw2+28,bh=34;
    var lx=Math.max(8,Math.min(VW-bw-8,bx-bw/2)),ly=Math.max(6,by-bh);cx.globalAlpha=Math.min(1,balaoT/0.6);
    cx.fillStyle="rgba(255,255,255,.96)";roundR(lx,ly,bw,bh,10);cx.fill();
    cx.beginPath();cx.moveTo(bx-8,ly+bh);cx.lineTo(bx+8,ly+bh);cx.lineTo(bx,ly+bh+11);cx.closePath();cx.fill();
    cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(balaoTxt,lx+bw/2,ly+bh/2+5);cx.globalAlpha=1;}
  if(hint>0){cx.globalAlpha=Math.min(1,hint);cx.fillStyle="rgba(8,16,30,.7)";roundR((VW-360)/2,VH-42,360,28,8);cx.fill();
    cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";cx.fillText("Use as setas ou CLIQUE para o Byte andar",VW/2,VH-23);cx.globalAlpha=1;}
  requestAnimationFrame(frame);
}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);
  cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
out=os.path.join(S,"byte-mundo-vivo.html")
open(out,"w",encoding="utf-8").write(HTML)
print("OK ->",out,"(",round(len(HTML)/1024),"KB )")
