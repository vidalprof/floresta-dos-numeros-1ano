# 🤖 QA que APRENDE — cada bug vira uma trava (não repete)

> Pedido do Marcos: "quem acha bug, aprende pra não acontecer de novo".
> Aqui mora a memória do auditor. **Toda vez que um erro novo aparecer, vira uma
> REGRA nova** (no `src/motor/auditor.ts` ou uma checagem no build) — assim ele
> **nunca mais passa silencioso**.

## As 3 camadas de trava automática

1. **Trava de ERRO DE JS (runtime)** — `index.html`: qualquer erro de código
   pinta uma **faixa vermelha** na tela → o **QA por screenshot pega na hora**.
   *(Foi o que faltou quando a colisão travou o `create()` sem avisar.)*
2. **Trava de DADOS (Zod)** — `motor/aventura.ts`: dado torto **não monta**
   (tipo errado, faltando campo → erro claro antes de montar).
3. **AUDITOR DE COERÊNCIA** — `motor/auditor.ts`: confere a cena e mostra uma
   faixa (o QA pega). Regras que ele já aprendeu:
   - peça com **asset que não existe** no kit;
   - peça **fora do mundo** (fora dos limites);
   - **COQUEIRO DENTRO DO MAR** (peça de terra numa zona de água);
   - **água/poça na terra seca**;
   - **sobreposição feia** (duas peças no mesmo lugar);
   - **herói começando na água / fora do mundo**;
   - **fala sem áudio** (cobertura de voz).

## Bugs já aprendidos nesta jornada (viraram trava)
- ⛔ `setCollideWorldBounds` numa imagem sem corpo → travava o `create()`.
  → Trava 1 (faixa vermelha) + usar `body.collideWorldBounds`.
- ⛔ Fundo **esticado** = distorção. → Regra de arte: nunca esticar (aspecto nativo).
- ⛔ **Perspectiva misturada** (poça de cima + praia de lado). → Cena coesa 3/4.
- ⛔ Personagem **flutuando** / papagaio subindo e descendo. → âncora nos pés + plantado.
- ⛔ Peça no lugar errado / coqueiro no mar. → **Auditor de coerência** (acima).
- ⛔ **MEMBRO FALTANDO no recorte** (sumiu perna/braço do herói no estilo limpo). Causa: o
  contorno é ESCURO; o recorte antigo tinha tolerância alta + passo "maior componente" que
  comia o contorno e soltava o membro fino, depois jogava fora. **Não pode acontecer.**
  → Conserto (em `tools/fabrica_personagem.py`): tolerância BAIXA (26) + flood só do fundo que
  toca a borda + **sem** descartar por "maior componente puro"; membros ficam garantidos. A
  limpeza de manchas usa **ponte de 5px** (`_maior_com_ponte`) — membro colado ao corpo fica,
  só mancha solta e distante sai. **Na origem:** prompt pede fundo preto liso, sem sombra,
  corpo inteiro no quadro, contorno fechado (ver Especialista em Prompts em `EDUVERSE-EQUIPE.md`).
- ⛔ **Mancha escura flutuante** (sombra que a IA desenha solta). → limpeza por ponte no recorte
  + prompt "no cast shadow / no ground shadow / solid flat black bg".
- ⛔ **COLISÃO não funcionava** (herói atravessava os objetos). Causa: o corpo físico estava
  preso ao sprite MUITO redimensionado (escala ~0.4 + squash/stretch por quadro) → `setSize/offset`
  em px de textura ficava do tamanho/lugar errado. → Conserto: **corpo físico DEDICADO** (retângulo
  fixo de 40×26 px do mundo) que o sprite só SEGUE; objetos usam corpo estático com `updateFromGameObject()`.
  → Trava: **teste automático de colisão** (`tools/qa-colisao.mjs`, Playwright) empurra o herói contra
  a pedra e confirma que TRAVA (x<690). Rodar a cada mudança de física.
