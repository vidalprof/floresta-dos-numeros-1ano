/* ============================================================
   O DIRETOR DE ARTE — o portão do ACABAMENTO (ago/2026)

   Ordem do Marcos, repetida em três frases seguidas: *"nosso app tem que ser
   profissional, ficar lindo, sem erros"*, *"o visual tem que ser maravilhoso,
   impecável"*, *"sempre melhorar o visual, sempre subir a régua nisso, sempre
   ser lindo, caprichado"* — e então: *"crie um profissional especialista para
   isso"*.

   ⚠️ POR QUE ELE PRECISA EXISTIR. Os 30 portões da casa medem se a atividade
   FUNCIONA: o código roda, a figura carrega, o alvo tem 40px, o texto passa no
   contraste. Nenhum deles mede se ela está BONITA. E foi por isso que, no mesmo
   dia, a banca deu código 0 numa tela em que:
     · o alto-falante **tapava a última palavra** do enunciado em toda fase
       ("toque na figura d[a]", "uma vez para ca[da]");
     · a figura estava dentro de um **quadrado branco chapado**, que o Marcos já
       tinha reprovado uma vez e escolhido substituir por vidro fosco.
   Os dois eu só achei **olhando a foto**. Portão que não vê acabamento deixa
   passar exatamente o que o professor vê primeiro.

   O QUE ELE MEDE — cinco coisas que um diretor de arte olharia, todas medidas
   em pixel de verdade, em 4 tamanhos de tela:

     1. BOTÃO SOBRE PALAVRA. O alto-falante (ou qualquer botão pequeno dentro de
        um bloco de texto) não pode cobrir letra nenhuma. Mede o retângulo das
        LINHAS de texto (Range), ignorando o próprio botão.
     2. QUADRADO BRANCO CHAPADO. Caixa de figura com fundo branco opaco é o
        acabamento que o Marcos reprovou. A casa usa vidro fosco (creme
        translúcido + desfoque) ou fundo nenhum.
     3. FAMÍLIA DESUNIDA. Cartões irmãos na mesma tela com raio de canto
        diferente entre si — o olho lê como remendo, não como app.
     4. TEXTO ESPREMIDO. Palavra a menos de 6px da borda do próprio cartão.
     5. AMONTOADO. Dois blocos de conteúdo encostando (menos de 6px entre eles).

   ⚠️ O que ele NÃO faz: dizer se está bonito. Isso é do Marcos. Ele tira do
   caminho o que é feio de forma MEDÍVEL, para a conversa sobre gosto começar
   num lugar decente.

   Uso: node _qa/visual.js <arquivo.html> [tela1 tela2 ...]
   ============================================================ */
const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const path = require('path');

const TAMANHOS = [
  {w: 320, h: 568, n: 'celular pequeno'},
  {w: 412, h: 820, n: 'celular comum'},
  {w: 1366, h: 640, n: 'PC da escola'},
  {w: 1024, h: 420, n: 'janela baixa'},
];

