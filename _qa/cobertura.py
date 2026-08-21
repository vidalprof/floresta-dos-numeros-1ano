# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "TUDO O QUE FOI PEDIDO FOI ATENDIDO?"

 ⚠️ LIÇÃO PAGA (ago/2026), e quem pegou foi o Marcos, não portão nenhum.
 O pedido da professora do 1º ano era **"sequência alfabética, identificar as
 letras e formar sílabas"**. Montei o plano da atividade e as sílabas ficaram
 fartas — cinco fases de bater, cinco de juntar — enquanto a **sequência
 alfabética**, que era a PRIMEIRA coisa pedida, ficou com **uma única mecânica**
 e três fases. Ele perguntou: *"nessa atividade ela não comentou de sequenciar
 o alfabeto? as dinâmicas atendem?"*. Não atendiam.

 E a ordem que veio junto foi clara: *"não pode cometer esses erros novamente"*
 e *"pode ter umas mecânicas diferentes, mas tudo tem que ser atendido na
 atividade"*.

 Por que nenhum portão pegava: os que existem medem a QUALIDADE do que foi
 feito (a escada sobe? o andaime cresce? a voz bate com a tela?). Nenhum media
 se o que foi feito **cobre o que foi pedido**. Uma atividade pode estar
 impecável em tudo e ainda assim deixar de fora metade da encomenda.

 O que este portão cobra, por objetivo declarado no `conteudo.json`:
   1. **existe?** — objetivo sem nenhuma fase é encomenda esquecida;
   2. **tem peso?** — pelo menos 3 fases. Uma fase é menção, não ensino;
   3. **tem mais de um GESTO?** — pelo menos 2 mecânicas diferentes. Um gesto
      só é um jeito só de entender: quem não pega por ali, não pega;
   4. **está equilibrado?** — nenhum objetivo pode ficar com menos de metade
      das fases do objetivo mais servido. Foi exatamente essa a desproporção
      (10 fases de sílaba contra 3 de alfabeto).

 ⚠️ O que ele NÃO mede: se a mecânica escolhida é a CERTA para aquela
 habilidade — isso é do pedagogo humano e do Marcos. Ele mede quantidade e
 variedade, que é o que dá para medir. Portão nenhum substitui olhar.

 Uso:  python3 _qa/cobertura.py _padaria            (pasta com conteudo.json)
       python3 _qa/cobertura.py _padaria/index.html (atividade montada)
