// ============================================================================
// ETAPA 3 — O MUNDO VIVO EXPLORÁVEL: Ilha do Tesouro (noite)
// ----------------------------------------------------------------------------
// - A criança ANDA livre pela ilha (setas/WASD ou toque) com câmera seguindo.
// - Cena VIVA (style bible): tudo respira, ondas, vagalumes, palmeiras
//   balançando, sombras, poeirinha ao andar, balão RPG com typewriter.
// - O problema aparece NO CONTEXTO: o Louro (NPC) conta que o baú ficou preso
//   nas pedras; a criança programa o caranguejo Chico (mecânica reutilizável
//   "ordenar comandos"). O conceito ALGORITMO é nomeado por ÚLTIMO.
// - VOZ: MP3 gerados por API (Antonio/Donato) — nunca a voz do navegador.
// - Arte: assets pintados por IA (public/img). Se um asset faltar, o código
//   pinta um reserva simples (o mundo nunca quebra).
// - Avaliação invisível: tentativas/tempo/acerto em localStorage.
// ============================================================================
import Phaser from 'phaser'
import { FALAS, IDS_FALAS } from '../falas'

const VW = 1024, VH = 768
const WORLD_W = 2400, WORLD_H = 768

// faixa onde dá para andar (areia seca)
const WALK = { x0: 60, x1: 2340, y0: 480, y1: 668 }

// a ENSEADA (onde mora a mecânica): o mar entra na praia formando uma baía
// rasa com pedras — a grade de células vive DENTRO dela.
// FICÇÃO: o norte (r<0) e o fundo (c>=cols) são água funda; o lado da praia
// (c<0) e o sul (r>=rows) são areia.
const POCA = { x0: 1780, y0: 450, cols: 5, rows: 3, cell: 64 }
const ENSEADA = { c: 1940, e0: 1700, e1: 2180, borda: 110, prof: 210 }
// pedras seguras (c,r) — o caminho + uma pedra "isca"
const PEDRAS = [[0, 2], [1, 2], [2, 2], [2, 1], [3, 1], [4, 1], [4, 0], [1, 0]]
const CHEGADA = { c: 4, r: 0 }          // a pedra do baú
const CHICO_INICIO = { c: -1, r: 2 }    // Chico começa na areia, à esquerda da poça
const MAX_PASSOS = 10

// modo QA (screenshot no CI): ?qa=inicio | ?qa=missao — sem áudio, sem intro
const QA = new URLSearchParams(location.search).get('qa')

const DIRS: { [k: string]: { dc: number, dr: number, rot: string } } = {
  cima: { dc: 0, dr: -1, rot: '↑' },
  baixo: { dc: 0, dr: 1, rot: '↓' },
  esq: { dc: -1, dr: 0, rot: '←' },
  dir: { dc: 1, dr: 0, rot: '→' }
}

function el (id: string): HTMLElement | null { return document.getElementById(id) }

export class Ilha extends Phaser.Scene {
  player!: Phaser.GameObjects.Image
  sombraP!: Phaser.GameObjects.Image
  louro!: Phaser.GameObjects.Image
  hintLouro!: Phaser.GameObjects.Text
  chico!: Phaser.GameObjects.Image
  sombraC!: Phaser.GameObjects.Image
  bau!: Phaser.GameObjects.Image
  cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  teclas!: any
  alvo: { x: number, y: number } | null = null
  estado = 'intro'          // intro | explora | dialogo | montar | executa | fim
  falouComLouro = false
  passos: string[] = []
  aval = { inicio: 0, tentativas: 0 }
  resp = 0                  // fase da respiração
  puffT = 0
  balao!: Phaser.GameObjects.Container
  balaoTxt!: Phaser.GameObjects.Text
  balaoNome!: Phaser.GameObjects.Text
  balaoPlaca!: Phaser.GameObjects.Graphics
  balaoAlvo: Phaser.GameObjects.Image | null = null
  typeTimer: Phaser.Time.TimerEvent | null = null
  ultimaFala = ''
  audioOk: { [id: string]: boolean } = {}
  ambienteLigado = false

  constructor () { super('Ilha') }

  // ==========================================================================
  // PRELOAD — assets de IA (com reserva pintada por código se faltar)
  // ==========================================================================
  preload () {
    const imgs = ['palmeira', 'tocha', 'bau_fechado', 'bau_aberto', 'louro', 'chico', 'pedra', 'rocha', 'capim']
    for (const n of imgs) this.load.image(n, 'img/' + n + '.png')
    if (!QA) {
      for (const id of IDS_FALAS) this.load.audio(id, 'audio/' + id + '.mp3')
    }
    this.load.on('loaderror', (f: any) => { console.warn('asset ausente:', f.key) })
    this.pintarTexturasBase()
  }

