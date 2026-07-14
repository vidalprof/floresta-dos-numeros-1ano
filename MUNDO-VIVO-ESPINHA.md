# 🦴 MUNDO VIVO — ESPINHA DORSAL À PROVA DE ERROS
## Contrato de produção em série: QUALQUER modelo (inclusive fraco) que seguir
## isto produz um mundo novo sem quebrar o que já funciona. Fontes-mãe (NÃO
## duplicadas aqui): IDEIA-MUNDO-VIVO.md (visão) + MUNDO-VIVO-MOTOR.md
## (manual técnico do motor, §1-§8). Referência viva: `_pub_confeitaria/mundo/index.html`.

================================================================
## 1. A VISÃO EM 10 LINHAS
================================================================
Cada ano/série ganha UM único mundo vivo, e o currículo do ano É o mapa
desse mundo — a criança não "abre atividade", ela **volta ao mundo dela**
o ano inteiro, pelo mesmo link. O conteúdo deixa de ser pergunta e vira
**ferramenta**: a criança age, o mundo reage; errar não dá X, dá
consequência visível que ela conserta. Os **6 pilares** que fazem ser GAME
(IDEIA §2), sagrados em todo mundo novo:
1. Espaço, não menu — desafios são LUGARES; 2. Consequência visível e
PERMANENTE no cenário; 3. Personagens com desejo (missão = pedido de
alguém); 4. Economia e coleção (moedas, mochila, bichinho); 5. Game feel
(parallax, partículas, squash, sons, câmera — ver §3); 6. O conteúdo é a
ferramenta, a "matéria" fica invisível dentro da vida do mundo.

================================================================
## 2. O QUE JÁ EXISTE vs O QUE FALTA
================================================================
Base: `_pub_confeitaria/mundo/index.html` (referência testada). Antes de
prometer algo ao Marcos, confira nesta tabela — evita reprometer o que já
existe ou esquecer o que ainda não foi construído.

**JÁ EXISTE (motor pronto, não reescrever — só clonar):**
- Rua andável: parallax, câmera com lerp, física do personagem (easing)
- Personagem vivo: sprites de passo/pulo, squash, idle, sombra, poeira, som
- Clima vivo: dia/noite, chuva/neve/trovoada, estrelas, luz nas lojas
- NPCs com desejo (balão ❗ + fala de pedido) e cliente-mascote de outra loja
- Consequência permanente: trancada/atual/feita persistidas (localStorage)
- Motor de missões micromundo (modos A/A2/A-montar/B/D), sem pergunta-resposta
- Plaquinha de matemática revelada DEPOIS da ação + festa
- Tela-título de videogame (rua viva atrás do logo, HUD escondido)
- HUD com moedas voando até o contador
- Entrada por porta de verdade + interior próprio por loja
- Save local de sessão (nome digitado, 1 slot, expira em 70 min)
- Modo professor por código digitado (`1275@`, destrava tudo)
- Conquistas (badges, 6 condições) + diploma no fim da rua
- Voz gravada em mp3 externo para toda fala do motor (não é TTS)

**FALTA (da IDEIA, zero linha de código ainda — ver §8 para ordem):**
| Item | Tamanho |
|---|---|
| Login sem digitação (turma → nome/avatar → 3 figurinhas) | M |
| Save por aluno no Firebase (`/mundos/<turma>/<aluno>`) | M |
| Senha de save/estepe em plaquinha (ex. `PÃO-42`) | P |
| Progressão que atravessa o ano (hoje o save é de 1 aula, 70 min) | M |
| Ovo (3 cores) que choca + bichinho que evolui o ano todo | M |
| História com decisões/ramificação, atos por bimestre | G |
| Painel do professor ao vivo + relatório anual | G |
| Economia de verdade + mochila + coleção de itens | M |
| Ponte/bairro seguinte — mundo multi-bairro incremental | G |
| Cadastro da lista da turma pelo professor (salvo no Firebase) | M |

================================================================
## 3. RECEITA DE GAME FEEL SAGRADA — não altere sem o modelo forte
================================================================
Estes números são o que faz o mascote parecer um personagem de jogo de
verdade, não uma imagem deslizando. São **canônicos**: todo mundo novo
clona e mantém exatamente estes valores. Mudar qualquer um é mecânica de
motor → escalada (§7), nunca ajuste "no olho" por um modelo fraco.
- **Aceleração/frenagem:** `alvo=held*5.4; vx+=(alvo-vx)*.16` (easing, não
  liga/desliga) — é o que o cérebro lê como peso real.
