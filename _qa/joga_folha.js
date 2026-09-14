/* ============================================================
   O JOGADOR DA FOLHA VIVA — ele RESOLVE o caderno, item por item.

   ⭐ POR QUE ELE EXISTE (pergunta do Marcos, 13/set/2026): *"a outra banca,
      aquela que corrige as atividades normais, seria uma boa utilizar para
      essas sequências didáticas?"* — e a resposta honesta foi: a banca do motor
      inteira não, porque ela procura `telaCapa`/`FASES`/`conteudo.json`, que
      folha viva não tem. **Mas três juízes dela mediam coisa que aqui ninguém
      media, e este é o mais sério dos três.**

      O `andar_folha.js` só ANDA o caderno: abre cada folha, vê se estourou JS,
      se alguma figura não carregou, se a folha registra itens. Ele **não
      resolve nada**. Ou seja, até hoje **nada garantia que uma folha pudesse
      ser TERMINADA**: bastava eu escrever uma em que o acerto nunca dispara e a
      banca aprovava. É o "beco sem saída" com a criança dentro — ela tenta,
      acerta, e a folha não fecha.

   COMO ELE SABE A RESPOSTA — e isto é o coração: ele **não adivinha**. Toda
   folha viva chama `registra(id, pagina, certo)`, e o `certo` fica em
   `RESP[id]`. O jogador lê dali. Se um dia a folha registrar a resposta errada,
   o portão de sentido é outro (`resposta_impressa.py`, `revisor.py`); aqui a
   pergunta é só uma: **com a resposta certa na mão, dá para fechar o item?**

   COMO ELE CLICA: as peças publicam `data-qa` (o mesmo contrato do motor). Ele
   casa o `certo` com o `data-qa` e clica na ordem. Quatro famílias têm jeito
   próprio, declarado aqui e não deduzido:
     · `lig…-e-<k>` + `lig…-d-<k>`  → clica a ponta esquerda e depois a direita
     · `esc-<id>`   (teclado)       → abre o quadro e DIGITA a letra
     · `traca-<id>` (canvas)        → varre a letra com o dedo, em serpentina
     · um alvo só com o id          → clica nele (o mural)

   ⚠️ FOLHA QUE ELE NÃO SOUBER RESOLVER **NÃO PASSA CALADA**: ela sai como
      "NAO RESOLVI" e o portão devolve 2 (não medi), nunca 0. Portão que aprova
      o que não mediu é pior que portão nenhum — a casa já pagou essa lição.

   ⚠️ E ELE NÃO SUBSTITUI O `andar_folha.js`: aquele mede o caderno ABRINDO
      (erro de JS, figura quebrada); este mede o caderno FECHANDO. Os dois na
      banca, porque medem coisas diferentes.

   Uso:  node _qa/joga_folha.js <pasta> [porta]
   Código 0 = fechou tudo · 1 = item que não fecha · 2 = não deu para medir
   ============================================================ */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + ').');
  process.exit(2);
}
const { spawn } = require('child_process');
const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const pasta = (process.argv[2] || '').replace(/\/$/, '');
const porta = parseInt(process.argv[3] || '8793', 10);
if (!pasta) { console.log('uso: node _qa/joga_folha.js <pasta> [porta]'); process.exit(2); }

/* ⚠️ O TEMPO DE ESPERA É PALPITE DECLARADO, nunca cronometrado com crianca:
   as folhas chamam `acertou()` dentro de um `setTimeout` de 240 a 850 ms (o
   tempinho em que a peca pisca antes de fechar). 1400 ms cobre o maior deles
   com folga; abaixo disso o jogador acusaria "nao fechou" o que so estava
   piscando — portao que reprova por causa do proprio relogio.

   ⚡ ELE E O TETO, NAO A ESPERA (14/set/2026, ordem do Marcos: "esses portoes
   precisam ser mais rapidos"). Antes o jogador PARAVA 1400 ms em CADA item,
   mesmo quando a folha ja tinha fechado em 300 — e o item nao fecha mais cedo
   por isso, so o portao fica mais lento. Medido: a banca da folha viva inteira
   levava 198 s e 193 deles eram este arquivo (102 itens x 1,4 s parado). Agora
   ele PERGUNTA a pagina se fechou, de 60 em 60 ms, e segue no instante em que
   fechar; os 1400 ms continuam sendo o teto, entao um item que de fato nao
   fecha espera o mesmo de antes e reprova igual. O portao mede o mesmo — so
   deixou de esperar o que ja aconteceu. */
