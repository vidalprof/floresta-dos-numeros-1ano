# ATIVIDADE-PREMIUM.md — MODELO OFICIAL DE TODA ATIVIDADE
## Marcos — pedagogo/dev, Blumenau-SC — escola pública
## Este arquivo define O FORMATO ÚNICO de toda atividade (criada do zero OU upgrade).
## Ler JUNTO com o MANUAL-CONSOLIDADO.md (regras técnicas completas). Em conflito, este arquivo manda no FORMATO/DINÂMICA.

================================================================
## LEIA PRIMEIRO — O QUE ESTE ARQUIVO EXIGE
================================================================
Qualquer conversa que for **CRIAR uma atividade nova** ou **fazer UPGRADE de uma atividade existente** deve entregar uma atividade **IDÊNTICA** ao modelo descrito aqui — mesma tela inicial, mesmo mapa vivo, mesmo fluxo de fase, mesmos botões e animações, mesma comemoração, mesma narração, mesma gamificação, mesmo relatório, mesmas regras de imagem e de língua portuguesa.

**O que pode mudar entre uma atividade e outra (e SÓ isso):**
- Tema/história e mascote
- Conteúdo pedagógico (série, disciplina, desafios)
- Cores do tema
- Imagens (geradas no ChatGPT para o tema novo)

**Todo o resto é FIXO e obrigatório.** Não é "inspiração": é para reproduzir exatamente. Se a atividade entregue divergir em estrutura, dinâmica, disposição, botões, narração ou qualquer item deste arquivo, ela está ERRADA e precisa ser corrigida antes de entregar. Na dúvida sobre qualquer detalhe, PERGUNTAR ao Marcos antes de fazer diferente (ver "REGRA DE CONDUTA"). Ao final de cada entrega, percorrer o checklist da seção 16 e relatar honestamente o que foi cumprido e o que (se algo) ficou pendente.

================================================================
## REGRA DE CONDUTA — NÃO INVENTAR NADA
================================================================
- **NUNCA inventar** nada fora deste modelo: nem botão novo, nem animação diferente, nem disposição própria, nem "melhoria" criativa. O modelo é fixo.
- **Na dúvida, PERGUNTAR ao Marcos ANTES de mexer** — sobre conteúdo, sobre um comportamento não descrito aqui, sobre uma imagem que parece estranha/trocada, sobre um resultado ambíguo de processamento. Parar e perguntar é sempre melhor que entregar errado.
- **Nunca aplicar correção automática em massa** (ex.: reprocessar todas as imagens) sem verificação visual do resultado; se a verificação não for conclusiva, segurar a mudança e perguntar.
- Ao encontrar indício de asset trocado/errado (cor não bate com o esperado, medalha que não parece medalha), NÃO "corrigir" por conta própria: levantar os fatos (dimensões, cores, comparações) e PERGUNTAR.

================================================================
## REGRA DE OURO — O MODELO É FIXO
================================================================
Existe UM modelo de atividade (o "Caça-Letras / A Aventura das Palavras" é a origem dele). TODA atividade nova ou reformada segue EXATAMENTE este modelo em: funcionamento, dinâmica, disposição das telas, botões, recursos, comemoração, narração, gamificação e relatório.

**O que MUDA de uma atividade para outra (e SÓ isso):**
- Tema/história (fazenda, espaço, oceano...) e mascote
- Conteúdo pedagógico (série, disciplina, desafios)
- Cores do tema
- Imagens (geradas no ChatGPT para o tema novo)

**O que NUNCA muda:** toda a estrutura descrita abaixo. Não inventar botões novos, não mover botões de lugar, não trocar o fluxo. Se algo aqui não estiver claro, PERGUNTAR ao Marcos antes de criar diferente.

================================================================
## 1. TELA INICIAL (estrutura exata, nesta ordem)
================================================================
1. **Título** da atividade (h1) + subtítulo (série/disciplina)
2. **Imagem da cena de abertura** (cena ilustrada do tema, gerada no ChatGPT — ver seção IMAGENS)
3. **Campo do nome** ("Digite seu nome") — SEM botão "Entrar sem nome" (se a criança clicar sem digitar, entra sem nome mesmo assim)
4. **Botão principal** "Começar a aventura! 🚀" (classe `pulsa` — salta e brilha)
5. **Dizeres da atividade embaixo, de uma vez** (parágrafo `lead`): o mascote se apresenta e conta a missão
6. **Narrada automaticamente**: ao abrir, o mascote lê a apresentação e convida a digitar o nome

**Se já houver progresso salvo:** mostra "Que bom te ver de novo, [nome]! Você já tem X pontos e completou Y paradas." + botão "▶ Continuar a aventura" (pulsa) + botão pequeno "🔄 Começar do zero" (com tela de confirmação antes de apagar).

================================================================
## 2. MAPA VIVO (estrutura exata)
================================================================
Ordem dos elementos, de cima para baixo:

1. **Topbar fixa**: emblema do nível atual (imagem, sempre visível), nome do nível, XP com barrinha. Atualiza ao ganhar pontos e ao carregar progresso salvo.
2. **Card do topo do mapa**: recompensa-que-cresce (imagem em 3 tamanhos por % de progresso) + **barra de progresso** logo abaixo da recompensa (enche conforme as paradas são concluídas) com contador "Colheita/Coleção: X de N paradas" (concordância correta: "1 parada"/"2 paradas") + título ("A aventura de [Nome]!") + frase-guia ("Siga a trilha! Complete cada parada para abrir a próxima...") + **botão de som redondo 🔊 SEM texto**, logo abaixo do texto (reconta a história do mapa). A recompensa-que-cresce dá o visual lúdico; a barra + contador dão a precisão fase a fase — os dois juntos.
3. **Balão do mascote com a HISTÓRIA** (só na primeira visita, 0 fases concluídas): o enredo completo e o convite.
4. **TRILHA** serpenteante:
   - Cada parada = cenário próprio (imagem) + companheiro (imagem de animal/personagem) + nome da fase + estado.
   - **Parada atual**: destacada, glow `drop-shadow` pulsando (NUNCA `box-shadow` — desenha quadrado), tag "você está aqui". Clicável.
   - **Paradas concluídas**: "Concluída ✓", trecho dourado. Clicáveis (rejogar).
   - **Paradas ainda não jogadas: TRANCADAS** — acinzentadas (`grayscale`), com **cadeado 🔒** sobreposto no cenário, clique bloqueado. Ao tocar, o mascote avisa com carinho: "Esta parada ainda está trancada! Termine a parada anterior para abrir esta." Cada parada só abre quando a ANTERIOR é concluída.
   - **Conector pontilhado** entre cada parada (linha vertical pontilhada dourada; dourado forte nos trechos concluídos).
