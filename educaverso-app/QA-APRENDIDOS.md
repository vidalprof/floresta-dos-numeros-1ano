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
