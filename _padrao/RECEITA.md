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
- **ROTEIRISTA** — cria a HISTÓRIA. A atividade não é uma lista de exercícios com
  tema: é uma viagem com um problema no começo, viradas no meio e um gancho no
  fim. Sem roteirista a atividade vira questionário fantasiado.
- **GAME DESIGNER** — escolhe os gestos pelo encaixe (§2).
- **DIRETOR DE ARTE** — proporção, contexto, coerência; tudo pintado por IA.
- **ENGENHEIRO** — o motor, os portões.

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

Não é a barra de progresso (isso é sintoma). É a escada do aprender:

- **O problema vem primeiro, o conceito por último.** A criança tem que sentir a
  falta antes de receber o nome. Nunca começar explicando.
- **Concreto → figural → simbólico.** Manuseia (a maquete, o voo, o porão do
  navio) → vê a figura → só então encontra o símbolo, a letra, a palavra.
  **Medida:** o primeiro símbolo não pode aparecer antes do primeiro figural.
- **O andaime CRESCE a cada erro:** 1º erro = dica que faz pensar; 2º = consolo +
  apoio concreto; 3º = revela e segue. **Nunca** a mesma dica três vezes.
  - ⚠️ **Em fase sem "errar"** (caça-palavras, exploração, memória) o andaime
    cresce pelo **tempo parado**, não pelo erro. Empacar calado é onde a criança
    desiste, e ninguém vê. 25s → diz o que procurar; 50s → acende o começo.
- **Aquecimento no meio** (revisão espaçada), não no fim.
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

## 3. A VOZ — as cinco regras que já custaram caro

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
- Cada opção com alto-falante.
- Distratores plausíveis, nunca absurdos.
- A dica da barra tem que falar da **tela que está ali** ("de cima você vê o
  telhado" numa tela de mesa e carro não bate).

---

## 5. AS ARMADILHAS QUE NÃO SÃO DE NENHUMA DINÂMICA

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

