/* ============================================================
   O EFEITO FAZ EFEITO? — o portão que mede PIXEL, não intenção.
   ⚠️ NASCEU DE UMA PERGUNTA DO MARCOS (24/set/2026): ***"os filtros e efeitos
   funcionam?"***. A resposta honesta, naquele instante, era **eu não sabia**:
   a cobaia media a MONTAGEM (trazer, aparar, dividir, exportar) e nunca havia
   olhado se ligar "preto e branco" tirava a cor de verdade.

   ⭐ E ESTA É A ARMADILHA DA FAMÍLIA INTEIRA DOS EFEITOS: eles são a coisa mais
   fácil de parecer que funciona. O botão acende, o controle desliza, o valor
   muda no objeto do projeto — e a tela continua igual, porque alguém esqueceu
   de chamar `desenha()`, porque o nome do campo mudou, ou porque o navegador
   ignora a propriedade calada (`ctx.filter` faz exatamente isso). Print
   nenhum pega, `node --check` nenhum pega.

   Então aqui não se pergunta "o valor mudou?": **compara-se o quadro ANTES e
   DEPOIS, pixel a pixel**, e exige-se a mudança CERTA — preto e branco tem de
   igualar os três canais, brilho tem de subir a luz média, fundo verde tem de
   APAGAR o verde, keyframe tem de MOVER a camada.

   Uso:  node _qa/efeitos_video.js _video69/index.html
   Códigos: 0 passou · 1 REPROVADO · 2 não deu para medir
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  try { chromium = require('playwright').chromium; }
  catch (e2) { console.log('efeitos: NAO MEDI (playwright ausente)'); process.exit(2); }
}
const path = require('path'), fs = require('fs'), http = require('http');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const alvo = process.argv[2] || '_video69/index.html';
const abs = path.resolve(alvo);
if (!fs.existsSync(abs)) { console.log('efeitos: NAO MEDI (nao achei ' + alvo + ')'); process.exit(2); }
const raiz = path.dirname(abs);
const falhas = [], notas = [];

function servidor() {
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      let f = decodeURIComponent(req.url.split('?')[0]);
      if (f === '/') f = '/' + path.basename(abs);
      const c = path.join(raiz, f);
      if (!c.startsWith(raiz) || !fs.existsSync(c)) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(c));
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}

/* ---- as reguas, todas medidas no proprio canvas do editor ----
   ⚠️ a amostragem pula de 4 em 4 pixels: e a MESMA amostra sempre (nada de
   acaso), e 60 mil pontos bastam para qualquer uma destas perguntas. */
const REGUAS = `
window.__medir = function(t){
  desenha(t);
  var d = ctx.getImageData(0,0,cv.width,cv.height).data, i;
  var somaL=0, somaR=0, somaG=0, somaB=0, n=0, difCanais=0, verdes=0, ls=[];
  for(i=0;i<d.length;i+=16){
    var r=d[i], g=d[i+1], b=d[i+2];
    var L=(r*299+g*587+b*114)/1000;
    somaL+=L; somaR+=r; somaG+=g; somaB+=b; n++;
    difCanais += Math.abs(r-g)+Math.abs(g-b)+Math.abs(r-b);
    if(g>110 && g>r*1.5 && g>b*1.5) verdes++;
    ls.push(L);
  }
  var med=somaL/n, v=0;
  for(i=0;i<ls.length;i++) v += (ls[i]-med)*(ls[i]-med);
  return {luz: med, cor: difCanais/n, r: somaR/n, g: somaG/n, b: somaB/n,
          verde: verdes/n, desvio: Math.sqrt(v/ls.length), n: n};
};
window.__assinatura = function(t){
  desenha(t);
  var d = ctx.getImageData(0,0,cv.width,cv.height).data, i, h=0;
  for(i=0;i<d.length;i+=64) h = (h*31 + d[i]*7 + d[i+1]*3 + d[i+2]) % 2147483647;
  return h;
};
/* Onde esta o "peso" da camada de cima, para saber se ela ANDOU.
   ⚠️⚠️ A PRIMEIRA REGUA DESTE PORTAO ESTAVA ERRADA, e vale registrar porque e
   um erro de medicao classico: ela procurava os pixels CLAROS da tela e tirava
   a media. So que o fundo era uma FOTO DE PAISAGEM, com ceu — e o ceu tem mais
   pixels claros que a camada inteira. O centro de massa mal se mexia (0,56 ->
   0,51) e o portao acusou o keyframe de nao funcionar quando quem nao
   funcionava era a regua.
   O conserto e procurar uma marca que SO a camada tem: ela e o clipe de fundo
   VERDE, e verde daquele tom nao existe em mais nada na tela. *Regua que mede
   o fundo junto com o assunto nao mede o assunto.* */
window.__centroVerde = function(t){
  desenha(t);
  var d = ctx.getImageData(0,0,cv.width,cv.height).data, i, sx=0, sy=0, n=0;
  var W=cv.width;
  for(i=0;i<d.length;i+=4){
    var r=d[i], g=d[i+1], b=d[i+2];
    if(g>110 && g>r*1.5 && g>b*1.5){ var p=i/4; sx += p % W; sy += Math.floor(p / W); n++; }
  }
  return n > 50 ? {x: sx/n/W, y: sy/n/cv.height, n: n} : null;
};
`;

