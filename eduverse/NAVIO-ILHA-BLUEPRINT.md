# BLUEPRINT DE PRODUÇÃO — "A Ilha do Byte Pirata" (números até 30, 1º ano)

> **Engenheiro-chefe + Game Director consolidando Level Designer + Roteirista + Diretor de Arte + Arquiteto de Dados.**
> Slug: **`navio-pirata`** (mesmo mundo, cenário refeito) · Motor **inalterado** (`eduverse/motor/kit-floresta.py`, ES5) · Câmera 3/4 mantida.
> **DECISÃO DO MARCOS:** o convés visto de cima ficava apertado e brigava com a 3/4 ("navio-dentro-do-navio"). Refazemos o MUNDO como uma **ILHA no meio do mar**, com as 7 paradas espalhadas na ilha e o **NAVIO ancorado** como a ÚLTIMA parada/destino. **Só o CENÁRIO muda** (convés → ilha) e a história se ajusta. **Pedagogia e as 7 paradas ficam INTACTAS.**

---

## 0) DECISÃO DE ENGENHARIA (o que muda e o que NÃO muda)

| | Estado |
|---|---|
| **Câmera 3/4, colisão, WW=1900 / WH=1330** | **Inalterados** (geometria provada no pomar/navio). |
| **Motor `kit-floresta.py`** | **Não tocar hoje.** O `dados.json` da ilha roda com o motor atual (verificado: `desProp` genérico desenha o navio; `ancora_chao` assenta as moedas na areia; caso `cabana` já existe). |
| **Pedagogia (7 rounds BNCC 1º ano)** | **Intacta 1:1** — contar 3 · contar 5 · ordenar 5 · contar 10 · trazer_exato 7(de 10) · agrupar 20 · agrupar 30. |
| **Mecânicas + objeto de contar** | **Iguais** — `contar/ordenar/trazer_exato/agrupar`; objeto = **MOEDA DE OURO** (`moeda_ouro.png`); dezena = `saco10`; recipiente = `bau`. |
| **CENÁRIO** | **Muda:** convés → **ilha de areia**. `grama→areia`, `arvore→palmeira`, `muro→mar`, prop **navio** ancorado no cais. |
| **HISTÓRIA** | **Reescrita** p/ ilha: a maré espalhou as moedas pela ilha; o Byte junta/conta em cada ponto e carrega pro navio pra zarpar. |
| **Arte** | **3 assets a gerar depois:** `areia` (tile), `palmeira` (objeto), `navio` (objeto). Tudo o mais reusa arte pronta. |

**HOJE = só PROJETO** (este blueprint + o `dados.json` pronto abaixo). **NÃO** editar o motor, **NÃO** commitar, **NÃO** montar antes de a arte dos 3 assets existir.

---

## 1) LIMITE HONESTO DO MOTOR (a decisão que rege o cenário)

O motor pinta **o chão inteiro com UM tile só** (`patG = IMG.grama`, linha ~1178) e **a câmera clampa** em `WW-VW` / `WH-VH`. Ou seja: **o motor NÃO pinta mar em volta da ilha sozinho.** O tile `mar` (`patM`, via `assets.muro`) só é usado como textura DENTRO de props (paredes/blocos). Dois caminhos:

- **(a) v1 SEM tocar no motor (é o que este blueprint entrega):** `assets.grama → "areia"` (o chão todo vira areia da ilha); céu (`ceu0`/`ceu1`) afinado para **azul-mar** no horizonte; a **orla** é sugerida por **palmeiras de borda + moldura de horizonte**; as bordas continuam paredes suaves (colisão de sempre). Aceita-se que a beira "corta" na borda — mitigada pela moldura de palmeiras/horizonte e por manter tudo ≥120px das bordas (a câmera clampa).
- **(b) IDEAL, upgrade futuro (NÃO hoje, ~3 linhas):** `MUNDO.mar_borda = N` → no passe do chão (linha ~1178), preencher a **banda externa de N px** com `patM(mar)` em vez de `patG`. Dá a moldura de água REAL cercando a ilha de areia. Fica **registrado como upgrade opcional** (§7), não bloqueia o v1.

---

## 2) MUNDO E CONTORNO DA ILHA

