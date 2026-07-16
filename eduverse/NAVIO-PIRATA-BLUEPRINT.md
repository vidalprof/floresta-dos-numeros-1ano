# BLUEPRINT DE PRODUÇÃO — "O Navio do Byte Pirata" (números até 30, 1º ano)

> **Engenheiro-chefe consolidando Pedagogo + Roteirista + Diretor de Arte + Arquiteto de Dados.**
> Slug: **`navio-pirata`** · Motor reutilizável (`eduverse/motor/kit-floresta.py`, ES5) · Formato herdado do **pomar**.
> Regra de ouro do Marcos: **movimento TUDO SUAVE** (respiração/deslizar; sem perna dura). Objetivo da história = **"colher/juntar"** (NUNCA "chave"/"labirinto" — o portão de coerência reprova).

---

## 0) DECISÃO DE ENGENHARIA (o mais importante)

Existem **dois níveis** de entrega, e o blueprint separa os dois com honestidade:

- **v1 JOGÁVEL HOJE (recomendado zarpar já):** o `dados.json` abaixo reaproveita **100%** do motor e da geometria do pomar, **sem mudar o motor** e **sem nenhuma arte nova**. As laranjas anti-escorbuto (`fruta.png`) são juntadas nos **baús** (`bau.png`) e agrupadas em **sacos de 10** (`sacola10.png`); o chão é o **convés** (`conves.png`); os barris (`barril.png`) são os pontos-âncora. **Passa nos 4 portões + runner hoje.** As "partes do navio" existem pela **narrativa e posição das paradas** (o pedido do Marcos "cada parada é uma parte do navio" é cumprido no roteiro).
- **v2 PIRATA CHEIO (2 levas de upgrade):** gerar a arte temática (moeda de ouro, mastro/vela, canhão, saco de estopa, papagaio, poses do Byte pirata) e aplicar **3 mudanças mínimas e opcionais** no motor (props de peça de navio visíveis; ancorar item sem "copa"; partícula de espuma). Nada disso bloqueia o v1.

**Ordem de zarpe:** montar e auditar o v1 → gerar arte da leva 1 → aplicar mudanças mínimas do motor → montar v2 → conferir cada imagem com o Marcos.

---

## 1) OBJETIVOS DE APRENDIZAGEM (verificados pelo Pedagogo) → MAPEADOS NAS PARADAS

Ancoragem **BNCC** (1º ano, matemática concreta):

| Objetivo concreto | BNCC | Mecânica do motor | Parada(s) |
|---|---|---|---|
| Número como **quantidade** no cotidiano do navio | EF01MA01 | `contar` | 1, 2, 4 |
| **Contagem 1 a 1 por pareamento** (toca 1 = diz 1, sem pular/repetir) | EF01MA02 | `contar` | 1, 2, 4 |
| **Cardinalidade** (o último número dito = o total: "são 5 ao todo") — o salto do 1º ano | EF01MA04 | `contar` | 1, 2, 4 |
| **Sequência / ordem crescente** 1→n (a reta numérica, o "vem depois") | EF01MA01/05 | `ordenar` | 3 |
| **Comparar** mais / menos / igual; **quantidade exata** (para no número certo com sobra na tela) | EF01MA03 | `trazer_exato` | 5 |
| **Agrupar de 10 em 10 = a DEZENA** (10, 20, 30 = "grupos de dez") — valor posicional | EF01MA05 | `agrupar` | 6, 7 |
| **Contar até 30 com confiança** (série falada sólida n0..n30) | EF01MA01 | fala + `aula.fim` | fecho |

**Critério "o aluno aprendeu" por parada** (checagem do pedagogo):
- **P1/P2 (contar 3, 5):** toca cada objeto UMA vez e diz o **total** correto ("são 5") — cardinalidade, não só recitar.
- **P3 (ordenar 5):** aciona 1,2,3,4,5 sem pular; erro → dica corrige a ordem.
- **P4 (contar 10):** chega ao 10 sem repetir/pular; nomeia "dez" (1ª dezena por contagem).
- **P5 (trazer exato 7 de 10):** entrega exatamente 7, reconhece "falta"/"tem demais".
- **P6 (agrupar 20):** forma 2 sacos de 10 e lê "20 = dois grupos de dez".
- **P7 (agrupar 30):** forma 3 sacos de 10 e lê "30 = três grupos de dez".
- **Global:** conta 1→30 na fala de fechamento e entende "30 = três dezes".

