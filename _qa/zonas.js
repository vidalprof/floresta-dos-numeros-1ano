/* ============================================================
   CONFERIR AS ZONAS DE "ACHE NA CENA" — pela COR, não pelo olho
   ------------------------------------------------------------
   Quando a arte de uma fase muda, as coordenadas cravadas nela
   ficam apontando para o lugar errado — e o defeito chega na
   criança da pior forma possível: ela toca CERTO e ouve que
   errou. Já aconteceu na cartografia ("o rio" apontava para uma
   célula vazia) e voltaria agora, na troca das cenas do 3º e do
   5º ano.

   ⚠️ E MEDIR NÃO É OLHAR. Na primeira passada eu pus as zonas no
   olho, com uma grade de 10% por cima da figura, e TRÊS delas
   caíram no mato. O que resolve é ler a COR DO PIXEL exatamente
   embaixo de cada alvo, na figura como ela aparece na tela:
   rio tem que dar AZUL, telhado tem que dar VERMELHO, roça tem
   que dar VERDE. Cor bate ou não bate; olho acha.

   ⚠️ file:// SUJA O CANVAS: `getImageData` estoura com
   SecurityError. Por isso a posição se mede no navegador e a cor
   se lê aqui fora, no arquivo da imagem — que é o que este
   script faz.

   USO
     node _qa/zonas.js _naveg/index.html mAldeia 3
                        (arquivo)        (fase)  (quantas rodadas)

   Sai uma linha por alvo com a posição em % e o nome da cor. Ler
   com a pergunta na mão: se a pergunta diz "o rio" e a cor diz
   VERDE, o alvo está no barranco, não no rio.
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

function nomeCor(r, g, b) {
  if (b > r + 25 && b > g + 10) return 'AZUL (agua, ceu)';
  if (r > 120 && r > g + 45 && r > b + 45) return 'VERMELHO (telhado)';
  if (g > r + 15 && g > b + 15) return 'VERDE (mato, grama, roca)';
  if (r > 90 && g > 60 && b < 100 && r > b + 35) return 'MARROM/BEGE (terra, palha, madeira, ponte)';
  if (Math.abs(r - g) < 28 && Math.abs(g - b) < 28 && r > 110) return 'CINZA (rua, calcada)';
  return 'ESCURO/outro (sombra? confira no olho)';
}

/* le a cor de um ponto do arquivo da imagem, sem depender do canvas */
async function corDoArquivo(cam, px, py) {
  const {execFileSync} = require('child_process');
  const out = execFileSync('python3', ['-c', `
from PIL import Image
im=Image.open(${JSON.stringify(cam)}).convert("RGB")
W,H=im.size
print(*im.getpixel((min(W-1,int(W*${px})), min(H-1,int(H*${py})))))
`]).toString().trim().split(/\s+/).map(Number);
  return out;
}

(async () => {
  const arq = process.argv[2], fase = process.argv[3];
  const rodadas = parseInt(process.argv[4] || '1', 10);
  if (!arq || !fase) { console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]); process.exit(2); }
  const pasta = path.dirname(path.resolve(arq));
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                                   args: ['--no-sandbox', '--disable-gpu']});
  let ruins = 0;
  for (let k = 0; k < rodadas; k++) {
    const p = await b.newPage({viewport: {width: 412, height: 820}});
    await p.goto('file://' + path.resolve(arq));
    await p.waitForTimeout(600);
    await p.evaluate(() => { window.falar = function(){}; window.depoisDaFala = function(i,m,cb){setTimeout(cb,50);}; });
    await p.evaluate(f => { window[f](); }, fase);
    await p.waitForTimeout(400);
    /* avanca ate a rodada k respondendo certo (o alvo publica data-qa="1") */
    for (let z = 0; z < k; z++) {
      await p.evaluate(() => { const a = document.querySelector('.janela [data-qa="1"]'); if (a) a.click(); });
      await p.waitForTimeout(1500);
    }
    await p.waitForTimeout(300);
    const r = await p.evaluate(() => {
      const im = document.querySelector('.janela img'); if (!im) return null;
      const ri = im.getBoundingClientRect();
      const bal = document.querySelector('.balao');
      const out = [];
      for (const a of document.querySelectorAll('.janela .achado.mira, .janela .lupamira')) {
        const ra = a.getBoundingClientRect();
        out.push([(ra.left + ra.width / 2 - ri.left) / ri.width,
                  (ra.top + ra.height / 2 - ri.top) / ri.height]);
      }
      return {img: im.getAttribute('src'), q: (bal ? bal.textContent : '').replace(/\s+/g, ' ').trim(), alvos: out};
    });
    await p.close();
    if (!r) { console.log('  (a fase ' + fase + ' nao tem .janela com figura)'); break; }
    console.log('\n' + r.q.slice(0, 88));
    for (const [px, py] of r.alvos) {
      const [cr, cg, cb2] = await corDoArquivo(path.join(pasta, r.img), px, py);
      const nome = nomeCor(cr, cg, cb2);
      if (/ESCURO/.test(nome)) ruins++;
      console.log('   (%s,%s)  rgb=%s  -> %s',
                  (px * 100).toFixed(1).padStart(5), (py * 100).toFixed(1).padStart(5),
                  '(' + [cr, cg, cb2].join(',') + ')'.padEnd(4), nome);
    }
  }
  await b.close();
  console.log('\n' + (ruins ? '  ' + ruins + ' alvo(s) em pixel escuro — confira se e sombra ou se caiu fora'
                            : '  todos os alvos caem em cor identificavel'));
})();
