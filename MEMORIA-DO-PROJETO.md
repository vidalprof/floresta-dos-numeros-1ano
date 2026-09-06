# 🧠 MEMÓRIA DO PROJETO — ler no INÍCIO de CADA sessão

> **Por que este arquivo existe:** eu (Claude) começo cada sessão do zero, SEM
> lembrar das anteriores. Então esta é a minha memória, por escrito, para eu
> reler e "lembrar" na hora. Se algo importante não estiver aqui (ou no
> `CLAUDE.md` / `MANUAL-MESTRE.md`), eu vou esquecer. **Toda capacidade ou
> decisão nova → anotar aqui.**
>
> **ANTES DE AGIR:** `git fetch origin <branch> && git status`. Se a cópia local
> estiver atrás, `git merge --ff-only origin/<branch>`. A pasta local pode estar
> VELHA (já enganou antes — ver "lição paga" no MANUAL-MESTRE.md). O trabalho
> vive nos COMMITS do GitHub, nunca só na pasta local.
>
> **📱 ONDE AS ATIVIDADES TÊM QUE RODAR (decisão do Marcos, set/2026).** Palavras
> dele: *"a princípio os apps são para os PCs da escola, tablete, Android e
> iPhone para os profs usarem"*. Ou seja, a régua deixou de ser só o netbook:
> - **PC da escola** — 1024×600, navegador possivelmente antigo, mouse;
> - **tablet e Android** — toque, tela média;
> - **iPhone/iPad — Safari**, que é o mais exigente e o que EU NÃO CONSIGO TESTAR
>   aqui (o container só tem Chromium). Safari tem armadilhas próprias: política
>   de áudio mais dura, `100vh` que muda com a barra do navegador, `backdrop-filter`
>   caro, e toque que não dispara os mesmos eventos. **Construir defensivo e pedir
>   ao Marcos para conferir no aparelho dele** — nunca afirmar "funciona no iPhone"
>   sem ele ter aberto.
> - **quem usa é o PROFESSOR**, com a turma — não é a criança sozinha em casa.
>
> **🚫🧰 NADA DE PLATAFORMA PRONTA DE TERCEIRO — o modelo é NOSSO (decisão do
> Marcos, set/2026).** Palavras dele: *"eu quero um modelo onde vá desenvolver,
> não sites para fazer atividades prontos da internet"*. Ou seja: **H5P,
> Wordwall, Genially, Kahoot, Articulate e afins estão FORA**, e não se propõe
> de novo. (A pesquisa `_pesquisa/web/substituir-motor-autoria-atividades.md`
> trouxe o H5P como matéria-prima — ela NÃO é regra, e esta decisão a encerra.)
>
> **Por que a decisão é boa, e não só preferência:** o que a casa entrega não
> cabe em ferramenta de terceiro — voz de verdade (Edge TTS em mp3, não a voz do
> navegador), mascote com lip-sync, relatório do professor escondido atrás da
> medalha, retomar por 55 minutos, o parecer em palavras sem nota. Fora isso,
> toda atividade nossa é **1 HTML autossuficiente**: abre em PC velho de escola,
> sem plugin, sem conta, sem servidor, sem mensalidade, e não quebra no dia em
> que a empresa mudar o formato ou começar a cobrar. Plataforma pronta troca
> tudo isso por um editor bonitinho.
>
> **O que continua valendo:** biblioteca própria, escrita aqui, que as atividades
> INCLUEM (ver a conversa do modelo novo, set/2026 — "parar de gerar e passar a
> ligar").
>
> **🖥️ REPOS-CHAVE (ferramentas do professor — para eu NÃO esquecer, ago/2026).**
> O catálogo de ATIVIDADES é o `ATIVIDADES.md`. As FERRAMENTAS ficam aqui:
> **📌 COMO SABER SE UM ESPELHO FOI AO AR — DE GRAÇA (set/2026).** O
> `atualizar.yml` agora deixa **`_status/espelho-<destino>.json`** neste repo
> (destino, pasta, commit, hora, resultado, **`noar`**, sha1 local × sha1
> servido, link). Ele não acredita no push: **pergunta ao site** (com no-cache,
> até ~3 min) e só grava `noar: true` quando o arquivo servido bate com o que
> subiu. Então conferir publicação é `git fetch` + `cat` — 200 bytes. **Nunca
> mais chamar `actions_list` para isso** (uma chamada come dezenas de milhares
> de caracteres da conversa).
>
> **🔀 O CANAL DA SALA — `/lab/<sala>` (Firebase RTDB) guarda DUAS coisas, não uma.**
> Além do último comando (`{id, ts, alvo, acao, url}`), guarda o campo
> **`trocarpc`** — o interruptor do link "trocar número" na tela do aluno:
> `""`/ausente = trancado (padrão), `"todos"`, ou uma lista tipo `"7,12"`. O
> professor liga/desliga por um botão no `controle.html` (usa o campo "Enviar
> para", então libera só a máquina que ele precisa consertar) e a tela do aluno
> lê no poll de 2,5s que ela já fazia — aparece/some em ~3s, sem recarregar.
> ⚠️ **O `controle.html` escreve o nó com `PUT`, que troca o nó INTEIRO.** Por
> isso ele lê o nó ao abrir (`lerCanal`, guarda em `_no`) e reescreve
> comando + interruptor SEMPRE JUNTOS. Quem mexer aqui: rodar
> `python3 -m http.server 8099 && node _qa/trocarpc.js` — são 23 medições com o
> Firebase simulado, incluindo "o comando não apaga o interruptor" e "liga/desliga
> ao vivo em 3,2s". `PATCH` seria o natural, mas verbo novo é risco na rede
> filtrada da escola, e este é o caminho quente que não pode quebrar em aula.
>
> - **Controle do Laboratório** → pasta `_lab/` → repo **`controle-lab`** →
>   `https://vidalprof.github.io/controle-lab/controle.html?sala=sala1` (professor)
>   e `.../controle-lab/index.html?sala=sala1` (aluno). Publica por `atualizar.yml`
>   (`repo_name=controle-lab`, `source_dir=_lab`). Firebase `/labstatus`.
> - **⭐ Painel de Atividades (a tela dos LINKS)** → pasta `_painel/` → repo
>   **`painel-de-atividades`** → `https://vidalprof.github.io/painel-de-atividades/`.
>   É a tela que ele abre na escola: todas as atividades por turma, busca, botão
>   **COPIAR** o link, e o **controle da sala embutido à direita** (por `iframe`
>   para o `controle-lab/controle.html`, que não muda nada). Publica por
>   `atualizar.yml` (`repo_name=painel-de-atividades`, `source_dir=_painel`).
>   **NÃO se edita o HTML à mão:** `_painel/index.html` é GERADO do `ATIVIDADES.md`
>   por `python3 _painel/montar_painel.py`. Regra dele (set/2026): *"cada
>   atividade nova vai para esse painel certo? certifique-se disso, que cada
>   seção saiba disso"* — então fechar atividade = linha no `ATIVIDADES.md` **+**
>   rodar o montador, no mesmo commit. **Medido pelo `_qa/catalogo.py`, que roda
>   dentro do `entregar.yml`: atividade fora do painel não é publicada.**
> - **Agenda de Aulas** → pasta `_agenda/` → repo **`agenda-aulas`** →
>   `https://vidalprof.github.io/agenda-aulas/` (ver CLAUDE.md §7).
> - **Painéis de prova** (senha do professor, leem `/provas/<slug>`): matemática 3º
>   =`matematica-2ano-painel` (_mat2painel); ed. física 2º=`painel-ef-2ano` (_edf2painel);
>   viagem Brasil=`painel-viagem-brasil` (_painelviagem); ciências=`painel-ciencias-3ano`
>   (_painelciencias); Santa Catarina 5º=`santa-catarina-5ano-painel` (_sc5painel);
>   cartografia 3º=`cartografia-3ano-painel` (_cartopainel). Todos têm o botão
>   "Remover provas de teste" (ago/2026). Publica por `atualizar.yml`.
>
> **🎛️ TAMANHO DA ATIVIDADE: ~7–8 DINÂMICAS (com repetições em bloco), NÃO 12
> (cobrança do Marcos, ago/2026: "eram 7 ou 8 dinâmicas com algumas repetições").**
> O padrão da casa é **7 a 8 mecânicas DIFERENTES**, cada uma repetida em BLOCO
> seguido (subindo o degrau) para encher a aula — e NÃO enfiar 10–12 mecânicas
> diferentes. Mais dinâmicas ≠ melhor: cada mecânica nova é mais superfície para
> bug (na Oficina das Palavras eu botei 12 e paguei com várias rodadas de conserto).
> Para aumentar a atividade: **mais fases da MESMA dinâmica em bloco**, não mais
> tipos. Alvo: ~7–8 gestos, nenhum acima de 40%, ~30–37 fases.
>
> **⏱️ POR QUE ÀS VEZES DEMORA (e a banca É rápida): a banca roda em poucos
> minutos; o que demora é a CADEIA DE CONSERTOS quando eu erro/exagero.** Cada
> defeito real (mascote desalinhado, jogador preso numa mecânica, figura≠palavra,
> contraste) obriga a: conserto → re-montar → re-banca. Menos dinâmicas e seguir a
> RECEITA antes de montar = menos rodadas. A banca não é o gargalo; o retrabalho é.
>
> **🎭 MASCOTE — as 3 poses TÊM que sair da MESMA base (senão treme OU vira cópia
> parada, e a banca reprova nos DOIS).** Se o Marcos gerar 3 imagens SEPARADAS
> (não-editadas), elas não alinham (tremor ~98%). O certo: gerar a FELIZ e EDITAR
> (boca aberta = fala; olhos fechados = pisca). Sem edição do Marcos, dá para
> **editar o rosto na mão** (PIL): abrir a boca / fechar os olhos SÓ na região do
> rosto sobre a pose feliz (funcionou no robô Léxi: fala 0,4%, pisca 3,2%). Um
> mascote 100% estático (fala=pisca=feliz) NÃO passa (`_qa/mascote.py` acusa "cópia").
>
> **🎨🆓 ARTE: FLUX (Pollinations) PARA PEÇAS/CENAS, ChatGPT SÓ PARA O MASCOTE
> (decisão do Marcos, ago/2026: "pode ser, o ChatGPT usamos para o mascote, daí vc me
> passa o prompt; se o FLUX ficar ruim mudamos de novo").** Isto ATUALIZA a regra antiga
> "o Claude não gera arte". Agora:
> - **⚠️ TESTADO ago/2026: o Pollinations/FLUX NÃO chega no ChatGPT** — ele usa uma versão
>   RÁPIDA/DESTILADA do FLUX e sai **borrado nas bordas** (o Marcos reprovou a cozinha de
>   teste, 2 tentativas com prompt anti-desfoque). NÃO oferecer o Pollinations como "nível
>   ChatGPT". Para peças/cenas de qualidade, seguir no **ChatGPT** (o Marcos gera; o Claude
>   passa prompt + recorta). O único grátis que PODE bater o ChatGPT é o **FLUX.1 cheio no
>   Hugging Face** (Inference API, precisa de `HF_TOKEN` grátis) — ainda NÃO testado; só
>   montar se o Marcos pedir e der o token.
> - **Mascote (e "mesmo personagem em várias poses")** → **ChatGPT** (o Claude PASSA o
>   prompt em bloco; o Marcos gera e edita fala/piscar). FLUX não edita base com fidelidade;
>   Gemini editava mas está sem cota.
> - **Fallback:** se o FLUX sair ruim numa peça, volta pro ChatGPT naquela peça.
> - Recorte de tudo (venha do FLUX ou do ChatGPT) → `_padrao/recortar.py` (rembg/isnet).
>
> **🖼️ MONTADOR — 2 lições da Blumenau (ago/2026, pegas pela banca):**
> - **`fundoSuave: True` quando o `fundo` é CENA detalhada** (mapa da cidade, feira cheia).
>   Sem isso o motor deixa o fundo NÍTIDO atrás do jogo e os cards de vidro somem no meio da
>   poluição. Com `fundoSuave`, a capa fica nítida e SÓ o jogo desfoca/escurece o fundo. Fundo
>   liso/gradiente não precisa.
> - **ESCOLHER: se as OPÇÕES têm figura, NÃO pôr figura no topo** — a foto do topo é a
>   resposta certa e entrega a fase. O helper `esc()` já faz: `topo="" if (cimg and eimgs)`.
>   Figura de topo fica só quando as opções são TEXTO (ex.: perguntas sobre o mapa).
> - **LIGAR: figura precisa de proporção ~0.9–1.5** (nem alta-fina nem larga-demais), senão o
>   portão `encaixe` reprova (largura < 44px) ou `vazamento` (a figura larga empurra o
>   alto-falante para fora do card). Padroniza com pad transparente antes de montar.
>
> **✂️🏆 RECORTE PROFISSIONAL = `rembg` (isnet), NÃO flood-fill (Marcos, ago/2026:
> "use ferramentas profissionais para recortar, tudo perfeito e lindo, sem mancha,
> tudo sem fundo" + "para o processo ficar mais rápido, confiável, com menos erros").**
> O flood-fill de cor NÃO separa peça PRETA em fundo PRETO — a cartola do Homem-Batata
> saía manchada de branco (o flood comia a peça). A cura é o **rembg** (modelo treinado),
> que já está **instalado aqui** (`pip install rembg onnxruntime`, funciona pelo proxy;
> o modelo `isnet-general-use` baixa sozinho na 1ª vez — melhor que `u2netp`, que deixava
> halo cinza). Utilitário pronto: **`_padrao/recortar.py`** (`grade LxC`, `um`, `mascote`).
> Recorta preto-no-preto perfeito, borda limpa; depois zera alfa < 60 (tira sombra) e apara.
> **Regra:** todo recorte de peça/cartela/mascote passa a ser pelo `_padrao/recortar.py`.
> Para o MASCOTE, o comando `mascote` recorta as 3 poses na MESMA bbox de união (não treme).
>
> **⚡ CHECK-RELÂMPAGO ANTES DA BANCA COMPLETA (cobrança do Marcos, ago/2026:
> "o processo tem que ser muito mais rápido").** O que faz uma atividade nova
> demorar NÃO é a banca (roda em minutos) — é o CICLO: descobrir um defeito só
> DEPOIS de 5 min de banca, consertar, re-gravar voz, e rodar a banca DE NOVO.
> Cada volta custa a voz + a banca inteira. Para cortar isso, **antes** de gastar
> a banca completa, rodar os portões DETERMINÍSTICOS que custam segundos e pegam
> os erros mais comuns de atividade nova (tudo sem Chromium pesado, exceto encaixe
> que é rápido):
> - `python3 _qa/duracao.py <pasta>` → 40 min? (o Marcos exige ≥40)
> - `node _qa/encaixe.js <pasta>/index.html 360 640 412 732 800 1280` → nenhuma
>   `.ligfig`/figura < 44px (figura EM PÉ, ratio < 0,82, fica fina quando o
>   `.ligfig` trava a altura em 54 — recortar mais QUADRADA, ratio ≥ 0,92).
> - conferir **voz × mascote**: mascote masculino → `"voz":"masculina"` no
>   `build_conteudo.py` (Téo, Nino… castor/menino = macho → Antonio, não Francisca).
> - `python3 _qa/padrao.py` + `_qa/cobertura.py` (gesto ≤40%, objetivos com peso).
> - `python3 _padrao/ESQUELETO/colher.py <pasta>` (colher os banners de tempo real)
>   → montar → gravar a voz. Só ENTÃO a banca completa, UMA vez.
> **Regra de ouro:** grave a voz UMA vez só, no fim, com o conteúdo já fechado e o
> check-relâmpago verde — nunca gravar, achar defeito, re-gravar. E a voz do
> mascote definida ANTES da 1ª gravação (masculina/feminina), senão re-grava tudo.
>
> **📋 PREFERÊNCIA DO MARCOS (ago/2026) — PROMPTS DE IMAGEM SEMPRE EM BLOCO DE
> CÓDIGO NO CHAT.** Palavras dele: *"mande os prompts aqui com um botão copiar, e
> sempre desse jeito"* e *"quero o conteúdo com botão copiar aqui no chat mesmo, sem
> página"*. Ou seja: cada prompt vai **num bloco ```code``` direto na resposta do
> chat** (o cliente já põe o botão de copiar no bloco). NÃO mandar como página/
> artifact e NÃO só como arquivo `.md` anexo. Cada figura/cartela = um bloco próprio,
> com o nome do arquivo (`ef_...png`) e uma linha de descrição por cima.

> **⛔⏱️ LIÇÃO PAGA (ago/2026) — BANCA COMPLETA NUNCA SE RODA EM CONSERTO.**
> Cobrança do Marcos, DUAS vezes no mesmo dia: *"lembra que não é passado banca
> completa em consertos"* e *"vc tem que lembrar disso, não posso ficar perdendo
> tempo com essas coisas"*. Eu tinha acabado de rodar `bash _qa/auditar.sh` inteiro
> (26 Chromiums, vários minutos, custo/tempo dele) só para validar um ajuste de VOZ
> no motor. **ERRADO.** A regra é MEDIDA e não pode depender de eu lembrar:
> - **CONSERTO / ajuste** (texto, cor, um dado, um comportamento pontual — mesmo que
>   toque o motor): rodar **SÓ os portões do que mexi** + `node --check` +
>   `python3 _qa/revisor.py <pasta>`. Para voz: `voz_dupla.js`, `vozigual.js`,
>   `fala_o_escrito.js`. Nada de banca inteira. (`auditar.sh --reparo <html>` roda só
>   os portões de texto, em segundos, quando serve.)
> - **BANCA COMPLETA** (`bash _qa/auditar.sh <html>`): **só** para atividade/fase
>   NOVA, ou quando o Marcos PEDIR. "Mudança de motor" NÃO é gatilho automático de
>   banca inteira — se a mudança é um conserto, valida-se pelos portões DAQUELE
>   assunto. Um conserto de voz se prova com os portões de voz saindo 0, não com a
>   banca toda.
> - **Nunca dizer que passou sem código 0** continua valendo — mas "código 0" é dos
>   portões CERTOS, não de todos sempre.

> **⚠️ LIÇÃO PAGA (ago/2026) — ATIVIDADE NOVA NASCE DO ESQUELETO, NUNCA HTML SOLTO.**
> O Marcos pediu uma atividade de matemática (2º ano) e eu saí montando um HTML
> avulso (emoji/CSS), do jeito ANTIGO — fora do nosso padrão do app Broto. Ele
> cobrou: *"vc esqueceu como vínhamos fazendo as atividades no modelo do app broto?
> vc esqueceu tudo?"*. A causa foi eu **não ter relido ISTO antes de agir** —
> peguei o pedido novo como licença pra improvisar. **REGRA MEDIDA:** todo pedido
> de *"atividade nova"* começa OBRIGATORIAMENTE por
> `python3 _padrao/ESQUELETO/esboco.py <pasta> --ano "Xº ano" --prefixo xx --titulo "..." --mascote nome`
> → preencher só o conteúdo (`mesa`, `voz`, `curriculo` verbatim, fases com o
> formato EXATO de cada peça em `pecas.json`) → `montar.py` (gera index.html +
> falas.json + arte.json; **arte de IA e voz em TODAS as telas**) → `colher.py` →
> `montar.py` → `prompts.py` → banca. Ver `_padrao/ESQUELETO/COMO-USAR.md`. Se eu
> me pegar escrevendo `<html>` na mão para uma atividade de criança, **parei no
> lugar errado** — volto pro esboço.
>
> **⚠️ LIÇÃO PAGA (ago/2026) — `rm -rf` com curinga apaga pasta RASTREADA.**
> Limpando lotes-descartáveis, `rm -rf _lote*` casou a pasta RASTREADA `_lote/`
> (37 atividades) e os `_lote_*.json` — 657 arquivos apagados. Sem commit, então
> `git checkout -- .` restaurou tudo (o remoto nunca foi tocado). REGRAS: (1)
> pasta throwaway usa nome que NÃO colide com nada rastreado (ex.: `_zzz_lote1`,
> nunca `_loteb`); (2) apagar por nome EXATO, nunca `_lote*`; (3) depois de
> qualquer `rm`, conferir `git status` — se aparecer `D` de arquivo rastreado,
> `git checkout -- .` NA HORA.
>
> **📝 PROVA NOVA = SHELL PADRÃO (decisão do Marcos, ago/2026).** A prova "Viagem
> pelo Brasil" saiu num app próprio (capa numa tela só, barra de carimbos,
> avança sozinho ao responder) e ele apontou: *"não está no padrão, não se
> parece com nossa atividade… botão prosseguir, barra no padrão que a gente vem
> fazendo"*. Ele decidiu **deixar essa como está e fazer no padrão nas próximas**.
> Então **toda prova NOVA nasce com a casca das nossas atividades**: capa com
> mascote → tela **"Quem vai jogar?"** (escolhe avatar) → nome/turma → quiz **uma
> pergunta por tela** com a **barra estilo app** (trilho de vidro que enche +
> cometinha, o `setProg`/`.pgfill` do `motor.html`, NÃO carimbos) e **banner com
> botão "Continuar/Prosseguir"** depois de responder (não avança sozinho) + selo/
> balão do padrão. O QUE MUDA na prova: o fim é **medalha + parabéns SEM nota** e
> a nota vai só pro **painel do professor** (Firebase). Caminho provável: montar
> no ESQUELETO com uma mecânica "quiz" + "modo prova" no fim, OU adaptar a casca
> reusando o CSS/fluxo do `motor.html`.

>> ## 🏗️ MOLDE OFICIAL DE ATIVIDADE PREMIUM (Marcos pediu 2026-07-21) — LER ANTES DE CRIAR
>> **Para montar QUALQUER atividade premium melhorada, siga o `MOLDE-ATIVIDADE-PREMIUM.md`** —
>> a receita fixa e profissional: BNCC → projeto pela pesquisa → LEI do mundo + história + mascote
>> → PLANO + aprovação do Marcos → arte/voz por workflow → **CLONAR o motor** (`_estrelas/index.html`)
>> e trocar tema/mascote/conteúdo/faixa → paradas de PRODUÇÃO → QA 3 níveis → aventura de ~55 min →
>> publicar no repo próprio + card no portal (`_portal`). A **Fábrica de Estrelas** é o EXEMPLAR-MODELO;
>> o motor (BKT/Leitner/autoexplicação/stealth/identidade/painel/lip-sync/animação) já vem pronto e
>> NÃO se reconstrói. Leis fixas (Portão 0): produção-não-reconhecimento, concreto→símbolo, problema
>> primeiro, o mundo reage por consequência, medição invisível, ZDP, revisão espaçada. Diferencial da
>> pesquisa = **Open Learner Model** (devolver ao aluno o que ele domina). Adequação por faixa (pré→9º)
>> muda só a "casca" (identificação/estética/avaliação). Ver também `PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md`.

>> ## 🧩 VARIEDADE DE MECÂNICA — o Marcos cobrou (2026-07-23) e ele estava certo
>> Ele perguntou: *"foram utilizadas várias interatividades? tradicionais? caça-palavras?"*. **CONTEI NO CÓDIGO:**
>> a Redação tinha **26 "escolher uma opção"** contra 2 de qualquer outra coisa — ou seja **~90% múltipla
>> escolha**. Zero: arrastar, caça-palavras, ligar colunas, digitar, cronômetro. **LIÇÃO: contar as mecânicas
>> ANTES de entregar** (`grep` por `el("div","opt"` etc.) — muda o cenário mas a mão da criança faz sempre igual.
>> - **4 MECÂNICAS NOVAS (levaram de ~30 para ~45 min, sem gerar imagem nenhuma — tudo HTML/CSS):**
>>   1. **Caça-palavras dos verbos** (grade 9x9 gerada em runtime; toca 1ª e última letra). **Pegadinha nossa:**
>>      tem SUBSTANTIVO na grade (BOLA/ESCOLA) — marcar errado ensina a diferença. Não é caça visual à toa.
>>   2. **Escreva o verbo (TECLADO)** — sem lista pra escolher; compara com `normal()` (minúsculas + tira acento)
>>      e aceita várias respostas. É a única PRODUÇÃO real de texto que temos.
>>   3. **Ligar colunas** (gênero ↔ função) — toca esquerda, toca direita.
>>   4. **Desafio relâmpago** — cronômetro de 45s + placar, "é verbo ou não é?". Virou a **Missão 3** do menu
>>      (a professora pode usar sozinha como aquecimento de 3 min em qualquer aula).
>> - **⚠️ NOVO CHECK DE QA (obrigatório, pegou bug de verdade):** *classe usada no JS sem CSS definido*.
>>   Regex nas classes de `el("div","xxx")`/`className=` vs as definidas no `<style>`. Pegou `.bin/.bins/.sim/.nao`
>>   (os botões do relâmpago tinham virado **texto solto**) — o auditor de sobreposição NÃO pega isso.
>>   **Rodar os DOIS: sobreposição + classe-sem-CSS.**
>>
>> ## 🔗 REGRA DO MARCOS: assuntos da MESMA turma = UM app, UM repo (2026-07-23)
>> Ele perguntou (com razão): *"o certo seria as duas na mesma atividade, em um repo só, não?"* — **SIM**.
>> Uma professora, uma turma, **um link**. Juntei Verbos + Gêneros em **`_redacao/` → "A Redação do Pingo"**
>> com um **MENU DE MISSÕES** (ela ainda escolhe se hoje é só verbos ou só gêneros; a missão feita fica
>> marcada "feito" em verde). **Um parecer só** (`?painel`) com os 8 conceitos das duas missões.
>> - **No ar nos DOIS endereços** (mesmo app, pra não quebrar link já compartilhado):
>>   https://vidalprof.github.io/plantao-na-redacao/ e https://vidalprof.github.io/banca-do-pingo/
>> - `_verbos/` e `_generos/` viraram **fonte histórica** — o que vale agora é `_redacao/`.
>> - **COMO JUNTAR DOIS APPS (receita que funcionou):** os dois tinham funções com o MESMO nome
>>   (telaCapa/telaQuem/telaAquecimento/telaEnsinar/telaFim/telaPainel). Cortei cada corpo nos banners
>>   `/* ===== CONTEÚDO ===== */` … `/* ===== PAINEL ===== */`, **renomeei com prefixo** (`vXxx`/`gXxx`),
>>   e escrevi capa/quem/menu/painel novos. Uni `IMGS`, `DOM`, `CONC` e a chave do localStorage.
>> - **⚠️ ARMADILHA PAGA:** ao montar o merge peguei o `<head>` do `_verbos` e **esqueci o CSS exclusivo dos
>>   gêneros** (`.silh`, `.txcard`, `.folha`). Pior: meu teste `if ".txcard{" not in h` deu **falso positivo**
>>   porque `.txcard` existia dentro de um `@media`. **Checar sempre por uma classe que só exista na regra
>>   base** (usei `.silh{`). O auditor de sobreposição pegou o estrago (conteúdo estourando a tela).
>>
>> ## 📐 AUDITORIA DE SOBREPOSIÇÃO — obrigatória em toda atividade (2026-07-23)
>> O Marcos pediu: *"as coisas não podem se sobrepor — textos, imagens, explicação"*. Criei um **auditor
>> automático** (`/tmp/audit2.js`, guardar a receita): abre o app, **chama cada `telaXXX()` direto pelo
>> `window`** (as telas são funções globais, não IIFE), mede o `getBoundingClientRect()` de todos os
>> elementos-chave e acusa **pares que se cruzam (>150px²)** e o que **corta pra fora da tela**. Rodar em
>> **360x640 e 412x840** (o 360 é o que pega tudo). É MUITO mais rápido que navegar clicando.
>> - **Bugs REAIS que ele achou:** (1) **Jardim: a barra de progresso invadia o balão em 12 telas**;
>>   (2) **Gêneros: as opções ficavam por baixo da barra Ouvir/Dica** (13 mil px²) na tela "Saiu errado!".
>> - **Conserto padrão (aplicar em toda atividade nova):** `.tela` com **padding-top ≥ 38px** (a `.prog`
>>   ocupa ~26px) e **padding-bottom ≥ 86px** (a `.barra` fixa), `.tela{overflow-y:auto}` para conteúdo alto,
>>   e um **`@media (max-height:720px)`** encolhendo imagem/fonte/gaps. Depois **re-rodar o auditor até dar 0**.
>>
>> ## 🪪 CRACHÁ = O PRÓPRIO MASCOTE (decisão do Marcos, 2026-07-23)
>> Na tela de identidade, as figurinhas **não** devem ser objetos aleatórios: são o **mesmo mascote em
>> versões diferentes** (cor + acessório). Fiz 6 do Pingo no Gemini editando a base (`cr_pingo1..6`:
>> vermelho/boné, verde/óculos, roxo/gravata-borboleta, laranja/chapéu de repórter, rosa/laço, amarelo/fones).
>> Usados nos DOIS apps do Pingo. **Pendente:** fazer o mesmo para o Broto (Jardim ainda usa estágios da planta).
>>
>> ## 📚 NOVA PREMIUM: "A Banca do Pingo" — GÊNEROS TEXTUAIS, 4º ano (2026-07-23)
>> Módulo 2 do pedido da professora (ela confirmou: **gêneros TEXTUAIS**). Publicada em **`banca-do-pingo`**
>> → https://vidalprof.github.io/banca-do-pingo/ . Pasta `_generos/` (2,9 MB).
>> - **REAPROVEITAMENTO (barato e coerente):** mesmo mundo (redação) e **mesmo mascote, o Pingo** — copiei
>>   `vb_pingo*` e `vb_fundo.jpg` do `_verbos`. Só gerei 5 imagens novas (ícones de poema/conto/carta/verbete
>>   + medalha). O **motor foi clonado do `_verbos`** cortando no marcador `/* ===== CONTEÚDO ===== */`.
>> - **Gêneros do 4º ano em Blumenau (conferido no PDF):** notícia, reportagem, poema, quadrinha, parlenda,
>>   trava-língua, conto (popular/de terror), carta (solicitação/reclamação), verbete de enciclopédia infantil.
>> - **6 fases:** (1) **"sem ler, só olhando"** — a criança vê só a SILHUETA do texto (barras em CSS!) e deduz
>>   o gênero pela FORMA (POE); (2) para que serve (função); (3) arrume a banca (mandar cada texto pra seção);
>>   (4) aquecimento; (5) **texto trocado** — notícia escrita como conto de fadas, a criança conserta;
>>   (6) **monte a carta** (produção: para quem → recado → despedida → assinatura); + ensinar o Pingo.
>> - **Truque bom e barato:** a silhueta do texto é feita com **barras CSS** (`.silh .sb`), não com imagem —
>>   ensina forma sem custo de geração. Reaproveitar em outras atividades de leitura.
>> - QA: playthrough completo no Chromium **sem erros** já na 1ª tentativa.
>>
>> ## 📰 NOVA PREMIUM: "Plantão na Redação" — VERBOS, 4º ano (2026-07-23)
>> Pedido da professora do 4º ano ("estão iniciando com os verbos"). Publicada em **`plantao-na-redacao`**
>> → https://vidalprof.github.io/plantao-na-redacao/ . Mascote **o Pingo** (gotinha de tinta, masculino →
>> voz masculina). Pasta `_verbos/` (3,7 MB: 30 MP3 + 12 imagens).
>> - **ANCORADA NO CURRÍCULO DE BLUMENAU (baixei o PDF com `baixar-curriculo.yml`):** 4º ano, Morfologia —
>>   *"Identificar em textos e usar na produção textual a concordância entre substantivo ou pronome pessoal e
>>   verbo (concordância verbal)"* — **gênero do discurso: NOTÍCIA**; + *"produzir notícias (...) para o jornal
>>   da escola"* e *"distinguir fatos de opiniões"*. Base do 3º ano: *função do verbo (agente, ação)*.
>>   ⚠️ A tabela de Blumenau **NÃO traz os códigos EF04LP** nesse trecho → citar o texto, não inventar código.
>> - **Por que "redação de jornal":** é o currículo que amarra verbo↔notícia. E o produto final é real:
>>   a criança **escreve a manchete** e ela sai na primeira página (jornal da escola).
>> - **7 fases:** (1) foto congelada + POE → a cena só ganha cor com o verbo; (2) caça à ação em 4 notícias;
>>   (3) ficha do repórter (quem fez / o que fez); (4) aquecimento; (5) três edições (ontem/hoje/amanhã);
>>   (6) erro de impressão = concordância verbal; (7) escreva a manchete + ensinar o Pingo.
>> - **Motor premium clonado do Jardim** (voz+lip-sync, Ouvir de novo, Dica, medição invisível, `?painel`,
>>   medalha, identidade). QA: playthrough completo no Chromium **sem erros**.
>> - **GÊNEROS (2º módulo) fica pendente:** o Marcos ainda vai confirmar com a professora se "gêneros" é
>>   **gêneros textuais** (provável, o currículo cita notícia/conto/lenda/HQ) ou gênero gramatical.
>> - **LIÇÃO de QA (paguei tempo):** no teste headless, casar texto por *substring* clica na opção ERRADA
>>   ("escreve" casa com "escreveu"). **Sempre casar texto EXATO primeiro** no Playwright.

>> ## 🛑 RUMO ATUAL (Marcos, 2026-07-23) — **EDUCAVERSO/EDUVERSE FICA DE LADO**
>> Decisão do Marcos, literal: *"deixamos o educaverso de lado (...) o que iremos fazer é continuar
>> nossas atividades premium com melhorias"*. Ou seja:
>> - **PARADO (não puxar mais como projeto):** portal/plataforma EducaVerso, cadastro/turmas, sequências
>>   didáticas do portal, fábrica de mundos/RPG, e o resto dessa linha (`EDUCAVERSO-*.md`, `EDUVERSE-*.md`,
>>   `ARQUITETURA-PLATAFORMA-RPG.md`, `EDUCAVERSO-PLANO-FABRICA.md` etc.). Não apagar — só **não é o foco**.
>> - **O FOCO AGORA:** as **ATIVIDADES PREMIUM** (uma por assunto/ano, 1 HTML autossuficiente) e
>>   **MELHORIAS** nelas: visual híbrido (imagem IA + animação), voz + lip-sync, dica, medição invisível,
>>   parecer do professor, mais fases/duração.
>> - **⚠️ O que NÃO caiu junto:** a pedagogia continua a mesma (aprendizagem ativa, problema primeiro,
>>   produção e não reconhecimento, medição invisível, mascote que pergunta). Isso é o miolo das premium.
>> - **Atenção:** o `CLAUDE.md` ainda manda ler os `EDUVERSE-*.md` como "LEI". Perguntei ao Marcos se quer
>>   que eu ajuste o CLAUDE.md para refletir este rumo — **aguardando a resposta dele**.

>> ## 🏁 PADRÃO DO FIM DE ATIVIDADE — vale para TODA atividade nova — 2026-08-03
>> Marcos: *"coloque isso para as novas que criarmos já ter essas regras"*. Código pronto e
>> armadilhas em **`_padrao/FIM-DE-ATIVIDADE.md`** (extraído da Doceria, já rodando nas 4).
>> Está citado no `CLAUDE.md` e virou a **FASE 0.5** do rito no `MANUAL-MESTRE.md`.
>> **Os 4 itens obrigatórios:**
>> 1. **Boletim animado (a criança vê)** — aparece sozinho na medalha: estrelas acendendo uma a
>>    uma, barra crescendo por objetivo, acertos subindo contando com som, tempo e frase de
>>    incentivo. **Sem nota, sem a palavra "errou"** (LEI: não é prova disfarçada).
>> 2. **Relatório do professor INVISÍVEL para o aluno** — pedido literal: *"não quero botão ou o
>>    painel do professor aparecendo para os alunos"*. Abre **segurando a medalha por 2 segundos**
>>    (toque curto não faz nada). `?painel` continua valendo.
>> 3. **Parecer em palavras** — "72%" não serve para o diário: **Dominou / Está construindo /
>>    Precisa retomar** + linha de resumo dizendo o que fazer.
>> 4. **"Treinar o que faltou"** — botão que só aparece para quem tem objetivo < 75%; monta um
>>    percurso curto com as fases fracas e volta para a medalha. **Quem dominou tudo não vê o
>>    botão** — é isso que evita o enjoo de repetir o que já sabe.
>> **Truque que fez isso funcionar sem tocar em nenhuma fase:** enquanto o treino roda, o
>> `mostraBanner` é substituído e ignora o "próximo" original, chamando a próxima fase da fila.
>> **Armadilhas pagas:** o mapa de conceitos do painel é variável LOCAL (o boletim mostrava
>> "grupos", "vezes" — daí nasceu o `ROTCRI` global) · a função de salvar muda de nome entre apps
>> (`salva()` × `salvaEstado()` no Jardim) · o bloco tem que entrar DEPOIS de todas as fases
>> existirem · atividade com 2 missões volta ao MENU, não a uma tela final.
>>
>> ## 🕵️ A BANCA DE AUDITORES (pedido do Marcos: "precisamos de auditores antes de entregar") — 2026-08-03
>> **Um comando roda todos:** `bash _qa/auditar.sh _doceria/index.html` (sem lista de telas ele descobre
>> sozinho quem chama `limpa()`). Sai 0 se a banca aprovar. Cada auditor é um profissional com UMA obsessão:
>> 1. **Engenheiro** — `node --check` no JS extraído. O código roda?
>> 2. **Arquiteto de fluxo** — `_qa/fluxo.py`: tela presa em si mesma / tela órfã.
>> 3. **Designer** — `_qa/classes.py`: classe usada no JS sem regra BASE (só dentro de `@media`).
>> 4. **Acessibilidade** — `_qa/contraste.js` ⭐ NOVO: mede o **pixel real**. Abre a tela, tira o print,
>>    deixa TODO texto transparente, tira o print só do FUNDO e compara com a cor computada (WCAG).
>>    Olhar o CSS engana: a regra diz `color:#fff` e parece certa, mas o pixel atrás é creme.
>> 5. **Leiaute** — `_qa/leiaute.js` ⭐ NOVO: 6 tamanhos reais. Reprova o que estoura na horizontal, a
>>    RESPOSTA fora da tela, a resposta atrás da barra de baixo e o alvo de toque < 40px.
>> 6. **Jogador** — `_qa/jogador.js`: joga clicando ao acaso até a medalha.
>> 7. **Pedagogo** — `_qa/curriculo.py` ⭐ NOVO: confere se toda conta cabe no ANO (ver abaixo).
>> Depois da banca ainda falta o **PROFESSOR** (portão final). A banca não substitui o Marcos.
>>
>> ## 📏 RESPOSTA COM FONTE: até que tabuada vai o 3º ano? (pergunta do Marcos)
>> `_curriculo/blumenau.txt`, verbatim: 3º ano = *"problemas de multiplicação **(por 2, 3, 4 e 5)**"*;
>> 4º ano = *"(por 2, 3, 4, 5 **e 10**)"*. **O 10 só entra no ano seguinte.** Regra que o
>> `_qa/curriculo.py` aplica: numa conta a×b do 3º ano, pelo menos UM fator entre 2 e 5 (é a tabuada que
>> ela está aprendendo); o outro vai até 10. "3 × 8" vale; "6 × 7" não. **A Doceria: 34 contas, todas
>> dentro, maior produto 45.** O 3º ano também pede *"dobro, metade, triplo e terça parte"* — **ainda
>> NÃO coberto**, fica como próxima fase.
>>
>> ## ⚠️ ERROS PAGOS NESTA RODADA (anotar para não repetir) — 2026-08-03
>> - **🎓 FALHA PEDAGÓGICA (a pior):** na fase do corte eu exigia UM corte específico (5 fileiras) e
>>   chamava de ERRO qualquer outro. Mas cortar 6 em 3+3 está tão certo quanto 5+1! Eu estava ensinando
>>   a criança a **adivinhar o que o app quer** em vez de pensar. Consertado: vale qualquer corte, o app
>>   calcula as partes que ELA escolheu; a dica apenas SUGERE o 5. **Regra nova: antes de marcar algo como
>>   errado, perguntar "isso está matematicamente errado ou só diferente do que eu esperava?".**
>> - **🔒 TRAVA por valor repetido:** no Quadro da Semana o 12 aparece na tabuada do 2, do 3 e do 4. O
>>   teclado era `unicos()` → uma só tecla "12"; ao preencher o 1º buraco ela virava `ok` e o 2º buraco
>>   NUNCA fechava. Criança presa para sempre. Certo: a tecla só descansa quando não sobrar buraco com
>>   aquele valor. **Achado pelo auditor-jogador.**
>> - **👆 ALVO DE TOQUE:** as 36 células do quadro de estoque tinham 28px de altura (herdadas do
>>   caça-palavras 9×9). Dedo de criança precisa de **40px**. O `.cel` do motor estava sendo sobrescrito
>>   por um `@media (max-height:900px)` — **cuidado ao inserir regra: `h.index('.cel{')` achou a de dentro
>>   de um @media, não a base.**
>> - **📱 RESPOSTA FORA DA TELA (foto do Marcos):** numa janela de ~360px de altura as opções ficavam
>>   abaixo da dobra — a criança via só o enunciado. Nasceram os tiers `@media (max-height:600px)` e
>>   `(max-height:430px)`. **E o monitor 1366×768 da escola é MAIS BAIXO que um celular** (~640px de
>>   janela útil): aumentar fonte lá faz rolar. Por isso o bloco de PC tem dois casos (alto = letra e
>>   caixas; baixo e largo = só a letra).
>> - **↕️ ESPAÇO NO LUGAR ERRADO:** o Marcos pediu ar entre as bandejas e o balão; eu aumentei a margem
>>   de CIMA (entre o selo e as bandejas) e o problema continuou. **Margem em bloco visual tem que ser
>>   nos DOIS lados** (`margin:16px 0`), senão o elemento seguinte continua colado.
>> - **🔊 CÓPIA DEMAIS:** `cp _audio/op_*.mp3 _doceria/audio/` levou 212 vozes de OUTRAS atividades para
>>   dentro do app (9,4 MB). Copiar só as chaves que estão no `VOZOK` daquele app.
>> - **🎨 PLURAL:** `"real"+(preco>1?"is":"")` gera "realis". Certo: `(preco>1?"reais":"real")`.
>>
>> ## 🍫 NOVA ATIVIDADE — "A Doceria do Cacau" (3º ano, multiplicação por grupos) — 2026-08-03
>> Pedido do Marcos: *"uma atividade para o 3 ano Multiplicação por soma de grupos, multiplicação de
>> grupos, bem didática, progressiva, temática com mascote e imagens novas que dure pelo menos 45 minutos"*.
>> - **Repo publicado:** `doceria-do-cacau` → **https://vidalprof.github.io/doceria-do-cacau/**
>>   (criado pela `fabrica.yml`, source_dir=`_doceria`). Fonte em `_doceria/`.
>> - **Currículo (Blumenau, 3º ano), verbatim:** *"Resolver **e elaborar** problemas de multiplicação
>>   (por 2, 3, 4 e 5) com a ideia de adição de parcelas iguais, utilizando ou não suporte de imagens
>>   e/ou material manipulável"*. Três palavras mandaram no desenho: **elaborar** (por isso existe a fase
>>   "Você é o chefe", em que a criança CRIA o pedido), **parcelas iguais** (a ponte soma→vezes é a fase
>>   central) e **material manipulável** (a fase "Monte as bandejas" é toque de verdade, não quiz).
>>   ⚠️ Há sobreposição parcial com a Fábrica de Estrelas (EF03MA07) — avisei o Marcos e segui.
>> - **17 telas, progressão fechada:** prever (POE) → montar grupos (manipulável) → escrever a soma →
>>   **a soma vira vezes** → bandeja em fileiras (organização retangular) → encomenda rápida (2,3,4,5) →
>>   ligar colunas → memória (soma ↔ multiplicação) → quadro do estoque (achar o total) → freguês na
>>   porta (problema escrito) → **você é o chefe (elaborar)** → relâmpago 60s → ensinar o Cacau → medalha.
>>   **Só 2 telas de múltipla escolha em 17.**
>> - **Mascote próprio: "o Cacau"**, um brigadeiro de massinha com chapéu de confeiteiro; fundo próprio
>>   `dc_fundo.jpg` (doceria). Masculino de propósito (mantém a voz `pt-BR-AntonioNeural`).
>>   8 imagens + poses (fala/pisca) + 6 crachás editando a base · 37 narrações + 44 vozes de resposta.
>> - **🔪 ARMADILHA NOVA DO RECORTE (custou o chapéu do mascote):** o `cut_border()` rodava com
>>   `tol=26` (aceita ≥229 como "branco"). O chapéu branco do chef tem highlight ~240 e **encostava na
>>   borda** → o floodfill comeu o topo do chapéu. **Conserto: `tol=6`** (só ≥249). O fundo do Gemini é
>>   253–255, então 6 basta. **Sempre amostrar o pixel do fundo E o do detalhe claro antes de escolher a
>>   tolerância.**
>> - **🔪 MEDALHA: floodfill de borda não alcança o buraco FECHADO** (o vão entre as duas pernas da fita
>>   ficou branco na tela). Para a medalha usei **corte por limiar puro** (≥249 → transparente), que pega
>>   também as regiões cercadas. Regra: mascote/poses = floodfill de borda (preserva olho e chapéu);
>>   objeto solto com vão fechado = limiar.
>> - **🔇 ACHADO NA LEGENDA DO CLIQUE:** os áudios `vb_acerto1..3`/`vb_erro1..2` (elogio/consolo) nunca
>>   foram copiados para `_nomes/audio/` — `elogio()`/`consolo()` estavam MUDOS lá desde a publicação.
>>   Copiados agora. **Checklist novo ao clonar o motor: copiar também os áudios COMPARTILHADOS, não só
>>   os `<prefixo>_*.mp3` da atividade.**
>> - **🧪 O auto-jogador aleatório deu falso "PRESO":** ele clicava o `#bcta` do banner ESCONDIDO (fora
>>   da tela por `translateY(115%)`, mas `.click()` ignora hit-test) e reiniciava a fase anterior em
>>   loop. Duas lições: (1) o auto-jogador tem que filtrar por `getBoundingClientRect()` dentro da
>>   viewport; (2) mesmo assim pus **`.banner{pointer-events:none}`** (e `auto` no `.show`) para não
>>   existir toque fantasma. Também: a assinatura de estado do auto-jogador precisa incluir a **barra de
>>   progresso** — só o `.selo` repete entre rodadas da mesma fase e parece "travado".
>>
>> ## 📸 NOVA ATIVIDADE — "A Legenda do Pingo" (4º ano, substantivo e adjetivo) — 2026-08-03
>> Pedido do Marcos: *"uma aula sobre substantivos e adjetivos para o 4 ano... tem que durar 45 minutos"*,
>> com **interatividades bem variadas** ("consulte nosso leque"), incluindo **caça-palavras e ligar**.
>> Ele escolheu **app novo com link próprio** (não missão dentro da Redação do Pingo).
>> - **Repo publicado:** `legenda-do-pingo` → **https://vidalprof.github.io/legenda-do-pingo/**
>>   (criado pela `fabrica.yml`, source_dir=`_nomes`). Arquivos em `_nomes/`.
>> - **⭐ O CURRÍCULO MUDOU O DESENHO (ler antes de mexer).** Em `_curriculo/blumenau.txt`, o 4º ano
>>   **não** pede "o que é substantivo/adjetivo" (isso é ano anterior). Pede, literal:
>>   *"Identificar em textos e usar na produção textual a concordância entre artigo, substantivo e
>>   adjetivo (concordância no grupo nominal)"* — **Gênero do discurso: notícia**. Por isso a atividade
>>   se passa na **mesa de fotos do jornal** (mesmo mundo do Pingo) e a criança escreve **legendas**.
>> - **Mecânicas escolhidas NO CATÁLOGO** (`CATALOGO-DINAMICAS-INTERATIVAS.md`), não inventadas:
>>   **H1 — montar a frase com peças de FORMA/COR por classe** (artigo=retângulo azul, substantivo=oval
>>   verde, adjetivo=losango laranja): é a estrela, deixa a gramática VISÍVEL. Glenberg: manipular as
>>   peças rende 1–2 DP acima de só ler. **[FORTE-mod]** · **LP1 — morfemas** (chuva+`-oso`=chuvoso),
>>   meta-análise d≈0,33–0,59, **primeira vez que usamos** · **B1 — card sort** (2 gavetas, 12 palavras)
>>   · **H2 — produção** (escrever a legenda) · + caça-palavras 9×9, ligar colunas, memória, cruzadinha,
>>   lupa, plural, gênero, revisor, relâmpago. **Só 2 telas de múltipla escolha em 19.**
>> - **Assets:** 7 imagens novas (Gemini, matte-clay) + mascote/crachás/fundo reaproveitados da Redação;
>>   43 narrações + **60 vozes de resposta** (alto-falante em 33 de 33 elementos).
>> - **RECEITA: CLONAR O MOTOR DA REDAÇÃO.** Recortei `_redacao/index.html` até
>>   `/* ===== CONTEÚDO ===== */` e escrevi só o conteúdo novo. **⚠️ ARMADILHA:** três coisas moram
>>   DEPOIS do conteúdo e ficam de fora do recorte — **o motor do alto-falante** (`VOZOK`/`chaveVoz`/
>>   `poeZap`), a função **`crachaEl`** e o **painel**. Sem elas: alto-falante em 0 de 19 e a tela final
>>   quebra com `crachaEl is not defined`. Puxar as três à mão depois de recortar.
>> - **🐛 TRÊS BUGS QUE O QA PEGOU (e as ferramentas que nasceram deles):**
>>   1. **COLISÃO DE NOME DE CLASSE:** criei `.base` (fábrica de adjetivos) e ela pintou de verde a
>>      camada `lay base` do mascote — a capa ficou com um círculo verde atrás do Pingo. Renomeada para
>>      `.fbase`. **Antes de criar classe, conferir se o motor já usa esse nome.**
>>   2. **`.pchip` só existia dentro de um `@media`** → sem estilo na tela normal (a lista do caça-palavras
>>      virou texto solto). É a MESMA armadilha do `.txcard`; o check antigo procurava no CSS inteiro e
>>      dava **falso negativo**. → criado **`_qa/classes.py`**: apaga os blocos `@media` e só então procura
>>      a regra BASE. Acusa "SÓ DENTRO DE @media" e "SEM CSS".
>>   3. **`_qa/fluxo.py` reconhecia tela pelo NOME** (`v[A-Z]|g[A-Z]|tela`) e por isso enxergou **3 das 19
>>      telas** desta atividade, calado. → agora detecta tela **pelo comportamento**: função que chama
>>      `limpa()`. Vale para qualquer prefixo (vXxx, gXxx, nXxx, telaXxx).
>> - **QA rodado:** `node --check`; `_qa/classes.py` e `_qa/fluxo.py` limpos nos 4 apps; auditor de
>> - **⭐ MASCOTE PRÓPRIO: "o Clique" (2026-08-03).** O Marcos pediu mascote novo, com outro nome, e
>>   **fundo próprio "que tenha a ver com o tema da aula"**. Virou **o Clique**, uma CÂMERA FOTOGRÁFICA
>>   de massinha — o mascote passou a fazer parte do tema (a aula é sobre legenda de foto) em vez de ser
>>   emprestado da Redação. **Escolhi MASCULINO de propósito:** pela regra de voz (mascote masculino =
>>   voz masculina), manteve o `pt-BR-AntonioNeural` e só precisei regravar **3 falas** das 43. Se fosse
>>   feminino, seriam as 43 numa voz nova — vale lembrar disso antes de escolher o gênero do mascote.
>>   - **Poses pela receita da imagem-âncora:** gera `cq_base`, depois EDITA a base para `cq_fala`
>>     (boca aberta) e `cq_pisca` (olhos fechados) + os 6 crachás. Conferido: bbox **idêntico
>>     (90,100,331,332)** nas 3 poses → o lip-sync funciona. **Recorte MANTENDO o quadro quadrado**
>>     (420×420); sem isso as camadas desalinham. Como a moldura tem margem, o mascote precisou de caixa
>>     MAIOR no CSS (`.clique` 186px, `.gg` 252px) — senão ele aparece minúsculo na capa.
>>   - **Fundo próprio:** `nm_fundo.jpg` (mesa de fotos com varal de fotos, abajur, lupa), 900×900 JPG.
>>   - **⚠️ Gemini deu 503 (Service Unavailable)** na 1ª tentativa do mascote e o job falhou. **Não é a
>>     nossa chave nem o prompt** — é instabilidade do Google. Conserto: repetir o lote. Vale olhar o log
>>     antes de mexer no prompt.
>> - **+3 FASES (2026-08-03, "aumentar o tempo"):** **Filtro mágico** — a criança toca no adjetivo e a
>>   FOTO MUDA de verdade (CSS `filter`/`transform`: escura, gigante, antiga, minúscula). É o ponto
>>   pedagógico mais forte: adjetivo = atributo, visto acontecendo, sem imagem nova · **Detetive** —
>>   caminho inverso: o Clique descreve com 2 adjetivos e a criança acha a foto (compreensão) ·
>>   **Encolhe e aumenta** — grau (casa+inha, port+ão). Total: **22 telas**, 39 de 39 respostas com
>>   alto-falante (72 clipes).
>> - **⚠️ ARMADILHA DO MARCADOR:** `_lote_falas.json` commitado junto de um commit com marcador
>>   `[imagens]` **não gera áudio** — o `finalizar.yml` olha o marcador da MENSAGEM. Se as falas forem
>>   junto, fazer um `git commit --allow-empty -m "... [audio]"` depois.
>>   sobreposição em 320/360/412; solucionador que JOGA as 6 mecânicas centrais (todas concluem);
>>   as 20 telas abrem sem erro de JS.
>>
>> ## 🌱 NOVA ATIVIDADE — "O Jardim do Broto" (2º ano, Ciências — as plantas) — 2026-07-22
>> Feita a pedido do Marcos ("crie uma nova atividade para o 2 ano nesse modelo... muitas dinâmicas
>> interativas variadas, me surpreenda, app inovador, visual diferente do que vimos"). **Visual NOVO**
>> (dia claro de jardim: Canvas com sol+raios, nuvens, morros, flores, borboletas), **mascote NOVO = o
>> Broto** (broto de plantinha fofo, desenhado no Canvas). **4 dinâmicas variadas:** (1) **Plantar**
>> = simulação (toca Sol/Água → a planta cresce em estágios); (2) **Ordenar** = sequência do crescimento
>> (semente→broto→planta→flor→fruto); (3) **Do que precisa** = classificar (com pegadinhas: refri/celular/
>> meia = "não precisa"); (4) **Partes da planta** = tocar a parte pedida (raiz/caule/folha/flor). Fonte
>> Fredoka embutida, som Web Audio, confete. **Sem emoji** visível (verificado). BNCC 2º ano: seres vivos/
>> plantas e suas partes; do que a planta precisa para viver.
>> - **Arquivos:** `_jardim/index.html` (1 HTML autossuficiente) + `_jardim/manifest.json`.
>> - **Repo publicado:** `jardim-do-broto` → **https://vidalprof.github.io/jardim-do-broto/**
>>   (criado pela Fábrica `fabrica.yml`, source_dir=_jardim, em 2026-07-22).
>> - **Republicar/atualizar:** `atualizar.yml` (repo_name=jardim-do-broto, source_dir=_jardim, ref=branch).
>> - **Pendente/futuro:** entrar no portal (`_portal`/hub) como card; QA 3 níveis formal; voz/narração;
>>   possível 5ª dinâmica (mistério "por que a planta murchou?"). É experimento de VISUAL novo (2º ano).
>> - **⭐ +VARIEDADE DE MECÂNICA (2026-08-01) — de ~15 min para ~45 min de aula.** O Marcos perguntou
>>   "foram utilizadas várias interatividades? tradicionais? caça-palavras etc?" — eu CONTEI e a resposta
>>   honesta era **não**: quase tudo era toque/múltipla escolha. Foram acrescentadas **4 mecânicas novas**,
>>   todas pensadas para 7 anos (**sem teclado**, sem leitura longa), encaixadas no fluxo linear:
>>   1. **Caça-palavras 6x6** (`telaCacaJd`, depois de `telaPrecisa`) — acha SOL, AGUA, TERRA, AR.
>>      Toca na 1ª e na última letra. **A validação é POR LETRA, não por posição plantada** (lê o caminho
>>      reto entre as duas células e compara com a lista): assim, se as letras aleatórias formarem a palavra
>>      por acaso, a criança também acerta — e palavras que se cruzam continuam clicáveis (célula já `.ok`
>>      NÃO bloqueia a seleção; guardo `ant` p/ devolver a cor certa se errar). Isso curou o "não achei a 4ª".
>>   2. **Monte o nome** (`telaMontaPalavra`, entre partes e funções) — letras embaralhadas de RAIZ/CAULE/
>>      FOLHA/FLOR + pista falada. É **produção sem teclado**: só a próxima letra certa entra no slot
>>      (andaime forte, sem precisar de "apagar"); letra errada balança e conta erro.
>>   3. **Memória parte × trabalho** (`telaMemoria`, antes de "Ensinar o Broto") — 8 cartas em **2 col × 4
>>      linhas**, verso com a carinha do Broto (nada de emoji), 4 pares (RAIZ↔bebe água, CAULE↔segura em pé,
>>      FOLHA↔toma sol, FLOR↔vira fruto).
>>   4. **Desafio relâmpago** (`telaRelampagoJd`, antes do fim) — 45 s, "precisa / não precisa" com placar
>>      e barra de tempo; reaproveita as imagens `jd_*` que já existiam (**nenhuma imagem nova foi precisa**).
>>   - **Narração:** 10 falas novas do Broto (`jd_caca_*`, `jd_monta_*`, `jd_mem_*`, `jd_rel_*`), geradas pelo
>>     `finalizar.yml` com `pt-BR-AntonioNeural` (mascote masculino = voz masculina) e copiadas p/ `_jardim/audio/`.
>>   - **Medição:** sem conceito novo — caça e relâmpago alimentam `necessidades`, montar alimenta `partes`,
>>     memória alimenta `funcoes` (o painel do professor continua com as 5 barras de sempre).
>>   - **QA rodado:** `node --check` do JS extraído; **check de classe-sem-CSS** (só sobrou `base`, que é
>>     marcador do lip-sync, sem estilo próprio — ok); **auditor de sobreposição** nas 17 telas em 360x640 e
>>     412x840 → `[]`; e um **teste funcional Playwright** que RESOLVE as 4 mecânicas de verdade (4/4 palavras,
>>     4 palavras montadas, 4 pares, placar do relâmpago) — não bastava a tela abrir.
>>   - **⚠️ Armadilha do container:** `curl` para `*.github.io` dá **code 000** (rede bloqueada) — isso NÃO
>>     quer dizer "não publicou". Quem diz a verdade é o `deploy-pages.yml` (`status=built erro=nenhum`).
>>     Publicado em 2026-08-01 (build `built`, commit 9c8eaca).
>> - **🐛 LIÇÃO PAGA — BALÃO DE DICA SOBREPONDO (Marcos reportou 2026-08-01; eu NÃO tinha visto).**
>>   O meu auditor de sobreposição dizia `[]` e mesmo assim o Marcos via balão em cima de imagem. Ele
>>   estava certo. Eram **DUAS** causas, e nenhuma aparecia no auditor porque ele só media o **estado
>>   inicial** de cada tela, sem clicar em "Dica" e sem trocar de tela:
>>   1. **Vazamento entre telas.** `mostraDica` cria o `#dicabox` em `document.body` com auto-remoção em
>>      6,5 s, mas `limpa()` só zerava o `#app` — o balão da tela ANTERIOR continuava boiando sobre a tela
>>      seguinte. Conserto: `tiraDica()` chamado dentro de `limpa()`.
>>   2. **Cobria na própria tela.** O balão era `position:fixed; bottom:86px; z-index:14` → passava por
>>      cima do que estivesse ali. Medido: **20–26 mil px²** de `.opts` cobertos nas telas de Gêneros
>>      (360 e 412 de largura) e pior a 320 (cobria a grade do caça-palavras). Conserto **estrutural**:
>>      a dica **não flutua mais** — entra NO FLUXO, logo depois do `.balao` da pergunta (classe `.dicain`),
>>      empurrando o conteúdo em vez de cobrir. Some sozinha em 7 s.
>>   - **REGRA NOVA DE QA (o auditor sozinho não basta):** testar também (a) **com a dica aberta**, (b) a
>>     **transição** tela A→dica→tela B, e (c) a largura **320×568**, não só 360/412. Os scripts:
>>     `/tmp/mesma.js` (dica na própria tela), `/tmp/leak.js` (vazamento entre telas), `/tmp/vis.js`
>>     (a dica continua visível, não foi parar embaixo da dobra).
>>   - **Ressalva honesta que sobrou:** a 320×568, na tela `gTrocado`, 3 frases longas não cabem — as
>>     opções passam atrás da barra de baixo enquanto a tela está no topo. Verificado que **rolando 58px
>>     nada fica coberto**. Em PC da escola e celular normal não acontece.
>>   - **`_estrelas` NÃO tem esse bug** (não usa o padrão `dicabox`).
>> - **🚨 BUG GRAVE — TELA PRESA (`gLigar`), achado pelo Marcos em 2026-08-02.** Ele disse:
>>   *"tem uma fase de embaralhar que repete, não sai disso, a mesma fase"*. Estava certíssimo.
>>   Ao inserir a mecânica nova `gLigar` (ligar colunas) eu copiei a linha do `gFuncao` e **esqueci de
>>   trocar o destino**: ficou `mostraBanner("Cada gênero tem a sua função!", gLigar)` — a tela chamava
>>   **a si mesma**. Consequência real, muito pior do que "repete": **6 telas ficaram inalcançáveis**
>>   (`gBanca`, `gAquec`, `gTrocado`, `gMonta`, `gEnsinar`, `gFim`). A criança NUNCA terminava a missão
>>   de Gêneros, nunca ganhava a medalha, nunca marcava "feito" — e, com o menu em progressão, a
>>   Missão 3 jamais destrancaria. Conserto: `gLigar` → **`gBanca`**, com mensagem própria.
>>   - **Por que meu QA não pegou:** o auditor de sobreposição abre cada tela ISOLADA (`window[f]()`)
>>     e mede o layout. Ele nunca **percorre o caminho**. Layout perfeito, fluxo quebrado.
>>   - **FERRAMENTA NOVA — `_qa/fluxo.py` (usar SEMPRE que inserir/remover tela):**
>>     `python3 _qa/fluxo.py _redacao/index.html telaCapa` → acusa **TELA PRESA** (volta pra si mesma)
>>     e **TELA ÓRFÃ** (ninguém chega nela). Rodando na versão com bug ele acusa o `gLigar` + as 6 órfãs;
>>     na corrigida diz "fluxo ok". Já passa limpo nos 3 apps. Detalhes que custaram acerto: incluir
>>     **todas** as funções no grafo (uma tela pode ser chamada de dentro de um ajudante), ler a
>>     **tabela de paradas** do Estrelas (`fn:function(){telaSoma();}`), e ignorar `telaPainel`/
>>     `telaPainelPin` (abrem pelo `?painel`) e os helpers `*Base`.
>>   - **Robô que joga sozinho (`/tmp/jogar.js`):** instrumenta as funções de tela, clica cada candidato
>>     UMA vez por tela e espera. Confirmou `gAbertura → ... → gFim` (10 telas) e a cadeia dos Verbos.
>>     **Lição do robô:** clicar rápido demais ATROPELA o `depoisDaFala` — cada erro dispara uma narração
>>     nova e o banner nunca chega. Isso me deu 3 falsos alarmes (`vCaca`, `vEscreve`). Antes de gritar
>>     "bug", esperar a narração (até 9-10 s) e conferir à mão.
>> - **📏 CONTAGEM REAL DE FASES (2026-08-02) — Redação do Pingo = 24 telas:** Missão 1 Verbos **13**
>>   (abertura, prever, revela, 4 notícias, caça-palavras, ficha, aquecimento, tempo, concordância,
>>   escrever, manchete, ensinar, fim); Missão 2 Gêneros **10**; Missão 3 Relâmpago **1**.
>>   ⚠️ Antes do conserto do `gLigar`, a Missão 2 entregava só **4** das 10 telas — a estimativa de
>>   "20–25 min" que eu tinha dado estava errada por causa disso.
>> - **⭐ CRACHÁ = O PRÓPRIO BROTO (2026-08-01).** Antes a tela de identidade oferecia as figurinhas
>>   dos **estágios da planta** (`jd_g0..jd_g4`) — errado pela regra do Marcos ("o crachá tem que ser o
>>   MESMO mascote, só com cores e roupas/acessórios diferentes"). Agora são **6 variantes do Broto**
>>   (`jd_cr1..jd_cr6`), geradas no Gemini **EDITANDO a imagem-âncora** (`base: _novo/jd_broto_base.png`,
>>   que é o `jd_broto_feliz` achatado sobre branco — PNG transparente como base faz o alfa virar preto):
>>   1 verde + chapéu de palha · 2 verde-azulado + óculos · 3 verde-limão + laço vermelho no broto ·
>>   4 rosa + margarida na cabeça · 5 verde-escuro + bandana azul · 6 lilás + chapéu de sol laranja.
>>   Recorte com o `cut_border()` (floodfill só das bordas), 200px de altura, ~40KB cada.
>>   Grade **3×2** (`.figs{max-width:270px}`, `.fig{82px}`) p/ o acessório ficar legível.
>>   **Migração no `carregaEstado`:** perfil salvo com `fig` antigo (`jd_g3`) é convertido p/ `jd_cr1` —
>>   senão a criança que já jogou voltaria sem nenhuma figurinha marcada.
>>   - **Observação em aberto:** o crachá escolhido só aparece NA TELA DE ESCOLHA (no Jardim e também na
>>     Redação do Pingo). A criança escolhe e nunca mais vê. Vale mostrá-lo no fim/medalha um dia.
>> - **⭐ VISUAL HÍBRIDO (Marcos 2026-07-22: "parece feito à mão, quadrado" → refeito):** a 1ª versão era
>>   toda Canvas desenhado à mão (chapado). O Marcos reprovou. Refiz no **HÍBRIDO** (respeitando a LEI
>>   "todo asset que a criança vê é IA"): **fundo, mascote (Broto), 5 estágios de crescimento e os itens
>>   viraram ILUSTRAÇÕES REAIS geradas no Gemini** (lote `_gerar_imagens.json` + commit `[imagens]` →
>>   `finalizar.yml`), com **animação suave por cima** (bob do mascote, cross-fade dos estágios, faíscas/
>>   gotas em Canvas, pólen/borboletas). Ficou nível storybook/Duolingo. **É ESTE o padrão visual daqui
>>   pra frente** (não desenhar à mão no Canvas o que a criança vê).
>>   - **Receita reutilizável do híbrido (guardar!):** (1) escrever prompts "soft 3D cartoon, fundo branco
>>     liso #FFFFFF p/ recorte, NO text/letters/numbers" no `_gerar_imagens.json`; (2) commit `[imagens]`
>>     → puxar de `_novo/`; (3) **recorte branco→transparente** com Pillow **floodfill a partir dos cantos
>>     de cima** (preserva branco interno dos olhos E a faixa de terra do `jd_partes`), autocrop nos avulsos,
>>     MANTER quadro quadrado nos estágios/partes (registro consistente p/ cross-fade e p/ as zonas de toque
>>     em %), fundo salvo como JPG; (4) imagens em `_jardim/img/` (arquivos, ~1,4MB total, sw-cacheia) —
>>     **não** base64 (evita HTML gigante). Render/QA com **Playwright** (chromium `/opt/pw-browsers/
>>     chromium-1194/chrome-linux/chrome`, `click{force:true}` p/ furar animação `beat`).
>>
>> ## 🆓 GERADOR DE IMAGEM GRÁTIS EM LOTE (Pollinations/FLUX) + truque do lip-sync — 2026-07-22
>> Quando a **cota do Gemini estourar** (429 — a grátis é baixa; billing precisa estar no MESMO projeto
>> da chave do secret `GEMINI_API_KEY`), use o **`gerar-poli.yml`** (criado 2026-07-22): lê `_gerar_poli.json`
>> (lista de `{nome,prompt,w,h,seed,model}`) e gera TUDO no **Pollinations (FLUX, grátis, sem chave)**, commit
>> em `_novo/`. Dispara por **push com `[poli]`** na mensagem. Qualidade rivaliza o Gemini com **super-prompt**
>> ("3D render, soft clay plasticine, subsurface scattering, Pixar Disney style, isolated on flat pure white
>> background, no shadow, no text"). Pollinations e HF e Cloudflare usam FLUX por baixo → "grátis bom" é parecido.
>> - **Truque do LIP-SYNC no grátis (funciona!):** o Pollinations não EDITA base como o Gemini, MAS gerando
>>   os quadros do mascote (base/fala/pisca/poses) com a **MESMA SEED** e mudando só a boca/olhos no prompt,
>>   sai quase idêntico → as camadas encaixam e o lip-sync (overlay de opacidade) funciona. Recorte: matte por
>>   luminância+saturação (tira branco/cinza-claro, preserva cor saturada) + floodfill dos cantos; para props
>>   com sombra, **regerar com "no shadow, floating, flat pure white background"** que corta limpo. Alinhar os
>>   quadros do mascote pela **MESMA caixa de corte fixa** (senão o lip-sync "pula").
>> - **Fábrica de Estrelas 2026-07-22:** o Marcos pediu **arte nova** (mesmo já estando no molde). Refiz TODA a
>>   arte no Pollinations (Fagulha 3D nova + fábrica + céu + caixa + estrelas), motor 100% intacto (narração/
>>   medição/BKT/Leitner/lip-sync). Publicado em `fabrica-de-estrelas`. Backup da arte antiga em `/tmp` (sessão).
>>   Pendência menor: sombrinha bege num canto da caixa do tesouro (dá pra limpar).
>> - **NOTA de custo:** Gemini edita base perfeito (lip-sync pixel-perfect) mas custa/tem cota; Pollinations é
>>   grátis e "quase lá" com seed fixa. Para MASCOTE novo com lip-sync perfeito → Gemini (billing no projeto certo);
>>   para volume/cenário/props → Pollinations resolve de graça.
>> - **🔑 DIAGNÓSTICO DEFINITIVO do 429 do Gemini (2026-07-22):** a mensagem exata é **"Your prepayment credits
>>   are depleted. Please go to AI Studio to manage your project and billing" (RESOURCE_EXHAUSTED)**. Ou seja:
>>   o **billing JÁ está no projeto certo da chave** (senão diria "ative billing") — o que acaba é o **CRÉDITO
>>   pré-pago**. Conserto = o **Marcos RECARREGA** em https://aistudio.google.com → Billing (os ~60 reais dele).
>>   NÃO é bug nosso, NÃO é projeto errado. Só faltou saldo. (Só ~16 imagens do Jardim não gastariam 60 reais →
>>   provável que já estava perto de zero.) **Os 3 nomes de modelo:** só `gemini-2.5-flash-image` existe; os outros
>>   2 do fallback dão 404 (tirar do código algum dia). **~R$/imagem: centavos** (12 imgs < R$1).
>> - **⚠️ O grátis NÃO iguala o Jardim:** Pollinations/Cloudflare/HuggingFace = todos **FLUX** (brilhoso, borda
>>   difícil de recortar → "pedaço faltando"). O acabamento fosco/massinha lindo do Jardim é **do Gemini** e só ele
>>   faz. O Marcos reprovou a tentativa Pollinations na Estrela; **restaurei a arte ORIGINAL** dela (backup) e a
>>   arte nova fica pra quando o crédito Gemini voltar. (Se um dia quiser pagar OUTRA: OpenAI gpt-image / Flux
>>   Kontext editam bem, mas é gastar noutro lugar tendo o Gemini.)
>> - **✅ RESOLVIDO (2026-07-23):** o Marcos gerou uma **chave nova no projeto QUE TEM crédito** e atualizou o
>>   secret `GEMINI_API_KEY` → Gemini voltou. Refiz a **Fábrica de Estrelas TODA no Gemini** no acabamento
>>   massinha do Jardim: Parte 1 (base Fagulha + fábrica + céu + caixa + estrelas, `_gerar_imagens.json` [imagens]),
>>   Parte 2 (**editar a base** `_novo/fagulha.png` → fala/pisca/pensa/comemora/acena, "mude SÓ a boca/olhos" =
>>   lip-sync pixel-perfect). Recorte só-borda (fundo branco limpo do Gemini = sem pedaço faltando). Publicado em
>>   `fabrica-de-estrelas`. **LIÇÃO:** se der "prepayment credits depleted" e o Marcos "recarregou", quase sempre
>>   a chave é de OUTRO projeto → o certo é **criar chave nova no projeto com crédito** e trocar o secret.
>>
>> ## 🎙️ JARDIM DO BROTO virou PREMIUM (2026-07-23) — o Marcos cobrou: "com as nossas configurações de áudio etc"
>> O Marcos perguntou se o Jardim podia ter **nossas interatividades comuns**. Estava certo: o Jardim era só
>> "casca bonita" (64 KB, sem voz/medição). **REGRA REAFIRMADA: toda atividade nova CLONA o motor** (MOLDE) —
>> não basta visual. Agora o Jardim tem (83 KB + 31 MP3 + imagens = 3,4 MB):
>> - **Narração do Broto** (31 falas, `_lote_falas.json` → `finalizar.yml [audio]`, voz **masculina** Antonio)
>>   + **LIP-SYNC** por camadas de imagem (base/fala/pisca geradas no Gemini editando a base = alinhadas).
>> - **REGRA DE VOZ DO MARCOS:** *mascote masculino → voz masculina; mascote feminino → voz feminina.*
>>   "O Broto" = masculina. ✅ **RESOLVIDO (2026-07-23):** a mascote das Estrelas se chamava "A Fagulha"
>>   (feminino) com voz masculina. O Marcos decidiu **trocar o NOME** (mais barato que regravar 85 falas):
>>   agora é **"O BRILHO"** (masculino). Descoberta que barateou tudo: de 1046 falas do histórico, **só UMA
>>   dizia o nome** (`abertura.mp3`) → regenerei só ela. Troca no texto feita com gramática ("a Fagulha"→
>>   "o Brilho", "da Fagulha"→"do Brilho"); **os arquivos de imagem seguem `img/fagulha*.png`** (nomes
>>   internos, não aparecem para a criança — não renomear à toa). Uma animação CSS virou `pontosBrilho`
>>   (definição e uso trocados juntos, conferido).
>> - **Dica** (botão + fala), **Ouvir de novo**, banner, **prever-antes (POE)**, **experimento de 3 vasos**
>>   (variável controlada: escuro / sem água / sol+água), **aquecimento** (revisão espaçada), **função das
>>   partes** (pergunta pela FUNÇÃO, sem o nome = produção), **Ensinar o Broto** (autoexplicação),
>>   **identidade** (nome + figurinha), **medalha**, **medição invisível + BKT-lite** e
>>   **parecer do professor em `?painel`** (domínio por conceito, dicas, tempo, GANHO antes×depois, BNCC).
>> - **BNCC:** EF02CI05 (água e luz) + EF02CI06 (partes e funções).
>> - **Narração NUNCA é atropelada:** `depoisDaFala(id,maxMs,cb)` — o prazo só dispara se o áudio NÃO estiver
>>   tocando (mesmo bug pago das Estrelas). No teste headless isso faz cliques "falharem" — é o certo, não é bug.
>>
>> ## 🎮 DECISÕES DO MARCOS (2026-07-22) — "atrativo, visual, simulação real, sem bug" — LER
>> Registradas em detalhe no `MOLDE-ATIVIDADE-PREMIUM.md` (§4½, §4⅗, §4⅘, §6, §9). Resumo:
>> - **JOGO, não formulário (§4⅗):** o que ensina certo mas parece medidor/lista/questionário NÃO prende.
>>   A criança **brinca COM o mundo** (toca/arrasta/pinta direto no planeta/mapa), com **reação visual +
>>   recompensa** a cada ação e **missão** ("o planeta apagou — reacenda"). Fora os +/− sempre que der.
>> - **Simulação REAL:** modelo por trás (ex.: `bioma(temp,chuva)`, ângulo do Sol→temperatura, altitude→
>>   clima) com resposta visual IMEDIATA. Não é 3D pesado — CSS/Canvas 2D/partículas/procedural, PC fraco.
>> - **Didática SEM aula (§4⅘):** ser progressivo = **andaime** (beat concreto → exemplo trabalhado do
>>   mascote → ✓ na hora por item), NÃO vídeo/texto obrigatório antes de agir (isso viola as leis). A
>>   "explicação da matéria" vem como **cutscene animada narrada / infográfico tocável / a própria
>>   simulação** + botão **"Saiba mais" OPCIONAL**. **~10–12 beats** p/ 55 min (5 é pouco).
>> - **Disciplina muda a mecânica (§6):** matemática = EXECUTAR (procedimento basta); geografia/ciências =
>>   COMPREENDER (espacial/sistêmico) → exige simulação real + mecânica visual/espacial (mapa em camadas,
>>   climograma, corte de relevo). O pedagogo escolhe pela demanda da disciplina.
>> - **Mascote (§4½), bugs que o Marcos pegou e o conserto:** (a) **recorte transparente** (fim do quadrado
>>   branco/preto); (b) **lip-flap NÍTIDO** (boca aberta/fechada com histerese — acaba o "fantasma" de boca
>>   meio-aberta que parecia bug); (c) **`fala`/`pisca` = base + só a boca/olhos** (senão o corpo treme ao
>>   falar); (d) **TODA pose de gesto volta à neutra** (comemora/aponta) — senão narra "com o braço no ar".
>> - **LIP-SYNC POR VISEMAS — IMPLEMENTADO (2026-07-22):** a Nara agora fala com **4 bocas** (fechada/
>>   meio/aberta/'O') sincronizadas pela timeline do **Rhubarb** (`gerar-audio.yml` com `visemas=sim`
>>   → `_clima/visemas.json`; app faz `fetch` e troca a boca no tempo). Fallback p/ flap RMS. É o
>>   **padrão-ouro reutilizável** — ver `MOLDE-ATIVIDADE-PREMIUM.md §4½` item 7.
>> - **Progresso do Planeta Vivo (arco):** já no novo padrão jogo/simulação — Parada 1 (latitude),
>>   LEI clima→bioma, Altitude, **Climograma**. Faltam: mapa em camadas, chuva orográfica, cutscene,
>>   geo-mistério; subir Tempo×Clima/Autoria/Desafio; QA final + auditoria ~55 min.
>> - **Duas pesquisas profundas rodando (2026-07-22):** (1) mecânicas interativas de GEOGRAFIA p/ 6º ano;
>>   (2) ARSENAL TÉCNICO (animação/lip-sync 2D, simulação leve, imagens IA consistentes, voz, desempenho).
>>   Quando chegarem → alimentar `CATALOGO-DINAMICAS-INTERATIVAS.md` e virar plano de mecânicas por beat.
>> - **PESQUISA "SIMULAÇÕES QUE ENSINAM" — CHEGOU (2026-07-22):** salva em
>>   `PESQUISA-SIMULACOES-EFICAZES-2026-07.md` (103 agentes, 23/25 claims). 6 achados: (1) realismo
>>   FUNCIONAL (carrega o mecanismo) > decorativo; (2) podar enfeite sedutor; (3) NÃO abstrair demais
>>   p/ 11–12 anos; (4) andaime IMPLÍCITO (a meta vira o controle, feedback imediato — jeito PhET);
>>   (5) indagação guiada leve POE (prever→observar→explicar), não demonstração passiva; (6) REFUTAR a
>>   concepção errada (nomear o erro → mostrar o certo). Já entrou no molde. **1º passo aplicado:** LEI
>>   clima→bioma agora mostra o MECANISMO em palavras (rótulos Sol/Nuvem + leitor "clima → bioma").
>>   **APLICADO POR INTEIRO (2026-07-22, sw v8, no ar):** (1) **POE — portão "Prever"** reutilizável
>>   (`preverGate`) antes de cada simulação (latitude/clima/altitude), 1x/parada (flag `PREV`), narração
>>   feminina nova (`prev_p1/prev_p3/prev_p4`); o "Explicar" é o `autoexplica` do fim. (2) **Refutação**
>>   (`refutaCard`: "Muita gente pensa… / Na verdade…") na revelação da latitude e altitude — **DENTRO** da
>>   caixa `.revela` (é `position:absolute`; card em fluxo normal sobe pro topo e sobrepõe o balão — LIÇÃO
>>   paga). (3) **Climograma → bioma** (`clgMostraBioma`): o gráfico montado revela o LUGAR (imagem do
>>   bioma). (4) **BUG REAL PEGO:** `FAT` (altitude) nunca declarado com `var` → em `"use strict"`
>>   `telaFatores()` lançava "FAT is not defined" e a altitude QUEBRAVA (tela branca). Fix: `var FAT;`.
>>   Planeta Vivo é novo, ainda sem QA em PC real — por isso não fora pego. Lição: declarar `var` p/ o
>>   estado de CADA tela (ZON/LEI/CLG tinham; FAT faltava). Falta ainda: corte transversal da montanha.
>>   **CLIMOGRAMA REFEITO p/ ser DEDUTÍVEL (Marcos apontou: resolvia por tentativa; a Savana [3,2,0,1]
>>   não saía da dica):** agora 3 níveis (0 seco/1 chuva/2 muita chuva) e CADA estação tem uma PISTA do
>>   tempo (ícone+palavra) — a criança LÊ o tempo e levanta a barra até bater (traduz tempo→gráfico = a
>>   habilidade real de climograma), sem adivinhar. + rodada DESERTO (contraste). No fim o gráfico vira o
>>   bioma (clgMostraBioma). sw v9. Regra p/ toda simulação de "montar": o alvo tem de ser DEDUTÍVEL de
>>   uma pista visível, nunca só do feedback verde (senão é adivinhação, não aprendizado).
>>   **CENA da simulação clima→bioma MUITO mais viva (Marcos: 'animação meio fraca'), sw v10:** o canvas
>>   era 300x200 ESTICADO p/ um container mais alto (distorcia+borrava) — agora casa a resolução ao tamanho
>>   REAL (LEI._cena.clientWidth*1.35, cap 520x560). Arte reescrita em Canvas 2D leve: céu 3 tons c/ horizonte
>>   quente, SOL com glow+raios girando, nuvens de fundo à deriva, morros (profundidade), chão em gradiente,
>>   e FLORA por bioma (árvores de copa em camadas, cactos saguaro, pinheiros 3 tiers c/ neve, capim/acácia
>>   com balanço). Helpers: leiSol/leiNuvemFundo/leiMorros/leiChaoCor/leiArvore/leiPinheiro/leiCacto/leiCapim/
>>   leiAcacia/leiMoita/rr. Lição: canvas com width/height fixos DENTRO de container flex vira borrão — sempre
>>   casar a resolução do buffer ao tamanho real (1x-1.4x) p/ nitidez.
>>   **2 IDEIAS INOVADORAS aplicadas (2026-07-22, sw v11):** (a) **CINEMA DA JOGADA** (`telaCinema`) — no
>>   fim, a Nara narra um recap PERSONALIZADO da jornada DAQUELE aluno (puxa dos eventos medidos + nome):
>>   torna a medição visível/emocionante e reforça memória (recuperação). (b) **ENSINAR A NARA** (efeito
>>   protégé: quem ensina aprende mais) — `autoexplica` ganhou flag `ensinar:true`: a Nara AFIRMA o erro
>>   ('neva no alto porque é mais perto do Sol') e a criança a CORRIGE; feedback vira 'Você ensinou a Nara!'
>>   + narração `ens_p4`/`ens_obrigada`. Aplicado na altitude (p4). Base: pesquisa de EdTech (Betty's Brain/
>>   teachable agents). Também: corrigido o PARECER do Planeta Vivo que ainda falava em multiplicação/array
>>   (copiado do estrelas) → agora geografia (clima→bioma; EF06GE05/03). **Nova pesquisa profunda RODANDO**
>>   (apps educacionais: o que os faz amados+eficazes, código por dentro, medição, aventura; checklist
>>   profissional) — quando chegar, destilar em regras do molde.
>>   **CHEGOU (2026-07-22) → `PESQUISA-APPS-EDUCACIONAIS-PROFISSIONAIS-2026-07.md` (110 agentes).** VEREDITO:
>>   nossa direção está CORRETA. Chaves: (1) INTEGRAÇÃO INTRÍNSECA é o coração (o conceito É a mecânica de
>>   vencer — nossas simulações já fazem); (2) gamificação (streak/badge) eleva motivação, NÃO domínio, e é
>>   mais fraca aos 8–12 → não depender dela; (3) recompensa: só SURPRESA (prometida por algo já gostoso reduz
>>   interesse — superjustificação, Lepper 1973); (4) o que separa os eficazes = feedback EXPLICATIVO + andaime
>>   personalizado + medição por aluno (XPRIZE); (5) mascote NÃO ensina por si (validar, não presumir); (6)
>>   ENSINAR o mascote (Betty's Brain/teachable agents) é ouro e leve → aprofundar via mapa causal. Há um
>>   CHECKLIST premium de 12 itens no doc. Também: **Cinema da jogada + Ensinar o mascote portados p/ a Fábrica
>>   de Estrelas** (sw v24) e Planeta Vivo (sw v11). Regra nova p/ o molde: recompensa só surpresa; feedback
>>   sempre EXPLICATIVO; todo premium tende a um 'chefe' de transferência.
>>   **PRÉ/PÓS — GANHO REAL (Planeta Vivo sw v12):** o diferencial 'profissional' da pesquisa. NÃO é prova
>>   disfarçada: reaproveita o POE — palpite inicial (`previsao.previu_certo`, marquei o certo com `ok:true`
>>   nos 3 preverGate) × compreensão do fim (`autoexplicacao`/`ensina_mascote`.razaoOk). `salvaParecerProf`
>>   computa por conceito: previu ERRADO→entendeu = APRENDEU; previu certo→certo = já sabia; senão = ainda
>>   construindo. Campo `parecer.ganho` + texto 'GANHO...' que o professor vê no ?painel, ESCONDIDO do aluno.
>>   Regra p/ molde: todo premium mede GANHO (pré×pós), não só acerto final. Falta: portar POE+ganho ao estrelas.
>>   **Fábrica de Estrelas (2026-07-22):** ficou curta → **escada de 3 itens
>>   curados por parada** (18 itens, era 8) + **epílogo encenado em 3 beats** (narração final/final2/final3,
>>   voz feminina) + "curadoria não sorteio" (itemIdx, sem Math.random no conteúdo). sw v23, no ar.
>> - **Áudio:** `gerar-audio.yml` ganhou input **`outdir`** (mp3 direto na pasta da atividade, sem colidir
>>   ids com o `_audio/` do estrelas); voz **feminina (Francisca)** p/ mascote menina.
>> - **Capa:** nada de "medalha" com anel dourado (o Marcos achou amador) → **Terra girando** (2 cópias em
>>   `transform` mascaradas por círculo + sombreamento de esfera + atmosfera). Biomas viram **JPG** (leve).

## ⚖️ AS LEIS FIXAS DO EDUCAVERSO + COMO A FÁBRICA FUNCIONA DE VERDADE (Marcos aprovou, 2026-07-19)
> **LER SEMPRE antes de criar QUALQUER atividade. O Marcos cravou isto nesta sessão.**
>
> **A) A FÁBRICA É AQUI, COMIGO — não é app nem site que gera sozinho.**
> O Marcos me dá **TEMA + TURMA** na conversa e **EU** produzo a atividade. O formulário
> "clica GERAR" (`Fabrica.ts`) e a IA-no-navegador (Pollinations, `ia-conteudo.ts`) **NÃO**
> são o caminho de produção — aquilo gera conteúdo raso ("mais do mesmo"). O **especialista de
> verdade sou eu**, aqui, com toda a nossa pesquisa na mão. **Gerar ≠ jogar:** gerar é nosso,
> na conversa; o app/site é só onde o **aluno joga** o resultado pronto (o link).
>
> **B) O ESPECIALISTA VESTE 3 CHAPÉUS numa pessoa só** (é a soma que faz a diferença):
> **(1) professor PhD da disciplina** que o Marcos passa (sabe como o humano aprende ESTE
> conteúdo, onde trava, o erro clássico); **(2) cientista da aprendizagem/neurociência** (projeta
> pela nossa pesquisa, não por achismo); **(3) desenvolvedor de RPG 2D** (sabe o que dá pra
> PROGRAMAR, então desenha o JOGO, não descreve um vídeo). O 3º chapéu é o que faz eu saber **o
> que programar pra criança aprender de forma eficaz — onde ela NÃO é mera espectadora**.
>
> **C) MOTORES SÃO REUTILIZÁVEIS — NÃO é um motor por tema** (isso seria inviável; o Marcos
> perguntou e esta é a resposta). Um jeito de aprender se repete em dezenas de conteúdos. A gente
> constrói um **catálogo pequeno (~6–10 motores profundos)** que cobre a maior parte da BNCC;
> cada tema novo é uma **CONFIGURAÇÃO** de motores que já existem (+ história + arte). Custo **na
> frente e amortizado**. Motores fundos ≠ mecânicas de quiz: são **verbos de construção**
> (repartir, equilibrar, montar, reparar, regular um medidor, ligar causa→efeito, decidir com
> consequência, simular). **1º motor profundo a construir: "REPARTIR JUSTO"** (cortar em partes
> iguais + medir na reta + sobrepor) → serve **frações, decimais, %, razão/proporção, divisão,
> comparação**. Outro motor citado: **"acúmulo → limiar → consequência"** (a "Máquina da Revolta"
> da Revolução Francesa; serve multicausalidade: causas de revolução, fatores de ecossistema, etc.).
>
> **D) FORMATO DE SAÍDA obrigatório do especialista — a FICHA DE 5 CAMPOS por fase** (é o que
> impede a aula virar textão+clique): **🎯 Objetivo** (o micro-conceito) · **🕹️ VERBO** (o que a
> criança FAZ com as mãos: cortar, repartir, montar, medir…) · **🧩 MOTOR** (o que o motor mostra
> e guarda) · **⚙️ REGRA** (o que o código calcula pra decidir certo/errado — estado do mundo, não
> gabarito A/B/C/D) · **🌍 CONSEQUÊNCIA** (o que a criança VÊ acontecer). + 1 linha "o que o
> engenheiro precisa construir de novo". **Se um passo não vira sistema jogável, é texto =
> espectador → reprova.** Proibido: pop-up de pergunta, "arraste a resposta certa", caça-palavras,
> NPC que dá a resposta.
>
> **E) AS LEIS FIXAS (todo tema passa por elas; entram como Portão 0 no QA):**
> 1. **VERIFICADO SEMPRE** — 2 níveis: (i) **portões de QA** antes de chegar na criança (Portão 0
>    filosofia, 1 funciona, Arte, aprovação do professor); (ii) **o motor adaptativo MEDE cada
>    criança ao vivo** (BKT por conteúdo: particionou sem chutar? acertou a transferência?).
>    Honestidade: a prova **final** é o dado da **sala real** — nunca afirmar "aprendeu" sem isso.
> 2. **CONCRETO SEMPRE** — a criança **manipula coisa real primeiro** (corta o pão, reparte,
>    sobrepõe, mede). Nunca começa pelo símbolo. O nome/fórmula chega **por último** (Bruner:
>    concreto → pictórico → abstrato; nunca inverter).
> 3. **VIVENCIADO SEMPRE** — aprende-se **fazendo/vivendo**: Dewey (aprender fazendo), Piaget
>    (constrói agindo sobre o mundo), Bruner (ação→imagem→símbolo), Vygotsky (atividade + mentor
>    que pergunta + ZDP), Papert (aprende construindo), Lave & Wenger (conhecimento vive na
>    situação) + neurociência da **cognição corporificada** (o corpo agindo fixa melhor).
> 4. **A CRIANÇA PRODUZ/CRIA — não reconhece.** Ela constrói/monta/repara/decide/explica.
>    "Escolher a alternativa correta" = **prova disfarçada** = reprovado.
> 5. **O MUNDO JULGA por consequência física** — errou, a família reclama / a ponte não fecha /
>    a máquina trava. Nunca um gabarito escondido, nunca X vermelho.
> 6. **NA MEDIDA DA ZDP — progressivo, adequado, didático, NÃO difícil demais.** Todo aluno tem
>    que **entender e conseguir resolver**; um degrau por vez; o mentor **pergunta** pra puxar o
>    próximo passo; errar **devolve a peça sem punição**. Profundo **não** é o mesmo que difícil —
>    a profundidade está em **construir** a ideia, não em complicar.
> 7. **FIXAÇÃO exige REVISÃO ESPAÇADA** — uma sessão de 55 min **constrói mas não fixa**. Sem
>    **missões de retorno** dias depois (nosso motor Leitner), boa parte evapora (Bjork). Não
>    afirmar "aprende efetivamente" sem prever a revisão espaçada.
>
> **F) EXEMPLO TRABALHADO (referência de como fica) — FRAÇÕES, 5º ano, "A Festa da Vila".**
> 6 fases rodando 100% no motor **"Repartir Justo"** (padeiro reparte comida numa vila que
> precisa dela). BNCC do 5º: **EF05MA03** (fração como divisão + frações **maiores que 1** + reta
> numérica), **EF05MA04** (equivalência), **EF05MA05** (comparar/ordenar). Peso nos **saltos do
> 5º ano** (fração=divisão, 5/4 = "1 e 1/4"), não em metades que já trazem. **4 ajustes
> obrigatórios** (senão aprende ERRADO): (a) **travar o inteiro** — comparar só barras do mesmo
> tamanho; (b) **trampolim** 2÷4=1/2 antes do 3÷4; (c) mostrar 5/4 como **"1 e 1/4" E "5 quartos"**;
> (d) **revisão espaçada** depois. Veredito do especialista: adequada e ensina o conceito de
> verdade **com esses 4 ajustes**. A sequência escrita completa está no transcript desta sessão.

## 🚨 QUAL É "O JOGO 2D" DO MARCOS (correção 2026-07-20 — ele usou a senha "você esqueceu")
> **"O nosso jogo 2D RPG" = o RPG PIXEL estilo Kenney/Ninja Adventure** — a cena
> **`FaseGrid`** (educaverso-app, grid-engine + Tiled, kit "vilarejo"): herói 16px na
> vila, fazendeiro, casa com interior, potes de mel, **PEDRAS que fecham a saída e
> SOMEM na entrega** ("a pedra libera o caminho no final"). É o que a **Fábrica**
> (`?fabrica`) gera; publicado como `vila-viva` / `fabrica-aventuras`.
> **NÃO confundir** com a "Floresta do Byte" (motor `Mundo`/aventura.ts, arte pintada,
> Byte robô + Castor) — ela existe, mas quando o Marcos diz "nosso jogo 2D", é o PIXEL.
> Eu errei isso 1x (construí o agrupar no motor errado) e ele pagou tempo/crédito.
> **Dinâmica nova nasce na `FaseGrid` + Fábrica.** (O agrupar foi PORTADO pra lá —
> ver entrega abaixo; commit "FaseGrid (RPG pixel): mecanica AGRUPAR".)
>
> **✅ ENTREGA no jogo CERTO (2026-07-20):** mecânica **`agrupar`** na FaseGrid+Fábrica
> (pedagogo escolhe p/ tabuada/multiplicação; dinâmica CRIAR; tiers 8/12/18 por BKT).
> A criança pega caixas na pilha (decide QUANTAS), reparte os potes pelo mundo, o
> FAZENDEIRO testa: desigual → a caixa diferente TOMBA + pergunta + BKT; igual →
> conceito POR ÚLTIMO da arrumação DELA ("3×4=12") → PEDRAS somem → vitória.
> 2×6/3×4/4×3/6×2 todas vencem. Ações de pilha/vaga só quando PARA no tile (imune ao
> ciclo pega-devolve). QA `tools/qa-agrupar.mjs` == APROVADO == 19/19.
> Teste: **https://vidalprof.github.io/educaverso-app/?fabrica** (objetivo com
> "tabuada/multiplicação" → sai a fase agrupar). Publica por `app-build.yml` (ref=branch).

## 🍎 ENTREGA (no motor ERRADO — ver correção acima): "O POMAR DOS GRUPOS" (2026-07-20)
> **Contexto (a dor do Marcos, 2026-07-19/20):** ele reprovou TUDO que eu fiz FORA do
> jogo 2D (protótipos HTML soltos = "premium com popup", "não foi mundo vivo", "não
> adianta"). **O jogo 2D dele = o motor `Mundo` (educaverso-app, cena do montador v2)
> com a gramática "a pedra libera o caminho no final"** (quer_item→ao_receber→
> remove_bloqueio, aventura da ponte/floresta). REGRA DEFINITIVA: **dinâmica nova
> nasce DENTRO do motor `Mundo`, nunca em tela/página à parte.**
>
> **O insight que destravou ("como se programa criatividade"):** NÃO se guarda
> respostas — **programa-se a LEI do mundo** (mini-simulação) e o mundo aplica a lei
> sobre QUALQUER coisa que a criança construir. Quiz = comparar com gabarito (1 jeito
> de vencer). Lei = calcular consequência (MUITOS jeitos de vencer). Catálogo de
> ~6-10 LEIS reutilizáveis cobre a BNCC (lei da igualdade de grupos, do equilíbrio/
> apoio, do acúmulo-com-limiar…). **Conteúdo entra assim:** pedagogo traduz conteúdo
> → ideia-mãe → LEI + configuração + história (ex.: tabuada = grupos iguais).
>
> **O que foi construído (commit "motor Mundo: missao AGRUPAR..."):**
> - **`MissaoAgrupar`** no contrato (união discriminada c/ `colher`); auditor com
>   regras novas (inclui "a LEI precisa ser vencível": N divisível em 2..vagas grupos).
> - **Motor:** a criança ANDA no mundo, pega cestas na pilha (decide QUANTAS), reparte
>   as 12 maçãs; tocar numa cesta pousada = tirar de volta (reequilibrar sem punição).
>   Desigual no teste do Castor = a cesta DIFERENTE tomba + pergunta socrática + BKT
>   registra (kc `grupos-iguais`). Igual = conceito nomeado POR ÚLTIMO da arrumação
>   DELA (fala `c_3x4` etc.) → pedrona rola pra fora → bloqueio sai → portal → FEIRA
>   (festa). 2×6/3×4/4×3/6×2 TODAS vencem (sem gabarito = criatividade real).
> - **Aventura como DADOS:** `src/aventuras/grupos.ts` (tabuada 3º ano, EF03MA07),
>   boot `?grupos` (ou `window.__AVENTURA='grupos'`). 100% sprites que JÁ tínhamos
>   (maçã/cesta/castor/rocha). Kits novos (galinha etc.) = baixar por workflow depois.
> - **QA robô** `tools/qa-grupos.mjs` == APROVADO == (joga de verdade: erra 5/4/3 →
>   tomba+BKT; reequilibra; vence 3×4; pedra sai; atravessa; 2×6 também vence).
> - **Publicação:** `app-build.yml` (repo_name=educaverso-app, ref=branch) builda na
>   Action e força-push 1 commit limpo (histórico nunca incha; NÃO commitar dist).
>   Link de teste: **https://vidalprof.github.io/educaverso-app/?grupos**
>
> **⚠️ LIÇÃO DE ENGENHARIA (mordeu 2× no MESMO dia):** ação por PROXIMIDADE sem trava
> de revisita = **ciclo infinito parado no lugar** (pega-devolve na pilha; tira-deposita
> na cesta). **Cura padrão:** o ponto de ação age **1x POR VISITA** — sair do raio
> rearma (`pilhaLivre` / `v.livre`). Vale para TODA interação por proximidade futura.
>
> **Falas ainda SEM áudio** (avisos do auditor, esperado): gerar MP3s por
> `gerar-audio.yml` (Antonio p/ Byte; Castor = Antonio grave) quando o Marcos aprovar
> a dinâmica. Próximos passos se aprovar: voz + kit galinheiro (variação da mesma lei)
> + missões de retorno (Leitner) + 2ª LEI (equilíbrio/apoio — a ponte que aguenta).

## ⭐ NORTE OFICIAL (decisão do Marcos, 2026-07-20): A FÁBRICA DE JOGOS 2D
> **A visão:** o Marcos passa TEMA + ANO → os "profissionais" da fábrica (pedagogo,
> game designer, roteirista, diretor de arte, engenheiro, QA) entregam um JOGO 2D
> COMPLETO temático: leis do mundo certas p/ o objetivo, roteiro/história, pack visual,
> sons/animações, voz — seguindo a pesquisa (leis do mundo, não popup) e com
> aprendizagem efetiva MEDIDA (evidências→parecer→nota). O jogo 2D testado (vila-tabuada)
> é o EXEMPLAR nº 1 dessa fábrica.
> **FASES DO CAMINHO (estamos saindo da 1 p/ a 2):**
> 1 ✅ FUNDAÇÃO: motor data-driven (5 leis), Portão 0, BKT/ZDP, avaliação, QA, 1 exemplar no ar.
> 2 ✅→⏳ TERMINAR O EXEMPLAR Nº 1 — GRANDE PARTE ENTREGUE (2026-07-20 tarde):
>   ✅ (2) SEQUÊNCIA/aula completa: tabuada 12 → 18 → **DIVISÃO como partilha 12÷3**
>     (lei `agTodas`: TODAS as caixas recebem; kc separado `particao-igual` EF03MA08;
>     2×6 é RECUSADO na divisão; conceito "÷" nomeado por último; botão "Próxima
>     missão"; QA novo `qa-sequencia.mjs` APROVADO de ponta a ponta);
>   ✅ (4) missão de revisão Leitner (abertura "🔁" quando o kc venceu);
>   ✅ (3) tutorial integrado (dif. fácil: mentor mostra o passo a passo sozinho);
>   ✅ (5) avatar MENINA escolhível no modal (menina.png, mesmo layout) + potes em
>     LINHAS×COLUNAS na carroça (disposição retangular da BNCC);
>   ✅ (6) BIBLIOTECA-LINK: a receita vive na URL `?ativ=<base64>` — link permanente
>     que remonta a atividade em qualquer máquina; (7) barra "Prévia do professor"
>     (copiar link) só no fluxo do formulário;
>   ✅ (9) card "Vila da Tabuada" no topo do 3º ano do hub Ilhas do Saber;
>   ⏳ AINDA FALTAM: (1) voz Edge por workflow (Web Speech segue como voz),
>     (8) lista da turma p/ 1 toque (esperando os nomes do Marcos),
>     (10) os 2 cliques do console (Marcos — FIREBASE-EDUCAVERSO.md).
> (era o plano:) TERMINAR O EXEMPLAR Nº 1 (decisão do Marcos: melhor que começar tema novo) —
>   vila-tabuada vira o PADRÃO-OURO completo: (1) voz Edge por workflow nas falas;
>   (2) SEQUÊNCIA (vitória → próxima missão: tier 18, divisão como partilha);
>   (3) tutorial integrado; (4) missões de retorno Leitner; (5) menina.png escolhível +
>   potes em linhas×colunas na carroça (array BNCC); (6) BIBLIOTECA (link persistente
>   por variação — hoje a fase gerada evapora); (7) portão do professor (prévia+aprovar);
>   (8) lista da turma p/ identificação em 1 toque; (9) card no hub Ilhas do Saber;
>   (10) Marcos: 2 cliques do console (FIREBASE-EDUCAVERSO.md). Só DEPOIS vem o 2º tema.
> 3 AUTOMATIZAR: roteirista-LLM, fábrica de kits (Kenney/IA por workflow), mapa variado,
>   voz Edge por workflow → tema+ano no formulário = jogo em minutos.
> 4 PROFUNDIDADE: sequência de missões (aula 55min), missões de retorno Leitner, leis novas.
> 5 ESCALA: biblioteca da escola, hub, outros professores, validação com turmas reais.
> **Honestidade registrada:** leis NOVAS (jogabilidade inédita) sempre precisam de
> engenharia; a fábrica automatiza COMBINAR leis prontas + tema + arte + som + conteúdo.

## 🎮 FLUXO OFICIAL (decisão do Marcos 2026-07-20): JOGO PRIMEIRO, PEDAGOGIA DEPOIS
> Causa de TANTOS erros de cenário: eu improvisava a montagem do jogo. Agora há fluxo:
> **`FLUXO-MONTAR-JOGO-2D.md`** — (1) escolher 1 PACK completo/coeso/livre e usar SÓ ele
> (Ninja-full em `content/assets/ninja-adventure-full/` OU Kenney Tiny Town — NUNCA
> misturar); (2) montar o JOGO FUNCIONAL como o AUTOR manda (MAPA composto de verdade —
> tree-line/casa/caminho autotile, NÃO prop solto em grama; personagem VIVO 4 direções +
> som + animação — já funciona no motor); Portão 1 = robô joga e aprova; (3) SÓ ENTÃO a
> camada pedagógica por cima (aluno só avança de fase ao alcançar o objetivo; conceito
> por último; voz Antonio; avaliação stealth). Personagem 4-direções ANIMADO já é
> nativo (fichas 64×112, FaseGrid anima). Packs completos temos: ninja-adventure-full
> (24+ personagens animados, tilesets, monstros, FX) e kenney/tiny-town (Sample lindo).

## ⚠️ LIÇÃO PAGA — ÁRVORES do atlas Ninja NÃO servem recortadas (2026-07-20 noite)
> O Marcos mandou zoom: os "pinheiros" recortados do `mundo.png` saíam CORTADOS (topo/base)
> e com DOIS troncos — porque naquela parte do atlas a árvore é um BLOCO DE FLORESTA DENSA
> (feito pra ladrilhar, vários troncos juntos). Recortar UM sempre dá colcha cortada.
> **REGRA:** as ÚNICAS árvores limpas do pack são o **arbusto redondo** [0,160,32,32] e
> afins (props com margem transparente). Árvore de verdade = **arbusto redondo recolorido**
> (`limpa-props.py recolore()` HSV): verde-claro (fazenda), verde-mata (floresta),
> rosa (cerejeira/pomar), laranja (arvore_outono/montanha). Inteiras, sem corte, mesmo pack.
> NÃO recortar pinheiro/carvalho/cerejeira do atlas denso. Se quiser SHAPE de pinheiro de
> verdade → gerar por IA (`gerar-imagens.yml`), não recortar do atlas.
> **2 TRAVAS AUTOMÁTICAS no gerador (mapaFase):** (1) clamp na zona segura x[3..16]y[4..12]
> = nenhum prop na borda/moldura; (2) distância mínima ciente do tamanho = nenhum prop
> colado. Nenhum cenário, nem futuro, dá árvore na borda ou uma sobre a outra.

## 🔧 CORREÇÕES do Marcos (senha "lembra?", 2026-07-20 noite) — voz + sprites
> Marcos pegou 2 erros meus e mandou usar as FERRAMENTAS certas, não a mão:
> - **VOZ: eu tinha posto speechSynthesis (PROIBIDO).** Removido. Agora narração = MP3 do
>   ANTONIO (edge-tts `pt-BR-AntonioNeural`, `gerar-audio.yml modelo=male`). 14 falas fixas
>   geradas (lote via `tools/falas-adventure.mjs`, id = `vozHash` djb2 base36 = nome do MP3),
>   copiadas p/ `public/rpg/voz/<hash>.mp3`; `FaseGrid.falar()` toca o MP3 por hash da fala.
>   Falas dinâmicas seguem em texto por ora. Botão 🔊/🔇 controla.
> - **SPRITES "halo/3 árvores/sobre a casa":** (a) a "cerejeira" do atlas Ninja era tile de
>   floresta DENSA (lê como 3 árvores) → troquei pelo arbusto redondo LIMPO **recolorido
>   verde→rosa** (HSV, em `limpa-props.py`) = cerejeira em flor, 1 árvore, forma da fase 1;
>   (b) reposicionei TODO scatter em zonas livres (nada sobre casa/carroça/fazendeiro,
>   espaçamento ≥3); (c) dropei o carvalho (limpeza cortou o tronco). Pinheiros/pedras OK.
>   Honestidade: árvores realmente sob medida = gerar por IA (`gerar-imagens.yml`) se pedir.

## 🎬 AVENTURA DE 5 PARADAS + PESQUISA DE JOGO 2D (2026-07-20 noite) — "não enjoar" + 55min
> Marcos (senha "lembra?"): cada FASE tem que ser um CENÁRIO DIFERENTE do pack (não a
> mesma tela), a aula dura ~55 min e há um PROFISSIONAL que joga como criança e mede o
> tempo. Pesquisei fundo (2 relatórios: game feel/level design + aventura multifase;
> gravados em PESQUISA-JOGO-2D-E-AVENTURA-55MIN-2026-07.md) e construí:
> - **CENÁRIOS por fase** (`cenarios.ts`): 5 lugares do mesmo pack Ninja Adventure —
>   Fazenda → Floresta (pinheiros+vaga-lumes) → Rio (laguinho+pedras) → Pomar
>   (cerejeiras+pétalas) → Montanha (pedras+folhas). Props catalogados no kit
>   (pinheiro/carvalho/cerejeira/pedra_g/pedra_p/toco/agua/flor/cogumelo…). O motor só
>   troca decoração+clima; jogabilidade intacta. É a "múltipla incorporação" de Dienes.
> - **AMBIENTE VIVO** (`montaAmbiente`): vaga-lumes/pétalas/folhas/neve — partículas
>   leves em tela (scrollFactor 0), lidas da prop `ambiente` do mapa.
> - **ARCO data-driven de 5 missões** (Fabrica): 2× multiplicar (12→18) + 3× DIVIDIR
>   (rio 12÷3, pomar 18÷3, montanha 12÷4). Cada parada = cenário novo + passo REAL de
>   matemática (não pote repetido). Botão "Próxima missão" + CELEBRAÇÃO de transição
>   (estrela+fanfarra "Rumo a <lugar>") = a passagem VIRA recompensa (jornada).
> - **GAME FEEL** (Swink/Vlambeer): squash&stretch+flash no sucesso (`juice()`), câmera
>   suave deadzone+lerp (Keren), pitch variável no som. Juice premia acerto, nunca pune.
> - **BFS de ALCANÇABILIDADE** no espalhador de itens (mapaFase): nenhum pote nasce
>   preso atrás de água/pedra — bug REAL que o auditor de duração pegou no cenário do rio.
> - **⏱️ AUDITOR DE DURAÇÃO** (`qa-duracao.mjs`): "joga como criança 7-9" e MODELA o
>   tempo pelo conteúdo real (constantes de ritmo da pesquisa, honestas, à vista).
>   Resultado: **~49 min, APROVADO (≥45)**. QA `qa-sequencia.mjs` APROVADO ponta a ponta.
> - **PROPS LIMPOS (conserto do "halo de foto colada", 2026-07-20):** o Marcos viu que
>   cerejeira/pinheiro/pedra vinham com fragmento da árvore vizinha + tile de terra colado
>   (naquela parte do atlas os objetos se encostam). Ferramenta do Diretor de Arte
>   **`tools/limpa-props.py`**: recorta cada prop, floodfill dos 4 CANTOS (remove vizinho
>   e PARA no contorno preto do sprite; trava: se a região >40% é o objeto, não apaga) +
>   maior blob + autocrop → PNG individual em `public/rpg/cen/<nome>.png`. O motor carrega
>   `cen_<nome>` (não mais sub-recorte do atlas). Água do rio REMOVIDA (retângulo azul
>   chapado = pior "colado"; água com margem/autotile fica pra depois). Resultado: os 5
>   cenários montam LIMPOS como a fase 1. QA gameplay + duração APROVADOS; ambos no ar
>   (vila-tabuada 16:51, fabrica-aventuras 16:58).

## 📋 CAMADA PROVA construída (2026-07-20) — evidências + painel + parecer que vira NOTA
> Pedido do Marcos: avaliação DESCRITIVA no Firebase, "da atividade ou do que eu quiser",
> transformável em nota. Pesquisa profunda em `PESQUISA-AJUDA-E-AVALIACAO-2026-07.md`
> (help-seeking/CMU, stealth assessment/Shute, LDB art.24-V, rubricas BNCC). Construído:
> - **`evidencias.ts`:** identidade leve (nome+turma, modal "Quem vai jogar?", 1ª vez;
>   "Jogar sem registrar" existe; QA/webdriver nunca vê). Cada vitória grava EVIDÊNCIA
>   {kc, mecânica, estratégia (ex. "3×4"!), erros, nivelAjuda 0/1/2, cliques ❓, duração,
>   pKnown} → Firebase `/educaverso/vidal-ramos/evidencias/<turma>/<aluno>` via LOGIN
>   ANÔNIMO; sem rede → fila local que sobe no próximo boot; espelho local sempre.
> - **RUBRICA auditável:** sem ajuda+sem erro=Consolidado; após pergunta/❓=Em
>   desenvolvimento; precisou do gesto=Iniciando. Nota sugerida por TABELA FIXA
>   (8,5-10 / 6,0-8,4 / <6,0 — professor ajusta). O ANDAIME GRADUAL é a régua!
> - **PAINEL DO PROFESSOR (`?painel`):** login = conta da AGENDA (matrícula/senha);
>   leitura só admin (regra usa /agenda/vidal-ramos/admins). Por turma/aluno: missões,
>   nível, PARECER DESCRITIVO rascunho (cita evidências reais, editável, botão copiar).
>   Modo "só desta máquina" sem login. Ex.: vila-tabuada/?painel.
> - **⚠️ FALTAM 2 PASSOS DO MARCOS no console (sem eles = só modo local):** ativar
>   Anonymous auth + colar a regra `educaverso` — receita EXATA em `FIREBASE-EDUCAVERSO.md`.
> - **Voz nos balões** (Web Speech pt-BR, botão 🔊/🔇, padrão ligado; QA não fala) e
>   **dica por INATIVIDADE** (~25s parado → mentor se oferece; cura o help avoidance).
> - Clicar no ❓ conta como ajuda nível 1 (anti-inflação da rubrica).

## 🎓 UPGRADE PEDAGÓGICO da fase agrupar (2026-07-20, pedido do Marcos após jogar)
> O Marcos testou e apontou 2 faltas REAIS: (1) a consequência do erro era fraca
> ("balança + texto" = popup disfarçado); (2) faltava EXPLICAR a lição no final
> (institucionalização, Brousseau). Consertado no motor (FaseGrid + mapaFase):
> - **Consequência VISÍVEL:** a caixa desigual TOMBA deitada (~74°) e os potes
>   ESCORREGAM pra fora (bounce + som grave); ~2,3s depois tudo volta sozinho
>   (trabalho não se perde). `tombaCaixa()`.
> - **CARROÇA no mundo:** prop `carroca: [82,130,28,28]` do atlas Ninja Adventure
>   (kits.ts), parada ao lado do fazendeiro (tile 11,6 + colisão). Na vitória as
>   caixas aprovadas são CARREGADAS nela (`agCarrega()`) — causa e efeito completos.
> - **CONSOLIDAÇÃO (a lição é DITA):** antes de aprovar, `agConfere()` conta caixa
>   por caixa com números flutuando (4… 8… 12) e a entrega nomeia com todas as
>   letras: "grupos IGUAIS tem nome — é MULTIPLICAR: 3×4=12". Descoberta PRIMEIRO,
>   explicação DEPOIS — Portão 0 intacto.
> - **Botão ❓ de ajuda** (canto sup. dir.): reconta o problema + "como fazer AGORA"
>   por mecânica/estado (`mostraAjuda()`). Casa mobiliada (tapete/estante+potes/baú)
>   com colisão; colisão da casa cobre o sprite inteiro. Decor aceita prop `depth`.
> - QA: qa-agrupar 19/19 + qa-fgrid APROVADOS (a conferência leva ~3,4s antes de
>   `entregou` — o QA espera até 6s, folga ok). Publicado em vila-tabuada +
>   fabrica-aventuras (12:3x UTC).

## 🌙 SAGA DA PUBLICAÇÃO (madrugada 2026-07-20) — lições PAGAS de deploy
> A fase da tabuada demorou HORAS pra ir ao ar. Causas REAIS (2, sobrepostas) e curas:
> 1. **Incidente do GitHub** (~00:38–03:40 UTC): API 503 até de dentro das Actions; builds
>    legados do Pages presos em "building"/"startup_failure" (em repo NOVO). Nada nosso.
>    Diagnóstico definitivo = **`checar-pages.yml`** (na main): consulta config/último build/
>    último commit/runs do repo DESTINO + curl do site, e **COMMITA o resultado em
>    `_diag/pages-<repo>.txt`** — leitura via git, imune a API instável. USAR SEMPRE que
>    "link não abre".
> 2. **⚠️ LIÇÃO PAGA (a pior): o `PAGES_TOKEN` NÃO tem escopo `workflow`** → push que
>    contenha QUALQUER arquivo `.github/workflows/` no repo destino é **REJEITADO inteiro**
>    ("refusing to allow a PAT to create or update workflow"). Meu "plano B" (embutir
>    auto-deploy no destino) quebrou TODAS as publicações por 1h até eu ler o log certo.
>    **REGRA: publicador NUNCA inclui workflow no destino.** Pages LEGADO (source=main)
>    funciona bem; o `app-build.yml` agora também FORÇA um build (`POST pages/builds`)
>    após o push (não espera evento, que atrasa em incidente).
> 3. Repo criado na hora do incidente (`vila-tabuada`) nasceu com builds startup_failure;
>    depois da recuperação + republicação, montou normal. Repos velhos seguiram servindo.
> **Links NO AR (04:10 UTC, build success + HTTP 200):**
> - **https://vidalprof.github.io/vila-tabuada/** — LINK DIRETO do jogo da tabuada
>   (boot injetado `window.__BOOT='tabuada'`: a Fábrica gera a fase sozinha, sem formulário).
> - **https://vidalprof.github.io/educaverso-app/** — idem (repo de teste, mesmo boot).
> - **https://vidalprof.github.io/fabrica-aventuras/** — a Fábrica com a mecânica agrupar
>   (digite "Tabuada" no objetivo → GERAR). `vila-viva` intocada.

## 🌐 DECISÃO DO MARCOS (2026-07): TRABALHAMOS SÓ ONLINE — esquecer "offline"
> O Marcos deixou claro (mais de uma vez): **a escola é ONLINE, sempre há internet.**
> **"Offline" NÃO é requisito.** Eu não devo mais usar "tem que rodar offline / HTML
> único offline" como argumento ou trava — isso já atrapalhou a conversa. O que
> **CONTINUA valendo** como restrição real é: **PC fraco da escola** (AMD FX-4300,
> 3,5 GB RAM, Win7, Chrome 109 / Firefox 106) → **leve e compatível**; e **custo baixo**.
>
> **Reflexo em Unity/motores pesados:** ser online **não** libera Unity. Os bloqueios
> reais que ficam são: (1) eu **não opero o editor do Unity** (é programa de tela, com
> licença; eu sou headless/linha de comando); (2) **Unity WebGL é pesado** (RAM/download)
> pro PC fraco da escola. O Monkey Mart roda por ser **WebGL/HTML5 muito otimizado** —
> mesma família do nosso Phaser. Logo, a qualidade "espetacular" vem de **arte + animação
> + game feel**, não do motor. Caminho certo = **Phaser + kit de sprites bem-feito**.

## 📦 DECISÃO DO MARCOS (2026-07): NÃO precisa ser HTML único — repo por aventura
> Também **não é requisito** espremer tudo num HTML só. Podemos ter **1 repositório por
> aventura**, com **pastas** (código, `assets/`, `dados/`, `audio/`). Isso é justamente a
> arquitetura PROFISSIONAL que já adotamos no **`educaverso-app`** (Phaser + TypeScript +
> **Vite** + build por **GitHub Actions** → publica no repo próprio). Ou seja: relaxar o
> "HTML único" **facilita** (multi-arquivo, atlas de sprites, code-split), não atrapalha.
> **O molde premium 1-HTML continua valendo só pro modelo LEVE antigo (atividades/hub).**
> O EducaVerso novo é multi-arquivo por repo.

## 🧊 DECISÃO DO MARCOS (2026-07): EducaVerso em 3D VOXEL (estilo Minecraft), com three.js
> Depois de testar tudo, o Marcos escolheu **3D voxel (blocos, tipo Minecraft) com three.js** —
> ele **rejeitou o desenhado-por-código 2D** ("ficou amador") e quis o mundo **explorável 3D**.
> - **RODOU no PC dele: 26–29 FPS** (jogável; 30 é o alvo do gênero). O 3D voxel é **viável na escola**.
> - **Otimização obrigatória** (pro FX-4300 aguentar): face-culling + **1 mesh** (BufferGeometry) por
>   grupo estático, **luz assada nas cores** (sem shadow map, sem luz dinâmica), resolução interna baixa
>   (`RQ`), **AUTO-QUALIDADE** (mede FPS; se <24, baixa `RQ` sozinho). Ilha da parada 1 = **~4 mil tri, ~55 draws**.
> - **Sem sombra/luz DINÂMICA** (cara demais p/ o PC fraco) — sombra é uma **manchinha** no chão + AO assada.
> - **Câmera orbita** (arrastar mouse gira) + **andar relativo à câmera** (WASD). Teclado+mouse é normal no 3D.
> - **Ganho enorme:** voxel **MATA o bug de arte** (recorte/membro faltando/inconsistência não existem — é bloco).
>   Objeto novo = uns cubos coloridos no código. Cenário novo = trocar DADOS (terreno + objetos a contar + falas).
> - **Onde está:** `_voxel/index.html` (three.js em `_voxel/three.module.min.js`), publicado por Fábrica/atualizar
>   no repo **`ilha-voxel-teste`** → https://vidalprof.github.io/ilha-voxel-teste/ . Roteiro pirata:
>   "Ilha das Trinta Moedas" (5 paradas 6→12→18→24→30). **Parada 1 (cocos) JÁ jogável** (contar tocando/andando).
> - **LEGAL:** NUNCA usar marca/logo/boneco LEGO (é cópia). Voxel/cubo é genérico e legal com o NOSSO Verso.

## 🕹️ DECISÃO DO MARCOS (2026-07): motor 2D top-down PROFISSIONAL = **Phaser 3 + KIT PRONTO (sprites reais)**
> Depois de testar 3D voxel e 2D desenhado-por-código, o Marcos foi claro em vários pontos-chave:
> - **"NÃO quero NADA desenhado por código"** (as árvores/sol/nuvem que eu desenhava com graphics ficaram
>   amadoras). **TUDO tem que ser SPRITE de verdade** — como o boneco. Regra firme.
> - **Kits PRONTOS (baixados) são o melhor caminho**, iguais ao personagem, e a gente **anima** eles. O
>   **Gemini/ChatGPT NÃO montam a cartela completa** de sprites (bug de coerência + grade desalinhada):
>   servem pra **1 imagem solta** (prop/fundo único, até com recorte transparente), **não** pro kit animado.
> - **"Um game usa ~300 imagens"** = na prática **1–3 cartelas** (sprite sheet/atlas: 1 PNG com centenas de
>   quadros). Baixar a cartela pronta é muito mais fácil/seguro que gerar. O **mundo vivo** (vento, sombra,
>   sons) é **código/animação** (de graça) — isso ele aprova; o que ele rejeita é **arte desenhada por código**.
>
> **MOTOR ESCOLHIDO: Phaser 3 (CANVAS + Arcade Physics)** — 1 MB (`phaser.min.js` vendorizado, offline),
> leve pro FX-4300 (vs Godot HTML5 = 35 MB, REJEITADO). Colisão nativa, animação por sprite sheet, câmera
> que segue (explorar), y-sort (profundidade), tween (vento). Renderer CANVAS + `pixelArt:true`.
>
> **PIPELINE DE ARTE (via GitHub Actions — internet liberada, igual gerar-imagens):**
> - **Personagem animado:** kit **LPC** (Liberated Pixel Cup, CC0). Baixado em `_anim/fetch_char.py`
>   (body + torso do `sanderfrenken/Universal-LPC-...`, compostos em `_anim/assets/hero.png`, 832x1344,
>   13 colunas × 64px). Andar 4 direções: IDLE {up:104,left:117,down:130,right:143}; walk up 105-112,
>   left 118-125, down 131-138, right 144-151. **PENDÊNCIA:** herói ainda **careca** (camada de cabelo
>   falhou no download) — encaixar `hair` do kit.
> - **Mundo (chão/árvores/água):** kit **LPC Base Assets (Sharm, CC0)** — `_anim/fetch_world.py` +
>   workflow **`mundo-build.yml`** (dispara por commit com **`[world]`**), raspa a página do OpenGameArt
>   e baixa 78 PNGs pra `_anim/assets/mundo/`. Daí eu **RECORTO** (Pillow) os sprites reais pra
>   `_anim/assets/mundo/cut/`: grama sólida (grass linha 5), terra (dirt), lago pronto (bloco 3x3 do
>   tileset de água), **árvore redonda** (copa treetop cols0-2/rows0-2 **+ tronco col 1** — a col 2 é
>   vazia!), pinheiro, sombra. Recortar pixel real do tileset **NÃO** é "desenhar por código" (é como
>   todo jogo usa tileset) — isso o Marcos aceita; desenhar formas com graphics, **não**.
>
> **DEMO no ar:** repo **`personagem-anima`** → https://vidalprof.github.io/personagem-anima/ (publicado
> por `fabrica.yml`, `source_dir=_anim`, `ref` = branch de trabalho). Estado atual (2026-07): mundo com
> sprites reais (grama/árvores/lago/canteiro de terra), **colisão** no tronco (testada por medição: herói
> trava na base), y-sort (copa passa na frente da cabeça), câmera que segue, vento (sway) + sons (Web
> Audio: vento/passarinho/passos). **Aprovado pelo Marcos:** personagem, movimento, vento, passarinho.
> **PRÓXIMO:** (1) cabelo/roupa no herói; (2) camada pedagógica — plantar no canteiro **acertando contas**
> (contar até 30) + o mundo **falar o nome** da criança (banco de vozes já existe, ver seção de vozes).

## 🌱 1ª ATIVIDADE COMPLETA no motor Phaser+LPC — "A HORTA DOS NÚMEROS" (2026-07)
> Primeira atividade EduVerse fechada no motor novo (Phaser + kit CC0), passando o FLUXO
> oficial (Pedagogo→Roteirista→…→Portões). No ar: **`horta-dos-numeros`** →
> https://vidalprof.github.io/horta-dos-numeros/ (publicado por `fabrica.yml`, `source_dir=_anim`).
> - **Conteúdo:** contar até 30 (BNCC 1º ano: contagem + agrupamento de 6 em 6). Doc em
>   `_anim/PLANO-PEDAGOGICO.md`.
> - **Portão 0 (LIÇÃO PAGA):** minha 1ª versão tinha **"baú trancado que abre em 30"** —
>   isso é o **exemplo INCORRETO** da FILOSOFIA (prova disfarçada). Redesenhei: **problema do
>   mundo primeiro** (bichos com fome, horta vazia) → criança **planta e conta** → Byte
>   **pergunta padrões** (nunca dá resposta) → conceito ("de 6 em 6") **por ÚLTIMO** + reflexão
>   → recompensa = **ter AJUDADO** (horta viva + bichos comem + medalha "Amigo da Horta"),
>   **nunca** número-que-destranca. **Regra reforçada: nada de baú/porta que abre por acertar.**
> - **Personagem:** usar **personagem COMPLETO do kit** (princesa LPC, 9col×4lin walkcycle:
>   IDLE {up:0,left:9,down:18,right:27}; andar up1-8/left10-17/down19-26/right28-35) em vez de
>   compor camadas (a loteria body+torso+hair deu **rosto sumido**, ver lição abaixo).
> - **LIÇÃO PAGA (rosto sumido):** compus corpo do sheet LPC **expandido (46 lin, 832×2944)**
>   com roupa/cabelo do **clássico (21 lin, 832×1344)** → linhas não batem → cabeça no lugar
>   errado. **Regra: TODAS as camadas da MESMA versão/repo** (usei jrconway3 p/ tudo). Melhor
>   ainda: personagem completo pronto (sem compor).
> - **LIÇÃO PAGA (UI + zoom):** `Text` com `scrollFactor(0)` numa câmera com **zoom** DESALINHA
>   (texto sai fora da caixa). Solução: **cena de UI SEPARADA** (`scene:[Mundo,UI]` + **`this.scene.launch('UI')`**
>   — o array NÃO auto-inicia a 2ª cena!). A UI usa coords de tela, sem zoom. Diálogo/HUD/número/
>   medalha/confete moram na cena UI; mundo/herói/plantio na cena Mundo.
> - **LIÇÃO PAGA (emoji em Text):** emoji no MEIO de texto do Phaser bagunça a medição/quebra —
>   manter emoji só em elementos soltos (HUD/plaquinha), texto de fala sem emoji no meio.
> - **Ganchos de engajamento aplicados (1 sessão):** nome falado (Antonio, `voz-nome.js` + banco
>   124 mp3 em `_anim/audio/`), número grande + som + planta crescendo, progresso visível,
>   confete + estrela cadente, Byte que pergunta. Sem cronômetro/punição (`_plano/plano_engajamento.md`).
> - **PENDENTE:** narração falada do Byte + números na voz do Antonio (workflow `[audio]`);
>   decisão final de estilo (LPC × chibi fofo — o Marcos vai comparar); ideias grandes (turma/
>   Docinho/álbum/save) DEPOIS que ele aprovar esta.
> - **DIREITOS:** LPC = **CC-BY-SA/GPL** (exige CRÉDITO — ver `_anim/CREDITOS.md`), NÃO é CC0;
>   Ninja Adventure = CC0. (Corrigido: eu chamava tudo de "CC0" por engano.)
> - **LIÇÃO PAGA (campo de NOME + Phaser):** o Phaser dá `preventDefault` nas teclas do jogo
>   (W/A/S/D e setas) → **essas letras não digitavam** no `<input>` do nome (Ana, Sara, Davi,
>   Wesley perdiam letras). Conserto: **`this.input.keyboard.clearCaptures()` + `disableGlobalCapture()`**
>   (o jogo ainda LÊ as teclas p/ mover; só não bloqueia o DOM). Regra: em atividade com campo
>   de texto + Phaser, SEMPRE desligar a captura de teclado.
> - **LIÇÃO PAGA (CELULAR — o Marcos testa no celular!):** só WASD/setas movia → **sem teclado no
>   celular, a criança não anda** = jogo intestável no celular. Conserto: **TOQUE PRA ANDAR**
>   (tap-to-move: toca no chão → `destino` = ponto do mundo (`camera.getWorldPoint`) → herói
>   caminha até lá; toca na terra onde ELA está → planta). Teclado (PC) tem prioridade e cancela
>   o destino. **Regra de ouro: TODA atividade tem que ser jogável 100% no TOQUE** (celular/tablet
>   da escola), teclado é extra. Testar sempre em viewport de celular (`isMobile+hasTouch`).
> - **⚠️ REGRA DE OURO — NADA DE EMOJI no que a criança VÊ (Marcos, PCs antigos da escola):**
>   emoji **NÃO renderiza** em navegador/PC antigo (fica quadrado/buraco) → quebra a atividade nas
>   máquinas da escola (FX-4300, 2012). **TUDO que a criança vê = SPRITE real** (personagem, Byte,
>   animais, frutas, cesta, medalha). **Efeitos** (brilho, setinha do balão, marcador) = **forma
>   desenhada no código** (graphics: círculo/triângulo/estrela) — isso aparece em qualquer
>   navegador. **NUNCA** usar emoji como asset de jogo. (No celular do Marcos o emoji aparece e
>   engana; nos PCs da escola, não.) Kenney/LPC dão animais/frutas/itens em sprite CC0 — usar eles.
> - **BALÃO não trava o boneco:** fala é **automática** (auto-avança por tempo), a criança anda o
>   tempo todo; toque = andar (não avança fala). Frutas/animais com **sombra** (não flutuam).

## ⭐ CORREÇÃO DE RUMO DO MARCOS (2026-07-19, LER ANTES DE MEXER NA FÁBRICA)
> **1) ESTILO DO MUNDO = "o da FLORESTA", NÃO a prancha do Pomar.** O Marcos quer o mundo
> **montado de sprites espalhados** (chão de textura contínua + árvores/pedras/rio/ponte como
> peças com colisão, a criança anda ENTRE elas, top-down estilo videogame — como floresta-do-byte
> e os jogos LPC/Kenney) — a prancha-quadro do Pomar NÃO é o estilo desejado p/ exteriores.
> **Síntese profissional registrada:** exteriores = mundo composto (chao_textura + props);
> pranchas pintadas ficam PERFEITAS para INTERIORES (a cabana provou). O Pomar fica no ar como
> prova, mas o padrão da fábrica é o estilo floresta.
> **2) GRAMÁTICA DE JOGO (a pedida do Marcos, ex. da PONTE):** problema EXPOSTO no mundo (ponte
> quebrada bloqueia a passagem) → criança resolve um problema → **ganha um ITEM** (mochila) →
> **ENTREGA a um personagem** (mestre Castor) → **o MUNDO MUDA** (ponte consertada, colisão sai)
> → passa adiante (nova área). Aluno protagonista; aprende sem perceber. Isso virou o contrato
> `quer_item/ao_receber/muda_objeto/remove_bloqueio` no motor.
> **3) FLUXO DE PRODUÇÃO OFICIAL (como o Marcos pede um mundo):** ele passa **TEMA + ANO** →
> PEDAGOGO (currículo BNCC/Blumenau) define o objetivo da AULA DE 55 MIN → com o ROTEIRISTA
> monta história+dinâmica → Game Designer mapeia nas mecânicas do motor → gera-se o mundo +
> imagens conforme o desenho deles → AUDITORIA (robô-QA + portões + arte) → entrega ao Marcos.
> Só criar atividade curricular DEPOIS da máquina pronta (ordem dele).
> **4) SE A SESSÃO CAIR/CRÉDITOS ACABAREM:** tudo está commitado na branch
> claude/github-pages-deploy-wbb7dy. Estado atual: kit floresta + falas da ponte GERANDO por
> workflow (commit "gera kit floresta [imagens] [audio]"); motor ganhando chao_textura/rio/
> bloqueios/mochila/entrega. Próximo passo se retomar: `git pull`, integrar kit em
> educaverso-app/public, montar aventuras/floresta.ts com a ponte, rodar tools/qa-mundo.mjs,
> publicar via fabrica.yml (repo mundo-floresta).

## 🌲 ENTREGA: "A FLORESTA DO BYTE" — o estilo CERTO + gramática da PONTE (2026-07-19)
> **Link: https://vidalprof.github.io/mundo-floresta/** (repo `mundo-floresta`, fabrica.yml
> `source_dir=educaverso-app/dist`; padrão do app — `?pomar` abre o mundo prancha antigo).
> **Estilo floresta entregue** (o que o Marcos pediu): chão de grama contínua (torus-blend
> anti-emenda) + árvores/pinheiros/pedras COM COLISÃO que a criança anda entre, rio animado,
> câmera explorando mundo 2080×1440. **Gramática provada de ponta a ponta pelo robô-QA**
> (`tools/qa-floresta.mjs` == APROVADO ==): problema exposto (PONTE QUEBRADA) → resolve
> (3 tábuas, contagem kn narrada) → ITEM na MOCHILA (HUD, persistido) → ENTREGA ao mestre
> CASTOR → **o mundo MUDA** (ponte troca de textura, bloqueio do rio sai) → atravessa →
> CLAREIRA SECRETA (festa) → tudo salvo (o mundo lembra). Contrato: `quer_item/ao_receber/
> muda_objeto/remove_bloqueio/bloqueios/chao_textura/agua/recompensa_item` em aventura.ts.
> **Kit floresta premium** (12 assets Gemini, cápsula coesa) + 8 falas Antonio (f_*) + de-white
> nas bases. **Polimentos registrados:** emendas da grama ainda levemente visíveis (melhorar
> textura), pontas brancas da ponte, poses costas/passo do Byte, castor só 1 pose.
> **PRÓXIMO PASSO OFICIAL (ordem do Marcos):** a máquina está pronta — agora o fluxo
> TEMA+ANO → Pedagogo → Roteirista → aula 55min → gerar mundo/arte → auditoria → entrega.

## 🏭 ENTREGA: FÁBRICA DE MUNDOS v1 + "O POMAR DO BYTE" (2026-07-19)
> **O MUNDO EXPLORÁVEL saiu** — no motor oficial (educaverso-app, Phaser+TS strict) e pelos portões.
> **Link: https://vidalprof.github.io/mundo-pomar/** (repo `mundo-pomar`; publica via `fabrica.yml`
> com `source_dir=educaverso-app/dist`; rebuild = `npm run build` + QA + fabrica de novo).
> - **Motor v2 (`src/motor/Mundo.ts`)**: grafo de ZONAS (prancha pintada 1440² > tela, câmera explora),
>   PORTAIS com fade (interior de cabana!), **MISSÃO DENTRO DO MUNDO** (colher SEM enunciado numérico;
>   contagem narrada kn1..N; conceito por último), vida ambiente (sol/pólen/lareira/música CC-BY 62s
>   cortada por frames), **memória** (localStorage: o mundo lembra), tap-to-move com solta-quina,
>   balão responsivo. Contrato v2 em `aventura.ts` (Zod; grafo validado). Auditor v2 por zona.
> - **1º mundo `src/aventuras/pomar.ts`** (BNCC EF01MA01/02): Pomar (coelho + colher 5 maçãs → cesta
>   ENCHE e fica) → Colina (casa) → **Cabana interior** (lareira acesa) → Lago (barquinho flutuando).
>   Arte premium Gemini coesa (z_pomar/z_colina/z_cabana/z_lago + barco recortado).
> - **Robô-QA oficial `tools/qa-mundo.mjs`** (Playwright real): boot + missão completa + grafo inteiro
>   + zero console errors → **== APROVADO ==**. Bugs pegos pelo robô e consertados: cesta sem preload,
>   auditor cruzando zonas, spawn checado contra zona errada, texto do balão estourando (setResolution),
>   404 de poses (→ **manifest.json de poses** no Personagem), favicon.
> - **AUDITORIA 10 agentes (fable-5) SUSTENTOU o plano** (ideia 8/10; notas 5-7 nas execuções, tudo
>   com conserto mapeado). Incorporado: mundo>tela, missão sem "traga N", construir NO motor TS (não
>   3º fork), emojis visíveis removidos, TS strict ligado (0 erros), tap-solta-quina. **Pendências
>   priorizadas da auditoria:** poses costas/passo do Byte (cartela completa), posse/canto da criança,
>   ritual de retorno semanal, cantos-brinquedo, colisores invisíveis p/ árvores da prancha, gate de
>   toque mobile no CI, teste no PC REAL da escola e com CRIANÇAS (férias → na volta às aulas).
> - **Músicas**: `musica-cc0.yml` baixou Kevin MacLeod (CC-BY, créditos em `_mundos/musica/`).

## 🎬 ESTÚDIO EDUVERSE — plano do "2D incrível" + DECISÃO do motor (2026-07)
> Plano completo escrito em **`ESTUDIO-EDUVERSE.md`** (montado após 4 subagentes lerem TODA a base
> documental). Ideia = mundo 2D vivo/persistente/explorável (não quiz); "2D incrível" vem de **4
> níveis**: (1) arte pintada premium ✅, (2) vida do personagem (respira/pisca/anda/**fala com a
> boca**/comemora), (3) mundo vivo (luz/vento/partículas/dia-noite/som), (4) suculência + **contagem
> que ACENDE** com a voz. Hoje só temos o nível 1.
> - **⭐ DECISÃO #1 DO MARCOS (jul/2026): motor único do mundo vivo = PHASER 3 + TypeScript + Vite**
>   (estúdio `educaverso-app/`, WebGL, roda ~59fps no Chrome 109 da escola). O **cérebro da fábrica**
>   (contrato `dados.json`, biblioteca LEGO, catálogo de mecânicas, robô-auditor, os 5 mundos como
>   CONTEÚDO) é agnóstico de motor → **transportar** pro Phaser. O motor ES5 `eduverse/kit-floresta.py`
>   **se aposenta** p/ mundo-vivo novo (vira referência). Molde premium single-HTML "Circo do Teo" segue
>   só p/ atividades **estruturadas/não-exploráveis**.
> - **Stack selecionado:** Phaser+TS (motor) · Gemini+Pollinations (arte) · edge-tts Antonio (voz) ·
>   `dados.json` validado por schema (cenas) · biblioteca LEGO + props vivos data-driven · Firebase
>   (save/avaliação invisível) · GitHub Actions (fábrica) · robô-auditor + 4 portões. Tudo grátis (Gemini
>   centavos com cache por hash).
> - **Roadmap:** Fase 0 decisão ✅ → Fase 1 fundação (motor genérico + schema + biblioteca + pipeline +
>   auditor + save) → **Fase 2 a "camada incrível"** (poses+lip-sync+piscar+emoções + módulo mundo-vivo +
>   contagem-acesa → 1 cena de referência) → Fase 3 1ª atividade testada com crianças → Fase 4 escala
>   (jornada 55min, Computação "programe o robô", avaliação→documentos).
> - **⭐ DECISÃO DO MARCOS (jul/2026): estúdio 100% GRÁTIS** (avaliou upgrades pagos — ElevenLabs/LoRA/
>   Suno/packs — e escolheu ficar no gratuito). Substitutos oficiais: **voz** = elenco edge-tts multi-voz
>   pt-BR (Antonio/Francisca/Thalita) + direção de atuação por prosódia (rate/pitch/volume por fala) +
>   pitch-shift ffmpeg p/ bichos/robô; **estilo** = cápsula de estilo fixa + edição por âncora (Gemini
>   centavos = "~de graça" pelo modelo híbrido já aprovado; zero absoluto = Pollinations c/ ressalva de
>   nitidez); **música** = bibliotecas CC0 (Kenney Audio/FreePD/OpenGameArt/Pixabay) baixadas por
>   workflow, loop curado por mundo, ffmpeg — TRILHA MUSICAL entra já na fatia vertical; **packs pagos**
>   = dispensados (nossa arte IA é mais coerente). Alvo do produto reafirmado: **MUNDO EXPLORÁVEL**
>   (floresta/cabana/barco era só exemplo; tema livre — 1º mundo = POMAR por máximo reuso). Se um dia
>   pagar ElevenLabs: trocar voz = só regenerar MP3s (mesmos ids, zero retrabalho de código).

## 🧭 FORMATO NOVO — APP-TRILHA "A VILA QUE ACORDA" (Duolingo-com-alma, pré→9º, 2026-07)
> Pasta `_trilha/` → publicada em **https://vidalprof.github.io/vila-que-acorda/** (via `fabrica.yml`/
> `atualizar.yml`, `source_dir=_trilha`). Pedido do Marcos: um **app moderno tipo Duolingo** (trilha de
> paradas, mascote, salvar progresso) mas **anti-prova** — a criança **FAZ**, não responde. O **casco**
> serve do pré ao 9º; muda só o conteúdo/dificuldade de cada parada.
> - **Trilha** = mapa de paradas (nó atual pulsa, próximos com cadeado) subindo até a **vila**; cada
>   parada concluída **acende uma casinha** (o mundo floresce) + abre a próxima. Salva em localStorage.
> - **Parada "A horta pede"** (juntar/somar): toca na macieira → maçã cai na cesta (conta com a voz do
>   Antonio + número grandão) → **JUNTAR** as duas cestas → conta o total → coelho comemora → "juntar
>   é somar" (conceito por ÚLTIMO). Erro não pune. Ganchos: chegada/uau, emoção, agência, feedback na
>   hora, pico-fim, posse.
> - **⚠️ LIÇÃO PAGA CARA (visual amador) — o Marcos reprovou na hora:** a 1ª versão usei **arte
>   desenhada por CÓDIGO (SVG/vetor)** pra mostrar o formato rápido → ele achou **fraco/amador** ("perto
>   do que vínhamos fazendo"). **NUNCA fazer isso pro que a criança vê.** A regra (style-bible) é: arte
>   **PINTADA PREMIUM por IA**. Consertado: gerei tudo no **Gemini** (`_gerar_imagens.json` + commit
>   `[imagens]` → `finalizar.yml`) — Byte, cenário-trilha, cenário-pomar, maçã, cesta, coelho, casinha —
>   com **1 brief coeso de Diretor de Arte** (mesmo estilo/luz), recortei com transparência limpa
>   (`_ferramentas/cortar_sprites.py`-style: flood-fill de borda + anti-franja 2px + autocrop) e
>   recompus o app com **SVG `<image>` + `preserveAspectRatio="slice"`** (enche a tela no celular E no
>   PC; props ficam colados no fundo pintado). **Bug SVG que mordeu:** animação CSS (`transform`) ANULA
>   o atributo `transform` do mesmo elemento → animar num `<g>` INTERNO sem transform-attr (ou usar
>   `<image>`, cujo x/y não conflita com a CSS transform).

## 🪙 2ª ATIVIDADE COMPLETA (Kenney) — "O TESOURO DOS DOIS MONTES" (juntar/somar, 2026-07)
> Pasta `_kenney/` → publicada em **https://vidalprof.github.io/kenney-vivo/** (via `fabrica.yml`,
> `source_dir=_kenney`). Mesma mecânica pedagógica da Horta (JUNTAR duas quantidades = SOMAR),
> mas com o **kit Kenney (CC0, ZERO atribuição)** e **narração de voz completa**.
> - **Herói** (ruivo, Kenney roguelike 0,9) + **guia Tomás** (aldeão 0,7 — NÃO cavaleiro; o Marcos
>   flagrou que o guia "coruja" parecia cavaleiro). Ambos ganham **vida por código** (respira/pula/
>   squash/sombra) — motor de vida universal, personagem de imagem única.
> - **GUIA FICA PARADO (decisão do Marcos):** o Tomás **não segue** a criança — fica num ponto fixo
>   (`_gx0/_gy0`), respira no lugar e **vira o rosto** na direção dela. Motivo: como TUDO é narrado
>   por VOZ, o balão não precisa acompanhar; seguir ficava estranho (ele não tem colisão → "flutuava"
>   por cima das árvores). Regra geral: **guia que fala = NPC parado**, a menos que o Marcos peça seguir.
> - **COLISÃO (lição paga):** colisor tem que cobrir o **volume visível** (tronco + parte da copa,
>   ~52/42×42), não só o tronco (22×14) — senão a criança "atravessa" a copa e parece SEM colisão.
>   E **itens nascem LONGE do herói** (cantos opostos, ~370-420px) pra a criança EXPLORAR.
> - **Itens = barrinhas ÚNICAS de ouro/prata** (recortadas 1-a-1 do sheet de pilha do Kenney;
>   o Marcos: "não são moedas, são barras de ouro" + "separe pra ser barrinha única" → item CONTÁVEL).
> - **⭐ NARRAÇÃO POR VOZ (Antonio/edge-tts) — pedido do Marcos "tudo narrado, inclusive o contar":**
>   - Helper **`Voz`** no `game.js` (HTML5 `Audio`, mp3 em `_kenney/audio/`): `um/cadeia/stop`.
>     Degrada gracioso (se o mp3 falha, `onerror`→segue; nunca trava).
>   - Falas geradas em lote pelo **`gerar-audio.yml` (modelo=male → `pt-BR-AntonioNeural`)** via
>     `_lote_falas.json`; ids: `kn1..kn20` (contagem), `k_abre1/k_abre2` (saudação em 2 p/ balão
>     pequeno), `k_pede0..3`, `k_soma0..3`, `k_mais`, `k_venceu`, `k_licao`, `k_pergunta`.
>   - **Balão sincronizado com a voz:** `dialogo(pgs,onDone,audios)` — a **voz manda no ritmo**
>     (avança quando a narração acaba), com **fallback** longo caso a criança corte a voz (já foi
>     juntando). Token de página (`_pgTok`) invalida callback velho — sem avanço duplo.
>   - **Contar APARECENDO o número:** a cada barra pega, toca `kn<n>` (Antonio fala "um","dois"...)
>     junto com o `numerao` (número grandão). Saudação personalizada pelo **nome** (banco de 124).
> - **Rodadas fixas** `[[3,2],[5,4],[7,6],[9,8]]` (por isso deu p/ gravar as falas exatas por rodada).

## 🔎 DISCIPLINA DE QA (o Marcos cobrou: "essas coisas não podem acontecer")
> Eu estava **usando o Marcos como QA** (mostrava tosco, ele achava o defeito). ERRADO — custa o tempo dele.
> **Antes de mostrar QUALQUER coisa visual, EU renderizo (headless + Playwright) e AUDITO** contra a lista:
> **(1) PROPORÇÃO** (personagem × cenário × objetos — o Verso é pequeno perto das árvores; papagaio ~1/3 do Verso);
> **(2) RECONHECÍVEL** (cada coisa parece o que é — coco redondo, não quadrado); **(3) nada FLUTUANDO** sem explicação;
> **(4) INTERAÇÃO** (o que é clicável é fácil de clicar/alcançar); **(5) CÂMERA** ok; **(6) FPS/leveza**.
> Bug de imagem (recorte/membro) **não é isso** — isso é **design/gosto**, e **nenhum motor decide** (nem Unity):
> é trabalho do DESIGNER (eu) + esta checklist. Cada tropeço novo → vira item da lista. **Só mostro o que passou no meu crivo.**

## ✅ O que EU consigo fazer (capacidades REAIS — não esquecer)
- **Criar e editar** as atividades (HTML/JS/CSS), cada uma em 1 arquivo único.
- **Publicar no ar:** commit/push + ligar o GitHub Pages (Fábrica de Sites).
- **GERAR IMAGENS** acionando o workflow **`gerar-imagens.yml`**:
  - `modelo=pollinations` (GRÁTIS) ou `modelo=gemini` (usa o secret `GEMINI_API_KEY`).
  - Pode EDITAR uma imagem base (input `base`) — mantém o personagem, muda o pedido.
  - Salva em `_novo/<nome>.png` e commita sozinho; eu depois dou `git pull`.
- **GERAR ÁUDIO / narração** com voz natural (workflow **`gerar-audio.yml`**,
  edge-tts — vozes Ricardo/Camila/Antônio... — + `otimizar-audio.yml`). Salva em `_audio/`.
- **Recortar imagens** (fundo transparente, sem franja) localmente com Python/Pillow.
- **Rodar equipes de especialistas** (workflows de pesquisa/redação).
- **Criar repositórios novos** e **atualizar outros repos** (workflows da Fábrica).

> ⚠️ A geração NÃO roda no chat (a rede do chat é travada — testar API direto
> dá **403, e isso é NORMAL**, não é "quebrado"). Ela roda no **WORKFLOW do
> GitHub**, que EU aciono (`actions_run_trigger`). **"O Claude gera" = o Claude
> ACIONA o workflow que gera**, e depois traz o resultado com `git pull`.

## 🔑 Secrets já configurados (no GitHub, nunca no código)
`PAGES_TOKEN` (criar/publicar repos) · `GEMINI_API_KEY` (imagem Gemini) ·
Firebase e Pollinations conforme o uso. O valor do secret nunca aparece no
código — só é usado dentro do workflow.

## 📦 O que já construímos
- **Atividades / hub "Ilhas do Saber":** Floresta dos Números, Vila do Miau,
  Desafio da Copa, Poli e o Tesouro do Mar, a confeitaria (Mundo Vivo), etc.
- **Manuais:** `MANUAL-MESTRE.md` (o principal), `ATIVIDADE-PREMIUM.md`,
  `MUNDO-VIVO-*.md`, `FABRICA-DE-MUNDOS.md`, `PLANO-FORA-DA-CAIXA.md`, os 5
  pareceres em `_plano/`.
- **Byte** (mascote robô) gerado em `_novo/byte.png`.
- **✅ DECISÃO FIRME DO MARCOS (não reabrir):** o motor é o **2D em TILE + pintura IA
  premium** (linhagem `eduverse/kit-floresta.py` — "A Floresta do Byte"), **NÃO** o motor
  antigo da confeitaria (`_pub_confeitaria/mundo/index.html`, que é **PESADO: 3 MB**).
  **Por quê:** o tile é **mais fácil de criar, mais rápido, mais leve e mais sustentável**
  (mundo novo = DADOS + peças reusadas, não um motor de 3 MB do zero) — e mantém o **mesmo
  visual lindo** (a arte é pintada por IA). **A FÁBRICA CLONA O MOTOR DE TILE**, não o da
  confeitaria. O "injetor" do tile **já existe** = `eduverse/builders/montar.py`
  (`dados.json` → `index.html`). **REGRA:** nunca reconstruir/clonar o motor pesado; se eu
  cismar de codar mundo na mão ou clonar a confeitaria, PARAR — a decisão é o tile leve.
- **Byte VESTE o tema:** cada atividade tem o Byte fantasiado do tema (pirata, viking…),
  gerado **editando a imagem-âncora** `byte.png` (mesmo personagem, só a fantasia) via
  `gerar-imagens.yml` (`modelo=gemini`, `base=eduverse/biblioteca/proc/byte.png`). O `byte_pirata`
  gerado (chapéu tricórnio + caveira + casaco vermelho, **rosto/tela idênticos**) PROVOU que
  qualquer tema funciona. A cartela de poses da fantasia entra sozinha no injetor
  (`assets.byte:"byte_pirata"` → puxa `byte_pirata_costas`, `_lado`, etc.). Falta gerar as 6 poses.
- **✅ MUNDO-VIVO v2 (jul/2026) — efeitos ricos JÁ no motor (equipe → integração auditada):**
  a equipe de especialistas (6 agentes por workflow + revisão do engenheiro-chefe) projetou
  e eu integrei no `kit-floresta.py`, tudo **data-driven e default-seguro** (mundo sem o campo
  fica igual): 🗨️ **balões RPG** (placa de nome + typewriter + ▼ + avança no toque, acima de
  QUEM fala — Byte ou NPC), 🌓 **sombra direcional** (sol/lua), 💨 **poeira ao andar** + lib de
  micro-movimento (`breathe/sway/blink`), ☁️ **nuvens** (chão+céu), 🌧️ **clima** (`MUNDO.clima`
  = chuva/neve/tempestade com trovão por Web Audio + vento visível), 🐾 **NPCs vivos**
  (`MUNDO.npcs`: patrulham rota, interagem com o Byte, acenam, abrem balão). **Checklist completo
  em `eduverse/style-bible/ambiente-vivo.md`.** Como os efeitos moram no MOTOR, TODO mundo que a
  fábrica gerar já nasce com eles — é o oposto de fazer na mão em cada atividade.
  **Nota de QA:** no screenshot headless (virtual-time) o rAF quase não acumula tempo → efeitos
  temporais (balão/typewriter) exigem um **driver `setInterval`** na foto; no navegador real (60fps)
  roda normal. Ainda pendentes (ver checklist): porta que range, tábuas, água (ondas/peixes),
  sons de animais CC0 (precisa `baixar-sons.yml`).

## 🏭 FÁBRICA DE ATIVIDADES por currículo (pedido do Marcos — incorporar no EducaVerso)
Gerar atividades AUTOMATICAMENTE, alinhadas ao currículo escolhido, e inserir no mundo.
- **Fontes de currículo:** BNCC geral, **Computação BNCC** (já há `ATIVIDADE-COMPUTACAO.md`),
  ou o **currículo de Blumenau** (já há `.github/workflows/baixar-curriculo.yml` que baixa o
  PDF e extrai o texto para ancorar a IA). O professor escolhe fonte + ano/turma + habilidade.
- **Como monta:** a IA LÊ o objetivo real do currículo (ancorada no texto — não inventa a
  habilidade) → escolhe a MECÂNICA (do catálogo de interatividades) → cria conteúdo/desafios →
  embrulha na narrativa do mundo (um personagem/lugar) → gera a arte (pipeline de imagem) e a voz.
- **Aprovação do professor** (as 3 aprovações: missões/pedagogia, arte, jogável) — a pedagogia
  passa pelo olho dele. "Automático" com portão de qualidade (a IA rascunha, o professor confirma).
- **Inserção no mundo:** a atividade vira ponto/NPC/gatilho no mundo; o resultado alimenta a
  avaliação descritiva. Fábrica de MUNDOS (o cenário) + Fábrica de ATIVIDADES (o aprendizado) =
  sistema de produção completo do EducaVerso.
- **Adequação à TURMA (faixa etária) é obrigatória:** a partir de DISCIPLINA + TEMA + TURMA, a
  Fábrica cria cenário, personagens, dificuldade, mecânica, narração e missões ADEQUADOS à faixa.
  Bandas: **pré/1º-2º (NÃO leitores → só ícone+voz+cor, missões curtas de 1 passo, muita
  recompensa)**; **3º-5º (leitura simples, missões de poucos passos)**; **6º-9º (missões
  multi-etapas, mais autonomia)**. A IA rascunha adequado à faixa; o professor confirma.
- **MISSÕES são o formato "legal de aprender":** cada aprendizado vira uma MISSÃO no mundo
  (um objetivo de história: ajudar X, recuperar Y, construir Z) e o conteúdo é o CAMINHO para
  cumprir. Curtas e concretas para os pequenos; quests de várias etapas para os maiores.
- **ALUNO ATIVO/PROTAGONISTA (inegociável):** a criança CONSTRÓI, interage e participa — nunca
  só assiste/escolhe alternativa. Ela monta a máquina, programa o robô, constrói a ponte, cria a
  solução. A construção SÓ funciona se o conceito estiver certo → construir = provar que entendeu.
- **AS FASES DEVEM ENTREGAR O OBJETIVO DO CURRÍCULO (gating + medição):** cada fase é desenhada a
  partir de um objetivo do currículo que o professor inseriu; completar a missão EXIGE demonstrar
  aquele objetivo (a construção "trava" até estar correta). A avaliação invisível MEDE quem
  alcançou o objetivo e quem precisa de apoio → relatório descritivo para o professor agir.
- Estado: groundwork existe (baixar-curriculo.yml, ATIVIDADE-COMPUTACAO.md, catálogo de
  interatividades); FALTA o montador que casa currículo→mecânica→mundo→faixa de forma semiautomática.

## 🎒 CAMADA DO ESTUDANTE + AVALIAÇÃO DESCRITIVA (pedido do Marcos, jul/2026) — "tudo que nossa ideia tinha"
O mundo tem que ser DO ALUNO e acompanhá-lo o ano inteiro. Requisitos (INEGOCIÁVEIS):
- **Tela inicial MARAVILHOSA — MODELO do Minecraft (NÃO o tema):** estrutura tipo "seus mundos"
  do Minecraft (você vê o SEU mundo salvo, entra e continua de onde parou, ou cria/entra), porém
  no NOSSO estilo **pintado por IA premium, MUITO mais bonito** (nada de visual de blocos). O
  estudante digita **NOME + TURMA** (e dados) → as informações dele são **puxadas** (histórico,
  progresso, personagem) → o mundo vira DELE (card do "mundo do aluno" com nome/turma/progresso).
  - **MARCA "EducaVerso":** a tela é BRANDED EducaVerso — **logo/título lindo e identidade visual
    própria** (nome + tema + a "cara" do EducaVerso), personalizada. É a porta de entrada com
    personalidade, não genérica. O roteirista + especialista em temática ajudam a definir essa identidade.
- **Interação pelo NOME:** o jogo/Byte/NPCs chamam o aluno pelo nome (voz + balão).
- **Progresso SALVO:** cada missão/atividade concluída fica registrada (retoma de onde parou).
- **AVALIAÇÃO DESCRITIVA contínua:** o sistema descreve o que o aluno demonstrou (por habilidade
  do currículo), acumulando por **mês / semestre / ano**. Alimentada pelo gating pedagógico
  (completar a missão = provou a habilidade → vira frase descritiva).
- **Opção de virar NOTA:** se o professor quiser, a avaliação descritiva converte em nota.
- **Painel do PROFESSOR:** ele vê a turma, o progresso e a avaliação de cada aluno (relatório).
- **DESAFIO TÉCNICO (honesto):** salvar progresso + o professor ver central = precisa de BACKEND
  (não só localStorage, que é por-aparelho/por-navegador e o professor não enxerga). Candidato
  natural: **Firebase** (Firestore + Auth) — há indício de Firebase nos secrets (`GEMINI_API_KEY`
  "Firebase/Pollinations conforme uso"); free tier, funciona a partir do Pages estático. Alternativas:
  Google Sheet/Apps Script. **A EQUIPE precisa desenhar esta camada** (persistência + modelo de dados
  do aluno + tela inicial + agregação da avaliação + conversão em nota + painel do professor).
- **Adequação por TURMA/idade** vale aqui também: tema, mecânica, FALAS, missão e voz mudam por faixa
  (pré/1-2 não-leitores → só ícone+voz+cor; 3-5 leitura simples; 6-9 multi-etapas). `dialogo.cps`
  (velocidade do balão) mais lento pros pequenos.
- **Régua de qualidade (Marcos):** 2D tile + **arte pintada por IA premium** = qualidade "quase real"
  que **prende o estudante** — é o diferencial que chama a atenção. Não baixar essa régua.

## 🗓️ SESSÃO jul/2026 — decisões e pedidos novos ("documentar tudo p/ nada se perder" — Marcos)
- **Mundo-vivo v2 no motor (FEITO, auditado):** balões RPG (nome+typewriter+▼+toque, acima de quem
  fala), sombra direcional, poeira ao andar, nuvens, clima (chuva/neve/tempestade+trovão), NPCs vivos.
  Ver `eduverse/style-bible/ambiente-vivo.md`.
- **Balões — DECISÃO FINAL do Marcos (jul/2026):** ele NÃO gostou do balão de fundo PRETO/escuro
  atual (`balaoDes` em `kit-floresta.py`) e pediu **CAIXA DE RPG CLÁSSICO** (estilo Zelda/Pokémon
  16-bit): retangular, **FIXA na parte de baixo da tela** (não segue o personagem/não flutua acima
  da cabeça), **fundo claro sólido** (branco/bege, NUNCA preto/transparente escuro), **borda grossa
  dupla** no estilo pixel-art. Substitui a caixa escura por essa; manter typewriter+▼+nome na placa
  (já existentes) só trocando a paleta/formato/posição. Aplicar em TODO mundo (é o motor, não por
  atividade). (Havia 2 opções candidatas — branco-quadrinho-arredondado × caixa-RPG-clara-fixa-embaixo
  — ele escolheu a 2ª.)
- **EQUIPE AMPLIADA** (rodar como agentes por workflow): além dos 6 (eng. software, eng. jogos,
  pedagogo, IA/prompts, produção/ops, produto), CONTRATAR: **Roteirista de histórias** · **Especialista
  em temática** (temas das fases por faixa) · **Especialista em PROMPT do GEMINI** — foco: **gastar o
  MÍNIMO possível sendo PRECISO** (Gemini é pago; economizar tokens/chamadas + precisão ao editar a
  imagem-âncora do Byte). Fazer um "playbook" de prompts econômicos p/ imagem.
- **Tela inicial = branded EducaVerso** (logo/identidade própria), MODELO "seus mundos" do Minecraft
  (continuar o mundo salvo) — **NÃO pode ser CÓPIA do Minecraft** (nada de blocos; visual pintado
  premium PRÓPRIO). Concept visual publicado (conceito, com efeitos + musiquinha Web Audio):
  https://claude.ai/code/artifact/ac466f52-adb6-4a9a-b21f-4be67b2197b7
- **3 PILARES inegociáveis (Marcos):** (1) 2D tile + **arte IA premium** = qualidade "quase real" que
  **prende o aluno**; (2) **adequação TOTAL por turma/idade** (tema, mecânica, falas, missão, voz);
  (3) **rápido, funcional, sustentável e vivo** (experiência maravilhosa, leve p/ escola).
- **DIREÇÃO DE ARTE na linha (lição paga — pedido do Marcos "não deveria ficar corrigindo se temos os
  profissionais"):** as correções da 1ª aula (fogueira sem contexto, fruta feia/grande, "quadrado")
  vieram do **Montador manual SEM Diretor de Arte**, não dos especialistas (o roteiro/pedagogia passou
  no Portão 0 de primeira). CONSERTO: **Diretor de Arte + Portão de Arte** entram na equipe/linha. Regras
  cravadas: (1) **PROPORÇÃO coerente com o Byte** (~64px) — a maçã (e objetos) tem que ser CLARAMENTE
  menor que o Byte; alvo fácil p/ 6 anos via **brilho + raio de toque invisível**, não aumentando o
  objeto; (2) **PROPS/objetos só com CONTEXTO** (maçãs PENDURADAS nas árvores + algumas caídas, não
  flutuando; fogueira só como cena de NOITE c/ aldeões); (3) **tudo pintado por IA**, nada geométrico
  code-drawn à mostra; (4) coerência com o style-bible. O mundo tem que chegar DIRIGIDO (o Marcos não
  corrige arte). E o **Montador automático** (conteudo.json→dados.json) ainda é a-fazer (hoje manual).
- **O ROTEIRO DIRIGE A CENA (modelo-mestre da fábrica — pedido do Marcos):** a história do
  **roteirista** NÃO é só as missões — é um **roteiro de cena por cena (breakdown)** que já ESPECIFICA
  o que cada cena precisa: **cenário, hora do dia, clima, quais PERSONAGENS estão presentes, quais
  EFEITOS, quais PROPS (e o porquê/contexto de cada um), a PROPORÇÃO dos objetos vs o Byte, e a ação
  da criança.** A fábrica trabalha A PARTIR desse roteiro: o **Diretor de Arte** realiza o visual, o
  **Engenheiro** liga os efeitos/mecânicas que a cena pede, e um **Portão de Coerência** verifica
  ("faz sentido? falta algo nesta cena? está coerente com a história?"). Isso faz a fábrica PENSAR em
  tudo (proporção, contexto, efeitos, personagens) de forma organizada, saindo da história — em vez de
  remendo depois. ➜ **AÇÃO:** expandir o schema do roteirista p/ incluir o breakdown de cena; e o
  Portão de Coerência entra na linha. (Foi a lição da 1ª aula: a arte/contexto tem que vir do roteiro.)
- **VOZ (decisão firme do Marcos — corrige o estudo da equipe):** NADA de voz do navegador
  (speechSynthesis). A narração é **SEMPRE gerada via API (edge-tts — Antonio/Francisca…) e volta como
  MP3 embutido** (base64). Voz natural, padrão premium. Peso: `otimizar-audio.yml` + cache por hash.
  Voz própria por personagem. (O `EDUCAVERSO-PLANO-FABRICA.md` supõe voz runtime p/ economia — ISTO
  sobrepõe: sempre gerada, ainda grátis via edge-tts.) Ver `EDUCAVERSO-SUSTENTABILIDADE.md`.
- **SUSTENTABILIDADE (produção + dados) documentada:** `EDUCAVERSO-SUSTENTABILIDADE.md` — produção
  ~grátis (Pollinations + edge-tts + Actions público + Pages; Gemini só na fantasia do Byte, cacheado);
  dados mínimos (~2 KB/aluno + rollup anual + só 1º nome) no Firebase free, com **backend PLUGÁVEL**
  (interface `salvar/carregar` — trocável sem mexer no jogo).
- **ARQUITETURA DA FÁBRICA (estudo da equipe):** ver **`EDUCAVERSO-PLANO-FABRICA.md`** — recomendação
  **HÍBRIDA**: uma ESPINHA (linha em fases: briefing→mecânica→roteiro→arte→voz→montador→auditor→3
  portões→publicação) + FÁBRICAS-SIDECAR (os workflows do GitHub, como funções puras cacheadas por
  hash) + CATÁLOGO DE MECÂNICAS como BIBLIOTECA fixa (não gerador). Contratos = JSON versionados no git
  (briefing→receita→conteudo→dados→index). MVP = rodar a pipeline INTEIRA com a mecânica atual.
- **UX da tela inicial — COMPUTADOR COMPARTILHADO (pedido/problema do Marcos):** muitas turmas, VÁRIOS
  alunos usam o MESMO PC no dia (troca de aula rápida), turmas têm seções **A, B, C…**. Desafio: pôr isso
  sem poluir. **Recomendação (proposta):** DIVULGAÇÃO PROGRESSIVA em 3 toques, 1 tela limpa por vez —
  (1) escolher o ANO; (2) aparece a letra da seção (A/B/C…); (3) **grade de NOMES da turma** (nome +
  mini-avatar/mascote) → o aluno **TOCA no próprio nome** (SEM digitar — ideal p/ não-leitores e p/
  troca rápida). Fallback "não achei meu nome → digitar". O PC **lembra a última turma** (a próxima
  criança da mesma turma já cai na grade de nomes). Só se vê UMA turma por vez → nunca polui. Depende da
  LISTA DE TURMAS/alunos (o professor fornece) + save no Firebase (`/mundos/<turma>/<aluno>`). Casa com o
  login documentado "código de turma + primeiro nome".
- **União das 2 ideias (já documentada — reler quando esquecer):** `EDUCAVERSO.md` (mestre da união) ·
  `EDUVERSE-*.md` (visão da outra IA "EduVerse": FILOSOFIA/PIPELINE/PLANO/EQUIPE/FASE0/COMPUTACAO) ·
  `MUNDO-VIVO-*.md` + `IDEIA-MUNDO-VIVO.md` + `PLANO-FORA-DA-CAIXA.md` + `_plano/*.md` (linhagem Mundo
  Vivo do Marcos) · `EDUCAVERSO-QA.md` (os Portões 0-3) · `ATIVIDADE-PREMIUM.md` (formato fixo).

## 🏭 ESPECIFICAÇÃO-MÃE DA FÁBRICA (Marcos, jul/2026 — o produto em 1 parágrafo)
> "Eu passo o TEMA DA AULA e a TURMA (ex.: adição para o 1º ano) → a fábrica me
> SUGERE o tema/ambiente (pirata, espacial, floresta, cidade...) → nesses temas
> JÁ EXISTEM os personagens, objetos, sons, animação, tudo pronto → deve haver um
> BANCO com ~10 TEMAS diferentes, com personagens e tudo mais pronto em cada tema
> para REAPROVEITAR → e quando eu pedir, GERAR um tema de ambiente NOVO (que
> entra no banco)."
- **BANCO DE TEMAS** = a peça central: cada tema é um pacote completo (cenário/tiles,
  personagens com poses, props com contexto, paleta, sons, falas-modelo) validado UMA
  vez pelos portões; as atividades só o REUSAM (custo marginal ~zero, qualidade estável).
- Entrada da fábrica: `disciplina + conteúdo + turma` → saída: atividade completa
  (tema do banco + mecânica do catálogo + história própria + voz gerada) já auditada.
- Tema novo = pipeline de criação de tema (gera assets via gerar-imagens.yml, valida
  nos portões, registra no banco) — roda só quando o Marcos pede.
- Meta do Marcos: "usar o Claude como uma EQUIPE que entrega produto espetacular
  pronto" — cada especialista faz sua parte e SAI PRONTO (sem o Marcos corrigir arte).

## 🤖 DECISÃO FIRME — TUDO AUTOMÁTICO, NADA À MÃO (Marcos, jul/2026)
O Marcos quer a fábrica **100% automática**: ele digita o pedido (ex.: "adição, 1º
ano") e a linha PRODUZ tudo — quem "faz à mão" é a fábrica (workflows), nunca o
Marcos nem o Claude posicionando coisa a coisa.
- **NÃO usar editor MANUAL como etapa obrigatória** (ex.: Tiled/LDtk para desenhar
  mapa à mão = descartado; a IA GERA o layout e os PORTÕES auto-corrigem/refazem).
- **Pilha grátis por API/workflow:** imagem = Pollinations (sem chave) + Gemini
  (free tier); voz = edge-tts; sons = Web Audio + Freesound CC0; conteúdo/mundo/
  história/dados.json = a IA; qualidade = os 4 portões (reprovam e mandam refazer);
  publicação = workflows da Fábrica. Nada disso exige o Marcos.
- **Movimento "vivo" do personagem, automático:** (1) gerar CICLO de frames de
  caminhada pela IA de imagem (já provado na FASE E — 2 frames do Gemini, sem
  desenhar à mão); (2) piloto do **Meta "Animated Drawings"** (grátis, open source,
  roda em workflow: 1 imagem → esqueleto auto → anima). DragonBones/Spine são
  editores MANUAIS (rigging à mão) — NÃO têm API automática; só valem se o Marcos
  aceitar riggar o personagem UMA vez e reusar em todos os mundos ("à mão 1x,
  automático pra sempre") — hoje ele quer nada à mão, então ficam de fora por ora.
- **Único passo humano que sobra:** o "OK" final do Marcos (aprovar), e mesmo esse
  é opcional. "Automático" = quando não fica bom, a LINHA detecta e refaz sozinha,
  sem chamar o Marcos (auto-corrigível, não mágico/perfeito de primeira).
- **Referência estética travada:** a cena do INTERIOR da Taberna (luz de lampião,
  aconchego) = o padrão de beleza; "só faltou ser MAIS VIVA" (chama tremulando,
  poeira no facho de luz, NPCs respirando/gesticulando, gato que anda, lareira). O
  motor já tem os ingredientes — é ligar na cena. Somado à CENA-PINTURA (a IA pinta
  a cena inteira de uma vez = beleza do navio + quase nada a posicionar = mais auto).

## 🗺️ A GRANDE AVENTURA — estrutura do mundo (visão do Marcos)
> **REAFIRMADO pelo Marcos (jul/2026), versão cristalina:** cada MUNDO é uma
> JORNADA contínua guiada por HISTÓRIA, não atividades soltas. O LOOP é:
> **faz a tarefa que a atividade pede → GANHA a recompensa (ex.: a CHAVE) → a
> chave ABRE algo (ex.: a caverna/cabana) pra DORMIR e INTERAGIR → AMANHECE →
> segue o CAMINHO até a próxima tarefa → nova recompensa → ...** por ~**10 fases**
> nesse mundo, até **cumprir um objetivo** — sempre a história costurando tudo.
> As "atividades" (contar, subtrair, memória, arrastar...) são as TAREFAS de cada
> parada; a recompensa+interação+dia/noite são o TECIDO entre elas. É a camada de
> JORNADA por cima das estações. O motor JÁ tem os ingredientes (dia/noite, chave,
> entrar em cabana/taberna com interior+lampião, NPCs vivos) — falta STITCHAR num
> caminho contínuo de ~10 fases com recompensa/gate por fase. Cada mundo do banco
> de temas nasce como uma dessas jornadas.
>
> **ESCLARECIMENTO CRÍTICO (Marcos):** o exemplo "chave→caverna→dormir" foi SÓ um
> exemplo — **NÃO é template fixo.** Quem DEFINE o enredo, as recompensas e o FINAL
> é a **IA (o roteirista da fábrica)**, ÚNICO por mundo/tema. A estrutura acima é só
> a FORMA (fases encadeadas por história com recompensa/gate); o CONTEÚDO da história
> (qual é o problema, o que se ganha, qual o desfecho) a IA cria. E a **criança é
> PROTAGONISTA**: ela **CRIA/CONSTRÓI e cumpre os objetivos** de cada fase para
> avançar e **CONCLUIR a história** (não só assiste/escolhe — casa com o "ALUNO
> ATIVO/PROTAGONISTA" e a FILOSOFIA do EDUVERSE: o mundo precisa, ela resolve). O
> roteirista gera: enredo + arco de ~10 fases + recompensa de cada fase + FINAL que
> fecha o enredo; o montador encadeia; os portões conferem coerência/pedagogia.

O EducaVerso pode ser uma AVENTURA grande e contínua (uma floresta com caminho), não fases soltas:
- **Loop:** explorar a floresta → interagir → achar a CHAVE → atravessar um LABIRINTO → abrir a
  JAULA → SALVAR o amiguinho preso (animação: chave destranca, som, o amigo agradece) → seguir em
  frente → entrar numa CASA/CABANA (interagir, achar a próxima chave) → próximo labirinto → e assim
  vai (achar chaves, interagir, salvar personagens).
- **Vários** labirintos e **vários** personagens para salvar, ao longo do caminho.
- **LABIRINTO REAL DE PEDRA (ideia do Marcos):** um labirinto DE VERDADE — muros de pedra (tile
  premium de IA) preenchem a MAIORIA das células, deixando só **corredores sinuosos com becos sem
  saída**; existe **um caminho certo** até o amiguinho preso. A criança programa as setas para o
  Byte **serpentear pelos corredores** até chegar. NÃO é grid aberto com poucas árvores — é maze
  real. Usar na atividade "A Floresta do Byte". (Gerar/definir layouts de labirinto reais.)
- **Casas/cabanas vivas:** chaminé soltando fumaça, lenhador cortando lenha, detalhes que as
  crianças amam.
- **Ciclo dia/noite com HISTÓRIA:** escurece → o Byte precisa entrar na cabana, chegar perto da
  cama e DORMIR um pouquinho → amanhece → sai e continua a jornada.
- **Fases de ALÍVIO** intercaladas (memória-no-chão, pegar vaga-lumes, etc.).
- **Muita animação e SOM:** chave destrancando, jaula abrindo, o amigo agradecendo, fumaça,
  machado do lenhador, porta batendo, vento, gato miando, trovoada.
- **Como o SOM funciona (2 camadas, honesto):** (1) **Web Audio sintetizado** (grátis, minúsculo,
  offline) — vento (ruído filtrado + LFO), trovão (rajada de ruído), porta (batida grave + rangido),
  machado (toc percussivo), passos, chave (tilintar), faísca, UI. JÁ uso trovão assim. (2) **Sons
  realistas** (miado real, pássaros, lenhador) ficam melhores como **clipes mp3 CC0** embutidos —
  origem: pacote livre (CC0) ou o professor fornece (o chat não baixa; workflow pode). Regra do
  navegador: som e voz só começam após o 1º clique/toque → botão "🔊 Som" + mudo (volume).
- **A pedagogia mora DENTRO:** cada chave/labirinto/jaula guarda um desafio de aprendizado do
  currículo — a aventura é o embrulho; o aprender é o conteúdo (aprender sem perceber).
- **Blocos que JÁ temos (prova de conceito):** mundo explorável + dia/noite/clima (demo Mundo
  Vivo); entrar em casa + interior + lampião + NPCs + chave/inventário/porta (demo Taberna);
  guiar personagem por caminho com placas (demo Jardim/Placas). FALTA costurar num mapa contínuo
  + o labirinto + a cena de dormir + mais personagens/animações/sons.

## 🚦 DECISÃO DE ROTA (Marcos, jul/2026) — "começar pelo mundo vivo + paradas + popups; o plano ousado depois"
Reconciliação madura do Marcos (decisão FIRME de por onde começar), depois de sentir que fazer TUDO
imersivo dentro do mundo estava difícil demais para uma tacada só:
- **COMEÇAR pelo MUNDO VIVO** com tudo que ele já pediu (floresta viva, caminho, dia/noite, clima, NPCs,
  som). As **PARADAS** do mundo são temáticas: na floresta = **cabanas com FUMAÇA lindas** em que dá pra
  **ENTRAR no interior aconchegante cheio de efeitos** (o padrão da Taberna, trazido pro motor de produção);
  em outro mundo = outras paradas temáticas, e assim por diante.
- **As ATIVIDADES entram como POPUP no CENTRO da tela** — as atividades **premium que já conhecemos**
  (contar/ordenar/arrastar/memória/etc., reusadas do catálogo). Pragmático: entrega já, sem travar.
- **QUALIDADE DA ATIVIDADE/POPUP (regra firme do Marcos, jul/2026) — NÃO baixar:** a atividade que abre NÃO
  é um modalzinho pequeno que "o aluno nem enxerga direito". É uma **TELA CHEIA (FULLSCREEN)**, GRANDE. A ARTE
  dela tem que ser **GERADA e BEM BONITA**, com **EFEITOS, SONS, FALAS (voz gerada)** — o padrão PREMIUM que
  as atividades tinham, ENGAJADOR (o aluno gosta e quer jogar). Ex.: um **jogo da memória bonito com efeitos**,
  um **caça-palavras bonito com efeitos**. Cada tipo de atividade premium (memória, caça, quebra-cabeça, contar,
  arrastar...) é uma tela cheia caprichada, não um popup apertado. (Combina com o mundo, que também é fullscreen.)
- **CADA MUNDO tem VÁRIAS PARADAS, cada uma com SEU MASCOTE TEMÁTICO** (os mesmos mascotes das atividades
  premium — a atividade premium NÃO morre, vira uma PARADA com mascote dentro do mundo). **O DIFERENCIAL
  (definição do Marcos):** aqui não é uma página solta — é um **MUNDO que dá pra EXPLORAR**, com personagens,
  sons, vozes e efeitos, tudo que já combinamos do EducaVerso. O mundo dá a ALMA (exploração + vida); a
  parada entrega a PEDAGOGIA (popup premium com o mascote dela).
- **O PLANO OUSADO (aprender 100% DENTRO do mundo, interagindo) fica pra DEPOIS** — "mais pra frente a
  gente volta". NÃO é descartado; é adiado de propósito para não bloquear o lançamento. (O meio-termo já
  guarda alma: entrar na cabana e interagir no interior é imersivo; só a tarefa pedagógica é popup por ora.)
- **CAMADA DO ESTUDANTE junto (inegociável nesta rota):** um **SITE pra ENTRAR no mundo** (login simples),
  **SALVAR os dados do estudante** (progresso, onde parou) e a **AVALIAÇÃO do aprendizado** dele. Isso exige
  **BACKEND** (Firebase free — login por código de turma + nome; ver seção "CAMADA DO ESTUDANTE"). É o único
  pedaço pesado e novo, e depende de um SETUP do Marcos (criar projeto Firebase + dar a chave como secret).
- **Fácil x difícil (honesto):** fácil/reusa = mundo vivo, cabana+fumaça+interior, popups de atividade
  premium. Difícil/novo = a camada do estudante (backend/save/avaliação).
- **Ordem de construção proposta (MVP fatia vertical, pra NÃO espalhar):** (1) trazer "entrar na cabana +
  interior vivo" pro motor de produção; (2) uma parada abre um POPUP com uma atividade premium; (3) concluir
  a atividade = parada "resolvida" + avança no caminho; (4) TELA INICIAL do EducaVerso LINDA (branded,
  logo/identidade própria, modelo "seus mundos" do Minecraft mas pintado premium, com efeitos + musiquinha
  Web Audio) — o Marcos quer "bem linda como a PRIMEIRA que você me passou" = o CONCEITO que ja publiquei:
  https://claude.ai/code/artifact/ac466f52-adb6-4a9a-b21f-4be67b2197b7 (RECUPERAR esse conceito e construir
  a tela real a partir dele; digita NOME+TURMA) + SAVE local; (5) backend
  Firebase (progresso + avaliação + painel do professor). Provar a fatia com 1 mundo (floresta) + 2 paradas
  antes de escalar.

## 🏴‍☠️ 1ª ATIVIDADE DO MODELO NOVO — NAVIO PIRATA (Marcos, jul/2026) — em produção
Números até 30, 1º ano, CONCRETA (estilo Floresta dos Números), tema NAVIO PIRATA em alto-mar, Byte PIRATA
(reusa byte_pirata.png), paradas temáticas, muita animação+som. Equipe (pedagogo verifica o que o aluno
aprende + roteirista + diretor de arte + arquiteto de dados) monta história e o dados.json.
- **GERAR o que faltar de arte, bem bonito, no padrão da demo do NAVIO** (`_demos/educaverso/navio` — convés
  pintado + mar, que o Marcos amou). Reusar: byte_pirata, mar, barril, baú/baú-tesouro, convés. Faltando
  (gerar via workflow): poses do Byte pirata (ou solução SUAVE sem perna), objetos de contagem temáticos
  (moedas, laranjas, bombas...), partes do navio, NPCs (papagaio/lobo-do-mar).
- **LAYOUT — DECISÃO (Marcos, jul/2026): usar a ILHA, não o convés.** Tentamos primeiro (A) o NAVIO como mundo
  (convés visto de cima), mas ficou APERTADO e a perspectiva 3/4 (mesma da floresta) BRIGA com um convés chapado
  (o mastro virou "navio dentro do navio"). DECISÃO = (B): o mundo é uma **ILHA no meio do mar** (praia/areia,
  palmeiras, caminho, paradas espalhadas — igual à floresta, que combina com a câmera 3/4), e o **NAVIO é a
  ÚLTIMA parada/destino** (explora a ilha preparando tudo → no fim embarca/zarpa pra Ilha do Tesouro). A câmera
  NÃO muda (3/4 já é ótima); só o CENÁRIO vira ILHA (encaixa nela). Os engenheiros propuseram as 2 opções e
  recomendaram a (A) só por ser + rápida (reuso 100%); ao VER, a (B) é mais bonita = iteração normal, não erro.
  RECONSTRUIR o navio-pirata como ILHA: praia (areia/mar/palmeiras), paradas como pontos da ilha, o navio como
  cena final. Reusa a força do motor de mundo aberto (floresta/pomar).
- **DINÂMICA das paradas (Marcos):** com POPUP — o aluno chega numa parada, **ajuda ALGUÉM do mundo**
  (um NPC) resolvendo a atividade; essa pessoa **dá uma RECOMPENSA**; o aluno **conserta/destrava algo** e
  **avança** pra próxima parada. (É o loop tarefa→ajuda alguém→recompensa→avança, com a atividade premium no
  popup — casa com a "camada de jornada" e o modelo novo.)
- **REGRA DE ANIMAÇÃO (Marcos):** tudo SUAVE — respiração, gestos, deslizar. Se perna alternando ficar dura,
  fazer SEM perna, só suave. Suavidade acima de perna.
- Blueprint em `eduverse/NAVIO-PIRATA-BLUEPRINT.md` (a equipe escreveu). **DECISÃO: fazer o v2** (tudo NOVO e
  BONITO — gerar toda a arte pirata temática + efeitos + vozes), não o v1 de reuso.
- **FASES DE ALÍVIO intercaladas (pedido do Marcos) — TEMÁTICAS + ligadas ao conteúdo:** além das 7 paradas
  pedagógicas, intercalar jogos de alívio (colorir, MEMÓRIA, jogo de SOMBRAS, LIGAR PONTOS, e outros do
  catálogo) — escolher alguns e fazer MAIS paradas. TUDO com a cara do tema (pirata) E do conteúdo (números
  até 30). Escolhas que ENCAIXAM em número+pirata: **LIGAR PONTOS 1→30** (desenha um navio/mapa do tesouro =
  ensina a ordem dos números até 30, perfeito no tema); **MEMÓRIA** (parear numeral↔quantidade de moedas, ou
  itens piratas); **JOGO DE SOMBRAS** (casar objeto pirata com sua silhueta: barril, canhão, papagaio);
  **COLORIR por número** (colorir cena pirata por número = reconhecer o numeral). Intercalar entre as paradas
  de aprender (alívio no meio, ex. após P3 e P5). HONESTO: memória/sombras já existem no catálogo; colorir e
  ligar-pontos-até-30 podem precisar ser construídos no motor — escolher os que melhor servem número+pirata.
  Construção do v2 (arte + vozes + alívios + auditar) após a Fase 1 (motor de personagem vivo).
- **APOIO AO ERRO POR CONTAGEM ACESA — FEATURE PREMIUM OBRIGATÓRIA (Marcos lembrou; CONFERIDO: hoje NÃO está
  no motor da aula, só há dica gentil):** quando o aluno erra numa tarefa de QUANTIDADE, o mascote fala "Não
  foi dessa vez! Vamos contar juntos, bem devagar." e **ACENDE cada objeto UM A UM, EM SINCRONIA COM A VOZ**
  (a luz do objeto k acende junto com a voz dizendo o número k) — só glow (`filter:drop-shadow`, SEM
  transform:scale). A FALA comanda a luz (encadear pelo callback do `falar`, não 2 relógios separados — ver
  MANUAL-MESTRE seção 6). No fim: "São N ao todo! Agora toque no número N." É PADRÃO das atividades premium.
  CONSTRUIR isso no motor/nas atividades de contagem (aula E popups premium de identificar quantidade). É
  requisito de entrega, não opcional.
- **CURADORIA = CURRÍCULO + EDUCAÇÃO (reforço firme do Marcos):** a escolha das mecânicas/atividades NÃO é
  por "ser divertida" — é ancorada no CURRÍCULO (BNCC/Blumenau) e na PEDAGOGIA. O especialista de
  interatividades cura junto com o pedagogo; toda mecânica escolhida serve um objetivo de aprendizagem real
  e a faixa etária. Diversão é o veículo, o aprendizado (verificado) é o destino.

## 🎮 PAPEL NOVO NA EQUIPE — GAME/LEVEL DESIGNER 2D (lição paga, jul/2026)
O convés-de-cima ficou apertado/incoerente (mastro virou "navio dentro do navio") porque faltava na equipe
um **GAME/LEVEL DESIGNER 2D** — o papel que pensa LAYOUT, PERSPECTIVA (a câmera 3/4 combina com o cenário?),
level design (o mundo é gostoso de explorar/jogar?) ANTES de construir. Tínhamos engenheiro/arte/roteiro/
pedagogia, mas esse olhar faltou. **AÇÃO: incluir o Game/Level Designer 2D na equipe/linha** — ele valida
layout+perspectiva+ritmo de exploração de cada mundo no PROJETO, evitando refazer depois. (Iterar é normal em
jogo — mas esse papel corta os erros grosseiros de layout de cara.) Junto com o Diretor de Arte e o Portão de
Coerência. E a linha modular (dados-driven) é o que torna a correção BARATA quando ela acontece.

## 🧱 ARQUITETURA MODULAR (direção do Marcos, jul/2026) — "um motor por coisa"
O Marcos propôs "fazer um motor pra cada coisa pra modularizar/automatizar" — incluindo o "aprender diferente"
como um motor À PARTE. INSTINTO CERTO (bate com os "12 módulos" da outra IA: Core/Render/World/NPC/Mission/
Dialogue/Inventory/Animation/Sound/Classroom/AI). AJUSTE IMPORTANTE: NÃO são motores DUPLICADOS separados (isso
reescreveria mundo/personagem/som toda vez) — são **MÓDULOS que se COMPÕEM** (peças de LEGO), cada um faz UMA
coisa e reusa os outros:
- **Módulo MUNDO** (cenário vivo), **Módulo PERSONAGEM** (o "ator vivo" universal — JÁ extraído ✅),
  **Módulo SOM/VOZ**, **Módulo ATIVIDADE** (plugável).
- **A ATIVIDADE é um MÓDULO PLUGÁVEL:** hoje = tipo "popup premium" + tipo "aula in-world" (rounds). O
  **"APRENDER DIFERENTE" (aluno cria/coliga/resolve o problema do mundo pra avançar) = um MÓDULO NOVO de
  atividade** ("construção/resolver-no-mundo") que pluga no MESMO mundo + MESMO personagem, SEM mexer no popup.
  Pode ser desenvolvido e testado SOZINHO e depois encaixado em qualquer mundo. É o jeito limpo de entregar a
  ideia ousada no futuro sem refazer o mundo.
- **HONESTO:** o motor hoje (`kit-floresta.py`) é meio MONOLÍTICO (mundo+personagem+aula juntos). Modularizar é
  investimento PROGRESSIVO; o sistema de personagem vivo foi o 1º pedaço tirado pra fora. Refatorar em módulos
  limpos conforme fizer a 2ª/3ª atividade — NÃO parar a entrega atual pra refatorar tudo de uma vez.
- **Regra:** o "aprender diferente" NÃO precisa de um motor duplicado — precisa de um MÓDULO de atividade novo
  sobre o mundo+personagem existentes. Quando chegar a hora, nasce como o módulo dele.

## 🧭 ARQUITETURA (a reconciliação): mundo-mapa + atividades-peça
NÃO é contradição — são DUAS CAMADAS:
- **Camada 1 — O MUNDO / MAPA com BAIRROS** (o hub "Ilhas do Saber", só que mais "mundo"): dá a
  sensação de **um universo só** e da **jornada do ano**. Bairros por faixa/turma/tema.
- **Camada 2 — AS ATIVIDADES:** cada **bairro/parada** é uma atividade, e cada uma é **seu próprio
  repo/link** (portal leve). Pode ser focada (55 min) OU uma **mini-aventura rica** (a floresta com
  labirintos). A criança está no mapa, entra num lugar, joga, volta ao mapa.
- **AO LONGO DO ANO = SEQUÊNCIA DIDÁTICA:** os bairros/atividades **abrem na ordem do currículo**
  (bimestre a bimestre); o **save** transforma em jornada contínua do ano letivo.
- É o **EduVerse (visão da outra IA) realizado**, mas de um jeito **leve e que escala**.
- **Decisão de design (do Marcos):** (A) mapa + atividades = recomendado (leve, escala, peça
  independente/descartável) · (B) mundo 100% contínuo = imersivo mas pesado/difícil de escalar.
  **Híbrido ideal:** mapa como espinha (A) + cada atividade pode ser mini-aventura + o próprio
  mapa bonito e vivo (mascote andando nele).
- **DECISÃO (corrigida pelo Marcos):** o EducaVerso é um **MUNDO NOVO E PRÓPRIO**. **NÃO** usamos
  o hub antigo "Ilhas do Saber" (`mundo-das-atividades`). Ficamos **só no mundo vivo novo — o
  EducaVerso**. Ele terá a **própria casa/mundo** (o mapa-mundo com bairros faz parte do EducaVerso,
  é dele, não do hub velho). As atividades-aventura são do EducaVerso, no espaço dele. Projeto
  novo, do zero, sem misturar com o antigo.

## 📦 Dinâmica do EducaVerso: 1 repo por atividade + empacotamento + som
- **Um repositório por atividade** (regra "portal leve" do CLAUDE.md): cada atividade =
  `index.html` + `img/` + `audio/`, publicada no GitHub Pages, com **link próprio**. O hub
  "Ilhas do Saber" é só um **mapa leve** que APONTA os links — não carrega o peso. Assim escala
  (5 ou 500 atividades) sem o build engasgar. Cada atividade é **independente e descartável**.
- **Empacotamento:** TESTE rápido = HTML self-contained (assets em base64, 1 arquivo). PUBLICADA
  = pasta leve (`index.html` + `img/` + `audio/`). Fábrica cria/atualiza o repo por workflow.
- **FALA (narração/diálogo)** = TEXTO → `gerar-audio.yml` (edge-tts) → mp3. (Voz por API, sim.)
- **SFX de ambiente/ação** (vento, trovão, porta, machado, passos, chave) = **Web Audio
  sintetizado** (grátis, offline).
- **SFX realistas** (miado, pássaros, lenhador) = **clipes mp3 CC0**: o chat NÃO baixa, mas um
  **workflow baixa** (a montar: `baixar-sons.yml`, igual gerar-imagens) OU o professor fornece.
  Regra séria: só **CC0 / livre de direitos** (é produto de escola).

## 🎓 ROADMAP CURRICULAR do Marcos (o que a Fábrica precisa saber)
- **ESTE ANO:** disciplinas **normais** do currículo (Português, Matemática, Ciências, etc.). As
  atividades EducaVerso deste ano servem essas disciplinas.
- **PRÓXIMO ANO:** **Computação específica** — objetivos de aprendizagem **POR TURMA**, pelos
  **TRÊS EIXOS da BNCC Computação**: (1) **Pensamento Computacional**, (2) **Mundo Digital**,
  (3) **Cultura Digital**. **Começar por PENSAMENTO COMPUTACIONAL.**
- **Encaixe:** a atividade Jardim/Placas (programar o caminho — sequência, algoritmo, lógica)
  **JÁ é Pensamento Computacional** → alinhada com o início do próximo ano. É um baita ponto de
  partida.
- **Fábrica de Atividades:** organizar por **DISCIPLINA** (este ano) e por **EIXO + TURMA**
  (Computação, próximo ano). Ancorar sempre no currículo real (Blumenau + BNCC Computação;
  ver `ATIVIDADE-COMPUTACAO.md`).

## 🎯 META CRÍTICA do Marcos: EducaVerso cobre TODO o currículo de Computação
> ⏳ **ADIADO a pedido do Marcos — DIALOGAR DEPOIS** (o mapa de cobertura + a questão
> plugado/desplugado). Registrado aqui para retomar. Prioridade agora: construir a 1ª atividade.
- Ano que vem o Marcos ministra o **currículo de Computação**. A **coordenadora** pede
  **atividades DESPLUGADAS** + **sequências didáticas**.
- O Marcos QUER que o **EducaVerso atinja TODOS os objetivos de aprendizagem** (3 eixos × turma)
  como uma **SEQUÊNCIA DIDÁTICA COMPLETA** — **sem** precisar fazer atividades desplugadas soltas
  nem outras sequências à parte. **Tudo alcançado no EducaVerso.**
- **Como provar/entregar:** um **MAPA DE COBERTURA CURRICULAR** — cada objetivo (BNCC Computação
  + currículo de Blumenau) → uma **missão/atividade EducaVerso**, em sequência ao longo do ano.
  Isso É a sequência didática **e** a prova de cobertura para a coordenadora.
- **Honestidade (tensão a alinhar):** EducaVerso é **PLUGADO** (tela); a coordenadora pede
  **DESPLUGADO** (sem computador). EducaVerso entrega os MESMOS objetivos com o mesmo espírito
  (construir/fazer/manipular) e pode **GERAR materiais desplugados imprimíveis** (cartas de
  comando, tabuleiros, trilhas) das mesmas missões. Se "conta" como desplugada é decisão
  pedagógica do Marcos + coordenadora — a gente dá as duas formas.

## 🛡️ Regra de ouro contra ESQUECER
1. **Sincronizar com o GitHub ANTES de agir** (o hook `.claude/hooks/sync-remoto.sh`
   já faz automático no início da sessão).
2. Se o **Marcos disser "isso a gente já fez"**, **ACREDITAR e verificar a fundo**
   (sincronizar + reler os manuais). **"Não achei" ≠ "não existe".** Nunca insistir.
3. **Anotar aqui** toda capacidade, secret ou decisão nova — para a próxima
   sessão (que sou eu, sem memória) já nascer sabendo.
4. **LIÇÃO PAGA CARA (jul/2026):** o ambiente reiniciou e me jogou numa cópia local
   ANTIGA (commit velho). Eu concluí que o `eduverse/` inteiro (fábrica, auditores,
   as 6 poses do Byte, a fogueira, os jogos APROVADOS) tinha se PERDIDO — e fiz o
   Marcos passar por uma caça enorme. **Estava tudo no GitHub o tempo todo.** Dois
   enganos meus: (a) confiei na pasta local sem `git fetch`; (b) a **busca de código
   do GitHub NÃO indexa branch que não é a `main`** — o `eduverse/` vive na branch de
   trabalho, então ela "não achou" e eu acreditei nela. **REGRA:** parece faltando?
   → `git fetch origin <branch>` + `git ls-files <caminho>` + `git log -- <caminho>`
   (NÃO a busca de código, que não vê a branch) + **acreditar no Marcos**. NUNCA
   declarar "perdido" de uma cópia local. E ao salvar: **confirmar o push no GitHub**
   (ex.: ler o arquivo pela API), não confiar no "push OK" local.
5. **TRAVA BLINDADA (jul/2026):** o `sync-remoto.sh` antigo DESISTIA na 1ª falha
   de fetch e imprimia o mesmo `✅ conferido` — parecendo tudo em dia quando NÃO
   estava (foi assim que abri numa cópia 30+ commits velha e "não achei" o
   `eduverse/`). Agora o hook tem **RETRY (3x)** no fetch e, se não conseguir
   confirmar o GitHub, imprime um **aviso ALTO** (`⚠️ NÃO consegui conferir`),
   NUNCA o `✅`. Regra pra mim: se vir esse aviso no início da sessão, rodar
   `git fetch origin <branch>` + `git merge --ff-only` ANTES de agir/declarar
   qualquer coisa "perdida".

## 🎙️ ELENCO DE VOZES — TODAS geradas por API (decisão firme do Marcos, jul/2026)
Todas as falas do mundo são GERADAS por API (edge-tts), embutidas em MP3 (base64). Nada de voz do navegador.
Casting pedido pelo Marcos:
- **NOSSO PERSONAGEM (protagonista, ex.: Byte) = ANTONIO** (masculina, edge-tts pt-BR).
- **NPCs MENINOS = OUTRA voz MASCULINA** (diferente do protagonista).
- **NPCs MENINAS = voz FEMININA.**
- **HONESTIDADE TÉCNICA (edge-tts):** o pt-BR do edge-tts tem POUCAS vozes nativas — masculina = **Antonio**;
  femininas = **Francisca** e **Thalita** (2 opções, ótimo p/ separar meninas). NÃO há uma 2ª masculina
  nativa confiável em pt-BR (a "Donato/male2" FALHOU no passado — lição paga). SOLUÇÃO p/ a 2ª voz masculina:
  (a) **pitch/rate shift no Antonio** (a função `pitch_shift` já existe no `gerar-audio.yml`, só ligar no
  `gerar()`) — grave p/ lobo-do-mar, agudo p/ menino; OU (b) voz **pt-PT masculina** (Duarte) se o sotaque
  de Portugal for aceitável (testar 1 fala antes). Preferir (a) pra manter sotaque BR.
- **Elenco por personagem** (registrar no dados.json de cada atividade): cada NPC declara sua voz (id +
  pitch/rate). O montador/gerador de áudio usa isso. Ex. navio: Byte pirata=Antonio; papagaio=Antonio agudo;
  lobo-do-mar=Antonio grave; NPC menina=Francisca; 2ª menina=Thalita.
- Testar 1 fala de cada voz antes de gerar o lote (nunca confirmar sem ouvir).

## 🧍‍♂️ MOTOR DE PERSONAGEM VIVO — UNIVERSAL (pedido firme do Marcos, jul/2026)
> "Se der pra ter o andar normal e suave, construa esse MOTOR e depois aplique em TODOS os personagens,
> como se estivessem vivos: respiração, movimento normal de pernas/braços, sentar, deitar, etc. E o
> personagem NÃO precisa ser sempre o robô — podemos gerar um NOVO por atividade, SE tivermos o motor pronto."
- **PROVA DE QUE DÁ:** o Byte já anda suave com 2 quadros de perna alternando (byte_frente_anda/_anda2,
  byte_costas_anda/_anda2), + respiração/blink/sway/gesto + sentar/deitar/falar/feliz. Deu certo SEM tremor.
- **AÇÃO:** GENERALIZAR essa animação (hoje amarrada ao `byte`/objeto `POSE`) num SISTEMA reutilizável que
  anima QUALQUER personagem a partir da sua CARTELA de poses (idle=respira+pisca+balança, andar=2 quadros de
  perna onde houver sprite senão só deslizar suave, sentar, deitar, falar, feliz, gesto). Data-driven,
  default-seguro. APLICAR a TODOS (Byte + NPCs — hoje NPC só respira/balança). Assim cada atividade escolhe/
  gera seu próprio mascote (a cartela de poses vem do pipeline de imagem, como já foi feito pro Byte pirata).
- **REGRA (Marcos):** SUAVIDADE acima de tudo. Se a perna alternando ficar dura num personagem, cair pro
  modo só-suave (respira/desliza/gesto) sem perna. Nunca preferir "com perna" se ficar pior.
- **OVO QUE CRESCE → MASCOTE (ideia do Marcos, manter):** um mascote pode NASCER de um ovo que cresce/choca
  e evolui (uma progressão de sprites: ovo→racha→filhote→mascote). É só mais um personagem no sistema, com
  uma cartela que muda por estágio. Lúdico e dá vínculo (o mascote "do aluno").
- **É o "motor pronto" que destrava TUDO:** personagem por atividade, mascote do aluno, o Byte pirata, etc.

## 🎭 Ideias do Marcos para PERSONAGENS VIVOS (incorporar no EducaVerso)
Pedidos do professor para os personagens ficarem "de videogame" — anotar para o
documento-mestre (`EDUCAVERSO.md`, seção Personagens Vivos) e para implementar:
- **Boca mexendo ao falar** + **piscar os olhos** + **respirar** no idle (já planejado).
- **Movimento suave e realista de mãos e pernas** — inclusive AÇÕES como
  *entregar a chave* (braço estende, a chave passa, braço recolhe). Caminho técnico:
  (a) **cartela de poses** gerada por IA (idle, andar, "entregando", feliz) trocada
  como sprite sheet — mais simples, é o que o pipeline já faz; OU (b) **recorte em
  partes** (corpo/braço/mão/pernas) animadas por código com easing — mais suave,
  mais trabalho. Começar por (a).
- **Interagir com o MASCOTE da criança** — o aluno tem seu próprio mascote/avatar
  que o acompanha; o Byte e os NPCs interagem com ele (legal p/ pertencimento).
- **O mascote/Byte SEMPRE fala o NOME do estudante** na narração ("Muito bem, João!").
  Fácil e alto impacto: o aluno informa o nome (login simples por código de turma) e
  o nome entra nas falas/narração (Web Speech interpola o texto). Já existe a ideia
  de `S.nome` nos manuais.
- **Guardar o progresso do estudante (a aventura dura o ANO INTEIRO):** o jogo salva
  onde a criança parou (mundos/áreas abertos, itens, atividades feitas, evidências).
  Duas camadas: **local** (localStorage, funciona offline) + **nuvem** (Firebase, com
  login simples por código de turma + nome) — a criança volta e CONTINUA de onde
  parou, a aventura seguindo o ano letivo (campanha por bimestre/semestre). **O mesmo
  dado salvo alimenta a avaliação descritiva** e o painel do professor (o que a criança
  fez = a evidência). É a "jornada do estudante" da visão do EducaVerso.

## ✅ CONSTRUÍDO — "A Floresta do Byte" (Etapa 1, versão incrível) — 2026-07-15
Primeira atividade do EducaVerso, montada com todos os especialistas e aprovada nos
**Portões 1 e 2** do `EDUCAVERSO-QA.md` (falta o Portão 3, do Marcos).
- **Arquivo:** `_demos/educaverso/floresta/index.html` (HTML único, ~611 KB, base64,
  offline). Builder: `_demos/educaverso/floresta/build_floresta2.py`. Assets (todos IA):
  grama (chão), muro de pedra (paredes), árvore, byte, gato, coelho, passarinho, nimbo,
  jaula, chave, seta de madeira, cabana.
- **Labirinto REAL de pedra:** chão de grama (IA) + muros de pedra (IA) preenchendo a
  maioria das células; corredores sinuosos com becos (M2). Grid 9×7. **Byte sempre
  desenhado por cima dos muros** (regra: muro nunca esconde o Byte). Muros em relevo
  (topo levantado + face frontal + sombra), y-sort linha a linha.
- **História:** Nimbo (nuvem cinzenta resmungona, com raio e trovão) prende 3 amiguinhos;
  no final o Nimbo vira bonzinho e há festa na cabana (chaminé com fumaça).
- **3 missões** guiando o Byte com **setas de madeira no chão** (clicar cicla a direção):
  M1 sequência (serpentina), M2 desvio (becos sem saída), M3 repetição (espiral até o
  centro). Amiguinhos: Gato Pigo → Coelha Nina → Passarinho Tuim.
- **1 alívio:** pegar vaga-lumes (após M1), volta ao mundo sozinho.
- **Som Web Audio:** vento (loop), passo, erro, chave, faísca, miau, pio, trovão, twinkle,
  vitória. **Voz** pt-BR (Nimbo com pitch grave). Destrava no 1º gesto + botão "Som e Voz".
- **Pedagogia (Pensamento Computacional, sem perceber):** a criança CONSTRÓI o algoritmo
  (sequência de setas), erra e depura (seta no muro = tremor + som, sem X vermelho),
  vê consequência no mundo. Gating: só liberta quem chega na jaula.
- **LIÇÃO PAGA (nova):** *screenshot com `--virtual-time-budget` engana* — o tempo virtual
  pode capturar o meio de uma animação/ciclo e parecer que "voltou ao início". Para PROVAR
  a mecânica, **dirigir de forma determinística**: `_qaSolve()` (BFS resolve o labirinto) +
  simular o `prox()` passo a passo e **despejar o resultado no `document.title` com
  `--dump-dom`** (não confiar só na foto). Assim confirmei M1/M2/M3 `reached=true` e a
  cadeia missão→alívio→missão→final `salvos=3`.
- **A-FAZER (próximas etapas):** mais amiguinhos (tartaruga/Lelê, esquilo/Tuca, sapo/Coaxo),
  missões de depuração e loop com a placa "repetir", mais alívios (memória-no-chão, regar
  flores), fechar os 55 min; depois: nome do estudante na narração + salvar progresso.

## 🔊 Voz gerada + controles no celular — "A Floresta do Byte" — 2026-07-15
- **VOZ GERADA (não a do navegador):** as falas fixas são geradas pelo workflow
  `gerar-audio.yml` (edge-tts) em **lote** (`_audio/<id>.mp3`) e **embutidas em
  base64** no HTML, tocadas por `<audio>`. A `speechSynthesis` do navegador vira só
  **reserva**. Vozes: narrador/Byte/amiguinhos = **female (Francisca)**; Nimbo =
  **male (Antonio)**. **LIÇÃO PAGA:** a voz `male2`/**Donato** FALHOU no edge-tts
  ("edge-tts falhou") — saiu do catálogo; usar `male` (Antonio) ou `female`
  (Francisca), que funcionam. Sempre restringir o embed à LISTA de ids da atividade
  (o `_audio/` do repo tem centenas de mp3 de outras atividades — embutir tudo incha).
- **D-PAD no celular (pedido do Marcos):** em telas de toque aparece um teclado de
  setas (▲◀✖▶▼); no PC ele **some** (detecção `pointer:coarse`/`ontouchstart`;
  `?dpad=1` força p/ teste). Dinâmica no toque: **tocar numa pedra** (anel de
  destaque) → **escolher a direção** no D-pad → **VAI**; ✖ remove. No PC continua o
  clique-que-cicla a seta.
- **LIÇÃO PAGA (screenshot):** o Chromium headless tem **largura mínima ~500px** —
  foto com `--window-size=400` corta a direita e PARECE overflow. Diagnosticar com
  `document.body.scrollWidth` vs `innerWidth` (deu 500==500 = sem estouro), não confiar
  no corte da foto. Fotografar em ≥500px de largura p/ prévia mobile fiel.
- **Publicação:** repo próprio **`floresta-do-byte`** → `atualizar.yml`
  (`repo_name=floresta-do-byte`, `source_dir=_novo`). No ar em
  **https://vidalprof.github.io/floresta-do-byte/**.

## 🎭 A-FAZER: voz PRÓPRIA por personagem (adiado pelo Marcos — 2026-07-15)
Decisão do Marcos: por ora fica com 2 vozes (Francisca = narrador/amiguinhos;
Antonio = Nimbo). Voz por personagem fica pra depois. Dois caminhos já mapeados:
- **edge-tts (grátis):** poucas vozes nativas pt-BR (Antonio/Francisca) → multiplicar
  por **pitch/velocidade** (função `pitch_shift` já existe no `gerar-audio.yml`, só
  falta ligar no `gerar()`): Nimbo grave, bichinhos agudos.
- **Gemini TTS (pago, chave configurada):** MUITAS vozes atuadas (Puck, Kore, Charon,
  Fenrir, Aoede...) + direção de atuação ("leia como vilão/gatinho"). `modelo=gemini`
  no workflow (testar 1 fala antes — nunca confirmar sem ouvir).
- **Elenco proposto:** Byte/Narrador = clara/acolhedora; Nimbo = grave/resmungona;
  Gato Pigo = agudo/brincalhão; Coelha Nina = doce; Passarinho Tuim = bem agudo/rápido.

## ⭐ FILOSOFIA DO EDUVERSE (LEI — trazida pelo Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-FILOSOFIA.md`** (é o **Portão 0** do QA). Resumo do que NÃO
esquecer NUNCA:
- **Não é jogo de pergunta/resposta. Não é prova disfarçada.** Nada de "acerte a conta →
  abre o baú/porta/ganha moeda". Esse modelo já existe; o EduVerse é OUTRA coisa.
- O aluno aprende porque **O MUNDO PRECISA** daquele conhecimento. **Problema primeiro**;
  o **conteúdo/pergunta NUNCA aparece primeiro**; o **conceito é nomeado por ÚLTIMO**.
- Arco fixo: **História → Exploração → Problema → Experimentação → Descoberta → Conceito →
  Aplicação → Reflexão** (nunca invertido).
- Conhecimento = **ferramenta** (resolve), nunca **obstáculo** (bloqueia).
- **Byte pergunta** ("o que você percebe?", "tem jeito mais rápido?", "achou um padrão?",
  "como organizar isso?"), nunca "qual é a resposta?".
- Eu (IA) transformo conteúdo escolar em **experiência** (história/construção/investigação),
  **nunca** em lista de perguntas. Exemplos do Marcos (multiplicação): plantar 6 canteiros ×
  4 árvores; caixas de 8 rodas × 7 caixas; galinheiros de 6 galinhas — o aluno organiza
  grupos, conta, vê padrão, e a multiplicação **nasce** disso.
- No fim o aluno diz "hoje **ajudei/construí/salvei/descobri**", e só depois "…aprendi X".

**Aplicar já na "Floresta do Byte":** o Byte deve **provocar** (perguntas), a mecânica de
guiar/empurrar é a **ferramenta** pra salvar o amigo (problema do mundo), e fechar com a
**descoberta + nome do conceito** (algoritmo/sequência/depuração) + **reflexão**, de leve.

## 🤖 FILOSOFIA DA COMPUTAÇÃO + MAPA DA SEQUÊNCIA DIDÁTICA (Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-COMPUTACAO.md`** (Parte 2 da filosofia). É o **mapa** que a
coordenação pede pro ano que vem. Progressão dos conceitos, cada um nascendo de um PROBLEMA
do mundo (nunca apresentado primeiro):
1. **Sequência/Algoritmo** — desenhar o caminho do robô; ele executa exatamente; erra na tela.
2. **Condição (SE)** — rio em que o robô cai → "SE achar rio → vira".
3. **Repetição (loop)** — 10 entregas iguais → "dá pra mandar repetir sozinho?".
4. **Função** — vários robôs iguais → "uma instrução que qualquer robô use".
5. **Depuração** — o robô executa o erro de verdade; observa, acha, corrige, testa.
Mundo-exemplo: **Vale das Máquinas** (robôs, trem, fábrica, esteiras, rio, ponte, cidade) —
cenário ideal pro ano da Computação, com o mesmo Byte.
**JÁ FAZEMOS o item 1** na "Floresta do Byte" (põe setas = desenha caminho; VAI; Byte erra no
muro = depuração sem X). FALTA: Byte perguntando + condição + repetição explícita + função.
A Floresta do Byte é a **Missão 1** dessa jornada (ponte pro currículo de Computação).

## 🏗️ PIPELINE DE CONSTRUÇÃO + BIBLIOTECA LEGO (Marcos, 2026-07-15)
Documento oficial: **`EDUVERSE-PIPELINE.md`** (Parte 3). Regra-mãe: **não criamos atividades,
criamos MUNDOS VIVOS**; a atividade nasce dentro. Pipeline de 10 etapas (mundo → vida →
personagens → rotina → objetos inteligentes → PROBLEMA → exploração → necessidade → conceito
natural → reflexão). **Mapas por TILES** (32/48/64) tipo LEGO; **biblioteca reutilizável** de
tiles/objetos/personagens; **folha de animações padrão** por personagem (parado, andar ↑↓←→,
falar, feliz, pensando, comemorando, triste, esperando). Tech: Canvas 2D, sprite sheets, tiles,
Firebase; compat. Win7/Chrome antigo, 1024×768. **Objetivo:** nova atividade = MONTADA com peças
reutilizáveis, não do zero (é isso que deixa a criação FÁCIL). Futuro: editor arrastar-e-soltar.
FALTA construir o KIT base (estilo travado → tiles + Byte animado + objetos) e passar a montar as
atividades a partir dele.

## 💰 REGRA DE OPERAÇÃO — modelo adequado por tarefa (economia, jul/2026)
Ao convocar subagentes/equipes: tarefa MECÂNICA (builds, greps, screenshots,
conferir laudo) = **Haiku**; codificação padrão (portão, dados.json) = **Sonnet**;
arquitetura/síntese/auditoria adversarial = **Opus/Fable**. Regular também o
esforço de raciocínio por agente (baixo no mecânico, alto só em verificação/chefia).
O modelo da SESSÃO principal só o Marcos troca (/model).

## 🌐 EDUMUNDO (tela do aluno) + PAINEL DO PROFESSOR — decisões travadas (Marcos, 2026-07-17)
DEPOIS que o teste de Firebase passou (login anônimo + gravar + ler no RTDB do projeto
`educaverso-73b1a`, run 29548937470 SUCCESS), o Marcos definiu como aluno e professor entram:

- **DOIS SITES/REPOS SEPARADOS.** (1) **EduMundo** (aluno, público e bonito, é "a tela do
  EducaMundo/EducaVerso inicial"); (2) **Painel do professor** (repo próprio, com **SENHA**,
  **invisível para os alunos**). Nunca juntar os dois no mesmo endereço.
- **Professor cadastra TURMAS + ALUNOS no painel** (só nome + avatar emoji; sem digitar senha
  para a criança). O painel também **mostra o progresso** (lê `/turmas/<turma>/alunos` = a função
  `listarTurma` já existente).
- **Login do aluno = ZERO digitação.** Professor abre o EduMundo nos PCs do lab já apontado pra
  turma pelo **link** (`educamundo/?t=<turmaId>`). A criança vê os cards **nome+avatar** da turma
  dela e **TOCA no seu**. Por baixo: login **anônimo silencioso** no Firebase; progresso salva em
  `/turmas/<turmaId>/alunos/<alunoId>`. Senha visual de 2 figurinhas fica OPCIONAL (ligar depois só
  se precisar; começar sem, pra não travar o piloto).
- **Acesso do professor = senha** (piloto: gate no cliente + site separado que a criança não conhece).
  Honestidade: é segurança de piloto (dado não sensível: 1º nome + progresso). Nível 2 (cada aluno só
  mexe no próprio; professor dono) fica pra produção.
- **Modelo de dados:** `/turmas/<turmaId>` = { nome, alunos:{ <alunoId>:{ nome, avatar, dados, atualizado_em } } }.
- **Arquivos no repo-fábrica:** `_educamundo/index.html` (aluno) e `_painel-prof/index.html` (professor).
  Publicar cada um no seu repo via Fábrica/atualizar. Regras do RTDB atualizadas em
  `eduverse/lib/REGRAS-FIREBASE.txt` (agora cobrem o metadado da turma + listar turmas no painel).

## 🗺️ EDUMUNDO = MUNDOS VIVOS COM PARADAS, CATÁLOGO DINÂMICO (Marcos, 2026-07-17)
Pergunta do Marcos: "as atividades no EduMundo são injetadas?" -> estavam FIXAS no
código (array JOGOS). Decisão: **NÃO ficam no código**. O EduMundo lê o CATÁLOGO do
Firebase (biblioteca que cresce; a Fábrica/painel adiciona, a tela mostra sozinha).
E o aluno vê **MUNDOS VIVOS COM PARADAS** (não lista plana): toca o nome -> vê os
MUNDOS (cards) -> entra num mundo -> MAPA temático com as PARADAS (medalhão do
mascote + trilha), toca a parada -> abre o jogo (link próprio; portal leve).
- **Modelo de dados (Firebase):** `/catalogo/mundos/<mundoId>` =
  { nome, emoji, tema, cor, ordem, paradas:{ <pid>:{ titulo, mascote, link, ordem, x, y, soon } } }
- **Progresso:** `/turmas/<t>/alunos/<a>/dados/progresso/<mundoId>/paradas` (paradas visitadas).
- **Semear catálogo:** workflow `semear-catalogo.yml` grava o mundo Ilha do Tesouro + 7 paradas.
  EduMundo tem fallback amigável + cache offline se o catálogo estiver vazio/offline.

## ⚠️ REINCIDÊNCIA: cópia local voltou pro base velho (2026-07-17)
Ao commitar o EduMundo dinâmico, o git local estava em 3dc86eb (base VELHO, "behind 847").
Cura aplicada: salvar os arquivos bons em /tmp, `git reset --hard origin/<branch>`, reaplicar
por cima, commitar. SEMPRE conferir `git status -sb` (procurar "behind N") ANTES de commitar.

## 🥚 EDUCAVERSO (nome correto) + ENTRADA COM OVO→MASCOTE (Marcos, 2026-07-17)
Marcos corrigiu: o nome é **EducaVerso** (eu tinha escorregado pra "EduMundo"). E a
entrada tem que ser a ideia inicial: aluno toca o nome -> (1ª vez) um **OVO choca** e
ele **escolhe o MASCOTE** dele -> **cai DIRETO no mundo vivo** (mapa de paradas), sem
menuzinho. O **mascote é o personagem** que anda no mapa (o token) e **cresce o ano
todo** (guarda quantas paradas fez; nivel=1+floor(paradas/3)). "Outros mundos" fica num
botão de canto. Pasta renomeada `_educamundo`->`_educaverso`; repo de destino = `educaverso`
(link `https://vidalprof.github.io/educaverso/`). Painel atualizado pra gerar esse link.
- **Mascote (dados):** `/turmas/<t>/alunos/<a>/dados/mascote` = { tipo, nivel, paradas, nascido_em }.
- **HONESTO:** mascote é EMOJI por enquanto (🐣🐉🦊...); a versão desenhada que cresce de
  verdade (arte por estágio) vem depois, via asset studio. Marcos é o professor E o admin
  (um usuário só). Enquanto a fábrica não é perfeita, a "equipe que conserta" sou eu (Claude).

## 🐾 VERSO vira FAMÍLIA (vários tipos, 1 esqueleto só) — (Marcos, 2026-07-17)
Marcos: "se é fácil assim, não seria melhor vários pra escolher?" (a dúvida da dificuldade
era porque achou que o mascote ocuparia o lugar do robô/animação pesada). Como o robô FICA
e o Verso é leve (vetor, flutua/pula), dá pra ter VÁRIOS — regra: **família que COMPARTILHA
o mesmo corpo/olhos/animação**; muda só a "cabeça" (orelha/chifre/crista/bico) + a cor. 6
tipos provados em SVG: gatinho, coelho, ursinho, dino, passarinho, chifrudo. A criança
escolhe TIPO + COR; + estágios (fofo→descolado, atende 1º ao 9º) + acessórios por mundo.
Bichos TOTALMENTE diferentes (polvo×dragão, animações próprias) continuam PROIBIDOS (pesado).
- **Byte NÃO some:** vira guia/morador dos mundos (dá as missões). Mascote = personagem do ALUNO.
- **Modelo de operação (Marcos):** "comando tudo do painel, mas a EQUIPE (Claude) está sempre
  aqui — é onde produzimos e melhoramos tudo". Painel = controle; sessão = oficina.
- **Verso é SVG paramétrico** (recolor=1 valor; roda em qualquer navegador, IE9+/Chrome/Firefox,
  sem lib, offline). Vira ator do motor de personagem vivo. Gerador guardado em /tmp (versos.html).

## 🚨🚨 CURA DEFINITIVA DO "BASE VELHO" (perda recorrente de tempo/créditos) — 2026-07-17
PROBLEMA (aconteceu de novo, Marcos MUITO incomodado, com razão): o container volta com a
branch/working-tree numa BASE VELHA (3dc86eb "Vila do Miau"), e o remote-tracking `origin/...`
fica DESATUALIZADO apontando pra ela. Se eu rodo `git reset --hard origin/<branch>` confiando
nesse ref velho, APAGO a eduverse/ + trunco a MEMORIA. **Nada se perde no GitHub** (fonte da
verdade), mas eu gasto tempo/créditos recuperando SEMPRE. 
REGRAS DE OURO (obrigatórias, nunca furar):
1. **NUNCA** `git reset --hard origin/<branch>` sem antes `git fetch --force origin <branch>`.
2. **SEMPRE** conferir o tip REAL do GitHub por API (mcp github list_branches / get_file_contents)
   ANTES de qualquer reset. Se o `origin/...` local ≠ tip da API, ele está velho: fetch --force.
3. Ao restaurar: `git fetch --force origin <branch>` -> conferir `git ls-files eduverse | wc -l`
   (tem que dar ~72) e `wc -l MEMORIA` (~740+) -> só então seguir.
4. O hook `.claude/hooks/sync-remoto.sh` foi endurecido pra AUTO-restaurar no início da sessão
   (fetch --force + reset --hard pro tip real do GitHub) — assim isso vira automático, não manual.

## 🚀 PUBLICADO PRA TESTE (Marcos: "faça tudo, deixe pronto") — 2026-07-17
Tudo no ar via Fábrica (dispatch com ref=claude branch, source_dir por site):
- educaverso  -> https://vidalprof.github.io/educaverso/  (aluno; Verso integrado)
- painel-prof -> https://vidalprof.github.io/painel-prof/  (senha vidal2026; cria turmas/alunos + mundos/paradas)
- navio-pirata-> https://vidalprof.github.io/navio-pirata/  (atividade de numeros; 1a parada da Ilha)
Regras do Firebase republicadas pelo Marcos (agora cobrem /catalogo). semear-catalogo.yml (na main)
rodou OK (run 29576419440): semeou /catalogo/mundos/ilha-pirata (fogueira=jogavel, resto "em breve")
+ criou turma-mestra /turmas/teste (Ana/Bento/Clara). LINK DE TESTE: educaverso/?t=teste.
FASE SEGUINTE = LAPIDAR (Marcos: "depois verificamos e lapidamos"): estagios do mascote (fofo->descolado),
animacao viva do Verso (respira/pisca/pula), a Ilha completa (7 paradas com jogo/historia/vozes),
ajustar coordenadas das paradas na arte da ilha.

## 🌎🌎 VISÃO-MESTRA DEFINITIVA — EDUCAVERSO / EDUVERSE PROFESSOR AI (Marcos, 2026-07-17)
O "REAL MOTIVO" do projeto (Marcos revelou colando 2 prompts-mestres inteiros):
**PROBLEMA REAL:** o **Currículo de Computação** está entrando nas escolas. O professor de
Informática Pedagógica vira **Professor de Computação** com currículo próprio -> tem que produzir
planejamento, sequência didática, plano de aula, atividades plugadas E desplugadas, avaliação,
relatórios e documentação pra coordenação. Carga de trabalho INSUSTENTÁVEL. **Educaverso nasce pra
resolver isso.**
**MISSÃO:** transformar AUTOMATICAMENTE cada objetivo OFICIAL do currículo numa experiência completa
de aprendizagem, e gerar SOZINHO toda a documentação pedagógica (nos modelos oficiais da Secretaria).
O professor gasta tempo com os ALUNOS, não com papel.
**DUAS VISÕES (regra de ouro):** o PROFESSOR vê planejamento/objetivos/conceitos/avaliação/relatórios;
o ALUNO vê uma AVENTURA (cidade, missão, personagens, mistérios). Nunca documento escolar pro aluno.
**CURRÍCULO INVISÍVEL (princípio absoluto):** o aluno NUNCA sente que estuda. Nada de "Atividade 3 /
Exercício 5 / prova / questionário". Ele explora, constrói, investiga, resolve problemas do mundo.
O conceito é vivido, nunca anunciado. Ex.: prof="algoritmos simples"; aluno="o robô perdeu a rota e
precisa entregar remédios antes do pôr do sol". Aprende sem perceber.
**O MUNDO É O PROFESSOR:** o ambiente ensina; moradores perguntam; problemas surgem naturais; solução
vem da exploração. O professor vira MEDIADOR.
**UM ÚNICO MUNDO PERSISTENTE (não coleção de jogos):** o aluno volta SEMPRE ao mesmo lugar; tudo salvo;
NPCs lembram; construções permanecem. **A cidade cresce com o aluno** — cada objetivo aprendido muda o
mundo dele (casas, árvores, robôs, bairros); cada aluno tem uma cidade ÚNICA. **Jornada de 9 anos**
(1º ao 9º ano) no mesmo mundo, que envelhece junto.
**MUNDO VIVO:** NPCs andam/conversam/dormem/trabalham; animais com comportamento; clima, dia/noite,
chuva, vento, partículas, som. Meta máxima do projeto: o aluno AMAR VOLTAR -> "Professor, hoje tem
Educaverso?".
**AVALIAÇÃO INVISÍVEL:** o jogo OBSERVA (tempo, tentativas, persistência, estratégias, decisões, pedidos
de ajuda, erros/acertos, autonomia) -> gera avaliação diagnóstica+formativa + evidências, SEM prova.
**SEQUÊNCIA = 55min = 1 objetivo = 1 aula:** 5 intro narrativa / 35 missão / 10 desafio final / 5 síntese+
registro+avaliação. Nunca aventura longa.
**MECÂNICAS REUTILIZÁVEIS (não criar do zero):** programar robôs, construir pontes, automatizar fazenda,
organizar biblioteca, logística, cidade inteligente, semáforos, lab de dados, reciclagem... cada mecânica
atende DEZENAS de objetivos só trocando contexto/narrativa. Regiões: cidade, lab, oficina, biblioteca,
museu, porto, fazenda, floresta, mina, usina...
**MOTOR PEDAGÓGICO (por objetivo -> "Pacote Pedagógico" automático):** objetivo oficial + conceitos +
conteúdos + conhecimentos prévios + sequência + plano de aula + planejamento + metodologia + recursos +
avaliação + rubricas + missão digital + versão DESPLUGADA (mesmos objetivos, p/ sem internet) + relatório
individual + relatório da turma + diário do professor + registro coordenação + recuperação.
**BRAIN/ASSET STUDIO:** cérebro decide região/mecânica/missão/NPCs; biblioteca permanente que só cresce,
nunca duplica; personagens modulares (paper-doll) mesmo estilo; map builder automático.
**TECH:** HTML5/CSS/JS, Firebase, IA p/ narrativa+diálogo+DOCUMENTAÇÃO, modular, Win7/Chrome/Firefox,
1024x768, leve, online com export offline. (Obs: prompts citam Phaser; nós decidimos Canvas 2D por peso.)

### HONESTIDADE — onde estamos vs. essa visão (Claude, 2026-07-17)
O que existe hoje = INFRAESTRUTURA (login por toque, ovo/mascote Verso, mapa de mundos/paradas, Firebase
salvando progresso, painel do professor) + UMA atividade de MATEMÁTICA (números até 30, pirata) que é
"mais do mesmo" (exercício gamificado). A ALMA da visão (currículo INVISÍVEL de COMPUTAÇÃO, mundo-professor,
cidade persistente que cresce 9 anos, avaliação invisível -> documentação automática) ainda está À FRENTE.
As pernas difíceis JÁ PROVADAS: IA gera conteúdo (Gemini) e dados (Firebase) — são exatamente os motores
que essa visão precisa p/ auto-documentação e avaliação invisível. Caminho realista = 1 FATIA VERTICAL
honesta num objetivo de COMPUTAÇÃO (ex.: algoritmos/sequência) que prove a filosofia ponta a ponta:
problema do mundo -> aluno resolve vivendo -> avaliação invisível -> Pacote Pedagógico gerado pro professor.
NÃO prometer a plataforma inteira de uma vez (é roadmap de anos); provar a filosofia numa fatia real primeiro.

### DECISÃO DE CENA (Marcos, 2026-07-17): paradas numa ILHA no meio do oceano; a ÚLTIMA fase é um NAVIO
(como o que ficou bonito). O convés repetido/câmera 3/4 dava "paredes/imagens coladas" -> ilha resolve.

## 🎨🌱 SPEC DEFINITIVA DO MUNDO VIVO — "EDUCAVERSO EXPERIENCE ENGINE" (Marcos, 2026-07-17)
Marcos quer o MUNDO VIVO (é o diferencial da ideia) e perguntou "tem como ser mais fácil e bonito
igual?". Colou a spec-mestra do mundo vivo. RESPOSTA: SIM — a própria spec é a receita. Princípios:
- **MÉTRICA DE SUCESSO:** criança perguntar "Professor, hoje tem Educaverso?". Beleza NÃO vem de
  gráfico caro — vem de **CONSISTÊNCIA** (tudo do mesmo "estúdio") + vida + som + rotina + eventos.
- **REGRA DE OURO ANTI-BUG (bate com nossos erros):**
  (a) **NUNCA gerar mapa/cena inteira com IA** (gera inconsistência) — foi o erro do tile "conves"
      cheio de viga (parede repetida / "imagens coladas").
  (b) IA gera **só RECURSOS individuais** (árvore, casa, robô, item), salvos numa **BIBLIOTECA
      PERMANENTE** que só cresce e nunca duplica. Antes de criar: "já existe? reutiliza".
  (c) O **BUILDER** monta a cena AUTOMÁTICO a partir da biblioteca (chão simples + assets colocados
      por cima). Chão simples/seamless = tiling invisível; a riqueza vem dos ASSETS variados colocados,
      não de um tile detalhado repetido.
- **VIDA PROCEDURAL (não animar mil coisas à mão):** REGRAS simples geram milhares de comportamentos —
  árvore balança, água mexe, fumaça sobe, borboleta voa, pássaro muda direção, cão passeia, gato dorme
  ao sol, robô trabalha, morador tem rotina. + **EVENTOS ALEATÓRIOS** (carteiro, balão, chuva, feira,
  navio atracando) só pra surpreender.
- **MUNDO COM MEMÓRIA + CIDADE EVOLUTIVA:** plantou árvore fica; ponte fica; morador lembra. Cada aluno
  começa com um terreno e a cidade cresce a cada objetivo — cada aluno tem cidade ÚNICA. Jogo não acaba;
  cada aula = novo capítulo (o que mudou? quem chegou? quem precisa de ajuda?).
- **MÓDULOS:** Asset Factory (só recursos reutilizáveis, ex. 200 árvores), Diretor de Arte IA (decide
  paleta/luz/hora/clima/qtd NPCs/som — mantém coerência), Builder automático, Educaverso Director AI
  (pergunta sempre "como deixar mais vivo?" respeitando performance).
- **PERFORMANCE:** Win7/Chrome/Firefox, 1024x768, pouca memória, animações leves, REUSO máximo.
- **RECONCILIAÇÃO com o que o Claude tinha sugerido:** eu tinha proposto "imagem única coesa por cena";
  a spec do Marcos é MELHOR pro objetivo vivo/evolutivo/consistente -> **chão simples + biblioteca de
  assets colocados + vida procedural**. O "flat ground" que comecei encaixa nisso (chão simples). Fim
  do tile busy e do mapa-IA. Obs: spec cita Phaser; princípios valem em Canvas 2D (nosso, mais leve).
- **ESCOPO HONESTO:** isso é um SISTEMA (biblioteca + builder + vida procedural + memória + cidade),
  build grande — a FUNDAÇÃO certa do mundo vivo, não remendo. Caminho: 1 CENA-PROVA (chão simples +
  poucos assets coerentes + vida procedural: pássaro/fumaça/personagem respirando) SEM bug, e crescer.

## 🏛️ ARQUITETURA TÉCNICA (a "outra IA" mandou) — avaliação honesta (2026-07-17)
Marcos colou um doc GRANDE de arquitetura feito por outra IA. REGRA-MÃE dele: **a IA gera DADOS
estruturados; o Educaverso EXECUTA código/mapas/mecânicas/componentes JÁ TESTADOS.** IA nunca escreve
um jogo inteiro do zero por objetivo. STACK proposto: React+TS (painel), Node+TS (Orquestrador),
IA c/ saída estruturada (JSON Schema/Zod + validação/rejeição), Educaverso Builder (templates+regras+
mecânicas), **Phaser** (motor), **Tiled** (mapas JSON), Firebase (auth/db/storage/hosting), Vitest+
Playwright+ESLint+CI (testes). Mecânicas reutilizáveis CONFIGURÁVEIS (ex. "ordenar_comandos" vira robô/
carteiro/receita só trocando contexto). Biblioteca de assets c/ metadados + Guia de Arte. Vida procedural
por comportamento. Eventos aleatórios. Som em camadas. Avaliação invisível -> docs automáticos. Modos
completo/econômico/ULTRALEVE (Canvas quando preciso). Offline/cache, missão gerada ANTES da aula (não
chamar IA durante). Validador técnico + pedagógico antes de publicar. Prévia do professor. 9 etapas de
desenvolvimento. Regra de ouro: IA sugere -> validador confere -> builder monta -> testes -> professor
revisa -> publica.

AVALIAÇÃO (Claude, honesto):
- **CONVERGE com tudo que a gente decidiu** (dados-não-código, reuso, biblioteca, vida procedural,
  consistência de arte, avaliação invisível, não-IA-na-aula, offline, docs automáticos). As visões batem
  = ótimo sinal.
- **A DIFERENÇA REAL é o STACK:** React+TS+Phaser+Tiled+Node+Vite+CI = **produto de software profissional**
  (meses, equipe, backend, build, hospedagem). É o jeito certo PRA UM PRODUTO que escala p/ muitas escolas
  e 9 anos. Mas é MUITO mais pesado que o nosso atual (HTML único no GitHub Pages, sem build, Canvas leve).
- **Tensão técnica:** Phaser+TS+build briga um pouco com "HTML único offline p/ Win7 sem instalar" (nosso).
  Phaser roda no navegador, mas some a simplicidade do arquivo único.
- **RECOMENDAÇÃO:** usar esse doc como **MAPA DO DESTINO**; adotar os PRINCÍPIOS AGORA no jeito leve (que
  já faz muito disso); migrar pro stack pesado só quando/se virar produto de verdade (com tempo/equipe).
  Um professor sozinho não toca React+TS+Phaser+Node+CI E dá aula — e o Marcos quer MENOS trabalho.
- O protótipo atual (praia viva + missão "ordenar passos" + narração + som, Canvas ultraleve) já aplica
  boa parte do doc: mecânica reutilizável configurável, vida procedural, avaliação embutível, offline.

## 🏗️ PLANO A INICIADO (stack profissional, À PARTE) — Etapa 1 no ar (2026-07-17)
Marcos escolheu o PLANO A (stack pesado do doc de arquitetura). Pediu: "não delete nada, faça
à parte, deixe o modelo leve como está pra acessar quando quiser". Feito:
- **educaverso-app/** (no repo, branch de trabalho): projeto **Phaser 3.80 + TypeScript + Vite**.
  src/main.ts = Etapa 1 (Núcleo técnico): personagem anda no mapa, câmera segue, colisão com água,
  passarinho de vida. tsconfig strict=false (afrouxado pro 1º build), vite base './' + target es2017
  (compat. navegador antigo atualizado).
- **.github/workflows/app-build.yml** (na main = dispatchável): npm install + vite build -> publica o
  dist num repo SEPARADO **educaverso-app** via PAGES_TOKEN + liga Pages. NÃO toca no modelo leve.
- **BUILD PASSOU DE PRIMEIRA** (run 29581472602 SUCCESS): prova que o stack profissional inteiro
  (npm/Vite/Phaser/deploy) é construível e publicável DAQUI, de graça, via GitHub Actions.
- Link do app: **https://vidalprof.github.io/educaverso-app/** (Pages leva 1-2 min na 1ª vez).
- HONESTO: NÃO consegui screenshotar o app no ar (o Chromium do sandbox não alcança sites externos
  pelo proxy — ERR_TUNNEL). Build+deploy confirmados pelo status do workflow; a validação visual é o
  Marcos abrir no navegador dele.
- Modelo leve INTACTO no ar: educaverso, painel-prof, navio-pirata, ilha-dos-passos, atividades.
- PRÓXIMAS ETAPAS (ordem do doc): Etapa 2 mecânica "ordenar comandos" (com avaliação) -> Etapa 3 mundo
  vivo (NPCs/rotinas/clima) -> Etapa 4 painel React -> Etapa 5 IA estruturada (JSON Schema/Zod) ->
  Etapa 6 Builder -> Etapa 7 avaliação -> Etapa 8 documentação -> Etapa 9 expansão.

## 📌 PENDÊNCIA (Marcos, 2026-07-17): DOCUMENTO ÚNICO com TODA a sequência
Quando o Marcos DER O SINAL (não antes): reformular TUDO (as visões-mestras, a arquitetura, as
decisões, as etapas) num **documento só**, organizado, com **toda a sequência** de desenvolvimento
do Educaverso. É consolidação — esperar o "agora pode" do Marcos.

## 🧩 ETAPA 2 iniciada — mecânica "ordenar comandos" no app Phaser (2026-07-17)
Marcos deu "pode fazer". Construindo no educaverso-app (Plano A): a mecânica REUTILIZÁVEL
"ordenar comandos" (algoritmo) numa cena única bonita (praia noturna). Criança monta os passos ->
Verso anda de célula em célula até o baú, desviando das poças -> conceito "ALGORITMO" no fim ->
avaliação invisível começa a registrar (tentativas/tempo/acerto em localStorage; Firebase depois).
Mira Chrome 109 (moderno). Config da mecânica separada (reutilizável p/ virar missão no mundo OU
atividade avulsa premium).

---

## [2026-07-17] Configuração REAL dos PCs da escola (alvo de hardware confirmado)

O Marcos enviou a tela de sistema de um PC da escola. **É este o hardware que
tem que rodar liso** (não é hipótese, é o alvo real):

- **CPU:** AMD FX-4300 Quad-Core 3,8 GHz (2012, arquitetura Bulldozer/Piledriver — fraco por núcleo)
- **RAM:** **3583 MB (~3,5 GB)** ← o gargalo mais sério
- **SO:** Windows 7 64 Bits
- **Navegador:** Chrome 109 (o último que roda no Win7)

### O que isso confirma / exige (regras de projeto)
- **RAM baixa (3,5 GB) é o limite crítico.** Win7 + Chrome já comem boa parte.
  → Texturas PEQUENAS e desenhadas 1x só (canvas via `textures.createCanvas`),
    nada de spritesheets gigantes, nada de segurar muitos assets na memória.
  → Uma cena por vez; liberar o que não está em uso.
- **CPU fraca por núcleo** → manter `fps.target: 30`, `antialias:false`,
  `powerPreference:'low-power'`, `roundPixels:true`, poucas tweens simultâneas.
- **Scale FIT 1024×768** continua certo (resolução baixa = menos pixels a
  desenhar = menos GPU/RAM).
- Chrome 109 é moderno (ES2022/WebGL2) → pode usar ferramenta moderna SEM
  gambiarra; o problema nunca foi o padrão da linguagem, é o PESO em RAM/CPU.
- **Teste de aceitação:** toda etapa nova tem que ser testada NO PC do Chrome
  109 (o do Marcos) antes de considerar pronta.

### [2026-07-17] Navegadores REAIS da escola (alvo de build definitivo)
O Marcos confirmou os dois navegadores usados nos PCs da escola:
- **Chrome 109.0.5414.120** (o último do Win7)
- **Firefox 106.0.5 64 bits** ← ATENÇÃO: é MAIS ANTIGO que o 115.

→ No `educaverso-app/vite.config.ts` o alvo do build tem que ser
  **`target: ['chrome109', 'firefox106']`** (NÃO firefox115 — o 106 é anterior;
  usar 115 faz o Vite gerar sintaxe que o Firefox 106 não entende).
Ambos suportam ES2022, então o `tsconfig target ES2022` continua ok.
Teste de aceitação de toda etapa: rodar nesses DOIS navegadores da escola.

---

## [2026-07-17] DUAS REGRAS DE OURO reafirmadas pelo Marcos (Etapa 2 → correção de rumo)

O Marcos testou a Etapa 2 ("Ajude o Louro"): **rodou**, mas ele lembrou de dois
pontos que são LEI do projeto e eu não podia ter deixado passar:

### REGRA 1 — VOZ: SEMPRE por API (voz "Antonio"), NUNCA pelo navegador
- **PROIBIDO** usar `Web Speech API` (`speechSynthesis` / `SpeechSynthesisUtterance`)
  do navegador. Nada de `fala()` que usa o sintetizador do Chrome.
- A voz TEM que ser **gerada por API** (Edge TTS, voz **pt-BR "Antonio"** =
  `pt-BR-AntonioNeural`) por **WORKFLOW do GitHub** (`gerar-audio.yml`), que
  produz **arquivos de áudio** (mp3/ogg). O app só **toca o arquivo pronto**.
- Motivo: a voz do navegador é robótica, muda de PC pra PC, às vezes nem existe;
  a voz por API é sempre a mesma, natural e coerente com o EduVerso. Todo asset
  que a criança ouve é gerado (mesmo princípio de "todo asset visto é IA").
- **Aplicar em TUDO** (app Plano A, atividades, hub). Refatorar a Etapa 2 pra
  tirar o Web Speech e tocar os áudios do Antonio.

### REGRA 2 — O norte é o MUNDO VIVO EXPLORÁVEL 2D (ensinar diferente)
- A Etapa 2 é uma boa MECÂNICA (ordenar comandos), mas ela virou uma "tela de
  puzzle" isolada. **Não é isso** o diferencial. O diferencial é o **mundo vivo
  2D explorável**: a criança ANDA pelo mundo, encontra os problemas no contexto,
  e a mecânica aparece DENTRO do mundo (não como uma telinha à parte).
- A mecânica continua sendo peça reutilizável — mas o invólucro é o mundo vivo.
- Próximo passo real = **Etapa 3**: mundo explorável (andar livre, NPCs, o
  problema no lugar), com a mecânica de algoritmo acontecendo lá dentro.

---

## [2026-07-17] NASCEU O `EDUCAVERSO-UNIFICADO.md` — o documento ÚNICO (fonte da verdade)

O Marcos pediu: "reúna-se com os profissionais e redija um documento único do
educaverso com tudo de novo, agora podemos utilizar tecnologia moderna, una o
melhor das duas ideias". Feito, com a sessão no modelo mais forte (Fable).

- **`EDUCAVERSO-UNIFICADO.md`** (raiz) = FONTE ÚNICA DA VERDADE. Em conflito
  entre documentos, ELE manda. Os antigos (EDUCAVERSO.md, EDUVERSE-*, eduverse/)
  ficam como referência/memória — NADA foi apagado (decisão do Marcos).
- Conteúdo: propósito real (2027, coordenadora, 55 min) · Lei pedagógica
  (Portão 0 verbatim) · Mundo vivo + Verso + avaliação invisível · Currículo
  de Computação (eixos PC/MD/CD, objetivo→missão) · Estúdio profissional
  (Phaser+TS+Vite; IA gera DADOS validados, motor executa) · hardware real
  (FX-4300/3,5GB/Win7/Chrome109/Firefox106) · Arte & Som (voz Antonio LEI;
  revogada a ressalva speechSynthesis do PLANO-FABRICA) · Equipe + Portões ·
  Sustentabilidade · Estado honesto · ROADMAP ÚNICO (9 etapas; Etapa 3 =
  mundo vivo explorável = PRÓXIMA, decisão do Marcos) · Regras permanentes.
- **DECISÃO (pergunta do Marcos): não escrevemos mais motor próprio.** O motor
  é o Phaser; os artesanais (kit-floresta.py, build_premium.py, build_taberna.py)
  estão APOSENTADOS para desenvolvimento novo (ficam como referência e servindo
  o modelo leve publicado). Levamos deles o aprendizado + o contrato de dados.
- **`MANUAL-MESTRE.md` atualizado** (seção datada no topo): aponta o doc único;
  estúdio moderno disponível p/ premium SÓ se o Marcos pedir (molde clássico
  continua padrão); alvo real de máquina; reforço da voz Antonio.
- Próximo build: **Etapa 3 — mundo vivo explorável no estúdio, já com a voz
  do Antonio desde o nascimento** (escolha explícita do Marcos).

### [2026-07-17] Lições da fábrica de assets (Etapa 3)
- **Voz "Donato" (pt-BR-DonatoNeural) QUEBROU no edge-tts** (todas as falas
  falharam; o Antonio, no mesmo minuto, funcionou). A voz parece ter saído do
  catálogo da Microsoft. → Personagens usam **Antonio** até validar outra voz;
  testar 1 fala antes de mandar lote com voz nova. Amostra Gemini TTS também
  falhou (cota/modelo) — tentar de novo depois, sem bloquear produção.
- **Pollinations à noite adora pintar uma LUA solta** no quadro do asset →
  o recorte local (Pillow) guarda SÓ o maior objeto conexo + preenche buracos
  internos (sombras escuras viravam furos) + apaga a faixa do céu se precisar.
  Script: scratchpad/recortar_ilha.py (recriar se preciso: limiar ~14-34,
  maior componente, dilata 2px, alpha gradual anti-franja, autocrop, resize).
- **"Baú fechado" veio aberto** na 1ª geração → prompt teve que gritar
  ("lid COMPLETELY CLOSED, sealed, no opening"). Portão de Arte pegou. Sempre
  OLHAR cada imagem antes de integrar.
- **QA visual automatizado no CI:** o `app-build.yml` agora tira screenshots
  headless (`?qa=inicio` / `?qa=missao`) e commita em `_qa/` — o Portão 1
  ganhou olhos dentro do próprio build.

### [2026-07-17] REGRA DE OURO do Marcos (não pode quebrar): NADA À MÃO, TUDO PROFISSIONAL
No app Plano A (mundo vivo, educaverso-app), tudo o que a criança VÊ é feito por
tecnologia profissional — NUNCA desenhado por código à mão:
- **Cenário/fundo, água, personagens, objetos = imagem de IA** (Pollinations/Gemini),
  recortadas e otimizadas. Proibido "pintar por canvas" o que é ARTE que a criança vê.
- **Vida/animação = sistemas do motor Phaser** (partículas, tweens, luzes) — não
  partícula/efeito feito na unha.
- **Colisão = física do Phaser (Arcade Physics)** — não colisão manual por clamp.
- **Texto nítido** = `setResolution` (motor), não aceitar borrado.
- Exceção tolerada: primitivas de efeito do motor (sombra suave, brilho, pontinho de
  partícula) e um RESERVA invisível (só se um asset 404, pra nunca dar tela quebrada).
- **Pesquisar sempre o mais moderno/grátis que caiba no PC da escola** (FX-4300/3,5GB/
  Chrome109). Ex.: animação de personagem viva = runtimes esqueléticos (DragonBones grátis,
  Spine, Creature/CreaturePack p/ Phaser) — porém exigem RIG uma vez num editor (passo
  humano); não há botão mágico "1 imagem -> anda em 4 direções" grátis e automático.

### [2026-07-17] CAIXA DE FERRAMENTAS + pipeline de PERSONAGEM ANIMADO (automático, eu controlo)
O Marcos pediu: só ferramentas que EU controlo e gero TUDO automático (sem site/upload manual).

**Caixa de ferramentas (tudo grátis/viável no PC FX-4300/3,5GB/Chrome109, eu opero por workflow):**
- Motor: **Phaser 3** (render/física/animação). NÃO trocar — Phaser não é o problema.
- Arte cenário/objetos: **Pollinations/Flux** (grátis).
- Arte consistente / poses / recorte: **Gemini image** (centavos) editando a ÂNCORA — funciona headless via `gerar-imagens.yml` (input `base`).
- Voz: **edge-tts Antonio** (grátis). Som: Web Audio + CC0 (Kenney/Freesound).
- Mapas: Tiled. Dados validados: Zod/JSON-Schema. Save: Firebase. Build/deploy: Actions+Pages.
  Testes/QA: Vitest+Playwright (já uso screenshots no CI). Offline: Vite PWA. Painel: React.
- **Sites de sprite (AutoSprite/Spritesheets.ai): NÃO uso** — GUI, sem API grátis que eu dirija.

**PIPELINE DE PERSONAGEM ANIMADO (PROVADO que funciona — "cartela de poses como a gente fazia"):**
1. Âncora do personagem (ex.: `_novo/ilha_verso_azul.png`).
2. `gerar-imagens.yml` modelo=gemini, base=âncora, prompt "Keep the EXACT same character... redraw in POSE X, isolated on solid pure black background". Gemini MANTÉM o personagem (testado: verso_passo_a/b/c, verso_feliz).
3. Recorte automático (Pillow: fundo preto->transparente, maior componente, buracos, autocrop) + NORMALIZAR base dos pés + mesmo tamanho de canvas por quadro.
4. Phaser: sprite com animação (idle sutil; walk = alterna quadros de passo; feliz na vitória).
   -> personagem VIVO de verdade, automático, sem site.

**ERROS a não repetir (feedback do Marcos):**
- NUNCA esticar arte (fundo esticado = distorcido = "horrível"). Usar aspecto NATIVO.
- NÃO misturar perspectivas (poça vista de CIMA + praia vista de LADO = parece colado).
  Cena coerente: ou tudo top-down (estilo JRPG, sprites de frente) OU tudo de lado. Decidir e manter.
- Personagem = cartela de poses animada (NÃO 1 imagem estática com "esticadinho").

---

## Nome do aluno vem do CADASTRO no Firebase (decisão registrada — 2026-07-18)

O Marcos lembrou: **na atividade de verdade, o nome do aluno vai estar no Firebase,
nos cadastros da turma.** Isso já está montado:
- Modelo: `/turmas/<turma>/alunos/<aluno> = { nome, progresso, ... }` (`eduverse/lib/eduverse-save.js`).
- `_painel-prof/` já lista os alunos da turma (`EduSave.listarTurma`).

**Consequência boa para a VOZ do Byte falar o nome:**
- Como os nomes da turma são **conhecidos de antemão** (estão no cadastro), dá pra
  **gerar o áudio EXATO de cada aluno matriculado** (mesmo nome raro), rodando o
  workflow `[audio]` uma vez com a lista da turma → **100% de cobertura**.
- O **banco de 124 nomes comuns** (já gerado, voz Antonio, em `_voxel/audio/nome_<slug>.mp3`)
  continua como **rede de segurança** (nome digitado na hora / turma sem cadastro / visitante).
- Voz SEMPRE por API (edge-tts Antonio), NUNCA voz do navegador.

**LGPD (criança):** cadastro guarda o MÍNIMO — primeiro nome + código/apelido +
pontuação/progresso. Nunca dado pessoal completo.

**PENDENTE (decidir DEPOIS — o Marcos disse "depois pensamos nisso"):** como o aluno
se identifica pra entrar — (a) escolher o nome na lista da turma, (b) digitar um
código/matrícula, ou (c) continuar digitando o nome. Não decidir sozinho.

---

## 🔊 O Byte FALA o nome do aluno — GANCHO PRONTO e REUTILIZÁVEL (2026-07-18)

Feito e **no ar** na aventura voxel (`_voxel` → `ilha-voxel-teste`). É o gancho de
engajamento #1 do `_plano/plano_engajamento.md` ("o NPC lembra o nome") **elevado**:
antes o nome só aparecia no texto; agora o personagem **fala o nome de verdade**.

**Como funciona:**
- **Banco de 124 nomes** comuns de criança, gravados na **voz do Antonio**
  (`pt-BR-AntonioNeural`, edge-tts, via workflow `[audio]`). ~9 KB cada.
- **Mestre canônico:** `eduverse/vozes/nomes/` (+ lista `eduverse/vozes/nomes-banco.json`).
  Em uso no jogo: `_voxel/audio/nome_<slug>.mp3`.
- **Helper plug-and-play:** `eduverse/lib/voz-nome.js` (`window.VozNome`: `idDe(nome)`,
  `slug()`, `cadeia([...], aoFim)`). Manual: `eduverse/vozes/LEIA-ME.md`.
- **slug** = 1º nome, `NFD` sem acento, minúsculo, só `a-z0-9` (igual ao que o workflow
  gera). Ex.: "Cauã" → `nome_caua`.
- **Cadeia de voz sem cortar:** `nome → saudação → problema`. Nome no banco → saudação
  **sem apelido** (`vx_ola_nome`/`vx_voltou_nome`); nome fora do banco → saudação
  **genérica** com "grumete" (`vx_ola`/`vx_voltou`). Senão vira "Marina!… Ôa, grumete!"
  (soa como 2 pessoas) — foi feedback do Marcos, corrigido.
- **Voz SEMPRE por API. NUNCA a do navegador** (`SpeechSynthesis` proibida).

**BUG achado e consertado na raiz (auditoria antes do Marcos):** a saudação tocava
**2×** e na 2ª caía no genérico. Causa: em falha de rede (Firebase bloqueado), o
navegador dispara `onreadystatechange` (status 0) **E** `onerror` → o callback do
`EduSave` rodava 2× → `montarParada` montava 2×. Conserto: **trava anti-duplo no `_xhr`**
(`pronto=true` na 1ª; vale p/ `_voxel/eduverse-save.js` E `eduverse/lib/eduverse-save.js`)
+ **start idempotente** no jogo (`comecou`). QA render (Playwright headless) confirmou:
Marina/Cauã → `nome_x`+`vx_ola_nome` (1×); nome fora do banco → `vx_ola` (1×).

**Expandir o banco:** nomes em `_lote_falas.json` (`{id:"nome_<slug>",texto:"<Nome>!"}`)
→ commit `[audio]` → `cp _audio/nome_*.mp3` pro mestre e pro projeto → atualizar o set
em `voz-nome.js` + `nomes-banco.json`. **Melhor:** gerar a voz EXATA da turma pelo
cadastro do Firebase (100% de cobertura).

## 🧲 PADRÃO: todo projeto deve ter os ganchos de engajamento (decisão do Marcos, 2026-07-18)
"Todos os projetos devem ter essas melhorias para ficarem bem atrativos para os
estudantes." Virou **padrão obrigatório** no `EDUCAVERSO-CHECKLIST-DE-CENA.md`
(seção "Ganchos de Engajamento"): (1) falar o nome, (2) o mundo lembra/retoma,
(3) progresso visível + coleção, (4) novidade a cada volta, (5) autonomia. O Auditor
barra o que não tiver ≥ #1 e #2. **Status de adoção:**
- ✅ `_voxel` (Ilha das Trinta Moedas): #1 e #2 prontos.
- ⬜ `educaverso-app` (2D/Phaser), atividades **premium** e hub **Ilhas do Saber**:
  PENDENTE aplicar (helper `voz-nome.js` já pronto pra plugar). Registrar aqui conforme adotar.

---

## 🚢 VISÃO DO MARCOS: mundos CONECTADOS por travessia (não "corta" pra próxima fase) — 2026-07-18

Ideia do Marcos (direção de design pra TODAS as aventuras, não só a voxel):
- **Continuidade física entre fases:** em vez de terminar uma fase e a cena "cortar"
  pra outra, a criança **VIAJA** — vai de **barco** (ou **ponte**) até a próxima ilha.
- **A matemática CONSERTA o mundo (o problema vem primeiro, filosofia EduVerse):** ex.
  fase 1 — o navio está parado, ancorado, **afundando pelos furos**. A criança conta os
  **cocos** e, **a cada coco contado, um furo é tapado** → o barco conserta na frente dela.
  Só com o barco consertado dá pra **zarpar pra próxima ilha**.
- **Item + NPC (o loop):** resolver o problema dá um **item**; **outro personagem** (o
  Pinça / o que conserta o barco) **recebe o item e conserta o barco**. Aí libera a viagem.
- **As ilhas já estão no mundo, VISÍVEIS (no horizonte):** a criança VÊ pra onde vai e
  **conquista o caminho** resolvendo problemas/coletando — é o "mistério visível-mas-
  trancado" (`_plano/plano_engajamento.md` §2.5, "a ponte que abre o bairro"). Bate 100%
  com a nossa bíblia de design.
- **Por que diferencia:** a maioria dos jogos "educativos" é *pergunta → próxima tela*.
  Aqui é *problema do mundo → a conta CONSERTA o mundo → você VIAJA → a história continua*
  = vira "novela que eu acompanho", não prova. É o EduVerse puro ("aprende porque o
  MUNDO PRECISA").

**Honestidade técnica (pra não prometer o impossível no PC da escola):** mundo aberto
100% contínuo (andar sem cortes entre todas as ilhas) é pesado. O mesmo SENTIMENTO se
entrega leve com: (a) a contagem consertando o barco furo-a-furo; (b) uma **transição de
navegação curta** (o barco desliza pela água até a ilha seguinte, que já estava no
horizonte); (c) o NPC recebendo o item e consertando. Prototipar fase 1→2 primeiro, ver,
iterar, depois espalhar pras 5. **Vira padrão dos mundos EduVerse** (registrar no checklist
quando o protótipo aprovar).

---

## 🚢 Travessia fase 1→2 — PROTÓTIPO construído + iteração de arte (2026-07-18, cont.)

O Marcos aprovou "fazer a travessia ficar boa de verdade". Estado atual (no ar em
`ilha-voxel-teste`):
- **A contagem CONSERTA o barco:** cada coco contado **voa em arco até o barco e tapa
  um furo** (`cocoVoaProBarco`→`tapaFuro`); o barco **sobe e se desendireita** furo a
  furo. 5 furos, 6 cocos → sobra 1 (bate com a comparação EF01MA03). A criança VÊ a
  conta consertar (era o principal: antes o conserto ficava no canto, invisível).
- **Câmera vai ao barco no fim** (`olhandoBarco`, ângulo médio/de cima) pra ver o
  conserto + o **Pinça** (caranguejo) comemorando de perto.
- **Barco com mastro/vela/bandeira** (parece barco); **Pinça separado do barco** (não
  vira "blob"), pequeno e limpo.
- **Navegação limpa:** o Verso embarca e o barco **acelera pro mar aberto** (`pr²`),
  deixando a ilha de casa pra trás (fim do "paredão verde"), fade → chega na Parada 2.

**Feedback do Marcos (registrado p/ não repetir):**
- Áudio do nome vinha **cortado** → 200ms de "respirada" entre nome→saudação→problema.
- **"Grumete" repetia** (saudação com nome + fala do problema abrindo com "grumete") →
  fala do problema da fase 1 regravada SEM "grumete".
- "Não vi o barco na fase" → cocos voadores + câmera no fim resolvem.
- "Visual/dinâmica não muito legal" → dinâmica melhorou muito; **arte voxel de perto é
  o ponto fraco** (crab/barco "quadradões" no close). LIÇÃO: de longe o voxel engana
  bem, de perto aparece o blocado → preferir enquadramento médio/de cima; o Marcos é o
  diretor de arte, iterar arte às cegas por screenshot é lento.

**PENDENTE:** (a) ilha 2 visível no horizonte (removida — renderizava como "paredão");
(b) refino de arte do Pinça e do barco com o olho do Marcos; (c) espalhar a travessia
pras fases 2→5 SÓ depois do Marcos aprovar o feeling da 1→2.

---

## 🎨 VIRADA DE FORMATO: 2D ILUSTRADO (IA) + imagem/CSS = lindo, reconhecível, leve e SEM bug (2026-07-18)

Depois de muita conversa com o Marcos (voxel quadradão → 3D fofo → e a dor real: "criar o
mundo, código coerente, sem bug; e 2D/3D deram bug"), chegamos à **fundação**:

**FORMATO OFICIAL das atividades EduVerse (recomendado):**
- **Arte:** a **IA DESENHA** tudo (cena, objetos, personagem) — via workflow `[imagens]`
  (Gemini). Fica lindo e **reconhecível** ("o barco parece barco" porque é desenho, não
  cubo que eu monto). Provado: `_novo/cena2d_ilha`, `barco2d`, `coco_claro`, `byte2d`.
- **Montagem:** **1 HTML + IMAGEM + CSS** (DOM). **Sem three.js, sem física, sem Phaser,
  sem build.** A tecnologia mais à prova de bug que existe. Roda em qualquer PC da escola.
- **Recorte:** só **imagem INTEIRA** (fundo branco→transparente, flood da borda). **NUNCA
  cortar personagem em membros pra animar** (foi a fonte nº1 dos bugs — braço sumindo).
- **VIDA/animação:** vem de **CSS/JS** (bob, sway, squash, "respira", Byte pula/reage,
  confete, +1, brilhos flutuando). Fácil e **não buga** (ao contrário do sprite rigado).
  Responde o medo do Marcos: **2D ilustrado NÃO é parado.**
- **Dado, não código:** posições/quantidade/tema/objetivo BNCC = **dado**. Atividade nova
  = trocar o dado. **Um motor, currículo infinito, controlado pelo Marcos.**

**Provas no ar:** `ilha-2d-lindo` (2D ilustrado vivo) — o Marcos aprovou o visual; pediu
objetos mais reconhecíveis (feito: coco fibroso com folhinha) e temeu "sem vida" (feito:
tudo animado por CSS). Também existe `ilha-3d-fofo` (3D arredondado) como alternativa,
mas o 2D ilustrado ganhou em beleza+reconhecimento+baixo-bug.

**Por que isso mata os bugs:** motor simples (imagem+CSS) + arte inteira (sem recorte de
membro) + dado (não código) + Auditor (render/E2E). Bug some porque as partes frágeis
(física, recorte de pose, framework com build) **saíram**.

**Assets 2D já prontos** (em `_novo/`, recortados em `_2d/img/`): cena da ilha, barco,
coco (fofo e claro), Byte passarinho pirata. Reaproveitáveis.

**PRÓXIMO PASSO combinado a decidir:** transformar o teste na 1ª atividade real ("Números
até 30" completa nesse formato, com nome falado + mundo que lembra), OU o Marcos joga e dá
o veredito antes. NÃO espalhar sem ele aprovar o feeling.

---

## 🎮 ENGINE OFICIAL DOS JOGOS EXPLORATÓRIOS: Phaser 3 (decisão do Marcos, 2026-07-18)

O Marcos assumiu o papel de Diretor Técnico e definiu diretrizes profissionais (física
NATIVA da engine — nada de colisão na mão; FSM de animação; sprite sheet + FPS; LERP;
camadas/máscaras de colisão; WebGL/HTML5). Testamos as ferramentas:
- **Godot/Unity: INVIÁVEL no meu ambiente** — não instalados e o **proxy bloqueia o
  download (403)**. Godot só rodaria na máquina do Marcos, e o **export WebGL do Godot 4
  é pesado demais pro PC velho da escola (FX-4300)**. Descartado.
- **Phaser 3: ESCOLHIDO.** Engine 2D profissional, HTML5/WebGL nativo, LEVE, e eu
  **construo 100% headless e publico**. Atende TODAS as diretrizes: Arcade Physics
  (`body`+`collider`+collision groups = camadas/máscaras; velocidade zera no impacto),
  FSM de animação, sprite sheet, LERP, WebGL com fallback Canvas.
- **Obtido pelo GitHub/npm** (o proxy libera o npm; CDNs jsdelivr/unpkg dão 403):
  `npm pack phaser@3.80.1` → extraí `dist/phaser.min.js` → **vendorizado em
  `_lib_jogo/phaser.min.js`** (offline, igual ao `three.module.min.js`).

**PIPELINE (tudo no GitHub, igual ao Gemini):** arte → workflow `[imagens]` (Gemini) →
jogo Phaser em 1 HTML com `phaser.min.js` embutido → commit → Fábrica/republicar (Pages)
→ Auditor (render+E2E headless) antes de subir. **COMPROMISSO: parar de pular de estilo;
Phaser exploratório é O caminho, com física nativa (mata os bugs de colisão na mão).**

---

## 🧪 PROVA GODOT PELO GITHUB (2026-07-18): FUNCIONA, mas PESA 35 MB (inviável p/ escola)

O Marcos queria uma ferramenta profissional onde eu construo e o GitHub exporta o jogo
pronto. **Provamos que É POSSÍVEL:**
- Escrevi um projeto Godot mínimo (`_godot/`: `CharacterBody2D`+`move_and_slide` = física
  NATIVA, `StaticBody2D` colisores) + workflow `.github/workflows/godot-web.yml` (dispara
  por push `[godot]`; imagem `barichello/godot-ci:4.2.2`; internet liberada no Actions —
  ao contrário do meu chat, que leva 403). Exportou HTML5 e commitou em `_godot/build/web`.
- **RODOU** (render headless: física nativa ok, FPS 60). Pipeline ponta a ponta funciona.

**MAS o veredito (número na mão):**
- **35 MB** o build — `index.wasm` sozinho **34 MB** (é o motor Godot inteiro; só um
  quadrado se mexendo, sem arte). Levou ~16s pra carregar no render de software.
- Comparação: **Phaser inteiro = 1,2 MB (~30x mais leve)**; atividade 2D nossa = centenas
  de KB. O FX-4300 da escola + internet compartilhada **não aguenta 35 MB por atividade**.
- Godot 3 seria ~10-15 MB e brotli reduz a transferência, mas o wasm ainda descompacta p/
  ~34 MB e compila — pesado em CPU velha. Continua um exagero.

**CONCLUSÃO:** Godot-pelo-GitHub é real e legal, mas **pesado demais pra realidade da
escola**. **Phaser 3** entrega as MESMAS diretrizes profissionais (física nativa Arcade,
FSM, sprite sheet, LERP, WebGL) **~30x mais leve** e eu construo/publico 100% headless.
Recomendação: seguir com Phaser. (Arquivos Godot ficam no repo como prova; não usar em prod.)

---

## ✅ KIT SPRITE COMPLETO + PHASER (física nativa) FUNCIONANDO — pelo GitHub (2026-07-18)

O Marcos queria "kit sprite completo e lindo", acesso pelo GitHub, jogo profissional sem
bug. ENTREGUE e provado:
- **Kit do Byte gerado pelo Gemini/GitHub** editando a âncora `byte2d` p/ manter o MESMO
  personagem: `byte_walk_a` (pé esq. à frente) + `byte_walk_b` (pé dir.). Consistentes.
- **Folha de sprite alinhada** (`_kit/montar_sheet.py`): recorta o fundo (imagem INTEIRA,
  sem cortar membro), normaliza os 3 quadros no MESMO tamanho com os PÉS na mesma linha
  (BASE_Y) → `_kit/img/byte_sheet.png` (3×200×240). É o alinhamento que tira o "travado".
- **Motor Phaser** (`_kit/index.html`, usa `_lib_jogo/phaser.min.js`): **física NATIVA
  Arcade** (`physics.add.sprite`/`body`, `collider` com obstáculos StaticBody = não
  atravessa, `overlap` pega coco), **FSM Idle/Walk** (spritesheet + frameRate 7), **LERP**
  na velocidade, **câmera segue** (exploração), **Phaser.AUTO** (WebGL+fallback Canvas).
- **Auditor (render E2E headless):** o Byte ANDOU, colidiu com obstáculo, coletou 2 cocos,
  **FPS ~59, sem erro de JS.** Leve (~1 MB Phaser + assets).
- **Publicado** pela Fábrica em `byte-explora`.

**LIÇÃO CHAVE (fim do círculo):** o bug de animação nunca foi do Phaser — era sprite
INCOMPLETO/recortado em membro + colisão na mão. Com **kit completo (frames inteiros
alinhados) + física nativa Arcade + Auditor**, ficou lindo, fluido, sem bug e leve. Godot
provou funcionar mas pesa 35 MB (inviável). **Phaser + kit completo + IA = o caminho.**
`byte_walk_*` reaproveitáveis; dá pra gerar mais poses (correr, pegar, comemorar) do mesmo jeito.

---

## 🏛️ PLATAFORMA "RPG Educativo IA" — o Canva dos RPGs (arquitetura + 1º tijolo) — jul/2026

**O Marcos pediu uma PLATAFORMA** (não um jogo): professor informa `ano · disciplina ·
objetivo · tema · tempo · dificuldade`, clica **GERAR** e recebe um RPG top-down educativo
completo, jogável, offline no PC velho. Sem programar/editar JSON/desenhar. Ver o documento
**`ARQUITETURA-PLATAFORMA-RPG.md`** (a lei da plataforma, escrita ANTES do código a pedido dele).

**3 DECISÕES que o Marcos fechou:**
1. **Asset Pack = Kenney (CC0)** — identidade visual única; IA NÃO desenha, só escolhe peças.
2. **LLM desde já** — reconciliação honesta: LLM roda na **hora que o professor GERA** (ele tem
   internet ao preparar); o **jogo gerado é estático** e o aluno joga **offline**. LLM no authoring,
   não no play → não quebra o custo-zero na sala.
3. **Ir direto ao gerador** — alerta técnico registrado: o gerador precisa renderizar, então
   "motor-plataforma + tilemap + Kenney" não some — vira **infra do gerador** (F1 funde em F2).

**1º TIJOLO CONSTRUÍDO E PROVADO — o cérebro do gerador (o que faz disto "o Canva"):**
- `educaverso-app/src/gerador/tipos.ts` — `BriefingProfessor`, `PlanoMissao`, `MecanicaPedagogica`.
- `educaverso-app/src/gerador/catalogo-pedagogico.ts` — mapeia **objetivo → conceito → mecânica
  jogável → params**. Escala por dificuldade E idade (pré/1º ano seguram o teto). Determinístico
  (mesmo briefing = mesma missão) e reproduzível por tema.
- **🔒 TRAVA DO PORTÃO 0 (a mais importante):** `src/motor/mecanicas/registro-ids.ts` é a "lista da
  verdade" (leve, zero Phaser) das mecânicas jogáveis. O gerador SÓ emite missão cujo `id` existe lá
  → **estruturalmente incapaz de gerar quiz**. Qualificação é pelo CONCEITO (gatilhos no objetivo),
  nunca por idade/disciplina soltas (senão matemática "casaria" com história só pelo ano — bug pego
  no QA e corrigido). Objetivo sem mecânica jogável → **0 missões** (avisa honesto, não inventa quiz).
- **ROBÔ-QA:** `educaverso-app/tools/qa-gerador.mjs` (bundla o TS com esbuild, roda em node) — 10/10
  APROVADO: reconhece contagem, escala dificuldade/idade, determinístico, reproduzível, trava do
  Portão 0 segura, tempo→nº de missões. `tsc --noEmit` = 0 erros (strict).
- **Estado runtime:** só a mecânica `contar` existe jogável → o catálogo pedagógico hoje cobre
  contagem (pré–3º ano). Crescer = escrever a mecânica runtime + 1 entrada pedagógica + 1 id no registro.

**PRÓXIMOS PASSOS da plataforma:** (a) trazer o Kenney CC0 pro repo; (b) tilemap Tiled com vagas
nomeadas + motor renderizando nele; (c) gerador de mapa (posiciona NPC/itens nas vagas a partir do
PlanoMissao); (d) gerador de diálogo (LLM no authoring); (e) formulário do professor → AdventureSpec;
(f) mais mecânicas jogáveis (juntar/somar, repartir/fração) pra ampliar a cobertura.

### 🎨 DECISÃO DE ARTE do Marcos (plataforma RPG) — jul/2026
- **Identidade visual = estilo "Ninja Adventure"** (pixel-boy, CC0 verdadeiro) — aprovado pelo
  Marcos vendo o GIF de prova (caminhada 4 direções frame a frame, tileset com borda orgânica).
- **⚠️ REGRA DO PORTÃO DE ARTE: SEM TEMA NINJA nos jogos das crianças** — nada de samurai/
  espada/arma. Usar o **elenco NEUTRO** do pack completo (aldeões, crianças, velhinhos, monges,
  animais). Os guerreiros do subconjunto (ninja_blue, samurai_*) NÃO entram em jogo de criança.
- **Kenney = reserva/complemento** ("qualquer coisa, Kenney") — packs tiny-town/tiny-dungeon/
  roguelike-characters continuam no repo como fallback.
- Assets em `content/assets/ninja-adventure/` (subconjunto do repo Godot; pack completo via
  espelhos GitHub CC0 — superpowers-asset-packs e learnGodotArabic). Workflow `baixar-kenney.yml`
  aceita slug kenney OU URL direta de zip (nome do destino = nome do repo da URL).
- Licenças: Ninja Adventure é CC0 (uso comercial, sem atribuição, pode viver em repo público).
  Filtro pra QUALQUER pack novo: a licença tem que permitir REDISTRIBUIR os arquivos em repo
  público (CC0/CC-BY sim; "licença própria itch" quase sempre NÃO).

### 🏘️ VILA VIVA publicada — 1ª prova PÚBLICA do motor RPG (jul/2026)
- **Link:** https://vidalprof.github.io/vila-viva/ (repo `vila-viva`, criado pela fábrica;
  Pages confirmado `built`, erro=nenhum). Lição: o Marcos vê as entregas por LINK publicado —
  todo marco relevante deve virar link, não imagem no chat.
- Conteúdo: cena `VilaViva` (educaverso-app/src/rpg/VilaViva.ts) — tilemap Phaser real
  (grama G(3,4)+blob 3x3 do tileset_floor NA), props recortados por segmentação com colisão
  pelos pés, herói (char 25) tap-to-move com caminhada 4 direções frame a frame, NPCs neutros
  (fazendeiro 5, menina 17, avô 9) + dog passeando, sombras, depth por Y, zoom 3 pixelArt.
- Boot: `?rpg` na URL do app OU `window.__BOOT='rpg'` injetado no index publicado. UI legada
  da Ilha é escondida no boot RPG (bug pego pelo MEU olho no screenshot do QA — o robô não vê capa).
- Publicação: pacote mínimo dist (index+assets+rpg, 1,7MB) testado pelo robô ANTES; `_novo` na
  MAIN via worktree (fluxo oficial fábrica) + `fabrica.yml` (repo_name=vila-viva) + `deploy-pages.yml`.
- QA `tools/qa-vila.mjs`: 12/12 (anda 4 direções com anim certa, casa bloqueia, 4 NPCs, zero 404).

### 📱 Vila Viva v2/v3 — lições do celular do Marcos (jul/2026)
- **v2 (blindagem celular):** no iPhone do Marcos o módulo JS morreu ANTES de esconder a capa
  legada → ele viu "Ilha do Tesouro" com botão morto. Cura tripla no index publicado:
  (1) CSS `display:none!important` na UI legada (independe de JS); (2) vite target
  +`safari13` (transpila `?.` — iPhone antigo abre); (3) caixa vermelha `erroBox` no
  `window.error` (o print do Marcos passa a contar o erro exato). **Regra: TODO index
  publicado de app leva essa blindagem.**
- **Robô-iPhone:** `tools/qa-vila-iphone.mjs` (Playwright device iPhone 12, toque real).
  ⚠️ Alarme falso aprendido: com câmera CLAMPADA na borda do mapa, o herói NÃO fica no centro
  da tela — tocar "no centro" = tocar no herói = não anda. Robô agora toca LONGE do herói.
- **v3 (feedback do Marcos por link):** "passa direto pelos personagens?" → NPCs ganharam
  CORPO (collider imóvel; herói esbarra e para) e VIRAM O ROSTO para o herói ao chegar perto
  (frame da coluna da direção). Dog continua atravessável de propósito. QA 15/15.
- **Fluxo de publicação da vila:** pacote mínimo dist → blindar index → QA desktop+iphone →
  `_novo` na MAIN (worktree) → `atualizar.yml` (repo_name=vila-viva) → conferir push no log
  (`main -> main`) → link com `?v=N` novo (cache do celular é teimoso).

### 🧭 Direções do Marcos (vila-viva, jul/2026) — valem p/ a plataforma
- **"Montar o jogo todo primeiro, a pedagogia entra depois em cima" — CONFIRMADO como caminho.**
  O motor/mundo não sabe o que é escola; a missão pedagógica PLUGA no mundo pronto (Portão 0:
  vira problema do mundo, nunca prova). Ordem de produção: mundo gostoso → missão encaixada.
- **Interior COMBINA com o tema** (fazenda=rústico; nada de casa moderna em vila de aldeões) —
  MAS **"mesmo pack = tudo ok, não precisa forçar"**: coerência é a regra, perfeccionismo não.
  Piso do interior trocado p/ palha rústica (tileset_interior_floor y~200) — reversível em 1 arquivo.
- **Câmera:** botão VER TUDO (lupa, zoom 2 mostra o cenário inteiro — resolve "casinha cortada
  no canto") + botão TELA CHEIA (cantoneiras). Cena UIVila separada (sem zoom), ícones pixel sem
  texto, stopPropagation (clicar no botão não anda). Troca de zona SEMPRE restaura a visão normal.
- vila-viva v5 no ar (?v=5). QA 21/21 + iPhone 3/3 antes de publicar, sempre.

### 🌟 VISÃO COMPLETA reafirmada pelo Marcos (jul/2026) — o produto final
Jogo TODO explorável primeiro → camada pedagógica vira AVENTURA (enredo/história completos,
ganchos neurocientíficos p/ o estudante AMAR) → 55 minutos, narrado, didático, progressivo →
progresso salvo no FIREBASE ("o mundo é DELE" — o aluno volta e o mundo lembra) → isso gera
AVALIAÇÃO DESCRITIVA (registro por missão) que pode virar NOTA se o professor quiser →
aventuras em SEQUÊNCIAS DIDÁTICAS (encadeadas) → tudo preparado e AUDITADO por equipe de
agentes, cada um com sua tarefa (pedagogo/roteirista/game designer/engenheiro/diretor de arte
+ robô-QA + Portão de Arte). Padrão de qualidade: "referência em criação de jogos do tipo".

### 🎯 ESCLARECIMENTO DEFINITIVO do Marcos (jul/2026) — o que é "enquadrado"
NÃO é fase de teste fake. É: **o MUNDO REAL do jogo** (mapas do autor, personagens,
história, MÚSICA, SONS, animações, INTERIORES — tudo como no jogo de verdade) mostrado em
**telas EMOLDURADAS** (screen-by-screen, estilo Zelda clássico) pra a criança **explorar aos
poucos**. A moldura é só a JANELA; o conteúdo é o jogo completo do autor. Depois a pedagogia
entra por cima virando aventura.
- Base = MundoAutor (mapa real 86x82 já decodificado). Apresentar em REGIÕES emolduradas com
  transição (câmera trava numa tela; ao chegar na borda/saída, fade pra tela vizinha).
- FALTA trazer do pack (tudo CC0): 10 músicas (audio/music/*.ogg) + 40 SFX + animações de
  ambiente (água animada tileset_animated, vento) + interiores reais + NPCs com diálogo (faceset).
- FasesDemo foi só a PROVA do mecanismo (aprovada). O de verdade é o mundo do autor emoldurado.

## 🔭 O OBSERVATÓRIO DO ÓRBI — 3º ano, Sistema Solar (ago/2026)

Pedido do Marcos: *"atividade para o terceiro ano sobre o sistema solar: vídeos,
informações sobre os planetas, atividades com bastante imagens, nos mesmos moldes
das últimas, bem didática, progressiva, sonora, visual, com relatório e tudo…
novo tema, novo mascote, 45 minutos"*. Mascote **Órbi** (astronautinha de massinha),
pasta `_orbi/`, repositório `observatorio-do-orbi`.

### Decisões de arte que viraram REGRA para conteúdo de ciências
- **Os planetas são FOTORREALISTAS** (estilo foto de telescópio/NASA: faixas de
  Júpiter, anéis de Saturno, Marte vermelho, Terra azul com a América do Sul).
  O **mascote e os objetos do dia a dia continuam em massinha**. Motivo pedagógico:
  a criança tem que **reconhecer o planeta de verdade** quando vir num livro ou no
  céu; desenhar planeta "fofinho" ensinaria a imagem errada. Mistura funciona: o
  personagem é do mundo do jogo, o planeta é do mundo real.
- **"Vídeos" não entram**: vídeo pesa dezenas de MB, quebra o offline e trava PC
  fraco. O que substitui com vantagem é **animação interativa dentro do app** (a
  criança gira a Terra e a Lua com a mão, em vez de assistir).

### 🌙 FASES DA LUA NO HEMISFÉRIO SUL (erro fácil de cometer — não repetir)
Em Blumenau o **quarto crescente aparece iluminado do lado ESQUERDO** e o
**minguante do lado DIREITO** — ao contrário de quase toda ilustração de livro
(que é feita para o hemisfério norte). Se a imagem sair invertida, a criança olha
o céu e vê o oposto do que o app ensinou.
**Como as fases foram feitas:** NÃO se pede a fase ao gerador de imagem (ele erra
o lado e muda a bola de tamanho). Gera-se **só a lua cheia** e as outras três saem
por código, escurecendo metade da MESMA bola (`ESC=0.15`, terminador suave). Isso
garante de brinde o conceito: *a Lua não muda de tamanho, muda o pedaço iluminado*.
**Na cena das fases o SOL tem que estar na tela** (à esquerda): sem ele, ligar
posição→fase é arbitrário. Lua à esquerda (entre Terra e Sol) = **nova**; à direita
= **cheia**; em cima e embaixo = os quartos.

### 📚 Currículo de Blumenau — 3º ano, Ciências (Terra e Universo)
Verbatim: *"Identificar o Sol como estrela, a Terra como planeta e a Lua como
satélite"*; *"Identificar características da Terra (formato esférico, presença de
água, solo)"*; *"A Lua e suas fases"*; *"Observar, identificar e registrar os
períodos diários (dia e/ou noite) em que o Sol, demais estrelas, Lua e planetas
estão visíveis no céu"*. ⚠️ **"Classificação dos planetas do Sistema Solar" e
"descrever a composição e a estrutura do Sistema Solar / Via Láctea" aparecem em
ANO POSTERIOR** — por isso os oito planetas entram aqui como **reconhecimento,
ordem e curiosidade**, e não como classificação (rochosos × gasosos).

### Mecânicas novas que entraram no leque (reaproveitáveis)
- **APAGUE O SOL** — botão que apaga o Sol e a criança VÊ quem continua aceso
  (Sol e lâmpada) e quem apaga (Lua, Terra, espelho). O espelho é a ponte concreta.
- **GIRE A TERRA** — a criança gira a Terra de 45º em 45º e leva a casinha para a
  sombra. Mata o "o Sol apaga de noite" sem nenhuma explicação verbal.
- **ÓRBITA PASSO A PASSO** — leva a Lua de pontinho em pontinho até fechar a volta.
- **FICHA DO PLANETA** — toca no planeta, vê a foto grande e OUVE o fato (é assim
  que "informação sobre os planetas" entra sem virar texto para ler).
- **FILA A PARTIR DO SOL** — ordenar montando uma fila que cresce ao lado do Sol.
- **DO MENOR AO MAIOR** — as cartas têm tamanhos diferentes de propósito.

### Armadilhas pagas nesta atividade
- **Gemini devolveu Marte com fundo PRETO** (e a estrela quase invisível) enquanto
  todos os outros vieram em branco. Sempre **olhar a folha de contato** antes de
  recortar; refazer só os que saíram errados custa centavos.
- **Lua cheia com tolerância 6 perdia uma "mordida" no limbo** (a borda da Lua é
  quase branca). Para imagem clara sobre branco, **tolerância 1**.
- **A banca reprovou por causa do caça-palavras**: `telaCacaBase(cfg)` recebia
  config e o auditor chama toda tela **sem argumento**. Regra: tela que recebe
  parâmetro precisa de `cfg=cfg||PADRAO`.
- **O jogador automático não conhecia as mecânicas novas** e ficou preso na órbita
  da Lua. Ao criar mecânica nova, **acrescentar a classe no `SEL` do
  `_qa/jogador.js`** — senão a banca reprova sem haver defeito.

## 🚫 REGRA PERMANENTE: nada do antigo se apaga (Marcos, ago/2026)

Palavras dele: *"não apagar nada do antigo, as atividades novas em repos novos"*.

- **Atividade nova = repositório NOVO** (`fabrica.yml`). Nunca publicar por cima de
  uma atividade existente, nem "aproveitar" o repo de outra.
- **Nenhum repo, card ou link antigo sai do ar** — nem quando a atividade nova trata
  do MESMO assunto e do MESMO ano. Foi exatamente o caso do Sistema Solar do 3º ano:
  ficaram os dois no hub, *"O Observatório do Órbi"* (novo, no topo, como manda a
  regra de ordem) e *"Aventura no Espaço — Sistema Solar"* (`Sistemasolar3ano`).
- Remover qualquer coisa só com pedido explícito do Marcos. Na dúvida, PERGUNTAR e
  MANTER. O `atualizar.yml` espelha o destino, então tomar cuidado para nunca apontar
  um `source_dir` para o repo errado — isso apagaria o conteúdo de lá.

## 🧩 LEGENDA DO CLIQUE — a fase da bancada estava intransponível (ago/2026)

Relato do Marcos: *"não tem como passar a fase do oval, retângulo, losango, pois não
arrasta no computador e nem por clique"*.

**O que estava errado (duas coisas somadas):**
1. A fase **exigia a ordem** artigo → substantivo → adjetivo e **recusava calada**
   qualquer outra. Quem começava pelo substantivo (o mais natural: é a palavra da
   foto) tomava "errado" sem entender e podia ficar preso a fase inteira.
2. A peça **parece** arrastável (peça encaixando numa vaga com a mesma forma), mas
   não existia nenhum código de arrasto. O aluno arrasta, não acontece nada, e
   conclui que o jogo travou.

**Como ficou:** cada peça procura **a vaga da forma dela, em qualquer ordem**, e a
mesma função atende **toque E arrasto** (mouse e dedo). Soltar no vazio devolve a
peça sem penalidade; soltar na vaga errada dá o "não" honesto.

**Armadilha paga:** não dar `preventDefault` no `touchstart` — isso cancela o clique
sintético e mata justamente a opção do toque. O toque passou a ser resolvido no
`touchend`/`mouseup`, com um carimbo de tempo para o clique seguinte não repetir a
jogada. Testado nos dois: PC (clique e arrasto do mouse) e tablet (toque simples).

**De quebra:** o auditor de contraste (que nasceu depois desta atividade) reprovava
**59 textos**. Toda a paleta foi escurecida o suficiente para passar o mínimo WCAG
sem mudar a cara do jornal, e a tela final foi compactada porque o botão "Treinar o
que faltou" nascia **atrás da barra de baixo**.

**Buraco conhecido do auditor jogador:** ele ainda fica preso no **QUADRO DE LETRAS**
(a cruzadinha), pelo mesmo motivo do caça-palavras — clicando ao acaso não dá para
resolver. Vale aplicar ali o mesmo truque do `data-qa` já usado no Observatório do
Órbi quando essa atividade for mexida de novo.

## 📊 AUDITOR NOVO: PROGRESSÃO — a barra andava PARA TRÁS (ago/2026)

O Marcos perguntou se as atividades estavam *"adequadas didaticamente, com
progressão"*. Fui medir em vez de opinar, e a pergunta achou defeito real: em
**três** delas a barra de progresso **voltava** no meio do percurso.

| atividade | onde | queda |
|---|---|---|
| Legenda do Clique | nFabrica → nPlural | **68% → 48%** |
| Plantão na Redação | gLigar → gBanca | 50% → 46% |
| Plantão na Redação | gPalavra → gTrocado | 82% → 80% |
| Doceria do Cacau | dMemoria → dCaca | 92% → 91% |

**Causa (sempre a mesma):** fases novas são inseridas no meio e ninguém renumera
o `setProg` das vizinhas. A ordem real das fases deixa de bater com o número que
cada uma pinta na barra. **Nenhum print pega isso** — só comparando a sequência
real com os números.

**Conserto:** as cinco atividades foram renumeradas e agora nenhuma volta.

**Para não acontecer de novo:** nasceu o **`_qa/progressao.py`**, já ligado no
`_qa/auditar.sh` como **portão 3b**. Ele segue os `mostraBanner(msg, próximaTela)`
e reprova qualquer transição que caia para um número menor. Sempre que inserir
fase no meio de uma atividade, é ele que avisa.

## 🎓 PROGRESSÃO DIDÁTICA — a ordem das fases estava errada em três (ago/2026)

O Marcos perguntou pela **progressão didática** (eu tinha respondido sobre a barra
de progresso; ele corrigiu: *"falo de progressão didática"*). Fui ler a sequência
real de fases das cinco atividades e encontrei três problemas de ORDEM.

### O que estava errado e como ficou

**1. A Legenda do Clique montava a casa antes dos tijolos.**
A criança montava o **grupo nominal** (artigo + substantivo + adjetivo) aos 32%,
mas o adjetivo só era trabalhado depois — "filtro mágico" (o que o adjetivo FAZ) e
"detetive" (usar o adjetivo) vinham aos 36% e 44%. Ela juntava uma peça que ainda
não conhecia.
**Nova ordem:** substantivo → separar as duas classes → o adjetivo em ação →
usar o adjetivo → **montar o grupo** → concordância → morfologia → produção.

**2. No Plantão na Redação (verbos), a criança consertava concordância antes de
saber conjugar** — e as duas fases de TEMPO estavam separadas por uma de
concordância no meio.
**Nova ordem:** identificar o verbo → quem fez a ação → aquecimento → tempo →
linha do tempo → **conjugar** → erro de concordância → revisor → produção.
⚠️ *Correção do meu próprio diagnóstico:* eu disse ao Marcos que "a concordância
vinha antes do sujeito". **Estava errado** — eu tinha lido os números da barra, não
a cadeia real. O sujeito já vinha antes. Lição: **seguir a cadeia de chamadas, nunca
inferir a ordem pelos números do setProg.**

**3. No Observatório do Órbi**, "o que só a Terra tem" estava aos 91%, longe do
bloco em que a Terra é o assunto; e havia **quatro fases seguidas de planetas** só
de reconhecer (ficha → ordem → pista → tamanhos), justo aos 30 minutos de jogo.
**Agora:** a Terra vem aos 22%, logo depois de classificar estrela/planeta/satélite;
e "monte a palavra" entra no meio do bloco dos planetas, quebrando a repetição.

### O auditor ficou mais esperto
O `_qa/progressao.py` só seguia `mostraBanner(msg, próximaTela)` e por isso **não
via** as transições por chamada direta — foi assim que as quedas do Plantão
(56% → 36%) passaram batido na primeira rodada. Agora ele segue as duas formas.

## 🧑‍🚀 REGRA: cada atividade tem os SEUS avatares (Marcos, ago/2026)

Ele reparou: *"no sistema solar você usou o avatar da atividade do broto para as
crianças escolherem, deveria ser avatar novo com roupas espaciais"*. E estava
certíssimo — eu tinha copiado os `jd_cr1..6` (os brotinhos verdes de chapéu e
laço) para dentro do Observatório do Órbi só para economizar geração de imagem.
No meio de um céu estrelado, seis brotos de jardim gritam que foi copiado.

**Regra:** a tela "Quem vai jogar?" é a primeira coisa que a criança vê e é onde
ela se coloca dentro da história. **Os avatares fazem parte do tema** — nunca
reaproveitar os de outra atividade. Custa 6 imagens; vale a pena.

**Os do Órbi:** seis criancinhas astronautas em massinha, retrato do peito para
cima (o rosto tem que ser legível a 62px no crachá), capacete de vidro com aro
prateado, e cada uma com **cor de gola e distintivo diferentes** (foguete, planeta,
estrela, cometa, lua, planeta com anel) para dar de distinguir. Tons de pele,
cabelos e detalhes variados de propósito — é escola pública, a criança tem que
se achar ali.

**De brinde, a prévia pegou mais duas coisas herdadas do molde:** a figurinha
escolhida acendia em **verde** (cor do Jardim) num app violeta — agora acende em
dourado; e a tela final, mais alta que a janela, deixava a última linha do boletim
**atrás da barra de baixo** — mesma armadilha do `_padrao/FIM-DE-ATIVIDADE.md`,
resolvida com a tela final compacta começando do topo.

### 🚫 VIROU LEI: nunca copiar avatar, arte sempre nova e temática

Palavras do Marcos: *"nunca copiar avatares, sempre ser temático, nunca repetir o
avatar, sempre novo e temático"*. Está escrito em três lugares para não depender
da minha memória:

1. **`CLAUDE.md`** (lido no começo de toda sessão) — junto das outras leis de
   atividade nova.
2. **`_qa/arte_propria.py`** — auditor novo, **portão 3c** da banca: tira o hash de
   cada imagem da atividade e compara com as de todas as outras. Byte a byte igual
   = reprova. Não adianta eu "lembrar"; agora a banca barra.
3. Aqui na memória.

**Regra em uma linha: clonar o MOTOR é obrigatório, clonar a ARTE é proibido.**

**Exceção honesta já registrada no auditor:** pastas que são **versões da mesma
atividade** não contam como cópia. É o caso de `_redacao` (A Redação do Pingo),
que nasceu da junção de `_verbos` (Plantão na Redação) e `_generos` (A Banca do
Pingo) — o Pingo é o mascote das três, a arte é dela mesma. O auditor apontou as
35 imagens repetidas ali logo na primeira rodada; conferi a origem antes de sair
"consertando" e registrei a exceção com a prova. **Só entra na lista com esse
tipo de prova; na dúvida, é cópia e reprova.**

## 🔁🔊 AQUECIMENTO na Doceria e na Legenda + ALTO-FALANTE no Órbi e no Jardim (ago/2026)

Marcos: **"Pode fazer tudo"** — os dois itens que ficaram pendentes da rodada
anterior. Feitos:

### 1) Aquecimento (revisão espaçada) — agora nas quatro
Já existia no Órbi (`telaAquecimento`) e no Jardim. Faltava na **Doceria do Cacau**
e na **Legenda do Clique**:

- **Doceria — `dAquecimento`, 48%**, entre o "vezes" e a bandeja em fileiras.
  Volta ao conceito **mais antigo** (grupos iguais): quatro caixinhas com três
  biscoitos, "qual soma combina?". Falas `dc_aquec_intro` / `dc_aquec_dica`.
- **Legenda — `nAquecimento`, 60%**, entre o grupo nominal e o plural. Volta a
  **nome × adjetivo** ("na legenda *a flor amarela*, qual palavra diz **como é**?").
  Falas `nm_aquec_intro` / `nm_aquec_dica`.

**Por que importa (e não é enfeite):** o acerto entra em `reg()` no conceito
ANTIGO, então o painel do professor passa a medir **retenção** (lembrou depois
de um tempão), e não só o acerto no instante em que se aprendeu. Receita fixa:
selo "LEMBRANDO...", mascote pequeno, 3 opções, `reg()` no conceito mais velho,
e o `setProg` escolhido no buraco entre a fase anterior e a seguinte (senão o
auditor de progressão reprova).

### 2) Alto-falante nas opções (acessibilidade) — Órbi e Jardim
A máquina do `.zap` já rodava na Doceria e na Legenda; foi portada para o
**Observatório do Órbi (32 vozes)** e o **Jardim do Broto (25 vozes)**. Botãozinho
redondo ao lado de cada resposta lê **aquela** resposta — nunca as outras, senão
vira "ouvir tudo" e a criança para de tentar ler.

**Receita completa (para repetir sem redescobrir):**
1. **Colher os textos** que a criança precisa ler. Dois jeitos somados, porque
   nenhum sozinho basta:
   - *runtime* (`/tmp/colher.js`, Playwright): abre cada tela e pega o
     `textContent` dos seletores — pega textos montados por concatenação, tipo
     `"ESTRELAfaz luz"` (rótulo + subtítulo colados);
   - *estático* (regex nos pares `["texto", true|false]` do fonte): pega as
     perguntas 2ª e 3ª de telas com várias rodadas, que o runtime não mostra.
2. **Chave** = `chaveVoz` = djb2 do texto normalizado (espaços colapsados,
   minúsculo) em base36. **Confira a conta do Python contra a do navegador** em
   umas amostras antes de gerar 30 mp3 com nome errado.
3. **Gerar** pelo `gerar-audio.yml` com o input **`lote`** (JSON inline) e
   `outdir=<pasta>/audio`, `ref` = a branch. Não precisa commitar
   `_lote_falas.json` — o input inline evita um commit só para isso.
4. O texto **falado** pode ser mais gentil que o da tela: `"ESTRELAfaz luz"` →
   *"Estrela. Faz luz."*; `"LUA CHEIA"` → *"Lua cheia."*. A chave é do texto da
   TELA; a fala é livre.
5. `ZAPSEL` por app (Órbi `.opt,.pc,.bin`; Jardim `.opt,.lig,.pc,.bin`) e CSS com
   ícone **branco** quando o fundo é escuro (`.bin`, `.pc.usada`, `.lig.ok`).

### 3) ⚠️ LIÇÃO PAGA: auditor que roda CEGO é pior que auditor que reprova
O `auditar.sh` chama o contraste e o leiaute com `2>/dev/null`. No Jardim, o
`telaCacaBase()` e o `telaPartesBase()` **estouravam quando chamados sem config**
(os auditores abrem TODA tela sem argumento) — o node morria na 1ª tela, o stderr
ia para o lixo, e o portão imprimia **nada**. Eu lia "reprovou" e olhava para o
jogador; os dois auditores de verdade **nunca tinham rodado** naquele app.

- **Regra:** toda `xxxBase(cfg)` começa com `if(!cfg){ <telaPadrão>(); return; }`.
  (Mesma correção que o Órbi já tinha; o Jardim tinha DUAS.)
- Quando um portão imprimir **linha nenhuma**, isso não é "passou" nem "falhou":
  é **rodou cego**. Rodar o auditor na mão, sem `2>/dev/null`, e ler o erro.

Assim que voltaram a enxergar, os dois acharam defeito real no Jardim: o placar
"Acertos: 0" era **branco sobre foto clara (1,32:1)** — virou pílula escura; e o
"Treinar o que faltou" dava 4,23:1 (na Doceria, 4,33:1) — verde escurecido para
#2f7a1c→#1d4f0d nos dois.

### 4) O auditor JOGADOR ficou menos burro
Ele clicava ao acaso e empacava em fases que **um humano passa fácil**, o que
gerava alarme falso (e alarme falso ensina a ignorar o alarme):
- **caça-palavras** — a tela publica `data-qa` na `.grade` com onde cada palavra
  ficou (Órbi já tinha; agora Jardim e Legenda também);
- **monte a palavra** — as letras só valem NA ORDEM; a tela publica `data-qa` na
  `.letras` com a palavra da vez (Órbi, Jardim e Legenda);
- `.errow` (palavra sublinhada do "Revisor da página") entrou no `SEL`.

`data-qa` **não aparece para ninguém** e não muda o jogo — é só a chave do
auditor. Órbi, Jardim, Doceria e Legenda chegam sozinhos até a medalha.

## 🧨 A ÚLTIMA FASE DA LEGENDA ESTAVA QUEBRADA — e nasceu o portão 1b (ago/2026)

O jogador automático, depois de aprender a preencher campo de texto, chegou na
última fase da **Legenda do Clique** ("Escreva a legenda", 96%) e devolveu isto:

> `ERROS JS: ... || normal is not defined || normal is not defined || ...`

**O que estava acontecendo com a criança:** ela escrevia a legenda, apertava
**Publicar** e **não acontecia nada**. Nem erro, nem elogio, nem passagem de
fase. `nLegenda` chamava `normal(...)` — a função que tira acento (para "cão" e
"cao" valerem as duas) — e essa função **nunca tinha sido copiada** para o
arquivo; ficou só na Redação do Pingo, de onde o motor foi clonado. O app
travava ali, na fase de PRODUÇÃO, que é a mais importante de todas.

**Por que ninguém pegou antes:** o `node --check` (portão 1) só vê **sintaxe** —
e a sintaxe estava perfeita. A tela abria bonita, a foto aparecia, o campo
aceitava texto. O defeito só existe no instante do clique. Print de tela não
mostra; olhar o código também não, porque o nome `normal(` parece o de sempre.

### 🕵️ AUDITOR NOVO — `_qa/funcoes.py` (portão **1b** da banca)
Junta tudo que é chamado como `nome(` no JS (**depois** de tirar comentários e
textos entre aspas — senão qualquer palavra escrita num comentário viraria
"chamada") e compara com tudo que o arquivo declara + os globais do navegador.
Rodando no arquivo ANTES do conserto ele aponta em uma linha:

```
   1 FUNCAO(OES) CHAMADA(S) QUE NAO EXISTEM (estoura na mao da crianca):
    normal()   (1a chamada por volta da linha 1049 do JS)
```

**Regra:** toda vez que eu clonar um motor e trazer só "a tela que interessa",
alguma função de apoio fica para trás. O portão 1b existe exatamente para isso.

**Ele já achou defeito parado em outras atividades** (não consertado nesta
rodada, fica anotado para a próxima): `_clima` chama `pcor()`, `gradeStars()` e
`nara_()`; `_estrelas` chama `pcor()`. Rodar `python3 _qa/funcoes.py <arq>` nelas
antes de qualquer aula que as use.

### O jogador também aprendeu a ESCREVER
Sem isso o portão 6 nem alcançava a fase onde estava o defeito. A tela de
produção publica em `data-qa` do `<input>` uma legenda que serve; o jogador
digita, dispara o evento `input` e aperta o botão. **Lição geral:** auditor que
não alcança a última fase dá uma sensação falsa de segurança — e o defeito mais
caro costuma estar justamente lá, onde ninguém testa com paciência.

## 🧸 A FÁBRICA DE BRINQUEDOS DO BENTO — 4º ano, multiplicação (ago/2026)

Pedido da **professora do 4º ano**, trazido pelo Marcos: *"multiplicação inicial…
rever o conteúdo poderia ajudar? Aquela que fizemos para o 3º ajudaria?"*. E a
pergunta importante que veio junto: **"vai ser no mesmo padrão das últimas?"**.

**Resposta honesta que dei (vale registrar):** a **Doceria do Cacau ajuda como
MOTOR, não como conteúdo**. O que a Doceria ensina é literalmente o 3º ano de
Blumenau. O 4º ano pede quatro coisas que ela não tem, e é por isso que a
atividade nova precisou existir em vez de "esticar" a antiga.

- **Repo publicado:** `fabrica-do-bento` → **https://vidalprof.github.io/fabrica-do-bento/**
  (criado pela `fabrica.yml`, source_dir=`_fabrica`). Fonte em `_fabrica/`.
- **Mascote:** **Bento**, um bonequinho de corda de macacão jeans, o ajudante da
  oficina. Nome escolhido de propósito longe de Teco, Teo, Nino e Pingo (que já
  existem) para não confundir ninguém.

### Currículo (Blumenau, 4º ano) — verbatim, e onde cada item virou fase
- *"…diferentes significados da multiplicação como adição de parcelas iguais,
  organização retangular, combinação de possibilidades e proporcionalidade…"*
  → encher caixas / esteira em fileiras / sala de pintura / mesa das peças.
- *"Utilizar as propriedades da multiplicação para desenvolver estratégias de
  cálculo"* → **girar a bandeja** (comutativa VISTA, não decorada) e **separar o
  pedido** (distributiva: 7×13 = 7×10 + 7×3).
- *"Compreender as relações existentes entre as operações de multiplicação e
  divisão"* → "quantas caixas?" (o total e o tamanho da caixa são dados; falta o
  número de caixas).
- *"…cálculo por estimativa…"* → "cabe no caminhão?" (arredonda e compara).
- **Álgebra:** *"Identificar regularidades em sequências numéricas compostas por
  múltiplos"* → a **esteira que pula** de N em N.
- Ainda: **×10 e ×100** (caixas de dez, caixotes de cem), do objeto de
  conhecimento "composição e decomposição por potências de 10".

**21 fases, ~55 min.** Começa concreto no 3º ano (grupos iguais → parcelas →
vezes) nos ~12 primeiros minutos — que é a "retomada" que a professora pediu — e
só então sobe. Aquecimento (revisão espaçada) aos 33%. Termina com a criança
**criando o próprio pedido** e ensinando o Bento.

### Como foi feita (o rito que funcionou, para repetir)
1. **Currículo primeiro**, lendo o `_curriculo/blumenau.txt` no bloco do 4º ano —
   não de memória. Foi isso que mostrou que "multiplicação inicial" para o 4º ano
   é bem mais do que a Doceria.
2. **Clonar o MOTOR** por recorte de arquivo: cabeça (CSS+engine, linhas 1‑933 da
   Doceria) + conteúdo NOVO + cauda (capa, painel, boletim, treino) — e renome
   mecânico `dc_`→`fb_`, `cacauEl`→`bentoEl`. Deu certo de primeira: os 4
   primeiros portões passaram sem nenhum ajuste.
3. **Arte em lote no começo** (23 imagens, `_gerar_imagens.json` + `[imagens]`),
   recorte com a rampa suave + maior blob + **bbox comum nas 3 poses do mascote**.
4. **Voz depois** (65 falas + 16 do alto-falante), pelo input `lote` inline.
5. **Banca inteira** e só então publicar.

### ⚠️ O que a banca pegou antes de chegar na criança (o valor dela em um caso)
- **Fase impossível de terminar:** o "quadro do estoque" tinha **produtos
  repetidos** (42, 54 e 56 apareciam duas vezes nas contas) e o quadro guarda cada
  número **uma vez só**. Na segunda vez que a conta caísse no mesmo total, a
  célula já estaria marcada e o clique seria ignorado: a criança ficava presa
  **sem ter errado nada**. É o mesmo tipo de defeito que o Marcos pegou na Legenda
  do Clique — agora pego pelo jogador automático, em casa. **Regra nova: em
  qualquer fase de "ache o número no quadro", conferir que todos os produtos são
  DIFERENTES.**
- **Três contrastes** abaixo do mínimo WCAG (contador do caixote 3,81:1; placar do
  relâmpago 2,86:1; célula verde da tabela 4,43:1) — o placar é exatamente o mesmo
  defeito do Jardim, herdado do molde. Vale conferir `.placar` em toda atividade
  clonada.
- **O `var DOM={...}` do motor veio com os conceitos da Doceria** e o boletim do
  fim mostrava "grupos, soma, vezes" numa atividade de 4º ano. Ao clonar um motor,
  o `DOM` inicial é tão conteúdo quanto as fases — trocar junto.
- **O `VOZOK` também veio da Doceria:** o alto-falante aparecia em respostas cuja
  voz não existia nesta pasta (botão que não faz nada é pior que botão nenhum).
  Ao clonar, **regerar o VOZOK** com os textos da atividade nova.

## 🛑 ATIVIDADE NOVA NÃO VAI MAIS PARA O HUB (Marcos, ago/2026)

Logo depois de eu publicar a Fábrica do Bento e já pôr o card no "Ilhas do
Saber", o Marcos cortou: *"não precisa publicar no site de atividades as que
cria, só publicar no repo e me mandar o link por enquanto"*.

**O fluxo novo, curto:** cria → `fabrica.yml` (repo próprio) → confere o build
(`deploy-pages.yml`, `status=built`) → **manda o link** → fim. Sem `_site/`, sem
card, sem `img/ativ-*.png`, sem `atualizar.yml` para o `mundo-das-atividades`.

**Por que isso importa (leitura minha, para não errar de novo):** ele quer ver e
aprovar cada atividade antes de ela aparecer para as crianças no portal. Pôr o
card sozinho é decidir por ele o que entra no ar da escola. O card é decisão
DELE, não etapa automática do meu rito.

Está escrito no `CLAUDE.md` (lido no começo de toda sessão), logo acima do
passo a passo do card — que continua lá, guardado, para o dia em que ele pedir.

**O que NÃO fazer por conta própria:** apagar os cards que já estão no hub. A
regra "nada do antigo se apaga" continua valendo; o card da Fábrica ficou no ar
e eu avisei que tiro em um comando se ele quiser. Tirar coisa do ar só com
pedido explícito.

## 🔎 O OLHO DO MARCOS NA FÁBRICA: mascote, duração e variedade (ago/2026)

Três perguntas dele, e o que cada uma revelou quando fui MEDIR em vez de responder
de memória:

**1) "O mascote está tremendo? Não deveria piscar?"** — Medi o `transform` a cada
250ms: o movimento é liso (sobe 8px e volta, 2,8s) e ele **pisca 3× a cada 14s**.
Não era bug. Mas ele estava certo no que viu: o molde inclina o mascote **±1,5°**,
e isso passa despercebido num mascote REDONDO (Cacau, Broto, Órbi) e vira balanço
num mascote de **corpo inteiro, mais alto que largo** como o Bento — a cabeça
anda uns 6px. **Regra: mascote de corpo inteiro pede giro menor** (baixei para
±0,5° só nesta atividade).

**2) "21 telas não é pouco para 45 minutos?"** — Tela ≠ rodada. Contando as
RODADAS de verdade (cada fase tem de 1 a 8 itens): **72 rodadas, ~48 min** em
ritmo normal e ~60 min com turma mais devagar. Ficou registrado o jeito de
estimar: somar `rodadas × segundos por rodada`, não contar telas.

**3) "Tem bastante dinâmicas diferentes?"** — Aqui ele acertou em cheio e eu
estava fraco. Contei: **o teclado numérico aparecia em 9 das 20 fases**. Clonar o
motor traz de brinde o VÍCIO do motor. Acrescentei duas mecânicas que não
existiam:
- **Ligar duas colunas** (situação escrita ↔ conta) — a criança LÊ e interpreta,
  sem digitar número nenhum;
- **Arrastar o caixote até o caminhão** — era a única atividade recente **sem
  nenhuma fase de arrasto**, e o manual manda usar arrasto onde a ação natural é
  "levar um item até um lugar".
Ficou: **13 mecânicas distintas em 22 fases**.

### ⚠️ DUAS LIÇÕES PAGAS NA FASE DE ARRASTAR (valem para toda fase nova de arrasto)
- **Evento de mouse FANTASMA mata o toque simples.** No celular o navegador
  dispara `mousedown`/`mouseup`/`click` de compatibilidade DEPOIS do toque. O meu
  `mouseup` fantasma rodava o `solta()` de novo e **desmarcava** a peça que a
  criança tinha acabado de escolher — o toque nunca entregava a carga (o arrasto
  com mouse funcionava, então passava despercebido). Guardar só o `onclick` **não
  basta**: é preciso um `ultimoToque` e barrar TODO evento de mouse por ~800ms
  depois de um toque. Teste obrigatório: **arrastar com mouse, tocar com o dedo e
  clicar** — os três, sempre.
- **A `.pc` do molde vem SEM fundo** (na atividade de origem ela ganhava cor de
  uma classe de forma). Reaproveitada aqui, virou texto branco solto no ar: uma
  peça que a criança deve PEGAR tem que parecer pegável. Deu 2,76:1 de contraste
  no auditor, além de ficar feio.

### 🐛 De brinde: pré-carga de imagem apontando para outra atividade
A Fábrica **e a Doceria** pré-carregavam 16 imagens da Legenda do Clique
(`cq_*`, `nm_*`) — 16 requisições 404 e **nenhuma** imagem própria pré-carregada.
Veio junto no clone do motor e ninguém tinha percebido. Nos PCs fracos da escola
isso significa cada imagem aparecendo com atraso na primeira vez. Corrigido nas
duas. **Ao clonar um motor, o `var IMGS=[...]` é conteúdo, não motor** — trocar
junto com o `DOM` e o `VOZOK`.

## 😬 O MASCOTE TREMIA AO FALAR E PISCAR — e por quê (Marcos, ago/2026)

Palavras dele: *"ao falar ou piscar o mascote se treme todo, não deveria"*. Na
rodada anterior eu tinha suavizado o giro do flutuar e achado que era isso.
**Não era.** Fui medir e o número não deixou dúvida.

**A causa:** o mascote são TRÊS imagens empilhadas (parado / falando / piscando)
e o motor faz o cruzamento delas ~60 vezes por segundo para o lip-sync. Eu gerei
as três **do zero**, em três prompts separados — e a IA devolve **três desenhos
diferentes**, por mais que o prompt diga "exatamente igual". Na Fábrica, a pose
de piscar veio até com **outro tom de pele e outro cabelo**. Cruzar isso a 60fps
não anima a boca: **morfa o boneco inteiro**.

**A medida que denuncia** — quantos % dos pixels do corpo mudam entre a pose
parada e cada outra:

| atividade | falar | piscar |
|---|---|---|
| Legenda do Clique | 1% | 2% |
| Jardim do Broto | 2% | 7% |
| Doceria do Cacau | 6% | 5% |
| Observatório do Órbi | 8% | 3% |
| **Fábrica (errada)** | **77%** | **78%** |

As outras quatro estavam boas porque nasceram de EDIÇÃO da pose parada. A Fábrica
foi a única que eu fiz do zero — erro meu, e o Marcos viu na tela antes de
qualquer auditor meu ver.

### ⭐ REGRA NOVA (não negociável)
**As poses de FALAR e PISCAR nunca se geram do zero.** Geram-se EDITANDO a pose
parada, com o `gerar-imagens.yml`: `modelo=gemini` + `base=_novo/<mascote>_base.png`,
pedindo para mudar SÓ a boca (ou só os olhos) e mais nada. Funcionou de primeira:
caiu de **77% para 2,8%** (falar) e **4,5%** (piscar). Depois recortar as três com
a **mesma bbox** (senão a imagem pula ao trocar de camada).

### 🕵️ AUDITOR NOVO — `_qa/mascote.py` (portão **3d** da banca)
Mede essa porcentagem e reprova acima de **15%**. Também reprova camada com
tamanho diferente da parada. Testado: reprova a Fábrica velha e aprova as outras
quatro — ou seja, o limiar está calibrado na realidade do projeto, não no chute.

**Lição maior:** a IA não obedece "mantenha exatamente igual" quando gera do
zero. Quando duas imagens precisam ser o MESMO desenho, o caminho é **editar**,
nunca **regerar** — e depois **medir**, porque no print parado as três parecem
iguais; o defeito só existe em movimento.

## 📌 A RODADA DA FÁBRICA VIROU MANUAL: `_padrao/CLONAR-MOTOR.md` (ago/2026)

Marcos: **"anote tudo para não acontecer mais"**. Anotado em três camadas, porque
o que fica só na memória eu esqueço e o que fica só escrito eu não cumpro:

1. **`_padrao/CLONAR-MOTOR.md`** — o manual completo: a tabela do que é CONTEÚDO
   e tem que trocar ao clonar, o caso do mascote com a medida de todas as
   atividades, o guarda do evento fantasma no arrasto, e a ordem de trabalho que
   funcionou.
2. **`CLAUDE.md`** — o ponteiro curto, logo abaixo do `FIM-DE-ATIVIDADE.md`, com
   as três armadilhas maiores em destaque. É o arquivo que eu leio no começo de
   TODA sessão.
3. **A banca** — o que dá para medir virou portão. De 7 para **12**.

### Os portões novos desta rodada
| portão | o que pega | defeito que o gerou |
|---|---|---|
| **1b** `funcoes.py` | função chamada que não existe | `normal()` faltando travava a última fase da Legenda |
| **1c** `clone.py` | resto da atividade de origem | pré-carga, alto-falante, conceitos e falas apontando para outra atividade |
| **3b** `progressao.py` | barra andando para trás | 3 atividades com a ordem trocada |
| **3c** `arte_propria.py` | imagem copiada de outra | avatares do Jardim dentro do Órbi |
| **3d** `mascote.py` | mascote que treme | as 3 camadas eram desenhos diferentes |

### ⚠️ O que o portão 1c achou de quebra, em atividade JÁ PUBLICADA
- **Legenda do Clique: 9 falas sem MP3** — três fases inteiras (filtro mágico,
  detetive da redação, encolhe e aumenta) com o **mascote MUDO**: sem introdução,
  sem dica falada, sem a revelação do conceito. Ninguém tinha visto porque a tela
  funciona perfeitamente; só o som some. Gravadas e publicadas.
- **Fábrica e Doceria: pré-carga apontando para as imagens da Legenda** — 16
  requisições 404 e nenhuma imagem própria pré-carregada.

**A lição que amarra tudo:** os defeitos desta rodada não davam erro. O
`node --check` passava, o app abria, o print ficava bonito. Eles só existem
**em movimento** (o mascote tremendo), **no dedo** (o toque que não entrega),
**no ouvido** (a fase muda) ou **no tempo** (a imagem que demora). Portão que
olha só o código não pega nenhum deles — por isso a banca precisa **medir,
tocar, ouvir e jogar**, não só ler.

## 🔑 CÓDIGO MESTRE `1275@` — o professor testa sem jogar tudo (Marcos, ago/2026)

Palavras dele: *"coloque um código 1275@ para que eu possa testar as atividades
sem precisar passar por todas. Tipo uma senha mestra"*.

**Onde se digita:** no **campo do NOME**, na tela de identidade ("Quem vai
jogar?"). Digita `1275@`, aperta o botão e abre o **MODO PROFESSOR**: a lista de
todas as fases, cada uma num botãozinho, e um toque abre a fase direto.

**Por que aí e não num botão:** a criança nunca descobre (não existe botão
nenhum na tela), e o professor entra em dois toques. É a mesma ideia do
relatório atrás do gesto de segurar a medalha 2 segundos.

**Não mexe em nada do aluno:** não zera progresso, não grava nome, não conta
acerto. É só um atalho para abrir a tela.

**Está nas CINCO:** Órbi (21 fases), Jardim (17), Doceria (25), Legenda (20) e
Fábrica (23).

**Como a lista se monta (para repetir em atividade nova):** o instalador lê o
próprio arquivo, pega toda função que chama `setProg()` e ordena pela
porcentagem — que é a ordem do percurso. O rótulo vem do `selo` da tela, que é o
título que a criança vê. Ou seja, a lista nunca fica desatualizada em relação às
fases de verdade.

---

## 🐛 "A ESTEIRA QUE PULA" ESTAVA SEM AS MARCAS (Marcos, ago/2026)

Palavras dele: *"falta a marca ou a linha para o estudante clicar"*. E era isso
mesmo.

**A causa:** a `.marca` do molde só aparece se tiver os **filhos** `<i>` (o
tracinho da régua) e `<b>` (o número) — o CSS estiliza `.reta .marca i` e
`.reta .marca b`, não a `div` sozinha. Eu tinha criado `el("div","marca",valor)`,
com o número no innerHTML e sem filho nenhum: a criança via números soltos, sem
tracinho, sem régua e sem alvo claro para tocar.

**O conserto** (copiando o `dSalto` da Doceria, que estava certo): cada marca é
`<i></i><b>número</b>`, a marca do zero já nasce acesa, e o **Bento pula de marca
em marca** (`.salta`, posicionado por `offsetLeft`), que é o que faz a criança
VER o salto em vez de só ler números.

**Lição:** ao reusar uma classe do molde, olhar **o CSS dela** — se ele estiliza
FILHOS, montar os filhos. "Tem regra base" (portão 3) não quer dizer "está com a
cara certa"; é a segunda vez que essa mesma armadilha morde (a primeira foi a
`.pc` sem fundo).

---

## 🃏 Carta de jogo da memória é SEMPRE grande (regra permanente — ago/2026)

Palavras do Marcos: *"lembre-se quando fizer jogo da memória faça cartas maiores,
registre para sempre fazer isso"*.

**Por que é regra e não gosto pessoal:** a carta de memória é o alvo mais difícil
que existe numa atividade. A criança precisa (1) **ver a figura**, (2) **ler a
palavra** e (3) **lembrar onde ela estava**. Carta pequena mata as três de uma vez
— e no caso da leitura, quem ainda soletra simplesmente desiste.

**O molde certo (carta FLUIDA, nunca px fixo):**

```css
.mcartas{...;max-width:430px;width:100%}
.mcarta{width:48%;max-width:210px;min-height:100px;...}
@media (max-height:720px){ .mcarta{min-height:92px;font-size:13.5px} }  /* encolhe a LETRA */
@media (min-width:760px){ .mcartas{max-width:680px} }                   /* PC: 3 colunas */
```

**O erro que isso corrige:** o molde vinha com `width:126px;height:78px` e, na
janela baixa, encolhia a CARTA para 116×68. Com px fixo a carta não aproveita a
tela: num celular de 412px ela ficava com 128px de largura quando cabiam 182px.
Medido depois da troca: **128×80 → 182×100** no celular comum (+78% de área) e
**210×100** no PC, onde o tabuleiro inteiro passou a caber **sem rolar**.

**Aplicado em:** `_orbi`, `_fabrica`, `_doceria`, `_nomes`, `_jardim` (todos os
que têm fase de memória).

**Auditor:** `_qa/leiaute.js`, **regra 6** — mede toda `.mcarta` visível nos 6
tamanhos de tela e reprova abaixo de **130 × 88 px**. Não dá mais para esquecer.

---

## 🧩 A Legenda do Clique ganhou seis dinâmicas novas (ago/2026)

Pedido do Marcos: *"precisamos melhorar e aumentar a dinâmicas de interatividade
na atividade dos substantivos e adjetivos... tem muita dinâmica parecida como
está agora, lembre-se que temos um leque bem grande de interatividade"* + *"pode
incluir algumas atividade onde o aluno tenha que digitar"*.

**O diagnóstico medido (antes de mexer):** agrupando as 19 fases pelo GESTO, e
não pelo conteúdo, **8 delas eram o mesmo gesto** (tocar na opção/peça certa) e
**só UMA pedia para escrever**. Cinco fases seguidas usavam a mesma `.pc` na
mesma posição da tela.

**Entraram (4 gestos que a atividade não tinha):**
- **Marca-texto do revisor** — pinta TODOS os nomes de um parágrafo, depois
  todos os adjetivos (gesto: marcar vários).
- **Complete a legenda** (digitar) — a palavra vem na forma base e a criança
  arruma o fim. A dica CRESCE: 1º o porquê, 2º a palavra quase pronta, 3º a
  resposta.
- **Ordene a legenda** (arrastar para sequenciar) — o arrasto que existia
  encaixava por FORMA; aqui a ORDEM manda.
- **Termômetro do grau** (`input type=range`) — a foto cresce e encolhe junto
  com a palavra.
- **Ditado do editor** (escrever ouvindo) — o Clique dita, a criança escreve,
  pode ouvir quantas vezes quiser.
- **Manchete do jornal** — contador ao vivo ("nome ✓ / adjetivos 1 de 2")
  enquanto digita: andaime DURANTE, não correção no fim.

**Saíram:** `nPlural`, `nGenero` (viraram o Complete), `nGrau` (virou o
Termômetro) e `nRevisor` (virou o Marca-texto). Nenhum conteúdo da BNCC se
perdeu. Resultado: **de 1 para 4 fases de escrever** e **de 3 para 7 gestos**.
22 telas, ~60 min.

### Dois defeitos achados de passagem (os dois estavam NO AR)

**1. `\n` LITERAL dentro do CSS.** No `_nomes` havia `}\n.pc.fantasma{...}`
escrito com barra-n de texto. Em CSS isso vira o seletor `n.pc.fantasma` (um
elemento `<n>`), que nunca casa. Resultado: no arrasto da Bancada a cópia da
peça **não seguia o dedo** — aparecia solta no fim da página — e a vaga não
acendia. Só o `_nomes` tinha; conferido nos 5 apps.

**2. ⭐ SERVICE WORKER: uma atividade apagava o offline das outras.** Todas as
atividades moram no MESMO endereço (`vidalprof.github.io`), então **dividem o
mesmo armazenamento de cache do navegador**. Dois problemas vinham daí:
- a Legenda tinha o `sw.js` inteiro da Redação (resto de clone): cache chamado
  `redacao-pingo-v1` e lista de pré-carga pedindo `img/vb_pingo.png`,
  `vg_conto.png`, `vb_abertura.mp3` — arquivos que não existem nela. Nunca
  pré-carregou nada. A Fábrica tinha o mesmo, com a lista da Doceria (9 arquivos).
- o `activate` de toda atividade apagava **qualquer** cache com nome diferente
  do seu. Abrir a Fábrica DELETAVA o offline do Órbi, do Jardim, da Doceria.

**Conserto nas 6:** `var PREFIXO="<atividade>-"` + `CACHE=PREFIXO+"vN"`, e o
`activate` só apaga `k.indexOf(PREFIXO)===0`. Listas refeitas.
**Auditor:** `_qa/clone.py` item 6 — reprova nome de cache igual ao de outra
atividade, apagador sem prefixo, e lista apontando para arquivo inexistente.
Testado com o defeito plantado: os três casos reprovam.

---

## ⭐⭐ O PADRÃO DA CASA virou portão (ago/2026)

Palavras do Marcos, já na sétima atividade: *"ela tem que ser bem didática
progressiva didaticamente, bem ilustrada, sonora lembra? isso deve ser guardado
para todas as atividades a serem produzidas, se isso já não estiver guardado"*.

Conferi: **não estava guardado em lugar nenhum** — nem no `CLAUDE.md`, nem no
`MANUAL-MESTRE.md`. Era costume, e costume um dia sai errado. Agora está escrito
no `CLAUDE.md` (bloco "O PADRÃO DA CASA") **e medido** pelo `_qa/padrao.py`
(portão 0b da banca).

**Os 4 pilares:** (1) didática e progressiva — problema primeiro, conceito por
último, andaime que cresce, aquecimento no meio, nunca prova disfarçada;
(2) bem ilustrada — arte de IA própria, nunca emoji, nunca arte copiada;
(3) sonora — toda tela narrada + alto-falante nas respostas; (4) leque grande de
interatividade — **contar GESTOS, não conteúdos**.

**O auditor reprova** se um gesto passar de 40% das fases, se houver menos de 4
gestos diferentes, ou se alguma fase estiver muda. Ele ignora as telas puramente
narrativas (só o botão de seguir) e nunca reprova pelo balde "outro", que
significa "não classifiquei" e não "um gesto só".

### Medição de estreia (o retrato honesto das 6 atividades)

| Atividade | Gesto que domina | Veredito |
|---|---|---|
| Legenda do Clique | digitar 21% (12 gestos) | **passa** — é a que acabou de ser tratada |
| Órbi | escolher 38% (5 gestos) | passa |
| Jardim do Broto | escolher 33% | passa |
| Plantão na Redação | escolher/outro 35% | passa (1 fase muda: `telaMenu`) |
| **Doceria do Cacau** | **escolher 64%** | **reprova** |
| **Fábrica do Bento** | **escolher 84%** (16 de 19) | **reprova** |

As duas que reprovam são as de **matemática** — e é o mesmo defeito que o Marcos
pegou na Legenda, só que pior. **Ficam na fila** para receber o mesmo tratamento
(trocar fases de "toque na resposta" por digitar, ordenar, deslizar, pintar).

---

## 🕰️ A MÁQUINA DO TEMPO DO VALE — 4º ano, História (ago/2026)

**Pedido:** professora do 4º ano, EF04HI01 — *"reconhecer a história como resultado
da ação do ser humano no tempo e no espaço, com base na identificação de mudanças
e permanências ao longo do tempo"*. O Marcos mandou fazer **pelo currículo de
Blumenau**, *"bem sonora e imagens"*, *"as melhores dinâmicas interativas bem
variadas"*, *"tem que durar uma aula inteira"*, com **post-it de curiosidades**,
e — com todas as letras — *"pesquise a fundo, não cometa erros, não invente"*.

- **Pasta:** `_historia/` · **Repo:** `maquina-do-tempo-do-vale`
- **Mascote:** **Juca**, bugio-ruivo · prefixo `hv_` · 37 imagens · 69 narrações
- **24 telas, ~55 min, 11 gestos diferentes** (máximo 21% num só gesto)

**O currículo bateu melhor do que o esperado.** As três unidades temáticas de
História do 4º ano de Blumenau são, ao pé da letra: *"Transformações e
permanências nas trajetórias dos grupos humanos no Vale do Itajaí"*,
*"Circulação de pessoas, produtos e culturas"* e *"As questões históricas
relativas às migrações no Vale do Itajaí"* — com os objetos de conhecimento
nomadismo/sedentarismo, *"Por que os povos migram?"*, *"os grupos indígenas, a
presença portuguesa e a diáspora forçada dos africanos"* e *"relacionar os
processos de ocupação do campo a intervenções na natureza, avaliando os
resultados"*. Está tudo em `_curriculo/blumenau.txt`, a partir do byte 1322228.

### Os dois carros-chefe (simuladores)
- **A Janela do Tempo:** a criança desliza os anos e a MESMA janela do Vale vira
  mata → aldeia Xokleng → barco de 1850 → colônia de 1875 → roça no morro →
  cidade. O rio e as montanhas continuam em todas. A EF04HI01 acontece ali,
  antes de qualquer explicação.
- **A Água Sobe:** chove igual nos três casos; a criança escolhe quanta mata
  ficou no morro e vê até onde a água chega na cidade. É o objetivo de
  "intervenções na natureza" virando coisa que se mexe.

### FORCA sem forca
Mecânica nova (o Marcos pediu). **Não tem boneco enforcado:** quem sobe a cada
erro é a **enchente** na régua do rio. Se a água chega ao topo, a palavra se abre
e a criança segue — ninguém fica preso nem perde nada.

### ⚠️ A PESQUISA PEGOU DOIS ERROS MEUS antes de irem para a tela
1. Eu ia ensinar que **a maior enchente de Blumenau foi a de 1983**. **NÃO FOI.**
   A maior medida foi **1880 (17,10 m)**; depois 1911 (16,90), 1984 (15,46) e só
   então 1983 (15,34).
2. A linha do tempo dizia *"1880: as primeiras casas"*. As primeiras casas são de
   **1850**.
Conferidos e confirmados: fundação em **2/9/1850 com 17 pessoas**; **açorianos a
partir de 1748**; **italianos em 1875** (Rio dos Cedros, Rodeio); **Xokleng** no
Vale, Kaingang nas terras altas, Guarani perto do litoral; **Oktoberfest em 1984**
depois das enchentes; "Itajaí" vem do tupi e **o significado exato ainda é
discutido** — isso virou post-it, porque história também tem pergunta em aberto.
**Lição:** todo número e toda data que vai para a tela é PESQUISADO. Post-it é o
que a criança leva para casa; professor não tem tempo de desmentir.

### O auditor jogador aprendeu QUATRO coisas nesta atividade
1. **Deslizar:** não sabia usar `input[type=range]`. Agora percorre todas as
   posições do menor ao maior (ir "um passo para o lado" ficava indo e voltando
   entre as duas últimas e nunca via a primeira).
2. **`#bcta` fantasma:** o botão do banner fica sempre no DOM (o banner se esconde
   por `transform`, não por `display`) e guarda o `onclick` do banner ANTERIOR —
   clicar nele jogava o jogador de volta para a fase passada, em loop.
3. **Campo de texto não faz fase andar:** a carta usava a classe `.carta` (a mesma
   das cartas do Órbi) e ele clicava no campo em vez do botão Enviar.
4. **Ele não ROLAVA a tela.** Dava "preso" numa fase que funciona, só porque o
   botão ficava abaixo da dobra. Uma criança rolaria; agora ele também.

---

## ⌨️🔊 As duas portas de entrada + o alto-falante (regras permanentes, ago/2026)

Duas regras que o Marcos pediu para valer em **todas as próximas atividades**, e
que nasceram enquanto a Máquina do Tempo era montada.

### 1. Teclado na tela? Então teclado de verdade também.
*"essa dinâmica de aceitar também o teclado seria interessante registrar para
todas as próximas atividades"*.

Toda fase que desenha letras para tocar — **cruzadinha, forca, monte a palavra** —
tem que escutar `document.onkeydown` além do clique. No PC da escola a criança tem
o teclado na frente e é natural que ela digite; no celular não tem teclado nenhum.
As duas portas ficam abertas e levam ao mesmo lugar.

Molde (o mesmo nas duas fases da Máquina do Tempo):
```js
document.onkeydown=function(ev){
  var L=String.fromCharCode(ev.keyCode||ev.which||0).toUpperCase();
  if(!/^[A-Z]$/.test(L)) return;
  /* acha a tecla NA TELA com essa letra e dispara o MESMO caminho do toque */
};
```
⚠️ `limpa()` faz `document.onkeydown=null` — senão a fase seguinte continuaria
escutando as teclas da anterior.

É irmã da regra do arrasto (*"quero as duas opções funcionando"*): onde há
arrastar, o **toque simples** também resolve.

**Auditor:** `_qa/padrao.py`, item 4 — fase com `.tec`/`.teclafc` sem `keydown`
reprova. Testado com o defeito plantado.

### 2. Alto-falante em toda resposta.
*"o alto-falante nas respostas também, para ajudar os alunos que não sabem ler"*.

Toda resposta tocável ganha um botãozinho de voz (`op_<chave>.mp3`, chave djb2 em
base36, registrada em `VOZOK`; o `ZAPSEL` + MutationObserver põe o botão sozinho).
No 4º ano ainda há quem soletre: **sem a voz, a criança escolhe pelo desenho e a
atividade vira loteria.** Na Máquina do Tempo foram **70 vozes de resposta**.

⚠️ A chave tem que ser calculada com **o mesmo hash do app** (djb2 `(h<<5)+h+c`,
base36) sobre o texto **já sem tags e com as entidades resolvidas** — é o
`textContent` que o app usa. Chave errada = botão que não faz nada, que é pior
que botão nenhum.

---

## 💾 CONTINUAR DE ONDE PAROU (55 min) — regra permanente (ago/2026)

Palavras do Marcos: *"outra coisa é ter a opção de continuar de onde parou caso
o aluno saia sem querer, e isso durar o tempo de uma aula 55 minutos tem como?
pode ser aplicado a toda atividade nova criada"*.

**Sim, tem — e já está feito.** Estreou em *A Máquina do Tempo do Vale*. O
código completo, com as armadilhas, está no **`_padrao/RETOMAR.md`** (copiar,
não reescrever). Resumo do que importa lembrar:

- a cada fase que abre, o app anota o **nome da fase** e a **hora** no
  `localStorage` (junto do `MED`, do `DOM` e do crachá, que já eram salvos);
- voltando **dentro de 55 minutos**, a capa oferece **"Continuar de onde parei"**
  (dourado, antes do "Começar") e volta para a MESMA fase, com o mesmo crachá e
  o mesmo domínio;
- passados os 55 min o convite **some sozinho** — a aula seguinte é outra turma,
  e ela não pode cair no meio da viagem de um colega;
- "Começar do início" chama `zeraProgresso()` de verdade, senão o boletim mente.

**Três armadilhas que custaram (ou custariam) caro:**

1. **A ordem do gancho.** O envelope das fases tem que rodar DEPOIS das funções
   existirem e **ANTES** do objeto `TREINO`, que guarda as funções por
   referência. Envelope depois = o "Treinar o que faltou" chama as versões
   antigas e não anota nada — e nada dá erro, a retomada só mente.
2. **`carrega()` tem que restaurar o `MED` também**, senão a criança volta na
   fase certa com o relatório do professor zerado.
3. **`localStorage` não funciona em `file://`.** O teste tem que servir por
   `http://` (Playwright + `page.route`). Testar em `file://` dá "passou" falso.

Testado nos três casos (salva / recarrega e volta / expira em 56 min): passou.

**Achado de brinde:** o `zeraProgresso()` da Máquina do Tempo ainda zerava com os
conceitos da **Legenda do Clique** (`reconhecer/grupo/concordancia/morfologia`) —
mais um resto de clone, do mesmo parentesco dos do `_padrao/CLONAR-MOTOR.md`.
Quem trocasse de nome ficava com o boletim errado. Corrigido.

**Senha mestra:** `1275@` — sim, está guardada (MANUAL-MESTRE.md, "MODO
PROFESSOR"). Digitar a qualquer momento abre o menu de fases para o professor
testar; não altera o progresso do aluno e não é segurança (está no código).

## 🌱 Jardim do Broto — dois consertos pedidos pelo Marcos (ago/2026)

1. **"Monte seu prato": no máximo 5.** Palavras dele: *"não permitir o aluno
   colocar mais de 5, para a comida não ficar de fora, que fica visualmente
   feio"*. Dava para empilhar alimento sem conta e a comida transbordava do
   prato. Agora o prato tem **5 lugares** (`MAXPRATO`) — e como a fase pede 5
   partes diferentes, cada lugar vale uma parte. Para não haver beco sem saída,
   **tocar num alimento do prato tira ele de volta**, e o prato **balança**
   avisando quando está cheio (nada de o toque sumir em silêncio). O prato
   cresceu para 212px para os cinco caberem em 3+2 sem transbordar.
2. **"Olhe de perto" não corta mais.** O quadro tinha `scale(1.35)` dentro de um
   `overflow:hidden`: a imagem aparecia grande e com as **beiradas cortadas** — e
   é justamente o FORMATO inteiro que a criança precisa ver para dizer se é
   raiz, folha ou fruto. Agora o quadro é maior (212×176) e a imagem entra
   inteira (`contain`), sem zoom que corte.

**Brinde do mesmo dia (Jardim):** a fase "Monte a palavra" ganhou o **teclado de
verdade** (regra das duas portas) e, no caminho, apareceu um vazamento antigo: o
`setTimeout(pede,780)` da próxima palavra continuava correndo **depois** de a
tela ter trocado e reinstalava o `document.onkeydown` da fase anterior por cima
da seguinte. Trava: `if(!t.parentNode) return;` no começo do `pede()`, e
`limpa()` do Jardim agora solta o teclado como o das outras.

**E um portão que morria calado:** o item 4 do `_qa/padrao.py` (teclado virtual
sem teclado físico) estourava `NameError` justamente na primeira atividade que
tinha o defeito — a lista `problemas` ainda não existia naquele ponto do
arquivo. Portão que morre na hora de falar é pior que portão que não existe.

---

## 🚫 "RESTO DE CLONE NUNCA MAIS" — o dia em que virou medida (ago/2026)

Ordem do Marcos: *"favor não poder mais haver resto do clone, faça com que isso
não aconteça mais"* e *"tem que aprender com os erros automaticamente e eles não
podem se repetir nas outras atividades"*.

O que ele viu: no jogo da memória da Máquina do Tempo aparecia um **quadradinho
vazio** em cima das cartas. O verso apontava para `img/cq_base.png` — arquivo de
OUTRA atividade, que nunca existiu nesta pasta.

**Por que nenhum portão pegou:** o `node --check` não abre imagem; o de leiaute
mede retângulos (e o quadradinho quebrado TEM retângulo); o de contraste olha
texto; o jogador clica e segue. O app funcionava inteiro com a figura faltando.

**Os dois portões novos (é isto que impede a repetição):**

1. **`_qa/imagens.js` (portão 1e)** — abre a atividade no navegador, percorre as
   telas e a pré-carga, e reprova **qualquer `<img>` que terminou de carregar com
   `naturalWidth === 0`**. É a conta que importa: a figura apareceu para a
   criança ou não?
2. **`_qa/clone.py` item 8 — PREFIXO ALHEIO.** Os itens 1–7 pegavam um TIPO de
   resto cada um, e a cada rodada surgia um tipo novo. Este não pergunta o tipo:
   descobre o prefixo desta atividade pelos arquivos de `img/` e `audio/`
   (`hv_`, `jd_`, `fb_`…), descobre o das outras, e **reprova qualquer marca de
   outra pasta** — imagem, voz, variável ou comentário.

**O que o item 8 achou no primeiro minuto de vida:** `vb_acerto1` na Máquina do
Tempo. As funções `elogio()` e `consolo()` — chamadas **18 vezes** pelo motor —
apontavam para os MP3 da atividade dos **Verbos**, que não existem nesta pasta.
Ou seja: **a atividade inteira estava muda justamente nos momentos de encorajar
a criança que errou**, e nada dava erro. Geradas as cinco falas do Juca
(`hv_acerto1/2/3`, `hv_erro1/2`).

**A regra que ficou:** todo defeito que chega ao Marcos tem conserto em DUAS
partes — arrumar o código **e** criar/estender o portão que o pega sozinho da
próxima vez. Sem a segunda parte, o trabalho não está feito.

## 🃏 O jogo da memória virou padrão da casa (ago/2026)

Palavras dele: *"os jogos da memória tem que ter bastante efeitos e sons, devem
ficar lindos, tamanho maior, claro adequando a tela, chamar atenção do
estudante"*. O molde, já aplicado na Máquina do Tempo:

- carta fluida ≥ **130×88** (na prática ficou **180×118**), medida pelo leiaute;
- **verso de arte de IA** (couro com relógio de bolso dourado) — nunca retângulo;
- **virada 3D de verdade** (`rotateY` + `preserve-3d` + `backface-visibility`),
  com queda para troca-de-face (`.semgiro`) no Chrome antigo da escola;
- **brilho dourado correndo** pelo verso, que é o que faz a mesa "chamar";
- par que **pulsa**, acende e solta duas fagulhas; **placar "N de M pares"**;
- **som próprio** de virar (madeira) e de formar par (arpejo), festa no fim.

⚠️ Ao fazer isso, o portão do contraste reprovou 8 cartas: ele media a letra da
FACE DA FRENTE (que existe no DOM mas está virada para trás) contra o couro do
verso. Texto que não está à mostra não tem contraste ruim — o portão aprendeu a
perguntar "quem recebe o dedo no centro deste texto?" antes de medir.

## 🎨 Interação dinâmica usa arte de IA (regra permanente, ago/2026)

*"nas interações dinâmicas sempre usar imagens geradas pela IA, como aconteceu na
água que sobe na atividade de história, pois ficou lindo e profissional"*.
Simulador, verso de carta, peça de arrastar, cenário que muda: a FIGURA é gerada;
o CSS entra só no que precisa se mexer em tempo real (a água subindo, a carta
girando). No mesmo dia ele reprovou dois desenhos de CSS — o morro de retângulo
verde com palitinhos e o quadradinho da forca.

## ⚡ A produção ficou 3x mais rápida (pedido: "otimize todo o processo")

- **`fetch-depth: 1` em 24 workflows.** O histórico do repositório passa de 1 GB
  (toda imagem e todo áudio de toda atividade estão nele) e o checkout sozinho
  levava **12 minutos** — publicar duas atividades ao mesmo tempo empacava. Com o
  checkout raso, a geração de áudio passou a landar em **1 minuto**. O clone do
  destino no `atualizar.yml` também virou `--depth 1`.
- **A banca roda em paralelo:** contraste, leiaute, jogador e imagens saem juntos
  na frente (são eles que seguram o relógio) enquanto os portões de texto rodam.
  **164s** no lugar de ~9 min. E saiu o `2>/dev/null`: portão que imprime nada
  não é "passou", é "rodou cego".
- **O portão do jogador passou a VOTAR.** Até hoje a saída dele ia para um
  `tail -4` e o código de saída se perdia no cano: ele jogava a partida inteira e
  o resultado era decorativo. Agora reprova se não chegar à medalha ou se houver
  erro de JS na partida.
- **Gemini 503 não para mais a produção:** insiste (5s/15s/40s) e, se ainda assim
  falhar, cai no Pollinations. Só para quando é EDIÇÃO de imagem base, que o
  Pollinations não faz.

---

## 🗺️ O VOO DO NICO — Geografia, 3º ano (ago/2026)

**Currículo de Blumenau, 3º ano**, unidade *"Formas de representação e pensamento
espacial"*, objeto *"Representações cartográficas em Blumenau"* — os dois
objetivos, verbatim: *"Identificar e interpretar imagens bidimensionais e
tridimensionais em diferentes tipos de representação cartográfica"* e
*"Reconhecer e elaborar legendas com símbolos de diversos tipos de representações
em diferentes escalas cartográficas"*.

⚠️ O Marcos pediu primeiro como **2º ano**; fui ao documento e os dois objetivos
estão na tabela do **3º ano**. Avisei, ele confirmou 3º ano. **Sempre conferir o
ano no `_curriculo/blumenau.txt` antes de montar** — o 2º ano tem os parentes
mais novos (visão vertical × oblíqua, maquete, direita/esquerda).

- **Pasta:** `_mapa/` · **prefixo `mp_`** · 20 fases, 24 telas, **11 gestos**
- **Mascote: Nico, um joão-de-barro** — o bicho que constrói a própria casa e
  que, voando, vê tudo de cima. "Visão de pássaro" virou o ponto de vista do
  personagem, não uma figura de linguagem.

**A mecânica nova: O VOO.** A criança desliza a altura e a MESMA praça (mesma
igreja, mesmas quatro casas, mesmo rio, mesma ponte) passa de vista de lado →
inclinada → reta de cima, que já é um mapa. **A passagem do 3D para o 2D
acontece na mão dela** — que é exatamente o que o objetivo pede. Depois vêm o
**roteiro com setas** (ela monta o caminho e o Nico voa), o **monte a legenda**
(o verbo do currículo é *elaborar*, não só reconhecer) e a **escala** (sala →
escola → bairro → cidade).

### Lições desta rodada (todas viraram portão ou regra)

1. **Chave base36 sem aspas derruba o JS inteiro.** `var VOZOK={13tpllt:1}` não
   é JavaScript válido. O portão 1 pegou.
2. **Classe passada como ARGUMENTO escapava do portão 3.** `cenaImg(n,"jimg")`
   não era vista, e a `.jimg` ficou sem regra: a figura do mapa vinha no tamanho
   natural (860px) e a fase do roteiro ficava com **1900px de altura** — a
   criança não via o mapa e as setas juntos. `_qa/classes.py` agora lê
   `cenaImg(...)`/`imgEl(...)` também.
3. **Alvo posicionado pelo canto, não pelo centro.** `.achado` com `left/top` em
   % nascia deslocado meia largura: a criança tocava na igreja e levava "errado".
   Classe `.achado.mira` com margem negativa.
4. **Coordenada chutada é erro pago.** As posições dos alvos agora são MEDIDAS na
   arte (a igreja está a 32% × 28% do mapa), não estimadas.
5. **O auditor jogador aprendeu três coisas:** que `.pc` nem sempre é peça de
   arrastar (no roteiro é botão de ação, e a tela diz qual serve agora); que
   existe o molde `.peca` → linha com `data-vaga`; e que **há DOIS moldes de
   caça-palavras** na casa (por extremos e letra-por-letra) — ele pergunta à
   tela em qual está antes de clicar.
6. **Manifesto com nome alheio** (portão 9 do `clone.py`): o da Máquina do Tempo
   ainda dizia "A Legenda do Pingo" — é o nome que apareceria ao instalar no
   celular.

### Quando o gerador de imagem cai

O Gemini esgotou a cota diária no meio da produção e o Pollinations ficou horas
devolvendo 500. O que ficou de aprendizado, já no código: os workflows **esperam
de verdade** (20s/60s/90s), o lote **commita o que deu certo**, o Pollinations
tenta **quatro motores** e o `gerar-imagens.yml` cai do Gemini para o
Pollinations sozinho — menos quando é EDIÇÃO de imagem base, que só o Gemini faz.
Nessa hora o Marcos gerou as três últimas no ChatGPT e subiu pelo GitHub.

**⭐ E daí saiu uma técnica que vale para sempre:** ele mandou as duas poses do
mascote num print só, e elas eram um render NOVO (não edição da base) — o que
faria o boneco tremer. Solução: **construir as três camadas de UMA imagem só**.
Da pose "piscando" (bico fechado) tirei o corpo; colei os **olhos abertos** da
pose "falando" → nasceu o *parado*; e desse colei o **bico aberto** → nasceu o
*falando*. Corpo pixel-idêntico nas três: tremor de **1,0% e 2,6%** (o limite é
15%). Guardar esta receita: é mais confiável que pedir três gerações.

**Publicada em 05/08/2026:** `_mapa/` → repositório **`o-voo-do-nico`** →
**https://vidalprof.github.io/o-voo-do-nico/** (Pages `status=built`, sem erro).
Não entrou no hub — continua valendo a regra de não pôr atividade nova no
`_site` até o Marcos pedir.

**⭐ Autorização permanente de publicação (05/08/2026):** *"pode publicar, pode
sempre publicar a menos que eu diga para esperar"*. Terminou e a banca aprovou →
publica e manda o link, sem perguntar. Só para quando ele disser "espere", e essa
pausa vale só para aquele trabalho.

## ⚠️ O NOME DA ATIVIDADE DE ORIGEM NA CARA DA CRIANÇA (ago/2026)

O Marcos cobrou **duas vezes**, e a segunda com razão: *"o nome da atividade
copiou de história, já avisei sobre isso e você me disse que não iria mais
acontecer"*. Na cartografia sobraram **três** lugares dizendo "A Máquina do Tempo
do Vale": o `<title>`, o **H1 DA CAPA** (a criança lê!) e o cabeçalho do
relatório do professor — este ainda com "(4º ano)".

**Por que escapou de tudo:** o item 8 do `clone.py` procura PREFIXO (`hv_`), e
nome de atividade não tem prefixo. E a minha troca à mão falhou porque **o mesmo
texto aparece com ACENTO e com ENTIDADE** (`A Máquina...` e `A M&#225;quina...`):
o replace pegou duas ocorrências e deixou a terceira.

**Portão 10 do `_qa/clone.py`:** resolve as entidades e reprova se o `<title>` de
QUALQUER atividade vizinha aparecer no texto desta. Exceção só para o hub, cujo
trabalho é justamente listar as atividades pelo nome. O `nova-atividade.sh`
também passou a trocar as duas formas.

**E uma lição sobre o próprio portão:** na primeira versão o bloco usava
`io.open()` sem importar `io`; o `NameError` caía num `except: continue` e a
lista de vizinhas vinha **vazia** — o portão dizia "ok" sem ter olhado nada.
**Portão que engole o próprio erro é pior que portão nenhum.** Nada de
`except: continue` em portão: se quebrou, tem que aparecer.

## ⚠️ E A HISTÓRIA DA OUTRA ATIVIDADE NA BOCA DO MASCOTE (ago/2026)

Logo depois de eu corrigir o NOME, o Marcos perguntou: *"a atividade não copiou
no fim a de história?"* — e tinha copiado. Duas frases, nas duas telas de maior
peso emocional:

- a **tela da medalha**: *"a viagem no tempo está completa"*;
- a **tela de entrada**: *"Quem vai viajar no tempo hoje?"* e *"crachá de
  explorador"*.

Não é prefixo (item 8) nem título (item 10): é a **narrativa** da outra atividade
sobrando. Viraram *"a viagem com o Nico está completa"*, *"Quem vai voar com o
Nico hoje?"* e *"crachá de cartógrafo"*.

**Portão 11 (aviso, não reprova):** lista as frases longas que existem aqui e em
**UMA outra atividade só** — que é justamente o motor de onde clonei. Frase que
aparece em três ou mais é mobiliário do motor ("Pode seguir para o próximo
conteúdo", o menu do professor) e deve mesmo ser igual. Não dá para a máquina
decidir isso sozinha; o que ela faz é **pôr a lista curta na minha frente a cada
rodada**, e eu leio uma a uma antes de publicar.

**Regra que fica:** ao clonar, reler as TRÊS telas de moldura — entrada
("quem vai jogar"), medalha e relatório — procurando a HISTÓRIA da origem, não só
os nomes. É onde ela mais se esconde, porque são telas que eu não reescrevo.

**E o auditor jogador ficou determinístico onde dá:** ele escolhia sempre ao
acaso e, num quiz de 3 opções, às vezes gastava os 420 giros sem fechar a rodada
— reprovando fase perfeita, ainda mais quando disputava processador com os outros
portões. Agora, se a tela publica `data-qa="1"`, é nela que ele toca.

---

## ⚙️ O SUCESSO MUDO — quando o workflow fica VERDE e não entrega nada (ago/2026)

Custou três execuções e quase uma hora. As 15 narrações das dinâmicas novas da
cartografia foram geradas certinho pelo `gerar-audio.yml`, o passo imprimiu
`sem mudancas`, o run terminou **verde** — e **nenhum mp3 entrou no repositório**.
Foram duas armadilhas, uma dentro da outra, e as duas nasceram de otimizações
minhas:

1. **`sparse-checkout` não cobria a pasta de SAÍDA.** Eu tinha reduzido o
   checkout para `/_lote_falas.json` (o repositório tem ~1 GB). O `git add`
   então recusou os arquivos novos — *"Disable or modify the sparsity rules"* —
   e o passo concluiu que não havia mudanças. **Regra: a pasta onde o workflow
   ESCREVE tem que estar nas regras do sparse-checkout**, e o `git add` vai com
   `--sparse`.
2. **`git add A B` com B inexistente falha INTEIRO.** O comando era
   `git add "$outdir" _audio/`, e `_audio/` só existe quando se usa o default.
   Um pathspec que não casa aborta o comando e **o A também não entra**. Agora é
   um caminho por vez, e só o que existe.

**O portão que ficou:** o passo de commit não aceita mais "sem mudanças" no
escuro. Se nasceram mp3 e nada foi para o índice, ele **falha com erro**
explicando o motivo. Antes disso, um run verde era indistinguível de um run que
jogou o trabalho fora — e sucesso mudo é o pior tipo de falha, porque ninguém
vai conferir.

**Também curado no mesmo dia:** o `apt-get update` para instalar ffmpeg ficou
**25 minutos pendurado** num espelho lento e o run nem chegou a gerar voz. O
runner do GitHub já vem com ffmpeg: agora o passo usa o que existe e só instala
se faltar, com prazo de 4 minutos e sem derrubar o trabalho.

## 🎯 ALVO DE "ACHE NA CENA" É INVISÍVEL (ago/2026)

A classe `.achado` do motor é uma **placa creme** — ela existe para segurar uma
figurinha. Reaproveitada como alvo de procura ("ache o morro com mata na foto
aérea"), ela vira um **quadrado branco em cima da foto entregando a resposta**.
Quem procura tem que procurar: `.achado.mira` agora é transparente, e só aparece
quando a criança erra duas vezes (o andaime, classe `pisca`) ou quando acerta.
A exceção é a planta da sala, onde o lugar vazio PRECISA ser visto —
`.achado.mira.vazio` continua tracejado.

## 🕵️ MECÂNICA NOVA = PORTÃO ATUALIZADO NO MESMO COMMIT (ago/2026)

Duas dinâmicas novas (a rosa dos ventos e a paleta de pintar) fizeram o auditor
**jogador** dar `PRESO` em fases que funcionavam: ele simplesmente não enxergava
onde tocar, porque `.vento`, `.tcor` e `.tinta` não estavam na lista de alvos
dele. O mesmo aconteceu com o auditor do **padrão da casa**, que classificou 10
fases como "outro" — ou seja, a medição dos 40% estava cega justamente nas fases
novas. **Toda mecânica nova entra na lista dos portões no mesmo commit em que
nasce**; senão o portão vira enfeite: reprova o que está bom e aprova o que não
mediu.

E um terceiro: no caça-palavras, palavras que se **cruzam** deixavam as letras já
marcadas, o jogador não clicava em nada, a tela não mudava e ele dava `PRESO`
numa fase que a criança fecha sem esforço. Agora, quando não há o que marcar, ele
desmarca e remarca a última letra só para a tela refazer a conferência.

## 🖼️ RECORTAR ARTE DE FUNDO CREME (`_mapa/cortar_props.py`, ago/2026)

Quando o Marcos gera as imagens de apoio no ChatGPT, elas vêm em **fundo creme
uniforme com sombra** — e não em fundo preto, como as do Gemini. Limiar de brilho
não serve (apagaria a lousa clara e o piso de madeira). O molde que funciona:

1. **tirar a tarja preta** que o celular deixa em volta — ela fica nos CANTOS, e
   é dos cantos que se amostra a cor do fundo; sem esse passo o recorte sai
   inteiro, com fundo e tudo;
2. alfa por **rampa** sobre a distância da cor do fundo (creme puro some, sombra
   fica translúcida) — máscara binária devolve a sombra como mancha creme sólida;
3. a rampa só vale **perto** do objeto; longe dele, zero;
4. **tamanho pelo uso, não pelo original**: os móveis da planta aparecem em 44px
   na tela — 520px de largura era doze vezes mais peso do que o PC da escola
   precisa baixar.

---

## 💳 O GEMINI FICOU SEM CRÉDITO (ago/2026) — e o que fazer nesse caso

Descoberto ao tentar gerar a vista aérea da cartografia. A `GEMINI_API_KEY`
responde **HTTP 429: "Your prepayment credits are depleted"** nas quatro
tentativas do `gerar-imagens.yml` (o modelo `gemini-2.5-flash-image`; os dois
`-preview` nem existem mais → 404). **Não é falha do workflow nem da rede: é
saldo.** Recarrega-se em https://ai.studio/projects.

**Enquanto não tiver crédito**, a ordem de preferência é:
1. **Pollinations** (grátis) — serve para cena/fundo genérico, mas **não segura
   o estilo de barro** da casa. Nesta tentativa devolveu um borrão verde e, antes,
   uma foto realista de vale. Não dá para confiar nela em arte que precisa
   combinar com o resto da atividade.
2. **O Marcos gerar no ChatGPT** e subir em `_novo/` — foi assim que nasceram a
   bússola, a planta da sala, a lousa e o armário, e o estilo bateu perfeito.
3. **Reaproveitar arte da PRÓPRIA atividade** com outro propósito — legítimo (a
   regra proíbe copiar de OUTRA atividade, não de si mesma).

Foi a opção 3 que salvou a fase "O bairro lá de cima": a vista da cidade que já
existia no degrau final da escala virou o cenário da procura, com alvos novos.

## 🗺️ "É DE VERDADE" VIROU "O BAIRRO LÁ DE CIMA" (decisão do Marcos, ago/2026)

Palavras dele: *"Não precisa ser real, porém com cara de mapa de vista aérea
mesmo sendo no modelo de foto mais infantil, mas que o estudante consiga
entender"*. A foto aérea real do centro de Blumenau (Wikimedia, CC BY-SA) é
**densa demais para 8 anos**: telhado, sombra e toldo viram a mesma mancha
cinza, e a fase deixa de ensinar e vira loteria. A vista **desenhada** mantém o
salto pedagógico (sem símbolo, cheia de coisa junta) e devolve o que a foto
tirava: **dá para reconhecer**.

**Regra que fica:** o que faz a fase funcionar não é a foto ser real — é a
criança **conseguir ler**. E se a figura deixa de ser foto de alguém, a voz e a
tela **não podem continuar dizendo que é foto**: mudam o selo, o balão, o
banner, as três narrações e sai o crédito. Prometer o que a tela não entrega é
o portão da promessa.

---

## 💰 CARTELA: A REGRA ESTAVA ESCRITA E MESMO ASSIM SE PERDEU (ago/2026)

O Marcos: *"tem como otimizar as imagens em cartela para não gastar tanto? Tem
até isso registrado nos manuais"*. Tinha, com todas as letras, no
`MANUAL-MESTRE` §"REGRA FIXA": *"SEMPRE tentar gerar em CARTELA... Nunca gerar
pose por pose separada"*.

**O que eu realmente fiz na cartografia** (contado, não estimado): 45 imagens.

| grupo | peças | uma a uma | em cartela |
|---|---|---|---|
| avatares | 6 | 6 chamadas | 1 |
| símbolos da legenda | 8 | 8 | 1 |
| objetos de lado/de cima | 12 | 12 | 2 |
| props (bússola, lousa, armário…) | 4 | 4 | 1 |
| medalha, verso, recado, lupa | 5 | 5 | 1 |
| **mascote (base + falar + piscar)** | 3 | 3 | **3 — tem que ser edição** |
| cenas (voo, escala, fundo, mapa) | 11 | — | **Pollinations, de graça** |

**~R$9,00 → ~R$1,60. 82% do dinheiro pela janela** — e o pior nem é o dinheiro:
peça gerada sozinha sai com luz e escala próprias, então as 8 da legenda nunca
ficam irmãs. Cartela conserta as duas coisas de uma vez.

**Por que se perdeu:** porque a regra dependia de eu lembrar dela na hora certa
— e a hora certa é lá no começo, quando estou pensando em conteúdo, não em
custo. Regra que depende de memória não é regra: é sorte.

**O que passou a existir:**
- **`_qa/cartela.py`** (portão do custo) — roda em cima do lote ANTES de acionar
  o workflow e **reprova** 3+ peças recortáveis indo uma a uma, imprimindo o
  gasto dos dois jeitos. Classifica cena (grátis), edição do mascote (uma a uma
  mesmo) e peça (cartela).
- **`_padrao/cartela.py plano`** — agrupa em cartelas de até 8 e escreve os
  prompts prontos (grade NxM, fundo preto liso, mesma escala e mesma luz).
- **`_padrao/cartela.py cortar`** — recorta a folha que voltou já com os NOMES
  certos, em ordem de leitura, e monta a **folha de conferência** em xadrez.
- ⚠️ **um cérebro só:** a classificação mora no `_padrao/cartela.py` e o portão
  a IMPORTA. Na primeira versão a regra estava escrita nos dois arquivos e eles
  já discordaram na estreia (um contou 3 peças, o outro 2) — porque o
  classificador procurava "room" no prompt e casou com "classROOM board".

---

## 🕳️ FUNDO PRETO ENGOLE O QUE É ESCURO (ago/2026)

Recortando a primeira cartela da Terra dos Papagaios, os avatares saíram com
**buracos vazados no cabelo preto e no ombro**. O limiar era um só
(`max(RGB) > 34`): ele acha o objeto, mas o cabelo preto e a sombra da roupa
estão ABAIXO dele e viram fundo. E `binary_fill_holes` **não salva** — o buraco
encosta na borda da figura, então não é buraco "fechado".

**A cura é limiar DUPLO (histerese):** o forte (>34) diz onde o objeto está; o
fraco (>10) só é aceito se estiver **grudado** no forte. O cabelo entra (encosta
no rosto) e o chuvisco do JPEG no fundo, que é solto, fica de fora. Aplicado no
`_padrao/cartela.py`, os quinze recortes saíram inteiros.

**E ficou a medida junto:** depois de recortar, a ferramenta mede quanto do
INTERIOR da peça ficou transparente e **avisa acima de 1%**. Era um defeito que
só se via ampliando cada figura uma a uma — agora ele grita sozinho.

⚠️ Isto é irmão da lição já registrada do **corpo branco sem contorno em fundo
branco** (`ATIVIDADE-PREMIUM.md`): a diferença é que aquele **não tem conserto
por código** (tem que regerar a cartela) e este tem.

---

## 🔤 O CAÇA-PALAVRAS "BUGADO": QUATRO DEFEITOS EMPILHADOS (ago/2026)

O Marcos: *"o caça palavras ele bugou... tem que destacar melhor as palavras
encontradas, de preferência cores diferentes, e ter uma comemoração e barulho
para cada palavra"*. Fui olhar e não era um defeito: eram quatro, e o primeiro
explica todos.

1. **A TELA NÃO RESPONDIA.** O JS punha a classe `mark` ao tocar e `ok` ao
   completar — e **nenhuma das duas tinha regra de CSS**. A criança tocava na
   letra e não acontecia nada; a palavra achada não acendia. Um jogo que não
   responde ao toque não está feio: está quebrado.
2. **A GRADE TINHA UMA COLUNA A MAIS.** As palavras eram sorteadas numa grade
   **lógica de 9×9**, mas a tela desenhava com `width:31px` numa caixa de 328px:
   cabiam **dez** por linha. A palavra deitada ainda saía certa por sorte; a
   palavra **em pé** (posições i, i+9, i+18) aparecia **na diagonal**, letra por
   letra espalhada. A criança procurava uma palavra que, na tela, não existia.
   Cura: largura em **porcentagem** (1/9), nunca em px — `flex:none` era
   justamente o que impedia.
3. **PALAVRA QUE CRUZA TRAVAVA A OUTRA.** Ao achar, as células trocavam de
   `mark` para `ok`, e a conferência só olhava `mark`: a palavra que cruzasse
   uma já achada nunca fechava. Cura: contar `mark` **ou** `ok`.
4. **TOCAR NUMA PALAVRA ACHADA APAGAVA ELA.** O clique era um interruptor cego
   (`tem mark ? tira : põe`). Cura: célula conquistada fica **travada**.

**O que ficou (o pedido do Marcos):** uma **cor por palavra** — e o chip da
lista usa a mesma cor (bolinha antes, chip inteiro depois), então o olho liga as
duas sozinho; as cinco cores passam 4,5:1 com a letra branca. Ao fechar uma
palavra: as letras acendem **uma a uma** (75 ms de intervalo), som subindo de
cinco notas, faísca na cor da palavra em cada letra, o chip carimba, a faixa
**"ACHOU!"** sobe e a **voz diz a palavra** (a lista também ganhou
alto-falante — 3º ano ainda soletra). No fim, festa e confete.

### 🚪 E O PORTÃO QUE DEIXOU PASSAR
O `_qa/classes.py` existia para pegar exatamente isto — classe sem CSS — e
olhou para o outro lado, porque só lia `className = "..."` **direto**. Aqui a
classe vinha de um **ternário**: `q.className = tem ? "cquad" : "cquad mark"`.
Agora ele lê a **instrução inteira até o `;`** e recolhe todo texto entre aspas,
o que cobre ternário e concatenação (`"cquad ok "+cor`). Conferido contra o
arquivo antigo: acusa `SEM CSS: .mark`.

**A lição maior:** um portão que passa **não** é prova de que está bom — é prova
de que aquilo que ele SABE olhar está bom. Quando um defeito escapa, a pergunta
não é só "como conserto?", é **"qual portão devia ter pego, e por que não
pegou?"**.

---

## 🪑 A FIGURA MAIOR QUE O LUGAR DELA (foto do Marcos, ago/2026)

Ele mandou a foto da **planta da sala** montada: a lousa ocupando um quarto da
tela, a mesa da professora como um disco gigante, o armário atravessado. *"Essa
fase ficou estranha, não funcionou como deveria."*

**A causa é sutil e vale mais que o conserto.** O móvel entrava na vaga com a
classe `pecaimg` — que **tem** regra de CSS, mas só **debaixo de outro pai**
(`.peca .pecaimg` e `.tvaga .pecaimg`). Dentro da vaga (`.achado`) ela ficava
sem tamanho nenhum, e a `<img>` entrava no **tamanho natural**: 240px de lousa
em cima de uma planta de 420px.

**Por que nenhum portão viu:**
- o de **classes** procura "classe sem CSS" — e a classe TEM regra; ele acha a
  regra e aprova. *Classe certa no lugar errado não é classe sem CSS.*
- o de **leiaute** abre cada fase e mede — mas a fase abre **VAZIA**: os móveis
  só existem depois que a criança os coloca. Ele mediu um cômodo vazio e
  aprovou, com razão.

**Onde a medida foi parar:** no **jogador**, que é o único portão que chega ao
**estado final** de cada fase. Depois de cada toque ele confere se alguma
`<img>` está maior que o pai posicionado (15% de folga para padding e sombra) e
reprova com nome e medida. Conferido contra o arquivo antigo:
`.pecaimg 240x81 dentro de .achado 66x66`. A mesma regra entrou no leiaute
(regra 7) para o caso estático.

**E a vaga passou a ter o formato do móvel** (a lousa comprida e fina, a cadeira
quadradinha), o que era o outro motivo de a sala não parecer uma sala.

**Lição de método:** quando um defeito escapa, a pergunta não é só *"qual portão
devia ter pego?"* — é *"em que MOMENTO ele existiria?"*. Defeito que só nasce
com a fase jogada tem que ser medido por quem joga.

## 🔦 ACHAR NUMA FOTO É ZONA, NÃO PONTO (ago/2026)

Na mesma mensagem: *"tem que ser mais intuitivo. Você fala para achar o rio, o
legal seria a criança clicar em QUALQUER PARTE do rio e dar certo. E não
aparecer um quadrado branco quando acham... quando pede o quarteirão de casas
tem muitas casas, fica confuso; o morro tem vários com árvores; a mesma coisa a
ponte"*.

As três queixas são o mesmo erro de fundo: **tratei uma foto como se fosse um
quiz de ponto único**. Numa cena de verdade a coisa procurada é **extensa** (o
rio atravessa a imagem inteira) ou **repetida** (há sete moitas de mata e duas
pontes). Um alvo de 66px no meio disso não é "achar": é adivinhar onde o
programador pôs o quadradinho.

**O que passou a valer para toda fase de "ache na cena":**
1. **O alvo é uma ZONA e são VÁRIAS** — o rio tem oito pontos ao longo do curso,
   a mata sete moitas, a rua quatro trechos, a ponte as duas pontes.
2. **O toque é medido por DISTÂNCIA** até a zona mais próxima, em % da figura
   (vale igual no celular e no PC), com raio generoso. Toca em qualquer parte
   do rio e dá certo.
3. **Pergunta ambígua sai.** "Um quarteirão de casas" numa foto que é toda casas
   não é pergunta. Entraram coisas inconfundíveis — e uma que ainda ensina
   relação espacial: *"o pedaço do bairro que fica do OUTRO LADO do rio"*.
4. **O achado é LUZ, não quadrado.** Anel dourado aceso no ponto tocado + uma
   plaquinha com o nome. Fica marcado sem tapar a figura.

---

## 🌉 "ESSES ERROS NÃO PODEM PASSAR" — o portão da pergunta ambígua (ago/2026)

O Marcos, cobrando o que ficou: *"a mesma coisa a ponte, fica confuso porque tem
DUAS pontes... não seria melhor gerarmos outra imagem, ser mais intuitivo?
**Esses erros não podem passar**"*.

Ele está certo duas vezes. Eu tinha consertado a MECÂNICA (aceitar as duas
pontes) e deixado a **confusão** de pé: a criança lê "a ponte", vê duas, e não
sabe qual — mesmo que as duas funcionem. Aceitar as duas resolve o meu problema
de código, não o dela.

**O defeito tem marca medível**, e é isso que virou portão. Numa fase de "ache
na cena" o código declara quantos lugares valem. Se a pergunta está no
**definido singular** ("a ponte", "o morro") — que quer dizer *aquela, a única*
— e a fase declara **duas ou mais** zonas, a própria tela está confessando que
há mais de uma na figura. Não é gosto: é contradição entre o que a voz promete
e o que a figura mostra.

**`_qa/ambiguo.py` (portão 0c da banca):**
- definido singular + 2 ou mais zonas → **reprova**;
- indefinido ou coletivo ("uma ponte", "alguma rua", "a mata em volta") → passa,
  porque é assim que se pede uma coisa repetida sem confundir;
- ⚠️ **coisa comprida ≠ coisa repetida**: o rio é UM só e as oito zonas dele são
  pedaços do mesmo rio. Quem sabe a diferença é quem escreve a fase, então ela
  se declara: `unico:1`. Sem o campo, o portão assume ocorrências diferentes —
  o padrão seguro.

**E o conserto de verdade foi a FIGURA, como ele disse.** O Gemini está sem
crédito e o Pollinations não dá conta de cena com lista de itens (tentei: voltou
uma foto de vale, sem casas nem ponte). A saída que funcionou custou zero:
**recortar** a vista da cidade na metade de baixo. Sobrou **uma ponte só**, e de
quebra tudo ficou maior na tela — mais intuitivo pelos dois lados. Com uma ponte
só, a pergunta pôde voltar ao português natural: *"a ponte em cima do rio"*.

**Regra que fica: figura de ensino não repete o que ela quer ensinar a achar.**
Antes de usar uma cena numa fase de procurar, contar quantas vezes cada coisa
pedida aparece nela. Se aparece mais de uma vez: ou muda o artigo, ou muda a
figura — e mudar a figura é melhor.

---

## 🔊 "O BOTÃO FALA A CURIOSIDADE, NÃO A PERGUNTA" (ago/2026)

O Marcos: *"na fase da maquete ao mapa, se clica no botão ao lado do enunciado
ele não fala isso: fala da curiosidade lá embaixo. Aliás isso está acontecendo
nas fases da atividade do terceiro ano"*.

**A causa é uma armadilha de nome.** O motor guardava `falaAtual` = **o último
áudio tocado**. E quem toca áudio numa fase não é só a tela: é o **elogio**, o
**consolo**, a **dica** e o **post-it de curiosidade**. Bastava a criança abrir o
"Você sabia?" para o botão do enunciado passar a repetir a curiosidade para
sempre.

**E o defeito era mais velho do que parecia:** o botão **"Ouvir de novo"**, que
existe desde o começo, tinha exatamente o mesmo problema — só que ninguém o
notava, porque ele fica longe do texto e é usado com menos frequência. O
alto-falante no enunciado não criou o defeito: tornou impossível não vê-lo.

**O conserto** é uma variável separada, `falaTela`, que só recebe narração **da
tela**; as secundárias (`_cur_`, `_dica`, `_acerto`, `_erro`) não a alteram. Os
dois botões passaram a repetir `falaTela`. Aplicado nas três atividades.

**O portão: `_qa/voztela.py` (0d da banca).** Confere que existe `falaTela`, que
`falar()` tem um GUARDA antes de gravar nela, e que nenhum botão de repetir lê
`falaAtual` sozinho. Conferido contra o arquivo antigo: acusa os dois.

**A lição que fica:** variável chamada "atual" quase sempre quer dizer "a última
que passou por aqui" — e "a última que passou" raramente é "a que interessa".
Quando um botão promete repetir ALGO ESPECÍFICO, ele precisa de uma variável que
guarde **aquilo**, não de um histórico global.

---

## 🦜 A TERRA DOS PAPAGAIOS — História, 5º ano (ago/2026)

Pedido do Marcos: *"uma atividade incrível para o 5º ano sobre as grandes
navegações"* e, depois de ver a primeira versão, o recado que virou meta:
***"tem que ficar uma atividade fantástica igual a de história do 4º ano"***.

**O ano certo (checado ANTES de escrever).** "Expansão marítima europeia" está
no **7º ano** do currículo de Blumenau. No 5º ano a unidade é *"Povos e
culturas: meu lugar no mundo"*, objeto **"o que forma um povo"**. Por isso as
navegações aqui **não são a matéria**: são o acontecimento que responde à
pergunta do 5º ano. Nada de capitães, datas e Tordesilhas. Ver `_naveg/PLANO.md`,
que amarra cada fase a um objetivo escrito do ano.

**A ideia:** o mascote é uma **arara** (*Ará* = arara em tupi) e **ela já estava
aqui**. A criança não "descobre" nada — ela **vê chegar**. E o título é verdade
histórica: os primeiros mapas europeus escreveram *Terra Papagalli*.

### O que "igual à do 4º ano" queria dizer, em número
A régua não era opinião: bastou medir as duas com o `_qa/padrao.py`.

| | A Máquina do Tempo do Vale (4º) | Papagaios, 1ª versão | Papagaios, agora |
|---|---|---|---|
| fases com gesto | 21 | 16 | **21** |
| gestos diferentes | 12 | 9 | **14** |
| maior gesto | 23,8% | 37,5% | **28,6%** |

As **cinco fases novas**, escolhidas pelo gesto que faltava (não pelo conteúdo
que sobrava): **ligar** ("para que servia?", prática de recuperação logo depois
do porão), **orientar** ("para que lado?", a bússola aplicada à rota),
**pintar** ("a língua guarda", marca-texto num dia comum sem **uma** palavra
vinda de Portugal), **digitar** ("complete a história", o degrau simbólico
depois da cruzadinha) e **explorar** ("o mapa antigo", lupa sobre uma carta de
marear de 1500).

### As lições desta rodada (as duas com portão, como manda a casa)

**1. `var VOZOK={}` vazio = atividade MUDA nas respostas, e ninguém percebia.**
A atividade tinha 21 fases, a banca inteira aprovada — e **nenhuma resposta
falava**. O motor pendura o alto-falante sozinho a partir do `VOZOK`, e o clone
traz esse objeto **vazio**. O `_qa/clone.py` só pega o contrário (voz prometida
sem mp3), então um `VOZOK` vazio passava calado. **Portão novo (`_qa/padrao.py`,
item 3c):** se a atividade tem resposta tocável (`.opt`, `.cx`, `.lig`, `.gav`…)
e o `VOZOK` está vazio, **reprova**. Conferido nas quatro atividades: 58, 38, 70
e 25 vozes de resposta. *Para juntar as respostas de uma atividade inteira sem
fazer na mão:* percorrer as tabelas de conteúdo com o mesmo `chaveVoz` (djb2 →
base36) e escrever `op_<chave>` no `_lote_falas.json`.

**2. O jogador reprovava fase que funcionava, por não rolar a tela.** No porão
do navio ficavam 4 fichas à vista e **2 abaixo da dobra**. Como sempre havia
algo clicável visível, o auditor nunca rolava: clicava eternamente nas 4 de cima
e dava `PRESO`. **Conserto (`_qa/jogador.js`):** quando o estado não anda há um
tempo (a cada 60 giros parados), ele **rola** — que é o que a criança faz quando
acha que já tocou em tudo. A rolagem-por-último-recurso (só quando não sobra
nada visível) não bastava.

**3. Legenda tem que descrever o que o recorte REALMENTE mostra.** A quarta
lupa prometia "o pedaço em branco" do mapa, mas com zoom de 3× a janela é
grande demais para centrar num canto: o recorte saía cheio de papagaios. Virou
"a terra do Ará" — que é o que aparece. *Regra:* depois de escolher um recorte,
**olhar o recorte** e só então escrever a legenda; nunca o contrário.

**Uma imagem só:** `nv_mapavelho` (Gemini, estilo de barro, sem letra nenhuma
para não arriscar palavra torta na frente da criança). A lupa aproxima **o mesmo
arquivo** (`background-size:300% 300%` numa janela quadrada) — quatro detalhes
sem gerar quatro imagens.

**4. E a mesma lição de sempre, cobrada duas vezes numa rodada só:** as duas
mecânicas novas (`.pal` do marca-texto e `.lupamira` da lupa) **não estavam na
lista do `_qa/jogador.js`** — ele não enxergava onde tocar e deu `PRESO` em fase
que funciona. E o marca-texto ainda tinha o **`data-qa` que nunca se apagava**:
a palavra já pintada continuava anunciando "é aqui", então o auditor (e a
criança teimosa) tocava nela para sempre. *Regra que vale para toda fase nova:*
**alvo novo entra no `SEL` do jogador no mesmo commit**, e **todo `data-qa` sai
do elemento no instante em que ele deixa de servir**.

**5. E o pior deles, achado no AVISO da própria banca:** a tela de entrada
perguntava ***"Quem vai voar com o NICO hoje?"*** e o crachá era ***"de
cartógrafo"*** — o mascote e o papel da **cartografia**, na primeira tela que a
criança vê, numa atividade de História. O relatório do professor ainda trazia o
**currículo de Geografia do 3º ano** inteirinho. Nenhum item do `_qa/clone.py`
pegava: não tem prefixo (item 8), não é o título (item 10), e a frase existia em
UMA outra atividade só — ou seja, caía no **aviso** do item 11, que é para ler,
e é fácil não ler.

**O portão novo (item 12 do `_qa/clone.py`): o NOME DO MASCOTE.** Cada atividade
declara `var MASCOTE_NOME="..."` (Ará, Nico, Juca, Broto) e o portão **reprova**
se (a) o nome do mascote de outra atividade aparecer no texto que a criança lê,
ou (b) o meu nome for igual ao de uma vizinha — que é o clone com o nome
esquecido. Duas armadilhas aprendidas ao montá-lo:
- **por estatística não dá.** Tentei achar o nome alheio por frequência (próprio
  raro aqui, frequente lá) e o resultado foi "Agora", "Vamos", "Vale", "Terra".
  Portão que grita à toa ensina a ignorar portão. **Declarar é melhor que
  adivinhar.**
- **comentário não é texto da criança.** Sem tirar os comentários antes de
  procurar, a própria lição escrita no código ("foi assim que *com o Nico* ficou
  na tela") reprovava as quatro atividades. Portão que reprova a si mesmo não
  serve.

---

## 🎨💰 CARTELA DE CENAS — a exceção da regra virou regra (ago/2026)

Pedido do Marcos: *"otimize em cartelas para não gastar muito como combinamos"* +
*"melhore o que precisar nas imagens da atividade do 3º e do 5º ano"*.

**O que a regra dizia até aqui:** cartela é para PEÇA recortável; **cena larga
fica de fora**, vai no Pollinations, que é de graça. Estava certo — enquanto o
Pollinations desse conta. Ele **não dá**: pedimos barro e veio foto; pedimos uma
caravela e veio desenho de aplicativo de bebê. Resultado medido na folha de
contato da Terra dos Papagaios: **quatro estilos brigando na mesma atividade**
(objetos e avatares em 3D fofo, duas cenas em barro, uma chapada, duas
foto-realistas escuras).

**Cena boa é paga — e cena paga volta para a cartela**, com uma diferença: cena
não se recorta por silhueta, se recorta por **geometria**. Ferramenta nova:
`python3 _padrao/cartela.py cortar-cenas <folha> <nomes> --grade LxC`.

| grade | tamanho de cada cena | para que serve |
|---|---|---|
| **2x1** (empilhadas) | 1024 × 512 | cena larga de fase — **mais nítida** que os 820px que usávamos |
| **2x2** | 512 × 512 | figura de moldura pequena, onde o que importa é serem IRMÃS |

**A conta desta rodada: 8 imagens em 3 chamadas (~R$0,60)** — uma a uma seriam 8
chamadas (~R$1,60). **62% mais barato**, e as cenas de cada folha saíram irmãs
(mesma luz, mesma paleta).

### O que melhorou, e por quê
- **5º ano** — `nv_caravela` + `nv_horizonte` numa folha; `nv_aldeia` + `nv_porao`
  noutra. A aldeia nova mostra, lado a lado, exatamente as três coisas que a
  narração promete: **casa de palha, roça e caminho** (a antiga era escura e
  vista de cima, e a fase pedia "o terreiro", que nem aparecia direito).
- **3º ano** — as quatro da escala (`mp_esc_sala/escola/bairro/cidade`) numa
  folha 2×2 **de propósito**: o balão diz *"veja o MESMO lugar de cada vez mais
  longe"* e, até hoje, eram quatro lugares diferentes. Agora a escola de telhado
  vermelho aparece na sala, na escola, no bairro e na cidade — a criança segue o
  mesmo prédio encolhendo. Isso é a fase inteira funcionando pela primeira vez.

### ⚠️ TROCAR A FIGURA É REMEDIR AS ZONAS — e medir não é olhar
Duas fases tinham coordenadas cravadas nas figuras velhas (`ALDEIA` no 5º ano,
`MARCAR` no 3º). Trocar a arte sem remedir faria a criança **tocar certo e ouvir
que errou** — o defeito que o Marcos já pegou uma vez na cartografia.

E aqui a lição nova: **eu errei olhando**. Na primeira passada pus as zonas "no
olho" sobre a grade e três delas caíram no mato. O que resolveu foi **medir a
cor do pixel embaixo de cada alvo**, na figura como ela aparece na tela: rio tem
que dar **azul**, telhado da escola tem que dar **vermelho**, roça tem que dar
**verde**. Está em `_qa/` como receita (`scratchpad/pixel.js` → posição no
navegador, cor no Python — `file://` suja o canvas e `getImageData` estoura).
Alvo conferido por cor é alvo conferido; alvo conferido no olho é chute com
grade em cima.

### E o portão que reprovou a atividade por causa da própria cópia
Na hora de publicar, a atividade é **copiada inteira para `_novo`**. O
`_qa/clone.py` varre as pastas vizinhas procurando resto de clone — e achou a
cópia: *"o mascote daqui se chama 'Ará', o MESMO nome do mascote de `_novo`"*,
*"o sw.js usa o MESMO nome de cache de `_novo`"*. **Reprovou a atividade por ela
ser igual a si mesma**, e justo no passo de publicar, que é onde eu mais
preciso confiar no portão. Conserto: `NAO_E_ATIVIDADE` + `e_vizinha()` no
`_qa/clone.py`, usados nos **cinco** varrimentos (prefixo, sw.js, nome, frases,
mascote). `_novo`, `_recuperado`, `_padrao`, `_qa` e companhia são área de
serviço, não atividade.

---

## 🔊❓ "OS BOTÕES DE AJUDA DO SOM FUNCIONAM?" — a pergunta que achou dois buracos

O Marcos perguntou (ago/2026), sobre a atividade do 3º ano: *"os botões de ajuda
do som funcionam? Corrigiu o problema que estava havendo?"*. Em vez de ler o
código e responder que sim, escrevi um teste que **clica em todos os botões de
som, fase por fase**, e confere qual arquivo cada um manda tocar. Achou duas
coisas que a banca inteira tinha deixado passar.

**1. A Terra dos Papagaios tinha 21 fases e ZERO botão no enunciado.** O
`poeVozPergunta()` foi escrito para o 3º ano; a atividade do 5º nasceu depois e
nunca o recebeu. As RESPOSTAS falavam (58 vozes), a PERGUNTA não. O mesmo valia
para a Máquina do Tempo do 4º ano. **Portão novo (`_qa/padrao.py`, item 3d):**
tem `.balao` e não tem `poeVozPergunta()` chamada pelo observador → **reprova**.

**2. E o defeito da curiosidade tinha voltado, por outra porta.** No palpite do
3º ano, `mp_palpite_ok` toca DEPOIS que a criança responde, na MESMA tela — e
virava "a voz da tela". O alto-falante do enunciado passava a repetir *"boa,
guarde o seu palpite"* em vez da pergunta.

**A regra estava errada de FORMA, não de conteúdo.** `ehSecundaria()` era uma
LISTA de sufixos (`_cur_`, `_dica`, `_acerto`, `_erro`) e crescia um item por
defeito descoberto — o mesmo vício que já tinha custado caro no `_qa/clone.py`.
Sufixo novo, buraco novo, para sempre.

**A regra nova não depende de nome de arquivo:**

> **a voz da tela é a PRIMEIRA narração depois que a tela foi montada.**
> `limpa()` zera `telaNarrou`; o primeiro `falar()` não-secundário a assume.
> Tudo o que vier depois, na mesma tela, é reação.

Isso resolve os dois lados de uma vez: pega o `_ok` (que não é o primeiro) **e**
continua certo na tela final do "Ensine o Ará", onde a narração se chama
`_revela` mas **é** a voz daquela tela (é a primeira depois do `limpa()`). Uma
lista de sufixos erraria justamente essa. Aplicado nas quatro atividades.

**A lição que fica:** *pergunta de conferência vale mais que leitura de código.*
Eu tinha lido o `poeVozPergunta` no motor e concluído que estava em todas; bastou
CLICAR para ver que numa atividade inteira não havia nenhum. E quando um portão
começa a virar lista que cresce a cada defeito, o problema não é o item que
falta — é a forma da regra.

### Três armadilhas ao INSTALAR o alto-falante do enunciado numa atividade pronta
1. **`.balao` precisa de `position:relative`.** O `.zapb` é absoluto e se ancora
   no primeiro pai POSICIONADO. Sem isso ele sai do balão e vai parar **em cima
   da figura da fase** — o `_qa/leiaute.js` acusou 6 fases no 5º ano e 6 no 4º.
2. **Pôr o botão sem pôr o `falaTela` é entregar o defeito de bandeja.** O 4º ano
   ainda estava com o `falaAtual` puro; o botão novo repetiria a curiosidade em
   18 fases. Instalar os dois juntos, sempre.
3. **`node --check` não vê variável que não existe.** Ao aplicar a regra nova no
   2º ano, o `telaNarrou=false` entrou no `limpa()` e a DECLARAÇÃO não — a
   sintaxe é válida e o `node --check` passou, mas a atividade estourava
   `ReferenceError` na primeira tela, ou seja, **não abria**. Quem pegou foram os
   portões que ABREM o app (leiaute e jogador). É a mesma lição do `_qa/funcoes.py`
   (função que não existe), agora com variável: **portão que só lê o código não
   substitui portão que roda o código.**

---

## 🖤🔊 TRÊS DEFEITOS NUMA TARDE — e os três viraram portão (ago/2026)

O Marcos testou a Terra dos Papagaios e mandou três coisas seguidas, fechando
com *"esses erros não podem acontecer mais"*. As três eram reais e nenhuma era
pequena.

### 1. "O segredo do vento… a foto é que gira e fica feio"
Palavras dele: *"deveria ter uma animação onde o navio avança, não?"*. Certíssimo
— e o problema não era só estético: **girar a foto não ensina nada**. A fase
rodava a cena inteira (mar, céu e barco juntos) uns graus, como se inclinar a
fotografia fosse navegar.

**Agora:** o mar é o fundo (arte de IA), o navio é uma **peça recortada** que
desliza por cima, e a vela **troca de posição** — três desenhos irmãos da mesma
cartela (1 chamada). O CSS anima só o que precisa se mexer: a posição do barco
(transição de 1,5 s), o balanço, a esteira de espuma e as rajadas de vento. Isso
é a regra da casa aplicada: *arte de IA para a figura, CSS só para o movimento*.

### 2. "Quando conclui, fica só a tela de fundo e falando"
O molde do defeito estava em **23 fases** das duas atividades:

    limpa();                          // apaga TUDO
    if(acabou){ depoisDaFala("x_revela",13000,...); return; }   // e nao desenha nada

Entre o `limpa()` e a faixa final passavam-se **até 13 segundos** de narração com
a criança olhando o fundo de madeira. Print nenhum pega isso: só jogando a fase
até o fim. **Conserto:** `fechaFase()` no motor — o fecho virou uma tela com o
mascote, o selo e o que ele está dizendo, escrito. **Portão: `_qa/telavazia.py`**
(0e da banca), testado contra a versão antiga: acusa as 8 do 5º ano.

### 3. "O botão de som não fala exatamente o que diz o enunciado"
A pergunta dele foi *"isso é problema?"* — e a resposta honesta é **sim, e do
pior tipo**: o botão existe exatamente para quem não lê saber o que a tela está
pedindo. Muitas fases **trocam o texto do balão a cada rodada** (a pergunta muda,
a explicação da peça aparece) e continuavam com a narração da abertura, tocada
uma vez só lá no começo. Ele tinha notado antes, no porão: *"o texto lá em cima
fica a explicação correta, mas se clica para ouvir ele narra a introdução"*.

**Conserto:** `falaDaTela(id)` — a fase diz "a voz desta tela agora é esta":
narra na hora **e** passa a ser o que o alto-falante repete. **44 vozes novas**
(29 no 5º ano, 15 no 3º). **Portão: `_qa/vozpergunta.py`** (0f), que exige
`falaDaTela` sempre que o balão recebe conteúdo — e sabe distinguir **placar**
("Faltam 3", "Já achou 2 de 5") e **aviso** ("Primeiro toque num povo"), que não
são pergunta e não precisam de voz.

### 🇧🇷 De brinde, um erro de português que a criança lia
Montar a frase por concatenação — `"Toque em " + it.q` — produzia **"Toque em a
roça"** e **"onde fica as casas"**. O verbo tem que aceitar qualquer artigo e
qualquer número: virou **"Ache a roça"**, **"Ache as casas"**. Vale como regra:
*quando o enunciado é montado com um pedaço variável, o começo da frase tem que
funcionar com todos os pedaços* — testar com o artigo feminino, o masculino e o
plural antes de fechar.

### ⚠️ E uma lição sobre MIM
Fiz a troca das 23 fases com um script de regex e ele **embaralhou os
argumentos** (pegou o texto de uma fase com o áudio de outra). O `node --check`
passou — era JavaScript válido, só que errado. Desfiz tudo com `git checkout` e
refiz varrendo a árvore de funções, do mais interno para o mais externo, para
achar o selo certo de cada fase. **Reescrita em massa por regex se confere fase
por fase, com o nome de cada uma impresso, antes de gravar.**

---

## 🗺️ A MAQUETE E O MAPA ERAM LUGARES DIFERENTES (ago/2026)

O Marcos reportou duas coisas pequenas na fase "da maquete ao mapa" do 3º ano:
*"ele não fala a palavra ponte no áudio"* e *"quando se clica na ponte aparece um
quadrado branco"*. Fui olhar e achei uma terceira, que era a de verdade:

**a maquete e o mapa não eram o mesmo lugar** — e a fase inteira existe para
mostrar que são o mesmo lugar, um com altura e outro achatado. A maquete tinha
igreja, praça, fileira de casas, rio **e ponte**; o mapa tinha uma igreja, quatro
quadradinhos vermelhos, um círculo verde e um rio — **sem ponte**, com outro
arranjo. O que a criança tomava por ponte era o **tronco da árvore** cruzando o
rio. Pedir "ache a ponte no mapa" era pedir o impossível.

**Conserto:** gerei o mapa como a maquete vista de cima (igreja à esquerda, praça
no meio, casas à direita, rio embaixo e a ponte sobre ele) e **remedi por COR**
os alvos das três fases que apontam nele — `NAMAQ`, `COORD` e `ONDE`.

### O que mais saiu desta rodada
- **Quadrado branco → luz.** O alvo acertado virava `.achado.ok`, um retângulo
  claro por cima do mapa. Agora some e no lugar acende a mesma **luz redonda com
  o nome** que já se usava no "bairro lá de cima".
- **"Onde fica no mapa" tinha DOIS eixos.** As gavetas misturavam
  esquerda/direita com meio/embaixo. Palavras dele: *"peça para classificar em
  cima, no meio e embaixo, porque a direita e a esquerda ficou confuso"*. Certo:
  não se classifica bem quando as caixas não são do mesmo tipo. Virou um eixo só.
- **"Ache pela coordenada" não usava a coordenada.** A tela perguntava "onde está
  a igreja?" e a criança achava **a olho**. Pedido dele: *"melhor colocar A1, D4
  etc"*. Agora a tela **dá** a coordenada e ela lê a letra (linha) e o número
  (coluna) para chegar lá — que é o que a fase se propõe a ensinar.
- **A barra fixa cobria conteúdo.** Ele viu na legenda; medindo em 360×640 eram
  16 fases. Metade era falso positivo (bastava rolar) — o medidor agora **rola
  antes de medir**, que é o que a criança faz. O que sobrou foi resolvido
  encolhendo a fase para caber sem rolagem: *ninguém rola o que não sabe que
  existe*.
- **Verso do jogo da memória cortado.** `object-fit:cover` preenche a carta
  cortando o desenho; o verso é ARTE e tem que aparecer inteiro. Virou `contain`
  e a carta cresceu de 118 para 138px de altura mínima — a regra da casa já dizia
  *carta grande*, agora com a arte inteira dentro.

### 🇧🇷 A armadilha da frase montada (de novo, três vezes)
`"Toque em " + it.q` → **"Toque em a roça"**. `"onde fica " + q` → **"onde fica
as casas"**. `"em cima " + rot` → **"em cima a mesa"**. `"é onde fica " + q` →
**"é onde fica as casas"**.

**Regra:** quando o enunciado é montado com um pedaço variável, o começo da frase
tem que funcionar com **todos** os pedaços — o feminino, o masculino e o plural.
Os consertos que servem sempre: trocar o verbo (*"Ache a roça"*, *"Ache as
casas"*), usar a forma contraída declarada na tabela (`de:"da mesa"`), ou uma
construção neutra (*"Lá tem a igreja" / "Lá tem as casas"*).

---

## 🔊= "O ÁUDIO TEM QUE FALAR EXATAMENTE O QUE ESTÁ ESCRITO" (ago/2026)

Palavras do Marcos: *"seria interessante que o áudio ao lado das instruções
falasse exatamente o que está escrito, favor verificar a escrita se está
correta, isso em toda atividade"*.

**O motivo é o pilar 3 levado até o fim.** Esse botão existe para quem NÃO LÊ.
Se a tela pede uma coisa e a voz conta outra — mesmo que as duas sejam boas —, a
criança que depende da voz recebe uma instrução diferente da que está na frente
dela; e quem lê devagar, acompanhando a voz com o dedo no texto, se perde. Não
adianta a voz ser "sobre" a tela: tem que ser **a tela**.

**Feito nas duas atividades:** 26 fases do 3º ano e 21 do 5º. Todas as narrações
de abertura foram **regravadas com o texto escrito**, e as fases cujo enunciado
muda a cada rodada ganharam voz por rodada (rosa dos ventos, cruzadinha, forca,
complete a frase, o custo, relâmpago, ensine o mascote, a bússola, o aquecimento).

### O portão: `_qa/vozigual.js` (0g da banca)
Abre cada fase, lê o balão **como a criança vê**, descobre qual áudio o
alto-falante repete (`falaTela`) e compara com o texto daquela narração. Acento,
vírgula e caixa não contam; palavra diferente conta.

### 📄 `<pasta>/falas.json` — o texto da voz vira parte da atividade
Sem isso o portão é impossível: **mp3 não se lê**. Agora cada atividade guarda
`[{"id","texto"}]` de todas as narrações, ao lado do `index.html`. Toda atividade
nova nasce com ele, e ele é a fonte do lote de geração de voz — um texto só,
usado para gravar E para conferir.

### 🎲 O defeito que só apareceu por causa do portão
No **Desafio Relâmpago** a fila de perguntas é **embaralhada** (`baguncar`), e o
código chamava `falaDaTela("mp_rel_q"+i)` com o índice da RODADA. Resultado: a
criança lia uma afirmação e ouvia outra. Conserto: `RELM.indexOf(it)` — o índice
da TABELA, não o da vez. **Regra:** em fase embaralhada, o id da voz vem do
ITEM, nunca do contador da rodada.

---

## 🗣️ A INTRO CALAVA A PERGUNTA — 27 fases, e o Marcos achou UMA (ago/2026)

Palavras dele: *"no mapa do bairro o símbolo escola não é falado"*. Fui medir e
eram **27 fases** das duas atividades. O molde era do motor:

```js
falaDaTela("x_q0");              // toca a pergunta...
if(idx===0) falar("x_intro");    // ...e a intro entra por cima
```

`falar()` dá `narr.pause()` antes do áudio novo. Então, na **primeira rodada de
quase toda fase**, a criança ouvia só a abertura — a pergunta nunca era dita.
Quem lê não percebe (o texto está na tela). **Quem não lê fica sem instrução
nenhuma** — e o alto-falante existe exatamente para essa criança.

**Conserto (motor):** `introEPergunta(idIntro,ms)` — guarda a `falaTela`, toca a
intro e, quando ela acaba, toca a pergunta.
**Portão:** `_qa/vozintro.py` (0h da banca) — dentro de uma mesma função,
`falar("..._intro")` não pode vir depois de um `falaDaTela(...)`.

## 🎯 ZONA MEDIDA POR PIXEL — "pode ser qualquer rua"

Cobranças dele: *"seria interessante o símbolo do rio ser colocado em qualquer
lugar onde esteja o rio"* e *"nessa fase pode ser qualquer rua, senão o aluno
não acha nunca"*. Antes eram 3–5 pontinhos escolhidos a olho com raio de 9%.

**A técnica (vale para toda fase de "ache na figura"):** recortar a coisa da
PRÓPRIA figura pela cor do pixel (numpy + scipy), virar uma string de 48×48
quadradinhos (`1` = ali é a coisa) e testar o toque com margem de 1 quadradinho.
O ponto do alvo visível é o pixel **mais longe da borda** da região
(`distance_transform_edt`), nunca o centroide — o centroide de um rio em curva
cai fora do rio.

**Mesma técnica, outro uso — PINTAR:** ideia do Marcos (*"o mapa deveria ser sem
cor, daí quando a criança clica com a cor certa ela pinta o desenho"*). O mapa
vira base clara (`mp_pmapa.jpg`) e cada região vira uma camada tingida com a cor
da legenda (`mp_pint_<zona>.png`), que aparece com o toque certo. Registro
perfeito de graça, porque as camadas saem da mesma imagem.

**⚠️ Onde a medição por cor NÃO resolve:** quando a mancha e o objeto têm a mesma
cor. As peças da planta da sala têm uma sombra creme assada no PNG, e ela é a
mesma cor da madeira clara — tentei cinco caminhos (cor do canto, contorno por
gradiente, saturação adaptativa, sombra translúcida, chroma novo) e todos comeram
a peça. **Solução real:** o FUNDO virou papel claro (`mp_planta_papel.jpg`), onde
a mancha some. O conserto definitivo é regerar as peças com recorte transparente
no Gemini — o Pollinations **não** entrega vista de cima isolada em fundo chroma
(pedi quatro, voltaram quatro vistas laterais sobre chão de madeira).

## 📐 O ENUNCIADO NUNCA ENCOSTA NO QUE VEM DEPOIS

Cobrado DUAS vezes: *"as opções de resposta estão encostando no enunciado"* e
depois *"esse encosto no enunciado eu já tinha comentado antes"*. Da primeira vez
consertei A FASE — por isso voltou. A causa era do motor: o balão tem sombra e
não tinha margem por baixo. Agora `.balao + *{margin-top:13px}` **e** o portão 5
regra 9 (`_qa/leiaute.js`), que mede a folga em 6 tamanhos e reprova abaixo de
6px. Ele achou de cara um caso que ninguém tinha visto (jogo da memória).

## 🌐 "O SITE NO AR ESTÁ SERVINDO O QUÊ?" — pergunte a ele

O build do Pages deu `errored` três vezes seguidas mesmo depois do
`republicar-limpo.yml`, e daqui do chat não dá para conferir (a rede é travada:
curl no github.io volta 403 pelo proxy). **Ficar re-disparando o build resolve**
— na quarta tentativa deu `built`. Mas a lição é outra: o `deploy-pages.yml`
agora **pergunta ao site** — faz `curl` no index e em arquivos-chave, imprime o
código HTTP de cada um e conta as marcas da versão nova dentro do index no ar.
É a única resposta honesta sobre o que a criança está recebendo.

## 🗓️ FILA COMBINADA COM O MARCOS (o que ficou agendado, por ordem)

Ele mesmo mandou agendar. Fica escrito aqui porque eu começo cada sessão sem
memória — e "agendar" só vale se o recado sobreviver ao reinício.

1. **Ler TODAS as pesquisas registradas** — ordem dele (ago/2026): *"faça uma
   leitura nos documentos das pesquisas que temos registrados, tanto as de
   educação, quanto interatividades e neurociência do aprendizado"*. São 24
   `PESQUISA-*.md` + `PEDAGOGIA-APRENDIZAGEM-CONCRETA`, `PEDAGOGIA-VYGOTSKY-
   DINAMICAS`, `AUDITORIA-APRENDIZAGEM-E-DINAMICAS`, `NARRACAO-POR-IDADE`,
   `MODELO-APRENDIZAGEM-EDUCAVERSO`, `CATALOGO-DINAMICAS-INTERATIVAS`.
   **O produto da leitura não é um resumo:** é o `_padrao/RECEITA.md` §7 deixar
   de ser índice e passar a responder por PERGUNTA de montagem ("como faço o
   erro ensinar?", "quantos gestos?", "que som usar?"), com a fonte ao lado.
   Pesquisa que não vira regra na hora de montar não muda atividade nenhuma.
2. **Jardim do Broto** — tirar/corrigir o áudio dos enunciados que não fala o
   mesmo que está escrito, e pôr alto-falante nas respostas (`op_<chave>.mp3`).
   Ele pediu para deixar para depois das correções do 5º ano.

## 🌐 O QUE A REDE DAQUI ALCANÇA (medido, ago/2026) — e por que a voz vai pelo Actions

O Marcos cobrou: *"otimize tudo para que no GitHub não fique essas filas
demoradas e pesadas"*. A otimização que resolveria de vez seria gerar a voz
**aqui**, sem fila nenhuma. Então eu medi, em vez de repetir o que estava escrito.

- O erro do `edge-tts` daqui **não era** "rede bloqueada": era **certificado**.
  O proxy faz MITM e o `edge-tts` usa o `certifi` embutido, ignorando
  `SSL_CERT_FILE`. Juntando o `/root/.ccr/ca-bundle.crt` no `certifi.where()`,
  o TLS passa. **Isso vale para qualquer biblioteca Python que use certifi.**
- Passado o certificado, o portão respondeu **403 ao WebSocket** do
  `speech.platform.bing.com`. Aí sim é política de rede — e não tem contorno.
- Varredura dos hosts: `speech.platform.bing.com`, `*.pollinations.ai`,
  `api.openai.com` → **não conectam**. `generativelanguage.googleapis.com`
  → **404** (ou seja, ALCANÇA; só não tem rota nesse caminho). Mas a chave do
  Gemini vive só como secret do GitHub e o Gemini está sem crédito.

**Conclusão honesta:** voz e imagem continuam sendo pelo Actions. O que dá para
otimizar é **quantas vezes se entra na fila** e **quanto se demora lá dentro** —
foi o que o `entregar.yml` passou a fazer (uma corrida para todas as atividades;
8 falas ao mesmo tempo, pela biblioteca, em vez de subir o processo 199 vezes).

⚠️ E uma economia de contexto: **nunca** chamar `actions_list` sem um filtro que
retorne pouco. Um `list_workflow_runs` com `per_page:1` devolveu **55 mil
caracteres** (o objeto do repositório inteiro, duas vezes). Quando precisar do
id da execução, deixar o resultado cair no arquivo e ler com `python3`.

## 🔎 PESQUISAR TAMBÉM É PELO GITHUB — o esquecimento que ele corrigiu

Ago/2026. Eu disse a ele que não dava para pesquisar na internet daqui, e ele
respondeu: *"veja, mas você pode usar o GitHub para pesquisar, lembra? nós
fazemos tudo de lá"* — e depois: *"faça com que você não se esqueça deste
detalhe"*. **Ele estava certo.** Eu tinha medido corretamente que o CHAT não tem
rede e concluí errado que o PROJETO não tem.

Nasceu daí o **`pesquisar.yml`**: busca no DuckDuckGo (sem chave, sem custo), abre
as páginas, limpa menu e propaganda, salva em `_pesquisa/web/<assunto>.md` e
commita. `git pull` e eu leio aqui.

**A regra que eu tenho que carregar:** *o chat não tem internet; o projeto tem.*
Sempre que eu for dizer "não consigo acessar isso", a frase certa é "vou acionar
o workflow que acessa". Está no topo do `CLAUDE.md` para eu ler no começo de toda
sessão.

---

## 🦴 O ESQUELETO — atividade deixou de ser código e virou CONTEÚDO (ago/2026)

**Pedido do Marcos:** *"precisamos otimizar o processo a ponto de conseguir
deixar uma atividade inteira com o esqueleto em minutos e não em horas"* — e,
para a manhã seguinte: *"eu gostaria de gerar uma atividade e que ela ficasse
pronta no máximo em 1 hora e meia"*.

**O que fazia levar horas não era o conteúdo: era eu reescrever o motor.** O
caça-palavras, a memória, o arrastar, o teclado — a cada atividade, do zero. É
de lá que saíam os defeitos que chegavam nele.

### Como funciona (`_padrao/ESQUELETO/`)

```
conteudo.json  ──▶  montar.py  ──▶  index.html + falas.json + arte.json
```

| arquivo | o que faz |
|---|---|
| `extrair_motor.py` | tira o motor **do Jardim do Broto** (ordem dele: "nosso modelo é a atividade do Broto"). Não se escreve motor do zero: o do Broto já passou por ele, pela banca e pelas crianças. |
| `motor.html` | **gerado.** A espinha: capa, crachá, barra, andaime, medição, mascote com lip-sync, boletim, medalha, relatório do professor, senha `1275@`. Não editar à mão. |
| `integrar.py` | pega as **74 peças** de `_padrao/pecas/` e as vira `MEC["nome"]`, sem reescrever nenhuma. |
| `pecas.js` / `pecas.css` | **gerados.** Todas as mecânicas juntas (938 KB) — o montador recorta só as usadas. |
| `pecas.json` | **gerado.** O formato de `dados` de cada mecânica, com o exemplo da própria peça ao lado. É o que se consulta ao escrever conteúdo. |
| `montar.py` | conteúdo entra, atividade sai. Confere antes: 32 fases, 16 mecânicas (10 até o 2º ano), teto de 40% por gesto, nada de gesto repetido colado, aquecimento no meio. |
| `CONTRATO.md` | o contrato + as ~35 lições pagas. |

### Os dois ganhos que não são tempo

1. **`falas.json` sai do próprio enunciado.** Fica *impossível* a voz dizer coisa
   diferente da tela — o defeito que ele cobrou três vezes num dia deixa de
   existir **por construção**, não por eu lembrar de conferir.
2. **Não há de onde clonar.** O motor é o mesmo para todas; o conteúdo é novo.

### ⚠️ O que essa primeira montagem custou (e virou portão)

A primeira atividade gerada inteira — 32 fases, 16 mecânicas — **reprovou na
banca**, e os quatro defeitos eram do mesmo parentesco: *o que não dá erro é o
que chega na criança*.

- **Resto de clone dentro do próprio esqueleto.** O motor extraído ainda trazia
  os conceitos do Broto (`DOM`/`ROTCRI`/`TREINO`, com o treino apontando para
  telas já removidas), o menu do professor com as 17 telas dele, a pré-carga, o
  alto-falante, o crachá, o nome do mascote, o fundo (cravado no **CSS**) e — a
  pior — a chave do `localStorage` `"jardim_med"`: no GitHub Pages **todas as
  atividades moram na mesma origem**, então duas geradas pelo esqueleto
  apagariam o progresso uma da outra na mesma tarde.
  → **`extrair_motor.py` agora varre o motor pronto atrás de `jd_` e "Broto" no
  código e SE RECUSA A ESCREVER se achar.** Uma marca esquecida ali viraria
  resto de clone em *toda* atividade gerada.
- **A marca de recorte colidia com os comentários das peças** (163 marcas para
  74 peças): o montador partia a peça no meio e escrevia **meia mecânica** — e o
  `node --check` não vê, porque a metade fecha as chaves.
- **`nota()` e a colisão de tipo do `ac`.** As peças usavam dois ajudantes que o
  motor não tinha; e o `ac` da peça é uma **função**, o do motor é o **objeto
  AudioContext** do lip-sync. Nome igual e tipo diferente **não dá erro**: o
  `var ac=` do motor sobrescreve, e só na hora do som é que morre.
  → `integrar.py` agora confere as peças contra o motor e reprova nas duas
  metades (falta e colisão de tipo).
- **Quem achou tudo isso foi o portão que JOGOU** (`_qa/jogador.js`). O
  `node --check` passou, o print ficou perfeito. **Atividade montada não se
  entrega sem o jogador ter chegado à medalha.**

### 🔊 O ciclo da voz: montar → COLHER → montar

O `falas.json` sai do `conteudo.json`, e isso resolve tudo o que está **escrito**.
Mas a peça monta frases **em tempo de jogo** — *"Achou as 4 palavras da horta!"* —
e o montador não tem como adivinhar o número. A saída não é adivinhar: é **jogar
e anotar**. O `_padrao/ESQUELETO/colher.py` roda o auditor-jogador em modo
colheita e transforma o que ele viu em `falas.json`.

*Medido na atividade de teste: 116 textos vistos jogando, 61 falas novas; o
`VOZOK` saiu de 18 para 79.*

⚠️ **O montador PRESERVA o que colheu.** Ele reescrevia o `falas.json` do zero,
então a terceira etapa apagaria o que a segunda ganhou — e as telas de fecho de
rodada voltariam a ficar mudas sem ninguém perceber.

### 🎨 A colisão de CSS entre a peça e o motor (custou 2h de medição)

A peça e o motor usam os **mesmos nomes** de classe — é isso que dispensa
reescrever as 74 peças. O preço: **o que a peça não declara vem do motor**.

- `.tela` no motor é `position:absolute;inset:0` (camada de tela cheia). A tela
  que a peça cria por dentro da fase virava uma camada solta sem largura.
- O `.mcartas` do motor tem `gap:10px`; o da peça fecha a conta com 48% + margem
  1%. O gap entrou de carona e o jogo da memória empilhou as 8 cartas numa
  coluna de 950px — **4 delas fora da tela de 640px da escola**.

Conserto: a `.pecabox` neutraliza a `.tela` do motor, e a peça declara `gap:0`.
E o integrador agora **lista as 54 classes que o motor também estiliza** — é ali
que se olha quando uma conta de largura não fechar.

### 🕵️ Os portões tiveram que APRENDER a atividade montada

Portão que acusa o inocente ensina a ignorar portão. Os quatro que erraram:

| portão | o que ele dizia | por quê |
|---|---|---|
| fluxo | "TELA ÓRFÃ" nas 16 mecânicas | numa montada não há corrente de chamadas: o motor lê `FASES` e chama `MEC[...]` |
| padrão | "82% do gesto *outro*", "16 fases mudas" | o gesto está **escrito** no campo `mec`, não se adivinha do código |
| dinâmicas | 2 armadilhas que não existiam | as 16 mecânicas moram no mesmo arquivo; a regra tem que olhar o bloco **de cada uma** |
| voz da pergunta | 16 perguntas sem voz, tendo 79 | quem fala é um **olheiro no balão**, não uma chamada no código |

Nos dois primeiros, o mesmo descuido: o motor **declara** `FASES = []` e
`VOZOK = {}` vazios e o montador **atribui** os de verdade depois — os portões
liam a primeira ocorrência. Quando há declaração e atribuição, **vale a maior**.

No último, a saída não foi afrouxar: foi **trocar adivinhação por medição** —
nasceu o portão `0f2`, que mede jogando (`colher.py --so-ver`).

---

## 🧰 O QUE A FÁBRICA GANHOU NA NOITE DE 2026-08-12 (para não reinventar)

Capacidades e portões novos, para eu não refazer amanhã o que já existe:

**No motor do esqueleto**
- **Continuar de onde parou, 55 min** — o motor NÃO tinha (só as atividades
  escritas à mão tinham). Agora toda atividade nascida do esqueleto ganha de
  graça: guarda o ÍNDICE da fase (no esqueleto as fases são lista, então não
  precisa envelopar nome de função), a capa oferece "Continuar de onde parei" e
  o convite expira sozinho. Só retoma quem já entrou numa fase (`_emJogo`).
  Testado por `http://` — em `file://` não existe `localStorage` e o teste
  passa mentindo.

**Nas peças (o leque)**
- **Foto da pergunta** em `escolher`, `completar`, `conserte-o-erro` e
  `montar-frase` (campo `img` na rodada): a criança OLHA a cena e responde
  sobre ela. A foto vem ANTES do balão — primeiro olhar, depois ler.
- **Gaveta de arte em vez de função**: `escrever-legenda` e `andar-ate` aceitam
  `img`; antes só aceitavam uma FUNÇÃO de desenho, que o `conteudo.json` não
  tem como preencher.

**Portões novos ou consertados** (todos com a lição escrita no CONTRATO)
- `_qa/beco_peca.py` — o beco medido NA PEÇA, sem navegador, em um segundo.
- integrador: **prosa renomeada** (a criança lia "ache ela na cp_grade") e
  **gaveta que só aceita função**.
- montador: **dependência entre gavetas** (PALDEF só liga com MODO), **gaveta
  técnica declarada pela peça** (`/*TECNICA*/`), **vitrine com menos de 3
  figuras não existe**, e **"a gerar" não vale para arte já na pasta**.
- `_qa/funcoes.py` — parou de acusar inocente (o limpador perde o fio em
  literal de regex).
- `_qa/cartela.py` — conta as folhas por FAMÍLIA, como o planejador conta.
- workflow de imagem — **registra quem desenhou de verdade** e por que o outro
  falhou.

**Três portões que eu tentei escrever e JOGUEI FORA por acusarem inocente**
(está tudo no CONTRATO, com número): "palavra do exemplo em frase da peça"
(52 de 80), o mesmo estreitado para a gaveta principal (27 de 80), e "mesa
clara sem tinta própria" (**80 de 80**). Sem DOM não dá para saber se o
elemento tem texto nem que cor ele herda. Quem mede isso é o `contraste.js`,
que lê o pixel. **Portão estático propõe, navegador dispõe.**

---

## ⛔ O GEMINI VOLTOU A DAR 429 (2026-08-12) — e o registro que MENTIA

Medido hoje, com data, para não virar outro aviso vencido: `gerar-imagens.yml`
com `modelo=gemini` responde **HTTP 429 — "You exceeded your current quota,
please check your plan and billing details"** nos três modelos de imagem
(`gemini-2.5-flash-image`, `-preview` e `gemini-2.0-flash-preview-image-generation`).
Em 07/08 tinha crédito (a seção abaixo); acabou entre as duas datas. **O Marcos
precisa saber: é conta dele.**

**RE-MEDIDO 2026-08-13 (atividade de inglês RIGHT NOW): AINDA 429.** `modelo=gemini`
volta o mesmo `HTTP 429 "You exceeded your current quota"`. Consequência prática
desta rodada: sem edição de imagem, o mascote não pode ter as camadas `_fala`/`_pisca`
(que são EDIÇÃO da pose parada) — então o lip-sync fica bloqueado. E o Pollinations,
único caminho grátis, segue MAL prompt longo/complexo: devolveu uma menina realista
para o mascote e uma janela azul para a medalha. Cura medida: **prompt curto e
FORÇANDO o estilo** ("cartoon clay 3D, plasticine, Pixar style, chibi, big head, NOT
realistic, not a photograph, plain white background") sai muito melhor que o prompt
premium longo. Enquanto o Gemini não voltar, mascote = pose feliz do Pollinations +
`_fala`/`_pisca` = CÓPIA da feliz (não treme, mas não faz lip-sync).

**E o pior desta rodada não foi a cota — foi o REGISTRO.** O workflow cai para o
Pollinations de propósito quando o Gemini falha (para não parar a produção), mas
a mensagem do commit vinha do INPUT: dizia `(gemini)` mesmo quando quem desenhou
foi o Pollinations. Pedi três cartelas, vieram três imagens ruins, e eu já ia
escrever *"o Gemini não entendeu o prompt"* — sobre um serviço que nem tinha
sido chamado. **Diagnóstico em cima de registro falso é chute caro**, e esse eu
ia pagar em rodada de imagem e em confiança do Marcos.

Consertado no mesmo commit, e é a lição que fica: **quem faz o trabalho tem que
assinar o trabalho.** Agora sai `_novo/<nome>.origem.txt` ao lado da imagem e a
mensagem vira `imagem: gera X [desenhado por: pollinations (o gemini falhou:
HTTP 429 ...)]`. Leio com `git fetch` + `git log`, de graça, sem tocar na API do
Actions. Todo caminho com PLANO B silencioso precisa disto: se o plano B pode
entrar sozinho, o registro tem que dizer qual dos dois entrou.

**O que fazer enquanto a cota não volta:** `gerar-imagens.yml` com o input
`lote=<arquivo.json>` — Pollinations desenha, o `rembg` recorta o fundo dentro
do runner, a peça sai transparente, **R$ 0,00**. Fica de fora só o que precisa
EDITAR uma imagem base: as camadas `_fala`/`_pisca` do mascote, que sem edição
fazem o boneco tremer (`_qa/mascote.py`). Essas esperam o crédito.

---

## ✅ O GEMINI TEM CRÉDITO — e a lição do aviso vencido (2026-08-07)

Passei a madrugada repetindo ao Marcos que *"o Gemini está sem crédito (429)"*,
porque era o que estava escrito no `CLAUDE.md`. **Foi ele que estranhou:** *"eu
coloquei 60 reais, não usamos tanto assim, como pode estar sem créditos?"*.

Acionei `gerar-imagens.yml` com `modelo=gemini`. **Voltou imagem, 1024×1024.**
O aviso era de **05/08** e tinha ficado velho.

**A regra que fica, e vale para qualquer serviço de fora (saldo, cota, chave):**

> Aviso de estado externo tem **data de validade**. Repetir o do manual sem
> remedir é passar adiante uma informação que pode ter mudado — e neste caso ela
> teria feito o Marcos recarregar uma conta que já tinha saldo.
> **Medir custa um minuto e centavos.** Antes de repetir, testar.

### O que respondi sobre o consumo (com os números que existem)

- Custo medido: **centavos por imagem** (12 imagens < R$1). R$60 dariam ~700.
- O erro de 22/07 e 05/08 era *"prepayment credits are depleted"* — o billing
  **está** no projeto certo; o que acabava era saldo.
- Neste repositório: **2.234 arquivos de imagem**, **90 rodadas de geração**
  desde 20/07 — a maioria Pollinations (grátis), sem como separar quais foram
  Gemini.
- **E a cartela não estava sendo usada.** A regra existia no manual, mas o portão
  que a cobra (`_qa/cartela.py`) só nasceu em **05/08**, depois de a cartografia
  sair com **45 imagens uma a uma (~R$9 onde ~R$1,60 bastaria)**. Regra escrita
  não é regra cumprida — é a mesma lição de sempre, agora custando dinheiro.

---

## 🔍 A LIÇÃO QUE APARECEU QUATRO VEZES NUM DIA: **existir não é medir**

Não é uma lição sobre código. É sobre **como eu me engano** — e por isso vale
estar escrita num lugar só, com os quatro casos, porque ela vai voltar.

O padrão é sempre o mesmo: **uma coisa que deveria conferir algo produz um
resultado com cara de sucesso sem ter conferido nada.** E como o resultado tem
cara de sucesso, eu sigo em frente — que é o pior desfecho possível, pior do que
uma falha barulhenta.

| onde apareceu | o que "parecia" | o que era |
|---|---|---|
| **três portões da banca** | `ok:` | *"0 alvo(s) conferido(s)"*, *"0 fase(s)"*, *"0 dica(s)"* — não olharam nada |
| **a pesquisa do EdiLim** | arquivo salvo, 1,8 KB, com título | cinco páginas de Scribd dizendo "Client Challenge" |
| **a peça dentro da fase** | a fase abre e joga | rodando com o conteúdo de EXEMPLO, não com o da atividade |
| **o `falas.json`** | montador rodou, arquivo escrito | tinha apagado as 61 falas colhidas jogando |

**A regra que fica, e que já virou código nos quatro lugares:**

> Quem confere tem que dizer **quantos** conferiu. Zero conferido é
> **"rodou cego"**, nunca "passou". E quem gera um arquivo tem que dizer se o
> arquivo tem conteúdo — porque existir não é medir.

Onde isso vive hoje:
- `_qa/auditar.sh` → a lista de **PORTÕES QUE RODARAM CEGOS**, ao lado do veredito;
- `_qa/dinamicas.py` → *"NENHUMA mecânica reconhecida — este portão NÃO mediu nada"*;
- `.github/workflows/pesquisar.yml` → reconhece muro anti-robô e grita quando
  nenhuma página deu texto;
- `_padrao/ESQUELETO/montar.py` → preserva o que colheu e avisa gaveta meia-cheia;
- `_padrao/ESQUELETO/provar_conteudo.js` → abre as 32 fases e confere que o que
  está na tela é o conteúdo **daquela** fase.

---

## 📌 JARDIM DO BROTO — 4 achados do pedagogo que FICAM COMO ESTÃO (decisão do Marcos, ago/2026)

Quando o `_qa/pedagogo.py` deixou de ser cego (ver o commit "portao do pedagogo:
estava CEGO na casa inteira"), ele passou a apontar no Jardim **4 fases em que dá
para errar e o andaime não cresce**: `telaExperimento`, `telaOrdenar`,
`telaPrecisa`, `telaMontaPalavra` — cada uma com uma dica só, sem 2º degrau.

Eu ofereci consertar. **Ele respondeu: *"não precisa mexer em atividades
prontas"*.** Decisão registrada.

**Consequência a NÃO esquecer:** `bash _qa/auditar.sh _jardim/index.html` sai com
**código 1** por causa disso, e isso é ESPERADO. Não é defeito novo, não é
regressão, e **não** é para "consertar" numa próxima sessão. Se um dia o Marcos
pedir a revisão do Jardim, aí sim estes 4 entram na lista.

⚠️ A lição geral: portão que começa a enxergar faz atividade aprovada passar a
reprovar. Isso é o portão funcionando, não a atividade piorando — e a diferença
tem que ficar ESCRITA, senão a próxima sessão gasta a manhã do Marcos
consertando o que ele mandou deixar quieto.

---

## 🧊 FLORESTA DOS NÚMEROS — o travamento nas contagens (ago/2026)

Pergunta do Marcos, do nada, no meio de outro assunto: *"achei que a atividade
meio que travava nas contagens"*. Não era impressão. Reproduzi e medi.

**A causa:** a contagem só andava quando a **voz do navegador avisava que tinha
terminado de falar** (`u.onend`). São **9 lugares** assim no `index.html`, e
todos são contagem: o "Conhecer os números até 10/20/30" e o "vamos contar
juntos" que aparece depois do erro.

Só que a voz nem sempre avisa: quando o motor de fala falha, quando a criança
troca de aba (o Chrome suspende a fala), ou pelo defeito conhecido do `cancel()`
logo antes do `speak()`. E o arquivo **não tinha `onerror` nenhum** (zero
ocorrências) **nem prazo**. Quando o aviso não chega, a contagem **morre
parada** — a tela fica dizendo "Vou começar a contar..." para sempre, e não há
botão nenhum para escapar: só voltando ao mapa.

Por isso era intermitente. O "**meio que** travava" dele era literal.

**Medido** na fase "Conhecer até 10", com a voz indisponível:

| | 0s | 4s | 8s |
|---|---|---|---|
| antes | 0 acesos | 0 | 0 — parada para sempre |
| depois | 1 aceso | 10 | "Concluímos!" |

**O conserto** (commit `bda96498` na `main`): a fala ganhou **prazo** e
**`onerror`**, com guarda para só uma das três portas passar (terminou / deu
erro / estourou o prazo). Uma função só, e cura os 9 lugares de uma vez.
Conferido que **não atrapalha quem tem voz boa**: com motor de fala simulado, o
original e o corrigido falam exatamente a mesma coisa na mesma ordem, sem
repetir e sem pular — o prazo é cancelado pelo `onend` muito antes de disparar.

### ⭐ A REGRA QUE FICA, e vale para TODA atividade da casa

> **Nada na atividade pode depender do retorno da voz para continuar.**
> A voz é enfeite que ajuda muito; ela **não** pode ser o trilho. Todo
> `falar(texto, callback)` precisa de **prazo** e de **`onerror`**, senão um PC
> sem voz — ou uma criança que troca de aba — trava a atividade inteira, sem
> mensagem de erro e sem saída.

Isso é irmão da lição *"existir não é medir"*: o `onend` **existia**, e por isso
parecia seguro. Ninguém tinha medido o que acontece quando ele **não chega**.

⚠️ E uma armadilha desta sessão, registrada para não custar de novo: a branch
`claude/vc-nao-funcionando-0pya0w` carrega uma cópia **VELHA** do `index.html`
(de antes do conserto dos 70 min de validade). **Ela nunca pode ser fundida na
`main`** — desfaria conserto que já está no ar. O conserto das contagens foi
publicado direto na `main`, por worktree, sem passar por essa branch.

### 🐚 E a armadilha do shell que quase me fez mentir

Nesta mesma conversa eu rodei um `cd _padaria` e, várias chamadas depois, listei
os manuais — **de dentro da `_padaria/`**. Conclusão que quase saiu da minha
boca: *"o `MANUAL-MESTRE.md` e o `MEMORIA-DO-PROJETO.md` não existem e nunca
existiram neste repositório"*. Existem os dois, com 1605 e 4837 linhas.

> **O diretório do shell PERSISTE entre as chamadas.** Antes de concluir que
> algo "não existe", conferir o `pwd` — e refazer a busca da RAIZ. É a mesma
> família do aviso que já está no `CLAUDE.md` sobre a cópia local atrasada:
> **"não existe" quase sempre é "eu estava olhando no lugar errado"**.

---

## 💰 O CAMINHO GRÁTIS DE IMAGEM — e a conta que realmente resolve (ago/2026)

Cobrança do Marcos: *"tem alguma alternativa ao Gemini? Pois estou gastando
bastante com as imagens nas atividades"*.

**O que eu medi antes de responder:** o Gemini custa **R$0,20 por chamada** e
cada atividade tem **35 a 54 figuras** (Padaria 35, Naveg 36, Jardim 44, Mapa
54) → **R$7 a R$11 por atividade** quando o lote inteiro vai para lá, que é o
que o `finalizar.yml` faz.

### A descoberta que muda o problema
O Gemini **não estava sendo pago pela imagem** — o Pollinations desenha de
graça. Estava sendo pago pelo **RECORTE**, o fundo transparente que a peça
precisa para assentar na cena. E recorte **não precisa de modelo pago**: o
`rembg` roda dentro do próprio runner do Actions, de graça.

### O que ficou pronto
`gerar-imagens.yml` ganhou o input **`lote`** (um JSON `[{nome,prompt,grupo}]`):
desenha no Pollinations → tira o fundo com `rembg` → apaga os **cacos** do
recorte (mancha abaixo de 8% da principal; não é "fica só a maior", porque o
mexedor do mel e a vela do bolo são partes legítimas separadas) → apara no bbox
→ commita. **Custo R$ 0,00.**

⚠️ **Mora dentro do `gerar-imagens.yml` de propósito:** o GitHub só aceita
`workflow_dispatch` de arquivo que **já existe na branch padrão**. Um workflow
novo criado na branch de trabalho devolve **404** ao ser acionado — testado. Sem
`lote`, o workflow segue funcionando exatamente como antes.

### O veredito honesto da primeira prova (as mesmas 6 peças da Padaria)
O recorte saiu limpo, mas a **arte ficou pior e de outra família**: o pão
francês virou pão de forma, o mexedor do mel caiu fora do pote, o bolo perdeu a
vela e os confeitos, e o estilo não bate com o barro fosco quente da Padaria.
Misturar os dois numa atividade se vê na hora.

### ⭐ A conta que realmente resolve: **CARTELA**
| Jeito | 35 figuras |
|---|---|
| Gemini uma a uma (como estava indo) | ~R$7,00 |
| **Gemini em cartela (9 por chamada)** | **~R$0,80** — R$0,02 a peça |
| Pollinations grátis | R$0,00, com a qualidade acima |

**Corta quase 90% do gasto sem perder nada da qualidade.** O portão
`_qa/cartela.py` já existe e reprova lote com 3+ peças indo uma a uma — ele não
foi respeitado na cartografia (45 imagens uma a uma, ~R$9,00 onde R$1,60
bastava). **Rodar o portão do custo antes de acionar qualquer geração.**

**A divisão de trabalho que fica:** cena/fundo/cenário → Pollinations (grátis,
imagem grande, sem recorte); peça que a criança olha de perto → Gemini **em
cartela**; edição de imagem base (as 3 camadas do mascote) → Gemini, 2 ou 3
chamadas, porque **nada de graça edita**.

### A segunda rodada (prompt afinado) — e o veredito final
Refiz as mesmas 6 peças com prompt curto no jeito do `flux` (243 caracteres no
lugar de 470). **Não fechou a distância:** o estilo chegou mais perto do barro
fosco, mas o objeto piorou — o pão virou rocambole fatiado, o queijo virou um
losango sem furos, o bolo ganhou velas com cara de cogumelo e, ao lado da
garrafa de leite, o motor **desenhou duas cerejas que ninguém pediu**.

E aqui está a distinção que importa: **isso não é defeito de recorte, é defeito
de geração.** O `rembg` fez o trabalho dele; o Pollinations é que não respeita
"um objeto só". Nenhum ajuste de recorte conserta isso.

O apagador de cacos **foi medido aqui, na mão** (não dá para confiar em código
de workflow que nunca se viu rodar): no leite da v1 ele apagou a mancha solta —
6,6% dos pixels — e no mel **não tocou no mexedor**, que é parte legítima
separada. A cereja da v2 tem 8% da mancha principal e ficou de fora do corte por
um fio; **não vou afrouxar o limite**, porque o que está do outro lado dele é o
mexedor do mel.

**Veredito:** o caminho grátis fica para **cena, fundo e cenário** (imagem
grande, sem recorte, onde ele vai bem). Peça que a criança olha de perto
continua no Gemini — **em cartela**, R$0,02 cada.

---

## ✅ PUBLICAR VIROU O PADRÃO, INCLUSIVE NO QUE JÁ ESTÁ NO AR (ago/2026)

Palavras dele, quando eu esperava a autorização para subir o conserto do
caça-palavras do Broto: *"sempre que ficar pronto pode publicar, a não ser que
eu avise o contrário"*.

Isto **amplia** a autorização que já existia (`CLAUDE.md`, "PODE SEMPRE
PUBLICAR", que valia para atividade nova): agora vale também para **melhoria em
atividade que já está no ar**. Não preciso mais parar e perguntar a cada
conserto.

**O que NÃO mudou, e continua valendo:**
- **a banca tem que sair 0 antes** — publicar sem os portões continua proibido;
- **o carimbo se confere depois** (`_status/entrega-<repo>.json` tem que bater
  com o sha do arquivo local): "acho que subiu" não é entrega;
- **o hub `_site/` continua fora** — atividade nova só entra em card quando ele
  pedir com todas as letras;
- a suspensão é dele: basta dizer "espere" / "não publique ainda", e vale para
  aquele trabalho.

---

## 🗂️ IDEIA DO MARCOS: A VITRINE DAS 72 INTERATIVIDADES (ago/2026) — combinado, não iniciado

Palavras dele: *"uma ideia que estou pensando seria: como temos 72
interatividades, você fazer um exemplo de cada dessas 72 interatividades, eu
verifico e aprovo, assim quando formos utilizar já estarão em um formato
aceitável. É só conversa, quando terminar tudo me chama sobre isso."*

**Fica registrado aqui para não se perder**, porque ele disse com todas as
letras que é conversa para DEPOIS que a frente de agora fechar — e porque a
ideia é boa demais para morrer numa mensagem de meio de sessão.

**Por que ela resolve um problema real.** Hoje o portão dele (o Portão 3, o do
professor) só entra em cena quando a atividade está montada — ou seja, ele
aprova a MECÂNICA junto com o CONTEÚDO, no fim da esteira, quando consertar
custa caro. Se ele aprovar a mecânica ANTES, uma vez só, cada atividade nova
nasce de peça já aprovada e o portão 3 passa a olhar só o conteúdo. É antecipar
a aprovação para onde ela é barata.

**A boa notícia da carpintaria:** o exemplo de cada peça **já existe**. Toda
peça em `_padrao/pecas/*.html` é um arquivo que abre e joga sozinho, com
conteúdo de exemplo dentro — foi assim que a bancada (`_qa/peca.sh`) sempre
funcionou. Falta só a **vitrine**: uma página que liste as 77, com o nome, a
descrição do gesto e o link para jogar cada uma; e um jeito de ele carimbar
"aprovada / mexer nisto aqui" sem precisar escrever e-mail.

**O que decidir com ele quando a conversa acontecer:**
- vitrine publicada num repositório próprio (para ele abrir do celular na
  escola) ou arquivo local?
- o carimbo de aprovação fica onde? (uma coluna no `_padrao/DINAMICAS.md` é o
  lugar natural: o catálogo já diz qual atividade tem a versão mais corrigida
  de cada mecânica);
- 72 ou 77? O número dele é de memória; hoje são **77 peças** com porta de
  entrada, e mais duas nascendo do EdiLim (raios-x e letras-escondidas).

**Não começar antes de falar com ele** — ele pediu para ser chamado sobre isso.

---

## 📦 ENTREGA (2026-08-12): as DUAS primeiras atividades montadas pelo ESQUELETO

São as primeiras que **não foram escritas à mão**: nasceram do
`conteudo.json` + `montar.py` + as peças de `_padrao/pecas/`. Publicadas no
repositório de cada uma (o hub NÃO foi tocado — a regra do "por enquanto" segue
valendo), as duas com a banca em **código 0** e conferidas NO AR pelo próprio
site (o `entregar.yml` pergunta ao endereço se ele serve o arquivo que subiu).

| | 6º ano | 9º ano |
|---|---|---|
| nome | A Central de Entregas | RIGHT NOW — Flagra na Cidade |
| assunto | gêneros textuais | inglês, present continuous |
| fases | 39 | 33 |
| gestos diferentes | 17 (nenhum acima de 13%) | 18 (nenhum acima de 9%) |
| vozes gravadas | 656 | 688 |
| pasta | `_central` | `_agora` |
| no ar | https://vidalprof.github.io/a-central-de-entregas/ | https://vidalprof.github.io/right-now-flagra-na-cidade/ |

E no mesmo dia entrou a **terceira**, a primeira que o Marcos pediu pelo nome:

**O Letreiro de Blumenau** — 5º ano, Língua Portuguesa, **M antes de P e B**,
34 fases, 24 mecânicas, 629 vozes, 26 figuras próprias. Pasta `_letreiro`,
no ar em https://vidalprof.github.io/o-letreiro-de-blumenau/

⚠️ **Antes de escrever, eu verifiquei a fundo se já existia** (ele perguntou
*"lembra da atividade do 5º ano que pedia m antes de p e b?"*): varri os 108
repositórios, os cards do hub e o histórico. **Não existia** — `ortografia2-`
é a Caça-Letras do 2º ano e `silabastonicas4-` é sílaba tônica do 4º. O que
existia era o GESTO: a peça `letras-escondidas` nasceu com esse conteúdo de
exemplo (`CA_PO`, `BO_BA`), e foi por isso que ela entrou no catálogo.

**A dívida honesta desta:** o mascote (o Pincel) **não pisca nem mexe a
boca** — as camadas `_fala` e `_pisca` têm que ser EDIÇÃO da pose parada
(gerar do zero faz o boneco tremer) e o Gemini está sem cota desde
2026-08-12. Ele não treme, que era o defeito grave. Refazer quando o crédito
voltar.

**O caminho que funcionou, e que serve para a próxima:**
`esboco.py` → `conteudo.json` → **montar → colher → montar → colher → montar →
auditar**. A colheita não é opcional: é ela que descobre o texto que só aparece
jogando. Depois, `entregar.yml` com `alvos=_pasta:repo,...` grava a voz que
falta, publica e confirma — **uma execução para as duas**.

**Duas coisas que valem para toda atividade daqui em diante** (as duas nasceram
de defeito que chegou perto da criança e viraram lição no
`_padrao/ESQUELETO/CONTRATO.md`):
- **tema escuro cobra o que o tema claro perdoa.** Token de cor que não existe
  (`var(--tinta-d)`) não pinta nada: a letra herda a de cima. No Jardim (claro)
  isso passou anos invisível; na Central (escura) virou creme sobre creme.
- **portão que não sabe abrir a fase tem que sair com código 2, nunca com 1.**
  Três portões reprovaram conteúdo correto nesta entrega (39 fases, 15 fichas e
  11 figuras) porque mediam pelo caminho errado. Portão que acusa inocente
  ensina a ignorar portão — e isso custa mais caro que o defeito.

## ✋ O MARCOS MANDOU PARAR O MOTOR E FAZER À MÃO (2026-08-12)

Palavras dele, depois de ver a atividade de M antes de P e B montada pelo
ESQUELETO: *"Faça a atividade como antes sem o motor / Refaça tudo / Preciso com
urgência para amanhã / Faça do nosso modo antigo como fazíamos as outras
atividades"*. Antes disso ele já tinha apontado três coisas na versão montada:
a dinâmica de **contar sílabas** (que não é o assunto), a linguagem de
**"buraco"/"pedaço"** (não é como a escola fala) e as **imagens ruins**.

**A decisão registrada:** o esqueleto continua existindo e continua sendo o
caminho para ELE montar sozinho; mas quando ele pede uma atividade, ela sai
**escrita à mão**, HTML único, clonando o motor do **Jardim do Broto** — que é
como as que ele aprovou foram feitas. Não discutir, não insistir no motor.

**A atividade:** `_lina/` — *A Oficina de Letreiros da Lina* (5º ano, Língua
Portuguesa, M antes de P e B). 15 fases, 10 gestos diferentes: prever, escolher
a prova certa, a letra que falta, ordenar sílabas, duas gavetas (M/N),
aquecimento, certa/errada, escrever o nome da loja, caça-palavras, **cartaz da
festa (marca-texto: achar os três erros)**, **carta da dona (forca)**, memória,
ensinar a regra à Lina, relâmpago e **a placa do morro** (aplicar tudo numa
placa só).

### O que ESTA rodada ensinou (defeitos meus, e como se pegam sozinhos)

1. **Clonar o motor traz o CSS do CONTEÚDO antigo, não do novo.** As fases novas
   usavam `.palavraGrande`, `.opt.letra`, `.placa`, `.vaga` — nenhuma existia no
   CSS clonado. O `node --check` passa, o app abre, e a fase aparece **sem forma
   nenhuma**. *Regra: classe inventada pelo JS nasce com a regra dela no CSS, no
   MESMO commit.* Quem pega: `_qa/classes.py` (portão 3) — ele acusou `.pequeno`.
2. **Inventei uma função que não existe** (`poeVoz`): no Jardim quem instala o
   alto-falante é o **MutationObserver** sobre `ZAPSEL`, não uma chamada por
   resposta. A tela estourava no `telaCerta`. Quem pega: `_qa/funcoes.py`.
3. **O `data-qa` marcado FIXO num botão de sim/não** faz o auditor-jogador bater
   sempre no mesmo lado e dar **"PRESO"** numa fase que a criança fecha. Onde a
   resposta muda a cada rodada, a marca muda junto (`marcaCerta()`).
4. **`.jpg` no código, `.png` no disco** — o fundo nunca carregava. É a MESMA
   lição de agosto, e ela voltou pelo clone. Conferir sempre a extensão real.
5. **O portão `_qa/voz_dupla.js` só sabia andar pela atividade MONTADA**: numa
   escrita à mão ele estourava com `FASES is not defined` e **parava a bancada
   inteira** sem medir nem dizer que não mediu. Ensinado a conhecer as duas
   formas e a sair com **código 2** quando não souber abrir a fase.
6. **Texto que a voz não consegue ler**: o enunciado tinha `CA_PO` e a gaveta
   dizia `com M<br>antes de P e B` (que no `textContent` vira *"com Mantes de P e
   B"*). Enunciado é para ser **falado**: nada de sublinhado no meio da palavra
   nem de `<br>` dentro do texto que vira chave de voz.

### 📌 FILA COMBINADA COM O MARCOS (13/08)

1. **Terminar o TANGRAM** (`_tangram`) — é o que está na mão.
2. **Depois: reescrever a `_agora`** (*RIGHT NOW, Flagra na Cidade*, 9º ano,
   Present Continuous). Palavras dele: *"essa atividade foi feita pelo MOTOR,
   então deve ter vários problemas. Preciso que você reescreva depois e veja o
   que aproveita"*. Ou seja: refazer À MÃO, no modo antigo, aproveitando o que
   presta (o conteúdo das 33 fases, os 689 áudios e as 33 imagens já existem —
   isso é muito trabalho pago que não se joga fora). ⚠️ Ela está NO AR: não
   mexer no repositório publicado antes de a nova passar pela bancada.

### 📇 "VOCÊ JÁ TINHA FEITO, POR QUE NÃO LEMBRA?" — a cura (13/08)

Ele perguntou pela atividade de inglês do 9º ano. Eu procurei por "inglês" e
"english", não achei, e respondi que **não existia**. Existia: **`_agora` —
*RIGHT NOW, Flagra na Cidade*, 33 fases, 18 mecânicas, 689 áudios, no ar desde
12/08**. Nem "inglês" nem "english" aparecem no nome dela.

**As duas partes da resposta honesta:**
1. Eu começo cada sessão **sem memória**: só sei o que está escrito. Por isso
   esta memória existe.
2. **Mas escrito não basta se estiver escrito onde eu não procuro.** Nesta
   sessão eu tinha listado o `_status/` com o
   `entrega-right-now-flagra-na-cidade.json` na minha frente e não liguei os
   pontos. O assunto mora dentro do `conteudo.json`, não no nome da pasta.

**A cura, e ela é medida:** `python3 _qa/indice.py` varre todas as pastas e
escreve o **`ATIVIDADES.md`** na raiz — pasta, título, ano, fases e o link de
quem está no ar. E `python3 _qa/indice.py <assunto>` procura **dentro** dos
arquivos, não pelo nome:

```
python3 _qa/indice.py ingles
_agora  RIGHT NOW - Flagra na Cidade  9º ano  33 fase(s)  no ar: .../right-now-flagra-na-cidade/
```

⚠️ **Regra que fica: antes de dizer que algo não existe, rodar o índice.** E ao
escrever o índice eu tropecei no mesmo defeito de novo — a primeira versão
procurava campo a campo (`objetivo1`, `objetivo2`) e falhou justamente no
`_agora`, onde os objetivos moram dentro das fases. **Quem procura assunto não
pode depender do formato: lê-se o arquivo inteiro.**

### ⏱️ AJUSTE PEQUENO NÃO PASSA PELA BANCADA INTEIRA (ordem do Marcos, 13/08)

Palavras dele: *"Não precisa passar no portão para ajustes pequenos, lembra? Não
estamos fazendo pelo motor e sim por você como antes"*.

Eu tinha transformado a bancada em pedágio de tudo: **40 minutos** de Chromium
por causa de uma cor, de um comentário, de um percentual. A bancada inteira
existe para a ENTREGA de uma atividade nova ou de uma mudança de peso — não para
cada conserto.

**A regra que vale:**
- **Ajuste pequeno** (cor, texto, posição, um comentário, um dado numa lista) →
  rodar só os portões DO QUE MEXI (`_qa/mascote.py`, `_qa/clone.py`,
  `_qa/classes.py`, `vozigual`, `falas`...) + `node --check`. Segundos. Publicar.
- **Bancada inteira** → atividade nova, fase nova, mudança de motor, ou quando
  ELE pedir.
- E ao contar, contar direito: *"os portões do que mexi passaram"* não é
  *"a bancada aprovou"*. Nunca trocar um pelo outro.

> **🖼️ RECORTE DE FIGURA: MÁSCARA BINÁRIA, NUNCA ALFA POR LUMINÂNCIA (19/08).**
> O Marcos pegou os avatares da tela "Quem vai jogar?" *"errados, até piorou"* — 3x.
> Causa raiz: recortei a cartela de fundo PRETO com **alfa derivado da luminância**,
> então as áreas CLARAS INTERNAS (o BRANCO DOS OLHOS, listras claras do boné) viraram
> transparentes → na tela a paisagem aparecia PELOS OLHOS (cara "boiando"). O `node`,
> a banca e o print pequeno não pegam — só se vê AMPLIADO e sobre fundo contrastante.
> Conserto certo: **máscara BINÁRIA** — pixel não-preto (`max(R,G,B)>38`) = OPACO (255),
> `binary_fill_holes`, split em GRADE (componentes quebram no cabelo escuro), recorte
> rente. E SEMPRE conferir o recorte **compondo sobre VERMELHO** (vaza = furo) e no
> **render real ampliado** antes de publicar. Enquadramento: copiar o do Jardim
> (figura preenchendo, margem ~zero, retrato) — não emoldurar com margem grande.
> Eu errei 3x por publicar sem olhar de perto: **avatar/figura recortada só fecha
> depois de ver o pixel ampliado sobre fundo contrastante.**

> **🎨 ARTE — O CLAUDE NÃO GERA, O MARCOS GERA (regra do Marcos, 19/08):**
> *"não usar Pollinations, eu gero as artes com os prompts que você passa"*. Então:
> o Claude **passa os prompts** (em bloco copiável) e o Marcos **gera e sobe** as
> imagens. O Claude **nunca** aciona `gerar-imagens.yml`/Pollinations por conta
> própria. O que segue sendo do Claude: **recortar/tratar** as imagens que o
> Marcos subir (recorte de fundo local, aparar bordas) e montar as camadas do
> mascote EDITANDO a pose parada dele. Impresso no hook de início de sessão.

> **🔁 REINCIDÊNCIA 19/08 (Trem do Alfabeto) — "isso tem que ser SEMPRE lembrado"
> (ordem do Marcos):** eu re-rodei a bancada INTEIRA várias vezes no meio dos
> ajustes (cruzadinha, forca, 3 erros de texto) e ainda a chamei de "25 min". O
> Marcos: *"isso não pode acontecer, pq daí você não cumpre o processo e eu perco
> tempo; tínhamos combinado otimizações para reduzir o tempo de banca"*. Os dois
> fatos que eu esqueci: **(1)** a bancada roda em PARALELO (`auditar.sh` larga os
> 3 navegadores + jogador juntos) e é RÁPIDA — poucos minutos, não 25; **(2)**
> durante os consertos usa-se **`_qa/revisor.py`** (testador humano de texto) e/ou
> **`bash _qa/auditar.sh --reparo <html>`** (portões de texto, segundos), NUNCA a
> bancada inteira. A inteira roda **UMA vez**, na entrega. Este lembrete agora
> imprime no início de TODA sessão (`.claude/hooks/sync-remoto.sh`).

### 🤔 POR QUE EU ERRO ESSAS COISAS (a pergunta dele, 13/08)

Ele perguntou, e a resposta honesta vale mais registrada do que dita:

1. **Clonar traz junto o que não é meu.** Copio o motor de uma atividade aprovada
   (é a ordem, e é o certo), e junto vem o conteúdo dela — as borboletas, o CSS do
   prato, o comentário da lupa. Nada disso dá erro: o app abre, o `node --check`
   passa, o print fica bonito. Resto de clone é o defeito mais silencioso que
   existe.
2. **Eu enxergo o que ensinei a bancada a medir.** Cada portão nasceu de um
   defeito que já tinha chegado nele. Um defeito de tipo NOVO passa sempre — a
   primeira vez é sempre de graça. Por isso todo achado dele vira portão no mesmo
   dia: é o único jeito de o mesmo erro não voltar.
3. **Eu aprovava pelo PRINT, e a criança JOGA.** Os três achados de hoje só
   existem em movimento ou na relação figura×texto: a boca que não abre (só se vê
   falando), o boné que balança (só se vê animado), o letreiro fora da tábua (o
   print sozinho não diz onde é a tábua). Print parado aprova qualquer coisa.
4. **Eu começo cada sessão sem memória.** O que não está escrito não existe para
   mim — por isso esta memória, e por isso a senha "RELEIA A MEMÓRIA".

Nada disso é desculpa: é o mapa de onde os defeitos nascem. Os quatro têm o mesmo
conserto — **escrever a regra e pô-la para medir sozinha.**

### A rodada de 13/08 — fechando a Oficina ("preciso que termine essa")

A atividade passou de **15 para 18 fases** e ficou com **6 gestos** diferentes.
O que esta rodada consertou, e o portao que passou a pegar cada coisa sozinho:

| defeito | quem pega agora |
|---|---|
| a **forca anunciava a palavra** no `data-qa`: uma tecla revela VARIAS letras e quem conta o passo pelas teclas usadas se perde | (tirado o atributo; a fase anda a cada toque) |
| a **barra voltava de 81% para 66%** — os `setProg` carregavam a numeracao de quando as fases estavam noutra ordem | `_qa/progressao.py` (ja pegava; **eu** e que li so o ultimo portao da lista) |
| **tres cartas de memoria com o mesmo texto** ("M, porque depois vem P" servia a CAMPO, SEMPRE e LAMPADA): a crianca virava duas certas e ouvia erro | `_qa/memoria_pares.py`, item 1b (compara o que a crianca VE, lendo a `face:`) |
| a atividade **nao enchia a aula** (ele mediu 14 min e pediu 40) | **`_qa/duracao.py`** (portao 3g), que pesa o gesto: digitar 25 s, procurar 20 s, tocar 8 s |
| a **voz dizia numeros velhos** em 4 fases ("5 palavras" onde a tela mostra 10) | `_qa/vozigual.js` (ja pegava) |
| **"complete" saindo "complite"** em 3 falas | `_qa/falas.py` — que so agora le o arquivo certo |
| o portao da narracao lia **`_lote_falas.json` da raiz**, sobrado de outra atividade: dizia "ok" depois de conferir 34 falas ALHEIAS enquanto as 129 desta passavam sem ninguem olhar | corrigido no `_qa/auditar.sh` (le `$PASTA/falas.json`) |

**O jogo da memoria virou o padrao da casa:** virada 3D de verdade (`rotateY`,
com queda para troca-de-face onde nao houver 3D), **brilho correndo** pelo verso,
par que **pulsa** ao fechar, **placar de pares** — e o placar ACIMA do tabuleiro,
porque embaixo ele ficava atras da barra fixa do "Ouvir de novo". Sao **6 pares
por partida sorteados de 10**: cabe na tela da escola e a partida seguinte vem
diferente.

⚠️ **A licao que mais custou nesta rodada nao foi de codigo: foi de leitura.** A
bancada imprime todos os portoes e so o veredito fica no fim. Eu vinha lendo o
ultimo erro, consertando um por rodada e gastando meia hora de bancada por vez —
enquanto a queda da barra estava impressa na tela desde a primeira. **Bancada se
le inteira.**

### O estado (2026-08-12, noite)
- 97 vozes gravadas (`entregar.yml`, `so_voz=sim`), todas com MP3 no lugar.
- "Continuar de onde parou" por **55 minutos** — os três testes passaram em
  `http://`.
- Três figuras saíram ruins do Pollinations (campo, bomba, lâmpada) e foram
  mandadas de novo com prompt reescrito (`_lote_lina.json`, R$ 0,00).
- A pasta `_letreiro/` (a versão do esqueleto, recusada) foi retirada da árvore;
  a história do git continua guardando tudo.

## ✋🔧 DUAS ORDENS DO MARCOS QUE VALEM DAQUI PARA FRENTE (2026-08-12, noite)

### 1. ATIVIDADE SE FAZ DO MODO ANTIGO — não pelo motor

Palavras dele, depois de eu ter voltado a mexer no esqueleto: *"Veja mais, você
não ia fazer do modo antigo para criar as atividades? Como fazíamos antes"*.

Ele estava certo, e o erro foi meu: a **atividade** eu fiz à mão (certo), mas
depois voltei a investir a noite no **motor do esqueleto** — porque o lembrete
automático da madrugada manda trabalhar nele. **A ordem é dele, não do
lembrete.** Se o lembrete e o Marcos discordarem, quem manda é o Marcos.

**Regra que fica:** atividade nova = **HTML único, escrito à mão, clonando uma
que ele já aprovou** (o Jardim do Broto é o modelo). Nada de `MEC[...]`, nada de
`conteudo.json`, nada de montar por peças — a não ser que ELE peça, com todas as
letras. O esqueleto continua existindo e continua servindo para ELE montar
sozinho; só não é o caminho das atividades que ele encomenda.

### 2. IMAGEM SE PEDE EM CARTELA — inclusive quando sou EU que escrevo o pedido

Palavras dele: *"Não seria melhor você gerar em cartelas?"*.

Ele tinha razão duas vezes. **Na atividade:** as três figuras refeitas da Oficina
da Lina ficaram destoando das outras justamente porque saíram **uma a uma**, em
gerações diferentes — cada uma com a sua luz e a sua escala. Refeitas em **duas
folhas** (12 palavras), saíram irmãs.

**E na ferramenta:** o gerador de prompts que eu tinha acabado de escrever
(`_padrao/ESQUELETO/prompts.py`) **nascia pedindo uma imagem por vez**. A regra
da cartela estava no `CLAUDE.md`, tinha ferramenta pronta (`_padrao/cartela.py`)
e portão que mede (`_qa/cartela.py`) — e mesmo assim o arquivo novo saiu
ignorando as três coisas. **Regra que o código novo não herda não é regra: é
sorte.** Corrigido: agrupa sozinho, com **uma família por folha** (juntar
medalha, seis crachás e mascote numa folha só faz a IA obedecer o "mesma escala"
e devolver a medalha do tamanho da criança).

### 3. E o recorte da cartela ganhou dois consertos (pagos na mesma noite)

- **Peça com PARTES SOLTAS perdia os pedaços.** O desenho do vento tem árvore,
  três espirais e duas folhas voando — sete componentes para UMA peça. O corte
  pegava "os N maiores" e jogava cinco partes fora. Sai bonito, só que faltando,
  e ninguém vê o que não está lá. Agora agrupa por **célula**: todo componente
  dentro da mesma célula da folha é a mesma peça.
- **O BRILHO virava halo preto.** A lâmpada acesa dissolve o amarelo no preto da
  folha; máscara dura recorta um anel escuro, que aparece feio sobre o fundo
  claro da atividade. Agora, na zona escura, o alfa segue o brilho do pixel.

⚠️ E a lição de método, que é a que mais custou: **eu reescrevi um recorte que a
casa já tinha.** O `_padrao/cartela.py cortar` existia, era melhor que o meu, e
eu só descobri depois de entregar um corte que comeu os ponteiros do relógio.
Antes de escrever qualquer coisa: procurar se já existe.

## ♻️ REGRA NOVA (ago/2026): reaproveitar o banco de imagens
Marcos reverteu a regra "arte sempre nova". Agora:
- **Mascote e imagens do banco PODEM ser reaproveitados** entre atividades.
- **Mascote novo só quando o Marcos pedir** — na dúvida, reusar do banco.
- **Toda imagem que o Marcos gera → o Claude põe no banco** (`python3 _banco/montar.py`).
- **Ao desenvolver, CONSULTAR o banco** (`_banco/index.json`; o montador reporta
  `no_banco` × `gerar`): se existe, aproveita; senão, passa o prompt para o Marcos gerar.
- O portão `_qa/arte_propria.py` **não reprova mais reuso** (virou informativo, exit 0);
  quem pega resto de clone de verdade (prefixo alheio) é o `_qa/clone.py` item 8.
Detalhe completo no CLAUDE.md (seção "REAPROVEITAR O BANCO DE IMAGENS").

## 🗺️🌐 FORMATO "SITE/LIVRO DE PESQUISA" (EXCEÇÃO) — contrato p/ passar jogador+banca (ago/2026)

O Marcos pediu atividades **em forma de site/pesquisa** (5º ano SC = portal rolável;
3º ano Cartografia = **livro de páginas**) — HTML custom, NÃO o ESQUELETO. Reaproveitei
o motor de **voz (`_chaveVoz`+audio/), Firebase (`/provas/<slug>`), avatares, medalha e
quiz** da prova. Para o **jogador** e a **banca** aprovarem um custom, tem que casar o
CONTRATO das mecânicas (li o `_qa/jogador.js` — ele espera marcação exata):

- **Quiz:** opção = `class="opc c<i> opt"` + `data-qa="1"` na CERTA. `#trilha` fica no
  fundo escuro → texto BRANCO (teal dá 1.4:1). Medalha precisa da classe **`.medal`**
  (não só `.medalha`), senão "NÃO CHEGOU NA MEDALHA".
- **Navegação (livro/portal):** botões "Próxima/Aos desafios" precisam da classe **`opt`**
  (o robô só clica os seletores de `SEL`). "Voltar" fica SEM `opt` (senão o robô volta).
- **Caça-palavras:** `<div class="grade" data-qa='{"MAPA":{"r":0,"c":0,"n":4,"dl":0,"dc":1},...}'>`
  (o robô lê as posições do JSON no data-qa da grade); células `.cel` em ORDEM row-major,
  largura em **%** (`100/N` + border-box), **NENHUMA palavra cruzando** (célula-ponta
  compartilhada trava o toque e a fase não fecha), **grade ≤ 8 colunas** (célula ≥30px no
  celular, senão leiaute reprova); chips `.pchip` com `data-qa="PALAVRA"` e ganham a classe
  **`feito`** ao achar. Ao fechar a última, avançar SÍNCRONO (setTimeout longo faz o robô
  desistir por "sem ação").
- **Digitar:** `<input data-qa="RESPOSTA">` escondido (o robô preenche) + teclado na tela
  + `document.onkeydown` (teclado real) + **auto-avança quando o texto == resposta**
  (o robô não clica OK sozinho). Resposta SEM acento.
- **Banca:** custom sem função `limpa()` → o auditor NÃO detecta as telas sozinho; rodar
  `bash _qa/auditar.sh <html> telaCapa telaLivro telaPergunta telaCaca telaDigitar`
  (passar as telas na mão). `crachaHTML` sem `<img>` de src vazio (senão "imagem quebrada"
  na renderização sem estado). Vidro fosco = `backdrop-filter:blur` (isenta do "quadrado
  branco"). Branco no laranja `#e07a3f` = 2.99:1 → usar `#c25f28`.
- **Duração:** o `_qa/duracao.py` foi ESTENDIDO p/ contar LEITURA de portal (item com
  `texto:`+`fala:` = 70s "ler", não 9s "tocar"). Mesmo assim, site curto (3º ano) fica
  <40min → é **EXCEÇÃO** que o Marcos autoriza ("não precisa ser como o auditor quer").
- **Imagens reais (cartografia):** Commons rende melhor com termo em INGLÊS
  (`globe Earth`, `magnetic compass`, `world map political`, `floor plan`).
- **Mascote estático** (sem lip-sync): publicar só a pose parada (`_feliz`); fala/pisca
  juntas disparam o portão de tremor. Reuso de coruja do banco serve de placeholder.

## 👆 O PORTÃO DO DEDO — `_qa/sobreposto.js` (set/2026, pedido do Marcos)

Nasceu de uma frase dele sobre a Pinta e Monta do 1º ano: *"a área de pintura de
algumas imagens fica em cima das cores, dificultando para os alunos escolherem as
cores, tendo que diminuir o zoom manualmente no navegador"* — e o pedido que
importa: ***"tipo de erros que seria legal o profissional que criamos pegar"***.

**A pergunta que ele faz é uma só, e é geometria pura:** no centro deste botão,
quem responde ao toque? Se responde OUTRO elemento, o de baixo está inalcançável
por mais bonito que fique no print. Nenhum portão antigo pegava isto: o
`leiaute.js` mede TAMANHO (e os alvos tinham 40px certinhos), o `encaixe.js` mede
se o conteúdo cabe (e cabia), e a foto parada parece boa. O defeito só existe no
GESTO — só o `elementFromPoint` o enxerga. Roda em dois tamanhos: **o netbook da
escola (1024x600)** e o celular (412x820).

**O que ele achou na estreia, varrendo as 74 atividades — cinco defeitos reais
que estavam no ar, todos invisíveis no print:**
| Onde | O que a criança via | O que o dedo tocava |
|---|---|---|
| Ateliê de Cores (netbook) | "Pronto!" no fim da pintura | "Ouvir de novo" |
| Museu dos Bichos (netbook) | "Ver mais bichos" | a barra de baixo |
| Museu dos Bichos (celular) | alto-falante da ONÇA | "Dica" |
| 3 provas (Léo/EF, Mat 2º, Vale 4º) — celular | o 6º crachá de personagem | liga/desliga o som |

**⚠️ AS QUATRO ARMADILHAS que ele já pagou, e por isso estão escritas no código:**
1. **Fora da janela não é coberto** — é rolagem. Sem esse cuidado ele acusava 28
   inocentes de uma vez (listas que rolam de propósito).
2. **Filho e pai não se cobrem** — botão com `<img>` dentro devolve a `<img>`.
3. **Tela de capa não é obstrução** — quem cobre mais de 90% da janela é a CAPA
   esperando o primeiro toque (`#telaIntro`, `#start`), não vizinho mal posto.
4. **Enfeite não é conteúdo** — a 1ª versão do "esmagado" usava
   `scrollWidth > clientWidth` e acusou a barra de progresso e a moldura da
   figura do Agora: o que transborda ali é o BRILHO CORRENDO, um `:before` posto
   de propósito para fora e cortado. Agora ele olha os FILHOS DE VERDADE,
   pulando pseudo-elemento, `position:absolute` e `pointer-events:none`.

### 🪤 E A LIÇÃO MAIOR: ele aprendeu "ESMAGADO" porque a CONTA disse "ok" e a FOTO disse não

Ao crescer o palco da Pinta e Monta (o Marcos tinha pedido: *"com isso a área de
desenho pode ser maior"*), o flex **esmagou a coluna das miniaturas para 8
pixels** e o portão passou — corretamente, porque nada estava COBERTO. Estava
espremido, que é outro defeito com o mesmo efeito: a criança não vê.

**Ensiná-lo custou TRÊS tentativas erradas, e elas valem mais que o conserto:**
1. Comparei `getComputedStyle(el).width` com o retângulo renderizado. **Medido:
   dão o mesmo número** — o computed style de largura devolve o valor USADO, já
   esmagado, não o que o CSS pediu. Era 1 dividido por 1.
2. Li a largura pedida nas REGRAS de CSS (respeitando media queries) e botei um
   **limiar chutado de 40%**. Refiz a quebra de propósito: a galeria caiu de
   116px para 54px — **47%, acima do limiar**, e passou de novo. Só que 54px com
   miniatura de 104px dentro já é o defeito inteiro.
3. `scrollWidth > clientWidth` — acusou os enfeites (item 4 acima).

**O que mede de verdade é FATO GEOMÉTRICO, sem calibrar nada:** um filho de
verdade fica para fora da caixa E a caixa esconde o que sobra
(`overflow-x:hidden|clip`). `auto` não entra: ali a pessoa rola e alcança.

**A regra que fica:** *número chutado não mede nada; e portão que diz "ok" não
dispensa a foto.* Duas vezes no mesmo dia o portão aprovou e a imagem reprovou.

## 🃏🤖 UNO DOS NÚMEROS 3/4/5 — e as três lições que ele pagou (set/2026)

Pedido do Marcos: *"Lembra do jogo do uno? Que criamos? Preciso de uma versão
mais difícil para os 3/4/5 anos"*. **Ele estava certo e eu estava errado**: eu
disse que o jogo não existia, porque meu `grep` casava "ALUNO" (contém "UNO") e
eu só procurei neste repositório. O jogo estava no ar em `jogoUno1-` havia
tempo — **e não tinha linha no `ATIVIDADES.md`**, que é a minha memória. Por
isso ele agora tem (`_uno1`), e o novo também (`_uno345`, três linhas: 3º, 4º e
5º ano). Regra confirmada na prática: **atividade fora do catálogo é atividade
que eu vou negar que existe.**

**Novo:** `_uno345/` → <https://vidalprof.github.io/uno-dos-numeros-345/?ano=4>
(`?ano=3` / `?ano=4` / `?ano=5`; sem nada = 4º). O antigo continua intacto.
O detalhe completo está no `_uno345/LEIA-ME.md`.

### Lição 1 — "mais difícil" se MEDE, não se acha
Fui procurar por que o jogo do 1º ano é fácil e não era o baralho: era o
adversário. `cpu.findIndex(c => podeJogar(c))` — ele jogava a primeira carta
jogável na ordem em que ela caiu na mão. Escrevi um **jogador automático** que
joga partidas inteiras sozinho, e comparei o robô novo com o antigo, com o mesmo
jogador burro dos dois lados: **250 partidas cada**.

⚠️ **A armadilha do benchmark:** o alívio anti-frustração (`_derrotasSeguidas`)
derruba o robô para força mínima depois de duas vitórias dele — numa corrida de
250 partidas ele passa quase o tempo todo lá, e a diferença entre os níveis
some. Para medir força tem que **zerar `_derrotasSeguidas` a cada partida**.
Sem isso a 1ª medição disse que o nível 5 era o mais FRACO, o contrário da
verdade.

### Lição 2 — a jogada mais forte era a que eu não tinha visto
Com dois jogadores, **"pular" e "girar" devolvem a vez para quem jogou**: é uma
carta a menos de graça. Meu robô "esperto" só usava essas cartas quando a
criança estava quase ganhando — e por isso ganhava 56% contra os 54% do robô
burro, ou seja, quase nada. Dando peso ao **turno extra** ele subiu de verdade.
Serve de regra: ao fazer IA de jogo, procurar primeiro a jogada que **repete o
turno**, não a que "parece agressiva".

### Lição 3 — a mão da criança estava fora da tela do laboratório
Em **1024 × 600**, que é a tela dos PCs da escola, a mão da criança ficava
**inteiramente abaixo da dobra**: ela lia "toque numa carta que brilha" e não
via carta nenhuma. Herdado do jogo do 1º ano, então **provavelmente valia para
ele também**. Curado com modo compacto (`max-height:820px, max-width:560px`),
e a regra ao encolher é **encolher a MOLDURA, nunca o ALVO** — a 1ª tentativa
deixou os botões do topo em 32px e o próprio testador reprovou.
⚠️ Medir com a mão CHEIA (14 cartas), não com as 7 do início.

### O que virou padrão para jogo (não-motor)
Jogo de tabuleiro/cartas não passa pela banca do motor (não tem `telas` nem
`falas.json`). O que passa a valer no lugar:
1. **jogador automático** que joga partidas inteiras e cobra: 0 erro de JS,
   0 partida travada, 0 carta brilhando contra a regra, a regra realmente
   aparece;
2. **medição de força** contra a versão anterior, com o mesmo jogador burro;
3. **leiaute/contraste em 6 tamanhos**, com a mão no pior caso.

## 🔧🔬 A AUDITORIA PESSOAL DO MOTOR E DOS PORTÕES (set/2026)

Pedido do Marcos, com a sessão no modelo máximo: *"corrija o motor e os portões e
otimize tudo para ser mais rápido e sem erros"* — e, quando eu quis delegar a uma
equipe de agentes: *"quero que você faça tudo pessoalmente"*. Fiz. Está aqui o
MÉTODO (para repetir) e as LIÇÕES (para não repetir os defeitos).

### O método: medir antes de mexer
1. **Baseline com número**: cobaia (`bash _qa/cobaia.sh`) e banca cronometrada
   (`bash _qa/auditar.sh <montada>`; agora imprime `⏱` por portão e o total).
   Antes: cobaia 12m38s REPROVADA; banca da _gincana **849s**.
2. **Censo dos portões** (`censo_portoes.py`, no scratchpad da sessão — vale
   reescrever): cada portão de texto contra 4 alvos (_cobaia, _gincana, _trem,
   _tangram), anotando código, tempo e "mediu zero". É isso que separa portão
   cego (sai 2 em TUDO), falso-positivo (reprova atividade no ar) e ruído.
3. **Censo das peças** por script (timers, globais, keyframes, toque, ES5).
4. Só depois: consertar na FONTE e provar peça a peça que o defeito sumiu.

### O que estava quebrado e chegava à criança
- **`circuito` media 6 pixels de largura dentro do motor.** Na bancada a placa é
  um bloco e estica; no motor o pai é coluna flex centrada e bloco sem `width`
  encolhe até o conteúdo (zero, tudo absoluto). As 6 pontas caíam no mesmo
  pixel. A cobaia dizia "botão sobre botão" — a mensagem certa era "a placa
  sumiu". **Regra**: peça com palco de geometria absoluta declara `width:100%`.
- **`ensinar-mascote` estourava na tela final** (`FECHO is not defined`): a frase
  estava em DUAS strings sem `+` (erro de sintaxe) e no PRIMEIRO `<script>` da
  peça — o "motorzinho" de bancada que o integrador DESCARTA. Conteúdo mora no
  segundo script. O ESLint da cobaia pegou; ninguém tinha lido.
- **20 peças fechavam por função própria** (`fimCal`, `fimContadores`,
  `telaFimTermo`…). O integrador só religa `fimDaPeca`; a guarda "acabaram as
  rodadas" (`if(!X[ri]){ fimY(); return; }`) levava direto à tela de BANCADA,
  com "Jogar de novo" e sem fase seguinte. Todas passaram a fechar por
  `fimDaPeca` — **regra da casa: peça fecha por `fimDaPeca`, e só por ele.**
- **Relógios da fase anterior**: 277 `setTimeout` soltos nas peças, 70 delas com
  callback que atravessa a troca de fase (`mostraBanner` em 68). O motor agora
  anota todo relógio criado com a fase viva e o `limpa()` mata todos. O que
  precisa sobreviver (pré-carga, o "Boa!" que sobe, o olheiro do balão) usa o
  relógio cru `_stRaw` — com o motivo escrito ao lado.
- `zeraRetomada()` nascia com MED incompleto → "Dicas usadas: NaN" no relatório
  de quem tocava "Começar do início".
- 4 peças de arrasto sem `touch-action:none` (circuito, grafico,
  mapa-conceitual, tangram): no iPad o arrasto vira rolagem.

### Portões que mentiam (e o padrão por trás)
- `halo.py` olhava a RAIZ da pasta; as figuras moram em `img/`. Cego em 100% das
  atividades, todo dia — e ninguém estranhou porque estava na lista dos "cegos"
  junto com 13 que só "não se aplicavam". **A lista de cegos tem que ser curta
  para ser lida**: agora "não se aplica" é lista separada.
- `zonas.js` exigia nome de fase; a banca passava só o arquivo → tela de USO em
  toda atividade. Numa montada ele acha as fases `achar-na-cena` sozinho.
- `cor_fixa.py` reprovava o MOTOR em toda atividade (10 "cravadas"): não sabia
  que quem pinta é o ÚLTIMO elemento do seletor descendente; e o motor tinha
  cor de texto solta em regras sem fundo. Os dois lados foram consertados.
- `clone.py` reprovava _gincana e _trem (no ar, aprovadas) porque o nome do
  portão `cor_fixa` citado num comentário casava com o prefixo `cor_` da pasta
  de imagens `_colecao`. E a `_cobaia` era "vizinha": toda frase de exemplo
  virava "igual à da _cobaia".
- `provar_portoes.sh` (o meta-portão) estava **vermelho há dias** por duas
  provas envelhecidas (regra de arte revogada; pasta `_prova30` apagada).
  Meta-portão vermelho permanente é o mecanismo exato dos "erros bobos
  repetidos": ninguém mais olha.
- `beco.py` só conhecia `PE&#199;A`; a `calendario` escreve `PE&Ccedil;A`.
  Ao ensinar a grafia, ele revelou as 20 peças acima.

### Velocidade: onde estavam os 849 segundos
leiaute 239s · jogador 215s · prova de sala 101s (no fio principal, tudo
parado) · vazamento 88s · voz-robo/voz dupla 81s · tema claro 75s · contraste
73s · diretor de arte 60s · encaixe 56s · imagem quebrada 44s.
O padrão comum: **recarregar a página inteira (700 KB) para cada tela** — o
leiaute fazia 240 recargas. O motor desenha a fase por `montaFase(i)` em cima da
página viva; só telas com nome (capa, quem joga, fim) precisam recarregar,
porque leem o estado salvo. Aplicado em leiaute, contraste (removendo a folha
"texto transparente" depois do print), imagens, encaixe (abria um navegador
NOVO por tela) e selo. Mais: semáforo = CPUs−1 (era 2 cravado), prova de sala
numa faixa paralela, jogador em trechos com ÁRBITRO serial
(`_qa/joga_banca.sh`: rápido quando passa, o antigo dá a palavra final quando
reprova).

### O que ficou MEDIDO no fim (antes → depois, mesma máquina, mesma atividade)
- **Banca inteira na `_gincana`: 849s REPROVOU → 542s APROVOU** (leiaute
  239→176s, jogador 215→85s, encaixe 56→41s; a prova de sala saiu do fio
  principal). A reprova "antes" era falsa (cor_fixa no motor + clone na
  `_colecao`), não defeito da atividade.
- **Cobaia do motor: 12m38s → 9m14s**, e o leiaute nela (6 tamanhos × 92 telas,
  84 fases) **rc=0, sem alvo abaixo de 40px** — depois de consertar circuito
  (`.placa` com 6px de largura dentro do `.centro`) e passo-a-passo (`.mesa`
  encolhida a 204px). Os dois eram o MESMO defeito: bloco sem `width` dentro de
  um flex-column com `align-items:center` encolhe para o conteúdo.
- **Lista de portões CEGOS na `_gincana`: 8 → 0.** Não porque passaram a medir
  algo — porque agora dizem "NAO SE APLICA … Nada a conferir." quando a
  armadilha não existe naquela atividade, e a banca os separa dos cegos de
  verdade. Regra: **portão que imprime "0 X conferidos" sem dizer POR QUE está
  mentindo por omissão** — ou ele mede, ou declara que não se aplica.
- **`provar_portoes.sh` (meta-portão): vermelho → verde (rc=0).**
- **ESLint: 0 erros nas 17 montadas + cobaia** (o `FECHO is not defined` era
  string quebrada em `ensinar-mascote`, no script que o integrador descarta).
- ⚠️ Um "achado" meu era falso: registrei que o `vozresposta.js` dizia "sem motor
  de fases" na `_gincana`. Não dizia — ele achava 0 respostas tocáveis (32 fases
  de `divisao-dourado`, peça de manipular). Lição: **ler a saída do portão no
  log da banca, não a memória do que ele "costuma" dizer.**
- Defeito de ARTE que ficou de fora (sem cota no Gemini): `_trem/img/tr_coru_fala`
  é cópia byte a byte da pose parada — a coruja não mexe a boca. Avisado ao Marcos.

## 🧩📏 A MEDIÇÃO DAS 88 INTERATIVIDADES DA FÁBRICA (set/2026)

Pedido do Marcos: *"teste todas as interatividades da fábrica que usamos nas
atividades, corrija todas, deixe perfeitas… pesquise amplamente… melhore o motor
se for necessário… mais ágil, mais rápido, menos erros"*. Feito pessoalmente, no
método de sempre: **censo no código → medida no navegador → conserto na FONTE →
medir de novo → portão que pega sozinho da próxima vez.** O detalhe técnico está
no `_padrao/DINAMICAS.md` (seção "O que a medição das 88 peças ensinou"); aqui
fica o que EU preciso lembrar.

**Ferramentas que passaram a existir (usar, não reinventar):**
- `bash _qa/peca.sh <peça>` já existia (9 portões por peça). O lote nas 88 roda em
  ~1 min/peça/faixa; com 2 faixas, ~50 min. Resultado importado para
  `_padrao/_bancada.json` por `python3 _padrao/interatividades.py --bancada <RESUMO>`.
- **`_padrao/interatividades.py` GERA o `INTERATIVIDADES.md`** (antes era à mão e
  dizia 84 peças; são 88). Peça nova, atividade nova, lote novo → rodar.
- **`_qa/toque.js`** mede `touch-action` no navegador (banca `1t`, bancada `5d`,
  prova 27 do meta-portão). O `toque.py` (lista) continua para o runner sem
  Chromium e recebeu os 16 nomes que a medida achou.
- Cobaia = **88 de 88** (`_qa/cobaia.py`, `PULAR` vazio — medido: o jogador fecha
  as 4 de produção livre pelo "Pronto").
- Pesquisa pelo `pesquisar.yml`: 5 arquivos `_pesquisa/web/interatividades-*.md`
  (arrasto/toque, feedback, usabilidade infantil NN/g, LM-GM-SDT, desempenho).

**O que a medida achou e foi consertado na fonte:**
- 19 peças cujo alvo escuta o dedo **sem `touch-action`** (rolava sob o dedo no
  iPad) — 16 `none` (arrasto) + 3 `manipulation` (toque). Nenhuma estava na
  lista do `toque.py`. **Lição: portão de lista é memória; quem manda é a medida.**
- **Escutas de fase vazando**: 14 peças pendem `document.addEventListener` sem
  remover, 42 atribuem `document.onmousemove=`. Museu (36 fases): 34 escutas
  vivas no fim → motor anota e o `limpa()` solta → **0 vivas**. Sem tocar em peça.
- `simulador` na cobaia sem tema de água (o `dinamicas.py` reprovava o fixture,
  não a peça) → enunciado do fixture declara a água.

**Lote da bancada da peça nas 88 (`_qa/peca.sh`, ~58 min de CPU em 2 faixas):
84 PRONTAS de primeira; girar, linha-do-tempo, mudanca-permanencia e
divisao-dourado consertadas na fonte → 88/88.** A divisao-dourado sozinha tinha
5 defeitos latentes que só a bancada avulsa mostrou (tela sem `limpa()`, pulso
`scale` que deixa o alvo instável, relógio `avanca` que estourava ao recomeçar,
tela de fim sem `.medal`, contraste 4,16:1 no tema claro) — na atividade montada
o motor mascarava três deles. Detalhe e regras no `DINAMICAS.md`.

**Ferramenta nova: `ver-rodando.yml` + `_padrao/ver_rodando.js`** (pedido do
Marcos: *"veja essas atividades rodando na internet"*): abre a referência num
Chromium do GitHub, clica/arrasta, fotografa (PC e celular) e mede eventos,
`touch-action`, alvo mínimo, fonte, som e mutações do feedback. **Gatilho por
push em `_pesquisa/rodando/PEDIDO.json`** (workflow novo fora da `main` não
aceita `workflow_dispatch` — 404). Saída: `_pesquisa/rodando/<lote>/RODANDO.md`
+ fotos. Lições do lote 1: `h5p.org/<tipo>` redireciona para a home (17 fotos
iguais — ler as fotos antes de acreditar na tabela); PhET precisa de
`?screens=1`; índices (Escola Games, Wordwall) não servem — tem que ser página
de JOGO; e um regex de `href` deixou as 10 buscas vazias em silêncio (busca que
não acha tem que gritar — consertado).

**📚 "Aprenda tudo sobre esses jogos" (Marcos, set/2026) → `_pesquisa/JOGOS-EDUCACIONAIS-REFERENCIAS.md`.**
Campanha de ~25 pesquisas pelo `pesquisar.yml` (casas + fundamentos) + 3 lotes
do `ver-rodando`. O documento tem: as casas (H5P, PhET, MLC, Toy Theater, PBS
KIDS, Cooney Center, ICT Games/Topmarks, GCompris, JClic, Wordwall/LearningApps/
Educaplay, Toca Boca/Khan Kids, Escola Games/NOAS), os fundamentos (4 pilares
de Hirsh-Pasek; Malone & Lepper + integração intrínseca; Plass GBL; andaime
implícito do PhET; gamificação em números + superjustificação; NN/g; WCAG 2.5.7;
UDL), a tabela do que medi por baixo de cada casa e **12 regras propostas** para
as 88 peças (prioridade: pressionar responde ≤150 ms; nada anima sem função;
figura responde ao toque; nunca só cor; simulador tematizável; caça-palavras
que ensina ao achar; cruzadinha falada; reflexão no relâmpago; artefato da
criança no fim). **Lições da campanha, para não repetir:** (1) as fontes boas
são PDF — `pesquisar.yml` agora lê PDF (pypdf); (2) 20 workflows commitando ao
mesmo tempo → push em corrida "cannot lock ref" → o lote 3 inteiro do
`ver-rodando` (40 fotos) se perdeu; os dois workflows agora tentam 6 vezes; (3)
`h5p.org/<tipo>` redireciona para a home — ler as FOTOS antes da tabela; (4)
PhET abre em tela de escolha → `?screens=1`; (5) busca que não acha tem que
gritar (o `BUSCAS.md` do lote diz status e trecho da resposta).

**O que a medida mostrou que NÃO é defeito (não "consertar"):** carga 55–128 ms;
o montador embute só as peças usadas; `preventDefault` no `touchstart` = 0 (12
suspeitas eram do `touchmove`); toque simples (WCAG 2.5.7) existe nas 5 peças
que pareciam sem; caminho duplo mouse+toque em 32 peças **funciona** — Pointer
Events só para peça NOVA.
