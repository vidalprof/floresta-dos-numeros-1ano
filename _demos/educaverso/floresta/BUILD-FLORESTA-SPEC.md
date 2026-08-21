# BUILD-FLORESTA-SPEC — "A Floresta do Byte" (aula de ~55 min)

> Plano de construção único e ordenado, síntese das 5 seções (Game Design, Pedagogia,
> Narrativa, Arte & Som, QA). É o que o dev implementa direto no arquivo
> `_demos/educaverso/floresta/index.html`, gerado por `build_floresta.py`.
> Responder/publicar sempre em pt-BR. Nada de dependência externa: tudo base64/inline, roda offline em PC velho.

## DECISÕES CANÔNICAS (conflitos das seções já resolvidos — não reabrir)
1. **Vilão = a Nimbo** (nuvenzinha cinzenta que chora névoa e, sem querer, prende os amiguinhos; vira amiga no fim entregando uma flor). O conceito alternativo "o Bug" (gremlin glitch) das seções de Game Design/Arte foi **descartado como personagem**; seu único resquício aproveitado é o *tema* "conserte o erro" (depuração), que já vive na mecânica das setas. Um personagem só, arco de empatia coerente com a abertura da floresta apagada.
2. **6 amiguinhos jogáveis** (1 por missão de resgate), nesta ordem fixa: **Miau (gato, já existe) · Pulo (coelho) · Piu (passarinho) · Lelê (tartaruga) · Tuca (esquilo) · Coaxo (sapo)**.
3. **Conceitos de PC** cobertos: sequência → ordem → desvio → **depuração** → repetição/loop → integração. **Condição (porteira colorida) é STRETCH** (opcional; só se sobrar orçamento de peso/tempo), embutida como variação, não como missão obrigatória.
4. **Motor reaproveitado**: grid 6×4 (`GW/GH`), `MIS[]`, `setMissao()`, `prox()`, `errou()`, `libertar()`, `signs{}`, `exec{}`, `ehObst()`, `cellPx()`, `balao()`, `salvos`, `estrelas[]`, `falar()`/speechSynthesis pt-BR, `unlock()` (destrava áudio no 1º gesto), loop `frame()`+`requestAnimationFrame`. **Nenhuma dependência nova, nada 3D.**
5. **Regra de ouro de ritmo**: DESAFIO → ALÍVIO → EXPLORAÇÃO → HISTÓRIA → repete. Nunca dois desafios seguidos sem respiro. Zero timer, zero placar de erro, zero "X vermelho". Erro = consequência fofa no mundo.

---

## 1) VISÃO (1 parágrafo)
A criança não "faz uma aula": ela **vive uma noite de resgate na Floresta do Byte**. A nuvenzinha triste Nimbo chorou uma névoa cinzenta que virou jaulas e prendeu os amiguinhos; a floresta perdeu cor e som. Guiando o vaga-lume Byte — plantando **setas de madeira** no chão (um algoritmo visível) e apertando **VAI** — a criança liberta um bichinho por missão. Cada resgate faz **um bichinho entrar no cortejo que segue o Byte**, **uma estrela subir** e **um naco do céu reacender** (progresso encarnado, nunca um número). O aprendizado de Pensamento Computacional (sequência, desvio, depuração, repetição) fica **escondido dentro do resgate** e cresce de dificuldade sem a criança perceber. No clímax, a criança descobre que Nimbo nunca foi má — só estava sozinha — e em vez de prendê-la, leva o Byte para entregar uma florzinha: a névoa vira arco-íris e todos festejam na cabana. É não-leitor-friendly (ícone + voz + cor), leve, offline e roda em máquina fraca.

---

## 2) ROTEIRO minuto a minuto (~55 min)
Uma **state machine de cenas** (`fase`) encadeia os blocos com transição em fade. Cada cena tem botão **"Ouvir de novo"** que repete a narração atual. `speechSynthesis.cancel()` antes de cada nova fala (não sobrepor).

