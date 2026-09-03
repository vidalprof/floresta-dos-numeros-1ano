# -*- coding: utf-8 -*-
u"""
PORTÃO DA PRONÚNCIA — o primeiro que OUVE.

POR QUE ELE EXISTE, e a conta é constrangedora: o Marcos relatou 7 defeitos
jogando com a turma (set/2026). Os portões da casa pegavam 2. Os 5 que escaparam
eram TODOS de voz:

    · "sandboard" lido do jeito português, em vez de "sendbord"
    · "ilefante" no lugar de "elefante"
    · a sílaba "PA" lida como a preposição "para"
    · a sílaba "BE" que simplesmente não sai
    · as letras P, T, N, H mudas — só A e O falavam

Fui então contar quantos dos ~70 portões abrem o mp3 e escutam o que ele diz.
Nenhum. Os que temos — falas, voz_bate, vozfalta, vozrobo — fazem coisas úteis,
mas todas em cima do TEXTO: conferem se a fala foi gravada, se a voz da resposta
é a palavra escrita, se há palavra da lista de armadilhas. Nenhum ouve.

É por isso que eu tentei consertar "elefante" QUATRO vezes ("ele fante",
"élefante", "êlefante"...) sem acertar: eu não escuto o resultado, então estava
chutando grafia — e cada chute custava uma aula com a criança ouvindo errado. A
conferência inteira ficava por conta do Marcos, no meio da aula.

O QUE ELE FAZ: pega o mp3 que a criança vai ouvir, converte para wav 16k mono,
transcreve com o Vosk (reconhecimento offline, grátis) e compara com o texto que
o `falas.json` prometeu. O ciclo fecha: gravou → ouviu → conferiu.

⚠️ O QUE ELE NÃO É: um juiz de sotaque. O reconhecedor erra, e erra mais em
áudio curto. Por isso ele NÃO exige transcrição perfeita numa FRASE — mede a
distância e só reclama quando é grande demais para ser ruído. Em palavra SOZINHA
a régua vira contagem de letras, porque ali uma letra trocada não é ruído: é a
palavra errada (ver LETRAS_SOZINHA).

⚠️⚠️ E O LIMITE HONESTO, que descobri testando e que muda o que prometer: o
Vosk tem MODELO DE LINGUAGEM. Ele não devolve o que ouviu foneticamente — devolve
a palavra mais provável do português que se parece com aquilo. Então há uma
chance real de ele ouvir "ilefante" e TRANSCREVER "elefante", consertando no
papel o defeito que a criança escuta no ouvido.

O que isso significa na prática:
  · o que ele pega com folga: silêncio (a sílaba BE que não sai), palavra
    trocada por outra (PA virando "para"), letra muda, palavra estrangeira lida
    ao pé da letra — ou seja, QUATRO dos cinco casos do Marcos;
  · o que pode escapar: a troca de vogal átona dentro de uma palavra que existe
    ("ilefante"), justamente porque o modelo a corrige.
Para esse resto existe caminho — dar ao reconhecedor uma gramática restrita com
as DUAS grafias e ver qual ele prefere — e ele fica anotado como próximo passo.
Prometer que este portão mata o "ilefante" seria repetir o erro de quatro
tentativas atrás: dizer que resolvi sem ter ouvido.

⚠️ ONDE ELE RODA: aqui não — o modelo de voz mora em alphacephei.com, que o
proxy do container bloqueia. Ele roda no GitHub Actions (internet liberada),
dentro do `entregar.yml`, logo DEPOIS de gravar a voz e ANTES de publicar. É o
lugar certo: é ali que o mp3 nasce.

Uso:  python3 _qa/pronuncia.py <pasta> [--modelo CAMINHO] [--limite N]
Sai 0 se a voz diz o que devia, 1 se algo saiu torto, 2 se não deu para ouvir.
"""
import json, os, re, subprocess, sys, unicodedata, wave

