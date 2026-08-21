# EduVerse — A LINHA DE MONTAGEM (fluxo completo, automático e auditado)

> Objetivo do Marcos: **uma fábrica onde cada especialista faz sua parte e o produto
> sai PRONTO e ESPETACULAR, sem ele corrigir arte no braço.** Este documento define o
> fluxo inteiro — do briefing/currículo até o `index.html` publicado e auditado —, os
> **portões automáticos** que faltam (Arte, Coerência, Variedade), o **contrato de dados
> único** (a história mora nos DADOS, nunca no motor) e um **plano de execução
> sequenciado**. Regra-mãe: **terminar o FLUXO antes de produzir a próxima atividade.**

---

## 0. Diagnóstico honesto de hoje

A linha **já é data-driven pela metade**: `montar.py` injeta geometria/tema/mecânica/NPCs/props
a partir de `dados.json`, e o `runner.py` tem uma infra real de Chromium headless
(screenshots, `_qaTeleport`, `_qaState`, comparação de pixels) provada nos gates técnicos.
O que quebra é tudo o que **ficou cravado no motor** e **tudo o que nenhum portão olha**:

1. **A HISTÓRIA está no CÓDIGO do motor** (`kit-floresta.py`), não nos dados. O subtítulo
   HTML fixo (`kit-floresta.py:67-68` "pegue a chave dourada / leve-a até o labirinto")
   **vaza** para o Pomar porque `montar.py` só troca `__TITULO__/__EMOJI__` e a geometria —
   nunca os textos. Balões de intro/chave/arco/HUD/fim também são literais no motor.
2. **Não existe PORTÃO DE ARTE nem de COERÊNCIA nem de VARIEDADE.** O único gate que toca
   arte/pedagogia é `runner.py:96-99` (`pedagogia_arco`) e ele **nem chama `gate()`** —
   vira `PENDENTE_HUMANO` e empurra a arte pro Marcos. Por isso o auditor **APROVOU** maçã
   flutuando, cabana desproporcional e coelho repetitivo.
3. **O laudo fica obsoleto**: a esteira não re-audita ao fim de cada especialista (o laudo do
   Pomar diz `som_voz_embutida: FALHA` mesmo com os 52 áudios já embutidos no dist atual).
4. **Faltam metadados de proporção/âncora** no `registro.json` (só `arquivo/tipo/tema/origem/
   bytes`) — sem altura em px nem escala-vs-Byte, é impossível **cobrar** proporção.
5. **Fantasias são vaporware**: `gerar-imagens.yml` grava em `_novo/` solto, não alimenta a
   biblioteca nem gera as 6 poses.

O conserto é **fechar a linha**: externalizar a narrativa, criar um **contrato de dados
único**, e ligar **3 portões novos** ao `runner.py` reusando a infra Chromium que já existe.

---

## 1. A LINHA DE MONTAGEM COMPLETA (etapa a etapa: entrada → saída)

Cada etapa é uma **função pura** (script Python ou workflow) com ENTRADA e SAÍDA em arquivo
versionado. A esteira `orquestra.py` roda as etapas em ordem, e **só regera o elo cujo
`hash_inputs` mudou** (cache por hash). "Sai pronto" = a saída de cada etapa é o contrato
exato que a próxima consome, sem intervenção humana no meio.

### Etapa 1 — BRIEFING (Coordenação pedagógica)
- **Entrada:** pedido do Marcos `{ habilidade BNCC, faixa (pre|1-2|3-5|6-9), tema do mundo,
  mecânica desejada }`.
- **Saída:** `eduverse/mundos/<slug>/briefing.json` (objetivo curricular + faixa + tema).
- **Automática porque:** é um formulário curto; um validador recusa combinação sem código
  BNCC ou sem faixa. Nada de arte/enredo ainda.

### Etapa 2 — ROTEIRO + BREAKDOWN (Roteirista/Pedagogo)
- **Entrada:** `briefing.json`.
- **Saída:** bloco `roteiro` + `narrativa` + `elenco` dentro de `dados.json` (rascunho):
  premissa, `objetivo_curricular`, **arco de 8 etapas na ordem** (História → Exploração →
  Problema → Experimentação → Descoberta → Conceito → Aplicação → Reflexão), **final
  espetacular roteirizado** (cena, não balão), e por cena o **breakdown**
  `{cenario, hora, clima, personagens, efeitos, props:[{tipo, porque_contexto,
  proporcao_vs_byte}], acao_crianca}`. Falas viram **objetos com TEXTO** (`{id, texto, voz}`),
  e cada NPC ganha `falas[]` por momento (o coelho conta 1 a 1).
