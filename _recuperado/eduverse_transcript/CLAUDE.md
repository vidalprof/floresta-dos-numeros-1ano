# Instruções do projeto — Sites do(a) professor(a) vidalprof

Este repositório publica páginas educativas no **GitHub Pages** e contém uma
**"Fábrica de Sites"** que cria/atualiza outros repositórios automaticamente.
Leia tudo antes de agir e responda sempre em **português**.

> ## 0. ORIENTAÇÃO OBRIGATÓRIA — LER PRIMEIRO (evita o erro de "cópia velha")
>
> **⭐ ANTES DE TUDO, leia o `EDUVERSE-FILOSOFIA.md`** — é a LEI pedagógica do EduVerse:
> nunca é prova disfarçada; o aluno aprende porque **o MUNDO PRECISA**; o problema vem
> primeiro e o conceito por ÚLTIMO; o Byte **pergunta**, não responde. É o **Portão 0** do QA.
>
> **Leia também o `MEMORIA-DO-PROJETO.md`** — é a memória do que já construímos e
> do que EU consigo fazer (gerar imagem/áudio por workflow, secrets, atividades).
> Como eu começo cada sessão sem memória, tudo importante fica escrito ali: é a
> cura do "esquecimento". Toda capacidade/decisão nova → anotar lá.
>
> **Toda atividade EducaVerso passa pelo `EDUCAVERSO-QA.md`** (3 portões: Verificar
> → Auditar → Aprovação do professor) ANTES de chegar ao Marcos. Nada de "entregar e
> ver depois"; nunca afirmar que funciona sem testar; todo asset visto pela criança é IA.
>
> **SEMPRE sincronize com o GitHub ANTES de agir.** Já aconteceu de o ambiente
> reiniciar e deixar a cópia local num ponto ANTIGO da história — aí manuais e
> workflows que EXISTEM ficam invisíveis, e é fácil concluir errado que "não
> existe". Um hook (`.claude/hooks/sync-remoto.sh`) já faz isso no início da
> sessão, mas confirme: `git fetch origin <branch> && git status`. Se a cópia
> estiver atrás, `git merge --ff-only origin/<branch>`. **Se o Marcos disser
> "isso a gente já fez", acredite e VERIFIQUE a fundo — nunca insista no contrário.**
>
> **A GERAÇÃO DE IMAGEM E ÁUDIO É REAL e roda por WORKFLOW do GitHub** (Actions,
> internet liberada, com os secrets) — **não** pelo chat (o chat tem a rede
> travada; testar API direto daqui dá 403, e isso é normal, não é "quebrado"):
> - **Imagem:** `gerar-imagens.yml` — `modelo=pollinations` (grátis) ou
>   `modelo=gemini` (usa o secret `GEMINI_API_KEY`; pode EDITAR uma imagem base).
>   Salva em `_novo/<nome>.png` e commita sozinho. Aciona-se por `actions_run_trigger`.
> - **Áudio/narração:** `gerar-audio.yml` e `otimizar-audio.yml`.
> - **Lote:** `finalizar.yml` (dispara por commit com `[imagens]` / `[medalha]`,
>   lê `_gerar_imagens.json`, gera no Gemini e commita).
> - **Secrets já configurados:** `PAGES_TOKEN`, `GEMINI_API_KEY` (e Firebase/
>   Pollinations conforme o uso). Secret nunca aparece no código — só é usado no workflow.
>
> Ou seja: **"o Claude gera" = o Claude ACIONA o workflow que gera** e depois dá
> `git pull` para trazer o resultado. Fluxo completo de atividade: ver o
> "PROCESSO OFICIAL" no topo do `MANUAL-MESTRE.md`.

> **CRIAR ATIVIDADE PREMIUM (conteúdo + ano/disciplina):** siga o **"PROCESSO
> OFICIAL"** no topo do `MANUAL-MESTRE.md` — ler os manuais na íntegra; primeiro
> como PROFESSOR da disciplina (verificar BNCC do ano, planejar didática e
> progressão); depois como DEV SÊNIOR + DESIGNER INSTRUCIONAL (CLONAR a base
> premium **"O Grande Circo do Teo"**, gerar TODAS as imagens em lote no começo,
> auditar + QA 3 níveis, publicar em blocos, card no topo do hub). NÃO INVENTAR;