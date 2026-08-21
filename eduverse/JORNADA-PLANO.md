# PLANO DA CAMADA DE JORNADA — EduVerse
### Consolidação da equipe (engenheiro-chefe) · artefato de PROJETO + AUTORIA
> Este documento NÃO edita o motor nem os dados dos mundos existentes
> (`pomar`/`cesta-do-tico`/`floresta`). Ele DECIDE a arquitetura da camada de
> jornada, AUTORA a primeira jornada por extenso, fixa o schema `mundo.jornada`
> e sequencia a implementação — que só começa DEPOIS que o polimento do motor
> (em curso por outro engenheiro) terminar.

---

## 0. Decisão executiva (o que fica cravado)

| Questão | Decisão consolidada | Justificativa |
|---|---|---|
| **Nº de fases** | **10 paradas** em `jornada.fases[]` = **8 fases-tarefa** (carga cognitiva) + **2 beat-fases** (alívio puro), mais abertura (~4 min) e final (~3 min). | Reconcilia roteirista (8 tarefas + 2 beats), pedagogo (8 fases, alívios embutidos) e engenheiro (que contava tarefa+beat como 1 unidade → "5-6"). São a MESMA aula contada em unidades diferentes. |
| **Tempo total** | **~52 min** (janela 50-55). | Ver a conta em §1. |
| **Jornada-piloto** | **"A Noite da Grande Geada"** (mundo O Pomar do Byte · 1º ano · Matemática). | Reusa 100% dos assets/beats do motor; escada BNCC limpa; final que fecha o enredo. |
| **Modelo de dados** | Bloco NOVO e OPCIONAL `mundo.jornada`, ao lado de `mundo.aula` (legado intacto). | `mundo.jornada == null` → motor idêntico ao de hoje. Zero regressão nos 3 mundos atuais. |
| **Papel do motor** | ORQUESTRADOR (jornada) + EXECUTOR (motor de rodadas atual roda a tarefa 1:1). | Evita reescrever as 4 mecânicas, render, física e NPCs. |

**Regra de ouro (loop-FORMA, não template):** a IA-roteirista alterna fases-tarefa
com beats curtos. "chave→cabana→dormir" é UM caminho possível, não obrigatório.
Quem autora enredo, recompensas e FINAL é a IA, único por mundo.

---

## 1. A CONTA DO TEMPO (por que 8 tarefas + 2 beats ≈ 52 min)

Custos fixos (fora das fases):
- Abertura + destravar som + Byte apresenta o problema do mundo: **~4 min**
- Final que resolve o enredo + reflexão "o que você descobriu hoje?": **~3 min**

Sobra para o miolo: `55 − 4 − 3 = ~48 min`.

Miolo = 8 fases-tarefa + 2 beat-fases:
- Fase-tarefa = GANCHO (~40s) + TAREFA (3-4 min, 1 rodada do motor) + RECOMPENSA/transição (~1 min) ≈ **~5 min** → `8 × 5 = 40 min`
- Beat-fase (alívio: entrar na despensa / dormir-amanhecer) ≈ **~2,5 min** → `2 × 2,5 = 5 min`

Miolo real ≈ `40 + 5 = 45 min`. Total ≈ `4 + 45 + 3 = 52 min`. **Folga real de 2-3 min**
(criança de 6 anos precisa de folga, não de encaixe apertado).

**Por que 8 tarefas e não 10:** 1º ano satura em ~4-6 min por micro-tarefa. 10 tarefas
= ~50 min só de esforço cognitivo → vale de atenção no minuto ~30 e a turma dispersa.
Reduzir para 8 + intercalar 2 alívios fortes (Beat A depois do bloco de chave; Beat B
no pico de fadiga, antes do clímax) segura a atenção. **Se a turma for mais nova/agitada:
cair para 7 tarefas** (remover a Fase 5 "prateleira do 8", virar a 4 em reforço) → ~45 min.

---

## 2. A JORNADA AUTORADA POR EXTENSO — "A Noite da Grande Geada"

