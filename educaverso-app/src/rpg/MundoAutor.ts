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
  local: 'mundo' | 'casa' = 'mundo'
  private trocando = false
  terreno!: { x: number, y: number, w: number, h: number }

  constructor () { super({ key: 'MundoAutor' }) }

  // monta uma sala INTERIOR (moldura wall_simple do autor + piso + móveis + porta no
  // muro de baixo). Mesma técnica validada na Vila Viva. Devolve nada; cria os corpos.
  montaSala (s: { x: number, y: number, tw: number, th: number }, solidos: Phaser.Physics.Arcade.StaticGroup): void {
    const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, BdL: 41, BdR: 42, B: 43, BR: 44, ESC: 50 }
    const cx = s.tw >> 1
    const bloco = (x: number, y: number, w: number, h: number): void => {
      const r = this.add.rectangle(x, y, w, h); this.physics.add.existing(r, true); solidos.add(r)
    }
    const tile = (ix: number, iy: number, fr: number, depth: number): void => {
      this.add.image(s.x + ix * T + 8, s.y + iy * T + 8, 'paredes', fr).setDepth(depth)
    }
    this.add.rectangle(s.x + s.tw * T / 2, s.y + s.th * T / 2, s.tw * T + 192, s.th * T + 192, 0x0e0c12).setDepth(-2)
    for (let iy = -3; iy < s.th + 3; iy++) for (let ix = -3; ix < s.tw + 3; ix++) {
      if (!(ix >= 0 && ix < s.tw && iy >= 0 && iy < s.th)) tile(ix, iy, PAR.ESC, 0.4)
    }
    for (let px = s.x + T; px < s.x + (s.tw - 1) * T; px += 48) {
      for (let py = s.y + T; py < s.y + (s.th - 1) * T; py += 48) this.add.image(px, py, 'piso').setOrigin(0).setDepth(-1)
    }
    this.add.image(s.x + cx * T, s.y + (s.th - 2) * T, 'piso').setOrigin(0).setDepth(-1).setCrop(0, 0, 16, 32)
    tile(0, 0, PAR.TL, 0.45); tile(s.tw - 1, 0, PAR.TR, 0.45)
    for (let ix = 1; ix < s.tw - 1; ix++) tile(ix, 0, PAR.T, 0.45)
    for (let iy = 1; iy < s.th - 1; iy++) { tile(0, iy, PAR.L, 0.45); tile(s.tw - 1, iy, PAR.R, 0.45) }
    tile(0, s.th - 1, PAR.BL, 9000); tile(s.tw - 1, s.th - 1, PAR.BR, 9000)
    for (let ix = 1; ix < s.tw - 1; ix++) {
      if (ix === cx) continue
      tile(ix, s.th - 1, ix === cx - 1 ? PAR.BdL : (ix === cx + 1 ? PAR.BdR : PAR.B), 9000)
    }
    bloco(s.x + s.tw * T / 2, s.y + 8, s.tw * T, 16)
    bloco(s.x + 4, s.y + s.th * T / 2, 8, s.th * T)
    bloco(s.x + s.tw * T - 4, s.y + s.th * T / 2, 8, s.th * T)
    bloco(s.x + (cx * T) / 2, s.y + (s.th - 1) * T + 8, cx * T, 16)
    const wDir = (s.tw - cx - 1) * T
    bloco(s.x + (cx + 1) * T + wDir / 2, s.y + (s.th - 1) * T + 8, wDir, 16)
    bloco(s.x + cx * T + 8, s.y + (s.th + 1) * T + 8, 32, 16)
    // móveis (aconchego + colisão) — encostados na parede.
    // PROFUNDIDADE RELATIVA À SALA (dep = 100 + Y local): a sala fica em Y NEGATIVO
    // (fora do mapa), então usar o Y do mundo daria profundidade negativa = móvel
    // sumido embaixo do piso. dep sempre positivo, entre piso(-1) e parede-baixo(9000).
    const dep = (y: number): number => 100 + (y - s.y)
    this.add.image(s.x + 80, s.y + 84, 'mundo', 'tapete').setDepth(0.6)
    const põe = (nome: string, x: number, y: number): void => {
      this.add.image(x, y, 'mundo', nome).setOrigin(0.5, 1).setDepth(dep(y))
      const r = this.add.rectangle(x, y - 5, 24, 10); this.physics.add.existing(r, true); solidos.add(r)
    }
    põe('estante', s.x + 36, s.y + 48); põe('prateleira', s.x + 76, s.y + 47)
    this.add.image(s.x + 122, s.y + 44, 'bau', 0).setOrigin(0.5, 1).setDepth(dep(s.y + 44))
    bloco(s.x + 122, s.y + 40, 14, 8)
    this.add.image(s.x + 140, s.y + 46, 'jar', 0).setOrigin(0.5, 1).setDepth(dep(s.y + 46))
  }

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
    this.load.image('piso', b + 'piso.png')
    this.load.image('mundo', b + 'mundo.png')
    this.load.spritesheet('bau', b + 'bau.png', { frameWidth: 16, frameHeight: 14 })
    this.load.spritesheet('jar', b + 'jar.png', { frameWidth: 16, frameHeight: 16 })
    this.load.json('mapa_autor', b + 'mapa_autor.json')
  }

  create (): void {
    const M = this.M = this.cache.json.get('mapa_autor') as MapaAutor

    // frames nomeados dos móveis (recortes AUDITADOS do tileset grande)
    const tex = this.textures.get('mundo')
    const FR: Record<string, [number, number, number, number]> = {
      estante: [160, 592, 33, 32], prateleira: [206, 592, 31, 31], tapete: [112, 592, 48, 48]
    }
    for (const [nome, [x, y, w, h]] of Object.entries(FR)) tex.add(nome, 0, x, y, w, h)

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

    // ---- limites do TERRENO jogável (não o grid inteiro — senão a câmera mostra
    // o vazio e o herói "some" na borda). Bounding box de onde há chão. ----
    let bx0 = M.w, bx1 = 0, by0 = M.h, by1 = 0
    for (let y = 0; y < M.h; y++) for (let x = 0; x < M.w; x++) {
      if (M.chao[y][x] < 0) continue
      if (x < bx0) bx0 = x; if (x > bx1) bx1 = x
      if (y < by0) by0 = y; if (y > by1) by1 = y
    }
    const TB = { x: bx0 * T, y: by0 * T, w: (bx1 - bx0 + 1) * T, h: (by1 - by0 + 1) * T }
    this.terreno = TB

    // ---- INTERIOR (casa do meio do autor — porta em ~tile 29,42) ----
    const SALA = { x: 200, y: -260, tw: 10, th: 8 }                 // fora do terreno, ao norte
    const PORTA = { x: 29 * T + 8, y: 43 * T + 2 }                  // soleira ANDÁVEL (tile 42 colide)
    const solidosSala = this.physics.add.staticGroup()
    this.montaSala(SALA, solidosSala)
    const vaoSala = { x: SALA.x + (SALA.tw >> 1) * T + 8, y: SALA.y + (SALA.th - 1) * T + 8 }

    const irPara = (dest: 'mundo' | 'casa'): void => {
      if (this.trocando) return
      this.trocando = true
      this.alvo = null; this.heroi.sp.setVelocity(0, 0)
      this.cameras.main.fadeOut(220, 14, 12, 18)
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.local = dest
        if (dest === 'casa') {
          this.heroi.sp.setPosition(vaoSala.x, vaoSala.y - 28)
          this.cameras.main.setZoom(4)
          this.cameras.main.setBounds(SALA.x - 48, SALA.y - 32, SALA.tw * T + 96, SALA.th * T + 64)
        } else {
          this.heroi.sp.setPosition(PORTA.x, PORTA.y + 16)
          this.cameras.main.setZoom(3)
          this.cameras.main.setBounds(TB.x, TB.y, TB.w, TB.h)
        }
        this.cameras.main.startFollow(this.heroi.sp, true, 0.12, 0.12)
        this.cameras.main.centerOn(this.heroi.sp.x, this.heroi.sp.y)
        this.cameras.main.fadeIn(220, 14, 12, 18)
        this.time.delayedCall(380, () => { this.trocando = false })
      })
    }
    const zEntra = this.add.zone(PORTA.x, PORTA.y, 12, 8); this.physics.add.existing(zEntra, true)
    this.physics.add.overlap(this.heroi.sp, zEntra, () => { if (this.local === 'mundo') irPara('casa') })
    const zSai = this.add.zone(vaoSala.x, vaoSala.y - 2, 16, 12); this.physics.add.existing(zSai, true)
    this.physics.add.overlap(this.heroi.sp, zSai, () => { if (this.local === 'casa') irPara('mundo') })
    for (const a of [this.heroi, ...this.npcs]) this.physics.add.collider(a.sp, solidosSala)
    ;(window as any).__irPara = irPara

    // ---- câmera ----
    this.cameras.main.setBounds(TB.x, TB.y, TB.w, TB.h)
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