| Tempo | Cena (`fase`) | Tipo | O que acontece | Amiguinho |
|---|---|---|---|---|
| 0–4 | `abertura` | história + destrava som | Fade-in. Floresta escura, poucos vaga-lumes. Criança **toca os vaga-lumes** e eles acendem com *plim* (1ª ação vitoriosa = destrava Web Audio/Speech). 9 falas de narração. Botão "Ouvir" pisca. | — (Nimbo prende todos) |
| 4–7 | `jogo` M1 | DESAFIO tutorial | Jaula perto, caminho reto. Mão-fantasma (setinha pulsando) mostra "toque no chão". Planta 1–2 setas → VAI → chave destranca + faísca + som próprio + agradecimento. Miau **sai da jaula e vira o 1º do cortejo**. +1 estrela. | Miau (gato) |
| 7–11 | `jogo` M2 | DESAFIO | Curva (1 virada). Cortejo cresce. A cada 2 resgates, vaga-lume grande sobe e acende um pedaço do céu. | Pulo (coelho) |
| 11–14 | `vagalumes` | ALÍVIO 1 | Vaga-lumes flutuam; toque captura num potinho que o Byte segura (*plim* + brilho). Sem falha/timer. Enche o pote → céu 1 tom mais claro. | — |
| 14–17 | `jogo` M3 | DESAFIO (desvio) | 1 árvore no caminho. Seta pra árvore → Byte **para e cheira a árvore** + balão "Ops! Por aqui não dá…". Reprograma. | Piu (passarinho) |
| 17–21 | `jogo` M4 | DESAFIO (depuração) | Começa com **setas pré-plantadas ERRADAS** (`setasPre`): rodar VAI mandaria o Byte na árvore. A criança troca só a peça errada e roda de novo. Vários obstáculos. | Lelê (tartaruga) |
| 21–25 | `exploracao` | EXPLORAÇÃO livre + HISTÓRIA | Flores murchas; toque leva o Byte a **regar** (som de água) → flor floresce → nasce vaga-lume. Sem trava. Narração calma: "a cor voltou; foi você". Gancho do fundo da floresta. | — |
| 25–29 | `memoria` | ALÍVIO 2 | Ladrilhos-folha virados no grid 6×4. Guia o Byte a **pisar** (mesma mecânica de setas) → folha vira → revela ícone de bicho. Par = acorde + piscar. Só ícone+cor+som, sem texto, sem timer. | — |
| 29–34 | `jogo` M5 | DESAFIO (repetição) | Corredor longo e reto: plantar 6 setas iguais fica "chato" (fricção de propósito). Byte "acha" no chão a **plaquinha REPETIR** (pips estilo dado, 2x/3x, sem número). Mão-fantasma ensina: solta num trecho reto, toca pra aumentar pips, Byte repete N vezes sozinho. *Aha* do laço. | Tuca (esquilo) |
| 34–39 | `jogo` M6 | DESAFIO (loop + desvio) | Corredor longo + pedras + curva. Solução bonita = REPETIR + desviar juntos. Ainda vencível na força bruta (não trava quem não pegou o loop). Reacende naco grande do céu. | Coaxo (sapo) |
| 39–42 | `exploracao` | EXPLORAÇÃO/alívio | Rega mais flores; cortejo (agora 6 bichos) anda em fila cantando baixinho. Céu quase todo aceso. | — |
| 42–49 | `climax` | HISTÓRIA (clímax) | Nimbo chorando no cantinho. **Sem jaula, sem erro punitivo.** Alvo = a Nimbo; ação = o Byte entrega uma **florzinha**. Diálogo: Nimbo pede desculpa ("só queria um amigo"). Névoa começa a virar arco-íris; flores nascem. | Nimbo (vira amiga) |
| 49–55 | `final` | FINAL / festa | Cabana com chaminé fumegando; cortejo inteiro + Nimbo dançam; céu lotado de vaga-lumes; fogos de pétala; arco-íris. **Contagem das estrelas** sobe uma a uma; **medalhinha de folha** com o Byte. Fala de encerramento. Loop calmo (dá pra ficar só olhando). | todos |

