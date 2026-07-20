# Catálogo de INTERATIVIDADES "a criança CRIA e RESOLVE" (2026-07)

> Parte da rodada "reúna o pessoal". Especialista Game Designer + Pedagogo. 24 mecânicas de
> criar/resolver p/ navegador, PC fraco, 6-12. Força: [FORTE] meta/RCT · [MODERADA] · [CONSENSO] ·
> [OPINIÃO]. Custo: Baixo (DOM/CSS+drag) · Médio (canvas/SVG+estado) · Alto (física/simulação — risco PC fraco).

## ACHADO TRANSVERSAL (a "física" do projeto)
Descoberta SOZINHA não ensina — **d = −0,38** vs. instrução explícita; mas descoberta **GUIADA/andaimada**
(feedback + exemplos + explicação elicitada) vira **+0,30** (Alfieri 2011, 164 estudos) [FORTE]. Casa com
brincadeira guiada > livre > instrução direta (Skene 2022) [FORTE]. **REGRA DE OURO: toda mecânica precisa
de andaime + feedback + pedir p/ a criança explicar.** Observáveis-padrão de stealth: tentativas, acerto-na-1ª,
TIPO de erro, caminho/estratégia, latência, uso de dica, e o teste-chave — **transferência ao item-símbolo**.

## AS 24 MECÂNICAS (nome — ensina — mede — custo)
**A. Construir/compor quantidade e número**
1. **Compor a quantidade** (arrastar itens ao ten-frame até o número) — contagem/cardinalidade/subitização/composição 5+n — conta 1-a-1 vs. âncora 5; over/undershoot — **Baixo**. [FORTE-mod]
2. **Reta numérica manipulável** (arrasta p/ onde fica o 62; ou saltos +10/+1) — magnitude/estimativa/valor posicional — **erro absoluto = nota contínua limpa** (preditor #1 de matemática, r≈.44) — **Baixo**. [FORTE] ⭐
3. **Agrupar/reagrupar dezenas** (10 cubinhos estalam→1 barra) — valor posicional/reagrupamento (vai-um) — trocou espontâneo aos 10? onde erra o transporte — **Médio**. [CONSENSO+FORTE]
4. **Number bonds / parte-todo** (reparte 8 entre 2 potes de todo jeito) — composição-decomposição/fatos de adição — quantas decomposições distintas; sistemático vs. acaso — **Baixo**. [FORTE-mod]
5. **Balança de igualdade** (equilibra os 2 lados; resolve 4+▢=6) — sentido RELACIONAL do "=" / pré-álgebra — relacional vs. "somar tudo dum lado"; item com operação nos 2 lados — **Médio**. [MOD/CONSENSO]
6. **Repartir/encher/despejar** (fatia a pizza p/ N pratos iguais) — frações parte-todo / divisão por partilha justa — partes iguais? lida com resto? nomeia a fração — **Médio**. [MOD/CONSENSO]

**B. Criar/desenhar p/ responder**
7. **Desenhar-para-responder** (traça o caminho da água / fecha o circuito) — ciências causa-efeito/geometria/explicação — o traço É o modelo mental; nº refinamentos — **Médio**. Desenho gerativo d=0,52-0,85 (COM integração). [FORTE]
8. **Desenhar máquinas que agem** (rampas/alavancas que a física resolve — Physics Playground) — física qualitativa/causa-efeito — que agente usou revela o conceito — **Alto** (Matter.js, risco FPS). [MODERADA]
9. **Compor formas / tangram** (arrasta+gira p/ preencher a silhueta) — geometria/raciocínio espacial — usa rotação mental vs. tentativa-erro — **Médio**. [MOD/CONSENSO]

**C. Construir artefato / sandbox guiado**
10. **Construtor de cena/cidade/mundo** ("monte uma horta p/ 5 coelhos"; a simulação testa) — sistemas/planejamento — respeitou a restrição? nº iterações — **Médio** (exige rubrica/andaime). [CONSENSO/MOD]
11. **Projete-o-seu → cria o desafio p/ o colega** (esconde o tesouro, define a senha) — qualquer conteúdo em nível META — o desafio é solucionável/bem-formado? (proxy forte de domínio) — **Baixo-Médio** (serializa em URL, offline). [MODERADA]
12. **Criar/estender padrão** (continua 🔵🔴🔵🔴; cria o próprio e o Byte adivinha) — padrões/pensamento algébrico — achou a unidade de repetição? — **Baixo**. [FORTE/MOD]
13. **Sequenciador sonoro** (arrasta ícones de som que cantam em loop — Incredibox) — padrões/ritmo/causa-efeito, muito SONORO — explora sistemático? recria alvo — **Médio** (Web Audio, latência). [OPINIÃO/CONSENSO]

**D. Programar/sequenciar**
14. **Programar o robô + DEPURAR** (fila de setas; roda, vê o erro, conserta — Bee-Bot/ScratchJr) — pensamento computacional/espaço/planejamento — **depuração = observável mais rico** (localiza o bug?) — **Baixo-Médio**. [MOD/FORTE] ⭐

**E. Manipular-e-observar (causa-efeito e sistemas)**
15. **Micro-mundo de causa-efeito** (slider "mais sol→planta cresce?" — PhET) — ciências/controle de variáveis — isola 1 variável? prevê antes? — **Médio** (fórmula simples, sem engine). PhET d≈0,83. [FORTE]
16. **Ecossistema/emergente** (povoa habitat, vê sustentar/colapsar — NetLogo) — sistemas/interdependência/micro→macro — entende que não há causa única? — **Médio-Alto** (limitar população). [MOD/CONSENSO]
17. **Cuidar do ser vivo / ciclo de vida** (alimenta/rega; erro murcha visível) — seres vivos/ciclos/causa-efeito/empatia — relaciona ação→necessidade? — **Baixo-Médio**. Casa com "o MUNDO PRECISA". [MODERADA]

**F. Ciência / hipótese (problema primeiro)**
18. **Estimar-depois-conferir** ("quantos feijões no pote?" palpita→revela) — estimativa/senso numérico/autorregulação — **calibração melhora = aprendizado**; viés sistemático — **Baixo**. Falha produtiva g≈0,36-0,87. [FORTE] ⭐
19. **Predizer-Observar-Explicar / caça-com-hipótese** ("afunda ou flutua?" prevê→vê→explica) — raciocínio científico/argumentação — **revê a hipótese diante de evidência contrária?** — **Baixo**. [CONSENSO/FORTE]
20. **Construir a régua / medir com unidade** (enfileira unidades, marca traços, mede objeto DESLOCADO do zero) — medida/iteração de unidade/ponto-zero — deixa vãos? conta traços vs. intervalos? acerta o deslocado? — **Baixo-Médio**. [MODERADA]

**G. Social / narrativa / metacognição**
21. **Ensine o mascote** (a criança ensina o Byte as regras; ele age e ERRA visível; ela conserta o ensino — Betty's Brain) — qualquer conteúdo em profundidade/metacognição — **as regras ensinadas SÃO o modelo mental** (medição direta); localiza a causa do erro? — **Médio**. É o "Byte pergunta, não responde". Efeito protégé, maior em quem tem mais dificuldade. [MODERADA] ⭐
22. **História ramificada** (decisão→consequência; p/ avançar aplica o conceito) — leitura/decisão/conteúdo embutido — escolhas = raciocínio/valores; refaz p/ explorar — **Baixo** (estados+texto+voz, offline perfeito). [MODERADA] ⭐
23. **Ordenar/seriar com justificativa** (arrasta cartas à ordem certa + diz o porquê) — seriação/magnitude/cronologia — ordena por atributo certo? a **justificativa** separa "faz" de "sabe por quê" — **Baixo**.
24. **Loja simulada / dinheiro e troco** (monta o preço, dá troco contando p/ cima) — dinheiro/composição de valor/±aplicado — compõe eficiente? dá troco contando p/ cima? — **Baixo**.

## OBJETIVO → MELHOR MECÂNICA (tabela)
| Objetivo | Melhor(es) | Objetivo | Melhor(es) |
|---|---|---|---|
| Quantidade/contagem | 1, 23 | Ciências causa-efeito | 15, 19, 8, 7 |
| Magnitude/valor posicional | **2**, 3 | Ciências seres vivos | 17, 16 |
| Composição-decomposição | 4, 1, 5 | Sistemas/emergência | 16 |
| Soma/subtração c/ reagrupar | 3, 24, 2 | Espaço/mapa/lógica | 14, 9 |
| **Multiplicação/divisão** | **6 Repartir**, 16 (grupos) | Pensamento computacional | 14, 11 |
| Frações/parte-todo | 6, 9 | Alfabetização/fonológica | 1/12/23 aplicadas a sons |
| Igualdade/"=" pré-álgebra | 5, 12 | Leitura/produção/decisão | 22, 7, 21 |
| Geometria/formas/espaço | 9, 8, 14 | Raciocínio científico | 19, 18 |
| Medida/grandezas | 20, 18, 15 | Metacognição (ensinar) | 21 |
| Padrões/sequências | 12, 13 | Dinheiro / Tempo | 24 / 23, 22 |

## TOP (aprendizado × facilidade de medir ÷ custo, em PC fraco)
1. **Reta numérica (#2)** — erro absoluto = nota contínua limpa, preditor #1, custo Baixo. COMEÇAR POR ESTA. [FORTE]
2. **Estimar-depois-conferir (#18)** — mede calibração, é a falha produtiva, custo mínimo. [FORTE]
3. **Programar o robô + depurar (#14)** — depuração = observável mais rico, BNCC Computação. [MOD/FORTE]
4. **Ensine o mascote (#21)** — as regras ensinadas = modelo mental; é a filosofia do Byte. [MODERADA]
5. **Compor quantidade (#1) + Number bonds (#4)** — fluência/estratégia visíveis, base de tudo, Baixo. [FORTE-mod]
6. **POE/caça-hipótese (#19)** — mede o revisar diante de evidência, Baixo. [CONSENSO/FORTE]
7. **História ramificada (#22)** — máxima emoção/agência por menor risco técnico. [MODERADA]
**Evitar como 1ª entrega (caro/risco PC fraco):** #8 desenhar-máquinas-com-física e #16 ecossistema c/ muitos agentes.

## 3 REGRAS DE MEDIÇÃO (p/ o TOP inteiro)
1. Registre **o CAMINHO, não só o resultado** (ordem das ações, tentativas, dicas) — é isso que vira parecer.
2. Inclua **1 item-símbolo no fim** (sem apoios) p/ medir **transferência** (o teste da concretude que desvanece).
3. Voz humana conversacional ("VOCÊ consegue…") — personalização d≈0,79-1,11; **corte tudo que não é o núcleo no momento de pensar** (coerência d=0,86, 23/23).

## HONESTIDADE (p/ o Portão 1)
Efeito MÉDIO de "jogo educativo" genérico é modesto (Wouters d≈0,29; Clark 2016); os efeitos GRANDES aparecem
com **desafio calibrado + feedback imediato + andaime + pedido de explicação + ponte ao símbolo**. O que decide
o aprendizado não é "ser jogo", é o **design instrucional dentro do jogo**. As mecânicas de criar/resolver só
entregam se vierem **guiadas** (não soltas) e **instrumentadas** (medindo o caminho).

## FONTES (principais)
Alfieri descoberta guiada https://physics.uwyo.edu/~rudim/S14_JEduPsych_DoesDiscoveryLrngEnhance.pdf · Skene guided
play https://onlinelibrary.wiley.com/doi/10.1111/cdev.13730 · manipulativos VMR https://eric.ed.gov/?id=EJ1154970 ·
reta numérica https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01576/full · balança/"="
https://par.nsf.gov/servlets/purl/10201368 · partilha justa→divisão https://www.sciencedirect.com/science/article/abs/pii/S0959475221000190
· desenhar p/ aprender (Science) https://www.science.org/doi/10.1126/science.1204153 · Physics Playground
https://link.springer.com/article/10.1007/s40593-020-00196-1 · construcionismo https://www.sciencedirect.com/science/article/pii/S0747563219300184
· ScratchJr/CT https://pmc.ncbi.nlm.nih.gov/articles/PMC11109739/ · PhET meta https://online-journals.org/index.php/i-joe/article/view/59007
· ABM/sistemas https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2023.1198307/pdf · falha
produtiva (Kapur) https://journals.sagepub.com/doi/10.3102/00346543211019105 · concretude que desvanece (Fyfe)
https://link.springer.com/article/10.1007/s10648-014-9249-3 · efeito protégé (Chase 2009) https://link.springer.com/article/10.1007/s10956-009-9180-4
· padrões prevêem matemática https://www.sciencedirect.com/science/article/abs/pii/S0022096520304197 · construir a
régua https://link.springer.com/article/10.1007/s10643-025-01915-w · narrativa ramificada https://doi.org/10.3390/educsci16020283
· stealth (Shute) https://myweb.fsu.edu/vshute/pdf/design.pdf · Owen&Baker analytics https://learninganalytics.upenn.edu/ryanbaker/OwenBakerLAGames.pdf
· Clark 2016 meta https://vittoriodublinoblog.org/wp-content/uploads/2024/10/clark-et-al-2016-digital-games-design-and-learning-a-systematic-review-and-meta-analysis.pdf
· Mayer personalização/voz https://www.cambridge.org/core/books/abs/multimedia-learning/personalization-voice-and-image-principles/97F9B31362E6491806A4718FECCADE3D
