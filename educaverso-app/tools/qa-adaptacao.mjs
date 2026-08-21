// QA da ADAPTAÇÃO AO RITMO (loop de verdade): a Fábrica lê o domínio já registrado e
// ajusta a dificuldade (DDA/ZDP); e o jogo REGISTRA o domínio ao concluir.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?fabrica'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const CHAVE = 'educ_progresso_local'

// gera uma fase com um domínio pré-carregado e devolve o alvo escolhido
async function geraCom (pKnown) {
  const page = await browser.newPage()
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate(([chave, pk]) => {
    if (pk === null) localStorage.removeItem(chave)
    else localStorage.setItem(chave, JSON.stringify({ contar: { pKnown: pk, caixa: 1, proximaRevisao: 0, tentativas: 2, acertos: 2 } }))
  }, [CHAVE, pKnown])
  await page.evaluate(() => { window.__fabrica.set('f_dif', 'medio') })   // base alvo = 5
  await page.evaluate(() => window.__fabrica.gerar())
  await page.waitForFunction(() => typeof window.__fabricaAlvo === 'number', { timeout: 15000 })
  const alvo = await page.evaluate(() => window.__fabricaAlvo)
  await page.close()
  return alvo
}

console.log('== ADAPTA: o domínio já registrado muda a dificuldade (base médio = 5) ==')
ok(await geraCom(null) === 5, 'sem histórico -> alvo base (5)')
ok(await geraCom(0.9) === 6, 'domínio ALTO (0.9) -> sobe a dificuldade (6)')
ok(await geraCom(0.3) === 4, 'domínio BAIXO (0.3) -> desce a dificuldade (4)')
ok(await geraCom(0.6) === 5, 'zona neutra (0.6) -> mantém (5)')

console.log('== MEDE: concluir a fase REGISTRA o domínio (sobe pKnown) ==')
{
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate((c) => localStorage.removeItem(c), CHAVE)
  await page.evaluate(() => { window.__fabrica.set('f_dif', 'facil'); window.__fabrica.gerar() })
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 20000 })
  await page.waitForTimeout(700)
  await page.evaluate(() => { Object.defineProperty(window.__grid, '__tq', { get () { return this.trocando }, configurable: true }) })
  const ev = (fn, a) => page.evaluate(fn, a)
  const prop = async (n) => ev((n) => window.__grid.P(n), n)
  const irPara = async (x, y, t = 9000) => { await ev(([x, y]) => window.__gAnda(x, y), [x, y]); await page.waitForTimeout(150); await page.waitForFunction(() => !window.__gMoving() && !window.__grid.__tq, { timeout: t }).catch(() => {}); await page.waitForTimeout(120) }
  // joga a fase inteira até a vitória
  const melExt = await ev(() => JSON.parse(window.__grid.map.properties.find(p => p.name === 'melExternos').value))
  for (const [mx, my] of melExt) await irPara(mx, my)
  await irPara(await prop('portaX'), await prop('portaY')); await page.waitForFunction(() => window.__grid.local === 'casa', { timeout: 5000 }).catch(() => {})
  const melInt = await ev(() => JSON.parse(window.__grid.map.properties.find(p => p.name === 'melInterno').value)); await irPara(melInt[0], melInt[1])
  await irPara(await prop('intSaiX'), await prop('intSaiY')); await page.waitForFunction(() => window.__grid.local === 'fase', { timeout: 5000 }).catch(() => {})
  await irPara(await prop('fazX'), await prop('fazY') + 1); await page.waitForFunction(() => window.__grid.entregou, { timeout: 5000 }).catch(() => {})
  await irPara(await prop('pedrasX'), await prop('pedrasY')); await page.waitForFunction(() => window.__grid.concluida, { timeout: 5000 }).catch(() => {})
  await page.waitForTimeout(300)
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog.contar && prog.contar.tentativas >= 1, 'concluir registrou uma tentativa no KC "contar"')
  ok(prog.contar && prog.contar.pKnown > 0.3, `pKnown subiu ao concluir (${prog.contar ? prog.contar.pKnown.toFixed(2) : '?'} > 0.30)`)
  await page.close()
}

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
