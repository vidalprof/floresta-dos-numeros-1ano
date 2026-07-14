# MANUAL MESTRE — ATIVIDADES EDUCATIVAS HTML GAMIFICADAS
## Marcos — pedagogo/dev, Blumenau-SC — escola pública
## Documento único de referência. Funde o antigo MANUAL-CONSOLIDADO + COMO-INICIAR + ATUALIZAÇÕES.
## Ler JUNTO com o ATIVIDADE-PREMIUM.md (que define o FORMATO/DINÂMICA fixo de toda atividade).
## Em conflito de FORMATO/dinâmica, o ATIVIDADE-PREMIUM.md manda; aqui estão as regras técnicas e pedagógicas completas.

================================================================
## REGRA DE CONDUTA — NÃO INVENTAR NADA (leia antes de tudo)
================================================================
- **NADA pode ser inventado.** Não criar botão novo, animação diferente, disposição própria, fase, mecânica, texto de fluxo ou "melhoria" criativa que não esteja neste manual ou no ATIVIDADE-PREMIUM.md. O modelo é fixo.
- **NA DÚVIDA, PERGUNTE AO USUÁRIO ANTES DE MEXER.** Vale para conteúdo pedagógico, para qualquer comportamento não descrito aqui, para uma imagem que parece estranha/trocada, para um resultado ambíguo de processamento. Parar e perguntar é sempre melhor que entregar errado.
- **Nunca aplicar correção automática em massa** (ex.: reprocessar todas as imagens, trocar vocabulário) sem verificação; se a verificação não for conclusiva, segurar a mudança e perguntar.
- Ao encontrar indício de asset trocado/errado (cor não bate, medalha que não parece medalha), NÃO "corrigir" por conta própria: levantar os fatos (dimensões, cores, comparações) e PERGUNTAR.
- Isso vale em TODA conversa, do início ao fim, mesmo sob pressão de pressa. Preferir a pergunta curta à suposição.

================================================================
## PROCESSO OFICIAL — CRIAR UMA ATIVIDADE PREMIUM (o rito, seguir sempre)
================================================================
Quando o usuário pedir uma **atividade premium** dando **CONTEÚDO + ANO/DISCIPLINA**, seguir esta ordem, sem pular etapa. A base premium de referência é **"O Grande Circo do Teo"** (Pré) — CLONAR ela, não recomeçar.

> **NEM TUDO É PREMIUM — o rito premium é SÓ quando o Marcos PEDIR (pedido dele):** existem
> pedidos **à parte**, que NÃO seguem este molde nem o checklist premium — ex.: o **Desafio da
> Copa** (leitura), um **jogo de colorir com várias imagens**, uma atividade pontual/mais simples,
> **OU um estilo/formato totalmente NOVO** que a gente nunca fez. **FORMATO PRÓPRIO já definido:**
> quando o Marcos disser **"atividade de computação"** = seguir o **`ATIVIDADE-COMPUTACAO.md`**
> (BNCC Computação, "programe o robô" etc.), NÃO o molde premium. **O ESTILO é livre — o Marcos
> manda no formato.** Nesses, construir **do jeito que ele pediu**, SEM impor a máquina premium
> (base-mãe, medalhas/níveis, adaptativo, `--exigir`) nem nenhum molde antigo. **O MÍNIMO que vale
> em QUALQUER estilo (não-negociável):** 1 HTML único autossuficiente; roda em navegador antigo
> (compatibilidade) + 0 erro de JS (`auditar-geral.py`, `testar-jogando.py`); imagens reais (nunca
> SVG); português; e "na dúvida, PERGUNTAR, não inventar". O que é SÓ do premium: o checklist de
> recursos (`--exigir`). **Na dúvida se é premium ou outro estilo, PERGUNTAR** — não presumir molde.

**FASE 0 — Ler tudo na íntegra.** Antes de qualquer coisa, ler por completo: `ATIVIDADE-PREMIUM.md`, este `MANUAL-MESTRE.md` e o `CLAUDE.md`. Não agir de memória. NÃO INVENTAR; na dúvida, PERGUNTAR (vale o rito inteiro).

**FASE 1 — Vestir o PROFESSOR da disciplina/ano (pedagógico primeiro, código depois).**
> **OS 5 CHAPÉUS (pedido do usuário — vestir SEMPRE, ao mesmo tempo):** (a) **professor
> especialista da disciplina** pedida; (b) **PEDAGOGO** quando for **Pré → 5º ano** (turmas
> menores); (c) **dev sênior**; (d) **designer instrucional** com ênfase em atividade
> pedagógica; (e) **especialista em GAMES EDUCATIVOS** — bagagem de **pesquisa acadêmica +
> cursos de game design** (SDT, Malone, Flow, DGBL, MDA, game feel); ver a seção
> **"Especialista em Games Educativos"** no fim deste manual. Tudo **lendo os manuais na
> íntegra** e **seguindo a atividade premium de referência** (Circo do Teo). Vamos
> **melhorando conforme a necessidade**.
1. **BNCC:** mapear as **habilidades e objetos de conhecimento** do ANO+DISCIPLINA pedidos (códigos EI/EF). Verificar se o conteúdo solicitado é **adequado àquele ano** — se estiver adiantado/atrasado ou fora do escopo do ano, APONTAR e PERGUNTAR antes de seguir. Nada de "achismo": se não tiver certeza da habilidade BNCC, dizer que vai confirmar / perguntar.
2. **SUGERIR TIPOS DE ATIVIDADE (pedido do usuário — antes de construir):** quando o usuário
   disser que quer desenvolver uma atividade (conteúdo+ano), **propor 2–3 formatos/tipos**
   que combinam com aquele conteúdo e idade (ex.: caça-palavras, monte-a-frase, contar
   objetos, arrastar-e-soltar, quiz ilustrado, história com missões…), com uma frase de
   por quê cada um serve — e deixar o usuário **escolher** antes de eu sair fazendo.
