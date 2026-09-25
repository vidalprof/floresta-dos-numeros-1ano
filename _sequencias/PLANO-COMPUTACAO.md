# 💻 COMO ENSINAR O CURRÍCULO DE COMPUTAÇÃO DE BLUMENAU

> Pergunta do Marcos (25/set/2026): ***"que ferramenta ou método eu poderia criar
> para ensinar computação, esse currículo? pq meu objetivo era utilizar essas
> atividades que desenvolvemos — a de antes, modo broto, ou essa folha viva —
> para criar sequências didáticas para o currículo de computação"***.
>
> Este documento responde as duas coisas: **qual ferramenta** (e são duas peças
> novas, não um programa novo) e **qual método** (o roteiro de 13 etapas do
> `SEQUENCIAS-DIDATICAS.md`, com três adaptações que a Computação obriga).
>
> **Fonte única dos objetivos:** `_curriculo/computacao-blumenau.txt` — o EBOOK
> que o Marcos enviou, 76 páginas, Educação Infantil ao 9º ano, guardado em
> 25/set/2026. É dali que sai a citação **verbatim** que o portão `0b9` confere
> palavra por palavra. ⚠️ **O `0b9` ainda não abre este arquivo** (só o
> `blumenau.txt`): até aprender, caderno de Computação dirá *"NÃO MEDI"*, que
> não é *"passou"*.

---

## §0 A RESPOSTA EM SETE LINHAS

1. **O modelo é a FOLHA VIVA**, não o motor — §1 diz por quê.
2. **Duas peças novas no motor, e só duas:** a **BANCADA QUE EXECUTA** (a criança
   monta a sequência e algo a cumpre na frente dela) e o **SIMULADOR DE TELA**
   (uma tela digital de faz-de-conta — navegador, área de trabalho, conversa —
   onde ela age e a tela reage).
3. ⚠️ **ISTO ESTAVA ERRADO E FOI CORRIGIDO — ver §4.2.** Eu escrevi aqui *"um
   caderno por ano cobre o ano inteiro"*. **Não cobre:** um caderno de 35 folhas
   dura ~30 minutos, que é o bloco de máquina de **UMA aula**. Um ano são ~40
   aulas de 55 min. O certo é **um caderno por SEQUÊNCIA** (~9 no ano), cada um
   com uma etapa por aula.
4. **20 dos 41 objetivos de 1º a 5º ano** já são alcançados pelos gestos que a
   folha viva **tem hoje** — zero engenharia nova.
5. **A bancada carrega 10, o simulador 8, e os 3 que restam são a Oficina de
   Vídeo, que já está no ar.** ⭐ **Total: 41 de 41 em atividade digital, sem
   nenhuma aula desplugada** — que é a condição que o Marcos pôs em 25/set/2026:
   ***"teria que dar aula de computação, mas não quero realizar o desplugado...
   gostaria de alcançar todo esse currículo em atividades digitais, para
   convencer minha coordenadora de computação"***.
6. **O piloto é o 3º ano** — §5 diz por quê. E o que a coordenadora recebe como
   prova está no **§7**.
7. **Limite declarado: isto vale até o 5º ano.** Do 6º ao 9º o currículo diz
   *"usando uma linguagem de programação"* sete vezes, e bloco não cumpre isso.

---

## §1 POR QUE FOLHA VIVA, E NÃO O MOTOR

O Marcos perguntou entre os dois modelos que a casa tem. A resposta é folha viva,
por três razões que vêm do **formato do currículo**, não do meu gosto:

- **O currículo de Computação é uma LISTA de objetivos por ano** (7 no 1º, 6 no
  2º, 9 no 3º, 8 no 4º, 11 no 5º). O relatório do professor da folha viva casa
  **objetivo → folhas que o medem**, um a um — que é exatamente o que o portão
  `0b9` confere. No motor, a fase é grande e mede várias coisas ao mesmo tempo;
  amarrar objetivo a fase ficaria frouxo.