- **Automática porque:** produz o CONTRATO que o Diretor de Arte e o Engenheiro consomem;
  o **Portão 0 (Coerência)** valida antes de gastar arte.

### Etapa 3 — CASAMENTO / COMPILADOR DE SPEC (valida o contrato)
- **Entrada:** `dados.json` (rascunho) + `dados.schema.json`.
- **Saída:** `dados.json` validado, ou **ABORTA** citando o campo/linha ofensor.
- **Automática porque:** `jsonschema` reprova cedo (arco fora de ordem, falta objetivo,
  mecânica não serve à faixa, prop sem `porque_contexto`/`proporcao_vs_byte`).

### Etapa 4 — CATÁLOGO / ARTE (Diretor de Arte + biblioteca)
- **Entrada:** `dados.json.assets` + breakdown de props.
- **Saída:** PNGs em `eduverse/biblioteca/proc/` + entradas em `registro.json` **com
  metadados de proporção/âncora** (`alvo_altura_px`, `escala_vs_byte`, `y_pe`).
- **Automática porque:** `gerar-fantasia.yml` (evolução de `gerar-imagens.yml`) edita a âncora
  via Gemini, gera as **6 poses**, autocrop → resize ~200px → optimize, **grava no proc/ E
  escreve no registro** — fecha o corte gerador↔catálogo. `checar.py` valida que todo id
  referenciado existe (e tem as poses) **antes** do build.

### Etapa 5 — VOZ (Sound Designer)
- **Entrada:** `dados.json.falas[].texto`.
- **Saída:** `_audio/<id>.mp3` (TTS) para cada id.
- **Automática porque:** `gerar-audio.yml` percorre os textos do dado (não do motor) e gera
  todos os mp3; o **gate de voz por cobertura** confere que cada id usado tem áudio.

### Etapa 6 — MONTAGEM (`montar.py`)
- **Entrada:** `dados.json` + `proc/*.png` + `_audio/*.mp3` + motor `kit-floresta.py`.
- **Saída:** `eduverse/dist/<slug>/index.html` autossuficiente (base64 offline).
- **Automática porque:** carimba TODO o `MUNDO` (agora incluindo `MUNDO.historia`) no motor;
  troca `__SUB__/__HINT__/__INTRO__/__HUD__/__FIM__` além de `__TITULO__/__EMOJI__`; e faz
  **sanity forte** (`re.search(r'__[A-Z_]+__', html)` → aborta se sobrou placeholder).

### Etapa 7 — AUDITORIA (`runner.py` = todos os portões)
- **Entrada:** `dist/<slug>/index.html` + `dados.json`.
- **Saída:** `eduverse/missoes/<slug>/laudo.json` + código de saída (0 aprovado / 1 reprovado).
- **Automática porque:** roda os gates TÉCNICOS de hoje **+ os 3 portões novos** (Arte,
  Coerência, Variedade) que **chamam `gate()`** de verdade e param o publish.

### Etapa 8 — RE-MONTA+RE-AUDITA (loop de fechamento)
- **Entrada:** disparo quando `dados.json`/`proc`/`_audio` mudam.
- **Saída:** laudo sempre fresco (nunca obsoleto como o do Pomar).
- **Automática porque:** `orquestra.py` sempre executa `montar → runner` em sequência; o laudo
  reflete o dist ATUAL.

### Etapa 9 — VEREDITO HUMANO (só o que sobra) + PUBLICAÇÃO
- **Entrada:** laudo APROVADO.
- **Saída:** repo próprio da atividade + card no hub `_site` (portal leve por link).
- **Automática porque:** publicação segue o CLAUDE.md (Fábrica/`atualizar.yml`/
  `republicar-limpo.yml`). O Marcos só vê o que os portões **não conseguem** medir — não
  mais a arte que deveria ter sido barrada.

**Cadeia versionada (cache por hash):**
`briefing.json → roteiro/dados.json → schema-ok → assets(registro) → audio → dist/index.html → laudo.json`

---

## 2. A REGRA-MÃE — a história mora nos DADOS (contrato único)

