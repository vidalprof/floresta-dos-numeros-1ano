# 🎬 ESTÚDIO EDUVERSE — plano do "2D incrível" (funcional · fluido · aproveitável · sustentável)

> Escrito para o professor Marcos, a partir da leitura integral da nossa base
> documental (visão, filosofia, style-bible, pipeline, equipe/QA, sustentabilidade,
> computação, manual-mestre, memória) por 4 especialistas em paralelo (jul/2026).
> **Objetivo:** parar de improvisar e montar o ESTÚDIO que produz o mundo vivo 2D
> incrível de forma repetível — do pré ao 9º ano.

---

## 1. A IDEIA que o estúdio precisa servir (reafirmada)

Um **mundo 2D vivo, persistente e explorável** (videogame de verdade, não quiz
ilustrado): a criança **anda, conversa e resolve problemas que o próprio mundo
precisa**. O conteúdo escolar é a **ferramenta** (salvar o pomar, fazer o navio
zarpar), e o conceito só ganha nome **no fim** (currículo invisível). O mundo
**lembra de cada criança** e cresce com ela ao longo dos 9 anos; a avaliação é
**invisível** e vira os documentos do professor. Lei imutável (Portão 0): problema
primeiro, conceito por último, conhecimento é ferramenta nunca tranca, o Byte
**pergunta** nunca responde, erro = consequência no mundo, **não é prova disfarçada**.

## 2. O que é "2D INCRÍVEL" (não vem do motor — vem destes 4 níveis)

1. **Arte pintada premium e COESA** (um estilo só, luz/sombra/volume — nunca chapado). ✅ *pipeline provado*
2. **Vida no personagem** — respira, pisca, anda suave (4 direções), **mexe a boca ao falar**, comemora, pensa, fica triste. *(poses IA editando a âncora + micro-vida por código)*
3. **Mundo vivo** — sol/luz deslizando, **vento** em rajadas, partículas (folhas/pólen/poeira nos pés), **dia/noite + clima**, água ondulando, sombras direcionais, bichos, NPCs que trabalham. **Regra dura: tela parada e muda = NÃO está pronta.**
4. **Suculência + som** — squash/stretch, faísca, **contagem que ACENDE** cada item em sincronia com a voz, som ambiente em camadas + narração do Antonio.

> Hoje a nossa melhor entrega tem só o **nível 1** (arte parada). O estúdio existe pra subir de forma **confiável** os níveis 2, 3 e 4.

## 3. ⚠️ DECISÃO #1 — o MOTOR oficial do mundo vivo (trava tudo)

Existem **dois estúdios** no repositório:

| | **Phaser 3 + TS + Vite** (`educaverso-app/`) | **ES5 `kit-floresta.py`** (`eduverse/`) |
|---|---|---|
| Estado | Declarado oficial (doc mais novo); anda/colide, mecânica de algoritmo, provado ~59fps no Chrome 109 | Fábrica madura: motor + montador + **robô-auditor** + biblioteca (~40 assets) + **5 mundos já compilados e jogáveis** |
| Render | **WebGL** (efeitos, luz, partículas, tweens — o "incrível" é mais fácil e mais bonito) | Canvas 2D à mão (mais frágil, ES5, teto de "incrível" menor) |
| Bugs | TypeScript pega erro no build | ES5 na unha (proibido `=>`/`let`/crase…) |
| Custo p/ adotar | **Re-hospedar a fábrica (contrato de dados + biblioteca + auditor) nele** | Já roda; mas contradiz a decisão declarada e limita o teto visual |

**Recomendação profissional (firme):** **Phaser 3 + TypeScript + Vite** vira o **motor único do mundo vivo**. É moderno, WebGL (teto de "incrível" alto), pega bug no build, roda no PC da escola, é grátis, e **já é a sua decisão declarada**. O que a linha ES5 tem de mais valioso **não é o motor** — é o **cérebro da fábrica** (contrato `dados.json`, biblioteca LEGO, catálogo de mecânicas, portões do auditor, os 5 mundos como CONTEÚDO). Isso é **agnóstico de motor** e a gente **transporta** pro Phaser. O motor ES5 escrito à mão **se aposenta** para mundo-vivo novo (os mundos viram conteúdo portável/referência).

