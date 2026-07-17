import Phaser from 'phaser'

/* ============================================================================
 * EducaVerso — Plano A · Etapa 2
 * Mecânica REUTILIZÁVEL "ordenar comandos" (o ALGORITMO) numa cena Phaser bonita
 * (praia noturna, em grade). A criança monta os passos -> o Verso anda de célula
 * em célula até o baú, desviando das poças -> conceito "algoritmo" no fim.
 * Avaliação INVISÍVEL: registra tentativas/tempo/acerto (localStorage; Firebase depois).
 * A config da mecânica é separada: a mesma mecânica vira missão no mundo OU atividade avulsa.
 * ==========================================================================*/

const VW = 1024, VH = 768

// ---- CONFIG da mecânica (reutilizável: muda contexto/grade/obstáculos) ----
const MEC = {
  id: 'ordenar_comandos',
  contexto: 'ilha_tesouro',
  objetivo: '1A2_algoritmos_sequencia_de_passos',
  cols: 6, rows: 3,
  start: { c: 0, r: 2 },
  goal: { c: 5, r: 0 },
  agua: [{ c: 2, r: 2 }, { c: 3, r: 1 }, { c: 4, r: 2 }],
  maxPassos: 12
}
const CELL = 140
const GX = (VW - MEC.cols * CELL) / 2
const GY = 210
const cx = (c: number) => GX + c * CELL + CELL / 2
const cy = (r: number) => GY + r * CELL + CELL / 2
const ehAgua = (c: number, r: number) => MEC.agua.some(a => a.c === c && a.r === r)

// ---- avaliação invisível ----
const AVAL = { inicio: 0, tentativas: 0 }
function registraAcerto() {
  const rec = { mecanica: MEC.id, contexto: MEC.contexto, objetivo: MEC.objetivo, tentativas: AVAL.tentativas, tempo_seg: AVAL.inicio ? Math.round((Date.now() - AVAL.inicio) / 1000) : 0, acerto: true }
  try {
    const arr = JSON.parse(localStorage.getItem('eduverso_aval') || '[]')
    arr.push(rec); localStorage.setItem('eduverso_aval', JSON.stringify(arr))
  } catch (e) { /* offline-safe */ }
}

// ---- som (Web Audio) ----
let AC: AudioContext | null = null
const ac = () => { if (!AC) { try { AC = new (window.AudioContext || (window as any).webkitAudioContext)() } catch (e) { /* */ } } return AC }
function beep(freq: number, dur: number, tipo: OscillatorType, vol: number) {
  const a = ac(); if (!a) return
  try { const o = a.createOscillator(), g = a.createGain(); o.type = tipo; o.frequency.value = freq; g.gain.value = vol; o.connect(g); g.connect(a.destination); const t = a.currentTime; o.start(t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.stop(t + dur) } catch (e) { /* */ }
}
const somPasso = () => beep(520, 0.09, 'square', 0.06)
const somSplash = () => { beep(180, 0.25, 'sawtooth', 0.10); setTimeout(() => beep(120, 0.3, 'sawtooth', 0.08), 60) }
const somWin = () => [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, 0.18, 'triangle', 0.10), i * 130))
const somTap = () => beep(700, 0.05, 'sine', 0.05)

// ---- voz (Web Speech) ----
function fala(t: string) { try { if (!('speechSynthesis' in window)) return; const u = new SpeechSynthesisUtterance(t); u.lang = 'pt-BR'; u.rate = 0.98; u.pitch = 1.08; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u) } catch (e) { /* */ } }

const DIRS: Record<string, { dc: number, dr: number, s: string }> = {
  cima: { dc: 0, dr: -1, s: '↑' }, baixo: { dc: 0, dr: 1, s: '↓' }, esq: { dc: -1, dr: 0, s: '←' }, dir: { dc: 1, dr: 0, s: '→' }
}

class Mission extends Phaser.Scene {
  private player!: Phaser.GameObjects.Image
  private seq: string[] = []
  private rodando = false
  private pos = { c: MEC.start.c, r: MEC.start.r }

