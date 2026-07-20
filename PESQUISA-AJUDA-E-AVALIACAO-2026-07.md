# 🔎 PESQUISA — Botão de ajuda, aprendizado real e AVALIAÇÃO DESCRITIVA (jul/2026)

> Pergunta do Marcos: (1) o botão de instruções "?" é a melhor maneira? (2) a atividade
> está adequada a um aprendizado DE VERDADE? (3) e a avaliação no Firebase — descritiva,
> da atividade ou do que ele quiser, que possa VIRAR NOTA. Pesquisa feita na web
> (fontes no fim) + cruzada com MODELO-APRENDIZAGEM-EDUCAVERSO.md.

## 1. O botão "?" — o que a evidência diz

- **Alunos usam MAL botões de ajuda** (Aleven & Koedinger, CMU, logs reais): ~72% das
  buscas de ajuda são improdutivas — ou "hint abuse" (clicar até sair resposta) ou
  **"help avoidance"** (quem mais precisa NÃO clica). Botão sozinho não resolve.
- **"Gaming the system"** (Baker et al.): quem explora a ajuda pra avançar sem pensar
  aprende só ~2/3 do normal. A dica NUNCA pode entregar a resposta do item avaliado.
- **On-demand vs proativa** (Razzaq & Heffernan; linha Hint Factory): sem vencedor
  absoluto; a literatura converge no **HÍBRIDO** — ajuda proativa disparada por
  DETECÇÃO de dificuldade (erros/tempo parado) + botão como rede de segurança.
- **Tutoria contingente** (Wood/Bruner): aumentar a ajuda após falha, diminuir após
  sucesso. Nosso andaime (1º erro pergunta → 2º erro ensina o gesto) é EXATAMENTE isso.
- **Crianças 6–9 não leem instruções** (NN/g, replicado por anos): instruções curtas,
  no momento do uso, com ícone/demonstração. **Sesame Workshop**: narração em VOZ para
  todo texto; demonstração visual supera texto nessa idade.
- **Veredito:** o "?" está certo como REDE DE SEGURANÇA (uso legítimo: "o que eu tinha
  que fazer mesmo?"), e o andaime proativo é o mecanismo principal — combinação
  defendida pela literatura. **Melhorias mapeadas:** (a) o "?" deve FALAR e MOSTRAR
  (voz + demonstração animada), não só texto; (b) disparar dica também por
  INATIVIDADE (parada ~20s = help avoidance detectado); (c) anti-gaming: a dica dá o
  MÉTODO, nunca o resultado; (d) 1ª missão = tutorial integrado (aprender jogando).

## 2. Aprendizado real — posição honesta

A fase agrupar cobre bem: CPA (concreto→pictórico→abstrato), falha produtiva (Kapur),
self-explanation ("por que ELA tombou?" — Chi), institucionalização (Brousseau — a
conferência contada + nomeação "é MULTIPLICAR"), integração intrínseca (Habgood),
BNCC EF03MA07 (parcelas iguais, estratégias múltiplas: 3×4 E 2×6 vencem) + toca
EF03MA08 (repartição) e contagem de 4 em 4. **Mas 1 fase 1 vez ≠ domínio**: fixação
exige repetição espaçada (Leitner já embutido, faltam as missões de retorno),
variação (Dienes: ≥2 mecânicas por objetivo) e transferência (problema NOVO).
A régua de sucesso continua: **transferência + retenção, nunca engajamento**.

## 3. Stealth assessment → AVALIAÇÃO DESCRITIVA que vira NOTA (o desenho)

- **Stealth assessment (Shute/FSU, Evidence-Centered Design):** competência → evidência
  observável → tarefa. Validado (ex.: Physics Playground, N=263, correlação com teste
  externo). A telemetria só vale se o indicador nasce COM a mecânica.
- **NOSSO OURO ESCONDIDO:** o andaime gradual já É uma régua de autonomia:
  **acertou sem ajuda** > **acertou após pergunta reflexiva** > **acertou após o gesto
  ensinado** > **não concluiu**. Isso mapeia direto nos níveis brasileiros
  **Consolidado / Em desenvolvimento / Iniciando** (rubrica BNCC, Movimento pela Base).
- **Base legal (LDB art. 24, V, "a"):** avaliação "contínua e cumulativa, com
  prevalência dos aspectos QUALITATIVOS sobre os quantitativos" — o parecer descritivo
  é a forma MAIS alinhada à lei; a nota é que se justifica a partir dele.
- **Conversão defensável em nota:** rubrica com descritores (não advérbios vagos);
  níveis → faixas numéricas definidas ANTES (tabela fixa da escola); parecer = texto
  que CITA as evidências. Auditável: evidência → nível → nota.
- **Furo do mercado:** os geradores de parecer por IA existentes partem de IMPRESSÕES
  digitadas, não de dados observados → texto genérico (o vício da cópia automatizado).
  **Ninguém liga telemetria real → evidência → parecer.** Nós temos esse elo pronto.

### Arquitetura proposta (aprovar com o Marcos antes de construir)
1. **Telemetria por missão** (Firebase RTDB, mesma infra da agenda, gaveta nova
   `/educaverso/<escola>/evidencias/<aluno>/<missao>`): {kc, dataHora, tentativas,
   erros, nivelAjuda (0=sem, 1=pergunta, 2=gesto, 3=não concluiu), estrategia
   (ex.: "3×4" vs "2×6"), duracao, pKnown}.
2. **Rubrica automática:** regra explícita nivelAjuda+erros → Iniciando/Em
   desenvolvimento/Consolidado (por KC/habilidade BNCC).
3. **Parecer descritivo AUTOMÁTICO-RASCUNHO** que cita evidências concretas ("repartiu
   12 potes em 3 grupos de 4 na 2ª tentativa, corrigindo sozinho uma distribuição
   desigual") — SEMPRE editável pelo professor (LDB + o jogo vê só um recorte).
4. **Nota sugerida por tabela fixa** (configurável pelo professor) — nunca automática
   sem revisão.
5. **Painel do professor**: por turma × habilidade (quem consolidou/quem travou) +
   critérios PRÓPRIOS do professor ("do que eu quiser": campos de observação livre
   que entram no mesmo parecer).
6. **Identificação leve do aluno** no jogo (1º acesso: nome/turma — decidir com o
   Marcos o formato; laboratório compartilhado exige isso).
- **Honestidade obrigatória no produto:** relatório rotulado "evidências sugerem"
  (estimativa, não veredito); BKT tem vieses conhecidos; validade plena só com
  correlação externa (a avaliação do próprio professor É a validação natural).

## Fontes principais
Aleven & Koedinger (help-seeking, ITS 2004/IJAIED 2016); Baker et al. (gaming the
system); Razzaq & Heffernan (ITS 2010); Roll et al. 2011 (Help Tutor); Wood/Bruner
(contingent tutoring); NN/g (UX crianças); Sesame Workshop Best Practices; Shute et
al. (stealth assessment, Physics Playground, PvZ2); Corbett & Anderson (BKT); pyBKT;
LDB 9.394/96 art. 24 V; Movimento pela Base/Instituto Reúna (rubricas BNCC); revista
Meta: Avaliação (pareceres). URLs completas no histórico da sessão de 2026-07-20.
