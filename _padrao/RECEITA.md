# 🍞 A RECEITA — montar já certo, sem o Marcos ter que apontar

> Cobrança dele (ago/2026): *"temos uma sequência para criar atividades, certo?
> O padrão que criamos hoje e da atividade do Broto, e você registrou os erros,
> auditorias etc. Precisamos otimizar isso, para tudo ser mais rápido e sem
> erros, **para que eu não fique toda hora dizendo o que tem que ser arrumado**"*.
>
> E antes disso: *"preciso que você treine para antes de montar, para quando
> você monte já sair perfeito, mesmo o portão verificando"*.
>
> **O portão é a rede de segurança, não o método.** Se eu monto errado e conserto
> depois, gasto o dobro e ainda escapa coisa. Este arquivo é o método: as
> ARMADILHAS de cada dinâmica, escritas ANTES de montar. Cada item aqui nasceu de
> um defeito que chegou até ele.

---

## 0-A. QUEM SENTA NA MESA ANTES DE MONTAR (regra do Marcos — ele já tinha dito)

> *"vários profissionais, auditores etc antes de entregar: roteirista, pedagogo,
> especialistas da área"* · *"quando for atividade até o quinto ano tem que ser um
> especialista PEDAGOGO; quando for do 6º ao 9º, um especialista da DISCIPLINA"* ·
> *"um roteirista que cria a história"*.

**A composição do painel muda com o ano — e isso não é detalhe:**

| Ano | Quem manda no conteúdo | Por quê |
|---|---|---|
| **Pré ao 5º** | **PEDAGOGO** (alfabetização, matemática inicial, ZDP) | nessa idade o COMO ensinar decide mais que o conteúdo: concreto antes do símbolo, andaime, uma ideia por tela, tudo narrado |
| **6º ao 9º** | **ESPECIALISTA DA DISCIPLINA** (professor de História, de Geografia, de Ciências…) | aqui o conteúdo tem profundidade própria e erro conceitual pesa; o pedagogo continua na mesa, mas quem decide o conteúdo é a área |

**E em todos os anos, sempre:**

| Papel | O que ele entrega | O portão dele |
|---|---|---|
| **ROTEIRISTA** | a HISTÓRIA. A atividade não é lista de exercícios com tema: é uma viagem com problema no começo, viradas no meio e gancho no fim. Sem ele vira questionário fantasiado | Portão 0 (filosofia) |
| **GAME DESIGNER** | os gestos, escolhidos pelo ENCAIXE (§2) | `_qa/padrao.py` |
| **ESPECIALISTA EM INTERATIVIDADE** | como o toque RESPONDE: alvo grande, resposta imediata, as duas portas (dedo e teclado), o gesto que o conteúdo pede. É ele que sabe as armadilhas do §4 | `_qa/leiaute.js`, `_qa/jogador.js` |
| **WEB DESIGNER** | hierarquia, ritmo, espaço, contraste, e que tudo isso funcione no PC velho da escola e no celular | `_qa/contraste.js`, `_qa/classes.py`, `_qa/leiaute.js` |
| **DIRETOR DE ARTE** | proporção, contexto, coerência; tudo pintado por IA, nada copiado | `_qa/arte_propria.py`, `_qa/mascote.py` |
| **ENGENHEIRO** | o motor e os portões | `node --check`, `_qa/funcoes.py`, `_qa/fluxo.py` |
| **PhD EM TESTES / QUALIDADE** | a banca inteira, e — o mais importante — **a banca que APRENDE** (§0-B) | `_qa/auditar.sh` |

---

## 0-B. O ESPECIALISTA EM TESTES QUE **AUTO-APRENDE**

> *"um especialista em testes que auto aprende"* · *"testes de qualidade PhD na área"*

Esta é a regra que mais vale dinheiro do projeto inteiro, e ela é simples:

> **Todo defeito que chega ao Marcos tem conserto em DUAS partes: arrumar o código
> E criar (ou estender) o portão que pega aquilo sozinho da próxima vez.**
> Sem a segunda parte, o trabalho NÃO está feito.

É isso que faz a banca crescer sozinha. Ela não nasceu de um plano: cada portão é
a cicatriz de um defeito que passou. **Hoje são 24**, e nenhum foi inventado —
todos vieram de algo que a criança (ou o Marcos) viu antes de mim:

| O que passou | O portão que nasceu |
|---|---|
| função que não existe estourava no clique | `funcoes.py` |
| sobrou conteúdo da atividade de origem | `clone.py` |
| a barra andava para trás | `progressao.py` |
| imagem copiada de outra atividade | `arte_propria.py` |
| o mascote tremia ao falar | `mascote.py` |
| a voz errava a palavra | `falas.py` |
| resposta fora da tela | `leiaute.js` (10 regras) |
| a criança empacava numa fase | `jogador.js` |
| a tela ficava vazia falando sozinha | `telavazia.py` |
| o botão de som falava outra coisa | `vozpergunta.py`, `vozigual.js` |
| a intro calava a pergunta (27 fases) | `vozintro.py` |
| a fase ficou muda: o mp3 nunca foi gerado | `vozfalta.py` |
| a dica falada ≠ dica escrita | `vozdica.py` |
| a figura era cortada dentro do quadrado | `leiaute.js` regra 10 |
| o enunciado encostava nas respostas | `leiaute.js` regra 9 |
| a escada didática não subia | `pedagogo.py` |

**Como o especialista de testes trabalha (o método, não a lista):**
1. **Reproduz** o que o Marcos viu — na tela, no tamanho dele, jogando.
2. **Mede** em vez de olhar. Cor de pixel, proporção, folga em px, trocas por
   segundo. *"Parece certo" não é resultado.*
3. **Pergunta: quantos mais existem?** Um defeito quase nunca é um. A escola do
   "símbolo escola não é falado" eram 27 fases; a do enunciado encostado, todas.
4. **Escreve o portão** que mede aquilo em TODA fase e em toda atividade futura.
5. **Roda nas outras atividades** — o mesmo motor carrega o mesmo defeito.
6. **Registra** na memória e na RECEITA, com a frase do Marcos entre aspas, para
   o próximo eu saber POR QUE aquilo existe.

