#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PROVA DE MONTAGEM DAS GAVETAS — TODA peça monta sem erro?

Nasceu de um buraco real (ago/2026): o `peca.sh` aprova a peça ISOLADA, e a
`provar_esteira.sh` monta 16 mecânicas juntas — mas **39 das 81 nunca tinham sido
MONTADAS**. Se o Marcos pega uma delas ao montar uma atividade, ela pode reprovar
no `montar.py` e ele perde a manhã. Foi assim que apareceu o `simetria`
impossível de montar (o montador lia "esquerda:" de um COMENTÁRIO e exigia o
campo).

Esta prova esboça UMA atividade com **1 fase por gaveta** (todas as 81), injeta o
cabeçalho de aferição (mesa/voz/currículo) e roda só o `montar.py` — que valida a
gaveta de cada peça. Sem navegador, sem publicar, ~5 s. Rode sempre que mexer no
`montar.py`, no `esboco.py`, no `pecas.json` ou numa gaveta de peça.

Uso:  python3 _padrao/ESQUELETO/provar_gavetas.py
Sai 0 se TODAS montam; 1 se alguma reprova (a linha do montador diz qual/porquê).
"""
import io
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PASTA = os.path.join(RAIZ, "_provagavetas")


def main():
    gav = json.load(io.open(os.path.join(AQUI, "pecas.json"),
                            encoding="utf-8"))["gavetas"]
    mecs = sorted(gav.keys())
    n = len(mecs)
    # 0) PORTÃO DO ACOPLAMENTO (estático, barato): função ou chave garblável em
    #    gaveta de conteúdo — a família que travava o jogador SÓ montado.
    ac = subprocess.run([sys.executable, os.path.join(RAIZ, "_qa", "acoplamento.py")],
                        cwd=RAIZ, capture_output=True, text=True)
    sys.stdout.write(ac.stdout)
    if ac.returncode != 0:
        print(u"prova: o portão do acoplamento reprovou (função em gaveta de "
              u"conteúdo). Conserte antes de montar.")
        return 1
    if os.path.isdir(PASTA):
        shutil.rmtree(PASTA)
    # 1) esboça 1 fase por gaveta
    r = subprocess.run([sys.executable, os.path.join(AQUI, "esboco.py"),
                        "_provagavetas", "--ano", u"3º ano", "--prefixo", "pg",
                        "--titulo", u"Prova das Gavetas", "--mascote", "nino",
                        "--mecs", ",".join(mecs), "--fases", str(n)],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        print(u"prova: o esboço reprovou:\n%s" % (r.stdout + r.stderr))
        return 1
    # 2) injeta o cabeçalho de aferição (mesa/voz/currículo), como a esteira faz
    cam = os.path.join(PASTA, "conteudo.json")
    d = json.load(io.open(cam, encoding="utf-8"))
    d["mesa"] = (u"PEDAGOGO (prova de montagem, 3º ano). NÃO é aula: 1 fase por "
                 u"peça, só para conferir que as %d gavetas montam sem erro." % n)
    d["voz"] = "masculina"
    objs = sorted(set(f.get("conceito") for f in d["fases"] if f.get("conceito")))
    d["curriculo"] = {o: u"(EF03XX00) prova de montagem — %s" % o for o in objs}
    io.open(cam, "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, indent=1))
    # 3) monta (valida a gaveta de cada peça)
    m = subprocess.run([sys.executable, os.path.join(AQUI, "montar.py"),
                        "_provagavetas"], cwd=RAIZ, capture_output=True, text=True)
    saida = (m.stdout or "") + (m.stderr or "")
    shutil.rmtree(PASTA, ignore_errors=True)
    print(u"PROVA DE MONTAGEM — %d gavetas, 1 fase cada" % n)
    if m.returncode == 0:
        print(u"   ok: TODAS as %d peças montam sem erro." % n)
        return 0
    print(u"   REPROVOU — alguma peça não monta:")
    for ln in saida.splitlines():
        if "PROBLEMA" in ln or "- " in ln or "mecanica" in ln:
            print(u"   %s" % ln.strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
