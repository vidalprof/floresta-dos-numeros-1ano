// ============================================================================
// FASE UM — a 1ª FASE REAL (prova do "estúdio profissional"): tela EMOLDURADA
// (grade de telas do autor), assets do jogo, MÚSICA do jogo, história simples,
// e o esqueleto da pedagogia: o Byte/fazendeiro tem um PROBLEMA, a criança
// RESOLVE (junta 5 potes de mel = contar), ENTREGA, o mundo MUDA (o caminho
// abre) e ela avança. Interior da casa entrável. Tudo dirigido pelo robô-QA.
// Depois, "juntar 5 potes" vira o desafio pedagógico que o gerador escolher.
// ============================================================================
import Phaser from 'phaser'

const T = 16
const FW = 20, FH = 12                 // fase emoldurada 320x192 (cabe inteira, zoom 3)

// props do tileset grande (recortes AUDITADOS)
const PROPS: Record<string, [number, number, number, number]> = {
  casa_a: [0, 0, 64, 48], arvore: [0, 160, 32, 32], toco: [97, 293, 30, 23],
  carroca: [82, 131, 27, 27], tapete: [112, 592, 48, 48],
  estante: [160, 592, 33, 32], prateleira: [206, 592, 31, 31], planta: [0, 600, 15, 24]
}
const MEL_ALVO = 5

interface Andante { sp: Phaser.Physics.Arcade.Sprite, sombra: Phaser.GameObjects.Image }

export class FaseUm extends Phaser.Scene {
  private heroi!: Andante
  private fazendeiro!: Andante
  private alvo: Phaser.Math.Vector2 | null = null
  private dir = 'baixo'
  private curs?: Phaser.Types.Input.Keyboard.CursorKeys
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
  mel = 0                              // quantos potes já pegou (QA lê)
  entregou = false                    // entregou ao fazendeiro? (QA lê)
  local: 'fase' | 'casa' = 'fase'     // dentro de casa? (QA lê)
  private trocando = false
  private hud!: Phaser.GameObjects.Text
  private balao!: Phaser.GameObjects.Text
  private pedras?: Phaser.GameObjects.Image
  private pedrasBloco?: Phaser.GameObjects.Rectangle
  private musica?: Phaser.Sound.BaseSound

  constructor () { super({ key: 'FaseUm' }) }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    for (const ch of ['heroi', 'fazendeiro']) this.load.spritesheet(ch, b + ch + '.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('paredes', b + 'paredes.png', { frameWidth: T, frameHeight: T })
    this.load.image('mundo', b + 'mundo.png')
    this.load.image('sombra', b + 'sombra.png')
    this.load.image('mel', b + 'mel.png')
    this.load.image('pedras2', b + 'pedras.png')
    this.load.image('piso', b + 'piso.png')
    this.load.spritesheet('bau', b + 'bau.png', { frameWidth: 16, frameHeight: 14 })
    this.load.spritesheet('jar', b + 'jar.png', { frameWidth: 16, frameHeight: 16 })
    this.load.audio('musica', b + 'musica.ogg')
  }

