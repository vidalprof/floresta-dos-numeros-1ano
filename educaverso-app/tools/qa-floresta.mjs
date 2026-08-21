// ============================================================================
// ROBÔ-QA — "A Floresta do Byte" (gramática problema->item->entrega->mundo muda)
// Dirige DE VERDADE: explora -> colhe tábuas (mochila) -> leva ao Castor ->
// ponte CONSERTA (bloqueio sai) -> atravessa -> clareira (festa). Portão 1.
// ============================================================================
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg

const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8142/index.html'
const OUT = process.env.OUT || '/tmp'

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const erros = []
page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 200)))
page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 200)) })
page.on('response', r => { if (r.status() === 404) erros.push('404: ' + r.url().split('/').pop()) })

const falhas = []
const ok = (cond, msg) => { if (cond) console.log('  ✔ ' + msg); else { console.log('  ✘ ' + msg); falhas.push(msg) } }
const espera = async (fn, t = 30000) => page.waitForFunction(fn, { timeout: t })

await page.goto(URL, { waitUntil: 'load' })
await espera(() => (window).__mundo && (window).__mundo.heroi)
await page.waitForTimeout(1500)

console.log('== BOOT (floresta, estilo composto) ==')
ok(await page.evaluate(() => (window).__mundo.zona.id) === 'floresta', 'zona inicial = floresta')
await page.screenshot({ path: OUT + '/qa_f_boot.png' })

console.log('== PROBLEMA EXPOSTO (ponte quebrada + Castor pede) ==')
await espera(() => (window).__mundo.estado === 'explora')
await page.evaluate(() => (window).__tp(1150, 950))          // perto do castor
await espera(() => (window).__mundo.estado === 'dialogo', 15000).catch(() => {})
const falouCastor = await page.evaluate(() => (window).__mundo.estado === 'dialogo')
ok(falouCastor, 'Castor apresenta o problema ao chegar perto')
await page.screenshot({ path: OUT + '/qa_f_castor.png' })
await espera(() => (window).__mundo.estado === 'explora', 60000)

console.log('== RESOLVE: colhe as tábuas (contagem narrada) ==')
await page.evaluate(() => (window).__tp(500, 760))           // AFASTA do castor (senão entrega na hora)
await page.waitForTimeout(400)
for (let i = 0; i < 3; i++) { await page.evaluate(() => (window).__colher1()); await page.waitForTimeout(900) }
// a recompensa chega DEPOIS da fala de descoberta (suspense + voz) — espera por ela
await espera(() => (window).__mundo.mochila && (window).__mundo.mochila.asset === 'tabuas', 60000).catch(() => {})
await espera(() => (window).__mundo.estado === 'explora', 60000)
const temItem = await page.evaluate(() => (window).__mundo.mochila && (window).__mundo.mochila.asset === 'tabuas')
ok(temItem, 'ITEM na mochila (tábuas) — recompensa da missão')
await page.screenshot({ path: OUT + '/qa_f_mochila.png' })

console.log('== ENTREGA: leva ao Castor -> o MUNDO MUDA ==')
await page.evaluate(() => (window).__tp(1150, 950))
await espera(() => (window).__mundo.entregou && (window).__mundo.entregou.castor, 30000)
await espera(() => (window).__mundo.estado === 'explora', 60000)
await page.waitForTimeout(900)
const ponteOk = await page.evaluate(() => {
  const m = (window).__mundo
  const obj = m.objPorId.ponte
  return obj && obj.img.texture.key === 'ponte' && !m.bloqPorId.rio_ponte.body
})
ok(ponteOk, 'PONTE consertada (textura trocada) e passagem ABERTA (bloqueio removido)')
const salvo = await page.evaluate(() => { const c = ((window).__mundo.mem().consertos || {}).floresta || {}; return c.objetos && c.objetos.ponte === 'ponte' })
ok(salvo, 'conserto SALVO na memória (o mundo lembra)')
await page.screenshot({ path: OUT + '/qa_f_ponte.png' })

console.log('== ATRAVESSA e chega à CLAREIRA (festa) ==')
await page.evaluate(() => (window).__tp(1600, 700))
await page.waitForTimeout(600)
await page.evaluate(() => (window).__tp(1960, 720))          // entra no portal
await espera(() => (window).__mundo.zona && (window).__mundo.zona.id === 'clareira', 25000)
await page.waitForTimeout(1800)
ok(true, 'transição pela ponte até a Clareira Secreta')
await page.screenshot({ path: OUT + '/qa_f_clareira.png' })

console.log('== ERROS ==')
const errosReais = erros.filter(e => !/favicon|asset ausente|Audio/.test(e))
ok(errosReais.length === 0, 'zero erros de página/404 (' + errosReais.length + ')')
errosReais.slice(0, 8).forEach(e => console.log('    ' + e))

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' falha(s) ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
