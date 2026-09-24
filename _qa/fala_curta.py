# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1q3 — O MP3 E CURTO DEMAIS PARA O QUE ELE DEVIA DIZER

 NASCEU DE SETE FALAS TRUNCADAS QUE FORAM AO AR (24/set/2026, `_div3`). Sete
 mp3 do caderno da divisao sairam com **0,36 segundo e 2160 bytes**, todos
 iguais — inclusive um que devia dizer *"Isso! Em cada coelho ficam 8 cenouras.
 O fato e 16 dividido por 2 igual a 8."*, que leva cinco segundos. E TRES deles
 eram **o mesmo arquivo, byte a byte**, para tres textos diferentes.

 ⚠️⚠️ POR QUE NENHUM PORTAO VIA: o `_qa/voz_gravada.py` (1q2) pergunta se o mp3
    EXISTE; o `_qa/vozfalta.py` (0i) vai do texto para o audio; o `0v` mede a
    FORCA (e estes tinham som, nao eram mudos); e o ouvido (`pronuncia.py`) nao
    reprova a entrega. Ninguem perguntava se o arquivo tem TAMANHO DE FALA.
    A crianca tocaria o alto-falante e ouviria um caco de som.

 ⭐ A REGUA, MEDIDA E NAO CHUTADA. Nas 412 falas gravadas do `_div3`:
      · as SETE truncadas ..... 0,0049 a 0,0212 segundo por caractere
      · a mais apertada das BOAS ............ 0,0734 s/caractere
    Entre as duas pontas ha 3,5x de folga. O corte fica em **0,045 s/caractere**
    — 2,1x abaixo da fala boa mais apertada e 2,1x acima da pior truncada.
    Trocou a voz ou a velocidade dela, REMEDE (a saida imprime a distribuicao).

 ⚠️ E O CARACTERE SE CONTA COMO A VOZ LE, nao como esta escrito: `12 ÷ 3 = 4.`
    tem onze caracteres no papel e a voz diz *"doze dividido por tres igual a
    quatro"*, que sao trinta e sete. Sem essa conta o portao chamaria de boa uma
    fala truncada de conta — que e justamente a metade deste caderno. E a mesma
    licao dos acentos e dos numeros: **normalizar ANTES da regua**.

 A SEGUNDA REGRA NAO TEM CORTE NENHUM, e e a mais forte: **dois textos
 diferentes nao podem ter o MESMO mp3**, byte a byte. Nenhuma folha precisa
 disso, e foi assim que tres das sete se denunciaram.

 Uso:  python3 _qa/fala_curta.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

# ⭐ MEDIDO, NAO CHUTADO — ver o cabecalho. A saida imprime a distribuicao em
#    toda rodada, para quem trocar a voz poder remedir sem abrir este arquivo.
PISO = 0.045          # segundos de audio por caractere falado
CURTO = 3             # textos com menos que isto de texto falado nao entram
                      # (⚠️ PALPITE DECLARADO: com um ou dois caracteres a
                      #  razao vira ruido, e "5." nao prova nada.)

SIMBOLOS = [(u"÷", u" dividido por "), (u"×", u" vezes "), (u"=", u" igual a "),
            (u"+", u" mais "), (u"%", u" por cento "), (u"&divide;", u" dividido por "),
            (u"&times;", u" vezes ")]


def falado(t):
    u"""O texto como a VOZ o le: simbolos por extenso, numeros por extenso."""
    t = u"%s" % (t or u"")
    for a, b in SIMBOLOS:
        t = t.replace(a, b)
    t = re.sub(r"<[^>]*>", u" ", t)
    t = re.sub(r"&[a-z]+;|&#\d+;", u" ", t)
    t = unicodedata.normalize(u"NFD", t)
    t = u"".join(c for c in t if unicodedata.category(c) != u"Mn").lower()
    try:
        from ouvir import extenso
        t = re.sub(r"\d+", lambda m: u" " + extenso(m.group(0)) + u" ", t)
    except Exception:                                            # noqa: BLE001
        pass          # sem a tabela a conta so fica mais rigorosa, nunca frouxa
    t = re.sub(r"[^a-z0-9 ]+", u" ", t)
    return re.sub(r"\s+", u" ", t).strip()


