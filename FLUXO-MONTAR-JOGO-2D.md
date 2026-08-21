# 🎮 FLUXO OFICIAL — MONTAR O JOGO 2D PRIMEIRO, DEPOIS A PEDAGOGIA

> Decisão do Marcos (2026-07-20, depois de MUITOS erros de cenário): a causa dos erros
> foi eu **improvisar a montagem do jogo** (espalhar prop por prop, recortar árvore de
> atlas denso, misturar peça de pack diferente). O pedagógico SEMPRE esteve documentado
> (MANUAL-MESTRE, EDUVERSE-*, pesquisas); faltava o fluxo de **MONTAR O JOGO**. É este.

## A REGRA DE OURO (grava no capacete)
**Primeiro um JOGO INTEIRO e FUNCIONAL, montado como o AUTOR do pack manda, de UM pack
só. Só DEPOIS a camada pedagógica por cima.** Nunca o contrário. Nunca misturar packs.

## Por que tantos erros antes (lição paga)
- Recortei UMA árvore de uma região de **floresta DENSA** do atlas Ninja (feita pra
  ladrilhar, vários troncos juntos) → saiu cortada, "3 árvores", "foto colada".
- Espalhei prop por prop num campo de grama vazio → ralo, sem cara de fase de verdade.
- Cheguei a cogitar misturar Kenney (simples) com Ninja (detalhado) → estilos brigam.
- **Conserto:** usar o pack como o autor projetou (tiles compostos em MAPA), de um pack só.

## O FLUXO, passo a passo (nunca pular)

### 1. ESCOLHER 1 PACK COMPLETO, COESO, LIVRE (CC0/CC-BY) — e usar SÓ ele
Candidatos que JÁ temos no repo (`content/assets/`):
- **Ninja Adventure — COMPLETO** (`ninja-adventure-full/`): ~24 personagens ANIMADOS
  (fichas 64×112 = 4 direções × 7 quadros), tilesets, monstros, armas, FX, itens, HUD.
  É o pack do jogo atual → **recomendado** (coeso, animado, detalhado, já familiar).
  ⚠️ As árvores moram no atlas DENSO — usar como MAPA (tree-line/mata composta), NÃO
  recortar uma isolada.
- **Kenney Tiny Town** (`kenney/tiny-town/`): 132 tiles avulsos LIMPOS (pinheiros, casas,
  cercas, caminhos, água), CC0, monta cena linda (ver `Sample.png`). Estilo mais
  simples/fofo. Precisa de personagem de outro pack Kenney (Tiny Dungeon tem).
- (Futuro) LPC/OpenGameArt: completos, mas CC-BY-SA = exige atribuição.
**REGRA:** tudo (chão, casa, árvore, herói, inimigo, item) do MESMO pack. Sem mistura.

### 2. MONTAR O JOGO FUNCIONAL como o AUTOR manda (antes de qualquer matemática)
- **MAPA de verdade** (level design): compor os tiles em cena — tree-line de mata (2
  tiles de altura pra árvore cheia), caminhos com cantos (autotile), casas montadas
  peça a peça (telhado+parede+porta), água com margem. Referência = o `Sample.png` do
  pack. NÃO espalhar prop solto em grama vazia.
- **PERSONAGEM VIVO:** anda nas 4 direções com animação (grid-engine já faz — o motor
  FaseGrid já anima down/up/left/right; a ficha 64×112 tem os quadros). ✅ já funciona.
- **VIVO:** sons/música, transições animadas entre telas, props com leve movimento,
  ambiente (partículas). ✅ o motor já tem tudo isso.
- **PORTÃO 1 (Robô-Lógica):** o robô-QA JOGA o mundo do começo ao fim como jogador —
  anda, entra em casa, atravessa. Travou/feio → volta pro passo 2. (Só passa adiante
  quando é um JOGO DE VERDADE, bonito e jogável.)

### 3. SÓ ENTÃO: a CAMADA PEDAGÓGICA por cima (institucionalização)
- A mecânica de aprendizagem entra SOBRE o jogo pronto: o aluno **só avança de fase
  quando alcança o OBJETIVO pedagógico** (ex.: arruma os grupos iguais → a carroça
  passa → próxima fase). Problema primeiro, conceito por último (Portão 0).
- Institucionalização (Brousseau): no fim, o mentor NOMEIA o que a criança fez
  ("isso é MULTIPLICAR: 3×4=12"). Voz do Antonio (edge-tts MP3, nunca navegador).
- Avaliação stealth por baixo (evidência→rubrica→parecer→nota), já construída.
- **PORTÕES 2/3 (professor):** prévia + aprovação do Marcos.

### 4. DOCUMENTAR/AUTOAPRENDER
- Todo bug/lição novo vira regra AQUI e na `MEMORIA-DO-PROJETO.md`. A esbo do 2º jogo
  já nasce sabendo o do 1º.

## Respostas diretas às perguntas do Marcos (2026-07-20)
- **"Os do Ninja são ninja?"** O pack chama "Ninja Adventure" mas é um **RPG top-down
  genérico** (aldeões, fazendeiro, monstros, vila) — nada obriga a ser tema ninja. Serve.
- **"Tem packs completos e livres?"** Sim: Ninja-full (temos), Kenney (temos), LPC.
- **"Consegue ficar vivo (animação, som, andar 4 direções)?"** SIM — já funciona no
  motor atual. Nunca foi o problema; o problema era só a montagem do cenário.
- **"Usar tudo de um pack só pra não dar bug?"** EXATO — é a regra de ouro acima.
