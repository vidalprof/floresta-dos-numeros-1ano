/* ============================================================
   O PC RUIM — "e se o enfeite falhar, a criança ainda passa de fase?"

   NASCEU COM A TURMA DO 1º ANO JOGANDO (set/2026). Palavras do Marcos:
   *"nas fases de ligar em alguns pcs está travando, nao passa, o botão de
   proximo que não aparece"* e, logo depois, a frase que mostrou o tamanho real
   do problema: *"sinto nas atividades que as vezes esse botão demora muito a
   aparecer ou não aparece"* — nas atividades, no PLURAL. Não era a peça de
   ligar: era o motor.

   A CAUSA: o fim de fase rodava assim, tudo numa linha e sem guarda nenhuma —
     bmsg.innerHTML=msg; banner.className=...; festa(); sCerto();
     paraDeVigiar(); mascoteFesteja();
   ...com a AÇÃO do botão atribuída só DEPOIS. E na ponte de cada peça o
   `festa()` vinha ANTES de chamar o banner. Basta um enfeite tropeçar — confete
   sem canvas, som num PC com áudio bloqueado, mascote cuja pose não carregou —
   e a exceção mata a função ali: a criança fica com a fase resolvida, sem botão,
   presa no meio da aula. Em máquina boa nunca acontece; é por isso que passou.

   POR QUE NENHUM PORTÃO PEGAVA: todos rodam num Chromium saudável, onde os
   enfeites nunca falham. O defeito só existe quando algo dá errado — e ninguém
   testava isso.

   O QUE ESTE PORTÃO FAZ: quebra os enfeites DE PROPÓSITO (festa, sCerto,
   mascoteFesteja, paraDeVigiar, confete, arma) e então joga o fim de fase. Exige
   que, mesmo com tudo isso falhando:
     1. o banner APAREÇA;
     2. o botão de próximo exista e esteja VISÍVEL;
     3. clicar nele FAÇA a fase andar.

   A regra da casa que ele defende: **enfeite nunca pode impedir a criança de
   avançar.** O que ela precisa vem primeiro; o enfeite vem depois, cada um no
   seu próprio try/catch.

   Uso:  node _qa/pcruim.js <arquivo.html> [quantas_fases]
   Sai 0 se passou, 1 se travou, 2 se não deu para medir.
   ============================================================ */
/* ⚠️⚠️ LICAO PAGA (set/2026, na 3a tentativa de publicar o mesmo conserto): o
   `require` do Playwright fica no TOPO, fora de qualquer try. Num lugar sem
   Playwright — o runner do GitHub, por exemplo — ele estoura na hora e o Node
   sai com codigo **1**, que a esteira le como REPROVOU. Mas o portao nao
   reprovou nada: ele nem conseguiu comecar. Isso e codigo **2** (NAO MEDI), e a
   diferenca decide se a entrega para ou segue. */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + '). ' +
              'Este portao roda na bancada local, onde ha Chromium.');
  process.exit(2);
}
const path = require('path');

const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

/* Os enfeites que a casa usa no fim de fase. Todos são decoração: nenhum deles
   pode ser condição para a criança seguir. */
const ENFEITES = ['festa', 'sCerto', 'mascoteFesteja', 'paraDeVigiar', 'confete',
                  'arma', 'sFesta', 'mascoteFala', 'vibra'];

