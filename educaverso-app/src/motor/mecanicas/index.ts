// ============================================================================
// REGISTRO das mecânicas (o catálogo). O Montador pergunta aqui pela id da
// mecânica da parada e recebe a peça pronta. Adicionar mecânica nova =
// escrever o módulo + registrar 1 linha aqui (o resto do motor não muda).
// ============================================================================
import type { Mecanica, CtxMecanica } from './tipos'
import { Contar } from './contar'

const CATALOGO: Record<string, Mecanica> = {
  [Contar.id]: Contar
}

export function temMecanica (id: string): boolean { return !!CATALOGO[id] }

export function abrir (id: string, ctx: CtxMecanica): boolean {
  const m = CATALOGO[id]
  if (!m) return false
  m.montar(ctx)
  return true
}

export type { Mecanica, CtxMecanica }
