// ============================================================================
// EVIDÊNCIAS — a camada PROVA do EducaVerso (stealth assessment, Shute/ECD).
// O jogo observa (sem prova visível) e grava EVIDÊNCIA por habilidade no Firebase
// (mesma infra da agenda; gaveta própria /educaverso). O andaime gradual vira uma
// RÉGUA DE AUTONOMIA: acertou sem ajuda > após pergunta > após o gesto ensinado —
// que mapeia direto na rubrica BNCC (Consolidado / Em desenvolvimento / Iniciando).
// LGPD: só o professor-admin LÊ (regra usa /agenda/vidal-ramos/admins); a escrita
// é por login anônimo. Offline/sem regra: fila local + espelho local (nada trava).
// ============================================================================

const API_KEY = 'AIzaSyCWX-lK7pr6yW_E5jDvDhVewe20lB3E6Ks'
const DB = 'https://atividades-educativas-16860-default-rtdb.firebaseio.com'
export const RAIZ = '/educaverso/vidal-ramos/evidencias'

export interface Aluno { nome: string, turma: string, avatar?: 'heroi' | 'menina' }
export interface Evidencia {
  nome: string, turma: string
  kc: string, atividade: string, mecanica: string
  estrategia?: string          // ex.: "3×4" — QUAL arrumação a criança criou
  alvo: number                 // tamanho do desafio (total de itens etc.)
  tentativas: number           // vezes que mostrou ao mentor (erros + 1)
  erros: number
  nivelAjuda: 0 | 1 | 2        // 0=sem ajuda; 1=pergunta reflexiva/botão; 2=gesto ensinado
  ajudaCliques: number
  duracaoSeg: number
  pKnown: number               // estimativa BKT do domínio APÓS a missão
  quando: string               // ISO
}

const K_ALUNO = 'educ_aluno'
const K_FILA = 'educ_evid_fila'
const K_LOCAL = 'educ_evid_local'
const K_TOKEN = 'educ_anon_token'

const ls = {
  get (k: string): string | null { try { return localStorage.getItem(k) } catch { return null } },
  set (k: string, v: string): void { try { localStorage.setItem(k, v) } catch { /* sem storage */ } }
}

export function getAluno (): Aluno | null {
  const s = ls.get(K_ALUNO)
  if (!s) return null
  try { const a = JSON.parse(s); return a?.nome ? a : null } catch { return null }
}
export function setAluno (a: Aluno): void { ls.set(K_ALUNO, JSON.stringify(a)) }

export const san = (s: string): string =>
  s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'x'

// fetch com prazo (lição da agenda: TODO fetch tem prazo)
async function fx (url: string, opts?: RequestInit, ms = 8000): Promise<Response> {
  const ctl = new AbortController()
  const t = setTimeout(() => ctl.abort(), ms)
  try { return await fetch(url, { ...opts, signal: ctl.signal }) } finally { clearTimeout(t) }
}

// login ANÔNIMO (Firebase Auth REST) — o crachá para as regras aceitarem a escrita
async function tokenAnonimo (): Promise<string | null> {
  const cache = ls.get(K_TOKEN)
  if (cache) {
    try { const c = JSON.parse(cache); if (c.exp > Date.now()) return c.tok } catch { /* renova */ }
  }
  try {
    const r = await fx(`https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${API_KEY}`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ returnSecureToken: true }) })
    if (!r.ok) return null
    const j = await r.json()
    if (!j.idToken) return null
    ls.set(K_TOKEN, JSON.stringify({ tok: j.idToken, exp: Date.now() + 50 * 60000 }))
    return j.idToken
  } catch { return null }
}

async function enviar (ev: Evidencia): Promise<boolean> {
  const tok = await tokenAnonimo()
  if (!tok) return false
  try {
    const url = `${DB}${RAIZ}/${san(ev.turma)}/${san(ev.nome)}.json?auth=${tok}`
    const r = await fx(url, { method: 'POST', body: JSON.stringify(ev) })
    return r.ok
  } catch { return false }
}