⚠️ **Portão que imprime NADA não é "passou": é "rodou cego".**
⚠️ **Portão que acusa quem está certo é pior que portão nenhum** — ensina a
ignorar portão. Quando um deles der falso positivo, o conserto é NELE.

**Ordem da mesa:** currículo → **pedagogo/especialista** (a escada) → **roteirista**
(a história) → game designer (os gestos) → arte → engenheiro → banca automática →
**Marcos (portão final)**.

⚠️ O portão `_qa/pedagogo.py` mede a parte mensurável da escada. Ele **não**
substitui a mesa: não sabe se o conteúdo está certo para o ano nem se a história
tem graça. Portão nenhum substitui olhar.

---

## 0. A ORDEM DE MONTAR (nunca outra)

1. **Currículo**: BNCC do ano + a âncora de Blumenau. O verbo do objetivo manda.
2. **Escada didática** (§1) — desenhar a escada ANTES de escrever qualquer fase.
3. **Escolher os gestos** pelo ENCAIXE (§2), não por lista.
4. **Escrever o `falas.json` junto com a tela** (§3). Texto da tela = texto da voz.
5. **Montar as fases** seguindo as armadilhas de cada dinâmica (§4).
6. **Fim de atividade**: copiar `_padrao/FIM-DE-ATIVIDADE.md` e `_padrao/RETOMAR.md`.
7. **Arte em CARTELA** (`_qa/cartela.py` antes de gerar).
8. `bash _qa/auditar.sh <arquivo>` — a banca **confirma**, não descobre.
9. `entregar.yml` (pasta + repo) — uma corrida só: voz que falta, publicar, conferir.

---

## 1. A ESCADA DIDÁTICA — o que o Marcos quer dizer

> ## 🛑🎯 A REALIDADE DA AULA MANDA MAIS QUE A PESQUISA — leia isto antes de §1
>
> Palavras dele (ago/2026), depois de eu trazer as pesquisas: *"mas veja, eles
> nunca voltam a fazer a mesma atividade, é sempre diferente; e não podemos fazer
> muito difícil, a criança tem que conseguir passar. Achei que a atividade do
> Broto está perfeita e o pessoal está gostando, não sei se devemos aplicar essas
> regras"*. **Ele está certo, e eu estava aplicando pesquisa feita para outro
> cenário.** Quase toda a literatura parte de um app usado por SEMANAS. Aqui é
> **uma atividade, uma aula, uma vez** — e turma de escola pública, com a criança
> que lê devagar na mesma sala da que voa.
>
> **NÃO se aplica (e não se tenta aplicar de novo):**
> - **Revisão espaçada de 1/3/7/14 dias** — ninguém volta. O que vale é o
>   Aquecimento no MEIO da própria aula, que a casa já faz.
> - **Medir retenção dias depois** — não existe nesse contexto.
> - **A última dica não revelar a resposta.** Esta é a mais perigosa das seis: a
>   pesquisa protege contra quem burla o sistema por semanas; a aula protege
>   contra **a criança travada, que perde a aula inteira**. Entre as duas, manda a
>   segunda. **O 3º erro continua revelando e seguindo.**
> - **Portão de domínio** que segura quem não atingiu X — mesma razão.
>
> **Continua valendo (é acabamento, não dificuldade):** os números do som,
> **embaralhar as opções**, não repetir o mesmo gesto em fases vizinhas, 44px de
> alvo para os pequenos, contar junto em voz alta.
>
> **🚫 E MAIS UMA REGRA DE PESQUISA DESCARTADA — a das animações.** Palavras dele
> (ago/2026): *"as animações que a gente vem fazendo não travam em nada, nem essa
> do loop; acho que vamos desconsiderar essa regra"*. A literatura manda animar só
> `transform`/`opacity` e proibir loop enquanto a criança pensa, por dois motivos:
> travar a máquina e distrair. **O primeiro ele mediu no parque de máquinas dele,
> em uso real: não trava.** O segundo ele viu com a criança na frente. Quem tem os
> PCs e a turma é ele; teoria não ganha de observação. **Não reprovar animação por
> propriedade nem por loop.**
>
> **E o que já está aprovado NÃO se mexe.** O Jardim do Broto está no ar, as
> crianças estão gostando, e "melhorar" o que funciona é o jeito mais rápido de
> estragar. Ideia nova entra em atividade NOVA.
>
> **A pergunta que eu faço antes de adotar qualquer regra de pesquisa:**
> *isso pressupõe que a criança volta amanhã? isso pode deixar alguém sem
> conseguir passar?* Se a resposta for sim para qualquer uma das duas, não entra.


> 🛑 **AS MUDANÇAS DESTA SEÇÃO VALEM PARA AS PRÓXIMAS ATIVIDADES — NÃO SE MEXE
> NAS QUE JÁ ESTÃO PRONTAS.** Ordem do Marcos (ago/2026): *"não faça essas
> modificações nessas atividades; depois vejo o que eu quero modificar na próxima
> que a gente criar"*. Ou seja: ler as pesquisas mudou a RECEITA, não o acervo.
> Mexer no que já está no ar (Voo do Nico, Terra dos Papagaios, Jardim do Broto,
> e as demais) só quando ELE pedir, atividade por atividade. Aplicar em massa uma
> ideia nova, por melhor que ela seja, é justamente o jeito de estragar o que já
> estava aprovado.


Não é a barra de progresso (isso é sintoma). É a escada do aprender:

- **O problema vem primeiro, o conceito por último.** A criança tem que sentir a
  falta antes de receber o nome. Nunca começar explicando.
- **Concreto → figural → simbólico.** Manuseia (a maquete, o voo, o porão do
  navio) → vê a figura → só então encontra o símbolo, a letra, a palavra.
  **Medida:** o primeiro símbolo não pode aparecer antes do primeiro figural.
- **⬇️ E o degrau tem caminho de VOLTA.** Bruner não é escada de mão única: quando
  o símbolo emperra, a MESMA fase tem que deixar descer ao concreto (ver de novo a
  figura, contar de novo as peças). Sem isso, quem trava no símbolo trava e pronto.
  `→ PEDAGOGIA-APRENDIZAGEM-CONCRETA` (destilado em `_pesquisa/REGRAS-APRENDIZAGEM.md`)
