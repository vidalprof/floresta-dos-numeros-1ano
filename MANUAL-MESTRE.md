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
- Narração: `speechSynthesis` pt-BR (só narra se houver voz pt-BR real instalada).
- `localStorage` funciona em GitHub Pages; usar variáveis em memória como fallback.
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
- **Conferir a HABILIDADE contra a SÉRIE, não só o tema (lição paga).** Um conteúdo pode "caber" no tema mas ser de outro ano. Ex. real: classificar/nomear "artigo definido/indefinido" é metalinguagem de 8º ano (EF08LP09) — NÃO é 2º ano; no 2º ano vale o USO natural (o/a/um/uma pelo sentido) e habilidades como sílabas (EF02LP02), sinônimos/antônimos (EF02LP10), aumentativo/diminutivo (EF02LP11). Antes de aprovar uma fase, casar o objetivo com o código BNCC do ano. Remover a metalinguagem das falas/explicações quando a série não pede (a criança escolhe pelo sentido, não pelo rótulo gramatical).
- Cobrir o conteúdo ESPERADO da série, não só o "seguro". Ex.: dinheiro no 5º ano (EF05MA) pede **porcentagem e desconto** (50%=metade, 10%=÷10, 25%=¼) e decimais — sem isso o teto fica em 4º ano. "Está adequado mas seguro demais para a série?" é sinal de que falta um degrau.
- O conteúdo mais avançado vem como ÚLTIMA parada de conteúdo antes dos bônus.
- Variar o ENUNCIADO dentro da fase (3-4 formas equivalentes por `i%`), para não repetir "Quanto vale?" 10x.

### Dose certa (atenção da idade — NÃO cansar)
- **~5-6 desafios por fase** (NÃO 10). 10×muitas fases = >1h, monótono. Limitar em `iniciarFase`: se >6, SORTEAR 6 (`embaralhar(todos).slice(0,6)`) — some o excesso e a fase muda a cada rejogada. Resetar `_mix=false` nos sorteados.
- **Variar a AÇÃO, não só o enunciado.** Intercalar **jogos de alívio** (memória, quebra-cabeça, caça-palavras) no MEIO (ex.: memória após a 6ª parada, quebra-cabeça após a 9ª).
- **Menos digitação livre** (gera erro de digitação, não de raciocínio). Equilibrar com toque/escolha.

### Apoio ao erro (correção com contagem — fases concretas)
Obrigatório em TODA fase de contar quantidade:
1. Mascote fala **"Não foi dessa vez!"** (com carinho, sem punir).
2. Pausa ~1,5s.
3. Fala separada **"Agora vamos contar. Bem devagar."** (frase à parte, dá tempo à criança).
4. Pausa.
5. **ACENDE cada objeto UM POR UM** — classe que dá SÓ glow via `filter:drop-shadow`, **SEM `transform:scale`** (aumentar o objeto some com a referência de tamanho/posição). Ex.: `.obj-item.sel .obj-img`. Conta em voz alta POR EXTENSO ("um... dois... três...") com ~850ms por objeto.
6. Todos acesos: **"São N! Agora toque no número N."** e apaga.
- **CRÍTICO:** a cadeia de acender usa `setTimeout` de RITMO FIXO, **NÃO** o `onend` da fala (em PC sem voz pt-BR o onend pode nunca disparar e travar). Cada objeto tem `id` próprio (`cItem0`, `cItem1`...). Números por extenso via `numExt(n)` (que evita o TTS ler o dígito "1" como "um" masculino) — e ACENTUADOS ("três", não "tres", senão o TTS erra a tônica).

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
A leitura usa `speechSynthesis`. Web Speech é o teto viável (vozes neurais pesam MB e quebram offline; nuvem é paga).

- **`limparFala()`**: remove tags/entidades HTML; corrige espaço após `, . ! ? :`; junta espaços duplos; SEMPRE põe ponto final. **Normaliza pronúncia** de palavras sem acento que o TTS erra: "voce"→"você", "voces"→"vocês", "numero"→"número", "proxima"→"próxima", "magica"→"mágica", "divisao"→"divisão", "multiplicacao"→"multiplicação", etc. (regex `\bpalavra\b/gi` preservando capitalização; adicionar palavras sempre que uma pronúncia errada for notada).
- **`escolherVoz()`**: melhor voz pt-BR (prioriza natural/neural/enhanced/google/microsoft/maria/francisca/luciana; cai para básica só se não houver outra).
- **Ritmo:** `rate ~0.92`, `pitch ~1.08`. Quebrar em frases (`. ! ? :`) faladas em fila com ~180ms de pausa.
- **Valores monetários por extenso:** "R$ 3,50" → "3 reais e 50 centavos"; "R$ 1,00" → "1 real"; "R$ 0,25" → "25 centavos" (o TTS lê "R$" errado — converter no limparFala).

