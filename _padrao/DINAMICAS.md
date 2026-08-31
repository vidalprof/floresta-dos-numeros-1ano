# 🧰 O LEQUE TREINADO — onde mora a versão que JÁ funciona de cada dinâmica

> 🍽️ **ANTES de montar, escolha a peça pelo CONTEÚDO no `_padrao/CARDAPIO.md`**
> (as 81 por tipo de conteúdo; marca as 44 nunca usadas). Aqui é o detalhe de
> cada uma: referência + armadilhas.
>

> Cobrança do Marcos (ago/2026): *"veja, nós temos um leque de interatividades
> muito grande, precisam ser TREINADAS, para quando for posta em prática não dar
> todos esses erros"* — e, logo depois: *"temos muitas outras: de arrastar,
> sombra, ligar pontos, achar sete erros, completar, forca, e muitas outras que já
> fizemos em outras atividades"*.
>
> **O diagnóstico honesto:** o defeito não é falta de ideia, é **reescrita**. Toda
> vez que eu montava um caça-palavras ou uma fase de arrastar, eu escrevia aquilo
> **do zero** — e repetia um defeito que já tinha sido pago noutra atividade.
>
> **A cura é este arquivo + o portão `_qa/dinamicas.py`.** Aqui está, para cada
> mecânica, **em qual atividade mora a versão mais corrigida** (a que já passou
> pelo Marcos e pela banca). Montar a próxima é **copiar de lá**, não reinventar.
> O portão confere as armadilhas antes de ele ver.
>
> **Levantamento feito medindo o acervo:** 199 fases catalogadas em 9 atividades
> premium (Doceria 25 · Mapa 27 · Fábrica 23 · Naveg 22 · Nomes 22 · Órbi 21 ·
> História 20 · Jardim 17).

---

## 🖐️ O JEITO CERTO DE ARRASTAR — o que a pesquisa ensinou (ago/2026)

> Ordem do Marcos: *"pesquise sites onde elas estão para clonar, aprender"*.
> Fontes lidas: MDN (Pointer Events, `setPointerCapture`, `touch-action`),
> web.dev (mouse e toque) e as casas que fazem o nosso leque há anos — H5P,
> JClic, LearningApps. Texto em `_pesquisa/web/o-jeito-certo-de-arrastar-*.md`.

**O que estávamos fazendo:** dois mundos separados — `mousedown/mousemove/mouseup`
de um lado, `touchstart/touchmove/touchend` do outro — mais uma guarda de relógio
(`ultimoToque`) contra o clique fantasma. Funciona, mas é o dobro de código e foi
onde o defeito escapou **duas vezes**.

**O que a fonte ensina, e vira regra da casa:**

1. **Um caminho só: `pointerdown` / `pointermove` / `pointerup`.** Cobre mouse,
   dedo e caneta com o mesmo código. Chrome 109 (o PC da escola) tem.
2. **`elemento.setPointerCapture(ev.pointerId)`** no `pointerdown`. A peça
   continua recebendo os eventos mesmo quando o dedo sai de cima dela — cura o
   "a peça para de seguir o dedo" sem escutar o documento inteiro.
3. **`touch-action:none` no CSS da peça** é o jeito certo de impedir que a tela
   role enquanto a criança arrasta. Substitui o `preventDefault` no `touchmove`
   (e continua **proibido** no `touchstart`, que mata o toque simples).
4. ⚠️ **A GUARDA DO CLIQUE FANTASMA CONTINUA NECESSÁRIA.** Eu ia jogá-la fora, e
   a própria MDN me corrigiu: cancelar o `pointerdown` evita os eventos de mouse
   de compatibilidade, **mas o `click` nunca é evitado** — *"click events are
   never prevented (even if the pointer is down)"*. Ou seja: sem a guarda, o
   toque simples dispararia duas vezes. Foi a pesquisa que impediu o meu
   conserto de virar defeito novo.
5. **Alvo grande o bastante para um dedo** — a MDN diz isso com todas as letras,
   e é a mesma régua do nosso `_qa/leiaute.js` (≥40px).

**Onde as dinâmicas moram, para ver funcionando:** H5P (`h5p.org` — arrastar e
soltar, memória, caça-palavras, cruzadinha), JClic (`clic.xtec.cat`, aberto desde
1992) e LearningApps. São as três casas que fazem exatamente o nosso leque, e
servem de referência de COMPORTAMENTO — não de código para copiar (o nosso motor
é outro, e a arte é nossa).

## 👀 PASSO ZERO: VER A DINÂMICA FUNCIONANDO — `python3 _padrao/ver_fonte.py <mecanica>`

> Pergunta do Marcos (ago/2026), e ela apontou o buraco exato: *"foi feita a
> pesquisa das dinâmicas, mas nessas pesquisas dizem como programar? você
> verifica ela funcionando da fonte que você buscou para clonar igual?
> Interessante seria você ver ela funcionando e copiar igual, isso iria
> economizar tempo com menos erros"*.

**A resposta honesta era NÃO — e ele acertou o ponto.** As pesquisas dizem o que
a mecânica ENSINA e o que observar na criança; **não dizem como programar**. Quem
diz onde está o código bom é esta tabela. Só que, na hora de usar, eu abria o
arquivo, **lia** a função e **reescrevia adaptando** — e é na adaptação que o
defeito nasce: some uma linha de guarda, troca-se um nome de classe, esquece-se a
terceira porta do toque.