- **O andaime CRESCE a cada erro:** 1º erro = dica que faz pensar; 2º = consolo +
  apoio concreto; 3º = **apoio máximo — e a criança AINDA produz**. **Nunca** a
  mesma dica três vezes.
  - 🚫 **O 3º nível NÃO entrega a resposta do item que está sendo avaliado.**
    Corrigido em ago/2026 depois de ler a pesquisa: quem pode clicar até sair a
    resposta aprende ~2/3 do normal (Baker, "burlar o sistema"). O molde certo é
    **"mostro UM, você faz o resto"** — preenche um exemplo, acende uma fileira,
    mas a mão que responde continua sendo a dela.
    `→ PESQUISA-AJUDA-E-AVALIACAO`
  - ⚠️ **Em fase sem "errar"** (caça-palavras, exploração, memória) o andaime
    cresce pelo **tempo parado**, não pelo erro. Empacar calado é onde a criança
    desiste, e ninguém vê. 25s → diz o que procurar; 50s → acende o começo.
- **Aquecimento no meio — e ele NÃO é a revisão espaçada.** São duas coisas, e
  confundi-las fez a gente achar que cumpria as duas cumprindo uma:
  - **Aquecimento** = prática de recuperação e intercalação DENTRO da sessão. Vai
    no meio (o portão do pedagogo mede: entre 25% e 65% do caminho).
  - **Revisão espaçada** = caixas de **1 / 3 / 7 / 14 dias**, disparada quando a
    criança volta **noutro dia**, no máximo 1 por dia. É o que faz o aprendido
    FICAR — e é a única coisa que mede retenção de verdade.
    `→ MODELO-APRENDIZAGEM-EDUCAVERSO`
- **A régua de sucesso é TRANSFERÊNCIA + RETENÇÃO, não estrela nem tempo no app.**
  Na prática: uma fase final **de propósito sem dica e sem apoio**, com item novo,
  e a medição dias depois pelo Aquecimento ("X de Y reacendidos de primeira").
  Sem isso a atividade termina no gancho e ninguém sabe se ensinou.
- **Uma ideia por tela.** Enunciado curto, narração junto com a figura.
- **Nunca prova disfarçada.** Nota nunca; parecer sempre.
- **Fecho com gancho** — termina deixando pergunta aberta.

**Confere sozinho:** a barra tem que subir na ORDEM REAL de jogo (a cadeia do
`fechaFase`), não na ordem do menu do professor — as duas são diferentes, e foi
por isso que a do 3º ano andava para trás em duas passagens.

---

## 2. OS GESTOS — variedade que a criança sente

Contar **gestos, não conteúdos**: duas fases podem ensinar coisas diferentes e
ser, para a criança, *a mesma tela pela terceira vez*.

- Nenhum gesto acima de **40%**; no mínimo **4** gestos; mirar 8–12 numa
  atividade de ~20 fases. Medido pelo `_qa/padrao.py`.
- A mecânica tem que ser o **gesto natural** daquele conteúdo: linha do tempo em
  História, simulador em Ciências, forca e cruzadinha onde a PALAVRA é o
  conteúdo. Mecânica enfiada à força cansa igual.

---

## 3. A VOZ — quanto narrar por ano, e as cinco regras que já custaram caro

### 3-A. A DOSE MUDA COM O ANO (regra do Marcos, ago/2026)

> *"a questão do áudio também: mais necessário para os pequenos; porém os maiores
> já não gostam muito de ficar ouvindo fala toda hora — mas mesmo assim um botão
> de som para ajudar os que não sabem ler nos anos finais"*.

Ele está apontando duas coisas que parecem opostas e não são:

| Ano | Quanto a voz toca SOZINHA | O botão de som |
|---|---|---|
| **Pré · 1º · 2º** (~5–8) | **TUDO, sempre.** Cada tela, cada dica, cada explicação toca sozinha. Nada essencial fica só escrito | em tudo: enunciado **e** cada resposta |
| **3º · 4º · 5º** (~8–11) | os **momentos-chave**: o problema/convite, a pergunta de cada rodada, o acerto com a descoberta, a virada — **e mais dois que a pesquisa marca como obrigatórios nesta faixa: CONTAR JUNTO em voz alta sempre que houver contagem ("uma… duas… três… quatro! cheia!"), e a DICA FALADA quando ela erra** | enunciado **e** cada resposta |
| **6º ao 9º** (~11–14) | **narração leve**: abertura, viradas e incentivo. Curta. **Não** tocar a cada tela — nessa idade voz demais irrita e eles desligam o som (e aí perdem até o que precisavam) | **continua em tudo, mas só quando ELE toca.** Nos anos finais ainda há criança que não lê fluente, e ela não pode ser exposta: o botão está lá, discreto, e ninguém vê quem usou |

**A regra que junta as duas pontas:** *nos anos finais a voz não se impõe — ela
fica disponível.* Tirar o botão porque "eles já leem" abandona exatamente a
criança que mais precisa, e de um jeito que ninguém percebe. Deixar tocando
sozinho o tempo todo faz o resto da turma desligar o som e perder o que importa.

⚠️ Vale para as respostas também: `op_<chave>.mp3` em toda opção tocável, em
todos os anos. Muda o **auto-play**, não o **acesso**.
*(base: `NARRACAO-POR-IDADE-2026-07.md`)*

### 3-B. As cinco regras que já custaram caro

1. **O `falas.json` é a verdade.** Escreveu o texto ali, a voz sai (o
   `entregar.yml` grava sozinho o que falta ou mudou). Sem ele não há como
   conferir nada: mp3 não se lê.
2. **A voz diz EXATAMENTE o que está escrito** — enunciado *e* dica. O botão
   existe para quem não lê; texto diferente = instrução diferente.
   *(portões `vozigual.js` e `vozdica.py`)*
3. **A intro não pode calar a pergunta.** `falaDaTela(pergunta)` seguido de
   `falar(intro)` faz a intro entrar por cima: na 1ª rodada a criança ouve só a
   abertura. Usar `introEPergunta()`. *(portão `vozintro.py` — pegou 27 fases)*
4. **Toda resposta que a criança toca tem alto-falante** (`op_<chave>.mp3` +
   `VOZOK`). Sem isso ela escolhe pelo desenho e a atividade vira loteria.
5. **Em fase embaralhada, o id da voz vem do ITEM, nunca do contador da rodada.**