# ---------------------------------------------------------------- limiares
#  A distância é o "quanto teria de mudar" para uma frase virar a outra, de 0
#  (idêntico) a 1 (nada a ver). Os números vieram de medir os casos REAIS:
#  "ilefante" x "elefante" dá 0,12 — pequeno, mas é justamente o erro que a
#  criança ouve. Palavra curta e isolada não tem contexto que ajude o
#  reconhecedor, então ali a régua é mais dura; frase longa tem, e afrouxa.
DISTANCIA_LONGA = 0.45    # frase: o reconhecedor troca palavrinha à toa
MINIMO_PARA_MEDIR = 2     # abaixo disso (uma letra) o ASR não tem o que ouvir

#  ⚠️ PALAVRA SOZINHA tem régua própria, e por um motivo medido: "elefante" x
#  "ilefante" difere em UMA letra de oito — 12%, que qualquer teto percentual
#  razoável deixa passar. Só que é exatamente esse 12% que a criança ouve. Numa
#  frase, uma letra trocada é ruído do reconhecedor; numa palavra dita sozinha,
#  é a palavra errada. Então aqui a conta é em LETRAS, não em porcento.
LETRAS_SOZINHA = 1        # 1 letra diferente numa palavra solta já é suspeito


def sem_acento(t):
    t = unicodedata.normalize("NFD", t)
    return u"".join(c for c in t if unicodedata.category(c) != "Mn")


def limpa(t):
    u"""deixa só o que a voz de fato pronuncia."""
    t = re.sub(r"<[^>]*>", u" ", u"%s" % t)
    t = re.sub(r"&[a-z]+;|&#\d+;", u" ", t)
    t = sem_acento(t).lower()
    t = re.sub(r"[^a-z0-9 ]+", u" ", t)
    return re.sub(r"\s+", u" ", t).strip()


