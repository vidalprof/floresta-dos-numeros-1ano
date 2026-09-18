# -*- coding: utf-8 -*-
u"""
============================================================
 A SILABA EM FORMA DE CITACAO — como pedir a voz SEM que ela soletre?

 ⭐ DECISAO DO MARCOS (18/set/2026): a silaba tocada sozinha deve soar "como a
    professora separa na lousa" — mais longa, vogal cheia ("SA — PO"), e nao
    como sai reduzida dentro da palavra ([pʊ], 0,08 s).

 O QUE JA SE SABE (medido nas gravacoes de 17/set, 5 palavras x 5 jeitos):
   · pedir a palavra APARTADA ("sa po") da a forma de citacao: PO 0,24-0,30 s,
     F1 510-550 Hz (vogal [o] plena), contra 0,08 s / F1 ~400 na corrida;
   · mas a voz SOLETRA pecas que nao sao palavra do portugues: ES ("e-esse"),
     NE ("ene"), GA ("ge-a") — e nao soletra SA, PO, TO, MA, CA, CO, LA;
   · a distancia de audio (MFCC+DTW) NAO separa soletrado de citacao (2a vez
     que falha: GA soletrado a 2,96, CA de citacao a 4,35). Descartada.
   · a DURACAO separa com zona cinzenta (soletrado >= 0,53 s; citacao <= 0,46).

 O QUE ESTE EXPERIMENTO MEDE (so no GitHub Actions: precisa de TTS e de modelo):
   para as 206 palavras dos oito cadernos, tres jeitos de pedir apartado
   (espaco / hifen / virgula), segmenta por silencio e, em cada peca:
     · duracao, numero de nucleos de vogal, F1 da vogal;
     · o que um reconhecedor (wav2vec2 pt) LE na peca — soletrado le como nome
       de letra ("ge a", "ene"), citacao le como a silaba. Em recorte de 250 ms
       de fala corrida ele falhou (17/set); a peca apartada e outra coisa: mais
       longa e articulada. Se ele ler bem aqui, vira o detector.
   e, de controle, o que o reconhecedor le no recorte CORRIDO da mesma silaba
   (ja no caderno) — para o teste ter um "sabidamente dificil".

 SAIDA: _pesquisa/citacao-prova.json (tudo) e _pesquisa/citacao-prova.txt
 (resumo: por jeito, quantas palavras deram N pecas; quantas pecas o
 reconhecedor leu como a silaba; quantas soletradas; onde a duracao e o
 reconhecedor discordam).
============================================================
"""
from __future__ import print_function

import asyncio
import importlib.util
import io
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(RAIZ, u"_pesquisa", u"silabas-inventario.txt")
DEST = os.path.join(RAIZ, u"_pesquisa", u"citacao-prova")
VOZ = u"pt-BR-AntonioNeural"
RATE = u"-25%"
CADERNOS = u"_alfa1 _ini1 _mont1 _sil1 _roda1 _sil2 _troca2 _nasal2".split()
JEITOS = [(u"espaco", lambda s: u" ".join(s).lower()),
          (u"hifen", lambda s: u"-".join(s).lower()),
          (u"virgula", lambda s: u", ".join(s).lower() + u".")]
LETRAS = {u"a": u"a", u"b": u"be", u"c": u"ce", u"d": u"de", u"e": u"e", u"f": u"efe", u"g": u"ge",
          u"h": u"aga", u"i": u"i", u"j": u"jota", u"k": u"ca", u"l": u"ele", u"m": u"eme", u"n": u"ene",
          u"o": u"o", u"p": u"pe", u"q": u"que", u"r": u"erre", u"s": u"esse", u"t": u"te", u"u": u"u",
          u"v": u"ve", u"w": u"dabliu", u"x": u"xis", u"y": u"ipsilon", u"z": u"ze"}


def _sem_acento(t):
    return u"".join(c for c in unicodedata.normalize(u"NFD", t) if unicodedata.category(c) != u"Mn")


def _norm(t):
    return re.sub(r"[^a-z]", u"", _sem_acento((t or u"").lower()))


def segmentos(y, sr):
    import numpy as np
    import librosa
    fr = librosa.feature.rms(y=y, frame_length=400, hop_length=80)[0]
    db = 20 * np.log10(fr / (fr.max() + 1e-12) + 1e-9)
    on = db > -30
    seg, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            if (j - i) * 80.0 / sr >= 0.06:
                seg.append((i * 80.0 / sr, j * 80.0 / sr))
            i = j
        else:
            i += 1
    out = []
    for a, b in seg:
        if out and a - out[-1][1] < 0.06:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return out


