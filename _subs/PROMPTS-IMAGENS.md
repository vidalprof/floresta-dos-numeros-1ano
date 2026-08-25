# PROMPTS DAS IMAGENS — As Plaquinhas do Téo

Gerado por `_padrao/ESQUELETO/prompts.py`. Copie o bloco de cada
figura e cole no gerador. Os prompts estao em **ingles de
proposito**: os geradores entendem melhor e erram menos.

## Como salvar

1. **O nome do arquivo tem que ser exatamente o que esta escrito**
   (ex.: `sn_castor_fala.png`). Nome trocado = figura que nao aparece.
2. Fundo branco liso; **PNG com fundo transparente** e melhor ainda.
3. Salvar tudo em `_subs/img/`.

> Atalho: em vez de gerar na mao, da para acionar o workflow
> `gerar-imagens.yml` com `lote=_subs/_lote.json` e `dest=_subs/img`
> — ele desenha, recorta o fundo e commita sozinho, por R$ 0,00.

---

# O MASCOTE (pose parada)

## `sn_castor_feliz.png`

```
a friendly cartoon character named Téo, the guide of this activity about As Plaquinhas do Téo, standing, full body, facing the viewer, smiling warmly, mouth closed, eyes open. Soft matte CLAY 3D illustration, handmade plasticine model photographed in a studio, rounded chunky friendly shapes, rich saturated colours, soft gentle shadows, smooth matte surface, children's storybook look. Not a photograph, not flat vector. No text, no letters, no numbers, no logo, no watermark. ONE single object, centered, filling the frame, isolated on a plain pure white background, no scenery, no floor, no horizon, no other objects.
```

---

# AS DUAS CAMADAS DO MASCOTE — sao EDICAO, nao desenho novo

⚠️ **Se estas duas forem geradas do zero, o mascote TREME na
tela** — o motor cruza as tres camadas umas 60 vezes por
segundo para a boca acompanhar a voz, e tres desenhos
diferentes viram tremor. No print parado nao aparece; so com
a crianca na frente. Suba a pose parada e peca a EDICAO.

## `sn_castor_fala.png`

```
[EDICAO da pose parada — subir sn_castor_feliz.png como base]
Keep this exact same character, exact same pose, exact same colours, exact same position and size in the frame. Change ONLY the mouth: open the mouth into a rounded "ah" shape as if speaking. Do not move anything else. Do not redraw the character.
```

## `sn_castor_pisca.png`

```
[EDICAO da pose parada — subir sn_castor_feliz.png como base]
Keep this exact same character, exact same pose, exact same colours, exact same position and size in the frame. Change ONLY the eyes: close the eyes into two happy curved lines, as if blinking. Do not move anything else. Do not redraw the character.
```
