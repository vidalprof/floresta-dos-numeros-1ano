import Phaser from 'phaser'

/* ============================================================================
 * EducaVerso — Plano A · Etapa 1 (Núcleo técnico)
 * Personagem andando num mapa vivo, câmera seguindo, colisão com a água.
 * Phaser + TypeScript + Vite. Projeto SEPARADO do modelo leve atual.
 * ==========================================================================*/

const TILE = 48
// 0 = chão (anda) · 1 = água (bloqueia)
const MAPA: number[][] = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
  [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
  [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
  [0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0],
  [0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
const COLS = MAPA[0].length
const ROWS = MAPA.length
const W = COLS * TILE
const H = ROWS * TILE

class Mundo extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys

  constructor() { super('mundo') }

  preload() {
    this.tile('grama', 0x2f7d46, 0x276b3c)
    this.tile('agua', 0x2f6f9e, 0x24597f)

    // personagem "Verso" (círculos, sem arquivo de imagem)
    const g = this.add.graphics()
    g.fillStyle(0x000000, 0.22); g.fillEllipse(20, 40, 30, 9)
    g.fillStyle(0xff9b57, 1); g.fillEllipse(20, 22, 34, 38)
    g.fillStyle(0xffe6cf, 1); g.fillEllipse(20, 28, 18, 18)
    g.fillStyle(0xffffff, 1); g.fillCircle(13, 16, 5); g.fillCircle(27, 16, 5)
    g.fillStyle(0x20305e, 1); g.fillCircle(13, 16, 2.4); g.fillCircle(27, 16, 2.4)
    g.generateTexture('verso', 40, 46); g.destroy()

    // passarinho (vida)
    const b = this.add.graphics()
    b.lineStyle(3, 0xffffff, 0.9)
    b.beginPath(); b.arc(6, 6, 6, Math.PI, 0); b.strokePath()
    b.beginPath(); b.arc(16, 6, 6, Math.PI, 0); b.strokePath()
    b.generateTexture('passaro', 22, 12); b.destroy()
  }

  private tile(key: string, c1: number, c2: number) {
    const g = this.add.graphics()
    g.fillStyle(c1, 1); g.fillRect(0, 0, TILE, TILE)
    g.lineStyle(1, c2, 0.6); g.strokeRect(0, 0, TILE, TILE)
    g.generateTexture(key, TILE, TILE); g.destroy()
  }

  create() {
    // chão (tilesprite de grama cobrindo o mundo)
    this.add.tileSprite(0, 0, W, H, 'grama').setOrigin(0)

    // água = obstáculos com corpo estático
    const agua = this.physics.add.staticGroup()
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        if (MAPA[r][c] === 1) {
          agua.create(c * TILE + TILE / 2, r * TILE + TILE / 2, 'agua')
        }
      }
    }

    // personagem
    this.player = this.physics.add.sprite(TILE * 1.5, TILE * 1.5, 'verso')
    this.player.setCollideWorldBounds(true)
    this.player.body!.setSize(26, 24)
    this.physics.add.collider(this.player, agua)

    // câmera segue o personagem, limitada ao mundo
    this.physics.world.setBounds(0, 0, W, H)
    this.cameras.main.setBounds(0, 0, W, H)
    this.cameras.main.startFollow(this.player, true, 0.12, 0.12)
    this.cameras.main.setBackgroundColor('#12305a')

    // teclado
    this.cursors = this.input.keyboard!.createCursorKeys()

    // VIDA: um passarinho cruzando o céu, de tempos em tempos
    const bird = this.add.image(-30, 70, 'passaro').setDepth(50)
    this.tweens.add({ targets: bird, x: W + 40, duration: 9000, repeat: -1, repeatDelay: 3000 })
    this.tweens.add({ targets: bird, y: 90, duration: 1400, yoyo: true, repeat: -1, ease: 'Sine.inOut' })

    // HUD fixo
    this.add.text(12, 12, '🧭  Use as SETAS para andar', {
      fontFamily: 'Arial', fontSize: '18px', color: '#eaf1ff'
    }).setPadding(8, 6, 8, 6).setScrollFactor(0).setDepth(100)
      .setBackgroundColor('rgba(8,16,32,0.55)')

    this.add.text(12, H - 0, '', {}) // noop p/ manter tipos felizes
  }

  update() {
    const s = 190
    const body = this.player.body as Phaser.Physics.Arcade.Body
    body.setVelocity(0)
    if (this.cursors.left.isDown) body.setVelocityX(-s)
    else if (this.cursors.right.isDown) body.setVelocityX(s)
    if (this.cursors.up.isDown) body.setVelocityY(-s)
    else if (this.cursors.down.isDown) body.setVelocityY(s)
    body.velocity.normalize().scale(s) // diagonal não fica mais rápido
    // respiração leve (escala) — vida sem flutuar
    const t = this.time.now * 0.004
    this.player.setScale(1, 1 + Math.sin(t) * 0.03)
  }
}

// eslint-disable-next-line no-new
new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: '#0b1226',
  pixelArt: false,
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: '100%',
    height: '100%'
  },
  physics: { default: 'arcade', arcade: { debug: false } },
  scene: [Mundo]
})
