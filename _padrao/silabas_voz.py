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


# ⚠️⚠️ O NOME DO ARQUIVO É SEM ACENTO — e a PALAVRA continua com ele.
#    As duas coisas são diferentes e as duas importam: a voz só pronuncia
#    "sabão" direito se receber o til, mas `audio/gv_sb_sabão_0.mp3` viaja por
#    git, por zip, por servidor de Pages e por navegador, e em cada uma dessas
#    pontes o acento tem um jeito diferente de ser escrito (NFC e NFD são bytes
#    distintos para a MESMA letra). Nenhum dos nove cadernos que já cortam
#    sílaba tem palavra acentuada — o `_sil2` é o primeiro, com SABÃO, SOFÁ,
#    CAÇA, PÃO, PÉ e MÃO. Em vez de descobrir a ponte quebrada com a criança na
#    frente, o acento sai do NOME e fica só no TEXTO.
#    ⚠️ Quem lê este nome são TRÊS: esta ferramenta, o portão `_qa/silabas.py` e
#       o `falarSilaba` do app. Mudar aqui sem mudar os outros dois emudece tudo.
def arquivo_da_palavra(palavra):
    import re
    return re.sub(r"[^a-z0-9]", "", _sem_acento(palavra.lower()))


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


def _inicio_da_fala(ff, caminho):
    u"""Onde a voz COMECA (o fim do silencio inicial), ou None.

    ⭐ (18/set/2026) A primeira silaba comecava em `letras[0].start - 20 ms`, e
    o alinhador marca a letra DEPOIS de o som ja ter comecado: 144 das 368
    primeiras silabas comecavam dentro do som (vogal, nasal, fricativa). O
    inicio certo e o fim do silencio que abre o arquivo — espelho do
    `_fim_da_fala`. Medido nas tres palavras do exemplo: cai 15 a 51 ms antes
    do onset, sem comer nada (o fim da 1a silaba nao muda)."""
    p = subprocess.Popen(
        [ff, "-i", caminho, "-af", "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = p.communicate()
    txt = (err or b"").decode("utf-8", "replace")
    pares = re.findall(r"silence_start: (-?\d+\.?\d*)\s*\n.*?silence_end: (\d+\.?\d*)", txt, re.S)
    for ini, fim in pares:
        if float(ini) <= 0.02:
            return float(fim)
    return None


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
    # ⭐ a PRIMEIRA silaba comeca onde a fala comeca, nao onde o alinhador
    #   marcou a primeira letra (ver `_inicio_da_fala`). Se nao houver silencio
    #   abrindo o arquivo (nao aconteceu em 371/371), fica como era.
    comeco = _inicio_da_fala(ff, mp3)
    if comeco is not None and comeco < inicios[0]:
        inicios[0] = comeco + 0.02        # a folga de 20 ms e descontada abaixo
    cortes = []
    for i, ini in enumerate(inicios):
        prox = inicios[i + 1] if i + 1 < len(inicios) else fim
        dur = prox - ini
        if dur <= 0.05:
            MOTIVOS.append(u"%s: silaba %d saiu com %.2fs" % (palavra, i, dur))
            return []
        cortes.append((max(0.0, ini - 0.02), dur + 0.04))
    return cortes



# ══════════════════════════════════════════════════════════════════════
#  ⭐⭐⭐ A VOZ SE CONFERE SOZINHA — o Marcos nao pode ser o portao
#
#  ORDEM DELE (17/set/2026): *"eu preciso de uma ferramenta ou metodo que deixe
#  tudo isso correto SEM EU TER QUE PRECISAR OUVIR"*. Ele esta certo: ate hoje
#  quem descobria que a silaba saiu errada era ele, na sala, com a crianca na
#  frente. Isso nao e portao, e sorte.
#
#  ⚠️⚠️⚠️ A PRIMEIRA VERSAO DESTE BLOCO (17/set/2026, de manha) ESTAVA ERRADA,
#     e o erro custou uma entrega inteira. Fica escrito porque a armadilha e
#     bonita e eu cairia nela de novo.
#
#     Eu medi cinco jeitos de PEDIR a voz e contei os PEDACOS FALADOS na
#     gravacao:
#
#         corrida   "escola"           1 bloco   <- "reprovado"
#         espaco    "es co la"         3 pedacos <- "aprovado"
#
#     e conclui que a fala corrida estava errada. **Estava certa.** Numa
#     palavra falada de verdade as silabas sao COARTICULADAS: nao ha silencio
#     entre elas, e por isso ela e um bloco so. Isso nao e defeito, e o
#     portugues. Quem separa nao e o silencio: e o ALINHAMENTO FORCADO.
#
#     Contar pedacos na GRAVACAO respondia a pergunta errada, e o preco foi
#     exato: o caminho `espaco` venceu em 205 das 326 palavras, a voz leu cada
#     pedaco ISOLADO, e pedaco isolado que nao e palavra do portugues ela
#     SOLETRA — "va" virou "ve-a", com 1,22 s no lugar de 0,32 s. O portao
#     `_qa/silabas.py` mediu a duracao, reprovou os OITO cadernos e segurou a
#     publicacao. O portao velho salvou a crianca do meu metodo novo.
#
#  ⭐ O QUE VALE AGORA, E A PERGUNTA E OUTRA:
#
#     1. a FONTE volta a ser a PALAVRA INTEIRA (`corrida`), que a voz nunca
#        soletra porque e palavra de verdade — e o corte e do alinhador;
#     2. a conferencia sai de cima da GRAVACAO e vai para cima dos RECORTES
#        PRONTOS, que e onde o defeito aparece: **toda silaba do portugues tem
#        exatamente UMA vogal**. Recorte com DOIS nucleos e a voz soletrando
#        ("ve-a" sao duas emissoes); com ZERO, e corte que perdeu a vogal.
#        A invariante e da LINGUA, nao minha — e e a mesma que o portao 1x
#        (`_qa/silaba_audio.py`) usa, medida em 882 recortes.
#
#     Os outros caminhos (espaco, pausa, virgula) ficam como ULTIMO RECURSO,
#     so para a palavra em que o alinhamento nao fecha. E o recorte que sair
#     deles tambem tem de passar na prova dos nucleos.
#
#  ⚠️ Sem `librosa` nao ha conferencia: nesse caso fica a PALAVRA INTEIRA (a
#     fonte segura) e o codigo DIZ que nao conferiu. Nao medir nunca e "passou".
#
#  ⚠️⚠️ TERCEIRA CORRECAO (18/set/2026, medida pela banca nos 52 soletrados):
#     a prova "uma vogal por recorte" NAO enxerga soletracao — 46 dos 52
#     soletrados tem exatamente UM nucleo (a voz diz "ve" longo, nao "ve-a").
#     Quem separa e a DURACAO: teto absoluto por tamanho (TETO_ABS) pega 33/52
#     e nao acusa nenhum dos 882 bons. E os caminhos apartados abaixo NAO
#     entregam mais nada: em 17/set eles assinaram 358 soletradas como
#     "conferidas". So `corrida` grava; os outros ficam como registro do que
#     foi medido e por que nao servem.
# ══════════════════════════════════════════════════════════════════════
CAMINHOS_DE_PEDIR = [
    (u"corrida", lambda sil: u"".join(sil).lower() + u"."),
    (u"pausa", lambda sil: u" ... ".join(sil).lower()),
    (u"virgula", lambda sil: u", ".join(sil).lower() + u"."),
    (u"espaco", lambda sil: u" ".join(sil).lower()),
]
CONFERIDAS = []          # (palavra, caminho que passou, recortes conferidos)
NAO_CONFERIDAS = []      # (palavra, motivo)
INFO_RECORTE = {}        # caminho do mp3 -> {ini, dur, ganho_db, preso}
# ⭐ O METODO ENTRA NA ASSINATURA DO CARIMBO (18/set/2026). Antes, toda mudanca
#    de codigo exigia apagar `audio/_silabas.json` a mao para regravar
#    (0789ecdb, 72af08be, 198acce4 — tres vezes em um dia). Agora o codigo que
#    corta diz quem e; mudou o metodo, o carimbo nao bate e a palavra regrava.
METODO = u"v5-citacao-virgula-ou-palavra"
# ⚠️ MESMOS TETOS de `_qa/silabas.py` (TETO_S) — a gravacao e o portao tem de
#    concordar. Aferidos em 18/set/2026: bom mais longo 0,30/0,42/0,48 s;
#    soletrado mais curto 0,64/0,32/0,39 s por 1/2/3 letras.
TETO_ABS = {1: 0.40, 2: 0.55, 3: 0.60}
ALVO_LK = -18.0          # LUFS-like (LKvoz, BS.1770 sem gate) para o pedaco
TETO_TP = -1.5           # dBTP: o mp3 ainda pode dar sobressalto acima disto
MIN_NUCLEO_MS = 50       # abaixo disso e transiente (o estalo da oclusiva)
MARGEM_DB = 6.0          # a consoante sonora (l, r, m, n) faz pico, mas FRACO


def conta_nucleos(caminho_mp3):
    u"""Quantas VOGAIS ha no recorte. None se nao der para medir.

    ⚠️ Copia fiel da medida do portao 1x (`_qa/silaba_audio.py`): os dois tem
    de concordar, senao a gravacao aprova o que a banca reprova. Mudou aqui,
    muda la — e remede os 882 recortes."""
    try:
        import numpy as np
        import librosa
    except ImportError:
        return None
    try:
        y, _ = librosa.load(caminho_mp3, sr=16000, mono=True)
    except Exception:                                            # noqa: BLE001
        return None
    if len(y) < 320:
        return 0
    S = np.abs(librosa.stft(y, n_fft=512, hop_length=80))
    fr = librosa.fft_frequencies(sr=16000, n_fft=512)
    e = S[(fr >= 250) & (fr <= 3000)].sum(axis=0)
    if e.max() <= 0:
        return 0
    db = 20 * np.log10(e / e.max() + 1e-9)
    if len(db) >= 5:
        db = np.convolve(db, np.ones(5) / 5.0, mode=u"same")
    acima = db > -12.0
    bl, i = [], 0
    while i < len(acima):
        if acima[i]:
            j = i
            while j < len(acima) and acima[j]:
                j += 1
            bl.append((i, j))
            i = j
        else:
            i += 1
    bl = [(a, b) for a, b in bl if (b - a) * 5.0 >= MIN_NUCLEO_MS]
    if not bl:
        return 0
    f = [bl[0]]
    for a, b in bl[1:]:
        pa, pb = f[-1]
        entre = db[pb:a]
        if len(entre) == 0 or (min(db[pa:pb].max(), db[a:b].max()) - entre.min()) < 6.0:
            f[-1] = (pa, b)
        else:
            f.append((a, b))
    topo = max(db[a:b].max() for a, b in f)
    return len([1 for a, b in f if db[a:b].max() >= topo - MARGEM_DB])


# ⚠️ ENTRADA PRIMEIRO, DEPOIS O `-ss`, E SEMPRE RECODIFICANDO.
#    O jeito antigo (`-ss` antes do `-i` com `-c copy`) é o rápido, mas em mp3
#    ele corta no meio do quadro e às vezes devolve arquivo quebrado — e como o
#    corte não levantava exceção nenhuma, a falha saía como "0 de 3 sílabas" SEM
#    motivo registrado. São pedaços de meio segundo: o custo de recodificar é
#    nada perto de um defeito invisível.
# ⚠️⚠️ APARAR O SILÊNCIO DO FIM DE CADA PEDAÇO. Sem isto a ÚLTIMA sílaba de cada
#    palavra levava junto o rabo de silêncio do arquivo e saía com 1,4 s —
#    medido em todas as 17 palavras na primeira rodada do alinhamento. O truque
#    é o de sempre: inverte, tira o silêncio do começo (que era o do fim),
#    desinverte. Não faz nada quando não há silêncio, então serve para todos os
#    pedaços e não só para o último.
# ⭐⭐ E IGUALAR A FORCA DE CADA PEDACO (17/set/2026). O DEFEITO, medido em 882
#    recortes de oito cadernos: 35 saiam QUASE MUDOS -- pico de energia abaixo de
#    um quarto dos vizinhos --, e quase todos eram a SILABA FINAL da palavra: o
#    PO de SAPO (0,022 contra 0,180 de mediana), o TO de GATO, o CO de MACACO, o
#    VO de BRAVO. A razao e da lingua, nao do corte: no portugues do Brasil a
#    silaba final atona e dita quase sem voz -- "sapo" sai [ˈsapʊ]. Dentro da
#    palavra ninguem nota; recortada e tocada SOZINHA, a crianca toca no PO e
#    praticamente nao ouve nada. Numa folha de alfabetizacao isso e grave: ela
#    escolhe pelo desenho. `loudnorm` poe todos os pedacos na mesma altura
#    percebida (EBU R128). Medido antes de entrar: o ganho necessario chega a
#    7,7x e o pico DEPOIS fica em 0,54 de 1,0 -- nao estoura em nenhum dos 882.
#    ⚠️ Isto muda o pedaco TOCADO SOZINHO, nunca a gravacao da palavra inteira,
#       que continua com a prosodia natural.
#
# ⚠️⚠️⚠️ E SAO DOIS PASSOS, NAO UM — licao paga em 17/set/2026, e eu tinha
#    ANUNCIADO o conserto sem ter medido o resultado.
#    Na primeira versao o `loudnorm` vinha no MESMO comando do corte, junto com
#    o `-ss`. Com o `-ss` DEPOIS do `-i`, o ffmpeg manda a PALAVRA INTEIRA pelo
#    filtro e so descarta o que esta fora da janela no fim — ou seja, o
#    `loudnorm` media e normalizava a PALAVRA, e a silaba final continuava tao
#    fraca quanto era. Medido, com uma "palavra" montada de proposito (SA forte
#    + PO quase mudo):
#
#        pecas soltas                         SA 0,2762   PO 0,0304
#        um passo so (-ss depois do -i)       PO -> 0,0308   <- nao fez NADA
#        -ss antes do -i                      PO -> 0,3013
#        DOIS PASSOS (corta, depois normaliza) PO -> 0,2932
#
#    Por isso o portao 1x ainda achava CEM recortes quase mudos DEPOIS do
#    "conserto": ele nunca tinha acontecido. Agora o corte sai num comando e a
#    normalizacao vem num segundo, sobre o pedaco JA SOZINHO — que e a unica
#    forma de o alvo da medida ser o pedaco.
FILTRO_CORTE = ("areverse,silenceremove=start_periods=1:"
                "start_silence=0.03:start_threshold=-42dB,areverse")
# ⚠️⚠️ O `loudnorm` SAIU DO 2o PASSO (18/set/2026) — e o motivo e medido: em
#    pedaco de menos de 400 ms (a janela de integracao dele), o loudnorm vira
#    um normalizador de PICO. Nos 882 recortes no ar: 9,8 dB de diferenca de
#    forca entre PA de capa e LI de galinha, ate 8,3 dB DENTRO da mesma palavra
#    — e a medida 1 do portao 1x (RMS maximo em 20 ms) e quase pico tambem, por
#    isso as duas diziam "esta igual". O comentario acima ("todos na mesma altura
#    percebida") foi escrito com regua de pico. Agora o ganho e CALCULADO no
#    pedaco (LKvoz: BS.1770 sem gate, so nas janelas com voz — `_qa/kvoz.py`) e
#    aplicado com `volume`, com teto de pico real; o loudnorm fica so como rede
#    se o `kvoz` nao carregar (e isso vai para o recibo).
FILTRO_FORCA = "loudnorm=I=-16:TP=-1.5:LRA=11"
# ⭐ FADE DE 10 ms NAS DUAS PONTAS (18/set/2026). O corte cai DENTRO da fala e o
#    audio comeca "no cheio": 659 dos 882 recortes tinham amplitude alta nos
#    primeiros ou ultimos 0,5 ms (onset natural do TTS: 0 de 12). Medido: 5 ms
#    deixa 11% dos estalos; 10 ms zera; 15 ms ja come o estouro do /b/ e do /d/
#    (p10 = 11-14 ms). Vai no 2o comando, sobre o pedaco ja sozinho — no 1o
#    (com -ss de saida) o filtro veria a palavra inteira e nao faria nada.
FADE = "afade=t=in:st=0:d=0.010,areverse,afade=t=in:st=0:d=0.010,areverse"


def _ganho_do_pedaco(cru):
    u"""(ganho_dB, preso_no_teto) medidos no pedaco cortado; (None, False) sem kvoz."""
    try:
        import sys as _s
        _s.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "_qa"))
        from kvoz import ganho_para
        import librosa
        import numpy as np
        y, sr = librosa.load(cru, sr=None, mono=True)
        # ⚠️ MEDIR O PICO DEPOIS DO FADE, nao antes (18/set/2026, provado nas 3
        #    palavras do exemplo): o pico do pedaco cru costuma ser o proprio
        #    ESTALO da borda, que o fade de 10 ms elimina. Medindo antes, o LO de
        #    CAVALO ficou "preso no teto" 2,6 dB abaixo do alvo sem precisar. O
        #    ganho e aplicado antes do fade no ffmpeg; a ordem nao muda o pico
        #    final, entao aqui a rampa entra so para medir o que vai sobrar.
        n = min(len(y) // 2, int(sr * 0.010))
        if n > 0:
            rampa = np.linspace(0.0, 1.0, n)
            y = y.copy()
            y[:n] *= rampa
            y[-n:] *= rampa[::-1]
        g, preso = ganho_para(y, sr, ALVO_LK, TETO_TP)
        return g, preso
    except Exception as e:                                       # noqa: BLE001
        MOTIVOS.append(u"sem kvoz/librosa para medir o ganho (%s) — caiu no loudnorm" % e)
        return None, False


def _recorta(ff, inteiro, silabas, pasta_audio, prefixo, palavra, corrida):
    u"""Corta o mp3 da gravação em um arquivo por sílaba. Devolve a lista deles.

    A ORDEM das duas fontes de fronteira depende de COMO a palavra foi pedida,
    e isso não é detalhe: na fala CORRIDA não existe silêncio entre as sílabas
    (elas são coarticuladas), então quem separa é o ALINHAMENTO; nos caminhos
    de último recurso, que pedem os pedaços apartados, o silêncio é justamente
    a fronteira de verdade. Cada uma serve de rede para a outra."""
    if corrida:
        cortes = _cortes_por_alinhamento(ff, inteiro, u"".join(silabas), silabas)
        if not cortes:
            cortes = [(a, b + FOLGA_MS / 1000.0)
                      for a, b in _cortes_por_silencio(ff, inteiro, len(silabas))]
    else:
        cortes = [(a, b + FOLGA_MS / 1000.0)
                  for a, b in _cortes_por_silencio(ff, inteiro, len(silabas))]
        if not cortes:
            cortes = _cortes_por_alinhamento(ff, inteiro, u"".join(silabas), silabas)
    if not cortes:
        return []
    feitos = []
    for i, _s in enumerate(silabas):
        ini, dur = cortes[i]
        saida = os.path.join(pasta_audio, "%ssb_%s_%d.mp3"
                             % (prefixo, arquivo_da_palavra(palavra), i))
        cru = saida[:-4] + "_cru.mp3"
        p = subprocess.Popen(
            [ff, "-y", "-loglevel", "error", "-i", inteiro,
             "-ss", "%.3f" % ini, "-t", "%.3f" % dur,
             "-af", FILTRO_CORTE,
             "-c:a", "libmp3lame", "-q:a", "5", cru],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = p.communicate()
        if os.path.exists(cru) and os.path.getsize(cru) > 300:
            # ⭐ 2º PASSO, sobre o pedaco JA SOZINHO (no 1o comando, com -ss de
            #   saida, o filtro veria a palavra inteira): ganho MEDIDO + fade.
            g, preso = _ganho_do_pedaco(cru)
            if g is None:
                forca = FILTRO_FORCA                 # rede: o loudnorm antigo
            else:
                forca = "volume=%.2fdB" % g
            INFO_RECORTE[saida] = {u"ini": round(ini, 3), u"dur": round(dur, 3),
                                   u"ganho_db": None if g is None else round(g, 2),
                                   u"preso_no_teto": bool(preso)}
            q = subprocess.Popen(
                [ff, "-y", "-loglevel", "error", "-i", cru,
                 "-af", forca + "," + FADE, "-c:a", "libmp3lame", "-q:a", "5", saida],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, err2 = q.communicate()
            if not (os.path.exists(saida) and os.path.getsize(saida) > 300):
                os.rename(cru, saida)          # sem a forca, mas com o corte
                MOTIVOS.append(u"%s: nao consegui igualar a forca da silaba %d"
                               % (palavra, i))
            else:
                try:
                    os.remove(cru)
                except OSError:
                    pass
        if os.path.exists(saida) and os.path.getsize(saida) > 300:
            feitos.append(saida)
        elif i == 0:
            MOTIVOS.append(u"%s: ffmpeg nao cortou (%s) -- %s"
                           % (palavra, ff,
                              (err or b"").decode("utf-8", "replace")[:120]))
    return feitos


async def _grava(edge_tts, pedido, voz, inteiro):
    com = edge_tts.Communicate(pedido, voz, rate=RATE)
    audio = io.BytesIO()
    async for pedaco in com.stream():
        if pedaco["type"] == "audio":
            audio.write(pedaco["data"])
    dados = audio.getvalue()
    if len(dados) < 800:
        return False
    open(inteiro, "wb").write(dados)
    return True


# ══════════════════════════════════════════════════════════════════════
#  ⭐⭐ A FORMA DE CITACAO — "como a professora separa na lousa"
#
#  DECISAO DO MARCOS (18/set/2026), a pergunta era dele e a resposta foi dele:
#  a silaba tocada sozinha deve soar como a professora a diz AO SEPARAR ("SA —
#  PO": mais longa, vogal cheia), nao como sai reduzida dentro da palavra.
#
#  MEDIDO no experimento `_pesquisa/citacao_prova.py` (206 palavras, no runner):
#    · pedir a palavra APARTADA por virgula ("sa, po.") separa certo em 204/206;
#      por espaco ou hifen so em ~48 (a voz emenda as pecas);
#    · a peca apartada E a forma de citacao: silaba final 0,29 s contra 0,21 s
#      na palavra, F1 mais alto (vogal mais aberta);
#    · MAS a voz SOLETRA 37 das 474 pecas (8%) — as que nao sao palavra do
#      portugues: GA, VA, VE, FO, FE, RO, ES, CRA, CRE, GRA, XE sempre; BA, NE,
#      CE as vezes. Soletrada, a peca dobra de tamanho (GRA 1,06 s; VA 0,75 s)
#      e o TETO ABSOLUTO por tamanho pega TODAS as 37. (O reconhecedor de fala
#      le "gi e ria" para GRA e "via" para VA — confirma o que sao, mas nao
#      serve de regua: le "para" em PA de citacao.)
#
#  ENTAO O METODO E HIBRIDO, e cada silaba diz no recibo qual forma recebeu:
#    1. grava a PALAVRA INTEIRA (corrida) — nunca soletra: da a fronteira pelo
#       alinhador e e o RESERVA de toda silaba;
#    2. grava a mesma palavra APARTADA por virgula e corta pelo silencio (tem
#       de dar exatamente N pecas);
#    3. para cada silaba, a peca apartada SUBSTITUI a da palavra se passar:
#       duracao ate o teto por tamanho, UM nucleo de vogal, e ter caido na
#       ordem certa; senao fica a da palavra inteira ("forma: palavra").
#  Nada e inventado: as duas fontes sao a voz lendo texto. O que muda e qual
#  das duas leituras a crianca ouve — e o recibo conta quantas de cada.
# ══════════════════════════════════════════════════════════════════════
def _troca_por_citacao(ff, apart, silabas, feitos, pasta_audio, prefixo, palavra):
    u"""Substitui, silaba a silaba, o recorte da palavra pela peca apartada que
    passar nas reguas. Devolve a lista de formas ('citacao' | 'palavra')."""
    formas = [u"palavra"] * len(silabas)
    cortes = _cortes_por_silencio(ff, apart, len(silabas))
    if len(cortes) != len(silabas):
        MOTIVOS.append(u"%s: apartada deu %d peca(s) para %d silaba(s) — ficou a palavra"
                       % (palavra, len(cortes), len(silabas)))
        return formas
    for i, s in enumerate(silabas):
        ini, dur = cortes[i]
        tmp = os.path.join(pasta_audio, u"_cit_%s_%d.mp3" % (arquivo_da_palavra(palavra), i))
        cru = tmp[:-4] + u"_cru.mp3"
        p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-i", apart,
                              "-ss", "%.3f" % max(0.0, ini - 0.02), "-t", "%.3f" % (dur + 0.04),
                              "-af", FILTRO_CORTE, "-c:a", "libmp3lame", "-q:a", "5", cru],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        if not (os.path.exists(cru) and os.path.getsize(cru) > 300):
            continue
        g, preso = _ganho_do_pedaco(cru)
        forca = FILTRO_FORCA if g is None else "volume=%.2fdB" % g
        q = subprocess.Popen([ff, "-y", "-loglevel", "error", "-i", cru,
                              "-af", forca + "," + FADE, "-c:a", "libmp3lame", "-q:a", "5", tmp],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        q.communicate()
        try:
            os.remove(cru)
        except OSError:
            pass
        if not (os.path.exists(tmp) and os.path.getsize(tmp) > 300):
            continue
        d = _duracao(ff, tmp)
        n = conta_nucleos(tmp)
        L = len(s)
        teto = TETO_ABS.get(L)
        motivo = None
        if teto is None:
            motivo = u"sem teto aferido para %d letras" % L
        elif d > teto:
            motivo = u"%.2fs passa do teto %.2fs (soletrada)" % (d, teto)
        elif n is not None and n != 1:
            motivo = u"%d nucleo(s) de vogal" % n
        if motivo:
            MOTIVOS.append(u"%s: %s apartada recusada (%s) — ficou a palavra" % (palavra, s, motivo))
            try:
                os.remove(tmp)
            except OSError:
                pass
            continue
        os.replace(tmp, feitos[i])
        info = INFO_RECORTE.get(feitos[i], {})
        info.update({u"ini_apartada": round(ini, 3), u"dur": round(d, 3),
                     u"ganho_db": None if g is None else round(g, 2), u"preso_no_teto": bool(preso)})
        INFO_RECORTE[feitos[i]] = info
        formas[i] = u"citacao"
    return formas


async def _uma(sem, edge_tts, texto, voz, destino_base, silabas, prefixo, palavra,
               varias_vogais=False):
    u"""Grava a PALAVRA INTEIRA, corta as silabas e CONFERE os recortes.

    ⭐⭐ SO A PALAVRA INTEIRA ENTREGA (18/set/2026). Os caminhos apartados
    (`pausa`, `virgula`, `espaco`) sairam do caminho de entrega: em 17/set eles
    assinaram como "conferidas" 358 palavras SOLETRADAS, porque a trava que os
    segurava (`+25%% sobre base_dur`) nunca rodava quando a corrida falhava
    (base_dur ficava vazio) — e a prova dos nucleos ve UM nucleo em 46 dos 52
    soletrados. Palavra em que a corrida nao fecha vai para NAO_CONFERIDAS,
    NAO recebe carimbo, e o portao 1y para a entrega. E o comportamento certo
    pela regra da casa: audio que ninguem conferiu nao vai para a crianca.

    O QUE SE CONFERE, por recorte, e com que faro (aferido nos 52 soletrados
    guardados e nos 882 bons):
      · numero de recortes == numero de silabas          (senao, recusa)
      · TETO ABSOLUTO de duracao por tamanho (TETO_ABS)   pega 33/52, 0 falsos
      · ZERO nucleo de vogal = perdeu a voz               (recusa)
      · DOIS+ nucleos                                     AVISO, nao recusa:
        pega so 6/52 soletrados e confunde a consoante liquida (LU, BRI) com
        vogal — ficou porque e informacao, nao porque decide.
    A regua relativa (1,7x a mediana do caderno) fica no portao `_qa/silabas.py`,
    que ve o caderno inteiro; aqui, palavra por palavra, ela nao tem base.
    """
    async with sem:
        for tent in (1, 2, 3):
            try:
                inteiro = destino_base + "_todo.mp3"
                pasta_audio = os.path.dirname(destino_base)
                ff = _ffmpeg()
                nome_cam, monta = CAMINHOS_DE_PEDIR[0]         # corrida, e so
                if not await _grava(edge_tts, monta(silabas), voz, inteiro):
                    raise RuntimeError("a voz nao devolveu audio")
                feitos = _recorta(ff, inteiro, silabas, pasta_audio, prefixo, palavra, True)
                try:
                    os.remove(inteiro)
                except OSError:
                    pass
                motivo = None
                if len(feitos) != len(silabas):
                    motivo = (u"a palavra inteira deu %d recorte(s) para %d silaba(s) "
                              u"(o alinhador nao fechou)" % (len(feitos), len(silabas)))
                detalhes = []
                if motivo is None and not varias_vogais:
                    durs = [_duracao(ff, f) for f in feitos]
                    nn = [conta_nucleos(f) for f in feitos]
                    ruins, avisos = [], []
                    for i, (sil, d, n) in enumerate(zip(silabas, durs, nn)):
                        L = len(sil)
                        info = dict(INFO_RECORTE.get(feitos[i], {}))
                        info.update({u"i": i, u"silaba": sil, u"dur_s": round(d, 3),
                                     u"nucleos": n})
                        detalhes.append(info)
                        if L in TETO_ABS and d > TETO_ABS[L]:
                            ruins.append(u"%s %.2fs passa do teto %.2fs (soletrada?)"
                                         % (sil, d, TETO_ABS[L]))
                        if n == 0:
                            ruins.append(u"%s sem nucleo de vogal" % sil)
                        elif n is not None and n >= 2:
                            avisos.append(u"%s com %d picos (liquida ou vizinha)" % (sil, n))
                    if any(n is None for n in nn):
                        motivo = u"sem librosa: NAO CONFERI"
                    elif ruins:
                        motivo = u"; ".join(ruins)
                    if avisos:
                        for a in avisos:
                            MOTIVOS.append(u"%s: aviso — %s" % (palavra, a))
                elif motivo is None:
                    for i, sil in enumerate(silabas):
                        info = dict(INFO_RECORTE.get(feitos[i], {}))
                        info.update({u"i": i, u"silaba": sil})
                        detalhes.append(info)
                if motivo is None:
                    # ⭐ A FORMA DE CITACAO (ver o bloco acima): so para palavra
                    #   que a corrida ja conferiu, e nunca para PEDACO de exercicio.
                    formas = [u"palavra"] * len(silabas)
                    if not varias_vogais:
                        apart = destino_base + "_apart.mp3"
                        if await _grava(edge_tts, u", ".join(silabas).lower() + u".", voz, apart):
                            formas = _troca_por_citacao(ff, apart, silabas, feitos,
                                                        pasta_audio, prefixo, palavra)
                            try:
                                os.remove(apart)
                            except OSError:
                                pass
                        for i, dtl in enumerate(detalhes):
                            dtl[u"forma"] = formas[i]
                            info = INFO_RECORTE.get(feitos[i], {})
                            if formas[i] == u"citacao":
                                dtl.update({k: info.get(k) for k in (u"dur", u"ganho_db", u"preso_no_teto")})
                                dtl[u"dur_s"] = info.get(u"dur")
                    CONFERIDAS.append((palavra, nome_cam + (u" (pedaco)" if varias_vogais else u""),
                                       len(feitos), detalhes))
                    return len(feitos)
                # ⚠️ NAO CONFERIDA: os arquivos ficam (para alguem OUVIR e decidir),
                #    mas a palavra NAO e carimbada (devolve 0) e o recibo diz por que.
                NAO_CONFERIDAS.append((palavra, motivo))
                return 0
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
    # ⚠️ PEDAÇO de exercício (CENOU+RA, CA+MA) tem mais de uma vogal de
    #    propósito: a prova dos núcleos não se aplica a ele. Mesma lista que o
    #    portão 1x (`_qa/silaba_audio.py`) lê.
    pedacos = {}
    fok = os.path.join(pasta, "silabas-ok.json")
    if os.path.exists(fok):
        try:
            pedacos = json.load(io.open(fok, encoding="utf-8"))
        except ValueError:
            pedacos = {}
    sem = asyncio.Semaphore(PAR)
    tarefas, alvos = [], []
    for palavra in sorted(mapa):
        sil = [s for s in mapa[palavra] if s]
        if not sil:
            continue
        assinatura = "|".join(sil) + "|" + voz + "|" + RATE + "|" + METODO
        prontos = all(os.path.exists(os.path.join(
            audio, "%ssb_%s_%d.mp3"
            % (prefixo, arquivo_da_palavra(palavra), i))) for i in range(len(sil)))
        if carimbo.get(palavra) == assinatura and prontos:
            continue
        # ⭐⭐ A PALAVRA INTEIRA, e não mais "bo, la, ca".
        #    Esta linha É o conserto: a voz pronuncia bem porque "cavalo" é
        #    palavra de verdade. Quem separa as sílabas depois é o alinhamento.
        texto = u"".join(sil).lower() + u"."
        base = os.path.join(audio, "_seq_" + arquivo_da_palavra(palavra))
        alvos.append((palavra, assinatura, len(sil)))
        tarefas.append(_uma(sem, edge_tts, texto, voz, base, sil, prefixo, palavra,
                            palavra in pedacos or palavra.upper() in pedacos))
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
    # ⭐ O RECIBO DA CONFERENCIA — e dele que o portao 1y le, e e ele que
    #   dispensa o Marcos de ouvir. Fica NO REPOSITORIO, nao so no log da
    #   execucao: o que o log engole, o repo guarda.
    if CONFERIDAS or NAO_CONFERIDAS:
        por_caminho = {}
        for _w, _c, _n, _d in CONFERIDAS:
            por_caminho[_c] = por_caminho.get(_c, 0) + 1
        print(u"   conferidas sozinhas: %d de %d (%s)"
              % (len(CONFERIDAS), len(CONFERIDAS) + len(NAO_CONFERIDAS),
                 u", ".join(u"%s x%d" % (k, v) for k, v in sorted(por_caminho.items()))))
        _fc = sum(1 for _w, _c, _n, _d in CONFERIDAS for x in _d if x.get(u"forma") == u"citacao")
        _fp = sum(1 for _w, _c, _n, _d in CONFERIDAS for x in _d if x.get(u"forma") == u"palavra")
        print(u"   forma da silaba: %d em CITACAO (como a professora separa) · %d ficaram "
              u"como saem NA PALAVRA (a apartada soletrou ou nao fechou)" % (_fc, _fp))
        for _w, _m in NAO_CONFERIDAS[:10]:
            print(u"   ⚠️ %s: %s" % (_w, _m))
        # ⭐⭐ O RECIBO SE MESCLA, NAO SE SOBRESCREVE (18/set/2026). Antes, uma
        #    gravacao INCREMENTAL (so a palavra nova) apagava as outras do
        #    recibo, e o portao 1y parava a entrega de um caderno inteiro por
        #    causa de uma palavra. Agora: le o recibo que existe, tira as
        #    palavras desta rodada das duas listas, junta, e so guarda palavra
        #    que ainda esta no mapa (senao acumula lixo de palavra apagada).
        rec_cam = os.path.join(audio, "_conferencia.json")
        velho = {u"conferidas": [], u"nao_conferidas": []}
        if os.path.exists(rec_cam):
            try:
                velho = json.load(io.open(rec_cam, encoding="utf-8"))
            except Exception:                                    # noqa: BLE001
                pass
        nesta = set(w for w, _c, _n, _d in CONFERIDAS) | set(w for w, _m in NAO_CONFERIDAS)
        vivas = set(mapa)
        conf = [x for x in (velho.get(u"conferidas") or [])
                if x.get(u"palavra") in vivas and x.get(u"palavra") not in nesta]
        nconf = [x for x in (velho.get(u"nao_conferidas") or [])
                 if x.get(u"palavra") in vivas and x.get(u"palavra") not in nesta]
        conf += [{u"palavra": w, u"caminho": c, u"pedacos": n, u"recortes": d}
                 for w, c, n, d in CONFERIDAS]
        nconf += [{u"palavra": w, u"motivo": m} for w, m in NAO_CONFERIDAS]
        io.open(rec_cam, "w", encoding="utf-8").write(json.dumps(
            {u"voz": voz, u"rate": RATE, u"metodo": METODO,
             u"tetos_s": TETO_ABS, u"alvo_lk": ALVO_LK, u"teto_tp": TETO_TP,
             u"conferidas": sorted(conf, key=lambda x: x[u"palavra"]),
             u"nao_conferidas": sorted(nconf, key=lambda x: x[u"palavra"])},
            ensure_ascii=False, indent=1))
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
