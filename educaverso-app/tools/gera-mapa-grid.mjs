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

// === AUTO-PAREDE (Terrain/Wang na prática): UMA função desenha a moldura correta de
// QUALQUER retângulo, escolhendo canto/lado sozinha + colisão. Antes havia 2 cópias na
// mão (com desenhos diferentes) — a fonte do bug "parede direita ≠ esquerda". Agora é 1 só.
const moldura = (x0, y0, w, h, isGap) => {
  for (let iy = 0; iy < h; iy++) for (let ix = 0; ix < w; ix++) {
    const x = x0 + ix, y = y0 + iy
    const eL = ix === 0, eR = ix === w - 1, eT = iy === 0, eB = iy === h - 1
    if (!(eL || eR || eT || eB)) continue                 // só a borda
    if (isGap && isGap(x, y)) continue                    // vão (porta/saída) fica aberto
    const fr = eT && eL ? PAR.TL : eT && eR ? PAR.TR : eB && eL ? PAR.BL : eB && eR ? PAR.BR : eT ? PAR.T : eB ? PAR.B : eL ? PAR.L : PAR.R
    put(muros, x, y, pg(fr)); put(colis, x, y, COL)
  }
}
// moldura EXTERNA (saída aberta na linha 7 do muro direito)
moldura(OX0, OY0, OX1 - OX0 + 1, OY1 - OY0 + 1, (x, y) => x === OX1 && y === SAI_Y)

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

// --- INTERIOR (sala): piso em tudo + a MESMA função de moldura (auto-parede) ---
const saiSalaX = IX0 + ((IW - 1) >> 1)
for (let y = IY0; y < IY0 + IH; y++) for (let x = IX0; x < IX0 + IW; x++) put(chao, x, y, GRAMA + 1)  // chão em toda a sala
moldura(IX0, IY0, IW, IH, (x, y) => y === IY0 + IH - 1 && x === saiSalaX)                              // saída no meio de baixo
const interiorEntra = { x: IX0 + ((IW - 1) >> 1), y: IY0 + IH - 2 }   // onde o herói aparece ao entrar
const interiorSai = { x: IX0 + ((IW - 1) >> 1), y: IY0 + IH - 1 }     // tile de saída (volta pra porta)

// tiles que COLIDEM (marca a propriedade ge_collide no tile local do paredes)
const collideIds = [PAR.TL, PAR.T, PAR.TR, PAR.L, PAR.R, PAR.BL, PAR.B, PAR.BR, PAR.SOLIDO]
const tilesProp = [...new Set(collideIds)].sort((a, b) => a - b).map(id => ({ id, properties: [{ name: 'ge_collide', type: 'bool', value: true }] }))
const layer = (name, data, visible = true) => ({ name, type: 'tilelayer', width: W, height: H, x: 0, y: 0, opacity: 1, visible, data })

// --- DECOR: enfeites como OBJETOS no mapa (posição é DADO; o código só renderiza) ---
// cada objeto: name = recorte a desenhar; props tex (textura) e org (origem y).
// x,y em pixels (âncora base). O motor desenha origin(0.5,1), depth = y.
let _oid = 1
const obj = (frame, tex, xpx, ypx) => ({ id: _oid++, name: frame, type: 'decor', x: xpx, y: ypx, width: 0, height: 0, point: true, visible: true, rotation: 0, properties: [{ name: 'tex', type: 'string', value: tex }] })
const decor = []
decor.push(obj('casa_a', 'mundo', (casa.x + 1.5) * T, (casa.y + 2) * T))
for (const [ax, ay] of arvores) decor.push(obj('arvore', 'mundo', (ax + 0.5) * T, (ay + 1) * T + 6))
decor.push(obj('estante', 'mundo', (IX0 + 2) * T, (IY0 + 2) * T))
decor.push(obj('bau', 'bau', (IX0 + IW - 3) * T, (IY0 + 2) * T))
const objLayer = (name, objects) => ({ name, type: 'objectgroup', objects, opacity: 1, visible: true, x: 0, y: 0, draworder: 'topdown' })

const P = (n, v) => ({ name: n, type: 'int', value: v })
const mapa = {
  compressionlevel: -1, infinite: false, orientation: 'orthogonal', renderorder: 'right-down',
  tiledversion: '1.10.2', type: 'map', version: '1.10', width: W, height: H, tilewidth: T, tileheight: T,
  layers: [layer('chao', chao), layer('muros', muros), layer('colisao', colis, false), objLayer('decor', decor)],
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