**Calibragem obrigatória de 1º ano** (herdada e respeitada no v1): 5–6 desafios por round; recompensa imediata (som+animação a cada acerto); zero leitura pesada (voz + ícone + numeral grande); **erro sem punição** (dica gentil, nunca game over); número sempre **visível E falado** (símbolo+palavra+quantidade); **um objetivo por parada**. **O 30 NUNCA é "conte 30 um a um"** — aparece só como AGRUPAR (3 sacos), que é a noção de dezena.

---

## 2) A HISTÓRIA (premissa + final)

**Premissa.** O veleiro **Byte dos Sete Mares** vai zarpar até a **Ilha do Tesouro**, mas uma **tempestade** se forma no horizonte. Para o navio aguentar o mar bravo, a tripulação precisa **preparar cada parte do navio antes da tempestade chegar** — carregar mantimentos, içar velas, guardar o tesouro, encher o porão. O Byte é o capitão pirata, mas **não sabe contar sozinho até 30**: é a **criança** (a heroína) que **conta e junta** as coisas em cada parte do navio. A cada parte pronta, o mar se acalma e o navio avança.

**Frase-âncora do objetivo** (compatível com o portão de coerência): *"Ajuda o Byte a JUNTAR e CONTAR tudo que o navio precisa pra travessia!"* — verbo = **juntar/carregar/contar**, jamais "chave"/"labirinto".

**Final espetacular.** Ao fechar a última parada, a **tempestade se afasta**, o céu abre num **amanhecer dourado** (vem de graça do ciclo dia/noite do motor no checkpoint da cabine do capitão), o navio corta as últimas ondas e surge a **Ilha do Tesouro** com um X gigante na areia. A **âncora desce** ("clanc"), o baú se abre e o Byte celebra: *"ARRR! Você preparou CADA parte do navio e nos trouxe são e salvo — e aprendeu a contar até 30 no meio da tempestade! Você é um PIRATA DOS NÚMEROS!"* Tela de medalha **"Pirata dos Números — 30"**.

**2 NPCs de apoio** (cada um com `falas[]` variado — passa `variedade_npc`):
- **Gato de bordo "Bigode"** (sprite `gato`, passeia pelo convés): dá as boas-vindas e reforça "não deixa laranja sem contar".
- **Papagaio "Louro"** (sprite `papagaio`→`passarinho` no v1; arte própria na leva 1): empoleirado, repete palavras, ensina que "10 laranjas viram um saco = uma DEZENA".

O **Byte sempre PERGUNTA e conta JUNTO** (nunca dá o número pronto). Sem violência: canhões (se forem gerados) soltam confete/fumacinha, nunca projétil.

---

## 3) AS 7 PARADAS (parte do navio + mecânica + n/alvo até 30 + beat + recompensa)

Escada pedagógica idêntica à validada no pomar (aquecer → ordenar → firmar 10 → exato → dezena 20 → dezena 30). Cada round = uma PARADA = uma PARTE do navio.

