# ✨ O ACABAMENTO NÃO É SEGUNDA PASSADA

> Cobrança do Marcos (ago/2026), no tangram: *"tem que ser mais intuitivo e
> profissional"* — e, quando eu disse o que ia fazer: **"por que você já não faz
> assim, precisa que eu fale?"**
>
> A resposta honesta: eu construía em duas passadas — primeiro *funciona*, depois
> *fica bom* — **e entregava entre as duas**. Por isso ele sempre pegava o
> acabamento. Esta folha existe para o acabamento entrar na PRIMEIRA passada.

## As sete regras do gesto (valem para TODA mecânica nova)

1. **As duas portas, sempre.** Se dá para arrastar, tem que dar para tocar no
   objeto e tocar no destino. (No tangram a vaga nasceu **sem clique**: só dava
   para jogar arrastando. Defeito pego pelo auditor, não por mim.)
2. **A ferramenta mora JUNTO do objeto.** Botão de girar no rodapé faz a criança
   procurar; junto da peça, ela acha sem instrução. Regra prática: a ferramenta
   fica a menos de um dedo (≈50px) do que ela opera.
3. **O escolhido grita.** Brilho sozinho não basta: contorno grosso + leve
   aumento + a ferramenta aparecendo ao lado. Se um adulto precisa olhar duas
   vezes para saber o que está selecionado, a criança não sabe.
4. **O destino acende quando a ação é possível** — no arrasto E no toque. A vaga
   que serve pisca no instante em que a peça é escolhida.
5. **Toda mudança ANDA.** A peça gira em 0,2s; ela não pula de ângulo. Pulo o
   olho não acompanha; movimento o olho segue e aprende.
6. **A primeira vez é demonstrada.** Na primeira figura, um dedo (ou seta) faz o
   gesto uma vez, sozinho. Instrução escrita explica; demonstração ensina.
7. **Nada de texto para o que o gesto mostraria.** Se a tela precisa de uma
   frase explicando como jogar, o gesto está errado.

## ⚠️ A armadilha técnica que custou hoje

**Animação em CSS ganha do estilo inline.** A peça selecionada pulsava com uma
animação que mexia no `transform` — e o giro (também `transform`) era apagado 60
vezes por segundo: o dado mudava e a tela não. **Quem gira usa o `transform`;
então o destaque usa outra propriedade** (filtro, borda, sombra). Vale para
qualquer par "animação de destaque" + "transformação de estado".

## Como conferir antes de entregar

- `python3 _qa/publicar.py <pasta>` — qual workflow publica isto.
- Abrir a fase e fazer o gesto **de três jeitos**: mouse, dedo, toque simples.
- Pedir a alguém que não viu o código: *"o que você faria nesta tela?"* Se a
  pessoa hesitar, a regra 3 ou a 6 está faltando.

---

## 🧬 Duas lições novas do mesmo dia (ago/2026, ainda no tangram)

### 1. Nome de classe repetido HERDA estilo alheio, e ninguém avisa

As vagas do tabuleiro se chamavam `.slot`. O CSS clonado da Oficina da Lina já
tinha um `.slot` — a casinha onde a criança encaixa a letra, com
`background:rgba(255,253,246,.93)`. Resultado: **cada vaga do tangram ganhou um
quadrado branco chapado atrás do contorno tracejado**, e a figura ficava
manchada. O `node --check` passa. Nada quebra. Só fica feio — que é a categoria
de defeito que sempre chega até o Marcos.

**Regra:** mecânica nova leva classe com o **prefixo da atividade** (`.tvg`,
`.tpeca`), nunca um nome genérico que o CSS de origem já pode ter ocupado. Quem
achou foi o `_qa/visual.js` (portão 5b), medindo o pixel.

### 2. Resto de clone também é ENREDO — e esse não quebra nada

A tela de abertura dizia, **escrito**: *"Oi! Eu sou a Marta, pintora de
letreiros. O meu ajudante trocou uma letra em quase todas as placas da rua..."*
— a história da Lina inteira, dentro de um jogo de tangram. E a **voz gravada**,
do `falas.json` desta pasta, contava a história certa. Quem lê recebia uma
história; quem não lê, outra.

Os doze itens do `_qa/clone.py` olhavam **arquivo** (imagem, mp3, prefixo, nome,
enfeite). Nenhum olhava o **enredo**. Agora o **item 14** compara: quando uma
`telaX` escreve um balão e chama `falar("id")`, o texto do balão tem que ser o
texto de `id` no `falas.json`. Menos de 45% de palavras em comum = outra
história, e reprova.

**Regra:** clonar o MOTOR é obrigatório; clonar a HISTÓRIA é o defeito mais
caro, porque não dá erro nenhum.

### 3. Portão não pode obrigar a desfazer uma ordem do professor

O tangram é **um jogo de mecânica única** — ordem explícita dele: *"não é pra
ser atividade, é pra ser o jogo do tangran só que didático"*. Dois portões
reprovavam justamente por isso (leque de 4 gestos; piso de 40 min). O caminho
certo **não** é enfiar fases estranhas no jogo nem afrouxar a regra para todo
mundo: é uma **exceção declarada e escrita no próprio arquivo** —
`var TIPO_ATIVIDADE="jogo"` — que o `_qa/padrao.py` e o `_qa/duracao.py` leem,
**anunciam em voz alta** e só então liberam. Ninguém escapa por acidente, e a
regra continua valendo para toda atividade.