(async () => {
  const arquivo = process.argv[2];
  const limite = parseInt(process.argv[3] || '0', 10) || 6;
  if (!arquivo) { console.log('uso: node _qa/pcruim.js <arquivo.html> [fases]'); process.exit(2); }

  let b, p;
  try {
    b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']});
    p = await b.newPage({viewport: {width: 1024, height: 600}});   // netbook da escola
  } catch (e) { console.log('NAO MEDI: Chromium nao abriu — ' + e.message); process.exit(2); }

  p.on('pageerror', () => {});   // erro de enfeite e ESPERADO aqui: e o teste

  await p.goto('file://' + path.resolve(arquivo), {waitUntil: 'load', timeout: 30000});
  await p.waitForTimeout(2000);

  const total = await p.evaluate(() => {
    try { return (typeof FASES !== 'undefined' && FASES.length) ? FASES.length : 0; }
    catch (e) { return 0; }
  });
  if (!total) {
    console.log('NAO MEDI: esta atividade nao expoe FASES (HTML proprio) — ' +
                'este portao so mede as MONTADAS.');
    await b.close(); process.exit(2);
  }

  /* ⭐ QUEBRA OS ENFEITES. Cada um passa a estourar, como estouraria num PC
     sem canvas, sem audio ou com a pose do mascote faltando. */
  await p.evaluate((nomes) => {
    window.__quebrados = [];
    nomes.forEach(n => {
      if (typeof window[n] === 'function') {
        window[n] = function () { throw new Error('[pc-ruim] ' + n + ' falhou de proposito'); };
        window.__quebrados.push(n);
      }
    });
  }, ENFEITES);
  const quebrados = await p.evaluate(() => window.__quebrados);
  if (!quebrados.length) {
    console.log('NAO MEDI: nenhum dos enfeites conhecidos existe nesta atividade ' +
                '(' + ENFEITES.join(', ') + ') — nada foi testado.');
    await b.close(); process.exit(2);
  }

  const quantas = Math.min(total, limite);
  const presas = [];

  for (let i = 0; i < quantas; i++) {
    try {
      await p.evaluate((n) => montaFase(n), i);
      await p.waitForTimeout(900);
      /* re-quebra: montar a fase pode ter reposto alguma funcao */
      await p.evaluate((nomes) => {
        nomes.forEach(n => {
          if (typeof window[n] === 'function' && String(window[n]).indexOf('[pc-ruim]') < 0)
            window[n] = function () { throw new Error('[pc-ruim] ' + n + ' falhou de proposito'); };
        });
      }, ENFEITES);

      /* chama o fim de fase como a peca chamaria */
      const r = await p.evaluate(async () => {
        const antes = (document.getElementById('app') || document.body).innerHTML.length;
        try { window.mostraBanner('teste de fim de fase', function () { window.__andou = 1; }); }
        catch (e) { return {erro: 'mostraBanner ESTOUROU: ' + e.message}; }
        await new Promise(r => setTimeout(r, 600));

        const banner = document.getElementById('banner');
        const visivel = !!(banner && banner.offsetHeight > 0 &&
                           /\bshow\b/.test(banner.className || ''));
        const bt = document.getElementById('bcta');
        const btVisivel = !!(bt && bt.offsetHeight > 0 && bt.offsetWidth > 0);
        const temAcao = !!(bt && typeof bt.onclick === 'function');
        window.__andou = 0;
        if (bt) { try { bt.click(); } catch (e) {} }
        await new Promise(r => setTimeout(r, 400));
        return {visivel: visivel, btVisivel: btVisivel, temAcao: temAcao,
                andou: !!window.__andou, antes: antes};
      });

      if (r.erro) presas.push('fase ' + (i + 1) + ': ' + r.erro);
      else if (!r.visivel) presas.push('fase ' + (i + 1) + ': o BANNER nao apareceu');
      else if (!r.btVisivel) presas.push('fase ' + (i + 1) + ': o banner apareceu mas o BOTAO nao esta visivel');
      else if (!r.temAcao) presas.push('fase ' + (i + 1) + ': o botao existe mas nao tem ACAO (clique morto)');
      else if (!r.andou) presas.push('fase ' + (i + 1) + ': cliquei no botao e a fase NAO andou');
    } catch (e) {
      presas.push('fase ' + (i + 1) + ': nao consegui medir — ' + e.message);
    }
  }

  await b.close();

  if (presas.length) {
    console.log(arquivo + ' -> PRESA no PC ruim (enfeites quebrados de proposito: ' +
                quebrados.join(', ') + '):');
    presas.slice(0, 8).forEach(m => console.log('    ✗ ' + m));
    if (presas.length > 8) console.log('    ... e mais ' + (presas.length - 8));
    console.log('   Regra: enfeite NUNCA pode impedir a crianca de avancar. Ponha a');
    console.log('   mensagem, o banner e a ACAO do botao ANTES dos enfeites, e cada');
    console.log('   enfeite no seu proprio try/catch.');
    process.exit(1);
  }
  console.log(arquivo + ' -> pc-ruim ok: com ' + quebrados.length +
              ' enfeite(s) falhando (' + quebrados.join(', ') + '), o banner apareceu, ' +
              'o botao ficou visivel e a fase andou nas ' + quantas + ' fases medidas.');
  process.exit(0);
})();
