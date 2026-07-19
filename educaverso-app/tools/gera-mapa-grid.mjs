// Gera o mapa da FASE 1 no formato TILED (JSON) — a fase é DADO, não código na mão.
// Tem: área externa emoldurada (grama + muro + saída), a CASA com porta, árvores,
// e um INTERIOR (sala) à direita (fora da vista da câmera externa). Colisão vem
// marcada no tile (ge_collide) numa camada invisível "colisao" — grid-engine lê.
// Saída: public/rpg/mapa_grid.json
import fs from 'fs'

const W = 56, H = 16, T = 16
const CHAO_FG = 1                 // firstgid tileset chão (chao.png, 22 colunas)
const PAR_FG = 1001               // firstgid tileset paredes (paredes.png, 10 colunas)
const GRAMA = CHAO_FG + 245       // grama (linha 11, col 3)
const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44, SOLIDO: 43, ESC: 50 }
const pg = (id) => PAR_FG + id
const SAI_Y = 7                   // linha da abertura no muro direito (a saída da fase)

// ÁREA EXTERNA: x 0..19, y 0..15 (emoldurada). INTERIOR: sala 9x7 em x 21..29, y 1..7.
const OX0 = 0, OX1 = 19, OY0 = 0, OY1 = H - 1
const IX0 = 45, IY0 = 1, IW = 9, IH = 7          // sala BEM longe do externo (câmera nunca mostra os 2)

const chao = new Array(W * H).fill(0)
const muros = new Array(W * H).fill(0)
const colis = new Array(W * H).fill(0)           // invisível: só colisão (ge_collide)
const put = (arr, x, y, gid) => { if (x >= 0 && x < W && y >= 0 && y < H) arr[y * W + x] = gid }
const COL = pg(PAR.SOLIDO)                        // tile-marcador de colisão (fica invisível)

// --- CHÃO externo: grama em toda a área externa ---
for (let y = OY0; y <= OY1; y++) for (let x = OX0; x <= OX1; x++) put(chao, x, y, GRAMA)

// --- MUROS externos (visível): borda + saída à direita (linha 7 aberta) ---
for (let x = OX0; x <= OX1; x++) { put(muros, x, OY0, x === OX0 ? pg(PAR.TL) : x === OX1 ? pg(PAR.TR) : pg(PAR.T)); put(muros, x, OY1, x === OX0 ? pg(PAR.BL) : x === OX1 ? pg(PAR.BR) : pg(PAR.B)) }
for (let y = OY0 + 1; y < OY1; y++) { put(muros, OX0, y, pg(PAR.L)); if (y !== SAI_Y) put(muros, OX1, y, pg(PAR.R)) }
// colisão da borda (a mesma da parede visível)
for (let x = OX0; x <= OX1; x++) { put(colis, x, OY0, COL); put(colis, x, OY1, COL) }
for (let y = OY0 + 1; y < OY1; y++) { put(colis, OX0, y, COL); if (y !== SAI_Y) put(colis, OX1, y, COL) }

// --- CASA externa: bloco de colisão 3x2 em (3,3); porta = meio de baixo aberto ---
const casa = { x: 3, y: 3 }
for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 3; dx++) put(colis, casa.x + dx, casa.y + dy, COL)
const porta = { x: casa.x + 1, y: casa.y + 2 }   // tile logo abaixo da casa = porta (pisar = entrar)

// --- ÁRVORES externas: base colide (1 tile) ---
const arvores = [[2, 9], [16, 3], [15, 9], [11, 11], [6, 12]]
for (const [x, y] of arvores) put(colis, x, y, COL)

// --- PEDRAS na saída (linha 7, coluna 19): fecham a passagem ATÉ a entrega ---
const pedras = { x: OX1, y: SAI_Y }
put(colis, pedras.x, pedras.y, COL)

