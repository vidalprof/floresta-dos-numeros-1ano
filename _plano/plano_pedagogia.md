# PARECER PEDAGÓGICO — MUNDO VIVO
## Prof. Marcos · E.B.M. Vidal Ramos · escola pública · jul/2026
### Fundamentação BNCC + construcionismo aplicada ao game-mundo anual

> Documento de apoio ao professor Marcos para conversa com a direção, planejamento
> do ano e defesa do projeto. Baseado em IDEIA-MUNDO-VIVO.md, MUNDO-VIVO-ESPINHA.md
> e MUNDO-VIVO-MOTOR.md. Escrito em linguagem que a direção entende, sem jargão vazio.

---

## 1. POR QUE MICROMUNDOS CONCRETOS ENSINAM MAIS QUE EXERCÍCIOS
### (texto pronto para o Marcos ler para a direção)

Seymour Papert (MIT, pai do construcionismo) mostrou que a criança aprende de
verdade quando **constrói e manipula** algo que lhe importa, não quando responde
uma conta solta na folha. Ele chamou isso de **micromundo**: um lugar onde a
criança age, o mundo reage na hora, e ela vê a consequência do que fez. No nosso
Mundo Vivo a matemática deixa de ser a *pergunta* e vira a *ferramenta* — a
criança reparte 20 brigadeiros em 4 pratos porque um personagem PEDIU, e se um
prato fica com menos, a carinha entristece e ela conserta. O erro não é um "X
vermelho" que humilha: é uma consequência que ela mesma resolve. Isso troca o
medo de errar pela vontade de acertar, e é a diferença entre **decorar** e
**compreender**. Pesquisa de aprendizagem (do concreto para o abstrato — Bruner,
Dienes) confirma o mesmo caminho que o jogo faz: primeiro a mão manipula a
quantidade, depois aparece a plaquinha "20 ÷ 4 = 5". A conta é o **prêmio da
descoberta**, não o começo da tortura.

**Frase-síntese para a direção:** "Em vez de a criança responder à matemática,
ela usa a matemática para resolver um mundo que precisa dela. É a BNCC vivida,
não decorada — e o jogo registra sozinho o que cada aluno já domina."

---

## 2. COMO ESTRUTURAR O ANO COM O MUNDO

### 2.1 Bairros = unidades curriculares
O currículo do ano inteiro É o mapa do mundo. Cada **bimestre é um bairro** que
"amanhece aberto" no mesmo link (colado uma vez no Invertexto, vale o ano todo).
A criança nunca "abre uma atividade nova" — ela **volta ao mundo dela** e descobre
que a ponte para o bairro seguinte, que ela via ao longe desde o primeiro dia,
agora está aberta. A curiosidade puxa o ano para frente: o próximo bairro é a
recompensa por dominar o atual.

- **1 bairro por bimestre** (4 bairros no ano), publicado incrementalmente.
- Cada bairro = 6 a 8 missões (lojas/lugares), cada missão trabalha 1–2
  habilidades BNCC de forma concreta.
- O **motor é construído uma vez** (rua andável, login, save, HUD, painel) e
  reusado o ano todo — o custo de produção cai a cada bairro.

### 2.2 Espiral de revisão embutida na GEOGRAFIA do mundo
A revisão espaçada (spaced review — o conteúdo volta em intervalos crescentes,
que a ciência da aprendizagem aponta como o que fixa de verdade) **não é uma lista
de "revisão"**: ela está desenhada no mapa. Um bairro do 3º bimestre reusa,
naturalmente, a habilidade que a criança aprendeu no 2º — porque o mundo é coeso.

- Exemplo real do projeto: **o Banco reusa a divisão da Confeitaria** (dividir
  reais entre pessoas usa a mesma repartição dos brigadeiros). A criança revisa
  sem perceber que está revisando — é só o mundo funcionando.
- O personagem-cliente que pede numa loja é o **mascote de OUTRA loja** (cameo
  rotativo): o mundo lembra o que já aconteceu, reforçando conexões.
