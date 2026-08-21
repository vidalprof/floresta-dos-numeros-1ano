// ============================================================================
// EducaVerso — App (FÁBRICA DE MUNDOS, motor oficial Phaser + TS)
// Config em MODO ULTRALEVE para o PC real da escola
// (AMD FX-4300 · 3,5 GB RAM · Win7 · Chrome 109 / Firefox 106).
//
// Cenas:
//  - Mundo (PADRÃO): o MONTADOR v2 — lê uma AVENTURA (grafo de zonas) e arma
//    o mundo explorável. Padrão: "A Floresta do Byte" (estilo composto — o que
//    o Marcos pediu). ?pomar = mundo Pomar (estilo prancha). ?teste = teste.
//  - Ilha (?ilha): a cena artesanal antiga (referência histórica).
// ============================================================================
import Phaser from 'phaser'
import { Ilha } from './scenes/Ilha'
import { Mundo } from './motor/Mundo'
import { validarAventura } from './motor/aventura'
import { AVENTURA_POMAR } from './aventuras/pomar'
import { AVENTURA_FLORESTA } from './aventuras/floresta'
import { AVENTURA_GRUPOS } from './aventuras/grupos'
import { AVENTURA_TESTE } from './aventuras/teste'
import { VilaViva } from './rpg/VilaViva'
import { UIVila } from './rpg/UIVila'
import { MundoAutor } from './rpg/MundoAutor'
import { FasesDemo } from './rpg/FasesDemo'
import { FaseUm } from './rpg/FaseUm'
import { FaseGrid } from './rpg/FaseGrid'
import { GridEngine } from 'grid-engine'
import { montarFabrica } from './fabrica/Fabrica'

const q = new URLSearchParams(location.search)

// PAINEL DO PROFESSOR (?painel / __BOOT='painel'): página própria, sem Phaser
const soPainel = q.has('painel') || (window as any).__BOOT === 'painel'
if (soPainel) {
  for (const id of ['telaIntro', 'telaWin', 'btnOuvir', 'hud']) {
    const el = document.getElementById(id)
    if (el) el.style.display = 'none'
  }
  document.body.style.background = '#0e1524'
  void import('./painel/painel').then(m => m.montarPainel())
}

const usarIlha = q.has('ilha')
// RPG (plataforma nova, identidade Ninja Adventure): ?rpg na URL OU flag
// window.__BOOT='rpg' injetada no index.html do repo publicado do demo.
const usarRpg = q.has('rpg') || (window as any).__BOOT === 'rpg'
const usarAutor = q.has('autor') || (window as any).__BOOT === 'autor'
const usarFases = q.has('fases') || (window as any).__BOOT === 'fases'
const usarF1 = q.has('f1') || (window as any).__BOOT === 'f1'
const usarGrid = q.has('fgrid') || (window as any).__BOOT === 'fgrid'
// 'tabuada' = LINK DIRETO DO JOGO: a Fábrica gera a fase sozinha (sem formulário)
const usarFabrica = q.has('fabrica') || (window as any).__BOOT === 'fabrica' || q.has('tabuada') || (window as any).__BOOT === 'tabuada'

// esconde a UI legada ANTES de criar o jogo (se o Phaser falhar no aparelho,
// a capa antiga nao pode ficar orfa na tela com botao morto)
const usarPix = usarRpg || usarAutor || usarFases || usarF1 || usarGrid || usarFabrica
if (usarPix) {
  for (const id of ['telaIntro', 'telaWin', 'btnOuvir', 'hud']) {
    const el = document.getElementById(id)
    if (el) el.style.display = 'none'
  }
  document.body.style.background = '#0e0c12'
}

const jogo = soPainel ? null : new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  backgroundColor: usarPix ? '#0e0c12' : '#060c18',
  // RPG usa FIT (o QUADRO INTEIRO do jogo aparece, com faixas se sobrar tela —
  // pedido do Marcos: nada de cortar os cantos). Mundos ilustrados seguem ENVELOP.
  scale: { mode: usarAutor ? Phaser.Scale.ENVELOP : ((usarRpg || usarFases || usarF1 || usarGrid || usarFabrica) ? Phaser.Scale.FIT : Phaser.Scale.ENVELOP), autoCenter: Phaser.Scale.CENTER_BOTH, width: 1024, height: 768 },
  fps: { target: 30, forceSetTimeOut: true },
  // pixel art 16px: nearest + roundPixels (nitido); mundos ilustrados: antialias.
  render: usarPix
    ? { antialias: false, pixelArt: true, roundPixels: true, powerPreference: 'low-power' }
    : { antialias: true, roundPixels: false, powerPreference: 'low-power' },
  physics: { default: 'arcade', arcade: { gravity: { x: 0, y: 0 }, debug: false } },
  // grid-engine é um plugin de CENA (usado pela FaseGrid, o novo jeito Tiled)
  plugins: { scene: [{ key: 'gridEngine', plugin: GridEngine, mapping: 'gridEngine' }] },
  scene: usarIlha ? [Ilha] : (usarGrid ? [FaseGrid] : (usarF1 ? [FaseUm] : (usarFases ? [FasesDemo] : (usarAutor ? [MundoAutor] : (usarRpg ? [VilaViva, UIVila] : [])))))
})

if (!jogo) {
  // painel: nada de jogo
} else if (usarFabrica) {
  // FÁBRICA: o professor preenche o formulário e a fase nasce na hora (sem cena inicial).
  jogo.events.once('ready', () => montarFabrica(jogo))
} else if (!usarIlha && !usarRpg && !usarAutor && !usarFases && !usarF1 && !usarGrid) {
  // Zod valida os dados ANTES de montar (dado torto não monta).
  // ?grupos (ou a flag __AVENTURA no index publicado) = "O Pomar dos Grupos"
  const usarGrupos = q.has('grupos') || (window as any).__AVENTURA === 'grupos'
  const aventura = validarAventura(q.has('teste') ? AVENTURA_TESTE : (q.has('pomar') ? AVENTURA_POMAR : (usarGrupos ? AVENTURA_GRUPOS : AVENTURA_FLORESTA)))
  jogo.events.once('ready', () => {
    jogo.scene.add('Mundo', Mundo, true, { aventura })
  })
}

// expõe o jogo p/ o QA automático (Playwright dirige o mundo de verdade)
;(window as any).jogo = jogo
