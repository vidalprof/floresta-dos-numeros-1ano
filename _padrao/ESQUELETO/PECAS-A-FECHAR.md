# 🔧 PEÇAS A FECHAR — passam no `peca.sh` isolado, mas FALHAM na banca MONTADA

Descoberto ago/2026 pela **prova de banca por lote**: o `peca.sh` prova a peça
SOZINHA, e a `provar_esteira.sh` só passa 16 mecânicas pela banca inteira. As
outras ~39 nunca tinham sido **jogadas montadas**. Rodando a banca num lote delas
(esboço + montar + `auditar.sh`), duas quebraram em tempo de jogo — defeitos que
o `peca.sh` NÃO pega e que morderiam o Marcos se ele pegasse a peça amanhã.

> ⚠️ Ao consertar cada uma: reproduzir montando um lote
> (`esboco.py <pasta> --mecs <peça> --fases 6` + mesa/voz/currículo, ver
> `provar_gavetas.py`) e rodar `bash _qa/auditar.sh <pasta>/index.html`. Fechar
> só quando o **jogador chegar à medalha** e o **leiaute** passar (as falhas de
> VOZ/escada/cobertura num lote-descartável são esperadas — não têm voz gravada
> nem conteúdo real; o que importa é jogador + leiaute + erros de JS).

## Lote 1 — Matemática/História/Geometria (13 peças pouco usadas) — ✅ FECHADO