const ESPERA_FECHA = 1400;
const PULSO = 60;

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(porta)], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 900));
  const b = await chromium.launch({ executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu'] });
  let ruim = 0, naoResolvi = 0;
  try {
    const pg = await b.newPage({ viewport: { width: 1024, height: 1200 } });
    const erros = [];
    pg.on('pageerror', e => erros.push(String(e).slice(0, 160)));
    await pg.goto(`http://localhost:${porta}/${pasta}/index.html`, { waitUntil: 'load' });
    await pg.waitForTimeout(600);
    await pg.fill('#nomeIn', 'Ana').catch(() => {});
    await pg.click('#bComecar').catch(() => {});
    await pg.waitForTimeout(500);

    const total = await pg.evaluate(() => (typeof PAGEL !== 'undefined' ? PAGEL.length - 1 : 0));
    if (!total) {
      console.log(`${pasta} -> NAO MEDI: nao achei PAGEL (nao e caderno de folha viva?).`);
      await b.close(); srv.kill(); process.exit(2);
    }
    console.log(`${pasta} -> o jogador vai resolver ${total} folha(s), item por item`);

    const relato = [];
    for (let pi = 1; pi <= total; pi++) {
      await pg.evaluate(k => { vaiPara(k); window.scrollTo(0, 0); }, pi);
      await pg.waitForTimeout(320);

      const nome = await pg.evaluate(k => (typeof NOMES !== 'undefined' && NOMES[k - 1]) || '', pi);
      const ids = await pg.evaluate(k => idsDaPagina(k), pi);
      let fechados = 0, semJeito = 0;
      const presos = [];

      for (const id of ids) {
        const jaEstava = await pg.evaluate(x => !!ST.resp[x], id);
        if (jaEstava) { fechados++; continue; }

        const plano = await pg.evaluate(montaPlano, id);
        if (!plano || plano.tipo === 'nao-sei') { semJeito++; continue; }
        await executa(pg, id, plano);
        const fechou = await pg.waitForFunction(
          x => !!ST.resp[x], id, { timeout: ESPERA_FECHA, polling: PULSO })
          .then(() => true).catch(() => false);
        /* ⚠️⚠️ ESTA LINHA E O PRECO DE TER FICADO RAPIDO, e ela custou duas
           rodadas para aparecer. A espera de 1400 ms fazia DUAS coisas: dava
           tempo do item fechar E separava um item do seguinte. Tirando a
           primeira, a segunda foi junto sem eu perceber — o jogador passou a
           clicar no item seguinte com o TECLADO do anterior ainda aberto, e
           reprovava itens de digitar que estavam certos. O sinal era claro e
           eu quase o li errado: os itens acusados MUDAVAM a cada rodada, e
           defeito que muda de lugar nao e defeito da atividade, e do portao.
           Entao agora ele espera a coisa certa, nao um relogio: o teclado ter
           fechado (`ATIVA` vazio) antes de tocar no proximo item. */
        await pg.waitForFunction(
          () => typeof ATIVA === 'undefined' || !ATIVA, null,
          { timeout: 900, polling: PULSO }).catch(() => {});
        if (fechou) { fechados++; continue; }
        /* ⚠️ ISTO AQUI É A LIÇÃO MAIS CARA DESTE ARQUIVO, e ela é de método:
           na primeira varredura o jogador REPROVOU três cadernos, e em DOIS
           deles ele estava errado — a folha do `_fra1` marca as palavras numa
           bolinha e confirma no botão "pronto"; a do `_alfa1` pega uma peça
           e depois solta no alvo. Ele não conhecia nenhuma das duas, mas achou
           um botão parecido, chutou um plano, e chamou de defeito o que era
           ignorância dele. Portão que acusa inocente é portão que se aprende a
           ignorar. Agora só REPROVA o que ele entendeu de verdade; o resto sai
           como dívida, que é o que é. */
        if (plano.fe === 'baixa') { semJeito++; continue; }
        presos.push(id + (plano.tipo !== 'clique' ? ' [' + plano.tipo + ']' : ''));
      }
      relato.push({ pi, nome, tem: ids.length, fechados, semJeito, presos });
    }

    for (const r of relato) {
      if (r.semJeito) {
        naoResolvi++;
        console.log(`   ?  folha ${r.pi} (${r.nome}): NAO RESOLVI ${r.semJeito} de ${r.tem}`
                    + ` — o jogador nao conhece a peca (isto nao e "passou")`);
      } else if (r.presos.length) {
        ruim = 1;
        console.log(`   X  folha ${r.pi} (${r.nome}): ${r.presos.length} de ${r.tem} NAO FECHARAM`
                    + ` com a resposta declarada certa`);
        console.log(`        ${r.presos.slice(0, 6).join(', ')}`);
      } else {
        console.log(`   ok folha ${r.pi} (${r.nome}): ${r.fechados} de ${r.tem}`);
      }
    }

    if (erros.length) {
      ruim = 1;
      console.log(`   ERRO DE JS ENQUANTO JOGAVA (${erros.length}):`);
      [...new Set(erros)].slice(0, 5).forEach(e => console.log('    - ' + e));
    }

    /* ⭐ O FECHO: com tudo respondido, o boletim tem que abrir. É o que a
       criança recebe no fim, e é o que o "andar_folha" nunca chegou a ver
       porque ele nunca respondia nada. */
    await pg.evaluate(() => { if (typeof fim === 'function') fim(); }).catch(() => {});
    await pg.waitForTimeout(900);
    const fecho = await pg.evaluate(() =>
      document.body.innerText.indexOf('boletim') > -1 ||
      document.body.innerText.indexOf('Boletim') > -1 ||
      !!document.querySelector('.estrelas,.barras,#relat'));
    if (!fecho) { ruim = 1; console.log('   X  o FECHO nao abriu depois de tudo respondido'); }
    else console.log('   ok o fecho abriu com o caderno resolvido');

  } catch (e) {
    console.log('NAO MEDI: ' + String(e).slice(0, 200));
    await b.close(); srv.kill(); process.exit(2);
  }
  await b.close(); srv.kill();

  if (ruim) {
    console.log('   REPROVADO: existe item que NAO FECHA nem com a resposta certa.');
    console.log('   conserto: seguir o caminho do `acertou(id, ...)` daquela folha —');
    console.log('   ou o clique nao chega na peca, ou a condicao de fechar nunca da.');
    process.exit(1);
  }
  if (naoResolvi) {
    console.log(`   NAO MEDI POR INTEIRO: ${naoResolvi} folha(s) o jogador nao sabe jogar.`);
    console.log('   conserto: ensinar a peca a ele (uma familia nova em `montaPlano`),');
    console.log('   no mesmo commit da folha. Ate la isto e divida, nao aprovacao.');
    process.exit(2);
  }
  console.log('   ok: todo item fecha com a resposta declarada, e o fecho abre');
  process.exit(0);
})();