O motor `kit-floresta.py` passa a ser **genérico e mudo**: zero string de enredo. Todo texto
que o produto MOSTRA ou FALA vem de `MUNDO.historia` / `MUNDO.falas[].texto`.

### `eduverse/schema/dados.schema.json` (contrato v1 — seções obrigatórias)

```
identidade    { slug, titulo, emoji, versao }
habilidade    { codigo(BNCC), texto, fonte }
faixa         "pre" | "1-2" | "3-5" | "6-9"
tema          { part, ceu0, ceu1, passaros, borboletas }   // paleta/ambiente
historia      {
                sub,              // subtitulo da tela inicial (substitui kit:67-68)
                hint,             // dica do dpad
                hud, hud_com,     // texto do HUD por estado
                intro  {txt,id},  // balao de abertura (substitui kit:224/266)
                objetivo "colher" | "chave" | ...,   // decide o FLUXO (fim do !MODO_AULA)
                chaveFala {txt,id}, arcoFala {txt,id},// so existem se objetivo=="chave"
                fim {txt,id}, ganchoProx,            // final roteirizado (substitui kit:1012-1013)
                arco  [8 etapas na ordem, cada uma com o que o Byte PERGUNTA],
                final { cena, clima, efeitos, som }  // final espetacular EM CENA
              }
personagem    { sprite_base:"byte", variante, poses[] }
mapa          { WW, WH, start, path, trees, tr, flores, props[] }  // o "mundo" de hoje
mecanica      { id, params, textos:{ anuncio:{tipo}, dica:{tipo} } } // textos por dado
elenco        [ { sprite, nome, rota, vel, escala, falas:[{id,texto}] } ] // NPC nunca repete
falas         [ { id, texto, voz, pitch } ]      // TEXTO no dado, nao IDs cegos
audit         { chegar[], colisao[] }
```

**Fronteira DADO×CÓDIGO:** o motor decide o fluxo por `MUNDO.historia.objetivo` (registro de
mecânicas), **não** mais por `!MODO_AULA` espalhado. Um mundo que declara `objetivo:"colher"`
**nunca** instancia chave/arco/labirinto — nem no desenho, nem no texto, nem na geometria
(as coords órfãs `chave`/`arco` viram **opcionais** em `montar.py`).

**Regra de ouro do produto (navegador antigo):** o HTML gerado continua só `var/function/for`,
sem `grid/gap/clamp/var(--)`, flex com fallback `-webkit-box`, emojis ≤ Unicode 6.0, imagens
PNG base64. (Isto vale para o dist, **não** para os scripts Python da fábrica.)

---

## 3. OS PORTÕES AUTOMÁTICOS (como cada um checa, na prática)

Todos entram no `runner.py` via `gate()` (entram em `falhou` e **param o publish**), com fase
de transição `--avisa` → `--rigoroso`. Reusam a infra Chromium já provada (`_qaTeleport`,
`_qaState`, screenshot + PIL/numpy).

### PORTÃO TÉCNICO (já existe — manter)
`build_existe, node_check, offline_sem_url, peso_ok(<2560KB), render_sem_erro, mecanica_*,
mecanica_colisao, som_no_canto, mundo_vivo, som_ambiente, texto_sem_simbolo`. **Endurecer o
gate de voz**: em vez de `'data:audio/mpeg' in html`, extrair o objeto `FALAS` embutido e
conferir que **todo id usado** (`dados.falas` + os chamados pelo motor) está presente —
reportar quais faltam (cobertura real, não "existe ≥1 áudio").

### PORTÃO DE ARTE — `eduverse/audit/portao_arte.py`
Renderiza o dist no Chromium e injeta `_qaState()` expondo as **bounding-boxes** de Byte/props/
frutas. Gates:
- **`arte_proporcao`** — lê `alvo_altura_px` do `registro.json` e `h` do prop no `dados.json`;
  o Byte é ~64px. Regra: prop de cenário pequeno (fruta/cesta) com `h > K*64` **FALHA**; e no
  screenshot mede a bbox REAL do prop vs a do Byte e compara com a razão declarada. **Cabana
  precisa ser ≥ 3×Byte** (hoje h=118 ≈ 1,8× → hoje passaria, com o gate **reprova por ser
  pequena demais/incoerente**; o alvo é ~200-260px).
