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
9. **CURADORIA, NÃO SORTEIO (lei do Marcos, 2026-07-22 — ele pegou isso na Fábrica de Estrelas).** O
   CONTEÚDO (o que se pede, a dificuldade, os alvos, os casos) é uma **PROGRESSÃO PENSADA**, escrita à
   mão numa ordem que ensina — **nunca gerado por `Math.random()`**. Sorteio só é permitido para o
   **cosmético** (posição de partícula, tempo de piscar, variação de som) e para **embaralhar a POSIÇÃO
   das opções** (anti-viés, p/ a criança não decorar "é sempre o 2º botão"). **Proibido sortear a
   substância pedagógica** (números do problema, qual bioma pedir, ordem de dificuldade) — isso deixa a
   atividade arbitrária, inconsistente e "rasa". Ex. certo: `alvos=["floresta","deserto","taiga"]`
   (curado); ex. errado: pegar dois números aleatórios e mandar multiplicar.

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
**FINAL DA HISTÓRIA de verdade (lei do Marcos — a Fábrica de Estrelas ficou sem isso):** a aventura
tem que **FECHAR a narrativa** — um **epílogo animado** onde a missão se resolve, o mundo curado
aparece por inteiro, o mascote comemora/agradece e o arco da criança conclui (emoção, não só a tela de
nota/parecer). Tela de resultado ≠ final da história; precisa dos DOIS. **NÃO pode ser curta:** poucas
paradas = reprova (o Marcos achou a Estrelas curta) → garantir as **~10–12 paradas** e o tempo cheio.
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
5. **LIP-FLAP NÍTIDO (não "fantasma").** NÃO deixar a boca em opacidade contínua — a meia opacidade
   mostra uma boca meio-aberta translúcida por cima da fechada = parece bug. A boca fica **ABERTA ou
   FECHADA** (0/1), trocando rápido, com **histerese** (abre >0,30, fecha <0,14 da RMS) p/ não tremular.
   Só o **gesto do corpo** (baloiço macio) usa o valor suavizado.
6. **TODA POSE DE GESTO VOLTA À NEUTRA (bug pago — o braço levantado).** `comemora`/`aponta`/`acena`
   levantam o braço; se não voltarem, a Nara **narra a explicação com a mão no ar** ("o tempo todo").
   Regra: (a) toda pose de gesto tem **timer de retorno** à `base` (~1,4s), como o `pensa` já faz; e
   (b) **ao COMEÇAR a narrar** (`falar()`), se estiver num gesto, volta à `base` ANTES de falar — a
   narração nunca começa com a mão levantada. Item fixo do QA do mascote.
