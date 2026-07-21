# Pesquisa — Adequação por faixa etária, leque de mecânicas interativas e o diferencial inovador

**Data:** 2026-07-21
**Para:** professor Marcos
**Escopo:** app educativo web LEVE (HTML/CSS/JS, roda em PC fraco e navegador antigo de
escola pública), do PRÉ ao 9º ano. Base do que este relatório recomenda: aprendizagem
adaptativa (BKT/domínio por conceito), revisão espaçada (Leitner), autoexplicação,
feedback formativo de tarefa, cognição incorporada (gestos), avaliação *stealth* e
produção-não-reconhecimento.

## Como ler este relatório (honestidade sobre a base de evidências)

Este relatório foi montado **somente** com o material recuperado da pesquisa (29
conclusões extraídas de fontes + 75 vereditos de verificação adversarial + 28 fontes).
Não inventei citações nem números.

Uma observação de método, para o senhor confiar no que está escrito: a verificação
adversarial **confirmou** a grande maioria das conclusões, mas **refutou/corrigiu quatro**
— e essas correções são justamente sobre o app "My Math Academy" e sobre a "revisão
espaçada como brincadeira". Preservei essas correções em vez de esconder, porque elas
mudam o que devemos afirmar. Além disso, várias fontes importantes para o **Bloco 1**
(Nielsen Norman Group por faixa etária, Self-Determination Theory de Ryan & Deci, teoria
da carga cognitiva, "dificuldades desejáveis" de Bjork, Open Learner Model) aparecem na
**lista de fontes** da pesquisa, mas **sem uma conclusão verbatim extraída e verificada**.
Onde é esse o caso, eu digo explicitamente "a pesquisa recuperada traz a fonte mas não
extraiu um achado específico dela" — e não coloco números na boca de ninguém.

Marcação de confiança usada abaixo: **[ALTA]** = veredito confirmado com confiança alta;
**[MÉDIA]** = confirmado com confiança média; **[RESSALVA]** = a verificação refutou ou
corrigiu parte da afirmação (explico o quê).

---

# BLOCO 1 — ADEQUAÇÃO POR FAIXA ETÁRIA

As três faixas do app: **Pré / 1º / 2º (~4–8 anos)**, **3º–5º (~8–11)**, **6º–9º (~11–15)**.

> **Aviso de cobertura.** As conclusões *verificadas* da pesquisa são fortes em
> **pedagogia da matemática e mecânicas de interação**, e mais fracas em "UX por idade"
> propriamente dito. As referências centrais de desenvolvimento e de interface por faixa
> — **Nielsen Norman Group** ("Design for Kids Based on Their Stage of Physical
> Development"; "UX Design for Children Ages 3–12"; "UX Design for Teenagers Ages 13–17")
> e **Ryan & Deci / Self-Determination Theory** — estão na lista de fontes da pesquisa,
> mas **não vieram com um achado verbatim verificado**. Cito-as como referências presentes
> no corpus; não atribuo a elas números que não foram recuperados. **A pesquisa recuperada
> não cobre com achado verificado:** os estágios de Piaget, a Zona de Desenvolvimento
> Proximal de Vygotsky, nem recomendações granulares de tamanho de alvo/toque por idade.

## 1.1 Pré / 1º / 2º (~4–8 anos) — "o mundo se toca com o dedo"

**O que a evidência verificada sustenta:**

- **Interação incorporada pelo dedo (finger-multitouch) é uma linha de design legítima
  para os pequenos — mas o app sozinho NÃO é automaticamente melhor que a atividade
  desplugada.** Um app de matemática inicial foi desenhado a partir da *cognição
  incorporada*, com jogos de contagem nos dedos e representação de magnitude cardinal e
  relações parte-todo para crianças da educação infantil (jardim). **[ALTA]** Porém, num
  estudo pré-pós com dois grupos de controle, a intervenção curta com o app **não melhorou
  significativamente** as habilidades matemáticas das crianças em comparação com um
  treino desplugado de conteúdo equivalente nem com um grupo de espera. **[ALTA]** Os
  autores atribuem o resultado nulo a fatores metodológicos e curriculares — ou seja,
  entregar conteúdo incorporado "por app" não é, por si só, superior à instrução
  desplugada na primeira infância.
  *Fonte: "Design and empirical evaluation of a multitouch interaction game-like app for
  fostering early embodied math learning", ScienceDirect S1071581923000368 (Ninaus/Barrocas
  et al., Int. J. Human-Computer Studies, 2023).*
  **Lição de design para nós:** nesta faixa, o gesto (contar/arrastar com o dedo) é o
  meio certo, mas o **valor vem do desenho curricular**, não do fato de ser digital. Não
  prometer ganho só porque "virou joguinho".

