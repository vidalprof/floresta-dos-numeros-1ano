# 🏭 FÁBRICA DE MUNDOS VIVOS

**Projeto do professor Marcos — jul/2026**

> **Tese:** entra **TEMA + TURMA**, sai o **mundo publicado** (repositório próprio, link no ar e card no hub "Ilhas do Saber"). Um mundo inteiro é descrito em **um único JSON** (o TEMA‑SPEC); a fábrica clona o motor "Mundo Vivo" byte a byte, troca só as zonas de dados e engole o resto com workflows.

Este manual foi escrito **depois** da dissecação real do motor de referência (`_pub_confeitaria/mundo/index.html`, 1749 linhas) e **corrigido item a item** pelo veredito do cético. **Nenhum furo conhecido ficou de fora** — os 12 apontamentos do cético viraram itens explícitos nas seções 3, 4 e 5.

**Descoberta que sustenta a fábrica:** multiplicação de 3º ano **não exige modo novo**. O motor já roteia `op:"×"` → cena "A‑montar" (bandeja/porão infinito, total revelado no fim) e `prop:1` → cena B "tot" (dobro/proporção). Os modos A / A2 / A‑montar / B / D cobrem multiplicação concreta, arranjos retangulares, proporção e dinheiro. **Porém** (ver §3, costura 1) a *cena montada* só sai certa depois de uma costura que o arquiteto não tinha visto — sem ela, "3 redes de 5" vira "5 redes de 3" na tela.

---

## 1. A LINHA DE MONTAGEM (do pedido do Marcos ao link no ar)

Legenda de quem faz: **🏭 fábrica** (workflow/script automático) · **🪙 modelo barato** (mecânico, delegável) · **👨‍🏫 professor** (decisão pedagógica / aprovação).

| # | Passo | Quem faz | Observação |
|---|---|---|---|
| 1 | **Pedido:** Marcos informa TEMA + TURMA + conteúdo + BNCC + faixa numérica | 👨‍🏫 | As 5 alavancas do bloco `entrada` do TEMA‑SPEC. Pedagogia é irredutível. |
| 2 | **Rascunho das paradas/missões** (progressão, dificuldade) | 🪙 rascunha do molde → 👨‍🏫 aprova/ajusta | 1ª aprovação do Marcos. |
| 3 | **Compilar TEMA‑SPEC → `_gerar_imagens.json`** (prompts de cartelas) | 🪙 | Interpola prompts de mascote, fachadas, interiores, itens do léxico, recipientes e `assets_cenario`. |
| 4 | **Gerar cartelas (PNGs) no Gemini** — commit `[imagens]` | 🏭 `finalizar.yml` + Gemini | Ver §3 costura 6: o trigger precisa apontar pra branch de trabalho. |
| 5 | **Aprovar/regerar cartelas** (montagem visual das provas) | 🪙 monta a prova → 👨‍🏫 aprova o visual | 2ª aprovação. Reprovados voltam num `_gerar_imagens.json` só com os ruins. |
| 6 | **Cortar sprites** (canvas comum, pés alinhados — cura o "piscar") | 🪙 `cortar_sprites.py` + conferência do autocrop | — |
| 7 | **Medir `FACH_INFO`** (fração‑x da porta + aspecto de cada fachada) | 🪙 mede → 👨‍🏫 **confere (visão obrigatória)** | Furo 10 do cético: é inspeção visual precisa, **não** é roteirizável às cegas. Porta fora do lugar = NPC no meio da rua. |
| 8 | **Montar o HTML** (todas as zonas de dados, na ordem, `node --check` por âncora) | 🪙 executa o injetor | O **injetor por âncora ainda não existe** — é costura 6. Arquivo de 3 MB: editar por âncora única, nunca regex gulosa. |
| 9 | **Extrair falas em runtime** → `_lote_falas.json` | 🪙 dispara `extrair_falas.py` | Ferramenta **ainda não existe** (costura 4). Instrumenta `falar()` e pega a string **exata** — a chave DJB2 sai daí, nunca de texto reescrito à mão. |
| 10 | **Gerar MP3** (edge‑tts `pt-BR-AntonioNeural`) — commit `[audio]` | 🏭 `finalizar.yml` | — |
| 11 | **Copiar MP3 `_audio/`→`<_pub>/audio/` + preencher `AUDIO_TXT` + diff zero‑mudez** | 🪙 | Furo 9 do cético: passo manual que **não tinha linha própria**. O diff (toda chave capturada existe em `AUDIO_TXT`) é o portão anti‑mudez. |
| 12 | **QA técnico** (`node --check`, cobertura de áudio) | 🏭 CI + 🪙 lê o diff | — |
| 13 | **QA visual** (headless; abrir cada cena, **errar de propósito**, ver consequência) | 🏭 gera capturas + 🪙 dispara → 👨‍🏫 aprova o mundo jogável | 3ª aprovação. Retrato 390×780 e paisagem, `--virtual-time-budget=4500`. |
| 14 | **Publicar o repositório** (`fabrica.yml`, `repo_name=<slug>`) | 🏭 + 🪙 1 disparo | Repo público + Pages via `PAGES_TOKEN`. |
| 15 | **Confirmar / consertar o build** (`deploy-pages.yml`; `republicar-limpo.yml` se histórico inchou) | 🏭 + 🪙 lê status | — |
| 16 | **Card no hub** (Pillow autocrop → ~200px; `ATIVIDADES["fase:turma"]` com **link**, nunca cópia) | 🪙 extrai/insere → 👨‍🏫 aprova mascote + posição | `desc` e `ic` saem de `meta.card_hub` (furo 11). |
| 17 | **Entrega:** link `https://vidalprof.github.io/<slug>/` | 🏭 | — |

