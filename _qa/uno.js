/* ============================================================
   PORTAO DO UNO — "a crianca nao fica comprando um monte de cartas"

   Ordem do Marcos (set/2026): *"se a crianca nao tiver uma carta para jogar ela
   deve comprar uma no monte; caso ela compre e ainda assim nao tenha, passa a
   vez de jogar, para nao ficar comprando um monte de cartas"*.

   Por que um portao e nao so o conserto: o defeito nao aparece em print nem em
   `node --check`. Ele e uma REGRA de jogo, e regra de jogo so se ve JOGANDO —
   e so se ve com a mao montada de proposito, porque numa partida normal a
   situacao "ela tem carta boa e mesmo assim aperta Pegar 1" pode nao acontecer
   nunca. O portao monta as duas maos na mao e mede.

   AS DUAS MEDIDAS
     1. COM carta jogavel na mao, apertar "Pegar 1" cinco vezes NAO pode
        aumentar a mao. (Era aqui que dava para chegar ao fim da partida com
        quinze cartas sem nunca jogar.)
     2. SEM carta jogavel, apertar "Pegar 1" compra UMA carta; se a comprada
        tambem nao servir, a vez PASSA (`vezDoJogador` vira false).

   Uso:  node _qa/uno.js _uno1/index.html [_uno345/index.html ...]
   Codigos: 0 passou · 1 REPROVOU · 2 NAO MEDI.
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + ').');
  process.exit(2);
}
const fs = require('fs'), path = require('path');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const alvos = process.argv.slice(2);
if (!alvos.length) { console.log('uso: node _qa/uno.js <arquivo.html> [...]'); process.exit(2); }

(async () => {
  let falhas = 0, medidos = 0;
  const navegador = await chromium.launch({ executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu'] });

  for (const alvo of alvos) {
    if (!fs.existsSync(alvo)) { console.log('NAO MEDI: nao achei ' + alvo); await navegador.close(); process.exit(2); }
    const pg = await navegador.newPage({ viewport: { width: 430, height: 900 } });
    const erros = [];
    pg.on('pageerror', e => erros.push('ERRO JS: ' + e.message));
    await pg.goto('file://' + path.resolve(alvo), { waitUntil: 'load' });
    await pg.waitForTimeout(900);

    /* cala a voz e fecha o tutorial, se houver */
    await pg.evaluate(() => {
      try { window.speechSynthesis.cancel(); } catch (e) {}
      try { if (typeof vozLigada !== 'undefined') vozLigada = false; } catch (e) {}
      try { if (typeof fecharTutorial === 'function') fecharTutorial(); } catch (e) {}
    });
    await pg.waitForTimeout(400);

    const temEstado = await pg.evaluate(() => typeof mao !== 'undefined' && typeof comprarCarta === 'function');
    if (!temEstado) {
      console.log('NAO MEDI: ' + alvo + ' nao expoe `mao`/`comprarCarta` (nao e um jogo de UNO?)');
      await pg.close(); continue;
    }
    medidos++;

    /* --- medida 1: com carta jogavel, "Pegar 1" nao compra --------------- */
    const m1 = await pg.evaluate(() => {
      /* monta a mao a mao: uma carta que combina com a mesa, e mais nada */
      mesa = { cor: 'azul', tipo: 'num', valor: 5 };
      corAtiva = 'azul';
      mao = [{ cor: 'azul', tipo: 'num', valor: 7 }];
      try { if (typeof regraAtiva !== 'undefined') regraAtiva = null; } catch (e) {}
      try { if (typeof pintaRegra === 'function') pintaRegra(); } catch (e) {}
      vezDoJogador = true;
      if (typeof esperandoCor !== 'undefined') esperandoCor = false;
      if (typeof render === 'function') render();
      const antes = mao.length;
      for (let k = 0; k < 5; k++) comprarCarta();
      return { antes: antes, depois: mao.length, vez: !!vezDoJogador };
    });

    /* --- medida 2: sem carta jogavel, compra UMA e a vez passa ----------- */
    const m2 = await pg.evaluate(() => {
      mesa = { cor: 'azul', tipo: 'num', valor: 5 };
      corAtiva = 'azul';
      /* uma carta que nao combina em cor nem em valor, e nao e coringa */
      mao = [{ cor: 'vermelho', tipo: 'num', valor: 9 }];
      /* no _uno345 a regra da rodada pode barrar cartas; aqui a medida e sobre a
         COMPRA, entao a rodada fica sem regra */
      try { if (typeof regraAtiva !== 'undefined') regraAtiva = null; } catch (e) {}
      try { if (typeof pintaRegra === 'function') pintaRegra(); } catch (e) {}
      /* o monte so com cartas que tambem nao servem: a compra tem que passar a vez */
      baralho = [];
      for (let k = 0; k < 12; k++) baralho.push({ cor: 'verde', tipo: 'num', valor: 1 });
      vezDoJogador = true;
      if (typeof esperandoCor !== 'undefined') esperandoCor = false;
      if (typeof render === 'function') render();
      const antes = mao.length;
      comprarCarta();
      return { antes: antes, depois: mao.length, vez: !!vezDoJogador };
    });

    const problemas = [];
    if (m1.depois !== m1.antes)
      problemas.push('com carta JOGAVEL na mao, cinco toques em "Pegar 1" compraram ' +
        (m1.depois - m1.antes) + ' carta(s) — a mao foi de ' + m1.antes + ' para ' + m1.depois +
        '. So se compra quando NAO da para jogar.');
    if (m2.depois !== m2.antes + 1)
      problemas.push('sem carta jogavel, um toque em "Pegar 1" comprou ' +
        (m2.depois - m2.antes) + ' carta(s); tem que comprar exatamente UMA.');
    if (m2.vez)
      problemas.push('a carta comprada tambem nao servia e a vez NAO passou — ' +
        'e assim que a mao vira um monte de cartas.');
    for (const e of erros) problemas.push(e);

    if (problemas.length) {
      falhas++;
      console.log(alvo + ' -> REPROVOU');
      problemas.forEach(p => console.log('   · ' + p));
    } else {
      console.log(alvo + ' -> ok: so compra quando nao da para jogar; compra UMA; e passa a vez');
    }
    await pg.close();
  }

  await navegador.close();
  if (!medidos) { console.log('NAO MEDI: nenhum jogo de UNO reconhecido'); process.exit(2); }
  if (falhas) { console.log('REPROVADO: ' + falhas + ' jogo(s) de UNO com a regra da compra errada'); process.exit(1); }
  console.log('passou (' + medidos + ' jogo(s) de UNO medidos)');
  process.exit(0);
})();
