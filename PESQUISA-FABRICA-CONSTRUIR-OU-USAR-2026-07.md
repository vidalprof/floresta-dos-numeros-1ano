# 🏭 Pesquisa: existe uma "Fábrica de Aventuras" pronta? (construir vs. usar) — jul/2026

> Pergunta do Marcos: "Tem alguma ferramenta que já faça o papel da Fábrica, pra eu não precisar
> construir? Pesquise amplamente." Foram avaliados ~40 candidatos contra 6 restrições duras.

## Restrições duras (critérios) — inegociáveis
Grátis (sem custo por professor/aluno) · roda em PC MUITO fraco por link no navegador · o PROFESSOR
gera · conteúdo BNCC anti-"prova disfarçada" · RPG jogável (não quiz) · sem lock-in (dados/jogo nossos).

## VEREDITO: NÃO existe pronto. Continuar CONSTRUINDO é o certo.
O mercado se divide em dois lados, e **nenhum** atende as 6 ao mesmo tempo:
- **Gera RPG por IA** (Rosebud, Ludo.ai, Astrocade, Google Genie): **pago por créditos**, **zero
  pedagogia BNCC**, **lock-in** (o jogo fica preso na plataforma deles), e pesado p/ PC fraco.
- **Grátis + BNCC** (MagicSchool, Diffit, Curipod, e as brasileiras planejamentosdeaula/atividade.digital):
  só geram **texto/plano/quiz**, **nunca RPG jogável**.
- **RPG educativo de verdade** (Prodigy, Legends of Learning, Classcraft): **conteúdo fixo fechado**,
  padrões dos EUA, o professor **escolhe** (não gera); Prodigy ainda é "pay-to-win" (queixa na FTC).

A interseção exata — "professor gera RPG BNCC jogável, grátis, leve, sem lock-in, anti-prova" — está
**VAZIA no mercado**. Não estamos reinventando a roda; estamos fazendo o que ninguém entrega.

## Candidato mais próximo (e por que reprova)
**Rosebud AI** — texto→RPG no navegador (usa Phaser), link compartilhável. Reprova em: **grátis**
(créditos que esgotam ~20/semana; planos ~US$10/mês), **BNCC/anti-quiz** (nenhuma; fica no prompt),
**lock-in** (não exporta projeto — tudo preso na plataforma), e trava em PC fraco. Serve de inspiração, não de substituto.

## Componentes que valem a pena (acelerar SEM entregar o núcleo)
- **Motor:** seguir no **Phaser 3** (grátis, open-source, roda onde Rosebud/Godot/Genie engasgam, zero lock-in, controle total). Trocar por Godot/GDevelop = retrabalho sem ganho.
- **História/diálogos:** um **LLM grátis por prompt ancorado na BNCC** (o que já usamos noutras partes) — "professor descreve → IA compõe", mas **sob nosso controle**, não terceirizado.
- **Mapas:** **Tiled** (open-source, nativo no Phaser) — já adotado.
- **Inspiração de narrativa:** **Twine** (nós de história em HTML leve) como ideia p/ o sistema de missões — sem adotar o produto.
- **NÃO** adotar Rosebud/Ludo/Astrocade nem como componente: lock-in + custo por geração = exatamente o que não podemos ter.

## Benchmark de filosofia (não é jogo, mas confirma o modelo)
**PlayLab.ai** — nonprofit, 100% grátis, professor cria apps de IA por linguagem natural, remixável.
Prova que "grátis + professor gera + remixável" funciona. Mas os apps são **chat**, não RPG — não substitui.

## Conclusão em 1 frase
A Fábrica que imaginamos **não existe pronta**; o mercado é "gera jogo mas caro/preso/sem pedagogia"
OU "grátis/BNCC mas só texto/quiz". **Construir sobre Phaser, com a pedagogia BNCC como núcleo
próprio**, é a decisão correta — usando componentes livres (LLM p/ roteiro, Tiled p/ mapas) para
acelerar, sem entregar o núcleo, o custo ou o lock-in a terceiros.

## Links
Rosebud https://rosebud.ai · limites https://www.summerengine.com/blog/rosebud-ai-free-tier-limits ·
Ludo https://ludo.ai/features/playable-generator · Astrocade https://www.astrocade.com/create ·
Genie https://deepmind.google/models/genie/ · GDevelop https://gdevelop.io/ · Prodigy https://www.prodigygame.com/ +
crítica https://fairplayforkids.org/pf/prodigy/ · Legends https://www.legendsoflearning.com/ ·
PlayLab https://www.playlab.ai/ · Phaser https://phaser.io/ · Twine https://twinery.org/ ·
BR: https://planejamentosdeaula.com/gerador-de-jogos-educativos-com-ia/ · https://atividade.digital/