**Mundo:** O Pomar do Byte · **Ano:** 1º · **Disciplina:** Matemática (BNCC EF01MA01/03/04/05).
**Assets reusados (zero peso novo):** Byte + poses, Tico (coelho), árvore, cabana+interior+lampião,
cesta, fruta, sacola10, chave, gato, passarinho, borboleta, flores, fogueira, ciclo dia/noite,
NPCs vivos, path. A "Grande Macieira" do final = `arvore` reusada em escala maior + glow CSS/canvas.

### Premissa (o problema que PRECISA da criança)
Cai a tarde. O Byte chega ao Pomar e o Tico está tremendo: **esta noite vem a primeira GEADA
do inverno** e o pomar não está pronto. Duas coisas deram errado — a **despensa está vazia**
(ninguém colheu a tempo) e os **lampiões que aquecem a trilha até a Grande Macieira se apagaram**,
deixando o caminho escuro e frio. A Grande Macieira é o coração do pomar: ao florescer, espalha
calor e protege todos. Mas ela só acorda se **a despensa estiver cheia e o caminho todo aceso
antes do amanhecer**. O Byte sabe andar e carregar, mas **não sabe contar, ordenar nem organizar
sozinho** — precisa da criança, a **Guardiã da Contagem**.

*(Filosofia respeitada: PROBLEMA primeiro — geada + despensa vazia + escuro. Contar/ordenar/dezena
são a FERRAMENTA que salva o pomar, nunca uma tranca. "Dezena" é nomeada só no fim.)*

### Objetivo final
Encher a despensa organizando as frutas em **grupos de dez (dezenas)**, **acender toda a trilha**
e **ACORDAR a Grande Macieira** antes de amanhecer. O aluno sai sentindo "salvei o pomar", e só
depois percebe "aprendi a contar, a ordem dos números e a contar de dez em dez".

### Recompensa VISÍVEL que costura tudo
Cada fase-tarefa **acende UM lampião da trilha** → o caminho sai literalmente do escuro rumo à
Grande Macieira. E a despensa **enche prateleira a prateleira**. Progresso físico, não fases soltas.

---

### FASE 1 — "O Byte Chega ao Pomar Gelado" · tarefa: **contar (n=3)**
- **História/gancho:** Anoitecer frio. O Tico corre até o Byte tremendo: a geada vem à noite, a
  despensa está vazia. Três frutinhas caíram na entrada.
- **Tarefa (a criança FAZ):** guia o Byte e toca em cada uma das 3 frutinhas; o Tico conta UMA a
  UMA, colocando na cesta. Habilidade: **contagem 1-a-1, correspondência termo-a-termo, cardinalidade**
  (a última palavra dita = o total).
- **Recompensa + conexão:** 1ª cesta cheia ACENDE o 1º lampião → a luz revela o próximo trecho. → F2.
- **Falas:**
  - Tico: "Byte! A geada chega hoje e a despensa está vazia… você me ajuda a colher? Toca em cada frutinha!"
  - Byte: "Olha, três caíram aqui. **Se a gente tocar uma de cada vez, o que você acha que vamos descobrir?**"
  - Byte (fecho): "Uma… duas… três! **Quantas ficaram na cesta no total?**"

### FASE 2 — "A Trilha Embaralhada" · tarefa: **ordenar (n=5)**
- **História/gancho:** O ventinho espalhou 5 frutinhas fora de ordem. A Grande Macieira só reconhece
  a colheita "na ordem certa", do 1 ao 5.
- **Tarefa:** colher na SEQUÊNCIA 1→2→3→4→5 (posições embaralhadas; colher fora de ordem = a frutinha
  treme e não vem = depuração natural, sem X vermelho). Habilidade: **sequência numérica / ordem
  crescente / qual vem antes-depois**.
- **Recompensa + conexão:** 2º lampião acende; uma **borboleta** surge da luz e voa apontando o rumo. → F3.
- **Falas:**
  - Byte: "Estão todas fora do lugar! **Se a gente fosse contar do começo, qual número viria primeiro?**"
  - Byte (após erro): "Essa não quis vir ainda. **Qual será que vem antes dela?**"
  - Tico: "Um, dois, três… a trilha adora quando a gente conta direitinho."

### FASE 3 — "A Chave da Despensa" · tarefa: **contar (n=8)**
- **História/gancho:** Chega-se perto da cabana, mas a porta da despensa está trancada. O **gato**
  guarda a **chave**; só a entrega depois de ver o Byte colher as 8 frutas maduras da moita.
