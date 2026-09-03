/* ============================================================
   PORTÃO DE BOOT — "a atividade ABRE mesmo?"

   NASCEU DE UM DEFEITO QUE CHEGOU NO MARCOS (03/set/2026).
   Palavras dele: *"clico no tangram e so aparece o fundo, não aparece a
   atividade"*. Eu tinha reescrito o `telaMestre()` e, no caminho, apaguei a
   declaracao `var FASES_MESTRE` — que um IIFE de boot, 400 linhas abaixo,
   ainda usava. Resultado: `Uncaught ReferenceError: FASES_MESTRE is not
   defined` na PRIMEIRA linha executada, o app morria antes de desenhar, e a
   crianca via so o papel de parede.

   POR QUE A BANCA INTEIRA APROVOU MESMO ASSIM — e esta e a licao cara:
     • `node --check` le SINTAXE. `FASES_MESTRE` esta escrito certo; so nao
       EXISTE. Erro de runtime nao e erro de sintaxe. Passou.
     • `_qa/funcoes.py` procura funcao chamada que nao foi declarada. Isto era
       uma VARIAVEL. Passou.
     • os portoes de navegador (leiaute, contraste, jogador) abrem a atividade
       e CHAMAM UMA TELA POR NOME (`window[t]()`). Quando o boot morre, a tela
       tambem nao existe — entao eles nao mediam nada e seguiam CALADOS. Um
       portao que nao mede nada imprime a mesma coisa que um portao que
       aprovou. Passou.
     • `_qa/telavazia.py` le o CODIGO procurando tela sem conteudo. O codigo
       estava cheio. Passou.

   Ou seja: a banca tinha 65 portoes e NENHUM fazia a pergunta mais burra de
   todas — "isso abre?". Este faz. E ele e o PRIMEIRO da fila: se o boot morre,
   nao adianta medir contraste de texto que nunca foi desenhado.

   O QUE ELE REPROVA (cada item aqui e uma forma real de tela branca):
     1. QUALQUER erro de runtime nao tratado no boot (`pageerror`) — foi este.
     2. `console.error` — o motor as vezes engole a excecao num try/catch e
        so reclama no console; a crianca ve a tela pela metade.
     3. Recurso que nao carrega (404 no proprio arquivo, script que sumiu).
     4. `#app` vazio ou sem NADA visivel depois do boot (tela branca "limpa",
        sem erro nenhum — acontece quando a capa depende de um asset que falta).
     5. O botao da capa nao leva a lugar nenhum (clicou e a tela nao mudou).

   ⚠️ REGRA DA CASA, aplicada aqui: portao que NAO CONSEGUE MEDIR nao devolve
   "ok" — devolve NAO MEDI e reprova. Ja fomos mordidos por portao que rodava
   cego e imprimia silencio (ver o cabecalho do `_qa/imagens.js`).

   Uso:  node _qa/boot.js <arquivo.html>
   Sai 0 se abriu limpo; 1 se reprovou; 2 se nao deu para rodar.
   ============================================================ */
const {chromium} = require('/opt/node22/lib/node_modules/playwright/index.js');
const path = require('path');

const CROMO = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

/* Erros que NAO sao culpa da atividade: rodamos em file://, sem rede e sem
   servidor. Tudo o que e consequencia disso e ruido e nao pode reprovar —
   senao o portao vira alarme falso e a esteira aprende a ignorar ele. */
