# 🎬 MUNDO-VIVO-SPRITES — o manual do movimento premium

**Projeto Mundo Vivo · Confeitaria = implementação de referência · jul/2026**
**Leitor-alvo:** um profissional que nunca viu o projeto e precisa produzir movimento PREMIUM sozinho.

> **Tese (a receita inteira numa linha):** um sprite premium não é um PNG bonito — é a
> soma de cinco coisas, e todas as cinco são obrigatórias:
>
> **cartela bem pedida** (a IA dá poses com contraste e escala consistente) **+ corte
> normalizado** (todas as poses do mesmo conjunto num canvas comum, pés na base — a cura do
> "piscar") **+ timing do demo** (os números canônicos do motor de referência, não "no olho")
> **+ suculência** (o código põe peso, atraso, arco e som por cima das poses) **+ QA de rajada**
> (o movimento se prova no tempo, com log, antes de chegar ao professor).
>
> Tire uma das cinco e o resultado cai de "jogo do Poki" para "GIF de 1998". Este manual é o passo
> a passo das cinco, com o **código real** dos dois motores testados
> (`_pub_confeitaria/mundo/index.html`, lateral; `.../proto/index.html`, top-down) e do **script
> oficial de corte** (`_ferramentas/cortar_sprites.py`).

---

## Índice

