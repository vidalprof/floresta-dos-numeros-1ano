'use strict';
// ============================================================================
// A HORTA DOS NÚMEROS — contar até 30 (1º ano). Segue EDUVERSE-FILOSOFIA:
// o MUNDO precisa (bichos com fome, horta vazia) -> a criança PLANTA e conta ->
// descobre o padrão (de 6 em 6) -> conceito por ÚLTIMO -> reflexão.
// O BYTE é um PAPAGAIO que acompanha a criança e PERGUNTA (não responde); a fala
// sai num BALÃO BRANCO ARREDONDADO (quadrinho) com rabinho apontando pra ele.
// Nome falado (voz Antonio). Sem prova/tranca, sem cronômetro, sem punição.
// Sprites REAIS (LPC/CC0 — ver CREDITOS.md). Cena MUNDO (jogo) + cena UI (HUD/
// número/medalha, sem zoom). Phaser CANVAS (leve p/ PC antigo).
// ============================================================================
const F = 64, HERO_SC = 1.0, WW = 1280, WH = 960, ZOOM = 1.6;
const IDLE = { up: 0, left: 9, down: 18, right: 27 };
const ALVO_PLOT = 6, META = 30;
const PLOTS = [[640, 470], [330, 300], [1010, 300], [980, 760], [430, 810]];  // 5 x 6 = 30

// ---------- SOM (Web Audio, começa no 1º gesto) ----------------------------
let AC = null, MASTER = null, _windGain = null, _somOn = false;
function initSom() {
  if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)();
    MASTER = AC.createGain(); MASTER.gain.value = 0.6; MASTER.connect(AC.destination);
    const buf = AC.createBuffer(1, AC.sampleRate * 2, AC.sampleRate);
    const d = buf.getChannelData(0); let last = 0;
    for (let i = 0; i < d.length; i++) { const wn = Math.random() * 2 - 1; last = (last + 0.02 * wn) / 1.02; d[i] = last * 3.2; }
    const src = AC.createBufferSource(); src.buffer = buf; src.loop = true;
    const lp = AC.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 520;
    _windGain = AC.createGain(); _windGain.gain.value = 0.045;
    src.connect(lp); lp.connect(_windGain); _windGain.connect(MASTER); src.start();
    _somOn = true;
  } catch (e) { }
}
function tom(freq, dur, tipo, vol, slideTo) {
  if (!AC || !_somOn) return;
  const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain();
  o.type = tipo || 'sine'; o.frequency.setValueAtTime(freq, t);
  if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, t + dur);
  g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(vol || 0.08, t + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(g); g.connect(MASTER); o.start(t); o.stop(t + dur + 0.02);
}
function somPop() { tom(520, 0.16, 'triangle', 0.1, 900); }
function somPasso() { tom(150, 0.1, 'triangle', 0.05, 70); }
function somPassaro() { if (Math.random() < 0.7) { tom(2200, 0.1, 'sine', 0.07, 3000); setTimeout(() => tom(2600, 0.09, 'sine', 0.06, 3200), 130); } }
function somCerto() { [523, 659, 784].forEach((f, i) => setTimeout(() => tom(f, 0.22, 'triangle', 0.09), i * 90)); }
function somFanfarra() { [523, 659, 784, 1046, 784, 1046].forEach((f, i) => setTimeout(() => tom(f, 0.3, 'triangle', 0.1), i * 140)); }
function rajadaSom() {
  if (!_windGain || !AC) return; const t = AC.currentTime;
  _windGain.gain.cancelScheduledValues(t); _windGain.gain.setValueAtTime(_windGain.gain.value, t);
  _windGain.gain.linearRampToValueAtTime(0.1, t + 0.8); _windGain.gain.linearRampToValueAtTime(0.045, t + 2.6);
}

