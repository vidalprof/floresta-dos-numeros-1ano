# 💡 PESQUISA — Formatos de aprendizagem REAL, MENSURÁVEL e BARATA DE ARTE (2026-07)

> Contexto: o RPG 2D deu MUITO trabalho de arte (cenário colado, árvores cortadas, bug atrás
> de bug). O Marcos quer manter aprendizagem **real + mensurada + alinhada ao currículo dele**
> e que a criança **AME** — mas sem depender de arte cara. Este ano = **currículo normal**
> (computação/pensamento computacional ficou pra depois, ver `PESQUISA-PENSAMENTO-COMPUTACIONAL`).
> Pergunta que abriu a pesquisa: *micro-mundos, simulações e explicações manipuláveis — como
> fazer isso ser ATRATIVO pras crianças?* A resposta curta está na seção "COMO DEIXAR ATRATIVO".

---

## A TESE (o que a evidência sustenta)
**O que faz uma atividade digital ENSINAR de verdade é o DESIGN da interação e do feedback,
não o capricho gráfico.** Meta-análises grandes mostram que jogos/sims com **arte esquemática**
(formas simples, símbolos, texto, emoji) ensinam **igual ou MAIS** que os de arte "bonita".
Ou seja: é exatamente o caminho de um professor + IA num PC fraco. E — a virada de chave pro
medo do Marcos — **o que faz a criança AMAR é a MESMA coisa que faz ela aprender**: ela mexer e
o mundo responder na hora. O gráfico nunca foi o que prendia; a responsividade era.

Peso da evidência marcado: **[FORTE]** meta-análise/RCT · **[MODERADA]** estudos individuais ·
**[CONSENSO]** teoria influente sem prova causal robusta.

---

## COMO DEIXAR ATRATIVO (o coração da pergunta do Marcos) — 6 alavancas baratas
Uma simulação "pelada" (só slider + gráfico) realmente **não** encanta criança de 6–12. O que
encanta não é arte — são estas 6 alavancas, TODAS baratas e que **a gente já construiu no motor
do RPG** (juice, Byte, voz do Antônio, celebração). Basta mover o esforço do cenário pra cá.

1. **Resposta na hora (game feel / "gostosura").** Mexeu → o mundo reage GRANDE, com som e
   exagero (squash&stretch, brilho, partícula). É o `juice()` que já temos. É isto que
   transforma um slider de formulário num BRINQUEDO. (Swink *Game Feel*; Vlambeer "juice".)
2. **Um OBJETIVO claro + "o mundo PRECISA de você".** Sandbox vazio entedia; a criança quer uma
   MISSÃO: "faça a carroça passar", "mantenha o peixe feliz", "atenda o cliente". Problema
   primeiro = a LEI do EduVerse **e** o que vira jogo em vez de enfeite. [FORTE: Kapur; Wouters]
3. **Surpresa / "o que acontece se eu exagerar?".** Deixe quebrar de propósito e rir (a planta
   se afoga, o peixe fica gordo e engraçado, o enxame faz algo inesperado). Exagero é de graça
   e é o que prende a atenção (curiosidade — Malone & Lepper).
4. **Um personagem que SENTE + você ENSINA ele (efeito protégé).** O Byte fica feliz/confuso
   conforme a criança acerta. Dá emoção sem arte nova e **ajuda MAIS quem está atrás**. [FORTE
   no esforço — Chase 2009] Casa com "o Byte pergunta, não responde".
