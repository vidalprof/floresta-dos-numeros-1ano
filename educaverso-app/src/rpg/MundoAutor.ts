// ============================================================================
// MUNDO DO AUTOR — o mapa COMPLETO do criador do pack (map_village.tscn do
// pixel-boy, CC0), decodificado tile a tile e montado no nosso motor Phaser.
// "Lendo o que o autor escreveu": chão dele, caminhos dele, florestas dele,
// construções dele — com as camadas profissionais (base ABAIXO do herói,
// copas/telhados POR CIMA), colisões, nossos personagens vivos dentro.
// QA: window.__mundoA + __tpA/__andaA.
// ============================================================================
import Phaser from 'phaser'

const T = 16

interface Andante {
  sp: Phaser.Physics.Arcade.Sprite
  sombra: Phaser.GameObjects.Image
  chave: string
}

interface MapaAutor { w: number, h: number, chao: number[][], paredes: number[][], base: number[][], topo: number[][] }

export class MundoAutor extends Phaser.Scene {
  private heroi!: Andante
  private npcs: Andante[] = []
  private alvo: Phaser.Math.Vector2 | null = null
  private dir = 'baixo'
  private curs?: Phaser.Types.Input.Keyboard.CursorKeys
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
  M!: MapaAutor

  constructor () { super({ key: 'MundoAutor' }) }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    for (const ch of ['heroi', 'fazendeiro', 'menina', 'avo']) {
      this.load.spritesheet(ch, b + ch + '.png', { frameWidth: T, frameHeight: T })
    }
    this.load.spritesheet('dog', b + 'dog.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('paredes', b + 'paredes.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('aldeia', b + 'aldeia.png', { frameWidth: T, frameHeight: T })
    this.load.image('sombra', b + 'sombra.png')
    this.load.json('mapa_autor', b + 'mapa_autor.json')
  }

  create (): void {
    const M = this.M = this.cache.json.get('mapa_autor') as MapaAutor

    // ---- as 4 camadas do autor (ordem profissional) ----
    const faz = (dados: number[][], tex: string, depth: number): Phaser.Tilemaps.TilemapLayer => {
      const mp = this.make.tilemap({ data: dados, tileWidth: T, tileHeight: T })
      const ts = mp.addTilesetImage(tex)!
      return mp.createLayer(0, ts, 0, 0)!.setDepth(depth)
    }
    faz(M.chao, 'chao', 0)
    const paredes = faz(M.paredes, 'paredes', 1)
    const base = faz(M.base, 'aldeia', 2)
    faz(M.topo, 'aldeia', 9000)                       // copas/telhados POR CIMA do herói

    // ---- colisões: paredes + bases sólidas + o VAZIO fora do terreno ----
    paredes.setCollisionByExclusion([-1])
    base.setCollisionByExclusion([-1])
    // vazio (fora do chão) vira parede invisível por tile — barato: só a borda
    const solidosVazio = this.physics.add.staticGroup()
    for (let y = 0; y < M.h; y++) {
      for (let x = 0; x < M.w; x++) {
        if (M.chao[y][x] >= 0) continue
        // só bloqueia vazio ENCOSTADO em chão (borda) — o resto é inalcançável
        const viz = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => {
          const g = (M.chao[y + dy] || [])[x + dx]
          return g !== undefined && g >= 0
        })
        if (viz) {
          const r = this.add.rectangle(x * T + 8, y * T + 8, T, T)
          this.physics.add.existing(r, true)
          solidosVazio.add(r)
        }
      }
    }

    // ---- gente (elenco neutro) ----
    const cria = (chave: string, x: number, y: number): Andante => {
      const sombra = this.add.image(x + 1, y + 6, 'sombra').setAlpha(0.6).setDepth(2.5)
      const sp = this.physics.add.sprite(x, y, chave, 0)
      sp.setDepth(3)
      const corpo = sp.body as Phaser.Physics.Arcade.Body
      corpo.setSize(10, 8).setOffset(3, 8)
      return { sp, sombra, chave }
    }
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

    this.heroi = cria('heroi', 43 * T + 8, 41 * T + 8)          // no caminho central
    this.npcs = [
      cria('fazendeiro', 40 * T + 8, 39 * T + 8),
      cria('menina', 47 * T + 8, 44 * T + 8),
      cria('avo', 38 * T + 8, 46 * T + 8)
    ]
    const dog = cria('dog', 45 * T + 8, 42 * T + 8); dog.sp.play('dog-anda')
    this.npcs.push(dog)

    for (const a of [this.heroi, ...this.npcs]) {
      this.physics.add.collider(a.sp, paredes)
      this.physics.add.collider(a.sp, base)
      this.physics.add.collider(a.sp, solidosVazio)
      if (a !== this.heroi && a.chave !== 'dog') (a.sp.body as Phaser.Physics.Arcade.Body).setImmovable(true)
      if (a !== this.heroi) this.physics.add.collider(this.heroi.sp, a.sp)
    }

    // dog passeia
    this.time.addEvent({
      delay: 2600, loop: true,
      callback: () => {
        const vx = Phaser.Math.Between(-40, 40)
        dog.sp.setVelocity(vx, Phaser.Math.Between(-30, 30))
        if (vx !== 0) dog.sp.setFlipX(vx < 0)
        this.time.delayedCall(900, () => dog.sp.setVelocity(0, 0))
      }
    })

    // ---- câmera ----
    this.cameras.main.setBounds(0, 0, M.w * T, M.h * T)
    this.cameras.main.setZoom(3).startFollow(this.heroi.sp, true, 0.12, 0.12)

    // ---- controles: toque + teclado ----
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY)
    })
    if (this.input.keyboard) {
      this.curs = this.input.keyboard.createCursorKeys()
      this.wasd = this.input.keyboard.addKeys('W,A,S,D') as Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
    }

    // ---- QA ----
    ;(window as any).__mundoA = this
    ;(window as any).__tpA = (x: number, y: number) => { this.heroi.sp.setPosition(x, y); this.alvo = null }
    ;(window as any).__andaA = (x: number, y: number) => { this.alvo = new Phaser.Math.Vector2(x, y) }
  }

  update (): void {
    const h = this.heroi
    const VEL = 70
    let kx = 0, ky = 0
    if (this.curs?.left.isDown || this.wasd?.A.isDown) kx -= 1
    if (this.curs?.right.isDown || this.wasd?.D.isDown) kx += 1
    if (this.curs?.up.isDown || this.wasd?.W.isDown) ky -= 1
    if (this.curs?.down.isDown || this.wasd?.S.isDown) ky += 1
    if (kx !== 0 || ky !== 0) {
      this.alvo = null
      const n = Math.hypot(kx, ky)
      h.sp.setVelocity(kx / n * VEL, ky / n * VEL)
    } else if (this.alvo) {
      const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.alvo.x, this.alvo.y)
      if (d < 4) { this.alvo = null; h.sp.setVelocity(0, 0) } else this.physics.moveTo(h.sp, this.alvo.x, this.alvo.y, VEL)
    } else {
      h.sp.setVelocity(0, 0)
    }

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

    for (const a of [h, ...this.npcs]) {
      a.sombra.setPosition(a.sp.x + 1, a.sp.y + 7)
    }
    // NPCs olham pro herói
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
