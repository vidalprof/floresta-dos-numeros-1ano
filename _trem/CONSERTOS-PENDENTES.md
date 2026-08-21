# Trem do Alfabeto (1º ano) — consertos PENDENTES (agendados p/ DEPOIS do pré)

Pedidos do Marcos (2026-08-20). **Só executar depois que "O Ateliê de Cores da Rai"
(pré) estiver publicado.** Publicado em: https://vidalprof.github.io/o-trem-do-alfabeto/

Ao consertar: rodar SÓ os portões do que mexi (a banca é otimizada — não a banca
inteira). Cada defeito que escapou vira lição no CONTRATO/MEMORIA + portão novo.

1. **"I de elefante" (errado).** Elefante começa com **E**, não I. Conferir a
   associação letra↔palavra/imagem e a fala. Provável troca de índice/letra numa
   fase de "letra inicial". Regravar só a(s) voz(es) afetada(s).
   → portão novo: acusar "letra ≠ primeira letra da palavra associada".

2. **Tela da IGREJA narra em INGLÊS.** Corrigir a fala para português (voz
   pt-BR). Conferir se o texto/objeto veio com termo em inglês (church) ou se o
   id da voz caiu no mp3 errado.
   → portão novo: acusar fala em idioma errado / palavra não-PT.

3. **Fase "Começa com": barra de rolagem.** Tirar a barra (conteúdo tem que
   caber). As **figuras sem fundo e sem borda**, dentro da moldura; **uma
   moldura só, a externa** (hoje parece ter moldura dupla / borda na figura).

4. **Fase "Ligar / ponto a ponto": pontos menores + animação melhor.** Reduzir o
   tamanho dos pontos e melhorar a animação do traço/ligação.

5. **Fases de PINTAR do Trem: área menor p/ não rolar.** O canvas/área de pintura
   está grande demais e força barra de rolagem — reduzir a área para caber na tela
   (medir com _qa/leiaute.js). Vale para todas as fases de pintar do Trem.

6. **Fase "em ordem": letras em PORTUGUÊS.** A voz fala o "i" como "ai" (inglês);
   e a **explicação depois do acerto também sai em inglês**. Corrigir toda a
   narração dessa fase para pt-BR (nomes das letras em português: a, bê, cê, dê,
   é, efe... "i" = /i/, não /ai/). Regravar as vozes afetadas.

7. **Fase "que letra": botões menores + letras mais premium.** Reduzir o tamanho
   dos botões e deixar as letras mais bonitas/premium (tipografia, brilho,
   acabamento) — sem quebrar o leiaute (medir com _qa/leiaute.js).

8. **Fase "o trem chegou": enunciado errado.** Fala "toque nos vagões que faltam";
   deveria ser **"toque nas letras para completar o alfabeto"**. Corrigir texto +
   voz.

9. **"U de ovo" (errado).** Ovo é com **O**. Mesma classe do item 1 (I de
   elefante): associação letra↔palavra trocada. Conferir TODAS as letras/palavras
   da(s) fase(s) de letra inicial de uma vez.

> ⚠️ Itens 1 e 9 (e talvez mais) são o MESMO defeito: pares letra↔palavra
> trocados. Ao consertar, revisar o mapa INTEIRO de letra→palavra→imagem→voz e
> criar o portão "letra ≠ 1ª letra da palavra" para pegar todos de uma vez.

Publicar o Trem depois: `atualizar.yml repo_name=o-trem-do-alfabeto` (ref na
branch de trabalho) e mandar o link ao Marcos.

11. **Fase "começo da palavra": imagens faltando pedaços.** As figuras estão
    sendo cortadas (recorte comendo parte). Refazer o recorte/enquadramento.

12. **Fase "bate a sílaba": inadequada p/ 1º ano.** O 1º ano ainda não tem o
    conceito de sílaba consolidado — remover ou trocar por algo de letra/som
    inicial. (Ver também a fase "escreva a letra" — enunciado da letra T horrível,
    e "ligar os pontos" ficou feio: avaliar remover essas.)

13. **Fase "monte a palavra": voz diz "jacarré" em vez de "jacaré".** Erro de
    pronúncia/gravação — regravar essa fala (grafia que a voz leia certo).

14. **Mover as fases de COLORIR para o FINAL** da atividade do Trem (ordem das
    fases).

15. **Opções de resposta na HORIZONTAL.** No 1º ano, dispor as opções de resposta
    em linha (horizontal) ajuda a leitura/escolha. Aplicar onde couber.

16. **Fase "escreva a palavra": fundo branco nas imagens + repetição.** As figuras
    ainda têm FUNDO BRANCO (pedido antigo: sem fundo). E mostra sempre as MESMAS
    (casa, etc.) — variar entre as 26 figuras disponíveis. Padrão premium: MOLDURA
    DE VIDRO com a imagem dentro, SEM borda e SEM fundo.

17. **Caça-palavras FÁCIL (1º ano).** Sem diagonal e sem palavra ao contrário —
    só horizontal/vertical no sentido normal de leitura. É 1º ano.

18. **Variação de imagens (reforço do 16).** Em TODAS as fases que mostram figura,
    variar entre as 26 disponíveis — não repetir sempre casa/etc.

19. **⭐ REGRA GERAL DE MOLDURA (vale p/ QUALQUER atividade).** NUNCA moldura dentro
    de moldura. O certo: pegar a imagem **sem fundo e sem moldura**, dar um
    **quadrado ao redor** e colocar dentro da **moldura de vidro** (uma só). A
    figura não pode ter borda/fundo próprios — a moldura é a única. Aplicar em
    "escreva a palavra" do Trem e onde mais houver moldura.
    → registrar também no MEMORIA/CONTRATO como padrão permanente da casa.