*(O molde premium single-HTML "Circo do Teo" continua para atividades **estruturadas/não-exploráveis** — é à prova de bug e já entrega. O Phaser é só para o **mundo vivo explorável**.)*

## 4. FERRAMENTAS SELECIONADAS (o stack do estúdio)

| Camada | Ferramenta | Por quê | Custo |
|---|---|---|---|
| **Motor** | Phaser 3 + TypeScript + Vite | WebGL, física, câmera, tweens, partículas; roda no Chrome 109; TS mata bug | grátis |
| **Arte** | **Gemini** (âncora + poses + fantasias) + **Pollinations** (cenas/fundos) | pintura premium coesa; Gemini edita a âncora p/ coerência | Pollinations grátis; Gemini centavos, **cacheado por hash** |
| **Recorte** | `scipy` flood-fill de borda + de-fringe + autocrop | transparência limpa, sem franja, sem membro faltando | grátis |
| **Voz** | **edge-tts "Antonio"** (`pt-BR-AntonioNeural`), MP3 base64 | natural, sempre igual; **nunca** voz do navegador | grátis |
| **Dados** | `dados.json` validado por **JSON-Schema** ("dado torto não compila") | atividade = trocar dados; motor genérico e mudo | grátis |
| **Biblioteca** | LEGO: tiles + personagens (cartela de animação) + **props vivos data-driven** | mundo novo reusa ~90%; conserta 1× vale p/ todos | grátis |
| **Save/Avaliação** | **Firebase (Spark)**, interface `salvar/carregar` | ~2 KB/aluno; avaliação invisível → docs do professor; backend plugável | grátis |
| **Fábrica** | **GitHub Actions** (gerar-imagens/finalizar, gerar-audio, app-build, publicar) | geração/build/deploy na nuvem; internet liberada + secrets | grátis |
| **QA** | **robô-auditor headless** (Chromium + PIL/numpy) + os 4 Portões | testa antes de subir; Marcos não é o QA | grátis |
| **Hospedagem** | GitHub Pages (portal leve: 1 repo por atividade) | escala sem engasgar o build | grátis |

**Autossustentável garantido:** todas as camadas são grátis; o único custo é Gemini em centavos (com cache por hash), só onde precisa de recorte transparente premium.

## 5. A LINHA DE MONTAGEM (estações + portões)

Ordem sagrada — **design PRIMEIRO, gera, monta, audita, professor**:

1. **Pedagogo** → objetivo BNCC vira PROBLEMA DO MUNDO · **Portão 0 (filosofia)**
2. **Roteirista** → história + falas-**pergunta** do Byte + descoberta + reflexão
3. **Game Designer** → mecânica viva (erro = consequência; gating pela descoberta)
4. **Diretor de Arte** (+ prompts) → brief de estilo coeso; cartela de poses; recorte
5. **Sound Designer** → ambiente em camadas + narração Antonio (fila que não corta)
6. **Engenheiro** → monta dos DADOS + biblioteca no motor Phaser
7. **Robô-Auditor** → **Portão 1 (funciona)** + **Portão de Arte** + **Portão 2 (pedagogia/língua/voz)** — dirige a mecânica de verdade, rajada de screenshots, proporção, y-sort, peso, offline, fps no PC fraco
8. **Marcos** → **Portão 3**: aprova **pedagogia → arte → jogável** (só vê o que passou)

Cada bug novo vira **teste permanente** do auditor (o mesmo erro nunca volta).

## 6. Como o estúdio cumpre "fluido · aproveitável · sustentável"

