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

export interface Espalhado { prop: string, tx: number, ty: number, tint?: number }

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

// POSIÇÕES SEGURAS (longe da casa x2-6/y2-5, do fazendeiro 9,6, da carroça 11,6, da
// pilha 17,13, das vagas y13, do herói 10,12 e da saída 19,7), bem ESPAÇADAS entre si
// (props grandes têm ~3 tiles; distância ≥3 evita sobreposição). Props grandes vão nas
// bordas; miúdos (flor/cogumelo/toco) em pontos abertos do meio.
const FLORESTA: CenarioDef = {
  id: 'floresta', nome: 'A Trilha da Floresta', ambiente: 'vagalumes', estrutura: 'casa_a',
  scatter: [
    { prop: 'pinheiro', tx: 1, ty: 8 }, { prop: 'pinheiro', tx: 16, ty: 4 }, { prop: 'pinheiro', tx: 15, ty: 11 },
    { prop: 'toco', tx: 5, ty: 9 }, { prop: 'cogumelo', tx: 13, ty: 9 }, { prop: 'arbusto', tx: 17, ty: 8 }, { prop: 'cogumelo', tx: 7, ty: 11 }
  ]
}

// cerejeira = o arbusto redondo LIMPO tingido de ROSA (flor) — limpo e automático pelo
// motor; a "cerejeira" do atlas denso lia como "3 árvores mal recortadas".
const POMAR: CenarioDef = {
  id: 'pomar', nome: 'O Pomar das Cerejeiras', ambiente: 'petalas', estrutura: 'casa_a',
  scatter: [
    { prop: 'cerejeira', tx: 1, ty: 8 }, { prop: 'cerejeira', tx: 16, ty: 4 }, { prop: 'cerejeira', tx: 15, ty: 11 },
    { prop: 'flor', tx: 6, ty: 9 }, { prop: 'margarida', tx: 13, ty: 9 }, { prop: 'flor', tx: 17, ty: 8 }
  ]
}

// (a água com MARGEM/autotile fica pra um passo futuro; um retângulo azul chapado dava
// cara de "colado" — melhor sem do que mal-feito. Rio = pedras + verde da margem.)
const RIO: CenarioDef = {
  id: 'rio', nome: 'O Mercado da Beira do Rio', ambiente: '', estrutura: 'casa_a',
  scatter: [
    { prop: 'pedra_g', tx: 1, ty: 8 }, { prop: 'pedra_p', tx: 16, ty: 4 }, { prop: 'pedra_g', tx: 15, ty: 11 },
    { prop: 'arbusto', tx: 13, ty: 9 }, { prop: 'arbusto', tx: 5, ty: 9 }, { prop: 'flor', tx: 17, ty: 8 }, { prop: 'margarida', tx: 7, ty: 11 }
  ]
}

const MONTANHA: CenarioDef = {
  id: 'montanha', nome: 'O Alto da Montanha', ambiente: 'folhas', estrutura: 'casa_a',
  scatter: [
    { prop: 'pedra_g', tx: 1, ty: 8 }, { prop: 'pedra_p', tx: 16, ty: 4 }, { prop: 'pinheiro', tx: 15, ty: 11 },
    { prop: 'toco', tx: 5, ty: 9 }, { prop: 'pedra_p', tx: 13, ty: 9 }, { prop: 'pinheiro', tx: 17, ty: 7 }
  ]
}

export const CENARIOS: Record<string, CenarioDef> = { fazenda: FAZENDA, floresta: FLORESTA, pomar: POMAR, rio: RIO, montanha: MONTANHA }

export function getCenario (id?: string): CenarioDef { return (id && CENARIOS[id]) || FAZENDA }
