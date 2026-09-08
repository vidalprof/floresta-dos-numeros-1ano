#!/usr/bin/env bash
# ============================================================
#  PORTÃO ESTÁTICO (ESLint) — o `ReferenceError` pego SEM abrir o navegador.
#
#  NASCEU DA TELA BRANCA DO TANGRAM (03/set/2026). O Marcos clicou e viu so o
#  fundo: eu tinha apagado a declaracao `var FASES_MESTRE` e um IIFE de boot,
#  400 linhas abaixo, ainda usava. `Uncaught ReferenceError`. O app morria na
#  primeira linha executada.
#
#  O `node --check` aprovou, porque `FASES_MESTRE` esta ESCRITO certo — so nao
#  EXISTE. Sintaxe e uma coisa; nome que nunca foi declarado e outra, e o
#  `node --check` nao olha a segunda.
#
#  O `_qa/boot.js` (portao 1z) pega isso abrindo o Chromium, e vai continuar
#  pegando — mas leva ~10 segundos e so ve o caminho que ELE percorre. Este aqui
#  le o arquivo INTEIRO em 1 segundo e ve TODOS os caminhos, inclusive o codigo
#  que so roda na fase 28 ou quando a crianca erra tres vezes. Os dois se
#  completam: o estatico ve tudo raso, o boot ve fundo um caminho so.
#
#  ⭐ FERRAMENTA GRATUITA (ordem do Marcos, set/2026: *"instale toda ferramenta
#  que deixe nosso trabalho moderno, mais profissional, mais perfeito, sem
#  erros"*). ESLint 9, MIT, instalado em `_qa/ferramentas/`. Nao custa nada e
#  nao depende de rede para rodar.
#
#  O que ele cobra (ver `_qa/ferramentas/eslint.config.mjs`, com o porque de
#  cada regra): nome nao declarado, uso antes de declarar, `case` que vaza,
#  chave/case duplicado, funcao redeclarada, `if(x=1)`, codigo inalcancavel.
#
#  Uso:  bash _qa/estatico.sh <arquivo.html>
#  Sai 0 se limpo, 1 se achou defeito, 2 se nao deu para rodar.
# ============================================================
set -uo pipefail
ARQ="${1:-}"
if [ -z "$ARQ" ]; then echo "uso: bash _qa/estatico.sh <arquivo.html>"; exit 2; fi
if [ ! -f "$ARQ" ]; then echo "NAO MEDI: nao achei $ARQ"; exit 2; fi

BIN="_qa/ferramentas/node_modules/.bin/eslint"
CFG="_qa/ferramentas/eslint.config.mjs"
if [ ! -x "$BIN" ]; then
  echo "NAO MEDI: o ESLint nao esta instalado. Rode: npm install --prefix _qa/ferramentas"
  exit 2
fi

# ⚠️ O ESLint 9 recusa arquivo FORA da pasta do projeto ("File ignored because
#    outside of base path") — e recusa CALADO, com codigo 0, que a banca leria
#    como "passou". Por isso o JS extraido vai para dentro do repo, e por isso
#    a saida e conferida antes de virar aprovacao.
TMP="_qa/.estatico-$$.js"
trap 'rm -f "$TMP"' EXIT

python3 - "$ARQ" "$TMP" <<'PY'
import os, re, sys
h = open(sys.argv[1], encoding="utf-8").read()
# so os <script> sem atributo (os mesmos que o `node --check` da banca le)
js = "".join(re.findall(r"<script>(.*?)</script>", h, re.S))
# ⚠️ (set/2026, Fabrica de Palavras) APP A MAO PARTIDO EM DOIS ARQUIVOS: o miolo
#    pode morar num `<script src="folhas.js">` ao lado. Lendo so o index, o portao
#    acusava "confereFolha is not defined" (funcao que existe, no irmao) e, pior,
#    ficaria CEGO para os erros do arquivo de fora. Os irmaos locais entram aqui.
base = os.path.dirname(os.path.abspath(sys.argv[1]))
for src in re.findall(r'<script[^>]+src="([^":]+\.js)"', h):
    p = os.path.join(base, src)
    if os.path.exists(p):
        js += "\n" + open(p, encoding="utf-8").read()
open(sys.argv[2], "w", encoding="utf-8").write(js)
PY

if [ ! -s "$TMP" ]; then echo "NAO MEDI: nao achei <script> em $ARQ"; exit 2; fi

SAIDA="$("$BIN" --no-config-lookup -c "$CFG" "$TMP" 2>&1)"
ST=$?

# ⚠️ (set/2026, UNO dos Numeros) APP A MAO em JavaScript moderno: o parser ES5 para
#    em "The keyword 'const' is reserved" antes de conferir qualquer nome — e o
#    entregar.yml segurou a voz da casa por isso. Se o arquivo NAO e do motor (sem
#    conteudo.json ao lado) e o tropeco e de SINTAXE, confere com as MESMAS regras
#    em ES2020. Atividade do motor continua obrigada ao ES5.
if [ "$ST" != "0" ] && printf '%s' "$SAIDA" | grep -q "Parsing error" \
   && [ ! -f "$(dirname "$ARQ")/conteudo.json" ]; then
  CFG2="_qa/ferramentas/eslint.es2020.config.mjs"
  SAIDA="$("$BIN" --no-config-lookup -c "$CFG2" "$TMP" 2>&1)"
  ST=$?
  echo "   (app a mao em JavaScript moderno: conferido com as mesmas regras em ES2020)"
fi

# "outside of base path" = o ESLint NAO leu o arquivo. Isso e cegueira, nao aprovacao.
if printf '%s' "$SAIDA" | grep -q "outside of base path"; then
  echo "NAO MEDI: o ESLint recusou o arquivo (fora da base). Nada foi conferido."
  exit 2
fi

if [ "$ST" != "0" ]; then
  echo "$ARQ -> o ESLint reprovou:"
  printf '%s\n' "$SAIDA" | grep -E "error|warning" | grep -v "^$" | head -20 | sed 's/^/  /'
  echo "   (cada regra e o porque dela estao em _qa/ferramentas/eslint.config.mjs)"
  exit 1
fi

LINHAS=$(wc -l < "$TMP")
echo "$ARQ -> estatico ok: $LINHAS linhas de JS, nenhum nome nao-declarado nem armadilha conhecida."
exit 0
