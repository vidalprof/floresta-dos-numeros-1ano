# 🧰 O LEQUE TREINADO — onde mora a versão que JÁ funciona de cada dinâmica

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
| **Memória** | `_mapa` (carta grande, verso de arte, virada 3D) | par **conceitual** (causa↔efeito, palavra↔imagem) | carta fluida **≥ 130×88px**; verso de **arte de IA**, nunca retângulo liso; `rotateY` com queda para troca-de-face no Chrome 109; em tela baixa encolhe a LETRA, nunca a carta; som de virar e de par |
| **Arrastar** | `_mapa` "MONTE A LEGENDA" (`arrasta(b,k)`) | pôr no lugar É o conceito espacial | **três caminhos: mouse, dedo, toque simples**; **nunca** `preventDefault` no `touchstart`; guarda contra o **mouse fantasma** que o celular dispara depois do toque. Pego **DUAS vezes** |
| **Sombra / ache o par** | `_mapa` "ACHE O PAR" | forma e silhueta: olhar o contorno, não a cor | a silhueta tem que ser **da MESMA figura** (recorte da própria arte), senão a criança compara coisas diferentes; par que acerta **acende e pulsa** |
| **Ligar colunas** | `_naveg` "PARA QUE SERVIA?" · `_jardim` "PARA QUE SERVE" | relação 1-a-1 explícita | alto-falante nos **dois** lados; a linha precisa de `touchmove`; nunca mais que ~6 pares (vira memória disfarçada) |
| **Ordenar / linha do tempo** | `_historia` "LINHA DO TEMPO" · `_jardim` "telaOrdenar" | seriação e etapas **com a justificativa** | três caminhos de arrasto; **conteúdo conferido por especialista** — o portão não pega data histórica errada; faixa que rola precisa de `overflow-x` próprio |
| **Classificar em gavetas** | `_naveg` "VEIO OU JÁ ESTAVA?" | formar categoria por atributo definidor | enunciado sem termo que ela não conhece (*"veio de lá"* → **"veio de fora"**); as gavetas se **refazem** quando o eixo muda; a explicação espera o áudio (`depoisDaFala`, nunca `setTimeout` fixo) |
| **Achar na cena / lupa** | `_mapa` "O BAIRRO LÁ DE CIMA" (`naZona`, grade 48×48) | observação dirigida: ler a paisagem | zona = a **FIGURA recortada por pixel**, nunca um pontinho com raio; alvo no pixel **mais longe da borda** (`distance_transform_edt`), nunca no centroide; achou = **V verde**; singular só se houver UMA |
| **Pintar / marca-texto** | `_mapa` "PINTE O MAPA" (camadas medidas por pixel) · `_naveg` "A LÍNGUA GUARDA" | mapear categoria sobre o real — o traço É a classificação | a figura é **arte de IA**, o CSS anima só o que se mexe; o mapa começa **sem cor**; no texto: traço correndo + som de risco + barra + carimbo |
| **Simulador / deslizar** | `_historia` "A ÁGUA SOBE" (o que ele mais elogiou) · `_naveg` "O SEGREDO DO VENTO" | causa-efeito e controle de variáveis | o mundo reage **de verdade** (foto que gira não é simulador); ponto **medido na figura**, não a olho; a figura é gerada, o CSS anima |
| **Completar lacuna** | `_naveg` "COMPLETE A HISTÓRIA" | produção mínima com apoio da frase | a voz diz **exatamente** o texto escrito; em fase embaralhada o id da voz vem do **ITEM**, nunca do contador da rodada; figura sem fundo branco aparecendo |
| **Montar a palavra** | `_jardim` "telaMontaPalavra" | soletrar: qual letra vem primeiro | as duas portas (tela + teclado real); ⚠️ o `setTimeout` da rodada continua correndo depois do `limpa()` e reinstala o `onkeydown` **por cima da fase seguinte** — guardar `if(!t.parentNode) return;` |
| **Escolher / quiz** | qualquer uma — mas **≤ 2 telas em 20** | aferir rápido um fato já ensinado | **embaralhar as opções** (na Fábrica de Estrelas a certa era sempre a 1ª); alto-falante em CADA opção; distratores plausíveis; a dica fala da tela que está ali |
| **Relâmpago** | `_mapa` · `_naveg` | evocação rápida do que já foi visto | **não exigir andaime aqui** — dica no meio acaba com o que a fase treina (é velocidade). Está na lista `SEM_ERRO` do `_qa/pedagogo.py` |
| **Ensinar o mascote** | `_naveg` "ENSINE O ARÁ" | metacognição: a regra que ela ensina É o modelo mental | o mascote **erra visível** com a regra ensinada, senão vira quiz fantasiado; enunciado que muda por rodada exige voz por rodada |
| **Rota animada no mapa** | `_naveg` "A ROTA DA VIAGEM" (`ROTAP`, o navio andando) | trajeto e ordem no espaço | os pontos são **medidos na imagem**, não estimados (navio ancorando no continente errado estraga a fase) |
| **Quebra-cabeça** | `_mapa` "O MAPA EM PEDAÇOS" | parte-todo e orientação | peça na **proporção certa** da imagem (0,91 e não 1,0); mira na vaga; som de pegar, de encaixar e de fechar |
| **Coordenadas / bússola** | `_mapa` "ACHE PELA COORDENADA" e "A ROSA DOS VENTOS" | par ordenado e orientação | as coordenadas têm que **bater com a figura** (medir, não estimar — ele pegou isso); célula ≥ 40px; referência explícita ("o lado da sua direita") |

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

