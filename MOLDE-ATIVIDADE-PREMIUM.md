# 🏗️ MOLDE OFICIAL — como montar uma ATIVIDADE PREMIUM MELHORADA (ler ANTES de criar qualquer atividade)

> **Por que este arquivo existe:** o Marcos pediu (2026-07-21) UMA receita fixa, profissional,
> que qualquer sessão siga para montar atividades no padrão que consolidamos — a aventura de
> ~55 min, a equipe, os portões, o motor que se herda e as leis. **A "Fábrica de Estrelas"
> (3º ano) é o EXEMPLAR-MODELO** (padrão-ouro). Toda atividade nova CLONA o motor/estrutura e
> troca **TEMA + MASCOTE + CONTEÚDO + adequação à FAIXA/disciplina**. Engenharia pesada = feita
> 1x; atividade nova = configuração + arte + som + as paradas de produção.
>
> Docs-irmãos (ler junto): `EDUVERSE-FILOSOFIA.md` (a LEI/Portão 0), `EDUCAVERSO-QA.md` (portões),
> `EDUVERSE-EQUIPE.md` (papéis), `AUDITORIA-APRENDIZAGEM-E-DINAMICAS-2026-07.md` (o que a atividade
> precisa ter), `PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md` (a pesquisa que fundamenta), o motor
> vivo em `_estrelas/index.html` (a base a clonar), `_clima/PLANO.md` (exemplo de plano novo).

## 1. AS LEIS FIXAS (Portão 0 — nenhum passo pode violar)
1. **PRODUÇÃO, não reconhecimento.** A criança CONSTRÓI/monta/regula/cria — nunca "escolhe a
   alternativa certa". A jogada É a evidência (stealth/ECD — Shute & Ventura). Proibido: pop-up de
   pergunta, "arraste a resposta certa", quiz de múltipla escolha, NPC que dá a resposta.
2. **CONCRETO → PICTÓRICO → ABSTRATO** (Bruner/CPA — verificado na pesquisa, vale do pré ao 9º):
   manipula o concreto primeiro; o símbolo/fórmula/nome chega por ÚLTIMO. Nunca inverter.
3. **PROBLEMA primeiro, conceito depois.** O mundo precisa de algo; a criança resolve; o conceito
   é institucionalizado no fim (Brousseau).
4. **O MUNDO REAGE por CONSEQUÊNCIA física** — acertou, o mundo vive/floresce; errou, a família
   reclama / a ponte não fecha / o bioma seca. Nunca um X vermelho, nunca gabarito escondido.
5. **A LEI do mundo (mini-simulação), não respostas guardadas.** Programa-se a LEI e o mundo a
   aplica sobre QUALQUER coisa que a criança construir → MUITOS jeitos de vencer (criatividade real).
6. **MEDIÇÃO por baixo (invisível à criança).** O motor mede ao vivo; a criança nunca vê nota/rótulo.
7. **NA ZDP** — progressivo, um degrau por vez, o mentor PERGUNTA (não responde); errar devolve a
   peça sem punição. Profundo ≠ difícil.
8. **FIXAÇÃO exige REVISÃO ESPAÇADA** (Leitner) — a sessão constrói, mas só fixa com missões de retorno.

## 2. A EQUIPE (chapéus) e OS PORTÕES (sempre passam antes do Marcos)
Uma pessoa (eu) veste os chapéus em ordem: **(1) professor PhD da disciplina** (sabe a BNCC, onde
trava, o erro clássico) → **(2) cientista da aprendizagem** (projeta pela pesquisa) → **(3) dev de
RPG 2D + designer instrucional** (desenha o JOGO jogável, não um vídeo) + **Diretor de Arte**.
Portões: **0 filosofia** · **1 funciona** (robô/QA joga) · **Arte** (proporção/contexto/coerência,
tudo IA) · **2/3 professor** (prévia + aprovação do Marcos).

## 3. O PROCESSO OFICIAL — passo a passo (a "receita")
**0) Marcos dá TEMA + ANO/disciplina.** (Ex.: "Climas do mundo, 6º ano".)
**1) BNCC (chapéu professor).** Verificar (web/`_curriculo/blumenau.txt`) as **habilidades e objetos
   de conhecimento** reais do ano; anotar os **erros clássicos** e a progressão. NÃO inventar código.
**2) Projeto de aprendizagem (chapéu cientista).** Escolher os motores da pesquisa que cabem:
   produção/ECD, CPA, **dificuldade desejável** (Bjork), **Leitner**, **autoexplicação**, **tutoria
   adaptativa (BKT)**, e o **DIFERENCIAL = Open Learner Model** (devolver ao aluno, de forma legível,
   o que ele já domina — metacognição visível). Definir os **KCs** (subconceitos medidos).
