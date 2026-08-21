# 🌎 EDUCAVERSO — Documento-Mestre

> **Versão de julho/2026** — documento vivo, escrito para o professor Marcos.
> Consolida os seis pareceres dos especialistas (motor, personagens vivos,
> produção, pedagogia, fábrica de mundos, roadmap) num só lugar, com uma regra
> acima de todas: **separar com honestidade o que já está CONSTRUÍDO e roda de
> verdade do que ainda é VISÃO / a-fazer.**

---

## 🛠️ ATUALIZAÇÃO 2026-07-17 — Plano A: o Estúdio Profissional (ferramentas modernas)

> **Decisão do Marcos:** adotar um **estúdio profissional** de ferramentas
> modernas — porque elas **facilitam a vida, são funcionais, gratuitas e evitam
> aquele monte de erro** que a gente pegava fazendo tudo "na unha" num HTML só.
> **Nada do modelo leve foi apagado** — o Plano A vive **À PARTE**, para a gente
> acessar quando quiser; os dois patrimônios continuam intactos.

**A pilha (stack) do Plano A — tudo grátis e open-source:**
- **Phaser 3** (3.80.x) — motor de jogo 2D (WebGL2/Canvas), física, câmera, tweens.
- **TypeScript** — pega erro ANTES de rodar (o "monte de erro" some no build).
- **Vite** — empacota/otimiza; `target: ['chrome109','firefox106']` (os navegadores REAIS da escola).
- **Node 20** — só na hora do build (no workflow), nunca no PC da escola.
- **Futuro (quando fizer sentido):** React (painel do professor), Tiled (mapas),
  Zod/JSON-Schema (validar os dados que a IA gera), Vitest/Playwright (testes),
  ESLint (padrão de código), PWA (funcionar offline no laboratório).

**Onde mora e como publica:**
- Código-fonte: pasta **`educaverso-app/`** (Phaser+TS+Vite) neste repositório.
- Build/deploy: workflow **`.github/workflows/app-build.yml`** (`workflow_dispatch`)
  → `npm install && npm run build` → publica o `dist/` num **repo separado
  `educaverso-app`** via `PAGES_TOKEN`. No ar em **https://vidalprof.github.io/educaverso-app/**.
- **Não mexe** no modelo leve (`_educaverso/`, `_site/`, atividades premium): continuam vivos.

**Alvo de hardware (PC real da escola — testar SEMPRE nele):**
- AMD FX-4300 · **3,5 GB RAM** · Windows 7 64 bits · **Chrome 109** e **Firefox 106**.
- Modo ultraleve obrigatório: `Scale.FIT 1024×768`, `fps.target: 30`, `antialias:false`,
  `roundPixels:true`, `powerPreference:'low-power'`, texturas pequenas desenhadas 1x.
  A RAM baixa (3,5 GB) é o gargalo → nada de spritesheet gigante; liberar o que não usa.

**Por que isso serve TANTO ao mundo vivo quanto às atividades premium:**
o mesmo estúdio produz a experiência revolucionária (mundo vivo explorável 2D) e,
quando o Marcos quiser, as atividades premium avulsas — a **mecânica é peça
reutilizável** (ver "ordenar comandos" = algoritmo), montada uma vez e encaixada
onde precisar (dentro do mundo OU como atividade solta).

### 🔊 REGRA DE OURO reafirmada (voz) — vale também no Plano A
**TODA voz é gerada por API (edge-tts, voz "Antonio" = `pt-BR-AntonioNeural`),
embutida como MP3 e tocada com `<audio>`. NUNCA a voz do navegador
(`speechSynthesis`/Web Speech).** É decisão firme do Marcos (ver
`EDUCAVERSO-SUSTENTABILIDADE.md` e `EDUCAVERSO-CHECKLIST-DE-CENA.md`). A voz é
gerada pelo workflow **`gerar-audio.yml`** (grátis, natural, sempre igual em
qualquer PC). *Pendência técnica registrada:* a Etapa 2 do app usou Web Speech
por engano → **refatorar para tocar os MP3 do Antonio.**

### 🧭 NORTE reafirmado — é MUNDO VIVO explorável 2D
O diferencial é a criança **andar pelo mundo vivo** e encontrar os problemas no
contexto (currículo invisível: o conceito vem por último). A "tela de puzzle"
isolada **não** é o objetivo — a mecânica acontece **dentro** do mundo vivo.

---

## A tese

**Um motor único + arte gerada por IA + dados = mundos infinitos, leves,
premium e sustentáveis.**

O EducaVerso não é "mais um joguinho". É a decisão de parar de pintar cada
mundo à mão (lindo, mas pesado e impossível de escalar) e montar uma **linha de
produção**: um **motor** escrito uma vez (o Canvas 2D que anda, tem câmera,
clima, luz, colisão, voz), alimentado por **arte que a IA gera** (tiles e
sprites) e por **dados** (o mapa, as falas, as missões). Fazer um mundo novo
deixa de ser "desenhar tudo de novo" e passa a ser "gerar uns PNGs + trocar
umas tabelas". O mesmo motor serve a Confeitaria das frações, o Mar dos Números
dos piratas e qualquer bairro da BNCC que vier depois — cada um leve o
bastante para rodar no PC Windows 7, 1024×768, da escola pública.

## O sonho — o melhor dos dois mundos

Existem, hoje, **dois patrimônios** neste repositório, e o sonho é uni-los sem
perder nenhum dos dois.

De um lado, a **visão do EducaVerso**: um universo educativo vivo — mundos que
mudam com o clima e a hora do dia, personagens que respiram e falam, a criança
entrando pelo **código da turma e o primeiro nome**, o mundo que **lembra
dela** de uma aula para outra, o mascote que evolve por marco de aprendizagem,
e o professor com um painel que mostra, sem prova nenhuma, **quem empacou em
quê**. Escala barata, arte premium, avaliação invisível.

Do outro lado, o **Mundo Vivo que já roda**: duas demos jogáveis e
autossuficientes (o *Mundo Vivo do Byte* e *A Taberna do Byte*), um motor de
missões concretas que já funciona (a Confeitaria, com o erro virando
consequência no mundo em vez de X vermelho), um pipeline de arte e voz que
gera de verdade nos workflows do GitHub, e uma biblioteca de manuais que
fundamenta cada decisão na BNCC e em Papert.

O sonho é **costurar os dois**: colocar o motor de missões que já ensina
**dentro** do mundo leve que já encanta, ligar a memória e o painel, e provar
que o molde barato escala por bimestre. Ambicioso — mas viável porque é
**incremental**: cada passo entrega algo que dá para levar para a sala já na
semana seguinte.

---

## Índice

