// ============================================================================
// AUDITOR AUTOMÁTICO DE COERÊNCIA (o "robô-fiscal") — v2: audita o GRAFO DE ZONAS
// Confere a aventura ANTES/DURANTE a montagem e aponta problemas:
//  - asset faltando · peça fora do mundo · peça fora da faixa ANDÁVEL
//  - sobreposição feia · portal p/ zona sem volta (beco sem saída)
//  - missão: item fora da faixa andável / em cima da cesta
//  - fala usada sem áudio (cobertura de voz)
// CADA erro novo que aparecer vira uma REGRA nova aqui → não repete (aprende).
// ============================================================================
import type { TAventura, TZona } from './aventura'

export interface Problema { grave: boolean; msg: string }

export function auditar (av: TAventura, opts: { assets: Set<string>, audios?: Set<string>, zonaAtual?: string } = { assets: new Set() }): Problema[] {
  const p: Problema[] = []
  const A = opts.assets

  for (const z of av.zonas) {
    const W = z.largura, H = z.altura
    const noMundo = (x: number, y: number) => x >= 0 && x <= W && y >= 0 && y <= H
    const andavel = (y: number) => y >= z.chao_min_y && y <= H - 44

    const colocados: { x: number, y: number, asset: string }[] = []
    for (const par of z.paradas) {
      for (const o of par.objetos) {
        if (A.size && (!opts.zonaAtual || opts.zonaAtual === z.id) && !A.has(o.asset)) p.push({ grave: true, msg: `[${z.id}/${par.id}] peça "${o.asset}" NÃO existe no kit.` })
        if (!noMundo(o.x, o.y)) p.push({ grave: true, msg: `[${z.id}/${par.id}] "${o.asset}" FORA do mundo (${o.x},${o.y}).` })
        for (const c of colocados) if (Math.hypot(c.x - o.x, c.y - o.y) < 30) { p.push({ grave: false, msg: `[${z.id}/${par.id}] "${o.asset}" quase em cima de "${c.asset}".` }); break }
        colocados.push({ x: o.x, y: o.y, asset: o.asset })
      }
      for (const pr of par.personagens) {
        if (!andavel(pr.y)) p.push({ grave: true, msg: `[${z.id}/${par.id}] personagem "${pr.nome}" fora da faixa andável (y=${pr.y}).` })
      }
      if (opts.audios) for (const f of par.falas) if (!opts.audios.has(f.id)) p.push({ grave: false, msg: `[${z.id}/${par.id}] fala "${f.id}" SEM áudio.` })
    }

    // portais: dentro do mundo, na faixa andável, e o grafo tem VOLTA
    for (const pt of z.portais) {
      if (!noMundo(pt.x, pt.y)) p.push({ grave: true, msg: `[${z.id}] portal p/ "${pt.para}" FORA do mundo.` })
      if (!andavel(pt.y)) p.push({ grave: true, msg: `[${z.id}] portal p/ "${pt.para}" fora da faixa andável (y=${pt.y}) — a criança não alcança.` })
      const dest = av.zonas.find(zz => zz.id === pt.para)
      if (dest && !dest.portais.some(v => v.para === z.id) && dest.portais.length > 0) {
        p.push({ grave: false, msg: `[${z.id}] portal p/ "${pt.para}" sem VOLTA direta (confira se é intencional).` })
      }
      if (dest && (pt.spawn.y < dest.chao_min_y || pt.spawn.y > dest.altura - 44)) p.push({ grave: true, msg: `[${z.id}] spawn do portal p/ "${pt.para}" cai fora da faixa andável de lá.` })
    }

    // missão colher: itens alcançáveis, sem colidir com a cesta
    if (z.missao) {
      const mi = z.missao
      if (A.size && (!opts.zonaAtual || opts.zonaAtual === z.id)) { if (!A.has(mi.asset)) p.push({ grave: true, msg: `[${z.id}] missão usa asset "${mi.asset}" que NÃO existe.` }); if (!A.has('cesta')) p.push({ grave: true, msg: `[${z.id}] missão colher exige o asset "cesta" no kit.` }) }
      for (const it of mi.itens) {
        if (!andavel(it.y)) p.push({ grave: true, msg: `[${z.id}] item da missão fora da faixa andável (y=${it.y}).` })
        if (mi.cesta && Math.hypot(it.x - mi.cesta.x, it.y - mi.cesta.y) < 90) p.push({ grave: false, msg: `[${z.id}] item da missão em cima da cesta.` })
      }
      if (opts.audios) for (const id of mi.ao_completar) if (!opts.audios.has(id)) p.push({ grave: false, msg: `[${z.id}] fala de conclusão "${id}" SEM áudio.` })
    }

    if (opts.audios) for (const id of z.chegada) if (!opts.audios.has(id)) p.push({ grave: false, msg: `[${z.id}] fala de chegada "${id}" SEM áudio.` })
  }

  // início do herói na faixa andável da zona inicial
  const zi = av.zonas.find(z => z.id === av.zona_inicial)
  if (zi && (av.inicio.y < zi.chao_min_y || av.inicio.y > zi.altura - 44)) p.push({ grave: true, msg: 'Herói começa fora da faixa andável.' })

  return p
}
