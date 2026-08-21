# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE ARTE PRÓPRIA — "esta imagem é desta atividade mesmo?"
#
#  Ordem do Marcos (ago/2026): *"nunca copiar avatares, sempre ser temático,
#  nunca repetir o avatar, sempre novo e temático"*.
#
#  Ele pegou no olho: os avatares do Observatório do Órbi eram os brotinhos
#  verdes do Jardim do Broto, copiados para economizar geração de imagem — seis
#  brotos de horta de chapéu e laço no meio de um céu estrelado. A tela "Quem vai
#  jogar?" é onde a criança se coloca dentro da história; avatar emprestado
#  denuncia remendo logo na primeira tela.
#
#  REGRA DA CASA: clonar o MOTOR é obrigatório. Clonar a ARTE é proibido.
#
#  Como funciona: tira o hash de cada imagem da atividade e compara com as
#  imagens de TODAS as outras pastas de atividade. Byte a byte igual = copiada.
#
#  Uso: python3 _qa/arte_propria.py _orbi/index.html
#       (aceita a pasta também: python3 _qa/arte_propria.py _orbi)
# ============================================================
import hashlib, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pastas import e_atividade   # UM CEREBRO SO: quem e atividade e quem e area de servico

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/arte_propria.py <pasta-da-atividade|arquivo.html>")
    sys.exit(2)
pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
pasta = os.path.relpath(pasta)
img = os.path.join(pasta, "img")
if not os.path.isdir(img):
    print("%s -> sem pasta img/, nada a conferir" % pasta)
    sys.exit(0)

# imagens que a criança NÃO vê como identidade da atividade e podem repetir
LIVRES = ("icon-", "apple-touch-icon", "favicon")

# Pastas que são VERSÕES DA MESMA atividade (mesmo mascote, mesma história) —
# ali repetir arte não é copiar, é a própria arte dela. O "A Redação do Pingo"
# nasceu da junção de "_verbos" (Plantão na Redação) com "_generos" (A Banca do
# Pingo): o Pingo é o mascote das três. Só entra aqui com esse tipo de prova;
# na dúvida, é cópia e reprova.
MESMA_ATIVIDADE = [
    {"_redacao", "_verbos", "_generos"},
]

def parente(a, b):
    a, b = a.strip("/"), b.strip("/")
    return any(a in g and b in g for g in MESMA_ATIVIDADE)

def digere(caminho):
    h = hashlib.sha1()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()

minhas = {}
for p in sorted(glob.glob(os.path.join(img, "*"))):
    if not os.path.isfile(p) or os.path.basename(p).startswith(LIVRES):
        continue
    minhas.setdefault(digere(p), []).append(p)

# ⭐ ISENCAO DO BANCO (documentada no _banco/montar.py, mas nunca implementada
#    aqui — a Lojinha caiu nisso, ago/2026): objeto NEUTRO do banco e vocabulario
#    reutilizavel ("uma cenoura e uma cenoura em qualquer atividade"; um brinquedo
#    de loja idem). O banco so guarda objeto neutro (mascote/avatar/cenario ficam
#    de fora, regra do Marcos), entao imagem cujo sha esta no banco pode repetir
#    entre atividades — e foi o proprio Marcos que mandou "consultar o banco de
#    imagens ou outras atividades". Arte de TEMA continua reprovando (nao entra no
#    banco, logo nao ganha isencao).
banco_shas = set()
_bimg = os.path.join("_banco", "img")
if os.path.isdir(_bimg):
    for p in glob.glob(os.path.join(_bimg, "*")):
        if os.path.isfile(p):
            banco_shas.add(digere(p))

# todas as outras atividades = pastas irmãs que também tenham img/ e index.html
outras = []
for d in sorted(glob.glob("_*")):
    # ⚠️ `_novo` e a COPIA que vai ao ar. Sem esta linha o portao acusava as 28
    #    imagens da atividade como "copiadas de outra atividade" — dela mesma.
    if not e_atividade(d):
        continue
    if os.path.abspath(d) == os.path.abspath(pasta) or parente(d, pasta):
        continue
    if os.path.isdir(os.path.join(d, "img")) and os.path.isfile(os.path.join(d, "index.html")):
        outras.append(d)

copiadas = []
for d in outras:
    for p in glob.glob(os.path.join(d, "img", "*")):
        if not os.path.isfile(p) or os.path.basename(p).startswith(LIVRES):
            continue
        dg = digere(p)
        if dg in minhas and dg not in banco_shas:   # banco = objeto neutro, pode repetir
            for meu in minhas[dg]:
                copiadas.append((meu, p))

print("%s -> %d imagens conferidas contra %d outra(s) atividade(s)"
      % (pasta, len(minhas), len(outras)))
# ⚠️ REGRA MUDOU (Marcos, ago/2026): "mascote e imagens do banco podem ser
#    reaproveitados". Reuso deixou de ser ERRO — este portão virou INFORMATIVO
#    (sempre exit 0). Ele só LISTA o que está reaproveitado, para ficar visível.
#    Quem ainda pega resto de clone de verdade (prefixo de OUTRA atividade
#    vazando) é o `_qa/clone.py` item 8, que continua reprovando.
if not copiadas:
    print("   arte ok: nada reaproveitado de outra atividade")
    sys.exit(0)
print("   %d imagem(ns) REAPROVEITADA(S) de outra atividade (permitido — regra do banco):" % len(copiadas))
for meu, dele in sorted(copiadas):
    print("    %s  ==  %s" % (meu, dele))
print("   (reuso é OK agora; ideal é vir do _banco. Mascote novo só quando o Marcos pedir.)")
sys.exit(0)
