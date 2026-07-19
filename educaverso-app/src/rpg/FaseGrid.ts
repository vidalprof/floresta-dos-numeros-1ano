// ============================================================================
// FASE 1 — o NOVO jeito (Tiled + grid-engine). Mesma história do jogo:
// o fazendeiro precisa de 5 potes de mel -> a criança JUNTA (conta) -> entrega ->
// o mundo MUDA (as pedras da saída somem) -> atravessa = vitória. Tem a CASA com
// interior (o 5º pote), árvores, música e som. TUDO com colisão vinda do MAPA
// (ge_collide) — nenhum retângulo de colisão escrito à mão.
// Boot: ?fgrid  ou  window.__BOOT='fgrid'.
// ============================================================================
import Phaser from 'phaser'
import { GridEngine } from 'grid-engine'
import { getKit, type KitVisual } from '../fabrica/kits'

const T = 16
const MEL_ALVO = 5

export class FaseGrid extends Phaser.Scene {
  private gridEngine!: GridEngine
  private heroi!: Phaser.GameObjects.Sprite
  private map!: Phaser.Tilemaps.Tilemap
  private colisao!: Phaser.Tilemaps.TilemapLayer
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
  mel = 0                                   // (QA lê)
  entregou = false                          // (QA lê)
  local: 'fase' | 'casa' = 'fase'           // (QA lê)
  private trocando = false                  // (QA lê) trava breve nas transições
  concluida = false                         // (QA lê)
  private prop: Record<string, number> = {}
  private melSprites: Array<{ x: number, y: number, sp: Phaser.GameObjects.Image }> = []
  private pedrasSp?: Phaser.GameObjects.Image
  private limExterno: number[] = [0, 0, 320, 256]
  private limInterior: number[] = [336, 16, 144, 112]
  private hud!: Phaser.GameObjects.Text
  private balao!: HTMLDivElement
  private audioOk = false

  private mapaKey = 'mapa_grid'
  private melAlvo = MEL_ALVO
  private plano?: { abertura?: string, problema?: string, juntouTudo?: string, entrega?: string, vitoria?: string, emoji?: string, nome?: string }
  private kitId = 'vilarejo'
  private kit!: KitVisual

  constructor () { super('FaseGrid') }

  // recebe um mapa gerado na hora (Fábrica) + os textos do plano + o KIT visual; senão padrão
  init (data?: { mapaKey?: string, plano?: FaseGrid['plano'], kitId?: string }): void {
    if (data?.mapaKey) this.mapaKey = data.mapaKey
    if (data?.plano) this.plano = data.plano
    if (data?.kitId) this.kitId = data.kitId
  }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    this.kit = getKit(this.kitId)
    const im = this.kit.imagens
    // ao TROCAR de kit numa mesma sessão, descarta as texturas do kit anterior
    const anterior = this.game.registry.get('kitCarregado') as string | undefined
    if (anterior && anterior !== this.kit.id) {
      for (const k of ['chao', 'paredes', 'mundo', 'sombra', 'mel', 'pedras2', 'piso', 'heroi', 'fazendeiro', 'bau']) if (this.textures.exists(k)) this.textures.remove(k)
    }
    this.game.registry.set('kitCarregado', this.kit.id)
    this.load.spritesheet('heroi', b + im.heroi, { frameWidth: T, frameHeight: T })
    this.load.spritesheet('fazendeiro', b + im.fazendeiro, { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + im.chao, { frameWidth: T, frameHeight: T })
    this.load.spritesheet('paredes', b + im.paredes, { frameWidth: T, frameHeight: T })
    this.load.image('mundo', b + im.mundo)
    this.load.image('sombra', b + im.sombra)
    this.load.image('mel', b + im.mel)
    this.load.image('pedras2', b + im.pedras)
    this.load.image('piso', b + im.piso)
    this.load.spritesheet('bau', b + im.bau, { frameWidth: this.kit.bauFrame[0], frameHeight: this.kit.bauFrame[1] })
    // só carrega o arquivo padrão; um mapa gerado pela Fábrica já vem no cache (init)
    if (this.mapaKey === 'mapa_grid' && !this.cache.tilemap.has('mapa_grid')) this.load.tilemapTiledJSON('mapa_grid', b + 'mapa_grid.json')
    this.load.audio('musica', b + 'musica.ogg')
  }

