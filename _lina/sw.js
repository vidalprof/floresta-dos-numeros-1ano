/* Service worker — REDE PRIMEIRO no HTML (nunca prende versão velha);
   CACHE PRIMEIRO em imagens/áudio (rápido em PC fraco), atualizando em 2º plano. */
var PREFIXO="oficina-lina-";
/* ⚠️ SUBIR ESTE NUMERO SEMPRE QUE MUDAR IMAGEM OU AUDIO (ago/2026).
   O HTML e "rede primeiro", entao a tela nova chega sozinha. Mas imagem e som
   sao "cache primeiro": um arquivo com o MESMO nome e conteudo novo (uma voz
   regravada, por exemplo) continua saindo do cache VELHO para sempre. Ou seja,
   a crianca ve a tela nova e ouve a voz antiga — exatamente o defeito que a
   gente esta tentando matar. Trocar o numero apaga o cache anterior. */
var CACHE=PREFIXO+"v1";
var ATIVOS=["./","./index.html","./manifest.json",
 "./img/lt_fundo.png",
 "./img/lt_pincel_feliz.png",
 "./img/lt_pincel_fala.png",
 "./img/lt_pincel_pisca.png",
 "./img/med_lt.png",
 "./img/lt_campo.png",
 "./img/lt_bomba.png",
 "./img/lt_tambor.png",
 "./img/lt_sempre.png",
 "./img/lt_ombro.png",
 "./img/lt_ponte.png",
 "./img/lt_canto.png",
 "./img/lt_manga.png",
 "./img/lt_vento.png",
 "./img/lt_lampada.png",
 "./img/lt_campeao.png",
 "./img/lt_bombeiro.png",
 "./img/lt_placa_pronta.png",
 "./img/lt_placa_pronta.png",
 "./img/lt_cr1.png",
 "./img/lt_cr2.png",
 "./img/lt_cr3.png",
 "./img/lt_cr4.png",
 "./img/lt_cr5.png",
 "./img/lt_cr6.png",
 "./audio/lt_abertura.mp3","./audio/lt_p1_intro.mp3"];
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
