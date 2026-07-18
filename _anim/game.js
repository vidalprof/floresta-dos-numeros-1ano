'use strict';
// ============================================================================
// A FLORESTA DOS BICHOS — JUNTAR quantidades (1º ano). REAPROVEITA o mundo/menino/
// Byte/bichos da Horta; muda só a DINÂMICA: em vez de plantar, a criança JUNTA
// dois grupos de frutas (vermelhas + verdes) andando por cima e recolhendo, e
// descobre quantas dão AO TODO (adição por reunião). Segue EDUVERSE-FILOSOFIA:
// mundo precisa (bichos com fome) -> age (junta/conta) -> conceito (SOMAR) por
// ÚLTIMO -> reflexão. Byte PERGUNTA. Nome falado (Antonio). Sem prova/tranca,
// sem cronômetro. 100% jogável no TOQUE (celular). Sprites LPC (CC0 — CREDITOS.md).
// ============================================================================
const F = 64, HERO_SC = 1.0, WW = 1280, WH = 960, ZOOM = 1.6;
const IDLE = { up: 104, left: 117, down: 130, right: 143 };
// cada rodada JUNTA dois grupos [vermelhas, verdes]. Números ajustáveis ao alvo.
const RODADAS = [[3, 2], [5, 4], [7, 6], [9, 8]];   // somas 5, 9, 13, 17
const CLUSTER_A = { x: 430, y: 340 }, CLUSTER_B = { x: 880, y: 660 };

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
function somColeta() { tom(600, 0.14, 'triangle', 0.09, 1000); }
function somPasso() { tom(150, 0.1, 'triangle', 0.05, 70); }
function somPassaro() { if (Math.random() < 0.7) { tom(2200, 0.1, 'sine', 0.07, 3000); setTimeout(() => tom(2600, 0.09, 'sine', 0.06, 3200), 130); } }
function somCerto() { [523, 659, 784].forEach((f, i) => setTimeout(() => tom(f, 0.22, 'triangle', 0.09), i * 90)); }
function somFanfarra() { [523, 659, 784, 1046, 784, 1046].forEach((f, i) => setTimeout(() => tom(f, 0.3, 'triangle', 0.1), i * 140)); }
function rajadaSom() {
  if (!_windGain || !AC) return; const t = AC.currentTime;
  _windGain.gain.cancelScheduledValues(t); _windGain.gain.setValueAtTime(_windGain.gain.value, t);
  _windGain.gain.linearRampToValueAtTime(0.1, t + 0.8); _windGain.gain.linearRampToValueAtTime(0.045, t + 2.6);
}

