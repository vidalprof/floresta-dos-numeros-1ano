# 🏛️ RPG EDUCATIVO IA — Arquitetura da Plataforma (o "Canva dos RPGs Educativos")

> Documento de arquitetura (jul/2026) — escrito a pedido do Marcos, antes de qualquer código.
> Papéis: Arquiteto Sênior · Game Dev Sênior · Engenheiro de IA · UX · EdTech.
> **Alvo do produto:** o professor informa **ano · disciplina · objetivo · tema · tempo · dificuldade**,
> clica **GERAR** e recebe um **RPG top-down educativo completo, jogável e adequado**. Sem programar,
> sem editar JSON, sem desenhar. Roda no PC de 2012 da escola **e** no celular. Escalável por anos.

---

## 0. O ponto de partida honesto — quanto JÁ existe (reaproveitar, não recomeçar)

O `educaverso-app/` (Phaser 3 + TypeScript + Vite) **já entrega o núcleo do motor RPG**:
movimentação + **colisão** + **câmera que segue** + **NPCs animados** + **sistema de missões** (catálogo
plugável) + **diálogos** (voz) + **inventário/mochila** + **entrega a NPC → o mundo MUDA** (gramática da
ponte) + **grafo de zonas com portais/interiores** + **save (localStorage)** + **contrato de dados
validado (Zod)** + **auditor de coerência** + **robô-QA (Playwright) que joga o mundo antes do professor**.
Isso é exatamente o "motor reutilizável" pedido. **A plataforma promove esse motor a produto** e adiciona
por cima: renderização por **tilemap + asset pack**, a **camada geradora (IA pedagógica)**, os **painéis**
(professor/aluno), o **Firebase** e o **relatório**.

### As 3 mudanças de rumo deste brief (e por que são boas decisões)
1. **Gráficos = Asset Pack profissional, NÃO IA.** ✅ Decisão profissional correta para uma PLATAFORMA:
   identidade **garantidamente consistente**, arquivos minúsculos (roda no PC velho), **zero custo por
   imagem**, e nenhuma "deriva de estilo" (o risco nº1 quando se gera arte por IA em escala). *(A arte
   pintada por IA que já produzimos vira uma linha "premium" à parte — a plataforma padrão usa o pack.)*
2. **Mapas via tilemap (modelos prontos).** ✅ É o padrão da indústria para RPG top-down e é o que
   permite "a IA escolhe o modelo e posiciona as coisas" sem desenhar nada.
3. **A IA gera só CONTEÚDO PEDAGÓGICO** (história, missões, diálogos, NPCs, recompensas, relatório) →
   um **AdventureSpec (JSON) validado** que o motor executa. A IA nunca toca em pixel nem em código.

---

## 1. Melhorias que eu PROPONHO (a parte de "sugerir melhorias" do pedido)

> Onde eu, como time sênior, discordo/acrescento ao brief — para a plataforma nascer certa.

### ⭐ 1.1 — O GUARDA-CHUVA PEDAGÓGICO (o risco nº1, inegociável)
O brief lista "Perguntas", "Desafios", "inimigos educativos". **Perigo mortal:** um gerador solto vira
**quiz disfarçado** ("responda 3×4 para abrir a porta") — que é **proibido pela nossa LEI** (Portão 0:
não é prova disfarçada; o conhecimento é ferramenta, não tranca; erro = consequência, não X vermelho).
**Melhoria obrigatória:** o gerador **nunca** emite missão do tipo pergunta-resposta. Toda missão sai do
**CATÁLOGO DE MECÂNICAS** (agrupar, juntar, repartir, ordenar, coletar-grupos, entregar, programar-robô,
medir-para-caber…). Os próprios exemplos do Marcos já são assim ("Multiplicação → coletar grupos",
"Adição → juntar recursos") — **ótimo**, só formalizo isso como regra dura. "Inimigos educativos" viram
**obstáculos/problemas do mundo** (a ponte quebrada, o moinho parado), não combate-por-pergunta. **O
AUDITOR reprova qualquer spec que fira o Portão 0 — automaticamente, antes de publicar.**

