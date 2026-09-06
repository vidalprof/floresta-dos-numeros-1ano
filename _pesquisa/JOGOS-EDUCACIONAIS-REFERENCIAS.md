# 🎮📚 JOGOS EDUCACIONAIS INTERATIVOS DE REFERÊNCIA — o que aprendi e o que vira regra

> Pedido do Marcos (set/2026): *"pesquise e veja essas atividades rodando na
> internet… pode ser das internacionais também… aprenda tudo sobre esses jogos
> educacionais interativos"*. Este documento destila (1) as **casas** que fazem o
> nosso leque há décadas — vistas RODANDO num Chromium (`ver-rodando.yml`,
> `_pesquisa/rodando/`) e lidas (`pesquisar.yml`, `_pesquisa/web/casa-*.md`); (2) os
> **fundamentos** publicados que sustentam o que elas fazem
> (`_pesquisa/web/fundamento-*.md`); (3) o **mapa para as nossas 88 peças**: o
> que já fazemos, o que copiar, o que evitar. **Matéria-prima lida com juízo; só
> vira lei da casa o que entrar no `_padrao/DINAMICAS.md` e o Marcos aprovar.**
>
> Como ler: cada casa tem *o que é · o que faz bem · o que medi rodando · o que
> a gente leva*. As frases marcadas **⇒ REGRA** são as que proponho para a casa.

---

## 1. As casas (quem faz o nosso leque há anos)

### H5P (Noruega, aberto) — o "catálogo de tipos" que virou padrão do mundo
- **O que é:** biblioteca aberta de ~50 tipos de conteúdo interativo embutíveis em
  qualquer site (Moodle, WordPress). Tipos que espelham as nossas peças: *Drag and
  Drop, Drag the Words, Fill in the Blanks, Mark the Words, Memory Game, Find the
  Words (caça-palavras), Crossword, Image Sequencing, Sort the Paragraphs, Image
  Pairing, Image Hotspots, Find the Hotspot, Dictation, Single Choice Set,
  True/False, Timeline, Flashcards*.
- **O que faz bem:** cada tipo tem UM gesto claro e um "check/retry/show solution"
  padronizado; **feedback por faixa de acerto** configurável pelo autor; teclado
  e leitor de tela em todos os tipos (a11y é requisito de publicação do tipo).
- **O que medi rodando (lote 1):** `h5p.org/<tipo>` hoje redireciona para a home
  (17 fotos iguais — só o *Memory Game* da capa, 6 cartas "?", cronômetro e
  contador de viradas). Lição para o medidor: **ler as fotos antes de acreditar na
  tabela**. Lote 2/3 tentam os exemplos por busca.
- **O que a gente leva:** a **gramática do fechamento** (conferir → tentar de novo
  → mostrar solução) é exatamente o nosso andaime de 3 degraus (dica → apoio →
  revelar) — nomes diferentes, mesma ideia; e o **feedback por faixa** ("acertou
  tudo / quase / vamos rever") é o nosso parecer em palavras.
  **⇒ REGRA (já é):** toda peça fecha por `fimDaPeca`, tem 3 degraus e nunca a
  palavra "errou".

### PhET Interactive Simulations (Univ. do Colorado, EUA) — o "simulador que guia sem parecer guiar"
- **O que é:** simulações de ciências e matemática, HTML5, gratuitas, usadas do
  fundamental à universidade. Para os pequenos: *Make a Ten, Number Play, Number
  Compare, Balancing Act, Fraction Matcher, Area Model Multiplication*.
- **O que faz bem (pesquisa própria, "implicit scaffolding" — Podolefsky, Moore &
  Perkins 2014; Paul et al. 2012):** o mundo reage de verdade e imediatamente;
  **texto mínimo**; a criança aprende **explorando**, e a sim "guia sem parecer
  guiar" por **affordances e restrições do próprio desenho** (o que dá para pegar,
  até onde vai, o que muda quando você mexe) — não por instrução escrita. 4–6
  entrevistas *think-aloud* com alunos por sim antes de publicar. Representações
  múltiplas ligadas (o número, os blocos, a reta).
