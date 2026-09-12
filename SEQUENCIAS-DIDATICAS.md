# 📚 SEQUÊNCIAS DIDÁTICAS — a LEI do formato "folha viva"

> **Este documento é só destas atividades.** As atividades do MOTOR (o Grande
> Circo do Teo, a Feirinha, a Expedição da Divisão, as provas) seguem o
> `MANUAL-MESTRE.md` e o `_padrao/ESQUELETO/CONTRATO.md`. **Aqui é outro
> formato, com outras regras, e misturar os dois já custou caro.**
>
> Pedido do Marcos que fez este arquivo existir (12/set/2026):
> *"registre um documento para essas nossas novas atividades separado das
> outras, e registre minhas regras, o que aprendemos, os erros, etc."*
>
> **Quem chega aqui sem memória: leia este arquivo inteiro antes de tocar em
> qualquer caderno de sequência didática.** Depois dele, o `POTE-*.md` do degrau
> em que vai mexer.

---

## 1. O que é uma "folha viva"

É o **caderno de folhas** que a criança vira uma a uma, como o caderno de papel
que o professor imprime — só que cada folha **funciona**: a figura fala, a peça
arrasta, o teclado escreve, o erro responde.

**Não é** uma atividade do motor com outro nome. Diferenças que importam:

| | Motor (Esqueleto) | **Folha viva** |
|---|---|---|
| Conteúdo | `conteudo.json` → fases | `var ITENS` (potes) + `folhas.js` |
| Unidade | a FASE (uma tela, um gesto) | a FOLHA (vários itens na mesma tela) |
| Origem | roteiro nosso | **uma folha impressa de verdade** |
| Navegação | trilha/lição | livro, com "Folha N de M" |
| Portões | a banca inteira alcança | **a banca do motor NÃO alcança** (§7) |

**As dez sequências que existem hoje** estão indexadas em
`_sequencias/ALFABETIZACAO-1ANO.md`, e o crivo de cada uma no `POTE-*.md`
correspondente.

---

## 2. ⭐⭐ AS REGRAS DO MARCOS — ditas por ele, com as palavras dele

### REGRA ZERO — "Nunca chute nunca invente" (12/set/2026)
Quatro palavras, e vêm antes de todas as outras. Número sem fonte não sai da
minha boca; **e "li no log" só vale se eu tiver aberto o MODELO que gerou o
log**. Constante inventada dentro de portão tem que estar escrita no comentário
**e impressa na saída** como `PALPITE DECLARADO`. O que não dá para medir daqui,
eu digo que não dá e mostro quem pode medir. E nunca dizer que fiz o que não fiz.
> *O teste, antes de mandar qualquer número:* **de onde veio, e o que eu teria
> que abrir para ele estar errado?**

### REGRA DO TAMANHO — no mínimo **25 folhas** por sequência (12/set/2026)
Palavras dele: *"eu acredito que cada sequência precise de no mínimo 25 folhas"*.
**A medição dá razão a ele** — a conta está no §4. O mínimo é 25; a meta de
tempo é a aula de **55 minutos**.

### REGRA DA ORIGEM — "veja o que as atividades pedem que o estudante FAÇA"
Palavras dele (set/2026), e depois, mais direto: *"seria legal se vc conseguisse
recriar como está ali, a interatividade necessária para executar as tarefas"*.
Folha nossa **nasce de uma folha impressa de verdade**, colhida da internet, e
recria **o gesto** dela — não "algo inspirado nela". Ver o processo no §5.

### REGRA DA VOZ
- **Toda tela é narrada**, com voz de verdade (Edge TTS, `pt-BR-AntonioNeural`).
- **Alto-falante em TODA resposta que a criança toca.** Palavras dele: *"o
  alto-falante nas respostas também, para ajudar os alunos que não sabem ler"*.
- **`falas.json` é a VERDADE**: texto escrito ali = voz gravada. MP3 não se lê.

### REGRA DAS DUAS PORTAS
Toda folha com teclado na tela aceita **também o teclado de verdade**
(`document.onkeydown`); toda folha de arrastar aceita **também o toque simples**.
Palavras dele: *"seria interessante se o aluno além de teclar no teclado virtual
funcionasse se ele tocasse no teclado de verdade, as duas opções"*.

### REGRA DA REPETIÇÃO SEGUIDA
Mecânica que repete vem em **BLOCO COLADO**, subindo um degrau dentro do bloco —
nunca espalhada. Palavras dele: *"as crianças me dizem 'isso eu já fiz, tô
fazendo de novo'"*.

