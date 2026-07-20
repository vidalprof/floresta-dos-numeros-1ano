// ============================================================================
// CENÁRIOS — cada FASE da aventura acontece num LUGAR diferente do mesmo pack
// (pedido do Marcos: "cenário diferente pra criança não enjoar"). O gerador de
// mapa monta o esqueleto jogável (fazendeiro, carroça, pilha, vagas, saída); o
// CENÁRIO troca a decoração (quais props espalhar), o CLIMA (ambiente vivo) e o
// tom — sem tocar na jogabilidade. Assim a mesma lei do mundo vira uma JORNADA:
// fazenda → floresta → cidade, como se a criança jogasse um jogo de verdade.
//
// Um cenário só usa props que EXISTEM no kit (kits.ts, objeto `props`). Se um
// prop não existir, o gerador ignora aquele item (degrada com elegância).
// ============================================================================

export type Ambiente = '' | 'vagalumes' | 'petalas' | 'folhas' | 'neve'

export interface Espalhado { prop: string, tx: number, ty: number }

export interface CenarioDef {
  id: string
  nome: string
  ambiente: Ambiente
  // props decorativos espalhados pelo campo (colidem na base). Posições fixas =
  // determinístico (o QA reproduz; nada de aleatório que quebra teste).
  scatter: Espalhado[]
  estrutura: string          // o "prédio" do canto (casa/loja/tenda) — prop do atlas
}

// FAZENDA — o lugar inicial (reproduz EXATAMENTE o visual auditado da vila-tabuada)
const FAZENDA: CenarioDef = {
  id: 'fazenda', nome: 'A Fazenda do Tião', ambiente: '',
  estrutura: 'casa_a',
  scatter: [
    { prop: 'arvore', tx: 2, ty: 9 }, { prop: 'arvore', tx: 16, ty: 3 },
    { prop: 'arvore', tx: 15, ty: 9 }, { prop: 'arvore', tx: 11, ty: 11 },
    { prop: 'arvore', tx: 6, ty: 12 }
  ]
}

export const CENARIOS: Record<string, CenarioDef> = { fazenda: FAZENDA }

export function getCenario (id?: string): CenarioDef { return (id && CENARIOS[id]) || FAZENDA }
