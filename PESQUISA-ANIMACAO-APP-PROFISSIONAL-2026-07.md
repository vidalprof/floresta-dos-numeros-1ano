# Pesquisa — Animação nível APP PROFISSIONAL (leve) + atividade cinematográfica (2026-07)

> Pedido do Marcos: "app profissional, espetacular, de encher os olhos" — abertura/nome fantástica em tela
> cheia sem cortar nada, comemorações lindas, mascote ANDANDO pela trilha até as paradas, tudo vivo, com
> aprendizagem de verdade. Alvo: 1 HTML, offline, PC FRACO. Força: [FORTE]/[CONSENSO]/[OPINIÃO].

## VERDADE-MÃE (Chromebook/Intel HD) [FORTE]
Barato e liso = **`transform`+`opacity`** (compõe na GPU, sem reflow/repaint) + **canvas 2D com ~80-150
partículas**. MATA o PC fraco: WebGL2 pesado (cai p/ SwiftShader = 5-10fps), **blur/box-shadow animados**,
muitas camadas promovidas, Lottie em cena complexa (60-80% CPU). Regra: tudo que a criança vê = transform/
opacity + canvas 2D leve; excesso desliga com `prefers-reduced-motion`. O "profissional" vem de **timing,
molas, som casado e encadeamento** — não de força bruta gráfica.

## STACK MESTRE (o "encher os olhos" sem quebrar 1-HTML/offline/PC-fraco)
- **Personagem:** **puppet CSS/DOM** (recorte da arte IA em partes — cabeça/olhos/boca/braços — cada junta
  gira por `transform` no `transform-origin`) p/ idle/respiração/aceno/lip-sync = **0 runtime, 0 licença,
  offline**. **+ sprite-sheet `steps()`** só p/ o walk-cycle e 1-2 reações grandes (movimento deformável).
  **Rive** (runtime **MIT**, ~200KB wasm, renderer **canvas 2D** não webgl2; variante `canvas-advanced-single`
  embute o wasm no JS) = **teto profissional (o que o Duolingo usa)**, mas exige riggar no editor → só p/ UM
  mascote-herói, depois. **Lottie** (MIT) só p/ selos/ícones simples. **Spine = PROIBIDO (licença paga)**.
- **Movimento/câmera:** **`offset-path`** (Baseline 2022; ou amostrar a curva com `getPointAtLength` p/ pausar
  nas paradas) + walk-cycle + **câmera com lerp** (`cam += (alvo-cam)*0.08` no rAF). Transições entre telas:
  **View Transitions API** (Baseline out/2025) **com fallback FLIP** (mede antes/depois, inverte o delta, anima).
- **Comemoração:** **canvas-confetti** (ISC, ~6KB, inline) + molas **CSS `linear()`** (overshoot/bounce que o
  cubic-bezier não faz; fallback `cubic-bezier(.34,1.56,.64,1)`) + **hitstop ~70ms** + **squash&stretch** +
  **screenshake COM rotação 0,05-0,3°** (translação pura parece glitch) + **count-up** dos pontos. Sequência
  Duolingo: antecipação→estouro→escalona por marco, mascote comemora, valor real no fim. ~80-150 partículas/1s.
- **Abertura/nome em TELA CHEIA sem cortar** [FORTE]: **palco com escala `contain`** — cena base fixa (ex.
  1280×720) e `scale = Math.min(innerW/1280, innerH/720)` → NUNCA corta (sobra faixa preenchida pelo fundo
  `cover`); + `100dvh` (não `vh`, que corta no mobile) + `clamp()` na tipografia + `env(safe-area-inset)` p/ o
  notch. **Fullscreen CONDICIONAL** (`requestFullscreen` com prefixo webkit + gesto; **iPhone não tem** → o
  botão só aparece se suportado e o layout tem de ficar lindo SEM fullscreen). Campo de nome grande, **pop por
  letra**, mascote-puppet reagindo, botão pulsando (mola) desabilitado até ter nome.
- **Ambiente:** 4-6 camadas de parallax (`translate3d` no rAF, **off no mobile/reduced-motion**) + luz por
  **gradiente** (nunca blur/box-shadow animados) + **Web Audio**: ambiente em **buffer-loop sem emenda**
  (`<audio loop>` tem gap), SFX curtos casados aos eventos, **ducking** do ambiente quando a narração toca,
  destrave no 1º gesto (howler.js MIT ~7KB opcional). Microinterações em todo toque (`:active{scale(.96)}`+SFX).

## CHECKLIST PRIORIZADO (maior impacto / menor custo primeiro)
1. **Molas `linear()` + squash&stretch + microinterações de toque** em tudo — muda a sensação inteira, ~0 custo.
2. **canvas-confetti nas comemorações** com a sequência Duolingo (hitstop→squash→confete→mascote→count-up→SFX).
3. **Abertura em tela cheia sem corte:** palco `contain`-scale + `100dvh`/`clamp` + fullscreen condicional +
   campo de nome animado (pop por letra).
4. **Mascote ANDANDO** com `offset-path` + walk-cycle + **câmera lerp** (o "uau" de app de verdade).
5. **Screenshake-com-rotação + hitstop** nos momentos de peso (acerto grande, chegada na parada).
6. **Áudio ambiente sem emenda + SFX casados + ducking na voz** (Web Audio/howler).
7. **Parallax 4-6 camadas + luz por gradiente** (off no mobile/reduced-motion).
8. **Transições hero** entre telas: View Transitions com fallback FLIP.
9. **(Opcional, teto):** portar 1 mascote-herói p/ **Rive** (canvas 2D, wasm inline) — só depois de 1-8.

## LICENÇAS (todas permissivas, embutíveis)
Rive MIT · canvas-confetti ISC · howler.js MIT · screenfull.js MIT · sprites/puppet = nossa arte IA. **Spine fora.**

## FONTES
Rive/Duolingo https://dev.to/uianimation/how-duolingo-uses-rive-for-their-character-animation-and-how-you-can-build-a-similar-rive-mascot-5d19
· rive-wasm (MIT) https://github.com/rive-app/rive-wasm · canvas-confetti (ISC) https://github.com/catdad/canvas-confetti
· molas linear() (Josh Comeau) https://www.joshwcomeau.com/animation/linear-timing-function/ · linear() (Chrome)
https://developer.chrome.com/docs/css-ui/css-linear-easing-function · screenshake/juice (Vlambeer)
https://www.youtube.com/watch?v=AJdEqssNZ-U · game feel web https://valdemird.com/blog/game-feel-on-the-web/
· offset-path (MDN) https://developer.mozilla.org/en-US/docs/Web/CSS/offset-path · View Transitions Baseline
https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available · dvh/svh (web.dev)
https://web.dev/blog/viewport-units · Fullscreen (caniuse) https://caniuse.com/fullscreen · parallax perf (Chrome)
https://developer.chrome.com/blog/performant-parallaxing · Web Audio best practices (MDN)
https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices · seamless loop
https://www.kevssite.com/seamless-audio-looping/ · howler.js (MIT) https://github.com/goldfire/howler.js/
· sprite steps() https://blog.logrocket.com/making-css-animations-using-a-sprite-sheet/ · GPU animation (Smashing)
https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/ · Lottie CPU/size
https://github.com/airbnb/lottie-web/issues/2139 · Spine license https://en.esotericsoftware.com/spine-runtimes-license