**FALA NUNCA É CORTADA (lição paga):** o erro clássico é cada `falar()` começar com `cancel()`, então falas em sequência (elogio + streak + subir de nível + conquista) se cortavam. Padrão obrigatório com QUATRO funções:
- **`falar(txt, aoTerminar)`** — inicia narração NOVA, cancelando a anterior. Usar SÓ em troca de contexto/tela (abrir mapa, próxima parada, abrir fase). É o único que corta — de propósito, para o áudio não vazar de uma tela para outra.
- **`enfileirarFala(txt)`** — ADICIONA ao fim da fila SEM cortar. Usar quando duas falas devem ser ouvidas em sequência (elogio + streak, nível, conquista). O pop de streak/nível/conquista usa `popCaixaFila()`.
- **`falarDepois(txt)`** — se já há fala tocando, enfileira; senão fala na hora. Usado ao AVANÇAR de desafio: o próximo enunciado não corta o feedback anterior.
- **Ordem no acerto:** `feedbackAcerto()` narra elogio+explicação PRIMEIRO (via `falar`, fila limpa) e SÓ DEPOIS dispara streak/nível/conquista (que entram na fila) — tudo ouvido em ordem.
- **Proteção de fila (`_falaSeq`):** contador incrementado a cada `pararFala()`; cada frase só continua a fila se o contador não mudou (impede fila antiga voltar após troca de tela).
- **Sem voz pt-BR:** a fila roda em modo silencioso com tempo estimado por frase (nunca `onend`) — nada trava.
- **Botão de avançar VISÍVEL mas DESABILITADO até a fala terminar (lição paga — repetida):** a regra é "o botão aparece, porém só habilita quando o áudio acaba, contando bem pausadamente, sem cortar nada". Deixar o botão habilitado e confiar em "clicar não corta" NÃO basta — a criança clica e corta. Padrão obrigatório: renderizar o botão já visível com `disabled` + classe de "aguardando" (ex.: `esperando`/`proxAguarda`, opacidade menor), e só habilitar quando a narração REALMENTE terminou.
- **Habilitar só após SILÊNCIO CONTÍNUO (não numa pausinha entre falas):** o elogio, o streak, o "subiu de nível" e a conquista entram na fila DEPOIS, por `setTimeout` (600–900ms). Um poll simples que checa "fila vazia + não falando" uma vez pode liberar numa fresta de silêncio ANTES de a comemoração começar — e aí o clique corta. Usar um helper (`esperarFalaTerminar`/`travarBotaoAteFala`) que só libera quando a fala fica **em silêncio CONTÍNUO por ~650ms** (após um mínimo inicial ~900ms): se algo for enfileirado nesse meio, o cronômetro do silêncio ZERA e a espera recomeça. Trava de segurança (`setTimeout` ~15s) para nunca ficar preso. Aplicar em TODAS as telas que narram + têm botão: feedback de acerto, "Começar!" da fase, fim de fase (inclusive botões secundários "Ver o mapa"/"Jogar de novo"), ofertas de Desafio Extra e Treino, e o Grande Final. Em PC sem voz o tempo estimado por frase alimenta o mesmo helper — avança normal.

- **Narração automática em TUDO:** tela inicial, mapa (história), intro de fase, cada enunciado ao abrir, feedback ao responder, fim de fase, grande final, jogos. Botão para repetir onde couber.
- **Bilíngue:** detectar idioma FRASE A FRASE (`detectaPT`) e usar a voz certa (`escolherVozPt`/`escolherVozEn`); pular a frase se não houver voz do idioma (nunca voz errada lendo o outro idioma).

