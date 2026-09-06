#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
============================================================
 TESTADOR HUMANO — o OUVIDO (o olho de VOZ do Revisor)

 Pedido do Marcos (set/2026): *"verifique a possibilidade de um testador humano
 que testa tudo — áudio, imagens etc. — a maioria desses erros que reportei"*.
 O `_qa/revisor.py` é o olho de TEXTO; este é o OUVIDO: ele **escuta cada mp3**
 com um reconhecedor de fala (faster-whisper, roda no runner do GitHub, sem
 chave nenhuma) e compara com o que o `falas.json` diz que a voz deveria dizer.

 O que ele pega — a família de erro que mais chegou ao Marcos:
   · "ilefante" (a voz diz outra palavra: a escrita fonética errou);
   · voz de OUTRA fala no arquivo (prefixo trocado, resto de clone);
   · fala cortada no meio (o mp3 acabou antes do texto);
   · mp3 vazio/mudo.

 O que ele NÃO julga sozinho (marca "CONFERIR"): falas muito curtas (nome de
 letra, "Cê", "Éfe": o reconhecedor erra nelas) e números/símbolos (a voz fala
 "vinte e quatro dividido por dois", o texto escreve "24 ÷ 2" — o comparador
 converte, mas na dúvida pede ouvido humano).

 Uso:  python3 _qa/testador_ouvido.py <pasta> [--modelo small|base|medium] [--max N]
 Escreve _status/testador-ouvido-<pasta>.md (+ .json). Sai 0 = tudo bateu;
 1 = achou voz que não diz o texto; 2 = não consegui medir.
