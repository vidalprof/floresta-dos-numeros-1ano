// ============================================================================
// CENÁRIOS — cada FASE da aventura acontece num LUGAR diferente do mesmo pack
// (pedido do Marcos: "cenário diferente pra criança não enjoar"; pesquisa: a troca
// de bioma reinicia o relógio de atenção 6-9 anos e é a "múltipla incorporação" de
// Dienes — o MESMO conceito em roupas diferentes). O gerador de mapa monta o esqueleto
// jogável (fazendeiro, carroça, pilha, vagas, saída); o CENÁRIO troca a decoração, a
// estrutura, a água e o CLIMA (ambiente vivo) — sem tocar na jogabilidade.
//
// A JORNADA da tabuada (aula ~50 min): Fazenda → Floresta → Pomar (multiplicar) →
// Beira do Rio → Montanha (dividir). Mesmo Tião, mesma lei dos grupos iguais, 5 lugares.
//
// Só usa props que EXISTEM no kit (kits.ts). Posições FIXAS = determinístico (o QA
// reproduz). O espalhador de itens usa BFS de alcançabilidade, então props/água nunca
// prendem um pote — as posições aqui são livres para compor o visual.
// ============================================================================

export type Ambiente = '' | 'vagalumes' | 'petalas' | 'folhas' | 'neve'

export interface Espalhado { prop: string, tx: number, ty: number }

export interface CenarioDef {
  id: string
  nome: string
  ambiente: Ambiente
  scatter: Espalhado[]       // props decorativos (colidem na base)
  estrutura: string          // o "prédio" do canto (prop do atlas)
  agua?: { x0: number, y0: number, w: number, h: number }   // laguinho opcional (colide)
}

const FAZENDA: CenarioDef = {
  id: 'fazenda', nome: 'A Fazenda do Tião', ambiente: '', estrutura: 'casa_a',
  scatter: [
    { prop: 'arvore', tx: 2, ty: 9 }, { prop: 'arvore', tx: 16, ty: 3 }, { prop: 'arvore', tx: 15, ty: 9 },
    { prop: 'arvore', tx: 6, ty: 12 }, { prop: 'flor', tx: 5, ty: 7 }, { prop: 'margarida', tx: 13, ty: 8 }, { prop: 'flor', tx: 8, ty: 4 }
  ]
}

const FLORESTA: CenarioDef = {
  id: 'floresta', nome: 'A Trilha da Floresta', ambiente: 'vagalumes', estrutura: 'carvalho',
  scatter: [
    { prop: 'pinheiro', tx: 2, ty: 4 }, { prop: 'pinheiro', tx: 16, ty: 3 }, { prop: 'pinheiro', tx: 15, ty: 10 },
    { prop: 'pinheiro', tx: 3, ty: 11 }, { prop: 'carvalho', tx: 7, ty: 3 }, { prop: 'cogumelo', tx: 5, ty: 8 },
    { prop: 'cogumelo', tx: 13, ty: 11 }, { prop: 'toco', tx: 6, ty: 12 }, { prop: 'arbusto', tx: 14, ty: 7 }
  ]
}

const POMAR: CenarioDef = {
  id: 'pomar', nome: 'O Pomar das Cerejeiras', ambiente: 'petalas', estrutura: 'casa_a',
  scatter: [
    { prop: 'cerejeira', tx: 2, ty: 4 }, { prop: 'cerejeira', tx: 16, ty: 3 }, { prop: 'cerejeira', tx: 15, ty: 10 },
    { prop: 'cerejeira', tx: 3, ty: 11 }, { prop: 'flor', tx: 6, ty: 8 }, { prop: 'margarida', tx: 13, ty: 7 }, { prop: 'flor', tx: 9, ty: 4 }
  ]
}

const RIO: CenarioDef = {
  id: 'rio', nome: 'O Mercado da Beira do Rio', ambiente: '', estrutura: 'casa_a',
  agua: { x0: 14, y0: 2, w: 4, h: 3 },
  scatter: [
    { prop: 'pedra_g', tx: 4, ty: 8 }, { prop: 'pedra_p', tx: 13, ty: 10 }, { prop: 'pedra_p', tx: 12, ty: 6 },
    { prop: 'arbusto', tx: 2, ty: 4 }, { prop: 'arbusto', tx: 6, ty: 11 }, { prop: 'margarida', tx: 8, ty: 4 }
  ]
}

const MONTANHA: CenarioDef = {
  id: 'montanha', nome: 'O Alto da Montanha', ambiente: 'folhas', estrutura: 'casa_a',
  scatter: [
    { prop: 'pedra_g', tx: 2, ty: 4 }, { prop: 'pedra_g', tx: 16, ty: 9 }, { prop: 'pedra_p', tx: 15, ty: 3 },
    { prop: 'pedra_p', tx: 4, ty: 11 }, { prop: 'pinheiro', tx: 7, ty: 3 }, { prop: 'pinheiro', tx: 14, ty: 11 }, { prop: 'toco', tx: 6, ty: 8 }
  ]
}

export const CENARIOS: Record<string, CenarioDef> = { fazenda: FAZENDA, floresta: FLORESTA, pomar: POMAR, rio: RIO, montanha: MONTANHA }

export function getCenario (id?: string): CenarioDef { return (id && CENARIOS[id]) || FAZENDA }