**GRAFIA DE TELA ≠ GRAFIA FALADA — sílabas, siglas, símbolos (lição paga):** o TTS soletra maiúsculas curtas ("GA"→"gê-á", "BO"→"bê-ô", "SA-PA-TO" letra a letra) e não lê "+" direito. Quando a TELA precisa de maiúsculas (destacar sílabas numa fase de consciência fonológica, siglas) mas isso soa errado na fala:
- **Campos opcionais `fala` e `falaExplica` no desafio.** A narração do enunciado usa `dd.fala||dd.enun`; o feedback usa `dd.falaExplica||dd.explica`. A criança VÊ "GA mais TO formam qual palavra?" e OUVE "ga, mais to, formam qual palavra?".
- Regras da versão falada: sílabas em MINÚSCULAS (o TTS lê o som, não as letras), separadas por VÍRGULA (micro-pausa), "+" escrito "mais", palavra-alvo como palavra inteira minúscula.
- A `fala` obedece à mesma regra do enunciado: NÃO revela a resposta após o "?". O fallback de tempo sem voz mede o comprimento do texto FALADO.
- Implementação: `falarDepois(dd.fala?dd.fala:dd.enun)` no render do desafio; `falar(el1+" "+(dd.falaExplica?dd.falaExplica:dd.explica),liberar)` no `feedbackAcerto`.

**RETICÊNCIAS PICOTAM A FALA (lição paga):** "..." vira ". . ." após o `limparFala` (espaço depois de cada ponto) e o TTS lê cada ponto como pausa isolada — a frase sai picotada. NUNCA "..." no que será falado; usar vírgula para a pausa. Na tela "..." pode aparecer, desde que o que vai ao `falar()` seja a string SEM reticências (ex.: mostrar "Pense de novo..." mas falar "Quase! Pense de novo.").

**NÃO NARRAR SÍMBOLOS, PONTUAÇÃO SOLTA NEM LACUNAS (lição paga):** o TTS lê em voz alta caracteres que só existem no visual — sublinhados de lacuna ("Complete: gato ___" o TTS fala "underline underline underline"), parênteses, colchetes, chaves, aspas «»""‘’, asterisco, cerquilha, til/circunflexo soltos, barras, `< > | = + @ • ~`. O `limparFala()` DEVE, antes de falar: trocar sequências de `_` por espaço (a lacuna vira uma pausa, não "traço traço"); colapsar reticências; trocar travessão `—`/`–` por vírgula; e REMOVER os símbolos avulsos acima (viram espaço). Também colar `([!?])\s*\.` → `$1` para não sobrar ". " depois de "!"/"?" (evita a pausa isolada que picota). Regra geral: o que vai ao `falar()` deve conter só letras, números e a pontuação que gera prosódia natural (`. , ! ? :`).

**Adicionar ao `pronuncia()`** as palavras que o TTS erra sem acento — quando houver fase de sílabas, incluir "silaba"→"sílaba", "silabas"→"sílabas", "pedaco/pedacos"→"pedaço/pedaços".

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

- **O DÍGITO "2" TAMBÉM tem gênero na fala (lição paga — "duas baldes"):** o TTS lê "2" como "dois" (masculino), então "2 baldes" fica certo mas "2 vacas" deveria ser "duas vacas" e "2 vezes" deveria ser "duas vezes". Em português só **1 e 2** flexionam (um/uma, dois/duas); de 3 em diante o número é invariável. Quando a fala tiver "2" diante de substantivo/palavra FEMININA, converter para "duas" (no `normPron`/`limparFala`, regex por palavra: `\b2\s+vacas\b`→"duas vacas", `\b2\s+vezes\b`→"duas vezes"; e um `\b2\b`→"dois" como padrão masculino). "vezes" é feminino ("duas vezes"). Preferir gerar a fala já por extenso com `numExt`/`pluralG` quando o gênero é conhecido.
- **ENUNCIADO FALADO/ESCRITO DEVE BATER COM A FIGURA MOSTRADA (lição paga):** se a tela mostra ovos, o enunciado não pode dizer "maçãs". O bug clássico aparece quando o objeto do desafio CICLA (sorteio) mas o texto ficou fixo, ou vice-versa. Em cada fase, a figura, o enunciado, a fala (`dd.fala`) e a explicação têm que nomear o MESMO objeto. Ao auditar, varrer fase a fase conferindo figura × texto × fala.
- **NUNCA substantivo em plural fixo ao lado de número variável** ("1 acertos", "1 moedas", "1 pontos" são bugs REAIS já encontrados — sempre passar por `plural()`/`pluralG()`).
- **Auditoria obrigatória com n=1:** forçar 1 ponto / 1 medalha / 1 acerto / 1 parada no RELATÓRIO e no GRANDE FINAL; varrer por regex `\b1\s+(pontos|acertos|medalhas|paradas|moedas|...)`. Esses bugs só aparecem quando o valor é exatamente 1.
- **Referência de gênero:** feminino = palavra, ilha, medalha, letra, estrela, moeda, fase, cesta, parada; masculino = ponto, acerto, erro, amigo, tesouro, dia, número.
- **Valores com centavos nas falas manuais:** escrever completo ("quatro reais e setenta e cinco centavos"), nunca truncado ("quatro e setenta e cinco").
- **Falas naturais e calorosas** — ler cada fala "em voz alta" mentalmente: soa como uma pessoa querida falando com uma criança?