- **Tarefa:** contar e colher 8 frutinhas (número maior, mesma correspondência 1-a-1). Habilidade:
  **contagem até 10, cardinalidade com quantidade maior**.
- **Recompensa + conexão:** o gato entrega a **CHAVE**; 3º lampião acende; a chave abre a cabana → **BEAT A**.
- **Falas:**
  - Byte: "O gato quer ver a gente colher todas antes de soltar a chave. **Como a gente garante que não pulou nenhuma?**"
  - Gato: "Contou tudo? Então a chave é sua. Cuida bem da despensa!"

### BEAT A (alívio, ~2,5 min) — "Dentro da Despensa" · beat: **entrar (interior + lampião)**
- **Interação:** o Byte destranca a cabana; **entra no interior aconchegante** (luz de lampião
  tremulando). Há **prateleiras vazias** esperando a colheita. Sem conta — respiro e tensão dramática:
  mostra QUANTO falta encher e apresenta as prateleiras das próximas fases.
- **Falas:**
  - Byte (olhando as prateleiras vazias): "Uau… tem muito espaço pra encher. **Será que a gente consegue antes de a geada chegar?**"
  - Tico: "Cada prateleira precisa da quantidade certinha. Bora!"

### FASE 4 — "A Prateleira do Seis" · tarefa: **trazer_exato (alvo=6, n=9)**
- **História/gancho:** A 1ª prateleira só aguenta EXATAMENTE 6 potes — nem mais (transborda/estraga),
  nem menos (não protege do frio). Há 9 frutas por perto (dá pra trazer demais → a criança PARA no 6).
- **Tarefa:** levar frutas até a prateleira e ENTREGAR até chegar em 6, reconhecendo "o bastante" e
  devolvendo o excesso. Habilidade: **cardinalidade exata, noção de mais/menos/igual, parar na quantidade pedida**.
- **Recompensa + conexão:** prateleira 1 cheia; 4º lampião acende. → F5.
- **Falas:**
  - Byte: "O Tico pediu exatamente seis. **Como a gente sabe que já chegou no seis — e que não passou?**"
  - Byte (se trouxe a 7ª): "Opa, essa sobrou! **Já temos seis — o que a gente faz com a que sobrou?**"

### FASE 5 — "A Prateleira do Oito" · tarefa: **trazer_exato (alvo=8, n=10)**
- **História/gancho:** A geada começa a aparecer nas bordas (efeito de clima/frio). A prateleira
  grande precisa de exatamente 8. Ainda uma a uma… e o Byte estranha a lentidão.
- **Tarefa:** trazer exatamente 8 (de 10 disponíveis). Habilidade: **cardinalidade exata até 10;
  comparar o que tem com o que falta ("faltam quantas para o oito?")**.
- **Recompensa + conexão:** prateleira 2 cheia; 5º lampião acende. MAS sobrou uma montanha de frutas.
  O Byte faz a **pergunta-semente da dezena**. → F6.
- **Falas:**
  - Byte: "Faltam quantas pra chegar no oito? **Dá pra saber sem contar tudo de novo?**"
  - Byte (gancho da dezena): "Tanta fruta, uma de cada vez… **e se a gente juntasse elas em grupos pra ir mais rápido?**"

### FASE 6 — "Sacolas de Dez" · tarefa: **agrupar (n=20)**
- **História/gancho:** O Tico mostra as **sacolas que cabem exatamente 10** (asset `sacola10`).
  Descoberta: em vez de contar 1,2,3…20, dá pra pegar sacolas cheias e contar de DEZ em DEZ.
- **Tarefa:** juntar 20 frutas com 2 sacolas de dez — a criança conta "dez… vinte". Habilidade:
  **agrupamento de base 10, contar de 10 em 10, introdução da DEZENA (10 unidades = 1 dez)**.
- **Recompensa + conexão:** a despensa enche muito mais rápido (recompensa = EFICIÊNCIA visível);
  6º lampião acende. → F7.
- **Falas:**
  - Byte (descoberta guiada): "Cada sacola tem dez… **se a gente pega duas sacolas cheias, quanto isso dá?**"
  - Byte: "Foi bem mais rápido, né? **Você percebeu o padrão? De quanto em quanto a gente contou?**"

