#!/usr/bin/env bash
# ============================================================
#  CRIA UM CADERNO NOVO DE FOLHA VIVA, a partir do esqueleto VAZIO.
#
#  ⭐ POR QUE ELE EXISTE (pergunta do Marcos, 15/set/2026): *"mas por que você
#  está clonando?"*. Porque o motor não se reescreve — mas o CONTEÚDO do caderno
#  de origem não pode vir junto. Este script resolve a segunda metade: o caderno
#  novo nasce do `_padrao/FOLHA-VIVA/`, que não tem conteúdo de ninguém, e o
#  prefixo é carimbado em TODOS os lugares de uma vez.
#
#  ⚠️ OS LUGARES DO PREFIXO, e por que cada um morde se ficar para trás:
#     · `PREFIXO` do gerar_falas.py  -> o nome dos mp3
#     · `"audio/xx_"` do index.html  -> onde a voz é buscada (404 mudo)
#     · `CHAVE_LS`                   -> o "continuar de onde parou". Repetido,
#       DOIS cadernos brigam pela mesma memória e a criança abre um e cai no
#       meio do outro
#     · `img/xx_trofeu.png` e os selos -> quadradinho vazio na tela do fim
#
#  Uso:  bash _padrao/nova_folha_viva.sh <pasta> <prefixo> "<Título>"
#  Ex.:  bash _padrao/nova_folha_viva.sh _verbo5 vb_ "A Oficina dos Verbos"
# ============================================================
set -e
PASTA="${1%/}"; PRE="$2"; TITULO="$3"
BASE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE"

if [ -z "$PASTA" ] || [ -z "$PRE" ] || [ -z "$TITULO" ]; then
  echo 'uso: bash _padrao/nova_folha_viva.sh <pasta> <prefixo> "<Título>"'
  echo 'ex.: bash _padrao/nova_folha_viva.sh _verbo5 vb_ "A Oficina dos Verbos"'
  exit 2
fi
[ -e "$PASTA" ] && { echo "⛔ $PASTA já existe — não vou escrever por cima."; exit 1; }
case "$PRE" in *_) ;; *) echo "⛔ o prefixo tem de terminar com _ (ex.: vb_)"; exit 1;; esac

# ⚠️ prefixo já usado = resto de clone garantido, e o `_qa/clone.py` reprova.
if grep -rqs "\"$PRE" --include=index.html _*/ 2>/dev/null; then
  echo "⛔ o prefixo '$PRE' já é usado por outra atividade. Escolha outro."
  exit 1
fi

mkdir -p "$PASTA/img" "$PASTA/audio"
cp _padrao/FOLHA-VIVA/index.html _padrao/FOLHA-VIVA/folhas.js \
   _padrao/FOLHA-VIVA/gerar_falas.py "$PASTA/"
# os SELOS DA CASA (troféu e as duas estrelas) já vão com o prefixo carimbado:
# são do banco, não são conteúdo de caderno nenhum, e sem eles a tela do fim
# abre com quadradinho vazio e 404 no console.
cp _padrao/FOLHA-VIVA/img/trofeu.png   "$PASTA/img/${PRE}trofeu.png"
cp _padrao/FOLHA-VIVA/img/selo.png     "$PASTA/img/${PRE}selo.png"
cp _padrao/FOLHA-VIVA/img/selo_off.png "$PASTA/img/${PRE}selo_off.png"
python3 - "$PASTA" "$PRE" <<'PYIMG'
import io, json, sys
pasta, pre = sys.argv[1], sys.argv[2]
io.open(pasta + "/img/ORIGEM.json", "w", encoding="utf-8").write(json.dumps({
  pre + "trofeu.png": "banco:trofeu",
  pre + "selo.png": "banco:selo",
  pre + "selo_off.png": "banco:selo"}, indent=1, sort_keys=True, ensure_ascii=False))
PYIMG

python3 - "$PASTA" "$PRE" "$TITULO" <<'PY'
# -*- coding: utf-8 -*-
import io, re, sys
pasta, pre, titulo = sys.argv[1], sys.argv[2], sys.argv[3]
chave = re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")

h = io.open(pasta + "/index.html", encoding="utf-8").read()
h = h.replace('"audio/sb_"', '"audio/%s"' % pre)
h = h.replace('"audio/xx_"', '"audio/%s"' % pre)
h = re.sub(r'img/\w+_trofeu\.png', 'img/%strofeu.png' % pre, h)
h = re.sub(r'var CHAVE_LS = "[^"]*";', 'var CHAVE_LS = "%s";' % chave, h)
h = h.replace("NOME DA ATIVIDADE", titulo)
io.open(pasta + "/index.html", "w", encoding="utf-8").write(h)

j = io.open(pasta + "/folhas.js", encoding="utf-8").read()
j = re.sub(r'img/\w+_selo', 'img/%sselo' % pre, j)
j = j.replace("NOME DA ATIVIDADE", titulo)
io.open(pasta + "/folhas.js", "w", encoding="utf-8").write(j)

g = io.open(pasta + "/gerar_falas.py", encoding="utf-8").read()
g = g.replace('PREFIXO = u"xx_"', 'PREFIXO = u"%s"' % pre)
g = g.replace("NOME DA ATIVIDADE", titulo)
io.open(pasta + "/gerar_falas.py", "w", encoding="utf-8").write(g)
print(u"  prefixo `%s` carimbado; CHAVE_LS = `%s`" % (pre, chave))
PY

echo
echo "✅ $PASTA criado do esqueleto — casca completa, conteúdo ZERO."
echo
echo "   Agora, nesta ordem (é ela que economiza voltas):"
echo "   1. colher as folhas de papel  -> workflow buscar-fotos.yml"
echo "   2. LER as trinta, uma a uma   -> _sequencias/POTE-<assunto>.md"
echo "   3. o roteiro sai do inventario de VERBOS do crivo"
echo "   4. preencher: GESTOS · ITENS · DADOS · NOMES · CURRICULO · novaFolha()"
echo "      e OBJETIVOS no folhas.js; depois as folhas f01..fN"
echo "   5. python3 $PASTA/gerar_falas.py"
echo "   6. bash _qa/previo.sh $PASTA        (2 s — erros baratos)"
echo "   7. node _qa/conta_folha.js $PASTA   (o pote bate com os itens?)"
echo "   8. node _qa/joga_folha.js $PASTA    (todo item fecha?)"
echo "   9. bash _qa/auditar_folha.sh $PASTA (a banca inteira)"
echo
echo "   ⚠️ O CADERNO RECEM-NASCIDO JA ABRE LIMPO (medido: zero erro de JS, zero 404),"
echo "      e o pre-voo reprova em TRES portoes — os tres dizendo a mesma coisa,"
echo "      'este caderno ainda esta vazio', e nao 'o esqueleto esta quebrado':"
echo "        · 0b6 catalogo  -> so entra no ATIVIDADES.md quando for publicar"
echo "        · 3g duracao    -> caderno sem folha nenhuma nao enche a aula"
echo "        · 1z boot       -> o mp3 da capa; o entregar.yml grava a voz"
echo "      Qualquer OUTRA reprovacao no primeiro minuto e defeito de verdade."
echo
echo "   Detalhes e armadilhas medidas: _padrao/CLONAR-FOLHA-VIVA.md"
