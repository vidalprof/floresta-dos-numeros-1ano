'use strict';
// ============================================================================
// JOGO KENNEY COMPLETO — "O Tesouro dos Dois Montes" (JUNTAR quantidades, 1º ano).
// TODOS os sprites são Kenney roguelike (CC0) — ZERO emoji (roda em PC antigo).
// Personagem e guia ganham VIDA por CÓDIGO (respira/pula/squash/sombra). Mundo
// com vento (árvores/arbustos) + colisão. A criança JUNTA as moedas de OURO com
// as de PRATA (anda por cima), conta, e descobre o total (soma). Balão branco
// desenhado por código (sem emoji), fala AUTOMÁTICA (não trava). Toque pra andar.
// ============================================================================
const WW = 1200, WH = 900, ZOOM = 2.0, S = 3.4, ST = 6.4, SB = 3.2, SM = 3.6, SG = 3.2;
const RODADAS = [[3, 2], [5, 4], [7, 6], [9, 8]];          // [ouro, prata]
const CA = { x: 420, y: 330 }, CB = { x: 860, y: 640 };

// ---------- SOM ----------
let AC = null, MASTER = null, _wg = null, _on = false;
function initSom() {
  if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)();
    MASTER = AC.createGain(); MASTER.gain.value = 0.6; MASTER.connect(AC.destination);
    const buf = AC.createBuffer(1, AC.sampleRate * 2, AC.sampleRate); const d = buf.getChannelData(0); let last = 0;
    for (let i = 0; i < d.length; i++) { const wn = Math.random() * 2 - 1; last = (last + 0.02 * wn) / 1.02; d[i] = last * 3.2; }
    const src = AC.createBufferSource(); src.buffer = buf; src.loop = true;
    const lp = AC.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 520;
    _wg = AC.createGain(); _wg.gain.value = 0.045; src.connect(lp); lp.connect(_wg); _wg.connect(MASTER); src.start(); _on = true;
  } catch (e) { }
}
function tom(f, dur, tp, v, sl) { if (!AC || !_on) return; const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain(); o.type = tp || 'sine'; o.frequency.setValueAtTime(f, t); if (sl) o.frequency.exponentialRampToValueAtTime(sl, t + dur); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v || 0.08, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.connect(g); g.connect(MASTER); o.start(t); o.stop(t + dur + 0.02); }
function somMoeda() { tom(880, 0.12, 'triangle', 0.09, 1400); }
function somPasso() { tom(150, 0.09, 'triangle', 0.04, 70); }
function somCerto() { [523, 659, 784].forEach((f, i) => setTimeout(() => tom(f, 0.22, 'triangle', 0.09), i * 90)); }
function somFanfarra() { [523, 659, 784, 1046, 784, 1046].forEach((f, i) => setTimeout(() => tom(f, 0.3, 'triangle', 0.1), i * 140)); }
function rajada() { if (!_wg || !AC) return; const t = AC.currentTime; _wg.gain.cancelScheduledValues(t); _wg.gain.setValueAtTime(_wg.gain.value, t); _wg.gain.linearRampToValueAtTime(0.1, t + 0.8); _wg.gain.linearRampToValueAtTime(0.045, t + 2.6); }

