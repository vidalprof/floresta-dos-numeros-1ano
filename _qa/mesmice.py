# -*- coding: utf-8 -*-
u"""MEDIDOR DE MESMICE — usamos sempre as mesmas peças? (ADVISORY, nunca reprova)

Cobrança do Marcos (ago/2026): *"temos 81 interatividades na fábrica mas usamos
sempre as mesmas, precisamos otimizar esse processo"*. Medido na estreia:
**37 das 81 já foram usadas; 44 nunca** — e um punhado carrega a carga.

Este medidor NÃO é portão da banca (não está no `auditar.sh`, sai sempre 0). É
para o Marcos VER a concentração e para me lembrar, ao montar, de puxar do
`_padrao/CARDAPIO.md` uma peça fora do núcleo habitual. Quando (e se) o Marcos
disser "pode ligar como portão", o `--strict` já reprova — aí é só chamar no
`auditar.sh`.

Uso:
  python3 _qa/mesmice.py                      # panorama da fábrica inteira
  python3 _qa/mesmice.py _solidos/conteudo.json          # uma atividade (aviso)
  python3 _qa/mesmice.py _solidos/conteudo.json --strict # idem, mas REPROVA (p/ futuro)

Regra do aviso (uma atividade): mira **>= 2 mecânicas fora do TOP-10 habitual**
da fábrica. Abaixo disso, avisa "caiu na mesmice" e sugere ⭐ do cardápio.
"""
import json
import glob
import os
import sys
from collections import Counter

TOTAL_PECAS = 81          # o catálogo (fora o MOLDE)
TOP_N = 10                # o "núcleo habitual"
MIN_FORA = 2              # uma atividade deve trazer >=2 mecânicas fora do núcleo


def _fases(cam):
    try:
        d = json.load(open(cam, encoding="utf-8"))
    except Exception:
        return []
    return d.get("fases") or []


def uso_da_fabrica(raiz="."):
    u"""conta cada mecânica em todos os _*/conteudo.json montados."""
    c = Counter()
    ativ = 0
    for cam in sorted(glob.glob(os.path.join(raiz, "_*/conteudo.json"))):
        fs = _fases(cam)
        if not fs:
            continue
        ativ += 1
        for f in fs:
            m = f.get("mec")
            if m:
                c[m] += 1
    return c, ativ


def panorama(raiz="."):
    c, ativ = uso_da_fabrica(raiz)
    tot = sum(c.values())
    usadas = len(c)
    print(u"MESMICE — panorama da fábrica")
    print(u"   %d atividade(s) montada(s) | %d fase(s)" % (ativ, tot))
    print(u"   %d de %d peças já foram usadas — %d NUNCA."
          % (usadas, TOTAL_PECAS, TOTAL_PECAS - usadas))
    if not tot:
        return 0
    print(u"   TOP-%d habitual (o núcleo que puxo por hábito):" % TOP_N)
    for m, n in c.most_common(TOP_N):
        print(u"     %-16s %3d  %4.0f%%" % (m, n, 100.0 * n / tot))
    print(u"   → abrir o _padrao/CARDAPIO.md e escolher pelo ENCAIXE; as 44 ⭐ "
          u"nunca usadas são o antídoto da mesmice.")
    return 0


def confere(cam, strict=False, raiz="."):
    fs = _fases(cam)
    if not fs:
        print(u"mesmice: %s sem fases (montou?)" % cam)
        return 2
    c, _ = uso_da_fabrica(raiz)
    top = set(m for m, _ in c.most_common(TOP_N))
    minhas = [f.get("mec") for f in fs if f.get("mec")]
    distintas = set(minhas)
    fora = sorted(distintas - top)
    print(u"%s -> %d fase(s), %d mecânica(s) distinta(s)"
          % (cam, len(minhas), len(distintas)))
    print(u"   %d fora do TOP-%d habitual: %s"
          % (len(fora), TOP_N, ", ".join(fora) if fora else "(nenhuma)"))
    if len(fora) >= MIN_FORA:
        print(u"   ok: a atividade sai da mesmice (>= %d peça(s) fora do núcleo)."
              % MIN_FORA)
        return 0
    # abaixo do mínimo: sugere ⭐ do cardápio (as que a fábrica menos usou)
    nunca = [p for p in _catalogo(raiz) if p not in c]
    print(u"   ⚠️ CAIU NA MESMICE: só %d peça(s) fora do núcleo (mira %d)."
          % (len(fora), MIN_FORA))
    if nunca:
        print(u"   experimente encaixar uma destas (nunca usadas): %s"
              % ", ".join(sorted(nunca)[:14]))
    print(u"   ver _padrao/CARDAPIO.md (peça por tipo de conteúdo).")
    return 1 if strict else 0


def _catalogo(raiz="."):
    d = os.path.join(raiz, "_padrao", "pecas")
    if not os.path.isdir(d):
        return set()
    out = set()
    for f in glob.glob(os.path.join(d, "*.html")):
        b = os.path.basename(f)[:-5]
        if b != "MOLDE":
            out.add(b)
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--strict"]
    strict = "--strict" in sys.argv
    if not args:
        return panorama()
    return confere(args[0], strict=strict)


if __name__ == "__main__":
    sys.exit(main())
