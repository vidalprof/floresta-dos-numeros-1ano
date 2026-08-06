# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE NARRACAO — "a voz vai falar isso direito?"
#
#  Nasceu de um erro pago DUAS VEZES (o Marcos ouviu e avisou nas duas):
#    - na Redacao do Pingo (jul/2026) e de novo na Doceria (ago/2026) o
#      edge-tts pt-BR leu "Complete" como "COMPLITE" (som de ingles).
#  A voz e gerada num workflow e so da para ouvir depois de publicar, entao
#  o erro so aparece na sala de aula. Este auditor pega ANTES: le o
#  _lote_falas.json (ou o JSON que voce passar) e reprova palavra que a voz
#  ja errou, sugerindo a troca.
#
#  ⚠️ REGRA: quando descobrir uma palavra nova que a voz erra, ACRESCENTE
#  aqui na hora — e assim que este auditor fica esperto.
#
#  Uso: python3 _qa/falas.py _lote_falas.json
# ============================================================
import json, re, sys

# palavra problematica -> (como a voz le, o que usar no lugar)
ARMADILHAS = {
    "complete":  ("complite (som de ingles)", "preencha / vamos preencher / termine"),
    "completa":  ("complita", "preenche / termina"),
    "completar": ("complitar", "preencher / terminar"),
    "delete":    ("delite", "apague"),
    "update":    ("apdeite", "atualize"),
    "online":    ("onlaine", "na internet"),
    "design":    ("dezaine", "desenho"),
    "site":      ("saite (as vezes 'site' mesmo)", "pagina / endereco"),
    "mouse":     ("maus", "mouse (ok, mas confira)"),
    "e-mail":    ("e-mail cortado", "correio eletronico"),
}

arq = sys.argv[1] if len(sys.argv) > 1 else "_lote_falas.json"
itens = json.load(open(arq, encoding="utf-8"))

achados = []
for it in itens:
    texto = it.get("texto", "")
    for palavra, (erro, troca) in ARMADILHAS.items():
        if re.search(r"\b%s\b" % re.escape(palavra), texto, re.I):
            achados.append((it.get("id", "?"), palavra, erro, troca, texto))

print("%s -> %d falas conferidas" % (arq, len(itens)))
if not achados:
    print("   narracao ok: nenhuma palavra da lista de armadilhas")
    sys.exit(0)
print("   %d FALA(S) COM PALAVRA QUE A VOZ ERRA:" % len(achados))
for ident, palavra, erro, troca, texto in achados:
    print("    [%s] \"%s\" -> a voz fala \"%s\"" % (ident, palavra, erro))
    print("        troque por: %s" % troca)
    print("        na fala: %s" % texto[:90])
sys.exit(1)
