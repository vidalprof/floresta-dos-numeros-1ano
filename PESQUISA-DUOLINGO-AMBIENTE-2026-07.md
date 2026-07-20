# Pesquisa PROFUNDA — o "ambiente Duolingo" (para o EduVerse parecer, sem copiar) — 2026-07

> Pedido do Marcos: estudar a fundo COMO o Duolingo é feito (design, telas, sensação, front-end) para o
> nosso app **parecer** com ele **de sentir** — **NÃO** as regras/pedagogia deles, **NÃO** as imagens deles.
> Alvo do nosso: **1 HTML, offline, PC fraco, 6–12 anos**. Força: [FORTE]/[CONSENSO]/[OPINIÃO].

## A LINHA (o que é seguro × o que dá problema) [FORTE]
- **PODE (padrão da indústria, sem dono):** trilha de progressão, barra de topo com XP/ofensiva, barra de
  progresso da lição, botões 3D "apertáveis", cantos redondos, cores semânticas (verde=certo/vermelho=erro),
  confete, mascote que reage por ESTADO, molas, som de acerto. São **técnicas/mecânicas** — livres.
- **NÃO PODE (é cópia / marca):** a arte deles, a **coruja Duo**, a fonte **Feather** deles, o nome/logo,
  as cores-assinatura deles como identidade, clonar tela por tela. E o Marcos reforçou: **nem a pedagogia,
  nem as imagens**. Nós usamos **Fagulha + céu/dourado + nossas regras (criar/resolver)**.
- **Resumo:** "cara de Duolingo, alma de EduVerse". Copiamos a **gramática de UX**, não o **conteúdo**.

## 1. DESIGN SYSTEM (o que dá o "capricho") [FORTE]
- **Tipografia deles:** *Feather Bold* (títulos, terminais arredondados, tirada do bico do Duo) + *DIN Next
  Rounded* (texto de interface). Lição: **fonte arredondada e cheia**. **Nós (offline):** não dá pra usar as
  deles; usar pilha arredondada do sistema `"SF Pro Rounded","Segoe UI",system-ui,"Baloo 2",Arial` + peso
  800/900 nos títulos. (Opção: embutir 1 fonte redonda leve em base64 — só se valer o peso.)
- **Cor:** paleta **super saturada + cores SEMÂNTICAS** — verde #58CC02=certo, vermelho #FF4B4B=erro,
  azul #1cb0f6, roxo #a570ff, amarelo #FFC200, cinza-nuvem #e5e5e5. **Nós:** mantemos **céu+dourado**, mas
  adotamos o PRINCÍPIO: verde p/ acerto, vermelho p/ erro (já temos em `.optbtn.certo/.erra`), cores fortes.
- **Botão 3D "apertável" [FORTE]:** sombra sólida embaixo `box-shadow:0 4px 0 <cor-escura>`, aperta e
  "afunda" (`translateY`). **Nós JÁ TEMOS** isso no `.btn`/`.sbtn`/`.optbtn`. Manter/expandir a TODO botão.
- **Regra de ouro:** **NADA de canto reto** — tudo `border-radius`. Espaçamento generoso. Poucas cores por tela.

## 2. TRILHA DE APRENDIZADO (a assinatura visual) [FORTE]
- Redesign 2022/2023: saíram da "árvore" solta e foram pra **trilha LINEAR guiada** — um caminho que
  serpenteia, **um nó = um nível**, agrupado em **unidades**, com **UM próximo passo óbvio** (a bolha
  "COMEÇAR" pulsando). Tira a "adivinhação": a criança sempre sabe pra onde ir.
