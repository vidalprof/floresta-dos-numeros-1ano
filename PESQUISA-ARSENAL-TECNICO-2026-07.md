# 🛠️ PESQUISA — Arsenal técnico para elevar as atividades (web leve, offline, PC fraco) — 2026-07-22

> Pesquisa profunda (deep-research). **Nota honesta:** a **síntese final não fechou** (bateu limite
> de sessão, reseta ~4h UTC) — este doc é a **consolidação das 18 afirmações verificadas** (voto 3-0)
> que voltaram. As frentes de **consistência de personagem por IA** e **ruído procedural/upscaling**
> ficaram sem afirmação verificada nesta rodada → **re-rodar a síntese depois do reset** para completar.
> Todas as recomendações respeitam o stack: 1 HTML autossuficiente, ES5, offline/PWA, sem CDN, custo ~zero.

## ✅ ADOTAR JÁ

### 1. Lip-sync por VISEMAS pré-computados (o salto de "parecer real") ⭐
- **Rhubarb Lip Sync** analisa o mp3 e gera o **tempo das formas de boca** (6 básicas Ⓐ–Ⓕ + 3 extras),
  **offline por linha de comando** → dá para rodar **no GitHub Actions** junto com o `gerar-audio.yml`
  e **embutir a "partitura" da boca** no HTML. No navegador é só trocar a boca no tempo certo — **leve,
  sem depender de análise em tempo real**. (github.com/DanielSWolf/rhubarb-lip-sync)
- **Ganho concreto:** hoje a Nara tem 2 estados (aberta/fechada) por RMS; com **6 visemas** a boca
  "forma" as sílabas → **muito mais real** (o que o Marcos pede). Custa: gerar **6 imagens de boca**
  (mesma técnica base + elipse por viseme) + o passo do Rhubarb no workflow.
- **Alternativa em tempo real:** `lipsync-engine` (~15KB, **zero dependência**, Chrome 66+ cobre o 109,
  saída **paramétrica** open/width/round). Cabe inline. Ressalva: exige **AudioWorklet** (ok no Chrome
  da escola; Safari só 14.1+). Preferir o **pré-computado** (mais previsível em PC fraco).

### 2. UX de toque para crianças (regras firmes)
- **Alvos ≥ 2 cm × 2 cm** (4× o do adulto) — motor fino é imaturo. (NN/g)
- **Arrastar é DIFÍCIL para os pequenos; tocar alvo grande e deslizar é fácil para todos** → **preferir
  TOCAR/DESLIZAR a ARRASTAR**, sobretudo pré–5º. (NN/g) *(Impacto no plano de geografia: onde eu propus
  "arrastar", oferecer variante de **tocar** para as turmas menores; no 6º ano arrastar ok com alvo grande.)*
- **TIDRC** = 57 recomendações de UI de toque por faixa (cognitivo/físico/socioemocional) — usar como
  checklist de acessibilidade por idade. (ResearchGate 333624343)

### 3. Animação leve com "juice"
- **Squash & stretch preservando massa/volume** dá "punch" à animação — só com `transform`, cabe no
  nosso limite. (12 Principles for Game Animation) *(Já usamos em parte; padronizar.)*

### 4. Desempenho em PC fraco (regra de ouro)
- **Parse/execução de JS é 2–5× mais lento** em aparelho fraco; bundles grandes custam caro (ex.: 1,3 MB
  → 1,29 s só de parse num aparelho antigo). → **manter o HTML/JS enxuto**, sem framework, é o certo. (fasterize)
- **Canvas 2D** ganha em operações de pixel/memória; **WebGL** só compensa em carga gráfica pesada →
  para nossas partículas/simulações 2D, **Canvas 2D basta**; WebGL é exagero. (semisignal 2D vs WebGL)

### 5. Voz e revisão espaçada (confirmam o que já fazemos)
- **edge-tts**: voz neural **grátis, sem chave**, via Actions — é o que já usamos; e **`--write-subtitles`
  gera legenda com tempo** (SRT) junto do mp3 **num comando** → tempo utilizável para guiar a boca. (rany2/edge-tts)
- **Repetição espaçada com agenda ótima** (experimento Duolingo/MEMORIZE) memoriza melhor que heurística
  → valida nosso **Leitner** (e sugere afinar a agenda). (PMC6410796)

## 🧪 TESTAR
- **`lipsync-engine` em tempo real** vs. **Rhubarb pré-computado**: qual dá a boca mais natural na Nara
  em PC fraco (medir fps). Aposto no pré-computado, mas vale comparar.
- **Ruído procedural (Perlin/simplex) em Canvas** para cenas "vivas" (nuvens/água) — barato se em
  resolução baixa; **testar custo** em PC fraco (a evidência não fechou nesta rodada).
- **Consistência de personagem por IA** entre cenas (seed fixa, img2img/edição a partir da base, folha de
  poses) — nossa técnica atual (editar a base no Gemini + recorte local) funciona; **testar** seed/img2img
  para reduzir variação (foi o que nos custou o "corpo tremendo").

## ⛔ EVITAR (hype/pesado demais para o nosso alvo)
- **Frameworks SPA / libs grandes / 3D pesado (WebGL para tudo)** — custo de parse/execução mata o PC
  fraco; nosso 1 HTML enxuto é a escolha certa. (fasterize; 2D vs WebGL)
- **Dependência de CDN/nuvem em runtime** — quebra o offline; tudo tem que ser **inline**.
- **Arrastar/pinça/rotação como interação principal nas turmas pequenas** — difícil para o motor fino
  delas; preferir tocar/deslizar. (NN/g; TIDRC)
- **Lip-sync por análise pesada em tempo real** quando dá para **pré-computar** no workflow.

## Lacunas (re-rodar após reset das 4h UTC)
Síntese final e as frentes de **consistência de personagem** e **procedural/upscaling** ficaram
incompletas por limite de sessão. Re-rodar para fechar. O que já está aqui é suficiente para o plano
técnico do próximo passo (lip-sync por visemas + UX de toque + Canvas 2D para simulação).