### 1.2 — ONDE a IA roda (a decisão de arquitetura mais importante)
"Clicar GERAR e acontecer na hora" exige um LLM acessível pela plataforma. Três caminhos, e eu recomendo
o **híbrido em 3 camadas** (robusto e barato):
- **Camada A — Gerador determinístico no navegador (SEMPRE funciona, grátis, offline, instantâneo).**
  A "IA" base é um **motor de montagem por regras**: escolhe modelo de mapa + preenche as missões a
  partir de um **BANCO CURRICULAR** (objetivos BNCC → mecânicas) e **bancos de história/diálogo por tema**.
  Sem servidor, sem chave, sem custo. **É o coração — a plataforma nunca depende de estar online com IA.**
- **Camada B — Enriquecimento por LLM (opcional, liga com uma chave).** Um **proxy serverless grátis**
  (Cloudflare Workers — free tier 100k req/dia) guarda a chave e chama um LLM de **cota grátis** (Google
  Gemini free tier / Groq / Pollinations-texto). Ele **reescreve** história/diálogos com mais criatividade
  e variedade. Se cair/faltar, **degrada** para a Camada A sem quebrar nada.
- **Camada C — Aventuras "curadas premium" (offline, por nós).** Onde a qualidade tem que ser máxima
  (aula de referência), o próprio Claude gera o AdventureSpec por workflow e ela entra no catálogo. O
  professor DUPLICA e ajusta.
> Resultado: **funciona 100% grátis e offline (A)**, fica **mágico com LLM quando quiser (B)**, e tem
> **ouro curado (C)**. Nunca fica na mão de um único ponto de falha.

### 1.3 — Tilemap real (Tiled/LDtk), não mapa por código
Cada "modelo de mapa" (Vila, Floresta, Escola…) é um **mapa Tiled** (.json) com **camadas**: chão, decor,
**colisão**, e uma **camada de OBJETOS com SLOTS nomeados** (`spawn_heroi`, `npc_1..n`, `porta_1`,
`area_missao_1`, `tesouro_1`, `bloqueio_1`). O gerador **só preenche os slots** (qual NPC, qual missão,
qual porta leva aonde). Phaser 3 carrega Tiled nativamente com culling (desenha só o visível → rápido no
PC fraco). Editar mapa vira arrastar no Tiled — **nós**, nunca o professor.

### 1.4 — Separação dura MOTOR × CONTEÚDO (já é nossa arquitetura)
O **motor é genérico e mudo** (zero string de enredo). Toda a aventura mora no **AdventureSpec**. Isso é
o que faz a plataforma escalar: mundo novo = novo JSON + (talvez) novo mapa Tiled, **nunca** recompilar
o motor.

### 1.5 — "Inimigos educativos" → **desafios do mundo** (coerência com a filosofia)
Reenquadrar: nada de monstro que você derrota acertando conta. Os "antagonistas" são **problemas**
(a enchente, a máquina quebrada, o portão emperrado) que o **conhecimento resolve** — mantém tensão de
jogo **sem** virar prova.

### 1.6 — Acessibilidade & não-leitores (o público real: pré ao 9º)
Voz em tudo (o pré não lê), ícones + cor, alvos de toque grandes, e **dois modos de UI** por faixa
(Pré-2º: só ícone+voz; 3º+: texto). Isso entra no gerador (a "dificuldade/faixa" muda a densidade de texto).

---

## 2. Stack tecnológico (confirmado + acréscimos)

