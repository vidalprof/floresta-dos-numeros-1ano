'use strict';
// Demo: personagem LPC animado andando nas 4 DIREÇÕES (mexe as pernas de verdade).
// Layout LPC universal (13 colunas): linhas de ANDAR = 8(cima) 9(esq) 10(baixo) 11(dir),
// cada uma com 9 quadros (o 1º = parado). Frame = linha*13 + coluna.
const F = 64, SC = 1.5, W = 640, H = 480;
const IDLE = { up: 104, left: 117, down: 130, right: 143 };

class Demo extends Phaser.Scene {
  constructor() { super('Demo'); }
  preload() { this.load.spritesheet('hero', 'assets/hero.png', { frameWidth: F, frameHeight: F }); }
  create() {
    // gramado (textura simples)
    const g = this.add.graphics();
    for (let y = 0; y < H; y += 16) for (let x = 0; x < W; x += 16) {
      const c = Phaser.Display.Color.GetColor(70 + Phaser.Math.Between(-6, 8), 132 + Phaser.Math.Between(-8, 10), 56 + Phaser.Math.Between(-6, 8));
      g.fillStyle(c, 1); g.fillRect(x, y, 16, 16);
    }
    for (let i = 0; i < 120; i++) { g.fillStyle(0x3f6a34, 1); const x = Phaser.Math.Between(0, W), y = Phaser.Math.Between(0, H); g.fillRect(x, y, 2, 4); g.fillRect(x + 3, y + 1, 2, 3); }

    this.anims.create({ key: 'up', frames: this.anims.generateFrameNumbers('hero', { start: 105, end: 112 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'left', frames: this.anims.generateFrameNumbers('hero', { start: 118, end: 125 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'down', frames: this.anims.generateFrameNumbers('hero', { start: 131, end: 138 }), frameRate: 9, repeat: -1 });
    this.anims.create({ key: 'right', frames: this.anims.generateFrameNumbers('hero', { start: 144, end: 151 }), frameRate: 9, repeat: -1 });

    this.hero = this.physics.add.sprite(W / 2, H / 2, 'hero', IDLE.down).setScale(SC);
    this.hero.setCollideWorldBounds(true);
    this.dir = 'down';
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    window.__ready = true;
    window.__mover = (dir) => { this._forc = dir; };
  }
  update() {
    let vx = 0, vy = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') vx = -1;
    else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') vx = 1;
    else if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') vy = -1;
    else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') vy = 1;
    this.hero.body.setVelocity(vx * 130, vy * 130);
    if (vx < 0) { this.hero.anims.play('left', true); this.dir = 'left'; }
    else if (vx > 0) { this.hero.anims.play('right', true); this.dir = 'right'; }
    else if (vy < 0) { this.hero.anims.play('up', true); this.dir = 'up'; }
    else if (vy > 0) { this.hero.anims.play('down', true); this.dir = 'down'; }
    else { this.hero.anims.stop(); this.hero.setFrame(IDLE[this.dir]); }
  }
}
new Phaser.Game({
  type: Phaser.CANVAS, parent: 'jogo', width: W, height: H, pixelArt: true,
  backgroundColor: '#4a7a3a', physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH }, scene: Demo
});
