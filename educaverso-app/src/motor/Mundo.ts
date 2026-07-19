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
import type { TAventura, TZona, TObjeto, TPortal } from './aventura'

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
  }
  spawnPt!: { x: number, y: number }

  // ---- memória (o mundo LEMBRA da criança) ----
  mem (): any { try { return JSON.parse(localStorage.getItem('ev_' + this.av.id) || '{}') } catch (e) { return {} } }
  memSalva (m: any) { try { localStorage.setItem('ev_' + this.av.id, JSON.stringify(m)) } catch (e) {} }
  missaoFeita () { return !!(this.mem().missoes || {})[this.zona.id] }

  preload () {
    const z = this.zona
    this.load.image('prancha_' + z.id, 'img/' + z.prancha)
    const objs = new Set<string>()
    for (const p of z.paradas) for (const o of p.objetos) objs.add(o.asset)
    if (z.missao) { objs.add(z.missao.asset); objs.add('cesta') }
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

    // PRANCHA pintada — o mundo é MAIOR que a tela (câmera explora)
    if (this.textures.exists('prancha_' + z.id)) {
      this.add.image(0, 0, 'prancha_' + z.id).setOrigin(0, 0).setDisplaySize(z.largura, z.altura).setDepth(0)
    } else { this.add.rectangle(z.largura / 2, z.altura / 2, z.largura, z.altura, 0x3f6f4a).setDepth(0) }

    // faixa ANDÁVEL: da linha do horizonte pra baixo (não anda no céu/copa)
    this.physics.world.setBounds(56, z.chao_min_y, z.largura - 112, z.altura - z.chao_min_y - 44)
    this.obst = this.physics.add.staticGroup()

    for (const p of z.paradas) {
      for (const o of p.objetos) this.colocaObjeto(o)
      for (const pr of p.personagens) {
        const np = new Personagem(this, pr.nome, pr.x, pr.y, pr.alt)
        ;(np as any)._falaChegar = pr.fala_ao_chegar
        ;(np as any)._parada = p.id
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

    // chegada: falas da 1ª visita (o mundo dá boas-vindas UMA vez)
    const m = this.mem(); m.visitadas = m.visitadas || {}
    if (!m.visitadas[z.id] && z.chegada.length) {
      m.visitadas[z.id] = true; this.memSalva(m)
      this.time.delayedCall(500, () => this.dialogo(z.chegada))
    } else if (!m.visitadas[z.id]) { m.visitadas[z.id] = true; this.memSalva(m) }

    // ganchos de QA (o robô dirige o mundo de verdade)
    ;(window as any).__mundo = this
    ;(window as any).__irZona = (id: string) => this.transitar({ x: 0, y: 0, raio: 0, para: id, spawn: this.av.inicio, rotulo: '' })
    ;(window as any).__colher1 = () => { const i = this.itens.find(it => it.visible && !(it as any)._colhida); if (i) this.colher(i) }
    if (new URLSearchParams(location.search).has('mec')) {
      const alvoP = z.paradas.find(p => p.mecanica && temMecanica(p.mecanica.id))
      if (alvoP) this.time.delayedCall(400, () => this.abreMecanica(alvoP.id))
    }
  }

  // ---------- missão "colher" ----------
  armaMissao () {
    const mi = this.zona.missao!
    if (this.missaoFeita()) {
      this.cestaCheia(mi)
      const np = mi.npc ? this.npcPorNome[mi.npc] : null
      if (np) { np.feliz(2.5); (np as any)._falaChegar = mi.fala_revisita }
      return
    }
    this.add.image(mi.cesta.x, mi.cesta.y, 'cesta').setOrigin(0.5, 1).setScale(120 / this.textures.get('cesta').getSourceImage().height).setDepth(mi.cesta.y)
    for (const it of mi.itens) {
      const im = this.add.image(it.x, it.y, mi.asset).setOrigin(0.5, 1)
      im.setScale(mi.alt / im.height).setDepth(it.y)
      ;(im as any)._tw = this.tweens.add({ targets: im, y: it.y - 5, duration: 700 + Math.random() * 200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      this.itens.push(im)
    }
  }
  cestaCheia (mi: { cesta: { x: number, y: number }, asset: string }) {
    this.add.image(mi.cesta.x, mi.cesta.y, 'cesta').setOrigin(0.5, 1).setScale(120 / this.textures.get('cesta').getSourceImage().height).setDepth(mi.cesta.y)
    for (let i = 0; i < 5; i++) {
      const mx = mi.cesta.x + (i % 3 - 1) * 26, my = mi.cesta.y - 52 - Math.floor(i / 3) * 18
      this.add.image(mx, my, mi.asset).setOrigin(0.5, 1).setScale(34 / this.textures.get(mi.asset).getSourceImage().height).setDepth(mi.cesta.y + 1)
    }
  }
  colher (im: Phaser.GameObjects.Image) {
    const mi = this.zona.missao!
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
    // o item VOA pra cesta (o mundo reage) e fica LÁ (consequência visível)
    const tw = (im as any)._tw as Phaser.Tweens.Tween | undefined; if (tw) tw.remove()
    const mx = mi.cesta.x + (n % 3 - 1) * 26, my = mi.cesta.y - 52 - Math.floor((n - 1) / 3) * 18
    this.tweens.add({
      targets: im, x: mx, y: my, scale: 34 / this.textures.get(mi.asset).getSourceImage().height, duration: 520, ease: 'Cubic.easeInOut',
      onComplete: () => { im.setDepth(mi.cesta.y + 1) }
    })
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (np) np.feliz(0.9)
    if (this.colhidas >= mi.itens.length) this.time.delayedCall(750, () => this.missaoCompleta())
  }
  missaoCompleta () {
    const mi = this.zona.missao!
    const m = this.mem(); m.missoes = m.missoes || {}; m.missoes[this.zona.id] = true; this.memSalva(m)
    const np = mi.npc ? this.npcPorNome[mi.npc] : null
    if (np) { np.feliz(60); (np as any)._falaChegar = mi.fala_revisita }
    this.heroi.feliz(3)
    this.confete()
    if (mi.ao_completar.length) this.dialogo(mi.ao_completar)
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
    if (!this.textures.exists(o.asset)) return
    const im = this.add.image(o.x, o.y, o.asset).setOrigin(0.5, 1)
    im.setScale(o.alt / im.height).setFlipX(o.flip).setDepth(o.profundidade ?? o.y)
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
    if (!QA && this.audioOk[id]) { const s = this.sound.add(id); s.once('complete', () => { this.sound.removeByKey(id); fim() }); s.play() } else this.time.delayedCall(1200 + f.texto.length * 42, fim)
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
        const dist = Phaser.Math.Distance.Between(this.heroi.x, this.heroi.y, np.x, np.y)
        if (dist < 150 && !this.falado[pid]) {
          this.falado[pid] = true; this.alvo = null; b.setVelocity(0, 0)
          const falasIds = (np as any)._falaChegar as string[]
          if (falasIds && falasIds.length) this.dialogo(falasIds, () => this.abreMecanica(pid))
          else this.abreMecanica(pid)
        }
      }
    }

    // MISSÃO: colher ao passar por cima (o mundo reage; sem botão, sem painel)
    if (this.estado === 'explora' && this.zona.missao) {
      for (const im of this.itens) {
        if (!(im as any)._colhida && Math.abs(this.heroi.x - im.x) < 44 && Math.abs(this.heroi.y - im.y) < 50) this.colher(im)
      }
    }

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
