# 🔍 A PROVA: o caderno de Computação do 3º ano, folha por folha

> Pergunta do Marcos (25/set/2026): ***"mas é possível criar sequências didáticas
> de computação usando isso que vc falou? cobrindo os objetivos do currículo?"***
>
> Resposta em forma de roteiro, não de promessa. Aqui estão **as 35 folhas** do
> `_comp3`, cada uma com **o que a criança faz**, **a peça da MÁQUINA DE VIDRO**
> que ela usa e **o objetivo do currículo** que aquela folha mede.
>
> **Os 9 objetivos do 3º ano são cobertos, todos, e nenhuma folha fica sem
> objetivo** — que são as duas contas que o portão `0b9` faz.
>
> ⚠️ Isto é **roteiro**, não caderno montado: é a etapa 3 do
> `SEQUENCIAS-DIDATICAS.md §0`. A colheita das folhas de papel (etapa 1) e o
> crivo (etapa 2) vêm antes de escrever uma linha de código — e o Marcos vê a
> colheita ANTES de eu escolher, que é ordem dele.
>
> **O modelo:** `_sequencias/PLANO-COMPUTACAO.md`. **O currículo:**
> `_curriculo/computacao-blumenau.txt`.

## Os 9 objetivos do 3º ano (resumidos; o verbatim está no currículo)

| Sigla | Eixo | Objetivo |
|---|---|---|
| **PC1** | Pens. Computacional | verdadeiro/falso em sentenças lógicas, **com negação** |
| **PC2** | Pens. Computacional | **decomposição**: dividir, resolver as partes, combinar |
| **PC3** | Pens. Computacional | criar e **simular** algoritmos com sequências e **repetição com condição** (iteração indefinida) |
| **MD1** | Mundo Digital | relacionar **informação** com **dado** |
| **MD2** | Mundo Digital | dados **estruturados em formatos** específicos |
| **MD3** | Mundo Digital | diferenciar **hardware** e **software** |
| **CD1** | Cultura Digital | utilizar **navegadores e ferramentas de busca** |
| **CD2** | Cultura Digital | usar ferramentas para **se expressar em formatos digitais** |
| **CD3** | Cultura Digital | impacto do **compartilhamento de informações pessoais** |

---

## As 35 folhas

### Bloco A · A MÁQUINA E O PROGRAMA — f1 a f13

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 1 | **O problema, antes de tudo:** a máquina precisa levar a mensagem e só entende instruções. Ela tenta com palavras e não funciona. | a máquina apagada | tentar | PC3 |
| 2 | Duas instruções, uma por vez — e **os blocos caem DENTRO da memória**, com o ponteiro andando à vista. | memória + ponteiro | montar e rodar | PC3 · MD3 |
| 3 | *"Agora são três instruções, e a ordem importa."* | memória | montar e rodar | PC3 |
| 4 | Ela **prevê onde a máquina vai parar** e só depois roda. | ponteiro | prever | PC3 |
| 5 | **Depurar:** o programa vem montado e errado; a máquina para na linha do erro. | memória | consertar | PC3 |
| 6 | *"Agora a máquina não mostra onde parou."* Ela **lê o programa** e acha. | memória | ler e consertar | PC3 |
| 7 | Quatro instruções iguais viram **"repita 4 vezes"**. | ponteiro voltando | montar e rodar | PC3 |
| 8 | *"Agora é repita **ATÉ** chegar"* — a iteração indefinida. | ponteiro + sensor | montar e rodar | PC3 |
| 9 | *"Agora o caminho é desconhecido"* — não dá para contar os passos, logo o "até" é obrigatório. | sensor | montar e rodar | PC3 |
| 10 | A máquina lê o sensor e mostra **V ou F** num registrador. | registrador | escolher V/F | PC1 |
| 11 | *"Agora com o NÃO":* "se **não** tiver parede, ande". | registrador | montar e rodar | PC1 |
| 12 | V/F em frases do dia a dia, com "não" no meio. | — | escolher V/F | PC1 |
| 13 | **Hardware ou software:** as peças de vidro × o programa que está dentro delas. | a máquina inteira | classificar | MD3 |

### Bloco B · DIVIDIR O PROBLEMA — f14 a f18

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 14 | **O problema:** o programa é longo demais e **não cabe na memória**. Ela vê não caber. | memória cheia | tentar | PC2 |
| 15 | **Dar nome a um pedaço** — nasce um bloco novo, guardado à parte. | memória com nome | criar bloco | PC2 |
| 16 | Usar o bloco criado **duas vezes**. | chamada | montar e rodar | PC2 |
| 17 | *"Agora são dois blocos com nome"*, e o programa fica curto. | chamadas | montar e rodar | PC2 |
| 18 | **Ler** um programa decomposto e dizer o que ele faz, sem rodar. | memória | ler | PC2 |

### Bloco C · ABRIR A MÁQUINA — f19 a f25

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 19 | A **mesma frase** aparecendo na tela e na memória: uma é o que se entende, outra é o que se guarda. | tela + memória | operar | MD1 |
| 20 | **Informação × dado:** separar a frase do número que a guarda. | memória | classificar | MD1 |
| 21 | A mesma informação em **duas linguagens** — letra e luz acesa. | codificador | decodificar | MD1 |
| 22 | O **formato manda:** no mesmo disco, foto, som e texto guardados de jeitos diferentes. | disco | classificar | MD2 |
| 23 | Abrir um arquivo **no formato errado** e ver sair bobagem na tela. | disco + tela | escolher e ver | MD2 |
| 24 | Pôr cada arquivo na **gaveta do seu formato**. | disco | arrastar | MD2 |
| 25 | Preencher a **ficha do arquivo**: nome, formato, tamanho, dono. | disco | preencher | MD2 |

