# -*- coding: utf-8 -*-
u"""
============================================================
O ÍNDICE DAS ATIVIDADES — a cura do "isso a gente já fez"

⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem cobrou: *"vc já tinha feito, pq
não lembra?"*. Ele perguntou pela atividade de inglês do 9º ano; eu procurei por
"inglês" e "english", não achei, e respondi que **não existia**. Existia: é a
*RIGHT NOW — Flagra na Cidade*, pasta `_agora`, 33 fases, no ar desde 12/08.
Nenhuma das palavras que procurei aparece no nome dela — o assunto mora DENTRO
do `conteudo.json`. E, pior: eu tinha listado o `_status/` na mesma sessão, com
o `entrega-right-now-flagra-na-cidade.json` na minha frente.

**Eu começo cada sessão sem memória: só sei o que está escrito.** Mas escrito
não basta se estiver escrito onde eu não procuro. Este programa varre TODAS as
pastas de atividade e escreve o `ATIVIDADES.md` na raiz — assunto, ano, número
de fases, se está no ar e onde. É a primeira coisa a ler quando ele perguntar
"e a atividade de X?".

Uso:  python3 _qa/indice.py          (escreve ATIVIDADES.md)
      python3 _qa/indice.py ingles   (procura por assunto/ano/título/pasta)
============================================================
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from pastas import e_atividade
except ImportError:
    def e_atividade(n):
        return n.startswith("_") and os.path.isdir(n)


def le(pasta):
    d = {"pasta": pasta, "titulo": "", "ano": "", "fases": 0, "assunto": "",
         "repo": "", "noar": "", "quando": "", "bruto": ""}
    cj = os.path.join(pasta, "conteudo.json")
    if os.path.exists(cj):
        try:
            c = json.loads(io.open(cj, encoding="utf-8").read())
            d["titulo"] = c.get("titulo") or ""
            d["ano"] = c.get("ano") or ""
            d["fases"] = len(c.get("fases") or [])
            # ⚠️ o assunto NAO esta num campo fixo: no _agora os objetivos vivem
            #    dentro das fases, nao no topo. Procurar campo a campo falhou
            #    exatamente no caso que originou este portao. Le-se o ARQUIVO
            #    INTEIRO — quem procura assunto nao pode depender do formato.
            bruto = io.open(cj, encoding="utf-8", errors="replace").read()
            d["bruto"] = re.sub(r"\s+", " ", bruto)
            objs = re.findall(r'"objetivo\d*"\s*:\s*"([^"]{20,})"', bruto)
            d["assunto"] = re.sub(r"\s+", " ", " ".join(objs))[:400]
        except ValueError:
            pass
    ih = os.path.join(pasta, "index.html")
    if not d["titulo"] and os.path.exists(ih):
        h = io.open(ih, encoding="utf-8", errors="replace").read(4000)
        m = re.search(r"<title>(.*?)</title>", h, re.S)
        if m:
            d["titulo"] = re.sub(r"\s+", " ", m.group(1)).strip()
    if not d["ano"] and d["titulo"]:
        m = re.search(r"(\d)\s*º?\s*ano", d["titulo"])
        if m:
            d["ano"] = m.group(1) + "º ano"
    return d


def status():
    s = {}
    if not os.path.isdir("_status"):
        return s
    for f in os.listdir("_status"):
        if not f.startswith("entrega-") or not f.endswith(".json"):
            continue
        try:
            j = json.loads(io.open(os.path.join("_status", f), encoding="utf-8").read())
            s[j.get("pasta", "")] = j
        except ValueError:
            pass
    return s


def main():
    busca = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    st = status()
    linhas = []
    for p in sorted(os.listdir(".")):
        if not e_atividade(p) or not os.path.exists(os.path.join(p, "index.html")):
            continue
        d = le(p)
        j = st.get(p) or {}
        d["repo"] = j.get("destino", "")
        d["noar"] = "sim" if j.get("noar") else ""
        d["quando"] = (j.get("quando") or "")[:10]
        linhas.append(d)

    if busca:
        achou = [d for d in linhas
                 if busca in (d["pasta"] + " " + d["titulo"] + " " + d["ano"] + " " +
                              d["assunto"] + " " + d["repo"] + " " + d["bruto"]).lower()]
        if not achou:
            print(u"nada com '%s'. ⚠️ isto NAO quer dizer que nao existe:" % busca)
            print(u"procure tambem pelo NOME da historia, nao so pelo assunto.")
            return 1
        for d in achou:
            print(u"%-12s %-38s %-8s %2d fase(s)  %s"
                  % (d["pasta"], d["titulo"][:38], d["ano"], d["fases"],
                     (u"no ar: https://vidalprof.github.io/%s/" % d["repo"]) if d["repo"] else u""))
        return 0

    out = [u"# 📇 ÍNDICE DAS ATIVIDADES — o que já existe\n",
           u"> Gerado por `python3 _qa/indice.py`. **Ler ANTES de dizer que algo não",
           u"> existe.** Nasceu de uma cobrança do Marcos: eu disse que a atividade de",
           u"> inglês do 9º ano não existia, e ela estava pronta e no ar — o nome dela",
           u"> é *RIGHT NOW — Flagra na Cidade*, e nem \"inglês\" nem \"english\" aparecem",
           u"> nele. **O assunto mora dentro do `conteudo.json`, não no nome da pasta.**\n",
           u"| pasta | atividade | ano | fases | no ar |",
           u"|---|---|---|---|---|"]
    for d in sorted(linhas, key=lambda x: (x["ano"], x["pasta"])):
        link = (u"[%s](https://vidalprof.github.io/%s/)" % (d["repo"], d["repo"])) if d["repo"] else u"—"
        out.append(u"| `%s` | %s | %s | %s | %s |"
                   % (d["pasta"], d["titulo"] or u"(sem título)", d["ano"] or u"—",
                      d["fases"] or u"—", link))
    out.append(u"\n## O que cada uma ENSINA (o assunto, para procurar por ele)\n")
    for d in sorted(linhas, key=lambda x: x["pasta"]):
        if d["assunto"]:
            out.append(u"- **`%s` — %s**: %s\n" % (d["pasta"], d["titulo"], d["assunto"][:300]))
    io.open("ATIVIDADES.md", "w", encoding="utf-8").write(u"\n".join(out) + u"\n")
    print(u"ATIVIDADES.md escrito: %d atividade(s), %d no ar"
          % (len(linhas), len([d for d in linhas if d["noar"]])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
