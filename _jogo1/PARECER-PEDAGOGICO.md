# Parecer pedagógico — O Grande Jogo das Palavras (1º ano)

> Degrau **8** e ÚLTIMO da sequência de alfabetização
> (`_sequencias/ALFABETIZACAO-1ANO.md`). É o caderno de **revisão**: o único que
> não sobe um degrau novo, porque volta e passa por todos.
> Currículo de Blumenau, 1º ano: retoma os objetivos **A** a **F** de uma vez.

## 1. O que este caderno faz, em uma frase

Faz a criança **usar de novo**, em forma de jogo, os sete degraus que ela subiu —
e é justamente o "usar de novo, depois de um tempo" que fixa (prática de
recuperação e revisão espaçada: Roediger, Bjork).

## 2. Cada folha revisa um degrau — e nenhuma repete o gesto de lá

| Folha | Jogo | Revisa | Por que o gesto MUDA |
|---|---|---|---|
| 1 | **Memória das rimas** | degrau 1 (rima) | Lá ela escolhia a palavra que rima; aqui ela precisa GUARDAR onde a carta estava e comparar o fim de duas palavras de cabeça |
| 2 | Quantas palmas? | degrau 2 (sílaba) | Lá havia a fileira de pedaços para tocar; aqui só a figura, a voz e o número |
| 3 | Quem começa igual? | degraus 3 e 4 (começo) | Lá o alvo vinha escrito; aqui são duas figuras e nada escrito |
| 4 | **Caça-palavras** | degraus 5 e 6 (a palavra escrita) | Lá a palavra estava montada ou com um buraco; aqui ela está ESCONDIDA no meio de outras letras |
| 5 | **A forca do balão** | degrau 6 (a letra) | Lá a palavra estava à vista com um buraco; aqui ela está inteira escondida e a criança precisa ARRISCAR |
| 6 | Monte o nome com as letras | degrau 6 | O mesmo gesto do degrau 6, de propósito: é a âncora que mostra que ela ainda sabe |
| 7 | Corte a frase | degrau 7 | Idem |
| 8 | Ligue a figura à frase | degrau 7 | Idem |
| 9 | **Escreva o nome inteiro** | tudo | ⭐ A folha mais alta da sequência inteira: sem opções, sem letras dadas, sem buraco. Só a figura, a voz e o teclado |
| 10 | O mural do campeão | — | O fecho de oito cadernos, não de um |

## 3. Os três clássicos que entram aqui — e por quê

O Marcos nomeou, em agosto: *"completar lacunas, digitar resposta, **forca**,
**memória**, **caça-palavras**, cruzadinha, quiz, simuladores…"*. Três deles a
sequência ainda não tinha usado, e o lugar deles é este — **porque jogo que
revisa precisa ser jogo**, senão a revisão vira prova disfarçada.

E nenhum entrou por enfeite: cada um mede um degrau anterior por um caminho que
nenhuma folha anterior usava (ver a tabela acima).

### ⚠️ Três decisões dentro dos três jogos

1. **Na memória, o par NÃO é a carta igual: é a carta que RIMA.** Memória de par
   idêntico não ensina nada de língua — treina memória visual. Assim ela tem que
   dizer as duas palavras na cabeça e comparar o FIM, que é o degrau 1 inteiro.
   ⚠️ E o crivo do montador confere uma coisa que passa fácil: **duas palavras de
   PARES diferentes não podem rimar entre si**, senão a criança casa certo e o
   app diz errado. (Pegou de verdade: VELA e PANELA rimavam com BOLA e MOLA no
   mesmo tabuleiro.)
2. **No caça-palavras, só HORIZONTAL e VERTICAL** — nunca diagonal nem de trás
   para frente. No 1º ano a criança ainda está firmando a direção da leitura, e
   palavra ao contrário ensina o oposto do que o ano inteiro ensinou. E ela toca
   na primeira e na última letra: arrastar numa grade exige mira fina, e o dedo
   de seis anos escorrega. ⚠️ O crivo também confere que **a palavra não aparece
   duas vezes na grade** — senão ela acha a outra e o app diz errado.
3. **Na forca, ninguém é enforcado.** O desenho da forca é violento e não tem
   nada a ver com o conteúdo: aqui o que desce a cada erro é um **balão**, e com
   seis erros ele pousa. A criança perde a rodada, não um boneco. ⚠️ E pousar
   **não trava a folha**: a palavra se revela, a voz a diz sem nenhuma palavra de
   derrota, e ela segue — deixá-la presa num item seria beco sem saída.
   ⚠️ A figura fica à vista desde o começo: sem ela, a criança que ainda não lê
   chuta letra no escuro e a folha vira loteria. Com ela, a tarefa é a certa —
   *"eu sei que palavra é; agora, quais são as letras dela?"*.

## 4. A voz

Em cada acerto ela **diz de qual degrau aquilo veio** ("as duas acabam igual —
isso é RIMA", "as duas começam com o mesmo pedaço"). Revisão que não diz o nome
do que está revisando vira só mais uma rodada de exercícios.

Sem recorte de sílaba: o caderno fala palavra e frase inteiras, e o
`silabas.json` sai vazio de propósito (o portão `_qa/silabas.py` confere).

## 5. Avaliação — e o que ela serve ao professor

O relatório tem **7 objetivos nomeados POR DEGRAU** ("Rima (degrau 1)",
"Pedaços da palavra (degrau 2)"…). Isso é de propósito: quando a criança trava,
a tabela diz **a qual caderno voltar**. É o único relatório da sequência que
funciona como diagnóstico do caminho todo.

E o parecer, quando nada chegou a 75%, não manda insistir aqui: manda **voltar ao
degrau em que ela travou**.

## 6. Medidas

| | |
|---|---|
| Duração estimada | **32 a 43 min** pelo estimador — na prática mais, porque ele não sabe cobrar o preço de um tabuleiro de memória nem de uma grade de caça-palavras |
| Itens por caderno | 66 |
| Palavras / figuras | 51, todas do banco |
| Frases | 17, das do degrau 7 |
| Recorte de voz | nenhum, de propósito |
| Peso | index 106 KB · imagens 2,8 MB |
| Jogado até o fim | sim, no navegador: 66/66, relatório abriu, sem erro de JS |
| Leiaute | `_qa/leiaute_mao.js` em 6 tamanhos: nenhuma figura cortada, alvos ≥ 40 px |
| Carta de memória | fluida, mínimo 130 px de largura e 118 de altura (piso da casa: 130 × 88) |

## 7. O que ficou de fora, e onde está guardado

- **d17 do degrau 6** ("junte as LETRAS, depois as SÍLABAS, e forme a palavra"):
  atravessa dois degraus de uma vez e seria o 11º jogo. Fica anotado como a
  primeira candidata se o Marcos quiser uma folha a mais aqui.
- **d19 do degrau 7** (formar frases livremente, escrevendo): produção aberta
  exige correção do professor — não cabe numa folha que se corrige sozinha.
