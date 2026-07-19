// ============================================================================
// FÁBRICA (v1) — o "clica GERAR". O professor preenche o formulário e sai a fase
// jogável, montada no motor novo (FaseGrid). Sem programar, sem desenhar.
// Fluxo: PEDIDO -> planejar() [valida Zod + Portão 0] -> montarMapaFase() [mapa Tiled
// na hora] -> injeta no cache do Phaser -> inicia FaseGrid com o mapa e os textos.
// ============================================================================
import Phaser from 'phaser'
import { FaseGrid } from '../rpg/FaseGrid'
import { PedidoAtividade, DISCIPLINAS, DIFICULDADES } from './tipos'
import { planejarPedagogiaIA } from './pedagogo'
import { escreverRoteiro } from './roteiro'
import { carrega } from './motor-adaptativo'
import { kitsDisponiveis, KIT_PADRAO } from './kits'
import { montarMapaFase } from './mapaFase'

// do PRÉ ao 9º (a exigência do Marcos): a MECÂNICA muda com o ano — o pedagogo decide
const ANOS = ['Pré', '1º ano', '2º ano', '3º ano', '4º ano', '5º ano', '6º ano', '7º ano', '8º ano', '9º ano']
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
        <label>Visual (kit de arte)<br><select id="f_kit" style="width:100%">${kitsDisponiveis().map(k => `<option value="${k.id}">${k.nome}</option>`).join('')}</select></label>
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

  const btn = document.getElementById('fgerar') as HTMLButtonElement
  btn.onclick = async () => {
    const erro = document.getElementById('ferro')!
    erro.textContent = ''
    const bruto = {
      ano: val('f_ano'), disciplina: val('f_disc'), objetivo: val('f_obj'),
      tema: val('f_tema'), tempoMin: Number(val('f_tempo')), dificuldade: val('f_dif')
    }
    const parsed = PedidoAtividade.safeParse(bruto)
    if (!parsed.success) { erro.textContent = '⚠️ ' + parsed.error.issues.map(i => i.message).join('; '); return }
    // 1º) o PEDAGOGO planeja a APRENDIZAGEM (banco instantâneo; conteúdo desconhecido -> IA
    //     com prazo e fallback — nunca trava). 1.5) ADAPTA AO RITMO (DDA/ZDP) ANTES da
    //     história, pra fala e mapa baterem. 2º) o ROTEIRISTA veste em cima.
    btn.disabled = true; const btnTxt = btn.textContent; btn.textContent = '⏳ Gerando a aventura…'
    let roteiro, espinha, alvo: number, alvoSoma: number | undefined, viaIA = false
    try {
      const plan = await planejarPedagogiaIA(parsed.data)
      espinha = plan.espinha; viaIA = plan.viaIA
      const kc = espinha.kc                             // o domínio é POR CONTEÚDO
      alvo = espinha.alvo; alvoSoma = espinha.alvoSoma
      const pk = carrega('local')[kc]?.pKnown
      if (pk !== undefined) {
        if (espinha.mecanica === 'somar') {
          // somar: sobe/desce de TIER (8 -> 12 -> 18) conforme o domínio
          const tiers = [8, 12, 18]
          let i = Math.max(0, tiers.indexOf(alvoSoma ?? 12))
          if (pk >= 0.8) i = Math.min(tiers.length - 1, i + 1)
          else if (pk < 0.4) i = Math.max(0, i - 1)
          alvoSoma = tiers[i]
        } else if (espinha.mecanica === 'contar') {
          if (pk >= 0.8) alvo = Math.min(9, alvo + 1); else if (pk < 0.4) alvo = Math.max(2, alvo - 1)
        }
        // selecionar/ordenar: o próprio conteúdo define o desafio (a IA gera itens mais
        // difíceis conforme o domínio — próximo passo do gerador de conteúdo)
      }
      roteiro = escreverRoteiro(parsed.data, { alvo, alvoSoma, mecanica: espinha.mecanica, regra: espinha.regra, necessidadeMundo: espinha.necessidadeMundo })
    } catch (e) { erro.textContent = '⚠️ ' + String((e as Error).message); return } finally { btn.disabled = false; btn.textContent = btnTxt }
    ;(window as any).__fabricaEspinha = espinha
    ;(window as any).__fabricaViaIA = viaIA
    ;(window as any).__fabricaAlvo = espinha.mecanica === 'somar' ? alvoSoma : alvo   // QA lê

    // o kit visual: o que o professor escolheu (senão o sugerido pelo roteiro)
    const kitId = (document.getElementById('f_kit') as HTMLSelectElement)?.value || roteiro.kitId || KIT_PADRAO
    const mapa = montarMapaFase({ melAlvo: alvo, kitId, mecanica: espinha.mecanica, alvoSoma, kc: espinha.kc, itens: espinha.itens })
    const key = 'mapa_fabrica'
    if (game.cache.tilemap.has(key)) game.cache.tilemap.remove(key)
    game.cache.tilemap.add(key, { format: Phaser.Tilemaps.Formats.TILED_JSON, data: mapa } as any)
    host.style.display = 'none'
    if (game.scene.getScene('FaseGrid')) game.scene.remove('FaseGrid')
    game.scene.add('FaseGrid', FaseGrid, true, {
      mapaKey: key, kitId,
      plano: {
        abertura: roteiro.falas.abertura, problema: roteiro.falas.pedido, juntouTudo: roteiro.falas.juntouTudo,
        entrega: roteiro.falas.entrega, vitoria: roteiro.falas.vitoria, emoji: roteiro.personagem.emoji,
        nome: roteiro.personagem.nome, regra: espinha.regra
      }
    })
    ;(window as any).__fabricaRoteiro = roteiro   // QA lê a história gerada
  }

  ;(window as any).__fabrica = { gerar: () => (document.getElementById('fgerar') as HTMLButtonElement).click(), set: (id: string, v: string) => { (document.getElementById(id) as HTMLInputElement).value = v } }
}
