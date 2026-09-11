# Sequência didática — Alfabetização, 1º ano

> **Ideia do Marcos (9/set/2026):** *"criar sequências didáticas de alfabetização
> com essas atividades da internet, dando a interatividade que elas pedem; o
> pedagogo bola as sequências didáticas progressivas, baseado no currículo e nos
> livros"* — e, sobre o formato: *"tipo como fizemos as duas últimas atividades"*
> (A Fábrica de Palavras e A Oficina do Material Dourado: **folha viva**, um HTML
> só, caderno de folhas).
>
> Este documento é o **mapa**. Ele vem ANTES do código: o Marcos olha a escada
> inteira e corrige, e só então eu monto caderno por caderno.

## ⭐ ONDE A SEQUÊNCIA ESTÁ — TERMINADA (set/2026)

> **Os oito degraus estão montados, jogados até o fim e no ar.** Este bloco é o
> índice; o desenho de cada caderno está no `PARECER-PEDAGOGICO.md` da pasta dele
> e o crivo das folhas de origem no `POTE-*.md` correspondente.
>
> ⚠️ A numeração que vale é a da `SD-MONTADA-DE-FOLHAS-SOLTAS.md` (degraus 0 a 8).
> A tabela de "sete cadernos" mais abaixo neste documento é o ESBOÇO de julho, de
> antes da colheita das folhas — ficou como registro do plano, não como mapa.

| Degrau | Caderno | Pasta | No ar |
|---|---|---|---|
| 0 | **O Desfile das Letras** — a fila do alfabeto | `_abc1` | https://vidalprof.github.io/o-desfile-das-letras/ |
| 1 | **O Bando das Rimas** | `_rima1` | https://vidalprof.github.io/o-bando-das-rimas/ |
| 2 | **Bate-Palma das Palavras** — a palavra tem pedaços | `_sil1` | https://vidalprof.github.io/bate-palma-das-palavras/ |
| 3 | **A Família das Palavras** — sílaba inicial | `_ini1` | https://vidalprof.github.io/a-familia-das-palavras/ |
| 4 | **O Som que Abre** — o fonema e a letra | `_som1` | https://vidalprof.github.io/o-som-que-abre/ |
| 5 | **A Máquina de Juntar Palavras** — síntese silábica | `_mont1` | https://vidalprof.github.io/a-maquina-de-juntar-palavras/ |
| 6 | **A Letra que Muda Tudo** — o grafema | `_let1` | https://vidalprof.github.io/a-letra-que-muda-tudo/ |
| 7 | **A Tecla do Espaço Quebrou** — o espaço em branco | `_fra1` | https://vidalprof.github.io/a-tecla-do-espaco-quebrou/ |
| 8 | **O Grande Jogo das Palavras** — a revisão de tudo | `_jogo1` | https://vidalprof.github.io/o-grande-jogo-das-palavras/ |

### 👩‍🏫 O que o PROFESSOR vê (set/2026)

Os oito cadernos carregam, cada um, um **`curriculo.json`** que liga cada
objetivo do relatório a uma habilidade do **currículo de Blumenau copiada
verbatim** (1º ano, Alfabetização e Língua Portuguesa) — e um **dossiê
pedagógico dentro da atividade**, que abre pelo menu do professor (chave
`1275@`, a qualquer hora) e por um botão no relatório. Ele mostra as habilidades
citadas, a escada didática folha a folha, como a criança é avaliada e o que foi
medido antes de publicar. O portão `_qa/pedagogo_curriculo.py` (0b9) reprova se a citação
não existir no documento, se relatório e currículo deixarem de bater, se alguma
folha ficar sem objetivo que a meça ou se o dossiê sumir da tela.

As habilidades usadas nos oito degraus (todas conferidas palavra por palavra):
*Nomear as letras do alfabeto e ordená-las* · *Recitar parlendas, quadras,
quadrinhas, trava-línguas, com entonação adequada e observando as rimas* ·
*Segmentar oralmente palavras em sílabas* · *Comparar palavras, identificando
semelhanças e diferenças entre sons de sílabas iniciais, mediais e finais* ·
*Identificar fonemas e sua representação por letras* · *Reconhecer o sistema de
escrita alfabética como representação dos sons da fala* · *Relacionar elementos
sonoros (sílabas, fonemas, partes de palavras) com sua representação escrita* ·
*Reconhecer a separação das palavras, na escrita, por espaços em branco* ·
*Reconhecer que textos são lidos e escritos da esquerda para a direita e de cima
para baixo da página* · *Escrever, espontaneamente ou por ditado, palavras e
frases de forma alfabética – usando letras/grafemas que representam fonemas*.

