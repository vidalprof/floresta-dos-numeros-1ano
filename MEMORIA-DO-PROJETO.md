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
- **Ideia em estudo:** mundo 2D em *tiles* (leve/escalável) + arte premium
  gerada por IA + Byte animado — o "casamento" que aproxima da confeitaria.

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
