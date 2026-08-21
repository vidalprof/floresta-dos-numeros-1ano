# PROMPTS DAS IMAGENS — A Oficina de Letreiros da Lina (5º ano)

## ⭐ Agora em CARTELA — o senhor tinha razão

As figuras da atividade estavam saindo **uma a uma**, e é por isso que
as três novas (campo, bomba, lâmpada) ficaram destoando das outras: elas
vieram de três gerações diferentes, cada uma com a sua luz e a sua
escala. Geradas **juntas, na mesma folha**, saem irmãs.

São **duas folhas** no lugar de doze pedidos:

| folha | o que vem nela | chamadas |
|---|---|---|
| `cart_peca1` | campo, bomba, tambor, sempre, ombro, ponte, canto, manga | 1 |
| `cart_peca2` | vento, lâmpada, campeão, bombeiro | 1 |

Doze chamadas viram duas — **83% a menos** — e, o que importa mais aqui,
as doze passam a ter o mesmo acabamento.

## Como fazer

1. Cole o prompt da folha no gerador.
2. Salve a folha inteira como `cart_peca1.png` (e a outra `cart_peca2.png`).
3. **Me mande as duas folhas** — eu recorto cada peça com o nome certo
   (`python3 _padrao/cartela.py cortar`), monto a folha de conferência e
   o senhor olha antes de eu embutir.

⚠️ O prompt pede **fundo preto**: é o que faz o recorte sair limpo. Se o
gerador teimar e devolver fundo creme, não tem problema — me avise que eu
uso o outro recorte, que trata sombra.

⚠️ E não deixe o gerador escrever nada na folha. IA sempre erra letra, e
nesta atividade a letra **é** o conteúdo.

---

# Folha `cart_peca1.png`

Vem nela: **lt_campo, lt_bomba, lt_tambor, lt_sempre, lt_ombro, lt_ponte, lt_canto, lt_manga**

```
A SHEET of 8 separate objects arranged in a clean 3x3 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. an empty neighbourhood football pitch with green grass, white side lines and one white goal with a net
  2. an old red cast-iron hand water pump over a stone well, with a curved spout and a wooden bucket under it
  3. a single marching band snare drum with a red rim and two wooden drumsticks resting on top
  4. a round wall clock with a cream face and thick black hands in a chunky wooden frame, no numbers on the face
  5. a friendly child seen from the chest up, from the side, with one hand resting on their own shoulder
  6. a small stone arch bridge over a blue river, seen from the side
  7. the inside corner of a cosy room: two cream walls meeting at a right angle with a small potted plant in the corner
  8. a single ripe mango fruit, yellow and red, with one green leaf attached
```

---

# Folha `cart_peca2.png`

Vem nela: **lt_vento, lt_lampada, lt_campeao, lt_bombeiro**

```
A SHEET of 4 separate objects arranged in a clean 2x2 GRID on a PLAIN PURE BLACK background (#000000), each object fully inside its own cell, well separated from the others, none touching, all at the SAME scale and the SAME lighting. Soft matte clay 3D illustration, children's storybook style, rich saturated colours, soft shadows. No text, no letters, no numbers, no labels, no frames, no background scenery. The objects, in reading order (left to right, top to bottom), are:
  1. a small leafy tree bending to the right, with three long curly white wind swirls and two leaves flying off
  2. a glowing yellow light bulb with clear round glass, a visible curly filament and a grey metal screw base
  3. a golden winner's trophy cup with two handles on a square base
  4. a friendly firefighter in a red helmet and red coat, seen from the chest up
```

---

# ⚠️ O MASCOTE FICA DE FORA DA CARTELA

A Lina tem três camadas: parada, falando e piscando. Elas **não** vão em
cartela nem se geram do zero — as duas últimas são **edição** da pose
parada. Se saírem como três desenhos, ela treme na tela quando fala (o
motor cruza as camadas umas 60 vezes por segundo), e isso não aparece no
print: só com a criança na frente.

As poses de hoje estão boas e medidas (0% de tremor). **Não precisa mexer.**
