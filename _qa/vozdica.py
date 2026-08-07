#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA VOZ DA DICA — "a dica falada é a mesma que está escrita?"

Pedido do Marcos (ago/2026): *"veja nos enunciados, dicas, etc: o som que é
falado tem que ser o mesmo do texto"*.

O portão 0g (`_qa/vozigual.js`) já cuida do ENUNCIADO — abre a fase, lê o balão
e compara com a narração. Mas a **dica** ficava de fora, e ela tem o mesmo
problema pela mesma razão: a criança toca em "Dica", lê uma frase na tela e
ouve outra. Foi o que aconteceu com *"De cima você vê o telhado, nunca a
porta"* numa tela de mesa, carro, cadeira e piscina — sem telhado nem porta
nenhuma.

Este portão é ESTÁTICO e por isso é barato: `montaBarra("id","texto")` diz as
duas coisas de uma vez, e o `falas.json` guarda o que a voz daquele id fala.
Basta comparar. Acento, vírgula, caixa e negrito não contam; palavra diferente
conta.

Uso:  python3 _qa/vozdica.py _naveg/index.html
Sai com 1 se alguma dica falar diferente do que está escrito.
"""
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

try:
    unichr
except NameError:
    unichr = chr

ENT = {"&#231;": u"ç", "&#225;": u"á", "&#227;": u"ã", "&#233;": u"é", "&#237;": u"í",
       "&#243;": u"ó", "&#245;": u"õ", "&#234;": u"ê", "&#224;": u"à", "&#250;": u"ú",
       "&#193;": u"Á", "&#205;": u"Í", "&#199;": u"Ç", "&#192;": u"À", "&#211;": u"Ó",
       "&#218;": u"Ú", "&#8212;": u"—", "&#8230;": u"...", "&#8593;": u"", "&#8595;": u"",
       "&#8592;": u"", "&#8594;": u""}


def limpo(s):
    u"""tira as marcas de negrito e devolve o texto como a crianca LE.

    ⚠️ a primeira versao disto tinha uma TABELA de entidades — e claro que
    faltou uma (`&#202;`, o E com circunflexo de "TRES"): o texto foi para o
    gerador de voz com o codigo cru dentro. Tabela escrita a mao sempre esquece
    um. Agora decodifica QUALQUER entidade numerica de uma vez.
    """
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"&#(\d+);", lambda m: unichr(int(m.group(1))), s)
    s = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: unichr(int(m.group(1), 16)), s)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


def chave(s):
    s = limpo(s).lower()
    s = unicodedata.normalize("NFD", s)
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^\w ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    pasta = os.path.dirname(os.path.abspath(alvo))
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)

    cam = os.path.join(pasta, "falas.json")
    if not os.path.exists(cam):
        print(u"%s -> sem falas.json: nao da para saber o que a voz diz." % alvo)
        return 1
    falas = dict((x["id"], x["texto"]) for x in json.load(io.open(cam, encoding="utf-8")))

    achados = re.findall(r'montaBarra\("([a-z0-9_]+)"\s*,\s*"((?:[^"\\]|\\.)*)"', js)

    # ⚠️ LICAO PAGA (ago/2026): este portao ficava CEGO na atividade MONTADA.
    #    Ele procura `montaBarra("id","texto")` escrito com todas as letras — o
    #    jeito da atividade feita a mao. No esqueleto, quem chama e o motor:
    #    `montaBarra(f.dicaVoz, f.dica)`, com VARIAVEIS. Resultado: "0 dica(s)
    #    conferida(s)" numa atividade com 32 dicas, e a banca dando por bom o que
    #    nao mediu. Aqui as dicas vem da lista FASES, que e onde elas moram.
    if not achados:
        crus = re.findall(r"(?:var\s+)?FASES\s*=\s*(\[[\s\S]*?\]);\s*\n", html)
        if crus:
            try:
                r = subprocess.run(
                    ["node", "-e", "console.log(JSON.stringify(%s))" % max(crus, key=len)],
                    capture_output=True, text=True, timeout=30)
                for f in (json.loads(r.stdout) if r.returncode == 0 else []):
                    if f.get("dica") and f.get("dicaVoz"):
                        achados.append((f["dicaVoz"], f["dica"]))
            except Exception:
                pass
    difs, ok, sem = [], 0, []
    for ident, texto in achados:
        voz = falas.get(ident)
        if voz is None:
            sem.append(ident)
            continue
        if chave(voz) == chave(texto):
            ok += 1
        else:
            difs.append((ident, limpo(texto), limpo(voz)))

    print(u"%s -> %d dica(s) conferida(s)" % (alvo, len(achados)))
    if sem:
        print(u"   %d dica(s) sem texto no falas.json (nao da para conferir): %s"
              % (len(sem), ", ".join(sem[:6])))
    if difs:
        print(u"   %d DICA(S) EM QUE A VOZ NAO DIZ O QUE ESTA ESCRITO:" % len(difs))
        for ident, t, v in difs[:8]:
            print(u"    - %s\n        tela: %s\n        voz : %s" % (ident, t, v))
        print(u"   conserto: regravar a dica com o texto DA TELA — a crianca le uma "
              u"frase e ouve outra.")
        return 1
    if sem:
        return 1
    print(u"   voz ok: toda dica fala exatamente o que esta escrito nela")
    return 0


if __name__ == "__main__":
    sys.exit(main())
