# 🌿 AMBIENTE VIVO — checklist de riqueza (pedidos do Marcos)

> Meta do Marcos: **"ambiente lindo e rico, vivo, de videogame de verdade".** Tudo mora
> no MOTOR (`kit-floresta.py`) → conserta 1x, vale pra TODO mundo. Cada item vira código
> reutilizável (data-driven onde faz sentido) e passa pelo auditor.

## ✅ JÁ FEITO (no motor, APROVADO)
- Byte VIVO: anda 4 direções + **sentar / deitar (dormindo, Zzz + roncar) / falar / feliz** (poses).
- **Fogueira** viva (fogo em camadas + luz + fumaça + faíscas + crepitar + colisão).
- **Casa/cabana com chaminé fumegando** (prop) + **lampião** aceso (prop, chama + halo).
- **Ciclo dia/noite** (cena escurece, lua + estrelas; fogueira/lampião brilham mais à noite).
- **Caminho que FUNDE na paisagem** (borda dissolvida + tufos de grama na borda, com vento).
- Vento (rajadas: sway de árvores/flores + áudio), folhas caindo, borboletas, pássaros,
  pólen/luz, som ambiente em camadas (vento/folhas/grilos), coruja, voz gerada (mp3).

## 🔨 FAÇO EM CÓDIGO (Web Audio + Canvas, sem asset novo) — fila
- [ ] **Poeirinha ao andar** — partículas de poeira nos pés quando o Byte se move.
- [ ] **Nuvens passando no céu** — sombras de nuvem cruzando o chão devagar.
- [ ] **Sombra direcional** — a sombra do personagem/objeto muda de lado/tamanho conforme a
      posição do sol/lua (do ciclo dia/noite).
- [ ] **Chuva + trovão** — gotas/riscos caindo + flash + estrondo (Web Audio); molha o chão.
- [ ] **Neve** — flocos caindo (o tema `inverno` já tem o modo `part:"neve"`; ligar como clima).
- [ ] **Vento visível** — rajadas mais fortes (linhas de vento/folhas voando na rajada).
- [ ] **Boca ao falar** — o Byte troca p/ pose `fala` + squash no ritmo (JÁ existe; reforçar/afinar).
- [ ] **Barulho das folhas** — camada de folhas farfalhando (JÁ existe; subir na rajada).
- [ ] **Porta que range e bate** — som de rangido (pitch-bend) + batida grave, no prop porta/casa.
- [ ] **Som das tábuas ao andar** — passo com "toc" de madeira quando o Byte anda sobre convés/tábuas.
- [ ] **Balões de conversa estilo VIDEOGAME** — caixa de diálogo RPG com o **nome do personagem**,
      texto que aparece letrinha a letra (typewriter), setinha "▼" e **avança no toque/clique**;
      balão sai do personagem e nunca cobre o rosto (âncora acima da cabeça, y-sort).
- [ ] **Personagens VIVOS que INTERAGEM** — NPCs com **rotina** (andam, sentam, trabalham),
      **conversam entre si e com o Byte**, reagem à presença dele (viram, acenam, dão a missão).
- [ ] **Micro-movimentos reais e leves** em TODOS (respira, pisca, balança suave, mão/pé com peso,
      boca ao falar) — "vida" por código (senoidal/easing), nunca boneco estático. É a regra geral
      que faz "parecer um mundo vivo".

## 🌊 PRECISA DE MUNDO COM ÁGUA (não tem na floresta; vale pro tema navio/lago/praia)
- [ ] **Ondas na água** (o tema navio já tinha espuma/ondulação — trazer pro motor como tile água viva).
- [ ] **Peixes pulando** na água (partícula-peixe que salta e faz splash + som).

## 🔊 PRECISA DE WORKFLOW DE SONS (clipes CC0 baixados por workflow, não pelo chat)
- [ ] **Sons de animais realistas** (miado, pássaros de verdade, lenhador) — `baixar-sons.yml`
      (a montar, igual `gerar-imagens.yml`): baixa mp3 **CC0/livre**, embute em base64.
      Regra séria: só CC0 (é produto de escola). SFX de ambiente/ação continua Web Audio (grátis).

## Regra
Cada item que sai → marcar aqui + virar checagem no auditor quando for estrutural
(ex.: "tem partícula de poeira ao mover", "chuva molha o chão"). O auditor só pega o que TESTA.
