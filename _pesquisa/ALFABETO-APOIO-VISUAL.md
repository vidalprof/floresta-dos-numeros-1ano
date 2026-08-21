# O alfabeto como apoio visual na Padaria das Letras — parecer do pedagogo

> Pergunta do Marcos (ago/2026), palavras dele: *"poderia verificar se o alfabeto
> como apoio visual nessa atividade do 1 ano faria sentido? consulte os
> especialistas em currículo e educação"*.
>
> Atividade: **A Padaria das Letras** (`_padaria/`), 1º ano, Língua Portuguesa,
> 32 fases, 14 mecânicas, mascote Fubá.
> Quem assina: **PEDAGOGO/CURRICULISTA** — que é quem manda na mesa até o 5º ano
> (`_padrao/RECEITA.md` §0-A), com o game designer e o especialista em
> interatividade consultados nas partes de tela.
>
> **Isto é PARECER, não implementação.** Nada foi alterado em `_padaria/` nem em
> `_padrao/pecas/`.

---

## A resposta em uma linha

**Sim, faz sentido — mas não do jeito que a pergunta sugere.** O alfabeto **não**
deve virar moldura fixa da tela: em **25 das 32 fases** o conteúdo é **SOM**
(sílaba, rima, fonema), e ali 26 letras não são apoio, são ruído. Ele entra em
**5 fases**, em **três formas diferentes**, e é **proibido em 2**.

| forma | o que é | onde |
|---|---|---|
| **BANCADA** | o arco vazio onde ela **põe** as letras. O alfabeto é o material da fase, não o gabarito | fase 2 (`f04`, ordenar) |
| **PRESENTE** | a fita à vista, com voz ao tocar, numa fase declarada **sem erro** | fase 32 (`f32`, ligar-pontos) |
| **GAVETA** | a fita **fechada**, que abre quando a criança pede ou quando o andaime cresce; conta como dica no relatório do professor | fases 4, 6 e 21 (`f12`, `f05`, `f25`) |
| **PROIBIDO** | a letra não pode existir na tela | fases 18 e 24 (`f18s`, `f24s`, caixas de som) |

E há uma resposta melhor do que a pergunta, no fim deste documento: **existe uma
habilidade de alfabeto do 1º ano de Blumenau que a Padaria não cobre**, e é
justamente aquela em que o alfabeto visível é o próprio conteúdo.

---

## 1. O que o currículo de Blumenau diz — verbatim

Fonte: `_curriculo/blumenau.txt` (Currículo da Educação Básica do Sistema
Municipal de Ensino de Blumenau, 440 pág.). O texto vem de tabela de PDF, então
as colunas quebram em linhas soltas; abaixo elas estão recompostas, **sem trocar
uma palavra**, com a linha do arquivo ao lado.

**1º ANO · TODOS OS CAMPOS DE ATUAÇÃO · Análise linguística/semiótica
(Alfabetização) · objeto de conhecimento: *Conhecimento do alfabeto do português
do Brasil*** — linhas 2787–2793:

> **"Distinguir as letras do alfabeto de outros sinais gráficos."**
> *Conceitos/conteúdos: sistema alfabético de escrita, alfabeto, sinais gráficos
> (números, sinais de pontuação, emoji, entre outros).*

**Mesma unidade, mesmo objeto de conhecimento** — linhas 2822–2825:

> **"Nomear as letras do alfabeto e ordená-las."**
> *Conceitos/conteúdos: ordem alfabética.*

**1º ANO · objeto: *Construção do sistema alfabético*** — linhas 2799–2802:

> **"Reconhecer o sistema de escrita alfabética como representação dos sons da
> fala."**
> *Conceitos/conteúdos: grafema/fonema, ordem alfabética.*

**1º ANO · objeto: *Construção do sistema alfabético e da ortografia*** —
linhas 2817–2820:

> **"Identificar fonemas e sua representação por letras."**
> *Conceitos/conteúdos: fonema/grafema, alfabeto e som das letras.*

**1º ANO · CAMPO ARTÍSTICO-LITERÁRIO · mesmo objeto** — linhas 2896–2899:

> **"Relacionar elementos sonoros (sílabas, fonemas, partes de palavras) com sua
> representação escrita."**
> *Conceitos/conteúdos: alfabeto, fonema/grafema, sílaba.*

**1º ANO · Escrita (compartilhada e autônoma)** — linhas 2772–2780:

> **"Observar escritas convencionais, comparando-as às suas produções escritas,
> percebendo semelhanças e diferenças."**
> *Conceitos/conteúdos: fonema/grafema, sistema alfabético de escrita, conceito
> de palavra, convenção da escrita (letras maiúsculas e minúsculas).*

E o parágrafo do texto introdutório de Alfabetização e Língua Portuguesa, que é
o que decide a **forma** do apoio — linhas 2167–2172:

> *"Para alfabetizar, é preciso entender que a língua/linguagem é um organismo
> vivo, pulsante e que se transforma em seu percurso histórico. O sistema de
> escrita alfabética é o resultado de processo histórico intenso e complexo, o
> qual **não pode ser apropriado efetivamente, de modo a constituir os sujeitos,
> fora de sua função social**. Isso implica um processo de imersão na cultura
> escrita do qual decorre a compreensão mais sistemática da língua, e nunca o
> contrário (BRITTO, 2012)."*

**O que isso decide, em uma frase:** o currículo de Blumenau é bakhtiniano — o
alfabeto tem que aparecer **em função social**, dentro do mundo da padaria (a
gaveta de pães com letra, a placa, a prateleira), **não** como friso decorativo
pendurado na parede da tela. Um alfabeto que não serve para nada dentro da
história contraria o texto acima ainda que esteja "certo" no conteúdo.

### Sobre os códigos EF01LP…

**Não achei nenhum código `EF01LP` no arquivo** (`grep` em 21.208 linhas: zero
ocorrências). O currículo de Blumenau, na extração que temos, traz as
habilidades **pelo texto**, sem o código da BNCC ao lado. As habilidades citadas
acima são reconhecivelmente as da BNCC de 1º ano, mas **não vou colar código em
cima de texto que o arquivo não traz** — isso viraria citação inventada. Se o
Marcos quiser os códigos, dá para baixar a BNCC pelo `baixar-curriculo.yml` e
fazer o casamento habilidade a habilidade.

### Uma coisa que achei conferindo, e que ele precisa saber

O `_padaria/conteudo.json` diz, no campo `mesa`, que as habilidades foram
*"copiadas verbatim do `_curriculo/blumenau.txt`"*. **Cinco das sete conferem
palavra por palavra** (objetivo1 a objetivo5 — são as cinco citadas acima).
**Duas não achei no arquivo:**

- `objetivo6` — *"Reconhecer e comparar palavras que rimam, identificando
  semelhanças e diferenças entre os sons finais das palavras"*, atribuída ao
  objeto de conhecimento *"Consciência fonológica"*. Procurei por
  `palavras que rimam`, `sons finais` e `fonológica`: a expressão
  **"consciência fonológica" não existe no arquivo**, e essa habilidade não
  aparece. O que existe de rima no 1º ano de Blumenau é outra coisa:
  *"Recitar parlendas, quadras, quadrinhas, trava-línguas, com entonação
  adequada e observando as rimas"* (Oralidade, linha 2845) e *"Identificar e
  (re)produzir, em cantiga, quadras, quadrinhas, parlendas, trava-línguas e
  canções, rimas, aliterações, assonâncias…"* (linha 3121).
- `objetivo7` — *"Segmentar oralmente palavras em sílabas e fonemas,
  relacionando os sons às letras que os representam na escrita"*. Não achei.
  O que há é *"Segmentar oralmente palavras em sílabas"* (2852) e *"Identificar
  fonemas e sua representação por letras"* (2817) — duas habilidades, não uma.

**O conteúdo das fases continua defensável** (as fases de rima ancoram nas
linhas 2845/3121; as caixas de som ancoram na 2817). O que está errado é a
**etiqueta**: dizem "verbatim de Blumenau" duas frases que Blumenau não escreve
assim. Não mexi — é conserto de conteúdo, e há gente trabalhando na pasta. Fica
registrado aqui.

---

## 2. O que a pesquisa da casa diz — os dois lados, com número

### A favor (por que a pergunta dele é boa)

1. **O alfabeto é objeto de conhecimento explícito do 1º ano**, com duas
   habilidades próprias (2787 e 2822). Não é apoio de fora da matéria: é
   matéria.