// ============================== CENA DE UI (sem zoom) — só HUD/número/medalha =
class UI extends Phaser.Scene {
  constructor() { super({ key: 'UI' }); }
  create() {
    this.hud = this.add.text(16, 14, '🌱 0 plantadas', { fontFamily: 'system-ui', fontSize: '24px', color: '#fff', stroke: '#173a52', strokeThickness: 6 }).setDepth(9000);
    this.scale.on('resize', () => { if (this.hudMedalha) this.hudMedalha.setPosition(this.scale.width / 2, this.scale.height / 2); });
  }
  setHUD(t) { this.hud.setText(t); }
  numerao(n) {
    const t = this.add.text(this.scale.width / 2, this.scale.height * 0.2, String(n), { fontFamily: 'system-ui', fontSize: '90px', color: '#fff359', stroke: '#173a52', strokeThickness: 10, fontStyle: 'bold' })
      .setOrigin(0.5).setDepth(9600).setScale(0.4);
    this.tweens.add({ targets: t, scale: 1.15, duration: 180, ease: 'Back.easeOut' });
    this.tweens.add({ targets: t, alpha: 0, y: '-=34', delay: 480, duration: 420, onComplete: () => t.destroy() });
  }
  confete() {
    const cores = [0xff5a5a, 0xffd76a, 0x5ad1ff, 0x8aff7a, 0xff8ad1];
    for (let i = 0; i < 46; i++) {
      const r = this.add.rectangle(Math.random() * this.scale.width, -20, 9, 13, cores[i % cores.length]).setDepth(9650);
      this.tweens.add({ targets: r, y: this.scale.height + 30, angle: Math.random() * 720 - 360, x: '+=' + (Math.random() * 120 - 60), duration: 1800 + Math.random() * 1400, delay: Math.random() * 500, onComplete: () => r.destroy() });
    }
  }
  medalha(onRestart) {
    const m = this.add.container(this.scale.width / 2, this.scale.height / 2).setDepth(9900);
    const bg = this.add.rectangle(0, 0, 320, 190, 0x11314a, 0.96).setStrokeStyle(4, 0xffd76a);
    const med = this.add.text(0, -38, '🏅', { fontSize: '66px' }).setOrigin(0.5);
    const t1 = this.add.text(0, 36, 'AMIGO(A) DA HORTA', { fontFamily: 'system-ui', fontSize: '21px', color: '#ffd76a', fontStyle: 'bold' }).setOrigin(0.5);
    const t2 = this.add.text(0, 66, 'Toque para brincar de novo', { fontFamily: 'system-ui', fontSize: '13px', color: '#cfe' }).setOrigin(0.5);
    m.add([bg, med, t1, t2]); m.setScale(0.2); this.hudMedalha = m;
    this.tweens.add({ targets: m, scale: 1, duration: 500, ease: 'Back.easeOut' });
    this.tweens.add({ targets: med, angle: { from: -8, to: 8 }, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    this.time.delayedCall(900, () => this.input.once('pointerdown', () => { m.destroy(); this.hudMedalha = null; if (onRestart) onRestart(); }));
  }
}

// ============================== CENA DO MUNDO ===============================
class Mundo extends Phaser.Scene {
  constructor() { super({ key: 'Mundo' }); }
  preload() {
    const B = 'assets/mundo/cut/';
    this.load.image('grass', B + 'grass1.png'); this.load.image('dirt', B + 'dirt.png');
    this.load.image('tree', B + 'tree.png'); this.load.image('pine', B + 'pine.png');
    this.load.image('pond', B + 'pond.png');
    this.load.spritesheet('hero', 'assets/hero.png', { frameWidth: F, frameHeight: F });
  }
  create() {
    this.total = 0; this.ativo = false; this.plotAtivo = null; this._venceu = false; this.dlgAberto = false;
    if (!this.scene.isActive('UI')) this.scene.launch('UI');
    this.ui = this.scene.get('UI');

    this.add.tileSprite(0, 0, WW, WH, 'grass').setOrigin(0).setDepth(-100);
    this.plots = PLOTS.map(([x, y]) => { this.add.tileSprite(x, y, 100, 100, 'dirt').setDepth(-90); return { x, y, count: 0, done: false, cel: 0 }; });

    this.blocos = this.physics.add.staticGroup();
    const solido = (x, y, w, h) => { const z = this.add.zone(x, y, w, h); this.physics.add.existing(z, true); this.blocos.add(z); };
    const lago = this.add.image(190, 720, 'pond').setDepth(720); solido(lago.x, lago.y + 6, 70, 48);

    const arvores = [['tree', 140, 180], ['pine', 700, 130], ['tree', 1150, 200], ['pine', 1180, 470], ['tree', 120, 470], ['pine', 640, 900], ['tree', 1180, 860], ['tree', 250, 900], ['pine', 820, 560], ['tree', 470, 600]];
    arvores.forEach(([tipo, x, y], i) => {
      const a = this.add.image(x, y, tipo).setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: a, angle: { from: -1.6, to: 1.6 }, duration: 2000 + (i % 5) * 220, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: (i % 7) * 250 });
      solido(x, y - 7, tipo === 'pine' ? 16 : 22, 14);
    });

    this.bichos = [];
    [['🐰', 900, 200], ['🐿️', 760, 640], ['🐦', 520, 380]].forEach(([e, x, y]) => {
      const b = this.add.text(x, y, e, { fontSize: '30px' }).setOrigin(0.5).setDepth(y);
      this.tweens.add({ targets: b, y: y - 6, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
      this.bichos.push(b);
    });

    this.anims.create({ key: 'up', frames: this.anims.generateFrameNumbers('hero', { start: 1, end: 8 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'left', frames: this.anims.generateFrameNumbers('hero', { start: 10, end: 17 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'down', frames: this.anims.generateFrameNumbers('hero', { start: 19, end: 26 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'right', frames: this.anims.generateFrameNumbers('hero', { start: 28, end: 35 }), frameRate: 10, repeat: -1 });

    this.sombra = this.add.ellipse(640, 480, 30, 12, 0x000000, 0.22);
    this.hero = this.physics.add.sprite(640, 480, 'hero', IDLE.down).setScale(HERO_SC);
    this.hero.body.setSize(20, 14).setOffset(22, 46);
    this.hero.setCollideWorldBounds(true);
    this.physics.add.collider(this.hero, this.blocos);
    this.dir = 'down'; this._passoT = 0; this._forc = null;
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    // NÃO roubar as teclas do campo de NOME (Phaser dá preventDefault em W/A/S/D/setas
    // e algumas letras não digitavam). O jogo ainda LÊ as teclas; só não bloqueia o DOM.
    this.input.keyboard.clearCaptures();
    this.input.keyboard.disableGlobalCapture();

    this.physics.world.setBounds(0, 0, WW, WH);
    this.cameras.main.setBounds(0, 0, WW, WH).setZoom(ZOOM).startFollow(this.hero, true, 0.12, 0.12);

    // ---- BYTE (papagaio companheiro) + BALÃO branco arredondado ----
    this.byte = this.add.text(700, 440, '🦜', { fontSize: '30px' }).setOrigin(0.5).setDepth(9497);
    this._by = 440;
    this.balaoG = this.add.graphics().setDepth(9498).setVisible(false);
    this.balaoT = this.add.text(0, 0, '', { fontFamily: 'system-ui', fontSize: '13px', color: '#16324a', lineSpacing: 2, wordWrap: { width: 150 } }).setOrigin(0, 0).setDepth(9499).setVisible(false);
    this.balaoSeta = this.add.text(0, 0, '▼', { fontSize: '13px', color: '#2e9b57' }).setOrigin(0.5).setDepth(9499).setVisible(false);

    this.marcador = this.add.text(0, 0, '👇', { fontSize: '30px' }).setOrigin(0.5).setDepth(9000).setVisible(false);
    this.tweens.add({ targets: this.marcador, y: '-=8', duration: 500, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    this.time.addEvent({ delay: 5000, loop: true, callback: rajadaSom });
    this.time.addEvent({ delay: 4200, loop: true, callback: () => { if (this._somOn2) somPassaro(); } });

    const liga = () => { initSom(); this._somOn2 = true; const dica = document.getElementById('somdica'); if (dica) dica.style.display = 'none'; };
    this.input.on('pointerdown', () => { liga(); this.aoTocar(); });
    this.input.keyboard.on('keydown', liga);

    window.__ready = true; window.__scene = this;
    window.__fs = () => { if (this.scale.isFullscreen) this.scale.stopFullscreen(); else this.scale.startFullscreen(); };
    window.__mover = (dir) => { this._forc = dir; };
    window.__parar = () => { this._forc = null; };
    window.__iniciarAtividade = () => this.iniciar();
    if (window.__nome) this.time.delayedCall(60, () => this.iniciar());
  }

  // ---------------- BALÃO DE FALA (branco, arredondado, sai do Byte) --------
  dialogo(paginas, onDone) {
    this.dlgAberto = true; this.marcador.setVisible(false);
    this._pgs = paginas.slice(); this._pg = 0; this._onDone = onDone || null;
    this.balaoG.setVisible(true); this.balaoT.setVisible(true);
    this.mostra();
  }
  mostra() {
    const full = this._pgs[this._pg]; this._full = full; this._n = 0; this._typing = true;
    this.balaoT.setText(''); this.balaoSeta.setVisible(false);
    if (this._typer) this._typer.remove();
    this._typer = this.time.addEvent({ delay: 26, loop: true, callback: () => {
      this._n++; this.balaoT.setText(full.slice(0, this._n));
      if (this._n % 2 === 0) tom(430, 0.03, 'square', 0.02);
      if (this._n >= full.length) { this._typing = false; this.balaoSeta.setVisible(true); this._typer.remove(); }
    } });
  }
  avanca() {
    if (this._typing) { this._typing = false; this._typer.remove(); this.balaoT.setText(this._full); this.balaoSeta.setVisible(true); return; }
    this._pg++;
    if (this._pg < this._pgs.length) { this.mostra(); }
    else {
      this.balaoG.setVisible(false); this.balaoT.setVisible(false); this.balaoSeta.setVisible(false);
      this.dlgAberto = false; const cb = this._onDone; this._onDone = null; if (cb) cb();
    }
  }
  desenhaBalao() {
    if (!this.dlgAberto) return;
    const pad = 9, tw = Math.max(28, this.balaoT.width), th = Math.max(14, this.balaoT.height);
    const w = tw + pad * 2, h = th + pad * 2;
    const cx = this.byte.x, base = this.byte.y - 26;      // balão acima do Byte
    const rx = cx - w / 2, ry = base - h;
    this.balaoG.clear();
    this.balaoG.fillStyle(0xffffff, 0.98); this.balaoG.lineStyle(2, 0x2e9b57, 1);
    this.balaoG.fillRoundedRect(rx, ry, w, h, 9); this.balaoG.strokeRoundedRect(rx, ry, w, h, 9);
    this.balaoG.fillStyle(0xffffff, 0.98); this.balaoG.fillTriangle(cx - 7, ry + h - 1, cx + 7, ry + h - 1, cx, base + 6);   // rabinho
    this.balaoT.setPosition(rx + pad, ry + pad);
    this.balaoSeta.setPosition(rx + w - 10, ry + h - 8);
  }

  // ---------------- INÍCIO ----------------
  iniciar() {
    if (this._iniciado) return; this._iniciado = true;
    initSom(); this._somOn2 = true;
    const dica = document.getElementById('somdica'); if (dica) dica.style.display = 'none';
    this.nome = (window.__nome || 'amiguinho');
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    this.falaNome();
    this.dialogo([
      'Oi, ' + N + '! Eu sou o Byte.',
      'Os bichinhos estao com fome e a horta esta vazia.',
      'Me ajuda a plantar? Ande ate a terra e toque pra plantar!'
    ], () => { this.ativo = true; });
  }
  falaNome(depois) {
    try { if (window.VozNome) { const id = window.VozNome.idDe(this.nome); if (id) { window.VozNome.cadeia(['audio/' + id], depois); return; } } } catch (e) { }
    if (depois) depois();
  }

  aoTocar() {
    if (this.dlgAberto) { this.avanca(); return; }
    if (!this.ativo || this._venceu) return;
    if (this.plotAtivo && !this.plotAtivo.done) this.plantar(this.plotAtivo);
  }
  plantar(plot) {
    if (plot.count >= ALVO_PLOT) return;
    const cols = [-30, 0, 30], rows = [-18, 18], c = plot.cel;
    const cx = plot.x + cols[c % 3], cy = plot.y + rows[Math.floor(c / 3)];
    plot.cel++; plot.count++; this.total++;
    const planta = this.add.image(cx, cy, 'tree').setOrigin(0.5, 1).setScale(0.02).setDepth(cy);
    this.tweens.add({ targets: planta, scale: 0.26, duration: 380, ease: 'Back.easeOut' });
    somPop(); this.ui.numerao(this.total); this.ui.setHUD('🌱 ' + this.total + ' plantadas');
    if (plot.count >= ALVO_PLOT) { plot.done = true; this.marcador.setVisible(false); this.plotDone(); }
  }
  plotDone() {
    somCerto(); this.falaNome();
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    this.plots.forEach(p => { if (p.done) this.brilho(p.x, p.y); });
    if (this.total >= META) { this.vencer(); return; }
    const feitos = this.plots.filter(p => p.done).length;
    let fala;
    if (feitos === 1) fala = ['Boa, ' + N + '! Quantas voce plantou aqui?', 'Vamos ao proximo canteiro!'];
    else if (feitos === 2) fala = ['Os canteiros tem a MESMA quantidade!', 'Tem um jeito mais rapido de contar?'];
    else if (feitos === 3) fala = ['Achou um padrao? Seis, doze, dezoito...', 'Vamos plantar mais!'];
    else fala = ['Falta pouco, ' + N + '!', 'Quantas vao ter no total?'];
    this.dialogo(fala);
  }
  brilho(x, y) {
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2, s = this.add.text(x, y - 20, '✨', { fontSize: '18px' }).setOrigin(0.5).setDepth(9000);
      this.tweens.add({ targets: s, x: x + Math.cos(a) * 46, y: y - 20 + Math.sin(a) * 40, alpha: 0, duration: 700, onComplete: () => s.destroy() });
    }
  }
  vencer() {
    if (this._venceu) return; this._venceu = true; this.ativo = false;
    somFanfarra();
    this.bichos.forEach((b, i) => {
      const alvo = this.plots[i % this.plots.length];
      this.tweens.add({ targets: b, x: alvo.x + (i % 2 ? 30 : -30), y: alvo.y, duration: 1200, ease: 'Sine.inOut', delay: i * 250, onComplete: () => this.tweens.add({ targets: b, y: '-=10', duration: 300, yoyo: true, repeat: -1 }) });
    });
    this.ui.confete();
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    this.falaNome();
    this.time.delayedCall(700, () => this.dialogo([
      'Voce conseguiu, ' + N + '! A horta esta viva!',
      'Olha os bichinhos vindo comer!',
      'Eram 5 canteiros de 6: seis, doze, dezoito, vinte e quatro, trinta!',
      'Da pra contar de 6 em 6, bem mais rapido!',
      'O que voce mais gostou hoje?'
    ], () => this.ui.medalha(() => { this._iniciado = false; this.scene.restart(); })));
  }

  update(time) {
    const livre = this.ativo && !this.dlgAberto && !this._venceu;
    let vx = 0, vy = 0;
    if (livre) {
      if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') vx = -1;
      else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') vx = 1;
      else if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') vy = -1;
      else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') vy = 1;
    }
    this.hero.body.setVelocity(vx * 150, vy * 150);
    const andando = vx !== 0 || vy !== 0;
    if (vx < 0) { this.hero.anims.play('left', true); this.dir = 'left'; }
    else if (vx > 0) { this.hero.anims.play('right', true); this.dir = 'right'; }
    else if (vy < 0) { this.hero.anims.play('up', true); this.dir = 'up'; }
    else if (vy > 0) { this.hero.anims.play('down', true); this.dir = 'down'; }
    else { this.hero.anims.stop(); this.hero.setFrame(IDLE[this.dir]); }

    this.hero.setDepth(this.hero.y);
    this.sombra.setPosition(this.hero.x, this.hero.y + 24).setDepth(this.hero.y - 1);
    if (andando && time - this._passoT > 300) { somPasso(); this._passoT = time; }

    // Byte acompanha a criança (voa ao lado, flutuando)
    const tx = this.hero.x + 52, ty = this.hero.y - 30;
    this._by = Phaser.Math.Linear(this._by, ty, 0.1);
    this.byte.setPosition(Phaser.Math.Linear(this.byte.x, tx, 0.1), this._by + Math.sin(time / 320) * 3);
    if (this.dlgAberto) this.desenhaBalao();

    this.plotAtivo = null;
    if (this.ativo && !this._venceu) {
      for (const p of this.plots) { if (!p.done && Math.abs(this.hero.x - p.x) < 56 && Math.abs(this.hero.y - p.y) < 56) { this.plotAtivo = p; break; } }
    }
    if (this.plotAtivo && !this.dlgAberto) this.marcador.setPosition(this.plotAtivo.x, this.plotAtivo.y - 60).setVisible(true);
    else if (!this.plotAtivo) this.marcador.setVisible(false);
  }
}

new Phaser.Game({
  type: Phaser.CANVAS, pixelArt: true, roundPixels: true, backgroundColor: '#3f6a34',
  physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.RESIZE, parent: 'jogo', width: '100%', height: '100%' },
  scene: [Mundo, UI]
});
