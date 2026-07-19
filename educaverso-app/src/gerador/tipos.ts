// ============================================================================
// GERADOR — tipos do authoring (a "hora do professor", com internet).
// Aqui mora o cérebro que transforma a INTENÇÃO pedagógica em MISSÃO jogável.
// Nada disto roda na sala: o professor GERA (pode usar LLM), o aluno JOGA o
// resultado estático, offline, no PC velho. Ver ARQUITETURA-PLATAFORMA-RPG.md.
//
// FILOSOFIA (Portão 0, virada tipo): a missão só nasce de uma MECÂNICA jogável
// do catálogo runtime — nunca de "responda a pergunta". Por isso PlanoMissao
// carrega `mecanica` (id runtime) e `verboDoMundo` (a ação diegética: colher,
// juntar, repartir), não "acerte/erre". O quiz é impossível por construção.
// ============================================================================

// Faixas de ano que a plataforma atende (pré a 9º).
export type Ano =
  | 'pre' | '1ano' | '2ano' | '3ano' | '4ano' | '5ano'
  | '6ano' | '7ano' | '8ano' | '9ano'

export type Dificuldade = 'facil' | 'medio' | 'dificil'

// O ÚNICO formulário que o professor preenche.
export interface BriefingProfessor {
  ano: Ano
  disciplina: string        // 'matematica' | 'portugues' | 'ciencias' | ...
  objetivo: string          // objetivo de aprendizagem (texto livre / BNCC)
  tema: string              // ambientação livre (ex: 'floresta', 'espaço')
  tempoMin: number          // duração alvo da aula (ex: 55)
  dificuldade: Dificuldade
}

// Uma missão já resolvida em termos JOGÁVEIS (o gerador de mapa/diálogo consome).
export interface PlanoMissao {
  mecanica: string          // id da mecânica RUNTIME (tem que existir no catálogo)
  conceito: string          // conceito ensinado, nomeado (ex: 'contagem até 10')
  verboDoMundo: string      // ação diegética: 'colher' | 'juntar' | 'repartir'...
  params: Record<string, any>   // params prontos p/ a mecânica runtime
  problema: string          // 1 frase: o problema do mundo (semente p/ o diálogo)
  recompensaSugerida: string    // item que a missão devolve (ex: 'tabuas')
  bnccPista?: string        // trecho do objetivo que ancorou a escolha (auditoria)
}

// Como uma mecânica pedagógica se descreve e se planeja.
export interface MecanicaPedagogica {
  id: string                // == id da mecânica RUNTIME (contrato)
  titulo: string            // nome humano (ex: 'Contar / quantidade')
  disciplinas: string[]     // disciplinas onde faz sentido
  anos: Ano[]               // faixas onde é adequada
  conceitos: string[]       // conceitos que ensina (nomeados no fim)
  verboDoMundo: string      // a ação diegética padrão
  gatilhos: RegExp[]        // pistas no objetivo que acionam esta mecânica
  // devolve a missão pronta (params + problema-semente) a partir do briefing.
  planejar (b: BriefingProfessor): PlanoMissao
}
