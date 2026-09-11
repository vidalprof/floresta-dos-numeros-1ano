# 📚 CATÁLOGO DE ATIVIDADES — fonte única da verdade

> **⭐ LEIA ISTO ANTES DE LISTAR ATIVIDADES.** Este é o registro oficial de TODAS
> as atividades criadas (o "site de atividades" em forma de tabela). Sempre que
> o Marcos pedir "a lista das atividades", responda a partir DESTE arquivo — não
> reconstrua de memória nem só dos `_status/` (que só cobrem o que foi publicado
> por workflow).
>
> **⭐ TODA ATIVIDADE NOVA ENTRA AQUI.** Ao criar/publicar uma atividade, adicione
> UMA LINHA na tabela do ano correspondente: **Ano · Nome · O que trabalha ·
> Link**. Commit + push junto com a atividade. Sem isso, a próxima sessão não
> sabe que ela existe (foi essa a cobrança do Marcos, ago/2026).
>
> Link = `https://vidalprof.github.io/<repositório>/`. Pasta = onde mora o código
> neste repo (`_xxx/`).
>
> ## ⭐ ESTE ARQUIVO É O PAINEL DE LINKS — não é só documentação
>
> Pedido do Marcos (set/2026): *"cada atividade nova vai para esse painel certo?
> certifique-se disso, que cada seção saiba disso"*. A corrente:
>
> ```
> ATIVIDADES.md  →  python3 _painel/montar_painel.py  →  _painel/index.html
>                →  https://vidalprof.github.io/painel-de-atividades/
> ```
>
> É a tela que ele abre na escola (busca, chips por turma, botão COPIAR, e o
> controle da sala ao lado). **Uma linha aqui = um cartão lá.** Nenhuma atividade
> nova pode faltar: se faltar, ele volta a pedir o link no chat — que é o atrito
> que o painel existe para acabar.
>
> **Fechar uma atividade = duas coisas, no mesmo commit:**
> 1. a linha nova na tabela do ano (Nome · O que trabalha · Pasta · Link);
> 2. `python3 _painel/montar_painel.py` (regera o `_painel/index.html`).
>
> **E isso é MEDIDO, não prometido:** `python3 _qa/catalogo.py <pasta> <repo>`
> reprova se a pasta não estiver aqui, se o link não for o do site que está
> subindo, ou se o painel estiver atrasado. Ele roda dentro do `entregar.yml`:
> **atividade fora do painel não é publicada.**

Última atualização: 2026-09-04 (Bancada da Divisão publicada; painel de links criado;
painel virou portão — `_qa/catalogo.py` no `entregar.yml`).

---

## Pré-escola (Educação Infantil)

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **Somando com os Dedinhos** (folha autoral · Pré e 1º) | Matemática: adição até 10 com os dedos das mãos — contar e digitar, ligar mãos ao número, MOSTRAR a quantidade levantando dedos, quantos faltam; mãos em vetor, somas sorteadas a cada abertura, voz em tudo, sem cabeçalho (1ª folha autoral, modelo: 40 folhas da internet) | `_dedos` | https://vidalprof.github.io/somando-com-os-dedinhos/ |
| **O Ateliê do Sr. Batata** | Partes do rosto/corpo, criação livre, coordenação | `_batata` | https://vidalprof.github.io/atelie-do-sr-batata/ |
| **O Ateliê de Cores da Rai** | Cores, formas, expressão | `_colorir` | https://vidalprof.github.io/o-atelie-de-cores/ |
| **Mundo Mágico — Brincar e Aprender** | Pré (rota geral) | — | https://vidalprof.github.io/pr-escola-1/ |

