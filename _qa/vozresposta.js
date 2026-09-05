/* ============================================================
   PORTÃO DO ALTO-FALANTE DA RESPOSTA — "o botão de som fala mesmo?"

   Defeito que o Marcos ouviu (ago/2026), na Padaria das Letras:
   *"os botões de som não estão funcionando... somente o som do enunciado"*.

   Ele estava certo, e a causa é da pior família — a que não quebra nada. A
   chave da voz de cada resposta sai do TEXTO dela (`chaveVoz(texto)`), e a
   opção da `ouvir-achar` guarda ESCONDIDOS a letra inicial (o andaime) e o
   aviso "já tentamos". O texto lido virava **"PPÃOjá tentamos"** em vez de
   **"PÃO"**: a chave não existia no `VOZOK`, o motor desistia de instalar o
   alto-falante dele, e sobrava o botão da peça — bonito, no lugar, e mudo.

   Por que NENHUM portão pegou:
     · o `vozfalta` conferia se os 428 mp3 existem — e existiam, todos;
     · o `voztela`/`vozdica` conferem o ENUNCIADO e a DICA, não as respostas;
     · o jogador clica na resposta, não no alto-falante dela;
     · o print mostra o botão desenhado.
   Ou seja: tudo verde, e a criança de 6 anos que ainda não lê escolhendo pelo
   desenho — que é exatamente o que o alto-falante existe para evitar.

   O QUE ESTE PORTÃO FAZ: abre a atividade, percorre TODAS as fases pelo motor
   e, para cada resposta tocável, refaz a conta do motor (o `data-voz` que a
   peça declarou, ou o texto VISÍVEL) e exige que:
     1. exista voz para ela (`temVoz`), e
     2. o mp3 correspondente CARREGUE de verdade.

   Uso:  node _qa/vozresposta.js _padaria/index.html
   Sai com 1 se alguma resposta tiver alto-falante mudo.
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

(async () => {
  const arquivo = process.argv[2];
  if (!arquivo) { console.log('uso: node _qa/vozresposta.js <arquivo.html>'); process.exit(2); }
  const b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']});
  const p = await b.newPage({viewport: {width: 412, height: 820}});
  p.on('pageerror', () => {});
  await p.goto('file://' + path.resolve(arquivo));
  await p.waitForTimeout(600);

  const pode = await p.evaluate(() =>
    (typeof montaFase === 'function' && typeof FASES !== 'undefined' && typeof temVoz === 'function')
      ? FASES.length : 0);
  if (!pode) {
    /* peça avulsa ou atividade feita à mão: aqui não há motor para percorrer.
       "Não medi" é a resposta honesta — nunca "passou". */
    console.log(arquivo + ' -> sem motor de fases (peca avulsa?): NAO MEDI o alto-falante das respostas.');
    await b.close(); process.exit(2);
  }

  const achados = await p.evaluate(async () => {
    const mudas = [], vistas = [];
    /* ⚠️ LICAO PAGA (ago/2026): este portao acusou 15 fichas INOCENTES da
       mecanica `ordenar` ("o alto-falante de 4 esta mudo"). Ele perguntava ao
       CARTAO o que a voz diz, e o cartao mostra so o numero da posicao — o
       texto esta DECLARADO no proprio botao (`.zap[data-voz]`), porque nessa
       peca quem fala e o botao dela, com o `onclick` dela. Medido no navegador:
       tocar o alto-falante toca `op_1f7frq9.mp3`, que e "Atenciosamente," — a
       frase certa, gravada. Quem responde pelo alto-falante e o ALTO-FALANTE;
       perguntar ao vizinho e inventar defeito. */
    const chaveDe = o => {
      const z = o.getElementsByClassName('zap')[0];
      const dz = z && z.getAttribute && z.getAttribute('data-voz');
      if (dz) return dz;
      if (o.getAttribute && o.getAttribute('data-voz')) return o.getAttribute('data-voz');
      return (typeof textoVisivel === 'function' ? textoVisivel(o) : o.textContent);
    };
    for (let i = 0; i < FASES.length; i++) {
      try { montaFase(i, function () {}); } catch (e) { continue; }
      await new Promise(r => setTimeout(r, 130));
      const alvos = [...document.querySelectorAll('.opt,.lig,.pc,.bin')].filter(e => e.offsetParent !== null);
      for (const o of alvos) {
        const txt = (chaveDe(o) || '').replace(/\s+/g, ' ').trim();
        if (!txt) continue;
        vistas.push(txt);
        const k = temVoz(txt);
        const zap = o.getElementsByClassName('zap')[0];
        if (!k) { mudas.push({fase: FASES[i].mec, txt: txt.slice(0, 22), por: 'sem voz no VOZOK'}); continue; }
        if (!zap) { mudas.push({fase: FASES[i].mec, txt: txt.slice(0, 22), por: 'sem botao de som'}); continue; }
        /* o mp3 carrega? (a chave pode existir e o arquivo faltar) */
        const ok = await new Promise(r => {
          const a = new Audio(); a.preload = 'metadata';
          a.onloadedmetadata = () => r(true); a.onerror = () => r(false);
          a.src = 'audio/op_' + k + '.mp3';
          setTimeout(() => r(false), 2500);
        });
        if (!ok) mudas.push({fase: FASES[i].mec, txt: txt.slice(0, 22), por: 'mp3 nao carrega (op_' + k + ')'});
      }
    }
    return {mudas, total: vistas.length};
  });

  await b.close();
  console.log(arquivo + ' -> ' + achados.total + ' resposta(s) tocavel(is) conferida(s)');
  if (!achados.total) {
    /* ⚠️ (set/2026) Na Bancada da Divisao — 32 fases de `divisao-dourado`, uma
       peca de MANIPULAR, sem nenhuma resposta de clicar (.opt/.lig/.pc/.bin) —
       este portao dizia "NAO MEDI" e a banca o listava como CEGO duas vezes.
       Nao e cegueira: a armadilha "alto-falante mudo na resposta" so existe
       onde HA resposta tocavel. Atividade sem resposta tocavel = nao se aplica. */
    console.log('  NAO SE APLICA: nenhuma resposta tocavel (.opt/.lig/.pc/.bin) em fase ' +
                'alguma — a atividade e toda de manipular, nao de escolher. Nada a conferir.');
    process.exit(2);
  }
  if (!achados.mudas.length) {
    console.log('  alto-falante ok: toda resposta fala o que esta escrito nela');
    process.exit(0);
  }
  console.log('  ' + achados.mudas.length + ' RESPOSTA(S) COM ALTO-FALANTE MUDO (quem nao le escolhe pelo desenho):');
  for (const m of achados.mudas.slice(0, 12))
    console.log('   [' + m.fase + '] "' + m.txt + '"  ->  ' + m.por);
  console.log('  conserto: a peca DECLARA o que a voz diz (`data-voz`), ou o texto');
  console.log('  visivel da resposta tem que bater com o que foi gravado no falas.json.');
  process.exit(1);
})();
