# 🔐 FIREBASE do EducaVerso — evidências de aprendizagem (2 passos do professor)

O jogo agora grava **EVIDÊNCIAS** de cada missão (aluno, habilidade, erros, nível de
ajuda, estratégia) e o **Painel do Professor** (`?painel` no link do jogo) transforma
isso em **rubrica BNCC + parecer descritivo em rascunho + nota sugerida**.

Para o Firebase aceitar, são **2 passos únicos no console** (só o Marcos tem acesso):

## Passo 1 — Ligar o "login anônimo" (o crachá das crianças)
Console → **Authentication → Sign-in method** → provedor **Anonymous** → **Ativar**.
Link direto: https://console.firebase.google.com/project/atividades-educativas-16860/authentication/providers
> Por quê: a criança não tem conta; o jogo pega um crachá anônimo só para as regras
> aceitarem a escrita. Ninguém além do admin consegue LER os dados.

## Passo 2 — Acrescentar a gaveta `educaverso` nas REGRAS
Console → Realtime Database → aba **Regras**:
https://console.firebase.google.com/project/atividades-educativas-16860/database/atividades-educativas-16860-default-rtdb/rules

Dentro do bloco `"rules": { ... }`, **ao lado** de `"agenda"` (sem mexer no resto!),
acrescente:

```json
"educaverso": {
  "vidal-ramos": {
    "evidencias": {
      ".read": "root.child('agenda/vidal-ramos/admins').child(auth.uid).exists()",
      ".write": "auth != null"
    }
  }
}
```

> - **Leitura:** só quem está em `/agenda/vidal-ramos/admins` (o Marcos) — os dados
>   das crianças NUNCA ficam públicos (LGPD).
> - **Escrita:** qualquer crachá (anônimo) — risco baixo e aceitável: só entra
>   registro novo de jogo, e ninguém consegue ler nem apagar os dos outros pelo app.
> - **NÃO mexer** em `/agenda` (blindada), nem em provas/lab/labstatus.

## Como usar no dia a dia
- **Criança:** abre o jogo → digita o primeiro nome + escolhe a turma (1ª vez só) →
  joga. (Tem "Jogar sem registrar" para visitas/demonstração.)
- **Professor:** abre `https://vidalprof.github.io/vila-tabuada/?painel` → entra com a
  **mesma matrícula/senha da Agenda** → vê por turma/aluno: missões, nível
  (Consolidado / Em desenvolvimento / Iniciando), **parecer descritivo em rascunho**
  (editável, cita as evidências reais) e **nota sugerida** (Consolidado 8,5–10 ·
  Em desenvolvimento 6,0–8,4 · Iniciando <6,0 — ajuste à régua da escola).
- **Sem internet na hora:** a evidência entra numa fila local e sobe sozinha no
  próximo acesso. O painel também tem o modo "só desta máquina".

## A rubrica (regra fixa, auditável — de onde vem o nível)
| O jogo observou | Nível |
|---|---|
| Acertou sem nenhuma ajuda e sem erro | **Consolidado** |
| Acertou após a pergunta reflexiva (ou usando o ❓) | **Em desenvolvimento** |
| Precisou do passo a passo ensinado | **Iniciando** |

Base: LDB art. 24, V ("prevalência dos aspectos qualitativos"); stealth assessment
(Shute/ECD); rubricas BNCC (Movimento pela Base). Detalhes e fontes:
`PESQUISA-AJUDA-E-AVALIACAO-2026-07.md`.
