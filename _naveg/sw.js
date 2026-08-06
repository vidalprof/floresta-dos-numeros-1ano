/* Service worker — rede primeiro no HTML; cache primeiro em imagem/áudio. */
var PREFIXO="naveg-";
var CACHE=PREFIXO+"v2";

var ATIVOS=["./","./index.html","./manifest.json","./img/nv_base.png","./img/nv_fala.png","./img/nv_pisca.png","./img/nv_cr1.png","./img/nv_cr2.png","./img/nv_cr3.png","./img/nv_cr4.png","./img/nv_cr5.png","./img/nv_cr6.png","./img/nv_mandioca.png","./img/nv_milho.png","./img/nv_batata.png","./img/nv_cacau.png","./img/nv_cavalo.png","./img/nv_trigo.png","./img/nv_cana.png","./img/nv_roda.png","./img/nv_bussola.png","./img/nv_astrolabio.png","./img/nv_barril.png","./img/nv_corda.png","./img/nv_mapa.png","./img/nv_luneta.png","./img/nv_bau.png","./img/nv_ampulheta.png","./img/nv_fundo.jpg","./img/nv_horizonte.jpg","./img/nv_caravela.jpg","./img/nv_aldeia.jpg","./img/nv_porao.jpg","./img/nv_atlantico.jpg"];
self.addEventListener("install",function(e){self.skipWaiting();e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ATIVOS).catch(function(){});}));});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k!==CACHE&&k.indexOf(PREFIXO)===0)return caches.delete(k);}));}));self.clients.claim();});
function guardar(req,resp){try{if(resp&&resp.status===200&&resp.type==="basic"){var cp=resp.clone();caches.open(CACHE).then(function(c){c.put(req,cp);});}}catch(x){}return resp;}
self.addEventListener("fetch",function(e){
  if(e.request.method!=="GET")return;
  var req=e.request,aceita=req.headers.get("accept")||"";
  var ehPagina=(req.mode==="navigate")||aceita.indexOf("text/html")>=0;
  if(ehPagina){e.respondWith(fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return caches.match(req).then(function(c){return c||caches.match("./index.html");});}));}
  else{e.respondWith(caches.match(req).then(function(c){var rede=fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return c;});return c||rede;}));}
});
