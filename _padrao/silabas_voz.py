#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""A SÍLABA SAI DE DENTRO DA PALAVRA — não se sintetiza solta.

⭐ ORDEM DO MARCOS (set/2026): *"a pronúncia das sílabas precisa ser precisa e
   melhorada, use alguma ferramenta profissional para melhorar isso"*.

────────────────────────────────────────────────────────────────────────
POR QUE A SÍLABA SOLTA SAI ERRADA — e não é culpa da voz

Um sintetizador não lê som: lê PALAVRA. Entregue a ele o texto "çã" e ele não
tem regra nenhuma, porque **ç não começa palavra em português** — sai soletrado.
Entregue "xí" e ele hesita entre [ʃ] e [ks]. E há um caso pior porque é
invisível: "bo" é [bɔ] em BOLA e [bo] em BOLO. A MESMA sílaba escrita tem dois
sons, e quem decide é a PALAVRA. Sintetizar "bo" sozinho é apostar numa delas.

Escrever a sílaba "como se fala" (foi o remendo anterior: çã → "sã") conserta
um caso de cada vez e nunca fecha a família.

────────────────────────────────────────────────────────────────────────
O QUE ESTA FERRAMENTA FAZ

Grava a palavra INTEIRA, sílaba por sílaba, numa tacada só — e recorta.

  1. manda ao Edge TTS o texto `gi, ra, fa` (as sílabas da palavra, na ordem);
  2. o serviço devolve, junto com o áudio, os **marcadores de tempo** de cada
     pedaço (WordBoundary: início e duração em unidades de 100 ns). Isto é do
     protocolo, não é adivinhação minha;
  3. corta o mp3 nesses tempos com ffmpeg e grava um arquivo por sílaba.

Ou seja: a criança ouve a sílaba **na voz, no ritmo e na altura daquela
palavra**, porque o áudio veio da mesma respiração. Nada de fragmento avulso.

⚠️ Por que ler a sequência e não a palavra corrida: para cortar dentro de
   "girafa" eu precisaria de alinhamento forçado (nível de fonema), que é
   pesado e frágil num runner. Lendo `gi, ra, fa` o próprio serviço me dá o
   corte de graça e a leitura é a que a professora faz na roda — sílaba a
   sílaba, com a entoação da palavra.

Uso:
    python3 _padrao/silabas_voz.py <pasta>            # grava o que falta
    python3 _padrao/silabas_voz.py <pasta> --refazer  # regrava tudo

Lê   `<pasta>/silabas.json`  ->  {"girafa": ["GI","RA","FA"], ...}
Grava `<pasta>/audio/<prefixo>sb_<palavra>_<i>.mp3`
Anota `<pasta>/audio/_silabas.json` (o carimbo: só regrava o que mudou).

