// ============================================================================
// FÁBRICA — gerador de MAPA da fase, rodando NO NAVEGADOR (não mais só no build).
// Recebe o PLANO (validado) e devolve um mapa no formato TILED (objeto), que o motor
// FaseGrid renderiza. É o mesmo layout auditado da Fase 1, agora parametrizável:
// o número de potes a juntar vem do plano (dificuldade do professor).
// Toda a colisão vem do tile (ge_collide) e as paredes são auto-desenhadas (moldura).
// ============================================================================

export interface PlanoMapa {
  melAlvo: number          // quantos itens juntar no total (inclui 1 dentro da casa)
  tituloProp?: string      // (reservado p/ variações de cenário futuras)
}

const T = 16
const CHAO_FG = 1
const PAR_FG = 1001
const GRAMA = CHAO_FG + 245
const PAR = { TL: 0, T: 3, TR: 4, L: 10, R: 14, BL: 40, B: 43, BR: 44, SOLIDO: 43 }
const pg = (id: number): number => PAR_FG + id

type Grid = number[]

export function montarMapaFase (plano: PlanoMapa): object {
  const W = 56, H = 16
  const OX0 = 0, OX1 = 19, OY0 = 0, OY1 = H - 1
  const IX0 = 45, IY0 = 1, IW = 9, IH = 7
  const SAI_Y = 7
  const melAlvo = Math.max(2, Math.min(9, Math.round(plano.melAlvo)))

  const chao: Grid = new Array(W * H).fill(0)
  const muros: Grid = new Array(W * H).fill(0)
  const colis: Grid = new Array(W * H).fill(0)
  const COL = pg(PAR.SOLIDO)
  const put = (arr: Grid, x: number, y: number, gid: number): void => { if (x >= 0 && x < W && y >= 0 && y < H) arr[y * W + x] = gid }

  // chão externo (grama)
  for (let y = OY0; y <= OY1; y++) for (let x = OX0; x <= OX1; x++) put(chao, x, y, GRAMA)

  // AUTO-PAREDE: uma função desenha a moldura correta de qualquer retângulo
  const moldura = (x0: number, y0: number, w: number, h: number, isGap?: (x: number, y: number) => boolean): void => {
    for (let iy = 0; iy < h; iy++) for (let ix = 0; ix < w; ix++) {
      const x = x0 + ix, y = y0 + iy
      const eL = ix === 0, eR = ix === w - 1, eT = iy === 0, eB = iy === h - 1
      if (!(eL || eR || eT || eB)) continue
      if (isGap && isGap(x, y)) continue
      const fr = eT && eL ? PAR.TL : eT && eR ? PAR.TR : eB && eL ? PAR.BL : eB && eR ? PAR.BR : eT ? PAR.T : eB ? PAR.B : eL ? PAR.L : PAR.R
      put(muros, x, y, pg(fr)); put(colis, x, y, COL)
    }
  }
  moldura(OX0, OY0, OX1 - OX0 + 1, OY1 - OY0 + 1, (x, y) => x === OX1 && y === SAI_Y)

  // casa + porta
  const casa = { x: 3, y: 3 }
  for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 3; dx++) put(colis, casa.x + dx, casa.y + dy, COL)
  const porta = { x: casa.x + 1, y: casa.y + 2 }

  // árvores (colisão na base)
  const arvores = [[2, 9], [16, 3], [15, 9], [11, 11], [6, 12]]
  for (const [x, y] of arvores) put(colis, x, y, COL)

  // pedras que fecham a saída
  const pedras = { x: OX1, y: SAI_Y }
  put(colis, pedras.x, pedras.y, COL)

  // interior (sala) — chão + auto-parede com saída no meio de baixo
  const saiSalaX = IX0 + ((IW - 1) >> 1)
  for (let y = IY0; y < IY0 + IH; y++) for (let x = IX0; x < IX0 + IW; x++) put(chao, x, y, GRAMA + 1)
  moldura(IX0, IY0, IW, IH, (x, y) => y === IY0 + IH - 1 && x === saiSalaX)
  const interiorEntra = { x: saiSalaX, y: IY0 + IH - 2 }
  const interiorSai = { x: saiSalaX, y: IY0 + IH - 1 }

  // MEL: 1 dentro da casa + (melAlvo-1) espalhados no externo, em tiles de chão livres
  const fazendeiro = { x: 9, y: 6 }
  const candidatos: number[][] = [[6, 6], [13, 5], [8, 10], [14, 12], [12, 8], [5, 12], [16, 11], [7, 4]]
  const ocupado = (x: number, y: number): boolean =>
    colis[y * W + x] !== 0 || (x === fazendeiro.x && y === fazendeiro.y) || (x === porta.x && y === porta.y)
  const melExternos: number[][] = []
  for (const c of candidatos) { if (melExternos.length >= melAlvo - 1) break; if (!ocupado(c[0], c[1])) melExternos.push(c) }
  const melInterno = [saiSalaX, IY0 + 2]

  // DECOR (enfeites como objetos — o motor só renderiza o que o mapa manda)
  let oid = 1
  const obj = (frame: string, tex: string, xpx: number, ypx: number): object => ({ id: oid++, name: frame, type: 'decor', x: xpx, y: ypx, width: 0, height: 0, point: true, visible: true, rotation: 0, properties: [{ name: 'tex', type: 'string', value: tex }] })
  const decor: object[] = [obj('casa_a', 'mundo', (casa.x + 1.5) * T, (casa.y + 2) * T)]
  for (const [ax, ay] of arvores) decor.push(obj('arvore', 'mundo', (ax + 0.5) * T, (ay + 1) * T + 6))
  decor.push(obj('estante', 'mundo', (IX0 + 2) * T, (IY0 + 2) * T))
  decor.push(obj('bau', 'bau', (IX0 + IW - 3) * T, (IY0 + 2) * T))

  const collideIds = [PAR.TL, PAR.T, PAR.TR, PAR.L, PAR.R, PAR.BL, PAR.B, PAR.BR, PAR.SOLIDO]
  const tilesProp = [...new Set(collideIds)].sort((a, b) => a - b).map(id => ({ id, properties: [{ name: 'ge_collide', type: 'bool', value: true }] }))
  const layer = (name: string, data: Grid, visible = true): object => ({ name, type: 'tilelayer', width: W, height: H, x: 0, y: 0, opacity: 1, visible, data })
  const objLayer = (name: string, objects: object[]): object => ({ name, type: 'objectgroup', objects, opacity: 1, visible: true, x: 0, y: 0, draworder: 'topdown' })
  const Pi = (n: string, v: number): object => ({ name: n, type: 'int', value: v })
  const Ps = (n: string, v: unknown): object => ({ name: n, type: 'string', value: JSON.stringify(v) })

  return {
    compressionlevel: -1, infinite: false, orientation: 'orthogonal', renderorder: 'right-down',
    tiledversion: '1.10.2', type: 'map', version: '1.10', width: W, height: H, tilewidth: T, tileheight: T,
    layers: [layer('chao', chao), layer('muros', muros), layer('colisao', colis, false), objLayer('decor', decor)],
    tilesets: [
      { firstgid: CHAO_FG, name: 'chao', image: 'chao.png', imagewidth: 352, imageheight: 416, tilewidth: T, tileheight: T, columns: 22, tilecount: 22 * 26, margin: 0, spacing: 0 },
      { firstgid: PAR_FG, name: 'paredes', image: 'paredes.png', imagewidth: 160, imageheight: 176, tilewidth: T, tileheight: T, columns: 10, tilecount: 110, margin: 0, spacing: 0, tiles: tilesProp }
    ],
    properties: [
      Pi('heroiX', 10), Pi('heroiY', 12),
      Pi('casaX', casa.x), Pi('casaY', casa.y), Pi('portaX', porta.x), Pi('portaY', porta.y),
      Pi('fazX', fazendeiro.x), Pi('fazY', fazendeiro.y),
      Pi('pedrasX', pedras.x), Pi('pedrasY', pedras.y), Pi('saidaY', SAI_Y),
      Pi('intEntraX', interiorEntra.x), Pi('intEntraY', interiorEntra.y),
      Pi('intSaiX', interiorSai.x), Pi('intSaiY', interiorSai.y),
      Ps('melExternos', melExternos), Ps('melInterno', melInterno),
      Ps('arvores', arvores), Ps('interior', { x0: IX0, y0: IY0, w: IW, h: IH })
    ]
  }
}
