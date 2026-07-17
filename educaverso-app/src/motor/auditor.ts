// ============================================================================
// AUDITOR AUTOMÁTICO DE COERÊNCIA (o "robô-fiscal")
// Confere a aventura ANTES/DURANTE a montagem e aponta problemas:
//  - asset faltando (peça que não existe no kit)
//  - peça FORA do mundo (fora dos limites)
//  - "COQUEIRO DENTRO DO MAR" (peça de terra numa zona de água)
//  - água/poça na terra seca
//  - sobreposição feia (duas peças no mesmo lugar)
//  - herói começando na água / fora do mundo
//  - (runtime) fala usada sem áudio
// CADA erro novo que aparecer vira uma REGRA nova aqui → não repete (aprende).
// ============================================================================
import type { TAventura } from './aventura'

export interface Problema { grave: boolean; msg: string }

function dentroDeAgua (x: number, y: number, zonas: { x: number, y: number, w: number, h: number }[]) {
  return zonas.some(z => x >= z.x && x <= z.x + z.w && y >= z.y && y <= z.y + z.h)
}

export function auditar (av: TAventura, opts: { assets: Set<string>, audios?: Set<string> } = { assets: new Set() }): Problema[] {
  const p: Problema[] = []
  const A = opts.assets, W = av.mundo.largura, H = av.mundo.altura, agua = av.mundo.zonas_agua

  // herói
  if (av.inicio.x < 0 || av.inicio.x > W || av.inicio.y < 0 || av.inicio.y > H) p.push({ grave: true, msg: 'Herói começa FORA do mundo.' })
  if (dentroDeAgua(av.inicio.x, av.inicio.y, agua)) p.push({ grave: true, msg: 'Herói começa DENTRO DA ÁGUA.' })

  const colocados: { x: number, y: number, asset: string }[] = []
  for (const par of av.paradas) {
    for (const o of par.objetos) {
      // asset existe?
      if (A.size && !A.has(o.asset)) p.push({ grave: true, msg: `[${par.id}] peça "${o.asset}" NÃO existe no kit.` })
      // dentro do mundo?
      if (o.x < 0 || o.x > W || o.y < 0 || o.y > H) p.push({ grave: true, msg: `[${par.id}] "${o.asset}" está FORA do mundo (${o.x},${o.y}).` })
      // coerência de terreno (coqueiro no mar!)
      const naAgua = dentroDeAgua(o.x, o.y, agua)
      if (o.terreno === 'terra' && naAgua) p.push({ grave: true, msg: `[${par.id}] "${o.asset}" (de terra) está DENTRO DA ÁGUA — coqueiro no mar!` })
      if (o.terreno === 'agua' && !naAgua && agua.length) p.push({ grave: false, msg: `[${par.id}] "${o.asset}" (de água) está na TERRA SECA.` })
      // sobreposição feia
      for (const c of colocados) if (Math.hypot(c.x - o.x, c.y - o.y) < 30) { p.push({ grave: false, msg: `[${par.id}] "${o.asset}" quase em cima de "${c.asset}".` }); break }
      colocados.push({ x: o.x, y: o.y, asset: o.asset })
    }
    // cobertura de voz (runtime): toda fala usada precisa de áudio
    if (opts.audios) for (const f of par.falas) if (!opts.audios.has(f.id)) p.push({ grave: false, msg: `[${par.id}] fala "${f.id}" SEM áudio (voz).` })
  }
  return p
}
