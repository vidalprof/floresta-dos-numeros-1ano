# 📐 O CONTRATO DO ESQUELETO — como uma mecânica se encaixa no motor

> ## ⭐ O MODELO É O **JARDIM DO BROTO** (ordem do Marcos, ago/2026)
>
> Palavras dele: *"só lembrando que o nosso modelo de atividade é a atividade do
> Broto por enquanto"*. **O esqueleto se parece com o Broto**, não com o Circo do
> Teo nem com nenhuma outra. Ele está no ar, as crianças estão gostando, e ele
> mesmo disse: *"achei que a atividade do Broto está perfeita"*. Quando houver
> dúvida sobre como uma tela deve ser, a resposta é **abrir o `_jardim/index.html`
> e olhar**.
>
> **A espinha do Broto, que o esqueleto herda inteira:**
> `telaCapa` → `telaQuem` (o crachá: quem vai jogar) → as fases → `telaFim`
> (boletim animado + medalha) → **relatório do professor escondido**
> (`segredoRelatorio`: abre segurando a medalha 2 segundos, nunca botão à vista).
>
> **E as peças do motor dele, pelos nomes que já existem:**
> - `ajudaJd(n, ops)` — o andaime que cresce: 1º erro dica · 2º consolo + apoio
>   concreto · 3º revela e segue;
> - `reg(conceito, acertouDePrimeira, tentativas)` — a medição invisível que vira
>   o parecer do professor;
> - `fracos()` + `treinarFracos()` — o "Treinar o que faltou", só para quem tem
>   objetivo abaixo de 75%;
> - `resumoAnimado()` — o boletim que conta estrelas e acertos, sem nota e sem a
>   palavra "errou";
> - `crachaEl()` — o crachá com o nome e a figurinha escolhida;
> - `setProg` · `montaBarra(dicaId, dicaTxt)` · `falar`/`falaDaTela` · `VOZOK`
>   (alto-falante em cada resposta) · `salvaEstado` (continuar de onde parou).
>
> **O que MUDA em relação ao Broto:** 32 fases no lugar de 17, e 16 mecânicas
> diferentes (10–12 para pré/1º/2º, onde o gesto ainda é conteúdo). O resto é o
> Broto — inclusive o jeito, o tom e o ritmo.


> Decisão do Marcos (ago/2026): **32 fases** por atividade, **16 mecânicas
> diferentes** (10–12 para pré/1º/2º, onde o gesto ainda é conteúdo). E a meta:
> *"conseguir deixar uma atividade inteira com o esqueleto em minutos e não em
> horas, e claro que fique profissional e fantástica"*.
>
> A ideia que torna isso possível: **a atividade deixa de ser código e passa a ser
> conteúdo.** O motor já tem as 16 mecânicas dentro; eu escrevo o `conteudo.json`
> e o montador gera o HTML, o `falas.json` e a lista de arte.

---

## 1. O QUE O MOTOR FAZ (a mecânica não precisa se preocupar)

Antes de chamar a mecânica, o motor já montou:

| Já pronto | O quê |
|---|---|
| `limpa()` | a tela anterior saiu |
| barra de progresso | na posição certa da fase (calculada da ordem real) |
| selo | o nome da fase |
| `.balao` | **o enunciado**, com o botão de ouvir |
| voz | o enunciado é falado (a dose muda com o ano — §3-A da RECEITA) |
| `cen` | o `<div class="centro">` onde a mecânica desenha |
| barra de dica | com o texto da dica e a voz dela |
| **o andaime** | `ajuda(n)`: 1º erro dica · 2º apoio concreto · 3º revela e segue |
| medição | `reg(conceito, acertouDePrimeira, tentativas)` alimenta o relatório |
| retomar | o ponto é salvo a cada fase (55 min) |

Depois que a mecânica chama `fim()`, o motor cuida da comemoração, do banner e
da fase seguinte.

## 2. O QUE A MECÂNICA TEM QUE FAZER

```js
MEC["nome-da-mecanica"] = function (f, cen, fim) {
  /* f   = o objeto desta fase, vindo do conteudo.json
     cen = onde desenhar (o enunciado já está acima)
     fim = chamar quando a fase terminar                         */
};
```

**Obrigações (é isto que os portões medem):**

1. **Alvo de toque ≥ 44 px** (≥ 40 px dentro de grade).
2. **Nada essencial só na cor** — sempre cor + forma/ícone/texto.
3. **Funciona no mudo**: todo som tem gêmeo visual.
4. **As duas portas**: se tem teclado na tela, aceita `document.onkeydown`;
   se tem arrastar, aceita **também o toque simples**.