Agora o passo zero é um comando:

```
python3 _padrao/ver_fonte.py arrastar
```

Ele (1) descobre nesta tabela onde mora a versão boa; (2) **abre aquela fase no
navegador e joga nela**, salvando as fotos em `_padrao/_fonte/<mecanica>/`;
(3) lista os ajudantes que a fase chama, para não sobrar chamada órfã; e
(4) imprime a **função inteira, pronta para copiar**.

⚠️ **Copiar é COPIAR.** Trocar só os dados e os ids de voz. E a conferência que
fecha: **se a função nova ficar menor que a de origem, alguma guarda se perdeu no
caminho** — e guarda perdida é defeito na mão da criança. (Na estreia: o arrastar
da Oficina saiu com 94 linhas contra 131 do `_mapa`; fui conferir uma a uma as
três portas, o `preventDefault` e o mouse fantasma antes de seguir.)

## COMO USAR (o passo que evita 90% do retrabalho)

1. Escolhi a mecânica no roteiro → **abro a coluna "onde está a boa"** e copio
   daquela atividade: o CSS, a função da fase e os ajudantes que ela usa.
2. Troco **só o conteúdo** (as palavras, as figuras, os ids de voz com o prefixo
   novo). ⚠️ Ver `_padrao/CLONAR-MOTOR.md`: o que mais escapa é conteúdo da
   origem que **não dá erro nenhum**.
3. Rodo `python3 _qa/dinamicas.py <arquivo>` — ele confere as armadilhas **daquela**
   mecânica.
4. Rodo a banca inteira (`bash _qa/auditar.sh`).

---

## A TABELA