- **Câmera de game:** mira `pos - VW*.42` com lerp `.1` — o personagem fica
  adiantado na tela, nunca colado no centro.
- **Troca de sprite:** a cada 135ms, alternando pose de contato e passagem.
- **Sons sintetizados com glissando** (Web Audio, nunca arquivo): passo
  `beep(150,120,.05,.05,'square')` grave descendente; pulo
  `beep(330,660,.18,.1,'sine')` subindo (impulso); pouso
  `beep(110,70,.12,.12,'sine')` descendo (baque de peso).
- **Respiração/logo (mvResp):** scale até `1.025` em `2.6s`.
- **Squash de aterrissagem:** achata e volta em `180ms`.
- **Poeira no pouso:** **2** partículas de puff (nunca 1, some rápido demais).
- **Sol pulsando:** scale até `1.07` em `5s` — o céu também respira.
- **Aceno idle:** após `~4s` parado o mascote acena; repete a cada `6s`.
- **Tela-título:** mascote GRANDE, de frente, acenando e quicando dentro do
  próprio título — diferente do chef pequeno passeando ao fundo (os dois
  existem no motor; quem dá boas-vindas é o grande).
- Gravidade `.95`, pulo `vy=13.5`, squash `scaleY(.82)/scaleX(1.12)`,
  parallax `1/.35/.12`, tick `33ms` — copiar o bloco de física inteiro.

================================================================
## 4. REGRAS INEGOCIÁVEIS DO MARCOS
================================================================
- Cada mundo tem **TEMA e cenário DIFERENTES** dos outros (nunca reusar
  fachada/paleta já publicada); **interiores temáticos** por local.
- **Nada de pergunta-e-resposta.** O mundo reage à ação (MOTOR §1) — se a
  ideia pedir botão "Conferir", pare e repense o desafio.
- **Sem sobreposição de texto/imagem**, em nenhuma tela nem resolução.
- **Objetos sempre contidos no recipiente** — nada vazando da borda, mesmo
  nas cenas extremas (30 itens, 7 grupos).
- **Setas na tela só no toque**; no PC o controle é teclado.
- **Entrar num local = seta pra CIMA na porta**, com balão de fala do NPC
  explicando o que tem ali antes de entrar.
- **Clima vivo obrigatório:** dia/noite, chuva, trovoada, neve, com luzes
  acendendo nas lojas à noite.
- **Voz gravada para TODA fala** — nunca TTS do navegador, nunca texto mudo.
- **Roda em PC antigo (ES5) e em celular** — 1 HTML, zero framework/CDN/WebGL.
- **Pré-título idêntico à tela inicial** cobre o carregamento dos assets —
  a criança nunca vê tela branca ou "carregando…".
- **Imagens pesadas de uso raro** (certificado, telas especiais) ficam em
  arquivo externo em `img/`, nunca em base64 no HTML principal.

================================================================
## 5. FLUXO DE PRODUÇÃO — aceite binário por etapa
================================================================
Os comandos e o roteiro de QA exatos estão em MUNDO-VIVO-MOTOR.md §5 (não
duplicados aqui). Cada etapa só avança com PASSA; NÃO PASSA = corrigir
antes de seguir, nunca "depois eu volto".
- **P1 Currículo:** habilidades BNCC do ano/bimestre mapeadas → missão →
  modo do motor (tabela MOTOR §2). PASSA = tabela aprovada pelo Marcos.
- **P2 Clonar:** copiar a referência byte a byte, trocar só tema/dados
  (§3 do MOTOR: fachadas, mascotes, interiores, cores). PASSA = `node
  --check` limpo e diff tocando só zonas de dados (nunca função do motor).
- **P3 Desafios:** escrever `PARADAS`/`desafios` no formato do MOTOR §3,
  sem renderer novo. PASSA = cada desafio abre uma cena válida no teste.
- **P4 Áudio:** gerar lote de fala (enunciado + explicação de cada missão
  nova) pelo pipeline do MOTOR §4. PASSA = zero fala muda.