**O que a sequência inteira soma:** ~100 folhas, ~660 itens, cerca de sete horas
de laboratório, todas as figuras do banco (arte nova: zero) e uma única mecânica
inventada em oito degraus — o **cortar a frase** do degrau 7. Todo o resto a casa
já tinha pronto e lapidado, que era exatamente o que a
`SD-MONTADA-DE-FOLHAS-SOLTAS.md` previa.

## 0. ⚗️ ISTO É UM TESTE — o que ele tem que responder

Palavras do Marcos (set/2026): *"isso é um teste para ver a possibilidade de ser
uma maneira nova de criar atividades"*. Então o entregável não são sete cadernos:
é **uma resposta**. E ela precisa de critério escrito ANTES, senão daqui a uma
semana teremos um caderno bonito e nenhuma conclusão.

**A pergunta que decide tudo:** *quanto do material da internet SOBREVIVE ao
crivo do currículo?*

- Se sobrevive muito, o método ganha de lavada: a parte cara da produção (decidir
  o quê, em que ordem, com quais itens) vem pronta e testada em sala.
- **Se sobrevive pouco, o método não economiza nada** — porque aí o pedagogo
  descarta quase tudo e eu escrevo o conteúdo do zero do mesmo jeito, só que
  depois de ter gasto tempo procurando. Este é o risco real, e é ele que o
  piloto mede.

**Os três números do teste**, medidos no caderno-piloto:
1. **Aproveitamento** — de N folhas achadas, quantas passam no crivo do pedagogo?
2. **Relógio** — do "quero uma aula de rima" até publicado, comparado com o
   caminho de hoje (a Fábrica de Palavras e a Oficina são a linha de base).
3. **Portões** — passa nos mesmos, com a mesma nota? O pedagogo assina sem
   ressalva grave?

## 1. O método — de onde vem cada coisa

### O fluxo, em quatro passos (do Marcos, set/2026)

1. **A matéria-prima são as atividades prontas da internet.** Nada de inventar
   conteúdo do zero: busca-se o que já existe escalonado e rodado em sala.
2. **O pedagogo faz a SELEÇÃO, e é aí que o trabalho dele acontece.** Ele olha o
   que veio e confere **contra o currículo**: serve a qual objetivo? é do ano
   certo? a ordem bate? O que não passa é descartado — não entra, não vira
   atividade.
3. **Ele confere os livros também**, pelo mesmo crivo (ver a ressalva abaixo).
4. **Só o que sobrou é que eu monto** — dando o gesto, a voz, o retorno, o
   relatório, e amarrando caderno com caderno.

**A curadoria vem ANTES da produção, e ela é do pedagogo.** O que chega até mim já
está aprovado no conteúdo; meu trabalho é dar interatividade ao que ele
selecionou, não escolher o que ensinar.


A unidade de produção deixa de ser a *atividade* e passa a ser a **sequência**.
Uma folha ensina; uma sequência **alfabetiza**. E são **três fontes**, cada uma
entrando com o que só ela tem:

| Fonte | O que ela dá | Quem manda |
|---|---|---|
| **Currículo de Blumenau** (`_curriculo/blumenau.txt`) | os **objetivos** — o que a criança tem que dominar | ⭐ manda sempre |
| **O livro** (sumário basta) | uma sugestão de **ordem e ritmo** | ⚠️ tambem e CONFERIDO contra o curriculo |
| **As folhas da internet** | os **itens** — palavras, figuras, exercícios já graduados | matéria-prima |

Nenhuma das três sozinha basta. O currículo diz *o quê* mas não diz *em quantas
aulas*; a folha da internet tem os itens mas nenhuma garantia pedagógica.

⚠️ **E o livro NÃO é autoridade** (correção do Marcos, set/2026). Eu tinha
escrito que ele "dá a ordem e o ritmo", como se mandasse. Não manda: **quem manda
é o currículo**, e o livro passa pelo mesmo crivo — o pedagogo confere se o que
ele traz está adequado ao ano. Livro é referência conferida, não fonte de
verdade.

### ⚠️ A REGRA QUE NÃO SE NEGOCIA — a folha dá o conteúdo, o GESTO se escolhe de novo

A folha da internet foi feita **para o papel**. Metade do que tem nela existe por
causa da limitação do papel: ligar com lápis, escrever na linha, pintar o
quadradinho. **Transpor direto produz "papel na tela" — que é PIOR que papel**,
porque a criança perde o lápis e não ganha nada em troca.