## 1º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **A Máquina de Juntar Palavras** (livro de folhas · 1º ano) | Consciência fonológica — SÍNTESE silábica: juntar pedaços para formar a palavra (Blumenau: *segmentar oralmente palavras em sílabas*; *construir o sistema alfabético reconhecendo que a palavra se forma por sílabas*): 10 folhas — juntar os dois pedaços (a folha que ensina) · qual pedaço falta no **fim** · qual pedaço falta no **começo** · pôr os pedaços na ordem · três pedaços e **um que sobra** · **que palavra é esta? (só pelo ouvido)** · ligar a figura aos pedaços escritos · **as duas começam igual** (BOLA/BOLO — decidir pelo fim) · escrever o pedaço que falta · o mural. ⭐ DEGRAU 5 da sequência, e o CAMINHO DE VOLTA do degrau 2: lá a criança PARTIA a palavra, aqui ela JUNTA — que é o que se faz por dentro para ler sem soletrar. As folhas 2 e 3 vêm em BLOCO (a mesma mecânica com o buraco mudando de lugar). Cada pedaço é RECORTADO da palavra inteira por alinhamento forçado — nunca lido solto pelo sintetizador, que soletra. 38 palavras, 100 recortes de voz, figuras do banco. Relatório descritivo por objetivo + nota de 0 a 10. **NÃO usa o motor** | `_mont1` | https://vidalprof.github.io/a-maquina-de-juntar-palavras/ |
| **O Som que Abre** (livro de folhas · 1º ano) | Consciência FONÊMICA — o som inicial e a letra que o escreve (Blumenau: *identificar fonemas e sua representação por letras*; *reconhecer o sistema de escrita alfabética como representação dos sons da fala*): 10 folhas — esticar o som · **julgar se duas começam igual (sim/não)** · achar quem começa igual · circular todas com o mesmo som · **o som virou LETRA** · a letra dos sons parados · as três gavetas · o intruso · escrever a letra · o mural. ⭐ DEGRAU 4, o coração da alfabetização. Regra não negociável: som CONTÍNUO (f, s, m, v, z, l, r, n — dá para esticar) antes de som PARADO (p, b, t, d, c, g — não existe sem vogal; "bê" é o NOME da letra, não o som). O som nunca é falado sozinho: a criança compara palavra com palavra. Só entram palavras em que letra e som se correspondem direto (cebola, girafa ficaram fora). 64 palavras, figuras do banco. Relatório descritivo + nota. **NÃO usa o motor** | `_som1` | https://vidalprof.github.io/o-som-que-abre/ |
| **A Família das Palavras** (livro de folhas · 1º ano) | Consciência fonológica — SÍLABA INICIAL (Blumenau: *comparar palavras, identificando semelhanças e diferenças entre sons de sílabas iniciais, mediais e finais*): 10 folhas em escada — ouvir o primeiro pedaço · qual é o começo · circular quem começa igual (com o alvo) · ligar a figura ao seu começo · **achar as DUAS que começam igual, sem alvo dado** · completar o começo que falta · quem não é da família · as três gavetas do começo · escrever o começo sem opções · o mural das famílias. ⭐ DEGRAU 3 da sequência. O pedagogo recusou SEIS folhas que pedem a LETRA inicial e não a sílaba (a letra é degrau 0 e o fonema é o 4 — trocar inverte a escada), e uma que oferecia KO/KA/KU como opção, grafia que não existe. Sílaba recortada de dentro da palavra falada (alinhamento forçado). 66 palavras por família de começo, 56 figuras do banco. Relatório descritivo por objetivo + nota de 0 a 10. **NÃO usa o motor** | `_ini1` | https://vidalprof.github.io/a-familia-das-palavras/ |
| **Bate-Palma das Palavras** (livro de folhas · 1º ano) | Consciência fonológica — SÍLABA (Blumenau: *segmentar oralmente palavras em sílabas*): 10 folhas em escada — bater palma em cada pedaço ouvindo a sílaba na voz da própria palavra · quantas palmas · pintar um pedacinho por palma · **qual tem MAIS pedaços** · pôr os pedaços nos quadradinhos · ligar a figura ao número · as três gavetas (1, 2 ou 3 palmas) · **letra não é sílaba** (FLOR tem 4 letras e 1 palma) · escrever o número sem opções · o mural. ⭐ DEGRAU 2 da sequência, depois da rima. O degrau é ORAL: a palavra chega sempre pela figura e pela voz, nunca só escrita — quatro folhas de origem foram recusadas por cobrarem LEITURA disfarçada de sílaba, e outras quatro reposicionadas para o degrau 5 (contar não é montar). 24 folhas de professor colhidas. 73 palavras com a divisão silábica escrita à mão; 58 figuras, todas do banco. Relatório descritivo por objetivo + nota de 0 a 10. **NÃO usa o motor** — 37 a 45 min de aula | `_sil1` | https://vidalprof.github.io/bate-palma-das-palavras/ |
| **O Desfile das Letras** (livro de folhas · 1º ano) | Ordem alfabética e nome das letras (Blumenau: *nomear as letras do alfabeto e ordená-las* — conceito: **ordem alfabética**): 10 folhas em escada — o desfile das 26 letras com a voz de cada nome · ouvir o nome e achar a letra · a letra que fugiu da fila · quem vem DEPOIS · **quem vem ANTES** (o degrau mais difícil: obriga a voltar na fila) · os dois lados · pôr em ordem · quem saiu da fila · com que letra começa · o alfabeto da turma. ⭐ DEGRAU 0 da sequência de alfabetização — vem ANTES da rima e de tudo mais, porque as outras folhas supõem que a criança já sabe o nome das letras. Alto-falante em TODA letra, com o nome escrito por extenso (á, bê, agá, xis…), porque o verbo do currículo é *nomear*. 24 folhas de professor colhidas, 9 recusadas pelo pedagogo (ordenar PALAVRAS é 2º/3º ano; duas fora da letra bastão). 26 figuras, todas do banco. Relatório descritivo por objetivo + nota de 0 a 10. **NÃO usa o motor** — 35 a 46 min de aula | `_abc1` | https://vidalprof.github.io/o-desfile-das-letras/ |
| **O Bando das Rimas** (livro de folhas · 1º ano) | Consciência fonológica — RIMA (Blumenau: *recitar parlendas, quadras, quadrinhas, trava-línguas... observando as RIMAS*; e a porta de entrada para *comparar palavras pelos sons das sílabas*): 10 folhas em escada — julgar se rima · achar entre três figuras · pintar a palavra escrita · **a pegadinha** (começa igual e não rima) · circular as duas · arrastar até o par · ligar quatro pares · completar a parlenda · escrever a palavra que rima · montar o próprio mural. ⭐ PRIMEIRA do método novo: cada folha veio de uma FOLHA REAL de professor e é fiel a ela (itens em `_sequencias/POTE-RIMA.md`); o crivo do currículo achou um ERRO de rima na folha de origem. 56 figuras — 37 recortadas das próprias folhas, 19 do banco. Voz em tudo, teclado na tela e de verdade, chave mestra **1275@**, continua de onde parou por 55 min. **NÃO usa o motor** — 34 a 47 min de aula | `_rima1` | https://vidalprof.github.io/o-bando-das-rimas/ |
| **A Fábrica de Palavras** (livro de folhas · 1º ano) | Alfabetização (Blumenau: *nomear e ordenar as letras*, *comparar palavras pelos sons das sílabas inicial, medial e final*, *segmentar oralmente em sílabas*): 10 folhas em escada — a letra escondida · contar sílabas batendo palma · sequência lógica · circular quem começa igual · pintar a sílaba inicial · ligar à sílaba final · marcar a sílaba do meio · escrever a sílaba que falta · ordenar sílabas e formar a palavra · recortar e colar. Cada folha nasceu de um VERBO impresso em folhas reais de papel (41 pesquisadas); 45 figuras do banco, voz em tudo, teclado na tela e de verdade, chave mestra **1275@**, continua de onde parou por 55 min. **NÃO usa o motor** — ~49 min de aula | `_alfa1` | https://vidalprof.github.io/a-fabrica-de-palavras/ |
| **UNO das Cores** | Jogo de UNO completo contra o robô: combinar por COR, por NÚMERO ou por tipo de carta (pula, inverte, +2, coringa) — atenção, classificação por atributo e primeiras estratégias; tutorial em slides, mascote e narração | `_uno1` | https://vidalprof.github.io/jogoUno1-/ |
| **O Trem do Alfabeto** | Alfabeto, sílabas e palavras | `_trem` | https://vidalprof.github.io/o-trem-do-alfabeto/ |
| **Somando com Desenhos — a folha viva** (TESTE, 8/set) | Matemática: adição até 10 com desenhos (EF01MA06). Uma folha real de PDF (6 páginas) resolvida no computador: digitar no quadradinho (teclado na tela e de verdade), ligar soma ao resultado com linha, desenhar e somar, nome na capa, voz lendo cada enunciado. Fonte da folha: atividadesdealfabetizacao.com.br | `_folha` | https://vidalprof.github.io/folha-viva-soma-ate-10/ |
| **Pinta e Monta** | Arte/coordenação: a criança pinta por área (balde), o desenho se recorta em quebra-cabeça de verdade (com encaixes), as peças caem numa bandeja e ela monta no quadro (8 desenhos, 12→16→20 peças; fundo de ateliê) | `_pinta` | https://vidalprof.github.io/pinta-e-monta/ |
| **A Padaria das Letras** | Alfabeto e pedaços das palavras | `_padaria` | https://vidalprof.github.io/a-padaria-das-letras/ |
| **A Lojinha de Brinquedos do Pipo** | Sistema monetário (moedas e cédulas) | `_lojinha` | https://vidalprof.github.io/a-lojinha-de-brinquedos-do-pipo/ |
| **A Floresta dos Números** | Números (1º ano) | — | https://vidalprof.github.io/floresta-dos-numeros-1ano/ |
| **Ilha das Letras — Aventura do Alfabeto** | Alfabeto / sequência | — | https://vidalprof.github.io/alfbetosequencia1-/ |

