# Parecer pedagógico — A Coroa dos Cinco Reinos (4º ano)

> Caderno de folha viva, 25 folhas. Ciências, 4º ano.
> Currículo de Blumenau, 4º ano: *"Conhecer os reinos dos seres vivos, sua
> importância e classificação."*, *"Seres unicelulares e multicelulares."*,
> *"Seres microscópicos (uso de lupa e microscópio)."*, *"Reino Monera, Fungi e
> Protista."*, *"Reino das plantas e dos animais."*, *"Classificação em
> reinos."*, *"Relacionar a participação de fungos e bactérias no processo de
> decomposição, reconhecendo a importância ambiental desse processo."*
> (`_curriculo/blumenau.txt`)
> Lido folha a folha, na ordem em que a criança encontra, em **20/set/2026**.

## 1. Por que este caderno merece um parecer mais desconfiado que os outros

**Foi aqui que o Marcos pegou, lendo, duas coisas que não eram do 4º ano** —
a gaveta *"já foram vivos"* e o NÚCLEO da célula — enquanto o portão `0b9`
passava com nota cheia. As dez citações existiam palavra por palavra; o que a
criança FAZIA na tela é que estava fora do ano. Foi essa rodada que criou a
sexta pergunta do `0b9` (a lista `conceitos`) e, mais tarde, este portão do
parecer.

Então comecei por conferir se o conserto está de pé. **Está:**

- a folha 4, que era a das "peças difíceis" com a gaveta do *já foi vivo*, hoje
  pergunta *"duas gavetas: vivo, ou não vivo?"* — duas gavetas, não três;
- a palavra NÚCLEO não aparece em folha nenhuma;
- e o `curriculo.json` declara **catorze conceitos**, que o portão `0b9` confere
  dentro do bloco do **4º ano de Ciências** do documento da rede. Os catorze
  passam.

⚠️ Este é, dos 31 cadernos de folha viva, **o único em que o `0b9` consegue medir
o conteúdo**: o PDF da rede só traz cabeçalho por ano em Ciências, Geografia e
História. Nos de Língua Portuguesa e Matemática o portão diz "NÃO MEDI", e quem
garante o ano é a leitura. Aqui a conta e o olho concordam.

## 2. O que este caderno ensina, em uma frase

Que os seres vivos se arrumam em **cinco reinos**, e que o critério para arrumar
não é o tamanho nem a beleza: é **quantas células**, **de onde vem o alimento** e
**se dá para ver a olho nu**.

## 3. A escada, e se ela sobe

| Folhas | O degrau |
|---|---|
| 1–5 | **O que é estar vivo** (e o ciclo de vida) |
| 6 | Uma célula ou muitas |
| 7, 10, 24 | O que só o microscópio mostra |
| 8, 9 | Fabrica o alimento, ou precisa comer |
| 11–13 | Os cinco reinos, um a um |
| 14, 15 | Ligar o ser vivo ao reino |
| 16–19 | ⭐ **Cruzar reino e característica** — a coroa |
| 20, 21, 23 | Classificar sozinha |
| 22 | Quem produz, quem come, quem desmancha |
| 25 | A minha coroa |

**O desenho do caderno é o seu argumento.** As folhas 6, 8 e 10 ensinam, uma de
cada vez, os **três critérios**; as folhas 16 a 19 os cruzam com os reinos numa
coroa de três pontas. A criança não decora cinco nomes: ela monta uma tabela de
dupla entrada com as próprias mãos. É a diferença entre classificar e recitar, e
é exatamente o que a habilidade citada pede (*"sua importância e
classificação"*).

**A folha 6 é uma lição paga que ficou boa.** A narração diz: *"todo ser vivo é
feito de células — pecinhas tão pequenas que só se veem no microscópio. Este ser
é feito de uma célula só, ou de muitas?"* Antes ela abria perguntando pela
célula sem nunca ter dito o que é uma. O conteúdo é do ano (está verbatim:
*"Seres unicelulares e multicelulares"*), mas **a palavra tinha de ser
apresentada antes de virar pergunta**. Quem viu foi o Marcos; o conserto está na
tela e o comentário está no `gerar_falas.py`, para não se perder.

**E a folha 22 é a que dá sentido a tudo.** *"Quem produz, quem come, quem
desmancha."* Sem ela, os cinco reinos seriam cinco gavetas; com ela, são um
sistema — e é ali que a habilidade da decomposição se cumpre.

## 4. O que eu fui procurar, e o que achei

- **Conteúdo de outro ano:** não achei (ver o item 1).
- **Contradição entre folhas:** não achei.
- **Degrau que não sobe:** não achei. As folhas 20, 21 e 23 sobem assim: puxar
  para a gaveta, achar o intruso, **escrever** o nome do reino.

### Um defeito que eu achei, e consertei (20/set/2026)

**Três pares de folhas diziam a mesma frase, palavra por palavra:**

| | |
|---|---|
| 12 e 13 | *"Olhe a figura. De qual reino ela é?"* |
| 14 e 15 | *"Ligue cada ser vivo ao reino dele."* |
| 16 e 17 | *"Marque as três características deste reino."* |

O nome na faixa do topo era diferente, e o degrau **existia** — a 13 traz os
reinos que só o microscópio mostra, a 15 põe planta e minúsculos na mesma folha,
a 17 é a coroa dos minúsculos. Mas **para quem ainda não lê, a folha é a
narração**: a criança ouvia a mesma frase e tinha todo o direito de achar que
estava refazendo a folha anterior. É o *"isso eu já fiz"* que o Marcos ouve da
turma, e aqui ele apareceria sem que o caderno estivesse repetindo coisa
nenhuma.

Agora a segunda folha de cada par **nomeia o que mudou**: *"agora os reinos que
não se veem a olho nu"*, *"agora a planta e os minúsculos na mesma folha"*,
*"agora a coroa dos minúsculos"*.

⚠️ **Conserto duplo:** virou o portão **`0b14`** (`_qa/enunciado_repetido.py`),
no pré-voo e na banca de folha viva. Ele compara os `pNenun` entre si, desconta o
*"Folha tal."* e o negrito, e reprova duas folhas com a mesma frase — com
declaração em `ENUNCIADO-OK.json` para a repetição de propósito. Rodado nos 31
cadernos: só o `_mult2` e o `_mult3` tinham mais casos, e os três foram
consertados no mesmo commit.

## 5. Uma ressalva

**25 folhas**, abaixo do piso de 35 de 15/set/2026. O piso vale para caderno
NOVO; os que já estão no ar não crescem nem encolhem, porque mexer no número de
folhas mexe no "continuar de onde parou" de quem está no meio. Registrado.

## 6. Veredito do pedagogo

**ADEQUADA ao 4º ano**, com o conserto das narrações aplicado. Conferido em **20
de setembro de 2026**, folha a folha, contra o *Currículo da Educação Básica do
Sistema Municipal de Ensino de Blumenau* (`_curriculo/blumenau.txt`). As dez
habilidades citadas existem no documento da rede palavra por palavra, os dez
objetivos cobrem as 24 folhas de trabalho sem sobra nem buraco, e os catorze
conceitos que o caderno ensina foram conferidos **dentro do bloco do 4º ano de
Ciências** — o que, neste caderno, é uma medida e não um juízo.

⚠️ **O que este parecer NÃO diz.** Ele não é um portão: nenhuma conta mediu o
julgamento acima. Ele diz que alguém leu o caderno inteiro, na ordem em que a
criança o encontra, e assinou.
