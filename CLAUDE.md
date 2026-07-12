# Instruções do projeto — Sites do(a) professor(a) vidalprof

Este repositório publica páginas educativas no **GitHub Pages** e contém uma
**"Fábrica de Sites"** que cria/atualiza outros repositórios automaticamente.
Leia tudo antes de agir e responda sempre em **português**.

> **CRIAR ATIVIDADE PREMIUM (conteúdo + ano/disciplina):** siga o **"PROCESSO
> OFICIAL"** no topo do `MANUAL-MESTRE.md` — ler os manuais na íntegra; primeiro
> como PROFESSOR da disciplina (verificar BNCC do ano, planejar didática e
> progressão); depois como DEV SÊNIOR + DESIGNER INSTRUCIONAL (CLONAR a base
> premium **"O Grande Circo do Teo"**, gerar TODAS as imagens em lote no começo,
> auditar + QA 3 níveis, publicar em blocos, card no topo do hub). NÃO INVENTAR;
> na dúvida, PERGUNTAR. Cada atividade é **1 HTML único autossuficiente**.

> **"ATIVIDADE DE COMPUTAÇÃO" = FORMATO PRÓPRIO (novo, em teste):** quando o Marcos
> disser **"atividade de computação"**, seguir o **`ATIVIDADE-COMPUTACAO.md`** (BNCC
> Computação — pensamento computacional, "programe o robô" etc.), **NÃO** o molde
> premium. O trabalho premium continua normal; este formato é experimental e evolui.

## 1. Este site (repositório atual)

- O site fica em **`index.html`** na branch **`main`**.
- Há deploy automático: **todo push na `main` republica o site sozinho**
  (workflow `.github/workflows/pages.yml`).
- Link no ar: **https://vidalprof.github.io/floresta-dos-numeros-1ano/**
- Para atualizar: substitua o `index.html` pelo arquivo novo que o usuário
  enviar, faça commit e push na `main`. Depois confirme que o workflow
  "Deploy to GitHub Pages" terminou com `success` e devolva o link.

## 2. Fábrica de Sites — criar um site NOVO

Workflow: `.github/workflows/fabrica.yml` (acionado por `workflow_dispatch`).
Usa o secret **`PAGES_TOKEN`** (token do usuário, guardado só no GitHub) para
criar o repositório, publicar e ligar o Pages. **Novos repositórios são públicos.**

Passo a passo quando o usuário pedir um site novo:
1. O usuário informa **o nome** (ex.: `tabuada-divertida`) e envia o **HTML**.
   - Regras do nome: só **minúsculas, números e hífens**, sem espaços/acentos.
2. Salve o HTML em **`_novo/index.html`** neste repositório, commit e push na `main`.
3. Acione a Fábrica via `workflow_dispatch` (ferramenta MCP
   `actions_run_trigger`, workflow `fabrica.yml`), passando o input
   `repo_name` = nome escolhido (o input `source_dir` já tem default `_novo`).
4. Acompanhe a execução; o link final fica no resumo (Step Summary) e segue o
   padrão **https://vidalprof.github.io/<repo_name>/**.
5. Devolva o link ao usuário (pode levar 1–2 min para ficar no ar na 1ª vez).

## 3. Atualizar um site que JÁ existe em OUTRO repositório

A conexão direta da sessão normalmente só alcança ESTE repositório. Para gravar
em outro repo do usuário, use o workflow **`.github/workflows/atualizar.yml`**
(acionado por `workflow_dispatch`), que usa o `PAGES_TOKEN`.

Passo a passo:
1. Salve o HTML novo em **`_novo/index.html`** neste repositório, commit e push na `main`.
2. Acione `atualizar.yml` via `actions_run_trigger`, input `repo_name` =
   nome do repositório de destino (ex.: `Sistemasolar3ano`). O input
   `source_dir` já tem default `_novo`.