2. **O arco do alfabeto tem lastro de pesquisa** — já está destilado na
   `_padrao/RECEITA.md` §"O que a pesquisa diz sobre alfabetização", item 3:
   *"Alphabet Arcs support students in visualizing the alphabetical sequence,
   recognizing shapes, and building phonics understanding"* (fonte primária:
   Florida Center for Reading Research, *Arco del Alfabeto / Speedy Alphabet
   Arc*, em `_pesquisa/web/dinamicas-alfabetizacao-fazendo.md`). A curva dá
   **âncora espacial** (o meio do arco é o M/N) que a fileira reta não dá.
3. **Apoio externo à memória é exatamente o que a carga cognitiva pede**
   (Sweller): a criança que não precisa segurar 26 letras na cabeça sobra
   memória de trabalho para a tarefa de verdade.
4. **A criança que não lê é a que mais precisa** — e a casa já decidiu isso duas
   vezes: o alto-falante em toda resposta (*"o alto-falante nas respostas
   também, para ajudar os alunos que não sabem ler"*) e, na própria peça
   `digitar.html`, a ordem dele registrada em comentário: *"nas fases com letras
   seria interessante ter apoio visual, figuras"*.
5. **O veto do Marcos manda:** *"não podemos fazer muito difícil, a criança tem
   que conseguir passar"* (`RECEITA.md` §1). Criança travada perde a aula
   inteira. Apoio que destrava é obrigação, não luxo.

### Contra (e é por isso que a resposta não é "põe o alfabeto na tela")

1. **Decoração não é neutra: ela subtrai.** `_pesquisa/REGRAS-NEUROCIENCIA.md`
   §C: *"decoração a mais atrapalha o aprendizado em **23 de 23 testes,
   d = 0,86**"*; e `REGRAS-INTERATIVIDADE.md` lei 3: detalhe sedutor
   **g ≈ −0,16** (compreensão −0,19, transferência −0,12). Em fase de rima, 26
   letras na borda da tela são detalhe sedutor com nome científico.
2. **Apoio que dá a resposta de graça não é apoio.** Em `f12` a tela pergunta
   *"A, B, ___, D"*. Um alfabeto visível responde sozinho. Vira reconhecimento
   visual, não recuperação — e recuperação é o que fixa (Roediger; Bjork,
   dificuldade desejável). A regra da casa já diz isso do outro lado:
   `RECEITA.md` §1 — *"o 3º nível NÃO entrega a resposta do item que está sendo
   avaliado… o molde certo é 'mostro UM, você faz o resto'"*.
3. **Numa escolha entre M e B, o alfabeto inteiro não ajuda em nada.** Ele só
   engorda o campo visual de uma tarefa que já tem 4 alvos.
4. **A peça de caixas de som PROÍBE a letra na tela.** `_padrao/DINAMICAS.md`,
   linha da peça `caixas-de-som`: *"a letra não pode aparecer durante o
   preenchimento: viraria ditado, que é outra coisa e vem depois. Primeiro o
   som; a letra só no fim, dentro das caixas."* Um alfabeto sempre visível
   **quebra a peça mais bem fundamentada da atividade** (consciência fonêmica é
   o preditor mais forte de leitura no 1º ano).
5. **Custo de tela real.** O `_padaria/index.html` roda em
   `#app{position:fixed;inset:0}` — altura fixa, sem rolagem de página. Uma
   faixa permanente de 26 letras com alvo de 44 px come uma linha inteira em
   toda fase, no PC velho da escola e no celular. A casa já pagou esse defeito
   com outro nome ("resposta fora da tela", `_qa/leiaute.js`).

### O que decide entre os dois

A pergunta que separa apoio de muleta, e que vale para cada fase:

> **A letra é a FERRAMENTA desta fase, ou é a RESPOSTA dela?**
> Ferramenta → o alfabeto entra. Resposta → o alfabeto é gabarito e fica fora
> (ou entra só como degrau do andaime, quando a criança já errou).

---

## 3. Fase a fase — as 32, olhando o `conteudo.json`

Ordem real de jogo. "Alfabeto?" responde a pergunta acima.

| # | id | mecânica | o que a criança faz | alfabeto? | por quê |
|---|---|---|---|---|---|
| 1 | `f01` | ouvir-achar | ouve PÃO/BOLO/MEL e toca na **figura** | **não** | a resposta é figura; letra nenhuma está em jogo |
| 2 | `f04` | ordenar | põe A, B, C, D, E na ordem | **sim — BANCADA** | o alfabeto **é** o material. Em **arco vazio**, não em fileira; ela põe as letras, o arco não as traz |
| 3 | `f03r` | intruso | acha a que não rima | **não** | conteúdo é o som do **fim**; 26 letras são ruído |
| 4 | `f12` | completar | "A, B, ___, D" | **sim — GAVETA** | é a resposta. Fechada por padrão; abre no 2º/3º degrau do andaime, e conta como dica no relatório |
| 5 | `f08` | traçar-letra | escreve P, B, M com o dedo | **não** | o modelo já está na tela (as bolinhas). Um alfabeto ao lado disputa o olho com o traço |
| 6 | `f05` | ouvir-achar | ouve "bê" e toca na letra (B/D/P/M) | **sim — GAVETA** | nomear letra é a habilidade avaliada (2822): visível vira gabarito falante. Fechada, é a rede de quem travou |
| 7 | `f06` | classificar | separa por som do começo (BO/MA) | **não** | sílaba, não letra |
| 8 | `f11` | memória | par palavra ↔ pedaço inicial | **não** | memória exige tela limpa; 26 letras competem com as cartas |
| 9 | `f09r` | escolher | acha a rima | **não** | som do fim |
| 10 | `f02` | bater-sílabas | bate uma vez por pedaço | **não** | e há armadilha: *"não desenhar os lugares prontos"* — mais coisa fixa na tela piora |
| 11 | `f03` | juntar-sílabas | BO + LO = BOLO | **não** | o material são as sílabas, e elas já estão na bandeja |
| 12 | `f07` | bater-sílabas | idem, palavras novas | **não** | — |
| 13 | `f09` | juntar-sílabas | três pedaços | **não** | — |
| 14 | `f13` | bater-sílabas | idem | **não** | — |
| 15 | `f15` | juntar-sílabas | monta o nome da figura | **não** | — |
| 16 | `aquecimento` | escolher | retoma o que já viu | **não** | é prática de recuperação: apoio na tela é exatamente o que ela anula |
| 17 | `f17r` | intruso | rima de novo | **não** | — |
| 18 | `f18s` | **caixas de som** | uma ficha por **som** | **PROIBIDO** | regra da própria peça: *"a letra não pode aparecer durante o preenchimento"*. Aqui não é "melhor não": é não |
| 19 | `f19e` | digitar | escreve PÃO, MEL, SAL | **não — e o teclado continua reduzido** | ver §4: a peça mostra **só as letras da palavra**, embaralhadas, e cada tecla **diz a própria letra**. Trocar por A–Z inteiro seria endurecer, não apoiar |
| 20 | `f18` | traçar-letra | escreve L, A, O | **não** | mesmo motivo da 5 |
| 21 | `f25` | ouvir-achar | ouve QUEIJO e acha a letra do começo | **sim — GAVETA** | grafema-fonema é a habilidade avaliada (2817). Fechada; abre com voz para quem empacou |
| 22 | `f28` | traçar-letra | escreve S, Q, T | **não** | — |
| 23 | `f19` | classificar | separa pelo som do **fim** | **não** | — |
| 24 | `f24s` | **caixas de som** | palavras com mais sons | **PROIBIDO** | mesma regra da 18 |
| 25 | `f26` | classificar | separa por número de batidas | **não** | conta sílaba, não letra |
| 26 | `f21` | bater-sílabas | palavras compridas | **não** | — |
| 27 | `f23` | completar | falta um **pedaço** da palavra | **não** | o que falta é sílaba; alfabeto não responde |
| 28 | `f20` | juntar-sílabas | pedaços parecidos | **não** | — |
| 29 | `f22` | memória | par palavra ↔ pedaço | **não** | — |
| 30 | `f27` | juntar-sílabas | a última encomenda | **não** | — |
| 31 | `f31` | pintar-desenho | pinta a placa | **não** | autoria livre: nada a apoiar |
| 32 | `f32` | ligar-pontos | liga A→J e aparece um coração | **sim — PRESENTE** | a própria fase diz *"não tem pressa e não tem erro"*. Não há nota a proteger, e é o fecho: a fita à vista, falante, é presente e é revisão |

**Placar:** 5 fases ganham o alfabeto (2, 4, 6, 21, 32), em três formas
diferentes; 2 o proíbem (18, 24); 25 não ganham nada — e é essa maioria que
responde à pergunta do Marcos.

---

## 4. Como entraria — o desenho, item por item

### O ARCO (fase 2, `f04`)

- Meio círculo com **26 lugares vazios**, não uma fileira. A criança arrasta as
  letras da bandeja para os lugares — o arco é a **bancada**, e o que ela põe é
  o que ela sabe.
- A fase de hoje usa só **A–E**: o arco começa mostrando o trecho de A a E e
  cresce se o conteúdo crescer. Arco de 26 vagas com 5 peças é vazio demais e
  assusta.
- Isto **não é ideia nova**: já está escrito na `RECEITA.md` como pendência
  (*"o `ordenar` do alfabeto ganha muito trocando a fileira por um arco"*).
  Custa uma mudança na peça `ordenar.html`, que já ordena por posição na lista.

### A FITA (fases 4, 6, 21 — gaveta; e 32 — presente)

- **Um pão-letra por letra**, arte da casa (a padaria já tem `pd_l_A` … `pd_l_I`
  em `_padaria/img/`), **maiúscula**, que é como a atividade inteira escreve.
- **Fala ao tocar.** Sem voz, a fita serve só a quem já reconhece a letra — que
  é quem não precisa dela. Isto é a regra 3 dos quatro pilares.
- **Rola na horizontal com `overflow-x` próprio**, nunca fazendo a página rolar,
  e nunca ocupando altura fixa em todas as fases (o app é `position:fixed`).
- **Alvo ≥ 44 px** (`REGRAS-APRENDIZAGEM.md` §E: 44 px para quem ainda não lê;
  o portão pede 40 px como piso, e até o 2º ano sobe para 44).
- **Fechada por padrão** nas fases 4, 6 e 21: um pão-botão do lado do balão
  ("ver as letras"). Abre por toque **ou** quando o andaime chega ao 2º degrau.
- **Aberta e fixa** só na 32.
- **Abrir a fita conta como dica** no relatório do professor. Sem isso, a fita
  apaga a medição e o parecer passa a mentir — e o parecer é o que o Marcos leva
  para a sala.

### O que NÃO fazer (as três armadilhas previsíveis)

1. **Faixa permanente em todas as 32 fases.** É a leitura mais natural do pedido
   e é a pior: quebra as caixas de som, come tela e enfeita 25 fases de som.
2. **Trocar o teclado reduzido da `f19e` pelo alfabeto A–Z inteiro.** A peça
   `digitar.html` mostra de propósito **só as letras da palavra**, embaralhadas,
   cada uma dizendo a própria letra ao toque. Abrir para 26 teclas transforma
   "escrever MEL" em "achar 3 letras entre 26" — mais difícil, não mais apoiado,
   e bate de frente com *"a criança tem que conseguir passar"*.
3. **Alfabeto de fonte, em texto.** Item 6 da lista que o Marcos pegou nesta
   mesma atividade: *"a ordem do alfabeto devia ser com imagens geradas (letra
   de fonte desalinha)"*. A fita nasce em arte de IA ou não nasce.

