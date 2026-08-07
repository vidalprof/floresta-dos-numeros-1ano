# O que o Marcos pegou na Padaria das Letras — e o que fazer

> Ele abriu a atividade publicada e, em minutos, achou **oito** defeitos. A banca
> tinha dado **código 0**. Está tudo escrito aqui para não se perder e para a
> próxima atividade não repetir.
>
> Palavras dele: *"não ficou boa a atividade"*, *"muitos erros"*, *"estou bem
> chateado e desanimado"*, *"a atividade tem que ser linda como foi a do Broto"*.

## O que ele achou

| # | o que ele viu | onde mora | situação |
|---|---|---|---|
| 1 | **duas vozes falando ao mesmo tempo** | integrador (15 das 76 peças falavam pelo navegador por cima do mp3) | ✅ **consertado e medido** (0 falas do navegador, 12 mp3) |
| 2 | **o áudio não diz o que está escrito**; alguns nem tocam | motor (narrava o enunciado da FASE enquanto a PEÇA escrevia outro balão) | ✅ **consertado** — o motor lê o balão da tela e fala aquilo; sem gravação, cala |
| 3 | **passa de fase sem o botão CONTINUAR** (o Broto tem) | ponte (pulava sozinha em 420ms) | ✅ **consertado** — banner com confete e botão |
| 4 | "Ouça e ache": **o nome fica fora do quadrado branco**, feio | peça `ouvir-achar` | 🔧 cartão refeito com moldura — falta ajustar em tela baixa |
| 5 | "Ouça e ache": **a letra aparece duas vezes**, metade dentro metade fora | peça `ouvir-achar` | ⏳ quando a opção é letra, mostrar UMA só |
| 6 | **a ordem do alfabeto devia ser com imagens geradas** (letra de fonte desalinha) | conteúdo + peças | 🔧 26 letras em massa de pão sendo geradas em 3 cartelas |
| 7 | "A letra que caiu da prateleira": **o retângulo é muito quadrado, visual feio** | peça `completar` (`.frase`) | ⏳ tirar a caixa pesada; letras viram peças soltas |
| 8 | "Junte os pedaços": **as sílabas deviam ser botões coloridos** | peça `juntar-silabas` | ⏳ |
| 9 | "Escreva a letra": **tem que ser ligar-pontos, profissional como o Circo do Teo** | peça `tracar-letra` | ⏳ trazer o `_circo/index.html` com `recuperar.yml` e copiar de lá |
| 10 | "Bata os pedaços": **pode não ser intuitivo para o 1º ano** | peça `bater-silabas` | ❓ decisão dele: tirar ou simplificar |
| 11 | **"A Fubá"** (feminino) | conteúdo | ✅ consertado |

## Por que a banca deixou passar — a resposta honesta

Os 28 portões nasceram de defeitos que **quebram**: código que estoura, tela
muda, fase sem saída, imagem que não carrega. Por isso eles só sabem pegar coisa
quebrada. **Nenhum olha a tela e pergunta se está bonito e claro para uma criança
de seis anos.**

- a voz errada: os portões comparavam o `falas.json` com o enunciado **no
  código** — e a peça escreve o balão **em tempo de execução**;
- o botão que sumiu: o auditor-jogador mede *"chegou na medalha"*, não *"o
  caminho tem fecho"*;
- o nome fora do cartão: o `leiaute.js` mede se algo saiu **da tela**, não se
  saiu **do próprio cartão**;
- letra de fonte: o `padrao.py` avisa sobre fase **sem** ilustração — uma letra
  de CSS conta como "tem algo";
- "A Fubá": nenhum portão lê português.

**Mas o furo maior não é técnico: eu rodei os portões e não OLHEI.** Tirei duas
telas, achei bonitas e publiquei. A banca virou substituto do olhar, quando ela
devia ser o que sobra depois dele.

## O que muda no processo (não é promessa, é passo obrigatório)

1. **Antes de publicar, abrir TODAS as fases em 4 tamanhos e olhar uma por uma.**
   O que o Marcos faz em dez minutos eu faço com o navegador em três.
2. **Três portões novos**, do que dá para medir:
   - texto que vaza do **próprio cartão** (não só da tela);
   - fase que termina **sem banner**;
   - a voz comparada com o texto **renderizado**, não com o do código.
3. **Conserto vai na PEÇA ou no MOTOR**, nunca só nesta atividade — senão a
   próxima nasce com o mesmo defeito. Foi assim com as duas vozes (76 peças de
   uma vez) e com o botão CONTINUAR (todas as atividades montadas).

## A lição que fica

> Um conserto que não é medido no caminho inteiro vira o defeito seguinte.
> A segunda voz fui **eu** que criei, hoje, consertando o áudio que dizia outra
> coisa. Não bastou consertar: faltou medir o que o conserto encostou.