- ⛔ **Tela não preenchia / arte serrilhada ao ampliar.** → `Scale.ENVELOP` (preenche) + `antialias:true`
  (arte de cartoon suave, não pixel-art).

## Como CRESCE (o combinado)
Quando um erro novo escapar: (a) reproduz, (b) vira uma **regra no auditor** (ou
uma checagem no build), (c) anota aqui. O auditor **só cresce** — o mesmo erro
não volta duas vezes.

## Lições da Vila Viva (jul/2026) — cada bug do Marcos virou TESTE permanente
1. **Textura faltando não é 404**: esquecer `load.image('piso2')` não dá erro de rede —
   o Phaser desenha quadrado verde `__MISSING`. REGRA no robô: varrer `children.list`
   por textura `__MISSING`/`__DEFAULT` → tem que ser 0. (Bug real: piso2 da sala 2.)
2. **Pixel art treme com tween de ESCALA** (0,48px de meio-pixel em zoom 3). "Respiração"
   por scaleY foi REMOVIDA; vida = olhar pro herói + dog andando. Nunca animar escala
   fracionária em sprite 16px.
3. **Porta "igual no jogo" = VÃO físico + gatilho DENTRO**: casa com colisor maciço +
   zona na frente dispara "de passagem" (reclamação real). Certo: blocos laterais +
   fundo do vão + zona na soleira. TESTE: cruzar na frente da porta NÃO pode entrar.
4. **Teste de colisão nunca empurra contra porta** (o herói ENTRA e o assert mente).
5. **Recorte de tileset com sobra do vizinho** (2px) aparece como "recortes de outra
   imagem" em cima do móvel — recortes sempre conferidos AMPLIADOS antes de entrar.
6. **`__tp` (teleporte de QA) não muda `local`** — testes que trocam de zona validam
   `local`+`salaAtual` explicitamente.
7. **FIT vs ENVELOP**: ENVELOP corta borda (a "casinha cortada" do Marcos). RPG usa FIT
   (quadro inteiro + faixas). No celular em pé o quadro fica menor — deitar resolve.

## Receita da AREIA do autor (auditor jul/2026 — casada BYTE A BYTE com o mockup)
chao.png (22 col; global=lin*22+col): campo=110 (liso 255,173,93); decor campo=111-114
(esparsas 1/8-1/12); miolo claro caminho/praça=23; decor claro=88,89; BLOB claro 3x3=
[[0,1,2],[22,23,24],[44,45,46]] (escala: cantos+bordas repetidas+miolo 23); trilha fina
V=3/25(repete)/47, H=66/67(repete)/68, pingo=69. NÃO usar cols 11-21 (bloco rosado).
Tudo opaco — camada única. Moldura de floresta: grama 245 + blob verde + árvores em cacho.

## Lições v7 (cada uma virou conferência obrigatória)
- Recorte contaminado pelo VIZINHO = "peça cortada" na tela (pedras com fatia de pedra
  alheia; prateleira com lasca da estante). REGRA: todo recorte novo é ampliado 8x e
  conferido ANTES de entrar; se o vizinho encosta, limpar os pixels intrusos (transparência).
- SALA DO AUTOR (wall_simple, 10 col): TL=0 T=3 TR=4 L=10 R=14 BL=40 tampas-porta=41/42
  B=43 BR=44, entorno=50 (parede escura). A PORTA é um VÃO no muro de baixo. Câmera do
  interior: zoom 4 + bounds colados (sala enche a tela; nunca "mar preto").
