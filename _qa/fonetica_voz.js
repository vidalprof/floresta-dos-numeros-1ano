/* fonetica_voz.js — aplica ao TEXTO DA TELA a mesma troca fonetica que o montador
   aplica ao texto que vai ao TTS ("face" -> "fásse", "sandboard" -> "sendibórdi"),
   para os portoes de voz compararem coisas comparaveis.

   ⚠️ LICAO PAGA (set/2026, Solidos): o 0g e o 0n tiravam acento e comparavam
   letras; "fasse" != "face" virou 6 "defeitos" numa atividade certa — e o mesmo
   truque ja valia para "êlefante"/"mími" so porque o acento cai na norma. A tabela
   mora em UM lugar (`montar._FONETICA_VOZ`) e chega aqui por `fonetica_dump.py`;
   se o python falhar, `fonetica()` devolve o texto intacto e AVISA (o portao nao
   pode passar cego, mas tambem nao pode morrer por causa do ajudante).

   Uso: const {fonetica} = require('./fonetica_voz'); norm(fonetica(textoDaTela)) */
const {execFileSync} = require('child_process');
const path = require('path');

let REGRAS = null;
function carrega() {
  if (REGRAS) return REGRAS;
  REGRAS = [];
  try {
    const json = execFileSync('python3', [path.join(__dirname, 'fonetica_dump.py')],
                              {encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']});
    for (const [pat, flags, sub] of JSON.parse(json)) {
      try { REGRAS.push([new RegExp(pat, 'g' + (flags || '')), sub]); }
      catch (e) { /* regex que o JS nao entende: pula so ela */ }
    }
  } catch (e) {
    console.log('   aviso: nao li a tabela fonetica do montador (' +
                String(e.message || e).split('\n')[0] + ') — comparo sem ela');
  }
  return REGRAS;
}

function fonetica(t) {
  let s = String(t || '');
  for (const [rx, sub] of carrega()) s = s.replace(rx, sub);
  return s;
}

module.exports = {fonetica};
