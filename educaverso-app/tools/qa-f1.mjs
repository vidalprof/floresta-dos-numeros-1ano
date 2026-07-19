// ROBÔ-QA — FASE UM (fase real: junta 5 mel -> entrega -> mundo muda -> vitória; casa)
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?f1'
const OUT = process.env.OUT || '/tmp'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const erros = []
page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 180)))
page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 180)) })
page.on('response', r => { if (r.status() === 404) erros.push('404: ' + r.url().split('/').pop()) })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const esp = (fn, t = 12000) => page.waitForFunction(fn, { timeout: t }).catch(() => {})

await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__fase1 && (window).__fase1.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(1200)

console.log('== BOOT (fase emoldurada + música carregada) ==')
ok(await page.evaluate(() => (window).__fase1.mel) === 0, 'começa com 0 mel')
ok(await page.evaluate(() => (window).__fase1.cache.audio.exists('musica')), 'música do jogo carregada')
const semMiss = await page.evaluate(() => (window).__fase1.children.list.filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(semMiss === 0, `zero textura faltando (${semMiss})`)
await page.screenshot({ path: OUT + '/qa_f1r.png' })

console.log('== MOLDURA: nenhum sprite pode VAZAR pra fora do quadro da fase ==')
const vazando = await page.evaluate(() => {
  const f = (window).__fase1, W = f.faseW, H = f.faseH, tol = 2
  const fora = []
  for (const o of f.children.list) {
    if (!o.getBounds || o.scrollFactorX === 0) continue          // ignora HUD (fixo na tela)
    // só o que a CRIANÇA VÊ: sprite/imagem com textura real (não retângulo de colisão)
    const key = o.texture && o.texture.key
    if (!key || key.startsWith('__')) continue                   // pula __BASE/__WHITE (colisão invisível)
    if (o.visible === false || o.alpha === 0) continue
    const b = o.getBounds()
    const cx = b.centerX, cy = b.centerY
    if (cx < 0 || cx > W || cy < 0 || cy > H) continue            // objeto de outra zona (interior)
    if (b.left < -tol || b.top < -tol || b.right > W + tol || b.bottom > H + tol) {
      fora.push(key + ' r=' + Math.round(b.right) + '/' + W)
    }
  }
  return fora
})
ok(vazando.length === 0, 'nenhum sprite vaza da moldura' + (vazando.length ? ': ' + vazando.slice(0, 4).join(', ') : ''))

console.log('== RESOLVE: junta os 5 potes de mel (contar) ==')
const potes = await page.evaluate(() => (window).__fase1.children.list.filter(o => o.texture && o.texture.key === 'mel').map(o => ({ x: o.x, y: o.y })))
ok(potes.length === 5, `5 potes de mel na fase (${potes.length})`)
for (const p of potes) {
  await page.evaluate(([x, y]) => (window).__tp1(x, y + 14), [p.x, p.y])
  await page.evaluate(([x, y]) => (window).__anda1(x, y), [p.x, p.y])
  await page.waitForTimeout(500)
}
await esp(() => (window).__fase1.mel >= 5)
ok(await page.evaluate(() => (window).__fase1.mel) === 5, 'juntou os 5 (contagem certa)')

console.log('== ENTREGA ao fazendeiro -> o MUNDO MUDA (pedras somem) ==')
await page.evaluate(() => { const f = (window).__fase1; (window).__tp1(f.fazendeiro.sp.x, f.fazendeiro.sp.y + 22) })
await page.evaluate(() => { const f = (window).__fase1; (window).__anda1(f.fazendeiro.sp.x, f.fazendeiro.sp.y + 12) })
await esp(() => (window).__fase1.entregou)
ok(await page.evaluate(() => (window).__fase1.entregou), 'entregou ao fazendeiro')
await page.waitForTimeout(600)
const pedrasFora = await page.evaluate(() => (window).__fase1.children.list.filter(o => o.texture && o.texture.key === 'pedras2').length === 0)
ok(pedrasFora, 'as pedras da saída SUMIRAM (mundo mudou)')
await page.screenshot({ path: OUT + '/qa_f1r_aberto.png' })

console.log('== VITÓRIA: atravessa a saída aberta ==')
await page.evaluate(() => { const f = (window).__fase1; (window).__tp1(f.faseW - 40, f.faseH / 2) })
await page.evaluate(() => { const f = (window).__fase1; (window).__anda1(f.faseW - 4, f.faseH / 2) })
await esp(() => (window).__fase1.trocando)
ok(await page.evaluate(() => (window).__fase1.trocando), 'passou pela saída = fase concluída')

console.log('== ENTRA NA CASA (interior) ==')
await page.reload({ waitUntil: 'load' })
await page.waitForFunction(() => (window).__fase1 && (window).__fase1.sys.isActive(), { timeout: 20000 })
await page.waitForTimeout(1000)
await page.evaluate(() => (window).__tp1(4 * 16 + 8, 4 * 16 + 24))
await page.evaluate(() => (window).__anda1(4 * 16 + 8, 4 * 16 + 6))
await esp(() => (window).__fase1.local === 'casa')
ok(await page.evaluate(() => (window).__fase1.local) === 'casa', 'entrou na casa (interior)')
await page.waitForTimeout(700)
await page.screenshot({ path: OUT + '/qa_f1r_casa.png' })

console.log('== ERROS ==')
const er = erros.filter(e => !/favicon/.test(e))
ok(er.length === 0, `zero erros/404 (${er.length})`)
er.slice(0, 6).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
