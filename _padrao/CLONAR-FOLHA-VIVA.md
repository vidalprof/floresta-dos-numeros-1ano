# CLONAR UM CADERNO DE FOLHA VIVA — a lista das peças que TÊM que trocar

> **Cobrança do Marcos (15/set/2026): *"todo esse processo precisa ser mais
> preciso e rápido"*.** Ele estava certo, e este documento nasce da conta do que
> me atrasou naquele dia. Montei A Fábrica de Nomes inteira e só *depois* fui
> rodar os portões — nove reprovações em fila, cada uma custando uma volta. E
> **cinco delas eram a mesma coisa**: pedaço do caderno de origem que veio junto
> no clone e que eu esqueci de trocar.
>
> O `_padrao/CLONAR-MOTOR.md` já faz esse papel para o motor. A folha viva não
> tinha o dela. Agora tem — e tem script: **`bash _padrao/clonar_folha.sh
> <origem> <nova> <prefixo>`** troca tudo o que está nesta lista e roda o
> pré-voo. Ler isto antes de clonar à mão.

---

## ⚠️ A REGRA QUE EXPLICA TODAS AS OUTRAS

**O que vem no clone e NÃO dá erro nenhum é o que morde.** O caderno abre
bonito, o `node --check` passa, o print fica perfeito — e o defeito só aparece
com a criança na frente, ou num portão lá no fim da fila. Tudo nesta lista é
*conteúdo* do caderno de origem disfarçado de motor.

---

## As sete peças, na ordem em que doem

| # | o que é | onde mora | o que acontece se ficar |
|---|---|---|---|
| 1 | **o sorteio das folhas** (`novaFolha()`) | `index.html`, no fim do `<script>` | ⚠️ **A PIOR.** Ele lista `p1..pN` do caderno ANTIGO. Se o novo tem mais folhas, as últimas ficam sem pote → `ST.folha["p24"]` é `undefined` → `TypeError` na montagem e o caderno **não abre**. Se tem menos, sobram potes órfãos. |
| 2 | **os objetivos do relatório** (`var OBJETIVOS`) | `folhas.js` | O relatório do professor sai com os objetivos da outra atividade. O `_qa/pedagogo_curriculo.py` reprova (pergunta 3), e é bom que reprove: sem isso ia para a escola dizendo que a criança "usa S ou SS pela posição" num caderno de substantivos. |
| 3 | **o `curriculo.json` + o `var CURRICULO`** | os dois lados, e têm de ser IGUAIS | Mesma coisa pelo lado do dossiê. E as citações têm de existir **palavra por palavra** no `_curriculo/blumenau.txt` — é a única coisa que o professor não tem como conferir sozinho. |
| 4 | **o prefixo das figuras e da voz** | `img()`, `_narr.src`, `CHAVE_LS`, o troféu e os selos | `img/ls_pato.png` num caderno cujo prefixo é `sb_` = quadradinho vazio e 404 no console. O `_qa/clone.py` (item 8, PREFIXO ALHEIO) pega. ⚠️ E o `CHAVE_LS` repetido faz **dois cadernos brigarem pelo mesmo "continuar de onde parou"**: a criança abre um e cai no meio do outro. |
| 5 | **o `var LIGAR`** | `folhas.js`, no topo | As folhas de ligar são as únicas cujos ids não nascem de `n<pi>_`. Apontar para a folha errada quebra DUAS: a que liga **nunca fecha** e a apontada **fecha sozinha**. Aconteceu no `_rima1`, no ar, e só o portão novo `_qa/conta_folha.js` pegou. |
| 6 | **`NOMES`, `GESTOS`, `ITENS`, `CORES`** | `index.html` (blocos marcados) | `NOMES` curto = folha sem título. `GESTOS` herdado = o portão do leque mede o cardápio errado. `CORES` curto = faixa sem cor no fim. |
| 7 | **a capa (`f0`)** e o cabeçalho do arquivo | `folhas.js` / topo do `index.html` | A capa é a primeira coisa que a criança vê. Numa capa herdada desta casa ficou um `img("sapo")` de outra atividade: o app abria com um quadradinho vazio, e **nenhum portão de texto viu**. |

---

## A ordem que economiza voltas (foi o que faltou em 15/set)

Montar tudo e só depois auditar é o caminho longo. A ordem certa:

1. **Clonar e trocar as SETE peças acima** — antes de escrever qualquer folha.
2. **`bash _qa/previo.sh <pasta>`** já aqui, com o caderno ainda vazio. Ele
   custa 2 segundos e pega prefixo alheio, objetivo herdado e currículo
   desencontrado *antes* de eu ter escrito mil linhas em cima.
3. Escrever os DADOS e as folhas.
4. **`python3 <pasta>/gerar_falas.py`** e `bash _qa/previo.sh` de novo.
5. **`node _qa/conta_folha.js <pasta>`** — o pote e os itens registrados batem?
6. **`node _qa/joga_folha.js <pasta>`** — todo item fecha?
7. Só então a banca inteira: `bash _qa/auditar_folha.sh <pasta>`.

⚠️ **O passo 5 é novo e não é opcional.** Ele nasceu de um defeito que passou
por TODA a banca: o jogador dizia "ok, 5 de 5" e o andarilho contava 14 itens —
cada um certo no seu canto. Só cruzando os dois números é que a folha que fecha
cedo demais aparece.

---

## Armadilhas medidas, que não estão em portão nenhum

- **Nome com espaço num campo de teclado.** O teclado da casa escreve letra por
  letra e **não tem barra de espaço**: `"SANTA CATARINA"` como gabarito é uma
  folha que nunca fecha. Palavras curtas e de uma só.
- **Acento no gabarito de um campo digitado.** Se o que a folha mede não é o
  acento, exigir o `Ã` num teclado de 39 teclas é reprovar a criança por outra
  coisa. Ou tira o acento da palavra escolhida, ou aceita as duas formas (ver o
  `semAcento` do `_casa1`, e o motivo de ele NÃO valer em caderno de ortografia).
- **Palavra repetida numa folha de "ache o erro".** Contar por palavra em vez de
  por posição faz a folha fechar deixando a segunda ocorrência errada na tela.
- **O contrato do jogador para pintar** é: a peça publica `pinta-<id>-<x>` **e
  carrega `data-lapis="<x>"`**, o estojo publica `lapis-<x>`. Pôr o `data-lapis`
  no lápis, ou com o valor da cor, faz o jogador dizer "não sei jogar" — e folha
  que o jogador não alcança é folha que ninguém mede.
- **Chave de dado igual à palavra que está na tela.** O
  `_qa/resposta_impressa.py` lê a resposta declarada dentro do texto visível e
  acusa — com razão, porque de fora não dá para distinguir. Trocar a chave por
  um número é mais honesto que declarar exceção.
- **Rodar um portão passando a PASTA quando ele quer o ARQUIVO** (e vice-versa).
  Vários da casa aceitam um só dos dois e, no outro, estouram ou dizem coisa que
  não é verdade. Quando um portão responder algo estranho, conferir a chamada
  antes de acreditar nela: perdi uma volta inteira em 15/set "consertando" uma
  capa que estava certa, porque tinha passado a pasta para o `_qa/boot.js`.
