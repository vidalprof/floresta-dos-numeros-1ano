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
- **SONS DE EFEITO sintetizados com Web Audio (lição paga):** para o "gostinho de jogo" (som de moeda ao acertar, "pop" ao encaixar, tom gentil ao errar, arpejo ao subir de nível, fanfarra ao concluir fase), SINTETIZAR os sons na hora com osciladores (`AudioContext` + `OscillatorNode` + `GainNode` com envelope rápido) — NÃO embutir arquivos de áudio (pesam MB). É leve (poucos KB de código), funciona em navegador antigo e não depende de baixar nada. Motor `tocarSom(nome)` com um `AudioContext` único; o contexto começa "suspenso" e só toca após o 1º gesto do usuário (regra de autoplay) — `resume()` no primeiro clique. Flag para poder desligar; volume discreto (~0.15).
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
A leitura usa `speechSynthesis`. Web Speech é o teto viável (vozes neurais pesam MB e quebram offline; nuvem é paga).

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

**BOTÃO NARRADO EM TODA A ATIVIDADE, não só nos desafios (lição paga):** o botão principal de CADA tela que abre com narração aparece na hora, mas começa DESABILITADO mostrando "🔊 Ouvindo..." e só habilita quando a narração termina (via callback), para a criança não pular a fala do Poli. Vale para: tela inicial (Começar/Continuar), intro de fase (Começar!), fim de fase (Próxima parada/Ver final), oferta de Extra (Aceitar), oferta de Reforço (Continuar), grande final (Ver relatório) — além dos desafios, que já tinham. Helper único: `botaoNarrado(txt, onclickAttr, extraCls)` gera o botão desabilitado + aviso; `falarComBotao(texto)` narra e libera via `liberarBotaoNarrado` (callback do `falar`), com RESERVA por tempo estimado se não houver voz pt-BR (nunca `onend`). **Cancelar o timer de liberação anterior ao criar um novo** (`clearTimeout`) — senão timers empilham ao longo das fases e podem liberar um botão de uma tela que já saiu.

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
Para qualidade premium, gerar os assets-chave como **imagens no ChatGPT**, não SVG desenhado. PNG renderiza garantido em navegador antigo e fica muito mais bonito.

**Sempre imagem (cartela ChatGPT):** mascote (4 poses), companheiro de cada fase, cenários/lugares do mapa, objetos de contar/somar (vários, para variar), emblemas de nível, selos/conquistas (tema, nunca emoji), objetos do dia a dia das questões, a recompensa-que-cresce, medalhas (medalhão dourado + número por código), cena de abertura e cena do grande final (estas duas viram JPEG de fundo, não recorte).
**Ilha/cenário de cada parada = OBJETO flutuante recortado (sem fundo/retângulo/texto), NÃO "cena":** obrigatório por parada (fácil de esquecer); no prompt pedir "só o objeto do circo flutuando no branco, sem parede/chão/céu/cortina/palco/retângulo, sem palavra" — se pedir "cena", o ChatGPT devolve retângulo com fundo. Na tela flutua sobre um holofote redondo suave feito no CÓDIGO (radial-gradient), não na imagem. Detalhes e recorte (flood-fill do branco pelas bordas) no ATIVIDADE-PREMIUM §2/§8. O mascote CAMINHA pela trilha (fica ao lado da parada atual e desce a cada conclusão).
**Pode ficar SVG:** ícones minúsculos de interface que mudam de cor/estado. Se um SVG falhar no PC antigo, vira imagem.

**PRINCÍPIO (não esquecer):** o prompt do ChatGPT NÃO resolve sozinho o problema de parte branca/franja. Um prompt bom (fundo branco puro + SEM sombra + contorno escuro definido) PREVINE a maior fonte (sombra na base) e facilita o recorte, mas SEMPRE sobra franja fina e às vezes vãos internos — só some com a LIMPEZA obrigatória do código. **Garantia = prompt bom + limpeza obrigatória juntos.** Nunca embutir sem passar pela limpeza e pela conferência visual.

