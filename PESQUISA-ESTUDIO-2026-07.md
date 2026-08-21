# 🏭 Pesquisa de ferramentas do ESTÚDIO (processo de produção) — jul/2026

> 2º pedido do Marcos: "pesquise OUTRA ferramenta profissional que melhore algum ponto do
> processo de produção, deixe mais profissional e sem erro, alavanque e torne o estúdio mais
> ágil." Foco no PIPELINE (não na engine — Phaser 3 fica). Só o que é grátis de verdade e leve.

## TOP 5 adoções de maior impacto (ranqueado por impacto × baixo esforço)

**1º — Visual regression: `Playwright toHaveScreenshot` (baseline gerada no Linux do Actions).**
Compara a tela nova com uma foto-base aprovada e ACUSA sozinho objeto cortado/desalinhado/sumido.
Resolve direto o que hoje depende de olho humano/agente-visão. Grátis (já usamos Playwright).
⚠️ gerar as baselines DENTRO do Actions (Linux), senão dá falso-positivo por fonte/SO.
Se ficar lento, trocar o motor de diff por **odiff** (6–7× mais rápido, baseline compatível).
NÃO adotar Percy/Chromatic (pago, dashboard na nuvem = overkill p/ 1 pessoa).

**2º — Quality gate no GitHub Actions que BLOQUEIA publicação** (`needs:` build → QA → visual →
axe/Lighthouse). Transforma os "3 portões" de manuais em AUTOMÁTICOS: nada quebrado vai ao ar.
Cachear o Chromium pela VERSÃO do Playwright (não pelo lockfile); subir report/traces como artifact;
retry 1×.

**3º — Hook `window.__PHASER_GAME__` + asserts de ESTADO no robô-QA.** Eleva o QA de "não quebrou"
para "verifica a REGRA pedagógica" (o Byte perguntou? pontuação subiu? fase completou?). É o padrão
profissional de testar jogo web (dirigir o Phaser expondo o estado no window) — já fazemos parecido
(`__fase1`, `__grid`); formalizar como padrão fixo.

**4º — `ffmpeg-normalize` (loudnorm two-pass, alvo -16 LUFS / -1.5 dBTP) no `otimizar-audio.yml`.**
Deixa TODA narração/SFX no mesmo volume percebido (nada de uma fase gritando e outra sussurrando).
Padrão broadcast, esforço ridiculamente baixo (1 passo no workflow que já existe).

**5º — LLM-as-judge com `promptfoo` validando o conteúdo contra a filosofia + BNCC.** Um LLM-juiz dá
nota e justifica se a atividade respeitou a LEI (`EDUVERSE-FILOSOFIA.md`: Byte pergunta não responde;
problema antes do conceito; BNCC do ano) ANTES de chegar ao Marcos. Automatiza o Portão 0/2. Centavos
de API por atividade; integra no CI (YAML simples, sem servidor).

**Menções honrosas:** `free-tex-packer` (CLI, junta sprites num atlas = mais leve no PC fraco);
`GoatCounter`/`Umami` (saber se a atividade funcionou, SEM rastrear a criança — cookieless, ético);
`@axe-core/playwright` (acessibilidade/contraste em CI); `Lighthouse CI` (garante abrir rápido no PC
velho, com performance budget que falha o build se estourar).

## O que NÃO adotar (pra não inflar um estúdio de 1 pessoa)
- **Percy/Chromatic** (pago, dashboard desnecessário) — a "aprovação de baseline" fazemos por commit + agente-visão.
- **BAML / Instructor / Outlines** — Zod + TS já resolve structured output; no máximo um retry re-injetando o erro do Zod no prompt (10 linhas).
- **Storybook** — é p/ design system web; cada atividade é 1 HTML com Phaser. Nosso Chromium+screenshot já cobre "ver sem publicar".
- **ElevenLabs** (free tier pequeno); **i18n** (prematuro, só pt-BR hoje); **Honeydiff** (novo demais).
- **Aseprite** — só se um dia formos editar pixel à mão (usamos pack CC0 + IA). Grátis alternativo p/ retoque: **Pixelorama**.

## Por etapa (detalhe)
- **Arte:** o ganho é EMPACOTAR/otimizar, não desenhar → `free-tex-packer` (Phaser nativo, CLI no Actions).
  Autocrop do que a IA gera: nosso script Pillow já é o certo. Licenças: manter `assets.json` com SPDX (`CC0-1.0`).
- **QA:** visual regression (item 1) + asserts de estado (item 3) = o maior salto de "sem erro".
- **CI/CD:** quality gate (item 2) com `needs:` e cache do Chromium por versão.
- **IA de conteúdo:** manter Zod; adicionar eval com `promptfoo`/`DeepEval` (item 5).
- **Áudio:** manter Edge-TTS como principal; **Piper TTS** (local, MIT, pt-BR) como backup offline/volume;
  `ffmpeg-normalize` (item 4); SFX CC0 com **jsfxr**/**ChipTone**; música Kenney Audio (CC0).
- **Telemetria ética:** `GoatCounter` (cookieless, grátis não-comercial) medindo só evento agregado ("fase X concluída"), nunca identificar aluno.
- **Acessibilidade/perf:** `@axe-core/playwright` (WCAG em CI) + `Lighthouse CI` (perf budget p/ PC fraco).

## Onde isso encaixa no que JÁ temos
Já temos robô-QA (Playwright) e auditor visual (screenshot + agente-visão). Os itens 1, 2 e 3 são a
evolução natural DISSO — mais automático e mais rigoroso. A `LINHA-DE-PRODUCAO.md` ganha portões
automáticos de verdade. Nada aqui troca o que funciona; tudo SOMA.