### REGRA DO REUSO DO BANCO
Antes de pedir arte, **consultar o banco** (`_banco/index.json`). Mascote pode
ser reaproveitado; **mascote novo só quando ele pedir**.

### REGRA DA PUBLICAÇÃO
*"pode publicar, pode sempre publicar a menos que eu diga para esperar"* — desde
que a banca tenha aprovado. **E atividade nova NÃO entra no hub** até ele pedir
com todas as letras: nasce no repositório dela e o link vai para ele.

### REGRA DO CONSERTO DUPLO
Defeito que chega perto da criança tem conserto de **duas partes**: arrumar o
código **e** criar/estender o portão que o pega sozinho da próxima vez. Sem a
segunda parte, o trabalho não está feito.

---

## 3. ⚠️ OS ERROS JÁ PAGOS NESTE FORMATO — um por um

> Esta lista existe para não se repetirem. Cada linha custou uma rodada com o
> Marcos, ou chegou até a criança.

### 3.1 A resposta estava IMPRESSA no enunciado — em 5 cadernos NO AR
A figura da mola vinha com a legenda **MOLA** logo abaixo e, embaixo dela,
`[ ][ ] L A` para a criança completar. **A resposta impressa dois centímetros
acima da pergunta.** Quem lia um pouco resolvia o caderno **copiando**, e a
folha media zero.

- **Causa:** o `figComSom`, clonado por todos os cadernos, escrevia o nome da
  figura por baixo dela.
- **Alcance:** `_roda1` (9 folhas), `_ini1` (22 itens), `_mont1` (20), `_let1`
  (21) e `_jogo1` (32 — **uma FORCA com a palavra escrita na tela**).
- **Conserto:** a legenda **não some** — fica invisível (`visibility`, para o
  espaço não pular) e **aparece no instante do acerto**. Assim a criança que
  chama a luneta de "telescópio" continua protegida.
- **Portão:** `_qa/resposta_impressa.py` (1i4 na banca).
- ⚠️ **Quem pegou foi uma FOTO, não um portão.** Regra que sai daqui: **depois
  de montar, OLHAR a tela** — e o que a foto achar vira portão no mesmo commit.

### 3.2 A sílaba saía da palavra ERRADA
A folha mostrava a figura da LATA e o alto-falante dizia LARANJA. Palavras dele:
*"não entendi muito o sentido da primeira atividade, pois cita laranja e aparece
lata"*. A sílaba nunca é sintetizada solta (senão a voz soletra): é recortada de
dentro de uma palavra gravada, e o gerador escolhia a fonte pela **ordem
alfabética**. → Portão `_qa/silaba_fonte.py` (0b10).

### 3.3 "Voz de navegador" = o MP3 não chegou ao site
Palavras dele: *"as sequências didáticas estão com voz de navegador"*. Não era
defeito de código: o `entregar.yml` tinha falhado e a pasta subiu **sem um único
mp3**; o `falar()` caía no sintetizador do Chrome. **Eu medi no container (onde
tocava perfeito) e disse que estava tudo bem — olhando para o lugar errado.**
→ Ferramenta `ouvir-no-ar.yml`: pergunta ao **site publicado**.

### 3.4 O commit sem a marca `[entregar]` não publica nada
Um conserto ficou commitado e não publicado, e eu disse a ele que estava no ar.
→ **Conferir a marca antes de empurrar**, e depois **ler o carimbo**
`_status/entrega-<repo>.json` comparando o `index` com `sha1sum <arquivo> | cut -c1-12`.

### 3.5 Os ids escritos à mão faziam o relatório sair ZERO
Cada folha gravava `n6_0` à mão e o `idsDaPagina` repetia a mesma tabela à mão:
dois lugares para combinar, os dois sintaticamente corretos. Quando a ordem das
folhas mudava, **o relatório do professor saía zero com a folha toda
respondida**, sem erro no console. Aconteceu duas vezes.
→ **A POSIÇÃO É A IDENTIDADE**: a folha da posição 7 usa o pote `p7`, grava
`n7_*` e fala `p7enun`, tudo derivado de `pi`. Não há segunda lista.

