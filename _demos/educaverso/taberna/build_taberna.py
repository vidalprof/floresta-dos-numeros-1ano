# -*- coding: utf-8 -*-
import base64, os
S=os.path.dirname(os.path.abspath(__file__))
def b64(n):
    with open(os.path.join(S,n),"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()
names={"grama":"grama.png","arvore":"arvore.png","byte":"byte.png","fachada":"fachada.png",
       "madeira":"madeira.png","parede":"parede.png","taberneiro":"taberneiro.png","gato":"gato.png","lampiao":"lampiao.png"}
A={("__%s__"%k.upper()):b64(v) for k,v in names.items()}

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EducaVerso - A Taberna do Byte</title>
<style>
 html,body{margin:0;height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow:hidden;}
 #wrap{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;}
 h1{font-size:15px;margin:6px 0 2px;} .sub{font-size:11px;color:#9fb6df;margin:0 0 6px;}
 #frame{position:relative;padding:8px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;}
 canvas{display:block;border-radius:10px;background:#4a8a3a;max-width:96vw;height:auto;touch-action:none;cursor:pointer;}
 #ctrl{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center;}
 #ctrl button{font-family:inherit;font-size:13px;font-weight:bold;color:#0a1120;border:0;border-radius:20px;padding:8px 14px;cursor:pointer;background:linear-gradient(#bff7d6,#5fd39a);box-shadow:0 3px 0 #2f9463;}
 #ctrl button:active{transform:translateY(2px);box-shadow:0 1px 0 #2f9463;}
 .cap{font-size:11px;color:#8fa8d4;margin-top:6px;} .k{display:inline-block;background:#1d335c;border:1px solid #35548a;border-radius:5px;padding:1px 6px;font-size:10px;}
</style></head><body><div id="wrap">
 <h1>&#127775; A Taberna do Byte &#8212; EducaVerso</h1>
 <p class="sub">ache a chave &#183; abra a porta de verdade &#183; entre e converse com os personagens &#183; luz de lampi&#227;o</p>
 <div id="frame"><canvas id="tela" width="840" height="540"></canvas></div>
 <div id="ctrl"><button id="btVoz" onclick="toggleVoz()">&#128266; Ouvir voz</button></div>
 <p class="cap">Ande: <span class="k">&#8592;&#8593;&#8594;&#8595;</span>/<span class="k">WASD</span> ou <span class="k">clique</span> &#183; <span class="k">E</span> para pegar/entrar/falar.</p>
</div><script>
var cv=document.getElementById("tela"),cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC={grama:"__GRAMA__",arvore:"__ARVORE__",byte:"__BYTE__",fachada:"__FACHADA__",madeira:"__MADEIRA__",parede:"__PAREDE__",taberneiro:"__TABERNEIRO__",gato:"__GATO__",lampiao:"__LAMPIAO__"};
var IMG={},patG,patM,patP,carreg=0;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===9)iniciar();};im.src=SRC[key];})(k);}

var cena="fora",inv={chave:false};
var byte={x:800,y:760,vx:0,vy:0,dir:1,passo:0,resp:0,mov:false,tx:null};
var cam={x:0,y:0},hint=1,fade=0,fadeDir=0,fadeAcao=null,proxE=null;
var balaoTxt=null,balaoT=0,balaoAlvo=null,audioOn=false;
/* MUNDO FORA */
var FW=1600,FH=1120,fx=800,fy=560; /* fachada base */
var arvoresF=[[200,760],[1300,700],[300,300],[1250,300],[150,1000],[1350,980]];
var chave={x:360,y:820,peg:false};
/* TABERNA DENTRO */
var RW=1120,RH=740,T=54;
var lampioes=[[200,120],[560,108],[920,120],[120,560],[1000,560]];
var tab={x:560,y:250},gato={x:800,y:470};
var vagas=[];for(var i=0;i<20;i++)vagas.push({x:(i*151)%FW,y:(i*97)%FH,f:i});

