// ============================================================================
// MOTOR ADAPTATIVO — a camada que ADAPTA ao ritmo e MEDE o domínio (barato e leve,
// roda no navegador, estado em localStorage/Firebase). Base científica:
// MODELO-APRENDIZAGEM-EDUCAVERSO.md — BKT-lite (domínio por KC), DDA na ZDP (dificuldade
// no ponto ~70-85% de acerto) e Leitner (revisão espaçada p/ fixar).
// Tudo em FUNÇÕES PURAS (testáveis sem navegador) + um armazém leve por criança.
// ============================================================================

// ---- 1) BKT-LITE: "a criança já domina este KC?" (Bayesian Knowledge Tracing) ----
export interface ParamsBKT { pT: number, pG: number, pS: number }   // aprende / chute / escorregão
export const BKT_PADRAO: ParamsBKT = { pT: 0.25, pG: 0.2, pS: 0.1 }
export const MASTERY = 0.95

// atualiza P(domina) após UMA resposta (acertou?), pela regra de Bayes + passo de aprendizagem
export function atualizaBKT (pKnown: number, acertou: boolean, p: ParamsBKT = BKT_PADRAO): number {
  const pk = Math.min(0.9999, Math.max(0.0001, pKnown))
  const post = acertou
    ? (pk * (1 - p.pS)) / (pk * (1 - p.pS) + (1 - pk) * p.pG)
    : (pk * p.pS) / (pk * p.pS + (1 - pk) * (1 - p.pG))
  return post + (1 - post) * p.pT            // depois de observar, a criança pode ter APRENDIDO no passo
}
export const domina = (pKnown: number): boolean => pKnown >= MASTERY

// ---- 2) DDA: escolher a DIFICULDADE (o alvo) na ZDP (~70-85% de chance de acerto) ----
// mantém a criança na "luta produtiva": subiu de nível com folga -> sobe o alvo; travou -> desce.
export function proximoAlvo (alvoAtual: number, pKnown: number, acertouLimpo: boolean, min = 2, max = 9): number {
  let a = alvoAtual
  if (acertouLimpo && pKnown >= 0.8) a += 1        // dominou com folga -> desafio maior
  else if (!acertouLimpo && pKnown < 0.5) a -= 1   // travou -> degrau menor (mais andaime)
  return Math.max(min, Math.min(max, a))
}

// ---- 3) LEITNER: revisão espaçada (traz de volta o KC no dia certo p/ FIXAR) ----
export const INTERVALOS_DIAS = [1, 2, 4, 7, 15, 30] as const
export function proximaCaixa (caixa: number, acertou: boolean): number {
  return acertou ? Math.min(INTERVALOS_DIAS.length - 1, caixa + 1) : 0   // errou volta pra caixa 0
}
export const intervaloDias = (caixa: number): number => INTERVALOS_DIAS[Math.max(0, Math.min(INTERVALOS_DIAS.length - 1, caixa))]
// quando revisar de novo (ms). agora e umDia entram como parâmetro p/ ser PURO/testável.
export function proximaRevisao (caixa: number, acertou: boolean, agora: number, umDiaMs = 86400000): number {
  return agora + intervaloDias(proximaCaixa(caixa, acertou)) * umDiaMs
}

// ---- 4) ARMAZÉM por criança (leve; localStorage agora, Firebase depois) ----
export interface ProgressoKC { pKnown: number, caixa: number, proximaRevisao: number, tentativas: number, acertos: number }
export type Progresso = Record<string, ProgressoKC>   // chave = kc

const kcNovo = (): ProgressoKC => ({ pKnown: 0.3, caixa: 0, proximaRevisao: 0, tentativas: 0, acertos: 0 })

// registra UMA observação (a criança respondeu ao KC) e devolve o progresso atualizado (imutável)
export function registra (prog: Progresso, kc: string, acertou: boolean, agora: number): Progresso {
  const at = prog[kc] ?? kcNovo()
  const novo: ProgressoKC = {
    pKnown: atualizaBKT(at.pKnown, acertou),
    caixa: proximaCaixa(at.caixa, acertou),
    proximaRevisao: proximaRevisao(at.caixa, acertou, agora),
    tentativas: at.tentativas + 1,
    acertos: at.acertos + (acertou ? 1 : 0)
  }
  return { ...prog, [kc]: novo }
}
// KCs cuja revisão venceu (para gerar "missões de retorno" espaçadas)
export const kcsParaRevisar = (prog: Progresso, agora: number): string[] =>
  Object.keys(prog).filter(k => prog[k].proximaRevisao > 0 && prog[k].proximaRevisao <= agora)

// persistência protegida (PC com armazenamento bloqueado não pode dar tela branca)
const CHAVE = 'educ_progresso_'
export function carrega (alunoId: string): Progresso {
  try { const s = localStorage.getItem(CHAVE + alunoId); return s ? JSON.parse(s) : {} } catch { return {} }
}
export function salva (alunoId: string, prog: Progresso): void {
  try { localStorage.setItem(CHAVE + alunoId, JSON.stringify(prog)) } catch { /* sem storage: segue sem persistir */ }
}