### O que isso custa

- **Voz:** praticamente pronta. O `_padaria/falas.json` já tem **25 letras
  gravadas** (`op_3t3a` … `op_3t3z`), **todas com o mp3 em `_padaria/audio/`** —
  conferido arquivo por arquivo. **Falta uma só: o U.**
- **Arte:** existem **9 letras** em `_padaria/img/` (`pd_l_A` … `pd_l_I`), e
  elas **não estão referenciadas no `index.html`** hoje. Faltariam 17 —
  **uma cartela só**, pela regra do `_qa/cartela.py` (17 peças uma a uma seriam
  ~R$3,40 onde ~R$0,20 resolve; e peça gerada junto sai irmã das outras).
- **Código:** o arco é mudança na peça `ordenar.html`; a fita é componente novo
  do motor, usado por 4 fases.

### E o portão (senão o conserto vira o defeito seguinte)

Se a fita for implementada, ela nasce com regra medida — é a lei do §0-B da
RECEITA (*todo defeito tem conserto em duas partes*). O que dá para medir
sozinho:

- **reprovar** fita de alfabeto visível em fase com `mec` = `caixas-de-som`;
- **reprovar** fita **aberta por padrão** em fase cuja resposta certa é uma
  letra do alfabeto (`f04`, `f12`, `f05`, `f25`);