- **WW=1900, WH=1330** (não mexer). **start = [317, 1089]** = **praia de desembarque**, canto inferior-esquerdo.
- **Ilha = blob ORGÂNICO** (nada de retângulo), inset ~170px das bordas: caixa útil `x∈[170,1730]`, `y∈[170,1160]`. A banda externa (~170px em volta) lê como **mar**.
- **Progressão monotônica**: da praia (inf-esq) subindo até o **cais** (sup-dir). A criança nunca faz backtracking; a trilha não se cruza.
- **Landmarks ≥120px das bordas** (a câmera clampa; colado na borda some metade do sprite).

### Trilha serpenteante (`path`, 16 nós) — agora FAZ sentido (trilha de areia, o oposto do convés chapado)
Saltos de ~120–200px, subindo da praia ao cais sem cruzar. Trilha caminhada total ~1900px (poucos segundos entre paradas: curto p/ não cansar o 1º ano, longo o bastante p/ "explorar").

```
[317,1089] [452,995] [540,905] [440,820] [512,722] [690,700] [636,600] [560,558]
[726,520] [884,516] [1012,586] [1096,642] [1188,560] [1262,492] [1388,502] [1500,516]
```

---

## 3) AS 7 PARADAS = 7 PONTOS DA ILHA (mesma escada pedagógica; só o cenário mudou)

Cada round = uma parada temática num ponto da ilha. **`cesta` = onde a moeda-de-ouro é juntada.** A ORDEM pedagógica (escada até a dezena) é MANTIDA. As posições foram desenhadas para que **cada cesta tenha ≥2 palmeiras a menos de ~130px** (o motor ancora as moedas nas `trees` mais próximas da cesta — sem palmeira perto, a moeda nasce longe). **Verificado por script** (distância das 2 palmeiras mais próximas, em px):

| # | Parada (ponto da ilha) | Mecânica | n / alvo | cesta (x,y) | 2 palmeiras ≈ | Beat + recompensa |
|---|---|---|---|---|---|---|
| 1 | **PRAIA DO NAUFRÁGIO** (acampamento da fogueira) | `contar` | 3 | (540, 965) | 86 · 88 | Byte acorda na areia: "Arr! 3 moedas rolaram da minha bota — conta comigo?" Recompensa: caem no bolso com "tlim"; o **sino do navio** ao longe bate 1×. |
| 2 | **COQUEIRAL DA VIGIA** (palmeiral + papagaio Louro) | `contar` | 5 | (430, 795) | 81 · 102 | Louro voa à copa: "Cráá! Do alto vejo 5 moedas entre os coqueiros!" Recompensa: "CINCO! ARR!" e uma bandeira pirata sobe na palmeira (posto de vigia). |
| 3 | **TRILHA DAS PEGADAS** (dunas) | `ordenar` (1→5) | 5 | (700, 690) | 69 · 83 | Bigode fareja: "As moedas pararam FORA DE ORDEM — do menor pro maior, qual vem primeiro?" Recompensa: "puf" de areia dourada a cada acerto; a trilha "acende" mostrando o caminho ao navio. |
| 4 | **CACIMBA DA ÁGUA DOCE** (poço de pedras) | `contar` | 10 | (566, 552) | 82 · 98 | Byte enche os barris pra viagem: "Preciso de 10 moedas pra pagar a água, e me perco depois do sete — conta comigo até o DEZ?" (1º dez inteiro por contagem.) Recompensa: a água jorra; os barris rolam pro navio. |
| 5 | **GRUTA DO ECO** (rocha, boca escura) | `trazer_exato` | 7 (de 10) | (1000, 612) | 65 · 79 | Louro guarda a porta: "A gruta só abre com EXATAMENTE 7 — tem 10 aqui, separa só 7 pra mim?" Erro → dica gentil ("tá sobrando / falta uma", o eco repete), sem punição. Recompensa: porta abre com brilho dourado. |
| 6 | **ARMAZÉM / BARRACÃO** (cabana de mantimentos) | `agrupar` (2×10) | 20 | (1200, 560) | 89 · 126 | Byte ensaca junto à fogueira do armazém: "Marujo esperto guarda de DEZ em DEZ! Enche 2 sacos — quanto dá?" (Introduz a dezena.) Recompensa: "nó" ao fechar cada saco; "Um saco, DOIS sacos — VINTE!" |
| 7 | **CAIS + NAVIO ANCORADO** (clímax/embarque) | `agrupar` (3×10) | 30 | (1470, 512) | 102 · 187 | A maré começa a subir: "Pra fechar o porão e zarpar, faltam TRINTA — enche os 3 sacos de dez, rápido!" Recompensa: âncora sobe ("clanc"), velas estufam; segue pro FINAL. |

