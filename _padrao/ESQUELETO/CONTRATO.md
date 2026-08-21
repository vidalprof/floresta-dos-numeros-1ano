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
- a mesma mecânica, quando repete, vem em **BLOCO — fases SEGUIDAS, não
  espaçadas** (regra VIRADA pelo Marcos, ago/2026, ver §6b), subindo **um
  degrau a cada vez** (a primeira com apoio, a última sem). Só o **aquecimento**
  pode reusar uma mecânica anterior fora do bloco — é revisão anunciada;
- fecho com gancho.


---

## 6b. ⭐ REPETIÇÃO SEGUIDA, NÃO ESPAÇADA (regra VIRADA — Marcos, ago/2026)

Palavras dele: *"as repetições das interatividades têm que ser seguidas e não
espaçadas — as crianças têm me dito 'mas professor isso eu já fiz, tô fazendo
de novo'"*.

**O que mudou:** o portão do montador cobrava o CONTRÁRIO — mecânica igual
colada era erro, tinha que espaçar ("nunca em fases vizinhas"). Só que o
espaçamento é JUSTAMENTE o que faz a criança sentir que voltou: ela faz
`escolher` na fase 1, mais quatro coisas, e reencontra `escolher` na fase 6 →
*"isso eu já fiz"*. Colada, ela lê como "mesmo jogo, próximo nível" (progressão);
espaçada, lê como "de novo o mesmo" (regressão).

**A regra agora:** cada mecânica que se repete aparece em **BLOCO** (fases
seguidas), subindo um degrau a cada vez (1ª com apoio → última sem). Reaparecer
depois de outra mecânica no meio = reprova (`a mecanica 'X' aparece ESPACADA`).
**Exceção única:** o **AQUECIMENTO** — revisão anunciada como tal, pode reusar
uma mecânica anterior fora do bloco (por isso sai da contagem do portão).

**Como o portão mede** (`montar.py`, na variedade por gesto): junta as posições
de cada mecânica (menos o aquecimento) e reprova se elas não forem contíguas
(`max-min+1 != quantidade` = tem buraco). A variedade continua valendo por cima
(≥4 gestos, nenhum > 40%): agrupar não reduz variedade, só muda a ordem.

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

## ⚠️ LIÇÃO PAGA — REGRA DE CSS QUE NÃO EXISTE, E NINGUÉM AVISA (ago/2026)

O Marcos apontou o **mesmo** botão de som **três vezes** — *"não ficou certo"*,
*"não ficou certo"*, e por fim *"esse botão de som está horrível. **A parte
preta tem que estar no meio do círculo. Acho que nem precisaria dizer isso**"*.
Não precisava mesmo. E a cada rodada eu ajustava pixel e ele continuava errado.

### Por que três rodadas
1. **Eu escrevia CSS para o elemento errado.** Estilei `.zap i`, `.zap b`,
   `.zap s` — que são os elementos do MOTOR. O botão daquela peça é outro:
   `<button class="zap"><i class="fone"></i></button>`. Deduzi a marcação de
   outra peça em vez de abrir o HTML daquela.
   → **REGRA: antes de escrever CSS para um componente, ABRIR o HTML DELE.**
2. **Eu media em número, não olhava.** `getBoundingClientRect` dizia "dentro do
   botão", e estava: a tinta ia de 6 a 27 num círculo de 32. Tecnicamente
   dentro, visualmente empurrada para o canto. **Encaixar não é centrar.**
   → **REGRA: acabamento se confere OLHANDO — foto em zoom 3×.** Foi a foto que
   mostrou o que número nenhum mostrou.
3. **E a última rodada eu escrevi a regra certa, que simplesmente não existiu.**
   Ver abaixo — é o defeito mais perigoso dos três, porque é MUDO.

