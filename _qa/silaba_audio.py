# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1x — O RECORTE DE SILABA TEM SOM, E SO UMA VOGAL

 ⭐ ORDEM DO MARCOS (17/set/2026): *"use tudo para que o falar das silabas fique
    perfeito, sem erros, pq isso e muito importante na alfabetizacao"*.

 ⚠️ POR QUE ESTE PORTAO NAO USA RECONHECEDOR DE FALA. Foi medido, e tres
    falharam: o wav2vec2 pt, o Whisper e o allosaurus. Nenhum le um recorte de
    250 ms com confianca — o `SA` de SAPO saiu como "i a ŋ". Um portao apoiado
    neles reprovaria por causa do proprio erro.

 ENTAO ELE MEDE O QUE E FISICO, e a invariante vem da LINGUA, nao de mim:
 **toda silaba do portugues tem exatamente UMA vogal** — e e isso que o caderno
 do degrau 1 ensina a crianca. Do audio da-se para contar.

 AS TRES MEDIDAS:

  1. TEM SOM? O pico de energia do recorte contra a MEDIANA dos recortes do
     mesmo caderno (mesma voz, comparacao justa). Abaixo de um quarto, reprova.
     ⭐ Foi esta que achou o defeito: 35 recortes quase mudos em sete cadernos,
        e quase todos a SILABA FINAL da palavra — o PO de SAPO com pico 0,022
        contra 0,180 de mediana, o TO de GATO, o CO de MACACO, o VO de BRAVO.
        A razao e da lingua: a final atona do portugues do Brasil e dita quase
        sem voz. Dentro da palavra ninguem nota; tocada SOZINHA a crianca nao
        ouve. O conserto entrou no `_padrao/silabas_voz.py` (`loudnorm`).

  2. COMECA COM SOM? Silencio na frente e a boca FECHADA da oclusiva (/p/, /t/,
     /k/). Um pouco e natural; muito e corte torto. Medido: mediana 0 ms, 90%
     ate 45 ms. O pior achado foi o `GA` de GATO no `_sil1`, com 180 ms de
     silencio absoluto num arquivo de 260 ms — a crianca toca e nao acontece
     nada por quase dois decimos de segundo.

  3. UMA VOGAL SO? Dois nucleos = o corte engoliu a silaba vizinha; zero =
     perdeu a vogal. Medido em 882 recortes: 872 com exatamente uma. Os dez
     restantes sao os PEDACOS de exercicio ja declarados em `silabas-ok.json`
     (CENOU+RA, CA+MA...), que tem mais de uma silaba de proposito.
     ⚠️ A consoante SONORA (l, r, m, n) tambem faz pico, mas um pico FRACO —
        foi o que separou o `LU` de LUA (o /l/) do `CENOU` de CENOURA (duas
        vogais de verdade). So conta como nucleo o pico que chega a 6 dB do
        mais forte do recorte.

 Uso:  python3 _qa/silaba_audio.py <pasta> [--medir]
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys
import unicodedata

# ⚠️ Os numeros abaixo NAO foram escolhidos: saem da medida de 17/set/2026 em
#    882 recortes de oito cadernos. Trocou a voz ou o RATE, remede.
FRACO = 0.25        # do pico mediano do caderno
SILENCIO_MS = 120   # na frente; o 90º percentil medido foi 45 ms
MIN_NUCLEO_MS = 50  # abaixo disso e transiente, nao vogal
MARGEM_DB = 6.0     # o pico secundario tem de chegar a isto do principal


def _base(p):
    return re.sub(r"[^a-z0-9]", u"",
                  unicodedata.normalize(u"NFKD", p.lower())
                  .encode(u"ascii", u"ignore").decode())


def _analisa(f, np, librosa):
    y, _ = librosa.load(f, sr=16000, mono=True)
    if len(y) < 320:
        return None
    S = np.abs(librosa.stft(y, n_fft=512, hop_length=80))
    fr = librosa.fft_frequencies(sr=16000, n_fft=512)
    voz = S[(fr >= 250) & (fr <= 3000)].sum(axis=0)
    tudo = S.sum(axis=0)
    if voz.max() <= 0 or tudo.max() <= 0:
        return None
    db = 20 * np.log10(voz / voz.max() + 1e-9)
    if len(db) >= 5:
        db = np.convolve(db, np.ones(5) / 5.0, mode=u"same")
    dbt = 20 * np.log10(tudo / tudo.max() + 1e-9)
    viva = np.where(dbt > -30)[0]
    frente = (viva[0] * 5.0) if len(viva) else 0.0
    n = 320
    r = [float(np.sqrt((y[k:k + n] ** 2).mean()))
         for k in range(0, max(1, len(y) - n), n)]
    return {u"pico": max(r) if r else 0.0, u"frente": frente,
            u"dur": len(db) * 5.0, u"db": db}


def _nucleos(db, np):
    acima = db > -12.0
    bl, i = [], 0
    while i < len(acima):
        if acima[i]:
            j = i
            while j < len(acima) and acima[j]:
                j += 1
            bl.append((i, j))
            i = j
        else:
            i += 1
    bl = [(a, b) for a, b in bl if (b - a) * 5.0 >= MIN_NUCLEO_MS]
    if not bl:
        return 0
    f = [bl[0]]
    for a, b in bl[1:]:
        pa, pb = f[-1]
        entre = db[pb:a]
        if len(entre) == 0 or (min(db[pa:pb].max(), db[a:b].max()) - entre.min()) < 6.0:
            f[-1] = (pa, b)
        else:
            f.append((a, b))
    topo = max(db[a:b].max() for a, b in f)
    return len([1 for a, b in f if db[a:b].max() >= topo - MARGEM_DB])