---

## 4. AS ARMADILHAS DE CADA DINÂMICA

*(cada linha é um defeito que chegou ao Marcos — não invente nada aqui, só some)*

### Achar na cena / no mapa
- Vale tocar em **qualquer parte** da coisa. Zona é a FIGURA recortada por cor de
  pixel (grade 48×48), não um pontinho com raio. "Toca na rua e dá errado" foi
  cobrança dele.
- O alvo visível fica no pixel **mais longe da borda** da região
  (`distance_transform_edt`), nunca no centroide — o centroide de um rio em curva
  cai fora do rio.
- Achou = **V de verificação** verde, não círculo. E nunca quadrado branco.
- Pergunta no singular só se houver UMA na figura (`_qa/ambiguo.py`).
- Relação espacial precisa de referência: "do outro lado do rio" não diz de que
  lado. Dizer **"o lado da sua direita"**.

### Arrastar
- **Três caminhos, sempre:** mouse, dedo e toque simples. No celular o navegador
  dispara mouse FANTASMA depois do toque — guardar `ultimoToque`.
- **Nunca** `preventDefault` no `touchstart` (mata o toque).
- A vaga acende quando a peça passa por cima.

### Teclado na tela (cruzadinha, forca, monte a palavra)
- Tem que aceitar **também o teclado de verdade** (`document.onkeydown`).
- Letra usada **sai do `data-qa`** — senão o auditor-jogador (e a criança
  teimosa) fica tocando na mesma para sempre.
- Palavra fechada **comemora**: letras acendendo em cascata, faixa com a palavra,
  som subindo.
- **Acento**: o teclado não tem tecla de acento, então a palavra a adivinhar vai
  sem — mas a que aparece na faixa é a **certa** (`ac:"BÚSSOLA"`).

### Caça-palavras
- A grade tem que ter as **colunas da grade lógica**: célula em `100/N` por cento
  com `box-sizing:border-box`. Com largura fixa em px cabem 10 numa grade de 9 e
  a palavra quebra de linha.
- Diagonal também (4 direções), e o enunciado avisa.
- Célula conquistada **trava**; a conferência conta `mark` OU `ok` (senão palavra
  que cruza outra nunca fecha).
- Cada palavra com a SUA cor, no chip e na grade.

### Memória
- Carta **fluida ≥ 130×88px**, verso de arte de IA, virada 3D, brilho correndo,
  par que pulsa, placar, som próprio de virar e de formar par.
- Em tela baixa encolhe a LETRA, nunca a carta.

### Pintar / marca-texto
- A figura é **arte de IA**; o CSS só anima o que se mexe.
- Mapa começa **sem cor** e a criança pinta de verdade (camadas recortadas por
  pixel, tingidas com a cor da legenda).
- No texto: traço de caneta correndo da esquerda para a direita, som de risco,
  barra de quantas faltam, carimbo no fim.

### Simulador / deslizar
- O mundo reage **de verdade** (a água que sobe, o navio que avança). Foto que
  gira não é simulador.
- Ponto medido na figura, não a olho: navio que ancora no continente errado
  estraga justamente o que a fase ensina.