7. **LIP-SYNC POR VISEMAS (padrão-ouro, JÁ IMPLEMENTADO na Nara — usar nas próximas):** em vez de 2
   estados (aberto/fechado por RMS), usar **4–6 formas de boca** que formam as sílabas. Pipeline
   (tudo no BUILD): **(a)** gerar as bocas por IA editando a base (`_gerar_imagens.json`: "muda SÓ a
   boca" — meio-aberta, bem aberta, 'O'…) e compor **só a elipse da boca** na base (como item 3);
   **(b)** no `gerar-audio.yml` passar **`visemas=sim`** (ou `so_visemas=sim` p/ áudio já existente) →
   ele roda o **Rhubarb** (`-r phonetic` = funciona em PT: mp3→ffmpeg wav→rhubarb→JSON) e commita
   `<pasta>/visemas.json` (tempo→letra A..X); **(c)** o app faz `fetch("visemas.json")`, mapeia
   letra→boca (A/X=fechada, B/C/H=meio, D/G=aberta, E/F='O') e **troca a imagem da boca** no
   `narr.currentTime` — leve, offline, sem lib. **Fallback**: se não houver timeline p/ a fala, cai no
   flap nítido por RMS (nunca fica mudo/travado). Novos ids de fala → rodar `visemas=sim` p/ recalcular.

## 4⅗. ATRATIVO = JOGO, NÃO FORMULÁRIO (lei do Marcos, 2026-07-22) ⭐ OBRIGATÓRIO
O que ensina certo mas parece **formulário** (medidores +/−, lista de linhas, "escolha o rótulo") **não
prende** o aluno — ainda mais do 6º ano pra cima. Regra: a criança **brinca COM o mundo**, não preenche.
- **INTERAÇÃO DIRETA no objeto de estudo:** toca/arrasta/pinta **direto no planeta/mapa/cena**, não em
  um controle abstrato ao lado. Fora os +/− sempre que der: vira **tocar a faixa que reage**, **arrastar
  para a região**, **girar o dial e o bioma nascer**, **subir a montanha com o dedo**.
- **REAÇÃO VISUAL + RECOMPENSA a cada ação:** mexeu → o mundo se transforma NA HORA (cor, partícula,
  brilho, som, hit-stop). O acerto **ACENDE** a coisa (glow + ✓). O feedback É o mundo reagindo.
- **MISSÃO com stakes:** enredo de jogo ("o planeta está apagado — reacenda cada faixa"), progresso
  épico, desbloqueios, o mascote reagindo com emoção. A medida (evidência) continua por baixo.
- **SIMULAÇÃO REAL, não script:** um **modelo** de verdade por trás (ex.: `bioma(temperatura, chuva)`,
  ângulo do Sol → temperatura, altitude → clima) que responde a QUALQUER combinação — com **resposta
  visual imediata**. "Simulação real" = modelo correto + reação visível; **NÃO** é 3D pesado: faz-se
  com CSS/Canvas 2D/partículas/ruído procedural, leve, PC fraco. (Ver a pesquisa do arsenal técnico.)
- **Régua:** se a tela parece um **questionário/planilha**, REPROVA — reprojetar como manipulação do mundo.

## 4⅘. DIDÁTICA SEM AULA — como "explicar a matéria" sem virar lousa (lei do Marcos)
Ser **didático e progressivo** é exigido pelas leis; **aula/vídeo/texto OBRIGATÓRIO antes de agir** as
**viola** (conceito primeiro → a criança desliga). O embasamento certo é **descoberta + apoio atrativo**:
- **ANDAIME (torna fácil sem entregar):** (1) **beat concreto** primeiro (a criança SENTE o fenômeno —
  ex.: o Sol batendo direto × de lado); (2) **exemplo trabalhado** do mascote ("eu faço" — 1 item já
  pronto); (3) a criança completa com **✓ na hora por item** (fim do "tudo certo ou nada"); (4) só então
  o símbolo/nome (CPA).
- **EXPLICAÇÃO como DINÂMICA atrativa** (o "vídeo bom"), nunca passiva:
  · **mini-cutscene animada narrada** (20–30s: a cena se move enquanto o mascote explica; **termina
    virando ação**) · **infográfico "descobrir tocando"** (toca a parte → revela o porquê) · **a própria
    simulação explica** (mexeu → viu → entendeu).
- **"Saiba mais" OPCIONAL:** botão que abre um texto/animação curta **só se a criança quiser** — dá o
  embasamento sem obrigar. (Já existe na parada 1 do Planeta Vivo.)
- **~10–12 beats para 55 min** (5 é pouco): variar o "verbo da mão" a cada um, com **revisão espaçada** no meio.

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
- **POR DISCIPLINA — a demanda cognitiva muda a mecânica (lei do Marcos, 2026-07-22):**
  · **Matemática/procedimental** = o aluno **EXECUTA** um procedimento → produção passo-a-passo (montar,
    contar, compor) já basta. · **Geografia/Ciências/Sociais** = o aluno precisa **COMPREENDER** padrões
    espaciais e sistemas de causa-efeito, e **ler/construir representações** (mapas, gráficos, perfis) →
    exige **SIMULAÇÃO REAL + mecânicas VISUAIS/ESPACIAIS** (mapa em camadas, construir climograma, corte
    do relevo, girar variáveis e o resultado emergir no mapa). Formulário aqui mata a compreensão.
  · O **pedagogo escolhe a mecânica pela demanda da disciplina**, não por moldar tudo igual. As mecânicas
    específicas por disciplina estão no `CATALOGO-DINAMICAS-INTERATIVAS.md` (e nas pesquisas profundas de
    2026-07: mecânicas de geografia + arsenal técnico — alimentam o catálogo quando chegam).

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

> **⭐ A PROVA DOS 6 (critério do Marcos, 2026-07-22) — toda atividade tem que dar SIM nos seis:**
> **(1) o aluno AMA** (atrativa, jogo) · **(2) CONSEGUE FAZER** (jogável, sem travar, alvo grande) ·
> **(3) APRENDE DE VERDADE** (ativa/real, produção, não decoreba) · **(4) MENSURADA** (medida por baixo →
> parecer/nota) · **(5) INSTRUTIVA** (explica a matéria ensinando, sem lousa) · **(6) ENTENDE** (compreensão
> real, não só acertar). É o mix certo: **leque de mecânicas variadas + motor medido + simulação real**.

- [ ] Toda parada é PRODUÇÃO (a criança constrói; nada de escolher alternativa).
- [ ] **JOGO, não formulário:** manipulação direta no mundo + reação visual/recompensa a cada ação;
      nenhuma tela parece questionário/planilha (§4⅗).
- [ ] **Simulação REAL** (modelo por trás, resposta visual imediata) onde a disciplina pede COMPREENDER
      (geografia/ciências) — não script, não 3D pesado.
- [ ] **Explicação como dinâmica** (cutscene animada / infográfico tocável / a simulação) + "Saiba mais"
      OPCIONAL — nunca aula/vídeo obrigatório antes de agir (§4⅘).
- [ ] Concreto antes do símbolo; problema antes do conceito; consequência no mundo (sem X).
- [ ] Andaime: beat concreto → exemplo trabalhado → ✓ na hora por item (sem "tudo certo ou nada").
- [ ] Cada parada mapeada a uma habilidade BNCC real (verificada) + item de transferência.
- [ ] **~10–12 beats** para ~55 min, "verbo da mão" diferente a cada um + revisão espaçada no meio.
- [ ] Motor herdado funcionando (BKT, Leitner/Aquecimento, autoexplicação, medição→parecer).
- [ ] Mascote pergunta (não responde); **voz coerente com o personagem** (menina→Francisca, menino→Antônio);
      **lip-flap nítido** (sem "fantasma"); **toda pose de gesto volta à neutra** (sem braço no ar ao narrar);
      recorte transparente (sem quadrado); animação profissional; sem emoji visível.
- [ ] Faixa correta (identificação/casca/avaliação/disciplina); PC fraco ok; ~55 min (auditor).
- [ ] Portões 0/1/Arte + prévia e aprovação do Marcos ANTES de publicar.
- [ ] Publicado no repo próprio + card no portal na turma certa.