def confere(pasta, medir=False):
    try:
        import numpy as np
        import librosa
    except ImportError as e:                                     # noqa: BLE001
        return 2, [u"   sem `librosa`/`numpy` (%s): NAO MEDI — e isto nao e "
                   u"'passou'. pip install librosa soundfile" % e]

    sj = os.path.join(pasta, u"silabas.json")
    if not os.path.exists(sj):
        return 2, [u"   sem `silabas.json`: este caderno nao fala silaba. NAO MEDI"]
    S = json.load(io.open(sj, encoding=u"utf-8"))
    pref = S.get(u"prefixo", u"")
    ok_dec = {}
    fok = os.path.join(pasta, u"silabas-ok.json")
    if os.path.exists(fok):
        try:
            ok_dec = json.load(io.open(fok, encoding=u"utf-8"))
        except ValueError:
            pass

    itens = []
    for w, sil in sorted((S.get(u"palavras") or {}).items()):
        for i, s in enumerate(sil):
            f = os.path.join(pasta, u"audio",
                             u"%ssb_%s_%d.mp3" % (pref, _base(w), i))
            if os.path.exists(f):
                itens.append((w, i, len(sil), s, f))
    if not itens:
        return 2, [u"   nenhum recorte na pasta: NAO MEDI. Eles nascem no "
                   u"`entregar.yml`, ao publicar."]

    dados = []
    for w, i, nn, s, f in itens:
        a = _analisa(f, np, librosa)
        if a:
            a.update({u"w": w, u"i": i, u"n": nn, u"s": s, u"f": f})
            dados.append(a)
    if not dados:
        return 2, [u"   nao consegui ler nenhum recorte: NAO MEDI"]

    picos = sorted(x[u"pico"] for x in dados)
    med = picos[len(picos) // 2]
    mudos = [x for x in dados if x[u"pico"] < med * FRACO]
    tardios = [x for x in dados if x[u"frente"] >= SILENCIO_MS]
    duplos = []
    for x in dados:
        if x[u"w"].upper() in ok_dec or x[u"w"] in ok_dec:
            continue
        k = _nucleos(x[u"db"], np)
        if k != 1:
            duplos.append((x, k))

    L = [u"   %d recorte(s) medidos · pico mediano %.3f" % (len(dados), med)]
    ruim = 0
    if mudos:
        ruim = 1
        L.append(u"   REPROVADO 1: %d recorte(s) QUASE MUDOS (a crianca toca e "
                 u"nao ouve) — abaixo de %d%% do pico mediano:"
                 % (len(mudos), int(FRACO * 100)))
        for x in sorted(mudos, key=lambda y: y[u"pico"])[:10]:
            L.append(u"      • %-11s silaba %d de %d: %-6s pico %.3f"
                     % (x[u"w"].upper(), x[u"i"] + 1, x[u"n"], x[u"s"], x[u"pico"]))
        L.append(u"   conserto: o `loudnorm` do `_padrao/silabas_voz.py` iguala a "
                 u"forca de cada pedaco. Se ja esta la, regrave (apague o "
                 u"`audio/_carimbo.json` da palavra).")
    else:
        L.append(u"   ✓ todos os recortes tem som (nenhum abaixo de %d%% do "
                 u"pico mediano)" % int(FRACO * 100))
    if tardios:
        ruim = 1
        L.append(u"   REPROVADO 2: %d recorte(s) comecam com %d ms ou mais de "
                 u"SILENCIO:" % (len(tardios), SILENCIO_MS))
        for x in sorted(tardios, key=lambda y: -y[u"frente"])[:10]:
            L.append(u"      • %-11s silaba %d de %d: %-6s %.0f ms mudos de %.0f"
                     % (x[u"w"].upper(), x[u"i"] + 1, x[u"n"], x[u"s"],
                        x[u"frente"], x[u"dur"]))
    else:
        L.append(u"   ✓ nenhum recorte comeca com silencio longo")
    if duplos:
        ruim = 1
        L.append(u"   REPROVADO 3: %d recorte(s) sem UMA vogal exata (silaba do "
                 u"portugues tem uma so):" % len(duplos))
        for x, k in duplos[:10]:
            L.append(u"      • %-11s silaba %d de %d: %-6s %d nucleo(s)"
                     % (x[u"w"].upper(), x[u"i"] + 1, x[u"n"], x[u"s"], k))
        L.append(u"   conserto: dois nucleos = o corte engoliu a vizinha; zero = "
                 u"perdeu a vogal. Se for PEDACO de exercicio, declare em "
                 u"%s/silabas-ok.json." % pasta)
    else:
        L.append(u"   ✓ cada recorte tem exatamente uma vogal")
    if medir:
        L.append(u"   MODO --medir: nao reprovo.")
        return 0, L
    return ruim, L


def main():
    args = [a for a in sys.argv[1:] if a != u"--medir"]
    medir = u"--medir" in sys.argv
    if not args:
        print(u"uso: python3 _qa/silaba_audio.py <pasta> [--medir]")
        return 2
    pior = 0
    for pasta in args:
        cod, L = confere(pasta.rstrip(u"/"), medir)
        print(u"%s -> som da silaba: %s"
              % (pasta.rstrip(u"/"),
                 {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
