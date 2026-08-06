# 🧠 REGRAS DE MONTAGEM — neurociência do aprendizado, som e encantamento

> Destilado de `PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`, `PRINCIPIOS-ENCANTAMENTO.md`,
> `PESQUISA-SOM-E-GAMEFEEL-2026-07.md`, `PESQUISA-DUOLINGO-AMBIENTE-2026-07.md` e
> `PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`.
>
> **Não é resumo: é a lista de decisões que eu tomo ENQUANTO monto.** Se um item não muda
> uma linha de HTML/CSS/JS, ele não está aqui. Onde a pesquisa não dá número, está escrito
> "sem número na pesquisa" e a regra vira ORDEM (o que vem antes do quê) — nunca invento
> milissegundo.

---

## A — OS PRIMEIROS SEGUNDOS (abrir a lacuna)

- **Como abro a lacuna de curiosidade?**
  Ordem fixa e não negociável: **problema → curiosidade → conceito por ÚLTIMO**. A abertura
  mostra uma falta concreta ("o baú está trancado — qual número abre?"), nunca a explicação.
  A curiosidade precisa estar aberta ANTES do passo-chave: é ela que abre a janela de memória
  do hipocampo. `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Quanto tempo até a criança AGIR pela primeira vez?**
  Sem número na pesquisa — a regra é ordinal e mais dura: **nenhuma tela só-de-leitura antes
  da primeira ação**. Novidade só liga o modo-aprender se exigir AÇÃO; texto/vídeo passivo não
  conta. Na prática: a primeira tela já tem algo para tocar ou arrastar, e o enunciado é falado
  por cima da figura. `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Como escolho a mecânica de cada fase?**
  Pelo **conceito que o gesto evoca**, não pela aparência: tocar = cardinalidade/contagem;
  arrastar = agrupar/parte-todo; girar = propriedade geométrica; traçar contínuo = grandeza
  contínua/reta numérica; deslizar = variação/proporção. Mecânica fora dessa matriz é enfeite,
  mesmo que divirta. `→ fonte: PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`

- **Clicar na alternativa certa ou arrastar até ficar certo?**
  **Arrastar**, sempre que couber: cognição corporificada ajuda memória (forte em matemática) e
  a trajetória do arraste é o que vira evidência de domínio. Múltipla escolha é o último
  recurso, não o padrão. `→ fonte: PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`

- **Onde termina a atividade?**
  **No símbolo, na MESMA atividade.** Concreto → figural → símbolo: é a concretude que
  desvanece, e é ela que dá TRANSFERÊNCIA. Sem a camada 3 acontece o "efeito DragonBox": a
  criança fica ótima no app e não leva nada para o caderno. No 8º ano, com azulejos algébricos
  (730 alunos), CPA subiu desempenho E motivação E baixou ansiedade.
  `→ fonte: PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`

---

## B — O LOOP (acerto, erro, gesto, som)

- **Que som para acerto, erro e passo — exatamente?**
  Acerto = **tríade maior que resolve**, 523,25 / 659,25 / 783,99 Hz, ~0,35 s, `triangle`,
  vol 0,18, 55 ms entre as notas. Erro = **dissonância curta e gentil**: 300 Hz + 318 Hz por
  **140 ms**, `sine`, vol ≤ 0,14 — nunca estridente. Passo/pegar = clique de **12 ms**. Contar
  = pitch sobe por unidade (`220 * 2^(k/12)`, um a cada 180 ms).
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **MP3 ou Web Audio?**
  **Regra dura: "ding" = Web Audio sintetizado; narração = MP3.** Feedback de acerto/erro/toque
  tem que caber em < 100 ms; MP3 para o "ding" chega atrasado e mata a sensação de causa-efeito.
  Todo oscilador leva envelope de **12–15 ms** de ataque e decaimento exponencial, senão estala.
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **O som de acerto pode ser sempre o mesmo?**
  **Não.** Varie pitch/timbre e, de vez em quando (não sempre), solte um brilho extra: é a
  surpresa que dispara o erro-de-previsão de recompensa e fixa memória. Previsível 100% = o
  cérebro para de responder. `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Posso dar estrelinha em toda ação certa?**
  **Não — isso corrói a motivação.** Overjustification: quem ganhou prêmio por desenhar passou a
  desenhar METADE, e o efeito é pior em criança. A recompensa tem que ser **parcimoniosa,
  informativa e ligada ao conteúdo** (celebra o que ela ENTENDEU), nunca o motivo de continuar.
  `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **O que o erro faz na tela?**
  Volta com **mola + shake de 2–3 px** + dissonância de 140 ms, e o texto traz **pista
  acionável** ("conte de novo começando pelo maior"), nunca só "errado" — cerca de **1/3 dos
  feedbacks chega a PREJUDICAR** quando é só resultado. Nada de game-over, vida perdida ou som
  punitivo; o elogio é ao PROCESSO ("você tentou outro jeito"), não à pessoa ("você é esperto").
  `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Como faço o arraste "sentir bem"?**
  Gruda no dedo sem atraso, **squash 1.15 / 0.88** ao pegar, sombra cresce durante o arraste,
  assenta com mola + **3 a 5 partículas** no alvo certo, e **hit-stop de ~50 ms** no impacto (a
  micro-pausa é o que dá "peso"). **Silêncio durante o arraste** — arrastar é raciocínio.
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **Posso animar largura, top, sombra, cor?**
  **Não: só `transform` e `opacity`.** O resto dispara reflow/repaint e trava o PC da escola.
  Todo o juice sai de scale/translate/opacity — e tudo dentro de
  `@media (prefers-reduced-motion: reduce)`, que zera screenshake, escalas grandes e partículas.
  `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **O som pode ser o único canal de alguma informação?**
  **Nunca.** Todo evento sonoro tem gêmeo visual, a narração tem legenda curta sincronizada,
  alvos ≥ **44 × 44 px**, e a atividade tem que ser 100% jogável no mudo (PC de escola sem caixa
  de som existe). Vibração é bônus de Android — iOS nunca teve, Firefox tirou.
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **Por que o som não toca na primeira tela?**
  Não é bug: autoplay é travado até o 1º gesto. Um único `AudioContext`, criado/retomado
  **dentro** do gesto (`if(AC.state==='suspended') AC.resume()`), destravado no `pointerdown`
  global — e o botão **"Ouvir" é o start 100% garantido** (mover o mouse às vezes não conta).
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

