# Templates de Capa (telas de abertura) — biblioteca reutilizável

Protótipos de **tela de capa/abertura** premium para atividades gamificadas.
Cada arquivo é um HTML **autossuficiente** (SVG/CSS inline, sem recurso externo) e
já dentro da **Compatibilidade Sagrada** (sem grid/gap/clamp/var(); flex com
`-webkit-box`; prefixos `-webkit-`/`-o-`; emojis ≤ Unicode 6.0; fontes de sistema).

Servem de **ponto de partida visual**: ao criar/reformar uma atividade, escolhe-se
um tema, copia-se a estrutura da capa (selo → título → mascote → história → campo do
nome → botão → prévia da trilha com 3 paradas) e liga-se às funções reais do jogo
(`campoNome`, `comecarComNome()`, continuar/`telaMenu()`, "Ouvir o guia").

## Temas disponíveis

| Arquivo | Tema | Matéria / faixa ideal |
|---|---|---|
| `atlas-expedicao.html` | Atlas de papel envelhecido, furos de fichário, foto com fita, selo de cera, rosa dos ventos | Geografia, Ciências, História · 4º–9º |
| `grimorio-encantado.html` | Livro iluminado, moldura dourada, vitral, capitular | Leitura, Português, Alfabetização · 2º–6º |
| `numeros-arcade.html` | Fliperama neon, tela CRT, gabinete cromado, robô | Matemática (cálculo rápido) · 3º–9º |
| `mundo-massinha.html` | Diorama fofo de massinha, sol sorridente, bichinho | Pré-escola ao 2º ano |

> Aplicado de verdade: a pele **Atlas de Expedição** foi usada na capa do
> `climas-do-mundo-6ano`.

## Regras ao reaproveitar
- Trocar textos/mascote/nomes das paradas conforme a atividade (a ordem e a
  hierarquia visual são o que importa).
- Manter o campo do nome, o botão de começar e a lógica de **Continuar** (reset de
  aula por carimbo deslizante — ver MANUAL-MESTRE).
- Rodar o auditor de compatibilidade e uma renderização headless antes de fechar.