| Camada | Tecnologia | Papel |
|---|---|---|
| Motor de jogo | **Phaser 3.80 + TypeScript + Vite** | RPG top-down, tilemap, física Arcade, câmera, tweens, partículas |
| Mapas | **Tiled** (`.tmj`/JSON) | modelos de mapa com camadas de colisão + slots de objeto |
| Arte | **Asset Pack CC0 profissional** (recomendo **Kenney** — top-down/RPG; identidade única, grátis) | tiles, personagens, NPCs, objetos, UI |
| Áudio | **edge-tts "Antonio"** (voz) + **música CC0** (Kenney Audio/FreePD) | narração embutida + trilha por bioma |
| Dados | **JSON validado por Zod/JSON-Schema** ("spec torta não roda") | AdventureSpec + bancos curriculares |
| IA (opcional) | **Proxy serverless grátis** (Cloudflare Workers) → **LLM de cota grátis** | enriquecer história/diálogo |
| Backend | **Firebase (Spark, grátis)** — RTDB/Firestore + Auth | professores, turmas, alunos, progresso, relatórios |
| CI/CD | **GitHub Actions** | build, otimização de assets, **robô-QA (Playwright)**, publicar |
| Hospedagem | **GitHub Pages** (portal leve) | a plataforma + cada RPG publicado |
| QA | **Playwright** headless nos Actions | joga o RPG gerado ANTES do professor (portões) |

**Custo:** núcleo 100% grátis (A + Pages + Actions + edge-tts + Firebase Spark + Kenney CC0). LLM
opcional (B) roda em cotas grátis; se um dia escalar além delas, centavos.

---

## 3. Arquitetura em camadas (o fluxo do brief, refinado)

```
  PROFESSOR (Painel)                          ALUNO (Painel)
        │ ano/disciplina/objetivo/tema/tempo        │ código da turma + nome
        ▼                                            ▼
  ┌───────────────────────────────────────────────────────────┐
  │  CAMADA GERADORA  (o "Canva")                              │
  │   1) Gerador Pedagógico  objetivo → conceitos → mecânicas  │
  │   2) Gerador de História  tema → título/enredo/NPCs        │
  │   3) Seletor de Mapa      escolhe modelo Tiled + preenche  │
  │   4) Gerador de Missões   mecânica por parada (catálogo)   │
  │   5) Gerador de Diálogos  falas curtas/infantis (+ voz)    │
  │   6) Gerador de Relatório  o que medir por objetivo        │
  │   (Camada A determinística  ·  B LLM opcional  ·  C curada)│
  └───────────────────────────────────────────────────────────┘
        │  produz →   AdventureSpec (JSON)
        ▼
  ┌───────────────────────────────────────────────────────────┐
  │  VALIDAÇÃO + AUDITOR  (Zod schema + Portão 0/Arte/Coerência)│  ← reprova spec ruim
  └───────────────────────────────────────────────────────────┘
        │  spec válida →
        ▼
  ┌───────────────────────────────────────────────────────────┐
  │  MOTOR RPG (genérico)  +  ASSET PACK  +  TILEMAP            │  → JOGO FINAL jogável
  └───────────────────────────────────────────────────────────┘
        │  eventos de jogo (acertos/tempo/missões) →
        ▼
        FIREBASE  (progresso, pontuação, RELATÓRIO do professor)
```

---

## 4. Organização de pastas (monorepo)

```
plataforma-rpg/
  packages/
    engine/            # MOTOR RPG genérico (Phaser+TS) — data-driven, reutilizável
      src/core/        # loop, câmera, colisão, input (teclado+toque)
      src/systems/     # movimento, tilemap, npc, dialogo, inventario, missao,
      src/systems/     #   porta/chave, bau, moeda, xp, som, particulas, save, dicas, conquistas
      src/mechanics/   # CATÁLOGO de mecânicas (agrupar, juntar, ordenar, coletar_grupos, programar_robo…)
      src/hud/         # inventário, missões, barra de progresso, relatório
      src/schema/      # AdventureSpec (Zod) — o contrato
    generator/         # CAMADA GERADORA (roda no navegador; Camada A)
      src/pedagogia/   # BANCO CURRICULAR (BNCC/Blumenau → objetivo→conceito→mecânica)
      src/historia/    # bancos de tema (vila, floresta, espaço, fundo-do-mar…) — nomes, NPCs, tom
      src/mapas/       # índice dos modelos Tiled + regras de seleção/slot-fill
      src/missoes/     # objetivo+mecânica → parâmetros da missão
      src/dialogos/    # gerador de falas curtas por papel (introdução/dica/feedback/conclusão)
    llm-proxy/         # (opcional) Cloudflare Worker — Camada B (chave server-side)
    ui/                # PAINÉIS (React ou HTML/TS): professor, aluno, tela GERAR
    shared/            # tipos, validação, util comum
  content/
    assets/            # Asset Pack (tiles/personagens/UI/som) — 1 identidade
    maps/              # modelos Tiled (.json) com slots nomeados
    audio/             # vozes (edge-tts) + música CC0
    adventures/        # AdventureSpecs curados (Camada C) + gerados
  tools/               # robô-QA (Playwright), otimizador de assets, semear Firebase
  .github/workflows/   # build, qa, publicar, gerar-voz, baixar-assets
```

