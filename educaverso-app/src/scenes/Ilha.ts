// ============================================================================
// ETAPA 3 — MUNDO VIVO: Ilha do Tesouro  (versão PROFISSIONAL)
// REGRA DE OURO (Marcos): nada à mão. Tudo o que a criança vê é ARTE de IA;
// a VIDA vem do motor (partículas Phaser), a COLISÃO da física (Arcade), o
// TEXTO nítido do motor (setResolution), a VOZ por API (MP3 Antonio).
// Tela única 1024×768: a criança vê a cena TODA com o mascote (o baú sempre à
// vista). Só primitivas de efeito (sombra/brilho/pontinho) e um reserva
// invisível (anti-tela-quebrada) são de código.
// ============================================================================
import Phaser from 'phaser'
import { FALAS, IDS_FALAS } from '../falas'

const VW = 1024, VH = 768
const QA = new URLSearchParams(location.search).get('qa')

// área onde o Verso anda (a areia — parte de baixo/direita da pintura)
const WALK = { x0: 70, y0: 470, x1: 958, y1: 726 }

// a POÇA (tide pool de IA) e a grade lógica DENTRO dela (mecânica algoritmo)
const POOL = { x: 712, y: 566, w: 404, h: 270 }
const G = { cols: 4, rows: 3, cell: 60, x0: 560, y0: 452 }   // grade dentro da poça
const PEDRAS = [[0, 2], [1, 2], [1, 1], [2, 1], [3, 1], [3, 0], [0, 0]]
const CHEGADA = { c: 3, r: 0 }          // pedra do baú
const CHICO_INI = { c: -1, r: 2 }       // Chico na areia, à esquerda da poça
const MAX_PASSOS = 10

const DIRS: { [k: string]: { dc: number, dr: number, rot: string } } = {
  cima: { dc: 0, dr: -1, rot: '↑' }, baixo: { dc: 0, dr: 1, rot: '↓' },
  esq: { dc: -1, dr: 0, rot: '←' }, dir: { dc: 1, dr: 0, rot: '→' }
}
function el (id: string) { return document.getElementById(id) }

export class Ilha extends Phaser.Scene {
  player!: Phaser.Physics.Arcade.Image
  sombraP!: Phaser.GameObjects.Image
  louro!: Phaser.GameObjects.Image
  hintLouro!: Phaser.GameObjects.Text
  chico!: Phaser.GameObjects.Image
  sombraC!: Phaser.GameObjects.Image
  bau!: Phaser.GameObjects.Image
  obstaculos!: Phaser.Physics.Arcade.StaticGroup
  cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  teclas!: any
  alvo: { x: number, y: number } | null = null
  estado = 'intro'
  falouLouro = false
  passos: string[] = []
  aval = { inicio: 0, tentativas: 0 }
  resp = 0; passoFase = 0
  poeira!: Phaser.GameObjects.Particles.ParticleEmitter
  balao!: Phaser.GameObjects.Container
  balaoTxt!: Phaser.GameObjects.Text
  balaoNome!: Phaser.GameObjects.Text
  balaoAlvo: Phaser.GameObjects.Image | null = null
  typeTimer: Phaser.Time.TimerEvent | null = null
  ultimaFala = ''
  audioOk: { [id: string]: boolean } = {}
  ambienteLigado = false

  constructor () { super('Ilha') }

  preload () {
    const imgs = ['fundo', 'verso', 'palmeira', 'tocha', 'bau_fechado', 'bau_aberto',
      'louro', 'chico', 'pedra', 'rocha', 'pocao']
    this.load.image('fundo', 'img/fundo.jpg')
    for (const n of imgs) if (n !== 'fundo') this.load.image(n, 'img/' + n + '.png')
    if (!QA) for (const id of IDS_FALAS) this.load.audio(id, 'audio/' + id + '.mp3')
    this.load.on('loaderror', (f: any) => console.warn('asset ausente:', f.key))
    this.efeitos()          // só primitivas de efeito do motor (sombra/brilho/partícula)
  }

