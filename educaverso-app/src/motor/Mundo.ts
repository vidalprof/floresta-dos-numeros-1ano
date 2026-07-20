// ============================================================================
// O MONTADOR v2 — o coração da FÁBRICA DE MUNDOS.
// Recebe uma AVENTURA (grafo de ZONAS, validado por Zod) e ARMA o mundo vivo:
//  - cada zona = PRANCHA PINTADA por IA maior que a tela (câmera explora)
//  - PORTAIS ligam as zonas (porta da cabana, trilha, saída) com fade
//  - MISSÃO acontece DENTRO do mundo (a criança age nos objetos da cena)
//  - personagens ANIMADOS (cartela de poses) + vida ambiente (sol, pólen,
//    lareira, música) + voz por API (mp3) + memória (o mundo LEMBRA da criança)
// Trocar de aventura/zona = trocar os DADOS. A máquina é a mesma.
// ============================================================================
import Phaser from 'phaser'
import { Personagem } from './Personagem'
import { auditar } from './auditor'
import { abrir as abrirMecanica, temMecanica } from './mecanicas'
import { carrega, salva, registra } from '../fabrica/motor-adaptativo'
import type { TAventura, TZona, TObjeto, TPortal } from './aventura'

// a missão 'agrupar' tipada (ramo do união discriminada)
type TMissaoAgrupar = Extract<NonNullable<TZona['missao']>, { tipo: 'agrupar' }>
type TMissaoColher = Extract<NonNullable<TZona['missao']>, { tipo: 'colher' }>
// uma caixa/grupo no mundo (vaga + cesta pousada + o tanto que ela tem)
interface VagaCaixa { x: number, y: number, img: Phaser.GameObjects.Image | null, count: number, frutas: Phaser.GameObjects.Image[], marca?: Phaser.GameObjects.Image, livre?: boolean }

const VW = 1024, VH = 768
const QA = new URLSearchParams(location.search).get('qa')
function el (id: string) { return document.getElementById(id) }

export class Mundo extends Phaser.Scene {
  av!: TAventura
  zona!: TZona
  heroi!: Personagem
  corpo!: Phaser.GameObjects.Rectangle
  npcs: Personagem[] = []
  npcPorNome: { [n: string]: Personagem } = {}
  obst!: Phaser.Physics.Arcade.StaticGroup
  cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  teclas!: any
  alvo: { x: number, y: number } | null = null
  travadoT = 0                       // tap-to-move: cancela alvo se ficar preso
  ultX = 0; ultY = 0
  estado = 'explora'
  poeira!: Phaser.GameObjects.Particles.ParticleEmitter
  falado: { [id: string]: boolean } = {}
  balao!: Phaser.GameObjects.Container
  balaoTxt!: Phaser.GameObjects.Text
  balaoNome!: Phaser.GameObjects.Text
  typeTimer: Phaser.Time.TimerEvent | null = null
  falas: { [id: string]: { quem: string, texto: string, cor: string } } = {}
  audioOk: { [id: string]: boolean } = {}
  paradaAtiva: string | null = null
  // missão colher
  itens: Phaser.GameObjects.Image[] = []
  colhidas = 0
  brilho!: Phaser.GameObjects.Image   // UM brilho compartilhado (orçamento GPU)
  numerao!: Phaser.GameObjects.Text
  portalCd = 0
  musicaSom: Phaser.Sound.BaseSound | null = null
  // gramática problema->item->entrega->mundo muda
  objPorId: { [id: string]: { img: Phaser.GameObjects.Image, alt: number } } = {}
  bloqPorId: { [id: string]: Phaser.GameObjects.Rectangle } = {}
  mochila: { asset: string, nome: string } | null = null
  hudItem: Phaser.GameObjects.Image | null = null
  hudItemTxt: Phaser.GameObjects.Text | null = null
  entregou: { [n: string]: boolean } = {}
  // missão "agrupar" (lei dos GRUPOS IGUAIS — a criança CRIA a arrumação)
  vagasC: VagaCaixa[] = []
  soltasAg: Phaser.GameObjects.Image[] = []
  carregando: { tipo: 'maca' | 'cesta', img: Phaser.GameObjects.Image } | null = null
  tiraDe: VagaCaixa | null = null      // tocou numa cesta = quer mexer NELA
  pilhaN = 0
  pilhaImgs: Phaser.GameObjects.Image[] = []
  pilhaLivre = true          // a pilha age 1x por visita (sair e voltar = agir de novo)
  pegaCd = 0
  testeCd = 0

  constructor () { super('Mundo') }

  init (dados: { aventura: TAventura, zonaId?: string, spawn?: { x: number, y: number } }) {
    this.av = dados.aventura
    const id = dados.zonaId || this.av.zona_inicial
    this.zona = this.av.zonas.find(z => z.id === id)!
    this.spawnPt = dados.spawn || this.av.inicio
    // zera estado por zona (a cena é reiniciada a cada portal)
    this.npcs = []; this.npcPorNome = {}; this.itens = []; this.colhidas = 0
    this.falas = {}; this.audioOk = {}; this.falado = {}; this.alvo = null
    this.estado = 'explora'; this.paradaAtiva = null; this.musicaSom = null
    this.objPorId = {}; this.bloqPorId = {}; this.hudItem = null; this.hudItemTxt = null; this.entregou = {}
    this.vagasC = []; this.soltasAg = []; this.carregando = null; this.tiraDe = null
    this.pilhaN = 0; this.pilhaImgs = []; this.pilhaLivre = true; this.pegaCd = 0; this.testeCd = 0
  }
  spawnPt!: { x: number, y: number }

  // ---- memória (o mundo LEMBRA da criança) ----
  mem (): any { try { return JSON.parse(localStorage.getItem('ev_' + this.av.id) || '{}') } catch (e) { return {} } }
  memSalva (m: any) { try { localStorage.setItem('ev_' + this.av.id, JSON.stringify(m)) } catch (e) {} }
  missaoFeita () { return !!(this.mem().missoes || {})[this.zona.id] }