// ============================== CENA DE UI (sem zoom) =======================
class UI extends Phaser.Scene {
  constructor() { super({ key: 'UI' }); }
  create() {
    this.hud = this.add.text(16, 14, '🧺 0 na cesta', { fontFamily: 'system-ui', fontSize: '24px', color: '#fff', stroke: '#173a52', strokeThickness: 6 }).setDepth(9000);
    this.scale.on('resize', () => { if (this.hudMedalha) this.hudMedalha.setPosition(this.scale.width / 2, this.scale.height / 2); });
  }
  setHUD(t) { this.hud.setText(t); }
  numerao(n) {
    const t = this.add.text(this.scale.width / 2, this.scale.height * 0.2, String(n), { fontFamily: 'system-ui', fontSize: '90px', color: '#fff359', stroke: '#173a52', strokeThickness: 10, fontStyle: 'bold' })
      .setOrigin(0.5).setDepth(9600).setScale(0.4);
    this.tweens.add({ targets: t, scale: 1.15, duration: 180, ease: 'Back.easeOut' });
    this.tweens.add({ targets: t, alpha: 0, y: '-=34', delay: 460, duration: 420, onComplete: () => t.destroy() });
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
    const bg = this.add.rectangle(0, 0, 330, 190, 0x11314a, 0.96).setStrokeStyle(4, 0xffd76a);
    const med = this.add.text(0, -38, '🏅', { fontSize: '66px' }).setOrigin(0.5);
    const t1 = this.add.text(0, 36, 'AMIGO(A) DOS BICHOS', { fontFamily: 'system-ui', fontSize: '20px', color: '#ffd76a', fontStyle: 'bold' }).setOrigin(0.5);
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
    this.total = 0; this.ativo = false; this._venceu = false; this.dlgAberto = false;
    this.rodada = 0; this.frutas = []; this.coletadas = 0; this.alvo = 0;
    if (!this.scene.isActive('UI')) this.scene.launch('UI');
    this.ui = this.scene.get('UI');

    this.add.tileSprite(0, 0, WW, WH, 'grass').setOrigin(0).setDepth(-100);

    this.blocos = this.physics.add.staticGroup();
    const solido = (x, y, w, h) => { const z = this.add.zone(x, y, w, h); this.physics.add.existing(z, true); this.blocos.add(z); };
    const lago = this.add.image(190, 720, 'pond').setDepth(720); solido(lago.x, lago.y + 6, 70, 48);

    const arvores = [['tree', 140, 180], ['pine', 700, 130], ['tree', 1150, 200], ['pine', 1180, 470], ['tree', 120, 470], ['pine', 640, 900], ['tree', 1180, 860], ['tree', 250, 900], ['pine', 1040, 560], ['tree', 300, 620]];
    arvores.forEach(([tipo, x, y], i) => {
      const a = this.add.image(x, y, tipo).setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: a, angle: { from: -1.6, to: 1.6 }, duration: 2000 + (i % 5) * 220, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: (i % 7) * 250 });
      solido(x, y - 7, tipo === 'pine' ? 16 : 22, 14);
    });

    this.bichos = [];
    [['🐰', 1080, 250], ['🐿️', 700, 880], ['🐦', 1120, 700]].forEach(([e, x, y]) => {
      this.add.ellipse(x, y, 26, 9, 0x000000, 0.22).setDepth(y - 1);           // sombra (não flutua)
      const b = this.add.text(x, y, e, { fontSize: '30px' }).setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: b, y: y - 3, duration: 850, yoyo: true, repeat: -1, ease: 'Sine.inOut' });   // balanço leve
      this.bichos.push(b);
    });

    this.anims.create({ key: 'up', frames: this.anims.generateFrameNumbers('hero', { start: 105, end: 112 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'left', frames: this.anims.generateFrameNumbers('hero', { start: 118, end: 125 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'down', frames: this.anims.generateFrameNumbers('hero', { start: 131, end: 138 }), frameRate: 10, repeat: -1 });
    this.anims.create({ key: 'right', frames: this.anims.generateFrameNumbers('hero', { start: 144, end: 151 }), frameRate: 10, repeat: -1 });

    this.sombra = this.add.ellipse(640, 480, 30, 12, 0x000000, 0.22);
    this.hero = this.physics.add.sprite(640, 480, 'hero', IDLE.down).setScale(HERO_SC);
    this.hero.body.setSize(20, 14).setOffset(22, 46);
    this.hero.setCollideWorldBounds(true);
    this.physics.add.collider(this.hero, this.blocos);
    this.dir = 'down'; this._passoT = 0; this._forc = null;
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    this.input.keyboard.clearCaptures(); this.input.keyboard.disableGlobalCapture();

    this.physics.world.setBounds(0, 0, WW, WH);
    this.cameras.main.setBounds(0, 0, WW, WH).setZoom(ZOOM).startFollow(this.hero, true, 0.12, 0.12);

    // Byte (papagaio) + balão branco
    this.byte = this.add.text(700, 440, '🦜', { fontSize: '30px' }).setOrigin(0.5).setDepth(9497); this._by = 440;
    this.balaoG = this.add.graphics().setDepth(9498).setVisible(false);
    this.balaoT = this.add.text(0, 0, '', { fontFamily: 'system-ui', fontSize: '13px', color: '#16324a', lineSpacing: 2, wordWrap: { width: 150 } }).setOrigin(0, 0).setDepth(9499).setVisible(false);
    this.balaoSeta = this.add.text(0, 0, '▼', { fontSize: '13px', color: '#2e9b57' }).setOrigin(0.5).setDepth(9499).setVisible(false);

    this.time.addEvent({ delay: 5000, loop: true, callback: rajadaSom });
    this.time.addEvent({ delay: 4200, loop: true, callback: () => { if (this._somOn2) somPassaro(); } });

    const liga = () => { initSom(); this._somOn2 = true; const dica = document.getElementById('somdica'); if (dica) dica.style.display = 'none'; };
    this.destino = null;
    this.input.on('pointerdown', (pointer) => { liga(); this.aoTocar(pointer); });
    this.input.keyboard.on('keydown', liga);

    window.__ready = true; window.__scene = this;
    window.__fs = () => { if (this.scale.isFullscreen) this.scale.stopFullscreen(); else this.scale.startFullscreen(); };
    window.__mover = (dir) => { this._forc = dir; };
    window.__parar = () => { this._forc = null; };
    window.__iniciarAtividade = () => this.iniciar();
    if (window.__nome) this.time.delayedCall(60, () => this.iniciar());
  }

  // ---------------- BALÃO ----------------
  dialogo(paginas, onDone) {
    this.dlgAberto = true; this._pgs = paginas.slice(); this._pg = 0; this._onDone = onDone || null;
    this.balaoG.setVisible(true); this.balaoT.setVisible(true); this.mostra();
  }
  mostra() {
    const full = this._pgs[this._pg]; this._full = full; this._n = 0; this._typing = true;
    this.balaoT.setText(''); this.balaoSeta.setVisible(false);
    if (this._typer) this._typer.remove(); if (this._auto) this._auto.remove();
    this._typer = this.time.addEvent({ delay: 26, loop: true, callback: () => {
      this._n++; this.balaoT.setText(full.slice(0, this._n));
      if (this._n % 2 === 0) tom(430, 0.03, 'square', 0.02);
      if (this._n >= full.length) {
        this._typing = false; this.balaoSeta.setVisible(true); this._typer.remove();
        // AUTO-avança (não trava o boneco — a criança anda o tempo todo)
        const espera = 800 + full.length * 26;
        this._auto = this.time.delayedCall(espera, () => this.avanca());
      }
    } });
  }
  avanca() {
    if (this._auto) { this._auto.remove(); this._auto = null; }
    if (this._typing) { this._typing = false; this._typer.remove(); this.balaoT.setText(this._full); this.balaoSeta.setVisible(true); return; }
    this._pg++;
    if (this._pg < this._pgs.length) { this.mostra(); }
    else { this.balaoG.setVisible(false); this.balaoT.setVisible(false); this.balaoSeta.setVisible(false); this.dlgAberto = false; const cb = this._onDone; this._onDone = null; if (cb) cb(); }
  }
  desenhaBalao() {
    if (!this.dlgAberto) return;
    const pad = 9, tw = Math.max(28, this.balaoT.width), th = Math.max(14, this.balaoT.height);
    const w = tw + pad * 2, h = th + pad * 2, cx = this.byte.x, base = this.byte.y - 26, rx = cx - w / 2, ry = base - h;
    this.balaoG.clear();
    this.balaoG.fillStyle(0xffffff, 0.98); this.balaoG.lineStyle(2, 0x2e9b57, 1);
    this.balaoG.fillRoundedRect(rx, ry, w, h, 9); this.balaoG.strokeRoundedRect(rx, ry, w, h, 9);
    this.balaoG.fillStyle(0xffffff, 0.98); this.balaoG.fillTriangle(cx - 7, ry + h - 1, cx + 7, ry + h - 1, cx, base + 6);
    this.balaoT.setPosition(rx + pad, ry + pad); this.balaoSeta.setPosition(rx + w - 10, ry + h - 8);
  }

  // ---------------- INÍCIO ----------------
  iniciar() {
    if (this._iniciado) return; this._iniciado = true;
    initSom(); this._somOn2 = true;
    const dica = document.getElementById('somdica'); if (dica) dica.style.display = 'none';
    this.nome = (window.__nome || 'amiguinho');
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    this.falaNome();
    this.ativo = true;   // já pode andar e recolher enquanto o Byte fala (não trava)
    this.iniciarRodada();
  }
  falaNome(depois) {
    try { if (window.VozNome) { const id = window.VozNome.idDe(this.nome); if (id) { window.VozNome.cadeia(['audio/' + id], depois); return; } } } catch (e) { }
    if (depois) depois();
  }

  // ---------------- RODADAS (juntar dois grupos) ----------------
  iniciarRodada() {
    const [a, b] = RODADAS[this.rodada];
    this.aRod = a; this.bRod = b; this.alvo = a + b; this.coletadas = 0;
    this.frutas.forEach(f => { if (f._sh) f._sh.destroy(); f.destroy(); }); this.frutas = [];
    this.poeFrutas('🍎', a, CLUSTER_A); this.poeFrutas('🍏', b, CLUSTER_B);
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    const fala = (this.rodada === 0)
      ? ['Oi, ' + N + '! Os bichinhos estao com fome!', 'Ande por cima das frutas pra recolher.', 'Junte as ' + a + ' vermelhas com as ' + b + ' verdes. Quantas dao ao todo?']
      : ['Junte as ' + a + ' vermelhas com as ' + b + ' verdes!', 'Quantas dao ao todo?'];
    this.dialogo(fala);
  }
  poeFrutas(emoji, n, centro) {
    for (let i = 0; i < n; i++) {
      const col = i % 4, lin = Math.floor(i / 4);
      const x = centro.x + (col - 1.5) * 30 + Phaser.Math.Between(-5, 5);
      const y = centro.y + (lin - (Math.floor((n - 1) / 4)) / 2) * 30 + Phaser.Math.Between(-5, 5);
      const sh = this.add.ellipse(x, y, 18, 6, 0x000000, 0.2).setDepth(y - 1);   // sombra
      const fr = this.add.text(x, y, emoji, { fontSize: '24px' }).setOrigin(0.5, 1).setDepth(y);
      this.tweens.add({ targets: fr, y: y - 3, duration: 650, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: i * 60 });
      fr._coletada = false; fr._sh = sh; this.frutas.push(fr);
    }
  }
  aoTocar(pointer) {
    // toque = ANDAR (o balão é automático e não trava o boneco)
    if (!this.ativo || this._venceu) return;
    const wp = pointer ? this.cameras.main.getWorldPoint(pointer.x, pointer.y) : { x: this.hero.x, y: this.hero.y };
    this.destino = { x: Phaser.Math.Clamp(wp.x, 10, WW - 10), y: Phaser.Math.Clamp(wp.y, 10, WH - 10) };
    this._destT = this.time.now;
  }
  coletar(f) {
    if (f._coletada) return; f._coletada = true;
    this.coletadas++; this.total++;
    somColeta(); this.ui.numerao(this.coletadas); this.ui.setHUD('🧺 ' + this.total + ' na cesta');
    if (f._sh) { this.tweens.add({ targets: f._sh, alpha: 0, duration: 200, onComplete: () => f._sh.destroy() }); }
    // "voa pra cesta" (sobe e vai pro canto de cima) ao pegar
    this.tweens.add({ targets: f, y: f.y - 46, x: f.x - 26, scale: 0.15, alpha: 0, duration: 380, ease: 'Back.easeIn', onComplete: () => f.destroy() });
    if (this.coletadas >= this.alvo) this.rodadaDone();
  }
  rodadaDone() {
    somCerto(); this.falaNome();
    const a = this.aRod, b = this.bRod, s = a + b;
    this.brilho(this.hero.x, this.hero.y);
    this.rodada++;
    if (this.rodada >= RODADAS.length) {
      this.dialogo([a + ' e ' + b + ', juntando, dao ' + s + '!'], () => this.vencer());
    } else {
      this.dialogo([a + ' e ' + b + '... juntando dao ' + s + '!', 'Vamos pro proximo grupo de frutas!'], () => this.iniciarRodada());
    }
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
    this.bichos.forEach((b, i) => { this.tweens.add({ targets: b, x: this.hero.x + (i % 2 ? 40 : -40), y: this.hero.y + 20, duration: 1200, ease: 'Sine.inOut', delay: i * 250, onComplete: () => this.tweens.add({ targets: b, y: '-=10', duration: 300, yoyo: true, repeat: -1 }) }); });
    this.ui.confete();
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    this.falaNome();
    this.time.delayedCall(700, () => this.dialogo([
      'Voce conseguiu, ' + N + '! Os bichinhos vao comer!',
      'Cada vez a gente JUNTOU dois grupos de frutas...',
      'Juntar dois grupos e o mesmo que SOMAR! Voce somou de verdade!',
      'O que voce mais gostou hoje?'
    ], () => this.ui.medalha(() => { this._iniciado = false; this.scene.restart(); })));
  }

  update(time) {
    const livre = this.ativo && !this._venceu;   // fala NÃO trava o boneco (balão é automático)
    let vx = 0, vy = 0;
    if (livre) {
      let kx = 0, ky = 0;
      if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') kx = -1;
      else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') kx = 1;
      if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') ky = -1;
      else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') ky = 1;
      if (kx || ky) { this.destino = null; vx = kx; vy = ky; }
      else if (this.destino) {
        const dx = this.destino.x - this.hero.x, dy = this.destino.y - this.hero.y, d = Math.hypot(dx, dy);
        if (d < 8 || time - this._destT > 4000) { this.destino = null; } else { vx = dx / d; vy = dy / d; }
      }
    } else { this.destino = null; }
    this.hero.body.setVelocity(vx * 150, vy * 150);
    const andando = vx !== 0 || vy !== 0;
    if (andando) { this.dir = (Math.abs(vx) >= Math.abs(vy)) ? (vx < 0 ? 'left' : 'right') : (vy < 0 ? 'up' : 'down'); this.hero.anims.play(this.dir, true); }
    else { this.hero.anims.stop(); this.hero.setFrame(IDLE[this.dir]); }

    this.hero.setDepth(this.hero.y);
    this.sombra.setPosition(this.hero.x, this.hero.y + 24).setDepth(this.hero.y - 1);
    if (andando && time - this._passoT > 300) { somPasso(); this._passoT = time; }

    // Byte acompanha
    const tx = this.hero.x + 52, ty = this.hero.y - 30;
    this._by = Phaser.Math.Linear(this._by, ty, 0.1);
    this.byte.setPosition(Phaser.Math.Linear(this.byte.x, tx, 0.1), this._by + Math.sin(time / 320) * 3);
    if (this.dlgAberto) this.desenhaBalao();

    // RECOLHE frutas ao passar por cima (funciona mesmo com o balão aberto)
    if (this.ativo && !this._venceu) {
      for (const f of this.frutas) {
        if (!f._coletada && Math.abs(this.hero.x - f.x) < 26 && Math.abs(this.hero.y - f.y) < 30) this.coletar(f);
      }
    }
  }
}

new Phaser.Game({
  type: Phaser.CANVAS, pixelArt: true, roundPixels: true, backgroundColor: '#3f6a34',
  physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.RESIZE, parent: 'jogo', width: '100%', height: '100%' },
  scene: [Mundo, UI]
});
