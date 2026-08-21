# Pesquisa — Visual PROFISSIONAL + encaixe perfeito (celular E computador) + mapa VIVO — 2026-07

> Pedido do Marcos: pesquisa profunda p/ o app ficar mais profissional no visual, aparecendo **tudo
> certinho no celular E no computador** (o mapa das premium às vezes não aparecia inteiro — não pode
> acontecer aqui); a faixa de unidade ficou feia; o mapa tem que ser **mais vivo**. Alvo: 1 HTML, offline,
> PC fraco. Força: [FORTE]/[CONSENSO]/[OPINIÃO].

## 1. ENCAIXAR EM QUALQUER TELA (celular + computador) [FORTE]
- **Palco `contain` (o que já usamos):** canvas fixo (400×780) escalado por `min(W/base, H/base)` → NUNCA
  corta. É a base certa; o "não aparecia inteiro" das premium era layout fluido sem palco fixo — aqui não acontece.
- **`viewport-fit=cover` + `env(safe-area-inset-*)` [FORTE]:** no iPhone o conteúdo vai atrás do notch/Dynamic
  Island; a barra de topo precisa de folga `env(safe-area-inset-top)` pra não ficar embaixo do notch. (No
  navegador com barra do Safari isso quase não aparece; no modo "app instalado" aparece — por isso resolver.)
- **Letterbox NUNCA vazio [FORTE]:** a sobra dos lados (grande no PC widescreen) deve mostrar um **fundo
  temático** (gradiente/estrelas), não um cinza chapado — senão parece amador. No desktop = coluna central
  (o "app") + moldura preenchida. É o que CNN/Duolingo-web fazem (coluna central + fundo).
- **Testar em aparelho real:** no Chrome "responsivo" o `safe-area-inset` é 0 → só o celular real mostra o notch.

## 2. VISUAL PROFISSIONAL (tirar o "amador") [FORTE]
- **Profundidade com sombras macias (soft-UI/neumorfismo leve):** sombra suave embaixo dos elementos +
  brilho sutil em cima = tátil e caro. Botão 3D (sombra sólida embaixo) já temos.
- **Gradientes suaves** (2 tons perto) em fundos/botões/faixas dão riqueza sem peso.
- **Consistência é tudo:** MESMO raio de canto, MESMO espaçamento, MESMA família de sombra em tudo. O amador
  vem da inconsistência (cada card com uma borda diferente). Definir "tokens" e repetir.
- **Fonte redonda e cheia** (já: `ui-rounded` no iPhone). Hierarquia clara (título gordo, corpo médio).
- **Menos é mais:** poucas cores por tela, contornos sutis (não dourado grosso em tudo).

## 3. MAPA VIVO (sem pesar o PC fraco) [FORTE]
- **Parallax de nuvens:** 2–3 camadas de nuvens suaves derivando em velocidades diferentes (`translateX` no
  CSS) = mundo vivo com profundidade. Barato (só transform).
- **Partículas/brilhos:** poucos pontinhos cintilando (sparkles) espalhados.
- **Idle nos botões:** os nós "respiram" (bob leve up/down), o atual pulsa (farol) — o mapa nunca fica parado.
- **Mascote com vida:** Fagulha respira/pisca/reage ao lado da trilha (já temos) — é o maior "vivo".
- **Regra PC fraco:** só `transform/opacity`, pausar o que sai da tela, desligar parallax no `reduced-motion`.

## 4. APLICAÇÃO no nosso app (o que muda agora)
1. **Letterbox temático** (tema claro = gradiente céu-claro; tema escuro = noite) → PC widescreen fica elegante.
2. **`safe-area-inset-top`** na barra de topo → não fica sob o notch no iPhone instalado.
3. **Faixa de unidade redesenhada** (mais limpa, com ícone, proporção melhor) — a atual "não ficou legal".
4. **Mapa vivo:** nuvens em parallax + brilhos + idle (bob) nos botões da trilha.
5. **Tokens de estilo** (raio 16–20px, sombra padrão, espaçamento) repetidos em tudo → tira o amador.

## 5. MASCOTE + HISTÓRIA (pedido: melhorar/refazer) — plano
- **Mascote:** manter a Fagulha (identidade), mas **elevar** — poses mais expressivas e, se o Marcos quiser,
  **regerar em melhor qualidade** (todas as poses no mesmo estilo, senão fica inconsistente). Decisão dele.
- **História:** reforçar o "porquê" (o mundo precisa de estrelas) com uma abertura mais clara e um arco por
  UNIDADE (cada unidade = um pedaço do céu que acende). Manter fantasia INTRÍNSECA (a história FAZ a matemática).

## FONTES
safe-area/PWA game https://gist.github.com/fozzedout/5e77925381991a9570151550992baf14 · safe-area-inset
https://polypane.app/blog/using-safe-area-inset-to-build-mobile-safe-layouts/ · scale/fit Phaser
https://www.xjavascript.com/blog/how-to-create-a-responsive-game-for-any-screen-size-with-phaser-3/ · centro+max-width
https://dev.to/trae_z/responsive-layouts-done-right-the-critical-role-of-max-width-8m6 · soft-UI/tendências
https://www.robinwaite.com/blog/what-are-mobile-app-ux-design-trends-in-2024 · parallax/vida
https://gamemaker.io/en/blog/creating-depth-and-immersion-parallax · idle animation
https://en.wikipedia.org/wiki/Idle_animation
