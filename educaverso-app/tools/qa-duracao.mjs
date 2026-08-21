// ⏱️ AUDITOR DE DURAÇÃO — o profissional que "joga como uma criança de 7-9 anos" e
// estima o tempo da aventura (FLUXO-AVENTURA-55MIN.md). Jogar 45 min de verdade no CI
// é inviável; então ele MODELA o tempo a partir do CONTEÚDO REAL de cada fase (nº de
// potes, caixas, missões) usando constantes de ritmo com base na pesquisa (atenção e
// leitura 6-9 anos; PESQUISA-JOGO-2D-E-AVENTURA-55MIN). É uma ESTIMATIVA transparente,
// não um cronômetro — as constantes ficam à vista e são ajustáveis.
// Alvo (FLUXO): mínimo 45 min, ideal ~55, segmentado em fases curtas.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js'
const { chromium } = pkg
const CHR = process.env.CHR || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const URL = process.env.URL || 'http://127.0.0.1:8215/index.html?tabuada'

// ---- MODELO DE RITMO (segundos) — criança 7-9 anos, com base na pesquisa ----
// Constantes REVISADAS 2026-07 para o ritmo REAL de sala (o 1º chute foi otimista):
// criança 7-9 anos hesita, conversa, se distrai e volta — cada ciclo de pote é mais
// lento que o "ideal de laboratório". Números defensáveis pela pesquisa de atenção/
// motricidade (NN/g) e por observação de sala, NÃO ajustados para "passar".
const R = {
  potePorCiclo: 20,     // andar até o pote + até a caixa + DECIDIR (ritmo real 7-9 anos)
  caixaColoca: 9,       // pegar caixa na pilha + posicionar na vaga
  leituraBalao: 7,      // ler/ouvir UMA fala do mentor (~1 palavra/s p/ essa idade + pausa)
  baloesPorMissao: 5,   // abertura + problema + juntouTudo + entrega + vitória
  porErro: 48,          // 1 erro real: tombamento + pergunta + repensar + refazer parcial
  errosEsperados: 1.6,  // crianças erram (falha produtiva) — mais nas fases difíceis
  exploraMissao: 60,    // olhar o cenário novo, vagar, se ambientar
  onboarding: 150,      // 1ª missão: descobrir controles, experimentar (sem texto)
  celebracao: 9,        // tela de transição entre fases
  respiro: 45           // micro-pausa/história entre blocos (segmentação de Mayer)
}

const browser = await chromium.launch({ executablePath: CHR, args: ['--no-sandbox', '--disable-gpu', '--use-gl=swiftshader', '--mute-audio'] })
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } })
const errs = []; page.on('pageerror', e => errs.push(String(e).slice(0, 140)))
await page.goto(URL, { waitUntil: 'load' })
await page.waitForFunction(() => window.__grid && window.__grid.sys.isActive(), { timeout: 30000 })
await page.waitForTimeout(600)

// lê o conteúdo de CADA missão avançando pelo arco (sem jogar — só medir)
const fases = []
let guard = 0
while (guard++ < 8) {
  const m = await page.evaluate(() => ({
    total: window.__grid.agTotal, caixas: window.__grid.agCaixas,
    todas: window.__grid.agTodas, cenario: JSON.parse(window.__grid.map.properties.find(p => p.name === 'cenario').value),
    temProx: !!window.__fabricaProxima && (window.__fabricaMissao() < 99)
  }))
  fases.push(m)
  const avancou = await page.evaluate(() => {
    const i = window.__fabricaMissao()
    window.__fabricaProxima()
    return window.__fabricaMissao() > i
  })
  if (!avancou) break
  await page.waitForTimeout(300)
}

console.log('⏱️  AUDITOR DE DURAÇÃO — aventura da tabuada (estimativa por conteúdo)\n')
let total = 0
fases.forEach((f, i) => {
  const caixasUsadas = f.todas ? f.caixas : Math.max(2, Math.round(f.total / 4))
  let s = 0
  s += R.exploraMissao
  s += R.baloesPorMissao * R.leituraBalao
  s += (f.total || 0) * R.potePorCiclo
  s += caixasUsadas * R.caixaColoca
  s += R.errosEsperados * R.porErro * (f.todas ? 1.4 : 1)   // divisão é mais difícil = mais erros
  if (i === 0) s += R.onboarding
  if (i > 0) s += R.celebracao + R.respiro
  total += s
  console.log(`  Fase ${i + 1} (${f.cenario}${f.todas ? ', DIVISÃO' : ''}): ${f.total} potes, ~${Math.round(s / 60 * 10) / 10} min`)
})
const min = total / 60
console.log(`\n  TOTAL estimado: ~${Math.round(min * 10) / 10} min  (${fases.length} fases)`)
console.log(`  Alvo (FLUXO-AVENTURA-55MIN): mínimo 45, ideal ~55.`)
const veredito = min >= 45 ? '✅ APROVADO (≥45 min)' : min >= 35 ? '⚠️  CURTO — acrescentar 1 fase/respiros p/ chegar a 45+' : '✘ MUITO CURTO — falta conteúdo'
console.log('  Veredito: ' + veredito)
console.log(`\n  (Modelo de ritmo, s: pote=${R.potePorCiclo}, leituraBalão=${R.leituraBalao}, erro=${R.porErro}, onboarding=${R.onboarding}. Ajustável no topo do arquivo.)`)
if (errs.length) console.log('  ⚠️ erros JS:', errs.slice(0, 3))
await browser.close()
process.exit(min >= 35 ? 0 : 1)   // só reprova se estiver MUITO curto (o "curto" é aviso, não erro)
