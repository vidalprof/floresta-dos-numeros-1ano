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
import { carrega, kcsParaRevisar } from './motor-adaptativo'
import { kitsDisponiveis, KIT_PADRAO } from './kits'
import { montarMapaFase } from './mapaFase'
import { getAluno, setAluno, sincronizarFila } from './evidencias'

// IDENTIFICAÇÃO LEVE (laboratório compartilhado): nome + turma no 1º acesso — é o
// que liga a jogada à avaliação descritiva do professor. "Jogar sem registrar"
// existe (demo/visita); robô de QA (webdriver) nunca vê esta tela.
const TURMAS = ['1º ano', '2º ano', '3º ano', '4º ano', '5º ano', '6º ano', '7º ano', '8º ano', '9º ano']
function garantirIdentidade (): Promise<void> {
  if ((navigator as any).webdriver || getAluno()) return Promise.resolve()
  return new Promise(resolve => {
    const m = document.createElement('div')
    m.style.cssText = 'position:fixed;inset:0;z-index:70;background:#0b1226ee;display:flex;align-items:center;justify-content:center;font-family:system-ui,Arial,sans-serif'
    m.innerHTML = `
      <div style="background:#16244a;color:#eaf1ff;border-radius:16px;padding:22px;max-width:340px;width:92%;text-align:center">
        <div style="font-size:38px">🧑‍🚀</div>
        <h2 style="margin:.3em 0;font-size:20px">Quem vai jogar?</h2>
        <input id="id_nome" placeholder="Seu primeiro nome" style="width:100%;padding:12px;border-radius:10px;border:0;font-size:16px;margin:6px 0">
        <select id="id_turma" style="width:100%;padding:12px;border-radius:10px;border:0;font-size:16px;margin:6px 0">
          <option value="">Sua turma…</option>${TURMAS.map(t => `<option>${t}</option>`).join('')}
        </select>
        <div style="display:flex;gap:10px;justify-content:center;margin:6px 0">
          <button id="id_av1" data-av="heroi" style="flex:1;padding:10px;font-size:26px;border-radius:10px;border:3px solid #57e08a;background:#0e1a38;cursor:pointer">👦</button>
          <button id="id_av2" data-av="menina" style="flex:1;padding:10px;font-size:26px;border-radius:10px;border:3px solid transparent;background:#0e1a38;cursor:pointer">👧</button>
        </div>
        <button id="id_ok" style="width:100%;padding:13px;font-size:17px;font-weight:800;border:0;border-radius:10px;background:#57e08a;color:#0b2350;cursor:pointer;margin-top:6px">▶ Começar!</button>
        <button id="id_pular" style="width:100%;padding:8px;border:0;border-radius:8px;background:transparent;color:#8fa3cf;cursor:pointer;font-size:13px;margin-top:6px">Jogar sem registrar</button>
      </div>`
    document.body.appendChild(m)
    const fim = (): void => { m.remove(); resolve() }
    let avatar: 'heroi' | 'menina' = 'heroi'
    for (const id of ['id_av1', 'id_av2']) {
      ;(m.querySelector('#' + id) as HTMLButtonElement).onclick = (e) => {
        avatar = ((e.currentTarget as HTMLElement).dataset.av as 'heroi' | 'menina')
        ;(m.querySelector('#id_av1') as HTMLElement).style.borderColor = avatar === 'heroi' ? '#57e08a' : 'transparent'
        ;(m.querySelector('#id_av2') as HTMLElement).style.borderColor = avatar === 'menina' ? '#57e08a' : 'transparent'
      }
    }
    ;(m.querySelector('#id_ok') as HTMLButtonElement).onclick = () => {
      const nome = (m.querySelector('#id_nome') as HTMLInputElement).value.trim()
      const turma = (m.querySelector('#id_turma') as HTMLSelectElement).value
      if (!nome || !turma) { (m.querySelector('#id_nome') as HTMLInputElement).placeholder = 'Preencha o nome e a turma!'; return }
      setAluno({ nome, turma, avatar }); fim()
    }
    ;(m.querySelector('#id_pular') as HTMLButtonElement).onclick = fim
  })
}

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

  void sincronizarFila()   // evidências represadas (sem internet na hora) sobem no boot

  const btn = document.getElementById('fgerar') as HTMLButtonElement
  btn.onclick = async () => {
    const erro = document.getElementById('ferro')!
    erro.textContent = ''
    await garantirIdentidade()
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
    let roteiro, espinha, alvo: number, alvoSoma: number | undefined, agTotal: number | undefined, viaIA = false
    try {
      const plan = await planejarPedagogiaIA(parsed.data)
      espinha = plan.espinha; viaIA = plan.viaIA
      const kc = espinha.kc                             // o domínio é POR CONTEÚDO
      alvo = espinha.alvo; alvoSoma = espinha.alvoSoma; agTotal = espinha.agTotal
      const pk = carrega('local')[kc]?.pKnown
      if (pk !== undefined) {
        if (espinha.mecanica === 'somar') {
          // somar: sobe/desce de TIER (8 -> 12 -> 18) conforme o domínio
          const tiers = [8, 12, 18]
          let i = Math.max(0, tiers.indexOf(alvoSoma ?? 12))
          if (pk >= 0.8) i = Math.min(tiers.length - 1, i + 1)
          else if (pk < 0.4) i = Math.max(0, i - 1)
          alvoSoma = tiers[i]
        } else if (espinha.mecanica === 'agrupar') {
          // agrupar: sobe/desce o TOTAL (8 -> 12 -> 18) conforme o domínio
          const tiers = [8, 12, 18]
          let i = Math.max(0, tiers.indexOf(agTotal ?? 12))
          if (pk >= 0.8) i = Math.min(tiers.length - 1, i + 1)
          else if (pk < 0.4) i = Math.max(0, i - 1)
          agTotal = tiers[i]
        } else if (espinha.mecanica === 'contar') {
          if (pk >= 0.8) alvo = Math.min(9, alvo + 1); else if (pk < 0.4) alvo = Math.max(2, alvo - 1)
        }
        // selecionar/ordenar: o próprio conteúdo define o desafio (a IA gera itens mais
        // difíceis conforme o domínio — próximo passo do gerador de conteúdo)
      }
      roteiro = escreverRoteiro(parsed.data, { alvo, alvoSoma, agTotal, mecanica: espinha.mecanica, regra: espinha.regra, necessidadeMundo: espinha.necessidadeMundo })
    } catch (e) { erro.textContent = '⚠️ ' + String((e as Error).message); return } finally { btn.disabled = false; btn.textContent = btnTxt }
    ;(window as any).__fabricaEspinha = espinha
    ;(window as any).__fabricaViaIA = viaIA
    ;(window as any).__fabricaAlvo = espinha.mecanica === 'somar' ? alvoSoma : (espinha.mecanica === 'agrupar' ? agTotal : alvo)   // QA lê

    // o kit visual: o que o professor escolheu (senão o sugerido pelo roteiro)
    const kitId = (document.getElementById('f_kit') as HTMLSelectElement)?.value || roteiro.kitId || KIT_PADRAO
    const planoDe = (r: typeof roteiro): Record<string, unknown> => ({
      abertura: r.falas.abertura, problema: r.falas.pedido, juntouTudo: r.falas.juntouTudo,
      entrega: r.falas.entrega, vitoria: r.falas.vitoria, emoji: r.personagem.emoji,
      nome: r.personagem.nome, regra: espinha.regra
    })
    // ---- ARCO DE MISSÕES (a aula continua depois da vitória) ----
    const planoBase = planoDe(roteiro) as any
    planoBase.tutorial = parsed.data.dificuldade === 'facil'   // 1ª missão fácil = mentor guia sozinho
    // MISSÃO DE REVISÃO (Leitner): se o retorno espaçado deste conteúdo venceu, avisa
    try { if (kcsParaRevisar(carrega('local'), Date.now()).includes(espinha.kc)) planoBase.abertura = '🔁 Missão de revisão — bora relembrar! ' + (planoBase.abertura ?? '') } catch { /* segue */ }
    // ARCO da aventura (aula ~50 min segmentada — pesquisa: 3+ fases curtas + variação
    // de cenário + os "4 passos" + Dienes). Multiplicar (fazenda→floresta) sobe 12→18;
    // depois DIVIDIR como partilha em 3 lugares (rio ÷3, pomar ÷3 maior, montanha ÷4).
    // Cada parada = cenário novo (não enjoa) + um passo real da matemática (não é pote
    // repetido). O auditor de duração e o QA leem este arco automaticamente.
    const mult = (cenario: string, total: number, local: string, abertura: string): { mapa: object, plano: any, local: string } =>
      ({ mapa: montarMapaFase({ melAlvo: alvo, kitId, mecanica: 'agrupar', kc: espinha.kc, agTotal: total, agCaixas: espinha.agCaixas, cenario }), plano: { ...planoBase, abertura }, local })
    const div = (cenario: string, total: number, caixas: number, local: string, t: any): { mapa: object, plano: any, local: string } =>
      ({ mapa: montarMapaFase({ melAlvo: alvo, kitId, mecanica: 'agrupar', kc: 'particao-igual', agTotal: total, agCaixas: caixas, agTodas: true, cenario }), plano: { ...t, emoji: roteiro.personagem.emoji, nome: roteiro.personagem.nome, regra: 'repartir igualmente entre TODOS' }, local })

    const missoes: Array<{ mapa: object, plano: any, local: string }> = []
    if (espinha.mecanica !== 'agrupar') {
      missoes.push({ mapa: montarMapaFase({ melAlvo: alvo, kitId, mecanica: espinha.mecanica, alvoSoma, kc: espinha.kc, itens: espinha.itens, agTotal, agCaixas: espinha.agCaixas, cenario: 'fazenda' }), plano: planoBase, local: 'a Fazenda do Tião' })
    } else {
      missoes.push({ mapa: montarMapaFase({ melAlvo: alvo, kitId, mecanica: 'agrupar', kc: espinha.kc, agTotal: 12, agCaixas: espinha.agCaixas, cenario: 'fazenda' }), plano: planoBase, local: 'a Fazenda do Tião' })
      missoes.push(mult('floresta', 18, 'a Trilha da Floresta 🌲', 'A notícia se espalhou — a encomenda CRESCEU! Agora são mais potes pra arrumar.'))
      missoes.push(div('rio', 12, 3, 'o Mercado da Beira do Rio 🌊', {
        abertura: 'A carroça chegou ao rio: 3 fregueses esperam, cada um com a SUA caixa!',
        problema: 'São 3 caixas — uma pra CADA freguês — e ninguém aceita menos que o outro. Como repartir os 12 potes pra ficar justo?',
        juntouTudo: 'Tudo repartido! Vem conferir comigo.', entrega: 'Contas justas, fregueses felizes!',
        vitoria: 'Você DIVIDIU: 12÷3! Bora pro pomar! 🌟'
      }))
      missoes.push(div('pomar', 18, 3, 'o Pomar das Cerejeiras 🌸', {
        abertura: 'No pomar a colheita rendeu 18 potes — e de novo são 3 cestas iguais!',
        problema: '18 potes, 3 cestas, tudo igual. Quantos vão em CADA cesta?',
        juntouTudo: 'Repartido! Confere comigo.', entrega: 'Cada cesta com o seu tanto certinho!',
        vitoria: '18÷3=6! Você mandou muito bem! 🌟'
      }))
      missoes.push(div('montanha', 12, 4, 'o Alto da Montanha ⛰️', {
        abertura: 'No alto da montanha, 4 amigos dividem a ÚLTIMA carga da aventura!',
        problema: 'Agora são 4 caixas iguais pra 12 potes. Quantos em cada uma?',
        juntouTudo: 'Tudo certo! Vem ver.', entrega: 'Divisão perfeita — todo mundo com o mesmo tanto!',
        vitoria: 'AULA COMPLETA! Você multiplicou E dividiu de vários jeitos! 🏆'
      }))
    }
    let mi = 0
    const montaMissao = (i: number): void => {
      const key = 'mapa_fabrica'
      if (game.cache.tilemap.has(key)) game.cache.tilemap.remove(key)
      game.cache.tilemap.add(key, { format: Phaser.Tilemaps.Formats.TILED_JSON, data: missoes[i].mapa } as any)
      host.style.display = 'none'
      if (game.scene.getScene('FaseGrid')) game.scene.remove('FaseGrid')
      game.scene.add('FaseGrid', FaseGrid, true, { mapaKey: key, kitId, plano: { ...missoes[i].plano, temProxima: i < missoes.length - 1 } })
    }
    // CELEBRAÇÃO de transição (pesquisa: a passagem de fase VIRA recompensa — a criança
    // sente a "jornada"). Estrela + fanfarra + "Rumo a <lugar>" por ~2,6s, aí monta.
    const celebra = (local: string, cb: () => void): void => {
      if ((navigator as any).webdriver) { cb(); return }   // QA não espera a festa
      const ov = document.createElement('div')
      ov.style.cssText = 'position:fixed;inset:0;z-index:80;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle,#123a7a 0%,#0a1226 80%);color:#fff;font-family:system-ui,Arial,sans-serif;animation:apf .3s'
      ov.innerHTML = `<div style="font-size:70px;animation:pf 1.2s ease-in-out infinite">🌟</div>
        <div style="font-size:26px;font-weight:800;margin:6px">Muito bem!</div>
        <div style="font-size:17px;color:#bcd0ff">Rumo a ${local}…</div>`
      const st = document.createElement('style'); st.textContent = '@keyframes pf{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}@keyframes apf{from{opacity:0}to{opacity:1}}'
      ov.appendChild(st); document.body.appendChild(ov)
      try { const A = new AudioContext(); [523, 659, 784, 1047].forEach((f, i) => { const o = A.createOscillator(), g = A.createGain(); o.type = 'triangle'; o.frequency.value = f; g.gain.value = 0.14; o.connect(g); g.connect(A.destination); o.start(A.currentTime + i * 0.12); g.gain.exponentialRampToValueAtTime(0.0001, A.currentTime + i * 0.12 + 0.3); o.stop(A.currentTime + i * 0.12 + 0.3) }) } catch { /* ok */ }
      setTimeout(() => { ov.remove(); cb() }, 2600)
    }
    ;(window as any).__fabricaProxima = () => { if (mi < missoes.length - 1) { mi++; celebra(missoes[mi].local, () => montaMissao(mi)) } }
    ;(window as any).__fabricaMissao = () => mi   // QA lê
    montaMissao(0)
    ;(window as any).__fabricaRoteiro = roteiro   // QA lê a história gerada
    mostraBarraProf()
  }

  ;(window as any).__fabrica = { gerar: () => (document.getElementById('fgerar') as HTMLButtonElement).click(), set: (id: string, v: string) => { (document.getElementById(id) as HTMLInputElement).value = v } }

  // ---- BIBLIOTECA-LINK + PORTÃO DO PROFESSOR ----
  // A "receita" da atividade cabe na URL (?ativ=...): o link é PERMANENTE e remonta a
  // atividade na hora, em qualquer máquina. A barra só aparece no fluxo do FORMULÁRIO
  // (professor); pelo link direto a criança não vê nada disso.
  const q0 = new URLSearchParams(location.search)
  const bootDireto = q0.has('tabuada') || q0.has('ativ') || (window as any).__BOOT === 'tabuada'
  const enc = (o: unknown): string => btoa(unescape(encodeURIComponent(JSON.stringify(o))))
  const dec = (s: string): any => JSON.parse(decodeURIComponent(escape(atob(s))))
  function mostraBarraProf (): void {
    if (bootDireto || (navigator as any).webdriver) return
    document.getElementById('fbarra')?.remove()
    const receita = { ano: val('f_ano'), obj: val('f_obj'), disc: val('f_disc'), tema: val('f_tema'), dif: val('f_dif'), kit: val('f_kit') }
    const link = `${location.origin}${location.pathname}?ativ=${enc(receita)}`
    const bar = document.createElement('div')
    bar.id = 'fbarra'
    bar.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:9997;background:#16244acc;color:#eaf1ff;border-radius:12px;padding:8px 10px;font:13px system-ui;display:flex;gap:8px;align-items:center;backdrop-filter:blur(3px)'
    bar.innerHTML = `👨‍🏫 <b>Prévia do professor</b>
      <button id="fb_copiar" style="padding:6px 10px;border:0;border-radius:8px;background:#57e08a;color:#0b2350;font-weight:700;cursor:pointer">🔗 Copiar link da atividade</button>
      <button id="fb_x" aria-label="fechar" style="padding:6px 8px;border:0;border-radius:8px;background:#26355c;color:#cdd9f5;cursor:pointer">✕</button>`
    document.body.appendChild(bar)
    ;(bar.querySelector('#fb_copiar') as HTMLButtonElement).onclick = function () {
      void navigator.clipboard.writeText(link).then(() => { (this as HTMLButtonElement).textContent = '✅ Link copiado!' })
    }
    ;(bar.querySelector('#fb_x') as HTMLButtonElement).onclick = () => bar.remove()
  }

  // BOOTS DIRETOS: ?tabuada (atalho fixo) e ?ativ=<receita> (biblioteca-link)
  const boot = (window as any).__BOOT
  if (boot === 'tabuada' || q0.has('tabuada')) {
    host.style.display = 'none'
    ;(window as any).__fabrica.set('f_ano', '3º ano')
    ;(window as any).__fabrica.set('f_obj', 'Tabuada: multiplicar com grupos iguais')
    ;(window as any).__fabrica.set('f_dif', 'medio')
    btn.click()
  } else if (q0.has('ativ')) {
    host.style.display = 'none'
    try {
      const r = dec(q0.get('ativ')!)
      if (r.ano) (window as any).__fabrica.set('f_ano', r.ano)
      if (r.obj) (window as any).__fabrica.set('f_obj', r.obj)
      if (r.disc) (window as any).__fabrica.set('f_disc', r.disc)
      if (r.tema) (window as any).__fabrica.set('f_tema', r.tema)
      if (r.dif) (window as any).__fabrica.set('f_dif', r.dif)
      if (r.kit) (window as any).__fabrica.set('f_kit', r.kit)
      btn.click()
    } catch { host.style.display = ''; (document.getElementById('ferro')!).textContent = '⚠️ Link de atividade inválido — confira se copiou inteiro.' }
  }
}