**Regra de ouro:** o professor **decide a pedagogia e aprova o visual**; a fábrica engole o resto. Restam **3 aprovações do Marcos** (pacote de missões · cartelas · mundo jogável) + o mascote do card.

---

## 2. O TEMA‑SPEC campo a campo

Arquivo único (`_fabrica_mundos/TEMA-<slug>.json`). Exemplo completo e corrigido: `_fabrica_mundos/TEMA-EXEMPLO-mar-3ano.json`. **Nada do MOTOR aparece aqui** — nenhuma função, nenhum `mmCena*`, nenhuma física. Só dados.

| Bloco | Campos | Vira o quê no clone | Fonte do furo corrigido |
|---|---|---|---|
| `entrada` | `tema`, `turma`, `conteudo`, `bncc[]`, `faixa_numerica{min,max,total_max}` | As 5 alavancas do professor. Dirige todos os prompts e a escolha de modos. | — |
| `meta` | `slug`, `nome_mundo`, `subtitulo`, `fase_hub`, `save_key`, **`nome_fallback`**, **`logo{linha1,linha2,sub}`**, **`card_hub{desc,ic}`** | `<title>` (7), chave do hub, save (549‑552), o texto que substitui `S.nome||'chef'`, as **duas** telas de abertura, o card do hub | `nome_fallback`/furo 7 · `logo`/furo 5 · `card_hub`/furo 11 |
| `paleta` | `fundo_topo`, `fundo_base`, `acento`, `plaquinha`, `tom_hub`, **`splash{topo,meio,base}`** | `:root`/`body` (12) + acentos; e o gradiente do `#mvSplash` (341) | `splash`/furo 5 (o gradiente do splash é paleta e **não** morava no `:root`) |
| `mascote` | `nome`, `papel`, `poses[]`, `cartela_prompt` | `IMG.mFeliz`/`mFala` + `__MV_IMG` (caminhada) | — |
| `lexico` | `itens[]{palavra[],sprite}`, `recipientes[]{palavra[],nome,fem,gente,sprite}` | Alimenta `mmDoceImg`/`mmLugar` **e** a contagem de grupos e os rótulos do roteador | furos 1 e 8 |
| **`niveis`** | `lista[]{p,n}` (5 patentes) | `NIVEIS` (405) — topbar, HUD, final | **furo 4** (zona órfã) |
| `falas_motor` | 15 chaves | Injeta `MMF` (654‑670) | costura 3 |
| **`diag`** | 11 chaves | Injeta `DIAG` (1287‑1298), narrado no 1º erro | **furo 3** (frases fixas nº 2) |
| `falas_mapa` | `boasVindas`, `meio`, `fim`, **`avisoTrofeu`**, **`avisoTranca`** | `narrarMapa` (629) + avisos narrados (630‑631) | `avisoTrofeu`/`avisoTranca`/furo 6 |
| **`falas_intro`** | `volta`, `primeira` | As 2 falas da tela inicial (583‑584) | **furo 7** |
| **`balao_mapa`** | `texto` (com `{nome}`) | O balão visível do mapa (598) | **furo 7** |
| **`final`** | `titulo`, `lead`, `fala`, `certificado{titulo,texto,assinatura}` | `grandeFinal` (1440‑1450) + certificado imprimível (1451‑1465) | **furo 6** (visível **e** narrado) |
| `assets_cenario` | prompts de `capa`, `trofeu`, céus, chão, medalha | Fundos/objetos globais | — |
| `paradas[]` | `ch`, `ilha`, `titulo`, `hab`, **`uau`**, `fachada_prompt`, `interior_prompt`, `hist`, `gancho`, `tipo`, `missoes[]` | `PARADAS` (431) + `HAB` (1426) + `FACH_INFO` (1600) + `UAU_FASE` (417) | **`uau`/furo 2** |

