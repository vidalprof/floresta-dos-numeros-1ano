// ============================================================================
// AUDITOR DE RECORTES — detecta AUTOMATICAMENTE imagem incompleta/cortada.
// Regra: um objeto recortado de um tileset (casa, estante, pedra, móvel) é um
// sprite AVULSO que "flutua" no recorte — logo a MOLDURA de pixels na borda tem
// que ser majoritariamente TRANSPARENTE. Se uma beirada está muito OPACA, o
// recorte cortou o objeto ao meio OU pegou um pedaço do vizinho (o "recorte de
// outra imagem" que o Marcos viu). Roda sobre a lista de PROPS (nome->x,y,w,h).
// Uso: node tools/auditor-recortes.mjs   (usa Pillow via python3)
// ============================================================================
import { execFileSync } from 'node:child_process'

// os mesmos recortes usados no jogo (mantidos em sincronia com FaseUm/VilaViva)
const PROPS = {
  'mundo.png': {
    casa_a: [0, 0, 64, 48], casa_b: [64, 0, 64, 48], arvore: [0, 160, 32, 32],
    toco: [97, 293, 30, 23], carroca: [82, 131, 27, 27], feira: [116, 130, 27, 28],
    estante: [160, 592, 33, 32], prateleira: [206, 592, 31, 31],
    tapete: [112, 592, 48, 48], planta: [0, 600, 15, 24],
    torii: [7, 51, 34, 29], cerca: [85, 71, 39, 22], varal: [128, 73, 32, 21]
  }
}
const DIR = new URL('../public/rpg/', import.meta.url).pathname
const LIMITE = 0.55        // se >55% de uma beirada é opaca, provável corte

const py = `
import json, sys
from PIL import Image
props = json.loads(sys.argv[1]); base = sys.argv[2]
falhas = []
def opac(linha):
    return (sum(1 for a in linha if a > 40) / len(linha)) if linha else 0
for arq, itens in props.items():
    im = Image.open(base + arq).convert('RGBA')
    W, H = im.size
    for nome, (x, y, w, h) in itens.items():
        if x+w > W or y+h > H:
            falhas.append(nome + ': recorte fora da textura'); continue
        c = im.crop((x, y, x+w, y+h)); px = c.load()
        # SLIVER DESTACADO: varre 5px pra dentro de cada beira. Se a linha da BORDA
        # é opaca, existe um VÃO transparente logo em seguida, e depois o objeto
        # volta a aparecer -> a borda tem um pedaço SOLTO (vizinho/corte).
        def col(ix): return [px[ix, j][3] for j in range(h)]
        def row(iy): return [px[i, iy][3] for i in range(w)]
        def sliver(linhas):
            ops = [opac(l) for l in linhas]
            if ops[0] < 0.25: return False                 # borda vazia = ok (tem margem)
            # procura vão (quase vazio) nos 4px seguintes, e objeto voltando depois
            for k in range(1, min(4, len(ops)-1)):
                if ops[k] < 0.08 and any(o > 0.25 for o in ops[k+1:]):
                    return True
            return False
        susp = []
        if sliver([col(w-1-k) for k in range(5)]): susp.append('dir')
        if sliver([col(k) for k in range(5)]): susp.append('esq')
        if sliver([row(k) for k in range(5)]): susp.append('topo')
        if susp: falhas.append(nome + ' pedaco solto na(s) beira(s): ' + ','.join(susp))
print(json.dumps(falhas, ensure_ascii=False))
`
const out = execFileSync('python3', ['-c', py, JSON.stringify(PROPS), DIR], { encoding: 'utf-8' })
const falhas = JSON.parse(out.trim().split('\n').pop())
if (falhas.length) {
  console.log('✘ RECORTES SUSPEITOS DE CORTE/INCOMPLETOS:')
  falhas.forEach(f => console.log('   - ' + f))
  console.log('  (AVISO p/ conferir no screenshot — nao trava; pixel-check tem falso-positivo com vizinho colado)')
  process.exit(0)
} else {
  console.log('✔ recortes OK — nenhum objeto cortado/incompleto (bordas com margem)')
}
