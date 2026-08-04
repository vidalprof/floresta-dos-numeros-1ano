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
> **🕵️ A BANCA DE AUDITORES roda ANTES de entregar:** `bash _qa/auditar.sh <arquivo.html>`.
> São DOZE portões, cada um nascido de um defeito que chegou perto da criança:
> engenheiro (`node --check`), **função que não existe** (`_qa/funcoes.py` — o app
> estoura no clique e o `node --check` não vê), **resto de clone** (`_qa/clone.py` —
> pré-carga, alto-falante, conceitos e falas apontando para a atividade de origem),
> fluxo (`_qa/fluxo.py`), designer (`_qa/classes.py`), **progressão** (`_qa/progressao.py`
> — a barra andava para trás), **arte própria** (`_qa/arte_propria.py` — imagem copiada
> de outra atividade), **mascote** (`_qa/mascote.py` — ele treme ao falar/piscar),
> acessibilidade (`_qa/contraste.js` — mede o PIXEL real do fundo, não o CSS), narração
> (`_qa/falas.py` — palavra que a voz erra, tipo "Complete" virando "complite"), leiaute
> (`_qa/leiaute.js` — 6 tamanhos, resposta fora da tela, alvo < 40px) e jogador
> (`_qa/jogador.js` — joga sozinho até a medalha). Há ainda o pedagogo
> (`_qa/curriculo.py`), fora da banca automática.
> **⚠️ Portão que imprime NADA não é "passou": é "rodou CEGO"** — rodar na mão, sem
> `2>/dev/null`, e ler o erro (já aconteceu: uma `telaBase()` estourava sem config e
> derrubava o contraste e o leiaute na primeira tela).
> A banca não substitui o Marcos: depois dela ainda vem o portão do professor.

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
> **🔑 SENHA DO MARCOS (se eu parecer perdido/esquecido — ele paga caro por isso):**
> se ele disser **"RELEIA A MEMÓRIA"** (ou "você esqueceu", "isso a gente já fez",
> "lembra do EducaVerso"), eu PARO tudo IMEDIATAMENTE e, ANTES de responder qualquer
> coisa: (1) `git fetch origin <branch>` + `git merge --ff-only`; (2) releio
> `MEMORIA-DO-PROJETO.md` inteiro + `EDUCAVERSO.md` + `eduverse/style-bible/ambiente-vivo.md`
> + os `EDUVERSE-*.md` + `EDUCAVERSO-PLANO-FABRICA.md`. Nunca discutir nem "achar que já
> sei" — sincronizar e reler PRIMEIRO. Essa é a cura garantida do esquecimento.
>
> **EQUIPE/PORTÕES da fábrica (sempre passam antes de chegar ao Marcos):** Pedagogo/Curriculista,
> Roteirista, Game Designer, Engenheiro, **Diretor de Arte** (proporção coerente com o Byte, props
> com contexto, tudo pintado por IA) + os PORTÕES: Portão 0 (filosofia), 1 (funciona), **Arte**
> (proporção/contexto/coerência), 2/3 (professor). Ver `EDUVERSE-EQUIPE.md` + `EDUCAVERSO-QA.md`.
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

> **⭐ TODA ATIVIDADE NOVA NASCE COM O `_padrao/FIM-DE-ATIVIDADE.md`** (decisão do Marcos,
> ago/2026: *"coloque isso para as novas que criarmos já ter essas regras"*). São 4 itens
> NÃO negociáveis no fim de qualquer atividade: (1) **boletim animado** para a criança —
> estrelas, barras e acertos contando, sem nota e sem a palavra "errou"; (2) **relatório do
> professor invisível para o aluno**, que abre **segurando a medalha 2 segundos** (nunca botão
> à vista); (3) **parecer em palavras** (Dominou / Está construindo / Precisa retomar) + linha
> de resumo; (4) **"Treinar o que faltou"**, que só aparece para quem tem objetivo abaixo de
> 75% e refaz só as fases fracas. O código pronto e as armadilhas estão nesse arquivo — copiar,
> não reescrever. Depois de colar, rodar `bash _qa/auditar.sh` (a tela final fica mais alta).