### FASE 7 — "A Despensa Cheia" · tarefa: **agrupar (n=30)**
- **História/gancho:** Reta final da despensa. Agora 3 sacolas de dez.
- **Tarefa:** juntar 30 contando 10→20→30, fechando a despensa. Habilidade: **consolidar dezenas
  (10,20,30)**. É aqui que o conceito é **NOMEADO de leve**: "isso que a gente fez — juntar de dez em
  dez — tem nome: é uma DEZENA."
- **Recompensa + conexão:** despensa CHEIA e o **ÚLTIMO lampião** acende → a trilha INTEIRA brilha do
  começo até a Grande Macieira, revelada ao fundo pela 1ª vez. Mas a noite fecha e a geada aperta. → **BEAT B**.
- **Falas:**
  - Byte: "Dez, vinte, trinta! **Percebeu como junto de dez em dez a gente conta um montão sem se perder?** Isso tem um nome: dezena!"
  - Tico: "A despensa está CHEIA! Olha a trilha toda acesa lá até a Grande Macieira!"

### BEAT B (alívio, ~3 min) — "A Noite Mais Fria" · beat: **dormir → amanhecer (fogueira + ciclo dia/noite)**
- **Interação:** a hora mais fria antes do amanhecer. Os amiguinhos (Tico, gato, passarinho) acendem
  uma **fogueira** perto da cabana. O Byte **chega perto da cama e dorme um pouquinho** enquanto a
  despensa e os lampiões protegem todos. **Amanhece devagar** (o céu clareia). Sem conta — beat
  emocional que faz a jornada respirar e prepara o clímax.
- **Falas:**
  - Tico: "Descansa, Byte. A despensa cheia e os lampiões acesos vão nos aquecer até o sol nascer."
  - Byte (bocejando): "A gente conseguiu encher tudo a tempo… **você acha que a Grande Macieira vai acordar?**"

### FASE 8 / FINAL — "Acordar a Grande Macieira" · tarefa: **contar (aplicação-celebração)**
- **História/gancho:** Amanhece. O caminho aceso leva à Grande Macieira, adormecida e coberta de geada.
  Ela só desperta se a criança lhe **apresentar a colheita completa**.
- **Tarefa final:** a criança leva a última cesta e, com o Byte e os amiguinhos, faz a **contagem da
  colheita** (aplicação leve de contar/dezena — sem dificuldade nova, é celebração). Ao concluir, toca
  a Árvore para "acordá-la".
- **FINAL ESPETACULAR:** ao toque, a **geada DERRETE** subindo pelo tronco; a Grande Macieira **acorda,
  brilha dourada e FLORESCE** — flores e frutas brotam, uma **onda de calor** varre o pomar (o frio azul
  vira luz quente/rosada), os lampiões pulsam, **borboletas e passarinhos** enchem o céu, cai uma
  **chuvinha de pétalas**. Festa em volta da fogueira. A Árvore agradece pelo nome (voz): "Obrigada,
  Guardiã da Contagem!"
- **Reflexão (Byte, na ordem da Filosofia — conceito por último, sem tom de prova):**
  - "Você salvou o Pomar da geada! Encheu a despensa e acendeu o caminho todo."
  - "**O que você descobriu hoje que fez a gente ir mais rápido?**" (a criança lembra da dezena).
  - Fecho de sentimento: "Hoje a gente não respondeu perguntas… **a gente salvou um pomar inteiro.** E,
    sem nem perceber, você aprendeu a contar, a pôr em ordem e a juntar de dez em dez."

---

### Como a HISTÓRIA costura tudo (visível no jogo)
1. **Fio condutor único:** a GEADA que se aproxima (relógio dramático) + a despensa que enche prateleira
   a prateleira + a trilha que sai do escuro lampião a lampião. Progresso FÍSICO, não fases soltas.
2. **Escada pedagógica limpa:** contar 1-a-1 (F1) → ordem (F2) → contar maior (F3) → quantidade exata /
   mais-menos (F4-F5) → agrupar de dez / dezena (F6-F7) → aplicação-celebração (F8). Cada mecânica NASCE
   de uma necessidade do enredo (a prateleira do 6; o "jeito mais rápido" que abre a dezena).
