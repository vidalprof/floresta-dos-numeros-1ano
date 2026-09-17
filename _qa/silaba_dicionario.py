# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1w — A SILABA CONFERIDA CONTRA UM DICIONARIO DE VERDADE

 ⭐ PERGUNTA DO MARCOS (17/set/2026): *"existe algum banco de audio em portugues,
    para vc comparar e checar se as silabas e palavras estao corretas na
    atividade?"*

 A resposta honesta era: as divisoes do `silabas.json` saiam da MINHA cabeca.
 Nada as conferia. E divisao silabica errada nao da erro em lugar nenhum — o
 app abre, a voz sai, e a crianca ouve o pedaco errado com toda a naturalidade
 do mundo. E exatamente o tipo de defeito que a REGRA ZERO proibe.

 O BANCO QUE EXISTE E DA PARA USAR DAQUI: o dicionario de hifenizacao pt_BR do
 LibreOffice/OpenOffice, empacotado no `pyphen` (PyPI alcanca do chat; o
 HuggingFace e o alphacephei nao — medido em 17/set/2026). Nao e um banco de
 AUDIO: e um banco de TEXTO, publicado, usado por todo editor de texto em
 portugues ha vinte anos.

 ⚠️⚠️ E ELE TEM UM LIMITE QUE PRECISA ESTAR ESCRITO, senao o portao vira medida
    falsa: um dicionario de HIFENIZACAO serve para quebrar linha, e por isso ele
    DE PROPOSITO cala alguns cortes validos — nunca deixa uma letra sozinha na
    ponta. Para `amor`, cuja divisao e A-MOR, ele nao oferece corte nenhum.

    Entao a regra deste portao e de MAO UNICA:
      · o dicionario ACUSA um corte que eu nao tenho  -> isso e forte, reprova;
      · o dicionario tem MENOS cortes do que eu       -> isso nao diz nada.
    Ele so acusa; nunca manda.

 O QUE ELE MEDE, exatamente: cada pedaco que o app FALA SOZINHO (o `SILMAP` do
 `index.html`, que e o que vira botao para a crianca). Se o dicionario ainda
 corta aquele pedaco, ele nao e uma silaba — e um pedaco de exercicio. Isso
 pode ser legitimo (a folha de papel manda juntar CAMA + LEAO), mas tem de
 estar DECLARADO em `<pasta>/silabas-ok.json`, com o motivo, do mesmo jeito que
 o `img/SOBRA-OK.json`.

 ⚠️ O QUE ELE NAO MEDE: se o mp3 diz o que esta escrito. Isso e ASR (voz ->
    texto) e o modelo mora no HuggingFace, que o chat nao alcanca — tem de ser
    no runner do Actions. Enquanto isso, este portao NAO e "o audio conferido".

 Uso:  python3 _qa/silaba_dicionario.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import subprocess
import sys



# ══════════════════════════════════════════════════════════════════════
#  O SEGUNDO BANCO — `espeak-ng`, e ele cobre o ponto CEGO do primeiro
#
#  Medido em 17/set/2026, nas 368 palavras dos nove cadernos que falam silaba:
#
#   · o `pyphen` (hifenizacao) so pode ACUSAR corte a mais, nunca exigir corte
#     — e por isso ele nao ve a divisao GROSSA DEMAIS (BI-GODE, que tem tres
#     silabas, passou batido por ele);
#   · o `espeak-ng` diz a PRONUNCIA (IPA) e dela se contam os nucleos
#     vocalicos — que e quantas silabas a palavra tem. Ele viu as catorze.
#
#  Os dois erram em lugares OPOSTOS, e e por isso que os dois estao aqui.
#
#  ⚠️ E O ESPEAK NAO E AUTORIDADE EM SILABA, so em som. Medido: ele junta o
#     HIATO final de `-io`, `-ia`, `-iao` num ditongo so — RIO (`xˈiʊ`), NAVIO,
#     AVIAO, PIAO saem com uma silaba a menos. Nessas SEIS palavras quem esta
#     certo sou eu, e por isso a familia esta declarada abaixo em vez de
#     virar reprovacao.
#
#  ⚠️ E ele insere um SCHWA depois do R travado (BORBOLETA -> `bˌoɾəbolˈetæ`),
#     que nao e silaba nenhuma: e regra do motor dele. Tirado antes de contar.
#
#  ⚠️ O QUE NENHUM DOS DOIS FAZ: ouvir o mp3. Isso e o `_qa/ouvir_silaba.py`,
#     e ali a noticia e ruim — medido com TRES reconhecedores diferentes
#     (wav2vec2 pt, Whisper, allosaurus), nenhum le um recorte de 250 ms com
#     confianca. A defesa do audio continua sendo o alinhador, a duracao, e
#     estes dois bancos de TEXTO.
# ══════════════════════════════════════════════════════════════════════
VOG = u"aeiou\u0250\u025b\u0254\u0259\u0268\u028a\u026a\u026f\u00e6\u0275\u00f8y\u0264\u028c\u0251\u0252\u0153\u025c"
ALTAS = u"i\u026au\u028ay\u026fwj"
TON = u"\u02c8\u02cc"
# a familia que o espeak junta e eu nao: o hiato final -io / -ia / -iao
_HIATO = re.compile(u"(i[oa]|i[a\u00e3]o)$", re.I)