- **Adaptatividade produz ganho mensurável em K–1 (~5–7 anos).** Num estudo com jardim e
  1ª série (N≈505 tratamento / 481 controle), crianças usando um app adaptativo de
  matemática ("My Math Academy") tiveram **ganhos significativos** frente a quem não usou.
  **[MÉDIA]** O app combina conteúdo personalizado com **avaliação embutida/adaptativa**
  (abordagem *stealth*), que é apresentada como o mecanismo que permite personalizar
  dentro do currículo existente. **[ALTA]**
  *Fonte: "Efficacy of an Adaptive Game-Based Math Learning App…", Springer
  10.1007/s10643-022-01332-3 (Early Childhood Education Journal, 2023).*
  **[RESSALVA importante — a verificação corrigiu dois pontos que costumam ser mal citados]:**
  (1) esse estudo específico de 505/481 é uma **comparação pareada/quase-experimental**,
  **não** um "estudo randomizado"; o verdadeiro ECR de "My Math Academy" é um **artigo
  separado** (Thai, Bang & Li, 2022, *Journal of Research on Educational Effectiveness*),
  que é o que recebeu selo "Strong Evidence" da ESSA. (2) O maior efeito **não** foi nos
  alunos de conhecimento prévio **mais baixo**, e sim nos do **terço médio** de
  conhecimento prévio (tamanho de efeito 0,46) — mais os "conteúdos mais difíceis". Não
  devemos repetir a versão inflada ("app randomizado, melhor para os mais fracos").

- **Revisão espaçada / recuperação pode entrar como BRINCADEIRA, não como quiz.** Para os
  pequenos, reformular a recuperação como jogo (ex.: "esconde-esconde" — o conhecimento
  está "escondido no cérebro" e precisa ser "achado") cria o ambiente de **baixo risco**.
  Jogos matemáticos propositais (ex.: "Que forma eu sou?") funcionam como recuperação
  genuína, puxando o vocabulário (polígono, vértices) e as propriedades. **[ALTA para a
  descrição do mecanismo de jogo]**
  *Fonte: "Retrieval practice: a game of 'hide and seek'", Education Endowment Foundation.*
  **[RESSALVA]:** a verificação **refutou** a versão forte "baixo risco torna a
  recuperação MAIS eficaz cognitivamente". A EEF é um **blog/artigo de prática
  (secundário)**, e a literatura primária (Roediger, Karpicke, Agarwal) mostra que a
  recuperação é robusta **em vários níveis de risco**; o benefício do baixo risco é
  **reduzir ansiedade e tornar sustentável**, não aumentar a potência do aprendizado.
  Então, para nós: usar o formato lúdico pela **redução de ansiedade** (o que é
  perfeitamente adequado à faixa), sem prometer ganho cognitivo extra por ser "leve".

**Síntese da faixa:** gesto/dedo como linguagem principal; adaptatividade dá ganho real
mas modesto; recuperação disfarçada de brincadeira serve para clima e afeto. Recompensa e
autonomia por faixa: a pesquisa recuperada **não** traz achado NNGroup/SDT específico
para esta idade — apenas as fontes.

## 1.2 3º–5º ano (~8–11 anos) — "faz sozinho, com apoio que mede"

**O que a evidência verificada sustenta:**

