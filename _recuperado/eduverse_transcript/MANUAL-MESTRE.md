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