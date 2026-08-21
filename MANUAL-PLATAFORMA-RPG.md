# 📕 MANUAL DA PLATAFORMA RPG — estado vivo + como continuar (para QUALQUER modelo)

> Ordem do Marcos (jul/2026): "deixe tudo documentado, para que qualquer modelo consiga
> seguir depois". Este arquivo é o mapa completo. Leia junto com `ARQUITETURA-PLATAFORMA-RPG.md`
> (o projeto) e `MEMORIA-DO-PROJETO.md` (a história). Regra de ouro: NADA chega ao Marcos sem
> passar pelo robô-QA E pelos olhos (screenshot) — e todo bug corrigido VIRA TESTE permanente.

## 1. O que é

"RPG Educativo IA": professor informa ano·disciplina·objetivo·tema·tempo·dificuldade →
GERAR → RPG top-down completo. IA gera SÓ conteúdo pedagógico; gráficos = asset pack
(SEM IA desenhando). Decisões do Marcos: pack CC0 estilo **Ninja Adventure** (pixel-boy),
**SEM tema ninja** nos jogos (elenco neutro: aldeões/crianças/velhinhos/animais), Kenney de
reserva; LLM no *authoring* (professor tem internet), jogo estático offline pro aluno;
**jogo/mundo primeiro, pedagogia pluga depois** (missões do catálogo — nunca quiz).

## 2. Mapa de arquivos (onde mora cada coisa)

```
educaverso-app/                  # app Phaser 3.80 + TS + Vite (strict, 0 erros)
  src/rpg/VilaViva.ts            # CENA-PROVA do motor (a "Vila Viva" publicada)
  src/rpg/UIVila.ts              # botões fixos: tela cheia + ver-tudo (cena própria)
  src/gerador/tipos.ts           # BriefingProfessor, PlanoMissao, MecanicaPedagogica
  src/gerador/catalogo-pedagogico.ts  # objetivo→missão jogável (TRAVA Portão 0)
  src/motor/mecanicas/registro-ids.ts # "lista da verdade" das mecânicas jogáveis
  src/motor/{Mundo,aventura,auditor,Personagem}.ts  # motor v2.1 (mundos ilustrados)
  public/rpg/*.png               # assets staged do demo (ver §4)
  tools/qa-vila.mjs              # robô-QA da vila (33 checks) — SEMPRE rodar antes de publicar
  tools/qa-vila-iphone.mjs       # robô em viewport iPhone com TOQUE real (3 checks)
  tools/qa-gerador.mjs           # robô do cérebro pedagógico (10 checks)
  QA-APRENDIDOS.md               # CADA lição de bug → regra (ler antes de mexer!)
content/assets/
  ninja-adventure/               # subconjunto do repo Godot do autor (tilesets, 4 chars)
  ninja-adventure/referencia/    # ⭐ vila OFICIAL do autor decodificada + COMO-LER.md
  ninja-adventure-full/          # pack completo (26 chars + monstros + itens + fx + hud)
  kenney/                        # reserva (tiny-town, tiny-dungeon, roguelike-characters)
ARQUITETURA-PLATAFORMA-RPG.md    # arquitetura completa (camadas, roadmap F1-F5)
MANUAL-PLATAFORMA-RPG.md         # ESTE arquivo
```

## 3. A Vila Viva (prova pública do motor) — https://vidalprof.github.io/vila-viva/