**Suculência transversal** (aplicar em toda vitória): micro screen-shake + zoom suave da câmera, burst de estrelas (já existe), arpejo da chave, faísca, som próprio do bicho, balão de agradecimento. Cortejo segue o Byte com atraso suave (trail de posições).

---

## 3) MISSÕES detalhadas (grid, objetivo de PC, conceito novo, gating)
Grid **6 col × 4 lin** (`GW=6, GH=4`), origem `[col,lin]` topo-esquerda. Expandir o `MIS[]` de 2 → 6 itens, adicionando campos novos por missão:

```
{
  start:[c,l], jaula:[c,l], obst:[[c,l],...],
  conceito:"sequencia"|"ordem"|"desvio"|"depuracao"|"repeticao"|"integracao",
  tipo:"jaula",                       // ("exploracao" p/ cenas sem objetivo)
  setasPre:{ "c,l":"dir"|"esq"|"cima"|"baixo", ... },  // só M4 (depuração): pré-planta ERRADO
  min:Number,                          // nº mínimo de setas (meta de eficiência; alimenta LOG)
  amiguinho:{ nome, mascoteImg, poseFeliz, posePreso, somClipe },
  falaIntro, falaDica, falaObrigado, falaGancho, corQueVolta
}
```

| # | `conceito` | Layout sugerido (start → jaula, obst) | Objetivo de PC (BNCC) | O que o GATING garante |
|---|---|---|---|---|
| M1 Miau | `sequencia` | start`[0,3]` jaula`[3,3]` obst`[]` | Instrução ordenada / causa-efeito: uma seta = uma ordem | `prox()`: sem seta na célula → `errou("O Byte não sabe pra onde ir…")` e reabilita VAI. Só liberta ao chegar na jaula. |
| M2 Pulo | `ordem` | start`[0,0]` jaula`[4,3]` obst`[]` | Sequência + "ordem importa": virar antes/depois muda o destino | Precisa ≥1 virada certa; direção errada bate na borda → consequência. |
| M3 Piu | `desvio` | start`[0,3]` jaula`[5,3]` obst`[[2,3],[3,3]]` (árvore bloqueia a reta) | Desvio / caminho alternativo: respeitar o mundo | Rota reta é `ehObst()` → trava; só completa contornando. Erro = "a seta apontou pra árvore" (Byte cheira a árvore). |
| M4 Lelê | `depuracao` | start`[0,0]` jaula`[5,3]` obst`[[2,1],[3,3],[4,1]]` + **`setasPre` propositalmente erradas** | Depuração: achar ONDE falhou, trocar só a peça, re-rodar | Começa "quebrada": rodar VAI levaria à árvore (consequência, sem X). Só completa quando a criança corrige a(s) seta(s). Registrar `corrigiuAposErro`. |
| M5 Tuca | `repeticao` | start`[0,2]` jaula`[5,2]` obst`[]` **corredor reto longo** | Repetição/laço: 1 peça faz o trabalho de muitas | Vencível na força bruta E com a **peça REPETIR** (não trava quem não pegou). Celebrar quando `usouRepeticao`. |
| M6 Coaxo | `integracao` | start`[0,0]` jaula`[5,3]` obst`[[2,0],[3,2],[4,0]]` **longo + curva + pedras** | Integração: reta + curva + desvio + laço juntos | Exige síntese; ao libertar o último (`mi===MIS.length-1`) → `fase="climax"` (não pula direto pro final). |

**Regra de gating (já no motor, manter):** `fase` fica `"jogo"` e o VAI reabilita a cada erro via `errou()`; a fase **não avança** enquanto a jaula não é alcançada (mastery gating, sem "pular fase"). `exec.steps>30` = anti-loop-infinito ("rodando em círculos").

