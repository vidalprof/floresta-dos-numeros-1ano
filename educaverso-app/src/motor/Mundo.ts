// ============================================================================
// O MONTADOR — o coração da ferramenta.
// Recebe uma AVENTURA (dados validados por Zod) e ARMA o mundo vivo:
//  - mundo amplo (câmera segue o herói), chão de IA
//  - PARADAS espalhadas (cada uma: objetos + NPCs + mecânica)
//  - personagens ANIMADOS (cartela de poses), objetos com VIDA (motor)
//  - diálogo (voz Antonio) ao chegar numa parada
//  - física (colisão) + partículas (vaga-lumes, poeira)
// Trocar de aventura = trocar os DADOS. A máquina é a mesma.
// ============================================================================
import Phaser from 'phaser'
import { Personagem } from './Personagem'
import { auditar } from './auditor'
import { abrir as abrirMecanica, temMecanica } from './mecanicas'
import type { TAventura, TObjeto } from './aventura'

const VW = 1024, VH = 768
const QA = new URLSearchParams(location.search).get('qa')
function el (id: string) { return document.getElementById(id) }

export class Mundo extends Phaser.Scene {
  av!: TAventura
  heroi!: Personagem
  corpo!: Phaser.GameObjects.Rectangle   // corpo físico dedicado (não depende da escala do sprite)
  npcs: Personagem[] = []
  obst!: Phaser.Physics.Arcade.StaticGroup
  cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  teclas!: any
  alvo: { x: number, y: number } | null = null
  estado = 'explora'
  poeira!: Phaser.GameObjects.Particles.ParticleEmitter
  falado: { [id: string]: boolean } = {}
  balao!: Phaser.GameObjects.Container
  balaoTxt!: Phaser.GameObjects.Text
  balaoNome!: Phaser.GameObjects.Text
  balaoAlvo: Phaser.GameObjects.GameObject | null = null
  typeTimer: Phaser.Time.TimerEvent | null = null
  falas: { [id: string]: { quem: string, texto: string, cor: string } } = {}
  audioOk: { [id: string]: boolean } = {}
  paradaAtiva: string | null = null

  constructor () { super('Mundo') }

  init (dados: { aventura: TAventura }) { this.av = dados.aventura }

  preload () {
    const av = this.av
    this.load.image('chao', 'img/' + av.mundo.chao + '.png')
    // objetos únicos do kit
    const objs = new Set<string>()
    for (const p of av.paradas) {
      for (const o of p.objetos) objs.add(o.asset)
      for (const o of (p.interior?.objetos || [])) objs.add(o.asset)
    }
    for (const a of objs) this.load.image(a, 'img/' + a + '.png')
    // personagens (herói + NPCs)
    Personagem.preload(this, av.heroi)
    const nomes = new Set<string>()
    for (const p of av.paradas) for (const pr of p.personagens) nomes.add(pr.nome)
    for (const n of nomes) Personagem.preload(this, n)
    // falas -> áudio
    for (const p of av.paradas) for (const f of p.falas) { this.falas[f.id] = f; if (!QA) this.load.audio(f.id, 'audio/' + f.id + '.mp3') }
    this.load.on('loaderror', (f: any) => console.warn('asset ausente:', f.key))
    this.efeitos()
  }

