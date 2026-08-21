// ============================================================================
// MECÂNICA "contar" — a criança CONTA quantos itens há e escolhe o número.
// Reutilizável p/ qualquer tema (galinhas, frutas, estrelas...). Ensina
// contagem/quantidade (números até 30) SEM parecer prova: é um problema do
// mundo ("quantos ovos o Byte precisa juntar?"), o Byte pergunta, e errar só
// pede pra CONTAR DE NOVO (os itens pulam um a um) — nunca "resposta errada".
//
// params (dos DADOS da parada):
//   quantidade   number  (obrigatório) — quantos itens mostrar/contar
//   item?        string  — asset do kit p/ cada item (senão usa fichas)
//   max?         number  — teto do intervalo dos botões (default 30)
//   pergunta_fala? string— id de fala do Byte ao abrir (o problema)
//   elogio_fala?  string — id de fala do Byte ao acertar
// ============================================================================
import Phaser from 'phaser'
import type { Mecanica, CtxMecanica } from './tipos'

const VW = 1024, VH = 768

export const Contar: Mecanica = {
  id: 'contar',
  montar (ctx: CtxMecanica) {
    const s = ctx.scene
    const p = ctx.params || {}
    const alvo = Math.max(1, Math.round(Number(p.quantidade) || 1))
    const teto = Math.max(alvo + 2, Math.round(Number(p.max) || 30))
    const item: string | undefined = p.item && s.textures.exists(p.item) ? p.item : undefined

    // camada fixa na tela (não rola com o mundo), acima de tudo
    const lay = s.add.layer().setDepth(99000)
    const scroll0 = (o: Phaser.GameObjects.GameObject & { setScrollFactor?: any }) => { o.setScrollFactor && o.setScrollFactor(0); return o }

    // véu escuro
    const veu = s.add.rectangle(VW / 2, VH / 2, VW, VH, 0x0b1020, 0.62); scroll0(veu); lay.add(veu)
    // painel
    const pw = 720, ph = 470, px = VW / 2, py = VH / 2
    const corHex = Phaser.Display.Color.HexStringToColor(ctx.cor || '#ffd25a').color
    const painel = s.add.graphics(); scroll0(painel)
    painel.fillStyle(0xf7f9ff, 1); painel.fillRoundedRect(px - pw / 2, py - ph / 2, pw, ph, 22)
    painel.lineStyle(6, corHex, 1); painel.strokeRoundedRect(px - pw / 2, py - ph / 2, pw, ph, 22)
    lay.add(painel)

    // sem setResolution em texto centralizado (desloca o origin no Phaser); o
    // FIT já mantém nítido nesse tamanho de fonte.
    const titulo = s.add.text(px, py - ph / 2 + 34, 'Conte com o Byte', { fontFamily: 'Arial Black, Arial', fontSize: '28px', color: '#22314f' }).setOrigin(0.5); scroll0(titulo); lay.add(titulo)
    const dica = s.add.text(px, py - ph / 2 + 76, 'Quantos há? Toque no número certo.', { fontFamily: 'Arial', fontSize: '18px', color: '#5a6684' }).setOrigin(0.5); scroll0(dica); lay.add(dica)

    // ---- bandeja de itens (a criança conta) ----
    const bandY = py - 40, cols = Math.min(10, alvo), gapx = 56, gapy = 58
    const linhas = Math.ceil(alvo / cols)
    const fichas: Phaser.GameObjects.GameObject[] = []
    for (let i = 0; i < alvo; i++) {
      const c = i % cols, l = Math.floor(i / cols)
      const fx = px - ((Math.min(cols, alvo) - 1) * gapx) / 2 + c * gapx
      const fy = bandY - ((linhas - 1) * gapy) / 2 + l * gapy
      let g: Phaser.GameObjects.GameObject
      if (item) {
        const im = s.add.image(fx, fy, item); im.setScale(46 / im.height); g = im
      } else {
        g = s.add.circle(fx, fy, 20, corHex, 1)
        ;(g as Phaser.GameObjects.Arc).setStrokeStyle(3, 0x22314f, 1)
      }
      scroll0(g as any); lay.add(g); fichas.push(g)
    }

    // conta-de-novo: pisca os itens um a um (consequência do erro, sem "errou")
    const contarDeNovo = () => {
      fichas.forEach((g, i) => {
        s.tweens.add({ targets: g, scale: { from: (g as any).scale ?? 1, to: ((g as any).scale ?? 1) * 1.35 }, yoyo: true, duration: 180, delay: 160 * i, ease: 'Sine.easeInOut' })
      })
    }

    // ---- botões de número (opções) ----
    const opcoes = gerarOpcoes(alvo, teto, 4)
    const bw = 108, bh = 70, gx = 20
    const totalW = opcoes.length * bw + (opcoes.length - 1) * gx
    const by = py + ph / 2 - 70
    let travado = false
    opcoes.forEach((n, i) => {
      const bx = px - totalW / 2 + bw / 2 + i * (bw + gx)
      const bg = s.add.graphics(); scroll0(bg)
      const desenha = (fill: number) => { bg.clear(); bg.fillStyle(fill, 1); bg.fillRoundedRect(bx - bw / 2, by - bh / 2, bw, bh, 14); bg.lineStyle(3, 0x22314f, 1); bg.strokeRoundedRect(bx - bw / 2, by - bh / 2, bw, bh, 14) }
      desenha(0xffffff)
      const tx = s.add.text(bx, by, String(n), { fontFamily: 'Arial Black, Arial', fontSize: '32px', color: '#22314f' }).setOrigin(0.5); scroll0(tx); tx.setResolution(2)
      lay.add(bg); lay.add(tx)
      const zona = s.add.zone(bx, by, bw, bh).setInteractive({ useHandCursor: true }); scroll0(zona as any); lay.add(zona)
      zona.on('pointerover', () => { if (!travado) desenha(0xfff2c6) })
      zona.on('pointerout', () => { if (!travado) desenha(0xffffff) })
      zona.on('pointerdown', () => {
        if (travado) return
        if (n === alvo) {
          travado = true
          desenha(0xbdf0c8)
          const fim = () => { s.tweens.add({ targets: lay.getChildren(), alpha: 0, duration: 320, onComplete: () => { lay.destroy(true) } }); ctx.aoConcluir(true) }
          if (p.elogio_fala && ctx.temAudio(p.elogio_fala)) ctx.falar(p.elogio_fala, fim)
          else { dica.setText('Isso! São ' + alvo + '.'); s.time.delayedCall(1100, fim) }
        } else {
          desenha(0xffd6d6)
          dica.setText('Quase! Vamos contar de novo, um por um…')
          contarDeNovo()
          s.time.delayedCall(400, () => desenha(0xffffff))
        }
      })
    })

    // o Byte apresenta o PROBLEMA (fala), depois conta-de-novo destaca os itens
    if (p.pergunta_fala && ctx.temAudio(p.pergunta_fala)) ctx.falar(p.pergunta_fala)
    s.time.delayedCall(500, contarDeNovo)
  }
}

// opções: inclui o alvo + vizinhos plausíveis, únicos, dentro de [1, teto]
function gerarOpcoes (alvo: number, teto: number, n: number): number[] {
  const set = new Set<number>([alvo])
  let raio = 1
  while (set.size < n && raio < teto) {
    for (const d of [raio, -raio]) { const v = alvo + d; if (v >= 1 && v <= teto) set.add(v); if (set.size >= n) break }
    raio++
  }
  const arr = Array.from(set)
  // embaralha (runtime; Math.random liberado no app)
  for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1));[arr[i], arr[j]] = [arr[j], arr[i]] }
  return arr
}
