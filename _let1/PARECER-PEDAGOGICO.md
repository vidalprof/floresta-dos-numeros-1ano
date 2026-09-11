# Parecer pedagógico — A Letra que Muda Tudo (1º ano)

> Degrau **6** da sequência de alfabetização (`_sequencias/ALFABETIZACAO-1ANO.md`).
> Colheita: 24 folhas reais em `_sequencias/folhas_d6/`; o crivo folha a folha
> está em `_sequencias/POTE-LETRA.md`.
> Currículo de Blumenau, 1º ano: *"nomear as letras do alfabeto"* e *"relacionar
> elementos sonoros com sua representação escrita"*.

## 1. O que este caderno ensina, em uma frase

Que **uma letra sozinha muda a palavra inteira** — e que, por isso, ler é olhar
TODAS as letras, não só o começo.

## 2. A escada, degrau por degrau

| Folha | O que ela pede | Por que vem aqui |
|---|---|---|
| 1 | Tocar em cada letra e ver a palavra mudar (_ATO → GATO, PATO, RATO) | **Ensina, não mede.** Manipulação livre antes da pergunta: não há resposta certa nem errada, só uma máquina para mexer. A folha só fecha quando ela experimentou TODAS as letras, porque é a COMPARAÇÃO entre elas que ensina |
| 2 | A letra que falta no **começo** | O começo é o que ela já caçava no degrau 4 — agora escrito |
| 3 | A letra que falta no **meio** e, no fim da folha, no **fim** | Mesmo bloco, buraco mudando de lugar. No meio e no fim não há som de abertura para ajudar: ela precisa ler |
| 4 | Duas palavras quase iguais (BOLA/BOTA, MALA/MOLA, SAL/SOL) | ⭐ **O teste do caderno.** Provoca de propósito o hábito de ler "por cima". Só acerta quem olha a letra que muda |
| 5 | Marcar **todas** as figuras cujo nome tem esta letra | Marcar várias é outro gesto: em vez de comparar duas opções, ela VARRE o conjunto e decide item por item — inclusive decidir que alguns NÃO são |
| 6 | Montar o nome da figura com as letras fora de ordem | O gesto do degrau 5, com a peça menor: com sílabas eram dois pedaços; com letras são quatro |
| 7 | Idem, com **uma letra a mais** que sobra | Sem a intrusa, a última vaga se resolve por eliminação e ela não olha letra nenhuma |
| 8 | Ligar a figura ao nome escrito, entre três nomes quase iguais | Três em cima da mesa, e não dá para decidir pela primeira letra |
| 9 | **Escrever** a letra que falta, sem opções | O degrau mais alto, e a única folha com escrita |
| 10 | O mural das palavras | O fecho: a tela final mostra o que a CRIANÇA fez |

## 3. As decisões que o pedagogo tomou contra a colheita

1. **Um buraco por palavra, sempre.** Oito das 24 folhas de origem pedem várias
   letras de uma vez (`C_MEL_`, `B_N_N_`, `P_T_C_`). Parece a mesma tarefa e não
   é: com quatro buracos a criança erra por CARGA, não por não saber a letra.
2. **Os distratores formam outra palavra de verdade** (`_ATO` com G, P e R). Isso
   é de propósito: as três respostas estão certas como palavra, e quem decide é a
   FIGURA. Distrator que não forma nada deixaria acertar por eliminação.
3. **A folha 8 não escreve o nome ao lado da figura.** Com o nome ali, "ligar a
   figura ao nome" vira comparar duas palavras idênticas — ela casa os desenhos
   das letras e nunca precisa saber o que a figura é. O andaime honesto é o
   alto-falante.
4. **A folha 9 não traz a palavra-modelo** (a folha d23 trazia). Com o modelo ao
   lado, escrever vira copiar.
5. **Nada de letra pontilhada para cobrir** (d20): traçado é motricidade, outro
   objetivo.
