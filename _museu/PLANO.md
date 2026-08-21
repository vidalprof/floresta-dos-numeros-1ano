# Museu Vivo dos Bichos — 3º ano Ciências (plano vivo)

Mascote: **Professor Tato** (tatu naturalista). Prefixo: `mv`. Tema: museu vivo.
Estilo: vidro + barra top premium (motor do esqueleto). Bem visual e sonoro.

## Conteúdo (BNCC 3º ano — Vida e evolução)
Características e grupos de animais. **Vertebrados** (têm coluna/esqueleto interno)
× **invertebrados** (não têm). Grupos de vertebrados: mamíferos, aves, répteis,
anfíbios, peixes. Invertebrados: insetos, aracnídeos, moluscos, crustáceos.

## Lineup (decisão do Marcos, ago/2026) — 8 mecânicas, 32 fases
| # | mecânica | fases | papel |
|---|---|---|---|
| 1 | vitrine (passo-a-passo) | 4 | explica vertebrado×invertebrado e cada grupo, com imagem+explicação — OBRIGATÓRIA |
| 2 | raios-x | 4 | conceito central: tem coluna? → vertebrado / não → invertebrado |
| 3 | classificar | 4 | arrasta o bicho ao grupo — OBRIGATÓRIA |
| 4 | ligar | 6 | grupo × característica (penas→aves, pelos→mamíferos…) |
| 5 | quem-sou-eu | 6 | adivinha o grupo pelas pistas |
| 6 | intruso | 4 | qual bicho não pertence ao grupo |
| 7 | caca-palavras | 2 | nomes dos grupos |
| 8 | memoria | 2 | par animal ↔ grupo (cartas grandes) |

Aquecimento (revisão espaçada) entre 25% e 65% do caminho.

## Imagens — em CARTELA (Pollinations grátis + rembg; rodar `_qa/cartela.py` antes)
### ESTILO (decisão): REALISTA ILUSTRADO, não foto (Ciências = ver a característica real)
"ilustração realista e detalhada, estilo enciclopédia infantil moderna, <animal>,
corpo inteiro de perfil, proporções e cores REAIS, com penas/pelos/escamas/patas
visíveis, luz suave de estúdio, fundo branco liso, sem sombra dura, alta nitidez";
em grade numa folha (cartela) para gerar as peças irmãs de uma vez.
- Cartela 1 — Mamíferos (6): cachorro, gato, morcego, baleia, onça-pintada, macaco-prego
- Cartela 2 — Aves (6): tucano, arara-azul, coruja, pinguim, beija-flor, galinha
- Cartela 3 — Répteis (5): jacaré, jiboia, tartaruga, lagarto, camaleão
- Cartela 4 — Anfíbios (4): sapo-cururu, perereca, rã, salamandra
- Cartela 5 — Peixes (5): dourado, tubarão, cavalo-marinho, peixe-palhaço, arraia
- Cartela 6 — Invertebrados (8): borboleta, joaninha, abelha, aranha, caracol, minhoca, caranguejo, polvo
- Cartela 7 — Avatares (6): crianças naturalistas variadas, colete + luneta/caderno

Fora da cartela: `mv_fundo.jpg` (cena larga, Pollinations grátis) e o mascote
`mv_tato_feliz/_fala/_pisca` (3 camadas editadas da mesma base — Gemini).

## Padrão VISUAL (exigência do Marcos, ago/2026) — "bem lindo, coisa de primeira"
- **Barra de progresso premium** no topo (a do motor — viva e moderna).
- **Imagens em MOLDURA DE VIDRO**: centralizadas, **borda fina**, brilho/reflexo
  de vidro (glassmorphism), cantos arredondados suaves. A figura sempre CENTRADA
  na moldura (object-fit contain, object-position center — nunca cortada).
- Vale para toda tela com imagem (vitrine, classificar, raio-x, quem-sou-eu…).
- Conferir no CSS da atividade após montar; se o motor não trouxer a moldura de
  vidro por padrão, acrescentar a classe .moldura/.vidro e medir contraste.

## Como o Marcos manda as imagens
Ele gera no ChatGPT e ENVIA os arquivos aqui no chat. Eu: rembg (transparente) →
corto as cartelas em peças (`_padrao/cartela.py cortar`) → `_museu/img/` → commit.

## Publicação
Repo novo pela `fabrica.yml` → https://vidalprof.github.io/o-museu-vivo-dos-bichos/
Mostrar as telas montadas com os bichos ao Marcos ANTES de publicar.
