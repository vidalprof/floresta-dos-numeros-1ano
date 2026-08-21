#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""MONTA O BANCO DE IMAGENS — o que já existe não se gera de novo.

Pedido do Marcos (ago/2026): *"poderíamos ter uma fábrica de imagens, um banco de
imagens para agilizar"* e, logo depois: *"vamos fazer tudo para automatizar, e
todas as geradas novas irão para o banco"*.

A prova de que precisava: o Jardim tem `jd_cana`, `jd_milho`, `jd_batata`; a Terra
dos Papagaios tem `nv_cana`, `nv_milho`, `nv_batata`. **A mesma cana, o mesmo
milho e a mesma batata, gerados duas vezes** — e pagos duas vezes. São 611 imagens
no acervo, e nenhuma delas era pesquisável antes deste arquivo.

⚠️ A DIVISÃO QUE FAZ O BANCO NÃO BRIGAR COM A REGRA DELE
   Ele foi taxativo: *"nunca copiar avatares, sempre ser temático, nunca repetir o
   avatar, sempre novo e temático"* — pegou os brotinhos do Jardim reaproveitados
   no céu estrelado do Órbi. Então:
     · VAI para o banco  → OBJETO NEUTRO. Cenoura, bússola, roda, martelo, sol.
       Uma cenoura é uma cenoura em qualquer atividade: não é tema, é vocabulário.
     · NÃO vai           → ARTE DE TEMA. Mascote (base/fala/pisca/feliz), avatares
       (`_cr1..6`), cenários e fundos (`.jpg`), medalha, verso de carta, capa.
   O portão `_qa/arte_propria.py` continua reprovando cópia entre atividades; o
   que vem do banco ele passa a aceitar (o índice diz quais são).

Uso:
  python3 _banco/montar.py            → varre tudo e (re)monta o banco
  python3 _banco/montar.py --so-ver   → só mostra o que entraria, não copia
"""
import hashlib
import io
import json
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "_banco", "img")
INDICE = os.path.join(RAIZ, "_banco", "index.json")

# pastas que não são atividade de criança
# ⚠️ "_banco" TEM que ficar de fora: senão a varredura lê a própria pasta de
#    destino e tenta copiar cada arquivo sobre ele mesmo (SameFileError).
FORA = {"_banco", "_site", "_agenda", "_educaverso", "_kit", "_kenney", "_estudio", "_2d",
        "_anim", "_lab", "_voxel", "_painel", "_painel-prof", "_portal", "_trilha",
        "_recuperado", "_novo", "_pub_aventura", "_pub_confeitaria"}

# ARTE DE TEMA — nunca entra no banco (regra do Marcos)
TEMA = re.compile(
    r"(_base|_fala|_pisca|_feliz|_festa|_pensa|_triste|_ok|_acena|_comemora)\.png$"
    r"|_cr\d\.png$"                                                  # avatares
    r"|^med[_-]|_med\.png$|medal"                                    # medalha
    r"|_fundo|_capa|^capa|_cena|_verso|_recado|_horizonte"           # cenario/moldura
    r"|^masc[-_]|^icon[-_]|^ilha[-_]|^emblema[-_]|^selo[-_]"         # identidade do app
    r"|^recompensa[-_]|^trofeu"                                      # premio (e do tema)
    # ⚠️ MASCOTE PELO NOME. O `nara_acena` e o `fagulha_comemora` passaram na
    #    primeira varredura porque a pose nao estava na lista de sufixos. Mascote
    #    e a cara da atividade: nunca se reaproveita (regra do Marcos, que pegou
    #    os brotinhos do Jardim dentro do ceu estrelado do Orbi).
    r"|^(nara|fagulha|byte|broto|nico|orbi|teo|juca|bento|clique|zeze|owl)([-_.]|$)"
    r"|\.jpg$|\.jpeg$"                                               # cenario largo
)

# o prefixo da atividade (jd_, mp_, nv_...) sai do nome: no banco a coisa se
# chama pelo que ELA E, nao pela atividade onde nasceu.
PREFIXO = re.compile(r"^[a-z]{2,3}_")


def alfa(cam):
    u"""Tem fundo transparente? (é o que decide se dá para pôr sobre qualquer cena)"""
    try:
        from PIL import Image
        im = Image.open(cam)
        if im.mode not in ("RGBA", "LA", "P"):
            return False
        im = im.convert("RGBA")
        # canto superior esquerdo transparente é o sinal barato e confiável
        return im.getpixel((0, 0))[3] < 20
    except Exception:
        return False


def main():
    so_ver = "--so-ver" in sys.argv
    banco = {}
    vistos = {}
    pulados = {"tema": 0, "repetida": 0}

    pastas = sorted(d for d in os.listdir(RAIZ)
                    if d.startswith("_") and d not in FORA
                    and os.path.isdir(os.path.join(RAIZ, d, "img")))

    for pasta in pastas:
        dimg = os.path.join(RAIZ, pasta, "img")
        for arq in sorted(os.listdir(dimg)):
            if not arq.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            cam = os.path.join(dimg, arq)
            if TEMA.search(arq):
                pulados["tema"] += 1
                continue
            sha = hashlib.sha1(io.open(cam, "rb").read()).hexdigest()[:16]
            if sha in vistos:
                pulados["repetida"] += 1
                banco[vistos[sha]]["tambem_em"].append(pasta)
                continue
            nome = PREFIXO.sub("", arq)
            base, ext = os.path.splitext(nome)
            # dois objetos diferentes com o mesmo nome: desempata pela atividade
            n = base
            k = 2
            while n in banco:
                n = "%s-%d" % (base, k)
                k += 1
            vistos[sha] = n
            banco[n] = {
                "arquivo": n + ext,
                "sha": sha,
                "origem": "%s/img/%s" % (pasta, arq),
                "tambem_em": [],
                "transparente": alfa(cam),
                "bytes": os.path.getsize(cam),
            }
            if not so_ver:
                if not os.path.isdir(DEST):
                    os.makedirs(DEST)
                shutil.copy2(cam, os.path.join(DEST, n + ext))

    if not so_ver:
        io.open(INDICE, "w", encoding="utf-8").write(
            json.dumps({"objetos": banco}, ensure_ascii=False, indent=1, sort_keys=True))

    transp = sum(1 for v in banco.values() if v["transparente"])
    reaproveitadas = sum(1 for v in banco.values() if v["tambem_em"])
    print(u"BANCO DE IMAGENS — %d pasta(s) varrida(s)" % len(pastas))
    print(u"  %d objeto(s) neutro(s) no banco  (%d com fundo transparente)"
          % (len(banco), transp))
    print(u"  %d arte(s) de TEMA fora do banco (mascote, avatar, cenario, medalha)"
          % pulados["tema"])
    print(u"  %d arquivo(s) que eram a MESMA imagem ja vista" % pulados["repetida"])
    if reaproveitadas:
        print(u"  %d objeto(s) que ja aparecem em MAIS DE UMA atividade:" % reaproveitadas)
        for n, v in sorted(banco.items()):
            if v["tambem_em"]:
                print(u"    %-18s %s + %s" % (n, v["origem"].split("/")[0],
                                              ", ".join(v["tambem_em"])))
    if so_ver:
        print(u"  (--so-ver: nada foi copiado)")
    else:
        print(u"  indice em _banco/index.json  |  arquivos em _banco/img/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
