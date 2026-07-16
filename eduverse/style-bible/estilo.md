# 🎨 BÍBLIA DE ESTILO DO EDUCAVERSO (a barra visual — cobrança do Marcos)

> **Regra de ouro:** 2D em **tile** é só a TÉCNICA. O **visual** tem que ser **tão lindo
> quanto o que a gente já produzia antes** (as atividades premium) — não "gráfico de tile
> sem graça". Bonito, rico, **realista no capricho** (luz/sombra/profundidade), pintado à mão.

## O que "lindo e realista" significa aqui
- **Arte pintada à mão premium** (gerada por IA), coesa — **um estilo só** em tudo
  (chão, objetos, personagens). Nada de peça "de outro jogo".
- **Profundidade e volume:** sombras de contato, luz suave, gradientes, oclusão nos cantos —
  o mundo tem "corpo", não é chapado.
- **Realista = caprichado/atmosférico** (não é foto): mantém a cara **storybook/cartoon
  premium** que o Marcos aprovou, só que **rico** em luz, cor e detalhe.

## Efeitos de mundo VIVO (obrigatórios — como nas premium de antes)
Luz do sol deslizando · raios/atmosfera · **vento em rajadas** (árvores/flores/grama balançam) ·
folhas/pétalas/poeira de luz caindo · **água brilhando e ondulando** · fumaça · faíscas ·
sombras que se mexem · **ciclo dia/noite e clima** (chuva, névoa) · bichos (pássaros, borboletas).

## Personagens — CARTELA DE ANIMAÇÃO PADRÃO (todos os personagens têm que ser VIVOS)
Estados obrigatórios (reusados em todas as atividades):
- **respira** no parado (idle) · **pisca** os olhos de vez em quando
- **caminha suave** e natural (4 direções: frente/costas/lados) — passo com peso, sem "patinar"
- **mexe a boca ao falar** (fala = boca animada + leve balanço)
- **senta** · **deita** · **feliz/comemora** · **pensando** · **triste** · **esperando**
- ações suaves de mãos/pernas (ex.: **entregar a chave**: braço estende, entrega, recolhe)

**Como fazer (técnica):** **cartela de poses gerada por IA** (editando a imagem-âncora do
personagem → mesma "cara", trocando a pose: sentado, deitado, andando, falando, feliz…),
**normalizando os pés na mesma base** (não "pula" ao trocar), + **micro-vida por código**
(respiração senoidal, bob do passo, squash da boca, piscar). Nada de boneco estático.

- **Temáticos:** o Byte e os personagens **vestem o tema** do mundo (pirata, viking…),
  sempre gerados **editando a imagem-âncora** (mesmo personagem, só a fantasia + a pose).

## Técnica (para ficar lindo E leve/compatível)
- Assets IA com **recorte limpo** (transparência de verdade), otimizados (~50KB mascote).
- Tiles via `createPattern`; sprites ancorados nos pés, dimensionados pela **altura**; **y-sort**.
- Canvas 2D, offline, compatível (Win7/Chrome antigo). Efeitos leves com fallback (`lowfx`).

## Quem cobra
- **Diretor de Arte** especifica e aprova (estilo/tema/recorte).
- **Auditor de Arte** (automático): tudo IA no estilo, **mundo vivo** (anima), sem sobreposição.
- **Portão 3 (Marcos):** o "ficou lindo?" final. Referência = **as atividades premium de antes**.

## Ambientes RICOS (chamam a atenção do estudante) — cobrança do Marcos
- Cada cena com **sons + movimentos + animações** — igual o **lampião da Taberna** (chama
  tremeluzindo + luz oscilando), fumaça subindo, água correndo, folhas, bichos, poeira de luz.
- **Sol e lua com efeito** (brilho, raios, halo) · **ciclo dia/noite** (a cena escurece e clareia)
  · **clima** (chuva, névoa). Tudo **natural e sonoro** — o mundo respira e faz barulho.
- **Objetos com vida própria:** máquinas girando, esteiras levando caixas, portas, trem passando,
  NPCs em rotina (andar, trabalhar, sentar, conversar).
- **Regra dura:** se uma tela fica **parada e muda**, NÃO está pronta (o auditor de Arte reprova
  "mundo_vivo"; o de Som exige ambiente sonoro).

## Personalização — o mascote fala o NOME do estudante (quando ligarmos nome + salvar)
- O mascote/Byte **sempre fala e se refere ao NOME do estudante** ("Muito bem, João!") — na
  narração e nos diálogos. Entra com o **login simples (código de turma + nome) + salvar
  progresso** (a aventura o ano inteiro, vira avaliação descritiva). Já no roteiro; a arte e a
  voz (falas com o nome interpolado) devem prever isso desde já.
