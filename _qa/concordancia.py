# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 0r2 — CONCORDÂNCIA nas falas (o que a criança OUVE)

 ⚠️ O DEFEITO, e quem o encontrou foi o MARCOS, com uma pergunta que nem era
    sobre isso (14/set/2026): *"é que falou de célula única etc em uma folha, não
    sei se isso o 4 ano já sabe, se é do nível deles"*. Fui conferir a folha da
    célula e esbarrei noutra coisa, pior: **49 das 323 falas da Coroa dos Cinco
    Reinos estavam com a concordância errada**, e falas viram MP3 — a criança
    OUVIA aquilo:

      "Certo! A borboleta é do reino DAS ANIMAIS."
      "Ligado! OS COGUMELOS MORA no reino das fungos."
      "Focou! APARECEU os cogumelos."

    A causa é de molde, não de digitação: dezesseis frases do gerador escreviam
    *"do reino das %s"* com o artigo FIXO, e dois dos cinco reinos são
    masculinos; e os modelos que começam pelo nome da figura fixavam o verbo no
    singular, mas uma das figuras se chama *"os cogumelos"*.

 ⚠️ E POR QUE O REVISOR (0r) NÃO VIU: ele procura erro de DIGITAÇÃO e palavra
    que a voz erra. Concordância entre artigo e substantivo, e entre sujeito e
    verbo, ninguém media. Texto gerado por molde é exatamente onde esse erro
    nasce — porque o molde está certo para um valor e errado para outro, e o
    olho passa batido pelas 47 vezes em que ele está certo.

 O QUE ELE MEDE, em `<pasta>/falas.json` (que é a VERDADE do que vira voz):

   1. ARTIGO × GÊNERO   — "das animais" (animais é masculino) reprova.
   2. SUJEITO PLURAL × VERBO SINGULAR — "Os cogumelos mora" reprova.

 ⚠️ E O QUE ELE **NÃO** FAZ: gramática de português inteira. Ele só julga as
    palavras que conhece, de um dicionário DECLARADO aqui embaixo; palavra que
    não está no dicionário ele **não acusa** — lista como "não sei esta" e segue.
    Isso é de propósito: a casa já pagou caro por portão que acusa inocente (o
    `silaba_fonte.py` reprovou 21 recortes legítimos, e portão que acusa inocente
    é portão que a gente aprende a pular). Dicionário novo = linha nova aqui.

 Uso:  python3 _qa/concordancia.py <pasta>
 Código 0 = passou · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

# ---- O DICIONÁRIO DECLARADO. Só o que está aqui é julgado.
#      "m" = masculino · "f" = feminino. Só palavras no PLURAL, que é onde o
#      artigo "dos/das" aparece.
GENERO = {
    u"animais": u"m", u"fungos": u"m", u"cogumelos": u"m", u"seres": u"m",
    u"bichos": u"m", u"reinos": u"m", u"minúsculos": u"m", u"decompositores": u"m",
    u"produtores": u"m", u"consumidores": u"m", u"grandes": None,   # os dois gêneros
    u"plantas": u"f", u"algas": u"f", u"bactérias": u"f", u"células": u"f",
    u"folhas": u"f", u"flores": None, u"figuras": u"f", u"palavras": u"f",
    u"letras": u"f", u"sílabas": u"f", u"coisas": u"f", u"partes": u"f",
    u"frutas": u"f", u"cores": u"f", u"pedras": u"f", u"nuvens": u"f",
}

# ---- Os verbos que os moldes da casa usam depois do nome da figura.
#      singular -> plural. Lista FECHADA: verbo que não está aqui não é julgado.
VERBO = {
    u"é": u"são", u"está": u"estão", u"tem": u"têm", u"mora": u"moram",
    u"vive": u"vivem", u"fabrica": u"fabricam", u"precisa": u"precisam",
    u"come": u"comem", u"guarda": u"guardam", u"nasce": u"nascem",
    u"cresce": u"crescem", u"apareceu": u"apareceram", u"ficou": u"ficaram",
    u"virou": u"viraram", u"foi": u"foram", u"faz": u"fazem", u"pode": u"podem",
    u"serve": u"servem", u"anda": u"andam", u"voa": u"voam", u"nada": u"nadam",
}


