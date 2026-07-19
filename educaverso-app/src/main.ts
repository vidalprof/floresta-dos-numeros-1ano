// ============================================================================
// EducaVerso — App (FÁBRICA DE MUNDOS, motor oficial Phaser + TS)
// Config em MODO ULTRALEVE para o PC real da escola
// (AMD FX-4300 · 3,5 GB RAM · Win7 · Chrome 109 / Firefox 106).
//
// Cenas:
//  - Mundo (PADRÃO): o MONTADOR v2 — lê uma AVENTURA (grafo de zonas) e arma
//    o mundo explorável. Padrão: "O Pomar do Byte". ?teste = aventura de teste.
//  - Ilha (?ilha): a cena artesanal antiga (referência histórica).
// ============================================================================
import Phaser from 'phaser'
import { Ilha } from './scenes/Ilha'
import { Mundo } from './motor/Mundo'
import { validarAventura } from './motor/aventura'
import { AVENTURA_POMAR } from './aventuras/pomar'
import { AVENTURA_TESTE } from './aventuras/teste'

const q = new URLSearchParams(location.search)
const usarIlha = q.has('ilha')

const jogo = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: '#060c18',
  // ENVELOP = PREENCHE a tela (sem tarjas pretas); recorta um pouco nas beiradas.
  scale: { mode: Phaser.Scale.ENVELOP, autoCenter: Phaser.Scale.CENTER_BOTH, width: 1024, height: 768 },
  fps: { target: 30, forceSetTimeOut: true },
  render: { antialias: true, roundPixels: false, powerPreference: 'low-power' },
  physics: { default: 'arcade', arcade: { gravity: { x: 0, y: 0 }, debug: false } },
  scene: usarIlha ? [Ilha] : []
})

if (!usarIlha) {
  // Zod valida os dados ANTES de montar (dado torto não monta).
  const aventura = validarAventura(q.has('teste') ? AVENTURA_TESTE : AVENTURA_POMAR)
  jogo.events.once('ready', () => {
    jogo.scene.add('Mundo', Mundo, true, { aventura })
  })
}

// expõe o jogo p/ o QA automático (Playwright dirige o mundo de verdade)
;(window as any).jogo = jogo
