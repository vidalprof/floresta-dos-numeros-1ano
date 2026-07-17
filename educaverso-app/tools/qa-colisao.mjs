import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg

const CHR = process.env.CHR
const URL = 'http://127.0.0.1:8142/?montador=1'

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const erros = []
page.on('pageerror', e => erros.push(String(e)))
await page.goto(URL, { waitUntil: 'load' })

// espera a cena Mundo existir e montar
await page.waitForFunction(() => {
  const j = window.jogo
  return j && j.scene && j.scene.getScene('Mundo') && j.scene.getScene('Mundo').corpo
}, { timeout: 15000 })

// TESTE: coloca o herói à ESQUERDA da pedra (700,700, com colisão) e manda ir
// pra DIREITA passando por ela (alvo 900). Se a colisão funciona, ele TRAVA
// antes de atravessar (corpo.x fica bem antes de 900).
const r = await page.evaluate(async () => {
  const s = window.jogo.scene.getScene('Mundo')
  s.estado = 'explora'
  s.corpo.body.reset(600, 700)
  s.alvo = { x: 900, y: 700 }
  const t0 = performance.now()
  await new Promise(res => {
    const iv = setInterval(() => { if (performance.now() - t0 > 1600) { clearInterval(iv); res() } }, 50)
  })
  return { x: Math.round(s.corpo.x), y: Math.round(s.corpo.y), obst: s.obst.getChildren().length }
})

const bloqueado = r.x < 690           // parou antes de entrar na pedra (colisor ~687)
console.log(JSON.stringify({ ...r, bloqueado, errosJS: erros }))
await browser.close()
process.exit(bloqueado && erros.length === 0 ? 0 : 1)