- **P5 QA completo:** roteiro Playwright do MOTOR §5, retrato E paisagem,
  todos os tipos de desafio, erro proposital + conserto. PASSA = zero
  `pageerror`, screenshots das cenas extremas sem vazamento/sobreposição.
- **P6 Publicar:** commit `[publicar]`, conferir `build=built`. PASSA =
  link abre com Ctrl+F5 e bate com o que foi mostrado ao Marcos.

================================================================
## 6. ERROS JÁ PAGOS → BARREIRA (uma linha cada; nunca apagar, só somar)
================================================================
- Sprite "pulsando" ao andar → recorte 1:1 da MESMA cartela, pés alinhados
  num canvas comum (nunca autocrop independente por pose).
- Pé patinando ao acelerar → trocar quadro por DISTÂNCIA (~34px), não tempo.
- Clique engolido pelo arrasto → guarda de 280ms (`MM.tDrop`).
- Fala velha invadindo a cena nova → `_encadear=false; pararFala()` na troca.
- Som travado até o navegador liberar → destravar no 1º keydown/mousedown/
  touchstart chamando `resume()` do AudioContext (explicar com honestidade
  à criança, nunca fingir bug resolvido).
- Mascote errado extraído do HTML de origem → ancorar busca em
  `MASCOTE_POSES` (ou objeto próprio do jogo), sempre conferir com o usuário.
- Build do Pages engasgando (histórico `.git` inchado por asset pesado que
  entrou e saiu) → portal leve (link, nunca cópia) + `republicar-limpo.yml`.
- Objeto vazando da bandeja → padding `20/58/46` + doce 32px quando lote
  ≥18, sempre conferido com screenshot das cenas extremas.
- Gênero errado no rótulo ("Quantas caixas?") → `fem:true` em `mmLugar`.
- Balão de fala desatualizado ao voltar ao NPC → `MV.perto=-2`.
- Interior "piscando" no boot → vestir a cena SÓ em `abrirParada`, nunca no
  carregamento da página.
- Arquivo de ~3MB quebrado por regex gulosa em base64 → editar sempre por
  âncora única (Python `sub1`), nunca busca-e-troca ampla.

================================================================
## 7. ESCALADA — parar é o comportamento correto
================================================================
- **Gatilhos automáticos:** mecânica que não existe nos 4 modos do MOTOR
  §2; necessidade de tocar função do motor (`mvTick`, `renderDesafio`,
  `mmCena*`, física, câmera); login/save novos; decisão pedagógica ambígua.
- **Regra das 2 tentativas:** bug que resiste a 2 hipóteses de conserto =
  escalar. Nunca a 5ª tentativa às cegas num arquivo de 3 MB.
- **Aviso ao Marcos/modelo forte:** o que travou, o que já foi tentado,
  arquivo + âncora exata, qual gate do §5 está falhando.
- **NUNCA escala** (é trabalho normal da produção em série): trocar dados,
  textos, imagens, áudios, cores; ajustar `desafios`; rodar QA; publicar.
- Depois da intervenção do modelo forte, a solução vira **atualização
  deste documento** (novo item no §4, novo gate no §5 ou nova barreira no
  §6) — o forte não conserta em silêncio, o documento fica mais forte.

================================================================
## 8. PRÓXIMAS FATIAS DA IDEIA — ordem sugerida
================================================================
Cada fatia é motor novo → modelo forte (política de modelos, IDEIA §6).
Ordem pensada por dependência (a de baixo precisa da de cima pronta):
1. **Login por figurinhas + save Firebase** — base de tudo que vem depois;
   sem isso não há "progressão que atravessa o ano" nem painel do professor.
2. **Ovo/bichinho que evolui** — usa o login/save recém-pronto, dá o
   primeiro motivo emocional para a criança voltar toda semana.
3. **História com decisões/ramificação** — precisa de save persistente
   (o caminho escolhido tem que sobreviver entre sessões).
4. **Painel do professor ao vivo** — lê os mesmos dados do Firebase que o
   login/save já estão gravando; sem eles não há o que mostrar.
5. **Bairros por bimestre (mundo multi-bairro)** — maior fatia (G),
   naturalmente por último: só compensa depois que login/save/história já
   dão sentido a "o mundo lembra o ano inteiro".
