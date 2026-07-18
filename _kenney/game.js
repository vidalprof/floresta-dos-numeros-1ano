'use strict';
// ============================================================================
// DEMO KENNEY + MOTOR DE VIDA — personagem de UMA imagem só (Kenney roguelike,
// CC0, SEM emoji) ganha VIDA por CÓDIGO: respira parado, PULA + squash/stretch
// ao andar, sombra no chão, vira pro lado. Prova: dá pra ficar VIVO sem cartela.
// Corpo FÍSICO (invisível) move/colide; o VISUAL segue o corpo + o pulo.
// Toque pra andar (celular/PC). Phaser CANVAS.
// ============================================================================
const WW = 1000, WH = 760, ZOOM = 2.2, S = 4;

class Demo extends Phaser.Scene {
  constructor() { super('Demo'); }
  preload() {
    this.load.image('grass', 'assets/grass.png');
    this.load.image('char', 'assets/char.png');
    this.load.image('tree', 'assets/tree.png');
    this.load.image('pine', 'assets/pine.png');
  }
  create() {
    this.add.tileSprite(0, 0, WW, WH, 'grass').setOrigin(0).setDepth(-100);

    const arv = [['tree', 160, 200], ['pine', 420, 150], ['tree', 760, 230], ['pine', 880, 460], ['tree', 120, 520], ['tree', 620, 560], ['pine', 300, 650], ['tree', 850, 690]];
    arv.forEach(([t, x, y]) => {
      this.add.ellipse(x, y, 30, 10, 0x000000, 0.2).setDepth(y - 1);
      this.add.image(x, y, t).setOrigin(0.5, 1).setScale(S).setDepth(y);
    });

    // CORPO fisico (invisivel) — move e colide
    this.corpo = this.physics.add.image(WW / 2, WH / 2, 'char').setVisible(false);
    this.corpo.body.setSize(12, 6); this.corpo.setCollideWorldBounds(true);
    // SOMBRA + VISUAL (a imagem que ganha vida)
    this.sombra = this.add.ellipse(WW / 2, WH / 2, 34, 12, 0x000000, 0.25);
    this.vis = this.add.image(WW / 2, WH / 2, 'char').setOrigin(0.5, 1);
    this.face = 1; this.destino = null;

    this.physics.world.setBounds(0, 0, WW, WH);
    this.cameras.main.setBounds(0, 0, WW, WH).setZoom(ZOOM).startFollow(this.corpo, true, 0.12, 0.12);
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    this.input.keyboard.clearCaptures(); this.input.keyboard.disableGlobalCapture();
    this.input.on('pointerdown', (p) => { const wp = this.cameras.main.getWorldPoint(p.x, p.y); this.destino = { x: Phaser.Math.Clamp(wp.x, 8, WW - 8), y: Phaser.Math.Clamp(wp.y, 8, WH - 8) }; this._dt = this.time.now; });

    window.__ready = true; window.__scene = this;
    window.__fs = () => { if (this.scale.isFullscreen) this.scale.stopFullscreen(); else this.scale.startFullscreen(); };
    window.__mover = (d) => { this._forc = d; };
    window.__parar = () => { this._forc = null; };
  }
  update(time) {
    let vx = 0, vy = 0, kx = 0, ky = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') kx = -1;
    else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') kx = 1;
    if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') ky = -1;
    else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') ky = 1;
    if (kx || ky) { this.destino = null; vx = kx; vy = ky; }
    else if (this.destino) {
      const dx = this.destino.x - this.corpo.x, dy = this.destino.y - this.corpo.y, d = Math.hypot(dx, dy);
      if (d < 8 || time - this._dt > 4000) this.destino = null; else { vx = dx / d; vy = dy / d; }
    }
    this.corpo.body.setVelocity(vx * 150, vy * 150);
    const andando = vx !== 0 || vy !== 0;
    if (vx < 0) this.face = -1; else if (vx > 0) this.face = 1;

    // ---- MOTOR DE VIDA (aplica no VISUAL, o corpo fica no chão) ----
    const bx = this.corpo.x, by = this.corpo.y + 8;   // pés no chão
    let sx, sy, yb;
    if (andando) {
      const p = time * 0.016;
      yb = -Math.abs(Math.sin(p)) * 7;                 // pulinho
      const sq = Math.abs(Math.cos(p));                 // squash ao aterrar
      sy = S * (1 - sq * 0.12); sx = S * (1 + sq * 0.10);
    } else {
      const b = Math.sin(time * 0.004) * 0.03;          // respiração
      sy = S * (1 + b); sx = S * (1 - b * 0.6); yb = 0;
    }
    this.vis.setPosition(bx, by + yb).setScale(sx * this.face, sy).setDepth(by);
    this.sombra.setPosition(bx, by + 1).setDepth(by - 1).setScale(andando ? 0.9 : 1, 1);
  }
}

new Phaser.Game({
  type: Phaser.CANVAS, pixelArt: true, roundPixels: true, backgroundColor: '#4a7a3a',
  physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.RESIZE, parent: 'jogo', width: '100%', height: '100%' },
  scene: Demo
});