1. **[Capítulo 1 — Princípios de animação aplicados a sprites 2D](#capitulo-1)** — fazer 2 poses
   lerem como 8; os 12 princípios da Disney para "poucas poses de IA + interpolação CSS/JS".
2. **[Capítulo 2 — Produção de cartelas e corte](#capitulo-2)** — como pedir a cartela; o
   `cortar_sprites.py` linha a linha; o canvas comum; o catálogo de defeitos de corte.
3. **[Capítulo 3 — O código do movimento natural (cookbook ES5)](#capitulo-3)** — o código real
   dos dois motores, cada trecho com o defeito visível que cura.
4. **[Capítulo 4 — Premium × amador (checklist de suculência)](#capitulo-4)** — o checklist
   auditável de "juice" com os valores reais do motor + os 10 upgrades de maior impacto.
5. **[Capítulo 5 — O ritual de QA de movimento](#capitulo-5)** — o QA canônico (Playwright) + a
   rajada de screenshots headless para caçar piscar e pulo de escala.
- **[Anexo A — O script oficial de corte](#anexo-a)** · **[Rodapé — A regra do Marcos](#rodape)**

---

<a name="capitulo-1"></a>
# Capítulo 1 — Princípios de animação profissional com poucos quadros

## Por que este capítulo existe

Nossos jogos rodam em PC velho de escola pública: 1 HTML, ES5, sem WebGL, sprites em PNG data-URI
gerados por IA e recortados com Python. Não temos 24 desenhos por segundo — temos 2, 4, no máximo
8 poses por ação. A boa notícia: os princípios que fazem um Monkey Mart parecer "vivo" não
dependem de quantidade de quadros. Dependem de **quais poses você escolhe** e do **que o código faz
entre elas**. Este capítulo destila os 12 princípios da Disney (*The Illusion of Life*) para a
nossa realidade — e está ancorado no **código real** dos dois motores
(`_pub_confeitaria/mundo/index.html`, lateral; `.../proto/index.html`, top-down) e nas **lições
pagas** de `MUNDO-VIVO-MOTOR.md` §8 e `MUNDO-VIVO-ESPINHA.md` §3/§6. Os números "canônicos" foram
lidos desses arquivos, não estimados.

A regra-mãe do nosso pipeline, antes de qualquer princípio:

> **Os quadros de IA dão as POSES-CHAVE. O código dá o MEIO.**
> Um ciclo de 2 quadros trocando secamente parece um GIF de 1998. Os mesmos 2 quadros com bob
> vertical senoidal, leve inclinação no sentido do movimento e squash na aterrissagem — tudo
> `transform` em código — parecem um jogo do Poki. Nunca dependa só da troca de imagem; nunca
> tente compensar pose ruim com código.

E a regra-mãe da produção (a cura do piscar): **todos os quadros de um mesmo conjunto são
recortados num canvas comum**, com a mesma âncora (pés na base, centro horizontal). Se cada
quadro for autocropado individualmente, o personagem "pulsa"/"teleporta" 2–5px a cada troca e a
animação inteira treme. Esse é o motivo de existir o script oficial de corte
(`_ferramentas/cortar_sprites.py`, função `normaliza_set`) — quadros de uma ação são um
**conjunto**, não imagens soltas. (Capítulo 2 mostra o script inteiro.)

---

## 1. Anatomia do ciclo de caminhada

**O que é.** Todo ciclo de caminhada profissional se decompõe em 4 posições por passo
(nomenclatura de Richard Williams, *The Animator's Survival Kit*):

1. **Contato** — o calcanhar da frente toca o chão; pernas e braços no máximo da abertura. É a
   pose mais LEGÍVEL — é ela que diz "estou andando".
2. **Baixo (down)** — o peso desce sobre a perna da frente; joelho dobra; o corpo afunda. É onde
   mora o peso.
3. **Passagem (passing)** — uma perna passa pela outra; corpo quase reto, no meio da subida.
4. **Alto (up)** — o corpo no ponto mais alto, impulsionado pela perna de trás, antes do próximo
   contato.

Um passo completo = essas 4 posições **duas vezes** (perna esquerda à frente, depois direita),
ou seja, 8 posições por ciclo.

**Por que 2 quadros já funcionam.** As duas poses de máximo contraste são **contato** e
**passagem**: pernas abertas × pernas fechadas. O olho humano completa o movimento entre elas
(fenômeno phi — o mesmo que faz o cinema funcionar). Um ciclo
contato→passagem→contato-espelhado→passagem já lê como "andando" sem ambiguidade. Com sprite
simétrico dá para fazer com **2 imagens**; se braços/mochila quebram a simetria, são 4
(contato-E, passagem, contato-D, passagem).

**Por que 4 ficam premium.** O que falta no ciclo de 2 é o **peso**: sem a pose "baixo", o
personagem flutua; sem a "alto", não há impulso. Com 4 quadros por passo o corpo sobe e desce, e
é essa oscilação vertical que o cérebro lê como massa. **Truque do nosso pipeline:** não gaste
quadros de IA com baixo/alto — gere só contato+passagem e faça a oscilação em código
(`translateY` senoidal sincronizado com a troca de quadro). É exatamente o que o motor faz: no
top-down, `chef.bob` é um `|sin|` de amplitude 3.2px suavizado; no lateral, a respiração/quique
são `transform` puros. **2 poses + bob + leve inclinação = leitura de 8 quadros.**

**Como pedir à IA.** Na cartela: "mesmo personagem, mesma escala, mesma direção, pose 1 =
passada aberta (uma perna à frente, braço oposto à frente), pose 2 = pernas se cruzando, pés
próximos". Exigir mesma altura de olhos nas duas poses (senão o canvas comum não alinha). A
lição registrada (`MUNDO-VIVO-ESPINHA.md` §6) é literal: *"corpo idêntico nos dois quadros, só
pernas/braços trocam"*.

**Erro típico que quebra.** (a) Duas poses quase iguais — a IA adora gerar "andando 1" e
"andando 2" com 5° de diferença; o resultado é vibração, não caminhada. Exija contraste máximo
entre as poses. A lição paga é taxativa: *"andar duro/sem vida → o problema NUNCA é o timing; é o
PAR de poses"* (`MUNDO-VIVO-ESPINHA.md` §6). (b) Pés que não "prendem" no chão: se a cadência da
troca de quadros não bater com o deslocamento, o personagem patina (moonwalk). A cura do nosso
motor é o §12 deste capítulo: **quadro por DISTÂNCIA**.

## 2. Corrida

**O que é.** Corrida não é caminhada rápida. Muda a natureza: existe um momento **sem nenhum pé
no chão** (suspensão), o tronco inclina para a frente, os braços bombeiam, a passada é maior.

**Com 2–4 quadros.** Ciclo mínimo = 2 poses: **impulso** (perna de trás estendida, corpo esticado
= stretch) e **recolhida** (pernas dobradas sob o corpo = squash). Em código: inclinação fixa
(5–10° com `rotate`), bob mais AMPLO e RÁPIDO que o da caminhada, troca de quadro mais frequente.
Poeirinha nos pés (`mvPuff()`, 2–3 partículas) vende velocidade quase de graça.

**Erro típico.** Usar os quadros da caminhada tocados mais rápido — lê-se como "andando nervoso",
nunca como correndo (falta suspensão e inclinação). Sem orçamento para poses de corrida, prefira
não ter corrida.

## 3. Parado respirando (idle)

**O que é.** Personagem parado imóvel = personagem morto. O idle é a respiração: o corpo sobe e
desce num ritmo lento, com tudo o mais quase parado.

**Com 1 quadro (sim, um).** É a ação mais barata do jogo: **1 pose + código**. Estes são os
valores **reais** do motor (não invente outros):

- **O que está publicado hoje** (`_pub_confeitaria/mundo/index.html`, classe `.mvResp`):
  `scale(1)` → `scale(1.025)` **uniforme** (X e Y iguais), `2.6s` por ciclo, `ease-in-out`,
  `infinite`, com o par `-webkit-`. Repare: é `scale` uniforme, **não** `scaleY` com `scaleX`
  compensatório para baixo.
- **A lição refinada registrada** (`MUNDO-VIVO-MOTOR.md` §8): `scale(1.018, 1.05)` com
  `transform-origin` **nos pés**. Ou seja, o scaleY chega a ~**5%** (a respiração é o tórax
  subindo) e o scaleX vai levemente para **cima** (1.018), não para baixo. Não existe teto de
  "3%" no projeto — o valor pago é 5% no eixo Y.

```css
/* real: _pub_confeitaria/mundo/index.html */
.mvResp img{-webkit-animation:mvResp 2.6s ease-in-out infinite;animation:mvResp 2.6s ease-in-out infinite;}
@-webkit-keyframes mvResp{0%,100%{-webkit-transform:scale(1)}50%{-webkit-transform:scale(1.025)}}
@keyframes mvResp{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
/* variante refinada (MUNDO-VIVO-MOTOR.md §8): scale(1.018,1.05), origem nos pés */
```

**A regra que importa** (essa sim, confirmada e inegociável): **`transform-origin` sempre na
base do sprite** (`50% 100%` / `bottom center`). Origem no centro faz o personagem **levitar**
(os pés saem do chão) em vez de respirar — a lição literal é *"do centro parece zoom"*
(`MUNDO-VIVO-MOTOR.md` §8). Com 2 quadros de IA (olhos abertos/fechados) adiciona-se a
**piscada**: não em ritmo fixo — a cada 3–6 s aleatório. Ritmo fixo parece metrônomo; aleatório
parece vivo. E o próprio motor tem uma micro-ação de idle: depois de **~4s** parado o chef
**acena** (troca para `IMG.mv.acena`) e repete a cada **~6s** — é o detalhe que o professor chama
de premium (código real no §11 do Capítulo 3).

## 4. Sentar

**O que é.** Sentar é uma transição com peso: o corpo desce, freia, acomoda.

**Com 1 quadro.** A pose sentada é 1 quadro de IA (a cartela `td_sentados.png` do motor top-down
é exatamente isso: clientes sentados como poses únicas, recortadas em `td_sentados` — ver o
`cortar_sprites.py`). A transição em pé→sentado é **código**, e o motor a resolve com uma coisa
simples e eficaz: uma `transition` de `margin-top` que "assenta" o cliente na cadeira:

```js
/* real: _pub_confeitaria/proto/index.html — cliente chega e SENTA */
spr(c.el, c.tipo+"_sentado");
c.el.style.webkitTransition = "margin-top .35s";
c.el.style.transition        = "margin-top .35s";
c.el.style.marginTop = "-96px";      // sobe/acomoda no assento em 350ms (ease do browser)
try{ plimP(520); }catch(e){}          // "plim" de confirmação
```

Sentado, o personagem continua com o idle de respiração (o mesmo `.mvResp`/`scaleY` de sempre).
Um cliente sentado que respira e pisca segura uma cena inteira com um único PNG.

**Erro típico.** Teleporte: trocar de pose em pé para pose sentada em 1 frame. Também: esquecer a
**oclusão da mesa** — sentado atrás da mesa, a parte de baixo do sprite deve ficar coberta
(ordem de desenho por Y, `zIndex = Math.round(c.y)` no motor — ver §12); personagem "sobre" a
mesa destrói a cena.

## 5. Carregar objeto

**O que é.** Carregar muda a postura: braços ocupados (não balançam), passada mais curta.

**Com 2 quadros + composição.** Duas estratégias:
- **Barata (preferida):** ciclo de andar "de braços ocupados" (2 quadros com braços fixos à
  frente) e o **objeto é um sprite separado** por cima, ancorado nas mãos, herdando o bob **com
  meio ciclo de atraso e amplitude menor** (movimento secundário de graça, §9). Qualquer objeto
  usa o mesmo ciclo.
- **Cara:** cartela do personagem já segurando cada objeto. Só vale para O objeto icônico do jogo.

**Erro típico.** Objeto **grudado rígido**, sem atraso nem oscilação — parece adesivo colado. E
objeto que pisca de posição por ter sido ancorado no bounding box do quadro (que muda) em vez de
numa âncora fixa do canvas comum.

## 6. Virar de direção

**O que é.** Na vida real ninguém gira instantaneamente 180°. Em animação limitada, a virada
precisa de pelo menos um "amortecedor" visual.

**Com 0–1 quadro extra.** Ordem de custo:
- **Custo zero (lateral):** espelhar com `scaleX(-1)`. É exatamente o que o mundo faz —
  `(MV.dir<0?" scaleX(-1)":"")` no transform do chef. Aceitável SE o personagem for
  razoavelmente simétrico (atenção: mochila, franja e detalhes assimétricos denunciam).
- **Custo zero premium:** não espelhar seco — encolher `scaleX` até ~0.1 em ~60 ms, trocar o
  sinal, voltar a 1. O personagem "gira sobre o próprio eixo". Três linhas, enorme ganho.
- **1 quadro:** uma pose "de frente" (ou ¾) usada como quadro do meio da virada. É o que separa 4
  direções de verdade. O motor top-down faz assim: `chef_baixo` (2 quadros), `chef_cima` (4
  quadros), `chef_lado` (4 quadros) e a **esquerda é o espelho do lado** (`scaleX(-1)`) — cortando
  a cartela de 4 direções para **3 poses únicas** (ver `cortar_sprites.py`, blocos `setA/setC/setL`).

**Erro típico.** Espelhar personagem com assimetria forte (todo mundo vê a mochila trocar de
ombro); e virar sem nenhuma transição durante o movimento contínuo — o flip seco no meio de uma
caminhada é o momento mais "de máquina" de um jogo simples.

## 7. Squash & stretch (pulos e aterrissagens)

**O que é.** Princípio nº 1 da Disney: o que é vivo deforma. Estica na velocidade (stretch),
amassa no impacto (squash), **sempre conservando volume** — se `scaleY` desce, `scaleX` sobe na
proporção.

**Com 0 quadros (é todo em código).** Não gaste cartela com isso. O **valor canônico do nosso
motor** para a aterrissagem é mais forte do que se imagina — leia do código, não do "olho":

```css
/* real: _pub_confeitaria/mundo/index.html — squash de POUSO */
.mvSquash img{-webkit-transform:scaleY(.82) scaleX(1.12)!important;transform:scaleY(.82) scaleX(1.12)!important;}
```

Isto é **18% de compressão vertical** (`scaleY .82`) e **12% de esticão horizontal**
(`scaleX 1.12`). Ou seja: para o nosso estilo cartoon, o squash de aterrissagem chega a ~**12–18%**
— bem acima do "6–12%" que às vezes se cita de outros estilos. E ele dispara **no impacto**, no
instante em que `MV.y <= 0` (o chef toca o chão), some depois de **180ms** e volta ao normal
(código no §7 do Capítulo 3). Amplitudes de referência: antecipação (agachar antes de pular) mais
suave (~6–8%); aterrissagem forte (~12–18%, o `.mvSquash` real).

O mesmo par squash/stretch serve para botão apertado, moeda coletada, mascote comemorando — é o
tempero universal.

**Erro típico.** (a) Esquecer a conservação de volume: só `scaleY` faz o personagem "derreter".
(b) `transform-origin` no centro: o squash levanta os pés do chão e o impacto perde todo o
sentido. Origem na base (`50% 100%`). (c) Exagero com duração longa: squash é RÁPIDO
(≤180 ms, como o motor); lento vira gelatina.

## 8. Antecipação

**O que é.** Todo movimento forte é precedido por um movimento pequeno no sentido CONTRÁRIO:
agachar antes de pular, recuar o braço antes de arremessar. É o que torna a ação legível — o olho
é avisado do que vem.

**Com 0–1 quadro.** Quase sempre em código: um deslocamento/escala contrário de 60–120 ms antes da
ação. Limite com input de criança: a antecipação não pode atrasar a resposta ao toque — mantenha
≤100 ms, ou aplique-a só em ações autônomas dos NPCs, onde pode ser generosa.

**Erro típico.** Ação que "nasce do nada" (o cliente levanta instantaneamente, o mascote dispara
sem inclinar). Cada ação sem antecipação é um teleporte de intenção — o somatório é o "duro" que o
professor chama de não-premium.

## 9. Follow-through e movimento secundário (orelhas, rabo, roupa)

**O que é.** Quando o corpo para, as partes moles continuam (follow-through); quando o corpo se
move, elas se movem **atrasadas e com vida própria** (overlapping/secundário). Orelhas, rabo,
cabelo, avental, chapéu.

**Com 0 quadros — a técnica da camada atrasada.** A mais rentável do pipeline: peça à IA o
apêndice expressivo (orelha, rabo, chapéu) **em sprite separado na mesma cartela**. No jogo, é um
`<img>` filho ancorado no pivô, que herda o movimento do corpo com **atraso de 60–120 ms e rotação
própria de ±4–8°** (senoide defasada do bob). Corpo para → orelha balança mais 2–3 oscilações
amortecidas. ~10 linhas de ES5, e é o efeito que mais aproxima do padrão Poki.

**Erro típico.** Tudo em fase (corpo, orelha e chapéu subindo JUNTOS) — vira estátua num
trampolim. A alma do secundário é a **defasagem**. E apêndice com pivô errado (orelha girando pelo
meio em vez da raiz).

## 10. Silhueta legível em tamanho pequeno

**O que é.** *Staging*/desenho sólido: a pose deve ser reconhecível como sombra preta pura. Nossos
sprites vivem entre 50 e 150 px num projetor ruim — a silhueta é o que sobrevive.

**Como aplicar com IA.** (a) Prompt: "poses de corpo inteiro, braços afastados do tronco, silhueta
clara" — braço colado no corpo some em 60 px. (b) Contorno escuro e fechado (já é requisito do
recorte: `cortar_sprites.py` pega o **maior componente conectado**; contorno aberto vaza fundo).
(c) **Teste obrigatório:** reduza a 48 px e pinte de preto. Se não dá pra dizer se o chef carrega
ou acena, a pose é ruim — regere. (d) As silhuetas das duas poses do ciclo devem ser
**distinguíveis entre si** (o contraste do §1 por outro ângulo).

**Erro típico.** Poses "bonitas de perto" que viram bolha em tamanho de jogo; e detalhe interno
tentando comunicar o que a silhueta deveria — em 60 px ninguém vê rosto.

## 11. Arcos

**O que é.** Nada vivo se move em linha reta: mãos, cabeças, saltos e objetos arremessados
descrevem arcos.

**Como aplicar.** Todo deslocamento composto tem componente vertical curva: item que "voa" ao
cesto vai por parábola (`4*h*t*(1-t)` no Y), não por reta; a moeda ao placar sobe em arco
(`mvVoaMoeda()`); o próprio bob é um arco repetido (`Math.abs(Math.sin(...))`). Em ES5, uma função
`arco(p0,p1,h,t)` de 3 linhas reaproveitada em tudo.

**Erro típico.** `left/top` interpolados linearmente (elevador em diagonal) — a assinatura do
amadorismo. E animar `left/top` em vez de `transform` (custo de layout em PC velho; só animamos
`transform`+`opacity`, regra da casa).

## 12. Timing — e a regra paga: QUADRO POR DISTÂNCIA

**O que é.** O princípio do timing diz que a DURAÇÃO define o significado (rápido = leve/nervoso;
lento = pesado/calmo). No nosso motor ele tem um **corolário pago, aprendido na dor**, que corrige
a intuição ingênua de "troca o quadro a cada X milissegundos":

> **Passo por DISTÂNCIA, não por tempo** (`MUNDO-VIVO-MOTOR.md` §8): trocar o quadro do ciclo de
> caminhada **a cada ~34px percorridos** — senão o pé patina na aceleração. Enquanto o
> personagem acelera/desacelera, um relógio de "a cada 140 ms" faz o pé escorregar (moonwalk); um
> relógio de "a cada 34 px" faz o pé **prender** no chão em qualquer velocidade.

É assim que o motor top-down realmente escolhe o quadro — **pela distância acumulada, não por
ms fixo**:

```js
/* real: _pub_confeitaria/proto/index.html — quadro do chef pela DISTÂNCIA andada */
chef.dTot = (chef.dTot||0) + passo;        // passo = distância percorrida neste frame
chef.frame4 = Math.floor(chef.dTot/13)%4;  // ciclo de 4 poses: um quadro a cada 13px
chef.frame  = Math.floor(chef.dTot/24)%2;  // ciclo de 2 poses: um quadro a cada 24px
```

Repare que o quadro é `Math.floor(distância / passoEmPx)`, não `Math.floor(agora / passoEmMs)`.
Assim, se o chef está parando, os quadros também "param"; se dispara, aceleram junto. Zero patinada.

**Onde o TEMPO ainda manda.** Timing por tempo continua correto para tudo que **não é
locomoção**: respiração (`mvResp` 2.6s), squash de pouso (180 ms), aceno idle (~4s/~6s), clima
(dia 70s/noite 45s). Para essas, vale o corolário técnico clássico do navegador: **o relógio é o
tempo real, nunca a contagem de frames** — o PC da escola roda a 18 fps num dia e 60 no outro.
Deslocamento eased do mundo lateral usa `MV.vx += (alvo - MV.vx) * .16` por tick de 33 ms, e o
quique é senoidal; nada depende de "contar frames do navegador".

> **Nota honesta sobre o mundo lateral.** No `mvTick`, a troca de pose de andar do chef é
> disparada por `if (ag - MV.tFrame > 135)` — ou seja, **135 ms** entre poses. Isso não contradiz
> a regra: como a velocidade do mundo é fortemente suavizada (easing `.16`) e no cruzeiro fica
> quase constante, "135 ms" ≈ "~34 px" na prática. O **padrão seguro** — o que nunca patina em
> aceleração — é a distância; o 135 ms é o equivalente aceitável quando a velocidade é eased e
> estável. Na dúvida, **use distância**. (O "135 ms do demo" é canônico e testado — mexer nele é
> mecânica de motor, `MUNDO-VIVO-ESPINHA.md` §6/§7.)

**Erro típico.** Contar frames do navegador (o câmera-lenta do PC fraco); `dt` sem teto (aba
minimizada volta e o personagem atravessa a parede); e — o clássico do projeto — trocar o quadro
de andar por **tempo** e ver o pé patinar na aceleração. A cura é o `dTot` acima.

---

## Tabela final — quantos quadros para quê

Custo no nosso pipeline = prompt na IA + conferência da cartela + corte no canvas comum
(`cortar_sprites.py`) + de-halo + base64 no HTML (~cada quadro otimizado custa 15–50 KB de
arquivo). O código (bob, squash, camada atrasada, arcos) custa zero bytes de imagem — por isso a
coluna "código por cima" é sempre parte da receita.

| Quadros | Para quê serve | Código por cima (obrigatório) | Custo-benefício |
|---|---|---|---|
| **1** | Idle base, pose sentada, objeto carregado, poses de emoção (feliz/triste — `MASCOTE_POSES`) | Respiração `scale(1.025)`/`scale(1.018,1.05)` origem nos pés, piscada, camada atrasada p/ orelha/rabo | **Excelente.** O grosso do jogo vivo é 1 quadro + código. Comece sempre aqui. |
| **2** | Caminhada (contato+passagem), mastigar, martelar, abanar rabo, piscar | Bob vertical, inclinação no sentido do movimento, espelho `scaleX(-1)` p/ outro lado | **O melhor custo-benefício em movimento.** 2 poses de contraste máximo + código já leem como natural. |
| **4** | Caminhada premium (braços assimétricos), chef 4 direções (`chef_cima`/`chef_lado` de 4 quadros), corrida (impulso/recolhida ×2), virada com quadro de frente | Bob fino, squash de pouso `scaleY(.82)`, poeira `mvPuff` na corrida, quadro por distância | **O padrão "premium" do projeto.** Dobra o custo de cartela sobre o de 2; vale para o personagem principal e ações vistas o tempo todo. |
| **6** | Ação-assinatura vista de perto e repetida (mascote comemorando, chef decorando o bolo) | Menos dependente de código; ainda exige quadro por distância e âncora comum | **Caro.** Cartela maior = mais risco de inconsistência entre poses da IA. Só para 1–2 ações-vitrine por jogo. |
| **8** | Ciclo de caminhada completo desenhado (contato/baixo/passagem/alto ×2) | Quase nenhum | **Quase nunca compensa.** ~200–400 KB por ação, alta chance de a IA quebrar a consistência, e o ganho sobre "4 + código" é invisível a 60–100 px num projetor. Reserve para um único herói. |

Regra de bolso para fechar: **gaste quadros em POSES (o que o personagem faz), gaste código em
FÍSICA (como ele pesa)**. A IA é boa em pose e péssima em consistência; o código é perfeito em
consistência e incapaz de pose. Todo o capítulo cabe nessa divisão.

*Fontes: *The Illusion of Life* (Thomas & Johnston), *The Animator's Survival Kit* (Williams);
[SLYNYRD Pixelblog 50 — Walk Cycle](https://www.slynyrd.com/blog/2024/5/24/pixelblog-50-human-walk-cycle);
[12 Principles for Game Animation (Chris Totten)](https://totter87.medium.com/12-principles-for-game-animation-a9137ef44345).
Números canônicos: código de `_pub_confeitaria/mundo|proto/index.html`, `MUNDO-VIVO-MOTOR.md` §8,
`MUNDO-VIVO-ESPINHA.md` §3/§6.*

---

<a name="capitulo-2"></a>
# Capítulo 2 — Produção de cartelas e corte (o pipeline que funcionou)

## Por que este capítulo existe

Um quadro de IA lindo é inútil se não puder ser **recortado do fundo** e **alinhado** com os
outros da mesma ação. 90% do trabalho de sprite é isto: pedir a cartela de um jeito que o script
consiga cortar, e cortar de um jeito que os quadros não pulem. Pipeline **real**, ancorado no
`_ferramentas/cortar_sprites.py` (lido linha a linha — os limiares abaixo são os do arquivo). Quatro
etapas: **(a) pedir · (b) conferir · (c) cortar no canvas comum · (d) empacotar em base64** + o
catálogo de defeitos.

---

## (a) Pedir a cartela — o que a IA precisa entregar para o corte funcionar

O script corta **cartelas em grade** (grid), não imagens soltas. Ele espera um layout fixo por
tipo de personagem, e recorta cada célula com uma pequena margem interna (`+8/-8` px) para não
pegar a borda da célula vizinha. Exemplos reais do `cortar_sprites.py`:

- **Chef, andar de frente + parado + feliz** (`td_chef2.png`): grade **4 colunas × 2 linhas**,
  célula = `c*W/4 .. r*H/2` com margem `+8/-8`.
- **Chef, cima e lado** (`td_chef4.png`): grade **4 colunas × 3 linhas**, célula com margem
  `+12/-12`.
- **Clientes andando** (`td_anda_<bicho>.png`): grade **3 × 2** = 6 poses na ordem
  `costas0, costas1, costasP, frente0, frente1, frenteP`.
- **Clientes de lado** (`td_anda_lado.png`): grade **3 × 2**, cada bicho numa coluna, 2 poses.
- **Sentados** (`td_sentados.png`): grade **3 × 1**, um bicho por coluna.

Requisitos que o prompt à IA (Gemini, no fluxo do Mundo Vivo) **precisa** garantir, senão o corte
falha:

1. **Fundo liso e claro, quase branco** (o script detecta por `mn>240 & (mx-mn)<14`). Nada
   texturizado ou colorido perto do branco.
2. **Sem NENHUM texto** (nome de loja, rótulo, marca-d'água) — texto vira componente conectado e
   suja o recorte. No Mundo Vivo, texto em placa é **gravado por código com Pillow**, nunca pela IA
   (`MUNDO-VIVO-MOTOR.md` §6).
3. **Mesma escala e mesma linha de "chão"** em todas as células. O canvas comum alinha os pés, mas
   não conserta escala derivando entre poses.
4. **Contorno escuro e fechado** (silhueta sólida, Cap. 1 §10) — contorno aberto deixa o fundo
   vazar para dentro do sprite.
5. **Contraste máximo entre as poses** (contato × passagem, Cap. 1 §1): *"corpo idêntico nos dois
   quadros, só pernas/braços trocam"* (`MUNDO-VIVO-ESPINHA.md` §6).
6. **Personagem centralizado e inteiro** em cada célula, com folga (o `+8/-8`/`+12/-12` come uma
   faixa — pé na borda é cortado).

## (b) Conferir a cartela (antes de gastar corte)

Abra a cartela e cheque a olho, célula por célula: (1) a grade está regular? (2) todas as poses
têm a mesma altura de olhos/mesma escala? (3) o par de andar tem contraste real (pernas
abertas × cruzadas)? (4) o fundo é uniforme e claro nas quatro bordas de cada célula? Reprovou
qualquer um → **regere a cartela**, não tente salvar no corte (a lição do Cap. 1 §1/§10). Cartela
ruim custa 1 novo prompt; salvar no código custa horas e sai pior.

## (c) Cortar no canvas comum — o coração do pipeline

O `cortar_sprites.py` faz três coisas, nesta ordem, e é por isso que ele existe:

**1. Recorte do fundo (`recorta_raw`) — detectar o quase-branco e ficar com o maior blob.**

```python
def recorta_raw(cel):
    a=np.asarray(cel.convert('RGB')).astype(int)
    mx=a.max(2); mn=a.min(2)
    fundo=(mn>240)&((mx-mn)<14)          # pixel é fundo se: bem claro (mn>240) E pouco colorido (dif<14)
    lab,n=ndimage.label(fundo)
    borda=set()
    for v in (lab[0,:],lab[-1,:],lab[:,0],lab[:,-1]): borda.update(np.unique(v))
    borda.discard(0)
    obj=~np.isin(lab,list(borda))         # objeto = tudo que NÃO é fundo tocando a borda
    obj=ndimage.binary_opening(obj,iterations=2)   # tira pixels-fiapo soltos (2 iterações)
    obj=ndimage.binary_fill_holes(obj)             # tapa buracos internos (ex.: vão entre as pernas)
    lab2,n2=ndimage.label(obj)
    if n2==0: return None
    tam=ndimage.sum(obj,lab2,range(1,n2+1))
    keep=(lab2==(int(np.argmax(tam))+1))  # fica só com o MAIOR componente conectado (o personagem)
    ys,xs=np.where(keep)
    er=ndimage.binary_erosion(keep,iterations=2)   # anti-halo: erode 2px a máscara
    keep2=keep&~((keep&~er)&(mn>232))     # ...e remove a borda de 2px SE ela for clara (mn>232) = franja/halo
    rgba=np.dstack([np.asarray(cel.convert('RGB')),(keep2*255).astype(np.uint8)]).astype(np.uint8)
    return Image.fromarray(rgba).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
```

Os **limiares reais** (grave-os, não invente faixas): fundo = `mn>240` **e** `(mx-mn)<14`;
opening de **2** iterações; erosão anti-halo de **2 px** com corte da franja onde `mn>232`. (São
valores fixos do arquivo — o próprio comentário do script diz: *"NÃO mude os limiares sem
atualizar o manual MUNDO-VIVO-SPRITES.md"*.)

**2. Canvas comum por conjunto (`normaliza_set`) — a cura do "piscar".** Este é o passo que faz o
personagem não pulsar ao andar. Todos os quadros do MESMO conjunto vão para um **canvas único**,
com o personagem **centralizado em X e com os pés na base**, e só então redimensionados para a
altura-alvo:

```python
def normaliza_set(frames, alt):
    """frames 1:1 da mesma cartela -> canvas comum, pes na base, centro x; depois resize p/ alt"""
    maxh=max(f.height for f in frames); maxw=max(f.width for f in frames)
    CH,CW=maxh+4,maxw+6                    # canvas comum = maior quadro + folga
    outs=[]
    for f in frames:
        cv=Image.new('RGBA',(CW,CH),(0,0,0,0))
        cv.paste(f,((CW-f.width)//2,CH-f.height),f)   # centro X, base embaixo (CH-f.height)
        fw=int(CW*alt/CH)
        outs.append(cv.resize((fw,alt),Image.LANCZOS))
    return outs
```

Por que cura o piscar: autocropada sozinha, a pose de pernas abertas teria uma "caixa" mais larga
e baixa que a de pernas fechadas — e o `<img>` redimensionaria a cada troca (o "pulsar"). No canvas
comum, **todas as poses têm o mesmo tamanho e a mesma linha de chão** — a troca é invisível. Lição
literal de `MUNDO-VIVO-MOTOR.md` §8: *"recortar TODAS as poses da MESMA cartela em escala 1:1
(célula fixa + maior componente + pés alinhados num canvas comum). Autocrop+resize por pose =
personagem 'pulsando' ao andar."* Alturas-alvo reais: chef **118**, clientes **100**, sentados
**86**.

**3. Empacotar (`uri`) — quantizar e virar data-URI.**

```python
def uri(im):
    q=im.convert('RGBA').quantize(colors=255,method=Image.FASTOCTREE)   # 255 cores, octree rápido
    b=io.BytesIO(); q.save(b,'PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
```

`quantize(colors=255, FASTOCTREE)` + `optimize=True` derruba o peso do PNG sem estragar o sprite.
Cada pose fica na casa de 15–50 KB — o orçamento que mantém o HTML leve e o build do Pages sem
engasgar.

## (d) Onde os data-URIs entram no jogo

O script despeja as chaves num JSON (`out[...]`) que o motor lê como o objeto `IMG`. Cada `<div>`
de sprite recebe `background-image:url(<dataURI>)` via `spr()` (que só troca se a chave mudou —
micro-otimização real do motor):

```js
/* real: _pub_confeitaria/proto/index.html */
function spr(el,k){ if(el._k===k) return; el._k=k; el.style.backgroundImage="url("+IMG[k]+")"; }
```

E os nomes das chaves são exatamente os que o `tick` do jogo pede: `chef_baixo0`, `chef_baixo1`,
`chef_parado`, `chef_feliz`, `chef_cima0..3`, `chef_lado0..3`, `<bicho>_frenteP`,
`<bicho>_sentado`, etc. Manter os nomes casados entre o script e o motor é parte do contrato.

## Catálogo de defeitos de corte (o que já mordeu e como o script previne)

| Defeito | Como aparece | Causa | Cura no pipeline |
|---|---|---|---|
| **Piscar / pulsar ao andar** | O personagem "vibra"/muda de tamanho a cada troca de pose | Autocrop+resize por pose (caixas diferentes) | `normaliza_set`: canvas comum por conjunto, pés na base, mesmo tamanho para todas as poses |
| **Triângulo/vão entre as pernas fica transparente** | Buraco de fundo dentro do corpo | Flood-fill entrou pelo vão entre as pernas | `binary_fill_holes` tapa buracos internos após pegar o objeto |
| **Chapéu/orelha "roído"** | Detalhe fino some ou fica serrilhado | Erosão anti-halo forte demais numa parte fina E clara | A erosão só remove a borda de 2px **onde `mn>232`** (clara); detalhe escuro sobrevive. Se ainda roer, o problema é a cartela (contorno claro) — regere |
| **Corte pega só a cabeça (ou um item solto)** | O recorte vem incompleto | O "maior componente" era outro blob (item, sombra desconectada) | Garanta contorno **fechado** e personagem como o maior objeto contíguo; `binary_opening(2)` já mata fiapos que roubariam a contagem |
| **Franja/halo branco na borda** | Contorno claro "brilhando" no fundo colorido do cenário | Pixels de transição claro→personagem ficaram opacos | `keep2 = keep & ~((keep&~er)&(mn>232))` remove a casca de 2px clara |
| **Sprite "flutuando" acima do chão** | Base do personagem não toca a linha do piso | Margem inferior sobrando no canvas | `normaliza_set` cola os pés na base (`CH-f.height`); a baseline fica idêntica em todas as poses |
| **Peso do HTML explodindo / build engasga** | Arquivo gigante, Pages falha | PNG sem quantizar/otimizar | `quantize(255, FASTOCTREE)` + `optimize=True`; cada pose ~15–50 KB |

**Regra de fechamento do capítulo:** cartela é **conjunto**, não coleção de imagens. Peça a grade
certa, confira antes de cortar, corte **sempre** com `normaliza_set` (nunca autocrop por pose), e
confira a montagem final com o professor (screenshot da tira de poses) antes de fechar.

---

<a name="capitulo-3"></a>
# Capítulo 3 — O código do movimento natural (cookbook ES5)

## Por que este capítulo existe

O Cap. 1 diz *o que* fazer; este diz *como*, com o **código real** dos dois motores. Cada receita
traz o trecho verbatim, os números canônicos e **o defeito visível** que ele cura. Copie daqui;
não reinvente valores "no olho" — mudá-los é mecânica de motor (escalada,
`MUNDO-VIVO-ESPINHA.md` §7).

Dois motores, duas físicas: **Mundo lateral** (`.../mundo/index.html`, protagonista = o chef): rua
andável com câmera, gravidade e pulo, velocidade **eased**. **Confeitaria top-down**
(`.../proto/index.html`, o chef): planta baixa 8-direções com profundidade falsa por Y, velocidade
**constante** mas com quadro-por-distância + bob/lean suavizados escondendo a rigidez.

---

## 1. Deslocamento lateral com peso (easing) — mundo

```js
/* real: _pub_confeitaria/mundo/index.html — mvTick (roda a cada ~33ms) */
var alvo = MV.held * 5.4;              // held = -1 | 0 | 1 (tecla/seta pressionada)
MV.vx += (alvo - MV.vx) * 0.16;        // EASING: a velocidade PERSEGUE o alvo, não liga/desliga
if (Math.abs(MV.vx) < 0.05) MV.vx = 0; // "cola" no zero para não tremer parado
MV.pos += MV.vx;
if (MV.pos < 60) MV.pos = 60; if (MV.pos > MV.W-60) MV.pos = MV.W-60;
if (MV.held !== 0) MV.dir = MV.held;   // só vira quando há intenção real
```

**Números canônicos:** velocidade-alvo `held*5.4`; fator de easing **`0.16`** (não 0.18 — é o
valor testado, `MUNDO-VIVO-ESPINHA.md` §3). **O que cura:** o "boneco em trilho" que congela e
dispara instantaneamente. Com o easing `.16`, ao soltar a tecla o chef **desliza 2–4 frames**
antes de parar, e ao apertar acelera suave — é o nº 1 do que o cérebro lê como peso real. **Erro
se remover:** velocidade liga/desliga = robô.

## 2. Gravidade, pulo e squash de pouso — mundo

```js
/* real: _pub_confeitaria/mundo/index.html */
function mvPular(){ if(!MV.on||!MV.noChao) return;
  if(MV.naPorta&&MV.entrarOk){ mvEntrarAtual(); return; }   // seta pra cima na porta = ENTRAR
  MV.vy = 13.5; MV.noChao = false; mvBeep(330,660,.18,.1,"sine");   // impulso: glissando SOBE
}
/* dentro do mvTick: */
if(!MV.noChao){
  MV.vy -= 0.95; MV.y += MV.vy;                 // gravidade
  if(MV.y <= 0){                                // POUSO
    MV.y = 0; MV.noChao = true;
    mvBeep(110,70,.12,.12,"sine");              // baque grave: glissando DESCE
    $("mvChef").className = "mvSquash";          // achata no impacto (scaleY .82 scaleX 1.12)
    mvPuff(); mvPuff();                          // 2 partículas de poeira (nunca 1: some rápido demais)
    setTimeout(function(){                       // desfaz o squash em 180ms
      $("mvChef").className = (MV.vx===0 ? "mvResp" : "");
    }, 180);
  }
}
```

**Números canônicos:** gravidade **`0.95`**, impulso de pulo **`vy=13.5`**, squash
`scaleY(.82) scaleX(1.12)` por **180 ms**, **2** puffs no pouso. **O que cura:** pulo "de
elevador" sem impacto. O squash + a poeira + o baque grave dão peso à aterrissagem. **Detalhe
premium real:** o squash dispara **no instante do toque** (`MV.y<=0`), não numa parada horizontal
qualquer — impacto tem que coincidir com o contato. **Erro se remover:** o personagem "pousa" sem
que nada aconteça — o pulo perde o sentido.

## 3. Câmera com mola — mundo

```js
/* real: _pub_confeitaria/mundo/index.html */
var alvoCam = MV.pos - VW*0.42;        // enquadra o chef a 42% da largura da tela (adiantado, não colado)
if (alvoCam < 0) alvoCam = 0;
if (alvoCam > MV.W - VW) alvoCam = MV.W - VW;
MV.cam += (alvoCam - MV.cam) * 0.1;    // MOLA: a câmera persegue o alvo com lerp .1
```

**Números canônicos:** offset de enquadramento **`VW*0.42`**, lerp da câmera **`0.1`** (não 0.08).
**Importante — sem look-ahead direcional:** o alvo é **fixo** em `MV.pos - VW*0.42`; a sensação de
"olhar à frente" vem desse enquadramento a 42% (o personagem fica adiantado na tela), **não** de
um deslocamento de ~40px no sentido do movimento. Não invente look-ahead: o motor não tem.
**O que cura:** câmera colada e dura. Com a mola `.1`, ao mudar de direção a câmera **desliza**
para o novo enquadramento; parada, ela assenta sem oscilar. **Parallax** (mesmo tick): casas
`1`, colinas `.35`, nuvens `.12` (com deriva lenta `.14`).

## 4. Troca de pose e aceno idle — mundo

```js
/* real: _pub_confeitaria/mundo/index.html — escolha do sprite do chef */
var andando = Math.abs(MV.vx) > 0.7, img = $("mvChefImg"), ag = agoraMs();
if (!MV.noChao) img.src = IMG.mv.pulo;
else if (andando){
  if (ag - MV.tFrame > 135){                    // troca de pose a cada 135ms (velocidade eased ≈ constante)
    MV.frame = 1 - MV.frame; MV.tFrame = ag;
    img.src = (MV.frame ? IMG.mv.passoD : IMG.mv.passoE);
    mvBeep(150,120,.05,.05,"square");            // passo (glissando curto, grave)
    if (Math.random() < 0.3) mvPuff();           // poeirinha esporádica
  }
  $("mvChef").className = ""; MV.parou = ag;
} else {
  if (ag - MV.parou > 200 && img.src !== IMG.mv.acena) img.src = IMG.mv.parado;
  $("mvChef").className = "mvResp";               // respira parado
  if (ag - MV.parou > 4000 && ag - MV.acenou > 6000){   // ocioso ~4s: ACENA, e repete a cada ~6s
    MV.acenou = ag; img.src = IMG.mv.acena;
    setTimeout(function(){ if (Math.abs(MV.vx)<=0.7) $("mvChefImg").src=IMG.mv.parado; },1100);
  }
}
```

**Chaves de sprite reais:** `IMG.mv.parado`, `IMG.mv.passoD`, `IMG.mv.passoE`, `IMG.mv.pulo`,
`IMG.mv.acena` (o elemento é `#mvChefImg`). **O que cura:** personagem parado que parece morto.
O `.mvResp` respira; o aceno a cada ~4s/~6s quebra a hipnose — e demo parada é como o professor
apresenta o jogo. **Nota de timing:** aqui o swap é por **tempo** (135 ms) porque a velocidade é
eased e quase constante no cruzeiro; para movimento com aceleração forte, prefira o quadro por
**distância** do §7 (regra paga, Cap. 1 §12).

## 5. Respiração (breathing) — CSS puro

```css
/* real: _pub_confeitaria/mundo/index.html */
.mvResp img{-webkit-animation:mvResp 2.6s ease-in-out infinite;animation:mvResp 2.6s ease-in-out infinite;}
@-webkit-keyframes mvResp{0%,100%{-webkit-transform:scale(1)}50%{-webkit-transform:scale(1.025)}}
@keyframes mvResp{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
/* #mvChef usa transform-origin: 50% 100% (pés) — obrigatório */
```

**Números canônicos:** `scale(1)`↔`scale(1.025)` **uniforme**, **2.6s**, origem **nos pés**. A
variante refinada registrada (`MUNDO-VIVO-MOTOR.md` §8) é `scale(1.018, 1.05)` — scaleY ~5%,
scaleX levemente para cima. **O que cura:** estátua. **Erro clássico:** `transform-origin` no
centro → o personagem **levita** ("do centro parece zoom"); origem na base sempre.

## 6. Som com glissando (Web Audio, zero arquivo) — mundo × proto

O mundo e o proto têm **funções de som diferentes** — use a certa para cada motor.

```js
/* real: _pub_confeitaria/mundo/index.html — GLISSANDO (frequência varia f0->f1) */
function mvBeep(f0, f1, dur, vol, tipo){ try{ if(VOZ_MUDA) return;   // assinatura: vol ANTES de tipo
  _ac = _ac || new (window.AudioContext||window.webkitAudioContext)();
  if (_ac.state==="suspended" && _ac.resume) _ac.resume();
  var o=_ac.createOscillator(), g=_ac.createGain();
  o.type = tipo||"sine";
  o.frequency.setValueAtTime(f0, _ac.currentTime);
  o.frequency.exponentialRampToValueAtTime(Math.max(1,f1), _ac.currentTime+dur);  // ← o glissando
  g.gain.setValueAtTime(vol, _ac.currentTime);
  g.gain.exponentialRampToValueAtTime(.001, _ac.currentTime+dur+.02);
  o.connect(g); g.connect(_ac.destination); o.start(); o.stop(_ac.currentTime+dur+.05);
}catch(e){} }
```

```js
/* real: _pub_confeitaria/proto/index.html — UMA frequência fixa (sem glissando) */
function plimP(f){ _acP = _acP || new (window.AudioContext||window.webkitAudioContext)();
  if(_acP.state==="suspended"&&_acP.resume)_acP.resume();
  var o=_acP.createOscillator(), g=_acP.createGain();
  o.type="sine"; o.frequency.value = f || 740;    // frequência única, sem ramp
  g.gain.setValueAtTime(.12, _acP.currentTime);
  g.gain.exponentialRampToValueAtTime(.001, _acP.currentTime+.18);
  o.connect(g); g.connect(_acP.destination); o.start(); o.stop(_acP.currentTime+.2);
}
```

**Kit canônico de sons do mundo** (`MUNDO-VIVO-ESPINHA.md` §3), tudo com `mvBeep`:
- passo: `mvBeep(150,120,.05,.05,"square")` — grave, descendente, curtíssimo;
- pulo: `mvBeep(330,660,.18,.1,"sine")` — sobe (impulso);
- pouso: `mvBeep(110,70,.12,.12,"sine")` — desce (baque de peso).

**O que cura:** o "bip de relógio" — o glissando (`exponentialRampToValueAtTime`) tira a cara de
despertador. **Destravamento:** o navegador só libera áudio após um gesto — registre
`keydown`/`mousedown`/`touchstart` chamando `resume()` (o `plimP`/`mvBeep` já fazem `resume()` na
chamada). Até o 1º gesto, roda **mudo sem travar**.

## 7. Movimento top-down: 8 direções, colisão por sub-passo — proto

```js
/* real: _pub_confeitaria/proto/index.html — chef top-down (loop rAF, fallback setTimeout 33ms) */
var sp = 3.1, ax = 0, ay = 0;                    // velocidade CONSTANTE (top-down não usa easing linear)
if(chef.mov.esq)ax=-1; if(chef.mov.dir)ax=1; if(chef.mov.cima)ay=-1; if(chef.mov.baixo)ay=1;
if(ax&&ay){ ax*=0.707; ay*=0.707; }              // diagonal normalizada (senão a diagonal é mais rápida)
var nx = chef.x+ax*sp, ny = chef.y+ay*sp;
/* colisão por sub-passo: tenta o passo inteiro, depois metade, depois 1px — nunca gruda na parede */
var stepx = nx-chef.x, stepy = ny-chef.y;
if(stepx!==0){ if(tenta(chef.x+stepx,chef.y)) chef.x+=stepx;
  else if(tenta(chef.x+stepx/2,chef.y)) chef.x+=stepx/2;
  else if(tenta(chef.x+(stepx>0?1:-1),chef.y)) chef.x+=(stepx>0?1:-1); }
if(stepy!==0){ if(tenta(chef.x,chef.y+stepy)) chef.y+=stepy;
  else if(tenta(chef.x,chef.y+stepy/2)) chef.y+=stepy/2;
  else if(tenta(chef.x,chef.y+(stepy>0?1:-1))) chef.y+=(stepy>0?1:-1); }
```

**Números canônicos:** velocidade **`3.1`**, diagonal `×0.707`. **O que cura:** personagem que
gruda na parede (sub-passo desliza rente) e diagonal veloz demais (normalização `.707`).
**Nota:** ao contrário do mundo lateral, o proto **não suaviza a velocidade linear** — a rigidez é
escondida pelo quadro-por-distância + bob + lean dos §8/§9.

## 8. Quadro por DISTÂNCIA — proto (a regra paga anti-patinar)

```js
/* real: _pub_confeitaria/proto/index.html */
var passo = Math.sqrt((chef.x-chef.lx)*(chef.x-chef.lx)+(chef.y-chef.ly)*(chef.y-chef.ly));
chef.dTot = (chef.dTot||0) + passo;              // distância acumulada
chef.lx = chef.x; chef.ly = chef.y;
chef.frame4 = Math.floor(chef.dTot/13)%4;        // ciclo de 4 poses: 1 quadro a cada 13px
chef.frame  = Math.floor(chef.dTot/24)%2;        // ciclo de 2 poses: 1 quadro a cada 24px
```

**O que cura:** o **moonwalk** (pé patinando) na aceleração. Como o quadro é função da distância
andada — não do relógio — os quadros aceleram e param **junto** com o personagem. Regra
registrada: *"Passo por DISTÂNCIA, não por tempo: trocar o quadro a cada ~34px percorridos (senão
o pé patina na aceleração)"* (`MUNDO-VIVO-MOTOR.md` §8). **Erro se usar tempo:** o pé escorrega
sempre que a velocidade muda.

## 9. Profundidade falsa, bob e lean — proto

```js
/* real: _pub_confeitaria/proto/index.html */
function esc(y){ return 0.86 + (y/900)*0.34; }   // escala por profundidade: 0.86 (fundo) -> 1.20 (frente)
// bob senoidal (|sin|), amplitude 3.2px, suavizado 0.3:
chef.bob  += ((and?Math.abs(Math.sin(chef.dAc0=(chef.dAc0||0)+vtot*sp*0.19)):0)*3.2 - (chef.bob||0))*0.3;
// inclinação no sentido horizontal, ±2.6°, suavizada 0.15:
chef.lean += ((and?(ax*2.6):0) - (chef.lean||0))*0.15;
var s = esc(chef.y).toFixed(3);
var tf = (chef.dir==="le"?"scaleX(-1) ":"")      // esquerda = espelho do lado
       + "scale("+s+") translateY("+(-(chef.bob||0)).toFixed(1)+"px) rotate("+(chef.lean||0).toFixed(1)+"deg)";
$("chef").style.webkitTransform = tf; $("chef").style.transform = tf;
$("chef").style.zIndex = Math.round(chef.y);     // ORDEM DE DESENHO por Y (painter's algorithm)
```

**Números canônicos:** escala `0.86 + (y/900)*0.34`, bob `|sin|×3.2` eased `0.3`, lean `±2.6°`
eased `0.15`, ordenação `zIndex = round(y)`. **O que cura:** (1) `esc(y)` dá a ilusão de
profundidade — quem está "mais na frente" (y maior) é maior; (2) o bob dá o quique do andar; (3) o
lean inclina o corpo pro lado do movimento; (4) o `zIndex` por Y garante que quem está atrás da
mesa é **ocluído** por ela (nada transpassa móvel). **Erro se remover o zIndex por Y:** personagem
"dentro" do balcão ou por cima da mesa — destrói a cena.

## 10. Sombra de contato (dark, reativa) — os dois motores

Atenção à regra de banimento (Cap. 4): o proibido é **sombra circular BRANCA/CLARA**. Os motores
usam uma sombra **escura e sutil** que reage ao pulo — e isso é premium, não banido:

```js
/* mundo: a sombra encolhe conforme o chef sobe no pulo */
var s = 1 - Math.min(.55, MV.y/240);   // quanto mais alto, menor a sombra
/* CSS: #mvSombra{background:rgba(40,25,10,.28);border-radius:50%} — marrom translúcida */

/* proto: a sombra acompanha a escala e o bob */
var ss = (esc(chef.y)*(1-(chef.bob||0)*0.04)).toFixed(3);
```

**O que cura:** peso no chão sem elipse branca (banida). Sombra escura translúcida que **encolhe
quando o personagem pula** vende a altura; sombra branca/clara fixa é o que o professor recusa.

## 11. Ondas de NPCs com guarda de estado — proto

```js
/* real: _pub_confeitaria/proto/index.html — próxima onda só quando a loja esvazia */
if(!fim && clientes.length===0 && aSpawnar===0 && !atendendo){
  if(onda<ONDAS.length){ var n=ONDAS[onda]; onda++; aSpawnar=n;
    for(var w=0;w<n;w++) setTimeout(function(){ novoCliente(); aSpawnar--; }, w*1200); }  // entra em cascata
  else { fim=true; festaFim(); }
}
```

**Números canônicos:** `var ONDAS=[1,2,2,1]`, spawn em cascata a cada **1200 ms**. **O que cura:**
**onda dupla**. A tripla-guarda `clientes.length===0 && aSpawnar===0 && !atendendo` impede a
próxima onda de nascer antes da atual terminar. **Erro se remover a guarda:** clientes dobram na
tela (o fantasma "onda dupla" do Cap. 5).

---

<a name="capitulo-4"></a>
# Capítulo 4 — PREMIUM: o checklist do "parece caro"

## 4.0 O princípio (por que Monkey Mart parece vivo)

O que separa um joguinho escolar de um jogo do Poki não é gráfico nem engine — é **"juice"**: a
camada de resposta sensorial em cima de uma mecânica que já funciona. A literatura de game feel
converge em poucas leis, e todas cabem nas nossas restrições (ES5, DIVs, sem WebGL):

1. **Toda ação do jogador recebe resposta em ≤100ms** — visual E sonora. Nunca só uma.
2. **Nada se move em velocidade constante** (linear = robô). Tudo acelera e desacelera (easing).
3. **Nada aparece ou some instantaneamente.** Tudo entra com pop e sai com fade/queda.
4. **Corpos têm massa:** squash no impacto, stretch no arranque, inclinação na direção do
   movimento.
5. **Personagens parados não estão parados** — respiram, piscam, olham em volta.
6. **A recompensa tem ritmo:** acerto pequeno = festa pequena; conquista grande = festa em
   camadas (som → pop → partículas → voz), nunca tudo no mesmo milissegundo.

Monkey Mart aplica isso, e nosso motor também: o chef **agacha no pouso** (`.mvSquash`), levanta
**poeira** (`mvPuff`), a moeda **voa em arco** até o contador (`mvVoaMoeda`), o cliente mostra um
**balãozinho** com o que quer. Nenhum efeito exige WebGL — todos são `transform`/`opacity` + Web
Audio, o nosso terreno.

**Regra de banimento vigente:** NADA de **sombra circular BRANCA/CLARA** sob os personagens
(banida pelo professor). Atenção: isso **não** proíbe sombra — os motores usam uma sombra
**escura, translúcida e reativa** (`#mvSombra` = `rgba(40,25,10,.28)`, que encolhe no pulo; e a
`shChef` do proto que acompanha a escala). Peso no chão se resolve com sombra escura discreta +
pose (pés plantados, squash no pouso) — nunca com elipse branca/clara.

Este capítulo está calibrado com os **valores reais** dos dois motores
(`_pub_confeitaria/mundo/index.html` e `.../proto/index.html`). O protagonista dos dois é **o
chef confeiteiro** (objeto `IMG.mv` com `parado/passoD/passoE/pulo/acena`, elemento `#mvChefImg`,
cena `.mmChefCena`) — **não** existe "raposa" nestes motores.

---

## 4.1 CHECKLIST AUDITÁVEL

Formato: **o que é → como saber se passou (teste objetivo) → custo → prioridade** para o **proto**
(confeitaria top-down: chef 4 direções, clientes em ondas, arrastar doces) e para o **mundo**
(lateral: chef andando com física, clima, câmera).

### BLOCO A — Micro-feedback de interação (a base de tudo)

**A1. Hover/toque em item pegável: cresce e "acorda".** Sobe para `scale(1.08)` com
`transition: transform .12s ease-out` + `drop-shadow` colorido (nunca `box-shadow` — desenha
quadrado no PNG). *Passou se:* 5 itens reagem em <150ms e voltam suave. **Custo: baixo. Proto:
ALTA. Mundo: média.**

**A2. Pegar: pop de confirmação + som.** No `mousedown`/`touchstart`: o ghost nasce em `scale(.9)`
e vai a `scale(1.05)` em ~100ms, o original fica com opacidade ~0.35, toca "plic" (`plimP`).
**Guarda paga:** clique-vs-arrasto exige guarda de **280ms** (`MM.tDrop`:
`if(mmAgora()-MM.tDrop<280)return;`), senão o toque vira arrasto acidental. *Passou se:* ≤2 frames
entre toque e resposta. **Custo: baixo. Proto: ALTA. Mundo: média.**

**A3. Soltar certo: o item ASSENTA (não teleporta).** Anima até o encaixe em ~150ms com ease-out +
mini-squash + som (pitch sobe). *Passou se:* em câmera lenta, nenhum frame mostra o item "trocando
de lugar" sem trajeto. **Custo: baixo/médio. Proto: ALTA. Mundo: baixa.**

**A4. Soltar errado: volta com elástico, sem punição.** Alvo inválido → volta voando à origem em
~250ms. Nunca some, nunca teleporta. *Passou se:* 5 erros seguidos sempre voltam animados.
**Custo: baixo. Proto: ALTA. Mundo: baixa.**

**A5. Botões afundam.** Sombra 3D inferior (`box-shadow 0 4px 0 <cor escura>`) + `:active` que
afunda 2px. *Passou se:* 100% dos clicáveis têm `:active` (inclusive setas). **Custo: baixo.
Ambos: ALTA.**

### BLOCO B — Personagem com massa e vida

**B1. Quadro de VIRADA de direção.** 1 quadro intermediário (¾ ou o parado da nova direção) por
~60-80ms antes do ciclo. No proto já existe (`chef_cima`/`chef_lado` de 4 quadros; esquerda =
espelho do lado, `scaleX(-1)`). No mundo, virar = espelhar (`MV.dir<0 ? scaleX(-1)`); inserir 1
quadro de compressão `scaleX(~.1)` no meio do flip disfarça. *Passou se:* a troca lê como giro,
não como troca de figura. **Custo: médio. Ambos: ALTA.**

**B2. Arranque e freada (o easing real do mundo).** Velocidade **eased**:
`MV.vx += (alvo - MV.vx) * 0.16` (`alvo = MV.held*5.4`) — fator **0.16**, testado
(`MUNDO-VIVO-ESPINHA.md` §3), **não 0.18**. O squash do motor é de **pouso** (`.mvSquash =
scaleY(.82) scaleX(1.12)`, quando `MV.y<=0`), não um `scale(1.04,.96)` genérico de parada. *Passou
se:* ao soltar a tecla, o chef desliza 2-4 frames. **Nota:** eased-velocity é o **mundo**; o
**proto** anda a velocidade constante `3.1` e esconde a rigidez com quadro-por-distância + bob/lean
(Cap. 3 §7-§9). **Custo: baixo. Ambos: ALTA.**

**B3. Idle vivo: respirar + piscar + olhar.** Parado: `.mvResp` = `scale(1)`→`scale(1.025)`
**uniforme**, **2.6s**, `ease-in-out`, origem nos pés (**não** `scaleY 1→1.02` nem 2.4s); variante
refinada `scale(1.018,1.05)`. Piscada a cada 3-5s aleatório; o motor acena após **~4s** parado,
repetindo a cada **~6s** (`IMG.mv.acena`). *Passou se:* 20s parado gera ≥3 eventos e nenhum trecho
de 5s imóvel; tempos NÃO fixos. **Custo: baixo/médio. Proto: média. Mundo: ALTA.**

**B4. Pose de CARREGAR item.** Pose própria + **item balança com atraso** (follow-through): DIV
filho com `transition: transform .15s ease-out`, deslocado 2-3px contra o movimento. *Passou se:*
a pose difere da de mãos vazias; o item inclina contra o movimento. **Custo: médio/baixo. Proto:
ALTA. Mundo: baixa.**

**B5. Inclinação no movimento (lean).** Corpo inclina no sentido do deslocamento, proporcional à
velocidade. É o `chef.lean` do proto: `lean += (ax*2.6 - lean)*0.15` (±2.6°, suavizado). *Passou
se:* em velocidade máxima a inclinação é perceptível mas não caricata (>1°, <6°). **Custo: baixo.
Proto: ALTA. Mundo: média.**

### BLOCO C — Transições de tela e entrada/saída

**C1. Nenhuma troca de tela é corte seco.** Sai com fade+descida (250ms ease-in), a nova entra com
fade+subida (300ms ease-out, atraso 100ms). *Passou se:* zero trocas instantâneas; nenhuma passa
de 450ms. **Custo: baixo. Ambos: ALTA.**

**C2. Listas entram em CASCATA (stagger).** Cards/clientes um a um com 60-90ms entre eles (pop
`scale(.6)→1` com overshoot). No proto a onda já nasce em cascata (`setTimeout(...w*1200)`).
*Passou se:* os itens NÃO nascem no mesmo frame. **Custo: baixo. Proto: ALTA. Mundo: média.**

**C3. Easing nunca linear.** 3 curvas: `ease-out` (entra/reage), `ease-in` (sai),
`cubic-bezier(.34,1.56,.64,1)` (overshoot de recompensa). Proibido `linear` exceto rotação
contínua. *Passou se:* grep por `linear` só acha rotações. **Custo: baixo. Ambos: ALTA.**

### BLOCO D — Partículas baratas (DIVs, zero canvas)

**D1. Sistema único de partícula-DIV reutilizável.** Função ES5 cria DIV absoluto, força reflow,
aplica `transform` + `opacity:0` com `transition` 500-800ms ease-out, e `setTimeout` remove o nó.
Pool máx. ~24 nós vivos. O `mvPuff()` do motor é o molde (`.mvPuff`, remove em 520ms).
*Passou se:* 50 acertos não passam de 24 DIVs no DOM. **Custo: baixo. Ambos: ALTA** (fundação de
D2-D4).

**D2. Poeirinha de passo/pouso.** A cada N passos (ou no pouso), 1-2 partículas nos pés somem em
~400-520ms. É o `mvPuff` real: **2** puffs no pouso, 1 esporádico (`Math.random()<.3`) ao andar.
NADA de elipse branca fixa. *Passou se:* aparecem poeirinhas e nenhuma persiste >1s. **Custo:
baixo. Proto: média. Mundo: ALTA.**

**D3. Explosão de acerto contextual.** Doce certo → 5-8 partículas do TEMA (⭐✨ + mini-PNG)
explodem DO PONTO da entrega em arco. *Passou se:* o centro é o local da ação; tamanhos/ângulos
variados. **Custo: baixo. Proto: ALTA. Mundo: média.**

**D4. Recompensa que VOA até o placar.** DIV nasce no local do acerto e voa ao contador em ~600ms
(via `transform translate` com bezier — nunca `left/top`); o contador dá um `scale(1.25→1)` + som
QUANDO a estrela chega. É o `mvVoaMoeda()` do motor. *Passou se:* o pulo do placar coincide com a
chegada (±100ms). **Custo: médio. Proto: ALTA. Mundo: média.** O truque que mais grita "Monkey
Mart".

### BLOCO E — NPCs que parecem gente

**E1. Balãozinho de emoção/pedido.** Balão-DIV com o PNG do doce desejado, nascendo com pop +
flutuação. Estados: pedido (item), feliz (✨), impaciente (balão treme). No proto é `.balaocli`
(`chama` longe, pedido perto). **Guarda paga:** o balão do mundo só reatualiza com `MV.perto=-2` ao
voltar. *Passou se:* dá para saber SEM texto o que cada cliente quer. **Custo: baixo/médio. Ambos:
ALTA.**

**E2. NPC reage no corpo, não só no balão.** Acertou: pulinho (com squash no pouso) + pose feliz
por ~1s. *Passou se:* a entrega mostra ≥2 respostas simultâneas (corpo + balão + som). **Custo:
baixo/médio. Proto: ALTA. Mundo: média.**

**E3. Dessincronizar a multidão.** Cada NPC com fase DIFERENTE (`animation-delay` aleatório; nunca
dois balões pulsando juntos). *Passou se:* print de 4+ NPCs sem dupla no mesmo frame. **Custo:
baixo. Ambos: ALTA.**

### BLOCO F — Som que acompanha o gesto (Web Audio, zero arquivo)

**F1. Use as funções REAIS do motor (não crie uma nova).** Mundo: `mvBeep(f0, f1, dur, vol, tipo)`
com **glissando** via `frequency.exponentialRampToValueAtTime` (ordem: `vol` antes de `tipo`).
Proto: `plimP(f)` — sine de UMA frequência fixa, sem glissando. Kit canônico do mundo
(`MUNDO-VIVO-ESPINHA.md` §3): passo `mvBeep(150,120,.05,.05,"square")`; pulo
`mvBeep(330,660,.18,.1,"sine")`; pouso `mvBeep(110,70,.12,.12,"sine")`. *Passou se:* cada
interação tem som distinto (teste cego); nenhum passa de 200ms. **Custo: baixo. Ambos: ALTA.**

**F2. Variação de pitch anti-metralhadora.** Som repetitivo com pitch ±6% aleatório; em série de
acertos, sobe um semitom por acerto (zera no erro). *Passou se:* 5 coletas soam como escadinha; 10
passos nunca idênticos. **Custo: baixo. Proto: ALTA. Mundo: média.**

**F3. Destravamento honesto do áudio.** `AudioContext`/`resume()` no 1º gesto
(keydown/mousedown/touchstart) — regra do navegador, não é defeito. Até lá, mudo sem travar.
*Passou se:* carregar sem clicar = zero erros no console. **Custo: baixo. Ambos: ALTA.**

### BLOCO G — Câmera, cenário e ritmo de recompensa

**G1. Câmera com mola (mundo).** `MV.cam += (alvoCam - MV.cam) * 0.1`, com
`alvoCam = MV.pos - VW*0.42` (chef a 42% da largura — adiantado, não colado). Fator **0.1** (não
0.08), **sem** look-ahead direcional de ~40px: o adiantamento vem do offset fixo `VW*0.42`, não da
direção do movimento. *Passou se:* ao virar desliza suave; parado assenta sem oscilar. **Custo:
baixo. Mundo: ALTA.**

**G2. Impacto sem screen-shake: o "nudge".** Em acerto grande, o container dá `scale(1.01)` por
90ms (ou 2px). Screen-shake de verdade é agressivo para crianças e caro em repaint. *Passou se:*
perceptível mas invisível como "tremor". **Custo: baixo. Ambos: média.**

**G3. Ritmo de recompensa em 3 degraus.** Acerto comum = som + pop + 5 partículas (~0,8s); fim de
onda = + estrela voando + pulo do placar + fala (~2s); conquista/final = CAMADAS sequenciais (som
→ carimbo → confete em ondas → voz), 4-6s. O degrau máximo NUNCA é gasto em acerto comum. *Passou
se:* acerto comum não dispara confete de tela cheia. **Custo: baixo. Ambos: ALTA.**

**G4. Cenário com 2 camadas de vida.** 2+ elementos ambientais dessincronizados. O mundo já tem
clima vivo: dia (70s)/noite (45s) + tempo aleatório (limpo/chuva/neve/trovoada), estrelas, lua,
luzes (`.mvLuz`), nuvens em parallax — tudo `transform`/`opacity`. *Passou se:* 10s de tela parada
= ≥2 coisas se moveram além do personagem. **Custo: médio. Proto: média. Mundo: ALTA.**

**G5. Compatibilidade do juice inteiro.** Só `transform`/`opacity` (zero `left/top/width`), par
`-webkit-` em 100% dos keyframes/transitions, degradação limpa, zero `let/const/arrow`. *Passou
se:* `@keyframes` == `@-webkit-keyframes`; jogável com animações desligadas à força. **Custo:
baixo. Ambos: ALTA — bloqueante.**

---

## 4.2 OS 10 UPGRADES DE MAIOR IMPACTO (ordenados)

Critério: impacto percebido ÷ custo nas nossas restrições.

1. **F1+F3 — Sons reais (`mvBeep` glissando / `plimP`) + destravamento** (ambos). Maior salto de
   percepção por linha de código.
2. **B2 — Easing `0.16` + squash de pouso `.mvSquash`** (mundo). Mata a rigidez de "boneco em
   trilho" — a diferença nº 1 entre amador e Poki.
3. **A2/A3/A4 — Ciclo pegar→soltar com pop, assentamento e volta elástica** (proto), com a guarda
   `MM.tDrop` de 280ms.
4. **D4 — Estrela/moeda voando até o placar com pulo sincronizado** (proto): `mvVoaMoeda` por um
   `getBoundingClientRect` + uma transition.
5. **C1+C3 — Transições de tela com fade/deslize e banimento do linear** (ambos). Revisão barata
   que eleva TODAS as telas.
6. **E1+E3 — Balões de pedido + dessincronizar a multidão** (proto), com `MV.perto=-2` no mundo.
7. **B1 — Quadro de virada de direção** (ambos). Remove o "estalo" que nenhum outro efeito disfarça.
8. **B3 — Idle vivo (respiração `.mvResp` + aceno ~4s/~6s + piscar aleatório)** (mundo primeiro).
9. **D1+D2 — Pool de partículas + poeira (`mvPuff`) no passo/pouso** (ambos).
10. **G3 — Ritmo de recompensa em 3 degraus** (ambos). Zero tecnologia; impede o carnaval constante.

Regra de fechamento: **gravar 30 segundos e assistir em câmera lenta** (Cap. 5). Se algo
teleportou, estalou, entrou/saiu num frame só, se moveu em reta constante ou em silêncio —
reprovou, volta para a bancada.

*Fontes: [Game feel on the web (Valdemird)](https://valdemird.com/blog/game-feel-on-the-web/);
[Squeezing more juice (Game Developer)](https://www.gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design-);
valores canônicos = código de `_pub_confeitaria/mundo|proto/index.html`, `MUNDO-VIVO-ESPINHA.md` §3/§6.*

---

<a name="capitulo-5"></a>
# Capítulo 5 — QA de Movimento: o ritual que impede o "no meu teste funcionava"

## Por que este capítulo existe

Um print único não prova nada sobre movimento. Piscar, pulo de escala, cliente preso e onda dupla
só aparecem comparando o jogo **consigo mesmo ao longo do tempo** — e um **teste com bug** pode
condenar um jogo que está certo. Duas partes: **(1) o QA canônico** (Playwright — comportamento,
o gate oficial) e **(2) a rajada de screenshots** (visual — sprite, os defeitos entre quadros).
Ambas terminam com a mesma disciplina: **veredito de bug só com log que o prove.**

Pré-requisitos (verificados neste ambiente):
- Chromium headless: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (Chromium 141)
- `node` (para `node --check`) e `python3` com Pillow 12.2 (para comparar quadros)
- O HTML do jogo é 1 arquivo autossuficiente — dá para testar com `file://`, sem servidor.

Convenção usada nos comandos:

```bash
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
QA=/tmp/qa-movimento
JOGO=/home/user/floresta-dos-numeros-1ano/_pub_confeitaria/proto/index.html
mkdir -p "$QA"
```

---

## PARTE 1 — O QA CANÔNICO DO PROJETO (roteiro Playwright, comportamento)

Este é o gate **oficial**, documentado em `MUNDO-VIVO-MOTOR.md` §5 e `MUNDO-VIVO-ESPINHA.md` §5.
O roteiro Playwright pronto é o `mm_test.js` (vive no scratchpad; recriar se sumir). Para CADA
tipo de desafio:

1. **Abrir a cena:** `abrirParada(i)` + `rodarFase()` (no proto, o fluxo equivalente passa por
   `abrirPedido`, `conferir`, `festaFim`, `clienteSai`; o mundo entra por `comecar()` e
   `renderDesafio(d)`).
2. **ERRAR de propósito** (repartição desigual / proposta baixa) → esperar a **consequência
   visível** e `_errouNeste=true`, **SEM** plaquinha de matemática.
3. **Consertar** → aí sim a plaquinha (`.mmPlaquinha`, ex. `20 ÷ 4 = 5`) + festa + botão Próximo.
4. **Zero `pageerror`** durante tudo.
5. **Testar retrato 390×780 E paisagem** — as duas orientações, sempre.

Regra de edição obrigatória (o arquivo tem ~3 MB): **`node --check` no JS extraído após CADA
edição**; editar **por âncora única** com Python `sub1`, **nunca regex gulosa** (base64 quebra
linha-a-linha e uma busca-e-troca ampla corrompe o arquivo — barreira registrada em
`MUNDO-VIVO-ESPINHA.md` §6).

**Lições pagas que o QA canônico já cravou** (são estas, e não episódios inventados):
- **Clique engolido pelo arrasto** → guarda de **280ms** (`MM.tDrop`:
  `if(mmAgora()-MM.tDrop<280)return;`). Um teste ingênuo que dispara toque e arrasto juntos
  reproduz o falso "o segundo clique não funciona" — o jogo está **certo**, é a guarda agindo.
- **Balão de fala desatualizado ao voltar ao NPC** → `MV.perto=-2` força a reatualização.
- **Fala velha invadindo a cena nova** → `_encadear=false; pararFala()` na troca de desafio.
- **Onda dupla** → a guarda de estado `clientes.length===0 && aSpawnar===0 && !atendendo` antes de
  spawnar a próxima onda (Cap. 3 §11).
- **Objeto vazando da bandeja** → padding `20/58/46` + doce 32px quando lote ≥18, sempre conferido
  com screenshot das cenas extremas (30 itens, 7 grupos).

---

## PARTE 2 — A RAJADA VISUAL (complementar: caçar piscar e pulo de escala)

O roteiro Playwright prova **comportamento**; não prova que o **sprite** não pisca nem pula de
escala entre poses. Esta camada complementar usa screenshots headless espaçados no tempo +
comparação com Pillow (técnica de bancada, não o gate oficial — mas casa com a cura de corte do
Cap. 2: piscar/pulo de escala vêm de recorte fora do canvas comum).

### Passo 0 — `node --check` em TODO script extraído (antes de qualquer render)

Não faz sentido caçar bug de movimento num arquivo com erro de sintaxe. Extraia os `<script>` e
valide:

```bash
python3 - "$JOGO" "$QA/jogo.js" <<'PY'
import re, sys
html = open(sys.argv[1], encoding="utf-8").read()
blocos = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
open(sys.argv[2], "w", encoding="utf-8").write("\n;\n".join(b for b in blocos if b.strip()))
print(len(blocos), "bloco(s) extraído(s)")
PY
node --check "$QA/jogo.js" && echo "SINTAXE: OK"
```

Se falhar aqui, **pare** e conserte a sintaxe primeiro. **Regra permanente:** rode `node --check`
de novo **toda** vez que editar o HTML (inclusive ao injetar os scripts de teste dos passos
seguintes). Script de teste com erro de sintaxe derruba o jogo inteiro e produz um falso "está
quebrado". E lembre da barreira do §5: no arquivo de 3 MB, **edite por âncora única** (Python
`sub1`), nunca por regex gulosa.

### Passo 1 — Render headless básico (o print de sanidade)

```bash
"$CHROME" --headless --no-sandbox --disable-gpu \
  --window-size=1280,720 --virtual-time-budget=4500 \
  --screenshot="$QA/sanidade.png" "file://$JOGO"
```

Duas regras aprendidas na dor: **(1) `--virtual-time-budget` ≥ 4500** — as telas têm fade de
entrada (`aparece .4s`) e spawn com `setTimeout`; budget curto captura no meio da animação e você
"diagnostica" um defeito que não existe (alinhado ao ≥4000 do `CLAUDE.md`). **(2)** o erro
`Failed to call method: org.freedesktop.DBus...` no stderr é ruído inofensivo (ambiente sem
D-Bus) — o que confirma sucesso é `N bytes written to file`. Este print confirma que a cena
aparece; **ele não valida movimento.**

### Passo 2 — RAJADA DE QUADROS: 6–10 screenshots espaçados ~150 ms

Piscar e pulo de escala são defeitos **entre** quadros. No headless cada execução tira 1 foto —
então a rajada varia o `--virtual-time-budget` em degraus de ~150 ms de tempo virtual. Como os
timers são determinísticos sob virtual time, cada run cai num instante diferente **da mesma cena**:

```bash
for T in 4500 4650 4800 4950 5100 5250 5400 5550; do
  "$CHROME" --headless --no-sandbox --disable-gpu \
    --window-size=1280,720 --virtual-time-budget=$T \
    --screenshot="$QA/quadro_$T.png" "file://$JOGO" 2>/dev/null
done
ls -la "$QA"/quadro_*.png
```

Escolha a janela de tempo de forma que o personagem esteja **andando** nesses instantes (se
preciso, injete um auto-start — Passo 3). Agora compare os quadros — dimensão e posição do sprite:

```bash
python3 - "$QA" <<'PY'
import sys, glob
from PIL import Image, ImageChops
arqs = sorted(glob.glob(sys.argv[1] + "/quadro_*.png"))
base = None
for a in arqs:
    im = Image.open(a).convert("RGB")
    if base is None:
        base = im; print(a, "(base)", im.size); continue
    diff = ImageChops.difference(base, im)
    print(a, "tamanho:", im.size, "| bbox da mudança:", diff.getbbox())
    base = im
PY
```

Como ler:
- **bbox `None` entre TODOS os quadros durante o andar** = jogo congelado (ou a janela pegou um
  momento parado — confira antes de gritar "bug").
- **bbox que "explode" num quadro e volta no seguinte** = sprite piscou (sumiu 1 frame) ou pulou de
  escala. É exatamente o defeito que o **canvas comum** (`normaliza_set` do Cap. 2) cura: poses do
  mesmo conjunto em canvases de tamanhos diferentes fazem o sprite redimensionar a cada troca.
- **bbox que anda suavemente** (desloca ~mesma quantidade por quadro) = movimento saudável.

Para inspeção humana, monte uma tira e **mande ao professor** (ferramenta de envio de arquivo):

```bash
python3 - "$QA" <<'PY'
import sys, glob
from PIL import Image
arqs = sorted(glob.glob(sys.argv[1] + "/quadro_*.png"))
ims = [Image.open(a) for a in arqs]
w, h = ims[0].size
tira = Image.new("RGB", (w*len(ims), h), "white")
for i, im in enumerate(ims): tira.paste(im, (i*w, 0))
tira.save(sys.argv[1] + "/tira_rajada.png", optimize=True)
print("tira em", sys.argv[1] + "/tira_rajada.png")
PY
```

Olho humano na tira pega em 5 segundos o que passa batido em números: um quadro onde o chef está
sem cabeça, espelhado errado, ou 20% maior.

### Passo 3 — Despejo de estado: a máquina de estados por escrito

Screenshot mostra pixels; não mostra **por que** o cliente está parado há 8 segundos. Injeta-se um
script de polling que despeja posição/estado/frame num `<div>` escondido, e lê-se com
`--dump-dom`. **Use os nomes REAIS das variáveis do proto** (`chef`, `clientes` com `.estado`/`.x`/
`.y`, `onda`, `aSpawnar`, `atendendo`) — não invente `painelAberto`/`servir`, que não existem.

Crie uma **cópia** do HTML com o script injetado antes de `</body>` (nunca teste no original):

```bash
python3 - "$JOGO" "$QA/jogo_qa.html" <<'PY'
import sys
html = open(sys.argv[1], encoding="utf-8").read()
sonda = """
<script>
(function(){
  var log=[];
  window.addEventListener("load",function(){
    setTimeout(function(){ try{ if(typeof comecar==="function") comecar(); }catch(e){ log.push("ERRO start: "+e.message); } },80);
  });
  setInterval(function(){
    try{
      var s = "t=" + Math.round(performance.now());
      if (typeof chef !== "undefined")
        s += " | chef x=" + Math.round(chef.x) + " y=" + Math.round(chef.y) + " dir=" + chef.dir;
      if (typeof clientes !== "undefined")
        s += " | clientes=" + clientes.length + " [" +
          clientes.map(function(c){return c.estado+"@"+Math.round(c.x)+","+Math.round(c.y);}).join(" ") + "]";
      if (typeof onda !== "undefined") s += " | onda=" + onda + " aSpawnar=" + aSpawnar + " atendendo=" + (!!atendendo);
      log.push(s);
    }catch(e){ log.push("ERRO sonda: "+e.message); }
    var d = document.getElementById("qa-dump");
    if(!d){ d=document.createElement("div"); d.id="qa-dump"; d.style.display="none"; document.body.appendChild(d); }
    d.textContent = log.join("\\n");
  }, 250);
})();
</script>
"""
open(sys.argv[2], "w", encoding="utf-8").write(html.replace("</body>", sonda + "</body>"))
print("injetado")
PY

# valida o HTML injetado (Passo 0 de novo — obrigatório):
python3 -c "
import re
h=open('$QA/jogo_qa.html',encoding='utf-8').read()
open('$QA/jogo_qa.js','w',encoding='utf-8').write('\n;\n'.join(re.findall(r'<script[^>]*>(.*?)</script>',h,re.S)))
"
node --check "$QA/jogo_qa.js" && echo "SONDA: sintaxe OK"

# roda tempo suficiente para ver a máquina girar e despeja o DOM:
"$CHROME" --headless --no-sandbox --disable-gpu \
  --virtual-time-budget=20000 \
  --dump-dom "file://$QA/jogo_qa.html" 2>/dev/null > "$QA/dom.html"

python3 - "$QA/dom.html" <<'PY'
import sys, re
dom = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'id="qa-dump"[^>]*>(.*?)</div>', dom, re.S)
print(m.group(1)[-6000:] if m else "SONDA NAO ENCONTRADA — o jogo quebrou antes do polling?")
PY
```

Os três fantasmas clássicos do motor top-down, no log:
1. **Cliente preso:** `estado` que não muda e `x,y` que não anda por vários ticks, sem estar em
   `esperando`/`sentado` legítimo. O log diz **em qual estado** ele travou.
2. **Onda dupla:** `onda` incrementando duas vezes, ou `clientes.length` saltando para o dobro. A
   guarda do §11 (`aSpawnar===0`) deveria impedir — o log data a duplicação.
3. **Cliente que some/reaparece:** `estado` indo `saindo → esperando` sem novo spawn.

Descubra os nomes reais com `Grep` (`var chef`, `estado`, `var ONDAS`, `atendendo`); **nunca leia
o arquivo de 3 MB inteiro**.

### Passo 4 — Antes de decretar "está quebrado": instrumente o JOGO, não confie no teste

Regra de ouro: **o teste também é código, e código de teste também tem bug.** Antes de concluir
defeito, **envelope as funções REAIS suspeitas** e veja o que o jogo recebeu e respondeu — usando
os nomes que existem no proto (`abrirPedido`, `conferir`, `clienteSai`, `festaFim`, `novoCliente`),
**não** nomes inventados:

```javascript
// instrumentação: registra toda chamada real, com estado no momento da chamada
["abrirPedido","conferir","clienteSai","festaFim","novoCliente"].forEach(function(nome){
  var orig = window[nome];
  if (typeof orig !== "function") return;
  window[nome] = function(){
    log.push("CHAMADA " + nome + "(" + [].join.call(arguments,",") + ")"
      + " | atendendo=" + (typeof atendendo!=="undefined" ? !!atendendo : "?")
      + " | onda=" + (typeof onda!=="undefined" ? onda : "?")
      + " | aSpawnar=" + (typeof aSpawnar!=="undefined" ? aSpawnar : "?"));
    var r = orig.apply(this, arguments);
    log.push("RETORNO " + nome + " -> " + r);
    return r;
  };
});
```

Com isso o log responde à pergunta certa: *"o jogo ignorou a ação (bug) ou recusou a ação de
propósito num estado em que ela é inválida (design)?"* O caso paradigmático real do projeto é a
guarda **`MM.tDrop` de 280ms**: um teste que dispara toque+arrasto em sequência imediata "vê" o
segundo gesto ser ignorado e grita "bug" — mas o log mostra a guarda agindo (design correto, para
a criança não perder o clique num arrasto acidental). Sem instrumentação, isso vira um "conserto"
que quebraria o jogo de verdade.

**Procedimento fixo:** teste acusou defeito → instrumente → reproduza → só então conclua. Um "bug"
só entra no relatório com a linha de log que o prova. E, por design do motor, respeite a máquina
de estados: entre ações, **espere a condição** (ex.: `!atendendo`, `aSpawnar===0`), não um tempo
fixo.

### Passo 5 — Checklist visual final

Gere um print da cena cheia (com o auto-start da sonda) e a tira da rajada, e percorra item por
item, **marcando de verdade**:

```bash
"$CHROME" --headless --no-sandbox --disable-gpu \
  --window-size=1280,720 --virtual-time-budget=8000 \
  --screenshot="$QA/final.png" "file://$QA/jogo_qa.html" 2>/dev/null
```

| # | Item | Como conferir |
|---|------|----------------|
| 1 | **Proporção entre personagens** | No print: chef vs. clientes vs. móveis. Ninguém 2× o outro sem motivo. |
| 2 | **Pés no chão** | A base de cada sprite toca a linha do piso. "Flutuando" = corte com margem inferior errada (o `normaliza_set` cola os pés na base). |
| 3 | **Nada transpassa móvel** | Personagem atrás da mesa é ocluído por ela (`zIndex = round(y)`); ninguém "dentro" do balcão. |
| 4 | **Nada pisca** | Rajada do Passo 2: nenhum quadro com sprite ausente, nem bbox explodindo. |
| 5 | **Sem pulo de escala** | Rajada: altura aparente constante entre poses (a cura é o canvas comum por conjunto). |
| 6 | **Respiração presente no idle** | Rajada extra com o personagem PARADO (janela no idle): bbox pequeno e periódico no tronco. bbox `None` em todos = personagem rígido, reprovado. |

Só depois dos 6 itens conferidos — e com a **tira da rajada enviada ao professor** para o aval
visual dele — o movimento está aprovado.

---

## Resumo do ritual (cola de bolso)

```text
PARTE 1 (canônico, comportamento — o gate oficial):
  Playwright mm_test.js: abrirParada(i)+rodarFase() → errar de propósito (_errouNeste=true, SEM
  plaquinha) → consertar (plaquinha + Próximo) → zero pageerror → retrato 390×780 E paisagem.
  node --check após CADA edição; editar por âncora Python sub1, nunca regex gulosa (arquivo 3MB).

PARTE 2 (complementar, visual — caçar piscar/pulo de escala):
  0. node --check no JS extraído (e de novo após CADA injeção)
  1. Print de sanidade (--virtual-time-budget=4500)
  2. Rajada: 6–10 prints em degraus de ~150ms + diff/bbox com Pillow
  3. Sonda de estado (chef/clientes/onda/aSpawnar/atendendo) + --dump-dom
  4. Acusou defeito? INSTRUMENTE as funções REAIS (abrirPedido/conferir/clienteSai/festaFim) antes
     de concluir. O teste também tem bug: respeite a máquina de estados (ex.: guarda MM.tDrop 280ms).
  5. Checklist visual: proporção / pés no chão / oclusão / não pisca / escala estável / respiração
  6. Tira de quadros para o professor validar com o próprio olho.
```

O espírito do capítulo em uma frase: **movimento se testa no tempo, e veredito de bug só com log
que o prove** — porque neste projeto tanto o "funciona" quanto o "está quebrado" já foram, cada um,
mentira uma vez.

*(Ambiente verificado: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, Chromium 141,
Pillow 12.2. QA canônico: `MUNDO-VIVO-MOTOR.md` §5, `MUNDO-VIVO-ESPINHA.md` §5.)*

---

<a name="anexo-a"></a>
# Anexo A — O script oficial de corte

O corte de sprites do Mundo Vivo tem **um único dono**: o arquivo
**`_ferramentas/cortar_sprites.py`** (versão v5, "canvas comum por conjunto"). O Capítulo 2 explica
o script função por função (`recorta_raw`, `normaliza_set`, `uri`) com os limiares reais.

**Regra de manutenção (permanente):** **TODA mudança de pipeline deve ser refletida nos DOIS
lugares** — no `_ferramentas/cortar_sprites.py` **e** neste manual (`MUNDO-VIVO-SPRITES.md`). O
próprio comentário do script deixa isso escrito:

> `# NAO mude os limiares sem atualizar o manual MUNDO-VIVO-SPRITES.md.`

Portanto, ao ajustar um limiar (fundo `mn>240 & diff<14`, opening `iterations=2`, anti-halo
`mn>232`/erosão 2px), uma altura-alvo (chef 118 / clientes 100 / sentados 86), a quantização
(`colors=255, FASTOCTREE`) ou o layout de grade de uma cartela nova: **edite o `.py` e atualize o
Capítulo 2 na mesma entrega**. Script e manual são um par — divergir os dois é como o piscar de
sprite: os quadros deixam de bater.

Onde o script lê e escreve (ajuste os caminhos `R`/`S` ao usar): entrada em `_novo/` (`td_chef2.png`,
`td_chef4.png`, `td_anda_<bicho>.png`, `td_anda_lado.png`, `td_sentados.png`), saída em JSON de
data-URIs que o motor carrega como o objeto `IMG`.

---

<a name="rodape"></a>
# Rodapé — A regra permanente do Marcos

Duas regras fecham este manual, e nenhuma delas é negociável:

**1. Se o movimento está saindo DURO ou MALFEITO depois de 2 tentativas — PARE e ELEVE O MODELO.**
Não é o timing (o "135 ms do demo" e os números canônicos deste manual são testados); não é
insistir na 5ª tentativa às cegas num arquivo de 3 MB. É a **regra das 2 tentativas**
(`MUNDO-VIVO-ESPINHA.md` §7): bug de movimento que resiste a 2 hipóteses de conserto, ou animação
que continua parecendo amadora depois de 2 rodadas, **é hora do modelo forte** — avisar o Marcos
para trocar no `/model`, e, para agentes delegados, o coordenador refaz num modelo mais alto após 2
entregas ruins. Nunca insistir no barato num trabalho que já mostrou precisar do forte. Depois da
intervenção do forte, a solução vira **atualização deste documento** (novo número canônico, nova
barreira) — nunca conserto em silêncio.

**2. Nada vai ao professor sem passar pelo ritual de QA do Capítulo 5.** O gate canônico (roteiro
Playwright: errar de propósito, consertar, zero `pageerror`, retrato E paisagem) **e** a rajada
visual (piscar, pulo de escala, pés no chão, respiração no idle), com a **tira de quadros enviada
ao professor** para o aval do próprio olho dele. Movimento se prova no tempo, com log — não no
"no meu teste funcionava".

> *Memória viva: cada número aqui foi lido do código real
> (`_pub_confeitaria/mundo|proto/index.html`, `_ferramentas/cortar_sprites.py`) ou das lições pagas
> (`MUNDO-VIVO-MOTOR.md`, `MUNDO-VIVO-ESPINHA.md`). Quando o motor mudar, mude o manual junto —
> senão os quadros deixam de bater.*
