// ============================================================================
// O PEDAGOGO — planeja a APRENDIZAGEM ANTES do roteirista (a ordem que o Marcos exige).
// Dado (ano, disciplina, objetivo/CONTEÚDO), entrega a "ESPINHA DE APRENDIZAGEM": a
// progressão CPA, a DINÂMICA de fundo (resolver/ordenar/coletar — NUNCA quiz raso), o
// CONTEÚDO jogável (itens + regra), a necessidade do mundo e COMO MEDIR (erros reais +
// transferência). O roteirista depois só VESTE de história.
//
// ARQUITETURA (pedido do Marcos: "o conteúdo varia; nem tudo é soma"): as mecânicas são
// MOTORES GENÉRICOS parametrizados por CONTEÚDO —
//   contar      -> quantidade exata (Pré–2º)
//   somar       -> combinação que fecha a soma exata (operações)
//   selecionar  -> só os itens que obedecem a REGRA do conteúdo (múltiplos, frações
//                  equivalentes, substantivos, primos… UM motor, infinitos conteúdos)
//   ordenar     -> coletar na SEQUÊNCIA certa (crescente, etapas, linha do tempo)
// v1 gera o conteúdo por regra (banco); a IA entra trocando SÓ gerarConteudo*, sem tocar
// no motor. Base: MODELO-APRENDIZAGEM-EDUCAVERSO.md (ZDP, CPA, LM-GM, integração intrínseca).
// ============================================================================
import { z } from 'zod'
import type { PedidoAtividade } from './tipos'
import { DIFICULDADES } from './tipos'
// import ESTÁTICO (dinâmico geraria chunk separado e quebraria o publish de 1 arquivo)
import { iaSelecionar, iaOrdenar } from './ia-conteudo'

export const DINAMICAS = ['resolver', 'criar', 'investigar', 'coletar', 'narrar', 'simular'] as const
// agrupar = a 1ª mecânica CRIATIVA (lei dos GRUPOS IGUAIS): a criança CRIA a arrumação
// (decide QUANTAS caixas usa e como reparte) — sem gabarito, várias arrumações vencem.
export const MECANICAS = ['contar', 'somar', 'selecionar', 'ordenar', 'agrupar'] as const
export type Mecanica = typeof MECANICAS[number]

// um sub-passo da progressão, marcado no eixo CPA (concreto→pictórico→abstrato)
export const Passo = z.object({
  kc: z.string().min(2),
  cpa: z.enum(['concreto', 'pictorico', 'abstrato']),
  descricao: z.string().min(3)
})

// um item jogável do CONTEÚDO (rótulo visível; ok = obedece a regra; ordem p/ sequência)
export const Item = z.object({
  rotulo: z.string().min(1),
  ok: z.boolean(),
  ordem: z.number().int().optional()
})
export type Item = z.infer<typeof Item>

export const Espinha = z.object({
  ano: z.string().min(1),
  disciplina: z.string().min(2),
  objetivo: z.string().min(3),
  dinamica: z.enum(DINAMICAS),
  mecanica: z.enum(MECANICAS),
  kc: z.string().min(2),                        // domínio é POR CONTEÚDO (ex.: "multiplos-3")
  alvo: z.number().int().min(2).max(9),          // contar: quantos juntar
  alvoSoma: z.number().int().min(6).max(20).optional(),   // somar: a soma exata
  regra: z.string().optional(),                 // selecionar/ordenar: a regra do conteúdo (texto)
  itens: z.array(Item).min(2).optional(),       // selecionar/ordenar: os itens rotulados
  agTotal: z.number().int().min(4).max(24).optional(),   // agrupar: total de itens a repartir
  agCaixas: z.number().int().min(2).max(8).optional(),   // agrupar: máximo de caixas disponíveis
  progressao: z.array(Passo).min(1),
  necessidadeMundo: z.string().min(5),
  medir: z.string().min(5)
})
export type Espinha = z.infer<typeof Espinha>

const ALVO: Record<typeof DIFICULDADES[number], number> = { facil: 3, medio: 5, dificil: 7 }
export const TIERS_SOMA = [8, 12, 18] as const
const ALVO_SOMA: Record<typeof DIFICULDADES[number], number> = { facil: 8, medio: 12, dificil: 18 }

