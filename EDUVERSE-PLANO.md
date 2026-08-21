# 🗺️ PLANO-MESTRE DA FÁBRICA EDUVERSE (aprovar antes de executar)

> Consolidação do trabalho dos dois especialistas contratados (engenheiro de software =
> arquitetura/auditoria; engenheiro de games = motor/missões). Os dois **convergiram** na
> mesma arquitetura. Este é o plano que acaba com o "vai e vem": **primeiro o plano, depois
> execução cirúrgica**. Regido por `EDUVERSE-FILOSOFIA.md` / `EDUVERSE-PIPELINE.md` /
> `EDUVERSE-COMPUTACAO.md` / `EDUCAVERSO-QA.md`, e feito pela equipe do `EDUVERSE-EQUIPE.md`.

## A IDEIA CENTRAL (o que muda tudo)
Hoje cada atividade é **escrita à mão** (motor + conteúdo colados) — por isso dá retrabalho.
A virada: **a atividade vira uma RECEITA (dados)**, montada por **um builder único** sobre
**um motor reutilizável** + uma **biblioteca de peças (LEGO)**, e um **robô-auditor** testa
tudo **antes** de chegar ao professor.

**3 camadas separadas** (o builder junta num HTML só):
1. **MOTOR** (`kit.js`) — genérico, nunca sabe "floresta": loop, câmera+clamp, tiles, y-sort,
   sprites/animação, objetos inteligentes, mundo vivo (som/partículas/vento/luz), a **VM que
   roda o programa do robô**, controles (teclado + D-pad), e os hooks de QA. Extraído do que
   **já funciona** em `build_floresta2.py` (labirinto/programar) e `build_floresta3.py`
   (andar livre/mundo vivo). Código ES5 (compat Win7/Chrome antigo).
2. **DADOS** (`missao.json` / `mundo`) — a atividade descrita como dado: mapa de tiles,
   objetos com função, elenco, e o **arco pedagógico** (história→exploração→problema→
   experimentação→descoberta→conceito→aplicação→reflexão) com as **falas-pergunta** do Byte.
3. **ASSETS** (biblioteca) — imagens IA + vozes, **versionadas de forma reprodutível**
   (bruto + receita de recorte → processado; nada de "recorte na mão que se perde").

**Trocar de atividade = trocar a pasta de dados.** O motor é testado uma vez; a atividade é
leve e descartável (padrão "portal leve", 1 repo por atividade).

## O "SEM ERRO" — o robô-auditor (o coração da coisa)
Um `audit runner` transforma cada regra do `EDUCAVERSO-QA.md` em teste automático:
- **Portão 0 (filosofia) vira código:** um validador **recusa o build** se o arco estiver fora
  de ordem, se o Byte **instruir** em vez de perguntar, se o conceito for **nomeado antes** da
  descoberta, ou se houver "pergunta-para-abrir-porta" (prova disfarçada). **Atividade que fere
  a filosofia não compila.**
- **Portão 1 (funciona):** `node --check`; renderiza sem erro; **dirige a mecânica de verdade**
  (injeta a solução e confirma que completa — não confia em screenshot); dirige o **erro**
  (consequência no mundo, sem X vermelho); mede peso e exige offline.
- **Portão 2 (arte):** detecta **imagens sobrepostas/fragmentos**, confere y-sort/âncora nos pés,
  regressão visual por screenshot, e que **todo asset é IA no estilo travado**.
- **Portão 3 (você):** só o que passou em tudo chega ao seu colo — você aprova **pedagogia,
  arte e jogabilidade**, não caça bug.
> Cada erro novo que aparecer vira um **assert permanente** → o mesmo erro **nunca volta**.

## COMO NASCE UMA ATIVIDADE (ponta a ponta, com os portões)
Objetivo do currículo → **Pedagogo** escreve a receita (problema do mundo + arco) → *[Portão 0
automático]* → faltou asset? entra na **fila** → workflow gera no **mesmo estilo** (editando a
imagem-âncora) + **recorte determinístico** → **Engenheiro** monta (dados+biblioteca→HTML) →
**Auditor** roda *[Portões 1 e 2]*; se falhar, volta ao especialista certo (não a você) →
**você** aprova *[Portão 3]* → publica (link no ar).

