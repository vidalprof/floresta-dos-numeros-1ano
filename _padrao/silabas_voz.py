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
import re
import subprocess
import sys

RATE = "-10%"          # um tico mais devagar que a narração: é segmentação
# ⚠️ O MOTIVO DE CADA FALHA FICA GUARDADO AQUI e vai para o `_silabas-log.txt`.
#    Antes o erro só era impresso, e "impresso" quer dizer "morreu no log da
#    execução". Sem o motivo, a sessão seguinte fica adivinhando.
MOTIVOS = []
FOLGA_MS = 60          # sobra no fim de cada corte, para não cortar o ar final
PAR = 4                # palavras ao mesmo tempo


def _diario(pasta, texto):
    u"""Deixa o RECADO no repo (`<pasta>/audio/_silabas-log.txt`).

    ⚠️ Existe porque esta ferramenta já falhou em silêncio: o passo do workflow
    tem `continue-on-error`, o aviso morre no log da execução e ninguém volta lá.
    O que o repo guarda, a próxima sessão lê."""
    try:
        d = os.path.join(pasta, "audio")
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(os.path.join(d, "_silabas-log.txt"), "w",
                encoding="utf-8").write(texto + u"\n")
    except Exception:                                            # noqa: BLE001
        pass


def _ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                                            # noqa: BLE001
        return "ffmpeg"


