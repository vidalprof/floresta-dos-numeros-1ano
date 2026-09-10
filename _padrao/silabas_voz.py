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
O QUE ESTA FERRAMENTA FAZ (reescrita em 10/set/2026)

Grava a PALAVRA INTEIRA e corta as sílabas de dentro dela.

  1. manda ao Edge TTS o texto `cavalo.` — a palavra inteira, devagar. A voz
     pronuncia certo porque é palavra de verdade, e não um fragmento;
  2. o `ctc-forced-aligner` (modelo MMS, CPU) alinha o áudio com o texto em
     NÍVEL DE CARACTERE e devolve o tempo de cada letra;
  3. a fronteira da sílaba é o COMEÇO da primeira letra da sílaba seguinte;
  4. corta o mp3 nesses tempos com ffmpeg, um arquivo por sílaba.

Medido na prova de bancada (`_pesquisa/prova-silaba.txt`):

    CAVALO   c@0,22  a@0,32  v@0,52  a@0,64  l@0,78  o@0,86
             └── CA ─────────┘└── VA ───────┘└── LO ──────────

⚠️ O QUE ESTA FERRAMENTA FAZIA ANTES, E POR QUE ESTAVA ERRADO: ela mandava a
   voz ler `gi, ra, fa` (os pedaços separados por vírgula) e cortava nas pausas.
   Parece a mesma coisa e não é: a voz lê cada pedaço ISOLADO e, quando o pedaço
   não é palavra do português, ela SOLETRA — "va" vira "vê-á". O erro nascia
   dentro do áudio, e cortar depois só repartia o erro. O Marcos ouviu isso duas
   vezes antes de eu enxergar. Medida que denuncia: sílaba soletrada leva o
   DOBRO da duração (VA 0,66s contra LA 0,26s) — é o que o portão
   `_qa/silabas.py` mede hoje.

⚠️ Só o `start` de cada letra é usado. O `end` da última vem furado (estica até
   o fim do arquivo) e letras de confiança baixa saem fora de lugar — na prova,
   o 'o' de GATO apareceu a 1,86s. Usando só o começo, nada disso atrapalha; o
   fim da última sílaba vem do fim da FALA, medido por silêncio.

⚠️ O corte por silêncio continua no arquivo como REDE (se o alinhador não
   estiver instalado), mas não é mais o caminho — e o portão reprova o resultado
   dele quando sai soletrado.

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

RATE = "-25%"          # bem devagar: ajuda a criança E ajuda o alinhamento
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



# ══════════════════════════════════════════════════════════════════════
#  ⭐⭐ O CAMINHO CERTO: A PALAVRA INTEIRA + ALINHAMENTO FORÇADO
#
#  ⚠️ POR QUE MUDOU (10/set/2026 — o Marcos ouviu, duas vezes):
#     mandar a voz ler "bo, la, ca" e cortar NÃO conserta a pronúncia. Ela lê
#     cada pedaço ISOLADO e, quando o pedaço não é palavra do português, ela
#     SOLETRA: "va" vira "vê-á", "ga" vira "gê-á". O erro já nasce dentro do
#     áudio; cortar depois só reparte o erro em pedaços menores. Medido: as
#     sílabas soletradas saíam com o DOBRO da duração das outras
#     (VA 0,66s · GA 0,63s · FO 0,64s contra LA 0,26s · TA 0,28s).
#
#  ⭐ O QUE SE FAZ AGORA: a voz lê a PALAVRA INTEIRA — "cavalo" —, que ela
#     pronuncia perfeitamente porque é palavra de verdade; e o alinhamento
#     forçado (`ctc-forced-aligner`, modelo MMS, roda em CPU) diz o tempo de
#     CADA LETRA dentro dela. Medido na prova de bancada:
#
#         CAVALO   c@0,22  a@0,32  v@0,52  a@0,64  l@0,78  o@0,86
#                  └── CA ─────────┘└── VA ───────┘└── LO ──────────
#
#     A fronteira da sílaba é o COMEÇO DA PRIMEIRA LETRA DA SÍLABA SEGUINTE.
#     Só o `start` da primeira letra de cada sílaba é usado — e isso importa,
#     porque o `end` da última letra vem furado (estica até o fim do arquivo) e
#     letras de confiança baixa saem fora de lugar (o 'o' de GATO veio a 1,86s).
#     Usando só o começo, nada disso atrapalha.
#
#     Resultado: a criança ouve a sílaba com a pronúncia, a coarticulação e a
#     entonação REAIS da palavra — que é o que a alfabetização pede.
#
#  A queda para o corte por silêncio continua existindo, para o caso de o
#  alinhador não estar instalado. Mas ela é REDE, não caminho: o portão
#  `_qa/silabas.py` mede a soletração e reprova.
# ══════════════════════════════════════════════════════════════════════
_ALINHADOR = {}