  create () {
    for (const id of IDS_FALAS) this.audioOk[id] = this.cache.audio.exists(id)
    this.reservas()

    // FUNDO de IA cobrindo a tela (nada desenhado à mão)
    const bg = this.add.image(0, 0, 'fundo').setOrigin(0, 0).setDepth(0)
    bg.setDisplaySize(VW, VH)

    // física: mundo = a areia caminhável
    this.physics.world.setBounds(WALK.x0, WALK.y0, WALK.x1 - WALK.x0, WALK.y1 - WALK.y0)
    this.obstaculos = this.physics.add.staticGroup()

    this.montarCena()
    this.criarPersonagens()
    this.criarBalao()
    this.vidaAmbiente()
    this.ligarHUD()

    this.cursors = this.input.keyboard!.createCursorKeys()
    this.teclas = this.input.keyboard!.addKeys('W,A,S,D,E,SPACE')
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.estado !== 'explora') return
      this.alvo = { x: Phaser.Math.Clamp(p.worldX, WALK.x0, WALK.x1), y: Phaser.Math.Clamp(p.worldY, WALK.y0, WALK.y1) }
    })

    if (QA) {
      this.estado = 'explora'
      el('telaIntro')?.classList.add('hidden')
      if (QA === 'missao') { this.player.setPosition(300, 640); this.iniciarMontagem(true) }
    }
  }

  // ---- primitivas de efeito do motor (não é "arte à mão", são utilidades) ----
  efeitos () {
    this.circulo('glow', 90, 'rgba(255,190,90,', 0.5)
    this.circulo('glowFrio', 60, 'rgba(170,225,255,', 0.4)
    this.circulo('vaga', 8, 'rgba(200,255,150,', 0.95)
    this.circulo('puff', 14, 'rgba(225,210,180,', 0.6)
    this.circulo('gota', 7, 'rgba(210,235,255,', 0.95)
    this.circulo('faisca', 9, 'rgba(255,225,120,', 0.98)
    const so = this.textures.createCanvas('sombra', 70, 26)!
    const gs = so.getContext()
    const gr = gs.createRadialGradient(35, 13, 2, 35, 13, 33)
    gr.addColorStop(0, 'rgba(6,10,18,.5)'); gr.addColorStop(1, 'rgba(6,10,18,0)')
    gs.fillStyle = gr; gs.beginPath(); gs.ellipse(35, 13, 33, 12, 0, 0, 7); gs.fill(); so.refresh()
    const mk = this.textures.createCanvas('marca', 70, 70)!
    const gm = mk.getContext(); gm.strokeStyle = 'rgba(150,225,255,.6)'; gm.lineWidth = 3
    gm.beginPath(); gm.arc(35, 35, 26, 0, 7); gm.stroke(); mk.refresh()
  }
  circulo (n: string, raio: number, c: string, a: number) {
    const d = raio * 2, t = this.textures.createCanvas(n, d, d)!, g = t.getContext()
    const grd = g.createRadialGradient(raio, raio, 1, raio, raio, raio)
    grd.addColorStop(0, c + a + ')'); grd.addColorStop(1, c + '0)')
    g.fillStyle = grd; g.fillRect(0, 0, d, d); t.refresh()
  }

  // reserva pintado SÓ se um asset de IA não carregar (nunca dá tela quebrada)
  reservas () {
    const mk: { [k: string]: [number, number, string] } = {
      fundo: [VW, VH, '#0b2a44'], verso: [120, 150, '#8fd4ff'], palmeira: [160, 300, '#2f7d4f'],
      tocha: [40, 120, '#c8862f'], bau_fechado: [120, 96, '#7a4d28'], bau_aberto: [120, 96, '#d9a23c'],
      louro: [90, 100, '#2e9c5b'], chico: [90, 66, '#e2703a'], pedra: [80, 54, '#8b93a0'],
      rocha: [120, 84, '#5d6672'], pocao: [420, 280, '#12506f']
    }
    for (const k of Object.keys(mk)) {
      if (this.textures.exists(k)) continue
      const [w, h, cor] = mk[k]
      const t = this.textures.createCanvas(k, w, h)!, g = t.getContext()
      g.fillStyle = cor
      if (k === 'pocao') { g.beginPath(); g.ellipse(w / 2, h / 2, w / 2 - 4, h / 2 - 4, 0, 0, 7); g.fill() }
      else if (k === 'fundo') { g.fillRect(0, 0, w, h) }
      else { g.beginPath(); g.ellipse(w / 2, h * 0.6, w / 2 - 4, h * 0.4, 0, 0, 7); g.fill() }
      t.refresh()
    }
  }

  colocar (chave: string, x: number, y: number, alt: number, flip = false) {
    const im = this.add.image(x, y, chave).setOrigin(0.5, 1)
    im.setScale(alt / im.height).setDepth(y).setFlipX(flip)
    return im
  }
  // caixa de colisão estática (invisível) para um obstáculo
  bloco (x: number, y: number, w: number, h: number) {
    const b = this.add.rectangle(x, y, w, h).setVisible(false)
    this.physics.add.existing(b, true)
    this.obstaculos.add(b)
  }

  montarCena () {
    // a POÇA (água de IA) no chão + brilho da lua
    const pool = this.add.image(POOL.x, POOL.y, 'pocao').setDepth(POOL.y - 120)
    pool.setDisplaySize(POOL.w, POOL.h)
    // colisão: o Verso não entra na água (elipse aproximada por caixa)
    this.bloco(POOL.x, POOL.y + 20, POOL.w * 0.82, POOL.h * 0.7)

    // pedras da grade (passagem do Chico) + baú na chegada
    for (const p of PEDRAS) {
      const im = this.add.image(this.cx(p[0]), this.cy(p[1]) + 10, 'pedra').setOrigin(0.5, 0.7)
      im.setScale(58 / im.width).setDepth(this.cy(p[1]))
    }
    const bx = this.cx(CHEGADA.c), by = this.cy(CHEGADA.r)
    this.bau = this.colocar('bau_fechado', bx, by + 8, 66); this.bau.setDepth(by + 40)
    const gb = this.add.image(bx, by - 16, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(by + 41)
    this.tweens.add({ targets: gb, alpha: { from: 0.3, to: 0.85 }, scale: { from: 0.8, to: 1.25 }, duration: 1100, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })

    // palmeiras (decoração viva) — nos cantos da areia, longe do caminho
    const p1 = this.colocar('palmeira', 930, 486, 300)
    const p2 = this.colocar('palmeira', 140, 470, 250, true)
    for (let i = 0; i < 2; i++) {
      const alvo = i ? p2 : p1
      this.tweens.add({ targets: alvo, angle: { from: -1.4, to: 1.4 }, duration: 3000 + i * 500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
      this.bloco(alvo.x, alvo.y, 34, 20)   // tronco colide
    }

    // tocha viva (luz pulsando) — acampamento na praia
    this.colocar('tocha', 360, 556, 120)
    const gl = this.add.image(360, 470, 'glow').setBlendMode(Phaser.BlendModes.ADD).setDepth(600)
    this.tweens.add({ targets: gl, alpha: { from: 0.55, to: 1 }, scale: { from: 0.85, to: 1.12 }, duration: 240, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })

    // rochas decorativas (com colisão)
    const r1 = this.colocar('rocha', 600, 720, 66)
    this.bloco(r1.x, r1.y - 12, 70, 24)
  }

  cx (c: number) { return G.x0 + c * G.cell + G.cell / 2 }
  cy (r: number) { return G.y0 + r * G.cell + G.cell / 2 }
  ehPedra (c: number, r: number) { return PEDRAS.some(p => p[0] === c && p[1] === r) }

  criarPersonagens () {
    // Verso (a criança) — sprite de IA + FÍSICA (colisão perfeita)
    this.sombraP = this.add.image(200, 654, 'sombra').setDepth(1)
    this.player = this.physics.add.image(200, 650, 'verso').setOrigin(0.5, 1)
    this.player.setScale(84 / this.player.height)
    const pb = this.player.body as Phaser.Physics.Arcade.Body
    pb.setSize(46, 26); pb.setOffset((this.player.width - 46) / 2, this.player.height - 26)
    this.player.setCollideWorldBounds(true)
    this.physics.add.collider(this.player, this.obstaculos)
    // poeira ao andar (emissor de partículas do MOTOR)
    this.poeira = this.add.particles(0, 0, 'puff', {
      lifespan: 420, speed: { min: 4, max: 16 }, angle: { min: 200, max: 340 },
      scale: { start: 0.5, end: 1.3 }, alpha: { start: 0.5, end: 0 }, emitting: false
    })
    this.poeira.setDepth(640)

    // Louro POUSADO numa rocha (não flutua) — mexe a cabeça e dá "crá"
    const rL = this.colocar('rocha', 470, 616, 74)
    this.bloco(rL.x, rL.y - 14, 78, 26)
    this.add.image(470, 588, 'sombra').setDepth(rL.depth + 1).setScale(0.6)
    this.louro = this.colocar('louro', 470, 568, 64, true)
    this.louro.setOrigin(0.5, 1).setDepth(rL.depth + 2)
    this.vidaLouro()
    this.hintLouro = this.add.text(470, 492, '!', { fontFamily: 'Arial Black, Arial', fontSize: '30px', color: '#ffd25a', stroke: '#3a2a00', strokeThickness: 5 }).setOrigin(0.5).setDepth(9500)
    this.tweens.add({ targets: this.hintLouro, y: '-=10', duration: 520, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })

    // Chico (caranguejo) na areia, à esquerda da poça
    this.sombraC = this.add.image(this.cx(CHICO_INI.c), this.cy(CHICO_INI.r) + 14, 'sombra').setDepth(1).setScale(0.7)
    this.chico = this.add.image(this.cx(CHICO_INI.c), this.cy(CHICO_INI.r) + 8, 'chico').setOrigin(0.5, 1)
    this.chico.setScale(46 / this.chico.height).setDepth(this.chico.y)
    this.tweens.add({ targets: this.chico, angle: { from: -4, to: 4 }, duration: 800, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
  }

  vidaLouro () {
    this.tweens.add({ targets: this.louro, scaleY: { from: this.louro.scaleY, to: this.louro.scaleY * 1.03 }, duration: 1300, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    const olhar = () => {
      this.tweens.add({ targets: this.louro, angle: (Math.random() < 0.5 ? -6 : 6), duration: 220, yoyo: true, hold: 500, ease: 'Sine.easeInOut' })
      if (Math.random() < 0.6) this.som('cra')
      this.time.delayedCall(2200 + Math.random() * 2600, olhar)
    }
    this.time.delayedCall(1200, olhar)
  }

  // ---- balão RPG (texto em ALTA RESOLUÇÃO — nítido) ----
  criarBalao () {
    const bg = this.add.graphics()
    bg.fillStyle(0xffffff, 0.97); bg.lineStyle(3, 0x22314f, 1)
    bg.fillRoundedRect(0, 0, 430, 116, 16); bg.strokeRoundedRect(0, 0, 430, 116, 16)
    bg.fillStyle(0x22314f, 1); bg.fillTriangle(200, 116, 230, 116, 215, 136)
    this.balaoNome = this.add.text(16, -12, '', { fontFamily: 'Arial Black, Arial', fontSize: '15px', color: '#fff' }).setPadding(8, 3, 8, 3)
    this.balaoTxt = this.add.text(16, 14, '', { fontFamily: 'Arial', fontSize: '17px', color: '#22314f', wordWrap: { width: 398 }, lineSpacing: 4 })
    const rr = Math.max(2, Math.min(3, Math.round((window.devicePixelRatio || 1) * 1.5)))
    this.balaoTxt.setResolution(rr); this.balaoNome.setResolution(rr)
    const seta = this.add.text(400, 86, '▼', { fontFamily: 'Arial', fontSize: '15px', color: '#5a7bbf' })
    this.tweens.add({ targets: seta, y: '+=5', duration: 460, yoyo: true, repeat: -1 })
    this.balao = this.add.container(0, 0, [bg, this.balaoNome, this.balaoTxt, seta]).setDepth(9800).setVisible(false)
  }
  posicionarBalao () {
    if (!this.balao.visible || !this.balaoAlvo) return
    let x = Phaser.Math.Clamp(this.balaoAlvo.x - 215, 12, VW - 442)
    let y = Phaser.Math.Clamp(this.balaoAlvo.y - this.balaoAlvo.displayHeight - 150, 12, VH - 240)
    this.balao.setPosition(x, y)
  }

  falar (id: string, aoFim?: () => void) {
    const f = FALAS[id]; if (!f) { aoFim?.(); return }
    this.ultimaFala = id
    this.balaoAlvo = (f.quem === 'Louro') ? this.louro : this.player
    this.balao.setVisible(true); this.balaoNome.setText(f.quem); this.balaoNome.setBackgroundColor(f.cor); this.balaoTxt.setText('')
    if (this.typeTimer) this.typeTimer.remove()
    let i = 0
    this.typeTimer = this.time.addEvent({ delay: 26, loop: true, callback: () => { i++; this.balaoTxt.setText(f.texto.slice(0, i)); if (i >= f.texto.length) this.typeTimer!.remove() } })
    const fim = () => aoFim && this.time.delayedCall(350, aoFim)
    if (!QA && this.audioOk[id]) { const s = this.sound.add(id); s.once('complete', fim); s.play() }
    else this.time.delayedCall(1200 + f.texto.length * 42, fim)
  }
  dialogo (ids: string[], aoFim?: () => void) {
    this.estado = 'dialogo'
    const prox = (n: number) => {
      if (n >= ids.length) { this.balao.setVisible(false); if (aoFim) aoFim(); else this.estado = 'explora'; return }
      this.falar(ids[n], () => prox(n + 1))
    }
    prox(0)
  }

  vidaAmbiente () {
    // vaga-lumes: emissor de partículas do MOTOR pela vegetação (surgem e somem)
    this.add.particles(0, 0, 'vaga', {
      x: { min: 90, max: 950 }, y: { min: 500, max: 705 },
      lifespan: 2600, frequency: 240, quantity: 1, blendMode: 'ADD',
      alpha: { start: 0.85, end: 0 },
      scale: { start: 0.5, end: 1.1 },
      speedX: { min: -12, max: 12 }, speedY: { min: -16, max: 6 },
      emitting: true
    }).setDepth(9000)
  }

  ligarAmbiente () {
    if (this.ambienteLigado || QA) return
    this.ambienteLigado = true
    try {
      const ctx: AudioContext = (this.sound as any).context; if (!ctx) return
      const sr = ctx.sampleRate, buf = ctx.createBuffer(1, sr * 2.2, sr), d = buf.getChannelData(0)
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * 0.35
      const src = ctx.createBufferSource(); src.buffer = buf; src.loop = true
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 430
      const ga = ctx.createGain(); ga.gain.value = 0.06
      src.connect(lp); lp.connect(ga); ga.connect(ctx.destination); src.start()
      const lfo = ctx.createOscillator(); lfo.frequency.value = 0.14
      const lg = ctx.createGain(); lg.gain.value = 0.03; lfo.connect(lg); lg.connect(ga.gain); lfo.start()
    } catch (e) {}
  }

  som (tipo: string) {
    if (QA) return
    try {
      const ctx: AudioContext = (this.sound as any).context; if (!ctx) return
      const t0 = ctx.currentTime
      if (tipo === 'splash') {
        const b = ctx.createBuffer(1, ctx.sampleRate * 0.3, ctx.sampleRate), d = b.getChannelData(0)
        for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length)
        const s = ctx.createBufferSource(); s.buffer = b
        const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 900
        const g = ctx.createGain(); g.gain.value = 0.25; s.connect(f); f.connect(g); g.connect(ctx.destination); s.start()
      } else if (tipo === 'cra') {
        for (let k = 0; k < 2; k++) {
          const o = ctx.createOscillator(); o.type = 'sawtooth'; const g = ctx.createGain(); g.gain.value = 0
          o.connect(g); g.connect(ctx.destination); const ta = t0 + k * 0.13
          o.frequency.setValueAtTime(720, ta); o.frequency.exponentialRampToValueAtTime(430, ta + 0.1)
          g.gain.setValueAtTime(0.06, ta); g.gain.exponentialRampToValueAtTime(0.001, ta + 0.11); o.start(ta); o.stop(ta + 0.13)
        }
      } else if (tipo === 'passo') {
        const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = 300
        const g = ctx.createGain(); g.gain.value = 0.05; o.connect(g); g.connect(ctx.destination); o.start()
        o.frequency.exponentialRampToValueAtTime(190, t0 + 0.09); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.1); o.stop(t0 + 0.12)
      } else if (tipo === 'tap') {
        const o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = 660
        const g = ctx.createGain(); g.gain.value = 0.06; o.connect(g); g.connect(ctx.destination); o.start()
        g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.12); o.stop(t0 + 0.14)
      } else if (tipo === 'vitoria') {
        const notas = [523, 659, 784, 1047]
        for (let i = 0; i < notas.length; i++) {
          const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = notas[i]
          const g = ctx.createGain(); g.gain.value = 0; o.connect(g); g.connect(ctx.destination); o.start(t0 + i * 0.14)
          g.gain.setValueAtTime(0.09, t0 + i * 0.14); g.gain.exponentialRampToValueAtTime(0.001, t0 + i * 0.14 + 0.5); o.stop(t0 + i * 0.14 + 0.55)
        }
      }
    } catch (e) {}
  }

  ligarHUD () {
    const bC = el('btnComecar'); if (bC) bC.onclick = () => { el('telaIntro')?.classList.add('hidden'); this.ligarAmbiente(); this.estado = 'dialogo'; this.time.delayedCall(400, () => this.dialogo(['n_bemvindo'])) }
    const bO = el('btnOuvir'); if (bO) bO.onclick = () => { if (this.ultimaFala && this.estado !== 'executa') this.falar(this.ultimaFala) }
    document.querySelectorAll('.seta').forEach((b: any) => { b.onclick = () => { if (this.estado === 'montar' && this.passos.length < MAX_PASSOS) { this.som('tap'); this.passos.push(b.dataset.dir); this.desenhar() } } })
    const bJ = el('btnJogar'); if (bJ) bJ.onclick = () => this.executar()
    const bL = el('btnLimpar'); if (bL) bL.onclick = () => { if (this.estado === 'montar') { this.passos = []; this.desenhar() } }
    const bD = el('btnDeNovo'); if (bD) bD.onclick = () => { el('telaWin')?.classList.add('hidden'); this.estado = 'explora' }
  }
  desenhar () {
    const box = el('passos'); if (!box) return
    box.innerHTML = this.passos.length ? this.passos.map((p, i) => '<span class="chip" id="chip' + i + '">' + DIRS[p].rot + '</span>').join('') : '<span class="vazio">seus passos aparecem aqui…</span>'
  }
  iniciarMontagem (silencioso = false) {
    this.estado = 'montar'
    if (!this.aval.inicio) this.aval.inicio = Date.now()
    el('hud')?.classList.remove('hidden')
    const d = el('dica'); if (d) d.innerHTML = 'Monte os passos do <b>Chico</b> 🦀 até o baú — cuidado com a água!'
    this.desenhar(); this.hintLouro.setVisible(false)
    if (!silencioso) for (const p of PEDRAS) {
      const m = this.add.image(this.cx(p[0]), this.cy(p[1]), 'marca').setDepth(8000).setAlpha(0)
      this.tweens.add({ targets: m, alpha: { from: 0, to: 0.7 }, duration: 500, yoyo: true, repeat: 1, onComplete: () => m.destroy() })
    }
  }

  executar () {
    if (this.estado !== 'montar' || !this.passos.length) return
    this.estado = 'executa'; this.aval.tentativas++
    let c = CHICO_INI.c, r = CHICO_INI.r
    const passo = (n: number) => {
      if (n >= this.passos.length) {
        if (c === CHEGADA.c && r === CHEGADA.r) this.vitoria()
        else this.dialogo(['l_quase'], () => { this.estado = 'montar' })
        return
      }
      const dr = DIRS[this.passos[n]]; c += dr.dc; r += dr.dr
      const chip = el('chip' + n); if (chip) chip.style.background = '#57e08a'
      const nx = this.cx(c), ny = this.cy(r) + 8; this.som('passo')
      this.tweens.add({
        targets: this.chico, x: nx, y: ny, duration: 340, ease: 'Sine.easeInOut',
        onUpdate: () => { this.sombraC.setPosition(this.chico.x, this.chico.y + 6); this.chico.setDepth(this.chico.y) },
        onComplete: () => {
          const dentro = c >= 0 && r >= 0 && c < G.cols && r < G.rows
          const naAgua = (dentro && !this.ehPedra(c, r)) || r < 0 || c >= G.cols
          if (naAgua) { this.splash(nx, ny); return }
          if (c === CHEGADA.c && r === CHEGADA.r) { this.vitoria(); return }
          this.time.delayedCall(140, () => passo(n + 1))
        }
      })
    }
    passo(0)
  }
  splash (x: number, y: number) {
    this.som('splash')
    this.add.particles(x, y - 6, 'gota', { lifespan: 460, speed: { min: 40, max: 120 }, angle: { min: 210, max: 330 }, scale: { start: 1, end: 0.2 }, alpha: { start: 0.95, end: 0 }, quantity: 8, emitting: false }).explode(8)
    this.tweens.add({
      targets: this.chico, alpha: 0, duration: 260, onComplete: () => {
        this.chico.setPosition(this.cx(CHICO_INI.c), this.cy(CHICO_INI.r) + 8); this.sombraC.setPosition(this.chico.x, this.chico.y + 6); this.chico.setDepth(this.chico.y)
        this.tweens.add({ targets: this.chico, alpha: 1, duration: 300 })
        this.dialogo(['l_agua'], () => { this.estado = 'montar' })
      }
    })
  }
  vitoria () {
    this.estado = 'fim'; this.som('vitoria')
    this.bau.setTexture('bau_aberto'); this.bau.setScale(66 / this.bau.height)
    this.add.particles(this.bau.x, this.bau.y - 30, 'faisca', { lifespan: 1100, speed: { min: 30, max: 120 }, angle: { min: 200, max: 340 }, scale: { start: 1, end: 0.2 }, alpha: { start: 1, end: 0 }, quantity: 14, emitting: false }).explode(14)
    this.tweens.add({ targets: this.chico, y: '-=14', duration: 240, yoyo: true, repeat: 3, ease: 'Sine.easeInOut' })
    this.registra()
    el('hud')?.classList.add('hidden')
    this.dialogo(['l_vitoria', 'n_conceito'], () => { el('telaWin')?.classList.remove('hidden'); this.estado = 'fim' })
  }
  registra () {
    try {
      const reg = JSON.parse(localStorage.getItem('eduverso_aval') || '[]')
      reg.push({ etapa: 'ilha_tesouro', mecanica: 'ordenar_comandos', objetivo: '1A2_1A3_algoritmos', tentativas: this.aval.tentativas, tempo_seg: Math.round((Date.now() - this.aval.inicio) / 1000), acerto: true, quando: new Date().toISOString() })
      localStorage.setItem('eduverso_aval', JSON.stringify(reg))
    } catch (e) {}
  }

  update (_t: number, dtMs: number) {
    const dt = Math.min(0.05, dtMs / 1000)
    const andando = this.mover()
    const base = 84 / this.player.height
    if (andando) {
      this.passoFase += dt * 12; const b = Math.sin(this.passoFase)
      this.player.setScale(base * (1 - 0.05 * b), base * (1 + 0.07 * b))
      this.player.setAngle(3.5 * Math.sin(this.passoFase * 0.5))
      this.sombraP.setScale(1 - 0.14 * Math.max(0, b))
      if (this.poeira) this.poeira.emitParticleAt(this.player.x, this.player.y, 1)
    } else {
      this.resp += dt * 2.2; const r = Math.sin(this.resp)
      this.player.setScale(base * (1 - 0.02 * r), base * (1 + 0.03 * r))
      this.player.setAngle(0); this.sombraP.setScale(1)
    }
    this.sombraP.setPosition(this.player.x, this.player.y + 4); this.player.setDepth(this.player.y)

    if (this.estado === 'montar') {
      const mp: any = { cima: this.cursors.up, baixo: this.cursors.down, esq: this.cursors.left, dir: this.cursors.right }
      for (const d of Object.keys(mp)) if (Phaser.Input.Keyboard.JustDown(mp[d]) && this.passos.length < MAX_PASSOS) { this.som('tap'); this.passos.push(d); this.desenhar() }
    }
    if (this.estado === 'explora') {
      const dist = Phaser.Math.Distance.Between(this.player.x, this.player.y, this.louro.x, this.louro.y)
      if (dist < 150 && !this.falouLouro) { this.falouLouro = true; this.alvo = null; this.pararPlayer(); this.dialogo(['l_ola', 'l_problema', 'l_como'], () => this.iniciarMontagem()) }
    }
    this.posicionarBalao()
  }

  pararPlayer () { const b = this.player.body as Phaser.Physics.Arcade.Body; b.setVelocity(0, 0) }

  // MOVIMENTO por FÍSICA (Arcade): colisão perfeita, desliza em espaços apertados
  mover (): boolean {
    const b = this.player.body as Phaser.Physics.Arcade.Body
    if (this.estado !== 'explora') { b.setVelocity(0, 0); return false }
    const v = 200
    let dx = 0, dy = 0
    const k = this.cursors, t = this.teclas
    if (k.left.isDown || t.A.isDown) dx -= 1
    if (k.right.isDown || t.D.isDown) dx += 1
    if (k.up.isDown || t.W.isDown) dy -= 1
    if (k.down.isDown || t.S.isDown) dy += 1
    if (dx || dy) this.alvo = null
    if (!dx && !dy && this.alvo) {
      const ax = this.alvo.x - this.player.x, ay = this.alvo.y - this.player.y, d = Math.hypot(ax, ay)
      if (d < 8) { this.alvo = null } else { dx = ax / d; dy = ay / d }
    }
    if (!dx && !dy) { b.setVelocity(0, 0); return false }
    const n = Math.hypot(dx, dy); dx /= n; dy /= n
    b.setVelocity(dx * v, dy * v)
    if (dx < 0) this.player.setFlipX(true); else if (dx > 0) this.player.setFlipX(false)
    return true
  }
}
