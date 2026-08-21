# 🎮 REGRAS DE MONTAGEM — o leque de interatividade: encaixe, armadilha e o que falta usar

> Destilado de `CATALOGO-DINAMICAS-INTERATIVAS.md`, `PESQUISA-CATALOGO-INTERATIVIDADES-2026-07.md`,
> `PESQUISA-SIMULACOES-EFICAZES-2026-07.md`, `PESQUISA-GEOGRAFIA-MECANICAS-6ANO-2026-07.md`,
> `PESQUISA-PENSAMENTO-COMPUTACIONAL-2026-07.md` e `PLANO-FORA-DA-CAIXA.md`.
>
> **(A)** é a tabela que eu consulto na hora de escolher a mecânica de cada fase.
> **(B)** é o que os documentos propõem e a gente ainda NÃO montou — é daqui que sai
> "o pensar fora da caixa" que o Marcos cobra.

---

## As 5 leis que valem para TODA linha da tabela

1. **Nenhuma mecânica ensina solta.** Descoberta pura **d = −0,38**; guiada/andaimada **+0,30**
   (Alfieri, 164 estudos). Toda mecânica precisa de andaime + feedback + pedido de explicação.
   `→ PESQUISA-CATALOGO-INTERATIVIDADES-2026-07.md`
2. **Contar GESTO, não conteúdo.** Duas fases podem ensinar coisas diferentes e ser, para a
   criança, a mesma tela pela terceira vez. Nenhum gesto acima de 40%, mínimo 4, mirar 8–12 em
   ~20 fases. `→ CLAUDE.md`, medido por `_qa/padrao.py`
3. **Enfeite que não carrega mecanismo ATRAPALHA** — detalhe sedutor: **g ≈ −0,16**
   (compreensão −0,19, transferência −0,12). Beleza a serviço do conceito.
   `→ PESQUISA-GEOGRAFIA-MECANICAS-6ANO-2026-07.md`
4. **Andaime IMPLÍCITO (o jeito PhET):** a meta vira o controle (o objetivo "altitude" vira o
   deslizante) e cada interação dá feedback imediato — guiar sem passo-a-passo escrito.
   `→ PESQUISA-SIMULACOES-EFICAZES-2026-07.md`
5. **"Ser jogo" não ensina.** Efeito médio de jogo educativo é modesto (d ≈ 0,29); os efeitos
   grandes vêm de desafio calibrado + feedback imediato + andaime + explicação + ponte ao
   símbolo. `→ PESQUISA-CATALOGO-INTERATIVIDADES-2026-07.md`

---

## (A) TABELA DE ENCAIXE

