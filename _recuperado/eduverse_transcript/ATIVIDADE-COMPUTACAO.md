# ATIVIDADE DE COMPUTAÇÃO — o FORMATO NOVO (BNCC Computação)

> **Gatilho:** quando o Marcos disser **"atividade de computação"**, é ESTE formato
> (não o molde premium do Circo). Responder sempre em **português**.
> **Status: EM TESTE.** O trabalho premium normal continua igual; este é um formato
> novo que vamos **experimentando e melhorando conforme a necessidade** — registrar
> aqui tudo que a gente aprender (como nos outros manuais).

================================================================
## 1. O QUE É / PRA QUÊ
================================================================
- Ensinar **Computação** (BNCC Computação) **TUDO NO COMPUTADOR** — **nada desplugado**
  (sem tampinhas, sem papel). É pedido do Marcos: interativo, na tela, engajante.
- **1 HTML único autossuficiente**, offline, o aluno **abre e resolve** — igual às nossas
  atividades. Sai pronta.
- **Não é a "atividade premium".** O premium é o molde do Circo (contar/soletrar/etc.
  gamificado). A de computação tem **MECÂNICAS PRÓPRIAS** (programar, depurar, achar
  padrões) a serviço dos **eixos da BNCC Computação**. PODE usar as camadas de engajamento
  do premium (mascote, narração, mapa de fases, medalhas, níveis, Extra/Reforço) — mas o
  **coração é outro**.

================================================================
## 1.5 OS ESPECIALISTAS (chapéus) — vestir SEMPRE
================================================================
Além do time que já temos, a computação pede **dois específicos**:
- **👨‍🏫 Professor de Computação (BNCC Computação) experiente** — autoridade no eixo e nos
  **objetivos por ANO**; garante que o conteúdo é certo e adequado à idade. Usa o **documento
  oficial** como fonte (confirmar, nunca inventar código).
- **🧩 Designer de desafios de Pensamento Computacional** (um "level designer" de puzzles) —
  quem **desenha os labirintos/sequências** com **boa curva de dificuldade**. É o segredo de um
  Lightbot/Code.org: puzzle bem escalonado engaja, puzzle mal desenhado mata o interesse. Esse é
  o chapéu **novo e crítico** deste formato.
- **🧸 Pedagogo** (Pré → 5º) — como a criança pequena aprende a pensar computacionalmente.
- **💻 Dev sênior** — o **motor executor** e a compatibilidade.
- **🎨 Designer instrucional** — a sequência didática, a progressão e o engajamento.
- **🔎 Time de QA** (já existe) — Auditor (compat) + Testador (joga até o fim) + Revisor de
  Português + Acessibilidade.

================================================================
## 2. OS 3 EIXOS DA BNCC COMPUTAÇÃO
================================================================
1. **Pensamento Computacional** ← **COMEÇAMOS SÓ POR AQUI.**
2. **Mundo Digital** — depois.
3. **Cultura Digital** — depois.

Não misturar tudo de uma vez. Fase 1 do projeto = só Pensamento Computacional.

================================================================
## 3. PENSAMENTO COMPUTACIONAL — os PILARES (giram em TODO ano, aprofundando)
================================================================
São ~5 pilares que se repetem do Pré ao 9º; o que muda é a **profundidade** (espiral):
- **Decomposição** — quebrar um problema grande em pedacinhos.
- **Reconhecimento de padrões** — o que se repete.
- **Abstração** — focar no que importa, ignorar o resto.
- **Algoritmo** — a sequência de passos.
- **Depuração (debug)** — achar e consertar o erro.

================================================================
## 4. MECÂNICA-ESTRELA: "PROGRAME O ROBÔ/MASCOTE" (o MOTOR)
================================================================
- A criança **monta uma SEQUÊNCIA de comandos** (andar, virar, pular, `repita Nx`,
  `se…então`) e aperta **EXECUTAR**; o mascote anda **passo a passo** por um
  labirinto/grade; **vence** ao chegar no objetivo.
- **CLICAR pra montar a fila** (toca no comando → entra na fila; toca pra remover) —
  **NUNCA arrastar.** HTML5 drag-and-drop **trava em navegador antigo e em toque**;
  clicar é **mais compatível** e **melhor pros pequenos** e pra lousa/tablet. *(lição
  antecipada — não repetir o erro do drag.)*
- **Executor:** a fila é um **array**; roda com **`setTimeout`/`setInterval`** (compat),
  anima o mascote e **destaca o comando atual** enquanto executa.