## 2º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **A Feirinha da Dona Coruja** | Adição/subtração: juntar, acrescentar, separar, retirar, comparar (com digitar-resultado e arrastar) | `_feirinha` | https://vidalprof.github.io/feirinha-da-coruja/ |
| **As Plaquinhas do Téo** | Substantivos próprios e comuns | `_subs` | https://vidalprof.github.io/as-plaquinhas-da-coruja/ |
| **A Cidade dos Sólidos** | Sólidos geométricos | `_solidos` | https://vidalprof.github.io/a-cidade-dos-solidos/ |
| **Brincar e Aprender com o Léo — Prova de Ed. Física** | Educação Física (avaliação trimestral) | `_edf2` (+ `_edf2painel`) | https://vidalprof.github.io/educacao-fisica-2ano/ · [painel](https://vidalprof.github.io/painel-ef-2ano/) |
| **Mundo dos Números — Juntar e Tirar** | Adição/subtração | — | https://vidalprof.github.io/AdicaoSubtra-o2-2-ano/ |
| **Caça-Letras — A Aventura das Palavras** | Ortografia | — | https://vidalprof.github.io/ortografia2-/ |

## 3º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **UNO dos Números** (3º ano) | Matemática + estratégia: UNO contra um robô que PENSA (guarda coringa, encadeia pula/gira, ataca quando você está quase ganhando, conta cartas). De vez em quando a mesa impõe uma REGRA DA RODADA sobre o número da carta — par/ímpar, maior que a da mesa, soma 10. Tutorial em slides, narração e alívio invisível para quem perde seguido | `_uno345` | https://vidalprof.github.io/uno-dos-numeros-345/?ano=3 |
| **Prova de Matemática — Coruja Cora** | Adição/subtração: conceitos, significados e algoritmos (com reagrupamento) | `_mat2` (+ `_mat2painel`) | https://vidalprof.github.io/matematica-2ano/ · [painel](https://vidalprof.github.io/matematica-2ano-painel/) |
| **O Museu Vivo dos Bichos** | Ciências: vertebrados e invertebrados | `_museu` | https://vidalprof.github.io/o-museu-vivo-dos-bichos/ |
| **Prova de Ciências** | Ciências (avaliação, 3º ano) | — | https://vidalprof.github.io/prova-ciencias-3ano/ · [painel](https://vidalprof.github.io/painel-ciencias-3ano/) |
| **O Livro dos Mapas** (cartografia) | Geografia: representação cartográfica de Blumenau, mapa, planta, bússola | `_carto` (+ `_cartopainel`) | https://vidalprof.github.io/cartografia-3ano/ · [painel](https://vidalprof.github.io/cartografia-3ano-painel/) |
| **Blumenau, a Nossa Cidade** | Geografia: a cidade e o mapa | `_blu` | https://vidalprof.github.io/blumenau-nossa-cidade/ |
| **Aventura no Espaço — Sistema Solar** | Ciências (sistema solar) | — | https://vidalprof.github.io/Sistemasolar3ano/ |
| **O Observatório do Órbi** | Ciências | — | https://vidalprof.github.io/observatorio-do-orbi/ |