// ---------------------------------------------------------------------------
// ESCOLHA da mecânica: primeiro pelo CONTEÚDO (o verbo/assunto do objetivo), depois
// pelo ano. Quiz nunca é opção.
// ---------------------------------------------------------------------------
function escolherMecanica (pedido: PedidoAtividade): Mecanica {
  const s = pedido.objetivo.toLowerCase()
  const anoNum = parseInt(pedido.ano) || 0                       // "Pré" -> 0, "6º ano" -> 6
  // tabuada/multiplicação = GRUPOS IGUAIS (a ideia-mãe) -> a mecânica CRIATIVA agrupar
  if (/tabuada|multiplica|vezes\b|grupos? igua|dobro|triplo/.test(s)) return 'agrupar'
  if (/orden|sequ[eê]n|crescente|decrescente|linha do tempo|etapa/.test(s)) return 'ordenar'
  if (/m[úu]ltipl|fra[çc]|equivalent|substantiv|adjetiv|primo|par(es)?\b|classific|identifi|selecion|separ/.test(s)) return 'selecionar'
  if (/som(a|ar)|adi[çc]|opera[çc]|c[aá]lcul/.test(s)) return 'somar'
  if (anoNum >= 6) return 'selecionar'          // anos finais: resolver pela REGRA do conteúdo
  if (anoNum >= 3) return 'somar'
  return 'contar'
}

// ---------------------------------------------------------------------------
// GERADORES DE CONTEÚDO (v1 por banco/regra — é AQUI que a IA entra depois, gerando
// itens+regra para QUALQUER conteúdo do professor, sem tocar no motor)
// ---------------------------------------------------------------------------
export interface Conteudo { kc: string, regra: string, certos: string[], errados: string[], reconhecido: boolean }

export function gerarConteudoSelecionar (objetivo: string): Conteudo {
  const s = objetivo.toLowerCase()
  if (/m[úu]ltipl/.test(s)) {
    const n = Math.max(2, parseInt((s.match(/m[úu]ltiplos? de (\d+)/) || [])[1] || '3') || 3)
    return { kc: `multiplos-${n}`, regra: `os múltiplos de ${n}`, certos: [String(n * 2), String(n * 4), String(n * 5)], errados: [String(n * 2 + 1), String(n * 3 + 1), String(n * 4 + 1)], reconhecido: true }
  }
  if (/fra[çc]|equivalent/.test(s)) return { kc: 'fracoes-equivalentes', regra: 'as frações equivalentes a 1/2', certos: ['2/4', '3/6', '4/8'], errados: ['2/3', '3/4', '5/8'], reconhecido: true }
  if (/substantiv/.test(s)) return { kc: 'substantivos', regra: 'os substantivos', certos: ['casa', 'rio', 'flor'], errados: ['correr', 'bonito', 'ontem'], reconhecido: true }
  if (/adjetiv/.test(s)) return { kc: 'adjetivos', regra: 'os adjetivos', certos: ['alto', 'veloz', 'doce'], errados: ['pular', 'mesa', 'hoje'], reconhecido: true }
  if (/primo/.test(s)) return { kc: 'numeros-primos', regra: 'os números primos', certos: ['2', '5', '7'], errados: ['4', '6', '9'], reconhecido: true }
  if (/[íi]mpar/.test(s)) return { kc: 'numeros-impares', regra: 'os números ímpares', certos: ['3', '7', '11'], errados: ['4', '8', '12'], reconhecido: true }
  // HISTÓRIA (banco curado — a IA cobre o resto dos conteúdos)
  if (/revolu[çc][ãa]o francesa/.test(s)) return { kc: 'revolucao-francesa-causas', regra: 'as CAUSAS da Revolução Francesa', certos: ['Fome e crise', 'Impostos altos', 'Iluminismo'], errados: ['Guerra Fria', 'Chegada de Cabral', 'Roma Antiga'], reconhecido: true }
  return { kc: 'numeros-pares', regra: 'os números pares', certos: ['2', '6', '10'], errados: ['3', '7', '11'], reconhecido: false }
}

export interface ConteudoOrdem { kc: string, regra: string, sequencia: string[], reconhecido: boolean }

export function gerarConteudoOrdenar (objetivo: string): ConteudoOrdem {
  const s = objetivo.toLowerCase()
  if (/revolu[çc][ãa]o francesa/.test(s)) return { kc: 'revolucao-francesa-tempo', regra: 'na ordem em que aconteceram (linha do tempo da Revolução Francesa)', sequencia: ['Bastilha', 'Direitos', 'República', 'Napoleão'], reconhecido: true }
  if (/decrescente/.test(s)) return { kc: 'ordem-decrescente', regra: 'em ordem DECRESCENTE (do maior ao menor)', sequencia: ['25', '16', '9', '4'], reconhecido: true }
  if (/fra[çc]/.test(s)) return { kc: 'ordem-fracoes', regra: 'da menor para a maior fração', sequencia: ['1/8', '1/4', '1/2', '3/4'], reconhecido: true }
  return { kc: 'ordem-crescente', regra: 'em ordem CRESCENTE (do menor ao maior)', sequencia: ['4', '9', '16', '25'], reconhecido: false }
}

