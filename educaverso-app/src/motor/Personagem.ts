// ============================================================================
// COMPONENTE PERSONAGEM (genérico e reaproveitável para QUALQUER personagem)
// Carrega o atlas de poses (public/personagens/<nome>/) e dá VIDA:
//   - micro-vida sempre (respira plantado, pisca de vez em quando) -> nunca parado/morto
//   - andar em 4 direções (frente/costas/lados) trocando os quadros da cartela
//   - EMOÇÕES guiadas pelo ROTEIRO: feliz, triste, sentar, deitar, acenar…
// A história aciona os gatilhos (ex.: acertou -> feliz; errou -> triste).
// Trocar de personagem = trocar a pasta do atlas. A mecânica não muda.
// ============================================================================
import Phaser from 'phaser'

// quadros de caminhada por direção (usa o que existir no atlas; cai p/ 'parado')
const CICLO: { [dir: string]: string[] } = {
  baixo: ['passo_a', 'passo_b', 'passo_c'],
  cima: ['costas', 'costas_passo'],
  esq: ['lado', 'lado_passo'],
  dir: ['lado', 'lado_passo']
}
const PARADO: { [dir: string]: string } = { baixo: 'parado', cima: 'costas', esq: 'lado', dir: 'lado' }

export class Personagem {
  scene: Phaser.Scene
  nome: string
  sprite: Phaser.GameObjects.Image
  sombra: Phaser.GameObjects.Image
  escalaAlt: number
  temPose: { [p: string]: boolean } = {}

  estado = 'parado'          // parado | andar | <emoção>
  dir = 'baixo'
  resp = 0; passoFase = 0; piscaT = 3; emoT = 0

  constructor (scene: Phaser.Scene, nome: string, x: number, y: number, escalaAlt = 88) {
    this.scene = scene; this.nome = nome; this.escalaAlt = escalaAlt
    // quais poses existem de fato (o atlas pode ter mais ou menos)
    for (const p of Personagem.POSES) this.temPose[p] = scene.textures.exists(nome + '_' + p)
    this.sombra = scene.add.image(x, y + 2, 'sombra').setDepth(1)
    this.sprite = scene.add.image(x, y, this.tex('parado')).setOrigin(0.5, 1)
    this.sprite.setScale(escalaAlt / this.sprite.height)
  }

  // conjunto-padrão de poses (a fábrica gera o que fizer sentido p/ o personagem)
  static POSES = ['parado', 'piscar', 'passo_a', 'passo_b', 'passo_c', 'costas', 'costas_passo',
    'lado', 'lado_passo', 'sentar', 'deitar', 'acenar', 'feliz', 'triste']

  // carrega as poses de um personagem (chamar no preload da cena).
  // Lê o manifest.json da pasta e carrega SÓ as poses que existem (zero 404);
  // sem manifest, cai no conjunto completo (comportamento antigo).
  static preload (scene: Phaser.Scene, nome: string) {
    const mk = nome + '_manifest'
    if (scene.cache.json.exists(mk)) { Personagem.carregaPoses(scene, nome); return }
    scene.load.json(mk, 'personagens/' + nome + '/manifest.json')
    scene.load.once('filecomplete-json-' + mk, () => Personagem.carregaPoses(scene, nome))
    scene.load.once('loaderror', (f: any) => { if (f && f.key === mk) { for (const p of Personagem.POSES) scene.load.image(nome + '_' + p, 'personagens/' + nome + '/' + p + '.png') } })
  }
  static carregaPoses (scene: Phaser.Scene, nome: string) {
    const m = scene.cache.json.get(nome + '_manifest')
    const poses = m && m.poses ? Object.keys(m.poses) : Personagem.POSES
    for (const p of poses) if (!scene.textures.exists(nome + '_' + p)) scene.load.image(nome + '_' + p, 'personagens/' + nome + '/' + (m && m.poses && m.poses[p] ? m.poses[p] : p + '.png'))
  }

  tex (p: string) {
    return this.temPose[p] ? this.nome + '_' + p : this.nome + '_parado'
  }
  troca (p: string) {
    const k = this.tex(p)
    if (this.sprite.texture.key !== k) {
      const escY = this.sprite.scaleY   // preserva o "respiro" atual
      this.sprite.setTexture(k)
      this.sprite.setScale(this.escalaAlt / this.sprite.height)
    }
  }

  // ---- GATILHOS que o ROTEIRO/mecânica aciona ----
  setDir (d: string) { this.dir = d }
  andar (ligado: boolean) { if (this.estado === 'andar' || this.estado === 'parado') this.estado = ligado ? 'andar' : 'parado' }
  parar () { this.estado = 'parado' }
  // emoção temporária (volta ao normal depois de seg); -1 = fica até trocar
  emocao (nome: string, seg = 2.2) { this.estado = nome; this.emoT = seg }
  feliz (s = 2.5) { this.emocao('feliz', s) }
  triste (s = 2.5) { this.emocao('triste', s) }
  acenar (s = 2) { this.emocao('acenar', s) }
  sentar () { this.emocao('sentar', -1) }
  deitar () { this.emocao('deitar', -1) }

  setPos (x: number, y: number) { this.sprite.setPosition(x, y); this.sombra.setPosition(x, y + 2) }
  get x () { return this.sprite.x }
  get y () { return this.sprite.y }

  update (dt: number) {
    // emoção com tempo -> volta ao parado
    if (this.emoT > 0) { this.emoT -= dt; if (this.emoT <= 0 && this.estado !== 'andar') this.estado = 'parado' }

    const flip = this.dir === 'esq'
    this.sprite.setFlipX(flip)
    this.sprite.setDepth(this.sprite.y)
    this.sombra.setPosition(this.sprite.x, this.sprite.y + 2)

    if (this.estado === 'andar') {
      this.passoFase += dt * 8
      const ciclo = (CICLO[this.dir] || CICLO.baixo).filter(p => this.temPose[p])
      const seq = ciclo.length ? ciclo : ['parado']
      this.troca(seq[Math.floor(this.passoFase) % seq.length])
      // saltinho plantado (squash & stretch), pés no chão
      const b = Math.sin(this.passoFase * Math.PI)
      const base = this.escalaAlt / this.sprite.height
      this.sprite.setScale(base * (1 - 0.04 * b) * (flip ? 1 : 1), base * (1 + 0.06 * b))
      this.sombra.setScale(1 - 0.12 * Math.max(0, b))
    } else if (this.estado === 'parado') {
      // respira + pisca de vez em quando (micro-vida)
      this.resp += dt * 2.2
      const r = Math.sin(this.resp)
      this.piscaT -= dt
      let pose = PARADO[this.dir] || 'parado'
      if (this.piscaT <= 0) {
        if (this.piscaT > -0.16 && this.temPose['piscar'] && this.dir === 'baixo') pose = 'piscar'
        else this.piscaT = 2.5 + Math.random() * 3
      }
      this.troca(pose)
      const base = this.escalaAlt / this.sprite.height
      this.sprite.setScale(base * (1 - 0.02 * r), base * (1 + 0.03 * r))
      this.sombra.setScale(1)
    } else {
      // EMOÇÃO (feliz/triste/sentar/deitar/acenar) — segura a pose, com respiro leve
      this.resp += dt * 2.6
      const r = Math.sin(this.resp)
      this.troca(this.estado)
      const base = this.escalaAlt / this.sprite.height
      const pulso = this.estado === 'feliz' ? 0.06 : 0.02
      this.sprite.setScale(base * (1 - pulso * r * 0.5), base * (1 + pulso * r))
    }
  }
}
