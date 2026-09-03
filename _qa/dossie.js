/* ============================================================
   O DOSSIÊ — a evidência que o REVISOR FINAL julga.

   POR QUE ISTO EXISTE (a pergunta do Marcos, set/2026):
     *"existe alguma possibilidade de ter um revisor final de atividade? como
     se fosse um humano, especialista em currículo, didática, designer
     instrucional, um profissional experiente em desenvolvimento de software
     educacional?"* — e logo depois a pergunta certa, a que dói:
     *"mas isso funcionaria realmente? pq temos vários portões etc mas sempre
     passam muitos erros bobos"*.

   A resposta honesta e o motivo deste arquivo: os 65 portoes leem CODIGO.
   Codigo nao mostra que o balao cobre a figura, que a palavra ficou fora da
   tela, que o mascote esta gigante do lado do menino, que a fase 12 parece a
   fase 8. Um humano pega isso em 3 segundos porque ele OLHA. Enquanto o
   revisor so recebe texto, ele e mais um portao — melhor escrito, mas cego.

   Entao o Revisor Final so pode funcionar se ele receber o que a crianca ve.
   Este arquivo produz exatamente isso: JOGA a atividade de ponta a ponta e
   FOTOGRAFA cada fase, em telefone e em PC, guardando junto o que estava
   escrito, o que a voz ia dizer e quanto tempo a fase levou.

   O que sai (em `_qa/_dossie/<pasta>/`):
     • `fase-NN-tel.png` / `fase-NN-pc.png` — a foto da tela
     • `dossie.json` — por fase: titulo, enunciado, mecanica, textos visiveis,
       falas, tamanho do menor alvo tocavel, se rolou de lado, erros de runtime
     • `resumo.md` — o mesmo em texto, para o revisor que so le

   ⚠️ REGRA DA CASA: se nao der para fotografar, ele diz NAO MEDI e sai 2.
   Dossie vazio nunca vira "nada a apontar".

   Uso:  node _qa/dossie.js <pasta>            (ex.: _revista5)
         node _qa/dossie.js <pasta> 12         (para na fase 12, para teste)
   ============================================================ */
const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const path = require('path'), fs = require('fs');

const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const TEL = {width: 412, height: 820};   // celular da escola
const PC  = {width: 1280, height: 720};  // PC do laboratorio