================================================================
## 9. ASSETS VISUAIS — IMAGENS GERADAS NO CHATGPT
================================================================
Para qualidade premium, gerar os assets-chave como **imagens no ChatGPT**, não SVG desenhado. PNG renderiza garantido em navegador antigo e fica muito mais bonito.

**Sempre imagem (cartela ChatGPT):** mascote (4 poses), companheiro de cada fase, cenários/lugares do mapa, objetos de contar/somar (vários, para variar), emblemas de nível, selos/conquistas (tema, nunca emoji), objetos do dia a dia das questões, a recompensa-que-cresce, medalhas (medalhão dourado + número por código), cena de abertura e cena do grande final (estas duas viram JPEG de fundo, não recorte).
**Pode ficar SVG:** ícones minúsculos de interface que mudam de cor/estado. Se um SVG falhar no PC antigo, vira imagem.

**PRINCÍPIO (não esquecer):** o prompt do ChatGPT NÃO resolve sozinho o problema de parte branca/franja. Um prompt bom (fundo branco puro + SEM sombra + contorno escuro definido) PREVINE a maior fonte (sombra na base) e facilita o recorte, mas SEMPRE sobra franja fina e às vezes vãos internos — só some com a LIMPEZA obrigatória do código. **Garantia = prompt bom + limpeza obrigatória juntos.** Nunca embutir sem passar pela limpeza e pela conferência visual.

**CORPO BRANCO SEM CONTORNO ESCURO = FRANJA IRRECUPERÁVEL (lição paga, crítica):** se a cartela desenhar um objeto/animal BRANCO (coelho, ovelha, galinha, ovo, pato) SEM linha de contorno escura e fechada, o corpo branco encosta direto no fundo branco — não há fronteira. O recorte deixa borda branca esfarrapada, e removê-la por código só PIORA (medido: coelho foi de 21% de franja para 78% e comeu 8,5% do corpo). **NÃO existe conserto por código — a ÚNICA solução é REGERAR** a cartela exigindo "contorno preto grosso e fechado em volta de cada objeto, INCLUSIVE os brancos". Diagnóstico: medir % de contorno escuro na borda; se ~0% e muito branco na borda, veio sem contorno → regerar. (Com contorno, a franja cai para 0%.)

### Regra do anexo — CARTELA ÚNICA
Sempre pedir todos os objetos numa **cartela única** (vários itens em grade, numa imagem só), nunca um a um (estoura o limite de anexos). Gerar e enviar uma cartela por vez.

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
- **Companheiro do mapa ao LADO da ilha, nunca por `bottom` (lição paga: personagem cobrindo o nome da parada).** Companheiro é imagem retrato alta (~163×220). Ancorado por `bottom` (com `.paradaNome` fluindo abaixo) ele desce e cobre o título. Correto: ancorar por `top` na altura do meio do cenário (cenário 80px → companheiro ~48px em `top:24px`, `right:-14px`), `overflow:hidden`, e `.paradaNome{margin-top:4px}`. Auditar renderizando com companheiro retrato ALTO a 360/320px: a base do companheiro tem que ficar ACIMA do topo do nome em todas as paradas.
- Glow em PNG recortado: `filter:drop-shadow` (par `-webkit-`), NUNCA `box-shadow` (desenha retângulo).
- Objetos de contagem: `display:block; width:100%; height:auto` no container com px.
- Flexbox com fallback `-webkit-box` (+ `-webkit-box-flex` explícito nos filhos).
- Imagens não-quadradas: altura fixa + `width:auto`. Cards com `overflow:visible` onde há halo/animação.

