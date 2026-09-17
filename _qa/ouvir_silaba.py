# -*- coding: utf-8 -*-
u"""
============================================================
 O OUVIDO DA SILABA — o recorte e ESCUTADO, letra por letra

 ⭐ PEDIDO DO MARCOS (17/set/2026): *"o banco de audio e para comparar se a fala
    esta certa, e isso que quero"* · ***"precisamos muito para as silabas"*** ·
    *"deve dar para comparar em atividades online ou banco de audios"* — e,
    antes disso, a lembranca que eu precisava: ***"vc pode usar o GitHub
    lembra?"***. O chat nao tem internet; o Actions tem. Isto roda la.

 POR QUE UM ARQUIVO SO PARA A SILABA, separado do `_qa/ouvir.py`:
 o reconhecedor de FRASE (Whisper) e otimo em frase inteira e ruim num pedaco
 de 300 ms — ele quer contexto, e um recorte de silaba nao tem nenhum. Usar o
 mesmo aparelho para as duas coisas daria um portao que acusa o proprio
 aparelho. Aqui o aparelho e outro: um reconhecedor **por caractere** (CTC,
 wav2vec2 treinado em portugues), que decide quadro a quadro e nao precisa de
 contexto. Para um recorte de "sa" ele devolve `sa`.

 ⭐⭐ E E EXATAMENTE O DEFEITO QUE O MARCOS OUVIU NA SALA: *"nas silabas nao esta
    bom, ao inves de falar Sa ele fala s a em sapo"*. A voz nao le SOM, le
    PALAVRA: entregue "SA" a ela e ela soletra "esse-a". Hoje isso e evitado
    gravando a palavra inteira e cortando a silaba de dentro — mas NADA CONFERIA
    O CORTE. Se ele sair torto (pegar "as" em vez de "sa"), ou se a queda para o
    corte por silencio entrar, a crianca ouve o pedaco errado e nenhum portao
    ve. Este ve:

        escrito:  SA        ouvido: sa      -> erro 0.00   ok
        escrito:  SA        ouvido: as      -> erro 1.00   REPROVA (corte torto)
        escrito:  SA        ouvido: esse a  -> erro 0.86   REPROVA (soletrou)

 ⚠️ OS LIMITES, ESCRITOS ANTES DO RESULTADO:
   1. O modelo erra em audio curtissimo — sobretudo em silaba de UMA letra (o A
      de ASA), onde nao ha consoante para ancorar. Silaba de uma letra e OUVIDA
      e RELATADA, mas nao reprova sozinha. Mesma regra que o `_qa/silabas.py`
      ja usa para a duracao, e pela mesma razao.
   2. A comparacao e por texto ACHATADO (minuscula, sem acento). O modelo nao
      poe acento; cobrar acento seria acusar o aparelho, nao o mp3.
   3. O CORTE que reprova NAO foi inventado. Sai da MEDIDA da primeira rodada
      (`--medir`) e fica escrito no relatorio, com modelo e data. Trocou o
      modelo, remede.

 ⭐ A SEGUNDA MEDIDA, QUE NAO DEPENDE DE MODELO NENHUM: **a mesma silaba,
    recortada de DUAS palavras diferentes, tem de soar parecida.** O `SA` de
    ASA e o `SA` de SAPO sao o mesmo som; se os dois recortes nao se parecem,
    um dos dois esta torto. Isso se mede com MFCC + DTW, e nao precisa de banco
    externo nenhum — o banco de audio somos nos mesmos, e e por isso que ele
    nao pode mentir sobre si.

 Uso:
   python3 _qa/ouvir_silaba.py <pasta> [...] [--modelo <hf>] [--medir]
                               [--limite 0.5] [--so N]
 Saida: `_qa/_ouvido/<pasta>-silabas.json` e `.md`
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

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, u"_ouvido")

# ⚠️ CTC por caractere, treinado em portugues (Common Voice + outros). E um
#    BANCO DE AUDIO de verdade, publico, virado em modelo — que e a forma util
#    de "comparar com banco de audio": nao se compara arquivo com arquivo, que
#    seria fragil a voz e a velocidade; compara-se o que o som DIZ.
MODELO_PADRAO = u"jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"


def achata(s):
    s = unicodedata.normalize(u"NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != u"Mn")
    s = s.lower().replace(u"ç", u"c")
    return re.sub(r"[^a-z]+", u"", s)


def distancia(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atual = [i]
        for j, cb in enumerate(b, 1):
            atual.append(min(ant[j] + 1, atual[j - 1] + 1,
                             ant[j - 1] + (ca != cb)))
        ant = atual
    return ant[-1]


def erro(escrito, ouvido):
    e, o = achata(escrito), achata(ouvido)
    if not e:
        return 0.0
    return min(1.0, distancia(e, o) / float(len(e)))


# ---------------------------------------------------------------------------
def carrega(nome):
    u"""Devolve (ouve(caminho)->texto, le_audio(caminho)->(sinal, taxa)) ou
    (None, motivo)."""
    try:
        import numpy as np                                        # noqa: F401
        import torch
        import librosa
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
    except ImportError as e:                                      # noqa: BLE001
        return None, (u"faltam bibliotecas (%s). No runner: "
                      u"pip install torch transformers librosa soundfile" % e)
    try:
        proc = Wav2Vec2Processor.from_pretrained(nome)
        mod = Wav2Vec2ForCTC.from_pretrained(nome)
        mod.eval()
    except Exception as e:                                        # noqa: BLE001
        return None, u"nao consegui carregar `%s`: %s" % (nome, e)

    def le(caminho):
        sinal, taxa = librosa.load(caminho, sr=16000, mono=True)
        return sinal, taxa

    def ouve(caminho):
        sinal, _ = le(caminho)
        if len(sinal) < 400:            # < 25 ms: nao ha o que ouvir
            return u""
        ent = proc(sinal, sampling_rate=16000, return_tensors=u"pt", padding=True)
        with torch.no_grad():
            log = mod(ent.input_values).logits
        ids = torch.argmax(log, dim=-1)
        return proc.batch_decode(ids)[0].strip()

    ouve.le = le
    return ouve, None


# ---------------------------------------------------------------------------
def recortes(pasta):
    u"""[(arquivo, silaba, palavra, posicao)] — do `silabas.json`, que e a
    mesma fonte que o `entregar.yml` usa para cortar."""
    sj = os.path.join(pasta, u"silabas.json")
    audio = os.path.join(pasta, u"audio")
    if not os.path.exists(sj):
        return None
    try:
        S = json.load(io.open(sj, encoding=u"utf-8"))
    except ValueError:
        return None
    pref = S.get(u"prefixo", u"")
    saida = []
    for palavra, sil in sorted((S.get(u"palavras") or {}).items()):
        base = re.sub(r"[^a-z0-9]", u"",
                      unicodedata.normalize(u"NFKD", palavra.lower())
                      .encode(u"ascii", u"ignore").decode())
        for i, s in enumerate(sil):
            mp3 = os.path.join(audio, u"%ssb_%s_%d.mp3" % (pref, base, i))
            if os.path.exists(mp3):
                saida.append((mp3, s, palavra, i))
    return saida


def irmas(linhas):
    u"""A MESMA silaba vinda de palavras diferentes — os pares que a segunda
    medida compara. Devolve [(silaba, [linha, linha, ...])]."""
    por = {}
    for x in linhas:
        por.setdefault(achata(x[u"silaba"]), []).append(x)
    return [(k, v) for k, v in sorted(por.items()) if len(v) > 1]


def parecidas(le, a, b):
    u"""distancia DTW entre dois recortes, em MFCC. 0 = iguais.
    ⚠️ PALPITE DECLARADO no uso, nao na conta: a conta (MFCC + DTW) e padrao;
    o que e juizo meu e o CORTE a partir do qual duas silabas 'nao se parecem'
    — e por isso ele sai da MEDIDA, nunca de um numero que eu escolhi."""
    import librosa
    import numpy as np
    sa, _ = le(a)
    sb, _ = le(b)
    if len(sa) < 400 or len(sb) < 400:
        return None
    ma = librosa.feature.mfcc(y=sa, sr=16000, n_mfcc=13)
    mb = librosa.feature.mfcc(y=sb, sr=16000, n_mfcc=13)
    ma = (ma - ma.mean()) / (ma.std() + 1e-9)
    mb = (mb - mb.mean()) / (mb.std() + 1e-9)
    D, wp = librosa.sequence.dtw(X=ma, Y=mb, metric=u"cosine")
    return float(D[-1, -1] / max(1, len(wp)))


def confere(pasta, ouve, limite, so, medir):
    itens = recortes(pasta)
    if itens is None:
        return 2, [u"   sem `silabas.json`: este caderno nao fala silaba. NAO MEDI"], None
    if not itens:
        return 2, [u"   o `silabas.json` existe mas nenhum recorte esta na pasta: "
                   u"NAO MEDI. Os recortes nascem no `entregar.yml`."], None
    if so:
        itens = itens[:so]

    linhas, ruins, curtas = [], [], []
    for n, (mp3, s, palavra, i) in enumerate(itens, 1):
        try:
            ouvido = ouve(mp3)
        except Exception as e:                                    # noqa: BLE001
            ouvido = u"<<ERRO: %s>>" % e
        er = erro(s, ouvido)
        x = {u"arquivo": os.path.basename(mp3), u"silaba": s, u"palavra": palavra,
             u"pos": i, u"ouvido": ouvido, u"erro": round(er, 3),
             u"bytes": os.path.getsize(mp3)}
        linhas.append(x)
        if len(achata(s)) < 2:
            curtas.append(x)                 # uma letra: relata, nao reprova
        elif er > limite:
            ruins.append(x)
        if n % 40 == 0:
            print(u"      ... %d de %d" % (n, len(itens)))

    L = [u"   ouviu %d recorte(s) de silaba" % len(linhas)]
    medidos = [x[u"erro"] for x in linhas if len(achata(x[u"silaba"])) >= 2]
    if medidos:
        o = sorted(medidos)
        L.append(u"   erro: mediana %.3f · 90%% abaixo de %.3f · pior %.3f · "
                 u"%d acima do corte %.2f"
                 % (o[len(o) // 2], o[int(len(o) * 0.9)], o[-1], len(ruins), limite))
    if curtas:
        L.append(u"   %d silaba(s) de UMA letra ouvidas e NAO cobradas (nao ha "
                 u"consoante para ancorar; mesma regra da duracao): %s"
                 % (len(curtas), u", ".join(sorted(set(x[u"silaba"] for x in curtas)))))

    for x in ruins[:14]:
        L.append(u"   ✗ %s — escrito `%s` (de %s), ouvido `%s`  erro %.2f"
                 % (x[u"arquivo"], x[u"silaba"], x[u"palavra"].upper(),
                    x[u"ouvido"], x[u"erro"]))
    if len(ruins) > 14:
        L.append(u"   ... e mais %d" % (len(ruins) - 14))

    # ---- a segunda medida: a mesma silaba, de palavras diferentes ----------
    pares = irmas(linhas)
    if pares and hasattr(ouve, u"le"):
        difs = []
        for sil, grupo in pares:
            for j in range(1, len(grupo)):
                a = os.path.join(pasta, u"audio", grupo[0][u"arquivo"])
                b = os.path.join(pasta, u"audio", grupo[j][u"arquivo"])
                d = parecidas(ouve.le, a, b)
                if d is not None:
                    difs.append((d, sil, grupo[0][u"palavra"], grupo[j][u"palavra"]))
        if difs:
            difs.sort()
            L.append(u"   irmãs: %d par(es) da MESMA silaba vindos de palavras "
                     u"diferentes · distancia mediana %.3f · pior %.3f (%s: %s x %s)"
                     % (len(difs), difs[len(difs) // 2][0], difs[-1][0],
                        difs[-1][1], difs[-1][2], difs[-1][3]))

    if medir:
        L.append(u"   MODO --medir: nao reprovo. E desta distribuicao que sai o corte.")
        return 0, L, linhas
    return (1 if ruins else 0), L, linhas


def main():
    args = sys.argv[1:]
    modelo, limite, so, medir, pastas = MODELO_PADRAO, 0.5, 0, False, []
    i = 0
    while i < len(args):
        a = args[i]
        if a == u"--modelo":
            i += 1
            modelo = args[i]
        elif a == u"--limite":
            i += 1
            limite = float(args[i])
        elif a == u"--so":
            i += 1
            so = int(args[i])
        elif a == u"--medir":
            medir = True
        else:
            pastas.append(a.rstrip(u"/"))
        i += 1
    if not pastas:
        print(u"uso: python3 _qa/ouvir_silaba.py <pasta> [--medir] [--so N]")
        return 2

    ouve, motivo = carrega(modelo)
    if ouve is None:
        print(u"NAO MEDI: %s" % motivo)
        print(u"   (o modelo mora no HuggingFace, que o chat NAO alcanca — 403 "
              u"medido em 17/set/2026. Este portao roda no Actions: `ouvir.yml`.)")
        return 2

    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    pior = 0
    for pasta in pastas:
        print(u"\n%s -> o ouvido da silaba (modelo %s, corte %.2f)"
              % (pasta, modelo.split(u"/")[-1], limite))
        cod, L, linhas = confere(pasta, ouve, limite, so, medir)
        for lin in L:
            print(lin)
        print(u"   %s" % {0: u"ok: os recortes dizem a silaba que esta escrita",
                          1: u"REPROVADO: ha recorte dizendo outra coisa",
                          2: u"NAO MEDI"}[cod])
        if linhas is not None:
            nome = (pasta.strip(u"_/") or u"raiz") + u"-silabas"
            io.open(os.path.join(SAIDA, u"%s.json" % nome), u"w",
                    encoding=u"utf-8").write(json.dumps(
                        {u"modelo": modelo, u"limite": limite, u"pares": linhas},
                        ensure_ascii=False, indent=1))
            md = [u"# O ouvido da sílaba — `%s`" % pasta, u"",
                  u"Modelo `%s` · corte %.2f · %d recortes."
                  % (modelo, limite, len(linhas)), u"",
                  u"| erro | arquivo | escrito | ouvido | de |",
                  u"|---|---|---|---|---|"]
            for x in sorted(linhas, key=lambda y: -y[u"erro"]):
                md.append(u"| %.2f | `%s` | %s | %s | %s |"
                          % (x[u"erro"], x[u"arquivo"], x[u"silaba"],
                             x[u"ouvido"] or u"—", x[u"palavra"].upper()))
            io.open(os.path.join(SAIDA, u"%s.md" % nome), u"w",
                    encoding=u"utf-8").write(u"\n".join(md) + u"\n")
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
