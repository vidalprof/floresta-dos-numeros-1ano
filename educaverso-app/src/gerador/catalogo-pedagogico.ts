// ============================================================================
// CATÁLOGO PEDAGÓGICO — o cérebro do gerador (o que faz disto "o Canva").
// Mapeia OBJETIVO DE APRENDIZAGEM -> CONCEITO -> MECÂNICA JOGÁVEL -> PARÂMETROS.
//
// 🔒 TRAVA DO PORTÃO 0 (a mais importante da plataforma):
//   `mecanicasDisponiveis()` só devolve uma mecânica pedagógica se o MOTOR
//   souber jogá-la (`temMecanica(id)` do catálogo runtime). Assim o gerador é
//   ESTRUTURALMENTE incapaz de emitir uma missão que não vira jogo — e, como
//   toda missão é um VERBO DO MUNDO (colher/juntar/repartir), nunca vira quiz.
//
// Crescer a plataforma = (1) escrever a mecânica runtime + (2) registrar a
// entrada pedagógica aqui. O resto do gerador não muda.
// ============================================================================
import { idRegistrado } from '../motor/mecanicas/registro-ids'
import type {
  BriefingProfessor, MecanicaPedagogica, PlanoMissao, Ano, Dificuldade
} from './tipos'

// --- utilidades de dificuldade -------------------------------------------
// Faixa de quantidade por dificuldade (contagem). Cresce com o ano também.
function faixaQuantidade (dif: Dificuldade, ano: Ano): [number, number] {
  const base: Record<Dificuldade, [number, number]> = {
    facil: [3, 5], medio: [6, 10], dificil: [11, 20]
  }
  const [lo, hi] = base[dif]
  // pré/1º ano seguram o teto baixo mesmo no "difícil" (respeita a idade)
  if (ano === 'pre') return [Math.min(lo, 3), Math.min(hi, 6)]
  if (ano === '1ano') return [lo, Math.min(hi, 10)]
  return [lo, hi]
}

// escolhe um valor estável dentro da faixa (sem Math.random p/ ser reprodutível;
// varia pelo comprimento do tema, então temas diferentes geram números diferentes)
function valorNaFaixa ([lo, hi]: [number, number], semente: string): number {
  const s = Array.from(semente).reduce((a, c) => a + c.charCodeAt(0), 0)
  return lo + (s % (hi - lo + 1))
}

// --- ENTRADAS DO CATÁLOGO -------------------------------------------------
// (por enquanto só 'contar' tem mecânica runtime; cada nova mecânica jogável
//  ganha aqui sua entrada pedagógica. NÃO inventar entrada sem runtime.)

const Contar: MecanicaPedagogica = {
  id: 'contar',
  titulo: 'Contar / quantidade',
  disciplinas: ['matematica'],
  anos: ['pre', '1ano', '2ano', '3ano'],
  conceitos: ['contagem', 'quantidade', 'correspondência um-a-um', 'numeral'],
  verboDoMundo: 'colher',
  gatilhos: [
    /cont(a|ar|agem|e)\b/i, /quant(os|as|idade)/i, /numeral/i,
    /n[uú]mer(o|os)\b/i, /at[eé]\s*\d+/i, /correspond[eê]ncia/i
  ],
  planejar (b: BriefingProfessor): PlanoMissao {
    const quantidade = valorNaFaixa(faixaQuantidade(b.dificuldade, b.ano), b.tema + b.objetivo)
    const teto = quantidade <= 10 ? 10 : quantidade <= 20 ? 20 : 30
    return {
      mecanica: 'contar',
      conceito: `contagem até ${teto}`,
      verboDoMundo: 'colher',
      params: { quantidade, max: teto },
      problema: `algo no mundo precisa de exatamente ${quantidade} — quantos o herói consegue juntar?`,
      recompensaSugerida: 'itens_coletados',
      bnccPista: (b.objetivo.match(/[^.;]*\b(cont|quant|numeral|n[uú]mer)[^.;]*/i) || [''])[0].trim()
    }
  }
}

// registro bruto (antes da trava). Adicionar mecânica nova = +1 linha aqui.
const BRUTO: MecanicaPedagogica[] = [Contar]

// --- API do catálogo ------------------------------------------------------

// Só as mecânicas pedagógicas que o MOTOR sabe jogar (Portão 0, por construção).
export function mecanicasDisponiveis (): MecanicaPedagogica[] {
  return BRUTO.filter(m => idRegistrado(m.id))
}

// Quantos gatilhos do CONCEITO aparecem no objetivo/tema. A qualificação é por
// AQUI (o conceito tem que ser invocado) — nunca por idade/disciplina soltas:
// senão uma mecânica de matemática "casaria" com um objetivo de história só
// porque o ano bate. O conceito manda; disciplina e ano só desempatam.
function gatilhosAcionados (m: MecanicaPedagogica, b: BriefingProfessor): number {
  const alvo = `${b.objetivo} ${b.tema}`
  let n = 0
  for (const g of m.gatilhos) if (g.test(alvo)) n++
  return n
}

// pontua p/ ORDENAR entre as já qualificadas (mais gatilhos > disciplina > ano)
function pontua (m: MecanicaPedagogica, b: BriefingProfessor): number {
  let p = gatilhosAcionados(m, b) * 2
  if (m.disciplinas.includes(b.disciplina)) p += 3
  if (m.anos.includes(b.ano)) p += 2
  return p
}

// Escolhe as mecânicas adequadas ao briefing (ordenadas). QUALIFICA só quem tem
// o CONCEITO invocado (≥1 gatilho). Vazio = nenhuma mecânica jogável cobre este
// objetivo AINDA — o gerador avisa com honestidade, nunca inventa um quiz.
export function escolherMecanicas (b: BriefingProfessor): MecanicaPedagogica[] {
  return mecanicasDisponiveis()
    .filter(m => gatilhosAcionados(m, b) > 0)
    .sort((a, z) => pontua(z, b) - pontua(a, b))
}

// Planeja as missões da aventura a partir do briefing. `quantasMissoes` é
// derivado do tempo da aula (mais tempo = mais missões), com teto são p/ crianças.
export function planejarMissoes (b: BriefingProfessor): PlanoMissao[] {
  const cands = escolherMecanicas(b)
  if (!cands.length) return []
  const alvo = Math.max(1, Math.min(4, Math.round(b.tempoMin / 20))) // ~1 missão / 20min
  const planos: PlanoMissao[] = []
  for (let i = 0; i < alvo; i++) {
    // cicla entre as mecânicas candidatas p/ variar a aventura
    planos.push(cands[i % cands.length].planejar(b))
  }
  return planos
}
