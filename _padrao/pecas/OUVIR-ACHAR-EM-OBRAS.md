# `ouvir-achar` — o diário desta peça (o que já foi medido e curado)

> ⚠️ **Este arquivo já disse "não publicar assim". Não diz mais** (ago/2026).
> A bancada fecha com código **0** (`bash _qa/peca.sh _padrao/pecas/ouvir-achar.html`)
> e o portão da voz também (`python3 _qa/vozrobo.py _padrao/pecas/ouvir-achar.html`).
> O que ficou aqui é a MEMÓRIA: cada defeito, por que ele existia e como foi
> **medido** — porque foi tentando adivinhar que eu gastei rodada atrás de rodada.

## 1. Os cartões empilhados numa coluna (curado)

Causa: o MOTOR tem `.opts{flex-direction:column}` (herdado do Broto, onde as
respostas são uma lista). A regra da peça definia `display:flex` e `flex-wrap`,
mas **não** a direção — e **especificidade vale por PROPRIEDADE**: a coluna do
motor continuava mandando.

**Medido** depois do conserto: os dois primeiros cartões em `x=22` e `x=211`, na
mesma altura. Antes: os dois em `x=16`, um embaixo do outro.

> **Regra que fica:** toda regra de flex numa peça que disputa com o motor
> escreve a DIREÇÃO, não só `display` e `wrap`.

## 2. O nome fora do cartão, o alto-falante sumido (curado)

Causa: a opção se chamava `.fig` — e `.fig` é o nome que o MOTOR usa para a
figurinha do **crachá** (82×82, quadrada, fundo branco). Dentro da atividade
montada o crachá atropelava a resposta.

Achado com `CSS.getMatchedStylesForNode` (CDP), listando TODAS as regras que
casavam com o elemento. **Adivinhar não resolveu três vezes; medir resolveu na
primeira.** Hoje o cartão é `.opt.oaf` do começo ao fim e **a classe `.fig` não
existe mais no arquivo** — nem no CSS, nem nas trocas de estado.

## 3. O botão OUVIR era MUDO na mão do Marcos (curado — e é a lição maior)

Palavras dele: *"onde tenho que ouvir a palavra não funciona, tem o enunciado
que funciona, o som da palavra que não funciona. os sons nas opções de respostas
funcionam"*.

A peça falava por `speechSynthesis` — e a ponte do integrador **desliga** essa
voz de propósito, desde que ele pegou duas vozes falando ao mesmo tempo. O
guarda estava certo; errada estava a peça. **Um defeito nascido de um conserto**,
e calado: nenhum erro, nenhum aviso.

Hoje a peça **não declara voz nenhuma**: chama o `diz(...)` que a ponte injeta
(MP3 gravado, Edge TTS), sempre com `if(typeof diz==="function")`. Na bancada
ela fica em silêncio e continua inteira, porque tudo o que a voz diz está
ESCRITO na tela. Medido por `_qa/vozrobo.py`.

## 4. Os defeitos achados AGORA, medindo (ago/2026)

| O que estava errado | Como apareceu | Conserto |
|---|---|---|
| **O desenho de CSS desmontado dentro do cartão** — o miolo do sol num canto e os raios noutro | na FOTO, não no código: as pecinhas têm `left/top` em pixel para uma caixa de 58×58, e o `.des` virou `width:100%` | `.descss` guarda os 58×58; quem cresce é a **escala** |
| **A letra do andaime e o "já tentamos" segurados por acidente** | medido no navegador: quem criava o bloco de contenção era o `backdrop-filter` do vidro fosco. Sem desfoque (Firefox antigo, PC sem aceleração) eles voariam para o canto da página — e só no 2º erro | `position:relative` escrito no `.opt.oaf` |
| **Entidade de HTML chegando na voz** (`Ou&#231;a`) | simulando a ponte na bancada: a chave da gravação sai do TEXTO, e `Ou&#231;a...` nunca bate com o mp3 de `Ouça...` | `textoDe()` — quem decodifica é o navegador, nunca uma expressão à mão |
| **Chave sem figura virava a LUA** | uma fase com `opcoes:["pao","bolo","leite"]` mostrava três luas iguais, sem erro nenhum | `desenho()` devolve `null` e o cartão fica só com a PALAVRA (`.oafso`) |
| **Alto-falante da resposta com 32px** | menor que o dedo de 6 anos (a pesquisa pede 44) | 44×44, e a linha do nome **envolve** para ele nunca encolher |
| **O botão OUVIR era o menor alvo da tela** | 46×96px — do tamanho de um botão de apoio, sendo a fase inteira | 64px de altura, até 320 de largura, com pulso |

## O molde (não esquecer)

- **Broto** (`_jardim/index.html`): figura GRANDE e redonda centrada; respostas
  em pastilhas; borda de baixo mais grossa. O "jeito do Broto" já está na ponte.
- **Marcos, ago/2026:** *"quero que a atividade seja um app lindo, sonoro,
  didático — se a interatividade não se adequa, não utilizar"*, *"os sons e as
  dicas são fundamentais, estão se alfabetizando"* e *"as dinâmicas interativas
  têm que ser mais VISUAIS e SONORAS para os pequenos"*.
- O medalhão grande da ponte é para a figura da PERGUNTA, não para a miniatura
  da resposta (usá-lo lá fez a figura vazar do cartão).
- **O número do `calc` da `.opts` é MEDIDO.** Quem mexer na altura do cabeçalho
  refaz a conta e roda `_qa/leiaute.js` nos seis tamanhos — foi mexendo no botão
  de ouvir que duas respostas ficaram penduradas atrás da borda de baixo.
