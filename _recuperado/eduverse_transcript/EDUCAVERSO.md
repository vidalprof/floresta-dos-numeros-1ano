**único gasto real de engenharia** (feito uma vez, com modelo forte). Feito
isso, cada mundo novo passa a ser **~2-4 h** de trabalho (escrever o TEMA-SPEC +
revisar), **3 aprovações do professor** e os workflows engolindo o resto — API
barata (Gemini para ~15-25 cartelas + narração edge-tts grátis).

---

## A Fábrica de Atividades por currículo + Diretrizes do professor Marcos

> Esta seção foi acrescentada **depois** da rodada dos especialistas, para registrar
> requisitos que o professor trouxe e que são o **coração pedagógico** do EducaVerso.
> Fonte permanente: `MEMORIA-DO-PROJETO.md`.

### 1. A Fábrica de ATIVIDADES (irmã da Fábrica de Mundos)
Se a **Fábrica de Mundos** cria o *cenário*, a **Fábrica de Atividades** preenche
com o *aprendizado alinhado ao currículo* — **entra um objetivo do currículo, sai uma
atividade pronta e inserida no mundo**.

- **Fontes de currículo:** BNCC geral, **Computação BNCC** (já há o `ATIVIDADE-COMPUTACAO.md`),
  ou o **currículo de Blumenau** (já há o workflow `.github/workflows/baixar-curriculo.yml`,
  que baixa o PDF e extrai o texto para **ancorar a IA** no objetivo real — ela não inventa
  a habilidade). O professor escolhe **fonte + ano/turma + habilidade**.
- **Como monta:** a IA lê o objetivo real → escolhe a **mecânica** (do catálogo de
  interatividades) → cria o conteúdo/desafios → **embrulha na narrativa do mundo** (um
  personagem/lugar) → gera arte (pipeline de imagem) e voz.
- **Portão de qualidade:** a IA **rascunha**; o professor **aprova** (as 3 aprovações:
  missões/pedagogia, arte, jogável). "Automático" **sem** perder a mão pedagógica.
- **Inserção:** a atividade vira um **ponto/NPC/gatilho** no mundo; o resultado alimenta a
  avaliação descritiva.
- **Construído × a-fazer:** *existe* — `baixar-curriculo.yml`, `ATIVIDADE-COMPUTACAO.md`, o
  catálogo de mecânicas, o pipeline; *falta* — o **montador** que casa
  currículo → mecânica → mundo → faixa de forma semiautomática.

### 2. Adequação à TURMA (faixa etária) — regra obrigatória
A partir de **DISCIPLINA + TEMA + TURMA**, tudo se ajusta à idade: cenário, personagens,
dificuldade, mecânica, narração e missões.
- **Pré / 1º-2º (NÃO leitores):** só **ícone + voz + cor**; missões curtas de 1 passo; muita recompensa.
- **3º-5º:** leitura simples; missões de poucos passos; mais exploração.
- **6º-9º:** missões **multi-etapas**; mais autonomia e desafio.
A IA rascunha adequado à faixa; o professor confirma.

### 3. Aluno ATIVO/protagonista + as fases ENTREGAM o objetivo (gating)
- **O aluno CONSTRÓI** — monta a máquina, programa o robô, constrói a ponte, cria a solução.
  Nunca só assiste ou escolhe alternativa. **A construção só funciona se o conceito estiver
  certo → construir já é provar que entendeu.**
- **Gating no objetivo:** cada fase nasce de um objetivo do currículo e **só é concluída
  quando o aluno demonstra aquele objetivo** (a ponte só abre / o robô só chega / o navio só
  zarpa quando está correto). Não se "passa sem aprender".
- **Medição:** a avaliação invisível registra quem **alcançou** o objetivo e quem precisa de
  apoio → relatório descritivo para o professor **agir**.
- **Ciclo:** construir (ativo) → travar no objetivo (garante) → registrar (avaliação) → o
  professor vê quem alcançou.

### 4. Aprender SEM perceber que está estudando (a regra-mãe)
Reforço da regra anti-quiz: a criança sente **jogo primeiro, lição nunca explícita**. O
conhecimento é a **ferramenta para vencer a missão**, não a pergunta. Ex.: para ganhar a
chave do taberneiro, ela **organiza 4 prateleiras com 3 barris** (multiplicação) — ela achou
que **ajudou um amigo e ganhou um tesouro**, não que "fez uma continha".

### 5. O mascote do próprio aluno (pertencimento)
Além do Byte (guia), o aluno tem o **seu próprio mascote/avatar** que o acompanha; o Byte e
os NPCs interagem com ele, e a narração **fala o nome do estudante** ("Muito bem, João!").
Pertencimento + emoção = engajamento. *(A-fazer: modelar o avatar do aluno e sua seleção no
login por código de turma.)*

---

## Roadmap & Produto — do que existe hoje ao EducaVerso em sala

> Escrito como líder de produto, com honestidade. Separo com rigor o que **já
> está construído e funciona** do que ainda é **visão / a-fazer**. Nada de
> promessa vazia: cada fase entrega algo **jogável de verdade** na turma, e a