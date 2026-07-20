# A Fábrica de Estrelas — PLANO (3º ano · EF03MA07 · premium NOVA GERAÇÃO)

> Primeira atividade no molde da `PLANTA-ATIVIDADE-PREMIUM-NOVA-GERACAO.md` (herda a casca do
> `ATIVIDADE-PREMIUM.md`, troca o miolo p/ criar/resolver). Mais animada e mais viva que o premium de
> hoje (abertura/final animados, mascote e mapa vivos). Voz do Antônio (MP3). Sem emoji na tela.
> Nomes/detalhes provisórios — o Marcos pode trocar.

## IDENTIDADE
- **Objetivo BNCC:** EF03MA07 — resolver/elaborar problemas de multiplicação (×2,3,4,5,10) com os
  significados de **adição de parcelas iguais** e **disposição retangular (array)**.
- **Mascote:** **Fagulha**, uma fagulinha/estrela viva que trabalha na fábrica de estrelas (provisório).
- **História (fantasia INTRÍNSECA — a história FAZ a multiplicação):** a noite chegou e o céu está
  escuro e vazio. A Fábrica de Estrelas precisa **acender o céu** arrumando as estrelas em **grupos
  iguais** (caixas) e em **grades** (constelações = arrays de linhas × colunas). A criança ajuda a
  Fagulha a encher o céu — cada parada acende uma parte do céu; no final, o céu inteiro se acende.
- **Cores:** noite (azul-marinho/roxo profundo) + dourado/estrela; contraste alto (WCAG nos 2 temas).
- **Público:** 3º ano. **Repo destino (sugestão):** `fabrica-de-estrelas` (confirmar).

## A LEI (miolo criar/resolver — teste de fogo em toda parada)
Problema primeiro → a criança CRIA/RESOLVE (monta grupos/arrays) → o **mundo REAGE** (as estrelas
acendem, a constelação brilha — nunca popup "Acertou!") → concretude que desvanece (estrelas → pontos
num array → 3×4=12) → a Fagulha **NOMEIA no fim** ("3 caixas de 4 é 4+4+4, e a gente escreve 3×4=12";
a Fagulha PERGUNTA, não responde).

## ARCO DE PARADAS (cada uma um canto da fábrica/céu; ALÍVIO on-mission entre as de aprendizado)
> Aprovado pelo Marcos (2026-07). Alívio de preferência **on-mission** (variedade + criação), com o
> quebra-cabeça clássico só como tempero temático e curto — nunca recheio. Alvo ~55 min; o
> `qa-duracao.mjs` confirma no fim (não chutar).

**Ordem:** Abertura animada → P1 → P2 → *Música das Estrelas* → P3 → P4 → *Monte a Constelação* → P5 →
*Decore o seu céu* → Final animado.

**Paradas de APRENDIZADO (contam nota):**
1. **As Caixas de Estrelas — grupos iguais (×2, ×3).** A criança arrasta estrelas p/ encher N caixas
   com M cada ("3 caixas, 4 estrelas em cada"); ao ficarem iguais, as caixas sobem e acendem um pedaço
   do céu. Mede: montou iguais? contou 1-a-1 ou de M em M (skip-count)?
2. **A Constelação — disposição retangular (×4, ×5).** A criança monta um **array** (arrasta estrelas
   em fileiras × colunas); ao fechar o retângulo, vira uma constelação que brilha. Mede: entende
   linhas × colunas? conta por fileira (repetição) ou 1-a-1?
3. **Dois jeitos, mesmo céu — comutatividade.** Monta 3×4 e depois 4×3 e vê **acender a mesma
   quantidade** de estrelas. Mede: percebeu 3×4 = 4×3?
4. **O Céu Grande — ×10.** Caixas/grade de 10; o céu enche rápido (a força do ×10). Mede: usa o ×10
   como atalho?
5. **A Sua Constelação — autoria (elaborar problema, BNCC).** A criança **cria** a própria constelação
   (escolhe fileiras × colunas / grupos) e desafia a Fagulha, que "lê" o array e diz a multiplicação —
   e às vezes **erra de propósito** (efeito protégé), pra criança consertar. Mede: o desafio criado é
   bem-formado (proxy de domínio)? corrigiu a Fagulha?
- Em cada parada de aprendizado, **1 item-símbolo no fim** (sem os apoios) p/ medir **transferência**.

**Paradas de ALÍVIO / DELEITE (NÃO contam nota — pacing e amor):**
- **Música das Estrelas** (alívio ON-TEMA, entre P2 e P3): cada grupo de estrelas toca uma nota
  (sonificação — pitch sobe por grupo); parece brincadeira/toy, alivia a atenção, e ainda é "grupos
  iguais" por baixo. É o alívio preferido (variedade sem sair da missão).