**Peças no catálogo hoje:** `achar-na-cena`, `arrastar-lugar`, `autoexplicacao`, `balanca`, `bussola`, `caca-palavras`, `caixa-dinheiro`, `classificar`, `completar`, `conserte-o-erro`, `contadores`, `coordenadas`, `criar-desafio`, `cruzadinha`, `decisao`, `digitar`, `ditado`, `ensinar-mascote`, `escolher`, `escrever-legenda`, `experimento-justo`, `filtro`, `forca`, `girar`, `grafico`, `investigar-fonte`, `ligar`, `linha-do-tempo`, `mapa-conceitual`, `memoria`, `misterio`, `montar-frase`, `morfemas`, `mudanca-permanencia`, `ordenar`, `pintar`, `prever-observar`, `quebra-cabeca`, `relampago`, `repartir`, `reta-numerica`, `saltos-na-fita`, `sete-erros`, `simetria`, `simulador`, `sombra`, `tabela`, `tangram`, `teia-alimentar`, `termometro`, `tracar-caminho`

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
| **arrastar-sombra** | levar o objeto até a silhueta — o par se faz pela FORMA | não confundir com `sombra`: lá se casa por TOQUE, aqui o gesto é ARRASTAR, e o gesto é conteúdo |
| **labirinto** | levar o personagem ao que ele precisa desviando dos inimigos | encostar no inimigo **não é castigo**: volta ao começo do trecho e segue. Sem vida, sem fim de jogo. E as SETAS DO TECLADO, não só o botão |
| **ligar-pontos** | a sequência numérica vira gesto: achar o 5 *depois* do 4 numa bagunça | tocar no ponto errado não pune — só não liga |
| **pintar-desenho** | a única em que a criança **produz** em vez de responder | **não tem certo nem errado**: nenhum som de tropeço, nenhuma marca de recusa. O peixe pode ser roxo. O que se mede é AUTORIA |
| **ouvir-achar** | o enunciado chega pelo ouvido, a resposta é uma FIGURA | a palavra tem que estar ESCRITA junto: PC de escola sem caixa de som existe, e criança surda também |
| **tracar-letra** | refazer o movimento da letra, sempre no mesmo sentido | sair da linha **não pune** — som de retorno, nunca de tropeço; o dedo da criança treme. E conferir por POSIÇÃO, não por identidade do elemento |
| **andar-ate** | dizer o caminho passo a passo — o começo do pensamento computacional | um comando = uma casa, e o boneco **anda** até lá (a transição é o que ensina) |
| **juntar-silabas** | **síntese**: BO + LO = BOLO. Os pedaços **deslizam** um até o outro e viram um só — é a corrida que ensina, não o encaixe | a palavra fecha dita **de uma vez**, nunca "BO… LO" (*Connected Phonation Is More Effective than Segmented Phonation*, Reading Rockets); a bandeja vai **embaralhada**, senão ela aprende a POSIÇÃO; erro devolve o pedaço com som de RETORNO; as **três portas** — clique, dedo e **arrasto** (aqui o arrasto **é** o conceito) |
| **bater-silabas** | **análise**, a outra metade: BOLO = BO + LO. A criança **bate uma vez por pedaço** (palma / mão no queixo) | **não desenhar os lugares prontos** — com 3 casinhas na tela ela conta as casinhas, não a palavra, e a resposta está dada; tem que dar para **Apagar** (contar errado no meio não prende); 2º degrau do andaime é pelo **OUVIDO** (a peça bate junto), só o 3º escreve; **barra de espaço** bate e **Enter** responde (as duas portas) |

