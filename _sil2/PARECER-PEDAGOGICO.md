# Parecer pedagógico — Aprendendo a separar as palavras em sílabas (2º ano)

> Caderno de folha viva, 35 folhas. Português, 2º ano.
> Currículo de Blumenau, 2º ano: *"Ler e escrever corretamente palavras com
> sílabas CV, V, CVC, CCV, identificando que existem vogais em todas as
> sílabas."*, *"Segmentar palavras em sílabas e remover e substituir sílabas
> iniciais, mediais ou finais para criar novas palavras."* e *"Segmentar
> corretamente as palavras ao escrever frases e textos."*
> (`_curriculo/blumenau.txt`).
> Lido folha a folha, na ordem em que a criança encontra, em **20/set/2026**.

## 1. O que este caderno ensina, em uma frase

Que a palavra se parte em **pedaços que a boca abre** — e que cada pedaço tem
uma vogal dentro, porque é ela que faz a boca abrir.

## 2. A escada, e se ela sobe

| Folhas | O degrau |
|---|---|
| 1, 2, 26 | **Sentir** a sílaba: bater palma, contar quantas vezes a boca abre |
| 3–5 | Onde a palavra se parte, e a vogal dentro de cada pedaço |
| 6–8, 27 | **Letra não é sílaba** |
| 9–14, 28, 29, 35 | Classificar pelo número de sílabas (as gavetas do armário) |
| 15–20, 33 | Mexer nas sílabas: tirar, pôr, trocar |
| 21–25 | Achar a sílaba certa no meio de muitas, e escrever a palavra |
| 30–32 | Separar as palavras dentro da frase e do texto |
| 34 | Escrever a própria palavra com o número de sílabas pedido |

**O degrau que faz este caderno valer é a folha 5.** Ela diz: *"em cada pedaço
há uma vogal: é ela que faz a boca abrir."* Isso é exatamente o que a habilidade
da rede pede (*"identificando que existem vogais em todas as sílabas"*) e é o que
transforma a divisão silábica de uma regra decorada num critério que a criança
pode **usar sozinha** numa palavra que nunca viu.

**E a folha 6 é o contraveneno.** *"Letra não é sílaba"* — a confusão clássica do
2º ano — vem imediatamente depois, quando o conceito de sílaba acabou de ficar de
pé. A folha 27 volta a ela vinte folhas depois: é revisão espaçada, e está no
lugar certo.

## 3. O que eu fui procurar, e o que achei

