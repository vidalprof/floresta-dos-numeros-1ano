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
  toco:    [97, 293, 30, 23],
  arvore:  [0, 160, 32, 32],
  carroca: [82, 131, 27, 27],
  feira:   [116, 130, 27, 28],
  // móveis do interior (régua na faixa y=584..640 do tileset)
  estante:   [160, 592, 33, 32],
  prateleira: [206, 592, 31, 31],
  tapete:    [112, 592, 48, 48],
  planta:    [0, 600, 15, 24]
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
  local: 'vila' | 'casa' = 'vila'                 // zona atual (QA lê)
  private trocando = false
  vistaTudo = false                               // modo "ver o cenário todo"
  salaAtual = 0                                   // qual interior (indice)
  private curs?: Phaser.Types.Input.Keyboard.CursorKeys
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>

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
    this.load.image('piso', b + 'piso.png')          // palha rústica (sala 1)
    this.load.image('piso2', b + 'piso2.png')        // pedra (sala 2 — depósito)
    this.load.spritesheet('paredes', b + 'paredes.png', { frameWidth: T, frameHeight: T })
    this.load.image('pedras2', b + 'pedras.png')     // trio de pedras LIMPO (sem vizinho fatiado)
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
      if (pes > 0) {
        const w = im.width * 0.8
        const corpo = this.add.rectangle(x, y - pes / 2, w, pes)
        this.physics.add.existing(corpo, true)
        solidos.add(corpo)
      }
      return im
    }
    const bloco = (x: number, y: number, w: number, h: number): void => {
      const r = this.add.rectangle(x, y, w, h); this.physics.add.existing(r, true); solidos.add(r)
    }
    põe('casa_a', 90, 70, 0); põe('casa_b', 330, 58, 0)
    // VÃO da porta ("igual no jogo"): casa sólida dos lados; a soleira é passagem
    bloco(71, 57, 26, 26); bloco(109, 57, 26, 26); bloco(90, 52, 12, 8)      // casa_a
    bloco(314, 45, 20, 26); bloco(346, 45, 20, 26); bloco(330, 40, 12, 8)    // casa_b
    põe('varal', 395, 52, 8)
    põe('torii', 256, 318, 8)                       // portal de entrada da vila (sul)
    põe('cerca', 40, 300, 8); põe('cerca', 470, 300, 8)
    { const pd = this.add.image(460, 120, 'pedras2').setOrigin(0.5, 1); pd.setDepth(120); bloco(460, 111, 44, 18) }
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

    // ---- INTERIORES — a SALA DO AUTOR (receita extraída do map_village.tscn) ----
    // Paredes = tileset wall_simple (10 col): cantos (0,0)(4,0)(0,4)(4,4), bordas
    // (3,0)/(0,1)/(4,1)/(3,4), PORTA no muro de baixo (tampas (1,4)+(2,4) com vão),
    // e o entorno preenchido com parede escura (0,5) — nunca vazio cru.
    const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, BdL: 41, BdR: 42, B: 43, BR: 44, ESC: 50 }
    interface CfgSala { porta: { x: number, y: number }, sala: { x: number, y: number }, tw: number, th: number, piso: string }
    const INTERIORES: CfgSala[] = [
      { porta: { x: 90, y: 62 }, sala: { x: 704, y: 48 }, tw: 10, th: 8, piso: 'piso' },
      { porta: { x: 330, y: 50 }, sala: { x: 704, y: 320 }, tw: 10, th: 8, piso: 'piso2' }
    ]
    const vaoDe = (c: CfgSala) => ({ x: c.sala.x + (c.tw >> 1) * T + 8, y: c.sala.y + (c.th - 1) * T + 8 })

    const montaSala = (cfg: CfgSala): void => {
      const s = cfg.sala, tw = cfg.tw, th = cfg.th, cx = tw >> 1
      const tile = (ix: number, iy: number, fr: number, depth: number): void => {
        this.add.image(s.x + ix * T + 8, s.y + iy * T + 8, 'paredes', fr).setDepth(depth)
      }
      // anel de parede ESCURA (3 tiles) em volta — some o "mar preto"
      for (let iy = -3; iy < th + 3; iy++) {
        for (let ix = -3; ix < tw + 3; ix++) {
          const dentro = ix >= 0 && ix < tw && iy >= 0 && iy < th
          if (!dentro) tile(ix, iy, PAR.ESC, 0.4)
        }
      }
      // piso (por baixo das paredes)
      for (let px = s.x + T; px < s.x + (tw - 1) * T; px += 48) {
        for (let py = s.y + T; py < s.y + (th - 1) * T; py += 48) {
          this.add.image(px, py, cfg.piso).setOrigin(0).setDepth(-1)
        }
      }
      // piso na SOLEIRA (a porta mostra chão, não buraco)
      this.add.image(s.x + cx * T, s.y + (th - 2) * T, cfg.piso).setOrigin(0).setDepth(-1).setCrop(0, 0, 16, 32)
      // moldura de parede do AUTOR (a porta fica no muro de baixo)
      tile(0, 0, PAR.TL, 0.45); tile(tw - 1, 0, PAR.TR, 0.45)
      for (let ix = 1; ix < tw - 1; ix++) tile(ix, 0, PAR.T, 0.45)
      for (let iy = 1; iy < th - 1; iy++) { tile(0, iy, PAR.L, 0.45); tile(tw - 1, iy, PAR.R, 0.45) }
      tile(0, th - 1, PAR.BL, 9000); tile(tw - 1, th - 1, PAR.BR, 9000)
      for (let ix = 1; ix < tw - 1; ix++) {
        if (ix === cx) continue                                   // o VÃO da porta
        tile(ix, th - 1, ix === cx - 1 ? PAR.BdL : (ix === cx + 1 ? PAR.BdR : PAR.B), 9000)
      }
      // colisão: muros (o de baixo em 2 pedaços, deixando o vão livre)
      bloco(s.x + tw * T / 2, s.y + 8, tw * T, 16)
      bloco(s.x + 4, s.y + th * T / 2, 8, th * T)
      bloco(s.x + tw * T - 4, s.y + th * T / 2, 8, th * T)
      const wEsq = cx * T
      bloco(s.x + wEsq / 2, s.y + (th - 1) * T + 8, wEsq, 16)
      const wDir = (tw - cx - 1) * T
      bloco(s.x + (cx + 1) * T + wDir / 2, s.y + (th - 1) * T + 8, wDir, 16)
      // fundo do vão (2 tiles abaixo, senão o herói sai andando no escuro)
      bloco(s.x + cx * T + 8, s.y + (th + 1) * T + 8, 32, 16)
    }
    for (const cfg of INTERIORES) montaSala(cfg)

    // decoração SALA 1 — casinha aconchegante (móveis ENCOSTADOS na parede, como no jogo)
    {
      const s = INTERIORES[0].sala
      this.add.image(s.x + 80, s.y + 84, 'mundo', 'tapete').setDepth(0.6)
      põe('estante', s.x + 36, s.y + 48, 10)
      põe('prateleira', s.x + 76, s.y + 47, 10)
      põe('planta', s.x + 22, s.y + 112, 8)
      this.add.image(s.x + 122, s.y + 44, 'bau', 0).setOrigin(0.5, 1).setDepth(s.y + 44)
      bloco(s.x + 122, s.y + 40, 14, 8)
      this.add.image(s.x + 140, s.y + 46, 'jar', 0).setOrigin(0.5, 1).setDepth(s.y + 46)
    }
    // decoração SALA 2 — depósito rústico (pedra + prateleira + jarros + toco)
    {
      const s = INTERIORES[1].sala
      põe('prateleira', s.x + 40, s.y + 47, 10)
      this.add.image(s.x + 96, s.y + 48, 'jar', 0).setOrigin(0.5, 1).setDepth(s.y + 48)
      this.add.image(s.x + 112, s.y + 50, 'jar', 0).setOrigin(0.5, 1).setDepth(s.y + 50)
      bloco(s.x + 104, s.y + 45, 28, 8)
      põe('toco', s.x + 118, s.y + 98, 10)
      põe('planta', s.x + 22, s.y + 104, 8)
    }

    // ---- PORTAS (fade — o grafo de zonas do motor) ----
    this.salaAtual = 0
    const vaiPara = (dest: number | 'vila') => {
      if (this.trocando) return
      this.trocando = true
      this.alvo = null
      this.heroi.sp.setVelocity(0, 0)
      this.cameras.main.fadeOut(240, 14, 12, 18)
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.vistaTudo = false
        if (dest === 'vila') {
          this.local = 'vila'
          const p = INTERIORES[this.salaAtual].porta
          this.heroi.sp.setPosition(p.x, p.y + 18)          // nasce em frente à casa
          this.cameras.main.setZoom(3)
          this.cameras.main.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
        } else {
          this.local = 'casa'
          this.salaAtual = dest
          const cfg = INTERIORES[dest]
          const v = vaoDe(cfg)
          this.heroi.sp.setPosition(v.x, v.y - 28)          // nasce NA porta, dentro da sala
          // câmera COLADA na sala (zoom 4): a sala enche a tela, sem mar preto
          this.cameras.main.setZoom(4)
          this.cameras.main.setBounds(cfg.sala.x - 48, cfg.sala.y - 32, cfg.tw * T + 96, cfg.th * T + 64)
        }
        this.cameras.main.startFollow(this.heroi.sp, true, 0.12, 0.12)
        this.cameras.main.centerOn(this.heroi.sp.x, this.heroi.sp.y)
        this.cameras.main.fadeIn(240, 14, 12, 18)
        this.time.delayedCall(400, () => { this.trocando = false })
      })
    }
    INTERIORES.forEach((cfg, i) => {
      // entrada: gatilho na SOLEIRA da casinha (vão físico na vila)
      const z = this.add.zone(cfg.porta.x, cfg.porta.y, 10, 6)
      this.physics.add.existing(z, true)
      this.physics.add.overlap(this.heroi.sp, z, () => { if (this.local === 'vila') vaiPara(i) })
      // saída: ANDAR até a PORTA da sala (o vão no muro de baixo) — como no jogo
      const v = vaoDe(cfg)
      const zs = this.add.zone(v.x, v.y + 6, 14, 12)
      this.physics.add.existing(zs, true)
      this.physics.add.overlap(this.heroi.sp, zs, () => { if (this.local === 'casa' && this.salaAtual === i) vaiPara('vila') })
    })
    ;(window as any).__vaiPara = vaiPara

    // ---- câmera (zoom 3 = pixel gigante e nítido no celular e no PC velho) ----
    this.physics.world.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setBounds(0, 0, MAPA_W * T, MAPA_H * T)
    this.cameras.main.setZoom(3).startFollow(this.heroi.sp, true, 0.12, 0.12)

    // ---- controle: toque/clique anda até lá ----
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY)
    })
    // ---- controle: TECLADO (PC da escola) — setas e WASD ----
    if (this.input.keyboard) {
      this.curs = this.input.keyboard.createCursorKeys()
      this.wasd = this.input.keyboard.addKeys('W,A,S,D') as Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
    }

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
    // TECLADO tem prioridade (segurou a tecla = anda; cancela o alvo do toque)
    let kx = 0, ky = 0
    if (this.curs?.left.isDown || this.wasd?.A.isDown) kx -= 1
    if (this.curs?.right.isDown || this.wasd?.D.isDown) kx += 1
    if (this.curs?.up.isDown || this.wasd?.W.isDown) ky -= 1
    if (this.curs?.down.isDown || this.wasd?.S.isDown) ky += 1
    if (kx !== 0 || ky !== 0) {
      this.alvo = null
      const n = Math.hypot(kx, ky)                 // diagonal não anda mais rápido
      h.sp.setVelocity(kx / n * VEL, ky / n * VEL)
    } else if (this.alvo) {
      const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.alvo.x, this.alvo.y)
      if (d < 4) {
        this.alvo = null
        h.sp.setVelocity(0, 0)
      } else {
        this.physics.moveTo(h.sp, this.alvo.x, this.alvo.y, VEL)
      }
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