def f1_vogal(y, sr):
    u"""F1 por LPC no terco central do trecho (Hz), ou None."""
    import numpy as np
    from scipy.signal import lfilter
    from scipy.linalg import solve_toeplitz
    n = len(y)
    w = y[n // 3: 2 * n // 3]
    if len(w) < 200:
        return None
    w = w * np.hamming(len(w))
    w = lfilter([1, -0.97], [1], w)
    r = np.correlate(w, w, u"full")[len(w) - 1:]
    p = 12
    try:
        a = solve_toeplitz(r[:p], r[1:p + 1])
    except Exception:                                            # noqa: BLE001
        return None
    rts = np.roots(np.concatenate(([1], -a)))
    rts = rts[np.imag(rts) > 0.01]
    fr = np.sort(np.angle(rts) * sr / (2 * np.pi))
    fr = fr[fr > 150]
    return float(fr[0]) if len(fr) else None


class Ouvido(object):
    def __init__(self):
        self.ok = False
        try:
            import torch
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
            nome = u"jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
            self.proc = Wav2Vec2Processor.from_pretrained(nome)
            self.mod = Wav2Vec2ForCTC.from_pretrained(nome).eval()
            self.torch = torch
            self.ok = True
        except Exception as e:                                   # noqa: BLE001
            print(u"   reconhecedor indisponivel: %s" % e)

    def le(self, y, sr):
        if not self.ok:
            return None
        import librosa
        if sr != 16000:
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
        ent = self.proc(y, sampling_rate=16000, return_tensors=u"pt", padding=True)
        with self.torch.no_grad():
            lg = self.mod(ent.input_values).logits
        ids = self.torch.argmax(lg, dim=-1)
        return self.proc.batch_decode(ids)[0].lower().strip()


def classifica(lido, silaba):
    u"""'silaba' se leu a silaba; 'soletrado' se leu nomes de letra; 'outro'."""
    if lido is None:
        return u"nao-ouvi"
    alvo = _norm(silaba)
    l = _norm(lido)
    if not l:
        return u"vazio"
    if l == alvo or l.startswith(alvo) or alvo.startswith(l) and len(l) >= max(1, len(alvo) - 1):
        return u"silaba"
    nomes = u"".join(LETRAS.get(c, c) for c in alvo)
    if l == nomes or nomes in l or any(LETRAS[c] in l for c in alvo if len(LETRAS[c]) >= 2 and LETRAS[c] not in alvo):
        return u"soletrado"
    return u"outro"


async def main():
    import edge_tts
    import numpy as np
    import librosa
    sp = importlib.util.spec_from_file_location(u"sv", os.path.join(RAIZ, u"_padrao", u"silabas_voz.py"))
    sv = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(sv)
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    inv = []
    for lin in io.open(INV, encoding=u"utf-8"):
        lin = lin.strip()
        if lin:
            w, s = lin.split(u" ", 1)
            inv.append((w, s.split(u"-")))
    ouvido = Ouvido()
    sem = asyncio.Semaphore(6)

    async def grava(texto, saida):
        async with sem:
            for t in range(3):
                try:
                    c = edge_tts.Communicate(texto, VOZ, rate=RATE)
                    await c.save(saida)
                    return os.path.exists(saida) and os.path.getsize(saida) > 800
                except Exception:                                # noqa: BLE001
                    await asyncio.sleep(1 + t)
        return False

    tarefas = []
    for w, sil in inv:
        for nome, monta in JEITOS:
            saida = os.path.join(DEST, u"%s__%s.mp3" % (w, nome))
            if not os.path.exists(saida):
                tarefas.append(grava(monta(sil), saida))
    print(u"gravando %d pedidos apartados..." % len(tarefas))
    await asyncio.gather(*tarefas)

    # recorte CORRIDO de controle: o primeiro caderno que tiver a palavra
    def corrida(w, i):
        for p in CADERNOS:
            S = json.load(io.open(os.path.join(RAIZ, p, u"silabas.json"), encoding=u"utf-8"))
            if w in S.get(u"palavras", {}) or w in (k.lower() for k in S.get(u"palavras", {})):
                pref = S.get(u"prefixo", u"")
                f = os.path.join(RAIZ, p, u"audio", u"%ssb_%s_%d.mp3" % (pref, re.sub(r"[^a-z0-9]", u"", _sem_acento(w)), i))
                if os.path.exists(f):
                    return f
        return None

    R = []
    for w, sil in inv:
        for nome, _ in JEITOS:
            f = os.path.join(DEST, u"%s__%s.mp3" % (w, nome))
            if not os.path.exists(f):
                R.append({u"palavra": w, u"jeito": nome, u"erro": u"sem audio"})
                continue
            y, sr = librosa.load(f, sr=16000, mono=True)
            seg = segmentos(y, sr)
            item = {u"palavra": w, u"silabas": sil, u"jeito": nome, u"pecas": len(seg), u"esperado": len(sil), u"detalhe": []}
            if len(seg) == len(sil):
                for i, (a, b) in enumerate(seg):
                    tr = y[int(a * sr):int(b * sr)]
                    lido = ouvido.le(tr, sr)
                    d = {u"i": i, u"silaba": sil[i], u"dur": round(b - a, 3),
                         u"f1": f1_vogal(tr, sr), u"lido": lido, u"classe": classifica(lido, sil[i])}
                    fc = corrida(w, i)
                    if fc:
                        yc, src = librosa.load(fc, sr=16000, mono=True)
                        d[u"corrida_dur"] = round(len(yc) / 16000.0, 3)
                        d[u"corrida_f1"] = f1_vogal(yc, 16000)
                        d[u"corrida_lido"] = ouvido.le(yc, 16000)
                        d[u"corrida_classe"] = classifica(d[u"corrida_lido"], sil[i])
                    item[u"detalhe"].append(d)
            R.append(item)
        print(u"   %s ok" % w)

    io.open(os.path.join(RAIZ, u"_pesquisa", u"citacao-prova.json"), u"w", encoding=u"utf-8").write(
        json.dumps({u"voz": VOZ, u"rate": RATE, u"itens": R}, ensure_ascii=False, indent=1))

    # resumo
    L = [u"PROVA DA FORMA DE CITACAO — %d palavras, voz %s, rate %s" % (len(inv), VOZ, RATE), u""]
    for nome, _ in JEITOS:
        its = [x for x in R if x.get(u"jeito") == nome and u"pecas" in x]
        fech = [x for x in its if x[u"pecas"] == x[u"esperado"]]
        pecas = [d for x in fech for d in x[u"detalhe"]]
        cl = {}
        for d in pecas:
            cl[d[u"classe"]] = cl.get(d[u"classe"], 0) + 1
        longas = [d for d in pecas if d[u"dur"] > 0.5]
        sol_curtas = [d for d in pecas if d[u"classe"] == u"soletrado" and d[u"dur"] <= 0.5]
        cit_longas = [d for d in pecas if d[u"classe"] == u"silaba" and d[u"dur"] > 0.5]
        L.append(u"== %s: %d/%d palavras deram o numero certo de pecas; %d pecas medidas"
                 % (nome, len(fech), len(its), len(pecas)))
        L.append(u"   reconhecedor leu: %s" % u", ".join(u"%s %d" % kv for kv in sorted(cl.items())))
        L.append(u"   pecas > 0,5 s: %d · soletradas CURTAS (duracao nao pegaria): %d · citacao LONGA (duracao acusaria inocente): %d"
                 % (len(longas), len(sol_curtas), len(cit_longas)))
        for d in sol_curtas[:6]:
            L.append(u"      soletrada curta: %s %.2fs leu '%s'" % (d[u"silaba"], d[u"dur"], d[u"lido"]))
        for d in cit_longas[:6]:
            L.append(u"      citacao longa:   %s %.2fs leu '%s'" % (d[u"silaba"], d[u"dur"], d[u"lido"]))
        f1s = [d[u"f1"] for d in pecas if d.get(u"f1") and d[u"classe"] == u"silaba" and d[u"i"] == len(d) - 1]
    # controle: o reconhecedor no recorte CORRIDO
    cc = {}
    for x in R:
        for d in x.get(u"detalhe", []):
            if u"corrida_classe" in d:
                cc[d[u"corrida_classe"]] = cc.get(d[u"corrida_classe"], 0) + 1
    L.append(u"")
    L.append(u"CONTROLE — o reconhecedor no recorte CORRIDO (o que esta no ar): %s"
             % u", ".join(u"%s %d" % kv for kv in sorted(cc.items())))
    io.open(os.path.join(RAIZ, u"_pesquisa", u"citacao-prova.txt"), u"w", encoding=u"utf-8").write(u"\n".join(L) + u"\n")
    print(u"\n".join(L))


if __name__ == u"__main__":
    sys.exit(asyncio.run(main()) or 0)