5. **TROFÉU no fim da trilha** (imagem): visível desde o início (levemente esmaecido + cadeado 🔒 enquanto bloqueado); quando tudo concluído, brilha/pulsa e abre o grande final. Nome legível embaixo.
6. **Botões extras EMBAIXO** (depois da trilha e do troféu), nesta lógica:
   - "🏅 Minhas Medalhas" — SEMPRE visível
   - "✏ Treinar Erros (N)" — SÓ quando houver erros guardados (N>0)
   - "📊 Relatório" — **SÓ quando o aluno concluir TODAS as paradas** (aparece depois do grande final e fica ali embaixo enquanto o aluno não zerar a atividade)
   - "🎧 Ditado" — SÓ quando o Marcos pedir explicitamente esse recurso (não é padrão)
7. **NÃO existe botão "Continuar aventura" no mapa** — a criança clica direto na ilha atual.
8. **Narração do mapa automática** (`narrarMapa()` ao abrir): conta a HISTÓRIA em 3 momentos — início (apresenta enredo e convida), meio (progresso DENTRO do enredo: o que já recuperou, o que falta), fim (comemora o desfecho e aponta o troféu). Usa o nome do aluno. O botão 🔊 reconta.

================================================================
## 3. FLUXO DA FASE (dinâmica exata)
================================================================
1. **Tela de introdução da fase**: imagem do cenário no topo (contida, ~140px, SEM sobrepor o título — título vem abaixo com margem), título da fase, mascote explicando o tema num balão (narrado), botão "Começar! ▶" (pulsa). SEM botão "Voltar ao mapa".
2. **Cada desafio**: barra/contador de progresso ("Desafio X de Y"), enunciado (narrado automaticamente), ilustração da SITUAÇÃO (nunca da resposta), dica "💡", opções/mecânica.
3. **Ao ACERTAR**: 
   - Comemoração grande (carimbo — ver seção 4) + confete
   - Caixa de feedback verde com elogio variado + explicação (`dd.explica`), narrada UMA vez
   - **Botão "Próximo ▶" aparece IMEDIATAMENTE** — a criança CLICA para avançar. **NUNCA avançar sozinho.**
   - **Clicar "Próximo" NÃO corta a narração do feedback** — se o áudio (elogio + explicação) ainda está tocando, ele TERMINA e só então emenda na narração do próximo desafio. O botão aparece na hora (a criança nunca espera), mas o clique não interrompe o que está sendo falado. Em PC sem voz pt-BR, nada trava — avança normal. (Implementação: `avancar()` marca `window._avancando=true`; `narrarDesafio()` usa `falarDepois()` que ENFILEIRA em vez de cortar quando já há fala tocando. Ver seção 10.)
   - No ÚLTIMO desafio da fase, o botão vira **"Ver resultado 🏁"** (também sem cortar o áudio ao clicar).
4. **Ao ERRAR**: aviso gentil ("Quase! Pense de novo..."), o erro é guardado para o Treino, e a criança tenta de novo. Sem punição, sem sistema de vidas.
5. **Durante a fase NÃO há botão de sair/voltar ao mapa** — a criança só avança.
6. **Tela de fim de fase**: "Parada concluída!", medalha da fase revelada (imagem, com número por código), pontuação em destaque ("⭐ N pontos no total"), curiosidade "Uau", mascote comemorando com o GANCHO narrativo da próxima parada (narrado), mensagem "🔓 Você abriu a próxima parada: [nome]!", botão principal "▶ Próxima parada" (pulsa) + botões pequenos "Ver o mapa" e "🔁 Jogar de novo".

**ARRASTAR PRIMÁRIO, TOQUE RESERVA (dinâmica das mecânicas):** onde a ação natural é "levar um item até um lugar" a mecânica é ARRASTAR (ligar sombra, ordenar sequência nos slots, classificar cor/tamanho/forma no "cesto", montar quebra-cabeça); onde é "apontar/escolher um" fica TOQUE (achar o diferente, letra inicial, vogais, contar). Memória (virar carta) e labirinto (setas) têm mecânica própria. O motor de arrastar é GLOBAL + GHOST (um fantasma segue o cursor, o original fica parado; listeners instalados uma vez via `instalarDragGlobal`) — nunca listeners por elemento (acumulam e travam). A instrução na tela bate com a mecânica ("Arraste" x "Toque").

**FASE DA SOMBRA:** bicho colorido em cima, silhueta PRETA embaixo; a criança ARRASTA o bicho até a sombra igual e, ao acertar, **a sombra REVELA o colorido**. Sem quadrado/card nos dois lados (ficam soltos). Para formas vazadas (caranguejo, polvo, estrela), a `<img>` da silhueta leva `pointer-events:none` para a área de acerto ser o box inteiro. Silhueta e colorido apontam para o mesmo lado (ver seção 12).

**FASE LIGAR OS PONTOS:** a criança TOCA nos números em ordem (só toque, NUNCA hover/passar o mouse — quebra no celular); ao ligar o último, some com as bolinhas e aparece a imagem PNG do objeto (animação de revelar por opacidade). O CONTORNO formado pelos pontos tem de ser a MESMA silhueta da imagem revelada — coordenadas extraídas da forma real da imagem (não chutadas), na mesma orientação; preferir figuras simples (estrela, concha). Proteger contra toque-duplo (o contador não pode pular). Fala com artigo de gênero por figura ("desenho da concha").

**FASE LABIRINTO:** grade de células separadas arredondadas; mascote (imagem) andando; troféu como objetivo; monstrinho (água-viva) que faz voltar ao início; vários labirintos em sequência com o TESOURO em posição diferente em cada um (senão a criança decora). Controlado por 4 setas NA TELA (funcionam no toque — ver seção 13) E pelo teclado juntos. É fase-jogo: sem Desafio Extra.

**FASE QUEBRA-CABEÇA:** os espaços formam uma GRADE 2×2 (não uma fileira horizontal) — dar ao container dos slots uma largura fixa que caiba exatamente 2 por linha. As peças vêm de fatiar a foto real do objeto. É fase-jogo: sem Desafio Extra.

**FASE VOGAIS DO MAR (letra inicial de vogais):** cada rodada mostra uma coisa do mar como imagem (água-viva=A, estrela=E, ilha=I, ostra=O, uva-do-mar=U) e a criança TOCA na vogal (bolha-imagem) com que o nome começa. As vogais são faladas foneticamente e pausadas (ver seção 13). Enunciados/dica/erro/gancho falam "vogal", não "letra".

**O DESAFIO EXTRA TEM CÓDIGO PRÓPRIO (lição paga):** o `desafioExtra(fase)` define seus próprios enunciado/opções/gênero/imagens. Um bug corrigido nas rodadas normais pode PERSISTIR no extra (só visível com 100% de acerto — parece intermitente). Ao corrigir/auditar uma fase (concordância, imagem faltando), auditar TAMBÉM o extra dela.

