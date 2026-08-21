// ============================================================================
// FASES DEMO — prova viva do FORMATO que o Marcos escolheu (opção 1):
// fase emoldurada -> RESOLVE algo -> o PORTÃO abre -> próxima fase.
// SEM pedagogia ainda (isso pluga depois): aqui o "resolver" é pegar a chave.
// É o esqueleto onde a sequência didática vai encaixar. Robô-QA prova o fluxo.
// ============================================================================
import Phaser from 'phaser'

const T = 16
// cada fase = uma área emoldurada (em tiles). Tudo cabe na tela (zoom 3).
const FASES = [
  { grama: 245, w: 18, h: 12, cor: 0xcaa06a },     // fase 1 — pradaria
  { grama: 245, w: 18, h: 12, cor: 0x8fae6b }      // fase 2 — chegada
]

interface Andante { sp: Phaser.Physics.Arcade.Sprite, sombra: Phaser.GameObjects.Image }

export class FasesDemo extends Phaser.Scene {
  private heroi!: Andante
  private alvo: Phaser.Math.Vector2 | null = null
  private dir = 'baixo'
  private curs?: Phaser.Types.Input.Keyboard.CursorKeys
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
  fase = 0                       // fase atual (QA lê)
  temChave = false               // resolveu? (QA lê)
  faseW = 0; faseH = 0           // dimensões da fase em px (QA mira o centro certo)
  private trocando = false
  private portao?: Phaser.GameObjects.Image
  private portaoBloco?: Phaser.GameObjects.Rectangle
  private chaveImg?: Phaser.GameObjects.Image
  private aviso!: Phaser.GameObjects.Text

  constructor () { super({ key: 'FasesDemo' }) }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    this.load.spritesheet('heroi', b + 'heroi.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('paredes', b + 'paredes.png', { frameWidth: T, frameHeight: T })
    this.load.image('sombra', b + 'sombra.png')
    this.load.image('chave', b + 'chave.png')
    this.load.image('pedras2', b + 'pedras.png')     // barreira (pedras limpas do pack)
  }