================================================================
## 11. GAMIFICAÇÃO (estrutura padrão)
================================================================
- **Níveis** com XP crescente (5 níveis temáticos). Ex.: Aprendiz (0) → Explorador (60) → Aventureiro (150) → Guardião (260) → Mestre (400). `nivelAtual()`.
- **Emblema do nível atual SEMPRE visível na topbar** (imagem ~42-44px), atualizando ao ganhar XP e ao carregar progresso salvo — `atualizarEmblemaTopo()` em `addEstrela`, no `carregar` e na inicialização. Erro comum: gerar os emblemas mas só mostrar no pop-up de level-up (some em 3s) — a criança nunca vê o emblema do nível dela.
- **Subir de nível** detectado em `addPontos`: animação + fanfarra + confete + fala.
- **Conquistas/selos** (imagens do tema, nunca emoji) em marcos: 1º acerto, 5 seguidos (streak), 1ª fase, metade, jogo, todas.
- **Medalha por fase:** um MEDALHÃO DOURADO (círculo de ouro com fita/laço colorido e borda serrilhada) com o SÍMBOLO da fase no centro (ovo, maçã, vaca, cenoura, osso, troféu...) — NÃO é o bicho/mascote inteiro nem emoji. Imagem dourada temática recortada; o NÚMERO (1..N) é adicionado por código via overlay `.med-num`. Regerar ao refazer a atividade. (Lição paga: uma cartela de "bichos" no lugar de medalhões passou como medalha sem ser — conferir % de dourado: medalhão tem ~37-56%; se der 1-3%, é figura, regerar.)
- **XP por acerto** com bônus de streak.
- Toda fase termina chamando a tela de fim de fase (registra `concluidas[fase]` e conquistas). Ao remover fases, religar conquistas órfãs.
- **Grande final:** confete em ondas, mascote comemorando, desfecho da história, recompensa no tamanho máximo, emblema do nível, estatísticas (concordância: "1 ponto"/"2 pontos"). Cena final ilustrada no topo.
- **Relatório do professor:** aproveitamento geral + tabela por fase (acertos/erros/% com cor) + o que revisar + dica de imprimir em PDF. Acessível a partir do grande final; depois, botão "Relatório" embaixo do mapa (só com tudo concluído).

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
- **Sílabas (consciência fonológica — EF02LP02):** juntar sílabas para formar a palavra, apontar a sílaba que falta, contar sílabas, trocar a sílaba inicial. Tela em MAIÚSCULAS para destaque; fala via `fala`/`falaExplica` em minúsculas (o TTS soletra maiúsculas — ver Seção 7). Como fase de conteúdo, o Desafio Extra é uma palavra com uma sílaba a mais; se tratada como fase-jogo, não leva Extra.
- **Frase em ordem:** "Monte a Frase" — ordenar palavras embaralhadas.
- **Escolha múltipla com imagem (`escolha-img`):** mesma regra de embaralhar.
- **Classificar fichas:** arrastar ou clicar (mouse + touch).
- **Forca:** tradicional, com figura simples (traço não-gráfico, sem sofrimento); dica + teclado + 6 vidas. Relief games NÃO levam Desafio Extra.

### Contas de dois algarismos
- Progredir de 1 para 2 algarismos, sem pedir emprestado nas séries iniciais.
- Resultados variados. Piscar a coluna das unidades ao abrir e mascote fala (com pausa): "Esta conta tem dezena e unidade. Começamos sempre pelas unidades!".