**3) Desenho do jogo (chapéu dev/designer).** Escrever:
   - a **LEI do mundo** (a mini-simulação: o que a criança regula → o que o mundo faz);
   - a **história intrínseca** (a fantasia FAZ o conteúdo; recompensa = o mundo curado);
   - o **MASCOTE** (guia que PERGUNTA; adequado à faixa — ver §6);
   - o **ARCO de ~55 min** (ver §4), com cada parada mapeada a uma habilidade da BNCC;
   - a lista de **assets** (mascote em partes/poses; cenários; objetos; medalha).
**4) PLANO em doc** (`_<slug>/PLANO.md`, no formato do `_clima/PLANO.md` ou `_estrelas/PLANO.md`) →
   **PORTÃO do professor**: mostrar ao Marcos; só seguir com o "GO" (mascote/estética/nome).
**5) ARTE por IA (workflow).** Base do mascote + poses (fala/pisca/pensa/comemora), cenários/biomas,
   ícones, medalha. Lote via `_gerar_imagens.json` + push `[imagens]` (Gemini) ou `gerar-imagens.yml`.
   Regras: fundo branco puro p/ recorte, contorno fechado, sem sombra, gerar em CAMADAS p/ animar,
   coerência de proporção com o mascote (Portão Arte). Trazer com `git pull` → mover p/ `_<slug>/img/`.
**6) VOZ (workflow).** Narração do **Antônio** (`gerar-audio.yml modelo=male`, `pt-BR-AntonioNeural`)
   por parada + falas de dica/autoexplicação/aquecimento. Copiar p/ `_<slug>/audio/`.
**7) MOTOR — CLONAR, não reescrever.** `cp _estrelas/index.html _<slug>/index.html` (+ sw.js/manifest).
   Trocar: `ATIVIDADE_ID`/`ATIVIDADE_NOME`, cache do sw, `TURMAS` da faixa, nomes dos PNGs do mascote,
   tema/cores, textos, ids de áudio, os **KCs** e as **VARS** (variações). Implementar a **LEI** e as
   **paradas de PRODUÇÃO** no lugar das da Fábrica de Estrelas — o resto do motor já vem pronto (§5).
**8) QA 3 níveis.** (a) `node --check` no JS extraído; (b) render headless (Chromium
   `/opt/pw-browsers/...`) de CADA tela + click-through sem erro; (c) portões 0/1/Arte. Compat PC
   fraco (só transform/opacity; sem grid/gap/var/clamp; sem emoji no que a criança vê).
**9) DURAÇÃO ~55 min.** Modelar o tempo por parada (auditor tipo `qa-duracao`); ajustar até ~45–55.
**10) PUBLICAR + PORTAL.** `fabrica.yml` (repo novo) ou `atualizar.yml`; card no **portal**
   (`_portal/index.html` → objeto `ATIVIDADES`) na **turma certa**. Portal leve: só o link.

## 4. A AVENTURA DE ~55 MIN (a estrutura do arco — sempre esta forma)
**Abertura animada** (cutscene: o problema aparece; o mascote convida) → **paradas de APRENDIZADO**
(produção, cada uma um "verbo da mão" diferente: arrastar → traçar → regular → tocar; cada uma
mapeada a 1 habilidade BNCC e termina com **1 item-símbolo de transferência** sem apoios) →
**ALÍVIOS on-mission** intercalados (variedade + criação; nunca recheio) → **parada de AUTORIA**
(a criança CRIA + efeito protégé) → **DELEITE final** (criação livre) → **Final animado** (o mundo
curado reacende) → **parecer** (medição → nota; só o professor vê). ~10–12 paradas.
Alvo **55 min**; a criança rápida não pode "furar" em 35 → prever variação/2ª rodada + prática.
**Ganchos de retorno éticos:** revisão espaçada como motivo de volta (não FOMO); streak gentil;
progresso visível; autoria persistente (galeria). O "prato" é a dinâmica; a medalha é o sal.

## 4½. PADRÃO DE QUALIDADE — "MODERNO É VIVO" (lei do Marcos, 2026-07-21) ⭐ OBRIGATÓRIO
A atividade NUNCA pode parecer amadora/parada. O padrão-ouro é a Fábrica de Estrelas: tudo RESPIRA.
- **Mascote VIVO:** respira, pisca (com piscada dupla ocasional), fidget, **lip-sync na voz**, poses
  com crossfade, entrada animada, sombra no chão, presença de bom tamanho na tela (não recorte
  minúsculo no canto). Guia que PERGUNTA. Voz coerente com o personagem (Nara=menina → voz feminina).