- **O que medi rodando:** é um **canvas só** (0 elementos de DOM tocáveis; 3 svg);
  som por **WebAudio** (11–39 fontes criadas ao carregar: cada gesto tem som);
  fonte mínima 10–16 px; abre numa tela de escolha (usar `?screens=1`).
- **O que a gente leva:** (1) **o gesto expõe o conceito** — a pergunta não tem
  resposta sem mexer no controle (a nossa "A ÁGUA SOBE" é exatamente isto; o
  `simulador` do motor precisa deixar de ser só água — hoje é o único tema); (2)
  **entrevistar a criança jogando antes de publicar** é o que o Marcos faz com a
  turma — a casa formalizou como portão final ("Aprovação do professor").
  **⇒ REGRA (nova):** peça de simulador/manipulável nasce com **texto mínimo** e
  restrições no desenho (só dá para fazer o que ensina), nunca com enunciado longo.

### The Math Learning Center — Apps (EUA) — manipulativos virtuais "abertos"
- **O que é:** *Number Pieces (base dez), Number Line, Math Clock, Fractions,
  Money Pieces, Pattern Shapes, Geoboard, Number Frames, Partial Product Finder*.
  Manipulativo puro: sem fase, sem acerto/erro, o professor propõe o problema
  (código de compartilhamento) e a criança mostra o raciocínio.
- **O que faz bem:** peças fiéis ao material concreto (juntar 10 unidades vira
  uma barra; quebrar a barra devolve 10); ferramentas de anotar/desenhar em cima;
  botões grandes (54–85 px) com `aria-label`; sem propaganda; sem login.
- **O que medi rodando (lotes 1–2):** canvas por peça (`canvas.draggable-canvas`),
  `mousedown`+`dblclick` no elemento e **pointer events no `document`**
  (pointerdown/move/up); `touch-action: auto` (eles resolvem por JS); **som zero**;
  **21–81 mutações de DOM no 1º segundo** após soltar (feedback visual denso);
  alvo mínimo 20–38 px (barras de 33 px).
- **O que a gente leva:** a **fidelidade ao material** (a nossa `base-dez` e
  `divisao-dourado` seguem isto — a troca "10 viram 1" é o coração); a
  **liberdade de manipular antes de responder** (manipulável ≠ quiz).
  Onde somos melhores: **som e voz** (eles não têm) e **andaime** (uma resenha
  independente aponta: "sem feedback automático, sem progressão, exige adulto").
  **⇒ REGRA (confirma a nossa):** manipulável tem SEMPRE um momento de manipular
  livre antes da pergunta; e a nossa vantagem (voz + andaime) fica.

### Toy Theater (EUA) — manipulativos e joguinhos para os pequenos
- **O que é:** centenas de manipulativos virtuais e jogos (relógio, tangram,
  blocos de base dez, balança, dinheiro), gratuitos, para pré/1º–3º.
- **O que medi rodando:** o jogo mora num **iframe** cercado de **anúncios** (8–11
  frames; alvo mínimo 15 px = os anúncios); fonte mínima 10–11 px.
- **O que a gente leva:** a gama (é o nosso catálogo de manipulativos quase igual)
  e o aviso: **propaganda em site infantil polui a medida e a atenção** — a nossa
  casa é sem anúncio, e isso é vantagem pedagógica, não só estética.

### PBS KIDS (EUA) — jogos com personagem, pesquisa e telemetria
- **O que é:** jogos de personagens (Daniel Tiger, Wild Kratts…), gratuitos, com
  princípios editoriais públicos (inclusão, pesquisa com crianças, especialistas
  de conteúdo) e **telemetria de aprendizagem** (com o CRESST/UCLA: milhares de
  eventos por sessão; predizem desempenho em matemática — correlação com TEMA-3;
  relatórios para os pais).
