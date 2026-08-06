/* Service worker — rede primeiro no HTML; cache primeiro em imagem/áudio. */
var PREFIXO="voo-do-nico-";
var CACHE=PREFIXO+"v6";

var ATIVOS=["./","./index.html","./manifest.json","./img/mp_base.png","./img/mp_fala.png","./img/mp_pisca.png","./img/mp_cr1.png","./img/mp_cr2.png","./img/mp_cr3.png","./img/mp_cr4.png","./img/mp_cr5.png","./img/mp_cr6.png","./img/mp_med.png","./img/mp_verso.png","./img/mp_fundo.jpg","./img/mp_voo_a.jpg","./img/mp_voo_b.jpg","./img/mp_voo_c.jpg","./img/mp_maquete.jpg","./img/mp_mapa.jpg","./img/mp_esc_sala.jpg","./img/mp_esc_escola.jpg","./img/mp_esc_bairro.jpg","./img/mp_esc_cidade.jpg","./img/mp_rosa.png","./img/mp_planta_sala.jpg","./img/mp_lousa_c.png","./img/mp_armario_c.png","./img/mp_bairro.jpg","./audio/mp_abertura.mp3"];
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
