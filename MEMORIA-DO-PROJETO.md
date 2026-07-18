# 🧠 MEMÓRIA DO PROJETO — ler no INÍCIO de CADA sessão

> **Por que este arquivo existe:** eu (Claude) começo cada sessão do zero, SEM
> lembrar das anteriores. Então esta é a minha memória, por escrito, para eu
> reler e "lembrar" na hora. Se algo importante não estiver aqui (ou no
> `CLAUDE.md` / `MANUAL-MESTRE.md`), eu vou esquecer. **Toda capacidade ou
> decisão nova → anotar aqui.**
>
> **ANTES DE AGIR:** `git fetch origin <branch> && git status`. Se a cópia local
> estiver atrás, `git merge --ff-only origin/<branch>`. A pasta local pode estar
> VELHA (já enganou antes — ver "lição paga" no MANUAL-MESTRE.md). O trabalho
> vive nos COMMITS do GitHub, nunca só na pasta local.

## 🌐 DECISÃO DO MARCOS (2026-07): TRABALHAMOS SÓ ONLINE — esquecer "offline"
> O Marcos deixou claro (mais de uma vez): **a escola é ONLINE, sempre há internet.**
> **"Offline" NÃO é requisito.** Eu não devo mais usar "tem que rodar offline / HTML
> único offline" como argumento ou trava — isso já atrapalhou a conversa. O que
> **CONTINUA valendo** como restrição real é: **PC fraco da escola** (AMD FX-4300,
> 3,5 GB RAM, Win7, Chrome 109 / Firefox 106) → **leve e compatível**; e **custo baixo**.
>
> **Reflexo em Unity/motores pesados:** ser online **não** libera Unity. Os bloqueios
> reais que ficam são: (1) eu **não opero o editor do Unity** (é programa de tela, com
> licença; eu sou headless/linha de comando); (2) **Unity WebGL é pesado** (RAM/download)
> pro PC fraco da escola. O Monkey Mart roda por ser **WebGL/HTML5 muito otimizado** —
> mesma família do nosso Phaser. Logo, a qualidade "espetacular" vem de **arte + animação
> + game feel**, não do motor. Caminho certo = **Phaser + kit de sprites bem-feito**.

## 📦 DECISÃO DO MARCOS (2026-07): NÃO precisa ser HTML único — repo por aventura
> Também **não é requisito** espremer tudo num HTML só. Podemos ter **1 repositório por
> aventura**, com **pastas** (código, `assets/`, `dados/`, `audio/`). Isso é justamente a
> arquitetura PROFISSIONAL que já adotamos no **`educaverso-app`** (Phaser + TypeScript +
> **Vite** + build por **GitHub Actions** → publica no repo próprio). Ou seja: relaxar o
> "HTML único" **facilita** (multi-arquivo, atlas de sprites, code-split), não atrapalha.
> **O molde premium 1-HTML continua valendo só pro modelo LEVE antigo (atividades/hub).**
> O EducaVerso novo é multi-arquivo por repo.

## 🧊 DECISÃO DO MARCOS (2026-07): EducaVerso em 3D VOXEL (estilo Minecraft), com three.js
> Depois de testar tudo, o Marcos escolheu **3D voxel (blocos, tipo Minecraft) com three.js** —
> ele **rejeitou o desenhado-por-código 2D** ("ficou amador") e quis o mundo **explorável 3D**.
> - **RODOU no PC dele: 26–29 FPS** (jogável; 30 é o alvo do gênero). O 3D voxel é **viável na escola**.
> - **Otimização obrigatória** (pro FX-4300 aguentar): face-culling + **1 mesh** (BufferGeometry) por
>   grupo estático, **luz assada nas cores** (sem shadow map, sem luz dinâmica), resolução interna baixa
>   (`RQ`), **AUTO-QUALIDADE** (mede FPS; se <24, baixa `RQ` sozinho). Ilha da parada 1 = **~4 mil tri, ~55 draws**.
> - **Sem sombra/luz DINÂMICA** (cara demais p/ o PC fraco) — sombra é uma **manchinha** no chão + AO assada.
> - **Câmera orbita** (arrastar mouse gira) + **andar relativo à câmera** (WASD). Teclado+mouse é normal no 3D.
> - **Ganho enorme:** voxel **MATA o bug de arte** (recorte/membro faltando/inconsistência não existem — é bloco).
>   Objeto novo = uns cubos coloridos no código. Cenário novo = trocar DADOS (terreno + objetos a contar + falas).
> - **Onde está:** `_voxel/index.html` (three.js em `_voxel/three.module.min.js`), publicado por Fábrica/atualizar
>   no repo **`ilha-voxel-teste`** → https://vidalprof.github.io/ilha-voxel-teste/ . Roteiro pirata:
>   "Ilha das Trinta Moedas" (5 paradas 6→12→18→24→30). **Parada 1 (cocos) JÁ jogável** (contar tocando/andando).
> - **LEGAL:** NUNCA usar marca/logo/boneco LEGO (é cópia). Voxel/cubo é genérico e legal com o NOSSO Verso.

## 🔎 DISCIPLINA DE QA (o Marcos cobrou: "essas coisas não podem acontecer")
> Eu estava **usando o Marcos como QA** (mostrava tosco, ele achava o defeito). ERRADO — custa o tempo dele.
> **Antes de mostrar QUALQUER coisa visual, EU renderizo (headless + Playwright) e AUDITO** contra a lista:
> **(1) PROPORÇÃO** (personagem × cenário × objetos — o Verso é pequeno perto das árvores; papagaio ~1/3 do Verso);
> **(2) RECONHECÍVEL** (cada coisa parece o que é — coco redondo, não quadrado); **(3) nada FLUTUANDO** sem explicação;
> **(4) INTERAÇÃO** (o que é clicável é fácil de clicar/alcançar); **(5) CÂMERA** ok; **(6) FPS/leveza**.
> Bug de imagem (recorte/membro) **não é isso** — isso é **design/gosto**, e **nenhum motor decide** (nem Unity):
> é trabalho do DESIGNER (eu) + esta checklist. Cada tropeço novo → vira item da lista. **Só mostro o que passou no meu crivo.**

## ✅ O que EU consigo fazer (capacidades REAIS — não esquecer)
- **Criar e editar** as atividades (HTML/JS/CSS), cada uma em 1 arquivo único.
- **Publicar no ar:** commit/push + ligar o GitHub Pages (Fábrica de Sites).
- **GERAR IMAGENS** acionando o workflow **`gerar-imagens.yml`**:
  - `modelo=pollinations` (GRÁTIS) ou `modelo=gemini` (usa o secret `GEMINI_API_KEY`).
  - Pode EDITAR uma imagem base (input `base`) — mantém o personagem, muda o pedido.
  - Salva em `_novo/<nome>.png` e commita sozinho; eu depois dou `git pull`.
- **GERAR ÁUDIO / narração** com voz natural (workflow **`gerar-audio.yml`**,
  edge-tts — vozes Ricardo/Camila/Antônio... — + `otimizar-audio.yml`). Salva em `_audio/`.
- **Recortar imagens** (fundo transparente, sem franja) localmente com Python/Pillow.
- **Rodar equipes de especialistas** (workflows de pesquisa/redação).
- **Criar repositórios novos** e **atualizar outros repos** (workflows da Fábrica).

> ⚠️ A geração NÃO roda no chat (a rede do chat é travada — testar API direto
> dá **403, e isso é NORMAL**, não é "quebrado"). Ela roda no **WORKFLOW do
> GitHub**, que EU aciono (`actions_run_trigger`). **"O Claude gera" = o Claude
> ACIONA o workflow que gera**, e depois traz o resultado com `git pull`.

## 🔑 Secrets já configurados (no GitHub, nunca no código)
`PAGES_TOKEN` (criar/publicar repos) · `GEMINI_API_KEY` (imagem Gemini) ·
Firebase e Pollinations conforme o uso. O valor do secret nunca aparece no
código — só é usado dentro do workflow.

## 📦 O que já construímos
- **Atividades / hub "Ilhas do Saber":** Floresta dos Números, Vila do Miau,
  Desafio da Copa, Poli e o Tesouro do Mar, a confeitaria (Mundo Vivo), etc.
- **Manuais:** `MANUAL-MESTRE.md` (o principal), `ATIVIDADE-PREMIUM.md`,
  `MUNDO-VIVO-*.md`, `FABRICA-DE-MUNDOS.md`, `PLANO-FORA-DA-CAIXA.md`, os 5
  pareceres em `_plano/`.
- **Byte** (mascote robô) gerado em `_novo/byte.png`.
- **✅ DECISÃO FIRME DO MARCOS (não reabrir):** o motor é o **2D em TILE + pintura IA
  premium** (linhagem `eduverse/kit-floresta.py` — "A Floresta do Byte"), **NÃO** o motor
  antigo da confeitaria (`_pub_confeitaria/mundo/index.html`, que é **PESADO: 3 MB**).
  **Por quê:** o tile é **mais fácil de criar, mais rápido, mais leve e mais sustentável**
  (mundo novo = DADOS + peças reusadas, não um motor de 3 MB do zero) — e mantém o **mesmo
  visual lindo** (a arte é pintada por IA). **A FÁBRICA CLONA O MOTOR DE TILE**, não o da
  confeitaria. O "injetor" do tile **já existe** = `eduverse/builders/montar.py`
  (`dados.json` → `index.html`). **REGRA:** nunca reconstruir/clonar o motor pesado; se eu
  cismar de codar mundo na mão ou clonar a confeitaria, PARAR — a decisão é o tile leve.
- **Byte VESTE o tema:** cada atividade tem o Byte fantasiado do tema (pirata, viking…),
  gerado **editando a imagem-âncora** `byte.png` (mesmo personagem, só a fantasia) via
  `gerar-imagens.yml` (`modelo=gemini`, `base=eduverse/biblioteca/proc/byte.png`). O `byte_pirata`
  gerado (chapéu tricórnio + caveira + casaco vermelho, **rosto/tela idênticos**) PROVOU que
  qualquer tema funciona. A cartela de poses da fantasia entra sozinha no injetor
  (`assets.byte:"byte_pirata"` → puxa `byte_pirata_costas`, `_lado`, etc.). Falta gerar as 6 poses.
- **✅ MUNDO-VIVO v2 (jul/2026) — efeitos ricos JÁ no motor (equipe → integração auditada):**
  a equipe de especialistas (6 agentes por workflow + revisão do engenheiro-chefe) projetou
  e eu integrei no `kit-floresta.py`, tudo **data-driven e default-seguro** (mundo sem o campo
  fica igual): 🗨️ **balões RPG** (placa de nome + typewriter + ▼ + avança no toque, acima de
  QUEM fala — Byte ou NPC), 🌓 **sombra direcional** (sol/lua), 💨 **poeira ao andar** + lib de
  micro-movimento (`breathe/sway/blink`), ☁️ **nuvens** (chão+céu), 🌧️ **clima** (`MUNDO.clima`
  = chuva/neve/tempestade com trovão por Web Audio + vento visível), 🐾 **NPCs vivos**
  (`MUNDO.npcs`: patrulham rota, interagem com o Byte, acenam, abrem balão). **Checklist completo
  em `eduverse/style-bible/ambiente-vivo.md`.** Como os efeitos moram no MOTOR, TODO mundo que a
  fábrica gerar já nasce com eles — é o oposto de fazer na mão em cada atividade.
  **Nota de QA:** no screenshot headless (virtual-time) o rAF quase não acumula tempo → efeitos
  temporais (balão/typewriter) exigem um **driver `setInterval`** na foto; no navegador real (60fps)
  roda normal. Ainda pendentes (ver checklist): porta que range, tábuas, água (ondas/peixes),
  sons de animais CC0 (precisa `baixar-sons.yml`).

## 🏭 FÁBRICA DE ATIVIDADES por currículo (pedido do Marcos — incorporar no EducaVerso)
Gerar atividades AUTOMATICAMENTE, alinhadas ao currículo escolhido, e inserir no mundo.
- **Fontes de currículo:** BNCC geral, **Computação BNCC** (já há `ATIVIDADE-COMPUTACAO.md`),
  ou o **currículo de Blumenau** (já há `.github/workflows/baixar-curriculo.yml` que baixa o
  PDF e extrai o texto para ancorar a IA). O professor escolhe fonte + ano/turma + habilidade.
- **Como monta:** a IA LÊ o objetivo real do currículo (ancorada no texto — não inventa a
  habilidade) → escolhe a MECÂNICA (do catálogo de interatividades) → cria conteúdo/desafios →
  embrulha na narrativa do mundo (um personagem/lugar) → gera a arte (pipeline de imagem) e a voz.
- **Aprovação do professor** (as 3 aprovações: missões/pedagogia, arte, jogável) — a pedagogia
  passa pelo olho dele. "Automático" com portão de qualidade (a IA rascunha, o professor confirma).
- **Inserção no mundo:** a atividade vira ponto/NPC/gatilho no mundo; o resultado alimenta a
  avaliação descritiva. Fábrica de MUNDOS (o cenário) + Fábrica de ATIVIDADES (o aprendizado) =
  sistema de produção completo do EducaVerso.
- **Adequação à TURMA (faixa etária) é obrigatória:** a partir de DISCIPLINA + TEMA + TURMA, a
  Fábrica cria cenário, personagens, dificuldade, mecânica, narração e missões ADEQUADOS à faixa.
  Bandas: **pré/1º-2º (NÃO leitores → só ícone+voz+cor, missões curtas de 1 passo, muita
  recompensa)**; **3º-5º (leitura simples, missões de poucos passos)**; **6º-9º (missões
  multi-etapas, mais autonomia)**. A IA rascunha adequado à faixa; o professor confirma.
- **MISSÕES são o formato "legal de aprender":** cada aprendizado vira uma MISSÃO no mundo
  (um objetivo de história: ajudar X, recuperar Y, construir Z) e o conteúdo é o CAMINHO para
  cumprir. Curtas e concretas para os pequenos; quests de várias etapas para os maiores.
- **ALUNO ATIVO/PROTAGONISTA (inegociável):** a criança CONSTRÓI, interage e participa — nunca
  só assiste/escolhe alternativa. Ela monta a máquina, programa o robô, constrói a ponte, cria a
  solução. A construção SÓ funciona se o conceito estiver certo → construir = provar que entendeu.
- **AS FASES DEVEM ENTREGAR O OBJETIVO DO CURRÍCULO (gating + medição):** cada fase é desenhada a
  partir de um objetivo do currículo que o professor inseriu; completar a missão EXIGE demonstrar
  aquele objetivo (a construção "trava" até estar correta). A avaliação invisível MEDE quem
  alcançou o objetivo e quem precisa de apoio → relatório descritivo para o professor agir.
- Estado: groundwork existe (baixar-curriculo.yml, ATIVIDADE-COMPUTACAO.md, catálogo de
  interatividades); FALTA o montador que casa currículo→mecânica→mundo→faixa de forma semiautomática.

## 🎒 CAMADA DO ESTUDANTE + AVALIAÇÃO DESCRITIVA (pedido do Marcos, jul/2026) — "tudo que nossa ideia tinha"
O mundo tem que ser DO ALUNO e acompanhá-lo o ano inteiro. Requisitos (INEGOCIÁVEIS):
- **Tela inicial MARAVILHOSA — MODELO do Minecraft (NÃO o tema):** estrutura tipo "seus mundos"
  do Minecraft (você vê o SEU mundo salvo, entra e continua de onde parou, ou cria/entra), porém
  no NOSSO estilo **pintado por IA premium, MUITO mais bonito** (nada de visual de blocos). O
  estudante digita **NOME + TURMA** (e dados) → as informações dele são **puxadas** (histórico,
  progresso, personagem) → o mundo vira DELE (card do "mundo do aluno" com nome/turma/progresso).
  - **MARCA "EducaVerso":** a tela é BRANDED EducaVerso — **logo/título lindo e identidade visual
    própria** (nome + tema + a "cara" do EducaVerso), personalizada. É a porta de entrada com
    personalidade, não genérica. O roteirista + especialista em temática ajudam a definir essa identidade.