================================================================
## 4. COMEMORAÇÃO (carimbo grande — obrigatório em todo acerto)
================================================================
A cada resposta certa, na tela toda: círculo colorido do tema que "carimba" com pop (escala 0→1.15→1 com leve rotação), check ✓ grande no centro, 2 anéis que se expandem e somem, 8 faíscas de estrelinhas (⭐✨🌟💫) ao redor, e uma **FRASE DE FESTA** grande girando num pool (ex.: "ACERTOU!", "MUITO BEM!", "BOA!", "ISSO!", "PERFEITO!", "MANDOU BEM!", "UAU!", "SHOW!"). Some sozinho em ~1,5s. Acompanha `confete(16)`. Animações só transform/opacity, com par `-webkit-`.

================================================================
## 5. ENGAJAMENTO SAUDÁVEL (os 4 pilares + streak)
================================================================
1. **Elogio variado**: pool de ~10 frases calorosas; nunca repetir seguido (10 acertos ≈ 10 frases diferentes).
2. **Curiosidades "Uau"**: 1 por fase, na tela de fim de fase, narrada.
3. **Gancho narrativo**: no fim de cada fase o mascote PROVOCA a próxima parada como história (nunca um "próximo" seco).
4. **Deleite ligado ao mérito**: nada de sorte/aleatório; recompensa só por conquista real.
5. **Streak**: acertos seguidos disparam pop em 3/5/8/10 com a frase COMPLETA "Você acertou N seguidas!" + reforço; zera no erro e ao iniciar cada fase.

================================================================
## 6. ADAPTATIVIDADE E TREINO
================================================================
- **100% na fase** → oferece Desafio Extra opcional, coerente com a fase (mesma habilidade, um degrau acima), com opções também embaralhadas. Fases-jogo (memória, quebra-cabeça, caça, forca) NÃO levam Extra.
- **<50%** → oferece Reforço com as próprias questões erradas antes de seguir.
- **50–99%** → segue normal, sem oferta.
- **Treino dos erros**: `guardarErro(dd)` acumula em `ERROS`; botão "✏ Treinar Erros (N)" aparece EMBAIXO do mapa só quando N>0; o treino refaz exatamente as N questões erradas.

================================================================
## 7. APOIO AO ERRO POR CONTAGEM ACESA (toda fase de contar)
================================================================
Quando a criança erra uma contagem: (1) mascote fala "Não foi dessa vez! Agora vamos contar juntos, bem devagar." (com carinho); (2) quando essa frase TERMINA (callback do `falar`), uma pausa curta e começa a contagem; (3) **ACENDE cada objeto UM POR UM EM SINCRONIA COM A FALA** — a luz do objeto acende JUNTO com a voz dizendo o número (classe que dá SÓ glow via `filter:drop-shadow` dourado — NUNCA `transform:scale`), contando em voz alta **POR EXTENSO** ("um... dois... três..."); (4) todos contados: "São N ao todo! Agora toque no número N." e apaga.
**A FALA COMANDA A LUZ — não dois relógios (lição paga)**: a versão antiga usava `setTimeout` de ritmo FIXO enquanto a fala corria numa fila própria — os dois se DESENCONTRAVAM. Correto: encadear pela fala. `contarPasso(k,n)` acende a luz do objeto k, chama `falar(numExt(k+1), callback)`, e SÓ no callback (voz terminou) faz pausa ~260ms e chama `contarPasso(k+1,n)`. Todas as luzes apagadas durante a abertura. O `falar` com callback já degrada sem voz (dispara por tempo estimado), então não trava. Cada objeto tem `id` próprio (`cItem0`...). Números por extenso via `numExt(n)`, acentuados.

================================================================
## 8. GRANDE FINAL E RELATÓRIO
================================================================
- **Grande final** (ao concluir tudo): imagem da CENA FINAL ilustrada no topo, título emocionante, confete em ondas, mascote comemorando, desfecho da HISTÓRIA fechado, recompensa no tamanho máximo, emblema do nível, estatísticas (com concordância: "1 ponto"/"2 pontos"). Botão principal "📊 Ver meu relatório" + "🏅 Minhas conquistas" + "Voltar ao mapa".
- **Relatório do professor**: tabela por fase (acertos/erros/% com cor), o que revisar, dica de imprimir. Acessível a partir do grande final; depois disso, o botão "📊 Relatório" fica EMBAIXO do mapa (enquanto o aluno não zerar a atividade). **Nunca aparece antes de concluir tudo.**

================================================================
## 9. BOTÕES (hierarquia e animação — IDÊNTICO à referência)
================================================================
- **Animação `pulsa` = pulso suave de ESCALA** (`scale(1)` → `scale(1.05)` → `scale(1)`, 1.3s ease-in-out infinito, par `-webkit-`). **NUNCA usar salto/pulinho, brilho piscando ou balanço** — o modelo não tem isso.
- **Recebem `pulsa`** (guia visual da criança): botões principais de cada tela (Começar a aventura, Continuar a aventura, Começar!, Próximo ▶, Ver resultado 🏁, Próxima parada, Aceitar desafio, Ver meu relatório, "Sim" da confirmação de reset), o botão **"✏ Treinar Erros (N)"** e o **botão de som 🔊** do mapa.
- **Botões secundários são ESTÁTICOS** (sem animação nenhuma): Minhas Medalhas, Relatório, Ver o mapa, Jogar de novo, Começar do zero, "Agora não", "Não, voltar".
- **Botão de som do mapa**: redondo ~34px, dourado, só o ícone 🔊 sem texto, no topo perto do texto do mapa; `:active` afunda 2px.
- Todos os botões: cantos arredondados, sombra "3D" inferior (`box-shadow 0 4-5px 0 <cor escura>`), `:active` afundando.

================================================================
## 10. NARRAÇÃO / TTS (qualidade obrigatória — A CRIANÇA OUVE TUDO)
================================================================
- `limparFala()`: remove tags/entidades HTML, corrige espaço após pontuação, junta espaços duplos, SEMPRE põe ponto final; **normaliza pronúncia** de palavras sem acento que o TTS erra ("voce"→"você", "magica"→"mágica", etc. — regex `\bpalavra\b/gi` preservando capitalização; adicionar novas palavras sempre que uma pronúncia errada for notada).
- `escolherVoz()`: melhor voz pt-BR (prioriza natural/neural/enhanced/google/microsoft/maria/francisca/luciana).
- Ritmo `rate ~0.92`, `pitch ~1.08`. Texto quebrado em frases (`. ! ? :`) faladas em fila com ~180ms de pausa.

