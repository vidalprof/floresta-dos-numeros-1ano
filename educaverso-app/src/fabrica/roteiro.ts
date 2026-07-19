// ============================================================================
// O ROTEIRISTA — monta a HISTÓRIA inteira (em dados) a partir do pedido do professor.
// Saída: um ROTEIRO validado (Zod) que o motor ENCENA: abertura → pedido (problema) →
// clímax (juntou tudo) → entrega (o mundo muda) → vitória. Personagem tem NOME, o mundo
// PRECISA da criança (Portão 0: o problema vem primeiro; o personagem PERGUNTA).
//
// Quem "pensa" a história é uma IA que escreve NESTA estrutura:
//  - EU (Claude), quando produzo a atividade sob encomenda (melhor qualidade, testável já);
//  - a IA do navegador (Pollinations) no site auto-serviço, depois.
// `escreverRoteiro` é o roteirista v1 (por regra, coerente com o tema) — a IA entra
// substituindo SÓ esta função, sem tocar no motor.
// ============================================================================
import { z } from 'zod'
import type { PedidoAtividade } from './tipos'
import { DIFICULDADES } from './tipos'

export const Roteiro = z.object({
  titulo: z.string().min(2),
  sinopse: z.string().min(5),
  personagem: z.object({ nome: z.string().min(2), emoji: z.string().min(1) }),
  kitId: z.string().min(2),                 // tema visual
  mecanica: z.literal('contar'),
  alvo: z.number().int().min(2).max(9),
  item: z.string().min(2),                  // "potes de mel", "cristais"...
  falas: z.object({
    abertura: z.string().min(5),            // narração do mundo (quem, onde)
    pedido: z.string().refine(s => s.trim().endsWith('?'), 'Portão 0: o personagem PERGUNTA (termine em "?")'),
    juntouTudo: z.string().min(3),          // clímax: a criança conseguiu tudo
    entrega: z.string().min(3),             // o mundo MUDA
    vitoria: z.string().min(3)              // fechamento + gancho
  })
})
export type Roteiro = z.infer<typeof Roteiro>

// tema -> elenco coerente (nome + papel + item + kit visual)
interface Cena { nome: string, papel: string, item: string, emoji: string, kitId: string, onde: string }
const ELENCO: Record<string, Cena> = {
  fazenda: { nome: 'Tião', papel: 'fazendeiro', item: 'potes de mel', emoji: '🧑‍🌾', kitId: 'vilarejo', onde: 'numa fazendinha ensolarada' },
  floresta: { nome: 'Cora', papel: 'coruja', item: 'cogumelos brilhantes', emoji: '🦉', kitId: 'vilarejo', onde: 'no coração da floresta' },
  espaco: { nome: 'Nova', papel: 'astronauta', item: 'cristais de energia', emoji: '🧑‍🚀', kitId: 'vilarejo', onde: 'numa base perdida no espaço' },
  mar: { nome: 'Bento', papel: 'pescador', item: 'conchas raras', emoji: '🎣', kitId: 'vilarejo', onde: 'à beira-mar' }
}
const chaveTema = (t: string): string => {
  const s = t.toLowerCase()
  if (s.includes('flor')) return 'floresta'
  if (s.includes('espa') || s.includes('planeta') || s.includes('estrel')) return 'espaco'
  if (s.includes('mar') || s.includes('praia') || s.includes('oceano')) return 'mar'
  return 'fazenda'
}
const ALVO: Record<typeof DIFICULDADES[number], number> = { facil: 3, medio: 5, dificil: 7 }

// ROTEIRISTA v1 (por regra). Objetivo -> história jogável, com o conceito DENTRO da ação
// (juntar/contar), nunca uma prova. O problema vem primeiro; o Byte pergunta.
export function escreverRoteiro (pedido: PedidoAtividade): Roteiro {
  const c = ELENCO[chaveTema(pedido.tema)]
  const alvo = ALVO[pedido.dificuldade]
  const r: Roteiro = {
    titulo: `${c.nome} e ${c.item}`,
    sinopse: `${c.nome}, ${c.papel} ${c.onde}, tem um problema — e só a criança pode ajudar juntando ${alvo} ${c.item}.`,
    personagem: { nome: c.nome, emoji: c.emoji },
    kitId: c.kitId,
    mecanica: 'contar',
    alvo,
    item: c.item,
    falas: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, corre até você, aflito.`,
      pedido: `Oi! Preciso de ${alvo} ${c.item} para a festa e não dou conta sozinho. Você conta e junta comigo?`,
      juntouTudo: `Isso! ${alvo} ${c.item}! Você contou tudo certinho. Leva pra mim, corre!`,
      entrega: `Muito obrigado! Olha — o caminho que estava fechado se abriu pra você. Vai lá!`,
      vitoria: `Você salvou a festa de ${c.nome}! E tem uma nova aventura te esperando adiante…`
    }
  }
  return Roteiro.parse(r)          // valida (inclui a trava do Portão 0)
}
