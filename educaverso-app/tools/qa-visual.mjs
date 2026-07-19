// AUDITOR DE VISUAL REGRESSION — compara a tela ATUAL com uma FOTO-BASE aprovada e
// ACUSA sozinho se algo saiu do lugar (objeto cortado, sumido, desalinhado). O diff é
// feito DENTRO do Chromium (canvas getImageData) — sem instalar pixelmatch/pngjs.
// 1ª execução: cria as baselines (tools/baseline_visual/*.png).
// Depois: se a tela mudar além do limiar, REPROVA e salva o diff em /tmp.
// Regra (da pesquisa): baseline é gerada no MESMO ambiente (este Linux/Chromium).
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
import fs from 'fs'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const BASE = process.env.URL_BASE || 'http://127.0.0.1:8190/index.html'
const DIR = new URL('./baseline_visual/', import.meta.url).pathname
const LIMIAR = Number(process.env.LIMIAR || 1.5)          // % de pixels diferentes tolerado
if (!fs.existsSync(DIR)) fs.mkdirSync(DIR, { recursive: true })

// cenas canônicas: (nome, como preparar antes da foto)
const CENAS = [
  { nome: 'f1_inicio', url: '?f1', prep: async () => {} },
  { nome: 'fgrid_externo', url: '?fgrid', prep: async () => {} },
  { nome: 'fgrid_interior', url: '?fgrid', prep: async (p) => {
    await p.evaluate(async () => { const g = window.__grid; await window.__gAnda(g.P('portaX'), g.P('portaY')) })
    await p.waitForFunction(() => window.__grid.local === 'casa', { timeout: 6000 }).catch(() => {})
    await p.waitForTimeout(900)
  } }
]

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const falhas = []; let criadas = 0
const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64')

for (const c of CENAS) {
  const page = await browser.newPage({ viewport: { width: 900, height: 700 } })
  await page.goto(BASE + c.url, { waitUntil: 'load' })
  await page.waitForFunction(() => (window.__grid && window.__grid.sys.isActive()) || (window.__fase1 && window.__fase1.sys.isActive()), { timeout: 30000 })
  await page.waitForTimeout(1000)
  await c.prep(page)
  const atualPath = '/tmp/vis_' + c.nome + '.png'
  await page.screenshot({ path: atualPath })
  const basePath = DIR + c.nome + '.png'
  if (!fs.existsSync(basePath)) { fs.copyFileSync(atualPath, basePath); criadas++; console.log('  📸 baseline criada: ' + c.nome); await page.close(); continue }
  // diff no Chromium (canvas)
  const r = await page.evaluate(async ([a, b]) => {
    const load = src => new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = src })
    const [ia, ib] = await Promise.all([load(a), load(b)])
    const w = Math.min(ia.width, ib.width), h = Math.min(ia.height, ib.height)
    const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const x = cv.getContext('2d')
    x.drawImage(ia, 0, 0); const da = x.getImageData(0, 0, w, h).data
    x.clearRect(0, 0, w, h); x.drawImage(ib, 0, 0); const db = x.getImageData(0, 0, w, h).data
    let dif = 0
    for (let i = 0; i < da.length; i += 4) { if (Math.abs(da[i] - db[i]) + Math.abs(da[i + 1] - db[i + 1]) + Math.abs(da[i + 2] - db[i + 2]) > 60) dif++ }
    return { dif, total: w * h }
  }, [b64(basePath), b64(atualPath)])
  const pct = (100 * r.dif / r.total)
  const passou = pct <= LIMIAR
  console.log((passou ? '  ✔ ' : '  ✘ ') + c.nome + ` — ${pct.toFixed(2)}% diferente (limiar ${LIMIAR}%)`)
  if (!passou) falhas.push(c.nome + ' (' + pct.toFixed(2) + '%)')
  await page.close()
}

await browser.close()
if (criadas) console.log('\n== ' + criadas + ' baseline(s) criada(s). Rode de novo p/ comparar. ==')
console.log(falhas.length ? '\n== REPROVADO (mudou o visual): ' + falhas.join(', ') + ' ==' : (criadas ? '' : '\n== APROVADO (visual estável) =='))
process.exit(falhas.length ? 1 : 0)