**Peça REPETIR (mecânica, M5/M6):**
- Placa de madeira solta num trecho reto; toque **aumenta os pips** (2 pips = 2x, 3 pips = 3x, estilo dado — nunca número escrito).
- Em `prox()`: ao ler uma célula marcada como REPETIR, ler a **direção do passo daquela célula** e re-executá-la N vezes (contador de repetição no `exec`) antes de seguir.
- Descoberta em M5 com **mão-fantasma** de tutorial. UI 100% ícone de madeira (símbolo ↻ + pips), sem texto.

**Depuração (M4):** `setasPre` popula `signs{}` no `setMissao()` com setas erradas; a criança edita `signs` normalmente (toque gira/troca). Nada é apagado automaticamente.

**Registro invisível (avaliação, nunca visível à criança):** objeto `LOG` por missão em `localStorage`:
`{ tentativas, erros:{semSeta,apontouArvore,loop}, corrigiuAposErro:bool, usouRepeticao:bool, setasUsadas, min, tempo, concluida:bool }`. `prox()` já distingue os 3 tipos de erro. **Painel discreto do professor**: atalho secreto (ex.: pressão longa num canto) mostra/exporta `.json`. Jamais nota, jamais X, jamais exibido ao aluno.

---

## 4) JOGOS DE ALÍVIO / EXPLORAÇÃO (sem gating, sem timer, sem falha)
1. **`vagalumes` — Pegar vaga-lumes (Alívio 1, 11–14 min).** Partículas flutuam pela tela; toque captura → *plim* + brilho → sobem pro **potinho** que o Byte segura. Sem contagem punitiva. Encerra clareando o céu 1 tom. Reusa partículas + toque; nenhum motor novo.
2. **`memoria` — Memória no chão (Alívio 2, 25–29 min).** Ladrilhos-folha virados no grid 6×4. A criança **guia o Byte a andar por cima** (mesma mecânica de setas/toque). Ao pisar, a folha vira e mostra um medalhão de ícone de bicho. Par = acorde + os dois piscam. **Não-leitor:** ícone + cor + som, zero texto, zero timer. Reforça memória e planejamento espacial e "treina" andar no grid.
3. **`exploracao` — Regar flores (21–25 e 39–42 min).** Flores murchas espalhadas; toque leva o Byte até elas, **rega** (som de água) → flor floresce → nasce um vaga-lume. Sem objetivo, sem trava. Dispara narração-história calma. Puro deleite e autonomia.

Todos são cenas da state machine (`fase`); entrar/sair em fade sem travar o motor nem sobrepor narração.

---

## 5) HISTÓRIA e FALAS EXATAS (para o dev colar)
Centralizar num objeto `NARR`. **Sanitizar para TTS**: trocar "…"/reticências por vírgula/pausa curta; sem símbolos/emoji/pontuação que o pt-BR leia em voz alta ("barra", "hífen"). A narração **nunca entrega a resposta** (nunca "vire à direita duas vezes"); lê só o convite/enunciado. Explicação, quando houver, vem DEPOIS da ação, pela consequência no mundo.

### ABERTURA (narrador, sobre a arte) — cena `abertura`
1. "Bem-vindo à Floresta do Byte."
2. "Aqui tinha cor, tinha música, tinha muita risada."
3. "Mas uma nuvenzinha triste, a Nimbo, se sentiu sozinha e chorou uma névoa cinzenta."
4. "A névoa virou jaulas e prendeu todos os amiguinhos da floresta."
5. "As cores sumiram. As canções calaram."
6. "Só o Byte, o vaga-lume mais corajoso, ainda brilha."
7. "Você vai ajudar o Byte a soltar cada amiguinho e trazer a alegria de volta."
8. "Toque no chão para plantar uma seta de madeira. O Byte anda por onde ela aponta."
9. "Vamos começar. A floresta está esperando por você."

### M1 — Miau, o gatinho (tutorial)
- Intro: "Escute o miado bem baixinho. É o Miau, o gatinho, preso na jaula. Plante as setas e leve o Byte até ele."
- Dica de mão (sem resposta): "Toque no chão para pôr uma seta. Toque de novo e ela gira."
- Ao apertar VAI: "Vai, Byte, vai."
- Obrigado: "Miau. Você me soltou. Obrigado, Byte."
- Cor volta: "Olha. Uma corzinha voltou pra floresta."
- Gancho: "Escute, tem mais alguém chamando ali adiante."

