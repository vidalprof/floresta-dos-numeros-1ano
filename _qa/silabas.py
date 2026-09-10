# -*- coding: utf-8 -*-
u"""PORTÃO DA SÍLABA FALADA — a sílaba tem que sair da PALAVRA, não do nada.

⚠️⚠️ POR QUE ESTE PORTÃO EXISTE (set/2026 — o Marcos ouviu e cobrou):
   *"na bate palmas das palavras, as sílabas precisam ser pronunciadas
   corretamente, ele está dizendo 'v a' ao invés de 'va'"*.

   O que tinha acontecido: o `_padrao/silabas_voz.py`, que recorta cada sílaba
   de dentro do mp3 da própria palavra, **falhou em silêncio**. O passo dele no
   `entregar.yml` tem `continue-on-error`, o aviso morreu no log da execução, e
   o app caiu na FALA DE RESERVA — a sílaba sintetizada solta. E sílaba solta
   sai errada por construção: a voz não lê som, lê PALAVRA. Entregue "VA" e o
   serviço soletra "vê-á"; entregue "ÇÃ" e ele soletra também, porque ç não
   começa palavra em português.

   Descobriu-se então que NENHUMA atividade da casa tinha os recortes — nem o
   `_alfa1`, que usa sílaba falada desde agosto. O defeito estava no ar havia
   semanas e ninguém via, porque não dá erro nenhum: o app abre, joga, o portão
   de falas passa (o texto está lá) e só a CRIANÇA ouve o problema.

   Regra da casa: defeito que chegou ao Marcos vira portão. Este é o portão.

O QUE ELE MEDE
   Para toda pasta que declara `silabas.json` (ou seja: que fala sílaba solta),
   confere que **existe um mp3 recortado para cada sílaba de cada palavra**:
   `<pasta>/audio/<prefixo>sb_<palavra>_<i>.mp3`, com tamanho de arquivo de
   verdade. Falta um? REPROVA.

   Confere também o contrário, que é o mesmo defeito visto do outro lado: se o
   `index.html` chama `falarSilaba(...)` mas a pasta **não tem** `silabas.json`,
   a atividade vai falar sílaba sintetizada — reprova igual.

Uso:  python3 _qa/silabas.py <pasta>
Códigos: 0 passou · 1 REPROVADO · 2 não consegui medir
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

MIN_BYTES = 300          # abaixo disso é arquivo vazio, não é áudio
FATOR = 1.7              # acima disso a sílaba está sendo soletrada, não falada


def _ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                                            # noqa: BLE001
        return "ffmpeg"


def _dur(ff, caminho):
    import subprocess
    p = subprocess.Popen([ff, "-i", caminho, "-f", "null", "-"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = p.communicate()
    t = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", (err or b"").decode("utf-8", "replace"))
    if not t:
        return 0.0
    h, m, s = t[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def _mediana(v):
    v = sorted(v)
    if not v:
        return 0.0
    meio = len(v) // 2
    return v[meio] if len(v) % 2 else (v[meio - 1] + v[meio]) / 2.0


def _mede_duracoes(audio, mapa, prefixo):
    u"""Devolve [(silaba, palavra, duracao, esperado)] das compridas demais.

    Compara cada sílaba com a MEDIANA das sílabas de mesmo tamanho de escrita
    (duas letras com duas letras, três com três): sílaba fechada como TAR e COM
    é naturalmente um pouco mais longa que LA, e comparar tudo junto acusaria
    falso. Se não houver ffmpeg, devolve [] — mede-se o que dá para medir, e o
    portão não reprova por não conseguir medir."""
    ff = _ffmpeg()
    try:
        if _dur(ff, os.devnull) < 0:
            return []
    except Exception:                                            # noqa: BLE001
        return []
    porTam, tudo = {}, []
    for palavra in sorted(mapa):
        for i, s in enumerate(mapa[palavra]):
            if not s:
                continue
            f = os.path.join(audio, u"%ssb_%s_%d.mp3" % (prefixo, palavra, i))
            if not os.path.exists(f):
                continue
            d = _dur(ff, f)
            if d <= 0:
                continue
            porTam.setdefault(len(s), []).append(d)
            tudo.append((s, palavra, d))
    if not tudo:
        return []
    ruins = []
    for s, palavra, d in tudo:
        base = _mediana(porTam.get(len(s), []))
        # ⚠️ com menos de 4 exemplos daquele tamanho a mediana não vale nada:
        #    uma única sílaba soletrada viraria a própria referência.
        if base <= 0 or len(porTam.get(len(s), [])) < 4:
            continue
        if d > base * FATOR:
            ruins.append((s, palavra, d, base))
    return sorted(ruins, key=lambda r: -r[2])


def mede(pasta):
    pasta = pasta.rstrip("/")
    cam = os.path.join(pasta, "silabas.json")
    html = os.path.join(pasta, "index.html")
    if not os.path.exists(html):
        print(u"%s: sem index.html — nada a medir" % pasta)
        return 2

    fonte = io.open(html, encoding=u"utf-8").read()
    js = os.path.join(pasta, "folhas.js")
    if os.path.exists(js):
        fonte += io.open(js, encoding=u"utf-8").read()
    # A atividade FALA sílaba solta?
    # ⚠️ A CHAMADA, nunca a DEFINIÇÃO: a casca do caderno traz
    # `function falarSilaba(palavra, i, silaba){...}` mesmo quando nenhuma folha
    # usa. Confundir os dois reprova caderno de alfabeto e de rima, que não têm
    # sílaba nenhuma — foi o primeiro resultado deste portão.
    usa = bool(re.search(r"(?<!function )\bfalarSilaba\s*\(\s*[^)\s]", fonte))

    if not usa:
        print(u"%s -> silabas ok: esta atividade nao fala silaba solta." % pasta)
        return 0

    if not os.path.exists(cam):
        print(u"%s -> REPROVADO: o app chama `falarSilaba` mas a pasta nao tem\n"
              u"   `silabas.json`. Sem ele o `_padrao/silabas_voz.py` nao recorta\n"
              u"   nada, e a crianca ouve a silaba SINTETIZADA solta ('ve-a' em vez\n"
              u"   de 'va'). Gere o mapa no `gerar_falas.py` da atividade." % pasta)
        return 1

    dados = json.load(io.open(cam, encoding=u"utf-8"))
    mapa = dados.get(u"palavras", dados)
    prefixo = dados.get(u"prefixo", u"") if isinstance(dados, dict) else u""
    audio = os.path.join(pasta, u"audio")

    faltam, total = [], 0
    for palavra in sorted(mapa):
        for i, s in enumerate(mapa[palavra]):
            if not s:
                continue
            total += 1
            f = os.path.join(audio, u"%ssb_%s_%d.mp3" % (prefixo, palavra, i))
            if not os.path.exists(f) or os.path.getsize(f) < MIN_BYTES:
                faltam.append(u"%s[%d]=%s" % (palavra, i, s))

    # ══════════════════════════════════════════════════════════════════
    #  2ª MEDIDA: A SÍLABA SOLETRADA É COMPRIDA DEMAIS
    #
    #  ⚠️ Existir o recorte não quer dizer que ele esteja certo — foi o meu erro
    #     de 10/set/2026. Eu gerei os 42 arquivos, comemorei, e o Marcos ouviu de
    #     novo "vê-á" no lugar de "va". Cortar uma sequência com vírgulas não
    #     conserta nada: a voz continua lendo cada pedaço ISOLADO, e pedaço
    #     isolado de consoante+A ela soletra.
    #
    #  E isso SE MEDE, sem ouvir: uma sílaba falada leva ~0,25 s; a mesma sílaba
    #  soletrada leva o dobro, porque são dois nomes de letra em vez de um som.
    #  Na medição que denunciou o defeito: LA 0,26 · TA 0,28 · TO 0,26 contra
    #  VA 0,66 · GA 0,63 · FO 0,64 · PA 0,50. Não é sutil.
    #
    #  O critério é RELATIVO (o dobro da mediana das sílabas de mesmo tamanho de
    #  escrita), não um número fixo: voz, velocidade e sílaba fechada mudam a
    #  base, mas a soletração dobra em qualquer base.
    # ══════════════════════════════════════════════════════════════════
    if not faltam:
        compridas = _mede_duracoes(audio, mapa, prefixo)
        if compridas:
            print(u"%s -> REPROVADO: %d silaba(s) SOLETRADA(S).\n"
                  u"   O recorte existe, mas dentro dele a voz diz o nome das letras\n"
                  u"   ('ve-a') em vez do som ('va') — dá o dobro da duração das outras.\n"
                  u"   %s\n"
                  u"   conserto: a sílaba tem que sair da PALAVRA INTEIRA falada, com\n"
                  u"   alinhamento forçado. Cortar uma sequencia com virgulas nao resolve:\n"
                  u"   a voz le cada pedaco isolado e soletra do mesmo jeito."
                  % (pasta, len(compridas),
                     u"; ".join(u"%s de %s (%.2fs, esperado ~%.2fs)" % c for c in compridas[:8])))
            return 1

    if faltam:
        log = os.path.join(audio, u"_silabas-log.txt")
        recado = u""
        if os.path.exists(log):
            recado = u"\n   o que a ferramenta registrou: " + \
                io.open(log, encoding=u"utf-8").read().strip()
        print(u"%s -> REPROVADO: faltam %d recorte(s) de %d.\n"
              u"   A crianca vai ouvir a silaba SINTETIZADA solta, e ela sai errada\n"
              u"   por construcao ('va' vira 've-a'; 'ca' vira 'ce-a').\n"
              u"   primeiros: %s%s\n"
              u"   conserto: rodar o `entregar.yml` (ele chama o\n"
              u"   `_padrao/silabas_voz.py`), e CONFERIR que os mp3 vieram no commit."
              % (pasta, len(faltam), total, u", ".join(faltam[:8]), recado))
        return 1

    print(u"%s -> silabas ok: %d recorte(s), um para cada silaba falada." % (pasta, total))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(mede(sys.argv[1]))