- **Mecânicas incorporadas de toque (tocar/arrastar/girar) sustentam a construção de
  significado matemático nesta faixa escolar (K-12).** Uma revisão sistemática (Web of
  Science, 2010–2023, 34 estudos empíricos) propõe uma **"matriz de ações de toque"**,
  ligando cada ação física (tocar, arrastar, traçar, girar) ao **significado matemático**
  que ela evoca. Gestos como tocar, arrastar e girar apoiam a aprendizagem incorporada ao
  **coordenar ação e percepção**. **[ALTA]**
  *Fonte: "Characterizing touchscreen actions in technology-enhanced embodied learning for
  mathematics… A systematic review (2010–2023)", Computers & Education / ScienceDirect
  S0360131523001586 (Yeung & Ng, 2023).* Corroborada por Duijzer/Abrahamson et al.,
  "Touchscreen Tablets: Coordinating Action and Perception…" (PMC5296304).
  **Ressalva honesta de magnitude:** a própria verificação nota que os tamanhos de efeito
  da linha "gestos" tendem a ser **pequenos**; é mecanismo de compreensão, não bala de
  prata.

- **Avaliação *stealth* funciona e agrada — inclusive na faixa que faz a ponte para o
  fundamental II.** (Detalhado no Bloco 3; a validação empírica em "Newton's Playground"
  foi com 8º/9º anos, mas o princípio de "a própria tarefa vira a evidência" vale desde
  aqui.)

**O que a pesquisa recuperada NÃO cobre para esta faixa:** não há achado verificado
específico sobre autonomia, tamanho de texto/narração, duração de atenção ou desenho de
recompensa para 8–11 anos. As referências NNGroup existem no corpus, sem extração
verificada.

## 1.3 6º–9º ano (~11–15 anos) — "do concreto ao abstrato, com afeto"

**O que a evidência verificada sustenta (esta é a faixa mais bem coberta):**

- **Sequência Concreto→Pictórico→Abstrato (CPA, de Bruner) tem apoio empírico direto no
  8º ano.** Um experimento pré-pós com **730 alunos de 8º ano** (rural de Ruanda, distrito
  de Musanze), usando **fichas/azulejos algébricos (algebra tiles)** para fatorar
  expressões algébricas e quadráticas, encontrou **melhora substancial de desempenho** nos
  alunos ensinados por CPA versus o grupo de controle. **[ALTA]** Também subiu a
  **motivação intrínseca e a motivação de carreira** (medidas iguais antes, diferentes
  depois, a favor do grupo CPA). **[ALTA/MÉDIA]** O braço qualitativo mostrou que o CPA
  **transformou experiências negativas em positivas** e **reduziu a ansiedade**
  matemática. **[MÉDIA]**
  *Fonte: "Concrete-Pictorial-Abstract instruction: enhancing students' learning
  motivation and achievement in mathematics", Cogent Education / tandfonline
  10.1080/2331186X.2025.2558303 (Iyamuremye & Burns, 2025).*
  **Por que isso importa para nós:** é a evidência mais nítida de que, mesmo no fundamental
  II (fase abstrata), **começar pelo concreto/manipulável antes do símbolo** melhora
  desempenho **e** afeto. É exatamente a lógica de manipular-antes-de-formalizar do nosso
  motor. (Corroborado por meta-análise de manipulativos de Carbonneau, Marley & Selig,
  citada na verificação.)

- **A motivação medida (intrínseca) conecta-se à Self-Determination Theory.** A conclusão
  do CPA foi explicitamente enquadrada como "motivação autodeterminada relevante à SDT".
  As fontes de **Ryan & Deci / SDT** estão no corpus (selfdeterminationtheory.org; APA).
  **[RESSALVA de cobertura]:** a pesquisa recuperada **não extraiu um achado verbatim
  verificado da própria SDT** (autonomia/competência/relação) — apenas a menção dentro do
  estudo CPA e os links das fontes. Usar SDT como moldura conceitual, sem afirmar números.

