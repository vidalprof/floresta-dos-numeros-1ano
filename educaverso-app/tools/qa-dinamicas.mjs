// ROBÔ-QA — DINÂMICAS POR CONTEÚDO (selecionar sob regra + ordenar sequência).
// Prova a exigência do Marcos: o professor passa um CONTEÚDO qualquer e a atividade faz a
// criança RESOLVER problemas DAQUELE conteúdo (não é sempre soma). Um motor, vários conteúdos:
//  (1) selecionar "múltiplos de 3"  (2) MESMO motor com "frações equivalentes"
//  (3) ordenar em ordem crescente — fora de ordem = erro real registrado.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8190/index.html?fabrica'
const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const CHAVE = 'educ_progresso_local'

async function gera (ano, objetivo) {
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
  const errosJs = []
  page.on('pageerror', e => errosJs.push(String(e).slice(0, 160)))
  await page.goto(URL, { waitUntil: 'load' })
  await page.waitForFunction(() => !!window.__fabrica, { timeout: 30000 })
  await page.evaluate((c) => localStorage.removeItem(c), CHAVE)
  await page.evaluate(([a, o]) => { window.__fabrica.set('f_ano', a); window.__fabrica.set('f_obj', o); window.__fabrica.set('f_dif', 'medio') }, [ano, objetivo])
  await page.evaluate(() => window.__fabrica.gerar())
  await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 20000 })
  await page.waitForTimeout(800)
  await page.evaluate(() => { Object.defineProperty(window.__grid, '__tq', { get () { return this.trocando }, configurable: true }) })
  return { page, errosJs }
}
const irPara = async (page, x, y, t = 9000) => {
  await page.evaluate(([x, y]) => window.__gAnda(x, y), [x, y]); await page.waitForTimeout(150)
  await page.waitForFunction(() => !window.__gMoving() && !window.__grid.__tq, { timeout: t }).catch(() => {})
  await page.waitForTimeout(120)
}
// posições dos itens + o item em si: [{x, y, rotulo, ok, ordem}]
const posicoes = (page) => page.evaluate(() => {
  const pos = JSON.parse(window.__grid.map.properties.find(p => p.name === 'melItens').value)
  const its = JSON.parse(window.__grid.map.properties.find(p => p.name === 'itens').value)
  return pos.map(([x, y, i]) => ({ x, y, ...its[i] }))
})
const vencer = async (page) => {
  const prop = async (n) => page.evaluate((n) => window.__grid.P(n), n)
  await irPara(page, await prop('fazX'), await prop('fazY') + 1)
  await page.waitForFunction(() => window.__grid.entregou, { timeout: 5000 }).catch(() => {})
  await page.waitForTimeout(700)
  await irPara(page, await prop('pedrasX'), await prop('pedrasY'))
  await page.waitForFunction(() => window.__grid.concluida, { timeout: 5000 }).catch(() => {})
  return page.evaluate(() => window.__grid.concluida)
}

console.log('== SELECIONAR: "múltiplos de 3" (7º ano) — o conteúdo vira regra jogável ==')
{
  const { page, errosJs } = await gera('7º ano', 'Identificar os múltiplos de 3')
  const esp = await page.evaluate(() => window.__fabricaEspinha)
  ok(esp.mecanica === 'selecionar' && esp.kc === 'multiplos-3', `pedagogo: mecânica=selecionar, kc=${esp.kc}`)
  const its = await posicoes(page)
  ok(its.length === 6, `6 itens rotulados no mapa (${its.length})`)
  ok(its.filter(i => i.ok).length === 3, 'há 3 corretos (múltiplos) e 3 distratores')
  // erro real primeiro: pega um item FORA da regra
  const errado = its.find(i => !i.ok)
  await irPara(page, errado.x, errado.y)
  await page.waitForTimeout(400)
  ok(await page.evaluate(() => window.__grid.erros) === 1, `pegar "${errado.rotulo}" (fora da regra) = ERRO real registrado`)
  await page.waitForTimeout(1100)
  const n = await page.evaluate(() => window.__grid.children.list.filter(o => o.texture && o.texture.key === 'mel' && o.active).length)
  ok(n === 6, `o item errado VOLTOU ao mapa (${n}/6) — tentar de novo sem punição`)
  // agora o caminho certo: só os múltiplos
  for (const it of its.filter(i => i.ok)) await irPara(page, it.x, it.y)
  ok(await page.evaluate(() => window.__grid.coletadosOk) === 3, 'coletou os 3 corretos (meta batida)')
  ok(await vencer(page), 'entregou e VENCEU a fase de conteúdo')
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['multiplos-3'] && prog['multiplos-3'].tentativas >= 2, `domínio registrado POR CONTEÚDO (kc multiplos-3: ${prog['multiplos-3']?.tentativas} obs.)`)
  ok(errosJs.length === 0, `zero erros de JS (${errosJs.length})`); errosJs.slice(0, 3).forEach(e => console.log('    ' + e))
  await page.close()
}

console.log('== MESMO MOTOR, OUTRO CONTEÚDO: "frações equivalentes a 1/2" ==')
{
  const { page } = await gera('7º ano', 'Reconhecer frações equivalentes')
  const esp = await page.evaluate(() => window.__fabricaEspinha)
  ok(esp.mecanica === 'selecionar' && esp.kc === 'fracoes-equivalentes', `kc mudou com o conteúdo (${esp.kc})`)
  const its = await posicoes(page)
  ok(its.some(i => i.rotulo === '2/4' && i.ok) && its.some(i => i.rotulo === '2/3' && !i.ok), 'itens são FRAÇÕES (2/4 certo, 2/3 distrator) — sem tocar no motor')
  for (const it of its.filter(i => i.ok)) await irPara(page, it.x, it.y)
  ok(await page.evaluate(() => window.__grid.coletadosOk) === 3, 'separou as 3 equivalentes')
  ok(await vencer(page), 'venceu com o conteúdo de frações')
  await page.close()
}

console.log('== ORDENAR: "ordem crescente" — fora de ordem = erro real ==')
{
  const { page } = await gera('4º ano', 'Colocar os números em ordem crescente')
  const esp = await page.evaluate(() => window.__fabricaEspinha)
  ok(esp.mecanica === 'ordenar' && esp.kc === 'ordem-crescente', `pedagogo: mecânica=ordenar, kc=${esp.kc}`)
  const its = await posicoes(page)
  ok(its.length === 4, `4 peças da sequência (${its.length})`)
  const porOrdem = [...its].sort((a, b) => (a.ordem ?? 0) - (b.ordem ?? 0))
  // erro real: tenta a 2ª peça antes da 1ª
  await irPara(page, porOrdem[1].x, porOrdem[1].y)
  await page.waitForTimeout(400)
  ok(await page.evaluate(() => window.__grid.erros) === 1, `pegar "${porOrdem[1].rotulo}" antes da hora = ERRO real`)
  ok(await page.evaluate(() => window.__grid.proxOrdem) === 1, 'a sequência NÃO avançou com o erro')
  await page.waitForTimeout(1100)
  // agora na ordem certa
  for (const it of porOrdem) await irPara(page, it.x, it.y)
  ok(await page.evaluate(() => window.__grid.proxOrdem) === 5, 'montou a sequência completa (4 peças na ordem)')
  ok(await vencer(page), 'entregou e venceu a fase de ORDENAR')
  const prog = await page.evaluate((c) => JSON.parse(localStorage.getItem(c) || '{}'), CHAVE)
  ok(prog['ordem-crescente'] && prog['ordem-crescente'].tentativas >= 2, 'domínio registrado no kc ordem-crescente')
  await page.close()
}

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
