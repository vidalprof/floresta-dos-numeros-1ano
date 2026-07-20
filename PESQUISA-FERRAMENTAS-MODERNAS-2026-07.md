# Pesquisa — FERRAMENTAS/TECNOLOGIAS modernas p/ micro-mundos em 1 HTML, PC fraco, offline (2026-07)

> Parte da rodada "reúna o pessoal". Especialista Engenheiro Sênior. Alvo: 1 HTML autossuficiente,
> PC fraco de escola, offline, licença SÓ permissiva (CC0/MIT/BSD/Apache/zlib). Tamanhos "medido" =
> baixou o tarball oficial do npm e mediu o `.min` real + gzip.
> ⚠️ RECONCILIAR com o manual premium §14 (compatibilidade): ele proíbe JS moderno (`=>`,`let`/`const`,
> crase, spread) e CSS moderno (`grid`,`gap`,`clamp()`,`var(--)`). As LIBS abaixo (Matter, WAAPI,
> Pointer Events, Web Audio) rodam nos navegadores da escola; o que precisa de decisão com o Marcos é
> quão estritas manter as regras de SINTAXE (um passo de transpile no "Nível 2" deixa escrever moderno
> e entregar JS compatível — mas CSS `grid`/`var(--)` ou funciona no navegador-alvo ou não).

## VEREDITO RÁPIDO — ADOTAR / TALVEZ / EVITAR
**ADOTAR agora (base):**
- **Pointer Events (nativo, 0KB)** — unifica toque+mouse+caneta; `pressure`/`tilt` p/ pincel;
  `setPointerCapture` p/ arrastar sem escapar. **Base de TODA interação.**
- **Web Animations API + CSS transitions (nativo, 0KB)** — o "lindo" barato via transform/opacity (GPU).
- **Web Audio API (nativo, 0KB)** — SFX e sonificação procedurais, sem asset, offline perfeito.
- **Matter.js (MIT, 25KB gzip)** — motor de FÍSICA 2D padrão. Menor e mais fácil; tem render Canvas
  embutido; `MouseConstraint` p/ arrastar; `enableSleeping` + timestep fixo p/ PC fraco.
- **Blockly (Apache-2.0, 203KB gzip)** — único maduro p/ "programe o robô". Offline: apontar `media`
  p/ assets embutidos ou `sounds:false` (senão faz request). Peso aceitável (é o núcleo da atividade).
- **Motion One (MIT, 2,3–17KB)** — springs/stagger quando a WAAPI nativa incomodar. Substitui o GSAP.
- **Canvas 2D nativo (0KB)** — pintar, partículas, muitas-imagens/poucos-objetos-lógicos.
- **SVG nativo (0KB)** — telas didáticas limpas e NÍTIDAS: frações, régua, relógio, diagrama, gráfico
  rotulado. Nítido em qualquer zoom, estilável por CSS, acessível, eventos por elemento. (Poucos
  objetos "de verdade" + texto → SVG; muitos pixels/partículas → Canvas.)
- **Howler.js (MIT, ~10KB gzip)** — só quando houver MUITOS samples base64 (unlock/sprites robustos).
- **uPlot (MIT, ~15KB gzip)** — explorables com gráfico de dados/curva, rapidíssimo, sem WebGL.
- **Konva.js (MIT, 54KB gzip)** — scene-graph em Canvas p/ arrastar/compor muitos objetos com
  camadas/undo/`toDataURL`. (Se são 3–4 objetos, DOM/SVG nativo é mais leve.)
- **vite-plugin-singlefile** — o passo que garante 1 HTML mesmo desenvolvendo em módulos/TS.

**TALVEZ (caso específico):** Interact.js (28KB — snap/dropzone/inércia/resize prontos) · Planck.js
(53KB — estabilidade Box2D em JS puro) · Tone.js (77KB — só se a atividade É música) · Two.js (48KB —
API de vetor agnóstica) · submódulos do D3 (`d3-scale`/`d3-shape` via bundler) · OffscreenCanvas+Worker
(quando o render travar a UI) · View Transitions (enhancement entre telas).

**EVITAR (com o porquê):**
- **GSAP** — virou "grátis" (2025) MAS a licença é **proprietária "no-charge", NÃO permissiva/OSI**;
  restringe redistribuição/uso concorrente/repos open-source. **Fere a regra "só CC0/MIT/BSD/Apache" e
  os repos são públicos.** Motion One (MIT)+WAAPI entregam o mesmo por menos KB e licença limpa.
- **Pixi.js v8 (219KB gzip)** — WebGL/WebGPU; overkill e arriscado em GPU de PC de escola.
- **Rapier2D (~1,1MB wasm)** e **box2d-wasm (~537KB)** — peso proibitivo p/ 1 HTML; sem ganho que a
  criança perceba vs. Matter.
