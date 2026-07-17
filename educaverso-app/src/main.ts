import Phaser from 'phaser'

/* ============================================================================
 * EducaVerso — Plano A · passo de ARTE
 * A praia noturna bonita (a mesma estética do modelo leve) agora DENTRO do
 * Phaser: mundo explorável, personagem plantado que respira, fogueira/tocha
 * com brilho, vaga-lumes, palmeiras, lua, mar — e colisão com a água.
 * A "arte quadrada" era só placeholder da Etapa 1; isto é o visual de verdade.
 * ==========================================================================*/

const W = 1400
const H = 900

// poças d'água (obstáculos) — posições no mundo
const POCAS = [
  { x: 470, y: 650, rx: 74, ry: 34 },
  { x: 880, y: 540, rx: 62, ry: 30 },
  { x: 1160, y: 720, rx: 84, ry: 38 },
  { x: 300, y: 770, rx: 58, ry: 28 },
  { x: 720, y: 780, rx: 66, ry: 32 }
]

class Praia extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  private flame!: Phaser.GameObjects.Image

  constructor() { super('praia') }

  preload() {
    this.pintaCenario()
    this.pintaVerso()
    this.pintaFagulha('flame', ['#ff6a1f', '#ffb02e', '#ffe98a'])
    this.pintaGlow('vagalume', 'rgba(210,255,150,')
    this.pintaGlow('brilho', 'rgba(255,170,70,')
  }

  /* ---- pinta o cenário inteiro num canvas e usa como textura ---- */
  private pintaCenario() {
    const tex = this.textures.createCanvas('cenario', W, H)!
    const x = tex.getContext() as CanvasRenderingContext2D
    // céu
    let sky = x.createLinearGradient(0, 0, 0, H * 0.46)
    sky.addColorStop(0, '#0a1030'); sky.addColorStop(1, '#1b3a63')
    x.fillStyle = sky; x.fillRect(0, 0, W, H)
    // estrelas
    let s = 7; const rr = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff }
    for (let i = 0; i < 150; i++) { x.globalAlpha = 0.3 + rr() * 0.6; x.fillStyle = '#eaf2ff'; x.beginPath(); x.arc(rr() * W, rr() * H * 0.42, rr() * 1.4 + 0.3, 0, 7); x.fill() }
    x.globalAlpha = 1
    // lua
    const mx = 1150, my = 120
    let mg = x.createRadialGradient(mx, my, 8, mx, my, 150); mg.addColorStop(0, 'rgba(230,240,255,.5)'); mg.addColorStop(1, 'rgba(230,240,255,0)')
    x.fillStyle = mg; x.beginPath(); x.arc(mx, my, 150, 0, 7); x.fill()
    x.fillStyle = '#f2f6ff'; x.beginPath(); x.arc(mx, my, 40, 0, 7); x.fill()
    x.fillStyle = 'rgba(200,214,240,.5)'; x.beginPath(); x.arc(mx - 16, my - 10, 9, 0, 7); x.arc(mx + 14, my + 14, 12, 0, 7); x.fill()
    // mar
    const seaY = H * 0.40
    let sea = x.createLinearGradient(0, seaY, 0, seaY + 90); sea.addColorStop(0, '#12365f'); sea.addColorStop(1, '#0c2444')
    x.fillStyle = sea; x.fillRect(0, seaY, W, 100)
    // reflexo da lua
    x.save(); x.globalCompositeOperation = 'lighter'
    let rf = x.createLinearGradient(0, seaY, 0, seaY + 96); rf.addColorStop(0, 'rgba(215,230,255,.28)'); rf.addColorStop(1, 'rgba(215,230,255,0)')
    x.fillStyle = rf; x.fillRect(mx - 34, seaY, 68, 96); x.restore()
    // areia
    let sand = x.createLinearGradient(0, seaY + 40, 0, H); sand.addColorStop(0, '#2f2a24'); sand.addColorStop(1, '#201d18')
    x.fillStyle = sand; x.fillRect(0, seaY + 30, W, H)
    x.strokeStyle = 'rgba(200,225,255,.28)'; x.lineWidth = 3; x.beginPath(); x.moveTo(0, seaY + 40); x.lineTo(W, seaY + 40); x.stroke()
    // poças
    for (const p of POCAS) {
      let wg = x.createRadialGradient(p.x, p.y, 3, p.x, p.y, p.rx); wg.addColorStop(0, '#2f6f9e'); wg.addColorStop(1, '#173f60')
      x.fillStyle = wg; x.beginPath(); x.ellipse(p.x, p.y, p.rx, p.ry, 0, 0, 7); x.fill()
      x.strokeStyle = 'rgba(200,230,255,.3)'; x.lineWidth = 2; x.beginPath(); x.ellipse(p.x, p.y, p.rx, p.ry, 0, 0, 7); x.stroke()
    }
    // poças de luz da fogueira e tochas
    const luz = (px: number, py: number, rad: number, cor: string, al: number) => {
      x.save(); x.globalCompositeOperation = 'lighter'; let g = x.createRadialGradient(px, py, 4, px, py, rad)
      g.addColorStop(0, cor); g.addColorStop(1, 'rgba(0,0,0,0)'); x.globalAlpha = al; x.fillStyle = g; x.beginPath(); x.arc(px, py, rad, 0, 7); x.fill(); x.restore()
    }
    luz(700, 620, 300, 'rgba(255,150,60,.55)', 0.6)
    luz(180, 640, 170, 'rgba(255,180,80,.5)', 0.5)
    luz(1240, 600, 150, 'rgba(255,180,80,.45)', 0.5)
    // palmeiras
    this.palma(x, 150, 560); this.palma(x, 1270, 590)
    // tochas
    this.tochaBase(x, 180, 640); this.tochaBase(x, 1240, 600)
    // base da fogueira (lenha + pedras) — a chama é sprite animado por cima
    this.fogueiraBase(x, 700, 616)
    tex.refresh()
  }

  private palma(x: CanvasRenderingContext2D, bx: number, by: number) {
    x.fillStyle = '#2a2320'
    x.beginPath(); x.moveTo(bx - 9, by); x.quadraticCurveTo(bx - 22, by - 130, bx + 10, by - 210); x.lineTo(bx + 26, by - 208); x.quadraticCurveTo(bx - 3, by - 130, bx + 10, by); x.closePath(); x.fill()
    const tx = bx + 16, ty = by - 212, ang = [-2.7, -1.8, -0.8, 0.2, 1.2, 2.2]
    for (const a of ang) {
      const ex = tx + Math.cos(a) * 130, ey = ty + Math.sin(a) * 80 + 8, m1x = tx + Math.cos(a) * 66, m1y = ty + Math.sin(a) * 32 - 28
      x.fillStyle = '#233016'; x.beginPath(); x.moveTo(tx, ty); x.quadraticCurveTo(m1x, m1y, ex, ey); x.quadraticCurveTo(m1x + 8, m1y + 16, tx + 6, ty + 6); x.closePath(); x.fill()
      x.strokeStyle = 'rgba(150,180,220,.4)'; x.lineWidth = 2; x.beginPath(); x.moveTo(tx, ty); x.quadraticCurveTo(m1x, m1y, ex, ey); x.stroke()
    }
    x.fillStyle = '#3a2a1e'; for (let c = 0; c < 3; c++) { x.beginPath(); x.arc(tx - 6 + c * 7, ty + 8, 5, 0, 7); x.fill() }
  }
  private tochaBase(x: CanvasRenderingContext2D, lx: number, ly: number) {
    x.strokeStyle = '#3a2a1c'; x.lineWidth = 9; x.lineCap = 'round'; x.beginPath(); x.moveTo(lx, ly + 46); x.lineTo(lx - 7, ly - 50); x.stroke()
    const tx = lx - 7, ty = ly - 50; x.save(); x.globalCompositeOperation = 'lighter'
    x.fillStyle = '#ff7a1f'; x.beginPath(); x.moveTo(tx, ty - 30); x.quadraticCurveTo(tx - 12, ty - 6, tx, ty + 2); x.quadraticCurveTo(tx + 12, ty - 6, tx, ty - 30); x.fill()
    x.fillStyle = '#ffe08a'; x.beginPath(); x.moveTo(tx, ty - 18); x.quadraticCurveTo(tx - 5, ty - 4, tx, ty); x.quadraticCurveTo(tx + 5, ty - 4, tx, ty - 18); x.fill(); x.restore()
  }
  private fogueiraBase(x: CanvasRenderingContext2D, fx: number, fy: number) {
    x.fillStyle = '#3a3d4a'; for (let p = 0; p < 8; p++) { const a = p / 8 * 6.28; x.beginPath(); x.ellipse(fx + Math.cos(a) * 50, fy + Math.sin(a) * 22 + 10, 13, 8, 0, 0, 7); x.fill() }
    x.strokeStyle = '#3a2a1c'; x.lineWidth = 11; x.lineCap = 'round'; x.beginPath(); x.moveTo(fx - 28, fy + 14); x.lineTo(fx + 24, fy - 2); x.stroke(); x.beginPath(); x.moveTo(fx + 28, fy + 14); x.lineTo(fx - 24, fy - 2); x.stroke()
  }

  private pintaVerso() {
    const tex = this.textures.createCanvas('verso', 60, 68)!
    const x = tex.getContext() as CanvasRenderingContext2D
    const c = '#ff9b57', b = '#ffe6cf', olho = '#20305e', px = 30, py = 30
    x.fillStyle = 'rgba(0,0,0,.28)'; x.beginPath(); x.ellipse(px, py + 30, 22, 7, 0, 0, 7); x.fill()
    x.fillStyle = c; x.beginPath(); x.moveTo(px - 18, py - 16); x.lineTo(px - 22, py - 36); x.lineTo(px - 4, py - 26); x.closePath(); x.fill()
    x.beginPath(); x.moveTo(px + 18, py - 16); x.lineTo(px + 22, py - 36); x.lineTo(px + 4, py - 26); x.closePath(); x.fill()
    x.fillStyle = c; x.beginPath(); x.ellipse(px, py, 24, 28, 0, 0, 7); x.fill()
    x.fillStyle = b; x.beginPath(); x.ellipse(px, py + 8, 14, 14, 0, 0, 7); x.fill()
    x.fillStyle = '#fff'; x.beginPath(); x.arc(px - 8, py - 6, 6, 0, 7); x.arc(px + 8, py - 6, 6, 0, 7); x.fill()
    x.fillStyle = olho; x.beginPath(); x.arc(px - 8, py - 5, 3, 0, 7); x.arc(px + 8, py - 5, 3, 0, 7); x.fill()
    x.fillStyle = '#fff'; x.beginPath(); x.arc(px - 6, py - 7, 1.4, 0, 7); x.arc(px + 10, py - 7, 1.4, 0, 7); x.fill()
    x.fillStyle = 'rgba(255,143,176,.5)'; x.beginPath(); x.arc(px - 14, py + 3, 3, 0, 7); x.arc(px + 14, py + 3, 3, 0, 7); x.fill()
    x.strokeStyle = olho; x.lineWidth = 2; x.beginPath(); x.moveTo(px - 4, py + 5); x.quadraticCurveTo(px, py + 9, px + 4, py + 5); x.stroke()
    tex.refresh()
  }
  private pintaFagulha(key: string, cols: string[]) {
    const tex = this.textures.createCanvas(key, 40, 60)!
    const x = tex.getContext() as CanvasRenderingContext2D
    x.save(); (x as any).globalCompositeOperation = 'lighter'
    const ch = (w: number, h: number, col: string) => { x.fillStyle = col; x.beginPath(); x.moveTo(20, 8); x.quadraticCurveTo(20 - w, 40, 20 - w * 0.4, 54); x.quadraticCurveTo(20, 48, 20 + w * 0.4, 54); x.quadraticCurveTo(20 + w, 40, 20, 8 - h + 8); x.fill() }
    ch(16, 0, cols[0]); ch(11, 6, cols[1]); ch(6, 12, cols[2]); x.restore(); tex.refresh()
  }
  private pintaGlow(key: string, rgbaPrefix: string) {
    const tex = this.textures.createCanvas(key, 24, 24)!
    const x = tex.getContext() as CanvasRenderingContext2D
    const g = x.createRadialGradient(12, 12, 0, 12, 12, 12); g.addColorStop(0, rgbaPrefix + '0.95)'); g.addColorStop(1, rgbaPrefix + '0)')
    x.fillStyle = g; x.fillRect(0, 0, 24, 24); tex.refresh()
  }

  create() {
    this.add.image(0, 0, 'cenario').setOrigin(0)

    // água = colisão
    const agua = this.physics.add.staticGroup()
    for (const p of POCAS) {
      const r: any = this.add.rectangle(p.x, p.y, p.rx * 1.6, p.ry * 1.6)
      r.setVisible(false); this.physics.add.existing(r, true); agua.add(r)
    }

    // chama da fogueira (sprite animado por cima da base)
    this.flame = this.add.image(700, 590, 'flame').setDepth(20)
    this.tweens.add({ targets: this.flame, scaleY: 1.18, scaleX: 0.9, duration: 140, yoyo: true, repeat: -1, ease: 'Sine.inOut' })

    // vaga-lumes (partículas suaves)
    for (let i = 0; i < 10; i++) {
      const fx = 200 + Math.random() * 1000, fy = 480 + Math.random() * 320
      const vl = this.add.image(fx, fy, 'vagalume').setScale(0.8).setDepth(15)
      this.tweens.add({ targets: vl, x: fx + (Math.random() * 80 - 40), y: fy + (Math.random() * 60 - 30), alpha: 0.3, duration: 1500 + Math.random() * 1500, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
    }

    // personagem
    this.player = this.physics.add.sprite(360, 700, 'verso').setDepth(30)
    this.player.setCollideWorldBounds(true)
    this.player.body!.setSize(30, 26)
    this.physics.add.collider(this.player, agua)

    // câmera segue
    this.physics.world.setBounds(0, 0, W, H)
    this.cameras.main.setBounds(0, 0, W, H)
    this.cameras.main.startFollow(this.player, true, 0.12, 0.12)

    this.cursors = this.input.keyboard!.createCursorKeys()

    // HUD
    this.add.text(12, 12, '🧭  Use as SETAS para explorar a ilha', {
      fontFamily: 'Arial', fontSize: '18px', color: '#eaf1ff'
    }).setPadding(9, 6, 9, 6).setScrollFactor(0).setDepth(100).setBackgroundColor('rgba(8,16,32,0.55)')
  }

  update() {
    const s = 200
    const body = this.player.body as Phaser.Physics.Arcade.Body
    body.setVelocity(0)
    if (this.cursors.left.isDown) { body.setVelocityX(-s); this.player.setFlipX(true) }
    else if (this.cursors.right.isDown) { body.setVelocityX(s); this.player.setFlipX(false) }
    if (this.cursors.up.isDown) body.setVelocityY(-s)
    else if (this.cursors.down.isDown) body.setVelocityY(s)
    body.velocity.normalize().scale(s)
    // respiração (sem flutuar)
    const t = this.time.now * 0.004
    this.player.setScale(1, 1 + Math.sin(t) * 0.03)
  }
}

// eslint-disable-next-line no-new
new Phaser.Game({
  type: Phaser.AUTO,                         // WebGL se houver; senão Canvas
  parent: 'game',
  backgroundColor: '#0a1226',
  // MODO LEVE p/ PC velho: resolução interna travada em 1024x768 (não renderiza
  // a tela cheia gigante) + escala pra caber na janela.
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, width: 1024, height: 768 },
  fps: { target: 30, forceSetTimeOut: true },  // 30 FPS = metade do trabalho, mais fluido em máquina fraca
  render: { antialias: false, roundPixels: true, powerPreference: 'low-power', pixelArt: false },
  physics: { default: 'arcade', arcade: { debug: false } },
  scene: [Praia]
})