- **Consequência permanente:** a placa consertada FICA consertada, a Dona Bela
  passa a acenar. O mundo guarda a memória do progresso — a criança vê o quanto
  já cresceu, o que sustenta a motivação por meses.

### 2.3 Avaliação diagnóstica INVISÍVEL
Toda missão já grava, por aluno, o que aconteceu: **acertou de primeira, errou e
consertou, quantas tentativas, em qual habilidade**. Isso é avaliação formativa
contínua (no sentido da BNCC: avaliar para ensinar, não para punir) sem prova,
sem folha, sem a criança sentir que está sendo testada. O dado nasce do jogo:
- `acerto()` / `erro()` por missão → mapeia a habilidade BNCC daquela loja.
- Salvo no Firebase em `/mundos/<turma>/<aluno>` (~2 KB: missões, moedas, fase
  do bichinho, erros/acertos por habilidade).
- Como a criança **conserta** o erro dentro do mundo, o professor vê não só "quem
  errou" mas "quem errou e superou sozinho" vs "quem travou de vez" — informação
  que uma prova de X/certo nunca dá.

**Princípio pedagógico:** a melhor avaliação é a que a criança nem percebe que é
avaliação, porque ela está jogando — e ainda assim gera o retrato mais honesto do
que cada um sabe.

---

## 3. MAPA EXEMPLO — 5º ANO MATEMÁTICA (4 bimestres → 4 bairros)
### Tema do mundo: CIDADE (conforme rascunho da IDEIA §3)

A Confeitaria (2º bimestre) **já está construída** — é a implementação de
referência. Os outros três bairros seguem o mesmo motor, só trocando tema,
cenário e dados. Cada objetivo abaixo cita o código BNCC correspondente.

### 🏪 BAIRRO 1 — MERCADO (1º bimestre): Numeração e Operações
Missões concretas: separar mercadorias em caixas, contar estoque, fechar o caixa,
montar combos.
- **EF05MA01** — Sistema de numeração decimal: ler, escrever e ordenar números
  naturais (preços, quantidades de estoque).
- **EF05MA02** — Ler, escrever e ordenar números racionais na forma decimal
  (etiquetas de preço: R$ 3,50).
- **EF05MA07** — Problemas de adição e subtração com naturais (fechar o caixa,
  dar troco simples).