- backgroundColor do jogo TEM que casar com a moldura escura (#0e0c12) — verde vazava no vão.

## Lições v8/v9 — Mundo do Autor (mapa oficial no motor)
- LER O AUTOR > montar à mão: o mapa da vila veio do `map_village.tscn` (Godot) do próprio
  pixel-boy, decodificado tile a tile p/ `mapa_autor.json` (4 camadas: chão, paredes, base
  ABAIXO do herói, topo/copas POR CIMA). Fórmula PackedInt32Array em referencia/COMO-LER.md.
- CÂMERA presa ao TERRENO jogável (bbox de chão>=0), não ao grid inteiro — senão o herói
  "some" na borda andando pro vazio. TESTE: teleporta pro canto inferior do terreno e confere
  que h fica dentro de cam.worldView.
- Mundo grande que ROLA usa ENVELOP (preenche a tela, sem tarja preta); tela FIXA pequena usa FIT.
- 🔴 DEPTH = Y DO MUNDO QUEBRA quando o objeto está em Y NEGATIVO (sala interior montada ao
  norte do mapa, y=-260): depth negativo joga o móvel PARA BAIXO do piso (some). Usar depth
  RELATIVO (100 + Ylocal). TESTE NOVO: móveis do interior têm depth>0 (senão afundam).
- Entrada de casa no mundo do autor: o tile da porta (base do prédio) COLIDE; a soleira andável
  é o tile de baixo. Gatilho de entrada vai no tile ANDÁVEL, não no desenho da porta.

## Auditores automáticos (pedidos pelo Marcos jul/2026) — o que É e o que NÃO É confiável
- ✅ **MOLDURA (confiável)**: nenhum sprite VISÍVEL pode vazar do quadro da fase
  (getBounds fora de [0,W]x[0,H]). Pegou a pedra vazando SOZINHO. Regra permanente no qa-f1.
  Filtro: pular texturas '__' (retângulos de colisão invisíveis) e HUD (scrollFactor 0).
- ✅ **DINÂMICA JOGÁVEL (o MAIS importante, confiável)**: o robô JOGA a fase até o fim como
  aluno (junta 5 mel → entrega → mundo muda → vitória). Se o aluno NÃO conseguisse concluir
  por bug, o robô REPROVA e nada chega à criança. É o detector nº1 de "travou, não dá pra fazer".
- ⚠️ **RECORTE INCOMPLETO/CORTADO (NÃO confiável por pixel)**: quando o vizinho está COLADO no
  tileset (sem vão transparente), nenhum heurístico de pixel distingue "recorte certo ao lado do
  vizinho" de "recorte que pegou o vizinho" — todos dão opaco dos dois lados. Testado: sliver-com-vão,
  contar-componentes, continua-fora → todos com falso-positivo OU falso-negativo. `auditor-recortes.mjs`
  fica ADVISORY (lista suspeitos p/ eu olhar, não trava). A rede confiável p/ corte é o SCREENSHOT
  (Portão de Arte: olhos meus + do Marcos). Honestidade registrada: não prometer auto-detecção de corte.
- Cada bug novo continua virando teste permanente (aprendizado automático da qualidade).

## Lições Fase 1 v13 (bugs do Marcos → testes permanentes)
- 🔴 TRAVOU NO INTERIOR (celular E pc): o handler de toque tinha `if(local==='fase')` →
  dentro da casa o toque/clique NÃO movia. No celular (só toque) = preso. Certo: mover em
  QUALQUER zona (guardar só por `trocando`). TESTE NOVO: herói SE MOVE dentro da casa + SAI
  da casa (nunca fica preso). Regra: toda zona nova onde o herói entra tem que ter teste de
  "move dentro" e "consegue sair".
- ⏱️ FALSO ALARME de QA: tocar DURANTE o fade de transição (trocando=true) é ignorado (correto)
  → o teste achou que travou. Testes de toque pós-transição têm que esperar `!trocando`.
- 🔊 SOM procedural (Web Audio oscillator) p/ feedback: 'plim' que SOBE a cada item coletado
  (reforça a contagem!), rumble grave nas pedras, arpejo na vitória. Placeholder até SFX reais
  (que ficam na versão itch do pack). AudioContext destrava no 1º gesto (junto com a música).
- 🔤 BALÃO/HUD nítidos em zoom 3: `setResolution(3)` renderiza o texto em 3x → sem borrão.
  (fonte menor compensa: balão 9px, hud 13px). Confirmar no screenshot.
