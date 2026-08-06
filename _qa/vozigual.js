/* ============================================================
   O ÁUDIO DIZ EXATAMENTE O QUE ESTÁ ESCRITO?
   ------------------------------------------------------------
   Pedido do Marcos (ago/2026): *"seria interessante que o áudio
   ao lado das instruções falasse exatamente o que está escrito,
   favor verificar a escrita se está correta, isso em toda
   atividade"*.

   Ele tem razão e o motivo é simples: esse botão existe para
   quem NÃO LÊ. Se a tela pede uma coisa e a voz conta outra —
   mesmo que as duas sejam boas —, a criança que depende da voz
   está recebendo uma instrução diferente da que está na frente
   dela. E quem lê devagar, tentando acompanhar a voz com o dedo
   no texto, se perde.

   Este portão ABRE cada fase, lê o texto do balão como a criança
   vê, descobre qual áudio o alto-falante repete (`falaTela`) e
   compara com o texto daquele áudio, guardado em
   `<pasta>/falas.json`. Diferença de acento, vírgula e caixa não
   conta; palavra diferente conta.

   ⚠️ O `falas.json` é o que torna isto possível: sem guardar o
   TEXTO de cada narração junto da atividade, não há como saber
   o que a voz diz — o mp3 não se lê. Toda atividade nova nasce
   com ele.

   USO   node _qa/vozigual.js _mapa/index.html
   ============================================================ */
const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const path = require('path');
const fs = require('fs');

const norm = t => (t || '').toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^\w ]/g, ' ').replace(/\s+/g, ' ').trim();

(async () => {
  const arq = process.argv[2];
  if (!arq) { console.log('uso: node _qa/vozigual.js <arquivo.html>'); process.exit(2); }
  const pasta = path.dirname(path.resolve(arq));
  const camFalas = path.join(pasta, 'falas.json');
  if (!fs.existsSync(camFalas)) {
    console.log('%s -> sem falas.json: nao da para saber o que a voz diz.', arq);
    console.log('   crie <pasta>/falas.json com [{"id":"...","texto":"..."}] — e o texto');
    console.log('   de cada narracao, o mesmo que foi para o gerador de voz.');
    process.exit(1);
  }
  const falas = {};
  for (const f of JSON.parse(fs.readFileSync(camFalas, 'utf8'))) falas[f.id] = f.texto;

  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                                   args: ['--no-sandbox', '--disable-gpu']});
  const p0 = await b.newPage();
  await p0.goto('file://' + path.resolve(arq)); await p0.waitForTimeout(400);
  const fases = await p0.evaluate(() => FASES_MESTRE.map(f => f[0]).filter(f => f !== 'mFim'));
  await p0.close();

  let iguais = 0; const problemas = [];
  for (const f of fases) {
    const p = await b.newPage({viewport: {width: 412, height: 820}});
    await p.goto('file://' + path.resolve(arq)); await p.waitForTimeout(250);
    /* ⚠️ `depoisDaFala` TAMBEM narra — e por ela que passa o `introEPergunta()`,
       que e como quase toda fase toca a abertura. Com o antigo stub vazio, o
       portao dizia "a tela nao tem voz nenhuma" numa fase FALADA (o porao do
       navio). Portao que acusa quem esta certo ensina a ignorar portao.    */
    await p.evaluate(() => { window.falar = function (id) { window.falaAtual = id; if (!window.__t) window.__t = id; };
                             window.depoisDaFala = function (id) { if (!window.__t) window.__t = id; }; });
    try { await p.evaluate(n => { window[n](); }, f); } catch (e) {}
    await p.waitForTimeout(380);
    const r = await p.evaluate(() => {
      const bal = document.querySelector('.tela .balao:not(.pequeno)');
      return {id: (typeof falaTela !== 'undefined' && falaTela) || window.__t || null,
              txt: bal ? bal.textContent.replace(/\s+/g, ' ').trim() : ''};
    });
    await p.close();
    if (!r.txt) continue;                       // tela sem enunciado
    if (!r.id) { problemas.push([f, 'a tela nao tem voz nenhuma', r.txt]); continue; }
    const voz = falas[r.id];
    if (voz === undefined) { problemas.push([f, 'falta o texto de ' + r.id + ' no falas.json', r.txt]); continue; }
    if (norm(voz) === norm(r.txt)) { iguais++; continue; }
    problemas.push([f, r.id, 'tela: ' + r.txt + '\n        voz : ' + voz]);
  }
  await b.close();

  console.log('%s -> %d fase(s) com a voz IGUAL ao texto escrito', arq, iguais);
  if (problemas.length) {
    console.log('   %d FASE(S) EM QUE A VOZ NAO DIZ O QUE ESTA ESCRITO:', problemas.length);
    for (const [f, id, det] of problemas.slice(0, 8)) console.log('    - %s [%s]\n        %s', f, id, det);
    console.log('   conserto: regravar a fala com o texto DA TELA (o botao existe para quem nao le).');
    process.exit(1);
  }
  console.log('   voz ok: o alto-falante fala exatamente o que a crianca ve escrito');
})();