  create () {
    const av = this.av
    for (const id of Object.keys(this.falas)) this.audioOk[id] = this.cache.audio.exists(id)
    this.reservaChao()

    // chão amplo (repete a imagem se o mundo for maior que ela)
    const t = this.textures.get('chao').getSourceImage() as HTMLImageElement
    const cw = t.width || 1024, ch = t.height || 768
    for (let x = 0; x < av.mundo.largura; x += cw)
      for (let y = 0; y < av.mundo.altura; y += ch)
        this.add.image(x, y, 'chao').setOrigin(0, 0).setDepth(0)

    this.physics.world.setBounds(40, 40, av.mundo.largura - 80, av.mundo.altura - 80)
    this.obst = this.physics.add.staticGroup()

    // PARADAS: objetos + NPCs + marcador
    for (const p of av.paradas) {
      for (const o of p.objetos) this.colocaObjeto(o)
      for (const pr of p.personagens) {
        const np = new Personagem(this, pr.nome, pr.x, pr.y, pr.alt)
        ;(np as any)._falaChegar = pr.fala_ao_chegar
        ;(np as any)._parada = p.id
        this.npcs.push(np)
      }
      // marcador brilhante da parada (chama a criança pra lá)
      const m = this.add.image(p.x, p.y - 40, 'glowFrio').setBlendMode(Phaser.BlendModes.ADD).setDepth(9000)
      this.tweens.add({ targets: m, alpha: { from: 0.25, to: 0.7 }, scale: { from: 0.7, to: 1.3 }, duration: 1200, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' })
    }

    // HERÓI (o aluno) — animado. O CORPO físico é um retângulo DEDICADO de
    // tamanho fixo em px do mundo (não depende da escala do sprite nem do
    // squash/stretch), então a colisão bate certinho. O sprite só SEGUE o corpo.
    this.heroi = new Personagem(this, av.heroi, av.inicio.x, av.inicio.y, 96)
    this.corpo = this.add.rectangle(av.inicio.x, av.inicio.y, 40, 26).setVisible(false)
    this.physics.add.existing(this.corpo)
    const b = this.corpo.body as Phaser.Physics.Arcade.Body
    b.setCollideWorldBounds(true)
    this.physics.add.collider(this.corpo, this.obst)
    this.poeira = this.add.particles(0, 0, 'puff', { lifespan: 420, speed: { min: 4, max: 16 }, angle: { min: 200, max: 340 }, scale: { start: 0.5, end: 1.3 }, alpha: { start: 0.5, end: 0 }, emitting: false }).setDepth(640)

    // vaga-lumes pelo mundo (vida ambiente)
    this.add.particles(0, 0, 'vaga', { x: { min: 60, max: av.mundo.largura - 60 }, y: { min: 60, max: av.mundo.altura - 60 }, lifespan: 2600, frequency: 200, quantity: 1, blendMode: 'ADD', alpha: { start: 0.8, end: 0 }, scale: { start: 0.5, end: 1.1 }, speedX: { min: -12, max: 12 }, speedY: { min: -16, max: 6 }, emitting: true }).setDepth(8500)

    this.cameras.main.setBounds(0, 0, av.mundo.largura, av.mundo.altura)
    this.cameras.main.startFollow(this.heroi.sprite, true, 0.1, 0.1)

    this.criarBalao()
    this.cursors = this.input.keyboard!.createCursorKeys()
    this.teclas = this.input.keyboard!.addKeys('W,A,S,D,E,SPACE')
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { if (this.estado === 'explora') this.alvo = { x: p.worldX, y: p.worldY } })
    const bO = el('btnOuvir'); if (bO) bO.onclick = () => { /* repete última fala se houver */ }
    el('telaIntro')?.classList.add('hidden')
    el('hud')?.classList.add('hidden')

    // 🤖 AUDITOR AUTOMÁTICO — pega peça fora do lugar, coqueiro no mar, etc.
    const assets = new Set<string>(this.textures.getTextureKeys())
    const audios = new Set<string>(Object.keys(this.audioOk).filter(k => this.audioOk[k]))
    const probs = auditar(this.av, { assets, audios })
    if (probs.length) {
      const grave = probs.some(x => x.grave)
      const d = document.createElement('div')
      d.id = 'auditoria'
      d.style.cssText = 'position:fixed;left:0;bottom:0;right:0;z-index:99998;max-height:45%;overflow:auto;background:' + (grave ? '#8a1c1c' : '#8a6a1c') + ';color:#fff;font:600 13px system-ui;padding:8px 12px;'
      d.textContent = '🤖 AUDITOR (' + probs.length + '): ' + probs.map(x => (x.grave ? '⛔ ' : '⚠️ ') + x.msg).join('   •   ')
      document.body.appendChild(d)
      console.warn('AUDITOR', probs)
    }

    // QA (?mec=1): abre a mecânica da 1ª parada que tiver — headless não anda,
    // então o screenshot precisa que a gente dispare a mecânica pra provar.
    if (new URLSearchParams(location.search).has('mec')) {
      const alvo = av.paradas.find(p => p.mecanica && temMecanica(p.mecanica.id))
      if (alvo) this.time.delayedCall(400, () => this.abreMecanica(alvo.id))
    }
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
      this.physics.add.existing(bl, true)                         // corpo ESTÁTICO
      ;(bl.body as Phaser.Physics.Arcade.StaticBody).updateFromGameObject()  // sincroniza posição/tamanho
      this.obst.add(bl)
    }
  }

