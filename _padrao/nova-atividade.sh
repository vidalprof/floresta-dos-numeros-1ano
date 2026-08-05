#!/usr/bin/env bash
# ============================================================
#  NOVA ATIVIDADE EM 30 SEGUNDOS — o molde, não o clone à mão
#
#  Ordem do Marcos (ago/2026): "por que está demorando tanto a criação de uma
#  atividade? Melhor otimizar a linha de produção, claro, com padrão de
#  qualidade altíssimo".
#
#  A demora NÃO estava em escrever as fases: estava em CLONAR o motor à mão e
#  depois caçar o que ficou da atividade de origem. Só na cartografia foram
#  cinco restos de clone (manifesto, relatório do professor, conceitos do
#  zeraProgresso, falas de elogio/consolo, prefixo das imagens) — cada um
#  achado numa rodada diferente da banca, e cada rodada custa minutos.
#
#  Este script faz de uma vez o que eu fazia em seis etapas: copia o motor da
#  atividade mais nova, troca o prefixo em TUDO, escreve o sw.js e o
#  manifest.json com o nome certo, põe os conceitos desta atividade no DOM, no
#  zeraProgresso, no ROTCRI, no CONCN e no TREINO, e deixa o arquivo passando
#  no `node --check`. O que sobra para mim é o que só eu posso fazer: as fases.
#
#  Uso:
#    bash _padrao/nova-atividade.sh _clima2 cl2 "A Bússola do Tempo" \
#         "Ci&#234;ncias &#183; 5&#186; ano" "ciclo,agua,solo,clima,producao"
# ============================================================
set -euo pipefail
PASTA="${1:-}"; PREF="${2:-}"; TITULO="${3:-}"; SUB="${4:-}"; CONC="${5:-}"
MOTOR="${MOTOR:-_mapa}"          # a atividade mais nova serve de motor
if [ -z "$PASTA" ] || [ -z "$PREF" ] || [ -z "$TITULO" ] || [ -z "$CONC" ]; then
  echo "uso: bash _padrao/nova-atividade.sh <pasta> <prefixo> \"<titulo>\" \"<subtitulo>\" \"<conc1,conc2,...>\""
  echo "     (o prefixo entra como <prefixo>_ nas imagens e nas vozes)"
  exit 2
fi
[ -d "$PASTA" ] && { echo "!! $PASTA ja existe — escolha outro nome (nada do antigo se apaga)"; exit 1; }
[ -d "$MOTOR" ] || { echo "!! motor $MOTOR nao encontrado"; exit 1; }

echo ">>> molde: $MOTOR   ->   $PASTA   (prefixo ${PREF}_)"
mkdir -p "$PASTA/img" "$PASTA/audio"
cp "$MOTOR/index.html" "$PASTA/index.html"
cp "$MOTOR/sw.js" "$PASTA/sw.js"
cp "$MOTOR/manifest.json" "$PASTA/manifest.json"

python3 - "$PASTA" "$PREF" "$TITULO" "$SUB" "$CONC" "$MOTOR" <<'PY'
import re, sys, json, os
pasta, pref, titulo, sub, conc, motor = sys.argv[1:7]
conceitos = [c.strip() for c in conc.split(",") if c.strip()]
velho = None
# descobre o prefixo do MOTOR pelos arquivos de imagem dele
from collections import Counter
c = Counter()
for f in os.listdir(os.path.join(motor, "img")):
    m = re.match(r"([a-z]{2,6}_)", f)
    if m: c[m.group(1)] += 1
if c: velho = c.most_common(1)[0][0]
if not velho: raise SystemExit("!! nao descobri o prefixo do motor")

p = os.path.join(pasta, "index.html")
s = open(p, encoding="utf-8").read()

# 1) o prefixo, em TUDO (imagens, vozes, ids de fala)
s = s.replace(velho, pref + "_")
# 2) titulo e subtitulo
mt = re.search(r"<title>(.*?)</title>", s, re.S)
if mt:
    antigo = mt.group(1)
    s = s.replace(antigo, titulo)
if sub:
    s = re.sub(r'el\("div","sub",".*?"\)', 'el("div","sub","%s")' % sub, s, count=1)