- **Monte a Constelação** (alívio TEMÁTICO curto, entre P4 e P5): quebra-cabeça da figura de estrelas.
  Alternativa: memória "grupo ↔ total" (3 grupos de 4 ↔ 12), que reforça a multiplicação de leve.
- **Decore o seu céu** (DELEITE final, antes do final animado): criação livre (pintar/enfeitar o céu) —
  autoria pura, sem certo/errado.

## ABERTURA E FINAL ANIMADOS (o "impressiona a criança")
- **Abertura (cutscene):** a noite cai (parallax do céu escurecendo), a fábrica acende as luzes, a
  Fagulha aparece e conta a missão (voz do Antônio, texto sincronizado). Céu vazio esperando.
- **Final (cutscene):** ao concluir tudo, o céu INTEIRO se acende numa grande constelação, fogos de
  estrela, a Fagulha comemora e fecha a história. (Técnica exata = pesquisa de animação em andamento;
  tudo em transform/opacity, camadas de arte IA, sem vídeo pesado.)

## MASCOTE VIVO + MAPA VIVO (mais vivo que hoje)
- **Fagulha viva:** respira, pisca, reage (pensando/comemorando) e fala com **lip-sync** na voz do
  Antônio. Gerada em PARTES (p/ animar) — detalhe final pela pesquisa de animação.
- **Mapa vivo:** o "céu-mapa" com parallax, estrelas piscando/derivando, poeira estelar (partículas),
  a Fagulha caminhando pela trilha de constelações, câmera que segue suave, próxima parada revelando
  com brilho. Barato (transform/opacity, pausa fora da tela).

## SOM (Web Audio p/ feedback + Antônio MP3 p/ voz)
- Feedback instantâneo sintetizado (envelope anti-clique); **acorde que resolve** ao acender a
  constelação; erro = dissonância curtíssima e gentil. **Sonificação:** cada grupo/fileira soa um
  "degrau" (pitch sobe) — dá pra OUVIR a multiplicação crescer. Silêncio no momento de pensar.
- Narração do Antônio em MP3 (conversacional, "você consegue…"), com legenda sincronizada.

## MEDIÇÃO (ECD → parecer)
- **Competência:** compreende multiplicação como grupos iguais e array; liga à adição de parcelas
  iguais; reconhece/usa o símbolo ×; (bônus) percebe comutatividade.
- **Evidência/observáveis:** grupos iguais vs. desiguais; skip-count/soma repetida vs. 1-a-1; monta o
  array por dimensões; comutatividade; acertou o item-símbolo (transferência); tentativas, acerto-na-1ª,
  hesitação, uso de dica.
- **Tarefa:** as 5 paradas acima.
- **Saída:** placar oculto por indicador → **parecer descritivo** (começa simples e honesto) → nota
  sugerida. Persistência local (localStorage; Firebase opcional como na Agenda).

## LISTA DE ASSETS (provisória — FINALIZAR com a pesquisa de animação, tudo gerado por IA em CAMADAS/PARTES)
- Mascote Fagulha: em PARTES (corpo, cabeça, olhos abertos/fechados, bocas p/ lip-sync, braços) +
  poses (feliz, pensando, comemorando, incentivando).
- Cena de abertura e cena final: em CAMADAS (céu ao fundo, fábrica/meio, frente).
- Céu-mapa: camadas de parallax (céu, estrelas de fundo, trilha de constelações).
- Estrelas/caixas/grade: objetos limpos p/ compor grupos e arrays.
- Medalhas/selos/emblemas/troféu/recompensa-que-cresce: no padrão premium.
- Regras de imagem = §12 do manual premium (fundo branco puro, contorno fechado, de-fringe, otimizar,
  base64) — mas agora pensadas p/ ANIMAR (partes/camadas), não cena chapada.

## FLUXO DE CONSTRUÇÃO
1. Esperar a pesquisa de animação (cutscene + mascote/mapa vivos) → fecha o método de layering/rig.
2. Escrever os prompts de imagem (camadas/partes) → disparar geração em lote pelo workflow → `git pull`.
3. Gerar a narração do Antônio (MP3) pelo workflow.
4. Montar a **fatia de teste** primeiro (Fagulha + abertura animada + tela inicial + mapa vivo) →
   mostrar ao Marcos p/ aprovar o estilo (Portão do professor).
5. Montar as 5 paradas (criar/resolver) + medição + som.
6. Auditoria 3 níveis + checklist da planta (teste de fogo, portão pedagógico/neurociência) → prévia →
   aprovação do Marcos → publicar pela Fábrica → card no hub.

## STATUS
- [x] Objetivo, tema, mascote, arco de paradas, medição (este plano)
- [ ] Pesquisa de animação (cutscene + vivo) — em andamento
- [ ] Arte em camadas/partes (workflow) + voz do Antônio (workflow)
- [ ] Fatia de teste (aprovar estilo)
- [ ] Paradas 1..5 + som + medição
- [ ] Auditoria + prévia + aprovação + publicação
