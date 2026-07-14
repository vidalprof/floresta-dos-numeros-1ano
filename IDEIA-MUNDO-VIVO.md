# 🌍 MUNDO VIVO — o game-mundo anual (ideia registrada)
## Marcos + Claude — jul/2026
## STATUS: ideia aprovada para registro. NÃO é manual de produção ainda.
## Piloto aguarda 2 decisões do Marcos: (1) ano/disciplina, (2) tema do mundo.

================================================================
## 1. A TESE (por que isso revoluciona)
================================================================
Hoje cada atividade é uma ilha solta com link próprio. O Mundo Vivo inverte:
**cada ano/série ganha UM único mundo vivo, e o currículo inteiro do ano É o
mapa desse mundo.** A criança não "abre uma atividade" — ela **volta ao mundo
dela**, o ano letivo inteiro, sempre pelo mesmo link (colado 1x no Invertexto).

O salto pedagógico: sair do "responder atividades" para **VIVER o conteúdo** —
o conteúdo deixa de ser a pergunta e vira a FERRAMENTA que a criança usa para
resolver um mundo que reage a ela (micromundos, Papert). Errar não dá X
vermelho: dá **consequência no mundo**, e a criança se corrige para consertar
o mundo.

As 3 ideias-mãe que o Marcos aprovou (a 4ª, missão em dupla, foi descartada —
a escola tem um PC por aluno):
1. **MICROMUNDOS** — o mundo que reage (aprender por consequência);
2. **HISTÓRIA QUE OBEDECE** — decisões da criança mudam o caminho;
3. **PROGRESSÃO QUE ATRAVESSA O ANO** — o mundo/bichinho dela cresce semana
   a semana (login + save; senha de estepe).

(Nota: a frente "BNCC Computação / 3 eixos" fica DE FORA por enquanto —
decisão do Marcos, ver mais pra frente.)

================================================================
## 2. A EXPERIÊNCIA DA CRIANÇA (os primeiros 5 minutos)
================================================================
- **Tela-título de videogame:** logo pulsando, mascote passeando ao fundo,
  faíscas, "▶ COMEÇAR" piscando, plim-plim de game.
- **Login de criança** (ver §4) e a escolha do **OVO** (3 cores) — que vai
  chocar na 2ª semana e evoluir o ano todo.
- **Ela cai NUMA RUA, não num menu:** vila viva vista de lado (parallax de
  2-3 camadas: céu/nuvens, montanhas, casas), fumaça na chaminé, passarinho
  cruzando. **Ela ANDA:** segura a setinha/dedo e o mascote caminha, câmera
  acompanhando. O mundo é um LUGAR.
- **Personagens com desejo:** NPCs com balão "❗ Me ajuda!" — cada missão é o
  pedido de alguém ("minha balança quebrou, pesa os pães pra mim?"), narrado
  na voz Antonio. Entrar pela porta = a missão (micromundo concreto: pesar,
  repartir, dar troco, montar, plantar…).
- **O mundo LEMBRA:** missão feita → a placa consertada FICA consertada; a
  Dona Bela passa a acenar; 3 missões → a ponte reconstruída ABRE o bairro
  seguinte (visível ao longe desde o dia 1 — curiosidade puxando).
- **HUD de game:** moedas (tilintam voando até a mochila), coleção, o ovo.
- **Fim da aula:** senha de save (`PÃO-42`) numa plaquinha para o caderno
  (estepe do login — ver §4).

### Os 6 pilares que fazem ser GAME (e não "atividade animada")
1. Espaço, não menu — os desafios são LUGARES;
2. Consequência visível e PERMANENTE no cenário;
3. Personagens com desejo (missão = pedido de alguém);
4. Economia e coleção (moedas, mochila, bichinho que evolui);
5. Game feel (parallax, partículas, squash, sons, câmera);
6. O conteúdo é a ferramenta — a "matéria" fica invisível dentro da vida
   do mundo.

================================================================
## 3. UM MUNDO POR ANO — o currículo como mapa
================================================================
- **Bairros/regiões = unidades do ano** (ex.: 5º ano matemática na "Cidade":
  Mercado = numeração/operações; Confeitaria = frações/divisão; Banco =
  decimais/dinheiro/porcentagem; Parque de Obras = geometria/medidas/gráficos).
- **Publicação incremental no MESMO repo/link:** o bairro do bimestre novo
  "amanhece aberto" — o link do Invertexto vale o ano inteiro.
