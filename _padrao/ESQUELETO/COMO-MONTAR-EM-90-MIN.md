# ⏱️ MONTAR UMA ATIVIDADE EM 1H30 — o caminho, com os tempos MEDIDOS

Meta do Marcos (ago/2026): *"conseguir deixar uma atividade inteira com o
esqueleto em minutos e não em horas, e claro que fique profissional e
fantástica"*.

O motor está pronto e a esteira roda do nada ao `index.html`. Este arquivo é o
**caminho**, na ordem, com o **relógio de verdade** — medido em 2026-08-09 nesta
máquina, não estimado. Serve para saber onde o tempo realmente vai e o que dá
(e o que não dá) para apressar.

---

## O relógio: máquina × cabeça

| Passo | Comando | Tempo MEDIDO |
|---|---|---|
| Esboço das 32 fases | `python3 _padrao/ESQUELETO/esboco.py _pasta --fases 32` | **5,5 s** |
| **Escrever o conteúdo** | (é aqui que mora o trabalho) | **o resto** |
| Montar o `index.html` | `python3 _padrao/ESQUELETO/montar.py _pasta` | **4,8 s** |
| Regerar as peças (só se mexeu numa) | `python3 _padrao/ESQUELETO/integrar.py --escrever` | **0,6 s** |
| Portão do custo, antes de gastar | `python3 _qa/cartela.py _gerar_imagens.json` | ~1 s |
| Gerar a arte (Actions, em cartela) | `gerar-imagens.yml` | **~5 min** por corrida |
| Voz + publicar + conferir | `entregar.yml` | **~4 min** |
| **Colher a voz da rodada** (2 voltas) | `colher.py _pasta` → `montar.py` → repetir | **~7 min** cada volta |
| Banca completa (35 portões) | `bash _qa/auditar.sh _pasta/index.html` | **6,1 min** (367 s) |
| **Só os portões de texto** (para consertar) | `bash _qa/auditar.sh --reparo _pasta/index.html` | **38 s** |
| Bancada de UMA peça | `bash _qa/peca.sh _padrao/pecas/x.html` | 30 s |

⚠️ **O relógio da banca, contado inteiro** (ago/2026, tudo medido). Ela levava
**4m30** — e era mentira barata: o jogador automático parava na **3ª fase de
32**, achando que a medalha *da peça* era o fim da atividade. Consertado, ele
joga as 32 e a banca foi para **15m14**. Dois cortes honestos depois:

| | tempo |
|---|---|
| antes (jogando 3 fases de 32) | 4m30 ⚠️ cega |
| jogando as 32, tudo em fila | 15m14 |
| jogador na mesma largada dos outros de navegador | 10m44 |
| conferir a voz com 2 partidas em vez de 6 | **6m07** |

A última merece explicação: **conferir e colher não custam o mesmo**. Colher
precisa das seis partidas (as dicas sorteiam de que carta falam); a banca só
pergunta *"sobrou alguma?"*, e o que falta de forma sistemática aparece na
primeira. Medido: com 2 partidas ela ainda acusou as **29** falas que faltavam.

Ou seja: a banca hoje custa **1m37 a mais** que a versão cega — e mede a
atividade inteira. Foi ela que revelou o beco da fase 3 e as 14 falas mudas.

⚠️ **O tempo da banca cresce com a atividade.** Os 6m07 são de uma atividade de
32 fases; a de 39 fases (a Central de Entregas, ago/2026) levou perto de meia
hora — ela abre o Chromium em 6 tamanhos × 45 telas e ainda joga até a medalha.
Por isso nasceu o **`--reparo`**: enquanto se conserta, roda-se ele (38 s,
só os portões de texto) quantas vezes for preciso; a banca inteira, sem
bandeira, antes de o Marcos ver. O rodapé do modo reparo diz com todas as letras
que passar nele **não é aprovação**.

**Soma da máquina: ~30 minutos** (era ~15 antes de a banca e a colheita
passarem a percorrer a atividade inteira). Ou seja: dos 90, **60 são de cabeça** —
escolher o conteúdo, escrever os enunciados, olhar a arte que voltou e decidir
se ela serve. Não existe atalho para essa parte, e é ela que faz a atividade
ficar boa ou medíocre. O esqueleto não escreve a aula; ele tira do caminho as
seis horas de código que vinham antes.

---

## A ordem, sem pular nada

1. **Currículo primeiro.** Abrir `_curriculo/blumenau.txt` e copiar os objetivos
   REAIS do ano/disciplina. O montador cobra `mesa` e `curriculo` preenchidos —
   e cobra de propósito: fase sem objetivo é fase sem razão de existir.
2. **`esboco.py`** → nasce o `conteudo.json` com as 32 fases já no formato certo,
   com as mecânicas distribuídas (nenhuma repetida em fases vizinhas, um
   objetivo a cada 4 fases). **Só trocar o que está entre «».** → antes de trocar
   a mecânica de uma fase, abrir o `_padrao/CARDAPIO.md` e escolher pelo ENCAIXE
   (as 44 peças nunca usadas estão marcadas ⭐ — mirar ≥1 por atividade).
3. **Escrever o conteúdo.** A escada sobe: concreto → figural → simbólico; o
   problema vem primeiro e o conceito por último; aquecimento entre 25% e 65%.
   Ver `_padrao/RECEITA.md` antes de começar, não depois.