**VOGAIS FALADAS FONETICAMENTE E PAUSADAS (lição paga):** o TTS pt-BR lê vogal isolada com o som errado. Escrever foneticamente na fala (tela ≠ fala): A→"á", E→"é", I→"i", O→"ó", U→"úú" (o U sai fraco; alongar dá presença). Helper `vogalFalada(letra)`. Para soarem PAUSADAS, cada vogal é uma FRASE separada (PONTO, não vírgula) — a lista "A, E, I, O, U" vira "á. é. i. ó. úú." e o `fatiarFrases` fala cada uma com pausa. NUNCA converter "A"/"E" soltos globalmente (viram artigo — "a estrela" vira "á estrela"): a regra segura no `limparFala` só pega a sequência COMPLETA das 5 vogais em ordem. Palavras que o TTS erra ganham entrada fonética na tabela (ex.: "olho"→"óio", senão sai "óleo"). `feedbackAcerto(explica, semAvancar, falaExplica)` permite tela ≠ fala (tela mostra "U", fala diz "úú").

**FALA NUNCA É CORTADA (lição paga — a criança precisa ouvir tudo até o fim):**
O erro clássico é cada `falar()` começar com `cancel()`, então falas em sequência (elogio + streak + subir de nível + conquista) se cortavam e a criança ouvia só pedaços. Padrão obrigatório com TRÊS funções:
- **`falar(txt, aoTerminar)`** — inicia uma narração NOVA, cancelando a anterior. Usar SÓ em troca de contexto/tela (abrir mapa, ir para próxima parada, abrir fase). É o único que corta — de propósito, para o áudio não vazar de uma tela para outra.
- **`enfileirarFala(txt)`** — ADICIONA ao fim da fila SEM cortar o que está tocando. Usar quando duas falas devem ser ouvidas em sequência (elogio + frase de streak, subir de nível, conquista). O pop de streak/nível/conquista usa `popCaixaFila()` (variante do `popCaixa` que enfileira em vez de cortar).
- **`falarDepois(txt)`** — se já há fala tocando, enfileira; senão fala na hora. Usado ao AVANÇAR de desafio, para o próximo enunciado não cortar o feedback anterior.
- **Ordem no acerto:** `feedbackAcerto()` narra o elogio+explicação PRIMEIRO (via `falar`, fila limpa) e SÓ DEPOIS dispara streak/nível/conquista (que entram na fila com `enfileirarFala`/`popCaixaFila`) — assim tudo é ouvido em ordem, nada é cortado.
- **Proteção de fila (`_falaSeq`):** um contador incrementado a cada `pararFala()`; cada frase agendada só continua a fila se o contador não mudou. Isso impede que uma fila antiga volte a tocar depois de uma troca de tela.
- **Sem voz pt-BR instalada:** a fila roda em modo silencioso com tempo estimado por frase (nunca usa `onend`, que pode não disparar) — nada trava, e o fluxo/botões seguem normais.

- **Narração automática em TUDO**: tela inicial, mapa (história), introdução de fase, cada enunciado ao abrir, feedback após responder, fim de fase, grande final, jogos. Botão para repetir onde couber.
- **A narração do enunciado NUNCA revela a resposta** (nada declarativo depois do último "?"). A explicação (`dd.explica`) só é falada DEPOIS que a criança responde.

**BOTÃO NARRADO EM TODA A ATIVIDADE (não só nos desafios):** o botão principal de cada tela que abre com narração aparece na hora mas começa DESABILITADO mostrando "🔊 Ouvindo..." e só habilita quando a fala do mascote termina (via callback), para a criança não pular a narração. Vale para tela inicial (Começar/Continuar), intro de fase (Começar!), fim de fase (Próxima parada/Ver final), oferta de Extra (Aceitar), oferta de Reforço (Continuar) e grande final (Ver relatório), além dos desafios. Helper único `botaoNarrado(txt, onclick, extraCls)` + `falarComBotao(texto)` (libera via callback do `falar`, com reserva por tempo se não houver voz pt-BR; cancelar o timer anterior ao criar um novo).
- Valores monetários por extenso ("R$ 3,50" → "3 reais e 50 centavos"; "R$ 1,00" → "1 real").
- Bilíngue: detectar idioma FRASE A FRASE (`detectaPT`) e usar a voz certa; pular a frase se não houver voz do idioma.

================================================================
## 11. LÍNGUA PORTUGUESA IMPECÁVEL (auditoria obrigatória)
================================================================
NENHUM texto da atividade pode ter erro de português. Antes de entregar, revisar TODOS os textos (títulos, enunciados, opções, explicações, falas, botões, relatório):
- **Acentuação e pontuação corretas** em todas as strings visíveis e faladas.
- **Concordância de NÚMERO e GÊNERO em todo texto dinâmico**: usar `pluralG(n, genero, sing, plur)` (n=1 vira "uma/um"+singular — nunca o dígito "1", que o TTS lê como "um" masculino), `plural(n, sing, plur)` para casos sem gênero, `numExt(n)` para contagens faladas. NUNCA substantivo em plural fixo ao lado de número variável ("1 acertos" é bug).
- **Auditar n=1 e n>1**: forçar cenário com 1 ponto / 1 medalha / 1 acerto no relatório e no grande final; varrer por regex `\b1\s+(pontos|acertos|medalhas|...)`.
- Referência de gênero: feminino = palavra, ilha, medalha, letra, estrela, moeda, fase, cesta, parada; masculino = ponto, acerto, erro, amigo, tesouro, dia, número.
- **Falas naturais e calorosas** — nada robótico, estranho ou truncado. Ler cada fala "em voz alta" mentalmente: soa como uma pessoa querida falando com uma criança?
- **Enunciados coerentes**: o texto nomeia o MESMO objeto que a ilustração mostra; opções são palavras/valores íntegros e coerentes; nada de "O de 7" (parece zero — usar "Grupo de 7").
- **Explicações que fazem sentido**: no acerto, a explicação CONFIRMA a resposta com o motivo VERDADEIRO (nunca justificativa inexata); no erro, corrige com carinho e ensina o caminho. Tanto o enunciado quanto o feedback devem ser lidos e conferidos um a um.

================================================================
## 12. IMAGENS — GERADAS NO CHATGPT, FUNDO TRANSPARENTE, ANIMAÇÃO SUAVE
================================================================
**Regra central**: TODO asset-chave é IMAGEM PNG gerada no ChatGPT, recortada com FUNDO TRANSPARENTE DE VERDADE, SEM vestígios brancos, e com animação suave (entrada pop + flutuação leve, par `-webkit-`). Lista do que é sempre imagem: mascote (4 poses), cenários das paradas, companheiro de cada fase, objetos de contagem/questões, emblemas de nível, medalhas (número adicionado por código), selos/conquistas, troféu, recompensa-que-cresce, CENA de abertura e CENA do grande final (estas duas são cena inteira: viram JPEG de fundo, não recorte).