5. **`data-qa`** no que o auditor-jogador precisa para conseguir terminar.
6. **Nunca trava**: sempre existe caminho para fechar a fase.
7. **Voz por rodada**: se o enunciado muda dentro da fase, `falaDaTela(id)` na
   mesma hora em que o texto muda.
8. **Erro não pune**: `sErro()` + `ajuda(n)`, nunca X vermelho nem "errou".
9. **Toda opção tocável ganha alto-falante** (`op_<chave>.mp3`) — o motor põe
   sozinho nas classes `.opt,.pc,.lig,.bin`; use essas classes.

## 3. OS AJUDANTES QUE A MECÂNICA PODE USAR

`el(tag,classe,html)` · `imgEl(nome,classe)` · `baguncar(lista)` ·
`falaDaTela(id)` · `mostraDica(txt)` · `ajuda(n)` · `reg(conceito,ok,tent)` ·
`sCerto() sErro() sTap() sPop()` · `festa()` · `faisca(x,y,cor,n)` ·
`centroTela(el)` · `depoisDaFala(id,ms,cb)`

## 4. O FORMATO DE UMA FASE NO `conteudo.json`

```json
{
  "id": "cores",
  "mec": "classificar",
  "selo": "AS DUAS GAVETAS",
  "enunciado": "Onde vai cada um?",
  "dica": "Pense de onde a coisa veio.",
  "conceito": "origem",
  "gavetas": [{"k":"aqui","n":"Já estava aqui"},{"k":"fora","n":"Veio de fora"}],
  "itens": [{"img":"milho","n":"MILHO","alvo":"aqui"}]
}
```

O montador confere: mecânica existe, campos obrigatórios presentes, imagens no
banco ou na lista de arte, e **gera o `falas.json` a partir dos próprios textos**
— é isso que torna impossível a voz dizer coisa diferente da tela.

## 5. A ESCADA (o motor cobra, o portão do pedagogo mede)

- fase 1 é **problema**, nunca explicação;
- o primeiro símbolo só depois do primeiro figural;
- **aquecimento entre 25% e 65%** do caminho;
- a mesma mecânica **nunca em fases vizinhas**, e a segunda vez é **um degrau
  acima** (a primeira com apoio, a segunda sem);
- fecho com gancho.


---

## 6. LIÇÕES DAS PRIMEIRAS PEÇAS (achadas construindo, ago/2026)

Cada uma destas foi descoberta por quem montou a peça, não por mim. Estão aqui
para a próxima não repetir.

- **Distratores demais ou de menos quebram o andaime.** Um quiz com 2 distratores
  faz a criança eliminar tudo antes do 3º erro — o degrau "revelar" vira **código
  morto**. Use 3 distratores, e tenha a rede: se as erradas acabarem antes,
  revele na hora em vez de deixar uma tela com uma opção só.
- **Marcar no `mousedown` quebra o mouse.** O `click` que vem logo atrás cai em
  "já estava marcada" e desmarca — com mouse de verdade, a criança clica e nada
  acontece. A marca é do **clique**; o arrasto só marca quando anda mesmo.
- **O clique FANTASMA do celular desmarca a escolha.** Quem vem do dedo resolve no
  `touchend`, e o clique sintético de trás é engolido por um guarda de tempo.
  ⚠️ Isto **o portão não pega**: só aparece com dedo de verdade.
- **A peça tem que terminar numa `.medal`.** Sem isso o auditor-jogador roda os
  5200 giros (~20 min) sem reconhecer que acabou. Com ela, fecha em ~10.
- **`preventDefault` só no `touchmove`, e só com peça na mão** — e longe do
  `touchstart`, que é a janela que o portão inspeciona.
- **O CSS da peça mora no PRIMEIRO `<style>`**: o `_qa/classes.py` só lê esse.
- **Nada de emoji para a criança.** A estrela da medalha é `content:"\2605"`.
- **Nunca citar `limpa()` num comentário dentro de uma função.** O detector de
  telas lê o **texto cru** do corpo — comentário não é comentário para ele. Uma
  função de acerto virou "tela", foi chamada sozinha sem argumento e derrubou
  três portões com `TypeError`. O comentário vai para FORA do corpo.
- **O `MOLDE.html` sozinho NÃO passa a bancada** (o jogador dá PRESO: não há
  `.medal`). Toda peça precisa da sua `telaFim()` com a medalha.