### Bloco D · LIGAR NA REDE — f26 a f32

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 26 | O **cabo** liga a máquina do colega. Ela manda um arquivo e vê chegar do outro lado. | porta de rede | operar | CD3 |
| 27 | O **navegador de faz-de-conta**: procurar e **ler o endereço**. | navegador | operar | CD1 |
| 28 | *"Agora você escolhe entre os resultados"* — e eles não são todos iguais. | navegador | operar e escolher | CD1 |
| 29 | **Voltar, aba, endereço** — as partes do navegador, usadas de verdade. | navegador | operar | CD1 |
| 30 | **O que se conta e o que não se conta.** Ela decide, e a tela mostra o que aconteceu. Pode voltar e tentar o outro caminho. | porta de rede | decidir e ver | CD3 |
| 31 | *"Agora é a senha"*, contada a um colega — e o que ele faz com ela. | porta de rede | decidir e ver | CD3 |
| 32 | *"Agora é a foto da turma"* — mandar ou não, e o que volta depois. | porta de rede | decidir e ver | CD3 |

### Bloco E · FAZER COM A MÁQUINA — f33 e f34

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 33 | Ela **produz** algo na máquina (um recado escrito e desenhado) e **salva no formato certo**. | tela + disco | produzir | CD2 |
| 34 | *"Agora o mesmo recado em outro formato"* — e ela escolhe qual serve para o que quer. | disco | produzir e escolher | CD2 |

⭐ **Companheira deste objetivo, já no ar:** a **Oficina de Vídeo**
(https://vidalprof.github.io/a-oficina-de-video/) cumpre o mesmo CD2 em escala
grande. O caderno dá a noção; a Oficina dá a ferramenta.

### Fecho — f35

| # | O que a criança faz | Peça da máquina | Gesto | Objetivo |
|---|---|---|---|---|
| 35 | **O cartaz:** a máquina de vidro inteira, rotulada, com o que ela mandou, do que ela é feita e o que ela fez na rede. **E o gancho:** *"e o que esta máquina ainda NÃO sabe fazer?"* | a máquina inteira | cartaz | MD3 |

---

## As duas contas que o portão `0b9` faz

### 1. Todo objetivo tem folhas que o medem — 9 de 9

| Objetivo | Folhas | Quantas |
|---|---|---|
| PC1 | 10 · 11 · 12 | 3 |
| PC2 | 14 · 15 · 16 · 17 · 18 | 5 |
| PC3 | 1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 | 9 |
| MD1 | 19 · 20 · 21 | 3 |
| MD2 | 22 · 23 · 24 · 25 | 4 |
| MD3 | 2 · 13 · 35 | 3 |
| CD1 | 27 · 28 · 29 | 3 |
| CD2 | 33 · 34 | 2 |
| CD3 | 26 · 30 · 31 · 32 | 4 |

### 2. Toda folha tem objetivo — 35 de 35

Nenhuma folha de enchimento: as 35 aparecem na tabela acima (as folhas 2 e 35
medem dois objetivos cada).

---

## O leque de gestos — a conta que o portão `0b` (padrão) faz

| Gesto | Folhas | % |
|---|---|---|
| montar e rodar | 2 · 3 · 7 · 8 · 9 · 11 · 16 · 17 | **23%** |
| operar a tela | 19 · 26 · 27 · 28 · 29 | 14% |
| escolher / V-F | 10 · 12 · 23 · 28 | 11% |
| classificar / arrastar | 13 · 20 · 22 · 24 | 11% |
| decidir e ver | 30 · 31 · 32 | 9% |
| prever · ler · consertar | 4 · 5 · 6 · 18 | 11% |
| produzir | 33 · 34 | 6% |
| tentar (o problema) | 1 · 14 | 6% |
| criar bloco · decodificar · preencher · cartaz | 15 · 21 · 25 · 35 | 11% |

✅ **Nenhum gesto acima de 40%** (o maior é 23%) e **muito mais de 4 gestos
diferentes** — as duas regras do leque, cumpridas por desenho e não por sorte.
⭐ **E repare como isso foi conseguido:** a bancada é UMA peça, mas dentro dela a
criança **monta, prevê, conserta, lê e cria bloco** — cinco coisas diferentes. Foi
assim que o bloco A ficou com 13 folhas sem virar "a mesma tela treze vezes".

---

## As regras da casa, conferidas neste roteiro

- ✅ **35 folhas** (piso medido no cronômetro do Marcos: 20–25 folhas = 30 min).
- ✅ **O conceito por último:** a folha 1 é o problema sem solução; a palavra
  *"algoritmo"* só é dita depois de ela ter montado muitos.
- ✅ **Mecânica em BLOCO, não espaçada** — cinco blocos colados, cada um subindo
  degrau, porque espaçar faz a criança sentir que voltou.
- ✅ **Cada segunda folha do par NOMEIA o que mudou** (*"agora são três"*, *"agora
  é repita ATÉ"*, *"agora o caminho é desconhecido"*, *"agora com o NÃO"*, *"agora
  é a senha"*) — portão `0b14`, porque para quem não lê a narração **é** a folha.
- ✅ **O fecho é alcançável a qualquer momento**, para o tamanho não castigar quem
  vai devagar.
- ⚠️ **Falta declarar `conceitos` no `curriculo.json`** — sem isso o portão diz
  *"NÃO MEDI"* o conteúdo, e 21 cadernos da casa já estão nessa dívida. Este
  nasce com a lista.
- ⚠️ **E o portão `0b9` ainda não abre o currículo de Computação** (só o
  `blumenau.txt`). É a primeira coisa a fazer, meia hora.