**PRINCÍPIO (não esquecer):** o prompt do ChatGPT NÃO resolve sozinho o problema de parte branca/franja. Um prompt bem-feito (fundo branco puro + SEM sombra + contorno escuro definido) PREVINE a maior fonte (a sombra na base) e facilita o recorte, mas SEMPRE sobra uma franja fina de borda e às vezes vãos internos — e isso só some com a LIMPEZA obrigatória do lado do código (passos 5, 6b). **Garantia = prompt bom + limpeza obrigatória juntos.** Nunca embutir uma imagem sem ter passado pela limpeza e pela conferência visual.

**CORPO BRANCO SEM CONTORNO ESCURO = FRANJA IRRECUPERÁVEL (lição paga, crítica):** se a cartela desenhar um objeto/animal BRANCO (coelho, ovelha, galinha, ovo, pato) SEM uma linha de contorno escura e fechada, o corpo branco encosta direto no fundo branco — não há fronteira. O recorte deixa uma borda branca esfarrapada, e tentar removê-la por código só PIORA (expõe mais branco do corpo; medido: coelho foi de 21% de franja para 78% e comeu 8,5% do corpo). **NÃO existe conserto por código nesse caso — a ÚNICA solução é REGERAR a cartela** com o prompt exigindo "contorno preto grosso e fechado em volta de cada objeto, INCLUSIVE os brancos". Diagnóstico rápido: medir % de contorno escuro na borda do recorte; se for ~0% e houver muito branco na borda, a cartela veio sem contorno → pedir para regerar, não tentar limpar. (Com o contorno, a franja cai para 0%.)

**ORIENTAÇÃO SILHUETA vs COLORIDO — MESMO LADO (lição paga):** na fase da sombra, silhueta preta e bicho colorido do mesmo animal têm de apontar para o mesmo lado (senão a criança vê a tartaruga virada para um lado e a sombra para o outro). Diagnóstico: comparar o centro de massa horizontal (lado que "pesa") do colorido e da silhueta; se opostos, estão invertidos. Correção sem regerar: espelhar a silhueta por código (`PIL FLIP_LEFT_RIGHT`) — seguro, pois silhueta é forma preta chapada. Auditar todos os pares antes de entregar a sombra.

**QUANDO A VISUALIZAÇÃO DE IMAGEM DO CLAUDE FALHA — AVISAR (lição paga):** a visualização do Claude pode voltar vazia. As métricas (franja, cor) seguem válidas, mas NÃO enxergam enquadramento (orientação, cabeça-para-baixo, corte, dois bichos colados) — só o olho pega. Quando falhar: AVISAR o Marcos de forma destacada, embutir por número só se o risco for baixo e puramente de franja/cor (contorno fechado + franja ≤1%), e deixar o mosaico `conferir_*.png` em outputs para o Marcos conferir. "Franja ok" ≠ "imagem ok". Ambíguo ou não pôde ver = apontar como PENDÊNCIA visual, nunca dar por concluído.

**OBJETOS DE CONTAGEM — variedade (não cansar a criança):** cada fase de contagem tem 2-3 objetos temáticos coerentes com o lugar, e a fase ALTERNA entre eles por desafio (helper `objDaFase()` cicla pela lista `F.objs` por `idxDesafio`; mantém `F.obj` como fallback). Nunca um único objeto repetido em 5-6 desafios seguidos. Gerar todos os objetos da fase na MESMA cartela.

**Fluxo:**
1. Claude entrega os prompts prontos numa página HTML com botão "Copiar". Cada prompt (cartela ÚNICA) DEVE pedir: itens em grade bem separados; fundo branco liso #FFFFFF sem textura/moldura/cartão; cartoon flat infantil, cores vivas; **SEM NENHUMA SOMBRA (nem projetada, nem elíptica de contato embaixo) — objetos flutuando no branco puro**; **contorno escuro e fechado em volta de cada objeto** (separa do fundo e do próprio branco interno, ex.: ovo); **sem partes brancas/cinza coladas na borda externa**; **objetos sólidos sem vãos internos vazados**; sem texto/letras/números. As CENAS (abertura/final) pedem retângulo deitado 3:2 preenchendo tudo (podem ter sombras normais, pois viram fundo inteiro).
2. Marcos gera UMA cartela por vez e envia.
3. **ANTES de recortar, diagnosticar o arquivo REAL no disco** (dimensões + análise de cores dominantes): os uploads às vezes chegam CORTADOS (só uma fileira) ou são OUTRA cartela que não a do preview do chat. Se não bater com o esperado, AVISAR e pedir reenvio — nunca recortar no escuro.
4. Recortar com PIL por COMPONENTE CONECTADO (scipy.ndimage.label; nunca célula fixa), flood-fill do branco, fill_holes, dilatação leve, margem transparente ~9-10%.
5. **DE-FRINGE OBRIGATÓRIO (lição paga)**: após o recorte, remover o HALO da borda — (a) zerar alpha dos pixels quase-brancos (R,G,B>226) na fronteira com a transparência; (b) erodir o alpha 1px; (c) zerar pixels semitransparentes claros; (d) suavizar e BINARIZAR o alpha (>130→255, senão 0). **ATENÇÃO: a franja também pode ser CINZA-CLARA (≥200, dessaturada), não só branca** — se após o primeiro passe ainda houver fio claro no contorno, aplicar um passe extra que erode +1px e mata pixels claros dessaturados no anel da borda. Sem isso, TODA imagem fica com contorno claro feio no fundo escuro.
6. **INSPEÇÃO VISUAL OBRIGATÓRIA antes de embutir**: montar o mosaico em fundo xadrez E TAMBÉM em FUNDO ESCURO (a cor de fundo da atividade), com ZOOM nas bordas, e conferir com os olhos. **Métricas numéricas sozinhas NÃO bastam** — corpos legitimamente brancos (galinha, ovo, coelho, medalha com símbolo claro) confundem qualquer métrica de "borda clara". Se a inspeção visual não for conclusiva, NÃO embutir: perguntar ao Marcos. Validar também por cor dominante (ex.: maçã tem que ser vermelha; se sair roxa, a cartela está trocada — PERGUNTAR, não corrigir sozinho).
6b. **LIMPEZA PROFISSIONAL PÓS-RECORTE (conferir TODA imagem, mesmo antiga):** três defeitos que sobram do fundo branco e aparecem no fundo escuro:
   - **Resto de SOMBRA na base** (mancha creme/cinza sob o objeto): remover componentes claros dessaturados (mín RGB≥185, saturação baixa) pequenos (4px até ~4% do objeto) com centro no terço inferior, mais migalhas nas ~6 linhas finais. **NUNCA aplicar essa régua em corpos brancos/creme (ovo, coelho, galinha, ovelha, vaca, pato...) sem conferir com os olhos — ela raspa o próprio corpo.**
   - **VÃO INTERNO branco opaco** (ex.: vão entre alça e cesta, alças de troféu): o fill_holes do recorte fecha esses buracos com branco. Detectar componentes branco-puros (≥240, dessaturados) grandes e torná-los transparentes — **somente com confirmação visual**; em corpos brancos e cenários com nuvens, NUNCA automático (o "vão" pode ser o corpo/a nuvem).
   - **FRANJA cinza-clara no contorno**: matar pixels claros dessaturados (≥200) no anel de 2px junto à transparência.
   Em TODA remoção: verificação numérica por imagem (perda ≤ poucos %, zero claros restantes na base, RGB intocado fora do alpha removido); imagem sem nada a remover mantém o base64 original; qualquer resultado ambíguo = NÃO embutir e perguntar.