def _ipa(palavra):
    u"""a pronuncia do espeak-ng, ou None se ele nao estiver instalado."""
    try:
        saida = subprocess.check_output(
            [u"espeak-ng", u"-v", u"pt-br", u"-q", u"--ipa", palavra],
            stderr=subprocess.STDOUT)
    except (OSError, subprocess.CalledProcessError):
        return None
    return saida.decode(u"utf-8").strip()


def _nucleos(ipa):
    u"""quantas silabas a pronuncia tem — um nucleo vocalico por silaba."""
    ipa = re.sub(u"([\u027er x\u0281])\u0259", u"\\1", ipa)   # o schwa do R travado
    n, i = 0, 0
    while i < len(ipa):
        if ipa[i] in VOG or (ipa[i] in TON and i + 1 < len(ipa) and ipa[i + 1] in VOG):
            grupo, ton = [], []
            while i < len(ipa):
                t = False
                if ipa[i] in TON:
                    if i + 1 < len(ipa) and ipa[i + 1] in VOG:
                        t = True
                        i += 1
                    else:
                        break
                if i < len(ipa) and ipa[i] in VOG:
                    grupo.append(ipa[i])
                    ton.append(t)
                    i += 1
                    while i < len(ipa) and ipa[i] in u"\u0303\u02d0\u02d1\u032f":
                        i += 1
                else:
                    break
            k = 0
            for j, v in enumerate(grupo):
                # vogal alta ATONA ao lado de outra e semivogal (VIAGEM, MEIA);
                # alta TONICA e nucleo proprio (DI-A, LU-A, RI-O)
                if v in ALTAS and not ton[j] and len(grupo) > 1:
                    continue
                k += 1
            n += max(1, k)
        else:
            i += 1
    return n


def conta_espeak(pasta, ok_dec):
    u"""Devolve (codigo, linhas). Compara quantas silabas eu registrei com
    quantos nucleos a pronuncia tem."""
    sj = os.path.join(pasta, u"silabas.json")
    if not os.path.exists(sj):
        return 2, [u"   (contagem) sem `silabas.json`: NAO MEDI"]
    try:
        P = json.load(io.open(sj, encoding=u"utf-8")).get(u"palavras") or {}
    except ValueError:
        return 2, [u"   (contagem) `silabas.json` ilegivel: NAO MEDI"]
    if not P:
        return 0, [u"   (contagem) nenhuma palavra registrada"]
    if _ipa(u"teste") is None:
        return 2, [u"   (contagem) sem o `espeak-ng` (apt-get install espeak-ng): "
                   u"NAO MEDI — e isto nao e 'passou'"]

    grossas, declaradas, hiatos = [], [], []
    for w in sorted(P):
        fala = _ipa(w)
        if not fala:
            continue
        n, meu = _nucleos(fala), len(P[w])
        if n == meu:
            continue
        if n < meu:
            # eu dividi de MAIS. Nas seis palavras da familia -io/-iao quem
            # esta certo sou eu: o espeak junta o hiato.
            if _HIATO.search(w):
                hiatos.append((w, meu, n, fala))
            else:
                grossas.append((w, u"-".join(P[w]), meu, n, fala, True))
        else:
            alvo = declaradas if w.upper() in ok_dec or w in ok_dec else grossas
            alvo.append((w, u"-".join(P[w]), meu, n, fala, False))

    L = []
    duros = [x for x in grossas if not x[5]]
    if duros:
        L.append(u"   (contagem) REPROVADO: %d palavra(s) registradas com MENOS "
                 u"silabas do que a pronuncia tem:" % len(duros))
        for w, div, meu, n, fala, _ in duros:
            L.append(u"      • %-12s eu %d (%s) · espeak %d nucleos · %s"
                     % (w.upper(), meu, div, n, fala))
        L.append(u"   conserto: divida certo no `gerar_falas.py` (`_reg`), ou "
                 u"declare em %s/silabas-ok.json se for pedaco da folha de papel."
                 % pasta)
    outros = [x for x in grossas if x[5]]
    if outros:
        L.append(u"   (contagem) REPROVADO: %d palavra(s) com MAIS silabas do "
                 u"que a pronuncia — e aqui o erro e meu:" % len(outros))
        for w, div, meu, n, fala, _ in outros:
            L.append(u"      • %-12s eu %d (%s) · espeak %d · %s"
                     % (w.upper(), meu, div, n, fala))
    if not grossas:
        L.append(u"   ✓ (contagem) as %d palavra(s) tem tantas silabas quantos "
                 u"nucleos o espeak-ng pronuncia" % len(P))
    if declaradas:
        L.append(u"   %d declarada(s) como pedaco de exercicio: %s"
                 % (len(declaradas), u", ".join(x[0].upper() for x in declaradas)))
    if hiatos:
        L.append(u"   %d na familia do HIATO -io/-ia/-iao, em que o espeak junta "
                 u"e EU estou certo (medido): %s"
                 % (len(hiatos), u", ".join(u"%s (eu %d, ele %d)" % (w.upper(), m, n)
                                            for w, m, n, _ in hiatos)))
    return (1 if grossas else 0), L