- **avisar** se a fita existir em fase cujo conceito é sílaba, rima ou fonema.

---

## 5. A resposta melhor que a pergunta — a habilidade que falta

Conferindo o currículo para responder isto, apareceu uma coisa que vale mais que
a fita: **Blumenau tem, no 1º ano, uma habilidade de alfabeto que a Padaria não
cobre** (linhas 2787–2793):

> **"Distinguir as letras do alfabeto de outros sinais gráficos."**
> *Conceitos/conteúdos: sistema alfabético de escrita, alfabeto, sinais gráficos
> (números, sinais de pontuação, emoji, entre outros).*

Os sete objetivos da atividade cobrem ordem alfabética, grafema-fonema, sílaba,
rima e fonema. **Nenhum cobre esta.** E ela é, das duas habilidades de alfabeto
do ano, exatamente aquela em que **o alfabeto visível é o próprio conteúdo** —
não apoio, não muleta: material.

**Como ela nasceria dentro da história, sem virar exercício com moldura:** a
placa de preços da padaria caiu junto com as etiquetas. Na bandeja vêm letras,
**números** (os preços), **vírgula e ponto**, um **cifrão**. O Fubá precisa
separar: *"na placa das LETRAS só vai o que é letra"*. A criança arrasta; o que
não é letra vai para a placa dos preços. É a peça `classificar`, que a atividade
já usa três vezes, com conteúdo que ela nunca teve — e resolve de uma vez a
pergunta do Marcos: **o alfabeto ganha uma fase própria, em função social,
exatamente como o texto de Blumenau exige (linha 2170), em vez de virar friso na
parede da tela.**