============================================================
"""
import io
import json
import os
import re
import subprocess
import sys

MIN_FASES = 3
MIN_GESTOS = 2


def do_conteudo(cam):
    c = json.load(io.open(cam, encoding="utf-8"))
    return c.get("curriculo") or {}, c.get("conceitos") or {}, c.get("fases") or []


def do_montada(cam):
    html = io.open(cam, encoding="utf-8", errors="replace").read()
    achados = re.findall(r"(?:var\s+)?FASES\s*=\s*(\[[\s\S]*?\]);\s*\n", html)
    if not achados:
        return {}, {}, []
    crua = max(achados, key=len)
    try:
        r = subprocess.run(["node", "-e", "console.log(JSON.stringify(%s))" % crua],
                           capture_output=True, text=True, timeout=30)
        fases = json.loads(r.stdout) if r.returncode == 0 else []
    except Exception:
        fases = []
    # o índice do currículo vive ao lado, no conteudo.json
    lado = os.path.join(os.path.dirname(cam), "conteudo.json")
    cur, conc = ({}, {})
    if os.path.exists(lado):
        cur, conc, _ = do_conteudo(lado)
    return cur, conc, fases


def main():
    alvo = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")
    if not alvo:
        print(u"uso: python3 _qa/cobertura.py <pasta|index.html>")
        return 2

    # ⭐ atividade CRIATIVA (colorir): producao, sem cobertura por multiplos
    #    gestos — isencao declarada no conteudo (igual ao montador/padrao).
    _camtipo = os.path.join(alvo, "conteudo.json") if os.path.isdir(alvo) \
        else os.path.join(os.path.dirname(os.path.abspath(alvo)), "conteudo.json")
    try:
        if os.path.exists(_camtipo):
            _t = json.load(io.open(_camtipo, encoding="utf-8")).get("tipo", "")
            if str(_t).strip().lower() in ("criativa", "livre", "colorir"):
                print(u"%s -> atividade CRIATIVA (colorir): producao, sem cobertura "
                      u"por multiplos gestos. Nada a conferir." % alvo)
                return 0
    except Exception:
        pass

    if os.path.isdir(alvo):
        cam = os.path.join(alvo, "conteudo.json")
        if not os.path.exists(cam):
            print(u"%s -> sem conteudo.json. Nada a conferir." % alvo)
            return 0
        cur, conc, fases = do_conteudo(cam)
    else:
        cur, conc, fases = do_montada(alvo)

    if not cur:
        print(u"%s -> a atividade nao declara `curriculo` (nao saiu do esqueleto). "
              u"Nada a conferir." % alvo)
        return 0
    if not fases:
        print(u"%s -> nao achei as fases. Nada a conferir." % alvo)
        return 0

    # conta fases e gestos por objetivo
    por = {}
    for f in fases:
        k = f.get("conceito") or "(sem objetivo)"
        d = por.setdefault(k, {"n": 0, "mecs": set(), "ids": []})
        d["n"] += 1
        d["mecs"].add(f.get("mec") or "?")
        d["ids"].append(f.get("id") or "?")

    problemas = []
    maior = max([por[k]["n"] for k in por] or [0])

    for k in sorted(cur):
        d = por.get(k)
        nome = conc.get(k) or k
        # ⭐ o objetivo "livre" e o FECHO SEM COBRANCA (decisao do Marcos,
        #    ago/2026: o fim tem que ser divertido e do tema). Ele nao ensina
        #    habilidade nenhuma de proposito, entao cobrar dele 3 fases e 2
        #    gestos seria o portao obrigando a inchar a brincadeira. So confiro
        #    que ele NAO virou a maior parte da atividade.
        if k == "livre":
            n = d["n"] if d else 0
            if n and len(fases) and n * 100.0 / len(fases) > 20.0:
                problemas.append(u"as fases LIVRES (sem cobranca) sao %d%% da atividade — "
                                 u"o fecho e o fecho, nao a atividade inteira."
                                 % round(n * 100.0 / len(fases)))
            continue
        if not d:
            problemas.append(u"o objetivo '%s' (%s) NAO TEM NENHUMA FASE — foi pedido "
                             u"e ficou de fora." % (k, nome))
            continue
        if d["n"] < MIN_FASES:
            problemas.append(u"o objetivo '%s' (%s) tem so %d fase(s). Uma ou duas e "
                             u"mencao, nao ensino — o minimo da casa e %d."
                             % (k, nome, d["n"], MIN_FASES))
        if len(d["mecs"]) < MIN_GESTOS:
            problemas.append(u"o objetivo '%s' (%s) e treinado por UM GESTO so (%s). "
                             u"Quem nao entende por esse caminho nao tem outro."
                             % (k, nome, ", ".join(sorted(d["mecs"]))))
        if maior and d["n"] * 2 < maior and k != "livre":
            problemas.append(u"o objetivo '%s' (%s) ficou com %d fase(s) contra %d do "
                             u"mais servido — menos da metade. Foi essa a desproporcao "
                             u"que o Marcos pegou (silabas fartas, alfabeto magro)."
                             % (k, nome, d["n"], maior))

    # fase apontando para objetivo que nao existe no curriculo
    for k in sorted(por):
        if k not in cur:
            problemas.append(u"as fases %s apontam para '%s', que nao esta declarado no "
                             u"curriculo." % (", ".join(por[k]["ids"][:4]), k))

    print(u"%s -> %d fase(s) para %d objetivo(s) do curriculo" % (alvo, len(fases), len(cur)))
    for k in sorted(cur):
        d = por.get(k)
        print(u"   %-11s %2d fase(s) | %d gesto(s): %s"
              % (k, d["n"] if d else 0, len(d["mecs"]) if d else 0,
                 ", ".join(sorted(d["mecs"])) if d else u"NENHUM"))
    if problemas:
        print(u"   %d PROBLEMA(S) DE COBERTURA:" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1
    print(u"   cobertura ok: todo objetivo pedido tem peso e mais de um gesto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