- **EF05MA08** — Problemas de multiplicação e divisão com naturais (combos "3
  pacotes de 4", repartir mercadoria em prateleiras) — modo A-montar e modo A.
- **EF05MA09** — Problemas de contagem/princípio multiplicativo (montar cesta com
  N opções de fruta × M opções de pão).

### 🧁 BAIRRO 2 — CONFEITARIA (2º bimestre): Frações e Divisão *(JÁ PRONTA)*
Missões: repartir doces em pratos iguais, sobras, meio/quarto de bolo.
- **EF05MA03** — Identificar e representar frações (metade, terço, quarto do bolo).
- **EF05MA04** — Frações equivalentes (2 quartos = 1 metade da bandeja).
- **EF05MA05** — Comparar e ordenar racionais (qual prato tem mais).
- **EF05MA11** — Repartições que NÃO dão quociente inteiro: divisão com resto — o
  "Pratinho do Chef" (resto visível; no acerto o Chef "come" a sobra) — modo A
  com `sobra:true`.
- **EF05MA13** — Partilha em partes DESIGUAIS (encomendas diferentes por cliente).

### 🏦 BAIRRO 3 — BANCO (3º bimestre): Decimais, Dinheiro, Porcentagem, Proporção
Missões: montar pilhas de reais, dar troco com centavos, calcular desconto,
proporção de ingredientes. *(Espiral: reusa a divisão da Confeitaria.)*
- **EF05MA06** — Associar 10%, 25%, 50%, 75%, 100% a frações (desconto na loja) —
  liga direto com EF05MA03/04 do bairro anterior.
- **EF05MA07** — Adição e subtração com racionais decimais (somar dinheiro, troco
  com centavos) — modo D (dinheiro).
- **EF05MA08** — Multiplicação e divisão com decimais (parcelar uma conta,
  preço unitário) — modo D.
- **EF05MA10** — Igualdade permanece ao operar dos dois lados (a balança do caixa
  tem que "bater": entrada = saída) — a pilha de moedas que não fecha é o erro
  visível.
- **EF05MA12** — Variação proporcional direta (2 pães custam R$ X, 6 pães custam?)
  — modo B "tot".

### 🏗️ BAIRRO 4 — PARQUE DE OBRAS (4º bimestre): Geometria, Medidas, Estatística
Missões: medir terrenos, montar plantas/planificações, orientar o guindaste por
coordenadas, ler a placa de obras (gráficos). *(Espiral: reusa medidas do Mercado.)*
- **EF05MA14 / EF05MA15** — Localização e movimentação no plano / 1º quadrante do
  plano cartesiano (dirigir o guindaste até a coordenada certa) — encaixa
  perfeitamente com o "andar pelo mundo" que o motor já faz.
- **EF05MA16** — Figuras espaciais e suas planificações (montar a caixa/telhado a
  partir da planta) — modo A-montar.
- **EF05MA17** — Reconhecer, nomear e comparar polígonos (peças da construção).
- **EF05MA19** — Medidas de comprimento, área, massa, tempo, capacidade (medir a
  parede, pesar a carga do caminhão).
- **EF05MA20** — Perímetro e área do terreno (cercar o lote vs. calcular o piso).
- **EF05MA24 / EF05MA25** — Ler e produzir gráficos de colunas/pictóricos e
  fazer pesquisa (a "placa de progresso da obra" é um gráfico vivo).
- *(Opcional, se sobrar espaço na história:)* **EF05MA22 / EF05MA23** — Espaço
  amostral e probabilidade (sorteio do prêmio da inauguração).

**Fechamento anual (dezembro):** final épico da história + certificado do ano, com
os 4 bairros abertos e o bichinho (Docinho) totalmente evoluído — a criança vê o
ano inteiro de aprendizagem materializado num mundo que ela ajudou a construir.

---

## 4. COMO O PROFESSOR USA OS DADOS (painel + intervenção dirigida)

O login por aluno destrava o **Painel do Professor** (modo professor `1275@` dentro
do próprio jogo). Ele transforma dado de jogo em ação de sala. O que o Marcos vê:

### 4.1 Ao vivo, durante a aula
- **Quem está em qual missão** agora (turma inteira em tempo real).
- **Quem empacou:** aluno que errou 2+ vezes na mesma missão e não conseguiu
  consertar — sinaliza para o professor ir até aquele PC AGORA, no momento exato
  da dificuldade (intervenção no ponto certo, que é quando mais funciona).

### 4.2 Relatório acumulado (diagnóstico do ano)
- **Mapa de habilidades por aluno:** quais códigos BNCC cada criança já domina
  (verde), está construindo (amarelo) ou travou (vermelho). Ex.: "Ana domina
  EF05MA03/04 mas empaca em EF05MA11 (divisão com resto)".
- **Mapa da turma por habilidade:** se 18 de 24 alunos travaram em EF05MA12
  (proporção), isso não é problema de aluno — é sinal de **replanejar a aula
  daquela habilidade** para a turma toda.

### 4.3 Da leitura à intervenção dirigida (o ciclo prático)
1. **Ler o painel** antes da aula (5 min): quem está vermelho em quê.
2. **Agrupar por necessidade:** juntar os 4 que travaram em resto de divisão para
   uma mini-oficina com material concreto (tampinhas), enquanto os que já dominam
   avançam no bairro — **atendimento diferenciado sem deixar ninguém para trás**.
3. **Devolver ao jogo:** a criança volta à mesma missão; se agora acerta, o painel
   fica verde — o professor VÊ a intervenção funcionar, com evidência.
4. **Portfólio para o conselho de classe / pais:** o histórico do ano por aluno é
   um retrato concreto do avanço, muito mais rico que uma nota. Serve de evidência
   para a direção sobre o impacto do projeto.

**Regra de ouro do dado:** o painel serve para **ensinar melhor**, nunca para
ranquear ou expor criança. Vermelho no painel = "aqui eu preciso ajudar", não
"este aluno é fraco".

---

## 5. CUIDADOS (tempo de tela, inclusão, equidade)

### 5.1 Tempo de tela
- O Mundo Vivo é **ferramenta de aula, não substituto do professor**. Sugestão:
  sessões de 20–35 min, 1–2x por semana, sempre com fechamento coletivo (o
  professor puxa a discussão do que descobriram — a tela abre a conversa, não a
  encerra).
- O jogo **salva sozinho e a qualquer momento** (Firebase por aluno): não precisa
  "terminar tudo hoje", o que tira a pressão de maratona de tela.
- Alternar com material concreto físico (tampinhas, dinheiro de brinquedo) reforça
  a mesma habilidade fora da tela — o digital e o concreto se somam.

### 5.2 Inclusão — criança sem coordenação fina
- O motor já prevê **tocar no destino OU arrastar** (não exige só arrasto fino):
  a criança que não consegue arrastar pode **tocar** no prato para mandar o doce.
- **Sem tempo/cronômetro** nas missões — nada de pressão motora. A criança age no
  ritmo dela; o mundo espera.
- Alvos grandes (lojas, pratos, caixas) e a **guarda de 280ms** que separa clique
  de arrasto (`MM.tDrop`) evitam que o toque trêmulo seja "engolido".
- No PC o controle é **teclado** (setas), alternativa para quem tem dificuldade
  com mouse/touch.

### 5.3 Inclusão — baixa visão e leitura
- **Toda fala tem voz gravada** (voz Antonio, mp3, nunca TTS robótico): a criança
  que não lê bem, ou enxerga pouco, **ouve** o pedido e a explicação. Nenhuma
  informação essencial é só-texto.
- Regra sagrada do projeto: **sem sobreposição de texto/imagem** em nenhuma tela
  ou resolução, e **objetos sempre contidos no recipiente** — legibilidade
  garantida por QA (screenshots das cenas extremas).
- Cores fortes, contraste alto, ícones grandes. *Cuidado a acompanhar:* conferir
  que informação nunca dependa SÓ de cor (para daltonismo) — o entristecer do
  prato usa carinha 😞 + tremida, não só cor, o que já ajuda.
- **Melhoria futura sugerida:** modo de fonte maior / alto contraste opcional para
  baixa visão severa (registrar como possível fatia).

### 5.4 Equidade (escola pública)
- **Roda em PC velho e em celular** (ES5, 1 HTML, sem framework/CDN/WebGL): nenhum
  aluno fica de fora por causa de máquina fraca ou celular antigo. Isso é equidade
  de acesso na prática.
- **Um único link** (Invertexto), sem instalação, sem app, sem loja — funciona em
  qualquer máquina da escola e na casa da criança.
- **Estepe offline** (localStorage + senha de save tipo `PÃO-42`): se a internet da
  escola cair, ninguém perde o progresso — o código no caderno é o pneu reserva.
- **Privacidade:** só primeiro nome, sem foto, sem e-mail, nada além do progresso
  do jogo. Login por 3 figurinhas (proteção de coleguinha, não vigilância).
- **Todos os alunos com o mesmo mundo:** o jogo se adapta ao ritmo de cada um (quem
  domina avança, quem trava recebe dica na 2ª falha), então a diferença de partida
  entre as crianças não vira exclusão — vira trilha personalizada dentro do mesmo
  mundo. Ninguém é separado em "turma dos fracos".

---

### FECHAMENTO
O Mundo Vivo não é "atividade animada": é um ambiente construcionista onde a
criança da escola pública **vive** a BNCC em vez de decorá-la, o professor ganha
avaliação diagnóstica contínua sem prova, e cada aluno — inclusive quem tem menos
coordenação, menos visão ou máquina mais fraca — tem o mesmo mundo pela frente.
É exatamente o "fora da caixa" com fundamento que o Marcos quer levar à direção.