- **D3 inteiro (90KB gzip)** — trocar por SVG nativo ou uPlot; no máximo submódulos.
- **anime.js v4 inteiro inline (40KB gzip)** — cresceu; ok tree-shaken via bundler, mas p/ inline
  direto WAAPI/Motion One ganham.
- **Vibration API como recurso central** — só Chrome/Android (iOS não; Firefox removeu v129+); só
  enhancement, com `if('vibrate' in navigator)`.

## STACK MÍNIMO POR TIPO DE ATIVIDADE
| Atividade | Stack (leve/offline/PC-fraco) | Peso extra (gzip) |
|---|---|---|
| **Física** (empurrar/cair/encaixar/equilibrar) | Matter.js + Pointer Events (MouseConstraint) + Web Audio; render no Canvas do Matter | ~25 KB |
| **Desenhar/pintar** | Canvas 2D nativo + Pointer Events (`pressure`) + `toDataURL`. 0 lib (Konva só p/ camadas/undo) | 0 KB (ou +54) |
| **Compor quantidade / arrastar-soltar** | Poucas peças → DOM/SVG + Pointer Events; muitas imagens → Konva; encaixe/inércia → Interact.js; + Web Audio | 0 / 54 / 28 KB |
| **Explorable com slider** | `<input range>` + CSS custom props + SVG/Canvas nativo redesenhando; uPlot só p/ dados | 0 KB (ou ~15) |
| **Programe o robô** | Blockly + palco Canvas/SVG + Web Audio; `media` embutido, `sounds:false` | ~203 KB |
| **Animação/feedback "lindo"** | WAAPI + CSS transitions; Motion One p/ springs/stagger | 0 KB (ou 2–17) |
| **Som** (qualquer) | Web Audio nativo (procedural); Howler só c/ muitos samples; Tone.js só se musical | 0 / 10 / 77 KB |

## APIs MODERNAS DA PLATAFORMA (0 KB, subutilizadas)
Pointer Events (base de tudo) · WAAPI (animar transform/opacity com playback) · Web Audio (+AudioWorklet)
· OffscreenCanvas+rAF em Worker (render sem travar a UI — só quando engasgar) · CSS custom properties
(slider→visual) · container queries · View Transitions (`if(document.startViewTransition)` + fallback) ·
`will-change` com parcimônia (gasta RAM/GPU) · Vibration (só Android, enhancement).

## PIPELINE MODERNO → 1 HTML (o "método melhor pra eu me consertar")
- **Nível 1 (atividade simples, o mais robusto p/ escola):** 1 HTML à mão + 1 vendor `.min.js` colado
  inline (Matter/Konva/Blockly) + JS vanilla + imagens/áudio base64. Sem build. Quebra menos.
- **Nível 2 (atividade complexa):** desenvolver em ES modules/TypeScript com **Vite** (HMR,
  tree-shaking) e finalizar com **`vite-plugin-singlefile`** → inlina JS+CSS num único `dist/index.html`
  (abre com duplo-clique, sem servidor). `build.assetsInlineLimit` alto → assets viram base64.
  Alternativa: `esbuild app.ts --bundle --minify --loader:.png=dataurl --loader:.mp3=dataurl` → 1 JS
  com tudo embutido; um template mínimo embrulha num `<script>`. **Um `target` de transpile baixo aqui
  poderia atender as regras de sintaxe do manual premium sem eu escrever em ES5 à mão** (decidir c/ Marcos).
- **base64 infla binário ~33%** → manter assets enxutos (PNG/WebP otimizado, áudio curto, ou SFX
  procedural via Web Audio p/ não ter asset). Pages entrega gzip (transfer ok), mas RAM/parse no PC
  fraco é o tamanho cru.

## FONTES (principais)
Matter.js https://brm.io/matter-js/ · Planck https://piqnt.com/planck.js/ · Rapier https://rapier.rs/ ·
Konva https://konvajs.org/ · Pixi https://pixijs.com/ · Two.js https://two.js.org/ · Pointer Events
https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events · caniuse https://caniuse.com/pointer ·
Interact.js https://interactjs.io/ · WAAPI https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
· Motion One https://motion.dev/ · GSAP licença https://gsap.com/community/standard-license/ ·
Web Audio https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API · Howler https://howlerjs.com/ ·
Tone.js https://tonejs.github.io/ · Blockly https://developers.google.com/blockly · uPlot
https://github.com/leeoniya/uPlot · D3 https://d3js.org/ · vite-plugin-singlefile
https://github.com/richardtallent/vite-plugin-singlefile · esbuild https://esbuild.github.io/ ·
View Transitions https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available ·
OffscreenCanvas https://caniuse.com/offscreencanvas · Vibration https://caniuse.com/vibration