def _silmap(pasta):
    ih = os.path.join(pasta, u"index.html")
    if not os.path.exists(ih):
        return None
    h = io.open(ih, encoding=u"utf-8").read()
    m = re.search(r"/\*SILMAP-INI\*/\s*var SILMAP = (\{.*?\});", h, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def confere(pasta):
    try:
        import pyphen
    except ImportError:
        return 2, [u"   sem o `pyphen` (pip install pyphen): NAO MEDI — e isto "
                   u"NAO e 'passou'. O dicionario pt_BR vem dentro dele."]
    if u"pt_BR" not in pyphen.LANGUAGES:
        return 2, [u"   o `pyphen` instalado nao traz o dicionario pt_BR: NAO MEDI"]

    S = _silmap(pasta)
    if S is None:
        return 2, [u"   sem `SILMAP` no index.html: este caderno nao fala silaba "
                   u"sozinha, ou nao e folha viva. NAO MEDI"]
    if not S:
        return 0, [u"   ok: este caderno nao fala nenhuma silaba sozinha "
                   u"(SILMAP vazio), entao nao ha o que conferir"]

    hif = pyphen.Pyphen(lang=u"pt_BR")
    ok_dec = {}
    fok = os.path.join(pasta, u"silabas-ok.json")
    if os.path.exists(fok):
        try:
            ok_dec = json.load(io.open(fok, encoding=u"utf-8"))
        except ValueError:
            pass

    L = [u"   ⚠️ MAO UNICA, e isto e parte da medida: o dicionario de "
         u"hifenizacao cala cortes de uma letra so (para `amor` ele nao oferece "
         u"corte). Ele so ACUSA corte a mais; nunca exige."]
    maus, declarados = [], []
    for pedaco in sorted(S):
        partes = hif.inserted(pedaco.lower()).split(u"-")
        if len(partes) <= 1:
            continue
        de = S[pedaco][0] if isinstance(S[pedaco], list) and S[pedaco] else u"?"
        if pedaco in ok_dec:
            declarados.append((pedaco, de, u"-".join(partes), ok_dec[pedaco]))
        else:
            maus.append((pedaco, de, u"-".join(partes)))

    if maus:
        L.append(u"   REPROVADO: %d pedaco(s) que o app fala como se fossem "
                 u"UMA silaba, e o dicionario pt_BR ainda corta por dentro:"
                 % len(maus))
        for pedaco, de, corte in maus:
            L.append(u"      • %-12s (recortado de %s) -> o dicionario divide %s"
                     % (pedaco, de, corte))
        L.append(u"   conserto: ou divida a palavra certo no `gerar_falas.py` "
                 u"(`_reg`), ou — se o pedaco for da FOLHA DE PAPEL, como o "
                 u"CAMA + LEAO de camaleao — declare em %s/silabas-ok.json "
                 u"com o motivo." % pasta)
        return 1, L

    L.append(u"   ✓ os %d pedaco(s) falados sozinhos conferem com o dicionario "
             u"pt_BR: nenhum esconde um corte por dentro" % len(S))
    cod2, L2 = conta_espeak(pasta, ok_dec)
    L.extend(L2)
    if cod2 == 1:
        return 1, L
    if declarados:
        # ⚠️ o que foi perdoado sai IMPRESSO em toda rodada, senao vira gaveta
        #    onde se esconde defeito.
        L.append(u"   %d pedaco(s) DECLARADO(S) como pedaco de exercicio, e nao "
                 u"como silaba:" % len(declarados))
        for pedaco, de, corte, por in declarados:
            L.append(u"      · %-12s (%s, dicionario: %s) — %s"
                     % (pedaco, de, corte, por))
    return 0, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/silaba_dicionario.py <pasta>")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, L = confere(pasta.rstrip(u"/"))
        cabec = {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]
        print(u"%s -> silaba x dicionario: %s" % (pasta.rstrip(u"/"), cabec))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