  create (): void {
    const tex = this.textures.get('mundo')
    for (const [n, [x, y, w, h]] of Object.entries(PROPS)) tex.add(n, 0, x, y, w, h)

    const dirCol: Record<string, number> = { baixo: 0, cima: 1, esq: 2, dir: 3 }
    for (const ch of ['heroi', 'fazendeiro']) for (const [d, c] of Object.entries(dirCol)) {
      this.anims.create({ key: ch + '-anda-' + d, frames: [0, 1, 2, 3].map(r => ({ key: ch, frame: r * 4 + c })), frameRate: 8, repeat: -1 })
    }

    const solidos = this.physics.add.staticGroup()
    const bloco = (x: number, y: number, w: number, h: number): Phaser.GameObjects.Rectangle => {
      const r = this.add.rectangle(x, y, w, h); this.physics.add.existing(r, true); solidos.add(r); return r
    }
    // zona = gatilho de OVERLAP (NÃO colide — senão o herói esbarra em vez de pegar)
    const zona = (x: number, y: number, w: number, h: number): Phaser.GameObjects.Rectangle => {
      const r = this.add.rectangle(x, y, w, h); this.physics.add.existing(r, true); return r
    }
    const põe = (nome: string, x: number, y: number, pes = 10): void => {
      this.add.image(x, y, 'mundo', nome).setOrigin(0.5, 1).setDepth(y)
      if (pes > 0) bloco(x, y - pes / 2, 22, pes)
    }

    // --- chão: grama + um caminho de terra (blob) ---
    const G = (col: number, lin: number) => (7 + lin) * 22 + col
    const grade: number[][] = Array.from({ length: FH }, () => new Array(FW).fill(245))
    for (let dy = 0; dy < 3; dy++) for (let dx = 0; dx < 3; dx++) grade[5 + dy][8 + dx] = G(dx, dy)
    const mp = this.make.tilemap({ data: grade, tileWidth: T, tileHeight: T })
    mp.createLayer(0, mp.addTilesetImage('chao')!, 0, 0)!.setDepth(0)

    const W = FW * T, H = FH * T
    // --- MOLDURA (a borda "legal" da tela) — cerca de muro em volta, saída à direita ---
    const saiY = FH >> 1                                  // abertura no muro da direita
    const par = (ix: number, iy: number, fr: number) => this.add.image(ix * T + 8, iy * T + 8, 'paredes', fr).setDepth(iy * T + 4)
    const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44 }
    for (let ix = 0; ix < FW; ix++) { par(ix, 0, ix === 0 ? PAR.TL : ix === FW - 1 ? PAR.TR : PAR.T); par(ix, FH - 1, ix === 0 ? PAR.BL : ix === FW - 1 ? PAR.BR : PAR.B) }
    for (let iy = 1; iy < FH - 1; iy++) { par(0, iy, PAR.L); if (iy !== saiY && iy !== saiY - 1) par(FW - 1, iy, PAR.R) }
    bloco(W / 2, 8, W, 16); bloco(W / 2, H - 8, W, 16); bloco(8, H / 2, 16, H)
    // muro direito em 2 pedaços (deixa a saída de 2 tiles no meio)
    bloco(W - 8, (saiY - 1) * T / 2, 16, (saiY - 1) * T)
    bloco(W - 8, ((saiY + 1) * T + H) / 2, 16, H - (saiY + 1) * T)

    // --- cenário (casa + árvores) ---
    põe('casa_a', 4 * T, 4 * T, 26)
    for (const [ax, ay] of [[2, 9], [17, 3], [16, 9], [11, 10]]) põe('arvore', ax * T, ay * T, 12)
    põe('toco', 6 * T, 8 * T, 10); põe('carroca', 13 * T, 3 * T, 12)

    // --- HUD + balão ---
    this.hud = this.add.text(10, 8, '', { fontFamily: 'sans-serif', fontSize: '14px', color: '#fff', backgroundColor: '#0009', padding: { x: 7, y: 4 } }).setScrollFactor(0).setDepth(20000)
    this.balao = this.add.text(0, 0, '', { fontFamily: 'sans-serif', fontSize: '11px', color: '#2a1a10', backgroundColor: '#fff', padding: { x: 6, y: 4 }, align: 'center', wordWrap: { width: 150 } }).setOrigin(0.5, 1).setDepth(19000).setVisible(false)

    // --- personagens ---
    const cria = (chave: string, x: number, y: number): Andante => {
      const sombra = this.add.image(x + 1, y + 6, 'sombra').setAlpha(0.6)
      const sp = this.physics.add.sprite(x, y, chave, 0); sp.setDepth(y)
      ;(sp.body as Phaser.Physics.Arcade.Body).setSize(10, 8).setOffset(3, 8)
      return { sp, sombra }
    }
    this.heroi = cria('heroi', W / 2, H - 40)
    this.fazendeiro = cria('fazendeiro', 5 * T, 6 * T)
    ;(this.fazendeiro.sp.body as Phaser.Physics.Arcade.Body).setImmovable(true)
    this.physics.add.collider(this.heroi.sp, solidos)
    this.physics.add.collider(this.heroi.sp, this.fazendeiro.sp)

