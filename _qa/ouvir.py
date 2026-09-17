# -*- coding: utf-8 -*-
u"""
============================================================
 O OUVIDO — a voz e ESCUTADA e comparada com o que esta escrito

 ⭐ PEDIDO DO MARCOS (17/set/2026): *"o banco de audio e para comparar se a fala
    esta certa, e isso que quero"* — depois de eu dizer que nao dava, e ele
    lembrar, de novo: ***"vc pode usar o GitHub lembra?"***. Ele esta certo e a
    regra ja estava escrita no CLAUDE.md: **o chat nao tem internet; o Actions
    tem**. Se eu me pegar dizendo "nao consigo", a resposta certa e ACIONAR UM
    WORKFLOW.

 O QUE ELE FAZ: abre cada `<pasta>/audio/<id>.mp3`, passa um reconhecedor de
 fala em portugues por cima, e compara o que OUVIU com o texto que gerou aquele
 mp3 (o `<pasta>/falas.json`, que e a VERDADE da casa). E o teste de ida e
 volta: **texto -> voz -> texto**.

 POR QUE ISTO E DIFERENTE DE TUDO O QUE JA HAVIA. O `falas.json` garante que o
 texto pedido e o texto escrito; o carimbo sha1 garante que o mp3 e daquele
 texto. Nenhum dos dois ouve nada. Se a voz engolir uma palavra, trocar a
 pronuncia, cortar no meio ou gravar um arquivo truncado, os dois continuam
 dizendo "ok" — e a crianca ouve a coisa errada. **mp3 nao se le; agora se
 ouve.**

 ⚠️⚠️ O LIMITE, ESCRITO ANTES DO RESULTADO, senao o portao vira medida falsa:
    1. O reconhecedor ERRA. Ele e bom em frase inteira e FRACO em pedaco curto.
       Por isso os recortes de silaba (`<prefixo>sb_<palavra>_<n>.mp3`, que tem
       200 a 400 ms) sao ouvidos e RELATADOS, mas NAO reprovam: um "sa" de
       300 ms mal reconhecido nao prova nada sobre o mp3.
    2. A comparacao e por TEXTO ACHATADO (minuscula, sem acento, sem
       pontuacao). "SALÃO" e "salao" sao a mesma coisa aqui — e tem de ser,
       senao o portao acusa o proprio reconhecedor.
    3. O CORTE de quanto erro reprova NAO foi inventado: sai da MEDIDA da
       primeira rodada (modo `--medir`), e fica escrito no topo do relatorio,
       com a data e o modelo. Trocou o modelo, remede.

 Uso:
   python3 _qa/ouvir.py <pasta> [<pasta2> ...] [--modelo small] [--medir]
                        [--limite 0.35] [--so 60]
   `--medir`  ouve tudo, imprime a distribuicao e NAO reprova (e o que calibra).
   `--so N`   ouve so as N primeiras falas (prova de bancada, para medir tempo).

 Saida: `_qa/_ouvido/<pasta>.json` (todos os pares ouvido x escrito) e
        `_qa/_ouvido/<pasta>.md` (o que um humano le).
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


# ---------------------------------------------------------------------------
# achatar: o que entra na comparacao
# ---------------------------------------------------------------------------
def achata(s):
    u"""minuscula, sem acento, sem pontuacao, um espaco so.

    ⚠️ Isto NAO e frouxidao: o reconhecedor devolve "salao" para "SALÃO" e
    "voce" para "você" conforme o modelo, e comparar acento a acento faria o
    portao acusar o proprio reconhecedor em vez do mp3."""
    s = unicodedata.normalize(u"NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != u"Mn")
    s = s.lower().replace(u"ç", u"c")
    s = re.sub(r"[^a-z0-9 ]+", u" ", s)
    return re.sub(r"\s+", u" ", s).strip()


def distancia(a, b):
    u"""Levenshtein em caracteres, sem dependencia nenhuma."""
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
    u"""0 = identico; 1 = nada a ver. Normalizado pelo tamanho do ESCRITO,
    que e o que a crianca deveria ouvir."""
    e, o = achata(escrito), achata(ouvido)
    if not e:
        return 0.0 if not o else 1.0
    return min(1.0, distancia(e, o) / float(len(e)))


# ---------------------------------------------------------------------------
# o reconhecedor
# ---------------------------------------------------------------------------
def carrega(modelo):
    u"""Devolve uma funcao ouve(caminho) -> texto, ou None com o motivo."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:                                     # noqa: BLE001
        return None, u"sem o `faster-whisper` (%s). No runner: pip install faster-whisper" % e
    try:
        m = WhisperModel(modelo, device=u"cpu", compute_type=u"int8")
    except Exception as e:                                       # noqa: BLE001
        return None, u"nao consegui carregar o modelo `%s`: %s" % (modelo, e)

    def ouve(caminho):
        segs, _info = m.transcribe(caminho, language=u"pt", beam_size=5,
                                   vad_filter=False)
        return u" ".join(s.text for s in segs).strip()
    return ouve, None