============================================================
"""
import io, os, re, sys, json, time, unicodedata

def norm(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = (s.replace(u"&nbsp;", " ").replace(u"&amp;", "e").replace(u"&eacute;", u"é")
           .replace(u"&aacute;", u"á").replace(u"&atilde;", u"ã").replace(u"&ccedil;", u"ç")
           .replace(u"&otilde;", u"õ").replace(u"&ecirc;", u"ê").replace(u"&oacute;", u"ó")
           .replace(u"&iacute;", u"í").replace(u"&uacute;", u"ú").replace(u"&ocirc;", u"ô")
           .replace(u"&acirc;", u"â"))
    s = re.sub(r"&#?\w+;", " ", s)
    # símbolos de conta como a voz os fala
    s = (s.replace(u"÷", u" dividido por ").replace(u"×", u" vezes ").replace(u"+", u" mais ")
           .replace(u"−", u" menos ").replace(u"-", u" ").replace(u"=", u" igual a "))
    s = s.lower()
    s = u"".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def numeros_por_extenso(s):
    try:
        from num2words import num2words
    except Exception:
        return s
    def troca(m):
        try:
            return u" " + num2words(int(m.group(0)), lang="pt_BR") + u" "
        except Exception:
            return m.group(0)
    return re.sub(r"\d+", troca, s)

def parecido(a, b):
    try:
        from rapidfuzz import fuzz
        return max(fuzz.ratio(a, b), fuzz.token_set_ratio(a, b))
    except Exception:
        import difflib
        return 100.0 * difflib.SequenceMatcher(None, a, b).ratio()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); return 2
    pasta = args[0].rstrip("/")
    modelo = "small"; maximo = 0
    for i, a in enumerate(sys.argv):
        if a == "--modelo" and i + 1 < len(sys.argv): modelo = sys.argv[i + 1]
        if a == "--max" and i + 1 < len(sys.argv): maximo = int(sys.argv[i + 1])
    fj = os.path.join(pasta, "falas.json")
    if not os.path.exists(fj):
        print(u"%s -> NAO MEDI: sem falas.json (a verdade da voz e ele)." % pasta); return 2
    falas = json.load(io.open(fj, encoding="utf-8"))
    if isinstance(falas, dict):
        falas = falas.get("falas") or [{"id": k, "texto": v} for k, v in falas.items()]
    itens = [(f.get("id"), f.get("texto", "")) for f in falas if isinstance(f, dict) and f.get("id")]
    itens = [(i, t) for i, t in itens if os.path.exists(os.path.join(pasta, "audio", i + ".mp3"))]
    # mp3 que NENHUMA fala do falas.json promete: sobra de texto que mudou (nao e defeito, e peso morto)
    pasta_audio = os.path.join(pasta, "audio")
    ids = set(i for i, _ in itens)
    orfaos = sorted(a[:-4] for a in os.listdir(pasta_audio) if a.endswith(".mp3") and a[:-4] not in ids) if os.path.isdir(pasta_audio) else []
    if maximo: itens = itens[:maximo]
    if not itens:
        print(u"%s -> NAO MEDI: nenhuma fala do falas.json tem mp3 em audio/." % pasta); return 2
    try:
        from faster_whisper import WhisperModel
    except Exception as e:
        print(u"%s -> NAO MEDI: faster-whisper nao esta instalado aqui (%s). Este ouvido roda no runner (testador-humano.yml)." % (pasta, e)); return 2
    t0 = time.time()
    wm = WhisperModel(modelo, device="cpu", compute_type="int8")
    ruins, conferir, ok, mudos = [], [], 0, []
    for n, (fid, texto) in enumerate(itens):
        cam = os.path.join(pasta, "audio", fid + ".mp3")
        esperado = norm(numeros_por_extenso(norm(texto)))
        try:
            segs, info = wm.transcribe(cam, language="pt", beam_size=1, vad_filter=False)
            ouvido = u" ".join(s.text for s in segs).strip()
            dur = float(getattr(info, "duration", 0) or 0)
        except Exception as e:
            mudos.append((fid, texto[:60], u"nao consegui abrir/transcrever: %s" % str(e)[:60])); continue
        ouv = norm(ouvido)
        if dur < 0.25 or not ouv:
            mudos.append((fid, texto[:60], u"mp3 %.2fs, nada ouvido" % dur)); continue
        sim = parecido(esperado, ouv)
        # ⚠️ (1a rodada, set/2026) "K de kiwi", "T de trem", "Y de yoyo" sairam como
        #    "diz OUTRA coisa" (ouvi "Kadkiuri", "TeideTrain", "e epsilon de olho"): e o
        #    reconhecedor tropecando em NOME DE LETRA + palavra curta, nao a voz
        #    errada (ipsilon E o nome do Y). Frase de ate 4 palavras com " de " no
        #    meio e nome de letra: vai para CONFERIR, com ouvido humano.
        nome_letra = bool(re.match(r"^(letra )?\S{1,8}\.? ?(\S{1,8} )?de \S{1,12}$", esperado)) and len(esperado.split()) <= 5
        curto = len(esperado) < 8 or nome_letra
        # fala cortada: o texto e longo e a voz parou muito antes (menos de 60% do tamanho)
        cortada = len(esperado) >= 30 and len(ouv) < 0.6 * len(esperado)
        if curto:
            (conferir if sim < 70 else None) and conferir.append((fid, texto[:60], ouvido[:60], sim, u"fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido"))
            if sim >= 70: ok += 1
        elif sim >= 80 and not cortada:
            ok += 1
        elif sim >= 62 and not cortada:
            conferir.append((fid, texto[:70], ouvido[:70], sim, u"parecido mas nao igual"))
        else:
            ruins.append((fid, texto[:80], ouvido[:80], sim, u"CORTADA (%.1fs)" % dur if cortada else u"diz OUTRA coisa"))
        if (n + 1) % 50 == 0:
            print(u"  ... %d/%d ouvidas (%.0fs)" % (n + 1, len(itens), time.time() - t0)); sys.stdout.flush()
    dt = time.time() - t0
    L = [u"# 👂 TESTADOR HUMANO — OUVIDO — `%s`" % pasta, u"",
         u"> %d fala(s) do `falas.json` ouvidas com faster-whisper (%s, CPU) em %.0f s. "
         u"Sai 1 se alguma voz NAO diz o texto. Isto é o olho de VOZ do Revisor (`_qa/revisor.py` é o de TEXTO)."
         % (len(itens), modelo, dt), u"",
         u"| resultado | quantas |", u"|---|--:|",
         u"| ✅ diz o que está escrito | %d |" % ok,
         u"| ❌ diz OUTRA coisa / cortada | %d |" % len(ruins),
         u"| 🔇 muda ou não abre | %d |" % len(mudos),
         u"| 🟡 conferir no ouvido (curta/parecida) | %d |" % len(conferir),
         u"| 🗑 mp3 órfão (nenhuma fala do falas.json usa; peso morto, não defeito) | %d |" % len(orfaos), u""]
    if ruins:
        L += [u"## ❌ Vozes que não dizem o texto", u"", u"| id | texto esperado | o que ouvi | parecido | motivo |", u"|---|---|---|--:|---|"]
        for r in ruins: L.append(u"| `%s` | %s | %s | %.0f | %s |" % (r[0], r[1].replace(u"|", u"/"), r[2].replace(u"|", u"/"), r[3], r[4]))
        L.append(u"")
    if mudos:
        L += [u"## 🔇 Mudas ou que não abrem", u""] + [u"- `%s` — %s — %s" % m for m in mudos] + [u""]
    if conferir:
        L += [u"## 🟡 Conferir no ouvido", u"", u"| id | texto | ouvi | parecido | por quê |", u"|---|---|---|--:|---|"]
        for r in conferir[:80]: L.append(u"| `%s` | %s | %s | %.0f | %s |" % (r[0], r[1].replace(u"|", u"/"), r[2].replace(u"|", u"/"), r[3], r[4]))
        if len(conferir) > 80: L.append(u"| … | e mais %d | | | |" % (len(conferir) - 80))
        L.append(u"")
    os.makedirs("_status", exist_ok=True)
    nome = pasta.strip("_/").replace("/", "-")
    io.open(os.path.join("_status", "testador-ouvido-%s.md" % nome), "w", encoding="utf-8").write(u"\n".join(L) + u"\n")
    json.dump({"pasta": pasta, "modelo": modelo, "ouvidas": len(itens), "ok": ok, "ruins": ruins, "mudos": mudos,
               "conferir": conferir, "orfaos": orfaos, "segundos": round(dt)},
              io.open(os.path.join("_status", "testador-ouvido-%s.json" % nome), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(u"%s -> ouvido: %d ok, %d NAO dizem o texto, %d mudas, %d a conferir (%.0fs, %s)"
          % (pasta, ok, len(ruins), len(mudos), len(conferir), dt, modelo))
    for r in ruins[:12]:
        print(u"   ❌ %s: esperava \"%s\" ouvi \"%s\" (%.0f) %s" % r)
    return 1 if (ruins or mudos) else 0

if __name__ == "__main__":
    sys.exit(main())