3. No log, confirme a linha de push (`<sha>..<sha>  main -> main`) = gravou.
4. Devolva o link **https://vidalprof.github.io/<repo_name>/** (Ctrl+F5 para ver).

## 4. Recuperar o index.html de OUTRO repositório

Workflow **`.github/workflows/recuperar.yml`** (`workflow_dispatch`). Lê o
`index.html` do repo de origem (input `repo_name`) e salva uma cópia em
`_recuperado/index.html` neste repositório. Depois é só dar `git pull` e
entregar o arquivo ao usuário (ferramenta de envio de arquivo).

## 5. Pré-requisito do token (IMPORTANTE) + diagnóstico

O `PAGES_TOKEN` precisa ter, no mínimo, estas permissões para tudo funcionar:
- **Contents: Read and write** ← grava os arquivos (HTML). SEM isso, dá erro
  `403 "Resource not accessible by personal access token"` na hora do push.
- **Administration: Read and write** ← criar repositórios (Fábrica).
- **Pages: Read and write** ← ligar/publicar o Pages.
- Repository access = **All repositories**. E o valor do token tem que estar
  realmente salvo no secret `PAGES_TOKEN` (campo não pode ficar vazio).

Se a escrita falhar, rode **`.github/workflows/diagnostico.yml`**
(`workflow_dispatch`) e leia o log: ele diz se o token lê e se consegue gravar
(`ESCRITA: SIM/NAO`), sem ficar tentando às cegas. Em telas de token em
português: "Contents" = **Conteúdo**, "Read and write" = **Leitura e gravação**.

## 6. Hub "Ilhas do Saber" (mapa de ilhas com as atividades)

Existe um site-portal gamificado chamado **"Ilhas do Saber"** (E.B.M. Vidal
Ramos). É um mapa com 3 ilhas grandes por faixa de ano, cada turma tem sua
ilhota/mascote, e dentro de cada turma ficam as **atividades** (jogos).

- **Onde mora o código:** neste repositório, na pasta **`_site/`**
  (`_site/index.html` + `_site/img/` + `_site/atividades/<slug>/index.html`).
- **Repositório publicado:** `mundo-das-atividades` → no ar em
  **https://vidalprof.github.io/mundo-das-atividades/** (o NOME na tela é
  "Ilhas do Saber"; o endereço/repo continua `mundo-das-atividades`).
- **Como publicar:** commit/push na `main` deste repo e acione
  `atualizar.yml` com `repo_name=mundo-das-atividades`, `source_dir=_site`.
  Confirme `success` e devolva o link com `?v=N` (cache-busting; suba o N).
- **Ilhas (fase) → tom da plaquinha:** Tesouro=ouro, Exploradores=prata,
  Aventureiros=bronze (objeto `TOM` no JS). Turmas: tesouro=pre/1ano/2ano,
  exploradores=3ano/4ano/5ano, aventureiros=6ano/7ano/8ano/9ano.

### Arquitetura: PORTAL LEVE (regra de ouro p/ escalar)
Cada atividade mora no **seu próprio repositório** (e tem o seu link
`https://vidalprof.github.io/<repo>/`). O hub `_site` é só o **mapa + cards**;
o card **aponta para o link** da atividade — **NÃO** se copia o jogo pesado
para dentro do hub. Assim o site fica pequeno e o build do Pages **nunca
engasga**, com qualquer volume de atividades (cada uma adiciona só o mascote
~50KB). O `atualizar.yml` **espelha** o destino (limpa o conteúdo antigo), então
o hub não acumula peso. NÃO criar `_site/atividades/` (era o modelo antigo,
pesado, que fazia o build falhar com "Page build failed").

### Hospedar uma atividade nova (padrão fixo — "será sempre desse jeito")
1. A atividade já está (ou será criada) no **próprio repositório** dela.
   Se for nova, use a **Fábrica** (`fabrica.yml`) para criar o repo; se for
   atualizar uma existente, use `atualizar.yml` (`repo_name=<repo>`,
   `source_dir=_novo`). Pegue o `index.html` dela com `recuperar.yml` para
   extrair o mascote. **Não apague o repo de origem** — é ele que serve o jogo.