**Síntese da faixa:** concreto→pictórico→abstrato é o caminho de ouro aqui; ele carrega
junto ganho de desempenho, de motivação e redução de ansiedade. É a faixa onde o app pode
ser mais "sério" sem perder o incorporado.

---

# BLOCO 2 — LEQUE DE MECÂNICAS INTERATIVAS BASEADAS EM EVIDÊNCIA

Restrição do app: só **toque, arrastar, traçar e regular** (leve, sem física pesada). A
espinha dorsal aqui é a **"matriz de ações de toque"** (Yeung & Ng, 2023): cada ação
física evoca um significado matemático — logo, **a escolha da mecânica não é estética, é
epistemológica**. Abaixo, cada mecânica ligada a um princípio com evidência, com faixa e
conceito.

## 2.1 Mecânicas que os claims sustentam

| Mecânica (só toque/arrastar/traçar/regular) | Princípio com evidência | Faixa / Conceito | Confiança |
|---|---|---|---|
| **Arrastar objetos concretos → agrupar/parte-todo** (fichas, dedos, "azulejos") | CPA/Bruner: concreto antes do símbolo (algebra tiles ↑ desempenho e motivação); coordenação ação-percepção | 6º–9º (fatoração/álgebra); adaptável a todas as faixas (parte-todo) | ALTA |
| **Tocar para contar / marcar cardinalidade** (finger-counting) | Cognição incorporada do dedo; magnitude cardinal e parte-todo | Pré–2º (contagem, número) | ALTA (mas ver ressalva do resultado nulo) |
| **Girar/rotacionar figura** | Ação↔percepção: rotação evoca propriedades geométricas | 3º–9º (geometria, transformações) | ALTA |
| **Traçar/desenhar caminho contínuo** (drag contínuo) | Gestos contínuos reforçam quantidades contínuas (a matriz mapeia ação→conceito) | 3º–9º (reta numérica, funções, grandeza contínua) | ALTA (efeitos pequenos) |
| **Regular um controle (slider) e ver o efeito** | Manipulação direta coordena ação e percepção | 3º–9º (variação, proporção, medida) | MÉDIA (inferido da matriz; sem claim isolado) |
| **Recuperação como jogo de adivinha/esconde** ("Que forma eu sou?") | Prática de recuperação em formato lúdico de baixo risco | Pré–5º (vocabulário, propriedades) | ALTA (formato) / RESSALVA (não é "mais eficaz", é menos ansioso) |
| **Avaliação embutida na jogada** (a ação da criança é a evidência) | *Stealth assessment* + Evidence-Centered Design | Todas (mais validada em 8º/9º) | ALTA |
| **Progressão por maestria adaptativa** (destrava conforme domina) | Adaptatividade dá ganho; ganho externo cresce com nº de habilidades dominadas | Pré–9º (qualquer conceito modelável) | MÉDIA / RESSALVA (correlação, não prova causal — ver 2.3) |

## 2.2 Como isso organiza o que JÁ temos

- **Cognição incorporada (gestos)** → é exatamente a "matriz de ações de toque". Nosso
  gesto não é enfeite: cada arrastar/tocar/girar deve ser escolhido pelo **conceito** que
  evoca. **[ALTA]**
- **Aprendizagem adaptativa (BKT/domínio por conceito)** → sustentada como caminho que dá
  ganho mensurável (My Math Academy). **[MÉDIA]** Ver ressalva causal em 2.3.
- **Avaliação *stealth*** → fortemente sustentada (Bloco 3); é o que permite "medir sem
  provar". **[ALTA]**
- **Revisão espaçada (Leitner) / autoexplicação / feedback de tarefa** → a recuperação
  lúdica de baixo risco cabe aqui como **embalagem afetiva**. **[RESSALVA / cobertura]:**
  a pesquisa recuperada **não traz** um achado verificado específico sobre Leitner, sobre
  autoexplicação, nem sobre "feedback de tarefa vs. de pessoa". Além disso, há uma fonte de
  **contraponto** honesta: *"Retrieval practice may not benefit mathematical word-problem
  solving"* (PMC9987560) — ou seja, o efeito da recuperação **não é universal em
  matemática**, especialmente em problemas de enunciado. Manter Leitner, mas sem prometer
  que resolve problema de palavras.

