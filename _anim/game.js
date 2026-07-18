'use strict';
// ============================================================================
// DEMO "AMBIENTE VIVO" com o kit LPC animado (Phaser CANVAS, leve p/ PC antigo).
// Prova pro Marcos: este motor faz TUDO que os nossos 2D faziam ->
//   SOL (luz quente + raios) · SOMBRA que segue o personagem ·
//   VENTO (grama + arvores balancando) · FOLHAS caindo · NUVENS passando ·
//   SONS (vento suave + passarinho + passos) — tudo por CODIGO (sem asset pesado).
// ============================================================================
const F = 64, SC = 1.6, W = 640, H = 480;
const IDLE = { up: 104, left: 117, down: 130, right: 143 };

// ---------- SOM (Web Audio proprio, comeca no 1o toque/tecla) --------------
let AC = null, MASTER = null, _windGain = null, _somOn = false;
function initSom() {
  if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)();
    MASTER = AC.createGain(); MASTER.gain.value = 0.6; MASTER.connect(AC.destination);
    // vento: ruido -> passa-baixa -> ganho (com rajadas via LFO)
    const buf = AC.createBuffer(1, AC.sampleRate * 2, AC.sampleRate);
    const d = buf.getChannelData(0); let last = 0;
    for (let i = 0; i < d.length; i++) { const wn = Math.random() * 2 - 1; last = (last + 0.02 * wn) / 1.02; d[i] = last * 3.2; }
    const src = AC.createBufferSource(); src.buffer = buf; src.loop = true;
    const lp = AC.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 520;
    _windGain = AC.createGain(); _windGain.gain.value = 0.05;
    src.connect(lp); lp.connect(_windGain); _windGain.connect(MASTER); src.start();
    _somOn = true;
  } catch (e) { /* sem audio, tudo bem */ }
}
function rajadaSom() { // sobe o vento na rajada e volta
  if (!_windGain || !AC) return;
  const t = AC.currentTime;
  _windGain.gain.cancelScheduledValues(t);
  _windGain.gain.setValueAtTime(_windGain.gain.value, t);
  _windGain.gain.linearRampToValueAtTime(0.12, t + 0.8);
  _windGain.gain.linearRampToValueAtTime(0.05, t + 2.6);
}
function passarinho() { // 2-3 pios com glissando
  if (!AC || !_somOn) return;
  const t0 = AC.currentTime, n = 2 + (Math.random() < 0.5 ? 1 : 0);
  for (let k = 0; k < n; k++) {
    const t = t0 + k * 0.16, o = AC.createOscillator(), g = AC.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(2100 + Math.random() * 400, t);
    o.frequency.exponentialRampToValueAtTime(3000 + Math.random() * 500, t + 0.09);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(0.09, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.13);
    o.connect(g); g.connect(MASTER); o.start(t); o.stop(t + 0.14);
  }
}
function passo() { // "tuf" curto e grave a cada passada
  if (!AC || !_somOn) return;
  const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain();
  o.type = 'triangle'; o.frequency.setValueAtTime(150, t);
  o.frequency.exponentialRampToValueAtTime(70, t + 0.08);
  g.gain.setValueAtTime(0.06, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
  o.connect(g); g.connect(MASTER); o.start(t); o.stop(t + 0.13);
}

class Mundo extends Phaser.Scene {
  constructor() { super('Mundo'); }
  preload() { this.load.spritesheet('hero', 'assets/hero.png', { frameWidth: F, frameHeight: F }); }

  create() {
    // ---- CHAO: gramado texturizado ----
    const g = this.add.graphics();
    for (let y = 0; y < H; y += 16) for (let x = 0; x < W; x += 16) {
      const c = Phaser.Display.Color.GetColor(72 + Phaser.Math.Between(-6, 8), 134 + Phaser.Math.Between(-8, 10), 58 + Phaser.Math.Between(-6, 8));
      g.fillStyle(c, 1); g.fillRect(x, y, 16, 16);
    }
    g.setDepth(0);

    // ---- SOL: luz quente no canto + raios suaves + brilho ----
    const sol = this.add.graphics().setDepth(1);
    sol.fillStyle(0xfff6c8, 0.30); sol.fillCircle(560, 70, 120);
    sol.fillStyle(0xfff0a8, 0.55); sol.fillCircle(560, 70, 46);
    sol.fillStyle(0xffffff, 0.9); sol.fillCircle(560, 70, 26);
    for (let i = 0; i < 7; i++) { // raios que pulsam
      const a = (i / 7) * Math.PI * 2;
      sol.fillStyle(0xfff2b0, 0.10);
      sol.fillTriangle(560, 70, 560 + Math.cos(a) * 260, 70 + Math.sin(a) * 260, 560 + Math.cos(a + 0.12) * 260, 70 + Math.sin(a + 0.12) * 260);
    }
    this.tweens.add({ targets: sol, alpha: { from: 0.85, to: 1 }, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    // luz quente geral por cima (sensacao de sol)
    const luz = this.add.rectangle(W / 2, H / 2, W, H, 0xfff1c0, 0.08).setDepth(2).setBlendMode(Phaser.BlendModes.ADD);
    this.tweens.add({ targets: luz, alpha: { from: 0.05, to: 0.12 }, duration: 4000, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    // ---- NUVENS: sombra passando no chao + nuvem clara no ceu ----
    for (let i = 0; i < 3; i++) {
      const y = 60 + i * 130, sombra = this.add.ellipse(-120, y, 160, 60, 0x2a4a24, 0.16).setDepth(3);
      this.tweens.add({ targets: sombra, x: W + 160, duration: 22000 + i * 6000, repeat: -1, delay: i * 5000, ease: 'Linear' });
      const nuvem = this.add.ellipse(-100, 40 + i * 40, 130, 44, 0xffffff, 0.5).setDepth(6);
      this.tweens.add({ targets: nuvem, x: W + 140, duration: 26000 + i * 6000, repeat: -1, delay: i * 4000, ease: 'Linear' });
    }

    // ---- TEXTURA de arvore (tronco + copa) desenhada por codigo ----
    const tg = this.add.graphics();
    tg.fillStyle(0x6b4a2a, 1); tg.fillRect(30, 78, 16, 34);           // tronco
    tg.fillStyle(0x2f6b2f, 1); tg.fillCircle(38, 46, 34);            // copa (3 circulos)
    tg.fillStyle(0x3a7d38, 1); tg.fillCircle(20, 56, 26); tg.fillCircle(56, 56, 26);
    tg.fillStyle(0x4b9146, 1); tg.fillCircle(38, 40, 20);
    tg.generateTexture('arvore', 76, 112); tg.destroy();

    // ---- TEXTURA de folha (para cair no vento) ----
    const lf = this.add.graphics();
    lf.fillStyle(0x4b8f3e, 1); lf.fillEllipse(5, 4, 9, 6);
    lf.fillStyle(0xcaa23a, 1); lf.fillEllipse(4, 3, 4, 3);
    lf.generateTexture('folha', 11, 8); lf.destroy();

    // ---- TUFOS de grama que balancam no vento ----
    const gt = this.add.graphics();
    gt.fillStyle(0x3f7a34, 1); gt.fillTriangle(0, 10, 2, 0, 4, 10); gt.fillTriangle(4, 10, 7, 1, 9, 10); gt.fillTriangle(8, 10, 11, 0, 13, 10);
    gt.generateTexture('tufo', 13, 11); gt.destroy();
    this.tufos = [];
    for (let i = 0; i < 40; i++) {
      const x = Phaser.Math.Between(10, W - 10), y = Phaser.Math.Between(30, H - 20);
      const t = this.add.image(x, y, 'tufo').setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: t, angle: { from: -7, to: 7 }, duration: Phaser.Math.Between(1400, 2200), yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: Phaser.Math.Between(0, 800) });
      this.tufos.push(t);
    }

    // ---- ARVORES (balancam a copa no vento; y-sort com o heroi) ----
    this.arvores = [];
    [[110, 150], [520, 210], [90, 360], [470, 400], [300, 120]].forEach(([x, y], i) => {
      const a = this.add.image(x, y, 'arvore').setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: a, angle: { from: -2.2, to: 2.2 }, duration: 2000 + i * 250, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: i * 300 });
      this.arvores.push(a);
    });

    // ---- FOLHAS caindo (recicla): saem das copas e planam ----
    this.folhas = [];
    for (let i = 0; i < 10; i++) this.novaFolha(true);

    // ---- ANIMACOES de andar (LPC: 8 quadros por direcao) ----
    this.anims.create({ key: 'up', frames: this.anims.generateFrameNumbers('hero', { start: 105, end: 112 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'left', frames: this.anims.generateFrameNumbers('hero', { start: 118, end: 125 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'down', frames: this.anims.generateFrameNumbers('hero', { start: 131, end: 138 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'right', frames: this.anims.generateFrameNumbers('hero', { start: 144, end: 151 }), frameRate: 9, repeat: -1 });

    // ---- SOMBRA do heroi (elipse escura que segue e amassa no passo) ----
    this.sombra = this.add.ellipse(W / 2, H / 2, 44, 16, 0x000000, 0.28);

    // ---- HEROI ----
    this.hero = this.physics.add.sprite(W / 2, H / 2, 'hero', IDLE.down).setScale(SC);
    this.hero.setCollideWorldBounds(true);
    this.dir = 'down'; this._passoT = 0;
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');

    // ---- rajadas de vento (som) e passarinho, de tempos em tempos ----
    this.time.addEvent({ delay: 5000, loop: true, callback: rajadaSom });
    this.time.addEvent({ delay: 4200, loop: true, callback: () => { if (Math.random() < 0.7) passarinho(); } });

    // ---- liga o som no 1o gesto ----
    const liga = () => { initSom(); const dica = document.getElementById('somdica'); if (dica) dica.style.display = 'none'; };
    this.input.on('pointerdown', liga);
    this.input.keyboard.on('keydown', liga);

    window.__ready = true;
    window.__mover = (dir) => { this._forc = dir; };
  }

  novaFolha(inicial) {
    const ar = this.arvores && this.arvores.length ? Phaser.Utils.Array.GetRandom(this.arvores) : { x: Phaser.Math.Between(0, W), y: 60 };
    const x = (ar.x || Phaser.Math.Between(0, W)) + Phaser.Math.Between(-20, 20);
    const y = inicial ? Phaser.Math.Between(0, H) : (ar.y ? ar.y - 90 : 20) + Phaser.Math.Between(-10, 10);
    const f = (this._folhaPool && this._folhaPool.length) ? this._folhaPool.pop().setPosition(x, y).setVisible(true).setActive(true)
      : this.add.image(x, y, 'folha');
    f.setDepth(9000);
    const dur = Phaser.Math.Between(5000, 9000);
    this.tweens.add({ targets: f, y: y + Phaser.Math.Between(160, 300), x: x + Phaser.Math.Between(-90, 90), angle: Phaser.Math.Between(180, 540), duration: dur, ease: 'Sine.inOut', onComplete: () => {
      f.setVisible(false).setActive(false); (this._folhaPool || (this._folhaPool = [])).push(f); this.novaFolha(false);
    } });
  }

  update(time) {
    let vx = 0, vy = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') vx = -1;
    else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') vx = 1;
    else if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') vy = -1;
    else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') vy = 1;

    this.hero.body.setVelocity(vx * 130, vy * 130);
    const andando = vx !== 0 || vy !== 0;
    if (vx < 0) { this.hero.anims.play('left', true); this.dir = 'left'; }
    else if (vx > 0) { this.hero.anims.play('right', true); this.dir = 'right'; }
    else if (vy < 0) { this.hero.anims.play('up', true); this.dir = 'up'; }
    else if (vy > 0) { this.hero.anims.play('down', true); this.dir = 'down'; }
    else { this.hero.anims.stop(); this.hero.setFrame(IDLE[this.dir]); }

    // y-sort: o heroi passa por TRAS/FRENTE de arvores e tufos conforme o y
    this.hero.setDepth(this.hero.y);

    // SOMBRA acompanha os pes e amassa levemente no passo
    const py = this.hero.y + this.hero.displayHeight * 0.42;
    this.sombra.setPosition(this.hero.x, py).setDepth(this.hero.y - 1);
    const amassa = andando ? 1 + Math.sin(time / 90) * 0.08 : 1;
    this.sombra.scaleX = amassa; this.sombra.scaleY = andando ? 0.94 : 1;

    // som de passo no ritmo da caminhada
    if (andando && time - this._passoT > 300) { passo(); this._passoT = time; }
  }
}

new Phaser.Game({
  type: Phaser.CANVAS, parent: 'jogo', width: W, height: H, pixelArt: true,
  backgroundColor: '#4a7a3a', physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }, scene: Mundo
});
