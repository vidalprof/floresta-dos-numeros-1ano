/* ============================================================================
 * FAZENDA DO SABER — RPG 2D top-down (Stardew-like), educativo.
 * Diretrizes: Phaser CANVAS (leve p/ PC velho), Arcade Physics, movimento 4-dir,
 * PROFUNDIDADE Z (herói passa atras das arvores), colisao, arte PIXEL consistente
 * do Kenney Tiny Town (sem bug de coerencia). Trava pedagogica: PLANTAR exige acertar
 * uma conta. Cresce com o tempo -> colher. Arte do heroi = tile do kit (por ora).
 * ========================================================================== */
'use strict';

const TS = 16, SCALE = 3, TILE = TS * SCALE;         // tile 16px -> 48px na tela
const COLS = 20, ROWS = 14, WW = COLS * TILE, WH = ROWS * TILE;

// indices de tile no Tiny Town (packed 12x11)
const T = { GRASS: 0, GRASS_B: 1, GRASS_FLOR: 2, DIRT: 25, TREES: [5], FENCE: 46, CROP: 93, HERO: 104, SPROUT: 17 };

let AC = null;
function initA() { if (AC) return; try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} }
function bip(f, d, v, t) { if (!AC) return; const o = AC.createOscillator(), g = AC.createGain(), n = AC.currentTime; o.type = t || 'sine'; o.frequency.value = f; g.gain.setValueAtTime(0.0001, n); g.gain.linearRampToValueAtTime(v || 0.1, n + 0.01); g.gain.exponentialRampToValueAtTime(0.0008, n + d); o.connect(g); g.connect(AC.destination); o.start(n); o.stop(n + d + 0.02); }
const somOk = () => [660, 880, 1046].forEach((f, i) => setTimeout(() => bip(f, 0.16, 0.09, 'square'), i * 55));
const somErro = () => bip(180, 0.25, 0.08, 'sawtooth');
const somColher = () => [784, 988, 1318].forEach((f, i) => setTimeout(() => bip(f, 0.2, 0.1, 'triangle'), i * 90));

class Fazenda extends Phaser.Scene {
  constructor() { super('Fazenda'); }
  preload() {
    this.load.spritesheet('tt', 'assets/images/tiny-town__Tilemap_tilemap_packed.png', { frameWidth: 16, frameHeight: 16 });
  }
  create() {
    const cl = document.getElementById('carregando'); if (cl) cl.remove();
    this.desafioAberto = false; this.colhidos = 0;
    this.physics.world.setBounds(0, 0, WW, WH);

    // ---- CHAO (grama) ----
    for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
      const idx = Math.random() < 0.82 ? T.GRASS : Phaser.Utils.Array.GetRandom([T.GRASS_B, T.GRASS_FLOR]);
      this.add.image(c * TILE + TILE / 2, r * TILE + TILE / 2, 'tt', idx).setScale(SCALE).setDepth(0);
    }
    // ---- CANTEIRO de terra (plots) ----
    this.plots = [];
    const px0 = 7, py0 = 5, pw = 6, ph = 4;
    for (let r = 0; r < ph; r++) for (let c = 0; c < pw; c++) {
      const tc = px0 + c, tr = py0 + r;
      this.add.image(tc * TILE + TILE / 2, tr * TILE + TILE / 2, 'tt', T.DIRT).setScale(SCALE).setDepth(1);
      this.plots.push({ x: tc * TILE + TILE / 2, y: tr * TILE + TILE / 2, estado: 'vazio', sprite: null });
    }
    // ---- solidos (arvores c/ Z + colisao, lago, cerca) ----
    this.solidos = this.physics.add.staticGroup();
    const arvores = [[2, 2], [4, 11], [16, 2], [18, 8], [10, 2], [13, 11], [2, 8], [17, 12], [6, 12], [11, 2]];
    arvores.forEach(([c, r]) => {
      const x = c * TILE + TILE / 2, y = r * TILE + TILE / 2;
      const t = this.add.image(x, y, 'tt', Phaser.Utils.Array.GetRandom(T.TREES)).setScale(SCALE * 1.15);
      t.setDepth(y + TILE / 2);                            // Z pela base (heroi passa atras)
      const b = this.solidos.create(x, y + TILE * 0.3).setScale(SCALE); b.setVisible(false);
      b.body.setSize(20, 12); b.refreshBody();
    });
    for (let c = 0; c < COLS; c++) {                                       // cerca em cima e embaixo
      [0, ROWS - 1].forEach(r => { this.add.image(c * TILE + TILE / 2, r * TILE + TILE / 2, 'tt', T.FENCE).setScale(SCALE).setDepth(2); });
    }

