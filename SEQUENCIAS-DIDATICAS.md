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

## 2. ⭐⭐ AS REGRAS DO MARCOS — ditas por ele, com as palavras dele

### REGRA ZERO — "Nunca chute nunca invente" (12/set/2026)
Quatro palavras, e vêm antes de todas as outras. Número sem fonte não sai da
minha boca; **e "li no log" só vale se eu tiver aberto o MODELO que gerou o
log**. Constante inventada dentro de portão tem que estar escrita no comentário
**e impressa na saída** como `PALPITE DECLARADO`. O que não dá para medir daqui,
eu digo que não dá e mostro quem pode medir. E nunca dizer que fiz o que não fiz.
> *O teste, antes de mandar qualquer número:* **de onde veio, e o que eu teria
> que abrir para ele estar errado?**

### REGRA DO TAMANHO — no mínimo **25 folhas** por sequência (12/set/2026)
Palavras dele: *"eu acredito que cada sequência precise de no mínimo 25 folhas"*.
**A medição dá razão a ele** — a conta está no §4. O mínimo é 25; a meta de
tempo é a aula de **55 minutos**.

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

## 3. ⚠️ OS ERROS JÁ PAGOS NESTE FORMATO — um por um

> Esta lista existe para não se repetirem. Cada linha custou uma rodada com o
> Marcos, ou chegou até a criança.

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

Agora é um comando só, **13 portões em ~18 segundos**, e ele imprime três grupos:
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
`catalogo.py`, `node --check`. Fora da banca, por rodarem no Actions:
`pronuncia.py` (ASR) e `silaba_fonte.py`.

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
