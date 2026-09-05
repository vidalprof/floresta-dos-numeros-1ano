/* ============================================================
   VER RODANDO — abre atividades de REFERÊNCIA na internet (H5P, PhET, Toy
   Theater, Math Learning Center, Wordwall, LearningApps, sites brasileiros),
   JOGA nelas com um Chromium de verdade e guarda o que elas fazem por baixo.

   Pedido do Marcos (set/2026): *"pesquise e veja essas atividades rodando em
   atividades na internet funcionando para deixar elas lapidadas da melhor
   forma possível"*. O `pesquisar.yml` traz TEXTO; este traz COMPORTAMENTO:
     · foto antes, no meio do arrasto e depois de soltar (PC 1024x600) e no
       celular (412x820);
     · que eventos os alvos escutam (pointer/touch/mouse), `touch-action`,
       `cursor`, tamanho dos alvos, fonte mínima, `draggable=`;
     · som: <audio>/<video> e WebAudio (quantas vezes tocou ao interagir);
     · "suco" (feedback): quantas mutações no DOM e classes trocadas no
       primeiro segundo depois de soltar/clicar; animações e transições em uso.
   Roda no GitHub Actions (`ver-rodando.yml`), onde há internet. Aqui no chat
   só se lê o resultado (`_pesquisa/rodando/<lote>/RODANDO.md` + as fotos).

   Uso:  ALVOS_JSON='[{"nome":"h5p-arrastar","url":"https://h5p.org/drag-and-drop"}]' \
         DEST=_pesquisa/rodando/lote node _padrao/ver_rodando.js
   ============================================================ */
const fs = require('fs');
const path = require('path');
let chromium;
try { chromium = require('playwright').chromium; }
catch (e) { console.log('NAO MEDI: sem playwright (' + e.code + ')'); process.exit(2); }

const ALVOS = JSON.parse(process.env.ALVOS_JSON || '[]');
const DEST = process.env.DEST || '_pesquisa/rodando/lote';
const JPG = {type: 'jpeg', quality: 55};
fs.mkdirSync(DEST, {recursive: true});

/* injetado ANTES de a página rodar (em todo frame): marca em cada elemento os
   tipos de evento que ele escuta, conta som e requestAnimationFrame. */
const ESPIAO = () => {
  try {
    const add = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function (t, fn, op) {
      try {
        if (this && this.nodeType === 1) { (this.__ev = this.__ev || {})[t] = 1; }
        else if (this === document || this === window) { (window.__evDoc = window.__evDoc || {})[t] = (window.__evDoc[t] || 0) + 1; }
      } catch (e) {}
      return add.call(this, t, fn, op);
    };
    window.__som = {media: 0, webaudio: 0};
    const play = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function () { window.__som.media++; return play.apply(this, arguments); };
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) {
      const prot = AC.prototype;
      ['createOscillator', 'createBufferSource', 'decodeAudioData'].forEach(k => {
        const o = prot[k]; if (o) prot[k] = function () { window.__som.webaudio++; return o.apply(this, arguments); };
      });
    }
    window.__raf = 0;
    const raf = window.requestAnimationFrame;
    window.requestAnimationFrame = function (f) { window.__raf++; return raf.call(window, f); };
    /* contador de mutações: ligado pelo medidor na hora da interação */
    window.__mut = 0;
    window.__ligaMut = () => {
      try { window.__mo && window.__mo.disconnect(); } catch (e) {}
      window.__mut = 0;
      window.__mo = new MutationObserver(ms => { window.__mut += ms.length; });
      window.__mo.observe(document.documentElement, {subtree: true, childList: true, attributes: true, characterData: true});
    };
  } catch (e) {}
};