- **Fluido:** **um** motor + **cenas data-driven**. Atividade nova = *gerar arte + preencher dados*, não reprogramar. O montador funde motor + dados → 1 build.
- **Aproveitável:** a **biblioteca LEGO** (tiles, personagens com cartela, **props vivos**), o **catálogo de mecânicas** (contar, ordenar, agrupar, trazer-exato, e a **VM do robô** de Computação) e os **testes do auditor** só **acumulam** — cada peça feita serve pra sempre.
- **Sustentável:** camadas grátis (Pages/Actions/edge-tts/Firebase/Pollinations) + Gemini centavos com **cache por hash** + HTML/bundle leve + `.git` limpo (portal leve).

## 7. O que APROVEITAR (já existe) × o que CONSTRUIR (falta)

**Aproveitar já:** pipeline de imagem (Gemini/Pollinations) e voz (Antonio) por workflow; recorte transparente; robô-auditor + portões; contrato `dados.json` + biblioteca + catálogo de mecânicas; **5 mundos em dados**; Phaser vendorizado + estúdio `educaverso-app` (anda/colide/mecânica); Firebase + save/voz-nome; hub, agenda, painel.

**Construir (as lacunas do "incrível"):**
1. **Consolidar no Phaser** o cérebro da fábrica (contrato + biblioteca + auditor).
2. **Mundo vivo NO Phaser** — andar livre + NPC vivo + a mecânica DENTRO do mundo (não telinha).
3. **Vida do personagem completa** — **6 poses reais** (pé normalizado) + **lip-sync + piscar + emoções** (hoje só respira/anda).
4. **Módulo "mundo vivo"** reusável — luz/vento/partículas/dia-noite/clima como props data-driven no Phaser.
5. **Contagem que ACENDE** sincronizada com a voz (requisito premium que falta em todas as mecânicas).
6. **Voz Antonio (MP3) desde o nascimento** — migrar todo legado que usa Web Speech.
7. **Jornada de 55 min** (`mundo.jornada`: 8 tarefas + 2 alívios) — planejada, falta implementar.
8. **Save por aluno no Firebase + painel ao vivo + documentos automáticos** (avaliação invisível).

## 8. ROADMAP em fases (cada fase entrega algo testável na sala)

- **Fase 0 — DECISÃO:** confirmar Phaser como motor único do mundo vivo. *(esta é a pergunta ao Marcos)*
- **Fase 1 — FUNDAÇÃO do estúdio:** motor Phaser genérico + contrato `dados.json` (schema) + estrutura da biblioteca + pipeline de arte/voz plugado + auditor headless + interface de save. *(a "máquina" pronta)*
- **Fase 2 — A CAMADA "INCRÍVEL":** vida do personagem (poses + lip-sync + piscar + emoções) + módulo mundo-vivo (luz/vento/partículas/dia-noite) + contagem-acesa + som ambiente. **Entregável: UMA cena de referência genuinamente incrível.**
- **Fase 3 — 1ª ATIVIDADE COMPLETA no estúdio:** um mundo vivo ponta-a-ponta pelos portões, **testado com crianças**.
- **Fase 4 — ESCALA:** jornada de 55 min, mais atividades por dados, Computação "programe o robô", avaliação → documentos do professor.

## 9. Regras inegociáveis (o estúdio respeita sempre)

Voz **sempre** API/Antonio (nunca navegador) · **tudo que a criança vê é IA** (zero desenho por código/SVG) · **zero emoji** lido pelo TTS · geração **por workflow** (nunca pelo chat) · alvo **FX-4300 / 3,5 GB / Chrome 109 / 1024×768 / 30 fps** — **testar no PC real** · **"tela parada = não pronta"** · **o Marcos não é o QA** · na dúvida **PERGUNTAR** · cada lição paga vira teste permanente + nota na memória.

---

**Próximo passo:** confirmar a **Decisão #1** (o motor). Com ela travada, começo a **Fase 1** (montar a fundação) e depois a **Fase 2** (a cena de referência "incrível"), que é a que te faz *ver* o teto.