- **Três eixos cabem em três blocos de folhas.** A regra da casa manda mecânica
  que repete vir em **BLOCO**, colada, subindo degrau (senão volta o *"isso eu já
  fiz"*). Os três eixos dão os três blocos naturalmente.
- **35 folhas absorvem 6 a 11 objetivos com folga**; 20 fases de motor, não.

⚠️ **O que o motor tem e a folha viva não:** um MUNDO, com mascote e missão — o
*"o mundo precisa"* da filosofia. Em Computação isso sai de graça: **o executor É
o mundo**. O robô que precisa atravessar, a máquina que precisa montar a palavra,
a planta que precisa crescer na ordem certa. Não falta enredo; ele vem com a
peça nova.

---

## §2 AS DUAS PEÇAS NOVAS — e por que exatamente duas

Cada eixo tem uma **natureza de verbo** diferente, e é o verbo que diz se o gesto
já existe ou não.

### 2.1 🤖 A BANCADA QUE EXECUTA (eixo Pensamento Computacional)

**O verbo é "criar e SIMULAR".** De 2º a 5º ano o objetivo não pede ordenar os
passos: pede *"criar e **simular** algoritmos"*. Uma folha de ordenar põe a
criança em ordem e diz se acertou — ela não faz os passos **acontecerem**. Sem
execução, metade do verbo fica de fora, e o melhor da aula desaparece: **o robô
bate na parede e a criança descobre onde errou.**

E o currículo pede esse erro com todas as letras — 2º ano: *"analisando como a
precisão da instrução impacta na execução do algoritmo"*. **É a filosofia da casa
escrita dentro do currículo:** o problema primeiro, a palavra "algoritmo" por
último.

**A anatomia da peça:** tela dividida. De um lado o **leque de blocos** daquela
folha (só os que aquela folha precisa — carga cognitiva, uma ideia por tela); do
outro o **palco** com o executor e o botão RODAR. Passo a passo visível: o bloco
que está sendo cumprido **acende**. No fim, sucesso ou o lugar exato onde parou.

⭐ **E O EXECUTOR NÃO PRECISA SER ROBÔ — é a mesma peça com pele diferente.**
É isso que faz a ferramenta servir também às disciplinas normais, que era o
pedido original do Marcos:

| Pele | Serve a | O que o executor faz |
|---|---|---|
| robô na grade | Computação, Matemática (coordenadas), Geografia (mapa, rosa dos ventos) | anda, gira, sente parede |
| máquina de palavras | alfabetização, ortografia | junta sílabas na ordem dada |
| receita / experimento | Ciências | cumpre etapas, e fora de ordem dá errado |
| dançarino / boneco | Arte, Ed. Física | repete a sequência de movimentos |

⚠️ **Um leque por folha, nunca o leque inteiro.** O 1º ano vê `andar` e `girar`.
O `repetir` só aparece na folha em que ele é o assunto. Leque cheio na folha 3 é
carga cognitiva jogada na criança.

⚠️ **Os blocos são ARRASTAR — logo valem as duas portas** (arrastar com o mouse
**e** tocar com o dedo) e o piso de **40 px** no alvo. Este é o gesto que já
custou dois consertos na casa; não se reescreve, se copia do que já funciona.

### 2.2 🖥️ O SIMULADOR DE TELA (eixos Cultura Digital e Mundo Digital)

**É esta peça que faz o currículo inteiro caber em atividade digital**, e ela
nasceu de uma exigência do Marcos: nada de desplugado, e nada de objetivo
entregue *"para o professor resolver com o projetor"*.

**O verbo é "utilizar", "acessar criticamente", "demonstrar postura",
"reconhecer o impacto".** São verbos de **fazer dentro de um ambiente digital** —
e é por isso que nem folha nem bancada os alcançam: a folha pergunta, a bancada
executa um programa, mas nenhuma das duas **é uma tela de computador de verdade
onde a criança mexe**.

**A peça:** uma **tela digital de faz-de-conta**, desenhada por nós, com conteúdo
FIXO e escrito por nós. A criança age — clica, digita, escolhe, arrasta — e a
tela **reage mostrando o que aconteceu**. Depois ela **pode voltar e tentar o
outro caminho**, porque o objetivo é ver a diferença, não ser reprovada.

⭐ **Uma peça, várias peles — e cada pele resolve objetivos que pareciam perdidos:**

| Pele | Objetivos que ela alcança |
|---|---|
| **navegador de faz-de-conta** (barra de endereço, aba, voltar, busca) | *"utilizar diferentes navegadores e ferramentas de busca"* (3º) · *"verificar a confiabilidade das fontes"* (4º) · *"acessar informações na Internet de forma crítica"* (5º) |
| **área de trabalho de faz-de-conta** (abrir programa, janela, pastas) | *"necessidade de um sistema operacional"* (5º) · *"dados em dispositivo local ou remoto"* (5º) |
| **conversa / mural de faz-de-conta** | *"impacto do compartilhamento de informações pessoais"* (3º) · *"uso seguro e proteção de dados pessoais"* (1º) · *"cuidados de segurança no uso de dispositivos"* (2º) |
| **página com uma imagem e a sua licença** | *"direitos autorais em diferentes mídias digitais"* (5º) · *"postura ética na coleta, guarda e uso de dados"* (4º) |

⭐⭐ **E O BUSCADOR DE FAZ-DE-CONTA RESOLVE O MEDO QUE O MARCOS JÁ TINHA
DECLARADO.** Nesta mesma semana ele mandou tirar a busca da Oficina de Vídeo:
***"meu medo é digitarem algo impróprio no campo busca"***. Estava certo — e a
saída não é abrir mão do objetivo, é **a busca não ser de verdade**: a criança
digita e recebe os resultados que NÓS escrevemos. Três ganhos de uma vez:
· **risco zero** de conteúdo impróprio, porque não há internet do outro lado;
· **funciona sem depender do wi-fi** da escola, que ele já disse ser ruim;
· e **ensina melhor**, porque os resultados podem ser desenhados para conter
exatamente o contraste da aula — uma página confiável e uma que não é, lado a
lado, o que a internet de verdade não entrega sob encomenda.

⚠️ **Nunca punir e nunca moralizar.** Sem placar, sem "errou", sem carinha triste.
A consequência é informação, igual ao robô que bate na parede. O risco aqui é a
peça virar **prova disfarçada** com cara de quiz de moral (*"é certo ou errado
compartilhar?"*), que o Portão 0 proíbe.

⚠️ **É desenho novo, não clone.** Diferente da bancada, aqui não há mecânica
parecida na casa para copiar. É a parte mais arriscada do plano e deve ser feita
**uma vez, num caderno só**, medida, e só depois repetida.

### 2.3 🧰 O QUE NÃO PRECISA DE PEÇA NENHUMA (eixo Mundo Digital, e mais)

Os verbos são **reconhecer, diferenciar, relacionar, codificar** — e para cada um
a folha viva já tem o gesto pronto, com armadilhas já pagas:

- hardware × software, dado × informação, local × remoto → **classificar em gavetas**
- componentes do computador → **ligar** peça ↔ função
- binário, ASCII, RGB → **escrever/decodificar** (fileira de lâmpadas acesas e
  apagadas; mesa de mistura de três cores). ⭐ São as folhas mais bonitas do
  caderno e as mais baratas de fazer: gesto de digitar, que já existe.
- adequação da tecnologia ao problema → **escolher** com alto-falante

---

## §3 O MAPA DOS 41 OBJETIVOS (1º ao 5º ano)

**Quem alcança:** `FOLHA` = gesto que a folha viva já tem · `BANCADA` = a peça
2.1 · `SIMUL.` = o simulador de tela, peça 2.2 · `OFICINA` = a Oficina de Vídeo,
que já está no ar. **Nenhuma linha diz "aula desplugada" e nenhuma diz "fica com
o professor".**

⚠️ **Esta coluna é a MINHA leitura, objetivo por objetivo — não é medição de
portão.** O texto verbatim de cada objetivo está no
`_curriculo/computacao-blumenau.txt`; aqui vai o verbo e o objeto, para caber.

### 1º ano — 7 objetivos

| Eixo | Objetivo (resumido) | Gesto | Quem |
|---|---|---|---|
| PC | organizar objetos por características, explicitando padrões e diferenças | classificar | FOLHA |
| PC | identificar e **seguir** sequências de passos do dia a dia | rodar a sequência | BANCADA |
| PC | reorganizar e criar sequências, ligando-as à palavra "Algoritmos" | montar e rodar | BANCADA |
| MD | reconhecer o que é informação: armazenada, transmitida, em várias linguagens | classificar / ligar | FOLHA |
| MD | representar informação usando diferentes codificações | decodificar | FOLHA |
| CD | reconhecer e explorar artefatos computacionais para necessidades | ligar artefato ↔ necessidade | FOLHA |
| CD | conhecer o uso seguro para proteger dados pessoais e a própria segurança | decidir e ver | CENA |

### 2º ano — 6 objetivos

| Eixo | Objetivo (resumido) | Gesto | Quem |
|---|---|---|---|
| PC | criar e comparar modelos de objetos, identificando padrões e atributos | montar / comparar | FOLHA |
| PC | criar e **simular** algoritmos com **repetições simples**, vendo como a precisão da instrução impacta | montar e rodar | BANCADA |
| MD | identificar que **máquinas diferentes executam conjuntos próprios de instruções** | dois executores, dois leques | BANCADA |
| MD | diferenciar hardware e software | duas gavetas | FOLHA |
| CD | reconhecer características e usos das tecnologias no cotidiano | classificar | FOLHA |
| CD | reconhecer os cuidados de segurança no uso de dispositivos | decidir e ver | CENA |

⭐ **Repare no terceiro:** é objetivo de **Mundo Digital** alcançado pela
**bancada** — duas máquinas com leques de blocos diferentes, e a mesma tarefa
resolvida de dois jeitos. Eixo não decide peça; **verbo decide peça.**

### 3º ano — 9 objetivos

| Eixo | Objetivo (resumido) | Gesto | Quem |
|---|---|---|---|
| PC | associar verdadeiro/falso a sentenças lógicas, **com negação** | escolher V/F | FOLHA + BANCADA |
| PC | aplicar **decomposição**: dividir, resolver as partes, combinar | sub-rotina | BANCADA |
| PC | criar e simular algoritmos com **repetição condicional** (iteração indefinida) | montar e rodar | BANCADA |
| MD | relacionar informação com dado | classificar | FOLHA |
| MD | compreender que dados são estruturados em formatos específicos | classificar | FOLHA |
| MD | diferenciar hardware e software | duas gavetas | FOLHA |
| CD | utilizar navegadores e ferramentas de busca | navegador de faz-de-conta | SIMUL. |
| CD | usar ferramentas computacionais para se expressar em formatos digitais | editar um vídeo | OFICINA ✅ |
| CD | reconhecer o impacto do compartilhamento de informações pessoais | decidir e ver | CENA |

⚠️ **O da busca esbarra numa decisão do próprio Marcos**, desta semana, quando
mandou tirar o buscador da Oficina de Vídeo: *"meu medo é digitarem algo impróprio
no campo busca"*. Esse objetivo é **do professor com o projetor**, não de
atividade solta — e dizer isso é mais honesto que fingir que a folha alcança.
✅ **O de se expressar em formatos digitais JÁ ESTÁ PRONTO: é a Oficina de Vídeo**
(https://vidalprof.github.io/a-oficina-de-video/).

### 4º ano — 8 objetivos

| Eixo | Objetivo (resumido) | Gesto | Quem |
|---|---|---|---|
| PC | objetos representados por **matrizes** (coordenadas), com manipulações | a grade É a matriz | BANCADA + FOLHA |
| PC | objetos representados por **registros** (componente com nome) | preencher fichas | FOLHA |
| PC | criar e simular algoritmos com **repetições aninhadas** | montar e rodar | BANCADA |
| MD | entender que guardar/transmitir dados exige codificá-los em formato digital | classificar | FOLHA |
| MD | codificar informações: **binária, ASCII, atributos de pixel (RGB)** | digitar / misturar | FOLHA ⭐ |
| CD | usar ferramentas para criação de conteúdo (textos, apresentações, vídeos) | editar um vídeo | OFICINA ✅ |
| CD | demonstrar postura ética na coleta, guarda e uso de dados | decidir e ver | CENA |
| CD | reconhecer a importância de verificar a **confiabilidade das fontes** | comparar duas páginas | CENA |

### 5º ano — 11 objetivos

| Eixo | Objetivo (resumido) | Gesto | Quem |
|---|---|---|---|
| PC | objetos representados por **listas** (nº variável de itens em sequência) | fila que cresce | FOLHA |
| PC | objetos representados por **grafos** (vértices e arestas) | o labirinto É o grafo | BANCADA |
| PC | negação, conjunção e disjunção sobre sentenças lógicas | escolher / bloco de condição | FOLHA + BANCADA |
| PC | criar e simular algoritmos com **seleção condicional** | montar e rodar | BANCADA |
| MD | reconhecer dados armazenados em dispositivo local ou remoto | classificar | FOLHA |
| MD | identificar os componentes do computador (entrada/saída, processador, armazenamento) | ligar | FOLHA |
| MD | reconhecer a necessidade de um **sistema operacional** | ordenar / escolher | FOLHA |
| CD | acessar informações na Internet distinguindo confiável de não confiável | decidir e ver | CENA |
| CD | usar informações considerando **direitos autorais** | decidir e ver | CENA |
| CD | expressar-se crítica e criativamente sobre as mudanças tecnológicas no trabalho | produzir um vídeo | OFICINA ✅ |
| CD | identificar a adequação de diferentes tecnologias na resolução de problemas | escolher | FOLHA |

### O placar

| Quem alcança | Objetivos | Engenharia |
|---|---|---|
| **FOLHA** (gestos de hoje) | **20** | nenhuma |
| **BANCADA** (peça 2.1) | **10** | uma peça, muitas peles |
| **SIMUL.** (peça 2.2) | **8** | uma peça, desenho novo |
| **OFICINA DE VÍDEO** | **3** | ✅ já está no ar |
| **total** | **41 de 41** | **tudo em atividade digital** |

⚠️ **Duas correções registradas, e as duas vieram de ele perguntar de novo:**
· Em conversa eu havia estimado *"~32 folha, ~6 robô, ~3 ferramenta"*. Era
estimativa **por eixo**, e estava errada para menos: as peças novas carregam
**18 de 41**, não 6. *Estimativa por eixo não substitui leitura objetivo por
objetivo* — e a diferença muda o tamanho do investimento.
· E eu havia dado um objetivo (o do navegador, 3º ano) como **"fica com o
professor e o projetor"**. Era desistência disfarçada de conclusão: o Marcos
respondeu que não quer desplugado nem aula em sala, e a saída existia e era
melhor — **o navegador de faz-de-conta**. *Quando eu entrego um objetivo "para o
professor resolver", quase sempre é porque não procurei a peça.*

---

## §4 O MÉTODO — o roteiro de 13 etapas, com três adaptações

O caminho é o do `SEQUENCIAS-DIDATICAS.md §0`, inteiro, sem atalho. O que a
Computação muda:

### 4.1 A colheita FUNCIONA — e o papel NÃO chega à criança

⚠️⚠️ **ANTES DE TUDO, A CONFUSÃO QUE TEM DE FICAR DESFEITA.** Colher folha de
papel é etapa do **meu** trabalho, não da aula. O Marcos foi explícito em
25/set/2026: ***"não quero realizar o desplugado, dando aula em sala"***. A folha
de papel é a minha **matéria-prima** — dela eu leio o comando impresso (que
escolhe o gesto) e dela eu recorto a figura. **O que chega à criança é sempre a
tela.** Nenhuma folha é impressa, nenhuma aula é desplugada.

*E por que não abrir mão da colheita, então?* Porque quando eu escolho a mecânica
só com a minha cabeça, o resultado está medido e é ruim: a Fábrica de Nomes saiu
com **84% de um gesto só** e a criança dizendo *"isso eu já fiz"*. A folha de
papel não tem esse vício — cada uma foi feita por um professor para uma aula
diferente.

A etapa 1 manda colher folhas de papel na internet e **ler o comando impresso**
para escolher o gesto. Parecia que isso quebraria em Computação. **Não quebra:**
existe muito material de **computação desplugada** em folha — grades com setas
para o robô andar, algoritmos de rotina do dia a dia, tabelas de codificação. É
a fonte ideal, porque essas folhas **já foram feitas para o papel, já têm o
comando impresso e já foram usadas em sala** — exatamente o que a regra da
origem protege.

⚠️ **Onde a colheita é magra: Mundo Digital e Cultura Digital.** Há muito menos
folha de papel sobre hardware, protocolo, dado pessoal e direito autoral. Nesses
dois eixos o gesto sai do **verbo do objetivo** e da **situação**, e isso tem de
ser dito no `POTE-<ASSUNTO>.md` com todas as letras — bloco declarado, como se
fez na moradia com os quatro que nenhuma folha cobria.

### 4.2 ⚠️ A UNIDADE É A **AULA DE 55 MINUTOS**, NÃO O CADERNO

**Este parágrafo é um conserto, e o erro era grande.** Eu tinha escrito *"um
caderno por ano cobre o ano inteiro de Computação"*. O Marcos perguntou
(25/set/2026): ***"mas vc entende que são sequências didáticas para cobrir o ano
inteiro de aulas? e cada aula dura 55 minutos?"*** — e a resposta é que **eu não
tinha entendido**. Eu dimensionei para uma ATIVIDADE e chamei de ano.

**A conta, com o número que a própria casa mediu:** o cronômetro do Marcos diz que
**20 a 25 folhas duram 30 minutos**. Então um caderno de 35 folhas é **o bloco de
máquina de UMA aula**, não de um ano.

| | |
|---|---|
| 1 aula | **55 min** |
| dentro dela, na máquina | **~30 min** (os outros 25 são chegar e ligar, o problema coletivo e o fecho — isso **é** a aula, não é desperdício) |
| 1 caderno de 35 folhas | **≈ os 30 min de máquina de uma aula** |
| objetivos do 3º ano | **9** |
| aulas no ano (1 por semana) | **~40** |
| logo, por objetivo | **~4 a 5 aulas** |

### ⭐ A ESTRUTURA CERTA, ENTÃO

> ⚠️ **CORRIGIDO PELO MARCOS na mesma conversa** — ***"serão várias sequências
> didáticas, 8 aulas para atender alguns objetivos etc"***. Eu havia posto
> *"1 objetivo em 4 a 5 aulas"*; o certo é o que ele disse:
>
> **SEQUÊNCIA DIDÁTICA = 8 aulas de 55 min, atendendo um GRUPO de objetivos.**
> **ANO = 5 sequências = 40 aulas** (com 1 aula de Computação por semana).
> **1 caderno por SEQUÊNCIA**, dividido em **8 etapas, uma por aula** — e o
> professor abre na etapa do dia pelo menu dele (senha `1275@`), que já existe.
>
> ⭐ **E os objetivos se agrupam por PARENTESCO, nunca por sobra.** A coordenadora
> vai perguntar exatamente isso: *por que estes dois juntos?* Cada par tem de ter
> resposta — e no 3º ano ela existe para os cinco (§4.2c).

### 4.2c O ANO DO 3º, sequência por sequência — 5 × 8 aulas

| # | Sequência | Objetivos | Por que estes juntos |
|---|---|---|---|
| **S1** | **Construir a máquina e mandar nela** | PC3 *(sequência, ordem, depurar)* + **MD3** *(hardware × software)* | É montando o programa que ela vê a diferença entre **as peças** e **o que está dentro delas**. Ensinar hardware/software longe da máquina é o que torna isso decorebа. |
| **S2** | **Decidir: verdadeiro, falso e o NÃO** | **PC1** *(V/F com negação)* + PC3 *(repetição com condição)* | Não existe *"repita até **não** ter parede"* sem a lógica do "não". A negação **é** a peça que faz o laço parar. |
| **S3** | **Dividir o problema** | **PC2** *(decomposição)* + **MD1** *(informação × dado)* | Dar nome a um pedaço da memória é, literalmente, transformar **dado** em **informação**. O mesmo gesto ensina os dois. |
| **S4** | **Guardar e mostrar** | **MD2** *(formatos)* + **CD2** *(expressar-se em formatos digitais)* | O formato em que ela **salva** é o formato em que ela **se expressa**. Separar os dois obrigaria a ensinar formato duas vezes. |
| **S5** | **Ligar na rede** | **CD1** *(navegador e busca)* + **CD3** *(informação pessoal)* | São a mesma porta da máquina: o que **entra** pelo cabo (e se dá para confiar) e o que **sai** (e não volta). |

✅ **9 objetivos, 5 sequências, 40 aulas.** O PC3 atravessa S1 e S2 — é o maior
objetivo do ano (*"sequências E repetições com condição"*) e não cabe honestamente
em oito aulas.

⚠️ **Com 2 aulas de Computação por semana a conta dobra**: ~80 aulas no ano, 10
sequências, e cada grupo de objetivos ganha o dobro de fôlego. **Este número tem
de vir do Marcos** — número de aula não se chuta.

⚠️⚠️ **E O PISO DE 35 FOLHAS NÃO TRANSFERE PARA COMPUTAÇÃO.** Ele nasceu da
alfabetização, onde **a folha é um exercício de ~45 segundos**. Aqui a unidade é
um **desafio**: fazer um programa funcionar leva minutos, e a criança tenta,
erra, conserta. Uma etapa de 30 minutos pode ser **6 desafios**, não 25 folhas.
**Piso por etapa, não piso único** — a mesma decisão que o Marcos já tomou para o
Pré (10 a 15 folhas em vez de 35).

⚠️ **E isso tem de ser CRONOMETRADO na turma, não estimado por mim.** O piso de 35
folhas só existe porque ele mediu a turma com o relógio na mão; o número de
desafios por etapa nasce do mesmo jeito. **Enquanto não for medido, é palpite
declarado** — e a regra da casa diz que, quando houver uma medida de sala e uma
conta minha, **a medida de sala ganha**.

### 4.2b Os três eixos, ao longo do ANO (não dentro de um caderno)

Os blocos A · B · C do §5 continuam valendo como **anatomia de uma sequência**;
o que muda é que eles se espalham pelo ano, sequência a sequência:

| Sequências | Eixo | Aulas (de ~40) |
|---|---|---|
| ~4 | Pensamento Computacional | ~18 |
| ~3 | Mundo Digital | ~11 |
| ~2 a 3 | Cultura Digital | ~11 |

⭐ **E o Marcos já escolheu por onde começar** (25/set/2026): *"acredito que eu
irei começar com pensamento computacional"* — que é também a ordem que o modelo
pede, porque a primeira sequência **constrói a máquina de vidro**, e as outras
abrem as portas dela.

A proporção segue o peso do eixo no ano, não um número fixo. E vale a regra do
leque: **nenhum gesto acima de 40%**, mínimo 4 gestos — a bancada é UM gesto, por
mais bonita que seja, então o bloco A precisa variar por dentro (montar, prever
antes de rodar, consertar uma sequência que já vem errada, ler o programa e dizer
onde para).

⭐ **"Consertar uma sequência que já vem errada" é depurar** — e é o gesto mais
barato e mais fundo do bloco A. O currículo pede isso explicitamente do 7º ano
(*"analisar programas para detectar e remover erros"*), mas a criança de 2º ano
já faz, e adora.

### 4.3 As três coisas que não mudam, e é por elas que este plano vale

- **Piso de 35 folhas** (o cronômetro do Marcos: 20–25 folhas duram 30 min).
- **`curriculo.json` com a habilidade verbatim** + `conceitos`, para o `0b9`
  medir conteúdo e não só citação.
- **`PARECER-PEDAGOGICO.md`** lido folha a folha, com o
  `python3 _qa/folha_a_folha.py <pasta>` na mesa. Em Computação isso vale mais
  ainda, porque eu não sou professor de Computação e o degrau errado aqui é
  fácil de não ver.

---

## §5 ⭐ O MODELO — **"O LABORATÓRIO"**, a anatomia das 35 folhas

> Pedido do Marcos (25/set/2026): ***"um método ou modelo de sequências didáticas
> de computação"***. Aqui está o **molde**: a casa passa a ter um terceiro modelo,
> ao lado do **motor** (atividade premium com fases) e da **folha viva** (caderno
> de 35 folhas). O Laboratório **é** folha viva — mesmo motor, mesmo relatório,
> mesma banca — com uma **anatomia fixa** e duas peças próprias.
>
> **O nome tem motivo:** a aula dele acontece no laboratório de informática, e
> cada folha é uma **bancada** onde a criança mexe numa máquina. Não é caderno de
> exercício sobre computador: é o computador sendo operado.

### 5.1 A anatomia (35 folhas, três blocos + fecho)

**A ordem dos blocos não é arbitrária: é a filosofia da casa.** O problema vem
primeiro, a criança sente a falta, e **o conceito chega por último**. Em
Computação isso é ainda mais forte porque o próprio currículo pede: 2º ano,
*"analisando como a precisão da instrução impacta na execução do algoritmo"* — ou
seja, **primeiro a instrução imprecisa dá errado, depois se fala de algoritmo.**

#### BLOCO A — A BANCADA · Pensamento Computacional · ~15 folhas

| Folhas | O que acontece | Gesto |
|---|---|---|
| A1 · 2 | **O problema, antes de qualquer conceito.** O executor precisa chegar e a criança ainda não tem como dizer como. Ela tenta, não dá, e descobre que falta uma linguagem. | tentar |
| A2 · 3 | **Uma instrução por vez**, cumprida à vista dela. O leque tem só dois blocos. | montar e rodar |
| A3 · 2 | **A sequência**: várias instruções em ordem, e a ordem importa. | montar e rodar |
| A4 · 2 | ⭐ **DEPURAR**: a sequência já vem montada e **errada**. A criança acha onde. | consertar |
| A5 · 2 | **Repetir** — quatro passos iguais viram "repita 4 vezes". | montar e rodar |
| A6 · 2 | **Decidir** — "se tiver parede, gire" (o condicional). | montar e rodar |
| A7 · 1 | **Decompor** — o pedaço que se usa duas vezes vira um bloco novo, com nome. | criar bloco |
| A8 · 1 | 🏁 **A palavra chega:** *"isto que você montou o tempo todo chama-se ALGORITMO."* | cartaz |

⚠️ **A bancada é UM gesto**, por bonita que seja, e a regra da casa proíbe um
gesto acima de 40%. Por isso o bloco A varia **por dentro**: montar · **prever
antes de rodar** (a criança diz onde o robô vai parar, depois confere) · consertar
o que veio errado · **ler o programa e dizer o que ele faz** · criar o bloco novo.
São cinco coisas diferentes na mesma peça.

⭐ **A4 (depurar) é a folha mais barata e mais fonda do caderno.** O currículo só
pede depuração explicitamente no 7º ano (*"analisar programas para detectar e
remover erros"*), mas a criança de 2º ano já faz — e é o que mais parece trabalho
de gente de verdade.

#### BLOCO B — A MÁQUINA POR DENTRO · Mundo Digital · ~10 folhas

| Folhas | O que acontece | Gesto |
|---|---|---|
| B1 · 2 | hardware × software — as duas gavetas | classificar |
| B2 · 2 | dado × informação; o dado guardado em formato | classificar |
| B3 · 3 | ⭐ **codificar**: fileira de lâmpadas (binário), mesa de mistura (RGB), tabela de símbolos | digitar / misturar |
| B4 · 2 | **onde o dado mora** — no computador ou longe (simulador de tela) | operar a tela |
| B5 · 1 | **duas máquinas, dois leques** — a mesma tarefa, instruções diferentes | montar e rodar |

⭐ **B3 são as folhas mais bonitas e mais baratas do caderno:** o gesto é digitar,
que já existe, e o efeito é imediato — a criança acende lâmpadas e sai um número,
mistura três cores e sai a cor exata. **É aqui que ela vê que a máquina é feita de
coisa simples.**

#### BLOCO C — VIVER NA TELA · Cultura Digital · ~8 folhas

| Folhas | O que acontece | Gesto |
|---|---|---|
| C1 · 2 | **o navegador de faz-de-conta**: procurar, ler o endereço, voltar, aba | operar a tela |
| C2 · 2 | **duas páginas lado a lado** — em qual dá para confiar, e por quê | comparar e decidir |
| C3 · 2 | **a conversa** — o que se conta e o que não se conta, e o que acontece depois | decidir e ver |
| C4 · 2 | **a imagem é de alguém** — de quem é, o que dá para usar | decidir e ver |

⚠️ **Este bloco é o que mais facilmente vira prova de moral**, e o Portão 0
proíbe. O teste é simples: **se a folha pergunta "é certo ou errado?", está
errada.** Ela tem de deixar a criança FAZER e mostrar o que aconteceu — e deixar
ela voltar e tentar o outro caminho.

#### FECHO — ~2 folhas

O cartaz que amarra os três eixos (o que eu mandei · do que a máquina é feita · o
que eu faço na tela) e o **gancho**: *"e o que a máquina ainda não sabe fazer?"* —
o *quero mais* que a casa exige no fim de toda atividade.

### 5.2 O que vem da folha viva sem mudar uma linha

Isto é metade do valor do modelo: **nada disso se reinventa.**

- **35 folhas** (piso medido no cronômetro: 20–25 folhas duram 30 min)
- **voz em tudo** e **alto-falante em toda opção** (`.somop`), para quem não lê
- **as duas portas**: teclado na tela **e** teclado de verdade; arrastar **e** tocar
- **continuar de onde parou por 55 minutos** (a aula), com convite que expira
- **boletim animado** sem nota e sem a palavra "errou"
- **relatório do professor** escondido (segurar a medalha 2 s) + **parecer em
  palavras** + **"treinar o que faltou"**
- **cor, capa e animação próprias** por caderno (portão `0b11`) — cinco cadernos de
  Computação não podem parecer o mesmo
- **`curriculo.json`** com a habilidade **verbatim** + `conceitos`, e o **dossiê do
  professor** dentro da atividade
- **a banca de 25 portões** (`bash _qa/auditar_folha.sh`) e o
  **`PARECER-PEDAGOGICO.md`** lido folha a folha

### 5.3 A convenção de nomes

| Ano | Pasta | Prefixo | Título |
|---|---|---|---|
| 1º | `_comp1` | `cp1_` | Aprendendo a dar instruções: sequências, informação e uso seguro |
| 2º | `_comp2` | `cp2_` | Aprendendo algoritmos com repetição, hardware e software |
| 3º | `_comp3` | `cp3_` | Aprendendo algoritmos com condição, decomposição e busca na internet |
| 4º | `_comp4` | `cp4_` | Aprendendo matrizes, repetições aninhadas e codificação (binário e RGB) |
| 5º | `_comp5` | `cp5_` | Aprendendo listas, grafos, lógica e o computador por dentro |

⚠️ **O título diz o assunto**, no vocabulário do currículo (regra do Marcos,
20/set/2026, portão `0b13`) — e é o título que a coordenadora lê primeiro.
⚠️ **Prefixo novo por caderno**, senão dois cadernos brigam pela mesma memória do
"continuar de onde parou". O `nova_folha_viva.sh` recusa prefixo repetido.

---

## §6 O PILOTO: 3º ANO — e por quê

Uma peça nova nesta casa custa historicamente **duas rodadas de conserto**. Então
a bancada e a cena nascem **num caderno só**, passam pela banca dos 25 portões,
e só depois são clonadas para os outros quatro anos.

**O 3º ano é o melhor primeiro** por quatro razões:

1. **9 objetivos, 3 por eixo** — o ano mais equilibrado dos cinco: o piloto
   exercita as três peças em peso igual.
2. **Tem o condicional** (*"repetições simples com condição"*), que é o primeiro
   robô genuinamente interessante — antes dele é só andar em linha.
3. **Tem a decomposição**, que prova a sub-rotina.
4. **Já estamos no 3º ano** (tarefa #19, quatro cadernos), então a colheita de
   figuras e a leitura do currículo daquele ano estão quentes.

**A ordem do piloto:** (a) ensinar o portão `0b9` a ler o currículo novo — meia
hora, e sem isso o caderno diz "NÃO MEDI"; (b) colher as folhas desplugadas e
**mostrar ao Marcos antes de escolher**, que é ordem dele; (c) o
`POTE-COMP3.md`; (d) a bancada numa folha só, medida, antes de 15 folhas em cima
dela; (e) o caderno inteiro.

---

## §7 OS LIMITES, DECLARADOS ANTES DE COMEÇAR

- ⛔ **Do 6º ao 9º ano isto não serve.** O currículo diz *"usando uma linguagem de
  programação"* **sete vezes** a partir do 6º ano, e *"linguagem oral, escrita ou
  pictográfica"* **quatro vezes**, todas de 2º a 5º. Bloco é o que o currículo
  pede até o 5º; do 6º em diante bloco é ponte, e o destino é a criança
  escrevendo código. Isso é outra ferramenta e outra decisão.
- ⚠️ **O objetivo do navegador/busca (3º ano) fica com o professor**, pela decisão
  do Marcos sobre campo de busca aberto para criança.
- ⚠️ **A cena de consequência não tem parente na casa** para clonar. É a parte que
  pode pedir a segunda rodada.
- ⚠️ **O portão `0b9` está cego para este currículo** até ser ensinado.
- ✅ **Máquina não é obstáculo:** os PCs da escola (FX-4300, 3,5 GB, Chrome 109)
  rodaram a Oficina de Vídeo a 60 fps. Um montador de blocos é muito mais leve.

---

## §8 ⭐ O QUE CONVENCE A COORDENADORA DE COMPUTAÇÃO

> Pedido do Marcos (25/set/2026): ***"preciso que seja algo muito bom e
> diferenciado, para convencer minha coordenadora"***.
>
> ⚠️ **E a primeira coisa honesta é esta: o que convence uma coordenadora não é
> quantidade.** Cinco cadernos meia-boca perdem para **um** caderno que ela abre,
> clica e vê funcionando, **mais o mapa dos 41 objetivos** mostrando o plano dos
> outros quatro anos. A recomendação é essa: o piloto do 3º ano acabado com
> excelência é a reunião; os outros quatro anos são o cronograma.

### 8.1 Os cinco argumentos que JÁ EXISTEM (e são os mais fortes)

Isto não precisa ser construído — está feito, e é justamente o que material de
prateleira não tem:

1. ⭐⭐ **O currículo citado é o DE BLUMENAU, verbatim, e conferido por máquina.**
   As plataformas do mercado citam a BNCC por cima. Aqui cada objetivo do
   relatório carrega a habilidade **copiada palavra por palavra** do Quadro
   Organizador do município, e o portão `0b9` **reprova a atividade** se a citação
   não existir no documento oficial, se sobrar objetivo sem folha ou folha sem
   objetivo. **A coordenadora não precisa acreditar em mim: ela confere.**
2. **O dossiê do professor mora DENTRO da atividade.** Ela abre na própria tela e
   vê objetivo → folhas que o medem → habilidade citada. Não é anexo, não é PDF
   que ninguém abre.
3. **Relatório por criança, com parecer em palavras e sem nota** — Dominou / Está
   construindo / Precisa retomar — e o botão **"treinar o que faltou"**, que refaz
   só o que ficou abaixo de 75%.
4. **Plano de aula pronto para colar.** No painel, cada atividade já entrega
   **Tema da aula** e **Objetivo** nos campos exatos da agenda on-line da escola.
   É a parte administrativa que sempre falta.
5. **Um arquivo HTML, sem instalar nada, sem conta, sem coletar dado de criança,
   rodando em Chrome 109 com 3,5 GB de RAM** — medido nos PCs da escola. Numa
   escola com wi-fi ruim e máquina de 2012 isso é o contrário do que o mercado
   oferece. ⭐ **E é argumento de Cultura Digital por si só: a ferramenta pratica
   o que ensina** — não pede dado pessoal nenhum.

### 8.2 As três coisas que ela nunca viu (o "pensar fora da caixa")

1. ⭐⭐ **A PONTE DO BLOCO PARA O CÓDIGO.** Na última folha do bloco A, ao lado da
   sequência de blocos que a criança montou, aparece **o mesmo programa escrito em
   texto**, linha por linha, acendendo junto. Ela não digita nada — só vê que o que
   ela montou **é** código. **Por que isto ganha a reunião:** o currículo vira a
   chave no 6º ano, de *"linguagem pictográfica"* para *"usando uma linguagem de
   programação"*, e material de 5º ano que **visivelmente prepara essa virada** é
   coisa que coordenador de Computação procura e não acha. E é barato: a estrutura
   dos blocos já existe, o texto é só outra forma de desenhá-la.
2. **AS DUAS MÁQUINAS.** O objetivo do 2º ano — *"máquinas diferentes executam
   conjuntos próprios de instruções"* — quase nunca é ensinado, porque é abstrato.
   Aqui a criança resolve a **mesma** tarefa em dois executores com leques
   **diferentes** de blocos, e descobre sozinha que a máquina limita o que dá para
   mandar.
3. **O BUSCADOR DE FAZ-DE-CONTA.** Ensina a procurar, ler endereço e desconfiar da
   fonte **com risco zero** e **sem depender do wi-fi** — e com os resultados
   desenhados para conter exatamente o contraste da aula, o que a internet de
   verdade não entrega sob encomenda. É a resposta técnica ao medo que o Marcos já
   tinha declarado sobre campo de busca aberto para criança.

### 8.3 O que ele leva para a reunião

| Peça | Estado |
|---|---|
| **1 caderno do 3º ano** (`_comp3`), no ar, com link | a construir — o piloto |
| **O mapa dos 41 objetivos** (§3), numa folha, com a coluna "quais folhas medem" | sai do `curriculo.json`, **gerado**, não digitado |
| **O dossiê do professor**, aberto na tela | já existe no motor |
| **A Oficina de Vídeo**, que já cobre 3 objetivos de Cultura Digital | ✅ no ar |
| **O cronograma** dos outros quatro anos | este documento |

⚠️ **O mapa tem de ser GERADO dos `curriculo.json`, não escrito à mão.** Mapa
digitado envelhece no primeiro conserto e aí passa a mentir para a coordenadora —
que é pior do que não ter mapa. Vale a mesma lição do painel: *evidência que a
máquina não mantém é evidência que ninguém mantém.*

### 8.4 O custo, dito antes

**Cinco cadernos × 35 folhas + duas peças novas não é trabalho de um dia.** A
ordem honesta é: (1) o portão `0b9` lendo o currículo novo — meia hora; (2) a
**bancada numa folha só**, medida na banca, antes de 15 folhas em cima dela;
(3) o simulador de tela, idem; (4) o caderno do 3º ano inteiro; (5) os outros
quatro anos, que aí são clonagem de molde e não invenção.

⚠️ **Peça nova nesta casa custa historicamente duas rodadas de conserto.** Por isso
as duas nascem num caderno só. Prometer os cinco anos para a mesma semana seria o
tipo de promessa que a casa já pagou caro.

---

## §9 ⭐ O QUE ELE RECEBE DE VERDADE: **O ANO PLANEJADO**, não um pacote de atividades

Quando a unidade passou a ser a **aula de 55 minutos** (§4.2), o entregável mudou
de natureza — e para muito melhor, porque é isto que responde ao pedido dele:
***"facilitar minha vida"*** e ***"convencer minha coordenadora"***.

### 9.1 A anatomia de UMA aula de 55 minutos

| Minutos | O que acontece | Onde |
|---|---|---|
| 0–5 | chegar, sentar, ligar as máquinas | a sala |
| 5–15 | **o problema**, coletivo — a máquina não faz o que se quer, e ninguém sabe ainda por quê | projetor |
| 15–45 | **a criança na máquina** — a etapa do caderno daquele dia | cada PC |
| 45–55 | **o fecho** — o que descobrimos, e o gancho para a aula seguinte | projetor |

⚠️ **Os 25 minutos fora da máquina não são desperdício: são a aula.** É onde o
problema nasce e onde a descoberta é dita em voz alta. Uma aula de informática que
é 55 minutos de clique é justamente a que cansa.

### 9.2 Os ~40 planos de aula — e eles são GERADOS

Para cada uma das ~40 aulas do ano, uma linha pronta para colar na agenda
on-line da escola, nos campos que ela tem:

- **Tema da aula** (uma linha)
- **Objetivo** (a habilidade **verbatim** do currículo de Blumenau + o que a
  criança faz nesta aula)
- **o link da etapa** do caderno
- **o que fazer nos 55 minutos** (a anatomia acima, preenchida)

⚠️⚠️ **GERADOS do `curriculo.json`, nunca digitados.** Plano digitado envelhece no
primeiro conserto e aí passa a mentir para a coordenadora — pior que não existir.
É a mesma lição do painel: *evidência que a máquina não mantém é evidência que
ninguém mantém.* O painel já faz metade disso hoje (o botão **"Plano de aula"**,
com Tema e Objetivo por atividade); o que falta é ele descer ao nível da **aula**.

### 9.3 O pacote do ano, por ano

| Peça | Quantas |
|---|---|
| sequências didáticas (1 por objetivo) | ~9 |
| cadernos (1 por sequência, em etapas) | ~9 |
| aulas planejadas de 55 min | ~40 |
| mapa de cobertura objetivo × aula | 1, gerado |

⚠️ **O número de aulas depende de quantas aulas de Computação há por semana** — com
1 por semana são ~40 no ano; com 2, ~80, e aí cada objetivo ganha ~9 aulas em vez
de ~4. **Isso muda o tamanho de cada sequência e tem de ser perguntado ao Marcos
antes de montar a primeira.** Número de aula não se chuta.

---

## §10 📋 O RELATÓRIO DESCRITIVO — **por AULA e por OBJETIVO**

> Ordem do Marcos (25/set/2026): ***"lembrando que todas essas aulas precisam ter
> um relatório descritivo, para analisar se o estudante conseguiu alcançar os
> objetivos"***.

### 10.1 O que já existe (e é mais do que parece)

Todo caderno de folha viva já traz o **relatório do professor**, escondido do
aluno (abre segurando a medalha 2 s), com **objetivo × acerto**, o **parecer em
palavras** (Dominou · Está construindo · Precisa retomar) e o **"treinar o que
faltou"**. E o motor já **guarda o que a criança fez folha a folha** — tentativas,
dicas pedidas, o que consertou. **O relatório descritivo é, em boa parte, um jeito
novo de desenhar dado que já está lá.** Isso é barato.

### 10.2 O que muda para Computação

| Hoje | Precisa ser |
|---|---|
| um relatório por **caderno** | um por **AULA** (a etapa do dia) |
| objetivo × porcentagem | objetivo × **frase que descreve o que ela fez** |
| foto de um momento | **linha do tempo do objetivo ao longo das 8 aulas** |

**A frase, e é isto que o Marcos vai ler:** não *"70%"*, e sim *"montou 5 dos 6
programas sozinha; nos dois com repetição precisou da dica uma vez cada; consertou
sem ajuda o programa que vinha errado"*. Nota nunca; **evidência sempre** — é a
regra da casa e é o que permite a ele analisar se o objetivo foi alcançado.

### 10.3 ⚠️ O OBSTÁCULO HONESTO: o motor esquece depois de 55 minutos

E esquece **de propósito**: o "continuar de onde parou" expira em 55 min porque,
passada a aula, quem senta ali é da **outra turma** e cairia no meio do trabalho de
um colega. Para a **linha do tempo das 8 aulas**, o dado tem de sobreviver entre
aulas — e não há servidor nem conta de criança. As saídas, com o custo de cada uma:

| Caminho | Funciona? | Custo honesto |
|---|---|---|
| **1. Mesma máquina** (localStorage por PC, com o nome que ela digita) | sim, **se o lugar for fixo** | de graça e imediato. **Quebra se ela trocar de computador**, e é por máquina, não por criança |
| **2. O professor copia o resultado** a cada aula | sim | 25 crianças × 8 aulas de trabalho manual — **é o contrário de "facilitar minha vida"**. Descartado |
| **3. Firebase** (a casa JÁ tem, é o da agenda) | sim, e some a fragilidade | robusto, e daria um painel com a turma inteira. **Mas é dado de criança em banco, e essa decisão é do Marcos, não minha** — inclusive porque é o próprio assunto do eixo Cultura Digital |

**Minha recomendação:** começar pelo **relatório por aula (grátis, imediato, e é o
que ele pediu)** e pelo caminho **1** para a linha do tempo. O caminho **3** só com
decisão explícita dele. ⚠️ **Não vou pôr nome de criança em banco de dados por
iniciativa própria.**

---

## §11 🔎 COLHER SEQUÊNCIAS DA INTERNET — sim, e é mais valioso aqui que colher folhas

> Pergunta do Marcos (25/set/2026): ***"é possível colher essas aulas, ou seja
> sequências da internet como folha viva, para vc ter um norte?"***

**Sim — e a diferença entre as duas colheitas importa:**

| Colher **folha** de papel | Colher **sequência didática** |
|---|---|
| dá o **comando impresso** → e dele sai o GESTO | dá a **PROGRESSÃO** → a ordem em que os conceitos entram, quantas aulas cada um leva, onde a turma trava |
| resolve *"que gesto esta folha pede?"* | resolve *"em que ORDEM se ensina isto?"* |

⭐ **E é justamente a segunda que me falta.** Gesto de bloco eu sei fazer. **Ordem
didática de Computação eu não sei** — não sou professor de Computação, e o erro de
degrau aqui é fácil de não ver. A sequência colhida é escrita por quem deu a aula:
ela traz a **ordem testada** e, o que vale ouro, **o erro clássico da turma naquele
ponto**.

**Onde procurar (e o `pesquisar.yml` já está rodando com isto):** currículos de
referência brasileiros de Computação com **plano de aula por ano e por eixo**,
material da comunidade de Computação na Educação Básica, e sequências de
pensamento computacional para os anos iniciais em português.

**O que cada sequência colhida tem de deixar registrado no
`_sequencias/POTE-COMP3.md`** — o crivo, igual ao das folhas:

1. **a fonte** e o ano a que ela se diz destinada;
2. **quantas aulas** ela usa e **quais objetivos** diz cumprir;
3. ⭐ **a ORDEM dos conceitos** — que é o que eu vim buscar;
4. **o erro que ela avisa** que a turma comete naquele ponto;
5. **o veredito:** a ordem entra · a ordem contradiz o currículo de Blumenau ·
   é aula desplugada e só serve como ordem, não como tarefa · ensina errado.

⚠️ **E o item 5 tem um filtro que vale dizer:** boa parte do material bom de
Computação para os anos iniciais **é desplugado**. Isso **não** o desqualifica —
eu colho dele a **ordem**, que é o que interessa, e a tarefa vira tela. O Marcos
não quer dar aula desplugada; isso não impede que a melhor ordem didática venha de
quem deu.

⚠️ **E antes de eu escolher qualquer coisa, ele vê o que foi colhido** — ordem dele
(15/set/2026): *"sempre me mostre as atividades que vc colheu"*.