3. **Plano didático:** objetivos de aprendizagem; **progressão** do concreto→abstrato / fácil→difícil (escada de Bloom); apoio ao erro (não punir, ensinar); linguagem e comandos na medida da idade; enunciados que batem com a figura.
4. **Escolher os MÓDULOS de fase** do catálogo (seção "MECÂNICAS DE FASE") que servem AO ANO E AO CONTEÚDO — e SÓ esses. Módulos são por idade: ex. Pré usa cores/vogais/contar/**pintar**; anos maiores usam contas armadas/monte-a-frase/interpretação/caça-palavras… e **NÃO** levam "pintar". A **recompensa final também troca por idade** (Pré=Tela de Pintar; maiores=estúdio de criação / desafio-mestre / diploma).

**FASE 2 — Vestir o DEV SÊNIOR + DESIGNER INSTRUCIONAL (construir).**
1. **Clonar o template-base** (Circo do Teo): o NÚCLEO já vem pronto e serve toda idade — mapa-aventura narrado, mascote, XP/níveis/emblemas, medalhas, conquistas/selos, relatório do professor, adaptatividade (Extra/Reforço — ver requisito abaixo), recompensa que cresce + barra, narração, compatibilidade, `build.py`, `auditar.py`. Trocar só TEMA (mascote/cores/ilhas), CONTEÚDO (dados dos desafios) e RECOMPENSA final.
   > **DIFICULDADE ADAPTATIVA = REQUISITO OBRIGATÓRIO em atividade NOVA (padrão a partir de agora):**
   > toda atividade nova precisa nascer com **os DOIS** mecanismos: **Desafio Extra**
   > (acertou 100% → oferece rodada mais difícil) **e Reforço** (acertou <50% → treina de
   > novo o que errou, antes de seguir). O Circo do Teo já traz o padrão pronto (`ofereceExtra`,
   > `ofereceRef`, `iniciarExtra()`, `iniciarReforco()` no `fimFase`) — clonar e adaptar o
   > conteúdo, nunca remover. Evolução futura possível (quando o usuário pedir): tornar o ajuste
   > **automático no meio da fase** (subir/descer conforme a criança), não só no fim.
   > **IMPORTANTE — não mexer no passado sem pedido:** as atividades JÁ publicadas ficam como
   > estão; algumas têm só o Extra e duas (`InglesRelativePronouns8`, `pr-escola-1`) não têm
   > nenhum. NÃO retrofitar em lote — só padronizar UMA quando o usuário pedir "melhorar".
2. **Front-load de TODAS as imagens (acelera muito):** logo no começo, entregar **UM documento com TODOS os prompts** que a atividade vai precisar (mascote 4 poses, companheiros, ilhas de cada parada, objetos, cartela de medalhas, cartela de emblemas, cartela de selos, recompensa em 3 fases, capa, cena final, e — se for do Pré — desenho de colorir). O usuário gera em LOTE e sobe tudo; aí recorto/monto em paralelo, sem ida-e-volta peça por peça. **Prompt sempre colado no CHAT** (além do arquivo). **→ AGORA no PADRÃO 3D VIVO: todas as cartelas em 3D (Pixar/última geração), e o Claude as deixa ANIMADAS/vivas (ver a seção "⭐ PADRÃO 3D VIVO"). Lista COMPLETA obrigatória — nunca resumir:** mascote (6 poses, incl. **boca aberta p/ falar**), **personagem-mascote de CADA ilha**, ilhas/cenários, objetos das questões, **medalhas** (bronze/prata/ouro), moeda/estrela/troféu/baú, **emblemas**, **selos/conquistas** (incl. o de **sequência**), **cadeado** (fechado/aberto), **recompensa-que-cresce (3 fases)**, capa e cena final.
3. **Compatibilidade SAGRADA sempre** (só `var`/`function`/`for`, prefixos `-webkit-`, emoji ≤ Unicode 6.0, imagens otimizadas, **1 HTML único autossuficiente** com tudo em base64).

**FASE 3 — Precisão (sem erros) ANTES de publicar.** `auditar.py` = APROVADO **+** QA nos 3 níveis (estático; play-through headless de TODAS as telas em 320/414px com 0 erro/overflow — lembrar do viewport fixo do headless, forçar `#wrap:340px` p/ testar estreito; pedagógico: concordância n=1, pronúncia, português, enunciado×figura, narração não entrega resposta). Conferir imagens COM o usuário (mosaico/screenshot).

### FERRAMENTAS DE QA — a "equipe de qualidade" (rodam AQUI, nunca no PC da escola)
- **`_circo/auditar.py <html>`** — auditoria específica do build do Circo (checks 1–12, inclui itens só do Circo como cenário/nome da parada). Use no build da atividade nova.
- **`_circo/auditar-geral.py [--matriz] [--exigir] <html> [...]`** — auditor **genérico** (roda em QUALQUER atividade). (a) **Compatibilidade** p/ navegador antigo (JS moderno, emoji que quebra ≥Unicode 7.0 vs. cosmético FE0F/ZWJ, `-webkit-`, `onclick` órfão — ignora conteúdo de strings E comentários p/ não dar falso positivo). (b) **Checklist de recursos** (reset55, adaptativo Extra/Reforço, relatório, narração, som, níveis, medalhas, conquistas, streak). `--matriz` = raio-x de várias; **`--exigir` = BARRA atividade NOVA que nasça sem recurso OBRIGATÓRIO** (reset, Extra+Reforço, relatório, níveis, medalhas, conquistas). **Só usar `--exigir` em atividade NOVA** — as antigas ficam como estão.
- **`_circo/testar-headless.py <html> [...]`** — teste headless de CARGA: injeta um capturador (`window.onerror`) numa cópia da página e lê o DOM final (`--dump-dom`) p/ pegar **erro de JS na abertura** + print da 1ª tela. (Lição paga: o Chromium headless novo **não** joga erro de JS no stderr — ler stderr era CEGO; sempre validar o próprio testador com um HTML propositalmente quebrado.)
- **`_circo/testar-jogando.py <html> [...]`** — **O TESTADOR (auto-playthrough).** Injeta um "robô" que JOGA sozinho (preenche nome, clica Começar, entra nas paradas, responde, avança) enquanto captura **erro de JS em QUALQUER tela** — pega o bug que só aparece no MEIO do jogo (ex.: a parada 7 quebra), que o teste de carga não vê. Cérebro do robô: prioriza avançar/entrar/responder, **evita voltar/menu**, e **não repete** o mesmo clique (senão faz loop). Filtra rejeições benignas do headless (tela cheia `requestFullscreen`, autoplay de áudio) que **não** são bug. Lições pagas: (1) `window.onerror` grava numa `<div id="__drvout">` lida via `--dump-dom` — mas ler o DOM todo dá falso positivo (o próprio script tem `[ERR]` no fonte), então ler SÓ a caixinha; (2) `--virtual-time-budget` alto p/ os `setTimeout` do robô rodarem rápido; (3) profundidade varia por estrutura — vai fundo em clones da base-mãe (alvo), raso em atividades de estrutura antiga. SEMPRE validar com um erro injetado no meio do jogo.

### PASSES DE REVISÃO no rito (2 "chapéus" novos — sem virar ferramenta pesada)
Na FASE 3, além do QA técnico, aplicar SEMPRE dois olhares de revisão (o usuário decide onde há julgamento):
- **✍️ REVISOR de Português:** ler TODO texto visível/falado — ortografia, concordância (n=1!), clareza do enunciado, e **tom por idade** (linguagem do Pré ≠ do 9º). Um errinho de português mina a confiança premium.
- **🎧 REVISOR de NARRAÇÃO ("o ouvido") — chapéu novo:** o Testador e o Auditor **NÃO OUVEM** — só pegam crash/compat. **Pronúncia é passo HUMANO.** Toda palavra que a voz TTS enrola vira uma entrada no **DICIONÁRIO DE PRONÚNCIA** (a lista de troca-pra-falar em `limparFala()`: `cor→côr`, `cores→côres`, `Teo→Téu`, e assim por diante). **Regra "vira barreira" aplicada à voz:** palavra errou uma vez → entra no dicionário UMA vez → fica certa **pra sempre, em toda atividade** (a base-mãe carrega o dicionário). LIMITE HONESTO: a IU **não escuta o áudio** de fato — ela **revisa o texto, conhece os vícios comuns do TTS pt-BR e PROPÕE a grafia**, mas quem confirma "soou certo?" é o **ouvido do Marcos** (automatizar pronúncia não vale: cada PC tem voz diferente; o que soa aqui ≠ o da escola). Ex. pendente: **"sombra"** (soa ora certo, ora não) → candidata a entrar no dicionário, com o Marcos testando a grafia.
- **♿ ACESSIBILIDADE:** contraste suficiente; **nunca só cor** p/ indicar certo/errado (criança daltônica); fonte legível (amigável a dislexia); alvos de toque grandes; funciona no teclado. Escola pública = inclusão é regra.
- **BASE-MÃE oficial = template do Circo** (`_circo/index-template.html` + `build.py`): subir a base = subir toda atividade futura (todas são clones dela). O checklist do `--exigir` reflete o que a base-mãe já entrega pronto.
- **⚠️ LIMITE HONESTO das ferramentas (não prometer demais):** Auditor + Testador pegam **crash (erro de JS)**, **compatibilidade** e — desde o check novo — **popup/overlay preso** (o Testador força uma subida de nível e confere se sobrou popup visível). AINDA **não** pegam **pronúncia**, **pedagogia**, nem outros bugs **visuais** (cor errada, layout torto, animação estranha) — esses precisam de **olho/ouvido humano**. Nunca dizer que o Testador garante "sem erros"; ele garante "sem crash, compatível e sem popup preso". **Todo bug concreto novo → virar um CHECK dirigido** (regra "vira barreira"): quando dá pra reproduzir, escrever um teste que dispara e confere o comportamento — e **validar o check nos dois sentidos** (pega o caso quebrado E aprova os sãos, sem falso-positivo).
- **💥 LIÇÃO PAGA — popup/overlay que fica PRESO na tela:** NUNCA apagar um popup comparando `innerHTML===html` — o navegador **re-serializa** o conteúdo (principalmente **SVG**: muda aspas/ordem de atributos), então a comparação **nunca bate** e o popup nunca some. Usar um **contador/token** (`var _popSeq; var meu=++_popSeq; setTimeout(...,se meu===_popSeq apaga)`). Verificação headless: disparar o popup, esperar passar a duração, conferir que a zona ficou vazia (antiga=PRESO, corrigida=LIMPOU). Achado na `climas-do-mundo-6ano`; era único dela.

### POLÍTICA DE AUDITORIA — "todo erro vira barreira" (pedido do usuário, facilitar o trabalho dele)
1. **Toda classe de erro que aparecer UMA vez vira um CHECK no `auditar.py` que REPROVA** — não pode voltar a acontecer. Já embutidos: tokens não resolvidos, JS inválido, JS moderno proibido, funções duplicadas, var acentuada, concordância (1+feminino, artigo/gênero), CSS moderno, keyframes pareados, onclick órfão, cenário/ilha, **nome da parada (mapa×título, check 11)**, **emoji moderno >Unicode 6.0 incl. entidades `&#N;` (check 12)**. Ao descobrir um novo tipo de bug, ADICIONAR o check ANTES de fechar.
2. **NUNCA publicar com FALHA.** `auditar.py` REPROVADO = não sobe. Aviso = revisar.
3. **Correção AUTOMÁTICA só quando o certo é ÚNICO e determinístico** (ex.: emoji fora de compat → trocar por equivalente ≤6.0; `-webkit-` faltando; token trocado). Nesses casos EU corrijo sozinho e sigo — não devolvo pro usuário.
4. **Onde há JULGAMENTO/conteúdo (qual nome é o certo, qual imagem, qual redação) — NÃO inventar: PERGUNTAR** (curto e objetivo). A auditoria BARRA; a decisão do "certo" é do usuário quando não é determinístico. Isso mantém o "não inventar" intacto e ainda facilita, porque o quebrado nunca chega a publicar.

### AUDITORIA PEDAGÓGICA — vestir o PROFESSOR/PEDAGOGO experiente da disciplina (2 trilhos)
A auditoria tem DOIS trilhos: (a) **técnico/erros** (acima — barra e auto-corrige o determinístico) e (b) **pedagógico** (julgamento — NÃO auto-corrige; AVISA + SUGERE, o usuário decide).
- **Vestir o especialista da disciplina/ano** (ex.: prof. de Matemática do 5º, alfabetizador do Pré) com muita experiência, e **consultar a BNCC**: as habilidades/objetos daquele ano batem com o conteúdo? O nível cognitivo é adequado à idade? A progressão faz sentido (concreto→abstrato)? O enunciado ensina sem confundir? Contextualiza? A explicação do erro é o motivo VERDADEIRO?
- **Se achar algo pedagógico, NÃO passar batido e NÃO corrigir sozinho:** AVISAR o usuário com (1) o que notei, (2) POR QUE (embasado — BNCC/didática), (3) SUGESTÕES concretas de melhoria, e deixar ELE DECIDIR. Agir como consultor pedagógico, não como dono do conteúdo.
- Se não tiver certeza de uma habilidade BNCC específica (código EI/EF), dizer que vai confirmar / perguntar — nunca afirmar de cabeça como se fosse certo.
- Diferença-chave: **erro técnico = barra/auto-corrige; questão pedagógica = aconselha e o usuário decide.** Silêncio pedagógico é falha; decidir conteúdo sozinho também.

**FASE 4 — Publicar em BLOCOS (não peça por peça).** Juntar 3–4 features → 1 build → 1 QA → 1 deploy. Publicar a atividade (repo próprio, 1 HTML), **adicionar o card no TOPO da turma no hub** (mascote da própria atividade) e confirmar os builds (`status=built`).

**Meta:** muito preciso, sem erros, e MAIS RÁPIDO que a 1ª vez — o ganho vem de (a) clonar o núcleo pronto, (b) gerar as imagens em lote no começo, (c) publicar em blocos.

================================================================
## COMO USAR ESTE MANUAL (leia primeiro)
================================================================
- O **ATIVIDADE-PREMIUM.md** diz o FORMATO EXATO da atividade (telas, botões, fluxo, comemoração) — é o molde.
- Este **MANUAL MESTRE** diz O QUE fazer e COMO agir: regras de compatibilidade, pedagogia, imagens, narração, gamificação, o fluxo de trabalho com o Marcos e a validação.
- Toda atividade entregue é **PREMIUM por padrão** — nunca uma versão "básica". Premium é o piso, não o extra.
- Ao iniciar, identifique o CENÁRIO (A: transformar um arquivo existente; B: criar do zero) e siga o fluxo correspondente (ver seção 2).
- Antes de entregar, rodar a VALIDAÇÃO (seção 13), DE VERDADE (executando, não de memória), e relatar honestamente o que ficou pendente.

================================================================
## 1. CONTEXTO E OBJETIVO
================================================================
- Público: escola pública, pré-escola ao 6º ano. Disciplinas: Português, Matemática, Inglês, Ciências.
- Entrega: arquivo único `index.html`, publicado via Claude Code → GitHub Pages → link no Invertexto.
- Cada atividade é gamificada: mascote, fases, narração, visual premium, história conectada.
- A atividade digital é UMA peça de uma sequência didática maior — não substitui manipulação física, interação social ou situações do cotidiano. Brilha como prática gamificada, individualizada, de reforço.

**Fluxo de trabalho:**
Marcos descreve o tema → Claude monta estrutura com prompts de imagem prontos → Marcos gera cartelas no ChatGPT e envia → Claude recorta (PIL), valida e entrega o `index.html` final → Marcos publica via Claude Code.

================================================================
## 2. FLUXO DE TRABALHO — OS DOIS CENÁRIOS
================================================================
Toda atividade é PREMIUM por padrão. O checklist premium (seção 3 do ATIVIDADE-PREMIUM.md e as regras deste manual) é OBRIGATÓRIO nos DOIS cenários. Não existe "premium parcial": uma atividade só está pronta quando TODOS os itens existem e funcionam de verdade (conferidos rodando). Se algo obrigatório não puder ser feito na conversa (ex.: falta uma cartela que só o Marcos gera), APONTAR a pendência com honestidade — nunca entregar como completo.

### CENÁRIO A — TRANSFORMAR uma atividade existente (Marcos anexa um arquivo)
Gatilho: Marcos anexa um `index.html` (ou cola código) e pede "deixar premium", "melhorar", "igual à Floresta dos Números", etc.
1. **Leia o arquivo inteiro antes de mudar nada.** Mapeie fases, mecânicas, vocabulário, mascote, tema, o que já é premium e o que falta.
2. **NÃO altere o conteúdo pedagógico** (vocabulário, desafios, ordem das fases) a menos que Marcos peça. A transformação premium é sobre a CAMADA (visual, história, mapa, narração, gamificação, correções), não sobre trocar as palavras/desafios. Achou um problema real de conteúdo? APONTE e PERGUNTE antes de mexer.
3. **Verifique o que é RENDERIZADO na tela, não só o array-fonte.** Ex.: `figura()` resolve a imagem pela PALAVRA (dicionário IMG sem acento); o emoji do array é só fallback. Não "corrija" incoerências que só existem no código-fonte mas não aparecem para a criança.
4. **AUDITORIA DE LACUNAS** logo no início: percorrer o checklist premium item por item contra o arquivo e listar o que falta/está incompleto/ainda em SVG-ou-emoji. TODO item obrigatório em falta DEVE ser completado — "melhorar/deixar premium" já significa cumprir o checklist inteiro. Itens que dependem de cartela do Marcos ficam com fallback temporário e são apontados como pendência.
5. **Valide** (seção 13) e entregue como `index.html`. Relate o cumprido e o pendente.

**Erros a NÃO repetir (lições pagas):**
- Ao recortar/colar arrays JS, SEMPRE incluir a linha `var d=[];` adjacente — esquecê-la quebra a inicialização (`d is not defined`).
- Não trocar vocabulário "para tirar repetição" sem confirmar — repetição entre fases normais pode ser intencional (o alvo costuma ser outro, ex.: Desafio Extra fixo).
- Conferir funções duplicadas (`grep -c "function nome("` deve ser 1) — a última definição sobrescreve silenciosamente.

### CENÁRIO B — CRIAR do zero (Marcos descreve tema/série/disciplina)
Gatilho: Marcos descreve tema, série e disciplina SEM anexar arquivo.
1. **Já nasce premium — checklist inteiro.** Não entregue "básico" para melhorar depois. A primeira entrega já cumpre tudo: mapa-aventura vivo com história narrada (início/meio/fim), mascote, emblemas de nível sempre visíveis, gamificação, streak, jogos de alívio, apoio ao erro por contagem acesa (fases de contar), narração automática tratada, concordância (n=1).
2. **Defina a identidade** com Marcos (1 pergunta só, se necessário): tema visual + mascote + série/disciplina.
3. **Monte a estrutura** pelo catálogo de mecânicas (seção 10), calibrada para a idade (seção 5).
4. **Gere os prompts de imagem** (cartelas ChatGPT) numa página HTML com botão "Copiar", uma cartela por vez.
5. **Integre** as cartelas recortadas (PIL), valide e entregue como `index.html`.

================================================================
## 3. COMPATIBILIDADE — REQUISITO SAGRADO (Firefox 106 / Chrome antigo)
================================================================

### JavaScript — PROIBIDO:
- Arrow functions (`=>`), `let`/`const`, template literals (crase), optional chaining (`?.`), nullish (`??`), `async`/`await`, spread (`...`), lookbehind (`(?<=`).
- `forEach` quando puder usar `for` clássico.
- **Usar sempre:** `var`, `function`, `for` clássico.
- **Nunca** acento/cedilha em nome de variável (`cacaPos` sim, `caçaPos` não). Acento em texto/string é OK.
- Validar: `new Function('"use strict";'+js)` deve passar sem erros.

### CSS — PROIBIDO:
- `grid`, `gap`, `clamp()`, `var(--)`.
- Flexbox **sempre** com fallback: `display:-webkit-box` (+ `-webkit-box-pack`, `-webkit-box-align`, `-webkit-box-orient`) antes de `display:flex`; `-webkit-box-flex` explícito nos filhos.
- **Toda animação** precisa do par `-webkit-`: `@-webkit-keyframes` + `@keyframes` e `-webkit-animation` + `animation`. Animar só `transform` e `opacity`.
- `radial-gradient`, `linear-gradient` e `drop-shadow` sempre com versão `-webkit-` antes.

### Emojis:
- Apenas Unicode 6.0 (2010) são seguros. Emojis 2014+ viram quadradinho vazio.
- Seguros já validados: ⭐ ✨ 🌟 💫 🎉 🔊 ▶ ✏ 🔒 🔓 🔁 🔄 🚀 🏁 📊 🏅 ✓ ✔ ✗ ➜ ✦ 🏆 💡 🔥 📋 📖 🔍 👀 👍.
- PROIBIDOS (quebram): 🗺 (7.0), 🤔 (2012), 🏅→ok mas 🥇🥈🥉 não, **bandeiras** (🇧🇷🇺🇸 viram letras "BR"/"US"), 🦊🦉🦋🦝🦔🦅🐺🦁🐿🪐☄🛸🧺🥕🥇🥈🥉🤩🥳 e qualquer 2014+. REMOVER variation selectors (FE0F).
- Para personagens, animais e ícones-chave: **imagem PNG** (garante 100%) ou SVG inline; nunca emoji.

### Assets:
- Imagens: base64 embutidas no HTML.
- Ícones de interface: SVG inline (que mudam de cor/estado).
- Áudio: Web Audio API.
- **SONS DE EFEITO sintetizados com Web Audio (lição paga):** para o "gostinho de jogo" (som de moeda ao acertar, "pop" ao encaixar, tom gentil ao errar, arpejo ao subir de nível, fanfarra ao concluir fase), SINTETIZAR os sons na hora com osciladores (`AudioContext` + `OscillatorNode` + `GainNode` com envelope rápido) — NÃO embutir arquivos de áudio (pesam MB). É leve (poucos KB de código), funciona em navegador antigo e não depende de baixar nada. Motor `tocarSom(nome)` com um `AudioContext` único; o contexto começa "suspenso" e só toca após o 1º gesto do usuário (regra de autoplay) — `resume()` no primeiro clique. Flag para poder desligar; volume discreto (~0.15).
- Narração: `speechSynthesis` pt-BR (só narra se houver voz pt-BR real instalada).
- `localStorage` funciona em GitHub Pages; usar variáveis em memória como fallback.
- **DURAÇÃO-ALVO ≥ 40 min (pedido do Marcos — aula tem 55 min):** a atividade premium precisa ter
  **conteúdo suficiente pra ocupar no MÍNIMO 40 minutos** de uma criança de 6º ano (sobra folga
  pros 55 do reset). Como garantir sem ficar monótono: **8+ ilhas/paradas** × ~5-6 desafios, **+ os
  mini-jogos** (memória, climograma, mapa, ligar, caça, forca, experimento) intercalados, **+
  narração** (o mascote falando some tempo), **+ adaptativo** (Extra estende quem vai bem, Reforço
  repete quem erra). Estimar antes de fechar: nº de telas × ~40-60s. Se der < 40 min, ADICIONAR
  paradas/desafios; se passar de ~55, cuidar da monotonia (sortear 6 de N por fase). Conferir o
  volume real, não de memória.
- **PROGRESSO EXPIRA EM 1 AULA — padrão de escola (pedido do usuário):** o "continuar de onde
  parou" vale só durante a aula; depois **zera sozinho**, pra a PRÓXIMA TURMA começar do zero SEM
  o professor resetar cada PC. ⚠️ *(A 1ª tentativa — relógio `ESTADO.inicio` de janela FIXA +
  `setInterval` — foi **abandonada**; o método correto e único é o **carimbo deslizante** logo
  abaixo.)*
- **🔒 OBRIGATÓRIO EM TODA ATIVIDADE PREMIUM — e TEM QUE FUNCIONAR (pedido do Marcos, jul/2026):**
  **nenhuma atividade premium sobe sem o reset de aula, e ele precisa ser TESTADO funcionando**
  (não basta ter o código: rodar os 3 cenários abaixo em node/headless antes de publicar). O
  auditor cobra isso no checklist (`reset55`); atividade nova sem reset é **BARRADA** por
  `--exigir`. É o padrão da escola: a próxima turma começa do zero **sem o professor zerar PC a PC**.
- **✅ JEITO CERTO — ÚNICO método aceito (canônico, jul/2026): carimbo DENTRO do progresso +
  expiração DESLIZANTE.** Os métodos antigos (relógio `ESTADO.inicio` de janela FIXA, e o
  retrofit `__aulaInicio` com `localStorage.clear()`+`reload()`) **falharam na prática** (na
  Floresta continuava aparecendo "Começar do zero" dias depois) e estão **APOSENTADOS — não usar
  mais, nem em retrofit**. O jeito robusto e simples:
  1. gravar `t: (new Date()).getTime()` **dentro do próprio objeto de progresso** no `salvar()`
     (renovado a CADA ação → nunca expira durante a aula ativa);
  2. no `carregar()`, logo após o `JSON.parse`, `if(!d.t || (agora-d.t) > VALIDADE_MIN*60000){
     remove a chave; return false/return; }` **antes** de popular os globais;
  3. helper `agoraMs(){ try{ return (new Date()).getTime(); }catch(e){ return 0; } }` (compat IE)
     e a constante `var VALIDADE_MIN=70;` (55 da aula + 15 de folga, fácil de mudar).
  Assim: mesma aula/aluno saiu sem querer → **Continuar**; outra aula/outro dia (ou dado antigo
  SEM carimbo) → **expira e abre no campo do nome**, sem zerar PC a PC. Vantagens vs. os antigos:
  **1 só chave** (não dessincroniza), **deslizante** (não corta no meio da aula), **sem `clear()`
  global nem `reload()`**. `apagarProgresso()`/"Começar do zero" seguem limpando a chave.
  **Já aplicado e testado em:** `floresta-dos-numeros-1ano` (raiz) e `climas-do-mundo-6ano`.
- **RETROFIT em atividade JÁ publicada = o MESMO patch canônico** (não o `__aulaInicio`!):
  achar `salvar()`/`carregar()` (ou o `localStorage.setItem/getItem` do progresso) e aplicar os
  3 passos acima na chave própria de cada jogo (ex.: `climasNino`, `aventuraespaco`). Se o HTML
  tiver o script velho `__aulaInicio` logo após `<body>`, **removê-lo** (ele dá `clear()`+`reload()`
  e briga com o carimbo). Pipeline por atividade: pegar o HTML vivo (`recuperar.yml` → `_recuperado/`)
  ou editar em `_lote/<repo>/index.html` → **validar** (`node --check` do JS + os 3 cenários) →
  **QA** (`testar-jogando.py` 0 erro + `auditar-geral.py` APROVADO) → commit → `atualizar.yml`
  (`source_dir=_lote/<repo>`). Como cada atividade é **1 HTML único autossuficiente**, o
  `atualizar` espelha só o `index.html` sem perder nada. **Não mexer** onde já há relógio nativo
  funcionando (ex.: circo-do-teo).
- **TESTE OBRIGATÓRIO do reset (3 cenários, em node com `localStorage`/`Date` mockados) — só
  publicar se os 3 passarem:** (1) **mesma aula** (salvou, "recarregou" a RAM, `carregar()` <70min)
  → volta com nome+pontos = **Continuar**; (2) **pausa curta no meio da aula** (ex.: +10min) →
  ainda **Continuar**; (3) **próxima aula / outro dia** (+71min) → nome vazio, pontos 0, chave
  **limpa** = **abre no campo do nome**. Guardar os prints do teste.
- Sem overflow horizontal em 414/390/360/320px.

================================================================
## 4. VISUAL PREMIUM (identidade de qualidade)
================================================================
- Fundo gradiente temático + orbes/luzes flutuando (animados, par `-webkit-`).
- Topbar com efeito vidro/brilho; cards profundos com sombra e animação de surgimento (`cardSurge`).
- Transições só com `transform`/`opacity`.
- Mascote com 4 poses (feliz/explicando/comemorando/pensando) em balão de fala.
- Barra de XP, níveis, medalhas douradas, conquistas, streak.
- **Preferir tema ESCURO bonito** com bom contraste. Ex. floresta noturna: `#14402a / #0d2c1d / #071a11` com brilho de vaga-lume; card `#1a4030/#112c20` com borda glow `rgba(150,240,180)`; textos claros `#eafff2 / #cdeeda / #9fd9b5`; títulos `#aef0c8`; destaque dourado `#ffe27a / #ffd23f`.
- **Contraste sempre auditado:** nenhum texto pode "sumir". Nomes/rótulos sobre o mapa: cor sólida legível (ex.: nomes de ilha em preto sólido `color:#000; text-shadow:none` sobre mapa claro).
- **Bem infantil e fofinho:** cantos arredondados, botões "gordinhos" com sombra, cores vivas, animações suaves.
- **Botões importantes pulsam e brilham** (classe `pulsa` = pulso suave de escala) para guiar o aluno. NUNCA salto/pulinho/brilho piscando (o modelo não tem — ver seção 9 do ATIVIDADE-PREMIUM.md).
- Testar responsivo: 414/390/360/320px — nada vaza da borda.
- **ELEMENTOS ANIMADOS DE FUNDO — POUCOS E DISCRETOS (lição paga):** dá pra dar vida ao cenário com elementos temáticos cruzando o fundo (ex.: 2-3 peixinhos nadando lento atrás do conteúdo), reusando imagens já embutidas — mas com PARCIMÔNIA. O fundo é onde a criança lê enunciados e arrasta itens; se ficar movimentado demais, compete pela atenção (pré-escola). Regra: poucos (2-3), bem TRANSLÚCIDOS (opacity ~0.12), LENTOS (26-40s pra cruzar), sempre ATRÁS do conteúdo (`z-index` baixo), sem vazar a borda (`overflow:hidden`). Animar só `transform` (par `-webkit-`). Vida sutil, nunca "puxar o olho".

================================================================
## 5. HISTÓRIA, ENGAJAMENTO E MAPA-AVENTURA VIVO
================================================================

### História/Missão
- Uma **narrativa RICA** conecta todas as fases (não fases soltas). Ex.: mascote precisa recuperar algo perdido; a criança ajuda fase a fase; no fim salva o mundo e vira herói. Com **FINAL SUPER FANTÁSTICO** que fecha o enredo de forma emocionante.
- **Coerência total de tema:** mascote, ilhas/cenários, companheiros, emblemas, troféu, recompensa — TUDO tem a ver com a mesma história. Nada solto fora do enredo.
- Cada fase tem **fechamento caloroso que puxa pra frente** — o mascote provoca a próxima como gancho de história (objeto `GANCHOS={fase:"teasa o próximo lugar"}` + `ganchoDe(ch)`), num balão do mascote E narrado. Nunca um "próximo" seco.

### Mapa-Aventura Vivo (padrão premium — default de toda atividade)
- Caminho serpenteante; cada fase é um **"lugar"** com cenário próprio (imagem) + personagem companheiro ao lado (1 por fase). ~8 cenários cobrem ~12-15 fases, intercalando.
- **Parada atual:** destaque com glow `drop-shadow` pulsando (**NUNCA `box-shadow`** — desenha um quadrado ao redor do PNG recortado; usar `filter:drop-shadow` com par `-webkit-filter`, seguindo o contorno real do alpha). Tag "você está aqui!". Clicável.
- **Paradas concluídas:** "Concluída ✓", trecho dourado. Clicáveis (rejogar).
- **Paradas não jogadas: TRANCADAS** — acinzentadas (`grayscale`) + cadeado 🔒, clique bloqueado com aviso carinhoso. Cada parada abre quando a ANTERIOR é concluída.
- **Conector pontilhado** entre cada parada (dourado forte nos trechos concluídos).
- **Recompensa que cresce** (ex.: cesta/árvore em 3 tamanhos por % de progresso) como IMAGEM, no topo do mapa. Logo abaixo, **barra de progresso** que enche por % + contador "X de N paradas" (concordância: "1 parada"/"2 paradas"). A recompensa dá o lúdico; a barra dá a precisão fase a fase.
  - **Como foi feito (circo em 3 fases):** pedir ao ChatGPT UMA cartela com o MESMO objeto/cena em 3 fases lado a lado (vazio → meio montado → completo), mesmo ângulo/tamanho, fundo branco, bem separadas. Recortar por VÃOS BRANCOS verticais (contar pixels não-brancos por coluna; runs de coluna quase-vazia = separador) → 3 recortes; transparência por flood-fill do branco das bordas (mantém o branco INTERNO, ex. listras da tenda). Escolher a fase por `feitas/N`: `<1/3`→fase1, `<2/3`→fase2, senão fase3. Legenda muda junto ("Vamos montar…"/"…ficando pronto"/"…pronto!"). Imagem com `filter:drop-shadow` + `@keyframes flutua` (nunca `box-shadow`, que faz quadrado no PNG recortado).
- **Troféu** (imagem) no fim da trilha: visível desde o início (esmaecido + 🔒 até concluir tudo); ao completar, pulsa/flutua e abre o grande final. Nome legível embaixo.
- **Personalização:** se o aluno digitou o nome, exibir no mapa ("A aventura de [Nome]!") e mascote chama pelo nome; cair para texto padrão se não houver.
- **Narração do mapa (`narrarMapa()`, automática):** conta a HISTÓRIA em 3 momentos ligados ao enredo — INÍCIO (apresenta e convida), MEIO (progresso DENTRO do enredo: o que já recuperou, o que falta), FIM (comemora o desfecho e aponta o troféu). Botão 🔊 reconta. Auditar concordância n=1 no enredo.
- Botões extras EMBAIXO (depois da trilha e do troféu): "Minhas Medalhas" (sempre), "Treinar Erros (N)" (só se N>0), "Relatório" (só quando TUDO concluído). NÃO existe botão "Continuar aventura" — a criança clica direto na ilha atual.

### Engajamento saudável ("enganchar em ESTUDAR", nunca vício)
Meta: a criança querer voltar para **aprender**, pela sensação de competência e progresso, **nunca** por compulsão. Evitar: "mais um sem fim", recompensa aleatória (caça-níquel), FOMO.
1. **Elogio variado** — pool de ~10 frases calorosas; nunca repetir seguido (10 acertos ≈ 10 frases diferentes).
2. **Curiosidades "Uau"** — 1 por fase, na tela de fim de fase, narrada.
3. **Gancho narrativo** — no fim de cada fase o mascote provoca a próxima como história.
4. **Deleite ligado ao mérito** — reações atreladas à conquista; nunca por sorte.
5. **Streak** — acertos seguidos disparam pop em 3/5/8/10 com a frase COMPLETA "Você acertou N seguidas!" + reforço variado (a criança pequena não entende "3 seguidas!" solto). `registrarStreak(acertou)` incrementa no acerto e ZERA no erro; resetar `streak=0` ao iniciar cada fase. É mérito puro, nunca sorte.

================================================================
## 6. PEDAGOGIA — PRINCÍPIOS
================================================================

**PROGRESSÃO:** concreto → abstrato, simples → complexo, em espiral. Intercalar fases de carga alta com alívio lúdico (jogos), respeitando a atenção curta.

**CONCRETO (Piaget):** a criança pensa com o corpo/objetos. Ilustrar para contar. Reduzir números abstratos altos. Manipulação real (arrastar, juntar, ver o resultado se formar) é o que falta na maioria das atividades digitais.

**ILUSTRAR A SITUAÇÃO, NUNCA A RESPOSTA:**
- Pode ilustrar onde a criança conta/soma (mostra objetos, ela conta).
- NÃO ilustrar onde a imagem entrega a resposta (ex.: "qual é o número 3?" ou comparação onde só de ver já se sabe). Não pôr rótulo do número no grupo.
- Comparações "maior/menor": mostrar grupos de objetos; separador "ou" (não "+"). Somas: separador "+".

**FALA/NARRAÇÃO NÃO ENTREGA RESPOSTA:** a narração da pergunta lê **só o enunciado**. A explicação/resposta só é narrada **depois** que a criança responde (luta produtiva). Auditoria: qualquer `fala` cujo texto depois do último "?" seja afirmação declarativa está entregando a resposta — bug, cortar. A resposta vai **só** em `dd.explica`, narrada após a resposta.

**EMBARALHAR AS OPÇÕES (resposta nunca na mesma posição):** embaralhar **uma vez** por questão, dentro do render, com flag para não reembaralhar:
```javascript
if(dd && !dd._mix){
  dd._mix=true;
  if(dd.opcoes && dd.opcoes.length>1){ dd.opcoes=embaralhar(dd.opcoes.slice()); }
  if(dd.opcoesImg && dd.opcoesImg.length>1){ dd.opcoesImg=embaralhar(dd.opcoesImg.slice()); }
}
```
Seguro porque a verificação compara por **valor** (`dd.opcoes[idx]===dd.certa`), não por índice. Aplicar também no Desafio Extra. Auditar rodando 2-3 vezes: a posição da certa deve MUDAR.

**LINGUAGEM/CLAREZA:** opções como "Grupo de 7" (NUNCA "O de 7" — o "O" parece zero). Nomes da resposta não aparecem em exercícios de identificação.

**APRENDIZAGEM SIGNIFICATIVA (Ausubel):** conectar com a vida real ("Eu Pesquisador" com perguntas de reflexão, `aceitaAmbas:true`, sem certo/errado).

**ZDP (Vygotsky) — ADAPTATIVIDADE:**
- 100% de acertos → **Desafio Extra** opcional, coerente com a fase (mesma habilidade, um degrau acima; NUNCA um extra fixo igual em todas). Embaralhar opções do Extra.
- **O DESAFIO EXTRA TEM CÓDIGO PRÓPRIO — ao corrigir uma fase, corrigir TAMBÉM o extra dela (lição paga):** o `desafioExtra(fase)` define seus próprios `pede`/`opcoes`/gênero/imagens, separados das rodadas normais. Um bug de concordância ou de imagem faltando pode estar corrigido nas rodadas normais mas PERSISTIR no extra (sintoma real: "peixinho roxa" e um peixe em SVG só apareciam no Desafio Extra, que só surge com 100% de acerto — por isso o bug parecia intermitente). Ao consertar/auditar uma fase, varrer TAMBÉM o `desafioExtra` correspondente, não só as rodadas normais.
- <50% → **Reforço** (treino dos erros) antes de seguir.
- 50-99% → nada (segue normal). Auditar os 3 casos.
- Fases-jogo (memória, caça, forca, quebra-cabeça) NÃO levam Desafio Extra.

**PRODUÇÃO / TOPO DE BLOOM:** "Monte a Conta/Frase" (ordenar partes embaralhadas), "Explique para o mascote", criação livre.

**ERRO CONSTRUTIVO (Kamii):** no erro, mostrar correção e dica, sem punir; sem sistema de vidas que pare o fluxo.

### Calibragem por idade (especialmente 1º ano)
- Evitar lacunas em frases e tarefas com muita leitura. Pares/ímpares são mais de 2º ano.
- Preferir **contagem visual concreta**: bichinhos/objetos fofos; a criança toca/arrasta. Opções = resposta + 2 vizinhos, embaralhados.
- Somas até ~10-20 (com ilustração). Dezena só como noção concreta.
- Botões grandes e redondos, animação "pulinho", narração calorosa.
- Fase complexa demais para a idade → **trocar** por uma concreta mais simples, não remendar.

### Calibragem por SÉRIE (alinhar ao currículo/BNCC)
- Cobrir o conteúdo ESPERADO da série, não só o "seguro". Ex.: dinheiro no 5º ano (EF05MA) pede **porcentagem e desconto** (50%=metade, 10%=÷10, 25%=¼) e decimais — sem isso o teto fica em 4º ano. "Está adequado mas seguro demais para a série?" é sinal de que falta um degrau.
- O conteúdo mais avançado vem como ÚLTIMA parada de conteúdo antes dos bônus.
- Variar o ENUNCIADO dentro da fase (3-4 formas equivalentes por `i%`), para não repetir "Quanto vale?" 10x.

### Dose certa (atenção da idade — NÃO cansar)
- **~5-6 desafios por fase** (NÃO 10). 10×muitas fases = >1h, monótono. Limitar em `iniciarFase`: se >6, SORTEAR 6 (`embaralhar(todos).slice(0,6)`) — some o excesso e a fase muda a cada rejogada. Resetar `_mix=false` nos sorteados.
- **Variar a AÇÃO, não só o enunciado.** Intercalar **jogos de alívio** (memória, quebra-cabeça, caça-palavras) no MEIO (ex.: memória após a 6ª parada, quebra-cabeça após a 9ª).
- **Menos digitação livre** (gera erro de digitação, não de raciocínio). Equilibrar com toque/escolha.

### Apoio ao erro (correção com contagem — fases concretas)
Obrigatório em TODA fase de contar quantidade:
1. Mascote fala **"Não foi dessa vez! Agora vamos contar juntos, bem devagar."** (com carinho, sem punir).
2. Quando essa frase de abertura TERMINA (callback do `falar`), uma pausa curta e começa a contagem sincronizada.
3. **ACENDE cada objeto UM POR UM, EM SINCRONIA COM A FALA** — a luz do objeto k acende JUNTO com a voz dizendo o número k; classe que dá SÓ glow via `filter:drop-shadow`, **SEM `transform:scale`** (aumentar o objeto some com a referência de tamanho/posição). Ex.: `.obj-item.sel .obj-img`.
4. Todos contados: **"São N ao todo! Agora toque no número N."** e apaga.
- **A FALA COMANDA A LUZ — NÃO dois relógios separados (lição paga, crítica):** a versão antiga acendia a luz por `setTimeout` de ritmo FIXO (850ms) enquanto a fala corria numa fila com ritmo próprio — os dois se DESENCONTRAVAM (a luz acendia adiantada ou atrasada em relação à voz). Correto: encadear pela fala. `contarPasso(k, n)`: acende a luz do objeto k, chama `falar(numExt(k+1), callback)`, e SÓ no callback (quando a voz termina aquele número) faz uma pausa de ~260ms e chama `contarPasso(k+1, n)`. Assim a luz acende exatamente quando a voz diz o número, no ritmo natural e pausado da fala. Garantir que TODAS as luzes estão apagadas durante a frase de abertura (nenhuma acende antes de começar a contar). O `falar` com callback já degrada sem voz (dispara o callback por tempo estimado), então não trava em PC sem TTS. Cada objeto tem `id` próprio (`cItem0`, `cItem1`...). Números por extenso via `numExt(n)` (que evita o TTS ler o dígito "1" como "um" masculino) — e ACENTUADOS ("três", não "tres", senão o TTS erra a tônica).

### Checklist de qualidade de conteúdo
1. **Coerência texto-imagem:** enunciado nomeia o MESMO objeto que a ilustração desenha.
2. **Opções íntegras:** cada alternativa é palavra/valor coerente ("felizmente", nunca "feliz mente").
3. **Explicações honestas:** ao acertar, o motivo VERDADEIRO (ex.: substantivo próprio → "é o nome específico de um lugar/pessoa", NÃO "leva maiúscula", que é grafia, não motivo).
4. **Sem variável crua / campo de texto livre** para séries iniciais — preferir tocar/escolher/arrastar.
5. **Instrução bate com o mecanismo:** fase por toque → "Toque", não "Arraste".
6. **Ilustração mostra a situação, não a resposta.**
7. **Narração só lê o enunciado.**

================================================================
## 7. NARRAÇÃO / VOZ (TTS) — A CRIANÇA OUVE TUDO
================================================================
A leitura usa `speechSynthesis` por padrão (leve, dinâmico). **PORÉM, pra voz NATURAL e
sempre igual** (o Web Speech sai robótico/diferente de PC a PC), agora há a opção premium de
**pré-gravar as falas fixas** com TTS natural GRÁTIS no build e embutir como base64 MP3
(ver "🔊 VOZ NATURAL PRÉ-GRAVADA" na seção de ferramentas + `gerar-audio.yml`). Regra:
falas fixas → MP3 embutido (natural); partes dinâmicas (nome/números) → Web Speech ou banco
de números pré-gravado; sempre com fallback pro `speechSynthesis` se o áudio travar.

- **`limparFala()`**: remove tags/entidades HTML; corrige espaço após `, . ! ? :`; junta espaços duplos; SEMPRE põe ponto final. Converte reticências (`…`) e pontos repetidos em vírgula (evita pausa fragmentada). **Normaliza pronúncia** de palavras sem acento que o TTS erra: "voce"→"você", "voces"→"vocês", "numero"→"número", "proxima"→"próxima", "magica"→"mágica", "divisao"→"divisão", "multiplicacao"→"multiplicação", "Poli"→"Póli" (tônica de nome de mascote), etc. (regex `\bpalavra\b/gi` preservando capitalização; adicionar palavras sempre que uma pronúncia errada for notada).

**VOGAIS FALADAS FONETICAMENTE E PAUSADAS (lição paga):** o TTS pt-BR NÃO lê o nome da letra vogal corretamente quando ela está isolada — lê o som aberto/fechado errado ou engole. Para a criança ouvir a vogal certa, escrever FONETICAMENTE na fala (tela ≠ fala): **A→"á", E→"é", I→"i", O→"ó", U→"úú"** (o U sai fraco; alongar/repetir dá mais presença). Helper `vogalFalada(letra)`. E para SOAREM PAUSADAS E DESTACADAS, cada vogal deve ser uma FRASE SEPARADA (com PONTO, não vírgula) — a vírgula dá pausa curtinha e as vogais saem emendadas; o ponto faz o `fatiarFrases` dividir e falar cada uma isolada com pausa real de ~180ms. Ex.: a lista "A, E, I, O, U" vira "á. é. i. ó. úú." na fala.
- **CUIDADO com artigos:** NUNCA converter "A"/"E" soltos globalmente (viram artigo "a"/"e" e conjunção — "a estrela" vira "á estrela", quebrando toda a fala). A regra segura no `limparFala` só converte a SEQUÊNCIA COMPLETA das 5 vogais em ordem (`\bA[,\s]+E[,\s]+I[,\s]+O[,\s]+U\b`), que nunca é uma frase normal. Vogais únicas ensinadas (acertos, "toque na vogal X") usam `vogalFalada` explicitamente no código da fase.
- **"olho" vira "óio" na fala:** o TTS tropeça no "lh" e lê "olho" como "óleo". Na tabela de pronúncia, "olho"→"óio" (o `\b` word-boundary garante que "orgulho" não é afetado). Padrão geral: toda palavra que o TTS pronuncia errado ganha uma entrada foneticamente escrita na tabela.
- **`escolherVoz()`**: melhor voz pt-BR (prioriza natural/neural/enhanced/google/microsoft/maria/francisca/luciana; cai para básica só se não houver outra).
- **Ritmo:** `rate ~0.92`, `pitch ~1.08`. Quebrar em frases (`. ! ? :`) faladas em fila com ~180ms de pausa.
- **Valores monetários por extenso:** "R$ 3,50" → "3 reais e 50 centavos"; "R$ 1,00" → "1 real"; "R$ 0,25" → "25 centavos" (o TTS lê "R$" errado — converter no limparFala).

**FALA NUNCA É CORTADA (lição paga):** o erro clássico é cada `falar()` começar com `cancel()`, então falas em sequência (elogio + streak + subir de nível + conquista) se cortavam. Padrão obrigatório com QUATRO funções:
- **`falar(txt, aoTerminar)`** — inicia narração NOVA, cancelando a anterior. Usar SÓ em troca de contexto/tela (abrir mapa, próxima parada, abrir fase). É o único que corta — de propósito, para o áudio não vazar de uma tela para outra.
- **`enfileirarFala(txt)`** — ADICIONA ao fim da fila SEM cortar. Usar quando duas falas devem ser ouvidas em sequência (elogio + streak, nível, conquista). O pop de streak/nível/conquista usa `popCaixaFila()`.
- **`falarDepois(txt)`** — se já há fala tocando, enfileira; senão fala na hora. Usado ao AVANÇAR de desafio: o próximo enunciado não corta o feedback anterior.
- **Ordem no acerto:** `feedbackAcerto()` narra elogio+explicação PRIMEIRO (via `falar`, fila limpa) e SÓ DEPOIS dispara streak/nível/conquista (que entram na fila) — tudo ouvido em ordem.
- **TELA ≠ FALA (lição paga):** `feedbackAcerto(explica, semAvancar, falaExplica)` — a TELA mostra `explica` (ex.: "começa com a vogal A") mas a FALA usa `falaExplica` quando dado (ex.: "começa com a vogal, á. á."). Serve para qualquer caso onde o que se lê difere do que se fala bem (vogais foneticas, letras, siglas). Mesmo princípio: a tela mostra a letra "U" e a fala diz "úú".
- **Proteção de fila (`_falaSeq`):** contador incrementado a cada `pararFala()`; cada frase só continua a fila se o contador não mudou (impede fila antiga voltar após troca de tela).
- **Sem voz pt-BR:** a fila roda em modo silencioso com tempo estimado por frase (nunca `onend`) — nada trava.
- **Botão "Próximo" ao acertar:** aparece IMEDIATAMENTE (a criança nunca espera), mas clicar NÃO corta o feedback — o áudio termina e emenda no próximo. Em PC sem voz, avança normal.

**⚠️ TRAVA DE ÁUDIO NO BOTÃO — APOSENTADA (jul/2026, pedido do Marcos: "agora não quero mais a trava no botão"):** padrão atual = **voz NÃO-BLOQUEANTE** (seção "DOSE DE VOZ"): botão sempre habilitado; clicar corta/emenda pela fila, nunca prende a criança. O parágrafo abaixo fica como registro histórico do padrão antigo:

~~**BOTÃO NARRADO EM TODA A ATIVIDADE, não só nos desafios (lição paga):**~~ o botão principal de CADA tela que abre com narração aparece na hora, mas começa DESABILITADO mostrando "🔊 Ouvindo..." e só habilita quando a narração termina (via callback), para a criança não pular a fala do Poli. Vale para: tela inicial (Começar/Continuar), intro de fase (Começar!), fim de fase (Próxima parada/Ver final), oferta de Extra (Aceitar), oferta de Reforço (Continuar), grande final (Ver relatório) — além dos desafios, que já tinham. Helper único: `botaoNarrado(txt, onclickAttr, extraCls)` gera o botão desabilitado + aviso; `falarComBotao(texto)` narra e libera via `liberarBotaoNarrado` (callback do `falar`), com RESERVA por tempo estimado se não houver voz pt-BR (nunca `onend`). **Cancelar o timer de liberação anterior ao criar um novo** (`clearTimeout`) — senão timers empilham ao longo das fases e podem liberar um botão de uma tela que já saiu.

- **Narração automática em TUDO:** tela inicial, mapa (história), intro de fase, cada enunciado ao abrir, feedback ao responder, fim de fase, grande final, jogos. Botão para repetir onde couber.
- **Bilíngue:** detectar idioma FRASE A FRASE (`detectaPT`) e usar a voz certa (`escolherVozPt`/`escolherVozEn`); pular a frase se não houver voz do idioma (nunca voz errada lendo o outro idioma).

================================================================
## 8. LÍNGUA PORTUGUESA IMPECÁVEL — CONCORDÂNCIA DINÂMICA
================================================================
NENHUM texto pode ter erro de português (títulos, enunciados, opções, explicações, falas, botões, relatório). Revisar TODOS antes de entregar.

Bug clássico: o dígito "1" é lido pelo TTS como "um" (masculino), então "1 palavra mágica" sai "um palavra mágica" (errado). E blocos de estatística com plural fixo ("X pontos") saem errados quando o valor é 1 ("1 acertos").

**Regra:** quando a contagem for 1, NÃO usar o dígito — usar o artigo com gênero correto por extenso + singular. Acima de 1, número + plural.
```javascript
function pluralG(n, genero, sing, plur){
  if(n===1){ return (genero==="f"?"uma ":"um ")+sing; }
  return n+" "+plur;
}
// pluralG(3,"f","palavra mágica","palavras mágicas") => "3 palavras mágicas"
// pluralG(1,"f","palavra mágica","palavras mágicas") => "uma palavra mágica"
// pluralG(1,"m","ponto","pontos") => "um ponto"
```
Manter `plural(n, sing, plur)` simples para casos sem gênero (n=1 → "1 "+sing). E `numExt(n)` ACENTUADO para contagens faladas.

- **NUNCA substantivo em plural fixo ao lado de número variável** ("1 acertos", "1 moedas", "1 pontos" são bugs REAIS já encontrados — sempre passar por `plural()`/`pluralG()`).
- **Auditoria obrigatória com n=1:** forçar 1 ponto / 1 medalha / 1 acerto / 1 parada no RELATÓRIO e no GRANDE FINAL; varrer por regex `\b1\s+(pontos|acertos|medalhas|paradas|moedas|...)`. Esses bugs só aparecem quando o valor é exatamente 1.
- **Referência de gênero:** feminino = palavra, ilha, medalha, letra, estrela, moeda, fase, cesta, parada; masculino = ponto, acerto, erro, amigo, tesouro, dia, número.
- **Valores com centavos nas falas manuais:** escrever completo ("quatro reais e setenta e cinco centavos"), nunca truncado ("quatro e setenta e cinco").
- **Falas naturais e calorosas** — ler cada fala "em voz alta" mentalmente: soa como uma pessoa querida falando com uma criança?

================================================================
## 9. ASSETS VISUAIS — IMAGENS GERADAS NO CHATGPT
================================================================
Para qualidade premium, gerar os assets-chave como **imagens 3D (estilo Pixar/última geração) no ChatGPT/Gemini**, não SVG/emoji desenhado — e o **Claude as deixa VIVAS/animadas** (ver a seção **⭐ PADRÃO 3D VIVO**). PNG/JPEG renderiza garantido em navegador antigo e fica muito mais bonito.

### 🎨 CHAPÉU NOVO — ESPECIALISTA EM PROMPTS DO POLLINATIONS (plataforma principal de imagem)

> **⭐ REGRA FIXA (pedido explícito do Marcos — NUNCA esquecer, NUNCA perder):**
> 1. **SEMPRE preferir o Pollinations — é GRÁTIS.** É o PADRÃO em tudo. O `gerar-imagens.yml`
>    já vem com `modelo=pollinations` por default. Gemini (pago) só como último recurso,
>    quando REALMENTE precisa recorte com fundo transparente e o Pollinations não entrega.
> 2. **SEMPRE tentar gerar em CARTELA** (várias peças numa folha só): o mascote em TODAS as
>    poses juntas na MESMA imagem, os companheiros juntos, os ícones juntos. Gerar em cartela
>    = mesmo estilo/proporção/luz para todas as peças (elas saem IRMÃS) e 1 chamada só.
>    Depois recorto por vãos (PIL). **Nunca gerar pose por pose separada** (sai cada uma de um
>    jeito, some a consistência — foi o erro do Nino gerado 1 a 1).
> 3. Se o Pollinations embolar a cartela (ele às vezes não segue lista longa), tentar: menos
>    peças por cartela, `enhance=true`, `seed` fixo, ou grade explícita no prompt
>    ("grade 2x3, cada quadro com uma pose, bem separadas, fundo branco"). Só depois de
>    esgotar o grátis é que se cogita o Gemini pago.

O **Claude gera imagens sozinho** via o workflow `gerar-imagens.yml` (no `main`), sem o Marcos subir nada. **Duas plataformas, estratégia de custo:**
- 🆓 **Pollinations (Flux) — GRÁTIS, sem chave, PADRÃO.** `modelo=free`. **Excelente para CENAS/paisagens/fotos de clima/texturas/UM item sozinho.** Fundo sai **escuro-degradê** (não preto liso) → **não serve pra recorte com fundo transparente**. Fraqueza: **cartela cheia de itens EMBOLA** (não segue lista longa).
- 💰 **Gemini pago (`gemini-3.1-flash-image`, ~R$0,20/imagem) — só quando precisa RECORTE limpo.** Fundo **preto liso perfeito**, segue lista de itens → **cartela de ícones/personagens recortáveis**, **enchendo o MÁXIMO de itens por cartela** (1 chamada = custo de 1). Precisa do secret `GEMINI_API_KEY` + billing com saldo (pré-pago). Erros já vistos: `free_tier=0` p/ imagem (precisa billing) e `prepayment credits depleted` (falta carregar saldo).
- **Regra de custo:** a atividade INTEIRA sai por **centavos** — quase tudo no Pollinations grátis, e no máximo 1–2 cartelas pagas (~R$0,40). Sempre preferir o grátis; pago só pro que precisa fundo transparente.

**Como pedir prompt PERFEITO no Pollinations (Flux):**
1. **Estrutura:** *[assunto claro] + [estilo] + [luz/atmosfera] + [enquadramento] + "sem texto"*. Ex.: "Foto de expedição de um deserto de dunas douradas ao entardecer, céu alaranjado, estilo ilustração 3D vibrante para crianças, sem texto."
2. **Âncora de estilo repetida** em todas as imagens do MESMO conjunto → cenas ficam consistentes (ex.: sempre "estilo ilustração 3D vibrante para crianças").
3. **Um assunto por imagem** (Flux foca melhor). Vários itens juntos → embola; se precisar vários, é cartela paga no Gemini.
4. **Params na URL** (o workflow já manda): `model=flux`, `width/height`, `nologo=true`. Dá pra testar `model=flux-3d` (3D desenho), `flux-realism` (realista), `turbo` (rápido) e `enhance=true` (um LLM melhora o prompt). `seed=N` fixa o resultado (reproduzir).
5. **Nada de fundo preto pra recorte no Pollinations** — não vem limpo. Recorte transparente = Gemini pago.
6. **Sem texto/rótulo** na imagem (Flux erra letras) — pôr "sem texto" e escrever rótulos em CSS por cima.

### 🔌 OUTRAS FERRAMENTAS GRÁTIS p/ elevar (o que dá e o que NÃO dá)
**A regra de ouro NÃO muda:** a atividade é **1 HTML único autossuficiente** que roda em **PC/navegador antigo** — então **NADA de CDN/ferramenta externa em tempo de execução** (quebraria o offline/antigo e o "self-contained"). O que dá é **usar ferramentas grátis no BUILD e EMBUTIR o resultado**:
- ✅ **Pollinations** (imagens) — feito.
- ✅ **Web Audio API** (sons sintetizados, já usado) — sem baixar arquivo.
- ✅ **Canvas** para partículas (confete, chuva/neve, faíscas) — nativo, sem lib, compat OK, mais rico que CSS puro.
- ⚠️ **Lottie** (animações vetoriais grátis do LottieFiles): premium, mas exige embutir o player (~KB) e **testar em navegador antigo** — usar com parcimônia e só se passar no compat.
- ⚠️ **Libs de animação** (GSAP/anime.js): só INLINE e se compat aprovar; em geral **CSS `transform` + `-webkit-` já entrega** sem risco.
- ❌ Qualquer coisa que **carregue de fora em runtime** (script/estilo/fonte via CDN, fetch) — proibido pelo self-contained + compat.

### 🔊 VOZ NATURAL PRÉ-GRAVADA (novo — resolve a "voz robótica do navegador")

> **⭐ REGRA FIXA (pedido explícito do Marcos — vale para TODAS as atividades, sem exceção):**
> **Toda voz da atividade é GRAVADA na voz que combinamos (Edge TTS "Antonio",
> `modelo=male` no `gerar-audio.yml`) e EMBUTIDA no HTML. ZERO voz de navegador.**
> Mecânica que garante isso (usada e PROVADA no `climas-do-mundo-6ano`) — copiar p/ toda atividade:
> 1. **`AUDIO_TXT`** = mapa `{ chave: "data:audio/mpeg;base64,…" }`, chave = `_chaveVoz(texto)`
>    (hash djb2 base36 do texto). `falar(texto)` procura a chave e toca o áudio gravado;
>    só cairia no navegador se não achasse.
> 2. **Falas DINÂMICAS** (montadas na hora: elogio+explicação, "subiu de nível X",
>    comemoração com nome) NÃO se gravam inteiras (combinações infinitas). Quebrar em
>    PEDAÇOS fixos e tocar com **`falarComposto([parte1, parte2, …])`** — cada pedaço
>    (elogio, explicação, "Quase!", nome do nível…) é gravado 1×. O que varia de verdade
>    (nome do aluno, palavra sorteada) sai só na TELA, **não no áudio**.
> 3. **`escolherVoz()` = só voz EXPLICITAMENTE masculina** (nome na lista MASC); nome
>    feminino OU genérico (ex.: "Google português do Brasil", que costuma ser feminina)
>    é RECUSADO → no pior caso fica MUDO, **nunca feminino**. (PCs da escola só têm
>    "Maria" → por isso qualquer fala não-gravada saía feminina.)
> 4. **`_circo/auditar-som.py` é OBRIGATÓRIO** antes de publicar: exige áudio embutido p/
>    toda narração fixa, todos os elogios, TODAS as explicações do banco e os cabeçalhos
>    ("Quase!", "Não foi dessa vez!"…), e dirige o grande final. Só publica com
>    **0 falas na voz do navegador**.
> 5. Voz padrão = **`modelo=male` (Edge TTS "pt-BR-AntonioNeural")**. `_lote_falas.json`
>    guarda `{id: chave, texto}` de cada fala p/ regerar quando precisar. Como capturar as
>    falas: instrumentar `falar`/`falarComposto` no headless e varrer o jogo (perguntas,
>    acertos/erros, fim de fase, grande final) OU extrair estaticamente elogios+explicações+
>    cabeçalhos do código (foi assim no climas).

Problema real (pedido do Marcos): o `speechSynthesis` (Web Speech) sai **diferente/robótico
de PC a PC** e às vezes pronuncia errado. **Solução premium:** gerar a voz NATURAL no
**build** (servidor, via Actions) e **embutir como base64** no HTML, tocando com `<audio>`/
`new Audio()` — **sem depender da voz do navegador**. Igual à estratégia das imagens.
- **Workflow:** `.github/workflows/gerar-audio.yml` (`workflow_dispatch`). Salva em
  `_audio/<nome>.mp3`. **USAR `modelo=google` → Google Translate TTS (GRÁTIS, PT-BR, FUNCIONA
  hoje — TESTADO OK)**, corta o texto em pedaços ~180 char e emenda os MP3. `modelo=free`
  (Pollinations `openai-audio`) **saiu do ar** no endpoint legado (`text.pollinations.ai`
  devolve 404 "Model not found"; a API nova pede conta) — fica no código como opção futura.
  Roda no Actions
  (internet liberada); **o sandbox do Claude tem proxy restrito e bloqueia esses hosts —
  por isso a geração é sempre server-side, nunca por curl local.**
- **Quando usar:** SEMPRE (regra fixa acima). Falas **FIXAS** (enunciados, história,
  cabeçalhos) → grava 1× e embute. Falas **DINÂMICAS** → `falarComposto` com pedaços
  gravados (ver regra fixa); o que varia de verdade (nome do aluno, número/palavra
  sorteada) fica só na TELA, nunca no áudio.
- **Vantagem:** voz idêntica e correta em qualquer PC, sem sotaque robótico; funciona
  offline (já está embutida). **Peso:** MP3 de fala curta é leve (~10–30KB); recomprimir
  p/ 24kbps mono (miniaudio+lameenc, ou `otimizar-audio.yml`) antes de embutir muitas.
- **NÃO tem fallback pra voz do navegador** (era o furo que deixava sair voz feminina):
  se por acaso faltar um áudio, `escolherVoz()` só usa voz explicitamente masculina —
  senão fica **mudo** (a informação continua visível na tela). Mudo é aceitável; voz
  feminina/robótica do navegador **não**. Por isso o `auditar-som.py` barra qualquer fala
  sem áudio embutido ANTES de publicar.

### 🔉 DOSE DE VOZ (não cansar o aluno) + PESO DO ARQUIVO

**Voz NÃO-BLOQUEANTE (regra):** a narração toca, mas **nunca trava o avanço**. O aluno
pode clicar "Próximo" a qualquer momento — o clique chama `pararFala()`, que **corta o
áudio** (o `<audio>` embutido, via `_falaAudio.pause()`, e o do navegador) e segue. Quem lê
rápido **não fica preso** esperando a voz terminar (era isso que cansava). No climas:
`_gatearAvanco()` foi neutralizada (`return null`) e `proximoDesafio()` chama `pararFala()`.
A informação continua **escrita na tela**, então ninguém perde conteúdo por não ouvir.

**Dose por FAIXA DE ANO (já implementado no climas — copiar p/ as outras):** um `var FAIXA`
controla a dose — `"peq"` (Pré–2º, ainda não leem → narra tudo, inclusive a explicação),
`"med"` (3º–5º), `"gde"` (6º–9º, leem bem → voz curta). Deriva `VOZ_EXPLICA=(FAIXA!=="gde")`:
no 6º–9º o feedback fala **só o elogio curto**; a explicação vai só pra **tela** com um botão
**🔊 (`fbExplica`/`ouvirExplica`)** pra ouvir se quiser. **Nunca** narrar o que a criança
acabou de ler.
**Controles de voz SEMPRE visíveis** (`montarControlesVoz`, canto inf. direito): **mudo**
(🔊/🔇, persiste em `localStorage`) e **repetir** (↻, reouve a última narração via
`_ultimaRepeticao`). `VOZ_MUDA` é checado em `falar`/`tocarFala` (com bypass `_forcar` p/ o
botão repetir e p/ o 🔊). **Narração automática só na 1ª vez** de cada tela
(`_telasNarradas` + `narrarTela`/guardas no mapa e nas aberturas de fase) — ao voltar não
repete, mas o botão repetir continua funcionando.

**⭐ ÁUDIO EXTERNO = PADRÃO NOVO (as atividades são SEMPRE ONLINE):** embutir tudo em base64
deixava o HTML gigante (~16 MB) porque o áudio é ~77% do peso. Como é sempre online, o áudio
**mora em arquivos** `audio/<chave>.mp3` **ao lado do `index.html`** (mesmo site, caminho
relativo — compat com PC antigo, `new Audio("audio/"+chave+".mp3")`). Nos mapas fica só
`"chave":1` (presença). Resultado no climas: **HTML de 16 MB → ~4 MB**; o navegador baixa
**só o clipe que vai tocar** e guarda em cache. **Mesma voz Antônio, zero navegador.**
Como fazer: extrair cada `data:audio` p/ `audio/<chave>.mp3`, trocar o valor do mapa por `1`,
e apontar `tocarFalaAudio("audio/"+chave+".mp3", …)`. O `auditar-som.py` já valida os dois
modos (embutido OU pasta `audio/`). Recomprimir os MP3 a **24 kbps mono** antes (voz fica
ótima). **O tamanho não quebra o Pages** (100 MB/arquivo, ~1 GB/site); o áudio externo
resolve a **1ª carga** e o **histórico**.

**SUSTENTABILIDADE (muitas atividades):** cada atividade no SEU repo (modelo portal-leve) →
o `audio/` mora **no repo da atividade**, não na fábrica. Repos separados = peso distribuído
(nenhum vira monstro). Este repo-fábrica fica **leve** (templates/manual/HTML-fonte); não
deve acumular o áudio de todas no histórico — publicar com `republicar-limpo.yml` mantém cada
`.git` de destino minúsculo. Limites do GitHub (~1 GB/repo e /site) cabem centenas de
atividades de ~8–10 MB.
**Se a fábrica inchar (ver `git count-objects -vH` → `size-pack`):** o jeito **SEGURO** é
**mesclar a PR (squash) + apagar a branch** — o peso antigo (versões grandes já superadas) fica
inalcançável e o **GitHub recolhe sozinho** (garbage collection), sem reescrever nada.
**Reescrever histórico** (`git filter-repo` + force-push) só quando precisar mesmo e, de
preferência, **com a PR já mesclada** (com a PR aberta é arriscado). A causa nº 1 do inchaço
eram os HTMLs **embutidos de ~16 MB**; com o **áudio externo** (HTML ~4 MB) isso acabou —
a fábrica praticamente não incha mais.

**Histórico do `.git` = o que REALMENTE trava o build (importante):** cada republicação de um
HTML grande empilha ~MB no histórico do repo de destino → é a causa do **"Page build failed"
intermitente**. Publicar com **`republicar-limpo.yml`** (1 commit limpo, force-push) **zera o
histórico** e o `.git` volta a ficar minúsculo → o build volta a `built`. Usar quando o build
começar a falhar (ou periodicamente em atividades que republicam muito).

### 🗂️ BIBLIOTECA DE CAPAS (telas de abertura reutilizáveis) — `_templates/capas/`
Coleção de **capas premium** prontas (HTML autossuficiente, compat OK), cada uma com um
tema/identidade forte, pra não recomeçar o visual do zero. Ao criar/reformar uma atividade,
escolher um tema, copiar a estrutura da capa (selo → título → mascote → história → campo do
nome → botão → prévia da trilha) e ligar às funções reais (`campoNome`, `comecarComNome()`,
Continuar/`telaMenu()`, reset de aula). Temas atuais: **Atlas de Expedição** (geografia/
ciências — JÁ usado no `climas-do-mundo-6ano`), **Grimório Encantado** (leitura/português),
**Números Arcade** (matemática), **Mundo de Massinha** (Pré–2º), **Laboratório do Cientista**
(ciências), **Safári Selvagem** (animais/geografia), **Missão Espacial** (mat/ciências),
**Fundo do Mar** (Pré–4º), **Cordel do Sertão** (português/cultura). Ver `_templates/capas/README.md`.

**Sempre imagem 3D TEMÁTICA (cartela — Pixar/última geração; o Claude ANIMA):** TUDO personalizado ao tema da atividade (nada genérico). mascote (**6 poses**, incl. **boca aberta p/ falar**), **personagem-mascote de CADA ilha** (temático), ilhas/cenários do mapa, objetos das questões (temáticos, vários), **emblemas** de nível, **selos/conquistas** (incl. o de **sequência**), **medalhas** (bronze/prata/ouro), moeda/estrela/troféu/baú, **cadeado** (fechado/aberto), a **recompensa-que-cresce (3 fases)**, cena de abertura e grande final (estas duas viram JPEG de fundo, não recorte). Nunca emoji/SVG nos elementos-chave.
**Ilha/cenário de cada parada = OBJETO flutuante recortado (sem fundo/retângulo/texto), NÃO "cena":** obrigatório por parada (fácil de esquecer); no prompt pedir "só o objeto do circo flutuando no branco, sem parede/chão/céu/cortina/palco/retângulo, sem palavra" — se pedir "cena", o ChatGPT devolve retângulo com fundo. Na tela flutua sobre um holofote redondo suave feito no CÓDIGO (radial-gradient), não na imagem. Detalhes e recorte (flood-fill do branco pelas bordas) no ATIVIDADE-PREMIUM §2/§8. O mascote CAMINHA pela trilha (fica ao lado da parada atual e desce a cada conclusão).
**Pode ficar SVG:** ícones minúsculos de interface que mudam de cor/estado. Se um SVG falhar no PC antigo, vira imagem.

**PRINCÍPIO (não esquecer):** o prompt do ChatGPT NÃO resolve sozinho o problema de parte branca/franja. Um prompt bom (fundo branco puro + SEM sombra + contorno escuro definido) PREVINE a maior fonte (sombra na base) e facilita o recorte, mas SEMPRE sobra franja fina e às vezes vãos internos — só some com a LIMPEZA obrigatória do código. **Garantia = prompt bom + limpeza obrigatória juntos.** Nunca embutir sem passar pela limpeza e pela conferência visual.

**CORPO BRANCO SEM CONTORNO ESCURO = FRANJA IRRECUPERÁVEL (lição paga, crítica):** se a cartela desenhar um objeto/animal BRANCO (coelho, ovelha, galinha, ovo, pato) SEM linha de contorno escura e fechada, o corpo branco encosta direto no fundo branco — não há fronteira. O recorte deixa borda branca esfarrapada, e removê-la por código só PIORA (medido: coelho foi de 21% de franja para 78% e comeu 8,5% do corpo). **NÃO existe conserto por código — a ÚNICA solução é REGERAR** a cartela exigindo "contorno preto grosso e fechado em volta de cada objeto, INCLUSIVE os brancos". Diagnóstico: medir % de contorno escuro na borda; se ~0% e muito branco na borda, veio sem contorno → regerar. (Com contorno, a franja cai para 0%.)

**ORIENTAÇÃO SILHUETA vs COLORIDO — DEVEM APONTAR PARA O MESMO LADO (lição paga):** na fase da sombra (objeto colorido em cima, silhueta preta embaixo), a silhueta e o colorido do MESMO bichinho precisam apontar para o mesmo lado — senão a criança vê a tartaruga virada para a direita e a sombra dela para a esquerda, o que confunde e quebra a associação. As cartelas do ChatGPT saem em orientações aleatórias, então isto acontece com frequência. **Diagnóstico automático:** para cada bichinho, comparar o "lado que pesa" (centro de massa horizontal dos pixels opacos vs. centro geométrico) do colorido (`comp_`/`obj_`) e da silhueta (`sil_`); se um pesa-esquerda e o outro pesa-direita → estão invertidos. **Correção (sem regerar):** espelhar a silhueta por código (`PIL Image.transpose(FLIP_LEFT_RIGHT)`) e re-embutir — é 100% seguro porque a silhueta é uma forma preta chapada; espelhar não distorce nada. Regerar a cartela só se o próprio colorido estiver ruim. Auditar SEMPRE a orientação de todos os pares antes de entregar a fase da sombra.

**SILHUETAS PRETAS (fase da sombra) — recorte por LUMINÂNCIA, não por branco (lição paga):** silhueta é forma preta chapada sobre fundo branco. Recortar detectando os pixels ESCUROS (luminância < ~110), pintar o RGB de preto puro `[0,0,0]`, erodir 1px, alpha = máscara. NÃO aplicar de-fringe de "matar escuros" (apagaria o próprio objeto). Comprimem pra <1KB. Guardar num dicionário separado `SOMBRA["sil_<chave>"]` (não no IMG). O colorido de cada bichinho é reaproveitado do companheiro já embutido (`comp_<chave>`) — NÃO precisa gerar coloridos novos; só as silhuetas.

**QUANDO A VISUALIZAÇÃO DE IMAGEM DO CLAUDE FALHA — AVISAR, NÃO SEGUIR NO ESCURO (lição paga):** a ferramenta de visualização do Claude pode retornar vazio (`[image]` em branco) de forma intermitente. Quando isso acontece, as métricas numéricas (franja, cor dominante, componentes) continuam confiáveis para franja/cor, mas NÃO enxergam problemas de ENQUADRAMENTO que só o olho pega: orientação virada, objeto de cabeça para baixo, recorte cortando um pedaço, dois bichos colados. Nesses casos o Claude deve: (a) AVISAR o Marcos de forma DESTACADA que não conseguiu ver a imagem ("minha visualização falhou nesta imagem — confira a orientação/enquadramento no mosaico `conferir_*.png`"), (b) embutir por número apenas quando o risco é baixo e puramente de franja/cor (contorno fechado + franja ≤1%), e (c) deixar o mosaico de conferência salvo em outputs para o Marcos validar com os olhos. NUNCA tratar "franja ok pelos números" como se fosse "imagem ok" — franja e orientação são coisas DIFERENTES, e só a segunda precisa de olho humano. Ambíguo ou não pôde ver = apontar como PENDÊNCIA de conferência visual, não como concluído.

### Regra do anexo — CARTELA ÚNICA
Sempre pedir todos os objetos numa **cartela única** (vários itens em grade, numa imagem só), nunca um a um (estoura o limite de anexos). Gerar e enviar uma cartela por vez.
> **O QUE VIRA CARTELA (quanto mais, melhor — barateia e facilita):** mascote (4 poses),
> companheiros, objetos de cada parada, medalhas, emblemas, selos, recompensa 3 fases, **e as
> ILHAS/cenários das paradas** (o Marcos já fez cartela de ilhas e funciona — são recortáveis,
> NÃO precisam ser solo). **Fica SOLO só o que vira fundo de tela cheia:** capa, cena final
> (viram JPEG de fundo) e o desenho de colorir. **Por que juntar em cartela:** menos gerações →
> **cabe no limite GRÁTIS** (app do ChatGPT/Gemini na assinatura, ou API grátis do Gemini/AI
> Studio com a chave em secret) — só a API da OpenAI é paga. **Corte limpo:** elementos em grade,
> bem separados, fundo liso/transparente, mesmo tamanho; recorto com PIL e **confiro com o Marcos**.

### Objetos de contagem — variedade (não cansar)
Cada fase de contagem tem 2-3 objetos temáticos coerentes com o lugar, e a fase ALTERNA entre eles por desafio (`objDaFase()` cicla pela lista `F.objs` por `idxDesafio`; `F.obj` como fallback). Nunca um único objeto repetido em 5-6 desafios seguidos. Gerar todos os objetos da fase na MESMA cartela.

### Fluxo obrigatório de imagem
1. Claude entrega o **prompt pronto** numa página HTML com botão "Copiar" (Marcos não copia da conversa). Cada prompt (cartela ÚNICA) pede: itens em grade bem separados; fundo branco liso #FFFFFF sem textura/moldura/cartão; cartoon flat infantil, cores vivas; **SEM NENHUMA SOMBRA (nem projetada, nem elíptica de contato embaixo)**; **contorno escuro e fechado em volta de cada objeto** (separa do fundo e do próprio branco interno); **sem partes brancas/cinza coladas na borda externa**; **objetos sólidos sem vãos internos vazados**; sem texto/letras/números (números só quando forem o objetivo, "bem grandes e legíveis"). As CENAS (abertura/final) pedem retângulo deitado 3:2 preenchendo tudo (podem ter sombras normais, viram fundo inteiro).
2. Marcos gera UMA cartela por vez e envia.
3. **ANTES de recortar, diagnosticar o arquivo REAL no disco** (dimensões + cores dominantes): uploads às vezes chegam CORTADOS (só uma fileira) ou são OUTRA cartela que não a do preview. Se não bater, AVISAR e pedir reenvio — nunca recortar no escuro.
4. Recortar com **PIL** por COMPONENTE CONECTADO (`scipy.ndimage.label`; nunca célula fixa) OU por projeção de grade (bandas de ocupação por coluna/linha, para grades regulares). Flood-fill do branco, `fill_holes`, dilatação leve, margem transparente ~9-10%.
5. **DE-FRINGE OBRIGATÓRIO:** (a) zerar alpha dos quase-brancos (R,G,B>226) na fronteira; (b) erodir alpha 1px; (c) zerar semitransparentes claros; (d) suavizar e BINARIZAR (>130→255, senão 0). A franja também pode ser CINZA-CLARA (≥200, dessaturada) — passe extra que erode +1px e mata claros dessaturados no anel da borda.
6. **LIMPEZA PROFISSIONAL PÓS-RECORTE** (conferir TODA imagem):
   - **Resto de SOMBRA na base** (mancha creme/cinza sob o objeto): remover componentes claros dessaturados (mín RGB≥185, saturação baixa) pequenos (4px até ~4% do objeto) com centro no terço inferior + migalhas nas ~6 linhas finais. **NUNCA em corpos brancos/creme sem conferir com os olhos — raspa o corpo.**
   - **VÃO INTERNO branco opaco** (vão entre alça e cesta, etc.): o `fill_holes` fecha com branco. Detectar componentes branco-puros grandes e tornar transparentes — **só com confirmação visual**; em corpos brancos e cenários com nuvens, NUNCA automático.
   - **FRANJA cinza-clara no contorno:** matar claros dessaturados (≥200) no anel de 2px junto à transparência.
   - Em TODA remoção: verificação numérica (perda ≤ poucos %, zero claros na base, RGB intocado fora do alpha removido); imagem sem nada a remover mantém o base64 original; ambíguo = NÃO embutir e perguntar.
7. **INSPEÇÃO VISUAL OBRIGATÓRIA antes de embutir:** mosaico em fundo xadrez E em FUNDO ESCURO (cor de fundo da atividade), com ZOOM nas bordas. Métricas sozinhas NÃO bastam (corpos brancos confundem). Ambíguo = perguntar. Validar por cor dominante (maçã vermelha; se sair roxa, cartela trocada → PERGUNTAR, não corrigir sozinho).
8. **Otimizar:** resize pela altura de uso (objetos ~110px, companheiros ~150px, medalhas/selos ~150-170px, troféu ~190px), `quantize(28-44 cores, MEDIANCUT, dither=NONE)`, alpha binário (`>120→255,0`). Cenas: JPEG quality 82, largura ~640px. **Objetos NUNCA em JPG** (JPG não tem alpha — vira quadradinho branco). Conferir mime REAL `image/png`, não só a aparência.
9. Embutir base64 e apresentar a atividade RENDERIZADA (Marcos não vê recortes intermediários).

**RECORTE DE CARTELA EM GRADE — por COMPONENTE CONECTADO, não célula fixa (lição paga):** se um item ultrapassa a célula, o corte reto DECEPA parte do corpo. Recortar: máscara do não-branco na imagem INTEIRA → `fill_holes`+`label` → manter os N maiores componentes → ordenar por centroide (linha por cy, coluna por cx) → re-adicionar só brilhos pequenos dentro do disco. Margem transparente ~9-10% em volta.

**SIZING/ANIMAÇÃO DE PEÇA NA TELA (lição paga):** ao exibir (ex.: medalha): `img{display:block;margin:0 auto}` (centraliza); largura limitada + altura fixa com `width:auto` (preserva proporção, NUNCA `WxH` fixo em imagem não-quadrada); card `overflow:visible`; a animação de revelar NÃO passa de `scale(1)` no meio (senão estoura a borda só durante a animação — o corte "pisca"). AUDITAR renderizando DURANTE a animação.

**CSS obrigatório para imagens:** `.card img { object-fit:contain; max-width:100%; }` e `overflow:visible` em halos.

================================================================
## 10. CSS ROBUSTO PARA NAVEGADOR ANTIGO (lições pagas)
================================================================
- **NUNCA `width:100%; height:100%; object-fit:contain` em imagem** — em Firefox 106/Chrome antigo COLAPSA a imagem para tamanho zero (some). Usar largura em px OU `width:100%; height:auto`, com `display:block`. Auditar o CSS inteiro.
- **Imagem RETRATO em container fixo — dimensionar pela ALTURA, nunca pela largura (lição paga: mascote sobrepondo o desafio).** O mascote ChatGPT é retrato (~163×220); com `width:100%;height:auto` num container 78×78 ele estoura para baixo e COBRE o conteúdo. Correto: container em px + `img{display:block;height:100%;width:auto;margin:0 auto}` + `overflow:hidden`. O mascote JAMAIS pode sobrepor o conteúdo — auditar renderizando.
- Glow em PNG recortado: `filter:drop-shadow` (par `-webkit-`), NUNCA `box-shadow` (desenha retângulo).
- Objetos de contagem: `display:block; width:100%; height:auto` no container com px.
- Flexbox com fallback `-webkit-box` (+ `-webkit-box-flex` explícito nos filhos).
- Imagens não-quadradas: altura fixa + `width:auto`. Cards com `overflow:visible` onde há halo/animação.

**TELA CHEIA (fullscreen) COM FALLBACK SEGURO (lição paga):** botão flutuante no canto superior (`requestFullscreen` com TODOS os prefixos: `webkit`/`moz`/`ms`), que só APARECE se `telaCheiaSuportada()` — em navegador antigo sem a API, o botão fica `display:none` e não quebra nada. O ícone alterna (entrar/sair) via listeners de `fullscreenchange` (todos os prefixos). Ativar fullscreen exige gesto do usuário (clique) — nunca automático.

**BOTÕES DE AÇÃO NO TOQUE — `onclick` SOZINHO NÃO FUNCIONA EM MUITOS CELULARES (lição paga, crítica):** botões que a criança usa para agir direto (setas do labirinto, controles de jogo, D-pad) precisam de `ontouchstart` ALÉM do `onclick`, senão em vários celulares reais a criança toca e NADA acontece (bug medido nas setas do labirinto). O `ontouchstart` executa a ação na hora (com `preventDefault`/`stopPropagation`); o `onclick` só age se NÃO veio de um toque nos últimos ~500ms (guardar timestamp do último toque e ignorar o click-fantasma). CSS do botão: `touch-action:manipulation` (tira o atraso de 300ms e evita zoom), `-webkit-tap-highlight-color:transparent`, `user-select:none`. Testar SEMPRE em modo toque (Playwright com `devices["iPhone 12"]` e `page.tap`), NUNCA só com clique de desktop — o bug só aparece no toque real.

**TOQUE-DUPLO DO CELULAR DISPARA O EVENTO 2× (lição paga, crítica):** no touchscreen, um único toque pode disparar o handler DUAS vezes (o touch e o click-fantasma logo depois). Em qualquer mecânica que AVANÇA um contador/sequência a cada toque (ligar-pontos em ordem, etapas), isso faz o contador pular (de 1 para 3) e o próximo toque "certo" passa a ser considerado errado — sintoma clássico: "toco no número/ponto certo e diz que não é o próximo". Proteção: guardar o último valor tocado + timestamp; se o MESMO valor vier de novo em menos de ~350ms, ignorar. Isso só reproduz no celular real (o Playwright normal não duplica o toque) — testar com `page.tap` em modo device.

**BUG QUE "PERSISTE" NA VERSÃO PUBLICADA PODE SER CACHE, NÃO CÓDIGO (lição paga):** quando o Marcos relata que um bug já corrigido continua aparecendo na versão publicada, a causa frequente é o CACHE do navegador servindo a versão ANTIGA do `index.html` — não um bug real no código atual. Antes de reinvestigar a lógica, confirmar que o código atual já está correto (rodando o teste) e orientar o Marcos a recarregar forçando atualização (puxar pra baixo no celular / aba anônima) ou usar "Começar do zero". Não perder tempo reinvestigando lógica que os testes mostram correta. SEMPRE lembrar o Marcos de limpar o cache ao republicar.
**LAYOUT ADAPTATIVO SEM QUEBRAR O CELULAR (lição paga):** aproveitar telas grandes AUMENTANDO o `max-width` do `.wrap` só via `@media (min-width:700px)` e `(min-width:1000px)` (ex.: 520px → 680px → 820px). No CELULAR (≤699px) NADA muda — o conteúdo continua 100% da largura, igual antes. `@media` é seguro em navegador antigo. **Auditar sobreposição do botão flutuante:** no celular estreito o botão de tela cheia cobre o título — reservar um respiro no topo (`body.tem-botao-tc .wrap{padding-top:48px}` no celular) e deixá-lo menor (38px celular / 44px PC). Testar 320–1920px: zero overflow, zero sobreposição.

================================================================
## 11. GAMIFICAÇÃO (estrutura padrão)
================================================================
- **Níveis** com XP crescente (5 níveis temáticos). Ex.: Aprendiz (0) → Explorador (60) → Aventureiro (150) → Guardião (260) → Mestre (400). `nivelAtual()`.
  - **Calibrar os limiares à ECONOMIA REAL de pontos, senão o nível 5 fica inalcançável (lição paga):** contar quanto a criança ganha completando tudo (ex.: +2 por acerto × ~5 rodadas × 7 fases de escolha + jogos +2 + extras ≈ 80–100 pts) e por os 5 limiares DENTRO disso (ex.: 0/15/35/55/75), pra ela chegar a "Estrela do Circo" ao terminar bem. Números bonitos (0/60/150/260/400) só servem se a economia der esses totais.
  - **Emblema por nível = IMAGEM de patente escalonada** (bronze → prata → ouro → ouro+louros → ouro+louros+coroa): pedir 1 cartela com os 5 lado a lado, recortar por vãos brancos (JPEG: usar limiar de branco ~226 e `binary_opening` p/ tirar chuvisco). Guardar `img` em cada `NIVEIS[i]`; `atualizarTopo` troca o `<img>` do emblema do topo. Emblema no topo é CONTAINER transparente (sem disco/fundo) — a própria arte é a insígnia.
  - **Pop "subiu de nível" — overlay SÓLIDO, animar só o card (lição paga):** o overlay de tela cheia NÃO pode animar a própria opacidade (fade), senão o card fica translúcido no meio da animação e o mapa atrás vaza. Overlay com `background` sólido semi-opaco fixo (`rgba(...,.78)`), e a entrada anima só o `.lucard` (`revela` = scale). Card com cor sólida de fallback ANTES do gradiente. Auto-remove em ~3,4s. Detectar level-up comparando `nivelIdx()` antes/depois de somar pontos (em `acertou` e `fimExtra`).
- **Emblema do nível atual SEMPRE visível na topbar** (imagem ~42-44px), atualizando ao ganhar XP e ao carregar progresso salvo — `atualizarEmblemaTopo()` em `addEstrela`, no `carregar` e na inicialização. Erro comum: gerar os emblemas mas só mostrar no pop-up de level-up (some em 3s) — a criança nunca vê o emblema do nível dela.
- **Subir de nível** detectado em `addPontos`: animação + fanfarra + confete + fala.
- **Conquistas/selos (FEITO)** — imagens do tema (ROSETAS de fita, distintas das medalhas e emblemas), nunca emoji. Marcos: primeiro acerto, 5 seguidos (streak), 1ª parada, metade, campeão (tudo). `CONQUISTAS[]` + `ESTADO.conquistas{}`; `checarConquistas()` (chamado em `acertou` e `fimFase`) destrava qualquer selo cuja `condConq(k)` virou true → `popConquista` (reusa o overlay `.levelup`) + `enfileirarFala`. Se vários caem juntos, ESCALONAR o pop (`atraso+=3500`). Coleção mostrada em "Minhas Medalhas" (ganhos coloridos, faltando cinza+cadeado). **Recorte dos selos (fundo FOTOGRÁFICO cinza, não branco):** segmentar por SATURAÇÃO (`fundo = sat<34 & claro`), não por branco — senão o amarelo (saturado e claro) seria apagado; componentes conectados + `fill_holes` (mantém branco interno da bandeira/estrela).
- **Medalha por fase:** um MEDALHÃO DOURADO (círculo de ouro com fita/laço colorido e borda serrilhada) com o SÍMBOLO da fase no centro (ovo, maçã, vaca, cenoura, osso, troféu...) — NÃO é o bicho/mascote inteiro nem emoji. Imagem dourada temática recortada; o NÚMERO (1..N) é adicionado por código via overlay `.med-num`. Regerar ao refazer a atividade. (Lição paga: uma cartela de "bichos" no lugar de medalhões passou como medalha sem ser — conferir % de dourado: medalhão tem ~37-56%; se der 1-3%, é figura, regerar.)
  - **SÍMBOLO PICTÓRICO, sem texto na imagem (lição paga):** letra/número dentro de imagem do ChatGPT sai torto. Pedir o centro como DESENHO (balões, argolas, formas, holofote, lâmpada, livro, lupa, peça de quebra-cabeça, cartas, binóculo…), NUNCA "as vogais A E I O U" ou "o número 3". O número da parada entra por código (`.med-num`, badge vermelho no canto).
  - **Uma CARTELA com as N medalhas + recorte por componente conectado + PREENCHER BURACOS:** gerar tudo numa folha (grade espaçada, fundo branco). Recortar cada medalha por `ndimage.label` do não-branco; para cada centro, pegar SÓ aquele componente (exclui fragmento da fita da medalha vizinha que cai no bounding box). `binary_fill_holes` no componente antes do alpha — senão o branco INTERNO (face das cartas, papel do livro, bulbo da lâmpada, lente da lupa) vira furo transparente. Mapear cada blob à parada por posição (row-major) e conferir num MOSAICO numerado antes de fechar. O ChatGPT às vezes gera 1 a mais (repetido) — sobra ignorada.
  - **Coleção "Minhas Medalhas" (botão sempre no mapa):** grade das N; ganha = colorida + badge do número; não-ganha = `filter:grayscale(1) opacity(.4)` + cadeado + badge cinza. Ao concluir a parada, `fimFase` mostra o medalhão real daquela parada (não mais o emoji) e a fala diz "você ganhou a medalha número N". Medalha ganha = `concluidas[ch]` (não precisa estado novo).
- **XP por acerto** com bônus de streak: `acertou()` dá +2 e **+1 extra quando `streak>=3`**. Guardar `ESTADO.maxStreak` (pra conquista "pegando fogo").
  - **STREAK VISÍVEL (feito):** ao emendar 3/5/7/10 acertos, um TOAST `.streakpop` no topo ("🔥 N seguidos!") + fala `numExt(N)+" acertos seguidos"`. Sem toast some sozinho (~1,7s), `pointer-events:none`.
  - **FILA DE FALA (feito) — `enfileirarFala` + defer:** `falar(t)` LIMPA a fila e fala agora (primário); `enfileirarFala(t)` ADICIONA sem cortar; ao terminar cada fala, `_drenarFila()` toca a próxima. **Pegadinha:** `acertou()` roda ANTES do `falar(elogio)` do responder — se enfileirar direto, o `falar(elogio)` limparia a fila. Solução: enfileirar streak/nível DENTRO de `setTimeout(...,0)` em `acertou`, pra rodar DEPOIS do `falar(elogio)` síncrono. Assim ouve-se elogio → "N seguidos" → "subiu de nível" em sequência, sem cortar. (Foi isso que destravou o level-up FALAR.)
- Toda fase termina chamando a tela de fim de fase (registra `concluidas[fase]` e conquistas). Ao remover fases, religar conquistas órfãs.
- **Grande final:** confete em ondas, mascote comemorando, desfecho da história, recompensa no tamanho máximo, emblema do nível, estatísticas (concordância: "1 ponto"/"2 pontos"). Cena final ilustrada no topo.
  - **CENA final = banner ilustrado (JPEG, não PNG):** cena é foto/ilustração cheia (com fundo) → salvar como **JPEG q82 ~720px** (fica ~100KB; PNG do mesmo daria ~400KB). Pra isso o `build.py` escolhe o MIME por extensão (`.jpg/.jpeg` → `image/jpeg`, senão `image/png`) — senão o data URI sai rotulado errado. Banner no topo do `telaFinal` com `border-radius` + `box-shadow` (não é recorte, é retângulo, então `box-shadow` pode). Objetos recortados continuam PNG (alpha).
- **Relatório do professor (feito):** aproveitamento geral + tabela por fase (acertos/erros/% com cor) + o que revisar + imprimir/PDF. Acessível do grande final e do mapa (só com tudo concluído). **Requer GRAVAR stats:** em `fimFase`, acumular `ESTADO.stats[ch]={a,e}` (soma `dAcertos`/`dErros`). `pctFase(ch)` = -1 se sem dados. "Vale revisar" = fases com `%<70`. Botão imprimir chama `imprimir(){window.print();}` — NÃO usar `onclick="window.print()"` direto (o auditor lê "window" como função inexistente → FALHA). **Tabela cabe no celular com `table-layout:fixed`** + larguras (1ª col 46%, demais 18%) + `word-break:break-word` (nomes longos quebram, a coluna % nunca some).

================================================================
## 12. MECÂNICAS DE FASE (catálogo do que funciona)
================================================================
- **Conhecer os números (até 10/20/30):** grade; cada número acende devagar (glow dourado) com áudio contando. Começa após a narração terminar (callback). Botão/aviso pulsante.
- **Completar a sequência:** fileira com slots `?`; o aluno **arrasta** o número que falta.
- **Número e quantidade:** conta bichinhos e **toca** no número (resposta + 2 vizinhos).
- **Cesta — adição concreta:** **arrasta** itens até a cesta em 2 etapas (a + b), vê encher e o total.
- **Cesta — subtração concreta:** cesta cheia; **arrasta** itens para fora; vê quantos sobraram.
- **Adição (conta armada):** parcelas concretas + conta armada; 2 quadradinhos (dezena/unidade) onde **arrasta** o resultado; banco 0-10. Resultados variados.
- **Subtração:** (1) conjunto com itens **riscados** — conta sobraram e toca; (2) conta armada sem pedir emprestado — arrasta o resultado.
- **Memória:** parear cartas iguais (conceito ↔ representação). 4 pares (8 cartas) para a idade.
- **Quebra-cabeça de ordenação:** ordenar itens tocando do menor ao maior. Slots `?` no topo; banco embaralhado embaixo; toque errado avisa sem punir.
- **Caça-palavras:** grade 10x10, célula ~27px para caber no celular.
- **Frase em ordem:** "Monte a Frase" — ordenar palavras embaralhadas.
- **Escolha múltipla com imagem (`escolha-img`):** mesma regra de embaralhar.
- **Classificar fichas:** arrastar ou clicar (mouse + touch).
- **Forca:** tradicional, com figura simples (traço não-gráfico, sem sofrimento); dica + teclado + 6 vidas. Relief games NÃO levam Desafio Extra.

### Ligar os Pontos (revela o desenho)
- A criança TOCA nos números em ordem (1→N); ao ligar o último, some com as bolinhas numeradas e aparece a IMAGEM PNG do objeto (animação de revelar por OPACIDADE — nunca `scale` no SVG, que voa pra fora), com o SVG poligonal só como reserva.
- **SÓ TOQUE — nunca "passar o mouse por cima" (lição paga):** ligar por hover (`onmouseenter`) quebra no celular e dispara "esse não é o próximo" à toa. Ligar exclusivamente por toque/clique no ponto. Proteger contra toque-duplo (ver seção 10) — senão o contador pula.
- **O CONTORNO DOS PONTOS DEVE FORMAR A MESMA SILHUETA DA IMAGEM REVELADA (lição paga):** as coordenadas não podem ser "chutadas" — se o desenho revelado é uma concha, ligar os pontos tem de traçar uma concha. Extrair o contorno REAL da imagem por código (amostrar o raio máximo do centro em vários ângulos com PIL, normalizar 0–100, reduzir a ~10 pontos bem distribuídos) e conferir a ORIENTAÇÃO (imagem e contorno apontam para o mesmo lado). Preferir figuras de silhueta SIMPLES (estrela, concha) a formas complexas (peixe com cauda/barbatanas). A imagem revelada e as coordenadas são um PAR: trocar uma exige refazer a outra. Fala com artigo de gênero por figura ("desenho da concha").

### Labirinto (setas na tela + teclado)
- Grade de células SEPARADAS com cantos arredondados (não grade contínua). Mascote como imagem andando; objetivo = troféu/imagem; paredes de coral (cor sólida, sem emoji). Labirintos como strings 5×5 (`S`=início, `E`=tesouro, `X`=monstro, `0`=caminho, `1`=parede).
- **Setas NA TELA (4 botões, funcionam no toque) + teclado juntos:** a criança no celular não tem teclado, então os botões de seta na tela são obrigatórios (~60px). Ver a lição de toque (seção 10): `ontouchstart`+`onclick`+`touch-action:manipulation`, senão não movem no celular. O teclado (setas) chama a MESMA função de mover por direção.
- **Monstrinho** (célula "X"): se o mascote toca, volta ao início com aviso gentil. **Vários labirintos em sequência** (ex.: 3 mapas); ao vencer um, carrega o próximo; ao vencer todos, fim de fase. É fase-jogo: NÃO leva Desafio Extra.
- **Variar a posição do TESOURO (e do início) entre os labirintos (lição paga):** se o tesouro fica sempre no mesmo canto, a criança decora o caminho. Cada labirinto com o `E` em lugar diferente (e às vezes o `S` no lado oposto). Validar por BFS que cada um é resolvível E que o monstro fica adjacente ao caminho certo (senão vira decoração inútil).
- Listeners do teclado instalados UMA vez (guardar com flag), removidos ao concluir a fase.

### Quebra-cabeça (grade configurável — 2×2, 2×3…)
- **Os espaços (slots) precisam formar uma GRADE, não uma fileira (lição paga):** `text-align:center` + `inline-block` põe todos os slots em UMA linha (horizontal), o que não parece quebra-cabeça. Dar ao container da grade uma LARGURA FIXA = `slotPx × colunas` (ex.: 3×90px=270px) — aí os `inline-block`/flex-wrap quebram naturalmente nas linhas certas. As peças da imagem real vêm de FATIAR a foto (recorte por código, uma `<img>` por peça), não de `background-position` — assim cada peça é um arquivo leve e a peça do tray é idêntica à do slot-guia.
- **Motor GENÉRICO por fase (`PZCFG`):** cada quebra-cabeça é `{pre, cols, rows}` (ex.: `quebra2:{pre:"q2",cols:3,rows:2}`); `renderQuebra` lê `cols*rows`, monta os slots-guia (imagem clarinha `opacity:.2`) e as peças embaralhadas no tray, tudo dimensionado por `cols` (slot 104px p/ 2 col, 90px p/ 3+ col) com estilo INLINE — sem CSS novo por fase. Peças numeradas em ORDEM LINHA-A-LINHA (0,1,2 na 1ª linha; 3,4,5 na 2ª); acerta quando `slot===peça`. Fatiar a foto na MESMA ordem.
- **Dificuldade por idade:** Pré começa em 2×2 (4 peças); um 2º quebra-cabeça pode subir p/ 2×3 (6). 3×3 (9) já costuma frustrar o Pré. Fase-jogo: `jogo:true`, sem Desafio Extra.
- **A FOTO tem que ser CHEIA e ESPALHADA (lição do puzzle):** cada peça precisa ter conteúdo reconhecível — se a cena tem céu/fundo liso grande, a peça vira "só azul" e a criança não tem pista de onde encaixa. No prompt, pedir cena de ESPETÁCULO cheia (personagens/objetos distribuídos por todo o quadro, fundo colorido de cortina/luzes, SEM manchas vazias). Usar proporção **3:2** (ex. 1200×800) → recorte 2×3 dá peças QUADRADAS (400×400). As peças são exibidas pequenas (~90px), então **reduzir cada peça p/ ~260px + quantizar** (não guardar 400px cheios): 6 peças ficam ~330KB em vez de ~640KB. Conferir por screenshot que as peças remontam a cena certa (auto-resolver no teste: chamar `onSoltaPeca(i,i)` p/ cada i).

### Caça aos 7 Erros (2 fotos + toque nas diferenças)
- **Padrão:** DUAS fotos empilhadas (a "certa" em cima, a "com erros" embaixo). A criança COMPARA e TOCA na foto de baixo em cada diferença. Contador "Você já achou X de 7". Ao achar todas → `acertou()` + fanfarra. É fase-jogo (`jogo:true`, `tipo:"erros"`, `montarRodadas`→`[{erros:true}]`), NÃO leva Desafio Extra. Cada acerto: `somAcerto()`+`confete(10)`+fala "Faltam N"; toque errado só avisa carinhoso (sem punir/zerar).
- **As 7 diferenças são feitas POR CÓDIGO** a partir de UMA cena limpa do ChatGPT (não peça 2 imagens ao usuário — o ChatGPT não garante que só 7 coisas mudem). Cena LIMPA = poucos elementos GRANDES e bem separados, fundo liso (céu/chão chapados), sem confete/estrelinhas miúdas — senão a criança do Pré não acha. Prompt em página com botão Copiar.
- **Overlay responsivo à prova de escala (caixa de aspecto):** o `<div class="errosImg">` usa `padding-bottom:54.43%` (=altura/largura da cena, ex. 381/700) pra manter a proporção em qualquer largura; a `<img>` vai `position:absolute` cobrindo 100%. Os anéis verdes são `<span>` absolutos posicionados por `left/top` em **%** (`x/W*100`, `y/H*100`) com `transform:translate(-50%,-50%)`; o círculo perfeito sai de `width:13%;height:0;padding-bottom:13%` (padding-% é relativo à LARGURA → vira círculo) + `border-radius:50%`. Marcadores iguais nas DUAS fotos (`hc<i>`/`he<i>`), revelados juntos ao acertar. Assim funciona de 320px a 520px sem recalcular nada em JS.
- **Acerto por HIT-TEST no espaço da cena, não por `<div>` clicável por erro (evita ambiguidade quando 2 erros ficam perto):** um ÚNICO `onclick` na foto de baixo converte o clique pra coordenadas da cena natural (`(clientX-rect.left)/rect.width*W`), acha o erro NÃO-achado mais PRÓXIMO dentro de um raio (ex. 44px em espaço 700×381) e revela. Divs sobrepostos dariam clique ambíguo entre erros vizinhos (ex. lua+estrela).
- **LIÇÃO PAGA — recolorir só funciona em elemento de cor ISOLADA; cuidado com cores repetidas na cena:** flood-fill/troca-de-faixa-de-cor vaza se a MESMA cor chapada aparece em dois lugares colados. Caso real: a manta VERMELHA do elefante tem exatamente o mesmo vermelho das LISTRAS da tenda atrás dele, e as duas se tocam → a troca "pintou" a listra da tenda em vez da manta (erro que parecia glitch). **Escolher diferenças em elementos de cor única e bem separados:** remover lua/estrela/pipoca (pintar da cor do fundo com elipse), recolorir 1 balão, 1 bandeirinha, o toco/pódio, o chapeuzinho do bicho — NÃO recolorir algo cuja cor se repete adjacente. Sempre CONFERIR por screenshot (recorte lado-a-lado certa×errada) que cada diferença caiu no lugar certo e não vazou, ANTES de fechar. Guardar a cena original e a modificada como 2 PNGs quantizados (~75KB cada).

### Tela de Pintar (presente do Grande Final — 100% código, sem imagem)
- **Recompensa livre depois de concluir tudo:** o troféu do fim da trilha só fica CLICÁVEL quando todas as paradas estão concluídas (`tudo` no mapa) → abre a tela de Grande Final (confete em ondas, mascote comemorando, desfecho da história, estatística com concordância "1 parada/N paradas", "1 ponto/N pontos") → botão grande "🎨 Pintar o Circo!" abre a Tela de Pintar. A narração do mapa passa a apontar "toque no troféu dourado".
- **PINTAR POR TOQUE (balde de tinta), NÃO pincel livre (pedido do usuário, melhor pro Pré):** a criança escolhe a cor e TOCA numa parte do desenho → aquela região inteira preenche até as linhas (flood fill). Muito melhor que pincel: o Pré não consegue "ficar dentro da linha". Canvas QUADRADO (600×600) + CSS `width:100%;height:auto`; mapear toque por `(clientX-rect.left)/rect.width*600`. Só `onmousedown`/`ontouchstart` (toque único, sem arrasto), com `preventDefault`.
  - **O DESENHO É DESENHADO NO PRÓPRIO CANVAS (não overlay) pra virar barreira do flood:** `drawImage(desenhoContorno,0,0,600,600)` sobre o branco (as linhas pretas do PNG viram as paredes). `baldePintar(x,y)`: `getImageData`, cor-alvo = pixel tocado; se for linha (soma RGB < ~330) ou já a cor nova, sai; BFS com pilha de ÍNDICES inteiros (`y*W+x`), barreira = `soma<360`, preenche vizinhos cuja cor casa com a alvo (tolerância ~60/canal), `putImageData` no fim. Fundo é UMA região (colore tudo em volta = o "céu") — normal. Cada listra/parte fechada é uma região. "Limpar" = repinta branco + `drawImage` do contorno de novo. Sem `visited` (o próprio recolorir impede reprocessar). Performance ok pra toques esporádicos (~360k px).
- **Paleta grande fala a cor:** ~10 bolões de cor; ao tocar, `falar(nome)` (o Teo diz "vermelho", "azul"…) e marca a cor selecionada (anel dourado). Botão branco precisa de anel cinza no `box-shadow` pra aparecer no fundo branco. Botões "Limpar" (repinta o fundo branco) e "Voltar".
- **Música de fundo na pintura: REMOVIDA (lição paga).** Tentou-se um loop com Web Audio (`setInterval`+`nota()`), mas não tocou de forma confiável no aparelho da professora (o `nota()` pontual de clique/acerto funciona, o loop contínuo não) — melhor TIRAR do que deixar um botão que não faz nada. O que fica na pintura: paleta que FALA a cor (TTS no gesto, funciona) + os sons de clique. Se um dia quiser trilha, usar `<audio>` com arquivo real embutido (mais confiável que oscilador em loop). `pararMusPinta()` foi mantido como no-op seguro (ainda é chamado ao trocar de tela).
- **DESENHO PARA COLORIR (livro de colorir):** gerar no ChatGPT um "coloring page" (só linhas pretas grossas, miolo branco, formas grandes/simples/bem fechadas — regiões amplas). Converter em LINHAS PRETAS TRANSPARENTES p/ arquivar limpo: `alpha = 255 - luminância`, `alpha=0` onde `lum>238`, RGB preto; autocrop + padding pra QUADRADO. No canvas o contorno é desenhado por cima do branco (vira as paredes do flood). Regiões precisam ser FECHADAS senão a cor "vaza" (contorno grosso e contínuo ajuda).
- Só `var`/`function`/`for`; sem arrow/template-literal. `setInterval`/`clearInterval`/`setTimeout`/`Math.abs`/`getImageData`/`putImageData`/`parseInt` são permitidos. Conferir por screenshot tocando regiões por código (`escolherCor(i)`+`baldePintar(x,y)`).

### Contas de dois algarismos
- Progredir de 1 para 2 algarismos, sem pedir emprestado nas séries iniciais.
- Resultados variados. Piscar a coluna das unidades ao abrir e mascote fala (com pausa): "Esta conta tem dezena e unidade. Começamos sempre pelas unidades!".

### Sistema de arrastar (motor GLOBAL + GHOST — lição paga)
- **Motor global, instalado UMA vez:** `instalarDragGlobal()` registra UM conjunto de listeners no `document` (mousemove/touchmove/up/end), guardado por `window.__dragInstalado`. NUNCA adicionar/remover listeners por elemento a cada arraste — acumula listeners órfãos e trava a página em fases longas (bug medido: `Target closed` na 11ª fase).
- **GHOST:** ao arrastar, `criarGhost()` clona o elemento num "fantasma" `position:fixed` que segue o cursor (`pointer-events:none`); o ORIGINAL fica parado. Isso evita que `elementFromPoint` pegue o próprio arrastado e evita bagunçar o layout. `moverGhost`/`removerGhost` cuidam do resto.
- **Assinatura:** `tornarArrastavel(el, chave, idx, onSolta)`; o callback recebe `(dropId, chave, idx)`. `marcarSoltavel(el, id)` seta `data-drop=id`. Ao soltar, `aoSoltar` sobe pelos pais (`parentNode`) procurando `data-drop` — então soltar sobre um filho do alvo (a imagem dentro do cesto) funciona igual.
- `instalarDragGlobal()` DEVE ser chamado quando a fase de arrastar inicia.
- **ARRASTAR PRIMÁRIO, TOQUE RESERVA** onde a ação é "levar um item até um lugar" (sombra=ligar, sequência=ordenar nos slots, classificar cor/tamanho/forma no "cesto", quebra-cabeça). Onde a ação é "apontar/escolher um" (achar o diferente, letra inicial, vogais, contar), fica TOQUE — arrastar seria forçado. Memória (virar carta) e labirinto (setas) têm mecânica própria.

### Fase da SOMBRA (padrão: revela o colorido ao acertar)
- Duas colunas: à esquerda os bichinhos COLORIDOS (imagem `comp_`/`obj_`); à direita as SILHUETAS PRETAS (`SOMBRA["sil_<chave>"]`). A criança ARRASTA cada bichinho até a sombra igual.
- **Ao acertar, a silhueta REVELA o colorido** por cima dela (troca a `<img>` preta pela colorida) — feedback lindo e claro.
- **Sem quadrado/card nos dois lados** (bichinhos e silhuetas ficam soltos, fundo transparente, sem borda) — fica mais bonito. Um leve `drop-shadow` no bichinho o destaca do fundo.
- **ÁREA DE ACERTO para formas VAZADAS (caranguejo, polvo, estrela, água-viva) — lição paga:** a `<img>` da silhueta precisa de `pointer-events:none` para que `elementFromPoint` sempre pegue o CONTAINER (o box inteiro, `data-drop`), e não caia num vão transparente da forma. Sem isso, soltar no "meio" do caranguejo não acerta. A área de acerto é o retângulo inteiro do alvo.
- Orientação silhueta↔colorido conferida (ver seção 9). Fallbacks de emoji devem ser Unicode 6.0 seguros (a imagem real sempre vence, mas o validador checa).

### Integração de fase-jogo
- Registrar `FASES.x={titulo,cor,icone,jogo:true}` e tratar no `iniciarFase` (`if(chave==="memoria"){iniciarMemoria();return;}`).
- Inserir na ORDEM no MEIO, espalhados. Mapa: cenário + companheiro como qualquer parada.
- Narram automaticamente, dão pontos (`addPontos`), têm `proximaFase()` para o gancho, e NÃO levam Desafio Extra.

================================================================
## 13. ESTRUTURA TÉCNICA / BUILD E VALIDAÇÃO
================================================================
- HTML base com marcador `/* LOGICA AQUI */` substituído pelos JS concatenados.
- Para atividades grandes: separar em módulos JS (mascote, animais/figuras, medalhas, topo, fases, rodapé). Facilita manutenção e evita duplicatas.
- **FASES como objeto:** cada fase tem `titulo`, `cor`, `desafios` (tipo `"regra"`/`"escolha"`) ou especial (`"ordem"`, `"memoria"`, `"caca"`, `"frase"`, `"explicar"`, `"criar"`, `"junte"`).
- Campo `ilustra`: `{tipo, n}` ou `{grupos:[...], comparar:true/false}`.

### Cuidado com funções duplicadas (lição crítica)
Ao reformular, é fácil deixar DUAS versões da mesma função — a última sobrescreve silenciosamente e quebra a fase sem erro visível. Sempre `grep -c "function nome("` → deve ser **1**. Ao remover duplicatas, fazer por balanceamento de chaves, preservando funções essenciais no mesmo bloco. Conferir variáveis globais que podem ter sido apagadas junto (`var ANIMAIS`, `FASES.x`).

### VALIDAÇÃO OBRIGATÓRIA — 3 NÍVEIS (antes de entregar, executando, não de memória)
**NÍVEL 1 — DEV:** (1) modo estrito `new Function('"use strict";'+js)` sem erro; (2) zero JS moderno; (3) zero CSS moderno; (4) nº `@keyframes` == nº `@-webkit-keyframes`; (5) zero funções duplicadas; (6) zero variável acentuada; (7) CSS de imagem robusto (nada que colapse, mascote pela altura, glow com drop-shadow).
**NÍVEL 2 — QA:** (8) play-through de TODAS as fases (simulador `node sim.js` ou Playwright) com **0 erros**, sem overflow em 414/390/360/320px; (9) zero emoji moderno/VS16; (10) toda função de `onclick` existe; (11) embaralhamento REAL (posição da certa varia entre execuções); (12) fala nunca cortada (elogio+explicação inteiros, streak/nível/conquista depois; clicar "Próximo" não corta; trocar de tela corta); (13) adaptatividade (100%→Extra, <50%→Reforço, erros→Treino); (14) mapa (só atual clicável, demais trancadas, conectores, troféu, relatório só no fim, barra de progresso).
  - **QA sem Playwright (Chromium headless + harness injetado — receita testada):** injetar antes de `</body>` um `<script>` que (a) `window.onerror` acumula erros num array; (b) uma função `cena(nome,fn)` roda cada render dentro de `try/catch` e mede `documentElement.scrollWidth-clientWidth` (overflow); (c) percorre TODAS as telas — `telaInicio`, `telaMapa` (0 e N concluídas), `introFase(ch)`+`comecarFase()` de cada parada, `telaMedalhas`, `telaFinal`, `telaPintar` — e ainda os FLUXOS (`fimFase` 100%/baixo, `iniciarExtra`, `fimExtra`, `iniciarReforco`, `levelUp`); (d) despeja `JSON.stringify` num `<div id="QARES">`. Rodar `chrome --headless --window-size=320,900 --virtual-time-budget=9000 --dump-dom` e extrair o JSON por regex. Rodar em 320px E 414px. Para AUTO-RESPONDER (achar a opção certa), casar pelo atributo do botão (`data-cor`/`data-forma`) e chamar o `responder*` com os MESMOS args do `onclick` (ex.: `responderCor(i,cor)` tem 2 args, `responderForma(i,forma,nome,g)` tem 4 — chamar com args errados dá falso "erro" no teste, não é bug do produto).
  - **Ícones utilitários (ex.: botão de tela cheia) também entram no check de emoji/consistência (lição paga):** achei o toggle começando com ⛶ (canto-de-quadrado) e virando ⛛ (triângulo pra baixo, ícone errado) ao alternar. Manter consistente e seguro: `&#9974;` (abrir) / `&#10005;` (✕ fechar). Varrer emojis TAMBÉM fora dos data-URIs base64.
  - **CUIDADO — `--window-size` do Chromium headless NÃO muda o layout viewport (lição paga):** com `<meta viewport width=device-width>`, o headless renderiza tudo num viewport FIXO (~500px) independente do `--window-size`; logo `scrollWidth-clientWidth` dá 0 mesmo em telas onde no celular real quebraria, e o SCREENSHOT em janela estreita só CORTA (não é overflow real). Para testar o layout estreito DE VERDADE, forçar por CSS injetado `#wrap{max-width:340px}` e renderizar numa janela LARGA (aí você vê o layout de ~360px sem clip). Vale sobretudo pra TABELAS e grades de largura fixa.
