// QA do MOTOR ADAPTATIVO — prova a matemática (funções puras), sem navegador.
// Transpila o módulo TS com esbuild e roda asserts: BKT sobe/desce/dá mastery,
// Leitner avança/reseta e espaça, DDA mantém o alvo na ZDP, armazém registra certo.
import { build } from 'esbuild'
import { writeFileSync } from 'fs'
import { pathToFileURL } from 'url'

const out = '/tmp/motor.mjs'
await build({ entryPoints: ['src/fabrica/motor-adaptativo.ts'], bundle: true, format: 'esm', outfile: out, logLevel: 'silent' })
const M = await import(pathToFileURL(out).href)

const falhas = []
const ok = (c, m) => { if (c) console.log('  ✔ ' + m); else { console.log('  ✘ ' + m); falhas.push(m) } }
const dia = 86400000, agora = 1000000000000

console.log('== BKT-lite: domínio sobe com acerto, desce com erro ==')
let pk = 0.3
const pkSubiu = M.atualizaBKT(pk, true)
ok(pkSubiu > pk, `acerto sobe P(domina): ${pk.toFixed(2)} -> ${pkSubiu.toFixed(2)}`)
const pkDesceu = M.atualizaBKT(0.7, false)
ok(pkDesceu < 0.7, `erro derruba P(domina): 0.70 -> ${pkDesceu.toFixed(2)}`)

console.log('== BKT-lite: vários acertos levam a MASTERY (>=0.95) ==')
pk = 0.3; let n = 0
while (!M.domina(pk) && n < 30) { pk = M.atualizaBKT(pk, true); n++ }
ok(M.domina(pk), `chegou a mastery em ${n} acertos (P=${pk.toFixed(3)})`)
ok(n >= 3 && n <= 15, `nº de acertos p/ mastery é razoável (${n}, esperado 3-15)`)

console.log('== BKT-lite: um erro no meio ATRASA a mastery (não trava) ==')
let pkA = 0.3; for (let i = 0; i < 5; i++) pkA = M.atualizaBKT(pkA, true)
let pkB = 0.3; for (let i = 0; i < 2; i++) pkB = M.atualizaBKT(pkB, true); pkB = M.atualizaBKT(pkB, false); for (let i = 0; i < 2; i++) pkB = M.atualizaBKT(pkB, true)
ok(pkB < pkA, `mesmo nº de respostas, com 1 erro dá domínio menor (${pkB.toFixed(2)} < ${pkA.toFixed(2)})`)

console.log('== LEITNER: acerto sobe de caixa, erro volta pra 0, intervalo cresce ==')
ok(M.proximaCaixa(0, true) === 1, 'acerto: caixa 0 -> 1')
ok(M.proximaCaixa(3, false) === 0, 'erro: caixa 3 -> 0')
ok(M.intervaloDias(0) < M.intervaloDias(3), `intervalo cresce com a caixa (${M.intervaloDias(0)}d < ${M.intervaloDias(3)}d)`)
const rev = M.proximaRevisao(1, true, agora)
ok(rev === agora + M.intervaloDias(2) * dia, 'próxima revisão = agora + intervalo da caixa nova')

console.log('== DDA: dificuldade fica na ZDP (sobe c/ folga, desce ao travar, respeita limites) ==')
ok(M.proximoAlvo(5, 0.9, true) === 6, 'dominou com folga -> alvo sobe (5 -> 6)')
ok(M.proximoAlvo(5, 0.3, false) === 4, 'travou -> alvo desce (5 -> 4)')
ok(M.proximoAlvo(9, 0.99, true) === 9, 'não passa do teto (9)')
ok(M.proximoAlvo(2, 0.1, false) === 2, 'não passa do piso (2)')
ok(M.proximoAlvo(5, 0.6, true) === 5, 'zona neutra: mantém (5)')

console.log('== ARMAZÉM: registra observação e devolve KCs a revisar ==')
let prog = {}
prog = M.registra(prog, 'contar', true, agora)
ok(prog.contar && prog.contar.tentativas === 1 && prog.contar.acertos === 1, 'registrou 1 tentativa/1 acerto no KC')
ok(prog.contar.proximaRevisao > agora, 'agendou próxima revisão no futuro')
const vencido = M.kcsParaRevisar({ contar: { pKnown: 0.5, caixa: 1, proximaRevisao: agora - dia, tentativas: 2, acertos: 1 } }, agora)
ok(vencido.length === 1 && vencido[0] === 'contar', 'lista KC cuja revisão VENCEU (missão de retorno)')

console.log(falhas.length ? '\n== REPROVADO: ' + falhas.length + ' ==' : '\n== APROVADO ==')
process.exit(falhas.length ? 1 : 0)
