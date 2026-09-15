# 📚 SEQUÊNCIAS DIDÁTICAS — a LEI do formato "folha viva"

> **Este documento é só destas atividades.** As atividades do MOTOR (o Grande
> Circo do Teo, a Feirinha, a Expedição da Divisão, as provas) seguem o
> `MANUAL-MESTRE.md` e o `_padrao/ESQUELETO/CONTRATO.md`. **Aqui é outro
> formato, com outras regras, e misturar os dois já custou caro.**
>
> Pedido do Marcos que fez este arquivo existir (12/set/2026):
> *"registre um documento para essas nossas novas atividades separado das
> outras, e registre minhas regras, o que aprendemos, os erros, etc."*
>
> **Quem chega aqui sem memória: leia este arquivo inteiro antes de tocar em
> qualquer caderno de sequência didática.** Depois dele, o `POTE-*.md` do degrau
> em que vai mexer.

---

## 1. O que é uma "folha viva"

É o **caderno de folhas** que a criança vira uma a uma, como o caderno de papel
que o professor imprime — só que cada folha **funciona**: a figura fala, a peça
arrasta, o teclado escreve, o erro responde.

**Não é** uma atividade do motor com outro nome. Diferenças que importam:

| | Motor (Esqueleto) | **Folha viva** |
|---|---|---|
| Conteúdo | `conteudo.json` → fases | `var ITENS` (potes) + `folhas.js` |
| Unidade | a FASE (uma tela, um gesto) | a FOLHA (vários itens na mesma tela) |
| Origem | roteiro nosso | **uma folha impressa de verdade** |
| Navegação | trilha/lição | livro, com "Folha N de M" |
| Portões | a banca inteira alcança | **a banca do motor NÃO alcança** (§7) |

**As dez sequências que existem hoje** estão indexadas em
`_sequencias/ALFABETIZACAO-1ANO.md`, e o crivo de cada uma no `POTE-*.md`
correspondente.

---

## 1b. ⭐⭐ COMO NASCE UM CADERNO NOVO — do ESQUELETO, nunca de um clone

```
bash _padrao/nova_folha_viva.sh <pasta> <prefixo> "<Título>"
```

**Pergunta do Marcos (15/set/2026), e ela mudou o método:** *"mas por que você
está clonando? Não é melhor colher as atividades da internet com o crivo e criar
as interatividades que são pedidas, sem clonar?"*

Ele estava certo sobre o problema, e a conta da Fábrica de Nomes prova:

| de onde veio o erro | quantos |
|---|---|
| a parte do método dele — colher, ler as trinta, o crivo, recortar as figuras | **0** |
| conteúdo do caderno de origem que veio junto no clone | **5** |
| contratos internos do motor montados errado | **3** |

As **interatividades nunca foram clonadas** — o gesto sai do comando impresso na
folha de papel, e a figura sai da mesma folha. O que se clonava era o **motor**,
e com ele vinham os objetivos do relatório, a citação do currículo, o sorteio
das folhas (`novaFolha`), o prefixo das figuras e da voz, o `var LIGAR`.

**O `_padrao/FOLHA-VIVA/` é o motor sem conteúdo nenhum.** Vem pronto: navegação
e progresso, voz com alto-falante em tudo, teclado de letras nas duas portas,
arrastar com mouse/dedo/caneta, gavetas, ligar, cruzadinha, boletim da criança,
relatório do professor pela medalha, dossiê, "continuar de onde parou" por 55
minutos, a chave `1275@` e o aviso ao controle da sala. Vem vazio: `GESTOS`,
`ITENS`, `DADOS`, `NOMES`, `CURRICULO`, `novaFolha()`, `OBJETIVOS` e as folhas.

⚠️ **O script recusa prefixo já usado** por outra atividade — prefixo repetido
faz dois cadernos brigarem pela mesma memória do "continuar de onde parou", e a
criança abre um e cai no meio do outro.

⚠️ **O recém-nascido JÁ ABRE LIMPO** (medido: zero erro de JS, zero 404), e o
pré-voo reprova em três portões que dizem *"este caderno ainda está vazio"*, não
*"o esqueleto está quebrado"*: `0b6` catálogo, `3g` duração e `1z` boot (o mp3
da capa, que o `entregar.yml` grava). **Qualquer outra reprovação no primeiro
minuto é defeito de verdade.**

**A ordem que economiza voltas** — e foi a falta dela que custou caro em
15/set, quando montei o caderno inteiro e só depois fui auditar:

1. colher as folhas (`buscar-fotos.yml`) · 2. **ler as trinta, uma a uma**, e
escrever o `POTE-<assunto>.md` · 3. o roteiro sai do **inventário de verbos** do
crivo · 4. preencher os blocos marcados · 5. `gerar_falas.py` ·
6. `bash _qa/previo.sh` · 7. **`node _qa/conta_folha.js`** ·
8. `node _qa/joga_folha.js` · 9. `bash _qa/auditar_folha.sh`.

As armadilhas medidas (nome com espaço num campo de teclado, acento no gabarito,
chave igual à palavra da tela, o contrato do pincel) estão no
`_padrao/CLONAR-FOLHA-VIVA.md`, que virou documento de conferência.

---

## 2. ⭐⭐ AS REGRAS DO MARCOS — ditas por ele, com as palavras dele

### REGRA ZERO — "Nunca chute nunca invente" (12/set/2026)
Quatro palavras, e vêm antes de todas as outras. Número sem fonte não sai da
minha boca; **e "li no log" só vale se eu tiver aberto o MODELO que gerou o
log**. Constante inventada dentro de portão tem que estar escrita no comentário
**e impressa na saída** como `PALPITE DECLARADO`. O que não dá para medir daqui,
eu digo que não dá e mostro quem pode medir. E nunca dizer que fiz o que não fiz.
> *O teste, antes de mandar qualquer número:* **de onde veio, e o que eu teria
> que abrir para ele estar errado?**

### REGRA DO TAMANHO — **20 folhas** nas novas; as 25 dos cadernos já feitos ficam
**MUDOU em 14/set/2026.** A regra nasceu em 12/set com as palavras dele: *"eu
acredito que cada sequência precise de no mínimo 25 folhas"*, e a medição do §4
deu razão a ele: 25 folhas é o que enche os 55 min da criança **rápida**.