**Regra de compilação (formulário do professor → `desafios` do motor):**
- `conteudo:"multiplicação"` + "quantos ao todo" ⇒ `{en, r, op:"×", ng:<nº de grupos>}`.
- "quantos em cada / para quantos" ⇒ `{en, r, d, v}` (A/A2).
- proporção / dobro ⇒ `{en, r, prop:1, expl}` (B "tot").
- repartir igual ⇒ `{en, r, op:"÷", ng:<nº de grupos>}`.
- dinheiro ⇒ `{cents, n, q, un}` — **o motor monta o enunciado sozinho**.
- item e recipiente do texto são resolvidos pelo **léxico** (não mais por vocabulário fixo).

> **Campo novo `ng` (número de grupos) — a correção‑chave do cético.** É ele que diz ao roteador quantos grupos existem, **sem** depender da regex de vocabulário travado. Ver §3 costura 1. Sem `ng`, o próprio exemplo‑carro‑chefe monta a cena errada.

---

## 3. COSTURAS A DESCOLAR **antes** do primeiro mundo fabricado

Lista priorizada. Todos os **12 furos do cético** estão incorporados. O que toca **função do motor** é trabalho de **modelo forte** (não improvisar num arquivo de 3 MB) e obriga a re‑rodar o QA inteiro.