/* ---------------------------------------------------------------
   MONTA O PLANO DE UM ITEM — roda DENTRO do navegador.
   Devolve {tipo, alvos[]} ou {tipo:'nao-sei'}.
   --------------------------------------------------------------- */
function montaPlano(id) {
  const R = (typeof RESP !== 'undefined' && RESP[id]) || null;
  if (!R) return { tipo: 'nao-sei' };
  const certo = String(R.certo == null ? '' : R.certo);
  const pag = document.querySelector('.pagina.viva') || document;
  const qa = [].slice.call(pag.querySelectorAll('[data-qa]'));

  /* o teclado: a folha de DIGITAR publica `esc-<id>` no quadro vazio */
  const cxEsc = qa.filter(e => e.getAttribute('data-qa') === 'esc-' + id)[0];
  if (cxEsc) return { tipo: 'digitar', alvo: 'esc-' + id, texto: certo, fe: 'alta' };

  /* o canvas: a folha de TRAÇAR publica `traca-<id>` */
  const cv = qa.filter(e => e.getAttribute('data-qa') === 'traca-' + id)[0];
  if (cv) return { tipo: 'tracar', alvo: 'traca-' + id, fe: 'alta' };

  /* LIGAR: o id é `l<pi><tag>_<k>` e as pontas são `lig<tag>-e-<k>` / `-d-<k>`
     ⚠️ A ETIQUETA É MÍNIMA, A CHAVE É O RESTO — e isto custou uma volta inteira
        (14/set/2026, cinco reinos). Com `(.+)` guloso na etiqueta, o id
        `l14a0_reino_fungi` era lido como etiqueta "a0_reino" e chave "fungi":
        o jogador procurava uma ponta que não existe e saía dizendo "não conheço
        a peça". Só quebrava quando a chave da figura TEM sublinhado — que é o
        caso de `reino_fungi`, `reino_monera`, `urso_pelucia`… Régua errada, e a
        folha estava certa. */
  const mLig = id.match(/^l\d+(.+?)_(.+)$/);
  if (mLig) {
    const e = 'lig' + mLig[1] + '-e-' + mLig[2], d = 'lig' + mLig[1] + '-d-' + mLig[2];
    if (qa.some(x => x.getAttribute('data-qa') === e) &&
        qa.some(x => x.getAttribute('data-qa') === d)) {
      return { tipo: 'ligar', alvos: [e, d], fe: 'alta' };
    }
  }

  /* ⭐ A FAMÍLIA "GAVETA" (arrastar para a caixa certa) — declarada, não
     deduzida. A folha registra a resposta como `p0>vivo p1>nao ...`: qual peça
     vai em qual gaveta. O gesto tem DOIS toques (pega a peça, solta na gaveta),
     e era exatamente por não conhecer isso que o jogador saía dizendo "NAO
     RESOLVI" em quatro folhas seguidas dos cinco reinos. */
  if (/^p\d+>/.test(certo)) {
    const alvos = [];
    let inteiro = true;
    for (const par of certo.split(/\s+/)) {
      const m = par.match(/^(p\d+)>(.+)$/);
      if (!m) { inteiro = false; break; }
      const pe = 'peca-' + id + '-' + m[1], gv = 'gav-' + id + '-' + m[2];
      if (!qa.some(x => x.getAttribute('data-qa') === pe) ||
          !qa.some(x => x.getAttribute('data-qa') === gv)) { inteiro = false; break; }
      alvos.push(pe, gv);
    }
    if (inteiro && alvos.length) return { tipo: 'clique', alvos: alvos, fe: 'alta' };
    return { tipo: 'nao-sei' };
  }

  /* ⭐ A FAMÍLIA "PINTAR POR LEGENDA" — também de dois toques: primeiro a
     CANETINHA do estojo, depois a figura. O alvo diz qual cor ele pede, em
     `data-lapis`, e o estojo publica `lapis-<cor>`. Sem isso o jogador pintava
     tudo com a primeira cor e acusava a folha de não fechar. */
  const pinta = qa.filter(e => {
    const v = e.getAttribute('data-qa') || '';
    return v.indexOf('pinta-' + id + '-') === 0 && e.getAttribute('data-lapis');
  })[0];
  if (pinta) {
    const cor = 'lapis-' + pinta.getAttribute('data-lapis');
    if (qa.some(x => x.getAttribute('data-qa') === cor))
      return { tipo: 'clique', alvos: [cor, pinta.getAttribute('data-qa')], fe: 'alta' };
    return { tipo: 'nao-sei' };
  }

  /* ⭐ A FAMÍLIA "MARQUE E CONFIRME" — a folha não fecha no clique da peça, e sim
     num botão de confirmar no fim ("Pronto", "Conferir"). Eu não sabia disto e
     por causa disso acusei o `_fra1` de ter uma folha quebrada: ele pinta uma
     bolinha por palavra e só depois confirma. Clicar a bolinha e esperar o item
     fechar era eu não conhecer a peça.
     ⚠️ Quando a resposta é um NÚMERO, ela não é o nome de um alvo: é QUANTAS.
        As bolinhas pintam da esquerda para a direita, então tocar a de índice
        N-1 deixa N pintadas. */
  const fecha = qa.filter(e => {
    const v = e.getAttribute('data-qa') || '';
    return v === 'pronto-' + id || v === 'conferir-' + id;
  })[0];
  if (fecha && /^\d+$/.test(certo)) {
    const n = parseInt(certo, 10);
    const bol = qa.filter(e => {
      const v = (e.getAttribute('data-qa') || '');
      return v.indexOf(id) > -1 && v.slice(-('-' + (n - 1)).length) === '-' + (n - 1);
    })[0];
    if (bol) return { tipo: 'clique', fe: 'alta',
                      alvos: [bol.getAttribute('data-qa'), fecha.getAttribute('data-qa')] };
    return { tipo: 'nao-sei' };
  }

  /* ⚠️ OS PEDAÇOS DA RESPOSTA, e a ambiguidade que precisou de MEDIDA e não de
     palpite: "ABCD" pode ser quatro letras para tocar em ordem (folha 14) ou
     uma palavra só para circular (folha 16, "ZEBRA"). Eu não decido pelo
     formato do texto — eu OLHO se existe um botão inteiro com aquele nome.
     Se existe, é um pedaço só; se não existe, tento quebrar em letras. */
  let pedacos = certo.indexOf(' ') > -1 ? certo.split(/\s+/) : [certo];
  pedacos = pedacos.map(p => (p.indexOf('=') > -1 ? p.split('=')[0] : p)).filter(Boolean);

  function acha(tok, usados) {
    /* ⚠️ A COMPARAÇÃO É SEM CAIXA, MAS O QUE VOLTA É O VALOR ORIGINAL — e isto
       foi o primeiro defeito deste arquivo, na primeira hora de vida dele.
       Eu devolvia o `data-qa` já em minúsculas, e depois procurava por ele com
       `querySelector('[data-qa="op-a7_0-b"]')` — que não casa com o atributo de
       verdade, `op-a7_0-B`. Resultado: o jogador reprovou DEZESSEIS folhas
       dizendo que a resposta certa não fecha, quando o que não fechava era o
       meu seletor. É a lição do halo outra vez: quando o portão reprova em
       massa, a primeira suspeita é a régua, não a peça. */
    const alvo = '-' + String(tok).toLowerCase();
    for (const e of qa) {
      const orig = e.getAttribute('data-qa') || '';
      const v = orig.toLowerCase();
      if (usados.indexOf(orig) > -1) continue;
      if (v.slice(-alvo.length) !== alvo) continue;
      /* o alvo tem que ser DESTA folha: ou traz o id, ou é peça compartilhada
         (a tira do alfabeto da folha 2, que serve a todas as perguntas) */
      if (v.indexOf(id.toLowerCase()) > -1 || v.split('-').length === 2) return orig;
    }
    return null;
  }

  const usados = [], alvos = [];
  for (const p of pedacos) {
    const achou = acha(p, usados);
    if (achou) { usados.push(achou); alvos.push(achou); continue; }
    /* não há botão com o pedaço inteiro: então ele é uma FILA de letras */
    let ok = true;
    const parciais = [];
    for (const ch of String(p).split('')) {
      const a = acha(ch, usados.concat(parciais));
      if (!a) { ok = false; break; }
      parciais.push(a);
    }
    if (!ok) {
      /* último caso: um alvo só, que carrega o id (o mural) */
      const so = qa.filter(e => (e.getAttribute('data-qa') || '').indexOf(id) > -1);
      if (so.length === 1) return { tipo: 'clique', alvos: [so[0].getAttribute('data-qa')], fe: 'baixa' };
      return { tipo: 'nao-sei' };
    }
    parciais.forEach(a => { usados.push(a); alvos.push(a); });
  }
  if (!alvos.length) return { tipo: 'nao-sei' };
  /* ⚠️ CONFIANÇA ALTA só quando TODO alvo carrega o id do item. Quando um deles
     veio de peça compartilhada (a tira do alfabeto) ou do último recurso, o
     plano pode estar simplesmente errado — e aí um item que não fecha é
     ignorância minha, não defeito da folha. */
  const forte = alvos.every(a => a.toLowerCase().indexOf(id.toLowerCase()) > -1);
  if (fecha) alvos.push(fecha.getAttribute('data-qa'));
  return { tipo: 'clique', alvos: alvos, fe: forte ? 'alta' : 'baixa' };
}