## 4º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **UNO dos Números** (4º ano) | Matemática + estratégia: UNO contra um robô que PENSA (guarda coringa, encadeia pula/gira, ataca quando você está quase ganhando, conta cartas). De vez em quando a mesa impõe uma REGRA DA RODADA sobre o número da carta — múltiplos de 3 e de 5, dobro e metade da carta da mesa. Tutorial em slides, narração e alívio invisível para quem perde seguido | `_uno345` | https://vidalprof.github.io/uno-dos-numeros-345/?ano=4 |
| **A Bancada da Divisão** | Matemática (4º ano): DIVISÃO do começo pela CONTA ARMADA com MATERIAL DOURADO que o aluno ARRASTA (a dinâmica da Oficina da Divisão, agora como peça do motor) — repartir um bloco por grupo, trocar a sobra (o "abaixa") e digitar o resultado. 32 contas progressivas | `_gincana` | https://vidalprof.github.io/a-bancada-da-divisao/ |
| **A Oficina das Palavras** | Aumentativo/diminutivo, sílabas, mau×mal, verbos | `_por4` | https://vidalprof.github.io/a-oficina-das-palavras/ (painel embutido) |
| **A Viagem no Tempo do Vale** | História (EF04HI01): colonização do Vale do Itajaí — Xokleng, açorianos, alemães (1850), italianos (1875), africanos; mudanças e permanências. Site de pesquisa + quiz | `_vale4` (+ painel) | https://vidalprof.github.io/a-viagem-no-tempo-do-vale/ |
| **Confeitaria Mágica — Divisão** | Matemática (4º ano): divisão — repartir igual, tabuada, relação com a multiplicação | `_pub_confeitaria` | https://vidalprof.github.io/confeitaria-da-divisao/ |
| **A Máquina do Tempo do Vale** | História 4º: mesma temática, formato app-trilha com simuladores | `_historia` | https://vidalprof.github.io/maquina-do-tempo-do-vale/ |

