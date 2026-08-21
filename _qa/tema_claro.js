/* ============================================================
   PORTÃO — "e se esta peça cair numa atividade de tema CLARO?"

   ⚠️ LIÇÃO PAGA (ago/2026), e ela custou catorze peças em duas noites.
   A bancada roda a peça sobre o fundo ESCURO dela. Dentro de uma atividade, o
   fundo é o que a atividade quiser: o galpão à noite da Central, o céu do
   Observatório, a rua fotografada do Letreiro. Uma peça de tinta clara passa
   na bancada e morre na atividade — e o defeito só aparece com a criança na
   frente, porque o print da bancada fica perfeito.

   O que este portão faz: injeta na peça o tema de uma atividade CLARA
   (`--texto` escuro, `body` de papel) e roda o mesmo `_qa/contraste.js` que a
   banca roda. É a peça sendo perguntada pelo LADO que a bancada nunca pergunta.

   ⚠️⚠️ POR QUE ELE TEM UMA LISTA DE DÍVIDA. Ligado de uma vez, ele reprova
   **44 das 79 peças** — todas as que hoje passam no escuro. Um portão que
   derruba metade do catálogo na estreia não protege ninguém: ele para a
   fábrica, e a reação humana a isso é desligar o portão. Então ele nasce com
   `DIVIDA-TEMA-CLARO.txt`, a lista das peças que JÁ estavam assim:

     · peça NOVA (fora da lista) que falhar   -> REPROVA. A dívida não cresce.
     · peça da lista que falhar               -> aviso, com o número. É dívida
                                                 conhecida, não surpresa.
     · peça da lista que PASSAR               -> REPROVA pedindo para tirar o
                                                 nome da lista. A lista só
                                                 encolhe, e ninguém precisa
                                                 lembrar de limpá-la.

   Uso: node _qa/tema_claro.js _padrao/pecas/x.html [tela1 tela2 ...]
   ============================================================ */
const fs = require('fs');
const os = require('os');
const path = require('path');
const {execFileSync} = require('child_process');

const RAIZ = path.resolve(__dirname, '..');
const LISTA = path.join(RAIZ, '_padrao', 'pecas', 'DIVIDA-TEMA-CLARO.txt');

/* o tema de uma atividade clara, como o `tema.css` de verdade faz: entra por
   ÚLTIMO, então ganha do CSS da peça no empate de especificidade. */
const TEMA = '<style>/* TEMA CLARO SIMULADO (portao _qa/tema_claro.js) */\n' +
             ':root{--texto:#2f2718}body{background:#efe6d6;color:#2f2718}</style>\n</body>';

const arq = process.argv[2];
if (!arq) { console.log('uso: node _qa/tema_claro.js <peca.html> [telas...]'); process.exit(2); }
const nome = path.basename(arq);

const html = fs.readFileSync(arq, 'utf8');
if (html.indexOf('</body>') < 0) {
  console.log(nome + ' -> sem </body>: NAO MEDI o tema claro.');
  process.exit(2);
}
const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'claro-')), nome);
fs.writeFileSync(tmp, html.replace('</body>', TEMA), 'utf8');

/* ⚠️ SEM A LISTA DE TELAS ELE MEDE ZERO — e "zero medido" saia daqui como se
   fosse "zero sumindo" (defeito do proprio portao, achado na estreia). Quando
   ninguem passa as telas, ele descobre sozinho, do mesmo jeito que a bancada.
   ⚠️ LICAO PAGA (ago/2026): a descoberta era por NOME (`^function (tela|peca)…`)
   e pegava HELPER que so parece tela: o `pecaEl(p)` do domino MONTA uma peca e
   EXIGE argumento — chamado sem args pelo contraste, estoura ("Cannot read
   properties of undefined") e o portao lia o estouro como "texto que some".
   Reprovava dominio/morfemas/passo-a-passo com "0 texto sumindo" (falso
   positivo). Pior: o nome tambem PERDIA tela real que nao comeca com tela/peca
   (o `desenhaTela` do passo-a-passo). A heuristica CERTA e a MESMA do peca.sh:
   tela e a funcao que chama `limpa()` (renderiza a tela do zero). */
let telas = process.argv.slice(3);
if (!telas.length) {
  const js = (html.match(/<script>([\s\S]*?)<\/script>/g) || []).join('\n');
  telas = [];
  const re = /function\s+([A-Za-z_$][\w$]*)\s*\(/g;
  let m;
  while ((m = re.exec(js))) {
    let j = js.indexOf('{', m.index), k = j, prof = 0;
    if (j < 0) continue;
    while (k < js.length) {
      const ch = js[k];
      if (ch === '{') prof++;
      else if (ch === '}') { prof--; if (prof === 0) break; }
      k++;
    }
    if (/\blimpa\(\)/.test(js.slice(j, k))) telas.push(m[1]);
  }
}

let saida = '', falhou = false;
try {
  saida = execFileSync('node', [path.join(RAIZ, '_qa', 'contraste.js'), tmp]
                       .concat(telas),
                       {encoding: 'utf8', maxBuffer: 1 << 24});
} catch (e) {
  saida = (e.stdout || '') + (e.stderr || '');
  falhou = true;
}
try { fs.rmSync(path.dirname(tmp), {recursive: true, force: true}); } catch (e) {}

const devendo = fs.existsSync(LISTA)
  ? fs.readFileSync(LISTA, 'utf8').split('\n')
      .map(l => l.replace(/#.*/, '').trim()).filter(Boolean)
  : [];
const naLista = devendo.indexOf(nome) >= 0;

/* ⚠️ "NAO MEDI" NAO E "PASSOU" — e tambem nao e "reprovou". Os tres codigos da
   casa valem aqui: se o contraste nao conseguiu abrir tela nenhuma, este portao
   sai com 2 e diz isso, em vez de carimbar a peca de um jeito ou de outro. */
if (/NAO MEDI|0 tela\(s\)/.test(saida)) {
  console.log(nome + ' -> tema CLARO: NAO MEDI (nenhuma tela aberta).');
  console.log(saida.split('\n').filter(l => l.trim()).slice(0, 3).join('\n'));
  process.exit(2);
}
const linhas = saida.split('\n').filter(l => /razao/.test(l));
console.log(nome + ' -> tema CLARO: ' + (falhou ? linhas.length + ' texto(s) sumindo' : 'ok'));
for (const l of linhas.slice(0, 6)) console.log('   ' + l.trim());

if (falhou && !naLista) {
  console.log('   !! PECA NOVA COM TEXTO QUE SOME NO TEMA CLARO.');
  console.log('   conserto: quem cai no FUNDO DA ATIVIDADE segue o tema');
  console.log('   (`var(--texto)`); quem quer cor propria carrega a MESA dela.');
  process.exit(1);
}
if (falhou && naLista) {
  console.log('   (divida conhecida: esta peca ja estava assim — ver ' +
              '_padrao/pecas/DIVIDA-TEMA-CLARO.txt)');
  process.exit(0);
}
if (!falhou && naLista) {
  console.log('   !! ESTA PECA SAIU DA DIVIDA: tire "' + nome + '" de');
  console.log('   _padrao/pecas/DIVIDA-TEMA-CLARO.txt. A lista so encolhe.');
  process.exit(1);
}
console.log('   tema claro ok: nenhum texto some quando o fundo e de papel');
