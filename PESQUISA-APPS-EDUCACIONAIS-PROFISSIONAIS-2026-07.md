# Pesquisa profunda — O que faz um app educacional ser AMADO + EFICAZ + PROFISSIONAL (2026-07)

> Encomendada pelo Marcos ("estou no caminho certo? preciso de algo profissional").
> Deep-research: 110 agentes, verificado por 3 votos adversariais. Fontes com evidência
> (Habgood & Ainsworth, XPRIZE, meta-análises de gamificação, Lepper, Crystal Island,
> Betty's Brain, Khan). **VEREDITO: a direção do projeto está CORRETA.**

## VEREDITO (resposta direta ao Marcos)
O caminho — **mix de mecânicas + simulações causa→efeito + aprendizagem ativa/mensurada
+ narrativa com mascote** — está **certo e alinhado à melhor evidência**. A ressalva central:
o que faz os apps serem amados E eficazes **não é a camada de jogo**, e sim (a) **integração
intrínseca** (o conceito É a mecânica de vitória) e (b) um **núcleo pedagógico**: feedback
explicativo + andaime personalizado + medição por aluno. Gamificação (streak/badge) é
**combustível motivacional fraco** — e o mais fraco justamente aos 8–12 anos.

## OS 10 ACHADOS (verificados)
1. **INTEGRAÇÃO INTRÍNSECA é o coração** (Habgood/Zombie Division, n=58 + réplica 2022 n=210):
   quando a mecânica de vencer É a matemática, aprende-se MAIS e joga-se ~7× mais por vontade.
   Falhar nisso = "chocolate-covered broccoli". **ADOTAR JÁ.** (nossas simulações já fazem)
2. **Gamificação eleva motivação/autonomia/pertencimento, NÃO competência** (meta-análises 2024/25):
   efeito mínimo em domínio (g≈0,28) e o motivacional é o MAIS FRACO na primária (g=0,31). **EVITAR**
   depender de streak/badge como motor de aprendizado.
3. **Recompensa extrínseca não é vilão automático** (Quest Atlantis, n≈106): badges/reconhecimento
   num ambiente RICO EM FEEDBACK não corroeram interesse e até elevaram compreensão. **TESTAR** com cuidado.
4. **Armadilha da superjustificação é real e específica** (Lepper 1973): prêmio PROMETIDO por algo
   que a criança já gosta reduz o interesse depois (caiu ~metade); prêmio SURPRESA não faz mal.
   **EVITAR prometer prêmio antes; usar recompensa-surpresa.**
5. **O que separa os eficazes é um núcleo checável** (XPRIZE, 2.041 crianças): os 2 melhores apps
   tinham 6 features + **feedback explicativo (por que certo/errado) + andaime personalizado +
   feedback motivacional (elogio)** — não engajamento sozinho. **CHECKLIST premium. ADOTAR JÁ.**
6. **Embrulhar quiz em jogo** não prejudica nem turbina aprendizado de longo prazo (d=0,09), mas
   ganha em engajamento (59/69 preferem). O jogo compra ENGAJAMENTO, não aprendizado extra.
7. **Medir por aluno é inegociável** (Crystal Island): narrativa/engajamento NÃO dão aprendizado
   uniforme; alunos fracos precisam de andaime EXPLÍCITO. **ADOTAR JÁ** (já iniciamos com BKT-lite).
8. **Mascote narrador NÃO é eficaz por si** (agentes pedagógicos: resultados mistos; Schroeder 2013
   = efeitos pequenos). Ajuda no AFETIVO; o ganho de aprendizado precisa ser DEMONSTRADO. **TESTAR.**
9. **Aprender ENSINANDO (teachable agents / Betty's Brain)** é mecânica leve e viável em HTML/JS:
   o aluno ENSINA um agente por um MAPA CAUSAL e aprende mais fundo. **TESTAR** (clima→bioma é um
   grafo causal perfeito para o aluno "ensinar" ao mascote). ← já começamos ("Ensinar a Nara").
10. **Mastery + dose regular = ganho real** (Khan, correlacional/fornecedor — usar como princípio,
    NÃO citar número como RCT). **ADOTAR o princípio.**

## RESSALVAS HONESTAS (não superinterpretar)
- Intrínseco vs extrínseco: nenhum estudo comparou os dois direto. Intrínseco = padrão-ouro p/
  MAXIMIZAR; extrínseco = "seguro" p/ engajamento quando o intrínseco for inviável ("não prejudica"
  ≠ "é ótimo").
- Transferência: XPRIZE/apps miraram 4–7 anos / fora da escola; a nossa faixa (8–12) é onde a
  gamificação rende MENOS. Cuidado ao importar.
- 2 claims REFUTADAS na verificação: (a) "gamificação melhora aprendizado g=0,257"; (b) "engajados no
  Betty's Brain ganharam significativamente mais". NÃO usar como apoio.
- Khan (0,36) e metas de gamificação: correlacional / heterogeneidade altíssima (I²≈89%). Estimativas,
  não leis.

## CHECKLIST "ATIVIDADE PREMIUM PROFISSIONAL" (derivado da evidência)
1. [ ] **Integração intrínseca:** a ação de vencer É o conteúdo (não exercício embrulhado).
2. [ ] **Feedback EXPLICATIVO:** diz por que está certo/errado (não só ✓/✗) — sobre a TAREFA, nunca a pessoa.
3. [ ] **Andaime personalizado:** o aluno fraco recebe apoio explícito; o forte, desafio (ZDP).
4. [ ] **Medição por aluno (stealth):** por conceito, escondida, vira parecer ao professor.
5. [ ] **Mastery + dose + revisão espaçada** (recuperação): relembrar, não só rever.
6. [ ] **POE / previsão + autoexplicação:** a criança prevê e explica (aprendizagem ativa).
7. [ ] **Refutação** de concepções erradas comuns da matéria.
8. [ ] **Recompensa só SURPRESA** (nunca prometida por algo que já é gostoso) — engajamento sem superjustificação.
9. [ ] **Aventura instrutiva:** narrativa a serviço do conteúdo; mascote como apoio afetivo (não como "prova" de aprendizado).
10. [ ] **Transferência:** um "chefe" final em contexto NOVO, sem apoios.
11. [ ] **Acessível e leve:** jogável ouvindo (pouca leitura), contraste, roda em PC fraco.
12. [ ] **VALIDAR:** medir ganho real (pré/pós simples) — não presumir que "engajou = aprendeu".

## O QUE ISSO MUDA NO NOSSO PROJETO (prioridades)
- **Já fazemos bem:** integração intrínseca (simulações), POE, refutação, medição BKT-lite, mastery/Leitner,
  autoexplicação, ensinar-o-mascote (começamos). **Continuar.**
- **Reforçar:** feedback EXPLICATIVO em toda mecânica; andaime para o aluno fraco; transferência (chefe final).
- **Cuidar:** recompensas — preferir SURPRESA, nunca prometer prêmio antes. Não inflar streak/badge.
- **Testar (o diferencial "profissional de verdade"):** validar ganho real (pré/pós rápido embutido) e
  aprofundar o "ensinar o mascote" via mapa causal (Betty's Brain) no 6º ano.

## Perguntas em aberto (para pesquisas futuras)
- Comparar intrínseco × extrínseco × quiz-puro na MESMA turma/conteúdo (BR) — ninguém testou os 3 juntos.
- Evidência independente (WWC/RCT) de mastery+espaçada em 8–12 anos, PC fraco, ~55 min.
- Playbook de streak/badge ético para 8–12 (surpresa × prometido) que preserve motivação E engajamento.
- Arquitetura de código dos melhores (PhET open-source; Canvas puro × Phaser/Pixi sob ES5/Chrome 109).
