# -*- coding: utf-8 -*-
u"""
Folha Viva (Somando com Desenhos) — gera o `falas.json` a partir do bloco FALAS do
index.html e grava o mapa VOZOK. Mesmo padrão do UNO dos Números (app à mão):
toda frase que a voz diz mora no index entre /*FALAS-INI*/ e /*FALAS-FIM*/; aqui
calculamos a MESMA chave do motor (`chaveVoz`: djb2 em base 36 do texto
normalizado) e o `entregar.yml` grava `audio/fv_<chave>.mp3` (voz do voz.txt).

Uso: python3 _folha/gerar_falas.py   (depois: commit com [entregar _folha:<repo>])
"""
import io, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(AQUI, "index.html")


def chave(s):
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    hh = 5381
    for ch in s:
        hh = (hh * 33 + ord(ch)) & 0xFFFFFFFF
    if hh == 0:
        return "0"
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while hh:
        out = d[hh % 36] + out
        hh //= 36
    return out


html = io.open(IDX, encoding="utf-8").read()
m = re.search(r"/\*FALAS-INI\*/\s*var FALAS\s*=\s*(\{.*?\});\s*/\*FALAS-FIM\*/", html, re.S)
if not m:
    raise SystemExit("index.html sem o bloco /*FALAS-INI*/ var FALAS = {...}; /*FALAS-FIM*/")
FAL = json.loads(m.group(1))

falas, vistos = [], set()
for k in FAL:
    t = re.sub(r"\s+", " ", FAL[k]).strip()
    c = chave(t)
    if c in vistos:
        continue
    vistos.add(c)
    falas.append({"id": "fv_" + c, "texto": t})

io.open(os.path.join(AQUI, "falas.json"), "w", encoding="utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1) + "\n")
if not os.path.exists(os.path.join(AQUI, "voz.txt")):
    io.open(os.path.join(AQUI, "voz.txt"), "w", encoding="utf-8").write("pt-BR-AntonioNeural\n")

mapa = "var VOZOK = " + json.dumps({f["id"][3:]: 1 for f in falas}, separators=(",", ":")) + ";"
novo, n = re.subn(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", "/*VOZOK-INI*/" + mapa + "/*VOZOK-FIM*/", html, flags=re.S)
if n != 1:
    raise SystemExit("index.html sem as marcas /*VOZOK-INI*/ ... /*VOZOK-FIM*/")
io.open(IDX, "w", encoding="utf-8").write(novo)
print("falas.json: %d fala(s); VOZOK gravado no index.html" % len(falas))