(async () => {
  const srv = await servidor();
  const porta = srv.address().port;
  const b = await chromium.launch({
    executablePath: fs.existsSync(CROMO) ? CROMO : undefined,
    args: ['--no-sandbox', '--disable-gpu', '--use-fake-ui-for-media-capture',
           '--use-fake-device-for-media-stream', '--autoplay-policy=no-user-gesture-required']
  });
  const pg = await b.newPage({ viewport: { width: 1366, height: 768 } });
  const erros = [];
  pg.on('pageerror', e => erros.push(String(e.message || e)));

  await pg.goto('http://127.0.0.1:' + porta + '/', { waitUntil: 'load' });
  await pg.waitForTimeout(400);
  await pg.click('#mdOk');
  await pg.addScriptTag({ content: REGUAS });

  const eu = (f, ...a) => pg.evaluate(f, ...a);
  const exige = (c, t) => { if (!c) falhas.push(t); };

  /* ---------- material: uma FOTO colorida do proprio acervo ---------- */
  await pg.click('[data-qa="f-acervo"]');
  await pg.waitForTimeout(180);
  await pg.click('#acFotos [data-v="paisagem"]');
  await pg.waitForTimeout(900);
  if (!(await eu(() => PROJ.clipes.length))) {
    console.log('efeitos: NAO MEDI (a foto do acervo nao entrou)');
    await b.close(); srv.close(); process.exit(2);
  }
  await eu(() => { PROJ.clipes[0].fim = 6; PROJ.clipes[0].fonteDur = 30;
                   PROJ.fundo = 'preto'; selecionar('clipes', 0); tudo(); });

  const temFiltro = await eu(() => TEMFILTRO);
  notas.push('ctx.filter neste navegador: ' + (temFiltro ? 'existe' : 'NAO existe'));

  const base = await eu(() => __medir(1));
  notas.push('quadro base: luz ' + Math.round(base.luz) + ', cor ' + Math.round(base.cor));
  exige(base.cor > 20, 'a foto de teste ja nasceu quase sem cor — a medicao nao valeria');

  /* ---------- 1. PRETO E BRANCO tira a cor ---------- */
  await eu(() => { PROJ.clipes[0].filtro = 'pb'; });
  const pb = await eu(() => __medir(1));
  exige(pb.cor < base.cor * 0.12,
    'filtro PRETO E BRANCO nao tirou a cor (dif de canais ' + Math.round(base.cor) +
    ' -> ' + Math.round(pb.cor) + ')');
  notas.push('preto e branco: cor ' + Math.round(base.cor) + ' -> ' + Math.round(pb.cor));

  /* ---------- 2. os outros tres filtros mudam o quadro, cada um do SEU jeito ---------- */
  const assin = {};
  for (const f of ['nenhum', 'vintage', 'frio', 'quente']) {
    await eu(v => { PROJ.clipes[0].filtro = v; }, f);
    assin[f] = await eu(() => __assinatura(1));
  }
  for (const f of ['vintage', 'frio', 'quente'])
    exige(assin[f] !== assin.nenhum, 'o filtro ' + f.toUpperCase() + ' nao mudou nada no quadro');
  exige(new Set([assin.vintage, assin.frio, assin.quente]).size === 3,
    'dois filtros diferentes produzem o MESMO quadro');
  await eu(() => { PROJ.clipes[0].filtro = 'nenhum'; });

  /* ---------- 3. BRILHO sobe a luz, e 60% dele ABAIXA ---------- */
  await eu(() => { PROJ.clipes[0].brilho = 160; });
  const claro = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].brilho = 60; });
  const escuro = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].brilho = 100; });
  exige(claro.luz > base.luz * 1.15 && escuro.luz < base.luz * 0.85,
    'o BRILHO nao mexeu na luz do quadro (60%: ' + Math.round(escuro.luz) +
    ' · 100%: ' + Math.round(base.luz) + ' · 160%: ' + Math.round(claro.luz) + ')');
  notas.push('brilho 60/100/160: luz ' + [escuro, base, claro].map(x => Math.round(x.luz)).join(' / '));

  /* ---------- 4. CONTRASTE abre o desvio ---------- */
  await eu(() => { PROJ.clipes[0].contraste = 170; });
  const dur = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].contraste = 100; });
  exige(dur.desvio > base.desvio * 1.1,
    'o CONTRASTE nao abriu a diferenca entre claro e escuro (' +
    Math.round(base.desvio) + ' -> ' + Math.round(dur.desvio) + ')');

  /* ---------- 5. SATURACAO em zero e preto e branco ---------- */
  await eu(() => { PROJ.clipes[0].satur = 0; });
  const cinza = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].satur = 100; });
  exige(cinza.cor < base.cor * 0.2, 'SATURACAO em 0 nao tirou a cor');

  /* ---------- 6. TEMPERATURA move o quadro para os lados opostos ---------- */
  await eu(() => { PROJ.clipes[0].calor = 60; });
  const quente = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].calor = -60; });
  const frio = await eu(() => __medir(1));
  await eu(() => { PROJ.clipes[0].calor = 0; });
  exige((quente.r - quente.b) > (frio.r - frio.b),
    'a TEMPERATURA nao esquentou nem esfriou (quente R-B ' +
    Math.round(quente.r - quente.b) + ', frio R-B ' + Math.round(frio.r - frio.b) + ')');
  notas.push('temperatura -60/+60: R-B ' + Math.round(frio.r - frio.b) + ' / ' +
             Math.round(quente.r - quente.b));

  /* ---------- 7. FUNDO VERDE apaga o verde de verdade ---------- */
  await pg.click('[data-qa="f-acervo"]');
  await pg.waitForTimeout(180);
  await pg.click('#acCenas [data-v="verde"]');
  await pg.waitForTimeout(5200);
  /* o clipe verde entrou na faixa principal; movo para a camada de cima */
  const virou = await eu(() => {
    var i = PROJ.clipes.length - 1;
    if (i < 1) return false;
    var c = PROJ.clipes[i];
    PROJ.clipes.splice(i, 1);
    PROJ.pip.push({id: novoId(), tipo: 'video', el: c.el, url: c.url, nome: 'verde', mini: null,
      x: 0.5, y: 0.5, esc: 0.9, op: 1, keys: [], mistura: 'normal', mascara: 'nenhuma',
      chroma: {on: false, cor: '#00c853', tol: 40}, t0: 0, t1: 5});
    tudo(); return true;
  });
  if (!virou) falhas.push('nao consegui pôr o clipe de fundo verde na camada de cima');
  else {
    await pg.waitForTimeout(400);
    const comVerde = await eu(() => __medir(1.2));
    await eu(() => { PROJ.pip[PROJ.pip.length - 1].chroma.on = true; });
    const semVerde = await eu(() => __medir(1.2));
    exige(comVerde.verde > 0.2,
      'o clipe de teste nao tem verde suficiente para medir (' +
      Math.round(comVerde.verde * 100) + '%)');
    exige(semVerde.verde < comVerde.verde * 0.15,
      'o FUNDO VERDE (chroma key) nao apagou o verde (' +
      Math.round(comVerde.verde * 100) + '% -> ' + Math.round(semVerde.verde * 100) + '%)');
    notas.push('chroma key: verde na tela ' + Math.round(comVerde.verde * 100) + '% -> ' +
               Math.round(semVerde.verde * 100) + '%');

    /* ---------- 8. MASCARA e MISTURA mudam o quadro ---------- */
    const semMasc = await eu(() => __assinatura(1.2));
    await eu(() => { PROJ.pip[PROJ.pip.length - 1].mascara = 'circulo'; });
    const comMasc = await eu(() => __assinatura(1.2));
    exige(semMasc !== comMasc, 'a MASCARA de circulo nao mudou nada');
    await eu(() => { PROJ.pip[PROJ.pip.length - 1].mascara = 'nenhuma';
                     PROJ.pip[PROJ.pip.length - 1].mistura = 'tela'; });
    const comMist = await eu(() => __assinatura(1.2));
    exige(semMasc !== comMist, 'a MISTURA (tela) nao mudou nada');
    await eu(() => { PROJ.pip[PROJ.pip.length - 1].mistura = 'normal'; });

    /* ---------- 9. KEYFRAME move a camada ---------- */
    await eu(() => {
      var o = PROJ.pip[PROJ.pip.length - 1];
      o.chroma.on = false; o.esc = 0.3;
      o.keys = [{t: 0.2, x: 0.20, y: 0.25, esc: 0.3, op: 1},
                {t: 4.0, x: 0.80, y: 0.75, esc: 0.3, op: 1}];
      tudo();
    });
    const c0 = await eu(() => __centroVerde(0.3));
    const c1 = await eu(() => __centroVerde(3.8));
    if (!c0 || !c1) falhas.push('nao consegui achar a camada na tela para medir o keyframe');
    else {
      exige((c1.x - c0.x) > 0.12 && (c1.y - c0.y) > 0.12,
        'o KEYFRAME nao moveu a camada (de ' + c0.x.toFixed(2) + ',' + c0.y.toFixed(2) +
        ' para ' + c1.x.toFixed(2) + ',' + c1.y.toFixed(2) + ')');
      notas.push('keyframe: a camada andou de ' + c0.x.toFixed(2) + ',' + c0.y.toFixed(2) +
                 ' ate ' + c1.x.toFixed(2) + ',' + c1.y.toFixed(2));
    }
    await eu(() => { PROJ.pip.length = 0; tudo(); });
  }

  /* ---------- 10. TRANSICAO: no meio dela o quadro nao e nem um nem outro ---------- */
  await pg.click('[data-qa="f-acervo"]');
  await pg.waitForTimeout(180);
  await pg.click('#acFotos [data-v="retrato"]');
  await pg.waitForTimeout(900);
  const dois = await eu(() => PROJ.clipes.length >= 2);
  if (!dois) falhas.push('nao consegui montar dois clipes para medir a transicao');
  else {
    await eu(() => {
      PROJ.clipes[0].fim = 3; PROJ.clipes[0].fonteDur = 30;
      PROJ.clipes[1].fim = 3; PROJ.clipes[1].fonteDur = 30;
      PROJ.clipes[1].transicao = {tipo: 'corte', dur: 1};
      tudo();
    });
    const soA = await eu(() => __assinatura(2.5));
    await eu(() => { PROJ.clipes[1].transicao = {tipo: 'fade', dur: 1}; });
    const meio = await eu(() => __assinatura(2.5));
    exige(soA !== meio, 'a TRANSICAO esmaecer nao mudou o quadro no meio da emenda');
    const tipos = {};
    for (const t of ['fade', 'deslizar', 'zoom', 'falha']) {
      await eu(v => { PROJ.clipes[1].transicao = {tipo: v, dur: 1}; }, t);
      tipos[t] = await eu(() => __assinatura(2.5));
    }
    exige(new Set(Object.values(tipos)).size === 4,
      'duas transicoes diferentes desenham o MESMO quadro');
    notas.push('transicoes: as quatro desenham quadros diferentes no meio da emenda');
    await eu(() => { PROJ.clipes[1].transicao = {tipo: 'corte', dur: 0.5}; });
  }

  /* ---------- 11. ZOOM LENTO (Ken Burns) ---------- */
  await eu(() => { PROJ.clipes[0].zoom = {de: 1, para: 1.6}; });
  const z0 = await eu(() => __assinatura(0.2));
  const z1 = await eu(() => __assinatura(2.6));
  exige(z0 !== z1, 'o ZOOM LENTO nao mudou a imagem do comeco ao fim do pedaco');
  await eu(() => { PROJ.clipes[0].zoom = {de: 1, para: 1}; });

  /* ---------- 12. ANIMACAO DO TEXTO: entrar e sair ---------- */
  await eu(() => {
    PROJ.textos.length = 0;
    PROJ.textos.push({id: novoId(), txt: 'AAAAAAA', x: 0.5, y: 0.5, tam: 16, cor: '#ffffff',
      contorno: false, corContorno: '#000000', negrito: true, fonte: 'Segoe UI, sans-serif',
      anim: 'aparecer', animSai: 'sumir', t0: 1, t1: 3});
    tudo();
  });
  const tEntra = await eu(() => __medir(1.03));
  const tCheio = await eu(() => __medir(2.0));
  const tSai = await eu(() => __medir(2.97));
  exige(tCheio.luz > tEntra.luz && tCheio.luz > tSai.luz,
    'a ANIMACAO do texto nao esmaeceu na entrada nem na saida (luz ' +
    tEntra.luz.toFixed(1) + ' / ' + tCheio.luz.toFixed(1) + ' / ' + tSai.luz.toFixed(1) + ')');
  notas.push('texto aparecendo/cheio/sumindo: luz ' +
    [tEntra, tCheio, tSai].map(x => x.luz.toFixed(1)).join(' / '));

  /* ---------- 13. FUNDO DESFOCADO desenha alguma coisa fora da figura ---------- */
  await eu(() => { PROJ.textos.length = 0; PROJ.clipes.length = 1;
                   PROJ.razao = '16:9'; PROJ.encaixe = 'contem'; PROJ.fundo = 'preto';
                   aplicaRazao(); tudo(); });
  const semFundo = await eu(() => __medir(1));
  await eu(() => { PROJ.fundo = 'desfoque'; });
  const comFundo = await eu(() => __medir(1));
  exige(comFundo.luz > semFundo.luz + 2,
    'o FUNDO DESFOCADO nao pintou nada em volta da figura (luz ' +
    semFundo.luz.toFixed(1) + ' -> ' + comFundo.luz.toFixed(1) + ')');
  notas.push('fundo desfocado: luz ' + semFundo.luz.toFixed(1) + ' -> ' + comFundo.luz.toFixed(1));

  /* ---------- 13b. FUNDO EM DEGRADE ---------- */
  await eu(() => { PROJ.fundo = 'cor'; PROJ.corFundo = '#3050c0'; });
  const solido = await eu(() => __assinatura(1));
  await eu(() => { PROJ.fundo = 'degrade'; });
  const grad = await eu(() => __assinatura(1));
  exige(solido !== grad, 'o fundo em DEGRADE saiu igual ao de cor solida');

  /* ---------- 13c. FULL HD muda a medida de saida ---------- */
  const antesHD = await eu(() => medidaDaSaida().join('x'));
  await eu(() => { PROJ.perfil = 'fullhd'; aplicaRazao(); });
  const depoisHD = await eu(() => medidaDaSaida().join('x'));
  exige(antesHD !== depoisHD && /1920|1080/.test(depoisHD),
    'o perfil FULL HD nao mudou a medida de saida (' + antesHD + ' -> ' + depoisHD + ')');
  notas.push('perfis: ' + antesHD + ' -> ' + depoisHD + ' em Full HD');
  await eu(() => { PROJ.perfil = 'leve'; aplicaRazao(); });

  /* ---------- 14. nenhum erro de JavaScript ---------- */
  const limpos = erros.filter(e => !/favicon|net::ERR_ABORTED/i.test(e));
  if (limpos.length) falhas.push('erro de JavaScript: ' + limpos.slice(0, 3).join(' | '));

  await b.close(); srv.close();
  console.log(alvo + ' -> efeitos: 16 medicoes de pixel');
  notas.forEach(n => console.log('   . ' + n));
  if (!falhas.length) {
    console.log('   efeitos ok: filtro, ajuste, chroma, mascara, mistura, keyframe, ' +
                'transicao, zoom, animacao de texto e fundo desfocado MUDAM o quadro');
    process.exit(0);
  }
  console.log('  ' + falhas.length + ' DEFEITO(S):');
  falhas.forEach(f => console.log('   - ' + f));
  process.exit(1);
})().catch(e => {
  console.log('efeitos: NAO MEDI (' + (e && e.message) + ')');
  process.exit(2);
});
