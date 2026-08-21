# CARTELAS — A Terra dos Papagaios (5º ano)

São **4 folhas**, não 23 imagens. Gere uma por vez (no Gemini quando houver
crédito, ou no ChatGPT) e me mande — eu recorto com os nomes certos.

⚠️ O fundo TEM que sair **preto liso**. É ele que permite o recorte transparente.


---

## cart_mascote  (1 peças)

`nv_base`

```
A SHEET of 1 separate objects arranged in a clean 1x1 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. a friendly BLUE-AND-YELLOW MACAW (arara) standing, seen from the side-front, beak closed, eyes open, calm and curious, whole body visible
```


---

## cart_avatares  (6 peças)

`nv_cr1, nv_cr2, nv_cr3, nv_cr4, nv_cr5, nv_cr6`

```
A SHEET of 6 separate objects arranged in a clean 2x3 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. a girl with dark brown skin and black curly hair, chest-up portrait, wearing a simple sailor scarf
  2. a boy with light brown skin and straight black hair, chest-up portrait, wearing a small straw hat
  3. a girl with light skin and red wavy hair, chest-up portrait, wearing a blue neckerchief
  4. a boy with dark skin and short black hair, chest-up portrait, wearing a rope necklace with a shell
  5. a girl with brown skin and two black braids, chest-up portrait, wearing a feather in her hair
  6. a boy with pale skin and brown curly hair, chest-up portrait, holding a tiny spyglass
```


---

## cart_travessia  (8 peças)

`nv_mandioca, nv_milho, nv_batata, nv_cacau, nv_cavalo, nv_trigo, nv_cana, nv_roda`

```
A SHEET of 8 separate objects arranged in a clean 3x3 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. a cassava root (mandioca), whole, single object, centred
  2. an ear of maize with green leaves, single object, centred
  3. a potato, single object, centred
  4. a cacao pod, open, showing the beans, single object, centred
  5. a horse standing, side view, single object, centred
  6. a bundle of wheat ears, single object, centred
  7. a stalk of sugar cane, single object, centred
  8. a wooden cart wheel, single object, centred
```


---

## cart_bordo  (8 peças)

`nv_bussola, nv_astrolabio, nv_barril, nv_corda, nv_mapa, nv_luneta, nv_bau, nv_ampulheta`

```
A SHEET of 8 separate objects arranged in a clean 3x3 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. an old brass compass, top view, single object, centred
  2. a brass astrolabe, single object, centred
  3. a wooden barrel, single object, centred
  4. a coil of thick rope, single object, centred
  5. an old rolled parchment map, single object, centred
  6. a small brass spyglass, single object, centred
  7. a wooden treasure chest, closed, single object, centred
  8. an hourglass with sand, single object, centred
```


---

## Depois que a folha voltar

```
python3 _padrao/cartela.py cortar _novo/<folha>.png \
        <nome1>,<nome2>,... --dest _naveg/img
```

Ele recorta na ordem de leitura e monta uma folha de conferência em
xadrez — que eu OLHO antes de embutir.