**CORPO BRANCO SEM CONTORNO ESCURO = FRANJA IRRECUPERÁVEL (lição paga, crítica):** se a cartela desenhar um objeto/animal BRANCO (coelho, ovelha, galinha, ovo, pato) SEM linha de contorno escura e fechada, o corpo branco encosta direto no fundo branco — não há fronteira. O recorte deixa borda branca esfarrapada, e removê-la por código só PIORA (medido: coelho foi de 21% de franja para 78% e comeu 8,5% do corpo). **NÃO existe conserto por código — a ÚNICA solução é REGERAR** a cartela exigindo "contorno preto grosso e fechado em volta de cada objeto, INCLUSIVE os brancos". Diagnóstico: medir % de contorno escuro na borda; se ~0% e muito branco na borda, veio sem contorno → regerar. (Com contorno, a franja cai para 0%.)

**ORIENTAÇÃO SILHUETA vs COLORIDO — DEVEM APONTAR PARA O MESMO LADO (lição paga):** na fase da sombra (objeto colorido em cima, silhueta preta embaixo), a silhueta e o colorido do MESMO bichinho precisam apontar para o mesmo lado — senão a criança vê a tartaruga virada para a direita e a sombra dela para a esquerda, o que confunde e quebra a associação. As cartelas do ChatGPT saem em orientações aleatórias, então isto acontece com frequência. **Diagnóstico automático:** para cada bichinho, comparar o "lado que pesa" (centro de massa horizontal dos pixels opacos vs. centro geométrico) do colorido (`comp_`/`obj_`) e da silhueta (`sil_`); se um pesa-esquerda e o outro pesa-direita → estão invertidos. **Correção (sem regerar):** espelhar a silhueta por código (`PIL Image.transpose(FLIP_LEFT_RIGHT)`) e re-embutir — é 100% seguro porque a silhueta é uma forma preta chapada; espelhar não distorce nada. Regerar a cartela só se o próprio colorido estiver ruim. Auditar SEMPRE a orientação de todos os pares antes de entregar a fase da sombra.

**SILHUETAS PRETAS (fase da sombra) — recorte por LUMINÂNCIA, não por branco (lição paga):** silhueta é forma preta chapada sobre fundo branco. Recortar detectando os pixels ESCUROS (luminância < ~110), pintar o RGB de preto puro `[0,0,0]`, erodir 1px, alpha = máscara. NÃO aplicar de-fringe de "matar escuros" (apagaria o próprio objeto). Comprimem pra <1KB. Guardar num dicionário separado `SOMBRA["sil_<chave>"]` (não no IMG). O colorido de cada bichinho é reaproveitado do companheiro já embutido (`comp_<chave>`) — NÃO precisa gerar coloridos novos; só as silhuetas.

**QUANDO A VISUALIZAÇÃO DE IMAGEM DO CLAUDE FALHA — AVISAR, NÃO SEGUIR NO ESCURO (lição paga):** a ferramenta de visualização do Claude pode retornar vazio (`[image]` em branco) de forma intermitente. Quando isso acontece, as métricas numéricas (franja, cor dominante, componentes) continuam confiáveis para franja/cor, mas NÃO enxergam problemas de ENQUADRAMENTO que só o olho pega: orientação virada, objeto de cabeça para baixo, recorte cortando um pedaço, dois bichos colados. Nesses casos o Claude deve: (a) AVISAR o Marcos de forma DESTACADA que não conseguiu ver a imagem ("minha visualização falhou nesta imagem — confira a orientação/enquadramento no mosaico `conferir_*.png`"), (b) embutir por número apenas quando o risco é baixo e puramente de franja/cor (contorno fechado + franja ≤1%), e (c) deixar o mosaico de conferência salvo em outputs para o Marcos validar com os olhos. NUNCA tratar "franja ok pelos números" como se fosse "imagem ok" — franja e orientação são coisas DIFERENTES, e só a segunda precisa de olho humano. Ambíguo ou não pôde ver = apontar como PENDÊNCIA de conferência visual, não como concluído.

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