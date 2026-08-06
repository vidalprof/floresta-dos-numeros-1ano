# 🧰 O LEQUE TREINADO — onde mora a versão que JÁ funciona de cada dinâmica

> Cobrança do Marcos (ago/2026): *"veja, nós temos um leque de interatividades
> muito grande, precisam ser TREINADAS, para quando for posta em prática não dar
> todos esses erros"* — e, logo depois: *"temos muitas outras: de arrastar,
> sombra, ligar pontos, achar sete erros, completar, forca, e muitas outras que já
> fizemos em outras atividades"*.
>
> **O diagnóstico honesto:** o defeito não é falta de ideia, é **reescrita**. Toda
> vez que eu montava um caça-palavras ou uma fase de arrastar, eu escrevia aquilo
> **do zero** — e repetia um defeito que já tinha sido pago noutra atividade.
>
> **A cura é este arquivo + o portão `_qa/dinamicas.py`.** Aqui está, para cada
> mecânica, **em qual atividade mora a versão mais corrigida** (a que já passou
> pelo Marcos e pela banca). Montar a próxima é **copiar de lá**, não reinventar.
> O portão confere as armadilhas antes de ele ver.
>
> **Levantamento feito medindo o acervo:** 199 fases catalogadas em 9 atividades
> premium (Doceria 25 · Mapa 27 · Fábrica 23 · Naveg 22 · Nomes 22 · Órbi 21 ·
> História 20 · Jardim 17).

---

## COMO USAR (o passo que evita 90% do retrabalho)

1. Escolhi a mecânica no roteiro → **abro a coluna "onde está a boa"** e copio
   daquela atividade: o CSS, a função da fase e os ajudantes que ela usa.
2. Troco **só o conteúdo** (as palavras, as figuras, os ids de voz com o prefixo
   novo). ⚠️ Ver `_padrao/CLONAR-MOTOR.md`: o que mais escapa é conteúdo da
   origem que **não dá erro nenhum**.
3. Rodo `python3 _qa/dinamicas.py <arquivo>` — ele confere as armadilhas **daquela**
   mecânica.
4. Rodo a banca inteira (`bash _qa/auditar.sh`).

---

## A TABELA

