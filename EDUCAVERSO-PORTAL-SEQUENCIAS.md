# EducaVerso PORTAL — sequências didáticas por turma + progresso do aluno (plano 2026-07-21)

## ⚠️⚠️ VIRADA DE RUMO (Marcos, 2026-07-21 noite) — LER PRIMEIRO
**O modelo NOVO NÃO é mais o site com HUB + MUNDOS VIVOS + OVO/MASCOTE-token** (aquele
descrito nas seções antigas abaixo, decisão de 17/07). Marcos decidiu: as atividades são
**APPS PREMIUM** (padrão Fábrica de Estrelas + melhorias + pesquisa), cada uma no seu link,
e o **PORTAL é algo NOVO e DIFERENCIADO** cuja função é **organizar as atividades nas TURMAS
certas** — o aluno entra na turma dele e joga as atividades dela; o professor organiza e
acompanha. Nada de decoração de mundos/mascote-token. As seções antigas (2, 2b, EduMundo,
ovo→mascote) ficam só como HISTÓRICO — não são mais o plano. O formato exato do portal novo
está sendo desenhado com o Marcos + a pesquisa profunda em andamento.

> Pedido do Marcos: o site EducaVerso profissional no MESMO molde do app das atividades;
> as atividades entram em SEQUÊNCIAS DIDÁTICAS por turma; o aluno entra, realiza e tem o
> seu progresso; o cadastro é AUTOMÁTICO quando o aluno digita nome+turma (sem o professor
> cadastrar). Problema a resolver junto com ele: nome/turma digitados errados.

## 0. DECISÃO-CHAVE (Marcos, 2026-07-21 noite): IDENTIDADE É O ALICERCE DA MEDIÇÃO
Marcos cravou: **link anônimo NÃO serve p/ valer** — sem o aluno amarrado ao nome certo, a
medição de aprendizagem e o registro no banco não têm valor. Logo, a pergunta NÃO é "portal
sim/não" e sim **"onde o aluno se identifica"**. Como todas as atividades moram no mesmo
domínio, **1 identificação vale p/ todas** (herdam via edu_atual / Firebase). O mínimo real =
uma **PORTA DE ENTRADA DE IDENTIDADE** (é a semente do portal, enxuta).

**Para medir de verdade, 3 obrigatórios (com ou sem portal bonito):**
1. **Lista da secretaria por turma** → aluno TOCA no nome (zero digitação = zero erro de grafia).
2. **Trava de pessoa certa = FIGURINHA/PIN SECRETO** (Marcos ESCOLHEU isto p/ valer):
   anos iniciais = figurinha secreta (desenho, sem leitura); anos finais = PIN de 4 números.
   1ª vez cria; depois só ELE entra no próprio nome. Professor VÊ/RESETA no painel se esquecer.
3. **Firebase ligado** (2 cliques do console) → grava no banco, junta a turma, cruza aparelhos.

**Estado atual:** identidade DORMENTE (IDENTIDADE_ATIVA=false) = bom só p/ Marcos TESTAR por
link anônimo. Vira real quando: Marcos manda a LISTA + faz os 2 cliques do Firebase → eu ligo
a porta de entrada (turma → nome → figurinha/PIN) + gravação no banco. NÃO construir antes
desses 2 insumos (evita retrabalho/credito à toa; a pesquisa profunda pode afinar o desenho).

## 1. A base JÁ EXISTE (implantada hoje na Fábrica de Estrelas — é o PADRÃO)
- **Identidade compartilhada `edu_*`** no localStorage do domínio `vidalprof.github.io`:
  como TODAS as atividades moram no mesmo domínio, elas **compartilham** o mesmo
  localStorage. Chaves padrão: `edu_alunos` (registro), `edu_atual` (quem joga),
  `edu_pareceres` (parecer de cada atividade, com alunoId/turma/slug).
- **Tela "Quem vai jogar?"** (1º acesso digita 1 vez; depois é só TOCAR no nome —
  pesquisa: criança pequena não digita bem; roster-tap é o padrão das plataformas K-2).
- **Anti-duplicata**: turma NUNCA é digitada (botões); nome passa por normalização
  (minúsculas, sem acento, espaços) + fuzzy Levenshtein ≤2 na mesma turma →
  "Você é a Sofia? [Sou eu] [Não]" antes de criar registro novo.
- Cada atividade grava dados POR ALUNO (`kAluno()`): motor BKT, evidências, retenção.

## 2. O PORTAL = o SITE EDUCAVERSO (CORREÇÃO do Marcos: NÃO é o hub Ilhas do Saber!)
O modelo novo já tem os DOIS sites próprios (decisão de 2026-07-17, na memória):
- **EducaVerso** (`vidalprof.github.io/educaverso/`) = o site do ALUNO: link da turma
  (`?t=<turmaId>`), toca no card nome+avatar (zero digitação), ovo→mascote Verso,
  MUNDOS VIVOS com paradas lidas do CATÁLOGO no Firebase (/catalogo/mundos). As
  SEQUÊNCIAS DIDÁTICAS = os mundos/paradas; atividade nova entra pelo catálogo (link
  próprio, portal leve), progresso em /turmas/<t>/alunos/<a>.