3. **Byte SEMPRE pergunta** (nunca dá a resposta); "dezena" só é NOMEADA na F7/F8. Erro = consequência no
   mundo (frutinha treme, fruta sobra), nunca X vermelho.
4. **Beats de reuso encaixados no enredo, não decorativos:** chave→abre despensa (F3/Beat A);
   interior+lampião (Beat A); fogueira+dormir+amanhecer (Beat B); clima/geada; NPCs vivos; path que acende.

---

## 3. SCHEMA DE DADOS — `mundo.jornada`

Bloco NOVO e OPCIONAL ao lado de `mundo.aula`. Se `mundo.jornada` existir, o motor a executa fase a
fase; se não, cai no legado `mundo.aula`. Uma fase `tipo_beat:"tarefa"` REUSA exatamente o objeto
`round` que a aula já entende (mesmos tipos `contar/ordenar/trazer_exato/agrupar`). O montador já
injeta o mundo inteiro como `MUNDO=__MUNDO_JS__`, então a jornada viaja para o JS sem nova plumbing.

### 3.1 Estrutura

```
mundo.jornada = {
  "id":            "<slug>-jornada-v1",       // estável — chave de SAVE
  "objetivo":      "problema-mãe do mundo (o que o mundo PRECISA)",
  "tema_chaves":   ["geada","colheita","tico","despensa","dezena"], // léxico p/ portão de coerência
  "tempo_alvo_min": 52,                        // calibração (soma de tempo_est_min + final ∈ [48,56])
  "fases":         [ <FASE>, ... ],            // ORDENADAS; a ordem É o arco
  "final": {                                   // desfecho autoral — OBRIGATÓRIO
    "id": "final",
    "titulo": "Acordar a Grande Macieira",
    "texto": "fala que FECHA o enredo",
    "recompensa": { "tipo":"selo","id":"trofeu_guardia","icone":"&#127942;","texto":"Guardiã da Contagem" },
    "cena": "amanhecer_festa|porta_abre|arvore_floresce"   // gatilho visual (reusa efeitos do motor)
  }
}
```

### 3.2 Objeto `<FASE>` (o coração — campos opcionais por tipo)

```
{
  "id":            "f1",                        // único; chave de SAVE/gate
  "titulo":        "O Byte Chega ao Pomar Gelado",
  "tipo_beat":     "tarefa|interacao|dormir|andar|final",
  "historia_beat": "1-2 frases de enredo (balão do Byte/NPC)",
  "falas":         ["id_audio_intro","id_audio_dica"],   // ids em dados.falas (voz gerada)
  "tempo_est_min": 5,

  // — só quando tipo_beat=="tarefa" (REUSA 1:1 o round da aula) —
  "mecanica":      "contar|ordenar|trazer_exato|agrupar",
  "params":        { "n":3, "alvo":6, "pedido":"O Tico", "cesta":{"x":520,"y":780} },
  "meta":          "colher e contar 3 frutas",

  // — só quando tipo_beat in (interacao|dormir|andar) (REUSA blocos do motor) —
  "interacao":     { "acao":"entrar_cabana|abrir_com_chave|dormir|acender_lampiao|pegar_item",
                     "prop":"cabana", "efeito":"noite->dia" },

  // — comum a TODA fase que produz progresso —
  "recompensa":    { "tipo":"chave|item|selo|abre_caminho|amanhece|lampiao",
                     "id":"lampiao_1", "icone":"&#128161;", "texto":"O 1º lampião acendeu!" },

  // — costura para a próxima parada —
  "transicao":     { "tipo":"andar_path|teleporta|abre_porta",
                     "de":[520,780], "ate":[900,520],
                     "gate":"recompensa:lampiao_1",         // pré-requisito p/ liberar a próxima fase
                     "fala":"Onde tem luz, dá pra seguir!" }
}
```

### 3.3 Exemplo JSON concreto (3 fases da jornada-piloto — F1 tarefa, Beat A interação, F4 tarefa)