### Sistema de arrastar
- `tornarArrastavel`, `instalarDragGlobal`, `marcarSoltavel`, `data-drop`.
- **`instalarDragGlobal()` precisa ser chamado** quando a fase de arrastar inicia — senão não funciona.
- **ARRASTAR é a 1ª opção; TOQUE é a reserva** (regra dos dois manuais). Em todo mecanismo onde faz sentido arrastar, o arrastar DEVE funcionar de verdade (não só o toque), e o enunciado/fala diz "arraste". O toque continua como alternativa para quem não consegue arrastar.
- **Imagem dentro do arrastável SEQUESTRA o mouse (lição paga — arrastar "não funcionava"):** um `<img>` dentro do item dispara o **drag nativo de imagem** do navegador, que rouba os eventos de mouse (chega 1 `mousemove` e nenhum `mouseup` no document) — o arrastar quebra em PC. Consertar: (a) `document.addEventListener("dragstart", ...)` com `preventDefault()` quando o alvo é arrastável; (b) `preventDefault()` no `mousedown` (só mouse, não toque: `if(!e.touches && e.preventDefault)`); (c) CSS `.arrasta{ touch-action:none; }` (impede o scroll do celular roubar o gesto) e `.arrasta img{ -webkit-user-drag:none; }`.
- **Preservar classes ao reconstruir o `className` (lição paga — "1ª vez arrasta, 2ª não"):** funções que remontam a classe do zero (`el.className="bicho drag"`, `el.className="cesto"`) APAGAM as classes `arrasta`/`solta` — depois do 1º drop não há mais zona de arrasto/solta e o jogo trava. Sempre reanexar `arrasta`/`solta` (e o estado, ex.: `hl`) ao reconstruir a classe.
- **Testar com evento REAL, não sintético:** eventos sintéticos disparados por JS passam mesmo com o bug do drag nativo. Validar com CDP (`Input.dispatchMouseEvent`) ou toque real; e usar `user-data-dir` limpo por teste (páginas reaproveitadas acumulam listeners e mascaram o bug).

### Caça-palavras — interação por PONTAS (1ª e última letra)
- **NÃO pedir para tocar letra por letra em sequência** acumulando numa string que nunca zera: um toque errado embaralha tudo e nada mais é reconhecido (bug real — "não funciona"). Padrão certo, intuitivo: a criança toca na **primeira letra** (fica destacada/laranja) e depois na **última letra** da palavra.
- Validar a **linha reta** entre as duas pontas (horizontal, vertical ou diagonal; rejeitar se não estiverem alinhadas) e comparar a sequência de letras com a lista de alvos **nos dois sentidos** (frente e de trás pra frente).
- Ao achar: células ficam **verdes**, a palavra fica **riscada na lista**, confete + pontos; ao achar todas, carimbo e fim de fase. Toque fora de linha reta apenas recomeça a seleção; toque que não forma palavra dá dica gentil, sem punir.

### Nomes de jogos honestos
- **"Pôr em ordem"** (ou "ordenar"), NUNCA "quebra-cabeça", para a fase de ordenar elementos — a fala do enunciado deve dizer "arraste/ponha em ordem", não "monte o quebra-cabeça". O nome anunciado tem que descrever o que a criança realmente faz.

### MODO PROFESSOR — senha mestra `1275@` (opcional, mas padrão em toda atividade)
Recurso para o professor **testar o jogo** sem precisar concluir fase por fase.
Digitar `1275@` no teclado a QUALQUER momento LIGA/DESLIGA o "modo professor",
que **destrava todas as fases no mapa**. Digitar de novo volta ao normal.
- **NÃO altera o progresso real do aluno** — é só uma flag `_adminLivre` que muda
  o que o mapa mostra como liberado. Ao desligar, volta exatamente ao estado real.
- **Não é segurança de verdade** (a senha fica visível no código-fonte) — é um
  atalho de conveniência. Só destrava fases; nada sensível. Funciona em **teclado
  físico** (PC); em celular/tablet sem teclado não há como digitar.
- **Emoji:** use os caracteres LITERAIS 🔓 🔒 na string (Unicode 6.0, ok). NUNCA
  escapes `\U0001F513`/`\u{...}` (em JS viram texto literal e quebram o toast).

**Bloco genérico** (idêntico em toda atividade; inserir no topo do script, perto
das globais de estado):
```javascript
/* ====== SENHA MESTRA DO PROFESSOR (1275@) ====== */
var _adminLivre=false;
(function(){
  var _buf="", _senha="1275@";
  document.addEventListener("keydown", function(e){
    var k=e.key;
    if(!k || k.length!==1){ return; } /* ignora Shift/Enter/setas */
    _buf=(_buf+k).slice(-8);
    if(_buf.indexOf(_senha)>=0){ _buf=""; _adminLivre=!_adminLivre; avisoAdmin(_adminLivre); _adminIrMapa(); }
  }, false);
})();
function avisoAdmin(ligado){
  var t=document.createElement("div");
  t.style.cssText="position:fixed;left:50%;top:14px;-webkit-transform:translateX(-50%);transform:translateX(-50%);background:"+(ligado?"#2f7d32":"#8a2a2a")+";color:#fff;padding:10px 16px;border-radius:12px;font-weight:bold;font-size:14px;z-index:99999;box-shadow:0 4px 14px rgba(0,0,0,.45)";
  t.innerHTML=ligado?"🔓 Modo professor: fases liberadas":"🔒 Modo professor desligado";
  document.body.appendChild(t);
  setTimeout(function(){ if(t.parentNode){ t.parentNode.removeChild(t); } },2200);
}
```

