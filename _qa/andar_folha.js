/* ============================================================
   ANDA O CADERNO DE FOLHA VIVA, FOLHA POR FOLHA — e reporta o que quebrou.

   ⭐ Por que ele existe (set/2026): quando se AUMENTA o pote de uma folha, o
      texto continua válido e todo portão de texto passa — mas a palavra nova
      pode não ter figura, não ter fala, ou faltar numa tabela de apoio que só
      aquela folha usa. Foi exatamente assim que o `TRIO` do `_som1` estourou:
      o pote cresceu e o gerador de falas morreu com KeyError. No navegador
      isso aparece na hora.

   O que ele mede, em cada uma das folhas:
     · erro de JS (pageerror e console.error);
     · figura que não carrega (404 e <img> com naturalWidth 0);
     · itens registrados (o `RESP` do caderno) — se uma folha registra ZERO,
       ela não tem o que a criança responda;
     · e no fim abre o relatório do professor, que é onde a conta se fecha.

   ⚠️ Precisa de http:// — o `localStorage` do "continuar de onde parou" não
      existe em file:// e o caderno passaria mentindo.

   Uso:  node _qa/andar_folha.js <pasta> [porta]
   Código 0 = andou inteiro sem erro · 1 = achou defeito · 2 = não deu para medir
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + ').');
  process.exit(2);
}
const { spawn } = require('child_process');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const pasta = (process.argv[2] || '').replace(/\/$/, '');
const porta = parseInt(process.argv[3] || '8791', 10);
if (!pasta) { console.log('uso: node _qa/andar_folha.js <pasta> [porta]'); process.exit(2); }

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(porta)], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 900));
  let ruim = 0;
  const b = await chromium.launch({ executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu'] });
  try {
    const pg = await b.newPage({ viewport: { width: 1024, height: 900 } });
    const erros = [], quebradas = [];
    pg.on('pageerror', e => erros.push(String(e).slice(0, 160)));
    pg.on('console', m => {
      if (m.type() !== 'error') return;
      const x = m.text();
      if (/Failed to load resource/.test(x)) return;   // o 404 ja e contado acima
      erros.push('console: ' + x.slice(0, 160));
    });
    // ⚠️ mp3 que falta NAO e defeito aqui: quem grava a voz e o `entregar.yml`,
    //    lendo o falas.json, na hora de publicar. Reprovar por isso ensinaria a
    //    ignorar este portao. Figura que falta, sim, e defeito.
    const semVoz = [];
    pg.on('response', r => {
      if (r.status() !== 404) return;
      const f = r.url().split('/').pop().split('?')[0];
      (/\.mp3$/i.test(f) ? semVoz : quebradas).push(f);
    });

    await pg.goto(`http://127.0.0.1:${porta}/${pasta}/index.html`, { waitUntil: 'load' });
    await pg.waitForTimeout(700);
    await pg.fill('#nomeIn', 'Ana').catch(() => {});
    await pg.click('#bComecar').catch(() => {});
    await pg.waitForTimeout(500);

    const total = await pg.evaluate(() => (typeof PAGEL !== 'undefined' ? PAGEL.length : 0));
    if (!total) { console.log(pasta + ' -> NAO MEDI: nao achei o PAGEL do caderno.'); process.exit(2); }

    const linhas = [];
    for (let i = 1; i < total; i++) {
      await pg.evaluate(n => vaiPara(n), i);
      await pg.waitForTimeout(320);
      const m = await pg.evaluate(n => {
        const daPag = Object.keys(RESP).filter(k => RESP[k].pag === n);
        const imgs = Array.prototype.slice.call(document.querySelectorAll('.pagina.viva img'));
        const vazias = imgs.filter(im => im.complete && im.naturalWidth === 0)
          .map(im => (im.getAttribute('src') || '').split('/').pop());
        const nome = (typeof NOMES !== 'undefined' && NOMES[n - 1]) || ('folha ' + n);
        return { itens: daPag.length, vazias: vazias, nome: nome };
      }, i);
      if (!m.itens) { ruim = 1; linhas.push(`   ⛔ folha ${i} (${m.nome}): NENHUM item registrado`); }
      else if (m.vazias.length) { ruim = 1; linhas.push(`   ⛔ folha ${i} (${m.nome}): figura que nao carrega -> ${m.vazias.join(', ')}`); }
      else linhas.push(`   ✓ folha ${i} (${m.nome}): ${m.itens} itens`);
    }

    // o fecho: responder tudo certo e abrir o relatório do professor
    const fim = await pg.evaluate(() => {
      let n = 0;
      for (const id in RESP) { tentativa(id, true); n++; }
      fim();
      return n;
    }).catch(e => { erros.push('fim(): ' + String(e).slice(0, 120)); return 0; });
    await pg.waitForTimeout(600);
    await pg.evaluate(() => { if (typeof abreRelatorio === 'function') abreRelatorio(); }).catch(() => {});
    await pg.waitForTimeout(400);
    const rel = await pg.evaluate(() => {
      const r = document.getElementById('relatorio');
      return r ? { aberto: r.style.display === 'block', linhas: r.querySelectorAll('table tr').length - 1 } : null;
    });

    console.log(`${pasta} -> andou ${total - 1} folha(s); ${fim} itens no total`);
    linhas.forEach(l => console.log(l));
    if (!rel || !rel.aberto || rel.linhas < 1) { ruim = 1; console.log('   ⛔ o relatorio do professor nao abriu'); }
    else console.log(`   ✓ relatorio do professor abriu com ${rel.linhas} objetivo(s)`);
    const q = Array.from(new Set(quebradas));
    if (q.length) { ruim = 1; console.log('   ⛔ arquivo que nao existe: ' + q.join(', ')); }
    const v = Array.from(new Set(semVoz));
    if (v.length) console.log(`   (voz ainda sem mp3: ${v.length} — o entregar.yml grava ao publicar)`);
    if (erros.length) { ruim = 1; console.log('   ⛔ erro de JS: ' + Array.from(new Set(erros)).join(' | ')); }
    if (!ruim) console.log('   ✓ sem erro de JS, sem figura quebrada');
  } finally {
    await b.close().catch(() => {});
    srv.kill();
  }
  process.exit(ruim);
})();