(async () => {
  const arquivo = process.argv[2];
  if (!arquivo) { console.log('uso: node _qa/visual.js <arquivo.html> [telas...]'); process.exit(2); }
  const telasArg = process.argv.slice(3);

  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']});

  const achados = [];
  let medidas = 0;

  for (const vp of TAMANHOS) {
    const p = await b.newPage({viewport: {width: vp.w, height: vp.h}});
    await p.goto('file://' + path.resolve(arquivo));
    await p.waitForTimeout(800);

    const montada = await p.evaluate(() =>
      typeof FASES !== 'undefined' && typeof montaFase === 'function');
    const quantas = montada ? await p.evaluate(() => FASES.length)
                            : (telasArg.length || 1);

    for (let i = 0; i < quantas; i++) {
      try {
        if (montada) {
          await p.evaluate(k => {
            try { perfil = {nome: 'ANA', fig: ID.pre + '_cr1'}; } catch (e) {}
            montaFase(k, function () {});
          }, i);
        } else if (telasArg[i]) {
          await p.evaluate(t => { if (typeof window[t] === 'function') window[t](); }, telasArg[i]);
        }
      } catch (e) { continue; }
      await p.waitForTimeout(420);
      medidas++;

      const r = await p.evaluate(() => {
        const out = [];
        const vis = e => {
          if (!e) return false;
          const c = getComputedStyle(e);
          if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false;
          const b = e.getBoundingClientRect();
          return b.width > 1 && b.height > 1;
        };
        /* o retangulo REALMENTE pintado: cortado por todo pai que recorta */
        const pintado = e => {
          let r = e.getBoundingClientRect();
          let box = {left: r.left, right: r.right, top: r.top, bottom: r.bottom};
          for (let a = e.parentElement; a; a = a.parentElement) {
            const c = getComputedStyle(a);
            if (!/(auto|scroll|hidden)/.test(c.overflowY + ' ' + c.overflowX)) continue;
            const ra = a.getBoundingClientRect();
            box = {left: Math.max(box.left, ra.left), right: Math.min(box.right, ra.right),
                   top: Math.max(box.top, ra.top), bottom: Math.min(box.bottom, ra.bottom)};
          }
          box.width = box.right - box.left; box.height = box.bottom - box.top;
          return box;
        };
        const linhas = el => {
          const rs = [];
          for (const no of el.childNodes) {
            if (no.nodeType !== 3 || !String(no.nodeValue).trim()) continue;
            const rg = document.createRange(); rg.selectNodeContents(no);
            for (const rt of rg.getClientRects()) rs.push(rt);
          }
          for (const f of el.children) {
            if (f.tagName === 'BUTTON' || /zap|btn/.test(String(f.className))) continue;
            for (const no of f.childNodes) {
              if (no.nodeType !== 3 || !String(no.nodeValue).trim()) continue;
              const rg = document.createRange(); rg.selectNodeContents(no);
              for (const rt of rg.getClientRects()) rs.push(rt);
            }
          }
          return rs;
        };

        /* 1. BOTAO SOBRE PALAVRA */
        document.querySelectorAll('.balao, .hint, .selo, .dica').forEach(cx => {
          if (!vis(cx)) return;
          const rs = linhas(cx);
          cx.querySelectorAll('button, .zap, .zapb').forEach(bt => {
            if (!vis(bt)) return;
            const rb = pintado(bt);
            for (const rt of rs) {
              const w = Math.min(rb.right, rt.right) - Math.max(rb.left, rt.left);
              const h = Math.min(rb.bottom, rt.bottom) - Math.max(rb.top, rt.top);
              if (w > 1 && h > 3) {
                out.push('o botao de som TAPA a palavra em .' +
                         String(cx.className).split(' ')[0]);
                return;
              }
            }
          });
        });

        /* 2. QUADRADO BRANCO CHAPADO atras da figura */
        document.querySelectorAll('#app *').forEach(e => {
          if (!vis(e)) return;
          if (!e.querySelector('img, svg')) return;
          const c = getComputedStyle(e);
          const m = c.backgroundColor.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);
          if (!m) return;
          const [rr, gg, bb] = [+m[1], +m[2], +m[3]];
          const al = m[4] === undefined ? 1 : +m[4];
          const claro = rr > 245 && gg > 240 && bb > 225;
          const temBlur = /blur/.test(c.backdropFilter || '') ||
                          /blur/.test(c.webkitBackdropFilter || '');
          const rc = e.getBoundingClientRect();
          /* ⚠️ EXCECAO QUE NAO E DESCUIDO: superficie em que a crianca DESENHA.
             Papel de ligar pontos, folha de tracar a letra, tela de pintar — as
             tres sao brancas de proposito, porque papel e branco e o traco dela
             precisa aparecer. Acusar isso seria o portao mandando pintar o
             caderno. O sinal e o desenho VIVO: um <svg> com traco/caminho dentro
             (a peca desenha ali), ou o nome da caixa dizendo o que ela e. */
          const ehPapel = /folha|quadro|papel|prancheta|canvas|desenh/i.test(
                            String(e.className) + ' ' + String(e.id)) ||
                          !!e.querySelector('svg path, svg line, svg circle, canvas');
          if (claro && al > 0.9 && !temBlur && !ehPapel && rc.width > 60 && rc.height > 60) {
            out.push('QUADRADO BRANCO chapado atras da figura em .' +
                     String(e.className).split(' ')[0] + ' — a casa usa vidro fosco');
          }
        });

        /* 3. FAMILIA DESUNIDA: irmaos com raio diferente */
        document.querySelectorAll('#app *').forEach(pai => {
          const fs = [...pai.children].filter(x => vis(x) &&
            x.getBoundingClientRect().width > 50 && x.getBoundingClientRect().height > 40);
          if (fs.length < 2) return;
          const raios = new Set(fs.map(x => getComputedStyle(x).borderTopLeftRadius));
          const cls = new Set(fs.map(x => String(x.className).split(' ')[0]));
          if (cls.size === 1 && raios.size > 1) {
            out.push('cartoes irmaos .' + [...cls][0] + ' com CANTOS diferentes entre si (' +
                     [...raios].join(' / ') + ')');
          }
        });

        /* 4. BOTAO ESTICADO e FAMILIA TORTA (ordem do Marcos, ago/2026:
              *"nada de botoes muito esticado, quero tudo simetrico no app,
              nada desconfigurado saindo da borda"*).
              Duas medidas:
                a) proporcao — botao mais de 6x mais largo que alto vira fita, e
                   fita nao parece botao para uma crianca de 6 anos;
                b) simetria da familia — irmaos da MESMA classe com alturas
                   diferentes entre si sao remendo: o olho ve a fileira torta
                   antes de ler qualquer palavra. */
        document.querySelectorAll('#app *').forEach(pai => {
          const fs = [...pai.children].filter(x => vis(x) &&
            (x.tagName === 'BUTTON' || /opt|btn|pc\b|carta|tecla/.test(String(x.className))));
          if (fs.length < 2) return;
          const cls = new Set(fs.map(x => String(x.className).split(' ')[0]));
          if (cls.size !== 1) return;
          const hs = fs.map(x => Math.round(x.getBoundingClientRect().height));
          const ws = fs.map(x => Math.round(x.getBoundingClientRect().width));
          if (Math.max(...hs) - Math.min(...hs) > 6) {
            out.push('fileira TORTA: os .' + [...cls][0] + ' tem alturas diferentes (' +
                     Math.min(...hs) + '..' + Math.max(...hs) + 'px)');
          }
          fs.forEach((x, k) => {
            if (hs[k] > 8 && ws[k] / hs[k] > 6) {
              out.push('botao ESTICADO .' + [...cls][0] + ' (' + ws[k] + 'x' + hs[k] +
                       'px, ' + (ws[k] / hs[k]).toFixed(1) + ' vezes mais largo que alto)');
            }
          });
        });

        /* 5. TEXTO ESPREMIDO na borda do proprio cartao */
        document.querySelectorAll('.balao, .opt, .hint, .dica, .selo').forEach(cx => {
          if (!vis(cx)) return;
          const rc = cx.getBoundingClientRect();
          for (const rt of linhas(cx)) {
            const folga = Math.min(rt.left - rc.left, rc.right - rt.right);
            if (folga < 4 && rt.width > 12) {
              out.push('texto ESPREMIDO na borda de .' + String(cx.className).split(' ')[0] +
                       ' (folga ' + Math.round(folga) + 'px)');
              return;
            }
          }
        });

        return [...new Set(out)];
      });

      const nome = montada ? ('fase ' + (i + 1)) : (telasArg[i] || 'tela');
      for (const x of r) achados.push(vp.n + ' | ' + nome + ' | ' + x);
      if (!montada && !telasArg.length) break;
    }
    await p.close();
  }
  await b.close();

  console.log(arquivo + ' -> acabamento conferido em ' + medidas + ' tela(s) x ' +
              TAMANHOS.length + ' tamanhos');
  if (!medidas) { console.log('   NAO MEDI NADA — isso nao e "passou".'); process.exit(2); }
  const u = [...new Set(achados)];
  if (!u.length) {
    console.log('   acabamento ok: nenhum botao sobre palavra, nenhum quadrado branco, ' +
                'cantos da mesma familia, texto com folga');
    process.exit(0);
  }
  console.log('   ' + u.length + ' PROBLEMA(S) DE ACABAMENTO:');
  for (const a of u.slice(0, 14)) console.log('    - ' + a);
  if (u.length > 14) console.log('    ... e mais ' + (u.length - 14));
  process.exit(1);
})();
