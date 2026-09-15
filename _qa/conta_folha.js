/* ============================================================
   PORTÃO — O POTE E OS ITENS DA FOLHA BATEM?   (1y)   [folha viva]

   ⭐ O DEFEITO QUE ELE PAGA (15/set/2026, A Fábrica de Nomes).
      Na folha viva o número de itens de uma folha NÃO está escrito em lugar
      nenhum: ele é o tamanho do POTE daquela posição (`ST.folha["p20"]`), e o
      `idsDaPagina()` o lê de lá para saber quantos itens faltam. A folha se dá
      por pronta quando `pendentes()` chega a zero.

      Na folha 20 o pote trazia as CINCO famílias de palavras, mas a folha
      desenhava CATORZE palavras no mural e registrava catorze ids. Resultado,
      medido no navegador: pintadas cinco palavras quaisquer, a folha se
      carimbava PRONTA, o carimbo caía na tela e o caderno pulava para a
      seguinte — com nove palavras ainda por pintar à vista da criança. E o
      relatório do professor contava cinco de catorze, dizendo que ela acertou
      tudo. O mesmo estava na folha 21 (oito itens, quatro posições) e na 24
      (cinco perguntas, uma posição).

   ⚠️ E NENHUM PORTÃO VIA, nem podia:
      · o `node --check` passa — a sintaxe está perfeita;
      · o ANDARILHO (`andar_folha.js`) conta os itens DESENHADOS e acha 14;
      · o JOGADOR (`joga_folha.js`) resolve os itens DECLARADOS e acha 5, fecha
        os cinco, vê a folha carimbar e diz "ok folha 20: 5 de 5";
      · o relatório abre, o fecho abre, não há erro no console.
      Os dois estavam certos cada um no seu canto. O defeito só aparece quando
      se CRUZAM os dois números — que é o que este portão faz, e é a única coisa
      que ele faz.

   O QUE ELE MEDE: para cada folha, `idsDaPagina(pi).length` (o que o caderno
   ACHA que tem) contra o número de ids que a folha REGISTROU de verdade em
   `RESP`. Diferentes = reprovado, e diz para que lado.

   ⚠️ O QUE ELE NÃO MEDE: se o número está CERTO do ponto de vista pedagógico —
      só se as duas contas são a mesma. Uma folha com três itens de menos, mas
      coerente, passa aqui e é o olho que vê.

   Uso:  node _qa/conta_folha.js <pasta> [porta]
   Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
   ============================================================ */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs');

const pasta = (process.argv[2] || '').replace(/\/$/, '');
const porta = process.argv[3] || '8231';
if (!pasta) { console.log('uso: node _qa/conta_folha.js <pasta> [porta]'); process.exit(2); }
if (!fs.existsSync(pasta + '/folhas.js')) {
  console.log(`${pasta} -> NAO SE APLICA: nao achei ${pasta}/folhas.js (nao e caderno de folha viva).`);
  process.exit(2);
}

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', porta], { cwd: pasta, stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 900));
  let b;
  try {
    b = await chromium.launch({
      executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
      args: ['--no-sandbox'] });
  } catch (e) {
    console.log('NAO MEDI: nao consegui abrir o navegador — ' + String(e).slice(0, 120));
    srv.kill(); process.exit(2);
  }
  const pg = await b.newPage({ viewport: { width: 412, height: 915 } });
  const erros = [];
  pg.on('pageerror', e => erros.push(String(e).slice(0, 120)));
  try {
    await pg.goto('http://localhost:' + porta + '/index.html');
    await pg.waitForTimeout(1200);
    /* ⚠️ É PRECISO ABRIR CADA FOLHA: algumas peças só registram os ids quando a
       página é montada, e uma folha nunca aberta registraria zero — o portão
       acusaria inocente. Por isso o `vaiPara(pi)` antes de contar. */
    const r = await pg.evaluate(() => {
      if (typeof PAGEL === 'undefined' || !PAGEL.length) return null;
      const out = [];
      for (let pi = 1; pi < PAGEL.length; pi++) {
        vaiPara(pi);
        const declarados = idsDaPagina(pi).length;
        const registrados = Object.keys(RESP || {})
          .filter(k => (RESP[k] || {}).pag === pi).length;
        out.push({ pi, nome: (typeof NOMES !== 'undefined' ? NOMES[pi - 1] : ''),
                   declarados, registrados });
      }
      return out;
    });
    await b.close(); srv.kill();
    if (!r) { console.log('NAO MEDI: o caderno nao montou as paginas.'); process.exit(2); }
    if (erros.length) {
      console.log(`${pasta} -> NAO MEDI: houve erro de JS ao abrir as folhas:`);
      [...new Set(erros)].slice(0, 3).forEach(e => console.log('    - ' + e));
      process.exit(2);
    }
    console.log(`${pasta} -> conta das folhas: ${r.length} folha(s) conferida(s)`);
    const ruins = r.filter(x => x.declarados !== x.registrados);
    if (!ruins.length) {
      console.log('   ok: em toda folha o pote e os itens registrados sao o mesmo numero.');
      process.exit(0);
    }
    console.log(`   REPROVADO — ${ruins.length} folha(s) fecham na conta errada:`);
    for (const x of ruins) {
      const cedo = x.declarados < x.registrados;
      console.log(`    x folha ${x.pi} (${x.nome}): o pote diz ${x.declarados}, `
                  + `a folha registra ${x.registrados}`);
      console.log('      ' + (cedo
        ? `a folha se da por PRONTA com ${x.declarados} respondidos e pula com `
          + `${x.registrados - x.declarados} item(ns) ainda na tela; o relatorio `
          + 'conta so os primeiros'
        : `a folha NUNCA fecha: faltam sempre ${x.declarados - x.registrados} `
          + 'item(ns) que nao existem na tela'));
    }
    console.log('   conserto: o POTE e que diz quantos itens a folha tem, entao cada');
    console.log('   item precisa de uma posicao nele. Se a folha desenha uma peca por');
    console.log('   palavra, o pote lista as palavras — nao as familias delas.');
    process.exit(1);
  } catch (e) {
    console.log('NAO MEDI: ' + String(e).slice(0, 180));
    try { await b.close(); } catch (_) {}
    srv.kill(); process.exit(2);
  }
})();