7. Otimizar: resize pela altura de uso (objetos ~110px, companheiros ~150px, medalhas/selos ~150-170px, troféu ~190px), `quantize(28-44 cores, MEDIANCUT, dither=NONE)`, alpha binário (`>120→255,0`). Cenas: JPEG quality 82, largura ~640px.
8. Embutir base64 e apresentar a atividade RENDERIZADA (Marcos não vê recortes intermediários).

================================================================
## 13. CSS ROBUSTO PARA NAVEGADOR ANTIGO (lições pagas — NUNCA repetir)
================================================================
- **NUNCA usar `width:100%; height:100%; object-fit:contain` em imagem** — em Firefox 106/Chrome antigo isso COLAPSA a imagem para tamanho zero (imagem "some"). Usar SEMPRE largura explícita em px OU `width:100%; height:auto`, com `display:block`. Auditar o CSS inteiro por esse padrão antes de entregar.
- **Imagem RETRATO (mais alta que larga) em container de tamanho fixo — dimensionar pela ALTURA, nunca pela largura (lição paga: mascote sobrepondo a ilustração do desafio).** O mascote gerado no ChatGPT é retrato (~163×220); com `width:100%; height:auto` num container 78×78 ele renderiza ~105px de altura, ESTOURA o container para baixo e COBRE o conteúdo abaixo. Correto: container com px definido + `img { display:block; height:100%; width:auto; margin:0 auto; }` + `overflow:hidden` no container. **O mascote JAMAIS pode sobrepor as imagens ou o conteúdo da atividade** — auditar renderizando as telas de desafio.
- Glow de destaque em PNG recortado: `filter:drop-shadow` (com par `-webkit-filter`) — NUNCA `box-shadow` (desenha retângulo ao redor do recorte).
- Objetos de contagem: `display:block; width:100%; height:auto` no container com px definido.
- Flexbox sempre com fallback `-webkit-box` (+ `-webkit-box-flex` explícito nos filhos; sem isso o filho pode colapsar).
- Toda animação: par `@-webkit-keyframes` + `@keyframes`; animar só transform/opacity; contagem de pares deve bater (nº de @keyframes == nº de @-webkit-keyframes).
- Imagens não-quadradas: altura fixa + `width:auto` (nunca WxH fixos — estica). Cards com `overflow:visible` onde há halo/animação. Animação de revelar sem `scale>1` no meio (estoura a borda durante a animação).
- Nomes/rotulos sobre o mapa: cor sólida legível com bom contraste (auditar contraste em TODO texto).

**TELA CHEIA + LAYOUT ADAPTATIVO (lição paga):** botão flutuante de tela cheia (`requestFullscreen` com prefixos `webkit`/`moz`/`ms`) que só APARECE se o navegador suportar (`telaCheiaSuportada()`) — senão fica `display:none`, sem quebrar o PC antigo; ativar exige clique do usuário. Para telas grandes, aumentar o `max-width` do `.wrap` só via `@media (min-width:700px/1000px)` (ex.: 520→680→820px); no CELULAR (≤699px) NADA muda, continua 100% da largura como antes. Auditar que o botão flutuante não cobre o título no celular (reservar respiro no topo; botão menor no celular). Testar 320–1920px: zero overflow, zero sobreposição.

**BOTÕES DE AÇÃO NO TOQUE — `onclick` SOZINHO NÃO FUNCIONA EM MUITOS CELULARES (lição paga, crítica):** botões que a criança usa para agir direto (setas do labirinto, controles de jogo) precisam de `ontouchstart` ALÉM do `onclick`, senão no celular real a criança toca e nada acontece. O `ontouchstart` executa a ação na hora (com `preventDefault`/`stopPropagation`); o `onclick` só age se não veio de um toque nos últimos ~500ms (ignora o click-fantasma). CSS do botão: `touch-action:manipulation`, `-webkit-tap-highlight-color:transparent`, `user-select:none`. Testar SEMPRE em modo toque (device emulado + `tap`), nunca só clique de desktop.

**TOQUE-DUPLO DISPARA O EVENTO 2× (lição paga):** no celular, um toque pode disparar o handler duas vezes (touch + click-fantasma). Em mecânicas que avançam um contador por toque (ligar-pontos em ordem), o contador pula e o próximo toque certo vira "errado" (sintoma: "toco certo e diz que não é o próximo"). Proteção: ignorar o mesmo valor repetido em <~350ms. Só reproduz no toque real.

**BUG QUE "PERSISTE" NA VERSÃO PUBLICADA = CACHE (lição paga):** bug já corrigido que continua aparecendo na versão publicada costuma ser o CACHE servindo o `index.html` antigo. Confirmar o código atual pelo teste e orientar recarregar forçado (aba anônima / "Começar do zero"). SEMPRE lembrar o Marcos de limpar o cache ao republicar.

================================================================
## 14. COMPATIBILIDADE SAGRADA (resumo — detalhes no MANUAL)
================================================================
- JS: só `var`, `function`, `for` clássico. PROIBIDO: `=>`, `let`/`const`, crase, `?.`, `??`, `async/await`, spread, lookbehind. Sem acento em nome de variável. Validar `new Function('"use strict";'+js)`.
- CSS: PROIBIDO `grid`, `gap`, `clamp()`, `var(--)`.
- **Emojis: só Unicode 6.0 (2010) ou anterior.** Seguros já validados: ⭐ ✨ 🌟 💫 🎉 🔊 ▶ ✏ 🔒 🔓 🔁 🔄 🚀 🏁 📊 🏅 ✓ ✔ 🏆 💡 🔥. REMOVER variation selectors (FE0F). Proibidos (viram quadrado): 🗺 🤔 🥇🥈🥉 bandeiras 🦊🦉 e qualquer 2014+.
- Arquivo único `index.html`, assets base64, `localStorage` com fallback em memória.
- Sem overflow horizontal em 414/390/360/320px.

