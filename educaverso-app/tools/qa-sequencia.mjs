// ROBÔ-QA — SEQUÊNCIA de missões (aula completa): tabuada 12 -> 18 -> DIVISÃO 12÷3.
// Testa: botão "Próxima missão", a lei apertada da partilha (agTodas: TODAS as caixas
// recebem — 2×6 é RECUSADO na divisão!) e o conceito ÷ nomeado por último.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8215/index.html?fabrica'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const errosJs = []
page.on('pageerror', e => errosJs.push(String(e).slice(0, 160)))
await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
await page.evaluate(() => { localStorage.removeItem('educ_progresso_local'); window.__fabrica.set('f_ano', '3º ano'); window.__fabrica.set('f_obj', 'Tabuada: multiplicar com grupos iguais'); window.__fabrica.set('f_dif', 'medio'); window.__fabrica.gerar() })
await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 20000 })
await page.waitForTimeout(700)
const prep = () => page.evaluate(() => { Object.defineProperty(window.__grid, '__tq', { get () { return this.trocando }, configurable: true }) })
await prep()
const anda = async (x, y) => { await page.evaluate(([a, b]) => window.__gAnda(a, b), [x, y]); await page.waitForTimeout(150); await page.waitForFunction(() => !window.__gMoving() && !window.__grid.__tq, { timeout: 15000 }).catch(() => {}); await page.waitForTimeout(220) }
const gp = (n) => page.evaluate((n) => JSON.parse(window.__grid.map.properties.find(p => p.name === n).value), n)
const prop = (n) => page.evaluate((n) => window.__grid.P(n), n)
const vence = async (plano) => {   // plano = [[caixaIdx, potes], ...]
  const V = await gp('agVagas'), P = await gp('agPilha')
  for (const [i] of plano) { await anda(P[0], P[1]); await anda(V[i][0], V[i][1]) }
  for (const [i, n] of plano) {
    for (let k = 0; k < n; k++) {
      const alvo = await page.evaluate(() => { const s = window.__grid.agSoltos[0]; return [s.x, s.y] })
      await anda(alvo[0], alvo[1]); await anda(V[i][0], V[i][1])
    }
  }
  await anda(await prop('fazX'), (await prop('fazY')) + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 9000 }).catch(() => {})
}

console.log('== M1: tabuada 12 (2 caixas de 6 vence) ==')
{
  ok(await page.evaluate(() => window.__grid.agTotal) === 12, 'M1 tem 12 potes')
  await vence([[0, 6], [1, 6]])
  await page.waitForTimeout(700)
  await anda(await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 6000 })
  ok(true, 'M1 vencida')
  await page.waitForFunction(() => !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => /Próxima missão/.test(b.textContent)), { timeout: 6000 })
  ok(true, 'botão "Próxima missão" apareceu')
  await page.evaluate(() => [...document.querySelectorAll('button')].find(b => /Próxima missão/.test(b.textContent)).click())
}

console.log('== M2: a encomenda cresce (18 potes) ==')
{
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive() && window.__grid.agTotal === 18 && !window.__grid.concluida, { timeout: 15000 })
  await prep()
  ok(true, 'M2 nasceu com 18 potes (mesma lei, desafio maior)')
  await vence([[0, 6], [1, 6], [2, 6]])
  await page.waitForTimeout(700)
  await anda(await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 6000 })
  ok(true, 'M2 vencida (3×6=18)')
  await page.waitForFunction(() => [...document.querySelectorAll('button')].some(b => /Próxima missão/.test(b.textContent)), { timeout: 6000 })
  await page.evaluate(() => [...document.querySelectorAll('button')].find(b => /Próxima missão/.test(b.textContent)).click())
}

console.log('== M3: DIVISÃO como partilha (12 ÷ 3) — a lei aperta ==')
{
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive() && window.__grid.agTodas === true && !window.__grid.concluida, { timeout: 15000 })
  await prep()
  const s0 = await page.evaluate(() => ({ tot: window.__grid.agTotal, cx: window.__grid.agCaixas, kc: window.__grid.kcId }))
  ok(s0.tot === 12 && s0.cx === 3 && s0.kc === 'particao-igual', `M3: 12 potes, 3 caixas obrigatórias, kc=${s0.kc}`)
  // tenta 2 caixas de 6 (venceria na tabuada) -> a partilha RECUSA (comprador sem caixa)
  await vence([[0, 6], [1, 6]])
  const s1 = await page.evaluate(() => ({ erros: window.__grid.erros, entregou: window.__grid.entregou }))
  ok(s1.erros >= 1 && !s1.entregou, `partilha recusou 2×6 (todos têm que receber) — erros=${s1.erros}`)
  const balao = await page.evaluate(() => window.__grid.balao.innerHTML)
  ok(/sem nada|SUA caixa|caixa vazia|falta/i.test(balao), 'o mentor explica: tem comprador sem caixa')
  // conserta: tira 2 potes de cada caixa cheia e monta a 3ª -> 4/4/4
  const V = await gp('agVagas'), P = await gp('agPilha')
  await anda(P[0], P[1]); await anda(V[2][0], V[2][1])          // 3ª caixa na vaga
  for (const de of [0, 0, 1, 1]) {
    await anda(V[de][0], V[de][1])                               // tira 1 (mãos vazias)
    await anda(V[2][0], V[2][1])                                 // guarda na 3ª
  }
  const s2 = await page.evaluate(() => window.__grid.agVagas.filter(v => v.tem).map(v => v.count))
  ok(JSON.stringify(s2) === '[4,4,4]', `repartiu certo: ${s2}`)
  await anda(await prop('fazX'), (await prop('fazY')) + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 9000 })
  const b2 = await page.evaluate(() => window.__grid.balao.innerHTML)
  ok(/12÷3=4/.test(b2) && /DIVIDIR/i.test(b2), 'o conceito ÷ veio POR ÚLTIMO: "12÷3=4 … DIVIDIR"')
  await page.waitForTimeout(700)
  await anda(await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 6000 })
  ok(true, 'aula completa: multiplicou E dividiu')
  const prog = await page.evaluate(() => JSON.parse(localStorage.getItem('educ_progresso_local') || '{}'))
  ok(prog['particao-igual'] && prog['particao-igual'].acertos >= 1, 'BKT registrou o kc particao-igual em separado')
}
ok(errosJs.length === 0, `zero erros de JS (${errosJs.length})`)
errosJs.slice(0, 4).forEach(e => console.log('    ' + e))
await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
