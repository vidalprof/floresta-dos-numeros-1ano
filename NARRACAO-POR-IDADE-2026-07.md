# Narração POR FAIXA ETÁRIA — regra do EduVerse (criança pequena lê pouco → tudo falado) — 2026-07

> Pedido do Marcos: "tem que ser TUDO narrado, até as explicações, porque são pequenos; verifique por faixa
> etária pra não ficar chato, como era na atividade premium. O certo é contar COM as crianças, falado."
> Pesquisa: no "lido em voz alta" a criança ouve ~3× mais palavras que só no texto; pré/início-leitor
> depende da voz + animação. Força: [FORTE].

## LEI: nenhuma instrução/explicação essencial FICA SÓ ESCRITA para quem ainda não lê fluente.
A voz (Antônio/edge-tts, natural — nunca a robótica do navegador) diz o problema, **conta JUNTO**, explica a
descoberta e incentiva. O texto na tela é REFORÇO, não a via principal. Sempre ter como **ouvir de novo**.

## POR FAIXA ETÁRIA (quanto narrar sem cansar)
- **Pré · 1º · 2º ano (~5–8, pré/início-leitor) — NARRAR TUDO, SEMPRE.** Cada tela, cada dica, cada explicação,
  falada. Ritmo mais lento, frases curtas e lúdicas. **Contagem sempre em voz alta** ("um… dois… três!").
  Texto mínimo, só palavra-chave em destaque. A ANIMAÇÃO + a VOZ carregam; leitura é bônus.
- **3º · 4º · 5º ano (~8–11, leitor em formação) — NARRAR OS MOMENTOS-CHAVE.** Falar: o problema/convite, a
  **contagem junto**, a **institucionalização** (a "descoberta": "isso é multiplicar"), e o incentivo. NÃO
  narrar cada micro-passo (cansa quem já lê um pouco). Texto acompanha, mas nunca é obrigatório ler.
- **6º–9º ano (~11–14, leitores) — NARRAÇÃO LEVE.** Voz na abertura, nas viradas e no incentivo; curta, pra
  não infantilizar. Mais autonomia de leitura; áudio opcional/repetível.

## O QUE SEMPRE NARRAR (todas as faixas, dose conforme acima)
1. **O problema/convite** (a Fagulha pergunta, não responde).
2. **Contar JUNTO** toda vez que há contagem — sincronizado com o que acende ("quatro… oito… doze!"). É o
   "contar com as crianças" que o Marcos pediu.
3. **A descoberta (institucionalização):** nomear a matemática no fim ("três grupos de quatro é 3×4 = 12").
4. **Incentivo** específico (não genérico): "você virou de lado e deu o mesmo!".
5. **Dicas** quando erra — faladas, gentis, nunca punir.

## COMO FICA NESTA ATIVIDADE (3º ano → tier 8–11)
- Intro de cada parada: falada. ✅ (feito)
- **Explicação/contagem no acerto:** falada, com **contagem junto** + a descoberta. ← agora.
- Dicas de erro: falar as principais (próxima camada).
- Final: falado (volta logo). ✅

## PADRÃO TÉCNICO
- Áudio por `gerar-audio.yml` (voz natural), tocado com `<audio>` + **lip-sync** da Fagulha. `falar()` já
  trata áudio ausente sem travar; toca destrava no 1º gesto (regra do navegador).
- Para contagem SINCRONIZADA fina (número a número aceso), o passo seguinte é gerar os números soltos
  ("quatro","oito"…) e tocar casado com a animação — hoje uso a frase-recapitulação ("quatro… oito… doze!").

## FONTES
read-aloud por idade https://maestra.ai/blogs/read-aloud-book-apps-for-kids · word-sync/velocidade
https://gramms.ai/blog/best-read-along-apps-for-kids/ · ganho de vocabulário (3×) — pesquisa de picture-book read-aloud.