2. Adicione no objeto `ATIVIDADES` (chave `"fase:turma"`, ex. `"tesouro:1ano"`)
   um item `{ titulo, desc, ic (emoji reserva), mascote, link }`, onde **`link`
   é a URL do site da atividade** (`https://vidalprof.github.io/<repo>/`).
   A ORDEM importa. **REGRA PADRÃO: atividade NOVA entra sempre no TOPO da lista
   da turma** (primeiro item do array `"fase:turma"`), a não ser que o usuário
   peça outra posição.
3. **Mascote do card = o mascote da PRÓPRIA atividade** (o personagem que
   anda pelo mapa do jogo), como imagem com animação suave. Extraia assim:
   - No HTML do jogo, ache `var MASCOTE_POSES={` e pegue o valor da pose
     `"feliz"` (data URI base64). **Ancore a busca em `MASCOTE_POSES`** —
     há jogos com mais de uma chave `"feliz"`; pegar a 1ª do arquivo traz o
     personagem errado. Alguns jogos usam outro objeto/chave (ex. Ilha das
     Letras = `A["ZEZE_FELIZ"]`; inglês = `A["OWL_FELIZ"]`, com `A["chave"]=`).
   - Decode base64 → Pillow → autocrop (getbbox) → redimensiona p/ ~200px de
     altura → `optimize` → salva em `_site/img/ativ-<slug>.png` (~50KB, leve).
   - Aponte `mascote: "img/ativ-<slug>.png"` no item. **Sempre confira a
     imagem com o usuário** (montagem/screenshot) antes de fechar.
4. Valide o JS (extrair `<script>` + `node --check`) e publique o hub. O build
   do Pages do `mundo-das-atividades` às vezes falha de forma **intermitente**
   ("Page build failed"). O jeito mais confiável de publicar é com **histórico
   limpo**: `republicar-limpo.yml` (`repo_name=mundo-das-atividades`,
   `source_dir=_site`) — faz 1 commit limpo + força 1 build. Confirme com
   `deploy-pages.yml` que ficou `built`. (O `atualizar.yml` também funciona,
   mas o build engasga com mais frequência.)

