# 🔤 ALFABETIZAÇÃO — o que funciona, e o que virou regra nas nossas peças

> Pedido do Marcos (set/2026), palavras dele: *"Estude dinâmicas para
> alfabetização também, que funcionam e são pedagógicas. O programa EdiLIM tem
> bastante dinâmicas interativas em suas páginas… Precisamos que nas atividades
> diminuam muito os erros, estude muito todas essas dinâmicas encontradas, essas
> interatividades, para ficarem perfeitas."*
>
> **Matéria-prima lida** (tudo trazido pelo `pesquisar.yml`, a internet do GitHub):
> - `_pesquisa/web/alfabetizacao-jogos-com-evidencia-brasil.md` — GraphoGame Brasil
>   (MEC / Tempo de Aprender / PUCRS), avaliações reais de professores na loja,
>   Elefante Letrado.
> - `_pesquisa/web/alfabetizacao-jogos-com-evidencia-internacional.md` — Teach Your
>   Monster to Read (Usborne Foundation; minijogos descritos um a um), GraphoGame
>   (HundrED, Learning Cabinet: os RCTs, inclusive o que NÃO deu efeito).
> - `_pesquisa/web/alfabetizacao-ciencia-da-leitura-principios.md` — os cinco
>   pilares (National Reading Panel 2000), *Simple View of Reading* (Gough &
>   Tunmer), mapeamento ortográfico (Ehri), e o PDF do **NCIL** (*How to Use
>   Systematic Phonics Instruction in Your Classroom*, National Center on
>   Improving Literacy, 2024) — o mais operacional de todos.
> - `_pesquisa/web/alfabetizacao-brasil-dinamicas.md` — consciência fonológica na
>   prática brasileira (rima, aliteração, segmentação, bingo dos sons, intruso
>   pelo som, letras móveis).
> - `_pesquisa/web/casa-edilim-manual-e-paginas.md` — o **manual oficial do
>   EdiLIM** (PDF, 18 pág.) lido de novo, agora com o `pypdf`, página por página.
>   Complementa `_pesquisa/EDILIM-DINAMICAS.md` (ago/2026).
>
> **Isto é destilado em REGRA e em CÓDIGO.** As três lapidações do §4 já estão
> nas peças-fonte, medidas na bancada. O que é peça nova ou decisão de conteúdo
> fica no §6 para o Marcos decidir.

---

## 1. A escada que a ciência da leitura desenha (e onde as nossas peças pisam)

Os cinco pilares (NRP 2000) e a ordem em que a criança sobe:

| degrau | o que é | a nossa peça |
|---|---|---|
| **consciência fonológica** (de olhos fechados: só som) | ouvir e mexer nos pedaços da fala — frase → palavra → sílaba → rima → fonema | `bater-silabas`, `juntar-silabas`, `rima`, `som-inicial`, `caixas-de-som` |
| **princípio alfabético / fônica** | ligar cada som à letra que o escreve, de forma **explícita, sistemática e cumulativa** | `tracar-letra`, `letras-escondidas`, `ditado`, `completar`, `forca` |
| **decodificação → fluência** | juntar os sons de volta numa palavra, depois sem parar entre eles ("keep the motor running") | `juntar-silabas` (fonação conectada), agora `caixas-de-som` (ler a palavra) |
| **vocabulário / compreensão** | o que a palavra quer dizer; ler para fazer algo | `montar-frase`, `caca-palavras`, `cruzadinha`, `ouvir-achar`, (proposta: `ler-e-fazer`) |

A **Visão Simples da Leitura** (Gough & Tunmer): compreensão = reconhecer a
palavra × entender a língua. Uma atividade de 1º ano que só faz o lado direito
(figuras, sentido) sem o esquerdo (som → letra) não alfabetiza; a nossa Padaria
e o nosso Trem estão do lado certo, e é por isso que a peça mais importante da
casa é a `caixas-de-som`.

---

## 2. O que as casas que funcionam fazem — e o que os professores reclamam delas