- **Cuidado com nome de propriedade que colide com nome de classe.** Uma
  propriedade `r.pal` fez o portão reconhecer a peça como marca-texto. Nome de
  dado ≠ nome de classe.
- **O enunciado não pode PROMETER o que a grade não tem.** No caça-palavras, com
  a direção sorteada palavra a palavra, saíam grades **sem nenhuma diagonal** — e
  o enunciado prometia diagonal sempre. A criança varre a diagonal à toa. Cura:
  as direções são um **plano embaralhado** (todas entram) **e** o enunciado é
  montado a partir de onde as palavras realmente ficaram.
- **Sorteio que nunca exercita a armadilha esconde o defeito.** As palavras quase
  nunca se cruzavam, então a armadilha da palavra cruzada (que conferia só `mark`
  e não `ok`) não era testada de verdade. A colocação passou a **preferir**
  posições que cruzam.
- **Tom: "Faltam 0 tentativas" soa como bronca.** No fim da forca virou "Vamos
  olhar a palavra juntos" — que é o que a peça de fato faz.
- **A CORRIDA DE EVENTOS: o toque que chega no meio da comemoração.** Ao acertar,
  a fase agenda a próxima etapa em ~700ms — mas continuava aceitando toque nesse
  intervalo. Um segundo toque rápido fazia a fase avançar com o estado ERRADO (a
  fita cortada em outro número de partes). Toda fase precisa de uma trava
  (`travada = true`) no instante do acerto, não só no fim da animação. **Criança
  toca duas vezes; é o normal dela, não o excepcional.**
- **Ajudante chamado antes do elemento existir.** Uma função de limpeza era
  chamada no começo da fase e lia um elemento criado mais abaixo — `TypeError` na
  primeira carga, derrubando quatro portões de uma vez. Todo ajudante que toca no
  DOM começa com `if(!elemento) return;`.
- **O andaime tem que crescer no erro MAIS NATURAL, não só no previsto.** Numa
  peça de traçar, o ramo "pulou casa" (tocar direto no destino — o gesto mais
  natural que existe, *"quero chegar ALI"*) escrevia uma dica FIXA e não chamava
  o andaime. A criança lia a mesma frase para sempre; os degraus de piscar e de
  abrir o caminho nunca chegavam nela. **Todo caminho de erro chama `ajuda(n)`.**
- **Vocabulário de outra rodada é resto de clone em miniatura.** Na 2ª rodada as
  dicas ainda diziam "a valeta", "olhe a água" — palavras da 1ª. Não estoura
  nada; só a criança percebe. O nome do que está na tela sai de uma função, nunca
  escrito à mão em cada dica.
- **Temporizador de rodada velha trava a tela.** Um `setTimeout` continuava
  rodando depois da troca de tela e deixava `travado = true` na rodada nova — a
  tela parava de responder ao dedo, sem erro nenhum no console. Todo temporizador
  guarda a GERAÇÃO da rodada (`if(ger !== geracaoAtual) return;`).
- **Opção já tentada não pode se distinguir só pela cor — nem responder com
  silêncio.** Um retângulo rosa e um `return` seco: quem não distingue cor toca
  ali para sempre achando que travou. Etiqueta em palavras ("já tentamos") + som
  de retorno.
- **A 3ª DICA INVISÍVEL — a família de defeito que passou pelos 8 portões.**
  Em quatro peças diferentes, `revela()` chamava o "acertou" no mesmo instante, e
  o "acertou" apagava a barra de dica. Resultado: o pedaço pulava sozinho para o
  lugar **sem a criança ler a explicação**. O 3º degrau do andaime existia no
  código e **nunca era visto**. Cura: `esperaERevela()` — acende o certo, deixa a
  dica de pé ~1s, e só então resolve; com guarda de geração e de peça já usada.
- **⭐ O ERRADOR (`_qa/errador.js`).** Os cinco defeitos mais graves do dia
  passaram inteiros pelos 8 portões e só apareceram **errando de propósito, com a
  receita certa de cada mecânica**, três vezes seguidas, e conferindo se ainda dá
  para chegar à medalha. É um teste por mecânica, como o `_qa/dinamicas.py`.
  **Mecânica nova = receita nova no errador**, junto com a linha no catálogo.
- **⚠️ O DEFEITO QUE APARECEU EM 5 DE 6 PEÇAS DO MESMO LOTE:** a dica do 3º
  degrau — a que EXPLICA a revelação — era escrita e **apagada no mesmo quadro**,
  porque o "revelar" chamava o "acertou" e o "acertou" limpa a dica. A peça se
  consertava sozinha e a criança não sabia por quê. **Ordem correta: revela →
  DEPOIS escreve a dica.** Nenhum portão vê isso: só medindo o texto na tela
  depois de errar.
