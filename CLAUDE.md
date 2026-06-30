# Instruções do projeto — Sites do(a) professor(a) vidalprof

Este repositório publica páginas educativas no **GitHub Pages** e contém uma
**"Fábrica de Sites"** que cria/atualiza outros repositórios automaticamente.
Leia tudo antes de agir e responda sempre em **português**.

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

### Hospedar uma atividade nova (padrão fixo — "será sempre desse jeito")
1. O usuário aponta o link de uma atividade já existente (ex.:
   `https://vidalprof.github.io/<repo>/`). Recupere o `index.html` dela com
   `recuperar.yml` (`repo_name=<repo>`) → cai em `_recuperado/index.html`
   (dê `git pull`). **Mantenha a cópia original no repo de origem funcionando**
   (não apague) até o usuário migrar tudo.
2. Copie para **`_site/atividades/<slug>/index.html`**.
3. Adicione no objeto `ATIVIDADES` (chave `"fase:turma"`, ex.
   `"tesouro:1ano"`) um item `{ titulo, desc, ic (emoji reserva), mascote,
   link }`. A ORDEM importa (o usuário pode pedir "antes/depois" de outra).
4. **Mascote do card = o mascote da PRÓPRIA atividade** (o personagem que
   anda pelo mapa do jogo), como imagem com animação suave. Extraia assim:
   - No HTML do jogo, ache `var MASCOTE_POSES={` e pegue o valor da pose
     `"feliz"` (data URI base64). **Ancore a busca em `MASCOTE_POSES`** —
     há jogos com mais de uma chave `"feliz"`; pegar a 1ª do arquivo traz o
     personagem errado. Alguns jogos usam outro objeto/chave (ex. Ilha das
     Letras = `A["ZEZE_FELIZ"]`).
   - Decode base64 → Pillow → autocrop (getbbox) → redimensiona p/ ~200px de
     altura → `optimize` → salva em `_site/img/ativ-<slug>.png` (~50KB, leve).
   - Aponte `mascote: "img/ativ-<slug>.png"` no item. **Sempre confira a
     imagem com o usuário** (montagem/screenshot) antes de fechar.
5. Valide o JS (extrair `<script>` + `node --check`), publique (passo acima).

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

## Se a sessão for aberta em OUTRO repositório

Este `CLAUDE.md` só é lido quando a sessão abre **neste** repositório
(`floresta-dos-numeros-1ano`). Se o usuário abrir a sessão em outro lugar e
mencionar a "Fábrica de Sites", oriente-o a apontar para cá. Frase que o
usuário pode usar para te situar em qualquer sessão:

> "As instruções da Fábrica de Sites estão no `CLAUDE.md` do repositório
> `vidalprof/floresta-dos-numeros-1ano`. Leia de lá antes de agir."

## Observações de segurança

- **Nunca** peça nem aceite o valor do token colado no chat. Ele vive apenas
  como secret `PAGES_TOKEN` em *Settings → Secrets → Actions*.
- Se um deploy falhar, o GitHub envia e-mail automático ao dono do repositório.
