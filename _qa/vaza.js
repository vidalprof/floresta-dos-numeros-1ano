/* ============================================================
   PORTÃO — "o conteúdo cabe dentro do próprio cartão?"

   ⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem viu, não portão nenhum:
   *"o dizer da figura fica fora do quadrado branco, ficou feio"* e, depois,
   *"na ouça e ache tem a letra no quadrado e embaixo a letra parte dentro do
   quadrado e parte fora"*.

   Nenhum dos 28 portões pegava isso. O `_qa/leiaute.js` mede se algo saiu **da
   TELA**, se o alvo tem 40px, se um botão cobre outro — mas não se o texto saiu
   **do próprio pai**. Uma tela pode estar inteira dentro do celular e ainda
   assim ter o nome pendurado para fora do cartão.

   A causa daquele caso era colisão de nome com o motor (o `.fig` do crachá
   impondo 82px de altura ao cartão da resposta). A colisão já foi fechada no
   integrador — este portão é a rede: se qualquer coisa parecida acontecer de
   novo, ele acusa ANTES de a atividade chegar ao Marcos.

   O que ele mede, em 4 tamanhos de tela e em toda tela da atividade:
   para cada elemento que tem fundo/borda próprios (um "cartão"), se algum filho
   passa da borda dele por mais de 4px, é VAZAMENTO.

   ⚠️ o que ele NÃO acusa, de propósito, porque é desenho legítimo:
   · quem tem `overflow:hidden` (o pai corta e assume isso);
   · quem foi posicionado de propósito para fora (`position:absolute` com
     deslocamento negativo — é o selo que "monta" na borda, um recurso comum);
   · o que está escondido (`display:none`, `visibility:hidden`).

   Uso: node _qa/vaza.js <arquivo.html> [tela1 tela2 ...]
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

const TAMANHOS = [
  {w: 320, h: 568, n: 'celular pequeno'},
  {w: 412, h: 820, n: 'celular comum'},
  {w: 1366, h: 640, n: 'PC 1366 com barras'},
  {w: 1024, h: 420, n: 'janela baixa'},
];

(async () => {
  const arquivo = process.argv[2];
  if (!arquivo) { console.log('uso: node _qa/vaza.js <arquivo.html> [telas...]'); process.exit(2); }
  const telas = process.argv.slice(3);

  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']});

  const achados = [];
  let medidos = 0;

  for (const vp of TAMANHOS) {
    const p = await b.newPage({viewport: {width: vp.w, height: vp.h}});
    await p.goto('file://' + path.resolve(arquivo));
    await p.waitForTimeout(700);

    /* atividade MONTADA: percorre as fases pelo motor. Escrita à mão: chama as
       telas pelo nome, como o resto da banca faz. */
    const montada = await p.evaluate(() => typeof abreFase === 'function' && typeof FASES !== 'undefined');
    const quantas = montada
      ? await p.evaluate(() => FASES.length)
      : (telas.length || 0);

    for (let i = 0; i < Math.max(quantas, 1); i++) {
      try {
        if (montada) {
          await p.evaluate(k => { try { perfil = {nome: 'ANA', fig: (typeof ID === 'object' ? ID.pre : '') + '_cr1'}; } catch (e) {} abreFase(k); }, i);
        } else if (telas[i]) {
          await p.evaluate(t => { if (typeof window[t] === 'function') window[t](); }, telas[i]);
        }
      } catch (e) { continue; }
      await p.waitForTimeout(650);

      const r = await p.evaluate(() => {
        const fora = [];
        const cartoes = [...document.querySelectorAll('#app *')].filter(e => {
          if (e.offsetParent === null) return false;
          const c = getComputedStyle(e);
          if (c.overflow !== 'visible' || c.overflowY !== 'visible') return false;
          const temFundo = c.backgroundColor !== 'rgba(0, 0, 0, 0)' && c.backgroundColor !== 'transparent';
          const temBorda = parseFloat(c.borderTopWidth) > 0 || parseFloat(c.borderBottomWidth) > 0;
          const temSombra = c.boxShadow && c.boxShadow !== 'none';
          if (!(temFundo || temBorda || temSombra)) return false;
          const r = e.getBoundingClientRect();
          return r.width > 40 && r.height > 24;
        });
        for (const ct of cartoes) {
          const rc = ct.getBoundingClientRect();
          for (const f of ct.children) {
            if (f.offsetParent === null) continue;
            const cf = getComputedStyle(f);
            if (cf.position === 'absolute' || cf.position === 'fixed') continue;
            const rf = f.getBoundingClientRect();
            if (rf.width < 2 || rf.height < 2) continue;
            const passa = Math.max(rf.bottom - rc.bottom, rc.top - rf.top,
                                   rf.right - rc.right, rc.left - rf.left);
            if (passa > 4) {
              const nome = '.' + String(ct.className || ct.tagName).split(' ')[0];
              const filho = '.' + String(f.className || f.tagName).split(' ')[0];
              const txt = (f.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 22);
              fora.push(filho + (txt ? ' ("' + txt + '")' : '') + ' vaza ' +
                        Math.round(passa) + 'px de ' + nome);
            }
          }
        }
        return fora;
      });
      medidos++;
      for (const x of new Set(r)) achados.push(vp.n + ' | fase ' + (i + 1) + ' | ' + x);
      if (!montada && !telas.length) break;
    }
    await p.close();
  }
  await b.close();

  console.log(arquivo + ' -> ' + medidos + ' tela(s) medida(s) em ' + TAMANHOS.length + ' tamanhos');
  if (!achados.length) {
    console.log('   vazamento ok: todo texto e figura cabe dentro do proprio cartao');
    process.exit(0);
  }
  const unicos = [...new Set(achados)];
  console.log('   ' + unicos.length + ' VAZAMENTO(S) — conteudo saindo do proprio cartao:');
  for (const a of unicos.slice(0, 14)) console.log('    ' + a);
  if (unicos.length > 14) console.log('    ... e mais ' + (unicos.length - 14));
  process.exit(1);
})();
