# 🗺️ PLANO BEAT-A-BEAT — Planeta Vivo (6º ano, clima/biomas) — 2026-07-22

> Junta as duas pesquisas: `PESQUISA-GEOGRAFIA-MECANICAS-6ANO-2026-07.md` (o QUE ensina) +
> `PESQUISA-ARSENAL-TECNICO-2026-07.md` (COMO executar leve). É o plano que o Marcos aprova
> ANTES de eu construir os ~11 beats. Segue o `MOLDE-ATIVIDADE-PREMIUM.md` (§4⅗/§4⅘/§6).

## Regras que atravessam TODOS os beats (das pesquisas)
1. **Andaime obrigatório** (geografia, achado 2): cada beat = **pergunta orientadora → manipular
   (produção) → o mundo reage (feedback) → FECHO que nomeia o conceito**. Como não há professor ao
   lado, a **Nara faz esse papel** (pergunta, checa, corrige) — tem que ser forte.
2. **Coerência / anti-"detalhe sedutor"** (geografia, achado 6/7): arte premium **sim**, mas **cada
   animação ENSINA** (mostra a causa-efeito), **curta e com zoom/destaque** no que muda. Nada decorativo.
3. **Jogo, não formulário** (molde §4⅗): manipular direto no mundo + reação visual + missão.
4. **Simulação real** = modelo por trás + **Canvas 2D** (arsenal: Canvas basta; WebGL é exagero).
5. **Toque** (arsenal): alvos **≥ 2 cm**; **tocar/deslizar > arrastar**. No 6º ano arrastar ok com alvo
   grande; ao adaptar p/ turmas menores, trocar arrastar por tocar.
6. **Mascote**: upgrade de **lip-sync por visemas** (ver "transversais") + toda pose de gesto volta à neutra.

## Os beats (~11, ~55 min, com revisão espaçada)

| # | Beat / Conceito (BNCC) | Mecânica (evidência) | Simulação/Modelo + Visual funcional | Andaime (Nara) |
|---|---|---|---|---|
| 0 | **Abertura** (missão) | cutscene curta | o planeta "apagado" fica cinza; ela convida | pergunta-gancho |
| 1 | **Latitude→temperatura** ✅já feito, refinar | tocar faixa + **1 gesto/conceito** | Sol inclina → faixas mudam; **zoom** no raio concentrado×espalhado | beat concreto→exemplo→✓ |
| 2 | **Por que o Sol esquenta o meio** | **mini-cutscene** sinalizada | animação curta: raios batendo reto×de lado, destaque | "o que muda?" → fecho |
| 3 | **Tempo × clima** | comparar lado a lado + linha do tempo | semana (tempo) × padrão de anos (clima); destaque no padrão | pergunta → separa os dois |
| 4 | **Alívio: sons do planeta** | tocar/explorar | biomas cantam a nota (game feel) | livre, on-mission |
| 5 | **A LEI clima→bioma** (núcleo) | **simulação real** `bioma(temp,chuva)` | girar 2 diais → o **bioma nasce** no mapa; comparar mapa↔foto | prevê→gira→vê→nomeia |
| 6 | **Construir o CLIMOGRAMA** (achado 3) | **construir a representação** | tocar p/ subir barras de chuva + traçar linha de temp.; **repete 2–3×** c/ feedback | modelo→faz→confere |
| 7 | **Altitude/relevo** (a pegadinha) | deslizar (subir a montanha) + **perfil** | sobe altitude → esfria/neva no topo; **corte transversal** revela | "por quê?" → altitude |
| 8 | **Chuva orográfica** | simulação causa-efeito | massa de ar bate na serra → chove de um lado, resseca do outro | prevê→testa→fecho |
| 9 | **Mapa em CAMADAS** (achado 4) | **toggle de camadas / comparar** | ligar/desligar temperatura, chuva, bioma no MESMO mapa; comparar regiões | correspondência mapa↔real |
| 10 | **Ser humano–natureza** | geo-indagação / mistério | pistas no mapa → "por que vivem aqui?"; consequência | investiga→conclui |
| 11 | **Autoria + Desafio + Deleite** ✅base feita | criar + protégé + pintar | cria a região; a Nara adivinha; pinta livre | transferência |
| — | **Final** + parecer | cutscene | planeta reacende; medição→parecer (só professor) | — |

**Revisão espaçada:** o climograma (6) e a LEI (5) voltam como **Aquecimento** nas sessões seguintes
(motor Leitner já existe). Cada beat mede 1 KC (stealth).

## Upgrades TRANSVERSAIS (valem para toda a atividade)
- **Mascote — lip-sync por visemas (o "parecer real"):** gerar **6 formas de boca** (base + 5 visemas,
  técnica base+elipse) e **pré-computar o tempo com Rhubarb no workflow** (a partir do mp3), embutindo a
  "partitura" da boca. Troca de boca no tempo certo = fala natural. (Alternativa: `lipsync-engine` 15KB inline.)
- **Simulação:** um `<canvas>` leve por beat que precisa (partículas de chuva/neve/calor, raios, massa de
  ar) — Canvas 2D, resolução modesta, `requestAnimationFrame` com teto de fps em PC fraco.
- **Som:** notas diegéticas (já existe) + trilha leve gerada.
- **Acessibilidade:** alvos ≥2cm, "Ouvir de novo", contraste, `prefers-reduced-motion`.

## Ordem de construção que proponho
1. **Upgrade do mascote (visemas)** — resolve de vez o "falar certinho" (o que o Marcos mais cobra).
2. **Beat 5 (LEI clima→bioma) como simulação de verdade** — é o núcleo e o mais "uau".
3. **Beat 6 (climograma)** e **Beat 9 (camadas)** — os de maior evidência.
4. Preencher os demais (2, 3, 7, 8, 10) reaproveitando os padrões.
5. QA 3 níveis + duração + publicar + prévia ao Marcos a cada bloco.

> **Decisão do Marcos pendente:** aprovar este arco de ~11 beats e a ordem de construção. Ao "GO",
> começo pelo upgrade do mascote (visemas) e pela LEI clima→bioma como simulação.