    // --- os 5 potes de mel (o desafio: juntar/contar) ---
    for (const [mx, my] of [[3, 7], [8, 8], [12, 7], [15, 6], [10, 4]]) {
      const im = this.add.image(mx * T + 8, my * T + 8, 'mel').setDepth(my * T + 8)
      this.tweens.add({ targets: im, y: im.y - 2, duration: 700, yoyo: true, repeat: -1 })  // flutua
      const z = zona(mx * T + 8, my * T + 8, 14, 14)
      this.physics.add.overlap(this.heroi.sp, z, () => this.pegaMel(im, z))
    }

    // --- barreira de pedras na saída (o mundo muda ao entregar) ---
    // DENTRO da moldura (right edge <= W): tamanho e posição pra tampar a saída sem vazar
    this.pedras = this.add.image(W - 26, saiY * T + 8, 'pedras2').setOrigin(0.5, 0.5).setDisplaySize(38, 34).setDepth(19500)
    this.pedrasBloco = bloco(W - 8, saiY * T + 8, 16, 32)
    const zSaida = zona(W - 6, saiY * T + 8, 12, 28); (zSaida.body as Phaser.Physics.Arcade.StaticBody).enable = false
    this.physics.add.overlap(this.heroi.sp, zSaida, () => { if (this.entregou && !this.trocando) this.vitoria() })
    this.zSaida = zSaida

    // --- entrega ao fazendeiro ---
    const zEntrega = zona(5 * T, 6 * T + 6, 22, 16); (zEntrega.body as Phaser.Physics.Arcade.StaticBody).enable = false
    this.physics.add.overlap(this.heroi.sp, zEntrega, () => this.entrega())
    this.zEntrega = zEntrega

    // --- INTERIOR da casa (entrável) ---
    this.montaInterior(solidos)
    const zPorta = zona(4 * T + 8, 4 * T + 4, 12, 8)
    this.physics.add.overlap(this.heroi.sp, zPorta, () => { if (this.local === 'fase') this.entra() })

    // --- câmera: mostra a TELA INTEIRA emoldurada (fundo escuro = a moldura) ---
    this.faseW = W; this.faseH = H
    this.cameras.main.setBounds(0, 0, W, H).setZoom(3).centerOn(W / 2, H / 2)

