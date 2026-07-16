# 👷 EQUIPE DE ESPECIALISTAS DO EDUVERSE (linha de montagem de atividades)

> O "esquema com especialistas" para fabricar atividades do EduVerse **sem erro e sem
> vai-e-vem**. Cada atividade percorre esta linha; **cada especialista tem um PORTÃO**
> que barra o erro antes do próximo. Casa com `EDUVERSE-FILOSOFIA.md` (Portão 0),
> `EDUVERSE-PIPELINE.md` (como construir) e `EDUCAVERSO-QA.md` (auditorias).
> Pode ser executado por MIM como uma equipe de agentes (um por papel), em sequência.

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
