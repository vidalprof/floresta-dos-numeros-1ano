# 🎓 MODELO DE APRENDIZAGEM DO EDUCAVERSO — a fundação científica (documento-mestre)

> Pedido do Marcos: uma ferramenta que a criança AME e queira voltar, que faça a APRENDIZAGEM
> SUBIR de verdade, e que SE ADAPTE ao ritmo de cada criança — inovadora e fundamentada na
> ciência. Formato escolhido: **RPG 2D** (mantido). Este doc costura as 3 camadas num só sistema.
> Detalhe teórico nos docs: PEDAGOGIA-APRENDIZAGEM-CONCRETA, PEDAGOGIA-VYGOTSKY-DINAMICAS,
> PRINCIPIOS-ENCANTAMENTO. Aqui é a SÍNTESE que guia a construção.

## As 3 camadas (e por que só juntas funcionam)
1. **ENCANTA** (a criança quer estar ali) — a "casca" RPG: mundo/faz-de-conta com regra, personagem
   que pergunta, problema que precisa dela.
2. **ADAPTA** (invisível, por baixo — é o que MOVE a nota) — dificuldade no ritmo de cada criança.
3. **PROVA** (mede e mostra o ganho) — painel do professor por objetivo BNCC; alimenta a adaptação.
> Verdade científica (meta-análises): **jogo bonito sozinho rende POUCO** (Wouters 2013, d≈0,29). O
> que faz subir é o motor (2) + medir aprendizagem real (3). Sem elas, é "brócolis com chocolate".

