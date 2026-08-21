# -*- coding: utf-8 -*-
u"""
============================================================
QUAL WORKFLOW PUBLICA ISTO? — o portão que responde antes de eu errar

⚠️ LIÇÃO PAGA (ago/2026), e o Marcos perguntou na cara: *"por que você está
errando tanto?"*. O erro daquele minuto: acionei o `entregar.yml` para um jogo
NOVO. Esse workflow ATUALIZA um site que já existe — quem CRIA é a
`fabrica.yml`. O resultado foi um 404 na mão dele, com a turma esperando.

A regra estava escrita no `CLAUDE.md`, com todas as letras. Eu não reli: agi
pela memória. É o mesmo defeito que me fez dizer, horas antes, que a atividade
de inglês do 9º ano não existia — quando ela estava pronta e no ar.

**Escrito não basta se eu não LER na hora certa.** Então isto aqui responde a
pergunta em um comando, olhando o estado real do repositório:

    python3 _qa/publicar.py _tangram

Ele diz: já existe recado de entrega para esta pasta? então é `entregar.yml`.
Nunca foi publicada? então é `fabrica.yml` PRIMEIRO (ela cria o repositório e
liga o Pages), e só depois o `entregar.yml` serve para as próximas versões.
============================================================
"""
import io
import json
import os
import re
import unicodedata
import sys


def main():
    pasta = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")
    if not pasta or not os.path.isdir(pasta):
        print(u"uso: python3 _qa/publicar.py <pasta-da-atividade>")
        return 2
    if not os.path.exists(os.path.join(pasta, "index.html")):
        print(u"%s -> nao tem index.html. NAO MEDI." % pasta)
        return 2

    # ja houve entrega desta pasta?
    recado, destino = None, None
    if os.path.isdir("_status"):
        for f in os.listdir("_status"):
            if not f.startswith("entrega-"):
                continue
            try:
                j = json.loads(io.open(os.path.join("_status", f), encoding="utf-8").read())
            except ValueError:
                continue
            if j.get("pasta") == pasta:
                recado, destino = j, j.get("destino")

    # um nome de repositorio sugerido, a partir do titulo
    h = io.open(os.path.join(pasta, "index.html"), encoding="utf-8", errors="replace").read(4000)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    tit = re.sub(r"\s+", " ", m.group(1)).strip() if m else pasta.strip("_")
    # ⚠️ LICAO PAGA (ago/2026): jogar fora o que nao e a-z COME a letra acentuada.
    #    "vovó" virava "vov" e o nome sugerido nao batia com o repositorio de
    #    verdade (`o-tangram-da-vovo-marta`). Acento se TRANSLITERA antes.
    _t = unicodedata.normalize("NFD", tit.split("—")[0].strip().lower())
    _t = "".join(ch for ch in _t if unicodedata.category(ch) != "Mn")
    sug = re.sub(r"[^a-z0-9]+", "-", _t).strip("-")

    print(u"%s -> %s" % (pasta, tit))
    if destino:
        print(u"   JA FOI PUBLICADA em: https://vidalprof.github.io/%s/" % destino)
        print(u"   (ultima vez: %s)" % (recado.get("quando") or "?"))
        print(u"")
        print(u"   >>> USE `entregar.yml` com alvos=%s:%s" % (pasta, destino))
        print(u"       (grava a voz que falta, publica e confere no ar)")
        return 0

    print(u"   NUNCA FOI PUBLICADA — nao ha recado em _status/.")
    print(u"")
    print(u"   >>> 1) `fabrica.yml` com repo_name=%s e source_dir=%s" % (sug, pasta))
    print(u"          (ela CRIA o repositorio e liga o Pages — sem isso da 404)")
    print(u"   >>> 2) so DEPOIS o `entregar.yml` serve, para as proximas versoes")
    print(u"")
    print(u"   ⚠️ acionar `entregar.yml`/`atualizar.yml` num site que nao existe")
    print(u"      nao cria nada: o professor abre o link e leva 404.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