| Mecânica | Onde está a boa (copiar daqui) | O que ela ensina bem | Armadilhas — cada uma já custou caro |
|---|---|---|---|
| **Caça-palavras** | `_naveg` "CAÇA-PALAVRAS DO MAR" · `_mapa` | reconhecer a forma escrita de um termo novo; alívio entre fases pesadas | célula em **`(100/N)%` + `box-sizing:border-box`** (com px fixo cabem 10 numa grade de 9 → *"TROCA e o A em outra linha"*); **diagonal só se o enunciado avisar**; célula conquistada **trava**; conferir `mark` **OU** `ok` (palavra que cruza outra nunca fechava); publicar `data-qa` senão o auditor dá "PRESO" |
| **Cruzadinha** | `_mapa` · `_naveg` | definição → palavra: recuperar o termo pelo sentido | teclado na tela **e** `document.onkeydown`; a voz de cada dica tem que existir (`_qa/vozfalta`) — foi aqui que 3 fases ficaram MUDAS; alvo ≥ 40px |
| **Forca** | `_mapa` · `_naveg` | onde a PALAVRA é o conteúdo | palavra a adivinhar **sem acento** (o teclado não tem), a da faixa **com** (`ac:"BÚSSOLA"`); letra usada **sai do alcance**; comemorar ao fechar |
| **Memória** | `_mapa` (carta grande, verso de arte, virada 3D) | par **conceitual** (causa↔efeito, palavra↔imagem) | carta fluida **≥ 130×88px**; verso de **arte de IA**, nunca retângulo liso; `rotateY` com queda para troca-de-face no Chrome 109; em tela baixa encolhe a LETRA, nunca a carta; som de virar e de par |
| **Arrastar** | `_mapa` "MONTE A LEGENDA" (`arrasta(b,k)`) | pôr no lugar É o conceito espacial | **três caminhos: mouse, dedo, toque simples**; **nunca** `preventDefault` no `touchstart`; guarda contra o **mouse fantasma** que o celular dispara depois do toque. Pego **DUAS vezes** |
| **Sombra / ache o par** | `_mapa` "ACHE O PAR" | forma e silhueta: olhar o contorno, não a cor | a silhueta tem que ser **da MESMA figura** (recorte da própria arte), senão a criança compara coisas diferentes; par que acerta **acende e pulsa** |
| **Ligar colunas** | `_naveg` "PARA QUE SERVIA?" · `_jardim` "PARA QUE SERVE" | relação 1-a-1 explícita | alto-falante nos **dois** lados; a linha precisa de `touchmove`; nunca mais que ~6 pares (vira memória disfarçada) |
| **Ordenar / linha do tempo** | `_historia` "LINHA DO TEMPO" · `_jardim` "telaOrdenar" | seriação e etapas **com a justificativa** | três caminhos de arrasto; **conteúdo conferido por especialista** — o portão não pega data histórica errada; faixa que rola precisa de `overflow-x` próprio |
| **Classificar em gavetas** | `_naveg` "VEIO OU JÁ ESTAVA?" | formar categoria por atributo definidor | enunciado sem termo que ela não conhece (*"veio de lá"* → **"veio de fora"**); as gavetas se **refazem** quando o eixo muda; a explicação espera o áudio (`depoisDaFala`, nunca `setTimeout` fixo) |
| **Achar na cena / lupa** | `_mapa` "O BAIRRO LÁ DE CIMA" (`naZona`, grade 48×48) | observação dirigida: ler a paisagem | zona = a **FIGURA recortada por pixel**, nunca um pontinho com raio; alvo no pixel **mais longe da borda** (`distance_transform_edt`), nunca no centroide; achou = **V verde**; singular só se houver UMA |
| **Pintar / marca-texto** | `_mapa` "PINTE O MAPA" (camadas medidas por pixel) · `_naveg` "A LÍNGUA GUARDA" | mapear categoria sobre o real — o traço É a classificação | a figura é **arte de IA**, o CSS anima só o que se mexe; o mapa começa **sem cor**; no texto: traço correndo + som de risco + barra + carimbo |
| **Simulador / deslizar** | `_historia` "A ÁGUA SOBE" (o que ele mais elogiou) · `_naveg` "O SEGREDO DO VENTO" | causa-efeito e controle de variáveis | o mundo reage **de verdade** (foto que gira não é simulador); ponto **medido na figura**, não a olho; a figura é gerada, o CSS anima |
| **Completar lacuna** | `_naveg` "COMPLETE A HISTÓRIA" | produção mínima com apoio da frase | a voz diz **exatamente** o texto escrito; em fase embaralhada o id da voz vem do **ITEM**, nunca do contador da rodada; figura sem fundo branco aparecendo |
| **Montar a palavra** | `_jardim` "telaMontaPalavra" | soletrar: qual letra vem primeiro | as duas portas (tela + teclado real); ⚠️ o `setTimeout` da rodada continua correndo depois do `limpa()` e reinstala o `onkeydown` **por cima da fase seguinte** — guardar `if(!t.parentNode) return;` |
| **Escolher / quiz** | qualquer uma — mas **≤ 2 telas em 20** | aferir rápido um fato já ensinado | **embaralhar as opções** (na Fábrica de Estrelas a certa era sempre a 1ª); alto-falante em CADA opção; distratores plausíveis; a dica fala da tela que está ali |
| **Relâmpago** | `_mapa` · `_naveg` | evocação rápida do que já foi visto | **não exigir andaime aqui** — dica no meio acaba com o que a fase treina (é velocidade). Está na lista `SEM_ERRO` do `_qa/pedagogo.py` |
| **Ensinar o mascote** | `_naveg` "ENSINE O ARÁ" | metacognição: a regra que ela ensina É o modelo mental | o mascote **erra visível** com a regra ensinada, senão vira quiz fantasiado; enunciado que muda por rodada exige voz por rodada |
| **Rota animada no mapa** | `_naveg` "A ROTA DA VIAGEM" (`ROTAP`, o navio andando) | trajeto e ordem no espaço | os pontos são **medidos na imagem**, não estimados (navio ancorando no continente errado estraga a fase) |
| **Quebra-cabeça** | `_mapa` "O MAPA EM PEDAÇOS" | parte-todo e orientação | peça na **proporção certa** da imagem (0,91 e não 1,0); mira na vaga; som de pegar, de encaixar e de fechar |
| **Coordenadas / bússola** | `_mapa` "ACHE PELA COORDENADA" e "A ROSA DOS VENTOS" | par ordenado e orientação | as coordenadas têm que **bater com a figura** (medir, não estimar — ele pegou isso); célula ≥ 40px; referência explícita ("o lado da sua direita") |

---

## O QUE AINDA NÃO TEMOS (do catálogo de pesquisa)

