// ROBÔ-QA — FASE 1 no NOVO jeito (Tiled + grid-engine). Joga a fase inteira:
// junta 4 mel -> entra na casa -> pega o 5º -> sai -> entrega ao fazendeiro ->
// as PEDRAS somem (mundo muda) -> atravessa = vitória. Tudo com colisão do MAPA.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?fgrid'
const OUT = process.env.OUT || '/tmp'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const erros = []
page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 200)))
page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 200)) })
page.on('response', r => { if (r.status() === 404) erros.push('404: ' + r.url().split('/').pop()) })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const ev = (fn, a) => page.evaluate(fn, a)
const prop = async (n) => ev((n) => (window).__grid.P ? (window).__grid.P(n) : (window).__grid[n], n)
// anda até um tile e espera parar E a transição soltar
const irPara = async (x, y, t = 9000) => {
  await ev(([x, y]) => (window).__gAnda(x, y), [x, y])
  await page.waitForTimeout(160)
  await page.waitForFunction(() => !(window).__gMoving() && !(window).__grid.__trocandoQA, { timeout: t }).catch(() => {})
  await page.waitForTimeout(140)
}

await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__grid && (window).__grid.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(900)
// expõe trocando pro wait (campo privado -> espelho)
await ev(() => { Object.defineProperty((window).__grid, '__trocandoQA', { get () { return this.trocando }, configurable: true }) })

console.log('== BOOT (fase rica no novo motor) ==')
ok(await ev(() => (window).__grid.mel) === 0, 'começa com 0 mel')
ok(await ev(() => (window).__grid.cache.audio.exists('musica')), 'música do jogo carregada')
const semMiss = await ev(() => (window).__grid.children.list.filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(semMiss === 0, `zero textura faltando (${semMiss})`)
ok(!(await ev(() => (window).__gridErr || null)), 'create sem erro')
await page.screenshot({ path: OUT + '/qa_fgrid.png' })

console.log('== JUNTA os 4 potes externos (contar) ==')
const melExt = await ev(() => JSON.parse((window).__grid.map.properties.find(p => p.name === 'melExternos').value))
for (const [mx, my] of melExt) { await irPara(mx, my) }
ok(await ev(() => (window).__grid.mel) === 4, `juntou os 4 externos (${await ev(() => (window).__grid.mel)})`)

console.log('== ENTRA na casa (pisar na porta) e pega o 5º ==')
await irPara(await prop('portaX'), await prop('portaY'))
await page.waitForFunction(() => (window).__grid.local === 'casa', { timeout: 5000 }).catch(() => {})
ok(await ev(() => (window).__grid.local) === 'casa', 'entrou na casa pela porta')
const melInt = await ev(() => JSON.parse((window).__grid.map.properties.find(p => p.name === 'melInterno').value))
await irPara(melInt[0], melInt[1])
ok(await ev(() => (window).__grid.mel) === 5, `pegou o 5º mel na casa (=5: ${await ev(() => (window).__grid.mel)})`)

console.log('== SAI da casa ==')
await irPara(await prop('intSaiX'), await prop('intSaiY'))
await page.waitForFunction(() => (window).__grid.local === 'fase', { timeout: 5000 }).catch(() => {})
ok(await ev(() => (window).__grid.local) === 'fase', 'saiu da casa com os 5')

console.log('== ENTREGA ao fazendeiro -> as PEDRAS somem (mundo muda) ==')
const fx = await prop('fazX'), fy = await prop('fazY')
await irPara(fx, fy + 1)                                  // encosta no fazendeiro
await page.waitForFunction(() => (window).__grid.entregou, { timeout: 5000 }).catch(() => {})
ok(await ev(() => (window).__grid.entregou), 'entregou ao fazendeiro')
await page.waitForTimeout(700)                            // deixa a animação das pedras terminar
const pedrasFora = await ev(() => (window).__grid.children.list.filter(o => o.texture && o.texture.key === 'pedras2' && o.visible && o.alpha > 0.1).length === 0)
ok(pedrasFora, 'as pedras da saída SUMIRAM')
await page.screenshot({ path: OUT + '/qa_fgrid_aberto.png' })

console.log('== VITÓRIA: atravessa a saída aberta ==')
await irPara(await prop('pedrasX'), await prop('pedrasY'))
await page.waitForFunction(() => (window).__grid.concluida, { timeout: 5000 }).catch(() => {})
ok(await ev(() => (window).__grid.concluida), 'passou pela saída = fase concluída')

console.log('== ERROS ==')
const er = erros.filter(e => !/favicon/.test(e))
ok(er.length === 0, `zero erros/404 (${er.length})`)
er.slice(0, 8).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
