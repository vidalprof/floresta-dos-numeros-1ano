# 🌿 AMBIENTE VIVO — checklist de riqueza (pedidos do Marcos)

> Meta do Marcos: **"ambiente lindo e rico, vivo, de videogame de verdade".** Tudo mora
> no MOTOR (`kit-floresta.py`) → conserta 1x, vale pra TODO mundo que a fábrica gerar.
> Cada item vira código reutilizável (data-driven onde faz sentido) e passa pelo auditor.

## ✅ JÁ FEITO (no motor, AUDITADO — APROVADO)
- Byte VIVO: anda 4 direções + **sentar / deitar (dormindo, Zzz + roncar) / falar / feliz** (poses)
  + **micro-balanço quando parado** (respira/oscila leve).
- **Fogueira** viva (fogo em camadas + luz + fumaça + faíscas + crepitar + colisão).
- **Casa/cabana com chaminé fumegando** (prop) + **lampião** aceso (prop, chama + halo).
- **Ciclo dia/noite** (cena escurece, lua + estrelas; fogueira/lampião brilham mais à noite).
- **Caminho que FUNDE na paisagem** (borda dissolvida + tufos de grama na borda, com vento).
- Vento (rajadas: sway de árvores/flores + áudio), folhas caindo, borboletas, pássaros,
  pólen/luz, som ambiente em camadas (vento/folhas/grilos), coruja, voz gerada (mp3).
- **[mundo-vivo v2 — equipe de especialistas → integração auditada, jul/2026]:**
  - 🗨️ **Balões de conversa estilo VIDEOGAME (RPG):** caixa com **placa de nome**, texto
    **letra a letra** (typewriter), **setinha ▼** piscando, **avança no toque/clique**;
    sai acima da cabeça e **nunca cobre o rosto** (cai pra baixo perto do topo). A caixa
    fica acima de **QUEM fala** (Byte ou NPC), com a cor da placa própria de cada um.
    Data: `MUNDO.dialogo.cps` (velocidade; default 34).
  - 🌓 **Sombra direcional:** a sombra de todos (Byte, árvores, props, chave) muda de
    **lado/comprimento/opacidade** conforme o sol/lua do ciclo dia/noite; azulada à noite.
    Liga por padrão; desliga com `MUNDO.sombraDir:false`.
  - 💨 **Poeirinha ao andar:** partículas de terra nos pés a cada passada (mais na rajada).
    Data: `MUNDO.poeira:true` (+ `MUNDO.poeiraCor`). Lib de micro-movimento (`breathe/sway/blink`).
  - ☁️ **Nuvens passando:** sombras de nuvem cruzando o chão devagar + nuvens claras no céu;
    somem à noite. Data: `MUNDO.nuvens` (default ligado leve; `false` desliga; N = quantidade).
  - 🌧️ **Clima data-driven:** `MUNDO.clima` = `""|"chuva"|"neve"|"tempestade"`.
    Chuva (riscos na diagonal + splash), **tempestade** (chuva + **flash** + **trovão** grave
    via Web Audio), **neve** (reusa os flocos), **vento visível** (linhas na rajada forte).
    `MUNDO.climaForca` (intensidade), `MUNDO.climaMolha` (brilho de chão molhado).
  - 🐾 **NPCs VIVOS que INTERAGEM:** `MUNDO.npcs=[{sprite,x,y,rota,fala,nome,...}]`.
    Patrulham a rota (andar→pausa→próximo) ou ficam com micro-movimento; quando o Byte
    chega perto, **viram-se pra ele, acenam e abrem o balão RPG** (cooldown). Entram no
    y-sort com sombra direcional. Default `[]` (mundo sem npcs fica igual).

## 🔨 FILA (código, sem asset novo)
- [ ] **Boca ao falar** — o Byte já troca p/ pose `fala` no typewriter; afinar squash/ritmo.
- [ ] **Barulho das folhas** — camada já existe; subir mais forte na rajada.
- [ ] **Porta que range e bate** — prop `porta` (rangido pitch-bend + batida grave). Precisa
      do prop na cena (casa com porta / navio).
- [ ] **Som das tábuas ao andar** — passo "toc" de madeira sobre convés/tábuas (piso `tabuas`).

## 🌊 PRECISA DE MUNDO COM ÁGUA (tema navio/lago/praia)
- [ ] **Ondas na água** (tile de água viva — trazer do protótipo do navio pro motor).
- [ ] **Peixes pulando** (partícula-peixe que salta + splash + som).

## 🔊 PRECISA DE WORKFLOW DE SONS (clipes CC0 baixados por workflow, não pelo chat)
- [ ] **Sons de animais realistas** (miado, pássaros de verdade, lenhador) — `baixar-sons.yml`
      (a montar, igual `gerar-imagens.yml`): baixa mp3 **CC0/livre**, embute em base64.
      Regra séria: só CC0 (é produto de escola). SFX de ambiente/ação continua Web Audio (grátis).

## Como o QA prova cada item
`node --check` no JS extraído + auditor `runner.py` (render/mecânica/mundo_vivo) + screenshot
headless (Chromium do projeto) com **driver contínuo** (setInterval) — sob virtual-time o rAF
sozinho quase não acumula tempo, então efeitos temporais (balão/typewriter) exigem o driver
na foto (no navegador real, a 60fps, roda normal). Cada item estrutural vira uma checagem nova.