- **`reta-numerica`** — ✅ **FECHADA** (ago/2026). A "CRASH lendo 'alvo'" era
  sintoma: a peça fechava chamando `fimReta()` DIRETO (tela de fim própria), e a
  ponte da esteira só avança de fase pelo `mostraBanner` — então na montada a
  criança ficava presa no medidor e o auditor-jogador (que só vê o fim quando a
  `.medal` aparece após um toque dele) estourava. **Conserto:** o fim passa pelo
  `mostraBanner("Você mediu a sua reta!", fimReta)`, igual à `estimar`. Verificado:
  o jogador ATRAVESSA a fase na montada. → virou lição no CONTRATO ("peça que
  fecha na mão é um beco").
- **Mesmo parentesco, achado ao consertar a reta e FECHADO junto:** `bingo`,
  `domino`, `relogio` fechavam por tela própria (`fimBingo`/`fimDomino`/
  `fimRelogio` + botão "Jogar de novo" que só reinicia) — becos idênticos. Os três
  agora fecham pelo `mostraBanner(...,fim<Nome>)`. Verificado montado: o jogador
  passa reta→bingo→domino→relógio sem travar e sem erro de JS. (`conserte-o-erro`
  parecia do grupo mas o botão de fim dela já chama `fimDaPeca()`, que a ponte
  reaponta — não é beco.)
- **`contadores`** — ✅ **FECHADA** (ago/2026). O `.btn` estourava na horizontal no
  celular estreito (montada). **Conserto:** `flex-wrap:wrap` no `.linc` (rede de
  segurança: nunca vaza) + `@media (max-width:380px)` encolhendo o mínimo dos
  botões (segue acima de 40px de alvo) e o mostrador.

As outras 11 do lote (balanca, base-dez, saltos-na-fita, repartir, estimar,
medir, grafico, tabela, linha-do-tempo, coordenadas, simetria) **não travaram o
jogador nem estouraram o leiaute** — os avisos que sobraram eram de voz/escada
(esperados no descartável). Ou seja: montam E jogam; ainda faltam voz+conteúdo
reais quando forem usadas de verdade.

## Lote 2 — "config garblada pelo esboço" (nova família, ago/2026)
Descoberta rodando o jogador nos lotes: o esboço marcava com «...» TODAS as
gavetas fora a principal, inclusive as de CONFIG — e config garblada prende o
jogador em 0% (0 alvos data-qa), sem erro de JS.
- **`bussola`** — ✅ **FECHADA**. `DIRS`→`["«NORTE»"...]` (botão nunca casava com
  o alvo) e `RODADAS.tipo`→`"«achalugar»"` (rodada no galho errado). Conserto:
  `esboco.py` pula as `/*TECNICA*/`; marquei `REF/SETA/RODADAS` como técnica na
  peça (só `LUGARES` sobra de conteúdo). Jogador ATRAVESSA (0→100→BANNER). Lição
  no CONTRATO.
- **`calendario`** — ✅ **FECHADA** (ago/2026). Conserto: `SEM/SEMH/SEMV/SEMD/ORD/
  UNM/FASES` ganharam a marca `/*TECNICA*/` na linha da `var` (o esboço para de
  garblar `FASES[i].t`, então a rodada não cai mais no galho torto). Para o
  var-pick não pegar `SEM` (1º vetor), a peça passou a dizer "troque APENAS `MES`"
  — o integrar reconhece o marcador (`troque APENAS|CONTEÚDO É SÓ EXEMPLO`) e
  elege `MES` como principal. Verificado: `var=MES, tecnicas=[FASES,ORD,SEM,SEMD,
  SEMH,SEMV,UNM]`; na montada o `FASES` sai **intacto** (`t:"achar"`, não `«achar»`);
  o jogador ATRAVESSA a calendario montada (0%→86%→BANNER, sem erro JS); `peca.sh`
  código 0. → lição no CONTRATO.
  - **⚠️ LIÇÃO PAGA no conserto (nova família de defeito):** escrever a marca
    `/*TECNICA*/` **como texto DENTRO de um comentário `/* … */`** fecha o
    comentário no primeiro `*/` e derrama o resto como CÓDIGO. Aqui virou uma
    chamada-fantasma `errado(` ("galho errado (0 alvos"). Quem pegou foi o portão
    `confere_contra_motor` do `integrar` ("AS PEÇAS CHAMAM N NOMES QUE NÃO EXISTEM:
    errado, semana") — ou seja o portão já existe e funcionou. Regra: nunca citar
    `/*…*/` literal dentro de um comentário; escrever "marca TECNICA" por extenso.

## Lote 3 — "config acoplada garblada" (as nunca jogadas montadas) — ✅ FECHADO (ago/2026)
Rodei o jogador MONTADO em 23 peças que nunca tinham sido jogadas na esteira
(lotes de 6 mecânicas × 30 fases, segmentos `JSTART/JSTOP` por mecânica). **Seis
travavam** — todas da MESMA família da bússola/calendário: o esboço garbla as
gavetas de config, e ou some com uma FUNÇÃO (vira `dados` JSON), ou quebra uma
CHAVE DE ACOPLAMENTO (a rodada aponta para um nó/efeito que não existe mais):
- **`camadas-mapa`** — `CAMADAS[i].monta is not a function` (as funções de desenho
  do mapa morriam no JSON). → CIDADES/MORROS/CAMADAS/PERG viram TECNICA.
- **`mapa-conceitual`** e **`teia-alimentar`** — `Cannot read properties of null
  (reading 'el')`: as ligações usam `a`/`b`/espécie como chave, e `a`/`b` NÃO estão
  no `LIGACAO` do `marca()`, então garblam e `noDe(chave)` volta null. → o grafo/
  simulador inteiro vira TECNICA.
- **`criar-desafio`** e **`passo-a-passo`** — travavam em 0% (grade/receita sem
  alvo depois de garblada; `passo-a-passo` ainda tem `EFEITO` de funções). →
  COLUNAS/PISTAS/ESC e RECEITAS/CE/EFEITO viram TECNICA.
- **`intruso`** — travava em 0%: `fora:"cenoura"` aponta para o `k` de um item,
  mas `fora` não é chave protegida (`marca()` só guarda k/alvo/sp/i/id/ref/para/de),
  garblava p/ «cenoura» e `item.k===fora` nunca casava. → RODADAS vira TECNICA.
  **Achado pela varredura estática (o portão novo abaixo), não pelo jogador.**
- **`calendario`** (Lote 2) — mesma raiz.

> **🚪 PORTÃO NOVO `_qa/acoplamento.py`** (regra em `_qa`, roda dentro do
> `provar_gavetas.py`): varre as 81 peças e reprova **função em gaveta de
> conteúdo** (o caso do `monta:function`/`EFEITO` — sempre defeito, 0 falso
> positivo) e **avisa** sobre uma propriedade não-protegida que aponta para a
> chave de um item (o caso do `fora`). O aviso é só p/ rodar o jogador montado
> (pode ser conteúdo legítimo). Hoje: 0 erros; 1 aviso benigno (`memoria.fig`,
> que só garbla em lote-descartável — em atividade real o `dados` vem inteiro).

As outras **18 passaram montadas sem tocar** (jogador 0%→BANNER, sem erro JS):
achar-na-cena, andar-ate, circuito, decisao, ditado, filtro, girar,
letras-escondidas, misterio, mudanca-permanencia, padrao, prever-observar,
rotular, simulador, tangram, termometro, tracar-caminho, trilha.

> **⭐ REGRA DA FAMÍLIA (para toda peça nova):** se uma gaveta guarda FUNÇÃO
> (`monta:function`, mapa de efeitos) **ou** uma CHAVE que outra parte procura
> (`a`/`b`/`k`/espécie/efeito), ela é CONFIG → marca `/*TECNICA*/` na linha da
> `var`. O `marca()` só protege `k`/`alvo`/`sp`; qualquer outra chave de
> acoplamento garbla e trava o jogador (0 alvos) ou estoura (`null.el`,
> `x is not a function`). Peça de simulador/mapa/grafo costuma ser TODA técnica
> (roda com o conteúdo real; o professor troca editando a peça, não o conteudo.json).
> Só o `provar_gavetas` NÃO pega isto — tem que rodar o JOGADOR montado.

## Ainda não jogadas montadas (fila)
Nenhuma da lista original. Todas as 81 gavetas montam (`provar_gavetas`) e as
peças pouco usadas foram jogadas montadas (lotes 1–3). Peça NOVA: rodar o jogador
montado antes de dar por fechada — o `peca.sh` isolado não pega a família acima.

## Balanço da varredura montada (ago/2026)
- **58 peças jogadas montadas por mim** (lotes B–Y + isoladas), todas 0%→BANNER
  sem erro JS. Dessas, **8 travavam e foram consertadas**: calendario,
  camadas-mapa, mapa-conceitual, teia-alimentar, criar-desafio, passo-a-passo,
  intruso (+ bussola, no Lote 2) — toda a família "config acoplada garblada".
- **23 restantes** são mecânicas do dia a dia usadas em atividades PUBLICADAS
  (arrastar, caça-palavras, cruzadinha, forca, quebra-cabeça, memória, digitar,
  bater/juntar-sílabas, montar-frase, quem-sou-eu, ligar-pontos, pintar/canvas,
  traçar-letra, vitrine, sombra, comparar, sete-erros, labirinto, autoexplicação,
  caixa-dinheiro, ouvir-achar) — provadas em produção (Trem, Legenda, Lojinha…).
- **Estático 100% limpo:** `node --check` nas 82, `provar_gavetas` (81 montam),
  `_qa/acoplamento.py` (0 erro; 1 aviso benigno `memoria.fig`).