def distancia(a, b):
    u"""Levenshtein normalizado, 0 = igual, 1 = nada a ver."""
    if a == b:
        return 0.0
    if not a or not b:
        return 1.0
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atual = [i]
        for j, cb in enumerate(b, 1):
            atual.append(min(ant[j] + 1, atual[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = atual
    return ant[-1] / float(max(len(a), len(b)))


def ffmpeg():
    for c in ("ffmpeg",):
        try:
            subprocess.run([c, "-version"], capture_output=True, check=True)
            return c
        except Exception:
            pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def para_wav(ff, mp3, wav):
    subprocess.run([ff, "-loglevel", "error", "-i", mp3, "-ar", "16000",
                    "-ac", "1", "-f", "wav", wav, "-y"], check=True,
                   capture_output=True)


def transcreve(modelo, wav):
    from vosk import KaldiRecognizer
    f = wave.open(wav, "rb")
    rec = KaldiRecognizer(modelo, f.getframerate())
    rec.SetWords(False)
    txt = []
    while True:
        d = f.readframes(4000)
        if not d:
            break
        if rec.AcceptWaveform(d):
            txt.append(json.loads(rec.Result()).get("text", ""))
    txt.append(json.loads(rec.FinalResult()).get("text", ""))
    f.close()
    return limpa(u" ".join(t for t in txt if t))


def confere(pasta, cam_modelo=None, limite=0):
    fal = os.path.join(pasta, "falas.json")
    aud = os.path.join(pasta, "audio")
    if not os.path.exists(fal):
        print(u"NAO MEDI: nao achei %s" % fal); return 2
    if not os.path.isdir(aud):
        print(u"NAO MEDI: nao achei a pasta %s (a voz ainda nao foi gravada)" % aud); return 2

    try:
        import types
        if "srt" not in sys.modules:                 # o vosk importa srt só para legenda
            sys.modules["srt"] = types.ModuleType("srt")
        from vosk import Model, SetLogLevel
        SetLogLevel(-1)
    except Exception as e:
        print(u"NAO MEDI: o Vosk nao esta disponivel aqui (%s). "
              u"Este portao roda no GitHub Actions, onde ha internet para o modelo." % e)
        return 2

    cam_modelo = cam_modelo or os.environ.get("VOSK_MODELO") or "_qa/ferramentas/modelos/pt"
    if not os.path.isdir(cam_modelo):
        print(u"NAO MEDI: nao achei o modelo de voz em %s.\n"
              u"   Baixe com: curl -sSL -o pt.zip "
              u"https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip\n"
              u"   (o proxy do container bloqueia esse site; no Actions funciona)"
              % cam_modelo)
        return 2

    ff = ffmpeg()
    if not ff:
        print(u"NAO MEDI: sem ffmpeg para converter o mp3 (pip install imageio-ffmpeg)")
        return 2

    modelo = Model(cam_modelo)
    falas = json.load(open(fal, encoding="utf-8"))
    if isinstance(falas, dict):
        falas = [{"id": k, "texto": v} for k, v in falas.items()]

    tortas, medidas = [], 0
    tmp = os.path.join(pasta, "_pron.wav")
    for f in falas:
        if limite and medidas >= limite:
            break
        fid, txt = f.get("id"), f.get("texto", "")
        mp3 = os.path.join(aud, "%s.mp3" % fid)
        esperado = limpa(txt)
        if not fid or not os.path.exists(mp3) or len(esperado) < MINIMO_PARA_MEDIR:
            continue
        try:
            para_wav(ff, mp3, tmp)
            ouvido = transcreve(modelo, tmp)
        except Exception as e:
            print(u"   (nao consegui ouvir %s: %s)" % (fid, e))
            continue
        medidas += 1
        if not ouvido:
            # ⚠️ silêncio conta a partir de DUAS letras, e é de propósito: o caso
            #    do Marcos foi a sílaba "BE" da ABELHA, que simplesmente não saía.
            #    Com régua de 4 letras ela escapava — e ela é o defeito.
            #    Em pedaço tão curto o reconhecedor às vezes não pega mesmo, então
            #    a mensagem diz isso: é para o humano ouvir, não para confiar cego.
            if len(esperado) >= MINIMO_PARA_MEDIR:
                tortas.append((fid, esperado,
                               u"(NADA — ou o mp3 esta mudo, ou e curto demais para o "
                               u"reconhecedor: OUCA este)", 1.0))
            continue
        d = distancia(esperado, ouvido)
        uma_palavra = (" " not in esperado)
        if uma_palavra:
            # conta em LETRAS: numa palavra solta, uma letra trocada é a palavra errada
            letras = round(d * max(len(esperado), len(ouvido)))
            if letras >= LETRAS_SOZINHA:
                tortas.append((fid, esperado, ouvido, d))
        elif d > DISTANCIA_LONGA:
            tortas.append((fid, esperado, ouvido, d))
    if os.path.exists(tmp):
        os.remove(tmp)

    if not medidas:
        print(u"NAO MEDI: nenhum mp3 pronto para ouvir em %s" % pasta)
        return 2

    if tortas:
        print(u"%s -> %d fala(s) SAIRAM TORTAS (de %d ouvidas):" % (pasta, len(tortas), medidas))
        for fid, esp, ouv, d in sorted(tortas, key=lambda x: -x[3])[:15]:
            print(u"    ✗ [%s] devia dizer “%s”" % (fid, esp))
            print(u"           e eu ouvi     “%s”   (%.0f%% diferente)" % (ouv, d * 100))
        if len(tortas) > 15:
            print(u"    ... e mais %d" % (len(tortas) - 15))
        print(u"   Conserto: escreva a palavra COMO SOA no `_FONETICA_VOZ` do montador")
        print(u"   (ex.: sandboard -> sendibórdi). A TELA continua com a grafia certa;")
        print(u"   só o texto que vai para a voz muda. Depois rode este portao de novo.")
        return 1

    print(u"%s -> pronuncia ok: ouvi %d fala(s), todas dizem o que estava escrito."
          % (pasta, medidas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/pronuncia.py <pasta> [--modelo CAMINHO] [--limite N]")
        sys.exit(2)
    mod = None; lim = 0
    if "--modelo" in sys.argv:
        mod = sys.argv[sys.argv.index("--modelo") + 1]
    if "--limite" in sys.argv:
        lim = int(sys.argv[sys.argv.index("--limite") + 1])
    sys.exit(confere(sys.argv[1].rstrip("/"), mod, lim))
