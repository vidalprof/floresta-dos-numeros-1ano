"use strict";
/* ============ Confeitaria Mágica — Divisão 5º ano · MOTOR ============ */
function $(id){return document.getElementById(id);}
function embaralhar(a){var i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(rnd()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
var _seed=1;function rnd(){_seed=(_seed*9301+49297)%233280;return _seed/233280;}
function reseed(n){_seed=n||((new Date()).getTime()%233280)+1;}
function plural(n,s,p){return n===1?("1 "+s):(n+" "+p);}
function pluralG(n,g,s,p){return n===1?((g==="f"?"uma ":"um ")+s):(n+" "+p);}
var NUMEXT=["zero","um","dois","três","quatro","cinco","seis","sete","oito","nove","dez","onze","doze","treze","quatorze","quinze","dezesseis","dezessete","dezoito","dezenove","vinte","vinte e um","vinte e dois","vinte e três","vinte e quatro"];
function numExt(n){return NUMEXT[n]!==undefined?NUMEXT[n]:(""+n);}
function agoraMs(){try{return (new Date()).getTime();}catch(e){return 0;}}

/* ============ NARRAÇÃO (audio Antonio embutido; não bloqueia o Próximo) ============ */
var VOZ_MUDA=false;try{VOZ_MUDA=localStorage.getItem("cm_mudo")==="1";}catch(e){}
var _aud=null,_ultima="",_falaSeq=0;
function _chaveVoz(t){var s=(""+t).replace(/\s+/g," ").replace(/^\s+|\s+$/g,"");var h=5381,i;for(i=0;i<s.length;i++){h=((h*33)+s.charCodeAt(i))>>>0;}return "v"+h.toString(36);}
function limparFala(t){t=(""+t).replace(/<[^>]+>/g," ");t=t.replace(/[_*#~|<>=\[\]{}]/g," ");
 t=t.replace(/\bdivisao\b/gi,"divisão").replace(/\bmultiplicacao\b/gi,"multiplicação");
 t=t.replace(/\s+([,.!?:])/g,"$1").replace(/\s\s+/g," ").replace(/^\s+|\s+$/g,"");
 if(t&&".!?:".indexOf(t.charAt(t.length-1))<0)t+=".";return t;}
function pararFala(){_falaSeq++;if(_aud){try{_aud.pause();_aud.src="";}catch(e){}_aud=null;}}
function falar(txt,cb){pararFala();_ultima=txt;var meu=_falaSeq;if(VOZ_MUDA){if(cb)setTimeout(cb,10);return;}
 var ch=_chaveVoz(limparFala(txt));var src=AUDIO_TXT[ch];
 if(!src){if(cb)setTimeout(cb,Math.min(4000,600+limparFala(txt).length*55));return;}
 try{_aud=new Audio(src);_aud.onended=function(){if(meu===_falaSeq&&cb)cb();};
 _aud.onerror=function(){if(meu===_falaSeq&&cb)cb();};_aud.play()["catch"]?_aud.play()["catch"](function(){}):0;}
 catch(e){if(cb)setTimeout(cb,10);}}
function repetirFala(){if(_ultima){VOZ_MUDA=false;falar(_ultima);}}
function alternarMudo(){VOZ_MUDA=!VOZ_MUDA;try{localStorage.setItem("cm_mudo",VOZ_MUDA?"1":"0");}catch(e){}
 $("btMudo").innerHTML=VOZ_MUDA?"&#128263;":"&#128266;";if(VOZ_MUDA)pararFala();}

/* ============ NÍVEIS / CONQUISTAS ============ */
var NIVEIS=[{p:0,n:"Ajudante de Confeitaria"},{p:14,n:"Confeiteiro Aprendiz"},{p:30,n:"Confeiteiro"},{p:48,n:"Mestre Confeiteiro"},{p:66,n:"Grande Chef da Divisão"}];
function nivelIdx(p){var i,r=0;for(i=0;i<NIVEIS.length;i++){if(p>=NIVEIS[i].p)r=i;}return r;}
var CONQUISTAS=[
 {id:"c1",cond:function(s){return s.acertosTot>=1;}},
 {id:"c2",cond:function(s){return s.maxStreak>=3;}},
 {id:"c3",cond:function(s){return s.feitas>=1;}},
 {id:"c4",cond:function(s){return s.feitas>=4;}},
 {id:"c5",cond:function(s){return s.maxStreak>=8;}},
 {id:"c6",cond:function(s){return s.feitas>=PARADAS.length;}}];

/* ============ CONTEÚDO — 8 paradas + 2 jogos ============ */
/* tipos: repartir(concreto), escolha(situação/inversa/mista/resto/2alg), tabuada, memoria, montar */
var PARADAS=[
 {ch:"p1",ilha:"iPrato",med:0,titulo:"Biscoitos nos pratos",
  hist:"Bem-vindo à Confeitaria Mágica! Sou o Chef Confeito. Nossa 1ª tarefa: repartir os biscoitos em partes iguais nos pratos. Repartir igual é dividir!",
  gancho:"Ótimo! Agora vamos ver quantas caixas cabem os doces.",
  tipo:"repartir",doce:"dBiscoito",
  desafios:[{tot:6,gr:2},{tot:8,gr:4},{tot:10,gr:5},{tot:12,gr:3},{tot:9,gr:3},{tot:15,gr:5}]},
 {ch:"p2",ilha:"iCaixas",med:1,titulo:"Encher as caixas",
  hist:"Agora o contrário do prato: quantas caixas dá pra encher? Se cada caixa leva um tanto, quantas caixas cabem?",
  gancho:"Show! Chegou um pedido grande pra festa. Vamos ler o problema.",
  tipo:"repartir",doce:"dCupcake",modo:"caixas",
  desafios:[{tot:12,gr:6},{tot:15,gr:5},{tot:20,gr:4},{tot:18,gr:3},{tot:14,gr:7},{tot:24,gr:8}]},
 {ch:"p3",ilha:"iBolo",med:2,titulo:"O pedido da festa",
  hist:"Chegaram os pedidos da Festa da Cidade! Leia cada situação e descubra a divisão certa.",
  gancho:"Você é rápido! Agora um segredo dos confeiteiros: multiplicar e dividir são contrários.",
  tipo:"escolha",
  desafios:[
   {en:"A festa tem 4 mesas. O Chef fez 20 brigadeiros para repartir igualmente. Quantos em cada mesa?",r:5,d:20,v:4},
   {en:"São 24 biscoitos em 6 sacolinhas iguais. Quantos biscoitos por sacolinha?",r:4,d:24,v:6},
   {en:"A dona tem 18 docinhos e dá 3 para cada criança. Para quantas crianças dá?",r:6,d:18,v:3},
   {en:"São 30 balas em 5 potes iguais. Quantas balas por pote?",r:6,d:30,v:5},
   {en:"Há 16 fatias de bolo, 2 para cada visitante. Para quantos visitantes?",r:8,d:16,v:2},
   {en:"São 21 pães em 3 cestas iguais. Quantos pães por cesta?",r:7,d:21,v:3}]},
 {ch:"p4",ilha:"iLivro",med:3,titulo:"A receita e o contrário",
  hist:"Segredo da receita: a divisão é o contrário da multiplicação! Se você sabe a de vezes, sabe a de dividir.",
  gancho:"Boa memória! Que tal um joguinho pra descansar?",
  tipo:"escolha",
  desafios:[
   {en:"3 bandejas com 4 biscoitos cada dão 12. Então 12 ÷ 4 = ?",r:3,mul:"3 × 4 = 12"},
   {en:"5 caixas com 6 doces cada dão 30. Então 30 ÷ 6 = ?",r:5,mul:"5 × 6 = 30"},
   {en:"Se 7 × 3 = 21, quanto é 21 ÷ 7?",r:3,mul:"7 × 3 = 21"},
   {en:"Se 6 × 8 = 48, quanto é 48 ÷ 8?",r:6,mul:"6 × 8 = 48"},
   {en:"Se 4 × 9 = 36, quanto é 36 ÷ 4?",r:9,mul:"4 × 9 = 36"},
   {en:"Se 8 × 5 = 40, quanto é 40 ÷ 5?",r:8,mul:"8 × 5 = 40"}]},
 {ch:"j1",ilha:"iCupcake",med:-1,titulo:"Memória da Confeitaria",jogo:true,
  hist:"Vira as cartas e junte cada conta de vezes com a divisão do contrário que dá o mesmo doce!",
  gancho:"Que memória boa! Agora vamos calcular de cabeça, usando a tabuada.",
  tipo:"memoria",pares:[["3 × 4","12 ÷ 4"],["5 × 6","30 ÷ 6"],["7 × 3","21 ÷ 7"],["6 × 8","48 ÷ 8"]]},
 {ch:"p5",ilha:"iVitrine",med:4,titulo:"A tabuada da vitrine",
  hist:"Pra dividir de cabeça, pense na tabuada: divisor vezes quanto dá o dividendo? A vitrine te ajuda!",
  gancho:"Rápido como um confeiteiro! Agora o desafio: é de multiplicar ou de repartir?",
  tipo:"tabuada",
  desafios:[{d:24,v:6},{d:35,v:7},{d:42,v:6},{d:48,v:8},{d:27,v:9},{d:56,v:7}]},
 {ch:"p6",ilha:"iBalanca",med:5,titulo:"Multiplicar ou repartir?",
  hist:"Cuidado agora: em cada pedido, decida se é pra JUNTAR grupos iguais (multiplicar) ou REPARTIR em partes iguais (dividir).",
  gancho:"Você pensa como um mestre! Vamos montar a conta certa no próximo jogo.",
  tipo:"escolha",
  desafios:[
   {en:"Cada caixa tem 8 doces. São 4 caixas. Quantos doces ao todo?",r:32,op:"×"},
   {en:"São 32 doces repartidos em 4 caixas iguais. Quantos por caixa?",r:8,op:"÷"},
   {en:"6 amigos comeram 3 biscoitos cada. Quantos biscoitos ao todo?",r:18,op:"×"},
   {en:"São 18 biscoitos repartidos entre 6 amigos. Quantos para cada um?",r:3,op:"÷"},
   {en:"5 bandejas com 7 cupcakes cada. Quantos cupcakes ao todo?",r:35,op:"×"},
   {en:"São 35 cupcakes em 5 bandejas iguais. Quantos por bandeja?",r:7,op:"÷"}]},
 {ch:"j2",ilha:"iCupcake",med:-1,titulo:"Monte a Conta",jogo:true,
  hist:"Arraste os números para montar a divisão certa. Lembre: na divisão a ordem importa!",
  gancho:"Perfeito! Agora, e quando não dá pra repartir tudo igual? Sobra!",
  tipo:"montar",
  desafios:[{d:24,v:6,r:4},{d:20,v:5,r:4},{d:18,v:3,r:6},{d:40,v:8,r:5},{d:30,v:6,r:5}]},
 {ch:"p7",ilha:"iCupcake",med:6,titulo:"O docinho que sobra",
  hist:"Nem sempre dá pra repartir tudo igual. O que não dá é o RESTO! Diga quanto fica em cada e quanto sobra.",
  gancho:"Você entendeu o resto! Falta só a grande encomenda final.",
  tipo:"resto",
  desafios:[{d:13,v:4,q:3,s:1},{d:17,v:5,q:3,s:2},{d:22,v:4,q:5,s:2},{d:10,v:3,q:3,s:1},{d:19,v:6,q:3,s:1},{d:25,v:7,q:3,s:4}]},
 {ch:"p8",ilha:"iCoroa",med:7,titulo:"A grande encomenda",
  hist:"A encomenda final da festa! Números maiores: reparta as dezenas e depois as unidades. Você consegue!",
  gancho:"Você conseguiu! A Festa da Cidade vai ser um sucesso!",
  tipo:"escolha",
  desafios:[
   {en:"48 ÷ 4 = ?",r:12},{en:"36 ÷ 3 = ?",r:12},{en:"60 ÷ 5 = ?",r:12},
   {en:"84 ÷ 4 = ?",r:21},{en:"55 ÷ 5 = ?",r:11},{en:"72 ÷ 6 = ?",r:12}]}
];
var ELOGIOS=["Isso!","Muito bem!","Boa!","Perfeito!","Mandou bem!","Show!","Uau!","Você é craque!","Delícia de resposta!","Certíssimo!"];
var FESTApool=["ACERTOU!","MUITO BEM!","BOA!","ISSO!","PERFEITO!","SHOW!","UAU!"];

/* ============ ESTADO ============ */
var VALIDADE_MIN=70;
var S={nome:"",pontos:0,feitasMap:{},stats:{},conq:{},maxStreak:0,acertosTot:0};
var atual=null,idx=0,streak=0,errosSeg=0,facil=false,ERROS=[],modoTreino=false,extraOn=false,runAc=0,reforcoOn=false;
function feitas(){var k,c=0;for(k in S.feitasMap)if(S.feitasMap[k])c++;return c;}
function salvar(){try{var o={nome:S.nome,pontos:S.pontos,feitasMap:S.feitasMap,stats:S.stats,conq:S.conq,maxStreak:S.maxStreak,acertosTot:S.acertosTot,t:agoraMs()};localStorage.setItem("cm_prog",JSON.stringify(o));}catch(e){}}
function carregar(){try{var r=localStorage.getItem("cm_prog");if(!r)return false;var d=JSON.parse(r);if(!d.t||(agoraMs()-d.t)>VALIDADE_MIN*60000){localStorage.removeItem("cm_prog");return false;}
 S.nome=d.nome||"";S.pontos=d.pontos||0;S.feitasMap=d.feitasMap||{};S.stats=d.stats||{};S.conq=d.conq||{};S.maxStreak=d.maxStreak||0;S.acertosTot=d.acertosTot||0;return true;}catch(e){return false;}}
function apagar(){try{localStorage.removeItem("cm_prog");}catch(e){}S={nome:"",pontos:0,feitasMap:{},stats:{},conq:{},maxStreak:0,acertosTot:0};}

/* ============ TELA INICIAL ============ */
function telaInicial(){pararFala();var tem=carregar();var h="";
 h+='<img class="capaimg" src="'+IMG.capa+'" alt="Confeitaria Mágica">';
 h+='<h1>Confeitaria Mágica</h1><div class="sub">A aventura da Divisão · 5º ano</div>';
 if(tem&&feitas()>0){
  h+='<div class="lead">Que bom te ver de novo, <b>'+esc(S.nome)+'</b>! Você já tem '+plural(S.pontos,"ponto","pontos")+' e completou '+plural(feitas(),"parada","paradas")+'.</div>';
  h+='<button class="btn pulsa" onclick="irMapa()">&#9654; Continuar a aventura</button>';
  h+='<div style="text-align:center"><button class="btn sec" onclick="confReset()">&#128260; Começar do zero</button></div>';
 }else{
  h+='<div class="lead" id="lead">Oi! Eu sou o <b>Chef Confeito</b>. Preciso da sua ajuda pra preparar os doces da Festa da Cidade — e tudo tem que ser repartido em partes iguais! Escreva seu nome e vamos começar.</div>';
  h+='<input class="campo" id="inpNome" placeholder="Digite seu nome" maxlength="16">';
  h+='<button class="btn pulsa" onclick="comecar()">Começar a aventura! &#128640;</button>';
 }
 $("app").innerHTML=h;
 if(!(tem&&feitas()>0))falar("Oi! Eu sou o Chef Confeito. Preciso da sua ajuda pra preparar os doces da Festa da Cidade, e tudo tem que ser repartido em partes iguais! Escreva seu nome e toque em começar.");
}
function comecar(){var el=$("inpNome");S.nome=el&&el.value?el.value.replace(/^\s+|\s+$/g,"").substring(0,16):"";irMapa();}
function confReset(){if(confirm("Começar tudo de novo? Você vai perder o progresso desta aula."))apagar(),telaInicial();}

/* ============ MAPA ============ */
function irMapa(){pararFala();salvar();desenharMapa();var f=feitas();
 var t=f===0?("Bem-vindo à Confeitaria, "+(S.nome||"chef")+"! Siga a trilha e complete cada parada pra abrir a próxima."):
        (f>=PARADAS.length?"Você completou tudo! Toque no troféu dourado pra sua festa!":"Você já preparou "+plural(f,"parada","paradas")+"! Continue na parada que está brilhando.");
 falar(t);}
function nivelImg(){return IMG.emb[nivelIdx(S.pontos)];}
function desenharMapa(){var h="",i;
 h+='<div class="topbar"><img src="'+nivelImg()+'"><div><div class="niv">'+NIVEIS[nivelIdx(S.pontos)].n+'</div><div class="xpbar"><i style="width:'+Math.min(100,S.pontos)+'%"></i></div></div><div class="niv">'+plural(S.pontos,"ponto","pontos")+'</div></div>';
 var f=feitas(),tot=PARADAS.length,rimg=IMG.rec[f<tot/3?0:(f<2*tot/3?1:2)];
 h+='<div class="card recomp"><img src="'+rimg+'" alt="bolo"><div class="prog"><i style="width:'+Math.round(f/tot*100)+'%"></i></div><div class="contparada">'+plural(f,"parada preparada","paradas preparadas")+' de '+tot+'</div>';
 h+='<div style="text-align:center;font-weight:bold;color:#ffd9a8;margin-top:4px">A aventura de '+esc(S.nome||"você")+'!</div>';
 h+='<button class="somap" onclick="narrarMapa()">&#128266;</button></div>';
 h+='<ul class="trilha">';
 for(i=0;i<PARADAS.length;i++){var p=PARADAS[i],st=(S.feitasMap[p.ch]?"feita":(desbloq(i)?"atual":"trancada"));
  var lado=(i%2===0?"lz":"rz");
  h+='<li class="no '+lado+' '+(st==="atual"?"atual":(st==="trancada"?"trancada":""))+'" style="-webkit-animation-delay:'+(i*0.06)+'s;animation-delay:'+(i*0.06)+'s">';
  h+='<div class="ilhawrap">';
  h+='<img class="ilha" src="'+IMG[p.ilha]+'" onclick="'+(st==="trancada"?"avisoTranca()":"abrirParada('+i+')")+'" alt="'+esc(p.titulo)+'">';
  if(st==="atual")h+='<img class="masccaminha" src="'+IMG.mFeliz+'">';
  if(st==="trancada")h+='<span class="cad">&#128274;</span>';
  h+='</div>';
  h+='<span class="nomeparada">'+(p.jogo?"&#127918; ":"")+esc(p.titulo)+'</span>';
  if(st==="atual")h+='<span class="aqui">você está aqui!</span>';
  if(st==="feita")h+='<span class="check">Concluída &#10003;</span>';
  h+='</li>';
  if(i<PARADAS.length-1)h+='<div class="conector '+(i%2===0?"lr":"rl")+' '+(S.feitasMap[p.ch]?"feito":"")+'"></div>';
 }
 h+='</ul>';
 var todas=f>=PARADAS.length;
 h+='<div class="no"><div class="ilhawrap"><img class="ilha'+(todas?"":" ")+'" src="'+IMG.trofeu+'" style="'+(todas?"":"-webkit-filter:grayscale(1) brightness(.7);filter:grayscale(1) brightness(.7)")+'" onclick="'+(todas?"grandeFinal()":"avisoTrofeu()")+'">'+(todas?"":'<span class="cad">&#128274;</span>')+'</div><span class="nomeparada">Diploma de Mestre &#127891;</span></div>';
 h+='<div style="text-align:center;margin-top:10px"><button class="btn sec" onclick="verMedalhas()">&#127941; Minhas Medalhas</button>';
 if(ERROS.length>0)h+=' <button class="btn sec pulsa" onclick="treinarErros()">&#9999; Treinar Erros ('+ERROS.length+')</button>';
 if(todas)h+=' <button class="btn sec" onclick="relatorio()">&#128202; Relatório</button>';
 h+='</div>';
 $("app").innerHTML=h;window.scrollTo(0,0);
}
function desbloq(i){if(i===0)return true;return !!S.feitasMap[PARADAS[i-1].ch];}
function narrarMapa(){var f=feitas();falar(f===0?"Siga a trilha, "+(S.nome||"chef")+"! Complete cada parada pra abrir a próxima e chegar ao diploma.":"Você já preparou "+plural(f,"parada","paradas")+"! Falta pouco pra virar Mestre da Divisão.");}
function avisoTranca(){falar("Essa parada ainda está trancada! Termine a parada anterior pra abrir esta.");}
function avisoTrofeu(){falar("Complete todas as paradas pra ganhar o Diploma de Mestre Confeiteiro!");}

/* ============ FASE ============ */
function abrirParada(i){atual=PARADAS[i];idx=0;streak=0;errosSeg=0;facil=false;extraOn=false;modoTreino=false;reseed(i*97+7);
 introFase();}
function introFase(){var p=atual,h="";
 h+='<div style="text-align:center"><img src="'+IMG[p.ilha]+'" style="height:130px;width:auto" alt=""></div>';
 h+='<h1 style="font-size:22px">'+esc(p.titulo)+'</h1>';
 h+='<div class="balao"><img src="'+IMG.mExplica+'" style="height:60px;width:auto;float:left;margin-right:8px">'+esc(p.hist)+'</div>';
 h+='<button class="btn pulsa" id="btIni" onclick="rodarFase()">Começar! &#9654;</button>';
 $("app").innerHTML=h;window.scrollTo(0,0);
 falar(p.hist);
}
function rodarFase(){idx=0;streak=0;runAc=0;
 if(atual.tipo==="memoria"){jogoMemoria();return;}
 proximoDesafio();
}
function totalDesafios(){return atual.desafios?atual.desafios.length:0;}
function proximoDesafio(){pararFala();
 if(idx>=totalDesafios()){fimFase();return;}
 renderDesafio(atual.desafios[idx],idx);
}
function cabecalhoDesafio(){return '<div class="contparada">Desafio '+(idx+1)+' de '+totalDesafios()+'</div><div class="prog"><i style="width:'+Math.round(idx/totalDesafios()*100)+'%"></i></div>';}

/* -- render por tipo -- */
function renderDesafio(d,i){
 if(atual.tipo==="repartir")return rDivRepartir(d);
 if(atual.tipo==="tabuada")return rTabuada(d);
 if(atual.tipo==="resto")return rResto(d);
 if(atual.tipo==="montar")return rMontar(d);
 return rEscolha(d);
}
function opcoesNum(certa,min){var set={},arr=[],tent=0;set[certa]=1;arr.push(certa);
 while(arr.length<4&&tent<50){tent++;var delta=Math.floor(rnd()*5)-2;if(delta===0)delta=1;var c=certa+delta;if(c<(min||0)||set[c])continue;set[c]=1;arr.push(c);}
 return embaralhar(arr);
}
function botoesOpcoes(opts,onclick){var h='<div class="opcoes">',i;for(i=0;i<opts.length;i++)h+='<button class="op" onclick="'+onclick+'('+opts[i]+',this)">'+opts[i]+'</button>';return h+'</div>';}

function rEscolha(d){var h=cabecalhoDesafio();
 h+='<div class="balao"><img src="'+IMG.mFala+'" style="height:52px;width:auto;float:left;margin-right:8px"><span class="enun" style="display:block;text-align:left;font-size:17px;margin:0">'+esc(d.en)+'</span></div>';
 if(d.mul)h+='<div class="dica">Dica: '+d.mul+'</div>';
 if(!facil&&d.op)h+='<div class="dica">É de juntar grupos iguais (× ) ou de repartir igual (÷)?</div>';
 var opts=facil?opcoesNum(d.r,0):opcoesNum(d.r,0);
 h+=botoesOpcoes(opts,"respEscolha");
 $("app").innerHTML=h;window.scrollTo(0,0);falar(d.en);
 window._d=d;
}
function respEscolha(v,el){if(v===window._d.r)acerto(explicaEscolha(window._d));else erro(el,window._d);}
function explicaEscolha(d){if(d.mul)return "A divisão é o contrário da multiplicação. Como "+d.mul+", então dividindo dá "+d.r+".";
 if(d.op==="×")return "Aqui juntamos grupos iguais, então é multiplicar. A resposta é "+d.r+".";
 if(d.op==="÷")return "Aqui repartimos em partes iguais, então é dividir. A resposta é "+d.r+".";
 if(d.d&&d.v)return "Repartir "+d.d+" em "+d.v+" partes iguais dá "+d.r+". Escrevemos "+d.d+" dividido por "+d.v+" igual a "+d.r+".";
 return "Isso mesmo, a resposta é "+d.r+"!";}

function rDivRepartir(d){var caixas=atual.modo==="caixas";var h=cabecalhoDesafio();
 var pergunta=caixas?("Temos "+d.tot+" doces. Cada caixa leva "+d.gr+". Quantas caixas dá pra encher?"):("Reparta "+d.tot+" biscoitos igualmente em "+d.gr+" pratos. Quantos em cada prato?");
 h+='<div class="enun">'+esc(pergunta)+'</div>';
 var img=IMG[atual.doce]||IMG.dBiscoito,i;
 h+='<div class="cena">';
 if(caixas){for(i=0;i<d.tot;i++)h+='<img class="doce" src="'+img+'">';}
 else{var per=d.tot/d.gr;for(i=0;i<d.gr;i++){h+='<span class="grupo"><img class="doce" src="'+IMG.dPrato+'" style="height:30px"><br>';var j;for(j=0;j<(facil?per:0);j++)h+='<img class="doce" src="'+img+'">';h+='</span>';}}
 h+='</div>';
 var ans=caixas?(d.tot/d.gr):(d.tot/d.gr);
 h+='<div class="dica">'+(caixas?("Veja quantos grupos de "+d.gr+" cabem em "+d.tot+"."):("Divida "+d.tot+" por "+d.gr+"."))+'</div>';
 h+=botoesOpcoes(opcoesNum(ans,1),"respRepartir");
 $("app").innerHTML=h;window.scrollTo(0,0);window._d=d;window._ans=ans;falar(pergunta);
}
function respRepartir(v,el){var caixas=atual.modo==="caixas";if(v===window._ans)acerto(caixas?("Cabem "+window._ans+" caixas! "+window._d.tot+" dividido por "+window._d.gr+" é "+window._ans+"."):("São "+window._ans+" em cada prato! "+window._d.tot+" dividido por "+window._d.gr+" é "+window._ans+"."));else erro(el,window._d);}

function rTabuada(d){var h=cabecalhoDesafio();
 h+='<div class="enun">'+d.d+' &divide; '+d.v+' = ?</div>';
 h+='<div class="dica">Pense: '+d.v+' vezes quanto dá '+d.d+'?</div>';
 h+='<div class="tabuada" id="tab">';var k;for(k=1;k<=10;k++)h+='<span id="tb'+k+'">'+d.v+'×'+k+'='+(d.v*k)+'</span>';h+='</div>';
 h+=botoesOpcoes(opcoesNum(d.d/d.v,1),"respTab");
 $("app").innerHTML=h;window.scrollTo(0,0);window._d=d;window._ans=d.d/d.v;falar(d.d+" dividido por "+d.v+". Use a tabuada do "+d.v+".");
}
function respTab(v,el){if(v===window._ans)acerto(window._d.v+" vezes "+window._ans+" é "+window._d.d+", então "+window._d.d+" dividido por "+window._d.v+" é "+window._ans+"!");else{var t=$("tb"+window._ans);if(t)t.className="on";erro(el,window._d);}}

function rResto(d){var h=cabecalhoDesafio();
 h+='<div class="enun">'+d.d+' doces em '+d.v+' pratos iguais.<br>Quantos em cada prato?</div>';
 h+='<div class="dica">Reparta o máximo igual. O que não dá é a sobra (resto).</div>';
 h+=botoesOpcoes(opcoesNum(d.q,1),"respResto1");
 $("app").innerHTML=h;window.scrollTo(0,0);window._d=d;falar(d.d+" doces em "+d.v+" pratos iguais. Quantos em cada prato?");
}
function respResto1(v,el){if(v===window._d.q){falar("Isso! "+window._d.q+" em cada. E quantos sobram?");var h=cabecalhoDesafio();h+='<div class="enun">Certo, '+window._d.q+' em cada prato!<br>Agora: quantos doces <b>sobram</b>?</div>';h+='<div class="dica">'+window._d.v+' × '+window._d.q+' = '+(window._d.v*window._d.q)+'. Falta chegar em '+window._d.d+'.</div>';h+=botoesOpcoes(opcoesNum(window._d.s,0),"respResto2");$("app").innerHTML=h;}else erro(el,window._d);}
function respResto2(v,el){if(v===window._d.s)acerto(window._d.d+" dividido por "+window._d.v+" dá "+window._d.q+" e sobra "+window._d.s+". Esse é o resto!");else erro(el,window._d);}

function rMontar(d){var h=cabecalhoDesafio();
 h+='<div class="enun">Monte a conta certa!<br>'+d.d+' repartido em '+d.v+' partes.</div>';
 h+='<div class="dica">Na divisão a ordem importa: o total vem primeiro.</div>';
 h+='<div style="text-align:center;font-size:26px;font-weight:bold;margin:10px">? &divide; ? = '+d.r+'</div>';
 h+='<div class="enun" style="font-size:16px">Qual conta está certa?</div>';
 var certo=d.d+" ÷ "+d.v,errado=d.v+" ÷ "+d.d;var opts=embaralhar([certo,errado]);
 h+='<div class="opcoes">';for(var i=0;i<opts.length;i++)h+='<button class="op" style="font-size:20px" onclick="respMontar(\''+opts[i]+'\',this)">'+opts[i]+'</button>';h+='</div>';
 $("app").innerHTML=h;window.scrollTo(0,0);window._d=d;window._cert=certo;falar("Monte a divisão certa: "+d.d+" repartido em "+d.v+" partes.");
}
function respMontar(v,el){if(v===window._cert)acerto("Certo! "+window._d.d+" dividido por "+window._d.v+" dá "+window._d.r+". O total sempre vem primeiro na divisão.");else erro(el,window._d);}

/* ============ ACERTO / ERRO / ADAPTATIVO ============ */
function acerto(explica){pararFala();S.acertosTot++;streak++;errosSeg=0;runAc++;
 var pts=2+(streak>=3?1:0);S.pontos+=pts;
 var st=atual.stats||0;if(!S.stats[atual.ch])S.stats[atual.ch]={a:0,e:0};S.stats[atual.ch].a++;
 if(streak>S.maxStreak)S.maxStreak=streak;
 carimbo();confete(16);
 var el=ELOGIOS[Math.floor(rnd()*ELOGIOS.length)];
 var ultimo=(idx>=totalDesafios()-1);
 var h='<div class="fb ok"><b>'+el+'</b> '+esc(explica||"")+'</div>';
 if(streak>=3)h+='<div class="dica" style="color:#7dffa8">&#128293; Você acertou '+streak+' seguidas!</div>';
 h+='<button class="btn verde pulsa" onclick="avancar()">'+(ultimo?"Ver resultado &#127937;":"Próximo &#9654;")+'</button>';
 var cont=$("app");cont.innerHTML=h+cont.innerHTML;window.scrollTo(0,0);
 falar(el+" "+(explica||""));salvar();
}
function avancar(){pararFala();checarConquistas();if(modoTreino){window._ti++;proxTreino();return;}idx++;proximoDesafio();}
function erro(el,d){pararFala();streak=0;errosSeg++;
 if(!S.stats[atual.ch])S.stats[atual.ch]={a:0,e:0};S.stats[atual.ch].e++;
 if(el){el.className="op erro";}
 if(!modoTreino)guardarErro(d);
 if(errosSeg>=2&&!facil){facil=true;falar("Sem pressa! Vou te ajudar. Olha com calma e tenta de novo.");}
 else falar("Quase! Pense de novo, com calma. Você consegue!");
 setTimeout(function(){if(el)el.className="op";},400);
}
function guardarErro(d){var k=JSON.stringify([atual.ch,d]);var i;for(i=0;i<ERROS.length;i++)if(ERROS[i].k===k)return;ERROS.push({k:k,tipo:atual.tipo,d:d,ch:atual.ch});}
function checarConquistas(){var i;for(i=0;i<CONQUISTAS.length;i++){if(!S.conq[CONQUISTAS[i].id]&&CONQUISTAS[i].cond(S)){S.conq[CONQUISTAS[i].id]=1;}}}

/* ============ FIM DE FASE ============ */
function errosDaFase(ch){var r=[],i;for(i=0;i<ERROS.length;i++)if(ERROS[i].ch===ch)r.push(ERROS[i]);return r;}
function ofertaExtra(p){pararFala();var h='<h1 style="font-size:22px">Você acertou tudo! &#11088;</h1>';
 h+='<div class="balao"><img src="'+IMG.mComemora+'" style="height:56px;width:auto;float:left;margin-right:8px">Uau, '+esc(S.nome||"chef")+'! Você mandou muito bem. Quer encarar um <b>desafio extra</b>, um pouquinho mais difícil?</div>';
 h+='<button class="btn pulsa" onclick="iniciarExtra()">Aceitar o desafio! &#128293;</button>';
 h+='<div style="text-align:center"><button class="btn sec" onclick="fecharOferta()">Agora não</button></div>';
 $("app").innerHTML=h;window.scrollTo(0,0);falar("Você acertou tudo! Quer encarar um desafio extra, um pouquinho mais difícil?");}
function iniciarExtra(){extraOn=true;var base=[[64,8],[81,9],[96,8],[72,6]];reseed(atual.ch.length*13+runAc);var pick=embaralhar(base.slice()).slice(0,2);
 atual={ch:atual.ch,tipo:"escolha",titulo:atual.titulo,gancho:atual.gancho,med:atual.med,jogo:false,_extra:true,
  desafios:[{en:pick[0][0]+" ÷ "+pick[0][1]+" = ?",r:pick[0][0]/pick[0][1]},{en:pick[1][0]+" ÷ "+pick[1][1]+" = ?",r:pick[1][0]/pick[1][1]}]};
 idx=0;streak=0;runAc=0;proximoDesafio();}
function ofertaReforco(p,errs){pararFala();var h='<h1 style="font-size:22px">Vamos treinar juntos!</h1>';
 h+='<div class="balao"><img src="'+IMG.mExplica+'" style="height:56px;width:auto;float:left;margin-right:8px">Sem problema! Vamos refazer com calma o que passou, pra você fixar. Você consegue!</div>';
 h+='<button class="btn pulsa" onclick="iniciarReforco()">Continuar &#9654;</button>';
 $("app").innerHTML=h;window.scrollTo(0,0);falar("Vamos treinar juntos, com calma, pra você fixar. Você consegue!");}
function iniciarReforco(){reforcoOn=true;window._reforcoParada=atual;var errs=errosDaFase(atual.ch);window._treino=errs.slice();window._ti=0;modoTreino=true;facil=true;proxTreino();}
function fecharOferta(){extraOn=true;fimFaseReal();}
function fimFase(){pararFala();var p=atual;
 var tot=totalDesafios(),ac=runAc;
 if(!p.jogo&&!modoTreino&&!p._extra){
  if(!extraOn&&tot>0&&ac>=tot){return ofertaExtra(p);}
  var ef=errosDaFase(p.ch);
  if(!reforcoOn&&ef.length>0&&ac<Math.ceil(tot*0.5)){return ofertaReforco(p,ef);}
 }
 fimFaseReal();
}
function fimFaseReal(){var p=atual;if(p._extra){S.pontos+=4;}
 if(!p.jogo&&!S.feitasMap[p.ch])marcarFeita(p);
 else if(p.jogo)S.feitasMap[p.ch]=1;
 checarConquistas();salvar();
 var h="";
 h+='<h1>Parada concluída!</h1>';
 if(p.med>=0)h+='<div style="text-align:center;position:relative;display:inline-block;width:100%"><img src="'+IMG.med[p.med]+'" style="height:110px;width:auto"></div>';
 else h+='<div style="text-align:center;font-size:60px">&#127881;</div>';
 h+='<div style="text-align:center;font-size:20px;font-weight:bold;color:#ffd9a8">&#11088; '+plural(S.pontos,"ponto","pontos")+' no total</div>';
 h+='<div class="balao"><img src="'+IMG.mComemora+'" style="height:56px;width:auto;float:left;margin-right:8px">'+esc(p.gancho)+'</div>';
 var prox=proximaParadaNome();
 if(prox)h+='<div class="dica">&#128275; Você abriu: '+esc(prox)+'!</div>';
 var todas=feitas()>=PARADAS.length;
 h+='<button class="btn pulsa" onclick="'+(todas?"grandeFinal()":"irMapa()")+'">'+(todas?"Ver o grande final &#127881;":"&#9654; Ir para o mapa")+'</button>';
 h+='<div style="text-align:center"><button class="btn sec" onclick="abrirParadaCh(\''+p.ch+'\')">&#128257; Jogar de novo</button></div>';
 $("app").innerHTML=h;window.scrollTo(0,0);confete(24);
 falar("Parada concluída! "+p.gancho);
}
function marcarFeita(p){S.feitasMap[p.ch]=1;}
function abrirParadaCh(ch){var i;for(i=0;i<PARADAS.length;i++)if(PARADAS[i].ch===ch){abrirParada(i);return;}}
function proximaParadaNome(){var i;for(i=0;i<PARADAS.length;i++)if(!S.feitasMap[PARADAS[i].ch])return PARADAS[i].titulo;return "";}

/* ============ JOGO MEMÓRIA ============ */
var _memAbertas=[],_memTrava=false,_memPares=0;
function jogoMemoria(){var cartas=[],i;for(i=0;i<atual.pares.length;i++){cartas.push({t:atual.pares[i][0],g:i});cartas.push({t:atual.pares[i][1],g:i});}
 embaralhar(cartas);_memAbertas=[];_memTrava=false;_memPares=0;window._memCartas=cartas;
 var h='<h1 style="font-size:22px">'+esc(atual.titulo)+'</h1><div class="enun" style="font-size:16px">Ache os pares: a conta de vezes e a divisão do contrário.</div><div class="memgrid">';
 for(i=0;i<cartas.length;i++)h+='<div class="memc" id="mc'+i+'" onclick="virarMem('+i+')">?</div>';
 h+='</div>';$("app").innerHTML=h;window.scrollTo(0,0);falar("Ache os pares! Junte cada conta de vezes com a divisão do contrário que dá o mesmo doce.");
}
function virarMem(i){if(_memTrava)return;var c=window._memCartas[i],el=$("mc"+i);if(el.className.indexOf("aberta")>=0||el.className.indexOf("par")>=0)return;
 el.className="memc aberta";el.innerHTML=c.t;_memAbertas.push(i);
 if(_memAbertas.length===2){_memTrava=true;var a=_memAbertas[0],b=_memAbertas[1];
  if(window._memCartas[a].g===window._memCartas[b].g){setTimeout(function(){$("mc"+a).className="memc par";$("mc"+b).className="memc par";_memAbertas=[];_memTrava=false;_memPares++;confete(8);falar("Par certo!");if(_memPares>=atual.pares.length){S.pontos+=6;setTimeout(fimFase,700);}},450);}
  else{setTimeout(function(){$("mc"+a).className="memc";$("mc"+a).innerHTML="?";$("mc"+b).className="memc";$("mc"+b).innerHTML="?";_memAbertas=[];_memTrava=false;},750);}
 }
}

/* ============ MEDALHAS / TREINO / RELATÓRIO / FINAL ============ */
function verMedalhas(){var h='<h1 style="font-size:22px">Minhas Medalhas</h1><div class="medgrid">',i;
 for(i=0;i<PARADAS.length;i++){var p=PARADAS[i];if(p.med<0)continue;var g=S.feitasMap[p.ch];
  h+='<div class="mi '+(g?"":"no0")+'"><img src="'+IMG.med[p.med]+'"><span class="mnum">'+(p.med+1)+'</span></div>';}
 h+='</div><h1 style="font-size:18px">Conquistas</h1><div class="medgrid">';
 for(i=0;i<IMG.selo.length;i++){var got=S.conq["c"+(i+1)];h+='<div class="mi '+(got?"":"no0")+'"><img src="'+IMG.selo[i]+'"></div>';}
 h+='</div><button class="btn" onclick="irMapa()">&#9654; Voltar ao mapa</button>';
 $("app").innerHTML=h;window.scrollTo(0,0);
}
function treinarErros(){if(!ERROS.length)return;modoTreino=true;window._treino=ERROS.slice();window._ti=0;proxTreino();}
function proxTreino(){if(window._ti>=window._treino.length){
  if(reforcoOn){reforcoOn=false;modoTreino=false;facil=false;atual=window._reforcoParada;falar("Muito bem! Agora você fixou.");fimFaseReal();return;}
  modoTreino=false;ERROS=[];falar("Muito bem! Você treinou tudo.");irMapa();return;}
 var e=window._treino[window._ti];atual={ch:e.ch,tipo:e.tipo,desafios:[e.d],doce:"dBiscoito"};idx=0;
 renderDesafio(e.d,0);}
function relatorio(){var h='<h1 style="font-size:22px">Relatório</h1><table class="reln"><tr><th>Parada</th><th>Acertos</th><th>Erros</th></tr>',i;
 for(i=0;i<PARADAS.length;i++){var p=PARADAS[i];if(p.jogo)continue;var s=S.stats[p.ch]||{a:0,e:0};h+='<tr><td>'+esc(p.titulo)+'</td><td>'+s.a+'</td><td>'+s.e+'</td></tr>';}
 h+='</table><button class="btn" onclick="window.print()">&#128424; Imprimir</button><button class="btn sec" onclick="irMapa()">Voltar</button>';
 $("app").innerHTML=h;window.scrollTo(0,0);
}
function grandeFinal(){pararFala();S.feitasMap.fim=1;salvar();
 var h='<h1>&#127881; Você é Mestre da Divisão!</h1>';
 h+='<img class="capaimg" src="'+IMG.diploma+'" alt="Diploma" style="border-color:#ffd93f">';
 h+='<div class="lead">Parabéns, <b>'+esc(S.nome||"chef")+'</b>! Você ajudou o Chef Confeito a preparar TODOS os doces da Festa da Cidade, repartindo tudo em partes iguais. Agora você é um <b>Mestre Confeiteiro da Divisão</b>!</div>';
 h+='<div style="text-align:center;font-size:20px;font-weight:bold;color:#ffd9a8">&#11088; '+plural(S.pontos,"ponto","pontos")+' · '+NIVEIS[nivelIdx(S.pontos)].n+'</div>';
 h+='<button class="btn pulsa" onclick="relatorio()">&#128202; Ver meu relatório</button>';
 h+='<button class="btn sec" onclick="verMedalhas()">&#127941; Minhas conquistas</button> <button class="btn sec" onclick="irMapa()">Voltar ao mapa</button>';
 $("app").innerHTML=h;window.scrollTo(0,0);confeteOndas();
 falar("Parabéns, "+(S.nome||"chef")+"! Você preparou todos os doces da Festa da Cidade e virou um Mestre Confeiteiro da Divisão!");
}

/* ============ COMEMORAÇÃO / CONFETE ============ */
function carimbo(){var d=document.createElement("div");d.className="carimbo";d.innerHTML='<div class="ci">&#10003;</div>';document.body.appendChild(d);
 var f=document.createElement("div");f.className="festa";f.innerHTML=FESTApool[Math.floor(rnd()*FESTApool.length)];document.body.appendChild(f);
 setTimeout(function(){if(d.parentNode)d.parentNode.removeChild(d);if(f.parentNode)f.parentNode.removeChild(f);},1400);}
function confete(n){var c=$("confete"),i;for(i=0;i<n;i++){(function(){var s=document.createElement("div");var x=Math.random()*100;s.style.cssText="position:absolute;top:-10px;left:"+x+"%;width:9px;height:9px;background:hsl("+(Math.random()*60+10)+",90%,60%);border-radius:2px;";c.appendChild(s);var y=0,vy=2+Math.random()*3,rot=Math.random()*360;var t=setInterval(function(){y+=vy;rot+=8;s.style.top=y+"px";s.style.webkitTransform="rotate("+rot+"deg)";s.style.transform="rotate("+rot+"deg)";if(y>window.innerHeight){clearInterval(t);if(s.parentNode)s.parentNode.removeChild(s);}},20);})();}}
function confeteOndas(){var k;for(k=0;k<4;k++)setTimeout(function(){confete(20);},k*400);}

function esc(t){return (""+(t==null?"":t)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}

/* ============ BOOT ============ */
telaInicial();