**NÍVEL 3 — PEDAGOGO:** (15) matemática/conteúdo consistente (resposta nas opções, produtos/divisões corretos, divisões exatas, zero opções duplicadas); (16) concordância n=1 E n>1 (tela E fala; forçar 1 ponto/1 medalha, varrer `\b1\s+(plural)`); (17) numExt ACENTUADO ("três"); (18) normalização de pronúncia cobre as palavras; (19) narração não entrega resposta (nada declarativo após o "?"); (20) enunciados coerentes + explicações verdadeiras; (21) português impecável (varrer palavras sem acento); (22) imagens conferidas (cor/mosaico, transparência real, sem franja/sombra/vão, mascote não sobrepõe).
**ENTREGA:** (23) único `index.html` (sem cópia com nome descritivo); (24) relatar honestamente o cumprido e o pendente.

================================================================
## 14. DESENHOS SVG (quando usados — fallback)
================================================================
- Personagens/objetos-chave em SVG inline só quando não houver PNG: aparecem idênticos em qualquer navegador.
- Ex.: coelho, passaro, urso, macaco, joaninha, gato, cachorro, abelha, rato, tartaruga, elefante, tigre, pinguim, sapo — via `svgAnimal(tipo, tam)`. Objetos: maçã, estrela, bolinha — via `svgObjeto()`.
- Animar suavemente (par `-webkit-`). Se um SVG falhar no PC antigo real, trocar por imagem PNG.