| # | Costura | Furo(s) do cético | Onde (linha) | Conserto | Toca o motor? | Prioridade |
|---|---|---|---|---|---|---|
| **1** | **Contagem de grupos data‑driven.** O roteador reconhece `op:"×"/"÷"`, mas extrai o nº de grupos por regex de vocabulário confeitaria: `/(\d+)\s+(caixas\|amigos\|bandejas\|mesas\|sacolinhas\|potes\|cestas\|pratos)/i`. Nenhuma palavra pirata casa. "Monte **3 redes** com 5 peixes" → cai no fallback e monta **5 redes de 3**: a cena **contradiz** o enunciado e a fala. Bug pedagógico, não cosmético. | **1** | 999‑1010 | Ler o `ng` do desafio compilado (ex.: `{op:"×", ng:3}`) **ou** casar as palavras via `lexico.recipientes`. Eliminar a heurística por vocabulário fixo. | **Sim (forte)** | **🔴 1 — bloqueante / MAIS URGENTE** |
| **2** | **Léxico data‑driven** em `mmDoceImg`/`mmLugar` (vocabulário confeitaria embutido: brigadeiro/cupcake/Mesa/Sacolinha) **+** rótulos `"Bandeja"` fixos vazados **dentro** do roteador (`lug:{n:"Bandeja",img:IMG.dPrato}` e `lugN:"Bandeja"`). | 8 | 672‑693; 995, 1013‑1017 | `mmDoceImg`/`mmLugar` leem o `lexico`; os `"Bandeja"`/`dPrato` fixos dos ramos passam a chamar `mmLugar(d.en)`. | **Sim (forte)** | 🔴 2 — bloqueante |
| **3** | **Falas fixas do motor injetadas.** `MMF` (15 frases: "doce/Chef/bandeja/loja") **e** `DIAG` (11 frases de diagnóstico narradas no 1º erro, ex. "aqui a gente reparte… é conta de dividir!"). Num mundo de multiplicação, o `DIAG` daria **dica invertida**. | **3** | 654‑670; 1287‑1298 | `MMF`←`falas_motor` e `DIAG`←`diag`, injetados do spec. Sem os dois, "falas do motor" fica pela metade. | **Sim (forte)** | 🔴 3 — bloqueante |
| **4** | **Extrair falas por runtime.** O `id` do lote vem da string de tela; o `texto` gravado é a versão falada — **divergem por design** e não há ferramenta. Uma fala vira **silêncio em sala** e passa no QA visual. O próprio exemplo do arquiteto (§5.4, chave `vg0129n` sobre "…3 redes…" ≠ `falaEn:d.en` que fala "…Monte 3 redes…") já mordeu. | **12** | 366 / 1005 / lote | Construir **`extrair_falas.py`** que instrumenta `falar()`, pega a string **exata**, calcula a chave DJB2 e casa com o `texto`. **Diff obrigatório** contra `AUDIO_TXT` antes de fechar. | Adjacente (forte) | 🔴 4 — alto risco (mudez) |
| **5** | **Zonas de dados órfãs** (fora do mapa do montador, com texto **visível e/ou narrado**): `UAU_FASE` (curiosidade por fase), `NIVEIS` (5 patentes), splash `#mvSplash` + título JS + gradiente, `grandeFinal`+certificado+`avisoTrofeu`, falas da tela inicial + balão do mapa + fallback `'chef'`. Todas ensinariam/mostrariam **confeitaria/divisão** num mundo pirata. | **2,4,5,6,7** | 417‑429; 405; 341‑345/571‑572; 1440‑1465/631; 583‑584/598 | Adicionar ao spec (`paradas[].uau`, `niveis`, `meta.logo`+`paleta.splash`, `final`, `falas_intro`+`balao_mapa`+`meta.nome_fallback`) e **incluir cada uma na Fase C e no lote de áudio**. | Dados (mas fora do mapa das 9 zonas) | 🔴 5 — bloqueante |
| **6** | **Infra do pipeline.** (a) `finalizar.yml` dispara **só** na branch `claude/github-pages-deploy-wbb7dy` (linha 13): commits `[imagens]`/`[audio]` na `main` **não rodam, sem erro**. (b) job `[publicar]` é 100% hardcoded p/ confeitaria (`SRC/DEST/OWNER`) — inútil p/ mundo novo (publicar é via `fabrica.yml`). (c) `extrair_falas.py` e o **injetor por âncora** foram marcados "automáticos" mas **não existem**. (d) copiar MP3 + preencher `AUDIO_TXT` é passo manual **sem linha** na tabela. | **9** | `finalizar.yml` 11‑13, 161‑168 | Repontar/duplicar o trigger p/ a branch de trabalho; **construir** `extrair_falas.py` e o injetor antes de chamá‑los de automáticos; dar linha própria a "copiar MP3 + `AUDIO_TXT`" (feito, §1 passo 11). | Infra | 🟠 6 — bloqueante p/ automação |
| **7** | **`FACH_INFO` é etapa de visão humana.** Medir fração‑x da porta + aspecto de 8‑13 fachadas geradas por IA é inspeção precisa por imagem, **não** roteirizável por "modelo barato". A tabela honesta antiga dobrava isso em "montar HTML". | **10** | 1600‑1602 | Linha própria na tabela (§4) como etapa de **visão com conferência humana obrigatória**, ou automatizar com detecção de porta + validar. | Processo | 🟠 7 |
| **8** | **Fallback genérico + rótulos globais.** Chave `IMG.dBiscoito` como fallback universal; `<title>`/save/`HAB`; boas‑vindas. | (parte de A/D/E do arquiteto) | 354‑364; 7,549,1426; 629 | Fallback vira slot `IMG.item0` resolvido pelo léxico; resto ←`meta`/`paradas`/`falas_mapa`. Saem de carona junto de 1‑3. | Dados | 🟢 8 |
| **9** | **`meta.card_hub{desc,ic}`.** `desc` e `ic` do card do hub eram inventados na hora, fora do "um mundo = um JSON". | **11** | Fase G | Campo no spec (feito). | Dados | 🟢 9 |
| **10** | **Conforto de escala** (não bloqueia): parametrizar `[publicar]` por marcador; `cortar_sprites.py` aceitar layout (linhas×colunas, altura‑alvo) por argumento. | — | `finalizar.yml` 166‑168; `cortar_sprites.py` 11‑12 | Só se quiser atalho por marcador / cartelas de layouts variados. | Infra | 🟢 10 — opcional |

**Resumo honesto:** o coração da fábrica são **as costuras 1 → 5** (grupos data‑driven, léxico, `MMF`+`DIAG` injetados, falas por runtime e as 5 zonas órfãs). Sem elas, "trocar 2 entradas" é mentira: o mundo pirata montaria a **cena errada** (furo 1), daria **dica de dividir** no erro (furo 3), abriria escrito **"A RUAZINHA DOS DOCES"** (furo 5), premiaria com **"Mestre da Divisão"** (furo 6) e poderia **emudecer** em sala (furo 4). Todas tocam o motor ou são conteúdo ativo → **modelo forte** + re‑rodar o QA §QA. As costuras 6‑10 são automação e conforto, não pré‑requisito pedagógico.

---

## 4. TABELA HONESTA — automática / delegável / professor (corrigida)

