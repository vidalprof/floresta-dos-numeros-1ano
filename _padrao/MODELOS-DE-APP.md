# MODELOS DE APP — seis CASCAS para o mesmo motor (proposta, set/2026)

> Pedido do Marcos (2026-09-07): *"uns 5 a 6 modelos de app das nossas atividades,
> modernos, leves, fluidos, responsivos, para nós variarmos com o modelo que temos
> atualmente — assim a criança pensa que está fazendo algo novo sempre"*.
>
> **A ideia central: separar CASCA de MIOLO.** O miolo (as 91 peças, o `conteudo.json`,
> a voz, o andaime, a retomada de 55 min, o boletim, a banca) não muda. O que muda é
> a **casca**: como a criança entra, como anda de uma fase para a outra, como vê o
> progresso e como a atividade termina. É a casca que dá a sensação de "app novo".
> Hoje todas as atividades usam a mesma casca (capa → crachá → fases em sequência com
> balão e barra/vitrine → medalha). Com seis cascas, a mesma padaria de peças vira
> seis apps diferentes aos olhos da criança — e o conteúdo, a banca e o custo continuam
> os de sempre.
>
> **Como entra no conteúdo:** um campo no `conteudo.json`, `"casca": "trilha"` (padrão:
> `"classica"`, a de hoje). O `montar.py` embute a casca escolhida; o motor desenha a
> capa, o entre-fases, o progresso e o fim conforme ela. Peça nenhuma sabe da casca.

## As seis cascas

| # | Casca | A criança vê | Entre as fases | Progresso | Fim | Encaixe |
|---|---|---|---|---|---|---|
| 1 | **Trilha / mapa** | um caminho com paradas numeradas e o mascote andando | volta ao mapa por ~1 s, o mascote pula para a próxima parada | as paradas ficam verdes | a bandeira no fim do caminho | qualquer conteúdo, 1º–9º; ótima para atividade longa (a criança VÊ quanto falta) |
| 2 | **Livro / revista** | uma página de livro com figura, texto curto e a peça | a página VIRA (dobra do canto) | número da página e marcador | o livro fecha e mostra a capa com a medalha | Português, História, leitura (Revista, Teatro, Detetives, Máquina do Tempo) |
| 3 | **Baralho de cartas** | uma carta grande com a pergunta/peça; o baralho atrás | a carta feita desliza para a pilha, a próxima entra | baralho afinando + "4 de 8" | a última carta vira a medalha | relâmpago, quiz, vocabulário, revisão; 3º–9º; excelente no celular |
| 4 | **Bancada / oficina** | uma cena fixa (mesa) com o quadro de pedidos pregados | o pedido é riscado, o próximo acende | notas no quadro | o quadro cheio de ✓ | Matemática e Ciências com manipuláveis (caixa de 10, balança, divisão, medir); 1º–5º |
| 5 | **Conversa com o mascote** | tela de mensagens: o mascote manda a pergunta, a peça aparece dentro do balão | a conversa rola | a conversa cresce; "faltam 3" | o mascote manda a medalha e a foto do que ela fez | 1º–3º e línguas; carga cognitiva mínima, uma coisa por vez, retomar é rolar |
| 6 | **Programa de auditório** | palco, telão, 4 botões grandes, plateia | "próxima rodada!" com luz e som | estrelas (nunca pontos, nunca ranking) | chuva de confete no palco | aquecimento e revisão, 4º–9º; casa com relâmpago e quiz |

## O que é comum a todas (não negociável)

- **Mesmo miolo:** peças, balão narrado, alto-falante nas respostas, andaime, boletim,
  relatório do professor, retomada de 55 min, senha `1275@`.
- **Leve:** só CSS e o JS do motor. Nenhuma biblioteca. Uma casca custa ~15 KB.
- **Fluido:** transições só de `transform`/`opacity` (portão `gamefeel` R5) e nada em
  laço sob `prefers-reduced-motion`.
- **Responsiva:** os 6 tamanhos da banca (320 px a 1366 px), alvo ≥ 44 px até o 2º ano.
- **Sem ranking, sem moeda, sem vida** (Portão 0 e `EDUVERSE-FILOSOFIA.md`).
- **A banca não muda:** `auditar.sh` mede a casca como mede a de hoje — a cobaia de
  91 mecânicas roda uma vez por casca antes de ela entrar no catálogo.

## Ordem que proponho (custo × ganho)

1. **Conversa** — a mais barata (é um `.tela` em coluna que empilha balões) e a de maior
   contraste com a casca atual. Serve as turmas de 1º–3º, onde está a maior parte das
   atividades.
2. **Trilha** — a segunda mais barata (um SVG com o caminho + paradas posicionadas em %).
   Resolve o "quanto falta" de atividades longas (Trem, Padaria, Gincana).
3. **Cartas** — transição de deslizar + pilha. Ideal para as de 4º–5º (Divisão, Oficina).
4. **Livro** — a virada de página é a parte cara (dobra em CSS, com queda para deslizar
   no Chrome antigo).
5. **Show** — palco e plateia são arte de IA (2 figuras), o resto é CSS.
6. **Bancada** — a mais cara porque a mesa é uma CENA por atividade (arte de IA) e os
   manipuláveis precisam "morar" nela.

Cada casca: ~1 dia de trabalho (casca + cobaia + banca numa atividade real) e entra
no `_padrao/INTERATIVIDADES.md` como ✅ só depois da banca.

## O que a pesquisa diz sobre variar (para não variar à toa)

- Criança de 4–8 anos "toca antes de ler, perde o interesse mais rápido do que o adulto
  espera e responde mais a personagem e imagem do que a texto" — por isso a variação
  tem que ser de **cena e gesto**, não de texto (`_pesquisa/web/modelos-de-app-infantil-navegacao.md`).
- **Uma ação por tela** e nenhum fluxo que dependa de memória (voltar, confirmar). As
  seis cascas respeitam isso: em nenhuma a criança precisa "navegar".
- Duolingo: "jogar primeiro, perfil depois" — a criança já está jogando em 15 s. Nas
  cascas, a capa continua de um toque, e o crachá vem depois da primeira fase quando a
  casca for Conversa ou Cartas (a proposta é testar isso na banca do professor).
- Personagem familiar como **guia** (PBS Kids, Noggin): reduz ansiedade e abre para o
  novo. Por isso a casca muda, mas o **mascote da casa continua o mesmo** dentro dela —
  ver `_pesquisa/MASCOTE-E-AVATAR.md`.
- Recompensa **parcimoniosa**: "pequenas conquistas que celebram marcos sem pressão".
  Estrelas no fim de rodada, não a cada toque.

## Decisão pendente

O Marcos escolhe **quais** cascas (todas ou algumas) e **em qual atividade** cada uma
estreia. Sugestão de estreia: Conversa na Padaria (1º), Trilha no Trem (1º), Cartas na
Oficina das Palavras (4º), Show na Gincana da Divisão (5º), Livro na Revista (5º),
Bancada na Feirinha (2º).