- **A DICA CAÍA ABAIXO DA DOBRA — nas 57 peças de uma vez.** Ela era o último
  filho do `.centro`; em 320×568 e no monitor 1366×768 da escola ficava 25 a 96 px
  fora da tela. A criança que errou tinha que ROLAR para achar a ajuda, justo
  quando está perdida. Agora entra **logo depois do enunciado**, que é onde o olho
  já está. ⚠️ O portão de leiaute **abre a fase vazia** e por isso nunca mediu
  isso — medir a tela COM A DICA ABERTA é portão que ainda falta.
- **Propriedade declarada e nunca lida = escada que não existe.** Uma peça tinha
  `apoio` em `FRASES[0]`, prometendo um degrau de ajuda na 1ª rodada — e nada no
  código lia essa propriedade. A escada estava no dado, não no comportamento.
- **Tela antiga continua clicável embaixo do banner.** Um toque no "+" depois de
  fechar a última coluna caía num índice que não existe e **matava o resto do JS
  da partida**. Toda função que mexe no estado começa com `if(!emJogo()) return;`.
- **PORTUGUÊS MONTADO POR CONCATENAÇÃO — o defeito que nenhum portão vê.**
  Saíram na tela: *"encostado na ponta **do a** fita azul"* (artigo decidido por
  `indexOf("fita")`) e *"**domingo-feira**"* (`nome + "-feira"`). Regra: **artigo
  e flexão são DADO** (`art:"a"`, `nomeCompleto:"domingo"`), nunca deduzidos de
  texto. Quem lê isso é uma criança aprendendo a ler.
- **"A ponta está no meio" não quer dizer nada para ela.** Virou "está entre o
  zero e o 1". Toda frase de ajuda tem que apontar para algo que ela VÊ na tela.
- **A DICA NÃO PODE MENTIR.** Na trilha, o 2º degrau dizia *"deixei um apoio na
  tela"* mesmo nas casas em que o apoio **já estava lá desde o começo**. A criança
  procurava uma novidade que não existia. Dica que descreve algo que não mudou é
  pior que dica nenhuma — ela manda procurar no lugar errado.
- **Peças que nascem uma em cima da outra escondem a mecânica.** No relógio os
  dois ponteiros começavam sobrepostos às 12:00 e a criança não descobria que há
  **dois** para mexer. A posição inicial é parte do ensino.
- **O dado não pode mostrar face antes do primeiro lance** (parece que já rolou),
  e a peça do jogador não pode tapar a palavra escrita na casa.
- **CONFERIR POR POSIÇÃO, NÃO POR IDENTIDADE DO ELEMENTO.** Ao traçar a letra T,
  o 2º traço começa **em cima** do ponto do meio do 1º. Conferindo por identidade,
  a criança tocava no lugar certo e a peça dizia que não era ali. O que importa é
  ONDE ela tocou, não em qual `<div>`.
- **Traçar não é responder: sair da linha não pune.** Som de **retorno**, nunca de
  tropeço — é gesto em treino, e o dedo da criança treme.
- **"Arrumar" preserva a ordem que ela montou.** Recomeçar do zero apaga o
  raciocínio dela; **depurar é a metade que ensina**.
- **Desenho feito de CSS mente com facilidade.** Numa mesma peça: o alto-falante
  desenhado ao contrário lia como seta para a esquerda; a bola virou placa de
  proibido e depois cruz; a árvore ficou sem tronco. **Nenhum portão vê forma** —
  só olhando o print. Quando a peça virar atividade, a figura é de IA.

---

## 7. LIÇÕES DA PRIMEIRA ATIVIDADE MONTADA (ago/2026)

A primeira atividade que o esqueleto gerou inteira — 32 fases, 16 mecânicas —
**reprovou na banca**. As quatro coisas que ela ensinou valem para sempre, e as
quatro são do mesmo parentesco: *o que não dá erro é o que chega na criança.*

- **A marca de recorte tem que ser uma marca que ninguém escreva por acaso.**
  A marca de peça era `/* ---------- nome ---------- */` — e as próprias peças
  usam esse traço nos comentários delas. Eram **163 marcas para 74 peças**: o
  montador partia a peça no primeiro comentário interno e escrevia **meia
  mecânica** na atividade. E o `node --check` **não veria**, porque a metade
  fecha as chaves. Marca de máquina se escolhe para não colidir com texto humano.