## O LOOP (o que acontece em cada missão) — as 3 camadas viram UM ciclo
1. **FISGA — curiosidade + emoção + pertencimento.** Abre com uma **lacuna** (Loewenstein: "o rio
   secou — por quê?") num mundo que **precisa da criança** (SDT). O Byte **pergunta**. → liga o
   circuito dopamina-hipocampo (Gruber & Ranganath 2014): entra em "modo de aprender".
2. **AÇÃO — aprender fazendo, problema ANTES do conceito.** Age no mundo 2D (construcionismo/Papert;
   cognição incorporada — o gesto ancora o conceito; integração intrínseca de Habgood; **falha
   produtiva** de Kapur). Conceito vem por último. Andaime via **worked example + fading** e **CPA**
   (concreto→pictórico→abstrato, Bruner).
3. **CONSOLIDA — feedback + autoexplicação.** Feedback **imediato e específico** (Hattie d≈0,70, o
   maior efeito) + o Byte perguntando "por que você fez assim?" (**self-explanation**, Chi). É
   avaliação formativa invisível.
4. **ADAPTA — modelo de domínio + dificuldade dinâmica.** Cada resposta atualiza um modelo LEVE por
   KC (Elo ou BKT-lite). Dificuldade se ajusta pra manter o **canal de flow = ZDP de Vygotsky**
   (~70–85% de acerto). **Mastery gating:** só libera o próximo nó da trajetória quem domina; senão,
   remedia ali.
5. **FIXA — repetição espaçada + recuperação + intercalação (as "dificuldades desejáveis" de Bjork).**
   Um agendador **Leitner/SM-2** marca o retorno; ao logar, o mundo gera **"missões de retorno"** que
   forçam **lembrar** (testing effect, Roediger & Karpicke: 61% vs 40%), **espaçado** (Cepeda) e
   **intercalado** (Rohrer) — disfarçado de jogo, aproveitando a consolidação do SONO entre sessões.
6. **MEDE aprendizagem DE VERDADE.** Não "estrelas/tempo no app": **transferência** (resolve problema
   NOVO?) + **retenção espaçada** (ainda sabe dias depois?), alinhadas à BNCC. Realimenta o modelo e
   abre a próxima lacuna. O loop recomeça.

## 2 camadas transversais (envolvem todo o loop)
- **Motivação intrínseca (SDT — Deci & Ryan):** **autonomia** (escolhas reais), **competência**
  (desafio ótimo + feedback de progresso, nunca ranking que compara crianças), **pertencimento** ("o
  mundo é dele"). Recompensa = **celebração de domínio real**, nunca isca aleatória.
- **Carga cognitiva (Sweller + Mayer):** UM conceito por vez; palavra+imagem coerentes; **estética a
  serviço do conceito** (cuidado: mundo bonito demais vira distração = carga extrínseca).

## 🔧 Como ADAPTAR ao ritmo — barato e leve (navegador + Firebase grátis, SEM servidor de ML)
1. **Mapa de KCs:** quebrar cada objetivo BNCC em **componentes pequenos e ordenados** (a trajetória,
   à la Clements & Sarama). Banco de **itens por KC**, cada um com uma dificuldade estimada.
2. **Estado por criança no Firebase:** `/alunos/<id>/dominio/<kc> = {rating, box, ease, proximaRevisao, historico}` (poucos bytes/KC).
3. **Próximo desafio (flow/ZDP):** com **Elo**, escolher o item com **~70–85%** de chance de acerto
   pro rating atual; acertou→sobe, errou→desce (~30 linhas de JS). Alternativa interpretável:
   **BKT-lite** (4 parâmetros/KC; mastery em P(sabe)≥0,95).
4. **Andaime adaptativo:** erra seguido → injeta worked example + volta ao concreto (CPA); acerta →
   faz **fading** (respeita a reversão da perícia).
5. **Mastery gating:** só avança quem cruza o limiar; senão remedia no mesmo KC com itens diferentes.
6. **Fixação (Leitner):** caixas com intervalos (1,2,4,7,15 dias); no boot, KCs vencidos viram
   missões de retorno; acertou sobe de caixa, errou volta.
7. **Sem rótulo:** ajuste **dinâmico e invisível**; nunca exibir "seu nível/estilo". Variar
   representações é pra TODOS.
8. **Robustez (já dominamos na Agenda):** localStorage + sync Firebase + PWA → roda em PC fraco.
9. **Professor no loop:** painel por KC (quem dominou / quem travou) = a camada PROVA + avaliação
   formativa real pro Marcos.
> NÃO precisa (e sai caro à toa): deep knowledge tracing, correção de resposta aberta por IA, geração
> adaptativa em tempo real. Basta **banco de itens por KC + modelos leves**.

## ⚖️ A régua de SUCESSO (o ponto que decide tudo)
**Medir APRENDIZAGEM, não engajamento.** Sucesso = **transferência (problema novo) + retenção
espaçada** na BNCC. NUNCA "tempo no app" ou estrelas. (As meta-análises avisam: engajamento alto não
garante nota; só a integração intrínseca + medição garantem.)

## 🚫 MITOS que NÃO usamos (pra ser sério)
Estilos de aprendizagem (visual/auditivo — desmascarado); inteligências múltiplas como base de
ensino; cérebro esquerdo/direito; "10% do cérebro"; "nativos digitais"; growth mindset como milagre
(usar o princípio, sem prometer nota); "10 mil horas"; Zeigarnik como técnica de memória (é só
gancho); **recompensa tipo caça-níquel/loot box/streaks coercitivos/FOMO** e **overjustification**
(prêmio esperado corrói a motivação — pior em crianças). Recompensa é celebração de domínio real.

## 🏭 Como isso encaixa no pipeline (pedagogo ANTES do roteirista)
**BNCC → Bloom → Learning Trajectory (progressão) → eixo CPA → DINÂMICA (resolver/criar/investigar/
coletar/narrar/simular) + LM-GM (mecânica) → necessidade-do-mundo → [Portão 0 + Portão 0.5 Vygotsky] →
Roteiro → Motor(adapta) → Medição(prova).**
- **Pedagogo** entrega a "Espinha de Aprendizagem": KCs ordenados + dinâmica + eixo CPA + curva de
  ZDP/andaime + banco de perguntas do mentor + como MEDIR cada KC.
- **Roteirista** veste de história (cenário/personagem) SEM trocar mecânica nem ordem.
- **Motor** adapta (Elo/BKT-lite + Leitner) e **mede** (transferência/retenção → painel).

## Veredito (honesto, da ciência)
Com esse mix, a ideia **é genuinamente inovadora E fundamentada**. Ela LIDERA onde a maioria falha:
**fixação (retrieval/spacing/interleaving) + adaptação ao ritmo + medir aprendizagem real** — barato,
no navegador. A filosofia (problema primeiro, o mundo precisa da criança, o Byte pergunta) já está do
lado certo da ciência (SDT, curiosidade/dopamina, construcionismo, integração intrínseca,
self-explanation). **O que decide o sucesso não é a teoria — é a disciplina de sempre medir
aprendizagem (transferência+retenção na BNCC), não encantamento, e manter a integração intrínseca
honesta.** Se fizermos isso, não é "mais um joguinho": é uma ferramenta rara.