- **painel-prof** (`vidalprof.github.io/painel-prof/`) = site SEPARADO do professor,
  com senha, invisível pro aluno: cadastra turmas+alunos (lista da secretaria!),
  acompanha progresso; deve ganhar as avaliações consolidadas/impressão + a
  ferramenta VER/RESETAR a figurinha-secreta/PIN de cada aluno (decisão 2026-07-21:
  aluno esqueceu -> professor vê ou reseta no painel).
- O hub Ilhas do Saber fica pro acervo ANTIGO; nada do modelo novo entra lá.
- O que a Fábrica de Estrelas ganhou hoje (edu_* local, ?painel) vira o modo
  OFFLINE/fallback por aparelho; a fonte da verdade do modelo novo é o Firebase.

## 2b. (texto anterior, mantido como referência do molde visual)
- **Home**: céu/identidade visual do molde (motion, mascote, som), mapa de TURMAS.
- **Turma** → **SEQUÊNCIA DIDÁTICA**: trilha ordenada de atividades (como o mapa de
  paradas da Fábrica de Estrelas, mas cada nó = uma ATIVIDADE completa, com link).
  Ordem pedagógica definida pelo Marcos + pedagogo (BNCC da turma).
- **Progresso do aluno**: o portal LÊ `edu_pareceres`/`edu_alunos` e acende os nós
  concluídos daquele aluno (funciona HOJE por aparelho, sem backend). O aluno toca o
  nome ao entrar no portal e a escolha vale para todas as atividades (edu_atual).
- **Arquitetura continua PORTAL LEVE**: o portal só aponta links; cada atividade no seu
  repo (regra de ouro do CLAUDE.md — o build nunca engasga).

## 3. CADASTRO AUTOMÁTICO no banco (Firebase) — análise do problema "digitou errado"
Camadas de defesa (na ordem):
1. **Não digitar o que dá pra tocar**: turma = botões; nome = digita SÓ na 1ª vez.
2. **Normalizar** antes de comparar/gravar (minúsculas, sem acento, espaços únicos).
3. **Fuzzy na criação** (Levenshtein ≤2 dentro da turma) → confirmação "Você é ...?".
4. **Chave no banco** = `turma + nomeNormalizado` (não o texto cru) → o mesmo aluno em
   aparelhos diferentes cai no MESMO registro sozinho.
5. **Reconciliação do professor** (painel): ferramenta "JUNTAR dois registros" (o certo
   absorve evidências do errado) e "RENOMEAR" — resolve o resto (ex.: "Davi"/"Davih").
6. (Opcional, elimina o problema de vez) **Lista da turma semeada 1x**: o Marcos manda
   os nomes; primeira tela vira só-toque, sem digitação nenhuma. O item 47 do backlog
   do vila-tabuada já esperava essa lista.
- **Sem Firebase**: tudo acima funciona por aparelho. **Com Firebase** (2 cliques do
  console — FIREBASE-EDUCAVERSO.md): `edu_alunos`/`edu_pareceres` sobem via login
  anônimo (mesmo modelo do evidencias.ts do vila-tabuada) → turma inteira em qualquer
  aparelho, painel único do professor, avaliação consolidada imprimível de todos.

## 3½. ADEQUAÇÃO POR IDADE (correção do Marcos: é do PRÉ ao 9º ANO — 2026-07-21)
O sistema atende as 3 faixas do hub (Tesouro=pré/1º/2º · Exploradores=3º/4º/5º ·
Aventureiros=6º–9º). O molde ganha um **perfil de idade** por atividade:
- **IDENTIFICAÇÃO:** pré–2º = lista narrada (mascote fala) + FIGURINHA secreta com
  desenhos (padrão pré-K, zero leitura; professora ajuda no pré) · 3º–5º = lista +
  figurinha secreta · 6º–9º = **PIN de 4 dígitos** criado pelo aluno (figurinha
  infantiliza adolescente), visual sóbrio.
- **CASCA por faixa:** Tesouro = tudo narrado, botões por ícone, alvos enormes, sem
  streak/nota visível · Exploradores = formato atual (Fábrica de Estrelas) ·
  Aventureiros = menos fofura, mais desafio/agência, gamificação sóbria, texto ok.
- **AVALIAÇÃO:** parecer descritivo puro nos anos iniciais; nos finais a nota entra
  naturalmente (LDB/rubricas).
- **O que NÃO muda:** registro de alunos (aceita qualquer turma), motor adaptativo
  (BKT/Leitner), evidências→parecer→consolidada — a base é a mesma do pré ao 9º.

## 4. FASES DE ENTREGA (proposta)
1. ✅ (hoje) Padrão de identidade + parecer consolidado + impressão na Fábrica de Estrelas.
2. Portal v1: home + turmas + 1 sequência do 3º ano (Fábrica de Estrelas + Vila da
   Tabuada) lendo progresso local; molde visual premium.
3. Firebase ligado → sincronização de alunos/pareceres/progresso + painel único.
4. Ferramenta de reconciliação (juntar/renomear) no painel.
5. Replicar o padrão nas atividades antigas (cada uma adota edu_* + parecer padrão).
