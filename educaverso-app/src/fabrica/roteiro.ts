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

export const Roteiro = z.object({
  titulo: z.string().min(2),
  sinopse: z.string().min(5),
  personagem: z.object({ nome: z.string().min(2), emoji: z.string().min(1) }),
  kitId: z.string().min(2),                 // tema visual
  mecanica: z.enum(['contar', 'somar', 'selecionar', 'ordenar', 'agrupar']),
  alvo: z.number().int().min(2).max(20),    // contar: qtde | somar: a soma | agrupar: o total | outras: reserva
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
// ROTEIRISTA v1 (por regra). Escreve a história EM CIMA da ESPINHA que o pedagogo entregou —
// não decide alvo nem dinâmica (isso é do pedagogo); só VESTE de mundo/personagem, com o
// conceito DENTRO da ação e o problema primeiro (Portão 0). `espinha` é opcional só p/ retro-
// compatibilidade; a Fábrica sempre passa a espinha do pedagogo.
export function escreverRoteiro (pedido: PedidoAtividade, espinha?: { alvo: number, alvoSoma?: number, agTotal?: number, mecanica?: 'contar' | 'somar' | 'selecionar' | 'ordenar' | 'agrupar', regra?: string, necessidadeMundo?: string }): Roteiro {
  const c = ELENCO[chaveTema(pedido.tema)]
  const mecanica = espinha?.mecanica ?? 'contar'
  const regra = espinha?.regra ?? 'a regra'
  const alvo = mecanica === 'somar' ? (espinha?.alvoSoma ?? 12) : (mecanica === 'agrupar' ? (espinha?.agTotal ?? 12) : (espinha?.alvo ?? { facil: 3, medio: 5, dificil: 7 }[pedido.dificuldade]))

  // as falas por mecânica — o pedido SEMPRE termina perguntando (Portão 0)
  const FALAS: Record<string, Roteiro['falas']> = {
    contar: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, corre até você, aflito.`,
      pedido: `Oi! Preciso de ${alvo} ${c.item} para a festa e não dou conta sozinho. Você conta e junta comigo?`,
      juntouTudo: `Isso! ${alvo} ${c.item}! Você contou tudo certinho. Leva pra mim, corre!`,
      entrega: `Muito obrigado! Olha — o caminho que estava fechado se abriu pra você. Vai lá!`,
      vitoria: `Você salvou a festa de ${c.nome}! E tem uma nova aventura te esperando adiante…`
    },
    somar: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, olha para umas fichas numeradas, confuso.`,
      pedido: `Cada ficha carrega um número. Preciso que a soma feche EXATAMENTE em ${alvo} — nem mais, nem menos. Quais você escolhe pra fechar essa conta comigo?`,
      juntouTudo: `Exatamente ${alvo}! Você fechou a conta certinha. Traz aqui, rápido!`,
      entrega: `Conta fechada, problema resolvido! Olha — o caminho que estava trancado se abriu. Vai!`,
      vitoria: `Você resolveu o problema de ${c.nome} planejando a soma exata! Uma nova missão te espera adiante…`
    },
    selecionar: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, olha para itens espalhados, sem saber quais servem.`,
      pedido: `Preciso separar SÓ ${regra} — um errado no meio estraga tudo! Quais deles você escolhe pra mim?`,
      juntouTudo: `É isso! Você separou exatamente os que obedecem a regra. Traz aqui!`,
      entrega: `Separação perfeita, problema resolvido! O caminho que estava trancado se abriu. Vai!`,
      vitoria: `Você resolveu o problema de ${c.nome} dominando a regra de verdade! Uma nova missão te espera…`
    },
    ordenar: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, olha para peças fora do lugar, aflito.`,
      pedido: `Preciso das peças ${regra} — uma fora do lugar e desmorona tudo! Qual você pega primeiro?`,
      juntouTudo: `Sequência perfeita! Cada peça no seu lugar. Traz aqui!`,
      entrega: `Tudo em ordem, problema resolvido! O caminho que estava trancado se abriu. Vai!`,
      vitoria: `Você resolveu o problema de ${c.nome} montando a sequência exata! Uma nova missão te espera…`
    },
    // AGRUPAR (criativa): o mundo pede grupos IGUAIS — a criança decide COMO (sem gabarito)
    agrupar: {
      abertura: `Você chega ${c.onde}. ${c.nome}, ${c.papel}, olha para ${c.item} espalhados e umas caixas vazias, aflito.`,
      pedido: `A feira é hoje! Preciso levar ${c.item} arrumados em caixas — e a carroça só viaja se TODAS as caixas tiverem o MESMO tanto. Como você arrumaria pra ficar igualzinho?`,
      juntouTudo: `Olha só… caixas igualzinhas! Me mostra essa arrumação!`,
      entrega: `Carga firme, carroça pronta! O caminho que estava fechado se abriu. Vai!`,
      vitoria: `Você criou uma arrumação de grupos IGUAIS — do seu jeito! Uma nova aventura te espera…`
    }
  }

  const TITULO: Record<string, string> = {
    contar: `${c.nome} e ${c.item}`, somar: `${c.nome} e a conta exata`,
    selecionar: `${c.nome} e a regra dos itens`, ordenar: `${c.nome} e a sequência perdida`,
    agrupar: `${c.nome} e as caixas iguais`
  }
  const r: Roteiro = {
    titulo: TITULO[mecanica],
    sinopse: `${c.nome}, ${c.papel} ${c.onde}, tem um problema que só se resolve com o conteúdo — e só a criança pode ajudar.`,
    personagem: { nome: c.nome, emoji: c.emoji },
    kitId: c.kitId,
    mecanica,
    alvo,
    item: c.item,
    falas: FALAS[mecanica]
  }
  return Roteiro.parse(r)          // valida (inclui a trava do Portão 0)
}
