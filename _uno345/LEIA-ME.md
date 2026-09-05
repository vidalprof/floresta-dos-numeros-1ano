# UNO dos Números — 3º, 4º e 5º ano

Pedido do Marcos (set/2026): *"Lembra do jogo do uno? Que criamos? Preciso de uma
versão mais difícil para os 3/4/5 anos"*.

O jogo antigo (`_uno1/`, no ar em <https://vidalprof.github.io/jogoUno1->) continua
existindo e continua sendo do 1º ano. **Nada dele foi apagado** — este é um jogo
novo, num repositório novo, como manda a regra da casa.

---

## O que ficou mais difícil (e por quê)

Fui medir **por que** o jogo do 1º ano é fácil, em vez de chutar. Não era o
baralho: era o **adversário**. A linha original dizia, literalmente:

```js
let idx = cpu.findIndex(c => podeJogar(c));   // joga a PRIMEIRA que serve
```

Ele não escolhia nada. Pegava a primeira carta jogável **na ordem em que ela caiu
na mão**. Não guardava coringa, não trocava para a cor que tinha mais, não atacava
quando a criança estava com uma carta só. Criança de 9 anos percebe isso na
terceira partida.

### 1. O robô que pensa

Agora ele **pontua** cada carta jogável (`notaDaCarta`) e joga a de maior nota:

| o que ele passou a fazer | peso | por quê |
|---|---|---|
| encadear **pular / girar** | +38 | com 2 jogadores essas cartas devolvem a vez: é uma carta a menos **de graça**. É a jogada mais forte do jogo |
| **guardar o coringa** | −40 | soltar coringa cedo é o erro nº 1 de quem joga mal |
| …e **soltar o +4** quando a criança está com ≤2 cartas | +70 | ou quando ele não tem a cor (+55) |
| **atacar** com +2 na hora certa | +60 | |
| **ficar na cor** que ele tem mais | +12 | assim ele continua tendo jogada |
| **contar cartas** (só nível 5) | +25 | se a criança comprou, é porque não tinha aquela cor — ele insiste nela |
| **errar de propósito** (só nível 3) | ruído ±15 | ele pensa, mas se distrai como um humano |

Pontuação em vez de uma escada de `if` porque assim dá para afinar um peso sem
reescrever a lógica.

### 2. A regra da rodada — o que transforma o jogo em ATIVIDADE

O gesto natural do UNO é **combinar por atributo** (cor, número, tipo). Em vez de
enfiar matemática por fora, a regra monta em cima desse mesmo gesto: de vez em
quando a mesa pede uma condição **a mais** sobre o número da carta, numa tarja
amarela que também é **narrada**.

| ano | regras |
|---|---|
| **3º** | par / ímpar · maior que a da mesa · a sua + a da mesa = 10 |
| **4º** | múltiplo de 3 · múltiplo de 5 · o dobro da carta da mesa · a metade dela |
| **5º** | múltiplo de 3 · **a soma das duas é múltiplo de 3** · o dobro · soma 10 |

**O ano vem do LINK** (`?ano=3`, `?ano=4`, `?ano=5`; sem nada = 4º). Não há
seletor na tela de propósito: a criança do 3º escolheria o do 5º "pra ver se é
mais legal", levaria uma surra do robô e desistiria. Quem cola o link é o
professor, um por turma, no controle do laboratório.

### 3. A capa

Pedido do Marcos (set/2026): *"o uno novo é para ser para 3/4 e 5 anos, precisa
estar isso na capa"*. Antes disto o jogo **não tinha capa** — abria direto na
mesa, com o ano só num `small` de 13px ao lado do logotipo, e quem abria o link
não tinha como saber de que turma era aquilo.

A capa mostra os **três anos lado a lado, com o ativo aceso**, mais a linha
"Esta partida está no Nº ano". Isso não é enfeite: é como o professor confere,
em um olhar, se colou o link certo para a turma que está na sala.

Os três anos são **plaquinhas, não botões** — pelo mesmo motivo de não haver
seletor.

⭐ E a capa resolve uma coisa que estava quebrada e eu não tinha visto: **nenhum
navegador deixa a voz começar antes de um gesto**. Sem capa, a primeira narração
do jogo simplesmente não saía. Agora o botão **JOGAR é o "start"** que destrava
o som — e há um **🔊 Ouvir** para quem quiser a capa lida em voz alta.

O leque de cartas da capa é montado com o **mesmo `conteudoCarta`** do jogo: se
o desenho da carta mudar, a capa muda junto, sozinha. O mascote é **clonado** do
tutorial pelo mesmo motivo — um desenho só, um lugar só para mexer.

---

## As armadilhas que já estão fechadas (não reabrir)

1. **A partida não pode travar.** A regra só entra se a criança tiver saída, e
   ação/coringa **nunca** são bloqueados. Medido: 0 travas em 360 partidas
   automáticas.
2. **A regra tem que APARECER.** A 1ª versão sorteava UMA regra e desistia se ela
   não coubesse — e como as regras difíceis quase nunca cabem, no 4º ano ela saía
   em só **28 de 120 partidas**. Agora ele embaralha as regras do ano e faz dois
   passes: primeiro procurando uma que deixe **duas ou mais** saídas (a criança
   escolhe), e só então aceitando uma que deixe **uma**.
3. **A voz não pode ser cortada.** `setMensagem` chama `falar`, que começa com
   `speechSynthesis.cancel()`. Duas falas seguidas viram uma, com a primeira
   cortada no meio — a criança ouviria *"Atenção! Regra desta ro—"*. Por isso a
   regra entra **na mesma fala** da mensagem, nunca numa fala à parte.
4. **A ordem em `vezDoJogadorComMensagem`**: sortear a regra **antes** do
   `render()` e do `temJogada()`. Ao contrário, a mão já estaria pintada com as
   cartas antigas brilhando e a criança tocaria numa que a regra acabou de barrar.
5. **O "conta cartas" tem que esquecer.** `_corQueFaltou` só era marcado e nunca
   apagado: depois de algumas compras as quatro cores estavam marcadas e o bônus
   valia para tudo, ou seja, para nada.
6. **1024 × 600 é a tela do laboratório.** Herdado do jogo do 1º ano, nesse
   tamanho a **mão da criança ficava inteiramente fora da tela** — ela via a
   mensagem "toque numa carta que brilha" e nenhuma carta. É o defeito clássico
   do `_qa/leiaute.js`. Curado com o modo compacto (`max-height:820px, max-width:560px`),
   que encolhe a **moldura**, nunca o **alvo**.
7. **O verso do robô não escreve nada.** As cartas dele são um leque sobreposto;
   um "UNO" em cada uma aparecia cortado e o topo da tela lia **"UNUNUNUNUNUNO"**.
   Agora é o oval branco inclinado, que é a marca da carta e não vira sopa de letra.

---

## Como isto foi medido (não "eu olhei e achei bom")

O testador `unoteste.js` **joga partidas inteiras sozinho** e cobra:

* nenhum erro de JS na página;
* nenhuma partida travada;
* nenhuma carta brilhando contra a regra da rodada (e a tarja nunca mente);
* a regra realmente aparece.

E o `unoforca.js` mede a **força do robô** com a regra desligada, contra o robô
antigo, com o mesmo jogador automático burro (joga a primeira carta que brilha) —
maçã com maçã. ⚠️ Nesse benchmark é obrigatório **zerar `_derrotasSeguidas` a cada
partida**: o alívio anti-frustração deixa o robô em força mínima depois de duas
vitórias seguidas dele, e numa corrida de 250 partidas isso apaga a diferença
entre os níveis (a 1ª medição chegou a dizer que o nível 5 era o mais fraco).

### O que a medição disse — inclusive o que eu não queria ouvir

250 partidas por nível, regra desligada:

| | robô venceu |
|---|---|
| robô **antigo** (1º ano) | **52%** |
| nível 3 | 58% |
| nível 4 | 56% |
| nível 5 | **64%** |

O robô ficou mais forte que o antigo, e o nível 5 (o que conta cartas) se destaca.
Mas **o 3 e o 4 são indistinguíveis** — 2 pontos, com margem de erro de ~4,4
pontos na diferença. Fica registrado com todas as letras para ninguém (nem eu,
noutra sessão) contar uma história melhor do que a verdade: **entre o 3º e o 4º
ano a escada é a das REGRAS**, não a da força do robô — e é onde ela tem que
estar, porque é a parte que ensina.

Frequência da regra, no mesmo teste: **3,1 por partida no 3º ano · 2,1 no 4º ·
2,3 no 5º**. (As regras do 4º e do 5º são mais exigentes, então cabem menos vezes
— por isso o sorteio faz dois passes.)

---

## Anti-frustração (invisível de propósito)

A cada **duas derrotas seguidas** da criança o robô afrouxa um degrau; a cada
quatro, dois. Quando ela ganha, ele volta à força cheia. **Nada na tela diz isso**
— saber que o robô pegou leve estraga a vitória.

## O que este jogo NÃO tem (e por quê)

Não tem **boletim/relatório do professor** nem **retomada de 55 minutos** do
`_padrao/FIM-DE-ATIVIDADE.md`. Aquelas regras foram escritas para atividade de
fases com objetivos: aqui não há fase para "retreinar o que faltou", e uma partida
dura ~3 minutos, então fechar a aba sem querer não custa uma aula de trabalho.
Se o Marcos quiser um placar de partidas por aluno, dá para acrescentar — é
pedido dele, não decisão minha.