### 3.6 O portão da duração aprovava por causa do próprio erro
Ele cobrava **25 s por item** (o preço de DIGITAR uma palavra no teclado) em
folha onde a criança só **toca** numa opção — e usava esse número inflado para
escrever *"duracao ok: enche a aula"*. Quem desconfiou foi o Marcos:
*"eu não acredito que 10 folhas durem uma aula toda"*.
→ O gesto agora é lido no corpo da própria folha.

### 3.7 "2,6 palavras por segundo" era invenção minha
O tempo de voz saía de `palavras / 2.6`. Esse 2,6 **eu inventei**, sem cronômetro
e sem fonte, e ele saía no log com cara de medida. **Medido em 890 mp3: a voz da
casa fala a 1,66–1,90 palavra/s — meu número era 37% rápido demais.**
→ `_qa/mp3_dur.py` lê a duração REAL contando os quadros do próprio arquivo.

### 3.8 O intruso que começava com a mesma letra
A folha dizia *"três começam com o mesmo pedacinho"* e mostrava MALA · MENINA ·
MOLA · MORCEGO. As três primeiras **não** começam com o mesmo pedacinho (MA, ME,
MO); o que têm em comum é a **roda**. E o intruso, *morcego*, **começa com M**: a
criança que o aceitava estava certa no que enxergava, e o app dizia que errou.

### 3.9 As folhas de ORIGEM também erram
Duas das 26 folhas colhidas ensinam separação silábica errada: **PORCO** como
exemplo de PO (é POR-CO) e **CIRCO** como exemplo de CI (é CIR-CO). E uma folha
de rima dava **BOCA / GOTA** como par (é assonância, não rima).
→ **Folha da internet é matéria-prima, não fonte confiável.** Toda palavra do
pote tem a separação declarada à mão e conferida.

### 3.10 Portão que acusa inocente se aprende a ignorar
O `silaba_fonte.py`, na estreia, acusou **21 recortes legítimos**. O
`resposta_impressa.py` acusou a folha cujo enunciado diz *"some a **letra** com a
vogal"* porque "LETRA" começa com "LE". → Toda regra nova de portão nasce com o
caso-limite conferido antes de entrar na banca.

### 3.11 Halo branco do recorte
15 figuras com a orla do fundo grudada na silhueta — invisível no branco, um
contorno leitoso no fundo colorido da folha. → `_padrao/tirar_halo.py` (inunda a
partir da BORDA, por vizinhança, com degradê: o branco de dentro da figura fica
intacto).

---

## 4. 📏 O TAMANHO DA SEQUÊNCIA — a conta, e por que 25 está certo

### O que foi MEDIDO (12/set/2026, com o relógio nos mp3 e o gesto lido da folha)

| Caderno | folhas | itens | duração | **min por folha** |
|---|---|---|---|---|
| O Desfile das Letras | 10 | 85 | 22–37 min | 2,2–3,7 |
| O Bando das Rimas | 10 | 80 | 24–41 | 2,4–4,1 |
| Bate-Palma das Palavras | 10 | 99 | 26–42 | 2,6–4,2 |
| A Tecla do Espaço Quebrou | 10 | 81 | 26–43 | 2,6–4,3 |
| O Grande Jogo das Palavras | 10 | 79 | 26–47 | 2,6–4,7 |
| A Família das Palavras | 10 | 95 | 29–43 | 2,9–4,3 |
| O Som que Abre | 10 | 103 | 30–51 | 3,0–5,1 |
| A Máquina de Juntar | 10 | 105 | 31–48 | 3,1–4,8 |
| A Letra que Muda Tudo | 10 | 99 | 31–51 | 3,1–5,1 |
| **A Roda das Sílabas** | **15** | 103 | **34–53** | 2,3–3,5 |

### A conta
A faixa existe porque há **duas crianças reais** na turma: a que só ouve o
retorno ("muito bem!") e a que toca no alto-falante de cada opção, erra, ouve a
dica. Entre uma e outra há **20 minutos** numa atividade de 1º ano.

Para a aula de 55 minutos:

| | folhas necessárias |
|---|---|
| pela criança **rápida** (só o retorno) | **18 a 25** |
| pela criança **devagar** (toca em tudo) | 11 a 16 |