| Mecânica | Onde está a boa (copiar daqui) | O que ela ensina bem | Armadilhas — cada uma já custou caro |
|---|---|---|---|
| **Caça-palavras** | `_naveg` "CAÇA-PALAVRAS DO MAR" · `_mapa` | reconhecer a forma escrita de um termo novo; alívio entre fases pesadas | célula em **`(100/N)%` + `box-sizing:border-box`** (com px fixo cabem 10 numa grade de 9 → *"TROCA e o A em outra linha"*); **diagonal só se o enunciado avisar**; célula conquistada **trava**; conferir `mark` **OU** `ok` (palavra que cruza outra nunca fechava); publicar `data-qa` senão o auditor dá "PRESO" |
| **Cruzadinha** | `_mapa` · `_naveg` | definição → palavra: recuperar o termo pelo sentido | teclado na tela **e** `document.onkeydown`; a voz de cada dica tem que existir (`_qa/vozfalta`) — foi aqui que 3 fases ficaram MUDAS; alvo ≥ 40px |
| **Forca** | `_mapa` · `_naveg` | onde a PALAVRA é o conteúdo | palavra a adivinhar **sem acento** (o teclado não tem), a da faixa **com** (`ac:"BÚSSOLA"`); letra usada **sai do alcance**; comemorar ao fechar |
| **Memória** | `_mapa` (carta grande, verso de arte, virada 3D) | par **conceitual** (causa↔efeito, palavra↔imagem) | carta fluida **≥ 130×88px**; verso de **arte de IA**, nunca retângulo liso; `rotateY` com queda para troca-de-face no Chrome 109; em tela baixa encolhe a LETRA, nunca a carta; som de virar e de par; **a arte de IA vai no campo `img`** (o motor lê pelo `imgEl`) — o `fig` do exemplo é só o desenho EMBUTIDO da peça; trocar um pelo outro deixa a carta mostrando **"undefined"** (pago no RIGHT NOW, ago/2026) |
| **Arrastar** | `_mapa` "MONTE A LEGENDA" (`arrasta(b,k)`) | pôr no lugar É o conceito espacial | **três caminhos: mouse, dedo, toque simples**; **nunca** `preventDefault` no `touchstart`; guarda contra o **mouse fantasma** que o celular dispara depois do toque. Pego **DUAS vezes** |
| **Sombra / ache o par** | `_mapa` "ACHE O PAR" | forma e silhueta: olhar o contorno, não a cor | a silhueta tem que ser **da MESMA figura** (recorte da própria arte), senão a criança compara coisas diferentes; par que acerta **acende e pulsa** |
| **Ligar colunas** | `_naveg` "PARA QUE SERVIA?" · `_jardim` "PARA QUE SERVE" | relação 1-a-1 explícita | alto-falante nos **dois** lados; a linha precisa de `touchmove`; nunca mais que ~6 pares (vira memória disfarçada) |
| **Ordenar / linha do tempo** | `_historia` "LINHA DO TEMPO" · `_detetive` (linha-do-tempo, jul/2026) · `_jardim` "telaOrdenar" | seriação e etapas **com a justificativa** | três caminhos de arrasto; **conteúdo conferido por especialista** — o portão não pega data histórica errada; faixa que rola precisa de `overflow-x` próprio; **a tela de fim TEM que se chamar `fimDaPeca`** (não `telaFimLinha`) — senão o integrador não a reaponta para a próxima fase e a criança cai num BECO com "PEÇA FECHADA" (pago no Detetive, ago/2026; `_qa/beco.py` pega) |
| **Classificar em gavetas** | `_naveg` "VEIO OU JÁ ESTAVA?" | formar categoria por atributo definidor | enunciado sem termo que ela não conhece (*"veio de lá"* → **"veio de fora"**); as gavetas se **refazem** quando o eixo muda; a explicação espera o áudio (`depoisDaFala`, nunca `setTimeout` fixo) |
| **Achar na cena / lupa** | `_mapa` "O BAIRRO LÁ DE CIMA" (`naZona`, grade 48×48) | observação dirigida: ler a paisagem | zona = a **FIGURA recortada por pixel**, nunca um pontinho com raio; alvo no pixel **mais longe da borda** (`distance_transform_edt`), nunca no centroide; achou = **V verde**; singular só se houver UMA |
| **Pintar / marca-texto** | `_mapa` "PINTE O MAPA" (camadas medidas por pixel) · `_naveg` "A LÍNGUA GUARDA" | mapear categoria sobre o real — o traço É a classificação | a figura é **arte de IA**, o CSS anima só o que se mexe; o mapa começa **sem cor**; no texto: traço correndo + som de risco + barra + carimbo |
| **Simulador / deslizar** | `_historia` "A ÁGUA SOBE" (o que ele mais elogiou) · `_naveg` "O SEGREDO DO VENTO" | causa-efeito e controle de variáveis | o mundo reage **de verdade** (foto que gira não é simulador); ponto **medido na figura**, não a olho; a figura é gerada, o CSS anima. ⚠️ **No motor ESQUELETO o `mec="simulador"` É A CHUVA/RIO/PONTE hardcoded** — ignora o conteúdo da fase e mostra a cena de água. Só usar em tema de ÁGUA; fora disso é resto de clone (print bonito, defeito só jogando). O `_qa/dinamicas.py` reprova simulador sem palavra de água no enunciado. Sólidos 2º ano usou `ligar`/`quem-sou-eu` no lugar |
| **Completar lacuna** | `_naveg` "COMPLETE A HISTÓRIA" | produção mínima com apoio da frase | a voz diz **exatamente** o texto escrito; em fase embaralhada o id da voz vem do **ITEM**, nunca do contador da rodada; figura sem fundo branco aparecendo |
| **Montar a palavra** | `_jardim` "telaMontaPalavra" | soletrar: qual letra vem primeiro | as duas portas (tela + teclado real); ⚠️ o `setTimeout` da rodada continua correndo depois do `limpa()` e reinstala o `onkeydown` **por cima da fase seguinte** — guardar `if(!t.parentNode) return;` |
| **Escolher / quiz** | qualquer uma — mas **≤ 2 telas em 20** | aferir rápido um fato já ensinado | **embaralhar as opções** (na Fábrica de Estrelas a certa era sempre a 1ª); alto-falante em CADA opção; distratores plausíveis; a dica fala da tela que está ali |
| **Relâmpago** | `_mapa` · `_naveg` | evocação rápida do que já foi visto | **não exigir andaime aqui** — dica no meio acaba com o que a fase treina (é velocidade). Está na lista `SEM_ERRO` do `_qa/pedagogo.py` |
| **Ensinar o mascote** | `_naveg` "ENSINE O ARÁ" | metacognição: a regra que ela ensina É o modelo mental | o mascote **erra visível** com a regra ensinada, senão vira quiz fantasiado; enunciado que muda por rodada exige voz por rodada |
| **Rota animada no mapa** | `_naveg` "A ROTA DA VIAGEM" (`ROTAP`, o navio andando) | trajeto e ordem no espaço | os pontos são **medidos na imagem**, não estimados (navio ancorando no continente errado estraga a fase) |
| **Quebra-cabeça** | `_mapa` "O MAPA EM PEDAÇOS" | parte-todo e orientação | peça na **proporção certa** da imagem (0,91 e não 1,0); mira na vaga; som de pegar, de encaixar e de fechar |
| **Coordenadas / bússola** | `_mapa` "ACHE PELA COORDENADA" e "A ROSA DOS VENTOS" | par ordenado e orientação | as coordenadas têm que **bater com a figura** (medir, não estimar — ele pegou isso); célula ≥ 40px; referência explícita ("o lado da sua direita") |

---

## ⭐⭐ MODO: A MESMA PEÇA COM OUTRO GESTO (lição do EdiLIM, ago/2026)

`_pesquisa/EDILIM-DINAMICAS.md`, seção *"melhorar as nossas olhando as delas"*.
O EdiLIM tira **"mais de 50 atividades" de ~40 páginas** porque quase toda página
dele tem **MODOS** — a *Etiquetas* tem seis; o *Reloj*, dois. As nossas 78 peças
sabiam fazer **uma coisa cada**.

**Por que isto vale mais que peça nova:** modo mexe direto no número que o
`_qa/padrao.py` mede (nenhum gesto acima de 40%). Uma atividade que usa `rotular`
três vezes era, para a criança, *a mesma tela pela terceira vez*; com modo, a
segunda é escrever e a terceira é passar por cima — e ela não se cansa.