- **O "resto de clone" mora onde não dá erro.** O motor extraído do Broto
  continuava carregando `DOM`/`ROTCRI`/`TREINO` (os conceitos dele), o menu do
  professor com as 17 telas dele, a pré-carga, o alto-falante, o crachá, o nome
  do mascote, o fundo (cravado no **CSS**, onde nenhum portão de JS olha) e —
  a pior — a chave do `localStorage` `"jardim_med"`. No GitHub Pages **todas as
  atividades moram na mesma origem**: duas geradas pelo esqueleto apagariam o
  progresso uma da outra na mesma tarde. Hoje o extrator **varre o motor pronto**
  atrás de `jd_` e "Broto" **no código** (comentário não conta: o esqueleto diz
  de propósito que nasceu do Broto) e **se recusa a escrever** se achar. Uma
  marca esquecida ali viraria resto de clone em *toda* atividade gerada: uma
  falha só, multiplicada por todas.

- **Ao colar dois motores, o que falta é o que ninguém declarou.** O integrador
  trazia só o segundo `<script>` da peça (a mecânica) e deixava o motorzinho do
  MOLDE para trás. Faltavam exatamente `nota()` e `ac()` — o som. `escolher`
  passou, `completar` passou, e a **memória morreu no primeiro som de carta
  virando**. Todo o resto do motorzinho o motor já tinha **com o mesmo nome**, e
  é por isso que nenhuma peça precisou ser reescrita.

- **O portão que achou tudo isso foi o que JOGOU.** O `node --check` passou, o
  `_qa/funcoes.py` passou no arquivo certo, o print ficou perfeito. Quem disse
  "PRESO na fase 3" foi o `_qa/jogador.js`, que joga até a medalha. **Atividade
  montada não se entrega sem o jogador ter chegado ao fim.**

### O conteúdo de cada mecânica: a GAVETA

Toda peça abre com um bloco de dados de exemplo, e o comentário acima dele diz
sempre a mesma frase: *"troque APENAS este bloco"*. O integrador acha o nome
dessa `var` e transforma a última linha da peça na troca do exemplo pelo
conteúdo **desta fase** (`f.dados`). É o que faz o `conteudo.json` virar
atividade **sem tocar na peça** — que é o ponto: a peça já foi testada, e
reescrevê-la é reintroduzir o que ela custou.

O formato de `dados` de cada uma das 74 está em **`pecas.json`**, com o exemplo
da própria peça ao lado. Fase **sem** `dados` roda com o exemplo — serve para
ver a mecânica de pé, **nunca** para entregar ao Marcos.

---

## 8. A OFICINA FECHADA — 74 de 74 (ago/2026)

Varredura de todas as peças pela bancada (`_qa/peca.sh`): **74 aprovadas, código 0**.

Duas reprovavam e **nenhuma tinha defeito**: era o portão das dinâmicas acusando
o inocente. A regra de *"ouvir e achar"* — que existe por um bom motivo, porque
**PC de escola sem caixa de som existe e criança surda também** — tinha como
gatilho `speechSynthesis` + opções na tela. Só que `speechSynthesis` é a **voz de
reserva do navegador**, usada por várias peças para ler a resposta em voz alta:
não é a marca daquela mecânica. Cinco peças casavam, uma só era de ouvir e achar.

**A lição, que já se repetiu cinco vezes neste projeto:** gatilho de portão tem
que ser a marca *daquela* mecânica, não uma ferramenta que qualquer peça usa.
Quando o gatilho é largo, o portão cobra de quem não deve — e portão que acusa o
inocente ensina a ignorar portão, que é o pior estrago possível.

### As lições novas desta rodada (todas medidas, nenhuma suposta)

- **A colisão de CSS entre a peça e o motor.** Elas usam os mesmos nomes — é isso
  que dispensa reescrever as peças. O preço: **o que a peça não declara vem do
  motor**. O `gap:10px` do motor entrou de carona no `.mcartas` da peça, a conta
  de 48% + 1% estourou, e o jogo da memória empilhou as 8 cartas numa coluna de
  950px — 4 fora da tela de 640px da escola. O integrador agora **lista as 54
  classes que o motor também estiliza**.
- **`.tela` do motor é camada absoluta de tela cheia.** A tela que a peça cria
  por dentro da fase virava uma camada solta sem largura. A `.pecabox` neutraliza.