// ---------- VOZ (narração REAL gravada — Antonio/edge-tts, mp3 em audio/) ----------
// NUNCA voz do navegador (robótica/proibida). mp3 gravado toca por cima do jogo.
const Voz = (function () {
  const base = 'audio/'; let atual = null;
  function stop() { if (atual) { try { atual.pause(); } catch (e) { } atual = null; } }
  function um(id, cb) {
    if (!id) { if (cb) cb(); return; }
    let a; try { a = new Audio(base + id + '.mp3'); a.volume = 1; } catch (e) { if (cb) cb(); return; }
    atual = a;
    const fim = () => { if (atual === a) atual = null; if (cb) { const c = cb; cb = null; c(); } };
    a.onended = fim; a.onerror = fim; a.play().catch(fim);
  }
  function cadeia(ids, cb) { const f = (ids || []).filter(Boolean); (function nx(k) { if (k >= f.length) { if (cb) cb(); return; } um(f[k], () => nx(k + 1)); })(0); }
  // slug do 1º nome (igual ao workflow) p/ achar o mp3 do nome do aluno
  function slug(s) { return (s || '').trim().split(/\s+/)[0].normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]/g, ''); }
  return { stop, um, cadeia, slug };
})();
// nomes com voz gravada (banco Antonio) — greeting personalizado quando existe
const NOMES_VOZ = new Set(['agatha','alexandre','alice','amanda','ana','analu','analuz','anthony','antonella','antonio','arthur','aurora','ayla','beatriz','benicio','benjamin','bento','bernardo','bianca','bruna','bruno','bryan','caio','caleb','camila','carolina','catarina','caua','cecile','cecilia','clara','daniel','danilo','davi','diego','duda','eduardo','elisa','eloa','emanuel','emanuelly','emilly','enzo','erick','ester','esther','felipe','fernanda','fernando','gabriel','gabriela','gael','giovanna','guilherme','gustavo','heitor','helena','heloisa','henrique','ian','igor','isaac','isabela','isadora','joao','jose','julia','juliana','kaique','lara','larissa','laura','leo','leticia','levi','live','livia','liz','lorena','lorenzo','luan','lucas','luiza','maite','malu','manuela','marcos','maria','mariana','marina','matheus','melissa','miguel','milena','murilo','nathan','nicolas','nicole','noah','olivia','otavio','pedro','pietra','pietro','rael','rafael','rafaela','ravi','rebeca','rodrigo','ryan','samuel','sarah','sofia','sophia','stella','theo','thiago','valentina','vicente','vitor','vitoria','yasmin','yuri']);
function idNome(nome) { const s = Voz.slug(nome); return NOMES_VOZ.has(s) ? 'nome_' + s : ''; }