    // ---- HERO ----
    this.hero = this.physics.add.sprite(WW / 2, WH - TILE * 2, 'tt', T.HERO).setScale(SCALE);
    this.hero.body.setSize(9, 9).setOffset(3.5, 6);
    this.hero.setCollideWorldBounds(true);
    this.physics.add.collider(this.hero, this.solidos);
    this.cameras.main.setBounds(0, 0, WW, WH).startFollow(this.hero, true, 0.15, 0.15);
    this.cameras.main.setZoom(1);

    // ---- HUD ----
    this.hud = this.add.text(10, 8, '🌾 Colheitas: 0', { fontFamily: 'system-ui', fontSize: '20px', color: '#fff', backgroundColor: '#0007', padding: { x: 8, y: 5 } }).setScrollFactor(0).setDepth(100);
    this.aviso = this.add.text(WW / 2, 20, '', { fontFamily: 'system-ui', fontSize: '16px', color: '#fff', backgroundColor: '#0e5a2e', padding: { x: 8, y: 4 } }).setOrigin(0.5, 0).setScrollFactor(0).setDepth(100);
    this.dizer('Ande até a terra marrom e aperte ESPAÇO (ou o botão) para plantar!');

    // ---- input ----
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    this.tecAcao = this.input.keyboard.addKey('SPACE');
    this.tecAcao.on('down', () => { initA(); this.interagir(); });
    this.input.on('pointerdown', () => initA());
    // botao "AÇÃO" na tela (touch)
    const btn = this.add.text(WW - 70, WH - 10, 'AÇÃO', { fontFamily: 'system-ui', fontSize: '18px', color: '#fff', backgroundColor: '#c46b1e', padding: { x: 12, y: 8 } }).setOrigin(1, 1).setScrollFactor(0).setDepth(100).setInteractive({ useHandCursor: true });
    btn.on('pointerdown', () => { initA(); this.interagir(); });

    this.overlay = this.add.container(0, 0).setScrollFactor(0).setDepth(200).setVisible(false);
    this.anim = 0;