- **Carta virada que a peça perde de vista fica MORTA.** A criança fecha 3 de 4
  pares e trava com dois quadradinhos na tela, sem erro nenhum. A carta órfã
  passou a ser **adotada**.
- **A ordem de boot.** O conteúdo é escrito DEPOIS do condutor; chamar a partida
  antes deixava o menu do professor sem fases e o boletim sem objetivos. E o `ID`
  tem que **substituir** o de fábrica lá em cima, não ser atribuído no fim — o
  corpo do motor usa `ID.pre` durante a leitura do arquivo.
- **A voz de tudo o que a peça mostra.** O `VOZOK` nascia vazio; agora o montador
  desce o `dados` inteiro. E o que só existe jogando se **colhe jogando**
  (`colher.py`), até duas partidas seguidas não trazerem nada novo.

---

## 9. A PRIMEIRA ATIVIDADE MONTADA PASSOU A BANCA INTEIRA (ago/2026)

`bash _qa/auditar.sh` → **código 0. BANCA APROVOU.**

32 fases · 16 mecânicas · 145 falas · 79 alto-falantes · 328 KB (as 74 peças
juntas dão 1 MB de JS; a atividade leva só as 16 que usa).

⚠️ **Como ler este resultado com honestidade.** A arte dessa atividade de teste é
de mentira — discos coloridos gerados com Pillow, não arte de IA. O que está
provado é o **motor**, não uma entrega. E as figuras de teste ensinaram uma coisa
por conta própria: na primeira versão eram três desenhos diferentes para o
mascote, e o portão `3d` reprovou com *"muda 69% do corpo — TREME"*. Refeitas
como as de verdade têm que ser (edição da pose parada: muda só a boca, só os
olhos), ele mediu **2,0% e 2,5% — ok**. O portão funciona, e a regra do
`CLONAR-MOTOR.md` está certa: **as camadas do mascote se EDITAM, nunca se geram
do zero**.

**Um aviso que não é defeito:** o portão `1f` diz *"a medalha ocupa só 8% da
caixa dela"*. O Jardim do Broto, que está no ar e foi aprovado pelo Marcos, dá o
mesmo aviso (11%) e sai com código 0 — é elemento decorativo centrado numa área
larga, não figura perdida. Conferi antes de mexer: **não era nada que o esqueleto
tivesse introduzido.**

---

## ⚠️ LIÇÃO PAGA — "0 figura a gerar" com DEZ figuras faltando (ago/2026)

Re-provei o esqueleto montando uma atividade de teste com 32 fases. O montador
anunciou, satisfeito: **"0 figura(s): 0 já no banco, 0 a gerar"**. A banca, logo
depois, achou **DEZ imagens que não carregam** — as três camadas do mascote, os
seis crachás e a medalha.

**O `arte.json` é a LISTA DE COMPRAS da atividade**, e ela vinha vazia por dois
motivos, os dois do mesmo tipo — olhar no lugar errado:

1. o montador só procurava figura em `itens`/`opcoes`, que é o formato ANTIGO,
   de antes do esqueleto. A arte das fases mora no **`dados`/`dadosExtra`** (é o
   que a peça lê), e ninguém descia até lá;
2. ninguém pedia a **arte da IDENTIDADE** — a que o MOTOR exige em toda
   atividade, exista o conteúdo que existir: `<pre>_<mascote>_feliz/_fala/_pisca`,
   `<pre>_cr1..crN`, `med_<pre>` e o fundo.

**O estrago que isso faria:** quem montasse uma atividade de manhã geraria a arte
que o `arte.json` listasse, publicaria, e a criança abriria o app com o mascote,
os crachás e a medalha em quadradinho vazio. Nada acusaria antes — o HTML está
certo; a figura simplesmente não existe.

**Os dois consertos**, porque um só não bastaria:
- `montar.py` desce ao `dados`/`dadosExtra` e sempre inclui a arte da identidade
  (os nomes vêm do `motor.html`, não da memória de ninguém);
- **`_qa/arte_pedida.py`** (portão 0l da banca) compara a lista de compras com a
  pasta `img/` e reprova o que foi pedido e não foi desenhado — e reprova
  também a lista VAZIA, que era a assinatura do defeito de origem. Visto
  reprovando os dois casos e aprovando depois de a arte existir.

**A regra que fica:** número que o montador imprime (`0 a gerar`) é afirmação,
não medição. Toda conta que o montador anuncia precisa de um portão que a
confira contra o mundo — arquivo em disco, tela no navegador. *Existir não é
medir* apareceu de novo, agora do lado de quem produz.

