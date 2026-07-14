# 🏗️ ROADMAP DE PRODUÇÃO — MUNDO VIVO (Arquiteto)
Fonte verificada no repo em 2026-07-14. Ordena as 6 fatias que o Marcos pediu, com
entregável, pré-requisitos, modelo (política ESPINHA §7), sessões e gate de aceite.

---
## ESTADO REAL VERIFICADO (não é promessa — é o que existe no disco hoje)

- **Motor lateral (referência):** `_pub_confeitaria/mundo/index.html` (2.9 MB). Rua andável,
  clima, NPCs, 4 modos de missão (A/A2/A-montar/B/D), plaquinha, badges, voz gravada.
  **Save = só localStorage, 1 slot, expira 70 min.** SEM login, SEM Firebase, SEM ovo integrado.
- **Protótipo top-down** `_pub_confeitaria/proto/index.html` (328 KB): "A Lojinha v2".
  **ES5 limpo** (0 const/let/arrow), 43 sprites, chef anda 4 direções, clientes
  entram/sentam/pedem/saem, ondas=fases, colisão macia. **A matemática AINDA NÃO está
  ligada** (grep: `conta`×4, `quant`×1) — hoje é loop de atendimento, não micromundo concreto.
- **Firebase:** é **Realtime Database** `atividades-educativas-16860-default-rtdb.firebaseio.com`,
  **já provado** no jogo "Aventura das Direções" `_pub_aventura/index.html` (REST via
  XMLHttpRequest, verbos GET/POST/PUT). **CORREÇÃO:** NÃO é o confeitaria premium
  `_pub_confeitaria/index.html` — esse arquivo não tem rede nenhuma (0 fetch, 0 XHR, 0 firebaseio).
  O RTDB **já é lido** pelo `_painel/index.html` (painel da "Aventura das Direcoes", via XHR →
  base de clone pronta p/ Fatia 4).
- **Ovo Docinho:** ARTE pronta em `_novo/` (`cartela-3-ovos.png`, `cartela-docinho-rosa/verde/
  azul-estagios.png`). O **CÓDIGO** login-figurinhas + save RTDB + ovo-evolui **não está
  integrado no motor** — "pronto" = specs no histórico + arte + caminho Firebase provado, NÃO um
  drop-in. Integrar num HTML de 3 MB tocando boot/save = **mexer no motor → modelo forte**.

## LEITURA DE MODELOS (ESPINHA §7 / IDEIA §6) — regra que rege todo o orçamento
- **FORTE (Fable/modelo alto):** motor, física/câmera, login/save novos, mecânica que não
  existe nos 4 modos, história/ramificação. É **CRIAÇÃO** → cota alta (arquivo 3 MB, geração de
  imagem, ciclos de QA, 2 hipóteses e escala).
- **Opus 4.8 esforço alto:** **PRODUÇÃO EM SÉRIE** sobre motor pronto — clonar, trocar
  tema/dados/áudio/cores, rodar QA, publicar. Cota **muito menor** por sessão.
- **Regra de custo honesta:** 1 sessão de CRIAÇÃO ≈ 3–5× a cota de 1 sessão de PRODUÇÃO
  (iteração em base64 de MB + imagens Gemini + QA repetido). Por isso concentro o forte no
  mínimo (Fatias 1–2 e a 1ª mecânica de cada tipo) e deixo o barato rodar o resto.

---
# FATIA 1 — FECHAR O PROTÓTIPO TOP-DOWN COMO MOTOR OFICIAL DE INTERIORES
**(esta fatia é, antes de tudo, uma DECISÃO do Marcos que trava as outras)**

**A pergunta que trava tudo:** o top-down **substitui as cenas de balcão** (interiores
`mmCena*` do mundo lateral) ou fica como **sala-bônus/arcade** ao lado do motor de missões?
Hoje são dois motores separados; não dá pra ter os dois como "interior padrão" sem inchar.

