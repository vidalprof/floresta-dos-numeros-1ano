# -*- coding: utf-8 -*-
u"""
============================================================
 LOUDNESS DE VERDADE PARA PEDACO CURTO — a "LKvoz"

 ⭐ POR QUE (18/set/2026, medido pela banca nos 882 recortes): o `loudnorm` do
    ffmpeg, em pedaco de menos de 400 ms, vira um normalizador de PICO — sua
    janela de integracao (400 ms) e maior que o audio, o gate nao tem o que
    gatear. Resultado: 9,8 dB de diferenca de forca entre recortes que deviam
    soar iguais (PA de capa vs LI de galinha), e ate 8,3 dB dentro da MESMA
    palavra. E o portao 1x ("quase mudo") media RMS maximo em 20 ms — que e
    quase pico tambem. Duas reguas de pico dizendo "esta igual".

 O QUE ISTO MEDE: a loudness da ITU-R BS.1770 (a mesma do loudnorm) — filtro K
 (shelf de +4 dB em 1,5 kHz + passa-altas em 38 Hz), potencia media em dBFS
 com o offset de -0,691 — MAS sem o gate de 400 ms e so nas janelas de 10 ms
 em que ha voz (ate 30 dB abaixo do pico do pedaco). E a loudness DO SOM, nao do arquivo com o
 seu silencio. Chamo de LKvoz para nao confundir com LUFS integrado.

 Os coeficientes do filtro K sao calculados para QUALQUER taxa de amostragem
 (a receita analogica da norma, discretizada por bilinear — mesma conta do
 `pyloudnorm`, que nao esta instalado aqui).

 Uso como biblioteca:
   from kvoz import lkvoz, pico_real
   lk = lkvoz(y, sr)            # dB (LUFS-like), None se nao ha voz
   tp = pico_real(y, sr)        # dBTP com 4x de sobreamostragem
============================================================
"""
from __future__ import print_function

import math

import numpy as np


def _biquad_shelf(fs, G=4.0, fc=1681.9744509555319, Q=0.7071752369554193):
    u"""Pre-filtro da BS.1770 (shelf de agudos). Receita do pyloudnorm."""
    A = 10 ** (G / 40.0)
    w0 = 2 * math.pi * fc / fs
    alpha = math.sin(w0) / (2 * Q)
    cw = math.cos(w0)
    b0 = A * ((A + 1) + (A - 1) * cw + 2 * math.sqrt(A) * alpha)
    b1 = -2 * A * ((A - 1) + (A + 1) * cw)
    b2 = A * ((A + 1) + (A - 1) * cw - 2 * math.sqrt(A) * alpha)
    a0 = (A + 1) - (A - 1) * cw + 2 * math.sqrt(A) * alpha
    a1 = 2 * ((A - 1) - (A + 1) * cw)
    a2 = (A + 1) - (A - 1) * cw - 2 * math.sqrt(A) * alpha
    return np.array([b0, b1, b2]) / a0, np.array([1.0, a1 / a0, a2 / a0])


def _biquad_hp(fs, fc=38.13547087602444, Q=0.5003270373238773):
    u"""Filtro RLB da BS.1770 (passa-altas). Receita do pyloudnorm."""
    w0 = 2 * math.pi * fc / fs
    alpha = math.sin(w0) / (2 * Q)
    cw = math.cos(w0)
    b0 = (1 + cw) / 2
    b1 = -(1 + cw)
    b2 = (1 + cw) / 2
    a0 = 1 + alpha
    a1 = -2 * cw
    a2 = 1 - alpha
    return np.array([b0, b1, b2]) / a0, np.array([1.0, a1 / a0, a2 / a0])


def filtro_k(y, fs):
    from scipy.signal import lfilter
    b, a = _biquad_shelf(fs)
    z = lfilter(b, a, y)
    b, a = _biquad_hp(fs)
    return lfilter(b, a, z)


def lkvoz(y, fs, janela_ms=10.0, piso_db=-30.0):
    u"""Loudness K-ponderada so das janelas com voz. None se nao ha voz.

    ⚠️ O "tem voz" e RELATIVO ao pico do proprio pedaco (piso_db abaixo dele),
    nao um -40 dBFS absoluto. Medido em 18/set/2026: com o piso absoluto, a
    medida dependia do GANHO — um pedaco fraco boostado em +15 dB passava a
    contar as caudas quietas como "voz", a media caia, e 95 silabas finais
    saiam 2 dB abaixo do alvo que o proprio ganho tinha mirado. Relativo ao
    pico, a medida antes e depois do ganho e a mesma."""
    y = np.asarray(y, dtype=np.float64)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if len(y) < int(fs * 0.02):
        return None
    z = filtro_k(y, fs)
    n = max(1, int(fs * janela_ms / 1000.0))
    ncomp = len(z) // n
    if ncomp == 0:
        return None
    blocos = z[:ncomp * n].reshape(ncomp, n)
    pot = (blocos ** 2).mean(axis=1)
    # "tem voz" se mede no sinal CRU, nao no filtrado (o filtro K tira grave)
    bruto = y[:ncomp * n].reshape(ncomp, n)
    pot_bruta = (bruto ** 2).mean(axis=1)
    if pot_bruta.max() <= 0:
        return None
    com_voz = pot_bruta > pot_bruta.max() * 10 ** (piso_db / 10.0)
    if not com_voz.any():
        return None
    media = pot[com_voz].mean()
    if media <= 0:
        return None
    return -0.691 + 10 * math.log10(media)


def pico_real(y, fs, vezes=4):
    u"""Pico verdadeiro (dBTP) com sobreamostragem — o mp3 estoura entre amostras."""
    from scipy.signal import resample_poly
    y = np.asarray(y, dtype=np.float64)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if not len(y):
        return -120.0
    z = resample_poly(y, vezes, 1)
    p = float(np.abs(z).max())
    return 20 * math.log10(p) if p > 0 else -120.0


def ganho_para(y, fs, alvo_lk=-18.0, teto_tp=-1.5):
    u"""Quantos dB somar para levar o pedaco ao alvo SEM passar do teto de pico.
    Devolve (ganho_dB, preso_no_teto). None se nao ha voz."""
    lk = lkvoz(y, fs)
    if lk is None:
        return None, False
    g = alvo_lk - lk
    tp = pico_real(y, fs)
    if tp + g > teto_tp:
        return teto_tp - tp, True
    return g, False


if __name__ == u"__main__":
    import sys
    import librosa
    for f in sys.argv[1:]:
        y, sr = librosa.load(f, sr=None, mono=True)
        lk = lkvoz(y, sr)
        print(u"%-40s LKvoz %s  TP %.1f dBTP" % (f, u"%.2f" % lk if lk is not None else u"(sem voz)", pico_real(y, sr)))
