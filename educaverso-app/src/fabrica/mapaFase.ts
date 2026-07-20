// ============================================================================
// FÁBRICA — gerador de MAPA da fase, rodando NO NAVEGADOR (não mais só no build).
// Recebe o PLANO (validado) e devolve um mapa no formato TILED (objeto), que o motor
// FaseGrid renderiza. É o mesmo layout auditado da Fase 1, agora parametrizável:
// o número de potes a juntar vem do plano (dificuldade do professor).
// Toda a colisão vem do tile (ge_collide) e as paredes são auto-desenhadas (moldura).
// ============================================================================

import { getKit } from './kits'

export interface PlanoMapa {
  melAlvo: number          // contar: quantos itens juntar (inclui 1 dentro da casa)
  kitId?: string           // tema visual (kit); default = Vilarejo
  mecanica?: 'contar' | 'somar' | 'selecionar' | 'ordenar' | 'agrupar'
  alvoSoma?: number        // somar: a soma exata (8 | 12 | 18)
  kc?: string              // o componente de conhecimento (domínio POR conteúdo)
  itens?: Array<{ rotulo: string, ok: boolean, ordem?: number }>   // selecionar/ordenar
  agTotal?: number         // agrupar: total de itens a repartir (8 | 12 | 18)
  agCaixas?: number        // agrupar: máximo de caixas disponíveis (vagas)
  agTodas?: boolean        // DIVISÃO como partilha: TODAS as caixas têm que receber (12÷3)
}

// somar: fichas por tier — 3 valores que FECHAM a soma + 2 distratores (que estouram).
// Determinístico (QA reproduz); várias combinações podem fechar, e isso é pedagógico.
const FICHAS_SOMA: Record<number, { sol: number[], dis: number[] }> = {
  8: { sol: [1, 3, 4], dis: [6, 5] },
  12: { sol: [3, 4, 5], dis: [7, 6] },
  18: { sol: [4, 6, 8], dis: [9, 7] }
}

const T = 16
const CHAO_FG = 1
const PAR_FG = 1001
const pg = (id: number): number => PAR_FG + id

type Grid = number[]

