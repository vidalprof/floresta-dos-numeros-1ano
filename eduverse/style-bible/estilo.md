# 🎨 BÍBLIA DE ESTILO DO EDUCAVERSO (a barra visual — cobrança do Marcos)

> **Regra de ouro:** 2D em **tile** é só a TÉCNICA. O **visual** tem que ser **tão lindo
> quanto o que a gente já produzia antes** (as atividades premium) — não "gráfico de tile
> sem graça". Bonito, rico, **realista no capricho** (luz/sombra/profundidade), pintado à mão.

## O que "lindo e realista" significa aqui
- **Arte pintada à mão premium** (gerada por IA), coesa — **um estilo só** em tudo
  (chão, objetos, personagens). Nada de peça "de outro jogo".
- **Profundidade e volume:** sombras de contato, luz suave, gradientes, oclusão nos cantos —
  o mundo tem "corpo", não é chapado.
- **Realista = caprichado/atmosférico** (não é foto): mantém a cara **storybook/cartoon
  premium** que o Marcos aprovou, só que **rico** em luz, cor e detalhe.

## Efeitos de mundo VIVO (obrigatórios — como nas premium de antes)
Luz do sol deslizando · raios/atmosfera · **vento em rajadas** (árvores/flores/grama balançam) ·
folhas/pétalas/poeira de luz caindo · **água brilhando e ondulando** · fumaça · faíscas ·
sombras que se mexem · **ciclo dia/noite e clima** (chuva, névoa) · bichos (pássaros, borboletas).

## Personagens
- **Vivos:** respiram no idle, andam suave, **mexem a boca ao falar**, piscam.
- **Temáticos:** o Byte e os personagens **vestem o tema** do mundo (pirata, viking…),
  sempre gerados **editando a imagem-âncora** (mesmo personagem, só a fantasia).

## Técnica (para ficar lindo E leve/compatível)
- Assets IA com **recorte limpo** (transparência de verdade), otimizados (~50KB mascote).
- Tiles via `createPattern`; sprites ancorados nos pés, dimensionados pela **altura**; **y-sort**.
- Canvas 2D, offline, compatível (Win7/Chrome antigo). Efeitos leves com fallback (`lowfx`).

## Quem cobra
- **Diretor de Arte** especifica e aprova (estilo/tema/recorte).
- **Auditor de Arte** (automático): tudo IA no estilo, **mundo vivo** (anima), sem sobreposição.
- **Portão 3 (Marcos):** o "ficou lindo?" final. Referência = **as atividades premium de antes**.