| peça | modos hoje | o campo |
|---|---|---|
| **rotular** | `arrastar` (padrão) · `escrever` · `mostrar` · `hover` | `var MODO` no topo, ou `modo:` dentro da rodada (a rodada manda mais) |
| **relogio** | `ponteiros` (padrão) · `escrever` | `var MODO` no topo; o `ROT` aceita `"e"` para misturar os gestos na mão |

**As três regras que o modo trouxe, e que valem para toda peça que ganhar modo:**
1. **O padrão é o comportamento de hoje.** Nenhuma atividade antiga pode mudar de
   comportamento por causa de um campo novo.
2. **Modo é GESTO, não rótulo.** Se as duas telas são a mesma coisa com outro
   nome, não é modo — é enfeite, e a criança percebe antes de nós.
3. **Modo novo nasce com o portão que o mede** (`_qa/dinamicas.py`, bloco
   "modos"), e com a receita do errador (`_qa/errador.js`) quando o modo tem erro
   a cometer. Sem isso o modo é caminho que ninguém confere — que é exatamente
   como nasceram os defeitos que chegaram ao Marcos. *(Medido: o modo `escrever`
   da `rotular` saiu do primeiro teste com o portão do andaime CEGO; com receita
   própria ele passou a ver os três degraus crescendo.)*

⚠️ **Modo sem erro possível** (o `mostrar` da `rotular`) faz o portão do andaime
sair com **"não medi"**, e isso está **certo**: ali não há erro para o andaime
socorrer. O que não pode existir nesse modo é **silêncio** — tocar de novo num
ponto já visto tem que responder.

---

## O QUE AINDA NÃO TEMOS (do catálogo de pesquisa)

Está em `_pesquisa/REGRAS-INTERATIVIDADE.md`, bloco (B), com 32 mecânicas em ordem
de custo. As três que eu recomendaria para a próxima, e **só se encaixarem no
conteúdo**:

1. **Conserte o erro** — a resposta vem **já feita com um erro plantado** e a
   criança acha. É o motor de "achar na cena" com o conteúdo invertido: quase de
   graça.
2. **Mapa conceitual** — arrastar conceitos e **traçar setas com nome**. A
   evidência mais forte de todas as mecânicas novas; serve a qualquer disciplina.
3. **Mistério guiado** — pistas que aproximam e erro que **dá mais pista**. É o
   formato que mais responde ao "quero mais".

⚠️ **Nenhuma delas pode deixar a atividade mais difícil.** Regra do Marcos: *"não
podemos fazer muito difícil, a criança tem que conseguir passar"*.

---

## O PORTÃO QUE CONFERE ISTO SOZINHO

`python3 _qa/dinamicas.py <arquivo.html>` (portão 0b2 da banca) reconhece a
mecânica pelo código e cobra as armadilhas **dela**. Na estreia ele já achou, no
acervo: Doceria e Fábrica com teclado na tela **sem** teclado de verdade; Gêneros
com opções **não embaralhadas**; três atividades com memória **sem virada 3D**;
duas com célula de caça-palavras em px fixo; e quase todas **sem o guarda do toque
fantasma**.

**Regra da casa:** mecânica nova = **linha nova neste arquivo e regra nova no
portão, no mesmo commit.** Sem isso, o defeito volta na próxima atividade — que é
exatamente o que ele está cobrando.

---

## 🧰 AS PEÇAS PRONTAS — copie DAQUI, não da atividade

A partir de ago/2026 a versão de referência de cada mecânica **não é mais a que
está dentro de uma atividade**: é a **peça isolada**, em `_padrao/pecas/`. A
diferença importa — dentro da atividade a mecânica vem misturada com o conteúdo
dela (as imagens, as vozes, os conceitos), e era daí que saíam os restos de clone.
A peça vem limpa e **já aprovada nos 8 portões da bancada**
(`bash _qa/peca.sh <arquivo>`), incluindo o jogador automático que joga sozinho
até a medalha.

**Peças no catálogo hoje:** `achar-na-cena`, `andar-ate`, `arrastar-lugar`, `arrastar-sombra`, `autoexplicacao`, `balanca`, `base-dez`, `bater-silabas`, `bingo`, `bussola`, `caca-palavras`, `caixa-dinheiro`, `caixas-de-som`, `calendario`, `camadas-mapa`, `circuito`, `classificar`, `comparar`, `completar`, `conserte-o-erro`, `contadores`, `coordenadas`, `criar-desafio`, `cruzadinha`, `decisao`, `digitar`, `ditado`, `domino`, `ensinar-mascote`, `escolher`, `escrever-legenda`, `estimar`, `experimento-justo`, `filtro`, `forca`, `girar`, `grafico`, `intruso`, `investigar-fonte`, `juntar-silabas`, `labirinto`, `letras-escondidas`, `ligar`, `ligar-pontos`, `linha-do-tempo`, `mapa-conceitual`, `medir`, `memoria`, `misterio`, `montar-frase`, `morfemas`, `mudanca-permanencia`, `ordenar`, `ouvir-achar`, `padrao`, `passo-a-passo`, `pintar`, `pintar-canvas`, `pintar-desenho`, `prever-observar`, `quebra-cabeca`, `quem-sou-eu`, `raios-x`, `relampago`, `relogio`, `repartir`, `reta-numerica`, `rima`, `rotular`, `saltos-na-fita`, `sete-erros`, `simetria`, `simulador`, `som-inicial`, `sombra`, `tabela`, `tangram`, `teia-alimentar`, `termometro`, `tracar-caminho`, `tracar-letra`, `trilha`, `vitrine`

