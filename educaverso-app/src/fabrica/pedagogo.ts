// ============================================================================
// O PEDAGOGO — planeja a APRENDIZAGEM ANTES do roteirista (a ordem que o Marcos exige).
// Dado (ano, disciplina, objetivo BNCC), entrega a "ESPINHA DE APRENDIZAGEM": a
// progressão (sub-passos concreto→pictórico→abstrato), a DINÂMICA de fundo (resolver/
// criar/investigar/coletar/narrar/simular — NUNCA quiz raso), a mecânica concreta, o
// alvo (dificuldade), a NECESSIDADE DO MUNDO (por que a criança é preciso) e COMO MEDIR
// (transferência — problema novo). O roteirista depois só VESTE de história.
// Base: MODELO-APRENDIZAGEM-EDUCAVERSO.md (Vygotsky/ZDP, CPA/Bruner, LM-GM, learning
// trajectories, integração intrínseca). v1 por regra; a IA entra trocando só esta função.
// ============================================================================
import { z } from 'zod'
import type { PedidoAtividade } from './tipos'
import { DIFICULDADES } from './tipos'

export const DINAMICAS = ['resolver', 'criar', 'investigar', 'coletar', 'narrar', 'simular'] as const

// um sub-passo da progressão, marcado no eixo CPA (concreto→pictórico→abstrato)
export const Passo = z.object({
  kc: z.string().min(2),                       // componente de conhecimento (o "nó")
  cpa: z.enum(['concreto', 'pictorico', 'abstrato']),
  descricao: z.string().min(3)
})

export const Espinha = z.object({
  ano: z.string().min(1),
  disciplina: z.string().min(2),
  objetivo: z.string().min(3),
  dinamica: z.enum(DINAMICAS),                 // a dinâmica de FUNDO (não é quiz)
  mecanica: z.literal('contar'),               // v1 jogável; catálogo cresce depois
  alvo: z.number().int().min(2).max(9),         // dificuldade calibrada (ZDP)
  progressao: z.array(Passo).min(1),           // sub-passos ordenados (learning trajectory)
  necessidadeMundo: z.string().min(5),         // por que o mundo PRECISA da criança
  medir: z.string().min(5)                      // como saber que aprendeu (transferência)
})
export type Espinha = z.infer<typeof Espinha>

const ALVO: Record<typeof DIFICULDADES[number], number> = { facil: 3, medio: 5, dificil: 7 }

// Escolhe a DINÂMICA pelo objetivo (não pela mecânica). v1: só temos "contar" jogável, então
// a dinâmica é "coletar/organizar com propósito" (itens = ferramentas-signo de Vygotsky).
// A estrutura já está pronta para, quando houver mais mecânicas, mapear objetivo→dinâmica.
function escolherDinamica (_pedido: PedidoAtividade): typeof DINAMICAS[number] {
  return 'coletar'
}

// PEDAGOGO v1 (por regra). Monta a espinha para o objetivo de CONTAGEM/quantidade.
export function planejarPedagogia (pedido: PedidoAtividade): Espinha {
  const alvo = ALVO[pedido.dificuldade]
  const dinamica = escolherDinamica(pedido)
  // progressão CPA da contagem (o "pedagogo" quebra o objetivo em sub-passos ordenados)
  const progressao = [
    { kc: 'correspondência 1-a-1', cpa: 'concreto' as const, descricao: `juntar ${alvo} objetos, um a um, tocando cada um` },
    { kc: 'cardinalidade', cpa: 'pictorico' as const, descricao: `saber que o último contado diz QUANTOS há (${alvo})` },
    { kc: 'reconhecer a quantidade', cpa: 'abstrato' as const, descricao: `associar a coleção ao número ${alvo}` }
  ]
  const espinha: Espinha = {
    ano: pedido.ano,
    disciplina: pedido.disciplina,
    objetivo: pedido.objetivo,
    dinamica,
    mecanica: 'contar',
    alvo,
    progressao,
    necessidadeMundo: `alguém no mundo precisa de exatamente ${alvo} de algo para resolver um problema real — e só contando/juntando certo isso se resolve`,
    medir: `dar à criança uma coleção NOVA e ver se ela conta e diz corretamente quantos há (transferência), não só repetir a fase`
  }
  return Espinha.parse(espinha)                 // valida: dado torto não monta
}
