#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""COLHE AS FALAS QUE SÓ EXISTEM JOGANDO — e fecha o pilar sonoro.

O `falas.json` sai do `conteudo.json`, e isso resolve tudo o que está escrito
no conteúdo. Mas a peça monta frases **em tempo de jogo**, com pedaços que só
existem ali:

    "Achou as <b>" + PAL.length + "</b> palavras da horta!"
    "<b>" + (w.ac || w.p) + "</b> — era essa mesmo!"

O montador não tem como saber que "Achou as 4 palavras da horta!" vai aparecer
na tela — o número vem do próprio jogo. E foi exatamente isso que a banca
mediu: *"16 perguntas que mudam na tela sem mudar a voz — quem não lê aperta o
alto-falante e ouve outra coisa"*.

A saída não é adivinhar: é **JOGAR e anotar**. O auditor-jogador já atravessa a
atividade inteira e já sabe colher todo texto que aparece (`COLHEITA=`). Aqui a
colheita dele vira `falas.json`:

    montar → colher (joga e anota) → montar de novo → gravar a voz

⚠️ NÃO é opcional numa entrega. Sem este passo, as telas de fecho de rodada e as
   respostas de segunda volta ficam MUDAS, e a criança que ainda não lê perde
   justamente o retorno do acerto.

Uso:  python3 _padrao/ESQUELETO/colher.py <pasta>
      python3 _padrao/ESQUELETO/colher.py <pasta> --so-ver
"""
import io
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)

from montar import chave_voz, eh_fala, texto_limpo  # noqa: E402


def joga_e_anota(pasta):
    u"""roda o auditor-jogador em modo colheita e devolve o que ele viu."""
    saco = os.path.join(pasta, "_colheita.json")
    if os.path.exists(saco):
        os.remove(saco)
    amb = dict(os.environ, COLHEITA=saco)
    r = subprocess.run(["node", os.path.join(RAIZ, "_qa", "jogador.js"),
                        os.path.join(pasta, "index.html")],
                       env=amb, cwd=RAIZ, capture_output=True, text=True)
    fim = [l for l in (r.stdout or "").splitlines() if "COLHEITA" in l
           or "CHEGOU NO FIM" in l or "PRESO" in l]
    for l in fim:
        print(u"   %s" % l.strip())
    if not os.path.exists(saco):
        print(u"   o jogador nao deixou colheita — a atividade abriu?")
        return {}
    d = json.load(io.open(saco, encoding="utf-8"))
    os.remove(saco)
    # `op` sao as respostas tocaveis; `bal` sao os enunciados/baloes
    vistos = {}
    vistos.update(d.get("op") or {})
    vistos.update(d.get("bal") or {})
    return vistos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    so_ver = "--so-ver" in sys.argv
    cam = os.path.join(pasta, "falas.json")
    if not os.path.exists(cam):
        print(u"nao achei %s — rode o montador antes" % cam)
        return 2

    falas = json.load(io.open(cam, encoding="utf-8"))
    ja = set(f["id"] for f in falas)
    # ⚠️ e tambem pelo TEXTO: a mesma frase escrita no conteudo e vista em jogo
    #    nao pode virar dois mp3 (dinheiro e tempo de gravacao a toa)
    ja_txt = set(texto_limpo(f["texto"]) for f in falas)

    print(u"COLHEITA — %s" % pasta)
    vistos = joga_e_anota(pasta)

    novas = []
    for txt in sorted(vistos):
        t = texto_limpo(txt)
        if not eh_fala(t) or t in ja_txt:
            continue
        ident = "op_" + chave_voz(t)
        if ident in ja:
            continue
        ja.add(ident)
        ja_txt.add(t)
        novas.append({"id": ident, "texto": t})

    print(u"   %d texto(s) vistos em jogo | %d fala(s) novas a gravar"
          % (len(vistos), len(novas)))
    for n in novas[:8]:
        print(u"      %s" % n["texto"][:74])
    if not novas:
        print(u"   nada a acrescentar: a voz ja cobre o que aparece jogando")
        return 0
    if so_ver:
        print(u"   (--so-ver: nada foi escrito)")
        return 0

    falas.extend(novas)
    io.open(cam, "w", encoding="utf-8").write(
        json.dumps(falas, ensure_ascii=False, indent=1))
    print(u"   %s atualizado. AGORA RODE O MONTADOR DE NOVO" % cam)
    print(u"   (e o `VOZOK` do index.html sai do falas.json — sem isso o "
          u"alto-falante nao aparece)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
