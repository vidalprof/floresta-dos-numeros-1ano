# CATÁLOGO DE INTERATIVIDADES — pesquisa + curadoria (Navio Pirata e além)

> Documento de PESQUISA + CURADORIA. Não altera o motor nem nenhum outro arquivo.
> Objetivo: (A) inventariar o que a fábrica JÁ TEM (motor `eduverse` + catálogo do
> `MANUAL-MESTRE.md`), (B) estudar mecânicas novas cabíveis no nosso stack leve
> (Canvas/DOM, ES5, sem libs), (C) recomendar quais usar como FASES DE ALÍVIO no
> **Navio do Byte Pirata** (números até 30, 1º ano), cruzando com o
> `NAVIO-PIRATA-BLUEPRINT.md` já existente.

---

## (A) INVENTÁRIO — o que já existe

Há DUAS linhas de produto distintas neste projeto, e é importante não confundi-las:

1. **Motor `eduverse`** (`eduverse/motor/kit-floresta.py`) — um mundo-vivo em Canvas
   (o Byte anda livre, câmera segue, NPCs, clima, ciclo dia/noite) onde um "modo aula"
   data-driven (`MUNDO.aula.rounds[]`) roda **rodadas de coleta**. É o motor por trás de
   `floresta`, `pomar`, `cesta-do-tico`, `clareira` e do blueprint do `navio-pirata`.
2. **Linha "premium"** (`ATIVIDADE-PREMIUM.md` + `MANUAL-MESTRE.md` §12 "MECÂNICAS DE
   FASE") — o molde de atividade single-HTML clonada do "Circo do Teo" (mapa-aventura
   com paradas/telas DOM, XP, medalhas). É onde vive o catálogo rico de mini-jogos
   (memória, caça-palavras, forca, etc.), usado em outras atividades do Marcos
   (fora deste repositório `eduverse`).

**Essas duas linhas NÃO compartilham código.** Isso importa demais pra curadoria da
seção (C): qualquer mecânica do catálogo premium usada no Navio Pirata precisa ser
**construída dentro do motor Canvas/mundo-vivo** (ou como uma tela DOM sobreposta que
pausa o loop do mundo) — não é um "copiar e colar", mesmo já sendo um padrão validado
noutra linha.

### A.1 — IMPLEMENTADO no motor `eduverse` (código real, `kit-floresta.py`)

Só **4 mecânicas de rodada**, todas lidas de `MUNDO.aula.rounds[].tipo` e resolvidas
pelo mesmo motor de coleta (andar até o item, tocar, ver o resultado na cesta):

| Mecânica | O que é | Habilidade | Onde no código |
|---|---|---|---|
| **`contar`** | Toca cada item pendurado/caído até juntar `n`; fala 1 a 1 (`n0..n30`), cardinalidade ao fechar. | Contagem 1-a-1, correspondência termo-a-termo, cardinalidade (EF01MA01/02/04). | `kit-floresta.py` bloco `rTipo==="contar"`, `_geraItens`, `aulaInit/aulaUpdate` |
| **`ordenar`** | Itens numerados 1..n em POSIÇÕES embaralhadas; só aceita na sequência (fora de ordem = "treme", não penaliza). | Sequência numérica / ordem crescente (EF01MA01/05). | `rTipo==="ordenar"`, `_piscaProx`, `_erroOrdem` |
| **`trazer_exato`** | Há `n` itens, a cesta só quer `alvo` (ex.: 7 de 10); sobra vira "demais" sem punir. | Cardinalidade exata, mais/menos/igual, parar na quantidade pedida (EF01MA03). | `rTipo==="trazer_exato"`, `rNaCesta/rExtra` |
| **`agrupar`** | Junta de 10 em 10 em "sacolas" (`sacola10.png`); introduz a dezena (20, 30). | Agrupamento de base 10, valor posicional (EF01MA05). | `rTipo==="agrupar"`, `bundles/loose` |

Reforços que o motor já dá de graça a QUALQUER rodada (não são "mecânicas" à parte,
mas valem registrar porque a curadoria em (C) depende deles): apoio ao erro sem
punição, narração encadeada por fala (nunca timer fixo), NPCs vivos com `falas[]`
variadas, clima/ciclo dia-noite, câmera seguindo o Byte, D-pad + teclado.