- **FUNDO e cena VIVOS:** nunca gradiente morto. Camadas animadas (partículas, aurora/nuvens à
  deriva, parallax leve, brilho que pulsa) — só transform/opacity, PC fraco.
- **OBJETOS da cena VIVOS:** os elementos que a criança vê reagir têm micro-vida (respiram, brilham,
  partículas próprias — chuva na floresta, neve na tundra, tremor de calor no deserto).
- **GAME FEEL:** hit-stop, tremida com micro-rotação, som variável, transição de entrada em toda tela.
- **ARTE premium coerente** (Portão Arte): personagem e cena no MESMO estilo; nada de recorte chapado
  sobre branco dentro do jogo (o branco é só p/ gerar o asset; na cena ele vive sobre o mundo).
- **Régua:** se ao lado da Fábrica de Estrelas a atividade parecer mais pobre/parada → REPROVA.

**RECEITA TÉCNICA DO MASCOTE VIVO (aprendida na Nara/Planeta Vivo — 2026-07, seguir à risca):**
1. **Recorte transparente OBRIGATÓRIO.** O Gemini entrega o mascote/globo/ícones com fundo sólido
   (branco/preto). Isso vira um **quadradão amador** sobre o cenário. Recortar de graça no container
   com Pillow: **flood-fill a partir da BORDA** (só o fundo conectado à borda vira alfa 0 — preserva
   brancos internos, ex. dentes/olhos), feather ~1px, autocrop. Cena de bioma é FOTO opaca → deixar
   como está (vira JPG); só personagem/props/ícones/medalha/globo são recortados.
2. **Poses em CANVAS ÚNICO, pés alinhados.** Todas as poses (base/fala/pisca/pensa/comemora/aponta)
   no MESMO tamanho de tela, figura **centrada em x e apoiada no mesmo chão** (bottom-align). Senão a
   troca de pose "pula". base/fala/pisca partilham o MESMO bbox (recorte em grupo).
3. **fala/pisca = base + SÓ a boca/olhos (o pulo do gato do lip-sync).** O motor faz crossfade da
   imagem `fala` inteira sobre a `base`; se o Gemini mudou o CORPO todo entre as imagens (é o padrão:
   ~14% dos pixels diferem), o corpo inteiro **treme** ao falar. Conserto: montar `nara_fala` =
   **cópia da base com só uma ELIPSE da boca vinda da imagem de boca aberta** (idem `nara_pisca` = base
   + elipse dos olhos fechados). Detectar a face (a pele infla com o colete/mãos → conferir com
   crosshair num render antes de salvar) e compor a elipse com feather. Alvo: diferença **<1%,
   localizada na boca/olhos** (a Fábrica de Estrelas fica ~2,6%). Aí a boca abre com a voz, limpo.
4. **Analisador liga no 1º gesto** (`createMediaElementSource(narr)` → analyser → destino) e o `loop()`
   dirige a opacidade da `fala` pela RMS da voz. Sem áudio de verdade não há lip-sync — **gerar a
   narração é pré-requisito** (mudo = "mascote morto").

## 4¾. PEDAGOGO ESCOLHE AS MECÂNICAS + MUITAS PARA 55 MIN (lei do Marcos)
- O **pedagogo** (chapéu 1+2) escolhe, do `CATALOGO-DINAMICAS-INTERATIVAS.md`, as mecânicas que
  MELHOR ensinam AQUELE conteúdo/habilidade (não repetir a mesma o tempo todo — 1 verbo da mão
  diferente por parada). Não é "adaptar a Fábrica de Estrelas": é ATINGIR O PADRÃO com o tema e as
  mecânicas certas da disciplina.
- **Usar o MÁXIMO de mecânicas de aprendizado real que caibam em ~55 min** (intercalação, ver
  pesquisa) — a aventura tem ~10-12 paradas, cada uma uma mecânica de PRODUÇÃO com evidência.