================================================================
## 15. PUBLICAÇÃO (fluxo do Marcos)
================================================================
1. Cria/refina no chat → baixa `index.html`.
2. Publica via **Claude Code** (nuvem): cria repo no GitHub + ativa GitHub Pages + retorna o link.
3. Cola o link no **Invertexto** (organizador de links para os alunos).

================================================================
## 16. FERRAMENTAS DO PROJETO
================================================================
- **Claude Code** — publicar no GitHub Pages.
- **ChatGPT** — gerar cartelas de imagem (sempre cartela única!).
- **PIL + scipy (Python)** — flood-fill/componentes conectados, de-fringe, limpeza de sombra/vão/franja, base64, mosaico de conferência.
- **Playwright** — validação de render (screenshot + play-through).
- **Node.js** — validação modo estrito e simulador (`node sim.js`).
- **Invertexto** — encurtador/organizador de links.
- Este manual é a referência de regras; o ATIVIDADE-PREMIUM.md é a referência de formato. Claude não edita os arquivos do projeto — entrega trechos prontos para o Marcos colar.

================================================================
## 17. RESUMO DE POSTURA
================================================================
- **Premium é o padrão, não o extra.** O checklist premium é obrigatório nos DOIS cenários (criar e upgrade). Não existe "premium parcial". Num upgrade, completar o que falta é parte do trabalho — não depende do Marcos pedir item por item. Se algo obrigatório não puder ser feito, APONTAR a pendência com honestidade.
- **NÃO inventar nada fora do modelo** (ATIVIDADE-PREMIUM.md): nem botão, nem animação, nem disposição própria. Na dúvida sobre qualquer detalhe, PERGUNTAR antes de fazer diferente.
- **Nunca correção automática em massa** (ex.: reprocessar todas as imagens) sem verificação visual; ambíguo = segurar e perguntar. Asset suspeito (cor não bate, medalha que não parece medalha) = levantar os fatos e PERGUNTAR, não corrigir sozinho.
- TODOS os assets-chave são IMAGEM do ChatGPT (sem fundo, com animação suave) — nunca SVG/emoji para mascote/ilhas/companheiros/emblemas/medalhas/selos/troféu/recompensa. Trocar SVG→imagem faz parte do upgrade.
- História RICA com FINAL SUPER FANTÁSTICO; tudo coerente com o enredo, nada solto.
- Engajamento = querer voltar para APRENDER (competência + progresso), nunca compulsão. 4 pilares + streak, tudo ligado ao mérito real.
- Dose certa: ~5-6 desafios por fase, ação variada, jogos de alívio no meio.
- Calibrar à série/BNCC: cobrir o conteúdo esperado, não só o seguro.
- Anexou arquivo → transformar a CAMADA, preservar conteúdo (Cenário A). Descreveu tema → criar do zero já premium (Cenário B).
- Mapa CONTA A HISTÓRIA (início/meio/fim ligados ao enredo, com nome do aluno; botão "Ouvir" reconta).
- Fases de contar têm apoio ao erro por contagem acesa (acende objeto a objeto EM SINCRONIA COM A FALA — a voz diz o número e a luz acende junto; encadeado pelo callback do `falar`, nunca por timers fixos separados).
- Peças (medalhas/selos) recortadas por componente conectado + margem transparente, exibidas centralizadas com proporção preservada; auditar corte renderizando DURANTE a animação.
- Pronúncia: normalizar acentos no limparFala; streak diz "Você acertou N seguidas".
- Auditoria honesta de pedagogo: apontar furos REAIS (cansaço, falta de degrau da série, fechamento seco), não só elogiar. Verificar de verdade (rodar, contar, testar n=1), não de memória.
- Sempre validar rodando, sempre entregar `index.html`.