/* o que cada frame conta sobre si */
const COLETA = () => {
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 4 && r.height > 4 && r.bottom > 0 && r.right > 0 && r.top < innerHeight * 2 && getComputedStyle(e).visibility !== 'hidden'; };
  const todos = [...document.querySelectorAll('body *')].filter(vis);
  const alvos = todos.filter(e => {
    const ev = e.__ev || {};
    const prop = ['onmousedown', 'ontouchstart', 'onpointerdown', 'onclick'].some(k => typeof e[k] === 'function');
    return ev.pointerdown || ev.touchstart || ev.mousedown || ev.click || prop || e.getAttribute('draggable') === 'true' ||
           /^(button|a|input|select)$/i.test(e.tagName) || /button|option|tab|slider|checkbox|radio/.test(e.getAttribute('role') || '');
  });
  const arrasto = alvos.filter(e => { const ev = e.__ev || {}; return ev.pointerdown || ev.touchstart || ev.mousedown || e.getAttribute('draggable') === 'true' || typeof e.onmousedown === 'function'; });
  const desc = e => {
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return {tag: e.tagName.toLowerCase(), cls: String(e.className || '').trim().split(/\s+/).slice(0, 3).join('.'),
            w: Math.round(r.width), h: Math.round(r.height), touchAction: cs.touchAction, cursor: cs.cursor,
            userSelect: cs.userSelect || cs.webkitUserSelect, transition: cs.transitionDuration, animation: cs.animationName,
            ev: Object.keys(e.__ev || {}).join(' '), draggable: e.getAttribute('draggable'), role: e.getAttribute('role'),
            aria: e.getAttribute('aria-label') ? 1 : 0, texto: (e.textContent || '').trim().slice(0, 40)};
  };
  const tipos = {};
  todos.forEach(e => Object.keys(e.__ev || {}).forEach(t => { tipos[t] = (tipos[t] || 0) + 1; }));
  const fontes = todos.map(e => parseFloat(getComputedStyle(e).fontSize)).filter(v => v > 0);
  const menores = alvos.map(e => e.getBoundingClientRect()).filter(r => r.width > 8 && r.height > 8);
  const minAlvo = menores.length ? Math.min(...menores.map(r => Math.min(r.width, r.height))) : null;
  const animados = todos.filter(e => { const cs = getComputedStyle(e); return (cs.animationName && cs.animationName !== 'none') || (cs.transitionDuration && cs.transitionDuration !== '0s'); }).length;
  return {
    url: location.href.slice(0, 120), elementos: todos.length, alvos: alvos.length, arrasto: arrasto.length,
    exemplosArrasto: arrasto.slice(0, 6).map(desc), exemplosAlvos: alvos.slice(0, 6).map(desc),
    tiposDeEvento: tipos, escutasNoDocumento: window.__evDoc || {}, draggableAttr: document.querySelectorAll('[draggable="true"]').length,
    audioTags: document.querySelectorAll('audio,video').length, som: window.__som || null, raf: window.__raf || 0,
    fonteMin: fontes.length ? Math.round(Math.min(...fontes)) : null, alvoMin: minAlvo ? Math.round(minAlvo) : null,
    animadosOuTransicoes: animados, canvas: document.querySelectorAll('canvas').length, svg: document.querySelectorAll('svg').length,
    ariaLive: document.querySelectorAll('[aria-live]').length,
  };
};

async function fechaAvisos(page) {
  const rx = /^(accept|aceitar|aceito|agree|i agree|ok|got it|entendi|allow|continuar|continue|fechar|close|×|x)$/i;
  for (const f of page.frames()) {
    try {
      const bs = await f.$$('button, a, [role=button]');
      for (const b of bs.slice(0, 60)) {
        const t = ((await b.textContent()) || '').trim();
        if (rx.test(t) && await b.isVisible()) { await b.click({timeout: 1500}).catch(() => {}); return t; }
      }
    } catch (e) {}
  }
  return null;
}

async function candidato(page, quero) {
  /* devolve {frame, handle, box} do primeiro elemento bom para o gesto pedido */
  for (const f of page.frames()) {
    let hs = [];
    try {
      hs = await f.evaluateHandle((quero) => {
        const vis = e => { const r = e.getBoundingClientRect(); return r.width >= 18 && r.height >= 18 && r.width <= 420 && r.height <= 420 && r.top >= 0 && r.left >= 0 && r.bottom <= innerHeight && r.right <= innerWidth; };
        const ok = e => {
          const ev = e.__ev || {};
          if (quero === 'arrasto') return ev.pointerdown || ev.touchstart || ev.mousedown || e.getAttribute('draggable') === 'true' || typeof e.onmousedown === 'function' || /drag|arrast|piece|tile|card|token|handle|thumb|draggable/i.test(e.className || '');
          return ev.click || typeof e.onclick === 'function' || /^(button|a)$/i.test(e.tagName) || /button|option/.test(e.getAttribute('role') || '') || /option|answer|choice|word|card|item|btn|button/i.test(e.className || '');
        };
        return [...document.querySelectorAll('body *')].filter(e => vis(e) && ok(e) && !/^(html|body|script|style)$/i.test(e.tagName)).slice(0, 12);
      }, quero);
      const props = await hs.getProperties();
      for (const h of props.values()) {
        const el = h.asElement(); if (!el) continue;
        const box = await el.boundingBox();
        if (box && box.width >= 18) return {frame: f, handle: el, box};
      }
    } catch (e) {}
  }
  return null;
}