---

## ⚠️ LIÇÃO PAGA — A ATIVIDADE MONTADA NASCEU MUDA (ago/2026)

Cobrança do Marcos, depois de abrir a Padaria das Letras: *"não teve fala
automática, visto que os pequinos precisam"* e, depois de eu mostrar a medição,
*"tem que falar o que está escrito"*.

**Medido antes de mexer:** 32 fases, **1 narrava sozinha**. E dos 23
alto-falantes, só 15 diziam o texto ao lado — **8 estavam em cima de uma letra
sozinha (M, B, P, D, C, G, Q, O) e não tocavam NADA**. Numa atividade de
alfabeto: a criança tocava o alto-falante da letra — o gesto exato que a
atividade ensina — e ouvia silêncio.

Eram **quatro** causas somadas, todas no caminho entre o texto da tela e o mp3.
Nenhuma delas dava erro; o app abria bonito e o `node --check` passava.

1. **O balão que a PEÇA escreve nunca era gravado.** O motor narra a fase
   *lendo* o balão que está na tela e procurando a gravação **daquele** texto; se
   não acha, fica calado de propósito. Só que **10 das 11 mecânicas escrevem o
   próprio balão dentro do código da peça**, e o montador só descia o `dados` da
   fase. → `balaoes_das_pecas()` no `montar.py`: abre a peça de cada mecânica
   usada e manda gravar o balão dela, renderizado como o navegador renderiza
   (tags fora, entidades decodificadas, espaços colapsados).

2. **Faltava o prefixo `op_` na hora de tocar.** `temVoz()` devolve só a *conta*
   do texto, e o arquivo gravado chama-se `op_<conta>.mp3`. O motor pedia
   `audio/<conta>.mp3`. **A fase ficaria muda mesmo com a voz gravada** — o
   defeito mais traiçoeiro dos quatro, porque some na inspeção do `falas.json`.

3. **O `dadosExtra` não era percorrido.** O balão do `ordenar` mora em
   `dadosExtra.ORDTXT.balao`, então as três fases de pôr o alfabeto em ordem
   ficavam mudas — justo o objetivo que a professora pediu primeiro.

4. **`eh_fala()` recusava a letra solta.** Exigia 3 caracteres e 2 letras, para
   impedir que `p0`/`gav1` virassem mp3. Regra certa, lugar errado: numa
   atividade de alfabeto ela barrava o conteúdo. Agora **letra em CAIXA é voz**
   (identificador de código é minúsculo), e duas letras em caixa são **sílaba**.

**Medido depois:** 32 de 32 fases narram · 29 de 29 alto-falantes dizem
exatamente o que está escrito.

### A regra que fica

> **O balão é contrato.** O que a peça escreve na tela tem que existir no
> `falas.json`. Peça que escreve balão próprio **declara** esse texto, e o
> montador o colhe — não se confia em "o colhedor pega jogando", porque ele só
> pega o que a partida alcança.

**Portão novo `_qa/fala_o_escrito.js` (0n da banca)**, porque a regra da casa é
que todo defeito que chega ao Marcos ganha o portão que o pega sozinho. Ele abre
a atividade e cobra três coisas: (1) o balão de cada fase tem gravação; (2) cada
alto-falante toca exatamente o texto escrito ao lado; (3) avisa quando há
resposta tocável sem alto-falante. Serve atividade **montada** (anda pelo
`FASES`) e **escrita à mão** (descobre as telas pelo nome).

**Testado com defeito plantado** — portão que só passa não prova nada:
tirei a gravação do `M` → acusou; fiz o `B` dizer "ELEFANTE" → acusou; apaguei o
balão do `juntar-silabas` → acusou as 5 fases, uma a uma. Código 1 nos três.

### E um defeito de VOZ ERRADA, do mesmo dia

O colhedor trouxe sete "falas" que não são frases: **`"BBOLOjá tentamos"`**,
`"LLEITEjá tentamos"`, `"MMELjá tentamos"`. É o `textContent` de um pai que
juntou dois filhos separados na tela (o crachá da letra, a palavra, e um aviso
de outro canto). Se passassem, o Edge TTS gravaria a bobagem e a criança que
aperta o alto-falante ouviria **"bêbolojá tentamos"** — e no 1º ano, quem ainda
não lê **acredita na voz**.

> **A marca da colagem é a mudança de caixa sem espaço.** Palavra em caixa alta
> grudada em minúscula não acontece em frase escrita para criança; acontece
> quando dois elementos viram um texto só. → `eh_colagem()` no `colher.py`,
> testado em 10 casos, 10 certos.

