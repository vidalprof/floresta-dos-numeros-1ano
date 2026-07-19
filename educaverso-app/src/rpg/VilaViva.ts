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
  feira:   [116, 130, 27, 28],
  // móveis do interior (régua na faixa y=584..640 do tileset)
  estante:   [160, 590, 37, 34],
  prateleira: [200, 590, 37, 33],
  tapete:    [112, 592, 48, 48],
  planta:    [0, 600, 15, 24]
}

// ---- zona INTERIOR (a casinha por dentro) — fica fora do mapa da vila,
// LONGE o bastante p/ a câmera (visão de ~341px) nunca alcançar a vila ----
const CASA = { x: 704, y: 48, w: 160, h: 128 }
const PORTA_VILA = { x: 90, y: 76 }                 // porta da casa_a na vila
const TAPETE_SAIDA = { x: CASA.x + 80, y: CASA.y + 118 }

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
  local: 'vila' | 'casa' = 'vila'                 // zona atual (QA lê)
  private trocando = false
  vistaTudo = false                               // modo "ver o cenário todo"

  // alterna câmera: seguir o herói (zoom 3) <-> ver o cenário inteiro (zoom 2)
  alternaVista (): void {
    const cam = this.cameras.main
    this.vistaTudo = !this.vistaTudo
    if (this.vistaTudo && this.local === 'vila') {
      cam.stopFollow()
      cam.removeBounds()                           // senão o clamp prega o mapa no topo
      cam.setZoom(2)                               // 512x320 cabe inteiro em 1024 (faixas em cima/embaixo)
      cam.centerOn(MAPA_W * T / 2, MAPA_H * T / 2)
    } else {
      this.vistaTudo = false
      cam.setZoom(3)
      if (this.local === 'vila') cam.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
      cam.startFollow(this.heroi.sp, true, 0.12, 0.12)
      cam.centerOn(this.heroi.sp.x, this.heroi.sp.y)
    }
  }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    for (const ch of ['heroi', 'fazendeiro', 'menina', 'avo']) {
      this.load.spritesheet(ch, b + ch + '.png', { frameWidth: T, frameHeight: T })
    }
    this.load.spritesheet('dog', b + 'dog.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.image('mundo', b + 'mundo.png')
    this.load.image('sombra', b + 'sombra.png')
    this.load.image('piso', b + 'piso.png')          // parquê do interior (NA)
    this.load.spritesheet('bau', b + 'bau.png', { frameWidth: 16, frameHeight: 14 })
    this.load.spritesheet('jar', b + 'jar.png', { frameWidth: 16, frameHeight: 16 })
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
      // SEM collideWorldBounds: trocar o bounds do mundo ARRASTAVA os NPCs da
      // vila p/ dentro da casa (clamp). As bordas são PAREDES estáticas.
      sp.setDepth(y)
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

    // bordas da VILA (paredes estáticas — substituem o worldBounds, que ao ser
    // trocado de zona ARRASTAVA os corpos de fora pra dentro)
    for (const [wx, wy, ww, wh] of [
      [MAPA_W * T / 2, -4, MAPA_W * T, 8], [MAPA_W * T / 2, MAPA_H * T + 4, MAPA_W * T, 8],
      [-4, MAPA_H * T / 2, 8, MAPA_H * T], [MAPA_W * T + 4, MAPA_H * T / 2, 8, MAPA_H * T]
    ] as const) {
      const r = this.add.rectangle(wx, wy, ww, wh); this.physics.add.existing(r, true); solidos.add(r)
    }

    // ---- INTERIOR da casinha (zona 2, montada fora do mapa da vila) ----
    this.add.rectangle(CASA.x + CASA.w / 2, CASA.y + CASA.h / 2, CASA.w + 192, CASA.h + 192, 0x0e0c12).setDepth(-2)
    for (let ix = CASA.x; ix < CASA.x + CASA.w; ix += 48) {
      for (let iy = CASA.y + 8; iy < CASA.y + CASA.h - 8; iy += 48) {
        this.add.image(ix, iy, 'piso').setOrigin(0).setDepth(-1)
      }
    }
    // recorta o piso que vazou da sala (moldura escura LARGA por cima)
    const mold = this.add.graphics().setDepth(0.5)
    mold.fillStyle(0x0e0c12)
    mold.fillRect(CASA.x - 96, CASA.y - 96, CASA.w + 192, 104)                 // topo
    mold.fillRect(CASA.x - 96, CASA.y + CASA.h - 8, CASA.w + 192, 104)         // base
    mold.fillRect(CASA.x - 96, CASA.y - 96, 104, CASA.h + 192)                 // esq
    mold.fillRect(CASA.x + CASA.w - 8, CASA.y - 96, 104, CASA.h + 192)         // dir
    // móveis (aconchego + colisão) — o tapete é só chão (sem corpo)
    this.add.image(CASA.x + 80, CASA.y + 62, 'mundo', 'tapete').setDepth(0.6)
    põe('estante', CASA.x + 34, CASA.y + 44, 12)
    põe('prateleira', CASA.x + 74, CASA.y + 43, 12)
    põe('planta', CASA.x + 18, CASA.y + 116, 8)
    const bau = this.add.image(CASA.x + 122, CASA.y + 36, 'bau', 0).setOrigin(0.5, 1).setDepth(CASA.y + 36)
    const cb = this.add.rectangle(CASA.x + 122, CASA.y + 32, 14, 8); this.physics.add.existing(cb, true); solidos.add(cb)
    this.add.image(CASA.x + 142, CASA.y + 40, 'jar', 0).setOrigin(0.5, 1).setDepth(CASA.y + 40)
    void bau
    // paredes invisíveis da sala
    for (const [wx, wy, ww, wh] of [
      [CASA.x + CASA.w / 2, CASA.y + 12, CASA.w, 24],                    // topo (parede alta)
      [CASA.x + CASA.w / 2, CASA.y + CASA.h - 2, CASA.w, 12],           // base
      [CASA.x + 4, CASA.y + CASA.h / 2, 8, CASA.h],                      // esq
      [CASA.x + CASA.w - 4, CASA.y + CASA.h / 2, 8, CASA.h]              // dir
    ] as const) {
      const r = this.add.rectangle(wx, wy, ww, wh); this.physics.add.existing(r, true); solidos.add(r)
    }

    // ---- PORTAS (entrar/sair com fade — o grafo de zonas do motor) ----
    const vaiPara = (dest: 'vila' | 'casa') => {
      if (this.trocando) return
      this.trocando = true
      this.alvo = null
      this.heroi.sp.setVelocity(0, 0)
      this.cameras.main.fadeOut(240, 14, 12, 18)
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.local = dest
        // trocar de zona SEMPRE volta pra visão normal (senão fica preso no zoom longe)
        this.vistaTudo = false
        this.cameras.main.setZoom(3)
        this.cameras.main.startFollow(this.heroi.sp, true, 0.12, 0.12)
        if (dest === 'casa') {
          // nasce ACIMA do tapete de saída (senão a zona de saída dispara na hora)
          this.heroi.sp.setPosition(TAPETE_SAIDA.x, TAPETE_SAIDA.y - 26)
          this.cameras.main.removeBounds()          // sala centrada na tela
        } else {
          this.heroi.sp.setPosition(PORTA_VILA.x, PORTA_VILA.y + 14)
          this.cameras.main.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
        }
        this.cameras.main.centerOn(this.heroi.sp.x, this.heroi.sp.y)  // corta direto (sem panorâmica no escuro)
        this.cameras.main.fadeIn(240, 14, 12, 18)
        this.time.delayedCall(400, () => { this.trocando = false })
      })
    }
    const portaCasa = this.add.zone(PORTA_VILA.x, PORTA_VILA.y, 18, 10)
    this.physics.add.existing(portaCasa, true)
    this.physics.add.overlap(this.heroi.sp, portaCasa, () => { if (this.local === 'vila') vaiPara('casa') })
    // tapete de saída (visível: o próprio tapete pequeno na base da sala)
    this.add.image(TAPETE_SAIDA.x, TAPETE_SAIDA.y, 'mundo', 'tapete').setDisplaySize(24, 12).setDepth(0.6)
    // zona ANTES da parede de baixo (o herói para na parede; a zona tem que
    // alcançar os pés dele ali — atrás da parede nunca sobrepõe)
    const portaSaida = this.add.zone(TAPETE_SAIDA.x, TAPETE_SAIDA.y - 2, 24, 12)
    this.physics.add.existing(portaSaida, true)
    this.physics.add.overlap(this.heroi.sp, portaSaida, () => { if (this.local === 'casa') vaiPara('vila') })
    ;(window as any).__vaiPara = vaiPara

    // ---- câmera (zoom 3 = pixel gigante e nítido no celular e no PC velho) ----
    this.physics.world.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setZoom(3).startFollow(this.heroi.sp, true, 0.12, 0.12)

    // ---- controle: toque/clique anda até lá ----
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY)
    })

    // ---- UI (tela cheia + ver tudo) numa cena própria, sem zoom ----
    this.registry.set('vila', this)
    this.scene.launch('UIVila')

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