Então: a folha entra com o **conteúdo** (quais palavras, qual sílaba, qual
degrau) e com a **progressão**. O **gesto** se escolhe do zero, pelo encaixe —
exatamente como manda o pilar 4 do padrão da casa. "Escreva a sílaba que falta"
pode virar teclado na tela, mas também pode virar bater palma, ouvir-e-achar ou
escada de palavras. Quem decide é o encaixe, não o que estava impresso.

### ⚠️ O pedagogo é FILTRO NA ENTRADA, não carimbo na saída

Folha de blog costuma ser ruim: sílaba complexa cedo demais, palavra fora do
vocabulário da idade, ordem trocada. O pedagogo **escolhe quais folhas entram e
em que ordem** — antes de eu montar. Depois ele ainda assina o parecer, como já
faz (`PARECER-PEDAGOGICO.md`), mas o trabalho principal dele é aqui na entrada.

### E o direito autoral, em uma linha

A **sequência didática é conhecimento pedagógico** e se pode seguir; a **página
do livro é obra de alguém** e não se copia. Desenho, texto e leiaute saem
**nossos**, como já saem hoje.

## 2. Os objetivos do 1º ano (verbatim do currículo de Blumenau)

| # | Objetivo, como está escrito no currículo |
|---|---|
| **A** | Nomear as letras do alfabeto e **ordená-las** |
| **B** | Comparar palavras, identificando semelhanças e diferenças entre sons de **sílabas iniciais, mediais e finais** |
| **C** | **Segmentar oralmente** palavras em sílabas |
| **D** | **Relacionar** elementos sonoros (sílabas, fonemas, partes de palavras) com sua **representação escrita** |
| **E** | Reconhecer a separação das palavras, na escrita, por **espaços em branco** |
| **F** | Recitar parlendas, quadras, quadrinhas, trava-línguas… **observando as rimas** |

## 3. O diagnóstico que motiva a sequência

**A Fábrica de Palavras faz, em 11 folhas de UMA aula, o que uma sequência faria
em oito cadernos.** Ela é um bom **sobrevoo** — e como revisão ou diagnóstico é
ótima —, mas ninguém aprende sílaba medial em duas folhas. É a diferença entre
*visitar* o conteúdo e *subir* nele.