- **Achados de pesquisa (EDC/CCT, estudo dos "transmedia suites"):** as crianças
  achavam os jogos divertidos, **mas quase nunca sabiam dizer o que estavam
  aprendendo** — precisavam do adulto para reconhecer o objetivo; **sem adulto
  perto, pulavam de jogo em jogo e ficavam pouco em cada um**; **desafio crescente
  sustenta o engajamento**; a ligação com o personagem/narrativa segura a criança.
- **O que medi rodando:** **Pointer Events** nos alvos (`pointerdown/up/enter/leave`),
  **"squish"** (a peça encolhe 100–150 ms ao pressionar — `transition .1–.15s`,
  `transitionend`), alvos ≥ 117×128 px, mascote na capa.
- **O que a gente leva:** (1) **a criança precisa OUVIR o que está aprendendo**
  — o nosso "conceito por último, dito pelo mascote" e o parecer em palavras
  atacam exatamente o achado do EDC; (2) o **squish ao pressionar** como resposta
  tátil imediata (já temos `:active{translateY(3px)}` — manter em TODA peça);
  (3) **telemetria**: o nosso relatório do professor já mede acertos/dicas/tempo
  — a direção deles (predizer aprendizagem pelo jogo) é a nossa "prova de sala".
  **⇒ REGRA (nova, medível):** todo alvo tocável responde ao PRESSIONAR (não só
  ao soltar) em ≤150 ms — o `_qa/leiaute.js` pode medir `:active`/transition.

### Sesame Workshop / Joan Ganz Cooney Center (EUA) — a pesquisa por trás
- **O que é:** o laboratório de pesquisa da Vila Sésamo. Relatórios abertos:
  *Level Up Learning* (Takeuchi & Vaala 2014 — uso de jogos por professores),
  *Translating Literacy Research to Edtech*, guias de design. Pergunta-mãe: "como
  a mídia emergente pode educar crianças?"
- **O que a gente leva:** a **tradição de testar com a criança e medir** (a
  "Aprovação do professor" da casa é isto) e a obsessão por **alfabetização** como
  meta de produto — bate com o nosso 1º/2º ano.

### ICT Games e Topmarks (Reino Unido) — fluência e "starter" de 5 minutos
- **O que é:** duas casas de professores: ICT Games (jogos de EYFS/KS1 — valor
  posicional, contagem, relógio, fonemas) e Topmarks (400+ jogos, *Hit the Button,
  Daily 10, Teddy Numbers, Caterpillar Ordering, Teaching Clock, Coins*), sem login,
  funcionam na lousa e no tablet.
- **O que a análise independente (Structural Learning, 2022–2026) diz:** ótimos
  para **fluência e recuperação** (retrieval practice) em rajadas curtas —
  *"model the strategy first, use the game for focused retrieval, then move back
  to manipulatives"*; **não** para lacuna conceitual; o aluno anota **um fato que
  o atrasou e explica a estratégia** depois do jogo. Autonomia + competência
  (Deci & Ryan) explicam o engajamento.
- **O que a gente leva:** confirma a nossa arquitetura: **aquecimento**
  (recuperação espaçada) como peça curta e rápida, e **ensino do conceito antes**
  — o `relampago` é o nosso "Hit the Button". **⇒ REGRA (confirma):** peça de
  velocidade não recebe andaime (já está no `pedagogo.py`), mas termina com UMA
  pergunta de reflexão do mascote ("qual foi a mais difícil?").

### GCompris (aberto, KDE) — 180+ atividades de 2 a 10 anos
- **O que é:** software livre com ~180 atividades por área (leitura, matemática,
  ciências, geografia, música, artes, lógica), sem anúncio, 50+ línguas, cada
  atividade com **descrição pedagógica** (objetivo, pré-requisito, manual).
- **O que a gente leva:** o **catálogo como documento** (cada atividade declara
  objetivo/pré-requisito — é o nosso `conteudo.json` + `INTERATIVIDADES.md`), e
  a **progressão por nível dentro da mesma atividade** (a nossa "escada didática").

