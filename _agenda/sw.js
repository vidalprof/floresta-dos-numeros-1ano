/* Service Worker — app shell offline + HTML sempre fresco.
   Os dados (Firebase, outra origem) NUNCA são cacheados: passam direto pela rede. */
const CACHE = "agenda-shell-v5";
const SHELL = ["./", "./index.html", "./manifest.json", "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL).catch(() => {})));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

// Só tratamos como "app de verdade" respostas 200 de HTML — um 403/500 cai para o cache
// bom em vez de virar "o app". (Contra portal cativo de Wi-Fi a proteção principal é o
// HTTPS do github.io + o bypass cross-origin abaixo: o portal não injeta um 200 válido na
// nossa origem sem quebrar o TLS, então o fetch falha e servimos o cache. Este htmlOk é a
// segunda camada, e evita cachear lixo caso um dia o app rode em HTTP.)
const htmlOk = (r) => !!(r && r.ok && (r.headers.get("content-type") || "").includes("text/html"));

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }
  // Requisições de outra origem (Firebase, etc.): deixa a rede cuidar — não cacheia dados.
  if (url.origin !== location.origin) return;
  // Navegação / HTML: rede primeiro (nunca fica velho); MAS com limite de tempo — se a
  // rede estagnar (conectada e pendurada), cai no cache em vez de travar a tela branca.
  if (req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html")) {
    const fromCache = () => caches.match(req).then((m) => m || caches.match("./index.html"));
    const net = fetch(req).then((r) => {
      if (htmlOk(r)) { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); }
      return r;
    });
    const timeout = new Promise((res) => setTimeout(() => res(null), 4000));
    e.respondWith(
      Promise.race([net.catch(() => null), timeout]).then((r) => (htmlOk(r) ? r : fromCache()))
    );
    return;
  }
  // Ícones/estáticos: cache primeiro, atualiza em segundo plano (só grava resposta boa).
  e.respondWith(
    caches.match(req).then((m) => m || fetch(req).then((r) => {
      if (r && r.ok) { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); }
      return r;
    }))
  );
});