```json
"jornada": {
  "id": "pomar-jornada-v1",
  "objetivo": "A primeira geada do inverno vem hoje à noite; o pomar só sobrevive se a despensa encher e a trilha acender antes do amanhecer, para acordar a Grande Macieira.",
  "tema_chaves": ["geada","inverno","colheita","tico","despensa","lampiao","dezena","macieira"],
  "tempo_alvo_min": 52,
  "fases": [
    {
      "id": "f1",
      "titulo": "O Byte Chega ao Pomar Gelado",
      "tipo_beat": "tarefa",
      "historia_beat": "O Tico tirita de frio: a geada vem à noite e a despensa está vazia. Três frutinhas caíram na entrada.",
      "falas": ["f1_intro_contar", "f1_dica_contar"],
      "tempo_est_min": 5,
      "mecanica": "contar",
      "params": { "n": 3, "cesta": { "x": 520, "y": 780 } },
      "meta": "tocar e contar 3 frutinhas, uma a uma",
      "recompensa": { "tipo": "lampiao", "id": "lampiao_1", "icone": "&#128161;",
                      "texto": "A 1ª cesta encheu — e o 1º lampião da trilha acendeu!" },
      "transicao": { "tipo": "andar_path", "de": [520,780], "ate": [760,640],
                     "gate": "recompensa:lampiao_1",
                     "fala": "Onde tem luz, dá pra seguir. Vamos!" }
    },
    {
      "id": "beatA",
      "titulo": "Dentro da Despensa",
      "tipo_beat": "interacao",
      "historia_beat": "Com a chave do gato, o Byte destranca a cabana e entra: prateleiras vazias esperando a colheita.",
      "falas": ["beatA_prateleiras"],
      "tempo_est_min": 3,
      "interacao": { "acao": "entrar_cabana", "prop": "cabana", "efeito": "interior_lampiao" },
      "recompensa": { "tipo": "abre_caminho", "id": "despensa_aberta", "icone": "&#127968;",
                      "texto": "A despensa abriu! Agora é encher cada prateleira." },
      "transicao": { "tipo": "abre_porta", "de": [900,520], "ate": [940,560],
                     "gate": "recompensa:despensa_aberta",
                     "fala": "Cada prateleira precisa da quantidade certinha. Bora!" }
    },
    {
      "id": "f4",
      "titulo": "A Prateleira do Seis",
      "tipo_beat": "tarefa",
      "historia_beat": "A 1ª prateleira só aguenta exatamente 6 potes — nem mais, nem menos.",
      "falas": ["f4_intro_exato", "f4_dica_sobra"],
      "tempo_est_min": 6,
      "mecanica": "trazer_exato",
      "params": { "n": 9, "alvo": 6, "pedido": "A prateleira", "cesta": { "x": 940, "y": 560 } },
      "meta": "trazer exatamente 6 frutas e devolver o que sobrar",
      "recompensa": { "tipo": "lampiao", "id": "lampiao_4", "icone": "&#128161;",
                      "texto": "Prateleira 1 cheia — 4º lampião aceso!" },
      "transicao": { "tipo": "andar_path", "de": [940,560], "ate": [1080,500],
                     "gate": "recompensa:lampiao_4",
                     "fala": "Falta a prateleira grande agora." }
    }
  ],
  "final": {
    "id": "final",
    "titulo": "Acordar a Grande Macieira",
    "texto": "A geada derreteu, a Grande Macieira floresceu e o calor voltou ao pomar. Você salvou o inverno inteiro — e, sem perceber, aprendeu a contar, a pôr em ordem e a juntar de dez em dez!",
    "recompensa": { "tipo": "selo", "id": "trofeu_guardia", "icone": "&#127942;",
                    "texto": "Troféu: Guardiã da Contagem" },
    "cena": "arvore_floresce"
  }
}
```

**Regra de ouro visível no exemplo:** `f1(tarefa) → beatA(interação) → f4(tarefa)` já é o loop-FORMA
(tarefa → recompensa → interação → andar → próxima tarefa), com um final que fecha o enredo. Cada
`params` de fase-tarefa é EXATAMENTE o `round` que a aula legada consome → 100% de reuso da mecânica.

---

## 4. MUDANÇAS MÍNIMAS NO MOTOR (todas guardadas por `MUNDO.jornada` → default idêntico)

> Referências de linha conforme o mapeamento do engenheiro de games sobre `kit-floresta.py`
> (~1150 linhas). Podem deslocar após o polimento em curso — reconferir antes de codar.