---

## C — O QUE CANSA O CÉREBRO DELA (o que eu APAGO da tela)

- **Quantos segundos de comemoração antes de virar enfeite?**
  Sem número na pesquisa — o corte é **por MOMENTO, não por relógio**: juice antes (curiosidade)
  e depois (comemorar), **nunca sobreposto ao passo de pensar**. Durante o raciocínio a tela
  fica limpa; decoração a mais atrapalha o aprendizado em **23 de 23 testes, d = 0,86**. Na
  prática: nada de animação em loop, brilho correndo ou mascote dançando enquanto o enunciado
  está de pé esperando resposta. `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Posso deixar musiquinha de fundo enquanto ela pensa?**
  **Não.** Som de fundo que MUDA de estado atrapalha memória de sequência (efeito de som
  irrelevante, às vezes pior em crianças), e som "interessante mas inútil" impõe carga.
  **Silêncio durante o raciocínio; som rico NO evento** — ação, acerto, erro, transição.
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **Texto na tela ou voz?**
  **Voz falada por cima da figura**, texto só como legenda curta: narração + animação vence
  narração + texto com **d ≈ 1,02**, porque o canal visual não fica sobrecarregado. E a voz é
  MP3 neural conversacional ("vamos ver quantas faltam?") — estilo conversacional venceu **11 de
  11 testes, d = 1,11**; o `speechSynthesis` do navegador é o pior caso e ainda varia de PC para
  PC. `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **O que eu NÃO escrevo, mesmo que dê engajamento?**
  Sem vida/energia/moeda que transforme o conteúdo em pedágio (anti-Prodigy: a matemática vira o
  preço de voltar a brincar), sem streak que pune, sem notificação que culpa, sem loja. E nada
  de trilha por "estilo de aprendizagem" (visual/auditivo/cinestésico é neuromito) — multimídia
  para TODOS, imagem + voz + ação. `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

---

## D — COMO FAÇO A CRIANÇA QUERER A PRÓXIMA TELA

- **Como fecho uma fase?**
  **Celebração + isca da seguinte** (Zeigarnik): concluir dá prazer, e o gancho leve é o que
  puxa de volta. Fase que só diz "parabéns, próxima" desperdiça o único momento em que ela está
  disposta a querer mais. Cada fase precisa carregar **um elemento que quebra o padrão** — um
  bicho que aparece, um segredo, uma reviravolta. `→ fonte: PRINCIPIOS-ENCANTAMENTO.md`

- **Como a criança sabe para onde ir?**
  **Um próximo passo óbvio e único**: trilha linear que serpenteia, **um nó = um nível**,
  agrupada em unidades, e três estados visuais claros (feito/colorido · atual/pulsando ·
  bloqueado/cinza). No nó atual, **bolha "COMEÇAR" saltitante + anel pulsante** — não só um
  rótulo. `→ fonte: PESQUISA-DUOLINGO-AMBIENTE-2026-07.md`

- **O que fica no topo durante a fase?**
  **Barra de progresso fina que enche e PULSA a cada acerto.** E o par **VERIFICAR → CONTINUA**
  padronizado: uma ação por vez, verde para certo, vermelho para erro, sem poluição. Botão
  sempre 3D e apertável (`box-shadow:0 4px 0 <escuro>` + `translateY` ao apertar), e **nenhum
  canto reto na tela inteira**. `→ fonte: PESQUISA-DUOLINGO-AMBIENTE-2026-07.md`

- **A dificuldade sobe como?**
  **Acertou 3 → sobe; errou 2 → desce**, e entre os blocos entra uma **micro-pausa de reflexão**
  ("por que deu certo?", com o mascote PERGUNTANDO). Flow contínuo encanta mas retém menos que
  flow interrompido por reflexão — a pausa não é perda de ritmo, é o que fixa.
  `→ fonte: PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`

- **Quando o mascote oferece ajuda?**
  Quando **a hesitação for alta E houver 2+ erros** — e o que ele faz é **PERGUNTAR** algo que
  reencaminha, não entregar a resposta. Tempo sozinho não é sinal de fraqueza (aluno bom às
  vezes vai devagar de propósito): o relógio serve para decidir o andaime, nunca para virar nota.
  `→ fonte: PESQUISA-SOM-E-GAMEFEEL-2026-07.md`

- **Duas fases seguidas podem usar a mesma mecânica?**
  **Não.** A regra de variedade é **sequencial**: o roteiro não repete a mesma mecânica em fases
  vizinhas. Repetição vizinha é o que faz a criança sentir "é a mesma tela pela terceira vez"
  mesmo quando o conteúdo mudou. `→ fonte: PRINCIPIOS-ENCANTAMENTO.md`

- **O que muda conforme o ano?**
  **Pré (4–5):** voz no lugar de texto, alvo enorme brilhando, causa-efeito imediata.
  **1º–2º:** número grande subindo + som ascendente, micro-escolha, selo de "consegui!".
  **3º–5º:** micro-desafio ("quantos faltam?"), segredos que premiam curiosidade, coleção de
  longo prazo. **6º–9º:** stakes reais, o conteúdo como OBSTÁCULO, trade-off, estética menos
  fofa — desafio genuíno é o respeito que essa idade cobra.
  `→ fonte: PRINCIPIOS-ENCANTAMENTO.md`

---

## E — MEDIR SEM PROVAR (o que eu registro por baixo)

- **O que eu gravo enquanto ela joga?**
  Quatro observáveis por fase: **hesitação (ms até a 1ª ação)**, **tentativas até o acerto**,
  **pediu dica (s/n)** e **acertou o item da camada simbólica**. A própria jogada é a evidência
  — não existe prova separada, e nada disso vira nota na tela da criança: vira parecer descritivo
  por habilidade. `→ fonte: PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`

- **Vale mostrar esse modelo para a própria criança?**
  Sim — é a lacuna do mercado: quase todo mundo gamifica quiz (efeito grande, **g = 0,822**, mas
  muito dependente do desenho) e mede pouca competência real. Devolver o progresso por habilidade
  de forma legível ativa metacognição. **Ressalva honesta:** o Open Learner Model está no corpus
  *sem achado verificado* — usar como aposta de design, não como promessa.
  `→ fonte: PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`

---

## 🤖 O QUE DÁ PARA MEDIR SOZINHO — a fila de portões novos

Cada item abaixo é um portão que ainda NÃO existe em `_qa/`. Estão em ordem de
custo/benefício: os de cima pegam defeito que já chegou perto da criança.

| # | O que mediria | Como |
|---|---|---|
| 1 | Som de acerto/erro é Web Audio, não MP3 | `createOscillator` dentro das funções de acerto/erro; reprovar se for só `new Audio()` |
| 2 | Envelope anti-clique | todo `createGain` de oscilador com `exponentialRampToValueAtTime`, ataque 0,010–0,020 s; reprovar `gain.value=` direto |
| 3 | O erro é gentil | duração do som de erro ≤ 0,25 s e volume ≤ o do acerto |
| 4 | Comemoração invadindo o pensar | `animation:` com `infinite` em elemento que coexiste com enunciado/opções |
| 5 | Só `transform`/`opacity` animados | parsear `@keyframes`/`transition:`; reprovar `width`, `top`, `left`, `box-shadow` |
| 6 | Existe `prefers-reduced-motion` | grep + conferir que zera shake/pop/confete |
| 7 | Feedback com gêmeo visual | toda chamada de som de acerto/erro tem mudança de classe na mesma função |
| 8 | Mesma mecânica em fases VIZINHAS | `_qa/padrao.py` já conta gesto por fase; falta a regra sequencial |
| 9 | Áudio destrava no gesto | `AudioContext` + `resume()` dentro de handler de `pointerdown`/`click` |
| 10 | Primeira interação nas 2 primeiras telas | tela de leitura pura na abertura reprova |
| 11 | O conceito vem por último | tela de conceito/definição antes da primeira tela de problema reprova |
| 12 | A camada simbólica existe | última fase usa representação simbólica, não figural |
| 13 | Recompensa parcimoniosa | recompensa em ≥ 90% das ações certas = aviso (overjustification) |
| 14 | Som de acerto sempre idêntico | acerto 100% determinístico = aviso |
| 15 | Observáveis do stealth gravados | as 4 chaves (hesitação, tentativas, dica, simbólico) no log |

**Primeiros dois a construir:** `_qa/gamefeel.py` (itens 1–5, 7, 14) e
`_qa/curiosidade.py` (itens 10–12).