1. [✅ O que já existe hoje (jogável)](#-o-que-já-existe-hoje-jogável)
2. [O Motor Único (arquitetura reutilizável)](#o-motor-único-do-educaverso--a-arquitetura-reutilizável)
3. [Personagens Vivos (animação estilo videogame)](#personagens-vivos--animação-estilo-videogame)
4. [Produção & Sustentabilidade (o pipeline)](#produção--sustentabilidade--a-linha-de-montagem-do-educaverso)
5. [Pedagogia (o aprendizado dentro do mundo)](#pedagogia--o-aprendizado-que-mora-dentro-do-mundo)
6. [Fábrica de Mundos (escalar por tema+turma)](#a-fábrica-de-mundos--escalar-por-tema--turma)
7. [Roadmap & Produto (tornar realidade)](#roadmap--produto--do-que-existe-hoje-ao-educaverso-em-sala)
8. [Tabela consolidada: CONSTRUÍDO × A-FAZER](#tabela-consolidada-construído--a-fazer)
9. [Os 5 primeiros passos](#os-5-primeiros-passos)
10. [Regras permanentes do projeto](#regras-permanentes-do-projeto)

---

## ✅ O QUE JÁ EXISTE HOJE (jogável)

> Resumo honesto do patrimônio real — o que se pode abrir no navegador **hoje**
> e o que já roda nos bastidores. Tudo com o caminho do arquivo.

### As duas demos jogáveis (rodam de verdade, sem servidor)

- **Mundo Vivo do Byte** — `_demos/educaverso/index.html` (~504 KB, gerado por
  `_demos/educaverso/build_premium.py`). Mundo de tiles com arte de IA, câmera
  que segue com suavidade, **clima** (sol, chuva, neve, tempestade, noite) com
  tint + vinheta + partículas, **raios com trovão** sintetizado, **dia/noite**
  com estrelas e lua, vento, colisão que desliza, ordenação por profundidade,
  poeirinha ao correr, balão de fala e narração por voz em pt-BR.
- **A Taberna do Byte** — `_demos/educaverso/taberna/index.html` (~764 KB,
  gerado por `_demos/educaverso/taberna/build_taberna.py`). Prova o
  **gerenciador de cenas** (fora/dentro) com transição em fade, **luz de
  lampião** (escuridão + poças de luz quente), **porta de verdade** trancada
  que só abre com a **chave** do **inventário**, **gatilhos por proximidade**
  com o prompt `[ E ]`, e **NPCs vivos** (o taberneiro e o gato) que respiram,
  falam e são narrados.

Juntas, elas provam — item por item — os 11 sistemas do motor: laço com
delta-time real, câmera com lerp/clamp, tiles infinitos por `createPattern`,
costa orgânica por funções de seno, clima e dia/noite, sistema de luz, colisão
por eixo, inventário/itens/porta, y-sort, personagem+NPCs com o mesmo "corpo
vivo", e fala/narração para quem ainda não lê. A evidência mais forte de que o
"motor único" existe na prática é que **as duas demos compartilham ~90% do
mesmo JavaScript** — muda a arte e os dados, o motor fica.

### O motor de missões que já ensina (protótipo Confeitaria)

- `_pub_confeitaria/proto/index.html` — o **micromundo de missões concretas**
  com 5 modos (A repartir, A2 agrupar, A-montar, B dinheiro, D proporção),
  catalogados em `MUNDO-VIVO-MOTOR.md`. O **erro vira consequência** (a carinha
  entristece e treme, a criança conserta sozinha; sem X, sem vidas, sem
  cronômetro). Tem `acerto()`/`erro()` por habilidade e **modo professor pelo
  código `1275@`**. O motor de referência completo mora em
  `_pub_confeitaria/mundo/index.html` (~2,9 MB, artesanal — é a peça que o
  EducaVerso torna leve).

### O pipeline de geração (roda nos workflows, não no navegador)

- **Arte:** `.github/workflows/gerar-imagens.yml` (Pollinations grátis, ou
  Gemini pago que **edita** uma imagem base mantendo o personagem).
- **Voz:** `.github/workflows/gerar-audio.yml` (edge-tts natural, grátis) +
  `otimizar-audio.yml` (recompressão para embutir muita fala sem inchar).
- **Corte de sprites:** `_ferramentas/cortar_sprites.py` (flood-fill,
  anti-franja, autocrop, canvas comum que cura o "piscar" das poses).
- **Publicação:** `fabrica.yml`, `atualizar.yml`, `recuperar.yml`,
  `republicar-limpo.yml`, `deploy-pages.yml`.
- **Molde de painel do professor** pronto para clonar: `_painel/index.html`.

### Os manuais e o molde da fábrica

- `MANUAL-MESTRE.md`, `MUNDO-VIVO-MOTOR.md`, `MUNDO-VIVO-ESPINHA.md`,
  `MUNDO-VIVO-SPRITES.md`, `PLANO-FORA-DA-CAIXA.md`, os 5 pareceres em `_plano/`.
- `FABRICA-DE-MUNDOS.md` — o manual da linha de montagem (17 passos, com os 12
  "furos" do cético já incorporados).
- `_fabrica_mundos/TEMA-EXEMPLO-mar-3ano.json` — o **TEMA-SPEC** de exemplo já
  revisado ("Mar dos Números", piratas, 3º ano, multiplicação, 11 paradas).

### O que ainda NÃO existe (para não haver ilusão)

O **motor único ainda não é um arquivo compartilhado** (é comprovado por
duplicação); **nenhuma demo tem login, save ou painel ligado**; o **montador**
que junta motor + TEMA-SPEC **não existe**; e **nenhuma demo foi testada com
crianças reais** ainda. Os detalhes de cada lacuna estão nas seções a seguir.

---

## O Motor Único do EducaVerso — a arquitetura reutilizável

> Fonte real: `_demos/educaverso/build_premium.py` (Mundo Vivo do Byte) e
> `_demos/educaverso/taberna/build_taberna.py` (A Taberna do Byte). Os
> `index.html` de cada pasta são o resultado desses scripts com a arte
> embutida em base64.

### A ideia central: "só a arte e os dados mudam; o motor fica"

Quem lê os dois demos lado a lado descobre uma coisa reveladora: **cerca de 90%
do código é idêntico**. O laço principal, a câmera, o andar do personagem, a
sombra, o balão de fala, a voz, o preenchimento de tiles, o balão e a ordenação
por profundidade são praticamente os mesmos nos dois mundos. O que muda de um
mundo para o outro é só:

1. **A arte** — os PNGs pintados pela IA (`grama.png`, `agua.png`,
   `fachada.png`, `taberneiro.png`...).
2. **Os dados** — as tabelas de posições (onde ficam as árvores, os lampiões, a
   chave, os NPCs) e as regras da cena.

Essa é a tese do EducaVerso provada em código: um mundo novo = trocar uns PNGs
+ trocar umas tabelas. O motor não se reescreve.

### 1. Laço principal — tempo REAL, nunca contar frames

O coração é a função `frame(ts)`, chamada por `requestAnimationFrame`. A
primeira linha calcula o **delta-time real**:

```
var dt=Math.min(0.05,(ts-ult)/1000);ult=ts;
```

`dt` é o tempo em segundos desde o quadro anterior. **Tudo se move multiplicado
por `dt`** (velocidade, partículas, animações), então o mundo anda na mesma
velocidade num PC rápido e num PC lento — essencial para os Windows 7 antigos
da escola. O `Math.min(0.05,...)` é uma trava de segurança: se a criança troca
de aba e volta, o `dt` não vira um número gigante que teletransportaria o Byte
para fora do mapa.

No Mundo Vivo o laço separa bem **lógica** (`logica(dt,t)`) de **desenho** (o
resto do `frame`); na Taberna está tudo dentro do `frame`, mas o princípio é o
mesmo.

### 2. Gerenciador de CENAS (fora/dentro) com transição em fade

Isto vive na Taberna. Uma única variável decide onde estamos: `var cena="fora"`.
O `frame` se ramifica por ela:

```
if(cena==="fora")moverByte(dt,limFora);else moverByte(dt,limDentro);
...
if(cena==="fora")drawFora(t);else drawDentro(t);
```

Cada cena traz o **seu próprio tamanho de mundo** (`FW/FH` fora, `RW/RH`
dentro), a **sua própria função de colisão** (`limFora` / `limDentro`) e o
**seu próprio desenho** (`drawFora` / `drawDentro`).

A **transição em fade** é elegante e reaproveitável:
- `irPara(novaCena, bx, by)` liga `fadeDir=1` e guarda um `fadeAcao` (uma
  função que troca `cena` e reposiciona o Byte).
- O `frame` escurece a tela (`fade` de 0 a 1). **No auge do escuro** ele
  executa o `fadeAcao` (a troca acontece invisível) e inverte para clarear
  (`fadeDir=-1`).
- Enquanto a transição roda, o movimento é congelado (`if(!fadeDir)moverByte(...)`).

O usuário nunca vê o "corte" — vê um piscar preto suave, como num livro que
vira a página.

### 3. Tiles via `createPattern` + costa/regiões orgânicas

A arte da IA vira "papel de parede infinito" com uma linha:

```
patG=cx.createPattern(IMG.grama,"repeat");
```

Depois pinta-se só a área visível, em coordenadas de mundo:
`cx.fillStyle=patG; cx.fillRect(cam.x,cam.y,VW,VH)`. Um único PNG de grama
cobre um mundo de 2200×1500 sem pesar nada.

O truque premium é como praia e mar aparecem **sem grade quadriculada**. Em vez
de tiles em xadrez, há **funções de borda orgânica**:

```
function edgeMar(y){return WW*0.64-(y/WH)*(WW*0.10)+Math.sin(y*0.009)*60+Math.sin(y*0.028)*18;}
```

Essa função devolve, para cada altura `y`, a posição `x` onde começa o mar —
com senos que dão uma linha de costa sinuosa e natural. `regMar()`/`regAreia()`
transformam essa curva num **recorte (`clip`)** e pintam o padrão de água/areia
só dentro dele. Resultado: praia e mar são **regiões orgânicas pintadas por
cima da grama**, não quadradinhos. Na Taberna o chão de madeira é um pattern
cheio (`patM`) e as paredes (`patP`) são quatro retângulos de espessura `T` na
borda.

### 4. Câmera que segue com lerp e clampa nas bordas

A câmera mira o Byte, mas com suavidade e sem "vazar" para fora do mapa:

```
var ax=Math.max(0,Math.min(byte.x-VW/2, W-VW));   // alvo já preso às bordas
cam.x+=(ax-cam.x)*Math.min(1,dt*7);               // lerp suave até o alvo
```

O `Math.max/min` (clamp) garante que a câmera nunca mostre o "nada" além da
borda do mundo. O `lerp` (`(alvo-atual)*fator`) faz a câmera **deslizar** atrás
do personagem em vez de grudar nele — dá sensação de cinema. Todo o desenho do
mundo acontece dentro de um `cx.translate(-cam.x,-cam.y)`, então basta desenhar
em coordenadas de mundo e a câmera cuida do resto.

### 5. Clima e Dia/Noite (tint + vinheta + partículas)

Tudo comandado por uma string `clima` (`sol`/`chuva`/`neve`/`tempestade`/`noite`).
A receita é sempre **três camadas por cima do mundo já desenhado**:

- **Tint (cor do ar):** `corClima()` devolve as cores de um degradê que cobre a
  tela inteira — roxo/laranja no sol, azul-acinzentado na chuva, azul-marinho
  profundo à noite.
- **Vinheta:** um degradê radial que escurece as beiradas (mais forte em
  tempestade e noite), focando o olhar no centro.
- **Partículas:** arrays `chuva[]` e `neve[]` (em coordenadas de tela),
  atualizados por `dt` e reciclados quando saem embaixo. Chuva vira linhas
  inclinadas; neve, bolinhas que balançam. O **vento** (`vento` que faz *lerp*
  até `ventoAlvo`) inclina a chuva e embala a neve e as árvores.

Efeitos especiais que dão o "uau":
- **Raios (tempestade):** um cronômetro `proxRaio` dispara um relâmpago — uma
  linha quebrada (`raio.pts`) construída com passos aleatórios, um `flash`
  branco que some, e **trovão sintetizado** em Web Audio (`trovao()`: ruído
  filtrado por *lowpass*).
- **Noite:** `estrelas[]` que piscam, lua desenhada com dois arcos (o segundo,
  na cor do céu, "morde" o primeiro e forma o crescente) e um brilho radial com
  `globalCompositeOperation="lighter"`.
- **Sol/cintilância:** brilho pulsante do sol e "vaga-lumes" (`vagas[]`) que só
  aparecem no sol e na noite, todos somados com `lighter` + `shadowBlur`.

### 6. Sistema de LUZ (lampião: escuridão + poças de luz quente)

Esta é a assinatura visual da Taberna e o padrão de iluminação do motor. São
dois passos:

1. **Escurecer tudo:** `cx.fillStyle="rgba(10,7,20,.72)"; cx.fillRect(0,0,VW,VH)`
   — a sala inteira fica na penumbra.
2. **Cavar a luz:** troca-se para `cx.globalCompositeOperation="lighter"` e,
   para cada lampião, desenha-se um degradê radial quente. No modo `lighter` a
   luz **soma** em vez de cobrir, então cada lampião **abre uma poça de luz
   dourada** no escuro. Uma bruxaria com `fl=0.85+0.15*Math.sin(...)` dá o
   **tremeluzir** da chama. O Byte também carrega uma luzinha fria suave, e há
   poeira de luz flutuando.

Esse par "manta escura + luz somada com `lighter`" é o mecanismo reutilizável
para qualquer ambiente fechado (caverna, porão, sala à noite).

### 7. Colisão por eixo (desliza em vez de travar)

O andar não trava feio na parede — ele **desliza**. No Mundo Vivo isso é
explícito:

```
if(colide(nx,byte.y)){nx=byte.x;byte.vx*=-0.3;}   // testa só o eixo X
if(colide(nx,ny)){ny=byte.y;byte.vy*=-0.3;}       // depois só o eixo Y
```

Testando cada eixo em separado, quando o Byte esbarra numa árvore andando na
diagonal, ele perde só a componente bloqueada e **continua correndo pela
outra** — a sensação natural de raspar num obstáculo. As árvores são colisores
circulares (`dx*dx+dy*dy < r*r`); o mar é bloqueado por `edgeMar`. Na Taberna a
colisão é injetada como **função da cena** (`limFora`/`limDentro`) passada para
`moverByte(dt, limitar)` — o motor não sabe o formato da sala, a cena é que
informa. Bloqueiam corpo do prédio, árvores e os NPCs (taberneiro, gato).

### 8. Inventário, itens, porta e gatilhos

- **Item + inventário:** `inv={chave:false}` e um objeto `chave` com flag `peg`.
  Perto da chave + tecla **E** → `chave.peg=true`, `inv.chave=true`, balão de
  fala. O HUD desenha a "Mochila" com o ícone da chave quando ela está guardada.
- **Gatilhos por proximidade:** a cada quadro o jogo calcula `proxE` — o texto
  da ação disponível ("Pegar a chave", "Abrir a porta", "Falar com o
  taberneiro") — e mostra o aviso `[ E ]`. A tecla **E** chama `acaoE()`, que
  decide a ação pela cena e pela distância.
- **Porta de verdade:** perto da fachada, se `inv.chave` for verdadeiro, fala
  "Vou entrar!" e chama `irPara("dentro",...)`; senão avisa que está trancada.
  O tapete de **SAÍDA** no centro embaixo devolve para fora. Chave → porta →
  cena nova: é o loop de exploração completo.

### 9. Ordenação por profundidade (y-sort)

Para o Byte passar corretamente na frente ou atrás das árvores e NPCs, tudo
entra numa lista com sua altura `y` e é ordenado antes de desenhar:

```
elems.push({y:byte.y,k:"byte"}); ... elems.sort(function(a,b){return a.y-b.y;});
```

Quem tem `y` maior (está "mais para baixo/perto") é desenhado por último e cobre
quem está atrás. É o que faz o mundo parecer ter profundidade com desenho 2D
puro.

### 10. Personagem e NPCs (o mesmo "corpo vivo")

`desenhaByte()` e `npc()` compartilham a mesma anatomia: imagem ancorada nos
**pés** (`drawImage(im,-w/2,-h,...)`), altura fixa e largura pela proporção,
`dir` que espelha com `scale(dir,1)`, **sombra elíptica** embaixo, **balanço
(bob)** ao andar e **respiração** (escala sutil) parado. O movimento usa
velocidade com *lerp* até a velocidade-alvo, marca `mov` quando passa de um
limiar e solta **poeirinha** ao correr. Trocar o personagem = trocar um PNG.

### 11. Fala e narração (para quem ainda não lê)

Web Speech API em pt-BR: `vozPt()` escolhe a melhor voz portuguesa, `falar()`
narra, `balao(texto, alvo)` mostra o balão (com rabinho apontando para quem
fala — Byte, taberneiro ou gato) e narra junto. Como **nenhum navegador deixa o
som começar sem um gesto**, há o `destrava()` no primeiro clique/tecla. É
acessibilidade real para os menores.

### O que JÁ ESTÁ construído (e funciona)

Os dois demos rodam de verdade e provam, item por item, todos os 11 sistemas
acima. A duplicação quase total entre eles é a evidência mais forte de que o
"motor único" existe na prática.

### O que ainda falta (visão honesta)

- **Extrair o motor de fato num arquivo só.** Hoje o motor é comprovado por
  *copiar-e-colar* entre os dois demos, não por um `motor.js` compartilhado. O
  próximo passo estrutural é isolar o núcleo (laço, câmera, colisão, tiles,
  luz, clima, y-sort) num módulo único que os mundos importam.
- **Gerenciador de cenas genérico.** Hoje é um `if(cena==="fora")...else...`.
  Para escalar a muitos mundos, precisa virar um **registro de cenas** guiado
  por dados (uma tabela que descreve cada cena, seus assets e gatilhos), não
  `if/else` na mão.
- **Tilemap por grade editável.** Os obstáculos são arrays fixos no código e
  funções de borda (`edgeMar`). Falta um **mapa em grade, editável por dados**,
  para o professor/aluno montar cenários sem mexer em JavaScript.
- **Colisão do prédio ainda meio artesanal.** O `limFora` (linha ~108 do
  `build_taberna.py`) tem um bloco confuso, com ramos `{}` vazios — funciona,
  mas pede uma caixa de colisão limpa e reutilizável.
- **Movimento por clique é em linha reta** (para no obstáculo, não o contorna).
  Falta busca de caminho (pathfinding) se quisermos clique "inteligente".
- **Diálogo é de uma frase só.** Os balões não têm árvore de conversa/perguntas
  — base necessária para o "conhecimento como ferramenta" da visão do professor.
- **Clima e luz ainda não unificados.** Clima completo vive só no Mundo Vivo; a
  Taberna tem só luz. Falta juntar num módulo único que qualquer cena ligue com
  uma linha.

---

## Personagens Vivos — animação estilo videogame

O professor quer que Byte e os outros personagens "ganhem vida como nos
videogames": respirar, mexer a boca ao falar, piscar os olhos, balançar parado.
Esta seção mostra, com honestidade, **o que os demos já fazem hoje** e
**projeta o sistema de expressão** que falta — leve, em Canvas 2D, rodando liso
em PC Windows 7 antigo.

### O que já está vivo hoje (nos arquivos reais)

Nos dois demos (`_demos/educaverso/index.html` e
`_demos/educaverso/taberna/index.html`, gerados por `build_premium.py` e
`build_taberna.py`) os personagens já têm três camadas de vida:

- **Respiração parada (idle).** Quando Byte está sem andar, o corpo infla e
  esvazia numa onda senoidal: `byte.resp += dt*3` e depois
  `resp = Math.sin(byte.resp)*0.028`, aplicado como
  `cx.scale(byte.dir*(1+resp), 1-resp*0.6)`. É o "peito subindo e descendo".
- **Balanço da caminhada (bob).** Ao andar, o personagem sobe e desce a cada
  passo: `bob = Math.abs(Math.sin(byte.passo*0.8))*6`, com
  `byte.passo += dt*11`. A sombra no chão encolhe junto — dá peso e ritmo.
- **NPCs também respiram.** Na taberna, a função `npc()` faz o taberneiro e o
  gato respirarem com `resp = Math.sin(t*0.002 + x)*0.02` — cada um numa fase
  diferente (o `+x`), então não "batem o peito" ao mesmo tempo.
- **Fala com balão + narração de voz.** `balao(texto)` mostra o balão por 4,6s
  e `falar(texto)` narra em pt-BR (`SpeechSynthesisUtterance`, voz escolhida por
  `vozPt()`), com destravamento do áudio no primeiro gesto (`destrava()`).

**O que ainda NÃO existe:** a boca **não mexe** durante a fala, os olhos **não
piscam**, e não há **emoções** (feliz/pensando/surpreso). Além disso, Byte e os
NPCs são **PNGs únicos e estáticos** (`byte.png`, `taberneiro.png`,
`gato.png`) — o rosto é uma imagem fixa. É exatamente essa lacuna que o sistema
abaixo preenche.

### A decisão de arquitetura: dois caminhos para o rosto

Como o sprite é uma foto única, para mexer boca e olhos há dois caminhos — e o
melhor é **misturar os dois**:

**Caminho A — desenhar boca e olhos POR CÓDIGO por cima do sprite (recomendado
para o Byte).** Byte é um robô: uma boca (curva/retângulo) e dois olhos
(pontos) desenhados no Canvas sobre a imagem custam quase nada, **não pesam 1
byte a mais**, e ficam **sempre em sincronia** com a fala. Desenhados dentro do
mesmo `translate/scale` do sprite, acompanham de graça a respiração e o bob.

**Caminho B — gerar uma CARTELA de poses por IA (para rostos humanos com
detalhe, ex. taberneiro).** Pede-se ao workflow de imagem uma folha do MESMO
personagem, só trocando boca/olhos: (1) boca fechada, (2) boca aberta, (3)
olhos fechados, (4) sorrindo. Troca-se a imagem do `drawImage` conforme o
estado. É fotorreal, mas pesa ~4× (cada pose ~30–50KB).

**Regra prática:** Byte e mascotes-robô = **Caminho A** (custo zero, sincronia
perfeita). Rostos que precisam de detalhe humano = **Caminho B**, e mesmo assim
de forma leve (só a faixa da boca/olhos como overlay, não o corpo inteiro).

### O sistema de expressão (4 peças)

#### 1. Boca sincronizada com a fala (lip-sync)

O evento `onboundary` do Web Speech marca fronteiras de palavra, mas em
navegadores antigos do Windows 7 **ele nem sempre dispara** — não dá para
confiar só nele. A solução robusta: um **flap por timer** que liga no `onstart`
e desliga no `onend`; enquanto o personagem fala, a boca oscila ~7 vezes por
segundo com um pouco de aleatório; quando `onboundary` existir, ele dá um
"empurrão" extra na abertura para ficar mais natural.

#### 2. Piscar (blink)

A cada 3–6 segundos, fecha os olhos por ~120ms. Cada personagem tem seu próprio
relógio, então não piscam todos juntos.

#### 3. Idle: micro-balanço + respiração

Já existe (respiração senoidal). Refinamento: somar um micro-balanço lateral
lentíssimo (`Math.sin(t*0.0009)*0.5px`) para o parado nunca ficar "congelado".

#### 4. Emoções simples

Um estado `emocao[personagem]` ("feliz" / "pensando" / "surpreso" / "neutro")
muda a forma dos olhos e da boca:
- **feliz:** boca em curva pra cima, olhos normais.
- **pensando:** um olho semicerrado, boca pequena de lado (combina com "..." no
  balão) — reforça o Byte que faz PENSAR, sem entregar a resposta.
- **surpreso:** olhos maiores, boca em "O" aberta.

### Pseudo-código: `falarComBoca(texto, personagem, emocao)`

```javascript
// --- ESTADO POR PERSONAGEM (um registro leve para cada um) ---
var vida = {
  byte: { falando:false, bocaAlvo:0, bocaAbertura:0, mouthPhase:0, kick:0,
          proxPisca:3, piscaT:0, olho:1, emocao:"neutro" }
  // ... um bloco igual para "tab", "gato", etc.
};

// Face de cada personagem: onde fica o rosto RELATIVO ao sprite,
// medido em fração da largura(w)/altura(h) do desenho. Calibra-se 1 vez.
var FACE = {
  byte: { cx:0.50, cy:0.30, eyeDx:0.13, eyeR:0.045,
          mouthDy:0.14, mouthW:0.22 }
};

function falarComBoca(texto, personagem, emocao){
  var V = vida[personagem];
  V.emocao = emocao || "neutro";
  balaoMostrar(texto, personagem);           // balão visual (já existe)
  if(!audioOn || !window.speechSynthesis){    // sem voz: só balão, mas
    V.falando = true;                          // ainda mexe a boca um pouco
    V.tempoMudo = Math.max(1.4, texto.length*0.06); // "fala" estimada
    return;
  }
  try{ speechSynthesis.cancel(); }catch(e){}
  var u = new SpeechSynthesisUtterance(texto);
  u.lang="pt-BR"; u.rate=0.98; u.pitch=1.12;
  var v=vozPt(); if(v)u.voice=v;
  u.onstart    = function(){ V.falando=true; };
  u.onend      = function(){ V.falando=false; V.bocaAlvo=0; };
  u.onerror    = function(){ V.falando=false; V.bocaAlvo=0; };
  u.onboundary = function(){ V.kick=1; };      // empurrão extra (quando existe)
  try{ speechSynthesis.speak(u); }catch(e){}
}

// --- NO LOOP DE LÓGICA, para cada personagem "p" ---
function atualizarRosto(V, dt){
  // BOCA
  if(V.falando){
    V.mouthPhase += dt * (2*Math.PI*7);              // ~7 batidas/seg
    var base = 0.5 + 0.5*Math.sin(V.mouthPhase);
    V.kick = Math.max(0, V.kick - dt*4);
    V.bocaAlvo = Math.min(1, base*0.7 + V.kick*0.5 + Math.random()*0.1);
    if(V.tempoMudo!=null){ V.tempoMudo-=dt; if(V.tempoMudo<=0){V.falando=false;V.bocaAlvo=0;V.tempoMudo=null;} }
  } else V.bocaAlvo = 0;
  V.bocaAbertura += (V.bocaAlvo - V.bocaAbertura) * Math.min(1, dt*18); // suaviza

  // PISCAR
  V.proxPisca -= dt;
  if(V.proxPisca<=0){ V.piscaT=0.12; V.proxPisca = 3 + Math.random()*3; }
  if(V.piscaT>0) V.piscaT -= dt;
  V.olho = (V.piscaT>0) ? 0 : 1;                       // 0 = fechado
}

// --- NO DESENHO, DENTRO do transform do sprite, DEPOIS do drawImage ---
function desenhaRosto(V, w, h){
  var cxf = (FACE.byte.cx-0.5)*w;                      // centro do rosto
  var cyf = -h + FACE.byte.cy*h;
  var ex  = FACE.byte.eyeDx*w, er = FACE.byte.eyeR*h;
  // OLHOS (piscar = achatar a altura para ~0)
  var oy = V.olho*er + (1-V.olho)*1;
  desenhaOlho(cxf-ex, cyf, er, oy, V.emocao);
  desenhaOlho(cxf+ex, cyf, er, oy, V.emocao);
  // BOCA (abre conforme bocaAbertura; curva conforme emoção)
  desenhaBoca(cxf, cyf+FACE.byte.mouthDy*h, FACE.byte.mouthW*w,
              V.bocaAbertura, V.emocao);
}
```

> **Detalhe importante do "espelho":** o sprite é desenhado com
> `cx.scale(byte.dir*..., ...)`. Como o rosto é desenhado **dentro** do mesmo
> transform, ele vira junto quando Byte olha para a esquerda — automático, sem
> código extra.

### Como gerar as POSES por IA (quando for o Caminho B)

Para NPCs humanos, peça ao workflow `gerar-imagens.yml` uma **folha de
personagem** (character sheet): o MESMO personagem, mesma pose, mesma luz e
mesmo tamanho, mudando **só** a boca e os olhos — 4 quadros: (1) neutro/boca
fechada, (2) boca aberta falando, (3) olhos fechados piscando, (4) sorrindo.
Frase-chave no prompt: *"mesmo personagem, mesma posição e iluminação, apenas a
boca e os olhos mudam"*. Depois:

1. Recorte cada quadro com o **mesmo** script Pillow já usado (flood-fill +
   erosão) que recorta o Byte.
2. **Alinhe pela caixa delimitadora** (`getbbox`) para os quadros sobreporem
   perfeitos — senão o rosto "pula".
3. Salve leve (`optimize`). Prefira exportar **só a faixa da boca/olhos** como
   overlay pequeno, não o corpo inteiro repetido, para não pesar.
4. No jogo, troque a fonte do `drawImage` conforme `V.bocaAbertura>0.5` e
   `V.olho===0`.

### Custo e integração (honesto)

- **Peso:** Caminho A = **zero KB** extra. Caminho B = ~3–4 sprites por
  personagem (só onde valer a pena).
- **Desempenho:** por quadro, é 1 curva + 2 elipses por personagem que fala —
  trivial no Canvas 2D, roda liso em Windows 7. Salvaguarda: só desenhar o
  rosto quando o personagem estiver na tela.
- **Onde encaixa nos arquivos reais:** trocar `falar()` por `falarComBoca()` e
  chamá-la de `balao()`; adicionar `atualizarRosto()` no laço `logica()`;
  chamar `desenhaRosto()` no fim de `desenhaByte()` (e dentro de `npc()` na
  taberna). Nada disso existe hoje — é o trabalho a fazer.

### Resumo construído × a-fazer

**Já vivo:** respiração idle, bob de caminhada, NPCs que respiram, balão de fala
e narração pt-BR com destravamento de áudio.

**A construir:** lip-sync (boca), piscar, emoções, o rosto desenhado por código
sobre o sprite, e a cartela de poses por IA com recorte alinhado — além dos
handlers `onstart/onend/onboundary` no utterance, que o `falar()` atual ainda
não usa.

---

## Produção & Sustentabilidade — a Linha de Montagem do EducaVerso

> Documento ancorado nos arquivos reais do repositório (workflows em
> `.github/workflows/` e os `build_*.py` dos demos). Onde digo "funciona", é
> porque existe no disco e já rodou; onde digo "falta", é visão/a-fazer.

### O princípio: por que a linha de montagem sustenta o modelo

O EducaVerso troca a **confeitaria artesanal** (cada mundo desenhado à mão,
pesado, lindo mas que não escala) por uma **linha de montagem**: um **motor
único** (o Canvas 2D dos demos) mais **arte gerada por IA** (tiles e sprites)
mais **dados** (o mapa). Fazer um mundo novo deixa de ser "pintar tudo de novo"
e vira "gerar uns tiles + trocar o mapa". Isso é o que os pareceres em
`_plano/plano_producao.md` chamam de sair da **criação** (cara) para a
**produção em série** (barata).

A conta física comprova. O mundo artesanal `_pub_confeitaria/mundo/index.html`
pesa **~3,0 MB** num único arquivo. Os dois mundos de tiles do EducaVerso, já
autossuficientes e com clima/câmera/NPCs/voz, pesam **~512 KB**
(`_demos/educaverso/index.html`) e **~779 KB**
(`_demos/educaverso/taberna/index.html`) — de **4 a 6 vezes mais leves**, o que
importa muito no PC Windows 7, 1024×768, da escola.

### As 4 estações da linha de montagem (como REALMENTE funciona)

**Estação 1 — Descrever o asset e mandar a IA gerar (workflow `gerar-imagens.yml`)**

A geração NÃO roda no navegador da criança nem no chat (a rede do chat é
travada — dá 403, e isso é normal). Ela roda num **workflow do GitHub Actions**,
acionado por `workflow_dispatch`. O especialista descreve a imagem no input
`prompt`, dá um `nome`, e escolhe o `modelo`:

- **`pollinations` (PADRÃO, GRÁTIS, sem chave):** monta a URL
  `image.pollinations.ai/prompt/<texto>?...&model=flux` e baixa o PNG. É o
  caminho barato para tiles e cenários.
- **`gemini` (usa o secret `GEMINI_API_KEY`):** tenta em cascata
  `gemini-2.5-flash-image` → `-preview` →
  `gemini-2.0-flash-preview-image-generation`. Sua vantagem é **EDITAR uma
  imagem base** (input `base` = caminho no repo): mantém o mesmo personagem e
  muda só o que o prompt pedir (ex.: "boca aberta", "pernas juntas") — chave
  para gerar poses coerentes do Byte.

O workflow salva em `_novo/<nome>.png` e **commita sozinho** (laço de
`git pull --rebase` + `git push`, até 6 tentativas, para não colidir). Depois é
só `git pull` local e o asset está na mão. Há ainda um **Plano B** para quando a
conexão MCP não está disponível: o `finalizar.yml` dispara por marcadores na
mensagem do commit (`[imagens]`, `[medalha]`, `[audio]`, `[publicar]`) e gera
lotes a partir de `_gerar_imagens.json`.

**Estação 2 — Recortar o fundo com Python/Pillow (flood-fill + anti-franja + autocrop)**

O recorte é 100% local, com Pillow + scipy. Há duas receitas reais, conforme a
cor do fundo:

- **Fundo claro/uniforme — `_ferramentas/cortar_sprites.py`** (o script oficial
  de sprites, `função recorta_raw`): detecta o fundo (`min>240` e `máx−mín<14`),
  rotula-o e marca como fundo **tudo que encosta nas bordas** (o flood-fill das
  bordas). O objeto é o que **não** está ligado à borda; aplica `binary_opening`
  + `binary_fill_holes` e fica com o **maior componente**. A **anti-franja** vem
  de uma erosão de 2 px que remove o anel claro do antialias
  (`keep & ~erosão & mín>232`). O **autocrop** é o `min/max` de `ys`/`xs`. Um
  detalhe caro que já foi resolvido: `normaliza_set` põe todos os quadros de uma
  cartela num **canvas comum** (pés alinhados, centrado no x) — é a cura do
  "piscar" (nenhum quadro muda de tamanho entre frames) — e só então
  redimensiona por LANCZOS.
- **Fundo preto (cartelas do Gemini) — `_novo/recortar.py`:** usa o canal máximo
  (`> limiar`), componentes conectados, e limpa o anel escuro do antialias com
  `grey_erosion` + `gaussian_filter`.

**Estação 3 — Otimizar e embutir em base64 (o HTML autossuficiente)**

Aqui moram os `build_*.py`. Eles leem cada PNG, transformam em
`data:image/png;base64,...` e **substituem marcadores** no HTML (`__GRAMA__`,
`__AGUA__`, `__BYTE__`, ...). O resultado é **um único arquivo HTML** que não
faz nenhuma requisição externa depois de carregado — perfeito para PC velho e
para o modelo "portal leve". No `build_premium.py` (Mundo Vivo do Byte) são 5
tiles/sprites virando um HTML de ~512 KB; no `build_taberna.py`, 9 assets num
HTML de ~779 KB. A otimização de imagem vem do próprio recorte (`uri()` em
`cortar_sprites.py`: `quantize(255, FASTOCTREE)` + `save(PNG, optimize=True)`),
deixando cada sprite na casa das dezenas de KB.

O truque de leveza do motor: os tiles de chão/água/areia entram como **padrões
repetidos** (`createPattern(..., "repeat")`) — poucas imagens pequenas preenchem
um mundo de 2200×1500. Não é uma imagem gigante do mapa inteiro; é um mosaico
barato.

**Estação 4 — Voz e narração (workflows `gerar-audio.yml` + `otimizar-audio.yml`)**

Para voz **gravada** (falas fixas), o `gerar-audio.yml` usa **edge-tts**
(Microsoft, natural, grátis): `male` = `pt-BR-AntonioNeural`, `male2` =
`Donato`, `female` = `Francisca`; ainda há StreamElements/Polly (Ricardo,
Camila), Google Translate TTS como reserva e Gemini TTS (pago) como opção. Um
**lote** (JSON no input `lote` ou o arquivo `_lote_falas.json`) gera muitas
falas de uma vez, cada uma virando `_audio/<id>.mp3`. Depois o
`otimizar-audio.yml` recomprime tudo (ffmpeg, mono 22 kHz, 24 kbps) para caber
muita fala embutida sem inchar o HTML. Esses MP3 entram como base64 e tocam num
`<audio>`, **sem depender da voz robótica** do navegador. (Nos demos atuais a
narração ao vivo ainda usa Web Speech — `função falar()`; o áudio gravado é o
caminho para as falas fixas do enunciado.)

### A conta da sustentabilidade (minutos e ~grátis, não reais)

| Item | Custo real | Peso final |
|---|---|---|
| Mundo novo (tema) | ~5–8 tiles no Pollinations (grátis) + trocar o mapa | ~0,5 MB de HTML |
| Personagem novo | 1 sprite (ou cartela de poses, editada no Gemini) | ~40 KB |
| Voz das falas | lote no edge-tts (grátis) + recompressão | KB por fala |
| Infra | minutos de GitHub Actions (grátis em repo público) | — |

Comparado ao artesanal: um mundo da confeitaria era **~3,0 MB feitos à mão** e,
para fazer o **próximo**, refazia-se quase tudo (criação pura, 3–5× a cota de
uma sessão de produção, segundo `plano_producao.md`). No EducaVerso, o **motor
é o mesmo** (`build_*.py` + o JS do canvas); um mundo novo reaproveita tudo e só
troca **tiles + mapa + áudio**. Por isso o custo por mundo **despenca** depois
que o motor está pronto — exatamente o desenho "motor único, bairros baratos".

### Construído × a-fazer (honesto)

**Já funciona:** os três workflows de geração (`gerar-imagens.yml`,
`gerar-audio.yml`, `finalizar.yml`) com commit automático; a otimização de áudio
(`otimizar-audio.yml`); os dois recortadores Pillow reais (fundo claro e fundo
preto) com anti-franja e canvas comum; os dois injetores base64
(`build_premium.py`, `build_taberna.py`) produzindo HTML autossuficiente leve; e
dois mundos de tiles provando o modelo.

**Falta para virar uma fábrica de verdade:** um **injetor por template** (hoje
cada `build_*.py` é específico do seu mundo, com marcadores no braço); uma
**biblioteca de tiles reutilizáveis** indexada (os tiles vivem soltos dentro da
pasta de cada demo, não num catálogo compartilhado); o **mapa como dado
externo** trocável (hoje o mapa — bordas, array de árvores, escolha de tile —
está fixo no JS, então "trocar o mapa" ainda é editar código); um **recortador
único parametrizado** (os scripts têm caminhos/limiares por sessão — o próprio
`cortar_sprites.py` avisa isso no cabeçalho); e um **gate de tamanho/QA
automático** do HTML antes de publicar. Enquanto isso, a cola entre as estações
(acionar workflow → `git pull` → rodar Python local → conferir com o Marcos)
continua manual.

---

## Pedagogia — o aprendizado que mora dentro do mundo

> Regra de ouro deste projeto: **a pedagogia é do professor Marcos**. A IA e o
> motor cuidam do *mundo* (arte, movimento, voz, clima); o *conteúdo* — qual
> habilidade, qual pergunta, qual explicação do erro — é decisão pedagógica
> humana, alinhada à BNCC. A IA nunca inventa o que se ensina.

O EducaVerso troca o "quiz ilustrado" por um princípio construcionista
(Papert): a criança **age no mundo, o mundo reage na hora, e ela vê a
consequência**. A matemática (ou qualquer conteúdo) deixa de ser a *pergunta* e
vira a *ferramenta* para resolver algo que um personagem precisa. Fundamentação
registrada em `_plano/plano_pedagogia.md` e `MUNDO-VIVO-ESPINHA.md`.

### 1. A atividade mora num LUGAR ou num PERSONAGEM (nunca num menu de quiz)

O princípio-espinha (do `MUNDO-VIVO-ESPINHA.md`) é literal: **"Espaço, não menu
— desafios são LUGARES; personagens têm desejo (missão = pedido)"**. A criança
não "abre a atividade 3": ela anda até a confeitaria, o Chef pede ajuda por
balão e voz, e o pedido *é* o desafio.

- **Já construído (motor de missões):** o protótipo da Confeitaria
  (`_pub_confeitaria/proto/index.html`) implementa o motor micromundo com 5
  modos concretos, catalogados em `MUNDO-VIVO-MOTOR.md`:
  - **Modo A — repartir concreto** (`mmCenaA`): arrasta OU toca no prato;
    validação viva.
  - **Modo A2 — agrupar** (`mmCenaG`): a caixa fecha sozinha ao encher; o número
    de caixas *é* a resposta — "não tem como errar, o mundo computa".
  - **Modo A-montar** (fonte infinita): a criança enche cada grupo; o total é
    revelado no fim como descoberta (multiplicação).
  - **Modo B / Modo D** (dinheiro, proporção): troco, desconto, preço unitário.
- **Já construído (personagem com desejo + interação no lugar):** nas demos
  EducaVerso em tiles (`_demos/educaverso/index.html` e
  `_demos/educaverso/taberna/index.html`), o Byte e os NPCs (taberneiro, gato)
  têm balão de fala + narração por voz, e o mundo tem porta de verdade, chave e
  inventário.
- **A fazer (a costura que falta):** hoje, na demo em tiles, **falar com o NPC
  ainda só conversa — ainda não abre uma missão do motor**. O desafio
  pedagógico está pronto no protótipo artesanal antigo (Confeitaria), e o mundo
  leve novo (tiles + IA) está pronto separado. O próximo passo é **plugar o
  motor de missões dentro do NPC/lugar do mundo em tiles** ("falar com o
  taberneiro" → abre `mmCenaA`).

### 2. Conhecimento como FERRAMENTA para avançar

A porta trancada da Taberna só abre com a chave; a chave é um item do
inventário. Essa mecânica de **"objeto/saber destrava o avanço"** já funciona na
demo (`taberna/build_taberna.py`: `inv.chave`, porta trancada → aberta). A visão
pedagógica é ligar essa chave ao **acerto de um desafio** — a recompensa por
resolver o pedido do Chef é o que abre o próximo lugar.

- **Já construído:** inventário, chave, porta que abre com o item, transição
  entre cenas (fora/dentro).
- **A fazer:** amarrar a recompensa (chave/item) ao **resultado de uma missão do
  motor**, não só à exploração.

### 3. ERRO = consequência no mundo, não X vermelho

Princípio "erro construtivo" (Kamii), já implementado no protótipo Confeitaria e
documentado no `MANUAL-MESTRE.md`:

- No **modo A**, se um prato fica com quantidade desigual, a **carinha
  entristece 😞 e treme** — e a criança **conserta ela mesma**. Sem "X", sem
  sistema de vidas que trave o fluxo, sem cronômetro.
- O **"Pratinho do Chef"** (`sobra:true`) mostra o **resto visível** da divisão;
  no acerto, o Chef "come" a sobra — o resto vira parte da história, não erro.
- **Consequência permanente:** a placa consertada *fica* consertada, a Dona Bela
  passa a acenar — o mundo guarda memória do progresso.
- **Acessibilidade do erro:** o "entristecer" usa carinha + tremida, **não só
  cor** (cuidado com daltonismo).

### 4. Avaliação INVISÍVEL + painel do professor

A avaliação nasce do jogo, sem prova nem folha. Funções `acerto()` / `erro()`
registram, por missão: acertou de primeira, errou-e-consertou, quantas
tentativas, em qual habilidade BNCC.

- **Já construído:** `acerto()`/`erro()` no motor; **modo professor por código
  `1275@`** que destrava o painel dentro do próprio jogo; diagnóstico e streak
  como mérito (nunca sorte).
- **A fazer (registro persistente e painel completo):** hoje o save é **local,
  de 1 aula (~70 min)**. Falta o **save por aluno no Firebase**
  (`/mundos/<turma>/<aluno>`, ~2 KB) e o **painel ao vivo + relatório anual** que
  mostra o mapa de habilidades por aluno (verde/amarelo/vermelho) e por turma. A
  leitura é **para ensinar melhor, nunca para ranquear**: vermelho = "aqui eu
  preciso ajudar". Roteiro de intervenção dirigida detalhado em
  `_plano/plano_pedagogia.md §4`.
- **Diferencial registrado:** como a criança *conserta* o erro dentro do mundo,
  o professor vê "quem errou e superou sozinho" vs "quem travou" — informação
  que uma prova de certo/errado nunca dá.

### 5. Não-leitores: ícone + voz + cor, tudo narrado

Regra sagrada do projeto — **nenhuma informação essencial é só-texto**.

- **Já construído:** narração por voz (Web Speech, pt-BR) em toda fala do mundo
  e das demos; nas atividades premium há voz **pré-gravada** (edge-tts, workflow
  `gerar-audio.yml`) para não depender de TTS robótico. Botões que abrem com
  narração começam desabilitados ("🔊 Ouvindo...") e só liberam quando a fala
  termina, para a criança não pular a instrução.
- **Regra pedagógica da narração:** a voz **lê só o enunciado** ao abrir o
  desafio; a explicação/resposta só é narrada **depois** que a criança responde
  (luta produtiva — a narração nunca entrega a resposta).
- Alvos grandes, contraste alto, ícones grandes; a informação nunca depende só
  de cor.

### 6. Alinhamento BNCC por ano e campanhas por semestre

O currículo do ano **é** o mapa do mundo: cada **bimestre é um bairro** que
"amanhece aberto" no mesmo link. A revisão espaçada está desenhada na
*geografia* (o Banco reusa a divisão da Confeitaria) — a criança revisa sem
perceber.

- **Já construído:** mapeamento BNCC completo e exemplar do **5º ano de
  Matemática** (4 bairros = 4 bimestres), com cada missão amarrada a um código
  EF05MA e a um modo do motor (`_plano/plano_pedagogia.md §3`; tabela
  BNCC→missão→modo em `MUNDO-VIVO-MOTOR.md`). O **Bairro 2 — Confeitaria
  (frações/divisão)** é a implementação de referência que já roda.
- **A fazer:** construir os outros três bairros (Mercado, Banco, Parque de
  Obras) reusando o mesmo motor; mapear BNCC dos **demais anos e disciplinas**
  (hoje só 5º Mat está detalhado); publicar as campanhas **incrementalmente por
  bimestre**.

### 7. Recompensas por marco (inventário e mascote que evolui)

- **Já construído:** inventário com item coletável (chave) na demo da Taberna; o
  mascote **Byte** acompanha, faz balão e narra — na visão original, ele **faz
  pensar, nunca entrega a resposta**.
- **A fazer:** o **bichinho/ovo que evolui** com o progresso (marco → evolução
  visível), amarrado ao save persistente; recompensas de inventário por marco de
  aprendizagem; fechamento anual com certificado.

### Resumo honesto do estado pedagógico

Estão **prontos e funcionando** os fundamentos: o motor de missões concretas
(Confeitaria), o erro-como-consequência, o `acerto()/erro()`, o modo professor
`1275@`, a narração para não-leitores e o mapeamento BNCC do 5º ano. O mundo
leve novo (tiles + IA) também está pronto, com NPCs vivos, inventário e chave.
**O elo que falta** é costurar os dois: fazer o **desafio do motor abrir a
partir do NPC/lugar** no mundo em tiles, e trocar o **save de 70 min** pelo
**save por aluno no Firebase** que alimenta o **painel do professor ao vivo** —
sem isso não há avaliação invisível ao longo do ano nem campanhas que atravessam
o semestre.

---

## A Fábrica de Mundos — escalar por TEMA + TURMA

### A ideia em uma frase

Entra um pedido do professor — **TEMA + TURMA + CONTEÚDO** — e sai um **mundo
publicado** (repositório próprio, link no ar e card no hub "Ilhas do Saber"). O
segredo é não construir cada mundo à mão. Um mundo inteiro passa a ser descrito
em **um único arquivo de dados** (o **TEMA-SPEC**, um JSON): paleta, tiles a
gerar, mapa, personagens, NPCs, falas e as atividades. Um **montador** pega o
**motor único** (reutilizável) e o TEMA-SPEC e monta o mundo. Trocar de tema =
gerar uns tiles novos + trocar os dados. Personagem novo = gerar um sprite.
Rápido, leve e sustentável.

Isso é o "melhor dos dois mundos" na prática: a **arte premium** (pintada por
IA, reaproveitada) continua, mas o **motor não se repete** — ele é escrito uma
vez e alimentado por dados.

### Como NASCE um mundo novo (a linha de montagem)

O documento de referência é `FABRICA-DE-MUNDOS.md`, escrito **depois** de
dissecar o motor real da confeitaria e **corrigido item a item** por um revisor
cético (os 12 "furos" viraram itens explícitos). A linha de montagem tem 17
passos, mas o essencial para o professor entender é o fluxo com **3 aprovações**:

1. **Pedido (professor):** informa TEMA + TURMA + conteúdo + BNCC + faixa
   numérica. Isso vira o bloco `entrada` do TEMA-SPEC. A pedagogia é
   irredutível — só o professor decide.
2. **Rascunho das missões/paradas** → **1ª aprovação do professor** (o pacote de
   fases e a progressão de dificuldade).
3. **Compilar o TEMA-SPEC em prompts de imagem** e **gerar as cartelas (PNGs)**
   nos workflows (Gemini/Pollinations).
4. **Aprovar as cartelas** (a arte) → **2ª aprovação do professor** (o visual:
   mascote, fachadas, itens). O que for reprovado volta para regerar.
5. **Cortar sprites, medir as fachadas, montar o HTML, extrair as falas, gerar
   os MP3 de narração** e rodar o QA técnico e visual.
6. **Aprovar o mundo jogável** → **3ª aprovação do professor** (testado de
   verdade, inclusive "errando de propósito" para ver a consequência).
7. **Publicar** o repositório (`fabrica.yml`) e **inserir o card no hub** (com o
   mascote da própria atividade) → o professor confere o mascote e a posição.

**Regra de ouro:** o professor **decide a pedagogia e aprova o visual**; a
fábrica (workflows + montador) engole o resto mecânico. Restam **3 aprovações**
(missões · arte · mundo jogável) + a conferência do mascote do card.

### O TEMA-SPEC — o "molde" de um mundo

O arquivo `_fabrica_mundos/TEMA-EXEMPLO-mar-3ano.json` é o exemplo completo e já
corrigido. **Nada do motor aparece nele** — nenhuma função, nenhuma física, só
**dados**. Os blocos:

- `entrada` — as 5 alavancas do professor (tema, turma, conteúdo, BNCC, faixa
  numérica).
- `meta` — nome do mundo, slug, chave de save, textos das telas de abertura,
  dados do card do hub.
- `paleta` — cores do mundo e do splash.
- `mascote` — nome, papel, poses e o **prompt** que gera a cartela do
  personagem.
- `lexico` — os itens (peixe, moeda, pérola...) e recipientes (rede, baú,
  saco...) do tema; alimenta a arte **e** a lógica de contar grupos.
- `niveis` — as 5 patentes que o aluno sobe (ex.: Grumete → Marujo → ... no tema
  pirata).
- `falas_motor`, `diag`, `falas_mapa`, `falas_intro`, `balao_mapa`, `final` —
  todas as falas e textos (visíveis e narrados), inclusive o diagnóstico do 1º
  erro e o certificado final.
- `assets_cenario` — prompts dos fundos e objetos globais (capa, troféu, céu,
  chão).
- `paradas[]` — cada fase: ilha, título, habilidade, curiosidade, prompts de
  fachada e interior, história e as **missões** (os desafios matemáticos).

**Descoberta importante que sustenta a escala:** o motor da confeitaria **já
roteia** os modos de multiplicação, proporção, divisão e dinheiro. Um mundo de
multiplicação do 3º ano **não exige um motor novo** — exige o TEMA-SPEC certo.
Cada missão de "×" carrega um campo `ng` (número de grupos) para o motor montar
a cena certa a partir dos dados, sem depender de vocabulário fixo.

### O que já existe (prova de conceito real)

- O **TEMA-SPEC de exemplo** — "Mar dos Números" (piratas, 3º ano,
  multiplicação), com 11 paradas, léxico pirata, níveis, falas e prompts
  completos. É o molde de referência, já revisado.
- O **motor único** existe e funciona: é o motor "Mundo Vivo" da confeitaria
  (`_pub_confeitaria/mundo/index.html`), dissecado linha a linha no
  FABRICA-DE-MUNDOS.md.
- Os **demos EducaVerso** (`_demos/educaverso/index.html` e
  `.../taberna/index.html`) provam o modelo **tile + arte de IA + motor leve**:
  câmera, clima, dia/noite, colisão, NPCs vivos, gerenciador de cenas,
  inventário, narração por voz. São a prova viva de que o "mundo de tiles leves"
  roda no PC antigo da escola.
- O **pipeline de geração** (workflows `gerar-imagens.yml`, `gerar-audio.yml`,
  `finalizar.yml`, `fabrica.yml`, `atualizar.yml`, `deploy-pages.yml`,
  `republicar-limpo.yml`) já gera arte, gera narração, publica repositórios e
  conserta builds.
- A **ferramenta de corte de sprites** (`_ferramentas/cortar_sprites.py`) já
  normaliza as poses do personagem (pés alinhados, sem "piscar").

### O que falta para virar "quase um botão"

O FABRICA-DE-MUNDOS.md é honesto: hoje **não dá para fabricar de verdade só
trocando os dados**. Faltam as "costuras" (as 5 primeiras são bloqueantes e
tocam o motor):

1. **Contagem de grupos guiada por dados** — hoje o motor conta grupos por uma
   lista de palavras da confeitaria. "3 redes de 5 peixes" viraria "5 redes de
   3" na tela. Precisa ler o campo `ng`/o léxico.
2. **Léxico guiado por dados** — tirar do motor os nomes fixos (brigadeiro,
   cupcake, "Bandeja") e fazê-lo ler o `lexico` do TEMA-SPEC.
3. **Injetar as falas do motor** (`MMF` e `DIAG`) a partir do spec — senão um
   mundo de multiplicação daria dica de "dividir" no erro.
4. **`extrair_falas.py`** — a ferramenta que pega a fala **exata** em tempo de
   execução para casar com o áudio. **Ainda não existe** (risco de uma fala
   virar silêncio em sala).
5. **As "zonas órfãs"** (splash, título, níveis, certificado, avisos) precisam
   vir todas do spec — senão o mundo pirata abriria escrito "A RUAZINHA DOS
   DOCES" e premiaria com "Mestre da Divisão".
6. **O MONTADOR/injetor por âncora** — o script que pega o motor + o TEMA-SPEC e
   monta o HTML autossuficiente. **Ainda não existe** (é o coração da
   automação).
7. **A grade de mapa editável** e a **conferência visual das fachadas** (medir
   onde fica a porta) — hoje é inspeção humana, ainda não roteirizável.

**Estimativa honesta:** descolar as costuras 1-5 e construir o montador é o
**único gasto real de engenharia** (feito uma vez, com modelo forte). Feito
isso, cada mundo novo passa a ser **~2-4 h** de trabalho (escrever o TEMA-SPEC +
revisar), **3 aprovações do professor** e os workflows engolindo o resto — API
barata (Gemini para ~15-25 cartelas + narração edge-tts grátis).

---

## A Fábrica de Atividades por currículo + Diretrizes do professor Marcos

> Esta seção foi acrescentada **depois** da rodada dos especialistas, para registrar
> requisitos que o professor trouxe e que são o **coração pedagógico** do EducaVerso.
> Fonte permanente: `MEMORIA-DO-PROJETO.md`.

### 1. A Fábrica de ATIVIDADES (irmã da Fábrica de Mundos)
Se a **Fábrica de Mundos** cria o *cenário*, a **Fábrica de Atividades** preenche
com o *aprendizado alinhado ao currículo* — **entra um objetivo do currículo, sai uma
atividade pronta e inserida no mundo**.

- **Fontes de currículo:** BNCC geral, **Computação BNCC** (já há o `ATIVIDADE-COMPUTACAO.md`),
  ou o **currículo de Blumenau** (já há o workflow `.github/workflows/baixar-curriculo.yml`,
  que baixa o PDF e extrai o texto para **ancorar a IA** no objetivo real — ela não inventa
  a habilidade). O professor escolhe **fonte + ano/turma + habilidade**.
- **Como monta:** a IA lê o objetivo real → escolhe a **mecânica** (do catálogo de
  interatividades) → cria o conteúdo/desafios → **embrulha na narrativa do mundo** (um
  personagem/lugar) → gera arte (pipeline de imagem) e voz.
- **Portão de qualidade:** a IA **rascunha**; o professor **aprova** (as 3 aprovações:
  missões/pedagogia, arte, jogável). "Automático" **sem** perder a mão pedagógica.
- **Inserção:** a atividade vira um **ponto/NPC/gatilho** no mundo; o resultado alimenta a
  avaliação descritiva.
- **Construído × a-fazer:** *existe* — `baixar-curriculo.yml`, `ATIVIDADE-COMPUTACAO.md`, o
  catálogo de mecânicas, o pipeline; *falta* — o **montador** que casa
  currículo → mecânica → mundo → faixa de forma semiautomática.

### 2. Adequação à TURMA (faixa etária) — regra obrigatória
A partir de **DISCIPLINA + TEMA + TURMA**, tudo se ajusta à idade: cenário, personagens,
dificuldade, mecânica, narração e missões.
- **Pré / 1º-2º (NÃO leitores):** só **ícone + voz + cor**; missões curtas de 1 passo; muita recompensa.
- **3º-5º:** leitura simples; missões de poucos passos; mais exploração.
- **6º-9º:** missões **multi-etapas**; mais autonomia e desafio.
A IA rascunha adequado à faixa; o professor confirma.

### 3. Aluno ATIVO/protagonista + as fases ENTREGAM o objetivo (gating)
- **O aluno CONSTRÓI** — monta a máquina, programa o robô, constrói a ponte, cria a solução.
  Nunca só assiste ou escolhe alternativa. **A construção só funciona se o conceito estiver
  certo → construir já é provar que entendeu.**
- **Gating no objetivo:** cada fase nasce de um objetivo do currículo e **só é concluída
  quando o aluno demonstra aquele objetivo** (a ponte só abre / o robô só chega / o navio só
  zarpa quando está correto). Não se "passa sem aprender".
- **Medição:** a avaliação invisível registra quem **alcançou** o objetivo e quem precisa de
  apoio → relatório descritivo para o professor **agir**.
- **Ciclo:** construir (ativo) → travar no objetivo (garante) → registrar (avaliação) → o
  professor vê quem alcançou.

### 4. Aprender SEM perceber que está estudando (a regra-mãe)
Reforço da regra anti-quiz: a criança sente **jogo primeiro, lição nunca explícita**. O
conhecimento é a **ferramenta para vencer a missão**, não a pergunta. Ex.: para ganhar a
chave do taberneiro, ela **organiza 4 prateleiras com 3 barris** (multiplicação) — ela achou
que **ajudou um amigo e ganhou um tesouro**, não que "fez uma continha".

### 5. O mascote do próprio aluno (pertencimento)
Além do Byte (guia), o aluno tem o **seu próprio mascote/avatar** que o acompanha; o Byte e
os NPCs interagem com ele, e a narração **fala o nome do estudante** ("Muito bem, João!").
Pertencimento + emoção = engajamento. *(A-fazer: modelar o avatar do aluno e sua seleção no
login por código de turma.)*

---

## Roadmap & Produto — do que existe hoje ao EducaVerso em sala

> Escrito como líder de produto, com honestidade. Separo com rigor o que **já
> está construído e funciona** do que ainda é **visão / a-fazer**. Nada de
> promessa vazia: cada fase entrega algo **jogável de verdade** na turma, e a
> próxima só começa depois que a anterior passou pela prova real (crianças
> usando).

### 1. Onde estamos hoje (o ponto de partida honesto)

Temos **duas demos jogáveis e autossuficientes**, um **pipeline de geração de
arte e voz que funciona de verdade** (roda nos workflows do GitHub, não no
navegador da criança) e uma **biblioteca grande de manuais e planos**. É um
patrimônio real e raro para uma escola pública — mas ainda é um **protótipo
técnico**, não um produto que a turma usa toda semana.

O ponto mais importante para ser honesto: **o "motor único" ainda é a tese, não
o código**. As duas demos (`_demos/educaverso/index.html`, ~504 KB, e
`_demos/educaverso/taberna/index.html`, ~764 KB) são hoje arquivos **separados
que repetem o motor cada um**. A promessa "trocar tema = trocar tiles + mapa"
ainda não está extraída num motor reaproveitável — é o primeiro grande trabalho
de engenharia do roadmap. Além disso, **nenhuma demo tem login, save ou painel
ligado** ainda: elas rodam, encantam, mas não lembram da criança nem contam
nada ao professor.

### 2. Princípios de produto (o que decide cada escolha)

- **Cada fase entrega algo jogável.** Nunca "seis meses construindo encanamento
  invisível". A régua é: *dá para levar para a turma no fim da fase?*
- **Leve acima de tudo.** PC com Windows 7, navegador antigo, 1024×768, Canvas
  2D, sem 3D, sem engine pesada. A geração de IA fica nos workflows; a criança
  só recebe HTML leve.
- **Concretude, nunca quiz.** A matéria é **ferramenta** para agir no mundo; a
  conta aparece **depois** da ação, como descoberta. (Regra vinda dos 5
  pareceres em `_plano/`.)
- **Sem conta, sem burocracia.** Entrada por **código de turma + primeiro
  nome** — sem e-mail, sem senha de criança, respeitando LGPD escolar.
- **Escala pelo molde barato.** Mundo novo = uns tiles gerados + um mapa + um
  sprite. Se um mundo novo custar "uma obra de arte artesanal", o modelo falhou.

### 3. As fases (incrementais, cada uma jogável)

#### Fase 0 — Levar as demos para a turma JÁ (validação real) · *sem código novo*
As duas demos existem e rodam. Antes de construir qualquer coisa, **observar 30
minutos de crianças reais** usando o "Mundo do Byte" e "A Taberna do Byte". O
que amaram, onde travaram, o que não entenderam sozinhas. Isso vira o backlog
verdadeiro. **Trava: só coragem e a autorização da direção.**

#### Fase 1 — Extrair o MOTOR único (a fundação técnica)
Transformar o código repetido das duas demos num **motor reaproveitável**
(`motor.js` conceitual): câmera que segue, clima, dia/noite, colisão, balão de
fala, narração por voz, gerenciador de cenas (fora/dentro), inventário. O mundo
passa a ser **dados** (mapa de tiles + lista de objetos + falas), não código.
*Entrega jogável:* recriar as duas demos atuais **a partir do motor**, provando
que agora um mundo novo é só um arquivo de dados novo.

#### Fase 2 — Identidade da criança: turma por código + o nome nas falas
Tela de entrada simples: a criança escolhe/digita o **código da turma** e o
**primeiro nome**. O nome entra na narração ("Muito bem, João!") — alto impacto
emocional, baixo custo técnico (Web Speech já interpola texto). Ainda **sem
servidor**: guarda localmente. *Entrega jogável:* o mundo já chama a criança
pelo nome.

#### Fase 3 — Memória: o mundo lembra dela (save online)
Ligar o **Firebase** (Realtime Database) para salvar progresso por turma/nome. O
gancho emocional central: "cheguei e o mundo **lembrou de mim**, algo mudou
desde ontem". Aqui entra o **Docinho/bichinho** que evolui por marco de
aprendizagem (nunca por assiduidade — regra de ouro anti-medo). *Trava real: o
professor libera as Rules do Firebase e manda a lista de turmas.* *Entrega
jogável:* volto na próxima aula e continuo de onde parei.

#### Fase 4 — Painel do professor (avaliação invisível)
O jogo já registra acerto/erro/tentativa por habilidade; o painel mostra **quem
empacou em quê**, para intervenção dirigida — nunca para ranquear. Já existe um
molde funcional de painel (`_painel/index.html`, feito para outra atividade)
para clonar. *Entrega:* o professor abre um link e vê a turma em tempo real.

#### Fase 5 — Mundos por bimestre (o molde barato provado)
Provar que o motor escala: **um mundo novo com tema diferente** (ex.:
mar/piratas), gerado com poucos tiles novos + mapa novo + um sprite novo.
Depois, os **4 bimestres viram 4 bairros** que "amanhecem abertos" no mesmo
link, mapeados à BNCC. *Entrega:* a matéria do ano inteiro dentro de um universo
só.

#### Fase 6 — Personagens vivos e história com decisões
Incorporar os pedidos do professor (anotados em `MEMORIA-DO-PROJETO.md`): **boca
mexendo ao falar, piscar, respirar, mãos/pernas suaves, ações como "entregar a
chave"**. Caminho técnico: começar por **cartela de poses gerada por IA** (o
pipeline já faz isso), evoluir para recorte em partes só se valer a pena. Mais
um motor de história com escolhas que têm consequência.

#### Fase 7 (futuro) — O aluno CRIA
O modo mais ambicioso e o mais adiado de propósito: a criança monta seu próprio
mundinho com os tiles e sprites existentes, e mostra para a turma/família. É a
virada de "consumir" para "autor" — mas só faz sentido depois que tudo abaixo
estiver sólido e usado.

### 4. Riscos reais e como mitigar

| Risco | Por que dói | Mitigação |
|---|---|---|
| **Build do Pages engasga** ("Page build failed"), sobretudo com histórico `.git` inchado | O mundo não vai ao ar | Modelo **portal leve** (mundo por link, não copiado pra dentro) + `republicar-limpo.yml` (1 commit limpo, force-push) — já testado |
| **Peso** (a confeitaria chegava a ~2,9 MB) | Trava no PC velho / net da escola | Tese dos **tiles**: arte reaproveitada, PNGs otimizados (~50 KB), Canvas 2D. Orçamento fixo por mundo (ex.: teto de ~600 KB) |
| **Consistência dos sprites** (a IA muda o rosto entre poses) | Personagem "vira outro" | Gerar poses **editando a mesma imagem base** (input `base` do `gerar-imagens.yml`), não do zero; conferir cada pose com o professor |
| **Custo de IA** | Insustentável se cada mundo custar caro | Pollinations **grátis** como padrão; Gemini (pago, centavos) só para recorte limpo. Arte é reaproveitada entre mundos |
| **Motor duplicado** (dívida técnica atual) | Cada correção precisa ser feita em N lugares | Fase 1 resolve na raiz: extrair o motor **antes** de multiplicar mundos |
| **Dependência do professor** (Firebase Rules, lista de turmas, BNCC) | Fases 3–5 travam sem isso | Deixar explícito e cedo o que só o professor destrava; não construir às cegas |
| **Web Speech não toca sem gesto** | Criança que não lê fica sem voz | Botão "Ouvir" garantido como 1º gesto; alternativa de MP3 gerado (`gerar-audio.yml`) para falas fixas |

### 5. Os 5 primeiros passos práticos (a partir de amanhã)

1. **Levar as duas demos para uma turma** (Fase 0) e observar 30 min de uso real
   — anotar o que encantou e onde travaram. É a decisão de produto mais barata e
   mais valiosa.
2. **Pedir ao professor as duas chaves que destravam o resto:** liberar as
   **Rules do Firebase** e mandar a **lista de códigos/nomes das turmas**. Sem
   isso, memória e painel não saem do papel.
3. **Começar a extração do motor** (Fase 1): tirar de uma demo o motor comum e
   recriá-la a partir de dados — a fundação de tudo que escala.
4. **Prototipar a tela de entrada** (código de turma + primeiro nome) e **plugar
   o nome na narração** — um ganho emocional enorme por pouco esforço.
5. **Definir com o professor o tema do 2º mundo e o mapa BNCC dos bimestres** —
   para o molde barato (Fase 5) já nascer com destino pedagógico, não
   decorativo.

> Ambicioso, sim — um universo educativo vivo, feito por uma escola pública, que
> lembra de cada criança. Mas viável **porque é incremental**: cada passo
> entrega algo que dá para levar para a sala já na semana seguinte.

---

## Tabela consolidada: CONSTRUÍDO × A-FAZER

> Junta os campos construído/a-fazer das seis seções, num só painel de estado.

### 🔧 Motor único

| ✅ CONSTRUÍDO (roda) | 🔲 A-FAZER (visão) |
|---|---|
| `build_premium.py` + `index.html` (Mundo Vivo): laço dt-real, câmera lerp/clamp, tiles `createPattern`, costa orgânica, clima completo (sol/chuva/neve/tempestade/noite), raios+trovão Web Audio, vento, colisão por eixo, y-sort, poeira, narração pt-BR | Extrair o motor num **arquivo único** (`motor.js`) em vez de copiar-e-colar entre os demos |
| `build_taberna.py` + `index.html` (Taberna): cenas fora/dentro por variável `cena`, fade com `fadeAcao`, colisão injetada por cena, luz de lampião, NPCs vivos, inventário+chave, porta de verdade, gatilhos `[E]`, saída | Gerenciador de cenas **genérico guiado por dados** (registro de cenas), no lugar do `if(cena===...)` |
| Núcleo compartilhado idêntico nos dois (frame/dt, moverByte, desenhaByte/npc, câmera, balão, vozPt/falar/destrava) | **Tilemap em grade** editável por dados (hoje obstáculos são arrays fixos + `edgeMar`) |
| Arte da IA embutida em base64 — HTML autossuficiente, leve para Canvas 2D em PC antigo | Caixa de colisão limpa; pathfinding no clique; diálogo com árvore; unificar clima+luz num módulo |

### 🙂 Personagens vivos

| ✅ CONSTRUÍDO | 🔲 A-FAZER |
|---|---|
| Respiração idle (seno na escala) do Byte; bob de caminhada com sombra que encolhe | **Lip-sync** (boca não mexe): flap por timer `onstart/onend` ~7 batidas/seg |
| NPCs que respiram, cada um em fase diferente (`npc()` na taberna) | **Piscar** (~120ms a cada 3–6s, relógio próprio por personagem) |
| Balão de fala (4,6s) + narração pt-BR com destravamento de áudio no 1º gesto | **Emoções** (feliz/pensando/surpreso) e **rosto desenhado por código** sobre o sprite (tabela FACE) |
| Sprites recortados com fundo transparente pelo pipeline Pillow | Handlers `onstart/onend/onboundary/onerror`; **cartela de poses por IA** alinhada por `getbbox`; `atualizarRosto()`/`desenhaRosto()` |

### 🏭 Produção & sustentabilidade

| ✅ CONSTRUÍDO | 🔲 A-FAZER |
|---|---|
| `gerar-imagens.yml` (Pollinations grátis / Gemini editando base), commit automático; `finalizar.yml` (Plano B por marcadores) | **Injetor por template** genérico (hoje cada `build_*.py` é do seu mundo) |
| `gerar-audio.yml` (edge-tts) + `otimizar-audio.yml` (ffmpeg mono 24k) | **Biblioteca de tiles reutilizáveis** indexada (hoje soltos por demo) |
| `_ferramentas/cortar_sprites.py` (flood-fill, anti-franja, canvas comum) e `_novo/recortar.py` (fundo preto) | **Mapa como dado externo** trocável (hoje fixo no JS) |
| `build_premium.py`/`build_taberna.py` (base64 → HTML autossuficiente); 2 mundos de tiles provando o modelo | Recortador único parametrizado (CLI); **gate de QA/tamanho**; automatizar a cola entre estações |

### 📚 Pedagogia

| ✅ CONSTRUÍDO | 🔲 A-FAZER |
|---|---|
| Motor de missões (5 modos A/A2/A-montar/B/D) rodando na Confeitaria (`_pub_confeitaria/proto/index.html`) | **Costurar desafio ao NPC/lugar** no mundo em tiles (falar → abrir missão do motor) |
| Erro construtivo (carinha triste que treme; Pratinho do Chef mostra o resto); sem X/vidas/cronômetro | Amarrar recompensa (chave/item) ao **acerto** de um desafio |
| `acerto()/erro()` por habilidade; modo professor `1275@`; narração que lê só o enunciado | **Save por aluno no Firebase**; **painel ao vivo + relatório anual** |
| BNCC do 5º ano de Matemática mapeada (4 bairros = 4 bimestres); revisão espaçada na geografia | Outros 3 bairros; BNCC dos demais anos/disciplinas; bichinho que evolui + certificado |

### 🌍 Fábrica de mundos

| ✅ CONSTRUÍDO | 🔲 A-FAZER |
|---|---|
| TEMA-SPEC de exemplo completo e revisado (`_fabrica_mundos/TEMA-EXEMPLO-mar-3ano.json`, 11 paradas) | **O MONTADOR / injetor por âncora** (motor + TEMA-SPEC → HTML) — **não existe** |
| `FABRICA-DE-MUNDOS.md` (17 passos, 12 furos do cético) | `extrair_falas.py` para casar fala↔áudio — **não existe** |
| Motor único de referência (confeitaria) que já roteia ×, proporção, ÷, dinheiro | Costuras bloqueantes 1–3: contar grupos por `ng`/léxico, léxico por dados, injetar falas `MMF`/`DIAG` |
| Pipeline de workflows + `cortar_sprites.py` (poses normalizadas) | Costura 5: zonas órfãs (splash/título/níveis/certificado) do spec; grade de mapa; reparar `finalizar.yml` |

### 🚀 Roadmap & produto

| ✅ CONSTRUÍDO | 🔲 A-FAZER |
|---|---|
| Duas demos jogáveis autossuficientes (Mundo do Byte + Taberna) | Extrair o **motor único** reaproveitável (mundo = dados) |
| Scripts de build (base64 → HTML); pipeline real de arte/voz nos workflows | Tela de entrada por **código de turma + primeiro nome**; nome na narração |
| Infra de publicação (`fabrica`/`atualizar`/`recuperar`/`republicar-limpo`/`deploy-pages`) | **Firebase** (save/memória) — depende do professor; ligar o **painel** ao EducaVerso |
| Molde de painel (`_painel/index.html`); biblioteca de manuais; mascote Byte + spec dos vivos | 2º mundo (mar/piratas) + 4 bimestres/bairros; personagens vivos; modo "aluno cria"; **validação em sala (ainda não feita)** |

---

## Os 5 primeiros passos

1. **Levar as duas demos para uma turma** (Fase 0) e observar 30 min de uso real
   — anotar o que encantou e onde travaram. A decisão de produto mais barata e
   mais valiosa; a única trava é a autorização da direção.
2. **Pedir ao professor as duas chaves que destravam o resto:** liberar as
   **Rules do Firebase** e mandar a **lista de códigos/nomes das turmas**. Sem
   isso, memória (Fase 3) e painel (Fase 4) não saem do papel.
3. **Começar a extração do motor** (Fase 1): tirar de uma demo o motor comum e
   recriá-la a partir de dados — a fundação técnica de tudo que escala, e a cura
   da dívida do "motor duplicado".
4. **Prototipar a tela de entrada** (código de turma + primeiro nome) e **plugar
   o nome na narração** ("Muito bem, João!") — ganho emocional enorme por pouco
   esforço, sem servidor ainda.
5. **Definir com o professor o tema do 2º mundo e o mapa BNCC dos bimestres** —
   para o molde barato (Fase 5) já nascer com destino pedagógico, não
   decorativo. O TEMA-SPEC "Mar dos Números" já serve de rascunho.

---

## Regras permanentes do projeto

Quatro princípios que valem para toda sessão, todo especialista, todo mundo
novo:

1. **Sincronizar antes de agir.** Os workflows commitam sozinhos (arte, áudio,
   publicação). Antes de qualquer trabalho, faça `git pull` para não sobrescrever
   o que a máquina gravou — e confirme o estado real (build `built`, push
   `sha..sha`) em vez de tentar às cegas.
2. **Geração é por workflow, nunca no chat.** A rede do chat é travada (403 é
   normal). Arte (`gerar-imagens.yml`), voz (`gerar-audio.yml`) e publicação
   (`fabrica.yml`/`atualizar.yml`) rodam no GitHub Actions. A criança só recebe
   HTML leve, autossuficiente.
3. **A pedagogia é do professor.** A IA e o motor cuidam do *mundo* (arte,
   movimento, voz, clima); o *conteúdo* — qual habilidade, qual pergunta, qual
   explicação do erro — é decisão humana, alinhada à BNCC. A IA nunca inventa o
   que se ensina, e as 3 aprovações do professor (missões · arte · mundo
   jogável) são irredutíveis.
4. **Honestidade construído × visão.** Nunca vender tese como código. Todo
   documento e toda conversa separam o que **roda de verdade hoje** do que ainda
   é **a-fazer**. Quando algo não existe, ele vai para a coluna "A-FAZER" — sem
   maquiagem.

---

> 📌 **Ponteiro:** os pedidos brutos do professor, o histórico de decisões e as
> anotações de sessão vivem em **`MEMORIA-DO-PROJETO.md`**. Este documento-mestre
> é a visão consolidada; a `MEMORIA-DO-PROJETO.md` é o diário de bordo. Leia os
> dois antes de agir.

*Documento-mestre do EducaVerso — julho/2026. Vivo: atualize a cada marco.*
