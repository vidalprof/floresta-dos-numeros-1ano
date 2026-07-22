# 🛠️ PESQUISA — Arsenal técnico para elevar as atividades (web leve, offline, PC fraco) — 2026-07-22

> Pesquisa profunda (deep-research, **síntese COMPLETA** na 2ª rodada). Todas as recomendações
> respeitam o stack: 1 HTML autossuficiente, ES5, offline/PWA, sem CDN em runtime, Chrome ~109, custo ~zero.
> **Princípio-mestre:** mover o trabalho CARO para o **BUILD (GitHub Actions)** e deixar o navegador só
> **REPRODUZIR dados prontos** (MP3 + JSON). Complementa `PESQUISA-GEOGRAFIA-MECANICAS-6ANO-2026-07.md`.

## ✅ ADOTAR JÁ

### 1. Lip-sync 2D por VISEMAS pré-computados (o salto do "falar de verdade") ⭐
- **Rhubarb Lip Sync** (CLI offline, roda no Actions) analisa o áudio e gera a **timeline das bocas**
  (6 básicas A–F + G/H/X opcionais = 6–9 visemas). Usa reconhecedor **FONÉTICO independente de idioma**
  → **funciona em português** (o modo que "entende inglês" NÃO serve; o fonético sim). Saída **JSON**
  (tempo→boca) que **embutimos no HTML**; no navegador é só trocar a imagem da boca por transform/opacity,
  **zero dependência em runtime**. (github.com/DanielSWolf/rhubarb-lip-sync)
- **Pipeline (nota de engenharia):** edge-tts entrega **MP3**, mas o Rhubarb só aceita **WAV/OGG** → o
  workflow precisa **converter com ffmpeg** antes do lip-sync.
- **Ganho:** boca que **forma as sílabas** sincronizada com a narração — muito além dos 2 estados de hoje.
  Custo: gerar **6 imagens de boca** (base + elipse por viseme) + o passo Rhubarb no workflow.

### 2. Voz por edge-tts no build (já usamos; explorar mais)
- Vozes neurais Microsoft **grátis, sem chave**, 322 vozes/74 idiomas; **`--rate/--volume/--pitch`**
  mudam a prosódia → **vozes por idade/personagem** do mesmo motor. `--write-subtitles` dá **SRT com
  tempo por palavra** (útil para alinhar boca). Ressalva honesta: é acesso **não-oficial** (pode ser
  bloqueado um dia) e roda **no build** (online), nunca em runtime — como já fazemos. (rany2/edge-tts)

### 3. Game feel pelos 12 princípios (transform/opacity, leve)
- **Squash & stretch** (comprime no impacto, alonga no movimento) dá "realidade física"; **antecipação
  "comprimida"** (frame de agachamento no início do pulo **enquanto** o personagem já sai do chão) parece
  antecipada mas continua **instantânea/responsiva** — ideal para jogo (antecipação clássica atrasaria o
  input). Tudo com transform/opacity. (gamedeveloper.com — 12 Principles for Game Animation)

### 4. UX de toque para crianças (TIDRC, ACM IDC 2019)
- **Fonte mínima ~14 pt**; **alvos grandes** com **ÁREA ATIVA AMPLIADA** (aceitar toque um pouco fora da
  borda). Reforça: **tocar/deslizar > arrastar** nas turmas pequenas. (ResearchGate 333624343)

### 5. Desempenho por "adaptive loading"
- Enviar um **baseline leve** e **LIGAR efeitos caros só quando o hardware aguenta**, lendo
  **`navigator.deviceMemory` e `navigator.hardwareConcurrency`** (ambos no Chrome 109, sem rede). →
  partículas/animações extras só em quem aguenta; PC fraco recebe a versão enxuta. (addyosmani.com/blog/adaptive-loading)

### 6. Repetição espaçada no CLIENTE (sem servidor)
- **MEMORIZE** (agenda ótima de revisão) — alunos que seguiram retiveram melhor (dados Duolingo,
  experimento natural). Valida e sugere afinar nosso **Leitner**. (PMC6410796)

## 🧪 TESTAR
- **`lipsync-engine`** (runtime, ~15KB, zero-dep, Web Audio/AudioWorklet, visemas em tempo real **sem**
  forced alignment): pode dispensar o passo de build, MAS as métricas são **auto-declaradas** e exige
  **AudioWorklet** → **testar fps real em Chrome 109/PC fraco** antes de adotar. Aposto no **Rhubarb
  pré-computado** como caminho confiável. (github.com/Amoner/lipsync-engine)
- **Variante "Select" da repetição espaçada** — validada em **RCT real** de larga escala (superou
  baselines). Considerar ao afinar o motor. (npj Science of Learning 2021, PMC8421401)

## ⛔ EVITAR
- **Frameworks SPA, 3D/WebGL pesado, libs grandes, dependências online/CDN em runtime, IA cara** — custo
  de parse/execução e de rede mata o PC fraco/offline. Nosso 1 HTML enxuto é a escolha certa.
- **Não afirmar como "comprovado"** o que a verificação DERRUBOU: **secondary motion fluído** (follow-through
  de cabelo/tecido) e a **fórmula linear fechada do MEMORIZE**. Usar squash/stretch + antecipação comprimida,
  não prometer secondary motion.

## Lacunas — precisam de pesquisa DEDICADA (não saíram nem na 2ª rodada)
1. **Consistência de personagem entre cenas com IA grátis/barata** (seed/referência/img2img/LoRA leve,
   recorte transparente confiável, folhas de sprite) — foi o que nos custou o "corpo tremendo" da Nara.
2. **Renderização/simulação**: receita de quando trocar CSS→SVG→Canvas 2D→WebGL, e **partículas/autômatos/
   ruído procedural (Perlin/simplex) a 60 fps em Chrome 109 de PC fraco**.
3. **Medição stealth/adaptatividade leve** além da repetição espaçada (que sinais no localStorage; fechar
   o loop sem inflar o HTML).
→ Rodar uma pesquisa focada só nesses 3 pontos quando for mexer em arte-consistente e em simulações Canvas.