## 2.3 A ressalva que precisa ficar registrada (maestria ≠ prova causal)

A verificação **refutou** a leitura de que "dominar mais habilidades no app **prova** que a
progressão por maestria **causa** transferência, e não só engajamento". O achado real é uma
**correlação intragrupo** ("mais habilidades dominadas → mais ganho externo"), **confundida
com dose/tempo de uso** (dominar mais = usar mais). O estudo **não** dissocia maestria de
engajamento. Conclusão prudente para nós: a progressão por maestria é uma boa aposta de
design, mas **não devemos afirmar** que "só a maestria, e não o engajamento, gera o
aprendizado". **[RESSALVA — refutado]**

---

# BLOCO 3 — O DIFERENCIAL INOVADOR

## 3.1 O que a pesquisa aponta como faltante nos apps atuais

- **Gamificação sobe engajamento — e até desempenho — mas o efeito é MUITO desigual, e o
  que decide é o DESENHO, não os pontos.** A meta-análise mais forte do corpus (41 estudos,
  49 amostras, >5.071 participantes) achou efeito geral **grande e significativo:
  Hedges g = 0,822 (IC 95% 0,567–1,078)**. **[ALTA]** MAS o efeito é **significativamente
  moderado** por tipo de usuário (nível de ensino), disciplina, **princípios de design**,
  **duração** da experiência e ambiente. **[ALTA]** (Curiosamente, *como* se mediu o
  resultado e o tipo de publicação **não** moderaram — então o efeito não é artefato de
  medição.) **[ALTA]**
  *Fonte: "Examining the effectiveness of gamification… a meta-analysis", Frontiers in
  Psychology, PMC10591086 (Li, Ma & Shi, 2023).*
  **Leitura para nós:** "quiz gamificado com pontinho e medalha" pega o piso do efeito. O
  diferencial mensurável vem de **quais princípios de design** você usa e **por quanto
  tempo** — não do placar. (As fontes "Beyond Points and Badges", "The Dark Side of
  Gamification" e "Gamification with Purpose" estão no corpus reforçando esse ponto, mas
  **sem achado verbatim verificado** — cito como referências presentes.)

## 3.2 A abordagem que seria um diferencial real e mensurável

**O eixo mais fortemente sustentado pela pesquisa é a AVALIAÇÃO *STEALTH* / EVIDENCE-CENTERED
DESIGN.** Este é o "pulo do gato" defensável com evidência:

- **A tarefa natural do aluno VIRA a evidência da competência — sem prova separada.** A
  avaliação *stealth* tece a medição, invisivelmente, dentro da jogabilidade: durante o
  jogo, o aluno produz sequências ricas de ações usando as próprias competências que
  queremos medir; **as interações com o jogo são a evidência**. **[ALTA]**
  *Fonte: Shute & Ventura, "Stealth Assessment: Measuring and Supporting Learning in Video
  Games", MIT Press (open access), 2013; e o "Stealth Assessment handbook chapter"
  (Shute, Lu & Rahimi, FSU).*
- **Isso mede o que a prova de múltipla escolha NÃO mede** — criatividade, resolução de
  problemas, persistência — com medidas **dinâmicas e contínuas** do processo, combatendo o
  desengajamento. **[ALTA]**
- **O método concreto é o Evidence-Centered Design (ECD): três modelos — competência,
  evidência e tarefa.** É literalmente o arcabouço para o nosso **BKT/domínio por
  conceito**: definir a competência, definir que ação no app conta como evidência dela, e
  desenhar a tarefa que produz essa ação. **[ALTA]**
- **Já foi testado empiricamente e deu certo:** no jogo de física "Newton's Playground"
  (167 alunos de 8º/9º ano, ~4h), a avaliação *stealth* foi **válida** (indicadores no jogo
  previram aprendizagem), os alunos **melhoraram** a compreensão e **gostaram** da
  experiência. **[ALTA]**

