// CAPTURADOR — dirige a fase pelos momentos-chave e salva screenshots pro
// AUDITOR VISUAL/DESIGN (o "game designer profissional") revisar depois.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8201/index.html?f1'
const OUT = process.env.OUT || '/tmp/audit'
import { mkdirSync } from 'node:fs'
mkdirSync(OUT, { recursive: true })

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__fase1 && (window).__fase1.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(1400)
const shot = async n => { await page.screenshot({ path: `${OUT}/${n}.png` }); console.log('  📸 ' + n) }

await shot('1_inicio')                                   // fazendeiro apresenta o problema
// coleta os 4 da fase
const potes = await page.evaluate(() => (window).__fase1.children.list.filter(o => o.texture && o.texture.key === 'mel' && o.x < 320).map(o => ({ x: o.x, y: o.y })))
await page.evaluate(([x, y]) => (window).__tp1(x, y + 14), [potes[0].x, potes[0].y]); await page.evaluate(([x, y]) => (window).__anda1(x, y), [potes[0].x, potes[0].y])
await page.waitForTimeout(700)
await shot('2_coletando')                                // HUD contando, pote flutuando
for (let i = 1; i < potes.length; i++) { await page.evaluate(([x, y]) => { (window).__tp1(x, y + 14); (window).__anda1(x, y) }, [potes[i].x, potes[i].y]); await page.waitForTimeout(400) }
// entra na casa
await page.evaluate(() => { (window).__tp1(64, 90); (window).__anda1(64, 66) })
await page.waitForFunction(() => (window).__fase1.local === 'casa', { timeout: 8000 }).catch(() => {})
await page.waitForTimeout(900)
await shot('3_interior_casa')                            // dentro da casa + 5o mel
// pega o mel da casa e sai
const mc = await page.evaluate(() => (window).__fase1.children.list.filter(o => o.texture && o.texture.key === 'mel' && o.x > 300).map(o => ({ x: o.x, y: o.y }))[0])
if (mc) { await page.evaluate(([x, y]) => { (window).__tp1(x, y + 12); (window).__anda1(x, y) }, [mc.x, mc.y]); await page.waitForTimeout(500) }
await page.evaluate(() => { const f = (window).__fase1; (window).__anda1(f.saidaCasa.x, f.saidaCasa.y + 20) })
await page.waitForFunction(() => (window).__fase1.local === 'fase', { timeout: 8000 }).catch(() => {})
await page.waitForTimeout(700)
// entrega e captura a EXPLOSÃO
await page.evaluate(() => { const f = (window).__fase1; (window).__tp1(f.fazendeiro.sp.x, f.fazendeiro.sp.y + 22); (window).__anda1(f.fazendeiro.sp.x, f.fazendeiro.sp.y + 12) })
await page.waitForFunction(() => (window).__fase1.entregou, { timeout: 8000 }).catch(() => {})
await page.waitForTimeout(150)
await shot('4_explosao_pedras')                          // pedras explodindo
await page.waitForTimeout(500)
await shot('5_caminho_aberto')                           // caminho livre
await browser.close()
console.log('OK — telas em ' + OUT)
