# Parecer pedagógico — *Aprendendo a divisão e as horas*

**Caderno:** `_divh4` · **Ano:** 4º · **Componente:** Matemática
**Formato:** folha viva, 35 folhas · **Conferido em:** 26/set/2026 (lido folha a folha)

> **Para que este documento existe.** Pedido do Marcos, repetido três vezes em
> 20/set/2026: *"o crivo que falo é o pedagogo olhando e dizendo que está tudo
> adequado"* e *"por isso eu pedi o crivo do pedagogo, para ver se está adequado
> E O CURRÍCULO — sempre fizemos assim"*.
>
> Os portões medem o que se conta. O que eles não medem é o que só aparece
> LENDO: objetivo que não descreve a folha, degrau que não sobe, conteúdo de
> outro ano, contradição entre folhas. Este parecer foi escrito com a saída de
> `python3 _qa/folha_a_folha.py _divh4` aberta ao lado.

---

## 1. As habilidades, copiadas do currículo da rede

Quatro habilidades do bloco do **4º ano de Matemática** do currículo de
Blumenau, conferidas palavra por palavra pelo portão `0b9`:

> **Números —** *"Resolver e elaborar problemas de divisão cujo divisor tenha no
> máximo dois algarismos, envolvendo os significados de repartição equitativa e
> de medida, utilizando estratégias diversas, como cálculo por estimativa,
> cálculo mental e algoritmos."* → folhas 1–3, 5–15, 19, 20 e 35.
>
> **Números —** *"Compreender as relações existentes entre as operações de
> multiplicação e divisão, aplicando-as na resolução e elaboração de
> problemas."* → folhas 4 e 16.
>
> **Álgebra —** *"Reconhecer, por meio de investigações, que há grupos de
> números naturais para os quais as divisões por um determinado número resultam
> em restos iguais, identificando regularidades."* → folhas 17 e 18.
>
> **Grandezas e medidas —** *"Ler e registrar medidas e intervalos de tempo em
> horas, minutos e segundos em situações relacionadas ao seu cotidiano, como
> informar os horários de início e término de realização de uma tarefa e sua
> duração."* → folhas 21–34.

---

## 2. Está adequado ao 4º ano?

**Sim**, e é adequado porque respeita os limites que o próprio texto do
currículo escreve:

- **«divisor … no máximo dois algarismos».** O divisor do caderno vai de 2 a 19
  (570 ÷ 19, 120 ÷ 12). Contas como 5580 ÷ 154, que apareceram em duas folhas
  colhidas (A05, B12), ficaram de fora.
- **«estimativa, cálculo mental e algoritmos».** Os três estão presentes, cada
  um com folha própria: estimar arredondando o divisor (12, 14, 19), calcular
  de cabeça para ligar (13) e o **algoritmo da chave** (9 a 11) — que no 3º ano
  ficou de fora de propósito e aqui é o conteúdo.
- **«repartição equitativa e de medida».** As duas perguntas têm folha própria
  (2: *quantos para cada um?*; 3: *quantos grupos dão?*), e a folha 3 **diz em
  voz alta** que a pergunta mudou e a conta não.
- **«início e término … e sua duração».** Ler o relógio (21 a 26) é retomada do
  3º ano e está declarado assim no POTE; o que é do 4º — o **intervalo** —
  tem cinco folhas (29 a 33).
- **O resto como investigação (Álgebra).** Não basta sobrar: na trilha do Hulk
  (17) a casa certa é a que sobra **exatamente 1**, e na 18 a criança marca os
  números de mesmo resto e o fecho lhe mostra que eles andam **de 3 em 3** ou
  **de 4 em 4**. É a «regularidade» que o currículo pede.

**Conteúdo de outro ano, declarado:** a folha 1 (repartir 12 pirulitos em 3
caixas) é retomada do 3º ano — dura um minuto e existe para lembrar o gesto de
dividir antes de armar a conta. Os nomes dos termos (5) usam «quociente», que o
bloco do 3º já nomeia: conteúdo de ano anterior cabe por definição.

---

## 3. O material dourado — o pedido do Marcos, e onde ele entra

Pedido de 26/set/2026: *"Divisão com ajuda do material dourado"*.

**O material é RECURSO, não conteúdo**, e está declarado assim no
`curriculo.json` (`fora_do_curriculo`, com o motivo): o nome não aparece no
bloco do 4º ano, mas as «estratégias diversas» e o «algoritmo» aparecem — e é
com a placa, a barra e o cubinho que a **troca** da conta armada deixa de ser
mágica.

A escada vai do concreto ao símbolo, **sem pular degrau**:

| Folha | O que a criança faz | Degrau |
|---|---|---|
| 6 | conta as peças e escreve o número (placa = 100, barra = 10, cubinho = 1) | conhecer a peça |
| 7 | leva as peças aos grupos, dando a volta, até ficarem iguais (ex.: 369 ÷ 3) | repartir sem troca |
| 8 | uma barra sobra: leva-a à **casa da troca**, ela vira dez cubinhos, e reparte (ex.: 52 ÷ 4) | a troca |
| 9 | a mesma conta **na chave**, com o material desenhado ao lado | o registro |
| 10 | a chave com troca, **sem** o material | o símbolo sozinho |
| 11 | a chave com resto | o que sobra |

**Duas escolhas que valem registrar:** o grupo **recusa** peça além da sua parte
(é o erro que a folha existe para mostrar), e a casa da troca **recusa** a barra
enquanto os grupos ainda não receberam as barras deles — trocar cedo é
desmanchar à toa, e a dica diz isso.