## 🧭 ROADMAP EM FASES (valor rápido e risco baixo primeiro)
| Fase | Entregável (marco) | Por que |
|---|---|---|
| **0 — Fundação** | Extrair o **motor** do que já roda + travar o **estilo** (Byte como âncora) + migrar os assets da Floresta para a **biblioteca reprodutível**. **Marco: reconstruir "A Floresta do Byte" a partir de DADOS, idêntica à atual.** | Prova a ideia com **risco zero** (reproduz algo já aprovado). |
| **1 — Builder + Auditor** | **Um builder** (dados→HTML) + o **robô-auditor** (Portão 1 completo + validador de filosofia do Portão 0). | Trava o **"sem erro"** desde já; automatiza o que hoje escorrega. |
| **2 — A prova da tese** | **"O Rio do Vale das Máquinas"** — missão de **Condição (SE)** montada **só com dados** + 1 objeto (rio) + 1 instrução (se), reusando o motor. | Prova que **atividade nova nasce sem motor novo** (o objetivo do projeto). |
| **3 — Fábrica de peças** | Pipeline industrial de assets (fila→estilo travado→recorte determinístico) + **cartela de animação do Byte** (parado/andar 4 direções/falar/feliz/pensando). | Escala mascotes e dá **vida** aos personagens, sem deriva de estilo. |
| **4 — Auditoria pesada** | Sobreposição/regressão visual no runner + CI (`auditar.yml`). | Fecha o Portão 2 automático; protege contra regressão. |
| **5 — Mais conceitos** | **Repetição (loop)**, **Função** e **empurrar pedras (Sokoban)** — cada um uma missão nova pelo mesmo trilho. | Cobre a sequência didática de Computação. |
| **6 — Currículo + professor** | Carregar o currículo (Blumenau/BNCC) → esqueleto de missão; **relatório do professor** (avaliação descritiva); (futuro) **editor arrastar-e-soltar**. | Fecha cobertura curricular e o painel do professor. |

**Regra de ouro do sequenciamento:** Fase 0→1→2 é a espinha; a **missão do Rio (Condição)**
é a prova que destrava o resto. Só generalizar (4–5) depois que "missão = dados sobre o motor"
estiver provado ponta a ponta nos portões.

## DECISÕES TÉCNICAS TRAVADAS (para não rediscutir)
- **Grade lógica de 48 px** (parâmetro por mundo: 32 p/ interiores, 64 p/ mascote grande). Chão
  em tiles; **tudo que tem altura é sprite ancorado nos pés, dimensionado pela ALTURA**.
- **Personagem = cartela de poses IA** (geradas **editando a imagem-âncora** p/ manter o estilo)
  + **micro-vida por código** (respirar, andar, boca ao falar, piscar). Normalizar a baseline
  dos pés entre poses (não "pular").
- **VM única do robô** que cresce: sequência → condição (SE) → repetição (loop) → função. O
  **erro executa de verdade** na tela = **depuração natural**. "Empurrar pedras" é um
  **comportamento** de objeto sobre a mesma base, não motor novo.
- **Monorepo de produção = este repositório**; cada atividade publicada continua em **seu repo
  leve**. HTML autossuficiente, base64, **sem URL externa**, alvo < ~2,5 MB.
- **QA determinístico é lei:** dirigir a mecânica e ler o estado (não confiar em screenshot
  com tempo virtual). Foto de QA ≥ 500 px de largura.

## RISCOS já mapeados (com mitigação)
Ambiente reinicia com cópia velha → tudo commitado + `raw+receita` reconstrói o processado ·
Deriva de estilo da IA → sempre **editar a imagem-âncora** + versão de estilo · Recorte que se
perde → **receita determinística**, não clique · Build do Pages engasga → `republicar-limpo` ·
HTML incha → embutir **só os assets da missão** + medir KB · Filosofia violada sem notar →
**GATE automático** barra antes de codar.
