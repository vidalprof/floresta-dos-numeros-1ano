# -*- coding: utf-8 -*-
# EducaVerso - PROVA DE TEMA: navio pirata (mesmo motor). Byte ANDA no convés,
# ondas suaves, e espuma de agua batendo no casco.
import base64, os, json as _json
S=os.path.dirname(os.path.abspath(__file__))
def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
IMGF={"mar":"mar.png","conves":"conves.png","byte":"byte.png","barril":"barril.png","bau":"bau.png"}
SRC={}
for k,fn in IMGF.items():
    p=os.path.join(S,fn)
    if os.path.exists(p): SRC[k]="data:image/png;base64,"+b64(p)
    else: print("!! falta",fn)
SRC_JSON=_json.dumps(SRC)

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EducaVerso - Navio Pirata</title>
<style>
 html,body{margin:0;min-height:100%;background:#08131f;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow-x:hidden;}
 #wrap{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:8px 0;}
 h1{font-size:15px;margin:4px 0 0;} .sub{font-size:11px;color:#9fc0df;margin:0 0 4px;width:100%;box-sizing:border-box;padding:0 8px;}
 #frame{padding:7px;border-radius:14px;background:#04101c;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #1f4a6e;max-width:96vw;box-sizing:border-box;}
 canvas{display:block;border-radius:10px;background:#2f79a8;max-width:100%;max-height:56vh;height:auto;}
 #dpad{display:none;margin:8px auto 0;grid-template-columns:repeat(3,56px);grid-template-rows:repeat(3,48px);gap:6px;justify-content:center;-webkit-user-select:none;user-select:none;}
 #dpad button{font-size:20px;font-weight:bold;border:0;border-radius:12px;color:#12325a;background:linear-gradient(#eaf3ff,#b7cbe9);box-shadow:0 3px 0 #7f93b3;touch-action:none;}
 .dU{grid-column:2;grid-row:1;}.dL{grid-column:1;grid-row:2;}.dR{grid-column:3;grid-row:2;}.dD{grid-column:2;grid-row:3;}
 .bt{font-family:inherit;font-weight:bold;border:0;border-radius:14px;cursor:pointer;padding:9px 16px;font-size:15px;color:#08131f;margin-top:6px;background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;}
 .subPC{display:block;} .subTouch{display:none;} body.touch #dpad{display:grid;} body.touch .subPC{display:none;} body.touch .subTouch{display:block;}
</style></head><body><div id="wrap">
 <h1>&#127988;&#8205;&#9760;&#65039; O Navio do Byte</h1>
 <p class="sub subPC">mesmo motor da floresta &#183; use as SETAS p/ o Byte andar no conv&#233;s</p>
 <p class="sub subTouch">mesmo motor da floresta &#183; use o D-pad p/ o Byte andar no conv&#233;s</p>
 <div id="frame"><canvas id="tela" width="720" height="480"></canvas></div>
 <div id="dpad"><button class="dU" id="dU">&#9650;</button><button class="dL" id="dL">&#9664;</button><button class="dR" id="dR">&#9654;</button><button class="dD" id="dD">&#9660;</button></div>
 <button class="bt" id="bSom" onclick="toggleSom()">&#128266; Som</button>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC=__SRC_JSON__,IMG={},carreg=0,NN=0;for(var kk in SRC)NN++;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===NN)iniciar();};im.onerror=function(){if(++carreg===NN)iniciar();};im.src=SRC[key];})(k);}
var patMar=null,patConv=null,som=false,AC=null,marG=null;
// convés (limites onde o Byte anda)
var DL=140,DR=590,DT=160,DB=395;
var byte={x:340,y:300,dir:1,mov:false,passo:0,resp:0};
var foam=[];for(var i=0;i<22;i++)foam.push({x:Math.random()*VW,y:Math.random()*VH,vx:6+Math.random()*10,vy:(Math.random()-.5)*4,r:2+Math.random()*3,ph:Math.random()*6.28});
var splashes=[];
var keys={},dp={U:false,D:false,L:false,R:false};
var IS_TOUCH=(("ontouchstart" in window)||(navigator.maxTouchPoints>0)||(window.matchMedia&&window.matchMedia("(pointer:coarse)").matches)||(location.search.indexOf("dpad=1")>=0));
if(IS_TOUCH){try{document.body.classList.add("touch");}catch(e){}}
window.addEventListener("keydown",function(e){keys[e.key]=true;if((e.key||"").indexOf("Arrow")===0){e.preventDefault();unlock();}});
window.addEventListener("keyup",function(e){keys[e.key]=false;});
function bindD(id,p){var el=document.getElementById(id);if(!el)return;function on(e){dp[p]=true;unlock();if(e.cancelable)e.preventDefault();}function off(e){dp[p]=false;}
 el.addEventListener("touchstart",on,{passive:false});el.addEventListener("touchend",off);el.addEventListener("touchcancel",off);el.addEventListener("mousedown",on);el.addEventListener("mouseup",off);el.addEventListener("mouseleave",off);}
bindD("dU","U");bindD("dD","D");bindD("dL","L");bindD("dR","R");
function iniciar(){if(IMG.mar)patMar=cx.createPattern(IMG.mar,"repeat");if(IMG.conves)patConv=cx.createPattern(IMG.conves,"repeat");requestAnimationFrame(frame);}

/* audio: ondas suaves */
function initA(){if(AC)return;try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return;}
 var n=Math.floor(AC.sampleRate*2),bf=AC.createBuffer(1,n,AC.sampleRate),d=bf.getChannelData(0);for(var i=0;i<n;i++)d[i]=Math.random()*2-1;
 var s=AC.createBufferSource();s.buffer=bf;s.loop=true;var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=480;
 var lfo=AC.createOscillator();lfo.frequency.value=0.14;var lg=AC.createGain();lg.gain.value=0.45;marG=AC.createGain();marG.gain.value=0;
 lfo.connect(lg);lg.connect(marG.gain);s.connect(f);f.connect(marG);marG.connect(AC.destination);s.start();lfo.start();}
function gaivota(){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();var t=AC.currentTime;o.type="sine";o.frequency.setValueAtTime(1400,t);o.frequency.linearRampToValueAtTime(1900,t+.12);o.frequency.linearRampToValueAtTime(1500,t+.24);g.gain.setValueAtTime(.05,t);g.gain.exponentialRampToValueAtTime(.001,t+.3);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+.3);}
function falar(txt){if(!som||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}var u=new SpeechSynthesisUtterance(txt);u.lang="pt-BR";u.pitch=1.1;try{speechSynthesis.speak(u);}catch(e){}}
function unlock(){initA();}
function toggleSom(){initA();som=!som;if(marG)marG.gain.value=som?0.5:0;var b=document.getElementById("bSom");
 if(som){b.innerHTML="&#128266; Som ligado";falar("Arr! Bem-vindo ao meu navio, marujo!");}else{b.innerHTML="&#128263; Mudo";}}

/* forma do casco (bico à direita) */
function casco(ins){var L=70+ins,R=VW-40-ins,T=95+ins,B=VH-40-ins,bico=R+58-ins*0.6,my=(T+B)/2,r=34;
 cx.beginPath();cx.moveTo(L+r,T);cx.lineTo(R,T);cx.quadraticCurveTo(bico,my,R,B);cx.lineTo(L+r,B);
 cx.quadraticCurveTo(L-14+ins*0.6,my,L+r,T);cx.closePath();}
// COLISAO: o Byte só anda DENTRO do casco (isPointInPath) e não atravessa os objetos
function onDeck(x,y){casco(30);return cx.isPointInPath(x,y);}
function inProp(x,y){var a=x-180,b=y-214;if(a*a+b*b<40*40)return true;var c=x-520,d=y-372;if(c*c+d*d<38*38)return true;return false;}
function podeAndar(x,y){return onDeck(x,y)&&!inProp(x,y);}
function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(6,20,30,.30)";cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function imgH(im,x,yb,h){var w=im.width*h/im.height;cx.drawImage(im,x-w/2,yb-h,w,h);}
// pontos ao longo do casco p/ nascer espuma (agua batendo)
var HULL=[[690,240],[90,240],[200,105],[430,105],[560,110],[200,435],[430,435],[560,430],[660,170],[660,310]];

var ult=null,gtimer=2.5,stimer=0;
function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 byte.resp+=dt*3;
 // ---- Byte anda (setas/D-pad), preso ao convés ----
 var vx=0,vy=0;
 if(keys["ArrowLeft"]||keys["a"]||keys["A"]||dp.L)vx-=1;
 if(keys["ArrowRight"]||keys["d"]||keys["D"]||dp.R)vx+=1;
 if(keys["ArrowUp"]||keys["w"]||keys["W"]||dp.U)vy-=1;
 if(keys["ArrowDown"]||keys["s"]||keys["S"]||dp.D)vy+=1;
 byte.mov=(vx||vy)?true:false;
 if(byte.mov){var L=Math.sqrt(vx*vx+vy*vy);vx/=L;vy/=L;var sp=115;
  var nx=byte.x+vx*sp*dt; if(podeAndar(nx,byte.y))byte.x=nx;      // desliza no eixo X
  var ny=byte.y+vy*sp*dt; if(podeAndar(byte.x,ny))byte.y=ny;      // desliza no eixo Y
  if(vx<-.2)byte.dir=-1;else if(vx>.2)byte.dir=1;byte.passo+=dt*10;}
 // ---- mar: deriva bem suave (swell) ----
 if(patMar){cx.save();var ox=Math.sin(t*.00018)*20-((t*0.008)%512),oy=Math.cos(t*.00022)*12;cx.translate(ox,oy);cx.fillStyle=patMar;cx.fillRect(-ox-4,-oy-4,VW+560,VH+560);cx.restore();}else{cx.fillStyle="#2f79a8";cx.fillRect(0,0,VW,VH);}
 // espuma flutuando (respawn suave, sem pulo)
 cx.save();cx.globalCompositeOperation="lighter";for(var i=0;i<foam.length;i++){var fo=foam[i];fo.x+=fo.vx*dt*6;fo.y+=(fo.vy+Math.sin(t*.0009+fo.ph)*3)*dt*6;if(fo.x>VW+12){fo.x=-12;fo.y=Math.random()*VH;}var a=.08+.10*(0.5+0.5*Math.sin(t*.0016+fo.ph));cx.fillStyle="rgba(255,255,255,"+a+")";cx.beginPath();cx.arc(fo.x,fo.y,fo.r,0,Math.PI*2);cx.fill();}cx.restore();
 // ---- AGUA BATENDO NO NAVIO: espuma nascendo no casco ----
 stimer-=dt;if(stimer<=0){stimer=0.28+Math.random()*0.25;var hp=HULL[(Math.floor(t*0.013)%HULL.length)];splashes.push({x:hp[0]+(Math.random()*20-10),y:hp[1]+(Math.random()*16-8),r:3,a:.7});if(Math.random()<.5){var hp2=HULL[Math.floor(Math.random()*HULL.length)];splashes.push({x:hp2[0],y:hp2[1],r:2,a:.6});}}
 // faixa de espuma pulsante ao redor do casco
 cx.save();cx.globalCompositeOperation="lighter";casco(2);cx.lineWidth=10+3*Math.sin(t*.004);cx.strokeStyle="rgba(255,255,255,"+(0.10+0.06*Math.sin(t*.003))+")";cx.stroke();cx.restore();
 // sombra do navio
 sombra(VW/2+6,VH/2+18,300,120);
 // ---- NAVIO balançando (suave) ----
 var ang=Math.sin(t*.0010)*0.022, bob=Math.sin(t*.0014)*5;
 cx.save();cx.translate(VW/2,VH/2+bob);cx.rotate(ang);cx.translate(-VW/2,-VH/2);
 casco(0);cx.fillStyle="#5a3a1e";cx.fill();
 cx.save();casco(15);cx.clip();if(patConv){cx.fillStyle=patConv;cx.fillRect(0,0,VW,VH);}else{cx.fillStyle="#b98a4e";cx.fillRect(0,0,VW,VH);}
 var g=cx.createRadialGradient(VW/2,VH/2,40,VW/2,VH/2,300);g.addColorStop(0,"rgba(0,0,0,0)");g.addColorStop(1,"rgba(30,18,8,.35)");cx.fillStyle=g;cx.fillRect(0,0,VW,VH);cx.restore();
 casco(0);cx.lineWidth=4;cx.strokeStyle="#3e2712";cx.stroke();
 casco(15);cx.lineWidth=2;cx.strokeStyle="rgba(255,240,210,.18)";cx.stroke();
 // props + byte (y-sort)
 var itens=[];
 if(IMG.barril)itens.push({y:214,f:function(){sombra(180,214,32,10);imgH(IMG.barril,180,214,84);}});
 if(IMG.bau)itens.push({y:372,f:function(){sombra(520,372,34,10);imgH(IMG.bau,520,372,66);}});
 itens.push({y:byte.y,f:function(){var bobb=byte.mov?Math.abs(Math.sin(byte.passo*.9))*5:0,rp=byte.mov?0:Math.sin(byte.resp)*.03;
   sombra(byte.x,byte.y+2,20,7);cx.save();cx.translate(byte.x,byte.y-bobb);cx.scale(byte.dir*(1+rp),1-rp*.5);imgH(IMG.byte,0,0,82);cx.restore();}});
 itens.sort(function(a,b){return a.y-b.y;});for(i=0;i<itens.length;i++)itens[i].f();
 cx.restore();
 // splashes por cima da borda (fora do rocking)
 for(i=splashes.length-1;i>=0;i--){var sp2=splashes[i];sp2.r+=dt*26;sp2.a-=dt*1.1;if(sp2.a<=0){splashes.splice(i,1);continue;}
  cx.save();cx.globalCompositeOperation="lighter";cx.strokeStyle="rgba(255,255,255,"+Math.max(0,sp2.a)+")";cx.lineWidth=2.5;cx.beginPath();cx.arc(sp2.x,sp2.y,sp2.r,0,Math.PI*2);cx.stroke();cx.restore();}
 // brilho do sol
 cx.save();cx.globalCompositeOperation="lighter";cx.globalAlpha=.05;cx.fillStyle="#fff6c0";cx.beginPath();cx.ellipse(VW*0.72,80,180,60,0,0,Math.PI*2);cx.fill();cx.restore();
 // HUD + balão
 cx.fillStyle="rgba(6,16,28,.5)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";cx.fillText("O mesmo Byte, agora navegando - ande pelo convés",VW/2,17);
 balao("Arr! Este é o meu navio. Ande por aqui, marujo!",VW/2,VH-34);
 gtimer-=dt;if(gtimer<=0){gtimer=3+Math.random()*3;gaivota();}
 requestAnimationFrame(frame);
}
function balao(txt,bx,by){cx.font="bold 13px Verdana";var w=cx.measureText(txt).width,bw=Math.min(w+24,VW-20),bh=28,lx=Math.max(8,Math.min(VW-bw-8,bx-bw/2)),ly=by-bh;
 cx.fillStyle="rgba(255,255,255,.96)";rr(lx,ly,bw,bh,10);cx.fill();cx.beginPath();cx.moveTo(bx-7,ly+bh);cx.lineTo(bx+7,ly+bh);cx.lineTo(bx,ly+bh+9);cx.closePath();cx.fill();
 cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(txt,lx+bw/2,ly+18);}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
</script></body></html>"""
HTML=HTML.replace("__SRC_JSON__",SRC_JSON)
out=os.path.join(S,"byte-navio.html")
open(out,"w",encoding="utf-8").write(HTML)
print("OK ->",out,"(",round(len(HTML)/1024),"KB )")