### O defeito mudo: prosa virando seletor
Escrevi um comentário novo logo abaixo de um comentário que **já tinha
fechado**. Sobrou o meu `*/`, e o texto virou CSS. O escopador não tem como
saber o que é prosa: prefixou tudo e gerou

    .mec-ouvir-achar ⚠️ E ELE ERA DESENHADO A BORDA (corpo no `:after`, ... {...}

— seletor inválido, que o navegador descarta **junto com a regra**. A minha
regra do alto-falante não existia. `node --check` passa, o montador escreve, a
banca inteira dá 0, e só o desenho é que some.

### O irmão do defeito, que estava escondido no repositório
O escopador quebrava o CSS **por chave**, sem saber o que era comentário. Então
um comentário que EXPLICA uma regra — e por isso a CITA, tipo
`` `.balao + *{margin-top:13px}` `` — traz um par de chaves dentro de si: a
quebra corta o comentário no meio, a primeira metade some e a **segunda metade
vira o seletor da regra seguinte**. `.regra` (criar-desafio) e `.if_placar`
(investigar-fonte) estavam **mortas havia semanas** por causa disso. Ninguém
tinha visto — porque não dá erro.

### Os dois portões que ficam (`integrar.py`)
- **Comentário guardado antes da quebra** (`_COMENT` → placeholder → devolvido
  no fim): comentário nunca mais participa da conta das chaves.
- **`SELETOR_OK`**: seletor de verdade só tem um punhado de caracteres. Crase,
  acento, `⚠`, travessão = prosa vazada. O integrador **para e diz a linha**, em
  vez de escrever um arquivo com regra fantasma dentro. (O `%` está na lista
  porque `0%`/`50%` dentro de `@keyframes` são seletores de verdade — foi o
  primeiro falso-positivo que ele deu, e falso-positivo também se conserta.)

### O conserto de fundo: desenho de ícone é SVG, não aritmética de borda
Os três alto-falantes do app (o do balão, o das respostas, o da peça) eram
desenhados com **bordas e filhos em `position:absolute`**, com left/top em pixel
repetidos em **cada quebra de tela** — 6 blocos de conta na mão para um ícone de
18px. Bastava um sair do lugar e o boneco desmontava.

Agora é **um SVG embutido como `background-image`**: centra-se sozinho pelo
próprio `viewBox`, não tem coordenada para errar, fica nítido em qualquer zoom,
e em tela pequena muda **uma linha** (`background-size`). Data URI = continua 1
arquivo só, sem pedido de rede.

⚠️ **A cor mora DENTRO do SVG**, então `background-color` e `background-image`
ficam **separados**: usar o atalho `background:` em qualquer regra de estado
(hover, `.tocando`, variante branca) apagaria o desenho.

E o mesmo glifo serve os três — **dois desenhos diferentes de alto-falante na
mesma tela é amadorismo**, e era exatamente o que estava no ar (o do balão tinha
duas ondas, o das respostas uma só).

### Os dois defeitos que o próprio conserto criou (e os portões que ficam)

Trocar o desenho de borda por SVG resolveu o botão — e **abriu duas frestas
novas**. Ficam registradas porque foram medidas, não supostas:

1. **CÍRCULO VAZIO.** A ponte de estilo do Broto tem
   `.centro .pecabox .zap{background:rgba(...)}` — o **atalho** `background:`.
   Ele zera o `background-image` junto, e o botão vira um círculo pastel liso,
   sem desenho. No cartão da `ouvir-achar` (que tem CSS próprio) o glifo
   aparecia; em **todas** as fases que passam pela ponte, não. Medido: **48
   ocorrências** em 128 telas.
   → Portão **5-B** em `_qa/visual.js`: todo `.zap`/`.zapb` visível precisa ter
   **imagem de fundo OU filho visível OU pseudo-elemento**. Os três "none" =
   círculo vazio, e reprova.
   → E a regra de escrita: **onde há ícone no `background-image`, nunca o
   atalho `background:`** — `background-color` separado, sempre.

2. **FALSO-POSITIVO no portão do desenho.** Ao desligar os filhos antigos
   (`i`,`b`,`s`) com `display:none`, a caixa deles passou a ser **0,0** — e o
   portão 5 acusou "o desenho sai 250px do botão", que é a distância do botão
   até o canto da tela. **256 falhas**, todas mentira.
   → Conserto: pular filho com `display:none`. Não dá para usar o `vis()`:
   elemento de tamanho ZERO que desenha só por `:before`/`:after` é exatamente
   o caso que o portão existe para pegar. A peneira é só o `display`.
   → **A regra geral: portão que muda de comportamento quando o CÓDIGO CERTO
   muda está medindo a coisa errada.** Falso-positivo também se conserta, e no
   mesmo commit.

### E a barra de 400px para uma letra só
Na `completar`, quando o pedaço que falta é uma **letra**, as três opções
empilhadas viravam três tarjas de **400×65** (6,2× mais largas que altas) com um
"E" perdido no meio — o oposto de *"nada de botões muito esticado, quero tudo
simétrico"*. Agora, pedaço de até 4 caracteres → `.opts.curtas`, **ladrilhos
lado a lado** (96×66), que é o gesto certo: comparar três letras de uma olhada,
não ler três frases. ⚠️ O `flex-direction:row` tem que ser **escrito**: alguma
folha acima já põe as opções em coluna, e sem isso os ladrilhos ficam bonitos e
empilhados — que não era o ponto.

## ⚠️ LIÇÃO PAGA — TRÊS DEFEITOS QUE SÓ O OLHO PEGOU (ago/2026)

A banca inteira dava **código 0** e a atividade tinha três defeitos que a
criança veria na primeira aula. Nenhum deles é bug: são conteúdo errado, e
conteúdo errado passa por qualquer portão que meça código.

### 1. "Cada ficha conta uma tarefa da PLANTA"
Enunciado do Jardim do Broto **cravado no corpo** da peça `classificar`. Na
Padaria das Letras a criança lia sobre planta enquanto separava BOLACHA e
MAMÃO. Está certo em português, não dá erro, e **viajava para toda atividade
que usasse a mecânica**.
→ **Enunciado é CONTEÚDO, então mora na gaveta — nunca no corpo da peça.**
→ E a gaveta só sabia ler `var X = [` e `var X = {`: **texto também é
conteúdo**. O detector aprendeu a ler texto (só MAIÚSCULA, e nunca como gaveta
principal — a principal é a lista de rodadas).

### 2. O mascote pedia cinco poses e a casa só desenha três
`_pensa` e `_festa` entravam na pré-carga e davam **404**. Pior: quando mandei
o Gemini **editar** a pose parada para criá-las, voltaram **dois personagens
completamente diferentes** — o Fubá é um ratinho padeiro em 3D e vieram dois
meninos humanos em 2D.
→ **Pensar e comemorar são MOVIMENTO da pose parada, não desenho novo.**
Desenho novo do mascote sai fora do personagem com uma facilidade assustadora;
movimento não tem como sair, porque é o mesmo desenho. (`.broto.pensando` e
`.broto.festejando` no motor.)
→ E a pré-carga só pede as duas opcionais **se o arquivo estiver na pasta**.

### 3. O gerador ignorava a base em silêncio
`gerar-imagens.yml` fazia `if base and os.path.exists(base)`. Caminho errado =
o `base` era **descartado sem avisar** e o Gemini gerava do zero, devolvendo um
personagem novo com cara de sucesso.
→ **Edição com base ausente é ERRO**, nunca "gera do zero".

### E o portão que rodava cego
`_qa/imagens.js` guardava `if(typeof srcDe!=="function") return [];` — e
`srcDe` **nunca existiu** no motor (o caminho é montado inline). A condição era
sempre verdadeira, a lista voltava vazia, e o portão imprimia "imagens ok".
→ **Portão que não mede não aprova**: agora diz "NÃO MEDI" e sai com código 2.
→ E a regra que fica: **quando um portão passa, perguntar *o que* ele mediu.**
Os três defeitos acima estavam na tela; eu só os vi porque fotografei.

## 🎨 O GANCHO DE TEMA — `<pasta>/tema.css`

O acabamento é da **atividade**, não do esqueleto. Pintar a madeira da padaria
no `.btn` do motor pintaria toda atividade futura — inclusive a de ciências do
6º ano. Então: se existir `<pasta>/tema.css`, o montador o injeta **por último**
no `<style>`, onde ele ganha do motor e das peças no empate de especificidade.

**A peça diz o que a coisa É; o tema diz como ela se PARECE.** A `completar`
marca `.opts.curtas.letra` ou `.silaba`; quem pinta de lousa ou de biscoito é o
tema. Sem essa separação a mecânica ficaria presa a uma atividade.

E a regra do Marcos que o tema serve: **cada acabamento com um papel fixo**,
nunca doze peles para o mesmo botão. Madeira = ação. Toldo = título. Azulejo =
balão. Lousa = letra. Biscoito = pedaço. Metal = bandeja. Massa = folha de
traçar. Carimbo = já feito. Vidro = vitrine. A criança olha e sabe o que é
**antes de ler** — e no 1º ano isso é a diferença entre entender e chutar.
⚠️ Metal, massa e vidro **nunca carregam letra**: a leitura neles foi medida e
é fraca. São superfície, e superfície não é resposta.

## ⚠️ LIÇÃO PAGA — A PEÇA NOVA E OS TRÊS TROPEÇOS DA ESTREIA (ago/2026)

Escrever a peça das **caixas de som** (Elkonin) foi fácil; fazê-la ENTRAR na
casa custou três defeitos, e os três são de família conhecida. Ficam aqui como
a lista de conferência de toda peça nova.

**1. COLISÃO DE NOME DE CLASSE.** As caixas nasceram como `.cx` — e `.cx` já é
a **caixa de largar** na ponte de estilo (`.centro .pecabox .opt,.pc,.ficha,.cx`),
que pinta cartão branco. Na bancada ficou perfeita; **dentro da atividade
montada as caixinhas saíram brancas**. Colisão de nome não dá erro: dá um
visual errado que só aparece quando a peça entra na atividade.
→ **Nome de classe de peça nova se confere ANTES, contra a ponte e o motor.**

**2. RENOMEAR CEGA O AUDITOR.** Troquei para `.csb` e o portão do jogador
passou a dizer *"PRESO — a peça TRAVA"*. A peça estava perfeita; cego era o
auditor, que só toca no que casa com a lista de seletores dele.
→ **Classe nova = seletor novo no `_qa/jogador.js`, no MESMO commit.** E entra
também no `VOCABULARIO_COMUM` do `integrar.py`, senão a renomeação automática
a troca e cega o auditor de novo.

**3. BONITA NO ESCURO, INVISÍVEL NA ATIVIDADE.** A caixa vazia era um contorno
claro com 8% de fundo. Na bancada (fundo escuro liso) ficava ótima; sobre a
foto da padaria as prateleiras apareciam através dela e a **caixinha sumia**.
→ **Caixa vazia é o convite da peça: precisa de CORPO próprio**, que não
dependa do que há atrás. Peça se olha nos dois lugares — sozinha e montada.

### E o defeito que a própria correção criou
Ao pôr rolagem no `escolher` (resposta presa atrás da barra), a opção parou de
esticar na vertical e caiu para 62px: **400×62 = 6,5×**, acima do teto de 6 do
diretor de arte. Consertado pelo lado da **largura** (360px), não da altura —
engordar o botão roubaria justamente a altura que faltava na tela baixa.
→ **Toda correção de leiaute se remede no portão do acabamento, sempre.**

## ⚠️ LIÇÃO PAGA — O TERCEIRO PORTÃO CEGO, E A BANCA JÁ AVISAVA (ago/2026)

A banca termina com uma lista: **"PORTÕES QUE RODARAM CEGOS (mediram ZERO)"**,
e embaixo a frase *"aprovação vazia dá confiança falsa"*. Eu li essa lista
várias vezes esta semana e **nunca fui conferir**. Fui, e dos três:

- **0c (pergunta ambígua)** e **0k (explica a regra)** eram zero **legítimo** —
  a Padaria não tem fase de "ache na cena" nem fase que fecha por atributo
  distinto. Não há o que medir, e dizer isso é honesto.
- **1d (promessa)** estava **CEGO** — e em *toda* atividade montada.

### O que ele não via
O portão procurava a forma do Broto — `function ajuda(n,ops){`, uma
**declaração**. O esqueleto escreve `window.ajuda = function(n, ops){`, uma
**atribuição**. A expressão regular nunca casava, e ele imprimia "nada a
conferir" com a maior calma. **Mesma família do `srcDe`** no portão das
imagens: o auditor procurando a forma de UMA atividade em vez do que o código
FAZ.

E a "fala" também mudou de nome: no esqueleto quem promete é o `consolo()` (que
toca a voz de erro) e o `mostraDica()` — que **escreve** a promessa na tela.
**Promessa escrita é promessa igual:** a criança lê e espera.

### Medido dos dois lados, que é o que faz o conserto valer
- na Padaria: **0 → 5 ajudantes** encontrados, e aprova (nenhuma fala de ajuda
  sem a ação correspondente);
- num arquivo com o defeito histórico do Bento plantado de propósito (*"deixa eu
  pôr os brinquedos na mesa"* com `ops.concreto` opcional): **reprova**, e diz a
  linha e a chave que falta.

### A regra que fica
**A lista de "rodaram cegos" é tarefa, não rodapé.** Toda vez que ela aparecer,
conferir um por um: ou a atividade realmente não tem aquilo — e aí se diz —, ou
o portão deixou de enxergar. Esta semana foram **três** portões cegos
(`imagens`, `funcoes`, `promessa`); os três aprovavam.

## ✅ A ESTEIRA TEM AFERIÇÃO — e ela achou dois defeitos no primeiro uso

`bash _padrao/ESQUELETO/provar_esteira.sh` faz o caminho inteiro **do nada**:
esboço → preenche `mesa` e currículo → monta → **13 portões de estrutura**.
Sai **código 0**. É o que transforma o "1h30" de promessa em medida.

**Por que ela vale mais que testar numa atividade real:** junta as **16
mecânicas** num arquivo só, nenhuma passando de 6% das 32 fases. É o **pior
caso** para o motor, e a única situação em que uma peça brigando com outra
aparece. Rodar depois de mexer no motor, no montador ou numa peça.

### ⚠️ Por que ela NÃO roda a banca inteira — a lição que custou uma rodada
Rodei `auditar.sh` na `_prova30` e ela reprovou: 11 figuras que não existem, 6
fases mudas, 14 alto-falantes sem gravação. **Tudo verdade, e tudo esperado** —
a `_prova30` é um esqueleto: nunca teve arte gerada nem voz, e os textos são os
`«...»` do esboço.

A banca está **certa** em reprovar (atividade sem arte e sem voz não vai para
criança nenhuma). Errado seria eu gerar 11 imagens e ~270 vozes para uma
aferição descartável — dinheiro e uma corrida de workflow jogados fora, contra
a regra da cartela.

Então a prova mede **o que ela existe para medir: a estrutura**. E os portões
de arte e voz ficam de fora **ditos em voz alta** no relatório — *portão pulado
em silêncio é o começo de toda aprovação vazia*.

### Os dois defeitos que ela achou de cara
1. **O esboço nascia reprovado**: 32 problemas de cobertura numa atividade
   recém-criada. O objetivo saía do índice da mecânica, então cada um ficava com
   2 fases da MESMA mecânica — 1 gesto só. O professor perderia a manhã
   consertando uma estrutura que não foi ele que montou.
2. **A opção comprida do `completar`** ia a 400×55 = **7,3×**. A regra do teto
   já valia para o ladrilho de letra; a opção de texto tinha escapado.

E um **falso-positivo** do diretor de arte: a "fileira torta" media todos os
irmãos, inclusive os **empilhados**, onde altura diferente é natural.

## 📋 O ESTADO MEDIDO (ago/2026) — o que está provado, e com que número

Escrito aqui porque *"passou"* sem número é opinião. Tudo abaixo foi medido
**depois** da última mudança de cada um.

| o quê | como se remede | resultado |
|---|---|---|
| **a esteira, do nada ao HTML** | `bash _padrao/ESQUELETO/provar_esteira.sh` | **0** — 13 portões de estrutura |
| **A Padaria das Letras** | `bash _qa/auditar.sh _padaria/index.html` | **0** — banca inteira |
| **as peças da oficina** | `bash _qa/peca.sh _padrao/pecas/<x>.html` | **77 de 77** |

⚠️ **Banca que rodou ANTES da mudança não vale para depois dela.** Rodei a da
Padaria de novo só porque o `completar` mudou; e rodei a esteira de novo só
porque o container reiniciou. Aferição que só passou antes do reinício não
prova nada.

### O que continua fora da medição — e por quê
- **arte e voz da `_prova30`**: ela é esqueleto, e gerar 11 imagens + ~270
  vozes para uma aferição descartável é dinheiro fora (ver a seção da prova);
- **o portão do PROFESSOR**: é o Marcos, e nenhum script substitui.

## 🕵️ QUEM VIGIA O VIGIA — `bash _qa/provar_portoes.sh`

Esta semana **três portões estavam cegos ao mesmo tempo, e os três aprovavam**
(`imagens`, `funcoes`, `promessa`). A conclusão é desconfortável e virou este
arquivo:

> **Um portão que aprova não prova nada enquanto não se mostrar que ele
> REPROVA o defeito que ele existe para pegar.** Código 0 sem isso é
> confiança, não medida.

Para cada portão, o script planta o defeito **histórico** — o que chegou até o
Marcos de verdade — e exige código ≠ 0. E, onde já houve falso-positivo,
planta também o caso **certo** e exige código 0: *portão que grita à toa ensina
a ignorar portão.*

Hoje prova **48 casos em 19 portões**: `funcoes` (função inexistente · chamada
protegida por `typeof`) · `promessa` (voz promete e a tela não cumpre) ·
`dinamicas` (citação em comentário não é gatilho) · `clone` (prefixo de outra
atividade) · `visual` (opção esticada · opção no molde do motor) · `imagens`
(pré-carga com 404 · `<img>` quebrado · fundo CSS que não vem · tudo no lugar) ·
`progressao` (barra que volta · barra que só avança) · `telavazia` (fundo
falando sozinho · fecho com `fechaFase`) · `classes` (só dentro de `@media` ·
comentário com a palavra `@media`) · `falas` ("Complete" → *complite*) ·
`fluxo` (tela presa em si mesma + órfã) · `contraste` (creme sobre creme) ·
`leiaute` (alvo de 26px) · `vozfalta` (texto escrito e mp3 que ninguém gravou) ·
`vozdica` (a voz diz outra coisa) · `arte_propria` (o avatar emprestado) ·
`ambiguo` ("a ponte" havendo duas) · `vozintro` (a intro que cala a pergunta).
**Portão novo entra aqui no mesmo commit** — senão ele nasce sem prova.

### As duas coisas que ele já ensinou, na estreia
1. **Um dos meus fixtures nasceu errado e o portão estava certo.** Pus `.opt` +
   opções no arquivo de mentira, e o `dinamicas` reconheceu um QUIZ de verdade
   e cobrou o embaralhamento — cobrança legítima. **Antes de acusar um portão,
   conferir se o defeito plantado é mesmo o que se quer medir.**
2. **O `clone` pulava a conferência de prefixo EM SILÊNCIO** quando não achava
   o prefixo da atividade (pasta sem `img/`, ou com menos de 4 arquivos). E
   "pulei" calado some no meio de um relatório de 30 portões e vira "passou".
   Agora ele diz **"NÃO MEDI"** — a mesma regra dos outros três.

---

## 📏 A CONTA MORA NO MOTOR, NÃO EM CADA PEÇA — a opção esticada (ago/2026)

Regra do Marcos: *"nada de botões muito esticados, quero tudo simétrico no
app"*. O teto do diretor de arte (`_qa/visual.js`, regra 4) é **6 vezes mais
largo que alto**.

O molde antigo do motor era `.opts{max-width:400px}` + `.opt` **sem piso de
altura**: uma opção de uma linha media `400×55` = **7,3**. Consertei isso
**três vezes, na mão** — dentro de `escolher`, `completar` e `intruso` — cada
uma com o seu comentário explicando a mesma conta. A quarta peça com opções
repetiria o defeito, porque nada no motor a impedia.

**O que fica:** a conta subiu para o motor —
`.opts{max-width:360px}` + `.opt{min-height:62px}` → **360/62 = 5,8**.
As peças mantêm a regra delas porque também rodam **sozinhas**, fora do motor;
ali a duplicação não é remendo, é o preço de a peça ser autossuficiente.

**A lição, em uma linha:** *quando eu me pego consertando a MESMA conta pela
terceira vez em arquivos diferentes, o lugar dela não é o arquivo — é o
molde.* Medido: esteira 13/13 e leiaute 6 tamanhos × 38 telas seguem em 0 com
a opção mais alta, e o `provar_portoes.sh` ganhou os dois casos (a fita
reprova, o molde do motor passa).

---

## 🔎 A PROVA ACHOU UM PORTÃO CEGO — o artigo contraído (ago/2026)

Esta é a primeira vez que o `provar_portoes.sh` paga o preço dele sozinho, sem
o Marcos ter de ver o defeito primeiro.

O portão da **pergunta ambígua** existe por causa de uma cobrança dele: *"a
mesma coisa a ponte, fica confuso porque tem DUAS pontes"*, e o recado que
fecha, **"esses erros não podem passar"**. A regra dele é boa: pergunta no
definido singular (*a ponte*) declarando **duas zonas** é a própria tela
confessando que há duas na figura.

**O que ele não via:** a regra procurava o artigo **solto** — `a <b>ponte</b>`,
que é como o `_mapa` escreve. Só que a frase mais natural para uma criança é a
**contraída**: *"Toque **na** `<b>`ponte`</b>`"*, *"o telhado **da** `<b>`escola`</b>`"*.
Ali o "a" está grudado no "n"/"d" e **não tem fronteira de palavra antes dele**,
então o `\b` do regex não casava. O portão ficava cego justamente na forma que
eu mais escrevo.

**Conserto:** `(?:[nd]?[oa]|ao|à)\s+<b>` no definido, e as contraídas do
indefinido (`num`, `numa`, `dum`, `duma`) mais os coletivos (`dois`, `duas`,
`vários`, `cada`, `todos`) no lado que **libera** — porque quem grita à toa
ensina a ignorar portão. Medido nas três atividades que têm "ache na cena"
(`_mapa`, `_naveg`, `_padaria`): nenhuma virou alarme falso.

**A lição:** *plantar o defeito no formato REAL, não no formato que eu imagino.*
O meu primeiro fixture escrevia `n<b>a ponte</b>` — que não é como ninguém
escreve — e por isso quase me fez concluir que o portão estava certo. Antes de
acusar (ou absolver) um portão, conferir o defeito plantado contra uma
atividade de verdade.

---

## 🕶️ "35 TELAS" QUANDO SE MEDIU 10 — o portão cego pela METADE (ago/2026)

Este é o achado mais caro da noite, e ele estava impresso no relatório da banca
o tempo todo — eu é que lia o rodapé e não o meio.

O relatório da Padaria dizia, no fim: **"imagens conferidas em 35 telas"**. Vinte
linhas acima, **vinte e cinco** vezes seguidas: `(pulei pecaEscolher: não é
função)`. Ou seja: mediu **dez**. O mesmo valia para o portão do **contraste** —
o portão que o Marcos pediu com todas as letras (*"sempre verificar se não há um
contraste nas cores, para que não aconteça de a criança não conseguir
enxergar"*).

**Por que:** numa atividade montada pelo esqueleto as fases **não são funções
globais** — são fechamentos dentro de `MEC["nome"]`, e quem as desenha é o motor
(`montaFase(i)`). O detector de telas da banca procura `function nome(){ …
limpa() … }`, então ele *lista* os nomes que moram dentro das peças e não
consegue chamar **nenhum**. Tudo o que a criança vê depois da capa ficava fora
da conta.

**O conserto tem duas partes, e as duas importam:**
1. medir as fases pelo caminho de verdade — `montaFase(i)` para cada fase da
   lista `FASES`, que é exatamente como a criança as vê;
2. **contar e dizer o número.** "35 telas" quando se mediu 10 é o mesmo pecado
   do portão que roda cego: número que consola. Agora o rodapé diz
   `42 tela(s) (10 por nome + 32 fase(s) pelo motor)` — e, se não medir nada,
   **reprova** com "NÃO MEDI NENHUMA TELA — isto não é 'passou'".

### O que apareceu quando o portão abriu os olhos
**45 textos abaixo do mínimo WCAG na Padaria**, o pior a **1,95:1** ("A PALAVRA
É / PÃO" escrito direto sobre a estante). Nenhum era descuido: é um defeito de
**parentesco**. Na bancada a peça roda sobre um fundo LISO e escuro (`#2b2118`),
e ali o creme e o amarelo dela passam folgado; dentro da atividade o mesmo texto
cai sobre a **FOTO** — a madeira da padaria, o céu do observatório — e a razão
despenca.

**A regra que fica, na PONTE (vale para as 77 peças):** *rótulo, contador e
frase que ficam direto sobre o fundo ganham uma placa escura translúcida* — o
cartão já tem a dele. E: *quem muda o FUNDO de um botão tem que mudar a LETRA
junto* (o `.bclaro` do pintar ficou creme sobre creme, 1,24:1).

Medido depois do conserto: **421 textos em 42 telas, contraste 0**.

---

## 🎛️ AS DEZ MECÂNICAS QUE O PORTÃO NÃO ENXERGAVA (ago/2026)

A regra da casa (CLAUDE.md) diz: *"Mecânica nova = linha nova no
`_padrao/DINAMICAS.md` **e** regra nova no portão, no mesmo commit."* Fui medir
quantas das **77 peças** o `_qa/dinamicas.py` reconhecia: **67**. As outras dez
saíam com *"0 dinâmica reconhecida"* — o aviso existe e é honesto, mas **aviso
não pega defeito**.

Eram: `balanca`, `bussola`, `contadores`, `escrever-legenda`,
`experimento-justo`, `filtro`, `simetria`, `sombra`, `tabela`, `termometro`.

Cada uma ganhou regra, e o critério foi este: **a regra cobra o que a própria
peça aprovada já faz.** O gatilho é uma marca que só aquela mecânica publica, e
a cobrança sai da lista *"AS ARMADILHAS QUE ESTA PEÇA FECHA"* escrita no
cabeçalho dela. Assim a regra não inventa exigência nova — ela impede que a
**cópia** perca o que a original tinha certo, que é de onde vem quase todo
defeito nosso.

### E o erro que eu cometi escrevendo as regras (duas vezes, na mesma leva)
As minhas regras novas **reprovaram duas peças aprovadas** — e as duas
acusações eram falsas:

1. *"a balança não gira"* — a viga gira, mas pelo **JS**
   (`style.webkitTransform="rotate("+g+"deg)"`), e eu procurei `rotate` só no
   **CSS**;
2. *"o teste justo não tem trava"* — a trava é a **classe** `btn trava`, e eu
   procurei `\.trava`, com ponto, que só casa em seletor de CSS.

**A lição, que é a mesma de sempre vista de outro ângulo:** *onde a peça faz a
coisa certa e onde a regra olha têm que ser o MESMO lugar.* Regra nova se testa
**contra a peça aprovada** antes de entrar — se ela reprova quem já passou pelo
Marcos, a errada é a regra.

Medido depois do conserto: **77 peças, 0 reprovadas, 0 não reconhecidas**; e as
atividades montadas (`_padaria`, `_prova30`, `_jardim`, `_mapa`) seguem em 0.

---

## 📉 EU DIZIA "77/77" SEM TER RODADO — e duas peças estavam quebradas (ago/2026)

Repeti ao Marcos, em várias respostas, que **as 77 peças passavam na bancada**.
Era um número que eu tinha *herdado* das minhas próprias anotações e nunca
remedi nesta sessão. Rodei a bancada inteira: **74 passaram, 3 não.**

- **`intruso`** — na *janela baixa* (1024×420, que é o monitor da escola com a
  barra do navegador aberta) a tela "POR QUÊ?" tem selo + balão + **quatro**
  razões compridas + botão + dica, e a última razão ficava **presa atrás da
  barra de baixo, sem rolagem**. A criança não via que existia uma quarta
  opção — e é ali que mora a resposta em metade das rodadas. Conserto copiado
  da peça `escolher` (a lista rola por dentro, com o vão saindo de um `calc` da
  tela, nunca de um número escolhido a dedo).
- **`linha-do-tempo`** — no 3º tropeço o andaime revela: escreve *"Era este! Eu
  coloco e você segue de onde parou"* e põe a peça. Só que **pôr a peça passa
  pelo caminho do acerto, que apaga a dica** — a frase aparecia e sumia no
  mesmo pisco. A criança que mais precisava da explicação era a única que não
  conseguia ler a dela. Agora a revelação **segura a dica por 4 segundos**.
- **`experimento-justo`** — este era falso: reprovou por causa de uma regra
  **minha**, escrita com o portão no meio da corrida.

### As duas lições, que valem mais que os consertos
1. **Número herdado não é número medido.** Um "77/77" repetido de memória tem a
   mesma cara de um medido — e foi assim que dois defeitos ficaram semanas sem
   quem os pegasse. Antes de afirmar que passou, **rodar**.
2. **Não se edita um portão com a bancada correndo.** Metade das peças rodou
   com a regra velha e metade com a nova, e eu quase abri um chamado contra uma
   peça aprovada. Portão muda com a bancada **parada**; depois roda tudo de novo.

Medido depois, e desta vez do jeito certo — **bancada parada, varredura inteira**
(3 por vez, as 77 peças do zero): **77 de 77, código 0, nenhuma reprovada.**
É este o número que vale; o anterior era herdado.

---

## 🪜 A REVELAÇÃO QUE SUMIA — e o que a cobertura do andaime realmente rendeu

**O buraco:** depois da varredura limpa fui ver *como* cada portão mediu cada
peça. O do **andaime** — o mais pedagógico da bancada, o que erra de propósito
para ver se a criança consegue seguir — dizia **"NÃO SEI JOGAR" em 47 das 77**.
A bancada dava "PEÇA PRONTA" do mesmo jeito, porque portão sem receita não
reprova: ele avisa. Mas 47 andaimes estavam sem quem os medisse.

**O que eu tentei:** um gesto genérico apoiado na convenção da casa (o que a
criança deve tocar publica `data-qa="1"`, o resto `"0"`), mais o "deslizar para
o valor errado".

**O que realmente rendeu — e aqui o número honesto importa:** de 30 peças
medidas para **31**, e de 47 cegas para **45**. Quase um empate. O gesto novo
não é a chave que eu imaginei: a maioria das 45 restantes erra de um jeito que
nenhum atalho genérico produz (desenhar o traço errado, escrever a palavra
errada, montar o circuito errado). Para essas, o caminho é **receita própria**,
uma a uma — trabalho que fica anotado, não resolvido.

**E o estrago que eu fiz no meio:** pus o gesto novo **na frente** dos
específicos. Nas peças de arrastar ele passou a clicar num alvo qualquer em vez
de levar a peça à vaga errada, e **cinco peças que estavam em 0 passaram a
reprovar**. Consertado pondo o genérico como **último recurso**.
> **Regra: gesto novo entra por ÚLTIMO.** Atalho geral posto na frente do
> específico não amplia cobertura — rouba o lugar do que já funcionava.

**O que a cobertura nova pagou (e valeu):** apareceu um defeito de **família**,
o mesmo em duas peças. No 3º degrau o andaime revela: escreve *"Era este! Eu
coloco e você segue"* **e põe a peça**. Só que pôr a peça passa pelo caminho do
acerto, que chama `apagaDica()` — a frase aparecia e sumia **no mesmo pisco**.
A criança que mais precisava da explicação era a única que não conseguia ler a
dela. Consertado na `linha-do-tempo` e na `ordenar` (a dica fica 4 segundos), e
o `_qa/dinamicas.py` ganhou um **aviso** para as outras 10 peças da mesma
família — aviso, não reprovação, porque só o navegador sabe se ali o revelar
também avança a fase.

---

## 🪜 A COBERTURA DO ANDAIME — de 30 para 45 peças medidas (ago/2026)

Continuação da nota acima. O primeiro gesto genérico que escrevi rendeu quase
nada (30 → 31 peças medidas) e eu quase parei por aí. Fui abrir as 45 cegas no
navegador, uma a uma, e o problema era a **minha premissa**:

> eu supunha *"a certa publica `data-qa="1"` e as erradas `"0"`"*. A maioria das
> peças publica **só o alvo certo** — todos os `data-qa` visíveis valem `"1"` —
> ou usa o campo para guardar a resposta (`"GATO"`, o nome da carta.) **Não
> havia nenhum `"0"` para clicar.**

A pergunta certa não era *"qual é a errada?"* e sim **"o que dá para tocar que
não é o alvo marcado?"** — que é o que a criança faz quando erra: vira a carta
que não forma par, pisa na parede, pinta o quadrado vizinho.

**Resultado medido:** **45 peças medidas** (eram 30), **30 sem medição** (eram
47). O que sobra erra de um jeito que nenhum atalho produz — traçar o caminho
errado, escrever a palavra errada, montar o circuito errado — e para essas o
caminho é **receita própria, uma a uma**. Fica anotado.

### As três armadilhas do próprio portão, todas pagas nesta rodada
1. **Gesto novo entra por ÚLTIMO.** Pus o genérico na frente do específico e
   cinco peças que estavam em 0 passaram a reprovar.
2. **A revelação que some.** Onde revelar TAMBÉM avança a fase, o `apagaDica()`
   do acerto apagava a explicação no mesmo pisco (`linha-do-tempo`, `ordenar`).
3. **Instrução de ordem não é erro.** O `bingo` e o `pintar-desenho` reprovaram
   com "1 de 3 dicas" porque o gesto tocou o tabuleiro sem fazer o passo 1, e a
   peça respondeu três vezes *"Primeiro tire uma pedra…"*. Isso é a peça
   ensinando a ORDEM, e repetir ali está certo. Agora o portão reconhece esse
   formato e diz **que não mediu**, em vez de reprovar.

O fio comum das três: **um portão que produz a condição errada mede outra coisa
— e o que ele mede parece defeito da peça.**

---

## 🧩 AS QUATRO DE DOIS PASSOS — e o que o veredito do andaime mede em cada caso

Mais quatro peças saíram da cegueira do portão do andaime: `bingo`,
`pintar-desenho`, `memoria` e `contadores`. Nenhuma era "difícil": todas exigem
**fazer o passo 1 antes de poder errar** (tirar a pedra, pegar a tinta, virar a
primeira carta, pôr as sementes). O gesto genérico tocava o tabuleiro direto e a
peça respondia, com razão, *"Primeiro tire uma pedra"* — instrução de ordem, não
erro. Receita própria resolve: faz o passo 1 e **só então** erra.

⚠️ **A minha primeira receita de `contadores` reprovou a peça** — eu apertava "+"
nove vezes achando que passar do número era erro. Não é: a criança pode tirar
sementes à vontade, e a peça só confere quando ela aperta **"Contar comigo"**.
Recibo do de sempre: *gesto que a peça não considera erro não mede andaime
nenhum*.

### O que o veredito significa (as duas leituras do mesmo portão)
Vale saber ao ler o relatório, porque **não é a mesma medida**:

- **Com receita GENÉRICA** → o veredito é o **andaime**: pelo menos duas ajudas
  diferentes em três erros. A medalha fica inconclusiva (a genérica sabe errar,
  não sabe resolver).
- **Com receita PRÓPRIA** → o veredito é **"não trava"**: depois de errar três
  vezes, dá para chegar à medalha. O crescimento do andaime aparece no relatório
  ("3 de 3"), mas não entra no veredito.

As duas são legítimas e nasceram de defeitos diferentes; o que não pode é
confundi-las ao ler o número.

### E o teto do acabador: 2 era pouco, 6 é o medido
O guarda que faz o acabador desistir do alvo marcado (posto para escapar do laço
da `ouvir-achar`) estava em **2 cliques seguidos** — e isso quebrou a
`contadores`, onde fechar a fase exige apertar **"+" várias vezes no mesmo
botão**. Ela reprovou três vezes seguidas por "MEDALHA: NÃO", que era o auditor
desistindo, não a peça travando. Com o teto em **6**, as duas passam, e passam
sempre (medido três vezes cada). *Todo número mágico num portão precisa do caso
que o justifica dos DOIS lados.*

### O placar do andaime, com a distinção que importa (ago/2026)

Varredura final das 77 peças, depois de nove receitas próprias novas e de quatro
consertos no próprio portão:

| | |
|---|---|
| peças **medidas** (o portão conseguiu errar e julgar) | **67** (eram 30) |
| **reprovadas** | **0** |
| sem medição (ele diz que não mediu) | **10** |
| das medidas, quantas exercitaram os **três** erros | **33 ± 1** (oscila, ver abaixo) |

Esse último número é o que vale como medida FORTE — "o andaime cresce a cada
erro". Nas outras 28 o veredito é o mais fraco, "não trava": a criança erra e
ainda assim consegue chegar ao fim. As duas contam, mas **não são a mesma
coisa**, e somá-las num número só seria inflar o placar.

### Uma peça pode sair de "medida" para "não medi" entre uma corrida e outra
Aconteceu com a `ditado`: numa corrida ela deu *3 de 3*, na seguinte caiu em
"não medi". Não é defeito — é o guarda funcionando. A receita genérica sorteia
em qual letra errada toca, e algumas tentativas não são erro; quando isso
acontece, o portão prefere dizer que **não mediu** a arriscar uma reprovação por
azar. O número de "medidas" oscila um ou dois para cima e para baixo por isso, e
está certo que oscile: o que **não** pode oscilar é a reprovação.

### As 10 que sobram, e por que ficam assim
`andar-ate` · `camadas-mapa` · `caca-palavras` · `criar-desafio` ·
`ensinar-mascote` · `escrever-legenda` · `mudanca-permanencia` ·
`prever-observar` · `quem-sou-eu` · `passo-a-passo`.

A maioria é mecânica de **criação** ou de **previsão**: ali "errar de propósito"
não é um clique, é **escrever** ou **prever** alguma coisa, e o auditor teria
que inventar conteúdo para produzir o erro. Nas outras (`caca-palavras`,
`camadas-mapa`) a peça simplesmente **não pune** — marcar letras que não formam
palavra não gera erro nenhum, por decisão pedagógica.

**Não vou forçar receita nessas.** Receita que finge erro mede o nada — e o
portão, achando que mediu, um dia reprova peça boa. Aconteceu duas vezes num só
dia (a `contadores` e as seis do `ReferenceError`). O honesto é o portão dizer
**"não medi"**, que é o que ele faz.

---

## Três lições do Jardim do Broto (ago/2026)

### 1. Código 2 é "não medi" — e a própria banca lia como reprovação
A casa tem três códigos (0 passou · 1 REPROVOU · 2 não consegui medir) e essa
distinção é o coração do QA. Mesmo assim o `auditar.sh` fazia
`if [ "$st" != "0" ]; then FALHOU=1`. Resultado: o portão do alto-falante da
resposta, que sai com **2** nas atividades **escritas à mão** (elas não têm o
motor de `FASES` para percorrer), derrubava a atividade inteira dizendo
literalmente "NÃO MEDI". Reprovar por não ter medido é o contrário do que o
código 2 significa, e ensina a ignorar a banca — que é o pior estrago possível.
Agora o 2 vai para a lista dos **CEGOS**, que aparece no fim; 1 (ou estouro)
reprova. **Regra:** portão novo que sabe dizer "não medi" só serve se quem o
chama souber ouvir.

### 2. A mesma frase se grava de DOIS jeitos
- atividade **montada** pelo esqueleto → a chave é a **conta** do texto
  (`op_<chaveVoz(balão)>.mp3`), porque o balão é gerado;
- atividade **escrita à mão** → a mesma frase é gravada com **nome próprio**
  (`jd_abertura`) e a tela chama `falar("jd_abertura")`.

O `fala_o_escrito.js` só conhecia o primeiro e acusou **24 fases de mudas** —
todas falam perfeitamente. É a mesma família do erro que já estava escrito no
topo daquele arquivo: portão que mede pelo mecanismo errado fica **cego para o
certo e barulhento para o errado**. A pergunta honesta não é "o id bate?", é
**"a criança OUVE o que está escrito?"** — então o índice guarda também o TEXTO.
Duas provas novas na bancada fecham os dois lados.

### 3. Botão fixo na tela = trava do segundo toque
Fase com botões que **não somem** entre uma rodada e outra (os dois latões do
"a planta precisa disto?", o Sim/Não, o Certo/Errado) tem duas janelas em que um
segundo toque cai no vazio: os ~480ms de troca da figura, e o intervalo depois
da **última** figura enquanto o banner não abriu. Sem trava, a função roda com o
índice fora da lista e estoura — no colo da criança isso é o app congelado no
meio da fase. **Padrão:** `if(trava) return; var it=lista[i]; if(!it) return;
trava=true;` e só liberar quando a próxima rodada entra. O portão que pegou foi
o **jogador**, que clica rápido e repetido como criança de 6 anos clica.

---

## 🪜 O ANDAIME MEDIDO: de 31 para 67 (ago/2026) — e os falsos "passou" que apareceram no caminho

Número anterior registrado aqui: **31 peças medidas, 45 cegas**. Medido agora,
bancada parada, varredura inteira das 78 peças, três vezes seguidas:

| | antes | depois |
|---|---|---|
| medidas e **aprovadas** | 31 | **67** |
| **reprovadas** | 0 | **0** |
| "não medi" | 45 | **11** |

*(O número passou por 67 antes de assentar em 63: aquele 67 ainda contava peças
que passavam tendo errado **uma ou duas** vezes, não três. Errar menos de três
vezes é teste pela metade — agora sai "não medi". O 63 é o número verdadeiro.)*

Receitas próprias novas: `ligar`, `digitar`, `quem-sou-eu`,
`mudanca-permanencia`, `ensinar-mascote`, `prever-observar`, `girar`.

### Os cinco consertos, todos da MESMA família
O padrão que se repetiu — e que vale mais que os consertos — é o auditor
**confessando o próprio limite com cara de veredito sobre a peça**:

1. **Medir cedo demais.** A `ensinar-mascote` erra de forma *encenada* (o
   mascote anda, obedece a regra, e só depois de 1,2s o mundo mostra que não
   deu certo). O auditor olhava a tela 500ms depois do clique e concluía "não
   houve erro". Agora ele **espera a ajuda aparecer**, até 3,5s.
2. **Medir o rastro velho.** Com a espera, ela passou a mostrar a *mesma* ajuda
   três vezes: os cliques 2 e 3 caíam com a cena ainda animando, a peça os
   ignorava, e o que estava na tela era a ajuda do erro 1 — relida como se
   fosse nova. Agora a dica velha é **apagada antes de cada tentativa**.
3. **Gastar as tentativas andando.** A `prever-observar` só tem erro na terceira
   tela (o palpite, por decisão pedagógica, nunca é erro). Cada tentativa agora
   **insiste até quatro voltas** antes de desistir.
4. **A receita própria que nunca aprendeu a apertar "Começar".** A genérica
   tinha esse passo desde o primeiro dia; a própria, não. Quatro peças abriam
   numa capa e a receita voltava `null` para sempre. E ao andar, o auditor
   clicava no "Continuar" do `#banner` **fechado** em vez do botão de verdade —
   agora o alvo marcado com `data-qa="1"` vem primeiro, e nada dentro de banner
   fechado conta.
5. **Chegar na medalha sem nunca ter errado.** Com receita própria o veredito é
   "não trava" — então uma receita que nunca erra **passava**. Seis peças
   estavam assim (`decisao`, `girar`, `misterio`, `repartir`, `teia-alimentar`,
   `termometro`): aprovação vazia. Agora **zero erro sai com código 2**.

### Um defeito de verdade e uma mecânica que não tem erro
- **`digitar`** — terceira da família da *revelação que some*: o 3º degrau
  escreve *"Era esta! Eu coloco e você segue"* e chama `revela()`, que põe a
  letra pelo caminho do acerto e **apaga a dica no mesmo pisco**. Conserto já
  validado nas outras duas: `seguraDica(4000)`.
- **`decisao`** — aqui **não existe erro**, e está escrito no coração da peça:
  *"Nada de 'você errou': a consequência é a resposta"*. É simulador de
  consequência. Minha receita clicava na decisão ruim e **anunciava um erro que
  a peça não comete** — inventar a condição que se quer medir é pior que não
  medir. Devolvendo `null`, o portão diz "não medi", que é a verdade.

### As que continuam sem medida, e por quê
`andar-ate` · `caca-palavras` · `camadas-mapa` · `criar-desafio` ·
`escrever-legenda` · `misterio` · `passo-a-passo` · `repartir` · `termometro`
(+ `MOLDE`, que é gabarito, e `decisao`, que não tem erro).

Três motivos honestos: mecânica de **criação** (errar seria escrever ou desenhar
uma coisa errada, não um clique); peça que **não pune** por decisão pedagógica
(`caca-palavras`, `camadas-mapa`); e o `passo-a-passo`, cujo erro só existe
**depois de executar a receita inteira** — uma animação de vários segundos que
uma tentativa de auditor não alcança. Receita que finge erro mede o nada; o
honesto é o portão dizer **"não medi"**.

### ⚖️ Até onde esta medida chega — o limite dito com todas as letras
O portão do andaime lê a ajuda em **um lugar só: o `#dicaP`**. Tentei fazer a
receita própria reprovar por "ajuda que não cresceu", como a genérica já faz, e
a varredura acusou **oito peças de uma vez** — entre elas a `quem-sou-eu`, cujo
andaime é a **pista nova** que aparece a cada erro, num quadro próprio. Teria
sido o erro desta série inteira mais uma vez: medir pelo mecanismo errado e
chamar de defeito da peça. Recuei.

**A linha que ficou:** com receita própria, "ajuda que não cresceu" é **aviso**,
e o veredito continua sendo *"não trava"*. Reprovar por andaime parado segue
valendo na genérica — foi assim que a `linha-do-tempo` e a `ordenar` caíram, e
as duas provas da bancada continuam vendo o portão reprovar o andaime parado e
aprovar o que cresce.

**O que fica anotado, não resolvido:** enquanto o portão não souber ler ajuda
fora do `#dicaP` (pista nova, fala do mascote, consequência no mundo), esse
avanço não pode virar reprovação. Alargar essa leitura é o próximo degrau —
e tem que nascer com prova, como todos os outros.

### 👀 A MEDIDA AMPLA — "apareceu ajuda nova na tela?", sem chutar nome de elemento
O degrau anotado acima começou a ser construído. Em vez de procurar `#dicaP`
(ou `.pistas`, ou `.fala` — mais nomes para chutar), o portão agora **guarda
todo o texto visível da tela antes do erro e conta o que apareceu depois**. É
mecanismo-independente: serve para dica, pista nova, fala do mascote ou
consequência no mundo.

Medido lado a lado: a `quem-sou-eu` dá **2 de 3** na medida estreita e **3 de 3**
na ampla — ou seja, a ampla enxerga exatamente a ajuda que a estreita perdia.

**Ela nasce como RELATÓRIO, não como veredito**, e com prova nos dois sentidos
(`provar_portoes.sh`, casos 23): vê a ajuda que mora fora do `#dicaP`, e **não
inventa** ajuda numa tela que não mudou. Promover a veredito exige antes uma
varredura inteira sem falso alarme — a lição do "oito peças de uma vez" está
fresca.

**Dois tropeços do caminho, que valem por si:**
- O filtro "só as folhas" (`children.length===0`) pulava justamente o `#dicaP`,
  que quase sempre tem um `<b>` dentro. A medida nova nascia **cega para a ajuda
  mais comum da casa**. Certo é contar quem só tem tags de texto dentro.
- A primeira prova acusou o portão de cego — e o defeito era **do meu caso de
  teste**, que repetia a última pista. Peça de mentira também precisa ser lida
  com cuidado: acusar o portão por defeito da prova é o mesmo erro, do outro
  lado do balcão.

### 🧠 Uma peça pode ajudar em outro RITMO — e isso não é andaime parado
A `memoria` erra três vezes e não mostra ajuda nenhuma, nas duas medidas. Não é
defeito: o andaime dela é a cada **6** tentativas sem par (`if(n%6!==0) return`),
porque jogo de memória que socorre a cada erro vira cola. O auditor erra só três
vezes, então nunca alcança o degrau. Fica o **aviso**, sem reprovação — e a
anotação de que "cadência do andaime" é uma dimensão que o portão ainda não
mede.

### 🎨 A MECÂNICA QUE NÃO PUNE — e por que esse teste é de RUNTIME
A `pintar-desenho`, a `estimar` e a `decisao` **definem `sErro()`** (vem do
MOLDE) e **nunca chamam**: pintar é livre, estimar é palpite, decidir tem
consequência e não correção. São escolhas pedagógicas legítimas — "errar não
pune" é regra da casa — mas ali **não existe erro para o andaime socorrer**.
Sem reconhecer isso, cada uma custava a mesma descoberta duas vezes: eu escrevia
uma receita, ela "errava", nenhuma ajuda aparecia, e eu ia procurar defeito numa
peça certa. E pior: **receita que anuncia um erro que a peça não comete inventa
a condição que se quer medir**.

**O tropeço, que é a parte que importa:** escrevi isso primeiro como leitura do
**arquivo** — "não chama `sErro` ⇒ não pune". A primeira coisa que a regra fez
foi **desligar a `balanca`**, que cinco minutos antes media 3 de 3. Ela socorre
em três degraus **sem tocar o somzinho de erro**, de propósito: *"desequilíbrio
não é erro: ninguém é corrigido por estar torto"*. **Não tocar o som não quer
dizer não ajudar.**

A conclusão só vale com as duas coisas juntas, e a segunda é medida: a peça
nunca pune **E**, depois de três tentativas, não apareceu ajuda em nenhuma das
duas leituras (piso "menos de duas" na ampla, porque nem todo texto novo é
ajuda — na `estimar` o que aparecia era o rótulo "O SEU PALPITE", mobília da
tela).

### 🧮 Onde o número parou: **61 medidas · 0 reprovadas · 17 "não medi"**
Ele desceu de 63 porque três peças saíram do "aprovado" para o "não medi" —
`pintar-desenho`, `estimar` e `memoria` —, e isso é o portão ficando mais
honesto, não pior. Em compensação `balanca` e `bingo` entraram: as duas
mediam ZERO e tinham o andaime **completo**, e o defeito era da receita nos
dois casos.
- **`balanca`** protege o peso que já veio posto (`if(d<0 && add<=0) return`):
  na configuração em que o lado pede MAIS, apertar "− tirar" não faz nada. O
  "erro" da receita virava clique perdido — ali a criança **não consegue
  piorar**. A receita agora põe um peso antes e só então tira.
- **`bingo`** precisa de um passo CERTO antes de poder errar (tirar a pedra
  para depois marcar a casa errada). A receita devolvia `null`, o auditor
  entendia "não achei nada" e **andava sozinho clicando no alvo marcado — que
  ali é a casa certa**. Nasceu o sinal **`#andei`**: *"dei um passo, não ande
  por mim"*.

### 🔁 A regra que jogava fora a prova que tinha na mão
`comparar`, `filtro` e `trilha` mostraram os **três degraus do andaime
crescendo**, ajuda diferente a cada erro, e chegaram na medalha — e mesmo assim
saíram **"não medi"**, só porque uma das três tentativas não contou como erro na
minha contabilidade.

"Teste pela metade" tem que ser sobre **não ter visto o andaime**, não sobre a
aritmética das tentativas. Quem viu a ajuda crescer duas ou três vezes **mediu**.
É o avesso do erro que esta série toda combateu — em vez de aprovar sem prova,
eu estava recusando a prova que tinha na mão —, mas erro igual. Agora:
`errosReais < 3` **e** nenhuma ajuda vista ⇒ "não medi"; ajuda vista ⇒ o
veredito vale.

### 🔢 Contador não é socorro
O `andar-ate` parecia socorrido três vezes por um **placar andando**: "passos
dados: 2" virava "passos dados: 4" e a medida ampla contava as duas como
novidade. Guardando cada frase com os números trocados por `#`, ela só conta
como nova quando as **palavras** mudam. O `andar-ate` caiu de 3 para 1 na medida
ampla — e continua aprovado pelo `#dicaP`, que é onde a ajuda dele de fato mora.

### 🧮 Onde o número parou: **67 medidas · 0 reprovadas · 11 "não medi"**
Receitas novas desta rodada: `escrever-legenda` (o tropeço é publicar um texto
curto demais — a genérica não sabia digitar num campo) e `andar-ate` (o tropeço
não é clique errado, é o **caminho perdido**: a peça socorre em 4, 8 e 12 passos
a mais).

As 11 restantes, com o motivo de cada uma: `MOLDE` (gabarito) · `decisao`,
`estimar`, `pintar-desenho` (**mecânicas que não punem**) · `memoria` (andaime
com cadência de 6 tentativas) · `caca-palavras`, `camadas-mapa` (**não punem**
por decisão pedagógica) · `criar-desafio` (criação: errar seria escrever) ·
`passo-a-passo` (o erro só existe depois de executar a receita inteira, uma
animação de vários segundos) · `repartir`, `teia-alimentar` (a receita ainda não
consegue os três erros).

---

## 🚨 O JOGADOR PARAVA NA 3ª FASE DE 32 E DIZIA "CHEGUEI AO FIM" (ago/2026)

O defeito mais grave que esta fábrica já teve, e estava escondido **dentro do
portão que existe justamente para achar criança presa**.

Cada peça do catálogo é uma mini-atividade que termina na **própria medalha** —
tela "PEÇA FECHADA", `div.medal`, botão "Jogar de novo". O jogador reconhecia o
fim por `document.querySelector('.medal')`. Dentro da atividade montada ele via
a medalha **da peça** na terceira fase, dava a partida por encerrada **com
código 0**, e as 29 fases seguintes **nunca foram jogadas por ninguém**. Todas
as atividades montadas passaram assim.

**Como apareceu:** rodei a banca completa na Padaria (montada pela máquina, com
arte e voz) só para provar a esteira ponta a ponta. Ela passou — e no log do
jogador estava escrito *"CHEGOU NO FIM"* com a barra em **50%**. Um número que
não fecha vale mais que um "passou".

### O que estava atrás dessa porta

1. **BECO SEM SAÍDA NA FASE — e este chegaria na criança.** Trinta das 78 peças
   chamam `fimDaPeca()` **direto**, sem passar pela ponte do `mostraBanner`. Na
   atividade montada isso leva a criança para a tela de **bancada** da peça
   ("PEÇA FECHADA", *"esta é a peça O INTRUSO"*), cujo único botão é **"Jogar de
   novo"**. Ela termina a fase 3 de 32 e só pode recomeçar a **mesma** fase.
   Para sempre. Conserto no integrador: `fimDaPeca` é **reapontado para a
   continuação do motor** antes de a peça começar.

2. **O auditor cego pelo NOME DA CLASSE.** O integrador **renomeia** as classes
   que colidem com o motor (`.grade` → `cp_grade`), e o jogador procurava pelos
   nomes antigos: o solucionador do caça-palavras não achava a grade e ele dava
   "PRESO" numa fase que a criança fecha. Agora acha pelo **conteúdo** do
   `data-qa`, e `[data-qa]` entrou na lista de alvos. **Nome de classe a fábrica
   troca; o `data-qa` não** — ele existe justamente para o auditor.

3. **DESENHO NÃO É TEXTO.** O esboço marcava as linhas do labirinto como texto a
   trocar: `"S..#."` virava `«.#X.F»` — **sete casas em vez de cinco**, a grade
   desalinhava, o caminho até a estrela deixava de existir. Fase **sem saída**,
   sem erro de JS, sem aviso nenhum. Agora string feita só de símbolos de mapa é
   tratada como estrutura.

**Medido:** na `_prova30`, de **3 fases jogadas para as 32**, chegando à medalha
do motor. `ESTEIRA=0` com o jogador percorrendo a atividade inteira.

### As duas regras que ficam
- **Fim de atividade é a medalha DO MOTOR** (`img` com `med_<prefixo>`), nunca
  qualquer `.medal`. Sem motor de fases (bancada da peça avulsa), aí sim vale
  qualquer uma — é o que sempre valeu ali.
- **Auditor não procura por nome de classe.** Nome, a fábrica troca; contrato
  (`data-qa`), não. Toda vez que eu acrescentava mais um nome à lista, resolvia
  UMA peça e deixava a próxima igual.

### ✅ O conserto provado no caso real (ago/2026)
Não basta a `_prova30` passar: ela é fixture. Remontei **a Padaria** (a atividade
que tem o beco no ar) a partir do `conteudo.json` dela, numa **cópia**, com a
fábrica corrigida — sem tocar na pasta publicada:

| | antes | depois |
|---|---|---|
| `_qa/beco.py` | **8 fases** que viram beco | **0**, saída ok |
| jogador automático | parava na 3ª fase dizendo "cheguei ao fim" | **21 fases fechadas, medalha, código 0** |

E a varredura das atividades: **só a Padaria** tem o defeito. `_mapa` e `_jardim`
são escritas à mão (não usam peça de catálogo) e o portão diz "não medi" nelas,
que é a verdade.

**A banca completa na cópia saiu 1, e o motivo é o teste, não a atividade:** o
único portão que reprova é o da **arte própria**, e ele está comparando a cópia
com a Padaria de onde ela veio — as imagens são byte a byte iguais *por
construção*. Uma cópia não tem como passar nesse portão. Todos os outros passam,
inclusive o do beco e o do jogador. Quando a pasta publicada for remontada no
lugar (se o Marcos autorizar), a comparação volta a ser contra as OUTRAS
atividades e o portão fecha como sempre fechou.

### 🔊 O buraco que o jogador cego escondia: 14 falas sem voz
O `colher.py` — o portão que confere **a voz da rodada** (banca 0f2) — usa o
próprio `_qa/jogador.js`. Ou seja: enquanto o jogador parava na 3ª fase, **a
colheita também parava ali**. O portão dizia *"nada a acrescentar: a voz já
cobre o que aparece jogando"* tendo visto **3 fases de 32**.

Medido agora, na Padaria remontada: **219 textos vistos em jogo, 14 falas sem
voz gravada**. São dicas de andaime — *"A letra que vem agora está piscando"*,
*"Dica: uma das cartas fala de bolo"*, *"Era esta! Eu coloco e você segue"*. É o
**pilar sonoro** com furo, justamente nos degraus de ajuda, que é onde a criança
que não lê mais precisa da voz.

**Duas correções no próprio colher, achadas nessa medição:**
- **Colagem que não muda a caixa.** O filtro pegava `"BBOLOjá tentamos"` pela
  mudança de maiúscula/minúscula sem espaço, mas deixava passar
  `"As outras três terminam com o mesmo som.é esta"` — duas coisas da tela
  juntadas no **ponto final**. Escrita de verdade não tem ponto grudado em
  minúscula. (As reticências ficam de fora: *"o jardim está vazio... vem me
  ajudar"* é uma frase só.) Passaram de 35 para 39 descartes corretos.
- **Relatório que se deixa ler errado.** As duas listas saíam **grudadas** — as
  descartadas e, logo abaixo, com o mesmo recuo e sem título, as novas. Li a
  minha própria saída e conclui que frases boas estavam sendo jogadas fora.
  Relatório ambíguo custa o mesmo que medição errada: leva a consertar o que não
  está quebrado. Agora as falas a gravar têm título e vêm com `+`.

### ⛔ E o portão da voz da rodada estava APROVANDO com o furo na mão
Achado logo depois: o `colher.py --so-ver` — o modo que a **banca** usa (portão
0f2) — saía com **código 0 mesmo listando 32 falas sem voz**. A banca lia "ok" e
seguia. É a mesma lição que já está escrita aqui para outro portão: **portão que
não reprova não é portão, é comentário**.

Estava escondido em camadas: enquanto o jogador parava na 3ª fase, a lista vinha
vazia e ninguém via o problema. Consertado o jogador, a lista encheu — e o portão
continuou aprovando.

**Agora, no modo de conferir, fala faltando REPROVA**, e o recado diz o caminho:
rodar o colher sem `--so-ver` (ele grava no `falas.json`) e montar de novo.

**E converge — medido, não suposto.** As dicas de andaime **sorteiam** de que par
falam ("uma das cartas fala de *chuva*" / de *abelha*), então uma rodada só não
cobre tudo. Na `_prova30`: **32 → 2 → 0** em dois ciclos de
`colher → montar`. O portão fecha; não vira bloqueio eterno.

**A receita, para não se perder:** `montar` → `colher` → `montar` → `colher`
→ `montar` → `auditar`. Duas voltas de colheita, e a segunda é barata.

### 📐 O portão do LEIAUTE nunca tinha medido uma fase de atividade montada
Mesma família do jogador cego, e escondida atrás de um número que **parecia**
cobertura.

O `_qa/leiaute.js` — o que mede *"cabe na tela? dá para tocar?"*, o que pegou a
opção presa atrás da barra e o alvo pequeno demais — só sabe abrir tela **pelo
nome** (`window[t]()`). E as 32 fases de uma atividade montada **não são funções
globais**: quem as desenha é o motor, com `montaFase(i)`.

Pior: a lista de telas que a banca passa incluía as **funções internas das
peças** — o integrador inlina o corpo da peça na coluna zero, então
`^function pecaIntruso(` casa com o detector. Para todas elas `window[t]` é
`undefined`, e o portão **pulava em silêncio**. Ele imprimia *"6 tamanhos x 38
telas"*: 38 era a conta dos nomes **tentados**, não das telas medidas. Das 38,
**28 eram pulos**; nenhuma das 32 fases era vista.

Dois consertos:
- **O portão anda pelo motor**, como o `contraste.js` e o `imagens.js` já faziam,
  e o relatório diz o número honesto: *"42 tela(s) (10 por nome + 32 fase(s) pelo
  motor)"* — e quantas ele **não conseguiu abrir**.
- **A lista de telas da banca deixa de fora o que está dentro de um `MEC[...]`.**
  Caiu de 38 nomes para **7 reais**, e sumiram 168 aberturas de página inúteis
  (28 nomes × 6 tamanhos) só no leiaute.

**Medido depois:** o leiaute abre 39 telas (7 por nome + 32 fases), **zero
pulos**, e continua aprovando a `_prova30` — nenhum alarme falso.

**A regra que fica, e vale para portão novo:** *número que parece cobertura tem
que ser o que foi MEDIDO, nunca o que foi tentado.* Se o portão pulou, ele diz
quantas — pulo em silêncio é o começo de toda aprovação vazia.

**E o `encaixe.js` tinha a mesma cegueira**, achada na mesma varredura: ele mede
figura esticada, cortada ou perdida dentro da caixa dela — e também só abria tela
por nome. Numa atividade montada **nunca tinha olhado uma figura de fase**. Agora
anda pelo motor e reporta *"38 tela(s) (6 por nome + 32 fase(s) pelo motor)"*.

**Um achado de mentira que sumiu junto:** `montaFase` chama `limpa()`, então
entrava na lista como se fosse uma TELA — e os portões a chamavam **sem índice**.
O motor desenhava um estado indefinido e o encaixe acusava
*"montaFase | .medal ocupa só 10% da caixa dela"*: um defeito que não existe, numa
tela que não existe. Ela é a **desenhista** das fases, não uma fase. Saiu da lista
(junto com `montaBarra` e `limpa`, pela mesma razão).

### 🕳️ DOIS PORTÕES QUE NUNCA RODAVAM — e um achou defeito na primeira corrida
Varrendo os portões de navegador atrás da cegueira do leiaute, apareceu coisa
pior que portão cego: **portão que não roda**.

O `_qa/vaza.js` (*"o conteúdo cabe dentro do próprio cartão?"*) e o `_qa/zonas.js`
(*"a zona de 'ache na cena' aponta para o lugar certo?"*) **não estavam em lugar
nenhum** — nem na banca, nem na bancada da peça, nem na esteira. Só rodavam se
alguém lembrasse de digitar o comando. E o `vaza` nasceu de uma reclamação do
Marcos: *"o dizer da figura fica fora do quadrado branco, ficou feio"*.

**Ligado na banca, achou na primeira corrida** — na fixture da própria fábrica:
o **alto-falante escapando 18px para fora do cartão** da `arrastar-lugar`, nas
fases 8 e 24, em **todos os quatro tamanhos de tela**.

**A causa e o conserto certo.** A peça desenha um cartão de tamanho FIXO
(74×70px). O motor põe dentro dele o alto-falante da resposta (30px + 8px de
margem), porque `.pc` está na lista das respostas tocáveis — e o botão sobrava.
Encolher o alto-falante seria o conserto errado: ele é alvo de dedo de criança e
já está no mínimo. Quem tem de ceder é o cartão. Na ponte:
`.centro .pecabox .pc:has(> .zap){width:auto;height:auto;min-width:74px;
min-height:70px}`, com queda para o Chrome 109 da escola, que não tem `:has()`.

Medido depois: **128 telas em 4 tamanhos, zero vazamentos**, e a esteira em 0.

**A regra que fica:** *portão que não roda não é portão — é um arquivo.* Portão
novo entra na banca (ou na bancada da peça, ou na esteira) **no mesmo commit** em
que nasce. Ficou faltando o `zonas.js`, que precisa de fase e rodada como
argumento; ele fica anotado aqui até ganhar um jeito de se achar sozinho.

---

## 🎞️ AS ANIMAÇÕES DE 60 PEÇAS MORRIAM NA ESTEIRA — e nada reclamava

**O que aconteceu (ago/2026).** Redesenhando a `ligar-pontos` para o Marcos
(*"tem que ser mais profissional, mais bonito"*), apareceu no caminho uma coisa
muito maior que a peça: **nenhuma peça tinha animação dentro de uma atividade
montada**. Nenhuma. Sessenta das setenta e sete declaram `@keyframes`; o
`pecas.css` gerado tinha **zero** — e no lugar delas, 512 linhas de lixo do tipo
`.mec-digitar 25%{transform:...}`.

**A causa, e ela estava dois andares abaixo de onde eu procurei.** O
`prefixa_css` era o suspeito óbvio, mas o CSS já chegava lá sem as animações: o
culpado era o `regras()`, o separador que quebra a folha em regras. Ele conhecia
`@media` e mais nada. O cabeçalho `@keyframes pulso{` não casava com alternativa
nenhuma da expressão regular, e o `finditer` **anda para a frente sem avisar** —
a linha era pulada e os `0%`/`100%` de dentro sobravam soltos, virando
"seletores". O `@supports` caía no mesmo buraco, e pior: o invólucro sumia e a
regra de RESERVA passava a valer **sempre** (era o caso do `:has` na PONTE).

**Por que ninguém pegou, por meses.** Animação que some **não dá erro**: sem
erro de JS, sem portão reprovando, print idêntico, jogador chega à medalha.
Na peça avulsa — que é onde a gente olha — tudo animava lindamente, porque ali o
CSS é o original. Só na atividade, na mão da criança, a tela ficava morta. É o
avesso exato do que o Marcos pede o tempo todo, e era invisível para a banca
inteira.

**Duas descobertas independentes, mesma causa.** O agente da `ligar-pontos`
achou desenhando em volta do problema; o agente do `completar/escolher/digitar`
achou medindo o `pecas.css` gerado e contando as 512 linhas de lixo. Dois
caminhos diferentes chegando no mesmo ponto é o sinal mais forte de que a causa
é estrutural, não um caso isolado.

**O conserto, em três partes** (as duas primeiras arrumam, a terceira é a que
importa daqui para a frente):
1. `tira_keyframes()` arranca o bloco INTEIRO, do `@` até a chave que o fecha,
   **antes** de a folha ser quebrada em regras;
2. `prefixa_css()` passou a reconhecer `@keyframes`/`@supports`, **não prefixa
   marco de tempo** (`0%`, `from`, `to`) e **renomeia a animação por peça** — um
   `fade` da peça A e um `fade` da peça B eram a MESMA animação no arquivo final
   (CSS não tem escopo para `@keyframes`), a última declarada ganhava e a outra
   animava errado, calada;
3. **o portão que faltava:** o integrador agora CONTA. Quantas animações as
   peças declaram, quantas chegaram no arquivo final. Se some uma, ele para e
   diz. Medido depois do conserto: **257 animações preservadas, eram 0**.

**A lição, e ela é da mesma família de três outras já escritas aqui** (o
comentário que comia a regra seguinte, o portão que media o arquivo errado, o
`--so-ver` que saía 0 com 32 vozes faltando): **uma expressão regular que não
conhece um caso não tem como dizer que não conhece — ela simplesmente pula.**
Todo varredor que anda por um arquivo precisa de uma CONTA no fim: entrou tanto,
saiu tanto. Sem a conta, o que ele não entende some em silêncio, e silêncio aqui
é sempre lido como "estava tudo bem".

---

## 🎲 FALA DE MOLDE NÃO SE COLHE — SE ENUMERA

**O sintoma (ago/2026, remontagem da Padaria).** A banca reprovava por **uma**
fala sem voz. Colhia, montava, rodava de novo — e reprovava por **outra**. Uma
vez era *"Vou abrir este par: BOLO — começa com BO"*, na seguinte era
*BISCOITO*. Parecia portão instável, do tipo que a gente aprende a rodar duas
vezes até passar. Não era.

**A causa.** Aquela frase é um **MOLDE** do andaime do jogo da memória: existe
**uma por par** do conteúdo. O colhedor descobre falas **jogando** — e o jogo
**embaralha**. Ele só encontra as frases dos pares que o sorteio abriu naquela
partida. Colher de novo achava mais uma e continuava escondendo o resto.

**A conta que fecha o assunto:** eram 8 pares; a colheita, somadas várias
rodadas, tinha achado 5. As 3 que faltavam não iam aparecer por insistência —
iam aparecer por sorte, uma por rodada, para sempre.

**O conserto.** Enumerar as oito direto do `conteudo.json` (as fases de memória
e os pares delas) e escrevê-las no `falas.json`. Antes de confiar, conferi a
conta da chave contra as 11 que já estavam gravadas: **11 de 11 batem**, então
os mp3 novos caem no nome que o motor vai procurar.

**A regra que fica:** **amostragem serve para DESCOBRIR o que existe; não serve
para PROVAR que a lista está completa.** Sempre que uma fala nascer de um molde
(`"... %s ..." % item`), ela tem que ser gerada da mesma fonte que gera os
itens — o conteúdo — e não esperada no jogo. Portão que acusa uma coisa
diferente a cada rodada quase nunca é portão instável: quase sempre é portão
certo medindo uma lista que ninguém gerou inteira.

---

## 🎨 NÃO EXISTE COR FIXA CERTA — a peça tem que seguir o tema

**O que aconteceu (ago/2026).** A dica da peça `digitar` era creme (`#f4efe6`).
Na **Padaria**, cujo tema é claro, ela dava **2,56:1** — invisível. Escureci
para `#241d12`, a Padaria passou, e eu dei o caso por encerrado. Horas depois,
na **Central**, cujo tema é escuro, a **mesma dica** dava **1,06:1** — invisível
de novo, agora pelo outro lado.

**Quando um defeito volta pelo lado oposto, o problema não é a cor: é a ideia de
escolher uma.** A peça não sabe em que atividade vai cair, e as atividades da
casa vão do azul-céu de um 1º ano ao galpão à noite de um 6º.

**As três saídas, e quando cada uma vale:**
1. **`var(--texto)`** — o padrão. O motor define o token, cada atividade o
   redefine, e a peça segue o tema em vez de apostar num.
2. **Cor cravada COM fundo próprio** — legítima. Um `.opt` creme com tinta
   escura carrega a mesa dele junto e é legível em qualquer tema.
3. **Mesa própria para o texto solto** — para o que cai sobre uma FAIXA COLORIDA
   do tema (`.passo`, `.dgpista`, `.bsTeclado`). Ali nem o token nem a cor fixa
   servem: um morre num tema, o outro no outro. Fundo próprio resolve os dois.

**O portão:** `_qa/cor_fixa.py` (4b da bancada). Ele acusa cor de texto em tom
**neutro** extremo definida **sem** fundo próprio. Três aparadas até virar
portão, e cada uma vale por si:
- **66 de 80** quando olhava só a própria regra — dica clara dentro de um cartão
  que a peça já pintou de escuro está protegida;
- **62 de 80** quando contava o amarelo da casa como "quase branco" — **acento
  tem dono, cinza claro não tem**;
- **1 de 80** quando lia `to{...}` de um `@keyframes` como seletor — marco de
  tempo não é elemento, a mesma família do defeito que engoliu as animações.

**E a bancada também declara o tema.** Ao trocar 43 peças para `var(--texto)`, a
cor de reserva escura passou a cair no fundo escuro da própria bancada. O
`MOLDE` agora declara `:root{--texto:#f4efe6}`, que combina com o fundo DELE; a
atividade redefine com o dela. Peça que segue o tema precisa que **todo lugar
onde ela roda** tenha um tema.

**A regra que fica:** *portão estático propõe, navegador dispõe.* O `cor_fixa`
acha a causa barato, na peça; o `contraste.js` mede o pixel na atividade. Os
dois são necessários — a varredura automática que fiz com o primeiro quebrou
três textos que só o segundo pegou.

---

## O REGISTRO QUE MENTIA — plano B silencioso (ago/2026)

**O que aconteceu.** Pedi três cartelas com `modelo=gemini`. Voltaram três
imagens ruins: rostos pálidos e tristes, fundo cinza, nada do que o prompt
pedia. Eu já ia escrever *"o Gemini não entendeu o prompt"* — e estava prestes a
gastar a rodada seguinte reescrevendo prompt.

**O Gemini nunca foi chamado.** A cota dele tinha acabado (HTTP 429). O
workflow, de propósito e com razão, **cai para o Pollinations** quando o Gemini
falha, para não parar a produção. Só que a mensagem do commit vinha do **INPUT**:
dizia `(gemini)` de qualquer jeito.

**A regra que fica:** *todo caminho com plano B silencioso precisa dizer qual dos
dois entrou.* Se o plano B pode assumir sozinho, o registro que diz "o que foi
pedido" é pior que nenhum registro — ele parece resposta e é chute. Agora sai
`_novo/<nome>.origem.txt` ao lado da imagem e o commit vira
`imagem: gera X [desenhado por: pollinations (o gemini falhou: HTTP 429 ...)]`,
com o motivo de cada um dos três modelos. Leio com `git log`, de graça.

**Irmã disto:** aviso de saldo/serviço externo tem **data** e se **remede** antes
de repetir. O `CLAUDE.md` dizia "o Gemini TEM crédito (07/08)" e eu repeti isso
como se fosse de hoje — cinco dias depois era mentira.

---

## AVISO QUE GRITA À TOA ENSINA A PULAR AVISO (ago/2026)

**O que aconteceu.** Montar o 6º ano imprimia **dez avisos**. Todos sobre gavetas
que estavam **certas** no exemplo: `LETRAS`/`ALFA` são o alfabeto do teclado,
`FEITOS` nasce vazia e a peça preenche jogando, `FORCA_FIG`/`MODO` são opções com
padrão legítimo. Passei o olho — e no meio deles ia um defeito de verdade.

**Duas coisas mudaram, e a segunda é a que importa:**
1. A lista de nomes perdoados morava no **montador**, e só crescia **depois** do
   defeito. Agora quem declara é a **PEÇA**: `/*TECNICA*/` na linha da `var`. Quem
   sabe o que é conteúdo e o que é engrenagem é quem escreveu a peça.
2. Montagem do 6º ano passou de dez avisos para **zero**. Aviso vale pelo que ele
   custa ao ser lido: se sempre há dez, não há nenhum.

---

## GAVETA QUE SÓ FUNCIONA COM A CHAVE DA OUTRA (ago/2026)

**O que aconteceu.** Escrevi as cinco definições de gênero em `PALDEF` — bula,
edital, conto, cada uma pensada para a criança adivinhar sem ver a palavra. A
fase abriu mostrando as **palavras**, como sempre. Não houve erro: a peça só olha
`PALDEF` quando `MODO="definicoes"`, e o `MODO` ficou no padrão. Trabalho
escrito, revisado e **invisível**.

`MODO` tem padrão legítimo, então não pode entrar na lista de avisos — o que pega
o caso é a **DEPENDÊNCIA**, declarada no montador:
`{("caca-palavras","PALDEF"): ("MODO","definicoes")}`. Provado: tirando o `MODO`,
o montador **reprova as três fases e não gera nada**. No mesmo dia ele pegou
sozinho as duas fases iguais do 9º ano.

**A regra que fica:** gaveta que só liga com a chave de outra não é aviso, é
reprovação — porque o sintoma dela é *nada acontecer*.

---

## VITRINE DE UMA FIGURA SÓ (ago/2026)

A Central de Entregas não tem "produto": tem TEXTO. A varredura achou **uma**
figura elegível e encheu as **39 vagas** com ela — a mesma miniatura de 53×32
repetida treze vezes por tela. O portão do encaixe acusou dezenas de vezes.

Pior que feio: a vitrine existe para dizer *"olha tudo o que você já juntou"*, e
uma prateleira com o mesmo item repetido diz o contrário — que nada muda por mais
que a criança ande. **O montador já imprimia "1 figura(s) diferentes" e eu passei
o olho.** Virou decisão: menos de 3 figuras diferentes, não há vitrine.

---

## O BECO, DE NOVO — e por que o portão que existia não pegou (ago/2026)

O `_qa/beco.py` mede a ATIVIDADE: para cada peça que **declara** `fimDaPeca`,
exige que a ponte do integrador a tenha reapontado. O `relampago` passou por ele
com folga — **porque não tinha `fimDaPeca` nenhum**. Tinha a tela de fim dela,
com nome próprio, chamada direto. A ponte estava armada e mirando no vazio.

Dentro da atividade a criança fechava o aquecimento da fase 13 de 39 e o único
botão voltava ao começo da **mesma** fase. Para sempre.

**O portão novo é na PEÇA** (`_qa/beco_peca.py`, bancada 3b), sem navegador, em
um segundo: *a tela que tem o botão de recomeçar é chamada DIRETO em algum
lugar?* Se sim, ela aparece de verdade e prende.

⚠️ **A aparada que ele precisou:** a primeira versão acusou **dez peças certas**.
Ter "jogar de novo" não é defeito — nessas dez a tela só é alcançada por
`mostraBanner()`, e dentro da atividade essa ponte leva embora antes de a tela
existir. Medido depois da aparada: **80 peças, 1 reprovada** — o
`conserte-o-erro`, gêmeo exato do relâmpago.

**A regra que fica:** quando um portão não pega um defeito da família dele,
perguntar *o que ele exige que o defeito não tinha* — aqui, a declaração. Portão
que só olha quem se apresenta não vê quem passa por fora.

---

## O TEMA DO EXEMPLO CRAVADO NA PEÇA (ago/2026) — e o portão que eu NÃO fiz

A peça `caca-palavras` nasceu com a horta da escola, e o assunto ficou **escrito
no código** em quatro lugares: o selo *"CAÇA-PALAVRAS DA HORTA"*, o pedido
(*"ache as 5 palavras da horta"*), a comemoração e a tela de fim. Toda atividade
que usasse a mecânica levava a horta junto: **a Central de Entregas, que é sobre
gêneros textuais, comemorava "achou as 5 palavras da horta!"**.

O `_qa/clone.py` não pega isto — ele procura **prefixo** de outra pasta, e
"horta" não é prefixo, é palavra. Quem pegou foi o `colher.py`, ao listar as
falas a gravar: a frase apareceu na lista e destoou.

**O conserto que vale para sempre:** a frase da peça não cita o assunto. *"Ache
as 5 palavras"* está sempre certo; *"ache as 5 palavras da horta"* está certo uma
vez só. Quando o assunto for mesmo necessário, ele vira **gaveta** (foi o caso do
`TITULO`).

**⚠️ E aqui vai a parte honesta: tentei transformar isto em portão e não
consegui.** Duas medições:
- *"palavra do exemplo aparecendo em frase da peça"* → **52 peças acusadas**,
  quase todas inocentes (`caixa` em `base-dez`, `hora` em `relogio`, `contorno`
  em `arrastar-sombra` — vocabulário DA MECÂNICA, não tema que muda);
- estreitando para a gaveta principal (a que a atividade troca) → **27 peças**,
  ainda com "hora", "pulos", "caixa" no meio.

Portão que acusa 27 inocentes é pior que portão nenhum, e essa lição já está
paga nesta casa três vezes. **Fica como dívida medida, não como portão fingido.**
O caminho provável, para quando houver tempo: exigir que TODO texto que a criança
lê numa peça more numa **gaveta** — aí o aviso de "gaveta com conteúdo de
exemplo", que já existe e já funciona, cobre esta família inteira sem regra nova.

---

## MESA CLARA SEM TINTA PRÓPRIA — e o portão que eu escrevi e joguei fora (ago/2026)

A bancada reprovou o `montar-frase`: **oito textos a 1,07:1**. As peças de
palavra pintam a própria mesa em pastel (verde, laranja, azul, lilás) e deixavam
a tinta por conta de `var(--texto)`. Num tema **escuro** esse token é creme —
creme sobre pastel some, e a fase é justamente montar a frase com elas.

É o **defeito contrário** ao que o `_qa/cor_fixa.py` procura: lá é cor cravada
demais, aqui é cor **nenhuma**. A regra que fica, e vale para toda peça nova:
**quem pinta a própria mesa crava a própria tinta** — esse elemento não depende
do tema, ele traz o tema dele.

**⚠️ E a parte que interessa mais que o conserto:** escrevi o portão estático
para isso — *"regra com `background` claro e sem `color`"* — e ele acusou
**80 peças de 80**. Nem cheguei a olhar uma por uma para saber que estava
errado: 100% é sempre ruído. A razão é simples e vale como regra geral: sem DOM
não dá para saber se aquele elemento **tem texto**, nem qual cor ele **herda**
de um pai que já resolveu o problema. Um `.card` claro sem `color` pode estar
perfeitamente certo porque a tinta está no filho.

Quem mede isto é o `_qa/contraste.js`, que abre o navegador e lê o **pixel** —
e foi ele que pegou. *Portão estático propõe, navegador dispõe*, pela terceira
vez nesta casa. Fica o conserto da peça e fica a regra escrita; portão estático,
não.

---

## O DEFEITO QUE MORA NO RECORTE ENTRE DOIS ARQUIVOS (ago/2026)

O jogador ficou **preso** em duas atividades diferentes, na mesma noite, com
`figEl is not defined`. A peça passava na bancada com código 0.

**Por quê:** o integrador leva para a atividade **o SEGUNDO `<script>`** da peça
— o primeiro é o motorzinho da bancada, que o motor de verdade já tem. Eu
declarei o `figEl` no primeiro. Na bancada o arquivo inteiro roda e tudo
funciona; dentro da atividade a declaração simplesmente **não viaja**, e a fase
morre com a criança na frente. **Quatro peças de uma vez.**

**E por que nenhum portão viu:** cada portão olhava **um arquivo inteiro** — a
peça, ou a atividade montada. O defeito não está em nenhum dos dois: está no
**recorte** que o integrador faz entre eles. Portão que valida as pontas não vê
o corte.

**A regra:** tudo o que a MECÂNICA usa mora no **segundo** `<script>`. O primeiro
é bancada, e bancada não viaja.

**O portão** (no integrador, onde o recorte acontece): o que o bloco `MEC[...]`
usa tem que estar declarado no bloco. Provado devolvendo a declaração para o
lugar errado — acusa.

**A regra geral, que vale além deste caso:** quando uma ferramenta RECORTA um
arquivo para dentro de outro, o portão tem que rodar **depois do recorte**. Foi
assim com as animações engolidas, com a prosa renomeada, e agora com o nome que
não viaja — três defeitos, o mesmo lugar.

---

## A FORMA SUMIA QUANDO O NOME DA CATEGORIA ERA OUTRO (ago/2026)

A peça `montar-frase` tem cinco **formas** de peça (pastilha, tijolo, folha,
seta, arco) e a mecânica inteira é *"cada vaga tem uma FORMA"*. As formas moram
no CSS com os nomes do exemplo: `f-art`, `f-sub`, `f-adj`, `f-ver`, `f-adv`.

O 9º ano de inglês chama as categorias dele de `quem`, `aju`, `acao`, `onde` —
nomes **certos** para aquela atividade, e que o CSS não conhece. Resultado: as
peças saíam **todas iguais**, sem forma e sem cor, e o apoio visual que sustenta
a mecânica virava texto solto. Sem erro nenhum.

O `_qa/classes.py` não vê: a classe é montada em tempo de execução, a partir do
conteúdo. **Classe que nasce de dado não é classe que o portão consegue ler.**

**O conserto:** a peça deixou de usar o nome como classe. Ela distribui as cinco
formas que TEM entre as categorias que a rodada trouxer, na ordem de aparição.
Qualquer atividade nomeia as categorias como quiser e continua ganhando as
formas. **Peça não impõe vocabulário à atividade.**

---

## SETE MECÂNICAS PASSAVAM PELO MONTADOR SEM CONFERÊNCIA (ago/2026)

Duas fases chegaram quebradas ao jogador **na mesma noite**: a `autoexplicacao`
do 6º ano **sem o campo `esc`** (as escolhas!) e a `forca` com o conteúdo
dizendo `palavra`/`pista` quando a peça lê `p`/`ac`/`d`. A criança ficava presa
em 73% e em 93% da atividade. Nenhum erro na montagem, nenhum aviso.

**A causa é a mais desconfortável desta noite.** O montador manda o exemplo da
peça para o `node` para descobrir o formato. Quando o exemplo cita um desenho
por NOME — `svg:SVG_JANELA_SOL`, `arte:svgPonte`, `fig:ARTE.LEAO` — o node
estoura com *"is not defined"*, o `literal()` devolve `None`, e o montador
**pula aquela mecânica inteira, calado**. Eram **sete das 79**. E não é acaso
que as duas que quebraram estavam entre elas: são justamente as mecânicas mais
ricas, as que têm arte no exemplo.

**Portão que pula calado é pior que portão que falta**, porque ele parece ter
olhado. É a mesma família do "rodou cego" que a banca grande já denuncia — mas
aqui o cego estava DENTRO de um portão que dizia "escada ok".

**O conserto:** uma leitura dos campos no **texto cru** do exemplo, que não
depende do node. Com ela, as duas metades da conferência passam a valer para as
79 mecânicas:
- campo **a mais** (a peça não lê) — já existia, agora alcança todas;
- campo **estrutural a menos** (lista/objeto que a peça PERCORRE) — novo, e
  reprova: escalar que falta costuma ser opcional, estrutura que falta nunca é.

---

## REMONTAR DEPOIS DO PULL (ago/2026)

Consertei a `forca`, montei, commitei, dei `git pull --rebase` e testei: **o
defeito continuava**, com o `conteudo.json` já certo no disco. O `index.html`
que eu tinha acabado de gerar foi **substituído pela versão do remoto** — os
workflows (voz, imagem) também commitam a pasta da atividade, e o rebase trouxe
o build antigo por cima do meu.

Gastei uma rodada inteira de jogador (10 min) achando que o conserto não tinha
pegado. **A ordem certa é: pull → montar → commit → push.** Nunca montar antes
de puxar.

---

## O RELÓGIO QUE SOBREVIVE À FASE (ago/2026)

Um erro de JS por partida, nas **duas** atividades, sempre o mesmo texto
(`Cannot read properties of undefined (reading 'c')`) e sempre **depois** de a
criança já ter passado. O jogador chegava à medalha; a banca reprovava — com
razão, mas sem dizer onde.

**Era o `raios-x`.** A peça arma um `setTimeout` de 7 segundos que abre a
pergunta sozinha se a criança demorar a explorar a chapa. O guarda desse timer é
uma **geração** (`rxGer`), e a geração só subia dentro de `fimDaPeca`.

**Só que dentro da atividade o `fimDaPeca` nunca roda**: a ponte do integrador
troca o `mostraBanner` por *"mostre e siga"*, então a peça sai de cena sem passar
por lá. O timer da ÚLTIMA chapa ficava vivo, disparava 7 segundos depois com a
criança já noutra fase, e lia `CHAPAS[rxI]` com o índice fora da lista.

**A regra, e ela vale para toda peça com relógio:** a geração tem que subir
**onde a peça sai de cena**, não dentro do `fimDaPeca`. Na bancada os dois
caminhos coincidem — por isso a peça passava sozinha, e por isso este defeito só
existe montado.

Varri as 80 peças procurando a mesma armadilha (geração que só sobe dentro de
`fimDaPeca`, com `setTimeout` no arquivo): **nenhuma outra**. E o guarda barato
ficou junto — `abreResposta` agora tem o mesmo `if(!ch) return;` que a `telaRX`
já tinha. Duas defesas, porque a que some é a que volta.

---

## A COLHEITA NÃO É UM PASSO OPCIONAL (ago/2026)

A receita diz **montar → colher → montar**, e nesta noite eu tratei o `colher.py`
como algo que se roda uma vez no fim. Ele foi a última coisa a reprovar as duas
atividades, **três vezes seguidas**, sempre pelo mesmo motivo: texto que só
existe em tempo de execução.

O montador escreve o `falas.json` a partir do `conteudo.json` — e há falas que
não estão lá:
- as que a peça **compõe na hora**: *"Agora é rápido! São **8** perguntas"*,
  *"Abri uma para você: **BULA**. Ache o par dela"*, *"Já achou **3** de 5"*;
- as que moram nas **gavetas de texto da peça** (`ENUN`, `FECHO`, `ORDTXT`) —
  e esta noite muitas nasceram, justamente para tirar o assunto do exemplo de
  dentro do código.

**A regra:** toda vez que mudar conteúdo OU mexer numa gaveta de texto de peça,
a ordem é `colher` → `montar` → gravar. Colher depois de gravar é gravar de
novo; colher antes de montar é colher a versão velha.

**Por que dói tanto pular:** a fase fica **muda**. Não quebra, não avisa, o print
sai perfeito — e a criança que ainda lê devagar perde exatamente o apoio que a
casa promete no pilar SONORA.

---

## O NOME QUE EXISTE DUAS VEZES, EM ESCOPOS DIFERENTES (ago/2026)

As duas atividades chegaram ao fim da noite com **uma única acusação cada**, a
mesma nas duas: *"TELA ÓRFÃ: ninguém chega em `telaAbertura`"* e *"em
`telaMestre`"*. E as duas eram **falsas**.

A peça `quem-sou-eu` chama a tela dela de `telaQuem` — e o MOTOR chama de
`telaQuem` a tela *"quem vai jogar"*. **Dentro da atividade não há conflito
nenhum:** cada peça vive dentro do seu `MEC[...] = function(){...}`, então a
`telaQuem` da peça é local e não encosta na do motor.

O portão, porém, varria o arquivo inteiro com um regex e guardava a **última**
definição de cada nome. Ficava com a `telaQuem` da PEÇA — que naturalmente não
chama `telaMestre` nem `telaAbertura` — e as duas telas do motor viravam órfãs.

**A regra:** portão que desenha o fluxo do motor tem que **respeitar o escopo**.
O corpo das peças sai do texto antes da varredura; o que acontece lá dentro já é
medido por `confere_esqueleto` e pelo auditor-jogador, que joga de verdade.

É a terceira vez na mesma noite que a resposta é *"o portão leu o arquivo como
se fosse um texto plano"* — as animações engolidas, a prosa renomeada, e agora o
nome repetido. **Arquivo montado tem camadas; leitor plano vê fantasma.**

---

## O PORTÃO QUE SÓ SABIA ANDAR NA ATIVIDADE ESCRITA À MÃO (ago/2026)

Depois de tudo verde, as duas atividades reprovavam **sem uma única linha de
problema**. O culpado era o portão 0g (`_qa/vozigual.js`), que abre fase por
fase e pergunta se o alto-falante repete o que está escrito.

Ele andava pela `FASES_MESTRE` — a lista global das atividades **escritas à
mão** — e abria a fase com `window[nome]()`. Numa atividade **montada** as fases
são DADOS (`FASES` + `montaFase(i)`) e não existem como função global: a chamada
estourava, o `try{}catch{}` engolia, a tela ficava parada na capa e o portão
carimbava *"a tela não tem voz nenhuma"* nas 39 fases. **Ele não mediu nada — e
reprovou a própria cegueira.**

Dois consertos, e os dois valem para qualquer portão novo:

1. **Quem anda pela atividade tem que conhecer as DUAS formas dela** (montada e
   escrita à mão) — igual ao `_qa/fala_o_escrito.js` e ao `_qa/fluxo.py`.
2. **Não medi ≠ reprovado.** Portão que não consegue abrir a fase sai com
   **código 2**, nunca com 1. Reprovar sem saber ensina a desconfiar do certo.

E um terceiro, da mesma família das lições anteriores: **o portão perguntava
trocando o `falar` da atividade por um stub** — só que é o `falar` quem guarda o
`falaTela`, que é justamente a resposta procurada. Perguntando assim, a resposta
nunca nascia. Agora ele desliga só o TOCADOR (`play`) e pergunta ao motor pelo
caminho do motor (`vozDaTela()`). **Portão tem que perguntar do mesmo jeito que
o motor responde.**

### O defeito REAL que apareceu quando o portão voltou a enxergar

Com ele medindo de verdade, saiu na hora um defeito de criança: a peça
`ensinar-mascote` chamava `falaDaTela("balaoP")`. **`falaDaTela` quer dizer duas
coisas diferentes nos dois mundos** — na bancada o argumento é o *id do
elemento* (ela lê o texto dali), na atividade é o *nome da gravação*. A peça
soava perfeita na bancada e, na atividade, mandava o motor buscar
`audio/balaoP.mp3`, que não existe: enunciado **mudo** e alto-falante que não
repete nada. Peça que empresta um nome do motor tem que perguntar em que mundo
está (`typeof temVoz==="function"`) antes de falar.

### E a regra de encolher que o navegador ignorava calado

No mesmo arquivo, o `@media (max-height:470px)` mandava `.opt{min-height:44px}`
— mas mais acima existia `.opts .opt{min-height:62px}`, **duas classes**, que
ganha por especificidade. A regra da janela baixa estava escrita, estava certa e
**não valia nada**: a quarta opção caía fora da tela. **Regra de encolher tem
que nascer com a mesma força da regra que ela conserta.**

---

## O TOKEN QUE NUNCA EXISTIU — e só acordou no primeiro tema escuro (ago/2026)

`.mbt` (os botões do menu de fases do professor) reprovou por contraste
**1,06:1** — creme sobre creme — nas 21 fases da Central. O CSS parecia certo:

```css
.mbt{background:rgba(255,253,244,.97); color:var(--tinta-d); …}
```

Só que **`--tinta-d` nunca foi declarado em lugar nenhum** — nem no motor, nem
no Jardim de onde ele veio (`--dourado` idem). Propriedade personalizada que não
existe não pinta nada: o `color` fica inválido no valor computado e a letra
**herda** a cor de cima.

**Por que dormiu tanto tempo:** no Jardim, `--texto` é escuro. A letra herdada
saía escura — igualzinha ao que se queria — e o defeito ficou invisível por
atividades e atividades. Na Central, cujo tema troca `--texto` por creme (a
Central trabalha à noite), a mesma linha virou creme sobre creme.

**As duas regras:**

1. **Token usado é token declarado.** `var(--x)` sem `--x` no `:root` não é
   "cor padrão": é herança silenciosa, e herança silenciosa é uma bomba com
   fusível de tema.
2. **Ladrilho claro tem a TINTA DELE, escrita.** O cartão do crachá é creme,
   então `.cnome` não pode usar `var(--texto)` — os irmãos dele (`.csel`,
   `.cfun`) já tinham tinta própria, sinal de que esta mesma lição já havia sido
   paga uma vez e não foi generalizada.

E o de sempre: **quem encolhe a altura tem que estreitar junto**. A regra da
janela baixa da peça `ensinar-mascote` baixou o botão para 44px e deixou os
360px de largura — 6,5 vezes mais largo que alto, exatamente o "botão esticado"
que o Marcos reprovou.

---

## A RESERVA DO `var()` NÃO É UMA REDE DE SEGURANÇA (ago/2026)

`quem-sou-eu` escrevia, com um comentário explicando o cuidado:

```css
.subm{ color: var(--texto, #d9cdf0) }   /* dentro da carta ROXA */
```

A reserva `#d9cdf0` **só entra em cena quando o token não existe**. Dentro de
uma atividade ele existe sempre — valendo a tinta *daquela* atividade. Numa de
tema claro, a linha virou tinta escura dentro de uma carta roxa: **1,01:1**. O
autor tinha visto o risco, escreveu o comentário certo e mesmo assim escolheu a
ferramenta que não protege.

**Tinta de superfície que a peça pinta é escrita, não herdada.** E, para o
portão `_qa/cor_fixa.py` conseguir enxergar isso sozinho, **o seletor tem que
dizer onde ele mora**: `.misterio .subm`, não `.subm` solto. O portão perdoa
tinta clara quando algum ancestral *do seletor* pinta fundo — e um seletor que
não nomeia a casa dele não tem como ser perdoado. Escrever o caminho não é
enfeite: é a única forma de a regra ser verificável.

## PRATO TRANSLÚCIDO É UMA MÉDIA, NÃO UMA COR

A ponte do integrador dava `background:rgba(58,48,32,.55)` à `.hint`. Sobre o
galpão escuro isso é quase opaco; sobre o céu claro da atividade a mistura subiu
para **3,7:1** em 14 fases — abaixo dos 4,5.

**Fundo com alfa não é uma cor: é uma média com o que estiver atrás, e o que
está atrás muda de tela para tela.** Quem escolhe a opacidade tem que fazer a
conta no PIOR caso (fundo branco), senão está apostando no fundo que viu no dia.

---

## O ELOGIO É DO ACERTO, NÃO DE CADA PEÇA QUE ACENDEU (ago/2026)

Terceira vez na família *"duas vozes juntas"* — as duas anteriores quem ouviu
foi o Marcos. A ponte do integrador varre a tela atrás do que a peça marcou como
certo e, **dentro do laço**, tocava som + elogio. Um único toque que acende DOIS
elementos de uma vez — o `completar` acende a lacuna *e* a palavra escolhida —
disparava `ce_acerto1` e `ce_acerto2` no mesmo instante.

**A faísca é de cada peça que acendeu; o elogio é do ACERTO, que é um só.**
Efeito visual pode ser por elemento (o olho aguenta dois); som e voz, nunca.

## E O PORTÃO QUE PARTIA A CONTA NA HORA ERRADA

O `_qa/voz_dupla.js` zerava a lista de áudios só DEPOIS de ler a abertura, então
o elogio do acerto da fase anterior entrava na conta da abertura da seguinte:
duas linhas para um defeito só, e a primeira apontando para uma fase inocente.
**A janela de medição começa quando a fase começa.**

## QUEM RESPONDE PELO ALTO-FALANTE É O ALTO-FALANTE

O `_qa/vozresposta.js` acusou 15 fichas mudas na mecânica `ordenar`. Ele
perguntava ao CARTÃO o que a voz diz — e o cartão mostra só o número da posição.
O texto está declarado no próprio botão (`.zap[data-voz]`), porque nessa peça
quem fala é o botão dela, com o `onclick` dela. Medido no navegador: tocar o
alto-falante toca a frase certa, gravada. **Perguntar ao vizinho é inventar
defeito** — e é a mesma lição que o `fala_o_escrito.js` já tinha pago.

---

## A CHAPA BORRADA NÃO É UMA SEGUNDA IMAGEM (ago/2026)

A fase "a foto do drone saiu desfocada" (`raios-x`) apontava a camada de cima
para `rn_blur1.png` — **uma imagem que nunca foi gerada**. A criança abria a
fase e via um quadradinho vazio.

Duas coisas erradas de uma vez:

1. **O montador não pediu a figura.** A lista `CHAVES_DE_FIGURA` não conhecia
   `cima`/`baixo`, os nomes que essa peça usa — então o arquivo nunca entrou na
   lista de compras e o montador disse, com toda a confiança, *"0 figura(s) a
   gerar"*. É a **terceira** vez que essa lista cresce depois do estrago. **Nome
   de campo que aponta figura entra na lista no mesmo commit em que a peça
   nasce.**
2. **A imagem nem devia existir.** Desfoque é **efeito de câmera, não
   ilustração**. Pedir à IA uma "versão borrada" custa dinheiro, volta com outra
   luz e outro enquadramento — e aí a janela passaria a revelar *outra cena*, o
   contrário da mecânica. Agora a peça aceita `borrado:true` e usa a MESMA foto
   com `filter:blur()`.

## O RAIO-X REVELA POR BAIXO: MESMO SENTIDO E FUNDO TRANSPARENTE (ago/2026)

O Museu ganhou raio-X de verdade (o Marcos gerou 8 chapas no ChatGPT). Chegaram
até ele com DOIS defeitos que o print parado esconde e só a criança vê:

1. **Esqueleto ESPELHADO.** A chapa `baixo` fica DEBAIXO do bicho `cima` na
   mesma `.chapa` (ambos `background-size:cover`). Se o bicho olha para a direita
   e o esqueleto para a esquerda, a janelinha revela um esqueleto que não bate
   com o corpo — "esqueleto invertido". **Regra: a chapa tem que olhar para o
   MESMO lado do bicho.** Conferir par a par (montagem lado a lado) e espelhar
   (`Image.FLIP_LEFT_RIGHT`) a chapa que estiver ao contrário. Bichos simétricos
   de topo (borboleta, aranha, polvo) não têm lado — não mexer.
2. **Fundo OPACO.** O bicho `cima` é PNG **transparente** sobre a `.chapa` escura
   (`#1d1710`). Se a chapa `baixo` vier com fundo navy OPACO (radiografia crua),
   a janela revela um RETÂNGULO colado, não um esqueleto — "ficou horrível".
   **Regra: a chapa também é PNG transparente — só o esqueleto brilhando.** Do
   navy cru: alfa por luminância (`smoothstep` de ~52 a ~150), esqueleto claro
   fica opaco, fundo escuro some. Aí bicho e esqueleto vivem na MESMA chapa
   escura, iguais. **Toda arte que entra numa peça de sobreposição (raio-X,
   verso de carta, camada que a janela revela) nasce transparente e no mesmo
   sentido da camada de cima** — senão vira caixa colada.

3. **BICHO CORTADO NA MOLDURA (ago/2026).** A `.chapa` do raio-X mostra a
   imagem com `background-size:cover` numa caixa de proporção fixa (`padding-
   bottom:74%` → ~1.35). Duas armadilhas que o Marcos pegou: (a) os
   INVERTEBRADOS usavam a imagem-BASE do bicho (outra proporção) — o `cover`
   recortava as pontas; (b) o `_rx` dos vertebrados tinha margem de só 6% e as
   extremidades encostavam na **moldura arredondada**. **Regra: TODA figura do
   raio-X (vertebrado E invertebrado) entra normalizada numa tela 800×592
   (=1.35) com margem de ~14%** — assim o `cover` preenche sem cortar e o bicho
   fica longe dos cantos. O esqueleto (`_xray`) é normalizado na MESMA caixa
   14%, então continua proporcional e alinhado. Conferir antes: simular o
   `cover` da chapa (max(bw/iw,bh/ih), recorte central) e olhar; e checar a
   ATIVIDADE TODA por `background-size:cover`/`object-fit:cover` em imagem de
   conteúdo (o verso da memória pode; foto de bicho, não).

## O HALO BRANCO DE RECORTE (ago/2026) — `_qa/halo.py`

Logo depois, o Marcos: *"tem imagens que estou com partes brancas do fundo"* e
*"ainda tem imagem com muito branco nas bordas"*. Figura recortada de fundo
branco fica com um **anel branco/cinza-claro** grudado na silhueta. No card
CLARO ninguém vê; na chapa ESCURA (raio-X, memória) o anel salta. Conserto que
funcionou (Pillow, sem navegador): (1) flood-fill da BORDA por {transparente OU
quase-branco} e apaga o quase-branco alcançado — o branco LEGÍTIMO interno
(barriga do pinguim, faixa do peixe) fica cercado pelo contorno colorido e não é
alcançado; (2) apaga franja **clara e SEM cor** até 2px da borda (protege bicho
cinza — tubarão/arraia — porque limita a distância); (3) **erode 1px** o alfa
para a borda ficar nítida. **Nunca reprocessar o mascote** (jaleco/lupa são
branco legítimo — pular `mv_tato*`). Portão: **`_qa/halo.py`** reprova só halo
GROSSO (casca fina >1,5% E razão casca/halo alta); fio de borda legítimo na
silhueta passa (fica para o olho do professor). **Regra permanente: toda figura
recortada roda `_qa/halo.py` e é conferida sobre FUNDO ESCURO, não só no card.**

## O NOME É O CONTRATO — QUEM FECHA A PEÇA SE CHAMA `fimDaPeca`

A `ensinar-mascote` tinha a tela de fechamento com nome próprio e a chamava
direto. A ponte do integrador só troca quem se chama `fimDaPeca`: dentro da
atividade a criança terminava as regras, caía na tela de bancada e ficava presa
num "Jogar de novo" que repetia a MESMA fase.

E a ironia do dia: o comentário que eu escrevi explicando o conserto **citava a
frase proibida por extenso**, e o portão `_qa/beco.py` — que procura essa frase
no código vivo — passou a acusar o próprio aviso. **Comentário também é texto.**

## COMPARAR PALAVRA INTEIRA SÓ FUNCIONA COM UMA PALAVRA

O `_qa/figura_certa.py` exigia que um nome contivesse o outro. `THE BOY` ×
`rn_boy_eating` é a figura CERTA e reprovava, porque `theboy` não está dentro de
`boyeating`: **onze acusações, todas em conteúdo correto.** Agora ele compara
**palavra por palavra**, descartando artigos e preposições — e o dente continua
onde importa (`ovo` × `mamao` segue reprovando, medido).

E quando a resposta é um **lugar** (`AT THE BENCH`), o nome do arquivo fala da
ação que acontece na cena: **não há como decidir pelo nome**. Isso virou lista
separada, para o olho do professor. *Não medi* nunca pode sair como *reprovado*.

---

## `--reparo`: o atalho para CONSERTAR (nunca para entregar)

`bash _qa/auditar.sh --reparo <arquivo.html>` roda só os portões de **texto**.
Medido: **38 segundos** contra ~25 minutos da banca inteira.

Por que ele existe: a banca completa abre o Chromium em 6 tamanhos × 40 telas e
ainda joga a atividade até a medalha. Isso está certo para ENTREGAR e errado
para CONSERTAR — quem acabou de trocar uma frase não pode esperar 25 minutos
para descobrir que trocou errado. Com a esteira parada, a tentação é entregar
sem rodar nada, e aí o portão vira enfeite.

**O que fica de fora** (e por isso ele NUNCA sai com "APROVOU"): contraste,
leiaute, imagem quebrada, encaixe, acabamento, vazamento, o alto-falante das
respostas, a voz igual ao texto, a voz dupla, o jogador que joga até a medalha
e a colheita. Ou seja: tudo que só o navegador vê.

**A regra:** `--reparo` durante o conserto, quantas vezes quiser; a banca
inteira, sem bandeira, antes de o Marcos ver. Passar no reparo é *"ainda não
reprovou no barato"* — não é aprovação, e o próprio rodapé dele diz isso.

---

## O PORTÃO QUE DIZIA "-" E SEGUIA EM FRENTE (ago/2026)

O pedagogo confere **concreto → figural → simbólico** procurando, no código da
fase, o desenho (`imgEl(`) e o campo de digitar. Numa atividade **montada** a
fase não tem código: ela é DADO, e o código mora na mecânica, compartilhada por
várias fases. Resultado: ele imprimia `figura: - | simbolo: -` e passava.
**Silêncio que parece aprovação é o pior resultado possível** — pior que
reprovar, porque ninguém vai conferir depois.

Agora ele diz, com todas as letras, que **não mediu** este item nas montadas.

E não adianta trocar por *"a fase tem campo de figura no dado?"*: numa atividade
de **ortografia** o objeto de estudo É a palavra escrita, então exigir uma figura
antes da primeira palavra reprovaria justamente o conteúdo certo. Quando o
portão não tem como saber, quem sabe é o professor — e o portão tem que dizer
isso em vez de fingir.

## E DUAS COLISÕES DE NOME, NO MESMO PORTÃO

- O sinal de "símbolo" era o texto `"campo"` — que existe para pegar o **campo de
  digitar** o nome (`el("input","campo")`). Numa atividade sobre a palavra
  **CAMPO** (o campo de futebol do bairro), a chave `k:"campo"` do jogo da
  memória batia no regex e o portão anunciava que o símbolo chegou antes da
  figura. Sinal tem que pedir o CONTEXTO, não a palavra solta.
- O sinal de "figura" era `imgEl(`, e a atividade montada desenha por `figEl(`,
  a ponte do integrador. Um nome a menos e **toda** atividade montada aparecia
  como "sem figura nenhuma".

**A regra que fecha as duas:** quando um portão nasce olhando a atividade
escrita à mão, ele precisa ser reapresentado à montada — senão ele mede a forma
que conhece e chama de erro a que não conhece.

---

## O FUNDO QUE NUNCA CARREGOU — e o portão que olhava só metade da tela

As duas atividades de ontem foram ao ar com o **fundo da tela não carregando**.
O gerador de imagem salva **PNG**; o esboço escrevia `<pre>_fundo.jpg` no
`conteudo.json`; e o motor monta `url(img/<fundo>)` **literal**. Extensão errada
= imagem que não existe. Sem erro no console, sem quadradinho vazio, sem nada:
só a tela lisa, sem a rua, sem o galpão.

**Por que nenhum portão pegou:** o `_qa/imagens.js` já conferia fundo de CSS —
mas varria apenas `#app` e seus filhos. O fundo da atividade mora no **`#bg`**,
que fica **fora** do `#app`. Ele imprimiu, com todas as letras, *"toda figura da
atividade carrega"*.

E a correção certa não era acrescentar `#bg` à lista: era **parar de ter
lista**. Agora ele varre a página inteira (`body, body *`). O que a criança vê
não pede licença para estar dentro de um seletor meu — e uma lista de lugares
onde procurar é uma promessa de esquecer o próximo.

Consertado nos três lugares, que é como um defeito destes se fecha de verdade:
o `esboco.py` (nasce `.png`), as duas atividades no ar, e o portão.

---

## EXEMPLO EM COMENTÁRIO SE ESCREVE COM MARCADOR (ago/2026)

Duas vezes no mesmo dia, e as duas do mesmo jeito: um comentário que **cita um
identificador de verdade** faz o portão ver um fantasma.

- No `_qa/beco.py`: o comentário que eu escrevi explicando o conserto repetia,
  por extenso, a frase de bancada que o portão procura no código vivo. Ele
  passou a acusar o próprio aviso.
- No `motor.html`: a lição sobre a chave da voz usava uma chave REAL
  (`op_<conta>` de uma atividade). Como o motor viaja para todas as atividades,
  o portão do resto-de-clone encontrava aquela chave num arquivo limpo e dizia
  *"marca de outra atividade"*.

**A regra:** exemplo em comentário usa **marcador** (`op_<conta>`, `<pre>_f01`),
nunca um identificador copiado de uma atividade. Comentário também é texto, e o
portão lê o arquivo inteiro — como tem que ler.

---

## FOTO DE FUNDO É O PIOR FUNDO POSSÍVEL PARA TEXTO (ago/2026)

O 5º ano nasceu com uma FOTO de rua como fundo — enxaimel, placas, calçada — e
o auditor achou **17 textos entre 1,1:1 e 2,9:1**. Não era tinta errada: foto
tem meio-tom em todo lugar, e sobre meio-tom **nem a tinta clara nem a escura
enxergam**. Um galpão escuro perdoa; um céu liso perdoa; uma foto não.

Dois consertos, e eles são de naturezas diferentes — vale separar:

1. **Da ATIVIDADE** (`tema.css`): acalmar o fundo. A rua continua lá, atrás de
   um véu de papel claro (`#bg{opacity:.28}` + `body` cor sólida), e todo o
   resto passa a trabalhar sobre um tom só. É o que a gráfica faz quando
   imprime texto sobre foto.
2. **Das PEÇAS**: todo texto que não mora dentro de cartão nenhum ganhou **a
   mesa dele** — `.conta`, `.contador`, `.placar`, `.legenda`, `.leCel`,
   `.ctit`. Esse conserto vale para TODAS as atividades, não só para esta: o
   texto solto não escolhe o fundo em que vai cair.

**A regra:** `background` translúcido não é fundo — é uma média com o que
estiver atrás. Quem escreve texto solto precisa carregar uma mesa **opaca o
bastante para o pior caso**, e quem escolhe uma foto de fundo precisa acalmá-la
antes de pôr letra em cima.

---

## PRAZO FIXO NÃO SERVE PARA ESPERAR FILA (ago/2026)

O portão da voz dupla acusava uma fase diferente **a cada corrida** — a
assinatura de artefato de medição, não de defeito. Medindo: o elogio do acerto
chega **2,8 segundos** depois do clique, porque entra na FILA atrás da voz da
peça (o motor toca uma voz por vez, e isso é o certo). O portão montava a fase
seguinte antes disso e o rabo da anterior caía na janela dela.

Duas tentativas erradas antes da certa: esvaziar a lista (o rabo chegava
depois) e esperar 700 ms fixos (a fila é mais longa que qualquer palpite).
**A resposta é esperar ficar QUIETO** — esvaziar, deixar escoar, conferir se
chegou algo novo, repetir até o silêncio.

**A regra:** quando o que se espera é uma FILA, não se espera com relógio; se
espera com condição. Prazo fixo em cima de fila mede o relógio, não o programa.

## E A MINIATURA QUE ENCOLHIA DENTRO DO FLEX

`max-width:100%` não segura item de flex: item de flex **encolhe** por padrão
(`flex-shrink:1`). A miniatura da vitrine saía com 11px numa vaga de 26px, e o
portão do encaixe acusou "PEQUENA DEMAIS" dezenas de vezes — eu fui procurar o
defeito na largura da vaga, que estava certa. Quem manda a figura não encolher
é `flex:none`.

E o mesmo portão media o **fantasma**: a vaga ainda não conquistada é desenhada
com `opacity:0` e `scale(.4)` de propósito. **O que a criança não vê não tem
tamanho a julgar** — agora ele pula elemento invisível, inclusive quando quem
apaga é um antecessor.

---

## O DEFEITO ESPELHO: TINTA HERDADA DENTRO DE LADRILHO PRÓPRIO (ago/2026)

A varredura das 79 peças reprovou **oito**, todas pelo mesmo motivo, e ele é o
espelho exato da lição que já estava escrita aqui:

```css
.rnum{ color: var(--texto, #221a12) }   /* o número do mostrador do relógio */
```

`--texto` é a tinta **da atividade**, escolhida para o fundo dela. Mas esse
número cai numa superfície que a **própria peça** pinta — o mostrador creme, a
célula da cruzadinha, a pedra do dominó, a barra colorida do medir. Numa
atividade de tema claro isso virou **creme sobre creme**: 1,05:1 em 36 números
do relógio de uma vez.

E a reserva do `var()` não protege — ela só vale quando o token **não existe**,
e dentro de uma atividade ele existe sempre. Escrever a reserva dá uma falsa
sensação de cuidado.

**As duas metades da regra, que agora andam juntas:**

- quem cai no **fundo da atividade** usa `var(--texto)` (a peça não sabe onde
  vai cair, então segue o tema) — é o que o `_qa/cor_fixa.py` já cobrava;
- quem cai numa superfície que a **peça pinta** escreve a tinta, **e o seletor
  nomeia a superfície** (`.relo .rnum`, `.pc .dme .dnum`, `.palavra .ptxt`).

Sem o caminho no seletor o portão não tem como saber que existe fundo, e passa
a acusar "cor cravada sem fundo próprio" — as duas regras brigando pelo mesmo
elemento. **Escrever o caminho não é enfeite: é o que torna a regra
verificável.**

O portão aprendeu a segunda metade: `_qa/cor_fixa.py` agora também reprova
`color:var(--texto)` em elemento que descende de algo que a peça pintou.


---

## AS 79 PEÇAS FECHADAS (ago/2026) — e o que a varredura inteira ensinou

**Todas as peças do catálogo saem da bancada em código 0.** Medido peça por
peça, com o `_qa/peca.sh` completo (dez portões, incluindo o que joga a peça
sozinha até a medalha e o que erra de propósito para ver se dá para seguir).

**O número que importa não é 79: é 8.** Das 79, oito reprovaram — e as oito
pelo MESMO defeito, o da tinta herdada dentro de ladrilho próprio. Uma
varredura completa não serve só para carimbar: ela mostra qual defeito é
**sistemático**, e defeito sistemático não se conserta peça por peça, se
conserta na regra e no portão. As oito foram achadas em uma noite porque a
varredura roda em bloco; achadas uma a uma, chegariam ao Marcos em oito
atividades diferentes, ao longo de meses, cada uma parecendo um caso isolado.

**A regra de manutenção:** peça nova entra no catálogo com a bancada em 0, e a
varredura inteira roda quando um portão NOVO nasce — porque portão novo mede
coisa que ninguém tinha medido, e é exatamente aí que aparecem os oito.

---

## A BANCADA PERGUNTAVA SÓ UM LADO DO TEMA (ago/2026)

Esta era a dívida mais cara do catálogo, e ela estava anotada há semanas: **a
bancada roda a peça sobre o fundo ESCURO dela**. Dentro de uma atividade o
fundo é o que a atividade quiser — o galpão à noite, o céu do observatório, a
rua fotografada. Peça de tinta clara passa na bancada e morre na atividade, e
o print da bancada fica perfeito.

Medido agora, com o tema claro injetado: **44 das 79 peças** têm texto que
some. É a mesma família das catorze que chegaram até a atividade em duas
noites — não eram casos isolados, eram a ponta de 44.

**Por que o portão nasce com uma LISTA DE DÍVIDA** (`DIVIDA-TEMA-CLARO.txt`):
ligado de uma vez, ele derruba metade do catálogo na estreia. Portão que para a
fábrica não protege ninguém — a reação humana a ele é desligá-lo. Então:

- peça **nova** que falhar → **reprova** (a dívida não cresce);
- peça **da lista** que falhar → aviso, com o número (dívida conhecida);
- peça da lista que **passar** → **reprova pedindo para tirar o nome da lista**.

Essa última linha é o que faz a lista **só encolher** sem depender de ninguém
lembrar de limpá-la. Uma lista de dívida que não tem catraca vira desculpa
permanente; com catraca, vira plano de trabalho.

## DIZER O QUE FALTA NÃO É DIZER COMO PEDIR (ago/2026)

Pedido do Marcos, com todas as letras: *"Gere os prompts que eu preciso, que eu
gero aqui"* / *"As imagens pode me passar os prompts que eu gero"*.

O esqueleto entregava o `arte.json` — a **lista** das figuras que faltam. E
parava ali. Quem escrevia o prompt de cada uma era eu, na mão, uma por uma. Isso
tem dois custos, e os dois aparecem justamente na 1h30 de montar uma atividade:

1. **É o passo mais lento que sobrou.** Trinta e poucas fases se montam em
   minutos; onze prompts escritos à mão, não.
2. **Prompt escrito na hora sai diferente a cada vez** — e figura irmã vira
   figura estranha. A "irmandade" (mesma luz, mesma escala, mesmo acabamento)
   não vem do gerador: vem de o pedido ser **o mesmo molde** em todas.

Conserto: `_padrao/ESQUELETO/prompts.py`, chamado pelo `montar.py` no fim da
montagem. Ele escreve dois arquivos:

- **`<pasta>/_lote.json`** — pronto para o `gerar-imagens.yml` (`lote=` +
  `dest=<pasta>/img`), marcado `modelo: pollinations`, que é o caminho de R$ 0,00;
- **`<pasta>/PROMPTS-IMAGENS.md`** — a folha para o Marcos gerar na mão, com o
  nome exato de cada arquivo.

**O que ele sabe, e que a mão esquecia:**

- **`no text, no letters` em toda figura.** A IA sempre escreve letra torta, e
  em atividade de língua a letra É o conteúdo. Uma placa com letra errada não é
  enfeite ruim: é o contrário do que a fase ensina.
- **As duas camadas do mascote NÃO entram no lote.** Elas são **edição** da pose
  parada, e o arquivo diz isso com o aviso do tremor junto. Gerar as três do zero
  faz o boneco tremer 60 vezes por segundo, e **isso não aparece no print** —
  só com a criança na frente (medido pelo `_qa/mascote.py`, reprova acima de 15%).
- **O assunto da figura sai do CONTEÚDO, não do nome do arquivo.** Adivinhar por
  `lt_manga` → "manga" funciona até a primeira palavra ambígua (fruta ou roupa?).
  O rótulo que a criança vê ao lado da figura já responde, então é ele que manda.
  E a constante `CHAVES_DE_FIGURA` é **importada** do `montar.py`, nunca copiada:
  duas listas de chaves que deveriam ser iguais sempre acabam diferentes.

**E o esboço passou a nascer com o bloco `arte`** (duas linhas: `cenario` e
`mascote`). São elas que transformam "a friendly scene" em "a small sign painter
workshop in a german-style street in Blumenau". Escrever as duas leva um minuto
e é o que separa a figura irmã da figura estranha — sem elas o gerador cai no
título, que serve, mas sai genérico.

## A VOZ ERA DE OUTRA PESSOA — e não havia defeito nenhum a achar (ago/2026)

Palavras do Marcos, ouvindo a atividade pronta: *"Veja, você botou mascote
feminina e voz do Antônio"*.

A Oficina de Letreiros tem a **Lina**, uma menina pintora de letreiros — e falou
a atividade inteira com **voz masculina**.

**A regra já existia**, escrita dentro do próprio `entregar.yml`, com as palavras
dele de uma cobrança ANTERIOR: *"quando for feminino tem que pegar voz feminina"*.
O conserto daquela vez foi bom: cada atividade escreve a voz dela em
`<pasta>/voz.txt`, e o montador do esqueleto **se recusa a gerar** sem o campo
`voz` no `conteudo.json`.

**Só que esta atividade foi escrita À MÃO** — a pedido dele, sem o motor. Não
passou pelo montador, não tem `conteudo.json`, e por isso nasceu **sem
`voz.txt`**, caindo no padrão do gravador, que é masculino.

⚠️ **A lição de fundo, e ela vale para toda regra da casa:** a regra estava
guardada no caminho do ESQUELETO. Quem sai do esqueleto sai também de todas as
proteções dele. Regra que mora num caminho só não é regra da casa — é regra
daquele caminho. Quando o Marcos pedir algo "à mão", conferir o que a mão perde.

**E por que nenhum portão pegou:** não havia defeito a achar. O mp3 existe, o
texto bate com a tela, a chave da voz confere, o alto-falante toca, o contraste
passa. O que não batia era a **PESSOA** — e isso nenhum portão de texto ou de
pixel enxerga.

**O portão novo: `_qa/voz_do_mascote.py`** (3e da bancada). Descobre o gênero do
mascote pelo **artigo que a própria atividade usa** antes do nome ("a Lina",
"o Broto") — não por terminação, que mentiria em Teo, Órbi, Byte e Zezé — e
compara com a voz declarada. Reprova quando discordam **e também quando a
atividade não declara voz nenhuma**, porque não declarar não é neutro: é sair na
voz padrão sem ninguém ter decidido, que foi exatamente o que aconteceu aqui.

## A CHAVE REPETIDA NA MEMÓRIA — a fase que nunca acaba (ago/2026)

Ao aumentar o jogo da memória da Oficina da Lina de 8 para 10 pares, escrevi
duas cartas com a **mesma chave**:

    {k:"campo", a:"CAMPO", b:"M, porque depois vem P"}
    {k:"campo", a:"LIMPO", b:"M, porque depois vem P"}     <-- repetida

O motor casa duas cartas quando `a.k === b.k` e os tipos diferem. Com a chave
repetida, CAMPO casa com o motivo de LIMPO — e sobram cartas **órfãs, que nunca
fecham**. A criança vira, vira, vira, e a fase não termina. Não há mensagem de
erro, não há tela branca: só uma criança presa até a aula acabar.

**Por que nenhum portão via:**
- `node --check` passa — é dado, não sintaxe;
- o portão da imagem quebrada não pega as figuras que faltam nessas cartas,
  porque a figura da carta **só aparece depois que a criança vira**; a tela
  parada não a mostra;
- o jogador automático acusa "PRESO", mas só depois de quinze minutos de
  partida — e sem dizer o motivo, o que custou três rodadas de bancada para eu
  entender.

**Portão novo: `_qa/memoria_pares.py`** (3f da bancada). Em dois segundos e sem
abrir navegador, confere que **toda chave é única**, que **os dois lados do par
estão escritos** e que **a figura de cada carta existe na pasta**.

⚠️ **A lição maior: dado repetido é defeito, e defeito de dado não aparece no
código.** Toda lista em que um campo serve de CHAVE (a memória, o ligar, o
dominó, o par pergunta-resposta) precisa de um portão que confira a unicidade
dela — porque o motor confia na chave e não tem como desconfiar.

## A CARTA IRMÃ TEM QUE DAR PARA RECONHECER (ago/2026, o MESMO baralho)

Consertada a chave repetida, o jogo da memória da Oficina da Lina continuava
injusto — e desta vez o defeito não era do código. O verso de cada carta era o
**motivo** da letra, e motivo se repete:

    CAMPO, SEMPRE e LÂMPADA  ->  "M, porque depois vem P"   (três cartas iguais)
    OMBRO, TAMBOR e BOMBA    ->  "M, porque depois vem B"
    PONTE, VENTO e CANTO     ->  "N, porque depois vem T"

O motor casa pela chave `k`. A criança virava CAMPO e uma carta escrita
*palavra por palavra* igual à irmã dele — e ouvia som de **erro**, porque
aquela pertencia a SEMPRE. Nenhum portão pegava: a chave era única, os dois
lados existiam, a figura estava lá. **Era o jogo pedindo adivinhação.**

O conserto: um lado passou a ser a palavra com a **letra faltando** (`CA_PO`) e
o outro a mesma palavra **inteira**, com o motivo como linha de apoio embaixo.
Única, reconhecível — e ainda mostra onde a letra mora. De quebra, a partida
sorteia **6 pares dos 10**: cabe na tela da escola sem rolar e a partida
seguinte vem diferente.

**Portão: `_qa/memoria_pares.py`, item 1b.** Ele não compara o campo cru — compara
o que a criança **vê**, lendo quais campos entram na `face:` de cada lado. (No
teste de fogo o portão só pegou o defeito depois disso: contando o `tx:`, que é
reserva interna e não aparece, duas cartas gêmeas passavam por diferentes.)

⚠️ **A lição: par não se define pelo que o motor compara, e sim pelo que a
criança consegue distinguir.** Vale para o ligar, o dominó, o pergunta-resposta:
se dois pares mostram o mesmo texto, o jogo virou sorte.

## A BARRA QUE VOLTOU DE 81% PARA 66% (ago/2026)

As dezoito fases da Oficina foram escritas em ordem diferente da que ficou no
`FASES_MESTRE`, e cada `setProg` carregava o número da posição ANTIGA. No meio
do percurso a barra caía de **81% para 66%** — a criança sente que perdeu o que
já fez. O `_qa/progressao.py` viu e reprovou na primeira rodada; **quem não viu
fui eu**, que li só o último portão da lista.

⚠️ **Duas lições.** (1) Percentual escrito à mão é dívida: quando a ordem das
fases muda, TODOS se renumeram — o número tem que sair da posição no
`FASES_MESTRE`, não da memória de quem escreveu. (2) **Bancada se lê inteira.**
Ela imprime todos os portões e só o veredito fica no fim; parar no último erro
faz gastar rodadas inteiras num defeito por vez.

## TRÊS DEFEITOS QUE O MARCOS PEGOU JOGANDO (ago/2026, Oficina da Lina)

Ele abriu a atividade aprovada pela bancada e achou três coisas em poucos
minutos. As três tinham a mesma raiz: **a bancada mede o que eu ensinei a ela a
medir, e eu não tinha ensinado nenhuma das três.**

### 1. "O mascote não movimenta a boca ao falar, e sim o boné"

As três camadas do mascote — parada, falando, piscando — eram o **mesmo arquivo,
byte a byte**. E o portão `_qa/mascote.py` imprimia `muda 0.0% do corpo ok`, que
é o elogio máximo dele: ele foi escrito para pegar camada que muda DEMAIS (o
mascote treme), e zero passava folgado. **Zero não é camada perfeita: é camada
que não existe.**

Sem boca se mexendo, o único movimento que sobrava era o balanço do corpo —
`translateY` + `rotate(1.5deg)`. A Lina usa boné, e girar o corpo faz a aba do
boné varrer a tela: a criança vê o CHAPÉU se mexendo enquanto ela fala.

**Conserto:** o balanço virou respiração (sobe 3px, incha 1,5%, **sem girar**), e
as camadas passaram a ser edição de verdade da arte da IA — queda de queixo com
boca aberta para o `_fala`, pálpebra descendo para o `_pisca`. Sem crédito no
Gemini, a edição foi feita na própria arte, só na região do rosto: os pixels
continuam sendo os que a IA pintou.

**Portão:** `_qa/mascote.py` ganhou **piso** (`PISO = 0.15%`), com mensagem
própria: `COPIA` ≠ `TREME`. Chão junto com o teto.

### 2. "Também tem as borboletas do Broto"

O motor veio do Jardim e trouxe o fundo vivo: pólen e **três borboletas voando**
— numa oficina de letreiros, no meio de uma rua de Blumenau.

**Por que nenhum item do `_qa/clone.py` pegava:** este resto não é imagem (item
1), nem voz (2, 3), nem prefixo alheio (8), nem nome (10, 12). É **código que
desenha** — e código que desenha não tem nome de arquivo para conferir. A
variável se chamava `borbs`, que não casa com palavra nenhuma.

**O que denunciava, e eu quase joguei fora: o COMENTÁRIO.** O cabeçalho dizia,
com todas as letras, `BRILHO VIVO (pólen + borboletas)`. Quem clona o motor
clona o comentário junto — ele é a etiqueta de origem.

**Portão novo: `_qa/clone.py`, item 13.** O enfeite desenha uma COISA DE UM MUNDO
(borboleta, semente, planeta, papagaio...); se a atividade nunca fala dessa coisa
— nem na tela, nem nas falas — e ela existe igual no código de outra atividade,
é enfeite clonado. Três armadilhas pagas ao escrever este item:
- **efeito genérico não é coisa de mundo.** A primeira lista tinha `faisca`,
  `gota`, `poeira`: o portão acusou o inocente, que é o jeito mais rápido de
  ensinar a ignorar portão.
- **o texto da criança não se procura no arquivo cru.** Entre duas aspas
  quaisquer cabe um comentário inteiro, e foi assim que "borboletas" — que só
  existia num comentário — passou por "texto da tela" e absolveu o réu.
- **o filtro das lições é por BLOCO, não por linha.** A lição ocupa quinze
  linhas e só a primeira leva o ⚠️.

Na estreia ele achou sozinho mais um: `gotas()` — regar a plantinha do Jardim —
declarada e nunca chamada. E a limpeza tirou junto **44 classes de CSS mortas**
(vaso, prato, ferramentas, lupa) e dois comentários grandes descrevendo fases que
não existem aqui.

### 3. "Na primeira fase, o letreiro não está centralizado na placa"

A chapa é uma placa **pendurada**: o braço de ferro e a corrente ocupam a metade
de cima do PNG, então a tábua creme — a única parte onde se escreve — não fica no
meio da imagem. `align-items:center` centraliza no meio do RETÂNGULO e joga a
pintura em cima da madeira.

Medido na própria imagem: o creme vai de 16% a 77% da largura e de 52% a 85% da
altura, com centro em **46,5% × 68,9%**.

⚠️ **Regra que fica: quando a figura de fundo tem moldura, o texto se posiciona
pelo MIOLO medido na imagem, nunca pelo centro do retângulo.** Vale para placa,
cartaz, quadro, tela de TV, balão — qualquer arte em que a área útil não é a
figura inteira.

## O ESBOÇO NASCIA REPROVADO PELO PRÓPRIO MONTADOR (ago/2026)

A prova da esteira (`provar_esteira.sh`) parava no passo do `montar` com
**2 PROBLEMAS**: as fases de caça-palavras (f04, f20) traziam `PALDEF` (as
definições) junto com `MODO="lista"` — e a peça só olha `PALDEF` quando
`MODO="definicoes"`. O `montar.py` já tinha o guarda certo (`DEPENDE`), mas quem
**gerava** o esboço (`esboco.py`) copiava o exemplo cru da peça, com as duas
gavetas, e caía no próprio guarda. Ou seja: a máquina produzia um esboço que ela
mesma recusava.

O conserto foi em três lugares, todos apontando um para o outro:

1. **`esboco.py`** — ganhou o mesmo mapa `DEPENDE`. Ao copiar as gavetas do
   exemplo, **não emite a gaveta dependente quando a condição dela não bate**
   (PALDEF fora de MODO="definicoes" simplesmente não entra). O esboço sai
   montável de nascença.
2. **`montar.py`** — o aviso "meia-cheia" (`voce deixou X com o exemplo`)
   também passou a **ignorar a gaveta dependente quando a condição não bate**.
   Sem isso, a atividade CORRETA (modo lista, sem PALDEF) nascia avisada à toa —
   e aviso à toa ensina a ignorar aviso.
3. **`provar_esteira.sh`** — o `rodar()` contava **qualquer** exit ≠ 0 como
   FALHOU. Mas a convenção da casa é **0 = passou, 1 = reprovou, 2 = não deu
   para medir**. O `_prova30` (exemplo, sem par palavra+figura) faz o portão
   `figura_certa.py` devolver 2, honestamente. Agora exit 2 vira **n/a**, não
   reprovação.

**Regra que fica:** gaveta que só vale sob condição de outra (o `DEPENDE`) é uma
regra ÚNICA que tem que valer nos DOIS lados — quem gera (`esboco`) e quem
confere (`montar`). Se só um lado conhece, a máquina briga consigo mesma. E
NÃO MEDI (exit 2) nunca é reprovação; script que trata os dois igual derruba a
esteira por um portão que nem se aplica ao exemplo.

## DOIS DESTAQUES QUE SOMIAM NO TEMA CLARO (ago/2026, P2 das peças)

`reta-numerica` e `rotular` reprovavam no `_qa/tema_claro.js`. As duas tinham
texto que lia lindo no fundo escuro da PÁGINA DA PEÇA e sumia no papel de uma
atividade de **tema claro**:

- **reta-numerica**: o amarelo `#ffd54a` do destaque (`.placar b`, `.res b`)
  dava 1,14:1 no papel. Conserto: o amarelo **carrega a mesa dele** — uma
  pílula escura só em volta do número, que lê nos dois temas.
- **rotular**: `.rtitem` era texto quase-branco numa mesa branca **translúcida**
  (`rgba(255,255,255,.12)`); no tema claro os 12% de branco somem no papel
  (1,05:1). Conserto: mesa de texto claro tem que ser **escura e opaca**
  (`rgba(22,24,30,.82)`).

**Regra que fica** (a mesma que o portão já dizia, agora paga duas vezes): texto
que cai no FUNDO da atividade segue o tema (`var(--texto)`); texto que quer cor
própria — um destaque amarelo, um branco sobre card — **carrega a mesa dele**, e
a mesa tem que ser opaca o bastante para valer no tema claro E no escuro.
⚠️ O portão mede o texto que está na tela no RENDER; texto que a peça injeta
**durante o jogo** (o `.res` de feedback) ele não vê — por isso o conserto
cobriu as duas classes, não só a que o portão apontou.

## MEMÓRIA COM ARTE DE IA: O CAMPO É `img`, NÃO `fig` (ago/2026, RIGHT NOW)

Cobrança justa do Marcos: *"você já fez jogo da memória em várias atividades,
então não deviam haver erros novamente"*. Ele está certo — e o erro **não** foi
esquecimento meu do jogo da memória. Foi um **portão novo do esqueleto** rígido
demais.

O que aconteceu: a peça `memoria` mostra a arte de IA pelo campo **`img`** (que o
motor resolve com `imgEl`, pasta `img/`). O campo `fig` é OUTRA coisa: o desenho
**embutido** da peça (o dicionário `ARTE`). O EXEMPLO da peça em `pecas.json` usa
`fig` (desenhos embutidos), então o checador do `montar.py` — que deriva os
"campos que a peça lê" do exemplo — marcava `img` como campo estranho e a fase
saía com as cartas mostrando **"undefined"**.

Dois consertos (o defeito E o portão, como manda a casa):
1. **`montar.py`**: o check de campos de `dados` agora isenta os campos
   universais `img`, `imgsen`, `voz`, `vozsen` — QUALQUER peça os lê pelo motor,
   estejam ou não no exemplo dela. (O check gêmeo já isentava "img"/"voz"; este
   não — agora os quatro.)
2. **`_padrao/DINAMICAS.md`**, armadilha da Memória: *"a arte de IA vai no campo
   `img`; o `fig` é só o desenho embutido; trocar deixa a carta 'undefined'."*

**Regra que fica:** portão que deriva "campos válidos" do exemplo de UMA peça não
pode reprovar campos UNIVERSAIS do motor (imagem e voz). E memória temática usa
`img` para a foto, `pal`/`sen` para os textos do par.

## CONTROLE `position:fixed` É INVISÍVEL PARA O JOGADOR (ago/2026, tangram)

O botão de girar do tangram (que fica NA peça, como no rachacuca) estava
`position:fixed`. O auditor-jogador (`_qa/jogador.js`) filtra os alvos clicáveis
por **`offsetParent !== null`** — para não clicar num botão escondido. E
**elemento `position:fixed` tem `offsetParent` NULL** (regra do CSS). Resultado:
o jogador não enxergava o botão de girar; colocava a primeira peça (que já
servia) e empacava em todas as que precisam girar → **"PRESO na fase 1"**, banca
reprovada. A criança conseguia (ela vê o botão); o auditor, não.

**Conserto:** o botão virou `position:absolute` com **coordenada de PÁGINA**
(somando `pageXOffset/pageYOffset`, senão ele desliza ao rolar). Aí
`offsetParent` é o `body` (não-nulo) e o jogador o alcança.

**Regra que fica:** qualquer controle que a criança toca — e que o
auditor-jogador precisa alcançar — **nunca é `position:fixed`**. Use
`position:absolute` (com coordenada de página) ou um elemento em fluxo. `fixed`
serve para moldura/HUD decorativo que o jogador não precisa clicar, não para
botão de jogo.

---

## Lições da atividade de inglês (RIGHT NOW, 9º ano, ago/2026)

**`confete` morava só no motorzinho de bancada.** A `memoria.html` chama
`confete(20)` a cada par, mas a função nascia no PRIMEIRO `<script>` da peça (o
motorzinho do MOLDE), e o integrador só traz o SEGUNDO. No jogo montado o
`confete` não existia → estouro calado, só com a criança na frente. O
`integrar.py` (portão `confere_contra_motor`) pegou ao integrar. **Conserto:**
`confete` virou FERRAMENTA do motor (injeta o próprio `@keyframes mcai`), útil a
qualquer mecânica. Regra: efeito visual que a peça chama e o motor não tem →
FERRAMENTAS, nunca no motorzinho de bancada.

**Moldura de foto: `object-fit:contain`, nunca `cover`.** A mata branca da "foto
instantânea" com `cover` CORTAVA 20–45% da figura (o `_qa/leiaute.js` reprovou
fase5 e fase10). `contain` faz a figura inteira assentar centrada; a sobra vira
a mata branca (o fundo já é branco). Vale para memoria/ouvir-achar e todo frame.

**Narração: "completa/complete/completar" a voz lê "complita".** Já estava no
`_qa/falas.py`; trocar por "falta/preencha/terminar". E o ENUN padrão da peça
`completar` também (era "que completa a frase").

**`montar` PRESERVA falas colhidas — inclusive órfãs.** Ao mudar o texto de um
enunciado, o `op_<hash>` antigo continua no `falas.json` e vaza para o `VOZOK`
(alto-falante apontando para MP3 que não existe). Ao trocar texto, remover as
falas órfãs do `falas.json` e remontar.

**`gerar-imagens.yml` + checkout esparso: a pasta do LOTE tem que entrar.** O
`/*.json` do esparso só pega JSON da RAIZ; um lote em `_rightnow9/_lote.json`
ficava invisível → "nao achei o arquivo do lote" (falhou 2×). Corrigido: o
workflow agora faz `sparse-checkout add "$(dirname lote)"` além do `dest`.

**BARRA DE PROGRESSO nova (motor).** Saiu a "vitrine de miniaturas" (o Marcos não
gostou); entrou uma barra estilo app de idioma: trilho de vidro, gradiente que
flui, brilho correndo, cometa que pulsa (você-está-aqui), tiques por fase, selo
"X/N". Decorativa (`pointer-events:none`). `poeVitrine(t, feitas)` mantém o
mesmo gancho; só `VITRINE.length` (nº de fases) importa agora. **Marcos aprovou.**

**Carta-legenda do jogo da memória.** A carta de FRASE nascia sem figura (de
propósito — figura igual dos dois lados vira "ache as gêmeas") e parecia "imagem
faltando". Virou LEGENDA DE JORNAL (papel creme, aspas, itálico) via classe
`tsen`. Combina com o tema e continua exigindo leitura.

## Voz bilíngue (atividade de inglês, ago/2026)

Ordem do Marcos: *"voz inglesa no inglês"*. O sistema de voz da casa usava UMA
voz (pt-BR) para tudo — numa atividade de inglês, as frases inglesas saíam com
sotaque forte. Agora o `montar` marca cada fala com `lang:"en"` quando o texto é
inglês (detector conservador `_idioma`: diacrítico PT ⇒ PT; senão conta sinal
EN vs PT fora das ambíguas "a/no/do", e só é EN quando o inglês domina ≥2×), e o
`entregar.yml` grava essas com `en-US-GuyNeural` (as demais seguem em português).
Atividade só-PT nunca marca nada ⇒ nada muda. Também: eh_fala aceita palavra de
2 letras com vogal ("Is"/"Am"), e `falas_dos_dados` grava o `c`/`r` da escolher
quando vêm como FRASE (eram mudos porque `c`/`r` são coluna nas grades).

## Dívida de tema claro ZERADA (P2, ago/2026)

As ~38 peças que o `_qa/tema_claro.js` reprovava (texto sumia num fundo claro)
foram fechadas. O padrão do defeito era sempre o mesmo: **`<b>` dourado
(`#ffd54a`) ou texto claro (`#f4efe6`) num placar/status/rótulo que fica direto
sobre o fundo da atividade** — bonito no escuro da bancada, invisível no papel.
Cura padrão: dar ao CONTÊINER (`.placar`, `.cont`, `.conta`, `.frase`, `.pist`,
`.reltopo`, `.tit`…) uma **mesa escura** (`background:rgba(22,24,30,.82);
color:#f4efe6`) — assim o dourado e o texto claro leem em qualquer fundo/tema.
Casos especiais: texto ESCURO sobre superfície ESCURA fixa (lâmpada, cena) →
texto claro; estado "agora"/preenchido que trocava a mesa por um translúcido
claro (`.cam.agora`) → manter a mesa, mudar só a BORDA. `DIVIDA-TEMA-CLARO.txt`
agora está vazio; o portão reprova se algum nome voltar sem conserto.

## Voz das fichas da `montar-frase` — a etiqueta grudava na palavra (P1, ago/2026)

A banca do RIGHT NOW (inglês 9º) reprovou com **"6 resposta(s) com alto-falante
mudo"** e, na colheita, falas-monstro: **"Isam/is/are", "cookingação -ing",
"Shequem"**. Um defeito, três lugares — e o conserto teve que ser nos três, senão
volta:

1. **A peça (`montar-frase.html`).** A ficha de apoio escreve a ETIQUETA da classe
   DENTRO dela: `frase.w[i] + '<i class="eti">'+CLA[..].r+'</i>'`. O `textContent`
   cru é "Is"+"am/is/are" = **"Isam/is/are"**. Cura: a ficha **DECLARA** o que a
   voz diz — `b.setAttribute("data-voz", frase.w[i])` (só a palavra).
2. **O montador (`montar.py`).** `w` estava em `CHAVES_MUDAS` porque na maioria
   das mecânicas é **largura** (int). Na `montar-frase` é a **lista de palavras**
   que a criança toca — ficavam sem alto-falante. Regra nova: **`w` como LISTA de
   strings vira voz** (cada palavra; inglês ⇒ `lang:"en"`). `w` inteiro (largura)
   não entra.
3. **O portão-jogador (`_qa/jogador.js`).** O coletor de voz (`limpo()`) lia o
   `textContent` e anotava a frase-monstro para gravar. Agora **honra `data-voz`**
   — a MESMA regra que o motor (`poeZap`) e o portão `vozresposta` já usavam. Três
   leitores do texto de uma resposta têm que concordar; dois honravam `data-voz`,
   um não, e era o que colhia errado.

Lição da casa: **quando um elemento mistura palavra + andaime (etiqueta, figura,
letra inicial), a resposta é `data-voz`, não deduzir do texto** — e todo mundo
que lê aquele texto (motor, colheita, portão) precisa honrá-lo no mesmo commit.

## Encaixe acusava a MEDALHA da telaFim (P1, ago/2026)

A banca reprovava TODA atividade montada no gate 1f (encaixe): "telaFim | .medal
ocupa so 10% da caixa dela" e ".cfoto ocupa so 16%". A regra "figura ocupa < 16%
do pai" existe para pegar **figura perdida numa moldura grande demais** — mas o
pai da medalha e a COLUNA `.centro` (que segura a tela inteira: medalha + título +
boletim + botões), e o da foto é a linha `.cracha`. Coluna de leiaute não é
moldura: é natural a figura ocupar pouca ÁREA dela (a medalha tem ~50% da LARGURA,
mas a coluna é alta). Cura no portão: a conta de ocupação só vale quando a figura
está **sozinha** na caixa (`parentElement.children.length<=1`) — aí sim o pai é
moldura. Com irmãos, o pai é leiaute e a regra não se aplica. Figura de verdade
perdida numa moldura (a foto sozinha no quadro) continua pega.

## Voz da fase passada esperando na fila (P1, ago/2026)

A banca (voz dupla, 1l) acusou "duas vozes juntas na fase 13" — de forma
CONSISTENTE nas 4 corridas, mas fase 13 (`quem-sou-eu`) NAO tem a frase acusada
("She is cooking.", que e da `montar-frase`). Era voz de OUTRA fase presa na
`_fila`: a casa toca uma voz por vez e guarda a próxima na fila; ao SOLTAR a
resposta da montar-frase enquanto o elogio tocava, "She is cooking." entrou na
fila — e a fila **não era limpa ao trocar de tela**, então a voz ficou guardada
e disparou NOVE fases depois, junto com o elogio do acerto da fase 13 (inocente).
No jogo real o tempo da criança escoa a fila; a banca, pulando de fase em fase,
a expunha. Cura no motor (`limpa()`): `_fila=null` ao desmontar a tela — a voz é
da TELA que a pediu. NÃO paro o que já toca (cortaria o elogio no meio quando a
peça troca de rodada), só descarto o que ficou ESPERANDO.

## Voz atrasada da peça caindo na fase seguinte (P1, ago/2026)

Continuação da lição acima. Achado com stack trace: a voz "She is cooking." não
vinha da `_fila` do motor — vinha de um **temporizador da própria peça**.
`ouvir-achar`/`caixas-de-som` têm `falaEmSeguida()`: a 2ª voz da tela espera o
motor calar e tenta por ATÉ 9s. A peça se protege com o contador `ger` (as
trocas de tela DELA). Só que quem trocou de fase foi o MOTOR (`montaFase`), e o
`ger` da peça não muda — então o `tenta` continuava vivo e disparava a frase
NOVE fases depois (fase 12 `ouvir-achar` → tocava na fase 13). Cura na peça:
`falaEmSeguida` guarda também `IFASE` (a fase do motor) e desiste se mudou. Regra
geral: **todo temporizador de peça que fala tem que morrer na troca de FASE, não
só na troca de tela interna** — o `ger` da peça é cego para o motor.

## Varredura completa das 79 peças (PRIORIDADE 2, ago/2026)

Rodei `bash _qa/peca.sh` em TODAS as peças do catálogo. 4 reprovaram e foram
consertadas (código 0 em cada uma):
 - **forca** — o `@media(max-width:400px)` encolhia as CASAS mas nunca o TECLADO;
   no 320×568 a 5ª fileira caía atrás da barra. Encolhi `.tecl` ao piso de toque.
 - **domino / criar-desafio / investigar-fonte** — o MESMO defeito de tema-claro:
   texto DOURADO/claro (`#ffe9a8`, `#f4efe6`) sem mesa própria, 1.0:1 sobre fundo
   de papel. Cura: **mesa escura fixa** (`rgba(22,24,30,.82)`) no container, e a
   cor clara mora NO container (pinta o fundo junto — `cor_fixa` exige), o texto
   filho HERDA. O dourado (hue) o `cor_fixa` não acusa; o quase-branco, sim.
Lição da casa: peça com acento dourado/claro que cai direto no fundo da atividade
precisa trazer a mesa dela — não dá para apostar que o tema é escuro. Os portões
`tema_claro.js` + `cor_fixa.py` já pegam sozinhos; o conserto é sempre o mesmo.

## LIGAR TEM TETO DE 6 PARES (RIGHT NOW, ago/2026)

Aumentei a fase de `ligar` de 6 para **8 pares** para a atividade "durar mais". A
banca reprovou no jogador: **PRESO em "MAKE IT -ING" a 38%** — com 8 pares (16
itens + linhas cruzando), a coluna estoura e alvos ficam fora do alcance; o
auto-jogador não fecha, e a criança no celular também não. Com 6 pares passa liso
(a outra fase de `ligar`, a 6, nunca travou). **Regra da casa: `ligar` no máximo
6 pares.** Para "durar mais" sem estourar, cresça as mecânicas que escalam —
`relampago`, `caca-palavras`, `escolher`/`completar` de texto, `forca` — não o
`ligar`/`memoria`/`classificar`, que têm tabuleiro fixo. Quem pegou foi o portão
`0f2` (colher.py, o jogador de verdade); ainda não há teto medido no `montar.py` —
candidato a virar aviso lá (item para o `_qa`/montador).

## PEÇA DE VIDRO: TEXTO ESCURO FIXO + VIDRO LEITOSO (RIGHT NOW / escolher, ago/2026)

O Marcos escolheu a família de **vidro fosco** para o `escolher` (moldura da foto
com brilho; enunciado e opções em vidro **sem** brilho — "um brilho, uma estrela",
só na foto). Dois defeitos pagos ao montar isso, ambos de CONTRASTE:
1. **`var(--texto)` no texto da opção** → num tema de exemplo escuro a variável é
   CLARA, e texto claro sobre vidro claro deu **1.08:1** ("O CAULE" sumiu, medido
   pelo `contraste_fundo.py`). **Cura: cor de texto ESCURA FIXA** (`#1a2129`),
   nunca `--texto`, em peça de vidro (o vidro é sempre claro).
2. **Vidro translúcido demais** → o `backdrop-filter` **não existe no PC velho da
   escola**, então a COR do vidro sozinha (sem o blur) tem que segurar 4.5:1 sobre
   QUALQUER fundo. **Cura: vidro LEITOSO** — branco de `.72`→`.58` (gradiente),
   nunca translúcido de verdade. Pior caso (sobre preto, sem blur) ≈ 148 cinza →
   texto escuro passa. Acento colorido (o negrito verde) precisa ir mais escuro
   (`#0f3e0c`; `#155a10` dava 4.03).
Lição da casa: **vidro = texto escuro fixo + branco ≥ .58**. O `contraste.js`
pega sozinho; o conserto é sempre este.

## LIGAR (E 2 COLUNAS): ITEM EM FLEX, ALTURA IGUAL, SENÃO DESALINHA (RIGHT NOW, ago/2026)

O Marcos: "os botões precisam ficar mais distanciados para as linhas aparecerem
melhor, e alinhados". Causa medida (foto): o `.lig` era `display:block`, e o
**alto-falante que o motor injeta QUEBRAVA para a 2ª linha** nas palavras longas
(a coluna `-ing`) — só aquela coluna ficava mais alta, as duas desalinhavam e a
linha de ligação saía torta. **Cura: `.lig` em FLEX na linha** (palavra + som
sempre juntos) + `min-height` fixo → os dois lados na MESMA altura de fileira.
Vão central maior (colunas 44% + 12% de vão, era 4%) → linha mais longa e visível.
⚠️ `margin-bottom` folgado (16px) estoura a **janela baixa** da escola (o
`leiaute.js` pegou: 2 fileiras presas atrás da barra) → `@media (max-height:560px)`
encolhe altura/respiro. Regra: em mecânica de 2 colunas, item sempre flex de
altura fixa, e todo espaçamento folgado precisa de recuo na janela baixa.

## JOGADOR: PASSO-A-PASSO PRECISA DE SOLVER DE ORDEM (P2, ago/2026)

O `passo-a-passo` (ordenar a receita: a crianca poe os passos na ordem e o mundo
executa) fazia o auditor-jogador entrar em LACO ate o timeout (exit 124) — ele
clicava `[data-qa]` ao acaso, a ordem saia errada, a receita nunca fechava. Nao
era defeito da PECA e sim do AUDITOR (ele nao sabia jogar a mecanica). Conserto no
`_qa/jogador.js`: solver que le a vaga (`data-vaga` INTEIRO = posicao certa) e clica
a fonte de mesmo `data-qa`, par por par, e no fim o botao "Comecar". Distingue do
quebra-cabeca (cujo `data-vaga` e "li_co", com "_") e usa SO atributos de dado
(nao classe — o integrador renomeia `.cam`, nunca o `data-vaga`). Regra da casa:
mecanica de ORDENAR/PAREAR precisa publicar em `data-qa`/`data-vaga` o alvo certo,
e o jogador precisa do par toque->vaga; clicar ao acaso nunca fecha. Testado:
passo-a-passo e quebra-cabeca exit 0.

## LIGAR: ALTO-FALANTE AO LADO VAZA NO CARTAO ESTREITO -> EMPILHAR (RIGHT NOW, ago/2026)

O Marcos: "nao ficaria melhor um pouco mais largo para os textos nao ficarem
cortados?". Ele estava certo: com palavra + alto-falante LADO A LADO, nos cartoes
estreitos das 2 colunas o `.zap` VAZAVA 4-5px do `.lig`. O `peca.sh` standalone
NAO pega (la o cartao e mais largo); quem pegou foi o portao 1h `vaza.js` na
atividade MONTADA. Tentar so reduzir padding/margem do som NAO resolveu.
Cura (o Marcos preferiu LADO A LADO, empilhar 'ficou feio'): colunas mais LARGAS
(47% + 47% + 6% de vao) + alto-falante COMPACTO no `.lig` (34px, margem 3) — assim
palavra + som cabem lado a lado sem o `.zap` sair. Regra: 2 colunas com alto-falante
-> cartao largo o bastante + som compacto; medir com `vaza.js` na atividade MONTADA,
nao so no `peca.sh`.

## O QUADRO COLAPSA: FILHO DE FLEX-CENTER SEM LARGURA (RIGHT NOW / ligar, ago/2026)

Por que o ligar deu TANTA volta: o defeito nao era o % das colunas nem o padding —
era a RAIZ. A `.centro` do motor e `display:flex;align-items:center`. Um filho de
bloco SEM `width` num flex assim NAO preenche: ENCOLHE para o conteudo. A `.ligbox`
(sem width) colapsava para ~196px, os cartoes de coluna ficavam ~86px e a palavra
+ alto-falante estouravam. Cada ajuste de superficie (fonte, padding, empilhar,
gap) mascarava, nunca curava — so medindo a largura real do quadro (196px) apareceu.
**Cura:** todo container de area-de-jogo que vira filho da `.centro` precisa de
`width` (ex.: `width:94%;max-width:360px`), senao colapsa. Vale para QUALQUER peca
de coluna/tabuleiro. Ja aplicado no ligar e na teia-alimentar (mesma copia).
Sintoma que o Marcos ve: "as palavras saem do quadrado". O `vaza.js` pega o
overflow (via o alto-falante), mas a cura definitiva e dar largura ao quadro.

## MOLDURA DE VIDRO: O PADRAO (RIGHT NOW / escolher + completar, ago/2026)

O Marcos fechou o visual das fases com imagem: **moldura de vidro fosco com
brilho** (o mesmo brilho do verso da carta de memoria), **sem cartao branco atras
da imagem**, botoes de **vidro** e acerto com **selo verde "certo"**. Duas licoes
de implementacao pagas aqui:
1. **A moldura tem que COLAR na imagem** ("a moldura nao precisa ser tao grande
   com a imagem pequena"). NAO usar `fit-content` numa `.qfig` com imagem: o
   `fit-content` usa a largura NATURAL do PNG (grande) e sobra vidro. Padrao que
   funciona: `.qfig{width:<fixo>px;max-width:<n>vw;padding:5px}` + `.qfig img{
   width:100%;height:auto}` — a imagem preenche a moldura, borda de vidro fina e
   UNIFORME. Larguras por tela via `@media` (ex.: 186 / 140 baixa / 200 alta).
2. **Borda fina e padrao** (padding 5px). Se ainda sobrar vidro, e margem
   EMBUTIDA no proprio PNG (recorte com borda vazia) — resolve regerando a imagem
   como recorte transparente, nao no CSS.
Isto e o PADRAO de toda fase com imagem na moldura (escolher, completar e as
proximas). O prompt-padrao da imagem (fundo transparente, sujeito unico) esta
anotado dentro de `_padrao/pecas/escolher.html`.

## _PROVA30 NAO MORA NO GIT (fonte de drift, ago/2026)

A `_prova30` e a fixture da esteira: `provar_esteira.sh` faz `rm -rf _prova30` e
a REGENERA do zero a cada rodada (esboco.py + montar.py). Ela estava com 8
arquivos RASTREADOS no git — entao toda prova deixava "uncommitted changes", o
stop-hook reclamava e a copia local escorregava (drift) sem parar. Cura: `git rm
-r --cached _prova30` + `_prova30/` no `.gitignore`. Regra: **artefato 100%
regeneravel nao se rastreia** — se um script recria do nada, ele so faz ruido no
git. (A prova continua valendo: roda-se `provar_esteira.sh` e le-se o EXIT=0; nao
precisa versionar o resultado.)

## CHAVE DE IMAGEM VAZANDO NA VOZ, PELO `opcoes` (motor, ago/2026)

Remontando a Padaria com o montador de hoje, o `falas.json` ainda saía com SEIS
falas que eram nome de arquivo: "pd_pao", "pd_bolo", "pd_mel", "pd_queijo",
"pd_leite", "pd_ovo" — MP3 dizendo "pê-dê pão". Causa: mecanica com CATALOGO
(arrastar-lugar/classificar) guarda em `opcoes` as CHAVES do catalogo, nao o
texto (o texto mora no catalogo). `opcoes` NAO pode entrar em `CHAVES_MUDAS` —
calaria as opcoes-frase da `escolher`. Entao a chave chegava ao `eh_fala` e
passava: "pd_pao" tem vogal, e minuscula, "parece palavra".

Cura na ORIGEM: `eh_fala` agora rejeita o formato `^[a-z]{2,4}_[a-z0-9_]+$`
(prefixo_nome) — a MESMA regra que o `_qa/falas.py` (linha 79) ja usava no fim da
esteira. O defeito era o filtro do montador nao conhecer a regra do portao.
Licao geral: **palavra de gente nunca tem "_"**; string nesse formato e sempre
referencia/chave, nunca fala. (A Padaria no ar segue com o falas.json velho ate o
Marcos pedir para remontar/republicar — nao se mexe em atividade publicada.)

**Conferido que o fix NAO emudece a peca:** a palavra que a crianca ouve mora no
`voz`/`nome` do CATALOGO ("voz":"pão"), nao na chave. Remontando a Padaria: "pão",
"PÃO", "bolo", "mel" seguem na fila de voz; so "pd_pao"/"pd_bolo" sairam. E a
varredura de TODOS os `_*/conteudo.json` achou o padrao `prefixo_nome` fora de
chave-muda SO no `opcoes` da Padaria (12, todas chave de imagem) — zero falso
positivo, nenhuma fala de gente silenciada.

## NOVO PADRAO: 6-7 MECANICAS x 6 FASES (decisao do Marcos, ago/2026)

Palavras dele, repetidas ate eu ouvir: *"eu quero so 6 ou 7 mecanicas com 6
fases cada... as atividades serao assim de agora em diante para ser mais
rapido"*. Troca deliberada: menos VARIEDADE-de-mecanica por mais VELOCIDADE-de-
producao (menos peças diferentes p/ autorar, menos arte p/ gerar). A
dificuldade sobe DENTRO de cada mecanica (6 fases da mesma, em degraus), nao
trocando de gesto. O `minimo` do montador caiu para **6** (era 10 p/ pequeno,
16 p/ maior). As redes de qualidade continuam: `_qa/padrao.py` cobra teto de
40%/gesto, minimo de 4 gestos e "nada de gesto colado" — 6 mecanicas x 6 fases
= ~17% cada, folgado. Esboço: `--fases 36 --mecs a,b,c,d,e,f` (ou 7 x 6 = 42).

## DURACAO NAO VIA A ATIVIDADE MONTADA (portao, ago/2026)

O `_qa/duracao.py` contava itens por `var X=[...]` MAIUSCULO — mas o montador
escreve o conteudo real como `FASES = [...]` (json.dumps, SEM `var`), invisivel a
esse regex. Resultado: o portao via so os EXEMPLOS das pecas e estimava ~21 min
numa atividade com 36 fases DE VERDADE — e reprovava. Como o novo padrao e 6
mecanicas x 6 fases, ISSO REPROVARIA TODA ATIVIDADE NOVA. Conserto: `_extrai_fases`
acha o array `FASES` por casamento de colchetes, le como JSON e conta o trabalho
real por fase (dados/RODADAS/FICHAS) com custo por gesto. Medido sem regressao:
Lojinha 21->56 min, Padaria 46, RIGHT NOW 51 — as tres passam.

## PROGRESSAO: "JOGAR DE NOVO" DA PECA NAO E BARRA VOLTANDO (portao, ago/2026)

A tela de fim de uma peca (100%) tem um botao que chama a ENTRADA da peca
(pecaLigar/pecaEscolher...) para recomecar do 0%. O `_qa/progressao.py` lia isso
como "a barra voltou 100->0" e reprovava — mas e REPLAY (escolha da crianca, igual
telaCapa), e numa atividade MONTADA e codigo MORTO (o motor avanca as fases). Havia
ainda 4 `fimDaPeca` com o mesmo nome (colisao entre pecas); sobrevive o da ultima.
Conserto: o portao isenta transicao `pecaX` indo de >=95% de volta a 0% (replay),
alem do telaCapa que ja isentava. Sem regressao: Lojinha/Padaria/RIGHT NOW passam.

## P1/P2 CONFERIDOS + peca.sh nao acusa o MOLDE (ago/2026)

Varredura das 80 pecas com `bash _qa/peca.sh`: **79 OK, e o 80o e o MOLDE**
(template em branco da oficina, base de CSS do `integrar.py`, fora do catalogo).
Ele estourava em 150s (o jogador nao acha fase para jogar) e aparecia como
"FAIL(124)" — acusacao do inocente. `peca.sh` agora reconhece `MOLDE.html` e sai
0 dizendo o que ele e. P1 (motor do Esqueleto) fica provado de ponta a ponta: a
Lojinha (36 fases > 32) foi montada pelo `montar.py` e passou a banca inteira
EXIT 0 nesta mesma sessao. Nada a reconstruir em P1/P2.

**Stress-test do motor na GAMA de mecanicas (2026-08-16).** Para caçar bug de
`montar.py`/gaveta antes do Marcos (foi assim que apareceram o `UNM` congelado e
a ficha muda da Lojinha), montei DOIS exemplos descartaveis de 32 fases cobrindo
o resto do leque: (1) escolher, completar, ordenar, cruzadinha, forca,
caca-palavras; (2) ligar, digitar, arrastar-lugar, sombra, montar-frase, relogio,
labirinto, sete-erros, misterio, pintar-desenho. Os dois montaram EXIT 0 e
passaram TODOS os portoes de estrutura (funcoes, classes, progressao, fluxo,
beco, dinamicas, padrao). Somando a Lojinha, o motor esta provado em ~16
mecanicas sem defeito estrutural novo. Os exemplos sao scratch (como o `_prova30`,
nao moram no git) — o valor e a verificacao, nao o arquivo.

## FIGURA TEM QUE SEGUIR O VALOR — E O PRINT DA TELA PEGA (Lojinha, ago/2026)

Ajuda visual em TODA fase (1o ano): a peca `ligar` ganhou figura opcional na
ponta (`img`+`voz` na gaveta), o `comparar` ganhou modo DINHEIRO (a cedula no
lugar dos blocos, via `imgA`/`imgB`) e a `memoria` passou a mostrar a cedula.
Dois defeitos so apareceram no PRINT da tela montada (portao nenhum viu):
  1. **comparar embaralhava so o valor.** `baguncar([a,b])` trocava vTopo/vBaixo
     mas `imgA`/`imgB` ficavam presos a a/b — a moeda de 1 real saia com o numero
     "2". Cura: embaralhar o PAR `{v,img}` JUNTO. Licao: quando numero e figura
     sao a MESMA resposta, viajam juntos pelo sorteio, nunca em listas paralelas.
  2. **memoria usava `fig`/`figsen`** (desenho embutido) em vez de `img`/`imgsen`
     (arte de IA) — a MESMA licao do RIGHT NOW. As cartas saiam so com texto.
     Cura: `img` de um lado (a cedula), o valor por extenso do outro.
  No modo dinheiro o rotulo "TURMA AZUL/LARANJA" do comparar sai vazio (nao faz
  sentido). **Licao geral: OLHAR o print da tela MONTADA antes de entregar — ha
  defeito de conteudo (figura trocada, rotulo alheio) que so o olho pega.**

## GAVETA CONGELA CONSTANTE DA PECA — E ELA ENVELHECE (Lojinha, ago/2026)

O `comparar` compara valores; a atividade de dinheiro chega a 20 (a nota de
vinte). O painel ficava MUDO no alto-falante do 20: `nomeNum(20)` devolvia "20"
cru. Investigado ate o fundo (a lista `UNM` no INDEX tinha 21 nomes, ate "vinte",
e mesmo assim o runtime usava 13). Causa: o motor da montada tem a linha
`if(_d.UNM !== undefined) UNM = _d.UNM;` — a gaveta secundaria sobrescreve a
constante da peca com o que o `conteudo.json` guardou. E o `esboco.py`, ao
esbocar a fase, CONGELOU `dadosExtra.UNM` com o default de ENTAO (13 nomes,
ate "doze"). Depois a peca cresceu para 21, mas o conteudo continuou mandando 13.

**Licao geral:** gaveta secundaria que e CONSTANTE da peca (nomes de numero,
textos de andaime fixos) NAO deveria ser congelada no `conteudo.json` — ela nao
e conteudo da atividade, e conteudo da PECA, e envelhece. Quando bater um
"a peca tem X mas roda com Y", suspeitar de `dadosExtra` sobrescrevendo.
**Conserto desta:** removido `UNM` do `dadosExtra` das 6 fases comparar do
`_lojinha/conteudo.json` — sem ele o motor mantem o `UNM` (21) da peca. O
`montar.py` passou a gravar a quantidade por extenso das fases comparar
(`_num_extenso`, a MESMA lista do `UNM`, com aviso cruzado nos dois arquivos).
Quem PEGOU o defeito sozinho foi o `_qa/vozresposta.js` (acusou "20" mudo) — a
rede de seguranca funcionou; a gaveta congelada so vira problema visivel quando
mexe em algo que um portao ja mede (aqui, a voz da resposta).

## 1º ANO NÃO LÊ: GAVETA/RÓTULO PRECISA DE FIGURA + SOM (Lojinha, ago/2026)

Marcos, jogando o `classificar` da Lojinha: *"a criança não sabe ler, ela não
consegue ler o que está escrito em cada quadrado — moeda ou cédula; precisa ter o
botão de som e uma imagem de moeda quase transparente e do outro lado uma imagem
quase transparente de cédula"*. A gaveta dizia só a PALAVRA ("MOEDA (de metal)",
"NOTA (de papel)"). No 1º ano isso é uma tela muda para quem ainda não lê: a
criança escolhe pela sorte.

**Conserto (na peça `classificar`, vale para toda atividade que a use):**
- cada gaveta ganhou um **alto-falante** (`.gzap` no cabeçalho `.ghead`, ao LADO
  do nome — nunca em cima, senão o portão leiaute reprova botão sobre texto) que
  fala a `voz` da gaveta ("moeda"/"nota");
- e uma **marca d'água** grande e quase transparente (`.gwater`, opacity ~.20,
  `pointer-events:none`, atrás das fichas) com a figura do dinheiro — moeda numa
  gaveta, cédula na outra. A criança reconhece pelo DESENHO, não pela palavra.
- no `conteudo.json` a gaveta passou a levar `img` (a figura) e `voz` (a palavra
  limpa); `voz` já é OPCIONAL universal no `montar.py`, `img` já existia no exemplo.

**Lição geral:** toda **categoria/rótulo que a criança do 1º–2º ano tem que
distinguir para agir** (gaveta de classificar, alvo de ligar, bin de arrastar)
precisa de **figura + som**, nunca só texto. Texto sozinho é loteria para quem
está se alfabetizando (o mesmo princípio do alto-falante nas respostas).

## PEÇA POSTA NA BANDEJA/CESTO NÃO PODE VAZAR DA CAIXA (Lojinha, ago/2026)

Marcos, sobre a `caixa-dinheiro`: *"quando a criança arrasta a nota ou a cédula
para juntar o valor, isso se adeque automaticamente para não ficar de fora da
caixa"*. As peças já postas eram `.chip` em `inline-block` sem quebra: ao juntar
muitas (ex.: 8 moedas de 1 real para pagar 8), elas transbordavam para fora da
`.balcao`.

**Conserto:** a bandeja virou um flex `.trayin` com `flex-wrap` (as peças QUEBRAM
em linhas) e as peças ENCOLHEM conforme enchem (`.balcao[data-cheio="2"/"3"]`
reduz a foto e a fonte, e some o "TIRAR" no mais cheio). E a peça na bandeja
passou a ser a MESMA FOTO do dinheiro da carteira (`dinDe(v)` acha a figura pelo
valor), não mais um chip de texto — pedido antigo do Marcos ("a caixa usa as
imagens") agora vale também DENTRO da bandeja.

**Lição geral:** qualquer área que RECEBE peças em quantidade variável (bandeja,
cesto, prato, carrinho) tem que ser **flex-wrap + encolher por quantidade** —
nunca `inline-block` fixo, que transborda quando a criança põe mais do que o
esperado. Contar com "vão caber poucas" é o mesmo erro que já vazou antes.

## PADRÃO 1º/2º ANO — CLASSIFICAR "SÓ IMAGEM" (Lojinha, ago/2026, guardar p/ os menores)

Decisão do Marcos: guardar esta configuração para toda atividade de classificar
dos **menores** (1º/2º ano, quem ainda não lê). O que faz esta fase funcionar:

- **Gaveta SEM texto**: nada de rótulo escrito ("MOEDA (de metal)"). O que
  identifica a gaveta é a **FIGURA** (moeda numa, cédula na outra) + o
  **alto-falante** que diz o nome ("moeda"/"nota"). No `conteudo.json` a gaveta
  leva `img` (a figura) e `voz` (a palavra); o `n` fica só como voz de reserva.
- **Quadrados GRANDES, imagens GRANDES, AFASTADOS**: `.cam` min-height ~210px,
  `.gwater img` ~92%/max 180px a 80% de opacidade (20% transparente), `.gavs`
  gap ~26px. A figura é grande de propósito — é ela que faz o quadrado ser
  grande. Sem texto o `.gavs` precisa de `width:100%`+`align-self:stretch` e o
  `.cam` de base de flex não-zero, senão colapsa numa barra fina.
- **Espaço para arrastar**: a ficha da vez fica EM CIMA (numa moldura tracejada),
  as duas gavetas grandes embaixo, bem separadas. A criança **toca na ficha e
  depois na gaveta**, ou **arrasta** a ficha até ela — os dois caminhos valem
  (mouse, dedo e toque simples).

Isto é o padrão da casa para os pequenos; copiar, não reinventar.

## COLHEITA ALEATÓRIA NÃO PEGA TODA VARIANTE DE DICA (Lojinha, ago/2026)

A dica do jogo da memória no modo só-imagem é "Ouça: <valor>. Ache a figura
igual." — uma frase por VALOR de carta (1, 2, 5, 10, 20 reais). O `colher.py`
joga ao ACASO, então pegou só as variantes que a sorte fez o andaime disparar
(1 e 2 reais); a banca, jogando mais, achou "5 reais" MUDO. Se eu só regravasse
o "5 reais", "10" e "20" ficariam mudos na próxima criança.

**Lição geral:** quando uma fala dinâmica tem um CONJUNTO FINITO e conhecido de
variantes (um por item/valor), não conte com a colheita aleatória — REGISTRE
todas de propósito no `falas.json` (o montador preserva as falas colhidas cujo
id não é gerado). Colheita é boa para o texto imprevisível; para o previsível,
enumere. Aqui: todas as "Ouça: N reais. Ache a figura igual." das cartas.

## BANCO É ISENTO NO arte_propria (Lojinha, ago/2026)

O `_banco/montar.py` sempre prometeu: "o portão `_qa/arte_propria.py` continua
reprovando cópia entre atividades; o que vem do banco ele passa a aceitar". Mas
a isenção NUNCA tinha sido implementada no portão. A Lojinha reutilizou 6
brinquedos do banco (bola, carrinho, boneca, cubo, pião, urso — objetos NEUTROS,
como o Marcos mandou: "consulte o banco de imagens ou outras atividades") e o
`arte_propria` reprovou byte-a-byte contra `_fabrica`.

**Conserto:** `arte_propria.py` agora isenta toda imagem cujo sha esteja em
`_banco/img` (objeto neutro registrado = vocabulário reutilizável). Arte de TEMA
(mascote, avatar, cenário, medalha) NÃO entra no banco, então continua reprovando
— a regra "clonar a arte é proibido" segue de pé para o que é identidade.
**Lição:** promessa em manual sem portão que a cumpra é promessa quebrada; ao
documentar uma isenção, implementá-la no portão no mesmo movimento.

## CÓDIGO DE CONTROLE DO SETE-ERROS VIRANDO FALA — E A PRESERVAÇÃO O FIXA (Lojinha, ago/2026)

O SETE-ERROS descreve as diferenças em `dadosExtra.MUDA = [{sp:1, acao:"img",
val:"lb_cubo"}, {sp:2, acao:"esc", val:0.6}, {sp:0, acao:"sumir"}]`. As chaves
`acao`/`val`/`sp`/`esc` são CÓDIGO de controle (o que a peça faz com cada zona),
não texto de tela. O montador desce o `dados`/`dadosExtra` com `falas_dos_dados`
e mandou gravar a voz de "sumir", "img", "esc" — três MP3 mudos (`op_4jn7dh`,
`op_3779qa`, `op_3776io`), que ainda entraram no `VOZOK` (o alto-falante) porque
o `VOZOK` nasce da lista de `falas`.

**Conserto (origem):** `acao sp val esc` entraram no `CHAVES_MUDAS` do
`montar.py` — chave de controle é muda.

**A ARMADILHA que quase enganou:** só corrigir o gerador NÃO limpou o
`falas.json`. A preservação da colheita ("a colheita não pode ser apagada",
`montar.py` ~1304) guarda TODA fala do `falas.json` antigo cujo `id` não é mais
gerado — então as três, uma vez gravadas por um mount pré-fix, ficavam
**preservadas para sempre** e voltavam ao `VOZOK` a cada remontagem. Remontar
não bastava; foi preciso PURGAR as três do `falas.json` e só então remontar.
**Lição geral:** ao consertar o que o montador GERA, lembrar que ele também
PRESERVA — um resíduo já persistido sobrevive ao fix da origem e precisa ser
apagado do `falas.json` à mão.

## PLAQUINHA (SELO) DUPLICADA EM PEÇA DE TELA CHEIA (Lojinha pintar, ago/2026)

O motor SEMPRE põe a plaquinha da fase (o `.selo`) em cima — o texto vem do
`conteudo.json` (`fase.selo`). As peças comuns desenham a DELAS dentro de
`.pecabox` e o motor esconde por CSS (`.pecabox .selo{display:none}`). Mas o
`pintar-canvas` monta a PRÓPRIA `.tela` (canvas de tela cheia) e fica FORA de
`.pecabox` — a regra do CSS não a alcança. Como a peça também desenhava
`el("div","selo","HORA DE PINTAR")`, saíam DUAS plaquinhas idênticas, uma
embaixo da outra, comendo a tela curta do monitor da escola.

Nenhum portão via: `node --check` passa (é DOM), contraste/leiaute passam (a
plaquinha é legível e cabe). É REDUNDÂNCIA — não estoura, só rouba espaço. Foi o
olho, no print, que viu.

**Conserto (código):** a peça de tela cheia NÃO desenha o próprio `.selo` — o
selo é do motor; a peça só põe o balão (a instrução da rodada).

**Conserto (portão):** `_qa/selo.js` (portão 3h da banca) RENDERIZA cada fase e
conta os `.selo` VISÍVEIS — dois ou mais na mesma tela reprova. Estático não
serve: TODA peça monta `.tela` e `.selo`; o que muda é o embrulho em `.pecabox`,
feito em tempo de execução — só o render distingue (tentei o estático primeiro e
ele acusou as 79 peças de uma vez).

## ORDENAR DE TEXTO MOSTRAVA O NÚMERO, NÃO A CENA (Teatro das Palavras, ago/2026)

A peça `ordenar` nasceu para "do menor para o maior" (fichas `{v, img, nome}`:
figura + número). No Teatro das Palavras ela foi usada para **ordenar CENAS de
uma história** — fichas `{v, nome}` **sem figura** ("Tico recebeu o convite.",
"Ensaiou a fala.", "Subiu ao palco."). Aí o `corpoFicha` caía no ramo sem
figura e escrevia **só o valor** (`oval` = "1/2/3"), ignorando o `nome`. A
criança via três numerinhos e ordenava 1-2-3 **sem LER as cenas** — justo o
oposto do que o balão pede ("Coloque as cenas na ordem em que aconteceram").

Por que a banca não pegou: o `jogador.js` só precisa CHEGAR na medalha, e três
números são ordenáveis; ele fez a fase e passou. Defeito de CONTEÚDO/exibição,
não de código — o tipo que só o olho do Marcos (ou um print) pega.

**Conserto:** no ramo sem figura, `corpoFicha` mostra o `nome` (a cena) quando
há um, e só cai no valor cru quando não há nem figura nem nome (ordenar numérico
puro). A ficha ganha a classe `.txt` (mais larga, fonte legível para o 5º ano) e
o `.onom.otexto` quebra linha (o `.onom` base tinha `white-space:nowrap` +
ellipsis, que cortava "Tico recebeu o con...").

**Lição geral:** peça reaproveitada num uso novo (número → cena de texto) traz
suposições velhas embutidas. Ao usar uma mecânica fora do seu caso de origem,
RENDERIZAR e OLHAR a tela — a banca confirma que joga, não que a criança
aprende.

**Coice do conserto — FILEIRA TORTA (o portão 5b pegou):** com as cenas virando
texto, frases de tamanhos diferentes quebravam em 1 ou 2 linhas e as fichas
ficavam com alturas diferentes (75..93px) — o `_qa/visual.js` reprovou "fileira
TORTA". Primeiro tentei `min-height` no `.pc.txt`, e NÃO funcionou: o motor tem
`.centro .pecabox .pc:has(> .zap){min-height:70px}` (especificidade 0,4,0) que
vence o `.mec-ordenar .pc.txt` (0,3,0) — e o `.mec-ordenar` mora num ANCESTRAL
acima do `.pecabox`, então subir a especificidade fica frágil. **A cura que
funciona não briga com o motor:** o TEXTO (`.onom.otexto`) reserva SEMPRE 2
linhas (`min-height:2.56em`) e centraliza — frase de 1 ou de 2 linhas ocupa a
mesma altura, a fileira fica reta caiba o que couber no `min-height` do motor.
**Lição:** quando o motor já força um tamanho via `:has()` (0,4,0), não dispute
especificidade — faça o CONTEÚDO ter altura uniforme, que é o que o portão mede.

## BALÃO DA PEÇA COM NÚMERO POR CONCATENAÇÃO FICA MUDO (Lojinha, ago/2026)

O balão do SETE-ERROS era `el("div","balao","As duas cenas têm <b>"+DIFS.length+"
diferenças</b>. Toque em cada uma...")`. O `balaoes_das_pecas` do montador só grava
voz de balão que é frase LITERAL e COMPLETA (`"balao","...frase inteira."`);
com o número no meio a string quebra em pedaços, o regex pega só `"As duas cenas
têm <b>"` — sem ponto final e curto — e descarta. Resultado: a fase apareceu na
tela com o balão que a criança VÊ e **sem voz nenhuma**. Quem pegou foi o portão
**0f2** (`colher.py --so-ver`, que joga e lista o que aparece sem gravação) — o
`node --check` e o print não veem, porque só falta o áudio.

**Conserto:** o balão virou frase fixa ("Ache as diferenças entre as duas cenas.
Toque em cada uma que você achar.") e o NÚMERO ficou só no contador dinâmico
("Faltam N diferenças") logo abaixo. Frase fixa → o montador grava.

**Regra p/ toda peça nova:** o balão (enunciado que a criança ouve) é SEMPRE
frase literal completa terminando em `.!?`; contagem/variável dinâmica vai num
elemento SEPARADO (contador/placar), nunca concatenada dentro do balão — senão
a fase nasce muda e só o 0f2 percebe.

## GAVETA SÓ-FIGURA VIRA CAIXA VAZIA EM ATIVIDADE DE TEXTO (Teatro das Palavras, 5º ano, ago/2026)

A `classificar` foi customizada na Lojinha para a gaveta NÃO ter texto (1º ano não
lê; a identidade é a figura do dinheiro + alto-falante). No Teatro das Palavras
(5º ano) a mesma peça separa **pronome pessoal × demonstrativo** — gavetas de
TEXTO, sem figura (`img:""`). Resultado: duas caixas escuras VAZIAS, a criança
sem saber qual é qual.

**Conserto:** `fazGaveta` agora tem `else` — quando não há `img`, mostra o NOME
escrito (`.gnome`, branco e forte sobre a gaveta escura). Gaveta COM figura
(Lojinha) não muda. **Lição:** customização feita para uma faixa etária (só
figura) não pode APAGAR a via de texto que outra faixa precisa; o certo é
condicional (figura quando há, texto quando não há), nunca remoção.

## PEÇA CUSTOMIZADA P/ FUNDO ESCURO SOME NO TEMA CLARO (Lojinha, ago/2026)

Varrendo TODAS as peças com `peca.sh` (P2), só 3 reprovaram — e eram as 3 que eu
tinha customizado para a Lojinha (fundo escuro de loja): `caixa-dinheiro`,
`classificar`, `comparar`. Passavam na banca da Lojinha (o `contraste.js` mede o
pixel sobre o fundo ESCURO real e dava ok), mas quebravam no `peca.sh`, que roda
o `_qa/tema_claro.js` — a peça sobre um tema CLARO simulado.

O que cada uma tinha:
- **comparar** `.grupo` (exibição, não-tocável): texto branco `#f4efe6` sobre
  vidro BRANCO `rgba(255,255,255,.10)`. Sobre a loja escura o branco passava; num
  tema claro o `.rotulo` caía para 3,3:1. Conserto: o grupo de exibição não pinta
  mesa própria → texto SEGUE o tema (`color:var(--texto)`, fundo transparente).
  O `.grupo.opt` (botão) carrega mesa ESCURA própria, agora forte o bastante
  (degrau de cima era `.44` de opacidade → dava 159 de luz sobre papel; subido
  para `.80/.86`) para o branco passar 4,5:1 em qualquer tema.
- **classificar** `.gnome` (rótulo de texto da gaveta): branco que apostava na
  "gaveta escura" — mas a gaveta é um vidro CLARO (rgba branca). Conserto: o
  rótulo carrega uma pílula ESCURA própria (`rgba(18,22,12,.80)`).
- **caixa-dinheiro** `.moeda.mfoto .mval`: cor escura `#22300f` numa regra que era
  `display:none` (carteira limpa). Cor de isca para o `cor_fixa`. Removida.

Além disso o `cor_fixa` só perdoa cor escura quando um ancestral NOMEADO no
seletor pinta fundo: `.bandeja .pctxt` (texto escuro no vidro claro do `.pc`)
precisou virar `.bandeja .pc .pctxt`.

**Lição geral (custa uma varredura inteira se esquecida):** ao customizar uma
peça para o fundo de UMA atividade (escuro), a peça continua tendo que sobreviver
em QUALQUER atividade. Regra da casa: texto ou **segue o tema** (`var(--texto)`,
fundo transparente) ou **carrega mesa própria** com opacidade alta o bastante
(≈.78+ com tinta escura) para passar 4,5:1 mesmo sobre papel claro. Nunca apostar
no fundo da atividade. Rodar `peca.sh` (que inclui o `tema_claro.js`) na peça
customizada ANTES de fechar — a banca da atividade sozinha não pega, porque mede
só o fundo escuro dela.

## PORTÃO tema_claro DESCOBRIA "TELA" POR NOME E ESTOURAVA EM HELPER (ago/2026)

Varrendo as 80 peças com o `_qa/tema_claro.js`, TRÊS reprovaram — domino,
morfemas, passo-a-passo — todas com a mensagem contraditória **"0 texto sumindo"
+ "PECA NOVA COM TEXTO QUE SOME"**. Não era a peça: era o PORTÃO.

O `tema_claro.js` descobria as telas por NOME (`^function (tela|peca)…`). No
domino isso pegava o helper `pecaEl(p)` — que MONTA uma peça do dominó e **exige
o argumento `p`**. O `contraste.js` o chamava sem args → `TypeError: Cannot read
properties of undefined (reading 'a')`. O portão capturava o estouro como
`falhou=true`, mas não havia linha `razao` nenhuma → imprimia "0 sumindo" e
reprovava assim mesmo. Pior: o nome também PERDIA tela real fora do padrão (o
`desenhaTela` do passo-a-passo).

**Conserto:** a descoberta passou a ser a MESMA do `peca.sh`/bancada — tela é a
função que chama `limpa()` (renderiza do zero), achada por casamento de chaves,
não por prefixo do nome. As três voltaram a `ok` (o contraste sempre passou nelas
com a tela certa), e a amostra que já passava continua passando.

**Lição geral:** heurística de "o que é uma tela" tem que ser ÚNICA em toda a
casa. Quando dois portões usam regras diferentes (`limpa()` x prefixo de nome),
um deles acusa o inocente — e portão que acusa inocente ensina a ignorar portão.
Reusar a heurística canônica, nunca reinventar uma pior.

## SINAIS >,<,= SÃO CEDO PARA O 1º ANO — COMPARAR POR PALAVRA (Lojinha, ago/2026)

O Marcos, olhando a fase de comparar dinheiro: *"essa fase está adequada ao 1º
ano, comparar por esses sinais?"*. Não estava. A peça `comparar` é de DOIS passos:
1) "qual vale mais?" (palavra) e 2) "escolha o SINAL" (>, <, =). Os símbolos
relacionais entram na BNCC só no 2º/3º ano (EF03MA); no 1º ano compara-se por
SIGNIFICADO — vale mais / vale menos / vale igual — com apoio visual.

**Conserto (aditivo, não quebra os outros anos):** a peça ganhou dois campos POR
RODADA — `semSinal:true` PULA o passo 2 (fica só a palavra) e `pergunta:"menos"`
inverte a pergunta ("qual vale menos?"). Rodada sem esses campos segue idêntica
(com sinal), então 2º/3º/9º ano não mudam. **Lição de motor:** campo novo de
gaveta tem que aparecer na RODADA DE EXEMPLO da peça, senão o validador do
`montar.py` acha que a peça não o lê e manda a fase sair vazia. **Lição
pedagógica:** casar a mecânica com o ANO — símbolo abstrato no 1º ano é prova
disfarçada; a comparação nasce concreta e falada.

## QUADRADO VERDE NO FIM DE FASE = A MEDALHA DE 190px NO AVISO (Teatro, ago/2026)
O Marcos jogando: uma fase fechava com um "quadrado grande desconfigurado" no
lugar do aviso fininho das outras. Causa: 7 peças (pintar, pintar-canvas, memória,
sete-erros, achar-na-cena, camadas-mapa, traçar-caminho) mandam no aviso de FIM DE
FASE `<div class="medal">★</div>`. No motor a `.medal` é a MEDALHA DE 190px do FIM
DA ATIVIDADE (imagem do mascote) — o motor inflava a estrelinha num quadradão verde
vazio. **Conserto (ponto único):** `motor.html` `mostraBanner` remove a medalha-DIV
do aviso de fase (a medalha real do fim é `<img>`, não casa com o regex, fica
intacta). O aviso de fase não leva medalha — o motor já comemora com confete.

## A BARRA PREMIUM (cometa) VALE PARA TODA ATIVIDADE, ATÉ AS DE TEXTO (Teatro, ago/2026)
Ordem do Marcos: *"essa barra premium da atividade do primeiro ano tem que estar em
todas as atividades daqui em diante"*. A `poeVitrine` (trilho+cometa+"X / N") usa só
`VITRINE.length` (o número de fases), NÃO as figuras. Mas o `montar.py` esvaziava a
VITRINE quando faltavam figuras de produto — e o 5º ano (palavras) ficava com a barra
simples enquanto o 1º ano (dinheiro) tinha a premium. **Conserto:** VITRINE sai
SEMPRE com uma vaga por fase; as miniaturas entram quando existem (≥3 distintas), mas
a barra premium não depende delas.

## `_qa/funcoes.py` NÃO ENTENDIA LITERAL DE REGEX (Teatro, ago/2026)
Ao pôr um `.replace(/regex/gi)` no motor, o `funcoes.py` reprovou o Teatro: os
enunciados ("Ache os adjetivos (todas as direções)") viravam "função que não existe".
O `limpa()` tirava string e comentário, mas não LITERAL DE REGEX — uma `"`/`'` dentro
do regex abria uma "string" que dessincronizava o resto do arquivo, e as palavras
seguidas de "(" vazavam como chamadas. **Conserto duplo:** (1) `limpa()` agora pula
o regex literal inteiro (detecta `/` em contexto de regex, respeita `\` e `[classe]`);
(2) no motor, o strip da medalha usa `new RegExp("...")` (string), não literal. Regra:
regex no motor/peça, prefira `new RegExp("...")` — o portão limpa string, não literal.

## "ISSO É TANGRAM?" — TODA FIGURA USA AS 7 PEÇAS (Tangram Vovó Marta, ago/2026)
O Marcos, olhando a tela: *"isso é tangram? é assim mesmo? nossa atividade está
correta?"*. Não estava. Tangram é UM jogo com 7 peças FIXAS (2 triângulos grandes,
1 médio, 2 pequenos, 1 quadrado, 1 paralelogramo) e TODA figura usa AS SETE. O
"Tangram da Vovó Marta" tinha figuras de 5 e 6 peças e — pior — figuras pedindo
**3 triângulos pequenos** ou **2/3 quadrados**, que NÃO EXISTEM (só há 2 pequenos
e 1 quadrado). Era "encaixe de formas", não tangram. **Portão novo:**
`_qa/tangram.py` — confere que cada figura usa exatamente {gra:2, med:1, peq:2,
quad:1, par:1} e área 8. **Conserto (em andamento):** refazer as figuras como
arranjos válidos das 7 peças. ⚠️ o portão pega a CONTAGEM; o ladrilhamento
(sem sobra/sobreposição) ainda se confere no olho/render. **Lição:** quando o
Marcos pede "o JOGO do X", conferir a REGRA do jogo, não só a aparência.

## Lição (ago/2026) — peça avulsa que fecha em LOOP engana o jogador-robô
`pintar.html` reprovou na varredura da bancada com **timeout 124**: o banner de
fim chamava `pecaPintar` (REINICIA a peça) e não tinha `div.medal`. O
jogador-robô pintava tudo → reiniciava → pintava tudo, sem nunca ver a medalha
terminal. **Padrão da casa para o fecho AVULSO de qualquer peça** (ver
`pintar-canvas.html`): o último banner mostra a `div.medal` e **não** reinicia.
Dentro da atividade montada o motor remove a `div.medal` do banner (não vira
quadradão) e segue para a próxima fase. Portão que pega: `_qa/jogador.js` (o que
joga até a medalha) — rodado por `_qa/peca.sh`.

## Lição (Museu, ago/2026): FALAS DE AUTO-AJUDA são DETERMINÍSTICAS — `falasExtra`
O portão `0f2` (colher `--so-ver`) joga a atividade e cobra voz para todo texto
que a criança vê. As frases de **auto-ajuda que a PEÇA monta ao jogar** (memória
"Vou abrir este par: X — Y" / "Abri uma para você: X. Ache o par dela.", caça
"Achou as N palavras!" / "Já achou n de N!", digitar "A letra que vem agora está
acesa.") o colher só pegava JOGANDO — e apenas as que o ACASO disparava naquela
rodada. Resultado: a banca reprovava uma frase DIFERENTE a cada vez (flakiness).
**Conserto:** o `conteudo.json` agora pode trazer `falasExtra` (lista de frases);
o `montar.py` gera `op_<chaveVoz>` para cada uma (mesma conta do runtime → o mp3
casa) e dedup com as colhidas. O `build_conteudo.py` enumera essas frases a partir
dos próprios dados (pares da memória, nº de palavras da caça). Assim TODAS entram
de uma vez, sempre — o colher deixa de ser a única rede para o que é previsível.
Regra: frase de auto-ajuda cujo texto dá para prever pelos dados → `falasExtra`,
não confiar no acaso do colher.

## Lição (Museu, ago/2026): o ENUNCIADO da fase = o texto que a PEÇA mostra/fala
Peças com balão próprio (quem-sou-eu "Descubra quem está falando…", intruso "Três
destes são X. Qual é o intruso?", memória "Ache a palavra e o desenho que combina")
IGNORAM o `enunciado` do conteúdo na hora de desenhar, mas a narração automática
sai do `enunciado`. Se os dois divergem, o portão `0g/0n` reprova ("a voz não diz
o que está escrito"). Regra: ao usar essas peças, escrever o `enunciado` IGUAL ao
texto que a peça exibe/fala (conferir a peça antes de montar).

## Lição (Museu, ago/2026): peça é desenhada para N gavetas — respeitar
A peça `classificar` foi feita para 2-3 gavetas. Forçar 5 encolhe a figura
(<44px, portão de encaixe) e estoura o `.bandeja` no celular de 320px (portão de
leiaute). Regra: classificar em muitos grupos → dividir em fases de ≤3 gavetas
(também baixa a carga cognitiva, Sweller). E marca d'água de gaveta (`.gwater`,
opacity .12) NÃO é ilustração — o portão de encaixe agora a ignora.

## Lição (Museu, ago/2026): PORTÃO LENTO = REPROVA FALSA (colhe espera o .st)
A banca dispara ~8 portões de navegador em paralelo (`larga`) e depois os lê
(`colhe`). O código de saída de cada um vive num arquivo `.st` que só existe
QUANDO o portão termina. Em atividade grande (36 fases), com a CPU disputada por
8 Chromium, o `voz_dupla.js` levava ~100s e ainda NÃO tinha terminado quando o
`colhe` foi ler — `.st` vazio, o default `1` entrava, e a banca **reprovava uma
atividade impecável** (todos os outros portões "ok", este sem NENHUMA saída no
relatório). Mesma família do "jogador lento reprova por lentidão do auditor".
Conserto: o `colhe` agora ESPERA o `.st` aparecer (até 240s) antes de julgar.
Sintoma para reconhecer: BANCA REPROVOU sem nenhum "PROBLEMA" impresso, e um
portão de `larga` faltando no relatório — é ele que não terminou.

## Lição (Museu, ago/2026): GAVETA DE CATEGORIA + EXEMPLAR e o portão "figura combina"
Classificar em GRUPOS mostra a gaveta "MAMÍFERO" com um EXEMPLAR (mv_cachorro) —
o cachorro representa a categoria, não é a legenda da palavra. O `_qa/figura_certa.py`
lia o par nome+img da gaveta e reprovava (palavra "MAMÍFERO" ≠ arquivo "cachorro"),
como se fosse o defeito "ovo escrito, mamão desenhado". Não é. Conserto: quando a
gaveta tem `rot:true` (mostra nome de categoria + figura fraca de exemplo), o portão
PULA o par nome→img. Regra: figura-legenda-da-palavra continua medida; figura-exemplo-
de-categoria fica de fora. Também: sinônimo com nome de arquivo diferente (cobra ↔
mv_jiboia) reprova o portão — usar o nome que casa com o arquivo (jiboia).

## Lição (Museu, ago/2026): ARTIGO da narração segue o NOME, não o grupo
A voz da vitrine dizia "A tucano" / "O jiboia" porque o artigo vinha do GRUPO
(aves=A, répteis=O). Errado: tucano é masculino, jiboia é feminina. Artigo é do
NOME: termina em -a/-ã → feminino (a arara, a jiboia, a rã); senão masculino
(o tucano, o jacaré). Marcos exige voz perfeita — gramática entra no acabamento.

## Lição (Museu, ago/2026): a banca largava 12 navegadores de uma vez → estourava
Num container apertado, abrir contraste+leiaute+imagens+jogador + 8 portões de
`larga` AO MESMO TEMPO estoura a memória: uns Chromium caem no meio (reprova
falsa) e às vezes a banca morre no arranque sem imprimir nada. Conserto: SEMÁFORO
`QA_MAX_PAR` (default 3) — os navegadores entram em fila. A banca fica um pouco
mais lenta mas TERMINA sempre, e menos briga por CPU deixa cada portão mais rápido.
Sintoma que era isto: banca reprova/morre sem nenhum "PROBLEMA" impresso e com
portões faltando no relatório (os que não couberam na largada).

## Lição (Museu, ago/2026): o REVISOR (testador humano de TEXTO) + voz stale
Criado `_qa/revisor.py` (portão 0o): o olho de TEXTO do "testador humano" que o
Marcos pediu — pega concordância artigo↔nome ("o jibóia"/"a tucano"), palavra
repetida, espaço duplo, HTML vazando na fala. Já pegou defeito real que a banca
inteira deixou passar. Erro de gênero por engano vira exceção nas listas do
próprio revisor (MASC_A/FEM_O), nunca afrouxar a regra.
E consertou um defeito do montar: quando o TEXTO de uma voz muda (o artigo),
a versão VELHA ficava presa como "colhida" (id diferente) e entupia o falas.json
— o montar agora normaliza (tira artigo/caixa) e descarta a stale.

## Otimização da banca (Museu, ago/2026): confiável primeiro, depois rápida
- SEMÁFORO QA_MAX_PAR (3): a banca parou de estourar o container (12 navegadores
  de uma vez) → passou a FECHAR sempre em código 0.
- Arranque: o `mktemp` do modo-cópia falhava no /tmp instável → rodar com
  `QA_COPIA=1` pula a cópia e não trava no arranque.
- JOGADOR PARALELO por padrão (joga_par, 3 trechos) rodando POR ÚLTIMO, sozinho
  (depois dos outros navegadores) → rápido (~110s x ~5min) sem briga por CPU.

## Lição (varredura das 81 peças, ago/2026): peça que só passou DENTRO de uma atividade
Rodei `_qa/peca.sh` SOLO nas 81 peças do catálogo. 80 já saíam código 0; a
`vitrine` REPROVAVA sozinha e ninguém tinha visto porque ela só fora medida
DENTRO do Museu (que é de tema escuro). Três defeitos que o contexto da
atividade mascarava:
- **tema_claro (5c):** card de VIDRO CLARO (`rgba(255,255,255,.15)`) com letra
  branca. Sobre a cena escura do museu ficava lindo; numa atividade de tema
  CLARO o card virava quase-branco e as 18 legendas SUMIAM. Conserto: a peça não
  escolhe a atividade — quem quer letra branca carrega a MESA ESCURA dela
  (`rgba(22,30,18,.72)`, vidro escuro que lê a foto por dentro). Vale nos dois temas.
- **cor_fixa (4b):** `.vnome`/`.vinfo` com `color:#fff` e sem fundo próprio na
  regra. O fundo existe (`.vitcard`), mas o portão só perdoa se o SELETOR mostrar
  o ancestral: qualifiquei `.vitcard .vnome` / `.vitcard .vinfo`.
- **funcoes (2):** `tocaVoz(chaveVoz(...))` chamados nus reprovam solo (o motor
  os declara, a peça solo não). Guardados por `if(window.tocaVoz&&window.chaveVoz)`
  e escritos `window.tocaVoz(window.chaveVoz(...))` — o portão pula chamada com `.` antes.
- **leiaute (7):** a grade de cards empurrava o botão de avançar para baixo da
  dobra; SOLO a `.tela` precisa rolar sozinha (`max-height:96vh;overflow-y:auto`),
  porque a rolagem do body não conta e o motor não está ali para rolar por ela.
REGRA que fica: **peça nova se prova SOZINHA no `_qa/peca.sh`, nunca só dentro da
atividade** — a atividade tem tema/motor que escondem o defeito que a próxima
atividade vai revelar.

## Verificação do MOTOR (ago/2026): o que dá para provar num container apertado
Montei uma atividade de 36 fases pelo ESQUELETO (`montar.py` → index.html de 7085
linhas, autossuficiente) e rodei a banca. **O motor está PROVADO** no que este
container consegue medir:
- `montar.py` gera index.html + falas.json + arte.json a partir do conteudo.json ✓
- PEDAGOGO (escada), PADRÃO DA CASA (didática/ilustrada/sonora/variada),
  DINÂMICAS, PERGUNTA AMBÍGUA, VOZ DA TELA, TELA VAZIA, VOZ DA PERGUNTA ✓
- imagens.js (45 figuras em 36 telas) ✓  ·  contraste.js (581 textos, 37 telas) ✓
**Limite do container, NÃO do motor:** os portões que PERCORREM a atividade no
Chromium (jogador.js — "joga sozinho até a medalha" — e a colheita `colher.py`,
que é 0f2) **travam/matam o processo neste container**, enquanto os portões que só
FOTOGRAFAM cada tela (imagens/contraste) passam. A causa raiz foi a colheita
disparando **3 percursos de jogador ao mesmo tempo** → estouro → chrome zumbi →
container degradado (depois disso nem um jogador sozinho roda). Consertei a raiz
(`colher.py` agora respeita `QA_MAX_PAR`), mas o container **já degradado** não
confirma o conserto: isso só se prova numa **sessão nova** com `QA_MAX_PAR=1`.
REGRA: o "código 0" da banca inteira de uma atividade montada de ~36 fases precisa
de runner folgado (sessão nova) ou `QA_MAX_PAR=1`. Nunca afirmar código 0 sem o
jogador ter percorrido — e o Museu (mesmo conteúdo) já saiu código 0 em sessão
anterior, então o motor não é o suspeito; o percurso pesado é.

## Lição (Museu, ago/2026): gênero por terminação erra "peixe"; e voz stale de artigo
- **"o dourado é UMA peixe"**: o gerador escolhia o artigo do grupo por letra final
  ("termina em E → uma"), que acerta AVE mas erra PEIXE (masculino). Gênero não se
  adivinha pela letra: usar dicionário EXPLÍCITO. O Revisor ganhou o item 6b
  (`GEN_FIXO`) que casa artigo definido E indefinido contra esse dicionário —
  agora pega "uma peixe" e "um ave".
- **classify com todas as fichas no mesmo `alvo`**: bug de tupla (casava `(nm,im)`
  de 2 contra INV de 3) fazia todo bicho virar "vert" e o invertebrado não entrar
  na gaveta certa. O jogador-auditor não pega. Portão novo no montar: 2+ gavetas
  exigem 2+ alvos e todo alvo tem que existir.
- **voz STALE de artigo**: quando o texto muda de "uma peixe" para "um peixe", a
  entrada VELHA (id = chaveVoz do texto antigo) ficava presa no falas.json como
  colhida. O runtime toca a voz do texto ATUAL (a criança ouve certo), mas o
  Revisor acusa a entrada morta. Cura: `rm <pasta>/falas.json && montar.py` para
  regravar limpo quando o TEXTO de uma voz mudar.

## ⚠️ LIÇÃO PAGA — O SIMULADOR DO MOTOR É A CHUVA, NÃO UM MOLDE VAZIO (ago/2026, Cidade dos Sólidos 2º ano)
A peça `simulador` do ESQUELETO **não é genérica**: ela é, inteira, a CHUVA/RIO/
PONTE da atividade de história onde nasceu — balão "Mexa a chuva. Em que número a
água encosta na ponte?", a água que sobe, o barco, os botões `3/4/5/7`, e os
globais `MAXC/NIVEL_PONTE/BASE/PASSO` **fixos**. Ela **ignora o conteúdo da fase**:
por mais que o `conteudo.json` diga `enunciado="Solte os sólidos na rampa"`, a
criança vê o jogo da chuva. Montei DUAS fases de sólidos com `mec="simulador"` e o
**print ficou lindo** — o defeito só existe JOGANDO. Foi resto de clone puro: a
cena de OUTRA atividade dentro desta.
- **Como a banca pegou:** portão 0f2 (voz medida jogando) achou os números `3/4/5/7`
  mudos no VOZOK e o balão "Mexa a chuva" sem voz — sintomas, não a causa. A causa
  só apareceu lendo `pecaSimulador()`.
- **O conserto do dia:** trocar as duas fases por `ligar` e `quem-sou-eu` temáticos
  de "rola × fica firme" (o motor as renderiza de verdade). O simulador-de-rampa
  fica como EVOLUÇÃO futura do motor (uma peça `simulador` tematizável), não como
  clone mal-usado.
- **O portão que fica (`_qa/dinamicas.py`):** lê o `FASES` do index e **reprova toda
  fase `mec="simulador"` cujo selo+enunciado não fale de água** (chuva|rio|ponte|
  água|barco|enchente|nível|maré/onda|represa). Enquanto o motor não tiver um
  simulador que leia o conteúdo, `mec="simulador"` só vale em tema de água.
- **A regra geral:** peça de motor que **hardcoda o tema** (texto, cena, globais) só
  serve no tema dela. Antes de reusar uma peça numa atividade nova, conferir se ela
  LÊ o `conteudo` ou se traz a cena da origem colada. Print bonito não prova nada —
  o simulador provou isso outra vez.

## ⚠️ LIÇÃO PAGA — VOZ POR TOQUE: REUSE A FORMA JÁ GRAVADA (ago/2026, Cidade dos Sólidos)
Duas peças ganharam **modo imagem** nesta sessão (o Marcos pediu "nome ↔ imagem"):
- **`memoria`**: par NOME × IMAGEM. A carta-palavra usa `pal` (sem `img`); a
  carta-figura usa `imgsen` (a arte de IA) e `sen` vazio. A peça já esconde a
  caixa de figura quando a carta é só-palavra (guarda `temFig` no `fazCarta`).
- **`arrastar-sombra`** e **`ligar`**: aceitam `img` numa ponta (a peça monta
  `<img>` via `window.imgEl`); a silhueta da sombra é a PRÓPRIA figura em
  `brightness(0)`. Sem `img`/`imgEl` caem no clip-path/texto (peça solta e
  atividades antigas seguem iguais).

**A ARMADILHA que custou 3 rodadas de banca — `_norm_voz` colapsa o artigo.**
Quando uma peça fala uma resposta por TOQUE (o alto-falante da ponta, via
`data-voz`/`voz`), o `montar.py` **descarta** essa voz se o texto normalizado já
existir no falas.json — e `_norm_voz("o cubo")` vira `"cubo"`, colidindo com a
palavra "CUBO" que a memória já grava. Resultado: `audio/op_<x>.mp3` nunca é
gerado e o toque fica MUDO (portão 0j: "mp3 nao carrega").
→ **Regra:** para a voz de uma resposta tocável, **reuse a forma EXATA que já
está gravada** (ex.: `voz:"CUBO"`, `voz:"BOLA"` — as palavras que a vitrine/
memória/escolher já gravaram), em vez de inventar "o cubo"/"a bola". O
`montar.py` NÃO extrai o campo `voz`/`img.voz` como fala nova; ele só preserva o
que veio do texto do conteúdo ou da COLHEITA. Inventar voz nova por toque =
gravar à mão (que o montar apaga) ou colher (que não toca o alto-falante). Reusar
é de graça e não colide.

## ⚠️ LIÇÃO PAGA — ALTO-FALANTE DENTRO DO BALÃO: O MOTOR JÁ FAZ (não reinvente)
O Marcos pediu "botão de som no enunciado". Tentei injetar um `.zap` DENTRO do
`.balao` (appendChild, inline no início, absoluto num vão) — e o `_qa/leiaute.js`
reprovou em TODA peça: ele trata a região do balão como TEXTO e acusa "botão sobre
o texto" em qualquer posição interna. **O motor já resolve isso** com
`poeVozPergunta()` (classe `.zapb` + `paddingRight:56px` inline reservado), que põe
o alto-falante em todo balão SEM tapar a última palavra, e NÃO põe um segundo se a
peça já tem o `.zap` dela. → **Não injetar zap no balão à mão.** Para narrar a
INSTRUÇÃO abaixo do enunciado (a `.hint`), o caminho é `vozesDaTela()` +
`_tocaSeq` no "Ouvir de novo" (lê balão + hint encadeados, nunca as duas juntas) —
já no motor.

## ⚠️ LIÇÃO PAGA — O MONTADOR LIA "esquerda:" DE UM COMENTÁRIO (ago/2026, prova das 81)
Fiz a **prova de montagem das 81 gavetas** (`provar_gavetas.py`) — 1 fase por peça,
só o `montar.py`, sem navegador. Descobriu que **39 das 81 nunca tinham sido
MONTADAS** (o `peca.sh` prova a peça isolada; a `provar_esteira.sh` só monta 16).
E achou um defeito real: o **`simetria` era IMPOSSÍVEL de montar**.
- **Causa:** `campos_no_texto` (o detector de "campos que a peça percorre") lia o
  exemplo do `pecas.json` **com comentário**. O `simetria` tem
  `/* metade da esquerda: [linha, coluna] */`, e `esquerda:` seguido de `[` era
  lido como **campo estrutural obrigatório**. O montador exigia `esquerda` — que a
  peça NUNCA lê (ela lê `modelo`). É a mesma lição dos portões: **quem lê prosa
  mede prosa**.
- **Conserto:** `campos_no_texto` tira `/* */` e `//` ANTES de varrer. Só pode
  remover falso-positivo (campo real nunca mora dentro de comentário), então é
  seguro.
- **O teste que fica:** `python3 _padrao/ESQUELETO/provar_gavetas.py` — roda em ~5s
  e reprova se QUALQUER peça deixar de montar. Rodar ao mexer em `montar.py`,
  `esboco.py`, `pecas.json` ou numa gaveta.

## ⚠️ LIÇÃO PAGA — PEÇA QUE FECHA NA MÃO É UM BECO NA ESTEIRA (ago/2026, prova por lote)
A **prova de banca por lote** (esboço + montar + `auditar.sh` num punhado de peças
pouco usadas) pegou a `reta-numerica` **travando o jogador com erro de JS** dentro
da atividade montada — sozinha, no `peca.sh`, ela passava lisa.
- **Causa:** o fim das rodadas ia DIRETO para uma função própria da peça
  (`fimReta()`), que monta a tela do medidor e um botão "Jogar de novo". A ponte
  da esteira (`integrar.py`) **só avança de fase pelo `mostraBanner`** (é ele que
  a ponte reaponta para o `_seguir`/`fim()` do motor). Fechando por fora do banner,
  a criança terminava as retas e ficava PRESA no medidor — e o auditor-jogador, que
  só reconhece o fim quando a `.medal` aparece logo depois de um toque dele,
  esbarrava numa tela sem `data-qa` e o app estourava. É o mesmo parentesco das 30
  peças que chamavam `fimDaPeca()` direto.
- **Conserto:** o fim passa PELO `mostraBanner(<parecer curto>, fimReta)`, igual à
  `estimar`. Na peça avulsa o banner chama o callback e mostra o medidor; na
  montada a ponte ignora o callback e leva para a fase seguinte. **Regra da casa:
  toda peça fecha por `mostraBanner(...)` — nunca por uma tela de fim própria
  chamada na mão.** Tela de "peça fechada" só como CALLBACK do banner.
- **O teste que fica:** a **prova de banca por lote** (`_padrao/ESQUELETO/PECAS-A-FECHAR.md`)
  — 1 fase por peça num lote grande + `auditar.sh`. O `peca.sh` NÃO pega isto
  (prova a peça isolada, onde o beco é um fim legítimo). Ao mexer numa peça que
  termina em tela própria, montar num lote e ver o jogador ATRAVESSAR a fase.

## ⚠️ LIÇÃO PAGA — O ESBOÇO NÃO PODE «PLACEHOLDAR» CONFIG (ago/2026, prova por lote)
A **prova de banca por lote** pegou a `bussola` prendendo o jogador em **0%** com
**0 alvos data-qa** e **sem erro de JS** — o pior tipo: monta bonito, o print
parece certo, e a criança não consegue dar o primeiro passo.
- **Causa:** o `esboco.py` marcava com «...» TODAS as gavetas fora a principal —
  inclusive as de CONFIG. Na bussola isso garblava `DIRS` para `["«NORTE»",...]`
  (o botão nascia com `rumo="«NORTE»"` e nunca casava com o alvo `"NORTE"`, que
  vem do `dirDe`) e `RODADAS[0].tipo` para `"«achalugar»"` (mandava a rodada para
  o galho `achadir`, errado). Config com default legítimo (direções cardeais,
  setas, tipos de rodada) **não é conteúdo editável** — virar placeholder a quebra.
- **Conserto (duas partes, como sempre):**
  1. `esboco.py` **pula as vars marcadas `/*TECNICA*/`** ao emitir `dadosExtra` —
     técnica fica no default; o autor só liga se quiser, com valor REAL.
  2. a peça **marca a config como `/*TECNICA*/`** (na bussola: `DIRS` já era;
     marquei `REF`, `SETA`, `RODADAS`). Sobra como conteúdo só o que o autor troca
     de verdade (na bussola, `LUGARES` = os lugares do mapa).
- **Verificado:** o jogador ATRAVESSA a bussola (0→25→50→75→100→BANNER). As 81
  continuam montando (`provar_gavetas`).
- **⚠️ ARMADILHA ao estender:** marcar TODAS as gavetas-array como técnica faz o
  `integrar` perder a gaveta principal e cair numa `var` interna (na calendario o
  `var` virou `cels`). Deixe UMA gaveta de conteúdo de fora (a que o autor troca).
  A `calendario` cai na MESMA família (o `FASES.t="achar"` garbla) mas precisa
  desse cuidado com o var-pick — está na fila em PECAS-A-FECHAR.

## Lição (ago/2026): NÃO confiar em `--virtual-time-budget` para opacity/animação
Ao consertar o "transparente" do Ateliê de Cores eu quase mexi no motor por um
diagnóstico ERRADO. As capturas com Chromium `--headless --virtual-time-budget`
mostravam a `.tela` em **opacity:0** (invisível), e eu li isso como um bug de
`prefers-reduced-motion` no motor. Não é: o `--virtual-time-budget` **congela as
animações CSS no quadro inicial** — a `.tela` entra com fade (opacity 0→1) e a
captura pega o t=0. Num navegador real (e no Playwright, que usa a timeline real)
a animação completa e a tela aparece: medido, `.tela` fica opacity 1.
- **Para medir VISIBILIDADE/opacity/fade:** usar Playwright (timeline real) OU
  renderizar SEM `--virtual-time-budget` e esperar mais que a duração da animação.
  Nunca concluir "tela invisível" de uma captura com virtual-time.
- O "transparente" que o Marcos via era (a) essa captura enganosa que EU mostrava
  e (b) o canvas de pintar real aparecendo SOBRE o fundo. O conserto de verdade
  foi no `tema.css` da atividade: quadrado **branco sólido** (`.pintawrap{background:#fff}`),
  cartão opaco e o fundo do cenário **borrado** atrás — não mexer no motor.

---

## 🔊 VOZ DUPLA: o carimbo do `.play()` (Feirinha, ago/2026)
Defeito pego pelo portão `_qa/voz_dupla.js` (só na banca MONTADA): na fase de
`escolher`, quando a criança tocava o 🔊 da pergunta e respondia no MESMO instante,
o som de acerto (`falar`, no `narr`) partia por cima da voz da opção (`tocaVoz`, no
`vz`) — duas `.play()` em <700ms. A causa: logo após `.play()` o `currentTime`
ainda é 0, então `_vozTocando()` NÃO via a voz recém-iniciada e deixava a 2ª
partir. Isso NÃO se pega isolado (peca.sh); só jogando montado.
**Conserto (motor):** um carimbo `_lastPlayT` gravado a cada `.play()` (narr e vz);
`_vozTocando()` conta como "tocando" por 500ms após qualquer play → a 2ª fala entra
na FILA em vez de sobrepor. E `falar` passou a calar o `vz` também (simétrico ao
`tocaVoz`, que já cala o `narr`). **Peça `escolher`:** o respiro pós-acerto subiu
de 560→900ms (a narração da PRÓXIMA rodada não parte no encalço do som de acerto).
Lição: fala nova disparada no MESMO tick de outra é uma corrida — o guardião de
voz tem que cobrir a janela do play(), não só o `currentTime>0`.

## 🎨 CONTRASTE sobre MADEIRA: creme não basta, escurecer o fundo (Feirinha, ago/2026)
Portão `_qa/contraste_fundo.py` reprovou rótulos das peças de matemática:
`.cxrot/.mrot/.numr` usam `var(--texto,#f4efe6)` (creme, previsto pela peça), mas
o motor sobrescreve `--texto` para ESCURO → texto escuro no caixote marrom (razão
~1.6). E os botões de peça (amarelo #ffd54a) ficavam com texto BRANCO do motor
(razão 1.4). E a prateleira do `base-dez` (marrom-claro 188,107,66) não fecha 4.5
NEM com creme NEM com escuro. **Conserto (por atividade, `<pasta>/tema.css`, que é
injetado por último e vence a cascata):** rótulos de madeira → creme forçado;
botões de peça de matemática → verde+branco (uniforme, como a casa); prateleira →
FUNDO escurecido (`#3a2410`) para o creme passar folgado. Lição: em fundo
marrom-médio, nenhuma cor de texto fecha o WCAG — muda o FUNDO, não só a letra.

## 📏 SUPERFÍCIE INTERATIVA QUE COLAPSA: a régua sumiu (reta-numerica, ago/2026)
O Marcos pegou: *"não vi a régua como funcional"*. A peça `reta-numerica` tem
TODOS os filhos da `.reta` em `position:absolute` (trilho, tracinhos, números,
`.rint`) → o `<div>` não tem largura própria nenhuma. Na peça avulsa ela enchia
porque o pai era bloco comum; DENTRO do motor a coluna é `flex; align-items:center`,
que **não estica** um item de conteúdo zero → a régua colapsava para ~4px, uma
tirinha invisível no alto. Pior: **o jogador-robô passava** (ele "crava" pelo
`data-alvo`, sem coordenada), e nenhum portão media a largura da régua → defeito
que só existia na mão da criança, invisível para a banca.
**Conserto (as duas partes da casa):** (1) código — `.reta{width:100%}` na peça
(recompilar com `integrar.py --escrever`) enche a coluna em qualquer pai; e, por
atividade, `tema.css` escurece o painel (tábua de madeira) para o trilho/números
creme lerem sobre a foto. (2) portão — `.reta` entrou na lista `RESPOSTA` do
`_qa/leiaute.js`: superfície interativa que encolhe abaixo de 40px passa a
reprovar sozinha. Lição: alvo cujos filhos são TODOS absolutos não tem largura
intrínseca — precisa de `width` explícito, e o portão de leiaute tem que MEDIR a
superfície, não confiar no robô que clica por `data-alvo`.

## 🧬 GAVETA QUE NÃO ABRE: a peça rodava com o EXEMPLO dela (Sólidos, ago/2026)
O Marcos: *"a fase 'qual não é' não tem nada a ver com sólidos"*. A peça INTRUSO
mostrava frutas (banana/uva/maçã/cenoura) dentro de uma atividade de sólidos.
**Causa raiz no `integrar.py`:** a detecção de gaveta era `^var\s+X\s*=\s*[\[{]`.
Oito peças declaram a gaveta como `var RODADAS= /*TECNICA*/[...]` — com o
comentário TECNICA ENTRE o `=` e o `[`. A regex parava no `=` e não via o `[`
depois do comentário → a gaveta não era detectada, `f.dados` não entrava, e a
peça caía no EXEMPLO próprio. Não dá erro de JS, o print fica bonito, o jogador-robô
passa — só a criança vê o conteúdo errado. Afetava: bussola, calendario,
camadas-mapa, criar-desafio, intruso, mapa-conceitual, passo-a-passo, teia-alimentar.
**Conserto:** a regex pula um comentário opcional antes do vetor/objeto
(`=\s*(?:/\*[^*]*\*/\s*)?[\[{]`). Lição: exemplo de peça que "vaza" para a
atividade é resto-de-clone MUDO; o detector de gaveta tem que enxergar a var mesmo
com a marca TECNICA colada nela.

## 🌐 SW REGISTRADO E INEXISTENTE: "página sem conexão" (Lojinha, ago/2026)
O motor sempre faz `navigator.serviceWorker.register("sw.js")`, mas o montador
NUNCA escrevia o sw.js → 404. Com a internet instável da escola, a navegação caía
na "página sem conexão" em ALGUNS PCs (intermitente = depende da rede de cada
máquina). Conserto: o montador GERA um sw.js rede-primeiro (online = fresco;
rede caindo = volta ao index.html do cache), cache-primeiro em imagem/áudio,
skipWaiting+clients.claim, com hash no nome do cache. Lição: se o motor registra
um SW, o montador tem que ENTREGAR o arquivo — e SW de HTML tem que ser
rede-primeiro com fallback pro shell, nunca deixar a navegação morrer.

## 🎬 BANNER QUE DESLIZA PRA FORA: botão Próximo some (Lojinha, ago/2026)
O banner de fim de fase se escondia com `transform:translateY(115%)` e só voltava
ao fim da transição. Em PC antigo (fixed+transform) a transição às vezes não
fechava e o botão Próximo ficava abaixo da dobra → "trava/não avança" em alguns
dos 30 PCs. Conserto: esconder por opacity+visibility e deslizar só 16px (no pior
caso 16px mais baixo, sempre inteiro na tela). Lição: reveal de elemento fixed
não pode depender de um transform grande terminar — opacity é à prova de strand.

## 🧾 RELATÓRIO COM RESTO DE CLONE: BNCC de plantas em toda atividade (ago/2026)
O `segredoRelatorio` do motor trazia PLANTAS fixo (EF02CI05/06, "água e luz",
"partes da planta", "sol+água") — clone do Jardim no parecer de TODA atividade.
Conserto: o montador injeta `RELBNCC` a partir da mesa/currículo da própria
atividade; o motor usa isso; "antes×depois" e "como ler" viram genéricos. Lição:
texto de disciplina no MOTOR é clone garantido — tem que vir do `dados`.

## 🔊 PISTA MUDA: "quem sou eu" sem áudio na pista (Sólidos, ago/2026)
A pista chegava escrita e muda. A voz de cada pista JÁ existia (op_<hash>, o
montador grava tudo do `dados`); faltava só o alto-falante. Bastou pôr `.ptxt`
(o texto da pista) no `ZAPSEL` do motor — o observador põe o botão sozinho em
todo elemento cujo texto tenha voz. Lição: antes de "gerar voz", conferir se ela
já existe e só falta o elemento entrar no ZAPSEL.

## 🔘 BOTÃO PRÓXIMO QUE "NÃO FAZ NADA" (motor, ago/2026)
O Marcos: "às vezes aparece o Próximo, clico e não faz nada". O onclick do banner
era `arma();banner.className="banner";cb();` SEM guarda: se `cb` fosse indefinido,
ou `cb()`/`arma()` estourasse (fase seguinte com problema, AudioContext num PC),
o clique morria no meio e a fase não andava — intermitente, só em algumas
máquinas/fases. Conserto: cada passo em try/catch e o AVANÇO (cb) roda de todo
jeito. Lição: o clique que faz a fase andar é sagrado — nunca deixar um passo
anterior (som, animação) poder abortá-lo.

## 🪟 PADRÃO DA CASA: opções em vidros na horizontal + figura limpa no vidro (ago/2026)
Decisão do Marcos: "torne isso padrão, fica mais bonito" + "opções na horizontal
torne padrão". Promovido das peças (escolher, quem-sou-eu, digitar) para o
motor/peças, valendo para toda atividade: (1) opções na HORIZONTAL, em vidros
SEPARADOS, cada uma no seu `.opt`; (2) tamanho enxuto (flex 1 1 96px) para as 4
caberem numa LINHA quando a tela permite, quebrando só nas estreitas; (3) a FIGURA
fica LIMPA (sem fundo branco/borda/sombra) dentro do vidro, com o brilho que já
existia (`.opfig:before`); (4) o `.dgfig` do digitar vira o mesmo vidro com brilho.
Atividade pode sobrescrever no seu `tema.css` (a Cidade dos Sólidos tem o dela).

## Lote de reparos ao vivo — sólidos (ago/2026, Marcos)

**RELATÓRIO mostrava conceitos de PLANTA (clone do Jardim).** O `telaPainel`
iterava `var CONC={luz_agua...partes da planta...}` cravado no motor, então TODA
atividade exibia objetivos de planta — e, como as fases registram sob os conceitos
DELAS (`objetivo1/2/3`), o domínio saía 0% em tudo. Conserto: o relatório itera
`ROTULOS` (os conceitos reais que o montador injeta de `conteudo["conceitos"]`);
`CONC` virou `{}`. Toda atividade precisa de `conceitos` no conteudo.json (o
montador avisa se faltar). Foi bug de MOTOR: valia para todas as atividades.

**Voz dizia "feice" em "face".** A voz pt-BR do Edge lê "face"/"faces" com sotaque
inglês. Não dá para mudar a tela (a professora quer ler "face") nem a CHAVE (o
`id`/hash sai do texto da tela, é o que casa o mp3). Conserto: `_fonetica_voz` em
`montar.py` reescreve SÓ o `texto` que vai ao TTS (face→fásse), aplicado depois do
`id` e numa varredura final sobre TODAS as falas (inclusive colhidas antigas).
Palavra nova que a voz erra entra só nesse dicionário (fonte única).

**Narração só na 1ª rodada (escolher etc.).** O motor narrava o balão UMA vez, ao
abrir a fase; peças de várias rodadas trocam o texto do balão e ficavam mudas da 2ª
em diante. Conserto: `narraBalao()` (fonte única) roda no abrir E no MutationObserver;
só fala quando o TEXTO do balão mudou (`__balaoNarrado`) e não reinicia o áudio em
curso — padrão da casa, vale para toda peça multi-rodada.

**Ligar muitos-para-um.** Cubo e pirâmide ambos "ficam firmes"; a criança era
reprovada por ligar ao "fica firme" do gênero errado. `casa()` na peça ligar aceita
par por `k` (exato) OU por `data-g` (grupo). Gaveta sem `g` = comportamento antigo.

**Gaveta de classificar quase invisível.** `fazGaveta` mostrava SÓ a marca d'água a
12% e, com `rot:false`, nem o nome — a gaveta virava fantasma. Conserto: `rot:true`
mostra figura NÍTIDA (`.gfig`) + nome (modo "aprender a categoria"); `rot:false`+img
segue marca d'água (legado dinheiro); sem img, só nome.

**Quebra-cabeça sumia no fundo.** Tabuleiro escuro fazia as peças (fotos) somirem.
`.qcmold` = moldura de vidro fosca centralizada em volta do tabuleiro (do tamanho
exato das vagas); vaga vazia com borda escura para ler no vidro.

**Arrastar-sombra "profissional".** Peça e sombra sem caixa (Marcos), mas o cenário
cheio some com elas: a atividade põe uma MESA de vidro (`.chao`/`.banco` no tema.css)
como palco; a peça em si fica limpa. `pool`+`n` na rodada sorteia formas a cada
jogada (aleatoriedade); `semSom` deixa o encaixe só visual.

## Lote Feirinha da Dona Coruja (ago/2026, Marcos ao vivo)

**⚠️⚠️ CRÍTICO — integrar ABORTA a escrita em silêncio.** A peça pintar-canvas
passou a chamar `Uint8Array` (fora dos globais do motor). O `integrar.py` imprimiu
`✗ AS PECAS CHAMAM 1 NOME(S) QUE NAO EXISTEM NO MOTOR: Uint8Array -> a peca nao se
reescreve` e **NÃO regravou pecas.js/json** — ou seja, NENHUMA peça recompilou
desde então, e uma correção já commitada (a máscara de repintura do Ateliê) **não
tinha ido ao ar**. Regra: depois de `integrar.py --escrever`, conferir que saiu
`escrito: pecas.js ... e pecas.css` e que NÃO há linha `✗ ... NAO EXISTEM` — se
houver, a build está velha. Nas peças, usar só globais do motor (Array, não
Uint8Array).

**Contagem (contadores) — sincronia e tema (o Marcos revisou fase a fase):**
- SINCRONIA: a versão guiada por `speechSynthesis.onend` travava no Chrome real
  (o `onend` não vinha e a cadeia de passos parava) e ainda era voz-robô. Agora
  `dizConta` avança quando a VOZ GRAVADA do número termina (`falar(id,cb)` do
  motor, cujo cb vem do `ended` do áudio) — nunca pula, nunca desincroniza.
- FRUTA, não bolinhas: ao PÔR aparece a fruta do banco (`item`/`pImg`); ao CONTAR,
  cada fruta acende como BOLA com o número dentro (o número precisa aparecer).
- Premium: a "terra" virou BANDEJA de madeira clara; variedade de frutas por
  rodada; campos de tema opcionais na gaveta (`item,pl,sing,verbo,onde,label,selo`).

**base-dez "caixa de 10":** as unidades aceitam `pImg` (fruta do banco) no lugar do
quadradinho abstrato — concreto para o 1º ano. Sem `pImg`, o bloco de sempre.

**completar "quanto falta":** a frase-problema morava num `.frase` que o motor NÃO
narra (só narra `.balao`). Agora a peça narra a conta (ante+dep) com a voz gravada
(o `falar` do motor enfileira depois do enunciado); calado se não houver gravação.

**Campo novo na gaveta = campo novo no EXEMPLO da peça.** Todo campo opcional novo
(`item`, `pImg`, `pool`, `enunPorque`, `g`...) precisa aparecer no exemplo `var`
da peça, senão o montador reprova ("campo não existe no exemplo"). Regra por gesto.

## Robustez em máquina antiga / rede filtrada (Marcos, ago/2026: "trava aleatório só em alguns PCs")
Análise de por que ALGUMAS máquinas travam ALEATORIAMENTE em ALGUMAS fases — e os
consertos no MOTOR (valem para toda atividade REMONTADA):
1. **`new AudioContext()` sem try/catch (o pior).** Rodava no topo do script; em PC
   cujo navegador já está no limite de 6 contextos de hardware (outras abas/
   extensões) ele ESTOURA e, sem proteção e no topo, derruba TODO o resto — a
   atividade nem monta. É "aleatório e só em algumas máquinas" (depende do que o
   navegador tem aberto). Conserto: `try{ac=new AC()}catch(e){ac=null}`.
2. **Faltava `window.onerror`.** Sem rede de segurança, qualquer exceção não tratada
   num clique/timer deixava a fase PRESA, sem avançar e sem aviso. Agora um erro não
   tratado mostra um botão de RESGATE "Continuar ▶" que pula para a próxima fase.
3. **`falar(id,cb)` sem watchdog.** Se o áudio emperra (rede filtrada: `play()`
   resolve mas `ended` nunca vem), o `cb` de quem esperava a voz para avançar nunca
   chegava e a fase congelava. Agora um teto de 10s força `fimFala` — o `cb` sempre
   dispara. (O `depoisDaFala` já tinha o dele.)
4. **Voz que morre no meio.** O mesmo watchdog pausa o `narr` travado e drena a fila
   de vozes (`_puxaFila`), senão a criança perdia a voz do resto da atividade.
Regra que fica: nenhum `new X()` de API de navegador (AudioContext, etc.) sem
try/catch; nenhum avanço de fase dependente SÓ de um evento de áudio.
