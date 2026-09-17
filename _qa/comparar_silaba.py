# -*- coding: utf-8 -*-
u"""
============================================================
 A IDEIA DO MARCOS, MEDIDA ATE O FIM (17/set/2026)

 PALAVRAS DELE: *"existem atividades na internet aos montes de separacao de
 silabas com audio, nao? nao daria para aproveitar para conferencia?"* — e,
 quando eu disse que a comparacao nao separava: *"liveworksheets e varios
 outros sites tem atividades com som"*.

 A IDEIA E BOA E E DO TIPO CERTO: comparar AUDIO com AUDIO, em vez de pedir a
 um reconhecedor que LEIA o recorte (isso ja falhou tres vezes — wav2vec2,
 Whisper e allosaurus nao leem um pedaco de 250 ms).

 ⭐ MAS A PERGUNTA QUE DECIDE NAO E "existe audio na internet". E: **uma medida
    de distancia entre dois audios consegue dizer que este recorte esta certo?**
    Se nao conseguir, achar o audio nao adianta — e se conseguir, ai vale
    procurar. Por isso este arquivo mede a MEDIDA, com tres grupos:

      A. mesma silaba, palavras diferentes  -> tem de dar PERTO
      B. silabas diferentes                 -> tem de dar LONGE
      C. a mesma silaba SOLETRADA (o defeito)-> tem de dar LONGE

    Se A nao ficar claramente abaixo de B e de C, a medida nao serve.

 ⚠️ E ESTA E A CONDICAO MAIS FAVORAVEL POSSIVEL: mesma voz, mesmo sintetizador,
    mesma velocidade, mesmo corte. Um audio de outro site tem outra pessoa,
    outra sala, outro microfone — so pode ser PIOR. Medida que falha no facil
    nao passa no dificil.

 DUAS MEDIDAS, porque elas falham por motivos diferentes:
   `mfcc`  — MFCC + DTW, a ferramenta classica. Roda em qualquer lugar.
   `w2v`   — as camadas internas do wav2vec2 portugues. ⚠️ Isto NAO e transcrever:
             o modelo pode errar a letra e ainda assim dar uma representacao util.
             Sao coisas diferentes e eu nao posso concluir uma pela outra.

 Uso:  python3 _qa/comparar_silaba.py <pastas...> [--modo mfcc|w2v|ambos]
 Codigos: 0 mediu · 2 nao consegui medir (falta biblioteca ou modelo)
============================================================
"""
from __future__ import print_function

import io
import itertools
import json
import os
import re
import sys
import unicodedata


def _base(p):
    return re.sub(r"[^a-z0-9]", u"",
                  unicodedata.normalize(u"NFKD", p.lower())
                  .encode(u"ascii", u"ignore").decode())


def junta(pastas):
    u"""{SILABA: [(pasta, palavra, arquivo), ...]} de todos os cadernos."""
    porsil = {}
    for p in pastas:
        sj = os.path.join(p, u"silabas.json")
        if not os.path.exists(sj):
            continue
        S = json.load(io.open(sj, encoding=u"utf-8"))
        pref = S.get(u"prefixo", u"")
        for w, sil in (S.get(u"palavras") or {}).items():
            for i, s in enumerate(sil):
                if not s:
                    continue
                f = os.path.join(p, u"audio",
                                 u"%ssb_%s_%d.mp3" % (pref, _base(w), i))
                if os.path.exists(f):
                    porsil.setdefault(s.upper(), []).append((p, w, f))
    return porsil


# ══════════════════════════════════════════════════════════════════════
#  AS DUAS MEDIDAS
# ══════════════════════════════════════════════════════════════════════
def vetor_mfcc(f, librosa, np):
    y, _ = librosa.load(f, sr=16000, mono=True)
    y, _ = librosa.effects.trim(y, top_db=30)
    if len(y) < 400:
        return None
    m = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=13, hop_length=80, n_fft=400)
    return (m - m.mean(axis=1, keepdims=True)) / (m.std(axis=1, keepdims=True) + 1e-9)


_W2V = {}


def vetor_w2v(f, librosa, np):
    u"""As camadas internas do wav2vec2 pt. ⚠️ Nao e transcricao."""
    if u"m" not in _W2V:
        try:
            import torch
            from transformers import AutoModel, AutoFeatureExtractor
            nome = u"facebook/wav2vec2-large-xlsr-53-portuguese"
            _W2V[u"fe"] = AutoFeatureExtractor.from_pretrained(nome)
            _W2V[u"m"] = AutoModel.from_pretrained(nome).eval()
            _W2V[u"torch"] = torch
        except Exception as e:                                   # noqa: BLE001
            print(u"   wav2vec2 indisponivel: %s" % e)
            _W2V[u"m"] = None
    if _W2V.get(u"m") is None:
        return None
    torch = _W2V[u"torch"]
    y, _ = librosa.load(f, sr=16000, mono=True)
    y, _ = librosa.effects.trim(y, top_db=30)
    if len(y) < 400:
        return None
    ent = _W2V[u"fe"](y, sampling_rate=16000, return_tensors=u"pt")
    with torch.no_grad():
        h = _W2V[u"m"](**ent).last_hidden_state[0].numpy()
    h = h.T
    return (h - h.mean(axis=1, keepdims=True)) / (h.std(axis=1, keepdims=True) + 1e-9)


def dist(a, b, librosa):
    D, wp = librosa.sequence.dtw(X=a, Y=b, metric=u"euclidean")
    return float(D[-1, -1] / len(wp))