## 5º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **A Oficina do Material Dourado** (livro de folhas · 5º ano) | Matemática (divisão com material dourado — EF05MA07): 10 folhas interativas em sequência — valor das peças (ligar), qual é o número, MONTAR o número pondo as peças na mesa (manipulação, não digitar), repartir igual em grupos, a TROCA do "abaixa", divisão com resto, a conta armada na chave, ligar conta ao resultado, problemas do dia a dia e a prova real. As peças (cubinho, barra, placa, cubão) são desenhadas em SVG pela casa, em 3D; cada abertura sorteia itens novos; voz em toda folha, teclado na tela e de verdade, continua de onde parou por 55 min; chave mestra **1275@** no campo do nome abre o menu de folhas. **NÃO usa o motor** (HTML próprio, como a Oficina da Divisão e o UNO) — ~52 min de aula | `_dourado5` | https://vidalprof.github.io/oficina-do-material-dourado/ |
| **UNO dos Números** (5º ano) | Matemática + estratégia: UNO contra um robô que PENSA (guarda coringa, encadeia pula/gira, ataca quando você está quase ganhando, conta cartas). De vez em quando a mesa impõe uma REGRA DA RODADA sobre o número da carta — múltiplos de 3, a SOMA das duas cartas múltiplo de 3, dobro, soma 10. Tutorial em slides, narração e alívio invisível para quem perde seguido | `_uno345` | https://vidalprof.github.io/uno-dos-numeros-345/?ano=5 |
| **A Grande Expedição** | Matemática (5º ano, divisão — EF05MA07): estratégias de raciocínio para dividir — repartir igual, quantas vezes cabe (medida), estimativa, tabuada, resto e divisor de até 2 algarismos | `_divisao` | https://vidalprof.github.io/a-grande-expedicao-divisao/ |
| **A Oficina da Divisão** | Matemática (4º/5º ano): raciocínio da CONTA ARMADA com MATERIAL DOURADO que o aluno MOVE (milhar/centena/dezena/unidade) — 32 contas progressivas; ARRASTA (não vale clicar) uma rodada para todos os grupos, troca a sobra (reagrupa/"abaixa") e DIGITA o resultado; nome + relatório final em % (exceção ao motor, HTML próprio) | `_dourado` | https://vidalprof.github.io/oficina-da-divisao/ |
| **A Revista das Palavras** | Português (5º ano): ler e interpretar DIFERENTES GÊNEROS (bilhete, convite, lista, aviso, e-mail, carta, poema, tirinha, anúncio, receita, notícia, regras, dobradura, fábula, verbete, quadrinha, trava-língua, propaganda, diário) + RETIRAR do texto substantivos, adjetivos e verbos — 34 fases, 9 mecânicas | `_revista5` | https://vidalprof.github.io/a-revista-das-palavras/ |
| **Expedição Santa Catarina** | Geografia: Florianópolis, Blumenau e o estado (revista + quiz 30q) | `_sc5` (+ `_sc5painel`) | https://vidalprof.github.io/santa-catarina-5ano/ · [painel](https://vidalprof.github.io/santa-catarina-5ano-painel/) |
| **O Teatro das Palavras** | Português (5º ano) | `_teatro` | https://vidalprof.github.io/o-teatro-das-palavras/ |
| **A Agência dos Detetives das Palavras** | Pronomes, interpretação (narrativo/injuntivo), mau×mal | `_detetive` | https://vidalprof.github.io/detetives-das-palavras/ |