**Complementos apontados pela pesquisa (presentes como fontes, com força variável):**

- **Open Learner Model (OLM) / metacognição visível.** Tornar o modelo do aluno **visível
  ao próprio aluno** para dirigir a metacognição. Fontes no corpus: "Open Learner Models as
  Drivers for Metacognitive Processes" (Bull & Kay) e "MetaCQ… Open Learner Model to
  support Metacognition". **[RESSALVA de cobertura]:** presentes como fontes, **sem achado
  verbatim verificado** — mas casam diretamente com "medir sem provar" + tornar o progresso
  legível ao aluno. É o candidato mais promissor a **somar** ao *stealth*.
- **Dificuldades desejáveis (Bjork).** Fonte no corpus ("Desirable Difficulties — síntese
  do trabalho de Robert & Elizabeth Bjork"). **[RESSALVA de cobertura]:** sem achado
  verbatim verificado. Coerente com espaçamento/recuperação, mas **atenção** ao contraponto
  do Bloco 2 (recuperação nem sempre ajuda em problema de enunciado).
- **Construcionismo / Papert.** **A pesquisa recuperada NÃO contém fonte de Papert nem de
  construcionismo.** Não posso fundamentá-lo com este material — se quisermos usar, é
  preciso nova pesquisa.
- **Tutoria adaptativa e avaliação formativa contínua.** Sustentadas indiretamente pelo
  eixo adaptativo (My Math Academy) e pelo *stealth* — mas com as ressalvas causais de 2.3.

**Currículo invisível SEM perder medição:** é exatamente o que o *stealth*/ECD entrega — o
aluno joga (currículo invisível), e o app coleta evidência estruturada (medição
preservada). Este é o ponto onde a pesquisa é mais robusta e mais alinhada ao nosso app.

---

# RECOMENDAÇÃO PARA O NOSSO APP

1. **Fazer o "stage-2 de produção" dos quizzes via Evidence-Centered Design, não via
   placar.** Para cada quiz, definir explicitamente os **3 modelos ECD**: (a) *competência*
   (o conceito BKT), (b) *evidência* (qual sequência de toque/arrastar/traçar conta como
   domínio — não só "acertou a alternativa"), (c) *tarefa* (a jogada que força essa ação).
   Assim a **própria produção do aluno** (mover fichas, traçar, agrupar) vira a medida — a
   "produção-não-reconhecimento" que já perseguimos ganha lastro de evidência. *(Base:
   Shute & Ventura, MIT Press; handbook Shute/Lu/Rahimi; validado em Newton's Playground.
   [ALTA])* Concretamente no quiz: substituir "escolha a resposta" por "**monte/arraste até
   ficar certo**", e registrar a trajetória como evidência.

2. **Manter a matriz "ação→conceito" como regra de design de toda mecânica.** Escolher
   tocar/arrastar/girar/traçar/regular **pelo conceito que a ação evoca**, não pela
   aparência. *(Base: Yeung & Ng, Computers & Education 2023. [ALTA])*

3. **O que muda por faixa etária:**
   - **Pré–2º (~4–8):** gesto do dedo (contar/agrupar) + recuperação **como brincadeira de
     baixo risco** (esconde-esconde / "que forma sou eu?") — usada pelo **clima e redução de
     ansiedade**, sem prometer ganho cognitivo extra. Lembrar do **resultado nulo**: o valor
     está no desenho curricular, não em "ser app". *(Ninaus/Barrocas 2023; EEF.)*
   - **3º–5º (~8–11):** mecânicas incorporadas de manipulação direta (arrastar/girar/traçar)
     ligadas a geometria e reta numérica; adaptatividade por maestria. *(Yeung & Ng.)*
   - **6º–9º (~11–15):** **CPA de verdade** — concreto/azulejos → pictórico → símbolo,
     inclusive em álgebra; é a faixa com maior ganho comprovado de desempenho **e** afeto.
     *(Iyamuremye & Burns, Cogent Education 2025. [ALTA])*

4. **Adaptatividade sim, promessa causal não.** Manter BKT/progressão por maestria (dá ganho
   mensurável, maior no **terço médio** de conhecimento prévio e nos conteúdos mais
   difíceis), mas **não** afirmar que "maestria, e não engajamento, causa o aprendizado" —
   a evidência é correlacional e confundida com dose. *(My Math Academy; ressalva da
   verificação. [MÉDIA/RESSALVA])*

5. **O "pulo do gato" do diferencial: casar *stealth assessment* (ECD) com um Open Learner
   Model visível.** O mercado gamifica quiz e sobe engajamento, mas mede pouca competência
   real (efeito grande **porém** dependente de design — g=0,822, fortemente moderado). Nosso
   diferencial mensurável é **medir invisivelmente pela jogada (currículo invisível +
   medição preservada) E devolver esse modelo ao aluno de forma legível** para ativar
   metacognição. É o único caminho no corpus que ataca a lacuna "engajamento sim,
   competência pouco". *(Li/Ma/Shi 2023 para a lacuna; Shute/Ventura para o stealth; Bull &
   Kay / MetaCQ para o OLM — este último presente como fonte, a confirmar com nova pesquisa.)*