# ---------------------------------------------------------------------------
def falas_da_pasta(pasta):
    u"""[(id, texto, caminho do mp3, e_silaba)] — o `falas.json` e a verdade."""
    fj = os.path.join(pasta, u"falas.json")
    audio = os.path.join(pasta, u"audio")
    if not os.path.exists(fj):
        return None
    try:
        F = json.load(io.open(fj, encoding=u"utf-8"))
    except ValueError:
        return None
    saida = []
    for f in F:
        mp3 = os.path.join(audio, f[u"id"] + u".mp3")
        if os.path.exists(mp3):
            saida.append((f[u"id"], f[u"texto"], mp3, False))
    # e os RECORTES de silaba, que nao moram no falas.json: eles nascem do
    # `silabas.json`, cortados de dentro da palavra inteira.
    sj = os.path.join(pasta, u"silabas.json")
    if os.path.exists(sj):
        try:
            S = json.load(io.open(sj, encoding=u"utf-8"))
        except ValueError:
            S = {}
        pref = S.get(u"prefixo", u"")
        for palavra, sil in sorted((S.get(u"palavras") or {}).items()):
            base = re.sub(r"[^a-z0-9]", u"",
                          unicodedata.normalize(u"NFKD", palavra.lower())
                          .encode(u"ascii", u"ignore").decode())
            for i, s in enumerate(sil):
                mp3 = os.path.join(audio, u"%ssb_%s_%d.mp3" % (pref, base, i))
                if os.path.exists(mp3):
                    saida.append((os.path.basename(mp3)[:-4], s, mp3, True))
    return saida