### Ramo A — DECISÃO = "top-down vira o interior oficial" (recomendado só se o Marcos amar o feel)
- **Entregável:** o loop de atendimento top-down com **a matemática concreta ligada** — o
  pedido do cliente É uma ação de micromundo (repartir/agrupar/dar troco *manipulando quantidade*,
  nunca pergunta-e-resposta), erro = consequência visível, plaquinha só depois da ação; game-feel
  canônico (§3) portado; 1 interior de exemplo plugado no motor do mundo.
- **Pré-requisitos:** decisão do Marcos (ver abaixo); proto atual (existe); receita §3 do motor.
- **Modelo:** **FORTE** — é motor novo + casar dois motores (gatilho §7 "tocar função do motor").
- **Sessões:** **4–7** (é o item mais caro do roadmap).
- **Cota:** **MUITO ALTA** (criação pura: arquivo grande, sprites, QA retrato+paisagem repetido).
- **Gate de aceite:** um cliente senta, o pedido dele é resolvido **manipulando quantidade**
  (não digitando resposta); errar de propósito gera consequência no salão e a criança conserta;
  ES5 limpo (`node --check`), zero `pageerror` em 390×780 E paisagem; game-feel bate com §3.

### Ramo B — DECISÃO = "top-down fica como sala-bônus / arcade"
- **Entregável:** proto congelado como mini-jogo opcional (1 porta no mundo lateral leva a ele),
  motor de missões segue o das cenas de balcão. Documentar a decisão na ESPINHA §4.
- **Modelo:** **Opus** (só empacotar/plugar, sem tocar motor de missões). **Sessões:** **1–2**.
- **Cota:** BAIXA. **Gate:** abre pela porta, fecha e volta pro mundo sem quebrar save.

> **SEM O MARCOS, ISTO NÃO ANDA.** É decisão de arquitetura, não técnica — e ela define se as
> Fatias 3/5/6 desenham interiores em top-down ou em balcão. **Recomendo decidir com um teste A/B
> de feel (1 sessão) antes de investir as 4–7 sessões do Ramo A.**

---
# FATIA 2 — LOGIN POR FIGURINHAS + SAVE FIREBASE + OVO DOCINHO
**(base de tudo: sem isto não há progressão anual, painel, história nem bairros)**

- **Entregável:** tela de entrada sem digitação (turma → nome/avatar → 3 figurinhas);
  save por aluno em **RTDB `/mundos/<turma>/<aluno>`** (~2 KB: missões, moedas, fase do ovo),
  grava sozinho ao fim de cada missão e **volta em qualquer PC**; **ovo (3 cores) que choca e
  evolui entre sessões** (arte de `_novo/` já existe); **estepe offline**: localStorage + senha
  de save `PÃO-42` quando a rede cai.
- **Pré-requisitos:** motor de referência (existe); caminho REST provado (existe); arte do ovo
  (existe); **[TRAVA MARCOS]** regras do RTDB no console + lista de turmas (ver "O que trava").
- **Modelo:** **FORTE** — login/save novos + mexer no boot/persistência do motor (§7).
- **Sessões:** **3–5**. **Cota:** **ALTA** (criação; integrar em 3 MB + ciclo de rede/QA).
- **Gate de aceite:** aluno loga com 3 figurinhas; fecha e reabre **em outra máquina** e o mundo
  dele (missões+moedas+ovo) está lá; ovo escolhido no dia 1 choca e evolui na semana seguinte;
  desligando a rede, aparece a senha de estepe e o jogo continua no localStorage; zero `pageerror`.

---
# FATIA 3 — MEMÓRIA TURBINADA + 2–3 MECÂNICAS NOVAS NA CONFEITARIA
**(engorda o mundo já existente enquanto o save assenta)**

- **Entregável:** o mini-jogo de memória (`j1`) turbinado (game-feel, voz, recompensa que
  entra na economia) + **2–3 mecânicas novas do catálogo** plugadas em missões da Confeitaria,
  sempre concretas (a criança manipula, não responde), nunca repetindo a mecânica da fase vizinha.