> ⚠️ **SEGUNDA CORREÇÃO DO MESMO TIPO, no mesmo dia.** Eu tinha escrito aqui que
> a Máquina de Juntar tem 8 folhas e a Letra que Muda Tudo tem 7. **Têm 10 cada
> uma.** O número saiu de um `grep` no `novaFolha()` que não reconhecia todas as
> formas de sacar o pote. **Contagem de folha agora se faz no NAVEGADOR**
> (`PAGEL.length - 1`), que é onde a criança conta — a mesma lição da Regra
> Zero: se o modelo não foi aberto, o número mede o meu regex.
> Medido em 12/set: nove cadernos com **10 folhas** e a Roda com **15**.

**Por isso 25 é o número certo — e o Marcos chegou nele de ouvido.** Com 25
folhas a criança rápida enche a aula; com menos, ela termina com meia aula
sobrando, que foi exatamente o que ele viu.

### ⚠️ MAS 25 FOLHAS COBRA UMA MUDANÇA JUNTO, e sem ela faz mal

Se a criança rápida enche a aula com 25 folhas, a criança devagar leva **~85
minutos** — ela **não termina**. E hoje o fecho (o boletim animado, o parecer, o
relatório do professor, a medalha) **só existe depois da última folha**. Ou seja:
a criança mais lenta da turma, que é justamente quem mais precisa do elogio,
seria a única que nunca o veria.

**Então a regra completa é:**
1. **25 folhas no mínimo** — o pote do dia.
2. **O fecho tem que ser alcançável a qualquer momento.**
3. **O convite de 55 minutos continua** (`_padrao/RETOMAR.md`): quem volta na
   mesma aula continua de onde parou.

### ✅ O item 2 está FEITO nos dez cadernos (12/set/2026)

Sem ele, aumentar para 25 folhas pioraria a vida de quem já vai devagar — a
criança mais lenta da turma seria a única a nunca ver o próprio elogio. O que
mudou, e é contrato do formato daqui para a frente:

| | Como era | Como é |
|---|---|---|
| chegar ao fecho | só depois da última folha | **botão "Terminar"** na barra de baixo, a qualquer momento |
| título do fecho | "Caderno completo!" | "**O seu boletim de hoje**" quando não terminou |
| folha não aberta | barra com **0 de 8** | "**ainda não**", apagadinha — nunca um zero |
| estrelas e barras | sobre o caderno inteiro | **sobre o que ela tentou** |
| parecer da criança | objetivo não alcançado caía em "vale treinar" | **não entra em lista nenhuma** |
| a linha de resumo | — | "*Ana, você fez 4 de 15 folhas hoje — e olhe o que já dá para ver…*" |
| voltar | impossível | **"Voltar para o caderno"**, se ainda houver aula |
| relatório do professor | 4 folhas bem feitas viravam **"Precisa retomar"** | aviso de caderno não terminado + coluna **"do que fez"** + nota sobre o que foi feito + "*ainda não chegou a fazer (a aula acabou antes)*" |

⚠️ **O relatório era o pior dos dois.** Ele dividia os acertos pelo caderno
inteiro: quem fez 4 de 15 folhas, e as fez bem, aparecia com **21%** e conceito
**"Precisa retomar"**. Um julgamento errado com cara de medida, exatamente o que
a Regra Zero proíbe — só que contra a criança.

⚠️ **Tensão que eu NÃO mexi, e que é decisão do Marcos:** a nota credita o acerto
com ajuda (1,0 de primeira, 0,6 com ajuda), mas a tabela por objetivo conta só o
acerto **de primeira**. Por isso é possível ler "**Dominou**" ao lado de "nenhum
objetivo chegou a 75%". Não é defeito novo — é como a nota sempre foi — mas para
o professor soa contraditório. Mudar o critério é escolha pedagógica, não minha.

**Medido nos dez** (12/set): fecho no meio do caderno funciona, nenhuma barra em
zero, "Voltar para o caderno" retorna, zero erro de JS; leiaute em 6 tamanhos
com todo alvo ≥ 40 px.

---

## 5. 🛠️ O PROCESSO — como nasce uma sequência (e a ordem importa)

### Passo 1 — COLHER as folhas de verdade
`buscar-fotos.yml` com `imagens=<o que procurar>` e
`destino=_sequencias/folhas_d<N>`. ~26 folhas por degrau.
> O chat não tem internet; a colheita roda no GitHub Actions.

### Passo 2 — O CRIVO, folha a folha, com olhar de pedagogo
**Ler cada folha e anotar UMA coisa: o VERBO** — o que ela manda a criança FAZER
com o lápis na mão. Depois o veredito, com o motivo escrito, no
`_sequencias/POTE-<NOME>.md`:

