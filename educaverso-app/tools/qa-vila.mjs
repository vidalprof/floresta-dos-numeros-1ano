// ============================================================================
// ROBÔ-QA — VILA VIVA (motor RPG, identidade Ninja Adventure)
// Dirige de verdade: boot -> anda nas 4 direções (anim certa) -> colide na
// casa (não atravessa) -> encosta no NPC -> screenshots. Portão 1.
// ============================================================================
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg

const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8143/index.html?rpg'
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
await espera(() => (window).__vila && (window).__vila.sys.isActive())
await page.waitForTimeout(1200)

console.log('== BOOT ==')
ok(true, 'cena VilaViva ativa')
await page.screenshot({ path: OUT + '/qa_v_boot.png' })

console.log('== ANDA nas 4 direções (anim frame a frame) ==')
const anda = async (dx, dy, nome) => {
  const antes = await page.evaluate(() => { const h = (window).__vila.heroi.sp; return { x: h.x, y: h.y } })
  await page.evaluate(([dx, dy]) => (window).__anda((window).__vila.heroi.sp.x + dx, (window).__vila.heroi.sp.y + dy), [dx, dy])
  await page.waitForTimeout(650)
  const meio = await page.evaluate(() => {
    const h = (window).__vila.heroi.sp
    return { anim: h.anims.currentAnim ? h.anims.currentAnim.key : '', x: h.x, y: h.y }
  })
  await page.waitForTimeout(1200)
  const moveu = Math.abs(meio.x - antes.x) + Math.abs(meio.y - antes.y) > 8
  ok(moveu, `andou p/ ${nome}`)
  ok(meio.anim === 'heroi-anda-' + nome, `animação certa (${meio.anim || 'nenhuma'})`)
}
await anda(0, 40, 'baixo')
await anda(60, 0, 'dir')
await anda(0, -40, 'cima')
await anda(-60, 0, 'esq')
await page.screenshot({ path: OUT + '/qa_v_andou.png' })

console.log('== COLISÃO: tenta atravessar a casa ==')
await page.evaluate(() => (window).__tp(90, 110))
await page.evaluate(() => (window).__anda(90, 30))
await page.waitForTimeout(2200)
const preso = await page.evaluate(() => (window).__vila.heroi.sp.y > 50)
ok(preso, 'casa BLOQUEIA o caminho (não atravessa)')

console.log('== NPCs vivos no lugar ==')
const npcs = await page.evaluate(() => (window).__vila.npcs.length)
ok(npcs === 4, `4 NPCs (fazendeiro, menina, avô, dog) — tem ${npcs}`)
await page.evaluate(() => (window).__tp(238, 168))
await page.waitForTimeout(700)
await page.screenshot({ path: OUT + '/qa_v_npc.png' })
ok(true, 'herói ao lado do fazendeiro (screenshot)')

console.log('== GENTE TEM CORPO (não atravessa) e OLHA pra você ==')
await page.evaluate(() => (window).__tp(232, 190))              // abaixo do fazendeiro (232,150)
await page.evaluate(() => (window).__anda(232, 120))            // tenta atravessá-lo
await page.waitForTimeout(2500)
const npcState = await page.evaluate(() => {
  const v = (window).__vila
  const faz = v.npcs[0].sp
  const h = v.heroi.sp
  return { dist: Math.hypot(h.x - faz.x, h.y - faz.y), frame: faz.frame.name }
})
ok(npcState.dist > 8, `fazendeiro BLOQUEIA (dist ${npcState.dist.toFixed(0)}px, não sobrepôs)`)
ok(String(npcState.frame) === '0', `fazendeiro OLHOU pra baixo, onde está o herói (frame ${npcState.frame})`)

console.log('== ERROS ==')
const errosReais = erros.filter(e => !/favicon/.test(e))
ok(errosReais.length === 0, 'zero erros/404 (' + errosReais.length + ')')
errosReais.slice(0, 8).forEach(e => console.log('    ' + e))

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' falha(s) ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
