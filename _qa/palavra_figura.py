# -*- coding: utf-8 -*-
u"""
============================================================
PORTÃO — "a figura é da palavra? o texto quebrado sai inteiro?"

⚠️ DUAS LIÇÕES PAGAS (ago/2026), as duas achadas pelo MARCOS jogando, na MESMA
fase — "A letra que falta", da Oficina da Lina.

**1. A figura contava outra história.** A palavra era SOMBRA e o desenho era
`lt_canto` — um canto de sala, com uma flor. Palavras dele: *"a palavra é sombra,
porém tem uma flor em um canto de sala, está certo?"*. Não estava. E o estrago é
maior do que parece: **quem não lê responde pelo DESENHO**. Se a figura mostra
outra coisa, a fase não mede a regra — mede sorte.

Nenhum portão pegava. O `_qa/figura_certa.py` existe, mas só sabe ler
`conteudo.json` — e atividade escrita à mão não tem conteudo.json. Ou seja: o
portão certo existia e estava **cego justamente na forma como o Marcos pede as
atividades**.

**2. Entidade HTML dentro de palavra quebrada letra a letra.** O campo `esc`
(a palavra com a lacuna) é partido caractere por caractere para virar as
casinhas. Com `esc:"L&#194;_PADA"`, a criança via **L & # 1 9 4 ; _ P A D A**.
Palavras dele: *"os campos para completar estão com vários caracteres estranhos"*.
Este é o mesmo defeito que já tinha aparecido em CAMPEÃO, **na mesma lista** — eu
consertei a linha que ele apontou e deixei a irmã de baixo intacta.

O QUE ESTE PORTÃO FAZ, sem abrir navegador:
  1. **figura × palavra**: para toda entrada com `pal:` e `fig:`, o nome da
     figura tem que conter a palavra (sem acento, minúscula). `TAMBOR` →
     `lt_tambor` passa; `SOMBRA` → `lt_canto` reprova.
  2. **quebra letra a letra**: descobre quais campos o código parte com
     `.charAt(` ou `.split("")` e reprova qualquer valor desses campos que
     tenha `&` — porque `&#194;` só vira `Â` quando o texto inteiro entra no
     `innerHTML`, e não quando é partido antes.

Uso:  python3 _qa/palavra_figura.py _lina/index.html
Sai 0 se bate, 1 se não bate, 2 se não deu para medir.
============================================================
"""
import io
import re
import sys
import unicodedata


def simples(t):
    u"""minúscula, sem acento, só letras — 'LÂMPADA' -> 'lampada'"""
    t = re.sub(r"&#(\d+);", lambda m: unichr_(int(m.group(1))), t)
    t = unicodedata.normalize(u"NFD", t)
    t = u"".join(c for c in t if unicodedata.category(c) != u"Mn")
    return re.sub(r"[^a-z]", u"", t.lower())


def unichr_(n):
    try:
        return chr(n)
    except ValueError:
        return u""


def confere(arq):
    html = io.open(arq, encoding=u"utf-8").read()

    # ---------- 1) a figura e da palavra? ----------
    pares = re.findall(r'pal:\s*"([^"]+)"[^}]*?fig:\s*"([^"]+)"', html)
    ruins = []
    for pal, fig in pares:
        p, f = simples(pal), simples(fig)
        if not p:
            continue
        if p not in f and f.split(u"_")[-1] not in p:
            ruins.append((pal, fig))
    print(u"%s -> %d palavra(s) com figura propria" % (arq, len(pares)))
    if ruins:
        print(u"   !! %d FIGURA(S) QUE NAO SAO DA PALAVRA:" % len(ruins))
        for pal, fig in ruins:
            print(u"      \"%s\" mostra a figura \"%s\"" % (pal, fig))
        print(u"   quem nao le responde pelo DESENHO: com a figura errada a fase")
        print(u"   nao mede a regra, mede sorte. Trocar a figura ou a palavra —")
        print(u"   e, se trocar a palavra, manter o ASSUNTO da atividade.")

    # ---------- 2) texto quebrado letra a letra ----------
    campos = set(re.findall(r'\.(\w+)\.charAt\(', html))
    campos |= set(re.findall(r'\.(\w+)\.split\(\s*""\s*\)', html))
    campos -= {u"innerHTML", u"textContent", u"className", u"value"}
    quebrados = []
    for c in sorted(campos):
        for v in re.findall(c + r':\s*"([^"]*)"', html):
            if u"&" in v:
                quebrados.append((c, v))
    if campos:
        print(u"   campo(s) partido(s) letra a letra: %s" % u", ".join(sorted(campos)))
    if quebrados:
        print(u"   !! %d TEXTO(S) COM ENTIDADE HTML SENDO PARTIDO LETRA A LETRA:"
              % len(quebrados))
        for c, v in quebrados[:6]:
            print(u"      %s:\"%s\"  ->  a crianca ve os caracteres soltos" % (c, v))
        print(u"   `&#194;` so vira `Â` quando o texto INTEIRO entra no innerHTML.")
        print(u"   Partido antes, cada pedaco vira uma casinha. Letra literal aqui.")

    if ruins or quebrados:
        return 1
    if not pares and not campos:
        print(u"   NAO SE APLICA: sem lista `pal:`/`fig:` nem quebra por letra — nao ha palavra x figura nesta atividade. Nada a conferir.")
        return 2
    print(u"   ok: toda figura e da sua palavra e nada quebrado tem entidade")
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/palavra_figura.py <arquivo.html>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1]))
