/* ============================================================
   PORTÃO — "a voz diz o que está ESCRITO?"

   ⚠️ LIÇÃO PAGA (ago/2026), e quem pegou foi o Marcos, não portão nenhum:
   *"os erros que achei nessa atividade foram (...) a questão dos botões não
   falar o que está escrito, e não teve fala automática, visto que os pequinos
   precisam"* — e, quando eu mostrei a medição: *"tem que falar o que está
   escrito"*.

   Medido na Padaria das Letras, ANTES do conserto:
     · 32 fases, **1** narrava sozinha — 31 mudas;
     · 23 alto-falantes, **8** deles em cima de uma letra sozinha (M, B, P, D,
       C, G, Q, O) não tocavam NADA. A criança do 1º ano tocava o alto-falante
       da letra — o gesto exato que a atividade ensina — e ouvia silêncio;
     · 2 fases tinham resposta tocável e nenhum alto-falante.

   Nenhum dos portões existentes via isso. Eles mediam se a voz EXISTE
   (`_qa/falas.py` mede a pronúncia; o montador conta quantas gravar), nunca se
   o que está NA TELA tem a gravação DAQUELE texto. É a mesma família do
   "existir não é medir".

   O que este portão faz, fase por fase, na atividade montada:
     1. lê o BALÃO da fase e confere que há gravação para aquele texto
        (senão o motor fica calado de propósito — é a "fala automática" que
        some);
     2. acha todo ALTO-FALANTE (`.zap`) e confere que a gravação dele é
        exatamente o texto escrito ao lado;
     3. avisa quando a fase tem resposta tocável e nenhum alto-falante — no 1º
        ano, quem ainda soletra escolhe pelo desenho e a atividade vira loteria.

   ⚠️ Ele NÃO mede se o mp3 já foi gravado (isso é do `entregar.yml`): mede se o
   texto da tela ESTÁ NA LISTA de gravação. Um sem o outro não resolve.

   Uso: node _qa/fala_o_escrito.js <pasta-da-atividade>
   ============================================================ */
const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const fs = require('fs');
const path = require('path');