  constructor() { super('mission') }

  preload() {
    this.pintaCenario()
    this.pintaVerso()
    this.pintaFlame()
    this.pintaGlow('vagalume', 'rgba(210,255,150,')
  }

  create() {
    this.add.image(0, 0, 'cenario').setOrigin(0)

    // chama animada nas tochas
    for (const fx of [50, 974]) {
      const fl = this.add.image(fx - 6, 636 - 52, 'flame').setDepth(20)
      this.tweens.add({ targets: fl, scaleY: 1.2, scaleX: 0.88, duration: 130, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
    }
    // vaga-lumes
    for (let i = 0; i < 9; i++) {
      const fx = 120 + Math.random() * 780, fy = 240 + Math.random() * 420
      const vl = this.add.image(fx, fy, 'vagalume').setScale(0.9).setDepth(15)
      this.tweens.add({ targets: vl, x: fx + (Math.random() * 70 - 35), y: fy + (Math.random() * 50 - 25), alpha: 0.3, duration: 1500 + Math.random() * 1500, yoyo: true, repeat: -1, ease: 'Sine.inOut' })
    }

    // personagem no início
    this.player = this.add.image(cx(MEC.start.c), cy(MEC.start.r), 'verso').setDepth(30)
    this.eventos()
  }

  update() {
    if (this.player) { const t = this.time.now * 0.004; this.player.setScale(1, 1 + Math.sin(t) * 0.03) }
  }

  /* ---------- CENÁRIO (canvas -> textura) ---------- */
  private pintaCenario() {
    const tex = this.textures.createCanvas('cenario', VW, VH)!
    const x = tex.getContext() as CanvasRenderingContext2D
    let sky = x.createLinearGradient(0, 0, 0, VH * 0.4); sky.addColorStop(0, '#0a1030'); sky.addColorStop(1, '#1b3a63')
    x.fillStyle = sky; x.fillRect(0, 0, VW, VH)
    let s = 7; const rr = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff }
    for (let i = 0; i < 130; i++) { x.globalAlpha = 0.3 + rr() * 0.6; x.fillStyle = '#eaf2ff'; x.beginPath(); x.arc(rr() * VW, rr() * VH * 0.32, rr() * 1.4 + 0.3, 0, 7); x.fill() }
    x.globalAlpha = 1
    const mx = 860, my = 90
    let mg = x.createRadialGradient(mx, my, 8, mx, my, 150); mg.addColorStop(0, 'rgba(230,240,255,.5)'); mg.addColorStop(1, 'rgba(230,240,255,0)')
    x.fillStyle = mg; x.beginPath(); x.arc(mx, my, 150, 0, 7); x.fill()
    x.fillStyle = '#f2f6ff'; x.beginPath(); x.arc(mx, my, 36, 0, 7); x.fill()
    const seaY = VH * 0.28
    let sea = x.createLinearGradient(0, seaY, 0, seaY + 80); sea.addColorStop(0, '#12365f'); sea.addColorStop(1, '#0c2444')
    x.fillStyle = sea; x.fillRect(0, seaY, VW, 90)
    let sand = x.createLinearGradient(0, seaY + 40, 0, VH); sand.addColorStop(0, '#2f2a24'); sand.addColorStop(1, '#201d18')
    x.fillStyle = sand; x.fillRect(0, seaY + 30, VW, VH)
    x.strokeStyle = 'rgba(200,225,255,.28)'; x.lineWidth = 3; x.beginPath(); x.moveTo(0, seaY + 40); x.lineTo(VW, seaY + 40); x.stroke()

    const luz = (px: number, py: number, rad: number, cor: string, al: number) => { x.save(); x.globalCompositeOperation = 'lighter'; let g = x.createRadialGradient(px, py, 4, px, py, rad); g.addColorStop(0, cor); g.addColorStop(1, 'rgba(0,0,0,0)'); x.globalAlpha = al; x.fillStyle = g; x.beginPath(); x.arc(px, py, rad, 0, 7); x.fill(); x.restore() }
    luz(50, 640, 240, 'rgba(255,170,70,.5)', 0.55); luz(974, 640, 240, 'rgba(255,170,70,.5)', 0.55)

    // pegadas (onde dá pra pisar) + poças
    for (let c = 0; c < MEC.cols; c++) for (let r = 0; r < MEC.rows; r++) {
      const px = cx(c), py = cy(r)
      if (ehAgua(c, r)) {
        let wg = x.createRadialGradient(px, py, 3, px, py, 52); wg.addColorStop(0, '#2f6f9e'); wg.addColorStop(1, '#173f60')
        x.fillStyle = wg; x.beginPath(); x.ellipse(px, py, 52, 30, 0, 0, 7); x.fill()
        x.strokeStyle = 'rgba(200,230,255,.3)'; x.lineWidth = 2; x.beginPath(); x.ellipse(px, py, 52, 30, 0, 0, 7); x.stroke()
      } else {
        x.fillStyle = 'rgba(255,240,210,.10)'; x.beginPath(); x.ellipse(px, py, 26, 12, 0, 0, 7); x.fill()
      }
    }
    // baú (goal)
    const bx = cx(MEC.goal.c), by = cy(MEC.goal.r)
    let glow = x.createRadialGradient(bx, by, 4, bx, by, 70); glow.addColorStop(0, 'rgba(255,200,90,.55)'); glow.addColorStop(1, 'rgba(255,200,90,0)')
    x.fillStyle = glow; x.beginPath(); x.arc(bx, by, 70, 0, 7); x.fill()
    x.fillStyle = '#7a4a1e'; this.rrect(x, bx - 34, by - 6, 68, 38, 8); x.fill()
    x.fillStyle = '#9a6a2e'; x.beginPath(); x.moveTo(bx - 34, by - 6); x.quadraticCurveTo(bx, by - 36, bx + 34, by - 6); x.fill()
    x.fillStyle = '#ffd25a'; x.fillRect(bx - 5, by - 2, 10, 16)
    x.strokeStyle = '#5a340f'; x.lineWidth = 3; x.beginPath(); x.moveTo(bx - 34, by + 8); x.lineTo(bx + 34, by + 8); x.stroke()

    // palmeira (canto sup. esq.) + tochas (bordas)
    this.palma(x, 105, 360)
    this.tochaBase(x, 50, 640); this.tochaBase(x, 974, 640)
    tex.refresh()
  }
  private rrect(x: CanvasRenderingContext2D, px: number, py: number, w: number, h: number, r: number) { x.beginPath(); x.moveTo(px + r, py); x.arcTo(px + w, py, px + w, py + h, r); x.arcTo(px + w, py + h, px, py + h, r); x.arcTo(px, py + h, px, py, r); x.arcTo(px, py, px + w, py, r); x.closePath() }
  private palma(x: CanvasRenderingContext2D, bx: number, by: number) {
    x.fillStyle = '#2a2320'; x.beginPath(); x.moveTo(bx - 9, by); x.quadraticCurveTo(bx - 22, by - 130, bx + 10, by - 205); x.lineTo(bx + 26, by - 203); x.quadraticCurveTo(bx - 3, by - 130, bx + 10, by); x.closePath(); x.fill()
    const tx = bx + 16, ty = by - 207, ang = [-2.7, -1.8, -0.8, 0.2, 1.2, 2.2]
    for (const a of ang) { const ex = tx + Math.cos(a) * 128, ey = ty + Math.sin(a) * 78 + 8, m1x = tx + Math.cos(a) * 64, m1y = ty + Math.sin(a) * 32 - 28
      x.fillStyle = '#233016'; x.beginPath(); x.moveTo(tx, ty); x.quadraticCurveTo(m1x, m1y, ex, ey); x.quadraticCurveTo(m1x + 8, m1y + 16, tx + 6, ty + 6); x.closePath(); x.fill()
      x.strokeStyle = 'rgba(150,180,220,.4)'; x.lineWidth = 2; x.beginPath(); x.moveTo(tx, ty); x.quadraticCurveTo(m1x, m1y, ex, ey); x.stroke() }
    x.fillStyle = '#3a2a1e'; for (let c = 0; c < 3; c++) { x.beginPath(); x.arc(tx - 6 + c * 7, ty + 8, 5, 0, 7); x.fill() }
  }
  private tochaBase(x: CanvasRenderingContext2D, lx: number, ly: number) {
    x.strokeStyle = '#3a2a1c'; x.lineWidth = 9; x.lineCap = 'round'; x.beginPath(); x.moveTo(lx, ly + 44); x.lineTo(lx - 6, ly - 48); x.stroke()
  }
  private pintaVerso() {
    const tex = this.textures.createCanvas('verso', 68, 76)!
    const x = tex.getContext() as CanvasRenderingContext2D
    const c = '#ff9b57', b = '#ffe6cf', olho = '#20305e', px = 34, py = 34
    x.fillStyle = 'rgba(0,0,0,.28)'; x.beginPath(); x.ellipse(px, py + 34, 24, 8, 0, 0, 7); x.fill()
    x.fillStyle = c; x.beginPath(); x.moveTo(px - 20, py - 18); x.lineTo(px - 25, py - 40); x.lineTo(px - 5, py - 29); x.closePath(); x.fill()
    x.beginPath(); x.moveTo(px + 20, py - 18); x.lineTo(px + 25, py - 40); x.lineTo(px + 5, py - 29); x.closePath(); x.fill()
    x.fillStyle = c; x.beginPath(); x.ellipse(px, py, 27, 31, 0, 0, 7); x.fill()
    x.fillStyle = b; x.beginPath(); x.ellipse(px, py + 9, 16, 16, 0, 0, 7); x.fill()
    x.fillStyle = '#fff'; x.beginPath(); x.arc(px - 9, py - 7, 6.5, 0, 7); x.arc(px + 9, py - 7, 6.5, 0, 7); x.fill()
    x.fillStyle = olho; x.beginPath(); x.arc(px - 9, py - 6, 3.2, 0, 7); x.arc(px + 9, py - 6, 3.2, 0, 7); x.fill()
    x.fillStyle = '#fff'; x.beginPath(); x.arc(px - 7, py - 8, 1.4, 0, 7); x.arc(px + 11, py - 8, 1.4, 0, 7); x.fill()
    x.fillStyle = 'rgba(255,143,176,.5)'; x.beginPath(); x.arc(px - 15, py + 3, 3, 0, 7); x.arc(px + 15, py + 3, 3, 0, 7); x.fill()
    x.strokeStyle = olho; x.lineWidth = 2; x.beginPath(); x.moveTo(px - 4, py + 5); x.quadraticCurveTo(px, py + 9, px + 4, py + 5); x.stroke()
    tex.refresh()
  }
  private pintaFlame() {
    const tex = this.textures.createCanvas('flame', 40, 60)!
    const x = tex.getContext() as CanvasRenderingContext2D
    x.save(); x.globalCompositeOperation = 'lighter'
    const ch = (w: number, h: number, col: string) => { x.fillStyle = col; x.beginPath(); x.moveTo(20, 54 - 46 - h); x.quadraticCurveTo(20 - w, 40, 20 - w * 0.4, 54); x.quadraticCurveTo(20, 48, 20 + w * 0.4, 54); x.quadraticCurveTo(20 + w, 40, 20, 54 - 46 - h); x.fill() }
    ch(15, 0, '#ff6a1f'); ch(10, 6, '#ffb02e'); ch(5, 12, '#ffe98a'); x.restore(); tex.refresh()
  }
  private pintaGlow(key: string, rgba: string) {
    const tex = this.textures.createCanvas(key, 24, 24)!
    const x = tex.getContext() as CanvasRenderingContext2D
    const g = x.createRadialGradient(12, 12, 0, 12, 12, 12); g.addColorStop(0, rgba + '0.95)'); g.addColorStop(1, rgba + '0)')
    x.fillStyle = g; x.fillRect(0, 0, 24, 24); tex.refresh()
  }

  /* ---------- HUD + mecânica ---------- */
  private $(id: string) { return document.getElementById(id)! }
  private eventos() {
    document.addEventListener('click', (ev) => {
      const el = ev.target as HTMLElement
      const d = el?.getAttribute?.('data-dir'); if (d) this.addPasso(d)
    })
    this.$('btnJogar').onclick = () => this.jogar()
    this.$('btnLimpar').onclick = () => this.limpar()
    this.$('btnOuvir').onclick = () => { ac(); this.narraIntro() }
    this.$('btnComecar').onclick = () => { ac(); this.$('telaIntro').className = 'overlay hidden'; this.narraIntro() }
    this.$('btnDeNovo').onclick = () => { this.$('telaWin').className = 'overlay hidden'; this.limpar() }
  }
  private narraIntro() { fala("Crá! O baú do tesouro ficou lá na ponta da praia. Monta os passos pro seu amiguinho chegar, e cuidado com as poças d'água!") }
  private renderPassos() {
    const box = this.$('passos')
    if (!this.seq.length) { box.innerHTML = '<span class="vazio">seus passos aparecem aqui…</span>'; return }
    box.innerHTML = this.seq.map(d => `<span class="chip">${DIRS[d].s}</span>`).join('')
  }
  private addPasso(d: string) { if (this.rodando || this.seq.length >= MEC.maxPassos) return; this.seq.push(d); somTap(); this.renderPassos() }
  private limpar() { if (this.rodando) return; this.seq = []; this.pos = { c: MEC.start.c, r: MEC.start.r }; this.player.setPosition(cx(this.pos.c), cy(this.pos.r)); this.renderPassos(); this.$('dica').innerHTML = 'Monte os passos e toque em <b>Jogar</b>. 🧭' }
  private jogar() {
    if (this.rodando || !this.seq.length) return
    this.rodando = true; AVAL.tentativas++; if (!AVAL.inicio) AVAL.inicio = Date.now()
    this.pos = { c: MEC.start.c, r: MEC.start.r }; this.player.setPosition(cx(this.pos.c), cy(this.pos.r))
    let i = 0
    const passo = () => {
      if (i >= this.seq.length) { this.fim(); return }
      const d = DIRS[this.seq[i]]; i++
      const nc = this.pos.c + d.dc, nr = this.pos.r + d.dr
      if (nc < 0 || nc >= MEC.cols || nr < 0 || nr >= MEC.rows) { this.time.delayedCall(360, passo); return }
      this.pos.c = nc; this.pos.r = nr; somPasso()
      this.tweens.add({ targets: this.player, x: cx(nc), y: cy(nr), duration: 340, ease: 'Sine.inOut' })
      if (ehAgua(nc, nr)) { this.time.delayedCall(420, () => this.splash()); return }
      this.time.delayedCall(430, passo)
    }
    passo()
  }
  private splash() { this.rodando = false; somSplash(); fala('Ops! Caiu na água. Ajusta os passos e tenta de novo.'); this.$('dica').innerHTML = "💦 Caiu na poça! Ajusta os passos e tenta de novo."; this.pos = { c: MEC.start.c, r: MEC.start.r }; this.player.setPosition(cx(this.pos.c), cy(this.pos.r)) }
  private fim() {
    if (this.pos.c === MEC.goal.c && this.pos.r === MEC.goal.r) {
      somWin(); registraAcerto(); fala('Você conseguiu! Você montou uma sequência de passos que levou seu amigo até o tesouro. Isso chama-se algoritmo!')
      this.time.delayedCall(400, () => { this.$('telaWin').className = 'overlay' })
    } else { this.rodando = false; fala('Quase! Ele parou fora do baú. Ajusta os passos.'); this.$('dica').innerHTML = 'Quase! Ele parou fora do baú. Ajusta os passos. 🙂' }
  }
}

// eslint-disable-next-line no-new
new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: '#060c18',
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, width: VW, height: VH },
  fps: { target: 30, forceSetTimeOut: true },
  render: { antialias: false, roundPixels: true, powerPreference: 'low-power', pixelArt: false },
  scene: [Mission]
})