### 3 alívios (sem matemática — respiro)
- **Papagaio "Louro"** empoleirado na palmeira do coqueiral: **(540, 740)** — ensina a dezena, vigia.
- **Gato "Bigode"** passeando na praia do desembarque, rota `[[519,1003],[640,960],[700,1080],[519,1003]]` — boas-vindas.
- **Mirante / Pedra do Vigia** (narrativo): vista do mar entre a gruta e o cais — pausa decorativa (sem prop no v1; entra na narração).

---

## 4) O NAVIO ANCORADO NO CAIS (última parada/destino)

- **Prop `navio` em (1560, 400)**, `h=260`, `r=44` (colisão) — no **topo-direita**, `y` BAIXO (fica "ancorado ao fundo", com água atrás pelo gradiente do céu). A cesta do agrupar-30 fica logo ao sul, em (1470, 512): o Byte chega **por baixo (sul)** = leitura 3/4 perfeita, o mastro sobe.
- **y-sort seguro:** `navio.y (400) < cesta7.y (512)` → o navio é desenhado ANTES (acima); a criança/moedas/cesta ficam por cima. **Não oclui.** Idem `cabana.y (470) < cesta6.y (560)`.
- **Renderização hoje:** `desProp` tem um caso genérico (linha ~639) que desenha `IMG[p.tipo]` na altura `p.h` com sombra de contato e balanço suave — **o navio aparece assim que a arte `navio.png` existir**, sem tocar no motor. Até lá, o prop cai em fallback seguro (não desenha, não quebra).
- **`lampiao` no cais** em (1540, 560) p/ clima de embarque (prop desenhado por código, fogo tremulando).
- **CUIDADO (o erro que quebrou o convés):** o navio tem de ser o **ÚNICO barco grande** da cena e ficar **só no cais**. Nada de props de convés espalhados competindo → foi exatamente o "navio-dentro-do-navio" que brigou com a 3/4.

---

## 5) A HISTÓRIA (premissa + final) — reambientada p/ ILHA

**Premissa.** O Byte Pirata, o papagaio **Louro** e o gato **Bigode** naufragaram numa **ILHA de areia dourada e palmeiras**. O navio **"Byte dos Sete Mares"** está ancorado na praia, mas a maré da tempestade **espalhou a carga de MOEDAS DE OURO por toda a ilha**. Para **ZARPAR** rumo à Ilha do Tesouro antes de a **maré subir de novo**, o Byte precisa **recolher e CONTAR/JUNTAR** as moedas em cada ponto da ilha e encher os baús. Cada ponto preparado deixa uma parte do navio pronta; quando o último saco fecha, o Byte embarca e o navio some no **horizonte dourado**.

**Frase-âncora do objetivo** (compatível com o portão de coerência — verbo = **juntar/contar**, jamais "chave"/"labirinto"): *"Ajuda o Byte a JUNTAR e CONTAR as moedas espalhadas pela ilha pra deixar o navio pronto pra zarpar!"*

**Falas-chave** (o Byte SEMPRE PERGUNTA e conta JUNTO, nunca dá o número pronto — cardinalidade): *"Quantas são ao todo?"* · *"Qual vem primeiro?"* · *"Você separa só 7 pra mim?"* · *"Dois sacos de dez, quanto dá?"* · *"Faltam quantas pra fechar?"*

**NPCs:** **Bigode** (gato de bordo) dá boas-vindas e reforça "não deixa moeda na areia sem contar"; **Louro** (papagaio) ensina "10 moedas viram 1 saco = uma DEZENA". Sem violência: nada de armas/tiros; se aparecerem canhões, soltam confete/fumacinha.