- **Pré-requisitos:** motor (existe); pipeline de áudio (`_lote_falas.json` → `gerar-audio.yml`).
- **Modelo:** **MISTO.** Se a mecânica cabe nos 4 modos (A/A2/A-montar/B/D) = só dados novos →
  **Opus série**. Se é renderer **inédito** (fora dos 4 modos) = **FORTE** para construir 1×, depois
  Opus popula. Memória turbinada, por tocar um jogo próprio, tende a **forte leve**.
- **Sessões:** **2–4** (1 forte p/ cada renderer inédito + 1–2 Opus de conteúdo/áudio/QA).
- **Cota:** **MÉDIA** (mistura criação pontual + produção). **Gate de aceite:** cada mecânica abre
  cena válida; erro = consequência visível **antes** de qualquer dica; plaquinha só após a ação;
  **zero fala muda** (áudio gerado p/ enunciado E explicação); screenshots das cenas extremas
  (30 itens, 7 grupos) sem vazar da bandeja nem sobrepor texto; `node --check` limpo.

---
# FATIA 4 — PAINEL DO PROFESSOR (ao vivo + relatório anual)

- **Entregável:** painel que lê o **mesmo RTDB** que a Fatia 2 grava — turma ao vivo (quem está
  em qual missão, quem empacou), habilidades por aluno e **relatório/diagnóstico anual**.
- **Pré-requisitos:** **Fatia 2 gravando dados** (sem escrita não há o que ler); `_painel/index.html`
  existente como **base de clone** (já lê esse RTDB); regra de leitura no console (Marcos).
- **Modelo:** **Opus** predominante (clonar o painel existente + adaptar a leitura `/mundos/...`).
  A visão "ao vivo" (polling leve) é ajuste, não motor. **Sessões:** **2–3**. **Cota:** **MÉDIA-BAIXA**.
- **Gate de aceite:** abre a turma e mostra, do RTDB real, quem está onde + empacados + relatório;
  roda em PC velho (ES5, sem CDN); **não expõe nada além do primeiro nome** (privacidade escola pública).

---
# FATIA 5 — MUNDO NOVO TEMA MAR/PIRATAS (a prova de que o molde é barato)

- **Entregável:** um 2º mundo completo (tema/cenário/interiores/paleta **DIFERENTES** da
  Confeitaria — regra sagrada), clonando o motor da referência e trocando só DADOS: fachadas,
  mascotes, interiores, missões, áudio. Prova que produzir mundo novo é **produção**, não criação.
- **Pré-requisitos:** motor de referência (existe). **[TRAVA MARCOS]** confirmar tema mar/piratas,
  nome do mundo/mascote e **ano/disciplina → mapa BNCC** (chapéu professor, ESPINHA P1).
- **Modelo:** **Opus série** (checklist MOTOR §7). O caro aqui é o **front-load de arte** (cartelas
  Gemini de fachadas/mascotes/interiores), não código. Risco baixo (motor pronto).
- **Sessões:** **3–5** (a maioria em geração/gravação de imagem + QA + publicação).
- **Cota:** **ALTA por causa da ARTE** (geração de imagem), mas **baixo risco de escalada**.
- **Gate de aceite:** `diff` contra a referência toca **só dados/tema** (nenhuma função do motor);
  paleta/fachadas/interiores visivelmente distintos da Confeitaria; missões concretas; zero fala
  muda; QA §5 completo; publicado com `build=built`.

---
# FATIA 6 — BAIRROS POR BIMESTRE (mundo multi-bairro incremental)

- **Entregável:** o bairro do bimestre "amanhece aberto" no MESMO link; save atravessa bimestres;
  espiral (revisão espaçada) embutida na geografia; história com decisões por ato.
- **Pré-requisitos:** **Fatias 2 (save anual) + 4** prontas; história/ramificação depende de save
  persistente. **[TRAVA MARCOS]** mapa BNCC por bimestre + as decisões da história (pedagógico).