  preload () {
    const z = this.zona
    if (z.prancha) this.load.image('prancha_' + z.id, 'img/' + z.prancha)
    if (z.chao_textura && !this.textures.exists(z.chao_textura)) this.load.image(z.chao_textura, 'img/' + z.chao_textura + '.png')
    if (z.agua_textura && !this.textures.exists(z.agua_textura)) this.load.image(z.agua_textura, 'img/' + z.agua_textura + '.png')
    const objs = new Set<string>()
    for (const p of z.paradas) for (const o of p.objetos) objs.add(o.asset)
    if (z.missao) {
      objs.add(z.missao.asset)
      if (z.missao.tipo === 'colher') { if (z.missao.cesta) objs.add('cesta'); if (z.missao.recompensa_item) objs.add(z.missao.recompensa_item.asset) } else objs.add(z.missao.caixa)
    }
    const memPre = this.mem(); if (memPre.mochila) objs.add(memPre.mochila.asset)
    for (const p of z.paradas) for (const pr of p.personagens) { if (pr.quer_item) objs.add(pr.quer_item); if (pr.ao_receber?.muda_objeto) objs.add(pr.ao_receber.muda_objeto.asset) }
    for (const a of objs) if (!this.textures.exists(a)) this.load.image(a, 'img/' + a + '.png')
    // personagens
    Personagem.preload(this, this.av.heroi)
    const nomes = new Set<string>()
    for (const p of z.paradas) for (const pr of p.personagens) nomes.add(pr.nome)
    if (z.missao?.npc) nomes.add(z.missao.npc)
    for (const n of nomes) Personagem.preload(this, n)
    // falas + contagem + música (tolerante a ausência)
    for (const f of z.falas) { this.falas[f.id] = f; if (!QA) this.load.audio(f.id, 'audio/' + f.id + '.mp3') }
    if (z.missao && !QA) for (let i = 1; i <= z.missao.itens.length; i++) this.load.audio(z.missao.voz_prefixo + i, 'audio/' + z.missao.voz_prefixo + i + '.mp3')
    if (z.musica && !QA) this.load.audio('musica_' + z.id, 'audio/' + z.musica + '.mp3')
    this.load.on('loaderror', (f: any) => console.warn('asset ausente:', f.key))
    this.efeitosBase()
  }

