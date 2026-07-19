// Gera um mapa no formato TILED (JSON) — a fase vira DADO, não código na mão.
// É a prova do novo jeito: colisão marcada no tile (ge_collide), grid-engine lê.
// Saída: public/rpg/mapa_grid.json
import fs from 'fs'

const W = 20, H = 15, T = 16
const CHAO_FG = 1                 // firstgid do tileset chão (chao.png, 22 colunas)
const PAR_FG = 1001               // firstgid do tileset paredes (paredes.png, 10 colunas)
const GRAMA = CHAO_FG + 245       // tile de grama (linha 11, col 3 do tileset_floor)
// frames de parede (ids locais no paredes.png, 10 colunas)
const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44, SOLIDO: 43 }
const pg = (id) => PAR_FG + id    // gid de uma parede
const SAI_Y = 7                   // linha da abertura (saída) no muro direito

// --- camada CHÃO: grama em tudo ---
const chao = new Array(W * H).fill(GRAMA)

// --- camada MUROS (visível + colide): borda com saída à direita + a CASA ---
const muros = new Array(W * H).fill(0)
const put = (x, y, gid) => { muros[y * W + x] = gid }
for (let x = 0; x < W; x++) { put(x, 0, x === 0 ? pg(PAR.TL) : x === W - 1 ? pg(PAR.TR) : pg(PAR.T)); put(x, H - 1, x === 0 ? pg(PAR.BL) : x === W - 1 ? pg(PAR.BR) : pg(PAR.B)) }
for (let y = 1; y < H - 1; y++) { put(0, y, pg(PAR.L)); if (y !== SAI_Y) put(W - 1, y, pg(PAR.R)) }
// CASA: bloco de colisão 3x2 (a imagem da casa é desenhada por cima na cena).
// Porta = tile do meto de baixo fica ABERTO (sem colisão) p/ entrar.
const casaX = 3, casaY = 3
for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 3; dx++) put(casaX + dx, casaY + dy, pg(PAR.SOLIDO))

// tiles que COLIDEM (grid-engine lê a propriedade ge_collide=true no tile local)
const collideIds = [PAR.TL, PAR.T, PAR.TR, PAR.L, PAR.R, PAR.BL, PAR.B, PAR.BR, PAR.SOLIDO]
const tilesProp = [...new Set(collideIds)].sort((a, b) => a - b).map(id => ({ id, properties: [{ name: 'ge_collide', type: 'bool', value: true }] }))

const layer = (name, data, visible = true) => ({ name, type: 'tilelayer', width: W, height: H, x: 0, y: 0, opacity: 1, visible, data })

const mapa = {
  compressionlevel: -1, infinite: false, orientation: 'orthogonal', renderorder: 'right-down',
  tiledversion: '1.10.2', type: 'map', version: '1.10', width: W, height: H, tilewidth: T, tileheight: T,
  layers: [layer('chao', chao), layer('muros', muros)],
  tilesets: [
    { firstgid: CHAO_FG, name: 'chao', image: 'chao.png', imagewidth: 352, imageheight: 416, tilewidth: T, tileheight: T, columns: 22, tilecount: 22 * 26, margin: 0, spacing: 0 },
    { firstgid: PAR_FG, name: 'paredes', image: 'paredes.png', imagewidth: 160, imageheight: 176, tilewidth: T, tileheight: T, columns: 10, tilecount: 110, margin: 0, spacing: 0, tiles: tilesProp }
  ],
  properties: [
    { name: 'heroiX', type: 'int', value: 10 }, { name: 'heroiY', type: 'int', value: 10 },
    { name: 'casaX', type: 'int', value: casaX }, { name: 'casaY', type: 'int', value: casaY },
    { name: 'saidaY', type: 'int', value: SAI_Y }
  ]
}

fs.writeFileSync('public/rpg/mapa_grid.json', JSON.stringify(mapa))
console.log('mapa_grid.json gerado:', W + 'x' + H, '| muros+casa colidem via ge_collide | porta e saída abertas')
