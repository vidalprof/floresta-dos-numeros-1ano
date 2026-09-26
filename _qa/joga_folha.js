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
        if (plano.tipo === 'sem-opcao') {
          presos.push(id + ' [a resposta declarada «' + plano.certo + '» nao esta '
                      + 'entre as ' + plano.tinha + ' opcoes da tela]');
          continue;
        }
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

  /* ⭐ BATER PALMA: a folha de CONTAR SÍLABAS publica `bater-<id>` e
     `pronto-<id>`, e a resposta declarada é um NÚMERO (quantas sílabas).
     ⚠️ SEM ISTO O JOGADOR REPROVAVA UMA FOLHA BOA — medido em 17/set/2026,
        `_alfa1` folha 3 ("Quantas sílabas?"): 11 de 11 "não fecharam". A folha
        estava certa; a régua é que não conhecia a peça, e o pior é que ela não
        dizia "não medi" — dizia REPROVADO. Régua que acusa o que não entende é
        pior que régua que se cala, porque manda consertar o que não está
        quebrado. É a mesma lição da fileira de letras (16/set): a peça estava
        certa, a régua era larga demais. */
  const bat = qa.filter(e => e.getAttribute('data-qa') === 'bater-' + id)[0];
  const prt = qa.filter(e => e.getAttribute('data-qa') === 'pronto-' + id)[0];
  if (bat && prt) {
    const quantas = parseInt(certo, 10);
    if (quantas > 0 && quantas < 12)
      return { tipo: 'palmas', alvo: 'bater-' + id, fecha: 'pronto-' + id,
               vezes: quantas, fe: 'alta' };
  }

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
  /* ⚠️ DUAS FORMAS, e a ordem importa. Desde 20/set/2026 o motor publica o
     NÚMERO DA FOLHA no data-qa (`lig<pi><tag>-e-<k>`), porque sem ele duas
     folhas de LIGAR no mesmo html publicavam a mesma etiqueta e o clique ia
     sempre para a primeira — a segunda não fechava nem com a resposta certa.
     A forma ANTIGA (`lig<tag>-e-<k>`) continua aceita: os cadernos que já
     estão no ar foram montados com ela, e um portão que passa a reprovar o
     que está publicado e correto não mede nada, só atrapalha. */
  const mLig = id.match(/^l(\d+)(.+?)_(.+)$/);
  if (mLig) {
    const formas = [['lig' + mLig[1] + mLig[2] + '-e-' + mLig[3], 'lig' + mLig[1] + mLig[2] + '-d-' + mLig[3]],
                    ['lig' + mLig[2] + '-e-' + mLig[3], 'lig' + mLig[2] + '-d-' + mLig[3]]];
    const achou = formas.find(([e, d]) =>
      qa.some(x => x.getAttribute('data-qa') === e) &&
      qa.some(x => x.getAttribute('data-qa') === d));
    if (achou) {
      const [e, d] = achou;
      return { tipo: 'ligar', alvos: [e, d], fe: 'alta' };
    }
  }

  /* ⭐ A FAMÍLIA "CORTAR A FRASE GRUDADA" (19/set/2026, com O Caderno do
     Juquinha; a peça nasceu n'A Tecla do Espaço Quebrou, do 1º ano).
     A folha mostra a frase SEM espaços, letra por letra, e a criança toca na
     letra que COMEÇA cada palavra nova. Cada letra publica `lfr-<id>-<k>`, e a
     resposta declarada é a frase COM os espaços — então dá para calcular
     exatamente em quais letras tocar, do mesmo jeito que o `cortesDe()` do
     caderno faz. Sem esta família o jogador dizia "não conheço a peça" em DEZ
     folhas de 35, e isso não é "passou": é metade do caderno sem medição.
     ⚠️ E ele tem de tocar SÓ nas letras certas: tocar numa errada conta como
        erro na folha, e o relatório do professor sairia sujo por culpa da
        régua. */
  const temLfr = qa.some(e => (e.getAttribute('data-qa') || '').indexOf('lfr-' + id + '-') === 0);
  if (temLfr && certo.indexOf(' ') > -1) {
    const ps = certo.split(' ');
    const alvos = [];
    let n = 0;
    for (let i = 0; i < ps.length - 1; i++) {
      n += ps[i].length;
      alvos.push('lfr-' + id + '-' + n);
    }
    if (alvos.every(a => qa.some(e => e.getAttribute('data-qa') === a)))
      return { tipo: 'clique', alvos: alvos, fe: 'alta' };
  }

  /* ⭐ A FAMÍLIA "DOIS TOQUES COM ALVO COMPARTILHADO" (15/set/2026).
     Existe folha em que a criança PEGA uma coisa e SOLTA em outra, e em que uma
     das duas é COMPARTILHADA pela folha inteira: a gaveta que recebe seis
     palavras, a fila de posições da receita, o quadro de palavras que serve as
     seis frases. Nessas o alvo NÃO pode carregar o id do item (ele é um só para
     todos), e por isso a família "gaveta" de cima não alcança — o jogador saía
     dizendo "não conheço a peça" em cinco folhas seguidas do caderno de
     ortografia.
     O contrato: o alvo se declara no nível da PÁGINA, como `alvo-<chave>`, e a
     chave TEM DE SER ÚNICA NO DOCUMENTO INTEIRO — as folhas moram todas no
     mesmo HTML ao mesmo tempo, só uma fica visível, e o `executa` busca o alvo
     com `document.querySelector`. Duas folhas com `alvo-gav_s` fazem o jogador
     clicar sempre na primeira do documento (medido: três itens da folha 5
     "não fechavam" por causa da gaveta homônima da folha 4). O jeito simples é
     pôr o número da folha no nome: `alvo-gav5_s`. E a
     resposta do item diz a chave E A ORDEM dos dois toques:
         ">chave"  = toca no item e depois no alvo   (a peça é o item)
         "<chave"  = toca no alvo e depois no item   (a peça é o alvo)
     A ordem importa de verdade: nessas folhas o primeiro toque MARCA e o
     segundo SOLTA; invertido, o app só diz "toque primeiro na palavra". */
  /* ⭐ A FAMÍLIA "SEQUÊNCIA DECLARADA" (26/set/2026, `_divh4` — a mesa do
     MATERIAL DOURADO). A peça tem vários gestos de tipos diferentes no mesmo
     item: levar placas, barras e cubinhos para os grupos e, no meio, TROCAR uma
     barra por dez cubinhos (os cubinhos novos só nascem depois da troca). Não
     há como o jogador deduzir essa ordem — então a folha a DECLARA:
         certo = "seq:<data-qa> <data-qa> …"
     e o jogador toca um a um, na ordem. O `executa` busca cada alvo NA HORA do
     clique, então o que ainda não existe quando o plano é montado (os cubinhos
     da troca) é achado quando chega a vez dele. */
  if (certo.indexOf('seq:') === 0) {
    const alvos = certo.slice(4).split(/\s+/).filter(Boolean);
    if (alvos.length && qa.some(x => x.getAttribute('data-qa') === alvos[0]))
      return { tipo: 'clique', alvos: alvos, fe: 'alta' };
    return { tipo: 'nao-sei' };
  }

  const mDois = certo.match(/^([<>])(\S+)$/);
  if (mDois) {
    const alv = 'alvo-' + mDois[2], iti = 'item-' + id;
    if (qa.some(x => x.getAttribute('data-qa') === alv) &&
        qa.some(x => x.getAttribute('data-qa') === iti))
      return { tipo: 'clique', fe: 'alta',
               alvos: mDois[1] === '>' ? [iti, alv] : [alv, iti] };
    return { tipo: 'nao-sei' };
  }

  /* ⭐ A FAMÍLIA "REPARTE" (24/set/2026, `_div3` — a bancada de potes). A peça
     não tem UM toque: a criança distribui N peças em K potes, `cada` em cada
     pote, e o item só fecha quando a última peça cai. O jogador dizia "não
     fecha nem com a resposta certa" em SEIS folhas do caderno da divisão — e a
     peça estava certa; quem não sabia jogar era ele.
     O contrato:
       · a resposta declarada é `rep:<potes>x<cada>`;
       · cada peça publica `item-<id>-<n>`, n de 0 a potes*cada - 1;
       · cada pote publica `pote-<id>-<j>`, j de 0 a potes - 1.
     ⚠️ E O POTE PODE AINDA NÃO EXISTIR na hora de montar o plano: na divisão
        por MEDIDA ele nasce quando o anterior enche (senão contar os potes
        daria a resposta de graça). Por isso esta família NÃO exige que os
        potes estejam no documento — exige a primeira peça e o primeiro pote, e
        o resto vem pelo nome. Dá certo porque o `executa` busca cada alvo com
        `querySelector` NA HORA do clique, não no plano. */
  const mRep = certo.match(/^rep:(\d+)x(\d+)$/);
  if (mRep) {
    const potes = parseInt(mRep[1], 10), cada = parseInt(mRep[2], 10);
    const temPeca = qa.some(x => x.getAttribute('data-qa') === 'item-' + id + '-0');
    const temPote = qa.some(x => x.getAttribute('data-qa') === 'pote-' + id + '-0');
    if (potes > 0 && cada > 0 && temPeca && temPote) {
      const alvos = [];
      let n = 0;
      for (let j = 0; j < potes; j++)
        for (let t = 0; t < cada; t++) alvos.push('item-' + id + '-' + (n++), 'pote-' + id + '-' + j);
      return { tipo: 'clique', alvos: alvos, fe: 'alta' };
    }
    return { tipo: 'nao-sei' };
  }

  /* ⭐ A FAMÍLIA "MEMÓRIA" (20/set/2026, `_corpo5` folha 37). O par publica as
     duas cartas com o ID DO ITEM dentro do `data-qa` (`mem-<id>-fig` e
     `mem-<id>-nome`), e não a posição na grade — é isso que permite ao jogador
     saber QUAIS duas cartas formam o par sem adivinhar pela ordem.
     ⚠️ Sem esta família o jogador dizia "não conheço a peça" e a folha ficava
        como dívida — e dívida numa folha boa é o mesmo que reprovar sem
        motivo (lição paga no `_alfa1`, 17/set). */
  if (qa.some(e => (e.getAttribute('data-qa') || '').indexOf('mem-' + id + '-') === 0)) {
    /* o ITEM é o tabuleiro inteiro; a resposta declarada lista as chaves dos
       pares, separadas por espaço. Para cada chave, as duas cartas. */
    /* ⚠️ OS DOIS LADOS NÃO SE CHAMAM SEMPRE `fig` E `nome` (24/set/2026): no
       caderno da divisão a memória casa a CONTA com o RESULTADO, e os lados
       são `conta` e `res`. O portão exigia os dois nomes de sempre e dizia
       "não conheço a peça" numa folha correta — dívida numa folha boa é o
       mesmo que reprovar sem motivo. Agora os lados saem do PRÓPRIO
       documento: para cada chave, as duas cartas que a carregam. */
    const alvos = [];
    for (const k of certo.split(/\s+/)) {
      const pref = 'mem-' + id + '-' + k + '-';
      const lados = qa.map(e => e.getAttribute('data-qa') || '')
                      .filter(v => v.indexOf(pref) === 0);
      if (lados.length === 2) alvos.push(lados[0], lados[1]);
    }
    if (alvos.length) return { tipo: 'clique', alvos: alvos, espera: 1300, fe: 'alta' };
  }

  /* ⭐ A FAMÍLIA "FORCA" (20/set/2026, `_corpo5` folha 38): a resposta declarada
     é a PALAVRA, e o teclado publica uma tecla por letra (`tf-<id>-<LETRA>`).
     O jogador toca nas letras DISTINTAS da palavra, na ordem em que aparecem —
     que é o caminho de quem já sabe a resposta. */
  if (/^[A-ZÀ-Ü]{3,}$/.test(certo) &&
      qa.some(e => (e.getAttribute('data-qa') || '').indexOf('tf-' + id + '-') === 0)) {
    const letras = [], vistas = {};
    for (const L of certo.split('')) {
      if (vistas[L]) continue;
      vistas[L] = 1;
      if (qa.some(e => e.getAttribute('data-qa') === 'tf-' + id + '-' + L))
        letras.push('tf-' + id + '-' + L);
    }
    if (letras.length) return { tipo: 'clique', alvos: letras, fe: 'alta' };
  }

  /* ⭐ A FAMÍLIA "SIMULADOR" (20/set/2026, `_corpo5` folha 39): a resposta É o
     gesto — a criança arrasta um controle até a posição pedida e o item fecha
     sozinho, sem botão de confirmar. O controle publica `sim-<id>` e a
     resposta declarada é a CHAVE do passo (`baixo`/`cima`), que o próprio
     `SIMU` traduz em valor.
     ⚠️ Não basta escrever o `value`: um `input[type=range]` só avisa a página
        pelo evento `input`. Sem disparar o evento, o jogador mexeria no
        controle sem que nada na tela soubesse — e acusaria a folha de não
        fechar. */
  const sl = qa.filter(e => e.getAttribute('data-qa') === 'sim-' + id)[0];
  if (sl && sl.getAttribute('data-vai') != null)
    return { tipo: 'simular', alvo: 'sim-' + id,
             valor: parseInt(sl.getAttribute('data-vai'), 10), fe: 'alta' };

  /* ⭐ A FAMÍLIA "CAÇA-PALAVRAS" (15/set/2026): a palavra se acha tocando na
     PRIMEIRA e na ÚLTIMA letra dela na grade. As duas pontas se declaram como
     `cp-<id>-a` e `cp-<id>-z`. Quando a folha não as publica (duas palavras
     cruzando exatamente numa ponta), o jogador diz "não sei" — dívida honesta,
     em vez de acusar de defeito uma folha boa. */
  const cpA = qa.filter(e => e.getAttribute('data-qa') === 'cp-' + id + '-a')[0];
  const cpZ = qa.filter(e => e.getAttribute('data-qa') === 'cp-' + id + '-z')[0];
  if (cpA && cpZ)
    return { tipo: 'clique', alvos: ['cp-' + id + '-a', 'cp-' + id + '-z'], fe: 'alta' };

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

  /* ⭐⭐ A RESPOSTA CERTA NÃO ESTÁ ENTRE AS OPÇÕES (24/set/2026, `_div3` folha
     14). O item desenha um leque de opções (`op-<id>-<v>`) e a resposta
     declarada NÃO É NENHUMA DELAS: a criança não tem como acertar, por mais
     que leia. Foi o que aconteceu com *"48 bolinhos, 2 em cada caixa"* — a
     resposta é 24 e o leque ia de 1 a 12.
     ⚠️ E ISTO TINHA DE DEIXAR DE SER DÍVIDA: o jogador saía com "não conheço a
        peça" (código 2, "não medi"), que é o mesmo recado que ele dá para uma
        peça nova e correta. Um item impossível não é ignorância da régua — é
        defeito da atividade, e reprova.
     Só vale quando há LEQUE e a resposta é um pedaço SÓ: as folhas de marcar
     vários publicam `op-` em cada peça certa e a resposta é uma lista. */
  if (certo.indexOf(' ') === -1) {
    const leque = qa.map(e => e.getAttribute('data-qa') || '')
                    .filter(v => v.indexOf('op-' + id + '-') === 0);
    if (leque.length > 1 &&
        !leque.some(v => v.toLowerCase() === ('op-' + id + '-' + certo).toLowerCase()))
      return { tipo: 'sem-opcao', certo: certo, tinha: leque.length };
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
    /* ⚠️⚠️ QUANDO DUAS PEÇAS TERMINAM IGUAL, A CERTA VEM PRIMEIRO (15/set/2026).
       Uma folha publicou `op-<id>-s0` na letra certa e `no-<id>-s0` nas erradas;
       eu acho a peça pelo FINAL do nome, peguei a errada e reprovei uma folha
       que estava boa. O nome da folha foi consertado — mas a régua tinha de
       ficar firme também, porque o próximo caderno vai repetir o nome. Duas
       passadas: primeiro só o que começa com `op-`, depois qualquer um. */
    for (const prefiro of [true, false]) {
      for (const e of qa) {
        const orig = e.getAttribute('data-qa') || '';
        const v = orig.toLowerCase();
        if (usados.indexOf(orig) > -1) continue;
        if (prefiro && v.indexOf('op-') !== 0) continue;
        if (v.slice(-alvo.length) !== alvo) continue;
        /* o alvo tem que ser DESTA folha: ou traz o id, ou é peça compartilhada
           (a tira do alfabeto da folha 2, que serve a todas as perguntas) */
        if (v.indexOf(id.toLowerCase()) > -1 || v.split('-').length === 2) return orig;
      }
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
      await pg.waitForTimeout(plano.espera || 220);
    }
    return;
  }
  if (plano.tipo === 'simular') {
    /* arrasta o controle até o valor pedido e AVISA a página (evento `input`) */
    await pg.evaluate(o => {
      const e = document.querySelector('[data-qa="' + o.qa + '"]');
      if (!e) return;
      e.scrollIntoView({ block: 'center' });
      e.value = String(o.v);
      e.dispatchEvent(new Event('input', { bubbles: true }));
      e.dispatchEvent(new Event('change', { bubbles: true }));
    }, { qa: plano.alvo, v: plano.valor });
    await pg.waitForTimeout(320);
    return;
  }
  if (plano.tipo === 'palmas') {
    /* bate uma palma por sílaba e depois confirma — é o gesto da criança */
    for (let n = 0; n < plano.vezes; n++) {
      await pg.evaluate(v => {
        const e = document.querySelector('[data-qa="' + v + '"]');
        if (e) { e.scrollIntoView({ block: 'center' }); e.click(); }
      }, plano.alvo);
      await pg.waitForTimeout(90);
    }
    await pg.waitForTimeout(160);
    await pg.evaluate(v => {
      const e = document.querySelector('[data-qa="' + v + '"]');
      if (e) e.click();
    }, plano.fecha);
    await pg.waitForTimeout(260);
    return;
  }

  if (plano.tipo === 'digitar') {
    /* ⚠️⚠️ CLICAR NA CASINHA, NÃO NA GRADE (18/set/2026). O Marcos viu na sala:
       *"o aluno não conseguia digitar"* na folha 8 d'A Fábrica de Nomes. O
       jogador dizia "4 de 4" porque clicava na GRADE (`data-qa="esc-..."`),
       que tem UM `onclick`; a criança toca na CASINHA, que tem o dela E o da
       grade — `abreCruz` duas vezes, a segunda fechava a primeira e o fecho
       estourava `CRUZ.E` de null. Dez cadernos no ar, e o jogador aprovando.
       Régua que não faz o gesto da criança não mede a criança. */
    await pg.evaluate(v => {
      const g = document.querySelector('[data-qa="' + v + '"]');
      const e = g && (g.querySelector('.ccel, button, [role="button"]') || g);
      if (e) { e.scrollIntoView({ block: 'center' }); e.click(); }
    }, plano.alvo);
    await pg.waitForTimeout(260);
    /* as DUAS portas: aqui vai pelo teclado DE VERDADE, que é o que o PC da
       escola tem — se só o teclado da tela funcionasse, isto reprovaria */
    for (const ch of plano.texto.split('')) {
      /* ⚠️ Ç E VOGAL ACENTUADA NÃO TÊM TECLA no teclado que o navegador de
         teste emula: o Playwright responde "Unknown key: Ç" e a corrida MORRIA
         ali, derrubando a medição do caderno inteiro (15/set/2026, caderno de
         ortografia — onde a metade das palavras tem Ç ou acento). Isto não é
         defeito da atividade: é o teclado de verdade que não tem essa tecla
         sozinha, e é exatamente para isso que existe o teclado DA TELA. Então
         a letra que o teclado real não alcança vai pela outra porta — e as
         duas continuam medidas. */
      const deu = await pg.keyboard.press(ch).then(() => true).catch(() => false);
      /* ⚠️ A OUTRA PORTA MUDOU DE LUGAR em 15/set/2026: o teclado de 41 teclas
         da casa saiu (ordem do Marcos — *"pode remover o teclado das
         atividades, melhor digitar com teclado normal"*) e no lugar dele há
         DUAS peças. A fileira de letras embaralhadas (`.letrabt`) é a que tem
         botão por letra; onde entrou o teclado do APARELHO não há botão
         nenhum, e aí só resta a tecla de verdade — que é o caso do Ç e das
         vogais acentuadas, e por isso esses cadernos guardam o gabarito sem
         acento. Procuro as duas, na ordem. */
      if (!deu) {
        /* ⚠️⚠️ A LETRA TEM DE SAIR DA FILEIRA DESTE ITEM, e não da primeira que
           existir na página — foi assim que eu reprovei uma folha boa
           (16/set/2026, caderno do som nasal). Aquela folha tem CINCO palavras
           com til, cada uma com a sua fileira; eu clicava sempre no `Ã` do
           item 0, e os outros quatro nunca fechavam. A folha estava certa: a
           criança toca na fileira DELA. A régua é que era larga demais. */
        const achou = await pg.evaluate(function(v){
          var alvo = document.querySelector('[data-qa="' + v.alvo + '"]');
          var cx = alvo && alvo.closest ? alvo.closest('.item') : null;
          var lista = (cx || document).querySelectorAll('.letrabt');
          for (var i = 0; i < lista.length; i++) {
            var b = lista[i];
            if (b.getAttribute('aria-label') === 'Letra ' + v.ch &&
                b.className.indexOf('usada') < 0) { b.click(); return true; }
          }
          return false;
        }, { alvo: plano.alvo, ch: ch });
        if (!achou) {
          /* ⚠️⚠️ SEM TECLA E SEM BOTÃO, SOBRA A LETRA SEM ACENTO — e isso não é
             um truque para o portão passar: é o que a CRIANÇA faz. Desde
             15/set/2026 a atividade aceita a palavra com e sem acento (ordem do
             Marcos: *"faça que tanto com o sem dê certo"*), justamente porque o
             teclado de verdade do PC da escola não tem Ç nem vogal acentuada
             numa tecla só. Digitar HABITO onde está escrito HÁBITO é o caminho
             normal, não o caminho de teste. */
          const semAc = { 'Á':'A','À':'A','Â':'A','Ã':'A','Ä':'A','É':'E','È':'E',
            'Ê':'E','Ë':'E','Í':'I','Ì':'I','Î':'I','Ï':'I','Ó':'O','Ò':'O',
            'Ô':'O','Õ':'O','Ö':'O','Ú':'U','Ù':'U','Û':'U','Ü':'U','Ç':'C' }[ch];
          if (semAc) await pg.keyboard.press(semAc).catch(() => {});
        }
      }
      await pg.waitForTimeout(90);
    }
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
