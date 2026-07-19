# 🔎 Pesquisa de ferramentas e referências — RPG Educativo por IA (jul/2026)

> Pedido do Marcos: "pesquise se alguém já faz o que estamos tentando, estude ferramentas
> pra melhorar e facilitar o trabalho, com conhecimento e tecnologia." Este é o resultado,
> resumido pra virar decisão. Fonte: pesquisa web real (jul/2026).

## O que importa em 1 parágrafo
**Ninguém faz exatamente o nosso recorte** (RPG jogável no navegador, grátis, roda em PC velho,
IA gera SÓ o miolo pedagógico ancorado na BNCC + arte CC0 fixa + Portão 0 anti-prova). O risco
não é "já existe igual" — é execução (peso e qualidade). E há **3 ferramentas prontas que matam
a nossa maior fonte de bug** (montar fase na mão no código): **Tiled + grid-engine + Zod**.

## Decisões recomendadas (as 6 ações)
1. **MANTER Phaser 3.** Benchmarks 2025-26: é o mais estável e leve para PC fraco (AMD FX/3.5GB/
   Chrome 109). NÃO migrar pra Godot (export web +40MB, risco out-of-memory) nem RPG Maker (330MB+).
2. **ADOTAR Tiled + grid-engine** (o par que acaba com os bugs de montagem manual):
   - **Tiled** (editor visual de mapa) → exporta JSON que o Phaser lê nativo (`tilemapTiledJSON`),
     com camada de colisão por propriedade. Desenhar o mapa em vez de codar acaba com bug de
     profundidade/colisão/moldura.
   - **grid-engine** (Annoraaq, plugin Phaser) → movimento em grade, colisão por tile em várias
     camadas, NPC que segue, pathfinding. https://github.com/Annoraaq/grid-engine
3. **PADRONIZAR assets em Kenney (CC0)** como base neutra (aldeões/crianças/cidade, sem violência:
   RPG Urban Pack, Tiny Town) + Ninja Adventure só pra cenário. **EVITAR** LPC (CC-BY-SA+GPL,
   ShareAlike obriga abrir a arte) e Sprout Lands grátis (não-comercial). https://kenney.nl
4. **CONTRATO da atividade em Zod (structured output).** Schema em Zod → JSON Schema pro LLM →
   valida o retorno com o mesmo Zod. Dá pra codar o **Portão 0 como validação automática**
   (ex.: `problema_do_mundo` obrigatório e ANTES de `conceito`; fala do personagem termina em "?").
   Vira parte do QA determinística — menos "entregar e ver depois".
5. **rexUI (rexRainbow)** para caixa de diálogo + efeito máquina de escrever (evita reinventar UI).
   https://rexrainbow.github.io/phaser3-rex-notes/docs/site/ui-dialog/
6. **Blindar o Portão 0 com ciência: "Intrinsic Integration" (Habgood & Ainsworth).** Conteúdo
   tem que viver na mecânica central (vencer = aprender), não em quiz entre fases. Lição do
   DragonBox: divertido ≠ aprendeu → incluir uma "missão-espelho" no fim que exige aplicar o
   conceito, pra MEDIR aprendizagem (registrada no JSON da atividade).

## Concorrentes/vizinhos (o que existe e por que não serve de base)
- **Rosebud AI** — texto→jogo no navegador, mas gera o jogo TODO por IA, tende a 3D/Three.js
  (pesado), pago, conteúdo não ancorado em currículo. Bom só como inspiração.
- **Eduaide / Educaplay** — geram ATIVIDADES (quiz/jeopardy/bingo) = prova disfarçada (nosso
  Portão 0 proíbe). Não é RPG de mundo.
- **GDevelop (education)** — engine no-code com IA e material pedagógico forte, mas o modelo é
  "o aluno aprende A FAZER jogo", não "professor pede e sai o RPG da matéria dele". Mentalidade
  diferente — vale estudar o material deles.
- **Astrocade / Taskade / Figma AI** — brainstorm/protótipo, não RPG leve jogável.

## Ciência que valida o nosso jeito
- **Intrinsic Integration** (Habgood 2011; réplica ACM 2022): integrar o conteúdo NA mecânica
  divertida gera MUITO mais aprendizagem que "conteúdo colado". É a versão acadêmica do Portão 0.
- **Prodigy Math** (RPG de contas, 20M usuários) — engajamento alto, mas pouca prova científica
  de eficácia. **DragonBox** — álgebra "sem perceber", porém num estudo os alunos gostaram mais
  mas APRENDERAM mais com tutor tradicional. **Lição:** medir aprendizagem, não só diversão.

## Links-chave
- Engines: https://phaser.io/news/2026/04/phaser-vs-kaplay-vs-excalibur-2d-web-game-framework
- grid-engine: https://github.com/Annoraaq/grid-engine
- Tiled+Phaser: https://baraujo.net/integrating-tiled-maps-with-phaser/
- Kenney CC0: https://kenney.nl/assets/rpg-urban-pack
- Zod/structured output: https://techsy.io/en/blog/llm-structured-outputs-guide
- Intrinsic Integration: https://dl.acm.org/doi/10.1145/3549503