// --- INTERIOR (sala): piso + paredes (visível) + colisão; sala emoldurada ---
for (let y = IY0; y < IY0 + IH; y++) for (let x = IX0; x < IX0 + IW; x++) {
  const borda = (x === IX0 || x === IX0 + IW - 1 || y === IY0 || y === IY0 + IH - 1)
    const saidaSala = (y === IY0 + IH - 1 && x === IX0 + ((IW - 1) >> 1))
  if (borda && !saidaSala) {
    // parede da sala (visível) + colisão — cada lado com o desenho CERTO
    const eL = x === IX0, eR = x === IX0 + IW - 1, eT = y === IY0, eB = y === IY0 + IH - 1
    const fr = eT && eL ? PAR.TL : eT && eR ? PAR.TR : eB && eL ? PAR.BL : eB && eR ? PAR.BR : eT ? PAR.T : eB ? PAR.B : eL ? PAR.L : PAR.R
    put(muros, x, y, pg(fr))
    put(colis, x, y, COL)
  } else {
    // piso do chão da sala (inclui o vão da porta/saída — chão livre, SEM parede)
    put(chao, x, y, GRAMA + 1)
  }
}
const interiorEntra = { x: IX0 + ((IW - 1) >> 1), y: IY0 + IH - 2 }   // onde o herói aparece ao entrar
const interiorSai = { x: IX0 + ((IW - 1) >> 1), y: IY0 + IH - 1 }     // tile de saída (volta pra porta)

// tiles que COLIDEM (marca a propriedade ge_collide no tile local do paredes)
const collideIds = [PAR.TL, PAR.T, PAR.TR, PAR.L, PAR.R, PAR.BL, PAR.B, PAR.BR, PAR.SOLIDO]
const tilesProp = [...new Set(collideIds)].sort((a, b) => a - b).map(id => ({ id, properties: [{ name: 'ge_collide', type: 'bool', value: true }] }))
const layer = (name, data, visible = true) => ({ name, type: 'tilelayer', width: W, height: H, x: 0, y: 0, opacity: 1, visible, data })

const P = (n, v) => ({ name: n, type: 'int', value: v })
const mapa = {
  compressionlevel: -1, infinite: false, orientation: 'orthogonal', renderorder: 'right-down',
  tiledversion: '1.10.2', type: 'map', version: '1.10', width: W, height: H, tilewidth: T, tileheight: T,
  layers: [layer('chao', chao), layer('muros', muros), layer('colisao', colis, false)],
  tilesets: [
    { firstgid: CHAO_FG, name: 'chao', image: 'chao.png', imagewidth: 352, imageheight: 416, tilewidth: T, tileheight: T, columns: 22, tilecount: 22 * 26, margin: 0, spacing: 0 },
    { firstgid: PAR_FG, name: 'paredes', image: 'paredes.png', imagewidth: 160, imageheight: 176, tilewidth: T, tileheight: T, columns: 10, tilecount: 110, margin: 0, spacing: 0, tiles: tilesProp }
  ],
  properties: [
    P('heroiX', 10), P('heroiY', 12),
    P('casaX', casa.x), P('casaY', casa.y), P('portaX', porta.x), P('portaY', porta.y),
    P('fazX', 9), P('fazY', 6),                          // fazendeiro
    P('pedrasX', pedras.x), P('pedrasY', pedras.y), P('saidaY', SAI_Y),
    P('intEntraX', interiorEntra.x), P('intEntraY', interiorEntra.y),
    P('intSaiX', interiorSai.x), P('intSaiY', interiorSai.y),
    { name: 'melExternos', type: 'string', value: JSON.stringify([[6, 6], [13, 5], [8, 10], [14, 12]]) },
    { name: 'melInterno', type: 'string', value: JSON.stringify([interiorEntra.x, IY0 + 2]) },
    { name: 'arvores', type: 'string', value: JSON.stringify(arvores) },
    { name: 'interior', type: 'string', value: JSON.stringify({ x0: IX0, y0: IY0, w: IW, h: IH }) }
  ]
}

fs.writeFileSync('public/rpg/mapa_grid.json', JSON.stringify(mapa))
console.log('mapa_grid.json v2:', W + 'x' + H, '| externo emoldurado + casa/porta + arvores + pedras + INTERIOR | colisao via ge_collide')
