# Pesquisa — ABERTURA e FINAL animados (cutscene) + ferramentas de animação (2026-07)

> Rodada de animação (pedido do Marcos: abertura/final animados que impressionam). Alvo: 1 HTML, PC
> FRACO, offline, 6-12, licença só permissiva, arte IA, animar só transform/opacity. Voz = MP3 Antônio.
> Força: [FORTE] fonte primária/consenso · [CONSENSO] · [OPINIÃO].

## O FORMATO CERTO: "MOTION COMIC" / storybook animado [FORTE]
Movimento MÍNIMO sobre arte parada — pan/zoom, parallax 2.5D, gesto sutil do personagem, legendas que
aparecem, voz e som. O oposto de quadro-a-quadro → **barato e roda em PC fraco**. Impressiona por
**DIREÇÃO** (timing, entrada do personagem, som na hora), não por mais efeito.

## REGRA FÍSICA (governa tudo) [FORTE]
Anime SÓ `transform` e `opacity` (compostos na GPU, sem Layout/Paint). NUNCA `width/height/top/left/
margin/filter/blur/box-shadow/backdrop-filter` (repaint caro, mata PC fraco).

## AS TÉCNICAS (com o "como fazer")
- **Cena em CAMADAS + PARALLAX:** 4 planos `position:absolute` (fundo/meio/frente/personagem); cada um
  com magnitude diferente de translate (fundo ~3%, meio ~7%, frente ~14%) → profundidade 2.5D. Parallax
  por mouse só no desktop; desligar em toque e em reduced-motion.
- **Ken Burns** (pan+zoom lento numa imagem parada): container `overflow:hidden`; imagem com
  `scale(1→1.15)` + `translate3d` numa animação de 10-20s. Zoom MODESTO (1.0→1.15) — escalar demais = overdraw.
- **Personagem entra** com overshoot (passa e volta) via translate+opacity; idle "respira" (±1-2% scale/
  translateY em 3s loop). Poses via spritesheet + `steps(N)` (salta quadro, roda no compositor).
- **Typewriter** guiado pelo `currentTime` do áudio (não timer solto).
- **Partículas:** CSS puro (poucos elementos transform/opacity) p/ fundo sempre-ligado; **canvas-confetti**
  (ISC, 6KB) só no clímax do FINAL.
- **Transições:** crossfade (opacity), wipe (translateX), íris (scale) — tudo transform/opacity.
- **Câmera virtual:** envolver TODOS os planos num `.palco` e animar o transform DO WRAPPER (push-in
  `scale 1→1.08`, micro-tremor de impacto) — move a cena inteira de graça.
- **Orquestração:** CSS `animation-delay` encadeado p/ cutscene simples; **Web Animations API** p/ controle
  fino (`el.animate().finished.then(...)`, seek, pause, playbackRate) — é o motor nativo da cutscene.

## FERRAMENTAS — VEREDITO (licença só permissiva)
**ADOTAR (nativo, 0KB):** CSS @keyframes (base) · **Web Animations API** (motor da cutscene: timeline/seek/
sync) · SVG animado por CSS · spritesheet com `steps()` (poses do mascote).
**ADOTAR pontual:** **canvas-confetti** (ISC, 6KB gzip, 1 canvas+rAF auto-limpa) — confete/estrelas do FINAL.
**TALVEZ (açúcar):** **Motion** (motion.dev, MIT, ~3.8KB, sobre WAAPI — timeline/stagger curtinho) · anime.js
v4 (MIT) · Theatre.js (core Apache-2.0 ~12KB — editor visual p/ montar a cutscene; em runtime só o core).
**EVITAR:**
- **Lottie** (MIT mas): é VETORIAL, arte IA é RASTER → embutir raster estoura o arquivo E é CPU-bound na
  main thread (60-80% CPU em PC fraco). Só p/ um flourish vetorial pequeno, se muito.
- **Rive** (runtime MIT) — poderoso p/ mascote INTERATIVO com state machine, mas wasm no boot + curva íngreme;
  reservar p/ interação real, não p/ cutscene linear.
- **GSAP** — virou "grátis" (2025) mas a licença **NÃO é permissiva/OSI** (GreenSock própria) → fora da regra
  do projeto. WAAPI+Motion cobrem tudo com MIT.
- tsParticles completo (~100KB), centenas de partículas, planos enormes simultâneos → estoura VRAM.

## SINCRONIZAR narração MP3 com animação/texto
- **Marcadores de tempo:** `audio.addEventListener('timeupdate')` + comparar `audio.currentTime` com uma
  lista de cues `{t, passo}` (dispara troca de cena/legenda). NUNCA `setInterval` (desalinha).
