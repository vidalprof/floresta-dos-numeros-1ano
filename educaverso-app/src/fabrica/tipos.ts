// ============================================================================
// FÁBRICA — o CONTRATO da atividade (Zod) e o planejador v1.
// O professor preenche o PEDIDO; o planejador vira um PLANO validado; o motor monta.
// "Dado torto não monta" — o Zod valida ANTES. E a trava do Portão 0 é regra aqui:
// o PROBLEMA vem primeiro; o personagem PERGUNTA (a fala termina com "?").
// (v1 é por REGRA/template; o passo de IA — Pollinations no navegador — entra depois,
//  substituindo só a função `planejar`, sem mexer no motor.)
// ============================================================================
import { z } from 'zod'

export const DIFICULDADES = ['facil', 'medio', 'dificil'] as const
export const DISCIPLINAS = ['Matemática', 'Português', 'Ciências', 'História', 'Geografia'] as const

export const PedidoAtividade = z.object({
  ano: z.string().min(1),                       // ex.: "1º ano"
  disciplina: z.enum(DISCIPLINAS),
  objetivo: z.string().min(3),                  // objetivo de aprendizagem (BNCC)
  tema: z.string().min(2),                      // ex.: "fazenda", "floresta", "espaço"
  tempoMin: z.number().int().min(5).max(90),
  dificuldade: z.enum(DIFICULDADES)
})
export type PedidoAtividade = z.infer<typeof PedidoAtividade>

// PLANO validado que o motor consome. `problema` é a fala do personagem — DEVE terminar
// em "?" (Portão 0: o personagem PERGUNTA, não responde; o problema vem primeiro).
export const PlanoFase = z.object({
  titulo: z.string().min(2),
  mecanica: z.literal('contar'),                // v1 só "contar/juntar"; catálogo cresce depois
  melAlvo: z.number().int().min(2).max(9),
  problema: z.string().refine(s => s.trim().endsWith('?'), 'Portão 0: o personagem PERGUNTA (termine em "?")'),
  entrega: z.string().min(3),
  vitoria: z.string().min(3),
  emoji: z.string().min(1),
  tema: z.string().min(2)
})
export type PlanoFase = z.infer<typeof PlanoFase>

// mapeia dificuldade -> quantos itens juntar (a "conta" que a criança faz)
const ALVO: Record<typeof DIFICULDADES[number], number> = { facil: 3, medio: 5, dificil: 7 }

// tema -> personagem + item (v1 por template; coerência mínima com o tema)
const CENARIO: Record<string, { quem: string, item: string, emoji: string }> = {
  fazenda: { quem: 'o fazendeiro', item: 'potes de MEL', emoji: '🧑‍🌾' },
  floresta: { quem: 'a coruja', item: 'cogumelos', emoji: '🦉' },
  espaco: { quem: 'o astronauta', item: 'cristais', emoji: '🧑‍🚀' },
  mar: { quem: 'o pescador', item: 'conchas', emoji: '🎣' }
}
const chaveTema = (t: string): string => {
  const s = t.toLowerCase()
  if (s.includes('flor')) return 'floresta'
  if (s.includes('espa') || s.includes('planeta') || s.includes('estrel')) return 'espaco'
  if (s.includes('mar') || s.includes('praia') || s.includes('oceano')) return 'mar'
  return 'fazenda'
}

// PLANEJADOR v1 (por regra). Recebe o pedido do professor -> devolve o plano validado.
// O problema é sempre uma PERGUNTA (Portão 0) e vem PRIMEIRO; o conceito (contar) fica
// embutido na AÇÃO de juntar, não numa prova.
export function planejar (pedido: PedidoAtividade): PlanoFase {
  const c = CENARIO[chaveTema(pedido.tema)]
  const alvo = ALVO[pedido.dificuldade]
  const plano: PlanoFase = {
    titulo: `${pedido.tema[0].toUpperCase()}${pedido.tema.slice(1)} — a coleta`,
    mecanica: 'contar',
    melAlvo: alvo,
    problema: `${c.quem} precisa de ${alvo} ${c.item} para a festa! Você me ajuda a juntar?`,
    entrega: `Obrigado! Você juntou ${alvo}. O caminho se abriu — siga!`,
    vitoria: 'Missão cumprida! (a próxima aventura entra aqui)',
    emoji: c.emoji,
    tema: chaveTema(pedido.tema)
  }
  return PlanoFase.parse(plano)          // valida (inclui a trava do Portão 0)
}
