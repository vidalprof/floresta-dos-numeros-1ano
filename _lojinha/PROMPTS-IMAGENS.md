# PROMPTS DAS IMAGENS — A Lojinha de Brinquedos do Pipo

Gerado por `_padrao/ESQUELETO/prompts.py`. Copie o bloco de cada
figura e cole no gerador. Os prompts estao em **ingles de
proposito**: os geradores entendem melhor e erram menos.

## Como salvar

1. **O nome do arquivo tem que ser exatamente o que esta escrito**
   (ex.: `lb_pipo_fala.png`). Nome trocado = figura que nao aparece.
2. Fundo branco liso; **PNG com fundo transparente** e melhor ainda.
3. Salvar tudo em `_lojinha/img/`.

> Atalho: em vez de gerar na mao, da para acionar o workflow
> `gerar-imagens.yml` com `lote=_lojinha/_lote.json` e `dest=_lojinha/img`
> — ele desenha, recorta o fundo e commita sozinho, por R$ 0,00.

---

# AS DUAS CAMADAS DO MASCOTE — sao EDICAO, nao desenho novo

⚠️ **Se estas duas forem geradas do zero, o mascote TREME na
tela** — o motor cruza as tres camadas umas 60 vezes por
segundo para a boca acompanhar a voz, e tres desenhos
diferentes viram tremor. No print parado nao aparece; so com
a crianca na frente. Suba a pose parada e peca a EDICAO.

## `lb_pipo_fala.png`

```
[EDICAO da pose parada — subir lb_pipo_feliz.png como base]
Keep this exact same character, exact same pose, exact same colours, exact same position and size in the frame. Change ONLY the mouth: open the mouth into a rounded "ah" shape as if speaking. Do not move anything else. Do not redraw the character.
```

## `lb_pipo_pisca.png`

```
[EDICAO da pose parada — subir lb_pipo_feliz.png como base]
Keep this exact same character, exact same pose, exact same colours, exact same position and size in the frame. Change ONLY the eyes: close the eyes into two happy curved lines, as if blinking. Do not move anything else. Do not redraw the character.
```
