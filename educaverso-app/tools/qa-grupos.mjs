// ROBÔ-QA — "O POMAR DOS GRUPOS" (missão AGRUPAR = lei dos GRUPOS IGUAIS, tabuada 3º ano).
// Prova as LEIS do EducaVerso no motor Mundo (o jogo 2D de verdade):
//  (1) a criança CRIA a arrumação (pega cestas, decide quantas, reparte as maçãs);
//  (2) DESIGUAL (5/4/3) = a cesta diferente TOMBA + o mentor PERGUNTA + BKT registra o erro;
//  (3) reequilibra SEM punição (tira uma maçã de volta) e vence com 4/4/4;
//  (4) o MUNDO MUDA: a pedrona sai, o bloqueio abre, atravessa até a FEIRA (festa);
//  (5) CRIATIVIDADE: 2 cestas de 6 TAMBÉM vence (não há gabarito único).
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8214/index.html?grupos&qa=1'
const OUT = process.env.OUT || '/tmp/claude-0/-home-user-floresta-dos-numeros-1ano/9052d2be-05eb-511d-8025-ca916a0a13ce/scratchpad'
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const CHAVE = 'educ_progresso_local'

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const errosJs = []
page.on('pageerror', e => errosJs.push('pageerror: ' + String(e).slice(0, 180)))

const st = () => page.evaluate(() => window.__agrupar())
const esperaExplora = async (t = 15000) => page.waitForFunction(() => window.__agrupar && window.__agrupar().estado === 'explora', { timeout: t })
// TODA ação espera o mundo estar livre (fala trava a ação — como deve ser) ANTES de andar
const tp = async (x, y, ms = 380) => { await esperaExplora(); await page.evaluate(([a, b]) => window.__tp(a, b), [x, y]); await page.waitForTimeout(ms) }
// as posições da AVENTURA (dados de src/aventuras/grupos.ts)
const MACAS = [[300, 640], [430, 540], [570, 700], [380, 870], [650, 590], [760, 810], [520, 1010], [300, 1080], [830, 540], [950, 640], [700, 1110], [980, 890]]
const VAGAS = [[700, 1000], [800, 1000], [900, 1000], [1000, 1000], [1100, 1000], [1200, 1000]]
const PILHA = [1330, 1010]
const CASTOR = [1380, 860]
const LONGE = [900, 700]

async function boot (limpar = false) {
  await page.goto(URL, { waitUntil: 'load' })
  if (limpar) { await page.evaluate(() => localStorage.clear()); await page.goto(URL, { waitUntil: 'load' }) }
  await page.waitForFunction(() => !!window.__mundo && !!window.__agrupar, { timeout: 30000 })
  await page.waitForTimeout(900)                                  // fala de chegada
  await esperaExplora()
}
const pegaCesta = async () => { await tp(...PILHA, 620) }
const poeCesta = async (i) => { await tp(...VAGAS[i], 650) }
const levaMaca = async (mIdx, vIdx) => { await tp(...MACAS[mIdx], 500); await tp(...VAGAS[vIdx], 560) }

console.log('== BOOT: o mundo 2D monta a aventura (auditor sem GRAVE, zona pomar) ==')
{
  await boot(true)
  ok(await page.evaluate(() => window.__mundo.zona.id) === 'pomar', 'zona inicial = pomar')
  const grave = await page.evaluate(() => (document.getElementById('auditoria')?.textContent || '').includes('[GRAVE]'))
  ok(!grave, 'auditor sem problema GRAVE')
  const s = await st()
  ok(s.soltas === 12 && s.pilha === 6 && s.cestas.length === 6, `12 maçãs, 6 cestas na pilha, 6 vagas (${s.soltas}/${s.pilha}/${s.cestas.length})`)
  await page.screenshot({ path: OUT + '/grupos-inicio.png' })
}

console.log('== O PROBLEMA EXPOSTO: fala do Castor (pedrona fecha a feira) ==')
{
  await tp(...CASTOR, 300)
  await page.waitForFunction(() => window.__agrupar().estado === 'dialogo', { timeout: 6000 }).catch(() => {})
  await esperaExplora()
  ok(true, 'Castor contou o problema (dialogo rodou e voltou ao explora)')
  await tp(...LONGE, 300)
}

console.log('== A CRIANÇA CRIA: 3 cestas, reparte DESIGUAL (5/4/3) de propósito ==')
{
  for (let i = 0; i < 3; i++) { await pegaCesta(); await poeCesta(i) }
  let s = await st()
  ok(s.cestas.filter(c => c.tem).length === 3 && s.pilha === 3, `3 cestas pousadas, 3 na pilha (${s.cestas.filter(c => c.tem).length}/${s.pilha})`)
  const plano = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 1], [6, 1], [7, 1], [8, 1], [9, 2], [10, 2], [11, 2]]  // 5/4/3
  for (const [m, v] of plano) await levaMaca(m, v)
  s = await st()
  ok(JSON.stringify(s.cestas.slice(0, 3).map(c => c.n)) === '[5,4,3]' && s.soltas === 0, `arrumação desigual montada: 5/4/3, nada solto (${s.cestas.slice(0, 3).map(c => c.n)})`)
}