Códigos: 0 gravou (ou já estava) · 1 alguma falhou · 2 não consegui rodar.
"""
from __future__ import print_function

import asyncio
import io
import json
import os
import subprocess
import sys

RATE = "-10%"          # um tico mais devagar que a narração: é segmentação
FOLGA_MS = 60          # sobra no fim de cada corte, para não cortar o ar final
PAR = 4                # palavras ao mesmo tempo


def _ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                                            # noqa: BLE001
        return "ffmpeg"


async def _uma(sem, edge_tts, texto, voz, destino_base, silabas, prefixo, palavra):
    u"""Grava a sequência da palavra e corta cada sílaba. Devolve nº de cortes."""
    async with sem:
        for tent in (1, 2, 3):
            try:
                com = edge_tts.Communicate(texto, voz, rate=RATE)
                audio = io.BytesIO()
                marcas = []
                async for pedaco in com.stream():
                    if pedaco["type"] == "audio":
                        audio.write(pedaco["data"])
                    elif pedaco["type"] == "WordBoundary":
                        marcas.append((pedaco["offset"], pedaco["duration"]))
                dados = audio.getvalue()
                if len(dados) < 800 or len(marcas) < len(silabas):
                    raise RuntimeError("audio curto ou marcas de menos "
                                       "(%d marcas para %d silabas)"
                                       % (len(marcas), len(silabas)))
                inteiro = destino_base + "_todo.mp3"
                open(inteiro, "wb").write(dados)
                ff = _ffmpeg()
                n = 0
                for i, s in enumerate(silabas):
                    ini = marcas[i][0] / 10000000.0
                    dur = marcas[i][1] / 10000000.0 + FOLGA_MS / 1000.0
                    saida = os.path.join(os.path.dirname(destino_base),
                                         "%ssb_%s_%d.mp3" % (prefixo, palavra, i))
                    r = subprocess.call(
                        [ff, "-y", "-loglevel", "error", "-ss", "%.3f" % ini,
                         "-t", "%.3f" % dur, "-i", inteiro, "-c", "copy", saida])
                    if r != 0 or not os.path.exists(saida) or os.path.getsize(saida) < 300:
                        # sem cópia direta: recodifica (mp3 nem sempre corta no quadro)
                        subprocess.call(
                            [ff, "-y", "-loglevel", "error", "-ss", "%.3f" % ini,
                             "-t", "%.3f" % dur, "-i", inteiro, saida])
                    if os.path.exists(saida) and os.path.getsize(saida) > 300:
                        n += 1
                try:
                    os.remove(inteiro)
                except OSError:
                    pass
                return n
            except Exception as e:                               # noqa: BLE001
                if tent == 3:
                    print(u"   ERRO em %s: %s" % (palavra, e))
                    return 0
                await asyncio.sleep(1.5 * tent)
    return 0


async def _tudo(pasta, mapa, voz, prefixo, refazer):
    import edge_tts
    audio = os.path.join(pasta, "audio")
    if not os.path.isdir(audio):
        os.makedirs(audio)
    campo = os.path.join(audio, "_silabas.json")
    carimbo = {}
    if os.path.exists(campo) and not refazer:
        try:
            carimbo = json.load(io.open(campo, encoding="utf-8"))
        except Exception:                                        # noqa: BLE001
            carimbo = {}
    sem = asyncio.Semaphore(PAR)
    tarefas, alvos = [], []
    for palavra in sorted(mapa):
        sil = [s for s in mapa[palavra] if s]
        if not sil:
            continue
        assinatura = "|".join(sil) + "|" + voz + "|" + RATE
        prontos = all(os.path.exists(os.path.join(
            audio, "%ssb_%s_%d.mp3" % (prefixo, palavra, i))) for i in range(len(sil)))
        if carimbo.get(palavra) == assinatura and prontos:
            continue
        texto = u", ".join(s.lower() for s in sil) + u"."
        base = os.path.join(audio, "_seq_" + palavra)
        alvos.append((palavra, assinatura, len(sil)))
        tarefas.append(_uma(sem, edge_tts, texto, voz, base, sil, prefixo, palavra))
    if not tarefas:
        print(u"%s -> silabas: nada novo (todas ja gravadas)" % pasta)
        return 0
    print(u"%s -> gravando %d palavra(s) em silabas..." % (pasta, len(tarefas)))
    saidas = await asyncio.gather(*tarefas)
    falhou = 0
    for (palavra, assinatura, quantas), n in zip(alvos, saidas):
        if n == quantas:
            carimbo[palavra] = assinatura
        else:
            falhou += 1
            print(u"   %s: sairam %d de %d silabas" % (palavra, n, quantas))
    io.open(campo, "w", encoding="utf-8").write(
        json.dumps(carimbo, ensure_ascii=False, indent=1))
    print(u"%s -> silabas ok: %d palavra(s) gravadas, %d com falha"
          % (pasta, len(alvos) - falhou, falhou))
    return 1 if falhou else 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    pasta = args[0].rstrip("/")
    cam = os.path.join(pasta, "silabas.json")
    if not os.path.exists(cam):
        print(u"%s: sem silabas.json — nada a fazer" % pasta)
        return 0
    dados = json.load(io.open(cam, encoding="utf-8"))
    mapa = dados.get("palavras", dados)
    prefixo = dados.get("prefixo", "") if isinstance(dados, dict) else ""
    voz = "pt-BR-AntonioNeural"
    cv = os.path.join(pasta, "voz.txt")
    if os.path.exists(cv):
        v = io.open(cv, encoding="utf-8").read().strip()
        if v:
            voz = v
    try:
        import edge_tts                                          # noqa: F401
    except ImportError:
        print(u"nao consegui rodar: falta o edge-tts (roda no workflow)")
        return 2
    return asyncio.get_event_loop().run_until_complete(
        _tudo(pasta, mapa, voz, prefixo, "--refazer" in sys.argv))


if __name__ == "__main__":
    sys.exit(main())