- **Typewriter/câmera:** ler `currentTime/duration` num loop `requestAnimationFrame` (mais fino).
- **Legenda:** WebVTT `<track>` (padrão HTML5; `cuechange` dispara eventos).
- **🔑 ATALHO DE OURO:** o **próprio edge-tts** (que gera o MP3 do Antônio) emite **WordBoundary/
  SentenceBoundary** e exporta **legenda com timing por palavra em SRT/VTT** (classe `SubMaker`). →
  **No MESMO `gerar-audio.yml`, gerar também o `.vtt`** = mapa de tempos exato e grátis p/ (a) legenda,
  (b) velocidade do typewriter, (c) marcadores das trocas de cena, (d) **lip-sync** do mascote. Embutir o
  VTT inline no HTML. É o pipeline mais limpo. ⚠️ AÇÃO: atualizar o workflow de áudio p/ cuspir o VTT.
- **Degradar SEM áudio (obrigatório):** cutscene começa por BOTÃO ("Começar a história" = gesto que
  destrava o áudio); se o áudio falhar, roda a mesma sequência por relógio interno (as animações têm
  durações próprias) + legenda por timer. Nunca depende do som.
- **`prefers-reduced-motion`:** cortar pan/zoom/parallax/câmera; manter crossfades, narração e texto.

## PIPELINE DE ASSET IA — gerar a cena p/ ANIMAR (não chapada)
- **Camadas separadas** (fundo, meio, frente, personagem), cada uma PNG transparente → o navegador é a mesa
  de montagem (parallax por plano, mascote desliza por cima). Uma cena chapada só faz pan/zoom em bloco.
  É a regra de ouro do projeto (assets limpos, montar/animar no navegador).
- **Personagem em POSES** (feliz, apontando, pulando, surpreso) e/ou **em PARTES** (cabeça/braço/boca) →
  poses via `steps()`; partes via mini-rig de fantoche (pivô por junta). 3-5 poses trocadas na hora já
  impressionam e custam quase nada.
- **Recorte transparente** (a IA sai raster sem alpha): rembg (open-source, local) OU LayerDiffuse (FLUX,
  gera PNG com alfa direto). Prompt empurra p/ recorte: "isolated subject, cutout, no background, studio
  lighting, object-centered", ≥768px.
- **Peso (PC fraco):** cada plano ~1280-1600px, otimizado (PNG-8/WebP); **máx 3-4 planos animados
  simultâneos** (cada plano = textura na GPU; muitas grandes estouram a VRAM integrada).

## JEITO RECOMENDADO
**ABERTURA (~12-18s):** HTML + CSS keyframes + WAAPI + `<audio>` MP3 + VTT do edge-tts. Zero lib externa.
Botão "Começar a história" → `.palco` com 4 planos (fundo Ken Burns + meio/frente parallax + mascote entra
e respira) → push-in de câmera durante a fala → legenda+typewriter pelo `currentTime` → partículas CSS
discretas → crossfade p/ a atividade. Reduced-motion: tudo por fade.
**FINAL (~8-12s):** o mesmo + **canvas-confetti** no clímax. Mascote comemora (troca de pose) + push-in com
micro-tremor → explosão de confete/estrelas → medalha com scale-overshoot + brilho → narração de parabéns +
legenda. Reduced-motion: confete vira fade de estrelas estáticas.

## HONESTIDADE (PC fraco)
Dá p/ impressionar MUITO com motion-comic bem dirigido (parallax 3-4 planos + Ken Burns + câmera + poses +
confete). O segredo é DIREÇÃO, não mais efeito. Máx 3-4 planos animados, só transform/opacity, imagens
otimizadas, `will-change` escopado (promover só na janela da animação e limpar depois), reduced-motion
respeitado, confete só no clímax. ⚠️ O código de exemplo desta pesquisa vem em ES6 (arrow/const) — reescrever
em var/function p/ atender o manual premium §14.

## FONTES
MDN WAAPI https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API · Smashing GPU animation
https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/ · Smashing orquestração WAAPI
https://www.smashingmagazine.com/2021/09/orchestrating-complexity-web-animations-api/ · Ken Burns CSS
https://www.kirupa.com/html5/ken_burns_effect_css.htm · Motion comic https://en.wikipedia.org/wiki/Motion_comic
· sprite steps() https://blog.teamtreehouse.com/css-sprite-sheet-animations-steps · timeupdate
https://www.w3schools.com/tags/av_event_timeupdate.asp · audio sync https://hansgaron.com/articles/web_audio/animation_sync_with_audio/part_one/
· MDN WebVTT https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API · edge-tts SubMaker
https://github.com/rany2/edge-tts/blob/master/src/edge_tts/submaker.py · canvas-confetti (ISC)
https://github.com/catdad/canvas-confetti/blob/master/LICENSE · Motion https://motion.dev/ · Theatre.js LICENSE
https://github.com/theatre-js/theatre/blob/main/LICENSE · GSAP não é open-source https://news.ycombinator.com/item?id=43872017
· LayerDiffuse https://runware.ai/blog/introducing-layerdiffuse-generate-images-with-built-in-transparency-in-one-step
· rembg https://gigazine.net/gsc_news/en/20260510-rembg/ · prefers-reduced-motion
https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