  create () {
    const z = this.zona
    for (const id of Object.keys(this.falas)) this.audioOk[id] = this.cache.audio.exists(id)

    // CHÃO — estilo FLORESTA (textura contínua; a criança anda entre as peças)
    // ou estilo PRANCHA (pintura única; ideal p/ interiores como a cabana)
    if (z.chao_textura && this.textures.exists(z.chao_textura)) {
      this.add.tileSprite(0, 0, z.largura, z.altura, z.chao_textura).setOrigin(0, 0).setDepth(0).setTileScale(0.5)
    } else if (z.prancha && this.textures.exists('prancha_' + z.id)) {
      this.add.image(0, 0, 'prancha_' + z.id).setOrigin(0, 0).setDisplaySize(z.largura, z.altura).setDepth(0)
    } else { this.add.rectangle(z.largura / 2, z.altura / 2, z.largura, z.altura, 0x3f6f4a).setDepth(0) }
    // ÁGUA (rio/lago): faixas de textura com brilho suave
    if (z.agua_textura && this.textures.exists(z.agua_textura)) {
      for (const a of z.agua) {
        const w = this.add.tileSprite(a.x, a.y, a.w, a.h, z.agua_textura).setOrigin(0, 0).setDepth(2).setTileScale(0.5)
        this.tweens.add({ targets: w, tilePositionY: 40, duration: 4000, repeat: -1 })
      }
    }

    // faixa ANDÁVEL: da linha do horizonte pra baixo (não anda no céu/copa)
    this.physics.world.setBounds(56, z.chao_min_y, z.largura - 112, z.altura - z.chao_min_y - 44)
    this.obst = this.physics.add.staticGroup()
    // BLOQUEIOS invisíveis (rio, barranco) — os consertados na memória NÃO voltam
    const cons = (this.mem().consertos || {})[z.id] || {}
    for (const bq of z.bloqueios) {
      if (cons.bloqueios && cons.bloqueios.indexOf(bq.id) >= 0) continue
      const r = this.add.rectangle(bq.x + bq.w / 2, bq.y + bq.h / 2, bq.w, bq.h).setVisible(false)
      this.physics.add.existing(r, true)
      ;(r.body as Phaser.Physics.Arcade.StaticBody).updateFromGameObject()
      this.obst.add(r); this.bloqPorId[bq.id] = r
    }
    this.mochila = this.mem().mochila || null

    for (const p of z.paradas) {
      for (const o of p.objetos) this.colocaObjeto(o)
      for (const pr of p.personagens) {
        const np = new Personagem(this, pr.nome, pr.x, pr.y, pr.alt)
        ;(np as any)._falaChegar = pr.fala_ao_chegar
        ;(np as any)._parada = p.id
        ;(np as any)._ref = pr
        this.npcs.push(np); this.npcPorNome[pr.nome] = np
      }
      if (p.marcador) {
        const m = this.add.image(p.x, p.y - 40, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(9000)
        this.tweens.add({ targets: m, alpha: { from: 0.25, to: 0.7 }, scale: { from: 0.7, to: 1.3 }, duration: 1200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      }
    }

    // PORTAIS (a passagem pulsa chamando a criança; rótulo curtinho)
    for (const pt of z.portais) {
      const m = this.add.image(pt.x, pt.y, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(8990)
      this.tweens.add({ targets: m, alpha: { from: 0.3, to: 0.8 }, scale: { from: 0.9, to: 1.5 }, duration: 1000, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      if (pt.rotulo) {
        this.add.text(pt.x, pt.y - 54, pt.rotulo, { fontFamily: 'Arial Black, Arial', fontSize: '17px', color: '#ffffff', stroke: '#1c2b46', strokeThickness: 5 }).setOrigin(0.5).setDepth(9001)
      }
    }

    // MISSÃO "colher" — dentro do mundo (ou o estado 'já feita': o mundo lembra)
    if (z.missao) this.armaMissao()

    // HERÓI — corpo físico dedicado; o sprite segue (colisão certinha)
    this.heroi = new Personagem(this, this.av.heroi, this.spawnPt.x, this.spawnPt.y, 96)
    this.corpo = this.add.rectangle(this.spawnPt.x, this.spawnPt.y, 40, 26).setVisible(false)
    this.physics.add.existing(this.corpo)
    const b = this.corpo.body as Phaser.Physics.Arcade.Body
    b.setCollideWorldBounds(true)
    this.physics.add.collider(this.corpo, this.obst)
    this.ultX = this.spawnPt.x; this.ultY = this.spawnPt.y
    this.poeira = this.add.particles(0, 0, 'puff', { lifespan: 420, speed: { min: 4, max: 16 }, angle: { min: 200, max: 340 }, scale: { start: 0.5, end: 1.3 }, alpha: { start: 0.5, end: 0 }, emitting: false }).setDepth(640)

    // ---- VIDA AMBIENTE (orçamento: no máx. 2 emissores + 2 brilhos) ----
    if (z.efeitos.polen) {
      this.add.particles(0, 0, 'vaga', { x: { min: 60, max: z.largura - 60 }, y: { min: 60, max: z.altura - 60 }, lifespan: 2600, frequency: 240, quantity: 1, blendMode: 'ADD', alpha: { start: 0.8, end: 0 }, scale: { start: 0.5, end: 1.1 }, speedX: { min: -12, max: 12 }, speedY: { min: -16, max: 6 }, emitting: true }).setDepth(8500)
    }
    if (z.efeitos.sol) {
      const s = this.add.image(z.efeitos.sol.x, z.efeitos.sol.y, 'glow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0.25).setScale(2.6).setDepth(8400)
      this.tweens.add({ targets: s, alpha: 0.4, scale: 3.1, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    }
    if (z.efeitos.lareira) {
      const l = this.add.image(z.efeitos.lareira.x, z.efeitos.lareira.y, 'glow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0.5).setScale(1.4).setDepth(8400)
      this.tweens.add({ targets: l, alpha: { from: 0.42, to: 0.75 }, scale: { from: 1.3, to: 1.55 }, duration: 220, yoyo: true, repeat: -1 })
    }
    // brilho compartilhado da contagem (UM só — nunca por item)
    this.brilho = this.add.image(-999, -999, 'glow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0).setDepth(9100)
    // número grandão da contagem (a criança VÊ o número enquanto OUVE)
    this.numerao = this.add.text(VW / 2, 190, '', { fontFamily: 'Arial Black, Arial', fontSize: '104px', color: '#ffdc3a', stroke: '#5a3a10', strokeThickness: 12 }).setOrigin(0.5).setScrollFactor(0).setDepth(99500).setAlpha(0)

    // música da zona (suave, em loop) + câmera
    if (z.musica && this.cache.audio.exists('musica_' + z.id)) {
      this.musicaSom = this.sound.add('musica_' + z.id, { loop: true, volume: 0.20 })
      this.musicaSom.play()
      this.events.once('shutdown', () => { try { this.musicaSom?.stop(); this.sound.removeByKey('musica_' + z.id) } catch (e) {} })
    }
    this.cameras.main.setBounds(0, 0, z.largura, z.altura)
    this.cameras.main.startFollow(this.heroi.sprite, true, 0.1, 0.1)
    this.cameras.main.fadeIn(320, 6, 12, 24)

    this.criarBalao()
    this.cursors = this.input.keyboard!.createCursorKeys()
    this.teclas = this.input.keyboard!.addKeys('W,A,S,D,E,SPACE')
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { if (this.estado === 'explora') { this.alvo = { x: p.worldX, y: p.worldY }; this.travadoT = 0 } })
    el('telaIntro')?.classList.add('hidden'); el('btnOuvir')?.classList.add('hidden')
    el('hud')?.classList.add('hidden')

    // AUDITOR (robô-fiscal) — só aparece com ?qa (a criança nunca vê a faixa)
    const assets = new Set<string>(this.textures.getTextureKeys())
    const audios = new Set<string>(Object.keys(this.audioOk).filter(k => this.audioOk[k]))
    const probs = auditar(this.av, { assets, audios, zonaAtual: this.zona.id })
    if (probs.length) {
      console.warn('AUDITOR', probs)
      if (QA) {
        const grave = probs.some(x => x.grave)
        const d = document.createElement('div')
        d.id = 'auditoria'
        d.style.cssText = 'position:fixed;left:0;bottom:0;right:0;z-index:99998;max-height:45%;overflow:auto;background:' + (grave ? '#8a1c1c' : '#8a6a1c') + ';color:#fff;font:600 13px system-ui;padding:8px 12px;'
        d.textContent = 'AUDITOR (' + probs.length + '): ' + probs.map(x => (x.grave ? '[GRAVE] ' : '[aviso] ') + x.msg).join('   |   ')
        document.body.appendChild(d)
      }
    }

    this.desenhaMochila()

    // chegada: falas da 1ª visita (o mundo dá boas-vindas UMA vez) + festa
    const m = this.mem(); m.visitadas = m.visitadas || {}
    if (!m.visitadas[z.id] && z.chegada.length) {
      m.visitadas[z.id] = true; this.memSalva(m)
      this.time.delayedCall(500, () => this.dialogo(z.chegada, () => { if (z.festa_na_chegada) { this.confete(); this.heroi.feliz(3) } }))
    } else if (!m.visitadas[z.id]) { m.visitadas[z.id] = true; this.memSalva(m) }

    // ganchos de QA (o robô dirige o mundo de verdade)
    ;(window as any).__mundo = this
    ;(window as any).__irZona = (id: string) => this.transitar({ x: 0, y: 0, raio: 0, para: id, spawn: this.av.inicio, rotulo: '' })
    ;(window as any).__colher1 = () => { const i = this.itens.find(it => it.visible && !(it as any)._colhida); if (i) this.colher(i) }
    ;(window as any).__tp = (x: number, y: number) => { this.corpo.setPosition(x, y); (this.corpo.body as Phaser.Physics.Arcade.Body).reset(x, y) }
    // QA da missão agrupar: o robô LÊ o estado e TOCA numa cesta como a criança tocaria
    ;(window as any).__agrupar = () => ({
      soltas: this.soltasAg.length, pilha: this.pilhaN, mao: this.carregando?.tipo ?? null,
      cestas: this.vagasC.map(v => ({ tem: !!v.img, n: v.count })), feita: this.missaoFeita(), estado: this.estado
    })
    ;(window as any).__tocaCesta = (i: number) => { const v = this.vagasC[i]; if (v?.img && !this.missaoFeita()) this.tiraDe = v }
    if (new URLSearchParams(location.search).has('mec')) {
      const alvoP = z.paradas.find(p => p.mecanica && temMecanica(p.mecanica.id))
      if (alvoP) this.time.delayedCall(400, () => this.abreMecanica(alvoP.id))
    }
  }

  // ---------- missão "colher" / "agrupar" ----------
  armaMissao () {
    const m0 = this.zona.missao!
    if (m0.tipo === 'agrupar') { this.armaAgrupar(); return }
    const mi = m0 as TMissaoColher
    if (this.missaoFeita()) {
      if (mi.cesta) this.cestaCheia(mi as { cesta: { x: number, y: number }, asset: string })
      const np = mi.npc ? this.npcPorNome[mi.npc] : null
      if (np) { np.feliz(2.5); (np as any)._falaChegar = mi.fala_revisita }
      return
    }
    if (mi.cesta) this.add.image(mi.cesta.x, mi.cesta.y, 'cesta').setOrigin(0.5, 1).setScale(120 / this.textures.get('cesta').getSourceImage().height).setDepth(mi.cesta.y)
    for (const it of mi.itens) {
      const im = this.add.image(it.x, it.y, mi.asset).setOrigin(0.5, 1)
      im.setScale(mi.alt / im.height).setDepth(it.y)
      ;(im as any)._tw = this.tweens.add({ targets: im, y: it.y - 5, duration: 700 + Math.random() * 200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      this.itens.push(im)
    }
  }

  // ---------- missão "agrupar" (a LEI dos grupos iguais; sem gabarito) ----------
  armaAgrupar () {
    const mi = this.zona.missao as TMissaoAgrupar
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (this.missaoFeita()) { if (np) { np.feliz(2.5); (np as any)._falaChegar = mi.fala_revisita } return }
    // vagas: marcas discretas no chão (onde uma cesta PODE ser pousada)
    for (const v of mi.vagas) {
      const marca = this.add.image(v.x, v.y - 10, 'glowFrio').setAlpha(0.3).setScale(0.8).setDepth(3)
      this.vagasC.push({ x: v.x, y: v.y, img: null, count: 0, frutas: [], marca })
    }
    // pilha de cestas (passar por cima de mãos vazias = pegar uma)
    this.pilhaN = mi.vagas.length
    const hCaixa = this.textures.get(mi.caixa).getSourceImage().height
    for (let i = 0; i < Math.min(3, this.pilhaN); i++) {
      this.pilhaImgs.push(this.add.image(mi.pilha.x, mi.pilha.y - i * 24, mi.caixa).setOrigin(0.5, 1).setScale(mi.caixa_alt / hCaixa).setDepth(mi.pilha.y + i))
    }
    const g = this.add.image(mi.pilha.x, mi.pilha.y - 70, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(9000)
    this.tweens.add({ targets: g, alpha: { from: 0.25, to: 0.7 }, scale: { from: 0.7, to: 1.2 }, duration: 1200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    // a fartura espalhada (o que precisa ser arrumado)
    for (const it of mi.itens) {
      const im = this.add.image(it.x, it.y, mi.asset).setOrigin(0.5, 1)
      im.setScale(mi.alt / im.height).setDepth(it.y)
      ;(im as any)._tw = this.tweens.add({ targets: im, y: it.y - 5, duration: 700 + Math.random() * 200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      this.soltasAg.push(im)
    }
  }

  // a criança AGE no mundo (andar = pegar/pousar/repartir); tocar numa cesta = mexer nela
  agirAgrupar (t: number) {
    const mi = this.zona.missao as TMissaoAgrupar
    const hx = this.heroi.x, hy = this.heroi.y
    const perto = (x: number, y: number, r: number) => Math.abs(hx - x) < r && Math.abs(hy - y) < r + 10
    const hFruta = this.textures.get(mi.asset).getSourceImage().height
    const naMao = (im: Phaser.GameObjects.Image) => {
      im.setDepth(99190)
      this.tweens.add({ targets: im, x: hx, y: hy - 116, scale: (mi.alt * 0.8) / hFruta, duration: 240, ease: 'Cubic.easeOut' })
    }
    // cada cesta age 1x POR VISITA (sair do raio = libera; senão tira-deposita em ciclo)
    for (const v of this.vagasC) if (!perto(v.x, v.y, 58)) v.livre = true
    // 0) a criança TOCOU numa cesta pousada (quer mexer nela) e chegou lá
    if (this.tiraDe && this.tiraDe.img && perto(this.tiraDe.x, this.tiraDe.y, 62) && !this.carregando && t > this.pegaCd) {
      const v = this.tiraDe; this.tiraDe = null; v.livre = false
      if (v.count > 0) {                       // tira UMA de volta (reequilibrar sem punição)
        const im = v.frutas.pop()!; v.count--
        naMao(im); this.carregando = { tipo: 'maca', img: im }
      } else {                                 // cesta vazia: pega a cesta de volta
        v.img!.destroy(); v.img = null; v.marca?.setAlpha(0.3)
        const img = this.add.image(hx, hy - 120, mi.caixa).setOrigin(0.5, 1)
        img.setScale((mi.caixa_alt * 0.62) / img.height).setDepth(99190)
        this.carregando = { tipo: 'cesta', img }
      }
      this.pegaCd = t + 500
      return
    }
    // 1) pegar CESTA na pilha (mãos vazias) — ou DEVOLVER a cesta que carrega.
    //    A pilha age 1x POR VISITA (senão pega-devolve em ciclo parado em cima dela).
    const noPilha = perto(mi.pilha.x, mi.pilha.y - 16, 56)
    if (!noPilha) this.pilhaLivre = true
    if (noPilha && this.pilhaLivre && t > this.pegaCd) {
      const hCaixa = this.textures.get(mi.caixa).getSourceImage().height
      if (!this.carregando && this.pilhaN > 0) {
        this.pilhaLivre = false
        this.pilhaN--
        if (this.pilhaImgs.length > Math.min(3, this.pilhaN)) this.pilhaImgs.pop()?.destroy()
        const img = this.add.image(hx, hy - 120, mi.caixa).setOrigin(0.5, 1)
        img.setScale((mi.caixa_alt * 0.62) / img.height).setDepth(99190)
        this.carregando = { tipo: 'cesta', img }
        this.pegaCd = t + 500
        return
      }
      if (this.carregando?.tipo === 'cesta') {   // devolve à pilha (mudou de ideia)
        this.pilhaLivre = false
        this.carregando.img.destroy(); this.carregando = null
        this.pilhaN++
        if (this.pilhaImgs.length < Math.min(3, this.pilhaN)) this.pilhaImgs.push(this.add.image(mi.pilha.x, mi.pilha.y - this.pilhaImgs.length * 24, mi.caixa).setOrigin(0.5, 1).setScale(mi.caixa_alt / hCaixa).setDepth(mi.pilha.y + this.pilhaImgs.length))
        this.pegaCd = t + 500
        return
      }
    }
    // 2) pousar a cesta numa VAGA livre
    if (this.carregando?.tipo === 'cesta' && t > this.pegaCd) {
      for (const v of this.vagasC) {
        if (v.img || !perto(v.x, v.y, 58)) continue
        this.carregando.img.destroy(); this.carregando = null
        v.img = this.add.image(v.x, v.y, mi.caixa).setOrigin(0.5, 1).setScale(mi.caixa_alt / this.textures.get(mi.caixa).getSourceImage().height).setDepth(v.y)
        v.img.setInteractive({ useHandCursor: true })
        v.img.on('pointerdown', () => { if (!this.missaoFeita()) this.tiraDe = v })
        v.marca?.setAlpha(0.1)
        this.pegaCd = t + 550
        return
      }
    }
    // 3) pegar um item solto (mãos vazias)
    if (!this.carregando && t > this.pegaCd) {
      for (let i = 0; i < this.soltasAg.length; i++) {
        const im = this.soltasAg[i]
        if (!perto(im.x, im.y - 14, 48)) continue
        this.soltasAg.splice(i, 1)
        const tw = (im as any)._tw as Phaser.Tweens.Tween | undefined; if (tw) tw.remove()
        naMao(im)
        this.carregando = { tipo: 'maca', img: im }
        this.pegaCd = t + 440
        return
      }
    }
    // 4) com item na mão, chegar numa cesta = DEPOSITA (a contagem DO GRUPO, falada)
    if (this.carregando?.tipo === 'maca' && t > this.pegaCd) {
      for (const v of this.vagasC) {
        if (!v.img || v.livre === false || !perto(v.x, v.y, 58)) continue
        v.livre = false
        const im = this.carregando.img; this.carregando = null
        v.count++
        const n = v.count
        const mx = v.x + (n % 3 - 1) * 22, my = v.y - 40 - Math.floor((n - 1) / 3) * 15
        this.tweens.add({ targets: im, x: mx, y: my, scale: 30 / hFruta, duration: 300, ease: 'Cubic.easeInOut', onComplete: () => im.setDepth(v.y + 1 + n) })
        v.frutas.push(im)
        // a contagem ACESA: ela VÊ e OUVE o tamanho DESTE grupo crescer
        this.brilho.setPosition(v.x, v.y - 44).setAlpha(0.85).setScale(0.8)
        this.tweens.add({ targets: this.brilho, alpha: 0, scale: 1.5, duration: 520, ease: 'Cubic.easeOut' })
        if (!QA && this.cache.audio.exists(mi.voz_prefixo + n)) { try { this.sound.play(mi.voz_prefixo + n) } catch (e) {} }
        this.numerao.setText(String(n)).setAlpha(1).setScale(0.4)
        this.tweens.add({ targets: this.numerao, scale: 1, duration: 160, ease: 'Back.easeOut' })
        this.tweens.add({ targets: this.numerao, alpha: 0, delay: 520, duration: 320 })
        this.pegaCd = t + 480
        return
      }
    }
    // 5) chegar ao personagem do TESTE = o mundo julga a arrumação DELA
    //    (só depois de ela COMEÇAR a arrumar — o Castor não cobra antes da ação)
    const mexeu = this.vagasC.some(v => v.img !== null) || !!this.carregando || this.soltasAg.length < mi.itens.length
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (np && mexeu && t > this.testeCd && this.falado[(np as any)._parada] && Phaser.Math.Distance.Between(hx, hy, np.x, np.y) < 150) {
      this.testeCd = t + 3200
      this.testarAgrupar(np)
    }
  }

  // A LEI (o juiz é o MUNDO, não um gabarito): todo grupo com o MESMO tanto?
  testarAgrupar (np: Personagem) {
    const mi = this.zona.missao as TMissaoAgrupar
    const usadas = this.vagasC.filter(v => v.img && v.count > 0)
    // sobrou item solto (ou na mão): o mundo aponta, sem punir
    if (this.soltasAg.length > 0 || this.carregando) { this.dialogo(mi.ao_sobrar); return }
    // tudo num grupo só: consequência (pesado demais) + pergunta
    if (usadas.length < 2) {
      if (usadas[0]) this.tomba(usadas[0], 0.6)
      this.registraKc(mi.kc, false)
      this.dialogo(mi.ao_uma_caixa)
      return
    }
    const counts = usadas.map(v => v.count)
    const iguais = counts.every(c => c === counts[0])
    if (!iguais) {
      // a(s) cesta(s) DIFERENTE(s) tombam — a consequência mostra ONDE, o mentor pergunta
      const freq: { [n: number]: number } = {}
      for (const c of counts) freq[c] = (freq[c] || 0) + 1
      let moda = counts[0], best = 0
      for (const k of Object.keys(freq)) if (freq[+k] > best) { best = freq[+k]; moda = +k }
      for (const v of usadas) if (v.count !== moda) this.tomba(v, 1)
      this.registraKc(mi.kc, false)
      this.dialogo(mi.ao_desigual)
      return
    }
    // VENCEU — com a arrumação DELA (n grupos de k; 2×6, 3×4... todas valem)
    const n = usadas.length, k = counts[0]
    this.registraKc(mi.kc, true)
    const m = this.mem(); m.missoes = m.missoes || {}; m.missoes[this.zona.id] = true; this.memSalva(m)
    np.feliz(60); (np as any)._falaChegar = mi.fala_revisita
    this.heroi.feliz(3)
    this.confete()
    const cid = mi.conceito_prefixo + n + 'x' + k          // o NOME nasce da arrumação dela
    const seq = [...mi.ao_completar, ...(this.falas[cid] ? [cid] : [])]
    this.dialogo(seq, () => {
      // o MUNDO MUDA na frente dela: a pedra sai e o caminho abre
      if (mi.some_objeto) {
        const o = this.objPorId[mi.some_objeto]
        if (o) {
          this.brilho.setPosition(o.img.x, o.img.y - o.alt / 2).setAlpha(0.95).setScale(1.5)
          this.tweens.add({ targets: this.brilho, alpha: 0, scale: 2.3, duration: 700, ease: 'Cubic.easeOut' })
          this.tweens.add({ targets: o.img, x: o.img.x + 90, angle: 40, alpha: 0, scale: o.img.scale * 0.5, duration: 800, ease: 'Cubic.easeIn', onComplete: () => o.img.destroy() })
        }
        const m2 = this.mem(); m2.consertos = m2.consertos || {}
        const cz = m2.consertos[this.zona.id] = m2.consertos[this.zona.id] || {}
        cz.some = cz.some || []; if (cz.some.indexOf(mi.some_objeto) < 0) cz.some.push(mi.some_objeto)
        this.memSalva(m2)
      }
      if (mi.remove_bloqueio) {
        const r = this.bloqPorId[mi.remove_bloqueio]
        if (r) { this.obst.remove(r); r.destroy() }
        const m3 = this.mem(); m3.consertos = m3.consertos || {}
        const cz = m3.consertos[this.zona.id] = m3.consertos[this.zona.id] || {}
        cz.bloqueios = cz.bloqueios || []; if (cz.bloqueios.indexOf(mi.remove_bloqueio) < 0) cz.bloqueios.push(mi.remove_bloqueio)
        this.memSalva(m3)
      }
      this.heroi.feliz(2.5)
    })
  }

  // consequência física: a cesta (e as frutas dela) tombam de leve — sem X vermelho
  tomba (v: VagaCaixa, forca: number) {
    if (!v.img) return
    const alvos = [v.img, ...v.frutas]
    this.tweens.add({ targets: alvos, angle: { from: -4 * forca, to: 14 * forca }, duration: 130, yoyo: true, repeat: 3, ease: 'Sine.easeInOut' })
    this.brilho.setPosition(v.x, v.y - 40).setAlpha(0.7).setScale(1.1)
    this.tweens.add({ targets: this.brilho, alpha: 0, scale: 1.8, duration: 600 })
  }

  // mede sem provar: cada teste vira observação no domínio (BKT local)
  registraKc (kc: string, ok: boolean) {
    try { salva('local', registra(carrega('local'), kc, ok, Date.now())) } catch (e) { /* sem storage: segue */ }
  }
  cestaCheia (mi: { cesta: { x: number, y: number }, asset: string }) {
    this.add.image(mi.cesta.x, mi.cesta.y, 'cesta').setOrigin(0.5, 1).setScale(120 / this.textures.get('cesta').getSourceImage().height).setDepth(mi.cesta.y)
    for (let i = 0; i < 5; i++) {
      const mx = mi.cesta.x + (i % 3 - 1) * 26, my = mi.cesta.y - 52 - Math.floor(i / 3) * 18
      this.add.image(mx, my, mi.asset).setOrigin(0.5, 1).setScale(34 / this.textures.get(mi.asset).getSourceImage().height).setDepth(mi.cesta.y + 1)
    }
  }
  colher (im: Phaser.GameObjects.Image) {
    const mi = this.zona.missao as TMissaoColher
    if ((im as any)._colhida) return
    ;(im as any)._colhida = true
    this.colhidas++
    const n = this.colhidas
    // a CONTAGEM ACESA: o item brilha NO MOMENTO em que o número é falado
    this.brilho.setPosition(im.x, im.y - mi.alt / 2).setAlpha(0.9).setScale(0.9)
    this.tweens.add({ targets: this.brilho, alpha: 0, scale: 1.6, duration: 600, ease: 'Cubic.easeOut' })
    if (!QA && this.cache.audio.exists(mi.voz_prefixo + n)) { try { this.sound.play(mi.voz_prefixo + n) } catch (e) {} }
    this.numerao.setText(String(n)).setAlpha(1).setScale(0.4)
    this.tweens.add({ targets: this.numerao, scale: 1.1, duration: 180, ease: 'Back.easeOut' })
    this.tweens.add({ targets: this.numerao, alpha: 0, delay: 560, duration: 380 })
    // o item VOA pra cesta (o mundo reage) — ou some com brilho (vai pra mochila)
    const tw = (im as any)._tw as Phaser.Tweens.Tween | undefined; if (tw) tw.remove()
    if (mi.cesta) {
      const ces = mi.cesta
      const mx = ces.x + (n % 3 - 1) * 26, my = ces.y - 52 - Math.floor((n - 1) / 3) * 18
      this.tweens.add({
        targets: im, x: mx, y: my, scale: 34 / this.textures.get(mi.asset).getSourceImage().height, duration: 520, ease: 'Cubic.easeInOut',
        onComplete: () => { im.setDepth(ces.y + 1) }
      })
    } else {
      this.tweens.add({ targets: im, y: im.y - 60, alpha: 0, scale: 0.2, duration: 480, ease: 'Cubic.easeIn', onComplete: () => im.destroy() })
    }
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (np) np.feliz(0.9)
    if (this.colhidas >= mi.itens.length) this.time.delayedCall(750, () => this.missaoCompleta())
  }
  missaoCompleta () {
    const mi = this.zona.missao as TMissaoColher
    const m = this.mem(); m.missoes = m.missoes || {}; m.missoes[this.zona.id] = true; this.memSalva(m)
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (np) { np.feliz(60); (np as any)._falaChegar = mi.fala_revisita }
    this.heroi.feliz(3)
    this.confete()
    const depois = () => { if (mi.recompensa_item) this.pegaItem(mi.recompensa_item) }
    if (mi.ao_completar.length) this.dialogo(mi.ao_completar, depois); else depois()
  }
  // ---------- MOCHILA (o item conquistado viaja com a criança) ----------
  pegaItem (item: { asset: string, nome: string }) {
    this.mochila = item
    const m = this.mem(); m.mochila = item; this.memSalva(m)
    this.desenhaMochila(true)
  }
  desenhaMochila (pulo = false) {
    if (this.hudItem) { this.hudItem.destroy(); this.hudItem = null }
    if (this.hudItemTxt) { this.hudItemTxt.destroy(); this.hudItemTxt = null }
    if (!this.mochila || !this.textures.exists(this.mochila.asset)) return
    this.hudItem = this.add.image(74, VH - 74, this.mochila.asset).setScrollFactor(0).setDepth(99300)
    this.hudItem.setScale(84 / this.hudItem.height)
    this.hudItemTxt = this.add.text(74, VH - 22, this.mochila.nome, { fontFamily: 'Arial Black, Arial', fontSize: '15px', color: '#ffffff', stroke: '#1c2b46', strokeThickness: 5 }).setOrigin(0.5).setScrollFactor(0).setDepth(99300)
    if (pulo) { this.hudItem.setScale(this.hudItem.scale * 0.2); this.tweens.add({ targets: this.hudItem, scale: 84 / this.textures.get(this.mochila.asset).getSourceImage().height, duration: 420, ease: 'Back.easeOut' }) }
  }
  // ENTREGA: a criança chega ao personagem COM o item -> ele age e o MUNDO MUDA
  entregar (np: Personagem, pr: { quer_item?: string, ao_receber?: { falas: string[], muda_objeto?: { id: string, asset: string }, remove_bloqueio?: string } }) {
    if (!pr.ao_receber) return
    this.entregou[np.nome] = true
    this.mochila = null
    const m = this.mem(); m.mochila = null
    m.consertos = m.consertos || {}; const cz = m.consertos[this.zona.id] = m.consertos[this.zona.id] || {}
    if (pr.ao_receber.muda_objeto) { cz.objetos = cz.objetos || {}; cz.objetos[pr.ao_receber.muda_objeto.id] = pr.ao_receber.muda_objeto.asset }
    if (pr.ao_receber.remove_bloqueio) { cz.bloqueios = cz.bloqueios || []; if (cz.bloqueios.indexOf(pr.ao_receber.remove_bloqueio) < 0) cz.bloqueios.push(pr.ao_receber.remove_bloqueio) }
    this.memSalva(m)
    this.desenhaMochila()
    np.feliz(3)
    this.dialogo(pr.ao_receber.falas, () => {
      // o MUNDO MUDA na frente da criança (a consequência visível)
      if (pr.ao_receber!.muda_objeto) {
        const alvoObj = this.objPorId[pr.ao_receber!.muda_objeto.id]
        if (alvoObj) {
          this.brilho.setPosition(alvoObj.img.x, alvoObj.img.y - alvoObj.alt / 2).setAlpha(0.95).setScale(1.4)
          this.tweens.add({ targets: this.brilho, alpha: 0, scale: 2.2, duration: 700, ease: 'Cubic.easeOut' })
          alvoObj.img.setTexture(pr.ao_receber!.muda_objeto.asset)
          alvoObj.img.setScale(alvoObj.alt / alvoObj.img.height)
        }
      }
      if (pr.ao_receber!.remove_bloqueio) {
        const r = this.bloqPorId[pr.ao_receber!.remove_bloqueio]
        if (r) { this.obst.remove(r); r.destroy() }
      }
      this.heroi.feliz(2.5)
    })
  }

  confete () {
    // efeito leve (formas por código são permitidas como EFEITO pela style-bible)
    const cores = [0xffd45a, 0xff5a5a, 0x5ad1ff, 0x8aff7a, 0xff8ad1]
    for (let i = 0; i < 40; i++) {
      const r = this.add.rectangle(Math.random() * VW, -20, 10, 14, cores[i % 5]).setScrollFactor(0).setDepth(99400)
      this.tweens.add({ targets: r, y: VH + 30, angle: Math.random() * 720 - 360, x: '+=' + (Math.random() * 140 - 70), duration: 2000 + Math.random() * 1400, delay: Math.random() * 400, onComplete: () => r.destroy() })
    }
  }

  // ---------- portais ----------
  transitar (pt: TPortal) {
    if (this.estado === 'transita') return
    this.estado = 'transita'
    try { this.musicaSom?.stop() } catch (e) {}
    this.cameras.main.fadeOut(300, 6, 12, 24)
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.restart({ aventura: this.av, zonaId: pt.para, spawn: pt.spawn })
    })
  }

  colocaObjeto (o: TObjeto) {
    const cons = (this.mem().consertos || {})[this.zona.id] || {}
    if (o.id && cons.some && cons.some.indexOf(o.id) >= 0) return   // objeto que SAIU não volta (a pedra)
    const asset = (o.id && cons.objetos && cons.objetos[o.id]) ? cons.objetos[o.id] : o.asset
    if (!this.textures.exists(asset)) return
    const im = this.add.image(o.x, o.y, asset).setOrigin(0.5, 1)
    im.setScale(o.alt / im.height).setFlipX(o.flip).setDepth(o.profundidade ?? o.y)
    if (o.id) this.objPorId[o.id] = { img: im, alt: o.alt }
    if (o.vida === 'balanca') this.tweens.add({ targets: im, angle: { from: -1.6, to: 1.6 }, duration: 2800 + Math.random() * 800, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    else if (o.vida === 'flutua_suave') this.tweens.add({ targets: im, y: o.y - 6, duration: 1500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    else if (o.vida === 'brilha') { const g = this.add.image(o.x, o.y - o.alt * 0.4, 'glow').setBlendMode(Phaser.BlendModes.ADD).setDepth(im.depth + 1); this.tweens.add({ targets: g, alpha: { from: 0.4, to: 0.9 }, scale: { from: 0.85, to: 1.15 }, duration: 900, yoyo: true, repeat: -1 }) }
    else if (o.vida === 'tremula') { const g = this.add.image(o.x, o.y - o.alt * 0.7, 'glow').setBlendMode(Phaser.BlendModes.ADD).setDepth(im.depth + 1); this.tweens.add({ targets: g, alpha: { from: 0.55, to: 1 }, scale: { from: 0.85, to: 1.12 }, duration: 240, yoyo: true, repeat: -1 }) }
    if (o.colide) {
      const w = Math.max(26, o.alt * 0.32), h = 22
      const bl = this.add.rectangle(o.x, o.y - h / 2, w, h).setVisible(false)
      this.physics.add.existing(bl, true)
      ;(bl.body as Phaser.Physics.Arcade.StaticBody).updateFromGameObject()
      this.obst.add(bl)
    }
  }

  // ---- primitivas de efeito (brilhos/partículas — permitidas como efeito) ----
  efeitosBase () {
    if (!this.textures.exists('glow')) { this.circ('glow', 90, 'rgba(255,190,90,', 0.5); this.circ('glowFrio', 60, 'rgba(170,225,255,', 0.4); this.circ('vaga', 8, 'rgba(255,240,170,', 0.95); this.circ('puff', 14, 'rgba(225,210,180,', 0.6) }
    if (!this.textures.exists('sombra')) {
      const so = this.textures.createCanvas('sombra', 70, 26)!; const gs = so.getContext()
      const gr = gs.createRadialGradient(35, 13, 2, 35, 13, 33); gr.addColorStop(0, 'rgba(6,10,18,.5)'); gr.addColorStop(1, 'rgba(6,10,18,0)')
      gs.fillStyle = gr; gs.beginPath(); gs.ellipse(35, 13, 33, 12, 0, 0, 7); gs.fill(); so.refresh()
    }
  }
  circ (n: string, raio: number, c: string, a: number) {
    if (this.textures.exists(n)) return
    const d = raio * 2, t = this.textures.createCanvas(n, d, d)!, g = t.getContext()
    const grd = g.createRadialGradient(raio, raio, 1, raio, raio, raio); grd.addColorStop(0, c + a + ')'); grd.addColorStop(1, c + '0)')
    g.fillStyle = grd; g.fillRect(0, 0, d, d); t.refresh()
  }

  criarBalao () {
    const bg = this.add.graphics(); bg.fillStyle(0xffffff, 0.97); bg.lineStyle(3, 0x22314f, 1)
    bg.fillRoundedRect(0, 0, 430, 116, 16); bg.strokeRoundedRect(0, 0, 430, 116, 16); bg.fillStyle(0x22314f, 1); bg.fillTriangle(200, 116, 230, 116, 215, 136)
    this.balaoNome = this.add.text(16, -12, '', { fontFamily: 'Arial Black, Arial', fontSize: '15px', color: '#fff' }).setPadding(8, 3, 8, 3)
    this.balaoTxt = this.add.text(16, 14, '', { fontFamily: 'Arial', fontSize: '17px', color: '#22314f', wordWrap: { width: 398 }, lineSpacing: 4 })
    this.balao = this.add.container(0, 0, [bg, this.balaoNome, this.balaoTxt]).setDepth(9900).setVisible(false).setScrollFactor(0)
    this.ajustaBalao()
    this.scale.on('resize', () => this.ajustaBalao())
  }
  // celular segura o app em pé: o ENVELOP corta as laterais — o balão ENCOLHE
  // pra caber inteiro na área visível (lição da auditoria)
  ajustaBalao () {
    const pw = this.scale.parentSize.width || VW, ph = this.scale.parentSize.height || VH
    const f = Math.max(pw / VW, ph / VH) || 1
    const visW = pw / f
    const s = Math.min(1, (visW - 20) / 450)
    this.balao.setScale(s).setPosition(VW / 2 - 215 * s, VH - 60 - 156 * s)
  }
  falar (id: string, aoFim?: () => void) {
    const f = this.falas[id]; if (!f) { aoFim?.(); return }
    this.balao.setVisible(true)
    this.balaoNome.setText(f.quem); this.balaoNome.setBackgroundColor(f.cor); this.balaoTxt.setText('')
    if (this.typeTimer) this.typeTimer.remove()
    let i = 0; this.typeTimer = this.time.addEvent({ delay: 26, loop: true, callback: () => { i++; this.balaoTxt.setText(f.texto.slice(0, i)); if (i >= f.texto.length) this.typeTimer!.remove() } })
    const fim = () => aoFim && this.time.delayedCall(400, aoFim)
    if (!QA && this.audioOk[id]) { const s = this.sound.add(id); s.once('complete', () => { this.sound.removeByKey(id); fim() }); s.play() } else this.time.delayedCall(QA ? 220 : 1200 + f.texto.length * 42, fim)
  }
  dialogo (ids: string[], aoFim?: () => void) {
    this.estado = 'dialogo'
    const prox = (n: number) => { if (n >= ids.length) { this.balao.setVisible(false); this.estado = 'explora'; aoFim?.(); return } this.falar(ids[n], () => prox(n + 1)) }
    prox(0)
  }

  update (_t: number, dtMs: number) {
    const dt = Math.min(0.05, dtMs / 1000)
    const b = this.corpo.body as Phaser.Physics.Arcade.Body
    let andando = false
    if (this.estado === 'explora') {
      const v = 200; let dx = 0, dy = 0; const k = this.cursors, t = this.teclas
      if (k.left.isDown || t.A.isDown) dx -= 1
      if (k.right.isDown || t.D.isDown) dx += 1
      if (k.up.isDown || t.W.isDown) dy -= 1
      if (k.down.isDown || t.S.isDown) dy += 1
      if (dx || dy) this.alvo = null
      if (!dx && !dy && this.alvo) {
        const ax = this.alvo.x - this.corpo.x, ay = this.alvo.y - this.corpo.y, d = Math.hypot(ax, ay)
        if (d < 10) this.alvo = null
        else {
          dx = ax / d; dy = ay / d
          // preso na quina? (quase não anda) -> solta o alvo em ~0,35s
          const mov = Math.hypot(this.corpo.x - this.ultX, this.corpo.y - this.ultY)
          if (mov < 0.6) { this.travadoT += dt; if (this.travadoT > 0.35) { this.alvo = null; dx = 0; dy = 0; this.travadoT = 0 } } else this.travadoT = 0
        }
      }
      if (dx || dy) { const n = Math.hypot(dx, dy); dx /= n; dy /= n; b.setVelocity(dx * v, dy * v); andando = true; if (Math.abs(dx) > Math.abs(dy)) this.heroi.setDir(dx < 0 ? 'esq' : 'dir'); else this.heroi.setDir(dy < 0 ? 'cima' : 'baixo') } else b.setVelocity(0, 0)
    } else b.setVelocity(0, 0)
    this.ultX = this.corpo.x; this.ultY = this.corpo.y
    this.heroi.setPos(this.corpo.x, this.corpo.y)
    this.heroi.andar(andando); this.heroi.update(dt)
    if (andando && this.poeira) this.poeira.emitParticleAt(this.heroi.x, this.heroi.y, 1)

    for (const np of this.npcs) {
      np.update(dt)
      if (this.estado === 'explora') {
        const pid = (np as any)._parada as string
        const pref = (np as any)._ref as { quer_item?: string, ao_receber?: any } | undefined
        const dist = Phaser.Math.Distance.Between(this.heroi.x, this.heroi.y, np.x, np.y)
        // ENTREGA (problema->item->entrega->mundo muda) tem prioridade
        if (dist < 150 && pref && pref.quer_item && this.mochila && this.mochila.asset === pref.quer_item && !this.entregou[np.nome]) {
          this.alvo = null; b.setVelocity(0, 0)
          this.entregar(np, pref)
          continue
        }
        if (dist < 150 && !this.falado[pid]) {
          this.falado[pid] = true; this.alvo = null; b.setVelocity(0, 0)
          const falasIds = (np as any)._falaChegar as string[]
          if (falasIds && falasIds.length) this.dialogo(falasIds, () => this.abreMecanica(pid))
          else this.abreMecanica(pid)
        }
      }
    }

    // MISSÃO: agir ao passar por cima (o mundo reage; sem botão, sem painel)
    if (this.estado === 'explora' && this.zona.missao?.tipo === 'colher') {
      for (const im of this.itens) {
        if (!(im as any)._colhida && Math.abs(this.heroi.x - im.x) < 44 && Math.abs(this.heroi.y - im.y) < 50) this.colher(im)
      }
    }
    if (this.estado === 'explora' && this.zona.missao?.tipo === 'agrupar' && !this.missaoFeita()) this.agirAgrupar(_t)
    // o que está na MÃO acompanha a criança (cesta/maçã sobre a cabeça)
    if (this.carregando) this.carregando.img.setPosition(this.corpo.x, this.corpo.y - 116)

    // PORTAIS: chegou perto -> troca de zona (com fade)
    if (this.estado === 'explora' && _t > this.portalCd) {
      for (const pt of this.zona.portais) {
        if (Phaser.Math.Distance.Between(this.heroi.x, this.heroi.y, pt.x, pt.y) < pt.raio) { this.portalCd = _t + 900; this.transitar(pt); break }
      }
    }
  }

  abreMecanica (paradaId: string) {
    const p = this.zona.paradas.find(x => x.id === paradaId)
    if (!p || !p.mecanica || !temMecanica(p.mecanica.id)) {
      if (p && p.mecanica && !temMecanica(p.mecanica.id)) console.warn('mecânica não registrada:', p.mecanica.id)
      this.estado = 'explora'; return
    }
    this.paradaAtiva = paradaId
    this.estado = 'mecanica'
    abrirMecanica(p.mecanica.id, {
      scene: this,
      params: p.mecanica.params,
      paradaId,
      cor: p.cor,
      falar: (id, aoFim) => this.falar(id, aoFim),
      temAudio: (id) => !!this.audioOk[id],
      aoConcluir: () => { this.paradaAtiva = null; this.estado = 'explora' }
    })
  }
}
