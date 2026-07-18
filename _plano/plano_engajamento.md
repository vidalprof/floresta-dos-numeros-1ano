# PLANO DO "QUERO VOLTAR AMANHÃ"
## Mundo Vivo — design de engajamento saudável (escola pública, sem dark patterns)
### Game Designer + Marcos · jul/2026 · ancorado em IDEIA/ESPINHA/MOTOR + motor da Confeitaria

> **Premissa honesta de cadência:** no laboratório da escola a criança volta ao mundo
> ~1x por semana, não todo dia. Então o loop é desenhado para funcionar em qualquer
> intervalo: o gatilho não é "não perca o dia", é "o mundo continuou existindo e
> guardou tudo pra você". Nada aqui pune quem faltou — é regra sagrada (seção 4).
>
> **Dependência técnica:** quase tudo abaixo precisa da **Fatia 1 (login por
> figurinhas + save Firebase)** e da **Fatia 2 (ovo/Docinho)** da ESPINHA §8. O que
> dá pra fazer barato JÁ, só com o motor atual, está marcado **[JÁ DÁ]**. O que
> depende de save está marcado **[PÓS-SAVE]**.

---

## 1. O LOOP EMOCIONAL DA SEMANA (o coração)

Seis batidas. Cada uma tem um sentimento-alvo e um gancho para a próxima. A criança
nunca sente "tarefa"; sente "minha vida no mundo continua".

**1) CHEGA → sensação: "eu tenho um lugar."**
Login sem digitação (turma → nome → 3 figurinhas). A câmera NÃO abre num menu: abre
sobre a rua já viva, e o **Docinho corre da direita da tela até parar na frente dela,
acenando** (reusa o sprite grande de boas-vindas da ESPINHA §3). Voz: "Você voltou!".
Não é login, é reencontro.

**2) O MUNDO LEMBRA DELA → sensação: "o que eu fiz ficou."**
Tudo que ela deixou está exatamente onde estava: a placa que ela consertou continua
consertada, a Dona Bela acena (consequência permanente do motor), as moedas dela
estão na mochila, o Docinho está no estágio de evolução que ela deixou. **Um NPC diz
uma frase-memória**: "Obrigada de novo pelos pães da semana passada!" — o mundo prova
que registrou a passagem dela.

**3) ALGO MUDOU DESDE A ÚLTIMA VEZ → sensação: "vale a pena ver o que há de novo."**
Este é o motor da curiosidade. A cada retorno, **1 a 3 pequenas mudanças visíveis**,
escolhidas do "baralho de deltas" (barato, reusa assets):
- o clima do dia é outro (o motor já sorteia dia/noite/chuva/neve);
- o ovo rachou mais um pouquinho / o Docinho está um tiquinho maior;
- uma **figurinha nova brilha "NOVA!"** numa vitrine;
- o **bairro ao longe** (o mistério trancado) ganhou +1 tábua na ponte;
- um NPC novo apareceu na porta com o balão "❗ Me ajuda!".
Regra de ouro: **sempre há pelo menos 1 mudança**, mesmo que mínima — nunca a criança
volta a um mundo idêntico. Deltas nunca são "você perdeu X"; são só coisas boas novas.

**4) JOGA → sensação: "eu resolvo, eu ajo."**
Missão concreta do motor existente (repartir/agrupar/dinheiro/montar). Sem
pergunta-e-resposta, sem cronômetro. O conteúdo é a ferramenta; errar vira
consequência que ela conserta, não X vermelho.

**5) PROGRESSO VISÍVEL → sensação: "eu subi, dá pra ver."**
No fim da missão, feedback físico e mensurável: **moedas voam** até o contador (motor
já faz), a **barra da ponte sobe um tijolo com som de construção**, o **Docinho ganha
XP visível** (uma faísca sobe até ele), a **figurinha entra no álbum com "toc" de
carimbo**. Progresso é sempre PESSOAL e da TURMA — nunca ranking (seção 4).