    // QA
    window.__interagir = () => this.interagir();
    window.__certo = () => this.responder(true, { setFillStyle() {} });
    window.__colhidos = () => this.colhidos;
    window.__irPara = (x, y) => { this.hero.setPosition(x, y); };
    window.__ready = true;
  }

  dizer(t) { this.aviso.setText(t); }

  plotPerto() {
    let melhor = null, dmin = 999;
    for (const p of this.plots) { const d = Phaser.Math.Distance.Between(this.hero.x, this.hero.y, p.x, p.y); if (d < dmin) { dmin = d; melhor = p; } }
    return dmin < TILE * 0.9 ? melhor : null;
  }

  interagir() {
    if (this.desafioAberto) return;
    const p = this.plotPerto();
    if (!p) { this.dizer('Chegue mais perto da terra marrom para plantar.'); return; }
    if (p.estado === 'vazio') { this.plotAlvo = p; this.abrirDesafio(); }
    else if (p.estado === 'pronto') { this.colher(p); }
    else { this.dizer('Essa plantinha ainda está crescendo… 🌱'); }
  }

  // ------- trava pedagogica (matematica) para plantar -------
  abrirDesafio() {
    this.desafioAberto = true; bip(880, 0.14, 0.1, 'square');
    const a = Phaser.Math.Between(2, 9), b = Phaser.Math.Between(2, 9), certo = a + b;
    const ops = Phaser.Utils.Array.Shuffle([certo, certo + 1, Math.max(0, certo - 2)]);
    this.overlay.removeAll(true);
    this.overlay.add(this.add.rectangle(WW / 2, WH / 2, WW, WH, 0x00160a, 0.62));
    this.overlay.add(this.add.rectangle(WW / 2, 190, 460, 120, 0xfff6e0).setStrokeStyle(5, 0x86c34a));
    this.overlay.add(this.add.text(WW / 2, 160, 'Para plantar, resolva:', { fontFamily: 'system-ui', fontSize: '18px', color: '#2e5a1e' }).setOrigin(0.5));
    this.overlay.add(this.add.text(WW / 2, 200, a + ' + ' + b + ' = ?', { fontFamily: 'system-ui', fontSize: '36px', color: '#173a10', fontStyle: 'bold' }).setOrigin(0.5));
    ops.forEach((n, i) => {
      const bx = WW / 2 - 150 + i * 150, by = 300;
      const bt = this.add.rectangle(bx, by, 120, 70, 0x4a8f2e).setStrokeStyle(3, 0x2e5a1e).setInteractive({ useHandCursor: true });
      const tx = this.add.text(bx, by, String(n), { fontFamily: 'system-ui', fontSize: '30px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
      bt.on('pointerover', () => bt.setFillStyle(0x5faf3a)); bt.on('pointerout', () => bt.setFillStyle(0x4a8f2e));
      bt.on('pointerdown', () => this.responder(n === certo, bt));
      this.overlay.add([bt, tx]);
    });
    this.overlay.setVisible(true);
  }
  responder(ok, bt) {
    if (ok) { bt.setFillStyle(0x2ecc71); somOk(); this.time.delayedCall(200, () => { this.overlay.setVisible(false); this.desafioAberto = false; this.plantar(this.plotAlvo); }); }
    else { bt.setFillStyle(0xe74c3c); somErro(); this.cameras.main.shake(180, 0.005); this.time.delayedCall(450, () => { this.overlay.setVisible(false); this.desafioAberto = false; this.dizer('Quase! Tente plantar de novo.'); }); }
  }

  plantar(p) {
    p.estado = 'crescendo';
    const s = this.add.image(p.x, p.y, 'tt', T.SPROUT).setScale(SCALE * 0.6).setDepth(p.y);
    p.sprite = s; this.dizer('Plantou! 🌱 Agora espere crescer…');
    this.tweens.add({ targets: s, scale: SCALE * 0.9, duration: 400, yoyo: false });
    // cresce em ~5s: troca sprout -> crop
    this.time.delayedCall(5000, () => {
      if (p.estado !== 'crescendo') return;
      p.estado = 'pronto'; s.setTexture('tt', T.CROP); s.setScale(SCALE);
      this.tweens.add({ targets: s, scale: SCALE * 1.12, duration: 300, yoyo: true, repeat: -1 });
      this.dizer('Trigo pronto! ✨ Chegue perto e aperte AÇÃO pra colher.');
    });
  }
  colher(p) {
    somColher(); this.colhidos++; this.hud.setText('🌾 Colheitas: ' + this.colhidos);
    const s = p.sprite; if (s) { this.tweens.killTweensOf(s); this.tweens.add({ targets: s, y: s.y - 30, alpha: 0, scale: SCALE * 1.4, duration: 500, onComplete: () => s.destroy() }); }
    // confete
    for (let i = 0; i < 12; i++) { const c = this.add.circle(p.x, p.y, 4, Phaser.Utils.Array.GetRandom([0xffd24a, 0x8ed36b, 0xe0553a])).setDepth(500); const a = Math.random() * 6.28; this.tweens.add({ targets: c, x: c.x + Math.cos(a) * 60, y: c.y + Math.sin(a) * 60 - 20, alpha: 0, duration: 700, onComplete: () => c.destroy() }); }
    p.estado = 'vazio'; p.sprite = null;
    this.dizer('Colheu! 🌾 Plante mais — cada plantio é uma conta!');
  }

  update(_t, dt) {
    if (this.desafioAberto) { this.hero.body.setVelocity(0, 0); return; }
    let vx = 0, vy = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown) vx = -1;
    if (this.cursors.right.isDown || this.wasd.D.isDown) vx = 1;
    if (this.cursors.up.isDown || this.wasd.W.isDown) vy = -1;
    if (this.cursors.down.isDown || this.wasd.S.isDown) vy = 1;
    const v = new Phaser.Math.Vector2(vx, vy); if (v.length() > 0) v.normalize();
    this.hero.body.setVelocity(v.x * 130, v.y * 130);
    const andando = v.length() > 0;
    if (vx < 0) this.hero.setFlipX(true); else if (vx > 0) this.hero.setFlipX(false);
    // "andar" (bob) — 1 quadro + squash (kit nao tem walk cycle); Z pela base
    this.anim += dt / 1000;
    this.hero.setScale(SCALE, SCALE + (andando ? Math.abs(Math.sin(this.anim * 12)) * 0.25 : 0));
    this.hero.setDepth(this.hero.y);
  }
}

new Phaser.Game({
  type: Phaser.CANVAS,                    // CANVAS: leve p/ PC velho sem GPU
  parent: 'jogo',
  width: WW, height: WH,
  pixelArt: true, roundPixels: true,
  backgroundColor: '#5fae4a',
  physics: { default: 'arcade', arcade: { debug: false } },
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  scene: Fazenda
});