- **Contradição entre folhas:** não achei.
- **Degrau que não sobe:** não achei. O bloco 17-18-19 é exemplar: falta o pedaço
  do **começo**, depois o do **meio** (e a narração avisa: *"o mais difícil de
  ouvir"*), depois o do **fim**. Está na ordem da dificuldade real, não na ordem
  da comodidade.
- **Vocabulário acima do ano:** o caderno diz *pedaço* nas 34 folhas e só chama
  de *sílaba* onde precisa. Os nomes técnicos (MONOSSÍLABA, DISSÍLABA,
  TRISSÍLABA, POLISSÍLABA) aparecem no cartaz da folha 35, depois de a criança já
  classificar há vinte folhas pelo NÚMERO. Está certo para o 2º ano.

### Dois consertos que eu fiz (20/set/2026)

**1. A folha 35 dava um comando que não era o dela.** A narração dizia *"agora as
palavras que dão nome: leve cada exemplo para a linha dele"* — "as palavras que
dão nome" é **substantivo**, e a folha classifica por número de sílabas
(MONOSSÍLABA · DISSÍLABA · TRISSÍLABA · POLISSÍLABA). É resto de clone: a mesma
peça de cartaz existe em dez cadernos e esta veio com o texto de outro. A criança
ouvia, no fecho do caderno, uma instrução de outra matéria. Reescrita para
*"agora monte o cartaz: leve cada palavra para a linha do número de sílabas
dela"*, no `folhas.js` e no `gerar_falas.py` — a voz regrava sozinha, porque o
`falas.json` é a verdade e o carimbo sha1 muda.

**2. A folha 25 estava pendurada no objetivo errado.** Ela pede escrever o nome
da figura inteiro, letra a letra, numa fileira de letras embaralhadas — e vinha
declarada em *"Achar a sílaba certa no meio de muitas"*, que é o que as folhas 21
a 24 fazem. Escrever a palavra toda não mede achar sílaba. O objetivo passou a
**"Achar a sílaba certa no meio de muitas, e escrever a palavra inteira"**.

⚠️ Nenhum portão via nenhum dos dois: o `0b9` confere que cada folha tem **algum**
objetivo, não que o objetivo seja o **certo**, e portão nenhum lê o enunciado para
ver se ele descreve a folha. Essas duas perguntas são de quem lê.

## 4. Uma coisa que eu fui conferir no código, e estava certa

O enunciado da folha 25 promete *"as letras estão embaralhadas ali embaixo"*.
Fui conferir se existia mesmo essa fileira ou se era o teclado de sempre — porque
enunciado que descreve uma tela que não existe é o defeito que eu já achei neste
caderno na folha 35. Existe: é a `fileiraLetras`, posta ali de propósito porque o
desafio da folha é **escrever** o nome do bicho, não escolher entre grafias
parecidas. Registro para quem ler depois não precisar conferir de novo.

## 5. Veredito do pedagogo

**ADEQUADA ao 2º ano**, com os dois consertos aplicados. Conferido em **20 de
setembro de 2026**, folha a folha, contra o *Currículo da Educação Básica do
Sistema Municipal de Ensino de Blumenau* (`_curriculo/blumenau.txt`). As três
habilidades citadas existem no documento da rede palavra por palavra, os oito
objetivos cobrem as 34 folhas de trabalho sem sobra nem buraco, e o conteúdo não
passa do que o 2º ano pede.

⚠️ **O que este parecer NÃO diz.** Ele não é um portão: nenhuma conta mediu o
julgamento acima. Ele diz que alguém leu o caderno inteiro, na ordem em que a
criança o encontra, e assinou.

## ⭐ 23/set/2026 — OS LEMBRETES (o post-it com áudio) e a capa nova

### A ideia, e de quem é

Do professor Marcos: *"em nossas sequências didáticas, o que acha de post-its
com áudio ou coisa do tipo ensinando o que vai ser cobrado na atividade? Para
ajudar o estudante. Seria uma melhoria nos cadernos."* Este caderno é a
**experiência** que ele autorizou (*"sim, faça em um caderno"*) — não é regra da
casa ainda, e só vira se funcionar na turma dele.

### O buraco que ele viu e eu não

Os cadernos de folha viva **ensinam fazendo**. A criança separa sílaba folha
após folha e **em lugar nenhum deste caderno estava escrito o que é uma
sílaba**. Quem esqueceu tinha a dica do item — que resolve *aquele* item — e
nenhum lugar para reaprender a regra. É um buraco de verdade, e ele estava aqui
desde a primeira versão.

### O que entrou

**Sete lembretes**, um por conceito, cada um acompanhando as folhas do seu bloco:

| Lembrete | Folhas |
|---|---|
| O que é uma sílaba | 1, 2, 26 |
| Toda sílaba tem uma vogal | 3, 4, 5 |
| Letra não é sílaba | 6, 7, 8, 27 |
| As quatro gavetas | 9 a 14, 28, 29, 34 |
| Tirar, pôr e trocar sílabas | 15 a 20, 33 |
| Montar a palavra com as sílabas | 21 a 25 |
| Onde uma palavra acaba e a outra começa | 30, 31, 32 |

Cada um é um bilhete amarelo, com a regra em três ou quatro frases e **um
alto-falante por frase**. A folha 35 **não tem** — ela é o cartaz, e o cartaz já
é o resumo.

### ⚠️⚠️ Por que ele nasce FECHADO — e isto é a parte pedagógica da decisão

A lei do EduVerso diz: **o problema vem primeiro e o conceito por ÚLTIMO**. Um
lembrete aberto de cara entregaria a regra antes de a criança tentar, mataria a
lacuna de curiosidade (Loewenstein) e **a folha viraria cópia**. Fechado, o
problema continua vindo primeiro e o conceito fica **disponível** — nunca
imposto. É a mesma decisão do botão *"ver no texto"* da prova de Ed. Física, e
pela mesma razão.

**Ele se abre sozinho uma única vez, e só depois do SEGUNDO erro na mesma
folha.** A conta é por folha e não por item, de propósito: dois tropeços no
mesmo item podem ser distração; dois na mesma folha são o conceito que não
entrou — que é exatamente o que o lembrete tem para dar. Antes disso seria
entregar; nunca seria abandonar quem travou.

### De onde saiu o texto (regra zero)

Do que **este caderno já ensina**: os objetivos declarados no `curriculo.json` e
os exemplos que já estão nos DADOS — BOLA, SOL, GATO, GALINHA, PA-NE-LA,
BOR-BO-LE-TA, COLA. Não há uma palavra que eu tenha escolhido de cabeça, e não
há um segundo texto que possa desencontrar do caderno.

### O que o professor ganha, e é novo

O relatório passa a ter **"Onde a criança foi buscar a regra"**: qual lembrete
ela abriu e quantas vezes. Até hoje o relatório dizia **quanto** ela acertou por
objetivo; agora diz **onde ela sentiu que não sabia** — que é a coisa que o
professor não consegue ver com trinta crianças na sala.

⚠️ **Só conta o que ELA abriu.** O que o caderno abriu sozinho não entra: ali
quem decidiu foi o caderno, e misturar os dois faria o relatório dizer uma coisa
que não aconteceu.

⚠️ **E abrir o lembrete NÃO é erro** — está escrito no próprio relatório, para
que ninguém leia aquele número como demérito. É a criança percebendo que não
lembrava e indo atrás, que é o comportamento que se quer ensinar.

### A capa

Ordem dele no mesmo pedido: *"lembrando a capa deve ficar fantástica"*. A capa
anterior era honesta e chapada — quatro pílulas com um bicho e uma sílaba. **O
caderno chama-se O Armário das Quatro Gavetas e não havia armário nenhum nela.**
Agora há: um móvel de madeira com tampo, laterais, pés e quatro gavetas que
**deslizam para fora**, uma depois da outra, sob uma luz quente. E cada gaveta
mostra **a palavra partida em sílabas** (GA | TO), que é o assunto do caderno
dito na primeira tela.

⚠️ **As figuras deste caderno são RGB com fundo branco** (recortadas das folhas
de papel, sem canal alfa). Dentro da gaveta isso aparecia como um quadrado
branco; em vez de mexer nos PNG — que são os mesmos das 35 folhas — o branco
virou **etiqueta**, de propósito. Tirar o fundo de todos é outro trabalho, com
outro risco, e fica anotado.

### O que este acréscimo NÃO resolve

- ⚠️ **Não sei se a criança vai abrir.** O post-it fechado é a decisão certa
  pedagogicamente e é também a que corre o risco de nunca ser tocada. **Quem
  mede isso é o professor Marcos, com a turma** — e o relatório foi feito
  justamente para ele poder medir.
- ⚠️ **Não sei se três ou quatro frases é o tamanho certo** para quem tem sete
  anos. Foi escolha minha, apoiada na regra de uma ideia por vez.
- ⚠️ **Os outros 32 cadernos continuam sem.** É de propósito: é uma experiência
  em um caderno, como ele pediu.

### Veredito

**ADEQUADO ao 2º ano**, com os sete lembretes e a capa nova. Conferido em
**23 de setembro de 2026**. Nada do conteúdo das 35 folhas mudou: o que entrou
foi um lugar onde a regra está escrita — e que até ontem não existia.