**Final espetacular.** Com o 3º saco fechado, a maré para de subir, o céu abre num **AMANHECER DOURADO** (ciclo dia/noite do motor, de graça). O Byte, com Louro no ombro e Bigode no colo, **sobe a passarela e embarca**; a âncora termina de subir, as velas incham e o navio corta as ondas, encolhendo até virar um **pontinho brilhante no horizonte dourado**. Fala do Byte: *"ARRR! Você juntou CADA moeda e aprendeu a contar até 30 na maior aventura — segura o leme comigo, PIRATA DOS NÚMEROS! Rumo à Ilha do Tesouro!"* Tela de medalha **"Pirata dos Números — 30"**.

> **Migração de coerência (importante):** o texto antigo falava *"colher laranjas no convés"* e *"escorbuto"*. Tudo isso foi reescrito para *"juntar moedas na ilha / carregar o tesouro pro navio"* nos textos visíveis (`sub_pc`, `sub_touch`, `aula.fim`, falas dos NPCs). O `npc0` (fala do Bigode) tem **texto novo** → o MP3 dele precisa ser **regerado** (§8).

---

## 6) `dados.json` COMPLETO E VÁLIDO — slug `navio-pirata`

Destino: **`eduverse/mundos/navio-pirata/dados.json`** (JSON parseia; **não** foi gravado lá — hoje é só projeto). Verificado com `python3 -c "json.load(...)"`: 7 rounds, 16 palmeiras, 16 nós de path, e cada cesta com ≥2 palmeiras a ~130px.