async function mede(page) {
  const out = [];
  for (const f of page.frames()) {
    try { out.push(await f.evaluate(COLETA)); } catch (e) { out.push({url: f.url().slice(0, 100), erro: String(e.message).slice(0, 80)}); }
  }
  return out;
}
const soma = (frames, k) => frames.reduce((a, f) => a + (f[k] || 0), 0);
const somaSom = frames => frames.reduce((a, f) => ({media: a.media + (f.som ? f.som.media : 0), webaudio: a.webaudio + (f.som ? f.som.webaudio : 0)}), {media: 0, webaudio: 0});

(async () => {
  /* no runner o `npx playwright install chromium` deixa o navegador certo; na
     bancada local o Chromium mora em /opt/pw-browsers (passar por CROMO=). */
  const b = await chromium.launch({executablePath: process.env.CROMO || undefined,
                                   args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']});
  const relat = [];
  for (const alvo of ALVOS) {
    const nome = alvo.nome.replace(/[^a-z0-9\-]+/gi, '-').toLowerCase();
    const obs = {nome, url: alvo.url, quando: new Date().toISOString(), fotos: []};
    console.log('\n== ' + nome + '  ' + alvo.url);
    /* ---- PC 1024x600 ---- */
    let ctx, page;
    try {
      ctx = await b.newContext({viewport: {width: 1024, height: 600}, locale: 'pt-BR', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'});
      await ctx.addInitScript(ESPIAO);
      page = await ctx.newPage();
      page.setDefaultTimeout(20000);
      await page.goto(alvo.url, {waitUntil: 'domcontentloaded', timeout: 60000});
      await page.waitForTimeout(6000);
      obs.avisoFechado = await fechaAvisos(page);
      await page.waitForTimeout(1500);
      obs.titulo = (await page.title()).slice(0, 100);
      obs.frames = page.frames().length;
      const f1 = path.join(DEST, nome + '-pc-antes.jpg');
      await page.screenshot({path: f1, ...JPG}); obs.fotos.push(path.basename(f1));
      obs.antes = await mede(page);
      /* clique num alvo de escolha */
      const c = await candidato(page, 'clique');
      if (c) {
        for (const f of page.frames()) { try { await f.evaluate(() => window.__ligaMut && window.__ligaMut()); } catch (e) {} }
        const s0 = somaSom(await mede(page));
        await page.mouse.click(c.box.x + c.box.width / 2, c.box.y + c.box.height / 2);
        await page.waitForTimeout(350);
        const f2 = path.join(DEST, nome + '-pc-clique.jpg');
        await page.screenshot({path: f2, ...JPG}); obs.fotos.push(path.basename(f2));
        await page.waitForTimeout(700);
        const dep = await mede(page); const s1 = somaSom(dep);
        let mut = 0; for (const f of page.frames()) { try { mut += await f.evaluate(() => window.__mut || 0); } catch (e) {} }
        obs.clique = {alvo: c.box, mutacoesEm1s: mut, somMedia: s1.media - s0.media, somWebAudio: s1.webaudio - s0.webaudio};
      } else obs.clique = null;
      /* arrasto */
      const d = await candidato(page, 'arrasto');
      if (d) {
        for (const f of page.frames()) { try { await f.evaluate(() => window.__ligaMut && window.__ligaMut()); } catch (e) {} }
        const s0 = somaSom(await mede(page));
        const x0 = d.box.x + d.box.width / 2, y0 = d.box.y + d.box.height / 2;
        const dx = (x0 + 160 < 1000) ? 160 : -160, dy = (y0 + 60 < 560) ? 60 : -60;
        await page.mouse.move(x0, y0); await page.mouse.down();
        for (let i = 1; i <= 8; i++) { await page.mouse.move(x0 + dx * i / 8, y0 + dy * i / 8); await page.waitForTimeout(30); }
        const f3 = path.join(DEST, nome + '-pc-arrastando.jpg');
        await page.screenshot({path: f3, ...JPG}); obs.fotos.push(path.basename(f3));
        await page.mouse.up();
        await page.waitForTimeout(400);
        const f4 = path.join(DEST, nome + '-pc-soltou.jpg');
        await page.screenshot({path: f4, ...JPG}); obs.fotos.push(path.basename(f4));
        await page.waitForTimeout(600);
        const dep = await mede(page); const s1 = somaSom(dep);
        let mut = 0; for (const f of page.frames()) { try { mut += await f.evaluate(() => window.__mut || 0); } catch (e) {} }
        /* o elemento andou de verdade? */
        let novo = null; try { novo = await d.handle.boundingBox(); } catch (e) {}
        obs.arrasto = {alvo: d.box, deslocouPx: novo ? Math.round(Math.hypot(novo.x - d.box.x, novo.y - d.box.y)) : null,
                       mutacoesEm1s: mut, somMedia: s1.media - s0.media, somWebAudio: s1.webaudio - s0.webaudio};
      } else obs.arrasto = null;
      obs.depois = await mede(page);
      await ctx.close();
    } catch (e) {
      obs.erroPC = String(e.message).slice(0, 160); console.log('  erro PC: ' + obs.erroPC);
      try { await ctx.close(); } catch (e2) {}
    }
    /* ---- celular 412x820 (toque) ---- */
    try {
      ctx = await b.newContext({viewport: {width: 412, height: 820}, isMobile: true, hasTouch: true, deviceScaleFactor: 2, locale: 'pt-BR'});
      await ctx.addInitScript(ESPIAO);
      page = await ctx.newPage(); page.setDefaultTimeout(20000);
      await page.goto(alvo.url, {waitUntil: 'domcontentloaded', timeout: 60000});
      await page.waitForTimeout(5000);
      await fechaAvisos(page);
      const f5 = path.join(DEST, nome + '-cel.jpg');
      await page.screenshot({path: f5, ...JPG}); obs.fotos.push(path.basename(f5));
      obs.celular = await mede(page);
      const c = await candidato(page, 'clique');
      if (c) { try { await page.touchscreen.tap(c.box.x + c.box.width / 2, c.box.y + c.box.height / 2); await page.waitForTimeout(500);
        const f6 = path.join(DEST, nome + '-cel-toque.jpg'); await page.screenshot({path: f6, ...JPG}); obs.fotos.push(path.basename(f6)); } catch (e) {} }
      await ctx.close();
    } catch (e) {
      obs.erroCel = String(e.message).slice(0, 160); console.log('  erro celular: ' + obs.erroCel);
      try { await ctx.close(); } catch (e2) {}
    }
    fs.writeFileSync(path.join(DEST, nome + '.json'), JSON.stringify(obs, null, 1));
    relat.push(obs);
    const fr = obs.depois || obs.antes || [];
    console.log('  frames=' + (obs.frames || 0) + ' alvos=' + soma(fr, 'alvos') + ' arrasto=' + soma(fr, 'arrasto') +
                ' som=' + JSON.stringify(somaSom(fr)) + (obs.arrasto ? ' deslocou=' + obs.arrasto.deslocouPx + 'px mut=' + obs.arrasto.mutacoesEm1s : ' (sem arrasto)'));
  }
  await b.close();

  /* ---- o relatório que eu leio no chat ---- */
  const L = ['# 👀 VER RODANDO — atividades de referência jogadas por um Chromium (' + new Date().toISOString().slice(0, 10) + ')', '',
             '> Gerado por `_padrao/ver_rodando.js` no GitHub Actions (`ver-rodando.yml`). Fotos: PC 1024×600 antes / clique / arrastando / soltou; celular 412×820. **Matéria-prima, não regra.**', ''];
  L.push('| alvo | frames | alvos tocáveis | arrasto (n) | eventos que os alvos escutam | touch-action dos arrastáveis | alvo mín. | fonte mín. | animados | som (media/webaudio) | arrasto deslocou | mutações após soltar | draggable= | canvas/svg |');
  L.push('|---|--:|--:|--:|---|---|--:|--:|--:|---|--:|--:|--:|---|');
  for (const o of relat) {
    const fr = o.depois || o.antes || [];
    const tipos = {}; fr.forEach(f => Object.entries(f.tiposDeEvento || {}).forEach(([k, v]) => { tipos[k] = (tipos[k] || 0) + v; }));
    const ta = {}; fr.forEach(f => (f.exemplosArrasto || []).forEach(x => { ta[x.touchAction] = (ta[x.touchAction] || 0) + 1; }));
    const mins = fr.map(f => f.alvoMin).filter(Boolean), fmins = fr.map(f => f.fonteMin).filter(Boolean);
    const s = somaSom(fr);
    L.push('| **' + o.nome + '**' + (o.erroPC ? ' ⚠️' : '') + ' | ' + (o.frames || 0) + ' | ' + soma(fr, 'alvos') + ' | ' + soma(fr, 'arrasto') + ' | ' +
           Object.entries(tipos).filter(([k]) => /pointer|touch|mouse|click|key/.test(k)).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => k + ':' + v).join(' ') + ' | ' +
           Object.entries(ta).map(([k, v]) => k + ':' + v).join(' ') + ' | ' + (mins.length ? Math.min(...mins) : '—') + ' | ' + (fmins.length ? Math.min(...fmins) : '—') + ' | ' +
           soma(fr, 'animadosOuTransicoes') + ' | ' + s.media + '/' + s.webaudio + ' | ' + (o.arrasto ? (o.arrasto.deslocouPx === null ? '?' : o.arrasto.deslocouPx + 'px') : '—') + ' | ' +
           (o.arrasto ? o.arrasto.mutacoesEm1s : (o.clique ? o.clique.mutacoesEm1s + ' (clique)' : '—')) + ' | ' + soma(fr, 'draggableAttr') + ' | ' + soma(fr, 'canvas') + '/' + soma(fr, 'svg') + ' |');
  }
  L.push('', '## Fotos e detalhes por alvo', '');
  for (const o of relat) {
    L.push('### ' + o.nome, '', '`' + o.url + '`' + (o.titulo ? ' — ' + o.titulo : ''), '');
    if (o.erroPC) L.push('⚠️ PC: ' + o.erroPC);
    if (o.erroCel) L.push('⚠️ celular: ' + o.erroCel);
    if (o.avisoFechado) L.push('(fechei um aviso: "' + o.avisoFechado + '")');
    L.push('', o.fotos.map(f => '![' + f + '](' + f + ')').join(' '), '');
    const fr = o.depois || o.antes || [];
    const ex = fr.flatMap(f => f.exemplosArrasto || []).slice(0, 5);
    if (ex.length) { L.push('Arrastáveis (amostra):', ''); ex.forEach(x => L.push('- `' + x.tag + '.' + x.cls + '` ' + x.w + '×' + x.h + ' · eventos: ' + (x.ev || '—') + ' · touch-action: ' + x.touchAction + ' · cursor: ' + x.cursor + ' · transição: ' + x.transition + (x.draggable ? ' · draggable=' + x.draggable : ''))); L.push(''); }
    const ea = fr.flatMap(f => f.exemplosAlvos || []).slice(0, 5);
    if (ea.length) { L.push('Tocáveis (amostra):', ''); ea.forEach(x => L.push('- `' + x.tag + '.' + x.cls + '` ' + x.w + '×' + x.h + ' · "' + x.texto + '" · eventos: ' + (x.ev || '—') + (x.role ? ' · role=' + x.role : '') + (x.aria ? ' · aria-label' : ''))); L.push(''); }
    if (o.clique) L.push('Clique: ' + o.clique.mutacoesEm1s + ' mutações no 1º s · som media/webaudio ' + o.clique.somMedia + '/' + o.clique.somWebAudio);
    if (o.arrasto) L.push('Arrasto: deslocou ' + o.arrasto.deslocouPx + ' px · ' + o.arrasto.mutacoesEm1s + ' mutações após soltar · som ' + o.arrasto.somMedia + '/' + o.arrasto.somWebAudio);
    const doc = {}; fr.forEach(f => Object.entries(f.escutasNoDocumento || {}).forEach(([k, v]) => { doc[k] = (doc[k] || 0) + v; }));
    if (Object.keys(doc).length) L.push('Escutas no document/window: ' + Object.entries(doc).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([k, v]) => k + ':' + v).join(' '));
    L.push('', '---', '');
  }
  fs.writeFileSync(path.join(DEST, 'RODANDO.md'), L.join('\n'));
  console.log('\nrelatorio: ' + path.join(DEST, 'RODANDO.md') + ' (' + relat.length + ' alvos, ' + relat.reduce((a, o) => a + o.fotos.length, 0) + ' fotos)');
})();
