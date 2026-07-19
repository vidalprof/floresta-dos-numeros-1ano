// ============================================================================
// IA DE CONTEÚDO — quando o professor digita um conteúdo que o banco não conhece
// ("Fotossíntese", "Brasil colônia", "Sistema Solar"...), a IA (Pollinations, grátis,
// roda no NAVEGADOR) gera os itens + a regra NO CONTRATO Zod. Blindado como manda a
// banca da Agenda: fetch com PRAZO (9s), resposta VALIDADA (dado torto não monta),
// rótulos curtos; qualquer falha -> null e o chamador cai no banco (o jogo NUNCA quebra).
// (No container do chat a rede é bloqueada — a IA só roda no navegador real; o QA
//  testa exatamente o caminho do fallback.)
// ============================================================================
import { z } from 'zod'

const rotulo = z.string().min(1).max(16)     // curto: vai desenhado sobre o item no mapa

const RespSelecionar = z.object({
  regra: z.string().min(4).max(60),
  certos: z.array(rotulo).length(3),
  errados: z.array(rotulo).length(3)
})
const RespOrdenar = z.object({
  regra: z.string().min(4).max(60),
  sequencia: z.array(rotulo).min(3).max(5)
})

export interface ConteudoIASel { kc: string, regra: string, certos: string[], errados: string[], reconhecido: true }
export interface ConteudoIAOrd { kc: string, regra: string, sequencia: string[], reconhecido: true }

const slug = (s: string): string =>
  s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 32) || 'conteudo'

function extraiJson (txt: string): unknown {
  const a = txt.indexOf('{'), b = txt.lastIndexOf('}')
  if (a < 0 || b <= a) throw new Error('sem json')
  return JSON.parse(txt.slice(a, b + 1))
}

async function chamaIA (prompt: string): Promise<string | null> {
  try {
    const ctl = new AbortController()
    const t = setTimeout(() => ctl.abort(), 9000)              // prazo: nunca trava o professor
    const r = await fetch('https://text.pollinations.ai/' + encodeURIComponent(prompt), { signal: ctl.signal })
    clearTimeout(t)
    if (!r.ok) return null
    return await r.text()
  } catch { return null }
}

// itens do SELECIONAR para um conteúdo livre (ex.: "as causas da Revolução Francesa")
export async function iaSelecionar (ano: string, disciplina: string, objetivo: string): Promise<ConteudoIASel | null> {
  const prompt =
    `Você é um professor especialista de ${disciplina} (${ano}, BNCC, Brasil). Conteúdo: "${objetivo}". ` +
    'Crie um desafio de SEPARAR itens: uma regra clara e itens que obedecem ou não a ela. ' +
    'Responda SÓ com JSON válido, sem comentários, neste formato exato: ' +
    '{"regra":"os/as ...","certos":["a","b","c"],"errados":["d","e","f"]} — ' +
    'rótulos CURTOS (máx 16 letras), conteúdo CORRETO, distratores plausíveis do mesmo universo, linguagem da idade.'
  const txt = await chamaIA(prompt)
  if (!txt) return null
  try {
    const d = RespSelecionar.parse(extraiJson(txt))
    return { kc: slug(objetivo), regra: d.regra, certos: d.certos, errados: d.errados, reconhecido: true }
  } catch { return null }
}

// sequência do ORDENAR para um conteúdo livre (ex.: "linha do tempo da independência")
export async function iaOrdenar (ano: string, disciplina: string, objetivo: string): Promise<ConteudoIAOrd | null> {
  const prompt =
    `Você é um professor especialista de ${disciplina} (${ano}, BNCC, Brasil). Conteúdo: "${objetivo}". ` +
    'Crie um desafio de ORDENAR: itens que têm uma ordem correta (cronológica, crescente ou de etapas). ' +
    'Responda SÓ com JSON válido, sem comentários, neste formato exato: ' +
    '{"regra":"na ordem ...","sequencia":["1º","2º","3º","4º"]} — a sequência JÁ na ordem certa, ' +
    'rótulos CURTOS (máx 16 letras), conteúdo CORRETO, linguagem da idade.'
  const txt = await chamaIA(prompt)
  if (!txt) return null
  try {
    const d = RespOrdenar.parse(extraiJson(txt))
    return { kc: slug(objetivo), regra: d.regra, sequencia: d.sequencia, reconhecido: true }
  } catch { return null }
}