- **História com espinha dorsal anual:** cada bimestre é um ato com decisões;
  dezembro tem o final épico + certificado anual.
- **Espiral embutida na geografia:** o Banco reusa a divisão da Confeitaria
  (revisão espaçada como consequência natural do mundo).
- Rascunho de temas por ano (a validar): 1º Fazendinha · 2º Floresta
  Encantada · 3º Vila dos Ofícios · 4º Expedição · 5º Cidade · 6º Estação
  Científica. Vale o mesmo desenho para Português (ex.: Biblioteca Viva).

================================================================
## 4. LOGIN DE ALUNO + SAVE (exigência do Marcos)
================================================================
- **Tela de entrada sem digitação:** toca na TURMA → toca no NOME/avatar →
  "senha de criança" = sequência de 3 figurinhas escolhida no 1º dia
  (proteção de coleguinha, não segurança de banco).
- **Save por aluno no Firebase** (mesmo Firebase já provado nas provas:
  projeto `atividades-educativas-16860`): caminho `/mundos/<turma>/<aluno>`,
  save pequeno (~2 KB: missões, moedas, fase do bichinho). Salva sozinho ao
  fim de cada missão. A criança senta em QUALQUER PC e o mundo dela está lá.
- **Estepe offline:** localStorage + **senha de save** (`PÃO-42`) exibida se
  a rede falhar. O código no caderno é o pneu reserva, não o sistema.
- **Lista da turma:** cadastrada 1x pelo professor no modo professor (`1275@`)
  dentro do próprio jogo, salva no Firebase para todas as máquinas.
- **Privacidade (escola pública):** só primeiro nome; sem foto/e-mail; nada
  além do progresso do jogo.
- **Bônus que o login destrava — PAINEL DO PROFESSOR ao vivo:** a turma
  inteira em tempo real (quem está em qual missão, habilidades, quem empacou),
  além do relatório/diagnóstico acumulado do ano.

================================================================
## 5. TECNOLOGIA (o dev garante: roda no PC velho)
================================================================
Tudo dentro das regras sagradas dos manuais (ES5, 1 HTML, sem CDN, voz
Antonio embutida, emoji ≤ 6.0, auditores antes de publicar):
- Parallax = 2-3 imagens com `transform` em velocidades diferentes;
- Andar = deslizar o cenário (translateX) + sprite do mascote (2-3 poses);
- Consequência permanente = trocar imagem por estado salvo;
- Partículas/confete/sons = os que já temos (Web Audio sintetizado);
- Firebase via REST (já provado na rede da escola); áudio em pasta `audio/`;
- Zero WebGL, zero framework. O que muda é DIREÇÃO DE ARTE e DESIGN DE
  MUNDO, não a tecnologia.

================================================================
## 6. PRODUÇÃO — como "bastante conteúdo" vira viável
================================================================
O mundo NÃO se constrói de uma vez. Nasce por fatias, cada uma do tamanho
de uma Confeitaria (que produzimos em dias):
- **FASE 0 — FATIA VERTICAL (o teste):** UMA rua com 2 missões completas +
  andar + ovo + login/save + 1 consequência permanente. Prova toda a
  experiência em miniatura; vai para uma turma real e observamos.
- **FASE 1 — 1º BAIRRO (1º bimestre):** ~6-8 missões + a história do ato 1.
  Cada missão é um MÓDULO (molde de mecânica + conteúdo), reusando o motor.
- **FASES 2-4:** um bairro por bimestre, publicado incrementalmente.
- **MOTOR ÚNICO:** mapa andável, login, save, HUD, consequências e painel são
  construídos UMA vez (na fatia) e reusados o ano todo — o custo por bairro
  cai a cada fase. Imagens 3D Gemini em cartelas (front-load por bairro).
- **Auditores/QA:** os mesmos do padrão premium + novos checks que a
  experiência exigir (regra "todo erro vira barreira").

================================================================
## 7. DECISÕES PENDENTES (para iniciar o piloto)
================================================================
1. **Ano e disciplina** do piloto (define o conteúdo das 2 missões da fatia);
2. **Tema do mundo** (vila/fazenda/cidade/floresta/praia… — ou o Marcos dá o
   ano e o Claude propõe o tema com os chapéus).
3. (Depois, com o piloto validado: nomes do mundo/mascote, lista de turmas.)

> Registrado como IDEIA. Vira produção quando o Marcos disser "vamos" com as
> decisões acima. Nada disso altera os manuais de produção atuais.