  create () {
    for (const id of IDS_FALAS) this.audioOk[id] = this.cache.audio.exists(id)
    this.garantirReservas()

    this.cameras.main.setBounds(0, 0, WORLD_W, WORLD_H)
    this.add.image(0, 0, 'cenario').setOrigin(0, 0).setDepth(0)

    this.decorar()
    this.montarPoca()
    this.criarPersonagens()
    this.criarBalao()
    this.vidaAmbiente()
    this.ligarHUD()

    this.cursors = this.input.keyboard!.createCursorKeys()
    this.teclas = this.input.keyboard!.addKeys('W,A,S,D,E,SPACE')

    // toque na areia = andar até lá (só fora dos overlays/HUD)
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.estado !== 'explora') return
      this.alvo = { x: Phaser.Math.Clamp(p.worldX, WALK.x0, WALK.x1), y: Phaser.Math.Clamp(p.worldY, WALK.y0, WALK.y1) }
    })

    this.cameras.main.startFollow(this.player, true, 0.12, 0.12)

    if (QA) {
      this.estado = 'explora'
      const tI = el('telaIntro'); if (tI) tI.classList.add('hidden')
      if (QA === 'missao') {
        this.player.setPosition(1350, 600)
        this.iniciarMontagem(true)
      }
    }
  }

  // ==========================================================================
  // TEXTURAS PINTADAS POR CÓDIGO (o chão simples da style bible + reservas)
  // ==========================================================================
  pintarTexturasBase () {
    // ---- o cenário: céu + mar + areia (chão SIMPLES; os enfeites são sprites)
    const t = this.textures.createCanvas('cenario', WORLD_W, WORLD_H)!
    const g = t.getContext()

    // céu noturno
    const ceu = g.createLinearGradient(0, 0, 0, 330)
    ceu.addColorStop(0, '#050d20'); ceu.addColorStop(0.7, '#0d1f3f'); ceu.addColorStop(1, '#1b3a63')
    g.fillStyle = ceu; g.fillRect(0, 0, WORLD_W, 330)
    // estrelas fixas
    for (let i = 0; i < 130; i++) {
      const x = Math.random() * WORLD_W, y = Math.random() * 250
      g.globalAlpha = 0.25 + Math.random() * 0.6
      g.fillStyle = '#fff'; g.fillRect(x, y, Math.random() < 0.15 ? 2 : 1, Math.random() < 0.15 ? 2 : 1)
    }
    g.globalAlpha = 1
    // lua + halo
    const lua = g.createRadialGradient(700, 110, 8, 700, 110, 90)
    lua.addColorStop(0, 'rgba(255,250,220,.95)'); lua.addColorStop(0.25, 'rgba(255,245,200,.35)'); lua.addColorStop(1, 'rgba(255,245,200,0)')
    g.fillStyle = lua; g.beginPath(); g.arc(700, 110, 90, 0, 7); g.fill()
    g.fillStyle = '#fdf6d8'; g.beginPath(); g.arc(700, 110, 34, 0, 7); g.fill()
    g.fillStyle = 'rgba(210,205,170,.5)'
    g.beginPath(); g.arc(688, 102, 6, 0, 7); g.fill()
    g.beginPath(); g.arc(712, 120, 4, 0, 7); g.fill()
    // ilha distante no horizonte (silhueta baixa e suave, com uma palmeirinha)
    g.globalAlpha = 0.55; g.fillStyle = '#0b1c34'
    g.beginPath(); g.moveTo(300, 314)
    g.quadraticCurveTo(400, 286, 520, 312); g.lineTo(520, 316); g.lineTo(300, 316); g.fill()
    g.strokeStyle = '#0b1c34'; g.lineWidth = 3
    g.beginPath(); g.moveTo(430, 300); g.quadraticCurveTo(438, 288, 442, 292); g.stroke()
    g.globalAlpha = 1

    // mar
    const mar = g.createLinearGradient(0, 300, 0, 452)
    mar.addColorStop(0, '#123a66'); mar.addColorStop(0.6, '#17507f'); mar.addColorStop(1, '#1d6a94')
    g.fillStyle = mar; g.fillRect(0, 300, WORLD_W, 152)
    // brilho da lua no mar
    g.globalAlpha = 0.18; g.fillStyle = '#ffeeb0'
    for (let y = 310; y < 445; y += 8) {
      const w = 40 + Math.random() * 90
      g.fillRect(700 - w / 2 + (Math.random() * 30 - 15), y, w, 2)
    }
    g.globalAlpha = 1
    // riscos de onda
    g.strokeStyle = 'rgba(255,255,255,.10)'; g.lineWidth = 2
    for (let i = 0; i < 34; i++) {
      const x = Math.random() * WORLD_W, y = 315 + Math.random() * 120
      g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 22, y - 3, x + 46, y); g.stroke()
    }

    // ÁGUA como corpo único: preenche do alto até a linha da costa — assim a
    // ENSEADA (o mergulho do mar na praia) é o MESMO mar, não um retângulo solto.
    const corpoAgua = g.createLinearGradient(0, 300, 0, 700)
    corpoAgua.addColorStop(0, '#17507f'); corpoAgua.addColorStop(0.45, '#123a66')
    corpoAgua.addColorStop(0.7, '#0f3357'); corpoAgua.addColorStop(1, '#0a2942')
    g.fillStyle = corpoAgua
    g.beginPath(); g.moveTo(0, 300)
    for (let x = 0; x <= WORLD_W; x += 12) g.lineTo(x, this.costa(x))
    g.lineTo(WORLD_W, 300); g.closePath(); g.fill()
    // fundo mais escuro no miolo da enseada (dá profundidade)
    const fundo = g.createRadialGradient(ENSEADA.c, 560, 20, ENSEADA.c, 560, 210)
    fundo.addColorStop(0, 'rgba(6,22,40,.55)'); fundo.addColorStop(1, 'rgba(6,22,40,0)')
    g.fillStyle = fundo; g.beginPath(); g.arc(ENSEADA.c, 560, 210, 0, 7); g.fill()

    // areia (abaixo da linha da costa)
    const areia = g.createLinearGradient(0, 440, 0, WORLD_H)
    areia.addColorStop(0, '#c9b184'); areia.addColorStop(0.5, '#bfa478'); areia.addColorStop(1, '#a98f66')
    g.fillStyle = areia
    g.beginPath(); g.moveTo(0, WORLD_H)
    for (let x = 0; x <= WORLD_W; x += 12) g.lineTo(x, this.costa(x))
    g.lineTo(WORLD_W, WORLD_H); g.closePath(); g.fill()
    // faixa de areia molhada logo abaixo da linha d'água
    g.save()
    g.beginPath(); g.moveTo(0, WORLD_H)
    for (let x = 0; x <= WORLD_W; x += 12) g.lineTo(x, this.costa(x))
    g.lineTo(WORLD_W, WORLD_H); g.closePath(); g.clip()
    g.strokeStyle = 'rgba(120,102,78,.5)'; g.lineWidth = 18
    g.beginPath(); g.moveTo(0, this.costa(0) + 9)
    for (let x = 0; x <= WORLD_W; x += 12) g.lineTo(x, this.costa(x) + 9)
    g.stroke(); g.restore()
    // espuma na costa
    g.strokeStyle = 'rgba(255,255,255,.4)'; g.lineWidth = 3
    g.beginPath(); g.moveTo(0, this.costa(0))
    for (let x = 0; x <= WORLD_W; x += 12) g.lineTo(x, this.costa(x))
    g.stroke()
    // brilho da lua na água (riscos claros perto da linha)
    g.strokeStyle = 'rgba(255,238,176,.10)'; g.lineWidth = 2
    for (let i = 0; i < 40; i++) {
      const x = Math.random() * WORLD_W, y = 320 + Math.random() * 120
      g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 20, y - 3, x + 42, y); g.stroke()
    }

    // textura da areia (pontinhos) + conchinhas — só onde há areia
    for (let i = 0; i < 700; i++) {
      const x = Math.random() * WORLD_W, y = 470 + Math.random() * (WORLD_H - 480)
      if (y < this.costa(x)) continue
      g.globalAlpha = 0.10 + Math.random() * 0.12
      g.fillStyle = Math.random() < 0.5 ? '#8a7355' : '#e8d9b8'
      g.fillRect(x, y, 2, 2)
    }
    g.globalAlpha = 1
    for (let i = 0; i < 14; i++) {
      const x = Math.random() * WORLD_W, y = 520 + Math.random() * 180
      if (y < this.costa(x) + 20) continue
      g.fillStyle = 'rgba(240,230,210,.5)'
      g.beginPath(); g.arc(x, y, 3, 3.1, 6.2); g.fill()
    }
    t.refresh()

    // ---- texturas pequenas de apoio
    this.circulo('glow', 90, 'rgba(255,190,90,', 0.5)     // luz quente (tocha)
    this.circulo('glowFrio', 60, 'rgba(160,220,255,', 0.35)
    this.circulo('vaga', 10, 'rgba(190,255,140,', 0.9)     // vagalume
    this.circulo('puff', 16, 'rgba(215,195,160,', 0.55)    // poeirinha
    this.circulo('gota', 8, 'rgba(210,235,255,', 0.9)      // splash
    this.circulo('faisca', 10, 'rgba(255,225,120,', 0.95)  // brilho do tesouro

    // sombra oval
    const so = this.textures.createCanvas('sombra', 64, 24)!
    const gs = so.getContext()
    const grd = gs.createRadialGradient(32, 12, 2, 32, 12, 30)
    grd.addColorStop(0, 'rgba(10,12,20,.42)'); grd.addColorStop(1, 'rgba(10,12,20,0)')
    gs.fillStyle = grd; gs.beginPath(); gs.ellipse(32, 12, 30, 11, 0, 0, 7); gs.fill()
    so.refresh()

    // espuma da maré (banda animada)
    const es = this.textures.createCanvas('espuma', 220, 10)!
    const ge = es.getContext()
    ge.strokeStyle = 'rgba(255,255,255,.7)'; ge.lineWidth = 3
    ge.beginPath(); ge.moveTo(0, 6)
    for (let x = 0; x <= 220; x += 12) ge.quadraticCurveTo(x + 6, x % 24 ? 2 : 8, x + 12, 6)
    ge.stroke()
    es.refresh()

    // o Verso (o mascote da criança) — corpo paramétrico pintado por código
    this.pintarVerso('verso', '#8fd4ff')
    // marcador "toque aqui" da montagem
    const mk = this.textures.createCanvas('marcaCel', 80, 80)!
    const gm = mk.getContext()
    gm.strokeStyle = 'rgba(140,220,255,.5)'; gm.lineWidth = 3
    this.rr(gm, 6, 6, 68, 68, 16); gm.stroke()
    mk.refresh()
  }

  // a linha da costa: senos suaves + a ENSEADA (o mar mergulha na praia)
  costa (x: number) {
    let t = Math.min((x - ENSEADA.e0) / ENSEADA.borda, (ENSEADA.e1 - x) / ENSEADA.borda)
    t = Math.max(0, Math.min(1, t))
    const s = t * t * (3 - 2 * t)
    return 452 + Math.sin(x / 210) * 12 + Math.sin(x / 57) * 5 + ENSEADA.prof * s
  }

  rr (g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
    g.beginPath()
    g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r)
    g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath()
  }

  circulo (nome: string, raio: number, corBase: string, alfa: number) {
    const d = raio * 2
    const t = this.textures.createCanvas(nome, d, d)!
    const g = t.getContext()
    const grd = g.createRadialGradient(raio, raio, 1, raio, raio, raio)
    grd.addColorStop(0, corBase + alfa + ')'); grd.addColorStop(1, corBase + '0)')
    g.fillStyle = grd; g.fillRect(0, 0, d, d)
    t.refresh()
  }

  pintarVerso (chave: string, cor: string) {
    const t = this.textures.createCanvas(chave, 76, 84)!
    const g = t.getContext()
    // orelhas (tipo gato)
    g.fillStyle = cor
    g.beginPath(); g.moveTo(16, 26); g.lineTo(24, 2); g.lineTo(34, 22); g.fill()
    g.beginPath(); g.moveTo(60, 26); g.lineTo(52, 2); g.lineTo(42, 22); g.fill()
    // corpo
    const grd = g.createRadialGradient(38, 40, 6, 38, 48, 40)
    grd.addColorStop(0, '#ffffff'); grd.addColorStop(0.25, cor); grd.addColorStop(1, this.escurecer(cor, 0.55))
    g.fillStyle = grd
    g.beginPath(); g.ellipse(38, 48, 30, 33, 0, 0, 7); g.fill()
    // barriga
    g.fillStyle = 'rgba(255,255,255,.75)'
    g.beginPath(); g.ellipse(38, 58, 16, 17, 0, 0, 7); g.fill()
    // olhos + brilho
    g.fillStyle = '#1c2340'
    g.beginPath(); g.arc(28, 42, 5.5, 0, 7); g.fill()
    g.beginPath(); g.arc(48, 42, 5.5, 0, 7); g.fill()
    g.fillStyle = '#fff'
    g.beginPath(); g.arc(30, 40, 2, 0, 7); g.fill()
    g.beginPath(); g.arc(50, 40, 2, 0, 7); g.fill()
    // bochechas + sorriso
    g.fillStyle = 'rgba(255,150,160,.55)'
    g.beginPath(); g.arc(21, 50, 4, 0, 7); g.fill()
    g.beginPath(); g.arc(55, 50, 4, 0, 7); g.fill()
    g.strokeStyle = '#1c2340'; g.lineWidth = 2.4
    g.beginPath(); g.arc(38, 48, 9, 0.45, 2.7); g.stroke()
    t.refresh()
  }

  escurecer (hex: string, f: number) {
    const n = parseInt(hex.slice(1), 16)
    const r = Math.floor(((n >> 16) & 255) * f), g2 = Math.floor(((n >> 8) & 255) * f), b = Math.floor((n & 255) * f)
    return 'rgb(' + r + ',' + g2 + ',' + b + ')'
  }

  // reserva pintada para asset de IA que não carregou (o mundo nunca quebra)
  garantirReservas () {
    const faltas: { [k: string]: () => void } = {
      palmeira: () => this.reservaPalmeira(),
      tocha: () => this.reservaTocha(),
      bau_fechado: () => this.reservaBau('bau_fechado', false),
      bau_aberto: () => this.reservaBau('bau_aberto', true),
      louro: () => this.reservaLouro(),
      chico: () => this.reservaChico(),
      pedra: () => this.reservaPedra(),
      rocha: () => this.reservaRocha(),
      capim: () => this.reservaCapim()
    }
    for (const k of Object.keys(faltas)) if (!this.textures.exists(k)) faltas[k]()
  }

  reservaPalmeira () {
    const t = this.textures.createCanvas('palmeira', 140, 190)!
    const g = t.getContext()
    g.strokeStyle = '#6b4f35'; g.lineWidth = 12; g.lineCap = 'round'
    g.beginPath(); g.moveTo(62, 186); g.quadraticCurveTo(78, 110, 66, 46); g.stroke()
    g.fillStyle = '#2f7d4f'
    for (let i = 0; i < 6; i++) {
      const a = -0.5 + i * 0.62
      g.save(); g.translate(66, 44); g.rotate(a)
      g.beginPath(); g.ellipse(34, 0, 38, 12, 0, 0, 7); g.fill(); g.restore()
    }
    t.refresh()
  }

  reservaTocha () {
    const t = this.textures.createCanvas('tocha', 44, 120)!
    const g = t.getContext()
    g.fillStyle = '#6b4f35'; g.fillRect(18, 34, 8, 84)
    g.fillStyle = '#8a6a45'; g.fillRect(14, 30, 16, 10)
    const f = g.createRadialGradient(22, 20, 2, 22, 20, 18)
    f.addColorStop(0, '#fff3b0'); f.addColorStop(0.5, '#ffb440'); f.addColorStop(1, 'rgba(255,110,40,0)')
    g.fillStyle = f; g.beginPath(); g.ellipse(22, 18, 13, 18, 0, 0, 7); g.fill()
    t.refresh()
  }

  reservaBau (chave: string, aberto: boolean) {
    const t = this.textures.createCanvas(chave, 84, 66)!
    const g = t.getContext()
    g.fillStyle = '#7a4d28'; this.rr(g, 8, 26, 68, 34, 8); g.fill()
    g.fillStyle = '#8f5c31'; this.rr(g, 8, aberto ? 4 : 14, 68, 18, 8); g.fill()
    g.fillStyle = '#d9a23c'
    g.fillRect(8, 32, 68, 5); g.fillRect(38, 26, 8, 34)
    if (aberto) {
      const br = g.createRadialGradient(42, 26, 2, 42, 26, 26)
      br.addColorStop(0, 'rgba(255,235,140,.95)'); br.addColorStop(1, 'rgba(255,235,140,0)')
      g.fillStyle = br; g.beginPath(); g.arc(42, 26, 26, 0, 7); g.fill()
    }
    t.refresh()
  }

  reservaLouro () {
    const t = this.textures.createCanvas('louro', 64, 70)!
    const g = t.getContext()
    g.fillStyle = '#2e9c5b'
    g.beginPath(); g.ellipse(32, 38, 18, 24, 0, 0, 7); g.fill()
    g.fillStyle = '#ffd25a'
    g.beginPath(); g.ellipse(32, 48, 10, 13, 0, 0, 7); g.fill()
    g.fillStyle = '#e2453c'
    g.beginPath(); g.moveTo(30, 58); g.quadraticCurveTo(20, 70, 34, 68); g.fill()
    g.fillStyle = '#f0a020'
    g.beginPath(); g.moveTo(18, 30); g.quadraticCurveTo(8, 34, 18, 40); g.fill()
    g.fillStyle = '#1c2340'; g.beginPath(); g.arc(24, 28, 3.4, 0, 7); g.fill()
    g.fillStyle = '#fff'; g.beginPath(); g.arc(25, 27, 1.2, 0, 7); g.fill()
    t.refresh()
  }

  reservaChico () {
    const t = this.textures.createCanvas('chico', 56, 42)!
    const g = t.getContext()
    g.fillStyle = '#e2703a'
    g.beginPath(); g.ellipse(28, 26, 17, 12, 0, 0, 7); g.fill()
    g.beginPath(); g.arc(10, 16, 6, 0, 7); g.fill()
    g.beginPath(); g.arc(46, 16, 6, 0, 7); g.fill()
    g.strokeStyle = '#e2703a'; g.lineWidth = 3
    g.beginPath(); g.moveTo(14, 20); g.lineTo(20, 26); g.stroke()
    g.beginPath(); g.moveTo(42, 20); g.lineTo(36, 26); g.stroke()
    g.fillStyle = '#fff'; g.beginPath(); g.arc(22, 14, 5, 0, 7); g.fill()
    g.beginPath(); g.arc(34, 14, 5, 0, 7); g.fill()
    g.fillStyle = '#1c2340'; g.beginPath(); g.arc(23, 15, 2.4, 0, 7); g.fill()
    g.beginPath(); g.arc(35, 15, 2.4, 0, 7); g.fill()
    t.refresh()
  }

  reservaPedra () {
    const t = this.textures.createCanvas('pedra', 78, 52)!
    const g = t.getContext()
    const grd = g.createRadialGradient(39, 22, 4, 39, 26, 38)
    grd.addColorStop(0, '#b9c0c9'); grd.addColorStop(1, '#6f7884')
    g.fillStyle = grd
    g.beginPath(); g.ellipse(39, 26, 36, 22, 0, 0, 7); g.fill()
    g.fillStyle = 'rgba(255,255,255,.25)'
    g.beginPath(); g.ellipse(32, 18, 16, 8, 0, 0, 7); g.fill()
    t.refresh()
  }

  reservaRocha () {
    const t = this.textures.createCanvas('rocha', 96, 66)!
    const g = t.getContext()
    g.fillStyle = '#5d6672'
    g.beginPath(); g.moveTo(8, 60); g.lineTo(20, 22); g.lineTo(46, 10); g.lineTo(76, 26); g.lineTo(90, 60); g.fill()
    g.fillStyle = 'rgba(255,255,255,.12)'
    g.beginPath(); g.moveTo(24, 24); g.lineTo(46, 14); g.lineTo(56, 24); g.lineTo(30, 34); g.fill()
    t.refresh()
  }

  reservaCapim () {
    const t = this.textures.createCanvas('capim', 52, 42)!
    const g = t.getContext()
    g.strokeStyle = '#3f7d4a'; g.lineWidth = 3; g.lineCap = 'round'
    for (let i = 0; i < 7; i++) {
      const x = 8 + i * 6
      g.beginPath(); g.moveTo(x, 40); g.quadraticCurveTo(x + (i % 2 ? 6 : -6), 18, x + (i % 2 ? 10 : -8), 6); g.stroke()
    }
    t.refresh()
  }

  // ==========================================================================
  // DECORAÇÃO — assets colocados com lógica (e com VIDA)
  // ==========================================================================
  colocar (chave: string, x: number, y: number, alt: number, flip = false) {
    const im = this.add.image(x, y, chave).setOrigin(0.5, 1)
    const esc = alt / im.height
    im.setScale(esc).setDepth(y).setFlipX(flip)
    return im
  }

  decorar () {
    // palmeiras (balançam com o vento — origem no pé)
    const palmas = [
      this.colocar('palmeira', 350, 512, 216),
      this.colocar('palmeira', 905, 496, 180, true),
      this.colocar('palmeira', 1445, 505, 205)
    ]
    for (let i = 0; i < palmas.length; i++) {
      this.tweens.add({
        targets: palmas[i], angle: { from: -1.6, to: 1.6 },
        duration: 2800 + i * 420, yoyo: true, repeat: -1, ease: 'Sine.easeInOut'
      })
    }

    // rochas, capim, poleiro do Louro
    this.colocar('rocha', 680, 622, 66)
    this.colocar('rocha', 1180, 500, 52, true)
    this.colocar('rocha', 2290, 640, 74)
    const capins = [[240, 648], [760, 690], [1290, 660], [1660, 700], [2200, 680], [520, 700]]
    for (const c of capins) {
      const cp = this.colocar('capim', c[0], c[1], 38, Math.random() < 0.5)
      this.tweens.add({ targets: cp, angle: { from: -2.5, to: 2.5 }, duration: 1900 + Math.random() * 900, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    }

    // tochas com luz VIVA (glow pulsando — contexto: acampamento na praia)
    for (const p of [[540, 528], [1560, 512]]) {
      this.colocar('tocha', p[0], p[1], 118)
      const gl = this.add.image(p[0], p[1] - 96, 'glow').setBlendMode(Phaser.BlendModes.ADD).setDepth(p[1] + 1)
      this.tweens.add({ targets: gl, alpha: { from: 0.55, to: 1 }, scale: { from: 0.85, to: 1.12 }, duration: 260, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    }

    // espuma da maré (bandas que vão e voltam na costa)
    for (let x = 110; x < WORLD_W; x += 300) {
      const e = this.add.image(x, 452 + Math.sin(x / 210) * 12, 'espuma').setDepth(2).setAlpha(0.5)
      this.tweens.add({
        targets: e, y: '+=10', alpha: { from: 0.55, to: 0.1 },
        duration: 2100 + (x % 700), yoyo: true, repeat: -1, ease: 'Sine.easeInOut'
      })
    }

    // vagalumes vagando perto da vegetação
    for (let i = 0; i < 9; i++) {
      const x = 200 + Math.random() * 2000, y = 520 + Math.random() * 160
      const v = this.add.image(x, y, 'vaga').setDepth(9000).setAlpha(0)
      this.tweens.add({ targets: v, alpha: { from: 0.1, to: 0.85 }, duration: 900 + Math.random() * 900, yoyo: true, repeat: -1 })
      this.tweens.add({ targets: v, x: x + (Math.random() * 120 - 60), y: y + (Math.random() * 50 - 25), duration: 3200 + Math.random() * 2600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    }
  }

  // a poça: pedras da grade + baú na chegada
  montarPoca () {
    for (const p of PEDRAS) {
      const x = this.celX(p[0]), y = this.celY(p[1])
      const im = this.add.image(x, y + 14, 'pedra').setOrigin(0.5, 0.72)
      im.setScale(62 / im.width).setDepth(y - 40)
    }
    const bx = this.celX(CHEGADA.c), by = this.celY(CHEGADA.r)
    this.bau = this.colocar('bau_fechado', bx, by + 6, 62)
    this.bau.setDepth(by + 6)
    // brilho chamando atenção no baú (o problema é VISÍVEL no mundo)
    const gb = this.add.image(bx, by - 30, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(by + 7)
    this.tweens.add({ targets: gb, alpha: { from: 0.25, to: 0.8 }, scale: { from: 0.8, to: 1.25 }, duration: 1100, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
  }

  celX (c: number) { return POCA.x0 + c * POCA.cell + POCA.cell / 2 }
  celY (r: number) { return POCA.y0 + r * POCA.cell + POCA.cell / 2 }
  ehPedra (c: number, r: number) { return PEDRAS.some(p => p[0] === c && p[1] === r) }

  criarPersonagens () {
    // o Verso (a criança)
    this.sombraP = this.add.image(180, 600, 'sombra').setDepth(1)
    this.player = this.add.image(180, 596, 'verso').setOrigin(0.5, 1)
    this.player.setScale(72 / this.player.height)

    // Louro numa rocha na praia, à ESQUERDA da enseada (contexto: vigia o baú)
    const rL = this.colocar('rocha', 1500, 592, 70)
    this.add.image(1500, 566, 'sombra').setDepth(rL.depth + 1).setScale(0.6)
    this.louro = this.colocar('louro', 1500, 548, 58, true)
    this.louro.setDepth(rL.depth + 2)
    this.tweens.add({ targets: this.louro, y: '-=5', duration: 1500, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    this.hintLouro = this.add.text(1500, 470, '!', {
      fontFamily: 'Arial Black, Arial', fontSize: '30px', color: '#ffd25a', stroke: '#3a2a00', strokeThickness: 5
    }).setOrigin(0.5).setDepth(9500)
    this.tweens.add({ targets: this.hintLouro, y: '-=10', duration: 520, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })

    // Chico, o caranguejo (na areia, ao lado da poça)
    this.sombraC = this.add.image(this.celX(CHICO_INICIO.c), this.celY(CHICO_INICIO.r) + 16, 'sombra').setDepth(1).setScale(0.7)
    this.chico = this.add.image(this.celX(CHICO_INICIO.c), this.celY(CHICO_INICIO.r) + 10, 'chico').setOrigin(0.5, 1)
    this.chico.setScale(44 / this.chico.height).setDepth(this.chico.y)
    this.tweens.add({ targets: this.chico, angle: { from: -4, to: 4 }, duration: 800, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
  }

  // ==========================================================================
  // BALÃO RPG — plaquinha de nome + typewriter + ▼ (nunca cobre o rosto)
  // ==========================================================================
  criarBalao () {
    const bg = this.add.graphics()
    bg.fillStyle(0xffffff, 0.97); bg.lineStyle(3, 0x22314f, 1)
    bg.fillRoundedRect(0, 0, 430, 118, 16); bg.strokeRoundedRect(0, 0, 430, 118, 16)
    bg.fillStyle(0x22314f, 1)
    bg.fillTriangle(200, 118, 230, 118, 215, 138)
    this.balaoPlaca = this.add.graphics()
    this.balaoNome = this.add.text(16, -12, '', { fontFamily: 'Arial Black, Arial', fontSize: '15px', color: '#ffffff' }).setPadding(8, 3, 8, 3)
    this.balaoTxt = this.add.text(16, 14, '', {
      fontFamily: 'Arial', fontSize: '17px', color: '#22314f', wordWrap: { width: 398 }, lineSpacing: 4
    })
    const seta = this.add.text(400, 88, '▼', { fontFamily: 'Arial', fontSize: '15px', color: '#5a7bbf' })
    this.tweens.add({ targets: seta, y: '+=5', duration: 460, yoyo: true, repeat: -1 })
    this.balao = this.add.container(0, 0, [bg, this.balaoPlaca, this.balaoNome, this.balaoTxt, seta])
    this.balao.setDepth(9800).setVisible(false)
  }

  posicionarBalao () {
    if (!this.balao.visible || !this.balaoAlvo) return
    const cam = this.cameras.main
    let x = this.balaoAlvo.x - 215
    let y = this.balaoAlvo.y - this.balaoAlvo.displayHeight - 160
    x = Phaser.Math.Clamp(x, cam.scrollX + 10, cam.scrollX + VW - 440)
    y = Phaser.Math.Clamp(y, cam.scrollY + 10, cam.scrollY + VH - 260)
    this.balao.setPosition(x, y)
  }

  // fala UMA fala: balão + MP3 (Antonio/Donato); se o áudio faltar, avança por tempo
  falar (id: string, aoTerminar?: () => void) {
    const f = FALAS[id]; if (!f) { if (aoTerminar) aoTerminar(); return }
    this.ultimaFala = id
    this.balaoAlvo = (f.quem === 'Louro') ? this.louro : this.player
    this.balao.setVisible(true)
    this.balaoNome.setText(f.quem)
    this.balaoNome.setBackgroundColor(f.cor)
    this.balaoTxt.setText('')

    // typewriter
    if (this.typeTimer) this.typeTimer.remove()
    let i = 0
    this.typeTimer = this.time.addEvent({
      delay: 26, loop: true,
      callback: () => {
        i++
        this.balaoTxt.setText(f.texto.slice(0, i))
        if (i >= f.texto.length && this.typeTimer) this.typeTimer.remove()
      }
    })

    const fim = () => { if (aoTerminar) this.time.delayedCall(350, aoTerminar) }
    if (!QA && this.audioOk[id]) {
      const s = this.sound.add(id)
      s.once('complete', fim)
      s.play()
    } else {
      this.time.delayedCall(1200 + f.texto.length * 42, fim)
    }
  }

  dialogo (ids: string[], aoTerminar?: () => void) {
    this.estado = 'dialogo'
    const proximo = (n: number) => {
      if (n >= ids.length) {
        this.balao.setVisible(false)
        if (aoTerminar) aoTerminar(); else this.estado = 'explora'
        return
      }
      this.falar(ids[n], () => proximo(n + 1))
    }
    proximo(0)
  }

  // ==========================================================================
  // SOM AMBIENTE (Web Audio — efeitos; a VOZ é sempre MP3 por API)
  // ==========================================================================
  vidaAmbiente () { /* ligado no 1º gesto, em ligarAmbiente() */ }

  ligarAmbiente () {
    if (this.ambienteLigado || QA) return
    this.ambienteLigado = true
    try {
      const ctx: AudioContext = (this.sound as any).context
      if (!ctx) return
      // mar: ruído filtrado com maré subindo/descendo
      const dur = 2.2, sr = ctx.sampleRate
      const buf = ctx.createBuffer(1, sr * dur, sr)
      const d = buf.getChannelData(0)
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * 0.35
      const src = ctx.createBufferSource(); src.buffer = buf; src.loop = true
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 420
      const ga = ctx.createGain(); ga.gain.value = 0.05
      src.connect(lp); lp.connect(ga); ga.connect(ctx.destination); src.start()
      const lfo = ctx.createOscillator(); lfo.frequency.value = 0.14
      const lfoG = ctx.createGain(); lfoG.gain.value = 0.028
      lfo.connect(lfoG); lfoG.connect(ga.gain); lfo.start()
      // grilos: chirps curtos de vez em quando
      const grilo = () => {
        try {
          const o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = 4200 + Math.random() * 600
          const g2 = ctx.createGain(); g2.gain.value = 0
          o.connect(g2); g2.connect(ctx.destination); o.start()
          const t0 = ctx.currentTime
          for (let k = 0; k < 3; k++) {
            g2.gain.setValueAtTime(0.012, t0 + k * 0.09)
            g2.gain.exponentialRampToValueAtTime(0.0001, t0 + k * 0.09 + 0.05)
          }
          o.stop(t0 + 0.4)
        } catch (e) {}
        this.time.delayedCall(2500 + Math.random() * 4000, grilo)
      }
      this.time.delayedCall(1800, grilo)
    } catch (e) { /* PC sem WebAudio: mundo segue mudo, nunca quebra */ }
  }

  som (tipo: string) {
    if (QA) return
    try {
      const ctx: AudioContext = (this.sound as any).context
      if (!ctx) return
      const t0 = ctx.currentTime
      if (tipo === 'splash') {
        const buf = ctx.createBuffer(1, ctx.sampleRate * 0.3, ctx.sampleRate)
        const d = buf.getChannelData(0)
        for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length)
        const s = ctx.createBufferSource(); s.buffer = buf
        const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 900
        const g = ctx.createGain(); g.gain.value = 0.25
        s.connect(f); f.connect(g); g.connect(ctx.destination); s.start()
      } else if (tipo === 'passo') {
        const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = 300
        const g = ctx.createGain(); g.gain.value = 0.05
        o.connect(g); g.connect(ctx.destination); o.start()
        o.frequency.exponentialRampToValueAtTime(190, t0 + 0.09)
        g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.1); o.stop(t0 + 0.12)
      } else if (tipo === 'tap') {
        const o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = 660
        const g = ctx.createGain(); g.gain.value = 0.06
        o.connect(g); g.connect(ctx.destination); o.start()
        g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.12); o.stop(t0 + 0.14)
      } else if (tipo === 'vitoria') {
        const notas = [523, 659, 784, 1047]
        for (let i = 0; i < notas.length; i++) {
          const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = notas[i]
          const g = ctx.createGain(); g.gain.value = 0
          o.connect(g); g.connect(ctx.destination); o.start(t0 + i * 0.14)
          g.gain.setValueAtTime(0.09, t0 + i * 0.14)
          g.gain.exponentialRampToValueAtTime(0.001, t0 + i * 0.14 + 0.5)
          o.stop(t0 + i * 0.14 + 0.55)
        }
      }
    } catch (e) {}
  }

  // ==========================================================================
  // HUD (DOM) — intro, setas da montagem, Ouvir
  // ==========================================================================
  ligarHUD () {
    const bC = el('btnComecar')
    if (bC) bC.onclick = () => {
      const tI = el('telaIntro'); if (tI) tI.classList.add('hidden')
      this.ligarAmbiente()
      this.estado = 'dialogo'
      this.time.delayedCall(400, () => this.dialogo(['n_bemvindo']))
    }
    const bO = el('btnOuvir')
    if (bO) bO.onclick = () => {
      if (this.ultimaFala && this.estado !== 'executa') this.falar(this.ultimaFala)
    }
    const setas = document.querySelectorAll('.seta')
    setas.forEach((b: any) => {
      b.onclick = () => {
        if (this.estado !== 'montar' || this.passos.length >= MAX_PASSOS) return
        this.som('tap')
        this.passos.push(b.dataset.dir)
        this.desenharPassos()
      }
    })
    const bJ = el('btnJogar'); if (bJ) bJ.onclick = () => this.executar()
    const bL = el('btnLimpar')
    if (bL) bL.onclick = () => { if (this.estado === 'montar') { this.passos = []; this.desenharPassos() } }
    const bD = el('btnDeNovo')
    if (bD) bD.onclick = () => {
      const tW = el('telaWin'); if (tW) tW.classList.add('hidden')
      this.estado = 'explora'
    }
  }

  desenharPassos () {
    const box = el('passos'); if (!box) return
    if (!this.passos.length) { box.innerHTML = '<span class="vazio">seus passos aparecem aqui…</span>'; return }
    box.innerHTML = this.passos.map((p, i) => '<span class="chip" id="chip' + i + '">' + DIRS[p].rot + '</span>').join('')
  }

  iniciarMontagem (silencioso = false) {
    this.estado = 'montar'
    if (!this.aval.inicio) this.aval.inicio = Date.now()
    const hud = el('hud'); if (hud) hud.classList.remove('hidden')
    const dica = el('dica'); if (dica) dica.innerHTML = 'Monte os passos do <b>Chico</b> até o baú 🦀 — cuidado com a água!'
    this.desenharPassos()
    this.hintLouro.setVisible(false)
    // realce suave das células (some sozinho — a criança enxerga a grade)
    if (!silencioso) {
      for (let c = 0; c < POCA.cols; c++) {
        for (let r = 0; r < POCA.rows; r++) {
          const m = this.add.image(this.celX(c), this.celY(r), 'marcaCel').setDisplaySize(66, 66).setDepth(8000).setAlpha(0)
          this.tweens.add({ targets: m, alpha: { from: 0, to: 0.7 }, duration: 500, yoyo: true, repeat: 2, delay: (c + r) * 90, onComplete: () => m.destroy() })
        }
      }
    }
  }

  // ==========================================================================
  // A MECÂNICA (reutilizável): executar a sequência — o erro RODA de verdade
  // ==========================================================================
  executar () {
    if (this.estado !== 'montar' || !this.passos.length) return
    this.estado = 'executa'
    this.aval.tentativas++
    let c = CHICO_INICIO.c, r = CHICO_INICIO.r
    const passo = (n: number) => {
      // acabou a sequência: chegou? quase?
      if (n >= this.passos.length) {
        if (c === CHEGADA.c && r === CHEGADA.r) this.vitoria()
        else this.dialogo(['l_quase'], () => { this.estado = 'montar' })
        return
      }
      const d = DIRS[this.passos[n]]
      c += d.dc; r += d.dr
      const chip = el('chip' + n); if (chip) chip.style.background = '#57e08a'
      const nx = this.celX(c), ny = this.celY(r) + 10
      this.som('passo')
      this.tweens.add({
        targets: this.chico, x: nx, y: ny, duration: 340, ease: 'Sine.easeInOut',
        onUpdate: () => { this.sombraC.setPosition(this.chico.x, this.chico.y + 6); this.chico.setDepth(this.chico.y) },
        onComplete: () => {
          const dentro = c >= 0 && r >= 0 && c < POCA.cols && r < POCA.rows
          // água: célula da grade sem pedra, OU o mar (norte), OU o fundo (direita)
          const naAgua = (dentro && !this.ehPedra(c, r)) || r < 0 || c >= POCA.cols
          if (naAgua) { this.splash(nx, ny); return }
          if (c === CHEGADA.c && r === CHEGADA.r) { this.vitoria(); return }
          // areia (c<0 ou r>=rows): seguro, mas não chega ao baú — segue a sequência
          this.time.delayedCall(140, () => passo(n + 1))
        }
      })
    }
    passo(0)
  }

  splash (x: number, y: number) {
    this.som('splash')
    for (let i = 0; i < 7; i++) {
      const gt = this.add.image(x, y - 6, 'gota').setDepth(9000)
      this.tweens.add({
        targets: gt, x: x + (Math.random() * 60 - 30), y: y - 26 - Math.random() * 26,
        alpha: 0, duration: 420, ease: 'Sine.easeOut', onComplete: () => gt.destroy()
      })
    }
    this.tweens.add({
      targets: this.chico, alpha: 0, duration: 260,
      onComplete: () => {
        // volta pro começo — o erro é consequência, a criança conserta
        this.chico.setPosition(this.celX(CHICO_INICIO.c), this.celY(CHICO_INICIO.r) + 10)
        this.sombraC.setPosition(this.chico.x, this.chico.y + 6)
        this.chico.setDepth(this.chico.y)
        this.tweens.add({ targets: this.chico, alpha: 1, duration: 300 })
        this.dialogo(['l_agua'], () => { this.estado = 'montar' })
      }
    })
  }

  vitoria () {
    this.estado = 'fim'
    this.som('vitoria')
    this.bau.setTexture('bau_aberto')
    this.bau.setScale(62 / this.bau.height)   // o desenho aberto pode ter outro tamanho
    const bx = this.bau.x, by = this.bau.y
    for (let i = 0; i < 12; i++) {
      const f = this.add.image(bx, by - 30, 'faisca').setDepth(9200)
      this.tweens.add({
        targets: f, x: bx + (Math.random() * 120 - 60), y: by - 40 - Math.random() * 90,
        alpha: 0, scale: { from: 1, to: 0.3 }, duration: 900 + Math.random() * 500,
        ease: 'Sine.easeOut', onComplete: () => f.destroy()
      })
    }
    // Chico comemora pulando
    this.tweens.add({ targets: this.chico, y: '-=14', duration: 240, yoyo: true, repeat: 3, ease: 'Sine.easeInOut' })
    this.registraAcerto()
    const hud = el('hud'); if (hud) hud.classList.add('hidden')
    this.dialogo(['l_vitoria', 'n_conceito'], () => {
      const tW = el('telaWin'); if (tW) tW.classList.remove('hidden')
      this.estado = 'fim'
    })
  }

  // avaliação invisível — semente do relatório automático do professor
  registraAcerto () {
    try {
      const reg = JSON.parse(localStorage.getItem('eduverso_aval') || '[]')
      reg.push({
        etapa: 'ilha_tesouro_mundo_vivo',
        mecanica: 'ordenar_comandos',
        objetivo: '1A2_1A3_algoritmos_sequencia_de_passos',
        tentativas: this.aval.tentativas,
        tempo_seg: Math.round((Date.now() - this.aval.inicio) / 1000),
        acerto: true,
        quando: new Date().toISOString()
      })
      localStorage.setItem('eduverso_aval', JSON.stringify(reg))
    } catch (e) {}
  }

  // ==========================================================================
  // UPDATE — andar, respirar, poeirinha, aproximação do Louro
  // ==========================================================================
  update (_t: number, dtMs: number) {
    const dt = Math.min(0.05, dtMs / 1000)
    this.resp += dt * 3
    // respiração (peito sobe e desce) — o mundo NUNCA fica parado
    const andando = this.moverPlayer(dt)
    const s = 72 / this.player.height
    this.player.setScale(s * (1 + (andando ? 0.04 : 0.018) * Math.sin(this.resp * (andando ? 3 : 1))), s * (1 - 0.022 * Math.sin(this.resp)))
    this.sombraP.setPosition(this.player.x, this.player.y + 4)
    this.player.setDepth(this.player.y)

    // poeirinha ao andar
    if (andando) {
      this.puffT -= dt
      if (this.puffT <= 0) {
        this.puffT = 0.24
        const p = this.add.image(this.player.x + (Math.random() * 14 - 7), this.player.y + 2, 'puff').setDepth(this.player.y - 1).setAlpha(0.5)
        this.tweens.add({ targets: p, y: '-=8', alpha: 0, scale: 1.5, duration: 430, onComplete: () => p.destroy() })
      }
    }

    // na montagem, as setas do teclado também adicionam passos
    if (this.estado === 'montar') {
      const mapa: any = { cima: this.cursors.up, baixo: this.cursors.down, esq: this.cursors.left, dir: this.cursors.right }
      for (const dir of Object.keys(mapa)) {
        if (Phaser.Input.Keyboard.JustDown(mapa[dir]) && this.passos.length < MAX_PASSOS) {
          this.som('tap'); this.passos.push(dir); this.desenharPassos()
        }
      }
    }

    // perto do Louro? (o problema encontra a criança no CONTEXTO)
    if (this.estado === 'explora') {
      const dist = Phaser.Math.Distance.Between(this.player.x, this.player.y, this.louro.x, this.louro.y)
      if (dist < 130) {
        if (!this.falouComLouro) {
          this.falouComLouro = true
          this.alvo = null
          this.dialogo(['l_ola', 'l_problema', 'l_como'], () => this.iniciarMontagem())
        } else if (Phaser.Input.Keyboard.JustDown(this.teclas.E) || Phaser.Input.Keyboard.JustDown(this.teclas.SPACE)) {
          this.dialogo(['l_como'], () => this.iniciarMontagem(true))
        }
      }
    }

    this.posicionarBalao()
  }

  moverPlayer (dt: number): boolean {
    // na montagem, as setas do teclado viram COMANDOS (não movem o Verso)
    if (this.estado !== 'explora') { this.alvo = null; return false }
    const v = 205 * dt
    let dx = 0, dy = 0
    const k = this.cursors, t = this.teclas
    if (k.left.isDown || t.A.isDown) dx -= 1
    if (k.right.isDown || t.D.isDown) dx += 1
    if (k.up.isDown || t.W.isDown) dy -= 1
    if (k.down.isDown || t.S.isDown) dy += 1
    if (dx || dy) this.alvo = null
    if (!dx && !dy && this.alvo) {
      const ax = this.alvo.x - this.player.x, ay = this.alvo.y - this.player.y
      const d = Math.hypot(ax, ay)
      if (d < 6) this.alvo = null
      else { dx = ax / d; dy = ay / d }
    }
    if (!dx && !dy) return false
    const n = Math.hypot(dx, dy); dx /= n; dy /= n
    let nx = Phaser.Math.Clamp(this.player.x + dx * v, WALK.x0, WALK.x1)
    let ny = Phaser.Math.Clamp(this.player.y + dy * v, WALK.y0, WALK.y1)
    // a ÁGUA bloqueia o Verso (os pés não podem passar da linha da costa):
    // só o Chico atravessa a enseada, pelas pedras! desliza no eixo livre.
    const margem = 10
    if (ny < this.costa(nx) + margem) {
      if (this.player.y >= this.costa(nx) + margem) ny = this.player.y          // trava só o vertical
      else if (this.player.y >= this.costa(this.player.x) + margem) { nx = this.player.x } // trava horizontal
      else { nx = this.player.x; ny = this.player.y }
    }
    if (dx < 0) this.player.setFlipX(true); else if (dx > 0) this.player.setFlipX(false)
    this.player.setPosition(nx, ny)
    return true
  }
}