  create (): void {
    try { this.montar() } catch (e) {
      ;(window as any).__gridErr = String((e as Error).stack || e)
      console.error('FaseGrid create falhou:', e)
    }
  }

  private P (n: string, d = 0): number { return this.prop[n] ?? d }

  private montar (): void {
    const tex = this.textures.get('mundo')
    for (const [n, [x, y, w, h]] of Object.entries(this.kit.props)) if (!tex.has(n)) tex.add(n, 0, x, y, w, h)

    this.map = this.make.tilemap({ key: this.mapaKey })
    this.map.addTilesetImage('chao', 'chao')
    this.map.addTilesetImage('paredes', 'paredes')
    const cChao = this.map.createLayer('chao', ['chao', 'paredes'], 0, 0)!.setDepth(0)
    this.map.createLayer('muros', ['chao', 'paredes'], 0, 0)!.setDepth(5)
    this.colisao = this.map.createLayer('colisao', ['chao', 'paredes'], 0, 0)!.setVisible(false)
    void cChao

    // propriedades do mapa (tudo é DADO)
    for (const p of (this.map.properties as Array<{ name: string, value: number }>)) this.prop[p.name] = p.value
    const gp = (n: string): any => { const p = (this.map.properties as Array<{ name: string, value: string }>).find(q => q.name === n); return p ? JSON.parse(p.value) : null }
    const melExt: number[][] = gp('melExternos') || []
    const melInt: number[] = gp('melInterno') || []
    this.melAlvo = melExt.length + (melInt.length ? 1 : 0) || MEL_ALVO   // alvo = quantos itens o mapa tem
    const arvores: number[][] = gp('arvores') || []
    const inter = gp('interior') || { x0: 21, y0: 1, w: 9, h: 7 }

    // piso do interior: um AZULEJO (tileSprite) que preenche EXATO o retângulo da sala.
    // (piso.png é 48x48; desenhar 1 por tile de 16 vazava a parede — bug que o Marcos viu.)
    const pisoX = (inter.x0 + 1) * T, pisoY = (inter.y0 + 1) * T
    const pisoW = (inter.w - 2) * T, pisoH = (inter.h - 2) * T
    this.add.tileSprite(pisoX, pisoY, pisoW, pisoH, 'piso').setOrigin(0).setDepth(1)

    // ENFEITES: o motor SÓ RENDERIZA o que o mapa manda (camada 'decor'). Nada de
    // posicionar arte no código — cada objeto traz a figura, a textura e a posição.
    void arvores
    const decor = this.map.getObjectLayer('decor')
    for (const o of (decor?.objects ?? [])) {
      const tex = (o.properties as Array<{ name: string, value: string }> | undefined)?.find(p => p.name === 'tex')?.value ?? 'mundo'
      const frame: string | number = tex === 'mundo' ? (o.name as string) : 0
      this.add.image(o.x!, o.y!, tex, frame).setOrigin(0.5, 1).setDepth(o.y!)
    }

    // PEDRAS que fecham a saída (some na entrega)
    const px = this.P('pedrasX'), py = this.P('pedrasY')
    this.pedrasSp = this.add.image(px * T + T / 2, py * T + T / 2, 'pedras2').setDisplaySize(20, 18).setDepth(py * T + 20)

    // MEL (4 externos + 1 no interior)
    const addMel = (tx: number, ty: number): void => {
      const sp = this.add.image(tx * T + T / 2, ty * T + T / 2, 'mel').setDepth(ty * T + 8)
      this.tweens.add({ targets: sp, y: sp.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
      this.melSprites.push({ x: tx, y: ty, sp })
    }
    for (const [mx, my] of melExt) addMel(mx, my)
    if (melInt.length) addMel(melInt[0], melInt[1])

    // HERÓI + FAZENDEIRO (personagens do grid-engine)
    const sombra = this.add.image(0, 0, 'sombra').setAlpha(0.5).setDepth(1)
    this.heroi = this.add.sprite(0, 0, 'heroi', 0)
    const faz = this.add.sprite(0, 0, 'fazendeiro', 0)
    this.criaAnimacoes()

    this.gridEngine.create(this.map, {
      characters: [
        { id: 'heroi', sprite: this.heroi, startPosition: { x: this.P('heroiX'), y: this.P('heroiY') }, speed: 4, collides: { collisionGroups: ['x'] } },
        { id: 'faz', sprite: faz, startPosition: { x: this.P('fazX'), y: this.P('fazY') }, collides: { collisionGroups: ['x'] } }
      ]
    })
    faz.setDepth(1)  // atualizado no update p/ ordenar por y
    this.events.on('update', () => {
      sombra.setPosition(this.heroi.x + 1, this.heroi.y + 6)
      this.heroi.setDepth(this.heroi.y + 8); faz.setDepth(faz.y + 8)
    })

    // câmera segue o herói, zoom clássico. LIMITES por ambiente = emoldura cada área
    // (externo OU interior), nunca mostra os dois juntos com o vão preto no meio.
    const inter2 = gp('interior') || { x0: 21, y0: 1, w: 9, h: 7 }
    this.limExterno = [0, 0, 20 * T, 16 * T]
    this.limInterior = [inter2.x0 * T, inter2.y0 * T, inter2.w * T, inter2.h * T]
    const cam = this.cameras.main
    cam.setBounds(...(this.limExterno as [number, number, number, number]))
    cam.startFollow(this.heroi, true); cam.setZoom(3); cam.roundPixels = true

    // animação de andar
    this.gridEngine.movementStarted().subscribe(({ charId, direction }) => { if (charId === 'heroi') this.heroi.anims.play(direction, true) })
    this.gridEngine.movementStopped().subscribe(({ charId, direction }) => { if (charId === 'heroi') { this.heroi.anims.stop(); this.heroi.setFrame(this.paradoFrame(direction)) } })
    this.gridEngine.directionChanged().subscribe(({ charId, direction }) => { if (charId === 'heroi') this.heroi.setFrame(this.paradoFrame(direction)) })
    // a cada tile que o herói ENTRA, checa gatilhos (pega mel, porta, entrega, saída)
    this.gridEngine.positionChangeFinished().subscribe(({ charId, enterTile }) => { if (charId === 'heroi') this.aoEntrarTile(enterTile.x, enterTile.y) })

    // HUD + balão (HTML = sempre nítido) + missão inicial
    this.montaHud()
    // ENCENA a abertura da história (narração do mundo) e depois o PEDIDO (o personagem
    // pergunta — Portão 0). Sem roteiro, cai no texto padrão.
    const emoji = this.plano?.emoji ?? '🧑‍🌾'
    const pedido = this.plano?.problema ?? `O fazendeiro precisa de ${this.melAlvo} potes de MEL para a festa! Você me ajuda a juntar?`
    if (this.plano?.abertura) { this.mostraBalao('📖', this.plano.abertura); this.time.delayedCall(3600, () => this.mostraBalao(emoji, pedido)) }
    else this.mostraBalao(emoji, pedido)

    // controles: setas + WASD + toque; e destrava do áudio no 1º gesto
    this.wasd = this.input.keyboard?.addKeys('W,A,S,D') as any
    const destrava = (): void => { if (this.audioOk) return; this.audioOk = true; try { const m = this.sound.add('musica', { loop: true, volume: 0.4 }); m.play() } catch { /* ok */ } }
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { destrava(); const wx = p.worldX, wy = p.worldY; this.gridEngine.moveTo('heroi', { x: Math.floor(wx / T), y: Math.floor(wy / T) }) })
    this.input.keyboard?.on('keydown', destrava)

    // QA hooks (o robô dirige o jogo de verdade)
    ;(window as any).__grid = this
    ;(window as any).__gTile = () => this.gridEngine.getPosition('heroi')
    ;(window as any).__gAnda = (x: number, y: number) => this.gridEngine.moveTo('heroi', { x, y })
    ;(window as any).__gMoving = () => this.gridEngine.isMoving('heroi')
  }

  private aoEntrarTile (tx: number, ty: number): void {
    // pega mel
    const i = this.melSprites.findIndex(m => m.x === tx && m.y === ty)
    if (i >= 0) { const m = this.melSprites[i]; m.sp.destroy(); this.melSprites.splice(i, 1); this.mel++; this.tom(520 + this.mel * 60, 0.12, 'square', 0.15); this.atualizaHud(); if (this.mel >= this.melAlvo) this.mostraBalao(this.plano?.emoji ?? '🍯', this.plano?.juntouTudo ?? `Você juntou os ${this.melAlvo}! Leve ao fazendeiro.`) }
    // entrar na casa: câmera FIXA e centralizada na sala (sala pequena = 1 tela)
    if (this.local === 'fase' && tx === this.P('portaX') && ty === this.P('portaY') && !this.trocando) return this.transita(() => { this.local = 'casa'; this.gridEngine.setPosition('heroi', { x: this.P('intEntraX'), y: this.P('intEntraY') }); this.camInterior() })
    // sair da casa: câmera volta a seguir o herói no EXTERNO
    if (this.local === 'casa' && tx === this.P('intSaiX') && ty === this.P('intSaiY') && !this.trocando) return this.transita(() => { this.local = 'fase'; this.gridEngine.setPosition('heroi', { x: this.P('portaX'), y: this.P('portaY') + 1 }); this.camExterno() })
    // entrega ao fazendeiro (encostar) quando tem os 5
    if (!this.entregou && this.mel >= this.melAlvo && this.local === 'fase') {
      const d = Math.abs(tx - this.P('fazX')) + Math.abs(ty - this.P('fazY'))
      if (d <= 1) this.entrega()
    }
    // vitória: pisou na saída já aberta
    if (this.entregou && !this.concluida && tx === this.P('pedrasX') && ty === this.P('pedrasY')) this.vitoria()
  }

  private entrega (): void {
    this.entregou = true
    // o MUNDO MUDA: as pedras somem (colisão + sprite) e a saída abre
    this.colisao.removeTileAt(this.P('pedrasX'), this.P('pedrasY'))
    if (this.pedrasSp) { this.tweens.add({ targets: this.pedrasSp, scale: 0, alpha: 0, duration: 500, onComplete: () => this.pedrasSp?.destroy() }); this.cameras.main.shake(220, 0.006) }
    this.tom(160, 0.3, 'sawtooth', 0.16)
    this.mostraBalao('🎉', this.plano?.entrega ?? 'Obrigado! A festa está salva. O caminho à direita se abriu — siga!')
    this.atualizaHud()
  }

  private vitoria (): void {
    if (this.concluida) return
    this.concluida = true
    this.cameras.main.flash(400, 255, 255, 200)
    ;[523, 659, 784, 1047].forEach((f, i) => this.time.delayedCall(i * 110, () => this.tom(f, 0.16, 'triangle', 0.2)))
    this.mostraBalao('🌟', this.plano?.vitoria ?? 'Fase 1 concluída! (a próxima aventura entra aqui)')
    this.hud.setText('Missão concluída! 🌟')
  }

  private camInterior (): void {
    const cam = this.cameras.main
    cam.stopFollow()
    cam.removeBounds()   // sem limite = centraliza EXATO na salinha (não gruda na borda do mapa)
    cam.centerOn(this.limInterior[0] + this.limInterior[2] / 2, this.limInterior[1] + this.limInterior[3] / 2)
  }

  private camExterno (): void {
    const cam = this.cameras.main
    cam.setBounds(...(this.limExterno as [number, number, number, number]))
    cam.startFollow(this.heroi, true)
  }

  private transita (aplica: () => void): void {
    if (this.trocando) return
    this.trocando = true
    this.cameras.main.fadeOut(200)
    this.time.delayedCall(210, () => { aplica(); this.cameras.main.fadeIn(200) })
    this.time.delayedCall(560, () => { this.trocando = false })
  }

  // -------- animação / hud / balão / som --------
  private criaAnimacoes (): void {
    const cols = this.kit.personagem.cols, d = this.kit.personagem.dir
    // recria (o kit pode mudar as colunas de direção) — remove o anterior antes
    const mk = (key: string, col: number): void => { if (this.anims.exists(key)) this.anims.remove(key); this.anims.create({ key, frames: [0, 1, 2].map(r => ({ key: 'heroi', frame: r * cols + col })), frameRate: 6, repeat: -1 }) }
    mk('down', d.down); mk('up', d.up); mk('left', d.left); mk('right', d.right)
  }

  private paradoFrame (dir: string): number { const d = this.kit.personagem.dir; return dir === 'up' ? d.up : dir === 'left' ? d.left : dir === 'right' ? d.right : d.down }

  private montaHud (): void {
    this.hud = this.add.text(this.scale.width / 2, this.scale.height - 26, '', { fontFamily: 'Arial', fontSize: '20px', color: '#fff', backgroundColor: '#0009', padding: { x: 10, y: 5 } }).setOrigin(0.5).setScrollFactor(0).setDepth(30000)
    this.balao = document.createElement('div')
    this.balao.style.cssText = 'position:fixed;left:50%;top:14%;transform:translateX(-50%);max-width:80%;background:#fff;color:#123a7a;border-radius:16px;padding:12px 16px;font:600 15px system-ui;text-align:center;box-shadow:0 4px 14px #0007;z-index:9998;display:none;'
    document.body.appendChild(this.balao)
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => this.balao?.remove())
    this.events.once(Phaser.Scenes.Events.DESTROY, () => this.balao?.remove())
    this.atualizaHud()
  }