- **Interação pelo NOME:** o jogo/Byte/NPCs chamam o aluno pelo nome (voz + balão).
- **Progresso SALVO:** cada missão/atividade concluída fica registrada (retoma de onde parou).
- **AVALIAÇÃO DESCRITIVA contínua:** o sistema descreve o que o aluno demonstrou (por habilidade
  do currículo), acumulando por **mês / semestre / ano**. Alimentada pelo gating pedagógico
  (completar a missão = provou a habilidade → vira frase descritiva).
- **Opção de virar NOTA:** se o professor quiser, a avaliação descritiva converte em nota.
- **Painel do PROFESSOR:** ele vê a turma, o progresso e a avaliação de cada aluno (relatório).
- **DESAFIO TÉCNICO (honesto):** salvar progresso + o professor ver central = precisa de BACKEND
  (não só localStorage, que é por-aparelho/por-navegador e o professor não enxerga). Candidato
  natural: **Firebase** (Firestore + Auth) — há indício de Firebase nos secrets (`GEMINI_API_KEY`
  "Firebase/Pollinations conforme uso"); free tier, funciona a partir do Pages estático. Alternativas:
  Google Sheet/Apps Script. **A EQUIPE precisa desenhar esta camada** (persistência + modelo de dados
  do aluno + tela inicial + agregação da avaliação + conversão em nota + painel do professor).
- **Adequação por TURMA/idade** vale aqui também: tema, mecânica, FALAS, missão e voz mudam por faixa
  (pré/1-2 não-leitores → só ícone+voz+cor; 3-5 leitura simples; 6-9 multi-etapas). `dialogo.cps`
  (velocidade do balão) mais lento pros pequenos.
- **Régua de qualidade (Marcos):** 2D tile + **arte pintada por IA premium** = qualidade "quase real"
  que **prende o estudante** — é o diferencial que chama a atenção. Não baixar essa régua.

## 🗓️ SESSÃO jul/2026 — decisões e pedidos novos ("documentar tudo p/ nada se perder" — Marcos)
- **Mundo-vivo v2 no motor (FEITO, auditado):** balões RPG (nome+typewriter+▼+toque, acima de quem
  fala), sombra direcional, poeira ao andar, nuvens, clima (chuva/neve/tempestade+trovão), NPCs vivos.
  Ver `eduverse/style-bible/ambiente-vivo.md`.
- **Balões — DECISÃO FINAL do Marcos (jul/2026):** ele NÃO gostou do balão de fundo PRETO/escuro
  atual (`balaoDes` em `kit-floresta.py`) e pediu **CAIXA DE RPG CLÁSSICO** (estilo Zelda/Pokémon
  16-bit): retangular, **FIXA na parte de baixo da tela** (não segue o personagem/não flutua acima
  da cabeça), **fundo claro sólido** (branco/bege, NUNCA preto/transparente escuro), **borda grossa
  dupla** no estilo pixel-art. Substitui a caixa escura por essa; manter typewriter+▼+nome na placa
  (já existentes) só trocando a paleta/formato/posição. Aplicar em TODO mundo (é o motor, não por
  atividade). (Havia 2 opções candidatas — branco-quadrinho-arredondado × caixa-RPG-clara-fixa-embaixo
  — ele escolheu a 2ª.)
- **EQUIPE AMPLIADA** (rodar como agentes por workflow): além dos 6 (eng. software, eng. jogos,
  pedagogo, IA/prompts, produção/ops, produto), CONTRATAR: **Roteirista de histórias** · **Especialista
  em temática** (temas das fases por faixa) · **Especialista em PROMPT do GEMINI** — foco: **gastar o
  MÍNIMO possível sendo PRECISO** (Gemini é pago; economizar tokens/chamadas + precisão ao editar a
  imagem-âncora do Byte). Fazer um "playbook" de prompts econômicos p/ imagem.
- **Tela inicial = branded EducaVerso** (logo/identidade própria), MODELO "seus mundos" do Minecraft
  (continuar o mundo salvo) — **NÃO pode ser CÓPIA do Minecraft** (nada de blocos; visual pintado
  premium PRÓPRIO). Concept visual publicado (conceito, com efeitos + musiquinha Web Audio):
  https://claude.ai/code/artifact/ac466f52-adb6-4a9a-b21f-4be67b2197b7
- **3 PILARES inegociáveis (Marcos):** (1) 2D tile + **arte IA premium** = qualidade "quase real" que
  **prende o aluno**; (2) **adequação TOTAL por turma/idade** (tema, mecânica, falas, missão, voz);
  (3) **rápido, funcional, sustentável e vivo** (experiência maravilhosa, leve p/ escola).
