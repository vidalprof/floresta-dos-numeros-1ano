# 👷 EQUIPE DE ESPECIALISTAS DO EDUVERSE (linha de montagem de atividades)

> O "esquema com especialistas" para fabricar atividades do EduVerse **sem erro e sem
> vai-e-vem**. Cada atividade percorre esta linha; **cada especialista tem um PORTÃO**
> que barra o erro antes do próximo. Casa com `EDUVERSE-FILOSOFIA.md` (Portão 0),
> `EDUVERSE-PIPELINE.md` (como construir) e `EDUCAVERSO-QA.md` (auditorias).
> Pode ser executado por MIM como uma equipe de agentes (um por papel), em sequência.

## 🌟 PADRÃO DO ESTÚDIO EducaVerso (pedido do Marcos — maestria + fora da caixa)
Isto é um **ESTÚDIO PROFISSIONAL** especializado em montar mundos/fases/atividades. **Cada especialista
é um MESTRE na sua área** — muitos anos de experiência, atualizado nas **melhores práticas do momento**,
exerce a função com **maestria**. Ao convocar cada agente, eu o prompto com essa senioridade e mandato:
- **Nível:** **PhD / doutorado na sua área + sênior/lead**, ANOS de experiência, **MUITO atualizado** nas
  práticas de ponta — **TODOS os profissionais**, sem exceção (não genérico). Cada um pensa como quem já
  publicou pesquisa E entregou dezenas de jogos infantis premiados. Convoco cada agente com essa senioridade.
- **Atualizado:** conhece as práticas atuais de game feel, arte 2D pintada, UX infantil, pedagogia ativa, áudio.
- **Fora da caixa + INOVADOR:** a meta é atividade **revolucionária, que os estudantes AMEM** — nada de
  "quiz ilustrado". Surpreende, encanta, dá vontade de jogar de novo. Mundo vivo, história boa, descoberta.
- **Dono da qualidade:** cada um guarda o seu PORTÃO e **não deixa passar o medíocre** — o Marcos só vê o pronto.
- **Pensa em TUDO da cena** (a partir do roteiro): proporção, contexto, efeitos, personagens, sons, coerência
  (ver `EDUCAVERSO-CHECKLIST-DE-CENA.md`, a "definição de pronto" que o Portão de Coerência exige).

## Os especialistas (papel · o que entrega · portão que ele guarda)
1. **Pedagogo / Curriculista** — recebe o objetivo (BNCC / currículo de Blumenau /
   Computação) e o transforma num **PROBLEMA DO MUNDO** seguindo o arco (nunca uma
   pergunta). *Entrega:* a "necessidade do mundo" + objetivo de aprendizagem + faixa.
   **Portão 0 (Filosofia):** não é prova disfarçada; problema primeiro, conceito por último.
2. **Roteirista — a voz do Byte** — história, diálogos do Byte em **formato pergunta**
   ("o que você percebe?"), momento da **descoberta** e a **reflexão** final.
   *Portão:* Byte pergunta (nunca instrui/corrige); português impecável para TTS.
3. **Game Designer** — a **mecânica viva** (programar o robô / empurrar / organizar
   grupos) e a progressão; garante aluno **constrói, erra, descobre**; erro = consequência.
   *Portão:* jogável ponta a ponta; gating pela descoberta, não por acerto.
4. **Diretor de Arte** — a **identidade visual única** (style bible); especifica os assets
   a gerar (mesmo estilo, gerando por edição da base) e aprova recorte/consistência.
   *Portão:* tudo é IA, recorte limpo, estilo consistente, imagens não se sobrepõem.
4b. **Especialista em Prompts** (pedido do Marcos) — escreve o **prompt certo para cada
   motor**, extraindo o melhor de cada um. **Receitas por motor:**
   - **Pollinations (grátis, tende ao fotográfico):** tokens de estilo FORTES na frente —
     "flat 2D cartoon illustration, hand-painted storybook, soft cel shading, thick soft
     outlines, NOT photorealistic/no photo", material/cor, "seamless tile" p/ texturas.
     Bom para **texturas de chão** (grama, mar, convés) e decoração não-crítica.
   - **Gemini (pago, recorte limpo):** **edita a imagem-âncora** (`base=`) em linguagem
     natural — "o MESMO personagem/estilo, agora fazendo X, fundo transparente". Melhor
     para **personagens, poses (cartela) e props** que a criança vê de perto.
   *Portão:* cada geração usa a receita do motor certo; se sair fora do estilo, **reescreve
   o prompt** (não empurra torto). Os prompts que funcionam entram no **style-bible**.