---

## 5. Modelo de dados

### 5.1 — AdventureSpec (o coração; validado por Zod)
```
Adventure {
  id, titulo, tema, faixa (pre|1-2|3-5|6-9),
  objetivo_bncc, conceito_final,           // conceito nomeado SÓ no fim (Portão 0)
  duracao_min, dificuldade,
  mapa: { modelo, musica },                // ex.: modelo="vila"
  heroi,                                    // personagem do aluno (do pack)
  zonas: [ Zona{ id, slots_preenchidos, portais, missao, npcs, falas } ],
  missoes: [ Missao{ id, mecanica_id, params, gancho, recompensa, gating } ],
  relatorio: { objetivos_medidos[], conceitos[] }
}
```
> `mecanica_id` **obrigatório** e ∈ catálogo → **impossível** gerar quiz disfarçado por construção.

### 5.2 — Firebase (Spark grátis; gaveta por escola, como já fazemos na Agenda)
```
/rpg/<escola>/
  professores/<uid>          # nome, turmas
  turmas/<turmaId>           # ano, alunos[]
  aventuras/<advId>          # AdventureSpec publicado + metadados
  progresso/<turmaId>/<aluno>/<advId>   # missões feitas, tempo, tentativas, pontuação
  relatorios/<advId>         # rollup (calculado na leitura → barato)
```
Regras: isolamento por dono (o padrão blindado que já validamos na Agenda). Só 1º nome + turma (LGPD).

---

## 6. Fluxo de geração (passo a passo)

1. Professor preenche o formulário → **GERAR**.
2. **Gerador Pedagógico**: objetivo BNCC → conceito(s) → escolhe **mecânica(s)** do catálogo (mapa fixo
   objetivo→mecânica no banco curricular).
3. **Seletor de Mapa**: escolhe o modelo Tiled adequado ao tema/nº de missões (ex.: multiplicação+vila →
   `vila`), lê os slots disponíveis.
4. **Gerador de História** (A determinístico, ou B LLM): título + enredo + escolhe NPCs do pack + amarra
   cada missão a um **lugar/NPC** (a lei: missão mora num lugar, não num menu).
5. **Gerador de Missões**: para cada parada, instancia a mecânica com `params` (quantidades, grupos…) e o
   **gancho** (problema do mundo) + **recompensa** (item que muda o mundo / abre caminho).
6. **Gerador de Diálogos**: falas curtas por papel + **narração** (edge-tts, gerada por workflow; nomes de
   arquivo determinísticos → cache).
7. **Montagem** do AdventureSpec → **Zod valida** → **Auditor** roda os portões (Portão 0 filosofia,
   coerência de mapa/slots, cobertura de voz). **Falhou → não publica; conserta ou volta pro gerador.**
8. **Robô-QA (Playwright)** joga a aventura de ponta a ponta (headless) → screenshots + laudo.
9. Aprovado → **publica** (Pages) + salva no Firebase. Professor recebe **link + relatório-modelo**.

---

## 7. Motor RPG — módulos (a lista do brief, organizada e priorizada)