def confere(pasta, ouve, limite, so, medir):
    itens = falas_da_pasta(pasta)
    if itens is None:
        return 2, [u"   sem `falas.json`: NAO MEDI (e isto nao e 'passou' — "
                   u"atividade sem falas.json nao tem como ser conferida)"], None
    if not itens:
        return 2, [u"   o `falas.json` existe mas nenhum mp3 esta na pasta: "
                   u"NAO MEDI. A voz e gravada pelo `entregar.yml` ao publicar."], None
    if so:
        itens = itens[:so]

    linhas, ruins, fracos = [], [], []
    for n, (ident, escrito, mp3, e_sil) in enumerate(itens, 1):
        try:
            ouvido = ouve(mp3)
        except Exception as e:                                   # noqa: BLE001
            ouvido = u"<<ERRO: %s>>" % e
        er = erro(escrito, ouvido)
        linhas.append({u"id": ident, u"escrito": escrito, u"ouvido": ouvido,
                       u"erro": round(er, 3), u"silaba": e_sil,
                       u"bytes": os.path.getsize(mp3)})
        if er > limite:
            (fracos if e_sil else ruins).append(linhas[-1])
        if n % 50 == 0:
            print(u"      ... %d de %d" % (n, len(itens)))

    L = [u"   ouviu %d mp3 (%d fala(s) + %d recorte(s) de silaba)"
         % (len(itens), sum(1 for x in linhas if not x[u"silaba"]),
            sum(1 for x in linhas if x[u"silaba"]))]

    frases = [x[u"erro"] for x in linhas if not x[u"silaba"]]
    if frases:
        frases_ord = sorted(frases)
        meio = frases_ord[len(frases_ord) // 2]
        L.append(u"   erro nas FALAS: mediana %.3f · pior %.3f · %d acima de %.2f"
                 % (meio, frases_ord[-1], len(ruins), limite))
    sil = [x[u"erro"] for x in linhas if x[u"silaba"]]
    if sil:
        sil_ord = sorted(sil)
        L.append(u"   erro nos RECORTES DE SILABA: mediana %.3f · pior %.3f "
                 u"(informativo — o reconhecedor e fraco em 300 ms, e isso "
                 u"esta declarado)" % (sil_ord[len(sil_ord) // 2], sil_ord[-1]))

    for x in ruins[:12]:
        L.append(u"   ✗ %s" % x[u"id"])
        L.append(u"       escrito: %s" % x[u"escrito"][:96])
        L.append(u"       ouvido : %s   (erro %.2f)" % (x[u"ouvido"][:96], x[u"erro"]))
    if len(ruins) > 12:
        L.append(u"   ... e mais %d" % (len(ruins) - 12))
    for x in fracos[:6]:
        L.append(u"   · (silaba, nao reprova) %s: escrito %s / ouvido %s"
                 % (x[u"id"], x[u"escrito"], x[u"ouvido"][:40]))

    if medir:
        L.append(u"   MODO --medir: nao reprovo, so mostro a distribuicao. "
                 u"E dela que sai o corte.")
        return 0, L, linhas
    return (1 if ruins else 0), L, linhas


def main():
    args = sys.argv[1:]
    modelo, limite, so, medir = u"small", 0.35, 0, False
    pastas = []
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
        print(u"uso: python3 _qa/ouvir.py <pasta> [--modelo small] [--medir] [--so N]")
        return 2

    ouve, motivo = carrega(modelo)
    if ouve is None:
        print(u"NAO MEDI: %s" % motivo)
        print(u"   (o reconhecedor mora no HuggingFace, que o chat NAO alcanca "
              u"— 403 medido em 17/set/2026. Este portao roda no Actions: "
              u"workflow `ouvir.yml`.)")
        return 2

    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)
    pior = 0
    for pasta in pastas:
        print(u"\n%s -> o ouvido (modelo %s, corte %.2f)" % (pasta, modelo, limite))
        cod, L, linhas = confere(pasta, ouve, limite, so, medir)
        for lin in L:
            print(lin)
        print(u"   %s" % {0: u"ok: a voz diz o que esta escrito",
                          1: u"REPROVADO: ha mp3 dizendo outra coisa",
                          2: u"NAO MEDI"}[cod])
        if linhas is not None:
            nome = pasta.strip(u"_/") or u"raiz"
            io.open(os.path.join(SAIDA, u"%s.json" % nome), u"w",
                    encoding=u"utf-8").write(json.dumps(
                        {u"modelo": modelo, u"limite": limite,
                         u"pares": linhas}, ensure_ascii=False, indent=1))
            md = [u"# O ouvido — `%s`" % pasta,
                  u"",
                  u"Modelo `%s` · corte %.2f · %d mp3 ouvidos." % (modelo, limite, len(linhas)),
                  u"",
                  u"| erro | id | escrito | ouvido |",
                  u"|---|---|---|---|"]
            for x in sorted(linhas, key=lambda y: -y[u"erro"])[:60]:
                md.append(u"| %.2f | `%s`%s | %s | %s |"
                          % (x[u"erro"], x[u"id"], u" ⟨sílaba⟩" if x[u"silaba"] else u"",
                             x[u"escrito"].replace(u"|", u"/"),
                             x[u"ouvido"].replace(u"|", u"/")))
            io.open(os.path.join(SAIDA, u"%s.md" % nome), u"w",
                    encoding=u"utf-8").write(u"\n".join(md) + u"\n")
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
