# ⚠️ `ouvir-achar` — REFAÇÃO VISUAL EM ANDAMENTO (não publicar assim)

## O que JÁ foi consertado (e é um defeito de verdade, com lição)

**Os cartões ficavam empilhados numa coluna, por mais que coubessem dois por linha.**

Causa: o MOTOR tem `.opts{flex-direction:column}` (herdado do Broto, onde as
respostas são uma lista). A regra da peça definia `display:flex` e `flex-wrap`,
mas **não** a direção — e **especificidade vale por PROPRIEDADE**: a coluna do
motor continuava mandando.

Conserto: a peça escreve a direção explicitamente. **Medido** depois: os dois
primeiros cartões em `x=22` e `x=211`, na mesma altura. Antes: os dois em `x=16`,
um embaixo do outro.

> **Regra que fica:** toda regra de flex numa peça que disputa com o motor
> escreve a DIREÇÃO, não só `display` e `wrap`.

## O que AINDA está errado (medido, não deduzido)

O cartão não cresce para caber o conteúdo:

```
.opt.fig   altura 82px   (display:block, overflow:visible, position:relative)
.moldura   altura 104px  (position:static, float:none)  ← filho estático MAIOR que o pai
.nom       fica em y=462, fora do cartão (que acaba em y=420)
.zap       NÃO EXISTE na árvore  ← o alto-falante sumiu das opções
```

Um bloco com filho estático de 104px **não pode** ter 82px de altura. Procurei
`height` explícito em toda regra `.opt*` do index montado e **não existe**.
Então falta descobrir quem impõe essa altura — candidatos ainda não descartados:

1. alguma `@media` que perdeu o embrulho ao ser prefixada pelo integrador
   (há `.opt.fig .moldura{width:74px}` que só deveria valer em tela baixa);
2. o `.opt` do MOLDE com `line-height`/`min-height` interagindo com o
   `display:block` que eu forcei;
3. o `.zap` sumido pode ser o mesmo problema — se ele foi removido do DOM, a
   `.linha` mudou de tamanho.

**Próximo passo concreto:** no navegador, listar TODAS as regras que casam com
`.opt.fig` via `getMatchedCSSRules`/CDP e ver qual impõe a altura. Uma medição,
não mais tentativa.

## O molde (não esquecer)

- **Broto** (`_jardim/index.html`): figura GRANDE e redonda centrada; respostas
  em pastilhas; borda de baixo mais grossa. O "jeito do Broto" já está na ponte.
- **Marcos, ago/2026:** *"quero que a atividade seja um app lindo, sonoro,
  didático — se a interatividade não se adequa, não utilizar"* e *"os sons e as
  dicas são fundamentais, estão se alfabetizando"*.
- O medalhão grande da ponte é para a figura da PERGUNTA, não para a miniatura
  da resposta (usá-lo lá fez a figura vazar do cartão).