### GraphoGame (Finlândia → Brasil pelo MEC; 300+ publicações, RCTs)
**O que faz:** letra-som e sílaba-som por escolha rápida com ÁUDIO como pergunta;
**adapta o nível** à criança; **interface que não exige ler** (setas grandes,
ícone que acende, tutorial); a voz explica a tarefa ("escolha a sílaba que rima
com o que você ouviu"); 15 min, 3× por semana; funciona **sem adulto na sala**;
avatar próprio. Efeito forte em quem estava atrasado, e nos meninos.
**O que NÃO fez:** o RCT inglês do *GraphoGame Rime* em crianças de 2º ano com
baixa leitura **não mostrou efeito** sobre o apoio normal da escola. Ou seja:
o jogo não é mágica — o que ensina é a **sequência** e o **retorno imediato**,
não o "ser jogo".

**As reclamações dos professores brasileiros na loja (1.517 pessoas marcaram a
primeira como útil) — e cada uma é um defeito que a nossa casa já pagou:**
1. *"o nível aumenta sem parar, sem oportunidade para praticar e consolidar"* →
   é a nossa regra da **repetição em BLOCO** (CONTRATO §6b): o som novo aparece
   em fases seguidas até firmar, e só depois vem outro.
2. *"as imagens de fundo atrapalham a visualização das letras (fundo do mar)"* →
   **letra nunca sobre cenário**: toda letra/sílaba-alvo da casa tem MESA própria
   opaca (`.siletra` com faixa escura, `.csb` creme, `.sic` creme). O
   `_qa/contraste.js` mede o PIXEL real do fundo por isso.
3. *"a pronúncia de algumas letras é ruim; não distingo o N do L"* e *"onde era
   para sair o som do G, saiu F — a criança é obrigada a marcar errado"* → é
   EXATAMENTE a família do "ilefante" e da voz trocada. A resposta da casa é o
   **testador humano** (`testador-humano.yml`, set/2026): o OUVIDO escuta cada
   mp3 e compara com o `falas.json`; o OLHO olha cada figura e diz se é o que o
   nome promete. Os dois erros mais votados do maior app de alfabetização do
   país são erros de **voz e figura**, não de mecânica — a banca de código
   nunca os pegaria.
4. *"queria exportar relatório de acertos por letra"* → já temos: o relatório do
   professor (segurar a medalha 2 s) com parecer por objetivo.

### Teach Your Monster to Read (Usborne Foundation, Reino Unido; 50 M de crianças)
Minijogos **testados com criança** ("play testing by our favourite users") e com
duas especialistas de leitura. O que dá para copiar do desenho deles:
- **Ouvir ANTES de escolher, sem custo**: *"fly the ship over the building
  blocks to listen to the letter-sounds"* — passar sobre o bloco toca o som; só
  o clique responde. É o nosso alto-falante em toda resposta (`op_*`), e é a
  razão de ele existir.
- **Segmentar E juntar são jogos separados**: *"segment CVC words into their
  constituent sounds"* (subir o prédio) e *"listen to the word and select the
  correct graphemes to build it"* (asteroides). Análise e síntese, cada uma com
  o seu gesto — como o nosso par `bater-silabas` / `juntar-silabas`.
- **Palavras irregulares viram PERSONAGENS** ("tricky words", cada uma com o seu
  bichinho, colecionáveis). Em português a lista é pequena (é, com, que, muito),
  mas a ideia serve: o que não se decodifica se **apresenta**, não se cobra.
- **Ler para FAZER** ("*Tap the crayon*" → instruções cada vez mais longas): a
  leitura com propósito, sem quiz. **Não temos** esta mecânica (ver §6).
- **Grafemas alternativos do mesmo som** (ou/ow) só no 3º estágio — em português
  é o **S/SS/Ç/C de /s/** e o **X/CH de /ʃ/**: conteúdo de 2º/3º ano, não de 1º.

### NCIL — *How to Use Systematic Phonics Instruction* (o manual operacional)
As instruções, uma a uma, e o que cada uma vira aqui:
- **Poucos sons por vez; nomear a letra E dizer o som.** → uma casa nova por
  bloco de fases; a casa fala "o som M" e a criança ouve o nome da letra no
  `tracar-letra`.
- **Figura-âncora para cada letra-som** (*"an image of a pig, the printed letter
  p, and the teacher orally stating /p/"*) e uma **historinha aliterada**
  ("Polly Pig likes pizza"). → **aplicado**: a casa do `som-inicial` aceita
  `img` (a MÃO em cima do M). A historinha aliterada é fala do mascote na
  abertura do bloco (conteúdo, §6).
- **Começar pelas relações de maior rendimento** (m, a, s) **e separar as que se
  confundem** no ouvido (b/v) ou no olho (b/d). → **aplicado**: o
  `_qa/dinamicas.py` avisa quando duas casas confundíveis caem na mesma rodada.
  Isto pega, por exemplo, a fase 6 da Padaria (B/D/P/M numa tela só, na primeira
  vez que nomeia letras).
- **Fonação conectada** (*"keep their motor running"*): juntar sem parar entre os
  sons, e depois ler "do jeito rápido". → já era regra do `juntar-silabas`; agora
  **também da `caixas-de-som`** (§4.1).
- **Ordem de dificuldade para juntar:** CVC só com sons contínuos → parada no
  fim (SAL… não: **MAT**) → parada no começo (**PÃO**, **TATU**) → encontro
  consonantal (**TREM**, **PRATO**). → confirma a nossa "regra de ouro" (som
  contínuo antes de parada) e a estende: **a palavra da 1ª rodada não tem
  encontro consonantal**.
- **Caixas de som com a SETA embaixo**: *"have students slide their finger across
  the arrow under the set of boxes to read the word"*. → **aplicado** (§4.1).
- **Escada de palavras** (*word ladder*: MALA → MOLA → BOLA, uma letra por vez).
  → é a `letras-escondidas` em série, ou uma peça nova pequena (§6).
- **Maiúscula E minúscula.** → o Trem e a Padaria são em caixa alta; a minúscula
  é conteúdo de 2º ano (Blumenau: "convenção da escrita, maiúsculas e minúsculas").

### Consciência fonológica — a prática brasileira (blogs de professor, MEC)
O repertório coincide com o nosso leque: **rima** (roda de rimas, histórias que
rimam), **aliteração** (caça ao som inicial, "quem fala palavras com /m/?"),
**segmentação** (palmas por sílaba, "corrida das sílabas" no chão), **síntese**
(juntar os pedaços), **bingo dos sons**, **intruso pelo som inicial** (*"o aluno
fala os nomes das figuras fazendo a diferença entre os sons"*), **letras móveis**
e **a mesma sílaba em posições diferentes tem o mesmo som** (BOla, saBOr). Duas
coisas que a prática brasileira faz e que valem regra:
- **o "intruso" fonológico fala o porquê pelo SOM** ("PATO, GATO, RATO… e o
  intruso é MESA, porque não termina em ATO") — a nossa peça `intruso` já exige
  o "por quê" tocado; em fase fonológica o porquê é um SOM, e a opção certa tem
  que ser o som, não uma frase.
- **a sílaba viaja**: a `juntar-silabas` pode pedir a MESMA sílaba em posição
  diferente nas rodadas seguidas (BO-LA, sa-BO-r) — a criança percebe que o
  pedaço é o mesmo. É conteúdo, não código (§6).

### EdiLIM — o manual, relido página a página
O que a releitura acrescentou ao `EDILIM-DINAMICAS.md` (ago/2026):
- **Dictado** tem duas opções que são ANDAIME: *"ver texto"* (a frase aparece
  para a criança copiar) e *"ver correcciones"* (mostra as palavras erradas E a
  escrita certa, só quando o ditado termina). → **aplicado** o "ver texto" como 2º
  degrau do nosso `ditado` (§4.2); o "ver correções" já é o nosso relatório.
- **Ortografía / Letras**: a letra escondida vem **com som** e o autor pode pôr
  **letras a mais** — a `letras-escondidas` já faz os dois (`distrator`).
- **Sopa de letras com IMAGENS** em vez de lista de palavras (*"Mostrar imágenes:
  la vista cambia para arrastrar"*) → o caça-palavras para quem não lê: a pista
  é a figura. **Não temos** (§6).
- **Parejas 2 com SONS** (2, 3 ou 6 pares) → memória de sons, já listada.
- **Identificar sonidos**: arrastar sons para duas colunas → é o nosso
  `som-inicial` com o som como carta (variante, §6).
- **Puzzle com fundo em opacidade** e **"ver destino"** em arrastar/classificar →
  andaime de graça, já anotado como regra para toda peça de arrastar.
- **Frases**: ordenar palavras na horizontal OU vertical → o `montar-frase` só
  faz horizontal; vertical serve para lista/poema (menor).

---

## 3. As regras que ficam (para as 14 peças de alfabetização)

Cada uma com o lastro e com onde se mede. As marcadas ✅ já estavam na casa;
as ⭐ nasceram desta pesquisa.

1. ✅ **Sistemático, não sorteado.** A ordem das letras/sons de uma atividade é
   decisão pedagógica (NCIL; RECEITA §alfabetização 1). Mede: `_qa/pedagogo.py`
   (escada) — e o pedagogo humano.
2. ✅ **Som contínuo antes de parada** (M, S, F, V, N, L, R, Z antes de B, P, T,
   D, K, G). ⭐ **E sem encontro consonantal na 1ª rodada** (NCIL, sequência de
   blending a→d). Mede: conteúdo; o `_qa/curriculo.py` pode avisar.
3. ⭐ **Confundíveis nunca juntos na estreia** (b/d, p/q no olho; b/v, f/v, t/d,
   m/n, p/b no ouvido) — cada um sozinho primeiro. Mede: `_qa/dinamicas.py`
   ("som inicial", aviso).
4. ✅ **Primeiro o som, depois a letra** — em `caixas-de-som` a letra só aparece
   no fim. Mede: `_qa/dinamicas.py` ("caixas de som", reprova letra na criação
   da caixa — regra escrita hoje; a linha do DINAMICAS existia, o portão não).
5. ⭐ **Separou → JUNTA.** Toda análise (bater, caixas) termina com a palavra
   dita **inteira, de uma vez** (fonação conectada; NCIL "seta embaixo das
   caixas"). Mede: `_qa/dinamicas.py` (aviso se falta `.csLer`).
6. ✅ **Ouvir antes de escolher, sem custo** — alto-falante em toda resposta,
   repetir é direito (TYMTR "fly over the blocks"; GraphoGame). Mede:
   `_qa/vozresposta.js`, `_qa/padrao.py` (fase muda).
7. ⭐ **Letra nunca sobre cenário** — mesa própria opaca atrás de toda
   letra/sílaba-alvo (reclamação nº 2 do GraphoGame). Mede: `_qa/contraste.js`
   (pixel real).
8. ✅ **A casa fala o SOM, o traço fala o NOME** — "o som M" no `som-inicial`;
   "ême" só ao traçar. Mede: `_qa/dinamicas.py` (aviso "o som").
9. ⭐ **Figura-âncora por letra-som** (o porco do /p/) — casa do `som-inicial`
   com `img`; o mascote abre o bloco com a frase aliterada. Mede: `_qa/imagens.js`
   (a figura carrega) + testador OLHO (a figura é o que o nome diz).
10. ⭐ **Andaime do ditado em três degraus de verdade**: ouvir de novo → **ver a
    palavra 2,5 s** (some) + letra pisca → revela. Mede: `_qa/dinamicas.py`
    ("ditado", `mostraPalavra`).
11. ✅ **Consolidar antes de subir** (reclamação nº 1 do GraphoGame) — o som novo
    em fases SEGUIDAS até firmar. Mede: `montar.py` (bloco), CONTRATO §6b.
12. ⭐ **Voz e figura conferidas por um testador que ESCUTA e VÊ** (reclamações
    nº 3 e o erro G→F). Mede: `testador-humano.yml` (ouvido faster-whisper ×
    `falas.json`; olho Gemini × nome da figura). Roda por pedido em
    `_status/TESTAR.json`; veredito em `_status/testador-*.md`.
13. ✅ **Nunca prova, nunca "errou"** — o erro responde com o que olhar (Hattie);
    GraphoGame: *"positive feedback to sustain engagement"*.
14. ✅ **Sessão curta, retomável** — 15 min 3×/semana (GraphoGame) ⇔ o nosso
    "continuar de onde parou" por 55 min.

---

## 4. O que foi lapidado HOJE (código na fonte, medido)

### 4.1 `caixas-de-som` — LER A PALAVRA (regra 5)
Depois que a última ficha entra e as letras aparecem, nasce a **seta de ler**
(`.csLer`, barra que corre da esquerda para a direita, transição de largura —
sem `@keyframes`, para o integrador nunca perder) e a voz diz a **palavra
inteira** (`palavraFalada`), e só depois o "Isso! PÃO tem 3 sons" (`falaEmSeguida`).
Antes a peça segmentava e parava: meio caminho.

### 4.2 `ditado` — VER A PALAVRA (regra 10)
O 2º degrau do andaime ganhou o "ver texto" do EdiLIM: `mostraPalavra(2500)` —
a caixa da voz mostra a palavra escrita (fundo claro, letra escura, espaçada) por
2,5 s e volta a esconder; a letra da vez pisca junto. Guardado por geração e por
tela (relógio de rodada velha não mexe na nova). O 1º degrau (ditar de novo) e o
3º (revelar) ficaram como eram.

### 4.3 `som-inicial` — FIGURA-ÂNCORA + guarda de confundíveis (regras 3 e 9)
A gaveta `CASAS` aceita `img` (arte do banco pelo `imgEl` do motor; na bancada não
há figura e a casa fica como era). E o `_qa/dinamicas.py` ganhou a armadilha 4:
duas casas confundíveis na mesma rodada → aviso com o par.

### 4.4b Segunda rodada (2026-09-06, tarde — "pode fazer tudo")
Passei as 11 peças restantes pelas 14 regras com um levantamento medido (voz,
alto-falante, andaime, teclado, "errou"). O que estava fora e foi consertado na
fonte:
- **`rima`** — a peça **não falava nada** (0 chamadas de voz): tocar a carta agora
  **diz a palavra** (regra 6, ouvir antes de escolher); o alto-falante do motor
  (`.ptxt`) continua como segundo gesto. Portão: aviso em `dinamicas.py`.
- **`montar-frase`** — idem, 0 chamadas de voz: quando a frase fecha, ela é **lida
  inteira** (campo `f` da rodada; o `montar.py` grava a frase). Regra 5
  (separou → junta). Portão novo "montar-frase" em `dinamicas.py`.
- **`bater-silabas`** — a figura da palavra (150 px) não respondia ao toque
  (regra 13 da pesquisa das casas): tocar a figura diz a palavra inteira.
- Conferido e **já certo**: `bater-silabas` diz a palavra inteira no fim (regra 5);
  `juntar-silabas`, `letras-escondidas`, `completar`, `forca`, `ouvir-achar`,
  `tracar-letra` têm alto-falante/`data-voz` e andaime; nenhuma mostra "errou" à
  criança (todas as ocorrências são comentário ou nome de função).
- **Decisão registrada (regra 8):** nas peças de ESCREVER (`letras-escondidas`,
  `completar`, `forca`) a voz diz o **nome** da letra ("ême") ao tocar a tecla —
  é o gesto de soletrar, e o nome é o certo ali. O **som** fica com `som-inicial`
  e `caixas-de-som`. Não é defeito; é a divisão da regra 8.
- `caca-palavras` e `cruzadinha` entraram pela pesquisa das casas (figura ao achar,
  pista falada, palavra inteira ao fechar) — ver `JOGOS-EDUCACIONAIS-REFERENCIAS §3`.

### 4.4 Portões novos/estendidos (`_qa/dinamicas.py`)
- **"caixas de som"** — regra nova (não existia): letra nascendo com a caixa
  reprova; sem `revela` avisa; sem `.csLer` avisa.
- **"ditado"** — regra nova: sem `onkeydown` reprova (duas portas); sem
  `mostraPalavra` avisa; frase com acento/cedilha reprova.
- **"som inicial"** — armadilha 4 (confundíveis).

**Medição:** `python3 _qa/dinamicas.py` código 0 nas três peças; integrador
regenerou `pecas.js`/`pecas.css` (88 peças, 292 animações preservadas); bancada
`_qa/peca.sh` PRONTA nas três (e nas 7 peças retocadas depois: bater-sílabas,
ligar-pontos, ouvir-achar, intruso, traçar-letra, pintar-desenho). A **Padaria**
foi remontada com as caixas de som que leem a palavra, MEL·SAL·OVO·PÃO e
MALA·MASSA·BOLO·PATO·LEITE·QUEIJO (40 min medidos), publicada em
2026-09-06 12:19Z (sha conferido no ar) e **a banca inteira APROVOU (código 0)**
— depois de o próprio processo pagar quatro lições, registradas no
`MEMORIA-DO-PROJETO.md` (frases de jogo colhidas, dicas da memória para todos os
pares, alto-falantes mudos por chave de texto, artigo cravado no intruso). O
testador humano (rodadas 3 e 4) não achou **nenhuma voz** dizendo outra coisa
no Trem nem na Padaria.

---

## 5. O que a pesquisa NÃO autoriza (para não errar por excesso)

- **Trocar mecânica por novidade.** O RCT que não deu efeito (GraphoGame Rime,
  Inglaterra) é o aviso: o que ensina é a sequência explícita com retorno
  imediato, não o "ser jogo". Mecânica nova entra quando o gesto dela É o
  conteúdo (RECEITA).
- **Alfabeto pendurado na tela.** Decoração subtrai (parecer
  `ALFABETO-APOIO-VISUAL.md`); a letra entra como FERRAMENTA da fase, nunca como
  gabarito visível.
- **Sinais de contexto para adivinhar a palavra** (*3-cueing*): a criança lê a
  palavra pelos sons, não pela figura ao lado. A figura confirma o SENTIDO,
  não substitui a decodificação — por isso na `caixas-de-som` a palavra está
  escrita e a figura é apoio, e no `ditado` a figura não aparece.
- **Cobrar antes de ensinar** (palavras "decodáveis"): em `ditado`, `digitar`,
  `letras-escondidas` só entram letras/sílabas já vistas na própria atividade.
  Regra de conteúdo, medida pelo pedagogo (`_qa/pedagogo.py`, escada).

---

## 6. Para o Marcos decidir (peça nova ou conteúdo)

| # | proposta | de onde vem | custo |
|---|---|---|---|
| 1 | **`ler-e-fazer`** — a instrução vem ESCRITA (sem voz automática: ler é o conteúdo) e a criança executa na cena ("toque no pão"; depois duas ações em ordem). Voz só como 2º degrau do andaime | TYMTR "read and do" | ✅ **feita 2026-09-06** (`_padrao/pecas/ler-e-fazer.html`, portão em `dinamicas.py`, linha no DINAMICAS) |
| 2 | **caça-palavras com pistas em FIGURA** (`PALFIG` + `MODO="figuras"`) | EdiLIM "sopa de letras: mostrar imágenes" | ✅ **feito 2026-09-06** na `caca-palavras` (e a figura aparece ao achar, no modo lista) |
| 3 | **escada de palavras** (MALA → MOLA → BOLA, uma letra por degrau) | NCIL word ladder | ✅ **feita 2026-09-06** (`_padrao/pecas/escada-de-palavras.html`: dois toques por degrau, duas portas, voz na troca) |
| 4 | **memória de SONS** e **`marcar-varias`** | EdiLIM (já em `EDILIM-DINAMICAS.md`) | ✅ **feitas 2026-09-06**: `memoria` ganhou a carta-som (`som:true` no par) e nasceu `_padrao/pecas/marcar-varias.html` |
| 5 | **frase aliterada do mascote** ao abrir cada bloco de letra ("a Miga mordeu a maçã…") | NCIL "Polly Pig" | ✅ **feito na Padaria 2026-09-06** (9 letras traçadas abrem com a frase: "Pipoca, pão e pudim: tudo com P!") |
| 6 | **a sílaba viaja** (BO-LA → sa-BO-r em rodadas seguidas do `juntar-silabas`) | prática brasileira | conteúdo |
| 7 | **Padaria fase 6** (B/D/P/M na primeira nomeação de letras) — escalonar: B e M primeiro, D e P depois | NCIL confundíveis; o portão agora avisa | ✅ **feito 2026-09-06**: B, M e P nomeadas sozinhas entre letras que não se confundem; o par p/b só na 4ª rodada |
| 8 | **gravar a leitura da criança** (Elefante Letrado grava e avalia o áudio do aluno) | Elefante Letrado | microfone + reconhecimento no navegador: futuro; anotar, não fazer |

---

## 7. O que não consegui apurar (com todas as letras)

- **Textos primários do GraphoGame** (graphogame.com: 403/202) e o **RCT da EEF**
  (educationendowmentfoundation.org.uk: 403). O que li do RCT vem do resumo do
  Learning Cabinet — de 2ª mão.
- **Shute 2008** continua sem o texto (só resumo de 2ª mão).
- **Wordwall de consciência fonológica** (403) e três blogs brasileiros (SSL).
- **Não medi o efeito** das três lapidações com criança: medi que a peça faz o
  que a regra manda (bancada) — o efeito de aprendizagem é o portão do professor.