## 6º ano

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **A Central de Entregas** | Língua Portuguesa: gêneros textuais | `_central` | https://vidalprof.github.io/a-central-de-entregas/ |
| **Mundo das Palavras — Substantivos e Adjetivos** | Classes de palavras | — | https://vidalprof.github.io/classesdepalavras6-/ |
| **Climas do Mundo — A Volta ao Mundo de Nimbo** | Geografia: climas | — | https://vidalprof.github.io/climas-do-mundo-6ano/ |

## 8º / 9º ano (Inglês)

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **RIGHT NOW — Flagra na Cidade** | Inglês 9º: Present Continuous (a pasta publicada é `_rightnow9`; `_agora` é um rascunho anterior da mesma atividade, guardado) | `_rightnow9` | https://vidalprof.github.io/right-now-flagra-na-cidade/ |
| **Relative Pronouns — Connecting Ideas** | Inglês 8º: pronomes relativos | — | https://vidalprof.github.io/InglesRelativePronouns8/ |

## Outras / diversas

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **Meu Pixel Art** | Arte digital / pixel | `_pixel` | https://vidalprof.github.io/meu-pixel-art/ |
| **Prova — Viagem pelo Brasil** | Geografia do Brasil (avaliação) | — | https://vidalprof.github.io/prova-viagem-brasil/ · [painel](https://vidalprof.github.io/painel-viagem-brasil/) |
| **O Tangram da Vovó Marta** | Geometria / tangram (montar figuras com as 7 peças) — 7 fases novas de ANIMAIS (gato, peixe, cisne, passarinho, tartaruga, cachorro, pato) mais difíceis, sem a ajuda que pisca; fala do montar só com a dica das peças | `_tangram` | https://vidalprof.github.io/o-tangram-da-vovo-marta/ |
| **Jardim do Broto** | — | `_jardim` | https://vidalprof.github.io/jardim-do-broto/ |
| **A Terra dos Papagaios** | — | `_naveg` | https://vidalprof.github.io/a-terra-dos-papagaios/ |
| **O Voo do Nico** | — | `_mapa` | https://vidalprof.github.io/o-voo-do-nico/ |
| **Letreiros de Blumenau** | — | — | https://vidalprof.github.io/o-letreiro-de-blumenau/ · https://vidalprof.github.io/a-oficina-de-letreiros/ |
| **O Grande Circo do Teo** (base premium) | — | — | https://vidalprof.github.io/circo-do-teo/ |
| **A Fábrica de Brinquedos do Bento** | — | — | https://vidalprof.github.io/fabrica-do-bento/ |
| **A Fazendinha do Teco** | — | — | https://vidalprof.github.io/fazendinha-do-teco/ |
| **Vila da Tabuada** | Matemática: tabuada | — | https://vidalprof.github.io/vila-tabuada/ |
| **Cidade do Dinheiro — Sistema Monetário** | Sistema monetário | — | https://vidalprof.github.io/sistemamonetario2-5ano/ |
| **Poli e o Tesouro do Mar** | — | — | https://vidalprof.github.io/poli-tesouro-do-mar/ |
| **A Vila do Miau** | — | — | https://vidalprof.github.io/vila-dos-livros-miau/ |

## Ferramentas do professor

| Atividade | O que trabalha | Pasta | Link |
|---|---|---|---|
| **Painel de Atividades** | Todos os links por turma, com busca e botão de copiar — gerado deste catálogo | `_painel` | https://vidalprof.github.io/painel-de-atividades/ |

## Portal / hub

| — | — | — | — |
|---|---|---|---|
| **Ilhas do Saber** (mapa com os cards) | Portal que reúne as atividades | `_site` | https://vidalprof.github.io/mundo-das-atividades/ |

---

