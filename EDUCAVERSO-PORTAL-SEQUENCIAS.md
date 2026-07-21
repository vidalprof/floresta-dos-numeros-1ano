# EducaVerso PORTAL — sequências didáticas por turma + progresso do aluno (plano 2026-07-21)

> Pedido do Marcos: o site EducaVerso profissional no MESMO molde do app das atividades;
> as atividades entram em SEQUÊNCIAS DIDÁTICAS por turma; o aluno entra, realiza e tem o
> seu progresso; o cadastro é AUTOMÁTICO quando o aluno digita nome+turma (sem o professor
> cadastrar). Problema a resolver junto com ele: nome/turma digitados errados.

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

## 2. O PORTAL (evolução do hub, no molde premium)
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

## 4. FASES DE ENTREGA (proposta)
1. ✅ (hoje) Padrão de identidade + parecer consolidado + impressão na Fábrica de Estrelas.
2. Portal v1: home + turmas + 1 sequência do 3º ano (Fábrica de Estrelas + Vila da
   Tabuada) lendo progresso local; molde visual premium.
3. Firebase ligado → sincronização de alunos/pareceres/progresso + painel único.
4. Ferramenta de reconciliação (juntar/renomear) no painel.
5. Replicar o padrão nas atividades antigas (cada uma adota edu_* + parecer padrão).