### M2 — Pulo, o coelho (curva)
- Intro: "É o Pulo, o coelhinho, tremendo de medo. A jaula dele fica depois de uma curva. Leve o Byte até lá."
- Obrigado: "Pulei, pulei. Que saudade de pular. Muito obrigado."
- Cor volta: "Mais uma cor acordou. A floresta já sorri de novo."
- Gancho: "Sente esse ventinho doce. Vamos respirar um pouquinho."

### ALÍVIO 1 — Pegar vaga-lumes (cena `vagalumes`)
- "Descanse aqui um instante. Toque nos vaga-lumes e veja a luz dançar."
- "Cada amiguinho livre traz um pouco de brilho de volta. Está ficando lindo."
- Gancho: "Ouviu? Um pio fininho vem do meio das árvores. Alguém precisa de nós."

### M3 — Piu, o passarinho (desvio)
- Intro: "É o Piu, o passarinho, com a asa cansada. Uma árvore grande está no caminho. Guie o Byte por fora dela até a jaula."
- Obrigado: "Piu piu. Já consigo cantar de novo. Obrigado."
- Som volta: "Ouça. A música voltou pra floresta."
- Gancho: "Devagarinho, alguém bem devagar também espera por você."

### M4 — Lelê, a tartaruga (depuração / desvio difícil)
- Intro: "É a Lelê, a tartaruguinha. Já tem setas no chão, mas elas estão erradas e batem na árvore. Conserte o caminho para o Byte passar."
- Erro de consequência: "Ops. Essa seta bate na árvore. Troque só essa e tente de novo."
- Obrigado: "Bem devagar, mas muito feliz. Obrigada, Byte."
- Gancho: "A floresta já tem quase toda a cor. Falta pouco. Venha ver."

### EXPLORAÇÃO — Regar flores + a cor volta (cena `exploracao`)
- "Olhe ao redor. As flores abriram, os vaga-lumes voltaram. Foi você quem fez isso."
- "Toque numa flor murcha. O Byte vai regar e ela floresce."
- Gancho: "Mas ainda tem amiguinhos lá longe, e agora o caminho é comprido, comprido."

### ALÍVIO 2 — Memória no chão (cena `memoria`)
- "Vamos brincar de achar os pares. Guie o Byte para pisar nas folhas e ver quem se esconde."
- (par encontrado) — só acorde + piscar, sem fala obrigatória.

### M5 — Tuca, o esquilo (repetição / loop)
- Intro: "É o Tuca, o esquilo saltador, lá no alto. O caminho é longo e se repete. Que tal ensinar o Byte a repetir o mesmo passo?"
- Dica de mão (sem resposta): "Monte um pedacinho e peça pro Byte repetir. Assim você anda longe com pouquinhas setas."
- Obrigado: "Tuc tuc. Que caminho esperto. Obrigado."
- Gancho: "Olha lá na lagoa. Um coaxo triste. O último amiguinho da lista."

### M6 — Coaxo, o sapo (loop + desvio)
- Intro: "É o Coaxo, o sapinho da lagoa. O caminho é longo e cheio de pedras. Use o que você aprendeu, repita e desvie."
- Obrigado: "Coaxo feliz. A lagoa vai cantar de novo. Obrigado."
- Gancho: "Todos os amiguinhos estão livres, menos um. E esse ninguém esperava."

