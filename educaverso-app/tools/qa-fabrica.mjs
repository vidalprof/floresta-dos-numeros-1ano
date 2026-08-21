// ROBÔ-QA — FÁBRICA: preenche o formulário do professor, clica GERAR e JOGA a fase
// gerada do início ao fim. Prova o "clica GERAR e sai a aventura jogável".
// Testa 2 dificuldades (o nº de itens a juntar muda com o pedido = fase diferente).
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?fabrica'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }

async function jogarUma (dif, alvoEsperado) {
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
  const erros = []
  page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 180)))
  page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 180)) })
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!(window).__fabrica, { timeout: 30000 })
  console.log(`\n== FÁBRICA: dificuldade "${dif}" -> deve gerar ${alvoEsperado} itens ==`)
  // preenche o formulário e GERA
  await page.evaluate((d) => { (window).__fabrica.set('f_dif', d); (window).__fabrica.set('f_tema', 'fazenda'); (window).__fabrica.set('f_obj', 'Contar quantidades') }, dif)
  await page.evaluate(() => (window).__fabrica.gerar())
  await page.waitForFunction(() => (window).__grid && (window).__grid.sys.isActive(), { timeout: 20000 })
  await page.waitForTimeout(900)
  const ev = (fn, a) => page.evaluate(fn, a)
  await ev(() => { Object.defineProperty((window).__grid, '__trocandoQA', { get () { return this.trocando }, configurable: true }) })
  ok(await ev(() => (window).__grid.melAlvo) === alvoEsperado, `alvo gerado = ${alvoEsperado} (motor: ${await ev(() => (window).__grid.melAlvo)})`)
  ok(!(await ev(() => (window).__gridErr || null)), 'create sem erro')

  const prop = async (n) => ev((n) => (window).__grid.P(n), n)
  const irPara = async (x, y, t = 9000) => {
    await ev(([x, y]) => (window).__gAnda(x, y), [x, y]); await page.waitForTimeout(150)
    await page.waitForFunction(() => !(window).__gMoving() && !(window).__grid.__trocandoQA, { timeout: t }).catch(() => {})
    await page.waitForTimeout(120)
  }
  const melExt = await ev(() => JSON.parse((window).__grid.map.properties.find(p => p.name === 'melExternos').value))
  for (const [mx, my] of melExt) await irPara(mx, my)
  ok(await ev(() => (window).__grid.mel) === melExt.length, `juntou os ${melExt.length} externos`)
  // entra, pega o 5o, sai
  await irPara(await prop('portaX'), await prop('portaY'))
  await page.waitForFunction(() => (window).__grid.local === 'casa', { timeout: 5000 }).catch(() => {})
  const melInt = await ev(() => JSON.parse((window).__grid.map.properties.find(p => p.name === 'melInterno').value))
  await irPara(melInt[0], melInt[1])
  ok(await ev(() => (window).__grid.mel) === alvoEsperado, `juntou o total = ${alvoEsperado}`)
  await irPara(await prop('intSaiX'), await prop('intSaiY'))
  await page.waitForFunction(() => (window).__grid.local === 'fase', { timeout: 5000 }).catch(() => {})
  // entrega + vitória
  await irPara(await prop('fazX'), await prop('fazY') + 1)
  await page.waitForFunction(() => (window).__grid.entregou, { timeout: 5000 }).catch(() => {})
  ok(await ev(() => (window).__grid.entregou), 'entregou ao personagem')
  await irPara(await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => (window).__grid.concluida, { timeout: 5000 }).catch(() => {})
  ok(await ev(() => (window).__grid.concluida), 'venceu a fase GERADA pela Fábrica')
  const er = erros.filter(e => !/favicon/.test(e))
  ok(er.length === 0, `zero erros (${er.length})`); er.slice(0, 4).forEach(e => console.log('    ' + e))
  await page.close()
}

await jogarUma('facil', 3)
await jogarUma('dificil', 7)
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