// embaralha determinístico (o QA reproduz): permutação fixa por tamanho
const PERM: Record<number, number[]> = { 4: [2, 0, 3, 1], 6: [3, 0, 4, 1, 5, 2] }
function intercala (certos: string[], errados: string[]): Item[] {
  const base: Item[] = [
    ...certos.map(r => ({ rotulo: r, ok: true })),
    ...errados.map(r => ({ rotulo: r, ok: false }))
  ]
  const p = PERM[base.length] ?? base.map((_, i) => i)
  return p.map(i => base[i])
}

// ---------------------------------------------------------------------------
// O PEDAGOGO
// ---------------------------------------------------------------------------
export function planejarPedagogia (pedido: PedidoAtividade): Espinha {
  const mecanica = escolherMecanica(pedido)
  if (mecanica === 'agrupar') return planejarAgrupar(pedido)
  if (mecanica === 'somar') return planejarSomar(pedido)
  if (mecanica === 'selecionar') return planejarSelecionar(pedido)
  if (mecanica === 'ordenar') return planejarOrdenar(pedido)
  return planejarContar(pedido)
}

// Versão com IA: se o BANCO reconhece o conteúdo, usa o banco (instantâneo e exato).
// Se NÃO reconhece (ex.: "Fotossíntese"), pede à IA os itens NO CONTRATO; se a IA
// falhar/timeout, cai no banco genérico — o professor NUNCA fica sem atividade.
export async function planejarPedagogiaIA (pedido: PedidoAtividade): Promise<{ espinha: Espinha, viaIA: boolean }> {
  const mecanica = escolherMecanica(pedido)
  if (mecanica === 'selecionar') {
    const banco = gerarConteudoSelecionar(pedido.objetivo)
    if (!banco.reconhecido) {
      const ia = await iaSelecionar(pedido.ano, pedido.disciplina, pedido.objetivo)
      if (ia) return { espinha: planejarSelecionar(pedido, ia), viaIA: true }
    }
    return { espinha: planejarSelecionar(pedido, banco), viaIA: false }
  }
  if (mecanica === 'ordenar') {
    const banco = gerarConteudoOrdenar(pedido.objetivo)
    if (!banco.reconhecido) {
      const ia = await iaOrdenar(pedido.ano, pedido.disciplina, pedido.objetivo)
      if (ia) return { espinha: planejarOrdenar(pedido, ia), viaIA: true }
    }
    return { espinha: planejarOrdenar(pedido, banco), viaIA: false }
  }
  return { espinha: planejarPedagogia(pedido), viaIA: false }
}

// AGRUPAR — a mecânica CRIATIVA (tabuada = GRUPOS IGUAIS). Sem gabarito: a LEI do mundo
// julga QUALQUER arrumação (todas as caixas com o mesmo tanto). 2×6, 3×4, 4×3, 6×2… vencem.
const ALVO_AGRUPAR: Record<typeof DIFICULDADES[number], { total: number, caixas: number }> = {
  facil: { total: 8, caixas: 4 }, medio: { total: 12, caixas: 6 }, dificil: { total: 18, caixas: 6 }
}
export const TIERS_AGRUPAR = [8, 12, 18] as const
function planejarAgrupar (pedido: PedidoAtividade): Espinha {
  const a = ALVO_AGRUPAR[pedido.dificuldade]
  return Espinha.parse({
    ano: pedido.ano, disciplina: pedido.disciplina, objetivo: pedido.objetivo,
    dinamica: 'criar', mecanica: 'agrupar', kc: 'grupos-iguais',
    alvo: ALVO[pedido.dificuldade], agTotal: a.total, agCaixas: a.caixas,
    regra: 'todas as caixas com o MESMO tanto',
    progressao: [
      { kc: 'repartir concreto', cpa: 'concreto', descricao: `distribuir ${a.total} itens em caixas, um a um, com as mãos` },
      { kc: 'grupos iguais', cpa: 'pictorico', descricao: 'VER que grupos iguais são justos — e que a caixa diferente tomba' },
      { kc: 'nomear a multiplicação', cpa: 'abstrato', descricao: 'só no FIM: "n grupos de k" tem nome — n×k (a arrumação DELA)' }
    ],
    necessidadeMundo: `a carga só viaja se TODAS as caixas tiverem o mesmo tanto — desigual, a caixa tomba; a criança CRIA a arrumação (não há resposta única)`,
    medir: 'os testes reais (desigual = observação negativa; igual = positiva) + vencer com OUTRA arrumação depois (transferência: qualquer divisor serve)'
  })
}