**O que a colheita NÃO deu:** das 65 folhas colhidas sobre o material, **nenhuma**
reparte peças em grupos — quase todas são de valor posicional. As folhas 7 e 8
entram como **bloco declarado**, apoiadas nas quatro que tocam o gesto (E31,
E28/G17, E37, E30), e as peças são as do G06, recortadas. Ver
`_sequencias/POTE-DIVH4.md` §8.

---

## 4. A escada, folha a folha — ela sobe?

- **1 → 3:** do gesto (arrastar) à conta com número maior, e da repartição à
  medida. O problema vem antes do nome.
- **4 → 5:** julgar a conta de outra criança (e o resto maior que o divisor, na
  j2 e na j3, é o erro clássico do 4º ano) → **só então** os quatro nomes.
- **6 → 11:** o material dourado até a chave, descrito acima.
- **12 → 14, 19:** o divisor ganha um algarismo. Conferi as dez contas da folha
  12: **em todas, arredondar o divisor para a dezena dá o quociente certo** (68
  ÷ 34 → 68 ÷ 30 ≈ 2; 55 ÷ 11 → 55 ÷ 10 ≈ 5). A estratégia que o enunciado
  ensina funciona em todos os itens — se falhasse num, a criança aprenderia que
  a estratégia mente.
- **15 → 18:** exata ou não → a conta de volta → o resto como investigação.
- **20:** elaborar — escolher a pergunta que a divisão responde, que é o
  «elaborar» do currículo e que nenhuma folha colhida pede.
- **21 → 26:** os minutos (com a flor da F24), ler, **girar** o relógio que
  a criança mesma acerta, ligar ao digital, as partes do dia.
- **27 → 28:** hora, minuto e segundo → a ponte: **minutos em horas é dividir
  por 60, e o resto são os minutos.** É a folha que costura as duas metades do
  caderno.
- **29 → 33:** daqui a 15 minutos → antes e depois → quanto durou → dá tempo? →
  a rotina em ordem.
- **34, 35:** a memória (relógio ↔ digital) e o cartaz.

**Pares com a mesma mecânica** (2/3, 7/8, 9/10/11, 13/14, 23/24, 29/30, 31/32):
em todos, a segunda folha **diz o que mudou** logo na primeira frase — *"Agora a
pergunta mudou"*, *"Agora sobra uma barra"*, *"Agora com troca, e sem o
material"*, *"Agora o divisor tem dois algarismos"*… (portão `0b14`).

---

## 5. O que esta leitura ACHOU e foi consertado

1. **A folha 10 dizia só "quando a barra não dá para repartir"** — mas o sorteio
   dela inclui **450 ÷ 5** e **100 ÷ 4**, em que a troca é da **placa** (quatro
   placas não se repartem em cinco grupos). A criança leria a regra e não a
   veria na conta. Hoje: *"quando a placa ou a barra não dá para repartir, ela
   é trocada por dez peças menores"* — na tela e na voz.
2. **A pergunta do fim repetia um item.** O gancho era *"quantas horas tem a
   semana inteira?"*, e a folha 27 já pergunta *"Uma semana tem ___ horas"*
   (168). Gancho que a criança já respondeu não é gancho. Hoje: *"quantos
   minutos você passa na escola numa semana inteira?"* — aberta, dela, e que
   junta a duração (folhas 29–33) com a multiplicação.
3. **"A tarde da Beatriz" com horários das 8h às 9h30.** O título da rotina
   (folha 33) contradizia os horários que a criança põe em ordem — e a folha 26
   acabou de ensinar que 8h é manhã. Hoje: *"A manhã da Beatriz"*.
4. **O ponteiro das horas da F08 é MAIOR que o dos minutos** (540 px contra 442
   px, medido na folha). A folha 21 ensina *"o ponteiro azul e comprido marca os
   minutos"*; com as figuras no tamanho do papel, a tela desmentiria a frase.
   Cada ponteiro tem agora a sua largura, e o dos minutos é o comprido.
5. **Quatro restos do esqueleto no relatório do professor** (sem erro nenhum na
   tela): o parecer da criança dizia *"você começou a reparar que o mesmo som
   pode se escrever de cinco jeitos"*, e o do professor falava de letras e de
   ditado. Reescritos para a divisão e as horas, com a retomada concreta (o
   material na mesa, o relógio na mão).

---

## 6. Ressalvas que ficam, e o professor precisa saber

- **A chave mede o quociente e o resto, não os passos.** As subtrações que se
  escrevem embaixo do dividendo ficam no papel — o relatório diz isso ao
  professor, com todas as letras.
- **O relógio da tela anda de 5 em 5 minutos.** O mostrador colhido não tem os
  risquinhos dos minutos. A leitura minuto a minuto continua no relógio da sala.
- **Na mesa do material dourado, a escala não é a real:** o cubinho aparece
  maior que um décimo da barra, senão teria 6 px e ninguém o contaria.
- **Material dourado de verdade na mesa é melhor que qualquer tela.** A folha 7
  e a 8 existem para quem não tem o material na escola, ou para depois dele —
  nunca em vez dele.

---

## 7. Parecer

**ADEQUADO para o 4º ano**, com as cinco correções da seção 5 já aplicadas.
As quatro habilidades citadas estão no bloco do ano, os limites que o texto do
currículo escreve (divisor de até dois algarismos; o intervalo de tempo) são
respeitados, o material dourado entra como degrau concreto antes da chave, e a
folha 28 costura as duas metades do caderno numa ideia só: *minutos em horas é
uma divisão por 60, e o resto são os minutos*.

**O que este parecer NÃO é:** aprovação do professor. Ele é o meu olhar lendo o
caderno inteiro; o olhar de quem dá a aula naquela turma continua sendo o do
Marcos.
