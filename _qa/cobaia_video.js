/* ============================================================
   COBAIA DA OFICINA DE VÍDEO — o robô que USA o editor.
   ⚠️ NASCEU DE UMA REGRA DA CASA, não de um capricho: *"nunca afirmar que
   funciona sem testar"*. Um editor de vídeo passa em `node --check`, passa no
   portão de leiaute, abre bonito no print — e mesmo assim pode não gravar um
   quadro sequer. O que prova um editor é EXPORTAR: se sai um arquivo com bytes
   dentro, a corrente inteira funcionou (canvas → captureStream → MediaRecorder
   → Blob), porque cada elo dela é obrigatório para o seguinte.

   O que ele faz, na ordem em que uma criança faria:
     1. abre o editor por HTTP (⚠️ em `file://` o navegador nega câmera,
        microfone e às vezes o próprio `captureStream` — teste em `file://`
        passa mentindo);
     2. fecha a tela de boas-vindas;
     3. manda fazer o CLIPE DE EXEMPLO (que já exercita MediaRecorder);
     4. apara, divide, muda a ordem, põe texto, transição, velocidade, figura;
     5. TOCA e mede quantos quadros por segundo a prévia consegue;
     6. EXPORTA e confere que saiu arquivo com tamanho;
     7. desfaz e confere que o projeto voltou.

   Uso:  node _qa/cobaia_video.js _video69/index.html
   Códigos: 0 passou · 1 REPROVADO · 2 não deu para medir
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  try { chromium = require('playwright').chromium; }
  catch (e2) { console.log('cobaia video: NAO MEDI (playwright ausente)'); process.exit(2); }
}
const path = require('path'), fs = require('fs'), http = require('http');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const alvo = process.argv[2] || '_video69/index.html';
const abs = path.resolve(alvo);
if (!fs.existsSync(abs)) { console.log('cobaia video: NAO MEDI (nao achei ' + alvo + ')'); process.exit(2); }

const raiz = path.dirname(abs);
const falhas = [], notas = [];

function servidor() {
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      let f = decodeURIComponent(req.url.split('?')[0]);
      if (f === '/') f = '/' + path.basename(abs);
      const c = path.join(raiz, f);
      if (!c.startsWith(raiz) || !fs.existsSync(c)) { res.writeHead(404); res.end(); return; }
      const ext = path.extname(c).toLowerCase();
      const tipo = ext === '.html' ? 'text/html; charset=utf-8'
        : ext === '.js' ? 'text/javascript' : ext === '.css' ? 'text/css'
        : ext === '.png' ? 'image/png' : 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': tipo });
      res.end(fs.readFileSync(c));
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}

(async () => {
  const srv = await servidor();
  const porta = srv.address().port;
  const b = await chromium.launch({
    executablePath: fs.existsSync(CROMO) ? CROMO : undefined,
    args: ['--no-sandbox', '--disable-gpu',
      /* ⚠️ sem estes três o robô trava numa caixa de permissão que ninguém
         clica, e o teste "falha" por motivo que não é do editor. */
      '--use-fake-ui-for-media-capture',
      '--use-fake-device-for-media-stream',
      '--autoplay-policy=no-user-gesture-required']
  });
  const pg = await b.newPage({ viewport: { width: 1366, height: 768 } });

  const erros = [];
  pg.on('pageerror', e => erros.push(String(e.message || e)));
  pg.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text()); });

  /* o download do vídeo exportado: interceptado para poder ser medido */
  await pg.context().grantPermissions(['microphone', 'camera'], { origin: 'http://127.0.0.1:' + porta });
  let baixado = null;
  pg.on('download', async d => {
    try {
      const p = path.join(require('os').tmpdir(), 'cobaia-' + d.suggestedFilename());
      await d.saveAs(p);
      baixado = { nome: d.suggestedFilename(), bytes: fs.statSync(p).size };
      fs.unlinkSync(p);
    } catch (e) { baixado = { nome: d.suggestedFilename(), bytes: -1 }; }
  });

  await pg.goto('http://127.0.0.1:' + porta + '/', { waitUntil: 'load' });
  await pg.waitForTimeout(400);

  async function eu(f, ...a) { return await pg.evaluate(f, ...a); }
  function exige(cond, texto) { if (!cond) falhas.push(texto); }

  /* ---- 1. a tela de boas-vindas abre e fecha ---- */
  const temModal = await eu(() => document.getElementById('veu').classList.contains('on'));
  exige(temModal, 'a tela de boas-vindas nao apareceu');
  await pg.click('#mdOk');
  await pg.waitForTimeout(120);
  exige(!(await eu(() => document.getElementById('veu').classList.contains('on'))),
    'a tela de boas-vindas nao fecha no botao');

  /* ---- 2. o clipe de exemplo (exercita MediaRecorder de saida) ---- */
  await pg.click('[data-qa="f-material"]');
  await pg.waitForTimeout(150);
  await pg.click('[data-qa="exemplo"]');
  await pg.waitForTimeout(5200);
  let n = await eu(() => PROJ.clipes.length);
  exige(n >= 1, 'o clipe de exemplo nao entrou na fita (MediaRecorder nao gravou)');
  if (n < 1) { await fim(b, srv); return; }
  notas.push('clipe de exemplo: ' + (await eu(() => Math.round(durTotal() * 10) / 10)) + ' s');

  /* ---- 3. a miniatura da fita ---- */
  await pg.waitForTimeout(900);
  exige(await eu(() => !!PROJ.clipes[0].mini), 'o pedaco da fita ficou sem miniatura');

  /* ---- 4. aparar encurta de verdade ---- */
  const antes = await eu(() => durTotal());
  await eu(() => { PROJ.clipes[0].fim = PROJ.clipes[0].fonteDur * 0.6; tudo(); });
  const depois = await eu(() => durTotal());
  exige(depois < antes - 0.2, 'aparar nao mudou a duracao do projeto');

  /* ---- 5. dividir faz dois pedacos do MESMO arquivo ---- */
  await eu(() => { TEMPO = durTotal() / 2; });
  await pg.click('[data-qa="f-aparar"]');
  await pg.waitForTimeout(140);
  await pg.click('[data-qa="dividir"]');
  await pg.waitForTimeout(160);
  exige(await eu(() => PROJ.clipes.length === 2 && PROJ.clipes[0].el === PROJ.clipes[1].el),
    'dividir nao gerou dois clipes apontando para o mesmo material');

  /* ---- 6. trocar a ordem ---- */
  const id0 = await eu(() => PROJ.clipes[0].id);
  await eu(() => { selecionar('clipes', 1); mover(-1); });
  exige(await eu(i => PROJ.clipes[1].id === i, id0), 'mover nao trocou os clipes de lugar');

  /* ---- 7. texto, transicao, velocidade, figura ---- */
  await pg.click('[data-qa="f-texto"]');
  await pg.waitForTimeout(140);
  await pg.click('[data-qa="texto"]');
  await pg.waitForTimeout(180);
  exige(await eu(() => PROJ.textos.length === 1), 'o texto nao entrou');

  await eu(() => { PROJ.clipes[1].transicao = { tipo: 'fade', dur: 0.5 };
                   PROJ.clipes[0].vel = 2; tudo(); });
  exige(await eu(() => Math.abs(durClipe(PROJ.clipes[0]) -
        (PROJ.clipes[0].fim - PROJ.clipes[0].ini) / 2) < 0.01),
    'a velocidade nao mexeu na duracao do pedaco');

  /* ---- 8. o palco desenha mesmo (o quadro nao e preto) ---- */
  const tinta = await eu(() => {
    desenha(durTotal() * 0.3);
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    let soma = 0, i;
    for (i = 0; i < d.length; i += 40) soma += d[i] + d[i + 1] + d[i + 2];
    return soma;
  });
  exige(tinta > 0, 'o palco desenhou um quadro inteiramente preto');

  /* ---- 9. tocar e MEDIR os quadros por segundo ---- */
  await eu(() => { TEMPO = 0; tocar(); });
  await pg.waitForTimeout(2600);
  const fps = await eu(() => fpsMost);
  const andou = await eu(() => TEMPO > 0.5);
  exige(andou, 'o tempo nao andou ao tocar');
  notas.push('prevía neste computador: ' + fps + ' fps (o PC da escola e mais lento)');
  await eu(() => pausar());

  /* ---- 10. EXPORTAR — a prova de fogo ---- */
  await eu(() => {
    /* encurta o projeto para o teste nao levar minutos: a exportacao e em
       tempo real, entao um projeto de 2 s leva 2 s. */
    PROJ.clipes.length = 1;
    PROJ.clipes[0].ini = 0; PROJ.clipes[0].fim = Math.min(2, PROJ.clipes[0].fonteDur);
    PROJ.clipes[0].vel = 1;
    PROJ.textos.length = 0; tudo();
  });
  await pg.click('[data-qa="exportar"]');
  await pg.waitForTimeout(6000);
  exige(!!baixado, 'a exportacao nao produziu arquivo nenhum');
  if (baixado) {
    exige(baixado.bytes > 2000, 'o arquivo exportado saiu vazio (' + baixado.bytes + ' bytes)');
    notas.push('exportou ' + baixado.nome + ' com ' + Math.round(baixado.bytes / 1024) + ' KB');
  }

  /* ⚠️ a exportacao abre a janela do resultado; se ela ficar aberta, todo
     clique seguinte bate no veu e o teste "falha" por motivo que nao e do
     editor. Fechar faz parte do passo. */
  if (await eu(() => document.getElementById('veu').classList.contains('on')))
    await pg.click('#mdOk');
  await pg.waitForTimeout(150);

  /* ---- 10b. ACERVO: a foto desenhada pelo proprio programa ---- */
  const antesA = await eu(() => PROJ.clipes.length);
  await pg.click('[data-qa="f-acervo"]');
  await pg.waitForTimeout(160);
  await pg.click('#acFotos [data-v="titulo"]');
  await pg.waitForTimeout(700);
  exige(await eu(a => PROJ.clipes.length === a + 1, antesA), 'a foto do acervo nao entrou');

  /* ---- 10c. ACERVO: o efeito sonoro SINTETIZADO ---- */
  await pg.click('#acEfeitos [data-v="ding"]');
  await pg.waitForTimeout(1500);
  exige(await eu(() => PROJ.audios.length >= 1), 'o efeito sonoro nao foi sintetizado');
  if (await eu(() => PROJ.audios.length >= 1))
    exige(await eu(() => PROJ.audios[0].el && PROJ.audios[0].el.duration > 0.05),
      'o som sintetizado saiu com duracao zero (o WAV esta mal montado)');

  /* ---- 10d. ACERVO: a trilha COMPOSTA ---- */
  const antesM = await eu(() => PROJ.audios.length);
  await pg.click('#acTrilhas [data-v="alegre"]');
  await pg.waitForTimeout(4000);
  exige(await eu(a => PROJ.audios.length === a + 1, antesM), 'a trilha nao foi composta');

  /* ---- 10e. CONGELAR ---- */
  const antesC = await eu(() => PROJ.clipes.length);
  await eu(() => { TEMPO = 0.5; selecionar('clipes', 0); });
  await pg.click('[data-qa="f-aparar"]');
  await pg.waitForTimeout(140);
  await pg.click('#btCongela');
  await pg.waitForTimeout(600);
  exige(await eu(a => PROJ.clipes.length === a + 1, antesC), 'congelar nao criou o quadro parado');

  /* ---- 10f. CORTAR muda a imagem de verdade ---- */
  const t1 = await eu(() => { desenha(0.3, true);
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data; let s = 0, i;
    for (i = 0; i < d.length; i += 40) s += d[i] + d[i+1] + d[i+2]; return s; });
  await eu(() => { PROJ.clipes[0].crop = {x:0.3, y:0.3, w:0.4, h:0.4}; });
  const t2 = await eu(() => { desenha(0.3, true);
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data; let s = 0, i;
    for (i = 0; i < d.length; i += 40) s += d[i] + d[i+1] + d[i+2]; return s; });
  exige(t1 !== t2, 'cortar o quadro nao mudou a imagem desenhada');
  await eu(() => { PROJ.clipes[0].crop = null; });

  /* ---- 10g. MOLDURA pinta a borda ---- */
  await eu(() => { PROJ.borda = {larg: 6, cor: '#ff0000'}; desenha(0.3); });
  const canto = await eu(() => { const d = ctx.getImageData(2, 2, 1, 1).data; return [d[0], d[1], d[2]]; });
  exige(canto[0] > 200 && canto[1] < 60, 'a moldura nao pintou o canto do quadro');
  await eu(() => { PROJ.borda = {larg: 0, cor: '#ffffff'}; desenha(0.3); });

  /* ---- 10h. ARRASTAR NA PREVIA move o texto ---- */
  await eu(() => {
    PROJ.textos.length = 0;
    PROJ.textos.push({id: novoId(), txt: 'ALVO', x: 0.5, y: 0.5, tam: 9, cor: '#fff',
      contorno: true, corContorno: '#000', negrito: true, fonte: 'Segoe UI, sans-serif',
      anim: 'nenhuma', animSai: 'nenhuma', t0: 0, t1: 99});
    TEMPO = 0.4; selecionar('textos', 0); desenha(TEMPO);
  });
  const cx0 = await eu(() => { const r = cv.getBoundingClientRect();
    return [r.left + r.width * 0.5, r.top + r.height * 0.5]; });
  await pg.mouse.move(cx0[0], cx0[1]);
  await pg.mouse.down();
  await pg.mouse.move(cx0[0] + 40, cx0[1] - 30, { steps: 6 });
  await pg.mouse.up();
  await pg.waitForTimeout(200);
  exige(await eu(() => PROJ.textos[0].x > 0.53 && PROJ.textos[0].y < 0.47),
    'arrastar o texto na previa nao mexeu nele (x=' +
    (await eu(() => Math.round(PROJ.textos[0].x * 100) / 100)) + ')');

  /* ---- 11. desfazer devolve o projeto ---- */
  const quantos = await eu(() => PROJ.clipes.length);
  await eu(() => { guardaPasso(); PROJ.clipes.length = 0; tudo(); desfazer(); });
  exige(await eu(q => PROJ.clipes.length === q, quantos), 'desfazer nao devolveu os clipes');
  exige(await eu(() => !!PROJ.clipes[0] && !!PROJ.clipes[0].el),
    'desfazer devolveu o clipe SEM o material (o <video> se perdeu na copia)');

  /* ---- 11b. REFAZER devolve o que o desfazer tirou ---- */
  await eu(() => { guardaPasso(); PROJ.textos.length = 0; tudo(); });
  await eu(() => desfazer());
  const voltou = await eu(() => PROJ.textos.length);
  await eu(() => refazer());
  exige(await eu(v => PROJ.textos.length !== v, voltou), 'refazer nao mudou nada');
  await eu(() => desfazer());

  /* ---- 11c. RASCUNHO: guardar e reabrir com os arquivos ---- */
  const guardou = await eu(() => new Promise(ok => {
    salvarRascunho();
    setTimeout(() => ok(!!FEITO.guardou), 2500);
  }));
  exige(guardou, 'o rascunho nao foi guardado no banco do navegador');
  if (guardou) {
    const quantosR = await eu(() => PROJ.clipes.length);
    await eu(() => { PROJ.clipes.length = 0; PROJ.audios.length = 0; PROJ.pip.length = 0;
                     PROJ.textos.length = 0; tudo(); });
    await eu(() => abrirRascunho());
    /* ⚠️ espera FOLGADA de proposito: o rascunho recria um <video> e dois
       <audio> a partir dos arquivos, e metadado de midia demora. Teste com
       prazo curto reprova o programa por impaciencia do teste. */
    await pg.waitForTimeout(6000);
    exige(await eu(q => PROJ.clipes.length === q, quantosR),
      'o rascunho reabriu com numero de clipes diferente (' +
      (await eu(() => PROJ.clipes.length)) + ' de ' + quantosR + '); ficaram de fora: ' +
      (await eu(() => (CAIRAM || []).join(' / ') || 'nada declarado')) +
      ' | diagnostico: ' + (await eu(() => JSON.stringify(DIAG))));
    exige(await eu(() => !!PROJ.clipes[0] && !!PROJ.clipes[0].el &&
      (PROJ.clipes[0].tipo === 'foto' ? PROJ.clipes[0].el.naturalWidth > 0
                                      : PROJ.clipes[0].el.videoWidth > 0)),
      'o rascunho voltou SEM o arquivo por tras (o blob: morreu com a aba)');
  }

  /* ---- 12. nenhum erro de JavaScript no caminho ---- */
  const limpos = erros.filter(e => !/favicon|Download is not|net::ERR_ABORTED/i.test(e));
  if (limpos.length) falhas.push('erro de JavaScript: ' + limpos.slice(0, 3).join(' | '));

  await fim(b, srv);
})().catch(e => {
  console.log('cobaia video: NAO MEDI (' + (e && e.message) + ')');
  process.exit(2);
});

async function fim(b, srv) {
  await b.close(); srv.close();
  console.log(alvo + ' -> cobaia de video: 20 passos de uso real');
  notas.forEach(n => console.log('   . ' + n));
  if (!falhas.length) {
    console.log('   cobaia ok: apara, corta, congela, arrasta, compoe som, EXPORTA e guarda rascunho');
    process.exit(0);
  }
  console.log('  ' + falhas.length + ' DEFEITO(S):');
  falhas.forEach(f => console.log('   - ' + f));
  process.exit(1);
}
