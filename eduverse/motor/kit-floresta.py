# -*- coding: utf-8 -*-
# EducaVerso — "A Floresta do Byte" — ETAPA 1: floresta VIVA (andar livre + pegar a chave)
# O Byte anda pela floresta (D-pad no celular / setas no PC), com camera que segue,
# arvores com colisao, folhas caindo, passaros, vento e luz. Pega a chave dourada e
# chega na entrada do labirinto (gancho da Etapa 2 = empurrar pedras-seta).
import base64, os, json as _json
S=os.path.dirname(os.path.abspath(__file__))
def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
# imagens (algumas opcionais: so entram se existirem)
IMGF={"grama":"grama.png","caminho":"caminho.png","arvore":"arvore.png","byte":"byte.png",
      "chave":"chave.png","flores":"flores.png","muro":"muro.png","passaro":"passarinho.png",
      "borboleta":"borboleta.png",
      # --- sprites de NPCS (opcionais; o loader ja pula os que nao existem) ---
      "gato":"gato.png","coelho":"coelho.png","passarinho":"passarinho.png",
      # --- props pintados do pomar (opcionais; o loader ja pula os que faltam) ---
      "cesta":"cesta.png","sacola10":"sacola10.png"}
# ---- TEMA (peca trocavel): o MESMO motor, mundo diferente ----
TEMA=os.environ.get("TEMA","floresta")
CFG={
 "floresta":{"chao":"grama.png","part":"folha","ceu0":"rgba(255,236,170,.10)","ceu1":"rgba(30,20,60,.12)",
   "passaros":True,"borboletas":True,"titulo":"A Floresta do Byte","emoji":"&#127795;"},
 "inverno":{"chao":"neve.png","part":"neve","ceu0":"rgba(205,228,255,.16)","ceu1":"rgba(40,64,120,.18)",
   "passaros":False,"borboletas":False,"titulo":"A Floresta de Inverno","emoji":"&#10052;"},
}[TEMA]
IMGF["grama"]=CFG["chao"]                       # o chao vira a peca do tema
if not CFG["borboletas"]: IMGF.pop("borboleta",None)
THEMEJS=_json.dumps({"part":CFG["part"],"ceu0":CFG["ceu0"],"ceu1":CFG["ceu1"],
                     "passaros":CFG["passaros"],"borboletas":CFG["borboletas"]})
print("TEMA =",TEMA,"| chao =",CFG["chao"])
SRCJS={}
for k,fn in IMGF.items():
    p=os.path.join(S,fn)
    if os.path.exists(p): SRCJS[k]="data:image/png;base64,"+b64(p)
    else: print("(opcional) sem",fn)
SRC_JSON=_json.dumps(SRCJS)
# falas
FALA_IDS=["s1_intro","s1_chave","s1_labirinto"]
AUD=os.path.join(S,"_audio");FAL={}
for idn in FALA_IDS:
    p=os.path.join(AUD,idn+".mp3")
    if os.path.exists(p): FAL[idn]="data:audio/mpeg;base64,"+b64(p)
    else: print("!! sem audio",idn)
FALAS_JSON=_json.dumps(FAL)