> ## 🧠✨ O ALUNO TEM QUE QUERER MAIS (ordem do Marcos, ago/2026)
> Palavras dele: *"essas atividades têm que ficar incríveis, usar técnicas de
> neurociência e ensino-aprendizagem modernas e dos mais renomados pensadores em
> educação, como foi feito nas pesquisas"*; *"o aluno tem que gostar de fazer, ficar
> com o sentimento de QUERO MAIS, despertar curiosidade, não ser chato, cansativo"*;
> *"sempre pesquise e se atualize para que as atividades sejam algo diferenciado, o
> pensar fora da caixa, a ideia inovadora que tanto falo, para que eu me destaque
> na minha área"*.
>
> Isto **não é enfeite: é critério de aprovação**, no mesmo nível dos 4 pilares.
> O que já está no motor e tem que continuar em toda atividade nova:
> - **Lacuna de curiosidade (Loewenstein):** o problema ANTES do conceito — a
>   criança percebe que não sabe e QUER saber. É o Portão 0 da filosofia.
> - **Prática de recuperação + revisão espaçada (Roediger, Bjork):** o Aquecimento
>   no meio da atividade não é enchimento — é o que fixa.
> - **"Dificuldade desejável" (Bjork):** errar e ser ajudado por andaime crescente
>   (dica → apoio concreto → revelar) ensina mais que acertar de primeira.
> - **Carga cognitiva (Sweller):** uma ideia por tela, nada de enunciado longo,
>   narração junto com a figura (princípio da modalidade, Mayer).
> - **Concreto → figural → simbólico (Bruner/CPA):** todo degrau sobe assim.
> - **Autonomia, competência e vínculo (Deci & Ryan):** escolher o crachá, ver a
>   barra andar, o mascote que torce. Nota nunca; parecer sempre.
> - **Feedback imediato e específico (Hattie):** o erro responde na hora e diz o
>   que olhar — nunca "errou".
> - **Fecho com gancho:** a atividade termina deixando uma pergunta aberta (a
>   exposição do museu, o post-it de curiosidade) — é o "quero mais".
>
> **E o pensar fora da caixa:** antes de montar o roteiro, ler o
> `CATALOGO-DINAMICAS-INTERATIVAS.md` e PESQUISAR mecânica nova; a atividade tem
> que ter pelo menos uma coisa que ele nunca viu (o simulador de enchente, a
> exposição de fotos reais, a máquina do tempo). Repetir o que já foi feito é o
> contrário do que ele pede.