Estado v6: herói (char 25) tap-to-move + TECLADO (setas/WASD), caminhada 4 direções frame a
frame; NPCs neutros com corpo (não atravessa) que OLHAM pro herói; dog passeando; colisão
pelos pés (passa atrás das casas); depth por Y; sombras; 2 casinhas ENTRÁVEIS ("igual no
jogo": vão físico na porta + gatilho na soleira; cruzar na frente NÃO entra); interiores
tema-combinando (palha rústica / depósito de pedra) montados em cantos afastados do mapa
(técnica validada pelo próprio autor); FIT (quadro inteiro, sem cortar cantos); botões tela
cheia + ver-tudo; sem tremor (NUNCA tween de escala em pixel art).

## 4. Coordenadas AUDITADAS dos assets (não re-descobrir!)

`public/rpg/chao.png` = tileset_floor.png (352×417, tiles 16px, **22 colunas**; índice
global = linha*22+coluna). Bloco VERDE começa na linha 7: grama lisa=245 (=G(3,4));
blob de terra orgânico 3×3 = cols 0-2 × lins 0-2 do bloco verde.
`public/rpg/mundo.png` = tileset de background (448×640). Props (x,y,w,h):
casa_a(0,0,64,48) casa_b(64,0,64,48) torii(7,51,34,29) cerca(85,71,39,22)
varal(128,73,32,21) pedras(225,147,61,44) toco(97,293,30,23) arvore(0,160,32,32)
carroca(82,131,27,27) feira(116,130,27,28) lago-prefab(288,104,96,72; borda de areia)
estante(160,592,37,32) prateleira(200,592,37,31) tapete(112,592,48,48) planta(0,600,15,24).
Personagens 64×112 = 4 colunas (direção: 0=frente 1=costas 2=esq 3=dir) × 7 linhas
(passos 0-3 + extras); frame Phaser = linha*4+coluna. Elenco NEUTRO liberado do full:
2,3,4,5(fazendeiro),6,9(avô),10,11,12,13,14,16,17(menina),19,20,22,25(herói)+dog.
BANIDOS de jogo infantil: 1,7,8,15,18,23,24 (ninjas/cavaleiros/caveira).
`items/`: big-treasure-chest(32×14=2 frames fechado/aberto), jar(32×16=2 frames), chaves,
moedas, corações, pergaminhos — prontos p/ missões.

## 5. A gramática do autor (referência de composição — ver referencia/COMO-LER.md)

Caminhos de terra ORGÂNICOS serpenteando/ramificando (a espinha do mapa); portas DAS casas
NO caminho; árvores em CACHOS de 2-4 copas sobrepostas (nunca solitárias espalhadas);
poço/estátua em entroncamentos; interior em canto afastado do mesmo mapa.

## 6. Pipeline de publicação do demo (provado 6×)

1. `cd educaverso-app && node_modules/.bin/tsc --noEmit && node_modules/.bin/vite build`
2. QA SEMPRE: servir `dist` (`python3 -m http.server PORTA -d dist`) →
   `URL='http://127.0.0.1:PORTA/index.html?rpg' node tools/qa-vila.mjs` (33/33) +
   `qa-vila-iphone.mjs` no PACOTE final (3/3). Olhar screenshots em /tmp (Portão de Arte!).
3. Pacote: dist/{index.html,assets,rpg} → /tmp/vila_pub + BLINDAGEM no index (script
   __BOOT='rpg' + caixa de erro vermelha + CSS display:none na UI legada) — ver
   MEMORIA "Vila Viva v2/v3".
4. `_novo` na MAIN via worktree (`git worktree add --detach /tmp/wt origin/main`) →
   commit/push → `actions_run_trigger` `atualizar.yml` (ref=main, repo_name=vila-viva) →
   conferir push `main -> main` no log → link com `?v=N` NOVO (cache).

## 7. Leis do Marcos (inegociáveis)

- Perfeito e profissional; bug corrigido NÃO volta (→ teste permanente no robô).
- Entregas = LINK publicado (ele só vê publicado). Sempre `?v=N` novo.
- Interior combina com o tema; mesmo pack = ok, sem forçar perfeccionismo.
- Porta entra SÓ pisando na soleira. Teclado E toque. Quadro inteiro visível (FIT).
- Sem emoji/texto visível pra criança pequena (ícones desenhados).
- Elenco neutro (sem armas/ninja). Tudo documentado.

## 8. Próximos passos (ordem)

1. **v7 "Vila do Autor"**: recompor a vila com a gramática do §5 (caminho orgânico
   ramificado, cachos de árvores, lago) — auditoria de tiles em andamento (workflow
   auditoria-tiles-vila-autor; resultados → aplicar em VilaViva).
2. **Tilemap Tiled + vagas nomeadas** (motor lê .tmx/JSON do Tiled; o gerador emitirá isso).
3. **Gerador de mapa** (PlanoMissao → mapa na gramática do autor, determinístico+testável).
4. **Diálogo com faceset** (caixa estilo RPG do mockup; LLM no authoring) + missões do
   catálogo (colher/entregar — itens do pack) + relatório → Firebase.
