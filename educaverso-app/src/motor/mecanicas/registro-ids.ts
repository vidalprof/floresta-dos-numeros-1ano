// ============================================================================
// REGISTRO-IDS — a "lista da verdade" das mecânicas que o motor sabe jogar.
// Módulo LEVE de propósito (zero Phaser): tanto o catálogo runtime (index.ts)
// quanto o catálogo pedagógico do gerador leem daqui. Assim a TRAVA DO PORTÃO 0
// (o gerador só emite missão que vira jogo) é verificável sem carregar o motor.
// Adicionar mecânica jogável = incluir o id aqui + registrar em index.ts.
// ============================================================================
export const IDS_MECANICAS = ['contar'] as const
export type IdMecanica = typeof IDS_MECANICAS[number]

export function idRegistrado (id: string): boolean {
  return (IDS_MECANICAS as readonly string[]).includes(id)
}