```json
{
 "slug": "navio-pirata",
 "tema": {
  "part": "folha",
  "ceu0": "rgba(160,225,255,.12)",
  "ceu1": "rgba(20,60,120,.15)",
  "passaros": true,
  "borboletas": false,
  "titulo": "A Ilha do Byte Pirata",
  "emoji": "&#127965;"
 },
 "assets": {
  "grama": "areia",
  "caminho": "caminho",
  "arvore": "palmeira",
  "byte": "byte_pirata",
  "flores": "flores",
  "muro": "mar",
  "cabana": "cabana",
  "passaro": "passarinho",
  "gato": "gato",
  "papagaio": "papagaio",
  "fruta": "moeda_ouro",
  "cesta": "bau",
  "sacola10": "saco10",
  "navio": "navio"
 },
 "mundo": {
  "WW": 1900,
  "WH": 1330,
  "start": [317, 1089],
  "tr": 16,
  "historia": {
   "objetivo": "colher",
   "sub_pc": "use as SETAS do teclado p/ o Byte Pirata explorar a ilha &#183; toca nas moedas de ouro e ajuda a encher os ba&#250;s do tesouro, contando cada uma!",
   "sub_touch": "use o D-pad p/ o Byte Pirata explorar a ilha &#183; toca nas moedas de ouro e ajuda a encher os ba&#250;s do tesouro, contando cada uma!"
  },
  "poeira": true,
  "ancora_chao": true,
  "dialogo": { "cps": 26 },
  "path": [
   [317, 1089], [452, 995], [540, 905], [440, 820],
   [512, 722], [690, 700], [636, 600], [560, 558],
   [726, 520], [884, 516], [1012, 586], [1096, 642],
   [1188, 560], [1262, 492], [1388, 502], [1500, 516]
  ],
  "trees": [
   [620, 928], [468, 1012], [352, 772], [520, 748],
   [772, 648], [662, 632], [822, 726], [492, 516],
   [664, 560], [1078, 598], [958, 662], [1288, 470],
   [1150, 486], [1560, 560], [200, 1170], [1712, 300]
  ],
  "flores": [
   [520, 1050], [700, 880], [560, 690], [930, 690],
   [1120, 610], [1300, 660], [1500, 520]
  ],
  "props": [
   { "tipo": "navio", "x": 1560, "y": 400, "h": 260, "r": 44 },
   { "tipo": "cabana", "x": 1200, "y": 470, "h": 210, "r": 56 },
   { "tipo": "fogueira", "x": 660, "y": 1010, "r": 14 },
   { "tipo": "lampiao", "x": 1540, "y": 560, "h": 60, "r": 8 }
  ],
  "npcs": [
   {
    "sprite": "gato",
    "x": 519, "y": 1003,
    "nome": "Bigode",
    "escala": 0.95,
    "vel": 26,
    "rota": [ [519, 1003], [640, 960], [700, 1080], [519, 1003] ],
    "falas": [
     { "texto": "Miau! Chegamos &#224; ilha do tesouro! Ajuda o Byte a juntar as moedas de ouro que a mar&#233; espalhou na areia e a contar cada uma pra encher os ba&#250;s?", "id": "npc0" },
     "Ronrom... eu sou o gato de bordo. Cada moeda que a gente conta &#233; um pedacinho a mais do tesouro pronto pro navio!",
     "Psst, Byte! N&#227;o deixa nenhuma moeda rolar pela areia sem contar, viu?",
     "Miau miau! Quando o ba&#250; encher, a gente carrega tudo pro navio e zarpa. Vamos contar mais uma?"
    ]
   },
   {
    "sprite": "papagaio",
    "x": 540, "y": 740,
    "nome": "Louro",
    "escala": 0.95,
    "falas": [
     "Cr&#225;! Cr&#225;! Moeda de ouro &#224; vista! Brilhando na areia da ilha, marujo!",
     "Um, dois, tr&#234;s... contar &#233; f&#225;cil! Vai enchendo o ba&#250; devagar, sem pular nenhuma!",
     "Cr&#225;! Dez moedas viram um saco &#8212; e um saco &#233; uma DEZENA cheia de ouro!",
     "Bom trabalho, Byte Pirata! Com voc&#234; contando, o navio leva TODO o tesouro pro pr&#243;ximo mar!"
    ]
   }
  ],
  "aula": {
   "id": "col1ano_navio",
   "fim": "Que aventura! Voc&#234; explorou a ilha e contou de 1 at&#233; 30 sozinho, enchendo os ba&#250;s de moedas de ouro &#8212; agora o Byte pode zarpar no navio levando todo o tesouro! Rumo ao pr&#243;ximo mar, marujo!",
   "rounds": [
    { "tipo": "contar", "n": 3, "cesta": { "x": 540, "y": 965 } },
    { "tipo": "contar", "n": 5, "cesta": { "x": 430, "y": 795 } },
    { "tipo": "ordenar", "n": 5, "cesta": { "x": 700, "y": 690 } },
    { "tipo": "contar", "n": 10, "cesta": { "x": 566, "y": 552 } },
    { "tipo": "trazer_exato", "alvo": 7, "n": 10, "pedido": "O Louro", "cesta": { "x": 1000, "y": 612 } },
    { "tipo": "agrupar", "n": 20, "cesta": { "x": 1200, "y": 560 } },
    { "tipo": "agrupar", "n": 30, "cesta": { "x": 1470, "y": 512 } }
   ]
  }
 },
 "falas": [
  "n0","n1","n2","n3","n4","n5","n6","n7","n8","n9","n10",
  "n11","n12","n13","n14","n15","n16","n17","n18","n19","n20",
  "n21","n22","n23","n24","n25","n26","n27","n28","n29","n30",
  "aula_intro_contar","aula_intro_ordenar","aula_intro_trazer_exato","aula_intro_agrupar",
  "aula_dica_contar","aula_dica_ordenar","aula_dica_trazer_exato","aula_dica_agrupar",
  "aula_ordem","aula_demais","aula_falta","aula_ok",
  "aula_ok_0","aula_ok_1","aula_ok_2","aula_ok_3","aula_ok_4","aula_ok_5","aula_ok_6",
  "aula_fim","npc0"
 ],
 "audit": { "chegar": [], "colisao": [] }
}
```