---

## ⚠️ LIÇÃO PAGA — A RENOMEAÇÃO DE CLASSES CEGAVA OS AUDITORES (ago/2026)

A banca reprovou uma atividade **certa**. O auditor-jogador dizia
*"PRESO em EM ORDEM [4%]"* — e a tela estava perfeita: as prateleiras 1º a 5º,
as letras D B A E C, tudo desenhado e clicável, sem um erro de JS.

**A causa:** o integrador renomeia classes para duas peças não brigarem pelo
mesmo nome (`.opt`, `.pc`, `.zona`). Ele renomeou `.pc` → `.o_pc` na peça de
ordenar — renomeação **correta**, sem colisão nenhuma. Só que o
`_qa/jogador.js` procura `.pc` para saber o que arrastar. Achou **zero peças** e
declarou a criança presa.

**O estrago real:** a banca reprovou o que estava bom, e eu quase fui
"consertar" uma fase sem defeito — que é o pior uso possível de uma manhã.

> **A regra que fica: classe pela qual um portão PEGA a atividade não se
> renomeia.** O vocabulário dos auditores é contrato, igual ao do motor.

Entraram no `VOCABULARIO_COMUM`: `pc cam lig par pchip peca qcpc qcvaga mcarta`
— tiradas de `grep` no `_qa/jogador.js` e no `_qa/errador.js`. **Auditor novo que
passe a depender de uma classe põe ela na lista no MESMO commit.**

Medido: jogador preso em 4% → **chegou ao fim, 181 passos**.

---

## ⚠️ LIÇÃO PAGA — MEDI UM ARQUIVO QUE O MONTADOR NÃO TINHA ESCRITO (ago/2026)

Reordenei as fases, rodei a banca inteira, li **"BANCA APROVOU"** e reportei ao
Marcos. Era mentira — sem querer, mas mentira.

O montador tinha **se recusado a gerar**: *"4 PROBLEMA(S) — nada foi gerado"*
(mecânicas iguais coladas, consequência do meu próprio reordenamento). O
`index.html` continuou sendo o de duas horas antes, e foi ele que a banca mediu.

> **Montador que reprova NÃO escreve.** Quem mede depois está medindo o arquivo
> de antes. Conferir a hora do arquivo (`ls -l`) antes de acreditar em qualquer
> veredito — e ler a ÚLTIMA linha do montador, que diz `escrito:` quando gerou.

É da mesma família de *"existir não é medir"*, agora no sentido inverso: o
arquivo existia, e por isso pareceu recente.

---

## 🎨 O DIRETOR DE ARTE — o portão que faltava (ago/2026)

Ordem do Marcos, quatro frases seguidas: *"profissional, lindo, sem erros"*,
*"maravilhoso, impecável"*, *"sempre subir a régua nisso"*, *"crie um
profissional especialista para isso"*.

**Por que ele precisava existir:** os 31 portões mediam se a atividade
**funciona**. Nenhum media se está **bonita**. Foi por isso que a banca deu
código 0 numa tela em que o alto-falante **tapava a última palavra** do
enunciado e a figura estava num **quadrado branco chapado** — os dois eu só
achei **olhando a foto**.

`_qa/visual.js` (portão 5b) mede em pixel, em 4 tamanhos: botão sobre palavra ·
quadrado branco chapado · cartões irmãos com cantos diferentes · **fileira
torta** (irmãos com alturas diferentes) · **botão esticado** (>6× mais largo que
alto) · texto espremido na borda.

**E já nasceu com a exceção que evita acusar inocente:** superfície em que a
criança DESENHA (folha de ligar pontos, traçar letra, tela de pintar) é branca
de propósito — papel é branco. Acusar isso seria o portão mandando pintar o
caderno.

**Dois defeitos estruturais que ele expôs:**
1. **Especificidade não se vence com especificidade.** O `comzap` do motor
   reserva 56px para o alto-falante; o CSS da peça, prefixado com `.mec-<nome>`,
   ganhava e devolvia para 18px. Medido: 18 onde deviam ser 56. Conserto:
   **estilo inline**, que folha nenhuma sobrepõe.
2. **Vão mágico é sempre origem de defeito.** A lista de respostas só rolava
   abaixo de 560px de altura — e 568 passa raspando por cima. Duas respostas
   ficavam fora da tela no celular pequeno. Conserto: o teto sai da conta da
   tela (`calc`), não de um número escolhido a dedo.
