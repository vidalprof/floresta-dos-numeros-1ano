# 🚀 PLANO FORA DA CAIXA — Mundo Vivo (sumário executivo)
## Marcos + Claude · jul/2026 · Síntese da reunião de 5 especialistas
## Pareceres completos: pasta `_plano/` (interatividades, pedagogia, engajamento, produção, destaque)

> A tese numa frase: **as crianças não respondem exercícios — elas VIVEM num
> mundo que lembra delas, e a matéria é a ferramenta que usam para cuidar
> desse mundo.** Errar dá consequência visível (não X vermelho); acertar vira
> descoberta; e toda semana o mundo guardou algo novo para elas.

================================================================
## 0. DECISÕES DO MARCOS (o plano trava sem elas)
================================================================
1. **Top-down vira o interior oficial?** O protótipo `/proto/` (estilo Monkey
   Mart) substitui as cenas de balcão do mundo, ou fica como modo especial?
   → Recomendação: decidir DEPOIS de levar os dois para a turma (teste A/B
   real: metade joga cada um, observar qual prende mais).
2. **Firebase:** liberar no console as Rules do nó `mundos` (leitura/escrita)
   e mandar a lista de nomes das turmas — destrava login + save + painel.
3. **Tema do mundo 2** (prova do molde barato): mar/piratas? — e o mapa BNCC
   dos bimestres para os bairros do ano.

================================================================
## 1. O QUE JÁ ESTÁ NO AR (patrimônio construído)
================================================================
- **Atividade premium** Confeitaria/Divisão 5º ano (revisada: vozes com
  "vezes/dividido por/igual a", enunciados completos).
- **Mundo Vivo** (`/mundo/`): rua andável, 13 lojas com placa, clima
  dia/noite/chuva/trovoada/neve com luzes, missões concretas sem
  pergunta-e-resposta, fila de clientes, diorama nos interiores.
- **Protótipo top-down** (`/proto/`): loja isométrica, chef em 4 direções com
  ciclo de 4 quadros, clientes que entram/sentam/pedem/vão embora em ondas,
  arrastar doces aos pratos, partida completa com festa.
- **Prontos para integrar:** login por figurinhas + save Firebase (spec+código),
  ovo/bichinho Docinho (spec+código+4 cartelas de arte).
- **Moldes:** ESPINHA (produção à prova de erros), MOTOR (micromundos),
  pipelines de arte (Gemini, centavos) e voz (Antonio, lote).

================================================================
## 2. AS REGRAS DE OURO CONSOLIDADAS (dos 5 pareceres)
================================================================
- **Concretude obrigatória:** a criança MOVE o conceito (reparte, pesa, paga);
  a conta aparece DEPOIS da ação, como descoberta. Nada de quiz disfarçado.
- **Anti-repetição:** nunca a mesma mecânica (o mesmo VERBO) em fases
  vizinhas — rodízio pelas 5 famílias do catálogo (33 mecânicas em
  `_plano/plano_interatividades.md`).
- **Erro = consequência visível** que a criança conserta, com escada de ajuda.
- **Engajamento saudável:** o gatilho é "o mundo guardou algo pra você",
  NUNCA medo/pressão. Sem ranking humilhante, sem punir quem faltou, sem
  cronômetro sufocante, Docinho evolui por MARCO de aprendizagem (nunca por
  assiduidade) e não adoece. Bússola: se depende de MEDO, está errado.
- **Equidade:** roda no PC velho e no celular, 1 link, sem instalação, voz
  gravada em tudo, tocar OU arrastar, só primeiro nome.
- **Modelos:** forte cria motor/mecânica nova; Opus produz em série com a
  ESPINHA; travou 2x ou saiu malfeito → elevar o modelo (regra permanente).

================================================================
## 3. ROADMAP POR FATIAS (detalhe: `_plano/plano_producao.md`)
================================================================
| # | Fatia | Modelo | Trava |
|---|-------|--------|-------|
| 0 | **Levar `/mundo/` à turma ESTA SEMANA** (validação real) | nenhum | só coragem |
| 1 | Decisão top-down (teste A/B com as crianças) | — | Marcos |
| 2 | Login figurinhas + save Firebase + ovo Docinho | forte (integração) | Rules + lista de turmas |
| 3 | Memória turbinada + 2-3 mecânicas novas do catálogo | forte 1x, depois Opus | — |
| 4 | Painel do professor ao vivo (clone do `_painel` existente) | Opus | Fatia 2 |
| 5 | Mundo 2: mar/piratas (prova do molde barato) | Opus | tema + BNCC |
| 6 | Bairros por bimestre + história com decisões | forte 1x (motor de história) | BNCC bimestres |

Se a cota apertar: ordem de valor = 2 → 4 → 5 → 3 → 6 (a 1 espera o A/B).

================================================================
## 4. O ANO PEDAGÓGICO (detalhe: `_plano/plano_pedagogia.md`)
================================================================
- 4 bimestres = 4 bairros que "amanhecem abertos" no MESMO link.
- 5º ano Cidade: Mercado (numeração/operações) → Confeitaria (✔ pronta,
  divisão) → Banco (decimais/dinheiro) → Parque de Obras (geometria/medidas),
  com códigos EF05MA mapeados por bairro.
- **Avaliação invisível:** o jogo grava acerto/erro/tentativa por habilidade
  por aluno — o painel mostra quem empacou em quê, para intervenção dirigida.
  Dado serve para ENSINAR, nunca para ranquear.
- Espiral de revisão embutida na geografia (o Banco reusa a divisão da
  Confeitaria).

================================================================
## 5. O "QUERO VOLTAR AMANHÃ" (detalhe: `_plano/plano_engajamento.md`)
================================================================
- Loop da semana: chega → o mundo LEMBRA dela → algo mudou → joga →
  progresso visível → gancho trancado pra próxima aula.
- Sistemas: Docinho por marcos, álbum de figurinhas, Bazar 100% cosmético
  (roupinhas/decoração), eventos que ESPERAM quem faltou, o bairro
  visível-mas-trancado ao longe.
- Rituais de aula: "O Mundo Acorda" (abertura, 1 min) e "Até Amanhã!"
  (senha de save no caderno, entardecer).
- 11 surpresas baratas prontas para entrar (lista no parecer, marcadas
  [JÁ DÁ] vs [PÓS-SAVE]).

================================================================
## 6. O DESTAQUE DO MARCOS (detalhe: `_plano/plano_destaque.md`)
================================================================
- Narrativa de 1 minuto (dor→virada→prova) pronta para direção e colegas.
- Demonstração de 10 min na sala dos professores (roteiro no parecer).
- Mostra para as famílias: as CRIANÇAS apresentam seus mundos.
- Evidência sem burocracia: diagnóstico antes/depois + falas das crianças +
  dados do painel.
- Caminhos reais de reconhecimento: feiras municipais, Prêmio Educador
  Nota 10, Professores do Brasil, redes docentes de SC.
- Cuidados: autorização da direção, imagem das crianças, LGPD escolar.

================================================================
## 7. PRIMEIRA SEMANA (concreto, começa já)
================================================================
1. Levar `/mundo/` para a turma (Fatia 0) — observar 30 min de uso real.
2. Marcos: Rules do Firebase + lista de turmas (destrava Fatia 2).
3. Anotar reações das crianças (o que amaram, onde empacaram) e trazer — 
   vira o backlog REAL da próxima sessão de produção.

> Registrado pelo coordenador (modelo forte) com base nos 5 pareceres.
> Este documento é o índice; a verdade detalhada mora em `_plano/`.
