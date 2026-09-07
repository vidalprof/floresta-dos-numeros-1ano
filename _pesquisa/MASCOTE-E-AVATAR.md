# 🎭 MASCOTE E AVATAR — funcionam? O que a evidência diz e o que mudou no motor (set/2026)

> Pedido do Marcos (2026-09-07): *"faça uma pesquisa para ver se esse negócio de mascote
> e avatar funciona, melhore tudo que pode ser melhorado"*.
>
> Fontes trazidas pelo `pesquisar.yml` (6 rodadas; 2 voltaram vazias por paywall —
> ScienceDirect, SAGE e ResearchGate devolvem 403 ao robô): `_pesquisa/web/mascote-
> agente-pedagogico-fontes-abertas.md` (Wikipedia "Pedagogical agent" + ERIC EJ1333173),
> `mascote-parassocial-fontes-abertas.md` (Wikipedia "Parasocial interaction" + o estudo
> de Calvert/Georgetown com a Dora), `avatar-criancas-motivacao-evidencia.md` (PMC sobre
> efeito Proteus; estudo com 48 crianças de 8–13 sobre avatares em Roblox/Minecraft),
> `modelos-de-app-infantil-navegacao.md` (UX de apps infantis; caso Duolingo).
> Onde eu completo com o que sei das meta-análises (Schroeder, Adesope & Gilbert 2013;
> Castro-Alonso et al. 2021), está marcado como **[memória, não lido hoje]**.

---

## 1. Mascote (agente pedagógico): funciona — MAS só de um jeito

**O que a evidência diz**

- Meta-análises do agente pedagógico acham efeito **pequeno e positivo** (g ≈ 0,2)
  sobre aprendizagem **[memória, não lido hoje]**; a própria Wikipedia resume: "melhora
  negligenciável... mais trabalho é necessário". Ou seja: **mascote por si só não
  ensina.**
- **Mayer:** o agente ajuda "**apenas como apresentador de pistas sociais**" — e a função
  que comprovadamente ajuda é a **SINALIZAÇÃO**: apontar o que importa na tela. Agente
  que vira o centro da atenção **aumenta a carga cognitiva** (a criança olha o boneco,
  não a tarefa).
- **ERIC EJ1333173 (2022):** agente **com olhar e gesto** (gaze + gesture) melhorou
  resultados e a atividade cerebral ligada à atenção — o corpo do personagem tem que
  apontar para o conteúdo, não dançar.
- **Estático × animado:** resultados mistos. Animação só vale quando **carrega
  informação** (aponta, reage); animação de enfeite é neutra ou pior.
- **Afeto:** agentes que **respondem ao estado da criança** (frustração, hesitação)
  melhoraram retenção, motivação e autoeficácia.
- **Calvert (Georgetown, 217 crianças de 3–6 anos, personagem Dora):** quem tinha
  **vínculo emocional** com o personagem e **conversava** com ele sobre matemática
  respondeu mais rápido e mais certo; e **transferiu** o aprendido para objetos reais
  melhor quando (a) havia um **personagem encarnado** (não só a voz) e (b) o personagem
  dava **respostas CONTINGENTES** ao que a criança fazia. Voz sem personagem transferiu
  menos.
- **Parassocial:** o vínculo com personagem de mídia se forma cedo e cresce com a
  **repetição de encontros** — é o que faz PBS Kids e Noggin usarem sempre os mesmos
  personagens como guias ("um amigo de confiança apresentando o novo reduz a ansiedade").

**Veredito:** o mascote funciona quando é **guia que aponta e responde**, e atrapalha
quando é **enfeite que chama atenção**. A casa já estava do lado certo em quase tudo
(mascote pequeno na fase, fala em pergunta, inclina quando ela hesita, festeja só no
acerto, `nada anima sem função` medido pela regra 12). O que faltava está abaixo.

**O que mudou no motor hoje (set/2026)**

1. **Sinalização na dica:** quando a dica entra (`mostraDica`), o mascote se **inclina
   para o conteúdo** (a pose "estou aqui" da hesitação) e volta sozinho em 2,6 s.
