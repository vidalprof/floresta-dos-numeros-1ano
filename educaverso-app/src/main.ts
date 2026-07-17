// ============================================================================
// EducaVerso — App (Plano A) · Etapa 3: o mundo vivo explorável
// (a mecânica da Etapa 2 agora vive DENTRO do mundo — ver scenes/Ilha.ts)
// Config do Phaser em MODO ULTRALEVE para o PC real da escola
// (AMD FX-4300 · 3,5 GB RAM · Win7 · Chrome 109 / Firefox 106):
// 1024×768 FIT · 30 fps · sem antialias · low-power · texturas pintadas 1x.
// ============================================================================
import Phaser from 'phaser'
import { Ilha } from './scenes/Ilha'

new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: '#060c18',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 1024,
    height: 768
  },
  fps: { target: 30, forceSetTimeOut: true },
  render: { antialias: false, roundPixels: true, powerPreference: 'low-power' },
  scene: [Ilha]
})
