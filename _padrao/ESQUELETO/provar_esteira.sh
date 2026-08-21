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

# ============================================================
#  ⚠️ POR QUE AQUI NAO RODA A BANCA INTEIRA — e a licao que custou uma rodada.
#  Rodei `auditar.sh` na `_prova30` e ela REPROVOU. Fui ver: 11 figuras que nao
#  existem, 6 fases mudas, 14 alto-falantes sem gravacao. Tudo VERDADE, e tudo
#  esperado: a `_prova30` e um ESQUELETO — nunca teve arte gerada nem voz
#  gravada, e os textos sao os «...» do esboco.
#  A banca esta certa em reprovar (atividade sem arte e sem voz nao vai para
#  crianca nenhuma). Errado seria eu gerar 11 imagens e ~270 vozes para uma
#  afericao descartavel: dinheiro e uma corrida de workflow jogados fora, e
#  contra a regra da cartela.
#  Entao a prova mede o que ELA existe para medir: a ESTRUTURA. Os portoes de
#  arte e de voz ficam de fora, e ficam de fora DITOS — portao pulado em
#  silencio e o comeco de toda aprovacao vazia.
# ============================================================
# ⭐ A PROVA DO CAMINHO DA VOZ — opcional, `--com-voz`.
#    Ela nao gera MP3 nenhum (isso custa dinheiro e fica de fora, como esta
#    dito acima): mede a LISTA. O `colher.py` joga a atividade, anota todo
#    texto que aparece e diz o que ainda nao tem voz; o montador refaz o
#    `falas.json`. Aqui a prova e que o ciclo CONVERGE — foi 32 -> 2 -> 0 na
#    medicao de ago/2026, e o portao fecha.
#    Fica fora do padrao porque sao ~15 minutos de jogador: a esteira de todo
#    dia mede a estrutura em ~5. Quem mexer no colher, no jogador ou na ponte
#    das pecas roda com `--com-voz`.
if [ "${1:-}" = "--com-voz" ]; then
  echo
  echo "--- PROVA DO CAMINHO DA VOZ (colher -> montar, ate fechar) ---"
  vok=0
  for volta in 1 2 3; do
    python3 _padrao/ESQUELETO/colher.py _prova30 --so-ver > /tmp/_ev.txt 2>&1
    if [ $? = 0 ]; then echo "   volta $volta: a voz ja cobre o que aparece jogando"; vok=1; break; fi
    grep -c "^      +" /tmp/_ev.txt | sed "s/^/   volta $volta: /;s/$/ fala(s) faltando — colhendo/"
    python3 _padrao/ESQUELETO/colher.py _prova30 > /dev/null 2>&1
    python3 _padrao/ESQUELETO/montar.py  _prova30 > /dev/null 2>&1
  done
  if [ "$vok" = "1" ]; then echo "   ok   caminho da voz (o ciclo converge e o portao fecha)"
  else echo "   FALHOU o caminho da voz: nao fechou em 3 voltas"; exit 1; fi
fi

ARQ=_prova30/index.html
falhou=0
rodar(){ # rodar "<nome>" <comando...>
  local nome="$1"; shift
  "$@" > /tmp/pe_gate.txt 2>&1
  local ec=$?
  # ⚠️ convencao da casa: 0 = passou, 1 = REPROVOU, 2 = NAO DEU PARA MEDIR.
  #    A _prova30 e o esqueleto de exemplo e NAO tem par palavra+figura, entao
  #    o portao 'figura combina' devolve 2 (honestamente: nada a medir). Contar
  #    isso como FALHOU derrubava a prova da esteira por um portao que nem se
  #    aplica a este exemplo. NAO MEDI vira 'n/a', nao reprovacao.
  if [ "$ec" = "0" ]; then
    echo "   ok   $nome"
  elif [ "$ec" = "2" ]; then
    echo "   n/a  $nome (nao se aplica ao exemplo — nao mediu)"
  else
    echo "   FALHOU  $nome"; sed -n '1,6p' /tmp/pe_gate.txt | sed 's/^/        /'
    falhou=1
  fi
}
echo "--- OS PORTOES DE ESTRUTURA (arte e voz ficam de fora, ver acima) ---"
rodar "engenheiro (o codigo roda)"      bash -c "python3 - <<'P'
import io,re,subprocess,sys
s=io.open('$ARQ',encoding='utf-8').read()
js='\n'.join(re.findall(r'<script>(.*?)</script>', s, re.S))
io.open('/tmp/pe.js','w',encoding='utf-8').write(js)
sys.exit(subprocess.call(['node','--check','/tmp/pe.js']))
P"
rodar "funcao que nao existe"           python3 _qa/funcoes.py   "$ARQ"
rodar "pedagogo (a escada sobe?)"       python3 _qa/pedagogo.py  "$ARQ"
rodar "padrao da casa"                  python3 _qa/padrao.py    "$ARQ"
rodar "dinamicas (armadilhas)"          python3 _qa/dinamicas.py "$ARQ"
rodar "cobertura por objetivo"          python3 _qa/cobertura.py "$ARQ"
rodar "resto de clone"                  python3 _qa/clone.py     "$ARQ"
# ⚠️ o beco de fim de fase: a tela de BANCADA da peca ("PECA FECHADA", botao
#    "Jogar de novo") virando fim de linha na fase 3 de 32.
rodar "beco sem saida (a fase continua?)" python3 _qa/beco.py    "$ARQ"
rodar "vazamento (cabe no cartao?)"      node _qa/vaza.js       "$ARQ"
rodar "figura combina com a palavra"     python3 _qa/figura_certa.py _prova30
rodar "toda voz e gravada (sem robo)"    python3 _qa/vozrobo.py  "$ARQ"
rodar "promessa"                        python3 _qa/promessa.py  "$ARQ"
rodar "fluxo (da para chegar ao fim?)"  python3 _qa/fluxo.py     "$ARQ" telaCapa
rodar "classes sem estilo"              python3 _qa/classes.py   "$ARQ"
rodar "progressao (a barra so anda?)"   python3 _qa/progressao.py "$ARQ"
rodar "diretor de arte (acabamento)"    node   _qa/visual.js     "$ARQ"
rodar "jogador (joga sozinho)"          node   _qa/jogador.js    "$ARQ"

echo "-----------------------------------------------------------"
if [ "$falhou" = "0" ]; then
  echo " ESTEIRA OK — do nada ao index.html, e a ESTRUTURA passa nos 13 portoes."
  echo " (arte e voz nao foram medidas: a _prova30 nao tem nem uma nem outra)"
else
  echo " ESTEIRA COM DEFEITO — conserte antes de montar atividade nova."
fi
exit "$falhou"
