/* ============================================================================
 * DESAFIO ESPORTIVO — jogo 2D educativo (Estudio Profissional)
 * Diretrizes: Phaser CANVAS (poupa PC velho sem placa de video), Arcade Physics.
 * Mecanica: o aluno leva o jogador ate a bola e, pra FAZER O GOL, precisa
 * ACERTAR um desafio (matematica). Acertou = gol + torcida; errou = tenta de novo.
 *
 * ARTE: por ora shapes provisorios (marcados com ARTE-PROV). O atlas profissional
 * do Kenney (baixado pelo workflow) entra por cima depois, SEM mudar a logica.
 * ========================================================================== */
'use strict';

const CFG = {
  W: 900, H: 560,
  velocidade: 200,
  contaMax: 10,          // teto das parcelas do desafio (adaptavel ao ano/BNCC)
};

// ---------- som simples (Web Audio) ate os sons do Gemini entrarem ----------
let AC = null;
function initAudio() { if (AC) return; try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} }
function bip(freq, dur, vol, tipo) {
  if (!AC) return; const o = AC.createOscillator(), g = AC.createGain(), t = AC.currentTime;
  o.type = tipo || 'sine'; o.frequency.value = freq; g.gain.setValueAtTime(0.0001, t);
  g.gain.linearRampToValueAtTime(vol || 0.1, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0008, t + dur);
  o.connect(g); g.connect(AC.destination); o.start(t); o.stop(t + dur + 0.02);
}
function somApito() { bip(880, 0.18, 0.12, 'square'); }
function somGol() { [523, 659, 784, 1046].forEach((f, i) => setTimeout(() => bip(f, 0.22, 0.12, 'triangle'), i * 110)); }
function somErro() { bip(200, 0.25, 0.1, 'sawtooth'); }

class Campo extends Phaser.Scene {
  constructor() { super('Campo'); }

  create() {
    const cl = document.getElementById('carregando'); if (cl) cl.style.display = 'none';
    this.placar = 0; this.desafioAberto = false;

    // ---- campo (ARTE-PROV: desenhado; depois vira tile do Kenney) ----
    for (let i = 0; i < 8; i++) this.add.rectangle(CFG.W / 2, 35 + i * 70, CFG.W, 70, i % 2 ? 0x2f9e4f : 0x2b8f46);   // faixas do gramado
    this.add.rectangle(CFG.W / 2, CFG.H / 2, 4, CFG.H, 0xffffff, 0.5);       // meio de campo
    this.add.circle(CFG.W / 2, CFG.H / 2, 60, 0xffffff, 0).setStrokeStyle(3, 0xffffff, 0.5);

    // ---- GOL (ARTE-PROV) ----
    this.golX = CFG.W - 70;
    this.add.rectangle(this.golX, CFG.H / 2, 20, 200, 0xffffff, 0.9).setStrokeStyle(4, 0xdddddd);
    this.add.text(this.golX, CFG.H / 2 - 120, 'GOL', { fontFamily: 'system-ui', fontSize: '18px', color: '#fff' }).setOrigin(0.5);

    // ---- JOGADOR com FISICA NATIVA (Arcade). ARTE-PROV = circulo; depois sprite Kenney ----
    this.jogador = this.add.container(140, CFG.H / 2);
    const corpo = this.add.circle(0, 0, 22, 0x2478c8).setStrokeStyle(3, 0x184e86);
    const cabeca = this.add.circle(0, -22, 13, 0xffd9a8);
    this.jogadorPerna = this.add.rectangle(0, 20, 10, 16, 0x184e86);   // "perna" p/ animar o chute
    this.jogador.add([this.jogadorPerna, corpo, cabeca]);
    this.physics.add.existing(this.jogador);
    this.jogador.body.setSize(50, 50).setOffset(-25, -25).setCollideWorldBounds(true);

    // ---- BOLA (Arcade) ----
    this.bola = this.add.circle(0, 0, 14, 0xffffff).setStrokeStyle(2, 0x222222);
    this.physics.add.existing(this.bola);
    this.bola.body.setCircle(14).setCollideWorldBounds(true).setBounce(0.4);
    this.novaBola();

    // FSM simples de animacao (idle/correr/chutar) — por ora via "perna"/bob
    this.estado = 'idle'; this.tempoAnim = 0;

    // ---- HUD ----
    this.hud = this.add.text(16, 12, 'Gols: 0', { fontFamily: 'system-ui', fontSize: '24px', color: '#fff', backgroundColor: '#0008', padding: { x: 10, y: 6 } });
    this.dica = this.add.text(CFG.W / 2, CFG.H - 24, 'Leve o jogador ate a bola e chute pra abrir o desafio!', { fontFamily: 'system-ui', fontSize: '15px', color: '#eaffea' }).setOrigin(0.5);

    // ---- input ----
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    this.input.keyboard.on('keydown', () => initAudio());
    this.input.on('pointerdown', () => initAudio());

    // grupo do overlay do desafio (fica escondido)
    this.overlay = this.add.container(0, 0).setDepth(50).setVisible(false);

    // ---- ganchos de QA (Auditor) ----
    window.__abrir = () => this.abrirDesafio();
    window.__certo = () => this.responder(true, { setFillStyle() {} });
    window.__placar = () => this.placar;
    window.__ready = true;
  }

  novaBola() {
    const x = Phaser.Math.Between(240, 520), y = Phaser.Math.Between(120, CFG.H - 120);
    this.bola.body.reset(x, y); this.bola.body.setVelocity(0, 0);
    this.bolaAtiva = true;
  }