const RUIDO = [
  /favicon/i,
  /serviceworker|sw\.js/i,          // SW nao registra em file://
  /localStorage|QuotaExceeded|SecurityError.*storage/i,
  /net::ERR_(INTERNET_DISCONNECTED|NAME_NOT_RESOLVED|CONNECTION|BLOCKED)/i,
  /speechSynthesis|AudioContext|play\(\).*user|NotAllowedError/i, // som exige gesto
  /Failed to load resource.*\.mp3/i,
  /pollinations|googleapis|firebase/i,
  /* ⚠️ `fetch` de arquivo local e SEMPRE bloqueado por CORS em file:// — o
     navegador so permite fetch por http. Isso e do TESTE, nao da atividade
     (que na escola roda por https no Pages). Deixar isto reprovando faria o
     portao acusar inocente em toda atividade que le um .json. */
  /blocked by CORS policy|Cross origin requests are only supported|ERR_FAILED/i,
  /Access to fetch at/i,
  /* som que comeca e e cortado por outro som: acontece o tempo todo num app
     narrado (a fala nova corta a antiga, de proposito) e o navegador chama
     isso de erro. Nao e defeito. */
  /play\(\) request was interrupted|The play\(\) request/i
];
const ehRuido = (t) => RUIDO.some(r => r.test(String(t)));