⚠️ **Cada peça tem no cabeçalho o bloco de dados a trocar.** Copiar = trocar o
conteúdo, nunca reescrever a mecânica.

### O que as peças ensinaram (e portão nenhum pegaria)

- **O erro encenado não pode sumir.** No "ensinar o mascote", a cena era limpa
  logo depois do erro: o boneco voltava para o canto e o que ela ensinou
  desaparecia — a criança lia "continua murcha" olhando uma cena vazia, e a fase
  virava **quiz fantasiado**. A limpeza passou para o COMEÇO da tentativa
  seguinte, para o erro ficar de pé enquanto ela olha.
- **Cada regra errada precisa do SEU resto.** Um monte de areia servindo para
  "cubro com um pano" denuncia que o mundo não está reagindo de verdade.
- **Ficha usada: `display:none`, não `visibility:hidden`.** O retângulo invisível
  continua ocupando lugar (buraco no banco) e ainda é medido pelo portão como
  "resposta fora da tela".
- **Escalar a cena inteira** (`transform:scale`) em vez de reposicionar peça por
  peça em cada `@media` — 12 regras que precisam concordar é 12 chances de errar.
- **A tela de fim tem que mostrar o estado REAL** (inclusive "ninguém
  respondeu"), senão ela vem vazia e nunca é medida.

---

## AS VINTE QUE FALTAVAM NO CATÁLOGO (ago/2026)

A varredura das 74 peças mostrou que **20 mecânicas existiam na oficina e não
estavam escritas aqui**. Isso é exatamente o defeito que este arquivo existe para
impedir: mecânica que não está no catálogo é mecânica que eu reescrevo do zero na
próxima atividade — e reescrever é reintroduzir o que ela já custou.

*Onde mora a versão mais corrigida: `_padrao/pecas/<nome>.html`, todas com a
bancada em código 0.*

### Para PRÉ e 1º ano (a criança não lê: alvo de 56px, uma linha, nada essencial escrito)

| mecânica | o gesto que ela ensina | a armadilha dela |
|---|---|---|
| **arrastar-sombra** | levar o objeto até a silhueta — o par se faz pela FORMA | não confundir com `sombra`: lá se casa por TOQUE, aqui o gesto é ARRASTAR, e o gesto é conteúdo. ⭐ A FORMA aceita `img` (arte de IA): então a silhueta é a PRÓPRIA figura em `brightness(0)`, nunca um clip-path chapado — use `img` sempre que a atividade já tem a arte (regra do Marcos, ago/2026, Cidade dos Sólidos). Sem `img`/`imgEl` cai no clip-path (peça solta, atividades antigas) |
| **labirinto** | levar o personagem ao que ele precisa desviando dos inimigos | encostar no inimigo **não é castigo**: volta ao começo do trecho e segue. Sem vida, sem fim de jogo. E as SETAS DO TECLADO, não só o botão |
| **ligar-pontos** | a sequência numérica vira gesto: achar o 5 *depois* do 4 numa bagunça | tocar no ponto errado não pune — só não liga |
| **pintar-desenho** | a única em que a criança **produz** em vez de responder | **não tem certo nem errado**: nenhum som de tropeço, nenhuma marca de recusa. O peixe pode ser roxo. O que se mede é AUTORIA |
| **pintar-canvas** | o pintar do **Circo do Teo**: balde de tinta em **canvas** sobre uma IMAGEM de contorno (`img/<img>.png`), flood-fill parando nas linhas pretas | também **não tem certo nem errado**. A figura é ARTE DE IA (não vetor). ⚠️ a `.tela` tem que ROLAR por dentro (`overflow-y:auto`) — na tela baixa o canvas+paleta+botões não cabem e o portão leiaute só aceita a dobra se a própria tela rolar. Reserva `img:""` desenha um contorno no ctx para a bancada |
| **ouvir-achar** | o enunciado chega pelo ouvido, a resposta é uma FIGURA | a palavra tem que estar ESCRITA junto: PC de escola sem caixa de som existe, e criança surda também |
| **tracar-letra** | refazer o movimento da letra, sempre no mesmo sentido | sair da linha **não pune** — som de retorno, nunca de tropeço; o dedo da criança treme. E conferir por POSIÇÃO, não por identidade do elemento |
| **andar-ate** | dizer o caminho passo a passo — o começo do pensamento computacional | um comando = uma casa, e o boneco **anda** até lá (a transição é o que ensina) |
| **juntar-silabas** | **síntese**: BO + LO = BOLO. Os pedaços **deslizam** um até o outro e viram um só — é a corrida que ensina, não o encaixe | a palavra fecha dita **de uma vez**, nunca "BO… LO" (*Connected Phonation Is More Effective than Segmented Phonation*, Reading Rockets); a bandeja vai **embaralhada**, senão ela aprende a POSIÇÃO; erro devolve o pedaço com som de RETORNO; as **três portas** — clique, dedo e **arrasto** (aqui o arrasto **é** o conceito) |
| **caixas-de-som** | **o SOM isolado**: uma caixinha por som, e ela empurra uma ficha para cada um, dizendo a palavra devagar. É o degrau que a sílaba não alcança — e o preditor mais forte de leitura no 1º ano | a **letra não pode aparecer durante o preenchimento**: viraria ditado, que é outra coisa e vem depois. Primeiro o som; a letra só no fim, dentro das caixas. E `letras` **não é uma por caixa** — o "CH" de CHÁ é UM som e DUAS letras, e é isso que a peça mostra: por isso ela não pode ser feita contando letras |
| **rima** (ago/2026) | **o par por SOM do fim**: um tabuleiro de cartas viradas para cima; a criança toca em duas que **rimam** (PATO–GATO). Degrau **onset-rime** da escada fonológica — habilidade própria, o 3º tema mais pedido nas pesquisas (33 menções) e o gap que o nosso leque tinha | o par é por SOM, **nunca por posição** → tabuleiro **embaralhado** (`baguncar`); **alto-falante em toda carta** (classe `.ptxt`), a rima é do ouvido; erro não pune e o **andaime cresce** (escute o fim → o par pisca → o par acende); **duas portas** (toque e mouse) + guarda do clique fantasma; os dois lados do par publicam a **mesma `data-qa`** (o auditor fecha a fase). Portão: `_qa/dinamicas.py` (regra "rima") |
| **som-inicial** (ago/2026) | **a casa do som do começo**: casas rotuladas pela letra (M, S…), uma esteira de palavras; a criança manda cada palavra para a casa do som com que ela **começa** (MALA→M, SAPO→S). É onde a criança trava para decodificar; agrupar por som inicial é de alto valor (pesquisa ago/2026) | agrupar por **SOM**, não por categoria de sentido (isso é `classificar`); cartas **embaralhadas** (`baguncar`); **alto-falante** em carta e casa (`.ptxt`), a casa fala **o SOM** ("o som M"), nunca o nome da letra ("ême"); a carta vem **sem a letra inicial destacada** (entregaria a resposta sem ouvir); **1ª rodada por som contínuo** (M, S, F…); erro não pune, **andaime cresce** (escute o começo → a casa acende → revela); carta e casa publicam a **mesma `data-qa`**. Portão: `_qa/dinamicas.py` (regra "som inicial") |
| **bater-silabas** | **análise**, a outra metade: BOLO = BO + LO. A criança **bate uma vez por pedaço** (palma / mão no queixo) | **não desenhar os lugares prontos** — com 3 casinhas na tela ela conta as casinhas, não a palavra, e a resposta está dada; tem que dar para **Apagar** (contar errado no meio não prende); 2º degrau do andaime é pelo **OUVIDO** (a peça bate junto), só o 3º escreve; **barra de espaço** bate e **Enter** responde (as duas portas); ⚠️ **CADEADO DE RE-ENTRADA** (`travando`): a comemoração do acerto dura segundos (uma sílaba por vez) e a criança impaciente toca **Pronto de novo** — sem o cadeado, `confere`/`acerta` roda 2× e a peça **trava** (Marcos pegou no ELEFANTE, a palavra mais longa = a maior janela). O gate `_qa/dinamicas.py` exige o `travando`. |

### Números e medida

| mecânica | o gesto | a armadilha |
|---|---|---|
| **base-dez** | a criança **enche** a caixa e é ela quem manda trocar 10 por 1 | o conceito mora na TROCA, e a troca tem que ser VISÍVEL |
| **comparar** | as duas quantidades lado a lado **antes** do símbolo | inverter essa ordem é o que faz decorar "a boca do jacaré" |
| **digitar-numero** (ago/2026) | motor ESQUELETO `_padrao/ESQUELETO/pecas.js` (`MEC["digitar-numero"]`) — a versão de estreia | **calcular e DIGITAR o resultado num teclado numérico, COM SUPORTE VISUAL** (pedido do Marcos: "digitar resultado com suporte visual"): as frutas da conta desenhadas para a criança contar (concreto → figural → simbólico). Config: `{a,b,op:"+"|"-",img:"fe_maca",resp,dic}`. Armadilhas: (1) a fruta é **arte de IA** (`figEl`/`img`), NUNCA desenho de CSS — na subtração as ÚLTIMAS `b` saem **riscadas** (modelo "tirar"); sem `figEl` cai numa ficha neutra só na bancada; (2) **as duas portas** — teclado numérico 0-9 na tela (alvo ≥48px) **e** `document.onkeydown` (dígitos + Backspace); (3) cada tecla **fala o número** por extenso ao ser tocada (`NOMEDIG`+`diz`) e o alto-falante diz a conta ("três mais dois") — quem ainda não lê o algarismo; (4) tremor/pisca **sem `@keyframes`** (duas classes + `setTimeout`, senão o integrador os perde); (5) andaime cresce (dica → frutas piscam/conte → revela e segue), **nunca "errou"**; (6) o auditor-jogador bate dígito a dígito pela `.numtecs[data-qa]`+`.dnvagas .vaga.cheia`. Portão: `_qa/dinamicas.py` (regra "digitar-numero") |
| **calendario** | "faltam quantos dias?" é um CAMINHO, não uma subtração | um pulo de cada vez, animado — é o pulo que ensina, não a conta |
| **relogio** | a criança **move os ponteiros** (pedido do professor, com todas as letras) — e tem **2 MODOS**: `"ponteiros"` (padrão) e `"escrever"`, em que ela lê o relógio e digita a hora | os dois ponteiros não podem começar sobrepostos: ela não descobre que há dois para mexer. No modo `escrever`, a leitura em números embaixo do relógio tem que ficar DESLIGADA — ela diria a resposta antes da pergunta |
| **bingo** | reconhecer sob pressão gostosa — prática de recuperação disfarçada | **não há relógio**: a pressão é da pedra que saiu, não do tempo |
| **trilha** | o acaso escolhe a pergunta, o que tira o peso do julgamento | o dado não pode mostrar face antes do primeiro lance, e a peça do jogador não tapa a palavra da casa |

### Raciocínio e leitura de mundo

| mecânica | o gesto | a armadilha |
|---|---|---|
| **intruso** | achar o que não pertence **e dizer por quê** | sem o segundo passo isto é um quiz: ela acerta por eliminação sem formular o critério. O "por quê" é TOCADO, nunca digitado |
| **quem-sou-eu** | eliminar candidatos com um atributo por vez | a informação chega em DOSES; a 1ª pista serve para pensar, não para acertar |
| **domino** | comparar duas pontas com quatro peças — a FORMA corrige, não o adulto | a peça só entra se a ponta bater; "combinar" não pode ser sinônimo de "ser igual" | ⚠️ `semente` é ÍNDICE do par (0..cadeia.length-2); FORA da faixa some a fase inteira em branco (`undefined.a`) — a peça agora GRAMPEIA o índice, mas o dado tem que ser válido.
| **passo-a-passo** | o mundo **executa** a sequência dela, na frente dela | **não é ordenar**: ninguém confere nada. Se ela mandou regar antes de plantar, a água cai na terra seca — e é isso que ensina |
| **circuito** | ligar os fios e a lâmpada **acende de verdade** | traço decorativo perde o efeito inteiro: cada fio ligado tem que mudar o mundo |
| **camadas-mapa** | ligar/desligar camadas e ver o que só aparece na sobreposição | a resposta não está escrita em lugar nenhum da tela — se estiver, virou quiz com figura |
| **rotular** | levar o nome ao lugar **espacial** dele na figura — e tem **4 MODOS**: `"arrastar"` (padrão), `"escrever"` (digita o nome do ponto aceso), `"mostrar"` (sem resposta certa: toca e o ponto CONTA o que é) e `"hover"` (o nome aparece e é falado ao passar o mouse) | não é classificar: lá o lugar é uma gaveta (categoria), aqui é ONDE na figura. No `hover`, o TOQUE tem que fazer o mesmo que o mouse — no celular não existe passar por cima, e sem isso a fase fica inacessível no telefone |

## 🔊 A PEÇA QUE FALTAVA — CAIXAS DE SOM (Elkonin), ago/2026

Nasceu de uma pergunta do Marcos: *"essas eram as melhores dinâmicas para essa
atividade?"*. Fui medir e achei o buraco: **A Padaria das Letras parava na
sílaba**. Bater sílabas, juntar sílabas, som do começo — e nenhuma fase de som
**isolado**. Só que a consciência **fonêmica** é o preditor mais forte de
leitura no 1º ano; a silábica vem antes e sozinha não abre a leitura. A oficina
não tinha a mecânica: a atividade não tinha como chegar lá nem que quisesse.

| peça | o gesto | a armadilha que ela fecha |
|---|---|---|
| **caixas-de-som** | uma caixinha por SOM; a criança diz a palavra devagar e **empurra uma ficha** para cada som | **a letra não pode aparecer durante o preenchimento** — isso viraria ditado, que é outra coisa e vem depois. Primeiro o som; a letra só no fim |

**O que ela ensina, nesta ordem** (é o coração da peça):
1. diz a palavra devagar e empurra **uma ficha por som**;
2. as caixas enchem da **esquerda para a direita** — som tem ordem, e é a mesma
   ordem da escrita: é aqui que nasce a direcionalidade;
3. **só depois** de fechar a palavra as letras aparecem dentro das caixas.

**Duas coisas que fazem diferença e não são óbvias:**
- **`letras` não é uma por caixa.** O "CH" de CHÁ é **um som e duas letras** —
  é justamente isso que a peça mostra no fim, e é por isso que ela **não pode
  ser feita contando letras**.
- **Tocar a caixa já empurra a próxima ficha.** No 1º ano, exigir dois toques
  onde um basta é atrito puro. Quem gosta de escolher a ficha primeiro
  continua podendo — e dá para arrastar.

**Medida na bancada:** código 0 nos 9 portões, com o errador medindo o andaime
(3 dicas distintas e crescentes, chega à medalha depois de errar).

### ⭐ REGRA DE OURO DAS FONOLÓGICAS: SOM CONTÍNUO ANTES DE SOM DE PARADA
Pesquisa profunda (ago/2026, `_pesquisa/web/como-fazer-fonologica-rima.md`): sons
que **se esticam** — /m/, /s/, /f/, /v/, /n/, /l/, /r/, /z/ — são muito mais
fáceis de **juntar e segmentar** do que os sons de **parada** — /b/, /p/, /t/,
/d/, /k/, /g/ (que não dá para "segurar" sem virar "bê", "tê"). Então, em
`caixas-de-som`, `juntar-silabas`, `bater-silabas` e `rima`, a
**primeira rodada começa por palavras de som contínuo** (ex.: MEL, SOL, FADA,
LUA, RÃ) e só depois entram as de parada (BOLA, PATO, GATO). Começar por som de
parada é pôr o degrau mais difícil primeiro — a criança trava logo na entrada.
Vale também: a escada da consciência fonológica é **frase → palavra → sílaba →
onset-rime (RIMA) → fonema**; não pular etapa.

---

## 🔤🕳️ A PEÇA QUE VEIO DO EDILIM — LETRAS ESCONDIDAS (ago/2026)

Nasceu do pedido do Marcos: *"faça uma pesquisa profunda nas dinâmicas do
Edilim"*. O manual oficial (páginas *Ortografía* e *Letras*) faz uma coisa que a
casa não tinha: a palavra aparece com letra faltando (`C_AS_A`, `_barco`), com
figura e com som, e a criança **arrasta a letra até o buraco** — podendo haver
**letras a mais** na bandeja, que não servem para nada. Ver
`_pesquisa/EDILIM-DINAMICAS.md`, achada nº 2.

| mecânica | o gesto | a armadilha que ela fecha |
|---|---|---|
| **raios-x** | levar uma JANELA pela figura e descobrir o que está por baixo | nesta mecânica **não existe errar** — o andaime cresce pela **olhada perdida** (3 pontos vazios) e pelo **tempo parado** (7s), nunca por resposta errada; e o brilho da 2ª ajuda **não pode ser outro anel amarelo** igual à janela (dois anéis iguais e a criança não sabe qual é a ajuda: a diferença tem que ser de FORMA, não de cor) |
| **letras-escondidas** | levar a letra que falta até o buraco DENTRO da palavra | a letra certa **sai da palavra**, na posição do `_` do molde — resposta escrita à parte um dia deixa de bater com a palavra e ninguém percebe |

**Por que ela não é a `completar` nem a `digitar`:** na `completar` a criança
escolhe um pedaço que fecha a FRASE; na `digitar` ela soletra a palavra inteira.
Aqui a palavra já está quase escrita e falta **uma letra dentro dela** — que é
exatamente o gesto de uma regra ortográfica. É a mecânica da atividade de
**M antes de P e B** do 5º ano (`ca_po`, `bo_ba`, `ta_bém`, com M e N na
bandeja), e por isso ela existe.

**As três coisas que fazem diferença e não são óbvias:**
- **Escreva pelo menos DUAS letras a mais, e a que a criança confunde primeiro.**
  O 2º degrau do andaime some com as que não ajudam e **deixa uma de pé** — em
  M/P/B a escolha fica cara a cara entre M e N, que é onde a regra mora. Com uma
  letra a mais só, o degrau limpa a bandeja, a resposta fica dada e o **3º degrau
  vira código morto** (é a mesma conta que a mecânica `escolher` já fazia).
- **`esc` e `pal` têm que ter o mesmo tamanho, letra a letra.** É o alinhamento
  entre os dois que diz qual letra some; não existe campo de "resposta".
- **A palavra pode ter mais de um buraco** (`BO_BO_`): as vagas se enchem da
  esquerda para a direita e a bandeja traz uma letra por buraco.

**Medida na bancada:** código 0 nos 9 portões. Duas coisas que só apareceram
JOGANDO, e que portão nenhum pegaria — ficam escritas para não voltarem:
- **o arrasto com MOUSE não chegava nunca.** Os `onmousemove`/`onmouseup`
  moravam no próprio ladrilho, e o mouse sai de cima dele no primeiro
  centímetro. Com o dedo funcionava (o toque continua indo para o elemento onde
  começou), então o defeito era invisível no celular e total no PC da escola —
  que é justamente onde há mouse. **Enquanto o gesto dura, quem escuta é o
  DOCUMENTO.**
- **o tremor do erro desfazia o andaime.** O estado do ladrilho morava na string
  `className`, e o tremor (110ms e 240ms depois do erro) a reescrevia por cima:
  a peça dizia "tirei as letras que não servem" e um quarto de segundo depois
  elas **voltavam para a bandeja**. Estado de peça é FLAG (`_usada`, `_some`,
  `_acesa`) e a roupa se escreve num lugar só.

**Portão:** `_qa/dinamicas.py` reconhece a mecânica pelo par `.leBuraco` +
`.leLetra` e cobra as quatro armadilhas dela (letra tirada da palavra, teclado
de verdade, bandeja embaralhada, letra usada saindo de cena) — **visto
reprovando em três mutantes** antes de entrar.

## vitrine (exposição do museu)
A versão mais corrigida mora em `_padrao/pecas/vitrine.html`. Expositiva: uma tela por bicho/grupo com imagem (IA), nome/grupo e fatos curtos (onde vive / o que come / marca do corpo); "Próximo" avança; a última chama `mostraBanner` (no motor vira a próxima fase). Armadilha: nunca ter caminho de saída — o botão tem `data-qa` para o jogador terminar.
