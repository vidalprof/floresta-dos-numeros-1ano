/* Service worker — REDE PRIMEIRO (nunca prende o app numa versão velha).
   Online: sempre traz a versão nova. Offline: usa a cópia guardada. */
var CACHE="fabrica-estrelas-v15";
var ATIVOS=["./","./index.html","./manifest.json",
 "./img/ceu_noite.jpg","./img/fagulha.png","./img/fagulha_fala.png","./img/fagulha_pisca.png",
 "./img/fagulha_acena.png","./img/fagulha_comemora.png","./img/fagulha_pensa.png",
 "./img/fabrica_estrelas.png","./img/estrela_grande.png","./img/estrela_no.png","./img/caixa_estrelas.png",
 "./audio/abertura.mp3","./audio/tela_inicial.mp3","./audio/p1.mp3","./audio/p2.mp3","./audio/r1.mp3","./audio/p3.mp3","./audio/soma.mp3","./audio/p4.mp3","./audio/r2.mp3","./audio/prob.mp3","./audio/p5.mp3","./audio/desafio.mp3","./audio/decore.mp3","./audio/final.mp3","./audio/e_p1.mp3","./audio/e_p2.mp3","./audio/e_p3.mp3","./audio/e_soma.mp3","./audio/e_p4.mp3","./audio/e_prob.mp3","./audio/e_p5.mp3","./audio/e_desafio.mp3",
 "./audio/conta_uma.mp3","./audio/conta_duas.mp3","./audio/conta_tres.mp3","./audio/conta_quatro_cheia.mp3","./audio/ouvir_de_novo.mp3",
 "./audio/aj_p1_1.mp3","./audio/aj_p1_2.mp3","./audio/aj_p1_3.mp3","./audio/aj_soma_1.mp3","./audio/aj_soma_2.mp3","./audio/aj_soma_3.mp3",
 "./audio/se_p1_q.mp3","./audio/se_soma_q.mp3","./audio/se_ok.mp3","./audio/se_quase.mp3","./audio/segue_pratica.mp3",
 "./audio/aj_p2_1.mp3","./audio/aj_p2_2.mp3","./audio/aj_p2_3.mp3","./audio/aj_prob_1.mp3","./audio/aj_prob_2.mp3","./audio/aj_prob_3.mp3",
 "./audio/se_p2_q.mp3","./audio/se_p3_q.mp3","./audio/se_p4_q.mp3","./audio/se_prob_q.mp3",
 "./audio/refl_ok.mp3","./audio/refl_hmm.mp3",
 "./icon-192.png","./icon-512.png"];
self.addEventListener("install",function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ATIVOS).catch(function(){});}));
});
self.addEventListener("activate",function(e){
  e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k!==CACHE)return caches.delete(k);}));}));
  self.clients.claim();
});
function guardar(req,resp){
  try{ if(resp&&resp.status===200&&resp.type==="basic"){ var cp=resp.clone(); caches.open(CACHE).then(function(c){c.put(req,cp);}); } }catch(x){}
  return resp;
}
self.addEventListener("fetch",function(e){
  if(e.request.method!=="GET")return;
  var req=e.request, aceita=req.headers.get("accept")||"";
  var ehPagina=(req.mode==="navigate")||aceita.indexOf("text/html")>=0;
  if(ehPagina){
    // HTML: rede primeiro (versão sempre fresca), cai pro cache se offline
    e.respondWith(fetch(req).then(function(r){return guardar(req,r);}).catch(function(){
      return caches.match(req).then(function(c){return c||caches.match("./index.html");});
    }));
  } else {
    // Imagens/áudio/etc: cache primeiro (rápido), mas atualiza em segundo plano
    e.respondWith(caches.match(req).then(function(c){
      var rede=fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return c;});
      return c||rede;
    }));
  }
});