### Se uma atividade nova não aparecer no ar (build do Pages)
O repositório pode atualizar mas o **build do Pages falhar** ("Page build
failed"). Diagnóstico: rode `.github/workflows/deploy-pages.yml`
(`repo_name=<repo>`) — mostra o último commit, o status REAL do build
(`built`/`errored`) e força um novo deploy. `.nojekyll` já é garantido no
destino pelo `atualizar.yml`.

**Causa que já mordeu (importante):** o build falha quando o **histórico do
`.git` fica inchado** (ex.: jogos pesados de ~2,5 MB que entraram e saíram
continuam guardados no histórico; o GitHub baixa esse peso para montar e
engasga). Conserto definitivo: `.github/workflows/republicar-limpo.yml`
(`repo_name=<repo>`, `source_dir=_site`) — republica com **1 commit limpo**
(force-push), zerando o histórico e deixando o `.git` minúsculo. Depois disso
o build volta a `built`. Com o modelo **portal leve** (atividades por link, não
copiadas pra dentro) o histórico não incha de novo.

### Estilo dos cards (premium) e prévia local
- Cards = **plaquinhas de alumínio gravadas** (dog tag): metal escovado com
  brilho deslizante, título e "JOGAR" em **baixo-relevo**, **mascote colorido
  cravado** num medalhão, **furo + correntinha** no canto sup. direito; tom por
  ilha (ver `TOM`). Tudo CSS leve com fallback (PCs antigos), responsivo.
- **Compatibilidade é regra de ouro:** prefixos `-webkit-`/`-o-`, fallback
  antes de flex/gradiente, imagens otimizadas, poucas animações.
- **Prévia sem publicar:** há Chromium em
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Renderize com
  `--headless --no-sandbox --disable-gpu --screenshot=... --virtual-time-budget=4500`
  (use ≥4000ms: a tela tem fade `aparece .4s` e budget curto captura no meio
  da animação). Para telas internas, injete antes de `</body>` um
  `<script>window.addEventListener("load",function(){setTimeout(function(){abrirFase("...");abrirTurma("...");},80);});</script>`
  e copie `_site/img` + `_site/atividades` para o lado do HTML temporário.
  Mande o screenshot ao usuário com a ferramenta de enviar arquivo.

### Narração por voz (limite do navegador — explicar com honestidade)
O hub fala (Web Speech API) e tem barulhinho (Web Audio). **Nenhum navegador
deixa o som começar antes de UM gesto** (clique/toque) — é regra de segurança,
não é defeito. O código tenta destravar no 1º gesto (inclui mover o mouse);
em navegadores rígidos (Chrome novo) ainda exige o 1º clique/toque. O botão
"Ouvir instruções" (piscando) é o "start" garantido.

## 7. Agenda de Aulas (app do laboratório — `_agenda/`)

App de **agendamento de aulas** do laboratório de informática (professor Marcos
= admin; **sempre tratá-lo no masculino**, "o professor"/"o senhor").

- **Onde mora:** `_agenda/index.html` (1 HTML autossuficiente) + `_agenda/sw.js`
  (service worker/PWA) + `_agenda/manifest.json` + ícones.
- **Repositório publicado:** `agenda-aulas` → no ar em
  **https://vidalprof.github.io/agenda-aulas/**
- **Como publicar:** commit/push na branch de trabalho e acione `atualizar.yml`
  (`actions_run_trigger`) com `repo_name=agenda-aulas`, `source_dir=_agenda`,
  **`ref` = a branch onde estão as mudanças** (o workflow dá checkout dessa ref).
  Confirme `success` e devolva o link com `?v=N` (cache-busting).
- **Testar sem publicar:** Firebase é **bloqueado no container**; renderize com o
  Chromium headless injetando um **`window.fetch` mockado** (retornando config/
  professores/reservas fake) antes do script do app — screenshot confirma o boot
  sem tela branca. Valide o JS extraindo os `<script>` sem atributo + `node --check`.

### Backend Firebase
- **Projeto:** `atividades-educativas-16860`; RTDB
  `atividades-educativas-16860-default-rtdb`; gaveta **`/agenda/vidal-ramos`**.
- **Login:** Firebase Auth (REST). Matrícula → e-mail sintético
  `<sanId>@vidalramos.agenda`; reset de senha usa versão (`-vN`, campo `authVer`).
- **App Check:** reCAPTCHA v3, **modo observação** (NÃO enforced). Só ligar o
  "enforce" DEPOIS de testar em PC real da escola (rede filtrada pode bloquear os
  scripts do Google e trancar todo mundo). O `SECRET` do reCAPTCHA vive só no
  console, **nunca no código** (só a *site key* pública fica no HTML).
- **Robustez (já resolvida):** todo fetch tem prazo (`_fetchT` + `_corpoJson` para
  o corpo), `localStorage` protegido no boot, service worker com timeout e que só
  cacheia HTML 200 (portal cativo não vira "o app"). Isso curou o "travou tudo".

### 🔒 ISOLAMENTO por dono (blindagem aplicada — jul/2026)
As regras do RTDB **não são mais** `auth != null` aberto. Agora:
- **Quem é admin** = estar em **`/agenda/vidal-ramos/admins/<uid> = true`**, um nó
  **semeado À MÃO no console** (aba Dados). `/admins` tem `.read/.write:false` (só o
  console grava; as regras sempre conseguem lê-lo). O app **mostra o uid** do admin
  em **Minha conta** (linha "Seu identificador (uid)", botão Copiar) — só admin vê.
- **Cada reserva carrega `ownerUid`** (uid do autor, carimbado em `salvarAgenda`;
  a edição preserva via `Object.assign` do registro base). Regra de `/reservas/
  $data/$turno/$aula`: só grava/apaga quem for **admin** OU o **dono**
  (`data/newData.child('ownerUid').val() === auth.uid`).
- **config/professores/disciplinas/turmas:** só admin grava (carve-out
  `|| !data.exists()` p/ o 1º bootstrap; e `config/reservasLastWrite` fica
  `auth != null` p/ o marcador do poll não quebrar).
- **provas/lab/labstatus** (fora de `/agenda`): **intactos**, não mexer.
- **Resultado:** de fora ninguém entra (Auth); dentro, um professor cadastrado
  **não** mexe na aula do outro nem vira admin, nem via F12/REST. Blindagem completa,
  de graça, sem servidor pago.

**Ordem OBRIGATÓRIA ao (re)aplicar as regras** (nunca inverter, senão o admin se
tranca pra fora): **1)** semear `/admins/<uid>` na aba Dados; **2)** só então
publicar as regras estritas. **Nunca aplicar regras às cegas** (não dá p/ testar
do container). Sempre testar: **Teste 1** = admin agenda/edita/apaga (tem que
funcionar); **Teste 2** = professor comum tenta apagar aula alheia (tem que
recusar). Se travar, **desfazer** colando as regras abertas antigas
(`config/professores/... = "auth != null || !data.exists()"`, reservas/recentes/
recentesOcultos `= "auth != null"`).