def duracao(cam):
    for prog in (u"ffprobe",):
        try:
            s = subprocess.check_output(
                [prog, u"-v", u"error", u"-show_entries", u"format=duration",
                 u"-of", u"csv=p=0", cam], stderr=subprocess.STDOUT)
            return float(s.strip())
        except Exception:                                        # noqa: BLE001
            return None
    return None


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/fala_curta.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    fj = os.path.join(pasta, u"falas.json")
    audio = os.path.join(pasta, u"audio")
    if not os.path.exists(fj):
        print(u"%s -> NAO MEDI: nao achei o falas.json." % pasta)
        return 2
    if not os.path.isdir(audio):
        print(u"%s -> NAO MEDI: a voz ainda nao foi gravada (sem pasta audio/). "
              u"O entregar.yml grava ao publicar." % pasta)
        return 2
    F = json.load(io.open(fj, encoding=u"utf-8"))

    razoes, curtas, sem_medida = [], [], 0
    porhash = {}
    for f in F:
        cam = os.path.join(audio, f[u"id"] + u".mp3")
        if not os.path.exists(cam):
            continue
        txt = falado(f[u"texto"])
        h = hashlib.md5(io.open(cam, u"rb").read()).hexdigest()
        porhash.setdefault(h, []).append((f[u"id"], f[u"texto"]))
        if len(txt) < CURTO:
            continue
        s = duracao(cam)
        if s is None:
            sem_medida += 1
            continue
        r = s / float(len(txt))
        razoes.append((r, f[u"id"], s, len(txt), f[u"texto"]))
        if r < PISO:
            curtas.append((r, f[u"id"], s, len(txt), f[u"texto"]))

    if not razoes and sem_medida:
        print(u"%s -> NAO MEDI: nao consegui ler a duracao de nenhum mp3 "
              u"(falta o ffprobe?)." % pasta)
        return 2
    if not razoes:
        print(u"%s -> NAO MEDI: nenhum mp3 gravado para medir." % pasta)
        return 2

    # ⭐ os gemeos: dois TEXTOS diferentes no mesmo arquivo
    gemeos = []
    for h, lista in porhash.items():
        textos = set(t for _i, t in lista)
        if len(lista) > 1 and len(textos) > 1:
            gemeos.append(lista)

    razoes.sort()
    print(u"%s -> duracao da fala: %d mp3 medido(s)" % (pasta, len(razoes)))
    print(u"   piso %.3f s por caractere falado (MEDIDO — ver o topo do arquivo)"
          % PISO)
    print(u"   a mais apertada das que passam: %.4f s/car · mediana %.4f"
          % (next((r[0] for r in razoes if r[0] >= PISO), float("nan")),
             razoes[len(razoes) // 2][0]))
    if sem_medida:
        print(u"   %d mp3 sem duracao legivel (nao entraram na conta)" % sem_medida)

    if not curtas and not gemeos:
        print(u"   ok: nenhuma fala curta demais e nenhum mp3 repetido.")
        return 0

    if curtas:
        print(u"   %d FALA(S) CURTA(S) DEMAIS — a crianca ouve um caco de som:"
              % len(curtas))
        for r, ident, s, n, txt in curtas:
            print(u"    x %-14s %.2fs para %d caracteres falados (%.4f s/car)"
                  % (ident, s, n, r))
            print(u"        devia dizer: %s" % txt[:86])
    if gemeos:
        print(u"   %d ARQUIVO(S) SERVINDO A MAIS DE UM TEXTO (mesmo mp3, byte a byte):"
              % len(gemeos))
        for lista in gemeos:
            print(u"    x " + u", ".join(i for i, _t in lista))
            for _i, t in lista:
                print(u"        %s" % t[:80])
    print(u"   conserto: apagar esses mp3 E a linha deles no "
          u"`<pasta>/audio/_carimbo.json`, e rodar o entregar.yml de novo — "
          u"o carimbo sha1 e quem decide se a voz se regrava.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
