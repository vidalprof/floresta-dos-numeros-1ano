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