> ## 🚫🧬 RESTO DE CLONE: NUNCA MAIS (ordem do Marcos, ago/2026)
> Palavras dele: *"favor não poder mais haver resto do clone, faça com que isso não
> aconteça mais"* e *"tem que aprender com os erros automaticamente e eles não podem
> se repetir nas outras atividades"*. **A regra da casa deixou de ser "tomar cuidado"
> e passou a ser MEDIDA.** O `_qa/clone.py` tinha um item por TIPO de resto (imagem,
> voz, conceito…) e, a cada rodada, aparecia um tipo NOVO. Agora ele tem o **item 8 —
> PREFIXO ALHEIO**, que não pergunta o tipo: descobre o prefixo desta atividade
> (`hv_`, `jd_`, `fb_`…) e o das outras, e **reprova qualquer coisa com a marca de
> outra pasta**, seja imagem, voz, variável ou comentário. E o **`_qa/imagens.js`**
> (portão 1e) abre a atividade no navegador e reprova **qualquer figura que não
> carregue** — foi assim que o quadradinho vazio do jogo da memória apareceu.
> **Toda vez que um defeito escapar até o Marcos, o conserto tem DUAS partes:
> arrumar o código E criar/estender o portão que o pega sozinho da próxima vez.**
> Sem a segunda parte, o trabalho não está feito.
>
> **⭐🎨 INTERAÇÃO DINÂMICA USA ARTE DE IA, NÃO DESENHO DE CSS** (regra do Marcos,
> ago/2026: *"nas interações dinâmicas sempre usar imagens geradas pela IA, como
> aconteceu na água que sobe na atividade de história, pois ficou lindo e
> profissional"*). Simulador, verso de carta, peça de arrastar, cenário que muda:
> a FIGURA é gerada (Gemini/Pollinations) e o CSS entra só no que precisa se mexer
> em tempo real (a água subindo, a carta girando). Retângulo de CSS com palitinho
> verde não é ilustração — o Marcos reprovou dois deles no mesmo dia.
>
> **⭐🃏 JOGO DA MEMÓRIA: GRANDE, BONITO, COM EFEITO E SOM** (regra do Marcos,
> ago/2026: *"os jogos da memória tem que ter bastante efeitos e sons, devem ficar
> lindos, tamanho maior, claro adequando a tela, chamar atenção do estudante"*).
> O padrão da casa: carta fluida ≥ **130×88 px** (medido pelo `_qa/leiaute.js`),
> **verso de arte de IA** (nunca retângulo liso), **virada 3D** de verdade
> (`rotateY`, com queda para troca-de-face no Chrome antigo), **brilho correndo**
> pelo verso para chamar, **par que pulsa** e acende, **placar de pares**, som
> próprio de virar e de formar par, e festa no fim.
>
> **⭐💾 TODA ATIVIDADE NOVA CONTINUA DE ONDE PAROU — POR 55 MINUTOS** (decisão do
> Marcos, ago/2026: *"ter a opção de continuar de onde parou caso o aluno saia sem
> querer, e isso durar o tempo de uma aula, 55 minutos... pode ser aplicado a toda
> atividade nova criada"*). Na escola a criança fecha a aba sem querer, o PC trava,
> cai a luz — e sem isso ela volta para a CAPA e perde a aula inteira de trabalho.
> **55 min é a aula:** dentro dela quem volta é a MESMA criança; passada a aula, quem
> senta ali é da OUTRA turma e cairia no meio da viagem de um colega — por isso o
> convite **expira sozinho**. O código pronto, a ordem obrigatória do gancho (antes do
> `TREINO`, senão o "Treinar o que faltou" não anota nada) e os 3 testes estão no
> **`_padrao/RETOMAR.md`** — copiar, não reescrever. ⚠️ `localStorage` não existe em
> `file://`: testar servindo por `http://`, senão o teste passa mentindo.
>
> **🔑 SENHA MESTRA `1275@`** (já registrada, ver `MANUAL-MESTRE.md` §modo professor):
> digitar a qualquer momento abre o menu de fases para o professor testar. Não é
> segurança (está no código-fonte) — é atalho.

> **⭐🧬 CLONAR O MOTOR? LEIA O `_padrao/CLONAR-MOTOR.md` ANTES** (lição paga na
> Fábrica do Bento, ago/2026 — foram SEIS defeitos do mesmo parentesco numa
> rodada só). Clonar o motor é obrigatório, mas junto vêm pedaços que são
> **CONTEÚDO da atividade de origem** e que **não dão erro nenhum**: o app abre
> bonito, o `node --check` passa, o print fica perfeito, e o defeito só aparece
> com a criança na frente. Trocar SEMPRE: `var IMGS` (pré-carga), `var VOZOK`
> (alto-falante), `var DOM` + `ROTCRI`/`TREINO`/`CONCD` (conceitos), o prefixo
> dos áudios, o `sw.js`/`manifest.json` e as 3 camadas do mascote.
>
> **🎭 O MASCOTE É O PIOR DELES:** as poses de **falar** e **piscar** NUNCA se
> geram do zero — a IA devolve três desenhos diferentes por mais que o prompt
> diga "exatamente igual", e como o motor cruza as camadas ~60×/s para o
> lip-sync, o boneco **inteiro treme**. Gerar só a pose parada e as outras duas
> **EDITANDO** ela (`gerar-imagens.yml` com `modelo=gemini` + `base=...`),
> recortando as três com a **mesma bbox**. No print parado as três parecem
> iguais: **o defeito só existe em movimento, então tem que ser MEDIDO**
> (`_qa/mascote.py`, portão 3d, reprova acima de 15%).
>
> **🖐️ FASE DE ARRASTAR:** testar SEMPRE os três caminhos separados — arrastar
> com mouse, **tocar com o dedo** e clicar. No celular o navegador dispara
> eventos de mouse FANTASMA depois do toque e eles desmarcam a peça; guardar só
> o `onclick` não basta (ver o guarda `ultimoToque` no manual). E **nunca** dar
> `preventDefault` no `touchstart`, que mata o toque. Este defeito o Marcos
> pegou DUAS vezes.

> ## ⭐⭐ O PADRÃO DA CASA — os 4 pilares de TODA atividade (regra permanente)
>
> Palavras do Marcos (ago/2026): *"ela tem que ser bem didática progressiva
> didaticamente, bem ilustrada, sonora lembra? isso deve ser guardado para todas as
> atividades a serem produzidas"*. Estava no costume; agora está escrito **e medido**.
>
> 1. **DIDÁTICA E PROGRESSIVA** — o problema vem primeiro e o conceito por ÚLTIMO
>    (Portão 0); os degraus sobem de verdade (concreto → figural → simbólico);
>    o andaime CRESCE a cada erro (dica → apoio concreto → revelar); tem
>    **aquecimento** (revisão espaçada) no meio; **nunca** é prova disfarçada.
> 2. **BEM ILUSTRADA** — arte própria de IA em toda tela que precisa; **nunca**
>    emoji para a criança; **nunca** arte copiada de outra atividade.
> 3. **SONORA** — **toda tela é narrada** com voz de verdade (Edge TTS); som de
>    acerto/erro/passo; e **alto-falante em TODA resposta que a criança toca**
>    (`op_<chave>.mp3` + `VOZOK`), porque no 4º ano ainda tem quem soletra: sem a
>    voz, a criança escolhe pelo desenho e a atividade vira loteria. Regra do
>    Marcos, ago/2026: *"o alto-falante nas respostas também, para ajudar os
>    alunos que não sabem ler"*.
>
> 3b. **AS DUAS PORTAS DE ENTRADA** — toda fase com **teclado na tela** (cruzadinha,
>    forca, monte a palavra) tem que aceitar **também o teclado de verdade**
>    (`document.onkeydown`), e toda fase de **arrastar** tem que aceitar **também o
>    toque simples**. Palavras dele: *"seria interessante se o aluno além de teclar
>    no teclado virtual funcionasse se ele tocasse no teclado de verdade, as duas
>    opções"*. No PC da escola tem teclado e a criança vai digitar; no celular, não
>    tem. Nunca só uma porta. Medido pelo `_qa/padrao.py`.
> 4. **LEQUE GRANDE DE INTERATIVIDADE** — contar **GESTOS, não conteúdos**. Duas fases
>    podem ensinar coisas diferentes e ainda assim ser, para a criança, *a mesma tela
>    pela terceira vez*. Palavras dele (ago/2026): *"dinâmicas interativas bem variadas,
>    completar lacunas, digitar resposta, **forca**, memória, caça-palavras, cruzadinha,
>    quiz, **simuladores**, e todas as dinâmicas das pesquisas e nosso leque, verificando
>    quais dinâmicas se encaixam melhor na atividade em questão... variedade de dinâmicas
>    para o estudante não se cansar"*.
>    - **O leque completo está no `CATALOGO-DINAMICAS-INTERATIVAS.md`** (11 famílias,
>       das pesquisas). Ler antes de montar o roteiro de fases.
>    - **Os clássicos que ele nomeou, e que TÊM que estar no cardápio:** quiz, completar
>       lacuna, digitar a resposta, **forca**, memória, caça-palavras, cruzadinha,
>       **simulador** (deslizar e o mundo reage), classificar, ligar, ordenar/linha do
>       tempo, arrastar, pintar/marca-texto, ensinar o mascote.
>    - **A escolha é por ENCAIXE, não por lista:** a mecânica tem que ser o gesto natural
>       daquele conteúdo (linha do tempo em História, simulador em Ciências, forca e
>       cruzadinha onde a PALAVRA é o conteúdo). Mecânica enfiada à força cansa igual.
>    - **Regra prática:** nenhum gesto acima de 40% e no mínimo 4 gestos por atividade —
>       medido pelo `_qa/padrao.py`. Numa atividade de ~20 fases, mirar **8 a 12 gestos**.
>
> **Auditor: `_qa/padrao.py`** (portão 0b da banca) — conta o gesto de cada fase e
> **reprova** se um só gesto passar de **40%**, se houver menos de **4 gestos**
> diferentes, ou se alguma fase estiver **muda**. Avisa sobre fases sem ilustração.
> *Medição de estreia:* Fábrica 84% "escolher" (16 de 19 fases) e Doceria 64% —
> as duas de matemática, e as duas com o mesmo defeito que o Marcos pegou na
> Legenda. **Ficam na fila para receber o mesmo tratamento.**

> **🃏⭐ CARTA DE JOGO DA MEMÓRIA É SEMPRE GRANDE** (regra permanente do Marcos,
> ago/2026: *"quando fizer jogo da memória faça cartas maiores, registre para sempre
> fazer isso"*). A carta de memória é o alvo mais difícil de qualquer atividade: a
> criança precisa **ver a figura**, **ler a palavra** e ainda **lembrar onde ela
> estava**. Carta pequena mata as três coisas de uma vez. O molde certo é **carta
> FLUIDA, não px fixo**: `.mcarta{width:48%;max-width:210px;min-height:100px}` +
> `.mcartas{max-width:430px;width:100%}` e, no PC largo (`min-width:760px`),
> `.mcartas{max-width:680px}` para abrir **três colunas** e o tabuleiro caber sem
> rolar. Em tela baixa encolhe a LETRA (`font-size`), nunca a carta. Piso medido
> pelo auditor: **130 × 88 px** (`_qa/leiaute.js`, regra 6) — abaixo disso reprova.

> **🚫⭐ NUNCA COPIAR AVATAR DE OUTRA ATIVIDADE — ARTE SEMPRE NOVA E TEMÁTICA**
> (decisão do Marcos, ago/2026: *"nunca copiar avatares, sempre ser temático,
> nunca repetir o avatar, sempre novo e temático"*). Ele pegou os brotinhos verdes
> do Jardim reaproveitados dentro do Observatório do Órbi — no meio de um céu
> estrelado. **A tela "Quem vai jogar?" é onde a criança se coloca dentro da
> história**, então os avatares fazem parte do tema tanto quanto o mascote:
> exploradores espaciais no espaço, jardineiros no jardim, repórteres no jornal.
> Vale para TODA arte, não só os avatares — clonar o MOTOR é obrigatório, clonar a
> ARTE é proibido. Custa 6 imagens; é o preço de a atividade não parecer remendo.
> Sempre com **tons de pele, cabelos e detalhes variados** (é escola pública, a
> criança tem que se achar ali) e **retrato do peito para cima** (o rosto precisa
> ser legível a 62px no crachá). O auditor **`_qa/arte_propria.py`** (portão 3c da
> banca) reprova qualquer imagem byte a byte igual à de outra atividade.

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

### 🚫 NADA DO ANTIGO SE APAGA (regra do Marcos, ago/2026)
Palavras dele: *"não apagar nada do antigo, as atividades novas em repos novos"*.
Ou seja: **atividade nova SEMPRE nasce num repositório NOVO** (pela `fabrica.yml`) —
nunca por cima de uma que já existe. E **nenhum repositório, card ou link antigo é
removido**, mesmo quando a atividade nova cobre o mesmo assunto e o mesmo ano.
Exemplo já acontecido: o 3º ano ficou com *"O Observatório do Órbi"* (novo, no topo)
**e** *"Aventura no Espaço — Sistema Solar"* (`Sistemasolar3ano`, antigo) convivendo
na mesma turma — os dois seguem no ar. Tirar card ou repo do ar só se o Marcos pedir,
com todas as letras. Na dúvida, PERGUNTAR e manter.

### 🛑 NÃO PÔR ATIVIDADE NOVA NO HUB (regra do Marcos, ago/2026 — vale AGORA)
Palavras dele: *"não precisa publicar no site de atividades as que cria, só
publicar no repo e me mandar o link por enquanto"*. Então, **atividade nova**:
1. nasce no **repositório dela** (`fabrica.yml`) e é publicada só lá;
2. confirmar o build (`deploy-pages.yml` → `status=built`);
3. **devolver o LINK ao Marcos** e parar por aí.
**NÃO** mexer no `_site/`, **NÃO** criar card, **NÃO** gerar `img/ativ-*.png`,
**NÃO** acionar `atualizar.yml` com `repo_name=mundo-das-atividades`. Ele decide
quando (e se) o card entra. O "por enquanto" é dele: só voltar a pôr card no hub
quando ELE pedir, com todas as letras.
Os cards **que já estão no hub continuam** — isto aqui não manda apagar nada
(ver "NADA DO ANTIGO SE APAGA"). O passo a passo abaixo segue valendo para o dia
em que ele pedir um card.

### Hospedar uma atividade nova (padrão fixo — SÓ quando o Marcos pedir o card)
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

### Login: ENTRAR × CRIAR senha (a tela de senha — `telaSenha`)
Ao digitar a matrícula, cai na **tela de senha**. Ela decide sozinha entre
**Entrar** (1 campo) e **Criar senha com confirmação** (2 campos: "Nova senha" +
"Confirmar senha"), em ORDEM DE CONFIANÇA (variável `novo` em `telaSenha`):
1. `_forcarNovo` (usuário clicou no link "**Prefiro criar a senha com
   confirmação**") → **CRIAR**. O flag é **consumido/zerado** depois (`_forcarNovo=false`)
   para não vazar pra uma tela de senha futura.
2. `_sessaoExpirou` (reentrada — já tinha login salvo) → **ENTRAR**. Nunca "criar"
   numa reentrada (era o bug: pedia senha nova toda vez que reabria o app).
3. `authVer>1` (admin resetou a senha) → **CRIAR**.
4. `p.senha` (migrando do hash antigo) → **CRIAR**.
5. PADRÃO (caso ambíguo) → **ENTRAR**. Nunca "criar" no ambíguo.
- **`authEntrarOuCriar(id,senha,ver)`** é o coração: tenta **entrar**; se o login
  falhar de forma ambígua, tenta **criar** — e o próprio Firebase revela a verdade
  (`EMAIL_EXISTS` = a conta já existe, então era só senha errada; senão, cria no 1º
  acesso). Assim **ninguém mais vê "crie a sua senha" tendo senha**.
- O link "**Prefiro criar a senha com confirmação**" é OPCIONAL (só na tela de
  Entrar): é o caminho mais seguro pra quem quer digitar a senha 2× e não errar. O
  padrão continua sendo o rápido (1 campo). É app de PROFESSOR (adulto) → confirmar
  senha ajuda, não atrapalha. **Auditado 2026-07: os 5 cenários batem** (normal→Entrar,
  reset→Criar, migração→Criar, link→Criar, sessão expirada→Entrar).

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
- **✅ VALIDADO NO PC REAL DA ESCOLA (2026-07):** o Marcos rodou o **Teste 1**
  (admin agenda/edita/apaga → funcionou) e o **Teste 2** (professor comum tenta
  mexer na aula alheia → recusado). O isolamento está **confirmado em produção**,
  não é só teórico. (Não re-pedir esses testes como se estivessem pendentes.)

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

### Rodízio + PEDIDOS de agendamento (fora da semana)
- **Rodízio:** cada professor só agenda na **semana do grupo da sua turma**
  (`grupoDaSemana` × `grupoDaTurma`). Isso é regra **do app**, não do servidor.
- **Fora da semana:** o professor comum **não agenda sozinho** — envia um
  **PEDIDO** (aba **Pedidos** 📨). O pedido **não ocupa horário** na agenda; só o
  **admin** aprova (vira reserva `excecao:true`) ou recusa.
  Admin agendando fora da semana → marca exceção automaticamente.
- **DONO da reserva de exceção = o professor que PEDIU, não o admin (corrigido
  2026-07).** `enviarPedido` guarda `ownerUid` = uid do professor; `aprovarPedido`
  copia esse `p.ownerUid` para a reserva (`ownerUid: p.ownerUid || admin` — fallback
  ao admin só p/ pedidos legados). ANTES a reserva nascia com `ownerUid`=admin e o
  professor não conseguia **editar/excluir** a própria aula (dava "só o admin"), pois
  `sheetReserva` e as regras do RTDB usam o `ownerUid` para permitir dono OU admin.
  **Legado:** reservas de exceção aprovadas ANTES do conserto continuam com
  `ownerUid`=admin → só o admin as remove; ou apague e o professor reenvia o pedido.
- **Onde moram os pedidos (SEM mexer nas regras):** em
  `/agenda/vidal-ramos/recentesOcultos/__PEDIDOS__/<pid>` — a área `recentesOcultos`
  já é `auth != null` r/w, então **não precisou de regra nova**. Cada leitura de
  recentes/ocultos é por `sanId(user)`, então `__PEDIDOS__` **não colide**. A
  agenda continua blindada (a aula só entra pela regra normal de `/reservas`, ao
  aprovar). Trade-off honesto: a *lista de pedidos* (dados não sensíveis) fica na
  área aberta; se um dia quiser isolá-la de verdade, aí sim precisa de regra nova.

### IA dos campos (tema/objetivo) — como funciona de verdade
A IA do app (**Pollinations**, grátis, roda no navegador) **NÃO** lê o
`_curriculo/blumenau.txt` nem navega na internet: é um LLM que gera a partir do
**treino dele + a "âncora curricular"** que embutimos no prompt (`_CURRIC_BLU` /
`_iaCurric` = as unidades temáticas/campos/eixos REAIS de Blumenau por
disciplina/ano, extraídos verbatim do PDF oficial). O documento completo (440 pág.)
fica salvo em `_curriculo/blumenau.txt` **para o Claude** usar ao montar atividades
premium — não cabe dentro da IA grátis. Ampliar a âncora (objetos de conhecimento
por ano) é o caminho de evolução; "navegar na internet" não existe nessa IA grátis.

### 🕵️ BANCA DE AUDITORIA DA AGENDA — os 4 profissionais (rodar a CADA mudança de peso)
A agenda já passou por **6 rodadas de auditoria** (2ª–6ª nos commits `agenda-aulas:`).
Antes de publicar qualquer mudança de peso (login, regras do RTDB, rede, PWA),
passar pelos **MESMOS 4 especialistas** — este é o ritual que sempre fizemos, agora
registrado para não se perder de novo. Para cada um: o que ele cobre + como checar.

1. **🔐 Segurança & Firebase.** Isolamento por dono (`ownerUid` em toda reserva;
   editar/excluir só admin OU dono → 403 senão); **XSS** (`esc()` em TODO texto livre
   — tema/objetivo/nome/disciplina; `corSegura()` valida cor antes do `style`);
   **injeção de fórmula no CSV** (célula que começa com `= + - @ \t \r` ganha `'` na
   frente, `cel()` em `exportarCSV`); **sem segredo no código** (só a *site key*
   pública). **Ordem SAGRADA ao reaplicar regras:** semear `/admins/<uid>` no console
   ANTES de fechar as regras (senão o admin se tranca pra fora).
2. **🛡️ App Check / reCAPTCHA.** **Modo observação** (NUNCA `enforce` sem testar no
   PC real da escola — rede filtrada pode travar o Google e trancar todo mundo). O
   carimbo `_acHeader` tem **timeout (2,5s) e DESISTE na sessão** (`_acFalhou`) se o
   reCAPTCHA for bloqueado — nunca trava o professor. O `SECRET` vive só no console.
3. **🌐 Robustez de rede & PWA.** **Todo** fetch com prazo (`_fetchT` 9s +
   `_corpoJson` lê o corpo com timeout próprio); `localStorage` no boot com try/catch
   (PC com armazenamento bloqueado = tela branca); **service worker** rede-com-timeout
   que só cacheia **HTML 200** (portal cativo não vira "o app"); renova o crachá em
   401/403 e repete a chamada 1×. Objetivo: **nunca tela branca / nunca "travou tudo"**.
4. **🎨 UX & Acessibilidade.** Mensagens **específicas** (403 "Esta reserva não é sua",
   conta órfã "peça reset ao admin", "muitas tentativas", reCAPTCHA/segurança);
   `toast` com `role="status" aria-live="polite"`; **contraste WCAG nos dois temas**
   (claro `#191d2e/#f2f3fa`, escuro `#e9ecf3/#0f1117`, até o `--muted` passa); alvos de
   toque grandes; Enter envia login/senha; `<img>` com `alt`.
   - **⚠️ LIÇÃO PAGA (avisos invisíveis) — 2026-07:** o `#toast` tinha só
     `class="hidden"`, mas o ESTILO que o posiciona/mostra é a CLASSE `.toast`
     (`position:fixed`, fundo, z-index). Sem a classe, `toast()` só tirava `hidden` e o
     texto ia pra um `<div>` sem estilo, **invisível** — TODOS os avisos ("Senha
     incorreta.", "Usuário não encontrado." etc.) sumiam. Certo: `class="toast hidden"`.
     **Sempre conferir que o elemento tem a MESMA classe que o seletor CSS estiliza**
     (não confundir `#id` com `.classe`). `#toast`/`#modal` ficam FORA do `#root` (senão
     `root.innerHTML=...` os apagaria a cada tela).

**Como rodar a banca:** (a) `node --check` no JS extraído dos `<script>`; (b) `grep`
das proteções (`ownerUid`, `esc(`, `corSegura`, `cel(`+CSV, `_fetchT`, `_acFalhou`,
`aria-live`); (c) testar `telaSenha` nos **5 cenários** (normal→Entrar, reset→Criar,
migração→Criar, link→Criar, sessão expirada→Entrar); (d) **Teste 1/Teste 2** do
isolamento **no PC real da escola** (admin edita tudo; professor comum leva 403 na
aula alheia). **Firebase é bloqueado no container** → os fluxos de banco só se validam
de verdade na escola; aqui, render com `fetch` mockado só confirma que não dá tela
branca. **Última banca: 2026-07 → APROVADO** (as 4 áreas passaram; única ressalva
BAIXA: 6 inputs de telas de admin sem `aria-label`, todos com placeholder visual).

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

## Política de modelos (resumo — detalhes no MANUAL-MESTRE §22)

Produção em série (moldes, cartelas, áudio, QA, publicar) = **Opus 4.8 esforço
alto dá conta**. Criação/diagnóstico difícil (motor novo, bug resistente,
decisão pedagógica ambígua) = **modelo mais forte**. O Claude não troca o
modelo da sessão sozinho: deve **avisar o Marcos AUTOMATICAMENTE** na hora
certa, sugerindo exatamente o quê — qual modelo (`/model`) e/ou o nível de
**esforço** (aumentar/baixar) — nos dois sentidos (forte quando precisa,
economizar quando dá). Em subtarefas delegadas a subagentes, a escolha do
modelo é automática por tarefa.

## Custo/sustentabilidade (resumo — MANUAL-MESTRE §23)

Autossustentável GARANTIDO: Pages + 1 HTML + Actions + voz Edge + Firebase
grátis (escala de escola). Imagens: HÍBRIDO padrão (Pollinations grátis p/
cenas/fundos/personagem; Gemini centavos só p/ recorte transparente) = ~de
graça. CUSTO ZERO absoluto é possível (Pollinations 1-por-imagem + recorte),
com ressalva honesta de nitidez levemente menor. Nunca prometer "grátis =
igual ao pago" em recorte sem a ressalva.

## Observações de segurança

- **Nunca** peça nem aceite o valor do token colado no chat. Ele vive apenas
  como secret `PAGES_TOKEN` em *Settings → Secrets → Actions*.
- Se um deploy falhar, o GitHub envia e-mail automático ao dono do repositório.