# ══════════════════════════════════════════════════════════════════════
def mede(pastas, modo):
    try:
        import numpy as np
        import librosa
    except ImportError as e:                                     # noqa: BLE001
        print(u"NAO MEDI: falta librosa/numpy (%s)" % e)
        return 2

    porsil = junta(pastas)
    if len(porsil) < 5:
        print(u"NAO MEDI: menos de 5 silabas com recorte")
        return 2

    fn = {u"mfcc": vetor_mfcc, u"w2v": vetor_w2v}[modo]
    cache = {}

    def v(f):
        if f not in cache:
            cache[f] = fn(f, librosa, np)
        return cache[f]

    # A. mesma silaba, palavras diferentes
    A = []
    for s, lista in sorted(porsil.items()):
        porpal = {}
        for p, w, f in lista:
            porpal.setdefault(w, f)
        for (w1, f1), (w2, f2) in itertools.combinations(list(porpal.items())[:3], 2):
            a, b = v(f1), v(f2)
            if a is not None and b is not None and f1 != f2:
                A.append((dist(a, b, librosa), s, w1, w2))

    # B. silabas diferentes
    B = []
    chaves = sorted(porsil)
    for s1, s2 in itertools.islice(itertools.combinations(chaves, 2), 0, 4000, 7):
        a, b = v(porsil[s1][0][2]), v(porsil[s2][0][2])
        if a is not None and b is not None:
            B.append((dist(a, b, librosa), s1, s2))

    # C. a mesma silaba SOLETRADA — o audio ruim guardado de proposito
    C = []
    ruim = u"_pesquisa/silabas-soletradas"
    if os.path.isdir(ruim):
        for f in sorted(os.listdir(ruim)):
            if not f.endswith(u".mp3"):
                continue
            # nome: <pasta>__<arquivo-bom>.mp3
            alvo = f[:-4].split(u"__")[-1]
            bons = [x for lista in porsil.values() for x in lista
                    if os.path.basename(x[2]) == alvo + u".mp3"]
            if not bons:
                continue
            a, b = v(bons[0][2]), v(os.path.join(ruim, f))
            if a is not None and b is not None:
                C.append((dist(a, b, librosa), alvo))

    def q(v_, p):
        v_ = sorted(v_)
        return v_[min(len(v_) - 1, int(len(v_) * p))] if v_ else float(u"nan")

    da = [x[0] for x in A]
    db = [x[0] for x in B]
    dc = [x[0] for x in C]
    print(u"\n== medida `%s` ==" % modo)
    print(u"A. mesma silaba, palavras diferentes  n=%3d  mediana %.2f  p90 %.2f  MAX %.2f"
          % (len(da), q(da, .5), q(da, .9), max(da) if da else float(u"nan")))
    print(u"B. silabas diferentes                 n=%3d  MIN %.2f  p10 %.2f  mediana %.2f"
          % (len(db), min(db) if db else float(u"nan"), q(db, .1), q(db, .5)))
    if dc:
        print(u"C. a mesma silaba SOLETRADA           n=%3d  MIN %.2f  mediana %.2f"
              % (len(dc), min(dc), q(dc, .5)))
    else:
        print(u"C. (sem audio soletrado guardado em %s)" % ruim)

    # ⭐ O VEREDITO E UM SO: existe um corte que separe A de (B e C)?
    #   Se o pior caso de A for maior que o melhor de B ou de C, nao existe.
    piorA = max(da) if da else None
    melhorB = min(db) if db else None
    melhorC = min(dc) if dc else None
    print(u"\n   VEREDITO:")
    if piorA is None or melhorB is None:
        print(u"   nao deu para julgar (faltou um dos grupos)")
        return 2
    if piorA < melhorB and (melhorC is None or piorA < melhorC):
        print(u"   ✅ SEPARA. O pior 'mesma silaba' (%.2f) fica abaixo do melhor\n"
              u"      'silaba diferente' (%.2f)%s. Cabe um limiar entre eles — e\n"
              u"      ai VALE procurar audio de referencia na internet."
              % (piorA, melhorB,
                 u" e do melhor soletrado (%.2f)" % melhorC if melhorC else u""))
        return 0
    print(u"   ❌ NAO SEPARA. O pior 'mesma silaba' (%.2f) ja passa do melhor\n"
          u"      'silaba diferente' (%.2f)%s: as faixas se sobrepoem e nao existe\n"
          u"      limiar. Achar audio na internet NAO resolve, porque o gargalo\n"
          u"      nao e a fonte — e a comparacao."
          % (piorA, melhorB,
             u" / do melhor soletrado (%.2f)" % melhorC if melhorC else u""))
    if A:
        A.sort()
        print(u"      o pior caso de A: %s de %s x %s = %.2f"
              % (A[-1][1], A[-1][2], A[-1][3], A[-1][0]))
    return 0


def main():
    modo = u"ambos"
    args = []
    k = 1
    while k < len(sys.argv):
        if sys.argv[k] == u"--modo" and k + 1 < len(sys.argv):
            modo = sys.argv[k + 1]
            k += 2
            continue
        args.append(sys.argv[k].rstrip(u"/"))
        k += 1
    if not args:
        print(u"uso: python3 _qa/comparar_silaba.py <pastas...> [--modo mfcc|w2v|ambos]")
        return 2
    pior = 0
    for m in ([u"mfcc", u"w2v"] if modo == u"ambos" else [modo]):
        c = mede(args, m)
        pior = max(pior, c)
    return pior


if __name__ == u"__main__":
    sys.exit(main())