1. **Injeção (montar.py, ~2 linhas):** expor `MUNDO.jornada`. O montador já injeta o mundo inteiro,
   então custo ~0. Adicionar só validação de `falas` (ids existem em `dados.falas`) e de `de/ate`
   coerentes com `mundo.path` (aviso, não erro).
2. **`noite` roteirável (kit ~L925):** com `MUNDO.jornada`, CONGELAR o ciclo automático de dia/noite;
   `noite` só muda por beat `dormir` (override `noiteForce`). Sem jornada, ciclo automático como hoje. (~6 linhas)
3. **Extrair 2 helpers de GATE do código chave/arco (kit ~L953-958):** `gatePega(alvo,raio,onDone)` e
   `gateChega(alvo,raio,onDone)` — mesma checagem de proximidade já existente, generalizada; usada por
   beats `andar/pegar` e por tarefas `chegar/pegar`. (~15 linhas, refatoração)
4. **`jornadaUpdate(dt,t)` + interpretador de beats (NOVO, isolado, no-op se `!MUNDO.jornada`):** chamado
   no loop junto de `rodadaUpdate` (~L962). Contém o FSM `{ENTRA_BEATS, TAREFA, RECOMPENSA, SAI_BEATS,
   TRANSICAO}` e o loop de beats (`fala/andar/dormir/entrar/recompensa`). (~120 linhas NOVAS)
5. **Ganchos de transição no motor de rodadas (kit ~L604-621):** onde hoje `rodadaUpdate` chama
   `aulaAvanca()` ao fim da transição, desviar para `jornadaAvancaDepoisDaTarefa()` quando
   `MUNDO.jornada` existir (senão, comportamento atual). (~8 linhas)
6. **Fade de cena + (opcional) sub-cenário p/ beat `entrar` (kit ~L1077):** `jFade` (0..1) no fim do
   frame. **MVP LEVE recomendado:** mesmo mapa + teleporte + escurecer + acender lampião (prop já
   existe). ~15 linhas. Interior REAL com troca de tileset → ADIAR (médio, ~40 linhas).
7. **HUD/overlay:** reaproveitar `aulaOverlay`/HUD para "Fase X" e a fala de recompensa. (~5 linhas)

**Total realista: ~150-190 linhas NOVAS**, quase todas dentro de `jornadaUpdate` + interpretador de
beats. Zero reescrita de render, física, NPCs ou das 4 mecânicas.

**SAVE:** `edujornada_<jornada.id>` guardando `{ faseIdx, faseId, inv:{recompensas}, progresso_fase,
concluido, v }`. Retomar = recarregar no INÍCIO da fase (re-roda os beats curtos de entrada). Se
`faseId` sumiu (IA re-autorou o arco) → descarta SAVE, começa do 0. Fallback `try/catch` como o
`_salvaProg` atual.

---

## 5. PLANO DE IMPLEMENTAÇÃO SEQUENCIADO (a construção começa DEPOIS do polimento do motor)

> **Pré-condição:** o outro engenheiro terminou o polimento de `kit-floresta.py`. Combinar quem
> encosta nas regiões L604-621, L925 e L953-962 ANTES de codar (alto risco de conflito de merge).

**Passo 0 — Contrato do `round` (bloqueante):** confirmar com o engenheiro paralelo que o schema do
`round` da aula (`tipo/n/alvo/pedido/cesta`) permanece estável. O dispatcher de fase-tarefa reusa esse
objeto 1:1 — se mudar, alinhar primeiro.

**Passo 1 — Schema + dados (sem tocar no motor):** criar `mundo.jornada` na jornada-piloto num mundo
NOVO/cópia de trabalho (NÃO nos 3 mundos existentes). Escrever as 10 fases + final conforme §2/§3.

**Passo 2 — Falas (produção de voz):** listar todos os ids de `falas` (Byte pergunta, Tico, gato,
Árvore, reflexão) em `dados.falas`; gerar mp3 via `gerar-audio.yml` (edge-tts). O montador valida os ids.

**Passo 3 — Injeção + guardas (motor, mudanças 1-2):** expor `MUNDO.jornada`; congelar `noite` sob
jornada. Verificar que os 3 mundos legados renderizam IDÊNTICOS (jornada null).