HTML=r"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EducaVerso - __TITULO__</title>
<style>
 html,body{margin:0;min-height:100%;background:#0a1120;color:#eaf2ff;font-family:Verdana,Geneva,sans-serif;text-align:center;overflow-x:hidden;}
 #wrap{min-height:100vh;width:100%;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:8px 0;}
 h1{font-size:15px;margin:4px 0 0;letter-spacing:.3px;width:100%;}
 .sub{font-size:11px;color:#9fb6df;margin:0 auto 4px;width:100%;max-width:94vw;box-sizing:border-box;padding:0 8px;line-height:1.35;}
 #frame{padding:7px;border-radius:14px;background:#060b16;box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 2px #23407a;max-width:96vw;box-sizing:border-box;}
 canvas{display:block;border-radius:10px;background:#3f7a34;max-width:100%;max-height:74vh;width:auto;height:auto;cursor:pointer;}
 #painel{display:flex;width:100%;box-sizing:border-box;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:6px;padding:0 6px;}
 .bt{font-family:inherit;font-weight:bold;border:0;border-radius:14px;cursor:pointer;padding:9px 16px;font-size:15px;color:#0a1120;-webkit-transition:transform .05s;transition:transform .05s;}
 .bt.vz{background:linear-gradient(#ffe08a,#f5b73f);box-shadow:0 3px 0 #b07d1e;}
 .subPC{display:block;} .subTouch{display:none;}
 #dpad{display:none;margin:8px auto 0;grid-template-columns:repeat(3,58px);grid-template-rows:repeat(3,50px);gap:6px;justify-content:center;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;}
 #dpad button{font-family:inherit;font-size:22px;font-weight:bold;border:0;border-radius:13px;color:#12325a;background:-webkit-linear-gradient(#eaf3ff,#b7cbe9);background:linear-gradient(#eaf3ff,#b7cbe9);box-shadow:0 3px 0 #7f93b3;cursor:pointer;-webkit-user-select:none;user-select:none;touch-action:none;}
 #dpad button:active{transform:translateY(2px);box-shadow:0 1px 0 #7f93b3;}
 .dU{grid-column:2;grid-row:1;} .dL{grid-column:1;grid-row:2;} .dR{grid-column:3;grid-row:2;} .dD{grid-column:2;grid-row:3;}
 body.touch .subPC{display:none;} body.touch .subTouch{display:block;} body.touch #dpad{display:grid;}
</style></head><body><div id="wrap">
 <h1>__EMOJI__ __TITULO__</h1>
 <p class="sub subPC">__SUB_PC__</p>
 <p class="sub subTouch">__SUB_TOUCH__</p>
 <div id="frame"><canvas id="tela" width="720" height="500"></canvas></div>
 <div id="dpad">
   <button class="dU" id="dU">&#9650;</button>
   <button class="dL" id="dL">&#9664;</button>
   <button class="dR" id="dR">&#9654;</button>
   <button class="dD" id="dD">&#9660;</button>
 </div>
</div><script>
var cv=document.getElementById("tela");
/* tela estreita (celular em pe): viewport mais ALTA p/ aproveitar a tela (area de jogo maior) */
(function(){try{var w=window.innerWidth||720;if(w<600){cv.height=760;}}catch(e){}})();
var cx=cv.getContext("2d"),VW=cv.width,VH=cv.height;
var SRC=__SRC_JSON__, FALAS=__FALAS_JSON__, TEMA=__THEME_JS__;
var HIST=(typeof MUNDO!=="undefined"&&MUNDO.historia)?MUNDO.historia:{}; // historia data-driven (default {} = floresta identica)
var IMG={},carreg=0,NN=0;for(var kk in SRC)NN++;
for(var k in SRC){(function(key){var im=new Image();im.onload=function(){IMG[key]=im;if(++carreg===NN)iniciar();};im.onerror=function(){if(++carreg===NN)iniciar();};im.src=SRC[key];})(k);}
var IS_TOUCH=(("ontouchstart" in window)||(navigator.maxTouchPoints>0)||(window.matchMedia&&window.matchMedia("(pointer:coarse)").matches)||(location.search.indexOf("dpad=1")>=0));
if(IS_TOUCH){try{document.body.classList.add("touch");}catch(e){}}

/* ---------- MUNDO ---------- */
var WW=1500,WH=1050;
var cam={x:0,y:0};
var byte={x:250,y:860,dir:1,resp:0,passo:0,mov:false,r:18};
byte.mvx=0;byte.mvy=1;byte.idle=0;  // vetor de movimento + tempo parado (poses vivas)
var hasKey=false, fase="andar", fim=false, fimT=0;
var chave={x:560,y:470,got:false,bob:0};
var arco={x:1150,y:340};
// caminho (polilinha) do inicio ate o arco
var PATH=[[250,860],[380,740],[300,600],[510,510],[690,560],[840,470],[1010,450],[1150,400]];
// arvores (base x,y) + raio de colisao no tronco
var TREES=[[120,520],[150,780],[470,880],[640,300],[430,360],[760,700],[560,690],
 [900,540],[1050,760],[1230,520],[1180,900],[330,470],[720,210],[980,180],[1300,300],
 [210,300],[880,860],[1080,420],[640,930],[400,640]];
var TR=16; // raio tronco
// flores decorativas
var FLORES=[[420,800],[300,690],[560,560],[700,470],[860,520],[1000,430],[1120,330],[240,820],[640,640],[900,700]];
var leaves=[],birds=[],pollen=[],estrelas=[],borbs=[];
// PROPS VIVOS (data-driven): fogueira/lareira/lampiao/chamine etc. cada um anima+soa sozinho
var PROPS=(typeof MUNDO!=="undefined"&&MUNDO.props)?MUNDO.props:[];
var fumos=[],faiscas=[],fogoTimer=0.5;
var temFogo=false;for(var _pi=0;_pi<PROPS.length;_pi++){var _tp=PROPS[_pi].tipo;if(_tp==="fogueira"||_tp==="lareira"||_tp==="lampiao")temFogo=true;}
for(var i=0;i<30;i++)pollen.push({x:Math.random()*WW,y:Math.random()*WH,f:i,r:1+Math.random()*1.6});
var luzChao=[];for(var i=0;i<3;i++)luzChao.push({y:120+i*320,ph:i*2.1,sp:14+i*4});

/* ===== ESTADO: subsistemas de mundo-vivo (mundo-vivo v2) ===== */
var balaoAlvo=null; // quem esta falando (obj com x,y no mundo); null=Byte
// --- POEIRINHA AO ANDAR: array + config data-driven (DEFAULT OFF: mundos sem o campo ficam IDENTICOS) ---
var poeira=[];
var POEIRA_ON=(typeof MUNDO!=="undefined"&&MUNDO.poeira)?true:false;                 // ligue com MUNDO.poeira:true
var POEIRA_COR=(typeof MUNDO!=="undefined"&&MUNDO.poeiraCor)?MUNDO.poeiraCor:"rgb(198,180,150)"; // terra clara (transparencia vem do globalAlpha)
// SOMBRA DIRECIONAL: liga por PADRAO (feature pedida); um mundo pode desligar com MUNDO.sombraDir===false
var SOMBRA_DIR=!(typeof MUNDO!=="undefined"&&MUNDO.sombraDir===false);
// estado global da luz, recalculado 1x/frame: dx=lado(xrx), dy=queda(xry), sx=esticao, a=opacidade, col=cor.
// DEFAULT SEGURO = igualzinho a sombra antiga (offset 0, alpha .28, rgba(12,8,20)); se SOMBRA_DIR=false, fica assim.
var luz={dx:0,dy:0,sx:0,a:0.28,col:"rgb(12,8,20)"};
/* ---------- CLIMA (data-driven; DEFAULT ""=nada, floresta identica) ---------- */
var CLIMA=(typeof MUNDO!=="undefined"&&MUNDO.clima)?MUNDO.clima:"";           // ""|"chuva"|"neve"|"tempestade"
var CLIMAF=(typeof MUNDO!=="undefined"&&MUNDO.climaForca)?MUNDO.climaForca:1; // intensidade (1=padrao)
var CLIMA_MOLHA=(typeof MUNDO!=="undefined"&&MUNDO.climaMolha)?true:false;    // brilho de chao molhado (opcional)
var chuvaOn=(CLIMA==="chuva"||CLIMA==="tempestade");
var trovaoOn=(CLIMA==="tempestade");
// pool FIXO de gotas (coord de TELA): cada gota tem posicao/velocidade proprias e recicla no topo (nada alocado por frame)
var gotas=[];if(chuvaOn){for(var _cg=0,_ng=Math.round(80*CLIMAF);_cg<_ng;_cg++)gotas.push({x:Math.random()*VW,y:Math.random()*VH,l:8+Math.random()*10,sp:520+Math.random()*280,s:0,sx:0});}
// pool FIXO de rajadas visiveis (linhas de vento cruzando a tela)
var ventos=[];for(var _cv=0;_cv<8;_cv++)ventos.push({on:false,x:0,y:0,len:0,sp:0,a:0});
// flash + trovao (tempestade)
var flash=0,flashT=3+Math.random()*5,trovaoDelay=-1;
// NUVENS (data-driven): MUNDO.nuvens -> false=off | true=ligado leve (default) | N=numero de sombras.
// DEFAULT LIGADO LEVE e bem discreto (a floresta ganha uma sombra de nuvem sutil).
var _nuvCfg=(typeof MUNDO!=="undefined"&&MUNDO.nuvens!==undefined)?MUNDO.nuvens:true;
var _nQtd=(_nuvCfg===false)?0:(typeof _nuvCfg==="number"?Math.max(2,Math.min(4,Math.round(_nuvCfg))):2); // 2-4 sombras
var _nCeu=(_nuvCfg===false)?0:2; // 2 nuvens claras no ceu (0 desliga; discreto)
var nuvSombra=[],nuvCeu=[];
// monta as nuvens UMA vez, com forma DETERMINISTICA (hash seeded, nao Math.random -> nao pisca nem varia)
(function(){function H(s,k){var v=Math.sin(s*12.9898+k*78.233)*43758.5453;return v-Math.floor(v);}
 for(var i=0;i<_nQtd;i++){var s=(i+1)*97.13,bl=[],nb=2+Math.floor(H(s,1)*2); // 2-3 blobs = manchas grandes
  for(var b=0;b<nb;b++)bl.push({dx:(H(s,b*3+2)-0.5)*170,dy:(H(s,b*3+3)-0.5)*70,r:120+H(s,b*3+4)*120});
  nuvSombra.push({x:H(s,5)*(WW+900),y:130+H(s,6)*(WH-260),w:0.85+H(s,7)*0.55,sp:0.7+H(s,8)*0.6,a:0.055+H(s,9)*0.035,ph:H(s,10)*6.28,bl:bl});}
 for(i=0;i<_nCeu;i++){var s2=(i+1)*53.7,bl2=[],nb2=3+Math.floor(H(s2,1)*2); // 3-4 puffs por nuvem de ceu
  for(var b2=0;b2<nb2;b2++)bl2.push({dx:(b2-nb2/2)*24+(H(s2,b2+2)-0.5)*10,dy:(H(s2,b2+9)-0.5)*8,r:15+H(s2,b2+5)*15});
  nuvCeu.push({x:H(s2,6)*(VW+300),y:18+H(s2,7)*44,s:0.9+H(s2,8)*0.7,sp:0.6+H(s2,9)*0.7,a:0.10+H(s2,10)*0.08,ph:H(s2,11)*6.28,bl:bl2});}})();
// NPCS VIVOS (data-driven): habitantes do mundo. Default [] -> floresta identica.
var npcs=[];(function(){var L=(typeof MUNDO!=="undefined"&&MUNDO.npcs)?MUNDO.npcs:[];
 for(var i=0;i<L.length;i++){var d=L[i];
  npcs.push({sprite:d.sprite,x:d.x,y:d.y,ox:d.x,oy:d.y,
   esc:d.escala||1,vel:d.vel||30,nome:d.nome||"",fala:d.fala||"",falas:d.falas||null,fi:0,
   rota:d.rota||null,ri:0,paus:0,dir:1,mvx:0,passo:0,
   olha:0,acen:0,cd:0});}})();


/* ===== ESTADO: MOTOR DE RODADAS (data-driven; DEFAULT AUSENTE = floresta intacta) ===== */
/* Colocar junto do bloco de estado data-driven (logo após a montagem de `npcs`, ~linha 150). */
var AULA=(typeof MUNDO!=="undefined"&&MUNDO.aula&&MUNDO.aula.rounds&&MUNDO.aula.rounds.length)?MUNDO.aula:null;
var MODO_AULA=!!AULA;                 // false => nada roda; motor chave->arco IDÊNTICO
var OBJETIVO=(HIST.objetivo)?HIST.objetivo:(MODO_AULA?"colher":"chave"); // interruptor da mecanica da chave
var rIdx=-1,rRound=null,rTipo="",rN=0,rAlvo=0,rCesta=null;
var rColhidas=0,rNaCesta=0,rExtra=0,rProx=1,rGrupos=0;   // contadores por tipo
var rItens=[],rFly=[],rBadges=[];     // frutas no mundo / frutas voando p/ cesta / badges de número
var rEstado="rodada",rTransT=0,rDicaT=5;                 // "rodada"|"transicao"; timers
var aulaFim=false,aulaFimT=0,aulaComemora=false;         // aulaComemora => pose "feliz" do Byte

/* ---------- AUDIO (ambiente rico em camadas) ---------- */
var AC=null,ventoG=null,ambMaster=null,som=false,gust=0.5,birdTimer=2.2,coruja=9;
var noite=0; // ciclo dia/noite: 0=dia, 1=noite profunda (computado no loop)
function initAudio(){if(AC)return;try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return;}
 ambMaster=AC.createGain();ambMaster.gain.value=0;ambMaster.connect(AC.destination);
 var n=Math.floor(AC.sampleRate*2),buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);
 for(var i=0;i<n;i++)d[i]=(Math.random()*2-1);
 // 1) vento grave (com rajadas via ventoG)
 var s=AC.createBufferSource();s.buffer=buf;s.loop=true;var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=440;
 ventoG=AC.createGain();ventoG.gain.value=0.05;s.connect(f);f.connect(ventoG);ventoG.connect(ambMaster);s.start();
 // 2) folhas farfalhando (medio, com swell lento)
 var s2=AC.createBufferSource();s2.buffer=buf;s2.loop=true;var f2=AC.createBiquadFilter();f2.type="bandpass";f2.frequency.value=2400;f2.Q.value=0.6;
 var rg=AC.createGain();rg.gain.value=0.016;var rlfo=AC.createOscillator();rlfo.frequency.value=0.12;var rlg=AC.createGain();rlg.gain.value=0.012;rlfo.connect(rlg);rlg.connect(rg.gain);
 s2.connect(f2);f2.connect(rg);rg.connect(ambMaster);s2.start();rlfo.start();
 // 3) grilinhos (agudo, pulsante)
 var s3=AC.createBufferSource();s3.buffer=buf;s3.loop=true;var f3=AC.createBiquadFilter();f3.type="bandpass";f3.frequency.value=5600;f3.Q.value=9;
 var cg=AC.createGain();cg.gain.value=0.003;var clfo=AC.createOscillator();clfo.type="triangle";clfo.frequency.value=6.5;var clg=AC.createGain();clg.gain.value=0.006;clfo.connect(clg);clg.connect(cg.gain);
 s3.connect(f3);f3.connect(cg);cg.connect(ambMaster);s3.start();clfo.start();
 // 4) FOGO crepitando (so quando ha fogueira/lareira/lampiao): ruido grave com tremular irregular
 if(temFogo){var s4=AC.createBufferSource();s4.buffer=buf;s4.loop=true;var f4=AC.createBiquadFilter();f4.type="lowpass";f4.frequency.value=820;
  var fgn=AC.createGain();fgn.gain.value=0.02;var flfo=AC.createOscillator();flfo.type="triangle";flfo.frequency.value=7.3;var flg=AC.createGain();flg.gain.value=0.018;flfo.connect(flg);flg.connect(fgn.gain);
  s4.connect(f4);f4.connect(fgn);fgn.connect(ambMaster);s4.start();flfo.start();}}
function somEstalo(){if(!AC||!som||!temFogo)return;bip(180+Math.random()*260,.045,"square",.02,0);} // estalo do fogo
function bip(fr,dur,tp,vol,del){if(!AC||!som)return;var o=AC.createOscillator(),g=AC.createGain();o.type=tp||"sine";o.frequency.value=fr;
 var t=AC.currentTime+(del||0);g.gain.setValueAtTime(vol||.14,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+dur);}
function somPasso(){bip(150,.05,"square",.03);}
function somChave(){bip(880,.09,"sine",.15,0);bip(1175,.09,"sine",.15,.1);bip(1568,.16,"sine",.15,.2);}
function somPio(){var b=1200+Math.floor((byte.passo*7)%5)*120;bip(b,.07,"sine",.09,0);bip(b*1.35,.08,"sine",.09,.08);bip(b*1.15,.09,"sine",.08,.17);}
function somVitoria(){bip(523,.13,"sine",.14,0);bip(659,.13,"sine",.14,.13);bip(784,.13,"sine",.14,.26);bip(1047,.24,"sine",.14,.39);}
// canto de passaro: sequencia melodica curta e variada
var CANTO=[[0,4,7,12,7],[0,7,5,9],[0,3,7,10,7,3],[0,5,9,14]];
function somCanto(){if(!AC||!som)return;var base=1650+Math.floor(Math.random()*6)*120;var seq=CANTO[Math.floor((birdTimer*7)%CANTO.length)];
 for(var i=0;i<seq.length;i++){var fr=base*Math.pow(2,seq[i]/12);bip(fr,.085,"sine",.055,i*0.10);bip(fr*2,.06,"sine",.02,i*0.10);}}
function somCoruja(){if(!AC||!som)return;bip(360,.5,"sine",.05,0);bip(300,.6,"sine",.05,.55);}

/* ---------- VOZ (com FILA: nao corta) ---------- */
function vozPt(){var vs=(window.speechSynthesis?speechSynthesis.getVoices():[])||[],b=null;for(var i=0;i<vs.length;i++){var l=(vs[i].lang||"").toLowerCase().replace("_","-");if(l.indexOf("pt-br")===0)return vs[i];if(l.indexOf("pt")===0&&!b)b=vs[i];}return b;}
function falarTTS(t,pitch){if(!som||!window.speechSynthesis)return;var u=new SpeechSynthesisUtterance(t);u.lang="pt-BR";u.rate=.97;u.pitch=pitch||1.12;var v=vozPt();if(v)u.voice=v;try{speechSynthesis.speak(u);}catch(e){}}
var curAudio=null,fila=null,tocando=false;
function _play(id,texto,pitch){tocando=true;try{if(window.speechSynthesis)speechSynthesis.cancel();}catch(e){}
 try{curAudio=new Audio(FALAS[id]);
   curAudio.onended=curAudio.onerror=function(){tocando=false;curAudio=null;var f=fila;fila=null;if(f)playFala(f.id,f.t,f.p);};
   var pr=curAudio.play();if(pr&&pr.catch)pr.catch(function(){tocando=false;falarTTS(texto,pitch);});}catch(e){tocando=false;falarTTS(texto,pitch);}}
// nao interrompe a fala em andamento: a proxima ESPERA na fila
function playFala(id,texto,pitch){if(!som)return;
 if(id&&FALAS[id]){ if(tocando){fila={id:id,t:texto,p:pitch};return;} _play(id,texto,pitch); }
 else { if(!tocando)falarTTS(texto,pitch); else fila={id:null,t:texto,p:pitch}; } }
function pararVoz(){try{if(curAudio){curAudio.onended=null;curAudio.pause();}}catch(e){}curAudio=null;tocando=false;fila=null;try{if(window.speechSynthesis)speechSynthesis.cancel();}catch(e){}}
/* ---------- CAIXA DE DIALOGO RPG (placa de nome + typewriter + setinha) ---------- */
var balaoT=0;                 // >0 = caixa aberta (tambem liga a pose "fala")
var balaoNome="Byte",balaoFull="",balaoN=0,balaoFimTxt=false,balaoBlink=0,balaoAppear=0;
var balaoCPS=(typeof MUNDO!=="undefined"&&MUNDO.dialogo&&MUNDO.dialogo.cps)?MUNDO.dialogo.cps:34; // letras/s (default seguro)
// balaoNPC: quem chama diz o NOME de quem fala; a fila de voz (playFala) NAO muda -> audio toca junto
function balaoNPC(nome,t,id,pitch,alvo){balaoNome=nome||"Byte";balaoFull=t||"";balaoN=0;balaoFimTxt=(balaoFull.length===0);balaoBlink=0;balaoAppear=0;balaoT=1;balaoAlvo=alvo||null;playFala(id,t,pitch);}
// assinatura ANTIGA intacta: quem ja chamava balao() nao muda -> nome vira "Byte"
function balao(t,id,pitch){balaoNPC("Byte",t,id,pitch);}
function balaoFecha(){balaoT=0;balaoFull="";balaoFimTxt=false;balaoAlvo=null;}
function unlock(){initAudio();if(!window._u&&window.speechSynthesis){window._u=1;try{speechSynthesis.speak(new SpeechSynthesisUtterance(" "));}catch(e){}}}
function toggleSom(){unlock();som=!som;if(ambMaster)ambMaster.gain.value=som?0.85:0;
 if(som){if(MODO_AULA){rodadaFala(true);}else if(!hasKey)balao((HIST.intro&&HIST.intro.txt)||"Vamos passear pela floresta! Use as setas para o Byte andar e pegar a chave dourada.",(HIST.intro&&HIST.intro.id)||"s1_intro");}
 else{pararVoz();}}
cv.addEventListener("mousedown",function(e){cliqueCv(e.clientX,e.clientY);});
cv.addEventListener("touchstart",function(e){if(e.touches[0]){cliqueCv(e.touches[0].clientX,e.touches[0].clientY);}},{passive:false});
function cliqueCv(cxp,cyp){var r=cv.getBoundingClientRect();var mx=(cxp-r.left)*(VW/r.width),my=(cyp-r.top)*(VH/r.height);
 if(mx>VW-46&&my<30){toggleSom();return;}                 // botao de som (canto sup. dir) tem prioridade
 if(balaoT>0&&balaoFull){                                 // caixa aberta: o toque avanca a fala
  if(!balaoFimTxt){balaoN=balaoFull.length;balaoFimTxt=true;} // 1o toque: completa o texto na hora
  else{balaoFecha();}                                     // 2o toque (texto ja completo): fecha
  return;}
}
function desBotaoSom(){var bx=VW-26,by=13;cx.save();cx.fillStyle="rgba(255,255,255,.9)";cx.beginPath();cx.arc(bx,by,12,0,Math.PI*2);cx.fill();cx.fillStyle="#17324a";cx.beginPath();cx.moveTo(bx-6,by-3);cx.lineTo(bx-2,by-3);cx.lineTo(bx+2,by-7);cx.lineTo(bx+2,by+7);cx.lineTo(bx-2,by+3);cx.lineTo(bx-6,by+3);cx.closePath();cx.fill();if(som){cx.strokeStyle="#17324a";cx.lineWidth=1.6;cx.beginPath();cx.arc(bx+2,by,4,-0.7,0.7);cx.stroke();cx.beginPath();cx.arc(bx+2,by,7,-0.7,0.7);cx.stroke();}else{cx.strokeStyle="#c0392b";cx.lineWidth=2;cx.beginPath();cx.moveTo(bx+4,by-4);cx.lineTo(bx+9,by+4);cx.moveTo(bx+9,by-4);cx.lineTo(bx+4,by+4);cx.stroke();}cx.restore();}

/* ---------- ENTRADA (teclado + D-pad segurar) ---------- */
var keys={},dp={U:false,D:false,L:false,R:false};
window.addEventListener("keydown",function(e){var k=e.key;keys[k]=true;if(k.indexOf("Arrow")===0){e.preventDefault();unlock();}});
window.addEventListener("keyup",function(e){keys[e.key]=false;});
function bindDpad(id,prop){var el=document.getElementById(id);if(!el)return;
 function on(e){dp[prop]=true;unlock();if(e.cancelable)e.preventDefault();}
 function off(e){dp[prop]=false;if(e&&e.cancelable)e.preventDefault();}
 el.addEventListener("touchstart",on,{passive:false});el.addEventListener("touchend",off,{passive:false});el.addEventListener("touchcancel",off,{passive:false});
 el.addEventListener("mousedown",on);el.addEventListener("mouseup",off);el.addEventListener("mouseleave",off);}
bindDpad("dU","U");bindDpad("dD","D");bindDpad("dL","L");bindDpad("dR","R");
function inputVec(){var vx=0,vy=0;
 if(keys["ArrowLeft"]||keys["a"]||keys["A"]||dp.L)vx-=1;
 if(keys["ArrowRight"]||keys["d"]||keys["D"]||dp.R)vx+=1;
 if(keys["ArrowUp"]||keys["w"]||keys["W"]||dp.U)vy-=1;
 if(keys["ArrowDown"]||keys["s"]||keys["S"]||dp.D)vy+=1;
 return [vx,vy];}

/* ---------- COLISAO ---------- */
function bloqueado(nx,ny){
 if(nx<24||ny<40||nx>WW-24||ny>WH-24)return true;
 for(var i=0;i<TREES.length;i++){var dx=nx-TREES[i][0],dy=ny-(TREES[i][1]-6);if(dx*dx+dy*dy<(TR+byte.r)*(TR+byte.r))return true;}
 for(var j=0;j<PROPS.length;j++){var pr=PROPS[j];if(pr.r){var px=nx-pr.x,py=ny-pr.y;if(px*px+py*py<(pr.r+byte.r)*(pr.r+byte.r))return true;}}
 return false;}

/* ---------- INICIO ---------- */
function iniciar(){patG=IMG.grama?cx.createPattern(IMG.grama,"repeat"):null;
 patC=IMG.caminho?cx.createPattern(IMG.caminho,"repeat"):null;
 var p=cellCam();cam.x=p[0];cam.y=p[1];
 if(IMG.borboleta)for(var i=0;i<3;i++)borbs.push({x:FLORES[i*3][0]+40,y:FLORES[i*3][1]-30,ang:Math.random()*6.28,ph:Math.random()*6.28,t:Math.random()*6.28});
 if(MODO_AULA){aulaInit();}else{balao((HIST.intro&&HIST.intro.txt)||"Vamos passear pela floresta! Use as setas para o Byte andar e pegar a chave dourada.",(HIST.intro&&HIST.intro.id)||"s1_intro");}
 requestAnimationFrame(frame);}
var patG=null,patC=null;
function cellCam(){return [Math.max(0,Math.min(WW-VW,byte.x-VW/2)), Math.max(0,Math.min(WH-VH,byte.y-VH/2))];}

/* ---------- DESENHO ---------- */
// SOMBRA DIRECIONAL (compartilhada): MESMA assinatura p/ nao quebrar as ~10 chamadas.
// Usa o estado global "luz" (lado/comprimento/opacidade/cor) calculado 1x por frame no UPDATE.
// E chamada DENTRO do translate da camera (coords de mundo). Sutil, nunca preta demais.
function sombra(x,y,rx,ry){var ex=x+luz.dx*rx,ey=y+luz.dy*ry;   // desloca p/ o lado oposto a luz
 var RX=rx*(1+luz.sx),RY=ry*(1+luz.sx*0.14);                    // estica no comprimento (sol baixo=longa)
 cx.save();cx.globalAlpha=luz.a;cx.fillStyle=luz.col;
 cx.beginPath();cx.ellipse(ex,ey,RX,RY,0,0,Math.PI*2);cx.fill();
 cx.restore();cx.globalAlpha=1;}                                // SEMPRE restaura globalAlpha
function estrela(x,y,r,a){cx.save();cx.globalAlpha=Math.max(0,a);cx.fillStyle="#ffd24a";cx.shadowColor="#ffd24a";cx.shadowBlur=10;cx.beginPath();
 for(var i=0;i<5;i++){var an=-Math.PI/2+i*2*Math.PI/5;cx.lineTo(x+Math.cos(an)*r,y+Math.sin(an)*r);var a2=an+Math.PI/5;cx.lineTo(x+Math.cos(a2)*r*.45,y+Math.sin(a2)*r*.45);}
 cx.closePath();cx.fill();cx.restore();cx.shadowBlur=0;}
function imgH(im,x,yBase,h){var w=im.width*h/im.height;cx.drawImage(im,x-w/2,yBase-h,w,h);}
function desCaminho(t){ // trilha de terra gasta que FUNDE na grama (borda dissolvida + tufos de grama)
 cx.save();cx.lineJoin="round";cx.lineCap="round";var col=patC||"rgba(150,112,72,1)";
 function traca(w,a){cx.globalAlpha=a;cx.strokeStyle=col;cx.lineWidth=w;cx.beginPath();cx.moveTo(PATH[0][0],PATH[0][1]);
  for(var i=1;i<PATH.length;i++)cx.lineTo(PATH[i][0],PATH[i][1]);cx.stroke();}
 // rampa suave: de quase-invisivel (fora) a cheio (dentro) => a borda se dissolve na grama
 traca(100,0.07);traca(92,0.13);traca(84,0.22);traca(76,0.34);traca(68,0.5);traca(60,0.72);traca(52,0.92);traca(46,1.0);
 cx.restore();cx.globalAlpha=1;
 // TUFOS de grama (patG, casa perfeito) invadindo a borda -> quebra o contorno, funde na paisagem
 if(patG){for(var i=0;i<PATH.length-1;i++){var ax=PATH[i][0],ay=PATH[i][1],bx=PATH[i+1][0],by=PATH[i+1][1];
  var dx=bx-ax,dy=by-ay,L=Math.sqrt(dx*dx+dy*dy)||1,nx=-dy/L,ny=dx/L;
  for(var s=0;s<L;s+=20){var px=ax+dx*(s/L),py=ay+dy*(s/L);
   var h=Math.sin(px*12.9898+py*78.233)*43758.5453;h-=Math.floor(h); // ruido deterministico (nao pisca)
   var side=h<0.5?-1:1,off=17+h*12,sw=Math.sin(t*0.004+px)*(0.6+gust*1.4);
   cx.save();cx.globalAlpha=0.82;cx.fillStyle=patG;
   cx.beginPath();cx.ellipse(px+nx*side*off+sw,py+ny*side*off,7+h*5,4.5+h*3,0,0,Math.PI*2);cx.fill();cx.restore();
   // 2o tufo do outro lado, mais para dentro (mescla os dois lados)
   var off2=9+h*8;cx.save();cx.globalAlpha=0.5;cx.fillStyle=patG;
   cx.beginPath();cx.ellipse(px-nx*side*off2+sw,py-ny*side*off2,5+h*3,3.5+h*2,0,0,Math.PI*2);cx.fill();cx.restore();}}}
 cx.globalAlpha=1;}
function desArvore(o,t){var x=o[0],y=o[1];sombra(x,y+2,26,8);var sw=Math.sin(t*.0016+x*.05)*(0.016+gust*0.03);
 cx.save();cx.translate(x,y);cx.rotate(sw);imgH(IMG.arvore,0,0,120);cx.restore();}
function desFlor(o,t){if(!IMG.flores)return;var x=o[0],y=o[1];var sw=Math.sin(t*.003+x)*(0.03+gust*0.06);
 cx.save();cx.translate(x,y);cx.rotate(sw);imgH(IMG.flores,0,0,34);cx.restore();}
function desChave(t){if(chave.got)return;var x=chave.x,y=chave.y-8-Math.sin(t*.004)*5;
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(x,y,2,x,y,34);
 g.addColorStop(0,"rgba(255,225,120,"+(0.5+0.2*Math.sin(t*.006))+")");g.addColorStop(1,"rgba(255,225,120,0)");
 cx.fillStyle=g;cx.beginPath();cx.arc(x,y,34,0,Math.PI*2);cx.fill();cx.restore();
 sombra(chave.x,chave.y+8,14,5);imgH(IMG.chave,x,y+18,40);}
// "Zzz" do sono subindo da boca (3 letras que sobem, crescem e somem em loop)
function desZzz(t,mx,my){cx.save();cx.textAlign="left";cx.lineJoin="round";
 cx.fillStyle="rgba(255,255,255,.95)";cx.strokeStyle="rgba(60,90,130,.75)";cx.lineWidth=2;
 for(var i=0;i<3;i++){var ph=((t*0.00045)+i*0.34)%1;var zx=mx+ph*20+i*3;var zy=my-ph*42;var sz=Math.round(10+i*3+ph*7);
  cx.globalAlpha=Math.max(0,0.95*(1-ph*0.85));cx.font="bold "+sz+"px Verdana";
  cx.strokeText("Z",zx,zy);cx.fillText("Z",zx,zy);}
 cx.restore();cx.globalAlpha=1;}
// CARTELA DE POSES (Byte vivo): cada pose tem escala propria p/ o personagem NAO mudar de tamanho
var POSE={frente:{im:"byte",f:1.00},costas:{im:"byte_costas",f:1.00},lado:{im:"byte_lado",f:1.12},
 frente_anda:{im:"byte_frente_anda",f:1.14},costas_anda:{im:"byte_costas_anda",f:1.19}, // f calibrado p/ a CABECA ficar do mesmo tamanho do frame parado (pernas em passo alongam o sprite)
 senta:{im:"byte_senta",f:0.95},deita:{im:"byte_deita",f:0.62},fala:{im:"byte_fala",f:0.98},feliz:{im:"byte_feliz",f:1.06}};
function poseByte(){ // decide a pose atual pela acao (prioridade: comemora>anda>fala>descanso>parado)
 if(fim||aulaComemora) return "feliz";
 if(byte.mov){var ax=Math.abs(byte.mvx),ay=Math.abs(byte.mvy);
  if(ay>ax){var pas=(Math.floor(byte.passo/1.2)%2===0); // caminhada: alterna frame parado<->passo, em sincronia com somPasso (1 troca por passo sonoro)
   if(byte.mvy<0) return pas?"costas":"costas_anda";    // sobe=costas
   return pas?"frente":"frente_anda";}                  // desce=frente
  return "lado";}                                   // esquerda/direita
 if(balaoT>0&&!balaoFimTxt&&!balaoAlvo) return "fala";
 if(byte.idle>13) return "deita";
 if(byte.idle>6)  return "senta";
 return "frente";}
function desByte(t){var x=byte.x,y=byte.y;
 var nome=poseByte(),P=POSE[nome]||POSE.frente;
 if(!IMG[P.im]){nome=(nome==="frente_anda")?"frente":(nome==="costas_anda")?"costas":nome; // sem frame de passo -> pose estatica da mesma direcao
  P=POSE[nome]||POSE.frente;
  if(!IMG[P.im]){P=POSE.frente;nome=(nome==="costas"||nome==="lado")?nome:"frente";}} // sem sprite da pose -> usa frente
 var im=IMG[P.im]||IMG.byte,h=64*P.f;
 var vert=byte.mov&&(nome==="frente"||nome==="costas"||nome==="frente_anda"||nome==="costas_anda");
 var andando=vert||(byte.mov&&nome==="lado");
 var bob=andando?Math.abs(Math.sin(byte.passo*.9))*6:0;
 var temPasso=(nome==="costas"||nome==="costas_anda")?!!IMG[POSE.costas_anda.im]:!!IMG[POSE.frente_anda.im];
 if(vert&&temPasso)bob*=0.5; // frente/costas com 2 frames: o passo visual vem do sprite, bob so leve
 var deitado=(nome==="deita");
 var rp=(!byte.mov&&!deitado&&nome!=="senta")?Math.sin(byte.resp)*.03:0; // respira parado em pe
 var talk=(nome==="fala")?(0.5+0.5*Math.sin(t*0.02))*0.05:0;             // boca/squash ao falar
 var flip=byte.dir;
 var ron=deitado?Math.sin(t*0.0026):0;               // respiracao lenta do sono (roncar)
 var sx=deitado?(1+ron*0.035):(1+rp);                // infla/desincha o corpo
 var sy=deitado?(1+ron*0.02):((1-rp*.6)*(1-talk));
 var rot=deitado?ron*0.02:((!byte.mov&&nome!=="senta")?sway(t,0,0.014):0);                          // leve balanco de roncar
 sombra(x,y+8,deitado?(32+ron*2):18,deitado?7:6);
 cx.save();cx.translate(x,y+8-bob);cx.rotate(rot);cx.scale(flip*sx,sy);imgH(im,0,0,h);cx.restore();
 if(deitado)desZzz(t,x-h*0.30,y+8-h*0.75);           // Zzz saindo da boca (acima da carinha)
 if(hasKey&&IMG.chave){var kw=IMG.chave.width*18/IMG.chave.height;cx.drawImage(IMG.chave,x+11,y-52,kw,18);}}
function desArco(t){var x=arco.x,y=arco.y; // arco de pedra = destino final (so existe se OBJETIVO=="chave")
 sombra(x,y+8,120,20);
 function bloco(bx,by,bw,bh){cx.fillStyle=patM||"#6a6a72";cx.fillRect(bx,by,bw,bh);
  cx.fillStyle="rgba(255,244,225,.10)";cx.fillRect(bx,by,bw,3);cx.strokeStyle="rgba(10,7,16,.5)";cx.lineWidth=2;cx.strokeRect(bx+1,by+1,bw-2,bh-2);}
 // abertura escura (tunel de passagem)
 cx.fillStyle="#0b0f18";cx.fillRect(x-50,y-104,100,104);
 var gg=cx.createLinearGradient(0,y-104,0,y);gg.addColorStop(0,"rgba(18,26,44,.25)");gg.addColorStop(1,"rgba(0,0,0,.78)");cx.fillStyle=gg;cx.fillRect(x-50,y-104,100,104);
 // pedras do fundo (dentro, sugerindo profundidade)
 cx.save();cx.globalAlpha=.5;cx.fillStyle=patM||"#555";cx.fillRect(x-50,y-44,44,44);cx.fillRect(x+8,y-72,42,72);cx.restore();
 // pilares + verga
 bloco(x-84,y-116,34,116); bloco(x+50,y-116,34,116); bloco(x-84,y-142,168,30);
 // ameias em cima
 for(var i=0;i<4;i++)bloco(x-84+i*46,y-158,30,20);
 cx.save();cx.globalCompositeOperation="lighter";var pg=cx.createRadialGradient(x,y-58,6,x,y-58,66);
 pg.addColorStop(0,"rgba(120,180,255,"+(0.12+0.07*Math.sin(t*.004))+")");pg.addColorStop(1,"rgba(120,180,255,0)");cx.fillStyle=pg;cx.fillRect(x-74,y-116,148,116);cx.restore();}
var patM=null;
/* ---------- PROPS VIVOS (fogo/fumaca reutilizaveis) ---------- */
function emiteFumaca(x,y,forca){if(fumos.length>80)return;fumos.push({x:x+(Math.random()-.5)*8,y:y,vy:-(16+Math.random()*12),vx:(Math.random()-.5)*7,r:6+Math.random()*5,a:0.62*forca,gro:9+Math.random()*10});}
function lingua(fx,base,hh,w,cor){cx.fillStyle=cor;cx.beginPath();cx.moveTo(fx-w,base);
 cx.quadraticCurveTo(fx-w*0.7,base-hh*0.55,fx,base-hh);cx.quadraticCurveTo(fx+w*0.7,base-hh*0.55,fx+w,base);
 cx.quadraticCurveTo(fx,base+2,fx-w,base);cx.closePath();cx.fill();}
function desFogueira(p,t){var x=p.x,y=p.y;
 var fl=0.78+0.14*Math.sin(t*0.022)+0.09*Math.sin(t*0.058)+0.05*Math.sin(t*0.15); // tremular
 sombra(x,y+6,30,9);
 // luz quente no chao/ar (oscilante, forte)
 var gm=1+noite*1.9,gr=104*fl*(1+noite*0.45);
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(x,y-16,6,x,y-16,gr);
 g.addColorStop(0,"rgba(255,196,100,"+Math.min(0.95,0.52*fl*gm)+")");g.addColorStop(.42,"rgba(255,132,46,"+Math.min(0.6,0.15*fl*gm)+")");g.addColorStop(1,"rgba(255,120,40,0)");
 cx.fillStyle=g;cx.beginPath();cx.arc(x,y-16,gr,0,Math.PI*2);cx.fill();cx.restore();
 // lenha (toras cruzadas, com topo iluminado)
 cx.save();cx.lineCap="round";
 cx.strokeStyle="#5a3a22";cx.lineWidth=10;cx.beginPath();cx.moveTo(x-24,y+5);cx.lineTo(x+24,y-5);cx.moveTo(x-24,y-5);cx.lineTo(x+24,y+5);cx.stroke();
 cx.strokeStyle="rgba(255,150,60,.5)";cx.lineWidth=3;cx.beginPath();cx.moveTo(x-22,y+2);cx.lineTo(x+22,y-2);cx.stroke();cx.restore();
 // CHAMAS: camadas laranja(alta) -> amarelo(media) -> nucleo branco-quente(baixo)
 cx.save();cx.globalCompositeOperation="lighter";
 for(var i=0;i<6;i++){var ph=t*0.022+i*1.05;var sw=Math.sin(ph)*5;var fx=x-16+i*6.4+sw;var f2=0.7+0.3*Math.sin(ph*1.4);
  lingua(fx,y+1,(30+Math.sin(ph*1.3)*10)*fl*f2,6.5,"rgba(255,120,36,0.72)");}   // laranja alta
 for(i=0;i<5;i++){var ph2=t*0.028+i*1.2;var sw2=Math.sin(ph2)*4;var fx2=x-12+i*6+sw2;
  lingua(fx2,y+1,(20+Math.sin(ph2*1.5)*7)*fl,5,"rgba(255,196,70,0.8)");}         // amarelo media
 for(i=0;i<3;i++){var ph3=t*0.04+i*1.5;var fx3=x-6+i*6+Math.sin(ph3)*3;
  lingua(fx3,y,(11+Math.sin(ph3*1.7)*4)*fl,3.6,"rgba(255,248,215,0.92)");}       // nucleo branco-quente
 cx.restore();}
function desLampiao(p,t){var x=p.x,y=p.y,H=p.h||62;var lx=x,ly=y-H; // ly = centro da lanterna
 var fl=0.8+0.12*Math.sin(t*0.03)+0.08*Math.sin(t*0.071); // tremular da chama
 sombra(x,y+3,10,4);
 // halo de luz quente oscilante
 var gm=1+noite*2.1,gr=62*fl*(1+noite*0.55);
 cx.save();cx.globalCompositeOperation="lighter";var g=cx.createRadialGradient(lx,ly,3,lx,ly,gr);
 g.addColorStop(0,"rgba(255,205,110,"+Math.min(0.92,0.42*fl*gm)+")");g.addColorStop(.5,"rgba(255,150,60,"+Math.min(0.5,0.12*fl*gm)+")");g.addColorStop(1,"rgba(255,150,60,0)");
 cx.fillStyle=g;cx.beginPath();cx.arc(lx,ly,gr,0,Math.PI*2);cx.fill();cx.restore();
 // poste + gancho
 cx.save();cx.strokeStyle="#3a2f26";cx.lineCap="round";cx.lineWidth=5;cx.beginPath();cx.moveTo(x,y);cx.lineTo(x,ly+9);cx.stroke();
 cx.lineWidth=3;cx.beginPath();cx.moveTo(x,ly-2);cx.lineTo(x,ly-9);cx.stroke();cx.restore();
 // lanterna (metal + vidro)
 cx.save();cx.fillStyle="#2b2420";
 cx.beginPath();cx.moveTo(lx-10,ly-5);cx.lineTo(lx+10,ly-5);cx.lineTo(lx+7,ly-10);cx.lineTo(lx-7,ly-10);cx.closePath();cx.fill(); // teto
 cx.fillStyle="rgba(70,45,22,.85)";cx.fillRect(lx-8,ly-5,16,17);                                                   // vidro
 cx.strokeStyle="#2b2420";cx.lineWidth=2.5;cx.strokeRect(lx-8,ly-5,16,17);
 cx.fillStyle="#2b2420";cx.fillRect(lx-9,ly+11,18,3);cx.restore();                                                 // base
 // chama dentro do vidro
 cx.save();cx.globalCompositeOperation="lighter";
 lingua(lx,ly+9,(11+Math.sin(t*0.03)*3)*fl,3.2,"rgba(255,150,50,0.8)");
 lingua(lx,ly+8,(7+Math.sin(t*0.05)*2)*fl,2,"rgba(255,238,190,0.95)");cx.restore();}
function desProp(p,t){if(p.tipo==="fogueira")desFogueira(p,t);
 else if(p.tipo==="lampiao")desLampiao(p,t);
 else if(p.tipo==="cabana"&&IMG.cabana){sombra(p.x,p.y+4,44,11);imgH(IMG.cabana,p.x,p.y,p.h||110);}}

/* ===== FUNCOES: MOTOR DE RODADAS (aula) ===== */
/* =====================================================================
   MOTOR DE RODADAS DE COLHEITA — EducaVerso "A Floresta do Byte"
   Reusa: byte, sombra(), balaoNPC/balao, playFala/FALAS, draws[], bloqueado,
   estrelas, bip/somVitoria, roundR. Sempre restaura globalAlpha.
   Ruído determinístico: LCG semeado por rodada (posições/wobble não piscam).
   ES5 puro. DEFAULT: sem MUNDO.aula => MODO_AULA=false => nada aqui roda.
   ===================================================================== */
var PAL=["zero","um","dois","três","quatro","cinco","seis","sete","oito","nove","dez",
 "onze","doze","treze","catorze","quinze","dezesseis","dezessete","dezoito","dezenove","vinte",
 "vinte e um","vinte e dois","vinte e três","vinte e quatro","vinte e cinco","vinte e seis",
 "vinte e sete","vinte e oito","vinte e nove","trinta"];
function palN(k){return (k>=0&&k<=30)?PAL[k]:(""+k);}
/* PRNG determinístico (LCG). Semeado por rodada => mesmo mundo toda vez, sem piscar. */
function _rng(seed){var s=(seed|0)||1;return function(){s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};}
var _CORF=["#e23b3b","#e07a1f","#8e44ad","#c0399b","#2e8b57","#d4a017","#3b7fe2","#e0526b"];
function _corFruta(i,it){return (it&&it.cor)?it.cor:_CORF[i%_CORF.length];}
function _pertoArvore(x,y){var i,dx,dy;
 for(i=0;i<TREES.length;i++){dx=x-TREES[i][0];dy=y-TREES[i][1];if(dx*dx+dy*dy<70*70)return true;}
 for(i=0;i<PROPS.length;i++){dx=x-PROPS[i].x;dy=y-PROPS[i].y;if(dx*dx+dy*dy<70*70)return true;}
 return false;}
/* gera itens quando a rodada não traz `itens`: ANCORA nas árvores perto da cesta.
   ~70% PENDURADAS na copa (sy=base da árvore -> desenha na frente da folhagem e a
   coleta mede pela base do tronco) e ~30% CAÍDAS no pé (chao -> leva sombra).
   Nenhum item a mais de ~120px de uma árvore. Determinístico (LCG por rodada). */
function _geraItens(R,idx){
 var rnd=_rng((idx+1)*7919),out=[],alvo=R.alvo||0,n=R.n||0,i,qtd,bundles=0,loose=0;
 if(R.tipo==="agrupar"){bundles=Math.floor(n/10);loose=n%10;qtd=bundles+loose;}
 else if(R.tipo==="trazer_exato"){qtd=R.n||(alvo+2);}   // sempre > alvo -> "demais" é possível
 else{qtd=n;}
 // árvores ordenadas pela proximidade da cesta da rodada (colher perto -> caminho curto)
 var cbx=(R.cesta?R.cesta.x:byte.x), cby=(R.cesta?R.cesta.y:byte.y);
 var trs=[];for(i=0;i<TREES.length;i++){var ddx=TREES[i][0]-cbx,ddy=TREES[i][1]-cby;trs.push({x:TREES[i][0],y:TREES[i][1],d:ddx*ddx+ddy*ddy});}
 trs.sort(function(a,b){return a.d-b.d;});
 var nTree=Math.max(2,Math.min(trs.length,Math.ceil(qtd/2)+1)); // usa um punhado das árvores mais perto
 var used=[];for(i=0;i<nTree;i++)used.push(0);                    // frutas já penduradas por árvore
 var offs=[-24,4,24,-12,16];                                     // offsets de copa (|ox|<=26, dentro da copa real)
 for(i=0;i<qtd;i++){var T=trs[i%nTree],tx=T.x,ty=T.y;
  var vale=1,nn=i+1,chao,x,y,sy,pendurada;
  if(R.tipo==="agrupar"&&i<bundles){ vale=10;nn=10;pendurada=false; } // sacola-de-10 no PÉ da árvore
  else if(R.tipo==="agrupar"){ vale=1;nn=1;pendurada=(rnd()<0.7); }
  else{ pendurada=(rnd()<0.7); }
  if(pendurada){ var ox=offs[used[i%nTree]%offs.length];used[i%nTree]++;
   x=tx+ox; y=ty-72-Math.floor(rnd()*26); sy=ty+2; chao=false; }        // ANCORADA na copa real (árvore=120px; copa ~ty-115..ty-45)
  else{ var ox2=(rnd()<0.5?-1:1)*(30+Math.floor(rnd()*16));               // ±30..45 no pé
   x=tx+ox2; y=ty+10; sy=y; chao=true; }
  out.push({x:x,y:y,sy:sy,n:nn,vale:vale,dez:(vale===10),chao:chao});}
 if(R.tipo==="ordenar"){ // posição != ordem: embaralha quais lugares recebem 1..n
  var ord=[],k;for(k=0;k<out.length;k++)ord.push(k+1);
  for(k=out.length-1;k>0;k--){var j=Math.floor(rnd()*(k+1)),tmp=ord[k];ord[k]=ord[j];ord[j]=tmp;}
  for(k=0;k<out.length;k++)out[k].n=ord[k];}
 return out;}
/* save/retomar por rodada (professor pode pausar; save retoma no início da rodada) */
function _salvaProg(idx){try{if(AULA&&AULA.id)localStorage.setItem("eduaula_"+AULA.id,""+idx);}catch(e){}}
function _leProg(){try{if(AULA&&AULA.id){var v=localStorage.getItem("eduaula_"+AULA.id);
 if(v!=null){var n=parseInt(v,10);if(n>=0&&n<AULA.rounds.length)return n;}}}catch(e){}return 0;}

function aulaInit(){ if(!MODO_AULA)return;
 if(AULA.byte){byte.x=AULA.byte.x;byte.y=AULA.byte.y;var c=cellCam();cam.x=c[0];cam.y=c[1];}
 rodadaCarrega(_leProg()); }

function rodadaCarrega(idx){
 rIdx=idx;rRound=AULA.rounds[idx];rTipo=rRound.tipo;rN=rRound.n||0;rAlvo=rRound.alvo||0;
 rCesta=rRound.cesta||{x:Math.max(160,Math.min(WW-160,byte.x+160)),y:byte.y};
 rColhidas=0;rNaCesta=0;rExtra=0;rProx=1;rGrupos=0;
 rItens=[];rFly=[];rBadges=[];rEstado="rodada";rTransT=0;rDicaT=5;aulaComemora=false;
 var itens=rRound.itens||_geraItens(rRound,idx),i;
 for(i=0;i<itens.length;i++){var it=itens[i];
  rItens.push({id:i,n:(it.n!=null?it.n:i+1),x:it.x,y:it.y,
   sy:(it.sy!=null?it.sy:it.y),chao:!!it.chao,
   vale:(it.vale||(it.dez?10:1)),got:false,over:false,blinkT:0,
   seed:(it.x*0.7+it.y*0.31),cor:_corFruta(i,it)});}
 _salvaProg(idx);rodadaAnuncia(); }

function rodadaAnuncia(){ var AT=(AULA&&AULA.textos)?AULA.textos:{},msg="";
 if(AT.anuncio&&AT.anuncio[rTipo]) msg=_txtRodada(AT.anuncio[rTipo]);
 else if(rTipo==="contar") msg="Vamos colher "+rN+" frutinhas! Conta comigo a cada uma.";
 else if(rTipo==="ordenar") msg="Colhe na ordem! Começa do um. Qual vem primeiro?";
 else if(rTipo==="trazer_exato") msg=(rRound.pedido||"O amiguinho")+" precisa de exatamente "+rAlvo+" na cesta. Vamos ajudar!";
 else if(rTipo==="agrupar") msg="Agora contamos de dez em dez! Pega as sacolas de dez.";
 balaoNPC("Byte",msg,"aula_intro_"+rTipo,1.12); }
// substituicao simples de variaveis nos textos de aula vindos dos DADOS
function _txtRodada(s){return String(s).replace("{n}",rN).replace("{alvo}",rAlvo).replace("{prox}",rProx).replace("{pedido}",(rRound&&rRound.pedido)||"O amiguinho");}
function rodadaFala(forcar){ if(rEstado==="rodada"){ if(forcar)rodadaAnuncia(); else byteDica(); } }

/* Byte PERGUNTA (nunca entrega a resposta) */
function byteDica(){ if(rEstado!=="rodada")return; var AT=(AULA&&AULA.textos)?AULA.textos:{},q="";
 if(AT.dica&&AT.dica[rTipo]) q=_txtRodada(AT.dica[rTipo]);
 else if(rTipo==="contar") q="Quantas já colhemos? Vamos ver!";
 else if(rTipo==="ordenar") q="Qual número vem primeiro agora? Procura o "+rProx+"!";
 else if(rTipo==="trazer_exato") q="Quantas faltam para chegar em "+rAlvo+"?";
 else if(rTipo==="agrupar") q="Quantos grupos de dez já temos?";
 if(rTipo==="ordenar")_piscaProx();
 balaoNPC("Byte",q,"aula_dica_"+rTipo,1.12); }
function _piscaProx(){for(var i=0;i<rItens.length;i++)if(!rItens[i].got&&rItens[i].n===rProx)rItens[i].blinkT=1.6;}

/* tentativa de colher — chamada por proximidade no update E pelo auditor via _qaColher */
function tentaColher(it){ if(it.got&&!it.over)return;
 if(it.over){ // fruta que sobrou boiando na cesta: a criança DEVOLVE (conserta o "demais")
  it.over=false;it.got=false;rExtra=Math.max(0,rExtra-1);
  var rnd=_rng((Math.floor(it.seed)|0)+rIdx*13),x,y,ok=false,tr=0;
  while(!ok&&tr++<40){x=140+rnd()*(WW-280);y=170+rnd()*(WH-320);
   ok=!_pertoArvore(x,y)&&(Math.abs(x-rCesta.x)>120||Math.abs(y-rCesta.y)>120);}
  it.x=x;it.y=y;it.sy=y;it.chao=true;somColher();  // volta ao chão -> sy/chao coerentes p/ coleta e sombra
  balaoNPC(rRound.pedido||"Byte","Isso! Agora são "+rNaCesta+"."+(rNaCesta<rAlvo?" Ainda faltam.":""),"aula_ok",1.1);
  return; }
 if(rTipo==="ordenar"&&it.n!==rProx){ _erroOrdem(); return; }   // ordem errada = consequência, NÃO colhe
 _colhe(it); }
function _erroOrdem(){ _piscaProx(); somErroGentil();
 balaoNPC("Byte","Ops! Esse não. Qual vem primeiro? Procura o "+rProx+"!","aula_ordem",1.14); } // sem X, não trava

function _colhe(it){ it.got=true; var extra=false,badge;
 if(rTipo==="ordenar"){ rProx++;rColhidas++;badge=it.n; }
 else if(rTipo==="agrupar"){ rColhidas+=it.vale;if(it.vale===10)rGrupos++;badge=rColhidas; }
 else if(rTipo==="trazer_exato"){ if(rNaCesta<rAlvo){rNaCesta++;badge=rNaCesta;}else{rExtra++;extra=true;badge="+";} }
 else{ rColhidas++;badge=rColhidas; } // contar
 rFly.push({x0:it.x,y0:it.y,p:0,cor:it.cor,vale:it.vale,badge:badge,extra:extra,srcId:it.id});
 somColher();
 for(var s=0;s<8;s++)estrelas.push({x:it.x,y:it.y-6,vx:Math.random()*70-35,vy:-(30+Math.random()*60),a:1,r:2+Math.random()*3});
 _falaConta(it,extra); _checaCompleta(); }
function _falaConta(it,extra){
 if(rTipo==="ordenar"){ playFala("n"+it.n,"Isso! O "+palN(it.n)+"!",1.16); }
 else if(rTipo==="agrupar"){ if(it.vale===10)somGrupo(); playFala("n"+rColhidas,palN(rColhidas)+"!",1.14); }
 else if(rTipo==="trazer_exato"){ if(extra)balaoNPC("Byte","Opa! Já temos "+rAlvo+". Essa sobrou — deixa na cesta pra tirar.","aula_demais",1.14);
   else playFala("n"+rNaCesta,palN(rNaCesta)+"!",1.16); }
 else{ playFala("n"+rColhidas,palN(rColhidas)+"!",1.16); } } // contar

/* trazer_exato: encostar na cesta = LEVAR/ENTREGAR (ação espacial, não botão) */
function _entrega(){ if(rEstado!=="rodada"||rTipo!=="trazer_exato")return;
 if(rExtra>0){ if(rDicaT>3){rDicaT=3;balaoNPC(rRound.pedido||"Byte","Tem "+rExtra+" a mais na cesta. Pega de volta, por favor!","aula_demais",1.12);} return; }
 if(rNaCesta<rAlvo){ if(rDicaT>3){rDicaT=3;balaoNPC(rRound.pedido||"Byte","Ainda faltam "+(rAlvo-rNaCesta)+". Traz mais!","aula_falta",1.12);} return; }
 if(rNaCesta===rAlvo) rodadaCompleta(); }

function _checaCompleta(){ if(rEstado!=="rodada")return; var done=false;
 if(rTipo==="contar") done=(rColhidas>=rN);
 else if(rTipo==="ordenar") done=(rProx>rN);
 else if(rTipo==="agrupar") done=(rColhidas>=rN);
 // trazer_exato só conclui via _entrega
 if(done) rodadaCompleta(); }
function rodadaCompleta(){ rEstado="transicao";rTransT=0;aulaComemora=true; if(som)somVitoria();
 var total=(rTipo==="ordenar")?rN:(rTipo==="trazer_exato")?rAlvo:rColhidas,s;
 for(s=0;s<20;s++)estrelas.push({x:rCesta.x,y:rCesta.y-10,vx:Math.random()*120-60,vy:-(40+Math.random()*80),a:1,r:3+Math.random()*4});
 balaoNPC("Byte","Conseguimos! Colhemos "+total+"! "+palN(total)+"! Muito bem!","aula_ok_"+rIdx,1.16);
 _salvaProg(rIdx+1); }
function aulaAvanca(){
 if(rIdx+1<AULA.rounds.length){ rodadaCarrega(rIdx+1); }
 else{ aulaFim=true;aulaFimT=0;aulaComemora=true; if(som)somVitoria();
  balaoNPC("Byte",AULA.fim||"Você contou tudo sozinho! Que colheita linda. Até a próxima!","aula_fim",1.14); } }

/* animação voar->cesta + badges (nada alocado por frame além do pool) */
function _flyUpdate(dt){ for(var i=rFly.length-1;i>=0;i--){var f=rFly[i];f.p+=dt/0.5;
  if(f.p>=1){ rBadges.push({x:rCesta.x,y:rCesta.y-34,txt:(""+f.badge),t:0,cor:f.cor});
   if(f.extra){ for(var k=0;k<rItens.length;k++)if(rItens[k].id===f.srcId){
     rItens[k].over=true;rItens[k].got=false;rItens[k].x=rCesta.x+(Math.random()*30-15);rItens[k].y=rCesta.y-26;break;} }
   rFly.splice(i,1);} } }
function _badgeUpdate(dt){for(var i=rBadges.length-1;i>=0;i--){var b=rBadges[i];b.t+=dt;b.y-=18*dt;if(b.t>1.1)rBadges.splice(i,1);}}

/* update por frame (chamado no loop logo após updateNPCs) */
function rodadaUpdate(dt,t){ if(!MODO_AULA)return;
 if(aulaFim){ aulaFimT+=dt;_flyUpdate(dt);_badgeUpdate(dt);return; }
 if(rEstado==="transicao"){ rTransT+=dt;_flyUpdate(dt);_badgeUpdate(dt);
   if(rTransT>2.6){ aulaComemora=false; aulaAvanca(); } return; }
 rDicaT-=dt; if(rDicaT<=0){ rDicaT=9+Math.random()*5; byteDica(); }   // Byte pergunta de tempos em tempos
 for(var i=0;i<rItens.length;i++){var it=rItens[i]; if(it.blinkT>0)it.blinkT-=dt;
   if(it.got&&!it.over)continue;
   // maçã PENDURADA: mede a distância contra a ÂNCORA DE CHÃO (base do tronco = it.sy),
   // não contra it.y (que fica na copa) -> a criança colhe encostando o Byte no PÉ da árvore.
   var ay=(it.chao?it.y:(it.sy!=null?it.sy:it.y));
   var dx=byte.x-it.x,dy=byte.y-ay; if(dx*dx+dy*dy<54*54) tentaColher(it); }
 if(rTipo==="trazer_exato"){var ex=byte.x-rCesta.x,ey=byte.y-rCesta.y; if(ex*ex+ey*ey<58*58)_entrega();}
 _flyUpdate(dt);_badgeUpdate(dt); }

/* ---------- DESENHO (tudo por código; restaura globalAlpha) ---------- */
function drawNum(x,y,size,txt,cor){cx.save();cx.font="bold "+size+"px Verdana";cx.textAlign="center";cx.textBaseline="middle";
 cx.lineWidth=Math.max(3,size*0.18);cx.lineJoin="round";cx.strokeStyle="rgba(15,25,45,.9)";cx.strokeText(txt,x,y);
 cx.fillStyle=cor||"#fff";cx.fillText(txt,x,y);cx.restore();cx.textBaseline="alphabetic";cx.globalAlpha=1;}
function desFruta(o,t){ if(o.got&&!o.over)return; var x=o.x,y=o.y;
 var wob=Math.sin(t*0.004+o.seed)*3,trem=o.blinkT>0?Math.sin(t*0.045)*4:0;
 var alvoNext=(rTipo==="ordenar"&&o.n===rProx);
 if(o.chao)sombra(x,y+14,o.vale===10?20:15,6); // só a maçã CAÍDA leva sombra de chão
 if(!o.chao&&o.vale!==10){ // fruta PENDURADA: haste ligando à copa + sombra pendurada (fruta ancorada, não flutua)
  // haste: galho curto marrom (~2px, 10px, leve curva) do topo da fruta p/ cima
  cx.save();cx.strokeStyle="#5a3a1e";cx.lineWidth=2;cx.beginPath();
  cx.moveTo(x+trem,y-20+wob);cx.quadraticCurveTo(x+trem+3,y-26+wob,x+trem+1,y-30+wob);cx.stroke();cx.restore();
  // sombra pendurada: elipse BEM suave dentro da copa, sob a fruta
  cx.save();cx.globalAlpha=0.10;cx.fillStyle="#1c3a12";cx.beginPath();
  cx.ellipse(x,y+9+wob,12,5,0,0,Math.PI*2);cx.fill();cx.restore();cx.globalAlpha=1; }
 if(o.vale===10){ // SACOLA DE DEZ
  if(IMG.sacola10){ imgH(IMG.sacola10,x+trem,y+wob,30); }
  else { cx.save();cx.translate(x+trem,y-10+wob);cx.fillStyle="#7a5230";roundR(-18,-14,36,30,7);cx.fill();
   cx.fillStyle="#8f6238";cx.fillRect(-18,-16,36,6);cx.restore();drawNum(x+trem,y-9+wob,20,"10","#fff"); }
 } else { // FRUTA: maçã PINTADA (IA) se houver; senão círculo desenhado (fallback leve)
  if(IMG.fruta){ imgH(IMG.fruta,x+trem,y+3+wob,24); }
  else { cx.save();cx.translate(x+trem,0);
   cx.beginPath();cx.arc(0,y-8+wob,15,0,Math.PI*2);cx.fillStyle=o.cor;cx.fill();
   cx.beginPath();cx.arc(-5,y-12+wob,5,0,Math.PI*2);cx.fillStyle="rgba(255,255,255,.35)";cx.fill();
   cx.fillStyle="#3a7d34";cx.beginPath();cx.ellipse(4,y-22+wob,7,4,-0.6,0,Math.PI*2);cx.fill();
   cx.strokeStyle="#5a3a1e";cx.lineWidth=2;cx.beginPath();cx.moveTo(0,y-22+wob);cx.lineTo(2,y-27+wob);cx.stroke();
   cx.restore(); }
  if(rTipo==="ordenar") drawNum(x+trem,y-8+wob,18,""+o.n,"#fff"); } // ordenar mostra o numeral
 if(o.vale!==10){ // BRILHO de maçã madura SEMPRE-LIGADO: halo quente suave pulsando (sinaliza "colhe aqui")
  var ph=0.07+0.04*Math.sin(t*0.006+o.seed);
  cx.save();cx.globalCompositeOperation="lighter";
  var gh=cx.createRadialGradient(x,y-8,3,x,y-8,30);gh.addColorStop(0,"rgba(255,240,150,"+ph+")");gh.addColorStop(1,"rgba(255,240,150,0)");
  cx.fillStyle=gh;cx.beginPath();cx.arc(x,y-8,30,0,Math.PI*2);cx.fill();cx.restore();cx.globalAlpha=1; }
 if(alvoNext||o.blinkT>0){ var pa=0.25+0.25*Math.sin(t*0.012);
  cx.save();cx.globalCompositeOperation="lighter";
  var g=cx.createRadialGradient(x,y-8,4,x,y-8,34);g.addColorStop(0,"rgba(255,240,150,"+pa+")");g.addColorStop(1,"rgba(255,240,150,0)");
  cx.fillStyle=g;cx.beginPath();cx.arc(x,y-8,34,0,Math.PI*2);cx.fill();cx.restore();cx.globalAlpha=1; }
 if(o.over){ cx.save();cx.globalAlpha=0.6+0.4*Math.sin(t*0.02);cx.fillStyle="#ffcf4a";cx.font="bold 16px Verdana";cx.textAlign="center";
  cx.fillText("↑",x,y-34+wob);cx.restore();cx.globalAlpha=1; } }
function desCesta(t){ if(!rCesta)return; var x=rCesta.x,y=rCesta.y,i;
 sombra(x,y+8,34,10);
 if(IMG.cesta){ imgH(IMG.cesta,x,y+14,40); }                        // CESTA pintada (IA)
 else { cx.save();cx.fillStyle="#a9762f";roundR(x-30,y-16,60,30,8);cx.fill();   // fallback code-drawn
  cx.strokeStyle="rgba(80,50,20,.6)";cx.lineWidth=2;
  for(i=-24;i<=24;i+=8){cx.beginPath();cx.moveTo(x+i,y-16);cx.lineTo(x+i,y+14);cx.stroke();}
  cx.beginPath();cx.moveTo(x-30,y-2);cx.lineTo(x+30,y-2);cx.stroke();
  cx.fillStyle="#8a5f24";cx.fillRect(x-32,y-18,64,5);cx.restore(); }
 if(rTipo==="agrupar"){ for(i=0;i<rGrupos&&i<3;i++){ if(IMG.sacola10){ imgH(IMG.sacola10,x-12+i*14,y-16,18); } // sacolas-de-10 pintadas na cesta
   else { cx.fillStyle="#7a5230";roundR(x-20+i*14,y-30,16,14,4);cx.fill();drawNum(x-12+i*14,y-23,10,"10","#fff"); } } }
 else if(rTipo==="trazer_exato"){ cx.save();cx.fillStyle="rgba(20,30,50,.85)";roundR(x-26,y-46,52,20,6);cx.fill(); // HUD/indicador (mantido: leitura de "faltam")
   for(i=0;i<rAlvo&&i<8;i++){cx.fillStyle=(i<rNaCesta)?"#7be07b":"rgba(255,255,255,.35)";cx.beginPath();cx.arc(x-20+i*6,y-36,2.4,0,Math.PI*2);cx.fill();}cx.restore(); }
 else{ var pilha=Math.min((rTipo==="ordenar"?rColhidas:rColhidas),6);
   for(i=0;i<pilha;i++){ var mfx=x-16+i*6, mfy=y-1-((i%2)*5);                    // monte na cesta = mini-maçãs pintadas
    if(IMG.fruta){ imgH(IMG.fruta,mfx,mfy,14); }
    else { cx.fillStyle=_CORF[i%_CORF.length];cx.beginPath();cx.arc(mfx,mfy-5,5,0,Math.PI*2);cx.fill(); } } }
 cx.globalAlpha=1; }
function desFly(){ for(var i=0;i<rFly.length;i++){var f=rFly[i];
  var px=f.x0+(rCesta.x-f.x0)*f.p, py=f.y0+(rCesta.y-f.y0)*f.p-Math.sin(f.p*Math.PI)*70;
  if(f.vale===10){ if(IMG.sacola10){ imgH(IMG.sacola10,px,py+10,22); } else {cx.fillStyle="#7a5230";roundR(px-9,py-8,18,16,4);cx.fill();} }
  else{ if(IMG.fruta){ imgH(IMG.fruta,px,py+10,20); } else {cx.beginPath();cx.arc(px,py-4,9,0,Math.PI*2);cx.fillStyle=f.cor;cx.fill();} } } cx.globalAlpha=1; }
function desBadges(){ for(var i=0;i<rBadges.length;i++){var b=rBadges[i];
  cx.save();cx.globalAlpha=Math.max(0,1-b.t/1.1);drawNum(b.x,b.y,20,b.txt,"#ffe38a");cx.restore();} cx.globalAlpha=1; }
/* HUD contador (TELA) — desenhado no lugar do texto da chave */
function desHUDrodada(){ if(!MODO_AULA)return; var cur=0,alvo=0,lab="";
 if(rTipo==="contar"){cur=rColhidas;alvo=rN;lab="colhidas";}
 else if(rTipo==="ordenar"){cur=rProx-1;alvo=rN;lab="em ordem";}
 else if(rTipo==="agrupar"){cur=rColhidas;alvo=rN;lab="de 10 em 10";}
 else if(rTipo==="trazer_exato"){cur=rNaCesta;alvo=rAlvo;lab="na cesta";}
 cx.save();cx.textAlign="center";
 cx.fillStyle="#ffe38a";cx.font="bold 14px Verdana";cx.fillText("🧺 "+cur+" / "+alvo,VW/2,17);
 cx.fillStyle="rgba(255,255,255,.5)";cx.font="10px Verdana";
 cx.fillText("Rodada "+(rIdx+1)+" de "+AULA.rounds.length+" · "+lab,VW/2,VH-8);
 cx.restore();cx.globalAlpha=1; }
/* overlay de comemoração/transição e fim da aula (TELA) */
function aulaOverlay(t){ if(!MODO_AULA)return;
 if(rEstado==="transicao"){ var a=Math.min(.5,rTransT*0.5);cx.fillStyle="rgba(6,12,26,"+a+")";cx.fillRect(0,0,VW,VH);
  var total=(rTipo==="ordenar")?rN:(rTipo==="trazer_exato")?rAlvo:rColhidas;
  var pop=1+Math.sin(Math.min(1,rTransT*3)*Math.PI/2)*0.2;
  cx.save();cx.translate(VW/2,VH/2-6);cx.scale(pop,pop);drawNum(0,0,64,""+total,"#ffe38a");cx.restore();
  cx.fillStyle="#eaf2ff";cx.font="bold 15px Verdana";cx.textAlign="center";cx.fillText("✨ "+palN(total)+"! ✨",VW/2,VH/2+42); }
 if(aulaFim){ var af=Math.min(.62,aulaFimT*0.5);cx.fillStyle="rgba(6,10,22,"+af+")";cx.fillRect(0,0,VW,VH);
  cx.fillStyle="#ffe38a";cx.font="bold 24px Verdana";cx.textAlign="center";cx.fillText("🌟 Colheita Completa! 🌟",VW/2,VH/2-6);
  cx.fillStyle="#eaf2ff";cx.font="13px Verdana";cx.fillText("Você contou tudo sozinho!",VW/2,VH/2+22); }
 cx.globalAlpha=1; }

/* sons novos (mesmo estilo bip do motor; silenciosos se som off) */
function somColher(){bip(660,.06,"sine",.12,0);bip(990,.08,"sine",.10,.05);}
function somErroGentil(){bip(440,.10,"sine",.10,0);bip(330,.14,"sine",.09,.09);} // suave/descendente, NÃO é buzzer
function somGrupo(){bip(523,.10,"sine",.12,0);bip(784,.12,"sine",.12,.1);}

/* ---------- QA / AUDITORIA ---------- */
window._qaAula=function(){return {modo:MODO_AULA,round:rIdx,tipo:rTipo,estado:rEstado,
 n:rN,alvo:rAlvo,colhidas:rColhidas,prox:rProx,naCesta:rNaCesta,extra:rExtra,grupos:rGrupos,
 aulaFim:aulaFim,total:(AULA?AULA.rounds.length:0),
 itens:rItens.map(function(o){return {id:o.id,n:o.n,vale:o.vale,got:o.got,over:o.over,blink:o.blinkT>0};})};};
window._qaColher=function(id){for(var i=0;i<rItens.length;i++)if(rItens[i].id===id){tentaColher(rItens[i]);break;}return window._qaAula();};
window._qaProx=function(){for(var i=0;i<rItens.length;i++)if(!rItens[i].got&&rItens[i].n===rProx)return rItens[i].id;return -1;};
window._qaEntrega=function(){_entrega();return window._qaAula();};
window._qaTransFim=function(){if(rEstado==="transicao")rTransT=99;return window._qaAula();}; // força fim da transição p/ testar avanço

/* ===== FUNCOES: subsistemas de mundo-vivo (mundo-vivo v2) ===== */
// ================= POEIRINHA AO ANDAR (reutilizavel) =================
// emite 1 nuvenzinha de poeira nos pes (x,y). Math.random SO aqui (no spawn),
// NUNCA no render -> nao pisca. Teto baixo p/ nao pesar no celular.
function emitePoeira(x,y){if(poeira.length>26)return;
 poeira.push({x:x+(Math.random()-.5)*7, y:y-Math.random()*3,
  vx:(-byte.dir)*(5+Math.random()*9)+(gust-0.5)*18, // chuta pra tras do passo + deriva do vento
  vy:-(7+Math.random()*9),                           // sobe
  r:2.3+Math.random()*1.8, gro:9+Math.random()*7,    // raio inicial + quanto expande
  a:0.26+Math.random()*0.13});}                       // ja nasce translucida (alpha baixo)

// ================= MICRO-MOVIMENTOS (biblioteca pura, sem estado) =================
// Determinísticas por FASE (ph): mesmo t+ph => mesmo valor (nao aloca, nao pisca).
// Cada personagem passa um ph proprio (ex.: o seu x) p/ nao ficarem sincronizados.
function breathe(t,ph){return Math.sin(t*0.0028+(ph||0));}            // respiro lento -> [-1,1]; o caller escala (ex.: *0.03 no scaleY)
function sway(t,ph,amp){return (amp||0.03)*Math.sin(t*0.0016+(ph||0));} // balanco suave do corpo -> RADIANOS (usar em cx.rotate)
function blink(t,ph){var c=(t*0.001+(ph||0)*3.3)%4.2;return c<0.11?0:1;} // 1=olho aberto / 0=piscando (~1 piscada a cada 4.2s)
/* ================= CLIMA / ATMOSFERA (data-driven, default off) ================= */
/* Decisao de camada: CHUVA e VENTO sao camada de TELA (colados na camera), nao de
   mundo. Motivo: gota/risco nao tem "posicao no mundo" util — teriamos que popular
   1500x1050 inteiro so pra ver ~80 gotas na viewport. Em TELA um pool fixo de ~80
   gotas cobre sempre o que aparece, de graca, e nunca depende do tamanho do mapa.
   O FLASH tambem e TELA (por cima de tudo, ate do HUD). Ja "chao molhado" (opcional)
   e do MUNDO (brilho no chao), entao desenha DENTRO do translate da camera. NEVE
   reusa os flocos de leaves (que ja sao spawnados em coord de tela via cam.x/cam.y). */

/* som de trovao — no MESMO estilo dos bip/somCoruja (usa o AC/ambMaster ja criados).
   Estrondo = ruido grave que decai; buffer curto criado SO no trovao (raro), nunca por frame. */
function somTrovao(){if(!AC||!som)return;
 var dur=1.5,n=Math.floor(AC.sampleRate*dur),buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);
 for(var i=0;i<n;i++){var k=1-i/n;d[i]=(Math.random()*2-1)*k*k;}          // envelope de decaimento
 var s=AC.createBufferSource();s.buffer=buf;
 var f=AC.createBiquadFilter();f.type="lowpass";f.frequency.value=170;    // grave: nao estressa a crianca
 var g=AC.createGain(),t0=AC.currentTime;
 g.gain.setValueAtTime(0.0001,t0);g.gain.exponentialRampToValueAtTime(0.45,t0+0.06);g.gain.exponentialRampToValueAtTime(0.001,t0+dur);
 s.connect(f);f.connect(g);g.connect(ambMaster||AC.destination);s.start(t0);s.stop(t0+dur);
 bip(46,dur*0.7,"sine",0.10,0.03);}                                       // rombo grave extra p/ peso

/* update por frame: move gotas, sorteia rajadas visiveis, agenda flash+trovao */
function climaUpdate(dt,t){
 if(!CLIMA)return;                                            // "" = nada (floresta intacta)
 var slope=0.32+gust*0.55;                                    // inclinacao segue o vento (gust)
 if(chuvaOn){for(var i=0;i<gotas.length;i++){var g=gotas[i];
   g.y+=g.sp*dt; g.x+=g.sp*slope*dt;                          // cai na diagonal
   if(g.s>0)g.s-=dt*3.2;                                      // decai o splash
   if(g.y>VH){ g.sx=g.x; g.s=1;                               // bateu no chao -> marca splash e recicla no topo
     g.y=-10-Math.random()*40; g.x=Math.random()*VW-40; g.l=8+Math.random()*10; g.sp=520+Math.random()*280; }
   if(g.x>VW+20)g.x-=VW+40;                                   // volta pela esquerda (nao esvazia a tela)
 }}
 // rajadas visiveis: so quando o vento aperta. recicla o pool fixo (nada de alocar).
 if(gust>0.72){for(var k=0;k<ventos.length;k++){var w=ventos[k];
   if(!w.on&&Math.random()<0.04){w.on=true;w.x=-40;w.y=20+Math.random()*(VH-60);w.len=40+Math.random()*70;w.sp=340+Math.random()*260;w.a=0.10+Math.random()*0.12;break;} }}
 for(var k2=0;k2<ventos.length;k2++){var w2=ventos[k2];if(w2.on){w2.x+=w2.sp*dt;w2.y+=w2.sp*0.12*dt;if(w2.x>VW+80)w2.on=false;}}
 // flash + trovao (tempestade): frequencia BAIXA p/ nao assustar
 if(flash>0)flash-=dt*7;                                      // clarao curto (~0.14s)
 if(trovaoOn){flashT-=dt;if(flashT<=0){flashT=7+Math.random()*8;flash=1;trovaoDelay=0.3+Math.random()*1.2;}
   if(trovaoDelay>0){trovaoDelay-=dt;if(trovaoDelay<=0){somTrovao();trovaoDelay=-1;}}}
}

/* desenho na TELA (chuva + rajadas). NAO usa o translate da camera. */
function climaDesenha(t){
 if(!CLIMA)return;
 var slope=0.32+gust*0.55;
 if(chuvaOn){
   // escurece MUITO pouco (ceu carregado); um tico a mais na tempestade
   cx.save();cx.fillStyle="rgba(30,40,66,"+(0.06+(trovaoOn?0.05:0))+")";cx.fillRect(0,0,VW,VH);cx.restore();
   // gotas: riscos finos, num unico traçado (barato)
   cx.save();cx.strokeStyle="rgba(190,215,255,0.5)";cx.lineWidth=1.2;cx.lineCap="round";cx.beginPath();
   for(var i=0;i<gotas.length;i++){var g=gotas[i];cx.moveTo(g.x,g.y);cx.lineTo(g.x-g.l*slope,g.y-g.l);}
   cx.stroke();cx.restore();
   // splash sutil onde cada gota bateu (arco no chao que abre e some)
   cx.save();cx.strokeStyle="rgba(200,220,255,0.35)";cx.lineWidth=1;
   for(var j=0;j<gotas.length;j++){var s2=gotas[j];if(s2.s>0){cx.globalAlpha=s2.s*0.5;var rr=(1-s2.s)*6+1;
     cx.beginPath();cx.arc(s2.sx,VH-6,rr,Math.PI*1.15,Math.PI*1.85);cx.stroke();}}
   cx.globalAlpha=1;cx.restore();
 }
 // rajadas de vento visiveis (linhas claras cruzando a tela)
 cx.save();cx.strokeStyle="rgba(255,255,255,0.6)";cx.lineWidth=1.4;cx.lineCap="round";
 for(var k=0;k<ventos.length;k++){var w=ventos[k];if(w.on){cx.globalAlpha=w.a;
   cx.beginPath();cx.moveTo(w.x,w.y);cx.lineTo(w.x-w.len,w.y-w.len*0.16);cx.stroke();}}
 cx.globalAlpha=1;cx.restore();
}

/* FLASH do raio: tela inteira, por CIMA de tudo (ate do HUD/fim) */
function climaFlash(){
 if(flash>0){cx.save();cx.fillStyle="rgba(255,255,255,"+Math.min(0.6,flash*0.6)+")";cx.fillRect(0,0,VW,VH);cx.restore();cx.globalAlpha=1;}
}

/* brilho de chao molhado (opcional, MUNDO) — desenha DENTRO do translate da camera */
function climaMolha(){
 if(!CLIMA_MOLHA||!chuvaOn)return;
 cx.save();cx.globalCompositeOperation="lighter";cx.globalAlpha=0.05;
 cx.fillStyle="rgba(150,180,230,1)";cx.fillRect(cam.x,cam.y,VW,VH);cx.restore();cx.globalAlpha=1;
}
/* ---------- NUVENS (sombras de nuvem no chao + nuvens claras no ceu) ---------- */
// SOMBRAS: manchas grandes e macias cruzando o chao (plano do MUNDO, dentro da camera).
// deterministicas em forma (blobs fixos) -> NAO piscam; movimento vem de t (sem random no loop).
function desNuvSombra(t){if(!nuvSombra.length||noite>0.92)return;
 var dim=1-noite*0.85;                                    // a noite quase somem
 var lo=-450,hi=WW+450,span=hi-lo;                        // faixa de loop no mundo
 for(var i=0;i<nuvSombra.length;i++){var c=nuvSombra[i];
  var px=((c.x+t*0.001*c.sp-lo)%span+span)%span+lo;       // deriva devagar no eixo do vento (+x), em loop
  var py=c.y+Math.sin(t*0.00008+c.ph)*40;                 // leve vaivem lento no y
  var env=Math.max(0,Math.min(1,Math.min(px-lo,hi-px)/300)); // some/reaparece suave nas pontas
  var breath=0.72+0.28*Math.sin(t*0.00013+c.ph);          // respiro proprio (nascer/morrer)
  var a=c.a*dim*env*breath; if(a<0.004)continue;
  for(var b=0;b<c.bl.length;b++){var bb=c.bl[b];           // cluster de blobs = 1 nuvem
   var bx=px+bb.dx*c.w,by=py+bb.dy*c.w,r=bb.r*c.w;
   var g=cx.createRadialGradient(bx,by,r*0.15,bx,by,r);
   g.addColorStop(0,"rgba(16,20,32,"+a+")");g.addColorStop(0.6,"rgba(16,20,32,"+(a*0.5)+")");g.addColorStop(1,"rgba(16,20,32,0)");
   cx.fillStyle=g;cx.beginPath();cx.arc(bx,by,r,0,Math.PI*2);cx.fill();}}}
// CEU: nuvens claras baixinhas no topo (coordenada de TELA), derivando devagar, bem discretas.
function desNuvCeu(t){if(!nuvCeu.length)return;var dim=1-noite*0.7;if(dim<=0.02)return;
 var lo=-150,hi=VW+150,span=hi-lo;
 for(var i=0;i<nuvCeu.length;i++){var c=nuvCeu[i];
  var px=((c.x+t*0.0016*c.sp-lo)%span+span)%span+lo;       // deriva lenta no topo, em loop
  var py=c.y+Math.sin(t*0.0001+c.ph)*4;
  var env=Math.max(0,Math.min(1,Math.min(px-lo,hi-px)/120)); // borda suave (sem pop no loop)
  var a=c.a*dim*env; if(a<0.004)continue;
  for(var b=0;b<c.bl.length;b++){var bb=c.bl[b];
   var bx=px+bb.dx*c.s,by=py+bb.dy*c.s,r=bb.r*c.s;
   var g=cx.createRadialGradient(bx,by-r*0.25,r*0.2,bx,by,r);
   g.addColorStop(0,"rgba(255,255,255,"+a+")");g.addColorStop(0.55,"rgba(250,252,255,"+(a*0.55)+")");g.addColorStop(1,"rgba(250,252,255,0)");
   cx.fillStyle=g;cx.beginPath();cx.arc(bx,by,r,0,Math.PI*2);cx.fill();}}}
/* ---------- NPCS VIVOS (IA de personagem leve) ---------- */
// Reaproveita a lib de micro-movimentos do subsistema "poeira-micromov"
// (breathe(seed,t)/sway(seed,t)/blink(seed,t)) e o balao do "baloes-rpg"
// (balaoNPC(nome,texto,id)). Todos com FALLBACK (guard typeof) p/ funcionar
// mesmo antes desses subsistemas serem integrados -> ordem-independente.
function updateNPCs(dt,t){
 for(var i=0;i<npcs.length;i++){var n=npcs[i];
  var dbx=byte.x-n.x,dby=byte.y-n.y,perto=(dbx*dbx+dby*dby)<90*90; // raio de interacao ~90
  n.cd-=dt;                                                        // cooldown do balao
  if(perto){                                                       // INTERACAO: encara o Byte
   n.olha=Math.min(1,n.olha+dt*4);
   if(dbx<-4)n.dir=-1;else if(dbx>4)n.dir=1;                       // olha na direcao dele
   if((n.fala||(n.falas&&n.falas.length))&&n.cd<=0){n.cd=8;n.acen=1.0; // fala 1x, reacena so apos 8s
    var nf=n.fala,nid="npc"+i;                                     // padrao: fala unica (como hoje)
    if(n.falas&&n.falas.length){n.fi=(n.fi||0);var fo=n.falas[n.fi%n.falas.length];n.fi++;
     if(typeof fo==="string"){nf=fo;nid=null;}                     // string simples -> TTS
     else{nf=fo.texto||"";nid=fo.id||null;}}                       // objeto {texto,id}
    if(typeof balaoNPC==="function")balaoNPC(n.nome,nf,nid,null,n);
    else balao(n.nome?n.nome+": "+nf:nf,nid);}                     // fallback: balao atual
  } else { n.olha=Math.max(0,n.olha-dt*2); }
  if(n.acen>0)n.acen-=dt;
  // ROTINA: patrulha a rota devagar; congela enquanto encara o Byte
  if(n.rota&&n.rota.length>1&&n.olha<0.2){
   if(n.paus>0){n.paus-=dt;n.mvx=0;}                               // pausa no ponto
   else{var tp=n.rota[n.ri],ax=tp[0]-n.x,ay=tp[1]-n.y,L=Math.sqrt(ax*ax+ay*ay);
    if(L<3){n.paus=1.2+(n.ri*0.7)%1.0;n.ri=(n.ri+1)%n.rota.length;n.mvx=0;} // chegou->pausa->proximo
    else{var st=Math.min(L,n.vel*dt);n.x+=ax/L*st;n.y+=ay/L*st;n.mvx=ax;
     if(ax<-1)n.dir=-1;else if(ax>1)n.dir=1;n.passo+=dt*8;}}       // vira pra onde anda
  } else { n.mvx=0; }
 }
}
function desNPC(n,t){var im=IMG[n.sprite];if(!im)return;            // sem sprite -> nao desenha
 var seed=n.ox*0.1+n.oy*0.13;                                      // semente deterministica (nao pisca)
 var andando=n.mvx!==0;
 // micro-movimento parado (respira + balanca no vento), com fallback deterministico
 var br=andando?0:((typeof breathe==="function")?breathe(t,seed):Math.sin(t*0.0028+seed));
 var sw=andando?0:Math.sin(t*0.0016+seed)*(0.6+gust);
 var bob=andando?Math.abs(Math.sin(n.passo*0.9))*4:0;             // pulinho ao andar
 var h=42*n.esc;
 sombra(n.x,n.y+4,15*n.esc,5*n.esc);
 cx.save();cx.translate(n.x+sw,n.y+4-bob);cx.rotate(sw*0.02);
 cx.scale(n.dir*(1+br*0.03),1-br*0.03);                            // flip + squash da respiracao
 imgH(im,0,0,h);cx.restore();
 // ACENO: patinha/mao levantada (traco simples) ao cumprimentar o Byte
 if(n.acen>0){cx.save();cx.globalAlpha=Math.min(1,n.acen);
  cx.strokeStyle="rgba(70,55,40,.85)";cx.lineWidth=3;cx.lineCap="round";
  var aw=Math.sin(t*0.02)*0.3;
  cx.beginPath();cx.moveTo(n.x+n.dir*h*0.26,n.y+4-h*0.5);
  cx.lineTo(n.x+n.dir*(h*0.32+aw*8),n.y+4-h*0.74);cx.stroke();
  cx.restore();cx.globalAlpha=1;}
}

/* ---------- LOOP ---------- */
var ult=null;
function frame(ts){if(ult===null)ult=ts;var dt=Math.max(0,Math.min(.05,(ts-ult)/1000));ult=ts;var t=ts;
 if(!patM&&IMG.muro)patM=cx.createPattern(IMG.muro,"repeat");
 byte.resp+=dt*3;
 // ---- caixa de dialogo RPG: typewriter (revela letra a letra) + setinha piscando ----
 if(balaoT>0&&balaoFull){ if(balaoAppear<1)balaoAppear=Math.min(1,balaoAppear+dt/0.16);
  if(!balaoFimTxt){balaoN+=balaoCPS*dt;if(balaoN>=balaoFull.length){balaoN=balaoFull.length;balaoFimTxt=true;}}
  balaoBlink+=dt; }
 // vento em rajadas + agenda de sons ambientes
 gust=0.45+0.35*Math.sin(t*.0004)+0.30*Math.max(0,Math.sin(t*.00013+1.2));
 var _sol=Math.cos(t*0.00005);noite=Math.max(0,Math.min(1,(0.35-_sol)/0.7)); // ciclo dia/noite (~125s, comeca de DIA)
 // ---- LUZ DIRECIONAL: deriva o VETOR do sol/lua do MESMO relogio t (_sol ja e a altura) ----
 if(SOMBRA_DIR){var _sunX=Math.sin(t*0.00005);         // leste/oeste do sol no ceu ( _sol=Math.cos = altura )
  var _A=Math.abs(_sol),_spread=1-_A;                  // _A=altura do luminar dominante: 1=a pino(curta) .. 0=baixo(longa)
  var _side=-_sunX*(1-2*noite);                        // lado OPOSTO a luz; a lua e o oposto do sol -> inverte sozinho de dia p/ noite
  luz.dx=_side*_spread*1.9;                            // (x rx) desloca a sombra p/ o lado oposto
  luz.dy=_spread*0.25;                                 // (x ry) leve queda p/ o chao quando o sol/lua esta baixo
  luz.sx=_spread*1.5;                                  // estica a elipse no comprimento (curta ao meio-dia, longa de manha/tarde)
  var _aD=(1-noite)*(0.30-0.13*_A);                    // DIA: cai ao meio-dia (_A alto) e forte de manha/tarde
  var _aN=noite*0.10;                                  // NOITE: bem fraca
  luz.a=Math.max(0.05,_aD+_aN);                         // nunca preta demais, nunca some de vez
  var _r=Math.round(18+12*noite),_g=Math.round(14+32*noite),_b=Math.round(28+68*noite);
  luz.col="rgb("+_r+","+_g+","+_b+")";}                 // neutra escura de dia -> AZULADA a noite
 if(ventoG&&som)ventoG.gain.value=0.028+0.05*gust;
 birdTimer-=dt;if(birdTimer<=0){birdTimer=3.2+Math.random()*4.2;if(TEMA.passaros)somCanto();}
 coruja-=dt;if(coruja<=0){coruja=16+Math.random()*16;somCoruja();}
 // ---- movimento ----
 if(!fim){var v=inputVec(),vx=v[0],vy=v[1];byte.mov=(vx||vy)?true:false;
  if(byte.mov){var L=Math.sqrt(vx*vx+vy*vy);vx/=L;vy/=L;byte.mvx=vx;byte.mvy=vy;var sp=140;
   var nx=byte.x+vx*sp*dt,ny=byte.y+vy*sp*dt;
   if(!bloqueado(nx,byte.y))byte.x=nx; if(!bloqueado(byte.x,ny))byte.y=ny;
   if(vx<-0.2)byte.dir=-1;else if(vx>0.2)byte.dir=1;
   byte.passo+=dt*11;if((byte.passo%1.2)<dt*11){somPasso();if(POEIRA_ON){emitePoeira(byte.x,byte.y+8);if(gust>0.6&&Math.random()<gust*0.55)emitePoeira(byte.x,byte.y+8);}}}
 } else { byte.mov=false; }
 byte.idle = byte.mov ? 0 : byte.idle+dt;  // acumula tempo parado -> senta/deita
 // ---- camera segue ----
 var cc=cellCam();cam.x+=(cc[0]-cam.x)*Math.min(1,dt*6);cam.y+=(cc[1]-cam.y)*Math.min(1,dt*6);
 // ---- pega a chave ----
 if(OBJETIVO==="chave"&&!chave.got){var dx=byte.x-chave.x,dy=byte.y-chave.y;if(dx*dx+dy*dy<40*40){chave.got=true;hasKey=true;somChave();
   for(var i=0;i<18;i++)estrelas.push({x:chave.x,y:chave.y-6,vx:Math.random()*80-40,vy:-(40+Math.random()*70),a:1,r:3+Math.random()*4});
   balao((HIST.chaveFala&&HIST.chaveFala.txt)||"Peguei a chave dourada! Agora vamos procurar o labirinto de pedra.",(HIST.chaveFala&&HIST.chaveFala.id)||"s1_chave");}}
 // ---- chega no arco (com a chave) ----
 if(OBJETIVO==="chave"&&hasKey&&!fim){var ax=byte.x-arco.x,ay=byte.y-(arco.y-16);if(ax*ax+ay*ay<80*80){fim=true;fimT=0;somVitoria();
   balao((HIST.arcoFala&&HIST.arcoFala.txt)||"Ali está o labirinto de pedra! É onde o Nimbo prendeu os amiguinhos. Na próxima aventura a gente entra para salvá-los.",(HIST.arcoFala&&HIST.arcoFala.id)||"s1_labirinto");}}
 if(fim)fimT+=dt;
 updateNPCs(dt,t); // IA dos NPCs: rotina/patrulha + interacao com o Byte

 rodadaUpdate(dt,t); // MOTOR DE RODADAS de colheita (no-op se sem MUNDO.aula): detecta colheita por proximidade, conta, ordena, entrega, agrupa, transição/comemoração e avanço entre rodadas.
 // ---- efeitos: folhas/petalas, passaros, borboletas, pollen ----
 if(leaves.length<(CLIMA==="neve"?72:40) && (Math.random()<0.06+gust*0.06+(CLIMA==="neve"?0.14*CLIMAF:0))){var neve=(TEMA.part==="neve"||CLIMA==="neve");var tipo=Math.random();
  var col=neve?(tipo<.5?"#ffffff":"#dbeafe"):(tipo<.4?"#7fae3a":tipo<.7?"#d98a2b":(tipo<.85?"#f2a6c0":"#e7d24a"));
  leaves.push({x:cam.x+Math.random()*VW,y:cam.y-10,vx:-(neve?4+Math.random()*10:10+Math.random()*24)*(0.6+gust),vy:(neve?22+Math.random()*20:14+Math.random()*22),rot:Math.random()*6.28,vr:(Math.random()-.5)*(neve?1.2:3.5),s:(neve?2.5+Math.random()*2.5:(tipo<.7?5:3.5)+Math.random()*4),a:.92,c:col,petal:!neve&&tipo>=.7,neve:neve}); }
 for(i=leaves.length-1;i>=0;i--){var lf=leaves[i];lf.x+=(lf.vx+Math.sin(t*.002+lf.y)*12*(0.5+gust))*dt;lf.y+=lf.vy*dt;lf.rot+=lf.vr*dt;if(lf.y>cam.y+VH+20||lf.x<cam.x-30){leaves.splice(i,1);}}
 // borboletas: vagueiam suave
 for(i=0;i<borbs.length;i++){var bo=borbs[i];bo.t+=dt;bo.ang+=Math.sin(t*.0013+bo.ph)*0.03;bo.x+=Math.cos(bo.ang)*36*dt;bo.y+=(Math.sin(bo.ang*1.4+bo.ph)*24+Math.sin(t*.004+bo.ph)*10)*dt;
  if(bo.x<40)bo.ang=0;if(bo.x>WW-40)bo.ang=Math.PI;if(bo.y<60)bo.y=60;if(bo.y>WH-60)bo.y=WH-60;}
 if(TEMA.passaros && birds.length<2 && Math.sin(t*.013+2)>0.999){birds.push({x:cam.x-40,y:cam.y+40+Math.random()*120,vx:60+Math.random()*40,ph:Math.random()*6.28,chirp:0});}
 for(i=birds.length-1;i>=0;i--){var bd=birds[i];bd.x+=bd.vx*dt;bd.y+=Math.sin(t*.005+bd.ph)*10*dt;bd.chirp-=dt;if(bd.chirp<=0){somPio();bd.chirp=1.2+Math.random();}if(bd.x>cam.x+VW+60)birds.splice(i,1);}
 for(i=estrelas.length-1;i>=0;i--){var s=estrelas[i];s.x+=s.vx*dt;s.y+=s.vy*dt;s.vy+=120*dt;s.a-=dt*.5;if(s.a<=0)estrelas.splice(i,1);}
 // ---- PROPS VIVOS: emite fumaca/faiscas + som de crepitar ----
 for(i=0;i<PROPS.length;i++){var pr=PROPS[i];
  if(pr.tipo==="fogueira"){if(Math.random()<0.55)emiteFumaca(pr.x,pr.y-16,0.7);
   if(Math.random()<0.35)faiscas.push({x:pr.x+(Math.random()-.5)*12,y:pr.y-8,vx:(Math.random()-.5)*34,vy:-(28+Math.random()*46),a:1,r:1+Math.random()*1.6});}
  else if(pr.tipo==="cabana"){if(Math.random()<0.22)emiteFumaca(pr.x+(pr.cx||24),pr.y-(pr.cy||96),0.55);}}
 if(temFogo){fogoTimer-=dt;if(fogoTimer<=0){fogoTimer=0.25+Math.random()*0.7;somEstalo();}}
 climaUpdate(dt,t); // clima: move gotas, sorteia rajadas, agenda flash/trovao (no-op se MUNDO.clima vazio)
 for(i=fumos.length-1;i>=0;i--){var fm=fumos[i];fm.y+=fm.vy*dt;fm.x+=(fm.vx+Math.sin(t*.001+fm.y)*7)*dt;fm.r+=fm.gro*dt;fm.a-=dt*0.12;if(fm.a<=0||fm.r>48)fumos.splice(i,1);}
 for(i=faiscas.length-1;i>=0;i--){var fs=faiscas[i];fs.x+=fs.vx*dt;fs.y+=fs.vy*dt;fs.vy+=42*dt;fs.a-=dt*1.1;if(fs.a<=0)faiscas.splice(i,1);}
 // poeira dos pes: sobe, expande e some rapido (gravidade leve freia a subida; atrito no vx)
 for(i=poeira.length-1;i>=0;i--){var du=poeira[i];
  du.x+=du.vx*dt;du.y+=du.vy*dt;du.vy+=6*dt;du.vx*=(1-dt*2.4);
  du.r+=du.gro*dt;du.a-=dt*0.85;if(du.a<=0)poeira.splice(i,1);}

 // ======== RENDER ========
 cx.save();cx.translate(-cam.x,-cam.y);
 // chao
 if(patG){cx.fillStyle=patG;cx.fillRect(cam.x,cam.y,VW,VH);}else{cx.fillStyle="#3f7a34";cx.fillRect(cam.x,cam.y,VW,VH);}
 desCaminho(t);
 desNuvSombra(t); // sombras de nuvem cruzando o chao (DENTRO da camera, sobre grama+trilha, sob arvores/byte)
 climaMolha(); // brilho de chao molhado (MUNDO, dentro do translate da camera; off por padrao)
 // brilho de luz do vento passando no chao
 cx.save();cx.globalCompositeOperation="lighter";
 for(i=0;i<luzChao.length;i++){var lc=luzChao[i];var lx=((t*0.012*lc.sp+lc.ph*500)%(WW+800))-400;
  var grd=cx.createRadialGradient(lx,lc.y,10,lx,lc.y,250);grd.addColorStop(0,"rgba(255,250,190,"+(0.05+0.03*gust)+")");grd.addColorStop(1,"rgba(255,250,190,0)");
  cx.fillStyle=grd;cx.beginPath();cx.ellipse(lx,lc.y,250,150,0,0,Math.PI*2);cx.fill();}
 cx.restore();
 // flores (no chao, atras dos personagens)
 for(i=0;i<FLORES.length;i++)desFlor(FLORES[i],t);
 // poeirinha dos pes (terra clara translucida) — no chao, dentro da camera, ATRAS dos personagens (y-sort vem depois)
 for(i=0;i<poeira.length;i++){var du=poeira[i];if(du.a<=0)continue;
  cx.globalAlpha=du.a;cx.fillStyle=POEIRA_COR;
  cx.beginPath();cx.arc(du.x,du.y,du.r,0,Math.PI*2);cx.fill();}
 cx.globalAlpha=1;
 // lista y-sort: arvores + chave + byte + arco
 var draws=[];
 for(i=0;i<TREES.length;i++)draws.push({y:TREES[i][1],f:(function(o){return function(){desArvore(o,t);};})(TREES[i])});
 if(OBJETIVO==="chave"&&!chave.got)draws.push({y:chave.y,f:function(){desChave(t);}});
 if(OBJETIVO==="chave")draws.push({y:arco.y,f:function(){desArco(t);}});
 draws.push({y:byte.y,f:function(){desByte(t);}});

 if(MODO_AULA){ // frutas + cesta entram no y-sort (o Byte passa na frente/atrás corretamente)
  for(var _ai=0;_ai<rItens.length;_ai++){var _it=rItens[_ai]; if(_it.got&&!_it.over)continue;
   // chave de profundidade = sy (base da árvore p/ pendurada) -> fruta na copa desenha NA FRENTE da própria árvore
   draws.push({y:(_it.sy!=null?_it.sy:_it.y),f:(function(o){return function(){desFruta(o,t);};})(_it)});}
  if(rCesta)draws.push({y:rCesta.y,f:function(){desCesta(t);}}); }
 for(i=0;i<PROPS.length;i++)draws.push({y:PROPS[i].y,f:(function(p){return function(){desProp(p,t);};})(PROPS[i])});
 for(i=0;i<npcs.length;i++)draws.push({y:npcs[i].y,f:(function(n){return function(){desNPC(n,t);};})(npcs[i])}); // NPCs no y-sort
 draws.sort(function(a,b){return a.y-b.y;});
 for(i=0;i<draws.length;i++)draws[i].f();

 if(MODO_AULA){ desFly(); desBadges(); } // frutas voando p/ a cesta + badges de número (mundo, por cima do y-sort)
 // passaros (por cima)
 for(i=0;i<birds.length;i++){var bd2=birds[i],by=bd2.y,wing=Math.sin(t*.02+bd2.ph)*6;
  if(IMG.passaro){cx.save();cx.translate(bd2.x,by);cx.scale(-0.5,0.5);cx.globalAlpha=.95;imgH(IMG.passaro,0,10,34);cx.restore();}
  else{cx.strokeStyle="#333";cx.lineWidth=2;cx.beginPath();cx.moveTo(bd2.x-8,by-wing);cx.lineTo(bd2.x,by);cx.lineTo(bd2.x+8,by-wing);cx.stroke();}}
 // borboletas (esvoacando por cima do prado)
 if(IMG.borboleta)for(i=0;i<borbs.length;i++){var bo=borbs[i];var flap=Math.abs(Math.sin(t*.02+bo.ph));
  var w=IMG.borboleta.width*26/IMG.borboleta.height;
  cx.save();cx.translate(bo.x,bo.y-Math.sin(t*.004+bo.ph)*4);cx.scale((0.45+0.55*flap)*(Math.cos(bo.ang)<0?-1:1),0.72+0.28*flap);
  cx.drawImage(IMG.borboleta,-w/2,-13,w,26);cx.restore();}
 // fumaca dos props (sobe por cima das arvores)
 for(i=0;i<fumos.length;i++){var fu=fumos[i];if(fu.r<=1)continue;cx.save();
  var fg2=cx.createRadialGradient(fu.x,fu.y,1,fu.x,fu.y,fu.r);
  fg2.addColorStop(0,"rgba(120,120,128,"+Math.max(0,fu.a)+")");fg2.addColorStop(.6,"rgba(150,150,158,"+Math.max(0,fu.a*0.6)+")");fg2.addColorStop(1,"rgba(160,160,168,0)");
  cx.fillStyle=fg2;cx.beginPath();cx.arc(fu.x,fu.y,fu.r,0,Math.PI*2);cx.fill();cx.restore();}
 cx.globalAlpha=1;
 // faiscas (brasas subindo)
 cx.save();cx.globalCompositeOperation="lighter";for(i=0;i<faiscas.length;i++){var fa=faiscas[i];
  cx.fillStyle="rgba(255,"+(150+Math.floor(Math.random()*60))+",60,"+Math.max(0,fa.a)+")";cx.beginPath();cx.arc(fa.x,fa.y,fa.r,0,Math.PI*2);cx.fill();}cx.restore();cx.globalAlpha=1;
 // folhas
 for(i=0;i<leaves.length;i++){var lf2=leaves[i];cx.save();cx.translate(lf2.x,lf2.y);cx.rotate(lf2.rot);cx.globalAlpha=lf2.a;cx.fillStyle=lf2.c;
  cx.beginPath();if(lf2.neve){cx.arc(0,0,lf2.s*.8,0,Math.PI*2);}else{cx.ellipse(0,0,lf2.s*.5,lf2.s,0,0,Math.PI*2);}cx.fill();cx.restore();cx.globalAlpha=1;}
 // estrelas da chave
 for(i=0;i<estrelas.length;i++)estrela(estrelas[i].x,estrelas[i].y,estrelas[i].r,estrelas[i].a);
 // pollen/luz
 cx.save();cx.globalCompositeOperation="lighter";for(i=0;i<pollen.length;i++){var pp=pollen[i];
  var px=pp.x+Math.sin(t*.0006+pp.f)*24,py=pp.y+Math.cos(t*.0007+pp.f)*18;var aa=.10+.18*Math.sin(t*.002+pp.f*2);
  cx.fillStyle="rgba(255,245,180,"+Math.max(0,aa)+")";cx.beginPath();cx.arc(px,py,pp.r,0,Math.PI*2);cx.fill();}cx.restore();
 cx.restore();
 climaDesenha(t); // chuva/rajadas na TELA (apos o restore do mundo, coladas na camera)
 // ---- clima/luz (tela) + CICLO DIA/NOITE ----
  desNuvCeu(t); // nuvens claras no topo do ceu (coord de TELA); o tint do ceu e a noite passam por cima logo abaixo
var lg=cx.createLinearGradient(0,0,0,VH);lg.addColorStop(0,TEMA.ceu0);lg.addColorStop(1,TEMA.ceu1);cx.fillStyle=lg;cx.fillRect(0,0,VW,VH);
 // escurece a cena a noite (azul profundo)
 if(noite>0.01){cx.fillStyle="rgba(12,18,45,"+(noite*0.58)+")";cx.fillRect(0,0,VW,VH);}
 // estrelas + lua quando anoitece
 if(noite>0.12){cx.save();
  cx.fillStyle="#ffffff";for(var si=0;si<14;si++){var sx=(si*151)%VW,sy=(si*97)%130+8;cx.globalAlpha=noite*(0.35+0.4*Math.sin(t*0.003+si*1.3));cx.fillRect(sx,sy,1.7,1.7);}
  var mx=VW*0.82,my=50;cx.globalAlpha=noite;cx.globalCompositeOperation="lighter";var mg=cx.createRadialGradient(mx,my,4,mx,my,36);mg.addColorStop(0,"rgba(220,230,255,.85)");mg.addColorStop(1,"rgba(180,200,255,0)");cx.fillStyle=mg;cx.beginPath();cx.arc(mx,my,36,0,Math.PI*2);cx.fill();
  cx.globalCompositeOperation="source-over";cx.fillStyle="#eef3ff";cx.beginPath();cx.arc(mx,my,13,0,Math.PI*2);cx.fill();cx.restore();cx.globalAlpha=1;}
 var vg=cx.createRadialGradient(VW/2,VH*.44,VH*.42,VW/2,VH*.5,VH*.95);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(6,10,25,"+(0.4+noite*0.32)+")");cx.fillStyle=vg;cx.fillRect(0,0,VW,VH);
 // raios de sol diagonais (somem a noite)
 if(noite<0.92){cx.save();cx.globalCompositeOperation="lighter";cx.globalAlpha=.05*(1-noite);cx.fillStyle="#fff3c0";
 for(i=0;i<3;i++){cx.save();cx.translate(140+i*220,0);cx.rotate(0.32);cx.fillRect(-30,-40,60,VH*1.6);cx.restore();}cx.restore();cx.globalAlpha=1;}
 // ---- HUD ----
 cx.fillStyle="rgba(8,16,30,.55)";cx.fillRect(0,0,VW,26);cx.fillStyle="#ffe38a";cx.font="bold 13px Verdana";cx.textAlign="center";
 if(OBJETIVO==="chave"){cx.fillText(hasKey?(HIST.hud_com||"Leve a chave dourada até o labirinto de pedra 🔑"):(HIST.hud||"Passeie pela floresta e pegue a chave dourada 🔑"),VW/2,17);}else if(MODO_AULA){desHUDrodada();}
 desBotaoSom();

 if(MODO_AULA) aulaOverlay(t); // comemoração de fim de rodada + tela de fim de aula (TELA; o balão do Byte fica por cima)
 // balao acima do Byte
 var _spk=balaoAlvo||byte;balaoDes(_spk.x-cam.x, _spk.y-cam.y);   // caixa acima de QUEM fala (Byte ou NPC)
 if(fim&&fimT>1.2){cx.fillStyle="rgba(6,10,22,"+Math.min(.55,(fimT-1.2)*.6)+")";cx.fillRect(0,0,VW,VH);
  cx.fillStyle="#ffe38a";cx.font="bold 22px Verdana";cx.textAlign="center";cx.fillText(HIST.fimTitulo||"✨ Fim da Etapa 1 ✨",VW/2,VH/2-10);
  cx.fillStyle="#eaf2ff";cx.font="13px Verdana";cx.fillText(HIST.ganchoProx||"Na próxima: entrar no labirinto e empurrar as pedras-seta!",VW/2,VH/2+18);}
 climaFlash(); // FLASH do raio por CIMA de tudo (ultimo desenho do frame)
 requestAnimationFrame(frame);
}
// cor da placa de nome: Byte tem a sua; cada NPC ganha uma cor ESTAVEL pelo nome
function corPlaca(nome){ if(nome==="Byte")return "#3ec6a6";
 var h=0;for(var i=0;i<nome.length;i++)h=(h*31+nome.charCodeAt(i))>>>0;
 var HS=["#e08a3c","#5aa0e0","#c56ad0","#7bb84a","#e0693c","#4ab0c0"];return HS[h%HS.length]; }
// caixa de dialogo RPG. (ancX,feetY) = base do personagem na TELA
function balaoDes(ancX,feetY){ if(!(balaoT>0&&balaoFull))return;
 var PAD=8,LH=15,MAXW=238,GAP=9,TOPO=30,fundo="rgba(18,26,48,.92)"; // TOPO=abaixo da HUD (26px)
 // 1) quebra o TEXTO COMPLETO (box FIXO: nao pula enquanto digita)
 cx.font="bold 12px Verdana";var words=balaoFull.split(" "),linhas=[],cur="";
 for(var i=0;i<words.length;i++){var tt=cur?cur+" "+words[i]:words[i];
  if(cx.measureText(tt).width>MAXW&&cur){linhas.push(cur);cur=words[i];}else cur=tt;}
 if(cur)linhas.push(cur);
 // 2) medidas
 var bw=0;for(i=0;i<linhas.length;i++)bw=Math.max(bw,cx.measureText(linhas[i]).width);
 bw=Math.min(bw+PAD*2,VW-16);var bh=linhas.length*LH+PAD*2;
 // 3) ACIMA da cabeca; se nao couber (perto do topo), CAI abaixo do personagem
 var headY=feetY-50,acima=(headY-GAP-bh)>=TOPO;
 var ly=acima?(headY-GAP-bh):Math.min(feetY+GAP,VH-bh-8);
 var lx=Math.max(8,Math.min(VW-bw-8,ancX-bw/2));
 var tx=Math.max(lx+20,Math.min(lx+bw-20,ancX)); // cauda presa na caixa
 // 4) aparece com leve fade+subida
 var ap=balaoAppear;cx.save();cx.globalAlpha=ap;cx.translate(0,acima?(1-ap)*6:-(1-ap)*6);
 // 5) corpo: fundo translucido + BORDA DUPLA arredondada
 roundR(lx,ly,bw,bh,8);cx.fillStyle=fundo;cx.fill();
 cx.lineWidth=2.5;cx.strokeStyle="rgba(196,214,250,.92)";cx.stroke();
 roundR(lx+3,ly+3,bw-6,bh-6,6);cx.lineWidth=1;cx.strokeStyle="rgba(120,150,210,.5)";cx.stroke();
 // 6) cauda POR CIMA (cobre a costura) apontando pro personagem
 cx.fillStyle=fundo;cx.beginPath();
 if(acima){cx.moveTo(tx-9,ly+bh-2);cx.lineTo(tx+9,ly+bh-2);cx.lineTo(tx,ly+bh+12);}
 else{cx.moveTo(tx-9,ly+2);cx.lineTo(tx+9,ly+2);cx.lineTo(tx,ly-12);}
 cx.closePath();cx.fill();
 cx.lineWidth=2.5;cx.strokeStyle="rgba(196,214,250,.92)";cx.beginPath();
 if(acima){cx.moveTo(tx-9,ly+bh-2);cx.lineTo(tx,ly+bh+12);cx.lineTo(tx+9,ly+bh-2);}
 else{cx.moveTo(tx-9,ly+2);cx.lineTo(tx,ly-12);cx.lineTo(tx+9,ly+2);}
 cx.stroke();
 // 7) TEXTO letra a letra (substring sobre linhas FIXAS -> nao treme)
 var vis=Math.floor(balaoN),used=0;cx.textAlign="left";cx.fillStyle="#f2f6ff";
 for(i=0;i<linhas.length;i++){var ln=linhas[i];
  if(used<vis)cx.fillText(ln.substr(0,Math.min(ln.length,vis-used)),lx+PAD,ly+PAD+11+i*LH);
  used+=ln.length+1;}
 // 8) SETINHA piscando quando terminou (deterministica: sin de acumulador de tempo)
 if(balaoFimTxt){var pb=0.3+0.7*(0.5+0.5*Math.sin(balaoBlink*6));
  cx.globalAlpha=ap*pb;cx.fillStyle="#ffe38a";cx.textAlign="center";cx.font="bold 10px Verdana";
  cx.fillText("▼",lx+bw-10,ly+bh-5);cx.globalAlpha=ap;}
 // 9) PLACA com o NOME (topo-esq, colorida, encaixada na borda de cima)
 cx.font="bold 10px Verdana";cx.textAlign="left";var nm=balaoNome,nw=cx.measureText(nm).width;
 var pw=nw+12,ph=15,plx=lx+9,ply=ly-ph+5;
 roundR(plx,ply,pw,ph,5);cx.fillStyle=corPlaca(nm);cx.fill();
 cx.lineWidth=1.5;cx.strokeStyle="rgba(0,0,0,.28)";cx.stroke();
 cx.fillStyle="rgba(255,255,255,.28)";cx.fillRect(plx+3,ply+2,pw-6,2);
 cx.fillStyle="#10202e";cx.fillText(nm,plx+6,ply+11);
 cx.restore();cx.globalAlpha=1; }
function roundR(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.lineTo(x+w-r,y);cx.quadraticCurveTo(x+w,y,x+w,y+r);cx.lineTo(x+w,y+h-r);cx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);cx.lineTo(x+r,y+h);cx.quadraticCurveTo(x,y+h,x,y+h-r);cx.lineTo(x,y+r);cx.quadraticCurveTo(x,y,x+r,y);cx.closePath();}
if(window.speechSynthesis)speechSynthesis.onvoiceschanged=function(){};
/* QA hooks */
window._qaMove=function(dx,dy){var nx=byte.x+dx,ny=byte.y+dy;if(!bloqueado(nx,byte.y))byte.x=nx;if(!bloqueado(byte.x,ny))byte.y=ny;};
window._qaTeleport=function(x,y){byte.x=x;byte.y=y;var c=cellCam();cam.x=c[0];cam.y=c[1];};
window._qaState=function(){return {hasKey:hasKey,fim:fim,bx:Math.round(byte.x),by:Math.round(byte.y)};};
</script></body></html>"""
HTML=HTML.replace("__SRC_JSON__",SRC_JSON).replace("__FALAS_JSON__",FALAS_JSON).replace("__THEME_JS__",THEMEJS)
HTML=HTML.replace("__TITULO__",CFG["titulo"]).replace("__EMOJI__",CFG["emoji"])
# standalone: subtitulos da floresta (o montador injeta __SUB_PC__/__SUB_TOUCH__ dos dados)
HTML=HTML.replace("__SUB_PC__","use as SETAS do teclado p/ o Byte andar &#183; pegue a chave dourada &#128273; &#183; leve-a at&#233; o labirinto")
HTML=HTML.replace("__SUB_TOUCH__","use o D-pad p/ o Byte andar &#183; pegue a chave dourada &#128273; &#183; leve-a at&#233; o labirinto")
out=os.path.join(S,"byte-%s.html"%TEMA)
open(out,"w",encoding="utf-8").write(HTML)
print("OK ->",out,"(",round(len(HTML)/1024),"KB ) TEMA:",TEMA,"imgs:",sorted(SRCJS.keys()),"falas:",sorted(FAL.keys()))
