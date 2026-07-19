// ============================================================================
// VILA VIVA — 1ª cena do MOTOR RPG top-down (identidade Ninja Adventure, CC0).
// Prova publicável: tilemap de chão + props com colisão + herói tap-to-move com
// caminhada 4 direções frame a frame + NPCs NEUTROS vivos (regra do Marcos:
// SEM tema ninja) + cachorrinho + sombras. PC velho: pixelArt, 30fps, leve.
// QA: window.__vila expõe estado p/ o robô (Playwright) dirigir de verdade.
// ============================================================================
import Phaser from 'phaser'

const T = 16                       // tile do pack (16px)
const MAPA_W = 32, MAPA_H = 20     // 512x320 px de mundo

// paleta do chão (tileset_floor.png, 22 colunas; bloco verde começa na linha 7)
const G = (col: number, lin: number) => (7 + lin) * 22 + col
const GRAMA = G(3, 4)              // grama lisa que CASA com a borda do blob (auditada)
const BLOB = [                     // clareira de terra 3x3 com borda orgânica
  [G(0, 0), G(1, 0), G(2, 0)],
  [G(0, 1), G(1, 1), G(2, 1)],
  [G(0, 2), G(1, 2), G(2, 2)]
]

// props do tileset grande (mundo.png) — caixas AUDITADAS por segmentação
const PROPS: Record<string, [number, number, number, number]> = {
  casa_a:  [0, 0, 64, 48],
  casa_b:  [64, 0, 64, 48],
  torii:   [7, 51, 34, 29],
  cerca:   [85, 71, 39, 22],
  varal:   [128, 73, 32, 21],
  pedras:  [225, 147, 61, 44],
  toco:    [97, 293, 30, 23],
  arvore:  [0, 160, 32, 32],
  carroca: [82, 131, 27, 27],
  feira:   [116, 130, 27, 28]
}

interface Andante {
  sp: Phaser.Physics.Arcade.Sprite
  sombra: Phaser.GameObjects.Image
  chave: string
}

export class VilaViva extends Phaser.Scene {
  private heroi!: Andante
  private npcs: Andante[] = []
  private alvo: Phaser.Math.Vector2 | null = null
  private dir = 'baixo'

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    for (const ch of ['heroi', 'fazendeiro', 'menina', 'avo']) {
      this.load.spritesheet(ch, b + ch + '.png', { frameWidth: T, frameHeight: T })
    }
    this.load.spritesheet('dog', b + 'dog.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.image('mundo', b + 'mundo.png')
    this.load.image('sombra', b + 'sombra.png')
  }

