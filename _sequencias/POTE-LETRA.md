# O pote do degrau 6 — "a letra que falta" (o grafema)

> Folhas de origem: `_sequencias/folhas_d6/` (24 folhas colhidas da internet).
> Caderno que saiu daqui: **A Letra que Muda Tudo** (`_let1`).
> Objetivos do currículo de Blumenau, 1º ano:
>
> > **"Nomear as letras do alfabeto."**
> >
> > **"Relacionar elementos sonoros (sílabas, fonemas, partes de palavras) com
> > sua representação escrita."**

## 1. O que este degrau é — e a descoberta que dá nome ao caderno

No degrau 5 a peça era a SÍLABA: BO + LA = BOLA. Aqui ela encolhe até a menor de
todas, a LETRA. E o que a criança tem que descobrir não é "esta letra chama-se
bê": é que **trocar UMA letra troca a palavra inteira**.

BOLA, BOTA, BOCA. GATO, PATO, RATO. FACA, VACA, FOCA.

Quem entendeu isso entendeu para que serve o alfabeto. Quem não entendeu vai ler
CASA onde está escrito CAMA a vida inteira — porque "quase igual" ainda parece
igual, e a leitura por adivinhação nasce exatamente aí.

## 2. ⚠️ A pergunta que parece contradizer o degrau 4 — e não contradiz

No degrau 4 (O Som que Abre) dizer **"bê"** era o erro: lá o assunto era o SOM
/b/, e o nome da letra o esconde. **Aqui o nome da letra é legítimo**, porque
aqui o assunto É a letra: o currículo pede *"nomear as letras do alfabeto"*, e o
nome é como a criança vai pedir a letra ao professor e achá-la no teclado.

É a mesma palavra em dois degraus, e é a ORDEM que decide se ela ensina ou
atrapalha — exatamente como aconteceu com a letra inicial entre os degraus 3 e 4.

Consequência prática boa: **este caderno não precisa de recorte de sílaba**. Nome
de letra é palavra de verdade ("éle", "ême", "érre") e o sintetizador diz certo.
O `silabas.json` sai vazio de propósito e o portão `_qa/silabas.py` confere isso.
⚠️ Mas os nomes vão **escritos como se falam**, um a um: mandar o TTS ler a letra
"F" sozinha devolve coisa errada; "éfe" devolve certo. Mesmo princípio que salvou
a sílaba no degrau 5 — a voz não lê símbolo, lê palavra.

## 3. ⚠️ O que a colheita quase toda faz de errado: LETRA DEMAIS DE UMA VEZ

Das 24 folhas, **oito pedem várias letras de uma vez** — `PIP__A`, `C_MEL_`,
`B_N_N_`, `J_N_L_`, `P_T_C_`. Parecem a mesma tarefa, e não são: com um buraco a
criança resolve um problema; com quatro ela resolve um quebra-cabeça, e erra por
carga, não por não saber a letra.

No caderno é **sempre um buraco por palavra**. A escada é o LUGAR do buraco
(começo → meio → fim), não a quantidade.

## 4. As folhas que viraram folha, uma a uma

| Origem | O que a folha de papel manda | O que virou aqui |
|---|---|---|
| **d14** ⭐ | *"Observe os desenhos, mude apenas a PRIMEIRA LETRA e leia a palavra formada"* — `_OLA _OLA _OLA`, `_ATO _ATO _ATO`, `_ACA _ACA _ACA` | **Folha 1**, a que ensina. É a folha de ouro da colheita: nenhuma outra mostra que a letra MUDA a palavra; todas as outras só pedem para completar. Virou manipulação livre — a criança toca na letra e a FIGURA troca na frente dela |
| **d02** | "A letra que falta" — `GALINH_`, `B_LSA`, `CHA_ÉU`, com figura | **Folhas 2 e 3** (um buraco por palavra) |
| **d07 / d12** | "Pinte a letra inicial do nome de cada desenho e complete" — `_ALA` com B / F / M | **Folha 2**, com as opções DECLARADAS |
| **d08 / d09** | "Escreva a letra inicial de cada figura" | **Folha 9** (a única com escrita) |
| **d11** | "Qual é a letra?" | **Folhas 2 e 3** |
| **d16** | "Complete a palavra" — `BO__`, `___RRO`, `MA___`, com figura | **Folhas 6 e 7** (montar com as letras) |
| **d18** | "Complete com as letras que faltam e pinte as figuras" — só a letra A | **Folha 5** (ache TODAS as figuras com esta letra) |
| **d05** | "Recorte e cole a PALAVRA correspondente ao nome da figura" (BALEIA / BICO / SINO…) | **Folha 8** (ligar a figura ao nome escrito) |
| **d15** | "Complete as palavras com as letras que faltam", em grade | **Folhas 6 e 7** |
| **d22** | "Pinte as figuras e complete as palavras" — `___va`, `___belha`, `___lefante` (vogal inicial) | **Folha 2** |
| **d23** | "Escreva as letras faltantes" com a palavra-modelo ao lado | **Folha 9**, sem o modelo (o modelo é muleta: ela copia) |