### JClic (Catalunha, desde 1992) — os 7 tipos que geraram 16 variantes
- **O que é:** o avô do nosso leque; aberto; milhares de atividades de
  professores. **7 tipos básicos → 16 variantes:** associação simples e
  complexa (1-1, vários-1, soltos), memória (pares iguais ou relacionados),
  **exploração** (clica e vê a informação), **identificação** (clique nos que
  cumprem a condição), **tela de informação**, quebra-cabeça (duplo, troca,
  buraco), **texto**: completar, preencher, identificar elementos, ordenar
  palavras/parágrafos; resposta escrita; cruzadinha (definição escrita, gráfica
  ou sonora); caça-palavras (com conteúdo que aparece a cada palavra achada).
  Tem **gravação de voz** para comparar pronúncia e **relatório** (tempo,
  tentativas, acertos).
- **O que a gente leva:** a taxonomia é um espelho para conferir o nosso leque
  (temos todas; as variantes "identificação" e "exploração" são as nossas
  `achar-na-cena` e `vitrine`); **cruzadinha com definição SONORA** é ideia para
  o 1º ano (a criança ouve a pista); **caça-palavras que mostra conteúdo a cada
  palavra achada** (a palavra "ensina" ao ser encontrada) — barato e forte.
  **⇒ IDEIA:** `caca-palavras` ganha, opcionalmente, figura+voz ao achar a palavra.