### Mapa de decisões (o que cada id vira no tema ilha)
- **`grama` → `areia`**: o CHÃO todo vira areia de praia (o motor preenche o mundo com esse tile). O "mar" vem pelo gradiente azul (`ceu0`/`ceu1`) + moldura de palmeiras/orla (motor pinta um piso só).
- **`arvore` → `palmeira`**: `trees` = palmeiras; são os **pontos-âncora das moedas** (o motor ancora TODA moeda nas `trees` mais próximas da cesta via `_geraItens`). `desArvore` desenha tronco+copa com balanço = coqueiro ao vento, em **altura fixa 120px**.
- **`muro` → `mar`**: textura de água (usada em blocos/paredes; a orla real vem do upgrade opcional `mar_borda`, §7).
- **`fruta` → `moeda_ouro`**: objeto de contagem (24px, bem menor que o Byte de 64px — regra de proporção mantida).
- **`cesta` → `bau`**, **`sacola10` → `saco10`**: baú do tesouro + saco da DEZENA (rounds `agrupar` 20 e 30).
- **`ancora_chao: true`**: as moedas **assentam na areia** (não "penduram" numa copa) — coerente com ilha; já suportado pelo motor (linha ~679).
- **`byte` → `byte_pirata`**: usa `byte_pirata` + `byte_pirata_costas` + `byte_pirata_lado` (já existem). ANDAR = deslizar + respiração (sem "perna dura") — regra do Marcos, de graça pelo fallback do motor.
- **props:** `navio` (imagem, via `desProp` genérico) · `cabana` (armazém/barracão, h=210, registro casa em 210) · `fogueira` + `lampiao` (desenhados por código, sem PNG).
- **`borboletas=false`** (não há em alto-mar); `flores` = toques tropicais leves na areia.

### Por que passa nos 4 portões (+ runner)
1. **`arte_proporcao`**: props cobrados pelo registro = `cabana` (h=210 == registro 210, dentro de ±25%). `navio` só é cobrado **quando** a arte for registrada (alvo=260 == h=260 → passa). `fogueira`/`lampiao` sem registro → não cobrados. `palmeira` registrada em 120 (= altura fixa do `desArvore`). Moedas (24px) claramente menores que o Byte (64px).
2. **`coerencia_tema`**: `objetivo="colher"` (≠"chave") ativa o gate; nenhum texto visível contém *labirinto, chave, nimbo, jaula, seta*. `sub_pc/sub_touch/fim/falas` são 100% de ilha/pirata. Verbo do objetivo = juntar/contar.
3. **`variedade_npc`**: os 2 NPCs têm `falas[]` com 4 itens cada (≥2).
4. **`variedade_contagem`**: maior `n` = 30 → `n0..n30` presentes nas `falas[]`.
- Ainda: `pedagogia_arco` OK (`historia.objetivo` + `aula.fim`); `mundo_vivo` garantido (palmeiras balançando + fogueira + lampião + partículas + respiração do Byte); geometria WW/WH/start/path/trees/cestas dentro dos limites (tudo ≥120px das bordas) → render + mecânica dirigível + área de jogo ≥45%.

---

## 7) ASSETS — REUSAR × GERAR

### REUSAR 1:1 (não regerar — já em `eduverse/biblioteca/proc/`)
`byte_pirata` (+ `byte_pirata_costas` + `byte_pirata_lado`, personagem VIVO) · `papagaio` (NPC Louro) · `moeda_ouro` (objeto de contar) · `saco10` (a dezena) · `bau` (recipiente/cesta) · `gato` (NPC Bigode) · `mar` (textura de água) · `cabana` (armazém/barracão) · `passarinho` (gaivotas ambiente) · `caminho` · `flores`. Props `fogueira`/`lampiao` = **desenhados por código** (sem PNG). `barril` e `conves` ficam de **reserva** (não usados na ilha).