Não implementei, não alterei o `conteudo.json`, e não é decisão minha. Fica como
proposta para ele decidir.

---

## 6. O que eu NÃO consegui apurar (dito com todas as letras)

1. **Os códigos EF01LP.** Não existem no `_curriculo/blumenau.txt` — zero
   ocorrências em 21.208 linhas. Não colei código nenhum por cima. Para tê-los,
   é preciso baixar a BNCC (`baixar-curriculo.yml`) e casar habilidade a
   habilidade.
2. **Pesquisa primária sobre "alfabeto exposto" / *alphabet chart*.** O acervo
   de `_pesquisa/` **não tem** um estudo específico sobre alfabeto permanentemente
   visível na tela. O que existe é (a) o **Alphabet Arc** do FCRR, que é sobre o
   arco **como material de trabalho**, não como cartaz, e (b) material de loja
   (TPT) em `letras-moveis-e-caixas-sonoras.md`, que é propaganda e não vale como
   evidência. As afirmações deste parecer sobre carga cognitiva e decoração vêm
   de `REGRAS-NEUROCIENCIA.md` e `REGRAS-INTERATIVIDADE.md`, que são gerais —
   **não são medição do efeito específico de um alfabeto na tela**. Se o Marcos
   quiser lastro direto, dá para mandar o `pesquisar.yml` buscar
   *alphabet chart classroom display letter knowledge evidence* — mas a decisão
   deste parecer não depende disso: ela se sustenta na pergunta
   "ferramenta ou resposta?".
3. **Não testei nada na tela.** Não abri a atividade no navegador nem medi a
   altura que a fita ocuparia em 6 tamanhos (`_qa/leiaute.js`). A afirmação de
   que a faixa permanente custa caro em tela vem da leitura do CSS
   (`#app{position:fixed;inset:0}`), não de medição — se a fita for adiante,
   **isso tem que ser medido antes**, não presumido.
4. **Por que as 9 letras (`pd_l_A` … `pd_l_I`) existem em `img/` e não são usadas
   no `index.html`.** Não apurei se foi decisão, se ficou pela metade, ou se são
   das 26 letras em massa de pão que o item 6 do `O-QUE-O-MARCOS-PEGOU.md` diz
   estarem sendo geradas em 3 cartelas.
5. **Achado incidental, fora do meu tema:** a fase 32 tem o selo
   *"A SURPRESA DA MIGA"*, e o `_padaria/embutir.sh` recorta `pd_miga_feliz`,
   `pd_miga_fala`, `pd_miga_pisca` — enquanto o mascote da atividade é o
   **Fubá** (`pd_fuba_*`). Parece resto de um nome anterior. Não mexi; anoto
   porque é o tipo de coisa que o `_qa/clone.py` existe para pegar.