(async () => {
  const pasta = (process.argv[2] || '').replace(/\/$/, '');
  if (!pasta) { console.log('uso: node _qa/fala_o_escrito.js <pasta>'); process.exit(2); }
  const html = path.resolve(pasta, 'index.html');
  const jf = path.resolve(pasta, 'falas.json');
  if (!fs.existsSync(html) || !fs.existsSync(jf)) {
    console.log(pasta + ' -> falta index.html ou falas.json. NAO MEDI NADA.');
    process.exit(2);
  }
  const porId = {};
  JSON.parse(fs.readFileSync(jf, 'utf8')).forEach(f => { porId[f.id] = f.texto; });

  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']});
  const p = await b.newPage({viewport: {width: 1366, height: 640}});
  await p.goto('file://' + html);
  await p.waitForTimeout(900);

  /* Atividade MONTADA anda pelo `FASES`. Atividade ESCRITA A MAO (o Jardim do
     Broto, o Circo do Teo) tem uma funcao por tela — entao as telas sao
     descobertas pelo nome, como o resto da banca ja faz. Sem isto o portao
     dizia "nao achei as FASES" justo nas atividades premium feitas a mao. */
  const montada = await p.evaluate(() => typeof FASES !== 'undefined' && typeof montaFase === 'function');
  const telas = montada ? [] : await p.evaluate(() => {
    const fora = {telaPainel: 1, telaCapa: 1, telaQuem: 1, telaP: 1};
    return Object.keys(window).filter(k => /^tela[A-Z]/.test(k) &&
      typeof window[k] === 'function' && !fora[k]).sort();
  });
  const n = montada ? await p.evaluate(() => FASES.length) : telas.length;
  if (!n) {
    console.log(pasta + ' -> nao achei nem FASES nem telas. NAO MEDI NADA (isso nao e "passou").');
    process.exit(2);
  }
  console.log(pasta + ' -> ' + (montada ? 'atividade montada' : 'atividade escrita a mao') +
              ', ' + n + ' tela(s) a medir');

  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const mudas = [], semVoz = [], semZap = [];
  let zaps = 0, batem = 0;

  for (let i = 0; i < n; i++) {
    const nome = montada ? ('fase ' + (i + 1)) : telas[i];
    try {
      if (montada) {
        await p.evaluate(k => {
          try { perfil = {nome: 'ANA', fig: ID.pre + '_cr1'}; } catch (e) {}
          montaFase(k, function () {});
        }, i);
      } else {
        await p.evaluate(t => {
          try { if (typeof ALUNO !== 'undefined') ALUNO = 'ANA'; } catch (e) {}
          window[t]();
        }, telas[i]);
      }
    } catch (e) { continue; }
    await p.waitForTimeout(330);

    const r = await p.evaluate(() => {
      const cx = (document.getElementsByClassName('pecabox')[0] || document.querySelector('.tela') || document.body);
      const bs = cx ? cx.getElementsByClassName('balao') : null;
      const balao = (bs && bs.length) ? (bs[0].textContent || '') : '';
      const lista = [];
      document.querySelectorAll('.zap, .zapb').forEach(z => {
        const dono = z.parentNode;
        const t = (dono.textContent || '').replace(/\s+/g, ' ').trim();
        lista.push({txt: t, k: (typeof chaveVoz === 'function' ? chaveVoz(t) : null)});
      });
      return {
        balao: balao,
        balaoK: (balao && typeof chaveVoz === 'function') ? chaveVoz(balao.replace(/\s+/g, ' ').trim()) : null,
        zaps: lista,
        resp: document.querySelectorAll('.opt, .oaf, .carta, .escolha').length
      };
    });

    if (r.balao && !porId['op_' + r.balaoK]) {
      mudas.push(nome + ': "' + norm(r.balao).slice(0, 52) + '"');
    }
    zaps += r.zaps.length;
    r.zaps.forEach(z => {
      const grav = porId['op_' + z.k];
      if (grav === undefined) {
        semVoz.push(nome + ': o alto-falante de "' + z.txt.slice(0, 32) + '" nao toca nada');
      } else if (norm(grav) !== norm(z.txt)) {
        semVoz.push(nome + ': escrito "' + z.txt.slice(0, 28) +
                    '" mas gravado "' + norm(grav).slice(0, 28) + '"');
      } else batem++;
    });
    if (!r.zaps.length && r.resp > 1) {
      semZap.push(nome + ': ' + r.resp + ' resposta(s) tocavel(is), 0 alto-falante');
    }
  }
  await b.close();

  console.log('   ' + n + ' tela(s) medida(s) | ' + zaps + ' alto-falante(s)');
  console.log('   balao COM gravacao (a fala automatica): ' + (n - mudas.length) + ' de ' + n);
  console.log('   alto-falante que diz o que esta escrito: ' + batem + ' de ' + zaps);

  const erros = mudas.length + semVoz.length;
  if (mudas.length) {
    console.log('   ' + mudas.length + ' FASE(S) MUDA(S) — o motor le o balao e nao acha gravacao:');
    mudas.slice(0, 8).forEach(m => console.log('    - ' + m));
  }
  if (semVoz.length) {
    console.log('   ' + semVoz.length + ' ALTO-FALANTE(S) QUE NAO DIZEM O ESCRITO:');
    semVoz.slice(0, 8).forEach(m => console.log('    - ' + m));
  }
  if (semZap.length) {
    console.log('   aviso: ' + semZap.length + ' fase(s) com resposta tocavel e sem alto-falante:');
    semZap.slice(0, 6).forEach(m => console.log('    . ' + m));
  }
  if (!erros) console.log('   voz ok: toda tela narra e todo alto-falante diz o que esta escrito');
  process.exit(erros ? 1 : 0);
})();