// ============================== UI (sem zoom) ==============================
class UI extends Phaser.Scene {
  constructor() { super({ key: 'UI' }); }
  preload() { this.load.image('cogHUD', 'assets/ourobar.png'); }
  create() {
    this.hud = this.add.text(16, 14, 'Barras: 0', { fontFamily: 'system-ui', fontSize: '24px', color: '#fff', stroke: '#173a52', strokeThickness: 6 }).setDepth(9000);
    this.scale.on('resize', () => { if (this.med) this.med.setPosition(this.scale.width / 2, this.scale.height / 2); });
  }
  setHUD(t) { this.hud.setText(t); }
  numerao(n) {
    const t = this.add.text(this.scale.width / 2, this.scale.height * 0.19, String(n), { fontFamily: 'system-ui', fontSize: '92px', color: '#ffe14d', stroke: '#5a3a10', strokeThickness: 10, fontStyle: 'bold' }).setOrigin(0.5).setDepth(9600).setScale(0.4);
    this.tweens.add({ targets: t, scale: 1.15, duration: 180, ease: 'Back.easeOut' });
    this.tweens.add({ targets: t, alpha: 0, y: '-=34', delay: 460, duration: 420, onComplete: () => t.destroy() });
  }
  confete() {
    const cor = [0xffd76a, 0xff5a5a, 0x5ad1ff, 0x8aff7a, 0xff8ad1];
    for (let i = 0; i < 46; i++) { const r = this.add.rectangle(Math.random() * this.scale.width, -20, 9, 13, cor[i % cor.length]).setDepth(9650); this.tweens.add({ targets: r, y: this.scale.height + 30, angle: Math.random() * 720 - 360, x: '+=' + (Math.random() * 120 - 60), duration: 1800 + Math.random() * 1400, delay: Math.random() * 500, onComplete: () => r.destroy() }); }
  }
  medalha(onRestart) {
    const m = this.add.container(this.scale.width / 2, this.scale.height / 2).setDepth(9900);
    const bg = this.add.rectangle(0, 0, 340, 200, 0x11314a, 0.96).setStrokeStyle(4, 0xffd76a);
    const coin = this.add.image(0, -44, 'cogHUD').setScale(6);
    const t1 = this.add.text(0, 34, 'CAÇADOR(A) DE TESOURO', { fontFamily: 'system-ui', fontSize: '19px', color: '#ffd76a', fontStyle: 'bold' }).setOrigin(0.5);
    const t2 = this.add.text(0, 64, 'Toque para brincar de novo', { fontFamily: 'system-ui', fontSize: '13px', color: '#cfe' }).setOrigin(0.5);
    m.add([bg, coin, t1, t2]); m.setScale(0.2); this.med = m;
    this.tweens.add({ targets: m, scale: 1, duration: 500, ease: 'Back.easeOut' });
    this.tweens.add({ targets: coin, angle: { from: -8, to: 8 }, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    this.time.delayedCall(900, () => this.input.once('pointerdown', () => { m.destroy(); this.med = null; if (onRestart) onRestart(); }));
  }
}

// ============================== MUNDO ==============================
class Mundo extends Phaser.Scene {
  constructor() { super({ key: 'Mundo' }); }
  preload() {
    ['grass', 'char', 'tree', 'pine', 'bush', 'ourobar', 'pratabar', 'guia'].forEach(k => this.load.image(k, 'assets/' + k + '.png'));
  }
  create() {
    this.total = 0; this.ativo = false; this._venceu = false; this.dlgAberto = false;
    this.rodada = 0; this.moedas = []; this.coletadas = 0; this.alvo = 0; this.destino = null; this.face = 1;
    if (!this.scene.isActive('UI')) this.scene.launch('UI'); this.ui = this.scene.get('UI');

    this.add.tileSprite(0, 0, WW, WH, 'grass').setOrigin(0).setDepth(-100);

    this.blocos = this.physics.add.staticGroup();
    const solido = (x, y, w, h) => { const z = this.add.zone(x, y, w, h); this.physics.add.existing(z, true); this.blocos.add(z); };

    const arv = [['tree', 160, 210], ['pine', 500, 150], ['tree', 1040, 240], ['pine', 1120, 520], ['tree', 110, 560], ['tree', 700, 560], ['pine', 320, 760], ['tree', 1080, 800], ['tree', 640, 860]];
    arv.forEach(([t, x, y], i) => { this.add.ellipse(x, y, 46, 14, 0x000000, 0.2).setDepth(y - 1); const a = this.add.image(x, y, t).setOrigin(0.5, 1).setScale(ST).setDepth(y); this.tweens.add({ targets: a, angle: { from: -1.8, to: 1.8 }, duration: 2000 + (i % 5) * 240, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: (i % 6) * 260 }); solido(x, y - 8, 22, 14); });
    const arb = [[280, 460], [620, 300], [900, 380], [200, 720], [520, 720], [980, 700], [420, 560]];
    arb.forEach(([x, y], i) => { this.add.ellipse(x, y, 24, 8, 0x000000, 0.18).setDepth(y - 1); const b = this.add.image(x, y, 'bush').setOrigin(0.5, 1).setScale(SB).setDepth(y); this.tweens.add({ targets: b, angle: { from: -3, to: 3 }, duration: 1500 + (i % 4) * 200, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: (i % 5) * 180 }); solido(x, y - 5, 18, 10); });

    // corpo físico + visual (vida) do herói
    this.corpo = this.physics.add.image(WW / 2, WH / 2, 'char').setVisible(false); this.corpo.body.setSize(12, 6); this.corpo.setCollideWorldBounds(true);
    this.physics.add.collider(this.corpo, this.blocos);
    this.sombra = this.add.ellipse(WW / 2, WH / 2, 32, 12, 0x000000, 0.25);
    this.vis = this.add.image(WW / 2, WH / 2, 'char').setOrigin(0.5, 1);

    // GUIA (personagem que fala) + sua sombra
    this.gsom = this.add.ellipse(700, 440, 26, 10, 0x000000, 0.22);
    this.guia = this.add.image(700, 440, 'guia').setOrigin(0.5, 1); this._gy = 440;

    // BALÃO branco (desenhado por código, sem emoji)
    this.balG = this.add.graphics().setDepth(9498).setVisible(false);
    this.balT = this.add.text(0, 0, '', { fontFamily: 'system-ui', fontSize: '13px', color: '#16324a', lineSpacing: 2, wordWrap: { width: 155 } }).setOrigin(0, 0).setDepth(9499).setVisible(false);

    this.physics.world.setBounds(0, 0, WW, WH);
    this.cameras.main.setBounds(0, 0, WW, WH).setZoom(ZOOM).startFollow(this.corpo, true, 0.12, 0.12);
    this.cursors = this.input.keyboard.createCursorKeys(); this.wasd = this.input.keyboard.addKeys('W,A,S,D');
    this.input.keyboard.clearCaptures(); this.input.keyboard.disableGlobalCapture();
    const liga = () => { initSom(); this._on2 = true; const dc = document.getElementById('somdica'); if (dc) dc.style.display = 'none'; };
    this.input.on('pointerdown', (p) => { liga(); if (!this.ativo || this._venceu) return; const wp = this.cameras.main.getWorldPoint(p.x, p.y); this.destino = { x: Phaser.Math.Clamp(wp.x, 8, WW - 8), y: Phaser.Math.Clamp(wp.y, 8, WH - 8) }; this._dt = this.time.now; });
    this.input.keyboard.on('keydown', liga);
    this.time.addEvent({ delay: 5000, loop: true, callback: rajada });

    window.__ready = true; window.__scene = this;
    window.__fs = () => { if (this.scale.isFullscreen) this.scale.stopFullscreen(); else this.scale.startFullscreen(); };
    window.__mover = (d) => { this._forc = d; }; window.__parar = () => { this._forc = null; };
    window.__iniciarAtividade = () => this.iniciar();
    if (window.__nome) this.time.delayedCall(60, () => this.iniciar());
  }

  // ---- BALÃO automático + NARRAÇÃO (voz Antonio) sincronizada; não trava ----
  // pgs = ['texto',...]; audios = [[id,...],...] (voz de cada página; opcional)
  dialogo(pgs, onDone, audios) { this.dlgAberto = true; this._pgs = pgs.slice(); this._audios = audios || null; this._pg = 0; this._pgTok = (this._pgTok || 0) + 1; this._onDone = onDone || null; this.balG.setVisible(true); this.balT.setVisible(true); this.mostra(); }
  mostra() {
    const tok = ++this._pgTok;
    const full = this._pgs[this._pg]; this._full = full; this._n = 0; this.balT.setText('');
    if (this._typer) this._typer.remove(); if (this._auto) { this._auto.remove(); this._auto = null; } if (this._fb) { this._fb.remove(); this._fb = null; }
    // efeito de digitação (visual)
    this._typer = this.time.addEvent({ delay: 26, loop: true, callback: () => { this._n++; this.balT.setText(full.slice(0, this._n)); if (this._n % 2 === 0) tom(430, 0.03, 'square', 0.02); if (this._n >= full.length) this._typer.remove(); } });
    const adv = () => { if (tok !== this._pgTok) return; this.avanca(); };
    const ids = this._audios ? this._audios[this._pg] : null;
    if (ids && ids.length) {
      // voz manda no ritmo: avança quando a narração termina; fallback longo cobre o caso de a voz ser cortada (ex.: criança já foi juntando)
      Voz.stop(); Voz.cadeia(ids, () => { if (tok !== this._pgTok) return; this._auto = this.time.delayedCall(320, adv); });
      this._fb = this.time.delayedCall(Math.max(3500, 350 + full.length * 100), adv);
    } else {
      this._auto = this.time.delayedCall(800 + full.length * 26, adv);
    }
  }
  avanca() { if (this._auto) { this._auto.remove(); this._auto = null; } if (this._fb) { this._fb.remove(); this._fb = null; } this._pg++; if (this._pg < this._pgs.length) this.mostra(); else { this.balG.setVisible(false); this.balT.setVisible(false); this.dlgAberto = false; Voz.stop(); const cb = this._onDone; this._onDone = null; if (cb) cb(); } }
  desenhaBalao() {
    if (!this.dlgAberto) return; const pad = 9, tw = Math.max(28, this.balT.width), th = Math.max(14, this.balT.height);
    const w = tw + pad * 2, h = th + pad * 2, cx = this.guia.x, base = this.guia.y - this.guia.displayHeight - 2, rx = cx - w / 2, ry = base - h;
    this.balG.clear(); this.balG.fillStyle(0xffffff, 0.98); this.balG.lineStyle(2, 0xffb23e, 1);
    this.balG.fillRoundedRect(rx, ry, w, h, 9); this.balG.strokeRoundedRect(rx, ry, w, h, 9);
    this.balG.fillStyle(0xffffff, 0.98); this.balG.fillTriangle(cx - 7, ry + h - 1, cx + 7, ry + h - 1, cx, base + 6);
    this.balT.setPosition(rx + pad, ry + pad);
  }

  iniciar() {
    if (this._ini) return; this._ini = true; initSom(); this._on2 = true;
    const dc = document.getElementById('somdica'); if (dc) dc.style.display = 'none';
    this.nome = (window.__nome || 'amiguinho'); this._idNome = idNome(this.nome); this.ativo = true; this.iniciarRodada();
  }
  iniciarRodada() {
    const r = this.rodada, [a, b] = RODADAS[r]; this.aR = a; this.bR = b; this.alvo = a + b; this.coletadas = 0;
    this.moedas.forEach(m => { if (m._sh) m._sh.destroy(); m.destroy(); }); this.moedas = [];
    this.poe('ourobar', a, CA); this.poe('pratabar', b, CB);
    const N = this.nome.charAt(0).toUpperCase() + this.nome.slice(1);
    const pede = 'Junte as ' + a + ' barras de ouro com as ' + b + ' de prata. Quantas dao ao todo?';
    if (r === 0) {
      this.dialogo(
        ['Ola, ' + N + '! Eu sou o Tomas.', 'Achei um tesouro espalhado em dois montes! Ande por cima das barrinhas pra pegar.', pede],
        null, [[this._idNome, 'k_abre1'], ['k_abre2'], ['k_pede0']]);
    } else {
      this.dialogo([pede], null, [['k_pede' + r]]);
    }
  }
  poe(tipo, n, centro) {
    const PR = 3, ESP = 76;   // BEM espaçado (criança anda até cada um pra contar)
    for (let i = 0; i < n; i++) {
      const col = i % PR, lin = Math.floor(i / PR);
      const x = centro.x + (col - (PR - 1) / 2) * ESP + Phaser.Math.Between(-4, 4);
      const y = centro.y + (lin - Math.floor((n - 1) / PR) / 2) * ESP + Phaser.Math.Between(-4, 4);
      this.add.ellipse(x, y, 16, 6, 0x000000, 0.2).setDepth(y - 1);
      const m = this.add.image(x, y, tipo).setOrigin(0.5, 1).setScale(SM).setDepth(y);
      this.tweens.add({ targets: m, y: y - 4, duration: 650, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: i * 60 });
      m._coletada = false; this.moedas.push(m);
    }
  }
  coletar(m) {
    if (m._coletada) return; m._coletada = true; this.coletadas++; this.total++;
    somMoeda(); this.ui.numerao(this.coletadas); this.ui.setHUD('Barras: ' + this.total);
    // NARRA a contagem: a criança ouve o número (Antonio) enquanto ele aparece grandão
    if (this.coletadas <= 20) { Voz.stop(); Voz.um('kn' + this.coletadas); }
    this.faisca(m.x, m.y - 10);
    this.tweens.add({ targets: m, y: m.y - 46, scale: 0.1, alpha: 0, duration: 360, ease: 'Back.easeIn', onComplete: () => m.destroy() });
    if (this.coletadas >= this.alvo) this.rodadaDone();
  }
  faisca(x, y) { for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; const s = this.add.rectangle(x, y, 4, 4, 0xfff2a0).setDepth(9000).setAngle(45); this.tweens.add({ targets: s, x: x + Math.cos(a) * 30, y: y + Math.sin(a) * 26, alpha: 0, scale: 0.2, duration: 520, onComplete: () => s.destroy() }); } }
  rodadaDone() {
    somCerto(); const a = this.aR, b = this.bR, s = a + b, rf = this.rodada; this.rodada++;
    if (this.rodada >= RODADAS.length) this.dialogo([a + ' e ' + b + ', juntando, dao ' + s + '!'], () => this.vencer(), [['k_soma' + rf]]);
    else this.dialogo([a + ' e ' + b + ', juntando, dao ' + s + '!', 'Vamos achar mais tesouro!'], () => this.iniciarRodada(), [['k_soma' + rf], ['k_mais']]);
  }
  vencer() {
    if (this._venceu) return; this._venceu = true; this.ativo = false; somFanfarra(); this.ui.confete();
    this.time.delayedCall(600, () => this.dialogo(
      ['Voce conseguiu! Que tesouro!', 'Toda vez a gente juntou dois montes. Juntar dois grupos e o mesmo que SOMAR!', 'O que voce mais gostou hoje?'],
      () => this.ui.medalha(() => { this._ini = false; this.scene.restart(); }),
      [['k_venceu'], ['k_licao'], ['k_pergunta']]));
  }

  vida(img, bx, by, andando, time, face, base) {
    let sx, sy, yb;
    if (andando) { const p = time * 0.016; yb = -Math.abs(Math.sin(p)) * 7; const sq = Math.abs(Math.cos(p)); sy = base * (1 - sq * 0.12); sx = base * (1 + sq * 0.10); }
    else { const b = Math.sin(time * 0.004) * 0.03; sy = base * (1 + b); sx = base * (1 - b * 0.6); yb = 0; }
    img.setPosition(bx, by + yb).setScale(sx * face, sy).setDepth(by);
    return by;
  }
  update(time) {
    let vx = 0, vy = 0, kx = 0, ky = 0;
    const livre = this.ativo && !this._venceu;
    if (livre) {
      if (this.cursors.left.isDown || this.wasd.A.isDown || this._forc === 'left') kx = -1; else if (this.cursors.right.isDown || this.wasd.D.isDown || this._forc === 'right') kx = 1;
      if (this.cursors.up.isDown || this.wasd.W.isDown || this._forc === 'up') ky = -1; else if (this.cursors.down.isDown || this.wasd.S.isDown || this._forc === 'down') ky = 1;
      if (kx || ky) { this.destino = null; vx = kx; vy = ky; }
      else if (this.destino) { const dx = this.destino.x - this.corpo.x, dy = this.destino.y - this.corpo.y, d = Math.hypot(dx, dy); if (d < 8 || time - this._dt > 4000) this.destino = null; else { vx = dx / d; vy = dy / d; } }
    } else this.destino = null;
    this.corpo.body.setVelocity(vx * 155, vy * 155);
    const andando = vx !== 0 || vy !== 0; if (vx < 0) this.face = -1; else if (vx > 0) this.face = 1;
    if (andando && time - (this._pt || 0) > 300) { somPasso(); this._pt = time; }

    const bx = this.corpo.x, by = this.corpo.y + 8;
    this.vida(this.vis, bx, by, andando, time, this.face, S);
    this.sombra.setPosition(bx, by + 1).setDepth(by - 1).setScale(andando ? 0.9 : 1, 1);

    // guia acompanha
    const tx = this.corpo.x + 60, ty = this.corpo.y + 6;
    this._gy = Phaser.Math.Linear(this._gy, ty, 0.08);
    const gx = Phaser.Math.Linear(this.guia.x, tx, 0.08);
    this.vida(this.guia, gx, this._gy, false, time * 0.7, 1, SG);
    this.gsom.setPosition(gx, this._gy + 1).setDepth(this._gy - 1);
    if (this.dlgAberto) this.desenhaBalao();

    // JUNTAR: recolhe moeda ao passar por cima
    if (this.ativo && !this._venceu) for (const m of this.moedas) { if (!m._coletada && Math.abs(this.corpo.x - m.x) < 28 && Math.abs(this.corpo.y - m.y) < 30) this.coletar(m); }
  }
}

new Phaser.Game({
  type: Phaser.CANVAS, pixelArt: true, roundPixels: true, backgroundColor: '#4a7a3a',
  physics: { default: 'arcade', arcade: {} },
  scale: { mode: Phaser.Scale.RESIZE, parent: 'jogo', width: '100%', height: '100%' },
  scene: [Mundo, UI]
});