console.log('== A LEI JULGA: desigual -> TOMBA + pergunta socrática + BKT registra o erro ==')
{
  await tp(...CASTOR, 300)
  await page.waitForFunction(() => window.__agrupar().estado === 'dialogo', { timeout: 6000 })
  ok(true, 'o mundo reagiu ao teste (a cesta diferente tomba; o Castor pergunta)')
  await page.screenshot({ path: OUT + '/grupos-desigual.png' })
  await esperaExplora()
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['grupos-iguais'] && prog['grupos-iguais'].tentativas >= 1 && prog['grupos-iguais'].acertos === 0, `BKT registrou o erro no kc grupos-iguais (${prog['grupos-iguais']?.tentativas} tent., ${prog['grupos-iguais']?.acertos} acertos)`)
  const feita = (await st()).feita
  ok(!feita, 'a missão NÃO fechou com arrumação desigual')
  await tp(...LONGE, 300)
}

console.log('== SEM PUNIÇÃO: tira 1 maçã da cesta cheia e reequilibra (4/4/4) ==')
{
  await page.evaluate(() => window.__tocaCesta(0))       // tocou na cesta 0 (a de 5)
  await tp(...VAGAS[0], 620)                              // chegou nela -> tira UMA
  let s = await st()
  ok(s.mao === 'maca' && s.cestas[0].n === 4, `tirou 1 de volta (mão=${s.mao}, cesta0=${s.cestas[0].n})`)
  await tp(...VAGAS[2], 560)                              // leva pra cesta magra
  s = await st()
  ok(JSON.stringify(s.cestas.slice(0, 3).map(c => c.n)) === '[4,4,4]', `reequilibrou: 4/4/4 (${s.cestas.slice(0, 3).map(c => c.n)})`)
}

console.log('== A LEI APROVA: 3 grupos de 4 -> conceito 3x4 POR ÚLTIMO + o MUNDO MUDA ==')
{
  await tp(...CASTOR, 300)
  await page.waitForFunction(() => window.__agrupar().feita === true, { timeout: 12000 })
  ok(true, 'missão FEITA com a arrumação DELA (3 grupos de 4)')
  await esperaExplora(20000)
  await page.waitForTimeout(1200)                        // a pedrona rola pra fora
  const pedraFoi = await page.evaluate(() => !window.__mundo.objPorId.pedrona || !window.__mundo.objPorId.pedrona.img.active)
  ok(pedraFoi, 'a PEDRONA saiu do caminho (consequência no mundo)')
  const bloqFoi = await page.evaluate(() => !window.__mundo.bloqPorId.saida || !window.__mundo.bloqPorId.saida.active)
  ok(bloqFoi, 'o BLOQUEIO da trilha sumiu (a lei abriu a passagem)')
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['grupos-iguais'] && prog['grupos-iguais'].acertos >= 1, 'BKT registrou o ACERTO no kc grupos-iguais')
  await page.screenshot({ path: OUT + '/grupos-vitoria.png' })
}

console.log('== ATRAVESSA: portal atrás da pedra -> FEIRA (festa na chegada) ==')
{
  await tp(1730, 880, 500)
  await page.waitForFunction(() => window.__mundo && window.__mundo.zona && window.__mundo.zona.id === 'feira', { timeout: 12000 })
  ok(true, 'chegou à FEIRA — o caminho que a pedra fechava abriu de verdade')
  await page.waitForTimeout(1400)
  await page.screenshot({ path: OUT + '/grupos-feira.png' })
}

console.log('== CRIATIVIDADE (sem gabarito): 2 cestas de 6 TAMBÉM vence ==')
{
  await boot(true)
  await tp(...CASTOR, 300); await esperaExplora(); await tp(...LONGE, 300)
  for (let i = 0; i < 2; i++) { await pegaCesta(); await poeCesta(i) }
  const plano = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1]]  // 6/6
  for (const [m, v] of plano) await levaMaca(m, v)
  const s = await st()
  ok(JSON.stringify(s.cestas.slice(0, 2).map(c => c.n)) === '[6,6]' && s.soltas === 0, `outra arrumação: 6/6 (${s.cestas.slice(0, 2).map(c => c.n)})`)
  await tp(...CASTOR, 300)
  await page.waitForFunction(() => window.__agrupar().feita === true, { timeout: 12000 })
  ok(true, '2×6 TAMBÉM venceu — a lei aceita TODAS as arrumações iguais (não há gabarito)')
}

ok(errosJs.length === 0, `zero erros de JS (${errosJs.length})`)
errosJs.slice(0, 4).forEach(e => console.log('    ' + e))

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