## 5. As folhas RECUSADAS — e o motivo de cada uma

| Origem | Por que não entrou |
|---|---|
| **d01, d03, d11, d13, d24** | **Várias letras de uma vez** (`C_MEL_`, `B_N_N_`, `P_T_C_`). Ver o item 3: erra-se por carga, não por não saber |
| **d06** | É o degrau 5 (completar com SÍLABAS), já feito |
| **d10** | É o degrau 5 (a sílaba que falta) |
| **d20** | Letra pontilhada para cobrir: é TRAÇADO (motricidade), outro objetivo |
| **d19, d21** | Frase — *"A bola é do Pedro"*, *"A ___ é delicada"*. É o degrau 7/8 (espaços entre palavras e leitura de frase). **Reposicionadas**, não descartadas |
| **d17** ⭐ | *"Junte as LETRAS, depois as sílabas, e forme a palavra"* (C+A+M+A → CA+MA → CAMA). Folha excelente — mas ela ATRAVESSA os degraus 5 e 6 de uma vez. Fica para o degrau 8, como revisão |
| **d04** | Grade de caixinhas com algumas letras dadas e acento a conferir. Acento é degrau bem posterior |

## 6. As regras que este caderno respeita

1. **Um buraco por palavra.** Sempre.
2. **Repetição em BLOCO.** Folhas 2 e 3 são a mesma mecânica com o buraco
   mudando de lugar (começo → meio → fim). Folhas 6 e 7 são o mesmo gesto com
   uma letra a mais para descartar.
3. **A escada está declarada e o sorteio a respeita** (`pegaEmEscada`): a folha 1
   abre nos moldes de duas opções e termina nos de três (`_ATO`, `BO_A`); a
   folha 3 só chega ao fim da palavra depois de sete buracos no meio.
4. **Os distratores das folhas 2 e 3 formam outra palavra DE VERDADE** — `_ATO`
   com G, P e R. Isso é de propósito e é o coração do degrau: as três respostas
   são palavras certas, e quem decide é a FIGURA. Distrator que não forma nada
   deixaria a criança acertar por eliminação sem olhar a letra.
5. **A folha 8 não escreve o nome ao lado da figura.** Com o nome ali, "ligar a
   figura ao nome" vira comparar duas palavras iguais: ela casa os desenhos das
   letras e nunca precisa saber o que a figura é. O andaime honesto é o
   alto-falante.
6. **Seis palavras novas entraram no pote só para formar PAR MÍNIMO** — BOCA,
   FOCA, MOLA, MALA, LOBO, COPO, todas do banco. Sem par, não há como mostrar
   que uma letra muda tudo.

## 7. Os gestos (o leque)

| Gesto | Folhas | % |
|---|---|---|
| escolher entre opções | 2, 3, 4 | 30% |
| montar arrastando / tocando | 6, 7 | 20% |
| explorar (a máquina de trocar letra) | 1 | 10% |
| marcar várias | 5 | 10% |
| ligar | 8 | 10% |
| escrever no teclado | 9 | 10% |
| marcar (o mural) | 10 | 10% |

Sete gestos, nenhum acima de 30%.