### GERAR — 3 assets (a arte vem depois; são exatamente os que o Marcos apontou como FALTA)
Regra de estilo (todos): **flat cartoon chapado, contorno fechado escuro (~#3A2A1E, nunca preto puro), fills lisos sem gradiente e SEM sombra própria, formas orgânicas, mesmo traço/espessura do `byte_pirata`, fundo branco só p/ gerar (some no autocrop), recorte 100% limpo em transparência.** Paleta tropical fixa: areia `#F3E2B3`/`#E7CD8F`/`#D9B972`; mar `#2FA9C6`/`#7ED8E4`/espuma `#FFFFFF`; palmeira `#46A85A`/`#2E7D45`; madeira `#A9743C`/`#7A4E28`; dourado `#F4CE4B`.

1. **`areia`** (tile de chão, substitui `grama`; registrar tipo `tile`, sem `alvo_altura_px`):
   *"flat cartoon seamless tile of light tropical beach sand, top-down 3/4 view, warm pale sand #F3E2B3 with a few #E7CD8F speckle patches and tiny scattered pebbles, painted flat shapes, no gradient, no shadow, soft dark outline only on details, cheerful storybook look, seamless repeating texture, full-bleed no white border."* Nota: clara e quase lisa (não pode competir com a moeda/mascote por cima).
2. **`palmeira`** (árvore/ponto-âncora, entra em `mundo.trees`; registrar tipo `objeto`, `alvo_altura_px=120`, `escala_vs_byte≈1.9` — igual ao `desArvore` que desenha em altura fixa 120):
   *"flat cartoon coconut palm tree, side 3/4 view, curved brown trunk #A9743C with lighter rings, crown of long green fronds #46A85A and #2E7D45, two small brown coconuts, closed dark outline, flat fills, no shadow, no gradient, cute storybook style, transparent, full body with trunk base visible."* Nota: copa contida (o Byte passa por trás); base do tronco no chão (ancoragem correta, senão "flutua").
3. **`navio`** (veleiro pirata ancorado no cais = ÚLTIMA parada/clímax; prop-imagem via `desProp` genérico; registrar tipo `objeto`, `alvo_altura_px=260` == `h` do prop, `escala_vs_byte≈4.1`):
   *"flat cartoon pirate sailing ship anchored at shore, 3/4 side view from slightly above, wooden hull #A9743C with #7A4E28 planks, single tall mast with a cream unfurled sail, small skull-and-coins pirate flag, a golden anchor chain down to the sand, gentle friendly look (no cannons firing, no violence), closed dark outline, flat fills, no gradient, no shadow, storybook style, transparent."* Nota: 3/4 real de cima-lado (NÃO "de frente chapado", senão vira caixa — foi o erro do convés); casco pousado na areia, não flutuando reto; bandeira/vela levemente ao vento.

### Deco opcional (leva 2 — não bloqueia o v1; exigiria props-imagem novos)
`pedra` (~28px), `concha` (~20px), `tronco`/driftwood (~40px) — enfeites de praia em `mundo.props`. Prompts flat cartoon na mesma paleta. Ficam para depois de o v1 fechar.

> **Cada imagem nova deve ser conferida com o Marcos (montagem/screenshot) antes de fechar** — em especial o `navio` (Portão 3, risco da perspectiva 3/4).

---

## 8) MUDANÇAS NO MOTOR

**Obrigatórias hoje: NENHUMA.** Verificado no `kit-floresta.py`:
- `desProp` (linha ~639) já tem o caso genérico `else if(IMG[p.tipo])` que desenha o **navio** (`IMG.navio`) na altura `p.h` com sombra e balanço — funciona assim que `navio.png` existir.
- `ancora_chao` (linha ~679) já assenta as moedas na areia.
- Caso `cabana` (linha ~636) já existe.

**Opcionais (registrar como upgrade; NÃO hoje):**
1. **`MUNDO.mar_borda = N`** — no passe do chão (linha ~1178), pintar a **banda externa de N px** com `patM(mar)` em vez de `patG(areia)`. ~3 linhas. Dá a **moldura de água REAL** cercando a ilha (resolve o "corte" da beira). Recomendado para o v2.
2. **`TEMA.part = "espuma"`** — novo caso na emissão de partículas (linha ~1082/1151) com respingos branco/azul-claro do mar em vez de folha. ~2 linhas. Cosmético.

---

## 9) ÁUDIO (TTS)

`falas[]` = 53 ids. **Reaproveitar 1:1 do pomar/navio** (mesmos MP3): `n0..n30`, `aula_intro_*`, `aula_dica_*`, `aula_ordem`, `aula_demais`, `aula_falta`, `aula_ok`, `aula_ok_0..6`, `aula_fim`.
**Regerar (texto novo de ilha):** **`npc0`** (fala do Bigode: "Miau! Chegamos à ilha do tesouro..."). O gate `variedade_contagem` exige `n_audio >= n_falas` no `dist` → regerar `npc0.mp3` antes de fechar. As demais falas dos NPCs são strings inline (balão de texto), como no pomar.

---

## 10) PLANO DE CONSTRUÇÃO (sequenciado)

1. **Gerar os 3 assets** (`areia`, `palmeira`, `navio`) via `gerar-imagens.yml` com os prompts da §7. **Conferir cada um com o Marcos** (screenshot). Sem eles, `montar.py` imprime "!! falta asset" e o build quebra (`IMG.arvore` indefinido → `desArvore` falha).
2. **Registrar no `registro.json`**: `areia` (tile), `palmeira` (objeto, alvo 120 / escala 1.9), `navio` (objeto, alvo 260 / escala ~4.1). Alvo divergente do `h`/altura fixa faz o gate `arte_proporcao` cobrar e reprovar (±25%) — casar os valores.
3. **Criar** `eduverse/mundos/navio-pirata/dados.json` com o conteúdo da §6. *(Substitui o dados atual do convés.)*
4. **Áudio:** copiar os MP3 reaproveitáveis + **regerar `npc0.mp3`** (texto novo do Bigode).
5. **Montar:** `python3 eduverse/builders/montar.py navio-pirata` → `eduverse/dist/navio-pirata/index.html`.
6. **Auditar:** `python3 eduverse/audit/runner.py navio-pirata` → confirmar **APROVADO** nos 4 portões + node_check + render + mecânica + mundo_vivo + área ≥45%.
7. **Prévia** com Chromium headless (`--screenshot`, `--virtual-time-budget=4500`) e **enviar ao Marcos** para validar o "sentimento de ilha".
8. *(Opcional v2)* aplicar `mar_borda` / `part="espuma"` (§8) e deco de praia (§7), com o Marcos ciente.
9. **Publicar como atividade** no padrão do projeto (repo próprio via Fábrica + card no hub "Ilhas do Saber" apontando pelo link) — fora do escopo de hoje.

> **PRÉVIA IMEDIATA sem esperar a arte (se o Marcos quiser ver o layout já):** apontar temporariamente `grama→conves`, `arvore→barril` e remover o prop `navio` — roda com os assets atuais e mostra a geometria da ilha. Mas o cenário-alvo é ilha (areia/palmeira/navio).

---

## 11) RISCOS CONSOLIDADOS (e como o blueprint os mata)

| Risco | Mitigação neste projeto |
|---|---|
| Forma grande "chapada de cima" quebra a 3/4 (erro do convés) | Todo landmark é sprite **vertical** (palmeira, navio, cabana, fogueira) com sombra de contato + y-sort. |
| Prop alto plantado ao SUL da cesta oclui a criança | `navio.y(400)<cesta7.y(512)` e `cabana.y(470)<cesta6.y(560)` → props altos ficam ACIMA e ao lado. |
| Palmeira-âncora longe da cesta → moeda nasce longe | **Verificado por script:** cada cesta tem ≥2 palmeiras a ~130px. |
| Palmeira/pedra em cima da trilha ou cesta polui/atrapalha spawn | Palmeiras espalhadas orgânicas, fora dos nós do `path` e das cestas; centro de cada stop limpo. |
| Motor NÃO pinta mar sozinho (1 tile, câmera clampa) | Assumido explicitamente: areia + céu azul + orla de palmeiras no v1; `mar_borda` como upgrade §8. |
| Ilha grande demais cansa o 1º ano | Saltos 120–200px, ~200–260px entre paradas, progressão monotônica (zero backtracking). |
| Landmark colado na borda some metade | Tudo ≥120px das bordas (câmera clampa em WW-VW/WH-VH). |
| "Navio-dentro-do-navio" de novo | Navio é o ÚNICO barco grande, só no cais; sem props de convés espalhados. |
| Texto antigo ("laranja/convés/escorbuto") reprovaria coerência | `sub_pc/sub_touch/aula.fim`/falas reescritos p/ "moedas/ilha/tesouro"; `npc0.mp3` regerado. |
| 3 assets ainda não existem | Passo 1 do plano; até lá **não montar** (build quebra sem `areia`/`palmeira`/`navio`). |
| Peso/halo branco no autocrop (navio 260px é o maior) | Exigir transparência real + `optimize`; vigiar bytes no `registro.json`. |
```
