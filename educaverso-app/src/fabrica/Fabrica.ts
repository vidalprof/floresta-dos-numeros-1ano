// ============================================================================
// FÁBRICA (v1) — o "clica GERAR". O professor preenche o formulário e sai a fase
// jogável, montada no motor novo (FaseGrid). Sem programar, sem desenhar.
// Fluxo: PEDIDO -> planejar() [valida Zod + Portão 0] -> montarMapaFase() [mapa Tiled
// na hora] -> injeta no cache do Phaser -> inicia FaseGrid com o mapa e os textos.
// ============================================================================
import Phaser from 'phaser'
import { FaseGrid } from '../rpg/FaseGrid'
import { PedidoAtividade, planejar, DISCIPLINAS, DIFICULDADES } from './tipos'

const ANOS = ['Pré', '1º ano', '2º ano', '3º ano', '4º ano', '5º ano']
const TEMAS = ['fazenda', 'floresta', 'espaço', 'mar']

export function montarFabrica (game: Phaser.Game): void {
  const host = document.createElement('div')
  host.id = 'fabrica'
  host.style.cssText = 'position:fixed;inset:0;z-index:50;overflow:auto;background:linear-gradient(160deg,#10203f,#0a1226);color:#eaf1ff;font-family:system-ui,Arial,sans-serif;padding:22px 14px;'
  const opt = (arr: readonly string[]): string => arr.map(a => `<option value="${a}">${a}</option>`).join('')
  host.innerHTML = `
    <div style="max-width:560px;margin:0 auto">
      <h1 style="font-size:23px;margin:.2em 0">🏭 Fábrica de Aventuras</h1>
      <p style="color:#a9bde6;margin:.2em 0 14px;font-size:14px">Preencha e clique <b>GERAR</b>. A aventura jogável nasce na hora — sem programar, sem desenhar.</p>
      <div id="fcampos" style="display:grid;gap:10px">
        <label>Ano<br><select id="f_ano" style="width:100%">${opt(ANOS)}</select></label>
        <label>Disciplina<br><select id="f_disc" style="width:100%">${opt(DISCIPLINAS)}</select></label>
        <label>Objetivo de aprendizagem (BNCC)<br><input id="f_obj" value="Contar quantidades até 10" style="width:100%"></label>
        <label>Tema do cenário<br><select id="f_tema" style="width:100%">${opt(TEMAS)}</select></label>
        <div style="display:flex;gap:10px">
          <label style="flex:1">Tempo (min)<br><input id="f_tempo" type="number" value="55" min="5" max="90" style="width:100%"></label>
          <label style="flex:1">Dificuldade<br><select id="f_dif" style="width:100%">${opt(DIFICULDADES)}</select></label>
        </div>
      </div>
      <div id="ferro" style="color:#ffb3b3;min-height:20px;margin:8px 0;font-size:14px"></div>
      <button id="fgerar" style="width:100%;padding:14px;font-size:18px;font-weight:800;border:0;border-radius:12px;background:#57e08a;color:#0b2350;cursor:pointer;box-shadow:0 4px 0 #2e9c5b">▶ GERAR aventura</button>
      <p style="color:#7f93bd;font-size:12px;margin-top:10px">v1: mecânica “contar/juntar”. O catálogo (repartir, ordenar…) e a IA de história entram nas próximas versões.</p>
    </div>`
  document.body.appendChild(host)
  const val = (id: string): string => (document.getElementById(id) as HTMLInputElement).value

  ;(document.getElementById('fgerar') as HTMLButtonElement).onclick = () => {
    const erro = document.getElementById('ferro')!
    erro.textContent = ''
    const bruto = {
      ano: val('f_ano'), disciplina: val('f_disc'), objetivo: val('f_obj'),
      tema: val('f_tema'), tempoMin: Number(val('f_tempo')), dificuldade: val('f_dif')
    }
    const parsed = PedidoAtividade.safeParse(bruto)
    if (!parsed.success) { erro.textContent = '⚠️ ' + parsed.error.issues.map(i => i.message).join('; '); return }
    let plano
    try { plano = planejar(parsed.data) } catch (e) { erro.textContent = '⚠️ ' + String((e as Error).message); return }

    // monta o mapa NA HORA e injeta no cache do Phaser
    import('./mapaFase').then(({ montarMapaFase }) => {
      const mapa = montarMapaFase({ melAlvo: plano.melAlvo })
      const key = 'mapa_fabrica'
      if (game.cache.tilemap.has(key)) game.cache.tilemap.remove(key)
      game.cache.tilemap.add(key, { format: Phaser.Tilemaps.Formats.TILED_JSON, data: mapa } as any)
      host.style.display = 'none'
      if (game.scene.getScene('FaseGrid')) game.scene.remove('FaseGrid')
      game.scene.add('FaseGrid', FaseGrid, true, {
        mapaKey: key,
        plano: { problema: plano.problema, entrega: plano.entrega, vitoria: plano.vitoria, emoji: plano.emoji }
      })
      ;(window as any).__fabricaPlano = plano   // QA lê o que foi gerado
    })
  }

  ;(window as any).__fabrica = { gerar: () => (document.getElementById('fgerar') as HTMLButtonElement).click(), set: (id: string, v: string) => { (document.getElementById(id) as HTMLInputElement).value = v } }
}