É exatamente esse o ganho da ideia do Marcos: sair do sobrevoo de uma aula e
montar a **escada ao longo de semanas**, com cada degrau tendo o seu caderno,
tempo de sobra e repetição em BLOCO (a regra que veio das crianças: *"isso eu já
fiz"*).

## 4. A sequência — sete cadernos

A ordem segue a consciência fonológica como a pesquisa e o currículo pedem:
**unidade grande antes da pequena** (rima → sílaba → dentro da sílaba) e, dentro
da sílaba, **inicial → final → medial** (a medial é a mais difícil e vem por
último). Cada caderno = **uma aula**, no molde da folha viva.

### ⏱️ A AULA TEM 55 MINUTOS — e passar disso não é defeito

O Marcos primeiro disse *"cada aula deve durar 50 minutos"* e logo corrigiu:
*"não tem problema se a aula durar mais, na verdade tem 55 minutos"*. É o mesmo
55 do convite do `RETOMAR`: **a criança que não termina volta de onde parou**,
dentro da aula.

Então o `_qa/duracao.py` ganhou o outro lado da régua, mas ele **avisa, não
reprova**: quem passa muito talvez não chegue no fecho (o boletim dela, o
parecer, o relatório do professor) — e quem decide se isso importa naquela
atividade é o professor, não o portão. O **piso** continua reprovando: catorze
minutos com a turma ociosa é defeito, e foi o que deu origem a este portão.

**O alvo de projeto de cada caderno: 40 a 50 min de tela.** No molde da folha
viva isso dá **10 a 11 folhas com 4 a 8 itens sorteados cada** — que é
exatamente o tamanho das duas últimas atividades.

⚠️ **E ao conferir isso descobri que o portão media errado** — vale saber, porque
muda o número de todas as atividades: ele somava o `falas.json` **inteiro** como
se a criança ouvisse tudo. Na Fábrica de Palavras são 515 falas, e 333 delas são
o "certo" e a "dica" de **cada item possível do pote**; a criança resolve 73. O
portão dizia 24 min de voz onde há 5 a 15. Corrigido, as duas últimas atividades
saíram de "54 min" para **35 a 45 min**. Ou seja: **não era
para cortar nada delas.**

| # | Caderno | Objetivo | O degrau |
|---|---|---|---|
| 1 | **A fila do alfabeto** | A | nomear e ordenar letra — o degrau anterior a tudo |
| 2 | **Palavras que rimam** | **F** ⭐ | rima: a unidade GRANDE, a mais fácil de ouvir |
| 3 | **A palavra tem pedaços** | C | segmentar e contar sílabas |
| 4 | **Como a palavra começa** | B | sílaba **inicial** |
| 5 | **Como a palavra termina** | B | sílaba **final** |
| 6 | **O meio da palavra** | B | sílaba **medial** — a mais difícil, por último |
| 7 | **Juntar e formar** | D + E | juntar sílabas em palavra; palavra em frase, com os espaços |

⭐ **O caderno 2 é o buraco que o pedagogo já tinha achado** no parecer da
Fábrica de Palavras: rima é objetivo do currículo e não estava em folha nenhuma.
Ele vira o **piloto** da sequência — resolve uma falta real e prova o formato num
pedaço pequeno.

**E a Fábrica de Palavras não se joga fora:** ela vira o **caderno de revisão**
no fim da sequência, que é o uso para o qual ela é boa. Nada do antigo se apaga.

## 5. Esboço do caderno-piloto — "Palavras que rimam" (caderno 2)

Oito a dez folhas, gesto diferente em cada bloco, tudo narrado:

| Folha | O que a criança faz | Gesto |
|---|---|---|
| 1 | ouve duas palavras e diz se terminam igual | escolher (sim/não) — o degrau mais baixo |
| 2 | dentre três figuras, acha a que rima com a do alto | escolher, com alto-falante em cada opção |
| 3 | idem, subindo a dificuldade (as duas erradas começam igual) | escolher |
| 4 | **puxa** a figura que rima até o par | arrastar |
| 5 | **circula** com o laço as duas que rimam | circular |
| 6 | **pinta** com a canetinha os pares que rimam | pintar (4 cores) |
| 7 | parlenda com uma palavra faltando — qual completa a rima? | escolher dentro do texto |
| 8 | **liga** cada palavra ao par que rima | ligar |
| 9 | escreve a palavra que rima | teclado na tela **e** teclado de verdade |
| 10 | inventa: escolhe a figura e o mascote diz a rima | ensinar o mascote |

Tudo isso são **gestos que a folha viva já tem prontos e testados** — escolher,
arrastar, circular com laço, pintar com canetinha, ligar com linha, teclado nas
duas portas. Não é construir do zero: é montar.

**O que falta ter na folha viva** (e que a sequência vai pedir mais adiante):
forca, caça-palavras, cruzadinha, memória de sons, escada de palavras,
ouvir-e-achar. Existem no motor, ainda não na folha viva.

## 6. O que fecha cada caderno

O de sempre, que já é regra da casa: capa com movimento (sem o nome em cima),
todas as telas narradas, alto-falante em toda resposta, retomar de onde parou por
55 min, boletim animado da criança, relatório do professor por trás da medalha
(com % e o que ela dominou), "treinar o que faltou", senha `1275@`. Mais os
portões e o parecer do pedagogo.

**E o que a sequência acrescenta:** cada caderno **abre retomando o anterior** e
**fecha com o gancho** do seguinte. É isso que transforma sete atividades soltas
numa escada.

## 7. Estado

- **Mapa:** escrito, aguardando o Marcos corrigir a escada.
- **Livro:** falta o sumário do livro que a escola adota (foto basta) para
  ajustar a **ordem e o ritmo** ao que ele já usa em sala.
- **Fontes abertas trazidas:** CEALE/UFMG (Portal de Livros Abertos) e os
  Cadernos do PNAIC, em `_pesquisa/web/livros-alfabetizacao-abertos.md`. O livro
  de atividades do MEC deu 403 nas duas tentativas.
- **Piloto proposto:** caderno 2, "Palavras que rimam".

_Escrito em 9/set/2026, contra `_curriculo/blumenau.txt` (1º ano, Língua
Portuguesa) e o parecer pedagógico de `_alfa1`._

---

## 8. ⚗️ RESULTADO DO TESTE

> ⚠️ **A 1ª rodada abaixo tirou a conclusão errada, por busca errada.** Eu
> procurei *"atividades de rima para imprimir"* e vieram folhas em PDF/imagem —
> daí concluí que "a internet não dá os itens". O Marcos corrigiu: *"são
> SEQUÊNCIAS DIDÁTICAS, lembra? você vai fazer a interatividade que as
> atividades pedem"*. Sequência didática é outro documento: escrita para o
> professor LER e aplicar, **vem em texto corrido com as atividades descritas**.
> Buscando com o termo certo veio uma sequência de **10 aulas inteira**, e o mapa
> dela está em **`_sequencias/SD-ALFABETIZACAO-10-AULAS.md`**: 8 das 10 aulas
> cabem em gestos que a casa já tem prontos.
>
> Fica registrado o erro, porque a lição é de PROCURA, não de método: o nome do
> documento muda tudo. "Atividade para imprimir" = PDF fechado. "Sequência
> didática" / "plano de aula" = texto aberto.

### 8.1 A 1ª rodada (busca errada — mantida como registro)

Rodei o passo 1 do método — buscar a matéria-prima — para o caderno-piloto da
rima. Seis sites de professor, 536 linhas de texto, ~4 minutos de relógio.
Está em `_pesquisa/web/folhas-rima-1ano.md`.

**O resultado contraria a premissa, e é melhor saber agora.**

### O que NÃO veio: os itens

**As folhas em si não chegam.** Elas moram em **PDF e em imagem**, atrás de um
botão de download — e o `pesquisar.yml` lê HTML, não abre PDF nem enxerga
figura. Em 536 linhas vieram **cinco ou seis pares de palavras** (GATO/PATO,
BOLA/ESCOLA, BRINCAR/PULAR). Isso não monta folha nenhuma.

E mesmo que chegassem: os sites são explícitos sobre direito autoral
(*"todo o conteúdo é original… não pode ser copiado. Pirataria é crime!"*).
Copiar os itens não é caminho, e não seria mesmo com o PDF na mão.

**Ou seja: a premissa "as folhas trazem os exercícios já graduados" não se
sustenta.** Os itens vão ser nossos, sempre.

### O que VEIO — e vale mais do que eu esperava

O que a internet entrega em texto aberto, de graça e em abundância, é o que eu
tinha subestimado: **o repertório de dinâmicas e a progressão**, escritos por
quem dá essa aula.

- **Dinâmicas**, descritas com detalhe de aplicação: memória de rimas, roda de
  rimas (a criança tem 5 s para responder), versos incompletos, varal de rimas
  da semana, polegar-para-cima/para-baixo, circular no poema com a mesma cor,
  criar quadrinha coletiva. Uma das fontes trouxe uma **lista numerada de 22
  tipos** de folha de consciência fonológica.
- **A progressão declarada**: "do concreto ao abstrato", e como diferenciar por
  nível dentro da mesma turma.
- **⭐ E uma armadilha que eu não teria pensado sozinho:** incluir pares
  *pegadinha* — palavras que **começam** igual mas **não rimam** (BOLA / BOLSA).
  No meu esboço eu tinha proposto a folha 3 "as duas erradas começam igual" por
  intuição; a professora confirma como técnica, com o porquê. Isso é exatamente
  o tipo de coisa que faz a atividade medir o que ela diz medir.

### A conclusão da rodada

**O método funciona — mas não pelo motivo que imaginávamos.** Ele não é
*"reaproveitar exercícios prontos"*; é **"aprender a sequência e o repertório de
quem já dá essa aula, e escrever os itens nossos"**.

E isso, olhando com honestidade, **não é uma decepção: é o negócio certo.**
Escrever 40 pares de palavras que rimam com vocabulário de 1º ano é trabalho de
minutos e nunca foi o gargalo. O gargalo era saber **quais dinâmicas existem,
em que ordem, e quais armadilhas evitar** — e é justamente isso que a internet
deu, em quatro minutos.

**Os três números, até aqui:**

| # | Medida | Resultado |
|---|---|---|
| 1 | Aproveitamento de **itens** | ~0 (as folhas estão em PDF/imagem, e são protegidas) |
| 1b | Aproveitamento de **dinâmicas e progressão** | **alto** — 10+ dinâmicas e a escada, utilizáveis |
| 2 | Relógio | 4 min para a matéria-prima chegar |
| 3 | Portões | ainda não (depende do caderno montado) |

**O que muda no fluxo dos 4 passos:** o passo 1 continua sendo "buscar na
internet", e o passo 2 continua sendo o pedagogo conferindo contra o currículo —
mas o que ele confere **não é uma pilha de exercícios: é uma pilha de dinâmicas
e uma proposta de ordem**. Ele decide quais dinâmicas entram, em que sequência,
e com que armadilhas. Os itens ele especifica; eu escrevo.
