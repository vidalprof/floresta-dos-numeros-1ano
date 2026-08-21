# 🏭 LINHA DE PRODUÇÃO COM AUTOAPRENDIZADO — como o sistema evolui até ficar perfeito

> Pedido do Marcos (jul/2026): "monte uma linha de produção com autoaprendizado, para o
> sistema evoluir e ficar perfeito". Este é o processo que TODA fase/aventura percorre antes
> de chegar ao Marcos e às crianças. Cada rodada deixa o sistema mais perfeito — de propósito.

## A esteira (7 estações)

```
1. ROTEIRO/SPEC      2. MOTOR MONTA        3. ROBÔ-LÓGICA        4. AUDITOR VISUAL/DESIGN
   (a história)  ->     (das peças    ->      (JOGA até o     ->    (JOGA + tira fotos +
   em dados            prontas, valida)       fim como aluno)       game designer infantil
                                              pega "travou")        por faixa etária)
        v                                                                    v
7. PUBLICA <- 6. PORTÃO DE ARTE (Marcos)  <-  5. CORRIGE + VIRA TESTE PERMANENTE (autoaprendizado)
   (link)          olhos humanos                cada bug/melhoria entra na memória e no robô
```

## Estação por estação

1. **ROTEIRO → SPEC.** O roteirista/pedagogo define a fase em DADOS (não em código solto):
   quem é o personagem, qual o problema, onde ficam casa/porta/itens, o desafio pedagógico,
   as falas, a recompensa, o que muda no mundo. (É o `AdventureSpec` da arquitetura — validado
   por Zod: "dado torto não monta".) **Improvisar no código = fonte dos bugs; a spec elimina isso.**

2. **MOTOR MONTA.** O engine constrói a fase a partir da spec, usando só peças prontas do pack
   (tiles, personagens, interiores, sons, música). Nada desenhado à mão → acaba a classe de
   bug de recorte.

3. **ROBÔ-LÓGICA (`qa-f1.mjs` etc).** JOGA a fase inteira como um aluno: coleta, entra na casa,
   entrega, o mundo muda, vence. Se o aluno NÃO conseguisse concluir por bug → **REPROVA e nada
   chega ao Marcos**. É o detector nº1 de "travou, não dá pra fazer". 100% confiável.
   Cobre também: textura faltando, sprite vazando da moldura, herói preso numa zona,
   destravamento garantido das transições.

4. **AUDITOR VISUAL/DESIGN (`capturar-fase.mjs` + agente).** JOGA, tira screenshots dos momentos-
   chave, e um agente com VISÃO os revisa como um **game designer profissional que conhece o
   encantamento infantil POR FAIXA ETÁRIA** (pré → 9º). Devolve: (a) bugs visuais que o headless
   não vê (corte, desalinho, proporção), (b) sugestões de melhoria adequadas a cada idade.
   É a rede que pega o que o robô-lógica não enxerga.

5. **CORRIGE + AUTOAPRENDIZADO.** Cada bug encontrado é corrigido E **vira teste permanente** no
   robô (a checklist CRESCE → o mesmo erro nunca volta). Cada melhoria de design vira diretriz na
   memória. É aqui que o sistema "aprende": o robô de amanhã é mais rigoroso que o de hoje.

6. **PORTÃO DE ARTE (Marcos).** Olhos humanos no resultado final — o que só quem sente o jogo pega.
   Reclamação do Marcos = ouro: cada uma virou teste (travou→teste, moldura→teste, mel-na-casa→teste).

7. **PUBLICA.** Só passa quem está verde nas estações 3-4 e aprovado na 6. Vai pro ar como LINK.

## Por que isso fica PERFEITO com o tempo (o autoaprendizado)

- O conjunto de **testes do robô só cresce** — cada fase nova herda todos os testes das anteriores.
- As **diretrizes de design** (o que encanta cada idade) se acumulam na memória e passam a guiar
  a montagem desde o início → menos retrabalho.
- A **spec** vira modelo reutilizável: a próxima fase começa de um molde já aprovado.
- Resultado: a 10ª fase nasce quase sem bug, porque atravessa uma esteira que já aprendeu com as 9.

## Estado atual (jul/2026)
- Estações 2, 3, 6, 7: **funcionando** (Fase 1 prova: QA 15/15, publicada, olhos do Marcos).
- Estação 4 (auditor visual/design por idade): **em construção** (capturador pronto; agente sendo
  ligado ao pipeline).
- Estação 1 (roteiro→spec formal) + gerador automático: **próximo grande passo** — é o que tira o
  "improviso no código" de vez (a raiz de vários bugs que o Marcos pegou).