| Mecânica | Ensina BEM | Onde ATRAPALHA | Armadilha técnica | Encaixe |
|---|---|---|---|---|
| **Quiz / escolher** | Aferir rápido um fato já ensinado; aquecimento de revisão | Como motor da atividade — vira prova disfarçada e mata o efeito de geração (produzir retém 30–50% mais). Fábrica saiu 84% "escolher", Doceria 64% | Alto-falante em CADA opção (`op_<chave>.mp3` + `VOZOK`); distratores plausíveis; **embaralhar as opções** (a certa era sempre a 1ª) | Todas, pré–9º — **≤ 2 telas em 20** |
| **Completar lacuna** | Concordância, colocação, termo em contexto — produção mínima com apoio da frase | Quando vira quiz com 3 botões: perde a produção, que é o valor dela | A voz diz **exatamente** o texto escrito; em fase embaralhada o id da voz vem do ITEM, nunca do contador da rodada | Língua 1º–9º; transversal |
| **Digitar a resposta** | Ortografia, vocabulário, morfologia — o núcleo do "produzir, não reconhecer" **[FORTE]** | Onde a criança ainda não escreve fluente e o conteúdo não é a palavra: vira barreira motora | Teclado na tela **e** teclado de verdade (`document.onkeydown`); o teclado não tem acento: a palavra a adivinhar vai sem, a da faixa vai com (`ac:"BÚSSOLA"`) | Língua pré–9º |
| **Forca** | Onde a PALAVRA é o conteúdo (termo técnico novo) — soletrar sob tensão fixa a grafia | Em conteúdo conceitual: adivinhar letra não ensina o conceito | Letra usada **sai do `data-qa`**; palavra fechada tem que comemorar; aceitar teclado real | Língua, Ciências (termos), 3º–9º |
| **Memória** | Só quando o par é **conceitual** (causa↔efeito, fração↔desenho): aí é associação | Par igual↔igual como "descanso": **[FRACO]**, come 2–3 min de aula sem ensinar | Carta fluida **≥ 130×88 px**; verso de **arte de IA**; virada 3D `rotateY`; em tela baixa encolhe a LETRA, nunca a carta; som de virar e de par | Pré–6º |
| **Caça-palavras** | Reconhecer a forma escrita de um termo novo; alívio entre fases pesadas | Como avaliação: não mede compreensão, só varredura visual | Célula em `100/N` por cento com `box-sizing:border-box` (com px fixo cabem 10 numa grade de 9); diagonal nas 4 direções e o enunciado avisando; célula conquistada **trava**; conferir `mark` **OU** `ok` | Língua e termos, 2º–9º |
| **Cruzadinha** | Definição → palavra: força recuperar o termo a partir do sentido | Quando a definição é longa: vira leitura difícil disfarçada de jogo | Mesmas regras do caça-palavras + teclado real; alvo ≥ 40 px | Língua, Ciências, Geografia, 3º–9º |
| **Simulador / deslizar** | Causa-efeito e controle de variáveis: **PhET d ≈ 0,83** — mas só com inquérito guiado | Em conteúdo sem relação funcional (gramática, cronologia): o deslizante vira enfeite | O mundo reage **de verdade** (foto que gira não é simulador); ponto medido na figura, não a olho; a figura é de IA, o CSS anima só o que se mexe | Ciências 3º–9º, Geografia 4º–9º |
| **POE (prever-observar-explicar)** | Colar em qualquer simulação: prever antes é **falha produtiva, d ≈ 0,43** | **Fraco fora de STEM** — não usar como ritual universal | Termina em revisão explícita ("o que eu pensava × o que vi"); a concepção errada se **nomeia antes** de mostrar o certo | Ciências/Matemática 3º–9º |
| **Classificar em gavetas** | Formar categoria por atributo definidor — o que separa especialista de novato | Quando as categorias se sobrepõem: a criança acerta e o app diz que errou | Enunciado sem termo que ela não conhece ("veio de lá" → **"veio de fora"**); as gavetas se **refazem** quando o eixo muda e os dois eixos nunca se misturam; a explicação espera o áudio (`depoisDaFala`) | Todas, pré–9º |
| **Ligar colunas** | Relação 1-a-1 explícita (termo↔definição, mapa↔foto) | Com 10 pares: vira memória disfarçada, carga alta e zero raciocínio | Alto-falante nos **dois** lados; a linha precisa de `touchmove`; alvo ≥ 40 px | Todas, 2º–9º |
| **Ordenar / seriar** | Seriação, etapas de processo, magnitude — **com a justificativa** | Sem o "por quê": vira tentativa-e-erro até travar | Três caminhos de arrasto; conteúdo conferido — o portão não pega erro histórico, só o especialista | Matemática, Ciências, Língua, História |
| **Linha do tempo** | Cronologia, antes/depois, duração (contextualização 52→77%) | Em Ciências sem processo temporal, ou com datas que não significam nada | Faixa com `overflow-x` próprio; datas verificadas; arrasto com toque | História 3º–9º |
| **Arrastar-para-o-lugar** | Localização e parte-todo: pôr no lugar É o conceito espacial | Quando não há "lugar certo" espacial: a vaga vira botão com passo extra | **Três caminhos:** mouse, dedo e toque simples — no celular vêm eventos de mouse FANTASMA depois do toque (guardar `ultimoToque`); **nunca** `preventDefault` no `touchstart`. Defeito pego DUAS vezes | Geografia 3º–9º, Ciências, Matemática |
| **Achar na cena / lupa** | Observação dirigida: ler a paisagem, achar a evidência | Quando o alvo não tem contorno claro: vira caça ao pixel | Zona = a FIGURA recortada por cor de pixel (grade 48×48), **não** um pontinho com raio; alvo no pixel mais longe da borda (`distance_transform_edt`); achou = **V verde**; singular só se houver UMA | Geografia, Ciências, História |
| **Pintar / marca-texto** | Mapear categoria sobre o real — o traço É a classificação | Como colorir livre: bonito e vazio | A figura é **arte de IA**; o mapa começa **sem cor** e ela pinta de verdade (camadas recortadas por pixel); no texto, traço correndo + som de risco + barra + carimbo | Geografia, Língua, Ciências |
| **Traçar caminho / circuito** | Causa-efeito e geometria: desenhar-para-aprender **d ≈ 0,52–0,85 quando integrado** | Traço decorativo sem consequência: perde todo o efeito | `touchmove` com tolerância; o traço tem que **produzir** algo (a água corre, a luz acende) | Ciências, Geografia, Matemática |
| **Montar a frase** | Sintaxe visível: quem **manipula** rende **1–2 desvios-padrão** acima de quem só lê | Em texto longo: a frase tem que caber sem rolar | Contraste medido nos dois temas; três caminhos de arrasto; resposta fora da tela reprova | Língua 1º–7º |
| **Morfemas** | Formação de palavra — **d ≈ 0,33 geral, 0,59 decodificação**; maior ensinando RADICAIS | Onde a palavra da unidade não é derivada | Combinação impossível **devolve a peça** (a regra é o feedback), não dá X | Língua 2º–9º |
| **Ensinar o mascote** | Metacognição: as regras que ela ensina **são** o modelo mental | Quando o mascote acaba dando a resposta: quebra a LEI | O Byte precisa **errar visível** com a regra ensinada; enunciado que muda por rodada exige voz por rodada | Todas, 3º–9º |
| **Construir o gráfico** | Construir é competência **distinta** de ler — e melhora também a leitura | Como leitura de gráfico pronto: aí é quiz, não isto | Barras com passo discreto; ligar à cena correspondente | Geografia 4º–9º, Matemática |
| **História ramificada** | Agência: a escolha aplica o conceito e o mundo muda. Máxima emoção pelo menor risco técnico | Quando a escolha é enfeite e não liga ao conteúdo | Estado sobrevive ao recarregamento (`_padrao/RETOMAR.md`); `localStorage` não existe em `file://` | Língua, História, Geografia |
| **Autoria / galeria** | Efeito de geração + autonomia: o que ela cria fica. É o "quero mais" | Sem rubrica: vira desenho livre e não mede nada | O artefato persiste; serializar o desafio em URL evita servidor | Todas — sempre no FECHO |
| **Girar / vira-tapete** | Comutatividade e invariância: girar **é** o argumento | Fora de estrutura multiplicativa/geométrica | Encaixe nos 90° (≥ 50° para disparar) | Matemática 3º–5º |
| **Coordenada / bússola** | Localização por par ordenado e orientação | Onde não há espaço a orientar | Célula ≥ 40 px; **um** movimento para **um** conceito; referência explícita ("o lado da sua direita") | Geografia 3º–9º |
| **Camadas do mapa** | Correspondência mapa↔realidade — ler mapa é raciocínio analógico | Com muitas camadas ao mesmo tempo: carga extrínseca estoura | Uma camada por vez com sinalização; animação curta, nunca autoplay longo | Geografia 5º–9º |
| **Investigar a fonte** | Cruzar fontes e decidir — supera controles em pensamento histórico E compreensão leitora | Antes do 4º ano sem redução | Cada fonte com autor/data/motivo visíveis; o veredito exige apontar a evidência | História 4º–9º |
| **Programar o robô + depurar** | Sequência, laços, condicionais; **a depuração é o observável mais rico** | Como atividade avulsa: evidência **fraca** de transferência durável | Blockly roda client-side, offline, 1 HTML; execução passo a passo obrigatória | Computação pré–9º |
| **Sequenciador sonoro** | Padrão, pulso e subdivisão — muito sonoro | Como "ganho de alfabetização": um ECR **não achou transferência** | Latência do Web Audio; loop precisa de pré-carga | Música, Matemática (padrão) |
| **Mistério / investigação** | "Aprender resolvendo um caso": inquérito **guiado** d ≈ 0,50 | **Mistério aberto demais, sem pista nem meta, frustra** | Erro tem que **dar mais pista**, nunca punir | Ciências, Geografia, História |
| **Escape room** | Quando **o conteúdo é a chave**: integração intrínseca e engajamento alto | Enigma decorativo = "brócolis com chocolate"; cadeia longa estoura a carga | Custo é de ROTEIRO; travar a próxima sala exige estado persistente | Transversal 4º–9º |
| **Sistemas / equilíbrio** | Pensamento sistêmico e trade-offs | Sem andaime vira "mexer à toa"; **[EVITAR muitos agentes em PC fraco]** | Poucas espécies e **barras**, não enxame animado | Ciências, Geografia, 5º–9º |
| **Exemplo resolvido que desvanece** | Procedimento novo: exemplo → completar → resolver, com **menos tempo** **[FORTE]** | Com aluno que já domina: vira redundância | Não é fase, é regra da escada — os passos têm que sumir de verdade | Todas |
| **Autoexplicação induzida** | O mascote pergunta "por quê?" e ela **aponta**: **g ≈ 0,55**, 64 estudos | Se virar campo de digitar no 2º ano: barreira motora | Ela toca o desenho do porquê, não digita; o mascote nunca dá a resposta | Todas |