6. **As folhas de FRASE (d19, d21) foram reposicionadas para o degrau 7/8**, não
   descartadas.
7. **A folha d17** (juntar LETRAS, depois SÍLABAS, e formar a palavra) é
   excelente — mas atravessa os degraus 5 e 6 de uma vez. Fica para o degrau 8,
   como revisão.

## 4. A voz — e por que aqui ela diz o NOME da letra

No degrau 4 dizer "bê" era o erro, porque lá o assunto era o SOM /b/. **Aqui o
assunto é a LETRA**, e o currículo pede *"nomear as letras do alfabeto"*: o nome
é como a criança vai pedir a letra ao professor e achá-la no teclado. É a mesma
palavra em dois degraus, e a ORDEM é que decide se ela ensina ou atrapalha.

Consequência boa: **este caderno não precisa de recorte de sílaba**. Nome de
letra é palavra de verdade e o sintetizador diz certo. O `silabas.json` sai vazio
de propósito, e o portão `_qa/silabas.py` confere isso sozinho.
⚠️ Mas os 26 nomes vão **escritos como se falam** ("éfe", "éle", "érre", "xis"),
um a um: mandar o TTS ler a letra "F" sozinha devolve coisa errada. É o mesmo
princípio que salvou a sílaba no degrau 5 — a voz não lê símbolo, lê palavra.

Além disso: **alto-falante em tudo** (enunciado, nome da figura, cada letra, cada
opção). No 1º ano metade da turma ainda soletra; sem a voz, a criança responde
pelo desenho e a folha vira loteria.

## 5. Avaliação

- **Boletim da criança**: estrelas, barras e "Você já …" — sem nota, sem
  porcentagem e sem a palavra "errou".
- **Relatório do professor** (invisível para o aluno, abre segurando a medalha
  2 segundos): 8 objetivos, acertos de primeira × com ajuda, parecer descritivo
  em palavras e nota de 0 a 10 (1,0 de primeira; 0,6 com ajuda).
- **Os 8 objetivos**: trocar uma letra muda a palavra · a letra do começo · a
  letra do meio e do fim · palavras quase iguais · achar a letra dentro da
  palavra · montar a palavra com letras · ler a palavra inteira · escrever a letra.

## 6. Medidas

| | |
|---|---|
| Duração estimada | **45 a 59 min** (piso 40, aula 55 — passar avisa, não reprova) |
| Itens por caderno | 70 |
| Palavras / figuras | 31, todas do banco (6 entraram só para formar par mínimo) |
| Recorte de voz | nenhum, de propósito |
| Peso | index 98 KB · imagens 1,8 MB |
| Jogado até o fim | sim, no navegador: 70/70, relatório abriu, sem erro de JS |
| Leiaute | `_qa/leiaute_mao.js` em 6 tamanhos: nenhuma figura cortada, alvos ≥ 40 px |

## 7. Dois defeitos que o contato-folha pegou (e que nenhum portão de texto via)

1. **A folha 5 perdia o NOME de quatro figuras.** A `.op.fig` herdada punha a
   figura em 88 px fixos e deixava o rótulo escorrer 38 px para FORA do botão:
   os nomes das quatro primeiras sumiam atrás da fileira de baixo e o botão
   "Pronto" caía em cima da última. A criança lia quatro figuras sem nome numa
   folha que pede justamente para olhar o NOME. Conserto: a figura da varredura
   virou COLUNA, como já era a `.op.figbt`.
2. **A folha 8 entregava a resposta**: o nome vinha escrito ao lado da figura, do
   lado esquerdo, e o mesmo nome do lado direito. Ver o item 3 acima.

## 8. O que este caderno deixa para o próximo

- **d19 e d21** (frase) esperam o degrau 7 — espaços entre palavras.
- **d17** (letras → sílabas → palavra) espera o degrau 8, como revisão que
  atravessa os dois degraus.
