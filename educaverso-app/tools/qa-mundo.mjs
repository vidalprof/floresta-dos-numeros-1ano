// ============================================================================
// ROBÔ-QA DA FÁBRICA DE MUNDOS — dirige o mundo DE VERDADE (Playwright).
// Portão 1: o jogo funciona antes de qualquer humano ver.
//  1. boot da zona inicial (sem erro de console)
//  2. MISSÃO: colhe todos os itens -> cesta enche -> celebração
//  3. PORTAIS: visita todas as zonas do grafo (transição real com fade)
//  4. screenshot de cada zona + relatório final (exit 1 se reprovar)
// Uso: node tools/qa-mundo.mjs  (serve dist/ em 8142 antes, ou usa URL env)
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

const falhas = []
const ok = (cond, msg) => { if (cond) console.log('  ✔ ' + msg); else { console.log('  ✘ ' + msg); falhas.push(msg) } }

await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__mundo && (window).__mundo.heroi, { timeout: 20000 })
await page.waitForTimeout(1200)

console.log('== BOOT ==')
const z0 = await page.evaluate(() => (window).__mundo.zona.id)
ok(z0 === 'pomar', 'zona inicial = pomar (' + z0 + ')')
await page.screenshot({ path: OUT + '/qa_z_pomar.png' })

console.log('== MISSÃO (colher no mundo) ==')
// espera o diálogo de chegada acabar (voz/texto) e colhe TUDO, um a um
await page.waitForFunction(() => (window).__mundo.estado === 'explora', { timeout: 30000 })
for (let i = 0; i < 5; i++) {
  await page.evaluate(() => (window).__colher1())
  await page.waitForTimeout(900)
}
const colhidas = await page.evaluate(() => (window).__mundo.colhidas)
ok(colhidas === 5, 'todas as maçãs colhidas (' + colhidas + '/5)')
await page.waitForTimeout(1200)
const feita = await page.evaluate(() => { const m = (window).__mundo.mem(); return !!(m.missoes && m.missoes.pomar) })
ok(feita, 'missão salva na memória (o mundo vai LEMBRAR)')
await page.screenshot({ path: OUT + '/qa_missao_fim.png' })

console.log('== PORTAIS (grafo completo) ==')
async function irZona (id) {
  await page.waitForFunction(() => ['explora', 'dialogo'].includes((window).__mundo.estado), { timeout: 30000 })
  await page.evaluate((zid) => { (window).__mundo.estado = 'explora'; (window).__irZona(zid) }, id)
  await page.waitForFunction((zid) => (window).__mundo && (window).__mundo.zona && (window).__mundo.zona.id === zid && (window).__mundo.heroi, id, { timeout: 20000 })
  await page.waitForTimeout(1400)
  const zid = await page.evaluate(() => (window).__mundo.zona.id)
  ok(zid === id, 'transição para "' + id + '"')
  await page.screenshot({ path: OUT + '/qa_z_' + id + '.png' })
}
await irZona('colina')
await irZona('cabana')
await irZona('colina2'.replace('2', ''))   // volta (prova ida-e-volta)
await irZona('lago')

console.log('== ERROS DE CONSOLE ==')
const errosReais = erros.filter(e => !/favicon|asset ausente|Audio/.test(e))
ok(errosReais.length === 0, 'zero erros de página (' + errosReais.length + ')')
errosReais.slice(0, 6).forEach(e => console.log('    ' + e))

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' falha(s) ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