6. **Registrar as lacunas honestas antes de prometer.** A pesquisa recuperada **não cobre**
   com achado verificado: Papert/construcionismo, Leitner especificamente, autoexplicação,
   "feedback de tarefa vs. pessoa", UX granular por idade (NNGroup) e SDT em detalhe. E há um
   **contraponto**: recuperação pode **não** ajudar em problemas de enunciado
   (PMC9987560). Se formos apostar nesses eixos, vale uma segunda rodada de pesquisa
   direcionada.

---

# FONTES USADAS

Todas as fontes abaixo constam do material recuperado. Marquei com ✔ as que embasam uma
conclusão **verificada** (com veredito), e com ○ as que aparecem no corpus como referência
**sem** achado verbatim extraído/verificado.

1. ✔ Yeung, W.L. & Ng, O.L. (2023). *Characterizing touchscreen actions in
   technology-enhanced embodied learning for mathematics… A systematic review (2010–2023).*
   Computers & Education. https://www.sciencedirect.com/science/article/abs/pii/S0360131523001586
2. ✔ Iyamuremye & Burns (2025). *Concrete-Pictorial-Abstract instruction: enhancing
   students' learning motivation and achievement in mathematics.* Cogent Education.
   https://www.tandfonline.com/doi/full/10.1080/2331186X.2025.2558303
3. ✔ Ninaus/Barrocas et al. (2023). *Design and empirical evaluation of a multitouch
   interaction game-like app for fostering early embodied math learning.* Int. J.
   Human-Computer Studies. https://www.sciencedirect.com/science/article/abs/pii/S1071581923000368
4. ✔ Bang, H.J., Li, L. & Flynn, K. (2023). *Efficacy of an Adaptive Game-Based Math
   Learning App (My Math Academy)…* Early Childhood Education Journal.
   https://link.springer.com/article/10.1007/s10643-022-01332-3
5. ✔ Li, M., Ma, S. & Shi, Y. (2023). *Examining the effectiveness of gamification… a
   meta-analysis.* Frontiers in Psychology. https://pmc.ncbi.nlm.nih.gov/articles/PMC10591086/
6. ✔ Shute, V. & Ventura, M. (2013). *Stealth Assessment: Measuring and Supporting Learning
   in Video Games.* MIT Press (open access).
   https://direct.mit.edu/books/oa-monograph/3700/Stealth-AssessmentMeasuring-and-Supporting
7. ✔ Shute, Lu & Rahimi. *Stealth Assessment* (handbook chapter).
   https://myweb.fsu.edu/vshute/pdf/sa_handbook.pdf
8. ✔ Education Endowment Foundation. *Retrieval practice: a game of 'hide and seek'.*
   https://educationendowmentfoundation.org.uk/news/retrieval-practice-a-game-of-hide-and-seek