**6) GANCHO PARA A PRÓXIMA AULA → sensação: "quero ver o que vem."**
Antes de sair, o mundo **mostra uma promessa concreta e trancada**:
- "Faltam **2 missões** para o ovo chocar!" (contador visível subindo);
- "**Sexta tem Chuva de Doces** na praça — o Docinho vai adorar";
- "A Dona Bela disse que semana que vem te mostra uma coisa atrás da porta azul";
- a **senha de save do dia** vai pro caderno (seção 3) com um **selo/carimbo novo**.
O gancho é sempre curiosidade ("vem ver"), nunca cobrança ("você tem que").

> **O truque do loop:** a batida 3 (algo mudou) + a batida 6 (promessa trancada) são
> o que transforma "atividade" em "novela que eu acompanho". Custam quase nada:
> reusam clima, sprites e a barra de progresso que o motor já tem.

---

## 2. OS SISTEMAS

### 2.1 Ovo / bichinho **Docinho** (já projetado — Fatia 2) [PÓS-SAVE]
O primeiro motivo emocional para voltar. Companheiro do ano inteiro.
- **Escolha do ovo (3 cores)** no 1º dia → **choca por MARCO DE APRENDIZAGEM, nunca
  por tempo nem por assiduidade** (ex.: "choca ao completar a 3ª missão"). Assim quem
  falta não é punido — o ovo espera o número de missões, não o calendário.
- **Estágios visíveis e colecionáveis:** ovo → ovo rachado → filhote → criança-Docinho
  → formas maiores. Cada evolução é uma **cena-recompensa curta** (festa, voz, confete
  do motor) e destrava uma pose/truque novo.
- **Reusa o motor de sprites** (poses/idle/squash da ESPINHA §3): o Docinho anda ao
  lado dela na rua, boceja no idle, comemora no acerto.
- **NUNCA adoece, nunca morre, nunca fica triste por ausência** (isso é dark pattern
  clássico de Tamagotchi — proibido, seção 4). Se a criança sumiu, ao voltar o Docinho
  "estava cochilando esperando" e acorda feliz. Zero culpa.
- **Vestível** pela Loja (2.3): chapéus, laços, óculos — só cosmético.

### 2.2 Coleção / **Álbum de Figurinhas do Mundo** [PARCIAL JÁ DÁ / PÓS-SAVE p/ persistir]
O pilar "coleção" (IDEIA §2, pilar 4) virado em álbum de caderninho no HUD.
- **Uma figurinha por descoberta:** cada NPC ajudado, cada loja aberta, cada clima raro
  visto (arco-íris, trovoada), cada evento do calendário, cada evolução do Docinho.
- **Raridade sem loot box:** comum (NPCs/lojas), especial (climas raros), lendária
  (eventos/aniversário). A raridade vem de **fazer coisas no mundo**, nunca de sorteio
  pago — nada de caixa-surpresa viciante (seção 4).
- **Repetida vira moeda:** figurinha que a criança já tem, ao reencontrar, converte em
  algumas moedas — sempre há ganho, nunca frustração.
- **Custo baixo:** reusa as **cartelas Gemini dos mascotes/lojas que já existem**; a
  figurinha é o mesmo PNG num quadro do álbum. O álbum é HTML/CSS leve.
- **Meta longa saudável:** completar o álbum do bairro = um selo grande, mas o álbum é
  generoso — dá pra completar jogando normal, sem grind.

### 2.3 Moedas + **Bazar do Docinho** (loja de recompensas) [PÓS-SAVE]
Economia de verdade (pilar 4), **100% cosmética — nada de pay-to-win**.
- **Ganha moedas** nas missões (motor já cospe moedas voando). Ganha extra ao converter
  figurinhas repetidas e em eventos.