================================================================
## 15. GAMIFICAÇÃO (estrutura padrão)
================================================================
- Níveis com XP (5 níveis temáticos), emblema do nível SEMPRE visível na topbar (atualiza em addPontos/carregar/boot).
- Subir de nível: fanfarra + confete + fala.
- Selos/conquistas (imagens do tema) em marcos: 1º acerto, streak, 1ª fase, metade, jogo, tudo.
- Medalha por fase: um MEDALHÃO DOURADO (círculo de ouro com fita/laço colorido e borda serrilhada) com o SÍMBOLO da fase no centro (ovo, maçã, vaca, cenoura, osso, troféu...) — NÃO é o bicho/mascote inteiro nem emoji. Imagem dourada temática recortada; o NÚMERO (1..N) é adicionado por código via overlay `.med-num` centralizado. Regerar ao refazer a atividade. (Lição paga: uma cartela de "bichos" no lugar de medalhões passou como medalha sem ser — conferir % de dourado no recorte: medalhão tem ~37-56% dourado; se der 1-3%, é figura, não medalha → regerar.)
- Toda fase termina chamando a tela de fim de fase (registra `concluidas[fase]` e conquistas).

================================================================
## 16. AUDITORIA DE QUALIDADE OBRIGATÓRIA — 3 NÍVEIS
================================================================
Antes de entregar QUALQUER atividade (criação ou upgrade), rodar a auditoria nos 3 papéis, DE VERDADE (executando, não de memória). Só entregar se todos passarem; relatar honestamente qualquer pendência.

### NÍVEL 1 — DESENVOLVEDOR SÊNIOR (compatibilidade e código)
1. **Modo estrito**: `new Function('"use strict";'+js)` sem erro.
2. **Zero JS moderno**: sem `=>`, `let`, `const`, crase, `?.`, `??`, spread `...`, `async`, `await`, lookbehind. (Varrer o all.js.)
3. **Zero CSS moderno**: sem `grid`, `gap`, `clamp()`, `var(--)`.
4. **Keyframes pareados**: nº `@keyframes` == nº `@-webkit-keyframes`.
5. **Zero funções duplicadas**: cada `function nome(` aparece 1× (após qualquer reformulação, é risco crítico).
6. **Zero variável acentuada** no nome.
7. **CSS de imagem robusto**: NENHUM `width:100%;height:100%;object-fit` (colapsa a imagem no PC antigo); imagem retrato dimensionada pela ALTURA (mascote não sobrepõe); glow com `drop-shadow` (não `box-shadow`).

### NÍVEL 2 — QA SÊNIOR (funcionamento e runtime)
8. **Play-through programático de TODAS as fases** (simulador `node sim.js` ou Playwright) terminando com **0 erros**; zero overflow em 414/390/360/320px.
9. **Zero emoji moderno / VS16**: varrer TODOS os code points >0x1F300 e 0xFE0F contra a lista segura.
10. **Toda função de `onclick` existe** (nenhuma referência quebrada).
11. **Embaralhamento REAL**: rodar a mesma fase várias vezes e confirmar que a posição da resposta certa VARIA (`_mix`, checagem por VALOR); `opcoesImg` também embaralhado quando houver.
12. **Fala nunca cortada**: existem `falar`/`enfileirarFala`/`falarDepois`/`popCaixaFila`; no acerto, elogio+explicação é ouvido inteiro e streak/nível/conquista entram DEPOIS sem cortar; clicar "Próximo"/"Ver resultado" NÃO corta o feedback (áudio termina e emenda no próximo); trocar de tela CORTA de propósito. Testar a sequência de um acerto com streak: todas as falas em ordem, zero cortes após iniciar.
13. **Adaptatividade**: 100%→oferece Desafio Extra; <50%→oferece Reforço; erros→Treino aparece embaixo do mapa. Reset apaga tudo e volta à tela inicial.
14. **Mapa**: só a parada atual clicável; demais TRANCADAS com cadeado (clique dá aviso); conectores pontilhados presentes; troféu visível (cadeado até 100%); Relatório só aparece com tudo concluído; barra de progresso da recompensa enche por %.

### NÍVEL 3 — PEDAGOGO EXPERIENTE (conteúdo, língua, áudio)
15. **Matemática/conteúdo consistente**: toda resposta certa está nas opções; todo produto/divisão confere; divisões exatas; zero opções duplicadas. (Varrer todos os desafios programaticamente.)
16. **Concordância de número e gênero** auditada com n=1 E n>1, na TELA e na FALA: forçar 1 ponto/1 medalha/1 parada/1 acerto no relatório e no grande final → "1 ponto", "1 medalha" (nunca "1 pontos"). Varrer por `\b1\s+(pontos|acertos|medalhas|paradas|...)` hardcoded. Usar `pluralG`/`plural`/`numExt`.
17. **Números falados por extenso corretos e ACENTUADOS**: conferir `numExt` — "três" (não "tres"), "treze", "vinte e três", etc. (o texto vai direto ao TTS na contagem do apoio ao erro).
18. **Normalização de pronúncia** cobre as palavras da atividade (você, número, próxima, divisão, multiplicação, tema...); adicionar qualquer palavra que o TTS ler errado.
19. **Narração não entrega resposta**: nada declarativo após o último "?"; a explicação (`dd.explica`) só é falada DEPOIS de responder. Narração automática em todas as telas.
20. **Enunciados coerentes** (nomeiam o objeto que a ilustração mostra; opções íntegras; nada de "O de 7") e **explicações verdadeiras** (confirmam a resposta com o motivo real; no erro, corrigem com carinho). Ler cada fala "em voz alta" mentalmente: soa natural e carinhosa para uma criança?
21. **Português impecável**: acentos e pontuação corretos em TODAS as strings visíveis e faladas (varrer por palavras comuns sem acento).
22. **Imagens**: conferidas por cor/mosaico (cada chave tem o desenho certo; maçã vermelha, etc.); transparência real; SEM parte branca / franja / sombra na base / vão interno (passaram pela limpeza do passo 12/6b); mascote não sobrepõe conteúdo.

### ENTREGA
23. Único `index.html` (sem cópia com nome descritivo).
24. Relatar honestamente o que foi cumprido e o que ficou pendente (ex.: cartela que só o Marcos gera, imagem segurada por dúvida) — nunca entregar como completo se faltar item; na dúvida, perguntar.

================================================================
## 17. POSTURA
================================================================
- **Toda atividade nova ou upgrade deve ficar IDÊNTICA ao modelo deste arquivo** — mesma tela inicial, mapa, fluxo, botões/animações, comemoração, narração (fila que não corta), gamificação, relatório, regras de imagem e de português. Só muda tema, conteúdo, cores e imagens. Divergiu do modelo = está errado, corrigir antes de entregar.
- Este modelo é o padrão para CRIAR e para dar UPGRADE. "Melhorar/deixar premium" = aplicar TUDO deste arquivo.
- Uma cartela de imagem por vez; conferir SEMPRE o que chegou no disco antes de recortar; de-fringe + limpeza de sombra/vão/franja; mosaico em fundo escuro antes de embutir.
- Na dúvida sobre conteúdo pedagógico ou qualquer coisa fora do modelo, PERGUNTAR antes de mexer — nunca inventar.
- Validar rodando (modo estrito, play-through, concordância n=1, fala sem corte), não de memória.
- Entregar sempre como único `index.html`. Honestidade total sobre bugs, pendências e limitações.


