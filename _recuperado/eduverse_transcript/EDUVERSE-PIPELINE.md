# 🏗️ PIPELINE OFICIAL DE CRIAÇÃO DE ATIVIDADES DO EDUVERSE (como construir)

> Trazido pelo Marcos. É a **planta baixa** do EduVerse — a Parte 3 da filosofia
> (`EDUVERSE-FILOSOFIA.md` = por quê / `EDUVERSE-COMPUTACAO.md` = mapa de conceitos /
> **este = COMO construir**). Vale o **Portão 0** do `EDUCAVERSO-QA.md`.

## IDEIA-MÃE
O EduVerse **não cria atividades — cria MUNDOS VIVOS**; a atividade acontece naturalmente
dentro. O estudante nunca sente que "abriu um exercício": entra num lugar que **já existia
antes dele e continua depois** que ele sai.

**NUNCA** começar por perguntas/exercícios/respostas. **SEMPRE** começar por um **MUNDO**.
O conteúdo nasce das **necessidades do mundo**; o conhecimento **resolve** problemas, nunca bloqueia.

## PIPELINE (10 etapas — nunca inverter)
1. **Criar o MUNDO** (ambiente completo). Ex.: Laboratório do Byte, Cidade Digital, Fazenda
   Inteligente, Vale das Máquinas, Castelo dos Inventores, Floresta dos Padrões, Porto dos
   Exploradores, Base Espacial, Museu do Conhecimento, Cidade Sustentável. Perguntar antes de
   tudo: **"como esse lugar funciona?"**
2. **Criar a VIDA do mundo** (vivo mesmo sem o aluno fazer nada): personagens andando, robôs
   trabalhando, animais, vento, árvores balançando, água correndo, nuvens, luzes, trens,
   máquinas, **som ambiente**, mudança de luz, objetos se movendo.
3. **Criar os PERSONAGENS** — cada um com: nome, história, personalidade, objetivo, rotina,
   diálogos, animações, expressões. (Byte: curioso, inteligente, divertido, guia, **nunca
   entrega respostas**. Engenheiro, Carteiro Robô, Cientista, etc.)
4. **Criar a ROTINA dos personagens** — nunca totalmente parados: andar, conversar, esperar,
   transportar caixas, sentar, ler, trabalhar, cumprimentar. Dá sensação de vida própria.
5. **Criar OBJETOS INTELIGENTES** — nada é só decoração; cada objeto tem **função**: porta
   (abre área), computador (inicia missão), livro (dá pista), caixa (transporta), ponte
   (passagem), botão (ativa), máquina (transforma), trem (leva), árvore (recurso).
6. **Criar o PROBLEMA do mundo** — nunca uma pergunta primeiro; um problema real: o robô não
   entrega, a fábrica parou, a ponte caiu, as plantações precisam ser organizadas, o trem se
   perdeu, os animais sumiram, a cidade sem energia. **Agora há motivo pra aprender.**
7. **Fazer o aluno EXPLORAR** (antes de qualquer conceito): andar, observar, conversar,
   experimentar, investigar, coletar pistas, testar, comparar.
8. **Criar a NECESSIDADE** — o aluno sente "preciso descobrir como resolver isso". **Só então**
   apresentar novas ferramentas. Jamais o conteúdo primeiro.
9. **Fazer o CONCEITO nascer naturalmente** — ex.: desenha caminhos p/ o robô; percebe que
   sempre faz andar/andar/virar/pegar/entregar = criou um **algoritmo** sem perceber; depois
   repetição, condição, função.
10. **REFLEXÃO** — só no fim o Byte comenta: "percebeu o que descobrimos? você criou uma
    sequência… usou um algoritmo." O conceito **recebe nome só depois da descoberta**.

## COMO CONSTRUIR OS MAPAS — TILES (LEGO)
Nunca desenhar um cenário inteiro. Montar com **tiles** de tamanho fixo (32×32 / 48×48 / 64×64),
como LEGO. Manter uma **biblioteca de tiles**.
- **Terrenos:** grama, terra, pedra, madeira, água, areia, gelo, estrada, ponte, lava, piso metálico.
- **Objetos:** árvores, flores, arbustos, rochas, placas, postes, computadores, mesas, cadeiras,
  caixas, máquinas, esteiras, portas, janelas, livros, alavancas, botões.
- **Decoração:** nuvens, sombras, luzes, tapetes, quadros, cabos, tubos…

## BIBLIOTECA DE PERSONAGENS (reutilizável — não criar novo a cada atividade)
Byte, Professora, Engenheiro, Robô Carteiro, Robô Construtor, Cientista, Guarda, Agricultor,
Explorador, Crianças, Animais.
**Animações padrão por personagem** (reusadas em centenas de atividades): parado, andar ↑↓←→,
falar, feliz, pensando, comemorando, triste, esperando.

## AMBIENTE VIVO (mesmo parado)
computadores piscam, luzes acendem, ventiladores giram, água corre, árvores balançam, folhas
caem, nuvens passam, fumaça sobe, pássaros voam, robôs trabalham, máquinas giram, trens circulam.

## A IA (eu) GERA sempre que possível
tiles, sprites, objetos, cenários, personagens, animações, efeitos, missões, diálogos, histórias,
sons, descrições — **mantendo o MESMO estilo e identidade visual**.

## EDITOR VISUAL (futuro)
Painel esquerdo (terrenos/objetos/personagens/construções/efeitos/missões) · centro (mapa) ·
painel direito (nome/animação/diálogo/missão/som/evento). Tudo **arrastar e soltar**, sem programar.

## FILOSOFIA VISUAL
Não precisa ser ultrarrealista. Precisa ser: **bonito, consistente, colorido, acolhedor, vivo,
claro, educativo, leve** e **compatível com computadores antigos**.

## TECNOLOGIA
HTML5, CSS3, JavaScript, **Canvas 2D**, sprites, **sprite sheets**, tiles, Firebase.
Compatibilidade: **Windows 7, Chrome/Firefox antigos**, resolução mínima **1024×768**.

## OBJETIVO FINAL
Uma **biblioteca reutilizável**: centenas de tiles, dezenas de personagens, centenas de objetos,
SFX, animações, missões, mundos, cenários, diálogos, eventos. **Nova atividade não é feita do
zero — é MONTADA com peças reutilizáveis (LEGO digital)**; a IA gera novas peças quando preciso,
sempre no mesmo estilo. O EduVerse **não é gerador de exercícios — é construtor de mundos vivos**
onde se aprende por exploração, experimentação, descoberta e resolução de problemas reais.

---
## 🔗 ONDE ESTAMOS (honesto) — ver detalhe na conversa/`MEMORIA-DO-PROJETO.md`
- **Já batemos:** Canvas 2D + tiles via pattern (grama/caminho), leve/offline/compatível,
  mundo vivo (som ambiente + animações), problema-primeiro, Byte-guia, assets IA em estilo
  que aprendemos a **casar** (gerar editando a base).
- **Falta (o LEGO):** uma **biblioteca reutilizável** organizada; **folha de animação do Byte**
  (parado/andar 4 direções/falar/feliz/pensando); tiles catalogados; sprite sheets; editor.
- **Próximo passo que deixa tudo fácil:** montar o **KIT base** (estilo travado → tiles +
  Byte animado + objetos), e passar a **MONTAR** as atividades a partir dele.