**Ganchos por atividade (2 pontos):**
1. `_adminIrMapa()` chama a função que RENDERIZA o mapa da atividade (redesenha já
   com o novo estado). Ex.: `function _adminIrMapa(){ try{ telaMenu(); }catch(e){} }`
   (ou `irMapa(false)`, conforme o nome real).
2. **Bypass na trava de fase.** Quase toda atividade tem uma função central que
   diz se a fase está liberada (`liberada(chave)`, `faseDesbloqueada(i)`...). Basta
   `if(_adminLivre){ return true; }` no INÍCIO dela — o mapa passa a mostrar todas
   clicáveis. Se o acesso ao FINAL/troféu tiver gate SEPARADO por contagem
   (`feitas===ORDEM.length`, `feitasCount()>=...` num `onclick`), some `|| _adminLivre`
   nessa condição também. Se o final for evento natural (disparado ao concluir a
   última fase, sem `onclick`), não precisa mexer. **Nunca** alterar `concluidas`.
- **Validar** com `node --check` e testar de verdade: digitar a senha destrava
  todas as fases; digitar de novo retranca, sem mudar o que o aluno já concluiu.

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
**NÍVEL 2 — QA:** (8) play-through de TODAS as fases (simulador `node sim.js` ou Playwright) com **0 erros**, sem overflow em 414/390/360/320px; (9) zero emoji moderno/VS16; (10) toda função de `onclick` existe; (11) embaralhamento REAL (posição da certa varia entre execuções); (12) fala nunca cortada (elogio+explicação inteiros, streak/nível/conquista depois; trocar de tela corta de propósito) E botão de avançar VISÍVEL porém DESABILITADO até o silêncio CONTÍNUO — testar clicando durante a narração em cada tela (feedback, Começar, fim de fase e secundários, ofertas, final): o clique não pode cortar; não narra símbolos/lacunas/`_`; (13) adaptatividade (100%→Extra, <50%→Reforço, erros→Treino); (14) mapa (só atual clicável, demais trancadas, conectores, troféu, relatório só no fim, barra de progresso).
**NÍVEL 3 — PEDAGOGO:** (15) matemática/conteúdo consistente (resposta nas opções, produtos/divisões corretos, divisões exatas, zero opções duplicadas); (16) concordância n=1 E n>1 (tela E fala; forçar 1 ponto/1 medalha, varrer `\b1\s+(plural)`); (17) numExt ACENTUADO ("três"); (18) normalização de pronúncia cobre as palavras; (19) narração não entrega resposta (nada declarativo após o "?"); (20) enunciados coerentes + explicações verdadeiras; (21) português impecável (varrer palavras sem acento); (22) imagens conferidas (cor/mosaico, transparência real, sem franja/sombra/vão, mascote não sobrepõe). (23) fala conferida: rodar cada enunciado/explicação pelo `limparFala` e LER a saída (zero sigla soletrada, zero "..." picotando, zero "+" cru; usar `fala`/`falaExplica` onde a grafia falada difere da de tela); (24) série casada: cada fase batendo com a habilidade BNCC do ano correto.
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
- Fases de contar têm apoio ao erro por contagem acesa (acende objeto a objeto, conta por extenso, ritmo fixo por setTimeout).
- Peças (medalhas/selos) recortadas por componente conectado + margem transparente, exibidas centralizadas com proporção preservada; auditar corte renderizando DURANTE a animação.
- Pronúncia: normalizar acentos no limparFala; streak diz "Você acertou N seguidas".
- Auditoria honesta de pedagogo: apontar furos REAIS (cansaço, falta de degrau da série, fechamento seco), não só elogiar. Verificar de verdade (rodar, contar, testar n=1), não de memória.
- Sempre validar rodando, sempre entregar `index.html`.