9. ✔ *Retrieval practice may not benefit mathematical word-problem solving* (contraponto,
   PMC). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9987560/
10. ○ Nielsen Norman Group. *Design for Kids Based on Their Stage of Physical Development.*
    https://www.nngroup.com/articles/children-ux-physical-development/
11. ○ Nielsen Norman Group. *UX Design for Children (Ages 3–12), 4th Edition.*
    https://www.nngroup.com/reports/children-on-the-web/
12. ○ Nielsen Norman Group. *UX Design for Teenagers (Ages 13–17).*
    https://www.nngroup.com/reports/teenagers-on-the-web/
13. ○ UXmatters. *UX Design for Kids: Key Design Considerations.*
    https://www.uxmatters.com/mt/archives/2020/01/ux-design-for-kids-key-design-considerations.php
14. ○ *Interactive Design Framework for Children's Apps for Enhancing Emotional Experience.*
    Interacting with Computers. https://academic.oup.com/iwc/article/34/3/85/6964644
15. ○ Ryan & Deci (2020). *Self-Determination Theory: Intrinsic and extrinsic motivation…*
    https://selfdeterminationtheory.org/wp-content/uploads/2020/04/2020_RyanDeci_CEP_PrePrint.pdf
    (e cópia https://stial.ie/resources/Ryan%20and%20Deci%202020%20self%20determination%20theory.pdf)
16. ○ American Psychological Association. *Self-determination theory: A quarter century of
    human motivation research.* https://www.apa.org/research-practice/conduct-research/self-determination-theory
17. ○ *Cognitive load theory and individual differences.* Learning and Individual
    Differences. https://www.sciencedirect.com/science/article/pii/S1041608024000165
18. ○ *Desirable Difficulties — síntese do trabalho de Robert & Elizabeth Bjork.*
    https://theeffortfuleducator.com/2020/05/22/desiring-difficulties/
19. ○ Bull & Kay. *Open Learner Models as Drivers for Metacognitive Processes.*
    https://link.springer.com/chapter/10.1007/978-1-4419-5546-3_23
20. ○ *MetaCQ: An eTextbook platform with an Open Learner Model to support Metacognition.*
    https://arxiv.org/pdf/2512.01313
21. ○ *Grounded and embodied mathematical cognition…* (Nathan et al., PMC5285420).
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5285420/
22. ○ *SRLAgent: Enhancing Self-Regulated Learning Skills through Gamification and LLM
    Assistance.* https://arxiv.org/pdf/2506.09968
23. ○ *Gamification 2.0 — Beyond Points and Badges: Designing for Players, Not Metrics.*
    https://uxmag.com/articles/gamification-2-0-beyond-points-and-badges-designing-for-players-not-metrics-chapter-1-the-problem
24. ○ *The Dark Side of Gamification: When Points, Badges & Leaderboards Go Wrong.*
    https://www.growthengineering.co.uk/dark-side-of-gamification/
25. ○ *Gamification with Purpose: What Learners Prefer to Motivate Their Learning.*
    https://arxiv.org/html/2512.08551v1
26. ○ *Quantifying the Efficacy of Gamification on Student Learning.*
    https://elqn.org/quantifying-efficacy-of-gamification-on-student-learning/

**Corroborações citadas na verificação adversarial (não estavam na lista principal, mas
apareceram nos vereditos):** Duijzer/Shayan/van der Schaaf/Bakker/Abrahamson (2017),
*Touchscreen Tablets: Coordinating Action and Perception…* (PMC5296304); Thai, Bang & Li
(2022), *Accelerating Early Math Learning… A Cluster Randomized Controlled Trial* (J. of
Research on Educational Effectiveness — este é o ECR real do My Math Academy);
Carbonneau, Marley & Selig (2013), meta-análise de manipulativos; Shute, Ventura & Kim
(2013), *Assessment and Learning of Qualitative Physics in Newton's Playground* (J. of
Educational Research 106(6)); Roediger & Karpicke e Agarwal et al. (literatura primária de
prática de recuperação).