================================================================
## 18. ÚLTIMOS APRENDIZADOS (novas lições pagas)
================================================================

**BOTÃO NARRADO — LIBERAR SÓ APÓS SILÊNCIO CONTÍNUO (refina a seção 7):** o botão que só habilita ao fim da narração NÃO pode confiar num teste único de "não está falando / fila vazia". O elogio, o streak, o "subiu de nível" e a conquista entram na fila DEPOIS (por `setTimeout` ~600–900ms); um poll único pode liberar numa FRESTA de silêncio antes da comemoração começar — e o clique corta. Correto: liberar só quando a fala ficar em SILÊNCIO CONTÍNUO por ~650ms (após um mínimo inicial ~700–900ms); se algo for enfileirado nesse meio, o cronômetro do silêncio ZERA e recomeça. Trava de segurança (`setTimeout` ~15s; até ~180s em textos longos de leitura) para nunca ficar preso. Em aparelho sem voz, o `falar` chama o callback na hora → libera (não trava o aluno). Aplicar em TODA tela com narração + botão de avançar.

**NÃO NARRAR SÍMBOLOS, PONTUAÇÃO SOLTA NEM LACUNAS (lição paga):** o TTS lê em voz alta caracteres que só existem no visual — o sublinhado de lacuna ("Complete: gato ___" vira "underline underline"), parênteses, colchetes, chaves, aspas «»“”‘’, asterisco, cerquilha, til/circunflexo soltos, barras, `< > | = + @ •`. O `limparFala()` DEVE, antes de falar: trocar sequências de `_` por espaço (a lacuna vira pausa); colapsar reticências; trocar travessão `—`/`–` por vírgula; e REMOVER os símbolos avulsos (viram espaço); colar `([!?])\s*\.`→`$1`. O que vai ao `falar()` fica só com letras, números e `. , ! ? :`.