def limpa(t):
    t = re.sub(r"<[^>]+>", u" ", t or u"")
    return re.sub(r"\s+", u" ", t).strip()


def olha(texto):
    u"""Devolve (erros, palavras que não conheço) de uma fala."""
    t = limpa(texto)
    erros, nao_sei = [], set()

    # 1) artigo x gênero: "dos/das <palavra>"
    for art, pal in re.findall(r"\b(dos|das|nos|nas|aos|às)\s+([A-Za-zÀ-ÿ]+)", t, re.I):
        chave = pal.lower()
        if chave not in GENERO:
            nao_sei.add(chave)
            continue
        g = GENERO[chave]
        if g is None:
            continue
        masc = art.lower() in (u"dos", u"nos", u"aos")
        if masc and g == u"f":
            erros.append(u"«%s %s» — %s é feminino" % (art, pal, pal))
        if (not masc) and g == u"m":
            erros.append(u"«%s %s» — %s é masculino" % (art, pal, pal))

    # 2) sujeito plural x verbo singular: "Os/As <palavra> <verbo singular>"
    for art, pal, vb in re.findall(
            r"\b(Os|As)\s+([A-Za-zÀ-ÿ]+)\s+(?:não\s+)?([a-zà-ÿ]+)", t):
        chave = vb.lower()
        if chave in VERBO:
            erros.append(u"«%s %s … %s» — sujeito no plural pede «%s»"
                         % (art, pal, vb, VERBO[chave]))
    return erros, nao_sei


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/concordancia.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"falas.json")
    if not os.path.exists(cam):
        print(u"%s -> NAO SE APLICA: sem falas.json (nao ha texto de voz para medir)."
              % pasta)
        return 2
    try:
        falas = json.load(io.open(cam, encoding=u"utf-8"))
    except Exception as e:
        print(u"%s -> NAO MEDI: falas.json nao e JSON valido (%s)." % (pasta, e))
        return 2
    if isinstance(falas, dict):
        falas = [{u"id": k, u"texto": v} for k, v in falas.items()]

    achados, nao_sei = [], set()
    for f in falas:
        e, n = olha(f.get(u"texto", u""))
        nao_sei |= n
        for x in e:
            achados.append((f.get(u"id", u"?"), x, limpa(f.get(u"texto", u""))))

    print(u"%s -> concordancia: %d fala(s) conferida(s) contra um dicionario "
          u"declarado de %d substantivo(s) e %d verbo(s)"
          % (pasta, len(falas), len(GENERO), len(VERBO)))
    if nao_sei:
        print(u"   %d palavra(s) que o dicionario NAO conhece (nao acusei nenhuma): %s"
              % (len(nao_sei), u", ".join(sorted(nao_sei)[:14])))
    if achados:
        print(u"   %d FALA(S) COM CONCORDANCIA ERRADA — e fala vira mp3, entao a "
              u"crianca OUVE isto:" % len(achados))
        vistos = set()
        for i, (ident, erro, txt) in enumerate(achados):
            if erro in vistos and i > 12:
                continue
            vistos.add(erro)
            print(u"    x %s" % erro)
            print(u"      %s" % txt[:110])
            if i >= 14:
                print(u"      ... e mais %d" % (len(achados) - i - 1))
                break
        print(u"   conserto: o erro quase sempre esta no MOLDE que gera a frase, nao")
        print(u"   numa fala solta — procure o `%s` fixo no gerador de falas da pasta.")
        return 1
    print(u"   ok: nenhum erro de concordancia nas palavras que o dicionario conhece")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