- **DIREÇÃO DE ARTE na linha (lição paga — pedido do Marcos "não deveria ficar corrigindo se temos os
  profissionais"):** as correções da 1ª aula (fogueira sem contexto, fruta feia/grande, "quadrado")
  vieram do **Montador manual SEM Diretor de Arte**, não dos especialistas (o roteiro/pedagogia passou
  no Portão 0 de primeira). CONSERTO: **Diretor de Arte + Portão de Arte** entram na equipe/linha. Regras
  cravadas: (1) **PROPORÇÃO coerente com o Byte** (~64px) — a maçã (e objetos) tem que ser CLARAMENTE
  menor que o Byte; alvo fácil p/ 6 anos via **brilho + raio de toque invisível**, não aumentando o
  objeto; (2) **PROPS/objetos só com CONTEXTO** (maçãs PENDURADAS nas árvores + algumas caídas, não
  flutuando; fogueira só como cena de NOITE c/ aldeões); (3) **tudo pintado por IA**, nada geométrico
  code-drawn à mostra; (4) coerência com o style-bible. O mundo tem que chegar DIRIGIDO (o Marcos não
  corrige arte). E o **Montador automático** (conteudo.json→dados.json) ainda é a-fazer (hoje manual).
- **O ROTEIRO DIRIGE A CENA (modelo-mestre da fábrica — pedido do Marcos):** a história do
  **roteirista** NÃO é só as missões — é um **roteiro de cena por cena (breakdown)** que já ESPECIFICA
  o que cada cena precisa: **cenário, hora do dia, clima, quais PERSONAGENS estão presentes, quais
  EFEITOS, quais PROPS (e o porquê/contexto de cada um), a PROPORÇÃO dos objetos vs o Byte, e a ação
  da criança.** A fábrica trabalha A PARTIR desse roteiro: o **Diretor de Arte** realiza o visual, o
  **Engenheiro** liga os efeitos/mecânicas que a cena pede, e um **Portão de Coerência** verifica
  ("faz sentido? falta algo nesta cena? está coerente com a história?"). Isso faz a fábrica PENSAR em
  tudo (proporção, contexto, efeitos, personagens) de forma organizada, saindo da história — em vez de
  remendo depois. ➜ **AÇÃO:** expandir o schema do roteirista p/ incluir o breakdown de cena; e o
  Portão de Coerência entra na linha. (Foi a lição da 1ª aula: a arte/contexto tem que vir do roteiro.)
- **VOZ (decisão firme do Marcos — corrige o estudo da equipe):** NADA de voz do navegador
  (speechSynthesis). A narração é **SEMPRE gerada via API (edge-tts — Antonio/Francisca…) e volta como
  MP3 embutido** (base64). Voz natural, padrão premium. Peso: `otimizar-audio.yml` + cache por hash.
  Voz própria por personagem. (O `EDUCAVERSO-PLANO-FABRICA.md` supõe voz runtime p/ economia — ISTO
  sobrepõe: sempre gerada, ainda grátis via edge-tts.) Ver `EDUCAVERSO-SUSTENTABILIDADE.md`.
- **SUSTENTABILIDADE (produção + dados) documentada:** `EDUCAVERSO-SUSTENTABILIDADE.md` — produção
  ~grátis (Pollinations + edge-tts + Actions público + Pages; Gemini só na fantasia do Byte, cacheado);
  dados mínimos (~2 KB/aluno + rollup anual + só 1º nome) no Firebase free, com **backend PLUGÁVEL**
  (interface `salvar/carregar` — trocável sem mexer no jogo).
- **ARQUITETURA DA FÁBRICA (estudo da equipe):** ver **`EDUCAVERSO-PLANO-FABRICA.md`** — recomendação
  **HÍBRIDA**: uma ESPINHA (linha em fases: briefing→mecânica→roteiro→arte→voz→montador→auditor→3
  portões→publicação) + FÁBRICAS-SIDECAR (os workflows do GitHub, como funções puras cacheadas por
  hash) + CATÁLOGO DE MECÂNICAS como BIBLIOTECA fixa (não gerador). Contratos = JSON versionados no git
  (briefing→receita→conteudo→dados→index). MVP = rodar a pipeline INTEIRA com a mecânica atual.
- **UX da tela inicial — COMPUTADOR COMPARTILHADO (pedido/problema do Marcos):** muitas turmas, VÁRIOS
  alunos usam o MESMO PC no dia (troca de aula rápida), turmas têm seções **A, B, C…**. Desafio: pôr isso
  sem poluir. **Recomendação (proposta):** DIVULGAÇÃO PROGRESSIVA em 3 toques, 1 tela limpa por vez —
  (1) escolher o ANO; (2) aparece a letra da seção (A/B/C…); (3) **grade de NOMES da turma** (nome +
  mini-avatar/mascote) → o aluno **TOCA no próprio nome** (SEM digitar — ideal p/ não-leitores e p/
  troca rápida). Fallback "não achei meu nome → digitar". O PC **lembra a última turma** (a próxima
  criança da mesma turma já cai na grade de nomes). Só se vê UMA turma por vez → nunca polui. Depende da
  LISTA DE TURMAS/alunos (o professor fornece) + save no Firebase (`/mundos/<turma>/<aluno>`). Casa com o
  login documentado "código de turma + primeiro nome".
- **União das 2 ideias (já documentada — reler quando esquecer):** `EDUCAVERSO.md` (mestre da união) ·
  `EDUVERSE-*.md` (visão da outra IA "EduVerse": FILOSOFIA/PIPELINE/PLANO/EQUIPE/FASE0/COMPUTACAO) ·
  `MUNDO-VIVO-*.md` + `IDEIA-MUNDO-VIVO.md` + `PLANO-FORA-DA-CAIXA.md` + `_plano/*.md` (linhagem Mundo
  Vivo do Marcos) · `EDUCAVERSO-QA.md` (os Portões 0-3) · `ATIVIDADE-PREMIUM.md` (formato fixo).

## 🏭 ESPECIFICAÇÃO-MÃE DA FÁBRICA (Marcos, jul/2026 — o produto em 1 parágrafo)
> "Eu passo o TEMA DA AULA e a TURMA (ex.: adição para o 1º ano) → a fábrica me
> SUGERE o tema/ambiente (pirata, espacial, floresta, cidade...) → nesses temas
> JÁ EXISTEM os personagens, objetos, sons, animação, tudo pronto → deve haver um
> BANCO com ~10 TEMAS diferentes, com personagens e tudo mais pronto em cada tema
> para REAPROVEITAR → e quando eu pedir, GERAR um tema de ambiente NOVO (que
> entra no banco)."
- **BANCO DE TEMAS** = a peça central: cada tema é um pacote completo (cenário/tiles,
  personagens com poses, props com contexto, paleta, sons, falas-modelo) validado UMA
  vez pelos portões; as atividades só o REUSAM (custo marginal ~zero, qualidade estável).
- Entrada da fábrica: `disciplina + conteúdo + turma` → saída: atividade completa
  (tema do banco + mecânica do catálogo + história própria + voz gerada) já auditada.
- Tema novo = pipeline de criação de tema (gera assets via gerar-imagens.yml, valida
  nos portões, registra no banco) — roda só quando o Marcos pede.
- Meta do Marcos: "usar o Claude como uma EQUIPE que entrega produto espetacular
  pronto" — cada especialista faz sua parte e SAI PRONTO (sem o Marcos corrigir arte).

## 🤖 DECISÃO FIRME — TUDO AUTOMÁTICO, NADA À MÃO (Marcos, jul/2026)
O Marcos quer a fábrica **100% automática**: ele digita o pedido (ex.: "adição, 1º
ano") e a linha PRODUZ tudo — quem "faz à mão" é a fábrica (workflows), nunca o
Marcos nem o Claude posicionando coisa a coisa.
- **NÃO usar editor MANUAL como etapa obrigatória** (ex.: Tiled/LDtk para desenhar
  mapa à mão = descartado; a IA GERA o layout e os PORTÕES auto-corrigem/refazem).
- **Pilha grátis por API/workflow:** imagem = Pollinations (sem chave) + Gemini
  (free tier); voz = edge-tts; sons = Web Audio + Freesound CC0; conteúdo/mundo/
  história/dados.json = a IA; qualidade = os 4 portões (reprovam e mandam refazer);
  publicação = workflows da Fábrica. Nada disso exige o Marcos.
- **Movimento "vivo" do personagem, automático:** (1) gerar CICLO de frames de
  caminhada pela IA de imagem (já provado na FASE E — 2 frames do Gemini, sem
  desenhar à mão); (2) piloto do **Meta "Animated Drawings"** (grátis, open source,
  roda em workflow: 1 imagem → esqueleto auto → anima). DragonBones/Spine são
  editores MANUAIS (rigging à mão) — NÃO têm API automática; só valem se o Marcos
  aceitar riggar o personagem UMA vez e reusar em todos os mundos ("à mão 1x,
  automático pra sempre") — hoje ele quer nada à mão, então ficam de fora por ora.
- **Único passo humano que sobra:** o "OK" final do Marcos (aprovar), e mesmo esse
  é opcional. "Automático" = quando não fica bom, a LINHA detecta e refaz sozinha,
  sem chamar o Marcos (auto-corrigível, não mágico/perfeito de primeira).
- **Referência estética travada:** a cena do INTERIOR da Taberna (luz de lampião,
  aconchego) = o padrão de beleza; "só faltou ser MAIS VIVA" (chama tremulando,
  poeira no facho de luz, NPCs respirando/gesticulando, gato que anda, lareira). O
  motor já tem os ingredientes — é ligar na cena. Somado à CENA-PINTURA (a IA pinta
  a cena inteira de uma vez = beleza do navio + quase nada a posicionar = mais auto).

## 🗺️ A GRANDE AVENTURA — estrutura do mundo (visão do Marcos)
> **REAFIRMADO pelo Marcos (jul/2026), versão cristalina:** cada MUNDO é uma
> JORNADA contínua guiada por HISTÓRIA, não atividades soltas. O LOOP é:
> **faz a tarefa que a atividade pede → GANHA a recompensa (ex.: a CHAVE) → a
> chave ABRE algo (ex.: a caverna/cabana) pra DORMIR e INTERAGIR → AMANHECE →
> segue o CAMINHO até a próxima tarefa → nova recompensa → ...** por ~**10 fases**
> nesse mundo, até **cumprir um objetivo** — sempre a história costurando tudo.
> As "atividades" (contar, subtrair, memória, arrastar...) são as TAREFAS de cada
> parada; a recompensa+interação+dia/noite são o TECIDO entre elas. É a camada de
> JORNADA por cima das estações. O motor JÁ tem os ingredientes (dia/noite, chave,
> entrar em cabana/taberna com interior+lampião, NPCs vivos) — falta STITCHAR num
> caminho contínuo de ~10 fases com recompensa/gate por fase. Cada mundo do banco
> de temas nasce como uma dessas jornadas.
>
> **ESCLARECIMENTO CRÍTICO (Marcos):** o exemplo "chave→caverna→dormir" foi SÓ um
> exemplo — **NÃO é template fixo.** Quem DEFINE o enredo, as recompensas e o FINAL
> é a **IA (o roteirista da fábrica)**, ÚNICO por mundo/tema. A estrutura acima é só
> a FORMA (fases encadeadas por história com recompensa/gate); o CONTEÚDO da história
> (qual é o problema, o que se ganha, qual o desfecho) a IA cria. E a **criança é
> PROTAGONISTA**: ela **CRIA/CONSTRÓI e cumpre os objetivos** de cada fase para
> avançar e **CONCLUIR a história** (não só assiste/escolhe — casa com o "ALUNO
> ATIVO/PROTAGONISTA" e a FILOSOFIA do EDUVERSE: o mundo precisa, ela resolve). O
> roteirista gera: enredo + arco de ~10 fases + recompensa de cada fase + FINAL que
> fecha o enredo; o montador encadeia; os portões conferem coerência/pedagogia.

O EducaVerso pode ser uma AVENTURA grande e contínua (uma floresta com caminho), não fases soltas:
- **Loop:** explorar a floresta → interagir → achar a CHAVE → atravessar um LABIRINTO → abrir a
  JAULA → SALVAR o amiguinho preso (animação: chave destranca, som, o amigo agradece) → seguir em
  frente → entrar numa CASA/CABANA (interagir, achar a próxima chave) → próximo labirinto → e assim
  vai (achar chaves, interagir, salvar personagens).
- **Vários** labirintos e **vários** personagens para salvar, ao longo do caminho.
- **LABIRINTO REAL DE PEDRA (ideia do Marcos):** um labirinto DE VERDADE — muros de pedra (tile
  premium de IA) preenchem a MAIORIA das células, deixando só **corredores sinuosos com becos sem
  saída**; existe **um caminho certo** até o amiguinho preso. A criança programa as setas para o
  Byte **serpentear pelos corredores** até chegar. NÃO é grid aberto com poucas árvores — é maze
  real. Usar na atividade "A Floresta do Byte". (Gerar/definir layouts de labirinto reais.)
- **Casas/cabanas vivas:** chaminé soltando fumaça, lenhador cortando lenha, detalhes que as
  crianças amam.
- **Ciclo dia/noite com HISTÓRIA:** escurece → o Byte precisa entrar na cabana, chegar perto da
  cama e DORMIR um pouquinho → amanhece → sai e continua a jornada.
- **Fases de ALÍVIO** intercaladas (memória-no-chão, pegar vaga-lumes, etc.).
- **Muita animação e SOM:** chave destrancando, jaula abrindo, o amigo agradecendo, fumaça,
  machado do lenhador, porta batendo, vento, gato miando, trovoada.
- **Como o SOM funciona (2 camadas, honesto):** (1) **Web Audio sintetizado** (grátis, minúsculo,
  offline) — vento (ruído filtrado + LFO), trovão (rajada de ruído), porta (batida grave + rangido),
  machado (toc percussivo), passos, chave (tilintar), faísca, UI. JÁ uso trovão assim. (2) **Sons
  realistas** (miado real, pássaros, lenhador) ficam melhores como **clipes mp3 CC0** embutidos —
  origem: pacote livre (CC0) ou o professor fornece (o chat não baixa; workflow pode). Regra do
  navegador: som e voz só começam após o 1º clique/toque → botão "🔊 Som" + mudo (volume).
- **A pedagogia mora DENTRO:** cada chave/labirinto/jaula guarda um desafio de aprendizado do
  currículo — a aventura é o embrulho; o aprender é o conteúdo (aprender sem perceber).
- **Blocos que JÁ temos (prova de conceito):** mundo explorável + dia/noite/clima (demo Mundo
  Vivo); entrar em casa + interior + lampião + NPCs + chave/inventário/porta (demo Taberna);
  guiar personagem por caminho com placas (demo Jardim/Placas). FALTA costurar num mapa contínuo
  + o labirinto + a cena de dormir + mais personagens/animações/sons.

## 🚦 DECISÃO DE ROTA (Marcos, jul/2026) — "começar pelo mundo vivo + paradas + popups; o plano ousado depois"
Reconciliação madura do Marcos (decisão FIRME de por onde começar), depois de sentir que fazer TUDO
imersivo dentro do mundo estava difícil demais para uma tacada só:
- **COMEÇAR pelo MUNDO VIVO** com tudo que ele já pediu (floresta viva, caminho, dia/noite, clima, NPCs,
  som). As **PARADAS** do mundo são temáticas: na floresta = **cabanas com FUMAÇA lindas** em que dá pra
  **ENTRAR no interior aconchegante cheio de efeitos** (o padrão da Taberna, trazido pro motor de produção);
  em outro mundo = outras paradas temáticas, e assim por diante.
- **As ATIVIDADES entram como POPUP no CENTRO da tela** — as atividades **premium que já conhecemos**
  (contar/ordenar/arrastar/memória/etc., reusadas do catálogo). Pragmático: entrega já, sem travar.
- **QUALIDADE DA ATIVIDADE/POPUP (regra firme do Marcos, jul/2026) — NÃO baixar:** a atividade que abre NÃO
  é um modalzinho pequeno que "o aluno nem enxerga direito". É uma **TELA CHEIA (FULLSCREEN)**, GRANDE. A ARTE
  dela tem que ser **GERADA e BEM BONITA**, com **EFEITOS, SONS, FALAS (voz gerada)** — o padrão PREMIUM que
  as atividades tinham, ENGAJADOR (o aluno gosta e quer jogar). Ex.: um **jogo da memória bonito com efeitos**,
  um **caça-palavras bonito com efeitos**. Cada tipo de atividade premium (memória, caça, quebra-cabeça, contar,
  arrastar...) é uma tela cheia caprichada, não um popup apertado. (Combina com o mundo, que também é fullscreen.)
- **CADA MUNDO tem VÁRIAS PARADAS, cada uma com SEU MASCOTE TEMÁTICO** (os mesmos mascotes das atividades
  premium — a atividade premium NÃO morre, vira uma PARADA com mascote dentro do mundo). **O DIFERENCIAL
  (definição do Marcos):** aqui não é uma página solta — é um **MUNDO que dá pra EXPLORAR**, com personagens,
  sons, vozes e efeitos, tudo que já combinamos do EducaVerso. O mundo dá a ALMA (exploração + vida); a
  parada entrega a PEDAGOGIA (popup premium com o mascote dela).
- **O PLANO OUSADO (aprender 100% DENTRO do mundo, interagindo) fica pra DEPOIS** — "mais pra frente a
  gente volta". NÃO é descartado; é adiado de propósito para não bloquear o lançamento. (O meio-termo já
  guarda alma: entrar na cabana e interagir no interior é imersivo; só a tarefa pedagógica é popup por ora.)
- **CAMADA DO ESTUDANTE junto (inegociável nesta rota):** um **SITE pra ENTRAR no mundo** (login simples),
  **SALVAR os dados do estudante** (progresso, onde parou) e a **AVALIAÇÃO do aprendizado** dele. Isso exige
  **BACKEND** (Firebase free — login por código de turma + nome; ver seção "CAMADA DO ESTUDANTE"). É o único
  pedaço pesado e novo, e depende de um SETUP do Marcos (criar projeto Firebase + dar a chave como secret).
- **Fácil x difícil (honesto):** fácil/reusa = mundo vivo, cabana+fumaça+interior, popups de atividade
  premium. Difícil/novo = a camada do estudante (backend/save/avaliação).
- **Ordem de construção proposta (MVP fatia vertical, pra NÃO espalhar):** (1) trazer "entrar na cabana +
  interior vivo" pro motor de produção; (2) uma parada abre um POPUP com uma atividade premium; (3) concluir
  a atividade = parada "resolvida" + avança no caminho; (4) TELA INICIAL do EducaVerso LINDA (branded,
  logo/identidade própria, modelo "seus mundos" do Minecraft mas pintado premium, com efeitos + musiquinha
  Web Audio) — o Marcos quer "bem linda como a PRIMEIRA que você me passou" = o CONCEITO que ja publiquei:
  https://claude.ai/code/artifact/ac466f52-adb6-4a9a-b21f-4be67b2197b7 (RECUPERAR esse conceito e construir
  a tela real a partir dele; digita NOME+TURMA) + SAVE local; (5) backend
  Firebase (progresso + avaliação + painel do professor). Provar a fatia com 1 mundo (floresta) + 2 paradas
  antes de escalar.

## 🏴‍☠️ 1ª ATIVIDADE DO MODELO NOVO — NAVIO PIRATA (Marcos, jul/2026) — em produção
Números até 30, 1º ano, CONCRETA (estilo Floresta dos Números), tema NAVIO PIRATA em alto-mar, Byte PIRATA
(reusa byte_pirata.png), paradas temáticas, muita animação+som. Equipe (pedagogo verifica o que o aluno
aprende + roteirista + diretor de arte + arquiteto de dados) monta história e o dados.json.
- **GERAR o que faltar de arte, bem bonito, no padrão da demo do NAVIO** (`_demos/educaverso/navio` — convés
  pintado + mar, que o Marcos amou). Reusar: byte_pirata, mar, barril, baú/baú-tesouro, convés. Faltando
  (gerar via workflow): poses do Byte pirata (ou solução SUAVE sem perna), objetos de contagem temáticos
  (moedas, laranjas, bombas...), partes do navio, NPCs (papagaio/lobo-do-mar).
- **LAYOUT — DECISÃO (Marcos, jul/2026): usar a ILHA, não o convés.** Tentamos primeiro (A) o NAVIO como mundo
  (convés visto de cima), mas ficou APERTADO e a perspectiva 3/4 (mesma da floresta) BRIGA com um convés chapado
  (o mastro virou "navio dentro do navio"). DECISÃO = (B): o mundo é uma **ILHA no meio do mar** (praia/areia,
  palmeiras, caminho, paradas espalhadas — igual à floresta, que combina com a câmera 3/4), e o **NAVIO é a
  ÚLTIMA parada/destino** (explora a ilha preparando tudo → no fim embarca/zarpa pra Ilha do Tesouro). A câmera
  NÃO muda (3/4 já é ótima); só o CENÁRIO vira ILHA (encaixa nela). Os engenheiros propuseram as 2 opções e
  recomendaram a (A) só por ser + rápida (reuso 100%); ao VER, a (B) é mais bonita = iteração normal, não erro.
  RECONSTRUIR o navio-pirata como ILHA: praia (areia/mar/palmeiras), paradas como pontos da ilha, o navio como
  cena final. Reusa a força do motor de mundo aberto (floresta/pomar).
- **DINÂMICA das paradas (Marcos):** com POPUP — o aluno chega numa parada, **ajuda ALGUÉM do mundo**
  (um NPC) resolvendo a atividade; essa pessoa **dá uma RECOMPENSA**; o aluno **conserta/destrava algo** e
  **avança** pra próxima parada. (É o loop tarefa→ajuda alguém→recompensa→avança, com a atividade premium no
  popup — casa com a "camada de jornada" e o modelo novo.)
- **REGRA DE ANIMAÇÃO (Marcos):** tudo SUAVE — respiração, gestos, deslizar. Se perna alternando ficar dura,
  fazer SEM perna, só suave. Suavidade acima de perna.
- Blueprint em `eduverse/NAVIO-PIRATA-BLUEPRINT.md` (a equipe escreveu). **DECISÃO: fazer o v2** (tudo NOVO e
  BONITO — gerar toda a arte pirata temática + efeitos + vozes), não o v1 de reuso.
- **FASES DE ALÍVIO intercaladas (pedido do Marcos) — TEMÁTICAS + ligadas ao conteúdo:** além das 7 paradas
  pedagógicas, intercalar jogos de alívio (colorir, MEMÓRIA, jogo de SOMBRAS, LIGAR PONTOS, e outros do
  catálogo) — escolher alguns e fazer MAIS paradas. TUDO com a cara do tema (pirata) E do conteúdo (números
  até 30). Escolhas que ENCAIXAM em número+pirata: **LIGAR PONTOS 1→30** (desenha um navio/mapa do tesouro =
  ensina a ordem dos números até 30, perfeito no tema); **MEMÓRIA** (parear numeral↔quantidade de moedas, ou
  itens piratas); **JOGO DE SOMBRAS** (casar objeto pirata com sua silhueta: barril, canhão, papagaio);
  **COLORIR por número** (colorir cena pirata por número = reconhecer o numeral). Intercalar entre as paradas
  de aprender (alívio no meio, ex. após P3 e P5). HONESTO: memória/sombras já existem no catálogo; colorir e
  ligar-pontos-até-30 podem precisar ser construídos no motor — escolher os que melhor servem número+pirata.
  Construção do v2 (arte + vozes + alívios + auditar) após a Fase 1 (motor de personagem vivo).
- **APOIO AO ERRO POR CONTAGEM ACESA — FEATURE PREMIUM OBRIGATÓRIA (Marcos lembrou; CONFERIDO: hoje NÃO está
  no motor da aula, só há dica gentil):** quando o aluno erra numa tarefa de QUANTIDADE, o mascote fala "Não
  foi dessa vez! Vamos contar juntos, bem devagar." e **ACENDE cada objeto UM A UM, EM SINCRONIA COM A VOZ**
  (a luz do objeto k acende junto com a voz dizendo o número k) — só glow (`filter:drop-shadow`, SEM
  transform:scale). A FALA comanda a luz (encadear pelo callback do `falar`, não 2 relógios separados — ver
  MANUAL-MESTRE seção 6). No fim: "São N ao todo! Agora toque no número N." É PADRÃO das atividades premium.
  CONSTRUIR isso no motor/nas atividades de contagem (aula E popups premium de identificar quantidade). É
  requisito de entrega, não opcional.
- **CURADORIA = CURRÍCULO + EDUCAÇÃO (reforço firme do Marcos):** a escolha das mecânicas/atividades NÃO é
  por "ser divertida" — é ancorada no CURRÍCULO (BNCC/Blumenau) e na PEDAGOGIA. O especialista de
  interatividades cura junto com o pedagogo; toda mecânica escolhida serve um objetivo de aprendizagem real
  e a faixa etária. Diversão é o veículo, o aprendizado (verificado) é o destino.

## 🎮 PAPEL NOVO NA EQUIPE — GAME/LEVEL DESIGNER 2D (lição paga, jul/2026)
O convés-de-cima ficou apertado/incoerente (mastro virou "navio dentro do navio") porque faltava na equipe
um **GAME/LEVEL DESIGNER 2D** — o papel que pensa LAYOUT, PERSPECTIVA (a câmera 3/4 combina com o cenário?),
level design (o mundo é gostoso de explorar/jogar?) ANTES de construir. Tínhamos engenheiro/arte/roteiro/
pedagogia, mas esse olhar faltou. **AÇÃO: incluir o Game/Level Designer 2D na equipe/linha** — ele valida
layout+perspectiva+ritmo de exploração de cada mundo no PROJETO, evitando refazer depois. (Iterar é normal em
jogo — mas esse papel corta os erros grosseiros de layout de cara.) Junto com o Diretor de Arte e o Portão de
Coerência. E a linha modular (dados-driven) é o que torna a correção BARATA quando ela acontece.

## 🧱 ARQUITETURA MODULAR (direção do Marcos, jul/2026) — "um motor por coisa"
O Marcos propôs "fazer um motor pra cada coisa pra modularizar/automatizar" — incluindo o "aprender diferente"
como um motor À PARTE. INSTINTO CERTO (bate com os "12 módulos" da outra IA: Core/Render/World/NPC/Mission/
Dialogue/Inventory/Animation/Sound/Classroom/AI). AJUSTE IMPORTANTE: NÃO são motores DUPLICADOS separados (isso
reescreveria mundo/personagem/som toda vez) — são **MÓDULOS que se COMPÕEM** (peças de LEGO), cada um faz UMA
coisa e reusa os outros:
- **Módulo MUNDO** (cenário vivo), **Módulo PERSONAGEM** (o "ator vivo" universal — JÁ extraído ✅),
  **Módulo SOM/VOZ**, **Módulo ATIVIDADE** (plugável).
- **A ATIVIDADE é um MÓDULO PLUGÁVEL:** hoje = tipo "popup premium" + tipo "aula in-world" (rounds). O
  **"APRENDER DIFERENTE" (aluno cria/coliga/resolve o problema do mundo pra avançar) = um MÓDULO NOVO de
  atividade** ("construção/resolver-no-mundo") que pluga no MESMO mundo + MESMO personagem, SEM mexer no popup.
  Pode ser desenvolvido e testado SOZINHO e depois encaixado em qualquer mundo. É o jeito limpo de entregar a
  ideia ousada no futuro sem refazer o mundo.
- **HONESTO:** o motor hoje (`kit-floresta.py`) é meio MONOLÍTICO (mundo+personagem+aula juntos). Modularizar é
  investimento PROGRESSIVO; o sistema de personagem vivo foi o 1º pedaço tirado pra fora. Refatorar em módulos
  limpos conforme fizer a 2ª/3ª atividade — NÃO parar a entrega atual pra refatorar tudo de uma vez.
- **Regra:** o "aprender diferente" NÃO precisa de um motor duplicado — precisa de um MÓDULO de atividade novo
  sobre o mundo+personagem existentes. Quando chegar a hora, nasce como o módulo dele.

## 🧭 ARQUITETURA (a reconciliação): mundo-mapa + atividades-peça
NÃO é contradição — são DUAS CAMADAS:
- **Camada 1 — O MUNDO / MAPA com BAIRROS** (o hub "Ilhas do Saber", só que mais "mundo"): dá a
  sensação de **um universo só** e da **jornada do ano**. Bairros por faixa/turma/tema.
- **Camada 2 — AS ATIVIDADES:** cada **bairro/parada** é uma atividade, e cada uma é **seu próprio
  repo/link** (portal leve). Pode ser focada (55 min) OU uma **mini-aventura rica** (a floresta com
  labirintos). A criança está no mapa, entra num lugar, joga, volta ao mapa.
- **AO LONGO DO ANO = SEQUÊNCIA DIDÁTICA:** os bairros/atividades **abrem na ordem do currículo**
  (bimestre a bimestre); o **save** transforma em jornada contínua do ano letivo.
- É o **EduVerse (visão da outra IA) realizado**, mas de um jeito **leve e que escala**.
- **Decisão de design (do Marcos):** (A) mapa + atividades = recomendado (leve, escala, peça
  independente/descartável) · (B) mundo 100% contínuo = imersivo mas pesado/difícil de escalar.
  **Híbrido ideal:** mapa como espinha (A) + cada atividade pode ser mini-aventura + o próprio
  mapa bonito e vivo (mascote andando nele).
- **DECISÃO (corrigida pelo Marcos):** o EducaVerso é um **MUNDO NOVO E PRÓPRIO**. **NÃO** usamos
  o hub antigo "Ilhas do Saber" (`mundo-das-atividades`). Ficamos **só no mundo vivo novo — o
  EducaVerso**. Ele terá a **própria casa/mundo** (o mapa-mundo com bairros faz parte do EducaVerso,
  é dele, não do hub velho). As atividades-aventura são do EducaVerso, no espaço dele. Projeto
  novo, do zero, sem misturar com o antigo.

## 📦 Dinâmica do EducaVerso: 1 repo por atividade + empacotamento + som
- **Um repositório por atividade** (regra "portal leve" do CLAUDE.md): cada atividade =
  `index.html` + `img/` + `audio/`, publicada no GitHub Pages, com **link próprio**. O hub
  "Ilhas do Saber" é só um **mapa leve** que APONTA os links — não carrega o peso. Assim escala
  (5 ou 500 atividades) sem o build engasgar. Cada atividade é **independente e descartável**.
- **Empacotamento:** TESTE rápido = HTML self-contained (assets em base64, 1 arquivo). PUBLICADA
  = pasta leve (`index.html` + `img/` + `audio/`). Fábrica cria/atualiza o repo por workflow.
- **FALA (narração/diálogo)** = TEXTO → `gerar-audio.yml` (edge-tts) → mp3. (Voz por API, sim.)
- **SFX de ambiente/ação** (vento, trovão, porta, machado, passos, chave) = **Web Audio
  sintetizado** (grátis, offline).
- **SFX realistas** (miado, pássaros, lenhador) = **clipes mp3 CC0**: o chat NÃO baixa, mas um
  **workflow baixa** (a montar: `baixar-sons.yml`, igual gerar-imagens) OU o professor fornece.
  Regra séria: só **CC0 / livre de direitos** (é produto de escola).

## 🎓 ROADMAP CURRICULAR do Marcos (o que a Fábrica precisa saber)
- **ESTE ANO:** disciplinas **normais** do currículo (Português, Matemática, Ciências, etc.). As
  atividades EducaVerso deste ano servem essas disciplinas.
- **PRÓXIMO ANO:** **Computação específica** — objetivos de aprendizagem **POR TURMA**, pelos
  **TRÊS EIXOS da BNCC Computação**: (1) **Pensamento Computacional**, (2) **Mundo Digital**,
  (3) **Cultura Digital**. **Começar por PENSAMENTO COMPUTACIONAL.**
- **Encaixe:** a atividade Jardim/Placas (programar o caminho — sequência, algoritmo, lógica)
  **JÁ é Pensamento Computacional** → alinhada com o início do próximo ano. É um baita ponto de
  partida.
- **Fábrica de Atividades:** organizar por **DISCIPLINA** (este ano) e por **EIXO + TURMA**
  (Computação, próximo ano). Ancorar sempre no currículo real (Blumenau + BNCC Computação;
  ver `ATIVIDADE-COMPUTACAO.md`).

## 🎯 META CRÍTICA do Marcos: EducaVerso cobre TODO o currículo de Computação
> ⏳ **ADIADO a pedido do Marcos — DIALOGAR DEPOIS** (o mapa de cobertura + a questão
> plugado/desplugado). Registrado aqui para retomar. Prioridade agora: construir a 1ª atividade.
- Ano que vem o Marcos ministra o **currículo de Computação**. A **coordenadora** pede
  **atividades DESPLUGADAS** + **sequências didáticas**.
- O Marcos QUER que o **EducaVerso atinja TODOS os objetivos de aprendizagem** (3 eixos × turma)
  como uma **SEQUÊNCIA DIDÁTICA COMPLETA** — **sem** precisar fazer atividades desplugadas soltas
  nem outras sequências à parte. **Tudo alcançado no EducaVerso.**
- **Como provar/entregar:** um **MAPA DE COBERTURA CURRICULAR** — cada objetivo (BNCC Computação
  + currículo de Blumenau) → uma **missão/atividade EducaVerso**, em sequência ao longo do ano.
  Isso É a sequência didática **e** a prova de cobertura para a coordenadora.
- **Honestidade (tensão a alinhar):** EducaVerso é **PLUGADO** (tela); a coordenadora pede
  **DESPLUGADO** (sem computador). EducaVerso entrega os MESMOS objetivos com o mesmo espírito
  (construir/fazer/manipular) e pode **GERAR materiais desplugados imprimíveis** (cartas de
  comando, tabuleiros, trilhas) das mesmas missões. Se "conta" como desplugada é decisão
  pedagógica do Marcos + coordenadora — a gente dá as duas formas.

## 🛡️ Regra de ouro contra ESQUECER
1. **Sincronizar com o GitHub ANTES de agir** (o hook `.claude/hooks/sync-remoto.sh`
   já faz automático no início da sessão).
2. Se o **Marcos disser "isso a gente já fez"**, **ACREDITAR e verificar a fundo**
   (sincronizar + reler os manuais). **"Não achei" ≠ "não existe".** Nunca insistir.
3. **Anotar aqui** toda capacidade, secret ou decisão nova — para a próxima
   sessão (que sou eu, sem memória) já nascer sabendo.
4. **LIÇÃO PAGA CARA (jul/2026):** o ambiente reiniciou e me jogou numa cópia local
   ANTIGA (commit velho). Eu concluí que o `eduverse/` inteiro (fábrica, auditores,
   as 6 poses do Byte, a fogueira, os jogos APROVADOS) tinha se PERDIDO — e fiz o
   Marcos passar por uma caça enorme. **Estava tudo no GitHub o tempo todo.** Dois
   enganos meus: (a) confiei na pasta local sem `git fetch`; (b) a **busca de código
   do GitHub NÃO indexa branch que não é a `main`** — o `eduverse/` vive na branch de
   trabalho, então ela "não achou" e eu acreditei nela. **REGRA:** parece faltando?
   → `git fetch origin <branch>` + `git ls-files <caminho>` + `git log -- <caminho>`
   (NÃO a busca de código, que não vê a branch) + **acreditar no Marcos**. NUNCA
   declarar "perdido" de uma cópia local. E ao salvar: **confirmar o push no GitHub**
   (ex.: ler o arquivo pela API), não confiar no "push OK" local.
5. **TRAVA BLINDADA (jul/2026):** o `sync-remoto.sh` antigo DESISTIA na 1ª falha
   de fetch e imprimia o mesmo `✅ conferido` — parecendo tudo em dia quando NÃO
   estava (foi assim que abri numa cópia 30+ commits velha e "não achei" o
   `eduverse/`). Agora o hook tem **RETRY (3x)** no fetch e, se não conseguir
   confirmar o GitHub, imprime um **aviso ALTO** (`⚠️ NÃO consegui conferir`),
   NUNCA o `✅`. Regra pra mim: se vir esse aviso no início da sessão, rodar
   `git fetch origin <branch>` + `git merge --ff-only` ANTES de agir/declarar
   qualquer coisa "perdida".

## 🎙️ ELENCO DE VOZES — TODAS geradas por API (decisão firme do Marcos, jul/2026)
Todas as falas do mundo são GERADAS por API (edge-tts), embutidas em MP3 (base64). Nada de voz do navegador.
Casting pedido pelo Marcos:
- **NOSSO PERSONAGEM (protagonista, ex.: Byte) = ANTONIO** (masculina, edge-tts pt-BR).
- **NPCs MENINOS = OUTRA voz MASCULINA** (diferente do protagonista).
- **NPCs MENINAS = voz FEMININA.**
- **HONESTIDADE TÉCNICA (edge-tts):** o pt-BR do edge-tts tem POUCAS vozes nativas — masculina = **Antonio**;
  femininas = **Francisca** e **Thalita** (2 opções, ótimo p/ separar meninas). NÃO há uma 2ª masculina
  nativa confiável em pt-BR (a "Donato/male2" FALHOU no passado — lição paga). SOLUÇÃO p/ a 2ª voz masculina:
  (a) **pitch/rate shift no Antonio** (a função `pitch_shift` já existe no `gerar-audio.yml`, só ligar no
  `gerar()`) — grave p/ lobo-do-mar, agudo p/ menino; OU (b) voz **pt-PT masculina** (Duarte) se o sotaque
  de Portugal for aceitável (testar 1 fala antes). Preferir (a) pra manter sotaque BR.
- **Elenco por personagem** (registrar no dados.json de cada atividade): cada NPC declara sua voz (id +
  pitch/rate). O montador/gerador de áudio usa isso. Ex. navio: Byte pirata=Antonio; papagaio=Antonio agudo;
  lobo-do-mar=Antonio grave; NPC menina=Francisca; 2ª menina=Thalita.
- Testar 1 fala de cada voz antes de gerar o lote (nunca confirmar sem ouvir).

## 🧍‍♂️ MOTOR DE PERSONAGEM VIVO — UNIVERSAL (pedido firme do Marcos, jul/2026)
> "Se der pra ter o andar normal e suave, construa esse MOTOR e depois aplique em TODOS os personagens,
> como se estivessem vivos: respiração, movimento normal de pernas/braços, sentar, deitar, etc. E o
> personagem NÃO precisa ser sempre o robô — podemos gerar um NOVO por atividade, SE tivermos o motor pronto."
- **PROVA DE QUE DÁ:** o Byte já anda suave com 2 quadros de perna alternando (byte_frente_anda/_anda2,
  byte_costas_anda/_anda2), + respiração/blink/sway/gesto + sentar/deitar/falar/feliz. Deu certo SEM tremor.
- **AÇÃO:** GENERALIZAR essa animação (hoje amarrada ao `byte`/objeto `POSE`) num SISTEMA reutilizável que
  anima QUALQUER personagem a partir da sua CARTELA de poses (idle=respira+pisca+balança, andar=2 quadros de
  perna onde houver sprite senão só deslizar suave, sentar, deitar, falar, feliz, gesto). Data-driven,
  default-seguro. APLICAR a TODOS (Byte + NPCs — hoje NPC só respira/balança). Assim cada atividade escolhe/
  gera seu próprio mascote (a cartela de poses vem do pipeline de imagem, como já foi feito pro Byte pirata).
- **REGRA (Marcos):** SUAVIDADE acima de tudo. Se a perna alternando ficar dura num personagem, cair pro
  modo só-suave (respira/desliza/gesto) sem perna. Nunca preferir "com perna" se ficar pior.
- **OVO QUE CRESCE → MASCOTE (ideia do Marcos, manter):** um mascote pode NASCER de um ovo que cresce/choca
  e evolui (uma progressão de sprites: ovo→racha→filhote→mascote). É só mais um personagem no sistema, com
  uma cartela que muda por estágio. Lúdico e dá vínculo (o mascote "do aluno").
- **É o "motor pronto" que destrava TUDO:** personagem por atividade, mascote do aluno, o Byte pirata, etc.

## 🎭 Ideias do Marcos para PERSONAGENS VIVOS (incorporar no EducaVerso)
Pedidos do professor para os personagens ficarem "de videogame" — anotar para o
documento-mestre (`EDUCAVERSO.md`, seção Personagens Vivos) e para implementar:
- **Boca mexendo ao falar** + **piscar os olhos** + **respirar** no idle (já planejado).
- **Movimento suave e realista de mãos e pernas** — inclusive AÇÕES como
  *entregar a chave* (braço estende, a chave passa, braço recolhe). Caminho técnico:
  (a) **cartela de poses** gerada por IA (idle, andar, "entregando", feliz) trocada
  como sprite sheet — mais simples, é o que o pipeline já faz; OU (b) **recorte em
  partes** (corpo/braço/mão/pernas) animadas por código com easing — mais suave,
  mais trabalho. Começar por (a).
- **Interagir com o MASCOTE da criança** — o aluno tem seu próprio mascote/avatar
  que o acompanha; o Byte e os NPCs interagem com ele (legal p/ pertencimento).
- **O mascote/Byte SEMPRE fala o NOME do estudante** na narração ("Muito bem, João!").
  Fácil e alto impacto: o aluno informa o nome (login simples por código de turma) e
  o nome entra nas falas/narração (Web Speech interpola o texto). Já existe a ideia
  de `S.nome` nos manuais.
- **Guardar o progresso do estudante (a aventura dura o ANO INTEIRO):** o jogo salva
  onde a criança parou (mundos/áreas abertos, itens, atividades feitas, evidências).
  Duas camadas: **local** (localStorage, funciona offline) + **nuvem** (Firebase, com
  login simples por código de turma + nome) — a criança volta e CONTINUA de onde
  parou, a aventura seguindo o ano letivo (campanha por bimestre/semestre). **O mesmo
  dado salvo alimenta a avaliação descritiva** e o painel do professor (o que a criança
  fez = a evidência). É a "jornada do estudante" da visão do EducaVerso.

## ✅ CONSTRUÍDO — "A Floresta do Byte" (Etapa 1, versão incrível) — 2026-07-15
Primeira atividade do EducaVerso, montada com todos os especialistas e aprovada nos
**Portões 1 e 2** do `EDUCAVERSO-QA.md` (falta o Portão 3, do Marcos).
- **Arquivo:** `_demos/educaverso/floresta/index.html` (HTML único, ~611 KB, base64,
  offline). Builder: `_demos/educaverso/floresta/build_floresta2.py`. Assets (todos IA):
  grama (chão), muro de pedra (paredes), árvore, byte, gato, coelho, passarinho, nimbo,
  jaula, chave, seta de madeira, cabana.
- **Labirinto REAL de pedra:** chão de grama (IA) + muros de pedra (IA) preenchendo a
  maioria das células; corredores sinuosos com becos (M2). Grid 9×7. **Byte sempre
  desenhado por cima dos muros** (regra: muro nunca esconde o Byte). Muros em relevo
  (topo levantado + face frontal + sombra), y-sort linha a linha.
- **História:** Nimbo (nuvem cinzenta resmungona, com raio e trovão) prende 3 amiguinhos;
  no final o Nimbo vira bonzinho e há festa na cabana (chaminé com fumaça).
- **3 missões** guiando o Byte com **setas de madeira no chão** (clicar cicla a direção):
  M1 sequência (serpentina), M2 desvio (becos sem saída), M3 repetição (espiral até o
  centro). Amiguinhos: Gato Pigo → Coelha Nina → Passarinho Tuim.
- **1 alívio:** pegar vaga-lumes (após M1), volta ao mundo sozinho.
- **Som Web Audio:** vento (loop), passo, erro, chave, faísca, miau, pio, trovão, twinkle,
  vitória. **Voz** pt-BR (Nimbo com pitch grave). Destrava no 1º gesto + botão "Som e Voz".
- **Pedagogia (Pensamento Computacional, sem perceber):** a criança CONSTRÓI o algoritmo
  (sequência de setas), erra e depura (seta no muro = tremor + som, sem X vermelho),
  vê consequência no mundo. Gating: só liberta quem chega na jaula.
- **LIÇÃO PAGA (nova):** *screenshot com `--virtual-time-budget` engana* — o tempo virtual
  pode capturar o meio de uma animação/ciclo e parecer que "voltou ao início". Para PROVAR
  a mecânica, **dirigir de forma determinística**: `_qaSolve()` (BFS resolve o labirinto) +
  simular o `prox()` passo a passo e **despejar o resultado no `document.title` com
  `--dump-dom`** (não confiar só na foto). Assim confirmei M1/M2/M3 `reached=true` e a
  cadeia missão→alívio→missão→final `salvos=3`.
- **A-FAZER (próximas etapas):** mais amiguinhos (tartaruga/Lelê, esquilo/Tuca, sapo/Coaxo),
  missões de depuração e loop com a placa "repetir", mais alívios (memória-no-chão, regar
  flores), fechar os 55 min; depois: nome do estudante na narração + salvar progresso.

## 🔊 Voz gerada + controles no celular — "A Floresta do Byte" — 2026-07-15
- **VOZ GERADA (não a do navegador):** as falas fixas são geradas pelo workflow
  `gerar-audio.yml` (edge-tts) em **lote** (`_audio/<id>.mp3`) e **embutidas em
  base64** no HTML, tocadas por `<audio>`. A `speechSynthesis` do navegador vira só
  **reserva**. Vozes: narrador/Byte/amiguinhos = **female (Francisca)**; Nimbo =
  **male (Antonio)**. **LIÇÃO PAGA:** a voz `male2`/**Donato** FALHOU no edge-tts
  ("edge-tts falhou") — saiu do catálogo; usar `male` (Antonio) ou `female`
  (Francisca), que funcionam. Sempre restringir o embed à LISTA de ids da atividade
  (o `_audio/` do repo tem centenas de mp3 de outras atividades — embutir tudo incha).
- **D-PAD no celular (pedido do Marcos):** em telas de toque aparece um teclado de
  setas (▲◀✖▶▼); no PC ele **some** (detecção `pointer:coarse`/`ontouchstart`;
  `?dpad=1` força p/ teste). Dinâmica no toque: **tocar numa pedra** (anel de
  destaque) → **escolher a direção** no D-pad → **VAI**; ✖ remove. No PC continua o
  clique-que-cicla a seta.
- **LIÇÃO PAGA (screenshot):** o Chromium headless tem **largura mínima ~500px** —
  foto com `--window-size=400` corta a direita e PARECE overflow. Diagnosticar com
  `document.body.scrollWidth` vs `innerWidth` (deu 500==500 = sem estouro), não confiar
  no corte da foto. Fotografar em ≥500px de largura p/ prévia mobile fiel.
- **Publicação:** repo próprio **`floresta-do-byte`** → `atualizar.yml`
  (`repo_name=floresta-do-byte`, `source_dir=_novo`). No ar em
  **https://vidalprof.github.io/floresta-do-byte/**.

## 🎭 A-FAZER: voz PRÓPRIA por personagem (adiado pelo Marcos — 2026-07-15)
Decisão do Marcos: por ora fica com 2 vozes (Francisca = narrador/amiguinhos;
Antonio = Nimbo). Voz por personagem fica pra depois. Dois caminhos já mapeados:
- **edge-tts (grátis):** poucas vozes nativas pt-BR (Antonio/Francisca) → multiplicar
  por **pitch/velocidade** (função `pitch_shift` já existe no `gerar-audio.yml`, só
  falta ligar no `gerar()`): Nimbo grave, bichinhos agudos.
- **Gemini TTS (pago, chave configurada):** MUITAS vozes atuadas (Puck, Kore, Charon,
  Fenrir, Aoede...) + direção de atuação ("leia como vilão/gatinho"). `modelo=gemini`
  no workflow (testar 1 fala antes — nunca confirmar sem ouvir).
- **Elenco proposto:** Byte/Narrador = clara/acolhedora; Nimbo = grave/resmungona;
  Gato Pigo = agudo/brincalhão; Coelha Nina = doce; Passarinho Tuim = bem agudo/rápido.

## ⭐ FILOSOFIA DO EDUVERSE (LEI — trazida pelo Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-FILOSOFIA.md`** (é o **Portão 0** do QA). Resumo do que NÃO
esquecer NUNCA:
- **Não é jogo de pergunta/resposta. Não é prova disfarçada.** Nada de "acerte a conta →
  abre o baú/porta/ganha moeda". Esse modelo já existe; o EduVerse é OUTRA coisa.
- O aluno aprende porque **O MUNDO PRECISA** daquele conhecimento. **Problema primeiro**;
  o **conteúdo/pergunta NUNCA aparece primeiro**; o **conceito é nomeado por ÚLTIMO**.
- Arco fixo: **História → Exploração → Problema → Experimentação → Descoberta → Conceito →
  Aplicação → Reflexão** (nunca invertido).
- Conhecimento = **ferramenta** (resolve), nunca **obstáculo** (bloqueia).
- **Byte pergunta** ("o que você percebe?", "tem jeito mais rápido?", "achou um padrão?",
  "como organizar isso?"), nunca "qual é a resposta?".
- Eu (IA) transformo conteúdo escolar em **experiência** (história/construção/investigação),
  **nunca** em lista de perguntas. Exemplos do Marcos (multiplicação): plantar 6 canteiros ×
  4 árvores; caixas de 8 rodas × 7 caixas; galinheiros de 6 galinhas — o aluno organiza
  grupos, conta, vê padrão, e a multiplicação **nasce** disso.
- No fim o aluno diz "hoje **ajudei/construí/salvei/descobri**", e só depois "…aprendi X".

**Aplicar já na "Floresta do Byte":** o Byte deve **provocar** (perguntas), a mecânica de
guiar/empurrar é a **ferramenta** pra salvar o amigo (problema do mundo), e fechar com a
**descoberta + nome do conceito** (algoritmo/sequência/depuração) + **reflexão**, de leve.

## 🤖 FILOSOFIA DA COMPUTAÇÃO + MAPA DA SEQUÊNCIA DIDÁTICA (Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-COMPUTACAO.md`** (Parte 2 da filosofia). É o **mapa** que a
coordenação pede pro ano que vem. Progressão dos conceitos, cada um nascendo de um PROBLEMA
do mundo (nunca apresentado primeiro):
1. **Sequência/Algoritmo** — desenhar o caminho do robô; ele executa exatamente; erra na tela.
2. **Condição (SE)** — rio em que o robô cai → "SE achar rio → vira".
3. **Repetição (loop)** — 10 entregas iguais → "dá pra mandar repetir sozinho?".
4. **Função** — vários robôs iguais → "uma instrução que qualquer robô use".
5. **Depuração** — o robô executa o erro de verdade; observa, acha, corrige, testa.
Mundo-exemplo: **Vale das Máquinas** (robôs, trem, fábrica, esteiras, rio, ponte, cidade) —
cenário ideal pro ano da Computação, com o mesmo Byte.
**JÁ FAZEMOS o item 1** na "Floresta do Byte" (põe setas = desenha caminho; VAI; Byte erra no
muro = depuração sem X). FALTA: Byte perguntando + condição + repetição explícita + função.
A Floresta do Byte é a **Missão 1** dessa jornada (ponte pro currículo de Computação).

## 🏗️ PIPELINE DE CONSTRUÇÃO + BIBLIOTECA LEGO (Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-PIPELINE.md`** (Parte 3). Regra-mãe: **não criamos atividades,
criamos MUNDOS VIVOS**; a atividade nasce dentro. Pipeline de 10 etapas (mundo → vida →
personagens → rotina → objetos inteligentes → PROBLEMA → exploração → necessidade → conceito
natural → reflexão). **Mapas por TILES** (32/48/64) tipo LEGO; **biblioteca reutilizável** de
tiles/objetos/personagens; **folha de animações padrão** por personagem (parado, andar ↑↓←→,
falar, feliz, pensando, comemorando, triste, esperando). Tech: Canvas 2D, sprite sheets, tiles,
Firebase; compat. Win7/Chrome antigo, 1024×768. **Objetivo:** nova atividade = MONTADA com peças
reutilizáveis, não do zero (é isso que deixa a criação FÁCIL). Futuro: editor arrastar-e-soltar.
FALTA construir o KIT base (estilo travado → tiles + Byte animado + objetos) e passar a montar as
atividades a partir dele.

## 💰 REGRA DE OPERAÇÃO — modelo adequado por tarefa (economia, jul/2026)
Ao convocar subagentes/equipes: tarefa MECÂNICA (builds, greps, screenshots,
conferir laudo) = **Haiku**; codificação padrão (portão, dados.json) = **Sonnet**;
arquitetura/síntese/auditoria adversarial = **Opus/Fable**. Regular também o
esforço de raciocínio por agente (baixo no mecânico, alto só em verificação/chefia).
O modelo da SESSÃO principal só o Marcos troca (/model).

## 🌐 EDUMUNDO (tela do aluno) + PAINEL DO PROFESSOR — decisões travadas (Marcos, 2026-07-17)
DEPOIS que o teste de Firebase passou (login anônimo + gravar + ler no RTDB do projeto
`educaverso-73b1a`, run 29548937470 SUCCESS), o Marcos definiu como aluno e professor entram:

- **DOIS SITES/REPOS SEPARADOS.** (1) **EduMundo** (aluno, público e bonito, é "a tela do
  EducaMundo/EducaVerso inicial"); (2) **Painel do professor** (repo próprio, com **SENHA**,
  **invisível para os alunos**). Nunca juntar os dois no mesmo endereço.
- **Professor cadastra TURMAS + ALUNOS no painel** (só nome + avatar emoji; sem digitar senha
  para a criança). O painel também **mostra o progresso** (lê `/turmas/<turma>/alunos` = a função
  `listarTurma` já existente).
- **Login do aluno = ZERO digitação.** Professor abre o EduMundo nos PCs do lab já apontado pra
  turma pelo **link** (`educamundo/?t=<turmaId>`). A criança vê os cards **nome+avatar** da turma
  dela e **TOCA no seu**. Por baixo: login **anônimo silencioso** no Firebase; progresso salva em
  `/turmas/<turmaId>/alunos/<alunoId>`. Senha visual de 2 figurinhas fica OPCIONAL (ligar depois só
  se precisar; começar sem, pra não travar o piloto).
- **Acesso do professor = senha** (piloto: gate no cliente + site separado que a criança não conhece).
  Honestidade: é segurança de piloto (dado não sensível: 1º nome + progresso). Nível 2 (cada aluno só
  mexe no próprio; professor dono) fica pra produção.
- **Modelo de dados:** `/turmas/<turmaId>` = { nome, alunos:{ <alunoId>:{ nome, avatar, dados, atualizado_em } } }.
- **Arquivos no repo-fábrica:** `_educamundo/index.html` (aluno) e `_painel-prof/index.html` (professor).
  Publicar cada um no seu repo via Fábrica/atualizar. Regras do RTDB atualizadas em
  `eduverse/lib/REGRAS-FIREBASE.txt` (agora cobrem o metadado da turma + listar turmas no painel).

## 🗺️ EDUMUNDO = MUNDOS VIVOS COM PARADAS, CATÁLOGO DINÂMICO (Marcos, 2026-07-17)
Pergunta do Marcos: "as atividades no EduMundo são injetadas?" -> estavam FIXAS no
código (array JOGOS). Decisão: **NÃO ficam no código**. O EduMundo lê o CATÁLOGO do
Firebase (biblioteca que cresce; a Fábrica/painel adiciona, a tela mostra sozinha).
E o aluno vê **MUNDOS VIVOS COM PARADAS** (não lista plana): toca o nome -> vê os
MUNDOS (cards) -> entra num mundo -> MAPA temático com as PARADAS (medalhão do
mascote + trilha), toca a parada -> abre o jogo (link próprio; portal leve).
- **Modelo de dados (Firebase):** `/catalogo/mundos/<mundoId>` =
  { nome, emoji, tema, cor, ordem, paradas:{ <pid>:{ titulo, mascote, link, ordem, x, y, soon } } }
- **Progresso:** `/turmas/<t>/alunos/<a>/dados/progresso/<mundoId>/paradas` (paradas visitadas).
- **Semear catálogo:** workflow `semear-catalogo.yml` grava o mundo Ilha do Tesouro + 7 paradas.
  EduMundo tem fallback amigável + cache offline se o catálogo estiver vazio/offline.

## ⚠️ REINCIDÊNCIA: cópia local voltou pro base velho (2026-07-17)
Ao commitar o EduMundo dinâmico, o git local estava em 3dc86eb (base VELHO, "behind 847").
Cura aplicada: salvar os arquivos bons em /tmp, `git reset --hard origin/<branch>`, reaplicar
por cima, commitar. SEMPRE conferir `git status -sb` (procurar "behind N") ANTES de commitar.

## 🥚 EDUCAVERSO (nome correto) + ENTRADA COM OVO→MASCOTE (Marcos, 2026-07-17)
Marcos corrigiu: o nome é **EducaVerso** (eu tinha escorregado pra "EduMundo"). E a
entrada tem que ser a ideia inicial: aluno toca o nome -> (1ª vez) um **OVO choca** e
ele **escolhe o MASCOTE** dele -> **cai DIRETO no mundo vivo** (mapa de paradas), sem
menuzinho. O **mascote é o personagem** que anda no mapa (o token) e **cresce o ano
todo** (guarda quantas paradas fez; nivel=1+floor(paradas/3)). "Outros mundos" fica num
botão de canto. Pasta renomeada `_educamundo`->`_educaverso`; repo de destino = `educaverso`
(link `https://vidalprof.github.io/educaverso/`). Painel atualizado pra gerar esse link.
- **Mascote (dados):** `/turmas/<t>/alunos/<a>/dados/mascote` = { tipo, nivel, paradas, nascido_em }.
- **HONESTO:** mascote é EMOJI por enquanto (🐣🐉🦊...); a versão desenhada que cresce de
  verdade (arte por estágio) vem depois, via asset studio. Marcos é o professor E o admin
  (um usuário só). Enquanto a fábrica não é perfeita, a "equipe que conserta" sou eu (Claude).

## 🐾 VERSO vira FAMÍLIA (vários tipos, 1 esqueleto só) — (Marcos, 2026-07-17)
Marcos: "se é fácil assim, não seria melhor vários pra escolher?" (a dúvida da dificuldade
era porque achou que o mascote ocuparia o lugar do robô/animação pesada). Como o robô FICA
e o Verso é leve (vetor, flutua/pula), dá pra ter VÁRIOS — regra: **família que COMPARTILHA
o mesmo corpo/olhos/animação**; muda só a "cabeça" (orelha/chifre/crista/bico) + a cor. 6
tipos provados em SVG: gatinho, coelho, ursinho, dino, passarinho, chifrudo. A criança
escolhe TIPO + COR; + estágios (fofo→descolado, atende 1º ao 9º) + acessórios por mundo.
Bichos TOTALMENTE diferentes (polvo×dragão, animações próprias) continuam PROIBIDOS (pesado).
- **Byte NÃO some:** vira guia/morador dos mundos (dá as missões). Mascote = personagem do ALUNO.
- **Modelo de operação (Marcos):** "comando tudo do painel, mas a EQUIPE (Claude) está sempre
  aqui — é onde produzimos e melhoramos tudo". Painel = controle; sessão = oficina.
- **Verso é SVG paramétrico** (recolor=1 valor; roda em qualquer navegador, IE9+/Chrome/Firefox,
  sem lib, offline). Vira ator do motor de personagem vivo. Gerador guardado em /tmp (versos.html).

## 🚨🚨 CURA DEFINITIVA DO "BASE VELHO" (perda recorrente de tempo/créditos) — 2026-07-17
PROBLEMA (aconteceu de novo, Marcos MUITO incomodado, com razão): o container volta com a
branch/working-tree numa BASE VELHA (3dc86eb "Vila do Miau"), e o remote-tracking `origin/...`
fica DESATUALIZADO apontando pra ela. Se eu rodo `git reset --hard origin/<branch>` confiando
nesse ref velho, APAGO a eduverse/ + trunco a MEMORIA. **Nada se perde no GitHub** (fonte da
verdade), mas eu gasto tempo/créditos recuperando SEMPRE. 
REGRAS DE OURO (obrigatórias, nunca furar):
1. **NUNCA** `git reset --hard origin/<branch>` sem antes `git fetch --force origin <branch>`.
2. **SEMPRE** conferir o tip REAL do GitHub por API (mcp github list_branches / get_file_contents)
   ANTES de qualquer reset. Se o `origin/...` local ≠ tip da API, ele está velho: fetch --force.
3. Ao restaurar: `git fetch --force origin <branch>` -> conferir `git ls-files eduverse | wc -l`
   (tem que dar ~72) e `wc -l MEMORIA` (~740+) -> só então seguir.
4. O hook `.claude/hooks/sync-remoto.sh` foi endurecido pra AUTO-restaurar no início da sessão
   (fetch --force + reset --hard pro tip real do GitHub) — assim isso vira automático, não manual.

## 🚀 PUBLICADO PRA TESTE (Marcos: "faça tudo, deixe pronto") — 2026-07-17
Tudo no ar via Fábrica (dispatch com ref=claude branch, source_dir por site):
- educaverso  -> https://vidalprof.github.io/educaverso/  (aluno; Verso integrado)
- painel-prof -> https://vidalprof.github.io/painel-prof/  (senha vidal2026; cria turmas/alunos + mundos/paradas)
- navio-pirata-> https://vidalprof.github.io/navio-pirata/  (atividade de numeros; 1a parada da Ilha)
Regras do Firebase republicadas pelo Marcos (agora cobrem /catalogo). semear-catalogo.yml (na main)
rodou OK (run 29576419440): semeou /catalogo/mundos/ilha-pirata (fogueira=jogavel, resto "em breve")
+ criou turma-mestra /turmas/teste (Ana/Bento/Clara). LINK DE TESTE: educaverso/?t=teste.
FASE SEGUINTE = LAPIDAR (Marcos: "depois verificamos e lapidamos"): estagios do mascote (fofo->descolado),
animacao viva do Verso (respira/pisca/pula), a Ilha completa (7 paradas com jogo/historia/vozes),
ajustar coordenadas das paradas na arte da ilha.

## 🌎🌎 VISÃO-MESTRA DEFINITIVA — EDUCAVERSO / EDUVERSE PROFESSOR AI (Marcos, 2026-07-17)
O "REAL MOTIVO" do projeto (Marcos revelou colando 2 prompts-mestres inteiros):
**PROBLEMA REAL:** o **Currículo de Computação** está entrando nas escolas. O professor de
Informática Pedagógica vira **Professor de Computação** com currículo próprio -> tem que produzir
planejamento, sequência didática, plano de aula, atividades plugadas E desplugadas, avaliação,
relatórios e documentação pra coordenação. Carga de trabalho INSUSTENTÁVEL. **Educaverso nasce pra
resolver isso.**
**MISSÃO:** transformar AUTOMATICAMENTE cada objetivo OFICIAL do currículo numa experiência completa
de aprendizagem, e gerar SOZINHO toda a documentação pedagógica (nos modelos oficiais da Secretaria).
O professor gasta tempo com os ALUNOS, não com papel.
**DUAS VISÕES (regra de ouro):** o PROFESSOR vê planejamento/objetivos/conceitos/avaliação/relatórios;
o ALUNO vê uma AVENTURA (cidade, missão, personagens, mistérios). Nunca documento escolar pro aluno.
**CURRÍCULO INVISÍVEL (princípio absoluto):** o aluno NUNCA sente que estuda. Nada de "Atividade 3 /
Exercício 5 / prova / questionário". Ele explora, constrói, investiga, resolve problemas do mundo.
O conceito é vivido, nunca anunciado. Ex.: prof="algoritmos simples"; aluno="o robô perdeu a rota e
precisa entregar remédios antes do pôr do sol". Aprende sem perceber.
**O MUNDO É O PROFESSOR:** o ambiente ensina; moradores perguntam; problemas surgem naturais; solução
vem da exploração. O professor vira MEDIADOR.
**UM ÚNICO MUNDO PERSISTENTE (não coleção de jogos):** o aluno volta SEMPRE ao mesmo lugar; tudo salvo;
NPCs lembram; construções permanecem. **A cidade cresce com o aluno** — cada objetivo aprendido muda o
mundo dele (casas, árvores, robôs, bairros); cada aluno tem uma cidade ÚNICA. **Jornada de 9 anos**
(1º ao 9º ano) no mesmo mundo, que envelhece junto.
**MUNDO VIVO:** NPCs andam/conversam/dormem/trabalham; animais com comportamento; clima, dia/noite,
chuva, vento, partículas, som. Meta máxima do projeto: o aluno AMAR VOLTAR -> "Professor, hoje tem
Educaverso?".
**AVALIAÇÃO INVISÍVEL:** o jogo OBSERVA (tempo, tentativas, persistência, estratégias, decisões, pedidos
de ajuda, erros/acertos, autonomia) -> gera avaliação diagnóstica+formativa + evidências, SEM prova.
**SEQUÊNCIA = 55min = 1 objetivo = 1 aula:** 5 intro narrativa / 35 missão / 10 desafio final / 5 síntese+
registro+avaliação. Nunca aventura longa.
**MECÂNICAS REUTILIZÁVEIS (não criar do zero):** programar robôs, construir pontes, automatizar fazenda,
organizar biblioteca, logística, cidade inteligente, semáforos, lab de dados, reciclagem... cada mecânica
atende DEZENAS de objetivos só trocando contexto/narrativa. Regiões: cidade, lab, oficina, biblioteca,
museu, porto, fazenda, floresta, mina, usina...
**MOTOR PEDAGÓGICO (por objetivo -> "Pacote Pedagógico" automático):** objetivo oficial + conceitos +
conteúdos + conhecimentos prévios + sequência + plano de aula + planejamento + metodologia + recursos +
avaliação + rubricas + missão digital + versão DESPLUGADA (mesmos objetivos, p/ sem internet) + relatório
individual + relatório da turma + diário do professor + registro coordenação + recuperação.
**BRAIN/ASSET STUDIO:** cérebro decide região/mecânica/missão/NPCs; biblioteca permanente que só cresce,
nunca duplica; personagens modulares (paper-doll) mesmo estilo; map builder automático.
**TECH:** HTML5/CSS/JS, Firebase, IA p/ narrativa+diálogo+DOCUMENTAÇÃO, modular, Win7/Chrome/Firefox,
1024x768, leve, online com export offline. (Obs: prompts citam Phaser; nós decidimos Canvas 2D por peso.)

### HONESTIDADE — onde estamos vs. essa visão (Claude, 2026-07-17)
O que existe hoje = INFRAESTRUTURA (login por toque, ovo/mascote Verso, mapa de mundos/paradas, Firebase
salvando progresso, painel do professor) + UMA atividade de MATEMÁTICA (números até 30, pirata) que é
"mais do mesmo" (exercício gamificado). A ALMA da visão (currículo INVISÍVEL de COMPUTAÇÃO, mundo-professor,
cidade persistente que cresce 9 anos, avaliação invisível -> documentação automática) ainda está À FRENTE.
As pernas difíceis JÁ PROVADAS: IA gera conteúdo (Gemini) e dados (Firebase) — são exatamente os motores
que essa visão precisa p/ auto-documentação e avaliação invisível. Caminho realista = 1 FATIA VERTICAL
honesta num objetivo de COMPUTAÇÃO (ex.: algoritmos/sequência) que prove a filosofia ponta a ponta:
problema do mundo -> aluno resolve vivendo -> avaliação invisível -> Pacote Pedagógico gerado pro professor.
NÃO prometer a plataforma inteira de uma vez (é roadmap de anos); provar a filosofia numa fatia real primeiro.

### DECISÃO DE CENA (Marcos, 2026-07-17): paradas numa ILHA no meio do oceano; a ÚLTIMA fase é um NAVIO
(como o que ficou bonito). O convés repetido/câmera 3/4 dava "paredes/imagens coladas" -> ilha resolve.

## 🎨🌱 SPEC DEFINITIVA DO MUNDO VIVO — "EDUCAVERSO EXPERIENCE ENGINE" (Marcos, 2026-07-17)
Marcos quer o MUNDO VIVO (é o diferencial da ideia) e perguntou "tem como ser mais fácil e bonito
igual?". Colou a spec-mestra do mundo vivo. RESPOSTA: SIM — a própria spec é a receita. Princípios:
- **MÉTRICA DE SUCESSO:** criança perguntar "Professor, hoje tem Educaverso?". Beleza NÃO vem de
  gráfico caro — vem de **CONSISTÊNCIA** (tudo do mesmo "estúdio") + vida + som + rotina + eventos.
- **REGRA DE OURO ANTI-BUG (bate com nossos erros):**
  (a) **NUNCA gerar mapa/cena inteira com IA** (gera inconsistência) — foi o erro do tile "conves"
      cheio de viga (parede repetida / "imagens coladas").
  (b) IA gera **só RECURSOS individuais** (árvore, casa, robô, item), salvos numa **BIBLIOTECA
      PERMANENTE** que só cresce e nunca duplica. Antes de criar: "já existe? reutiliza".
  (c) O **BUILDER** monta a cena AUTOMÁTICO a partir da biblioteca (chão simples + assets colocados
      por cima). Chão simples/seamless = tiling invisível; a riqueza vem dos ASSETS variados colocados,
      não de um tile detalhado repetido.
- **VIDA PROCEDURAL (não animar mil coisas à mão):** REGRAS simples geram milhares de comportamentos —
  árvore balança, água mexe, fumaça sobe, borboleta voa, pássaro muda direção, cão passeia, gato dorme
  ao sol, robô trabalha, morador tem rotina. + **EVENTOS ALEATÓRIOS** (carteiro, balão, chuva, feira,
  navio atracando) só pra surpreender.
- **MUNDO COM MEMÓRIA + CIDADE EVOLUTIVA:** plantou árvore fica; ponte fica; morador lembra. Cada aluno
  começa com um terreno e a cidade cresce a cada objetivo — cada aluno tem cidade ÚNICA. Jogo não acaba;
  cada aula = novo capítulo (o que mudou? quem chegou? quem precisa de ajuda?).
- **MÓDULOS:** Asset Factory (só recursos reutilizáveis, ex. 200 árvores), Diretor de Arte IA (decide
  paleta/luz/hora/clima/qtd NPCs/som — mantém coerência), Builder automático, Educaverso Director AI
  (pergunta sempre "como deixar mais vivo?" respeitando performance).
- **PERFORMANCE:** Win7/Chrome/Firefox, 1024x768, pouca memória, animações leves, REUSO máximo.
- **RECONCILIAÇÃO com o que o Claude tinha sugerido:** eu tinha proposto "imagem única coesa por cena";
  a spec do Marcos é MELHOR pro objetivo vivo/evolutivo/consistente -> **chão simples + biblioteca de
  assets colocados + vida procedural**. O "flat ground" que comecei encaixa nisso (chão simples). Fim
  do tile busy e do mapa-IA. Obs: spec cita Phaser; princípios valem em Canvas 2D (nosso, mais leve).
- **ESCOPO HONESTO:** isso é um SISTEMA (biblioteca + builder + vida procedural + memória + cidade),
  build grande — a FUNDAÇÃO certa do mundo vivo, não remendo. Caminho: 1 CENA-PROVA (chão simples +
  poucos assets coerentes + vida procedural: pássaro/fumaça/personagem respirando) SEM bug, e crescer.

## 🏛️ ARQUITETURA TÉCNICA (a "outra IA" mandou) — avaliação honesta (2026-07-17)
Marcos colou um doc GRANDE de arquitetura feito por outra IA. REGRA-MÃE dele: **a IA gera DADOS
estruturados; o Educaverso EXECUTA código/mapas/mecânicas/componentes JÁ TESTADOS.** IA nunca escreve
um jogo inteiro do zero por objetivo. STACK proposto: React+TS (painel), Node+TS (Orquestrador),
IA c/ saída estruturada (JSON Schema/Zod + validação/rejeição), Educaverso Builder (templates+regras+
mecânicas), **Phaser** (motor), **Tiled** (mapas JSON), Firebase (auth/db/storage/hosting), Vitest+
Playwright+ESLint+CI (testes). Mecânicas reutilizáveis CONFIGURÁVEIS (ex. "ordenar_comandos" vira robô/
carteiro/receita só trocando contexto). Biblioteca de assets c/ metadados + Guia de Arte. Vida procedural
por comportamento. Eventos aleatórios. Som em camadas. Avaliação invisível -> docs automáticos. Modos
completo/econômico/ULTRALEVE (Canvas quando preciso). Offline/cache, missão gerada ANTES da aula (não
chamar IA durante). Validador técnico + pedagógico antes de publicar. Prévia do professor. 9 etapas de
desenvolvimento. Regra de ouro: IA sugere -> validador confere -> builder monta -> testes -> professor
revisa -> publica.

AVALIAÇÃO (Claude, honesto):
- **CONVERGE com tudo que a gente decidiu** (dados-não-código, reuso, biblioteca, vida procedural,
  consistência de arte, avaliação invisível, não-IA-na-aula, offline, docs automáticos). As visões batem
  = ótimo sinal.
- **A DIFERENÇA REAL é o STACK:** React+TS+Phaser+Tiled+Node+Vite+CI = **produto de software profissional**
  (meses, equipe, backend, build, hospedagem). É o jeito certo PRA UM PRODUTO que escala p/ muitas escolas
  e 9 anos. Mas é MUITO mais pesado que o nosso atual (HTML único no GitHub Pages, sem build, Canvas leve).
- **Tensão técnica:** Phaser+TS+build briga um pouco com "HTML único offline p/ Win7 sem instalar" (nosso).
  Phaser roda no navegador, mas some a simplicidade do arquivo único.
- **RECOMENDAÇÃO:** usar esse doc como **MAPA DO DESTINO**; adotar os PRINCÍPIOS AGORA no jeito leve (que
  já faz muito disso); migrar pro stack pesado só quando/se virar produto de verdade (com tempo/equipe).
  Um professor sozinho não toca React+TS+Phaser+Node+CI E dá aula — e o Marcos quer MENOS trabalho.
- O protótipo atual (praia viva + missão "ordenar passos" + narração + som, Canvas ultraleve) já aplica
  boa parte do doc: mecânica reutilizável configurável, vida procedural, avaliação embutível, offline.

## 🏗️ PLANO A INICIADO (stack profissional, À PARTE) — Etapa 1 no ar (2026-07-17)
Marcos escolheu o PLANO A (stack pesado do doc de arquitetura). Pediu: "não delete nada, faça
à parte, deixe o modelo leve como está pra acessar quando quiser". Feito:
- **educaverso-app/** (no repo, branch de trabalho): projeto **Phaser 3.80 + TypeScript + Vite**.
  src/main.ts = Etapa 1 (Núcleo técnico): personagem anda no mapa, câmera segue, colisão com água,
  passarinho de vida. tsconfig strict=false (afrouxado pro 1º build), vite base './' + target es2017
  (compat. navegador antigo atualizado).
- **.github/workflows/app-build.yml** (na main = dispatchável): npm install + vite build -> publica o
  dist num repo SEPARADO **educaverso-app** via PAGES_TOKEN + liga Pages. NÃO toca no modelo leve.
- **BUILD PASSOU DE PRIMEIRA** (run 29581472602 SUCCESS): prova que o stack profissional inteiro
  (npm/Vite/Phaser/deploy) é construível e publicável DAQUI, de graça, via GitHub Actions.
- Link do app: **https://vidalprof.github.io/educaverso-app/** (Pages leva 1-2 min na 1ª vez).
- HONESTO: NÃO consegui screenshotar o app no ar (o Chromium do sandbox não alcança sites externos
  pelo proxy — ERR_TUNNEL). Build+deploy confirmados pelo status do workflow; a validação visual é o
  Marcos abrir no navegador dele.
- Modelo leve INTACTO no ar: educaverso, painel-prof, navio-pirata, ilha-dos-passos, atividades.
- PRÓXIMAS ETAPAS (ordem do doc): Etapa 2 mecânica "ordenar comandos" (com avaliação) -> Etapa 3 mundo
  vivo (NPCs/rotinas/clima) -> Etapa 4 painel React -> Etapa 5 IA estruturada (JSON Schema/Zod) ->
  Etapa 6 Builder -> Etapa 7 avaliação -> Etapa 8 documentação -> Etapa 9 expansão.

## 📌 PENDÊNCIA (Marcos, 2026-07-17): DOCUMENTO ÚNICO com TODA a sequência
Quando o Marcos DER O SINAL (não antes): reformular TUDO (as visões-mestras, a arquitetura, as
decisões, as etapas) num **documento só**, organizado, com **toda a sequência** de desenvolvimento
do Educaverso. É consolidação — esperar o "agora pode" do Marcos.

## 🧩 ETAPA 2 iniciada — mecânica "ordenar comandos" no app Phaser (2026-07-17)
Marcos deu "pode fazer". Construindo no educaverso-app (Plano A): a mecânica REUTILIZÁVEL
"ordenar comandos" (algoritmo) numa cena única bonita (praia noturna). Criança monta os passos ->
Verso anda de célula em célula até o baú, desviando das poças -> conceito "ALGORITMO" no fim ->
avaliação invisível começa a registrar (tentativas/tempo/acerto em localStorage; Firebase depois).
Mira Chrome 109 (moderno). Config da mecânica separada (reutilizável p/ virar missão no mundo OU
atividade avulsa premium).

---

## [2026-07-17] Configuração REAL dos PCs da escola (alvo de hardware confirmado)

O Marcos enviou a tela de sistema de um PC da escola. **É este o hardware que
tem que rodar liso** (não é hipótese, é o alvo real):

- **CPU:** AMD FX-4300 Quad-Core 3,8 GHz (2012, arquitetura Bulldozer/Piledriver — fraco por núcleo)
- **RAM:** **3583 MB (~3,5 GB)** ← o gargalo mais sério
- **SO:** Windows 7 64 Bits
- **Navegador:** Chrome 109 (o último que roda no Win7)

### O que isso confirma / exige (regras de projeto)
- **RAM baixa (3,5 GB) é o limite crítico.** Win7 + Chrome já comem boa parte.
  → Texturas PEQUENAS e desenhadas 1x só (canvas via `textures.createCanvas`),
    nada de spritesheets gigantes, nada de segurar muitos assets na memória.
  → Uma cena por vez; liberar o que não está em uso.
- **CPU fraca por núcleo** → manter `fps.target: 30`, `antialias:false`,
  `powerPreference:'low-power'`, `roundPixels:true`, poucas tweens simultâneas.
- **Scale FIT 1024×768** continua certo (resolução baixa = menos pixels a
  desenhar = menos GPU/RAM).
- Chrome 109 é moderno (ES2022/WebGL2) → pode usar ferramenta moderna SEM
  gambiarra; o problema nunca foi o padrão da linguagem, é o PESO em RAM/CPU.
- **Teste de aceitação:** toda etapa nova tem que ser testada NO PC do Chrome
  109 (o do Marcos) antes de considerar pronta.

### [2026-07-17] Navegadores REAIS da escola (alvo de build definitivo)
O Marcos confirmou os dois navegadores usados nos PCs da escola:
- **Chrome 109.0.5414.120** (o último do Win7)
- **Firefox 106.0.5 64 bits** ← ATENÇÃO: é MAIS ANTIGO que o 115.

→ No `educaverso-app/vite.config.ts` o alvo do build tem que ser
  **`target: ['chrome109', 'firefox106']`** (NÃO firefox115 — o 106 é anterior;
  usar 115 faz o Vite gerar sintaxe que o Firefox 106 não entende).
Ambos suportam ES2022, então o `tsconfig target ES2022` continua ok.
Teste de aceitação de toda etapa: rodar nesses DOIS navegadores da escola.

---

## [2026-07-17] DUAS REGRAS DE OURO reafirmadas pelo Marcos (Etapa 2 → correção de rumo)

O Marcos testou a Etapa 2 ("Ajude o Louro"): **rodou**, mas ele lembrou de dois
pontos que são LEI do projeto e eu não podia ter deixado passar:

### REGRA 1 — VOZ: SEMPRE por API (voz "Antonio"), NUNCA pelo navegador
- **PROIBIDO** usar `Web Speech API` (`speechSynthesis` / `SpeechSynthesisUtterance`)
  do navegador. Nada de `fala()` que usa o sintetizador do Chrome.
- A voz TEM que ser **gerada por API** (Edge TTS, voz **pt-BR "Antonio"** =
  `pt-BR-AntonioNeural`) por **WORKFLOW do GitHub** (`gerar-audio.yml`), que
  produz **arquivos de áudio** (mp3/ogg). O app só **toca o arquivo pronto**.
- Motivo: a voz do navegador é robótica, muda de PC pra PC, às vezes nem existe;
  a voz por API é sempre a mesma, natural e coerente com o EduVerso. Todo asset
  que a criança ouve é gerado (mesmo princípio de "todo asset visto é IA").
- **Aplicar em TUDO** (app Plano A, atividades, hub). Refatorar a Etapa 2 pra
  tirar o Web Speech e tocar os áudios do Antonio.

### REGRA 2 — O norte é o MUNDO VIVO EXPLORÁVEL 2D (ensinar diferente)
- A Etapa 2 é uma boa MECÂNICA (ordenar comandos), mas ela virou uma "tela de
  puzzle" isolada. **Não é isso** o diferencial. O diferencial é o **mundo vivo
  2D explorável**: a criança ANDA pelo mundo, encontra os problemas no contexto,
  e a mecânica aparece DENTRO do mundo (não como uma telinha à parte).
- A mecânica continua sendo peça reutilizável — mas o invólucro é o mundo vivo.
- Próximo passo real = **Etapa 3**: mundo explorável (andar livre, NPCs, o
  problema no lugar), com a mecânica de algoritmo acontecendo lá dentro.

---

## [2026-07-17] NASCEU O `EDUCAVERSO-UNIFICADO.md` — o documento ÚNICO (fonte da verdade)

O Marcos pediu: "reúna-se com os profissionais e redija um documento único do
educaverso com tudo de novo, agora podemos utilizar tecnologia moderna, una o
melhor das duas ideias". Feito, com a sessão no modelo mais forte (Fable).

- **`EDUCAVERSO-UNIFICADO.md`** (raiz) = FONTE ÚNICA DA VERDADE. Em conflito
  entre documentos, ELE manda. Os antigos (EDUCAVERSO.md, EDUVERSE-*, eduverse/)
  ficam como referência/memória — NADA foi apagado (decisão do Marcos).
- Conteúdo: propósito real (2027, coordenadora, 55 min) · Lei pedagógica
  (Portão 0 verbatim) · Mundo vivo + Verso + avaliação invisível · Currículo
  de Computação (eixos PC/MD/CD, objetivo→missão) · Estúdio profissional
  (Phaser+TS+Vite; IA gera DADOS validados, motor executa) · hardware real
  (FX-4300/3,5GB/Win7/Chrome109/Firefox106) · Arte & Som (voz Antonio LEI;
  revogada a ressalva speechSynthesis do PLANO-FABRICA) · Equipe + Portões ·
  Sustentabilidade · Estado honesto · ROADMAP ÚNICO (9 etapas; Etapa 3 =
  mundo vivo explorável = PRÓXIMA, decisão do Marcos) · Regras permanentes.
- **DECISÃO (pergunta do Marcos): não escrevemos mais motor próprio.** O motor
  é o Phaser; os artesanais (kit-floresta.py, build_premium.py, build_taberna.py)
  estão APOSENTADOS para desenvolvimento novo (ficam como referência e servindo
  o modelo leve publicado). Levamos deles o aprendizado + o contrato de dados.
- **`MANUAL-MESTRE.md` atualizado** (seção datada no topo): aponta o doc único;
  estúdio moderno disponível p/ premium SÓ se o Marcos pedir (molde clássico
  continua padrão); alvo real de máquina; reforço da voz Antonio.
- Próximo build: **Etapa 3 — mundo vivo explorável no estúdio, já com a voz
  do Antonio desde o nascimento** (escolha explícita do Marcos).

### [2026-07-17] Lições da fábrica de assets (Etapa 3)
- **Voz "Donato" (pt-BR-DonatoNeural) QUEBROU no edge-tts** (todas as falas
  falharam; o Antonio, no mesmo minuto, funcionou). A voz parece ter saído do
  catálogo da Microsoft. → Personagens usam **Antonio** até validar outra voz;
  testar 1 fala antes de mandar lote com voz nova. Amostra Gemini TTS também
  falhou (cota/modelo) — tentar de novo depois, sem bloquear produção.
- **Pollinations à noite adora pintar uma LUA solta** no quadro do asset →
  o recorte local (Pillow) guarda SÓ o maior objeto conexo + preenche buracos
  internos (sombras escuras viravam furos) + apaga a faixa do céu se precisar.
  Script: scratchpad/recortar_ilha.py (recriar se preciso: limiar ~14-34,
  maior componente, dilata 2px, alpha gradual anti-franja, autocrop, resize).
- **"Baú fechado" veio aberto** na 1ª geração → prompt teve que gritar
  ("lid COMPLETELY CLOSED, sealed, no opening"). Portão de Arte pegou. Sempre
  OLHAR cada imagem antes de integrar.
- **QA visual automatizado no CI:** o `app-build.yml` agora tira screenshots
  headless (`?qa=inicio` / `?qa=missao`) e commita em `_qa/` — o Portão 1
  ganhou olhos dentro do próprio build.

### [2026-07-17] REGRA DE OURO do Marcos (não pode quebrar): NADA À MÃO, TUDO PROFISSIONAL
No app Plano A (mundo vivo, educaverso-app), tudo o que a criança VÊ é feito por
tecnologia profissional — NUNCA desenhado por código à mão:
- **Cenário/fundo, água, personagens, objetos = imagem de IA** (Pollinations/Gemini),
  recortadas e otimizadas. Proibido "pintar por canvas" o que é ARTE que a criança vê.
- **Vida/animação = sistemas do motor Phaser** (partículas, tweens, luzes) — não
  partícula/efeito feito na unha.
- **Colisão = física do Phaser (Arcade Physics)** — não colisão manual por clamp.
- **Texto nítido** = `setResolution` (motor), não aceitar borrado.
- Exceção tolerada: primitivas de efeito do motor (sombra suave, brilho, pontinho de
  partícula) e um RESERVA invisível (só se um asset 404, pra nunca dar tela quebrada).
- **Pesquisar sempre o mais moderno/grátis que caiba no PC da escola** (FX-4300/3,5GB/
  Chrome109). Ex.: animação de personagem viva = runtimes esqueléticos (DragonBones grátis,
  Spine, Creature/CreaturePack p/ Phaser) — porém exigem RIG uma vez num editor (passo
  humano); não há botão mágico "1 imagem -> anda em 4 direções" grátis e automático.

### [2026-07-17] CAIXA DE FERRAMENTAS + pipeline de PERSONAGEM ANIMADO (automático, eu controlo)
O Marcos pediu: só ferramentas que EU controlo e gero TUDO automático (sem site/upload manual).

**Caixa de ferramentas (tudo grátis/viável no PC FX-4300/3,5GB/Chrome109, eu opero por workflow):**
- Motor: **Phaser 3** (render/física/animação). NÃO trocar — Phaser não é o problema.
- Arte cenário/objetos: **Pollinations/Flux** (grátis).
- Arte consistente / poses / recorte: **Gemini image** (centavos) editando a ÂNCORA — funciona headless via `gerar-imagens.yml` (input `base`).
- Voz: **edge-tts Antonio** (grátis). Som: Web Audio + CC0 (Kenney/Freesound).
- Mapas: Tiled. Dados validados: Zod/JSON-Schema. Save: Firebase. Build/deploy: Actions+Pages.
  Testes/QA: Vitest+Playwright (já uso screenshots no CI). Offline: Vite PWA. Painel: React.
- **Sites de sprite (AutoSprite/Spritesheets.ai): NÃO uso** — GUI, sem API grátis que eu dirija.

**PIPELINE DE PERSONAGEM ANIMADO (PROVADO que funciona — "cartela de poses como a gente fazia"):**
1. Âncora do personagem (ex.: `_novo/ilha_verso_azul.png`).
2. `gerar-imagens.yml` modelo=gemini, base=âncora, prompt "Keep the EXACT same character... redraw in POSE X, isolated on solid pure black background". Gemini MANTÉM o personagem (testado: verso_passo_a/b/c, verso_feliz).
3. Recorte automático (Pillow: fundo preto->transparente, maior componente, buracos, autocrop) + NORMALIZAR base dos pés + mesmo tamanho de canvas por quadro.
4. Phaser: sprite com animação (idle sutil; walk = alterna quadros de passo; feliz na vitória).
   -> personagem VIVO de verdade, automático, sem site.

**ERROS a não repetir (feedback do Marcos):**
- NUNCA esticar arte (fundo esticado = distorcido = "horrível"). Usar aspecto NATIVO.
- NÃO misturar perspectivas (poça vista de CIMA + praia vista de LADO = parece colado).
  Cena coerente: ou tudo top-down (estilo JRPG, sprites de frente) OU tudo de lado. Decidir e manter.
- Personagem = cartela de poses animada (NÃO 1 imagem estática com "esticadinho").

---

## Nome do aluno vem do CADASTRO no Firebase (decisão registrada — 2026-07-18)

O Marcos lembrou: **na atividade de verdade, o nome do aluno vai estar no Firebase,
nos cadastros da turma.** Isso já está montado:
- Modelo: `/turmas/<turma>/alunos/<aluno> = { nome, progresso, ... }` (`eduverse/lib/eduverse-save.js`).
- `_painel-prof/` já lista os alunos da turma (`EduSave.listarTurma`).

**Consequência boa para a VOZ do Byte falar o nome:**
- Como os nomes da turma são **conhecidos de antemão** (estão no cadastro), dá pra
  **gerar o áudio EXATO de cada aluno matriculado** (mesmo nome raro), rodando o
  workflow `[audio]` uma vez com a lista da turma → **100% de cobertura**.
- O **banco de 124 nomes comuns** (já gerado, voz Antonio, em `_voxel/audio/nome_<slug>.mp3`)
  continua como **rede de segurança** (nome digitado na hora / turma sem cadastro / visitante).
- Voz SEMPRE por API (edge-tts Antonio), NUNCA voz do navegador.

**LGPD (criança):** cadastro guarda o MÍNIMO — primeiro nome + código/apelido +
pontuação/progresso. Nunca dado pessoal completo.

**PENDENTE (decidir DEPOIS — o Marcos disse "depois pensamos nisso"):** como o aluno
se identifica pra entrar — (a) escolher o nome na lista da turma, (b) digitar um
código/matrícula, ou (c) continuar digitando o nome. Não decidir sozinho.

---

## 🔊 O Byte FALA o nome do aluno — GANCHO PRONTO e REUTILIZÁVEL (2026-07-18)

Feito e **no ar** na aventura voxel (`_voxel` → `ilha-voxel-teste`). É o gancho de
engajamento #1 do `_plano/plano_engajamento.md` ("o NPC lembra o nome") **elevado**:
antes o nome só aparecia no texto; agora o personagem **fala o nome de verdade**.

**Como funciona:**
- **Banco de 124 nomes** comuns de criança, gravados na **voz do Antonio**
  (`pt-BR-AntonioNeural`, edge-tts, via workflow `[audio]`). ~9 KB cada.
- **Mestre canônico:** `eduverse/vozes/nomes/` (+ lista `eduverse/vozes/nomes-banco.json`).
  Em uso no jogo: `_voxel/audio/nome_<slug>.mp3`.
- **Helper plug-and-play:** `eduverse/lib/voz-nome.js` (`window.VozNome`: `idDe(nome)`,
  `slug()`, `cadeia([...], aoFim)`). Manual: `eduverse/vozes/LEIA-ME.md`.
- **slug** = 1º nome, `NFD` sem acento, minúsculo, só `a-z0-9` (igual ao que o workflow
  gera). Ex.: "Cauã" → `nome_caua`.
- **Cadeia de voz sem cortar:** `nome → saudação → problema`. Nome no banco → saudação
  **sem apelido** (`vx_ola_nome`/`vx_voltou_nome`); nome fora do banco → saudação
  **genérica** com "grumete" (`vx_ola`/`vx_voltou`). Senão vira "Marina!… Ôa, grumete!"
  (soa como 2 pessoas) — foi feedback do Marcos, corrigido.
- **Voz SEMPRE por API. NUNCA a do navegador** (`SpeechSynthesis` proibida).

**BUG achado e consertado na raiz (auditoria antes do Marcos):** a saudação tocava
**2×** e na 2ª caía no genérico. Causa: em falha de rede (Firebase bloqueado), o
navegador dispara `onreadystatechange` (status 0) **E** `onerror` → o callback do
`EduSave` rodava 2× → `montarParada` montava 2×. Conserto: **trava anti-duplo no `_xhr`**
(`pronto=true` na 1ª; vale p/ `_voxel/eduverse-save.js` E `eduverse/lib/eduverse-save.js`)
+ **start idempotente** no jogo (`comecou`). QA render (Playwright headless) confirmou:
Marina/Cauã → `nome_x`+`vx_ola_nome` (1×); nome fora do banco → `vx_ola` (1×).

**Expandir o banco:** nomes em `_lote_falas.json` (`{id:"nome_<slug>",texto:"<Nome>!"}`)
→ commit `[audio]` → `cp _audio/nome_*.mp3` pro mestre e pro projeto → atualizar o set
em `voz-nome.js` + `nomes-banco.json`. **Melhor:** gerar a voz EXATA da turma pelo
cadastro do Firebase (100% de cobertura).

## 🧲 PADRÃO: todo projeto deve ter os ganchos de engajamento (decisão do Marcos, 2026-07-18)
"Todos os projetos devem ter essas melhorias para ficarem bem atrativos para os
estudantes." Virou **padrão obrigatório** no `EDUCAVERSO-CHECKLIST-DE-CENA.md`
(seção "Ganchos de Engajamento"): (1) falar o nome, (2) o mundo lembra/retoma,
(3) progresso visível + coleção, (4) novidade a cada volta, (5) autonomia. O Auditor
barra o que não tiver ≥ #1 e #2. **Status de adoção:**
- ✅ `_voxel` (Ilha das Trinta Moedas): #1 e #2 prontos.
- ⬜ `educaverso-app` (2D/Phaser), atividades **premium** e hub **Ilhas do Saber**:
  PENDENTE aplicar (helper `voz-nome.js` já pronto pra plugar). Registrar aqui conforme adotar.

---

## 🚢 VISÃO DO MARCOS: mundos CONECTADOS por travessia (não "corta" pra próxima fase) — 2026-07-18

Ideia do Marcos (direção de design pra TODAS as aventuras, não só a voxel):
- **Continuidade física entre fases:** em vez de terminar uma fase e a cena "cortar"
  pra outra, a criança **VIAJA** — vai de **barco** (ou **ponte**) até a próxima ilha.
- **A matemática CONSERTA o mundo (o problema vem primeiro, filosofia EduVerse):** ex.
  fase 1 — o navio está parado, ancorado, **afundando pelos furos**. A criança conta os
  **cocos** e, **a cada coco contado, um furo é tapado** → o barco conserta na frente dela.
  Só com o barco consertado dá pra **zarpar pra próxima ilha**.
- **Item + NPC (o loop):** resolver o problema dá um **item**; **outro personagem** (o
  Pinça / o que conserta o barco) **recebe o item e conserta o barco**. Aí libera a viagem.
- **As ilhas já estão no mundo, VISÍVEIS (no horizonte):** a criança VÊ pra onde vai e
  **conquista o caminho** resolvendo problemas/coletando — é o "mistério visível-mas-
  trancado" (`_plano/plano_engajamento.md` §2.5, "a ponte que abre o bairro"). Bate 100%
  com a nossa bíblia de design.
- **Por que diferencia:** a maioria dos jogos "educativos" é *pergunta → próxima tela*.
  Aqui é *problema do mundo → a conta CONSERTA o mundo → você VIAJA → a história continua*
  = vira "novela que eu acompanho", não prova. É o EduVerse puro ("aprende porque o
  MUNDO PRECISA").

**Honestidade técnica (pra não prometer o impossível no PC da escola):** mundo aberto
100% contínuo (andar sem cortes entre todas as ilhas) é pesado. O mesmo SENTIMENTO se
entrega leve com: (a) a contagem consertando o barco furo-a-furo; (b) uma **transição de
navegação curta** (o barco desliza pela água até a ilha seguinte, que já estava no
horizonte); (c) o NPC recebendo o item e consertando. Prototipar fase 1→2 primeiro, ver,
iterar, depois espalhar pras 5. **Vira padrão dos mundos EduVerse** (registrar no checklist
quando o protótipo aprovar).

---

## 🚢 Travessia fase 1→2 — PROTÓTIPO construído + iteração de arte (2026-07-18, cont.)

O Marcos aprovou "fazer a travessia ficar boa de verdade". Estado atual (no ar em
`ilha-voxel-teste`):
- **A contagem CONSERTA o barco:** cada coco contado **voa em arco até o barco e tapa
  um furo** (`cocoVoaProBarco`→`tapaFuro`); o barco **sobe e se desendireita** furo a
  furo. 5 furos, 6 cocos → sobra 1 (bate com a comparação EF01MA03). A criança VÊ a
  conta consertar (era o principal: antes o conserto ficava no canto, invisível).
- **Câmera vai ao barco no fim** (`olhandoBarco`, ângulo médio/de cima) pra ver o
  conserto + o **Pinça** (caranguejo) comemorando de perto.
- **Barco com mastro/vela/bandeira** (parece barco); **Pinça separado do barco** (não
  vira "blob"), pequeno e limpo.
- **Navegação limpa:** o Verso embarca e o barco **acelera pro mar aberto** (`pr²`),
  deixando a ilha de casa pra trás (fim do "paredão verde"), fade → chega na Parada 2.

**Feedback do Marcos (registrado p/ não repetir):**
- Áudio do nome vinha **cortado** → 200ms de "respirada" entre nome→saudação→problema.
- **"Grumete" repetia** (saudação com nome + fala do problema abrindo com "grumete") →
  fala do problema da fase 1 regravada SEM "grumete".
- "Não vi o barco na fase" → cocos voadores + câmera no fim resolvem.
- "Visual/dinâmica não muito legal" → dinâmica melhorou muito; **arte voxel de perto é
  o ponto fraco** (crab/barco "quadradões" no close). LIÇÃO: de longe o voxel engana
  bem, de perto aparece o blocado → preferir enquadramento médio/de cima; o Marcos é o
  diretor de arte, iterar arte às cegas por screenshot é lento.

**PENDENTE:** (a) ilha 2 visível no horizonte (removida — renderizava como "paredão");
(b) refino de arte do Pinça e do barco com o olho do Marcos; (c) espalhar a travessia
pras fases 2→5 SÓ depois do Marcos aprovar o feeling da 1→2.

---

## 🎨 VIRADA DE FORMATO: 2D ILUSTRADO (IA) + imagem/CSS = lindo, reconhecível, leve e SEM bug (2026-07-18)

Depois de muita conversa com o Marcos (voxel quadradão → 3D fofo → e a dor real: "criar o
mundo, código coerente, sem bug; e 2D/3D deram bug"), chegamos à **fundação**:

**FORMATO OFICIAL das atividades EduVerse (recomendado):**
- **Arte:** a **IA DESENHA** tudo (cena, objetos, personagem) — via workflow `[imagens]`
  (Gemini). Fica lindo e **reconhecível** ("o barco parece barco" porque é desenho, não
  cubo que eu monto). Provado: `_novo/cena2d_ilha`, `barco2d`, `coco_claro`, `byte2d`.
- **Montagem:** **1 HTML + IMAGEM + CSS** (DOM). **Sem three.js, sem física, sem Phaser,
  sem build.** A tecnologia mais à prova de bug que existe. Roda em qualquer PC da escola.
- **Recorte:** só **imagem INTEIRA** (fundo branco→transparente, flood da borda). **NUNCA
  cortar personagem em membros pra animar** (foi a fonte nº1 dos bugs — braço sumindo).
- **VIDA/animação:** vem de **CSS/JS** (bob, sway, squash, "respira", Byte pula/reage,
  confete, +1, brilhos flutuando). Fácil e **não buga** (ao contrário do sprite rigado).
  Responde o medo do Marcos: **2D ilustrado NÃO é parado.**
- **Dado, não código:** posições/quantidade/tema/objetivo BNCC = **dado**. Atividade nova
  = trocar o dado. **Um motor, currículo infinito, controlado pelo Marcos.**

**Provas no ar:** `ilha-2d-lindo` (2D ilustrado vivo) — o Marcos aprovou o visual; pediu
objetos mais reconhecíveis (feito: coco fibroso com folhinha) e temeu "sem vida" (feito:
tudo animado por CSS). Também existe `ilha-3d-fofo` (3D arredondado) como alternativa,
mas o 2D ilustrado ganhou em beleza+reconhecimento+baixo-bug.

**Por que isso mata os bugs:** motor simples (imagem+CSS) + arte inteira (sem recorte de
membro) + dado (não código) + Auditor (render/E2E). Bug some porque as partes frágeis
(física, recorte de pose, framework com build) **saíram**.

**Assets 2D já prontos** (em `_novo/`, recortados em `_2d/img/`): cena da ilha, barco,
coco (fofo e claro), Byte passarinho pirata. Reaproveitáveis.

**PRÓXIMO PASSO combinado a decidir:** transformar o teste na 1ª atividade real ("Números
até 30" completa nesse formato, com nome falado + mundo que lembra), OU o Marcos joga e dá
o veredito antes. NÃO espalhar sem ele aprovar o feeling.

---

## 🎮 ENGINE OFICIAL DOS JOGOS EXPLORATÓRIOS: Phaser 3 (decisão do Marcos, 2026-07-18)

O Marcos assumiu o papel de Diretor Técnico e definiu diretrizes profissionais (física
NATIVA da engine — nada de colisão na mão; FSM de animação; sprite sheet + FPS; LERP;
camadas/máscaras de colisão; WebGL/HTML5). Testamos as ferramentas:
- **Godot/Unity: INVIÁVEL no meu ambiente** — não instalados e o **proxy bloqueia o
  download (403)**. Godot só rodaria na máquina do Marcos, e o **export WebGL do Godot 4
  é pesado demais pro PC velho da escola (FX-4300)**. Descartado.
- **Phaser 3: ESCOLHIDO.** Engine 2D profissional, HTML5/WebGL nativo, LEVE, e eu
  **construo 100% headless e publico**. Atende TODAS as diretrizes: Arcade Physics
  (`body`+`collider`+collision groups = camadas/máscaras; velocidade zera no impacto),
  FSM de animação, sprite sheet, LERP, WebGL com fallback Canvas.
- **Obtido pelo GitHub/npm** (o proxy libera o npm; CDNs jsdelivr/unpkg dão 403):
  `npm pack phaser@3.80.1` → extraí `dist/phaser.min.js` → **vendorizado em
  `_lib_jogo/phaser.min.js`** (offline, igual ao `three.module.min.js`).

**PIPELINE (tudo no GitHub, igual ao Gemini):** arte → workflow `[imagens]` (Gemini) →
jogo Phaser em 1 HTML com `phaser.min.js` embutido → commit → Fábrica/republicar (Pages)
→ Auditor (render+E2E headless) antes de subir. **COMPROMISSO: parar de pular de estilo;
Phaser exploratório é O caminho, com física nativa (mata os bugs de colisão na mão).**
