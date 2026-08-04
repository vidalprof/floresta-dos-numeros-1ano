/* Service worker — REDE PRIMEIRO no HTML (nunca prende versão velha);
   CACHE PRIMEIRO em imagens/áudio (rápido em PC fraco), atualizando em 2º plano. */
var CACHE="orbi-observatorio-v2";
var ATIVOS=["./","./index.html","./manifest.json",
 "./img/sr_fundo.jpg","./img/sr_orbi_feliz.png","./img/sr_orbi_fala.png","./img/sr_orbi_pisca.png",
 "./img/sr_orbi_pensa.png","./img/sr_orbi_festa.png","./img/med_espaco.png",
 "./img/sr_sol.png","./img/sr_terra.png","./img/sr_lua.png","./img/sr_estrela.png",
 "./img/sr_lampada.png","./img/sr_espelho.png","./img/sr_casa.png",
 "./audio/sr_abertura.mp3","./audio/sr_prever.mp3","./audio/sr_luz_intro.mp3"];
self.addEventListener("install",function(e){self.skipWaiting();e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ATIVOS).catch(function(){});}));});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k!==CACHE)return caches.delete(k);}));}));self.clients.claim();});
function guardar(req,resp){try{if(resp&&resp.status===200&&resp.type==="basic"){var cp=resp.clone();caches.open(CACHE).then(function(c){c.put(req,cp);});}}catch(x){}return resp;}
self.addEventListener("fetch",function(e){
  if(e.request.method!=="GET")return;
  var req=e.request,aceita=req.headers.get("accept")||"";
  var ehPagina=(req.mode==="navigate")||aceita.indexOf("text/html")>=0;
  if(ehPagina){e.respondWith(fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return caches.match(req).then(function(c){return c||caches.match("./index.html");});}));}
  else{e.respondWith(caches.match(req).then(function(c){var rede=fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return c;});return c||rede;}));}
});