### CLÍMAX — o encontro com a Nimbo (cena `climax`; sem jaula, sem erro punitivo)
- "Olhe ali no cantinho. Ainda chorando, está a nuvenzinha Nimbo."
- "Ela não é má. Ela só estava sozinha e muito triste."
- "Aqui não tem jaula. Leve o Byte até a Nimbo e leve uma florzinha de presente."
- (ao chegar) "O Byte entregou a flor. A Nimbo abriu os olhinhos."
- Nimbo: "Vocês não fugiram de mim. Ninguém nunca ficou comigo."
- Nimbo: "Desculpa por prender todo mundo. Eu só queria um amigo."
- "A Nimbo chorou de alegria. E a chuvinha dela, agora feliz, fez as flores nascerem por toda parte."

### GRANDE FINAL — festa na cabana (cena `final`)
- "A névoa cinzenta virou arco-íris. A floresta acordou inteirinha."
- "Todos correram pra cabana: o Miau, o Pulo, o Piu, a Lelê, o Tuca, o Coaxo, e a Nimbo, a nova amiga."
- "A chaminé soltou uma fumacinha alegre. É festa na floresta."
- "E foi você quem trouxe a alegria de volta. Obrigado, pequeno guia."
- "Viva. A Floresta do Byte é feliz de novo."

### FALAS DE APOIO (reusáveis)
- Pôr seta: só som de madeira, sem voz (não cansar).
- Erros (consequência, com carinho — manter os existentes):
  - "Ops. A seta apontou pra árvore. Vamos arrumar?"
  - "O Byte não sabe pra onde ir aqui. Ponha uma seta nesta pedrinha."
  - "O Byte está rodando em círculos. Confira as setinhas."
- Nudge se parada ~20s: "Toque no chão para plantar a primeira seta. O Byte confia em você."
- Botão "Ouvir de novo": repete a fala da cena atual (essencial p/ não-leitor).

---

## 6) LISTA DE ASSETS NOVOS (com prompt curto) + DESIGN DE SOM
**Estilo obrigatório de toda imagem:** cartoon premium pintado à mão, mesma "cara" do Byte (contorno macio, luz suave, cores saturadas), **fundo branco puro para recorte** (transparência de verdade, sem franja branca, sem sombra na base). Corpo inteiro, ancorado nos pés. Pipeline: gerar PNG na pasta → autocrop → adicionar chave em `NM{}` e placeholder `__CHAVE__` em `SRC{}` no `build_floresta.py`.

### A) Amiguinhos (2 poses cada: `preso` triste na jaula / `feliz` andando)
> Se o orçamento de peso apertar: gerar só `feliz` e derivar `preso` por dessaturação leve + lágrima em canvas.
- **Pulo — coelho:** "Coelhinho filhote branco, bochechas rosadas, orelhas caídas, olhos grandes, corpo inteiro." (feliz pulando / preso com uma lágrima, orelhas baixas)
- **Piu — passarinho:** "Passarinho bebê azul, peito amarelo, asinhas abertas." (feliz voando/cantando / preso encolhido, olhinhos tristes)
- **Lelê — tartaruga:** "Tartaruguinha fofa, casco verde, focinho simpático." (feliz andando devagar / preso cabisbaixo)
- **Tuca — esquilo:** "Esquilo saltador fofo, rabo grande fofo, bochechas cheias." (feliz saltando / preso triste)
- **Coaxo — sapo:** "Sapinho de lagoa fofo, verde brilhante, bochechas de coaxar." (feliz sorrindo / preso triste)
- *(Miau, o gato, já existe — reusar `gato.png`.)*

### B) Nimbo (vilã fofa, 3 poses)
- "Nuvenzinha cinzenta fofa, olhinhos, boquinha — POSE emburrada/carrancuda."
- "Nimbo — POSE triste chorando lagriminhas cinzentas."
- "Nimbo — POSE feliz com pequeno arco-íris e chuvinha alegre."

### C) Props que viram mecânica
- **Placa REPETIR:** "Placa de madeira com setinha em laço circular gravada e pips estilo dado (versões 2 e 3 pontos), sem números."
- **Pedra grande** (obstáculo alternativo à árvore): "Pedra cinza arredondada com um pouco de musgo."
- **Tronco caído** (obstáculo): "Tronco de madeira caído com musgo."
- **Florzinha de presente** (item que o Byte entrega à Nimbo): "Florzinha colorida fofa."
- *(STRETCH, só se fizer condição) Porteira colorida:* "Cancela/porteira rústica, uma versão verde e uma vermelha."

