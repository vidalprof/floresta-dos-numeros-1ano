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
const fs = require('fs');

/* ⚠️ LICAO PAGA (Detetive, ago/2026): a LACUNA do completar ("___" na tela) vira
   uma PAUSA no audio (o `montar._fonetica_voz` troca por "…", senao a voz lia
   "underline"). Como o `_` e caractere de palavra (\w), a norma ANTIGA mantinha
   o "___" na tela mas apagava o "…" da voz -> "diferentes" numa fase que esta
   certa. O buraco do preenchimento e um GAP nos dois lados: ele sai da conta.
   Por isso a classe agora e `[^a-z0-9 ]` (tira `_` e `…`), como o achata do 0n. */
const norm = t => (t || '').toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();

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
  /* ⚠️ LICAO PAGA (ago/2026, nas duas atividades do ESQUELETO): este portao so
     sabia andar pela `FASES_MESTRE` — a lista GLOBAL das atividades ESCRITAS A
     MAO. Numa atividade MONTADA as fases sao DADOS (`FASES` + `montaFase(i)`) e
     nao existem como funcao global: o `window[nome]()` estourava, o `catch`
     engolia, a tela ficava na capa e o portao carimbava
     "a tela nao tem voz nenhuma" nas 39 fases. Ele nao mediu nada — reprovou a
     propria cegueira. E a mesma familia do `_qa/fluxo.py` e do
     `_qa/fala_o_escrito.js`: quem anda pela atividade tem que conhecer as DUAS
     formas dela. Portao que nao sabe abrir a fase tem que sair com codigo 2
     ("nao medi"), nunca com 1 ("reprovado").                                */
  const montada = await p0.evaluate(() => typeof FASES !== 'undefined' && typeof montaFase === 'function');
  const fases = montada
    ? await p0.evaluate(() => FASES.map((f, i) => 'fase ' + (i + 1)))
    : await p0.evaluate(() => (typeof FASES_MESTRE !== 'undefined'
        ? FASES_MESTRE.map(f => f[0]).filter(f => f !== 'mFim') : []));
  await p0.close();
  if (!fases.length) {
    console.log('%s -> nao achei nem FASES nem FASES_MESTRE. NAO MEDI NADA (isso nao e "passou").', arq);
    await b.close(); process.exit(2);
  }

  let iguais = 0; const problemas = [];
  for (let i = 0; i < fases.length; i++) {
    const f = fases[i];
    const p = await b.newPage({viewport: {width: 412, height: 820}});
    await p.goto('file://' + path.resolve(arq)); await p.waitForTimeout(250);
    if (montada) {
      /* ⚠️ NAO se troca o `falar` da atividade montada: e ELE que guarda o
         `falaTela` (motor.html), que e a resposta da pergunta deste portao —
         qual audio o alto-falante repete. Trocando o `falar`, a resposta nunca
         nascia. O que se desliga aqui e so o TOCADOR: sem `play`, o `narr` fica
         parado, o guarda "uma voz por vez" nao segura ninguem e o motor faz o
         resto do caminho dele, inteiro.                                     */
      await p.evaluate(() => { HTMLMediaElement.prototype.play = function () { return Promise.resolve(); }; });
      try {
        await p.evaluate(k => {
          try { perfil = {nome: 'ANA', fig: ID.pre + '_cr1'}; } catch (e) {}
          montaFase(k, function () {});
        }, i);
      } catch (e) {}
    } else {
      /* ⚠️ `depoisDaFala` TAMBEM narra — e por ela que passa o `introEPergunta()`,
         que e como quase toda fase toca a abertura. Com o antigo stub vazio, o
         portao dizia "a tela nao tem voz nenhuma" numa fase FALADA (o porao do
         navio). Portao que acusa quem esta certo ensina a ignorar portao.    */
      await p.evaluate(() => { window.falar = function (id) { window.falaAtual = id; if (!window.__t) window.__t = id; };
                               window.depoisDaFala = function (id) { if (!window.__t) window.__t = id; }; });
      try { await p.evaluate(n => { window[n](); }, f); } catch (e) {}
    }
    await p.waitForTimeout(380);
    const r = await p.evaluate(() => {
      /* ⚠️ LICAO PAGA (ago/2026): este portao lia o PRIMEIRO balao da tela e
         reprovou as 32 fases de uma atividade correta. Numa atividade montada
         existem dois: o enunciado do conteudo.json e o da peca — e a regra
         `.centro.tembalaopeca > .balao{display:none}` ESCONDE o enunciado,
         porque quem manda na tela e a peca. O portao comparava a voz com um
         texto que a crianca nao ve.
         Portao tem que medir o que esta NA TELA, nao o que esta no HTML. */
      const bal = [...document.querySelectorAll('.tela .balao:not(.pequeno)')]
        .filter(b => getComputedStyle(b).display !== 'none' &&
                     b.getBoundingClientRect().height > 0)[0] || null;
      /* ⚠️ na atividade MONTADA quem responde "qual audio o alto-falante toca"
         e o proprio motor (`vozDaTela()` = `falaTela` ou, na falta dele, a
         gravacao DO QUE ESTA ESCRITO). Perguntar so pelo `falaTela` era medir
         por um caminho que o motor nem sempre usa — e todo portao que pergunta
         diferente de como o motor responde inventa defeito.                 */
      const doMotor = (typeof vozDaTela === 'function') ? vozDaTela() : '';
      return {id: doMotor || (typeof falaTela !== 'undefined' && falaTela) || window.__t || null,
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
