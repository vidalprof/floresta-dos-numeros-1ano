#!/usr/bin/env bash
# ============================================================================
# TRAVA ANTI-CÓPIA-VELHA (SessionStart hook)
# Motivo: já aconteceu de o ambiente reiniciar e deixar a cópia local num
# ponto ANTIGO da história (atrás do GitHub) — o assistente então "não via"
# manuais e workflows que existiam, e concluía errado. Esta trava sincroniza
# com o GitHub logo no início de cada sessão e avisa o estado.
# NUNCA é destrutiva: só faz fast-forward (ff-only) quando a pasta está limpa.
# ============================================================================
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" 2>/dev/null || exit 0

BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
[ -z "$BR" ] && exit 0

# busca o estado do GitHub (silencioso, tolerante a rede)
git fetch origin "$BR" --quiet 2>/dev/null || git fetch origin --quiet 2>/dev/null || true

LOCAL="$(git rev-parse @ 2>/dev/null)"
REMOTE="$(git rev-parse "origin/$BR" 2>/dev/null)"

if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
  BASE="$(git merge-base @ "origin/$BR" 2>/dev/null)"
  if [ "$LOCAL" = "$BASE" ]; then
    # a cópia local está ATRÁS do GitHub
    if git diff --quiet && git diff --cached --quiet; then
      if git merge --ff-only "origin/$BR" --quiet; then
        echo "🔄 [sync] A cópia local estava ATRÁS do GitHub — atualizei sozinho para o topo do branch '$BR'. Nada foi perdido."
      fi
    else
      echo "⚠️ [sync] A cópia local está ATRÁS do GitHub, mas há mudanças não salvas aqui. Antes de agir: 'git stash && git merge --ff-only origin/$BR && git stash pop'."
    fi
  elif [ "$REMOTE" = "$BASE" ]; then
    echo "ℹ️ [sync] A cópia local está À FRENTE do GitHub (há commits locais ainda não enviados no branch '$BR')."
  else
    echo "⚠️ [sync] Local e GitHub DIVERGIRAM no branch '$BR'. Investigar com 'git log --oneline --graph @ origin/$BR' antes de agir — NÃO force nada sem entender."
  fi
fi

echo "✅ [sync] Branch '$BR' conferido com o GitHub."
echo "🧩 [lembrete] Geração é por WORKFLOW do GitHub (internet liberada + secrets), NÃO pelo chat:"
echo "   • imagem  -> gerar-imagens.yml  (Pollinations grátis | Gemini via GEMINI_API_KEY)"
echo "   • áudio   -> gerar-audio.yml / otimizar-audio.yml"
echo "   • lote    -> finalizar.yml  (commit '[imagens]' / '[medalha]')"
echo "   Secrets já configurados: PAGES_TOKEN, GEMINI_API_KEY (Firebase/Pollinations conforme uso)."
echo "📖 [regra] Ler o MANUAL-MESTRE.md antes de criar/alterar atividade. Na dúvida, PERGUNTAR ao Marcos."
exit 0