def _carrega_alinhador():
    u"""Devolve (modelo, tokenizador) ou None. Carrega uma vez só."""
    if "m" in _ALINHADOR:
        return _ALINHADOR["m"]
    _ALINHADOR["m"] = None
    try:
        import torch
        from ctc_forced_aligner import load_alignment_model
        _ALINHADOR["m"] = load_alignment_model("cpu", dtype=torch.float32)
        print(u"   alinhador forcado: carregado (palavra inteira -> silaba)")
    except Exception as e:                                       # noqa: BLE001
        print(u"   alinhador forcado indisponivel (%s) — caindo para o silencio" % e)
    return _ALINHADOR["m"]


def _sem_acento(t):
    import unicodedata
    return u"".join(c for c in unicodedata.normalize("NFD", t)
                    if unicodedata.category(c) != "Mn")


def _fim_da_fala(ff, caminho, total):
    u"""Onde a voz PARA de falar (o resto do arquivo é silêncio).

    ⚠️ Necessário porque a última sílaba vai até o fim da fala, e o `end` que o
    alinhador dá para a última letra estica até o fim do ARQUIVO — foi assim que
    o 'o' de CAVALO apareceu com 2,08s num áudio de 1,x s."""
    p = subprocess.Popen(
        [ff, "-i", caminho, "-af", "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = p.communicate()
    txt = (err or b"").decode("utf-8", "replace")
    inicios = [float(x) for x in re.findall(r"silence_start: (-?\d+\.?\d*)", txt)]
    fins = [float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", txt)]
    # o último silêncio que vai até o fim do arquivo marca o fim da fala
    for ini in reversed(inicios):
        if not [f for f in fins if f > ini]:
            return ini
    return total


def _cortes_por_alinhamento(ff, mp3, palavra, silabas):
    u"""[(inicio, duracao)] por sílaba, a partir da PALAVRA INTEIRA falada."""
    mt = _carrega_alinhador()
    if not mt:
        return []
    modelo, tok = mt
    wav = mp3[:-4] + ".wav"
    subprocess.call([ff, "-y", "-loglevel", "error", "-i", mp3,
                     "-ar", "16000", "-ac", "1", wav])
    try:
        from ctc_forced_aligner import (load_audio, generate_emissions,
                                        preprocess_text, get_alignments,
                                        get_spans, postprocess_results)
        onda = load_audio(wav, modelo.dtype, modelo.device)
        em, stride = generate_emissions(modelo, onda, batch_size=1)
        # ⚠️ A PALAVRA ESCRITA, não a chave da figura: a chave é `pao`/`maca`
        #    (sem acento, para virar nome de arquivo), e alinhar por ela erraria
        #    a contagem de letras. A escrita se remonta das sílabas do PAL.
        escrito = u"".join(silabas).lower()
        tks, txts = preprocess_text(escrito, romanize=True, language="por",
                                    split_size="char")
        seg, sc, branco = get_alignments(em, tks, tok)
        res = postprocess_results(txts, get_spans(tks, seg, branco), stride, sc)
    except Exception as e:                                       # noqa: BLE001
        MOTIVOS.append(u"%s: alinhamento falhou (%s)" % (palavra, e))
        return []
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass

    letras = [r for r in res if (r.get("text") or u"").strip()]
    escrita = _sem_acento(u"".join(silabas)).lower()
    # ⚠️ o alinhador devolve o texto ROMANIZADO (ç->c, ã->a). Se por algum motivo
    #    o número de letras não bater com a palavra, não dá para mapear sílaba —
    #    e mapear errado é pior que não cortar.
    if len(letras) != len(escrita):
        MOTIVOS.append(u"%s: %d letra(s) alinhada(s) para %d escrita(s)"
                       % (palavra, len(letras), len(escrita)))
        return []

    total = _duracao(ff, mp3)
    fim = _fim_da_fala(ff, mp3, total)
    inicios, k = [], 0
    for s in silabas:
        inicios.append(float(letras[k]["start"]))
        k += len(_sem_acento(s))
    cortes = []
    for i, ini in enumerate(inicios):
        prox = inicios[i + 1] if i + 1 < len(inicios) else fim
        dur = prox - ini
        if dur <= 0.05:
            MOTIVOS.append(u"%s: silaba %d saiu com %.2fs" % (palavra, i, dur))
            return []
        cortes.append((max(0.0, ini - 0.02), dur + 0.04))
    return cortes


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
                # ⭐ 1º o ALINHAMENTO na palavra inteira (o caminho certo);
                #    2º o silêncio, só como rede se o alinhador não estiver lá.
                cortes = _cortes_por_alinhamento(ff, inteiro, palavra, silabas)
                if not cortes:
                    cortes = _cortes_por_silencio(ff, inteiro, len(silabas))
                    cortes = [(a, b + FOLGA_MS / 1000.0) for a, b in cortes]
                if not cortes:
                    try:
                        os.remove(inteiro)
                    except OSError:
                        pass
                    raise RuntimeError("nao consegui achar as fronteiras de %d silaba(s)"
                                       % len(silabas))
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
        # ⭐⭐ A PALAVRA INTEIRA, e não mais "bo, la, ca".
        #    Esta linha É o conserto: a voz pronuncia bem porque "cavalo" é
        #    palavra de verdade. Quem separa as sílabas depois é o alinhamento.
        texto = u"".join(sil).lower() + u"."
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
