/* ============================================================
   PORTÃO DO ELEMENTO COBERTO — "o dedo alcança o que a criança quer tocar?"

   NASCEU DE UM PEDIDO DIRETO DO MARCOS (set/2026), sobre a Pinta e Monta do 1º
   ano: *"a área de pintura de algumas imagens fica em cima das cores,
   dificultando para os alunos escolherem as cores, tendo que diminuir o zoom
   manualmente no navegador"*. E ele completou dizendo o que queria de verdade:
   *"tipo de erros que seria legal o profissional que criamos pegar"*.

   Dá para pegar, e sem calibrar nada: é geometria. A pergunta é única —
   **no centro deste botão, quem responde ao toque?** Se responde OUTRO
   elemento, o de baixo está inalcançável, por mais bonito que pareça no print.

   MEDIDO na Pinta e Monta em 1024x600 (o netbook da escola): 25 elementos com o
   centro coberto. As miniaturas dos desenhos ficavam ATRÁS do quadro de pintura,
   e as cores idem — porque a paleta é irmã do quadro no HTML e, empilhadas em
   coluna, o quadro (que cresce com a altura da tela) empurrava a paleta para
   trás dele. Numa tela baixa isso é garantido, não eventual.

   POR QUE OS PORTÕES QUE JÁ EXISTIAM NÃO PEGAVAM:
     · `_qa/leiaute.js` mede TAMANHO (alvo < 40px) — e aqui os alvos tinham
       40px certinhos, só estavam debaixo de outra coisa;
     · `_qa/encaixe.js` mede se o conteúdo cabe na caixa — e cabia;
     · o print parece bom: as cores APARECEM, com a bordinha de cima de fora.
   O defeito só existe no gesto, e só o `elementFromPoint` o enxerga.

   ⚠️ DUAS ARMADILHAS que este portão já pagou, e por isso estão no código:
     1. FORA DA JANELA não é coberto. O `elementFromPoint` devolve `null` para o
        que está abaixo do scroll — e listas que rolam (a galeria de desenhos)
        são de propósito. Sem esse cuidado, ele acusava 28 inocentes.
     2. FILHO E PAI não se cobrem. Um botão com <img> dentro devolve a <img> no
        centro, e isso é o normal — não é obstrução.

   TAMANHOS que ele mede: o netbook da escola (1024x600) e o celular (412x820).
   É onde falta espaço; numa tela grande quase nada se cobre.

   Uso:  node _qa/sobreposto.js <arquivo.html> [tela1 tela2 ...]
   Sai 0 se tudo alcançável, 1 se algo está coberto, 2 se não deu para medir.
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + ').');
  process.exit(2);
}
const path = require('path');

const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const TELAS = [[1024, 600, 'netbook da escola'], [412, 820, 'celular']];

/* o que a criança toca */
const TOCAVEL = 'button, [onclick], .btn, .op, .cor, .pc, .lig, .mcarta, .gthumb, ' +
                '.thumb, .mini, .opt, .optbtn, .carta, .peca, input, select, canvas';

