# Referência OFICIAL de composição — a vila do próprio autor (pixel-boy)

- `na_map_village.tscn` + `na_tileset.tres`: a cena Godot REAL do autor
  (github.com/pixel-boy/NinjaAdventure, CC0), baixada em jul/2026.
- `mapa_oficial_renderizado.png`: o mapa dele reconstruído tile a tile pelos nossos PNGs.

## Como decodificar (fórmula provada)
`layer_N/tile_data = PackedInt32Array(a,b,c, ...)` — trios por tile:
- `a` = posição: x = a & 0xffff, y = (a>>16) & 0xffff (int16 com sinal)
- `b` = fonte: src = b & 0xffff (0=village_abandoned 1=floor 2=interior_floor 3=animated 4=wall_simple),
  atlas_x = (b>>16) & 0xffff
- `c` = atlas_y = c & 0xffff (int16 com sinal)
Desenhar camada 3 (chão/paredes) PRIMEIRO, depois 0,1,2 (props).

## A GRAMÁTICA do autor (o que copiar na nossa vila)
1. Chão = campo de grama com tufos esparsos.
2. CAMINHOS de terra ORGÂNICOS (borda irregular) serpenteando e RAMIFICANDO;
   casas com a porta NO caminho; caminho sai do mapa (convida a explorar).
3. Árvores em CACHOS de 2-4 copas sobrepostas (triângulo/losango), formando
   manchas de floresta nas bordas — nunca árvores solitárias espalhadas.
4. Poços/torres/estátua nos ENTRONCAMENTOS do caminho.
5. INTERIOR = sala com moldura wall_simple num canto AFASTADO do mesmo mapa
   (mesma técnica que o nosso motor usa — validada pelo autor).
