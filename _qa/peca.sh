#!/usr/bin/env bash
# ============================================================
#  A BANCADA DA PEÇA — mede UMA mecânica sozinha, antes de ela entrar
#  em qualquer atividade.
#
#  Pedido do Marcos (ago/2026): *"você não tem como criar um profissional que
#  pesquisa mecânicas novas, monta num PC virtual, executa tudo, treina, e fica
#  disponível para a gente pronta e testada?"*
#
#  A banca grande (`_qa/auditar.sh`) mede uma ATIVIDADE inteira. Esta aqui mede
#  uma PEÇA: o mesmo Chromium, os mesmos auditores, mas apontados para um
#  arquivinho de uma mecânica só. É o que deixa a peça "pronta e testada" antes
#  de existir atividade nenhuma.
#
#  Uso:  bash _qa/peca.sh _padrao/pecas/conserte-o-erro.html
#  Sai 0 se a peça estiver pronta para entrar no catálogo.
# ============================================================
set -uo pipefail
ARQ="${1:-}"
if [ -z "$ARQ" ]; then echo "uso: bash _qa/peca.sh <_padrao/pecas/arquivo.html>"; exit 2; fi
# ⚠️ CORRIDA ENTRE BANCADAS (ago/2026). O caminho era FIXO (`/tmp/_peca.js`).
#    Com dois profissionais rodando a bancada ao mesmo tempo, um sobrescrevia o
#    JS do outro e AS DUAS pecas reprovavam no portao 1 com erro de sintaxe
#    FALSO. Reprovacao fantasma e o pior estrago: faz consertar o que nao esta
#    quebrado. Cada corrida agora tem o seu arquivo.
JSTMP="$(mktemp -t qajs.XXXXXX.js)"
FALHOU=0
TELAS=$(python3 - "$ARQ" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
js="".join(re.findall(r"<script>(.*?)</script>",h,re.S))
n=[]
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    nm=m.group(1); j=js.find("{",m.end()); k=j; p=0
    while k<len(js):
        if js[k]=="{": p+=1
        elif js[k]=="}":
            p-=1
            if p==0: break
        k+=1
    if re.search(r"\blimpa\(\)", js[j:k]): n.append(nm)
print(" ".join(n))
PY
)
echo "==================================================="
echo " BANCADA DA PEÇA — $ARQ"
echo " telas: $(echo $TELAS | wc -w)  ($TELAS)"
echo "==================================================="

echo; echo "--- 1) O CODIGO RODA? ------------------------------"
python3 - "$ARQ" > "$JSTMP" <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
if node --check "$JSTMP" >/dev/null 2>&1; then echo "  JS ok"; else echo "  ERRO DE SINTAXE"; node --check "$JSTMP"; FALHOU=1; fi

echo; echo "--- 2) FUNCAO QUE NAO EXISTE -----------------------"
python3 _qa/funcoes.py "$ARQ" || FALHOU=1

echo; echo "--- 3) DINAMICAS (as armadilhas da mecanica) -------"
python3 _qa/dinamicas.py "$ARQ" || FALHOU=1

echo; echo "--- 4) CLASSES SEM ESTILO --------------------------"
python3 _qa/classes.py "$ARQ" || FALHOU=1

TMPQ="$(mktemp -d)"
node _qa/contraste.js "$ARQ" $TELAS > "$TMPQ/c.txt" 2>&1 & PC=$!
node _qa/leiaute.js   "$ARQ" $TELAS > "$TMPQ/l.txt" 2>&1 & PL=$!
node _qa/imagens.js   "$ARQ" $TELAS > "$TMPQ/i.txt" 2>&1 & PI=$!

echo; echo "--- 5) A CRIANCA ENXERGA O TEXTO? ------------------"
wait $PC || FALHOU=1; cat "$TMPQ/c.txt"
echo; echo "--- 6) TODA FIGURA APARECE? ------------------------"
wait $PI || FALHOU=1; cat "$TMPQ/i.txt"
echo; echo "--- 7) CABE NA TELA? DA PARA TOCAR? ----------------"
wait $PL || FALHOU=1; cat "$TMPQ/l.txt"

echo; echo "--- 8) DA PARA TERMINAR? (joga sozinho) ------------"
INICIO="$(echo $TELAS | awk '{print $1}')" node _qa/jogador.js "$ARQ" > "$TMPQ/j.txt" 2>&1
tail -4 "$TMPQ/j.txt"
grep -q "PRESO" "$TMPQ/j.txt" && { echo "  !! a peca TRAVA — a crianca fica presa"; FALHOU=1; }
grep -q "ERROS JS: nenhum" "$TMPQ/j.txt" || { echo "  !! houve erro de JS durante a partida"; FALHOU=1; }

echo; echo "==================================================="
if [ "$FALHOU" = "0" ]; then
  echo " PECA PRONTA — pode entrar no catalogo (_padrao/DINAMICAS.md)."
else
  echo " PECA REPROVADA — conserte antes de guardar."
fi
echo "==================================================="
rm -rf "$TMPQ"
exit $FALHOU
