// ============================================================================
// CENÁRIOS — cada FASE da aventura acontece num LUGAR diferente do mesmo pack
// (pedido do Marcos: "cenário diferente pra criança não enjoar"; pesquisa: a troca
// de bioma reinicia o relógio de atenção 6-9 anos e é a "múltipla incorporação" de
// Dienes — o MESMO conceito em 3 roupas). O gerador de mapa monta o esqueleto
// jogável (fazendeiro, carroça, pilha, vagas, saída); o CENÁRIO troca a decoração,
// a estrutura, a água e o CLIMA (ambiente vivo) — sem tocar na jogabilidade.
//
// A JORNADA da tabuada: Fazenda (multiplicar) → Floresta (a travessia) → Beira do
// Rio / Mercado (dividir). Mesmo Tião, mesma lei dos grupos iguais, lugares novos.
//
// Só usa props que EXISTEM no kit (kits.ts). Prop ausente = ignorado (degrada bem).
// Posições FIXAS = determinístico (o QA reproduz; nada aleatório que quebra teste).
// As posições evitam a faixa de jogo (fazendeiro ~9,6; carroça 11,6; vagas y=13;
// pilha 17,13; casa 3,3) — colisão nos props faz o espalhador de itens desviar deles.
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

// FASE 1 — FAZENDA (reproduz EXATAMENTE o visual auditado; sol, arbustos, casa)
const FAZENDA: CenarioDef = {
  id: 'fazenda', nome: 'A Fazenda do Tião', ambiente: '',
  estrutura: 'casa_a',
  scatter: [
    { prop: 'arvore', tx: 2, ty: 9 }, { prop: 'arvore', tx: 16, ty: 3 },
    { prop: 'arvore', tx: 15, ty: 9 }, { prop: 'arvore', tx: 11, ty: 11 },
    { prop: 'arvore', tx: 6, ty: 12 }, { prop: 'flor', tx: 5, ty: 7 }, { prop: 'margarida', tx: 13, ty: 8 }
  ]
}

// FASE 2 — FLORESTA (pinheiros densos, carvalho, cogumelos, toco; vaga-lumes)
const FLORESTA: CenarioDef = {
  id: 'floresta', nome: 'A Trilha da Floresta', ambiente: 'vagalumes',
  estrutura: 'carvalho',
  scatter: [
    { prop: 'pinheiro', tx: 2, ty: 4 }, { prop: 'pinheiro', tx: 16, ty: 3 },
    { prop: 'pinheiro', tx: 15, ty: 10 }, { prop: 'pinheiro', tx: 3, ty: 11 },
    { prop: 'carvalho', tx: 7, ty: 3 }, { prop: 'cogumelo', tx: 5, ty: 8 },
    { prop: 'cogumelo', tx: 13, ty: 11 }, { prop: 'toco', tx: 6, ty: 12 }, { prop: 'arbusto', tx: 14, ty: 7 }
  ]
}

// FASE 3 — BEIRA DO RIO / MERCADO (pedras, laguinho, cerejeiras; clímax da divisão)
const RIO: CenarioDef = {
  id: 'rio', nome: 'O Mercado da Beira do Rio', ambiente: 'petalas',
  estrutura: 'casa_a',
  agua: { x0: 14, y0: 2, w: 4, h: 3 },
  scatter: [
    { prop: 'cerejeira', tx: 2, ty: 4 }, { prop: 'cerejeira', tx: 6, ty: 11 },
    { prop: 'pedra_g', tx: 4, ty: 8 }, { prop: 'pedra_p', tx: 13, ty: 10 },
    { prop: 'pedra_p', tx: 12, ty: 6 }, { prop: 'flor', tx: 8, ty: 4 }, { prop: 'margarida', tx: 15, ty: 8 }
  ]
}

export const CENARIOS: Record<string, CenarioDef> = { fazenda: FAZENDA, floresta: FLORESTA, rio: RIO }

export function getCenario (id?: string): CenarioDef { return (id && CENARIOS[id]) || FAZENDA }