function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;
 for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falar(t){if(!audioOn||!window.speechSynthesis)return;try{speechSynthesis.cancel();}catch(e){}
 var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.98;u.pitch=1.1;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
function balao(t,alvo,n){balaoTxt=t;balaoT=4.6;balaoAlvo=alvo||"byte";if(n!==false)falar(t);}
function toggleVoz(){audioOn=!audioOn;var b=document.getElementById("btVoz");
 if(audioOn){b.textContent="🔊 Voz ligada";balao("Oi! Eu sou o Byte. Vamos achar a chave da taberna?","byte");}else{b.textContent="🔇 Voz desligada";try{speechSynthesis.cancel();}catch(e){}}}

var teclas={};
document.addEventListener("keydown",function(e){var c=e.keyCode;
 if(c===37||c===65)teclas.e=1;else if(c===39||c===68)teclas.d=1;else if(c===38||c===87)teclas.c=1;else if(c===40||c===83)teclas.b=1;
 else if(c===69){acaoE();}else return; byte.tx=null;destrava();if(e.preventDefault)e.preventDefault();});
document.addEventListener("keyup",function(e){var c=e.keyCode;
 if(c===37||c===65)teclas.e=0;else if(c===39||c===68)teclas.d=0;else if(c===38||c===87)teclas.c=0;else if(c===40||c===83)teclas.b=0;});
function destrava(){if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
function clique(px,py){var r=cv.getBoundingClientRect();byte.tx=(px-r.left)*(VW/r.width)+cam.x;byte.ty=(py-r.top)*(VH/r.height)+cam.y;hint=0;destrava();}
cv.addEventListener("mousedown",function(e){clique(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){clique(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});

function irPara(nc,bx,by){if(fadeDir)return;fadeDir=1;fadeAcao=function(){cena=nc;byte.x=bx;byte.y=by;byte.vx=byte.vy=0;byte.tx=null;hint=0;};}
function acaoE(){destrava();
 if(cena==="fora"){
   if(!chave.peg && dist(byte.x,byte.y,chave.x,chave.y)<48){chave.peg=true;inv.chave=true;balao("Achei a chave! Agora posso abrir a taberna.","byte");return;}
   if(dist(byte.x,byte.y,fx,fy+18)<70){ if(inv.chave){balao("Vou entrar!","byte");setTimeout(function(){irPara("dentro",RW/2,RH-90);},500);}
     else balao("A porta está trancada. Preciso achar a chave!","byte"); return;}
 } else {
   if(dist(byte.x,byte.y,tab.x,tab.y+40)<80){balao("Bem-vindo à minha taberna, viajante! Sente-se e descanse.","tab");return;}
   if(dist(byte.x,byte.y,gato.x,gato.y+20)<70){balao("Miau! O gatinho ronrona feliz.","gato");return;}
   if(byte.y>RH-96 && Math.abs(byte.x-RW/2)<70){balao("Até logo!","byte");setTimeout(function(){irPara("fora",fx,fy+120);},450);return;}
 }}
function dist(a,b,c,d){var dx=a-c,dy=b-d;return Math.sqrt(dx*dx+dy*dy);}

function iniciar(){patG=cx.createPattern(IMG.grama,"repeat");patM=cx.createPattern(IMG.madeira,"repeat");patP=cx.createPattern(IMG.parede,"repeat");
 var q=(location.search.match(/cena=(\w+)/)||[])[1];if(q==="dentro"){cena="dentro";byte.x=RW/2;byte.y=RH-90;}
 if(/chave=1/.test(location.search)){chave.peg=true;inv.chave=true;}
 ult=null;requestAnimationFrame(frame);}

function sombra(x,y,rx,ry){cx.save();cx.fillStyle="rgba(15,10,25,.32)";cx.shadowColor="rgba(0,0,0,.35)";cx.shadowBlur=9;cx.beginPath();cx.ellipse(x,y,rx,ry,0,0,Math.PI*2);cx.fill();cx.restore();}
function desenhaByte(){var im=IMG.byte,h=90,w=im.width*h/im.height;var bob=byte.mov?Math.abs(Math.sin(byte.passo*.8))*6:0;var rp=byte.mov?0:Math.sin(byte.resp)*.028;
 sombra(byte.x,byte.y,25-bob*.5,8);cx.save();cx.translate(byte.x,byte.y-bob);cx.scale(byte.dir*(1+rp),1-rp*.6);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
function npc(im,x,y,hh,t,pulo){var w=im.width*hh/im.height;var resp=Math.sin(t*0.002+x)*0.02;sombra(x,y,w*0.34,8);
 cx.save();cx.translate(x,y);cx.scale(1,1+resp);cx.drawImage(im,-w/2,-hh,w,hh);cx.restore();}
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
function chaveDes(x,y,t){var bob=Math.sin(t*.004)*4;cx.save();cx.translate(x,y+bob);cx.shadowColor="#ffd24a";cx.shadowBlur=18;
 cx.strokeStyle="#f4c430";cx.lineWidth=5;cx.beginPath();cx.arc(0,-7,7,0,Math.PI*2);cx.stroke();
 cx.beginPath();cx.moveTo(0,0);cx.lineTo(0,17);cx.moveTo(0,17);cx.lineTo(6,17);cx.moveTo(0,12);cx.lineTo(5,12);cx.stroke();cx.restore();cx.shadowBlur=0;}

var ult=null,tpo=0;
function moverByte(dt,limitar){var dx=0,dy=0;
 if(teclas.e)dx=-1;else if(teclas.d)dx=1; if(teclas.c)dy=-1;else if(teclas.b)dy=1;
 if(dx===0&&dy===0&&byte.tx!=null){var ax=byte.tx-byte.x,ay=byte.ty-byte.y,d=Math.sqrt(ax*ax+ay*ay);if(d>6){dx=ax/d;dy=ay/d;}else byte.tx=null;}
 var sp=180,tvx=dx*sp,tvy=dy*sp;byte.vx+=(tvx-byte.vx)*Math.min(1,dt*9);byte.vy+=(tvy-byte.vy)*Math.min(1,dt*9);
 var v=Math.sqrt(byte.vx*byte.vx+byte.vy*byte.vy);byte.mov=v>12;if(byte.vx<-6)byte.dir=-1;else if(byte.vx>6)byte.dir=1;
 var nx=byte.x+byte.vx*dt,ny=byte.y+byte.vy*dt;var r=limitar(nx,ny);byte.x=r[0];byte.y=r[1];
 if(byte.mov){byte.passo+=dt*11;hint=Math.max(0,hint-dt*1.2);tpo-=dt;}byte.resp+=dt*3;
 if(balaoT>0)balaoT-=dt;}

/* ==== FORA ==== */
function limFora(nx,ny){nx=Math.max(30,Math.min(FW-30,nx));ny=Math.max(120,Math.min(FH-24,ny));
 // predio (bloqueia corpo, deixa a porta embaixo)
 if(nx>fx-140&&nx<fx+140&&ny<fy-6&&ny>fy-300){ if(byte.y<=fy-6)ny=byte.y; else ny=fy-6; if(byte.x<=fx-140||byte.x>=fx+140){}else{} nx=byte.x; }
 for(var i=0;i<arvoresF.length;i++){var a=arvoresF[i];if((nx-a[0])*(nx-a[0])+(ny-(a[1]-4))*(ny-(a[1]-4))<22*22){nx=byte.x;ny=byte.y;}}
 return [nx,ny];}
function drawFora(t){
 cx.save();cx.translate(-cam.x,-cam.y);
 cx.fillStyle=patG;cx.fillRect(cam.x,cam.y,VW,VH);
 // ordena por y: arvores, fachada, byte, chave
 var els=[];for(var i=0;i<arvoresF.length;i++)els.push({y:arvoresF[i][1],k:"arv",d:arvoresF[i]});
 els.push({y:fy,k:"fachada"});els.push({y:byte.y,k:"byte"});
 if(!chave.peg)els.push({y:chave.y,k:"chave"});
 els.sort(function(a,b){return a.y-b.y;});
 for(i=0;i<els.length;i++){var e=els[i];
  if(e.k==="arv"){var im=IMG.arvore,h=150,w=im.width*h/im.height;sombra(e.d[0],e.d[1],33,10);var sw=Math.sin(t*.0016+e.d[0])*0.02;cx.save();cx.translate(e.d[0],e.d[1]);cx.rotate(sw);cx.drawImage(im,-w/2,-h,w,h);cx.restore();}
  else if(e.k==="fachada"){var f=IMG.fachada,fh=300,fw=f.width*fh/f.height;sombra(fx,fy+6,fw*0.4,14);cx.drawImage(f,fx-fw/2,fy-fh,fw,fh);
    if(inv.chave){cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(fx,fy-70,4,fx,fy-70,60);g.addColorStop(0,"rgba(120,255,150,.5)");g.addColorStop(1,"rgba(120,255,150,0)");cx.fillStyle=g;cx.fillRect(fx-70,fy-140,140,140);cx.restore();}}
  else if(e.k==="chave")chaveDes(chave.x,chave.y,t);
  else desenhaByte();
 }
 cx.restore();
 // luz de dia (quente suave) + vaga-lumes
 var gg=cx.createLinearGradient(0,0,0,VH);gg.addColorStop(0,"rgba(60,40,95,.10)");gg.addColorStop(1,"rgba(255,160,80,.10)");cx.fillStyle=gg;cx.fillRect(0,0,VW,VH);
 var vg=cx.createRadialGradient(VW/2,VH/2,VH*.4,VW/2,VH/2,VH*.85);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,.42)");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<vagas.length;j++){var va=vagas[j];var vx=va.x-cam.x+Math.sin(t*.001+va.f)*15,vy=va.y-cam.y+Math.cos(t*.0011+va.f)*13;if(vx<0||vx>VW||vy<0||vy>VH)continue;var aa=.3+.4*Math.sin(t*.003+va.f*2);cx.shadowColor="#fff2a0";cx.shadowBlur=8;cx.fillStyle="rgba(255,240,150,"+aa+")";cx.beginPath();cx.arc(vx,vy,2,0,Math.PI*2);cx.fill();}cx.restore();
 // prompt E
 proxE=null;
 if(!chave.peg&&dist(byte.x,byte.y,chave.x,chave.y)<48)proxE="Pegar a chave";
 else if(dist(byte.x,byte.y,fx,fy+18)<70)proxE=inv.chave?"Abrir a porta":"Porta trancada";
}
/* ==== DENTRO ==== */
function limDentro(nx,ny){nx=Math.max(T+18,Math.min(RW-T-18,nx));ny=Math.max(T+18,Math.min(RH-30,ny));
 // saida (gap embaixo) permite passar do limite? mantemos dentro
 if((nx-tab.x)*(nx-tab.x)+(ny-(tab.y+30))*(ny-(tab.y+30))<40*40){nx=byte.x;ny=byte.y;}
 if((nx-gato.x)*(nx-gato.x)+(ny-(gato.y))*(ny-(gato.y))<28*28){nx=byte.x;ny=byte.y;}
 return [nx,ny];}
function drawDentro(t){
 // camera segue dentro da sala
 cx.save();cx.translate(-cam.x,-cam.y);
 // chao
 cx.fillStyle=patM;cx.fillRect(cam.x,cam.y,VW,VH);
 // paredes (borda)
 cx.fillStyle=patP;
 cx.fillRect(0,0,RW,T);cx.fillRect(0,RH-T,RW,T);cx.fillRect(0,0,T,RH);cx.fillRect(RW-T,0,T,RH);
 // saida (tapete) embaixo centro
 cx.fillStyle="rgba(120,80,40,.6)";roundR(RW/2-46,RH-T-4,92,T+2,6);cx.fill();
 cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";cx.fillText("▼ SAÍDA",RW/2,RH-T+18);
 // balcao do taberneiro
 var bg=cx.createLinearGradient(0,tab.y+18,0,tab.y+70);bg.addColorStop(0,"#8a5a30");bg.addColorStop(1,"#5f3d20");cx.fillStyle=bg;roundR(tab.x-120,tab.y+22,240,50,8);cx.fill();
 // elementos por profundidade
 var els=[{y:tab.y,k:"tab"},{y:gato.y,k:"gato"},{y:byte.y,k:"byte"}];els.sort(function(a,b){return a.y-b.y;});
 for(var i=0;i<els.length;i++){if(els[i].k==="tab")npc(IMG.taberneiro,tab.x,tab.y+30,150,t);else if(els[i].k==="gato")npc(IMG.gato,gato.x,gato.y,72,t);else desenhaByte();}
 // lampioes (imagem)
 for(i=0;i<lampioes.length;i++){var lp=lampioes[i],im=IMG.lampiao,h=64,w=im.width*h/im.height;cx.drawImage(im,lp[0]-w/2,lp[1]-h/2,w,h);}
 cx.restore();
 // ==== ESCURIDAO + LUZ DE LAMPIAO ====
 cx.fillStyle="rgba(10,7,20,.72)";cx.fillRect(0,0,VW,VH);
 cx.save();cx.globalCompositeOperation="lighter";
 for(i=0;i<lampioes.length;i++){var lp=lampioes[i],lx=lp[0]-cam.x,ly=lp[1]-cam.y;var fl=0.85+0.15*Math.sin(t*0.02+i);
  var g=cx.createRadialGradient(lx,ly,6,lx,ly,150);g.addColorStop(0,"rgba(255,190,110,"+(0.95*fl)+")");g.addColorStop(.5,"rgba(255,160,80,.35)");g.addColorStop(1,"rgba(255,160,80,0)");cx.fillStyle=g;cx.fillRect(lx-160,ly-160,320,320);}
 // luz suave no byte
 var bx=byte.x-cam.x,by=byte.y-cam.y-30;var gb=cx.createRadialGradient(bx,by,4,bx,by,90);gb.addColorStop(0,"rgba(180,220,255,.25)");gb.addColorStop(1,"rgba(180,220,255,0)");cx.fillStyle=gb;cx.fillRect(bx-90,by-90,180,180);
 cx.restore();
 // poeirinha de luz flutuando
 cx.save();cx.globalCompositeOperation="lighter";for(var j=0;j<14;j++){var mx=((j*137+t*0.02)%RW)-cam.x,my=((j*211+t*0.01)%RH)-cam.y;cx.fillStyle="rgba(255,220,150,"+(0.1+0.1*Math.sin(t*0.002+j))+")";cx.beginPath();cx.arc(mx,my,1.5,0,Math.PI*2);cx.fill();}cx.restore();
 proxE=null;
 if(dist(byte.x,byte.y,tab.x,tab.y+40)<80)proxE="Falar com o taberneiro";
 else if(dist(byte.x,byte.y,gato.x,gato.y+20)<70)proxE="Fazer carinho no gato";
 else if(byte.y>RH-96&&Math.abs(byte.x-RW/2)<70)proxE="Sair da taberna";
}

function frame(ts){if(ult===null)ult=ts;var dt=Math.min(.05,(ts-ult)/1000);ult=ts;var t=ts;
 if(!fadeDir){ if(cena==="fora")moverByte(dt,limFora);else moverByte(dt,limDentro); }
 // camera
 var W=(cena==="fora")?FW:RW,H=(cena==="fora")?FH:RH;
 var ax=Math.max(0,Math.min(byte.x-VW/2,W-VW)),ay=Math.max(0,Math.min(byte.y-VH/2,H-VH));
 cam.x+=(ax-cam.x)*Math.min(1,dt*7);cam.y+=(ay-cam.y)*Math.min(1,dt*7);
 cx.clearRect(0,0,VW,VH);
 if(cena==="fora")drawFora(t);else drawDentro(t);
 // inventario
 cx.fillStyle="rgba(8,16,30,.55)";roundR(10,10,120,40,10);cx.fill();cx.fillStyle="#cfe0ff";cx.font="bold 12px Verdana";cx.textAlign="left";cx.fillText("Mochila:",20,35);
 if(inv.chave){cx.save();cx.translate(104,30);cx.scale(0.9,0.9);chaveDes(0,0,t);cx.restore();}
 // prompt E
 if(proxE){cx.fillStyle="rgba(8,16,30,.8)";var w=cx.measureText(proxE).width*1.0+70;cx.font="bold 13px Verdana";w=cx.measureText(proxE).width+74;roundR((VW-w)/2,VH-42,w,28,8);cx.fill();
  cx.fillStyle="#ffe38a";cx.textAlign="center";cx.fillText("[ E ] "+proxE,VW/2,VH-23);}
 // balao
 if(balaoT>0&&balaoTxt){var ax2,ay2;if(balaoAlvo==="tab"){ax2=tab.x-cam.x;ay2=tab.y-cam.y-160;}else if(balaoAlvo==="gato"){ax2=gato.x-cam.x;ay2=gato.y-cam.y-78;}else{ax2=byte.x-cam.x;ay2=byte.y-cam.y-96;}
  cx.font="bold 14px Verdana";var tw=cx.measureText(balaoTxt).width,bw=Math.min(tw+28,VW-20),bh=34;var lx=Math.max(8,Math.min(VW-bw-8,ax2-bw/2)),ly=Math.max(6,ay2-bh);
  cx.globalAlpha=Math.min(1,balaoT/.6);cx.fillStyle="rgba(255,255,255,.96)";roundR(lx,ly,bw,bh,10);cx.fill();
  cx.beginPath();cx.moveTo(ax2-8,ly+bh);cx.lineTo(ax2+8,ly+bh);cx.lineTo(ax2,ly+bh+11);cx.closePath();cx.fill();
  cx.fillStyle="#17324a";cx.textAlign="center";cx.fillText(balaoTxt,lx+bw/2,ly+bh/2+5);cx.globalAlpha=1;}
 // dica inicial
 if(hint>0&&cena==="fora"){cx.globalAlpha=Math.min(1,hint);cx.fillStyle="rgba(8,16,30,.7)";roundR((VW-300)/2,14,300,26,8);cx.fill();cx.fillStyle="#ffe38a";cx.font="bold 12px Verdana";cx.textAlign="center";cx.fillText("Ache a chave dourada e abra a taberna!",VW/2,31);cx.globalAlpha=1;}
 // fade
 if(fadeDir>0){fade+=dt*2.6;if(fade>=1){fade=1;if(fadeAcao){fadeAcao();fadeAcao=null;}fadeDir=-1;}}
 else if(fadeDir<0){fade-=dt*2.6;if(fade<=0){fade=0;fadeDir=0;}}
 if(fade>0){cx.fillStyle="rgba(0,0,0,"+fade+")";cx.fillRect(0,0,VW,VH);}
 requestAnimationFrame(frame);
}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
</script></body></html>"""
for ph,uri in A.items(): HTML=HTML.replace(ph,uri)
open(os.path.join(S,"byte-taberna.html"),"w",encoding="utf-8").write(HTML)
print("OK -> byte-taberna.html (",round(len(HTML)/1024),"KB )")