**O DÍGITO "2" TAMBÉM TEM GÊNERO NA FALA (complementa a seção 8):** o TTS lê "2" como "dois" (masculino). Em português só **1 e 2** flexionam (um/uma, dois/duas); de 3 em diante o número é invariável. Então "2 baldes" fica certo, mas "2 vacas" deveria ser "duas vacas" e "2 vezes" deveria ser "duas vezes" ("vezes" é feminino). Quando a fala tiver "2" diante de palavra FEMININA, gerar "duas" (por `numExt`/`pluralG`, ou regex no `normPron`: `\b2\s+vacas\b`→"duas vacas", `\b2\s+vezes\b`→"duas vezes"). O bug real que mordeu: a fazendinha falava "duas baldes".

**ENUNCIADO (TEXTO + FALA) BATE COM A FIGURA MOSTRADA:** se a tela mostra ovos, o enunciado/`dd.fala` não pode dizer "maçãs". O bug clássico aparece quando o objeto do desafio é SORTEADO/cicla mas o texto ficou fixo (ou vice-versa). Auditar fase a fase: figura × enunciado × fala × explicação nomeiam o MESMO objeto.

**NOME DA PARADA IDÊNTICO EM TODO LUGAR (lição paga):** o nome de cada parada tem que ser EXATAMENTE o mesmo no `PARADAS` (`n`), no `FCFG` (`titulo`), na medalha (usa `p.n`) e em qualquer citação nos `intro`/`gancho`/narração. NÃO escrever o mesmo nome em duas ordens/variações (caso real: o mapa dizia "Formas da Festa" e o texto dizia "Festa das Formas"). **Prevenção automática:** o `auditar.py` (check 11) compara `PARADAS.n` × `FCFG.titulo` por `ch` e REPROVA se diferirem. Se um `gancho` cita a PRÓXIMA parada pelo nome (ex.: cores → "Contando no Picadeiro"), esse nome também tem que ser o título exato dela.

**ARRASTAR — A IMAGEM DENTRO DO ITEM SEQUESTRA O MOUSE (lição paga, complementa a seção 12):** um `<img>` dentro do arrastável dispara o **drag nativo de imagem** do navegador, que rouba os eventos de mouse (chega 1 `mousemove` e nenhum `mouseup` no document) — o arrastar quebra em PC (funciona na 1ª vez e trava depois, ou nem começa). Consertar: (a) `document.addEventListener("dragstart", ...)` com `preventDefault()` quando o alvo é arrastável; (b) `preventDefault()` no `mousedown` (só mouse, não toque: `if(!e.touches && e.preventDefault)`); (c) CSS `.arrasta{ touch-action:none; }` (impede o scroll do celular roubar o gesto) e `.arrasta img{ -webkit-user-drag:none; }`.
- **PRESERVAR AS CLASSES ao reconstruir o `className` (lição paga — "arrasta na 1ª vez, na 2ª não"):** funções que remontam a classe do zero (`el.className="bicho drag"`) APAGAM as classes `arrasta`/`solta` — depois do 1º drop não há mais zona de arrasto/solta e o jogo trava. Sempre reanexar `arrasta`/`solta` (e o estado, ex.: `hl`).
- **Testar com evento REAL, não sintético:** eventos disparados por JS passam mesmo com o bug do drag nativo. Validar com CDP (`Input.dispatchMouseEvent`) ou toque real; usar `user-data-dir` limpo por teste (páginas reaproveitadas acumulam listeners e mascaram o bug).

**CAÇA-PALAVRAS — INTERAÇÃO POR PONTAS (1ª e última letra):** NÃO pedir para tocar letra por letra numa string que nunca zera (um toque errado embaralha tudo e nada mais é reconhecido — bug real "não funciona"). Certo: a criança toca na PRIMEIRA letra (fica destacada) e depois na ÚLTIMA. Validar a linha reta entre as duas pontas (horizontal, vertical ou diagonal; rejeitar se não alinhadas) e comparar com a lista de alvos NOS DOIS SENTIDOS (frente e de trás pra frente). Ao achar: células verdes, palavra riscada na lista, confete + pontos.

**NOME DE JOGO HONESTO — "PÔR EM ORDEM", nunca "quebra-cabeça" (corrige a seção 12):** para a fase de ORDENAR elementos (do menor ao maior), o nome anunciado e a fala do enunciado dizem "arraste/ponha em ordem", NÃO "monte o quebra-cabeça" (isso é a outra fase, a de fatiar a foto 2×2). E o ordenar é ARRASTAR primário (toque reserva), como toda mecânica de "levar um item a um lugar".

**MONTAR A CONTA — MULTIPLICAÇÃO É COMUTATIVA:** na fase de montar a conta de multiplicação, aceitar os operandos em QUALQUER ordem (3 × 5 = 15 e também 5 × 3 = 15) — validar contra as sequências aceitas por comutatividade (trocar os operandos ao redor do "×"). A DIVISÃO NÃO é comutativa (6 : 2 ≠ 2 : 6): só a ordem correta vale.

**MODO PROFESSOR — senha mestra `1275@` (recurso padrão opcional):** digitar `1275@` no teclado a QUALQUER momento LIGA/DESLIGA o "modo professor", que destrava todas as fases no mapa para teste (digitar de novo volta ao normal). NÃO altera o progresso real do aluno — só uma flag `_adminLivre` muda as travas exibidas no mapa. NÃO é segurança (a senha fica visível no código-fonte) — é atalho de conveniência; funciona em teclado físico (PC). Ganchos: (1) um listener de `keydown` acumula as últimas teclas e compara com a senha; ao bater, inverte `_adminLivre`, mostra um toast e re-renderiza o mapa; (2) bypass `if(_adminLivre){ return true; }` no INÍCIO da função central de liberação de fase (`liberada(chave)`/`faseDesbloqueada(i)`); (3) se o FINAL/troféu tiver gate por contagem num `onclick`, somar `|| _adminLivre`. Emoji do toast: 🔓 / 🔒 LITERAIS (nunca escapes `\U0001F513`, que em JS viram texto "U0001F513").

**PROVA/QUIZ COM RELATÓRIO EM PLANILHA (Google Apps Script):** para o professor receber nome + turma + nota numa planilha, usar um Web App do Google Apps Script (`doPost(e)` com `appendRow`) como backend gratuito de um site estático; o jogo faz `fetch(URL, {method:"POST", mode:"no-cors", headers:{"Content-Type":"application/x-www-form-urlencoded"}, body:...})`. A NOTA vai na escala 0 a 10 (`Math.round(ac/total*100)/10`, vírgula no pt-BR), com os acertos "ac/total" numa coluna à parte. A URL do Web App vive no `index.html` (é do próprio professor, não é secret).

**TELA DE LEITURA ANTES DA PROVA (quiz com texto):** quando a prova pede um texto de leitura antes das perguntas, usar um LEITOR GENÉRICO por índice (`telaLeituraN(n)` sobre uma lista `LEITURAS=[{img,texto,titulo,deco}]`), permitindo vários textos em sequência (texto 1 → texto 2 → prova). Cada tela: a imagem do texto EMBUTIDA em base64 (self-contained — o `republicar-limpo` espelha só o `_novo`, então imagem solta no repo some), narração automática do texto ao abrir, botão "🔊 Ouvir o texto" (reouvir), e o botão de avançar (Próximo/Começar a prova) só habilita ao FIM da narração (mesma trava do botão narrado). Ao avançar, `speechSynthesis.cancel()` para a narração. Uma ilustração pode reusar imagem já embutida na prova (resolver em tempo de render, ex.: `OBJ[chave]`, para não quebrar no load se o objeto é definido depois).

**SCREENSHOT HEADLESS ≠ VIEWPORT REAL (lição paga — falso "estouro"):** o Chromium headless às vezes faz o layout num viewport MAIOR (ex.: 500px) do que o `--window-size` pedido, então o screenshot sai CORTADO à direita e PARECE que a imagem estourou a largura — quando NÃO estourou. Antes de "consertar" um overflow aparente, MEDIR: injetar um script que reporta `window.innerWidth`, `document.body.scrollWidth` e o `offsetWidth` do card/imagem. Se `bodyScroll ≤ innerWidth`, não há overflow real — é só o screenshot mais estreito que o viewport; renderizar com a janela = viewport para conferir de verdade. `max-width:100%` (padrão) escala a imagem no container e funciona; não trocar por `width:100%`/`vw` achando que conserta. (Corolário: o headless "prende" a largura mínima em ~500px — não dá pra testar um celular de 320/360px por `--window-size`; nesses casos, CALCULAR o overflow na mão pela soma das larguras+margens dos elementos por linha.)

**TELA CHEIA PRECISA AUMENTAR O JOGO, NÃO SÓ A MOLDURA (lição paga — "dá tela cheia mas o jogo não aumenta"):** alargar só o container (`.wrap max-width`) por media query NÃO resolve — os elementos do jogo (cartas da memória 70px, células da caça 27px, teclas, peças) têm tamanho FIXO em px e continuam pequenos, agrupados no centro, com espaço vazio em volta. Pior: NO CELULAR a tela cheia **não muda a largura do viewport** (só esconde a barra do navegador), então as media queries de `min-width` nem disparam e nada cresce. Correção que serve pros dois casos: nos listeners de `fullscreenchange` (todos os prefixos, já usados pra trocar o ícone) alternar uma classe no body — `body.tc-ativa` — e no CSS AUMENTAR os elementos do jogo sob essa classe (ex.: `body.tc-ativa .memCarta{width:96px;height:96px}`, células da caça 34px, teclas/peças/títulos maiores, `.wrap max-width:820px`). Assim o tabuleiro cresce de verdade em tela cheia, inclusive no celular; ao sair, a classe some e volta ao normal. CUIDADO com overflow horizontal em telas estreitas: dimensionar pela pior largura (ex.: caça 8×34+padding ≈ 292px cabe em 320px; memória 96px+margem quebra em 2–3 por linha com `flex-wrap`, sem estourar). Ao remover a classe, usar `className.replace(/\s*tc-ativa\b/g,"")` (não zerar o className, que apagaria `tem-botao-tc` e outras).

**IMAGEM DE ABERTURA/FINAL COMO MEDALHÃO REDONDO (PADRÃO FIXO — aplicar em TODA atividade):** "será sempre desse jeito": a foto grande da tela inicial (e da tela final) de QUALQUER atividade nova ou revisada deve nascer como CÍRCULO — não um retângulo largo. Já aplicado em Vila do Miau, Poli e Climas do Mundo; ao mexer numa capa retangular antiga, converter. A foto grande da tela inicial (e da tela final) fica mais bonita como um CÍRCULO — não um retângulo largo. Padrão: `border-radius:50%`, tamanho fixo quadrado (ex.: 220px, subindo p/ 260px em `min-width:700px`), `object-fit:cover` + `object-position:center` (recorta no centro SEM distorcer — a foto landscape vira círculo mostrando o miolo, ex.: o mascote), borda clara translúcida (5px) no TOM da atividade, `box-shadow` dupla (sombra + anel), e uma animação suave de flutuar (`@keyframes boia`: `translateY` de ~-9px + leve `scale`/`rotate`, 4.5s infinita). Prefixos `-o-object-fit`/`-webkit-`/`-moz-` para PCs antigos. Mesma classe serve p/ abertura e final. Conferir por screenshot que o recorte central pega o personagem (se a foto tem o foco fora do centro, ajustar `object-position`).

**TTS — CUIDADO COM JUNÇÕES QUE VIRAM OUTRA PALAVRA (liaison, lição paga):** o sintetizador de voz JUNTA palavras vizinhas e às vezes o resultado soa como uma palavra diferente. O caso real que mordeu: "ligou todos os bichinhos **às sombras**" — o TTS colava "às sombras" e saía soando como o verbo **"assombras"** (assombrar). Isso não tem entrada no `limparFala`/mapa de pronúncia (a grafia está certa), então NÃO adianta procurar bug no código — a correção é REESCREVER a frase pra desfazer a junção. Preferir o SINGULAR ou reordenar: "ligou **cada bichinho à sombra** certinha dele" (bônus: bate com a intro da fase). Ficar atento a `a`/`às`/`as` + palavra começando com `s`/vogal, `de`+vogal, `com`+`o`, etc. Como não dá pra OUVIR o áudio em teste headless, ler a frase em voz alta mentalmente e, na dúvida, reescrever.

**FILA HORIZONTAL: LARGURA FIXA NO CONTAINER VIRA GRADE (lição paga — "tem que ser uma fila"):** quando os itens devem ficar numa ÚNICA LINHA horizontal (ex.: ordenar peixinhos do menor ao maior — a intro até diz "nadar em fila"), um `width` FIXO e estreito no container de `inline-block`/`flex` (ex.: `.slots{width:184px}`) faz os itens QUEBRAREM em várias linhas = vira grade 2×N, não fila. Correção: no modo fila, `width:auto; max-width:100%; white-space:nowrap;` (impede a quebra) e DIMENSIONAR os quadros/peças pela PIOR largura pra caber todos (ex.: 4 itens a ~64px+margem ≈ 280px cabem em 320px); `overflow-x:auto` só como rede de segurança em telas minúsculas. Aplicar por uma CLASSE modificadora condicional (ex.: `.slots.fila`) para não afetar outras fases que usam o mesmo render. Medir por screenshot que ficou `linhas=1` e sem overflow.

**TRAVA DE ÁUDIO NUM SÓ PONTO — GATEAR DENTRO DO `falar()` (padrão DRY, lição paga):** quando a atividade tem MUITOS botões "Próximo" espalhados (um por tipo de feedback: escolha, completar, montar, classificar…), NÃO saia editando cada um. Como TODO feedback chama `falar(texto)` logo depois de inserir o botão, dá pra gatear num ÚNICO lugar: no começo do `falar`, uma função `_gatearAvanco()` varre o container de tela (`#app`) e DESABILITA só os botões de AVANÇAR — identificados por `onclick` conter `"proximoDesafio"` OU pela classe marcadora `gate-audio` (que você põe nos botões de abertura/fim de fase). Ela retorna um `liberar()`; o `falar` encadeia esse `liberar` no seu callback de término (`cb`, junto do `aoTerminar` original) + um `setTimeout(liberar, 20000)` de segurança. Assim um só gancho cobre todos os feedbacks e as telas narradas (abertura, fim de fase), sem tocar nos botões de AÇÃO (ex.: "Conferir", que não têm esses marcadores). Botão travado ganha classe `travado-audio` (CSS: opacidade, sem pulsar, cinza). Em navegador sem voz, o `falar` chama `cb` por `setTimeout` → libera (não prende o aluno). Testar em headless: montar um `#zonaFeed` sintético com o botão, chamar `falar`, conferir `disabled=true` logo após e `disabled=false` depois (sem voz, ~300ms).

**FLUXO DE IMAGENS DA PROFESSORA — PASTA `_imagens/` (sem chat, sem base64 na mão):** o Claude NÃO gera imagens (só o prompt), e a professora às vezes não consegue anexar imagem no chat. Fluxo padrão: ela sobe os arquivos direto neste repo, na pasta **`_imagens/`** (pelo github.com, funciona no celular: Add file → Upload files), com nomes simples (só minúsculas/números/hífen: `mascote.png`, `capa.png`, `texto1.png`), formatos png/jpg/webp, e avisa "subi em `_imagens`". Então: `git pull` → Read a imagem → Pillow (autocrop `getbbox`, redimensiona, `optimize`) → embute como base64 (data URI) na atividade. Ela não mexe em código nem em base64. Guia curto vive em `_imagens/LEIA-ME.md`.

**REGRAS FIXAS DE IMAGEM (preferência da professora — "será sempre desse jeito"):**
- **SEMPRE imagem de verdade (ChatGPT/DALL·E), NUNCA SVG.** A prof NÃO quer mascote/figuras em SVG. Se faltar imagem, o certo é PEDIR a imagem (dar o prompt), não cair pra vetor. (O SVG de reserva `svgMascote`/`svgCena` só existe como fallback técnico se a imagem não carregar — não é o visual pretendido.)
- **Ao criar/atualizar uma atividade, entregar uma LISTA de prompts** — um por imagem — já com o **nome do arquivo** que cada uma deve ter (`capa.png`, `mascote-feliz.png`, `q1-vulcao.png`…). A prof gera tudo no ChatGPT, sobe em lote em `_imagens/` e avisa.
- **IMAGENS DE CONTEXTO NAS QUESTÕES (padrão premium, igual Vila do Miau):** além de capa e mascote, as QUESTÕES ganham imagem própria (uma por questão que pedir), deixando colorido e divertido pras crianças. Incluir essas imagens na lista de prompts.
- **LIMPAR `_imagens/` depois de embutir:** assim que as imagens viram base64 dentro da atividade, APAGAR os arquivos da pasta (`git rm _imagens/<arquivo>` + commit), deixando só `LEIA-ME.md`. A pasta fica **sempre vazia** — a prof pediu isso.
- Otimizar cada imagem (Pillow, `optimize`, dimensão adequada) pra não inchar o HTML; muitas fotos base64 pesam.

**NARRAÇÃO ROBUSTA — A CORRIDA `cancel()`→`speak()` PRENDE O BOTÃO (lição paga — "erra, depois acerta e o botão não libera"):** quando uma nova fala começa logo após cancelar a anterior (ex.: feedback do ERRO tocando e a criança já ACERTA), o `speechSynthesis` de vários navegadores (sobretudo celular) BUGA: o `onend` da nova fala não dispara, o áudio "não termina" para o código, e o botão gateado por áudio fica preso até o timer de segurança. Padrão robusto: (1) detectar o fim pelo POLL de `speechSynthesis.speaking` (não confiar só no `onend`), liberando ~90ms após o áudio parar; (2) um CONTADOR de sequência `_falaSeq` incrementado em `pararFala()` — cada `falar` guarda `meuSeq` e toda continuação (`prox`) aborta se `meuSeq!==_falaSeq` (a fala nova invalida a antiga, sem vazamento); (3) LIMPAR o `_pollAtivo` da fala anterior no `pararFala` (senão o poll velho volta a rodar); (4) iniciar a nova fala com um pequeno ATRASO (~130ms) após o `cancel()` e chamar `speechSynthesis.resume()` antes do `speak()` (destrava a fila pós-cancel); (5) teto de segurança do gate curto (~9s, não 20s) pra nunca prender demais. Testar o fluxo ERRAR→ACERTAR: o botão "Próximo" tem de aparecer e liberar.

**NÃO CONTORNAR PROBLEMA DE VOZ TIRANDO A PALAVRA DA LIÇÃO (lição paga):** se o TTS lê mal uma palavra que É o conteúdo (ex.: "cor" numa atividade de cores), NÃO reescreva a frase pra remover a palavra — a explicação é sobre ela. O certo é: (a) garantir texto == fala (mesma string); (b) escolher a MELHOR voz pt-BR do aparelho (pontuar por `pt-BR` + `natural/neural/google/microsoft` + nomes br + `localService=false`) e tom natural (pitch ~1.04, rate ~0.97); (c) se ainda ler errado, dar a PRONÚNCIA da palavra foneticamente só na fala (tela ≠ fala), nunca apagar a palavra. E lembrar do CACHE: "voz/texto errado que já foi corrigido" quase sempre é cache — testar com `?v=N`. **Caso real:** a voz do aparelho lia a palavra "cor" (fim de frase) como "cor-reto/correto"; conserto = no `limparFala`, `\bcor\b`→"côr" e `\bcores\b`→"côres" (a pronúncia entra SÓ na fala; a TELA continua mostrando "cor"). Objetos vazados (argola/aro) precisam do FURO transparente: tornar transparente a maior região branca ENCLAUSURADA (que não toca a borda do recorte).

**NÚMEROS COMO IMAGEM (cartela de números — lição paga):** a prof prefere os números das opções como IMAGEM colorida do tema, não texto/botão. É a ÚNICA cartela em que a IA costuma errar algarismos — PEDIR "1 a 10, algarismos grandes e legíveis, contorno preto, sem outras letras" e CONFERIR algarismo por algarismo (regerar se sair torto). Recorte: o "10" são DOIS glifos (1 e 0) que precisam ficar JUNTOS — não usar componente-conectado puro (separaria); cortar por LINHA + agrupar por GAP (numa linha de K números, os K-1 MAIORES vãos horizontais separam os números; o vão menor, dentro do "10", junta 1+0). Miolo/contador dos algarismos vazados (0, 4, 6, 8, 9) tem de ficar TRANSPARENTE (região branca ENCLAUSURADA que não toca a borda) — **cuidado com o LIMIAR de área**: o miolo do "4" é um triângulo pequeno (~75px) e pode cair abaixo de um limiar fixo (ex.: 90px) e ficar branco; baixar o limiar (bolinhas decorativas normalmente são coloridas, não brancas, então não são furadas). Números na tela = soltos e flutuando (sem caixa de botão).

**AUDITORIA OBRIGATÓRIA ANTES DE CADA PUBLICAÇÃO (regra da prof — não só na entrega final):** rodar a auditoria ANTES de TODO `atualizar`/`republicar`, mesmo em mudanças pequenas — foi um erro de concordância publicado ("um parada") que gerou essa regra. Existe um script pronto: **`_circo/auditar.py <index.html>`**, que checa: tokens de imagem não resolvidos, `node --check`, JS moderno proibido (`=>`/`let`/`const`/crase/`?.`/`??`/`async`/`await`/spread), **funções duplicadas**, variável com acento, **CONCORDÂNCIA** (dígito "1"/número + substantivo feminino dentro de `falar(...)`), CSS moderno (`grid`/`gap`/`clamp`/`var(--)`), keyframes pareados e `onclick` sem função definida. Só publicar se der **APROVADO** (avisos são para conferir). Além disso, para concordância, forçar mentalmente o cenário n=1 (1 parada/medalha/ponto) e conferir a FALA.

**VALOR ALEATÓRIO NO TEXTO E NA FALA = CALCULAR UMA VEZ (lição paga — "a explicação fala diferente do que está escrito"):** quando um valor SORTEADO (elogio variado, frase de festa, número aleatório) aparece TANTO no texto da tela QUANTO na narração, ele precisa ser calculado UMA vez e guardado numa variável, reusada nos dois. Chamar `elogio()` (ou qualquer função com `Math.random`/índice que avança) SEPARADAMENTE para o `innerHTML` e para o `falar()` faz a tela mostrar um elogio e a voz dizer OUTRO — a criança/professora percebe na hora que "a fala não bate com o texto". Certo: `var el=elogio(); tela=...el...; falar(el+...)`. Vale para todo par tela+fala com conteúdo variável.

