// QA extra — Vila Viva em VIEWPORT DE IPHONE com TOQUE de verdade
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium, devices } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8145/index.html'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const ctx = await browser.newContext({ ...devices['iPhone 12'], isMobile: true, hasTouch: true })
const page = await ctx.newPage()
const erros = []
page.on('pageerror', e => erros.push(String(e).slice(0, 150)))
await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => window.__vila && window.__vila.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(1200)
const antes = await page.evaluate(() => ({ x: window.__vila.heroi.sp.x, y: window.__vila.heroi.sp.y }))
// toca LONGE do heroi (canto sup. esquerdo do canvas) — tocar em cima dele = nao anda
await page.touchscreen.tap(80, 200)
await page.waitForTimeout(1500)
const depois = await page.evaluate(() => ({ x: window.__vila.heroi.sp.x, y: window.__vila.heroi.sp.y }))
const moveu = Math.abs(depois.x - antes.x) + Math.abs(depois.y - antes.y) > 6
console.log(moveu ? '  ✔ TOQUE move o heroi (celular)' : '  ✘ toque NAO moveu')
const capa = await page.evaluate(() => { const b = document.getElementById('telaIntro'); return b && getComputedStyle(b).display !== 'none' })
console.log(!capa ? '  ✔ capa legada INVISIVEL' : '  ✘ capa aparece!')
console.log(erros.length === 0 ? '  ✔ zero erros JS' : '  ✘ erros: ' + erros.join(' | '))
await page.screenshot({ path: '/tmp/qa_v_iphone.png' })
await browser.close()
process.exit(moveu && !capa && erros.length === 0 ? 0 : 1)
