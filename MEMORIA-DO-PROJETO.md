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
- Estado: groundwork existe (baixar-curriculo.yml, ATIVIDADE-COMPUTACAO.md, catálogo de
  interatividades); FALTA o montador que casa currículo→mecânica→mundo→faixa de forma semiautomática.

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