# ══════════════════════════════════════════════════════════════════════
#  ONDE ESTÃO OS CORTES — duas fontes, e a segunda é a que salva
#
#  ⚠️⚠️ MEDIDO EM 10/set/2026: o serviço da Microsoft **parou de mandar os
#     marcadores de tempo** (`WordBoundary`). Vieram ZERO marcas em todas as 17
#     palavras, inclusive nas de uma sílaba só. A ferramenta inteira dependia
#     deles, então não saía recorte nenhum — e como o passo era
#     `continue-on-error`, isso durou semanas em silêncio.
#
#     Depender de um campo opcional de um protocolo alheio foi o erro de
#     projeto. Agora há um caminho que não depende de ninguém: o texto que se
#     manda é `bo, la, ca.` — as VÍRGULAS produzem pausas de verdade no áudio —
#     e o corte sai medindo o SILÊNCIO com o próprio ffmpeg. Se as marcas
#     voltarem um dia, elas continuam sendo preferidas (são exatas); se não
#     voltarem, o silêncio resolve.
# ══════════════════════════════════════════════════════════════════════
def _duracao(ff, caminho):
    p = subprocess.Popen([ff, "-i", caminho, "-f", "null", "-"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = p.communicate()
    txt = (err or b"").decode("utf-8", "replace")
    achado = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", txt)
    if not achado:
        return 0.0
    h, m, s = achado[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def _cortes_por_silencio(ff, caminho, quantas):
    u"""Devolve [(inicio, duracao)] de cada trecho FALADO, ou [] se não deu.

    Tenta vários limiares porque voz e volume variam: começa exigente (silêncio
    bem definido) e vai afrouxando. Só aceita quando o número de trechos bate
    exatamente com o número de sílabas — trecho a mais ou a menos significa que
    a leitura saiu diferente do esperado, e aí é melhor não cortar do que cortar
    errado (sílaba cortada no lugar errado ensina errado igual)."""
    total = _duracao(ff, caminho)
    if total <= 0:
        return []
    for ruido, minimo in (("-35dB", 0.10), ("-40dB", 0.08), ("-30dB", 0.12),
                          ("-45dB", 0.06)):
        p = subprocess.Popen(
            [ff, "-i", caminho, "-af",
             "silencedetect=noise=%s:d=%.2f" % (ruido, minimo), "-f", "null", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = p.communicate()
        txt = (err or b"").decode("utf-8", "replace")
        inicios = [float(x) for x in re.findall(r"silence_start: (-?\d+\.?\d*)", txt)]
        fins = [float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", txt)]
        # monta os trechos FALADOS a partir dos vãos de silêncio
        trechos, cursor = [], 0.0
        for k, ini in enumerate(inicios):
            if ini > cursor + 0.04:
                trechos.append((cursor, ini - cursor))
            cursor = fins[k] if k < len(fins) else ini
        if total > cursor + 0.04:
            trechos.append((cursor, total - cursor))
        trechos = [t for t in trechos if t[1] >= 0.08]
        if len(trechos) == quantas:
            return trechos
    return []


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
                if len(dados) < 800:
                    raise RuntimeError("audio curto (%d bytes)" % len(dados))
                inteiro = destino_base + "_todo.mp3"
                open(inteiro, "wb").write(dados)
                ff = _ffmpeg()
                # 1º os marcadores do serviço (exatos, quando vêm);
                # 2º o silêncio entre as vírgulas (não depende de ninguém).
                if len(marcas) >= len(silabas):
                    cortes = [(marcas[i][0] / 10000000.0,
                               marcas[i][1] / 10000000.0 + FOLGA_MS / 1000.0)
                              for i in range(len(silabas))]
                else:
                    cortes = _cortes_por_silencio(ff, inteiro, len(silabas))
                    if not cortes:
                        try:
                            os.remove(inteiro)
                        except OSError:
                            pass
                        raise RuntimeError(
                            "sem marcas (%d) e o silencio nao separou em %d trecho(s)"
                            % (len(marcas), len(silabas)))
                    cortes = [(a, b + FOLGA_MS / 1000.0) for a, b in cortes]
                n = 0
                for i, s in enumerate(silabas):
                    ini, dur = cortes[i]
                    saida = os.path.join(os.path.dirname(destino_base),
                                         "%ssb_%s_%d.mp3" % (prefixo, palavra, i))
                    # ⚠️ ENTRADA PRIMEIRO, DEPOIS O `-ss`, E SEMPRE RECODIFICANDO.
                    #    O jeito antigo (`-ss` antes do `-i` com `-c copy`) é o
                    #    rápido, mas em mp3 ele corta no meio do quadro e às vezes
                    #    devolve arquivo quebrado — e como o corte não levantava
                    #    exceção nenhuma, a falha saía como "0 de 3 sílabas" SEM
                    #    motivo registrado. São pedaços de meio segundo: o custo
                    #    de recodificar é nada perto de um defeito invisível.
                    p = subprocess.Popen(
                        [ff, "-y", "-loglevel", "error", "-i", inteiro,
                         "-ss", "%.3f" % ini, "-t", "%.3f" % dur,
                         "-c:a", "libmp3lame", "-q:a", "5", saida],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    _, err = p.communicate()
                    if os.path.exists(saida) and os.path.getsize(saida) > 300:
                        n += 1
                    elif i == 0:
                        MOTIVOS.append(u"%s: ffmpeg nao cortou (%s) -- %s"
                                       % (palavra, ff,
                                          (err or b"").decode("utf-8", "replace")[:120]))
                try:
                    os.remove(inteiro)
                except OSError:
                    pass
                return n
            except Exception as e:                               # noqa: BLE001
                if tent == 3:
                    print(u"   ERRO em %s: %s" % (palavra, e))
                    MOTIVOS.append(u"%s: %s" % (palavra, e))
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
    _diario(pasta, u"%d palavra(s) gravadas, %d com falha (voz %s, rate %s)\n%s"
            % (len(alvos) - falhou, falhou, voz, RATE,
               u"\n".join(u"   " + m for m in MOTIVOS[:12]) or u"   (sem motivo registrado)"))
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
        _diario(pasta, u"FALHOU: sem o edge-tts neste ambiente")
        return 2
    # ⚠️⚠️ LIÇÃO PAGA (set/2026, o Marcos ouviu "vê-á" no lugar de "va"):
    #    aqui estava `asyncio.get_event_loop().run_until_complete(...)`. A partir
    #    do Python 3.12 chamar isso sem um laço em andamento é obsoleto e do 3.14
    #    em diante ESTOURA — e o passo do workflow tinha `continue-on-error`, de
    #    modo que a falha só deixava um aviso que ninguém lia. Resultado: NENHUM
    #    recorte foi gerado, nem aqui nem no `_alfa1`, e a criança ouviu a sílaba
    #    sintetizada solta (a fala de reserva), que é justamente o que este
    #    arquivo inteiro existe para não acontecer.
    #    `asyncio.run` é o mesmo que a narração do `entregar.yml` já usava.
    try:
        return asyncio.run(_tudo(pasta, mapa, voz, prefixo, "--refazer" in sys.argv))
    except Exception as e:                                       # noqa: BLE001
        print(u"nao consegui rodar: %s" % e)
        _diario(pasta, u"FALHOU: %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
