# Pesquisa — MASCOTE VIVO + MAPA VIVO em HTML leve (2026-07)

> Rodada de animação (pedido do Marcos: mascote e mapa muito mais vivos). Alvo: 1 HTML, PC FRACO,
> offline, 6-12, só transform/opacity, prefers-reduced-motion, voz MP3 (Antônio), arte IA.
> Força: [FORTE]/[CONSENSO]/[OPINIÃO]. ⚠️ Os trechos de código vêm em ES6 — reescrever em var/function
> p/ o manual premium §14.

## FRENTE 1 — MASCOTE VIVO
**O segredo do "vivo mesmo parado" = soma de MICRO-animações lentas e DESSINCRONIZADAS** (períodos
quebrados 3.1s/4.7s/0.9s que nunca "batem juntos"). Se todas têm a mesma duração, vira robô. [CONSENSO]

- **Respiração** (maior retorno): ciclo 3.5-4.5s, deslocamento ~1-2%, `transform-origin:50% 100%`, e
  **volume constante** (quando scaleX cresce, scaleY encolhe — squash&stretch homeopático). [FORTE]
- **Piscar**: troca de olhos por opacity, intervalo ALEATÓRIO 4-8s, duração ~140ms; piscada dupla
  ocasional (10-20%) parece muito mais natural.
- **Bob + gingado**: translateY 3-5px (2.5-3.5s) + rotate ±1.5° (3-4s), defasados (bob no wrapper,
  gingado numa camada interna).
- **Fidgets**: a cada 6-12s uma reaçãozinha (orelha treme, olha pro lado) por 0.5-1s — separa "vivo" de "loop".
- Parâmetros de partida: respira 4.2s / bob 3s / gingado 3.5s / piscar 4-8s / fidget 6-12s — TODOS
  diferentes e não-múltiplos.

**LIP-SYNC (com o MP3 do Antônio):**
- **Base = por AMPLITUDE (RMS)** [FORTE]: `AnalyserNode` (`getByteTimeDomainData`) → RMS → `scaleY` da
  boca (ganho ~3, suavização `boca += (alvo-boca)*0.35`, corte de silêncio se rms<0.02). Barato, robusto.
- **Capricho = VISEMAS PRÉ-COMPUTADOS no build** [OPINIÃO, melhor aqui]: como a narração é FIXA, gerar
  no Actions uma trilha `[{t,v}]` e em runtime só trocar a pose de boca por `currentTime` — **zero DSP no
  PC fraco, o mais fiel**. (Visema por bandas em tempo real = wawa-lipsync MIT, aproxima o "clima".)
- **⚠️ 2 armadilhas [FORTE]:** (1) **CORS** — MP3 de outra origem sem header faz o Analyser ler ZEROS
  (boca nunca abre); usar MP3 na MESMA origem ou embutido `data:`/blob. (2) **Autoplay** — `AudioContext`
  nasce suspended; `ac.resume()` no 1º gesto (o botão "Ouvir").
- **Reações por evento** (feliz/pensando/comemora/incentiva): troca de pose + pop com overshoot
  `cubic-bezier(.34,1.56,.64,1)`. Já é o padrão `MASCOTE_POSES={}` do projeto.

**RIG — recomendação [OPINIÃO forte]: cutout/puppet 2D (transform) + spritesheet só p/ boca (visemas) e
trocas de expressão.** Bate 100% na regra transform/opacity, SEM biblioteca externa (crucial offline/1
HTML), idle contínuo quase de graça. A IA gera 1 personagem → recorta em camadas (cabeça, 2 olhos, boca,
2 braços) OU spritesheet coeso (seed fixa + estilo travado + img2img strength ~0.55 + ControlNet, paleta
forçada no pós). **Rive/Lottie pesam mais do que ajudam** aqui (só p/ cena vetorial complexa).

## FRENTE 2 — MAPA VIVO
- **Parallax**: camadas céu→montanha→meio→frente, `translate3d` proporcional ao `data-depth` (fundo anda
  menos). **3-4 camadas bastam**; imagens já no tamanho de tela (NUNCA reescalar gigante). [FORTE]
- **Partículas por bioma** (vaga-lumes/folhas/neve/poeira de estrela/bolhas): **30-50 seguro em qualquer
  PC; ~20 no fraco; 150+ só em Canvas**. Só transform/opacity, delays escalonados; ou **box-shadow
  múltiplo num único `<div>`** (dezenas de pontos, 1 nó no DOM). [FORTE]
- **Água/céu shimmer**: gradiente claro varrendo com `translateX`+`skewX`; nuvens à deriva (translateX
  lento 30-90s, opacity baixa, 2-3 camadas).
- **Mascote CAMINHANDO**: `offset-path: path('...')` (= o `d` da trilha) + `offset-distance:0→100%` +
  `offset-rotate:auto`; por cima, bob + squash no passo (+ walk cycle `steps()`). **Fallback** p/
  navegador velho sem offset-path: posicionar por JS com translate em pontos pré-amostrados da curva (lerp).
- **Câmera lerp INDEPENDENTE de frame-rate**: `camX += (alvoX-camX)*(1-Math.exp(-6*dt))` — persegue com
  atraso natural; alimenta o parallax. (Sem o `exp`, 144Hz vira câmera rápida.) [FORTE]