- **`arte_sem_flutuante`** — cruza a coord de cada fruta com `mapa.trees`: fruta **pendurada**
  tem que ter tronco/copa num raio X; fruta **caída** tem que tocar o solo. No screenshot:
  fruta = blob colorido **sem pixels de tronco/copa logo abaixo** e **sem sombra** = FALHA.
  Exige `haste/galho` ligando fruta→copa e **sombra** sob a fruta.
- **`arte_area_jogo`** — injeta JS que lê `canvas.width/height` vs `innerWidth/innerHeight`;
  em viewport de 360px de largura, canvas ocupando **< 60%** da tela útil = FALHA.
- **`arte_poses`** — renderiza o Byte de frente/costas/lado e compara **altura de silhueta**
  por bbox: as 3 vistas têm que ter altura parecida; se `byte_costas` cair no fallback de
  `frente` ("andando de ré") a silhueta/pernas destoam = FALHA.
- **`arte_tudo_IA`** — `origem=="IA"` em todo asset usado (barra geométrico code-drawn).

### PORTÃO DE COERÊNCIA — `eduverse/audit/portao_coerencia.py`
Extrai **todo texto que o produto mostra/fala** (subtítulo, HUD, `balao(...)`, `playFala`,
`MUNDO.historia.*`, `falas[].texto`) e cruza com o **LÉXICO DO TEMA** vindo dos dados
(`tema/titulo`, `assets`, `mecanica.id`). Gates:
- **`coerencia_tema`** — **LISTA NEGRA** de termos de outros mundos: quando
  `historia.objetivo != "chave"`, qualquer ocorrência de `{labirinto, chave dourada, pedra,
  Nimbo, jaula}` no HTML final = **FALHA** citando a linha. **LISTA BRANCA** esperada por tema
  (pomar: fruta, colher, contar, cesta, árvore). Como a história agora vem do dado, **não há
  como o motor injetar texto de outro mundo** — o portão fecha a porta que sobrar.
- **Curto prazo (custo baixo):** grep direto no dist por `labirinto`/`chave dourada` quando o
  tema não for floresta — pega o bug do Pomar **sem nem renderizar**.

### PORTÃO DE VARIEDADE — `eduverse/audit/portao_variedade.py`
- **`variedade_npc`** — reprova NPC com `fala` string única em contexto repetitivo; exige
  `falas[]`. No run headless, se a **mesma string de balão** aparece 2× seguidas = FALHA.
- **`variedade_contagem`** — na mecânica de contar, exige que a fala mude a CADA fruta
  (`n1..nN`) — os ids `n0..n30` já existem; o portão prova que o coelho/Byte os usa em vez de
  repetir uma linha a cada 8s.

### PORTÃO DE PEDAGOGIA (troca o stub) — dentro do `runner.py`
Substitui `pedagogia_arco` (hoje só checa presença da chave `arco`) por gate real:
`arco` com as **8 etapas na ordem**, existe `objetivo_curricular`, os rounds **cobrem** esse
objetivo, e há `final` roteirizado (não o default). **FALHA** quando faltar (não
`PENDENTE_HUMANO`).

---

## 4. PLANO DE EXECUÇÃO (sequenciado e priorizado — fluxo ANTES da atividade)

> Cada erro que escapar vira um teste novo do auditor. Priorizado por "destrava o resto".

**FASE A — Externalizar a história (mata o bug que vaza AGORA)**
1. `kit-floresta.py:67-68` → trocar subtítulo fixo por `__SUB__`/`__HINT__`; `montar.py`
   injeta de `MUNDO.historia.sub/hint`. (Mata "chave dourada/labirinto" no Pomar já.)
2. Criar bloco `MUNDO.historia` no schema e trocar os literais do motor por leitura de dado:
   intro (`:224/:266`), chaveFala (`:889`), arcoFala (`:892`), HUD (`:1005`), fim/gancho
   (`:1012-1013`), textos de rodada (`:490-504`) → `mecanica.textos`. **Tudo com fallback** ao
   texto atual (a Floresta não muda).
3. Trocar o interruptor `!MODO_AULA` por `MUNDO.historia.objetivo`; tornar `chave`/`arco`
   **opcionais** em `montar.py`. Remover as coords órfãs do Pomar.
4. `montar.py`: sanity forte `re.search(r'__[A-Z_]+__', html)` → aborta.

**FASE B — Contrato único + validação**
5. Escrever `eduverse/schema/dados.schema.json` (seção 2) e `checar.py` (jsonschema + refs de
   asset/pose existem).