- ✅ **entra** — o gesto serve a este degrau;
- ⛔ **é de outro degrau** — ensina coisa de antes ou de depois;
- ⛔ **fora do ano** — o currículo de Blumenau põe isso noutro ano;
- ⛔ **sem tarefa** — é cartaz de parede;
- ⚠️ **erra** — a própria folha ensina errado (§3.9).

> **Exemplo do que isso rende:** no degrau 9, 26 folhas → 15 entram, 5 são de
> outro degrau, **4 ensinam as famílias do C e do Q, que Blumenau situa no 2º
> ano**, 2 são cartaz. E apareceram **cinco gestos** que o caderno não tinha.

### Passo 3 — MONTAR, fiel ao comando
Cada folha recria o gesto da folha de origem. Mecânica que repete vem em bloco
colado (§2). **Nada de escolher do nosso cardápio: a folha é que manda.**

### Passo 4 — A VOZ
`python3 <pasta>/gerar_falas.py` → escreve `falas.json`, `silabas.json`,
`voz.txt` e remenda os blocos `FALAS`/`VOZOK`/`SILMAP` no `index.html`.

### Passo 5 — MEDIR (nunca pular)
```
bash _qa/previo.sh <pasta>                 # 39 portões de texto, ~3 s
node _qa/andar_folha.js <pasta>            # anda o caderno inteiro no navegador
node _qa/leiaute_mao.js <pasta>/index.html # 6 tamanhos de tela
python3 _qa/resposta_impressa.py <pasta>   # a legenda entrega a resposta?
python3 _qa/duracao.py <pasta>             # enche a aula?
python3 _qa/pedagogo_curriculo.py <pasta>  # o currículo citado existe?
```
**E OLHAR A TELA** — foto de cada folha nova, no celular e no PC. Metade dos
defeitos desta lista foi achada assim, não por portão.

### Passo 6 — PUBLICAR
Commit com a marca **`[entregar _pasta:repo]`** na mensagem → o `entregar.yml`
acorda sozinho, grava a voz que falta, publica e deixa
`_status/entrega-<repo>.json`. **Conferir o carimbo** (`index` ×
`sha1sum <arquivo> | cut -c1-12`) antes de dizer que está no ar.

---

## 6. 🧱 A ANATOMIA DO CADERNO (para clonar sem herdar defeito)

```
<pasta>/
  index.html      capa + CSS + os POTES + FALAS/VOZOK/SILMAP + relatório + dossiê
  folhas.js       uma função por folha + os ajudantes + DISTRA + OBJETIVOS
  gerar_falas.py  escreve o falas.json a partir dos potes
  curriculo.json  a habilidade de Blumenau, verbatim, por objetivo
  falas.json      a VERDADE da voz
  silabas.json    de qual palavra cada sílaba é recortada
  img/            prefixo próprio (ro_, in_, jg_…)
  audio/          gravado pelo entregar.yml
```

**Blocos que o gerador remenda** (não editar à mão):
`/*ITENS-INI*/…/*ITENS-FIM*/` · `/*FALAS-INI*/…` · `/*VOZOK-INI*/…` ·
`/*SILMAP-INI*/…` · `/*RODAS-INI*/…` · `<!--<dossie-html>-->`

**Ao CLONAR um caderno, trocar SEMPRE:** o prefixo das imagens e do áudio, o
`var PAL`, os potes, o `var DISTRA`, os `OBJETIVOS`, o `curriculo.json`, o
`CHAVE_LS` (a gaveta do "continuar de onde parou"), o `sw.js` e o
`manifest.json`. O `_qa/clone.py` (item 8) reprova qualquer coisa com o prefixo
de outra pasta.

**Contrato do id:** `"n" + pi + "_" + i` dentro da folha; a folha de LIGAR usa
`"l" + pi + "g" + i + "_" + chave` e se declara na constante `LIGAR`. Nunca
escrever número fixo (§3.5).

**Contrato do alvo:** o que MOSTRA a resposta de propósito (a testa da gaveta, o
modelo da roda) leva `data-alvo="1"`. Tudo o que não se declarar é tratado como
enunciado, e no enunciado a resposta não entra (§3.1).

---

## 7. ⚠️ O QUE A BANCA **NÃO** ALCANÇA NESTE FORMATO

Honestidade que vale mais que um "aprovado": vários portões da banca são do
MOTOR e, em folha viva, dizem **"NÃO MEDI"** — o que **não é "passou"**:

| Portão | Por que não alcança |
|---|---|
| `jogador.js` · `prova de sala` | procuram `telaCapa`/`FASES` |
| `contraste` · `encaixe` · `imagens` | abrem telas por nome |
| `0a pedagogo` (escada didática) | lê a cadeia de fases |
| `0b padrão da casa` (leque de gestos) | conta fases, não folhas |
| `entrega` · `enunciado_bate` · `figura_certa` | precisam de `conteudo.json` |

**O que cobre a folha viva hoje:** `andar_folha.js` (anda tudo, erro de JS e
figura quebrada), `leiaute_mao.js` (6 tamanhos, alvo ≥ 40 px), `resposta_impressa.py`,
`duracao.py`, `pedagogo_curriculo.py`, `silaba_fonte.py`, `revisor.py`, `clone.py`,
`duplicatas.py`, `pronuncia.py` (ASR), `halo.py`, `previo.sh`.

**A dívida (tarefa #104):** a escada didática e o leque de gestos **não são
medidos** em folha viva. Nenhum portão hoje diz se as 25 folhas sobem de
verdade, nem se um gesto passa de 40%. Enquanto isso não existir, quem responde
por isso é o crivo escrito do `POTE-*.md` — e ele é meu, não é medida.

---

## 8. 📋 O ESTADO DE HOJE (12/set/2026) — e a fila

| Degrau | Caderno | Folhas | Duração | Crivo com o VERBO? |
|---|---|---|---|---|
| 0 | O Desfile das Letras | 10 | 22–37 | ⛔ **sem colheita própria** |
| 1 | O Bando das Rimas | 10 | 24–41 | ✅ **28 folhas, 12/set** |
| 2 | Bate-Palma das Palavras | 10 | 26–42 | ✅ |
| 3 | A Família das Palavras | 10 | 29–43 | ✅ |
| 4 | O Som que Abre | 10 | 30–51 | ✅ |
| 5 | A Máquina de Juntar | 10 | 31–48 | ✅ |
| 6 | A Letra que Muda Tudo | 10 | 31–51 | ✅ |
| 7 | A Tecla do Espaço Quebrou | 10 | 26–43 | ✅ |
| 8 | O Grande Jogo das Palavras | 10 | 26–47 | ⛔ **sem colheita própria** (a colheita já chegou: `folhas_d8`) |
| 9 | **A Roda das Sílabas** | **15** | 34–53 | ✅ 26 folhas |

**Nenhum chega às 25 folhas** — o maior, a Roda, tem 15. **Oito de dez têm o
crivo do verbo**; faltam o degrau 0 e o 8, que nunca tiveram colheita própria.

> ⚠️ **CORREÇÃO, e ela é lição de método (12/set/2026).** Eu disse ao Marcos que
> só **quatro** de dez tinham crivo. Estava errado: contei com um `grep` que só
> reconhecia UM formato de tabela, e os `POTE-MONTAR`, `POTE-LETRA`,
> `POTE-FRASE` e `POTE-SOM` usam outro (*"As folhas que viraram folha, uma a
> uma"* + *"As folhas RECUSADAS — e o motivo de cada uma"*). É a **Regra Zero**
> me pegando: rodei uma medida sem abrir o modelo dela e repeti o número.
> O conserto de processo: **antes de contar arquivo com `grep`, abrir dois deles
> e ver se o padrão casa** — senão a contagem mede o meu regex, não o repositório.

### A fila, na ordem
1. **O fecho alcançável a qualquer momento** (§4) — vem antes das folhas novas,
   senão 25 folhas piora a vida de quem vai devagar.
2. **Crivo** dos degraus que não têm: **faltam só o 0 e o 8**. O degrau 1 foi
   feito em 12/set (28 folhas lidas uma a uma, `POTE-RIMA.md` §crivo — achou
   **seis** gestos que o caderno não faz, sendo o maior deles **PRODUZIR rima**,
   que quatro das 28 pedem e o nosso caderno não pede nenhuma vez). A colheita
   do 8 já está em `_sequencias/folhas_d8`; a do 0 ainda não foi feita.
3. **Crescer cada caderno até 25 folhas**, na ordem do mais curto.
4. **Portão da escada didática e do leque de gestos** para folha viva (#104).

---

*Escrito em 12/set/2026. Toda regra nova do Marcos e todo erro novo entram aqui,
no mesmo commit em que forem descobertos.*
