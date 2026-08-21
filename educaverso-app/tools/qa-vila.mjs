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
// casa_b (330,58): a SEM porta — empurrar contra a casa_a faz o herói ENTRAR
// pela porta (é jogo, não bug) e o teste de colisão viraria mentira.
await page.evaluate(() => (window).__tp(314, 100))
await page.evaluate(() => (window).__anda(314, 20))
await page.waitForTimeout(2200)
const preso = await page.evaluate(() => (window).__vila.heroi.sp.y > 40 && (window).__vila.local === 'vila')
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
  const dx = h.x - faz.x, dy = h.y - faz.y
  const esperado = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 3 : 2) : (dy > 0 ? 0 : 1)
  return { dist: Math.hypot(dx, dy), frame: String(faz.frame.name), esperado: String(esperado) }
})
ok(npcState.dist > 7, `fazendeiro BLOQUEIA (dist ${npcState.dist.toFixed(1)}px, não sobrepôs)`)
ok(npcState.frame === npcState.esperado, `fazendeiro OLHOU pro herói (frame ${npcState.frame}, esperado ${npcState.esperado})`)

console.log('== TECLADO (PC da escola): setas e WASD ==')
await page.evaluate(() => (window).__tp(256, 200))
const tecla = async (key, nome, eixo, sinal) => {
  const antes = await page.evaluate(() => ({ x: (window).__vila.heroi.sp.x, y: (window).__vila.heroi.sp.y }))
  await page.keyboard.down(key)
  await page.waitForTimeout(500)
  const anim = await page.evaluate(() => { const s = (window).__vila.heroi.sp; return s.anims.currentAnim ? s.anims.currentAnim.key : '' })
  await page.keyboard.up(key)
  await page.waitForTimeout(250)
  const depois = await page.evaluate(() => ({ x: (window).__vila.heroi.sp.x, y: (window).__vila.heroi.sp.y }))
  const delta = eixo === 'x' ? depois.x - antes.x : depois.y - antes.y
  ok(delta * sinal > 10, `tecla ${nome} move (${delta.toFixed(0)}px)`)
  ok(anim.startsWith('heroi-anda-'), `tecla ${nome} anima (${anim})`)
}
await tecla('ArrowRight', 'SETA-direita', 'x', 1)
await tecla('ArrowLeft', 'SETA-esquerda', 'x', -1)
await tecla('KeyS', 'S(baixo)', 'y', 1)
await tecla('KeyW', 'W(cima)', 'y', -1)

console.log('== BOTÃO "VER TUDO" (cenário inteiro na tela) ==')
const heroiAntes = await page.evaluate(() => ({ x: (window).__vila.heroi.sp.x, y: (window).__vila.heroi.sp.y }))
await page.mouse.click(980, 112)                              // lupa (UI fixa)
await page.waitForTimeout(500)
const vista = await page.evaluate(() => ({ zoom: (window).__vila.cameras.main.zoom, modo: (window).__vila.vistaTudo }))
ok(vista.zoom === 2 && vista.modo === true, `VER TUDO liga (zoom ${vista.zoom})`)
const heroiDepois = await page.evaluate(() => ({ x: (window).__vila.heroi.sp.x, y: (window).__vila.heroi.sp.y }))
ok(Math.abs(heroiDepois.x - heroiAntes.x) + Math.abs(heroiDepois.y - heroiAntes.y) < 4, 'clicar no botão NÃO move o herói')
await page.screenshot({ path: OUT + '/qa_v_vertudo.png' })
await page.mouse.click(980, 112)
await page.waitForTimeout(500)
const volta = await page.evaluate(() => (window).__vila.cameras.main.zoom)
ok(volta === 3, `VER TUDO desliga (zoom ${volta})`)

console.log('== ENTRA NA CASINHA (porta -> fade -> interior) ==')
await page.evaluate(() => (window).__tp(90, 110))
await page.evaluate(() => (window).__anda(90, 56))            // pisa na SOLEIRA (vão da porta)
await espera(() => (window).__vila.local === 'casa', 15000).catch(() => {})
const dentro = await page.evaluate(() => (window).__vila.local)
ok(dentro === 'casa', 'herói ENTROU na casa (zona=' + dentro + ')')
await page.waitForTimeout(900)
await page.screenshot({ path: OUT + '/qa_v_casa.png' })
// os NPCs têm que FICAR na vila (bug pego no olho: worldBounds arrastava todos)
const npcsForam = await page.evaluate(() => (window).__vila.npcs.filter(n => n.sp.x > 520).length)
ok(npcsForam === 0, 'NPCs ficaram na vila (nenhum arrastado p/ dentro da casa)')

console.log('== SAI DA CASINHA (tapete -> fade -> vila) ==')
await page.evaluate(() => (window).__anda((window).__vila.heroi.sp.x, (window).__vila.heroi.sp.y + 30))
await espera(() => (window).__vila.local === 'vila', 15000).catch(() => {})
const fora = await page.evaluate(() => (window).__vila.local)
ok(fora === 'vila', 'herói VOLTOU pra vila (zona=' + fora + ')')
await page.waitForTimeout(600)

console.log('== PASSAR NA FRENTE DA PORTA NÃO ENTRA (regra do Marcos) ==')
await page.evaluate(() => (window).__tp(50, 84))
await page.evaluate(() => (window).__anda(150, 84))           // cruza na frente da casa_a
await page.waitForTimeout(1800)
const passou = await page.evaluate(() => (window).__vila.local)
ok(passou === 'vila', 'cruzou na frente da porta e NÃO entrou (zona=' + passou + ')')

console.log('== SEGUNDA CASINHA (depósito de pedra) ==')
await page.evaluate(() => (window).__tp(330, 86))
await page.evaluate(() => (window).__anda(330, 44))           // soleira da casa_b
await espera(() => (window).__vila.local === 'casa' && (window).__vila.salaAtual === 1, 15000).catch(() => {})
const s2 = await page.evaluate(() => ({ l: (window).__vila.local, s: (window).__vila.salaAtual }))
ok(s2.l === 'casa' && s2.s === 1, `entrou na SALA 2 (${s2.l}/${s2.s})`)
await page.waitForTimeout(700)
await page.screenshot({ path: OUT + '/qa_v_casa2.png' })
await page.evaluate(() => (window).__anda((window).__vila.heroi.sp.x, (window).__vila.heroi.sp.y + 40))
await espera(() => (window).__vila.local === 'vila', 15000).catch(() => {})
const v2 = await page.evaluate(() => (window).__vila.local)
ok(v2 === 'vila', 'saiu da sala 2 de volta pra vila (' + v2 + ')')

console.log('== TEXTURA FALTANDO (lição: piso2 esquecido no preload) ==')
const faltando = await page.evaluate(() => (window).__vila.children.list
  .filter(o => o.texture && (o.texture.key === '__MISSING' || o.texture.key === '__DEFAULT')).length)
ok(faltando === 0, `zero objetos com textura faltando (${faltando})`)

console.log('== ERROS ==')
const errosReais = erros.filter(e => !/favicon/.test(e))
ok(errosReais.length === 0, 'zero erros/404 (' + errosReais.length + ')')
errosReais.slice(0, 8).forEach(e => console.log('    ' + e))

await browser.close()
console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' falha(s) ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