================================================================
## 18. ÚLTIMOS APRENDIZADOS (resumo — detalhes técnicos no MANUAL §18)
================================================================
- **Botão narrado → liberar só após SILÊNCIO CONTÍNUO:** o botão que espera a narração não pode liberar numa fresta de silêncio antes de streak/conquista/nível (que entram depois por `setTimeout`). Exigir ~650ms de silêncio contínuo; zera se algo novo é enfileirado. Vale em toda tela com narração + botão de avançar.
- **Não narrar símbolos/pontuação solta/lacunas** (`___`, `() [] {} «»“”‘’ * # ~ | < > = + @`, travessão, reticências): o `limparFala` remove antes de falar (só letras, números e `. , ! ? :`).
- **Dígito "2" tem gênero na fala** (dois/duas): só 1 e 2 flexionam; "2 vacas"→"duas vacas", "2 vezes"→"duas vezes" (complementa a seção 11).
- **Enunciado (texto+fala) bate com a figura mostrada** — cuidado quando o objeto é sorteado/cicla.
- **Arrastar de verdade:** a `<img>` dentro do item dispara o drag NATIVO e sequestra o mouse → `preventDefault` de `dragstart`/`mousedown` + `touch-action:none` + `-webkit-user-drag:none`; PRESERVAR as classes `arrasta`/`solta` ao reconstruir o `className`; testar com evento REAL (não sintético).
- **Caça-palavras por PONTAS:** tocar a 1ª e a última letra da palavra (valida a linha reta nos dois sentidos), nunca tocar letra por letra acumulando.
- **"Pôr em ordem", nunca "quebra-cabeça"** para a fase de ordenar; e ordenar é ARRASTAR primário (toque reserva).
- **Montar a conta de MULTIPLICAÇÃO aceita as duas ordens** (3×5 e 5×3 = 15); a DIVISÃO não (6:2 ≠ 2:6).
- **Modo professor (senha `1275@`):** digitar no teclado destrava todas as fases para teste (liga/desliga), sem alterar o progresso do aluno. Não é segurança (fica visível no código) — é atalho de professor.
- **Prova com texto de leitura:** leitor genérico (vários textos em sequência), imagem embutida em base64, narração automática + botão "🔊 Ouvir o texto", e o botão de avançar só habilita ao fim da narração.
- **Screenshot headless pode não bater com o viewport real** (layout a 500px): medir `innerWidth`/`scrollWidth` antes de "consertar" um falso overflow; `max-width:100%` funciona. (O headless prende a largura mínima em ~500px — não testa celular de 320/360px; calcular o overflow na mão.)
- **Tela cheia tem que AUMENTAR o jogo, não só a moldura:** alargar só a `.wrap` deixa cartas/células pequenas no centro; e no celular a tela cheia não muda a largura (media query nem dispara). Nos listeners de `fullscreenchange` alternar `body.tc-ativa` e no CSS aumentar os elementos do jogo sob essa classe (memória 96px, caça 34px, teclas/peças/títulos maiores). Dimensionar pela pior largura p/ não estourar; ao sair, remover só a classe `tc-ativa` (não zerar o `className`).
- **Imagem de abertura/final como medalhão REDONDO (PADRÃO FIXO — em TODA atividade):** "será sempre desse jeito"; toda capa nova/revisada nasce redonda (Vila do Miau, Poli e Climas já feitos; capa retangular antiga = converter). Foto grande da tela inicial/final fica melhor como círculo (`border-radius:50%`, quadrado ~220px→260px, `object-fit:cover`+`object-position:center` p/ recortar no centro sem distorcer), com borda no tom da atividade, sombra e leve flutuar (`@keyframes boia`). Prefixos `-o-`/`-webkit-`. Conferir por screenshot que o recorte pega o mascote.
- **TTS — junção que vira outra palavra:** a voz cola palavras vizinhas ("às sombras" → soa "assombras"). Grafia está certa, não é bug de código — REESCREVER a frase (singular/reordenar: "cada bichinho à sombra certinha dele"). Atenção a `a/às/as`+`s`/vogal, `de`+vogal. Ler em voz alta na dúvida (headless não dá pra ouvir).
- **Fila horizontal: largura fixa no container vira grade:** p/ itens numa única linha (ordenar do menor ao maior), `width` fixo estreito no container (`.slots{width:184px}`) quebra em 2×N. No modo fila: `width:auto;max-width:100%;white-space:nowrap` + dimensionar os quadros p/ caber todos (4×~64px cabe em 320px); `overflow-x:auto` de reserva. Usar classe modificadora condicional (`.slots.fila`) p/ não afetar outras fases. Conferir screenshot `linhas=1`.
- **Trava de áudio num só ponto (gatear dentro do `falar`):** com muitos botões "Próximo" espalhados, não edite cada um — no início do `falar()`, uma `_gatearAvanco()` varre `#app` e desabilita só os botões de avançar (`onclick` com `proximoDesafio` ou classe `gate-audio`), retorna um `liberar()` encadeado no callback de término do `falar` (+ `setTimeout` de segurança 20s). Um gancho cobre todos os feedbacks e telas narradas, sem tocar em "Conferir". Classe `travado-audio` pro visual. Sem voz, libera em ~300ms.
- **Imagens da professora → pasta `_imagens/` (regras fixas):** o Claude não gera imagem (só o prompt). **SEMPRE imagem real do ChatGPT, NUNCA SVG** (o SVG é só fallback técnico, não o visual pretendido). Ao criar/atualizar, entregar uma **lista de prompts** com o **nome do arquivo** de cada um (`capa.png`, `mascote-feliz.png`, `q1-x.png`…). A prof gera e sobe em lote em `_imagens/` (github.com, funciona no celular) e avisa; Claude puxa → Pillow (autocrop/otimiza) → embute base64. **Questões ganham imagem de contexto** (padrão, igual Vila do Miau) — uma por questão. **Depois de embutir, APAGAR as imagens de `_imagens/`** (pasta sempre vazia, só o guia fica). Guia em `_imagens/LEIA-ME.md`.
- **Dica/instrução com LUZ, não caixa pontilhada:** o textinho de dica das fases é solto, itálico, com **brilho suave** (`text-shadow` dourado + respiro de `opacity`), nunca uma caixa com borda tracejada.
- **Transição em fade (opção em avaliação):** o card pode surgir só com fade de opacidade (calmo p/ pré), em vez do deslize `translateY`. Sugestão do Claude, ainda NÃO é regra fixa — confirmar com a prof antes de adotar em todas.
