#!/usr/bin/env bash
# ============================================================
#  PRÉ-ENTREGA — roda AQUI exatamente o que o `entregar.yml` roda LÁ.
#
#  ⚠️ POR QUE ELE EXISTE (20/set/2026, prova de Ed. Física). Montei a prova,
#     rodei uma lista de portões que eu mesmo escolhi — catálogo, clone,
#     revisor, contraste, leiaute, sobreposto, currículo, o jogador que joga a
#     prova inteira — deu tudo zero, commitei e disparei a entrega. O workflow
#     reprovou em UM portão que não estava na minha lista: `_qa/falas.py`, que
#     sabe que a voz lê "Tangram" com a ênfase errada (defeito que o MARCOS
#     ouviu em ago/2026). Nada foi publicado, e eu só descobri depois de três
#     disparos e de ler o log do Actions.
#
#     O buraco não era falta de portão: era eu escolher a lista. O `previo.sh`
#     roda o `falas.py` e teria pego — mas o `previo.sh` é de FOLHA VIVA e
#     reprova uma prova por desenho (duração, cor cravada, game-feel), então eu
#     o pulei e montei a minha. Lista escolhida a dedo é lista que esquece.
#
#  A REGRA QUE ISSO DEIXA: o que decide se a entrega passa é o `entregar.yml`.
#  Então a conferência local tem de ser a MESMA lista, não uma parecida. Este
#  arquivo é a cópia dela; se o workflow ganhar um portão novo, ganha aqui
#  também, no mesmo commit.
#
#  Códigos, iguais aos de lá: 1 = REPROVA e segura a entrega · 2 = "não medi"
#  (vira aviso, não segura) · 0 = passou.
#
#  uso:  bash _qa/pre_entrega.sh <pasta> <repo-de-destino>
# ============================================================
set -uo pipefail

PASTA="${1:-}"
REPO="${2:-}"
if [ -z "$PASTA" ]; then
  echo "uso: bash _qa/pre_entrega.sh <pasta> <repo-de-destino>"
  exit 2
fi
PASTA="${PASTA%/}"
IDX="$PASTA/index.html"
FAL="$PASTA/falas.json"
CONT="$PASTA/conteudo.json"

if [ ! -f "$IDX" ]; then
  echo "NAO MEDI: nao achei $IDX"
  exit 2
fi

FALHOU=0
NAOMEDIU=0
VERDE=0

portao() {
  local nome="$1"; shift
  local saida rc
  saida="$("$@" 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    VERDE=$((VERDE+1))
    printf '  \033[32mok  \033[0m %s\n' "$nome"
  elif [ "$rc" = "2" ]; then
    NAOMEDIU=$((NAOMEDIU+1))
    printf '  \033[33m--  \033[0m %s  (nao medi aqui — nao segura a entrega)\n' "$nome"
  else
    FALHOU=1
    printf '  \033[31mXX  \033[0m %s  \033[31mREPROVOU\033[0m\n' "$nome"
    echo "$saida" | sed 's/^/        /' | head -22
  fi
}

echo "=============================================================="
echo " PRE-ENTREGA de $PASTA  ->  ${REPO:-<sem destino>}"
echo " (a MESMA lista que o entregar.yml roda; nada escolhido a dedo)"
echo "=============================================================="

# 1) o catalogo e o painel do Marcos — atividade fora do painel nao sobe
if [ -n "$REPO" ]; then
  portao "catalogo + painel de links" python3 _qa/catalogo.py "$PASTA" "$REPO"
else
  echo "  --   catalogo: sem repo de destino no comando, nao da para conferir o link"
  NAOMEDIU=$((NAOMEDIU+1))
fi

# 2) o que roda em toda atividade
portao "PC ruim (enfeite que falha prende a crianca)" node _qa/pcruim.js "$IDX"
portao "estatico (nome usado que nunca foi declarado)" bash _qa/estatico.sh "$IDX"
portao "dinamicas (armadilha de mecanica aberta)"      python3 _qa/dinamicas.py "$IDX"

# 3) so quando a atividade e MONTADA (tem conteudo.json)
if [ -f "$CONT" ]; then
  portao "resposta entregue (destaque na palavra certa)" python3 _qa/entrega.py "$PASTA"
  portao "enunciado bate (promete um, cobra outro)"      python3 _qa/enunciado_bate.py "$PASTA"
  portao "texto de exemplo (assunto de outra atividade)" python3 _qa/exemplo.py "$PASTA"
fi

# 4) leiaute e dedo
portao "moldura corta (o container come a figura)" python3 _qa/corta_figura.py "$IDX"
portao "elemento coberto (o dedo nao alcanca)"     node _qa/sobreposto.js "$IDX"
portao "toque (arrasto sem touch-action)"          python3 _qa/toque.py "$IDX"

# 5) A VOZ — foi aqui que a prova de Ed. Fisica caiu
if [ -f "$FAL" ]; then
  portao "narracao (palavra que a voz erra)" python3 _qa/falas.py "$FAL"
else
  echo "  --   narracao: $PASTA nao tem falas.json — a voz nao tem como ser conferida"
  NAOMEDIU=$((NAOMEDIU+1))
fi
if [ -f "$CONT" ]; then
  portao "voz bate (a voz diz o texto que a crianca ve)" python3 _qa/voz_bate.py "$PASTA"
fi

echo "--------------------------------------------------------------"
echo "  passaram: $VERDE   nao mediram: $NAOMEDIU"
if [ "$FALHOU" != "0" ]; then
  echo "  -> REPROVOU. Se voce disparar a entrega assim, o workflow para no"
  echo "     mesmo portao e NADA e publicado. Conserte antes."
  exit 1
fi
echo "  -> verde na lista do entregar.yml. Pode disparar a entrega."
echo "     (isto NAO substitui a banca nem o portao do professor.)"
exit 0