function planejarContar (pedido: PedidoAtividade): Espinha {
  const alvo = ALVO[pedido.dificuldade]
  return Espinha.parse({
    ano: pedido.ano, disciplina: pedido.disciplina, objetivo: pedido.objetivo,
    dinamica: 'coletar', mecanica: 'contar', kc: 'contar', alvo,
    progressao: [
      { kc: 'correspondência 1-a-1', cpa: 'concreto', descricao: `juntar ${alvo} objetos, um a um, tocando cada um` },
      { kc: 'cardinalidade', cpa: 'pictorico', descricao: `saber que o último contado diz QUANTOS há (${alvo})` },
      { kc: 'reconhecer a quantidade', cpa: 'abstrato', descricao: `associar a coleção ao número ${alvo}` }
    ],
    necessidadeMundo: `alguém no mundo precisa de exatamente ${alvo} de algo para resolver um problema real — e só contando/juntando certo isso se resolve`,
    medir: 'dar à criança uma coleção NOVA e ver se ela conta e diz corretamente quantos há (transferência), não só repetir a fase'
  })
}

function planejarSomar (pedido: PedidoAtividade): Espinha {
  const alvoSoma = ALVO_SOMA[pedido.dificuldade]
  return Espinha.parse({
    ano: pedido.ano, disciplina: pedido.disciplina, objetivo: pedido.objetivo,
    dinamica: 'resolver', mecanica: 'somar', kc: 'somar', alvo: ALVO[pedido.dificuldade], alvoSoma,
    progressao: [
      { kc: 'valor das partes', cpa: 'concreto', descricao: 'cada item carrega um NÚMERO — pegar é somar de verdade' },
      { kc: 'soma parcial', cpa: 'pictorico', descricao: `acompanhar quanto já juntou rumo a ${alvoSoma} (quanto falta?)` },
      { kc: 'planejar a combinação', cpa: 'abstrato', descricao: `escolher QUAIS itens fecham exatamente ${alvoSoma} — passou, recomeça` }
    ],
    necessidadeMundo: `alguém precisa de itens que juntos somem EXATAMENTE ${alvoSoma} — passou ou faltou, o problema não se resolve; só a combinação certa salva`,
    medir: 'observar os ERROS reais (passar do alvo) e se a criança fecha a soma com valores NOVOS na fase seguinte (transferência)'
  })
}

// SELECIONAR sob a REGRA do conteúdo — um motor, infinitos conteúdos.
// `conteudo` externo (vindo da IA) substitui o banco quando fornecido.
function planejarSelecionar (pedido: PedidoAtividade, conteudo?: Conteudo): Espinha {
  const c = conteudo ?? gerarConteudoSelecionar(pedido.objetivo)
  return Espinha.parse({
    ano: pedido.ano, disciplina: pedido.disciplina, objetivo: pedido.objetivo,
    dinamica: 'resolver', mecanica: 'selecionar', kc: c.kc, alvo: ALVO[pedido.dificuldade],
    regra: c.regra, itens: intercala(c.certos, c.errados),
    progressao: [
      { kc: 'ler cada item', cpa: 'concreto', descricao: 'cada item do mundo carrega um rótulo do conteúdo' },
      { kc: 'testar contra a regra', cpa: 'pictorico', descricao: `perguntar de cada um: entra em "${c.regra}"?` },
      { kc: 'justificar a escolha', cpa: 'abstrato', descricao: 'saber POR QUE entra (ou não) — o mentor pergunta' }
    ],
    necessidadeMundo: `alguém precisa separar SÓ ${c.regra} — um item errado no meio estraga tudo; só quem domina a regra resolve`,
    medir: 'os ERROS reais (pegar item fora da regra) + separar itens NOVOS da mesma regra na fase seguinte (transferência)'
  })
}

// ORDENAR — coletar na SEQUÊNCIA certa (fora de ordem = erro real).
function planejarOrdenar (pedido: PedidoAtividade, conteudo?: ConteudoOrdem): Espinha {
  const c = conteudo ?? gerarConteudoOrdenar(pedido.objetivo)
  const itens: Item[] = c.sequencia.map((r, i) => ({ rotulo: r, ok: true, ordem: i + 1 }))
  return Espinha.parse({
    ano: pedido.ano, disciplina: pedido.disciplina, objetivo: pedido.objetivo,
    dinamica: 'resolver', mecanica: 'ordenar', kc: c.kc, alvo: ALVO[pedido.dificuldade],
    regra: c.regra, itens,
    progressao: [
      { kc: 'comparar itens', cpa: 'concreto', descricao: 'olhar dois itens e decidir qual vem antes' },
      { kc: 'construir a sequência', cpa: 'pictorico', descricao: `montar a fila ${c.regra}, um passo por vez` },
      { kc: 'antecipar o próximo', cpa: 'abstrato', descricao: 'saber o que vem a seguir SEM testar um por um' }
    ],
    necessidadeMundo: `alguém precisa das peças ${c.regra} — uma fora do lugar e tudo desmorona; só a sequência exata funciona`,
    medir: 'os ERROS reais (pegar fora da ordem) + ordenar uma sequência NOVA na fase seguinte (transferência)'
  })
}