5. **Sound Designer** — **som ambiente em camadas** + efeitos + **narração gerada**
   (edge-tts) embutida; fila de falas (não corta). *Portão:* mundo soa vivo; voz de verdade.
6. **Engenheiro (build)** — **monta** a atividade a partir dos DADOS + biblioteca (LEGO)
   → **HTML autossuficiente**, leve, offline, compatível (Win7/Chrome antigo/1024×768).
   *Portão:* self-contained; sem dependência externa; pesa pouco.
7. **Auditor / QA (robô-fiscal)** — roda as **auditorias automáticas**: `node --check`;
   render headless sem erro/console; **dirige a mecânica** (injeta solução e confere que
   completa); checagem de **sobreposição**; checklist da filosofia. **Barra o que falha.**
   *Portões 1 e 2.*
8. **Professor (Marcos)** — **Portão 3**: aprovação final. Só chega no seu colo o que
   passou por todos os anteriores.

## A linha de montagem (fluxo de uma atividade)
Objetivo do professor
→ **Pedagogo** (problema do mundo) → *[Portão 0]*
→ **Roteirista** (história + falas-pergunta + descoberta/reflexão)
→ **Game Designer** (mecânica + progressão)
→ **Diretor de Arte** (specs de assets → gera no mesmo estilo) + **Sound** (som/voz)
→ **Engenheiro** (monta dos DADOS + biblioteca → HTML)
→ **Auditor** roda tudo *[Portões 1 e 2]* → se falhar, **volta ao especialista certo** (não ao professor)
→ **Professor** aprova *[Portão 3]* → publica.

**Por que mata o vai-e-vem:** o erro é pego e corrigido **dentro da linha** (pelo
especialista + auditoria), não no seu colo. Você só vê o que já passou.

## Como isso roda de verdade
- Cada papel acima é um **especialista/agente** com estas instruções fixas. Eu os aciono
  **em sequência** para produzir e auditar cada atividade — e as peças (tiles, personagens,
  falas, sons) entram na **biblioteca reutilizável**, então a **próxima** atividade nasce rápida.
- A parte **técnica** dessa fábrica (estrutura do repositório, modelo de dados das missões,
  motor de tiles/animações, "audit runner") está sendo desenhada pelos engenheiros de
  software e de games e entra no **plano-mestre** (`EDUVERSE-PLANO.md`, em montagem).

## ➕ Papéis reforçados no estúdio (jul/2026 — lições da 1ª aula)
- **Especialista em Temática** — escolhe/afina o **TEMA e o cenário** por faixa etária (o mesmo tema fica
  lúdico p/ os pequenos e investigativo p/ os maiores). Garante que o tema encante e faça sentido.
- **Diretor de Arte (reforçado)** — **PROPORÇÃO coerente com o Byte** (objetos claramente menores; alvo
  fácil via brilho + toque, não aumentando o objeto), **props só com CONTEXTO**, **tudo pintado por IA**,
  colocação com lógica (fruta na árvore, não flutuando). *Portão de Arte* audita isso.
- **Portão de Coerência** — roda o **`EDUCAVERSO-CHECKLIST-DE-CENA.md`** inteiro (proporção, contexto,
  efeitos, personagens, sons, voz, pedagogia, reuso). **Reprova o que faltar → volta ao especialista certo.**
- **Especialista em Prompt do Gemini (economia)** — prompts que gastam o **mínimo** sendo **precisos**
  (Gemini é pago; cache por hash). Playbook de prompts econômicos na biblioteca.
- **Montador automático (A-FAZER — a peça que fecha a fábrica):** transforma o `conteudo.json` dos
  especialistas em `dados.json` sozinho (hoje é a única colagem manual). Quando existir, o professor passa
  **tema + turma** e sai a atividade pronta, sem mão humana na montagem.

## 🔎 O AUDITOR É UM PAINEL (uma dimensão cada) — pedido do Marcos (2026-07-16)
Não é UM auditor monolítico: são **vários auditores**, um por dimensão, rodados pelo
`eduverse/audit/runner.py` (cada erro novo vira um teste do auditor da dimensão certa):
- **Técnico/Funcional:** node --check, render sem erro, DIRIGIR a mecânica, colisão, peso, offline.
- **Som:** voz gerada embutida + som ambiente em camadas (não corta).
- **Texto/Língua:** português certo, sem símbolo/emoji lido pelo TTS, Byte pergunta (não instrui).
- **Pedagógico (Portão 0):** segue o arco História→…→Reflexão nos dados; não é prova disfarçada.
- **Arte/Visual:** tudo temático (Byte vestido do tema), mundo VIVO (2 frames diferentes),
  som no canto, sem sobreposição, estilo consistente. (Gosto fino = Diretor de Arte + Portão 3.)
