# 🎨 CARTELAS DE FIGURAS — A Fábrica de Palavras (1º ano)

> Pedido do Marcos, 8/set/2026: *"pode passar o prompt para as figuras que faltarem"* · *"cartela sabe"*.

> **Por que em cartela, e não uma a uma:** peça gerada junto sai IRMÃ das outras — mesma luz,
> mesma escala, mesmo estilo. E custa uma geração em vez de nove. É a regra da casa desde a
> cartografia, quando 45 figuras uma a uma custaram ~R$9,00 onde ~R$1,60 bastava.

> **A semente vai TRAVADA** (o número no fim de cada bloco). Se precisar refazer uma peça
> depois, gerar com a MESMA semente mantém a família.

> **Caminho:** `gerar-imagens.yml` com `modelo=gemini` (ou `lote=` no Pollinations, de graça).
> Depois o Claude recorta com `python3 _padrao/cartela.py cortar <folha> nome1,nome2,... --dest _alfa1/img`,
> renomeia com o prefixo `al_` e roda o `_banco/montar.py` para as figuras entrarem no banco.

---

## Cartela A — as palavras-irmãs da troca de sílabas (9 figuras)

**Nomes dos arquivos, na ordem de leitura:** `lobo, lama, boca, cabo, gola, lago, goma, mago, tora`

```
A sheet showing 9 separate objects arranged in a tidy 3x3 grid. Each object sits alone inside its own cell, well separated from the others, none of them touching, all drawn at the same scale and lit the same way. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. Soft even studio light coming from the upper left, gentle contact shadow directly under the object. The background behind every object is plain, perfectly flat, pure black (#000000). Every surface is smooth, blank and unmarked. The image contains only the objects themselves. The objects, in reading order from left to right and top to bottom, are:
  1. a friendly grey wolf standing on all four paws, seen from the side
  2. a small puddle of thick brown mud with a little splash
  3. a smiling open mouth with pink lips and white teeth
  4. a coiled electric cable with a plug on one end
  5. the folded collar of a blue shirt, seen from the front
  6. a small round blue lake with a green grassy bank around it
  7. a bottle of white glue with the cap open
  8. a friendly wizard with a pointed blue hat and a long white beard
  9. a short log of cut wood with visible bark and rings
```

**Semente:** `7011`

---

## Cartela B — palavras novas para as folhas de alfabetização (12 figuras)

**Nomes dos arquivos, na ordem de leitura:** `pipa, luva, dedo, foca, sino, vela, peixe, faca, uva, panela, girafa, tesoura`

```
A sheet showing 12 separate objects arranged in a tidy 4x3 grid. Each object sits alone inside its own cell, well separated from the others, none of them touching, all drawn at the same scale and lit the same way. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. Soft even studio light coming from the upper left, gentle contact shadow directly under the object. The background behind every object is plain, perfectly flat, pure black (#000000). Every surface is smooth, blank and unmarked. The image contains only the objects themselves. The objects, in reading order from left to right and top to bottom, are:
  1. a colourful diamond kite with a long ribbon tail
  2. a single woollen glove, thumb up
  3. a hand with the index finger pointing up, other fingers closed
  4. a friendly grey seal sitting up, balancing a ball on its nose
  5. a golden hand bell with a wooden handle
  6. a lit white candle with a small orange flame
  7. a plump orange fish seen from the side
  8. a kitchen knife with a wooden handle, blade pointing left
  9. a bunch of purple grapes with two green leaves
  10. a metal cooking pot with two handles and a lid
  11. a friendly giraffe standing, long neck, seen from the side
  12. a pair of scissors with red plastic handles, blades closed
```

**Semente:** `7012`

---

## O que cada cartela destrava

- **Cartela A** libera a folha *"troque as sílabas de lugar e forme outra palavra"* (BOLO → LOBO,
  MALA → LAMA, CABO → BOCA, LAGO → GOLA, GOMA → MAGO, RATO → TORA). Hoje ela está de fora da
  Fábrica de Palavras por falta EXATAMENTE dessas figuras — o exercício só funciona com as duas.
- **Cartela B** engorda o vocabulário de todas as folhas: sílabas novas (PI, LU, DE, FO, SI, VE,
  PEI, FA, U, PA, GI, TE) e palavras de 1, 2 e 3 sílabas para a escada didática ficar mais larga.
