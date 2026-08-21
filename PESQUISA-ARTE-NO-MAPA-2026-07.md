# 🗺️ Pesquisa: tirar 100% do posicionamento de ARTE do código (Tiled faz) — jul/2026

> Pedido do Marcos: "se a ferramenta faz tudo isso, então não faça nada na mão." E ele lembrou
> que JÁ tinha pedido isso antes (tarefa "motor genérico que lê o mapa"). Resultado: SIM, dá —
> e a ferramenta é o **Tiled**, que já usamos. O código vira um RENDERIZADOR GENÉRICO.

## Resposta curta
O Tiled posiciona TUDO visualmente (chão, parede, casa, móveis, árvores) e o Phaser lê como DADO.
Faltavam dois recursos do Tiled que agora entram: **object layer + `createFromObjects`** (arrastar
móveis) e **Terrain/Wang tiles** (parede que se desenha sozinha — mata o bug "esquerda ≠ direita").

## O que JÁ fizemos nesta rodada (confere com a pesquisa)
- ✅ Enfeites viraram **objetos no mapa** (camada `decor`); o código só faz um laço genérico que
  desenha o que o mapa manda (`map.getObjectLayer('decor')`). Auditor visual: 0.00% (idêntico).
  → É exatamente o passo 2–3 da recomendação da pesquisa.

## Recomendação prática (ordem) — como zerar arte no código
1. **Atlas único de props em grade 16×16** (juntar casa/estante/baú/árvore/piso num PNG só, tudo
   múltiplo de 16). Mata o bug "imagem de 48px transbordou a parede": arte alinhada à grade, 1
   textura só (leve p/ PC de escola). `Object Alignment = Top Left` no tileset (Tiled e Phaser
   concordam na origem).
2. **Object layer "decor" no Tiled, arrastar os props com o mouse** (Insert Tile), cada um com um
   `type` (bau/estante/casa/arvore). Nada disso vai pro código. ✅ (já emitimos por gerador; o
   ideal futuro é o Tiled GUI ou a IA gerando essa camada por regra.)
3. **Um loader genérico** no Phaser: cria as tile layers, liga colisão pelo `ge_collide`, e
   `createFromObjects` com fábrica `type → sprite/classe` (lê depth e props do objeto). ✅ (feito)
4. **Collision Editor do Tiled** p/ marcar quais props são sólidos (com Arcade/grid-engine a
   colisão é sempre o retângulo do tile — suficiente p/ bloquear/não bloquear).
5. **Terrain Brush / Wang Set p/ paredes** — bordas e cantos se resolvem sozinhos no editor e
   exportam prontos (Phaser carrega normal, custo zero em runtime). **Fim de desenhar parede na
   mão** (a causa do bug parede direita ≠ esquerda). ← PRÓXIMO PASSO de maior valor.
6. **(Opcional) Interiores por parâmetro:** libs JS leves geram o layout de um cômodo a partir de
   parâmetros (`@mikewesthad/dungeon`, `rot.js`) — "a IA pede sala 9×7 e sai o cômodo". A mobília
   coerente vem de REGRA + IA gerando a object layer (não existe lib grátis que auto-mobilie).

## Decisões
- **NÃO migrar pro LDtk agora:** o auto-tiling dele é mais bonito, mas o loader Phaser é imaturo
  (v0.0.0, sem docs). O Tiled carrega nativo e resolve 100% da dor. (LDtk exporta pra Tiled se um
  dia quisermos o auto-layer dele.)
- **Sprite Fusion** (editor web grátis, exporta JSON-Tiled) serve p/ montar chão/parede rápido;
  mais básico que o Tiled p/ props/colisão. Dá pra usar os dois (ambos falam JSON-Tiled).

## O que SEMPRE sobra pro código (honesto)
Comportamento, não posição: o que o objeto FAZ (contar mel, entrega, pedras sumirem, vitória),
diálogo, animação, som, câmera, a cola do grid-engine e as "regras" procedurais. Isso é regra de
jogo — não é arte. **Zero posicionamento de ARTE no código é atingível; o código guarda REGRAS.**

## Links
- Phaser Tilemap API: https://docs.phaser.io/api-documentation/class/tilemaps-tilemap
- createFromObjects (mikewesthad post-2): https://github.com/mikewesthad/phaser-3-tilemap-blog-posts
- Collision editor + Arcade: https://phaser.discourse.group/t/using-tiled-collision-editor-with-arcade-physics/9977
- Terrain/Wang (autotile runtime, se preciso): https://github.com/browndragon/phaser3-autotile
- Interiores procedurais: https://github.com/mikewesthad/dungeon
- Sprite Fusion: https://www.spritefusion.com/  · LDtk loader (imaturo): https://github.com/mobilex1122/phaser-ldtk-importer
