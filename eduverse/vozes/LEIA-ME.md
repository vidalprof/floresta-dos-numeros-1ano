# 🔊 Banco de VOZES DE NOME — o personagem fala o nome do aluno (gancho reutilizável)

> **Padrão EduVerse — obrigatório em TODO projeto** (ver `EDUCAVERSO-CHECKLIST-DE-CENA.md`).
> Ouvir o próprio nome na voz do personagem é um dos ganchos de engajamento mais
> fortes e mais baratos (`_plano/plano_engajamento.md`, ideia #1). Custo ~zero.

## O que é
- **124 nomes comuns de criança** gravados na **voz do Antonio** (`pt-BR-AntonioNeural`,
  edge-tts). Um mp3 por nome: `nome_<slug>.mp3` (~9 KB cada, ~1,2 MB o banco todo).
- **Mestre canônico:** `eduverse/vozes/nomes/` (esta pasta). Lista em `eduverse/vozes/nomes-banco.json`.
- **Helper plug-and-play:** `eduverse/lib/voz-nome.js` (`window.VozNome`).

## Regra de ouro (nunca quebrar)
- **Voz SEMPRE por API (edge-tts, Antonio). NUNCA a voz do navegador** (`SpeechSynthesis`
  é proibida — robótica, inconsistente, não é a identidade do Byte).
- **Nome fora do banco** → cai só no **texto** + **saudação genérica** (com apelido
  "grumete/marujo"). Nome no banco → fala o nome + saudação **sem** apelido (senão vira
  *"Marina!… Ôa, grumete!"*, que soa como duas pessoas).
- **Som só começa após 1 gesto** (clique/toque) — regra do navegador. Como o aluno
  clica pra entrar, esse clique já libera a voz.

## Como plugar num projeto novo (3 passos)
1. **Inclua o helper:** `<script src="voz-nome.js"></script>` (copie de `eduverse/lib/`).
2. **Copie os mp3** pro `audio/` do projeto: `cp eduverse/vozes/nomes/*.mp3 <projeto>/audio/`.
3. **Toque em cadeia** quando o aluno entrar:
   ```js
   var idNome = VozNome.idDe(nome);          // 'nome_marina' ou '' se não tiver
   var saud = idNome ? 'audio/vx_ola_nome' : 'audio/vx_ola';  // sem/ com apelido
   VozNome.cadeia([idNome && 'audio/'+idNome, saud], () => narrarProblema());
   ```
   O `vx_ola_nome` (saudação sem apelido) e o `vx_ola` (genérico) são gravados por
   projeto — o **conteúdo** da saudação muda por atividade, só o **banco de nomes** é
   compartilhado.

## Expandir o banco (nome que faltou)
1. Acrescente em `_lote_falas.json`: `{ "id": "nome_<slug>", "texto": "<Nome>!" }`.
2. Commit com `[audio]` → o workflow `finalizar.yml` gera `_audio/nome_<slug>.mp3` (voz Antonio).
3. `cp _audio/nome_<slug>.mp3 eduverse/vozes/nomes/` (atualiza o mestre) e pro `audio/` do projeto.
4. Atualize o set em `eduverse/lib/voz-nome.js` (e `nomes-banco.json`).

## Melhor ainda: gerar por TURMA (100% de cobertura)
Na atividade de verdade, os nomes vêm do **cadastro no Firebase** (`/turmas/<turma>/alunos`).
Como são conhecidos de antemão, dá pra **gerar o áudio EXATO de cada aluno matriculado**
(mesmo nome raro) — ninguém fica sem ouvir o próprio nome. O banco de 124 é a rede de
segurança (visitante / nome digitado / turma sem cadastro).

## Referência de implementação
`_voxel/index.html` (aventura "Ilha das Trinta Moedas") — primeiro projeto com o gancho.