  create (): void {
    const dirCol: Record<string, number> = { baixo: 0, cima: 1, esq: 2, dir: 3 }
    for (const [dnome, col] of Object.entries(dirCol)) {
      this.anims.create({ key: 'heroi-anda-' + dnome, frames: [0, 1, 2, 3].map(r => ({ key: 'heroi', frame: r * 4 + col })), frameRate: 8, repeat: -1 })
    }
    const sombra = this.add.image(0, 0, 'sombra').setAlpha(0.6).setDepth(4.5)
    const sp = this.physics.add.sprite(0, 0, 'heroi', 0).setDepth(5)
    ;(sp.body as Phaser.Physics.Arcade.Body).setSize(10, 8).setOffset(3, 8)
    this.heroi = { sp, sombra }

    this.aviso = this.add.text(0, 0, '', { fontFamily: 'sans-serif', fontSize: '13px', color: '#fff', backgroundColor: '#0008', padding: { x: 6, y: 3 } })
      .setScrollFactor(0).setDepth(20000).setPosition(12, 12)

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY) })
    if (this.input.keyboard) {
      this.curs = this.input.keyboard.createCursorKeys()
      this.wasd = this.input.keyboard.addKeys('W,A,S,D') as Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
    }

    this.montaFase(0)
    ;(window as any).__fases = this
    ;(window as any).__tpF = (x: number, y: number) => { this.heroi.sp.setPosition(x, y); this.alvo = null }
    ;(window as any).__andaF = (x: number, y: number) => { this.alvo = new Phaser.Math.Vector2(x, y) }
  }

  private montaFase (i: number): void {
    // limpa a fase anterior (menos herói/sombra/aviso/câmera)
    this.children.list.slice().forEach(o => {
      if (o === this.heroi.sp || o === this.heroi.sombra || o === this.aviso) return
      o.destroy()
    })
    this.physics.world.colliders.destroy()
    this.fase = i
    this.temChave = false
    const f = FASES[i]
    const W = f.w * T, H = f.h * T
    this.faseW = W; this.faseH = H

    // chão
    const grade: number[][] = Array.from({ length: f.h }, () => new Array(f.w).fill(f.grama))
    const mp = this.make.tilemap({ data: grade, tileWidth: T, tileHeight: T })
    mp.createLayer(0, mp.addTilesetImage('chao')!, 0, 0)!.setDepth(0)

    // MOLDURA (borda legal) — muro do autor em volta, com abertura no topo (a saída)
    const solidos = this.physics.add.staticGroup()
    const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44 }
    const parede = (ix: number, iy: number, fr: number) => this.add.image(ix * T + 8, iy * T + 8, 'paredes', fr).setDepth(iy * T + 4)
    // abertura de 2 tiles no CENTRO do muro de cima (centraliza com o herói,
    // e passagem larga = fácil de atravessar — não trava na quina)
    const sA = (f.w >> 1) - 1, sB = f.w >> 1                   // colunas abertas
    const saidaCx = f.w / 2 * T                                // centro exato da abertura
    for (let ix = 0; ix < f.w; ix++) {
      if (ix !== sA && ix !== sB) parede(ix, 0, ix === 0 ? PAR.TL : ix === f.w - 1 ? PAR.TR : PAR.T)
      parede(ix, f.h - 1, ix === 0 ? PAR.BL : ix === f.w - 1 ? PAR.BR : PAR.B)
    }
    for (let iy = 1; iy < f.h - 1; iy++) { parede(0, iy, PAR.L); parede(f.w - 1, iy, PAR.R) }
    // colisão da moldura (topo em 2 pedaços deixando a abertura central)
    const wEsq = sA * T
    solidos.add(this.fisico(wEsq / 2, 8, wEsq, 16))
    const wDir = (f.w - sB - 1) * T
    solidos.add(this.fisico((sB + 1) * T + wDir / 2, 8, wDir, 16))
    solidos.add(this.fisico(W / 2, H - 8, W, 16))
    solidos.add(this.fisico(8, H / 2, 16, H))
    solidos.add(this.fisico(W - 8, H / 2, 16, H))

    this.heroi.sp.setPosition(W / 2, H - 40)
    this.physics.add.collider(this.heroi.sp, solidos)
    this.cameras.main.setBounds(0, 0, W, H).setZoom(3).centerOn(W / 2, H / 2)

    if (i < FASES.length - 1) {
      // BARREIRA de pedras fechando a abertura (só some ao resolver) + a CHAVE
      this.portao = this.add.image(saidaCx, 22, 'pedras2').setOrigin(0.5, 0.5).setDepth(9000)
      this.portaoBloco = this.fisico(saidaCx, 12, 32, 20)
      solidos.add(this.portaoBloco)
      this.chaveImg = this.add.image(W / 2, H / 2, 'chave').setDepth(H / 2)
      const zc = this.fisico(W / 2, H / 2, 18, 18)
      this.physics.add.overlap(this.heroi.sp, zc, () => this.pegaChave(zc))
      this.aviso.setText('Fase ' + (i + 1) + ' — pegue a chave para abrir o portão')
      // zona de saída (só passa com o portão aberto)
      const zs = this.fisico(saidaCx, 4, 28, 12)
      this.physics.add.overlap(this.heroi.sp, zs, () => { if (this.temChave && !this.trocando) this.proximaFase() })
    } else {
      this.aviso.setText('Fase ' + (i + 1) + ' — você chegou! 🏁'.replace('🏁', ''))
      this.aviso.setText('Fase ' + (i + 1) + ' — voce chegou!')
    }
  }

  private fisico (x: number, y: number, w: number, h: number): Phaser.GameObjects.Rectangle {
    const r = this.add.rectangle(x, y, w, h)
    this.physics.add.existing(r, true)
    return r
  }

  private pegaChave (zc: Phaser.GameObjects.Rectangle): void {
    if (this.temChave) return
    this.temChave = true
    zc.destroy()
    this.chaveImg?.destroy()
    // o mundo MUDA: o portão abre (some o bloqueio) com um brilho
    if (this.portaoBloco) { (this.portaoBloco.body as Phaser.Physics.Arcade.StaticBody).enable = false; this.portaoBloco.destroy() }
    if (this.portao) this.tweens.add({ targets: this.portao, alpha: 0, y: this.portao.y - 6, duration: 300, onComplete: () => this.portao?.destroy() })
    this.aviso.setText('Portão aberto! Suba pela passagem →')
  }

  private proximaFase (): void {
    this.trocando = true
    this.alvo = null; this.heroi.sp.setVelocity(0, 0)
    this.cameras.main.fadeOut(260, 14, 12, 18)
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.montaFase(this.fase + 1)
      this.cameras.main.fadeIn(260, 14, 12, 18)
      this.time.delayedCall(400, () => { this.trocando = false })
    })
  }

  update (): void {
    const h = this.heroi, VEL = 70
    let kx = 0, ky = 0
    if (this.curs?.left.isDown || this.wasd?.A.isDown) kx -= 1
    if (this.curs?.right.isDown || this.wasd?.D.isDown) kx += 1
    if (this.curs?.up.isDown || this.wasd?.W.isDown) ky -= 1
    if (this.curs?.down.isDown || this.wasd?.S.isDown) ky += 1
    if (kx || ky) { this.alvo = null; const n = Math.hypot(kx, ky); h.sp.setVelocity(kx / n * VEL, ky / n * VEL) }
    else if (this.alvo) {
      const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.alvo.x, this.alvo.y)
      if (d < 4) { this.alvo = null; h.sp.setVelocity(0, 0) } else this.physics.moveTo(h.sp, this.alvo.x, this.alvo.y, VEL)
    } else h.sp.setVelocity(0, 0)

    const vx = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.x
    const vy = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.y
    if (Math.abs(vx) + Math.abs(vy) > 4) {
      this.dir = Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 'dir' : 'esq') : (vy > 0 ? 'baixo' : 'cima')
      h.sp.play('heroi-anda-' + this.dir, true)
    } else if (h.sp.anims.isPlaying) { h.sp.stop(); h.sp.setFrame(({ baixo: 0, cima: 1, esq: 2, dir: 3 } as Record<string, number>)[this.dir]) }
    h.sp.setDepth(h.sp.y)
    h.sombra.setPosition(h.sp.x + 1, h.sp.y + 7).setDepth(h.sp.y - 0.5)
  }
}
