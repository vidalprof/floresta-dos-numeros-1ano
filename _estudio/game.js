'use strict';
// ============================================================================
// EduVerse — CENA DE REFERÊNCIA do "2D INCRÍVEL" (Phaser, motor oficial).
// Mostra o TETO: mundo pintado + Byte VIVO (anda/respira/comemora, troca de pose)
// + luz do sol respirando + pólen no ar + a CONTAGEM QUE ACENDE em sincronia com a
// voz do Antonio. Vitrine + contagem gentil (não é prova). ZERO emoji.
// ============================================================================
const DW = 1024, DH = 1024;   // cena quadrada (bg 1024) — Scale.FIT

// ---------- VOZ (Antonio, mp3) ----------
const Voz = (function () {
  const base = 'audio/'; let atual = null;
  function stop() { if (atual) { try { atual.pause(); } catch (e) {} atual = null; } }
  function um(id, cb) { if (!id) { if (cb) cb(); return; } let a; try { a = new Audio(base + id + '.mp3'); a.volume = 1; } catch (e) { if (cb) cb(); return; } atual = a; let d = false; const f = () => { if (d) return; d = true; if (atual === a) atual = null; if (cb) cb(); }; a.onended = f; a.onerror = f; a.play().catch(f); }
  return { stop, um };
})();

// ---------- SOM ambiente (WebAudio) ----------
let AC = null, MST = null, _wg = null, _on = false;
function initSom() {
  if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)(); MST = AC.createGain(); MST.gain.value = 0.5; MST.connect(AC.destination);
    const buf = AC.createBuffer(1, AC.sampleRate * 2, AC.sampleRate), d = buf.getChannelData(0); let last = 0;
    for (let i = 0; i < d.length; i++) { const w = Math.random() * 2 - 1; last = (last + 0.02 * w) / 1.02; d[i] = last * 3; }
    const src = AC.createBufferSource(); src.buffer = buf; src.loop = true; const lp = AC.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 460;
    _wg = AC.createGain(); _wg.gain.value = 0.03; src.connect(lp); lp.connect(_wg); _wg.connect(MST); src.start(); _on = true;
  } catch (e) {}
}
function tom(f, dur, tp, v, sl) { if (!AC || !_on) return; const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain(); o.type = tp || 'sine'; o.frequency.setValueAtTime(f, t); if (sl) o.frequency.exponentialRampToValueAtTime(sl, t + dur); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v || 0.08, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.connect(g); g.connect(MST); o.start(t); o.stop(t + dur + 0.02); }
function sColeta() { tom(880, 0.12, 'triangle', 0.09, 1500); }
function sFest() { [523, 659, 784, 1046, 784, 1046, 1318].forEach((f, i) => setTimeout(() => tom(f, 0.3, 'triangle', 0.1), i * 130)); }

const POSES = { idle: 'byte_idle', anda: 'byte_anda', feliz: 'byte_feliz', fala: 'byte_fala', pensa: 'byte_pensa' };