| Etapa | 🏭 Automática | 🪙 Modelo barato | 👨‍🏫 Professor |
|---|---|---|---|
| Definir tema+turma+conteúdo+BNCC | — | — | **✅ pedagogia (irredutível)** |
| Escrever `paradas`/`missoes` | — | rascunho do molde | **✅ aprova/ajusta** |
| Compilar TEMA‑SPEC → `_gerar_imagens.json` | — | ✅ interpola prompts | — |
| Gerar PNGs (`[imagens]`) | ✅ `finalizar.yml`+Gemini | — | — |
| Aprovar/regerar cartelas | — | ✅ monta as provas | **✅ aprova o visual** |
| Corte de sprites | — | ✅ `cortar_sprites.py` | conferência do autocrop |
| **Medir `FACH_INFO` (fração‑x da porta + aspecto)** | (só se automatizar detecção de porta) | mede | **✅ conferência de VISÃO obrigatória** — *furo 10, linha nova* |
| Montar HTML (todas as zonas, ordem + `node --check`) | injetor por âncora — **⚠️ a construir** | ✅ executa o injetor | — |
| **Extrair falas** → `_lote_falas.json` | **⚠️ `extrair_falas.py` a construir** (runtime) | ✅ dispara | — |
| Gerar MP3 (`[audio]`) | ✅ `finalizar.yml`+edge‑tts | — | — |
| **Copiar MP3 → `<_pub>/audio/` + preencher `AUDIO_TXT` + diff zero‑mudez** | — | ✅ copia/preenche/lê o diff | — *(furo 9, linha nova)* |
| QA técnico (`node --check`, cobertura de áudio) | ✅ CI | ✅ lê o diff | — |
| QA visual (screenshots headless, errar de propósito) | ✅ gera capturas | ✅ dispara | **✅ aprova o mundo jogável** |
| Publicar repo (`fabrica.yml`) | ✅ | ✅ 1 disparo | — |
| Confirmar/consertar build | ✅ `deploy-pages`/`republicar-limpo` | ✅ lê status | — |
| Card no hub | ✅ Pillow+republicar | ✅ extrai/insere | **✅ aprova mascote + posição** |

*Correções do cético nesta tabela:* `FACH_INFO` deixou de ser dobrada em "montar HTML" e ganhou linha de **visão humana**; "copiar MP3 + `AUDIO_TXT`" ganhou linha própria; `extrair_falas.py` e o injetor estão marcados **"a construir"** — não são automáticos hoje.

---

## 5. ESTIMATIVA HONESTA — custo e tempo por mundo novo

### Hoje (antes das costuras 1‑5)
**Não dá pra "fabricar" de verdade.** Trocar só os dados produz um mundo **quebrado**: a multiplicação monta a cena errada (furo 1), o erro sugere dividir (furo 3), o splash/certificado/níveis saem "Confeitaria/Divisão" (furos 4‑6) e uma fala pode virar silêncio (furo 4). Fazer um mundo hoje = **edição manual de modelo forte** no arquivo de 3 MB, caça a strings vazadas em ~15 pontos, **alto risco de bug chegar em sala**. Ordem de **dias**, não horas — e frágil.

### Depois das costuras 1‑5 (+ 6 pra automação)
- **Trabalho humano/modelo:** **~2‑4 h** — escrever o TEMA‑SPEC, revisar cartelas e o mundo jogável.
- **Aprovações do Marcos:** **3 rodadas** (missões · cartelas · mundo jogável) + mascote do card.
- **Espera de workflow (paralela ao resto):** imagens ~10‑20 min · áudio ~5‑10 min · build do Pages ~1‑2 min (ou `republicar-limpo` se o histórico inchar).
- **Custo de API:** Gemini para ~15‑25 cartelas (baixo) + **edge‑tts grátis**. Modelo **forte** entra **uma vez** (nas costuras); depois, cada mundo é **modelo barato + workflows**.

> **Investimento único:** descolar as costuras 1‑5 é o único gasto real de engenharia (modelo forte, com re‑QA). Feito isso, "tema + turma → mundo" passa a ser, de fato, **preencher um TEMA‑SPEC, apertar 3 aprovações e deixar os workflows engolirem o resto**.

---

### Arquivos‑âncora
- Motor+dados de referência: `/home/user/floresta-dos-numeros-1ano/_pub_confeitaria/mundo/index.html`
- Pipeline: `/home/user/floresta-dos-numeros-1ano/.github/workflows/finalizar.yml`
- Corte de sprites: `/home/user/floresta-dos-numeros-1ano/_ferramentas/cortar_sprites.py`
- Contratos: `/home/user/floresta-dos-numeros-1ano/MUNDO-VIVO-MOTOR.md`, `MUNDO-VIVO-ESPINHA.md`
- TEMA‑SPEC de exemplo (corrigido): `/home/user/floresta-dos-numeros-1ano/_fabrica_mundos/TEMA-EXEMPLO-mar-3ano.json`