**DICA/INSTRUÇÃO COM DESTAQUE DE LUZ, NÃO CAIXA PONTILHADA (preferência da prof):** o textinho de instrução/dica das fases ("Olhe bem na cor que o Teo pediu") NÃO leva caixa com borda tracejada/pontilhada (fica "comprimida" e pesada). Padrão: texto solto, itálico, com **brilho de luz suave** (`text-shadow` dourado, ex.: `0 0 10px rgba(255,205,110,.75)`) e um leve respiro de opacidade (`@keyframes` só de `opacity`, ~2.4s). Fica mágico e chama a atenção da criança sem poluir. Vale para dicas e instruções em geral.

**TRANSIÇÃO DE TELA EM FADE (opção em avaliação — confirmar com a prof antes de virar regra):** o card pode surgir só com **fade de opacidade** (curto, ~.35s), sem deslize `translateY` — fica mais calmo para a pré-escola. NÃO é regra fixa ainda: foi sugestão do Claude, aguardando a prof decidir se adota em todas ou mantém o `cardSurge` com deslize suave. (Registrar como fixo só depois do OK dela.)

---

## Especialista em Games Educativos (5º chapéu) — base de pesquisa + cursos

**Quem é / quando atua:** um dev-designer de **jogos educativos** com bagagem de **pesquisa
acadêmica** e do que se ensina em **cursos de game design**. Veste junto com os outros 4 chapéus:
na FASE 1 ("o que esta atividade tem que fazer como JOGO, e não só como exercício?") e na FASE 3
("isto está divertido E ensinando de verdade?"). **Base em fonte, não em achismo** — referências no
fim da seção. Esta bagagem foi levantada em pesquisa (pedido do Marcos: "consultada na internet e
em cursos") e vira barreira via o checklist abaixo.

### Os fundamentos que ele traz (os frameworks que os cursos ensinam)

1. **Teoria da Autodeterminação (SDT) — o motor da motivação.** Três necessidades a satisfazer:
   **Autonomia** (a criança tem escolha/controle), **Competência** (sente que consegue, com desafio
   na medida) e **Relacionamento/Pertencimento** (mascote, "nós", elogio caloroso). Meta-análise:
   a gamificação eleva motivação intrínseca, autonomia e pertencimento — mas **a competência só
   melhora se a dificuldade for adaptada** à criança (nem fácil demais, nem difícil demais).

2. **Malone — o que "prende":** **Desafio** (metas claras, resultado incerto), **Fantasia**
   (história/mundo) e **Curiosidade** (surpresa, "o que vem na próxima?"). → nosso mapa-aventura,
   mascote, ilhas e "próxima página".

3. **Flow — a dificuldade na medida certa.** Engajamento profundo surge quando **desafio ≈
   habilidade**: fácil demais = tédio; difícil demais = frustração. Por isso **dificuldade
   adaptativa (Extra/Reforço) não é enfeite — é o que segura o flow.** As condições de flow mudam
   com a idade/série.

4. **Os 4 princípios do aprendizado por jogo digital (DGBL):**
   - **Interatividade significativa** (mão na massa: arrastar, ligar, ordenar, tocar no mapa, ler
     gráfico — **não** só "clique em A/B/C"). Foi exatamente o salto de nível do *climas-do-mundo*.
   - **Imersão** (animação, som, personagem, papel de "explorador").
   - **Feedback eficaz** (pontos, níveis, mensagens): o **elogio motiva**; a **explicação ensina**.
   - **Liberdade de explorar sem medo de errar** (errar e tentar de novo, sem punição).

5. **MDA — como o designer pensa:** **Mecânica → Dinâmica → Estética.** O designer constrói a
   *mecânica* (regra/ação); dela emerge a *dinâmica* (o comportamento que aparece); o jogador sente
   a *estética* (a emoção). O jogador vive na ordem inversa: **sente primeiro**. → ao criar uma
   fase, decidir a **emoção-alvo** (curiosidade? orgulho de acertar?) e desenhar a mecânica pra ela.

6. **"Juiciness" / game feel:** feedback audiovisual **imediato e generoso** a cada ação (confete,
   som, o número que sobe, o "pulsa"). É o que faz o jogo parecer **gostoso de tocar**. → nossos
   `confete`, `somAcerto`, `pulsa`, streak são exatamente isto — usar sempre.

### Checklist do especialista (aplicar em TODA atividade nova — "vira barreira")

- [ ] **Mão na massa > clique-na-resposta:** a atividade tem mecânicas **táteis variadas**
  (arrastar/ligar/ordenar/tocar/ler gráfico), não só múltipla escolha? (Meta de variedade: o Circo.)
- [ ] **Dificuldade na medida (flow):** tem **Desafio Extra** (100%) e **Reforço** (<50%)? A curva é
  fácil→difícil?
- [ ] **Autonomia:** a criança **escolhe** algo (ordem das fases, aceitar o Extra)?
- [ ] **Competência visível:** progresso claro (barra, "X de N", níveis, medalhas, selos)?
- [ ] **Pertencimento:** mascote com personalidade que **fala com a criança**; elogio caloroso?
- [ ] **Feedback imediato e "juicy":** som + animação + confete a cada acerto; o erro **explica sem
  punir**?
- [ ] **Fantasia + curiosidade:** história/mundo que dá vontade de ver a próxima tela?
- [ ] **Liberdade de errar:** dá pra tentar de novo sem castigo?
- [ ] **Emoção-alvo (MDA):** eu sei qual sentimento a fase quer provocar — e a mecânica serve a ele?
- [ ] **Idade certa (SDT + Flow variam por série):** a mecânica e o tom batem com o ano (não
  infantiliza 6º–9º; não complica o Pré)?

> **Como isso muda o que a gente faz:** menos "quiz puro"; toda atividade nova deve ter pelo menos
> **uma mecânica tátil-assinatura** ligada ao conteúdo (como o climograma/mapa-múndi/ligar no clima).
> A base-mãe (Circo) já entrega SDT+feedback+flow; o especialista garante que a **variedade de
> mecânica** e a **emoção-alvo** também estejam lá, não só os "recursos" da lista do auditor.

### Fontes (a "consultada na internet e nos cursos")
- Principles for educational game development for young children — *Journal of Children and Media* (Tandfonline / ResearchGate).
- Designing Engaging Games for Education: a Systematic Literature Review on Game Motivators and Design Principles (ResearchGate).
- Principles and Best Practices of Designing Digital Game-Based Learning (ERIC EJ1297914).
- Malone — Intrinsically Motivating Instruction (learning-theories.com); Prensky — Digital Game-Based Learning; Gee — *good video games & learning*.
- Self-Determination Theory em gamificação (SCOPE Journal; University XP) e meta-análise "Gamification enhances intrinsic motivation, autonomy and relatedness…" (*ETR&D*, Springer, 2023).
- Age-Aware Gamification Mechanics for Multimedia Learning (arXiv 2512.15630).
- MDA: A Formal Approach to Game Design (Hunicke, LeBlanc, Zubek) — via yukaichou.com / FutureLearn; "juiciness"/game feel (estudos de engajamento).

> Manter estas fontes como ponto de partida; quando o Marcos quiser aprofundar em algum curso
> específico, atualizar esta seção com o que ele trouxer.

### Caixa de ferramentas do especialista — LEQUE de mecânicas interativas + COMO fazer

Referência de amplitude: **H5P** (biblioteca aberta com 50+ "content types" interativos, todos
testados para acessibilidade **WCAG 2.1 AA**) — é o cardápio consagrado de atividade interativa em
educação. Abaixo, o leque adaptado à **nossa stack** (1 HTML, compat SAGRADA, base64), dizendo
**COMO fazer cada uma aqui**. Cross-ref: catálogo por idade na **seção 12**, e o **motor de
arrastar (GHOST global)** já documentado ("Sistema de arrastar").

> **REGRA DE OURO da interação (compat + acessibilidade):** o **arrastar nativo do HTML5
> (`draggable`) NÃO serve** — falha no touch e em PC antigo. Duas formas válidas: **(1) TOQUE-TOQUE**
> (toca na origem, toca no destino) — a mais acessível e à prova de touch ruim, **preferir sempre
> que der**; **(2) ARRASTO por PONTEIRO** — o **motor GHOST global** (mousedown/touchstart + move +
> up/end no `document`; ghost `position:fixed` seguindo o dedo; `elementFromPoint` no alvo), usar
> quando o GESTO de arrastar é parte do sentido (ex.: levar a sombra até o objeto). H5P sempre
> oferece alternativa por teclado/toque ao arrasto — **espelhar isso**. Alvos **≥44px**, contraste
> alto, nunca depender só de cor.

**A) Escolha & leitura**
- **Quiz ilustrado (escolha):** enunciado + figura + 2-3 opções (resposta + vizinhos plausíveis),
  embaralhadas. Base de tudo — mas **não pode ser a única mecânica** (ver checklist do especialista).
- **Verdadeiro/Falso rápido:** 2 botões; ótimo pra "mito ou verdade", com relógio opcional.
- **Ler gráfico/dado (climograma, tabela):** desenhar em **SVG** (barras+linha), interação = tocar
  no ponto certo OU escolher. *Nosso ex.: Estação de Leitura (climas).*

**B) Arrastar & soltar (usar o motor GHOST; oferecer toque-toque alternativo)**
- **Arrasta-e-solta livre (encaixe):** levar item ao alvo certo (letra→palavra, animal→habitat).
- **Categorizar/classificar:** caixas rotuladas + fichas → cada ficha na caixa certa (quente/frio…).
  *Nosso ex.: "classificar" no climas; cesta de adição/subtração no de números.*
- **Ordenar/sequência:** fileira de slots; arrastar (ou **tocar na ordem**) do 1º ao último
  (mais quente→mais frio; passos de uma receita). *Nosso ex.: quebra-cabeça dos climas.*

**C) Palavras (letras & texto)**
- **Caça-palavras:** grade ~10×10 (célula ~27px p/ caber no celular); **interação por PONTAS**
  (toca 1ª e última letra), validar linha reta e comparar **nos dois sentidos** (lição paga —
  seção da caça). *Nosso ex.: Oásis das Palavras.*
- **Palavras cruzadas:** **montar a grade À MÃO** (matriz pré-definida com números e as posições —
  gerar cruzada por algoritmo no cliente é frágil); cada célula = 1 input de 1 letra ou preenche por
  **teclado virtual**; validar célula a célula; dica numerada (horizontal/vertical). Idade: 3º+.
- **Lacuna / completar (fill-in-the-blanks):** frase com espaços; **banco de palavras** que a
  criança **arrasta ou toca** para o espaço (evita digitar nas séries iniciais); comparar
  normalizado (sem acento/caixa). *Ex. próximo: monte-a-frase.*
- **Marque as palavras (mark-the-words):** um texto onde cada palavra é um `<span>` clicável; a
  criança **toca nas certas** (ex.: "marque os substantivos", "ache as palavras do clima quente").
  Verde ao acertar, conta X de N. Ótimo p/ Português/leitura.
- **Forca:** palavra escondida + teclado virtual; erra = parte do desenho; dica temática. *Nosso ex.:
  Iglu das Letras.* (Cuidado: no Pré é frustrante — usar do 2º ano pra cima.)

**D) Associar & memória**
- **Ligar/associar (com linha):** duas colunas; **toca na origem e no par certo** → traça uma
  **linha SVG**; erro pisca vermelho. *Nosso ex.: Trilhas do Clima.*
- **Pares/Memória:** cartas viradas; achar os pares (clima↔característica, palavra↔figura).
  *Nosso ex.: Acampamento das Nuvens.*
- **Flashcards / cartas de diálogo:** vira a carta (frente pergunta, verso resposta); bom p/
  vocabulário/revisão. Implementar com flip por classe (`-webkit-transform`) ou troca de face.

**E) Espacial & visual (tocar na imagem)**
- **Hotspot / mapa interativo:** zonas clicáveis (divs `position:absolute` transparentes) sobre uma
  imagem base64; acerta a região certa. *Nosso ex.: Sala de Mapas (mapa-múndi por faixas).*
- **Achar as diferenças:** duas fotos empilhadas; toca nas diferenças; conta "achou X de N"; toque
  errado só avisa carinhoso (lição paga — ver seção). Idade: todas.
- **Colorir (Pré):** paleta + zonas pintáveis (flood-fill / troca de faixa de cor com cuidado de
  cores repetidas — lição paga). Recompensa/relaxamento no Pré.

**F) Tempo & valor**
- **Linha do tempo (timeline):** eventos que a criança **ordena** ou posiciona; bom p/
  História/sequência. Implementar como "ordenar" horizontal.
- **Slider / termômetro:** um marcador que se **arrasta** numa régua (ou `input range` estilizado
  com par `-webkit-`); "ajuste a temperatura", "quanto de chuva?". Feedback ao soltar.
- **Contar objetos:** bichinhos/objetos fofos; toca/arrasta pra contar; opções = resposta+vizinhos
  (concreto, Piaget — séries iniciais).

**G) Computação (pensamento computacional)**
- **Programe o robô:** monta uma sequência de comandos **clicando** (não arrastando) e roda; ver
  **`ATIVIDADE-COMPUTACAO.md`** (formato próprio, BNCC Computação).