    // --- música (começa no 1º gesto — política do navegador) ---
    this.musica = this.sound.add('musica', { loop: true, volume: 0.45 })
    const destrava = () => { if (this.musica && !this.musica.isPlaying) this.musica.play() }
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { destrava(); if (this.local === 'fase') this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY) })
    if (this.input.keyboard) {
      this.curs = this.input.keyboard.createCursorKeys()
      this.wasd = this.input.keyboard.addKeys('W,A,S,D') as Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
      this.input.keyboard.on('keydown', destrava)
    }

    this.fala(this.fazendeiro.sp, 'Oi! Preciso de ' + MEL_ALVO + ' potes de mel pra feira. Me ajuda a juntar?')
    this.atualizaHud()
    ;(window as any).__fase1 = this
    ;(window as any).__tp1 = (x: number, y: number) => { this.heroi.sp.setPosition(x, y); this.alvo = null }
    ;(window as any).__anda1 = (x: number, y: number) => { this.alvo = new Phaser.Math.Vector2(x, y) }
  }

  faseW = 0; faseH = 0
  private zEntrega!: Phaser.GameObjects.Rectangle
  private zSaida!: Phaser.GameObjects.Rectangle
  private salaX = 400; private salaY = -260

  private atualizaHud (): void {
    this.hud.setText('🍯 Mel: ' + this.mel + '/' + MEL_ALVO)
  }

  private fala (quem: Phaser.GameObjects.Sprite, txt: string): void {
    this.balao.setText(txt).setPosition(quem.x, quem.y - 20).setVisible(true)
    this.time.delayedCall(3600, () => this.balao.setVisible(false))
  }

  private pegaMel (im: Phaser.GameObjects.Image, z: Phaser.GameObjects.Rectangle): void {
    im.destroy(); (z.body as Phaser.Physics.Arcade.StaticBody).enable = false; z.destroy()
    this.mel++
    this.atualizaHud()
    if (this.mel >= MEL_ALVO) {
      (this.zEntrega.body as Phaser.Physics.Arcade.StaticBody).enable = true
      this.fala(this.heroi.sp, 'Juntei os ' + MEL_ALVO + '! Vou levar ao fazendeiro.')
    }
  }

  private entrega (): void {
    if (this.entregou || this.mel < MEL_ALVO) return
    this.entregou = true
    ;(this.zEntrega.body as Phaser.Physics.Arcade.StaticBody).enable = false
    this.fala(this.fazendeiro.sp, 'Obrigado! Agora o caminho está livre. Vá em frente!')
    // o MUNDO MUDA: as pedras somem e a saída abre
    if (this.pedrasBloco) { (this.pedrasBloco.body as Phaser.Physics.Arcade.StaticBody).enable = false; this.pedrasBloco.destroy() }
    if (this.pedras) this.tweens.add({ targets: this.pedras, alpha: 0, duration: 400, onComplete: () => this.pedras?.destroy() })
    ;(this.zSaida.body as Phaser.Physics.Arcade.StaticBody).enable = true
  }

  private vitoria (): void {
    this.trocando = true
    this.hud.setText('Fase 1 concluída! 🌟  (a próxima fase entra aqui)')
    this.cameras.main.flash(400, 255, 255, 200)
    this.heroi.sp.setVelocity(0, 0); this.alvo = null
  }

  private montaInterior (solidos: Phaser.Physics.Arcade.StaticGroup): void {
    const sx = this.salaX, sy = this.salaY, tw = 9, th = 7, cx = tw >> 1
    const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, BdL: 41, BdR: 42, B: 43, BR: 44, ESC: 50 }
    const dep = (y: number) => 100 + (y - sy)
    const tile = (ix: number, iy: number, fr: number, d: number) => this.add.image(sx + ix * T + 8, sy + iy * T + 8, 'paredes', fr).setDepth(d)
    this.add.rectangle(sx + tw * T / 2, sy + th * T / 2, tw * T + 160, th * T + 160, 0x0e0c12).setDepth(-2)
    for (let iy = -2; iy < th + 2; iy++) for (let ix = -2; ix < tw + 2; ix++) if (!(ix >= 0 && ix < tw && iy >= 0 && iy < th)) tile(ix, iy, PAR.ESC, 0.4)
    for (let px = sx + T; px < sx + (tw - 1) * T; px += 48) for (let py = sy + T; py < sy + (th - 1) * T; py += 48) this.add.image(px, py, 'piso').setOrigin(0).setDepth(-1)
    this.add.image(sx + cx * T, sy + (th - 2) * T, 'piso').setOrigin(0).setDepth(-1).setCrop(0, 0, 16, 32)
    tile(0, 0, PAR.TL, 0.45); tile(tw - 1, 0, PAR.TR, 0.45)
    for (let ix = 1; ix < tw - 1; ix++) tile(ix, 0, PAR.T, 0.45)
    for (let iy = 1; iy < th - 1; iy++) { tile(0, iy, PAR.L, 0.45); tile(tw - 1, iy, PAR.R, 0.45) }
    tile(0, th - 1, PAR.BL, 9000); tile(tw - 1, th - 1, PAR.BR, 9000)
    for (let ix = 1; ix < tw - 1; ix++) { if (ix === cx) continue; tile(ix, th - 1, ix === cx - 1 ? PAR.BdL : ix === cx + 1 ? PAR.BdR : PAR.B, 9000) }
    const b = (x: number, y: number, w: number, h: number) => { const r = this.add.rectangle(x, y, w, h); this.physics.add.existing(r, true); solidos.add(r) }
    b(sx + tw * T / 2, sy + 8, tw * T, 16); b(sx + 4, sy + th * T / 2, 8, th * T); b(sx + tw * T - 4, sy + th * T / 2, 8, th * T)
    b(sx + (cx * T) / 2, sy + (th - 1) * T + 8, cx * T, 16); const wD = (tw - cx - 1) * T; b(sx + (cx + 1) * T + wD / 2, sy + (th - 1) * T + 8, wD, 16)
    b(sx + cx * T + 8, sy + (th + 1) * T + 8, 32, 16)
    this.add.image(sx + 68, sy + 70, 'mundo', 'tapete').setDepth(0.6)
    this.add.image(sx + 34, sy + 46, 'mundo', 'estante').setOrigin(0.5, 1).setDepth(dep(sy + 46)); b(sx + 34, sy + 42, 22, 8)
    this.add.image(sx + 100, sy + 40, 'bau', 0).setOrigin(0.5, 1).setDepth(dep(sy + 40)); b(sx + 100, sy + 36, 14, 8)
    this.add.image(sx + 118, sy + 44, 'jar', 0).setOrigin(0.5, 1).setDepth(dep(sy + 44))
    this.saidaCasa = { x: sx + cx * T + 8, y: sy + (th - 1) * T + 8 }
  }
  private saidaCasa = { x: 0, y: 0 }

  private entra (): void {
    if (this.trocando) return
    this.trocando = true; this.alvo = null; this.heroi.sp.setVelocity(0, 0)
    this.cameras.main.fadeOut(220, 14, 12, 18)
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.local = 'casa'
      this.heroi.sp.setPosition(this.saidaCasa.x, this.saidaCasa.y - 26)
      this.cameras.main.setZoom(4).setBounds(this.salaX - 40, this.salaY - 30, 9 * T + 80, 7 * T + 60).startFollow(this.heroi.sp, true, 0.15, 0.15).centerOn(this.heroi.sp.x, this.heroi.sp.y)
      this.cameras.main.fadeIn(220, 14, 12, 18)
      this.time.delayedCall(380, () => { this.trocando = false })
    })
  }

  private saiCasa (): void {
    if (this.trocando) return
    this.trocando = true; this.alvo = null; this.heroi.sp.setVelocity(0, 0)
    this.cameras.main.fadeOut(220, 14, 12, 18)
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.local = 'fase'
      this.heroi.sp.setPosition(4 * T + 8, 4 * T + 22)
      this.cameras.main.stopFollow(); this.cameras.main.setZoom(3).setBounds(0, 0, this.faseW, this.faseH).centerOn(this.faseW / 2, this.faseH / 2)
      this.cameras.main.fadeIn(220, 14, 12, 18)
      this.time.delayedCall(380, () => { this.trocando = false })
    })
  }

  update (): void {
    const h = this.heroi, VEL = 70
    // dentro de casa: detecta a saída pela porta
    if (this.local === 'casa' && !this.trocando) {
      if (Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.saidaCasa.x, this.saidaCasa.y + 8) < 10) this.saiCasa()
    }
    let kx = 0, ky = 0
    if (this.curs?.left.isDown || this.wasd?.A.isDown) kx -= 1
    if (this.curs?.right.isDown || this.wasd?.D.isDown) kx += 1
    if (this.curs?.up.isDown || this.wasd?.W.isDown) ky -= 1
    if (this.curs?.down.isDown || this.wasd?.S.isDown) ky += 1
    if (kx || ky) { this.alvo = null; const n = Math.hypot(kx, ky); h.sp.setVelocity(kx / n * VEL, ky / n * VEL) }
    else if (this.alvo) { const d = Phaser.Math.Distance.Between(h.sp.x, h.sp.y, this.alvo.x, this.alvo.y); if (d < 4) { this.alvo = null; h.sp.setVelocity(0, 0) } else this.physics.moveTo(h.sp, this.alvo.x, this.alvo.y, VEL) }
    else h.sp.setVelocity(0, 0)

    const vx = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.x, vy = (h.sp.body as Phaser.Physics.Arcade.Body).velocity.y
    if (Math.abs(vx) + Math.abs(vy) > 4) { this.dir = Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 'dir' : 'esq') : (vy > 0 ? 'baixo' : 'cima'); h.sp.play('heroi-anda-' + this.dir, true) }
    else if (h.sp.anims.isPlaying) { h.sp.stop(); h.sp.setFrame(({ baixo: 0, cima: 1, esq: 2, dir: 3 } as Record<string, number>)[this.dir]) }
    h.sp.setDepth(h.sp.y); h.sombra.setPosition(h.sp.x + 1, h.sp.y + 7).setDepth(h.sp.y - 0.5)
    this.fazendeiro.sombra.setPosition(this.fazendeiro.sp.x + 1, this.fazendeiro.sp.y + 7).setDepth(this.fazendeiro.sp.y - 0.5)
    this.fazendeiro.sp.setDepth(this.fazendeiro.sp.y)
  }
}