**Núcleo (já temos, generalizar):** loop dt-real · movimento 4-direções · **colisão** · câmera lerp/clamp ·
input **teclado + toque** · **tilemap (novo)** · NPCs animados · **diálogos** · **inventário/mochila** ·
**missões (catálogo)** · **entrega → mundo muda** · portais/interiores · **save automático**.
**A construir (extensões limpas):** tilemap Tiled + culling · **porta/chave/baú/moeda/XP** (mecânicas de
mundo) · **sistema de dicas** (o Byte oferece ajuda sem entregar) · **conquistas** · **relatório** (coleta
eventos → Firebase) · **partículas/som** por prop data-driven (já iniciado) · **sistema de progresso**
(barra de missões).
> Tudo **data-driven**: cada sistema lê do AdventureSpec; nada hard-coded por aventura.

---

## 8. Desempenho & compatibilidade (o PC de 2012 é requisito, não desculpa)

- **Tilemap com culling** (Phaser desenha só tiles visíveis) → mundo grande sem custo.
- **Atlas de texturas** do pack (1 folha) → poucas chamadas de GPU; **pixelRatio travado em 1**.
- **Orçamento por cena**: ≤ N texturas vivas, ≤ 2 emissores de partícula, `fps.target: 30`,
  `powerPreference: low-power`, `antialias` conforme o pack.
- **Fallback**: `Phaser.AUTO` (WebGL → Canvas2D se a GPU for fraca/blacklistada no Chrome 109).
- **Peso**: cada RPG publicado usa o **pack compartilhado** (cacheado pelo navegador) → páginas minúsculas.
- **Toque**: `ontouchstart` + `touch-action:manipulation` + anti-toque-duplo (celular/tablet).
- **Teste no PC REAL da escola** entra no ciclo (gate de fps no CI + validação presencial).

---

## 9. Estratégia de crescimento & manutenção (durar anos)

- **Modular/versionado**: `engine`, `generator`, `ui` evoluem separados; o **AdventureSpec tem versão**
  (specs antigas continuam jogáveis).
- **Catálogos que só CRESCEM**: mecânicas, modelos de mapa, bancos de tema, testes do auditor — cada peça
  feita serve pra sempre; cada bug vira **teste permanente** (o robô-QA nunca deixa voltar).
- **Conteúdo é dado, não deploy**: aventura nova não precisa de release do motor.
- **Documento vivo**: este arquivo + a memória são a fonte da verdade entre sessões.

---

## 10. Roadmap de construção (cada fase entrega algo usável)

- **F1 — MOTOR-PLATAFORMA:** generalizar o motor da Floresta + **tilemap Tiled** + **1 asset pack** + 1
  modelo de mapa (Vila) jogável a partir de um AdventureSpec escrito à mão. *(reuso altíssimo)*
- **F2 — GERADOR (Camada A) + AUDITOR:** formulário do professor → AdventureSpec determinístico válido →
  RPG jogável, sem LLM, 100% grátis. **É aqui que nasce o "Canva".**
- **F3 — VOZ + RELATÓRIO + FIREBASE:** narração automática, salvar progresso, relatório do professor.
- **F4 — PAINÉIS + PUBLICAR/DUPLICAR/EXPORTAR** e **LLM opcional (Camada B)** para variedade.
- **F5 — ESCALA:** mais modelos de mapa, mais mecânicas, mais temas; **teste com crianças** na escola.

---

## 11. Decisões que dependem do Marcos (para eu não chutar)

1. **Asset Pack:** confirmo **Kenney (CC0, top-down)** como a identidade única? (grátis, consistente,
   leve, sem atribuição). Se quiser um visual específico, você escolhe o pack e eu construo em cima dele.
2. **A IA ao vivo:** começamos **100% grátis/offline (Camada A)** e adicionamos o LLM opcional depois?
   (recomendo sim — a plataforma nasce funcionando sem depender de chave/servidor).
3. **Escopo da F1:** eu já **generalizo o motor + ligo tilemap + monto a Vila jogável** como prova da
   plataforma, e só depois o gerador — de acordo?
