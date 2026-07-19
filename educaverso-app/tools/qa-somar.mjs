// ROBÔ-QA — mecânica SOMAR (resolver problema, anos 3º-9º): fichas com VALOR; a criança
// planeja quais fecham a soma EXATA. Testa: (1) caminho certo até a vitória;
// (2) o ERRO real (estourar) — fichas voltam, soma zera e o domínio REGISTRA o erro.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?fabrica'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const CHAVE = 'educ_progresso_local'

async function abre () {
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
  const erros = []
  page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 180)))
  page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 180)) })
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate((c) => localStorage.removeItem(c), CHAVE)
  await page.evaluate(() => { window.__fabrica.set('f_ano', '6º ano'); window.__fabrica.set('f_dif', 'medio'); window.__fabrica.set('f_obj', 'Resolver problemas de adição') })
  await page.evaluate(() => window.__fabrica.gerar())
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 20000 })
  await page.waitForTimeout(800)
  await page.evaluate(() => { Object.defineProperty(window.__grid, '__tq', { get () { return this.trocando }, configurable: true }) })
  return { page, erros }
}
const irPara = async (page, x, y, t = 9000) => {
  await page.evaluate(([x, y]) => window.__gAnda(x, y), [x, y]); await page.waitForTimeout(150)
  await page.waitForFunction(() => !window.__gMoving() && !window.__grid.__tq, { timeout: t }).catch(() => {})
  await page.waitForTimeout(120)
}
const fichas = (page) => page.evaluate(() => JSON.parse(window.__grid.map.properties.find(p => p.name === 'melValores').value))

console.log('== SOMAR: 6º ano + "adição" -> pedagogo escolhe RESOLVER/somar (T=12) ==')
{
  const { page, erros } = await abre()
  const esp = await page.evaluate(() => window.__fabricaEspinha)
  ok(esp.mecanica === 'somar' && esp.dinamica === 'resolver', `pedagogo escolheu somar/resolver (${esp.mecanica}/${esp.dinamica})`)
  ok(await page.evaluate(() => window.__grid.mecanica) === 'somar', 'motor entrou no modo somar')
  ok(await page.evaluate(() => window.__grid.alvoSoma) === 12, `alvo da soma = 12 (${await page.evaluate(() => window.__grid.alvoSoma)})`)
  const fs = await fichas(page)
  ok(fs.length === 5, `5 fichas com valor no mapa (${fs.length})`)
  const soma345 = fs.filter(f => [3, 4, 5].includes(f[2]))
  ok(soma345.length === 3, 'existem as fichas da solução (3, 4, 5)')

  console.log('== caminho CERTO: pega 3+4+5 = 12 -> entrega -> pedras somem -> vitória ==')
  for (const [fx, fy] of soma345) await irPara(page, fx, fy)
  ok(await page.evaluate(() => window.__grid.soma) === 12, 'soma fechou EXATA em 12')
  const prop = async (n) => page.evaluate((n) => window.__grid.P(n), n)
  await irPara(page, await prop('fazX'), await prop('fazY') + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 5000 }).catch(() => {})
  ok(await page.evaluate(() => window.__grid.entregou), 'entregou (meta = soma exata)')
  await page.waitForTimeout(700)
  await irPara(page, await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 5000 }).catch(() => {})
  ok(await page.evaluate(() => window.__grid.concluida), 'venceu a fase de SOMAR')
  await page.waitForTimeout(300)
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog.somar && prog.somar.acertos >= 1, 'registrou ACERTO no KC "somar"')
  const er = erros.filter(e => !/favicon/.test(e))
  ok(er.length === 0, `zero erros de JS (${er.length})`); er.slice(0, 4).forEach(e => console.log('    ' + e))
  await page.close()
}

console.log('== caminho do ERRO: estourar a soma -> fichas VOLTAM, soma zera, domínio registra ==')
{
  const { page } = await abre()
  const fs = await fichas(page)
  const f7 = fs.find(f => f[2] === 7), f6 = fs.find(f => f[2] === 6)
  ok(!!f7 && !!f6, 'existem os distratores (7 e 6)')
  await irPara(page, f7[0], f7[1])
  ok(await page.evaluate(() => window.__grid.soma) === 7, 'pegou a ficha 7 (soma parcial = 7)')
  await irPara(page, f6[0], f6[1])                      // 7 + 6 = 13 > 12 -> ERRO
  await page.waitForTimeout(400)
  ok(await page.evaluate(() => window.__grid.erros) === 1, 'registrou 1 estouro (erro real)')
  ok(await page.evaluate(() => window.__grid.soma) === 0, 'a soma ZEROU após o estouro')
  const nFichas = await page.evaluate(() => window.__grid.children.list.filter(o => o.texture && o.texture.key === 'mel' && o.active).length)
  ok(nFichas === 5, `as 5 fichas VOLTARAM ao mapa (${nFichas}) — errar = tentar de novo`)
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog.somar && prog.somar.tentativas >= 1 && prog.somar.acertos === 0, 'o domínio REGISTROU o erro (tentativa sem acerto)')
  ok(prog.somar && prog.somar.pKnown < 0.3, `pKnown DESCEU com o erro (${prog.somar ? prog.somar.pKnown.toFixed(2) : '?'} < 0.30)`)
  await page.close()
}

console.log('== ADAPTA por tier: domínio alto no somar -> próxima fase pede 18 ==')
{
  const page = await browser.newPage()
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate((c) => localStorage.setItem(c, JSON.stringify({ somar: { pKnown: 0.9, caixa: 1, proximaRevisao: 0, tentativas: 3, acertos: 3 } })), CHAVE)
  await page.evaluate(() => { window.__fabrica.set('f_ano', '6º ano'); window.__fabrica.set('f_dif', 'medio'); window.__fabrica.gerar() })
  await page.waitForFunction(() => typeof window.__fabricaAlvo === 'number', { timeout: 15000 })
  ok(await page.evaluate(() => window.__fabricaAlvo) === 18, 'domínio alto (0.9) subiu o tier: 12 -> 18')
  await page.close()
}

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
