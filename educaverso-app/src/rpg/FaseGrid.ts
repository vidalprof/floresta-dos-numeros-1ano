// ============================================================================
// FASE-COBAIA — o NOVO jeito (Tiled + grid-engine).
// Prova a virada que o Marcos aprovou: o mapa é um DADO (mapa_grid.json feito no
// formato Tiled), a colisão vem marcada no tile (ge_collide) e o grid-engine cuida
// do movimento em grade e das colisões. NADA de retângulo de colisão na mão —
// é isso que corta a categoria de bug (parede/afundar/objeto sem colisão).
// Boot: ?fgrid  ou  window.__BOOT='fgrid'.
// ============================================================================
import Phaser from 'phaser'
import { GridEngine } from 'grid-engine'

const T = 16

export class FaseGrid extends Phaser.Scene {
  private gridEngine!: GridEngine
  private heroi!: Phaser.GameObjects.Sprite
  private wasd?: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>
  local: 'fase' | 'casa' = 'fase'          // (QA lê) — por ora só a fase; casa é o próximo passo
  private casa = { x: 3, y: 3 }
  private saidaY = 7

  constructor () { super('FaseGrid') }

  preload (): void {
    const b = import.meta.env.BASE_URL + 'rpg/'
    this.load.spritesheet('heroi', b + 'heroi.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('chao', b + 'chao.png', { frameWidth: T, frameHeight: T })
    this.load.spritesheet('paredes', b + 'paredes.png', { frameWidth: T, frameHeight: T })
    this.load.image('sombra', b + 'sombra.png')
    this.load.image('mundo', b + 'mundo.png')
    this.load.tilemapTiledJSON('mapa_grid', b + 'mapa_grid.json')
  }

  create (): void {
    try { this.montar() } catch (e) {
      ;(window as any).__gridErr = String((e as Error).stack || e)
      console.error('FaseGrid create falhou:', e)
    }
  }

  private montar (): void {
    // registra o recorte da casa na textura 'mundo' (igual a fase antiga faz)
    this.textures.get('mundo').add('casa_a', 0, 0, 0, 64, 48)

    const map = this.make.tilemap({ key: 'mapa_grid' })
    map.addTilesetImage('chao', 'chao')
    map.addTilesetImage('paredes', 'paredes')
    // as duas camadas usam tiles dos dois tilesets — passa os dois
    const cChao = map.createLayer('chao', ['chao', 'paredes'], 0, 0)!
    const cMuros = map.createLayer('muros', ['chao', 'paredes'], 0, 0)!
    cChao.setDepth(0)
    cMuros.setDepth(5)

    // propriedades do mapa (posição inicial, casa, saída) — vêm do DADO, não do código
    const prop = (n: string, d: number): number => {
      const p = (map.properties as Array<{ name: string, value: number }>).find(q => q.name === n)
      return p ? p.value : d
    }
    const hx = prop('heroiX', 10), hy = prop('heroiY', 10)
    this.casa = { x: prop('casaX', 3), y: prop('casaY', 3) }
    this.saidaY = prop('saidaY', 7)

    // CASA: a imagem é desenhada por cima do bloco de colisão (que já está no mapa).
    // porta = tile do meio de baixo do bloco (casaX+1, casaY+1) fica sem colisão no mapa.
    this.add.image(this.casa.x * T + T * 1.5, (this.casa.y + 2) * T, 'mundo', 'casa_a')
      .setOrigin(0.5, 1).setDepth((this.casa.y + 2) * T)

    // herói (sprite 16x16, 4 colunas = direções, 7 linhas = quadros de animação)
    const sombra = this.add.image(0, 0, 'sombra').setAlpha(0.55).setDepth(1)
    this.heroi = this.add.sprite(0, 0, 'heroi', 0)
    this.criaAnimacoes()

    this.gridEngine.create(map, {
      characters: [{ id: 'heroi', sprite: this.heroi, startPosition: { x: hx, y: hy }, speed: 4 }]
    })
    // sombra segue o herói
    this.events.on('update', () => { sombra.setPosition(this.heroi.x + 1, this.heroi.y + 6); this.heroi.setDepth(this.heroi.y) })

    // câmera segue e dá zoom (cabe na tela, estilo clássico)
    const cam = this.cameras.main
    cam.setBounds(0, 0, map.widthInPixels, map.heightInPixels)
    cam.startFollow(this.heroi, true)
    cam.setZoom(3)
    cam.roundPixels = true

    // animação de andar (grid-engine emite os eventos; a gente toca a anim certa)
    this.gridEngine.movementStarted().subscribe(({ direction }) => this.heroi.anims.play(direction, true))
    this.gridEngine.movementStopped().subscribe(({ direction }) => { this.heroi.anims.stop(); this.heroi.setFrame(this.paradoFrame(direction)) })
    this.gridEngine.directionChanged().subscribe(({ direction }) => this.heroi.setFrame(this.paradoFrame(direction)))

    // controles: setas + WASD (o jogo tem que andar no teclado — pedido do Marcos)
    this.wasd = this.input.keyboard?.addKeys('W,A,S,D') as any

    // porta da casa: ao pisar no tile logo ABAIXO da porta, "entra" (por ora só marca)
    // toque/clique: anda na direção do ponto (mobile)
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => this.andaPara(p.worldX, p.worldY))

    // QA hooks (o robô dirige o jogo de verdade)
    ;(window as any).__grid = this
    ;(window as any).__gTile = () => this.gridEngine.getPosition('heroi')
    ;(window as any).__gMove = (dir: string) => this.gridEngine.move('heroi', dir as any)
    ;(window as any).__gAnda = (x: number, y: number) => this.andaTile(x, y)
    ;(window as any).__gMoving = () => this.gridEngine.isMoving('heroi')
  }

  private criaAnimacoes (): void {
    const mk = (key: string, col: number) => {
      if (this.anims.exists(key)) return
      this.anims.create({ key, frames: [0, 1, 2].map(r => ({ key: 'heroi', frame: r * 4 + col })), frameRate: 6, repeat: -1 })
    }
    // colunas: 0=baixo/frente, 1=cima/costas, 2=esquerda, 3=direita
    mk('down', 0); mk('up', 1); mk('left', 2); mk('right', 3)
  }

  private paradoFrame (dir: string): number {
    const col = dir === 'up' ? 1 : dir === 'left' ? 2 : dir === 'right' ? 3 : 0
    return col
  }

  private andaPara (wx: number, wy: number): void {
    const tx = Math.floor(wx / T), ty = Math.floor(wy / T)
    this.andaTile(tx, ty)
  }

  // caminha até um tile alvo (grid-engine acha o caminho e desvia das paredes)
  private andaTile (tx: number, ty: number): void {
    this.gridEngine.moveTo('heroi', { x: tx, y: ty })
  }

  update (): void {
    if (this.gridEngine.isMoving('heroi')) return
    const k = this.input.keyboard?.createCursorKeys()
    const w = this.wasd
    if (k?.left.isDown || w?.A.isDown) this.gridEngine.move('heroi', 'left' as any)
    else if (k?.right.isDown || w?.D.isDown) this.gridEngine.move('heroi', 'right' as any)
    else if (k?.up.isDown || w?.W.isDown) this.gridEngine.move('heroi', 'up' as any)
    else if (k?.down.isDown || w?.S.isDown) this.gridEngine.move('heroi', 'down' as any)
  }
}
