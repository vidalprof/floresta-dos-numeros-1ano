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
import { carrega, salva, registra } from '../fabrica/motor-adaptativo'
import { getAluno, gravarEvidencia } from '../fabrica/evidencias'

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
  private melSprites: Array<{ x: number, y: number, sp: Phaser.GameObjects.Image, v?: number, idx?: number, txt?: Phaser.GameObjects.Text }> = []
  mecanica: 'contar' | 'somar' | 'selecionar' | 'ordenar' | 'agrupar' = 'contar'   // (QA lê)
  alvoSoma = 0                              // somar: a soma exata pedida (QA lê)
  soma = 0                                  // somar: soma atual (QA lê)
  erros = 0                                 // erros REAIS da criança (estouro/regra/ordem) (QA lê)
  kcId = 'contar'                           // domínio é por CONTEÚDO (QA lê)
  coletadosOk = 0                           // selecionar: certos já coletados (QA lê)
  totalOk = 0                               // selecionar: total de certos (QA lê)
  proxOrdem = 1                             // ordenar: próxima posição da sequência (QA lê)
  itens: Array<{ rotulo: string, ok: boolean, ordem?: number }> = []   // (QA lê)
  private melValores: number[][] = []
  private melItensPos: number[][] = []
  // AGRUPAR (lei dos GRUPOS IGUAIS — a criança CRIA a arrumação; sem gabarito)
  agTotal = 0                               // (QA lê) total de itens a repartir
  agCaixas = 0                              // (QA lê) máximo de caixas
  agVagas: Array<{ x: number, y: number, tem: boolean, count: number, img?: Phaser.GameObjects.Image, potes: Phaser.GameObjects.Image[] }> = []   // (QA lê)
  agSoltos: Array<{ x: number, y: number, sp: Phaser.GameObjects.Image }> = []       // (QA lê .length)
  agPilha = { x: 0, y: 0 }
  agPilhaN = 0                              // (QA lê)
  agMao: 'caixa' | 'pote' | null = null     // (QA lê) o que está na mão
  private agMaoSp?: Phaser.GameObjects.Image
  private agPilhaImgs: Phaser.GameObjects.Image[] = []
  private agTesteCd = 0
  private pedrasSp?: Phaser.GameObjects.Image
  private limExterno: number[] = [0, 0, 320, 256]
  private limInterior: number[] = [336, 16, 144, 112]
  private hud!: Phaser.GameObjects.Text
  private balao!: HTMLDivElement
  private btnAjuda?: HTMLButtonElement
  private btnVoz?: HTMLButtonElement
  private audioOk = false
  // telemetria da missão (vira EVIDÊNCIA na vitória)
  nivelAjuda: 0 | 1 | 2 = 0                 // (QA lê) 0=sem; 1=pergunta/botão; 2=gesto ensinado
  ajudaCliques = 0                          // (QA lê)
  private inicioMs = 0
  private ultimaAcao = 0                    // p/ dica por INATIVIDADE (help avoidance)
  private vozLigada = true

  private mapaKey = 'mapa_grid'
  private melAlvo = MEL_ALVO
  private plano?: { abertura?: string, problema?: string, juntouTudo?: string, entrega?: string, vitoria?: string, emoji?: string, nome?: string, regra?: string }
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
      const props = o.properties as Array<{ name: string, value: string | number }> | undefined
      const tex = (props?.find(p => p.name === 'tex')?.value as string) ?? 'mundo'
      const depth = props?.find(p => p.name === 'depth')?.value as number | undefined
      const frame: string | number = tex === 'mundo' ? (o.name as string) : 0
      this.add.image(o.x!, o.y!, tex, frame).setOrigin(0.5, 1).setDepth(depth ?? o.y!)
    }

    // PEDRAS que fecham a saída (some na entrega)
    const px = this.P('pedrasX'), py = this.P('pedrasY')
    this.pedrasSp = this.add.image(px * T + T / 2, py * T + T / 2, 'pedras2').setDisplaySize(20, 18).setDepth(py * T + 20)

    // MECÂNICA da fase (vem do MAPA = dado): contar | somar | selecionar | ordenar
    this.mecanica = (gp('mecanica') as FaseGrid['mecanica']) || 'contar'
    this.kcId = (gp('kc') as string) || this.mecanica
    this.alvoSoma = this.P('alvoSoma', 0)
    this.melValores = (gp('melValores') as number[][]) || []
    this.itens = (gp('itens') as FaseGrid['itens']) || []
    this.melItensPos = (gp('melItens') as number[][]) || []
    this.totalOk = this.itens.filter(i => i.ok).length

    // ITENS no mundo: contar = potes simples; somar = fichas com VALOR; selecionar/ordenar =
    // itens com RÓTULO do conteúdo (a criança testa cada um contra a regra)
    for (const [mx, my] of melExt) this.addMel(mx, my)
    if (melInt.length) this.addMel(melInt[0], melInt[1])
    if (this.mecanica === 'somar') for (const [mx, my, v] of this.melValores) this.addMel(mx, my, v)
    if (this.mecanica === 'selecionar' || this.mecanica === 'ordenar') for (const [mx, my, idx] of this.melItensPos) this.addMelItem(mx, my, idx)
    if (this.mecanica === 'agrupar') this.armaAgrupar(gp)

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
    this.gridEngine.positionChangeFinished().subscribe(({ charId, enterTile }) => { if (charId === 'heroi') { this.ultimaAcao = this.time.now; this.aoEntrarTile(enterTile.x, enterTile.y) } })

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
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { destrava(); this.ultimaAcao = this.time.now; const wx = p.worldX, wy = p.worldY; this.gridEngine.moveTo('heroi', { x: Math.floor(wx / T), y: Math.floor(wy / T) }) })
    this.input.keyboard?.on('keydown', () => { destrava(); this.ultimaAcao = this.time.now })
    this.inicioMs = Date.now()
    this.ultimaAcao = this.time.now

    // QA hooks (o robô dirige o jogo de verdade)
    ;(window as any).__grid = this
    ;(window as any).__gTile = () => this.gridEngine.getPosition('heroi')
    ;(window as any).__gAnda = (x: number, y: number) => this.gridEngine.moveTo('heroi', { x, y })
    ;(window as any).__gMoving = () => this.gridEngine.isMoving('heroi')
  }

  // um pote/ficha no chão; no somar, com o VALOR visível (rótulo nítido acima do item)
  private addMel (tx: number, ty: number, v?: number): void {
    const sp = this.add.image(tx * T + T / 2, ty * T + T / 2, 'mel').setDepth(ty * T + 8)
    this.tweens.add({ targets: sp, y: sp.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
    let txt: Phaser.GameObjects.Text | undefined
    if (v !== undefined) {
      txt = this.add.text(tx * T + T / 2, ty * T - 3, String(v), { fontFamily: 'Arial', fontSize: '9px', color: '#ffffff', stroke: '#1c1206', strokeThickness: 3, resolution: 6 } as any).setOrigin(0.5, 1).setDepth(ty * T + 9)
    }
    this.melSprites.push({ x: tx, y: ty, sp, v, txt })
  }

  // item com RÓTULO do conteúdo (selecionar/ordenar)
  private addMelItem (tx: number, ty: number, idx: number): void {
    const it = this.itens[idx]; if (!it) return
    const sp = this.add.image(tx * T + T / 2, ty * T + T / 2, 'mel').setDepth(ty * T + 8)
    this.tweens.add({ targets: sp, y: sp.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
    const txt = this.add.text(tx * T + T / 2, ty * T - 3, it.rotulo, { fontFamily: 'Arial', fontSize: '9px', color: '#ffffff', stroke: '#1c1206', strokeThickness: 3, resolution: 6 } as any).setOrigin(0.5, 1).setDepth(ty * T + 9)
    this.melSprites.push({ x: tx, y: ty, sp, idx, txt })
  }

  // a meta da fase foi cumprida?
  private metaOk (): boolean {
    if (this.mecanica === 'somar') return this.soma === this.alvoSoma
    if (this.mecanica === 'selecionar') return this.totalOk > 0 && this.coletadosOk === this.totalOk
    if (this.mecanica === 'ordenar') return this.itens.length > 0 && this.proxOrdem > this.itens.length
    if (this.mecanica === 'agrupar') {
      // A LEI (sem gabarito): tudo repartido, ≥2 caixas usadas, TODAS com o mesmo tanto.
      const usadas = this.agVagas.filter(v => v.tem && v.count > 0)
      return this.agSoltos.length === 0 && !this.agMao && usadas.length >= 2 && usadas.every(v => v.count === usadas[0].count)
    }
    return this.mel >= this.melAlvo
  }

  // ---------- AGRUPAR: a criança CRIA a arrumação (grupos iguais) ----------
  private armaAgrupar (gp: (n: string) => any): void {
    this.agTotal = this.P('agTotal', 12)
    this.agCaixas = this.P('agCaixas', 6)
    const vagas: number[][] = gp('agVagas') || []
    const pilha: number[] = gp('agPilha') || [17, 13]
    this.agPilha = { x: pilha[0], y: pilha[1] }
    this.agPilhaN = this.agCaixas
    // marcas das vagas (forma por código = EFEITO, permitido) + pilha de caixas
    const marcas = this.add.graphics().setDepth(2)
    marcas.lineStyle(1, 0xffffff, 0.35)
    for (const [vx, vy] of vagas) {
      marcas.strokeRoundedRect(vx * T + 2, vy * T + 2, T - 4, T - 4, 3)
      this.agVagas.push({ x: vx, y: vy, tem: false, count: 0, potes: [] })
    }
    this.desenhaPilha()
    for (const [ix, iy] of (gp('agItens') || []) as number[][]) {
      const sp = this.add.image(ix * T + T / 2, iy * T + T / 2, 'mel').setDepth(iy * T + 8)
      this.tweens.add({ targets: sp, y: sp.y - 3, duration: 700 + Math.random() * 150, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
      this.agSoltos.push({ x: ix, y: iy, sp })
    }
  }

  private desenhaPilha (): void {
    for (const s of this.agPilhaImgs) s.destroy()
    this.agPilhaImgs = []
    for (let i = 0; i < Math.min(3, this.agPilhaN); i++) {
      this.agPilhaImgs.push(this.add.image(this.agPilha.x * T + T / 2, this.agPilha.y * T + T / 2 - i * 5, 'bau', 0).setDisplaySize(16, 13).setDepth(this.agPilha.y * T + 8 + i))
    }
  }

  private pegaNaMao (tipo: 'caixa' | 'pote'): void {
    this.agMao = tipo
    this.agMaoSp?.destroy()
    this.agMaoSp = tipo === 'pote'
      ? this.add.image(this.heroi.x, this.heroi.y - 12, 'mel').setDisplaySize(10, 10)
      : this.add.image(this.heroi.x, this.heroi.y - 12, 'bau', 0).setDisplaySize(12, 10)
  }

  private soltaMao (): void { this.agMao = null; this.agMaoSp?.destroy(); this.agMaoSp = undefined }

  // interações do agrupar no tile em que a criança ENTROU
  private agTile (tx: number, ty: number): void {
    // pote solto: pega ao passar por cima (mãos vazias) — como o mel de sempre
    if (!this.agMao) {
      const i = this.agSoltos.findIndex(s => s.x === tx && s.y === ty)
      if (i >= 0) {
        const s = this.agSoltos.splice(i, 1)[0]
        s.sp.destroy()
        this.pegaNaMao('pote'); this.tom(620, 0.1, 'square', 0.14); this.atualizaHud()
        return
      }
    }
    // pilha e vaga: só agem quando a criança PARA no tile (decisão, não atropelo —
    // andar POR CIMA de uma caixa a caminho de outra não deposita sem querer)
    const naPilha = tx === this.agPilha.x && ty === this.agPilha.y
    const vaga = this.agVagas.find(v => v.x === tx && v.y === ty)
    if (!naPilha && !vaga) return
    this.time.delayedCall(40, () => {
      if (this.concluida || this.gridEngine.isMoving('heroi')) return
      const pos = this.gridEngine.getPosition('heroi')
      if (pos.x !== tx || pos.y !== ty) return
      if (naPilha) this.agPilhaAcao()
      else if (vaga) this.agVagaAcao(vaga)
    })
  }

  private agPilhaAcao (): void {
    if (!this.agMao && this.agPilhaN > 0) { this.agPilhaN--; this.desenhaPilha(); this.pegaNaMao('caixa'); this.tom(500, 0.1, 'square', 0.14) } else if (this.agMao === 'caixa') { this.soltaMao(); this.agPilhaN++; this.desenhaPilha(); this.tom(380, 0.1, 'square', 0.12) }
    this.atualizaHud()
  }

  private agVagaAcao (v: FaseGrid['agVagas'][number]): void {
    if (this.agMao === 'caixa' && !v.tem) {
      // pousa a caixa na vaga
      this.soltaMao()
      v.tem = true
      v.img = this.add.image(v.x * T + T / 2, v.y * T + T / 2, 'bau', 0).setDisplaySize(16, 13).setDepth(v.y * T + 6)
      this.tom(520, 0.1, 'square', 0.14)
    } else if (this.agMao === 'pote' && v.tem) {
      // deposita 1 pote NESTE grupo (a contagem DO GRUPO sobe — ela vê o grupo crescer)
      this.soltaMao()
      v.count++
      const p = this.add.image(v.x * T + T / 2 + ((v.count % 3) - 1) * 4, v.y * T - 2 - Math.floor((v.count - 1) / 3) * 4, 'mel').setDisplaySize(8, 8).setDepth(v.y * T + 7 + v.count)
      v.potes.push(p)
      this.tom(480 + v.count * 60, 0.11, 'square', 0.15)
    } else if (!this.agMao && v.tem && v.count > 0) {
      // tira 1 de volta (reequilibrar SEM punição)
      const p = v.potes.pop()!; p.destroy(); v.count--
      this.pegaNaMao('pote'); this.tom(430, 0.1, 'square', 0.12)
    } else if (!this.agMao && v.tem && v.count === 0) {
      // caixa vazia: pega a caixa de volta
      v.tem = false; v.img?.destroy(); v.img = undefined
      this.pegaNaMao('caixa')
    }
    this.atualizaHud()
  }

  // o TESTE do fazendeiro quando a arrumação ainda NÃO cumpre a lei (consequência + pergunta)
  private agTesta (): void {
    const usadas = this.agVagas.filter(v => v.tem && v.count > 0)
    const mexeu = this.agVagas.some(v => v.tem) || this.agMao !== null || this.agSoltos.length < this.agTotal
    if (!mexeu) return
    if (this.agSoltos.length > 0 || this.agMao) {
      this.mostraBalao(this.plano?.emoji ?? '🧑‍🌾', 'Ainda tem potes soltos pelo campo! Nenhum pode ficar pra trás.')
      return
    }
    // ANDAIME GRADUAL (pedido do Marcos): no 1º erro o mentor só PERGUNTA (reflexão);
    // do 2º em diante ele ENSINA O GESTO do conserto (tirar da cheia, pôr na magra)
    const repetiu = this.erros >= 1
    if (usadas.length < 2) {
      if (usadas[0]) this.tombaCaixa(usadas[0], 0.6)
      this.erroReal(repetiu
        ? 'Pesada demais de novo! Tenta assim: pare de MÃOS VAZIAS nesta caixa para TIRAR um pote, pegue outra caixa na pilha e reparta.'
        : 'Tudo numa caixa só? Ficou pesada demais — nem consigo levantar! Será que dá pra repartir em mais caixas?')
      return
    }
    // desigual: a(s) caixa(s) DIFERENTE(s) tombam — a consequência mostra ONDE
    const freq: Record<number, number> = {}
    for (const v of usadas) freq[v.count] = (freq[v.count] || 0) + 1
    let moda = usadas[0].count, best = 0
    for (const k of Object.keys(freq)) if (freq[+k] > best) { best = freq[+k]; moda = +k }
    for (const v of usadas) if (v.count !== moda) this.tombaCaixa(v, 1)
    this.erroReal(repetiu
      ? 'Tombou de novo! Tenta assim: pare de MÃOS VAZIAS na caixa mais CHEIA para tirar um pote, e leve ele até uma caixa com MENOS. Quando todas tiverem o mesmo tanto, me chama!'
      : 'Opa! Na hora de carregar, uma caixa tombou… Por que será que ELA tombou e as outras não?')
  }

  // CONSEQUÊNCIA VISÍVEL (pedido do Marcos): a caixa TOMBA de verdade (deita) e os
  // potes ESCORREGAM pra fora; depois de a criança VER o estrago, tudo volta ao
  // lugar sozinho — o trabalho dela nunca se perde, só a LIÇÃO fica
  private tombaCaixa (v: FaseGrid['agVagas'][number], forca: number): void {
    const box = v.img
    if (!box) return
    const orig = v.potes.map(p => ({ p, x: p.x, y: p.y, a: p.angle }))
    const bx = { x: box.x, a: box.angle }
    this.tweens.add({ targets: box, angle: 74 * forca, x: box.x + 4, duration: 300, ease: 'Quad.in' })
    v.potes.forEach((p, i) => this.tweens.add({ targets: p, x: p.x + 9 + i * 5, y: v.y * T + T / 2 + 3, angle: 90, duration: 420, ease: 'Bounce.out', delay: 150 + i * 60 }))
    this.tom(170, 0.28, 'sawtooth', 0.15)
    this.time.delayedCall(2300, () => {
      if (!box.scene) return
      this.tweens.add({ targets: box, angle: bx.a, x: bx.x, duration: 240 })
      for (const o of orig) this.tweens.add({ targets: o.p, x: o.x, y: o.y, angle: o.a, duration: 240 })
    })
  }

  // CONSOLIDAÇÃO (pedido do Marcos): antes de aprovar, o fazendeiro CONFERE caixa
  // por caixa contando JUNTO com a criança (4… 8… 12) — a lição é dita com todas as
  // letras no final, não só descoberta (institucionalização do saber)
  private agConferindo = false
  private agConfere (): void {
    if (this.agConferindo || this.entregou) return
    this.agConferindo = true
    const usadas = this.agVagas.filter(v => v.tem && v.count > 0)
    const k = usadas[0]?.count ?? 0
    this.mostraBalao(this.plano?.emoji ?? '🧑‍🌾', 'Deixa eu conferir! Vamos contar juntos, caixa por caixa…', 8000)
    usadas.forEach((v, i) => {
      this.time.delayedCall(700 + i * 800, () => {
        for (const a of [v.img, ...v.potes].filter(Boolean) as Phaser.GameObjects.Image[]) this.tweens.add({ targets: a, scale: a.scale * 1.25, duration: 150, yoyo: true })
        this.tom(500 + i * 100, 0.15, 'triangle', 0.2)
        const t = this.add.text(v.x * T + T / 2, v.y * T - 12, String(k * (i + 1)), { fontFamily: 'Arial', fontSize: '11px', color: '#ffffff', stroke: '#7a4a12', strokeThickness: 3, resolution: 6 } as any).setOrigin(0.5, 1).setDepth(30000)
        this.tweens.add({ targets: t, y: t.y - 7, alpha: { from: 1, to: 0 }, delay: 1000, duration: 450, onComplete: () => t.destroy() })
      })
    })
    this.time.delayedCall(700 + usadas.length * 800 + 300, () => { this.agConferindo = false; this.entrega(); this.agCarrega() })
  }

  // o FINAL da história acontece na frente da criança: a carga aprovada é CARREGADA
  // na carroça (causa e efeito completos — arrumou certo, a carroça leva)
  private agCarrega (): void {
    const cx = this.P('carrocaX', 0), cy = this.P('carrocaY', 0)
    if (!cx) return
    const usadas = this.agVagas.filter(v => v.tem && v.count > 0)
    usadas.forEach((v, i) => {
      for (const a of [v.img, ...v.potes].filter(Boolean) as Phaser.GameObjects.Image[]) {
        this.time.delayedCall(300 + i * 260, () => a.setDepth(cy * T + 30 + i))
        this.tweens.add({ targets: a, x: cx * T + T / 2 + (i - usadas.length / 2) * 3, y: cy * T + 2 - i * 3 + (a === v.img ? 0 : -5), scale: a.scale * 0.8, duration: 700, delay: 300 + i * 260, ease: 'Quad.inOut' })
      }
    })
  }

  private aoEntrarTile (tx: number, ty: number): void {
    // AGRUPAR: pegar/pousar/repartir por tile (a lei julga no fazendeiro)
    if (this.mecanica === 'agrupar' && !this.concluida) {
      this.agTile(tx, ty)
      if (!this.entregou && this.local === 'fase' && !this.metaOk()) {
        const d = Math.abs(tx - this.P('fazX')) + Math.abs(ty - this.P('fazY'))
        if (d <= 1 && this.time.now > this.agTesteCd) { this.agTesteCd = this.time.now + 3000; this.agTesta() }
      }
    }
    // pega mel/ficha/item
    const i = this.melSprites.findIndex(m => m.x === tx && m.y === ty)
    if (i >= 0) {
      const m = this.melSprites[i]
      m.sp.destroy(); m.txt?.destroy(); this.melSprites.splice(i, 1)
      if (this.mecanica === 'somar') this.pegaFicha(m.v ?? 0)
      else if (this.mecanica === 'selecionar') this.pegaItemRegra(m)
      else if (this.mecanica === 'ordenar') this.pegaItemOrdem(m)
      else { this.mel++; this.tom(520 + this.mel * 60, 0.12, 'square', 0.15); this.atualizaHud(); if (this.mel >= this.melAlvo) this.mostraBalao(this.plano?.emoji ?? '🍯', this.plano?.juntouTudo ?? `Você juntou os ${this.melAlvo}! Leve ao fazendeiro.`) }
    }
    // entrar na casa: câmera FIXA e centralizada na sala (sala pequena = 1 tela)
    if (this.local === 'fase' && tx === this.P('portaX') && ty === this.P('portaY') && !this.trocando) return this.transita(() => { this.local = 'casa'; this.gridEngine.setPosition('heroi', { x: this.P('intEntraX'), y: this.P('intEntraY') }); this.camInterior() })
    // sair da casa: câmera volta a seguir o herói no EXTERNO
    if (this.local === 'casa' && tx === this.P('intSaiX') && ty === this.P('intSaiY') && !this.trocando) return this.transita(() => { this.local = 'fase'; this.gridEngine.setPosition('heroi', { x: this.P('portaX'), y: this.P('portaY') + 1 }); this.camExterno() })
    // entrega ao fazendeiro (encostar) quando a meta está cumprida; no agrupar,
    // primeiro vem a CONFERÊNCIA contada (consolidação), depois a entrega
    if (!this.entregou && this.metaOk() && this.local === 'fase') {
      const d = Math.abs(tx - this.P('fazX')) + Math.abs(ty - this.P('fazY'))
      if (d <= 1) { if (this.mecanica === 'agrupar') this.agConfere(); else this.entrega() }
    }
    // vitória: pisou na saída já aberta
    if (this.entregou && !this.concluida && tx === this.P('pedrasX') && ty === this.P('pedrasY')) this.vitoria()
  }

  // SOMAR: pegou uma ficha de valor v. Fechou exato = clímax; PASSOU = ERRO REAL
  // (falha produtiva: registra no domínio, o mentor PERGUNTA, e as fichas voltam).
  private pegaFicha (v: number): void {
    this.soma += v
    this.tom(420 + this.soma * 24, 0.12, 'square', 0.15)
    if (this.soma === this.alvoSoma) {
      this.mostraBalao(this.plano?.emoji ?? '🧑‍🌾', this.plano?.juntouTudo ?? `Exatamente ${this.alvoSoma}! Fechou a conta — leve pra mim!`)
    } else if (this.soma > this.alvoSoma) {
      const estourou = this.soma
      this.erroReal(`Passou! Deu ${estourou}, e eu preciso de ${this.alvoSoma}. Quanto passou? Quais fichas fecham a conta certinha?`)
      this.soma = 0
      // as fichas VOLTAM (errar = tentar de novo sem punição — nunca "game over")
      for (const m of this.melSprites) { m.sp.destroy(); m.txt?.destroy() }
      this.melSprites = []
      for (const [mx, my, val] of this.melValores) this.addMel(mx, my, val)
    }
    this.atualizaHud()
  }

  // ERRO REAL (falha produtiva): registra no domínio, o mentor PERGUNTA — nunca pune.
  // Telemetria: 1º erro = viu a pergunta (nível 1); 2º+ = recebeu o gesto (nível 2).
  private erroReal (pergunta: string): void {
    this.erros++
    this.nivelAjuda = Math.max(this.nivelAjuda, this.erros >= 2 ? 2 : 1) as FaseGrid['nivelAjuda']
    try { salva('local', registra(carrega('local'), this.kcId, false, Date.now())) } catch { /* sem storage */ }
    this.cameras.main.shake(200, 0.006); this.tom(150, 0.3, 'sawtooth', 0.16)
    this.mostraBalao('🤔', pergunta)
  }

  // SELECIONAR: só entra quem obedece a REGRA do conteúdo. Errado = erro real + o item volta.
  private pegaItemRegra (m: { x: number, y: number, idx?: number }): void {
    const it = this.itens[m.idx ?? -1]; if (!it) return
    if (it.ok) {
      this.coletadosOk++
      this.tom(500 + this.coletadosOk * 70, 0.12, 'square', 0.15)
      if (this.metaOk()) this.mostraBalao(this.plano?.emoji ?? '🧺', this.plano?.juntouTudo ?? 'Separou exatamente os certos! Traz aqui!')
    } else {
      this.erroReal(`"${it.rotulo}"? Hmm… será que entra mesmo em ${this.plano?.regra ?? 'nossa regra'}? Pensa e tenta de novo!`)
      this.time.delayedCall(900, () => { if (!this.concluida) this.addMelItem(m.x, m.y, m.idx ?? 0) })   // o item VOLTA
    }
    this.atualizaHud()
  }

  // ORDENAR: só entra o PRÓXIMO da sequência. Fora de ordem = erro real + o item volta.
  private pegaItemOrdem (m: { x: number, y: number, idx?: number }): void {
    const it = this.itens[m.idx ?? -1]; if (!it) return
    if (it.ordem === this.proxOrdem) {
      this.proxOrdem++
      this.tom(440 + this.proxOrdem * 80, 0.12, 'square', 0.15)
      if (this.metaOk()) this.mostraBalao(this.plano?.emoji ?? '📏', this.plano?.juntouTudo ?? 'Sequência perfeita! Traz aqui!')
    } else {
      this.erroReal(`"${it.rotulo}" agora? Olha a regra: ${this.plano?.regra ?? 'a ordem certa'}. O que vem ANTES dele?`)
      this.time.delayedCall(900, () => { if (!this.concluida) this.addMelItem(m.x, m.y, m.idx ?? 0) })   // o item VOLTA
    }
    this.atualizaHud()
  }

  private entrega (): void {
    this.entregou = true
    // o MUNDO MUDA: as pedras somem (colisão + sprite) e a saída abre
    this.colisao.removeTileAt(this.P('pedrasX'), this.P('pedrasY'))
    if (this.pedrasSp) { this.tweens.add({ targets: this.pedrasSp, scale: 0, alpha: 0, duration: 500, onComplete: () => this.pedrasSp?.destroy() }); this.cameras.main.shake(220, 0.006) }
    this.tom(160, 0.3, 'sawtooth', 0.16)
    let msg = this.plano?.entrega ?? 'Obrigado! A festa está salva. O caminho à direita se abriu — siga!'
    if (this.mecanica === 'agrupar') {
      // o CONCEITO por ÚLTIMO, nascido da arrumação DELA — e agora DITO com todas
      // as letras (consolidação): grupos iguais têm nome, é MULTIPLICAR
      const u = this.agVagas.filter(v => v.tem && v.count > 0)
      if (u.length) msg = `Deu certinho: ${u.length} caixas com ${u[0].count} potes cada. Fazer grupos IGUAIS tem nome — é MULTIPLICAR: ${u.length}×${u[0].count}=${this.agTotal}! ` + msg
    }
    this.mostraBalao('🎉', msg)
    this.atualizaHud()
  }

  private vitoria (): void {
    if (this.concluida) return
    this.concluida = true
    // MEDE + ADAPTA: registra o domínio do KC do CONTEÚDO jogado. Os ERROS já entraram um a
    // um (estouro/regra/ordem = observação negativa); concluir = observação positiva.
    try { salva('local', registra(carrega('local'), this.kcId, true, Date.now())) } catch { /* sem storage: segue */ }
    // EVIDÊNCIA (stealth assessment): a missão inteira vira UM registro por habilidade
    // no Firebase (ou fila local) — o insumo do parecer descritivo do professor
    try {
      const aluno = getAluno()
      if (aluno) {
        const u = this.agVagas.filter(v => v.tem && v.count > 0)
        void gravarEvidencia({
          nome: aluno.nome, turma: aluno.turma, kc: this.kcId,
          atividade: this.plano?.nome ?? 'fase', mecanica: this.mecanica,
          estrategia: this.mecanica === 'agrupar' && u.length ? `${u.length}×${u[0].count}` : undefined,
          alvo: this.mecanica === 'agrupar' ? this.agTotal : (this.mecanica === 'somar' ? this.alvoSoma : this.melAlvo),
          tentativas: this.erros + 1, erros: this.erros,
          nivelAjuda: this.nivelAjuda, ajudaCliques: this.ajudaCliques,
          duracaoSeg: Math.round((Date.now() - this.inicioMs) / 1000),
          pKnown: Math.round(((carrega('local')[this.kcId]?.pKnown) ?? 0) * 100) / 100,
          quando: new Date().toISOString()
        })
      }
    } catch { /* evidência nunca pode travar a festa */ }
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
    // BOTÃO DE AJUDA (pedido do Marcos): a criança revê a missão a QUALQUER momento
    this.btnAjuda = document.createElement('button')
    this.btnAjuda.textContent = '❓'
    this.btnAjuda.setAttribute('aria-label', 'Ajuda: rever a missão')
    this.btnAjuda.style.cssText = 'position:fixed;right:12px;top:12px;width:48px;height:48px;border:0;border-radius:50%;background:#fff;font-size:24px;line-height:1;box-shadow:0 3px 10px #0006;cursor:pointer;z-index:9998;'
    this.btnAjuda.onclick = () => this.mostraAjuda(true)
    document.body.appendChild(this.btnAjuda)
    // BOTÃO DE VOZ (Sesame/NN-g: criança de 6-9 não lê — o balão FALA; aqui liga/desliga)
    try { this.vozLigada = localStorage.getItem('educ_voz') !== '0' } catch { /* padrão ligado */ }
    this.btnVoz = document.createElement('button')
    this.btnVoz.textContent = this.vozLigada ? '🔊' : '🔇'
    this.btnVoz.setAttribute('aria-label', 'Ligar/desligar a voz')
    this.btnVoz.style.cssText = 'position:fixed;right:12px;top:68px;width:48px;height:48px;border:0;border-radius:50%;background:#fff;font-size:22px;line-height:1;box-shadow:0 3px 10px #0006;cursor:pointer;z-index:9998;'
    this.btnVoz.onclick = () => {
      this.vozLigada = !this.vozLigada
      this.btnVoz!.textContent = this.vozLigada ? '🔊' : '🔇'
      try { localStorage.setItem('educ_voz', this.vozLigada ? '1' : '0'); if (!this.vozLigada) speechSynthesis.cancel() } catch { /* ok */ }
    }
    document.body.appendChild(this.btnVoz)
    const limpa = (): void => { this.balao?.remove(); this.btnAjuda?.remove(); this.btnVoz?.remove(); try { speechSynthesis.cancel() } catch { /* ok */ } }
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, limpa)
    this.events.once(Phaser.Scenes.Events.DESTROY, limpa)
    this.atualizaHud()
  }

  // fala o texto do balão (Web Speech, grátis, pt-BR) — desligável no 🔇
  private falar (txt: string): void {
    if (!this.vozLigada || (navigator as any).webdriver) return
    try {
      speechSynthesis.cancel()
      const u = new SpeechSynthesisUtterance(txt.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim())
      u.lang = 'pt-BR'; u.rate = 0.96; u.pitch = 1.05
      speechSynthesis.speak(u)
    } catch { /* sem voz: segue no texto */ }
  }

  // AJUDA sob demanda: repete o PROBLEMA e diz COMO agir AGORA (por mecânica e estado)
  mostraAjuda (pedidaPelaCrianca = false): void {
    if (pedidaPelaCrianca) { this.ajudaCliques++; this.nivelAjuda = Math.max(this.nivelAjuda, 1) as FaseGrid['nivelAjuda'] }
    const emoji = this.plano?.emoji ?? '🧑‍🌾'
    if (this.concluida) { this.mostraBalao('🌟', this.plano?.vitoria ?? 'Missão concluída!', 6000); return }
    if (this.entregou) { this.mostraBalao(emoji, 'Missão cumprida! Agora siga pela saída à DIREITA, onde as pedras sumiram.', 7000); return }
    const problema = this.plano?.problema ?? `O fazendeiro precisa de ${this.melAlvo} potes de MEL! Você ajuda?`
    let como = ''
    if (this.mecanica === 'agrupar') {
      const usadas = this.agVagas.filter(v => v.tem && v.count > 0)
      const desigual = this.agSoltos.length === 0 && !this.agMao && usadas.length >= 2 && !usadas.every(v => v.count === usadas[0].count)
      como = desigual
        ? `Tem caixa com MAIS potes que as outras (olhe os números embaixo: ${usadas.map(v => v.count).join(' | ')}). Pare de MÃOS VAZIAS na caixa mais cheia para TIRAR um pote, e leve ele até uma caixa com menos. Iguais? Vem falar comigo!`
        : `1) Pare na PILHA de caixas para pegar uma. 2) Pare numa marquinha branca para pousar a caixa. 3) Pegue um pote e pare numa caixa para guardar. Reparta TODOS os potes igualzinho (use 2 caixas ou mais!). 4) No fim, venha falar comigo.`
    } else if (this.mecanica === 'somar') {
      como = `Pegue fichas que somem exatamente ${this.alvoSoma}. Você está com ${this.soma}. Se passar, as fichas voltam — tente outra combinação.`
    } else if (this.mecanica === 'selecionar') {
      como = `Pegue SÓ o que obedece a regra${this.plano?.regra ? ' (' + this.plano.regra + ')' : ''}. Já pegou ${this.coletadosOk} de ${this.totalOk}.`
    } else if (this.mecanica === 'ordenar') {
      como = `Pegue os itens NA ORDEM certa${this.plano?.regra ? ' (' + this.plano.regra + ')' : ''}. Agora vem o ${this.proxOrdem}º.`
    } else {
      como = `Ande até cada pote para pegar (já tem ${this.mel} de ${this.melAlvo} — espia dentro da casinha também!). Depois traga pra mim.`
    }
    this.mostraBalao(emoji, `${problema}<br><b>Como fazer:</b> ${como}`, 9000)
  }

  private atualizaHud (): void {
    if (this.concluida) return
    if (this.entregou) { this.hud.setText('Siga para a saída à direita →'); return }
    if (this.mecanica === 'somar') {
      const falta = this.alvoSoma - this.soma
      this.hud.setText(`Soma: ${this.soma} de ${this.alvoSoma}` + (falta > 0 ? `  (faltam ${falta})` : '  — leve ao fazendeiro!'))
      return
    }
    if (this.mecanica === 'selecionar') {
      this.hud.setText(`Certos: ${this.coletadosOk} de ${this.totalOk}` + (this.metaOk() ? '  — leve ao fazendeiro!' : ''))
      return
    }
    if (this.mecanica === 'ordenar') {
      this.hud.setText(`Na ordem: ${this.proxOrdem - 1} de ${this.itens.length}` + (this.metaOk() ? '  — leve ao fazendeiro!' : ''))
      return
    }
    if (this.mecanica === 'agrupar') {
      const u = this.agVagas.filter(v => v.tem)
      const contas = u.map(v => v.count).join(' | ')
      this.hud.setText((u.length ? `Caixas: ${contas}` : 'Pegue caixas na pilha e reparta os potes') + (this.metaOk() ? '  — mostre ao fazendeiro!' : ''))
      return
    }
    const falta = Math.max(0, this.melAlvo - this.mel)
    this.hud.setText(`Mel: ${this.mel}/${this.melAlvo}` + (falta ? `  (faltam ${falta})` : '  — leve ao fazendeiro!'))
  }

  private balaoTimer?: Phaser.Time.TimerEvent
  private mostraBalao (emoji: string, txt: string, ms = 4200): void {
    this.balao.innerHTML = `<span style="font-size:26px">${emoji}</span><br>${txt}`
    this.balao.style.display = 'block'
    this.falar(txt)
    this.balaoTimer?.remove()                       // cancela o esconder anterior (senão um balão some cedo)
    this.balaoTimer = this.time.delayedCall(ms, () => { this.balao.style.display = 'none' })
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
    // o que está na MÃO acompanha a criança (pote/caixa sobre a cabeça)
    if (this.agMaoSp) this.agMaoSp.setPosition(this.heroi.x, this.heroi.y - 12).setDepth(this.heroi.depth + 1)
    // DICA POR INATIVIDADE (help avoidance — quem mais precisa não clica no ❓):
    // criança parada ~25s sem concluir -> o mentor se oferece sozinho
    if (!this.concluida && !this.trocando && !this.agConferindo && this.ultimaAcao > 0 && this.time.now - this.ultimaAcao > 25000 && !(navigator as any).webdriver) {
      this.ultimaAcao = this.time.now
      this.mostraAjuda()
    }
    if (this.trocando || this.concluida || this.gridEngine.isMoving('heroi')) return
    const k = this.input.keyboard?.createCursorKeys(); const w = this.wasd
    if (k?.left.isDown || w?.A.isDown) this.gridEngine.move('heroi', 'left' as any)
    else if (k?.right.isDown || w?.D.isDown) this.gridEngine.move('heroi', 'right' as any)
    else if (k?.up.isDown || w?.W.isDown) this.gridEngine.move('heroi', 'up' as any)
    else if (k?.down.isDown || w?.S.isDown) this.gridEngine.move('heroi', 'down' as any)
  }
}