**⚠️ GAP CONFIRMADO NO CÓDIGO — falta o "apoio ao erro por CONTAGEM ACESA" (recurso
premium obrigatório, `MANUAL-MESTRE.md` §6/§7):** conferi linha a linha o tratamento
de erro do motor da aula (`_erroOrdem` na linha ~755 e o feedback do `trazer_exato`
na linha ~751) e hoje ele só dá **dica gentil falada** ("Qual vem primeiro? Procura o
X!", `somErroGentil()`) — **não existe, em NENHUMA das 4 mecânicas (nem em `contar`,
a mais óbvia candidata), o padrão obrigatório de "acender cada objeto UM POR UM EM
SINCRONIA COM A FALA"** (mascote diz "Não foi dessa vez! Vamos contar juntos, bem
devagar." → cada item acende via `filter:drop-shadow` — NUNCA `transform:scale` —
exatamente quando a voz diz aquele número, encadeado pelo callback do `falar`, nunca
por `setTimeout` de ritmo fixo). Isso é tratado no manual como requisito **não
opcional** de toda fase de contar quantidade. **Este é um débito do motor `eduverse`
inteiro** (afeta toda atividade construída sobre `kit-floresta.py`, não só o Navio
Pirata) e precisa entrar como item de construção — ver marcação em cada mecânica de
contagem na curadoria (C) abaixo.

A camada de **jornada** (`eduverse/JORNADA-PLANO.md`) planeja um FSM de "beats"
(`tarefa | interacao | dormir | andar`) que orquestraria pausas narrativas (entrar na
cabana, dormir/amanhecer) ao redor dessas 4 mecânicas — mas é **só plano**: "a
construção começa DEPOIS que o polimento do motor... terminar" (citação do próprio
documento). Nenhuma linha de `jornadaUpdate`/interpretador de beats existe ainda em
`kit-floresta.py`. Ou seja: **hoje não há nenhum mecanismo pronto para intercalar uma
tela diferente (mini-jogo) no meio do mundo-vivo** — isso teria que ser construído,
mesmo que de forma mínima e isolada só para o Navio Pirata (ver seção C).