- **Depuração:** quando falha, **mostrar ONDE** (qual passo) deu errado; deixar
  **consertar e re-executar sem punir** (mesmo espírito do "feedback que ensina").
- **Compatibilidade SAGRADA:** só `var`/`function`/`for`; nada de ES6; pares `-webkit-`;
  emoji ≤ Unicode 6.0; grade com `div` ou `<canvas>`; imagens reais em base64 (nunca SVG).

================================================================
## 5. REAPROVEITAR O QUE JÁ TEMOS (os outros eixos, quando chegar a hora)
================================================================
- **Mundo Digital** → **pixel art** (mesmo motor da nossa Tela de Pintar): "a imagem é
  feita de quadradinhos" = representação de dados. Também: "monte o computador"
  (clicar as peças), "mande o pacotinho" pela rede.
- **Cultura Digital** → **quiz com feedback que ensina** (cenários de escolha: "é
  verdade ou boato?", "essa senha é segura?", "como agir legal online?").
→ ~80% do formato reusa mecânica que já dominamos; o pedaço **novo** é o **executor de
  comandos** (construir 1 vez, reusar em todas as atividades de computação).

================================================================
## 6. PROGRESSÃO POR ANO (espiral) — SEQUÊNCIA DIDÁTICA PARA CADA ANO
================================================================
Mesmos pilares, complexidade crescente:
- **Pré / 1º** — comandar o mascote **2–3 passos** (setinhas); **continuar padrões** simples.
- **2º / 3º** — sequências maiores, **`repita Nx`**, **primeiro debug** ("por que o robô caiu?").
- **4º / 5º** — **`se…então`**, **decompor** a missão em etapas, laços.
- **6º ao 9º** — **laços aninhados**, **variáveis**, algoritmos mais abstratos, **eficiência**
  ("qual caminho usa menos comandos?").

================================================================
## 7. ENGENHARIA: UM MOTOR + CONFIG POR ANO (igual à base-mãe)
================================================================
- Construir o **executor UMA vez**; cada ano vira só uma **configuração** dele: quais
  comandos liberam, tamanho da grade, desafios, objetivos. A **série inteira** (Pré→9º)
  sai **sem refazer do zero**.
- **Escopo honesto:** Pré→9º = ~10 níveis; é um **currículo**, não uma tarde. Caminho
  esperto: **prototipar UM ano primeiro** (de preferência um que o Marcos dá aula agora),
  acertar o motor e o "gostinho", e **replicar** pra cima/baixo depois.

================================================================
## 8. BNCC COMPUTAÇÃO (fonte da verdade)
================================================================
- Mapear os **objetivos/habilidades** do eixo **por ANO** no documento **oficial**
  (Complemento à BNCC — Computação, CNE/CEB 2022). **CONFIRMAR, nunca inventar** código.
- Cada sequência **declara quais objetivos cobre** (material lindo pra coordenação:
  "esta sequência do 3º ano cobre tais habilidades").

================================================================
## 9. RITO (leve — formato em teste, vai evoluir)
================================================================
1. **Planejar:** escolher **ANO + pilar(es)**; mapear os **objetivos BNCC** (confirmar);
   desenhar os desafios (labirintos/sequências) na progressão da idade. Sugerir 2–3
   ideias de desafio pro Marcos escolher.
2. **Construir:** motor (executor) + config do ano. Imagens **por cartela** (mascote,
   grade/cenário, ícones dos comandos, objetos) — front-load dos prompts, cartela única.
3. **Testar:** `auditar-geral.py` (compat) + `testar-jogando.py` (joga até o fim, 0 erro)
   + revisão de **Português** e **Acessibilidade**. Conferir imagens com o Marcos.
4. **Publicar:** repo próprio (1 HTML); card no hub se fizer sentido.

================================================================
## 10. O MÍNIMO NÃO-NEGOCIÁVEL (igual a TUDO que fazemos)
================================================================
- **1 HTML único** autossuficiente; roda em **navegador antigo** + **0 erro de JS**;
  **imagens reais** (nunca SVG); **português**; **na dúvida, PERGUNTAR, não inventar**;
  **auditar/testar antes de publicar**.

================================================================
## 11. ENGAJAMENTO
================================================================
- Pode ser **premium** (mascote, narração, história, mapa de fases, medalhas, níveis,
  Extra/Reforço) **ou mais enxuto** — o Marcos decide. O tipo "programe o robô" já é
  **naturalmente viciante** (testar → errar → ajustar → "só mais uma vez").
