# Parecer pedagógico — A Máquina de Juntar Palavras (1º ano)

> Degrau **5** da sequência de alfabetização (`_sequencias/ALFABETIZACAO-1ANO.md`).
> Colheita: 24 folhas reais em `_sequencias/folhas_d5/`; o crivo folha a folha
> está em `_sequencias/POTE-MONTAR.md`.
> Currículo de Blumenau, 1º ano: *"segmentar oralmente palavras em sílabas"* e
> *"construir o sistema alfabético, reconhecendo que a palavra se forma por
> sílabas"*.

## 1. O que este caderno ensina, em uma frase

Que **os pedaços se juntam e viram palavra** — e que juntar tem ORDEM (LA-BO não
é BOLA) e tem FIM (BO-LA não é BO-LO).

## 2. A escada, degrau por degrau

| Folha | O que ela pede | Por que vem aqui |
|---|---|---|
| 1 | Tocar no 1º pedaço, no 2º, e apertar JUNTAR | **Ensina, não mede.** A criança VÊ os dois pedaços correrem um para o outro e virarem uma palavra só. É a demonstração física de "juntar", e é dela que saem as outras nove |
| 2 | O pedaço que falta **no fim** (BO + ?) | O mais fácil da série: o que falta vem DEPOIS do que ela já ouviu |
| 3 | O pedaço que falta **no começo** (? + LA) e, no fim da folha, **no meio** (CA + ? + LO) | Mesmo bloco, buraco mudando de lugar. O meio é o mais alto: ela tem que segurar começo E fim ao mesmo tempo |
| 4 | Pôr **dois** pedaços embaralhados na ordem | Primeiro uso do gesto de mover |
| 5 | **Três** pedaços — e **um sobra** | Mesmo gesto, dois degraus de uma vez: mais pedaços e um que não é da palavra (sem ele, acerta-se a última vaga por eliminação, sem escutar nada) |
| 6 | **Só o ouvido**: escuta os pedaços e aponta a figura | ⭐ A síntese pura. Não há palavra escrita nem pista visual. Nenhuma folha de papel consegue fazer esta |
| 7 | Ligar a figura ao nome escrito em pedaços | Primeira vez que ela vê a palavra PARTIDA no papel (BA·NA·NA). É a ponte para a folha 9 |
| 8 | Duas palavras que começam igual (BOLA / BOLO) | Provoca de propósito o erro que faz o leitor iniciante trocar CASA por CAMA. Só quem escuta até o FIM acerta |
| 9 | **Escrever** o pedaço que falta, sem opções | O degrau mais alto, e a única folha com escrita — depois de o pedaço já ter sido ouvido oito vezes e visto escrito na folha 7 |
| 10 | O mural das palavras montadas | O fecho: a tela final mostra o que a CRIANÇA fez, e o painel vai para o relatório do professor |

## 3. As decisões que o pedagogo tomou contra a colheita

1. **Não se escreve a palavra formada.** 19 das 24 folhas de origem mandam
   escrever. Escrever é degrau posterior; cobrar aqui trocaria o que a folha
   mede (síntese silábica) por outra coisa (grafia). A escrita entra uma vez só,
   na folha 9, e de um pedaço, não da palavra.
2. **Nada de encontro consonantal** (PLA, CLA, BLO). A folha d10 pedia isso;
   sílaba com dois sons colados é degrau depois do CV simples, e misturar faz a
   criança errar por uma razão que não é a que a folha mede.
3. **Nada de cursiva** (d06, d23). Outro objetivo, e no 1º ano ainda é caixa alta.
4. **A folha d17** ("junte as LETRAS, depois as sílabas") foi **reposicionada
   para o degrau 6/7**, não descartada: ela começa na letra.
5. **A folha 7 liga ao nome inteiro em pedaços, não à sílaba final** (como pedia
   a d12). No 1º ano a sílaba final sozinha não identifica figura nenhuma: DO
   serve a DADO e a TUDO, e a criança acertaria por sorte.

## 4. A voz — e por que ela É o conteúdo aqui

Juntar pedaços é operação de OUVIDO. Todo pedaço que o caderno fala é
**recortado da palavra inteira** por alinhamento forçado
(`_padrao/silabas_voz.py`, modelo MMS): a criança ouve VA na voz, no ritmo e na
altura de VACA.

⚠️ **O beco que já custou três rodadas** (set/2026, o Marcos ouviu): mandar o
sintetizador ler a sílaba SOLTA nunca fecha, porque ele não lê som, lê PALAVRA —
e "VA" sozinho ele SOLETRA ("vê-á"). Não adianta escrever "como se fala": a
MESMA sílaba escrita tem sons diferentes conforme a palavra (BO é [bɔ] em BOLA e
[bo] em BOLO). São **36 palavras e 100 recortes** neste caderno, e o portão
`_qa/silabas.py` reprova a publicação se faltar um.

Além disso: **alto-falante em tudo** (enunciado, nome da figura, cada pedaço,
cada opção). No 1º ano metade da turma ainda soletra; sem a voz, a criança
responde pelo desenho e a folha vira loteria.

## 5. Avaliação

- **Boletim da criança**: estrelas, barras e "Você já ..." — sem nota, sem
  porcentagem e sem a palavra "errou". O currículo de Blumenau diz que *"mostrar
  o que sabe ou o que não sabe é pertinente, faz parte do crescimento e não da
  exclusão"*.
- **Relatório do professor** (invisível para o aluno, abre segurando a medalha
  2 segundos): 7 objetivos, acertos de primeira × com ajuda, parecer descritivo
  em palavras e nota de 0 a 10 (1,0 de primeira; 0,6 com ajuda).
- **Os 7 objetivos**: juntar dois pedaços · achar o pedaço que falta (fim,
  começo, meio) · pôr na ordem · juntar só de ouvido · reconhecer a palavra
  escrita em pedaços · escutar até o fim · escrever o pedaço.

## 6. Medidas

| | |
|---|---|
| Duração estimada | **40 a 52 min** (piso 40, aula 55) — `_qa/duracao.py` |
| Itens por caderno | 79 |
| Palavras / figuras | 36, todas do banco |
| Recortes de voz | 100, em 36 palavras |
| Peso | index 95 KB · imagens 2,1 MB |
| Jogado até o fim | sim, no navegador: 79/79, relatório abriu, sem erro de JS |
| Leiaute | `_qa/leiaute_mao.js` em 6 tamanhos: nenhuma figura cortada, alvos ≥ 40 px |

## 7. O que este caderno deixa para o próximo

- A folha **d17** (letra → sílaba → palavra) espera o degrau 6/7.
- A folha **d19** (formar 10 palavras livremente a partir de um banco) espera o
  degrau 8, quando a escrita já estiver de pé.
- **"Pinte as sílabas que formam o nome"** (d14, d21) é a primeira candidata a
  folha extra, se o Marcos quiser uma a mais.