### Wordwall (Reino Unido), LearningApps (Suíça), Educaplay (Espanha) — "molde + conteúdo"
- **O que são:** fábricas de atividades para professores: o professor escolhe um
  **molde** (ligar, anagrama, roda, quiz, caça-palavras, verdadeiro/falso…), entra
  com o conteúdo, e **troca de molde com um clique** (Wordwall: *"the content is
  the game — students win by knowing the answer, not by earning points"*).
  Wordwall cita estudos (Scopus) com ganho de vocabulário e engajamento em EFL;
  a maior parte com 9–15 anos.
- **O que a gente leva:** somos a mesma ideia (motor + peças + `conteudo.json`)
  levada mais longe (voz, mascote, andaime, relatório). A lição deles: **o mesmo
  conteúdo em vários moldes** é o que evita a "mesma tela pela terceira vez" — o
  nosso `padrao.py` (≤40 % por gesto, ≥4 gestos) mede isto.

### Toca Boca e Khan Academy Kids (apps) — dois extremos que ensinam
- **Toca Boca:** brinquedo digital **sem regras, sem pontuação, sem tutorial** —
  confia na criatividade da criança; forte em faz-de-conta e narrativa.
  **Khan Kids:** caminho adaptativo com personagens, leitura em voz alta, sem
  anúncio, gratuito.
- **O que a gente leva:** as nossas 4 peças de **produção livre** (`pintar`,
  `pintar-canvas`, `pintar-desenho`, `criar-desafio`) são o lado Toca Boca — e o
  fecho de atividade ("exposição", "post-it de curiosidade") também; o resto é
  Khan Kids (objetivo claro, voz, progressão). **Regra que fica:** produção livre
  **sem cronômetro e sem "acertou/errou"**.

### Escola Games e NOAS (Brasil) — os vizinhos
- **Escola Games:** jogos por ano e disciplina, alinhados à **BNCC**, gratuitos
  (com anúncios); guias para o professor ("verifique qual habilidade ele
  desenvolve", "observe se o aluno persiste diante do erro").
  **NOAS** (UFC): objetos de aprendizagem por habilidade.
- **O que medi rodando:** Tailwind + swipers com `touch-action: pan-y`,
  `touchstart`+`pointerdown`, 40+ elementos animados, 46 svg; página de índice
  cheia de anúncios (jogo só pela página própria).
- **O que a gente leva:** a **ligação explícita à habilidade da BNCC** é o nosso
  `curriculo` no `conteudo.json`; e a cobrança do Marcos de **sem anúncio** é o
  diferencial concreto frente ao vizinho.

---

## 2. Os fundamentos (por que as boas fazem o que fazem)

### 2.1 Os 4 pilares + 1 (Hirsh-Pasek, Zosh, Golinkoff, Gray, Robb & Kaufman, 2015 — *Psychological Science in the Public Interest*)
"Educacional" é o app que promove aprendizagem **ativa** (*minds-on*, não só
dedo-on: pensar, não só deslizar/tocar), **engajada** (ficar na tarefa,
**sem distração de elementos periféricos** — os "hot spots" que pulam, sons e
enfeites fora do objetivo), **significativa** (liga ao que a criança já sabe e à
vida dela; expande o conceito, não decora) e **socialmente interativa**
(interações **contingentes** — respondem ao que a criança fez — e adaptáveis;
com adulto ou colega), **a serviço de um objetivo de aprendizagem** claro, num
contexto de **exploração com andaime** (não instrucionismo).
- **Onde já estamos:** conceito por último (ativo), uma ideia por tela
  (engajado), problema do mundo primeiro (significativo), mascote que responde ao
  que ela fez e relatório para o professor (social/contingente), objetivo por fase.
- **O que cobrar mais:** o pilar **engajado** é medível — *tudo que se mexe na
  tela e não é o conceito é distração*. **⇒ REGRA (nova, medível):** fora do
  mascote e do alvo da fase, nada pisca/anima sem função (`_qa/leiaute.js` pode
  contar `animation`/`transition` em elementos que não são alvo nem mascote).

### 2.2 Motivação intrínseca (Malone & Lepper, 1987) e integração intrínseca (Kafai; Habgood 2005/2007)
Individuais: **desafio** (meta clara, resultado incerto, dificuldade ajustada,
feedback frequente e encorajador), **curiosidade** (sensorial — luz, som,
mudança; cognitiva — incompletude, inconsistência: a nossa "lacuna"),
**controle** (escolhas reais e resposta contingente à escolha) e **fantasia**
(endógena — ligada ao conteúdo, não decorativa; a criança se identifica com o
personagem). Interpessoais: cooperação, competição (a **endógena** vale mais
que ranking), reconhecimento (o trabalho da criança vira artefato visível).
**Integração intrínseca** (Habgood): o conteúdo mora nas partes MAIS divertidas
do jogo e é representado pela mecânica central — o contrário do
**"brócolis com chocolate"** (Bruckman 1999): quiz obrigatório para ganhar o
tiro; a matemática como barreira para a diversão.
- **Onde já estamos:** o EduVerse é "o mundo precisa" (fantasia endógena);
  escolha do crachá (controle); dica → apoio → revelar (desafio ajustado).
- **O que cobrar:** **reconhecimento endógeno** — a exposição/mural do fim da
  atividade com o que a criança fez (já existe em algumas; virar padrão do
  `FIM-DE-ATIVIDADE.md`). **⇒ REGRA (proposta):** toda atividade termina com um
  artefato da criança à vista (o que ela montou/pintou/escolheu), não só medalha.

### 2.3 Modelo de aprendizagem baseada em jogos (Plass, Homer & Kinzer, 2015 — *Educational Psychologist*)
Quatro engajamentos que o jogo pode acionar — **cognitivo** (o alvo de todos),
**afetivo** (emoção: personagem, estética), **comportamental** (o gesto) e
**sociocultural**. Elementos de design: **mecânica de jogo × mecânica de
aprendizagem × mecânica de avaliação** (têm que ser a MESMA coisa quando dá),
sistema de incentivos (estrelas, pontos — úteis num contexto, distração noutro),
**narrativa**, **estética**, trilha sonora, **adaptatividade** (medir a variável e
ajustar problema/andaime/feedback às ações) e **falha graciosa** (*graceful
failure*: errar é passo esperado e às vezes necessário — Kapur). Alerta deles:
*"é menos desejável usar enfeite de jogo para 'melhorar' mecânica chata e mais
desejável tornar a mecânica em si interessante"*.
- **Onde já estamos:** falha graciosa = "nunca a palavra errou" + andaime;
  adaptatividade = "Treinar o que faltou" (só quem ficou < 75 %).
- **O que cobrar:** que a **mecânica de avaliação seja o próprio gesto** (o
  relatório do professor lê o jogo, não uma prova no fim) — já é a direção;
  registrar como princípio no `EDUVERSE-FILOSOFIA.md`.

### 2.4 Feedback (Hattie; Shute 2008 — a pesquisa específica ainda em coleta)
Imediato, específico ("olhe o X"), sem julgamento da pessoa, **elaborado** quando
a criança erra (o porquê, não só o certo/errado), e **dosado**: ajuda cresce com
o erro (o nosso andaime). Malone & Lepper: frequente, claro, construtivo e que
constrói autoestima.

### 2.5 O que a criança consegue fazer com o dedo (NN/g *UX for Children 3–12*, 4ª ed.; WCAG 2.5.7/2.5.8)
Alvos grandes e gestos simples (motor fino ainda em formação: 6–8 anos erram
toques precisos); feedback imediato **visual e sonoro**; instruções **visuais e
faladas** antes do texto até 7 anos; 3–5 minutos por interação com recompensa
frequente; crianças **tocam em personagens e figuras esperando resposta** (tudo
que parece tocável tem que responder); se não funciona em 2–3 tentativas, **fecham
a aba**. WCAG 2.5.7: **toda ação de arrastar precisa de alternativa de ponteiro
simples** (o nosso "toque simples" — medido nas 32 peças de gesto: OK).
- **⇒ REGRA (nova, medível):** figura e mascote na tela **respondem ao toque**
  (fala ou reage), porque a criança VAI tocar — `_qa/vozresposta.js` pode
  estender para "toda figura grande tem `onclick`".

### 2.6 Acessibilidade e UDL (CAST, *Guidelines 3.0*, 2024)
Múltiplos meios de **representação** (voz + figura + texto), de **ação e
expressão** (arrastar E tocar E teclado), de **engajamento** (escolha, relevância,
autorregulação). Para nós: já temos voz em tudo e duas portas de entrada; falta
pensar **daltonismo** (nunca cor como única pista — o `divisao-dourado` usa cor
por casa: conferir se há forma/rotulo redundante) e **redução de movimento**
(`prefers-reduced-motion` já existe em algumas peças — virar padrão do motor).
- **⇒ REGRA (nova, medível):** nenhuma resposta depende **só** de cor
  (`_qa/contraste.js` pode conferir que alvos distintos diferem em forma/texto).

### 2.7 Gamificação × jogo (Plass; Wordwall; Topmarks; brócolis com chocolate)
Pontos/medalhas/ranking são **incentivo extrínseco** — servem para dar ritmo
(Topmarks, *Hit the Button*), não para ensinar; ranking entre colegas
(**exógeno**) é fraco e pode ferir; a **medalha da casa** é reconhecimento do
percurso, não competição. **Regra que fica:** sem ranking entre crianças; sem
"moedas"; a recompensa é **ver o mundo mudar** e o artefato próprio.

### 2.7b Andaime implícito (Podolefsky, Moore & Perkins 2014 — o PDF lido)
O framework do PhET, agora lido na fonte: o andaime é construído **na própria
ferramenta**, por **affordances** (o que convida a ser pego/mexido),
**restrições** (o que a ferramenta NÃO deixa fazer — e por isso guia), **pistas**
(*cueing*: cor, posição, movimento que chamam para o próximo passo) e **feedback**
(o mundo responde na hora). Assim o aluno acha caminhos produtivos **sem
instrução explícita**: *"guides without students feeling guided"*, servindo ao
mesmo tempo metas de conteúdo, de processo e de **agência** (o aluno se sente
dono do que está fazendo) — o que a instrução dirigida não dá. Contexto: o
debate instrução direta (Kirschner, Sweller & Clark 2006) × descoberta guiada
(Hmelo-Silver 2007); o andaime implícito é a terceira via.
- **Para as nossas peças:** é a definição precisa do que o Marcos chama de "o
  gesto ensina": a `divisao-dourado` só deixa dar um bloco por grupo por rodada
  (restrição), o grupo que falta pisca (pista), o total muda na hora (feedback),
  o bloco tem cara de pegável (affordance). **⇒ REGRA (proposta para o
  `EDUVERSE-FILOSOFIA.md`):** antes de escrever um enunciado, perguntar "que
  restrição/pista no DESENHO faria a criança descobrir isto sozinha?" — enunciado
  é o último recurso, não o primeiro.

### 2.7c Gamificação — os números (meta-análises lidas)
Efeito **positivo mas moderado** sobre aprendizagem: *g* = 0,50 (19 estudos,
*Educ. Psych. Review*) a 0,82 (41 estudos, 5 000+ participantes, *Frontiers*);
revisão 2008–2023 (*BJET*) confirma. **O que decide é o desenho, não a presença**
de gamificação: "BPL" (badges, points, leaderboards) colado por cima de tarefa
chata **subdesempenha** e dispara o **efeito de superjustificação** (recompensa
externa por algo que já era interessante reduz a motivação; tirada a recompensa,
o engajamento cai abaixo do inicial). Ranking **absoluto** desanima quem está
embaixo e leva a otimizar pontos em vez de entender; ranking **relativo** (só
os vizinhos) ou de **melhora** funciona melhor. Pela SDT, gamificação mexe em
autonomia e vínculo, **quase nada em competência**.
- **Para nós:** confirma a política da casa (sem ranking, sem moeda; medalha =
  percurso). Onde há "pontos" (placar de pares na memória, estrelas do boletim),
  eles são **marcadores de progresso da própria tarefa**, não recompensa externa
  — manter assim e nunca introduzir loja/moeda.

### 2.7d Como o PBS KIDS testa antes de publicar (WestEd, Ready To Learn)
A WestEd avaliou formativamente **24 versões alfa** de jogos de matemática com
professores e alunos de pré e fundamental: alinhamento a padrões, adequação à
sala, sugestões de melhoria e uma **análise cognitiva de tarefa** por jogo
(forças e pontos a melhorar). Ou seja: a casa mais rica do ramo publica só depois
de professor + criança + análise de tarefa — a nossa banca automática + "Aprovação
do professor" é a versão de escola pública disso, e a **análise cognitiva de
tarefa** é o que o `pedagogo.py`/`curriculo.py` tentam fazer sozinhos.

### 2.7e Fontes que não rendiam texto (registro honesto)
- **Shute 2008** (*Focus on Formative Feedback*): o PDF veio (37 pág.) mas com 4 KB
  de texto legível — não dá para citar da fonte. O que sei dela de formação (a
  confirmar quando abrir): feedback **elaborado** > só verificação; **específico
  e simples**; **imediato para tarefa difícil/novato**, **atrasado para
  transferência**; evitar comparação normativa e elogio à pessoa; dosar ("não
  interromper a criança que está tentando"). Nova busca por resumo HTML em curso.
- **H5P**: as páginas de tipo em `h5p.org` viraram home/fórum; o catálogo de tipos
  fica para o lote 3 do `ver-rodando` ou para a documentação (`h5p.org/documentation`).

### 2.8 O que medi por baixo das casas (lotes 1–2 do `ver-rodando`)
| casa | eventos | touch-action | alvo mín. | som | feedback (mutações/1 s) |
|---|---|---|--:|---|--:|
| MLC (Number Pieces, Geoboard…) | `mousedown`+`dblclick` no elemento; **pointer events no document** | auto | 20–38 px | nenhum | 21–81 |
| PhET | canvas único | — | — | WebAudio (11–39 fontes) | — |
| PBS KIDS | **pointerdown/up/enter/leave**; squish 100–150 ms | auto | 117 px | — | 5 |
| Escola Games | touchstart + pointerdown | pan-y | 35 px | — | — |
| JClic (zonaClic) | click; barra de acessibilidade (fonte, cinza, alto contraste) | — | 33 px | — | 8 |
| Toy Theater | jogo em iframe; anúncios | — | 15 px (anúncios) | — | 15 |
| **Nós (cobaia, 88 peças)** | mouse+touch (32) / pointer (1); `document` limpo a cada fase | **none/manipulation em 100 %** | **≥ 40 px (piso do portão)** | **voz + efeito em toda tela** | — |

Leitura: **em toque e alvo somos mais rígidos que todas** (touch-action medido,
40 px de piso, toque simples em tudo); **em som/voz somos únicos** (nenhuma casa
gratuita fala a resposta); **em movimento** o PBS KIDS tem o "squish" ao
pressionar e o MLC tem feedback visual mais denso que o nosso ao soltar.

---

## 3. O mapa para as nossas 88 peças — o que entra

| # | Regra proposta (fonte) | Medida | Onde |
|---|---|---|---|
| 1 | Alvo tocável responde ao **pressionar** em ≤150 ms (PBS KIDS "squish"; NN/g feedback imediato) | `leiaute.js`: `:active`/`transition` nos `.opt/.pc/.lig/.bin` | motor (`.opt:active` já existe) + peças sem `:active` |
| 2 | Fora do mascote e do alvo, **nada anima sem função** (pilar "engajado", Hirsh-Pasek) | contar `animation`/`transition` em não-alvos | `leiaute.js` |
| 3 | Figura grande e mascote **respondem ao toque** (NN/g: crianças tocam em tudo) | `onclick` em `img`/`svg` ≥ 80 px | `vozresposta.js` |
| 4 | Nenhuma resposta depende **só de cor** (UDL/daltonismo) | alvos distintos diferem em forma/texto | `contraste.js` |
| 5 | Manipulável tem **manipulação livre antes da pergunta** (MLC, PhET) | fase com `dados.livre` ou 1ª rodada sem acerto/erro | `base-dez`, `balanca`, `reta-numerica`, `relogio` |
| 6 | Simulador **tematizável** (PhET: o gesto expõe o conceito, em qualquer tema) | `simulador` aceita cena/variável do `conteudo.json` | `simulador.html` (hoje só água) |
| 7 | Caça-palavras que **ensina ao achar** (JClic) | figura+voz ao completar a palavra | `caca-palavras.html` (opcional `dados.mostra`) |
| 8 | Cruzadinha com **pista falada** (JClic, 1º ano) | `dados.voz` por pista | `cruzadinha.html` |
| 9 | Peça de velocidade fecha com **1 pergunta de reflexão** (Topmarks) | fala do mascote no `fimDaPeca` | `relampago.html` |
| 10 | Produção livre **sem cronômetro e sem certo/errado** (Toca Boca) | já é; registrar | `pintar*`, `criar-desafio` |
| 11 | Fim de atividade com **artefato da criança à vista** (reconhecimento endógeno) | tela final mostra o que ela fez | `FIM-DE-ATIVIDADE.md` |
| 12 | **Sem ranking, sem moeda** (gamificação exógena) | já é; registrar | `EDUVERSE-FILOSOFIA.md` |

**Prioridade (custo × ganho, minha proposta ao Marcos):** 1 e 2 (motor + portão,
uma tarde), 3 e 4 (portões), 6 (a maior lacuna do leque), 7–9 (peças de
alfabetização, baratas), 5 e 11 (roteiro/`FIM-DE-ATIVIDADE`), 10 e 12 (só registro).

---

## 4. Pendências desta pesquisa (o que ainda não li)
- Shute 2008 (*Focus on Formative Feedback*) — 3ª busca em andamento.
- PhET *implicit scaffolding* em PDF (arXiv 1306.6544) — em andamento.
- PBS KIDS Ready To Learn — lições de design (PDF) — em andamento.
- H5P tipos (a página de tipos) e gamificação × jogo — 2ª busca em andamento.
- Lote 3 do `ver-rodando` (Reino Unido, EUA, Espanha) — em andamento; buscas
  com diagnóstico (`BUSCAS.md`).
- Pesquisa brasileira: a busca trouxe mais alfabetização científica do que jogos
  digitais — refazer com termos de jogo digital + alfabetização.
