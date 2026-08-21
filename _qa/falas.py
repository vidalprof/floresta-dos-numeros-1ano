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
#  Uso (banca):    python3 _qa/falas.py _lote_falas.json
#  Uso (montador): from falas import checa; checa(lista_de_falas)
# ============================================================
import json
import re
import sys

# palavra problematica -> (como a voz le, o que usar no lugar)
ARMADILHAS = {
    "tangram":   ("enfase/pronuncia errada na voz", "tangram (na VOZ escreva 'tangram' foneticamente; o Marcos pegou, ago/2026)"),
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

# ⚠️ ARMADILHA DE OUTRA FAMILIA (ago/2026), e foi o Marcos quem ouviu:
#    *"o E tem que ser dito somente 'e'; e nas 'qual nao rima' tem que dizer
#    bem certinho o som, ex: EL"*.
#    Aqui nao e palavra estrangeira: e a voz lendo O NOME DA LETRA quando a
#    fase precisa do SOM dela. "terminam com o som EL" sai "terminam com o som
#    ÉLE" — o nome da letra L. A crianca do 1o ano esta justamente aprendendo a
#    diferenca entre o NOME e o SOM da letra; ouvir o nome no lugar do som
#    ensina o contrario do que a fase quer.
#    O conserto e escrever a fala como a voz tem que DIZER, nao como se
#    escreve: "o som ÉL", "o som ÃO", "o som ATO" — sempre em minusculas e com
#    acento, porque a caixa alta empurra a voz para soletrar.
SONS_SOLETRADOS = re.compile(
    r"\bsom\s+(?:d[eo]\s+)?([A-ZÃÂÁÉÊÍÓÔÕÚÇ]{1,3})\b")
# ⚠️ ERA {1,4} e virou {1,3} (ago/2026), depois de medir a Padaria: a regra
#    acusava "o som de BOLO" e "o som de PATO". Palavra inteira em caixa alta a
#    voz LE como palavra — e a casa escreve palavra em caixa alta em todo lugar
#    ("BOLO", "QUEIJO"). Quem soletra e o pedaco CURTO ("BO" vira "be-o"), e os
#    exemplos do proprio manual desta regra tem 1 a 3 letras: EL, AO, ATO.
#    Portao barulhento e portao que se aprende a ignorar — o ruido aqui custava
#    mais que o defeito.


def sons_lidos_como_letra(texto):
    u"""devolve os pedaços em que a fala manda a voz dizer o NOME da letra."""
    return [m.group(1) for m in SONS_SOLETRADOS.finditer(texto or u"")]


def checa(itens):
    u"""Confere uma lista de falas ({id, texto}) e devolve os achados como
    tuplas (id, palavra, como_a_voz_le, troca_sugerida, texto). Lista vazia =
    narracao ok. ⭐ E a MESMA funcao que o `montar.py` chama ao montar, para o
    defeito aparecer NA HORA e nao so na banca de 20 min — uma fonte de verdade,
    nunca duas listas (licao paga: 'lista em dois lugares vira duas listas')."""
    achados = []
    for it in itens:
        texto = it.get("texto", "")
        for palavra, (erro, troca) in ARMADILHAS.items():
            if re.search(r"\b%s\b" % re.escape(palavra), texto, re.I):
                achados.append((it.get("id", "?"), palavra, erro, troca, texto))
        # ⚠️ LICAO PAGA (ago/2026): NOME DE ARQUIVO NA FILA DE GRAVACAO.
        #    O montador tinha uma lista de "chaves que nao sao fala" com `img`
        #    dentro, mas sem `fig`/`foto`/`cena` — e a familia inteira existia,
        #    completa, 120 linhas abaixo no mesmo arquivo. Resultado medido na
        #    Padaria: DOZE falas mandadas gravar dizendo "pê-dê bolo", "pê-dê
        #    queijo". Nao quebrava nada e ninguem via: so gastava voz.
        #    O portao pergunta a coisa obvia que faltava — "isto e frase para uma
        #    crianca ouvir, ou e nome de arquivo?".
        if re.match(r"^[a-z]{2,4}_[a-z0-9_]+$", texto.strip()):
            achados.append((it.get("id", "?"), texto.strip(),
                            u"a voz vai LER o nome do arquivo, letra por letra",
                            u"isto nao e fala: e chave de imagem. Tire da fila de "
                            u"gravacao (CHAVES_MUDAS no montar.py)",
                            texto))
        for pedaco in sons_lidos_como_letra(texto):
            achados.append((it.get("id", "?"), u"som %s" % pedaco,
                            u"a voz diz o NOME da letra, nao o SOM",
                            u'escreva como se fala: "o som %s"' % pedaco.lower(),
                            texto))
    return achados


if __name__ == "__main__":
    arq = sys.argv[1] if len(sys.argv) > 1 else "_lote_falas.json"
    itens = json.load(open(arq, encoding="utf-8"))
    achados = checa(itens)
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
