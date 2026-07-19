// ROBÔ-QA — FASE-COBAIA (Tiled + grid-engine). Prova o NOVO jeito:
// andar na grade, PAREDE barra, CASA barra — tudo por ge_collide no mapa (DADO),
// SEM um único retângulo de colisão escrito à mão. Se isto passa, a virada funciona.
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
const tile = () => page.evaluate(() => (window).__gTile())
// manda andar até um tile e espera parar (grid-engine acha o caminho e desvia)
const andaAte = async (x, y, t = 8000) => {
  await page.evaluate(([x, y]) => (window).__gAnda(x, y), [x, y])
  await page.waitForTimeout(150)
  await page.waitForFunction(() => !(window).__gMoving(), { timeout: t }).catch(() => {})
  await page.waitForTimeout(120)
}

await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => (window).__grid && (window).__grid.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(800)

console.log('== BOOT (mapa Tiled carregado + grid-engine ativo) ==')
ok(await page.evaluate(() => !!(window).__gTile), 'grid-engine no ar (hooks expostos)')
const semMiss = await page.evaluate(() => (window).__grid.children.list.filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(semMiss === 0, `zero textura faltando (${semMiss})`)
const ini = await tile()
ok(ini.x === 10 && ini.y === 10, `herói começa no tile do MAPA (${ini.x},${ini.y}) = (10,10)`)
await page.screenshot({ path: OUT + '/qa_fgrid.png' })

console.log('== ANDAR NA GRADE (movimento em tiles) ==')
await andaAte(14, 10)
const t1 = await tile()
ok(t1.x === 14 && t1.y === 10, `andou pela grade até (14,10) — chegou (${t1.x},${t1.y})`)

console.log('== PAREDE barra (borda direita é sólida, menos a saída na linha 7) ==')
await andaAte(19, 10)                       // x=19 é o muro direito (sólido) na linha 10
const t2 = await tile()
ok(t2.x <= 18, `a PAREDE barra o herói na borda (parou em x=${t2.x}, não entrou no muro x=19)`)

console.log('== CHÃO até a parede de baixo (linha 14 é sólida) ==')
await andaAte(14, 14)                        // y=14 é o muro de baixo
const t3 = await tile()
ok(t3.y <= 13, `a PAREDE de baixo barra o herói (parou em y=${t3.y}, não entrou no muro y=14)`)

console.log('== CASA barra (bloco de colisão 3x2 marcado no mapa) ==')
await andaAte(4, 3)                          // (4,3) é tile da casa (sólido) — não pode parar nele
const t4 = await tile()
ok(!(t4.x === 4 && t4.y === 3), `a CASA barra o herói (não pisou no tile sólido; ficou em ${t4.x},${t4.y})`)

console.log('== volta pro centro (prova que anda livre onde é chão) ==')
await andaAte(10, 10)
const t5 = await tile()
ok(t5.x === 10 && t5.y === 10, `voltou ao centro livre (${t5.x},${t5.y})`)
await page.screenshot({ path: OUT + '/qa_fgrid_fim.png' })

console.log('== ERROS ==')
const er = erros.filter(e => !/favicon/.test(e))
ok(er.length === 0, `zero erros/404 (${er.length})`)
er.slice(0, 8).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
