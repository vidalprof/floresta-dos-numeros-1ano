// ROBÔ-QA — FASES DEMO (formato opção 1: fase emoldurada -> resolve -> próxima)
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8180/index.html?fases'
const OUT = process.env.OUT || '/tmp'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const erros = []
page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 180)))
page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 180)) })
page.on('response', r => { if (r.status() === 404) erros.push('404: ' + r.url().split('/').pop()) })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }

await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__fases && (window).__fases.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(1000)

console.log('== FASE 1 emoldurada ==')
ok(await page.evaluate(() => (window).__fases.fase) === 0, 'começa na fase 1')
const semMiss = await page.evaluate(() => (window).__fases.children.list.filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(semMiss === 0, `zero textura faltando (${semMiss})`)
await page.screenshot({ path: OUT + '/qa_f1.png' })

console.log('== a barreira BLOQUEIA a saída antes de resolver ==')
await page.evaluate(() => { const f = (window).__fases; (window).__tpF(f.faseW/2, 40) })
await page.evaluate(() => { const f = (window).__fases; (window).__andaF(f.faseW/2, -20) })
await page.waitForTimeout(1500)
const naoPassou = await page.evaluate(() => (window).__fases.fase)
ok(naoPassou === 0, 'sem a chave, NÃO passa (barreira segura)')

console.log('== RESOLVE: pega a chave -> barreira some ==')
const centro = await page.evaluate(() => { const f = (window).__fases; return { x: f.faseW/2, y: f.faseH/2 } })
await page.evaluate(([x, y]) => (window).__tpF(x, y + 20), [centro.x, centro.y])
await page.evaluate(([x, y]) => (window).__andaF(x, y), [centro.x, centro.y])
await page.waitForFunction(() => (window).__fases.temChave, { timeout: 8000 }).catch(() => {})
ok(await page.evaluate(() => (window).__fases.temChave), 'pegou a chave (resolveu)')
await page.waitForTimeout(500)
await page.screenshot({ path: OUT + '/qa_f1_aberto.png' })

console.log('== avança: sobe pela passagem -> FASE 2 ==')
await page.evaluate(([x]) => (window).__tpF(x, 44), [centro.x])
await page.evaluate(([x]) => (window).__andaF(x, -30), [centro.x])
await page.waitForFunction(() => (window).__fases.fase === 1, { timeout: 8000 }).catch(() => {})
ok(await page.evaluate(() => (window).__fases.fase) === 1, 'passou para a FASE 2')
await page.waitForTimeout(700)
await page.screenshot({ path: OUT + '/qa_f2.png' })

console.log('== ERROS ==')
const er = erros.filter(e => !/favicon/.test(e))
ok(er.length === 0, `zero erros/404 (${er.length})`)
er.slice(0, 6).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
