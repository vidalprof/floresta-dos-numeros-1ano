/* Service worker — REDE PRIMEIRO (nunca prende o app numa versão velha).
   Online: sempre traz a versão nova. Offline: usa a cópia guardada. */
var CACHE="planeta-vivo-v12";
/* Só a casca + imagens que aparecem já no começo. Biomas/áudio entram sozinhos
   pelo cache de runtime (fetch) — evita precache pesado em PC fraco. */
var ATIVOS=["./","./index.html","./manifest.json",
 "./img/earthmap.jpg","./img/globo.png",
 "./img/nara.png","./img/nara_fala.png","./img/nara_pisca.png","./img/nara_v_meio.png","./img/nara_v_o.png","./img/nara_aponta.png",
 "./visemas.json",
 "./img/ic_sol.png","./img/medalha_clima.png",
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
