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

/* ⚠️ MODO CELULAR (`--celular`): o professor de Ciencias vai dar a aula com os
   estudantes filmando NO TELEFONE deles, e passar a midia para o PC e o
   gargalo. A saida honesta e editar no proprio telefone — mas "e responsivo"
   nao e prova. Aqui a cobaia inteira roda numa tela de 390x780 com TOQUE (sem
   mouse), e so passa se der para trazer arquivo, aparar, dividir, arrastar na
   previa e EXPORTAR com o dedo. */
const CELULAR = process.argv.indexOf('--celular') >= 0;
const alvo = process.argv.filter(a => a !== '--celular')[2] || '_video69/index.html';
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
  const pg = await b.newPage(CELULAR
    ? { viewport: { width: 390, height: 780 }, hasTouch: true, isMobile: true,
        deviceScaleFactor: 2,
        userAgent: 'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 ' +
                   '(KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36' }
    : { viewport: { width: 1366, height: 768 } });

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
      /* ⚠️ o arquivo FICA: o passo 21 abre ele de volta num <video>, e e esse
         passo que prova que o embrulho MP4 escrito a mao esta certo. */
      baixado = { nome: d.suggestedFilename(), bytes: fs.statSync(p).size, caminho: p };
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

  /* ---- 1b. MEDIR A MAQUINA sem material nenhum ----
     ⚠️ o Marcos apontou que, para saber se o PC aguenta, era preciso montar um
     projeto antes. Este passo prova que nao e mais: com a fita VAZIA, o botao
     do canto da previa mede e devolve um numero. */
  /* ---- 1a2. A PROVA CEGA DA ABERTURA escolheu o tamanho pela MEDIDA ----
     ⚠️ a sala desmentiu a ficha: os PCs da escola bateram 60 fps e eu os
     mandava para 360x640 por causa do processador de 2012. Este passo prova
     que a escolha agora vem do que foi medido, e que ela fica guardada. */
  await pg.waitForTimeout(2200);
  const escolhido = await eu(() => PROJ.perfil);
  const lembrado = await eu(() => { try { return localStorage.getItem('oficina-fps'); }
                                    catch (e) { return null; } });
  exige(!!lembrado, 'a prova da abertura nao guardou a medida nesta maquina');
  notas.push('prova da abertura: escolheu o perfil "' + escolhido + '" (guardou ' +
             lembrado + ')');
  exige(escolhido !== 'leve',
    'neste computador rapido a prova ainda escolheu o perfil mais baixo');

  await eu(() => { PROJ.perfil = 'leve'; aplicaRazao(); });   /* mede sempre do mesmo degrau */
  await pg.click('[data-qa="medir"]');
  await pg.waitForTimeout(3400);
  const medidaVazia = await eu(() => document.getElementById('medidorFps').textContent);
  exige(/\d+ fps/.test(medidaVazia),
    'medir a maquina com a fita vazia nao devolveu numero (' + medidaVazia + ')');
  notas.push('prova da maquina com a fita vazia: ' + medidaVazia);
  /* ⚠️ maquina folgada tem de OUVIR que pode subir: 60 fps quase sempre e o
     teto da tela, nao a forca do computador. Sem este aviso, quem tem PC bom
     fica no tamanho pequeno por falta de saber. */
  const folga = await eu(() => fpsMost >= 50);
  if (folga) {
    const ofereceu = await eu(() =>
      /sobrou m[aá]quina/i.test(document.getElementById('cxmodal').innerHTML));
    exige(ofereceu, 'com ' + (await eu(() => fpsMost)) +
      ' fps o programa NAO ofereceu subir o tamanho');
    notas.push('maquina folgada: o programa ofereceu subir o tamanho');
  }
  if (await eu(() => document.getElementById('veu').classList.contains('on')))
    await pg.click('#mdOk');
  await pg.waitForTimeout(150);

  /* ---- 1c. O EDITOR NAO ABRE VAZIO, e o play toca no primeiro toque ----
     ⚠️ o Marcos teve de dizer TRES vezes que o play pedia arquivo. Este passo
     existe para isso nunca mais voltar calado: ao abrir ja ha material, e um
     clique em tocar faz o tempo ANDAR. */
  exige(await eu(() => PROJ.clipes.length >= 1),
    'o editor abriu com a fita VAZIA — o play vai pedir arquivo de novo');
  /* ⚠️ e a foto de partida NAO pode marcar missao nenhuma: senao o relatorio
     diz que a crianca trouxe material sem ela ter encostado em nada. */
  exige(await eu(() => { confereMissoes();
    return document.querySelectorAll('#listaM .missao.feita').length === 0; }),
    'a foto de partida marcou missao sozinha (' +
    (await eu(() => document.querySelectorAll('#listaM .missao.feita').length)) + ' marcada(s))');
  await eu(() => { fechaGaveta(); TEMPO = 0; });
  await pg.click('[data-qa="tocar"]');
  await pg.waitForTimeout(1200);
  exige(await eu(() => TOCANDO && TEMPO > 0.3),
    'o play nao tocou no primeiro clique (TOCANDO=' +
    (await eu(() => String(TOCANDO))) + ', tempo=' +
    (await eu(() => Math.round(TEMPO * 10) / 10)) + ')');
  await eu(() => pausar());

  /* e se a pessoa apagar tudo, tocar repoe material em vez de reclamar */
  await eu(() => { PROJ.clipes.length = 0; PROJ.audios.length = 0; tudo(); });
  await pg.click('[data-qa="tocar"]');
  await pg.waitForTimeout(1200);
  exige(await eu(() => PROJ.clipes.length >= 1),
    'com a fita vazia, tocar so reclamou em vez de pôr material');
  await eu(() => { pausar(); PROJ.clipes.length = 0; PROJ.textos.length = 0;
                   PROJ.audios.length = 0; PROJ.pip.length = 0; tudo(); });

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

  /* ---- 9b. o caminho RAPIDO existe neste navegador? ---- */
  const rapido = await eu(() => podeRapido());
  notas.push(rapido ? 'caminho rapido (WebCodecs) disponivel: sim'
                    : 'caminho rapido indisponivel — sera medido o caminho antigo');

  /* ---- 10. EXPORTAR — a prova de fogo ---- */
  await eu(() => {
    /* encurta o projeto para o teste nao levar minutos: a exportacao e em
       tempo real, entao um projeto de 2 s leva 2 s. */
    PROJ.clipes.length = 1;
    PROJ.clipes[0].ini = 0; PROJ.clipes[0].fim = Math.min(2, PROJ.clipes[0].fonteDur);
    PROJ.clipes[0].vel = 1;
    PROJ.textos.length = 0; tudo();
  });
  const relogio0 = Date.now();
  await pg.click('[data-qa="exportar"]');
  for (let i = 0; i < 40 && !baixado; i++) await pg.waitForTimeout(500);
  const gastou = (Date.now() - relogio0) / 1000;
  notas.push('exportacao de 2 s de video levou ' + gastou.toFixed(1) + ' s');
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
  /* ⚠️ no celular a pagina e uma coluna so, e a essa altura da corrida ela ja
     rolou: o palco pode estar ACIMA da janela. O toque iria para coordenada
     negativa e cairia no vazio — o teste acusaria o programa por um descuido
     dele proprio. Subir a pagina faz parte do gesto. */
  await eu(() => window.scrollTo(0, 0));
  await pg.waitForTimeout(200);
  const cx0 = await eu(() => { const r = cv.getBoundingClientRect();
    return [r.left + r.width * 0.5, r.top + r.height * 0.5]; });
  if (CELULAR) {
    /* ⚠️ com o dedo os eventos sao `pointer*` do tipo touch — e por isso que o
       editor foi escrito com pointerdown/move/up e setPointerCapture, e nao
       com mousedown. Este passo e o que prova que a escolha valeu. */
    const cdp = await pg.context().newCDPSession(pg);
    const toque = (tipo, x, y) => cdp.send('Input.dispatchTouchEvent', {
      type: tipo,
      /* ⚠️ o `id` NAO e opcional: sem ele o navegador trata cada evento como um
         DEDO NOVO e nunca gera o `pointermove` — o teste acusaria o programa
         por um defeito do proprio teste. */
      touchPoints: tipo === 'touchEnd' ? []
        : [{ x: Math.round(x), y: Math.round(y), id: 1, radiusX: 8, radiusY: 8, force: 1 }]
    });
    /* ⚠️ COM UM INTERVALO ENTRE OS TOQUES. Disparar os tres no mesmo instante
       reprovava o programa — e o programa estava certo: medido a parte, o texto
       andava de 0,50 para 0,80. Dedo nenhum se move em zero milissegundo, e
       entrada sintetica sem tempo entre os passos nao e dedo: e um piscar que o
       navegador junta num evento so. *Teste que nao respeita o tempo do gesto
       mede o teste, nao o programa.* */
    await toque('touchStart', cx0[0], cx0[1]);
    await pg.waitForTimeout(60);
    await toque('touchMove', cx0[0] + 20, cx0[1] - 15);
    await pg.waitForTimeout(60);
    await toque('touchMove', cx0[0] + 44, cx0[1] - 32);
    await pg.waitForTimeout(60);
    await toque('touchEnd', cx0[0] + 44, cx0[1] - 32);
  } else {
    await pg.mouse.move(cx0[0], cx0[1]);
    await pg.mouse.down();
    await pg.mouse.move(cx0[0] + 40, cx0[1] - 30, { steps: 6 });
    await pg.mouse.up();
  }
  await pg.waitForTimeout(200);
  exige(await eu(() => PROJ.textos[0].x > 0.53 && PROJ.textos[0].y < 0.47),
    'arrastar o texto na previa nao mexeu nele (x=' +
    (await eu(() => Math.round(PROJ.textos[0].x * 100) / 100)) + ')');

  /* ---- 10a. O ARQUIVO EXPORTADO ABRE DE VOLTA? ----
     ⚠️ ESTE e o passo que justifica ter escrito o embrulho MP4 a mao em vez de
     pegar uma biblioteca: um arquivo com o indice errado SAI do mesmo jeito,
     com o mesmo tamanho, e so nao toca. Aqui ele volta para dentro de um
     <video> e tem de declarar duracao e largura. */
  if (baixado && baixado.caminho && fs.existsSync(baixado.caminho)) {
    const b64 = fs.readFileSync(baixado.caminho).toString('base64');
    const tipo = /mp4$/.test(baixado.nome) ? 'video/mp4' : 'video/webm';
    const volta = await pg.evaluate(([b64, tipo]) => new Promise(ok => {
      const bin = atob(b64), n = bin.length, a = new Uint8Array(n);
      for (let i = 0; i < n; i++) a[i] = bin.charCodeAt(i);
      const v = document.createElement('video');
      v.preload = 'auto';
      const guarda = setTimeout(() => ok({erro: 'nao carregou em 10 s'}), 10000);
      v.onloadedmetadata = () => { clearTimeout(guarda);
        ok({dur: v.duration, w: v.videoWidth, h: v.videoHeight}); };
      v.onerror = () => { clearTimeout(guarda);
        ok({erro: 'codigo ' + (v.error && v.error.code)}); };
      v.src = URL.createObjectURL(new Blob([a], {type: tipo}));
    }), [b64, tipo]);
    if (volta.erro) falhas.push('o arquivo exportado NAO abre de volta: ' + volta.erro);
    else {
      notas.push('o arquivo reabre: ' + volta.w + 'x' + volta.h + ', ' +
                 (Math.round(volta.dur * 10) / 10) + ' s');
      exige(volta.w > 0 && volta.h > 0, 'o arquivo exportado abriu sem imagem (0x0)');
      exige(volta.dur > 1 && volta.dur < 6,
        'a duracao do arquivo exportado esta errada (' + volta.dur + ' s para 2 s de projeto)');
    }
    try { fs.unlinkSync(baixado.caminho); } catch (e) {}
  }

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

  /* ---- 11d. O BUSCADOR DE MATERIAL LIVRE ----
     ⚠️ O QUE ESTE PASSO MEDE E O QUE ELE NAO MEDE. Ele NAO prova que a rede da
     escola deixa alcancar o Commons — isso so o PC do laboratorio responde.
     Ele prova o que esta do lado de ca: que a resposta e lida certo (nome,
     autor e licenca, com o HTML do campo de autor virando TEXTO), que o
     arquivo entra na fita, que o credito e guardado e escrito, e que a
     FALHA DE REDE mostra o aviso certo em vez de deixar a crianca esperando.
     Para isso o `fetch` e trocado por um de mentira — de mentira e de
     proposito: e a unica forma de medir a leitura sem depender de rede. */
  await eu(() => {
    window.__fetchReal = window.fetch;
    window.__pngFalso = null;
    const c = document.createElement('canvas'); c.width = 40; c.height = 40;
    const x = c.getContext('2d'); x.fillStyle = '#2e7d32'; x.fillRect(0, 0, 40, 40);
    return new Promise(ok => c.toBlob(b => { window.__pngFalso = b; ok(true); }, 'image/png'));
  });
  await eu(() => {
    window.fetch = function (u) {
      if (String(u).indexOf('commons.wikimedia.org') >= 0) {
        return Promise.resolve({ ok: true, json: function () { return Promise.resolve({
          query: { pages: { '1': { title: 'File:Folha verde.jpg', imageinfo: [{
            /* ⚠️ miniatura em `data:` — um endereco inventado (`blob:falso`)
               o navegador recusa carregar, e o console cuspia um erro que era
               do TESTE, nao do programa. */
            thumburl: 'data:image/gif;base64,R0lGODlhAQABAIAAAC4uLgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==',
            url: 'data:image/gif;base64,R0lGODlhAQABAIAAAC4uLgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==',
            descriptionurl: 'https://commons.wikimedia.org/wiki/File:Folha_verde.jpg',
            extmetadata: {
              Artist: { value: '<a href="/wiki/User:Fulano">Fulano <i>de Tal</i></a>' },
              LicenseShortName: { value: 'CC BY-SA 4.0' } } }] } } } }); } });
      }
      return Promise.resolve({ ok: true, blob: function () {
        return Promise.resolve(window.__pngFalso); } });
    };
  });
  await pg.click('[data-qa="f-buscar"]');
  await pg.waitForTimeout(250);

  /* ⚠️⚠️ A TRAVA E O QUE MAIS IMPORTA AQUI. O professor disse: "meu medo e
     digitarem algo improprio no campo busca". O Commons e arquivo publico e tem
     material adulto. Entao o aluno NAO PODE ter campo de texto: se um dia
     alguem mexer nisso sem perceber, este passo reprova. */
  exige((await pg.locator('#qBusca').count()) === 0,
    'o ALUNO tem campo de busca livre — era para ser so os assuntos prontos');
  exige((await pg.locator('#assuntos [data-t]').count()) > 10,
    'os assuntos prontos nao apareceram');
  notas.push('busca: aluno sem campo livre, ' +
    (await pg.locator('#assuntos [data-t]').count()) + ' assuntos prontos');

  /* palavra barrada nao chega a sair pedido nenhum */
  await eu(() => { window.__pediu = 0;
    const f = window.fetch;
    window.fetch = function (u) { window.__pediu++; return f.apply(this, arguments); }; });
  await eu(() => buscarCommons('foto de sexo', 'imagem'));
  await pg.waitForTimeout(300);
  exige(await eu(() => window.__pediu === 0),
    'uma palavra barrada AINDA saiu para a internet');
  exige(await eu(() => /nao e para a aula|não é para a aula/i.test($('resBusca').innerHTML)),
    'a palavra barrada nao mostrou o aviso');
  notas.push('busca: palavra impropria e barrada ANTES de sair o pedido');

  /* a chave do professor destranca o campo */
  pg.once('dialog', d => d.accept('1275@'));
  await pg.click('[data-qa="destrancar"]');
  await pg.waitForTimeout(400);
  exige((await pg.locator('#qBusca').count()) === 1,
    'a chave do professor nao destrancou o campo de busca');
  notas.push('busca: a chave 1275@ destranca o campo para o professor');

  /* e ai, com o campo do professor, a busca de verdade */
  await pg.fill('#qBusca', 'folha');
  await pg.click('[data-qa="buscar"]');
  await pg.waitForTimeout(700);
  const leu = await eu(() => achados.length ? {
    nome: achados[0].nome, autor: achados[0].autor, lic: achados[0].licenca } : null);
  exige(!!leu, 'a busca nao leu nenhum resultado da resposta');
  if (leu) {
    exige(leu.autor === 'Fulano de Tal',
      'o autor nao foi limpo do HTML (veio "' + leu.autor + '")');
    exige(leu.lic === 'CC BY-SA 4.0', 'a licenca nao foi lida');
    exige(leu.nome === 'Folha verde.jpg', 'o nome do arquivo nao foi lido');
    notas.push('busca: leu "' + leu.nome + '" de ' + leu.autor + ' (' + leu.lic + ')');
  }
  const antesB = await eu(() => PROJ.clipes.length);
  await pg.click('#grAchados [data-i="0"]');
  await pg.waitForTimeout(1600);
  exige(await eu(a2 => PROJ.clipes.length === a2 + 1, antesB),
    'o material escolhido na busca nao entrou na fita');
  exige(await eu(() => (PROJ.creditos || []).length === 1), 'o credito nao foi guardado');
  exige(await eu(() => { try { ctx.getImageData(0, 0, 1, 1); return true; }
                         catch (e) { return false; } }),
    'o palco ficou CONTAMINADO depois da busca — a exportacao quebraria');
  await eu(() => { PROJ.textos.length = 0; poeCreditos(); });
  exige(await eu(() => PROJ.textos.length === 1 &&
    /Fulano de Tal/.test(PROJ.textos[0].txt) && /CC BY-SA/.test(PROJ.textos[0].txt)),
    'os creditos nao foram escritos no video');
  notas.push('busca: o credito entrou no video sozinho');

  /* e a rede caindo tem de AVISAR, nao deixar esperando */
  await eu(() => { window.fetch = function () { return Promise.reject(new Error('rede')); }; });
  await pg.fill('#qBusca', 'outra coisa');
  await pg.click('[data-qa="buscar"]');
  await pg.waitForTimeout(700);
  exige(await eu(() => /bloqueia|n[aã]o consegui alcan/i.test($('resBusca').innerHTML)),
    'com a rede fora, a busca nao avisou nada');
  notas.push('busca: com a rede fora, avisa e manda usar o Acervo');
  await eu(() => { window.fetch = window.__fetchReal;
                   PROJ.textos.length = 0; PROJ.creditos = []; tudo(); });

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
  console.log(alvo + ' -> cobaia de video: 26 passos de uso real' +
              (CELULAR ? ' NO CELULAR (390x780, com o dedo)' : ''));
  notas.forEach(n => console.log('   . ' + n));
  if (!falhas.length) {
    console.log('   cobaia ok: apara, corta, congela, arrasta, compoe som, EXPORTA e guarda rascunho');
    process.exit(0);
  }
  console.log('  ' + falhas.length + ' DEFEITO(S):');
  falhas.forEach(f => console.log('   - ' + f));
  process.exit(1);
}