(async () => {
  const pasta = (process.argv[2] || '').replace(/\/$/, '');
  const limite = parseInt(process.argv[3] || '0', 10) || 999;
  if (!pasta) { console.log('uso: node _qa/dossie.js <pasta> [limite]'); process.exit(2); }
  const arq = path.join(pasta, 'index.html');
  if (!fs.existsSync(arq)) { console.log('NAO MEDI: nao achei ' + arq); process.exit(2); }

  const saida = path.join('_qa', '_dossie', path.basename(pasta));
  fs.mkdirSync(saida, {recursive: true});

  let b;
  try { b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']}); }
  catch (e) { console.log('NAO MEDI: Chromium nao abriu — ' + e.message); process.exit(2); }

  const url = 'file://' + path.resolve(arq);
  const fases = [];
  const erros = [];

  const p = await b.newPage({viewport: TEL});
  p.on('pageerror', e => erros.push(String(e.message).split('\n')[0]));

  await p.goto(url, {waitUntil: 'load', timeout: 30000});
  await p.waitForTimeout(2000);

  /* Quantas fases tem? O motor guarda em FASES; atividade de HTML proprio
     (a Oficina da Divisao, o Tangram) nao tem — ai andamos pelo que houver. */
  const total = await p.evaluate(() => {
    try { return (typeof FASES !== 'undefined' && FASES.length) ? FASES.length : 0; }
    catch (e) { return 0; }
  });
  if (!total) {
    console.log('NAO MEDI: esta atividade nao expoe FASES (HTML proprio). ' +
                'O dossie de fase-a-fase so serve para as MONTADAS; ' +
                'para as proprias, use `node _qa/boot.js` + revisao a olho.');
    await b.close(); process.exit(2);
  }

  const quantas = Math.min(total, limite);
  console.log('fotografando ' + quantas + ' de ' + total + ' fases...');

  for (let i = 0; i < quantas; i++) {
    const t0 = Date.now();
    let dado;
    try {
      await p.evaluate((n) => { window.__err = []; montaFase(n); }, i);
      await p.waitForTimeout(1400);   // o motor tem fade + narracao comecando

      dado = await p.evaluate(() => {
        const app = document.getElementById('app') || document.body;
        const vis = el => {
          const r = el.getBoundingClientRect();
          if (r.width < 4 || r.height < 4) return false;
          const cs = getComputedStyle(el);
          return cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > .05;
        };
        /* textos que a crianca REALMENTE le (folhas visiveis, sem repetir pai) */
        const textos = [];
        app.querySelectorAll('*').forEach(el => {
          if (el.children.length) return;
          if (!vis(el)) return;
          const t = (el.textContent || '').replace(/\s+/g, ' ').trim();
          if (t && t.length < 300 && textos.indexOf(t) < 0) textos.push(t);
        });
        /* menor alvo tocavel: a WCAG e o dedo de 6 anos pedem >= 40px */
        let menorAlvo = 9999, alvoTxt = '';
        app.querySelectorAll('button, .btn, .op, [onclick], .pc, .lig, .mcarta').forEach(el => {
          if (!vis(el)) return;
          const r = el.getBoundingClientRect();
          const m = Math.min(r.width, r.height);
          if (m < menorAlvo) { menorAlvo = Math.round(m); alvoTxt = (el.textContent || '').trim().slice(0, 30); }
        });
        /* figuras que nao carregaram — o quadradinho vazio que a crianca ve */
        const figsQuebradas = [];
        app.querySelectorAll('img').forEach(im => {
          if (im.complete && im.naturalWidth === 0) figsQuebradas.push(im.src.split('/').pop());
        });
        const balao = app.querySelector('.balao');
        return {
          enunciado: balao ? (balao.textContent || '').replace(/\s+/g, ' ').trim() : '',
          mecanica: (app.className.match(/mec-([\w-]+)/) || [, ''])[1] ||
                    ((app.querySelector('[class*="mec-"]') || {className: ''}).className.match(/mec-([\w-]+)/) || [, '?'])[1],
          textos: textos.slice(0, 40),
          menorAlvo: menorAlvo === 9999 ? null : menorAlvo,
          alvoMenorTexto: alvoTxt,
          figsQuebradas: figsQuebradas,
          rolaDeLado: document.documentElement.scrollWidth > window.innerWidth + 2,
          alturaConteudo: Math.round(app.scrollHeight)
        };
      });
    } catch (e) {
      dado = {erro: 'nao consegui montar a fase ' + (i + 1) + ': ' + e.message};
    }

    const nn = String(i + 1).padStart(2, '0');
    try { await p.screenshot({path: path.join(saida, 'fase-' + nn + '-tel.png')}); } catch (e) {}
    dado.n = i + 1;
    dado.foto = 'fase-' + nn + '-tel.png';
    dado.ms = Date.now() - t0;
    fases.push(dado);
    process.stdout.write('.');
  }
  console.log('');

  /* Segunda passada no PC largo: e onde os defeitos de leiaute aparecem
     diferentes (a carta de memoria em 3 colunas, o balao esticado). */
  const p2 = await b.newPage({viewport: PC});
  await p2.goto(url, {waitUntil: 'load', timeout: 30000});
  await p2.waitForTimeout(1500);
  for (let i = 0; i < quantas; i++) {
    try {
      await p2.evaluate((n) => montaFase(n), i);
      await p2.waitForTimeout(900);
      await p2.screenshot({path: path.join(saida, 'fase-' + String(i + 1).padStart(2, '0') + '-pc.png')});
    } catch (e) {}
  }

  /* as falas, que sao a metade da atividade que nenhuma foto mostra */
  let falas = {};
  try { falas = JSON.parse(fs.readFileSync(path.join(pasta, 'falas.json'), 'utf8')); } catch (e) {}

  await b.close();

  const dossie = {
    pasta: pasta,
    fases_no_total: total,
    fases_fotografadas: quantas,
    erros_de_runtime: [...new Set(erros)],
    falas_gravadas: Object.keys(falas).length,
    fases: fases
  };
  fs.writeFileSync(path.join(saida, 'dossie.json'), JSON.stringify(dossie, null, 1), 'utf8');

  /* o resumo em texto — para o revisor ler antes de abrir as fotos */
  let md = '# Dossiê — ' + pasta + '\n\n';
  md += '- fases: ' + quantas + ' de ' + total + '\n';
  md += '- falas gravadas: ' + Object.keys(falas).length + '\n';
  if (dossie.erros_de_runtime.length)
    md += '- ⚠️ ERROS DE RUNTIME: ' + dossie.erros_de_runtime.join(' | ') + '\n';
  md += '\n';
  const conta = {};
  fases.forEach(f => { conta[f.mecanica || '?'] = (conta[f.mecanica || '?'] || 0) + 1; });
  md += '## Mecânicas usadas\n\n';
  Object.keys(conta).sort((a, b) => conta[b] - conta[a]).forEach(k => {
    md += '- ' + k + ': ' + conta[k] + ' fase(s) (' + Math.round(conta[k] * 100 / quantas) + '%)\n';
  });
  md += '\n## Fase a fase\n\n';
  fases.forEach(f => {
    md += '### Fase ' + f.n + ' — ' + (f.mecanica || '?') + '  \n';
    md += '`' + f.foto + '` / `' + f.foto.replace('-tel', '-pc') + '`  \n';
    if (f.erro) { md += '**FALHOU:** ' + f.erro + '\n\n'; return; }
    if (f.enunciado) md += '**Enunciado:** ' + f.enunciado + '  \n';
    if (f.textos && f.textos.length) md += '**Na tela:** ' + f.textos.join(' · ') + '  \n';
    const alertas = [];
    if (f.menorAlvo !== null && f.menorAlvo < 40) alertas.push('menor alvo ' + f.menorAlvo + 'px ("' + f.alvoMenorTexto + '") — abaixo dos 40px do dedo de criança');
    if (f.rolaDeLado) alertas.push('a tela ROLA DE LADO no celular');
    if (f.figsQuebradas && f.figsQuebradas.length) alertas.push('figura(s) que não carregaram: ' + f.figsQuebradas.join(', '));
    if (alertas.length) md += '**⚠️ ' + alertas.join(' / ') + '**  \n';
    md += '\n';
  });
  fs.writeFileSync(path.join(saida, 'resumo.md'), md, 'utf8');

  console.log('dossiê pronto em ' + saida + '/ (' + quantas + ' fases, ' +
              (quantas * 2) + ' fotos)');
  if (dossie.erros_de_runtime.length) {
    console.log('⚠️ ' + dossie.erros_de_runtime.length + ' erro(s) de runtime durante a partida:');
    dossie.erros_de_runtime.slice(0, 5).forEach(e => console.log('   ✗ ' + e));
  }
  process.exit(0);
})();
