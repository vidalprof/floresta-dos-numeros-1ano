# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "TODA FALA SAI COM A MESMA FORÇA?"  (0v)

 ⭐ DE ONDE ELE NASCEU (19/set/2026, cobrança do Marcos: *"os áudios têm que
    ficarem perfeitos"*). Os portões de voz da casa mediam tudo, menos a única
    coisa que o ouvido sente primeiro: **o volume**. Havia portão para a fala
    que falta (`vozfalta`), para a voz-robô (`vozrobo`), para a palavra que a
    voz erra (`falas.py`), para a opção muda (`voz_opcao`) e até para a
    pronúncia (o Vosk dentro do `entregar.yml`). Nenhum abria o mp3 para ver se
    ele sai **audível**.

 ⚠️ O QUE A MEDIÇÃO ACHOU, no dia em que este arquivo nasceu: em CINCO cadernos
    medidos, 2 a 3 falas de cada um saem **7 dB mais baixas** que as outras —
    sempre as MESMAS, e sempre pelo mesmo motivo: são **palavras curtas e
    isoladas** ("Livros.", "e.", "O mar."). O Edge TTS dá menos energia a uma
    palavra solta do que a uma frase. Sete decibéis é o dobro/metade da força
    percebida: no PC da escola, com o alto-falante no meio do caminho, a criança
    aperta o botão da opção e não ouve nada — e escolhe pelo desenho, que é
    exatamente o defeito que o alto-falante da resposta existe para matar.

 ⚠️ POR QUE O **PICO** E NÃO A MÉDIA (e isto é medida, não palpite): o
    `mean_volume` do ffmpeg divide pela DURAÇÃO INTEIRA, então uma fala longa,
    cheia de pausas, mede baixo sem ser baixa. Medi as duas coisas nas mesmas
    701 falas: pelo `mean_volume` o espalhamento dava 10,8 dB e acusava falas
    boas; pelo PICO dava 6 dB e acusava exatamente as duas que o ouvido pega.
    O mesmo vale para o LUFS integrado, pelo mesmo motivo (a janela de
    integração é maior que a fala curta) — é a lição que o `_qa/kvoz.py` já
    tinha pago nos 882 recortes de sílaba.

 ⚠️ E O LIMIAR É COMPARATIVO, NÃO ABSOLUTO: cada caderno tem a sua mediana (o
    Edge TTS muda de nível entre vozes). O que reprova é a fala que destoa das
    IRMÃS dela — porque é o degrau entre uma fala e a seguinte que a criança
    sente, não o nível absoluto.

 ⚠️ PALPITE DECLARADO (está dito aqui e é impresso na saída): os 6 dB de
    tolerância são ESCOLHA MINHA, não medida com criança. Vêm de que 6 dB é,
    grosso modo, a metade da força percebida — abaixo disso a fala continua
    audível no mesmo volume de sistema. Se um dia o Marcos disser que ouviu
    degrau menor que isso, ganha a sala, não a minha conta.

 CONSERTO: `python3 _padrao/voz_forca.py <pasta>` — ele levanta SÓ as falas que
 destoam até a mediana do caderno, por GANHO PURO (nada de compressão, nada de
 `loudnorm`, que em áudio curto vira normalizador de pico). As outras não são
 tocadas, e por isso o git não incha.

 Uso:  python3 _qa/voz_forca.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import subprocess
import sys

try:
    import concurrent.futures as cf
except ImportError:                                        # pragma: no cover
    cf = None

TOLERANCIA_DB = 6.0        # ⚠️ PALPITE DECLARADO — ver o cabeçalho


def pico(cam):
    u"""o pico de amplitude do arquivo, em dBFS (None se o ffmpeg não abriu)."""
    try:
        r = subprocess.run([u"ffmpeg", u"-hide_banner", u"-i", cam,
                            u"-af", u"volumedetect", u"-f", u"null", u"-"],
                           capture_output=True, text=True)
    except Exception:
        return None
    m = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr or u"")
    return float(m.group(1)) if m else None


def picos(arquivos):
    if cf:
        with cf.ThreadPoolExecutor(8) as ex:
            return list(ex.map(pico, arquivos))
    return [pico(a) for a in arquivos]


def mede(pasta):
    u"""devolve (mediana, [(pico, id, texto)]) ou (None, motivo)."""
    pasta = pasta.rstrip(u"/")
    audio = os.path.join(pasta, u"audio")
    cam = os.path.join(pasta, u"falas.json")
    if not os.path.isdir(audio):
        return None, u"nao tem pasta audio/"
    if subprocess.run([u"which", u"ffmpeg"], capture_output=True).returncode:
        return None, u"o ffmpeg nao esta aqui"
    texto = {}
    if os.path.exists(cam):
        d = json.load(io.open(cam, encoding=u"utf-8"))
        for f in (d if isinstance(d, list) else d.get(u"falas", [])):
            texto[f[u"id"]] = f.get(u"texto", u"")
    arqs = sorted(a for a in os.listdir(audio) if a.endswith(u".mp3"))
    if not arqs:
        return None, u"nenhum mp3 gravado ainda (o entregar.yml grava ao publicar)"
    cams = [os.path.join(audio, a) for a in arqs]
    vals = [(p, a[:-4], texto.get(a[:-4], u"")) for p, a in zip(picos(cams), arqs)
            if p is not None]
    if not vals:
        return None, u"o ffmpeg nao abriu nenhum mp3"
    vals.sort()
    return vals[len(vals) // 2][0], vals


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/voz_forca.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    if not os.path.exists(os.path.join(pasta, u"falas.json")):
        print(u"%s -> NAO SE APLICA: sem falas.json." % pasta)
        return 2
    med, vals = mede(pasta)
    if med is None:
        print(u"%s -> NAO MEDI: %s (isso nao e 'passou')." % (pasta, vals))
        return 2

    baixas = [v for v in vals if v[0] < med - TOLERANCIA_DB]
    altas = [v for v in vals if v[0] > -0.1]
    print(u"%s -> forca da voz: %d mp3 medido(s) | pico mediano %.1f dB | "
          u"menor %.1f | maior %.1f"
          % (pasta, len(vals), med, vals[0][0], vals[-1][0]))
    print(u"   PALPITE DECLARADO (nunca cronometrado com crianca): a tolerancia "
          u"de %.0f dB e escolha minha, nao medida de sala." % TOLERANCIA_DB)
    if altas:
        print(u"   %d fala(s) ESTOURADA(S) (pico em 0 dB — a voz satura):" % len(altas))
        for p, i, t in altas[:8]:
            print(u'    x %5.1f dB  %-12s %r' % (p, i, t[:46]))
    if baixas:
        print(u"   %d fala(s) MAIS BAIXA(S) que as irmas em mais de %.0f dB:"
              % (len(baixas), TOLERANCIA_DB))
        for p, i, t in baixas[:10]:
            print(u'    x %5.1f dB  %-12s %r' % (p, i, t[:46]))
        print(u"   a crianca aperta o alto-falante da opcao e nao ouve — e escolhe")
        print(u"   pelo desenho, que e o defeito que o alto-falante existe para matar.")
    if baixas or altas:
        print(u"   conserto: python3 _padrao/voz_forca.py %s" % pasta)
        return 1
    print(u"   ok: nenhuma fala destoa das irmas; nada estourado.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
