#!/usr/bin/env bash
# ============================================================
#  A BANCA — roda TODOS os auditores antes de entregar
#  Pedido do Marcos (ago/2026): "precisamos de auditores antes de
#  entregar a atividade". Cada auditor e um profissional com uma
#  obsessao só. Nenhum deles confia no outro.
#
#  Uso:  bash _qa/auditar.sh _doceria/index.html telaCapa dMonta dSoma ...
#        (sem lista de telas, ele descobre sozinho quem chama limpa())
#
#  Sai 0 se a banca inteira aprovar; 1 se algum reprovar.
# ============================================================
set -uo pipefail
ARQ="${1:-}"
if [ -z "$ARQ" ]; then echo "uso: bash _qa/auditar.sh <arquivo.html> [tela1 tela2 ...]"; exit 2; fi
shift || true
TELAS="$*"

if [ -z "$TELAS" ]; then
  TELAS=$(python3 - "$ARQ" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
js="".join(re.findall(r"<script>(.*?)</script>",h,re.S))
# tela = funcao que chama limpa() (mesma regra do _qa/fluxo.py)
nomes=[]
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    n=m.group(1); i=m.end()
    prof=0; j=js.find("{",i); k=j
    while k<len(js):
        if js[k]=="{": prof+=1
        elif js[k]=="}":
            prof-=1
            if prof==0: break
        k+=1
    if re.search(r"\blimpa\(\)", js[j:k]): nomes.append(n)
print(" ".join(nomes))
PY
)
fi

echo "==================================================="
echo " BANCA DE AUDITORIA — $ARQ"
echo " telas: $(echo $TELAS | wc -w)"
echo "==================================================="
FALHOU=0

echo
echo "--- 1) ENGENHEIRO (o codigo roda?) -----------------"
python3 - "$ARQ" > /tmp/_qa_js.js <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
if node --check /tmp/_qa_js.js >/dev/null 2>&1; then echo "  JS ok (node --check)"; else echo "  ERRO DE SINTAXE NO JS"; node --check /tmp/_qa_js.js; FALHOU=1; fi

echo
echo "--- 1b) FUNCAO QUE NAO EXISTE (estoura na mao da crianca?) -"
python3 _qa/funcoes.py "$ARQ" || FALHOU=1

echo
echo "--- 1c) RESTO DE CLONE (sobrou coisa da origem?) --"
python3 _qa/clone.py "$ARQ" || FALHOU=1

echo
echo "--- 2) ARQUITETO DE FLUXO (da para chegar ao fim?) -"
python3 _qa/fluxo.py "$ARQ" telaCapa || FALHOU=1

echo
echo "--- 3) DESIGNER (toda classe tem estilo de base?) --"
python3 _qa/classes.py "$ARQ" || FALHOU=1

echo
echo "--- 3b) PROGRESSAO (a barra so anda para a frente?) -"
python3 _qa/progressao.py "$ARQ" || FALHOU=1

echo
echo "--- 3c) ARTE PROPRIA (imagem copiada de outra atividade?) -"
python3 _qa/arte_propria.py "$ARQ" || FALHOU=1

echo
echo "--- 3d) MASCOTE (ele treme ao falar ou piscar?) ---"
python3 _qa/mascote.py "$ARQ" || FALHOU=1

echo
echo "--- 4) ACESSIBILIDADE (a crianca ENXERGA o texto?) -"
node _qa/contraste.js "$ARQ" $TELAS 2>/dev/null || FALHOU=1

echo
echo "--- 4b) NARRACAO (a voz fala direito?) -------------"
if [ -f _lote_falas.json ]; then python3 _qa/falas.py _lote_falas.json || FALHOU=1; else echo "  (sem _lote_falas.json)"; fi

echo
echo "--- 5) LEIAUTE (cabe na tela? da para tocar?) ------"
node _qa/leiaute.js "$ARQ" $TELAS 2>/dev/null || FALHOU=1

echo
echo "--- 6) JOGADOR (joga sozinho ate a medalha) --------"
node _qa/jogador.js "$ARQ" 2>/dev/null | tail -4

echo
echo "==================================================="
if [ "$FALHOU" = "0" ]; then
  echo " BANCA APROVOU. Falta so o PROFESSOR (portao final)."
else
  echo " BANCA REPROVOU — conserte antes de mostrar ao Marcos."
fi
echo "==================================================="
exit $FALHOU
