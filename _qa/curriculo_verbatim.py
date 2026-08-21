# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "essa habilidade foi mesmo COPIADA do currículo?"

 ⚠️ LIÇÃO PAGA (ago/2026). O `conteudo.json` da Padaria das Letras diz, com
 todas as letras, no campo `mesa`:

     "Habilidades copiadas verbatim do _curriculo/blumenau.txt
      (1º ano, Língua Portuguesa, Análise linguística/semiótica)"

 Sete objetivos, cada um com a habilidade entre aspas. Cinco conferem. **Dois
 não existem no currículo** — foram escritos por mim e ganharam a etiqueta de
 "verbatim" junto com os outros, no mesmo bloco, sem que ninguém notasse.

 Isto é pior que um defeito de tela. Uma tela torta o professor vê e manda
 arrumar; uma citação falsa de currículo ele NÃO tem como conferir sem abrir
 440 páginas de PDF — e é justamente o que ele mostra à coordenação para provar
 que a atividade está alinhada. Inventar a fonte é quebrar a única coisa que ele
 não pode auditar sozinho.

 ⚠️ E O QUE ESTE PORTÃO **NÃO** FAZ, dito antes de qualquer número: ele NÃO
 confere a frase inteira. O `_curriculo/blumenau.txt` foi extraído do PDF com
 `pdftotext -layout`, que preserva COLUNAS: uma frase da tabela do currículo
 chega aqui partida, com texto de outra coluna no meio. Procurar a frase inteira
 acusaria as SETE — inclusive as cinco corretas. Portão que acusa inocente é
 portão que se aprende a ignorar, e essa lição já custou caro nesta casa.

 O QUE ELE FAZ, e é uma pergunta que não tem resposta ambígua: **cada palavra
 marcante da citação existe em algum lugar do currículo?** Uma frase copiada de
 um documento não pode conter uma palavra que o documento não tem. Foi assim que
 o objetivo 6 caiu: a habilidade dele fala em palavras que "rimam", e a palavra
 **rimam** não aparece UMA vez nas 440 páginas.

 Uso: python3 _qa/curriculo_verbatim.py <pasta-da-atividade> [curriculo.txt]
============================================================
"""
import io
import json
import os
import re
import sys
import unicodedata

# palavras curtas e de ligação não distinguem nada: "das", "com", "que".
# O corte em 5 letras deixa de fora conjugação rara sem perder o essencial.
TAMANHO_MINIMO = 5

# palavras que a CASA usa ao redor da citação e que podem legitimamente não
# estar no currículo (são rótulo nosso, não texto dele).
NOSSAS = set(u"""habilidade habilidades objeto conhecimento conceitos conteudos
    campos atuacao analise linguistica semiotica alfabetizacao ano lingua
    portuguesa blumenau todos""".split())


def achata(s):
    s = unicodedata.normalize("NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", u" ", s.lower())


# a citação da habilidade vem entre aspas curvas ou retas, depois de HABILIDADE:
_CITACAO = re.compile(u'HABILIDADE\\s*:\\s*[“"]([^”"]+)[”"]')


def citacoes(o, chave=None, achados=None):
    u"""toda string do conteúdo que se apresenta como habilidade citada."""
    if achados is None:
        achados = []
    if isinstance(o, dict):
        for k, v in o.items():
            citacoes(v, k, achados)
    elif isinstance(o, list):
        for v in o:
            citacoes(v, chave, achados)
    elif isinstance(o, str):
        for m in _CITACAO.finditer(o):
            achados.append((chave or u"?", m.group(1).strip()))
    return achados


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/curriculo_verbatim.py <pasta> [curriculo.txt]")
        return 2
    pasta = sys.argv[1].rstrip("/")
    cam = os.path.join(pasta, "conteudo.json")
    cur = sys.argv[2] if len(sys.argv) > 2 else "_curriculo/blumenau.txt"

    if not os.path.exists(cam):
        print(u"%s -> sem conteudo.json (atividade escrita a mao?): NAO MEDI "
              u"se as habilidades sao do curriculo." % pasta)
        return 2
    if not os.path.exists(cur):
        print(u"%s -> nao achei o curriculo em %s: NAO MEDI NADA "
              u'(isso nao e "passou").' % (pasta, cur))
        return 2

    d = json.load(io.open(cam, encoding="utf-8"))
    ach = citacoes(d)
    if not ach:
        print(u"%s -> nenhuma habilidade citada entre aspas. NAO MEDI." % pasta)
        return 2

    palavras = set(achata(io.open(cur, encoding="utf-8").read()).split())
    ruins, ok = [], 0
    for chave, frase in ach:
        fora = [p for p in achata(frase).split()
                if len(p) >= TAMANHO_MINIMO and p not in NOSSAS
                and p not in palavras]
        if fora:
            ruins.append((chave, frase, sorted(set(fora))))
        else:
            ok += 1

    print(u"%s -> %d habilidade(s) citada(s), conferidas contra %s"
          % (pasta, len(ach), cur))
    if not ruins:
        print(u"   curriculo ok: toda palavra marcante das citacoes existe no "
              u"documento")
        return 0

    print(u"   %d CITACAO(OES) QUE O CURRICULO NAO TEM COMO TER DITO:"
          % len(ruins))
    for chave, frase, fora in ruins:
        print(u'    [%s] "%s"' % (chave, frase[:76]))
        print(u"        palavra(s) que NAO existem no curriculo inteiro: %s"
              % u", ".join(fora))
    print(u"   conserto: abrir o %s, achar a habilidade DE VERDADE e colar" % cur)
    print(u"   ela. Se a habilidade que a atividade ensina nao estiver la, dizer")
    print(u"   isso — 'inspirada em' e honesto; 'verbatim' inventado nao e. O")
    print(u"   professor mostra isto para a coordenacao e nao tem como conferir.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
