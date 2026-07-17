#!/usr/bin/env bash
# ============================================================================
# TRAVA ANTI-CÓPIA-VELHA (SessionStart hook) — versão BLINDADA
# Motivo: já aconteceu de o ambiente reiniciar e deixar a cópia local num
# ponto ANTIGO da história (atrás do GitHub) — o assistente então "não via"
# manuais/workflows/atividades que existiam, e concluía errado ("perdido").
# Esta trava sincroniza com o GitHub logo no início de cada sessão.
# NUNCA é destrutiva: só faz fast-forward (ff-only) quando a pasta está limpa.
#
# BLINDAGEM (lição paga jul/2026): a versão antiga DESISTIA na 1ª falha de
# fetch e imprimia o mesmo "✅ conferido" tranquilizador — parecendo tudo em
# dia quando NÃO estava (fetch falhou = seguiu quieto na cópia velha). Agora:
#   (1) RETRY no fetch (3 tentativas com espera) antes de desistir;
#   (2) se NÃO conseguir confirmar o estado do GitHub, imprime um aviso BEM
#       CHAMATIVO (nunca o ✅) — "não confie na cópia local".
# ============================================================================
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" 2>/dev/null || exit 0

BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
[ -z "$BR" ] && exit 0

# --- busca o estado do GitHub com RETRY (não desistir na 1ª falha) ---------
FETCH_OK=0
for tentativa in 1 2 3; do
  # --force é ESSENCIAL: se o container voltar com origin/<BR> apontando pra uma
  # base VELHA (rebobinada), só o --force atualiza o ref pro tip REAL do GitHub.
  # Sem isso, um 'reset --hard origin/<BR>' cai na base velha e apaga eduverse/MEMORIA
  # (lição paga várias vezes, jul/2026).
  if git fetch --force origin "$BR" --quiet 2>/dev/null || git fetch --force origin --quiet 2>/dev/null; then
    FETCH_OK=1
    break
  fi
  # espera crescente entre tentativas (2s, 4s) — rede/proxy no arranque
  [ "$tentativa" -lt 3 ] && sleep $((tentativa * 2))
done

REMOTE="$(git rev-parse "origin/$BR" 2>/dev/null || true)"

# --- NÃO conseguiu confirmar o GitHub? AVISO ALTO, nunca o ✅ ---------------
if [ "$FETCH_OK" != "1" ] || [ -z "$REMOTE" ]; then
  echo "############################################################"
  echo "⚠️⚠️⚠️  ATENCAO: NAO consegui conferir com o GitHub  ⚠️⚠️⚠️"
  echo "O fetch falhou (rede/proxy) em 3 tentativas. A copia LOCAL"
  echo "pode estar VELHA/atras do GitHub e eu NAO tenho como saber agora."
  echo "NAO confie na pasta local. ANTES DE AGIR ou de declarar algo"
  echo "'perdido/faltando', rode manualmente:"
  echo "    git fetch origin $BR && git status"
  echo "    git merge --ff-only origin/$BR   # se estiver atras"
  echo "Lembre a licao paga: 'nao achei' != 'nao existe' — o trabalho"
  echo "vive nos COMMITS do GitHub, nunca so na copia local."
  echo "############################################################"
  exit 0
fi

LOCAL="$(git rev-parse @ 2>/dev/null)"

if [ "$LOCAL" != "$REMOTE" ]; then
  BASE="$(git merge-base @ "origin/$BR" 2>/dev/null)"
  if [ "$LOCAL" = "$BASE" ]; then
    # a cópia local está ATRÁS do GitHub
    if git diff --quiet && git diff --cached --quiet; then
      if git merge --ff-only "origin/$BR" --quiet; then
        echo "🔄 [sync] A cópia local estava ATRÁS do GitHub — atualizei sozinho para o topo do branch '$BR'. Nada foi perdido."
      else
        echo "⚠️ [sync] A cópia local está ATRÁS do GitHub, mas o fast-forward falhou. Rode: 'git merge --ff-only origin/$BR' e investigue antes de agir."
      fi
    else
      echo "⚠️ [sync] A cópia local está ATRÁS do GitHub, mas há mudanças não salvas aqui. Antes de agir: 'git stash && git merge --ff-only origin/$BR && git stash pop'."
    fi
  elif [ "$REMOTE" = "$BASE" ]; then
    echo "ℹ️ [sync] A cópia local está À FRENTE do GitHub (há commits locais ainda não enviados no branch '$BR'). LEMBRE de empurrar (git push) e CONFERIR no GitHub."
  else
    echo "⚠️ [sync] Local e GitHub DIVERGIRAM no branch '$BR'. Investigar com 'git log --oneline --graph @ origin/$BR' antes de agir — NÃO force nada sem entender."
  fi
fi

echo "✅ [sync] Branch '$BR' conferido com o GitHub (fetch OK)."
echo "🧩 [lembrete] Geração é por WORKFLOW do GitHub (internet liberada + secrets), NÃO pelo chat:"
echo "   • imagem  -> gerar-imagens.yml  (Pollinations grátis | Gemini via GEMINI_API_KEY)"
echo "   • áudio   -> gerar-audio.yml / otimizar-audio.yml"
echo "   • lote    -> finalizar.yml  (commit '[imagens]' / '[medalha]')"
echo "   Secrets já configurados: PAGES_TOKEN, GEMINI_API_KEY (Firebase/Pollinations conforme uso)."
echo "📖 [regra] Ler o MANUAL-MESTRE.md antes de criar/alterar atividade. Na dúvida, PERGUNTAR ao Marcos."
exit 0