| # | Parte do navio | Mecânica | n / alvo | Beat (o que acontece) | Recompensa |
|---|---|---|---|---|---|
| 1 | **Convés (proa/embarque)** | `contar` | n=3 | Byte acorda a criança: "Arr! O convés tá bagunçado, caíram uns barris — junta comigo?" Toca 3 e conta 1,2,3. | Barris se encaixam com "toc" de madeira; **sino do navio** bate 1 vez. |
| 2 | **Cesto da gávea (vigia)** | `contar` | n=5 | O papagaio Louro vigia lá em cima: "Conta as gaivotas/mapas, marujo!" Conta até 5. | Papagaio grita "CINCO! ARR!" batendo asas. |
| 3 | **Canhões (casco)** | `ordenar` | n=5 (1→5) | Lobo-do-mar: "Canhão carrega em ORDEM, do menor pro maior!" Encaixa 5 bombas em ordem. | Cada bomba certa solta "puf" de fumaça colorida; salva de confete no fim. |
| 4 | **Velas / mastro principal** | `contar` | n=10 | Byte iça a vela: "Preciso de 10 puxões na corda e sempre me perco — conta comigo!" 1ª vez que chega ao 10 inteiro. | Vela sobe tremulando ao vento; navio ganha velocidade (mar corre pra trás). |
| 5 | **Porão do tesouro** | `trazer_exato` | alvo=7 de n=10 | "O baú quer EXATAMENTE 7 moedas/laranjas — nem mais, nem menos! Tem 10, traz só 7." | Moedas tilintam no baú; tampa abre com brilho dourado. Erro → dica ("tá sobrando/faltando"), sem entregar. |
| 6 | **Cozinha / despensa** | `agrupar` | n=20 (2 sacos de 10) | "Marujo esperto guarda de DEZ em DEZ! Enche 2 sacos = VINTE laranjas (curam o escorbuto)." Introduz a dezena. | "Nó" satisfatório ao fechar cada saco; "Um saco, DOIS sacos — VINTE! Arr!" |
| 7 | **Leme / âncora (popa)** — clímax | `agrupar` | n=30 (3 sacos de 10) | Céu escurecendo: "Pra vencer a tempestade o porão precisa de TRINTA de tudo — enche os 3 sacos de dez!" | Byte gira o leme, **âncora sobe** ("clanc"/corrente), vela estufa; segue pro FINAL. |

**Cortes previstos** (confirmar nº final com o pedagogo antes de fechar): **6 paradas** = fundir P1+P2 (contar 3 + contar 5 no convés); **8 paradas** = inserir um `ordenar` n=10 (organizar 10 bandeiras de sinalização) entre P4 e P5.

**Animação/som por parada** (regra Marcos = tudo suave): convés balançando senoidal (~2–3px); pena do chapéu e velas tremulando; gaivotas em arco com "iááá"; moedas tilintando; papagaio "braaa"; sino a cada parada; "nó" de corda ao fechar cada dezena; âncora com corrente. **Nota de honestidade (Web Speech/Audio):** o som só começa após o 1º gesto (regra do navegador, não é bug) — manter o botão "Ouvir instruções" piscando como start garantido, igual ao hub.

---

## 4) `dados.json` COMPLETO E VÁLIDO — slug `navio-pirata` (v1, passa nos 4 portões)

Salvar em **`eduverse/mundos/navio-pirata/dados.json`**. Montar: `python3 eduverse/builders/montar.py navio-pirata`. Auditar: `python3 eduverse/audit/runner.py navio-pirata`.