O `NAVIO-PIRATA-BLUEPRINT.md` (já escrito) confirma isso: o v1 "reaproveita 100% do
motor e da geometria do pomar, sem mudar o motor", usando só `contar/ordenar/
trazer_exato/agrupar` nas 7 paradas. Nenhuma fase de alívio está no blueprint hoje.

### A.2 — DOCUMENTADO/CONCEITO (catálogo premium, `MANUAL-MESTRE.md` §12) — não está no motor `eduverse`

Estas mecânicas **existem de verdade** (são receitas com "lições pagas" reais, ou
seja, já foram construídas e depuradas em outras atividades do Marcos — a prova é o
nível de detalhe das lições), mas como **código de atividades single-HTML da linha
premium**, não como parte do motor Canvas do `eduverse`. Para entrarem no Navio
Pirata precisam ser **portadas/reconstruídas** para o paradigma do mundo-vivo (ou
como overlay DOM que pausa o loop):

- **Conhecer os números** (grade que acende com áudio), **Completar a sequência**
  (arrastar o número que falta num slot `?`), **Número e quantidade** (contar
  bichinhos + tocar no numeral) — primos próximos do que `contar`/`ordenar` já fazem.
- **Cesta (adição/subtração concreta)**, **Adição em conta armada**, **Subtração**
  (riscado ou conta armada) — fora do escopo do 1º ano/Navio (adição formal é depois).
- **Memória** (parear cartas iguais, conceito↔representação).
- **Quebra-cabeça de ordenação** (tocar do menor ao maior) — é OUTRA coisa que o
  "ordenar" do motor (lá é numeral 1..n; aqui pode ser por tamanho/atributo).
- **Caça-palavras** (grade 10×10) — não serve ao 1º ano não-leitor.
- **Frase em ordem / Monte a Frase** — idem, exige leitura.
- **Escolha múltipla com imagem**, **Classificar fichas** (arrastar/clicar).
- **Forca** — exige leitura/alfabeto; fora do 1º ano não-leitor.
- **Ligar os Pontos** (revela desenho tocando números em ordem 1→N) — MUITO citado
  pelo Marcos como candidato pro Navio; documentado com lições específicas (silhueta
  tem que bater com a imagem revelada; só toque, nunca hover; anti-toque-duplo).
- **Labirinto** (setas na tela + teclado, monstrinho, tesouro em posição variável).
- **Quebra-cabeça de grade** (fatiar foto 2×2/2×3, slots em grade real).
- **Caça aos 7 Erros / Achar o Diferente** (2 fotos comparadas, toque na diferença).
- **Tela de Pintar por toque** (balde de tinta / flood-fill) — hoje é a recompensa
  final do modelo premium (Pré), 100% código.
- **Sistema de arrastar GLOBAL+GHOST** (`instalarDragGlobal`) — é a INFRAESTRUTURA por
  trás de várias mecânicas acima (sombra, quebra-cabeça, classificar). Não existe
  equivalente no motor `eduverse` hoje (lá a interação é "andar até tocar", não
  "arrastar item pela tela").
- **Fase da Sombra** (arrastar bicho colorido até a silhueta preta igual, que revela
  o colorido ao acertar) — um dos exemplos citados pelo Marcos para o Navio.

**Resumo da distinção que importa para a curadoria:** todas as mecânicas de (A.2) são
"existe, mas não aqui" — precisam de trabalho de portagem para o motor Canvas do
Navio Pirata (mínimo: uma tela DOM/canvas separada que pausa `frame()`/`aulaUpdate`,
roda o mini-jogo, e devolve controle ao mundo). Nenhuma é "gratuita".

---

## (B) MECÂNICAS NOVAS ESTUDADAS

Pesquisei práticas consagradas de jogos educativos pra educação infantil/1º ano
(busca web: mecânicas de correspondência/classificação/sequenciamento na pedagogia
infantil, e apps de traçado com o dedo para pré-escrita/numeracia) e cruzei com o que
CABE no nosso stack (Canvas 2D ou DOM, ES5 puro, sem libs, toque+mouse, PC antigo).
A pesquisa confirma que classificar/parear/sequenciar são pré-requisitos de
matemática ANTES do número abstrato (Playgroup WA; SimplyFun), que memória de
trabalho e atenção sustentada no pré-escolar predizem desempenho posterior em
matemática (revisão em PMC/MoveEarly), e que aprendizagem baseada em jogo tem efeito
positivo em desenvolvimento cognitivo na infância (Frontiers, meta-análise 2024) —
o que sustenta pedagogicamente investir em variedade de mecânica, não só em
"contar mais uma vez". Fontes ao fim da seção.

Abaixo, 10 famílias REALMENTE novas (não duplicam nada de A.1/A.2). Não incluí de
novo "spot-the-difference" (= Caça aos 7 Erros, já em A.2) nem "labirinto de dedo"
(= Labirinto, já em A.2) — esses dois já existem como receita; ver A.2.

### 1. Traçar o Caminho (trace contínuo com o dedo)
- **Mecânica:** arrastar o dedo/mouse seguindo uma trilha pontilhada contínua (não
  pontos numerados discretos como o "Ligar os Pontos" — aqui é o gesto CONTÍNUO que
  importa), com um "corredor" de tolerância; sair muito da linha não quebra o jogo,
  só não pontua aquele trecho.
- **Habilidade:** controle motor fino / pré-escrita (o mesmo gesto usado pra formar
  o traço do algarismo), noção de trajeto/direção espacial.
- **Por que serve a quem não lê:** zero texto — é gesto puro, com reforço sonoro
  contínuo (um "zzzip" que acompanha o dedo) e visual (a trilha brilha atrás do
  dedo).
- **Como fica leve:** Canvas 2D; a trilha é uma polilinha (mesmo formato de dados que
  `mundo.path` já usa no motor!); a cada frame mede a distância do ponteiro ao
  segmento mais próximo (perpendicular a um segmento de reta — geometria simples,
  sem lib); progresso = % da polilinha "pintada". Reaproveita a MESMA representação
  de path do motor — só muda a interação (arrastar sobre ela em vez de andar).
- **Como tematizar (pirata):** o dedo da criança é o "traçado do mapa do tesouro" —
  vai do navio até o X; ou, mais alinhado à numeracia, TRAÇAR o contorno do algarismo
  (1 a 30) desenhado grosso na tela, como se "cavasse a areia" até formar o número.

### 2. Sequência / Padrão (o que vem depois)
- **Mecânica:** fileira de ícones num padrão (AB-AB-AB, ou crescente por quantidade:
  1 moeda, 2 moedas, 3 moedas, `?`); a criança toca/arrasta o próximo elemento certo
  pro slot `?`. Diferente do "ordenar" do motor (que é sequência NUMÉRICA 1..n fixa)
  — aqui o padrão pode ser de COR/FORMA/REPETIÇÃO, treinando reconhecimento de
  padrão, não só contagem.
  - Pesquisa confirma "pattern completion" como base pré-algébrica no pré-escolar,
    normalmente antes mesmo de aritmética formal.
- **Habilidade:** reconhecimento de padrão, raciocínio lógico, precursor de álgebra.
- **Por que serve a quem não lê:** só ícones + cor; enunciado é 1 frase falada
  ("O que vem agora?"), sem leitura de resposta.
- **Como fica leve:** DOM simples — fileira de `<img>`/divs com um slot `?`
  destacado; banco de opções embaixo (arrastar OU tocar); validação por comparação de
  valor (nunca por índice, seguindo a regra de embaralhar do manual).
- **Como tematizar:** bandeiras de sinalização içadas no mastro (padrão de cores);
  pegadas de caveira-osso-caveira-osso na areia da ilha; moedas empilhadas em
  sequência crescente (1,2,3...) — bom gancho pro tema "contar até 30".

### 3. Balança (comparar peso / mais-menos-igual visual)
- **Mecânica:** uma gangorra/balança de dois pratos; a criança coloca (ou já vem
  posta) quantidades diferentes de itens nos dois lados; a balança PENDE
  visivelmente pro lado mais pesado (ou fica reta se igual); pergunta "qual tem
  mais?"/"tem a mesma quantidade?".
- **Habilidade:** comparação, conservação de quantidade, vocabulário
  mais/menos/igual — falta HOJE no motor (que só tem `trazer_exato`, que é
  "quantidade exata", não "comparar dois grupos").
- **Por que serve a quem não lê:** o resultado é 100% visual (o prato desce), sem
  precisar ler "maior"/"menor".
- **Como fica leve:** Canvas 2D; desenhar uma balança simples (triângulo+trave+2
  cordas+2 pratos) e girar a trave por CSS/canvas `rotate` proporcional à diferença
  de quantidade (ângulo pequeno, sem exagero); os itens ficam empilhados nos pratos
  (reaproveita sprites de contagem já existentes).
- **Como tematizar:** balança de mercador de baú pirata pesando moedas de ouro vs.
  pedras/conchas; "qual baú é mais pesado, o com 5 moedas ou o com 8?".

### 4. Encaixar Formas (shape sorter)
- **Mecânica:** peças com formas geométricas (círculo, quadrado, triângulo, estrela)
  são arrastadas até o "furo"/silhueta da MESMA forma num baú/caixa; encaixe errado
  não entra (a peça "ricocheteia" de volta).
- **Habilidade:** reconhecimento de forma geométrica, correspondência forma-espaço,
  coordenação olho-mão.
- **Por que serve a quem não lê:** correspondência puramente visual de silhueta.
- **Como fica leve:** é literalmente a MESMA infraestrutura da "Fase da Sombra" já
  documentada em A.2 (arrastar item até a área com `data-drop` da mesma forma,
  motor drag global+ghost) — só troca "silhueta de bicho" por "silhueta de forma
  geométrica". Menor esforço de arte (formas geométricas são fáceis de gerar/
  recortar, sem risco de franja em bordas retas).
- **Como tematizar:** tampa do baú do tesouro com furos de moeda-redonda,
  joia-triangular, medalhão-quadrado, estrela-do-mar — a criança encaixa cada peça
  no furo certo antes do baú "trancar" satisfeito.

### 5. Ordenar por Tamanho (seriação)
- **Mecânica:** 4-5 itens do MESMO tipo em tamanhos visivelmente diferentes (do
  menorzinho ao gigante); a criança arrasta/toca em ordem do menor pro maior (ou
  vice-versa). Diferente do "ordenar" do motor (que ordena NUMERAIS 1..n) — aqui não
  há número nenhum na tela, só comparação de tamanho.
- **Habilidade:** seriação (clássico de Piaget — organizar por um atributo contínuo),
  vocabulário "pequeno/médio/grande/maior/menor".
- **Por que serve a quem não lê:** puramente visual, sem numeral.
- **Como fica leve:** mesma UI de slots em fila (`?` vira posição na fila) usada em
  "Completar a sequência"/"ordenar"; a "regra vira barreira" da fila horizontal
  (largura fixa vira grade sem querer) já está documentada e se aplica aqui também.
- **Como tematizar:** barris/baús de tamanhos crescentes empilhados no porão; peixes
  fisgados pela vara do Byte, alinhados do menor ao maior no convés.

### 6. Parear com Linha (matching numeral↔quantidade, sem virar carta)
- **Mecânica:** duas colunas fixas na tela (numerais à esquerda, grupos de objetos à
  direita, ambos embaralhados); a criança toca num numeral e depois no grupo
  correspondente (ou arrasta uma linha entre os dois) — SEM o componente de "virar
  carta e memorizar posição" da Memória (que exige memória de curto prazo; aqui é
  só correspondência visual direta, mais fácil pro 1º ano iniciante).
- **Habilidade:** correspondência numeral-quantidade (o mesmo conceito da
  cardinalidade, mas em formato de escolha em vez de contagem ativa).
- **Por que serve a quem não lê:** numeral é símbolo, não texto; grupo é imagem.
- **Como fica leve:** DOM + SVG `<line>` (mesma técnica já usada em "Ligar os
  Pontos" pra desenhar linhas por %) ligando os dois toques; ou, mais simples ainda,
  toque-toque sem desenhar linha (só destaca os dois e funde numa animação se
  acertou).
- **Como tematizar:** numeral em pergaminho ↔ montinho de moedas de ouro da mesma
  quantidade; ou bandeira com número ↔ grupo de canhões.

### 7. Estourar/Tocar Alvos (pop the targets, com atenção seletiva)
- **Mecânica:** vários alvos aparecem (bolhas, ondas, luzes) e a criança deve tocar
  SÓ os que atendem a um critério (ex.: só os com "3 bolinhas", ou só os numerais
  pares) antes que desapareçam sozinhos; ritmo calmo (sem pressão de tempo curta —
  adaptado pra 1º ano, nunca "quanto mais rápido melhor").
- **Habilidade:** atenção seletiva/sustentada e reconhecimento rápido de quantidade —
  a pesquisa (working memory/attention control no pré-K) liga isso a ganho posterior
  em matemática, então a fase treina algo além da contagem em si.
- **Por que serve a quem não lê:** critério visual (quantidade de bolinhas/cor), sem
  texto.
- **Como fica leve:** Canvas; pool fixo de "bolhas" reciclado (nunca aloca por
  frame, mesmo padrão de `gotas`/`ventos` já usado no motor pra chuva/vento);
  toque = hit-test por distância ao centro da bolha.
- **Como tematizar:** bolhas de espuma do mar sobem com números/quantidades dentro;
  a criança estoura só as que têm exatamente N mariscos, ao ritmo das ondas.

### 8. Deslizar pra Categoria (drag-to-bin / classificar em 2 grupos)
- **Mecânica:** um item aparece por vez; a criança arrasta (ou desliza com toque)
  pra ESQUERDA ou DIREITA, cada lado sendo uma categoria (ex.: "menos que 10" /
  "mais que 10"; ou "par"/"ímpar" pra séries seguintes). Mais simples que
  "Classificar fichas" (A.2, que é grade de vários itens simultâneos) — aqui é
  1 item de cada vez, decisão binária, ritmo mais tranquilo pro 1º ano.
- **Habilidade:** classificação/categorização (pré-requisito de matemática segundo a
  pesquisa de sorting em educação infantil), decisão binária rápida.
- **Por que serve a quem não lê:** os dois "baldes"/lados são ILUSTRADOS (não
  rotulados por texto) — ex. lado esquerdo = baú pequeno, lado direito = baú grande.
- **Como fica leve:** reaproveita o drag global+ghost (se optarmos por arrastar) OU,
  mais simples ainda, dois botões grandes nas laterais (toque, sem arrastar) —
  a opção mais leve de implementar de toda a lista.
- **Como tematizar:** "esse grupo de moedas cabe no bolso pequeno do Byte ou no
  baú grande?" — grupos de quantidade variável, a criança decide onde manda.

### 9. Montar/Construir (assemble partes distintas — não é fatiar foto)
- **Mecânica:** peças CONCEITUALMENTE diferentes (não pedaços de uma foto cortada,
  como o "Quebra-cabeça" de A.2) se juntam para formar um objeto completo — ex.:
  casco + mastro + vela + bandeira = o navio inteiro; cada peça entra num slot
  próprio, na ORDEM que faz sentido (casco primeiro, vela por último) ou livre.
- **Habilidade:** noção de parte-todo, sequência de montagem, vocabulário das
  partes do próprio tema (reforça literalmente "cada parada é uma parte do navio",
  pedido original do Marcos pro Navio Pirata).
- **Por que serve a quem não lê:** silhuetas-guia mostram onde cada peça entra
  (mesmo princípio do quebra-cabeça, mas com peças ÚNICAS e reconhecíveis, não
  fatias arbitrárias de foto — mais fácil pro 1º ano que um recorte 2×3 de céu
  liso).
- **Como fica leve:** drag global+ghost + slots com `data-drop` (infra já
  documentada); as "peças" são simplesmente os PNGs de peça de navio que o
  blueprint já lista como Leva 2 de arte (`mastro`, `canhao`, `leme`, `ancora`,
  `amurada`) — ou seja, reaproveita arte JÁ PLANEJADA no blueprint, não pede nada
  novo de imagem.
- **Como tematizar:** já é o tema — "monte o Navio do Byte Pirata peça a peça" seria
  literalmente o fecho visual da jornada (o navio vai ganhando partes conforme as
  paradas terminam, reaproveitando a ideia de "recompensa que cresce" que o manual
  já usa noutras atividades).

### 10. Girar/Alinhar (rotacionar até encaixar orientação)
- **Mecânica:** um objeto aparece girado/desalinhado; a criança toca numa seta de
  girar (ou arrasta em círculo) até ele ficar na orientação certa (encaixa com um
  "clique" quando alinhado, tolerância de alguns graus).
- **Habilidade:** rotação mental, orientação espacial — habilidade menos comum nos
  outros mini-jogos do catálogo (a maioria é toque/arraste linear, não rotação).
- **Por que serve a quem não lê:** feedback puramente visual+sonoro (o objeto
  "trava" com um som quando alinha).
- **Como fica leve:** Canvas; `ctx.rotate()` num ângulo controlado por variável de
  estado; toque num botão de seta soma/subtrai graus (reaproveita o padrão de botão
  D-pad+toque já usado no motor); ou arraste circular medindo o ângulo
  `atan2(dy,dx)` do ponteiro em torno do centro do objeto.
- **Como tematizar:** girar o LEME até apontar pro rumo certo (a bússola/estrela
  do norte); ou alinhar a luneta/mapa do tesouro na direção da Ilha.

**Fontes da pesquisa:**
- [Why sorting and matching is important for young children — Playgroup WA](https://www.playgroupwa.com.au/why-sorting-and-matching-is-important-for-young-children/)
- [Sequencing Activities for Kids to Build Logic — SimplyFun](https://simplyfun.com/blogs/simplyfun-blog/sequencing-activities-for-preschoolers)
- [Educational Game Tools in Early Childhood Mathematics Learning (ResearchGate)](https://researchgate.net/publication/348654265_Educational_Game_Tools_in_Early_Childhood_Mathematics_Learning)
- [MoveEarly study protocol — working memory/attention control and kindergarten math (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12888564/)
- [Game-based learning in early childhood education: systematic review and meta-analysis — Frontiers in Psychology 2024](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1307881/full)
- [Number Tracing Games for Toddlers and Preschoolers — Kokotree](https://kokotree.com/blog/games-activities/number-tracing-games-for-toddlers-and-preschoolers)
- [The Benefits of Tracing for Young Learners — GunjanApps](https://gunjanappstudios.com/blog/the-benefits-of-tracing-for-young-learners)

---

## (C) CURADORIA PARA O NAVIO DO BYTE PIRATA

Contexto do blueprint já escrito (`NAVIO-PIRATA-BLUEPRINT.md`): 7 paradas fixas, cada
uma reaproveitando 1:1 as 4 mecânicas do motor (`contar`/`ordenar`/`trazer_exato`/
`agrupar`), na ordem:

1. Convés — `contar n=3` · 2. Cesto da gávea — `contar n=5` · 3. Canhões — `ordenar
n=5` · 4. Velas/mastro — `contar n=10` (marco: 1ª dezena) · 5. Porão do tesouro —
`trazer_exato 7/10` · 6. Cozinha/despensa — `agrupar n=20` · 7. Leme/âncora (clímax) —
`agrupar n=30`.

**Aviso honesto antes da recomendação:** nenhuma fase de alívio existe hoje no motor
`eduverse` nem no blueprint do Navio. Inserir qualquer uma exige construir, no
mínimo, um mecanismo simples de "pausar o mundo, mostrar uma tela/overlay de
mini-jogo, retomar" — a camada de Jornada (`JORNADA-PLANO.md`) prevê algo parecido
(`tipo_beat:"interacao"`) mas **ainda não foi implementada** ("construção começa
DEPOIS do polimento do motor"). Recomendo NÃO esperar por ela: as 3 fases abaixo
podem ser feitas como overlays ad-hoc, isolados, só para o Navio Pirata (sem tocar em
`kit-floresta.py` além de um gancho mínimo de pausa/retomada), sem bloquear o zarpe
do v1 (que já passa nos 4 portões sem nenhuma delas).

### Recomendação: 3 fases de alívio + 1 recompensa final

**Princípio que rege toda a tabela abaixo (pedido explícito do Marcos): curadoria é
CURRÍCULO, a diversão é o VEÍCULO, não o destino.** Cada mecânica só entra na lista
se eu conseguir apontar (a) o objetivo de aprendizagem/código BNCC real que ela
treina e (b) por que aquele objetivo é adequado à FAIXA do 1º ano/não-leitor — nunca
"porque é divertida". Por isso descartei candidatas fortes (Balança, Encaixar
Formas, Sequência/Padrão — ver justificativa abaixo): são boas mecânicas, mas não
têm um objetivo curricular NOVO e prioritário pra ESTA atividade (números até 30),
o que quebraria o princípio.

| # | Mecânica | Objetivo curricular (BNCC) e por que serve à FAIXA (1º ano) | Já existe? | Esforço | Onde intercalar |
|---|---|---|---|---|---|
| 1 | **Fase da Sombra** (bicho/objeto colorido → silhueta preta que revela cor) | **Não é objetivo NUMÉRICO** — treina reconhecimento visual/vocabulário de objetos do tema (pré-requisito de atenção e discriminação visual que sustenta a matemática, mas não mapeia a um código EF01MA específico). Por isso é o alívio mais "puro": ao NÃO carregar conteúdo numérico, garante o respiro real de atenção que a faixa etária precisa entre duas tarefas de contagem (curva de atenção curta do 1º ano) sem arriscar confundir o objetivo pedagógico da aula (que é número). | Receita documentada em A.2 (linha premium); **não implementada no motor `eduverse`** | **BAIXO-MÉDIO** — infra de drag+ghost é nova pro motor Canvas (hoje só "andar até tocar"), mas a receita/lições já estão todas mapeadas; poucos assets (colorido+silhueta de 3-4 objetos piratas: chapéu, luneta, âncora pequena, papagaio) | **Após a Parada 3** (Canhões/`ordenar`), antes da Parada 4 (Velas, `contar n=10`) — bom respiro ANTES do marco emocional de contar até 10 pela 1ª vez. |
| 2 | **Parear com Linha** (numeral ↔ quantidade de moedas) — preferido a "Memória" completa | **EF01MA02/EF01MA04** — correspondência numeral↔quantidade e cardinalidade, o MESMO objetivo central das 7 paradas, mas em formato de RECONHECIMENTO (escolher o par certo) em vez de PRODUÇÃO ativa (contar em voz alta enquanto toca) — serve à faixa como CONSOLIDAÇÃO de baixa carga do que já foi ensinado, não introdução de conteúdo novo (por isso cabe bem como alívio, não como 8ª parada). | Memória clássica documentada em A.2; a variante SEM virar carta é da seção (B.6), ainda mais simples | **BAIXO** — sem infra de drag pesado (pode ser toque-toque), só precisa de numerais 1-10 como imagem (já é regra do manual "números como imagem do tema") + grupos de moedas (asset `moeda_ouro` já está na Leva 1 do blueprint). **Requer o apoio ao erro por contagem acesa (ver nota abaixo) — é mecânica de quantidade.** | **Após a Parada 5** (Porão do tesouro/`trazer_exato`) — a fase de MAIOR carga cognitiva da escada (parar exatamente em 7 exige inibir o impulso de continuar); consolida sem introduzir carga nova, antes de entrar na dezena. |
| 3 | **Ligar os Pontos** (1→30, revela um objeto do tema ao fim) | **EF01MA01** — series/contagem falada sólida de 1 a 30 (o objetivo de "fecho" que o blueprint já lista como habilidade-alvo global do Navio Pirata: "contar até 30 com confiança"). Adequado à faixa porque é a ÚNICA atividade da aula (parada ou alívio) que percorre a série NUMÉRICA INTEIRA de uma vez em ordem crescente — reforço direto do objetivo mestre da atividade, não um desvio dele. | Receita bem documentada em A.2, com lições específicas de silhueta/toque | **MÉDIO** — para v1, usar uma figura GEOMÉTRICA simples (ex.: âncora ou estrela-do-mar, calculável por trigonometria conforme a lição do manual — 10 pontos por elipse/pontas), o que evita o trabalho de extrair contorno de imagem complexa (Moore-neighbor tracing); o "navio inteiro" fica pra uma v2 (contorno mais complexo) | **Após a Parada 6** (Cozinha/despensa, `agrupar n=20`), antes do clímax da Parada 7 (`agrupar n=30`) — reforça "eu já sei contar até 30" logo antes do desafio final pedir isso em grupos de dez. |
| 4 (bônus, não é "alívio no meio") | **Colorir por número** (balde de tinta / flood-fill) como RECOMPENSA do Grande Final | **Nenhum objetivo curricular novo, DE PROPÓSITO** — é a recompensa livre pós-conclusão que o próprio `MANUAL-MESTRE.md` prescreve por faixa etária ("recompensa final troca por idade: Pré/1º ano = Tela de Pintar"); entra DEPOIS que todos os objetivos BNCC da aula já foram cumpridos (parada 7 concluída), então não compete com currículo — é o "veículo de diversão" na hora certa, o pós-jogo, não o meio da aprendizagem. | Receita documentada em A.2 ("Tela de Pintar"), já usada como recompensa-padrão do Pré noutra atividade | **MÉDIO** — reaproveita o código de flood-fill já provado; só precisa de 1 desenho-contorno novo (navio/ilha do tesouro) e paleta de cores | **Depois da Parada 7**, no Grande Final (troféu/âncora desce). |

**🔒 REQUISITO DE CONSTRUÇÃO OBRIGATÓRIO — apoio ao erro por CONTAGEM ACESA em TODA
mecânica de quantidade (padrão premium, não opcional, `MANUAL-MESTRE.md` §6/§7):**
como registrado no gap de (A.1), o motor `eduverse` hoje só tem dica gentil falada no
erro — falta em TUDO o padrão "mascote fala 'Não foi dessa vez! Vamos contar juntos,
bem devagar' → cada objeto acende UM A UM (`filter:drop-shadow`, nunca `scale`) EM
SINCRONIA com a voz dizendo o número, encadeado pelo callback do `falar` (nunca por
`setTimeout` de ritmo fixo)". Isso vale para:
- **As 7 paradas fixas** do blueprint (`contar` ×3, `ordenar` ×1 — este já usa uma
  variante própria de destaque piscante, `_piscaProx`, mas SEM o padrão de contagem
  acesa sincronizada por voz —, `trazer_exato` ×2, `agrupar` ×2): é um débito comum
  a QUALQUER mundo construído no motor `eduverse`, não exclusivo do Navio.
- **O alívio #2 (Parear numeral↔quantidade)** acima, por lidar diretamente com
  quantidade — se implementado sem esse apoio, fica ABAIXO do padrão premium que o
  resto da atividade deveria ter.
- **NÃO se aplica** ao alívio #1 (Sombra, que não é de quantidade) nem ao #4
  (Colorir, que é recompensa livre sem certo/errado).
Recomendo tratar essa construção como um item de esforço PRÓPRIO (estimativa:
MÉDIO — o encadeamento fala→luz já está especificado passo a passo no manual, é
"seguir a receita", mas toca em `_erroOrdem`/`_colhe`/`_geraItens` do motor
`kit-floresta.py`, então convém ser feito e testado uma vez só, de forma genérica
para as 4 mecânicas, ANTES ou JUNTO do Navio Pirata — não é algo pra reinventar por
atividade) e não como algo implícito em "está tudo pronto".

**Por que não as outras candidatas citadas no pedido** (justificativa rápida, pra não
parecer que foram esquecidas):
- **"Balança"/"Encaixar formas"/"Montar o navio"** (seção B) são ótimas mas cobrem
  habilidades que as 7 paradas fixas JÁ cobrem bem (comparar, forma, parte-todo não
  é o foco do 1º ano em números até 30) — ficam como candidatas fortes pra uma
  PRÓXIMA atividade (ex. uma de Geometria) em vez de disputar espaço aqui.
- **"Sequência/Padrão"** quase duplica o que `ordenar` (Parada 3) já treina — dá
  pouco ganho marginal pro esforço de construir uma mecânica nova.
- **Labirinto e Caça aos 7 Erros** (já existentes em A.2) foram considerados, mas o
  Marcos não os citou como exemplo e o esforço de construção (labirinto: grade+BFS
  de validação; erros: 2 imagens+diffs por código) é mais alto que as 3 escolhidas
  para o mesmo ganho pedagógico no tema números-até-30.

**Ordem final sugerida (8 paradas + 3 alívios + 1 recompensa final):**
Convés → Cesto da gávea → Canhões → **[Sombra]** → Velas/mastro → Porão do tesouro →
**[Parear numeral↔quantidade]** → Cozinha/despensa → **[Ligar os Pontos 1→30]** →
Leme/âncora (clímax) → Grande Final → **[Colorir por número]**.

**Antes de construir qualquer uma:** confirmar com o Marcos (regra "não inventar" do
`MANUAL-MESTRE.md`) — em especial se ele prefere adiar as fases de alívio pro v2 (o
v1 já "zarpa" sem elas, como o próprio blueprint decidiu) ou se quer priorizar 1 das
3 antes de gerar a arte da Leva 1/2.