---

## (B) O QUE OS DOCUMENTOS PROPÕEM E A GENTE AINDA NÃO MONTOU

Ordem: da mais viável (1 HTML, ES5, PC fraco, Chrome 109, zero arte nova) para a mais cara.
Conferido contra o acervo (`_clima`, `_historia`, `_jardim`, `_orbi`, `_doceria`, `_fabrica`,
`_circo`, `_redacao`, `_generos`, `_estrelas`, `_mapa`, `_naveg`).

### Nível 1 — cabe no motor de hoje sem código novo

1. **Conserte o erro (exemplo errôneo).** A criança recebe a solução **já feita com um erro
   plantado** e tem de achar e corrigir. Conta armada errada, climograma mal montado, frase com
   concordância quebrada. É o motor de "achar na cena" que já temos, com o conteúdo invertido.
2. **Exemplo resolvido que DESVANECE.** Primeira rodada quase pronta, os passos vão sumindo.
   Para toda atividade que ensina um **procedimento** novo. **[FORTE]**, custo zero.
3. **Autoexplicação induzida como passo FIXO.** Existe embrionária, nunca como beat obrigatório:
   ao fechar um passo, o Byte pergunta "por quê?" e ela **aponta** a razão. **g ≈ 0,55**.
4. **Afirmação–Evidência–Raciocínio (CER).** Três cartas arrastadas: o que afirmo, a prova, o elo.
   Ciências 4º–9º e texto argumentativo — "pensar como cientista" com custo de três `div`s.