  // ---- efeitos base (primitivas do motor) ----
  efeitos () {
    this.circ('glow', 90, 'rgba(255,190,90,', 0.5); this.circ('glowFrio', 60, 'rgba(170,225,255,', 0.4)
    this.circ('vaga', 8, 'rgba(200,255,150,', 0.95); this.circ('puff', 14, 'rgba(225,210,180,', 0.6)
    const so = this.textures.createCanvas('sombra', 70, 26)!; const gs = so.getContext()
    const gr = gs.createRadialGradient(35, 13, 2, 35, 13, 33); gr.addColorStop(0, 'rgba(6,10,18,.5)'); gr.addColorStop(1, 'rgba(6,10,18,0)')
    gs.fillStyle = gr; gs.beginPath(); gs.ellipse(35, 13, 33, 12, 0, 0, 7); gs.fill(); so.refresh()
  }
  circ (n: string, raio: number, c: string, a: number) {
    const d = raio * 2, t = this.textures.createCanvas(n, d, d)!, g = t.getContext()
    const grd = g.createRadialGradient(raio, raio, 1, raio, raio, raio); grd.addColorStop(0, c + a + ')'); grd.addColorStop(1, c + '0)')
    g.fillStyle = grd; g.fillRect(0, 0, d, d); t.refresh()
  }
  reservaChao () {
    if (this.textures.exists('chao')) return
    const t = this.textures.createCanvas('chao', 512, 512)!; const g = t.getContext()
    g.fillStyle = '#3f6f4a'; g.fillRect(0, 0, 512, 512); t.refresh()
  }

  criarBalao () {
    const bg = this.add.graphics(); bg.fillStyle(0xffffff, 0.97); bg.lineStyle(3, 0x22314f, 1)
    bg.fillRoundedRect(0, 0, 430, 116, 16); bg.strokeRoundedRect(0, 0, 430, 116, 16); bg.fillStyle(0x22314f, 1); bg.fillTriangle(200, 116, 230, 116, 215, 136)
    this.balaoNome = this.add.text(16, -12, '', { fontFamily: 'Arial Black, Arial', fontSize: '15px', color: '#fff' }).setPadding(8, 3, 8, 3)
    this.balaoTxt = this.add.text(16, 14, '', { fontFamily: 'Arial', fontSize: '17px', color: '#22314f', wordWrap: { width: 398 }, lineSpacing: 4 })
    const rr = Math.max(2, Math.min(3, Math.round((window.devicePixelRatio || 1) * 1.5))); this.balaoTxt.setResolution(rr); this.balaoNome.setResolution(rr)
    this.balao = this.add.container(0, 0, [bg, this.balaoNome, this.balaoTxt]).setDepth(9900).setVisible(false).setScrollFactor(0)
  }
  falar (id: string, aoFim?: () => void) {
    const f = this.falas[id]; if (!f) { aoFim?.(); return }
    this.balao.setVisible(true).setPosition(VW / 2 - 215, VH - 200)
    this.balaoNome.setText(f.quem); this.balaoNome.setBackgroundColor(f.cor); this.balaoTxt.setText('')
    if (this.typeTimer) this.typeTimer.remove()
    let i = 0; this.typeTimer = this.time.addEvent({ delay: 26, loop: true, callback: () => { i++; this.balaoTxt.setText(f.texto.slice(0, i)); if (i >= f.texto.length) this.typeTimer!.remove() } })
    const fim = () => aoFim && this.time.delayedCall(400, aoFim)
    if (!QA && this.audioOk[id]) { const s = this.sound.add(id); s.once('complete', fim); s.play() } else this.time.delayedCall(1200 + f.texto.length * 42, fim)
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
      if (!dx && !dy && this.alvo) { const ax = this.alvo.x - this.corpo.x, ay = this.alvo.y - this.corpo.y, d = Math.hypot(ax, ay); if (d < 10) this.alvo = null; else { dx = ax / d; dy = ay / d } }
      if (dx || dy) { const n = Math.hypot(dx, dy); dx /= n; dy /= n; b.setVelocity(dx * v, dy * v); andando = true; if (Math.abs(dx) > Math.abs(dy)) this.heroi.setDir(dx < 0 ? 'esq' : 'dir'); else this.heroi.setDir(dy < 0 ? 'cima' : 'baixo') } else b.setVelocity(0, 0)
    } else b.setVelocity(0, 0)
    // o sprite do herói SEGUE o corpo físico (colisão certinha, visual solto)
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
          const falas = (np as any)._falaChegar as string[]
          if (falas && falas.length) this.dialogo(falas, () => this.abreMecanica(pid))
          else this.abreMecanica(pid)
        }
      }
    }
  }

  // GANCHO das mecânicas (catálogo). Instancia a mecânica da parada a partir
  // dos DADOS (id + params). A mesma máquina serve qualquer mecânica registrada.
  abreMecanica (paradaId: string) {
    const p = this.av.paradas.find(x => x.id === paradaId)
    if (!p || !p.mecanica || !temMecanica(p.mecanica.id)) {
      if (p && p.mecanica && !temMecanica(p.mecanica.id)) console.warn('mecânica não registrada:', p.mecanica.id)
      this.estado = 'explora'; return
    }
    this.paradaAtiva = paradaId
    this.estado = 'mecanica'                       // congela a exploração enquanto joga
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