> **Como usar este leque:** na FASE 1, o especialista escolhe **2-4 mecânicas DIFERENTES** que
> sirvam ao conteúdo e à idade (variar a ação, não só o enunciado — seção 5), sempre com **pelo
> menos uma tátil-assinatura** ligada ao tema. Cada mecânica nova que a gente construir e validar
> entra aqui com o "como fazer" + a lição paga, pra virar patrimônio reutilizável.
>
> Fontes do leque: catálogo **H5P** ([content types](https://h5p.org/content-types-and-applications),
> testados p/ WCAG 2.1 AA) e a nossa própria experiência de build (motor GHOST, caça por pontas,
> ligar com linha, hotspots, climograma).

### Estudo de campo — sites de jogos educativos consagrados (referência de mecânica e "feeling")

Além da teoria (H5P/frameworks), o especialista **estuda plataformas reais e conhecidas** para tirar
ideias de **mecânica, ritmo, recompensa e o que engaja a criança brasileira** — e as adapta ao nosso
padrão (dark/premium, compat SAGRADA, 1 HTML). **NÃO se copia jogo nem asset — copia-se a IDEIA de
mecânica e o que funciona.** O que observar em cada um: quais mecânicas usam, como dão feedback, como
calibram a dificuldade por idade, o "game feel".

**Brasileiros (mais próximos do nosso público / BNCC):**
- **Escola Games** ([escolagames.com.br](https://www.escolagames.com.br/)) — anos iniciais do EF,
  com pedagogos, alinhado à BNCC (matemática, português, ciências, geografia, história, inglês, meio
  ambiente). Traz colorir, quebra-cabeça, raciocínio, "eu sei contar", alfabetização com som+imagem.
  Melhor referência de **mecânica simples bem-feita para os anos iniciais**.
- **Coquinhos** ([coquinhos.com](https://www.coquinhos.com/)) — jogos educativos variados, visual
  leve.
- **Racha Cuca** ([rachacuca.com.br](https://rachacuca.com.br/)) — quebra-cabeças, lógica, cruzadas,
  caça-palavras, sudoku, trivia. Referência de **jogos de raciocínio** para os anos finais/adultos.
- **Digipuzzle** ([digipuzzle.net](https://www.digipuzzle.net/)) — enorme variedade de mini-jogos
  (arrasta, encaixa, memória, palavras) — bom "cardápio" de mecânicas.

**Internacionais (referência de polimento e "game feel"):**
- **ABCya** ([abcya.com](https://www.abcya.com/)) — jogos por série (K-6), muito polidos.
- **PBS Kids** ([pbskids.org/games](https://pbskids.org/games)) — jogos com personagem/narrativa,
  ótimo exemplo de **imersão e mascote**.
- (Complementares: ABCmouse, Coolmath Games, Khan Academy Kids.)

> **Como o especialista usa isto:** ao **sugerir tipos** (FASE 1) e ao **construir** (FASE 2),
> lembrar-se de exemplos concretos desses sites ("tipo o 'eu sei contar' do Escola Games, mas com o
> nosso mascote e no nosso padrão"), sempre elevando ao **nível premium** nosso (fotos reais,
> dark, adaptativo, narração, recompensas) — que é o que nos **destaca** frente a esses sites.
> Quando o Marcos trouxer um jogo específico que gostou, registrar aqui a mecânica + o que copiar.

### Gamificação & Narrativa/História — as camadas que envolvem a mecânica

Mecânica é o "como se joga"; **gamificação e narrativa são o que fazem a criança QUERER continuar.**
São as camadas por cima do leque de mecânicas.

**1) Gamificação — os 8 motores (Octalysis, Yu-kai Chou).** Em vez de só "pontos/medalhas/ranking"
(PBL, que é superficial e cansa em 3 semanas), pensar nas **motivações**:
1. **Propósito/Missão** (Epic Meaning): "salvar o Atlas do Clima", "consertar o balão". → dá sentido.
2. **Progresso/Conquista** (Development): XP, níveis, barra, medalhas, "X de N". *← já temos.*
3. **Criatividade & Feedback** (Empowerment): experimentar e ver a resposta na hora. *← feedback juicy.*
4. **Posse/Coleção** (Ownership): colecionar selos, mascotes, o "atlas" que cresce. *← selos/conquistas.*
5. **Social** (Relatedness): comparar, mostrar — *usamos leve* (mascote como "companheiro"; ranking
   entre colegas NÃO, é escola/turma).
6. **Escassez** (Scarcity): "vidas/corações", tempo. **Black Hat — usar com MUITO cuidado com
   criança** (gera ansiedade). No máximo um relógio leve e opcional; nunca punir.
7. **Curiosidade/Surpresa** (Unpredictability): "o que vem na próxima página?", recompensa surpresa. *← "próxima parada".*
8. **Perda/Evitar** (Loss & Avoidance): streak ("não perca a sequência"). **Também Black Hat** — o
   nosso streak é **só mérito e elogio, nunca castigo** (some no erro sem punir). Manter assim.
   > **REGRA para crianças: White Hat > Black Hat.** Priorizar propósito, progresso, criatividade,
   > posse e curiosidade (motores de cima, positivos). Escassez/perda/pressão de tempo só em dose
   > mínima e nunca de forma que castigue ou estresse. (Duolingo usa os 8; pra escola, pegamos os
   > positivos.)

**2) Narrativa/História — o que faz o aprendizado virar aventura.** Pesquisa (serious games):
- **Estruturas:** **Jornada do Herói** (monomito — "chamado à aventura" … "provação/chefão final"),
  **episódica** (paradas/capítulos), **ramificada** (a escolha muda o caminho — personaliza), e
  emergente. → nosso **mapa-aventura narrado** JÁ é uma jornada do herói por episódios (cada ilha =
  uma etapa; a Tempestade Final = o chefão). A **ramificação** (escolher caminhos) é evolução futura.
- **As 4 marcas de uma boa narrativa de jogo** (pesquisa): narrativa **distribuída** (a história
  aparece aos poucos, em cada tela), **fantasia INTRINSECAMENTE INTEGRADA** (a história CARREGA o
  conteúdo, não é enfeite), **personagens empáticos** (o mascote com quem a criança se importa),
  **responsividade** (a história reage ao que a criança faz).
  > **A mais importante — "fantasia integrada":** a história tem que estar **grudada no conteúdo**.
  > Ex. bom: o Nimbo cruza o planeta e *para aprender clima é que ele avança* (a aventura É o
  > conteúdo). Ex. ruim: uma historinha decorativa que podia ser trocada por qualquer tema sem mudar
  > o aprendizado. Sempre perguntar: "se eu tirar a história, o aprendizado muda? Se não muda, ela
  > está solta." (Malone/Habgood: fantasia integrada motiva e ensina mais que fantasia externa.)

**Como o especialista aplica (na FASE 1):** além de escolher as **mecânicas** (leque), desenhar a
**moldura**: (a) uma **missão** com propósito; (b) um **mascote empático** que narra e reage; (c) a
jornada em **episódios** com um **chefão final**; (d) **coleção** que cresce (selos/atlas); (e)
**curiosidade** entre as telas; (f) recompensas **White Hat**. Isso é o que transforma "lista de
exercícios" em "jogo que a criança pede pra jogar de novo".

> Fontes: **Octalysis / 8 Core Drives** (Yu-kai Chou —
> [octalysis](https://yukaichou.com/gamification-examples/octalysis-gamification-framework/)); **Why
> Story Matters — narrative in serious games** (Naul & Liu, 2020); **A storytelling model for
> educational games: Hero's interactive journey** (ResearchGate); "fantasia intrinsecamente
> integrada" (Malone; Habgood & Ainsworth).

### ⚠️ FILTRO DA REALIDADE — TUDO passa pelo PC/navegador ANTIGO da escola (regra que governa o resto)

**Esta é a regra mais importante da caixa do especialista.** Tudo que ele estuda (H5P, Octalysis,
narrativa, Duolingo, Escola Games…) é **INSPIRAÇÃO de IDEIA — nunca de código.** A escola pública do
Marcos roda em **PC antigo e navegador antigo**. Então **toda ideia passa por este filtro ANTES de
virar atividade** — se não passa no PC velho, **não sobe, por mais bonita que seja**:

- **Código:** só `var`/`function`/`for`; **ZERO ES6** (let/const/arrow/template/spread/optional/
  nullish/async/await); prefixos `-webkit-`/`-o-`; **1 HTML único** autossuficiente; **tudo em
  base64** (sem CDN, sem fonte/rede/fetch); emoji ≤ Unicode 6.0; imagens otimizadas.
- **Sem framework/engine:** nada de React/Phaser/Unity/WebGL/canvas pesado. As referências usam
  stack moderna — a gente pega só a **MECÂNICA + o FEELING** e reescreve leve, do nosso jeito.
- **Interação:** **toque-toque > arrastar**; arrasto só pelo **motor GHOST** (mouse+touch); alvos
  ≥44px; nunca depender de gesto fino, hover ou hardware novo.
- **Desempenho:** poucas animações, só `transform`/`opacity`; fundo discreto; nada que "engasgue" em
  máquina fraca; o build do Pages não pode inchar (**portal leve**).
- **Gamificação/narrativa cabem de boa:** as camadas (missão, jornada, coleção, medalhas, streak,
  mascote) são **CSS/JS leves + imagem + texto narrado** — não exigem tecnologia nova nenhuma.
- **Prova final:** **auditor de compatibilidade APROVADO** + play-through headless em 320/414px com
  **0 erro**. Só então publica.

> **Resumo (o nosso diferencial):** a **IDEIA vem do mundo todo**; o **CÓDIGO é sempre à prova de
> escola pública com máquina velha**. Premium **E** roda em qualquer PC — é isso que nos destaca.

### Layout: PREENCHER a tela, mostrar TUDO, sem perder qualidade nem cortar o jogo

**Requisito (pedido do Marcos):** a atividade tem que **usar a tela toda** (cara de app/tela cheia),
com **tudo visível sem zoom nem rolagem** e **sem perder resolução** — **nada do jogo pode ficar
escondido ou cortado**.

**Como conseguir (compat-safe):**
- **Fundo edge-to-edge:** o gradiente/cenário preenche a tela inteira (já fazemos) — dá sensação de
  tela cheia mesmo com o card centralizado.
- **Ajuste-à-tela (fit-to-viewport):** desenhar a atividade num "tamanho de projeto" (ex.: 400×760) e
  um escalonador ajusta pra caber: `escala = min(largura/projW, altura/projH)`, aplicado com
  `transform: scale()` (+ `-webkit-transform`; `transform-origin` topo-centro). Assim **tudo cabe**
  (nada cortado, sem rolagem) e **fica NÍTIDO** — DOM/SVG/texto escalam **vetorialmente**, não borram
  como imagem esticada. Recalcular no `resize`/`orientationchange`. **Limitar o upscale** (ex.: até
  ~1.4×) pra não estourar/borrar; o resto do espaço quem preenche é o fundo.
- **Unidades fluidas onde der:** `vw`/`vh`/`vmin` (existem em navegador antigo); **evitar `clamp()`**
  (não existe no IE/antigos).
- **Imagens com resolução suficiente:** fotos/base64 entram um pouco MAIORES que o tamanho de tela
  (pra escalar sem borrar), mas otimizadas (peso controlado).
- **Tela cheia real (botão ⛶):** o modo fullscreen tem que **AUMENTAR os elementos do jogo**
  (`body.tc-ativa`), não só a moldura — ver a lição paga "TELA CHEIA PRECISA AUMENTAR O JOGO".

**Limite honesto (dizer ao usuário):** preencher **100% em largura E altura** só dá se a proporção do
jogo == a da tela. Quando diferem, a escolha é **mostrar TUDO (nada cortado) e preencher o resto com
o fundo** — **NUNCA cortar o jogo pra preencher**. Regra: *"tudo aparece" ganha de "preencher cada
pixel".*

**Barreira (testar antes de publicar):** renderizar em **320×480** (PC/celular antigo), **414×896** e
numa **tela larga** (desktop). Em TODAS: nada cortado, sem rolagem, nada minúsculo — e o mais cheio
possível sem perder nitidez.

---

## ⭐ PADRÃO 3D VIVO (última geração) — novo padrão premium (decisão do Marcos)

**Decisão:** as atividades premium agora nascem com **imagens 3D geradas, personalizadas ao tema**
(estilo Pixar/última geração) e **TUDO vivo** (animado). É o nosso diferencial — nível de game
comercial, **rodando em PC antigo**. Vale para atividades NOVAS (as antigas ficam como estão até o
Marcos pedir "melhorar").

**1) Imagens 3D personalizadas ao tema** (o Marcos gera; **front-load de TODAS de uma vez**):
- **Mascote temático em 6 poses:** parado (boca fechada), **falando (boca ABERTA)**, acenando,
  comemorando, pensando, apontando.
- **Capa** (cena épica), **tela final/recompensa**, **cartela de gamificação** (moeda, estrela,
  medalhas bronze/prata/ouro, troféu, baú), **cadeado** (fechado/aberto = ilha bloqueada/liberada),
  **ilhas** (ou usar fotos reais de contexto).
- Regras: **arquivo, NÃO print** (print tem a UI do app + baixa qualidade); **fundo TRANSPARENTE**
  nos cutouts/ícones; cenas (capa/final) podem ter fundo; alta resolução.

**2) Recorte/limpeza (lição paga — sempre dá trabalho):** as gerações costumam vir em **fundo
xadrez** (claro OU escuro) ou branco. Pipeline: **matar o fundo** dessaturado (xadrez, `sat<~18`) /
branco puro → **restaurar SÓ buracos pequenos** (dentes/olhos, via *opening* morfológico: erode×N →
dilate×N; buracos grandes = vãos do fundo, ficam transparentes) → **de-fringe** (erodir o anel
claro/dessaturado na borda) → autocrop (`getbbox`) → **resize HD com LANCZOS** (~2× o tamanho de uso,
nítido no pequeno). Conferir SEMPRE no fundo escuro antes de embutir.

**3) TUDO VIVO** (só CSS leve + troca de `src` → roda em PC antigo; **nada de vídeo/WebGL**):
- **Mascote vivo em TODA a atividade:** **respira** (`transform`), **fala com a boquinha**
  (alterna boca-fechada↔boca-aberta sincronizado com a narração), **salta + comemora no acerto**.
  Sistema: classe `js-masc` + `data-pose` no `<img>`; `mascoteFala(on)` liga/desliga dentro do
  `falar()`; `mascoteSalta()` chamado no `somAcerto()`; `nimbo-vivo` (respirar) + `nimbo-hop` (pulo).
- **Capa/telas:** brilho pulsante, **zoom lento (Ken Burns)**, faíscas/partículas, o mascote animado
  na frente.
- **Gamificação:** **moeda gira e voa** até o contador, que **conta subindo**; medalha entra com
  **pop + brilho**; **confete** na vitória.
- Técnica: `@keyframes` de `transform`/`opacity` (par `-webkit-`), troca de `src`, SMIL leve.

**4) Peso & compat — a disciplina que faz CABER (regra de ouro):** 3D pesa → **otimizar forte**:
JPEG (~q80) p/ cenas com fundo, PNG otimizado p/ cutouts, **resize ao tamanho real de uso** (não
embutir 1200px pra mostrar em 100px), base64. Poucas animações simultâneas. **Auditor APROVADO +
play-through headless 0 erro** antes de publicar. Se engasgar em máquina fraca, **aliviar**
(menos animação / imagem menor). O filtro da realidade continua mandando: se não roda no PC antigo,
não sobe.

**5) Front-load (velocidade):** entregar a **cartela COMPLETA de prompts de uma vez** (tudo que a
atividade precisa), o Marcos gera em LOTE e sobe junto, e o Claude **constrói o resto sem idas por
imagem**. Reaproveitar o que já existe (não regerar à toa).
## APRENDIZADOS DA SESSÃO (Climas do Mundo — voz + layout Atlas + mascote)
- **Voz natural (gerar-audio.yml, na main):** o que FUNCIONA hoje = **Google TTS** (`modelo=google`, feminina) e **masculina** = Google TTS + **tom grave via ffmpeg** (`modelo=male`, pitch 0.86; o runner precisa `apt-get install ffmpeg`). StreamElements/Polly = **bloqueado** no Actions (Cloudflare). Pollinations openai-audio **saiu do ar**. **Modo LOTE:** preencher `_lote_falas.json` (`[{"id","texto"}]`) e rodar com input `lote` vazio → gera todas em 1 run em `_audio/<id>.mp3`.
- **Embutir a voz:** base64 num mapa JS `var AUDIO={"id":"data:audio/mpeg;base64,..."}`; `tocarFala(id, textoFallback)` toca o mp3 (senão cai no `falar()` do Web Speech). `tocarFalaAudio` chama `_gatearAvanco()` → **o botão de avançar só libera quando o áudio termina**. Limpar o texto p/ TTS (tirar tags, `(a)/(s)`, `—`, `_`, vírgulas duplas) senão a voz lê estranho.
- **Boca sincronizada:** `mascoteFala(true)` faz a boca abrir/fechar (flip 170ms, troca `.js-masc` entre poses `falando`/`feliz`) enquanto o áudio toca; fecha no `onended`. (Opcional ouro+: dirigir a boca pela AMPLITUDE do áudio via Web Audio AnalyserNode, com fallback no flip.)
- **Mascote SEM perna (recorrente):** o recorte remove as calças/botas escuras → as poses ficam com pernas quebradas e "piscam" ao falar. Conserto sem o original: **cortar as poses num BUSTO consistente** (peito p/ cima, ~0,62 da altura do bbox, autocrop) — todas iguais, nada some ao trocar de pose. (Pillow: getbbox → crop topo → reautocrop → PNG optimize.)
- **Layout Atlas unificado:** capa + mapa = **papel claro**; telas internas via `body.atlas` também papel. Mini-jogos com fundo próprio (grade da caça, teclas, balão de fala escuro) viram "peças" sobre o papel — legíveis. Textos claros → escuros (`#46351f`/`#23384a`); feedback de erro `#a3161a`. NUNCA misturar papel claro (capa) com couro escuro (interno) = o usuário nota a "mistura".

## VOZ PADRÃO DA FÁBRICA (decidido com o Marcos): Edge TTS "Antonio"
- **Voz oficial dos mascotes = `pt-BR-AntonioNeural`** (Microsoft **Edge TTS**): masculina, natural, **GRÁTIS e sem chave**, roda no Actions. É o padrão de `gerar-audio.yml` em `modelo=male`. (Alternativa masculina: `modelo=male2` = "Donato"; feminina: `modelo=female` = "Francisca".)
- **NÃO usar** pitch-shift do Google (soa artificial) nem Gemini TTS (pago). Edge TTS é o padrão.
- **Como o áudio funciona (igual à API de imagem):** manda os textos em lote (`_lote_falas.json`, input `lote` vazio → o workflow lê o arquivo) → gera todos os MP3 em `_audio/<id>.mp3` numa rodada → **embute base64** num mapa `var AUDIO={...}` no HTML → toca com `<audio>`/`new Audio()`. Em runtime **não depende de navegador/internet/API** — a voz vai colada no arquivo, igual em qualquer PC, offline.
- O `gerar-audio.yml` instala `ffmpeg` e `edge-tts` (pip) no runner. `tocarFala(id, fallback)` gate o botão de avançar até o áudio acabar; a boca sincroniza pela **amplitude** do áudio (Web Audio), com fallback no flip por tempo.

---

# 19. PROCESSO PROFISSIONAL — QA e TEMA CLARO (padrão da fábrica)

Decidido com o Marcos: elevar o padrão, **menos erros**, tudo verificado antes de publicar.

## 🧠 NEUROCIÊNCIA DO APRENDIZADO (novo especialista do time — pedido do Marcos)

Um **neurocientista do aprendizado** entrou no time: foco em COMO o cérebro **retém** e
**se engaja**, com as técnicas de maior evidência. Complementa o "especialista em games"
(que cuida de mecânica/emoção). Auditor dele: **`_circo/auditar-pedagogia.py`**.

### Pilar A — APRENDER DE VERDADE (o que fixa na memória)
- **Recuperação ativa (retrieval practice / efeito do teste):** *lembrar* fixa muito mais que
  *reler*. A atividade JÁ é recall — garantir que a criança **produz** a resposta (não só
  reconhece) e variar o formato. *(Roediger & Karpicke; retrievalpractice.org.)*
- **Espaçamento (spaced practice):** rever o conteúdo **mais tarde**, não tudo de uma vez.
  O **Reforço** reapresenta os ERROS depois; intercalar revisão de fases antigas. *(Cepeda et al.)*
- **Intercalação (interleaving):** misturar tipos de problema (não blocos iguais) — o
  `embaralhar`/`MIX_FIXO`. *(Rohrer.)*
- **Feedback imediato e elaborativo:** corrigir na hora **e explicar o porquê** (a `explica`). O
  feedback é o momento em que o cérebro consolida. *(Hattie; Make It Stick.)*
- **Dificuldades desejáveis:** um tiquinho de esforço (não fácil demais) fixa melhor →
  adaptatividade (Extra/Reforço). *(Bjork.)*
- **Codificação dupla (dual coding):** palavra + **imagem** juntas = duas rotas de memória
  (`figura()` + mascote + cenário). *(Paivio; Mayer — multimídia.)*
- **Carga cognitiva baixa (Sweller):** uma ideia por tela, tirar ruído, **narração curta / 1ª
  vez** — liga direto ao anti-cansaço (`narrarTela`, `VOZ_EXPLICA`, feedback curto). Sobrecarga
  = não aprende.
- **Elaboração / "explique":** pedir pra criança **explicar** (Bloom, "explique ao mascote")
  ativa compreensão profunda. **Concreto → abstrato** (concreteness fading).

### Pilar B — QUERER FAZER (não achar chato e realmente fazer)
- **Curiosidade (dopamina antecipatória):** "lacunas de curiosidade", **ganchos** de história,
  surpresa/novidade abrem o cérebro pra aprender e dão vontade da próxima tela (`GANCHOS`,
  cenários variados, mini-jogos). *(Gruber & Ranganath.)*
- **Recompensa & previsão de erro (dopamina):** a recompensa engaja mais quando é ligada a
  **esforço** e um pouco imprevisível; celebrar o **progresso** (confete/medalha) — mas a
  recompensa **intrínseca** (sentir que consegue) vale mais que só pontos.
- **Progresso e meta (goal-gradient):** ver o **Atlas encher** / a barra subir; a motivação
  cresce perto do fim. Sempre mostrar "X de N".
- **SDT — Autonomia, Competência, Pertencimento** (base neurobiológica da motivação intrínseca):
  escolhas, desafio na medida, mascote + nome. *(Deci & Ryan.)*
- **Flow:** desafio ≈ habilidade, metas claras, feedback na hora, **sem interrupção** (não
  travar o "Próximo"!). *(Csikszentmihalyi.)*
- **Mentalidade de crescimento (Dweck):** elogiar **esforço/estratégia** (não "inteligente");
  **normalizar o erro** ("errar e treinar é assim que os cientistas aprendem"). Erro sem medo =
  cérebro aberto.
- **Emoção positiva amplia atenção e memória:** humor, mascote carismático, história — o afeto
  é "cola" da memória.
- **Sessões curtas + pausas:** fases curtas e **jogos de alívio** ajudam a consolidar.

### Checklist do neurocientista (vira BARREIRA — cobre pelo `auditar-pedagogia.py`)
- [ ] Recuperação ativa (produz a resposta, não só reconhece).
- [ ] Feedback imediato **que explica o porquê**.
- [ ] Erro sem punir + frase de **mentalidade de crescimento**.
- [ ] Revisão **espaçada** dos erros (Reforço reapresenta depois).
- [ ] Intercalação (embaralha tipos/itens).
- [ ] Codificação dupla (imagem + palavra).
- [ ] Competência visível (progresso/medalha/nível).
- [ ] Autonomia (escolha) + personalização (nome/mascote).
- [ ] Curiosidade/gancho + celebração "juicy".
- [ ] **Carga cognitiva baixa** (narração curta/1ª vez, uma ideia por tela).

### Fontes (ponto de partida — atualizar quando o Marcos trouxer cursos)
*Make It Stick* (Brown, Roediger, McDaniel); *Understanding How We Learn* e The Learning
Scientists (Weinstein & Sumeracki — "6 strategies"); retrievalpractice.org (Agarwal); spacing
(Cepeda et al.); interleaving (Rohrer); cognitive load (Sweller); multimídia (Mayer);
dual coding (Paivio); desirable difficulties (Bjork); growth mindset (Dweck); SDT (Deci &
Ryan); flow (Csikszentmihalyi); curiosidade & dopamina (Gruber, Ranganath); *How People Learn II*
(National Academies).

## 19.1 Auditor de CONTRASTE (obrigatório antes de publicar)
Ferramenta: **`_circo/auditar-contraste.py <arquivo.html>`**. Abre a atividade no
Chromium headless, percorre **todas as telas** (capa, mapa, desafio e cada
mini-jogo), **desliga o fade/animação e a narração**, e mede o contraste de
**cada texto** contra o fundo efetivo (padrão **WCAG**: ≥ 4,5:1 texto normal,
≥ 3:1 texto grande). **Reprova qualquer texto que "some no fundo"** e sai com
código ≠ 0. Foi criado porque o tema Atlas tinha textos ilegíveis que a gente
não conseguia enxergar (ex.: "Globo Dourado" preto sobre fundo escuro).
- **Regra de ouro:** trocou cor/tema? **Rode o auditor de contraste** e conserte
  até dar **APROVADO (0 texto ilegível)**. Não publique com reprovação.
- Texto sobre **imagem** (ex.: rótulos no mapa-múndi) o auditor pula (não dá p/
  medir com segurança) — esses confira **visualmente** (renderização).

## 19.2 QA visual de TODAS as telas (não só o robô)
O robô (`testar-jogando.py`) prova que **funciona**; ele **não vê** contraste/layout.
Renderize cada tela com o **fade desligado** (`*{animation:none!important;
opacity:1!important}` + narração no-op) e **olhe** — foi assim que enxergamos as
telas de verdade (o fade capturava telas "escuras" que eram só animação).

## 19.3 Checklist de publicação (todo deploy de atividade)
1. `node --check` no `<script>` (JS válido).
2. `_circo/auditar-geral.py` → **APROVADO** (recursos completos).
3. `_circo/testar-jogando.py` → **0 erro jogando**.
4. `_circo/auditar-contraste.py` → **APROVADO** (0 texto ilegível).
5. `_circo/auditar-imagens.py` → **APROVADO** (0 imagem com "restos de outra imagem"
   grudados — recortes com fragmentos soltos. Foi o buraco que deixou passar as
   ilhas e a águia com pedaços de outras cenas, escondidos pelo fundo escuro).
6. `_circo/auditar-som.py` → **APROVADO** (voz CONSISTENTE). Dispara cada narração
   e reprova qualquer uma que caia na **voz do navegador** (feminina, destoa das
   falas gravadas do Nino) em vez do **MP3 embutido**; e valida o mapa `AUDIO`
   (cada entrada é áudio real, e toda chave de `tocarFala("x",…)` existe). Foi o
   buraco que deixou a voz do **mapa** feminina.
7. **Prévia renderizada** das telas-chave conferida (e do usuário, se novo visual).
8. Só então commit + `atualizar.yml` + confirmar `success`.

> **Lição (voz):** narração **dinâmica** (com nome/progresso) cai na voz do
> navegador (costuma ser feminina) e destoa das falas gravadas (masculinas).
> Regra: toda narração fixa OU com variante genérica deve ter **MP3 embutido**
> (`tocarFala(id, fallback)`); o fallback do navegador é só rede de segurança.

### 19.5 A EQUIPE da fábrica (papéis) e o QA de cada um
Para cada frente há um "profissional" **e** um auditor automático que o cobre:
- **Web designer / instrucional** → `auditar-geral.py` (recursos/estrutura).
- **Dev / testador** → `testar-jogando.py` (o robô que joca a atividade).
- **Designer de contraste (acessibilidade)** → `auditar-contraste.py`.
- **Artista / recorte de imagem** → `auditar-imagens.py` (restos soltos).
- **Profissional de som** → `auditar-som.py` (voz consistente, áudios válidos).
- **Neurocientista do aprendizado** → `auditar-pedagogia.py` (ingredientes de
  retenção + engajamento: retrieval, espaçamento, feedback elaborativo, mentalidade
  de crescimento, dual coding, competência, curiosidade, carga cognitiva baixa).
- **Auditor de PROVA (avaliação)** → `auditar-prova.py` (nasceu porque estes erros
  escaparam de todos os outros numa prova de lateralidade). Checa: (1) **concordância
  escrito × falado** por pista (mesmo eixo cima/baixo × esquerda/direita); (2) **gênero
  uniforme** — direção sempre no feminino "direita/esquerda" (igual aos botões), barra a
  forma masculina "direito/esquerdo"; (3) **gabarito de lateralidade** recomputado (de
  costas = alinhado, de frente = espelho, par = lado do alvo, seta = sentido, vert =
  objeto de cima) vs. o `correta` do código; (4) **final não revela nem fala em
  "professora"/registro** ao aluno; (5) **assets** — pose `masc_<vista>_<lado>.png`,
  objeto `<obj>.png` e `audio/<chave>.mp3` de cada fala existem. Rodar SEMPRE antes de
  publicar uma prova: `python3 _circo/auditar-prova.py _lote/<ativ>/index.html --rigoroso`.
Regra de ouro: **nenhuma frente sem auditor**. Achou um erro que passou? O
conserto não é só o erro — é criar/ajustar o auditor pra ele **não passar de novo**.
(Foi assim que nasceu o `auditar-prova.py`: concordância escrito×falado, gênero,
gabarito e a mensagem "registrada para a professora" passaram porque não havia um
auditor específico — agora há, e ele **reprova** a publicação se algo disso voltar.)

## 19.4 TEMA CLARO = padrão visual da fábrica
Padrão novo: **fundo claro, cards brancos, texto escuro** (contraste alto por
construção — o oposto do risco do papel-Atlas claro misturado com áreas escuras).
- Paleta: página `#eef3f9` (grad. `#eaf3fb→#eef3f9`); card `#ffffff` borda
  `#e4ebf4`; texto `#17263a` (títulos) / `#42566b` (corpo) / `#5b6b7f` (legenda);
  azul acento `#1f79d6`; âmbar de TEXTO **escuro** `#8a5300` (âmbar claro não passa
  no branco); verde texto `#0f7a4e` (fill `#22b573`); vermelho `#b23636` (fill
  `#c0392b`); dica `#fff8e6`/borda `#f0cf85`/texto `#7a5a12`.
- **Como aplicar num arquivo que já é escuro:** bloco `body.claro{...}` no fim do
  `<style>` que sobrescreve **todas** as superfícies (inclua os fundos por fase
  `body.claro.cl-sol` etc. — foi a parte que o Atlas esqueceu) + `<body class="claro">`.
  As superfícies usam gradiente → **redefina o `background` inteiro** (não só a cor).
  Depois **rode o auditor de contraste** e ajuste até `APROVADO`.
- **Compatibilidade continua sagrada:** prefixos `-webkit-`, **cor sólida antes de
  todo gradiente**, sem `grid/gap/var()/clamp`, emojis ≤ Unicode 6.0.
- Referência viva: **`climas-do-mundo-6ano`** foi migrada p/ o tema claro (mantendo
  voz, reset e Nino inteiro), com contraste verificado.

## 20. `git fetch` ANTES de dizer "não existe" (lição paga — 2026-07)
**A cópia local do repositório pode estar MUITO atrasada** — num caso real ela
estava **445 commits atrás** do remoto. Resultado: `git log`, `git grep` e ler o
`CLAUDE.md` mostravam uma versão VELHA, sem uma pasta inteira (`_agenda/`) e sem
uma seção inteira do manual que **já existiam** no remoto. Eu afirmei com
convicção que "a agenda nunca passou por este repo" — **e estava errado**; era só
a cópia local defasada. Regra:
- **Antes de concluir que algo "não existe" / "nunca foi feito aqui"**, rodar
  `git fetch origin <branch>` e comparar com `origin/<branch>` (`git log
  origin/<branch>`, `git status -sb` mostra "behind N"). Só depois afirmar.
- **Pistas de que a cópia está velha:** `git status -sb` diz `behind N`; o
  `head_commit` de um workflow run (retornado pelas ferramentas do GitHub) menciona
  arquivos/pastas que você "não tem"; o usuário insiste que fez algo aqui e você não
  acha. Nesses casos: **fetch/pull primeiro, investigar depois.**
- **Nunca prometer ao usuário que "nunca vou esquecer".** Entre sessões NÃO há
  memória — a única memória real é o que está ESCRITO no repo (`CLAUDE.md` + manuais
  + histórico do git). Quando o usuário pedir "para não esquecer", a resposta certa é
  **registrar no repo**, não prometer lembrança.

## 21. Lições da Confeitaria Mágica (2026-07 — rodadas 1 a 3)
- **Texto do enunciado dentro do balão:** `.enun` global é quase branco (feito p/
  fundo escuro). Dentro de `.balao` (fundo claro) fica **invisível**. Todo `<span
  class="enun">` dentro de balão precisa de `color:#5a2e1c` inline. Esse bug ficou
  meses sem ser notado porque as montagens de teste não incluíam telas de escolha.
  **QA visual deve incluir pelo menos 1 tela de CADA renderizador.**
- **Conquistas com snapshot:** condições `cond(s)` que usam `s.feitas` quebram se o
  estado real guarda `feitasMap` (mapa). Passar um **snapshot** `{acertosTot,
  maxStreak, feitas: feitas()}` para as condições — nunca o objeto `S` cru.
- **Zonas de arrastar SEM retângulo pontilhado:** o dono pediu para remover TODOS os
  `border: dashed`. O alvo do drop é a PRÓPRIA imagem (prato/caixa); o feedback de
  hover é brilho + leve escala (`drop-shadow` + `scale(1.06)`), não borda.
- **Áudio com hash ≠ conteúdo falado:** a chave em `AUDIO_TXT` vem do hash do texto
  EXIBIDO (`_chaveVoz(limparFala(texto))`), mas o MP3 pode ser gerado com outro
  texto (ex.: "R$ 4,80" exibido → "quatro reais e oitenta centavos" falado). No
  lote: `id` = hash do texto exibido, `texto` = forma falada.
- **Falas compostas:** fim de fase fala `"Uau! " + UAU_FASE[ch]` e `"Parada
  concluída! " + gancho` — o áudio precisa ser gerado da string COMPOSTA.
  Reusar ganchos entre paradas = reusar o MP3 (string idêntica, hash idêntico).
- **Plano B sem MCP (token expirado no meio do trabalho):** o push do git continua
  funcionando. `.github/workflows/finalizar.yml` roda por PUSH nesta branch com
  marcadores na mensagem do commit: `[medalha]` gera imagem no Gemini; `[publicar]`
  republica `_pub_confeitaria` → `confeitaria-da-divisao` (histórico limpo), força o
  build do Pages, ESPERA o resultado e grava `_status/confeitaria.txt` neste repo
  (basta `git pull` para ler o status do build sem MCP). Commits dos jobs não levam
  marcador → sem loop.

## 22. POLÍTICA DE MODELOS — forte onde precisa, Opus 4.8 esforço alto no resto (decisão do Marcos, jul/2026)
**Regra de custo-benefício:** onde precisa de força criativa/diagnóstica vai o modelo
mais FORTE disponível; onde o trabalho é seguir padrão, o **Opus 4.8 em esforço alto
dá conta** — e é o padrão.
**ABRANGÊNCIA: vale para TUDO nesta fábrica** — Mundo Vivo, atividades premium,
provas/quiz, hub Ilhas do Saber, retrofits, demos e **qualquer pedido futuro do
Marcos**. Não é política de um projeto; é a política da casa.

**Que tarefa pede qual nível:**
- **Opus 4.8 esforço alto (padrão — produção em série):** construir bairros/missões
  sobre moldes existentes, gerar/recortar cartelas, lotes de áudio, publicar,
  rodar QA/auditores, retrofits guiados por manual, conteúdo novo em mecânica
  já pronta.
- **Modelo mais forte (pontual — criação e diagnóstico difícil):** desenhar
  mecânica/motor INÉDITO (ex.: motor de andar/física do Mundo Vivo), caçar bug
  sutil de timing/física/voz que resistiu a 2 tentativas, decisão pedagógica
  ambígua, auditoria profunda de arquitetura.

**Como aplicar na prática (3 camadas):**
1. **Sessão principal:** o Claude NÃO troca o próprio modelo — quem troca é o
   Marcos com `/model`. O Claude deve AVISAR ativamente quando a tarefa mudar de
   natureza: "esta etapa é de motor/criação — sugiro trocar para o modelo forte"
   ou, no sentido inverso, "isto é produção em série, o Opus 4.8 esforço alto
   resolve — pode economizar". Avisar É obrigação; trocar é decisão do Marcos.
2. **Subtarefas delegadas (AUTOMÁTICO):** ao despachar subagentes/workflows, o
   Claude escolhe o modelo POR subtarefa: leve/padrão para varreduras e tarefas
   mecânicas; forte para verificação crítica ou criação. Isso não depende do
   Marcos e deve ser feito por padrão.
3. **Transparência:** em trabalhos longos, dizer no começo qual nível está ativo
   e se serve para a etapa. Evidência desta política: a Confeitaria começou no
   Opus 4.8 (motor de arrastar, P1/P2) e seguiu no modelo forte (rodadas 2-3,
   demo do Mundo Vivo) — os dois entregaram no padrão dos manuais, porque o
   segredo é o que está ESCRITO no repo (manuais + referências), não o modelo.