5. **Cravar na reta numérica.** Toca onde fica o 62. **Um dos melhores preditores do desempenho
   matemático**, e o erro absoluto vira nota contínua limpa para o professor.
6. **Experimento justo (controle de variáveis).** Muda só uma coisa por vez; se mudar duas, o
   mascote avisa. **[FORTE] e transfere** (Chen & Klahr).
7. **Balança da igualdade.** Para quem lê "=" como "aqui vem a resposta". 2º–4º equivalência,
   5º–9º isolar a incógnita.
8. **Mudança e permanência.** Deslizante de tempo entre duas cenas da mesma rua; ela separa o que
   mudou do que ficou. História e "transformação do lugar" — custo: 2 imagens.
9. **Mistério / geo-mistério guiado.** "Por que o rio secou?" — pistas que aproximam, erro que dá
   mais pista. Brilha como **arco de uma atividade inteira**, não como fase.
10. **Memória de par CONCEITUAL.** O motor já está pronto; falta trocar igual↔igual por
    causa↔efeito. Upgrade de conteúdo, não de código — muda de **[FRACO]** para **[MODERADO]**.
11. **Mapa da história.** Cenário → personagem → problema → tentativas → solução, arrastando
    trechos. Sumarização g ≈ 0,57, com a ressalva de que o ganho pode não se manter sem revisão.
12. **Costurar com conectivos.** Troca "mas" por "então" e a cena encena o novo sentido. Usar
    como andaime para quem precisa, não como regra universal.
13. **Crie o desafio para o colega.** Ela esconde o tesouro e o desafio **serializa em URL** (sem
    servidor). Criar um desafio bem-formado é proxy forte de domínio.

### Nível 2 — pede SVG/canvas leve ou estado novo (ainda 1 HTML, ES5)

14. **⭐ Mapa conceitual construído.** Arrastar conceitos e **traçar setas rotuladas**. É a
    **evidência mais forte de todas as mecânicas novas** (d ≈ 0,63–0,66; construir vale muito mais
    que copiar) e abre Ciências/História/Geografia/Língua com um só gesto.
15. **Traçar o exemplo com o dedo.** Antes de resolver, ela percorre o exemplo e o rastro
    desvanece. Quem traça resolve mais, mais rápido, com melhor transferência.
16. **Compor formas / tangram.** Temos o girar, falta o **encaixe-silhueta**. Geometria pré–7º.
17. **Máquina de simetria.** Traçar o outro lado da borboleta. Matemática e Arte pré–7º.
18. **Geometria dinâmica: arrastar o vértice.** O que muda e o que se **conserva** — a construção
    "de aparência" desmancha ao arrastar, e isso é o argumento. Matemática 4º–9º.
19. **Girador de probabilidade.** Roda 200 vezes e vê a frequência se aproximar da teoria. 4º–9º.
20. **Bancada de circuitos.** Fechar o laço e a cidade acende. Ganho ~0,81 vs ~0,39 com inquérito
    guiado. Ciências 4º–9º.
