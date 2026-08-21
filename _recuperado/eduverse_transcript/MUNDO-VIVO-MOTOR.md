# ⚙️ MUNDO VIVO — MANUAL DO MOTOR (para produzir barato)
## Criado pelo modelo forte (Fable) em jul/2026 · Confeitaria = implementação de referência
## Para quem lê: o modelo em produção em série (Opus 4.8 esforço alto) segue ESTE molde.

> **O que este manual é:** a receita pronta do motor de missões "micromundo"
> (o mundo reage, sem pergunta-e-resposta) + do mundo andável (rua com lojas).
> O motor JÁ EXISTE e está TESTADO em `_pub_confeitaria/mundo/index.html`.
> Produzir um mundo novo = CLONAR esse arquivo de referência e trocar DADOS
> (paradas, textos, imagens, tema) — **não** reescrever o motor.
> Na dúvida sobre uma mecânica NOVA (que não está aqui): PARAR e avisar o
> Marcos que a etapa pede o modelo forte (política de modelos, MANUAL-MESTRE §22).

================================================================
## 1. A REGRA DE OURO (o que "vivo" significa)
================================================================
A criança NÃO responde pergunta. Ela **age no mundo** e o mundo **reage**:
- Missão = pedido de um personagem (balão + voz). O conteúdo é a FERRAMENTA.
- **Sem botão "Conferir"**: quando a ação termina (bancada esvazia / grupos
  completos), o mundo confere SOZINHO depois de ~0,5s.
- **Erro ≠ X vermelho**: erro = consequência visível (o prato com menos fica
  triste 😞 e balança; a pilha de moedas não bate com o total) + fala guiando.
  A criança CONSERTA o mundo. Só na 2ª falha aparece a dica com a conta.
- **Acerto = descoberta**: a matemática aparece DEPOIS da ação, numa
  plaquinha de madeira (`.mmPlaquinha`, ex.: `20 ÷ 4 = 5`) + festa (confete,
  elogio, voz). Diagnóstico/streak/pontos continuam os do jogo (acerto()/erro()).

================================================================
## 2. OS 4 MODOS DO MOTOR (cobrem qualquer divisão/multiplicação)
================================================================
Regras de escolha do modo pelo TAMANHO do número (tátil até ~30):

| Modo | Quando | Função | Como joga |
|------|--------|--------|-----------|
| **A — concreto repartir** | total ≤ 30 | `mmCenaA(cfg)` | arrasta OU toca no destino; validação viva; carinha triste + treme no desigual; `sobra:true` liga o "Pratinho do Chef" (resto visível; no acerto o Chef "come" a sobra) |
| **A2 — concreto agrupar** | total ≤ 30, pergunta "quantos grupos" | `mmCenaG(cfg)` | caixa fecha SOZINHA ao encher (cap); nº de caixas fechadas É a resposta; não tem como errar — o mundo computa |
| **A-montar** (fonte infinita) | multiplicação pequena ("quantos ao todo?") | `mmCenaA({fonte:true,cap:...})` | bandeja nunca esvazia; criança enche cada grupo até o cap; total revelado no fim = descoberta |
| **B — propõe-e-encena** | números grandes (>30) | `mmCenaB(cfg)` | criança propõe com ➕/➖ e toca FAZER; a loja ENCENA (grupos enchem animados, total cresce); não bateu → "Faltaram 12!"/"Passaram 8!" visível + tenta de novo |
| **D — dinheiro** | preço/divisão de reais | `mmCenaD(d)` | propõe o preço de 1 unidade; pilhas 💰 encenam a soma; compara com o total |

`sub` do modo B: `"per"` (grupos fixos, propõe quantos em cada), `"ngr"`
(cap fixo, propõe quantos grupos), `"tot"` (tudo fixo, propõe o total —
usado em proporção; se errar, o mundo conta junto).

================================================================
## 3. O ROTEADOR (dados → cena) — onde plugar conteúdo novo
================================================================
`renderDesafio(d)` roteia por `atual.tipo`:
- `repartir` → `mmRepartirCena` (modo A) · `modo:"caixas"` → `mmCaixasCena` (A2)
- `resto` → `mmRestoCena` (A com `sobra:true`; usa `d.d,d.v,d.q,d.s`)
- `tabuada` → `mmTabuadaCena` (B "per": bandejas da vitrine)
- `dinheiro` → `mmCenaD` (usa `d.cents,d.n,d.q,d.un`)
- `escolha` → `mmEscolhaCena` decide sozinha lendo o desafio:
  - `d.op==="×"` → A-montar (fonte infinita) · `d.op==="÷"` → A repartir
  - `d.mul` (inversa) → extrai `D ÷ V` do enunciado; D≤30 → A; senão B "per"
  - `d.est` ou "÷" no texto → B "per" (padrão `(\d+) ÷ (\d+)`) ou B "ngr"
    (padrão "de N" = tamanho do grupo, ex. "bandejas de 12")
  - `d.prop` (proporção) → 3º número = 1 → descobre o "per" (A se ≤30, senão
    B "per"); 3º número > 1 → B "tot"
  - `d.d`+`d.v` (problema padrão) → "Para quant..." → A2 agrupar; senão A