2. **Contingência com nome:** o texto flutuante do acerto passa a trazer o **nome da
   criança** uma em cada três vezes ("Boa, Ana!"). A voz é gravada e não sabe o nome —
   por isso é escrito, e a criança reconhece o próprio nome antes de ler qualquer coisa.
3. (já existia e fica registrado como regra) o mascote **hesita junto**: 8 s sem toque →
   inclina e a dica aparece, sem responder por ela.

**Regras que ficam (para toda atividade)**

- O mascote **aponta, pergunta e reage**; nunca explica sozinho, nunca dança durante a
  tarefa. Animação em laço só na capa e na medalha.
- **Mesmo personagem para a mesma turma**, atividade após atividade: o vínculo
  parassocial é acumulativo (Coru no 1º ano, Fubá na Padaria é a exceção que já existe;
  daqui para a frente, **reusar** — é também a regra do banco de imagens).
- Toda resposta do mascote é **contingente ao que ela fez** ("você pôs 7, falta 1"),
  nunca genérica. O andaime em 3 degraus já é assim; os elogios agora também.
- **Encarnado, não só voz:** a voz da casa sempre sai de um personagem visível — é o que
  fez a transferência no estudo de Calvert.

## 2. Avatar (crachá): funciona — se ela se VÊ

**O que a evidência diz**

- Crianças de 8–13 fazem avatar para **se representar**, **experimentar outro eu**,
  **pertencer** ao grupo e melhorar no jogo; e sofrem o **"efeito guarda-roupa"**:
  acumulam muitos, usam um favorito. Personalizar aumenta **identificação, motivação e
  flow** (revisão do efeito Proteus). O mesmo estudo alerta: em jogo comercial, a
  personalização vira gancho de **compra** — nada disso cabe na casa.
- Autonomia (escolher) é uma das três necessidades de Deci & Ryan que a casa já adota;
  o crachá é a forma mais barata de dar autonomia real.
- UX infantil: **ícones de perfil coloridos** ajudam a criança a achar "o meu" de
  imediato e evitam toque errado.

**Veredito:** o crachá funciona, mas hoje a criança o escolhia na 2ª tela e **só o
revia na medalha**. Avatar invisível não identifica ninguém.

**O que mudou no motor hoje**

4. **O crachá viaja junto:** um chip pequeno com a figura escolhida e o primeiro nome
   fica ao lado da barra de progresso em toda fase (`.pgeu`); em tela de 320 px fica só
   a figura. Não é alvo de toque.

**Regras que ficam**

- Crachá **sempre visível** na viagem; nunca só na medalha.
- Poucos crachás (4–6), **variados** (tons de pele/cabelo, ao menos um loiro), retrato do
  peito para cima. Não é guarda-roupa: escolher é um toque, e acabou.
- **Nunca** moeda, loja ou item para ganhar: o avatar é identidade, não recompensa.

## 3. O que NÃO fazer (a evidência também diz)

- Mascote grande no meio da tela durante a tarefa (carga cognitiva).
- Mascote que fala o tempo todo (a fala compete com a narração do conteúdo).
- Trocar de mascote a cada atividade (zera o vínculo).
- Avatar "sexy" ou humano realista: a pesquisa de aparência vale para adultos e não
  transfere; para criança o que vale é **coerente com a história** e **reconhecível a
  62 px**.
- Ranking, moeda, vida — em mascote, avatar ou casca.

## 4. O que ainda não medimos

- **Efeito do chip do crachá** na permanência: só se mede na escola (o Marcos observando
  se a criança olha para ele). Instrumentação possível: contar toques no chip.
- **Contingência falada:** só com voz sintetizada em tempo real, que a casa proíbe
  (voz-robô). Fica no texto.
- Se o mascote **apontar** com a mão (arte com braço estendido) melhora mais que
  inclinar: exige uma pose a mais por mascote — só com o gerador pago editando a base.