/* --------------------------------------------------------------- */
async function executa(pg, id, plano) {
  if (plano.tipo === 'clique' || plano.tipo === 'ligar') {
    for (const qa of plano.alvos) {
      await pg.evaluate(v => {
        const e = document.querySelector('[data-qa="' + v + '"]');
        if (!e) return;
        e.scrollIntoView({ block: 'center' });
        /* ⚠️ as peças de LIGAR e de arrastar ouvem `pointerdown`, não `click` —
           disparar só o click não faz nada nelas e o jogador acusaria inocente.
           Então vai o par: pointerdown e depois click. */
        e.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true }));
        if (typeof e.click === 'function') e.click();
      }, qa);
      await pg.waitForTimeout(220);
    }
    return;
  }
  if (plano.tipo === 'digitar') {
    await pg.evaluate(v => {
      const e = document.querySelector('[data-qa="' + v + '"]');
      if (e) { e.scrollIntoView({ block: 'center' }); e.click(); }
    }, plano.alvo);
    await pg.waitForTimeout(260);
    /* as DUAS portas: aqui vai pelo teclado DE VERDADE, que é o que o PC da
       escola tem — se só o teclado da tela funcionasse, isto reprovaria */
    for (const ch of plano.texto.split('')) { await pg.keyboard.press(ch); await pg.waitForTimeout(90); }
    /* ⚠️⚠️ O ENTER SO VAI SE A FOLHA NAO TIVER CONFIRMADO SOZINHA, e esta linha
       custou tres rodadas. O teclado do caderno confere sozinho 380 ms depois
       que o numero fica do tamanho da resposta (`if(ATIVA.val.length >=
       ATIVA.certa.length) setTimeout(confereNum, 380)`). Bater Enter por cima
       disso manda conferir DUAS vezes, e a segunda pega o campo ja limpo: o
       item nao fecha. Antes isso nao aparecia porque o jogador parava 1400 ms
       em cada item e a corrida se acomodava sozinha — o defeito estava ali o
       tempo todo, escondido pela lentidao.
       ⚠️ As DUAS PORTAS continuam medidas: os digitos vao pelo teclado DE
          VERDADE, que e o que o PC da escola tem. O Enter so entra quando a
          folha espera por ele. */
    const jaFechou = await pg.waitForFunction(
      x => !!ST.resp[x], id, { timeout: 700, polling: 60 })
      .then(() => true).catch(() => false);
    if (!jaFechou) await pg.keyboard.press('Enter');
    return;
  }
  if (plano.tipo === 'tracar') {
    /* varre o quadro em serpentina, como o dedo de uma criança rabiscando por
       cima da letra — não é "resolver", é cobrir, que é o que a folha pede */
    const cx = await pg.evaluate(v => {
      const e = document.querySelector('[data-qa="' + v + '"]');
      if (!e) return null;
      e.scrollIntoView({ block: 'center' });
      const r = e.getBoundingClientRect();
      return { x: r.left, y: r.top, w: r.width, h: r.height };
    }, plano.alvo);
    if (!cx) return;
    await pg.mouse.move(cx.x + 8, cx.y + 8);
    await pg.mouse.down();
    const linhas = 22;
    for (let i = 0; i < linhas; i++) {
      const y = cx.y + 6 + (cx.h - 12) * i / (linhas - 1);
      const ida = i % 2 === 0;
      for (let k = 0; k <= 12; k++) {
        const t = ida ? k / 12 : 1 - k / 12;
        await pg.mouse.move(cx.x + 6 + (cx.w - 12) * t, y);
      }
    }
    await pg.mouse.up();
  }
}
