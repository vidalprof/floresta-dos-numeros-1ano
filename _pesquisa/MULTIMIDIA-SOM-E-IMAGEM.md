# 🔊🖼️ Som e imagem que ENSINAM — as regras, destiladas

> Pedido do Marcos (ago/2026): *"pode pesquisar melhorias nas interatividades,
> para ficarem mais sonoras e visuais"*, logo depois de *"as dinâmicas
> interativas têm que ser mais visuais e sonoras para os pequenos"*.
>
> **Fonte:** os 12 princípios de **Richard Mayer** (Multimedia Learning, UC Santa
> Barbara), trazidos pelo `pesquisar.yml` para `_pesquisa/web/interatividade-sonora-visual.md`.
> São a base científica de "por que som + figura ensina mais que figura sozinha".
>
> **Isto é matéria-prima virada em REGRA DE MONTAGEM.** Pesquisa que não vira
> regra na hora de montar não muda atividade nenhuma.

---

## As três premissas (é daqui que sai todo o resto)

1. **Dois canais separados.** O ouvido e o olho processam por caminhos
   diferentes. Falar E mostrar usa dois canais; mostrar texto E figura usa **o
   mesmo canal duas vezes** e entope.
2. **Cada canal é estreito.** A criança segura pouca coisa de cada vez.
3. **Aprender é ativo.** Quem só recebe não aprende — tem que fazer.

---

## O que vira REGRA aqui, e o que mede

| Princípio de Mayer | A regra da casa | Quem mede |
|---|---|---|
| **Multimídia** — palavra + figura ensina mais que palavra só | toda opção que a criança toca aceita `img`; toda tela que precisa tem arte de IA | `_qa/padrao.py` (avisa fase sem ilustração) |
| **Modalidade** — narração + figura bate texto + figura | **toda tela narrada**, e a narração acompanha a figura | `_qa/fala_o_escrito.js` |
| **Contiguidade espacial** — o texto perto da figura dele | a **dica entra logo depois do enunciado**, não no fim da tela; o alto-falante fica **ao lado** da resposta dele | `_qa/leiaute.js` (resposta/dica fora da tela reprova) |
| **Contiguidade temporal** — a voz JUNTO da animação, não antes nem depois | a sílaba acende **enquanto** a voz a diz; o compasso é o tempo da gravação, não um número inventado | ainda no olho — ver "o que falta medir" |
| **Sinalização** — apontar o que importa | o **"ver destino"** (o lugar certo aparece no 2º erro), o brilho no ponto da vez, a seta que anda | `_qa/errador.js` (a ajuda tem que CRESCER) |
| **Coerência** — tirar o que não serve | nada de enfeite que não ensina; uma ideia por tela | Portão 0 (filosofia) |
| **Segmentação + controle do ritmo** — pedaços, e a criança manda no passo | **"Ouvir de novo" é isto**, e é por isso que fica: não é enfeite, é o controle do ritmo na mão dela | — |
| **Pré-treino** — saber os nomes antes de usar | a "parada" antes da fase que cobra; o modo `mostrar` do rótulo | — |
| **Voz** — voz humana ensina mais que voz de máquina | **voz gravada (Edge TTS) sempre; voz-robô do navegador nunca** | `_qa/vozrobo.py` |
| **Personalização** — falar como gente, na segunda pessoa | "Toque no pedaço que falta", nunca "o usuário deve selecionar" | `_qa/falas.py` |

---

## ⭐ A RESSALVA QUE VALE MAIS QUE TUDO (e que quase me fez errar)

Mayer tem um princípio — a **REDUNDÂNCIA** — que diz o contrário do que a gente
faz: *"não narre o mesmo texto que está escrito na tela; use gráfico OU texto
com a fala, nunca os dois"*.

**Não vale para o 1º ano, e a razão é simples: para quem não lê, o texto na tela
não é informação — é desenho.** Não há redundância nenhuma em narrar o que está
escrito quando a criança não consegue ler o escrito. A pesquisa de Mayer foi
feita com universitários leitores fluentes; o princípio pressupõe que ler e
ouvir a mesma coisa disputa o mesmo canal. Numa criança em alfabetização, ler
ainda **não é** um canal disponível.

**Onde a redundância volta a valer:** do 6º ao 9º ano, com leitor fluente,
narrar parágrafo inteiro escrito na tela **atrapalha**. Ali a voz explica o que
a figura mostra; não repete o que o olho já leu.

Escrevo isto porque é exatamente o tipo de princípio que, aplicado sem pensar na
criança da frente, teria me feito **tirar** a narração que o Marcos passou meses
cobrando: *"não teve fala automática, visto que os pequenos precisam"*.

---

## O que isto muda na prática, amanhã

1. **Alto-falante ao lado da resposta, nunca dentro dela** (contiguidade
   espacial + o dedo que quer ouvir não pode arrastar a peça).
2. **A voz e o movimento juntos.** Sílaba que acende depois da voz é pior que
   sílaba que não acende: quebra a ligação entre o som e o pedaço.
3. **"Ouvir de novo" fica.** É o controle do ritmo, princípio da segmentação —
   e é o único jeito de a criança lenta não ficar para trás sem pedir ajuda.
4. **Figura que não ensina, sai.** Enfeite bonito custa canal.
5. **Do 6º ano em diante, menos narração e mais explicação:** a voz diz o que a
   figura NÃO diz.

---

## O que ainda NÃO medimos (dito com todas as letras)

- **Contiguidade temporal.** Hoje o compasso da narração picada é cronômetro
  (820 ms por pedaço), não o fim real do áudio. Encaixa em palavra de 2 e 3
  sílabas; numa de 4 pode desencontrar. O portão que faltaria mediria o
  `ended` do áudio contra o acender da sílaba.
- **Coerência.** Nenhum portão sabe dizer se uma figura ensina ou só enfeita.
  Isso continua sendo olho de professor — e é o Portão 3, o do Marcos.