  create (): void {
    // ---- frames nomeados dos props (recortes do tileset grande) ----
    const tex = this.textures.get('mundo')
    for (const [nome, [x, y, w, h]] of Object.entries(PROPS)) tex.add(nome, 0, x, y, w, h)

    // ---- CHÃO (tilemap de verdade) ----
    const grade: number[][] = []
    for (let y = 0; y < MAPA_H; y++) grade.push(new Array(MAPA_W).fill(GRAMA))
    const bx = 13, by = 8                          // clareira central
    for (let dy = 0; dy < 3; dy++) for (let dx = 0; dx < 3; dx++) grade[by + dy][bx + dx] = BLOB[dy][dx]
    const mapa = this.make.tilemap({ data: grade, tileWidth: T, tileHeight: T })
    const ts = mapa.addTilesetImage('chao')!
    mapa.createLayer(0, ts, 0, 0)!.setDepth(0)

    // ---- PROPS com colisão (depth por "pé" = ordena sozinho) ----
    const solidos = this.physics.add.staticGroup()
    const põe = (nome: string, x: number, y: number, pes = 10): Phaser.GameObjects.Image => {
      const im = this.add.image(x, y, 'mundo', nome).setOrigin(0.5, 1)
      im.setDepth(y)
      const w = im.width * 0.8
      const corpo = this.add.rectangle(x, y - pes / 2, w, pes)
      this.physics.add.existing(corpo, true)
      solidos.add(corpo)
      return im
    }
    põe('casa_a', 90, 70, 26); põe('casa_b', 330, 58, 26)
    põe('varal', 395, 52, 8)
    põe('torii', 256, 318, 8)                       // portal de entrada da vila (sul)
    põe('cerca', 40, 300, 8); põe('cerca', 470, 300, 8)
    põe('pedras', 460, 120, 18)
    põe('toco', 60, 200, 10)
    põe('carroca', 190, 150, 12); põe('feira', 300, 152, 12)
    for (const [ax, ay] of [[30, 120], [140, 250], [370, 240], [480, 200], [210, 300], [430, 90]]) {
      põe('arvore', ax, ay, 12)
    }

    // ---- animações (colunas = direção; linhas 0-3 = passos) ----
    const dirCol: Record<string, number> = { baixo: 0, cima: 1, esq: 2, dir: 3 }
    for (const ch of ['heroi', 'fazendeiro', 'menina', 'avo']) {
      for (const [dnome, col] of Object.entries(dirCol)) {
        this.anims.create({
          key: ch + '-anda-' + dnome,
          frames: [0, 1, 2, 3].map(r => ({ key: ch, frame: r * 4 + col })),
          frameRate: 8, repeat: -1
        })
      }
    }
    this.anims.create({ key: 'dog-anda', frames: [{ key: 'dog', frame: 0 }, { key: 'dog', frame: 1 }], frameRate: 6, repeat: -1 })

    const cria = (chave: string, x: number, y: number): Andante => {
      const sombra = this.add.image(x + 1, y + 6, 'sombra').setAlpha(0.6)
      const sp = this.physics.add.sprite(x, y, chave, 0)
      sp.setDepth(y).setCollideWorldBounds(true)
      const corpo = sp.body as Phaser.Physics.Arcade.Body
      corpo.setSize(10, 8).setOffset(3, 8)          // só os PÉS colidem (passa atrás das casas)
      return { sp, sombra, chave }
    }

    // ---- HERÓI + NPCs neutros + dog ----
    this.heroi = cria('heroi', 256, 260)
    this.npcs = [cria('fazendeiro', 232, 150), cria('menina', 120, 220), cria('avo', 330, 90)]
    const dog = cria('dog', 290, 250); dog.sp.play('dog-anda')
    this.npcs.push(dog)

    this.physics.add.collider(this.heroi.sp, solidos)
    for (const n of this.npcs) {
      this.physics.add.collider(n.sp, solidos)
      // gente tem corpo: nao se atravessa (imovel = o heroi nao sai empurrando)
      if (n.chave !== 'dog') (n.sp.body as Phaser.Physics.Arcade.Body).setImmovable(true)
      this.physics.add.collider(this.heroi.sp, n.sp)
    }

    // NPCs respiram (bob sutil) e dão um pulinho quando o herói chega perto
    for (const n of this.npcs) {
      this.tweens.add({ targets: n.sp, scaleY: 1.03, duration: 900 + Math.random() * 400, yoyo: true, repeat: -1 })
    }
    // dog passeia sozinho
    this.time.addEvent({
      delay: 2600,
      loop: true,
      callback: () => {
        const vx = Phaser.Math.Between(-40, 40)
        dog.sp.setVelocity(vx, Phaser.Math.Between(-30, 30))
        if (vx !== 0) dog.sp.setFlipX(vx < 0)
        this.time.delayedCall(900, () => dog.sp.setVelocity(0, 0))
      }
    })

    // ---- câmera (zoom 3 = pixel gigante e nítido no celular e no PC velho) ----
    this.physics.world.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setZoom(3).startFollow(this.heroi.sp, true, 0.12, 0.12)

    // ---- controle: toque/clique anda até lá ----
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY)
    })

    // ---- ganchos do robô-QA ----
    ;(window as any).__vila = this
    ;(window as any).__tp = (x: number, y: number) => { this.heroi.sp.setPosition(x, y); this.alvo = null }
    ;(window as any).__anda = (x: number, y: number) => { this.alvo = new Phaser.Math.Vector2(x, y) }
  }

  update (): void {
    const h = this.heroi
    const VEL = 70
    if (this.alvo) {
      const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.alvo.x, this.alvo.y)
      if (d < 4) {
        this.alvo = null
      } else {
        this.physics.moveTo(h.sp, this.alvo.x, this.alvo.y, VEL)
      }
    }
    if (!this.alvo) h.sp.setVelocity(0, 0)

    const vx = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.x
    const vy = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.y
    if (Math.abs(vx) + Math.abs(vy) > 4) {
      this.dir = Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 'dir' : 'esq') : (vy > 0 ? 'baixo' : 'cima')
      h.sp.play('heroi-anda-' + this.dir, true)
    } else if (h.sp.anims.isPlaying) {
      h.sp.stop()
      const col: Record<string, number> = { baixo: 0, cima: 1, esq: 2, dir: 3 }
      h.sp.setFrame(col[this.dir])
    }

    // sombra segue + depth vivo (passa na frente/atrás conforme o Y)
    for (const a of [h, ...this.npcs]) {
      a.sombra.setPosition(a.sp.x + 1, a.sp.y + 7)
      a.sp.setDepth(a.sp.y)
      a.sombra.setDepth(a.sp.y - 0.5)
    }

    // gente de verdade OLHA pra você quando você chega perto
    for (const n of this.npcs) {
      if (n.chave === 'dog') continue
      const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, n.sp.x, n.sp.y)
      if (d < 26 && !n.sp.anims.isPlaying) {
        const dx = h.sp.x - n.sp.x, dy = h.sp.y - n.sp.y
        const col = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 3 : 2) : (dy > 0 ? 0 : 1)
        n.sp.setFrame(col)
      }
    }
  }
}