## 5. O QUE O MOTOR JÁ ENTREGA (herdado da Fábrica de Estrelas — NÃO reconstruir)
- **Adaptação ao ritmo** (BKT-lite por KC) + **mastery gating gentil** (recomenda praticar, nunca bloqueia).
- **Variações** por parada (números/casos novos) — "praticar de novo" ≠ decoreba.
- **Revisão espaçada Leitner** (caixas 1/3/7/14 dias) + tela **Aquecimento** na volta + **retenção medida**.
- **Autoexplicação com feedback VISUAL** (toca no desenho do porquê; Portão 0 mantido, sem certo/errado na tela).
- **Dica graduada 3 níveis** (pergunta → aponta → mostra 1; nunca dá a resposta) + **"Ouvir de novo"**.
- **Medição stealth → parecer descritivo → consolidada (todas as atividades) → nota sugerida → IMPRIMIR**.
- **Identidade `edu_*`** compartilhada (turma → nome → **figurinha/PIN secreto**) + **painel do professor** (senha).
- **Lip-sync real** (boca segue a voz) + **mascote profissional** (crossfade de poses, squash&stretch, sombra,
  ciclos dessincronizados, rastro) + **game feel** (hit-stop, tremida, som variável) + transições de tela.
- Tudo `transform/opacity`, `prefers-reduced-motion`, PWA/sw.

## 6. ADEQUAÇÃO POR FAIXA (pré → 9º — a "casca" muda, o motor não)
- **Identificação:** pré–2º = lista narrada + **figurinha secreta** (desenho, zero leitura) · 3º–5º = lista +
  figurinha · 6º–9º = **PIN de 4 números** (figurinha infantiliza adolescente).
- **Casca:** Tesouro (pré/1º/2º) = tudo narrado, botões por ícone, alvos enormes, sem nota visível ·
  Exploradores (3º–5º) = formato da Fábrica de Estrelas · Aventureiros (6º–9º) = SÓBRIO, mais desafio/
  agência, menos fofura, texto ok, mascote mais maduro.
- **Avaliação:** parecer descritivo nos anos iniciais; nota entra naturalmente nos finais.

## 7. ASSETS & VOZ (pipeline — TUDO por workflow, nunca pelo chat)
- Imagem: `_gerar_imagens.json` + push `[imagens]` (Gemini, lote) ou `gerar-imagens.yml` (pollinations grátis
  p/ cenas; gemini p/ recorte). Mascote/props: fundo branco, contorno fechado, em camadas p/ animar.
- Voz: `gerar-audio.yml` — **`modelo=female` (Francisca) p/ mascote menina** (Nara), `male` (Antônio)
  p/ menino. Passar **`outdir=<pasta>/audio`** (ex. `_clima/audio`) p/ o mp3 cair DENTRO da atividade —
  senão vai pro `_audio/` comum e os ids (p1..p5,r1,r2,final) **colidem com os da Fábrica de Estrelas**.
  Lote inline OU `_lote_falas.json`. Uma fala por id chamado por `falar()/depoisDaFala()` no HTML.
- Otimizar antes de publicar: **cenas fotográficas (biomas) → JPG ~720px** (12 MB → 0,5 MB, PC fraco);
  mascote/props/ícones → PNG transparente enxuto. Gerar **ícones PWA reais** + `manifest`/`theme` da
  atividade (não deixar restos do clone). Testar render headless (capa + parada + a cabeça do mascote).

## 8. PUBLICAÇÃO & PORTAL
- Cada atividade no **seu repo** (`fabrica.yml` cria; `atualizar.yml` espelha). Portal LEVE só linka.
- Card no `_portal` (objeto `ATIVIDADES["turma"]`) na turma certa = a **sequência didática**.
- A criança se identifica **1x no portal**; a atividade **herda** o aluno (mesmo domínio). NÃO pedir nome de novo.
- **Firebase** (2 cliques do Marcos, `FIREBASE-EDUCAVERSO.md`) = registro pra valer (turma inteira, qualquer aparelho).

## 9. CHECKLIST FINAL (o teste de fogo — reprova se algum falhar)
- [ ] Toda parada é PRODUÇÃO (a criança constrói; nada de escolher alternativa).
- [ ] Concreto antes do símbolo; problema antes do conceito; consequência no mundo (sem X).
- [ ] Cada parada mapeada a uma habilidade BNCC real (verificada) + item de transferência.
- [ ] Motor herdado funcionando (BKT, Leitner/Aquecimento, autoexplicação, medição→parecer).
- [ ] Mascote pergunta (não responde); voz Antônio; lip-sync; animação profissional; sem emoji visível.
- [ ] Faixa correta (identificação/casca/avaliação); PC fraco ok; ~55 min (auditor).
- [ ] Portões 0/1/Arte + prévia e aprovação do Marcos ANTES de publicar.
- [ ] Publicado no repo próprio + card no portal na turma certa.