- **Console — aba Dados:** `https://console.firebase.google.com/project/atividades-educativas-16860/database/atividades-educativas-16860-default-rtdb/data`
- **Console — aba Regras:** `https://console.firebase.google.com/project/atividades-educativas-16860/database/atividades-educativas-16860-default-rtdb/rules`

## Se a sessão for aberta em OUTRO repositório

Este `CLAUDE.md` só é lido quando a sessão abre **neste** repositório
(`floresta-dos-numeros-1ano`). Se o usuário abrir a sessão em outro lugar e
mencionar a "Fábrica de Sites", oriente-o a apontar para cá. Frase que o
usuário pode usar para te situar em qualquer sessão:

> "As instruções da Fábrica de Sites estão no `CLAUDE.md` do repositório
> `vidalprof/floresta-dos-numeros-1ano`. Leia de lá antes de agir."

## Contexto enxuto ao checar workflows (evitar estourar a conversa)

Checar status de Actions pelo MCP (`actions_list` / `actions_get`
`get_workflow_run`) devolve **payload gigante** (300–430 mil caracteres: cada
run traz o objeto do repositório inteiro, 2×) e **incha o contexto do chat**.
Para confirmar workflow sem estourar:
- **Triggar** com `actions_run_trigger` — resposta é pequena, ok.
- **Confirmar que terminou:** dar `git fetch origin <branch>` e ver se o commit
  do workflow chegou (ex.: `git log origin/<branch> -1 --pretty=%s` mostra
  "audio: gera vozes…"). Barato e direto.
- **Ler resultado/build:** `get_job_logs` com `tail_lines` pequeno (8–15) e
  `return_content:true` — pega só o fim do log (status `built`/`errored`).
- **Se precisar de `actions_list`/`get_workflow_run`:** usar `per_page:1` e, se
  vier grande, parsear o arquivo salvo com `python3` (fatiar por range), nunca
  despejar no chat.

## Observações de segurança

- **Nunca** peça nem aceite o valor do token colado no chat. Ele vive apenas
  como secret `PAGES_TOKEN` em *Settings → Secrets → Actions*.
- Se um deploy falhar, o GitHub envia e-mail automático ao dono do repositório.
