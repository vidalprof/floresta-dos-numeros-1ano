var CACHE="fabrica-estrelas-v1";
var ATIVOS=["./","./index.html","./manifest.json",
 "./img/ceu_noite.jpg","./img/fagulha.png","./img/fagulha_fala.png","./img/fagulha_pisca.png",
 "./img/fagulha_acena.png","./img/fabrica_estrelas.png","./img/estrela_grande.png",
 "./audio/abertura.mp3","./audio/tela_inicial.mp3","./icon-192.png","./icon-512.png"];
self.addEventListener("install",function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ATIVOS).catch(function(){});}));
});
self.addEventListener("activate",function(e){
  e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k!==CACHE)return caches.delete(k);}));}));
  self.clients.claim();
});
self.addEventListener("fetch",function(e){
  if(e.request.method!=="GET")return;
  e.respondWith(caches.match(e.request).then(function(r){return r||fetch(e.request).catch(function(){return caches.match("./index.html");});}));
});