- **Nós/ilhas**: flutuar + farol pulsante com **delays diferentes por nó** (o mapa "respira"); o **próximo
  nó pulsa mais rápido**/pop ao ser revelado.

## FRENTE 3 — PERFORMANCE + ACESSIBILIDADE
- **Teto DOM/CSS**: 60fps estável até ~100 objetos animados; degrada ~500; acima disso Canvas/WebGL
  [FORTE, benchmark 2026]. **Orçamento de escola: ≤40-60 elementos animados na tela.**
- **Orçamento de frame**: 60fps=16.7ms; **30fps estável e suave > 60fps que engasga** — em Chromebook/
  Intel HD, mirar 30fps e degradar qualidade sozinho. Callback JS <~10ms.
- **Só transform/opacity** (compositor/GPU, sem layout/paint). Nunca top/left/width/margin/box-shadow
  geométrico/filter/blur/backdrop-filter.
- **UM loop rAF só** p/ tudo em JS (câmera, lip-sync, fidgets), com delta-time; idle e partículas ficam em
  CSS `@keyframes` (rodam no compositor, fora do loop).
- **Pausar fora de vista**: `IntersectionObserver` → `animation-play-state:paused`; **aba oculta**
  (`visibilitychange`/`document.hidden`) → cancelar rAF + pausar áudio.
- **`will-change` com parcimônia**: só no elemento que vai animar, e remover depois (espalhar = mais
  vídeo-memória = pior no PC fraco).
- **`prefers-reduced-motion`** (CSS **e** JS): desligar movimento contínuo/decorativo (parallax,
  partículas, flutuação, walk); preservar essencial trocando por opacity/troca de pose SEM deslocamento.
- **Medir FPS** e **degradar sozinho** (qualidade adaptativa): se cair <~50fps por alguns segundos, cortar
  partículas (50→20), desligar shimmer, reduzir camadas. Testar no Chromium headless com CPU throttled.

## RECEITA DE MASCOTE VIVO (checklist)
1. Arte IA: 1 personagem + poses (seed fixa, paleta travada); recortar em camadas OU spritesheet coeso.
2. `transform-origin:50% 100%`.
3. Idle empilhado dessincronizado: respira 4.2s + bob 3s + gingado 3.5s + piscar 4-8s + fidget 6-12s.
4. Squash&stretch de volume constante em toda reação.
5. Lip-sync base por RMS; capricho = visemas pré-computados no build.
6. Garantir CORS (áudio mesma origem/`data:`) e `ac.resume()` no 1º gesto.
7. Reações por evento com pop back-out.
8. reduced-motion: idle estático; lip-sync/reação viram troca de pose.

## RECEITA DE MAPA VIVO (checklist)
1. 3-4 camadas de parallax por `data-depth`, imagens no tamanho de tela.
2. 1 camada de partículas do bioma (30-50 desktop / ~20 fraco), transform/opacity, delays escalonados.
3. Água/céu: 1 shimmer + 2-3 nuvens à deriva.
4. Trilha: `offset-path`+`offset-distance`+`offset-rotate:auto`; fallback JS por pontos.
5. Vida do andar: bob + squash (+ walk cycle steps()).
6. Câmera lerp independente de frame-rate alimentando o parallax.
7. Nós: flutuar + farol com delays diferentes; próximo pulsa mais rápido/pop ao revelar.
8. Tudo num loop rAF pausável.

## FONTES (principais)
Squash&stretch https://www.joshwcomeau.com/animation/squash-and-stretch/ · idle/respiração
https://mocaponline.com/blogs/mocap-news/idle-animation-game-dev-guide · AnalyserNode
https://developer.mozilla.org/en-US/docs/Web/API/AnalyserNode · lip-sync por volume
https://docs.live2d.com/en/cubism-sdk-tutorials/native-lipsync-from-wav-web/ · wawa-lipsync (MIT)
https://github.com/wass08/wawa-lipsync · CORS MediaElementSource https://bugzilla.mozilla.org/show_bug.cgi?id=937718
· sprite steps() https://leanrada.com/notes/css-sprite-sheets/ · Rive×Lottie
https://www.callstack.com/blog/lottie-vs-rive-optimizing-mobile-app-animation · parallax perf
https://keithclark.co.uk/articles/pure-css-parallax-websites/ · partículas/contagens
https://www.studiolimb.com/guides/snowfall-effect-css-guide.html · box-shadow partículas
https://css-tricks.com/almanac/properties/b/box-shadow/ · shimmer https://www.codeguage.com/blog/shimmer-effect-html-css
· offset-path https://css-tricks.com/almanac/properties/o/offset-path/ · câmera lerp https://gamedevmath.com/lerp/
· benchmark 100/500/5000 https://pmc.ncbi.nlm.nih.gov/articles/PMC12843483/ · GPU/compositor
https://developer.chrome.com/blog/hardware-accelerated-animations · IntersectionObserver pausa
https://css-tricks.com/how-to-play-and-pause-css-animations-with-css-custom-properties/ · Page Visibility
https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API · will-change
https://blog.logrocket.com/when-how-use-css-will-change/ · prefers-reduced-motion
https://web.dev/articles/prefers-reduced-motion
