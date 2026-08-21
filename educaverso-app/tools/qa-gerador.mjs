// ============================================================================
// ROBÔ-QA — CÉREBRO DO GERADOR (catálogo pedagógico / Portão 0).
// Prova que objetivo->missão jogável funciona SEM depender de asset nem LLM:
//   - reconhece objetivo de contagem e devolve missão da mecânica 'contar';
//   - respeita dificuldade e idade (números menores pra pré/1º ano);
//   - é DETERMINÍSTICO (mesmo briefing -> mesma missão);
//   - é REPRODUZÍVEL por tema (temas diferentes -> quantidades diferentes);
//   - a TRAVA do Portão 0 segura: objetivo sem mecânica jogável -> 0 missões
//     (o gerador avisa com honestidade, nunca inventa quiz).
// Uso: node tools/qa-gerador.mjs   (bundla o TS com esbuild e roda em node)
// ============================================================================
import { execFileSync } from 'node:child_process'
import { writeFileSync, mkdtempSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

const raiz = new URL('..', import.meta.url).pathname
const dir = mkdtempSync(join(tmpdir(), 'qa-ger-'))
const entrada = join(dir, 'entrada.ts')
const saida = join(dir, 'bundle.mjs')

// entry que re-exporta a API do catálogo pedagógico
writeFileSync(entrada, `export * from '${join(raiz, 'src/gerador/catalogo-pedagogico.ts')}'\n`)

// bundla (resolve imports extensionless de TS; tira os tipos)
execFileSync(join(raiz, 'node_modules/.bin/esbuild'), [
  entrada, '--bundle', '--format=esm', '--platform=node', `--outfile=${saida}`
], { stdio: ['ignore', 'ignore', 'inherit'] })

const G = await import(pathToFileURL(saida).href)

const falhas = []
const ok = (cond, msg) => { if (cond) console.log('  ✔ ' + msg); else { console.log('  ✘ ' + msg); falhas.push(msg) } }

const brief = (o = {}) => ({
  ano: '2ano', disciplina: 'matematica',
  objetivo: 'contar quantidades até 10 com correspondência um a um',
  tema: 'floresta', tempoMin: 55, dificuldade: 'medio', ...o
})

console.log('== 1. RECONHECE objetivo de contagem -> mecânica jogável ==')
const m1 = G.planejarMissoes(brief())
ok(m1.length > 0, 'gerou ao menos 1 missão')
ok(m1.every(p => p.mecanica === 'contar'), 'toda missão usa a mecânica runtime "contar"')
ok(m1.every(p => p.verboDoMundo && p.verboDoMundo !== 'responder'), 'missão é VERBO DO MUNDO, não quiz')
ok(m1.every(p => typeof p.params.quantidade === 'number' && p.params.quantidade >= 1), 'params.quantidade válido p/ o motor')
console.log('    ex:', JSON.stringify(m1[0]))

console.log('== 2. DIFICULDADE escala a quantidade ==')
const qFacil = G.planejarMissoes(brief({ dificuldade: 'facil' }))[0].params.quantidade
const qDificil = G.planejarMissoes(brief({ dificuldade: 'dificil' }))[0].params.quantidade
ok(qFacil <= qDificil, `fácil (${qFacil}) <= difícil (${qDificil})`)

console.log('== 3. IDADE segura o teto (pré/1º ano não recebe número grande) ==')
const qPre = G.planejarMissoes(brief({ ano: 'pre', dificuldade: 'dificil' }))[0].params.quantidade
ok(qPre <= 6, `pré-escola no "difícil" ainda fica pequeno (${qPre} <= 6)`)

console.log('== 4. DETERMINÍSTICO (mesmo briefing -> mesma missão) ==')
const a = JSON.stringify(G.planejarMissoes(brief()))
const b = JSON.stringify(G.planejarMissoes(brief()))
ok(a === b, 'duas gerações do mesmo briefing são idênticas')

console.log('== 5. REPRODUZÍVEL por tema (temas diferentes variam a quantidade) ==')
const qs = ['floresta', 'espaço', 'oceano', 'castelo', 'fazenda'].map(t => G.planejarMissoes(brief({ tema: t }))[0].params.quantidade)
ok(new Set(qs).size >= 2, `temas geram números variados: ${qs.join(', ')}`)

console.log('== 6. TRAVA DO PORTÃO 0 (objetivo sem mecânica jogável -> 0 missões) ==')
const semMec = G.planejarMissoes(brief({ disciplina: 'historia', objetivo: 'compreender a Revolução Francesa e suas causas', tema: 'castelo' }))
ok(semMec.length === 0, 'objetivo sem mecânica jogável NÃO vira quiz (0 missões, avisa honesto)')

console.log('== 7. tempo da aula -> nº de missões (mais tempo, mais missões) ==')
const n20 = G.planejarMissoes(brief({ tempoMin: 20 })).length
const n80 = G.planejarMissoes(brief({ tempoMin: 80 })).length
ok(n20 >= 1 && n80 >= n20, `20min=${n20} missão(ões), 80min=${n80}`)

console.log(falhas.length ? `\n== REPROVADO: ${falhas.length} falha(s) ==` : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
