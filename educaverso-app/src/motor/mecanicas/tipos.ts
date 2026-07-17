// ============================================================================
// CATÁLOGO DE MECÂNICAS (o "LEGO" jogável do EduVerse).
// Cada mecânica é uma peça reutilizável que PLUGA no gancho do Montador
// (Mundo.abreMecanica). Trocar a atividade = trocar os DADOS; a mesma mecânica
// serve qualquer tema (contar galinhas hoje, contar estrelas amanhã).
// FILOSOFIA (Portão 0): o problema vem primeiro, o Byte PERGUNTA (não corrige),
// o erro é CONSEQUÊNCIA (conte de novo), o conceito é nomeado só no fim.
// ============================================================================
import Phaser from 'phaser'

export interface CtxMecanica {
  scene: Phaser.Scene
  params: Record<string, any>          // params livres da parada (dos DADOS)
  paradaId: string
  cor: string                          // cor-tema da parada (do roteiro)
  // fala com a voz do Byte (Antonio) — reaproveita o balão do Mundo
  falar: (id: string, aoFim?: () => void) => void
  temAudio: (id: string) => boolean
  // chamado quando a criança CONCLUI a mecânica (volta a explorar)
  aoConcluir: (sucesso: boolean) => void
}

export interface Mecanica {
  id: string
  montar (ctx: CtxMecanica): void
}
