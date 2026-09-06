#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
============================================================
 TESTADOR HUMANO — o OLHO (o olho VISUAL do Revisor, para IMAGENS)

 Para cada figura de `img/*.png` da atividade, pergunta a um modelo de visão
 (Gemini, pela GEMINI_API_KEY — só no runner do GitHub) se a imagem mostra o
 que o NOME dela promete (`tr_elefante.png` -> "elefante"). Pega a família de
 erro "a figura não é o que a palavra diz" (o OVO apontando para o mamão), a
 figura vazia/preta, o recorte que cortou a cabeça, e o texto/letra que a IA
 desenhou dentro da figura sem ninguém pedir.

 Fica de fora (não é figura de conteúdo): as camadas do mascote (`_fala`,
 `_pisca`, `_feliz`, `coru`, `masc`), `fundo`, `med_` (medalha), `cr1..cr6`
 (crachás), `pintar_` (desenho para colorir — a criança e que da a cor).

 Uso:  python3 _qa/testador_olho.py <pasta> [--modelo gemini-2.0-flash] [--max N]
 Escreve _status/testador-olho-<pasta>.md (+ .json). Sai 0 = todas batem;
 1 = figura que não é o que o nome diz; 2 = não consegui medir (sem chave, cota).
============================================================
"""
import io, os, re, sys, json, time, base64

IGNORA = re.compile(r"(_fala|_pisca|_feliz|coru|masc|fundo|^med_|_cr\d|pintar_|_capa|_logo|_ceu|_chao)", re.I)

def rotulo(nome):
    n = re.sub(r"^[a-z0-9]{1,4}_", "", nome)           # tira o prefixo da atividade
    n = re.sub(r"\d+$", "", n)                            # tira numero final
    return n.replace("_", " ").strip()

def pergunta(key, modelo, png, rot):
    import urllib.request
    b64 = base64.b64encode(io.open(png, "rb").read()).decode("ascii")
    prompt = (u"Você é um revisor de material didático para crianças de 6 a 10 anos. "
              u"Esta figura foi feita para representar: \"%s\". "
              u"Responda em UMA linha, neste formato exato: "
              u"VEREDITO=SIM ou VEREDITO=NAO | VEJO=<3 a 6 palavras do que a imagem mostra> | "
              u"PROBLEMAS=<nenhum, ou: texto/letras/números desenhados na imagem, figura cortada, fundo não transparente, figura vazia ou escura, mais de um objeto, objeto errado>" % rot)
    # ⚠️ (rodada 3) com 120 tokens de saida o Gemini 2.5 gastava tudo PENSANDO e a
    #    resposta chegava cortada ("VEREDIT"). Pensamento desligado + saida folgada.
    corpo = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/png", "data": b64}}]}],
             "generationConfig": {"temperature": 0.1, "maxOutputTokens": 400, "thinkingConfig": {"thinkingBudget": 0}}}
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (modelo, key)
    req = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    try:
        partes = d["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError):
        raise RuntimeError("resposta sem texto (bloqueio/vazia): %s" % json.dumps(d)[:120])
    txt = u" ".join(p.get("text", "") for p in partes).strip()
    return txt.replace("*", "").replace("\n", " ")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); return 2
    pasta = args[0].rstrip("/")
    modelo = "gemini-2.0-flash"; maximo = 0
    for i, a in enumerate(sys.argv):
        if a == "--modelo" and i + 1 < len(sys.argv): modelo = sys.argv[i + 1]
        if a == "--max" and i + 1 < len(sys.argv): maximo = int(sys.argv[i + 1])
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print(u"%s -> NAO MEDI: sem GEMINI_API_KEY (este olho roda no runner, testador-humano.yml)." % pasta); return 2
    pngs = sorted(f for f in os.listdir(os.path.join(pasta, "img")) if f.endswith(".png") and not IGNORA.search(f[:-4])) if os.path.isdir(os.path.join(pasta, "img")) else []
    if maximo: pngs = pngs[:maximo]
    if not pngs:
        print(u"%s -> NAO SE APLICA: nenhuma figura de conteudo em img/. Nada a conferir." % pasta); return 2
    t0 = time.time(); ok, ruins, avisos, falhas = 0, [], [], []
    # ⚠️ (1a rodada, set/2026) `gemini-2.0-flash` respondeu 404 em TODAS as figuras: o
    #    nome do modelo aposentou. Nome de modelo e coisa que muda por baixo de nos —
    #    entao ha uma FILA de nomes, e o 404 pula para o proximo em vez de parar.
    # ⚠️ (rodada 4) o plano gratis do `gemini-flash-latest` (2.5 Flash) deu 429 na 7a
    #    figura mesmo com 4,5 s de folga: o limite dele e ~5 pedidos/minuto. O
    #    `gemini-2.5-flash-lite` tem cota propria e mais folgada: e o primeiro da fila;
    #    quando UM modelo esgota, a fila passa ao proximo em vez de parar tudo.
    fila = [m for m in (modelo, "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash") if m]
    fila = list(dict.fromkeys(fila))
    for n, f in enumerate(pngs):
        rot = rotulo(f[:-4])
        resp = None; paciencia = 2
        while fila and resp is None:
            try:
                resp = pergunta(key, fila[0], os.path.join(pasta, "img", f), rot)
            except Exception as e:
                msg = str(e)
                if "429" in msg or "quota" in msg.lower() or "RESOURCE_EXHAUSTED" in msg:
                    # ⚠️ (rodada 3) o 429 era LIMITE POR MINUTO (bateu na 30a figura), nao
                    #    cota do dia: espera e tenta de novo antes de desistir.
                    if paciencia > 0:
                        paciencia -= 1; print(u"   429 em %s: espero 65 s e tento de novo" % fila[0]); time.sleep(65); continue
                    if len(fila) > 1:
                        print(u"   %s esgotou a cota: passo para %s" % (fila[0], fila[1])); fila.pop(0); paciencia = 1; continue
                    falhas.append((f, u"COTA do Gemini esgotada (429) em %s — parei aqui" % fila[0]))
                    fila = []
                    break
                if "503" in msg and paciencia > 0:
                    paciencia -= 1; time.sleep(8); continue
                if "404" in msg and len(fila) > 1:
                    print(u"   modelo %s -> 404; tentando %s" % (fila[0], fila[1])); fila.pop(0); continue
                falhas.append((f, u"%s: %s" % (fila[0], msg[:90]))); break
        if not fila:
            break
        if resp is None:
            continue
        modelo = fila[0]
        # (rodada 4) o modelo as vezes responde "VEREDITO: SIM" ou "VEREDITO - SIM":
        # aceitar =, : e - — senao a abelha certa virava "NAO e o que o nome diz".
        m = re.search(r"VEREDITO\s*[=:\-]\s*(SIM|NAO|N[ÃA]O)", resp, re.I)
        vejo = re.search(r"VEJO\s*[=:\-]\s*([^|]+)", resp, re.I); prob = re.search(r"PROBLEMAS\s*[=:\-]\s*(.+)$", resp, re.I)
        vejo = vejo.group(1).strip() if vejo else resp[:60]; prob = prob.group(1).strip() if prob else u"?"
        sim = bool(m and m.group(1).upper() == "SIM")
        if sim and re.match(r"(?i)nenhum", prob):
            ok += 1
        elif sim:
            avisos.append((f, rot, vejo, prob))
        else:
            ruins.append((f, rot, vejo, prob))
        time.sleep(6.5)   # o plano gratis conta pedidos por MINUTO (~5–15/min conforme o modelo)
    dt = time.time() - t0
    L = [u"# 👁 TESTADOR HUMANO — OLHO (imagens) — `%s`" % pasta, u"",
         u"> %d figura(s) de conteúdo julgadas por %s em %.0f s: a imagem mostra o que o NOME promete? "
         u"Camadas do mascote, fundo, medalha, crachás e desenhos para colorir ficam de fora." % (len(pngs), modelo, dt), u"",
         u"| resultado | quantas |", u"|---|--:|", u"| ✅ mostra o que o nome diz, sem problema | %d |" % ok,
         u"| ❌ NÃO é o que o nome diz | %d |" % len(ruins), u"| 🟡 é, mas com problema (texto na figura, corte, fundo…) | %d |" % len(avisos),
         u"| ⚠️ não consegui julgar | %d |" % len(falhas), u""]
    if ruins:
        L += [u"## ❌ Figuras que não são o que o nome diz", u"", u"| arquivo | nome promete | o modelo vê | problemas |", u"|---|---|---|---|"]
        L += [u"| `%s` | %s | %s | %s |" % tuple(x.replace(u"|", u"/") for x in r) for r in ruins] + [u""]
    if avisos:
        L += [u"## 🟡 Batem, mas com problema", u"", u"| arquivo | nome | vê | problema |", u"|---|---|---|---|"]
        L += [u"| `%s` | %s | %s | %s |" % tuple(x.replace(u"|", u"/") for x in r) for r in avisos] + [u""]
    if falhas:
        L += [u"## ⚠️ Não julgadas", u""] + [u"- `%s` — %s" % x for x in falhas] + [u""]
    os.makedirs("_status", exist_ok=True)
    nome = pasta.strip("_/").replace("/", "-")
    io.open(os.path.join("_status", "testador-olho-%s.md" % nome), "w", encoding="utf-8").write(u"\n".join(L) + u"\n")
    json.dump({"pasta": pasta, "modelo": modelo, "figuras": len(pngs), "ok": ok, "ruins": ruins, "avisos": avisos, "falhas": falhas, "segundos": round(dt)},
              io.open(os.path.join("_status", "testador-olho-%s.json" % nome), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(u"%s -> olho: %d ok, %d NAO sao o que o nome diz, %d com problema, %d nao julgadas (%.0fs)" % (pasta, ok, len(ruins), len(avisos), len(falhas), dt))
    for r in ruins[:10]: print(u"   ❌ %s: promete \"%s\", o modelo ve \"%s\" (%s)" % r)
    if falhas and len(falhas) == len(pngs): return 2
    return 1 if ruins else 0

if __name__ == "__main__":
    sys.exit(main())