class Cena extends Phaser.Scene {
  constructor() { super({ key: 'Cena' }); }
  preload() {
    this.load.image('bg', 'img/bg.jpg'); this.load.image('maca', 'img/maca.png');
    Object.values(POSES).forEach(k => this.load.image(k, 'img/' + k + '.png'));
  }
  create() {
    this.ativo = false; this.destino = null; this.face = 1; this.total = 0; this._venceu = false;
    // fundo pintado cobrindo a cena
    this.add.image(DW / 2, DH / 2, 'bg').setDisplaySize(DW, DH).setDepth(-100);

    // luz do sol RESPIRANDO (aditiva) — canto superior
    const g = this.add.graphics(); g.fillStyle(0xffef9e, 1); g.fillCircle(0, 0, 300);
    g.generateTexture('glow', 600, 600); g.destroy();
    this.sol = this.add.image(820, 150, 'glow').setBlendMode(Phaser.BlendModes.ADD).setAlpha(0.22).setScale(1.2).setDepth(-50);
    this.tweens.add({ targets: this.sol, alpha: 0.34, scale: 1.4, duration: 2600, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    // pólen/luz no ar (partículas)
    const pg = this.add.graphics(); pg.fillStyle(0xffffff, 1); pg.fillCircle(4, 4, 4); pg.generateTexture('poeira', 8, 8); pg.destroy();
    this.add.particles(0, 0, 'poeira', {
      x: { min: 0, max: DW }, y: { min: 0, max: DH }, quantity: 1, frequency: 260, lifespan: 6000,
      scale: { start: 0.5, end: 0 }, alpha: { start: 0.7, end: 0 }, tint: 0xfff2b0,
      speedY: { min: -14, max: -4 }, speedX: { min: -8, max: 8 }, blendMode: 'ADD'
    }).setDepth(50);

    // maçãs espalhadas na campina (longe das árvores do fundo: x 300..724)
    this.macas = [];
    const pos = [[400, 770], [560, 810], [660, 730], [470, 860], [610, 880]];
    pos.forEach(([x, y], i) => {
      const sh = this.add.ellipse(x, y, 60, 20, 0x123a12, 0.18).setDepth(y - 2);
      const glow = this.add.image(x, y - 26, 'glow').setBlendMode(Phaser.BlendModes.ADD).setScale(0.16).setAlpha(0).setDepth(y - 1).setTint(0xfff0a0);
      const m = this.add.image(x, y, 'maca').setOrigin(0.5, 1).setDisplaySize(56, 68).setDepth(y);
      this.tweens.add({ targets: m, y: y - 6, duration: 640, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: i * 90 });
      m._glow = glow; m._sh = sh; m._got = false; this.macas.push(m);
    });

    // BYTE vivo
    this.sombra = this.add.ellipse(512, 690, 90, 30, 0x000000, 0.22);
    this.vis = this.add.image(512, 690, POSES.idle).setOrigin(0.5, 1);
    this.bx = 512; this.by = 690; this._pose = 'idle'; this.setPose('idle');

    // entrada
    this.input.on('pointerdown', (p) => {
      this.liga();
      if (!this.ativo || this._venceu) return;
      const wp = { x: p.worldX, y: p.worldY };
      this.destino = { x: Phaser.Math.Clamp(wp.x, 120, DW - 120), y: Phaser.Math.Clamp(wp.y, 480, DH - 60) }; this._dt = this.time.now;
    });
    this.scale.on('resize', () => {});

    window.__ready = true; window.__cena = this;
    this.time.delayedCall(400, () => this.iniciar());
  }
  liga() { if (this._lig) return; this._lig = true; initSom(); const d = document.getElementById('dica'); if (d) d.style.display = 'none'; }
  setPose(nome) {
    const key = POSES[nome]; this.vis.setTexture(key);
    const tx = this.textures.get(key).getSourceImage(); this._baseH = 185; this._baseScale = this._baseH / tx.height; this._pose = nome;
  }
  iniciar() { this.liga(); this.ativo = true; Voz.um('t_ola'); }
  numerao(n) {
    const nd = document.getElementById('numerao'); nd.textContent = n;
    nd.style.transition = 'none'; nd.style.opacity = '1'; nd.style.transform = 'translate(-50%,-50%) scale(.4)';
    requestAnimationFrame(() => { nd.style.transition = 'transform .18s cubic-bezier(.2,1.7,.4,1)'; nd.style.transform = 'translate(-50%,-50%) scale(1.1)'; });
    clearTimeout(this._nt); this._nt = setTimeout(() => { nd.style.transition = 'opacity .4s,transform .4s'; nd.style.opacity = '0'; nd.style.transform = 'translate(-50%,-70%) scale(1)'; }, 500);
  }
  faisca(x, y) { for (let i = 0; i < 7; i++) { const a = (i / 7) * Math.PI * 2, s = this.add.rectangle(x, y, 6, 6, 0xfff2a0).setDepth(9000).setAngle(45); this.tweens.add({ targets: s, x: x + Math.cos(a) * 44, y: y + Math.sin(a) * 40, alpha: 0, scale: 0.2, duration: 560, onComplete: () => s.destroy() }); } }
  coletar(m) {
    if (m._got) return; m._got = true; this.total++;
    sColeta(); Voz.stop(); Voz.um('kn' + this.total); this.numerao(this.total); this.faisca(m.x, m.y - 26);
    // A CONTAGEM QUE ACENDE: o item brilha (aditivo) no momento do número
    const gl = m._glow; gl.setAlpha(0.9); this.tweens.add({ targets: gl, alpha: 0, scale: 0.42, duration: 620, ease: 'Cubic.out', onComplete: () => gl.destroy() });
    if (m._sh) this.tweens.add({ targets: m._sh, alpha: 0, scaleX: 0.4, duration: 360, onComplete: () => m._sh.destroy() });
    this.tweens.add({ targets: m, y: m.y - 60, scale: 0.1, alpha: 0, duration: 400, ease: 'Back.easeIn', onComplete: () => m.destroy() });
    if (this.total >= this.macas.length) this.vencer();
  }
  vencer() {
    if (this._venceu) return; this._venceu = true; this.destino = null;
    this.time.delayedCall(300, () => { this.setPose('feliz'); sFest(); this.confete(); Voz.um('t_festa'); });
  }
  confete() {
    const cor = [0xffd45a, 0xff5a5a, 0x5ad1ff, 0x8aff7a, 0xff8ad1];
    for (let i = 0; i < 70; i++) { const r = this.add.rectangle(Math.random() * DW, -20, 12, 16, cor[i % 5]).setDepth(9500); this.tweens.add({ targets: r, y: DH + 30, angle: Math.random() * 720 - 360, x: '+=' + (Math.random() * 160 - 80), duration: 2200 + Math.random() * 1600, delay: Math.random() * 500, onComplete: () => r.destroy() }); }
  }
  update(time) {
    let vx = 0, vy = 0;
    if (this.ativo && !this._venceu && this.destino) {
      const dx = this.destino.x - this.bx, dy = this.destino.y - this.by, d = Math.hypot(dx, dy);
      if (d < 6 || time - this._dt > 4000) this.destino = null; else { vx = dx / d; vy = dy / d; }
    }
    const andando = vx !== 0 || vy !== 0;
    if (vx < -0.02) this.face = -1; else if (vx > 0.02) this.face = 1;
    if (andando) { this.bx += vx * 3.0; this.by += vy * 3.0; }

    // troca de pose contextual (só quando não venceu)
    if (!this._venceu) { const alvo = andando ? 'anda' : 'idle'; if (this._pose !== alvo) this.setPose(alvo); }

    // motor de vida (respira parado / pula andando) + flip
    let sx, sy, yb;
    if (andando) { const p = time * 0.016; yb = -Math.abs(Math.sin(p)) * 8; const sq = Math.abs(Math.cos(p)); sy = this._baseScale * (1 - sq * 0.10); sx = this._baseScale * (1 + sq * 0.08); }
    else { const b = Math.sin(time * 0.0038) * 0.03; sy = this._baseScale * (1 + b); sx = this._baseScale * (1 - b * 0.6); yb = 0; }
    this.vis.setPosition(this.bx, this.by + yb).setScale(sx * this.face, sy).setDepth(this.by);
    this.sombra.setPosition(this.bx, this.by + 2).setDepth(this.by - 1).setScale(andando ? 0.9 : 1, 1);

    // coletar ao passar por cima
    if (this.ativo && !this._venceu) for (const m of this.macas) if (!m._got && Math.abs(this.bx - m.x) < 46 && Math.abs(this.by - m.y) < 52) this.coletar(m);
  }
}

new Phaser.Game({
  type: Phaser.AUTO, backgroundColor: '#bfe3f2', roundPixels: true,
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, parent: 'jogo', width: DW, height: DH },
  scene: [Cena]
});