4. **`montar.py`** → escreve `index.html`, `falas.json` e `arte.json`.
   Ele já reprova id repetido, mecânica que não existe e campo faltando.
4b. **COLHER A VOZ DA RODADA — duas voltas, não pular.** As peças montam frases
   em tempo de jogo ("Dica: uma das cartas fala de *bolo*", "A letra que vem
   agora está piscando") que o montador não tem como adivinhar: elas vivem
   dentro da peça, não no seu conteúdo. Sem este passo a criança aperta o
   alto-falante da ajuda e ouve **silêncio** — e é a ajuda, justamente onde quem
   não lê mais precisa da voz.
   ```
   python3 _padrao/ESQUELETO/colher.py _pasta     # joga e grava no falas.json
   python3 _padrao/ESQUELETO/montar.py  _pasta    # o VOZOK sai do falas.json
   python3 _padrao/ESQUELETO/colher.py _pasta     # 2a volta: as dicas SORTEIAM
   python3 _padrao/ESQUELETO/montar.py  _pasta
   ```
   **Duas voltas porque as dicas sorteiam de que carta falam.** Medido na
   `_prova30`: **32 → 2 → 0**. A banca reprova enquanto faltar alguma (portão
   0f2), então não dá para esquecer — mas é melhor já fazer certo.
5. **Arte em CARTELA.** `python3 _padrao/cartela.py plano` agrupa; o portão do
   custo reprova 3+ peças soltas. Cena e fundo vão pelo **caminho grátis**
   (Pollinations); peça que a criança olha de perto vai no Gemini, em cartela
   (~R$0,02 cada). As 3 camadas do mascote são **edição** da pose parada — nunca
   geradas do zero, senão ele treme.
6. **`entregar.yml`** grava a voz que falta (o `falas.json` é a verdade),
   publica e pergunta ao próprio site se está servindo o que subiu.
7. **`bash _qa/auditar.sh`** até sair **0**. Portão que imprime nada não é
   "passou": é "rodou cego" — ler a lista de "não medi".
8. **PUBLICAR.** A banca saiu 0? Então publica (a autorização é permanente,
   ver CLAUDE.md — só para quando o Marcos disser "espere"):
   - **Atividade NOVA** (não tem repo ainda): `fabrica.yml` com
     `repo_name=<nome-minusculo-com-hifens>` e `source_dir=_pasta`. Ela CRIA o
     repositório, publica e liga o Pages. O link fica
     `https://vidalprof.github.io/<repo_name>/`.
   - **Atividade que JÁ existe** noutro repo: `atualizar.yml`
     (`repo_name=<repo>`, `source_dir=_pasta`) — espelha o destino.
   - **Confirmar o build:** `deploy-pages.yml` (`repo_name=<repo>`) → o log diz
     `200` na URL e o status real (`built`). Sem `actions_list` (payload gigante).
   - ⚠️ **NÃO** pôr card no hub `_site` — regra do Marcos: atividade nova é só
     repo + link, até ele pedir o card com todas as letras.
9. **O portão do professor.** Nenhum script substitui.

*(Exemplo de ponta a ponta, ago/2026: a Lojinha do Pipo — 36 fases, dinheiro 1º
ano — nasceu do `esboco.py`, passou a banca EXIT 0 e foi publicada pela
`fabrica.yml` em `lojinha-do-pipo`. É a prova de que a esteira fecha o ciclo.)*

---

## O que NÃO dá para apressar (e por que insisto nisso)

- **A arte volta errada com frequência.** Pedir "um pão francês" e receber um
  pão de forma é normal; por isso o passo 5 tem revisão humana. Publicar sem
  olhar é como imprimir prova sem ler.
- **A banca leva 4,5 minutos.** Vale cada segundo: nesta semana ela pegou 45
  textos ilegíveis, uma opção presa atrás da barra e uma explicação que sumia
  num pisco. Rodar no fim, uma vez, é mais barato que descobrir na sala.
- **A voz só se confere pelo `falas.json`.** MP3 não se lê. Atividade sem
  `falas.json` não tem como ser conferida — criar o arquivo é parte do trabalho.

---

## O estado medido do estoque (2026-08-16)

| O quê | Número |
|---|---|
| Peças (arquivos em `_padrao/pecas/`) | **80** (79 reais + o `MOLDE`) |
| Peças reais que passam `peca.sh` EXIT 0 | **79 / 79** (varredura 2026-08-16) |
| `MOLDE.html` | é o **template** (base de CSS do `integrar`); o `peca.sh` o reconhece e sai 0, sem FAIL falso |
| Esteira do nada ao `index.html` | **provada de ponta a ponta**: Lojinha 36 fases → banca EXIT 0 |

*(Medido em 2026-08-11, varredura inteira com a bancada parada. As 11 sem medida
estão listadas no `CONTRATO.md` com o motivo de cada uma — a maioria é mecânica
de criação ou que não pune por decisão pedagógica.)*

⚠️ A `_prova30` é a atividade de EXEMPLO da esteira: ela passa nos 13 portões de
estrutura e **reprova na banca completa de propósito** — não tem arte nem voz
(11 figuras pedidas que não existem, 6 fases mudas). Isso é o esperado, não é
defeito; a banca completa é para atividade de verdade.