Está em `_pesquisa/REGRAS-INTERATIVIDADE.md`, bloco (B), com 32 mecânicas em ordem
de custo. As três que eu recomendaria para a próxima, e **só se encaixarem no
conteúdo**:

1. **Conserte o erro** — a resposta vem **já feita com um erro plantado** e a
   criança acha. É o motor de "achar na cena" com o conteúdo invertido: quase de
   graça.
2. **Mapa conceitual** — arrastar conceitos e **traçar setas com nome**. A
   evidência mais forte de todas as mecânicas novas; serve a qualquer disciplina.
3. **Mistério guiado** — pistas que aproximam e erro que **dá mais pista**. É o
   formato que mais responde ao "quero mais".

⚠️ **Nenhuma delas pode deixar a atividade mais difícil.** Regra do Marcos: *"não
podemos fazer muito difícil, a criança tem que conseguir passar"*.

---

## O PORTÃO QUE CONFERE ISTO SOZINHO

`python3 _qa/dinamicas.py <arquivo.html>` (portão 0b2 da banca) reconhece a
mecânica pelo código e cobra as armadilhas **dela**. Na estreia ele já achou, no
acervo: Doceria e Fábrica com teclado na tela **sem** teclado de verdade; Gêneros
com opções **não embaralhadas**; três atividades com memória **sem virada 3D**;
duas com célula de caça-palavras em px fixo; e quase todas **sem o guarda do toque
fantasma**.

**Regra da casa:** mecânica nova = **linha nova neste arquivo e regra nova no
portão, no mesmo commit.** Sem isso, o defeito volta na próxima atividade — que é
exatamente o que ele está cobrando.

---

## 🧰 AS PEÇAS PRONTAS — copie DAQUI, não da atividade

A partir de ago/2026 a versão de referência de cada mecânica **não é mais a que
está dentro de uma atividade**: é a **peça isolada**, em `_padrao/pecas/`. A
diferença importa — dentro da atividade a mecânica vem misturada com o conteúdo
dela (as imagens, as vozes, os conceitos), e era daí que saíam os restos de clone.
A peça vem limpa e **já aprovada nos 8 portões da bancada**
(`bash _qa/peca.sh <arquivo>`), incluindo o jogador automático que joga sozinho
até a medalha.

**Peças no catálogo hoje:** `achar-na-cena`, `arrastar-lugar`, `autoexplicacao`, `balanca`, `bussola`, `caca-palavras`, `caixa-dinheiro`, `classificar`, `completar`, `conserte-o-erro`, `contadores`, `coordenadas`, `criar-desafio`, `cruzadinha`, `decisao`, `digitar`, `ditado`, `ensinar-mascote`, `escolher`, `escrever-legenda`, `experimento-justo`, `filtro`, `forca`, `girar`, `grafico`, `investigar-fonte`, `ligar`, `linha-do-tempo`, `mapa-conceitual`, `memoria`, `misterio`, `montar-frase`, `morfemas`, `mudanca-permanencia`, `ordenar`, `pintar`, `prever-observar`, `quebra-cabeca`, `relampago`, `repartir`, `reta-numerica`, `saltos-na-fita`, `sete-erros`, `simetria`, `simulador`, `sombra`, `tabela`, `tangram`, `teia-alimentar`, `termometro`, `tracar-caminho`

⚠️ **Cada peça tem no cabeçalho o bloco de dados a trocar.** Copiar = trocar o
conteúdo, nunca reescrever a mecânica.

### O que as peças ensinaram (e portão nenhum pegaria)

- **O erro encenado não pode sumir.** No "ensinar o mascote", a cena era limpa
  logo depois do erro: o boneco voltava para o canto e o que ela ensinou
  desaparecia — a criança lia "continua murcha" olhando uma cena vazia, e a fase
  virava **quiz fantasiado**. A limpeza passou para o COMEÇO da tentativa
  seguinte, para o erro ficar de pé enquanto ela olha.
- **Cada regra errada precisa do SEU resto.** Um monte de areia servindo para
  "cubro com um pano" denuncia que o mundo não está reagindo de verdade.
- **Ficha usada: `display:none`, não `visibility:hidden`.** O retângulo invisível
  continua ocupando lugar (buraco no banco) e ainda é medido pelo portão como
  "resposta fora da tela".
- **Escalar a cena inteira** (`transform:scale`) em vez de reposicionar peça por
  peça em cada `@media` — 12 regras que precisam concordar é 12 chances de errar.
- **A tela de fim tem que mostrar o estado REAL** (inclusive "ninguém
  respondeu"), senão ela vem vazia e nunca é medida.