21. **Teia alimentar com cascata.** Tira o predador e o bioma seca. **Poucas espécies e barras.**
22. **Perfil do relevo pelas curvas de nível.** O traço vira a montanha ao lado. **[PROMISSOR]**.
23. **Grade rítmica.** Compor a batida numa grade de pulsos — **sem prometer alfabetização**.
24. **Camadas / coroplético sobre o MESMO mapa.** É a mecânica de correspondência explícita que a
    pesquisa recomenda para ler mapa. Geografia 5º–9º.
25. **Escape room encadeado.** O conteúdo é a chave da próxima sala. **[PROMISSOR]** — motivação
    alta, ganho de aprendizado menos consolidado.

### Nível 3 — caro, ou com ressalva explícita

26. **Programar o robô num grid + depurar, com Blockly.** Melhor custo-benefício da pesquisa de
    Computação. **Mas o Marcos pediu para deixar Computação de lado por enquanto.**
27. **Turtle/Logo e Parsons.** Zero arte — a criança gera a arte. Mesma trava acima.
28. **Sistemas com loops de feedback.** 6º–9º, **exige andaime forte senão vira "mexer à toa"**.
29. **Construtor de cena construcionista.** Exige rubrica e andaime; **[MODERADA]**.
30. **Assembleia / júri.** História e cidadania 5º–9º — medir o ganho é difícil.
31. **Prancheta tática.** Ed. Física 4º–9º: efeito grande em decisão (ES ≈ 0,89) **mas com
    qualidade de evidência baixa**.
32. **Máquinas com física (Matter.js).** **[EVITAR em PC fraco]** — risco de travar.

---

**Se for pegar três do bloco B para a próxima atividade:** *Conserte o erro* (1), *Mapa conceitual*
(14) e *Mistério guiado* (9) — o primeiro é quase de graça, o segundo é a evidência mais forte que
ainda não usamos, e o terceiro é o formato que dá o "quero mais" que o Marcos cobra.
Regra anti-repetição do `PLANO-FORA-DA-CAIXA.md`: **nunca o mesmo VERBO em fases vizinhas.**

---

## 🔤 SÍLABAS: JUNTAR E SEPARAR (pesquisa ago/2026 — Reading Rockets e outros)

*Trazido pelo `pesquisar.yml`; fonte principal Reading Rockets, que é referência
séria (as lojas de material didático que vieram junto foram descartadas).*

**O que a pesquisa diz, e que muda o desenho da mecânica:**

1. **Começar pela unidade GRANDE e descer.** *"Beginning with larger units of
   speech can help"* — frase → palavra → **sílaba** → fonema. No 1º ano a sílaba
   é o degrau certo; o fonema vem depois.
2. **O som CONTÍNUO ensina mais que o som picado.** O estudo citado chama-se
   *"Connected Phonation Is More Effective than Segmented Phonation for Teaching
   Beginning Readers to Decode Unfamiliar Words"*: **"ssssuuunnn" rende mais que
   "s‑u‑n"**. ⚠️ Isto é regra de ÁUDIO, não de tela: ao juntar sílabas, a voz
   tem que **deslizar** de uma para a outra, não dar duas batidas separadas.
3. **O gesto ajuda o conceito.** *"Hand motions help reinforce the concept."*
   Para JUNTAR, a metáfora citada é o **escorregador**: as partes *deslizam* uma
   até a outra e viram uma coisa só. Para SEPARAR, é **bater palma** — uma por
   sílaba — ou **a mão no queixo**, que cai uma vez por sílaba.
4. **"Robot Talk"** — o boneco fala picado e a criança junta. É o inverso do
   escorregador, e é o mesmo conteúdo pelo outro lado.
5. **Figura em vez de palavra escrita** para os menores.
6. **Separar por NÚMERO de sílabas** (uma pilha para 1, outra para 2, outra para
   3) é atividade consagrada — e isso a nossa peça `classificar` já faz.
7. **Trocar sílabas para inventar palavras bobas** — manipular, não só
   reconhecer. É autoria, e é o "quero mais".

**O que isso significa para a oficina (medido contra as 74 peças):**

| o que a pesquisa pede | temos? |
|---|---|
| som inicial (ouvir e achar a figura) | ✅ `ouvir-achar` |
| separar por número de sílabas | ✅ `classificar` (gavetas 1, 2, 3) |
| traçar a letra | ✅ `tracar-letra` |
| **JUNTAR sílabas com deslize e som contínuo** | ❌ **falta** |
| **BATER as sílabas (uma toque por sílaba)** | ❌ **falta** |

As duas que faltam são o **coração da alfabetização** — e nenhuma das 74 faz o
gesto delas.
