/* ============================================================
   PORTÃO DO TOQUE MEDIDO — "o dedo arrasta ou a tela rola?"

   ⚠️ LIÇÃO PAGA (set/2026, censo das 88 peças da fábrica). O `_qa/toque.py`
   confere `touch-action:none` por uma LISTA de mecânicas de arrasto (13 nomes).
   Lista é memória, e memória esquece: medindo no navegador, 19 mecânicas
   tinham elemento que ESCUTA o dedo (touchstart/pointerdown/mousedown) sem
   `touch-action` — base-dez, relógio, régua do `medir`, folha do `tracar-letra`,
   trilha do `tracar-caminho`, `montar-frase`, `rotular`, `raios-x`... Nenhuma
   estava na lista. No iPad da escola o gesto vira ROLAGEM e a peça some sob o
   dedo — o mesmo "não funciona" que a Feirinha teve em ago/2026.

   Este portão NÃO usa lista. Ele abre a atividade, marca todo elemento que
   recebe um ouvinte de dedo (envolvendo `addEventListener` antes da página
   rodar, e olhando as propriedades `onmousedown`/`ontouchstart`), monta cada
   fase pelo motor (`montaFase(i)`) — ou cada tela por nome, numa peça avulsa — e
   pergunta ao NAVEGADOR o `touch-action` computado de cada um. `none` ou
   `manipulation` passa; `auto` reprova e diz a mecânica e o seletor.

   Uso:  node _qa/toque.js <arquivo.html> [tela1 tela2 ...]
   Sai 0 = todo alvo blindado · 1 = alvo que rola sob o dedo · 2 = não medi.
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + '). ' +
              'Este portao roda na bancada local, onde ha Chromium.');
  process.exit(2);
}
const path = require('path');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const arq = process.argv[2];
  const telas = process.argv.slice(3);
  if (!arq) { console.log('uso: node _qa/toque.js <arquivo.html> [tela ...]'); process.exit(2); }
  const b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']});
  const p = await b.newPage({viewport: {width: 412, height: 820}});
  p.on('pageerror', () => {});
  /* antes de a página rodar: todo addEventListener de dedo deixa uma marca no elemento */
  await p.addInitScript(() => {
    const add = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function (t, fn, op) {
      if ((t === 'touchstart' || t === 'pointerdown' || t === 'mousedown') && this && this.nodeType === 1) {
        this.__escutaDedo = (this.__escutaDedo || '') + t + ' ';
      }
      return add.call(this, t, fn, op);
    };
  });
  await p.goto('file://' + path.resolve(arq));
  await p.waitForTimeout(500);

  const nFases = await p.evaluate(() =>
    (typeof montaFase === 'function' && typeof FASES !== 'undefined') ? FASES.length : 0);

  const mede = () => p.evaluate(() => {
    const raiz = document.getElementById('app') || document.body;
    const alvos = [...raiz.querySelectorAll('*')].filter(e => {
      const prop = ['onmousedown', 'ontouchstart', 'onpointerdown'].some(k => typeof e[k] === 'function');
      return (e.__escutaDedo || prop) && e.offsetParent !== null;
    });
    const sem = [], com = [];
    for (const e of alvos) {
      const ta = getComputedStyle(e).touchAction;
      const tag = e.tagName.toLowerCase() +
        (e.className ? '.' + String(e.className).trim().split(/\s+/).slice(0, 2).join('.') : '');
      (ta === 'none' || ta === 'manipulation' ? com : sem).push(tag);
    }
    return {sem: [...new Set(sem)], com: [...new Set(com)], total: alvos.length};
  });

  const porGrupo = {};
  const anota = (g, r) => {
    if (!porGrupo[g]) porGrupo[g] = {sem: new Set(), com: new Set(), total: 0};
    r.sem.forEach(x => porGrupo[g].sem.add(x)); r.com.forEach(x => porGrupo[g].com.add(x));
    porGrupo[g].total += r.total;
  };

  let medidas = 0;
  if (nFases) {
    for (let i = 0; i < nFases; i++) {
      try { await p.evaluate(i => montaFase(i, function () {}), i); } catch (e) { continue; }
      await p.waitForTimeout(80);
      const mec = await p.evaluate(i => FASES[i].mec || ('fase' + i), i);
      anota(mec, await mede()); medidas++;
    }
  } else if (telas.length) {
    /* peça avulsa ou atividade à mão: cada tela pelo nome */
    for (const t of telas) {
      const ok = await p.evaluate(t => { try { if (typeof window[t] === 'function') { window[t](); return true; } } catch (e) {} return false; }, t);
      if (!ok) continue;
      await p.waitForTimeout(120);
      anota(t, await mede()); medidas++;
    }
  }
  await b.close();

  if (!medidas) {
    console.log(arq + ' -> NAO MEDI o toque: sem motor de fases e sem tela por nome que abrisse.');
    process.exit(2);
  }
  const grupos = Object.keys(porGrupo).filter(g => porGrupo[g].total).sort();
  if (!grupos.length) {
    console.log(arq + ' -> ' + medidas + ' tela(s) medida(s): NAO SE APLICA — nenhum elemento escuta o dedo ' +
                '(nada de arrastar/tocar com mousedown ou touchstart). Nada a conferir.');
    process.exit(2);
  }
  let ruins = 0;
  console.log(arq + ' -> ' + medidas + ' tela(s) medida(s); ' + grupos.length + ' com elemento que escuta o dedo:');
  for (const g of grupos) {
    const d = porGrupo[g], sem = [...d.sem];
    if (sem.length) {
      ruins++;
      console.log('  ✗ ' + g + ': SEM touch-action -> ' + sem.slice(0, 4).join(' ; ') + (sem.length > 4 ? ' (+' + (sem.length - 4) + ')' : ''));
    }
  }
  if (ruins) {
    console.log('  ' + ruins + ' MECANICA(S) COM ALVO QUE ROLA SOB O DEDO (no iPad/Android o arrasto some).');
    console.log('  conserto: na PECA (_padrao/pecas/<mec>.html, dentro do <style>): ' +
                '`.seletor{-ms-touch-action:none;touch-action:none}` para o que se ARRASTA, ' +
                '`touch-action:manipulation` para o que so se TOCA. Depois integrar --escrever.');
    process.exit(1);
  }
  console.log('  toque ok: todo alvo que escuta o dedo tem touch-action (none/manipulation) — ' +
              grupos.length + ' mecanica(s) conferida(s) no navegador');
  process.exit(0);
})();