**Passo 4 — Helpers de gate (mudança 3):** extrair `gatePega`/`gateChega` do código chave/arco; testar
que o beat `chave→arco` legado continua funcionando.

**Passo 5 — FSM + interpretador de beats (mudança 4):** implementar `jornadaUpdate` com os 5 estados e
os beats `fala/andar/dormir/entrar/recompensa`. Beat `entrar` = MVP LEVE (teleporte+darken+lampião).

**Passo 6 — Ganchos de transição (mudança 5):** desviar o pós-transição do motor de rodadas para a
jornada quando `MUNDO.jornada` existir. Aqui as fases-tarefa passam a rodar de verdade.

**Passo 7 — Recompensa visível + fade + HUD (mudanças 6-7):** lampião que acende por fase, despensa que
enche, `jFade`, overlay "Fase X". A recompensa VISÍVEL é o que dá sensação de progresso.

**Passo 8 — SAVE de jornada:** `edujornada_<id>` (faseIdx + inventário); invalidação por `faseId` sumido.

**Passo 9 — Final autoral:** cena `arvore_floresce` (arvore em escala + glow + pétalas + tint frio→quente),
reflexão do Byte na ordem da Filosofia.

**Passo 10 — Portões (audit/):** estender sob `--avisa` primeiro, depois bloqueante:
- `portao_coerencia` modo jornada: arco na ordem (nenhum `gate` cita recompensa futura); final presente e
  não-vazio; coerência de tema por whitelist (`tema_chaves`); nenhuma fase-tarefa sem `mecanica/params`.
- `portao_pedagogia`: progressão não-decrescente; **≤2 fases-tarefa seguidas sem beat**; calibração
  `sum(tempo_est_min)+final ∈ [48,56]`; mínimo de fases-tarefa (protagonismo, não vira cutscene).
- `portao_variedade`: NPC com `falas[]>=2`; falas de fase não repetem verbatim.

**Passo 11 — QA headless:** os beats são TEMPORAIS (como os balões) e o virtual-time do Chromium quase
não acumula — usar o driver `setInterval` já documentado no CLAUDE.md para fotografar cada fase. No
navegador real (60fps) roda normal. Enviar screenshots ao Marcos.

---

## 6. RISCOS CONSOLIDADOS E MITIGAÇÕES

| Risco | Mitigação |
|---|---|
| Motor em edição paralela toca L604-621/L925/L953-962 → conflito de merge | Combinar as regiões ANTES de codar (Passo 0); só começar após o polimento. |
| Enum de `interacao.acao`/`recompensa.tipo` que o motor não anima → fase trava | Fallback beat genérico ("ganhou X" + andar) + gate que só aceita verbos do catálogo suportado. |
| Interior REAL (troca de tileset) passa de trivial | MVP LEVE (teleporte+darken+lampião no mesmo mapa); adiar multi-mapa. |
| Ciclo dia/noite automático escurece a cena de contagem sozinho | Com jornada, `noite` só muda por beat `dormir` (mudança 2). |
| SAVE preso a `jornada.id` → re-autoria descarta progresso | Aceitável em sala; documentar ("mudou o mundo = recomeça"); salvar só no início da fase. |
| `agrupar`/dezena pode ser avançado p/ início do 1º ano | Entra como descoberta leve (F6/F7); fácil rebaixar os `n` para reforço de contagem grande se o pedagogo pedir. |
| Falas novas precisam virar áudio (edge-tts) | Passo 2 dedicado; montador valida ids e emite "(sem audio) <id>". |
| Efeito geada/frio→calor do final depende do tint do motor-vivo | Confirmar com o engenheiro que o tint vira de azul-frio p/ quente na cena final. |
| Peso do `index.html` | Jornada = só DADOS + ~180 linhas; manter interiores leves; orçar arquivo < ~1,5 MB. |

---

## 7. RESUMO DE UMA LINHA

10 paradas (8 fases-tarefa + 2 beats de alívio) contando a jornada **"A Noite da Grande Geada"** em
~52 min, executadas por um FSM data-driven (`mundo.jornada`, opcional) que ORQUESTRA beats e delega as
tarefas ao motor de rodadas EXISTENTE — ~150-190 linhas novas isoladas, zero regressão nos mundos atuais,
construção só após o polimento do motor.
