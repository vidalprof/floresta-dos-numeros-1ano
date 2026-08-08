#!/usr/bin/env bash
# ============================================================
#  A PROVA DA ESTEIRA — do NADA ao index.html, e depois a banca.
#
#  Existe porque o "1h30" precisava de AFERICAO, nao de promessa. Ela monta
#  uma atividade de 32 fases com as 16 mecanicas juntas — o PIOR CASO para o
#  motor, e a unica situacao em que uma peca brigando com outra aparece.
#
#  ⚠️ `_prova30` NAO e conteudo para crianca: os textos sao os «...» do
#  esboco e o campo `mesa` diz isso com todas as letras. Ela existe para ser
#  RODADA sempre que se mexer no motor, no montador ou numa peca — nunca
#  publicada.
#
#  Uso:  bash _padrao/ESQUELETO/provar_esteira.sh
# ============================================================
set -uo pipefail
cd "$(dirname "$0")/../.."
rm -rf _prova30
python3 _padrao/ESQUELETO/esboco.py _prova30 \
  --ano "3º ano" --prefixo pv --titulo "A Prova do Esqueleto" --mascote nino || exit 1

# o montador COBRA `mesa` e a habilidade do curriculo por objetivo — e faz bem.
# Aqui elas entram automaticamente, porque esta atividade e afericao, nao aula.
python3 - <<'PY'
# -*- coding: utf-8 -*-
import json, io, collections
p = '_prova30/conteudo.json'
d = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
d['mesa'] = (u"PEDAGOGO ESPECIALISTA (3º ano — até o 5º ano quem manda na mesa é o "
             u"pedagogo, ver _padrao/RECEITA.md). PROVA DE ESTEIRA: este conteúdo "
             u"NÃO é para criança — existe só para medir o caminho esboço → montar "
             u"→ banca de ponta a ponta.")
d['voz'] = 'masculina'
hab = (u"Blumenau, 3º ano, Matemática — Números · objeto de conhecimento: Leitura, "
       u"escrita, comparação e ordenação de números naturais de quatro ordens — "
       u"HABILIDADE: “Ler, escrever e comparar números naturais de até a ordem de "
       u"unidade de milhar, estabelecendo relações entre os registros numéricos e "
       u"em língua materna.”")
cur = collections.OrderedDict()
for k in sorted(set(f.get('conceito') for f in d['fases'] if f.get('conceito'))):
    cur[k] = hab if k != 'livre' else u"SEM COBRANÇA — fase de fecho, não avalia nada."
d['curriculo'] = cur
io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
print("   mesa + %d objetivo(s) do curriculo preenchidos (afericao)" % len(cur))
PY

python3 _padrao/ESQUELETO/montar.py _prova30 || exit 1
echo "--- a banca ---"
bash _qa/auditar.sh _prova30/index.html
