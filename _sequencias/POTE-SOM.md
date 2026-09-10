# O pote do degrau 4 — "o som que abre" (fonema inicial e a letra)

> Folhas de origem: `_sequencias/folhas_d4/` (24 folhas). Objetivos do currículo
> de Blumenau, 1º ano:
>
> > **"Identificar fonemas e sua representação por letras."**
> >
> > **"Reconhecer o sistema de escrita alfabética como representação dos sons
> > da fala."**

## 1. Aqui a LETRA inicial é legítima — e no degrau 3 não era

No caderno anterior (A Família das Palavras) **seis folhas foram recusadas** por
pedirem a LETRA quando o degrau era a SÍLABA. Nesta colheita a maioria das 24
folhas também pede a letra — e agora está no lugar certo, porque **este degrau é
o do som isolado e da letra que o escreve**.

É a mesma pergunta em dois degraus diferentes, e é a ORDEM que decide se ela
ensina ou atrapalha.

## 2. ⚠️ A regra que governa o caderno: CONTÍNUO antes de PARADO

Esta é a armadilha central deste degrau, e ela é da mesma família do defeito da
sílaba soletrada que custou três rodadas em set/2026.

- **Sons contínuos** — /f/, /s/, /m/, /v/, /z/, /x/, /l/, /r/, /n/ — podem ser
  **esticados** e ouvidos sozinhos: *mmmmacaco*, *sssapo*, *fffaca*.
- **Sons parados** — /p/, /b/, /t/, /d/, /k/, /g/ — **não existem sem uma vogal
  grudada**. "bê" não é o som /b/: é o **nome da letra**.

Começar pelos parados é ensinar a criança a dizer o nome da letra no lugar do
som — e depois ela lê BOLA como "bê-ó-éle-á". **As folhas 1 a 5 usam só
contínuos; os parados entram na folha 6**, depois de a correspondência som-letra
já estar montada.

## 3. ⚠️ E o som NUNCA é falado sozinho

Não existe mp3 de /m/. Nenhum sintetizador diz um fonema, e mandar ele tentar
traz de volta a soletração. Aqui a criança **sempre compara palavra com palavra**
("MACACO começa igual a MALA") — que é, aliás, o que a pesquisa manda fazer de
qualquer jeito: o fonema se percebe na comparação, não no ar.

A única coisa que a voz diz sobre um som isolado é o **nome da letra** ("ême"), e
nome de letra é uma palavra de verdade. Por isso o `silabas.json` deste caderno
sai vazio, e o portão `_qa/silabas.py` confere isso sozinho.

## 4. ⚠️ Só entra palavra em que a letra e o som se correspondem direto

**CEBOLA** começa com o som /s/ e com a letra **C**. **GIRAFA** começa com /ʒ/ e
com a letra **G**. São exatamente os casos que separam som de letra — e são
conteúdo de 2º/3º ano. Num caderno de 1º ano que ensina *"o som virou letra"*,
elas ensinariam o contrário.

**Ficaram fora: cebola, cenoura, celular, girafa.**

## 5. O crivo — o que sobrou das 24

| Folha | O que pede | Veredito |
|---|---|---|
| **D01, D03** | aliteração: figura que começa com o **mesmo som** | ✅ **o coração do degrau** |
| D14, D17 | qual é o **som inicial** (escrever a letra) | ✅ entra |
| D04, D09, D10, D13, D15, D18–D24 | escrever/pintar a **letra inicial** | ✅ entram (agora é o degrau certo) |
| D12 | circular as figuras que começam com a letra em destaque | ✅ vira "marcar todas" |
| D05, D07, D08, D11, D19, D20 | pintar a letra inicial entre 3–4 | ✅ entram |
| D16 | som inicial **e final** na mesma folha | ⚠️ só a parte inicial |
| D06 | letra inicial, letra final e **número de letras** | ⛔ três coisas numa folha só |
| D02 | completar a palavra com a letra que falta | ⛔ é o degrau 6 |
| D22 | letra inicial só com **vogais** | ⚠️ absorvido: as vogais entram na folha 6 |
| D23 | letra inicial + **reescrever em cursiva** | ⛔ cursiva não é 1º ano nesta casa |

## 6. O buraco que as 24 deixavam: JULGAR duas palavras

Todas mandam **escolher** entre três ou mais. Nenhuma pergunta o mais simples:
*estas duas começam com o mesmo som — sim ou não?* Escolher entre três já
pressupõe o critério pronto; **julgar duas é onde o critério nasce**. É o mesmo
degrau que a folha 1 do Bando das Rimas ocupa, e pelo mesmo motivo. Virou a
folha 2.

## 7. O pote

64 palavras, agrupadas por som inicial:

| | Sons | Palavras |
|---|---|---|
| **Contínuos** (folhas 1–5) | F S M V Z X L R N | faca · foca · foguete · sapo · sapato · sino · sol · sorvete · macaco · mala · mapa · maçã · mel · menina · morcego · vaca · vela · zebra · xícara · lata · lupa · laranja · luneta · rato · navio |
| **Parados** (folha 6 em diante) | P B T D C G | pato · panela · pipa · pipoca · peixe · pirulito · pão · papagaio · bola · bolo · boneca · bota · boca · banana · batata · tomate · tesoura · tucano · tijolo · trem · tartaruga · dado · casa · cavalo · cachorro · caracol · coruja · cone · gato · galinha |
| **Vogais** | A E I O U | abelha · aranha · elefante · escola · estrela · igreja · ovo · uva · urso |

⚠️ **ZEBRA saiu da folha 3** (achar quem começa igual): era a única palavra com Z
no pote, e sem uma palavra irmã não há resposta certa possível. Continua nas
outras folhas, onde é distrator.

_Escrito em 10/set/2026, contra `_curriculo/blumenau.txt` (1º ano, Língua
Portuguesa) e as 24 folhas de `_sequencias/folhas_d4/`._