Em 14/set ele baixou o piso, e disse por quê: **velocidade de produção**
(*"pode baixar para 20"*, *"torna criar mais rápido também"*, *"digo nas
próximas atividades pode fazer com 20"*). Então, com todas as letras:

| | piso |
|---|---|
| sequência **nova**, daqui para a frente | **20 folhas** |
| os cadernos **que já existem** | ficam como estão — nenhum encolhe |

⚠️ **O que a medição continua dizendo, e não muda por decisão:** com 20 folhas a
criança **rápida** sobra tempo no fim da aula. Quem vai devagar não é
prejudicado (o fecho é alcançável a qualquer momento — §4). Ou seja, o custo de
20 é *tempo ocioso da mais rápida*, não *aula incompleta* — e foi com essa
informação na mesa que ele decidiu.

⚠️ **E o piso não vira teto ao contrário:** se o conteúdo der 25 folhas de
verdade, ficam as 25. O que o piso de 20 proíbe é o oposto — **inventar folha
de enchimento para fechar número**. Faltou conteúdo para 20? A resposta é
perguntar ao Marcos, nunca preencher.

### REGRA DA ORIGEM — "veja o que as atividades pedem que o estudante FAÇA"
Palavras dele (set/2026), e depois, mais direto: *"seria legal se vc conseguisse
recriar como está ali, a interatividade necessária para executar as tarefas"*.
Folha nossa **nasce de uma folha impressa de verdade**, colhida da internet, e
recria **o gesto** dela — não "algo inspirado nela". Ver o processo no §5.

### REGRA DA VOZ
- **Toda tela é narrada**, com voz de verdade (Edge TTS, `pt-BR-AntonioNeural`).
- **Alto-falante em TODA resposta que a criança toca.** Palavras dele: *"o
  alto-falante nas respostas também, para ajudar os alunos que não sabem ler"*.
- **`falas.json` é a VERDADE**: texto escrito ali = voz gravada. MP3 não se lê.

### REGRA DAS DUAS PORTAS
Toda folha com teclado na tela aceita **também o teclado de verdade**
(`document.onkeydown`); toda folha de arrastar aceita **também o toque simples**.
Palavras dele: *"seria interessante se o aluno além de teclar no teclado virtual
funcionasse se ele tocasse no teclado de verdade, as duas opções"*.

### REGRA DA REPETIÇÃO SEGUIDA
Mecânica que repete vem em **BLOCO COLADO**, subindo um degrau dentro do bloco —
nunca espalhada. Palavras dele: *"as crianças me dizem 'isso eu já fiz, tô
fazendo de novo'"*.

### REGRA DO REUSO DO BANCO
Antes de pedir arte, **consultar o banco** (`_banco/index.json`). Mascote pode
ser reaproveitado; **mascote novo só quando ele pedir**.

### REGRA DA PUBLICAÇÃO
*"pode publicar, pode sempre publicar a menos que eu diga para esperar"* — desde
que a banca tenha aprovado. **E atividade nova NÃO entra no hub** até ele pedir
com todas as letras: nasce no repositório dela e o link vai para ele.

### REGRA DO CONSERTO DUPLO
Defeito que chega perto da criança tem conserto de **duas partes**: arrumar o
código **e** criar/estender o portão que o pega sozinho da próxima vez. Sem a
segunda parte, o trabalho não está feito.

---

## 2b. 📸 ⭐ MOSTRAR AS FOLHAS DE PAPEL — SEMPRE (ordem do Marcos, 14/set/2026)

**Palavras dele:** *"sempre mostre as folhas das atividades que encontrou, que
passaram pelo crivo do especialista"*.

Não é pedido de relatório: é **prova**. A regra da origem diz que o gesto vem do
comando impresso da folha de papel — e até aqui essa prova ficava só escrita, num
`.md` que ele teria de abrir para conferir. Escrever "veio do papel d29" é uma
afirmação minha; **mostrar o d29** é a evidência.

**Como fica, e é parte da entrega, não um extra:**

1. O crivo (`_sequencias/POTE-<assunto>.md`) continua igual: comando impresso
   VERBATIM, o verbo, e o veredito de cada folha colhida.
2. **Monta-se um CONTATO-FOLHA das APROVADAS**, uma miniatura por folha, com o
   código (`d29`) e **o que ela virou no caderno** escrito embaixo. Fica guardado
   em `_sequencias/crivo/<assunto>-aprovadas-*.png`, commitado junto.
3. **Esse contato-folha vai para o Marcos na mesma mensagem em que o caderno é
   entregue** — nunca só o link.
4. O que foi **recusado** continua listado no crivo com o motivo; se ele pedir,
   monta-se o contato-folha das recusadas também.

⚠️ E vale para o que JÁ existe: os cadernos de alfabetização foram entregues sem
este contato-folha. Quando algum deles for mexido, o contato-folha da colheita
dele entra junto.

---

## 3. ⚠️ OS ERROS JÁ PAGOS NESTE FORMATO — um por um

> Esta lista existe para não se repetirem. Cada linha custou uma rodada com o
> Marcos, ou chegou até a criança.

### 3.00000 ⭐⭐⭐ O PORTÃO QUE MEDIA NUMA PONTA E NÃO NA OUTRA — quatro publicações falharam e eu não sabia por quê

**O que o Marcos viu:** a manhã inteira sem receber os consertos. Ele perguntou
três vezes — *"já foi atualizada a horta da vovó?"*, *"então publique tudo que
foi consertado"*, *"verifiquei agora que a Coroa dos Cinco Reinos só tem 10
folhas"* — e eu respondia "disparei, está na fila". Quatro corridas de entrega,
nenhuma publicou nada.

**O que estava acontecendo.** No log da corrida, escrito:

```
##[error]_sil1: estatico (nome usado que nunca foi declarado) REPROVOU
##[error]PORTÃO PRÉ-ENTREGA REPROVOU — NADA foi publicado.
```

O `rolaParaCruz` que eu tinha escrito naquela manhã testava
`typeof CRUZ !== "undefined" && CRUZ && CRUZ.E`. O `typeof` protege só a
**primeira** ocorrência; o `CRUZ` nu depois do `&&` é `'CRUZ' is not defined`
para o ESLint (ele não faz análise de fluxo) em todo caderno sem cruzadinha.
Como `CRUZ` e `ATIVA` são `var` globais, a forma que passa é `window.CRUZ`.

**E por que eu não vi.** O portão `0a2 estatico` **não roda neste container**: o
`node_modules` do ESLint não vem instalado. Ele dizia `NAO MEDI` e o pré-voo o
listava entre os doze que não mediram — uma linha no meio de muitas, fácil de
ler como "não se aplica a esta atividade".

> ## ⚠️⚠️ A LIÇÃO, e ela vale para todo portão
>
> **O mesmo `0a2` roda DENTRO do `entregar.yml`, onde o ESLint existe — e lá ele
> REPROVA E SEGURA A PUBLICAÇÃO DO REPOSITÓRIO INTEIRO.** Aqui cego, lá
> vermelho. Eu publicava achando que estava tudo bem.
>
> **Portão que mede numa ponta e não na outra é pior que portão nenhum: ele dá a
> sensação de ter passado.** Quando um portão disser `NAO MEDI`, a pergunta não é
> "esta atividade tem isso?" — é **"ele mede na hora de publicar?"**. Se medir,
> `NAO MEDI` aqui é uma bomba armada.

**O conserto, em duas partes:** o código nos 19 cadernos, e o
`_qa/estatico.sh`, que agora **instala o ESLint sozinho** na primeira vez e, se
não conseguir, diz com todas as letras que isso não é "passou" e que o
`entregar.yml` vai segurar. Testado com o `node_modules` apagado de propósito:
ele se reinstalou e mediu.

**E a dívida foi paga na hora:** varri os quinze portões que o `entregar.yml`
roda e conferi um a um se eles medem AQUI. Quatro dizem `NAO MEDI` porque a
peça não existe neste formato (`corta_figura`, `enunciado_bate`, `exemplo` e
`pcruim` pedem `conteudo.json` ou FASES do motor) — inofensivos. Um depende de
instalação como o ESLint: o **`pronuncia`**, que precisa do Vosk. Mas **ele só
emite `::warning::` no workflow e não segura a entrega**, então não é a mesma
armadilha. O `estatico` era o único cego aqui e bloqueante lá.

---

### 3.0000 ⭐⭐ O `@` QUE SUMIU DO CSS — 36 REGRAS MORTAS NUM CADERNO NO AR

**Data: 14/set/2026. Achado por mim, um dia depois de publicar — e por acaso.**

Ao escrever o estilo do caderno de multiplicação eu reparei que o arquivo tinha
`keyframes pulsa{...}` e `media (max-width:430px){...}` **sem o arroba**. Fui
conferir o Desfile das Letras, que tinha subido no dia anterior: **36 regras-@
sem o `@`** — 28 `@keyframes` e 8 `@media`. Uma edição minha em massa comeu o
caractere, e o git confirma o commit exato em que isso aconteceu.

**O que a criança perdeu:** *toda* animação (o confete do fim, o tremor do erro,
a letra que entra no desfile, o brilho do botão) **e todas as regras de tela
pequena** — no celular da escola o caderno ficava com o leiaute da tela larga.

**Por que nada reclamou, e esta é a parte que interessa:**

| portão | por que passou |
|---|---|
| `node --check` | não olha CSS |
| contraste (`contraste.js`) | mede o pixel do fundo — a cor continuava certa |
| leiaute (`leiaute_mao.js`) | mede a caixa — a caixa continuava certa |
| `andar_folha` / `joga_folha` | o app abre e responde igual: animação não é função |
| foto de regressão (5c) | fotografa a tela **parada**; o que morreu foi o **movimento** |

E o navegador não dá erro: `keyframes pulsa{...}` sem arroba não é sintaxe
inválida — vira uma **regra de estilo com o seletor "keyframes pulsa"**, que
nunca casa com nada. O CSS segue válido. A página segue abrindo bonita.

**A regra que fica:** *defeito que só existe em MOVIMENTO tem que ser MEDIDO* —
é a mesma lição do tremor do mascote, com outra roupa. Portão novo **4c3
`_qa/css_atregra.py`**, no pré-voo e nas duas bancas: reprova regra-@ sem o
arroba e **animação órfã** (`animation:` apontando para um `@keyframes` que não
existe). Na estreia achou, além das 36, uma `aparece` órfã que estava em TODOS
os cadernos de folha viva desde o primeiro, e animações órfãs em mais dezesseis
atividades (`pop`, `revIn`) — fila registrada na tarefa #109.

---

### 3.000 ⭐ A CAPA PROMETIA DEZ FOLHAS E O CADERNO TINHA VINTE E CINCO

**Quem viu foi o Marcos, não eu, e no mesmo dia em que subi o caderno**
(13/set/2026): *"na última atividade que você fez ou atualizou você fala de 10
folhas na página inicial, Desfile das Letras, quando agora são 25; favor de
atentar a isso"*.

Eu levei o Desfile de 11 para 25 folhas, troquei a **voz** da capa para *"vinte
e cinco"* e deixei o **escrito** em *"dez folhas do alfabeto"*. É a família **"a
tela diz uma coisa e a voz diz outra"** — a mesma que o `falas.json` existe para
matar — só que **na capa**, que é justamente onde nenhum portão olhava. E a capa
é a primeira coisa que a criança e o professor veem.

**A varredura mostrou que não era só o meu.** Medindo `PAGEL` contra o que cada
capa promete, nos doze cadernos:

| caderno | a capa prometia | tinha |
|---|---|---|
| O Desfile das Letras | dez folhas | **25** |
| A Fábrica de Palavras | dez folhas (escrito **e** falado) | **11** |
| A Roda das Sílabas | *"dez folhas **do começo das palavras**"* | **15**, e é de sílabas |

⚠️ **A Roda tinha DOIS erros na mesma linha:** o número e o ASSUNTO — *"do
começo das palavras"* é o subtítulo da **Família das Palavras**, resto de clone
que o `clone.py` nunca veria, porque não há prefixo alheio nenhum num pedaço de
texto em português.

**O portão (conserto duplo):** o `_qa/andar_folha.js` agora lê o número que a
capa promete — **no escrito e na fala** — e compara com o número de folhas que o
caderno tem. Ele já abria o caderno e já contava o `PAGEL`; faltava cruzar as
duas coisas.

⚠️ **E ele só olha número colado em "folha(s)"**, senão acusaria o Grande Jogo
por dizer *"a revisão dos oito degraus"* — que não fala de folhas, fala de
degraus. Portão que acusa inocente é portão que se aprende a ignorar.

### 3.00 ⭐ A FOLHA DE CIRCULAR NÃO FECHAVA — em SETE cadernos, todos no ar

**Nasceu de uma pergunta do Marcos** (13/set/2026): *"a outra banca, aquela que
corrige as atividades normais, seria uma boa utilizar para essas sequências
didáticas?"*. A resposta foi que a banca do motor inteira não serve aqui, mas
que **três juízes dela mediam coisa que em folha viva ninguém media** — e o mais
sério era o **jogador**, que RESOLVE a atividade. Escrevi o
`_qa/joga_folha.js`. **Na primeira hora de vida ele achou três defeitos, dois
deles em sete cadernos publicados.**

O mais grave é o do `riscoDeCircular` (a folha de *"circule quem saiu da fila"*),
e ele tem duas metades:

1. **O toque não fazia nada.** O `pointerdown` saía cedo em
   `pointerType === "touch"`, com o comentário *"no dedo, tocar já resolve"* — e
   **nada implementava esse "tocar já resolve"**. Nenhum botão tinha `onclick`.
   No celular e no tablet a folha era uma parede. No PC, o clique simples
   também não fazia nada: só valia o gesto de circular com o rato.
2. **Circular a resposta CERTA contava como ERRO.** O `for(w in botoes)`
   percorre um ARRAY, então `w` é o ÍNDICE ("0", "1"…) — e era isso que ia para
   a função de resposta. Só o `_alfa1` passa um OBJETO indexado por palavra, e
   por isso só ele funcionava. Nos outros sete a função recebia `"0"` onde
   esperava o BOTÃO, lia `"0"._w` (undefined), não batia com a resposta certa e
   caía no ramo do erro. **Sempre.**

Somando as duas: **a folha não fechava por caminho nenhum** — nem clicando, nem
tocando, nem circulando certo. A criança acertava e o caderno dizia que não.

- **Alcance:** `_abc1` (duas folhas), `_ini1`, `_novo`, `_rima1`, `_roda1`,
  `_som1` — e o `_sil1`, que tem a função clonada. Seis deles no ar.
- **Por que nenhum portão via:** o `andar_folha.js` abre a folha e confere erro
  de JS e figura quebrada — e não havia nem um nem outro. O `leiaute_mao.js`
  mede tamanho de alvo — e o alvo era grande. A folha estava *bonita e morta*.
- **Conserto (na fonte, nos oito):** `alterna` passa o BOTÃO quando recebeu um
  array e a CHAVE quando recebeu um objeto; e cada botão ganhou um `click` — a
  segunda porta — com um guarda de 400 ms para o traço que termina em cima de um
  botão não contar duas vezes.

E o terceiro defeito, do mesmo dia e do mesmo juiz: **o teclado não tinha K, W
nem Y**. Num caderno cujo assunto é o alfabeto de 26 letras, o pote da folha de
digitar sorteia as 26 — e em três delas a criança batia num teclado sem a tecla.
Corrigido nos doze cadernos, no teclado da tela e no `document.onkeydown`.

> ⚠️ **A lição de método, e ela é a mesma de sempre:** quando o jogador reprovou
> DEZESSEIS folhas de uma vez, a primeira suspeita foi a régua, não a peça — e
> estava certa: eu devolvia o `data-qa` em minúsculas e procurava por ele com
> `[data-qa="op-a7_0-b"]`, que não casa com `op-a7_0-B`. Consertada a régua,
> sobraram três reprovações — e as três eram verdadeiras.

### 3.0 `var` no fim do arquivo: o caderno morria na folha 2, e o `node --check` passava

Ao escrever as catorze folhas novas do Desfile (13/set/2026) eu pus o código
delas **no fim** do `folhas.js` — e os DADOS delas junto: `var POEMA = [...]`,
`var TRA_CEL = 10`. O arquivo tem, mais acima, um `monta()` que roda no
carregamento e chama todas as folhas.

**`function` sobe no arquivo (hoisting); `var x = ...` NÃO.** A declaração sobe
vazia e a atribuição fica onde está. Então, na hora em que `monta()` chamou a
folha 2, `POEMA` existia e valia `undefined` — e o caderno estourou em
`POEMA.forEach`, morrendo na segunda folha das 25.

- **Por que nenhum portão de texto viu:** não há erro de sintaxe nenhum. O
  `node --check` passou, o pré-voo passou, os 39 portões de texto passaram.
- **Quem pegou:** o `_qa/andar_folha.js`, que abre o caderno no navegador de
  verdade e anda folha por folha. Ele parou na folha 1 e imprimiu o
  `TypeError`. É exatamente para isso que ele existe.
- **A regra, daqui para a frente:** **dado de folha (`var` com valor) mora no
  TOPO do `folhas.js`**, junto do `var livro = ...`. Só as `function` podem
  ficar no fim. E folha nova **sempre** passa pelo `andar_folha.js` antes de
  qualquer outra coisa — "compilou" não é "abre".

### 3.1 A resposta estava IMPRESSA no enunciado — em 5 cadernos NO AR
A figura da mola vinha com a legenda **MOLA** logo abaixo e, embaixo dela,
`[ ][ ] L A` para a criança completar. **A resposta impressa dois centímetros
acima da pergunta.** Quem lia um pouco resolvia o caderno **copiando**, e a
folha media zero.

- **Causa:** o `figComSom`, clonado por todos os cadernos, escrevia o nome da
  figura por baixo dela.
- **Alcance:** `_roda1` (9 folhas), `_ini1` (22 itens), `_mont1` (20), `_let1`
  (21) e `_jogo1` (32 — **uma FORCA com a palavra escrita na tela**).
- **Conserto:** a legenda **não some** — fica invisível (`visibility`, para o
  espaço não pular) e **aparece no instante do acerto**. Assim a criança que
  chama a luneta de "telescópio" continua protegida.
- **Portão:** `_qa/resposta_impressa.py` (1i4 na banca).
- ⚠️ **Quem pegou foi uma FOTO, não um portão.** Regra que sai daqui: **depois
  de montar, OLHAR a tela** — e o que a foto achar vira portão no mesmo commit.

**E ela voltou em 14/set/2026, nos cinco reinos** — por um caminho novo: a folha
de ESCREVER o nome do reino trazia, como pista, a lista de quem mora nele
(*"o reino de a ameba, o paramécio e as **algas** do mar"*) e a resposta era
ALGAS. Mesmo defeito, origem diferente: não foi uma legenda, foi um TEXTO DE
APOIO que por acaso continha a palavra. → Em folha de escrever, a pista tem que
ser **descrição**, nunca enumeração — e o alto-falante dela fala a PISTA, não o
nome (senão a folha de escrever vira folha de copiar, e o relatório passa a dizer
"dominou" sobre cópia). Quem pegou: o portão 1i4, sozinho.

### 3.2 A sílaba saía da palavra ERRADA
A folha mostrava a figura da LATA e o alto-falante dizia LARANJA. Palavras dele:
*"não entendi muito o sentido da primeira atividade, pois cita laranja e aparece
lata"*. A sílaba nunca é sintetizada solta (senão a voz soletra): é recortada de
dentro de uma palavra gravada, e o gerador escolhia a fonte pela **ordem
alfabética**. → Portão `_qa/silaba_fonte.py` (0b10).

### 3.3 "Voz de navegador" = o MP3 não chegou ao site
Palavras dele: *"as sequências didáticas estão com voz de navegador"*. Não era
defeito de código: o `entregar.yml` tinha falhado e a pasta subiu **sem um único
mp3**; o `falar()` caía no sintetizador do Chrome. **Eu medi no container (onde
tocava perfeito) e disse que estava tudo bem — olhando para o lugar errado.**
→ Ferramenta `ouvir-no-ar.yml`: pergunta ao **site publicado**.

### 3.4 O commit sem a marca `[entregar]` não publica nada
Um conserto ficou commitado e não publicado, e eu disse a ele que estava no ar.
→ **Conferir a marca antes de empurrar**, e depois **ler o carimbo**
`_status/entrega-<repo>.json` comparando o `index` com `sha1sum <arquivo> | cut -c1-12`.

### 3.5 Os ids escritos à mão faziam o relatório sair ZERO
Cada folha gravava `n6_0` à mão e o `idsDaPagina` repetia a mesma tabela à mão:
dois lugares para combinar, os dois sintaticamente corretos. Quando a ordem das
folhas mudava, **o relatório do professor saía zero com a folha toda
respondida**, sem erro no console. Aconteceu duas vezes.
→ **A POSIÇÃO É A IDENTIDADE**: a folha da posição 7 usa o pote `p7`, grava
`n7_*` e fala `p7enun`, tudo derivado de `pi`. Não há segunda lista.

### 3.6 O portão da duração aprovava por causa do próprio erro
Ele cobrava **25 s por item** (o preço de DIGITAR uma palavra no teclado) em
folha onde a criança só **toca** numa opção — e usava esse número inflado para
escrever *"duracao ok: enche a aula"*. Quem desconfiou foi o Marcos:
*"eu não acredito que 10 folhas durem uma aula toda"*.
→ O gesto agora é lido no corpo da própria folha.

### 3.7 "2,6 palavras por segundo" era invenção minha
O tempo de voz saía de `palavras / 2.6`. Esse 2,6 **eu inventei**, sem cronômetro
e sem fonte, e ele saía no log com cara de medida. **Medido em 890 mp3: a voz da
casa fala a 1,66–1,90 palavra/s — meu número era 37% rápido demais.**
→ `_qa/mp3_dur.py` lê a duração REAL contando os quadros do próprio arquivo.

### 3.8 O intruso que começava com a mesma letra
A folha dizia *"três começam com o mesmo pedacinho"* e mostrava MALA · MENINA ·
MOLA · MORCEGO. As três primeiras **não** começam com o mesmo pedacinho (MA, ME,
MO); o que têm em comum é a **roda**. E o intruso, *morcego*, **começa com M**: a
criança que o aceitava estava certa no que enxergava, e o app dizia que errou.

### 3.9 As folhas de ORIGEM também erram
Duas das 26 folhas colhidas ensinam separação silábica errada: **PORCO** como
exemplo de PO (é POR-CO) e **CIRCO** como exemplo de CI (é CIR-CO). E uma folha
de rima dava **BOCA / GOTA** como par (é assonância, não rima).
→ **Folha da internet é matéria-prima, não fonte confiável.** Toda palavra do
pote tem a separação declarada à mão e conferida.

### 3.10 Portão que acusa inocente se aprende a ignorar
O `silaba_fonte.py`, na estreia, acusou **21 recortes legítimos**. O
`resposta_impressa.py` acusou a folha cujo enunciado diz *"some a **letra** com a
vogal"* porque "LETRA" começa com "LE". → Toda regra nova de portão nasce com o
caso-limite conferido antes de entrar na banca.

### 3.11 Halo branco do recorte
15 figuras com a orla do fundo grudada na silhueta — invisível no branco, um
contorno leitoso no fundo colorido da folha. → `_padrao/tirar_halo.py` (inunda a
partir da BORDA, por vizinhança, com degradê: o branco de dentro da figura fica
intacto).

### 3.11b ⭐ RECORTE DA FOLHA DE PAPEL: o portão do halo tem UM falso positivo, e ele é conhecido (14/set/2026, cinco reinos)
Das 45 figuras recortadas das folhas de papel dos reinos, **dez** saíram com halo.
Nove eram halo de verdade — a **franja de antialiasing** do escaneamento, pixels
entre 210 e 237, que o `limpa_fundo` (corta acima de 238) não alcança. O conserto
é o **`tira_halo`**: em vez de um segundo flood-fill mais frouxo (que comeria a
nuvem inteira, porque o corpo dela é quase branco), morde **só o que ENCOSTA no
transparente**, no máximo 4 px para dentro. Dez caíram para três.

As **três que sobraram não são halo**: são desenhos de traço com a silhueta
**VAZADA** — o chapéu do cogumelo, a asa rendada da mariposa, a nuvem. O flood do
portão entra pelos buracos do próprio traço e conta o branco de DENTRO como fundo
que sobrou; a erosão de 3 px não salva porque essas áreas brancas são finas de
verdade. **Olhadas num fundo escuro, as três estão limpas.**

→ O portão ganhou a **exceção declarada `<pasta>/img/HALO-OK.json`**: uma linha
por figura, com o MOTIVO escrito. Ele continua reprovando figura nova; passa só o
que alguém OLHOU e assinou, e ainda imprime as três com a porcentagem e o motivo,
para ninguém dizer depois que "passou limpo". ⚠️ Isto **não** é desligar portão —
é a diferença entre *"não medi"* e *"medi, vi, e este caso o portão não sabe
distinguir"*. Desligar seria clarear a figura para enganar o limiar.

### 3.11c A linha da moldura que sobra colada na beirada (14/set/2026)
Depois do `tira_moldura` e do `aperta`, **doze** das 45 figuras ainda saíram com
um risco na beirada: a linha da célula da tabela (d20/d22, traço cheio à direita)
ou o tracejado de recortar (d26). No contato-folha ele aparece como um risco solto
ao lado do desenho. → **`tira_risco`**, que corta as quatro beiradas girando a
figura 4×, com duas travas MEDIDAS: **grossura** (risco de moldura tem 1–3 px;
acima de 4 é desenho e fica) e o **VÃO** (entre o risco e a figura há papel
branco; sem pelo menos 2 linhas vazias depois não é risco solto, e sim o próprio
desenho encostando na beirada — é o que salva a base do monte de terra).
⚠️ E o "vazio" tem que ter **folga** (3% da largura), não ser zero cravado: logo
abaixo do traço sobram dois ou três pixelzinhos de tinta esfarelada, e exigir zero
fazia a regra desistir justamente nas três figuras mais sujas.

### 3.11d ⭐ O `riscoDeCircular` DEVOLVE A CHAVE, não o botão (14/set/2026)
Nos cinco reinos as duas folhas de circular (a 1 e a 21) não fechavam **nunca**,
mesmo circulando certo, e o console cuspia oito `TypeError: Cannot read
properties of undefined (reading 'indexOf')`. O motivo: o ajudante só devolve o
ELEMENTO quando se passa um **array** de botões; passando um **objeto**
(`{chave: elemento}`), que é o caso normal, ele devolve a **CHAVE**. Eu escrevi a
volta esperando o botão. → A volta recebe `w` e busca `bts[w]`. ⚠️ Isto não dava
erro de sintaxe, não aparecia no print e o pré-voo passava; quem pegou foi o
**`_qa/joga_folha.js`**, que resolve o caderno item por item. É o que ele existe
para fazer.

### 3.11e ⭐ LIGAR COM RÓTULO REPETIDO É ARMADILHA, não exercício (14/set/2026)
A primeira versão das folhas de ligar dos reinos punha **três bichos num item
só** — e a coluna da direita saía com **"ANIMAIS" escrito três vezes**. O motor
casa por chave da FIGURA, não pelo texto: a criança que ligasse o cachorro na
segunda caixa "ANIMAIS" levaria erro **por ter acertado**. → Item de ligar leva
**um ser por reino**, sempre; nenhum rótulo se repete dentro do mesmo item.
⚠️ E isto nenhum portão pegou: apareceu porque o jogador da banca não conseguiu
resolver a folha e eu fui ver por quê. O portão que fecha esta família ainda não
existe — fica como dívida declarada.

### 3.11f O jogador da banca aprendeu duas peças novas (14/set/2026)
O `joga_folha.js` saía com **"NAO RESOLVI"** nas quatro folhas de GAVETA e
reprovava quatro dos cinco itens da folha de PINTAR. Nos dois casos a ignorância
era dele, não defeito da folha — as duas peças têm **dois toques**:
- **gaveta:** pega a peça, solta na gaveta. A folha passou a registrar a resposta
  como `p0>vivo p1>nao …` (qual peça em qual gaveta, e não só quais peças
  existem) e a peça publica `peca-<id>-p<i>`.
- **pintar por legenda:** escolhe a canetinha, depois pinta. A pétala publica
  `data-lapis="<cor>"` e o estojo já publicava `lapis-<cor>`.
→ Regra que fica: **peça de dois toques declara o par**, e quem monta a folha
ensina a peça ao jogador **no mesmo commit**. Enquanto não ensinar, aquilo é
dívida (código 2), nunca aprovação.

### 3.11g A régua do jogador quebrava quando a figura tem sublinhado (14/set/2026)
Depois de ensinadas as duas peças novas, o `joga_folha.js` ainda dizia "não
conheço a peça" nas duas folhas de LIGAR. Não era a folha: o id de um par é
`l<folha><etiqueta>_<chave da figura>`, e a régua lia a etiqueta com `(.+)`
**guloso** — então `l14a0_reino_fungi` virava etiqueta `a0_reino` e chave
`fungi`, e a ponta procurada não existia. Só quebra quando a chave da figura TEM
sublinhado (`reino_fungi`, `reino_monera`, `urso_pelucia`…), que é justamente o
caso deste caderno. → `(.+?)`, mínimo. ⚠️ Terceira vez que a lição aparece neste
arquivo: **quando o portão reprova em massa, a primeira suspeita é a régua.**

### 3.11h ⭐ O PORTÃO DA DURAÇÃO MEDIU 71 ONDE HAVIA 112 (14/set/2026)
O `_qa/duracao.py` exigia que o `};` do `var ITENS` viesse **colado** no
`/*ITENS-FIM*/`. O gerador dos cinco reinos passou a escrever um SEGUNDO var
dentro do bloco marcado (`FIGNOME`, o nome falado de cada figura) — e aí o
`json.loads` estourava, o portão caía no galho seguinte e media **71 itens onde
havia 112**, imprimindo *"duracao ok: enche a aula"* com o número errado. →
A âncora agora para no `};` do próprio objeto e não se importa com o que venha
depois **dentro** do bloco. ⚠️ **Portão que aprova com número errado é pior que
portão nenhum**, e é por isso que a conta à mão (somar os `pega(...)`) vale a
pena quando o número parece baixo.

### 3.12 A cartela voltou em MANCHA — e várias delas iguais
Na Rua do Mundo pedi a arte em **oito cartelas de seis peças**, todas com a
**mesma semente**. Vieram **duas imagens distintas** entre as oito (md5 igual em
c1=c3=c4=c6=c7 e em c2=c5=c8) e nenhuma servia: o que chegou foram manchas de
argila sem forma.

Duas causas, as duas medidas:
1. **Semente igual em pedidos parecidos devolve a MESMA imagem.** A receita da
   casa diz *"semente fixa POR CARTELA"* — uma por cartela, não **uma para
   todas**. Eu li "fixa" e esqueci o "por".
2. **O Flux não lê "seis objetos numa grade"** com uma lista numerada longa: ele
   funde tudo. A cartela existe para **economizar chamada PAGA** — e no caminho
   grátis (Pollinations) não há chamada paga. Uma peça por chamada custa o mesmo
   **zero** e é o que o modelo sabe desenhar.

→ **A regra, daqui para a frente:** cartela quando a chamada é paga (Gemini,
OpenAI); **uma peça por chamada quando é de graça**, sempre com **semente
diferente por peça**. A irmandade continua vindo do BLOCO DE ESTILO, que é o
mesmo em todas.

### 3.13 Um portão que só funcionava num caderno mede um caderno
O `_qa/resposta_impressa.py` lia as palavras do caderno em
`Object.keys(PAL)` — o dicionário dos cadernos de **alfabetização**. Num caderno
de Geografia, que guarda as moradias em `MOR`, o `PAL` não existe: o script
estourava no navegador e o portão imprimia **"NÃO MEDI"**, com código 2.
E "NÃO MEDI" **não é "passou"**: é *rodou cego*. Fosse eu confiar no resumo do
pré-voo, teria publicado sem que nada ali tivesse sido olhado.
→ As palavras agora saem das **próprias respostas** (`RESP`), que todo caderno
tem. Conferido: o `_roda1` continua passando com a regra nova.

### 3.14 `data-alvo` só valia DENTRO do item
Há folhas em que a coisa que a criança **toca** é a resposta visível — e isso é
a tarefa, não defeito: o caça-palavras imprime a lista do que procurar (a folha
de papel de origem também imprime), o poema mostra as palavras que ela tem de
**achar no texto**, e o mural mostra o nome da casa que ela **escolhe** (ali não
existe resposta errada). O portão reprovava os três.
→ A marca passa a valer **na raiz do item**, e os itens declarados são
**impressos no log**: declarado não é escondido.


---

### ⌨️ ERRO 15/set/2026 — **O TECLADO NÃO TINHA AS LETRAS ACENTUADAS** (e trancava a criança)

**O que acontecia.** O teclado da folha viva monta os botões de uma string
escrita à mão, e o filtro do teclado DE VERDADE usa a mesma string:

```js
var letras = "ABCDEFGHIJLMNOPQRSTUVXZÇÁÉÍÓÚ".split("");
```

Falta **K**, falta **W**, falta **Y** — e faltam **Ê, Â, Ã, Ô, Õ, À e Ü**.

**O que a criança vive:** ela abre a folha *"escreva a palavra certa"*, ouve
**PÊSSEGO**, digita P… e o **Ê não entra**. Nem tocando na tela (a tecla não
existe) nem no teclado do PC da escola (o `keydown` recusa a letra). Ela fica com
`PSSEGO`, a folha **nunca fecha**, e **não há erro nenhum no console**: o app
está funcionando exatamente como foi escrito. Ela tenta de novo até desistir, e
o professor vê "uma folha que travou".

**Por que nenhum portão via.** O `node --check` passa. O leiaute passa. O revisor
de texto passa. O **andarilho** (`andar_folha.js`) passa — ele ABRE a folha, não
a resolve. Quem pegou foi o **jogador** (`joga_folha.js`), e **só porque a
palavra sorteada naquele dia tinha acento**: com outra semente, passava batido.

**O conserto tem as duas partes.** O alfabeto virou
`ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÔÕÚÜÇ` nos dois lugares, e nasceu o portão
**`_qa/teclado.py` (1t)**, no pré-voo e na banca: ele cobra as 26 letras e os 13
sinais do português, **e** cobra que o teclado da tela e o filtro do teclado de
verdade usem o **mesmo** alfabeto — dois alfabetos diferentes é o mesmo defeito
com uma porta só, e a porta que sobra é justamente a do PC da escola.

> ⚠️ **DOZE CADERNOS JÁ NO AR REPROVAM NESTE PORTÃO** (medido em 15/set/2026):
> `_jogo1`, `_abc1`, `_roda1`, `_alfa1`, `_fra1`, `_ini1`, `_let1`, `_mont1`,
> `_rima1`, `_sil1`, `_som1` e o `_reinos`. **Não foram consertados** — mexer em
> atividade publicada é decisão do Marcos. Lá o defeito pode estar **dormindo**:
> ele só acorda quando uma palavra com acento chega ao teclado. Consertados
> foram os três em que eu estava trabalhando: `_ort5`, `_ort5b` e `_casa1`.

### 🔇 ERRO 15/set/2026 — **A FOLHA QUE FECHAVA SEM A CRIANÇA FAZER NADA**

A primeira versão do **ditado** (`_ort5b`, folha 19) fechava o item no toque da
palavra do quadro, **sem olhar qual ditado estava valendo**. Resultado: a criança
fechava a folha inteira tocando no quadro a esmo, sem ouvir uma palavra sequer.

**Uma folha que fecha sem a criança fazer o que ela pede não mede: ela mente** —
e mente para os dois lados, porque o relatório do professor sai dizendo que ela
domina o objetivo. Agora são dois toques, e o número (que dita) vem primeiro.

Não há portão para isto, e **é honesto dizer que não há**: nenhuma medida
distingue "fechou porque fez" de "fechou porque tocou". Quem responde é o crivo
e o olho de quem monta.

## 4. 📏 O TAMANHO DA SEQUÊNCIA — a conta, e por que 25 está certo

### O que foi MEDIDO (12/set/2026, com o relógio nos mp3 e o gesto lido da folha)

| Caderno | folhas | itens | duração | **min por folha** |
|---|---|---|---|---|
| O Desfile das Letras | 10 | 85 | 22–37 min | 2,2–3,7 |
| O Bando das Rimas | 10 | 80 | 24–41 | 2,4–4,1 |
| Bate-Palma das Palavras | 10 | 99 | 26–42 | 2,6–4,2 |
| A Tecla do Espaço Quebrou | 10 | 81 | 26–43 | 2,6–4,3 |
| O Grande Jogo das Palavras | 10 | 79 | 26–47 | 2,6–4,7 |
| A Família das Palavras | 10 | 95 | 29–43 | 2,9–4,3 |
| O Som que Abre | 10 | 103 | 30–51 | 3,0–5,1 |
| A Máquina de Juntar | 10 | 105 | 31–48 | 3,1–4,8 |
| A Letra que Muda Tudo | 10 | 99 | 31–51 | 3,1–5,1 |
| **A Roda das Sílabas** | **15** | 103 | **34–53** | 2,3–3,5 |

### A conta
A faixa existe porque há **duas crianças reais** na turma: a que só ouve o
retorno ("muito bem!") e a que toca no alto-falante de cada opção, erra, ouve a
dica. Entre uma e outra há **20 minutos** numa atividade de 1º ano.

Para a aula de 55 minutos:

| | folhas necessárias |
|---|---|
| pela criança **rápida** (só o retorno) | **18 a 25** |
| pela criança **devagar** (toca em tudo) | 11 a 16 |

> ⚠️ **SEGUNDA CORREÇÃO DO MESMO TIPO, no mesmo dia.** Eu tinha escrito aqui que
> a Máquina de Juntar tem 8 folhas e a Letra que Muda Tudo tem 7. **Têm 10 cada
> uma.** O número saiu de um `grep` no `novaFolha()` que não reconhecia todas as
> formas de sacar o pote. **Contagem de folha agora se faz no NAVEGADOR**
> (`PAGEL.length - 1`), que é onde a criança conta — a mesma lição da Regra
> Zero: se o modelo não foi aberto, o número mede o meu regex.
> Medido em 12/set: nove cadernos com **10 folhas** e a Roda com **15**.

**Por isso 25 é o número certo — e o Marcos chegou nele de ouvido.** Com 25
folhas a criança rápida enche a aula; com menos, ela termina com meia aula
sobrando, que foi exatamente o que ele viu.

### ⚠️ MAS 25 FOLHAS COBRA UMA MUDANÇA JUNTO, e sem ela faz mal

Se a criança rápida enche a aula com 25 folhas, a criança devagar leva **~85
minutos** — ela **não termina**. E hoje o fecho (o boletim animado, o parecer, o
relatório do professor, a medalha) **só existe depois da última folha**. Ou seja:
a criança mais lenta da turma, que é justamente quem mais precisa do elogio,
seria a única que nunca o veria.

**Então a regra completa é:**
1. **25 folhas no mínimo** — o pote do dia.
2. **O fecho tem que ser alcançável a qualquer momento.**
3. **O convite de 55 minutos continua** (`_padrao/RETOMAR.md`): quem volta na
   mesma aula continua de onde parou.

### ✅ O item 2 está FEITO nos dez cadernos (12/set/2026)

Sem ele, aumentar para 25 folhas pioraria a vida de quem já vai devagar — a
criança mais lenta da turma seria a única a nunca ver o próprio elogio. O que
mudou, e é contrato do formato daqui para a frente:

| | Como era | Como é |
|---|---|---|
| chegar ao fecho | só depois da última folha | **botão "Terminar"** na barra de baixo, a qualquer momento |
| título do fecho | "Caderno completo!" | "**O seu boletim de hoje**" quando não terminou |
| folha não aberta | barra com **0 de 8** | "**ainda não**", apagadinha — nunca um zero |
| estrelas e barras | sobre o caderno inteiro | **sobre o que ela tentou** |
| parecer da criança | objetivo não alcançado caía em "vale treinar" | **não entra em lista nenhuma** |
| a linha de resumo | — | "*Ana, você fez 4 de 15 folhas hoje — e olhe o que já dá para ver…*" |
| voltar | impossível | **"Voltar para o caderno"**, se ainda houver aula |
| relatório do professor | 4 folhas bem feitas viravam **"Precisa retomar"** | aviso de caderno não terminado + coluna **"do que fez"** + nota sobre o que foi feito + "*ainda não chegou a fazer (a aula acabou antes)*" |

⚠️ **O relatório era o pior dos dois.** Ele dividia os acertos pelo caderno
inteiro: quem fez 4 de 15 folhas, e as fez bem, aparecia com **21%** e conceito
**"Precisa retomar"**. Um julgamento errado com cara de medida, exatamente o que
a Regra Zero proíbe — só que contra a criança.

⚠️ **Tensão que eu NÃO mexi, e que é decisão do Marcos:** a nota credita o acerto
com ajuda (1,0 de primeira, 0,6 com ajuda), mas a tabela por objetivo conta só o
acerto **de primeira**. Por isso é possível ler "**Dominou**" ao lado de "nenhum
objetivo chegou a 75%". Não é defeito novo — é como a nota sempre foi — mas para
o professor soa contraditório. Mudar o critério é escolha pedagógica, não minha.

**Medido nos dez** (12/set): fecho no meio do caderno funciona, nenhuma barra em
zero, "Voltar para o caderno" retorna, zero erro de JS; leiaute em 6 tamanhos
com todo alvo ≥ 40 px.

---

## 5. 🛠️ O PROCESSO — como nasce uma sequência (e a ordem importa)

### Passo 1 — COLHER as folhas de verdade
`buscar-fotos.yml` com `imagens=<o que procurar>` e
`destino=_sequencias/folhas_d<N>`. ~26 folhas por degrau.
> O chat não tem internet; a colheita roda no GitHub Actions.

### Passo 2 — O CRIVO, folha a folha, com olhar de pedagogo
**Ler cada folha e anotar UMA coisa: o VERBO** — o que ela manda a criança FAZER
com o lápis na mão. Depois o veredito, com o motivo escrito, no
`_sequencias/POTE-<NOME>.md`:

- ✅ **entra** — o gesto serve a este degrau;
- ⛔ **é de outro degrau** — ensina coisa de antes ou de depois;
- ⛔ **fora do ano** — o currículo de Blumenau põe isso noutro ano;
- ⛔ **sem tarefa** — é cartaz de parede;
- ⚠️ **erra** — a própria folha ensina errado (§3.9).

> **Exemplo do que isso rende:** no degrau 9, 26 folhas → 15 entram, 5 são de
> outro degrau, **4 ensinam as famílias do C e do Q, que Blumenau situa no 2º
> ano**, 2 são cartaz. E apareceram **cinco gestos** que o caderno não tinha.

### Passo 3 — MONTAR, fiel ao comando
Cada folha recria o gesto da folha de origem. Mecânica que repete vem em bloco
colado (§2). **Nada de escolher do nosso cardápio: a folha é que manda.**

### Passo 4 — A VOZ
`python3 <pasta>/gerar_falas.py` → escreve `falas.json`, `silabas.json`,
`voz.txt` e remenda os blocos `FALAS`/`VOZOK`/`SILMAP` no `index.html`.

### Passo 5 — MEDIR (nunca pular)
```
bash _qa/previo.sh <pasta>                 # 39 portões de texto, ~3 s
node _qa/andar_folha.js <pasta>            # anda o caderno inteiro no navegador
node _qa/leiaute_mao.js <pasta>/index.html # 6 tamanhos de tela
python3 _qa/resposta_impressa.py <pasta>   # a legenda entrega a resposta?
python3 _qa/duracao.py <pasta>             # enche a aula?
python3 _qa/pedagogo_curriculo.py <pasta>  # o currículo citado existe?
```
**E OLHAR A TELA** — foto de cada folha nova, no celular e no PC. Metade dos
defeitos desta lista foi achada assim, não por portão.

### Passo 6 — PUBLICAR
Commit com a marca **`[entregar _pasta:repo]`** na mensagem → o `entregar.yml`
acorda sozinho, grava a voz que falta, publica e deixa
`_status/entrega-<repo>.json`. **Conferir o carimbo** (`index` ×
`sha1sum <arquivo> | cut -c1-12`) antes de dizer que está no ar.

---

## 6. 🧱 A ANATOMIA DO CADERNO (para clonar sem herdar defeito)

```
<pasta>/
  index.html      capa + CSS + os POTES + FALAS/VOZOK/SILMAP + relatório + dossiê
  folhas.js       uma função por folha + os ajudantes + DISTRA + OBJETIVOS
  gerar_falas.py  escreve o falas.json a partir dos potes
  curriculo.json  a habilidade de Blumenau, verbatim, por objetivo
  falas.json      a VERDADE da voz
  silabas.json    de qual palavra cada sílaba é recortada
  img/            prefixo próprio (ro_, in_, jg_…)
  audio/          gravado pelo entregar.yml
```

**Blocos que o gerador remenda** (não editar à mão):
`/*ITENS-INI*/…/*ITENS-FIM*/` · `/*FALAS-INI*/…` · `/*VOZOK-INI*/…` ·
`/*SILMAP-INI*/…` · `/*RODAS-INI*/…` · `<!--<dossie-html>-->`

**Ao CLONAR um caderno, trocar SEMPRE:** o prefixo das imagens e do áudio, o
`var PAL`, os potes, o `var DISTRA`, os `OBJETIVOS`, o `curriculo.json`, o
`CHAVE_LS` (a gaveta do "continuar de onde parou"), o `sw.js` e o
`manifest.json`. O `_qa/clone.py` (item 8) reprova qualquer coisa com o prefixo
de outra pasta.

**Contrato do id:** `"n" + pi + "_" + i` dentro da folha; a folha de LIGAR usa
`"l" + pi + "g" + i + "_" + chave` e se declara na constante `LIGAR`. Nunca
escrever número fixo (§3.5).

**Contrato do alvo:** o que MOSTRA a resposta de propósito (a testa da gaveta, o
modelo da roda) leva `data-alvo="1"`. Tudo o que não se declarar é tratado como
enunciado, e no enunciado a resposta não entra (§3.1).

---

## 7. ⚠️ O QUE A BANCA **NÃO** ALCANÇA NESTE FORMATO

Honestidade que vale mais que um "aprovado": vários portões da banca são do
MOTOR e, em folha viva, dizem **"NÃO MEDI"** — o que **não é "passou"**:

| Portão | Por que não alcança |
|---|---|
| `jogador.js` · `prova de sala` | procuram `telaCapa`/`FASES` |
| `contraste` · `encaixe` · `imagens` | abrem telas por nome |
| `0a pedagogo` (escada didática) | lê a cadeia de fases |
| `0b padrão da casa` (leque de gestos) | conta fases, não folhas |
| `entrega` · `enunciado_bate` · `figura_certa` | precisam de `conteudo.json` |

### ⭐ E AGORA EXISTE UMA BANCA PRÓPRIA: `bash _qa/auditar_folha.sh <pasta>`

Pergunta do Marcos (13/set/2026), depois de eu dizer que a `auditar.sh` tinha
reprovado o caderno de moradia e que metade daquilo "não era deste formato":
*"Mas tem banca para esse tipo de atividade?"* — e a resposta honesta era **não**.

O que existia era esta tabela, escrita, mais a minha memória para escolher quais
portões rodar. Memória não é portão: é o defeito que este projeto inteiro
combate, e é pior que portão nenhum, porque leva a chamar de "aprovado" o que
ninguém mediu.

Agora é um comando só — eram **13 portões em ~18 s** na estreia, hoje são **19**
(o pré-voo, que é um deles, sozinho carrega 43) — e ele imprime três grupos:
**passou** (código 0, medido), **NÃO MEDIU** (o portão rodou e não achou o que
medir — isto não é "passou", e aparece na tela para ninguém confundir silêncio
com aprovação) e **não alcança** (os do motor, com o motivo escrito ao lado, para
a ausência ficar visível). Ele só diz APROVOU com 0 em todos, e o rodapé repete,
toda vez, o que nenhum portão mede ainda (a escada didática e o leque de gestos —
tarefa #104).

Tem também o portão do próprio portão: se a pasta não tiver `PAGEL` nem
`folhas.js`, ele PARA e manda usar a `auditar.sh`. Rodar a banca da folha viva
num app do motor daria uma enxurrada de "não medi" que alguém leria como
aprovação.

### 🩹 O QUE A ESTREIA DA BANCA CONSERTOU (13/set/2026)

| Defeito | Onde | Conserto |
|---|---|---|
| **Halo branco** — o papel da folha grudado na silhueta | **os onze**, 517 figuras | `_padrao/limpar_halo.py`, com as **mesmas duas réguas** do `_qa/halo.py` escritas no cabeçalho. Foi a divergência entre elas que criou o defeito: eu media com uma e apagava com outra |
| **Portão que ESTOURA** (`int.upper()`) quando a resposta é número | `_alfa1`, folha "Quantas sílabas?" | `resposta_impressa.py` pula resposta que não é palavra. ⚠️ Portão que estoura é o pior tipo: acusa a atividade de um defeito que é **dele** |
| **A palavra escrita entregava a resposta** — a tela mostrava JANELA e pedia para pintar JA | `_alfa1`, folha 6 | a palavra virou segredo até o acerto (o alto-falante fica). É a mesma lição da MOLA na Roda |
| **Não enchia a aula** (22–37 min; piso 40) | `_abc1`, `_alfa1` | pote com o **alfabeto inteiro** (era 10 de 26 letras) e saque maior. 30–42 e 32–54 |
| **Cor cravada sem fundo** (portão 4c) | `_alfa1` | herdar; as duas regras só repetiam à mão o preto do `body` |
| **Sete palavras do pote SEM VOZ** — e fui eu que criei, no mesmo commit em que aumentei o pote | `_abc1` | as sete falas escritas; e o portão novo **`_qa/voz_do_pote.py` (0i2)**, que confere o pote INTEIRO |

#### ⚠️ O portão `0i2` nasceu de um erro meu, e a lição é sobre SORTEIO

Ao pôr o alfabeto inteiro no pote do Desfile das Letras, entraram sete palavras
novas com figura — **e nenhuma com voz**. Num caderno de 1º ano a voz não é
enfeite: a criança que ainda não lê aperta o alto-falante para saber o que é a
figura. Se o sorteio lhe desse "xícara", ela apertava e não vinha nada.

**Por que nenhum portão viu:** a folha é SORTEADA, e o `andar_folha.js` anda UMA
tirada. Numa tirada de 12 entre 23 palavras, a chance de não cair nenhuma das
sete é alta. **Portão que depende de sorte não é portão: é aposta.** O `0i2` não
sorteia — confere o pote inteiro, item por item.

E ele custou duas versões erradas antes de ficar de pé, o que também é lição:
a primeira juntava todos os textos do pote num saco só e adivinhava a família
pelo tamanho (416 acusações falsas na moradia); a segunda separou por campo mas
ainda cruzava folhas (`perg12_` cobrado da folha 10). A terceira lê o
`folhas.js` **função por função** e só cobra de `pN` os prefixos que aparecem
dentro de `fN` — e ainda exige que a MAIORIA do campo já seja falada com aquele
prefixo, senão se cala. **"Não medi" é melhor que acusar inocente**: portão que
acusa inocente é portão que se aprende a ignorar.

⚠️ **O remendo da duração NÃO é a regra das 25 folhas.** Os dez cadernos de
alfabetização têm 10 a 15 folhas; só a moradia tem 26. A **tarefa #105 continua
aberta** e é ela que fecha isso de verdade — com folhas novas, tiradas do crivo,
e não com saque maior.

**⚠️ NA ESTREIA ELE REPROVOU OS ONZE CADERNOS**, dez deles já no ar: os onze com
**halo branco** no recorte (o papel da folha grudado na silhueta), o `_abc1` e o
`_alfa1` também na duração e no pré-voo, e o `_alfa1` ainda na resposta impressa.
Nenhum desses defeitos era novo — eles estavam lá desde sempre, e ninguém os via
porque não havia um comando que olhasse. Isso é o argumento a favor da banca, não
contra ela.

**O que cobre a folha viva hoje** (é a lista que vive dentro do `auditar_folha.sh`;
portão novo que passe a alcançar este formato entra LÁ no mesmo commit, senão ele
existe e ninguém roda): `previo.sh` (39 portões de texto), `boot.js`,
`andar_folha.js` (anda tudo, erro de JS e figura quebrada), `leiaute_mao.js`
(6 tamanhos, alvo ≥ 40 px), `resposta_impressa.py`, `duracao.py`,
`pedagogo_curriculo.py`, `halo.py`, `clone.py`, `duplicatas.py`, `revisor.py`,
`catalogo.py`, `figura_da_folha.py`, `sobra_da_folha.py`, `node --check`. Fora da
banca, por rodarem no Actions: `pronuncia.py` (ASR) e `silaba_fonte.py`.

### ✂️🧾 A PAUTA DA FOLHA VEIO JUNTO — portão 1i6 (14/set/2026)

Palavras do Marcos, olhando os cinco reinos no ar: *"a atividade do reino, tem
resto de outras imagens nas imagens, e imagens que faltam partes, resolva por
favor"*. E logo depois, quando eu ainda tateava: *"já falei mil vezes, não chute
nem ache nada, faça para não haver erros"*.

**A causa não foi descuido, foi método errado.** A folha de papel não traz só o
desenho: traz o **quadradinho de marcar** ao lado dele, a **moldura tracejada**
de recortar, a **linha que separa as colunas** da tabela. Eu recortava dividindo
a folha numa **grade regular medida no olho** — e grade chutada erra dos dois
lados ao mesmo tempo: larga demais traz o vizinho, apertada demais come a figura
(o urso sem os pés, o elefante sem as pernas, o bebê cortado). Depois eu conferia
numa folha de contato de **130 px por figura**, onde nada disso aparece. Conferir
em miniatura não é conferir: é se tranquilizar.

**O que ficou no lugar disso, e tudo medido na própria folha:**
1. **A caixa sai da TINTA**, não de uma grade — ilhas de tinta, ou o interior da
   moldura impressa quando a folha tem uma. E se o número de caixas não bater com
   o número de nomes, o recortador **PARA** em vez de casar no escuro.
2. **`apaga_quadradinhos`** mata o quadradinho na FOLHA, onde ele ainda é um dos
   vinte quadrados iguais de uma grade 4×5 (medidos 19 dos 20; o vigésimo, que
   estava grudado no monte de terra, sai do cruzamento das colunas e linhas que
   os outros dezenove formam). No recorte já seria tarde: lá o quadradinho e o
   rabo do passarinho são **um componente só**.
3. **`tira_linha_impressa`** mata o tracejado e a régua da tabela, por tamanho
   (≤ 0,5% do corpo, encostado na beirada) e por forma (traço de ≤ 4 px que
   atravessa 90% de um lado). Entre o maior risco (0,19%) e a menor parte de
   desenho que também encosta na beirada (o raio do sol2, 1,83%) há folga de 10×.
4. **A folha de contato sai SEMPRE, a 300 px** e em lotes de 12.

**O portão: `python3 _qa/sobra_da_folha.py <pasta>` (1i6)**, no pré-voo e na
banca. Rodado nas figuras do commit anterior, reprovou 8 — entre elas a árvore
com a moldura em volta e o reino animal com a linha da coluna atravessando.

⚠️ **E ele diz, na própria tela, as DUAS coisas que não vê** — porque tentei
medir as duas e as assinaturas se confundem com figura limpa:
- **quadradinho fundido no desenho**: passarinho sujo e passarinho limpo dão o
  mesmo número (8 px de corrida, 13% de coluna);
- **figura cortada**: o urso truncado deu 67% de tinta na beirada, e o menino
  INTEIRO dá 67% também; a água, que é um retângulo, dá 100%.
Para esses dois, a defesa é **olhar a folha de contato** — e é por isso que ela
passou a sair sozinha e grande. Um "ok" do 1i6 **não** quer dizer que alguém
olhou as figuras.

⚠️ **Lição de método, e esta doeu:** no meio do conserto eu declarei que o
`reino_animal` já estava limpo — tinha medido o PNG e ele tinha um componente só.
Estava limpo **por causa de uma exceção pelo nome dele** numa lista que eu estava
justamente apagando. Exceção pelo nome não é conserto: é um bilhete para não
esquecer. A lista `SOBRA_COLADA` tinha cinco nomes e hoje está **vazia de
propósito** — os cinco viraram duas medidas que valem para qualquer folha.

**A dívida (tarefa #104) — PAGA em 13/set/2026, e só pela metade que dá para
medir.** Nasceu o **`_qa/leque_folha.py` (portão 0b7)**, dentro da banca: ele
conta o gesto de cada folha e reprova se um só gesto passar de **40%**, se o
caderno tiver menos de **4 gestos** diferentes, ou se a **escada descer** (o
último terço mais leve que o primeiro). O peso vem importado do `duracao.py`, e
é PALPITE DECLARADO — nunca cronometrado com criança.

⚠️ **O gesto é DECLARADO pelo caderno, não adivinhado do código**, e essa foi a
lição mais cara do arquivo, paga na primeira hora de vida dele. A primeira
versão lia o gesto do corpo da `fN` reusando o classificador do `duracao.py` —
parecia elegante (uma régua só) e era falsa: *"Ligue cada figura ao seu pedaço"*
saía como **arrastar**, *"Pinte só os balões deste pedacinho"* saía como
**ligar**. Para o relógio isso não importa (erra 5 s e a soma continua na ordem
certa); para dizer QUAL é o gesto, importa tudo — e o portão chegou a reprovar
três cadernos por conta do próprio erro. Agora cada `index.html` traz um bloco
`/*GESTOS-INI*/ var GESTOS = {"f1":"..."}` escrito pela mão de quem monta, como
já são o `LIGAR` e o `curriculo.json`. Sem declaração o portão diz **NÃO MEDI**,
que aparece na banca como dívida e não como carimbo.

⚠️ **O que ele continua NÃO medindo, e eu não vou fingir que mede:** se o
CONTEÚDO sobe — sílaba simples antes da complexa, palavra curta antes da
comprida, o degrau do currículo. O peso do gesto é um proxy honesto e está dito
assim na tela. Quem responde pelo resto continua sendo o crivo do `POTE-*.md` e
o professor.

**⚠️ E a banca deixou de carimbar o que não mediu (13/set/2026).** O
`auditar_folha.sh` imprimia *"NÃO MEDIU — isto não é passou"* no meio da tela e
**"BANCA APROVOU"** no fim, na mesma corrida — e é a última linha (o código de
saída) que o script chamador lê. Portão cego ia embrulhado como aprovação. Agora
qualquer 2 segura o veredito em **"BANCA NÃO CONCLUIU"**, código 2.

---

## 8. 📋 O ESTADO DE HOJE (12/set/2026) — e a fila

| Degrau | Caderno | Folhas | Duração | Crivo com o VERBO? |
|---|---|---|---|---|
| 0 | **O Desfile das Letras** | **25** | 41–80 | ✅ **24 folhas**, `POTE-ABC.md` |
| 1 | O Bando das Rimas | 10 | 24–41 | ✅ **28 folhas, 12/set** |
| 2 | Bate-Palma das Palavras | 10 | 26–42 | ✅ |
| 3 | A Família das Palavras | 10 | 29–43 | ✅ |
| 4 | O Som que Abre | 10 | 30–51 | ✅ |
| 5 | A Máquina de Juntar | 10 | 31–48 | ✅ |
| 6 | A Letra que Muda Tudo | 10 | 31–51 | ✅ |
| 7 | A Tecla do Espaço Quebrou | 10 | 26–43 | ✅ |
| 8 | O Grande Jogo das Palavras | 10 | 26–47 | ⛔ **sem colheita própria** (a colheita já chegou: `folhas_d8`) |
| 9 | **A Roda das Sílabas** | **15** | 34–53 | ✅ 26 folhas |

**E há uma sequência FORA da alfabetização** (13/set/2026), a primeira do
formato em outro componente:

| Ano | Caderno | Folhas | Duração | Crivo com o VERBO? |
|---|---|---|---|---|
| 2º · Geografia | **A Rua do Mundo** (tipos de moradia) | **25** | 39–69 | ✅ 30 folhas, `POTE-MORADIA.md` |

> ⭐ **É o primeiro caderno a cumprir a REGRA DO TAMANHO** (25 folhas) e o
> primeiro com **dezenove gestos diferentes** — nenhum passa de duas folhas.
>
> ⚠️ **E ele trouxe uma lição que vale para toda sequência nova:** o crivo
> mostrou que **22 das 30 folhas de papel param no degrau do ANO ANTERIOR**
> (pedem só o nome da moradia, que em Blumenau é habilidade do 1º ano). Quando
> isso acontece, **quem manda deixa de ser o pote e passa a ser o currículo**:
> quatro blocos deste caderno (a visão vertical, o tempo, o porquê do material
> e o porquê do lugar) não existem em folha impressa nenhuma do pote — nasceram
> da rede. A REGRA DA ORIGEM continua valendo; ela só não pode rebaixar o ano.

> ⭐⭐ **E ELE É O PRIMEIRO CADERNO DE ALFABETIZAÇÃO A CUMPRIR A REGRA DO
> TAMANHO** (13/set/2026): saiu de 11 para **25 folhas**, com **15 gestos** e
> nenhum passando de **24%**. As catorze folhas novas vieram todas do comando
> impresso — a lista está no `POTE-ABC.md §3`, com a folha de papel de cada uma.
> O que ele ganhou, e que não existia em caderno nenhum da sequência:
>
> | folha nova | de onde veio | o que a criança faz |
> |---|---|---|
> | O poema do alfabeto | d09 "VAMOS LER JUNTOS?" | ouve o poema e **acha a letra na tira de 26**, sem três opções |
> | O alfabeto pequeno · A mesma letra, pequenininha | d12 | a **minúscula**, que o caderno inteiro ignorava |
> | Quem vem ANTES | d08 | voltou como folha própria, colada no "depois" |
> | A letra do MEIO | d13 "ANTES, **ENTRE** E DEPOIS" | segura as duas pontas ao mesmo tempo |
> | **Escreva a vizinha** | d01, d03, d06, d16 | **digita** a letra, teclado da tela e o de verdade |
> | A grade do alfabeto | d09, d17 | o quadro com buracos, não a fila |
> | **O teclado fora de ordem** | d19 | as letras do **teclado do PC da escola**, em QWERTY |
> | Mesma letra no começo | d05 | ordena pela **segunda** letra |
> | Quem vem primeiro no dicionário | d04 "PINTE A PALAVRA QUE VEM PRIMEIRO" | pinta a 1ª das duas |
> | A gaveta de cada palavra | d18, d21 | uma gaveta por letra — a ideia do índice |
> | As figuras em ordem alfabética | d02 | ordena FIGURAS, dizendo o nome para si |
> | Os nomes da turma em ordem | d24 | a **chamada** da sala |
> | Pratique a escrita do alfabeto | d15 | **traça a letra com o dedo** e o app mede a cobertura |
>
> ⚠️ **A folha mais importante da lista é a de DIGITAR**, e por um motivo
> constrangedor: *escrever a letra vizinha* é o verbo mais pedido do pote (seis
> das 24 folhas de papel) e o caderno pedia isso **zero vezes**. Todas as nossas
> folhas de vizinhança eram de escolher entre três. Escolher entre três é
> reconhecer; escrever é produzir. Era o meu cardápio mandando, não o pote.
>
> ⚠️ **E o preço da regra do tamanho, medido:** 11 folhas de 12 itens dariam,
> em 25, quase 300 itens e três aulas. O saque de cada folha teve que ENCOLHER
> (de 10-12 para 4-6). O que enche a aula é o número de FOLHAS — a criança sente
> que andou; lista comprida da mesma coisa é o "isso eu já fiz". Deu 135 itens.

**Só um caderno de alfabetização chega às 25 folhas** — o Desfile. O seguinte, a Roda, tem 15.
(A Rua do Mundo, de Geografia, nasceu já com 25.) **Nove de dez têm o
crivo do verbo**; falta só o degrau 8, cuja colheita já está em `folhas_d8`.

> **O degrau 0 saiu da fila em 13/set/2026.** Colhi **45 folhas de papel** de
> sequência alfabética (`_sequencias/folhas_d0`) e o comando impresso delas
> mandou fazer duas coisas que o Desfile não fazia:
> - **`CIRCULE O NOME QUE ESTÁ FORA DA ORDEM EM CADA GRUPO`** (folha d14) →
>   virou a **folha 5, "Qual palavra está fora da ordem?"**, que substituiu uma
>   folha de escolher que era a quinta seguida do mesmo gesto e repetia o que a
>   folha 6 já pedia.
> - **pôr PALAVRAS (não letras) em ordem alfabética** → virou a **folha 10,
>   "Palavras em ordem alfabética"**, clonando a mecânica de ordenar da folha 7.
>
> É a REGRA DA ORIGEM funcionando como o Marcos a escreveu: *"as
> interatividades têm que vir das atividades que você seleciona na internet, o
> que as atividades pedem para o aluno fazer, então você dá essa
> interatividade"*. Eu não inventei os dois gestos — li o comando impresso.
> Resultado medido pelo 0b7: o Desfile passou de **5 para 7 gestos** e o
> "escolher" caiu de 55% para **36%** (o teto é 40%).

> ⚠️ **CORREÇÃO, e ela é lição de método (12/set/2026).** Eu disse ao Marcos que
> só **quatro** de dez tinham crivo. Estava errado: contei com um `grep` que só
> reconhecia UM formato de tabela, e os `POTE-MONTAR`, `POTE-LETRA`,
> `POTE-FRASE` e `POTE-SOM` usam outro (*"As folhas que viraram folha, uma a
> uma"* + *"As folhas RECUSADAS — e o motivo de cada uma"*). É a **Regra Zero**
> me pegando: rodei uma medida sem abrir o modelo dela e repeti o número.
> O conserto de processo: **antes de contar arquivo com `grep`, abrir dois deles
> e ver se o padrão casa** — senão a contagem mede o meu regex, não o repositório.

### A fila, na ordem
1. **O fecho alcançável a qualquer momento** (§4) — vem antes das folhas novas,
   senão 25 folhas piora a vida de quem vai devagar.
2. **Crivo** dos degraus que não têm: **faltam só o 0 e o 8**. O degrau 1 foi
   feito em 12/set (28 folhas lidas uma a uma, `POTE-RIMA.md` §crivo — achou
   **seis** gestos que o caderno não faz, sendo o maior deles **PRODUZIR rima**,
   que quatro das 28 pedem e o nosso caderno não pede nenhuma vez). A colheita
   do 8 já está em `_sequencias/folhas_d8`; a do 0 ainda não foi feita.
3. **Crescer cada caderno até 25 folhas**, na ordem do mais curto.
   O degrau **0 está feito** (13/set): 11 → 25 folhas, catorze delas tiradas do
   comando impresso. Faltam os degraus 1 a 9 — e o caminho está provado: ler o
   crivo do `POTE-*.md`, pegar os verbos que ficaram de fora, clonar a mecânica
   de quem já a tem, encolher o saque de cada folha e medir com a banca.
4. **Portão da escada didática e do leque de gestos** para folha viva (#104).

---

*Escrito em 12/set/2026. Toda regra nova do Marcos e todo erro novo entram aqui,
no mesmo commit em que forem descobertos.*
