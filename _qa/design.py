# -*- coding: utf-8 -*-
u"""
PORTÃO DE DESIGN — a peça obedece ao sistema da casa? (`_padrao/DESIGN.md`)

Ordem do Marcos (2026-09-07): apps "como os das grandes empresas: bonitos, modernos,
sem erros". O que faz um app parecer de estúdio é TUDO obedecer a um sistema só:
cores, raios, escala de letra. Este portão conta a DERIVA de cada peça (valores
fora dos tokens) e funciona como CATRACA: reprova se a deriva de uma peça CRESCEU
em relação à marca registrada em `_qa/_design_base.json`. Lapidou → `--gravar`
abaixa a marca para sempre. Peça nova nasce exigida em deriva 0.

Uso:
  python3 _qa/design.py                 # ranking + veredito (0 ok · 1 piorou · 2 não mediu)
  python3 _qa/design.py --gravar        # registra a marca de agora
  python3 _qa/design.py --peca ordenar  # o que exatamente foge numa peça
"""
import io, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PECAS = os.path.join(RAIZ, "_padrao", "pecas")
MOTOR = os.path.join(RAIZ, "_padrao", "ESQUELETO", "motor.html")
BASE = os.path.join(RAIZ, "_qa", "_design_base.json")

NEUTROS = {"#fff", "#ffffff", "#000", "#000000", "#f4efe6", "#221a12"}
RAIOS = {"8px", "12px", "16px", "22px", "999px", "50%", "0"}
LETRAS = {"12px", "13.5px", "15px", "17px", "19px", "22px", "26px", "32px"}


def tokens_do_motor():
    u"""as cores declaradas no :root do motor (os tokens)."""
    try:
        css = io.open(MOTOR, encoding="utf-8").read()
    except Exception:
        return set()
    m = re.search(r":root\{(.*?)\}", css, re.S)
    if not m:
        return set()
    return set(c.lower() for c in re.findall(r"#[0-9a-fA-F]{3,6}\b", m.group(1)))


def norm_hex(h):
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(ch * 2 for ch in h[1:])
    return h


def deriva(css, paleta):
    u"""(contagem, detalhes) do que foge ao sistema neste CSS."""
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    fora = []
    for m in re.finditer(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})\b", css):
        h = norm_hex(m.group(1))
        if h not in paleta and h not in NEUTROS:
            fora.append(("cor", m.group(1)))
    for m in re.finditer(r"border-radius\s*:\s*([^;}]+)", css):
        for v in m.group(1).split():
            v = v.strip()
            if v and v not in RAIOS and not v.startswith("var("):
                fora.append(("raio", v))
    for m in re.finditer(r"font-size\s*:\s*([0-9.]+px)", css):
        if m.group(1) not in LETRAS:
            fora.append(("letra", m.group(1)))
    return len(fora), fora


def main():
    argv = sys.argv[1:]
    gravar = "--gravar" in argv
    so = argv[argv.index("--peca") + 1] if "--peca" in argv and argv.index("--peca") + 1 < len(argv) else None
    paleta = set(norm_hex(c) for c in tokens_do_motor())
    if not paleta:
        print("design: NAO MEDI — nao achei o :root do motor")
        return 2
    if not os.path.isdir(PECAS):
        print("design: NAO MEDI — sem _padrao/pecas")
        return 2
    marcas = {}
    for f in sorted(os.listdir(PECAS)):
        if not f.endswith(".html"):
            continue
        html = io.open(os.path.join(PECAS, f), encoding="utf-8", errors="replace").read()
        css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
        n, det = deriva(css, paleta)
        marcas[f[:-5]] = n
        if so and f[:-5] == so:
            print("%s -> deriva %d" % (f[:-5], n))
            from collections import Counter
            for (tipo, v), q in Counter(det).most_common():
                print("   %-6s %-10s x%d" % (tipo, v, q))
    total = sum(marcas.values())
    if gravar:
        io.open(BASE, "w", encoding="utf-8").write(json.dumps(marcas, indent=1, sort_keys=True))
        print("design: marca gravada — %d peca(s), deriva total %d" % (len(marcas), total))
        return 0
    try:
        base = json.load(io.open(BASE, encoding="utf-8"))
    except Exception:
        base = None
    if base is None:
        io.open(BASE, "w", encoding="utf-8").write(json.dumps(marcas, indent=1, sort_keys=True))
        print("design: ESTREIA — marca gravada (%d peca(s), deriva total %d). A partir de agora, piorar reprova." % (len(marcas), total))
        return 0
    piores = [(p, marcas[p], base.get(p, 0)) for p in marcas if marcas[p] > base.get(p, 0)]
    melhores = [p for p in marcas if p in base and marcas[p] < base[p]]
    top = sorted(marcas.items(), key=lambda kv: -kv[1])[:8]
    print("design -> %d peca(s), deriva total %d (marca: %d); mais fora do sistema: %s"
          % (len(marcas), total, sum(base.values()),
             ", ".join("%s %d" % kv for kv in top)))
    if melhores:
        print("   melhorou: %s — rode `--gravar` para abaixar a marca" % ", ".join(melhores))
    if piores:
        print("   %d PECA(S) PIORARAM (mais cor/raio/letra fora do sistema que a marca):" % len(piores))
        for p, n, b in piores:
            print("    - %-22s deriva %d (era %d)  -> python3 _qa/design.py --peca %s" % (p, n, b, p))
        print("   conserto: usar os tokens do DESIGN.md (var(--texto), raio 8/12/16/22, letra da escala).")
        return 1
    print("   design ok: nenhuma peca piorou em relacao a marca")
    return 0


if __name__ == "__main__":
    sys.exit(main())
