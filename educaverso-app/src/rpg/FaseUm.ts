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
  private balaoDom!: HTMLDivElement          // balão em HTML = sempre NÍTIDO (resolução real)
  private balaoAlvo: Phaser.GameObjects.Sprite | null = null
  private balaoAte = 0
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

    // --- HUD (Phaser, nítido com setResolution) ---
    this.hud = this.add.text(10, 8, '', { fontFamily: 'sans-serif', fontSize: '13px', color: '#fff', backgroundColor: '#000a', padding: { x: 7, y: 4 } }).setScrollFactor(0).setResolution(3).setDepth(20000)
    // --- BALÃO em HTML (por cima do canvas) = texto SEMPRE nítido, em qualquer tela ---
    this.balaoDom = document.createElement('div')
    this.balaoDom.style.cssText = 'position:fixed;transform:translate(-50%,-100%);max-width:180px;padding:6px 10px;' +
      'background:#fff;color:#241a12;border-radius:10px;border:2px solid #b98b5e;font-family:system-ui,sans-serif;' +
      'font-size:15px;font-weight:600;line-height:1.25;text-align:center;pointer-events:none;z-index:9998;display:none;' +
      'box-shadow:0 3px 0 rgba(0,0,0,.25);'
    document.body.appendChild(this.balaoDom)
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => this.balaoDom?.remove())
    this.events.once(Phaser.Scenes.Events.DESTROY, () => this.balaoDom?.remove())

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
    for (const [mx, my] of [[3, 7], [8, 8], [12, 7], [15, 6]]) {   // 4 na fase; o 5o fica DENTRO da casa
      const im = this.add.image(mx * T + 8, my * T + 8, 'mel').setDepth(my * T + 8)
      this.tweens.add({ targets: im, y: im.y - 2, duration: 700, yoyo: true, repeat: -1 })  // flutua
      const z = zona(mx * T + 8, my * T + 8, 14, 14)
      this.physics.add.overlap(this.heroi.sp, z, () => this.pegaMel(im, z))
    }

    // --- barreira de pedras: TAPA EXATAMENTE a abertura (2 tiles: y = saiY-1..saiY) ---
    const abreCy = saiY * T                                        // centro vertical da abertura
    this.pedras = this.add.image(W - 22, abreCy, 'pedras2').setOrigin(0.5, 0.5).setDisplaySize(44, 42).setDepth(19500)
    this.pedrasBloco = bloco(W - 8, abreCy, 16, 36)               // colisão cobre a abertura inteira
    const zSaida = zona(W - 6, abreCy, 12, 34); (zSaida.body as Phaser.Physics.Arcade.StaticBody).enable = false
    this.physics.add.overlap(this.heroi.sp, zSaida, () => { if (this.entregou && !this.trocando) this.vitoria() })
    this.zSaida = zSaida

    // --- entrega ao fazendeiro ---
    const zEntrega = zona(5 * T, 6 * T + 6, 22, 16); (zEntrega.body as Phaser.Physics.Arcade.StaticBody).enable = false
    this.physics.add.overlap(this.heroi.sp, zEntrega, () => this.entrega())
    this.zEntrega = zEntrega

    // --- INTERIOR da casa (entrável) ---
    this.montaInterior(solidos)
    const zPorta = zona(4 * T, 4 * T + 2, 14, 12)   // EXATO na porta da casa (bottom-center)
    this.physics.add.overlap(this.heroi.sp, zPorta, () => { if (this.local === 'fase') this.entra() })
    // o 5º pote de mel fica DENTRO da casa (dá motivo pra explorar o interior!)
    const melCasa = this.add.image(this.salaX + 68, this.salaY + 52, 'mel').setDepth(250)   // depth positivo (interior em Y negativo)
    this.tweens.add({ targets: melCasa, y: melCasa.y - 2, duration: 700, yoyo: true, repeat: -1 })
    const zMelCasa = zona(this.salaX + 68, this.salaY + 52, 14, 14)
    this.physics.add.overlap(this.heroi.sp, zMelCasa, () => this.pegaMel(melCasa, zMelCasa))

    // --- câmera: mostra a TELA INTEIRA emoldurada (fundo escuro = a moldura) ---
    this.faseW = W; this.faseH = H
    this.cameras.main.setBounds(0, 0, W, H).setZoom(3).centerOn(W / 2, H / 2)
    // MATTE (moldura preta em cima da tela): cobre TUDO fora do quadro da fase —
    // garante que NADA vaze visualmente (grama/interior/o que for), hoje e sempre.
    for (const [mx, my, mw, mh] of [[512, 44, 1200, 100], [512, 724, 1200, 100], [14, 384, 40, 800], [1010, 384, 40, 800]] as const) {
      this.add.rectangle(mx, my, mw, mh, 0x0e0c12).setScrollFactor(0).setDepth(30000)
    }

    // --- música (começa no 1º gesto — política do navegador) ---
    this.musica = this.sound.add('musica', { loop: true, volume: 0.45 })
    const destrava = () => { if (this.musica && !this.musica.isPlaying) this.musica.play() }
    // BUG corrigido: o toque move o herói em QUALQUER zona (na fase E dentro da casa).
    // Antes só valia na fase -> no celular o herói ficava preso no interior ("travou").
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { destrava(); if (!this.trocando) this.alvo = new Phaser.Math.Vector2(p.worldX, p.worldY) })
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

  // som procedural (Web Audio) — feedback imediato. Placeholder até virem os SFX
  // reais do pack (que ficam na versão itch). Leve, funciona no PC velho.
  private tom (freq: number, dur: number, tipo: OscillatorType = 'sine', vol = 0.18): void {
    const ctx = (this.sound as unknown as { context?: AudioContext }).context
    if (!ctx || ctx.state !== 'running') return
    const o = ctx.createOscillator(), g = ctx.createGain()
    o.type = tipo; o.frequency.value = freq
    o.connect(g); g.connect(ctx.destination)
    const t = ctx.currentTime
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + dur)
    o.start(t); o.stop(t + dur)
  }

  private fala (quem: Phaser.GameObjects.Sprite, txt: string): void {
    this.balaoAlvo = quem
    this.balaoDom.textContent = txt
    this.balaoDom.style.display = 'block'
    this.balaoAte = this.time.now + 3800
    this.posicionaBalao()
  }

  // posiciona o balão HTML EXATAMENTE sobre a cabeça do personagem (world -> tela CSS)
  private posicionaBalao (): void {
    if (this.balaoDom.style.display === 'none' || !this.balaoAlvo) return
    const cam = this.cameras.main
    const sx = (this.balaoAlvo.x - cam.worldView.x) * cam.zoom
    const sy = (this.balaoAlvo.y - 14 - cam.worldView.y) * cam.zoom
    const cb = this.scale.canvasBounds
    const gw = this.scale.gameSize.width, gh = this.scale.gameSize.height
    this.balaoDom.style.left = (cb.left + (sx / gw) * cb.width) + 'px'
    this.balaoDom.style.top = (cb.top + (sy / gh) * cb.height) + 'px'
  }

  private pegaMel (im: Phaser.GameObjects.Image, z: Phaser.GameObjects.Rectangle): void {
    im.destroy(); (z.body as Phaser.Physics.Arcade.StaticBody).enable = false; z.destroy()
    this.mel++
    this.tom(560 + this.mel * 90, 0.13, 'triangle', 0.2)   // 'plim' que sobe a cada pote
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
    // o MUNDO MUDA: as pedras EXPLODEM em cacos e somem aos poucos
    if (this.pedrasBloco) { (this.pedrasBloco.body as Phaser.Physics.Arcade.StaticBody).enable = false; this.pedrasBloco.destroy() }
    ;(this.zSaida.body as Phaser.Physics.Arcade.StaticBody).enable = true
    if (this.pedras) this.explodePedras(this.pedras.x, this.pedras.y)
  }

  // 💥 pedras explodindo: cacos voam (pra DENTRO do quadro, não vazam) + tremida + ronco
  private explodePedras (px: number, py: number): void {
    const cores = [0x8a5a3a, 0xa06b45, 0x6f4630]
    for (let i = 0; i < 16; i++) {
      const s = Phaser.Math.Between(3, 7)
      const caco = this.add.rectangle(px + Phaser.Math.Between(-8, 8), py + Phaser.Math.Between(-16, 16), s, s, cores[i % 3]).setDepth(19600)
      const ang = Phaser.Math.FloatBetween(Math.PI * 0.55, Math.PI * 1.45)   // pra ESQUERDA/cima (dentro do quadro)
      const dist = Phaser.Math.Between(18, 46)
      this.tweens.add({
        targets: caco, x: px + Math.cos(ang) * dist, y: py + Math.sin(ang) * dist + Phaser.Math.Between(6, 22),
        alpha: 0, angle: Phaser.Math.Between(-200, 200), scale: 0.3,
        duration: Phaser.Math.Between(380, 720), ease: 'Quad.easeOut', onComplete: () => caco.destroy()
      })
    }
    // a pedra some encolhendo (não só fade) — parece que desmoronou
    if (this.pedras) this.tweens.add({ targets: this.pedras, scale: 0, alpha: 0, angle: 20, duration: 320, onComplete: () => this.pedras?.destroy() })
    this.cameras.main.shake(260, 0.007)
    this.tom(150, 0.32, 'sawtooth', 0.17); this.time.delayedCall(90, () => this.tom(100, 0.42, 'sawtooth', 0.15))
  }

  private vitoria (): void {
    this.trocando = true
    this.hud.setText('Fase 1 concluída! 🌟  (a próxima fase entra aqui)')
    this.cameras.main.flash(400, 255, 255, 200)
    ;[523, 659, 784, 1047].forEach((f, i) => this.time.delayedCall(i * 110, () => this.tom(f, 0.16, 'triangle', 0.2)))
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

  // transições À PROVA DE FALHA: baseadas em TEMPO (não no evento da câmera, que
  // não dispara em alguns aparelhos e deixava o jogo travado). trocando SEMPRE
  // volta a false — a criança nunca fica presa.
  private transita (aplica: () => void): void {
    if (this.trocando) return
    this.trocando = true; this.alvo = null; this.heroi.sp.setVelocity(0, 0)
    this.balaoDom.style.display = 'none'; this.balaoAlvo = null
    this.cameras.main.fadeOut(200, 14, 12, 18)
    this.time.delayedCall(210, () => {
      aplica()
      this.cameras.main.fadeIn(200, 14, 12, 18)
    })
    this.time.delayedCall(560, () => { this.trocando = false })   // destrava GARANTIDO
  }

  private entra (): void {
    this.transita(() => {
      this.local = 'casa'
      this.heroi.sp.setPosition(this.saidaCasa.x, this.saidaCasa.y - 34)
      this.cameras.main.setZoom(4).setBounds(this.salaX - 40, this.salaY - 30, 9 * T + 80, 7 * T + 60)
      this.cameras.main.startFollow(this.heroi.sp, true, 0.16, 0.16).centerOn(this.heroi.sp.x, this.heroi.sp.y)
    })
  }

  private saiCasa (): void {
    this.transita(() => {
      this.local = 'fase'
      this.heroi.sp.setPosition(4 * T, 4 * T + 26)                 // em frente à porta da casa
      this.cameras.main.stopFollow()
      this.cameras.main.setZoom(3).setBounds(0, 0, this.faseW, this.faseH).centerOn(this.faseW / 2, this.faseH / 2)
    })
  }

  update (): void {
    const h = this.heroi, VEL = 70
    // dentro de casa: detecta a saída pela porta
    if (this.local === 'casa' && !this.trocando) {
      // saída FÁCIL: basta andar até a porta (perto do x dela e na parte de baixo)
      if (Math.abs(h.sp.x - this.saidaCasa.x) < 14 && h.sp.y >= this.saidaCasa.y - 4) this.saiCasa()
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
    // PROFUNDIDADE zone-aware: dentro da casa (Y NEGATIVO) usar depth relativo à sala
    // (senão depth negativo joga o herói PARA BAIXO do piso = INVISÍVEL). Bug real do Marcos.
    const dz = this.local === 'casa' ? (100 + (h.sp.y - this.salaY)) : h.sp.y
    h.sp.setDepth(dz); h.sombra.setPosition(h.sp.x + 1, h.sp.y + 7).setDepth(dz - 0.5)
    // balão HTML: acompanha o personagem e some no tempo
    if (this.balaoDom.style.display !== 'none') { this.posicionaBalao(); if (this.time.now > this.balaoAte) { this.balaoDom.style.display = 'none'; this.balaoAlvo = null } }
    this.fazendeiro.sombra.setPosition(this.fazendeiro.sp.x + 1, this.fazendeiro.sp.y + 7).setDepth(this.fazendeiro.sp.y - 0.5)
    this.fazendeiro.sp.setDepth(this.fazendeiro.sp.y)
  }
}