### D) Itens dos alívios / exploração
- **Potinho de vaga-lumes:** "Jarro de vidro com tampa de folha, vaga-lumes acesos dentro, brilho suave." (o Byte segura)
- **Ladrilho-folha (memória):** "Folha virada para baixo (verso)" + "mesma folha virada mostrando um medalhão de ícone."
- **Flor murcha + florida:** "Flor murcha e a mesma flor aberta em 3 cores (rosa, amarela, lilás)."
- **Regador rústico:** "Regador de lata/madeira combinando com a floresta."

### E) Final / decoração
- **Medalha de folha:** "Medalha em forma de folha com a carinha do Byte gravada." (tela final)
- **Decoração não-colidível** (reusar com flip/escala p/ não inflar): tufo de flores silvestres; grupo de cogumelos vermelhos com pintinhas; arbusto com frutinhas; toco; pinheiro-ao-fundo (variação da árvore).

### DESIGN DE SOM (2 camadas — leve, offline)
**Camada 1 — Web Audio sintetizado (padrão do motor, sem arquivo):** adicionar, no molde dos bips/`somPasso` atuais —
`somPlantarSeta` (toc seco de madeira) · `somGirarSeta` (clique curto) · `somVai` (whoosh + sininho ascendente) · `somErro` (thud macio + farfalhar, gentil, NUNCA buzzer) · `somEstrela/coletar` (twinkle) · `somPassoPonte` (passo oco de tábua) · `somSplash` (água) · **1 som por amiguinho no resgate** (piado, grunhidinho, "sniff/pulo", coaxo, tuc-tuc — hoje só existe miau) · `somLoop` (pop/whoosh ao acionar REPETIR) · `somFanfarra` (fanfarra maior e calorosa no clímax).
**Camada 2 — clipes CC0 realistas embutidos em base64 (<60KB, mono, curtos, loop, ganho baixo):** ambiente de pássaros (~8s loop) · riacho/água (loop, sobe perto da água) · farfalhar de folhas/vento (loop) · chuvinha feliz (clímax) · celebração/festa (final). Fontes: Freesound CC0 / BBC SFX uso educativo. Tocar só após o 1º gesto (`unlock()` já existe); `speechSynthesis.cancel()` antes de cada narração.

---

## 7) CHECKLIST DE QA (gate antes de mostrar ao Marcos)