  private atualizaHud (): void {
    if (this.concluida) return
    const falta = Math.max(0, this.melAlvo - this.mel)
    this.hud.setText(this.entregou ? 'Siga para a saída à direita →' : `Mel: ${this.mel}/${this.melAlvo}` + (falta ? `  (faltam ${falta})` : '  — leve ao fazendeiro!'))
  }

  private balaoTimer?: Phaser.Time.TimerEvent
  private mostraBalao (emoji: string, txt: string): void {
    this.balao.innerHTML = `<span style="font-size:26px">${emoji}</span><br>${txt}`
    this.balao.style.display = 'block'
    this.balaoTimer?.remove()                       // cancela o esconder anterior (senão um balão some cedo)
    this.balaoTimer = this.time.delayedCall(4200, () => { this.balao.style.display = 'none' })
  }

  private tom (freq: number, dur: number, tipo: OscillatorType, vol: number): void {
    try {
      const ctx = (this.sound as any).context as AudioContext; if (!ctx) return
      const o = ctx.createOscillator(), g = ctx.createGain()
      o.type = tipo; o.frequency.value = freq; g.gain.value = vol
      o.connect(g); g.connect(ctx.destination); o.start()
      g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur); o.stop(ctx.currentTime + dur)
    } catch { /* silencioso */ }
  }

  update (): void {
    if (this.trocando || this.concluida || this.gridEngine.isMoving('heroi')) return
    const k = this.input.keyboard?.createCursorKeys(); const w = this.wasd
    if (k?.left.isDown || w?.A.isDown) this.gridEngine.move('heroi', 'left' as any)
    else if (k?.right.isDown || w?.D.isDown) this.gridEngine.move('heroi', 'right' as any)
    else if (k?.up.isDown || w?.W.isDown) this.gridEngine.move('heroi', 'up' as any)
    else if (k?.down.isDown || w?.S.isDown) this.gridEngine.move('heroi', 'down' as any)
  }
}
