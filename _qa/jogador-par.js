// -*- js -*-
// JOGADOR EM PARALELO — roda o _qa/jogador.js em SEGMENTOS ao mesmo tempo.
//
// Motivo (set/2026): a banca inteira estourou o tempo (560s) porque o jogador
// joga as fases UMA por UMA; numa atividade de 24 fases sao ~20 min. O jogador.js
// JA sabe jogar um TRECHO (env JSTART=fase inicial, JSTOP=fase final) — este
// orquestrador so parte a atividade em K trechos e roda os K de uma vez, cada um
// no seu Chromium. A uniao dos trechos cobre todas as fases; o ULTIMO trecho vai
// sem JSTOP e exige a MEDALHA (fim de verdade). Em serie (jogador.js sozinho)
// nada muda — isto e so a versao rapida.
//
// Uso:  node _qa/jogador-par.js <arquivo.html> [K]     (K = nº de trechos, def 4)
// Sai 0 se TODOS os trechos passaram; 1 se qualquer um reprovou/travou.

const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const {spawn} = require('child_process');
const path = require('path');

const ARQ = process.argv[2];
if (!ARQ) { console.error('uso: node _qa/jogador-par.js <arquivo.html> [K]'); process.exit(2); }
let K = parseInt(process.argv[3] || '4', 10); if (!(K >= 1)) K = 4;

// quantas fases tem a atividade? (uma abertura rapida do motor)
async function contaFases() {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-gpu']
  });
  const p = await b.newPage({viewport: {width: 412, height: 820}});
  await p.goto('file://' + path.resolve(ARQ));
  await p.waitForTimeout(500);
  const n = await p.evaluate(() => {
    if (typeof FASES !== 'undefined' && FASES && FASES.length) return FASES.length;
    if (typeof QUESTOES !== 'undefined' && QUESTOES && QUESTOES.length) return QUESTOES.length;
    return 0;
  });
  await b.close();
  return n;
}

function rodaTrecho(jstart, jstop, rotulo) {
  return new Promise((resolve) => {
    const env = Object.assign({}, process.env);
    if (jstart != null) env.JSTART = String(jstart);
    if (jstop != null) env.JSTOP = String(jstop);
    const cp = spawn('node', [path.join(__dirname, 'jogador.js'), ARQ], {env});
    let out = '';
    cp.stdout.on('data', d => out += d);
    cp.stderr.on('data', d => out += d);
    cp.on('close', code => resolve({rotulo, code, out}));
  });
}

(async () => {
  let n = 0;
  try { n = await contaFases(); } catch (e) { n = 0; }

  // sem contagem confiavel OU atividade pequena -> serial (1 trecho, sem corte)
  if (!n || n <= 6 || K <= 1) {
    const r = await rodaTrecho(null, null, 'serial');
    process.stdout.write(r.out);
    console.log(r.code === 0 ? 'jogador-par: 1 trecho (serial) — OK' : 'jogador-par: reprovou (serial)');
    process.exit(r.code);
  }

  K = Math.min(K, Math.ceil(n / 3));       // no minimo ~3 fases por trecho
  const tam = Math.ceil(n / K);
  const trechos = [];
  for (let i = 0; i < K; i++) {
    const ini = i * tam;
    if (ini >= n) break;
    const ehUltimo = (i === K - 1) || (ini + tam >= n);
    // JSTOP = a fase onde o trecho fecha; o ultimo NAO tem JSTOP (exige medalha).
    const stop = ehUltimo ? null : Math.min(ini + tam, n - 1);
    trechos.push({ini, stop, rot: 'fases ' + ini + '..' + (ehUltimo ? (n - 1) + ' (medalha)' : stop)});
  }

  console.log('jogador-par: ' + n + ' fases em ' + trechos.length + ' trecho(s) paralelo(s)');
  const res = await Promise.all(trechos.map(t => rodaTrecho(t.ini, t.stop, t.rot)));

  let falhou = 0;
  for (const r of res) {
    const okTxt = r.code === 0 ? 'OK' : 'REPROVOU';
    console.log('  [' + r.rotulo + '] ' + okTxt);
    if (r.code !== 0) {
      falhou = 1;
      // so o log do trecho que falhou (o resto e ruido)
      process.stdout.write(r.out.split('\n').slice(-18).join('\n') + '\n');
    }
  }
  console.log(falhou ? 'jogador-par: ALGUM trecho reprovou' : 'jogador-par: todos os trechos passaram');
  process.exit(falhou);
})();