```json
{
 "slug": "navio-pirata",
 "tema": {
  "part": "folha",
  "ceu0": "rgba(120,200,255,.12)",
  "ceu1": "rgba(10,30,80,.16)",
  "passaros": true,
  "borboletas": false,
  "titulo": "O Navio do Byte Pirata",
  "emoji": "&#9875;"
 },
 "assets": {
  "grama": "conves",
  "caminho": "caminho",
  "arvore": "barril",
  "byte": "byte_pirata",
  "muro": "mar",
  "cabana": "cabana",
  "passaro": "passarinho",
  "gato": "gato",
  "papagaio": "passarinho",
  "fruta": "fruta",
  "cesta": "bau",
  "sacola10": "sacola10"
 },
 "mundo": {
  "WW": 1900,
  "WH": 1330,
  "start": [317, 1089],
  "tr": 16,
  "historia": {
   "objetivo": "colher",
   "sub_pc": "use as SETAS do teclado p/ o Byte Pirata andar pelo conv&#233;s &#183; toca nas laranjas e ajuda a encher os ba&#250;s, contando cada uma!",
   "sub_touch": "use o D-pad p/ o Byte Pirata andar pelo conv&#233;s &#183; toca nas laranjas e ajuda a encher os ba&#250;s, contando cada uma!"
  },
  "poeira": true,
  "dialogo": { "cps": 26 },
  "path": [
   [317, 1089], [481, 937], [380, 760], [646, 646],
   [874, 709], [1064, 595], [1279, 570], [1457, 507]
  ],
  "trees": [
   [1184, 196], [572, 404], [1609, 261], [819, 201], [155, 379],
   [1202, 742], [1718, 523], [1466, 936], [1011, 1192], [559, 1153],
   [385, 568], [1772, 842], [1046, 889]
  ],
  "flores": [],
  "props": [
   { "tipo": "cabana", "x": 1381, "y": 760, "h": 210, "cx": -56, "cy": 186, "r": 64 },
   { "tipo": "lampiao", "x": 1472, "y": 793, "h": 60, "r": 8 }
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
     { "texto": "Miau! O escorbuto ronda o mar. Ajuda o Byte a colher as laranjas e contar cada uma pra encher os ba&#250;s?", "id": "npc0" },
     "Ronrom... eu sou o gato de bordo. Laranja fresca deixa a tripula&#231;&#227;o forte pra travessia!",
     "Psst, Byte! N&#227;o deixa nenhuma laranja rolar pelo conv&#233;s sem contar, viu?",
     "Miau miau! Quando o ba&#250; encher, ganho um cochilo no sol. Vamos contar mais uma?"
    ]
   },
   {
    "sprite": "papagaio",
    "x": 1230, "y": 700,
    "nome": "Louro",
    "escala": 0.95,
    "falas": [
     "Cr&#225;! Cr&#225;! Laranja &#224; vista! A melhor carga do por&#227;o &#233; essa aqui!",
     "Um, dois, tr&#234;s... contar &#233; f&#225;cil, marujo! Vai enchendo o ba&#250; devagar!",
     "Cr&#225;! Dez laranjas viram um saco &#8212; e um saco &#233; uma DEZENA cheia!",
     "Bom trabalho, Byte Pirata! Com voc&#234; contando, ningu&#233;m fica doente no mar!"
    ]
   }
  ],
  "aula": {
   "id": "col1ano_navio",
   "fim": "Que travessia! Voc&#234; contou de 1 at&#233; 30 sozinho e encheu os ba&#250;s de laranjas &#8212; a tripula&#231;&#227;o n&#227;o vai adoecer no mar! Rumo &#224; pr&#243;xima ilha, marujo!",
   "rounds": [
    { "tipo": "contar", "n": 3, "cesta": { "x": 659, "y": 988 } },
    { "tipo": "contar", "n": 5, "cesta": { "x": 1140, "y": 659 } },
    { "tipo": "ordenar", "n": 5, "cesta": { "x": 887, "y": 811 } },
    { "tipo": "contar", "n": 10, "cesta": { "x": 1317, "y": 570 } },
    { "tipo": "trazer_exato", "alvo": 7, "n": 10, "pedido": "O Louro", "cesta": { "x": 912, "y": 811 } },
    { "tipo": "agrupar", "n": 20, "cesta": { "x": 709, "y": 785 } },
    { "tipo": "agrupar", "n": 30, "cesta": { "x": 1165, "y": 1013 } }
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

### Mapa de decisões (o que cada id vira no tema navio)
- **`grama` → `conves.png`**: o CHÃO é o convés de madeira (o motor preenche o mundo com esse tile). O "mar em alto-mar" vem pelo **gradiente de céu azul** (`ceu0`/`ceu1`), já que o motor usa um único tile de piso.
- **`arvore` → `barril.png`**: pontos-âncora dos objetos de contagem. `trees` = barris de carga espalhados pelo convés (o motor ancora TODA laranja em `trees` via `_geraItens`; sem `trees` não nasce item). `desArvore` desenha o barril com balanço suave = navio jogando no mar. **Zero mudança de motor.**
- **`fruta` → `fruta.png`**: objeto de contagem = **laranjas anti-escorbuto** (24px, bem menor que o Byte de 64px — regra de proporção). Tema histórico real de pirata.
- **`cesta` → `bau.png`**: o **baú** do porão onde a criança junta as laranjas (o motor destaca a "cesta" da rodada).
- **`sacola10` → `sacola10.png`**: o **saco de 10** = introduz a DEZENA (rounds `agrupar` 20 e 30).
- **`byte` → `byte_pirata`**: o montador auto-carrega a cartela `byte_pirata_<pose>`; como as poses não existem ainda, cai no `byte_pirata.png` base → **a perna não alterna, fica só a respiração suave** (exatamente a regra do Marcos "se a perna ficar dura, faz sem perna").
- **`passaro` → `passarinho.png`**: gaivotas ambiente (`passaros=true`).
- **`cabana` → `cabana.png`** (prop, h=210): a **cabine do capitão** (castelo de popa) — solta fumaça pela chaminé e passa no gate de proporção (registro alvo=210).
- **`lampiao`** (prop, h=60): lampião de convés (fogo tremulando + crepitar); sem entrada no registro → o gate de proporção o ignora.
- **`gato` → `gato.png`** (NPC "Bigode"): gato de bordo, passeia com rota.
- **`papagaio` → `passarinho.png`** (NPC "Louro"): papagaio do pirata (placeholder no v1; arte própria na leva 1).
- **`borboletas=false`, `flores=[]`**: sem borboletas nem flores em alto-mar.

### Por que passa nos 4 portões (+ runner)
1. **`arte_proporcao`**: único prop cobrado pelo registro é `cabana` (h=210, dentro de ±25% do alvo 210 e >192=3×Byte). `lampiao` não tem registro → não cobrado. Objetos de contagem (24px) claramente menores que o Byte (64px).
2. **`coerencia_tema`**: `objetivo="colher"` (≠"chave") ativa o gate; nenhum texto visível/script contém *labirinto, chave dourada, nimbo, jaula, pedra-seta*. `sub_pc/sub_touch/fim/falas` são 100% de navio. (Os fallbacks do motor com "chave"/"labirinto" ficam em linhas com `||` → tolerados, igual ao pomar.)
3. **`variedade_npc`**: os 2 NPCs têm `falas[]` com 4 itens cada (≥2). Nenhum NPC decorativo com fala única.
4. **`variedade_contagem`**: maior `n` dos rounds = 30 → exige `n1..n30` nas `falas[]` (incluídos `n0..n30`). *(A cobertura de áudio `n_audio>=n_falas` é etapa de geração de voz — ver §7.)*
- Ainda: `pedagogia_arco` OK (tem `historia.objetivo` + `aula.fim` roteirizado); `mundo_vivo` garantido por barris balançando + lampião + partículas + nuvens + respiração do Byte; geometria (WW/WH/start/path/trees/cestas) reaproveitada 1:1 do pomar → render, mecânica dirigível e área de jogo ≥45% garantidos.

---

## 5) ASSETS — REUSAR (não regerar) × GERAR (com prompt curto)

### REUSAR 1:1 (já no banco / demo — NÃO regenerar)
`byte_pirata.png` (pose frente) · `mar.png` · `conves.png` · `barril.png` · `bau.png` (+ `bau_tesouro`) · convés/casco da demo `_demos/educaverso/navio/` · genéricos: `fruta.png` (=laranja), `sacola10.png`, `cabana.png`, `lampiao`, `gato.png`, `passarinho.png`, `caminho.png`.

### GERAR (via `gerar-imagens.yml`; não bloqueia o build, só enriquece o tema)
Todos os prompts terminam com: *"fundo branco sólido, contorno preto fechado, sem sombra, estilo cartoon storybook pintado à mão, cores saturadas, **mesmo traço/estilo do Byte**."*

**LEVA 1 (mínimo pra virar pirata de verdade — prioridade):**
1. **`papagaio`** — "um papagaio colorido de pirata (vermelho, azul e amarelo) empoleirado, fofo, olhando de lado" *(substitui o placeholder do NPC Louro; entra no registro como bicho/NPC)*.
2. **`byte_pirata_costas`** — "o mesmo robô pirata visto DE COSTAS, chapéu bicorne e casaco vermelho por trás".
3. **`byte_pirata_lado`** — "o mesmo robô pirata de PERFIL/lado, olhando pra direita". *(2 e 3 dão as 4 direções de face; ANDAR continua sem perna, só deslizar+respiração — regra Marcos.)*
4. **`moeda_ouro`** — "uma moeda de ouro de pirata brilhante com uma caveira gravada, vista de frente" *(variante do objeto de contagem; alvo ~30px)*.
5. **`saco10`** — "um saco de estopa bege amarrado com corda, cheio, com o número 10 escrito" *(recipiente da dezena, tema navio; alvo ~40px)*.
6. **`mastro`** — "um mastro alto de navio pirata em madeira com grande vela branca inflada, cesto da gávea no topo e bandeira pirata preta com caveira, corpo inteiro vertical" *(marco visual; alvo tall ~3–4× Byte no registro)*.

**LEVA 2 (peças de navio + vida — depois do mínimo):**
7. **`canhao`** — "um canhão de navio de ferro preto sobre carreta de madeira com rodas, visto de lado".
8. **`leme`** — "um leme de navio (roda do capitão) em madeira com raios e punhos, visto de frente".
9. **`ancora`** — "uma âncora de ferro preto com corrente, encostada, vista de frente".
10. **`amurada`** — "um trecho de amurada/corrimão de navio em tábuas de madeira, horizontal" *(tile de borda + colisão)*.
11. **`bomba_canhao`** — "uma bala de canhão preta redonda de ferro com brilho metálico, pequena" *(objeto do `ordenar`; alvo ~32px)*.
12. **`caixote`** — "um caixote de madeira aberto com moedas de ouro transbordando" *(contexto das moedas)*.
13. **`gaivota`** — "uma gaivota branca de asas abertas voando, simples, fofa" *(substitui a borboleta no céu do mar)*.
14. **`passarela`** — "tile de tábuas de madeira clara e gasta, vista de cima, sem costura (seamless)" *(trilha entre paradas; opcional)*.
15. **Poses de estado do Byte pirata** (`byte_pirata_feliz`, `byte_pirata_fala`, `byte_pirata_senta`, `byte_pirata_deita`) — para o checkpoint noturno; **até lá o motor cai na pose base** (OK).

**Cada imagem nova deve ser conferida com o Marcos (montagem/screenshot) antes de fechar** (regra do projeto). Cada peça de navio visível que virar prop precisa de **entrada no `registro.json` com `alvo_altura_px`** coerente, senão o gate `arte_proporcao` não a protege.

---

## 6) LISTA DE FALAS (áudio TTS)

Já no `dados.json.falas[]` (53 ids). Reaproveitáveis **1:1 do pomar** (mesmos MP3): `n0..n30`, `aula_intro_*`, `aula_dica_*`, `aula_ordem`, `aula_demais`, `aula_falta`, `aula_ok`, `aula_ok_0..6`, `aula_fim`.

**Precisam de TTS NOVO** (texto próprio do navio):
- **`npc0`** — fala do gato de bordo Bigode ("Miau! O escorbuto ronda o mar...").
- *(As demais falas dos NPCs — Bigode itens 2–4, Louro 1–4 — são strings inline no diálogo; se o projeto gerar voz por string, incluir; senão ficam em balão de texto lido pela criança/voz do sistema, como no pomar.)*

**Gate de voz:** `variedade_contagem` exige que o `dist` embuta `n_audio >= n_falas`. Como `npc0` tem texto novo, **regerar o MP3 de `npc0`** antes de fechar; o resto é cópia do pomar.

---

## 7) MUDANÇAS MÍNIMAS NO MOTOR (TODAS OPCIONAIS — v1 não precisa de nenhuma)

O v1 roda **sem tocar no motor**. As três abaixo são para o v2 pirata cheio; cada uma é pequena e isolada.

1. **Ancorar item SEM "copa" (recomendada p/ v2).** Hoje `_geraItens` pendura ~70% dos itens ~72px ACIMA da âncora (feito pra copa de árvore); num barril/convés lê como laranja levemente "flutuando". **Mínimo:** condicionar o offset de copa a um flag — ex.: quando `TEMA.part!=="folha"` ou um novo `MUNDO.ancora_chao=true`, forçar `pendurada=false` (item assenta no chão/topo do barril). ~2 linhas em `_geraItens` (linha ~608). Alternativa sem motor: gerar `mastro.png` e apontar `assets.arvore→mastro` (a laranja "pendura" na rede do mastro, e aí o offset faz sentido).
2. **Peças de navio como props VISÍVEIS (mastro/canhão/leme/âncora/amurada).** `desProp` (linha 559) só conhece `fogueira/lampiao/cabana`. **Mínimo:** adicionar casos genéricos que desenhem `IMG[p.tipo]` na altura `p.h` com sombra de contato (espelhando o caso `cabana`). ~4–6 linhas + arte + entradas no `registro.json`. Sem isso, as "partes do navio" ficam por narrativa/posição (v1).
3. **Partícula de ESPUMA em vez de folha.** `TEMA.part` só aceita `folha`/`neve`; o motor emite folhas/pétalas coloridas (linha ~1082). **Mínimo:** novo caso `part==="espuma"` com cor branca/azul-clara (respingos do mar). ~2 linhas. Cosmético.

> **Byte "andar sem perna" NÃO exige mudança de motor:** o fallback já usa a pose estática + respiração quando faltam os frames de passo (linha ~462). Isso É a regra do Marcos, de graça.

---

## 8) PLANO DE CONSTRUÇÃO (sequenciado)

1. **Criar** `eduverse/mundos/navio-pirata/dados.json` com o conteúdo da §4.
2. **Montar:** `python3 eduverse/builders/montar.py navio-pirata` → gera `eduverse/dist/navio-pirata/index.html`.
3. **Áudio:** copiar os MP3 reaproveitáveis do pomar para `_audio/` e **regerar `npc0.mp3`** (texto do gato de bordo). Remontar.
4. **Auditar:** `python3 eduverse/audit/runner.py navio-pirata` → confirmar **APROVADO** nos 4 portões + node_check + render + mecânica + mundo_vivo + área ≥45%.
5. **Prévia** com o Chromium headless (`--screenshot`, `--virtual-time-budget=4500`) e **enviar ao Marcos** para validar o "sentimento de navio" do v1.
6. **Leva 1 de arte** (via `gerar-imagens.yml`): `papagaio`, `byte_pirata_costas`, `byte_pirata_lado`, `moeda_ouro`, `saco10`, `mastro`. **Conferir cada imagem com o Marcos.** Registrar `alvo_altura_px` no `registro.json`.
7. **Aplicar mudanças mínimas do motor** (§7, itens 1 e — se quiser peças visíveis — 2 e 3), com o Marcos ciente (não commitar sem ok).
8. **Trocar no `dados.json`** para a versão pirata cheia: `papagaio→papagaio`, objeto de contagem `fruta→moeda_ouro` (ou manter laranja), `sacola10→saco10`, `arvore→mastro` (ou barril + flag `ancora_chao`), props de peças de navio. Remontar + reauditar.
9. **Leva 2 de arte** (canhão/leme/âncora/amurada/bomba/gaivota/poses de estado) conforme o Marcos quiser subir o acabamento.
10. **Publicar como atividade** no padrão do projeto (repo próprio via Fábrica + card no hub "Ilhas do Saber" apontando pelo link) — fora do escopo de hoje.

> **HOJE:** só **projeto + autoria** (este blueprint + o `dados.json` pronto). **NÃO** codar o motor. **NÃO** commitar.