### Classificar em gavetas
- Enunciado sem termo que a criança não conhece ("veio de lá" → **"veio de
  fora"**).
- As gavetas se **refazem** quando o eixo muda (cima/meio/baixo ≠
  esquerda/direita) — e os dois eixos nunca se misturam na mesma sequência.
- A explicação do acerto **espera o áudio acabar** (`depoisDaFala`), não um
  `setTimeout` fixo.

### Quiz / escolher
> ⚖️ **O limite, decidido em ago/2026 depois de ler as pesquisas.** O pedagogo do
> `PEDAGOGIA-VYGOTSKY-DINAMICAS` diz "quiz nunca é opção", e a auditoria registra
> as 3 paradas de escolher que foram **redesenhadas para produção** — porque
> produzir retém 30–50% mais que reconhecer. A regra honesta da casa: **quiz
> continua valendo como gesto de VARIEDADE, mas nunca carrega a evidência
> principal de um conceito.** Onde o conceito é medido, a criança PRODUZ
> (contadores, construção, teclado de dígitos). Mirar ≤ 2 telas de quiz em 20.
- Cada opção com alto-falante.
- **Embaralhar as opções.** Defeito já pago: na Fábrica de Estrelas a certa era
  sempre a 1ª, e a criança aprendeu a posição, não o conteúdo.
- Distratores plausíveis, nunca absurdos.
- A dica da barra tem que falar da **tela que está ali** ("de cima você vê o
  telhado" numa tela de mesa e carro não bate).

---

## 5. AS ARMADILHAS QUE NÃO SÃO DE NENHUMA DINÂMICA

**📏 O alvo de toque: 40 px no portão, 44 px na pesquisa — e por quê.**
O `_qa/leiaute.js` reprova abaixo de **40 px**; a pesquisa de acessibilidade pede
**≥ 44 px** para criança que ainda não lê. São 4 px que o portão deixa passar, e
isso está aqui escrito de propósito, para não parecer descuido: **até o 2º ano
mirar 44 px**, porque o dedo é menor e a criança erra o alvo antes de errar a
resposta; do 3º em diante 40 px é o piso que ainda cabe numa grade de
caça-palavras sem quebrar a linha. Onde der para dar 44, dê.
`→ AUDITORIA-APRENDIZAGEM-E-DINAMICAS` (destilado em `_pesquisa/REGRAS-APRENDIZAGEM.md`)


- **Fecho de fase nunca deixa a tela vazia falando** — usar `fechaFase()`.
- **O enunciado nunca encosta** no que vem depois (6px de folga; é regra do
  motor, `.balao + *`).
- **Figura nunca cortada na caixa**: `object-fit:cover` numa peça cuja proporção
  não bate corta o topo do barril. `contain` + fundo claro. Cena larga é a
  exceção.
- **Figura que não existe não vai para a tela** — quadradinho vazio é pior que
  figura nenhuma.
- **Mascote**: falar e piscar são EDIÇÃO da pose parada, nunca geradas do zero
  (senão ele treme). A boca abre rápido e fecha devagar, no ritmo da sílaba
  (~3,3/s) — não em saltos aleatórios.
- **Clonar o motor**: trocar `IMGS`, `VOZOK`, `DOM`/`ROTCRI`/`TREINO`/`CONCD`,
  prefixo dos áudios, `sw.js`, `manifest.json`, `MASCOTE_NOME` e as 3 camadas.
- **Arte nunca se copia de outra atividade** — nem os avatares.
- **Ícone de interface é SVG embutido, nunca desenho de borda.** O alto-falante
  era feito de bordas e filhos `position:absolute`, com left/top em pixel
  repetidos em cada quebra de tela: o Marcos apontou o mesmo botão **três
  vezes** (*"a parte preta tem que estar no meio do círculo. Acho que nem
  precisaria dizer isso"*). Um `background-image:url("data:image/svg+xml,...")`
  se centra sozinho pelo `viewBox`, não tem coordenada para errar e é nítido em
  qualquer zoom. ⚠️ A cor mora dentro do SVG → `background-color` e
  `background-image` **separados**, senão o atalho `background:` de um `:hover`
  apaga o desenho. E **um só glifo para o app inteiro**: dois alto-falantes
  diferentes na mesma tela é amadorismo.
- **Acabamento se confere OLHANDO, em foto ampliada (3×)** — não em
  `getBoundingClientRect`. "Dentro do botão" e "no meio do botão" são coisas
  diferentes, e o número diz que está tudo bem nas duas.
- **Botão novo nasce com `data-qa` no MESMO commit.** Os robôs só tocam no que
  casa com a lista deles; botão que eles não enxergam vira "a peça não chega na
  medalha" — reprovando uma peça que estava certa.

---

## 6. A BANCA (confirma, não descobre)

`bash _qa/auditar.sh <arquivo.html>` — portões 0b padrão, 0c ambíguo, 0d voztela,
0e telavazia, 0f vozpergunta, 0g vozigual, 0h vozintro, 0i vozfalta, 0j vozdica,
1 engenheiro, 1b funções, 1c clone, 1d promessa, 1e imagens, 2 fluxo, 3 classes,
3b progressão, 3c arte própria, 3d mascote, 4 contraste, 4b narração, 5 leiaute
(10 regras), 6 jogador.

⚠️ **Portão que imprime NADA não é "passou": é "rodou cego".**
⚠️ **Defeito que escapou tem conserto em DUAS partes:** arrumar o código E criar
ou estender o portão. Sem a segunda parte o trabalho não está feito.

---

## 7. DE ONDE VEM CADA COISA — o índice por MOMENTO de uso

O que eu já aprendi está espalhado em ~70 documentos, e é por isso que eu
reaprendia sendo corrigido. **Este é o índice: cada pesquisa aparece no passo em
que ela decide alguma coisa.** Ler no momento certo, não "um dia".

| No passo… | Ler | O que ele decide |
|---|---|---|
| **antes de tudo** | `EDUVERSE-FILOSOFIA.md` | Portão 0: nunca prova disfarçada; o problema antes do conceito; o mascote pergunta, não responde |
| **1. currículo** | `_curriculo/blumenau.txt`, `ATIVIDADE-PREMIUM.md` | objetos de conhecimento do ano |
| **2. escada** | `PEDAGOGIA-VYGOTSKY-DINAMICAS-2026-07.md`, `PEDAGOGIA-APRENDIZAGEM-CONCRETA-2026-07.md`, `MODELO-APRENDIZAGEM-EDUCAVERSO.md` | as 6 dinâmicas de aprender-fazendo; escolher pelo OBJETIVO, não pela mecânica; ZDP = o andaime |
| **3. gestos** | `CATALOGO-DINAMICAS-INTERATIVAS.md`, `PESQUISA-CATALOGO-INTERATIVIDADES-2026-07.md` | as 11 famílias; qual encaixa neste conteúdo |
| **4. voz** | `NARRACAO-POR-IDADE-2026-07.md` | **quanto** narrar por faixa: pré–2º = TUDO; 3º–5º = os momentos-chave; 6º–9º = leve. Lei: nada essencial fica só escrito para quem não lê fluente |
| **5. som** | `PESQUISA-SOM-E-GAMEFEEL-2026-07.md` | modalidade de Mayer (narração falada > texto); pitch subindo = quantidade; som de recompensa VARIÁVEL; e o lado escuro — som de fundo que muda de estado atrapalha a leitura |
| **5. encantar** | `PRINCIPIOS-ENCANTAMENTO.md` | os 11 ganchos; o que encanta muda com a idade; a regra da variedade |
| **5. visual** | `PESQUISA-DESIGN-VISUAL-2026-07.md`, `PESQUISA-VISUAL-PROFISSIONAL-RESPONSIVO-2026-07.md`, `PESQUISA-ANIMACAO-APP-PROFISSIONAL-2026-07.md` | hierarquia, ritmo de animação, PC velho |
| **arte** | `EDUCAVERSO-CHECKLIST-DE-CENA.md`, `_padrao/cartela.py`, `PESQUISA-ARTE-NO-MAPA-2026-07.md` | proporção, contexto, cartela |
| **clonar** | `_padrao/CLONAR-MOTOR.md` | os 6 restos de clone que não dão erro nenhum |
| **fim** | `_padrao/FIM-DE-ATIVIDADE.md`, `_padrao/RETOMAR.md` | boletim, relatório, treinar o que faltou, os 55 min |
| **entregar** | `MANUAL-MESTRE.md` §"caminho curto" | `entregar.yml`: uma corrida só |
| **o que já aconteceu** | `MEMORIA-DO-PROJETO.md` | a memória — toda capacidade e decisão nova vai para lá |

### A BIBLIOTECA DE PESQUISA — o que cada bloco já provou

> *"e também tem as pesquisas de ensino-aprendizagem que já realizamos antes,
> estão em documentos, e a pesquisa de neurociência também, juntamente com as
> pesquisas de interatividades"*.

São três blocos, e **cada um responde uma pergunta diferente**. Confundi-los é o
que faz a atividade sair bonita e não ensinar, ou ensinar e ser chata.

**BLOCO 1 — ENSINO-APRENDIZAGEM: *o que faz aprender de verdade?***
`PESQUISA-FORMATOS-APRENDIZAGEM-REAL`, `MODELO-APRENDIZAGEM-EDUCAVERSO`,
`PEDAGOGIA-APRENDIZAGEM-CONCRETA`, `PEDAGOGIA-VYGOTSKY-DINAMICAS`,
`AUDITORIA-APRENDIZAGEM-E-DINAMICAS`.
- O que ensina não é o conteúdo bonito: é o **design da interação e do feedback**.
- **Micro-mundo guiado** (PhET, meta-análise de 31 estudos [FORTE]) — a criança
  mexe e o mundo responde; a concretude vai **desvanecendo**.
- **Prática de recuperação + revisão espaçada** (Roediger, Bjork [FORTE]) — o
  Aquecimento não é enchimento: é o que fixa.
- **Dificuldade desejável** (Bjork) — errar e ser ajudado ensina mais que acertar
  de primeira. É a razão do andaime que cresce.
- **Feedback imediato e específico** (Hattie) — o erro responde na hora e diz o
  que olhar; nunca "errou".
- **Autoria** (generation effect) — a criança CRIAR algo (a legenda, a planta, o
  mapa pintado) vale mais que reconhecer. A auditoria já cobrou: falta autoria
  **persistente** (guardar o que ela fez).

**BLOCO 2 — NEUROCIÊNCIA: *o que traz e o que prende?***
`PESQUISA-APPS-AMAR-E-NEUROCIENCIA`, `PRINCIPIOS-ENCANTAMENTO`,
`PESQUISA-SOM-E-GAMEFEEL`.
- **Beleza e voz TRAZEM; o micro-mundo guiado PRENDE.** Enfeite sem mundo cansa
  em dois dias.
- **Lacuna de curiosidade** (Loewenstein) — o problema antes do conceito: ela
  percebe que não sabe e QUER saber.
- **Malone & Lepper — 4 motores:** desafio, curiosidade, controle, fantasia.
- **Autonomia, competência e vínculo** (Deci & Ryan, N=213 mil [FORTE]) — o que
  prende não é "diversão": é escolher o crachá, ver a barra andar, ter quem torça.
- **Carga cognitiva** (Sweller) + **modalidade** (Mayer, d≈1,02 [FORTE]) — uma
  ideia por tela, e a explicação **falada junto com a figura**, nunca texto ao lado.
- **Recompensa variável** — duas jogadas nunca iguais.

**BLOCO 3 — INTERATIVIDADE: *qual gesto, e como ele responde?***
`CATALOGO-DINAMICAS-INTERATIVAS` (11 famílias),
`PESQUISA-CATALOGO-INTERATIVIDADES`, `PESQUISA-SIMULACOES-EFICAZES`,
`PESQUISA-DIFERENCIAL-E-MECANICAS`, `PESQUISA-ARSENAL-TECNICO`.
- O gesto tem que ser o **movimento natural daquele conteúdo**.
- **Simulação eficaz** = a criança muda UMA coisa e vê a consequência; não é
  animação bonita.
- E as **armadilhas de cada gesto** estão no §4 — que é a destilação prática
  deste bloco, escrita a partir do que já falhou aqui.

**Como usar sem reler 70 arquivos:** o §7 diz QUAL ler em QUE passo. Se a dúvida
é *"isso ensina?"* → bloco 1. *"isso prende?"* → bloco 2. *"que gesto uso e como
ele responde?"* → bloco 3.

### As três coisas destes documentos que eu mais esqueço

1. **Narração por idade** (`NARRACAO-POR-IDADE`): no 3º–5º ano não é "narrar
   tudo" nem "narrar pouco" — é narrar **o problema, a pergunta, o acerto com a
   descoberta e a virada**. Foi por não seguir isto que a primeira pergunta de 27
   fases ficou muda e ninguém percebeu.
2. **Modalidade de Mayer** (`SOM-E-GAMEFEEL`): a explicação vai **falada junto
   com a figura**, nunca como parágrafo ao lado dela. Texto + imagem ao mesmo
   tempo disputa o mesmo canal.
3. **Escolher a dinâmica pelo OBJETIVO** (`VYGOTSKY`): o verbo do currículo manda
   na mecânica. "Elaborar legendas" pede MONTAR, não pede escolher entre três.


---

## 🔤 O QUE A PESQUISA DIZ SOBRE ALFABETIZAÇÃO — destilado (ago/2026)

Cinco pesquisas baixadas pelo `pesquisar.yml` (`_pesquisa/web/`): apps que
funcionam, dinâmicas de "aprender fazendo", letras móveis e caixas sonoras,
jogos que funcionam, e juntar/separar sílabas. O que sobra depois de tirar a
propaganda — e que vira **regra de montagem** para 1º e 2º ano:

**1. A instrução é EXPLÍCITA e SISTEMÁTICA, nunca ao acaso.**
*"Systematic instruction means letters are introduced [in order], rather than
randomly or all at once."* Ou seja: a ordem das letras da atividade é decisão
pedagógica, não sorteio. Letras de traço e som mais fáceis primeiro, e as
parecidas (b/d, p/q) **longe uma da outra**.

**2. Caixas sonoras (Elkonin) são a mecânica com mais evidência.**
Uma caixa por som, e a criança **empurra uma peça para dentro da caixa** ao
dizer o som. É "aprender fazendo" de verdade: o gesto é a própria segmentação.
*"boxes provide a visual representation for each sound in a word and help
students stretch/blend the word"*. → No nosso leque isto é o **`bater-silabas`
feito direito**: cada batida cria uma caixa, e a peça entra nela.

**3. O ARCO DO ALFABETO ensina a sequência melhor que a fila.**
*"Alphabet Arcs support students in visualizing the alphabetical sequence,
recognizing shapes, and building phonics understanding."* A curva dá âncora
espacial (o meio do arco é o M/N) que a linha reta não dá. → o `ordenar` do
alfabeto ganha muito trocando a fileira por um **arco**.

**4. Traçar é MULTISSENSORIAL, e o som vai junto do traço.**
*"Tracing sandpaper letters while saying the sound; skywriting the letter in
the air with large arm motions."* → no `tracar-letra`, o som da letra tem que
tocar **enquanto** o dedo anda, não no fim. E o traço grande vale mais que o
pequeno.

**5. Sessão curta e diária ganha de sessão longa.**
*"Short, daily activities that focus on listening, segmenting, and blending."*
→ 32 fases é o tamanho de uma AULA, não de uma sentada. O "continuar de onde
parou" (55 min) não é conforto: é o que torna a atividade compatível com a
evidência.

**6. Quem está com dificuldade precisa de MAIS gesto, não de mais texto.**
→ o andaime cresce para o concreto (mostrar a figura, acender a caixa da vez),
nunca para uma explicação mais longa.

⚠️ **O que a pesquisa NÃO autoriza:** trocar a mecânica por outra "porque é
nova". Item 1 manda: sistemático. Mecânica nova entra quando o gesto dela É o
conteúdo — não para variar.

---

## 👥 QUEM SENTA NA MESA — a equipe completa (ordens do Marcos, ago/2026)

Palavras dele: *"tem um monte de caminhos a seguir, roteirista, especialista da
área, pedagogo ou da disciplina para verificar e montar a parte pedagógica, eles
devem ser profundos conhecedores da BNCC e currículo de Blumenau"* e *"nas nossas
atividades especialistas web designer, UI/UX, acessibilidade, e tudo que se
precisa para desenvolver nosso app pedagógico"*.

**Nenhuma atividade nasce de uma cabeça só.** Antes de o montador rodar, estes
papéis passam pelo conteúdo — e cada um tem uma pergunta que só ele faz:

| Papel | A pergunta dele | Onde está a resposta |
|---|---|---|
| **Pedagogo / especialista da disciplina** | *isto é o que a professora pediu, na habilidade do ANO certo?* | `_curriculo/blumenau.txt` (o documento oficial, 440 pág.) + BNCC quando o Marcos pedir. Do 1º ao 5º manda o PEDAGOGO; do 6º ao 9º, o ESPECIALISTA DA DISCIPLINA |
| **Roteirista** | *existe um MUNDO que precisa da criança, ou é exercício com moldura?* | `EDUVERSE-FILOSOFIA.md` — o problema vem primeiro, o conceito por último |
| **Game designer / interatividade** | *o gesto é o próprio conteúdo, ou é enfeite?* | `CATALOGO-DINAMICAS-INTERATIVAS.md` + `_padrao/DINAMICAS.md` |
| **Diretor de arte** | *a proporção e o contexto batem com o mascote? é arte de IA, própria desta atividade?* | portões `3c` (arte própria) e `1f` (encaixe) |
| **Web designer / UI** | *tem a cara do Broto — a mesma moldura, o mesmo raio, a mesma sombra?* | `_jardim/index.html` é a referência, e o bloco "O JEITO DO BROTO" no integrador |
| **UX** | *a criança de 6 anos sabe o que fazer sem ninguém explicar?* | uma ideia por tela; alvo grande; o erro responde na hora |
| **Acessibilidade** | *funciona no mudo, no contraste baixo, com o dedo grande e sem saber ler?* | portões `4` (contraste WCAG), `5` (alvo ≥40px), `0n` (toda resposta com voz) |
| **Engenheiro** | *roda no Chrome 109 de 3,5 GB?* | ES5, `-webkit-`, `node --check` |
| **PhD de testes** | *o que escapou desta vez vira portão?* | `_qa/` — a cada defeito, uma regra nova |

⚠️ **O papel que NÃO pode ser pulado é o primeiro.** Mecânica bonita ensinando a
habilidade errada é trabalho perdido inteiro — e é o único erro que os portões
não pegam sozinhos, porque eles medem a execução, não a encomenda.

---

## 📈 PROGRESSÃO É PROGRESSÃO **DIDÁTICA** (correção do Marcos, ago/2026)

Palavras dele, curtas e decisivas: *"quando eu falo em progressão eu falo
progressão didática"*.

**Isto corrige um mal-entendido caro.** A casa tem um portão chamado
`_qa/progressao.py`, e ele mede a **barra de progresso** — se ela anda para trás.
Útil, mas não é disto que ele fala. **Progressão didática é a escada do
CONHECIMENTO**: cada fase só pede o que a anterior já ensinou, e pede um degrau
a mais.

**O que a escada exige, e onde se mede:**

1. **O degrau é pequeno e é UM só.** Entre duas fases muda **uma** coisa: ou o
   conteúdo, ou o gesto — nunca os dois. Fase que muda os dois é fase nova, não
   degrau.
2. **Concreto → figural → simbólico** (Bruner/CPA). A criança primeiro FAZ com a
   figura, depois VÊ representado, e só então lida com o símbolo. Símbolo antes
   do figural é a escada invertida — é o que o `_qa/pedagogo.py` reprova.
3. **O problema antes do conceito.** A criança precisa sentir a falta antes de
   receber o nome (lacuna de curiosidade). Conceito na primeira tela é aula
   expositiva com botão.
4. **O andaime CRESCE.** 1º erro dica · 2º apoio concreto · 3º revela e segue.
   Andaime que repete a mesma dica não é andaime, é eco.
5. **Aquecimento no meio** (revisão espaçada): a fase que retoma o que foi visto
   há dez telas é o que transforma "fez" em "aprendeu".
6. **Nada é cobrado antes de ser ensinado.** Se a fase 7 pede a sílaba complexa,
   alguma fase antes dela ensinou a sílaba complexa — ou a fase 7 está fora de
   lugar.

**Medido por `_qa/pedagogo.py` (portão 0a)**, que é o portão da escada. O
`_qa/progressao.py` (portão 3b) continua existindo e continua útil, mas ele é da
BARRA. Quando o Marcos falar em progressão, é o **0a** que responde.

---

## 📚 O QUE JÁ PESQUISAMOS — o índice, para nunca refazer (ago/2026)

Cobrança do Marcos: *"lembre-se que fizemos pesquisas profundas sobre educação e
os grandes pensadores do passado e atuais e neurociência também, com ênfase em
ensino-aprendizagem"*. Ele está certo — **já está tudo pesquisado**, e eu quase
mandei buscar de novo. Conferido: **8 documentos, 17 pensadores**.

| Onde | O que responde |
|---|---|
| `MODELO-APRENDIZAGEM-EDUCAVERSO.md` | o modelo da casa, de ponta a ponta |
| `PEDAGOGIA-VYGOTSKY-DINAMICAS-2026-07.md` | zona de desenvolvimento próximo → o andaime que cresce |
| `PEDAGOGIA-APRENDIZAGEM-CONCRETA-2026-07.md` | Bruner/CPA → concreto, figural, simbólico |
| `PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md` | o "quero mais": curiosidade, recompensa, atenção |
| `AUDITORIA-APRENDIZAGEM-E-DINAMICAS-2026-07.md` | o que de fato ensina em cada dinâmica |
| `PESQUISA-FORMATOS-APRENDIZAGEM-REAL-2026-07.md` | formatos que produzem aprendizagem, não sensação dela |
| `PESQUISA-DIFERENCIAL-E-MECANICAS-2026-07.md` | o "pensar fora da caixa" com lastro |
| `PRINCIPIOS-ENCANTAMENTO.md` | por que a criança quer voltar |

**Pensadores já destilados:** Mayer, Bruner, Vygotsky, Bjork, Deci & Ryan,
Sweller, Roediger, Piaget, Loewenstein, Hattie, Dewey, Ausubel, Willingham.

⚠️ **Regra:** antes de pedir pesquisa nova, abrir esta tabela. Pesquisa repetida
gasta tempo do Marcos e ainda faz parecer que a casa esqueceu o que sabe.

---

## 🪜 A SEQUÊNCIA DIDÁTICA — a forma da atividade (pesquisa nova, ago/2026)

`_pesquisa/web/sequencia-didatica-e-progressao.md`. Era o que faltava nos 17
pensadores: **Dolz & Schneuwly**, e a estrutura brasileira de sequência
didática. E ela muda o formato da nossa atividade, não só o discurso.

**As quatro etapas, e onde cada uma cai nas nossas 32 fases:**

1. **Apresentação da situação** — o mundo precisa da criança. É a abertura, e já
   fazemos: *"as etiquetas da padaria caíram!"*.
2. **PRODUÇÃO INICIAL** — a criança TENTA antes de ser ensinada. *"as produções
   dos alunos servirão de base para a organização dos módulos e como fonte de
   comparação com a última produção"*. **Isto nos falta**, e é o que dá sentido
   ao resto: sem a tentativa inicial não há o que comparar no fim, e o "Treinar o
   que faltou" adivinha em vez de saber.
3. **Módulos** — as fases que ensinam, uma dificuldade por módulo. É o miolo que
   já temos.
4. **Produção final** — a criança refaz o que tentou na etapa 2, e **vê o
   próprio crescimento**. Hoje o nosso fecho é livre e divertido (o que é certo);
   o que falta é ele RETOMAR a produção inicial.

**A regra que fica, para toda atividade nova:** a fase 2 é uma **tentativa sem
cobrança** do que a atividade inteira vai ensinar — sem dica, sem erro marcado,
só medida em silêncio pelo `reg()`. E a penúltima fase repete aquela mesma
tarefa. O boletim do fim ganha a única comparação que interessa à criança:
**"olha o que você já sabia e o que você sabe agora"**.

⚠️ E o cuidado que a própria pesquisa impõe: produção inicial **não é prova**.
Ela é silenciosa, curta, e o mascote diz que ninguém precisa acertar — senão
vira exatamente o que o `EDUVERSE-FILOSOFIA.md` proíbe.

---

## ❤️ POR QUE A CRIANÇA VOLTA — o que a pesquisa diz, e o que vira código

Pedido do Marcos, repetido três vezes: *"o aluno tem que gostar de fazer, ficar
com o sentimento de QUERO MAIS"*, *"para que eles não sintam que a aula é
chata"*, *"eu preciso que os estudantes amem fazer minhas atividades, que eles
aprendam com elas, que achem legal, não chato e cansativo"*.

Fonte: `_pesquisa/web/engajamento-5a8-anos.md` (75 KB — APA "Top 20 Principles",
UConn KIDS, e estudos sobre curiosidade e mentalidade de crescimento em 5–8
anos), somada ao `PESQUISA-APPS-AMAR-E-NEUROCIENCIA-2026-07.md`.

**O achado central, e ele é incômodo:** *"avoid using external rewards to
indicate a job well done or to motivate behavior"*. Estrela, ponto e prêmio
aleatório **compram** a atenção de hoje e **cobram** a de amanhã — a criança
passa a fazer pela estrela. O que sustenta é **competência + autonomia**:
*"promoting intrinsic motivation requires practices that support children's
fundamental need to feel competent and autonomous"*.

**As cinco coisas que fazem a criança amar, e onde cada uma já vive no motor:**

1. **CURIOSIDADE — a lacuna aberta antes da resposta.** É o previsor número um
   de desempenho nesta faixa, junto com a meta de domínio. → o Portão 0: o
   problema vem primeiro, o conceito por último. Uma tela que começa explicando
   já perdeu.
2. **COMPETÊNCIA VISÍVEL — "eu consigo, e estou melhorando".** Não é nota: é a
   barra andando, o boletim que conta os acertos, o parecer em palavras. →
   `resumoAnimado()`. E é por isso que a **produção inicial** importa: sem ela a
   criança não vê o quanto cresceu.
3. **AUTONOMIA — escolhas de verdade.** Escolher o crachá, escolher o que
   pintar, poder ouvir de novo quantas vezes quiser. Escolha decorativa não
   conta; a criança percebe.
4. **PERSONAGEM QUE SE IMPORTA.** A pesquisa mostra crianças respondendo a
   HISTÓRIAS de personagens que eram ruins numa matéria e melhoraram praticando
   — é assim que a mentalidade de crescimento entra nesta idade: **pela boca do
   mascote**, não por sermão. O Fubá pode dizer *"eu também errava isso"*.
5. **FECHO COM GANCHO.** Termina deixando uma pergunta aberta. É o "quero mais".

**O que NÃO fazer, e que é o caminho fácil:** encher de estrelas, dar prêmio
aleatório, comparar crianças, ranking. Tudo isso funciona uma semana.

⚠️ **E o cansaço, que é o outro pedido dele.** Cansa: a mesma tela pela terceira
vez (por isso nenhum gesto acima de 40%); trocar de assunto a cada tela (por
isso os BLOCOS de objetivo — foi o defeito medido na Padaria, 30 trocas em 32
fases); enunciado longo; e erro que responde "errou" sem dizer onde olhar.
