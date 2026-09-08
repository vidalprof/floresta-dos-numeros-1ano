# 🗂️ As folhas de cartela, como vieram do gerador

Aqui ficam as **folhas inteiras** que o Marcos gerou, antes do recorte. Guardar a
origem importa: se uma peça precisar ser recortada de novo (com margem diferente,
outro tamanho, ou porque melhorei o recorte), não é preciso gerar tudo outra vez.

| arquivo | receita | o que traz |
|---|---|---|
| `Gemini_Generated_Image_4fing…` | preta, com contorno de adesivo | lobo, lama, boca, cabo, gola, lago |
| `Gemini_Generated_Image_88m41…` | idem | goma, mago, tora, bola, rosa, caneca |
| `Gemini_Generated_Image_cw2x2…` | idem | saco, mapa, navio, fada (+ navio repetido 2×) |
| `Gemini_Generated_Image_fs5f3…` | idem | pipa, luva, dedo, foca, sino, vela |
| `Gemini_Generated_Image_sbu0h…` | idem | peixe, faca, uva, panela, girafa, tesoura |
| `cartela_d.jpg` | **magenta, sem contorno** ⭐ | xícara, cola, pipoca, janela, cebola, bota |
| `nova__*.jpg` | preta (segunda leva das mesmas) | repetição das cinco de cima |

⭐ **A receita boa é a do `cartela_d.jpg`**: fundo magenta chapado, sem contorno de
adesivo, sem sombra. Com ela o recorte é exato; com a preta+contorno eu tive que
adivinhar onde acabava o adesivo, e a bola de futebol chegou a perder um pedaço.
Receita completa e prontos para copiar: `_alfa1/PROMPTS-FIGURAS.md`.

**Como recortar** (o caminho que funciona, em `MEMORIA-DO-PROJETO.md`):
distância à cor exata do fundo (medida na borda da própria folha), alfa em rampa,
despill só a 3 px da beirada, e **nunca** `fill_holes` — senão tapa o vazado da asa.