  // ------------ DESAFIO PEDAGOGICO (gate pra fazer o gol) ------------
  abrirDesafio() {
    if (this.desafioAberto) return; this.desafioAberto = true; somApito();
    const a = Phaser.Math.Between(1, CFG.contaMax), b = Phaser.Math.Between(1, CFG.contaMax);
    const certo = a + b;
    const opcoes = Phaser.Utils.Array.Shuffle([certo, certo + 1, Math.max(0, certo - 2)]);

    this.overlay.removeAll(true);
    this.overlay.add(this.add.rectangle(CFG.W / 2, CFG.H / 2, CFG.W, CFG.H, 0x001018, 0.66));
    this.overlay.add(this.add.rectangle(CFG.W / 2, 210, 520, 130, 0xffffff).setStrokeStyle(5, 0xffd25a));
    this.overlay.add(this.add.text(CFG.W / 2, 175, 'Para fazer o GOL, resolva:', { fontFamily: 'system-ui', fontSize: '20px', color: '#123a5a' }).setOrigin(0.5));
    this.overlay.add(this.add.text(CFG.W / 2, 220, a + ' + ' + b + ' = ?', { fontFamily: 'system-ui', fontSize: '40px', color: '#0e3d22', fontStyle: 'bold' }).setOrigin(0.5));

    opcoes.forEach((n, i) => {
      const bx = CFG.W / 2 - 170 + i * 170, by = 340;
      const bt = this.add.rectangle(bx, by, 130, 80, 0x2478c8).setStrokeStyle(3, 0x123a5a).setInteractive({ useHandCursor: true });
      const tx = this.add.text(bx, by, String(n), { fontFamily: 'system-ui', fontSize: '34px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
      bt.on('pointerover', () => bt.setFillStyle(0x3a90e0));
      bt.on('pointerout', () => bt.setFillStyle(0x2478c8));
      bt.on('pointerdown', () => this.responder(n === certo, bt));
      this.overlay.add([bt, tx]);
    });
    this.overlay.setVisible(true);
  }

  responder(acertou, bt) {
    if (acertou) {
      bt.setFillStyle(0x2ecc71);
      this.time.delayedCall(220, () => { this.overlay.setVisible(false); this.desafioAberto = false; this.fazerGol(); });
    } else {
      bt.setFillStyle(0xe74c3c); somErro();
      this.cameras.main.shake(200, 0.006);
      this.time.delayedCall(500, () => { this.overlay.setVisible(false); this.desafioAberto = false; this.dica.setText('Quase! A bola voltou — tente de novo.'); });
    }
  }

  fazerGol() {
    // a bola voa pro gol (tween) + placar + torcida
    this.bolaAtiva = false; this.estado = 'chutar';
    this.tweens.add({
      targets: this.bola, x: this.golX, y: CFG.H / 2, duration: 420, ease: 'Cubic.easeIn',
      onComplete: () => {
        somGol(); this.placar++; this.hud.setText('Gols: ' + this.placar);
        // confete
        for (let i = 0; i < 20; i++) {
          const c = this.add.circle(this.golX, CFG.H / 2, 5, Phaser.Utils.Array.GetRandom([0xffd24a, 0xe74c3c, 0x2ecc71, 0x3498db]));
          const a = Math.random() * 6.28, s = 100 + Math.random() * 160;
          this.tweens.add({ targets: c, x: c.x + Math.cos(a) * s, y: c.y + Math.sin(a) * s - 60, alpha: 0, duration: 800, onComplete: () => c.destroy() });
        }
        const g = this.add.text(CFG.W / 2, 120, 'GOOOL! ⚽', { fontFamily: 'system-ui', fontSize: '48px', color: '#fff', fontStyle: 'bold', stroke: '#0e3d22', strokeThickness: 6 }).setOrigin(0.5).setDepth(40);
        this.tweens.add({ targets: g, scale: { from: 0.5, to: 1.2 }, alpha: { from: 1, to: 0 }, duration: 1100, onComplete: () => g.destroy() });
        this.time.delayedCall(700, () => { this.novaBola(); this.dica.setText('Boa! Vai pra proxima bola!'); });
      }
    });
  }

  update(_t, dt) {
    if (this.desafioAberto) { this.jogador.body.setVelocity(0, 0); return; }
    let vx = 0, vy = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown) vx = -1;
    if (this.cursors.right.isDown || this.wasd.D.isDown) vx = 1;
    if (this.cursors.up.isDown || this.wasd.W.isDown) vy = -1;
    if (this.cursors.down.isDown || this.wasd.S.isDown) vy = 1;
    const v = new Phaser.Math.Vector2(vx, vy); if (v.length() > 0) v.normalize();
    this.jogador.body.setVelocity(v.x * CFG.velocidade, v.y * CFG.velocidade);

    // FSM idle/correr (ARTE-PROV: bob; depois anima o atlas Kenney)
    const correndo = v.length() > 0;
    this.tempoAnim += dt / 1000;
    this.jogador.y += 0; // container ja se move pela fisica
    this.jogadorPerna.angle = correndo ? Math.sin(this.tempoAnim * 14) * 30 : 0;

    // perto da bola? mostra que pode chutar; chuta ao encostar (ou espaco)
    if (this.bolaAtiva) {
      const d = Phaser.Math.Distance.Between(this.jogador.x, this.jogador.y, this.bola.x, this.bola.y);
      if (d < 46) this.abrirDesafio();
    }
  }
}

new Phaser.Game({
  type: Phaser.CANVAS,                       // FORCA CANVAS — poupa PC velho sem GPU
  parent: 'jogo',
  width: CFG.W, height: CFG.H,
  backgroundColor: '#2f9e4f',
  physics: { default: 'arcade', arcade: { debug: false } },
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  scene: Campo
});