- **Gasta em três prateleiras:**
  1. **Roupinhas do Docinho** — chapéu, laço, óculos, cachecol, capa. O item mais
     desejado das crianças pequenas (elas amam vestir o bichinho).
  2. **O Cantinho dela** — um pedacinho da rua que é SÓ dela (a "casinha/vitrine do
     Docinho"): tapete, plantinha, placa com o nome, cor da parede. Territorialidade =
     apego. Reusa assets de decoração como stickers posicionáveis.
  3. **Enfeites do álbum e da fala** — moldura do álbum, cor do balão de fala, carimbo
     favorito.
- **Curva de desejo saudável:** itens baratinhos logo cedo (sensação de "já consigo
  comprar algo na 1ª aula") + alguns itens "dos sonhos" mais caros como meta de longo
  prazo. **Sem escassez artificial** ("só hoje!") e **sem item que dá vantagem no
  aprendizado** (senão comprar vira obrigação, não prazer).

### 2.4 Eventos de calendário [PARCIAL JÁ DÁ / melhor PÓS-SAVE]
O mundo tem vida própria no tempo — mas **sem punir quem não estava lá**.
- **Sexta: Chuva de Doces** — a praça enche de doces caindo (reusa motor de partículas
  como confete), NPCs comemoram, uma **figurinha "Sexta Doce"**. **Anti-punição:** o
  bônus do evento **não é exclusivo do dia**; quem faltou na sexta encontra, na próxima
  entrada, a mesma figurinha com o recado "guardei um docinho pra você". Ninguém perde
  por não ter vindo no dia certo.
- **Aniversário do aluno** (data no cadastro do professor, ESPINHA): o mundo faz festa
  no dia OU na 1ª entrada depois — bolo na praça, NPCs cantam (voz gravada), Docinho
  ganha chapéu de festa e a **figurinha "Aniversário" lendária**. Momento mágico, custo
  quase zero.
- **Estações e datas escolares:** a rua troca a decoração (junina, dia das crianças,
  natal). **Dezembro = final épico do ano + certificado** (já previsto na IDEIA §3).
- **Regra:** todo evento é **oportunidade extra que espera a criança**, nunca uma janela
  que fecha e castiga.

### 2.5 O **mistério visível-mas-trancado** (a ponte / o bairro ao longe) [JÁ DÁ p/ o visual]
O maior puxador de curiosidade do jogo (IDEIA §2). Já é a arquitetura oficial.
- **Visível desde o 1º dia:** o bairro seguinte aparece ao longe no parallax de fundo,
  com a **ponte quebrada** no meio. A criança VÊ o futuro e quer chegar lá.
- **Cada missão constrói um pedaço** (a barra de progresso disfarçada de obra: +1 tábua,
  +1 tijolo, com som de martelo). Quando completa, o bairro **"amanhece aberto"** — tema
  novo, conteúdo do bimestre novo, no mesmo link.
- **Mistérios pequenos espalhados** (fractal do grande): uma porta com cadeado ("volto
  quando você tiver 5 figurinhas"), um baú na praça, o topo da montanha, uma sombra na
  janela. Cada um é uma perguntinha visual que a cabeça da criança quer responder.
- **Curiosidade > obrigação:** o trancado é convite ("o que será que tem ali?"), nunca
  muro punitivo. Sempre há caminho para destravar jogando normal.

---

## 3. RITUAIS DE AULA (o professor Marcos conduz)

Rituais transformam "abrir um site" em "cerimônia da turma". Baratos, curtos, marcantes.

### Abertura — **"O MUNDO ACORDA"** (~1 min, coletivo)
- Marcos projeta ou dá o start; cada criança entra pelo login.
- Ao entrar, uma **cena de despertar**: o mundo passa de noite para dia, o galo canta
  (Web Audio), as luzes das lojas apagam, os NPCs saem de casa, o **Docinho boceja e se
  espreguiça** (idle do motor). Voz: "Bom dia! O mundo acordou pra você."
- **Mural da turma (não ranking):** aparece a meta coletiva do dia — "Hoje a turma vai
  colocar 20 tábuas na ponte, JUNTOS". Cria pertencimento sem comparar crianças.
- Efeito: sincroniza a turma, foca, e já planta o objetivo do dia.

### Fechamento — **"ATÉ AMANHÃ!"** (~2 min, ritual físico jogo↔caderno)
- Faltando poucos minutos, **o mundo entardece sozinho** (sino da escola dentro do jogo,
  céu alaranjado). Sinaliza o fim SEM cronômetro estressante — é poético, não pressão.
- O **Docinho acena "tchau!"** e aparece a **plaquinha com a senha de save do dia**
  (ex.: `PÃO-42` — estepe do login, IDEIA §4) mais um **selo/carimbo do dia** (12
  carimbos girando ao longo do ano).
- **Ritual do caderno:** a criança copia a senha e desenha o carimbo do dia no caderno.
  Isso (a) garante o save de reserva, (b) conecta jogo↔caderno↔casa (leva o mundo pra
  fora da tela), (c) vira um **colecionável físico** (a página de carimbos do ano).
- Última fala: **o gancho da próxima aula** (batida 6 do loop) — "Semana que vem o ovo
  choca! Até amanhã!". A criança sai com uma promessa na cabeça, não com uma cobrança.

---

## 4. O QUE NUNCA FAZER (linhas vermelhas — é escola pública, criança pequena)

- **NUNCA pressão de tempo excessiva.** Sem cronômetro que estressa, sem "corra ou
  perde". Se existir tempo, é **desafio-bônus opcional**, nunca porta obrigatória. O
  mundo espera a criança pensar — o valor pedagógico está na manipulação concreta, não
  na velocidade.
- **NUNCA ranking público humilhante.** Nada de lista "1º João... último Maria". Toda
  comparação é **só consigo mesma** (você-de-hoje vs você-de-antes) e a única coisa
  coletiva é a **meta da turma construída junto** (cooperação, não competição). Expor a
  criança mais lenta na frente dos colegas é proibido.
- **NUNCA recompensa por assiduidade que pune quem faltou.** Sem "streak" que zera, sem
  "você perdeu tudo por não vir", sem ovo/Docinho que adoece ou morre por ausência
  (dark pattern clássico — banido). Faltar é normal na vida de criança pobre (doença,
  transporte, chuva). **O mundo GUARDA tudo e recebe de volta com festa**, nunca com
  culpa. Eventos perdidos ficam disponíveis no retorno.
- **NUNCA loot box / caixa-surpresa viciante.** Raridade vem de **agir no mundo**, nunca
  de sorteio. Sem gancho de aleatoriedade compulsiva.
- **NUNCA pay-to-win.** Moeda só compra cosmético. Nada comprável dá vantagem no
  aprendizado — senão comprar deixa de ser prazer e vira obrigação/ansiedade.
- **NUNCA escassez falsa ou notificação de culpa.** Sem "só nas próximas 2h!", sem
  lembrete que envergonha, sem comparar o bichinho de uma criança com o de outra ("o do
  fulano é maior").
- **NUNCA esconder progresso pra forçar grind.** Progresso sempre visível e honesto.

> Bússola: **se um sistema depende de MEDO (de perder, de ficar atrás, de decepcionar o
> bichinho) para funcionar, ele está errado.** Aqui o motor é CURIOSIDADE, PERTENCIMENTO
> e ORGULHO do que construiu. Só isso.

---

## 5. DEZ IDEIAS BARATAS DE SURPRESA E DELEITE (P de custo — reusam o motor)

Todas ES5, sem asset pesado novo, reusando sprites/partículas/Web Audio/clima que já
existem. Deleite é o que faz a criança **contar pro colega** — marketing orgânico.

1. **O NPC lembra o nome dela — E FALA O NOME EM VOZ ALTA.** ✅ **FEITO (upgrade jul/2026)**
   No balão o primeiro nome aparece no texto E o personagem **fala o nome de verdade**
   na voz do Antonio (não mais só genérico): banco de **124 nomes gravados** (edge-tts,
   `eduverse/vozes/nomes/`) + helper reutilizável `eduverse/lib/voz-nome.js`. Nome fora
   do banco cai no texto + saudação genérica. Voz SEMPRE por API, **nunca a do navegador**.
   Melhor ainda: com o cadastro no Firebase dá pra gerar o áudio EXATO de cada aluno da
   turma (100% de cobertura). Sensação enorme, custo quase zero. Referência: `_voxel`.
   **→ Padrão obrigatório em todo projeto** (ver `EDUCAVERSO-CHECKLIST-DE-CENA.md`). [FEITO/reutilizável]
2. **Arco-íris surpresa.** Raramente, depois da chuva do motor, um arco-íris (gradiente
   CSS + um PNG) cruza o céu e solta a **figurinha rara "Arco-íris"**. [JÁ DÁ]
3. **Docinho imita o clima.** Chovendo, ele abre uma guarda-chuvinha; no frio/neve, põe
   cachecol (reusa o sistema de roupinha, troca automática). Vida = detalhe. [PÓS-SAVE]
4. **A criaturinha que passa.** Um passarinho/gato cruza a tela de vez em quando; se a
   criança tocar, solta 1 moeda e um "piu". Reusa motor de sprite + partícula. [JÁ DÁ]
5. **O bilhete do NPC.** Ao voltar, um NPC deixou um recado curtinho gravado ("Senti sua
   falta! Volte quando quiser."). Humaniza o retorno SEM punir a ausência. [PÓS-SAVE]
6. **Easter egg do sol.** Tocar 5x no sol e ele sorri e chove confete (Web Audio +
   confete já existem). Segredo que vira lenda no recreio. [JÁ DÁ]
7. **A vitrine do dia.** A vitrine mostra um doce diferente por dia da semana (mesmo
   asset, rótulo trocado): "hoje tem cupcake!". Micro-novidade constante, custo zero.
   [JÁ DÁ]
8. **O truque do Docinho.** Cada evolução destrava um truque (cambalhota, piscar, dar a
   patinha); a criança toca nele e ele executa. Reusa poses de sprite. [PÓS-SAVE]
9. **O carimbo do dia.** 12 selos girando ao longo do ano no fechamento (seção 3):
   colecionável no caderno físico, custo = 12 desenhinhos. Liga jogo↔caderno. [JÁ DÁ]
10. **A estrela cadente.** Às vezes, ao fim de uma missão, uma estrela cadente cruza o
    céu e a voz diz "faça um pedido!" (só visual + som). Reforço emocional gratuito. [JÁ DÁ]

> **Bônus 11 — Foto do mundo:** um botão "tirar foto" põe uma moldura bonita sobre a
> cena atual (overlay CSS, sem salvar arquivo pesado) pra criança mostrar orgulhosa o
> lugar dela. Orgulho é o melhor engajamento — e é de graça. [JÁ DÁ]

---

## ORDEM SUGERIDA (encaixa na ESPINHA §8, sem reprometer nada)

1. **Já, com o motor atual [JÁ DÁ]:** deltas de retorno (clima/vitrine do dia), mistério
   visível ao fundo, easter eggs 2/4/6/7/10/11, ritual de abertura/fechamento com senha
   de save. Barato e transforma a sensação hoje.
2. **Depois da Fatia 1 (login+save):** álbum de figurinhas persistente, nome no NPC,
   bilhete de retorno, mural da turma, moedas que sobrevivem entre aulas.
3. **Depois da Fatia 2 (ovo/Docinho):** evolução por marco, roupinhas, Bazar do Docinho,
   Docinho que imita o clima, truques, aniversário.
4. **Com os bairros por bimestre:** a ponte que abre o bairro novo vira o arco emocional
   grande do ano, fechando em dezembro com o final épico + certificado.

> Regra que atravessa tudo: **motivar por curiosidade, pertencimento e orgulho — nunca
> por medo de perder.** É isso que faz a criança querer voltar e faz o Marcos se
> destacar sem trair a ética de escola pública.
