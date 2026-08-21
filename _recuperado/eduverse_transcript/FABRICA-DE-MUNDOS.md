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
