// ============================================================================
// ROBÔ-QA — MUNDO DO AUTOR (mapa completo 86x82 do pixel-boy no nosso motor)
// boot -> zero textura faltando -> anda 4 direções -> colisão na floresta ->
// NPCs -> screenshots. Portão 1.
// ============================================================================
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8167/index.html?autor'
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
await page.waitForFunction(() => (window).__mundoA && (window).__mundoA.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(1500)

console.log('== BOOT do MUNDO COMPLETO ==')
const dim = await page.evaluate(() => ({ w: (window).__mundoA.M.w, h: (window).__mundoA.M.h }))
ok(dim.w === 86 && dim.h === 82, `mapa 86x82 do autor carregado (${dim.w}x${dim.h})`)
const faltando = await page.evaluate(() => (window).__mundoA.children.list
  .filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(faltando === 0, `zero texturas faltando (${faltando})`)
await page.screenshot({ path: OUT + '/qa_a_boot.png' })

console.log('== ANDA nas 4 direções no caminho ==')
const anda = async (dx, dy, nome) => {
  const a = await page.evaluate(() => ({ x: (window).__mundoA.heroi.sp.x, y: (window).__mundoA.heroi.sp.y }))
  await page.evaluate(([dx, dy]) => (window).__andaA((window).__mundoA.heroi.sp.x + dx, (window).__mundoA.heroi.sp.y + dy), [dx, dy])
  await page.waitForTimeout(650)
  const m = await page.evaluate(() => { const h = (window).__mundoA.heroi.sp; return { anim: h.anims.currentAnim ? h.anims.currentAnim.key : '', x: h.x, y: h.y } })
  await page.waitForTimeout(900)
  ok(Math.abs(m.x - a.x) + Math.abs(m.y - a.y) > 8 && m.anim === 'heroi-anda-' + nome, `${nome} ok (${m.anim})`)
}
await anda(0, 30, 'baixo'); await anda(40, 0, 'dir'); await anda(0, -30, 'cima'); await anda(-40, 0, 'esq')

console.log('== COLISÃO: floresta bloqueia ==')
// acha a base sólida mais próxima do herói e tenta atravessá-la
const alvoSolido = await page.evaluate(() => {
  const v = (window).__mundoA; const M = v.M
  const hx = Math.round(v.heroi.sp.x / 16), hy = Math.round(v.heroi.sp.y / 16)
  let melhor = null
  for (let y = 0; y < M.h; y++) for (let x = 0; x < M.w; x++) {
    if (M.base[y][x] < 0) continue
    const d = Math.hypot(x - hx, y - hy)
    if (!melhor || d < melhor.d) melhor = { d, x, y }
  }
  return melhor
})
await page.evaluate(([x, y]) => (window).__tpA(x * 16 + 8, y * 16 + 40), [alvoSolido.x, alvoSolido.y])
await page.evaluate(([x, y]) => (window).__andaA(x * 16 + 8, y * 16 - 20), [alvoSolido.x, alvoSolido.y])
await page.waitForTimeout(2000)
const dist = await page.evaluate(([x, y]) => {
  const h = (window).__mundoA.heroi.sp
  return Math.hypot(h.x - (x * 16 + 8), h.y - (y * 16 + 8))
}, [alvoSolido.x, alvoSolido.y])
ok(dist > 8, `construção/árvore BLOQUEIA (dist ${dist.toFixed(0)}px)`)

console.log('== NPCs e dog no mundo ==')
const n = await page.evaluate(() => (window).__mundoA.npcs.length)
ok(n === 4, `4 habitantes (${n})`)
await page.evaluate(() => (window).__tpA(43 * 16, 41 * 16))
await page.waitForTimeout(800)
await page.screenshot({ path: OUT + '/qa_a_centro.png' })

console.log('== ENTRA NA CASA DO AUTOR (porta -> interior) ==')
await page.evaluate(() => (window).__tpA(29 * 16 + 8, 44 * 16 + 8))     // em frente à porta
await page.evaluate(() => (window).__andaA(29 * 16 + 8, 43 * 16))       // sobe até a soleira
await page.waitForFunction(() => (window).__mundoA.local === 'casa', { timeout: 12000 }).catch(() => {})
const dentro = await page.evaluate(() => (window).__mundoA.local)
ok(dentro === 'casa', `ENTROU no interior da casa (${dentro})`)
await page.waitForTimeout(800)
const semMiss = await page.evaluate(() => (window).__mundoA.children.list
  .filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(semMiss === 0, `interior sem textura faltando (${semMiss})`)
// REGRA: os móveis do interior TÊM que estar VISÍVEIS (não afundados sob o piso).
// Bug pego: sala em Y negativo -> depth=Y do mundo = negativo -> móvel some.
const moveis = await page.evaluate(() => (window).__mundoA.children.list
  .filter(o => o.frame && o.frame.texture && o.frame.texture.key === 'mundo' && o.frame.name !== 'tapete')
  .map(o => ({ nome: o.frame.name, depth: o.depth })))
ok(moveis.length >= 2 && moveis.every(m => m.depth > 0),
  `móveis do interior VISÍVEIS (depth>0): ${moveis.map(m => m.nome + '=' + m.depth).join(', ')}`)
await page.screenshot({ path: OUT + '/qa_a_interior.png' })
await page.evaluate(() => (window).__andaA((window).__mundoA.heroi.sp.x, (window).__mundoA.heroi.sp.y + 40))
await page.waitForFunction(() => (window).__mundoA.local === 'mundo', { timeout: 12000 }).catch(() => {})
const voltou = await page.evaluate(() => (window).__mundoA.local)
ok(voltou === 'mundo', `SAIU de volta pro mundo (${voltou})`)

console.log('== CÂMERA presa ao terreno (herói nunca some na borda de baixo) ==')
// leva o herói pro CANTO inferior JOGÁVEL (dentro do terreno) e confere que a
// câmera o mantém na tela (era o bug: ele sumia embaixo)
await page.evaluate(() => { const t = (window).__mundoA.terreno; (window).__tpA(t.x + t.w / 2, t.y + t.h - 24) })
await page.waitForTimeout(1800)                                          // câmera (follow suave) assenta
const dentroT = await page.evaluate(() => {
  const v = (window).__mundoA, h = v.heroi.sp, cam = v.cameras.main
  return h.x >= cam.worldView.x && h.x <= cam.worldView.right && h.y >= cam.worldView.y && h.y <= cam.worldView.bottom
})
ok(dentroT, 'herói visível no canto inferior do terreno (câmera segura)')

console.log('== ERROS ==')
const er = erros.filter(e => !/favicon/.test(e))
ok(er.length === 0, `zero erros/404 (${er.length})`)
er.slice(0, 6).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
