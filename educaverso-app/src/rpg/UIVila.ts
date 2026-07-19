// ============================================================================
// UI da Vila — cena SEPARADA (sem zoom): botões fixos no canto sup. direito.
//   ◱ tela cheia (Fullscreen API via gesto)   🔍- ver o cenário TODO / voltar
// Ícones desenhados em pixel (sem texto/emoji — lei: criança pequena não lê).
// ============================================================================
import Phaser from 'phaser'
import type { VilaViva } from './VilaViva'

export class UIVila extends Phaser.Scene {
  constructor () { super({ key: 'UIVila' }) }

  create (): void {
    const vila = this.registry.get('vila') as VilaViva

    const botao = (x: number, y: number, desenha: (g: Phaser.GameObjects.Graphics) => void, cb: () => void): void => {
      const c = this.add.container(x, y).setDepth(10)
      const bg = this.add.circle(0, 0, 26, 0x0e0c12, 0.55).setStrokeStyle(3, 0xffffff, 0.85)
      const g = this.add.graphics()
      desenha(g)
      c.add([bg, g])
      bg.setInteractive({ useHandCursor: true })
      bg.on('pointerdown', (p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation()
        this.tweens.add({ targets: c, scale: 0.86, duration: 70, yoyo: true })
        cb()
      })
    }

    // ◱ TELA CHEIA (cantoneiras)
    botao(1024 - 44, 44, g => {
      g.lineStyle(4, 0xffffff, 0.95)
      const s = 9, o = 13
      g.beginPath()
      g.moveTo(-o, -o + s); g.lineTo(-o, -o); g.lineTo(-o + s, -o)
      g.moveTo(o - s, -o); g.lineTo(o, -o); g.lineTo(o, -o + s)
      g.moveTo(o, o - s); g.lineTo(o, o); g.lineTo(o - s, o)
      g.moveTo(-o + s, o); g.lineTo(-o, o); g.lineTo(-o, o - s)
      g.strokePath()
    }, () => {
      // gesto do usuário → pode pedir fullscreen; alguns aparelhos negam (ok)
      if (this.scale.isFullscreen) this.scale.stopFullscreen()
      else { try { this.scale.startFullscreen() } catch { /* aparelho não deixa */ } }
    })

    // 🔍 VER TUDO (lupa com menos) / voltar ao zoom normal
    botao(1024 - 44, 112, g => {
      g.lineStyle(4, 0xffffff, 0.95)
      g.strokeCircle(-3, -3, 10)
      g.beginPath(); g.moveTo(5, 5); g.lineTo(13, 13); g.strokePath()
      g.beginPath(); g.moveTo(-8, -3); g.lineTo(2, -3); g.strokePath()
    }, () => vila.alternaVista())
  }
}
