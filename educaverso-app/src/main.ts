// ============================================================================
// EducaVerso — App (Plano A)
// Config do Phaser em MODO ULTRALEVE para o PC real da escola
// (AMD FX-4300 · 3,5 GB RAM · Win7 · Chrome 109 / Firefox 106).
//
// Duas cenas:
//  - Ilha (padrão): a cena artesanal da Etapa 3 (bonita, atividade única).
//  - Mundo (?montador): o MONTADOR — lê uma AVENTURA (dados) e arma o mundo.
//    É a ferramenta reaproveitável. Provada com a AVENTURA_TESTE.
// ============================================================================
import Phaser from 'phaser'
import { Ilha } from './scenes/Ilha'
import { Mundo } from './motor/Mundo'
import { validarAventura } from './motor/aventura'
import { AVENTURA_TESTE } from './aventuras/teste'

const usarMontador = new URLSearchParams(location.search).has('montador')

const jogo = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: '#060c18',
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, width: 1024, height: 768 },
  fps: { target: 30, forceSetTimeOut: true },
  render: { antialias: false, roundPixels: true, powerPreference: 'low-power' },
  physics: { default: 'arcade', arcade: { gravity: { x: 0, y: 0 }, debug: false } },
  scene: usarMontador ? [] : [Ilha]
})

if (usarMontador) {
  // Zod valida os dados ANTES de montar (dado torto não monta).
  const aventura = validarAventura(AVENTURA_TESTE)
  jogo.events.once('ready', () => {
    jogo.scene.add('Mundo', Mundo, true, { aventura })
  })
}