(async () => {
  const arquivo = process.argv[2];
  const telas = process.argv.slice(3);
  if (!arquivo) { console.log('uso: node _qa/sobreposto.js <arquivo.html> [telas...]'); process.exit(2); }

  let b;
  try { b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']}); }
  catch (e) { console.log('NAO MEDI: Chromium nao abriu — ' + e.message); process.exit(2); }

  const url = 'file://' + path.resolve(arquivo);
  const achados = [];
  let medidas = 0;

  for (const [w, h, nomeTela] of TELAS) {
    const p = await b.newPage({viewport: {width: w, height: h}});
    p.on('pageerror', () => {});
    try { await p.goto(url, {waitUntil: 'load', timeout: 30000}); }
    catch (e) { await p.close(); continue; }
    await p.waitForTimeout(1800);

    /* entra na atividade (a capa não tem o que se cobrir) */
    await p.evaluate(() => {
      const b = [...document.querySelectorAll('button,.btn,[onclick]')]
        .find(e => /come|jogar|vamos|iniciar|pintar|entrar/i.test(e.textContent || ''));
      if (b) b.click();
    });
    await p.waitForTimeout(2000);

    /* se a atividade tem fases, passeia por algumas; senão fica na tela atual */
    const nFases = await p.evaluate(() => {
      try { return (typeof FASES !== 'undefined' && FASES.length) ? FASES.length : 0; }
      catch (e) { return 0; }
    });
    const paradas = nFases ? [0, Math.floor(nFases / 3), Math.floor(nFases * 2 / 3)] : [null];

    for (const f of paradas) {
      if (f !== null) {
        try { await p.evaluate((n) => montaFase(n), f); await p.waitForTimeout(1100); }
        catch (e) { continue; }
      }
      const r = await p.evaluate((sel) => {
        const vis = el => {
          const r = el.getBoundingClientRect();
          if (r.width < 8 || r.height < 8) return false;
          const cs = getComputedStyle(el);
          return cs.display !== 'none' && cs.visibility !== 'hidden' &&
                 parseFloat(cs.opacity) > 0.05 && cs.pointerEvents !== 'none';
        };
        const out = [], esmagados = [];
        let vistos = 0;
        const nome = e => (e.id ? '#' + e.id :
          '.' + String(e.className || e.tagName).split(' ')[0]).slice(0, 26);

        /* ⚠️⚠️ LICAO PAGA NA HORA (set/2026): eu cresci o palco da Pinta e Monta,
           o flex ESMAGOU a coluna das miniaturas para 8 PIXELS de largura, e este
           portao disse "ok" — corretamente, porque nada estava COBERTO. Estava
           espremido, que e outro defeito com o mesmo efeito: a crianca nao ve.
           Foi a FOTO que mostrou, nao a conta. Entao a conta aprendeu.

           ⚠️ DUAS tentativas erradas antes desta, e elas valem mais que o
           conserto, porque sao o jeito de errar que se repete:

           1a) comparei `getComputedStyle(el).width` com o
               `getBoundingClientRect()`. Medido aqui: os dois dao o MESMO
               numero, porque o `computed style` de largura devolve o valor
               USADO (ja esmagado), nao o que o CSS pediu. Era 1 dividido por 1;
               o portao nunca acusaria nada. Quem sabe o que foi PEDIDO e a
               REGRA de CSS — dai o `pedidaPx` abaixo, que abre as folhas de
               estilo, respeita as media queries e le a declaracao em px.
           2a) com a largura pedida na mao, botei um LIMIAR chutado: "menos de
               40% do pedido = esmagado". Refiz a quebra de proposito na Pinta e
               Monta e a galeria caiu de 116px para 54px — 47%, ACIMA do limiar,
               e o portao passou de novo. So que 54px com miniatura de 104px
               dentro ja e o defeito inteiro: a crianca ve meia miniatura.
               Numero chutado nao mede nada; o que mede e FATO GEOMETRICO.

           O FATO, entao, sem calibrar nada: **o conteudo e mais largo que a
           caixa E a caixa esconde o que sobra** (`overflow-x:hidden|clip`).
           Ai o pedaco que sobra nao esta rolavel nem visivel: sumiu.
           Medido: quebrado -> #galeria client=54 scroll=112 hidden; bom ->
           client=116 scroll=116. Separacao limpa, sem limiar nenhum.
           `overflow-x:auto` NAO entra: ali a pessoa rola e alcanca. */
        function pedidaPx(el) {
          let v = null;
          const anda = (regras) => {
            for (const r of regras) {
              if (r.media) {
                try { if (matchMedia(r.conditionText).matches) anda(r.cssRules); } catch (e) {}
                continue;
              }
              if (!r.selectorText || !r.style || !r.style.width) continue;
              let casa = false;
              try { casa = el.matches(r.selectorText); } catch (e) {}
              if (!casa) continue;
              const m = /^(\d+(?:\.\d+)?)px$/.exec(r.style.width.trim());
              if (m) v = parseFloat(m[1]);   /* a ultima que casa vence, como no cascata */
            }
          };
          for (const s of document.styleSheets) { try { anda(s.cssRules); } catch (e) {} }
          const inline = /^(\d+(?:\.\d+)?)px$/.exec((el.style && el.style.width || '').trim());
          if (inline) v = parseFloat(inline[1]);
          return v;
        }

        /* o esmagado se procura em TUDO, nao so no tocavel: quem sumiu na
           Pinta e Monta foi a COLUNA da galeria, que nao e botao nenhum. */
        for (const el of document.querySelectorAll('div,section,aside,nav,ul,main,form')) {
          const rr = el.getBoundingClientRect();
          if (rr.height < 8 || el.clientWidth < 10) continue;   /* escondido/fechado */
          const cs0 = getComputedStyle(el);
          if (cs0.display === 'none' || cs0.visibility === 'hidden') continue;
          /* so `hidden`/`clip` CORTAM. Em `auto`/`scroll` a pessoa rola e alcanca. */
          if (cs0.overflowX !== 'hidden' && cs0.overflowX !== 'clip') continue;
          /* texto cortado com reticencias e decisao de design, nao esmagamento */
          if (cs0.textOverflow === 'ellipsis') continue;
          if (!el.querySelector('*')) continue;   /* caixa so de texto: idem */
          const sobra = el.scrollWidth - el.clientWidth;
          if (sobra <= 8) continue;               /* 8px = folga de arredondamento */
          const pedida = pedidaPx(el);
          esmagados.push({q: nome(el), tem: el.clientWidth,
                          precisa: el.scrollWidth, pediu: pedida});
        }

        for (const el of document.querySelectorAll(sel)) {
          if (!vis(el)) continue;
          const rc = el.getBoundingClientRect();
          const cx = rc.left + rc.width / 2, cy = rc.top + rc.height / 2;
          /* ⚠️ armadilha 1: fora da janela não é coberto — é rolagem */
          if (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight) continue;
          vistos++;
          const emCima = document.elementFromPoint(cx, cy);
          if (!emCima) continue;
          /* ⚠️ armadilha 2: filho e pai não se cobrem */
          if (emCima === el || el.contains(emCima) || emCima.contains(el)) continue;
          out.push({q: nome(el), por: nome(emCima),
                    tam: Math.round(rc.width) + 'x' + Math.round(rc.height)});
        }
        return {cobertos: out, vistos: vistos, esmagados: esmagados};
      }, TOCAVEL);

      medidas += r.vistos;
      for (const c of r.cobertos) {
        achados.push({tela: nomeTela, tipo: 'coberto',
                      texto: c.q + ' (' + c.tam + ') esta DEBAIXO de ' + c.por});
      }
      for (const e of (r.esmagados || [])) {
        achados.push({tela: nomeTela, tipo: 'esmagado',
                      texto: e.q + ' foi ESMAGADO pelo vizinho: o conteudo precisa de ' +
                             e.precisa + 'px, a caixa tem ' + e.tem +
                             'px e ESCONDE o resto' +
                             (e.pediu ? ' (o CSS pedia ' + e.pediu + 'px)' : '')});
      }
    }
    await p.close();
  }
  await b.close();

  if (!medidas) {
    console.log('NAO MEDI: nenhum elemento tocavel visivel em ' + arquivo);
    process.exit(2);
  }

  if (achados.length) {
    /* agrupa: 20 cores debaixo do mesmo quadro é UM defeito, não 20 */
    const grupos = {};
    for (const a of achados) {
      const k = a.tela + '|' + a.texto;
      grupos[k] = grupos[k] || {...a, n: 0};
      grupos[k].n++;
    }
    const lista = Object.values(grupos).sort((a, b) => b.n - a.n);
    const nCob = lista.filter(g => g.tipo === 'coberto').length;
    const nEsm = lista.filter(g => g.tipo === 'esmagado').length;
    console.log(arquivo + ' -> ' + (nCob ? nCob + ' COBERTO(s)' : '') +
                (nCob && nEsm ? ' e ' : '') + (nEsm ? nEsm + ' ESMAGADO(s)' : '') +
                ' (de ' + medidas + ' alvos conferidos):');
    for (const g of lista.slice(0, 10)) {
      console.log('    ✗ [' + g.tela + '] ' + g.texto + (g.n > 1 ? ' ×' + g.n : ''));
    }
    if (lista.length > 10) console.log('    ... e mais ' + (lista.length - 10));
    if (nCob) {
      console.log('   COBERTO: a crianca ve o elemento mas o dedo nao alcanca — quem');
      console.log('   responde ao toque no centro dele e outro. Costuma ser altura fixa');
      console.log('   que estoura em tela baixa, ou dois irmaos empilhados sem espaco.');
    }
    if (nEsm) {
      console.log('   ESMAGADO: o vizinho tomou a largura e a caixa cortou o que sobrou.');
      console.log('   Cura: `flex:0 0 <largura>` na coluna que nao pode encolher, e');
      console.log('   conferir se algum pai ainda tem `max-width` de quando era 1 coluna.');
    }
    process.exit(1);
  }

  console.log(arquivo + ' -> sobreposicao ok: ' + medidas +
              ' alvo(s) conferidos em 2 tamanhos, todos alcancaveis pelo dedo.');
  process.exit(0);
})();