(async () => {
  const arquivo = process.argv[2];
  if (!arquivo) { console.log('uso: node _qa/boot.js <arquivo.html>'); process.exit(2); }

  const problemas = [];
  let b, p;
  try {
    b = await chromium.launch({executablePath: CROMO, args: ['--no-sandbox', '--disable-gpu']});
    p = await b.newPage({viewport: {width: 412, height: 820}});
  } catch (e) {
    console.log('NAO MEDI: nao consegui abrir o Chromium — ' + e.message);
    process.exit(2);
  }

  /* 1) erro de runtime nao tratado — o defeito do Tangram mora aqui */
  p.on('pageerror', err => {
    const t = err && (err.message || String(err));
    if (!ehRuido(t)) problemas.push('ERRO DE RUNTIME no boot: ' + String(t).split('\n')[0]);
  });
  /* 2) excecao engolida que so reclama no console */
  p.on('console', m => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (!ehRuido(t)) problemas.push('console.error: ' + t.slice(0, 200));
  });
  /* 3) arquivo que a propria atividade pede e nao existe */
  p.on('requestfailed', r => {
    const u = r.url();
    if (!ehRuido(u) && !ehRuido(String(r.failure() && r.failure().errorText))) {
      problemas.push('recurso nao carregou: ' + u.split('/').slice(-1)[0]);
    }
  });

  const url = 'file://' + path.resolve(arquivo);
  try {
    await p.goto(url, {waitUntil: 'load', timeout: 30000});
  } catch (e) {
    console.log('REPROVADO: a pagina nem carregou — ' + e.message);
    await b.close(); process.exit(1);
  }
  await p.waitForTimeout(2500);   // o motor tem fade e pre-carga

  /* 4) tela branca SEM erro: o app existe mas nao desenhou nada visivel.
        Conta so o que tem area de verdade e nao esta escondido — um <div>
        vazio de 0x0 nao e conteudo, e um `display:none` tambem nao. */
  let medida;
  try {
    medida = await p.evaluate(() => {
      const alvo = document.getElementById('app') || document.getElementById('root') || document.body;
      if (!alvo) return {erro: 'nao achei #app/#root/body'};
      let visiveis = 0, comTexto = 0, maiorArea = 0;
      const todos = alvo.querySelectorAll('*');
      for (const el of todos) {
        const r = el.getBoundingClientRect();
        if (r.width < 8 || r.height < 8) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) continue;
        visiveis++;
        maiorArea = Math.max(maiorArea, r.width * r.height);
        const txt = (el.textContent || '').trim();
        if (txt && el.children.length === 0) comTexto++;
      }
      return {
        html: alvo.innerHTML.length,
        filhos: todos.length,
        visiveis: visiveis,
        comTexto: comTexto,
        maiorArea: Math.round(maiorArea),
        assinatura: alvo.innerHTML.length + '/' + todos.length
      };
    });
  } catch (e) {
    console.log('NAO MEDI: nao consegui inspecionar a pagina — ' + e.message);
    await b.close(); process.exit(2);
  }

  if (medida.erro) problemas.push('estrutura: ' + medida.erro);
  else {
    /* Os numeros vem do que a tela branca do Tangram realmente devolvia:
       o #app ficava com o fundo e mais nada — poucos elementos, zero texto. */
    if (medida.visiveis < 3)
      problemas.push('TELA BRANCA: so ' + medida.visiveis + ' elemento(s) visivel(is) depois do boot (o app nao desenhou)');
    else if (medida.comTexto === 0)
      problemas.push('TELA MUDA: nenhum texto visivel na capa — a crianca abre e nao le nada');
  }

  /* 5) a capa LEVA a algum lugar? Clicar no botao principal tem que mudar a
        tela. Ja aconteceu de a capa desenhar e o "Comecar" ser um beco. */
  if (!medida.erro && medida.visiveis >= 3) {
    try {
      const antes = medida.assinatura;
      const clicou = await p.evaluate(() => {
        const cands = Array.from(document.querySelectorAll('button, .btn, [onclick]'))
          .filter(el => {
            const r = el.getBoundingClientRect();
            if (r.width < 20 || r.height < 20) return false;
            const cs = getComputedStyle(el);
            return cs.display !== 'none' && cs.visibility !== 'hidden';
          });
        /* prefere o que fala de comecar/jogar; senao o maior botao da tela */
        const fala = cands.find(el => /come|jogar|iniciar|vamos|entrar|play/i.test(el.textContent || ''));
        const alvo = fala || cands.sort((a, b) => {
          const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
          return rb.width * rb.height - ra.width * ra.height;
        })[0];
        if (!alvo) return null;
        alvo.click();
        return (alvo.textContent || '').trim().slice(0, 40) || '(sem texto)';
      });
      if (clicou === null) {
        problemas.push('a capa nao tem nenhum botao clicavel visivel');
      } else {
        await p.waitForTimeout(1800);
        const depois = await p.evaluate(() => {
          const alvo = document.getElementById('app') || document.getElementById('root') || document.body;
          return alvo.innerHTML.length + '/' + alvo.querySelectorAll('*').length;
        });
        if (depois === antes) {
          /* ⚠️ LICAO PAGA NA HORA (set/2026): a Expedicao Santa Catarina caiu
             aqui e ESTAVA CERTA. A capa dela e um CADASTRO (nome, turma,
             personagem) e o "Comecar a explorar!" so libera depois de
             preencher — a tela nao mudar e a VALIDACAO funcionando, nao um
             beco. Portao que acusa inocente ensina a ignorar portao. Entao:
             se a capa pede dados que ninguem preencheu, isto nao e defeito. */
          const pedeDados = await p.evaluate(() => {
            const ins = [...document.querySelectorAll('input[type=text], input:not([type]), textarea')]
              .filter(i => { const r = i.getBoundingClientRect(); return r.width > 20 && r.height > 10; });
            const vazio = ins.some(i => !String(i.value || '').trim());
            const escolhas = document.querySelectorAll('.sel, .escolhido, [aria-pressed="true"], input:checked').length;
            return (ins.length > 0 && vazio) || (ins.length > 0 && escolhas === 0);
          });
          if (!pedeDados)
            problemas.push('BECO NA CAPA: cliquei em "' + clicou + '" e a tela nao mudou em nada');
        }
      }
    } catch (e) {
      problemas.push('NAO MEDI o clique da capa: ' + e.message);
    }
  }

  await b.close();

  /* um erro repetido 40x e UM defeito, nao 40 */
  const unicos = [...new Set(problemas)];
  if (unicos.length) {
    console.log('REPROVADO — a atividade nao abre limpa:');
    unicos.slice(0, 12).forEach(m => console.log('  ✗ ' + m));
    if (unicos.length > 12) console.log('  ... e mais ' + (unicos.length - 12));
    process.exit(1);
  }
  console.log('boot ok — abriu sem erro, desenhou ' + medida.visiveis +
              ' elementos (' + medida.comTexto + ' com texto) e a capa leva adiante');
  process.exit(0);
})();
