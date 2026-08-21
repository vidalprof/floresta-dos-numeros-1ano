// ============================================================================
// REGISTRO das mecânicas (o catálogo). O Montador pergunta aqui pela id da
// mecânica da parada e recebe a peça pronta. Adicionar mecânica nova =
// escrever o módulo + registrar 1 linha aqui (o resto do motor não muda).
// ============================================================================
import type { Mecanica, CtxMecanica } from './tipos'
import { Contar } from './contar'
import { IDS_MECANICAS, idRegistrado } from './registro-ids'

const CATALOGO: Record<string, Mecanica> = {
  [Contar.id]: Contar
}

// Consistência dev: o registro-ids (a "lista da verdade", leve) e o CATALOGO
// (as peças reais) têm que bater. Se divergirem, o gerador poderia prometer uma
// mecânica que o motor não tem (ou vice-versa) — o alerta cedo evita isso.
if (import.meta.env?.DEV) {
  const doCatalogo = Object.keys(CATALOGO).sort().join(',')
  const doRegistro = [...IDS_MECANICAS].sort().join(',')
  if (doCatalogo !== doRegistro) {
    console.warn(`[mecanicas] registro-ids (${doRegistro}) != CATALOGO (${doCatalogo}) — sincronize`)
  }
}

export function temMecanica (id: string): boolean { return !!CATALOGO[id] && idRegistrado(id) }

export function abrir (id: string, ctx: CtxMecanica): boolean {
  const m = CATALOGO[id]
  if (!m) return false
  m.montar(ctx)
  return true
}

export type { Mecanica, CtxMecanica }