- `memoria`/`montar` (j1/j2) → jogos próprios, INTACTOS.

**Contexto visual automático:** `mmDoceImg(texto)` escolhe o doce
(brigadeiro/cupcake/pirulito/donut/pão...) e `mmLugar(texto)` o recipiente +
nome + gênero (Mesa/Sacolinha/Pote/Cesta/Caixa/Amigo/Criança... `fem:true`
nas femininas — cuida do "Quantas caixas?"). O cliente que pede é o mascote
de OUTRA loja (`mmCliImg()` — cameo rotativo, mundo coeso).

**Para adicionar conteúdo novo:** só escrever `desafios` com os campos acima.
O roteador monta a cena. NÃO criar renderer novo sem necessidade real.

================================================================
## 4. FALAS E ÁUDIO (voz Antonio, sem TTS no navegador)
================================================================
- `falar(txt)` SÓ toca o que está gravado (`AUDIO_TXT[chave]`); texto sem
  gravação fica mudo. **Toda fala nova precisa entrar no lote.**
- Falas do motor são FIXAS (sem números) → objeto `MMF` (15 frases). Falas
  com números (enunciados/explicações) são as MESMAS já gravadas do jogo —
  o motor as reutiliza de propósito. **Ao criar missão nova: gerar o áudio
  do enunciado E da explicação do acerto.**
- Pipeline: frases → `_lote_falas.json` `[{id,texto}]` (id = `_chaveVoz(limparFala(t))`,
  DJB2 base36 — replicável em Python, ver `finalizar.yml`) → commit com
  `[audio]` → workflow gera `_audio/<id>.mp3` → copiar para
  `_pub_confeitaria/audio/` → adicionar `"<id>": "../audio/<id>.mp3"` no
  `AUDIO_TXT`. Conferir 1 chave com `node -e` antes de gravar o lote.

================================================================
## 5. QA OBRIGATÓRIO (o teste que já pegou bugs)
================================================================
Roteiro Playwright pronto: `mm_test.js` (scratchpad; recriar se sumir).
Para CADA tipo: (1) abrir a parada via `abrirParada(i)` + `rodarFase()`;
(2) ERRAR de propósito (desigual / proposta baixa) → esperar consequência
visível e `_errouNeste=true`, SEM plaquinha; (3) consertar → plaquinha +
botão Próximo; (4) zero `pageerror`. Testar retrato 390×780 E paisagem.
`node --check` no JS extraído após CADA edição (arquivo tem 3 MB — editar
por âncora com Python `sub1`, nunca regex gulosa; base64 quebra linha-a-linha).
Lições pagas: clique-vs-arrasto precisa de guarda de 280ms (`MM.tDrop`);
balão do mundo só atualiza com `MV.perto=-2` ao voltar; gênero nos rótulos.

================================================================
## 6. O MUNDO LÁ FORA (rua, fachadas, estados) — já pronto
================================================================
- Rua andável: parallax + chef com física (easing/squash/idle) — `mvTick`.
- Cada parada = fachada de loja com NOME GRAVADO POR CÓDIGO na placa
  (Gemini NUNCA escreve texto: gerar placa LISA, gravar com Pillow —
  `grava_placas.py`). Estados: trancada (cinza+cadeado), atual (❗ + NPC na
  porta), feita (bandeirinhas + ✓ permanentes). Título = rua viva atrás do
  logo (`telaInicial`), UI escondida com `#mundoLayer.modoTitulo`.
- Publicar: commit `[publicar]` → espelho no repo do site → conferir
  `_status/confeitaria.txt` = `build=built`.

================================================================
## 7. CHECKLIST DE PRODUÇÃO EM SÉRIE (Opus segue isto)
================================================================
1. Clonar a referência (`_pub_confeitaria/mundo/index.html`) — motor intacto.
2. Trocar TEMA: fachadas novas (cartelas 2×2 SEM texto → recortar → gravar
   nomes), mascotes/cartelas, interior claro, cores.
3. Escrever `PARADAS` novas (dados `desafios` no formato do §3 — o roteador
   monta as cenas sozinho). BNCC do ano ANTES (chapéu professor).
4. Gerar áudios (enunciados + explicações + falas fixas novas se houver).
5. Rodar o QA do §5 completo. Erro achado = barreira nova no teste.
6. Publicar e conferir build. Card no hub se for o caso.
7. **Avisar o Marcos** se aparecer mecânica nova, bug resistente ou decisão
   pedagógica ambígua → é hora do modelo forte (não improvisar).

> Fatias seguintes registradas (IDEIA-MUNDO-VIVO.md): ovo/bichinho, login
> por figurinhas + save Firebase, senha de estepe, bairros por bimestre.