6. Migrar `pomar`, `floresta`, `clareira` para o schema v1 (renomear `mundo`→`mapa`, promover
   `falas` de ids para objetos com texto, adicionar `historia/roteiro/faixa/habilidade`).

**FASE C — Metadados de arte no catálogo**
7. Evoluir `registro.json`: `alvo_altura_px`, `escala_vs_byte`, `y_pe` por asset; agrupar
   personagem `{base, fantasias, poses}`. Definir cabana ~200-260px, fruta ≤ ~28px.

**FASE D — Ligar os portões ao runner (o coração da tarefa)**
8. `portao_coerencia.py` (lista negra/branca) — **primeiro**, é o mais barato e pega o Pomar.
9. `portao_arte.py` (proporção, flutuante, área, poses) reusando o harness de `runner.py:69-85`.
10. `portao_variedade.py` (NPC array + contagem 1 a 1).
11. Trocar `pedagogia_arco` stub por gate real; **importar os 3 portões no `runner.py`** via
    `gate()`; endurecer o gate de voz (cobertura). Modo `--avisa` → `--rigoroso`.
12. `orquestra.py`: sempre `montar → runner` (re-audita; laudo nunca obsoleto).

**FASE E — Fechar o gerador de fantasia (produção espetacular)**
13. `gerar-fantasia.yml`: edita âncora (Gemini) → 6 poses → autocrop/resize/optimize → grava
    em `proc/` **e** no `registro.json`.

**FASE F — Só então produzir/reproduzir a atividade**
14. Rodar a linha inteira no Pomar; laudo tem que sair **APROVADO** com os 3 portões ativos.
    Só depois publicar (repo próprio + card no hub, portal leve).

---

## 5. Cada defeito do Pomar × a etapa/portão que passa a impedi-lo

| Defeito do Pomar | Etapa/portão que passa a IMPEDIR |
|---|---|
| **Labirinto/chave herdados** (texto de outro mundo) | **FASE A** (história sai do motor, vem de `MUNDO.historia`; `montar.py` injeta `__SUB__`) **+ PORTÃO DE COERÊNCIA** `coerencia_tema` (lista negra `labirinto/chave dourada/Nimbo` quando `objetivo!=chave`). |
| **Maçã flutuando** | **PORTÃO DE ARTE** `arte_sem_flutuante` (fruta sem tronco/copa no raio e sem sombra = FALHA; exige haste+sombra) + breakdown na Etapa 2 (`porque_contexto:"pendurada + caídas"`). |
| **Cabana do tamanho do Byte** | **PORTÃO DE ARTE** `arte_proporcao` (lê `alvo_altura_px` do registro; cabana < ~3×Byte = FALHA) + **FASE C** (metadados de proporção no `registro.json`). |
| **Coelho repete a mesma fala** | **PORTÃO DE VARIEDADE** `variedade_npc`/`variedade_contagem` (exige `elenco[].falas[]`, reprova balão repetido 2× e exige `n1..nN` na contagem). |
| **Poses frente/costas com pernas estranhas** | **PORTÃO DE ARTE** `arte_poses` (compara silhueta das 3 vistas; reprova fallback "frente andando de ré") + **FASE E** (gerar as 6 poses de verdade, normalizando o pé). |
| **Área de jogo pequena em tela pequena** | **PORTÃO DE ARTE** `arte_area_jogo` (canvas < 60% da viewport em 360px = FALHA) + canvas responsivo no motor. |
| **Auditor aprovou tudo (arte empurrada)** | **FASE D** (os 3 portões chamam `gate()` de verdade; `pedagogia_arco` deixa de ser `PENDENTE_HUMANO`) + **Etapa 8** (re-audita sempre; laudo nunca obsoleto). |

---

**Maior risco:** o **PORTÃO DE ARTE por render headless** (medir bbox de fruta/Byte/cabana e
"flutuante"/"pernas") é o mais frágil — thresholds mal calibrados geram falso-positivo/negativo
e podem travar a linha ou deixar passar. Mitigação: começar pelos gates **por-dados** (baratos
e determinísticos: proporção lida do `registro.json`+`dados.json`, lista negra por grep) já na
FASE A/D, e introduzir os gates **por-pixel** em modo `--avisa` antes de `--rigoroso`,
calibrando com o Pomar corrigido como caso-verdade.
