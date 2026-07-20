# 🎮 PESQUISA — Design de jogo 2D + aventura educativa de 55 min (jul/2026)

> Pedido do Marcos: "não chute nada, pesquise, aprenda com os melhores, seja expert".
> Duas frentes pesquisadas na web (fontes no fim). Guia a construção da aventura da
> tabuada (fazenda→floresta→cidade) e de TODA aventura futura da fábrica.

## PARTE A — GAME FEEL / "juice" e LEVEL DESIGN (jogos 2D profissionais)

### TOP 10 melhorias (maior impacto, menor custo — PC fraco/Chrome 109)
1. **Squash & stretch** por tween em TODO sucesso (coletar/depositar/vencer): `ease:'Back.easeOut', yoyo:true`. Custo ~zero. (Swink *Game Feel*; "Juice it or lose it")
2. **Hit-stop 2–4 quadros** no impacto (pausa breve). Vende o "aconteceu". (Vlambeer "Art of Screenshake"; Wagar)
3. **Flash de tint no alvo + `camera.flash` curto** no acerto. (Juice it or lose it)
4. **`startFollow` lerp 0.1 + `setDeadzone`** = câmera suave que não treme. (Keren "Scroll Back", GDC 2015)
5. **`camera.shake` amplitude MUITO baixa, só no SUCESSO** (nunca no erro; tremor forte enjoa criança). (Screenshake + acessibilidade NN/g)
6. **Uma "cor de interativo" fixa** (brilho quente + leve bob) em tudo tocável. Vira linguagem sem texto. (wayfinding; pixel-art readability)
7. **Cada fase pelos "4 passos" da Nintendo**: Introduzir (seguro)→Desenvolver→Twist→Conclusão. UMA ideia nova por fase. (Mark Brown/GMTK; Anna Anthropy)
8. **Onboarding só por demonstração** (seta/mão pulsando + personagem anda sozinho; migalhas + landmark ao fundo). Zero texto. (Miyamoto 1-1; Celeste; NN/g)
9. **Variação de pitch nos SFX** (`detune` ±150). Mata a fadiga do "mesmo bip". 1 linha.
10. **Tela de celebração + mapa que avança entre fases** (personagem caminha ao próximo bioma, medalha, fanfarra 2–3s). Transição VIRA recompensa. (progressão; overworld)

**Cuidado PC fraco:** partículas = efeito mais caro (teto baixo, 1 emitter, atlas). Evitar shader/post-FX. Shake diminuto. **Juice premia ACERTO, nunca pune erro** (é a LEI do EduVerso).
**Câmera/leitura:** herói + interativos com outline e cor saturada; fundo dessaturado; foco (`camera.pan`) no objetivo ao abrir a fase.

## PARTE B — AVENTURA MULTIFASE de ~55 min (6–9 anos), aprender sem perceber

### Evidência FORTE (meta-análises)
- **Clark et al. 2016** (RER 86): jogos digitais > sem-jogo, g=0,33. **O DESIGN pesa mais que "jogo vs não-jogo"** — scaffolding/feedback/personalização movem o ponteiro.
- **Wouters et al. 2013** (JEP 105): aprendizagem d=0,29, **retenção d=0,36**; jogos NÃO foram mais motivadores (alerta: engajamento ≠ aprendizado). Ajuda: **múltiplas sessões**, complementar com outra instrução, jogar em grupo.
- **Mayer 2014**: método "value-added" (jogo base vs base+1 recurso) isola o que funciona. Ceticismo metodológico.

### Frameworks (consolidados)
- **Malone & Lepper**: desafio, curiosidade, controle, **fantasia ENDÓGENA** (a matemática É o poder que move o mundo — não enfeite sobre exercício).
- **Habgood (Zombie Division)**: integração intrínseca; crianças jogaram ~7× mais a versão intrínseca.
- **Gee (36 princípios)**: identidade, erro barato (moratória psicossocial), problemas ordenados, "pleasantly frustrating", info just-in-time, significado situado, ciclo de expertise.
- **Csikszentmihalyi/Chen**: canal de flow (desafio≈habilidade); DDA leve + escolha subconsciente.
- **Dienes (múltipla incorporação)**: MESMO conceito em ≥3 "roupas" perceptuais → abstração. Multiplicar E dividir juntos (inversos), CRA (concreto→pictórico→abstrato).
- **Atenção 6–9 anos** (heurística): 7–8 ≈ 16–24 min; construto de atenção só estável ~9 anos. **55 min só é realista SEGMENTADO** (3 fases de ~13–15 min + micro-pausas); mecânica contínua única → ~30–35 min.

### ESTRUTURA IDEAL DA AVENTURA (a que vamos seguir) — fase a fase
- **0–3 min GANCHO** "o mundo precisa": o mentor apresenta o problema e PERGUNTA (não responde). Destrava voz no 1º gesto. Mini pré-teste disfarçado de "aquecimento" (stealth baseline).
- **3–16 FASE 1 FAZENDA / MULTIPLICAR** (fácil, CRA concreto): grupos iguais, fatores pequenos, feedback imediato, gating leve.
- **16–19 RESPIRO** ativo + micro-história (troca de cenário reinicia o relógio de atenção).
- **19–33 FASE 2 FLORESTA / ponte ×↔÷** (média): nova representação (array/reta numérica), sobe degrau a degrau.
- **33–36 RESPIRO** + recuperação disfarçada (retrieval espaçado dos fatos da fase 1).
- **36–50 FASE 3 CIDADE / DIVIDIR** (difícil, clímax): repartição justa; pico "pleasantly frustrating"; resolve o problema do mundo.
- **50–55 RESOLUÇÃO + CELEBRAÇÃO** + semente da próxima sessão (retenção espaçada; medalha CELEBRA, não suborna — cuidado SDT com pontos-coleira).
- Tempo ativo de matemática ≈ 42–45 min. As 3 fases = as **3 incorporações de Dienes** do mesmo "grupos iguais".

### Régua de sucesso (honestidade — Wouters/Clark)
Medir **transferência + retenção**, não engajamento. Pré/pós disfarçados + retorno espaçado 1 semana (transferência próxima e distante). Stealth assessment (Shute) já embutido no nosso motor.

## Fontes principais
Swink *Game Feel*; Vlambeer "Art of Screenshake"; Jonasson&Purho "Juice it or lose it"; Mark Brown/GMTK "4-step level design"; Anna Anthropy; Keren "Scroll Back" (GDC 2015); Phaser cameras docs; Malone&Lepper 1987; Habgood&Ainsworth 2011; Gee 2003; Csikszentmihalyi 1990 / Jenova Chen "Flow in Games"; Hunicke MDA; Dienes; Clements&Sarama learningtrajectories.org; Clark/Tanner-Smith 2016; Wouters 2013; Mayer 2014; Shute stealth assessment; NN/g UX for children. URLs completas no histórico da sessão 2026-07-20.