- **Modelo:** **MISTO.** Cada bairro/missão = **Opus série** (barato). A **história com
  ramificação** (1ª vez) = **FORTE** (mecânica nova, ESPINHA §8 item 3), depois Opus reusa o molde.
- **Sessões:** **contínuo** — ~2–3 por bairro × 4 bimestres (+1 forte inicial p/ o motor de história).
- **Cota:** **DECRESCENTE** — 1º bairro médio-alta (motor de história), demais baixas (série).
- **Gate de aceite:** bairro novo abre no link existente sem quebrar saves; o caminho escolhido na
  história **sobrevive entre sessões**; a revisão do bairro anterior aparece como consequência
  natural (não como "atividade de revisão"); dezembro tem final + certificado anual.

---
## 🔴 O QUE TRAVA SEM O MARCOS (decisões/ações que só ele faz)

1. **Fatia 1 — decisão arquitetural:** top-down **substitui** o balcão ou é **bônus**? Trava o
   desenho de interiores de TODAS as fatias seguintes. (Recomendo teste A/B de feel antes.)
2. **Fatia 2 — Firebase console (Claude não acessa o console):** definir as **Rules** do RTDB para
   `/mundos/<turma>/<aluno>` (quem lê/grava), senão ou trava por permissão ou fica aberto demais.
   É ação manual do Marcos no console do projeto `atividades-educativas-16860`.
3. **Fatias 2/4 — lista de turmas/alunos:** dado do Marcos (só primeiro nome; sem foto/e-mail).
4. **Fatia 5 — decisões de tema:** confirmar mar/piratas, nome do mundo/mascote, ano/disciplina.
   Regra sagrada: tema/paleta DIFERENTES do já publicado.
5. **Fatias 5/6 — mapa BNCC (P1, chapéu professor):** habilidades do ano/bimestre → missão → modo.
   Decisão pedagógica; sem ela não se escreve `desafios`.
6. **Fatia 6 — as ramificações da história:** que decisão muda o quê no mundo (pedagógico).

## 💰 ORÇAMENTO DE COTA — RESUMO HONESTO (criação vs produção)

| Fatia | Natureza | Modelo | Sessões | Cota relativa | Trava do Marcos |
|---|---|---|---|---|---|
| 1 top-down oficial (Ramo A) | CRIAÇÃO | Forte | 4–7 | ●●●●● muito alta | Decisão arquitetural |
| 1 top-down bônus (Ramo B) | produção | Opus | 1–2 | ● baixa | (mesma decisão) |
| 2 login+Firebase+ovo | CRIAÇÃO | Forte | 3–5 | ●●●● alta | Rules RTDB + lista turma |
| 3 memória + mecânicas | misto | Forte→Opus | 2–4 | ●●● média | — |
| 4 painel professor | produção | Opus | 2–3 | ●● média-baixa | Fatia 2 + regra leitura |
| 5 mundo mar/piratas | produção (arte pesada) | Opus | 3–5 | ●●●● alta (imagem) | Tema + BNCC |
| 6 bairros/bimestre | misto (1º caro) | Forte→Opus | 2–3/bairro | ●●→● decrescente | BNCC + história |

**Leitura de fundo:** o gasto forte (caro) concentra-se em **Fatias 1–2** (fundação) e nas
*primeiras* mecânicas/história. Depois disso o custo por entrega DESPENCA — é exatamente o modelo
"motor único, bairros baratos" da IDEIA §6. Se a cota apertar, a ordem que **maximiza valor por
real gasto** é: **2 (fundação) → 4 (painel, barato, vira "vitrine" p/ a escola) → 5 (prova o
molde barato) → 3 → 6**, deixando a Fatia 1-Ramo A (a mais cara) para depois de o Marcos confirmar
que quer o top-down como interior oficial. Sem essa confirmação, **não gastar** as 4–7 sessões dela.