# 3) a chave do localStorage (duas atividades no mesmo dominio se atropelam)
s = re.sub(r'localStorage\.(getItem|setItem)\("\w+_med"',
           lambda m: 'localStorage.%s("%s_med"' % (m.group(1), pasta.strip("_")), s)
# 4) os CONCEITOS desta atividade, nos CINCO lugares em que eles aparecem
dom = ",".join("%s:0.3" % k for k in conceitos)
s = re.sub(r"var DOM=\{.*?\};", "var DOM={%s};" % dom, s, flags=re.S)
s = re.sub(r"DOM=\{[a-z_]+:0\.3.*?\};", "DOM={%s};" % dom, s, flags=re.S)
s = re.sub(r"var ROTCRI=\{.*?\};",
           "var ROTCRI={%s};" % ",".join('%s:"%s"' % (k, k) for k in conceitos), s, flags=re.S)
s = re.sub(r"var CONCN=\{.*?\};",
           "var CONCN={%s};" % ",".join('%s:"%s"' % (k, k) for k in conceitos), s, flags=re.S)
s = re.sub(r"var TREINO=\{.*?\};",
           "var TREINO={%s};" % ",".join("%s:mAbertura" % k for k in conceitos), s, flags=re.S)
# 5) as listas de arte e de voz comecam VAZIAS (a lista velha e resto de clone)
s = re.sub(r"var IMGS=\[.*?\];", 'var IMGS=["%s_base","%s_fala","%s_pisca"];' % (pref, pref, pref), s, flags=re.S)
s = re.sub(r"var CENAS=\{.*?\};", "var CENAS={};", s, flags=re.S)
s = re.sub(r"var VOZOK=\{.*?\};", "var VOZOK={};", s, flags=re.S)
open(p, "w", encoding="utf-8").write(s)

# 6) service worker e manifesto PROPRIOS
sw = open(os.path.join(pasta, "sw.js"), encoding="utf-8").read()
sw = re.sub(r'var PREFIXO="[^"]+";', 'var PREFIXO="%s-";' % pasta.strip("_"), sw)
sw = re.sub(r'var CACHE=PREFIXO\+"v\d+";', 'var CACHE=PREFIXO+"v1";', sw)
sw = re.sub(r"var ATIVOS=\[.*?\];",
            'var ATIVOS=["./","./index.html","./manifest.json",'
            '"./img/%s_base.png","./img/%s_fala.png","./img/%s_pisca.png"];' % (pref, pref, pref),
            sw, flags=re.S)
open(os.path.join(pasta, "sw.js"), "w", encoding="utf-8").write(sw)

man = json.load(open(os.path.join(pasta, "manifest.json"), encoding="utf-8"))
man["name"] = re.sub(r"&#\d+;", "", titulo)
man["short_name"] = man["name"].split("—")[0].strip()[:18]
json.dump(man, open(os.path.join(pasta, "manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("   prefixo trocado: %s -> %s_" % (velho, pref))
print("   conceitos: %s" % ", ".join(conceitos))
PY

echo ">>> conferindo o esqueleto..."
python3 - "$PASTA/index.html" > /tmp/_novo_js.js <<'PY'
import re,sys
h=open(sys.argv[1],encoding="utf-8").read()
print("".join(re.findall(r"<script>(.*?)</script>",h,re.S)))
PY
node --check /tmp/_novo_js.js && echo "   JS ok"
echo ">>> o portao de clone deve acusar SO estas coisas, que somem sozinhas"
echo "    conforme voce faz os passos abaixo (arte, voz e fases):"
python3 _qa/clone.py "$PASTA/index.html" 2>&1 | sed 's/^/    /' || true

cat <<FIM

>>> $PASTA criado. O QUE FALTA (e so isto):
    1. escrever as FASES em $PASTA/index.html (o bloco "CONTEUDO")
    2. listar a arte em _gerar_imagens.json e commitar com [imagens]
    3. listar as falas em _lote_falas.json e disparar o gerar-audio.yml
    4. preencher CENAS, IMGS e VOZOK com o que foi gerado
    5. bash _qa/rapido.sh $PASTA/index.html   (a cada mudanca, 5 segundos)
    6. bash _qa/auditar.sh $PASTA/index.html  (a banca inteira, no fim)
FIM
