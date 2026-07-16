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
- **Balões:** compactados (estilo videogame). **PENDENTE decisão do Marcos: balão BRANCO (quadrinho,
  arredondado) × ESCURO (caixa RPG).** Renderizei os dois; ele inclina pro branco (mais fofo/leve p/ crianças).
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

## 🗺️ A GRANDE AVENTURA — estrutura do mundo (visão do Marcos)
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
