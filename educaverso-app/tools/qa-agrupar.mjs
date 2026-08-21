// ROBÔ-QA — mecânica AGRUPAR no RPG pixel (FaseGrid): a 1ª dinâmica CRIATIVA.
// Tabuada 3º ano = lei dos GRUPOS IGUAIS: a criança pega caixas na pilha (decide
// QUANTAS), reparte os potes andando pelo mundo e o FAZENDEIRO testa a arrumação.
// Sem gabarito: 3 caixas de 4 E 2 caixas de 6 vencem. Desigual = a caixa tomba +
// pergunta + BKT registra. Vencer = conceito POR ÚLTIMO (n×k) + PEDRAS somem.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8215/index.html?fabrica'
const OUT = process.env.OUT || '/tmp/claude-0/-home-user-floresta-dos-numeros-1ano/9052d2be-05eb-511d-8025-ca916a0a13ce/scratchpad'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const CHAVE = 'educ_progresso_local'

async function gera (page) {
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate((c) => localStorage.removeItem(c), CHAVE)
  await page.evaluate(() => { window.__fabrica.set('f_ano', '3º ano'); window.__fabrica.set('f_obj', 'Tabuada: multiplicar com grupos iguais'); window.__fabrica.set('f_dif', 'medio') })
  await page.evaluate(() => window.__fabrica.gerar())
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 20000 })
  await page.waitForTimeout(800)
  await page.evaluate(() => { Object.defineProperty(window.__grid, '__tq', { get () { return this.trocando }, configurable: true }) })
}
const anda = async (page, x, y, t = 12000) => {
  await page.evaluate(([a, b]) => window.__gAnda(a, b), [x, y]); await page.waitForTimeout(150)
  await page.waitForFunction(() => !window.__gMoving() && !window.__grid.__tq, { timeout: t }).catch(() => {})
  await page.waitForTimeout(200)                        // a ação de pilha/vaga espera a criança PARAR
}
const st = (page) => page.evaluate(() => ({
  mao: window.__grid.agMao, pilha: window.__grid.agPilhaN, soltos: window.__grid.agSoltos.length,
  caixas: window.__grid.agVagas.filter(v => v.tem).map(v => v.count),
  erros: window.__grid.erros, entregou: window.__grid.entregou, concluida: window.__grid.concluida
}))
const prop = (page, n) => page.evaluate((n) => window.__grid.P(n), n)
const gp = (page, n) => page.evaluate((n) => JSON.parse(window.__grid.map.properties.find(p => p.name === n).value), n)

console.log('== FÁBRICA: "Tabuada" (3º ano) -> pedagogo escolhe a mecânica CRIATIVA agrupar ==')
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const errosJs = []
page.on('pageerror', e => errosJs.push(String(e).slice(0, 160)))
{
  await gera(page)
  const esp = await page.evaluate(() => window.__fabricaEspinha)
  ok(esp.mecanica === 'agrupar' && esp.dinamica === 'criar' && esp.kc === 'grupos-iguais', `pedagogo: agrupar/criar, kc=${esp.kc}`)
  ok(await page.evaluate(() => window.__fabricaAlvo) === 12, 'total do tier médio = 12 potes')
  const s = await st(page)
  ok(s.soltos === 12 && s.pilha === 6, `12 potes espalhados + 6 caixas na pilha (${s.soltos}/${s.pilha})`)
  const roteiro = await page.evaluate(() => window.__fabricaRoteiro)
  ok(/\?$/.test(roteiro.falas.pedido.trim()), 'Portão 0: o fazendeiro PERGUNTA (pedido termina em "?")')
  await page.screenshot({ path: OUT + '/agrupar-inicio.png' })
}

console.log('== A CRIANÇA CRIA: 3 caixas na fileira, reparte DESIGUAL (5/4/3) ==')
const VAGAS = await gp(page, 'agVagas')
const PILHA = await gp(page, 'agPilha')
{
  for (let i = 0; i < 3; i++) {
    await anda(page, PILHA[0], PILHA[1])
    await anda(page, VAGAS[i][0], VAGAS[i][1])
  }
  let s = await st(page)
  ok(s.caixas.length === 3 && s.pilha === 3, `3 caixas pousadas (${s.caixas.length}), 3 na pilha (${s.pilha})`)
  const plano = [5, 4, 3]                        // potes por caixa (desigual de propósito)
  for (let v = 0; v < 3; v++) {
    for (let k = 0; k < plano[v]; k++) {
      const alvo = await page.evaluate(() => { const s0 = window.__grid.agSoltos[0]; return [s0.x, s0.y] })
      await anda(page, alvo[0], alvo[1])
      await anda(page, VAGAS[v][0], VAGAS[v][1])
    }
  }
  s = await st(page)
  ok(JSON.stringify(s.caixas) === '[5,4,3]' && s.soltos === 0, `arrumação desigual montada: ${s.caixas} (nada solto)`)
}