// grava a evidência: espelho local SEMPRE (painel na mesma máquina funciona já);
// Firebase quando der (senão entra na fila e tenta de novo no próximo boot)
export async function gravarEvidencia (ev: Evidencia): Promise<void> {
  try {
    const loc: Evidencia[] = JSON.parse(ls.get(K_LOCAL) || '[]')
    loc.push(ev); ls.set(K_LOCAL, JSON.stringify(loc.slice(-200)))
  } catch { /* segue */ }
  if ((navigator as any).webdriver) return          // QA/robô: não fala com a internet
  if (!(await enviar(ev))) {
    try {
      const fila: Evidencia[] = JSON.parse(ls.get(K_FILA) || '[]')
      fila.push(ev); ls.set(K_FILA, JSON.stringify(fila.slice(-100)))
    } catch { /* segue */ }
  }
}

export async function sincronizarFila (): Promise<void> {
  if ((navigator as any).webdriver) return
  let fila: Evidencia[] = []
  try { fila = JSON.parse(ls.get(K_FILA) || '[]') } catch { return }
  if (!fila.length) return
  const resto: Evidencia[] = []
  for (const ev of fila) if (!(await enviar(ev))) resto.push(ev)
  ls.set(K_FILA, JSON.stringify(resto))
}

export function evidenciasLocais (): Evidencia[] {
  try { return JSON.parse(ls.get(K_LOCAL) || '[]') } catch { return [] }
}

// ---------- RUBRICA (regra explícita e auditável — evidência -> nível) ----------
export type Nivel = 'Consolidado' | 'Em desenvolvimento' | 'Iniciando'
export function nivelRubrica (ev: Pick<Evidencia, 'nivelAjuda' | 'erros'>): Nivel {
  if (ev.nivelAjuda === 0 && ev.erros === 0) return 'Consolidado'
  if (ev.nivelAjuda <= 1) return 'Em desenvolvimento'
  return 'Iniciando'
}
// sugestão de nota por TABELA FIXA (o professor pode adotar outra régua; é só sugestão)
export const NOTA_SUGERIDA: Record<Nivel, string> = {
  Consolidado: '8,5 – 10', 'Em desenvolvimento': '6,0 – 8,4', Iniciando: 'abaixo de 6,0'
}

// ---------- PARECER DESCRITIVO (rascunho que CITA evidências; o professor edita) ----------
const NOME_KC: Record<string, string> = {
  'grupos-iguais': 'multiplicação como grupos iguais (EF03MA07)',
  contar: 'contagem de quantidades', somar: 'adição com composição de parcelas',
  selecionar: 'classificação por critério', ordenar: 'ordenação de sequências'
}
export function gerarParecer (nome: string, evs: Evidencia[]): string {
  if (!evs.length) return ''
  const porKc = new Map<string, Evidencia[]>()
  for (const e of evs) { const l = porKc.get(e.kc) || []; l.push(e); porKc.set(e.kc, l) }
  const partes: string[] = []
  for (const [kc, lista] of porKc) {
    const ult = lista[lista.length - 1]
    const nivel = nivelRubrica(ult)
    const hab = NOME_KC[kc] || kc
    let p = `Em ${hab}, ${nome} `
    if (ult.mecanica === 'agrupar') {
      p += `repartiu ${ult.alvo} itens em grupos iguais${ult.estrategia ? ` (organizou como ${ult.estrategia})` : ''}`
    } else p += `concluiu a missão (alvo ${ult.alvo})`
    if (ult.erros === 0 && ult.nivelAjuda === 0) p += ' de forma autônoma, sem precisar de ajuda'
    else if (ult.nivelAjuda <= 1) p += `, reorganizando sozinho(a) após ${ult.erros === 1 ? 'uma tentativa' : ult.erros + ' tentativas'} em que refletiu sobre o próprio erro`
    else p += `, precisando que o passo a passo fosse retomado (${ult.erros} tentativas)`
    p += `. Nível observado: ${nivel}.`
    if (lista.length > 1) p += ` (${lista.length} missões registradas; considerar a evolução entre elas.)`
    partes.push(p)
  }
  partes.push('Observação: registro gerado a partir das evidências do jogo (as evidências sugerem, não sentenciam) — revisar e complementar com a observação em sala.')
  return partes.join(' ')
}
