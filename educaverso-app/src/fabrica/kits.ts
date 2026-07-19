// ============================================================================
// ADAPTADOR DE KIT VISUAL — tudo que era FIXO do Ninja Adventure vira DADO aqui.
// Um "kit" descreve: quais imagens carregar, qual tile é grama/parede, onde ficam
// os recortes dos props e como os quadros do personagem estão arrumados.
// Trocar/adicionar visual = plugar um KitVisual novo (baixado por workflow) — o
// motor e o gerador de mapa leem o kit, não valores cravados no código.
// ============================================================================

export interface KitVisual {
  id: string
  nome: string
  // arquivos (em public/rpg/...) por papel
  imagens: {
    chao: string, paredes: string, mundo: string, piso: string,
    heroi: string, fazendeiro: string, sombra: string, mel: string, pedras: string, bau: string
  }
  // tileset do chão (grade de 16)
  chao: { cols: number, imagewidth: number, imageheight: number, tilecount: number, grama: number, pisoInterno: number }
  // tileset das paredes: os 8 pedaços da moldura + um sólido invisível (colisão)
  paredes: { cols: number, imagewidth: number, imageheight: number, tilecount: number,
    TL: number, T: number, TR: number, L: number, R: number, BL: number, B: number, BR: number, solido: number }
  // recortes dos props dentro do atlas "mundo" (x, y, w, h)
  props: Record<string, [number, number, number, number]>
  // personagem 16x16: coluna por direção (baixo/cima/esq/dir) e nº de colunas
  personagem: { cols: number, dir: { down: number, up: number, left: number, right: number } }
  bauFrame: [number, number]     // tamanho do quadro do baú (spritesheet própria)
}

// KIT 1 — "Vilarejo" (o atual, Ninja Adventure CC0, sem tema ninja: elenco neutro)
export const KIT_VILAREJO: KitVisual = {
  id: 'vilarejo',
  nome: 'Vilarejo (padrão)',
  imagens: { chao: 'chao.png', paredes: 'paredes.png', mundo: 'mundo.png', piso: 'piso.png', heroi: 'heroi.png', fazendeiro: 'fazendeiro.png', sombra: 'sombra.png', mel: 'mel.png', pedras: 'pedras.png', bau: 'bau.png' },
  chao: { cols: 22, imagewidth: 352, imageheight: 416, tilecount: 22 * 26, grama: 245, pisoInterno: 246 },
  paredes: { cols: 10, imagewidth: 160, imageheight: 176, tilecount: 110, TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44, solido: 43 },
  props: { casa_a: [0, 0, 64, 48], arvore: [0, 160, 32, 32], estante: [160, 592, 33, 32], tapete: [112, 592, 48, 48] },
  personagem: { cols: 4, dir: { down: 0, up: 1, left: 2, right: 3 } },
  bauFrame: [16, 14]
}

export const KITS: Record<string, KitVisual> = { [KIT_VILAREJO.id]: KIT_VILAREJO }
export const KIT_PADRAO = KIT_VILAREJO.id

export function getKit (id?: string): KitVisual { return (id && KITS[id]) || KIT_VILAREJO }

// lista para o seletor da Fábrica (nome + se já está disponível)
export function kitsDisponiveis (): Array<{ id: string, nome: string }> {
  return Object.values(KITS).map(k => ({ id: k.id, nome: k.nome }))
}