console.log('== A LEI JULGA: desigual -> caixa TOMBA + pergunta + BKT registra o erro ==')
{
  const faz = [await prop(page, 'fazX'), await prop(page, 'fazY')]
  await anda(page, faz[0], faz[1] + 1)
  await page.waitForTimeout(500)
  const s = await st(page)
  ok(s.erros === 1 && !s.entregou, `o teste recusou a arrumação desigual (erros=${s.erros}, entregou=${s.entregou})`)
  const balao = await page.evaluate(() => window.__grid.balao.innerHTML)
  ok(/tombou/i.test(balao), 'a consequência é física e o mentor PERGUNTA ("…uma caixa tombou… por que ELA?")')
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['grupos-iguais'] && prog['grupos-iguais'].tentativas >= 1 && prog['grupos-iguais'].acertos === 0, 'BKT registrou o ERRO no kc grupos-iguais')
  await page.screenshot({ path: OUT + '/agrupar-desigual.png' })
}

console.log('== SEM PUNIÇÃO: tira 1 pote da caixa cheia e reequilibra (4/4/4) ==')
{
  await anda(page, VAGAS[0][0], VAGAS[0][1])            // mãos vazias na caixa de 5 = tira 1
  let s = await st(page)
  ok(s.mao === 'pote' && s.caixas[0] === 4, `tirou 1 de volta (mão=${s.mao}, caixa0=${s.caixas[0]})`)
  await anda(page, VAGAS[2][0], VAGAS[2][1])            // leva pra caixa magra
  s = await st(page)
  ok(JSON.stringify(s.caixas) === '[4,4,4]', `reequilibrou: ${s.caixas}`)
}

console.log('== A LEI APROVA: conceito POR ÚLTIMO (3×4=12) + PEDRAS somem + vitória ==')
{
  const faz = [await prop(page, 'fazX'), await prop(page, 'fazY')]
  await anda(page, faz[0], faz[1] + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 6000 }).catch(() => {})
  const s = await st(page)
  ok(s.entregou, 'a arrumação DELA passou no teste (entregou)')
  const balao = await page.evaluate(() => window.__grid.balao.innerHTML)
  ok(/3×4=12/.test(balao), `o conceito veio POR ÚLTIMO, da arrumação dela ("3×4=12" no balão)`)
  await page.waitForTimeout(700)
  await anda(page, await prop(page, 'pedrasX'), await prop(page, 'pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 6000 }).catch(() => {})
  ok((await st(page)).concluida, 'as PEDRAS sumiram e a criança atravessou = VITÓRIA')
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['grupos-iguais'] && prog['grupos-iguais'].acertos >= 1, 'BKT registrou o ACERTO no kc grupos-iguais')
  await page.screenshot({ path: OUT + '/agrupar-vitoria.png' })
}

console.log('== CRIATIVIDADE (sem gabarito): 2 caixas de 6 TAMBÉM vence ==')
{
  await gera(page)
  for (let i = 0; i < 2; i++) { await anda(page, PILHA[0], PILHA[1]); await anda(page, VAGAS[i][0], VAGAS[i][1]) }
  for (let v = 0; v < 2; v++) {
    for (let k = 0; k < 6; k++) {
      const alvo = await page.evaluate(() => { const s0 = window.__grid.agSoltos[0]; return [s0.x, s0.y] })
      await anda(page, alvo[0], alvo[1])
      await anda(page, VAGAS[v][0], VAGAS[v][1])
    }
  }
  const s = await st(page)
  ok(JSON.stringify(s.caixas) === '[6,6]' && s.soltos === 0, `outra arrumação: ${s.caixas}`)
  const faz = [await prop(page, 'fazX'), await prop(page, 'fazY')]
  await anda(page, faz[0], faz[1] + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 6000 }).catch(() => {})
  ok((await st(page)).entregou, '2 caixas de 6 TAMBÉM venceu — a lei aceita TODAS as arrumações iguais')
  const balao = await page.evaluate(() => window.__grid.balao.innerHTML)
  ok(/2×6=12/.test(balao), 'e o conceito nomeado foi o DELA: "2×6=12"')
}

ok(errosJs.length === 0, `zero erros de JS (${errosJs.length})`)
errosJs.slice(0, 4).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