5. **"Eu que fiz!" — modo criar e mostrar.** Botão que gera link/QR do que a criança montou (ou
   do desafio que ela criou pro colega). Autoria = orgulho = motivação (construcionismo; Resnick
   4 P's). Arte ≈ 0 porque a arte vira OUTPUT da criança.
6. **Progressão e descoberta.** Destrava lugares/regras novas; "você descobriu a regra secreta"
   vira detetive. Mistério + progresso visível é motor de retorno.

**Resumo:** micro-mundo (barato de construir, aprendizado forte) **+** esta camada de
game-feel/objetivo/personagem/autoria (barata, é o que faz amar) = o melhor dos dois mundos,
SEM o cenário caro que causou todos os bugs.

---

## 1. Simulações / micro-mundos / sandboxes
- **PhET: uma das maiores bases de evidência da edtech. [FORTE]** Meta-análise de 31 estudos
  (2011–2020): efeito **grande, d = 0,83** vs. ensino tradicional; base global de **13.000+
  estudos**. Fundada por Carl Wieman (Nobel de Física). Uma sim PhET é literalmente **formas +
  sliders + regras** — quase zero arte; replicável em canvas/SVG puro, 1 HTML, PC fraco.
- **O segredo é "implicit scaffolding", não gráfico. [MODERADA/CONSENSO]** O design guia o aluno
  por caminhos úteis **sem instruir**: a ordem de interação leva à descoberta, com feedback
  imediato a cada toque. É o manual a copiar (monte a tela pra descoberta emergir). Casa c/ Portão 0.
- **Simulação/laboratório virtual: efeito robusto. [FORTE]** g = 0,85 no superior (Chernikova
  2020); labs virtuais g ≈ 0,59; **scaffolding aumenta o efeito**. Pra 6–12: tanque de misturar
  cor, balança de 2 pratos, circuito com 1 lâmpada — tudo em `<div>`/canvas.
- **NetLogo / agentes "pontinhos + 1 regra": micro→macro. [MODERADA]** Regras simples de muitos
  agentes idênticos geram padrão complexo (formiga na trilha, vírus que espalha, cardume). Cada
  agente = 1 círculo de 4px. MENOR arte, MAIOR impacto conceitual de sistema. (Wilensky/CCL.)
- **Micro-mundo de Papert. [CONSENSO]** Recorte UM conceito, dê UM conjunto de regras
  manipuláveis, deixe explorar. É o gabarito de toda atividade EduVerse.

## 2. Construcionismo / ferramentas de CRIAÇÃO
- **Construcionismo (Papert). [CONSENSO influente]** Aprende-se construindo um artefato público
  ("objects to think with"). Vire o RPG de cabeça pra baixo: a criança **produz** a arte (vira
  output dela), não consome a sua. Padrão, música, mosaico, história — arte ≈ 0, autoria alta.
- **Efeito protégé: ensinar um agente faz esforçar MAIS. [FORTE no esforço]** "Betty's Brain"
  (Chase 2009): quem **ensina** um agente lê mais, aprende mais, corrige mais — **efeito maior
  nos alunos de menor desempenho**. Enquadre como **"ensine o Byte"**: a criança arrasta peças
  pra "explicar", o Byte age e erra visível se o ensino estava errado. Zero arte nova.
- **Scratch: ganho consistente em pensamento computacional. [MODERADA/FORTE]** (revisão de 55
  estudos). Não precisa embutir; copie o **princípio de autoria por blocos/arrasto**.
- **Twine / ficção interativa. [CONSENSO/MODERADA]** "Escolha sua aventura" = texto + botões,
  arte zero; mede-se pelos caminhos escolhidos (já é dado stealth). Bom pra humanas/ciências.
- **Teachable Machine / Quick Draw. [MODERADA]** A criança TREINA o próprio modelo de IA no
  navegador em ~15 min — "uau" alto, arte ≈ 0, mensurável (acurácia). (Letramento de IA.)

## 3. Explorable explanations (texto manipulável)
- **Bret Victor. [CONSENSO seminal]** Simulação interativa + prosa que orienta; o leitor testa
  expectativas contra o comportamento real → leitura ATIVA. Um número que vira **slider** e o
  gráfico/frase muda ao vivo. HTML+JS+SVG, sem assets. "Muito conceito por pouco código".
- **Nicky Case / "Parable of the Polygons". [CONSENSO, alto impacto]** Ensina sistema difícil
  (segregação de Schelling) com **formas + carinhas**. Prova viva de "emoji + regra" ensinando
  ideia difícil — o estilo barato que a gente já domina.
- **Ecossistema pronto pra "roubar" padrão. [RECURSO]** Hub Explorable Explanations + lista
  "awesome-explorables": dezenas de exemplos abertos com código. Peça à IA "adapte este de
  fração/probabilidade pro meu conteúdo BNCC" — parte de molde testado.
- **Ressalva honesta. [OPINIÃO]** Interatividade **não garante** aprendizado: **cada coisa que a
  criança mexe precisa mudar algo que EXPÕE o conceito-alvo** — senão é enfeite (Portão de Arte).

## 4. Stealth assessment / analytics — O DIFERENCIAL DO PROFESSOR
- **Medir SEM parecer prova (Shute). [MODERADA, arcabouço sólido]** A criança joga; o professor
  recebe a medida. É a resposta técnica ao mandamento "nunca é prova disfarçada".
- **Como funciona: Evidence-Centered Design, 3 modelos. [CONSENSO metodológico]** (1) competência
  (o que medir: ex. "compõe/decompõe números até 20"); (2) evidência (que ações contam como
  prova); (3) tarefa (situações que forçam essas ações). Escreva as 3 listas ANTES de codar → cada
  clique já nasce etiquetado como evidência de uma habilidade da BNCC. É planilha, não arte.
- **Já validado medindo coisa difícil. [MODERADA]** Persistência e criatividade (Physics
  Playground) bateram com indicadores tradicionais. Dá pra medir **persistência** (tentativas
  antes de desistir), **estratégia** (caminho) e **autocorreção** — o que enche um parecer.
- **Dashboard pro professor. [MODERADA]** O mesmo 1 HTML grava as jogadas (localStorage/Firebase
  que já usamos na Agenda) e cospe resumo por criança/turma. **É o produto que ninguém dá de
  graça na escola pública.**
- **Ressalva honesta. [EMERGENTE]** Estimador bayesiano válido é difícil e exige dados. Comece
  simples: contadores etiquetados + regra clara ("4/5 sem dica = provável domínio") → parecer
  descritivo confiável. Bayes é evolução, não pré-requisito. **Não prometer "nota oficial" de cara.**

## 5. "INCRÍVEL ≠ CARO" — a evidência
- **Clark et al. (2016), a meta-análise-chave: DESIGN vence GRÁFICO. [FORTE]** 57–69 estudos
  K–16. Jogo vs. não-jogo: **d ≈ 0,33**. E o achado decisivo: **arte esquemática (formas/símbolos)
  foi MAIS eficaz que "cartoon"/realista**. O que move o ponteiro é **valor agregado** (feedback,
  andaime, personalização). É a licença científica pra largar o RPG 2D caro.
- **Wouters et al. (2013). [FORTE]** 77 estudos: aprendizagem d = 0,29, retenção d = 0,36. Melhor
  **complementado por instrução, em várias sessões**. Honestidade: **não** foi mais motivador que o
  convencional (n.s.) → não vender "mágica de motivação"; vender **aprendizagem e retenção medíveis**.
- **Mayer (multimídia). [FORTE]** Coerência: detalhe visual a mais **atrapalha**. Feedback é
  indispensável. Tela limpa, uma ideia por vez, feedback imediato > cenário rico. Forte em
  **transferência**, não em decorar — meça isso.
- **Prática de recuperação (testing effect): a evidência MAIS forte, arte ZERO. [FORTE]** g ≈
  0,50–0,61; funciona no fundamental; maior **com feedback**. Uma boa pergunta + feedback +
  repetição espaçada. Barato de construir, forte de efeito, trivial de medir.
- **Autoexplicação. [MODERADA]** "Por que você acha que deu certo?" (com opções/lacuna) agrega
  aprendizado + vira evidência. Ressalva: evidência de sala/longo prazo mais fraca que em lab.
- **Falha produtiva (Kapur): problema PRIMEIRO. [FORTE]** Tentar antes de ensinar → mais
  compreensão e transferência (**d ≈ 0,36**). É **exatamente** a LEI do EduVerse, com RCT por trás.

## 6. Exemplos reais (alto impacto, baixa arte)
- **DragonBox Algebra. [MODERADA + RESSALVA]** Intuição algébrica em ~42 min com ícones simples.
  **MAS não transfere sozinho pra notação formal — exige andaime do professor.** Lição: planeje a
  PONTE pro formal (o jogo cria a intuição; uma fase final/o professor faz a transferência explícita).
- **Desmos & GeoGebra. [MODERADA]** "Arraste o ponto e veja a fórmula mudar" = explorable de novo;
  replicável em SVG pra frações, área, simetria (6–12).
- **PhET & Scratch. [FORTE/MODERADA]** Os dois maiores casos de edtech aberta usam **formas +
  regras** e **blocos + criação** — nenhum depende de arte cara. Prova de escala do caminho.
- **Professor + IA como fábrica de sims sob medida. [EMERGENTE]** "Instructors as Innovators"
  (Mollick 2024): a IA democratiza a criação de ferramentas pelo próprio professor. Confirma que a
  dupla professor+IA é o arranjo certo: a IA não precisa desenhar — precisa **codar o micro-mundo +
  o stealth assessment** em 1 HTML. É onde a gente já é forte.

---

## EXEMPLOS CONCRETOS pro currículo NORMAL (esboço, pra conversar — não construído ainda)
- **Frações — A Sorveteria / A Pizzaria do Byte.** O cliente pede "metade", "um terço"; a criança
  fatia/monta a bola; o cliente sorri ou faz careta NA HORA. Fila de clientes engraçados, cada um
  quer uma fração; fica mais rápido. (Objetivo + surpresa + personagem que sente.)
- **Ciências — O Aquário / A Horta.** Sliders de sol, água, comida; a plantinha/peixe reage ao
  vivo (murcha, cresce, fica feliz). É um bicho de estimação que a criança mantém vivo (energia
  Tamagotchi); exagerar afoga a planta e é engraçado. (Causa-efeito + "o mundo precisa de você".)
- **Sistemas — Espalha a Alegria / O Cardume.** Pontinhos + 1 regra; a criança muda a regra e vê o
  enxame fazer algo que ela não previu. Vira "deusa" do mundinho. (Emergência com arte mínima.)
- **Números / composição — A Máquina de Números.** Monta uma máquina, alimenta números, vê a
  saída; descobre a regra secreta. (Construcionismo + descoberta.)
Em TODOS, por baixo: stealth assessment etiquetado por habilidade BNCC → parecer/nota (o diferencial).

---

## FONTES (URLs)
**Simulações/micro-mundos:** PhET meta (d=0,83) https://online-journals.org/index.php/i-joe/article/view/59007
· PhET pesquisa https://phet.colorado.edu/en/research · implicit scaffolding https://arxiv.org/pdf/1306.6544
· simulação superior (g=0,85) https://journals.sagepub.com/doi/10.3102/0034654320933544 · labs virtuais
https://www.ijiet.org/vol12/1598-IJIET-3079.pdf · NetLogo https://ccl.northwestern.edu/papers/MEE/
**Construcionismo/criação:** Papert http://www.papert.org/articles/SituatingConstructionism.html · efeito
protégé https://link.springer.com/article/10.1007/s10956-009-9180-4 · Scratch (55 estudos)
https://www.sciencedirect.com/science/article/abs/pii/S0360131519301605 · Twine
https://programminghistorian.org/en/lessons/interactive-text-games-using-twine · Teachable Machine
https://www.kidsaitools.com/en/articles/google-ai-tools-for-kids
**Explorable explanations:** Bret Victor https://worrydream.com/ExplorableExplanations/ · verbete
https://en.wikipedia.org/wiki/Explorable_explanation · Parable of the Polygons https://ncase.me/polygons/
· awesome-explorables https://github.com/blob42/awesome-explorables
**Stealth assessment/analytics:** Shute (MIT Press, OA) https://direct.mit.edu/books/oa-monograph/3700/ ·
ECD (cap.) https://files.eric.ed.gov/fulltext/ED612156.pdf · Physics Playground
https://link.springer.com/article/10.1007/s40593-020-00196-1 · dashboard K-12
https://dl.acm.org/doi/fullHtml/10.1145/3631700.3665228
**Incrível ≠ caro:** Clark 2016 https://journals.sagepub.com/doi/full/10.3102/0034654315582065 · Wouters
2013 https://eric.ed.gov/?id=EJ1008015 · Mayer https://www.sciencedirect.com/science/article/pii/S1747938X25000673
· prática de recuperação https://www.nature.com/articles/s44159-022-00089-1 · falha produtiva (Kapur)
https://journals.sagepub.com/doi/10.3102/00346543211019105
**Exemplos:** DragonBox (crítica de transferência) https://repository.isls.org/bitstream/1/10064/1/ICLS2023_1873-1874.pdf
· Desmos/GeoGebra https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12645096/ · Quick Draw
https://quickdraw.withgoogle.com/ · Instructors as Innovators (Mollick 2024) https://arxiv.org/pdf/2407.05181
