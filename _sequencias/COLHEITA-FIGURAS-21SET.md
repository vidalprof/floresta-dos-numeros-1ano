# 🔍 Colheita de figuras — 21/set/2026 (as borradas do `_ort5`, `_ort5b` e a faca)

> Ordem do Marcos: ***"corrija e publique"***, sobre a dívida das figuras que
> apareciam acima de 1,35× da própria resolução e saíam borradas.
> Regra que manda aqui (dele, 14/set/2026): ***"procure na internet, nada de
> imagem gerada por IA, utilize das atividades"*** — e, quando a internet não dá
> versão maior, **mostrar a figura no tamanho dela**.

## 1. O que foi colhido

Quatro buscas pelo `buscar-fotos.yml` (input `imagens=`), **96 imagens**, todas
olhadas em folha de contato antes de escolher:

| busca | termo | destino | trouxe |
|---|---|---|---|
| faca | `faca de cozinha desenho infantil clipart colorido` | `_sequencias/figuras_21set/faca` | 24 |
| anzol | `anzol desenho para colorir atividade` | `_sequencias/figuras_21set/anzol` | 24 |
| sol | `sol desenho para colorir simples atividade` | `_sequencias/figuras_21set/sol` | 24 |
| dinossauro | `dinossauro desenho para colorir simples contorno` | `_sequencias/figuras_21set/dino` | 24 |

## 2. O que entrou — e de onde veio

Recortadas com o `_padrao/recortar_do_branco.py` (enchente a partir da borda,
nunca limiar), aparadas na caixa do desenho e postas com 400 px de altura.

| figura | caderno | era | ficou | página de origem |
|---|---|---|---|---|
| `o5_anzol.png` | `_ort5` | 35×74 | **255×400** | `pt.vecteezy.com/arte-vetorial/12551699-anzol-de-desenho-animado-preto-e-branco` |
| `o5_sol.png` | `_ort5` | 75×89 | **394×400** | `amocolorir.com.br/sol-para-colorir-12-desenhos/` |
| `ls_dinossauro.png` | `_ort5b` | 208×90 | **495×400** | `daquidali.com.br/desenho-de-dinossauro-para-colorir/` |

As três são **linha preta de folha de colorir** — o mesmo desenho que a
professora entrega no papel, que é exatamente o que a regra da origem protege.
O `VIMG` dos dois cadernos subiu para `3`, senão o navegador da criança
continuaria servindo a figura pequena do cache.

## 3. O que NÃO entrou — a faca, e o motivo

**A faca continua a de sempre (260×71 px), agora mostrada no tamanho dela.**
Isto está escrito aqui para ninguém refazer a busca achando que eu esqueci:

- as facas **bonitas e do estilo certo** das 24 colhidas vêm de banco de imagem
  **com marca-d'água estampada em cima do desenho** ("Magnific") — e
  **marca-d'água não vai para a criança**;
- as **limpas** são de estilo realista, que briga com o barro 3D dos cadernos de
  alfabetização (abelha, abóbora, bota, caneca — ver `_alfa1/img/`);
- **gerar por IA está proibido** em folha viva, por ordem dele.

Então valeu a saída que a própria regra nomeia. Com o guarda `naoAmplia()` (hoje
portão `1i9`), a faca aparece a 260×71 px: **menor do que aparecia e nítida**,
nos sete cadernos em que ela mora (`_abc1`, `_alfa1`, `_jogo1`, `_let1`,
`_mont1`, `_sil1`, `_som1`).

**Se um dia aparecer uma faca grande, limpa e no estilo do barro 3D**, é só
trocar o arquivo e subir o `VIMG` dos sete — nada mais precisa mudar.
