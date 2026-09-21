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
# o numero escrito e o numero FALADO sao duas escritas diferentes
# ---------------------------------------------------------------------------
# ⚠️⚠️ LICAO PAGA EM 21/set/2026, no caderno do dinheiro do 5o ano: o portao
#    acusou 12 falas de "tortas" e as doze estavam CERTAS. O texto dizia
#    "isso da 520 reais", a voz leu "quinhentos e vinte reais" — que e o certo —
#    e o reconhecedor devolveu as palavras, porque reconhecedor nenhum devolve
#    algarismo. Comparar "520" com "quinhentos e vinte" nao mede o mp3: mede a
#    distancia entre DUAS ESCRITAS do mesmo numero, e da 56% de diferenca num
#    audio impecavel. Entrega barrada por defeito que nao existia.
#    A regra que fica: quando os dois lados da comparacao podem escrever a mesma
#    coisa de formas diferentes, a normalizacao vai ANTES da regua — senao o
#    portao acusa o proprio alfabeto.
UNI = [u"zero", u"um", u"dois", u"tres", u"quatro", u"cinco", u"seis",
       u"sete", u"oito", u"nove", u"dez", u"onze", u"doze", u"treze",
       u"quatorze", u"quinze", u"dezesseis", u"dezessete", u"dezoito",
       u"dezenove"]
DEZ = [u"", u"", u"vinte", u"trinta", u"quarenta", u"cinquenta", u"sessenta",
       u"setenta", u"oitenta", u"noventa"]
CEM = [u"", u"cento", u"duzentos", u"trezentos", u"quatrocentos",
       u"quinhentos", u"seiscentos", u"setecentos", u"oitocentos",
       u"novecentos"]


def extenso(n):
    u"""Inteiro por extenso em portugues, ate 999.999 — sem acento, porque o
    `achata` ja tirou os acentos dos dois lados."""
    n = int(n)
    if n < 0:
        return u"menos " + extenso(-n)
    if n < 20:
        return UNI[n]
    if n < 100:
        d, u_ = divmod(n, 10)
        return DEZ[d] + (u" e " + UNI[u_] if u_ else u"")
    if n == 100:
        return u"cem"
    if n < 1000:
        c, r = divmod(n, 100)
        return CEM[c] + (u" e " + extenso(r) if r else u"")
    if n < 1000000:
        m, r = divmod(n, 1000)
        cab = u"mil" if m == 1 else extenso(m) + u" mil"
        if not r:
            return cab
        return cab + (u" e " if r < 100 or r % 100 == 0 else u" ") + extenso(r)
    # acima de um milhao nenhuma fala nossa chega; devolver o algarismo aqui
    # seria voltar ao defeito, entao quebra-se em blocos de mil.
    m, r = divmod(n, 1000000)
    cab = u"um milhao" if m == 1 else extenso(m) + u" milhoes"
    return cab + (u" e " + extenso(r) if r else u"")


def _dinheiro(m):
    u"""`R$ 97,50` -> `noventa e sete reais e cinquenta centavos`, que e o que a
    voz de verdade le."""
    inteiro, cent = int(m.group(1)), int(m.group(2))
    partes = []
    if inteiro or not cent:
        partes.append(extenso(inteiro) + (u" real" if inteiro == 1 else u" reais"))
    if cent:
        partes.append(extenso(cent) + (u" centavo" if cent == 1 else u" centavos"))
    return u" " + u" e ".join(partes) + u" "


# ---------------------------------------------------------------------------
# achatar: o que entra na comparacao
# ---------------------------------------------------------------------------
def achata(s):
    u"""minuscula, sem acento, sem pontuacao, numero por extenso, um espaco so.

    ⚠️ Isto NAO e frouxidao: o reconhecedor devolve "salao" para "SALÃO" e
    "voce" para "você" conforme o modelo, e comparar acento a acento faria o
    portao acusar o proprio reconhecedor em vez do mp3."""
    s = unicodedata.normalize(u"NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != u"Mn")
    s = s.lower().replace(u"ç", u"c")
    # o dinheiro PRIMEIRO, enquanto o `R$` e a virgula ainda existem
    s = re.sub(r"r\$?\s*(\d+)[,.](\d{2})\b", _dinheiro, s)
    s = re.sub(r"\b(\d+)[,.](\d{2})\s*(reais|real)\b", _dinheiro, s)
    # e depois todo algarismo solto que tenha sobrado
    s = re.sub(r"\d+", lambda m: u" " + extenso(m.group(0)) + u" ", s)
    s = re.sub(r"[^a-z ]+", u" ", s)
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