- **Nó tem ESTADOS claros:** feito (colorido/coroa) · atual (destacado, pulsa, bolha START) · bloqueado (cinza).
- **Nós (JÁ TEMOS):** trilha rolante com câmera seguindo a Fagulha, nós feito/atual/futuro, rótulo no atual.
  **Próximo passo p/ ficar idêntico de sentir:** (a) **bolha "COMEÇAR"** saltitante no nó atual (em vez de só
  o rótulo); (b) agrupar visualmente em **unidades** ("Unidade 1 — Grupos", "Unidade 2 — Constelações") com
  uma faixa/*header* entre blocos; (c) nó atual com **anel branco pulsante** (o "farol").

## 3. HUD + GAMIFICAÇÃO (o vício do bem) [FORTE]
Mecânicas deles (todas são padrões livres): **XP**, **ofensiva/streak** + **streak freeze** (aversão à perda —
"quanto maior, mais dói perder"), **vidas/hearts**, **gemas** (moeda), **ligas** (ranking semanal), **quests**
(diárias/mensais), **meta diária**, **recompensas variáveis** (boost/gema aleatória = dopamina).
- **Nós JÁ TEMOS:** barra de topo com **estrelas ganhas + progresso + ofensiva**, e **prêmio de estrelas**
  por parada (contagem subindo).
- **Adotar (leve, sem servidor), em ordem de valor:**
  1. **Meta diária** ("acenda 30 estrelas hoje") + **anel de meta** enchendo — retenção diária. [FORTE]
  2. **Recompensa variável** no fim da parada: às vezes cai um **bônus** (2×, estrela extra) — surpresa. [FORTE]
  3. **Selos/conquistas** ("Mestre dos Grupos", "5 dias seguidos") — guardados no localStorage. [CONSENSO]
  4. **Streak freeze** ("escudo de ofensiva") como recompensa — perdoa 1 dia. [OPINIÃO/depois]
  5. **Liga/ranking** exige servidor (Firebase) e vários alunos → **fase 2**, junto com o parecer no Firebase.
- **CUIDADO PEDAGÓGICO (nosso, não deles):** gamificação é **tempero, não o prato**. Sem "dark patterns"
  (culpa, pressão agressiva). No EduVerse a estrela vem de **aprender**, não de "logar". Ver EDUVERSE-FILOSOFIA.

## 4. FLUXO DA LIÇÃO (dentro da parada) [FORTE]
- **Barra de progresso no topo** que **enche de verde e PULSA** a cada exercício certo — feedback constante.
- Fluxo: pergunta → escolhe (a opção "sobe" pro lugar da resposta) → botão **VERIFICAR** → vira **CONTINUAR**;
  **verde+ding** se certo, **vermelho+treme** se erro (com a resposta certa). 1 ação por vez, sem poluição.
- **Nós:** **adotar a barra de progresso fina no topo das paradas** (hoje só o mapa tem). E padronizar o par
  **VERIFICAR→CONTINUAR** nas paradas de pergunta (Soma/Problema/Desafio). Verde/vermelho **já temos**.

## 5. ANIMAÇÃO / "JUICE" (o que dá vida) [FORTE]
- **Animação DIRIGIDA POR ESTADO** (máquina de estados no Rive): o personagem **reage** a acerto/erro/marco —
  bater de asa no acerto, giro triunfal no marco. **Lip-sync** por *visemes* (20+ formatos de boca por
  personagem, mistura aditiva sincronizada aos fonemas).
- **Confete** ao completar a lição + **jingle** de acordes maiores.
- **Nós (sem Rive, só transform/opacity p/ PC fraco):** já temos Fagulha viva (respira/pisca/comemora/pensa),
  lip-sync por troca de boca, e "estouro de estrelas". **Próximos (leves):**
  - **Reação por estado** da Fagulha: acerto→pulinho/aceno; erro→encolhe/pensa (nós temos as poses). [FORTE]
  - **Molas `linear()`** (quique) nos botões/entradas — já pesquisado (ver PESQUISA-ANIMACAO-APP). [FORTE]
  - **Confete de estrelas** no fim de parada e no final (canvas leve, ~80 partículas). [CONSENSO]
  - **Hitstop + micro-tremor com rotação** no acerto grande (game feel). [CONSENSO]

## 6. SOM (dopamina auditiva) [FORTE]
- **Ding** curto no acerto; **treme+som seco** no erro; **jingle** de acordes maiores no fim da lição; "pop"
  de gema. Cada evento tem seu som — barato e viciante.
- **Nós:** já temos Web Audio (a "Música das Estrelas" e as notinhas). **Adotar:** um **ding de acerto**, um
  **som gentil de erro**, e um **acorde que resolve** ao acender a constelação (envelope anti-clique; destrava
  no 1º toque). Narração = voz do Antônio (MP3). Nunca travar o toque se o áudio falhar.

## 7. O QUE JÁ TEMOS × PRÓXIMOS PASSOS (priorizado p/ "parecer Duolingo")
**Já temos:** trilha rolante, HUD (estrelas/progresso/ofensiva), prêmio por parada, botões 3D, cantos
redondos, verde/erro-vermelho, mascote vivo, lip-sync, estouro de estrelas.
**Fazer a seguir (maior impacto / menor custo):**
1. **Bolha "COMEÇAR" pulsante** no nó atual + **anel-farol**. (trilha idêntica de sentir)
2. **Barra de progresso no topo das paradas** + par **VERIFICAR→CONTINUAR**.
3. **Ding de acerto / som de erro / acorde-resolve** (Web Audio leve).
4. **Reação por estado da Fagulha** (pulo no acerto, encolhe no erro) + **molas `linear()`**.
5. **Confete de estrelas** no fim de parada/final.
6. **Meta diária + recompensa variável + selos** (localStorage).
7. **Fonte arredondada** (pilha do sistema; embutir só se preciso).
8. (fase 2, com Firebase) **liga/ranking** + **parecer no banco** do professor.

## FONTES
Design system (cor/tipografia) https://design.duolingo.com/identity/color · https://design.duolingo.com/identity/typography
· Feather/DIN https://www.designyourway.net/blog/duolingo-font/ · Botão 3D / tokens https://www.designmd.co/d/duolingo
· Redesign da trilha https://blog.duolingo.com/new-duolingo-home-screen-design · https://duoplanet.com/duolingo-new-learning-path-review/
· Apple "Behind the Design" https://developer.apple.com/news/?id=jhkvppla · 12 padrões https://www.925studios.co/blog/duolingo-design-breakdown
· Rive/estado/lip-sync https://dev.to/uianimation/how-duolingo-uses-rive-for-their-character-animation-and-how-you-can-build-a-similar-rive-mascot-5d19
· Micro-interações https://medium.com/@Bundu/little-touches-big-impact-the-micro-interactions-on-duolingo-d8377876f682
· Gamificação (deconstructor) https://www.deconstructoroffun.com/blog/2025/4/14/duolingo-how-the-15b-app-uses-gaming-principles-to-supercharge-dau-growth
· Gamificação (case) https://trophy.so/blog/duolingo-gamification-case-study · Som https://soundcy.com/article/what-does-duolingo-sound-like
· Fluxo/barra de progresso https://usabilitygeek.com/ux-case-study-duolingo/ · Home redesign https://blog.duolingo.com/new-duolingo-home-screen-design/
