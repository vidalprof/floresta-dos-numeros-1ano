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