### Números e medida

| mecânica | o gesto | a armadilha |
|---|---|---|
| **base-dez** | a criança **enche** a caixa e é ela quem manda trocar 10 por 1 | o conceito mora na TROCA, e a troca tem que ser VISÍVEL |
| **comparar** | as duas quantidades lado a lado **antes** do símbolo | inverter essa ordem é o que faz decorar "a boca do jacaré" |
| **calendario** | "faltam quantos dias?" é um CAMINHO, não uma subtração | um pulo de cada vez, animado — é o pulo que ensina, não a conta |
| **relogio** | a criança **move os ponteiros** (pedido do professor, com todas as letras) | os dois ponteiros não podem começar sobrepostos: ela não descobre que há dois para mexer |
| **bingo** | reconhecer sob pressão gostosa — prática de recuperação disfarçada | **não há relógio**: a pressão é da pedra que saiu, não do tempo |
| **trilha** | o acaso escolhe a pergunta, o que tira o peso do julgamento | o dado não pode mostrar face antes do primeiro lance, e a peça do jogador não tapa a palavra da casa |

### Raciocínio e leitura de mundo

| mecânica | o gesto | a armadilha |
|---|---|---|
| **intruso** | achar o que não pertence **e dizer por quê** | sem o segundo passo isto é um quiz: ela acerta por eliminação sem formular o critério. O "por quê" é TOCADO, nunca digitado |
| **quem-sou-eu** | eliminar candidatos com um atributo por vez | a informação chega em DOSES; a 1ª pista serve para pensar, não para acertar |
| **domino** | comparar duas pontas com quatro peças — a FORMA corrige, não o adulto | a peça só entra se a ponta bater; "combinar" não pode ser sinônimo de "ser igual" |
| **passo-a-passo** | o mundo **executa** a sequência dela, na frente dela | **não é ordenar**: ninguém confere nada. Se ela mandou regar antes de plantar, a água cai na terra seca — e é isso que ensina |
| **circuito** | ligar os fios e a lâmpada **acende de verdade** | traço decorativo perde o efeito inteiro: cada fio ligado tem que mudar o mundo |
| **camadas-mapa** | ligar/desligar camadas e ver o que só aparece na sobreposição | a resposta não está escrita em lugar nenhum da tela — se estiver, virou quiz com figura |
| **rotular** | levar o nome ao lugar **espacial** dele na figura | não é classificar: lá o lugar é uma gaveta (categoria), aqui é ONDE na figura |
