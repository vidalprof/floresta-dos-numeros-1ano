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
# ⚠️ O MOLDE NAO E PECA — e o TEMPLATE em branco da oficina (o `integrar.py` o
#    usa como base de CSS; nao entra em atividade nem no catalogo DINAMICAS.md).
#    Rodar a bancada nele so fazia o jogador estourar em 150s (timeout 124) e
#    aparecer como "FAIL" numa varredura — acusacao do inocente, que e o que a
#    casa combateu em toda parte ("portao que acusa o inocente ensina a ignorar
#    portao"). Aqui ele sai limpo, dizendo o que e.
case "$(basename "$ARQ")" in
  MOLDE.html)
    echo "==================================================="
    echo " $ARQ e o MOLDE (template em branco da oficina), nao uma peca."
    echo " Nada a testar: copie-o para criar uma peca nova e teste a copia."
    echo "==================================================="
    exit 0 ;;
esac

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

# ⭐ o BECO: tela de fim que so sabe voltar ao comeco da propria peca. Dentro
# da atividade a crianca fecha a fase e fica presa nela. Barato, sem navegador.
echo; echo "--- 3b) BECO (da para SAIR da peca?) ---------------"
python3 _qa/beco_peca.py "$ARQ" || FALHOU=1

echo; echo "--- 4) CLASSES SEM ESTILO --------------------------"
python3 _qa/classes.py "$ARQ" || FALHOU=1

# cor de texto cravada sem fundo proprio: a peca nao sabe em que atividade vai
# cair, e as da casa vao do azul-ceu ao galpao a noite. Ver a licao no cabecalho.
echo; echo "--- 4b) COR CRAVADA (a peca segue o tema?) ---------"
python3 _qa/cor_fixa.py "$ARQ" || FALHOU=1

TMPQ="$(mktemp -d)"
node _qa/contraste.js "$ARQ" $TELAS > "$TMPQ/c.txt" 2>&1 & PC=$!
node _qa/leiaute.js   "$ARQ" $TELAS > "$TMPQ/l.txt" 2>&1 & PL=$!
node _qa/imagens.js   "$ARQ" $TELAS > "$TMPQ/i.txt" 2>&1 & PI=$!

echo; echo "--- 5) A CRIANCA ENXERGA O TEXTO? ------------------"
wait $PC || FALHOU=1; cat "$TMPQ/c.txt"

# ⚠️ ...E DO OUTRO LADO DO TEMA. A bancada roda no ESCURO; a atividade pode ser
#    clara (o Letreiro tem uma rua fotografada de fundo). Peca de tinta clara
#    passa aqui e morre la — foi assim que catorze pecas chegaram ate a
#    atividade em duas noites. Ver o cabecalho do _qa/tema_claro.js, inclusive
#    por que ele nasce com uma lista de divida em vez de derrubar 44 de 79.
echo "--- 5c) E NUMA ATIVIDADE DE TEMA CLARO? ------------"
node _qa/tema_claro.js "$ARQ" $TELAS || FALHOU=1
echo; echo "--- 6) TODA FIGURA APARECE? ------------------------"
wait $PI || FALHOU=1; cat "$TMPQ/i.txt"
echo; echo "--- 7) CABE NA TELA? DA PARA TOCAR? ----------------"
wait $PL || FALHOU=1; cat "$TMPQ/l.txt"

echo; echo "--- 8) DA PARA TERMINAR? (joga sozinho) ------------"
INICIO="$(echo $TELAS | awk '{print $1}')" node _qa/jogador.js "$ARQ" > "$TMPQ/j.txt" 2>&1
tail -4 "$TMPQ/j.txt"
grep -q "PRESO" "$TMPQ/j.txt" && { echo "  !! a peca TRAVA — a crianca fica presa"; FALHOU=1; }
grep -q "ERROS JS: nenhum" "$TMPQ/j.txt" || { echo "  !! houve erro de JS durante a partida"; FALHOU=1; }

echo; echo
echo "--- 9) ERRADOR (erra de proposito: da para seguir?) -"
# ⭐ O portao do ANDAIME: erra tres vezes de proposito e confere que a ajuda
#    CRESCE (dica -> apoio concreto -> revela) e que a medalha continua
#    alcancavel. E o unico que mede a promessa central da casa: errar nao pune,
#    e ninguem fica preso. Sai 2 quando nao tem receita para a peca — e isso
#    NAO e aprovacao, e "nao sei medir esta".
node _qa/errador.js "$ARQ" > "$TMPQ/errador.txt" 2>&1; _ERR=$?
tail -6 "$TMPQ/errador.txt"
if [ "$_ERR" = "2" ]; then
  echo "  ⚠️ SEM RECEITA — este portao NAO mediu o andaime desta peca."
elif [ "$_ERR" != "0" ]; then FALHOU=1; fi

echo "==================================================="
if [ "$FALHOU" = "0" ]; then
  echo " PECA PRONTA — pode entrar no catalogo (_padrao/DINAMICAS.md)."
else
  echo " PECA REPROVADA — conserte antes de guardar."
fi
echo "==================================================="
rm -rf "$TMPQ"
exit $FALHOU
