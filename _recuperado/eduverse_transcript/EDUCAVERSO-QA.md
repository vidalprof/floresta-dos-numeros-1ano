# ✅ EDUCAVERSO-QA — Protocolo de qualidade (para nenhuma atividade sair errada)

> **Regra:** TODA atividade passa por este protocolo **antes** de chegar ao Marcos.
> Nada de "entregar e ver depois". Ancorado nas *lições pagas* do `MANUAL-MESTRE.md`
> e no ritual desta era: **nunca afirmar que funciona sem testar**.

---

## Os PORTÕES (nesta ordem — não pular)

### 🌱 Portão 0 — FILOSOFIA (a atividade É EduVerse? — ver `EDUVERSE-FILOSOFIA.md`)
Antes de qualquer código, a missão passa por este crivo. Se falhar, **redesenhar** — não codar.
- [ ] Começa com um **problema do mundo** (história), **nunca** com o conteúdo/pergunta.
- [ ] O conhecimento é **ferramenta** que resolve o problema, **nunca obstáculo/tranca**.
- [ ] Aluno **age/constrói/experimenta ANTES** de qualquer conceito; o **padrão** emerge da ação.
- [ ] O **conceito escolar é nomeado por ÚLTIMO** (de leve) + **Reflexão** no fim.
- [ ] **Byte pergunta** ("o que você percebe?", "tem jeito mais rápido?", "achou um padrão?") —
      nunca "qual é a resposta?" nem "faça X".
- [ ] **NÃO** é prova disfarçada: sem pergunta-para-abrir-porta, sem X vermelho, sem alternativa.
- [ ] Segue o arco: História → Exploração → Problema → Experimentação → Descoberta → Conceito →
      Aplicação → Reflexão (nunca invertido).
- [ ] No fim o aluno diria "hoje **ajudei/construí/salvei/descobri**", e só depois "…aprendi X".

## Os 3 PORTÕES seguintes (nesta ordem — não pular)

### 🔧 Portão 1 — VERIFICAR (a máquina prova que funciona)
- [ ] `node --check` em todo o JavaScript extraído — **zero** erro de sintaxe.
- [ ] Renderiza no Chromium headless **sem erro** (a tela aparece; não fica preta).
- [ ] **Dirigir a mecânica de verdade** (não presumir): injetar a solução e renderizar o
      resultado — o personagem anda, a fase completa, a vitória dispara. *(Foi assim que
      testamos o Jardim e as Placas: montamos o caminho e vimos o boneco andar.)*
- [ ] **Rajada de screenshots** (6–10 espaçados ~150ms) durante o movimento — conferir que
      **nada pisca, nada trava, o passo não patina**, a respiração está presente.
- [ ] **Autossuficiente e leve:** abre offline (assets em base64), roda em navegador antigo,
      sem `console error`, sem depender de arquivo externo.

### 🕵️ Portão 2 — AUDITAR (o cético confere contra a lista)
Um passe cético — de preferência **um agente separado** — confere item a item:

**Visual / arte**
- [ ] TODO asset-chave é **imagem gerada por IA** — NUNCA desenho de código para
      casa/prop/personagem/cenário. *(Lição paga: a casinha de código ficou amadora.)*
- [ ] Recorte limpo: **fundo transparente de verdade**, sem franja branca, sem sombra na base.
- [ ] **Estilo consistente** entre os assets (mesma "cara" cartoon premium pintada à mão).
- [ ] **Animações de verdade:** respiração no idle, andar suave, clima, luz, vento, água — o
      mundo **VIVO** (idêntico ao padrão premium de antes, só que 2D/tile).
- [ ] **Imagens NÃO se sobrepõem indevidamente** *(lição paga do Marcos)*: ordenação por
      profundidade (**y-sort**) correta; sprites **ancorados nos pés** e dimensionados pela
      **ALTURA** (não estouram a célula/container); o **balão de fala não cobre o personagem**;
      no **labirinto**, o muro não esconde o Byte no corredor; personagem/jaula/props não se
      tampam. Conferir renderizando cada tela e cada momento.

**Mecânica**
- [ ] Funciona ponta a ponta; o **gating** trava até o objetivo ser cumprido.
- [ ] **Erro = consequência** no mundo (nunca X vermelho).
- [ ] Colisão certa (não atravessa parede/árvore/personagem).

**Pedagogia**
- [ ] Aprende **SEM perceber** (jogo primeiro, lição nunca explícita).
- [ ] Aluno **ATIVO / constrói** (não escolhe alternativa).
- [ ] **Entrega o objetivo do currículo** escolhido; **adequado à FAIXA** da turma.
- [ ] Não-leitores: ícone + voz + cor, tudo narrado; a **narração NÃO entrega a resposta**
      (lê só o enunciado; a explicação vem depois da ação).

**Língua**
- [ ] Português impecável: acentos, concordância (n=1), sem símbolo/pontuação lido pelo TTS.

### 👨‍🏫 Portão 3 — APROVAÇÃO DO PROFESSOR (o gate humano)
As **3 aprovações do Marcos**: (1) as missões/pedagogia, (2) a arte, (3) o mundo jogável.
Só publica **depois** das três.

---

## Regras permanentes (nunca esquecer)
1. **Sincronizar com o GitHub antes de agir** (hook `sync-remoto.sh` + `MEMORIA-DO-PROJETO.md`).
2. **Geração de imagem/áudio é por workflow** (Gemini/Pollinations/edge-tts), nunca pelo chat.
3. **Tudo que a criança vê é IA** — nunca prop/personagem de código.
4. Se algo sai **duro, feio ou errado** depois de 2 tentativas: **PARAR e perguntar / elevar o
   modelo**, não empurrar torto.
5. **Documento vivo:** a cada teste, mover a tabela CONSTRUÍDO×A-FAZER e **anotar a lição paga**.

> Como usar: rodar o Portão 1 e 2 em cada entrega; registrar aqui (ou no commit) o que passou e
> o que ficou pendente; só levar ao Marcos o que passou nos dois. O Portão 3 é dele.