### PORTÃO 1 — VERIFICAR (a máquina prova)
- [ ] `node --check` no JS extraído do HTML final: **zero** erro de sintaxe.
- [ ] Renderiza no Chromium headless (`--headless --no-sandbox --disable-gpu --virtual-time-budget=4500`) **sem tela preta e sem console error**. (Chromium em `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.)
- [ ] **Dirigir CADA missão** (não presumir): injetar a solução de setas de M1–M6 e renderizar até a vitória — Byte chega, chave destranca, faísca + som + agradecimento, gating libera a próxima. Cobrir sequência, desvio, depuração e loop.
- [ ] **Dirigir cada ALÍVIO/EXPLORAÇÃO/HISTÓRIA** (`vagalumes`, `memoria`, `exploracao`, `climax`, `final`): entrar e sair sem travar o motor nem sobrepor áudio/narração.
- [ ] **Dirigir o ERRO de cada missão**: plantar seta pra árvore/parede → consequência no mundo (Byte para/cheira + fala), **nunca X vermelho**, e dá pra corrigir e seguir. Incluir o caso da depuração (M4 começa quebrada).
- [ ] **Rajada de 6–10 screenshots (~150 ms)** durante o movimento de cada missão: nada pisca, nada trava, passo não patina, respiração presente, câmera acompanha suave.
- [ ] **Offline/autossuficiente**: abre com `file://`, tudo base64, **nenhuma URL externa** (grep falha se achar `http`).
- [ ] **Orçamento de peso**: medir KB do HTML final; alvo **< ~2,5 MB**. Rodar com **CPU throttle 6x** e manter ~30 fps.

### PORTÃO 2 — AUDITAR (o cético confere)
**Arte:** todos os assets-chave são imagem de IA (nunca prop/personagem desenhado por código, inclusive os NOVOS: obstáculos, placa REPETIR, amiguinhos, Nimbo, potinho, folha, flores). Recorte transparente sem franja/sombra. Estilo consistente com o Byte. Mundo VIVO (respiração idle, vento, vaga-lumes, luz, fumaça) em cada tela. **y-sort** correto: sprites ancorados nos pés, dimensionados pela ALTURA (não estouram a célula), **balão não cobre o Byte**, obstáculo não esconde o Byte, jaula/animal/setas não se tampam. Conferir CADA tela e momento (idle, andando, na jaula, na festa, clímax).
**Mecânica:** ponta a ponta em todas as missões; gating trava (VAI não dispara sem setas válidas; não pula fase); erro = consequência em toda missão; colisão certa (não atravessa árvore/parede/obstáculo/jaula/personagem); **desvio realmente exige contornar** (reta falha de propósito); **loop realmente repete** (não é sequência disfarçada).
**Pedagogia:** aprende SEM perceber (nunca aparece "algoritmo/sequência/loop" pra criança); aluno ATIVO constrói o caminho (nunca escolhe alternativa); PC (BNCC) adequado a anos iniciais; não-leitores (ícone+voz+cor, narração NÃO entrega a resposta); ritmo de ~55 min sem buraco morto nem pico que trave o não-leitor.
**Língua:** pt-BR impecável, acentos, concordância (n=1), **nenhum símbolo/pontuação/emoji lido pelo TTS** (varrer cada string narrada).

### PORTÃO 3 — APROVAÇÃO DO PROFESSOR (Marcos)
- [ ] (1) missões/pedagogia + ritmo de 55 min · (2) a arte (assets novos recortados) · (3) o mundo jogável. Publica só depois das três.

### RISCOS × MITIGAÇÃO
- **Peso base64** (base já ~421 KB): alvo < ~2,5 MB; se estourar, otimizar/quantizar PNG, reusar o MESMO tile de grama/árvore, mascotes ~50 KB. Medir a cada entrega.
- **Partículas em PC velho**: cap de partículas por tela + degradação por fps (reduzir vaga-lumes se cair de ~30 fps); testar com throttle 6x; evitar redesenhar o mundo inteiro todo frame.
- **Áudio/narração no 1º gesto**: botão "Ouvir" piscando como start garantido; `resume()` do AudioContext cobrindo clique+toque+tecla; `speechSynthesis.cancel()` + fila por cena.
- **Regressão entre missões**: a bateria do Portão 1 dirige TODAS as missões a cada entrega, não só a nova.

---

## ORDEM DE IMPLEMENTAÇÃO SUGERIDA (para o dev)
1. State machine de cenas (`fase`) + fade + botão "Ouvir de novo" + objeto `NARR` central (sanitizado p/ TTS).
2. Expandir `MIS[]` p/ 6 missões com os campos novos (conceito/tipo/setasPre/min/amiguinho/falas).
3. Cortejo de salvos + medidor de estrelas + marcos do céu (progresso visível).
4. Depuração (M4, `setasPre`) e peça REPETIR (M5/M6) — as duas mecânicas novas de `prox()`.
5. Alívios/exploração (`vagalumes`, `memoria`, `exploracao`) reusando o motor de grid.
6. Clímax da Nimbo (alvo≠jaula, entregar flor, sem erro punitivo) + Grande Final (festa, contagem de estrelas, medalha).
7. Sons camada 1 (Web Audio) + camada 2 (loops CC0 base64) + suculência (screen-shake/zoom).
8. `LOG` invisível + painel do professor.
9. Gerar assets, injetar via `build_floresta.py`, rodar a bateria de QA dos 3 portões.