export function montarMapaFase (plano: PlanoMapa): object {
  const kit = getKit(plano.kitId)
  const GRAMA = CHAO_FG + kit.chao.grama
  const PISO_INT = CHAO_FG + kit.chao.pisoInterno
  const PAR = { TL: kit.paredes.TL, T: kit.paredes.T, TR: kit.paredes.TR, L: kit.paredes.L, R: kit.paredes.R, BL: kit.paredes.BL, B: kit.paredes.B, BR: kit.paredes.BR, SOLIDO: kit.paredes.solido }
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

  // casa + porta — a colisão cobre o SPRITE inteiro (64px = 4 tiles + beirais),
  // não só o miolo 3x2: antes dava pra atravessar as laterais do telhado
  const casa = { x: 3, y: 3 }
  for (let dy = 0; dy < 2; dy++) for (let dx = -1; dx < 4; dx++) put(colis, casa.x + dx, casa.y + dy, COL)
  const porta = { x: casa.x + 1, y: casa.y + 2 }

  // árvores (colisão na base)
  const arvores = [[2, 9], [16, 3], [15, 9], [11, 11], [6, 12]]
  for (const [x, y] of arvores) put(colis, x, y, COL)

  // pedras que fecham a saída
  const pedras = { x: OX1, y: SAI_Y }
  put(colis, pedras.x, pedras.y, COL)

  // CARROÇA ao lado do fazendeiro (a história fica VISÍVEL: é nela que a carga vai)
  const carroca = { x: 11, y: 6 }
  put(colis, carroca.x, carroca.y, COL)

  // interior (sala) — chão + auto-parede com saída no meio de baixo
  const saiSalaX = IX0 + ((IW - 1) >> 1)
  for (let y = IY0; y < IY0 + IH; y++) for (let x = IX0; x < IX0 + IW; x++) put(chao, x, y, PISO_INT)
  moldura(IX0, IY0, IW, IH, (x, y) => y === IY0 + IH - 1 && x === saiSalaX)
  const interiorEntra = { x: saiSalaX, y: IY0 + IH - 2 }
  const interiorSai = { x: saiSalaX, y: IY0 + IH - 1 }

  // MEL: 1 dentro da casa + (melAlvo-1) espalhados no externo, em tiles de chão livres
  const fazendeiro = { x: 9, y: 6 }
  const candidatos: number[][] = [[6, 6], [13, 5], [8, 10], [14, 12], [12, 8], [5, 12], [16, 11], [7, 4]]
  const ocupado = (x: number, y: number): boolean =>
    colis[y * W + x] !== 0 || (x === fazendeiro.x && y === fazendeiro.y) || (x === porta.x && y === porta.y)
  const mecanica = plano.mecanica ?? 'contar'
  const somar = mecanica === 'somar'
  const comItens = mecanica === 'selecionar' || mecanica === 'ordenar'
  const agrupar = mecanica === 'agrupar'
  const alvoSoma = somar ? (FICHAS_SOMA[plano.alvoSoma ?? 12] ? (plano.alvoSoma ?? 12) : 12) : 0
  const livres = candidatos.filter(c => !ocupado(c[0], c[1]))
  const melExternos: number[][] = []
  const melValores: number[][] = []            // somar: [x, y, valor]
  const melItens: number[][] = []              // selecionar/ordenar: [x, y, índice do item]
  if (somar) {
    // 5 fichas: intercala solução e distrator em posições livres (determinístico p/ o QA)
    const f = FICHAS_SOMA[alvoSoma]
    const valores = [f.sol[0], f.dis[0], f.sol[1], f.dis[1], f.sol[2]]
    for (let i = 0; i < valores.length && i < livres.length; i++) melValores.push([livres[i][0], livres[i][1], valores[i]])
  } else if (comItens) {
    // um item rotulado do CONTEÚDO em cada posição livre (a ordem dos itens já vem embaralhada)
    const itens = plano.itens ?? []
    for (let i = 0; i < itens.length && i < livres.length; i++) melItens.push([livres[i][0], livres[i][1], i])
  } else if (!agrupar) {
    for (const c of livres) { if (melExternos.length >= melAlvo - 1) break; melExternos.push(c) }
  }
  const melInterno = (somar || comItens || agrupar) ? [] : [saiSalaX, IY0 + 2]

  // AGRUPAR: N itens espalhados + fileira de VAGAS de caixa + PILHA de caixas.
  // Determinístico (o QA reproduz). As vagas ficam na faixa de baixo, espaçadas de 2
  // (andar entre elas sem "entrar" numa vaga sem querer); a pilha ao lado.
  const agTotal = agrupar ? (plano.agTotal ?? 12) : 0
  const agCaixas = agrupar ? Math.max(2, Math.min(6, plano.agCaixas ?? 6)) : 0
  const agItens: number[][] = []
  const agVagas: number[][] = []
  const agPilha = [17, 13]
  if (agrupar) {
    for (let i = 0; i < agCaixas; i++) agVagas.push([3 + i * 2, 13])
    const evitar = (x: number, y: number): boolean =>
      ocupado(x, y) || (Math.abs(y - 13) < 2 && x <= 4 + agCaixas * 2) ||           // fileira de vagas
      (x === agPilha[0] && y === agPilha[1]) || (x === 10 && y === 12) ||            // pilha + spawn do herói
      (Math.abs(x - fazendeiro.x) + Math.abs(y - fazendeiro.y) <= 2)                 // longe do fazendeiro (o TESTE é lá)
    // varredura determinística por linhas (espalha pelo campo, longe das vagas)
    fora: for (let y = 2; y <= 11; y++) {
      for (let x = 2; x <= 18; x += 2) {
        const xx = (y % 2 === 0) ? x : x + 1                                        // ziguezague
        if (xx > 18 || evitar(xx, y)) continue
        agItens.push([xx, y])
        if (agItens.length >= agTotal) break fora
      }
    }
  }

  // DECOR (enfeites como objetos — o motor só renderiza o que o mapa manda).
  // "depth" opcional: força a profundidade (tapete rente ao chão, pote sobre a estante).
  let oid = 1
  const obj = (frame: string, tex: string, xpx: number, ypx: number, depth?: number): object => ({ id: oid++, name: frame, type: 'decor', x: xpx, y: ypx, width: 0, height: 0, point: true, visible: true, rotation: 0, properties: [{ name: 'tex', type: 'string', value: tex }, ...(depth !== undefined ? [{ name: 'depth', type: 'int', value: depth }] : [])] })
  const decor: object[] = [obj('casa_a', 'mundo', (casa.x + 1.5) * T, (casa.y + 2) * T)]
  for (const [ax, ay] of arvores) decor.push(obj('arvore', 'mundo', (ax + 0.5) * T, (ay + 1) * T + 6))
  decor.push(obj('carroca', 'mundo', (carroca.x + 0.5) * T, (carroca.y + 1) * T))
  // CASA MOBILIADA (pedido do Marcos): tapete no meio (passável), estante encostada
  // na parede com 2 potes em cima, baú no canto — e os móveis SÓLIDOS (colisão),
  // pra criança não atravessar a mobília
  decor.push(obj('tapete', 'mundo', (IX0 + 4.5) * T, (IY0 + 5) * T, 2))
  decor.push(obj('estante', 'mundo', (IX0 + 2) * T, (IY0 + 2) * T))
  decor.push(obj('mel', 'mel', (IX0 + 1.6) * T, (IY0 + 1.65) * T, (IY0 + 2) * T + 2))
  decor.push(obj('mel', 'mel', (IX0 + 2.4) * T, (IY0 + 1.65) * T, (IY0 + 2) * T + 2))
  decor.push(obj('bau', 'bau', (IX0 + IW - 2.5) * T, (IY0 + 2) * T))
  for (const [fx, fy] of [[IX0 + 1, IY0 + 1], [IX0 + 2, IY0 + 1], [IX0 + IW - 3, IY0 + 1]]) put(colis, fx, fy, COL)

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
      { firstgid: CHAO_FG, name: 'chao', image: kit.imagens.chao, imagewidth: kit.chao.imagewidth, imageheight: kit.chao.imageheight, tilewidth: T, tileheight: T, columns: kit.chao.cols, tilecount: kit.chao.tilecount, margin: 0, spacing: 0 },
      { firstgid: PAR_FG, name: 'paredes', image: kit.imagens.paredes, imagewidth: kit.paredes.imagewidth, imageheight: kit.paredes.imageheight, tilewidth: T, tileheight: T, columns: kit.paredes.cols, tilecount: kit.paredes.tilecount, margin: 0, spacing: 0, tiles: tilesProp }
    ],
    properties: [
      Pi('heroiX', 10), Pi('heroiY', 12),
      Pi('casaX', casa.x), Pi('casaY', casa.y), Pi('portaX', porta.x), Pi('portaY', porta.y),
      Pi('fazX', fazendeiro.x), Pi('fazY', fazendeiro.y),
      Pi('carrocaX', carroca.x), Pi('carrocaY', carroca.y),
      Pi('pedrasX', pedras.x), Pi('pedrasY', pedras.y), Pi('saidaY', SAI_Y),
      Pi('intEntraX', interiorEntra.x), Pi('intEntraY', interiorEntra.y),
      Pi('intSaiX', interiorSai.x), Pi('intSaiY', interiorSai.y),
      Ps('melExternos', melExternos), Ps('melInterno', melInterno),
      Ps('mecanica', mecanica), Pi('alvoSoma', alvoSoma), Ps('melValores', melValores),
      Ps('kc', plano.kc ?? mecanica), Ps('itens', plano.itens ?? []), Ps('melItens', melItens),
      Pi('agTotal', agTotal), Pi('agCaixas', agCaixas), Pi('agTodas', agrupar && plano.agTodas ? 1 : 0),
      Ps('agItens', agItens), Ps('agVagas', agVagas), Ps('agPilha', agPilha),
      Ps('arvores', arvores), Ps('interior', { x0: IX0, y0: IY0, w: IW, h: IH })
    ]
  }
}
