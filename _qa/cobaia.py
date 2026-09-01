#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""COBAIA DO MOTOR — gera uma atividade-fixture que usa TODAS as mecânicas.

Lição paga (Marcos, set/2026): os dois piores bugs do dia (o pote da estimativa
virando barra fina; o texto de "dinheiro" numa comparação de cenouras) SÓ
aparecem quando a peça roda DENTRO da atividade — na bancada, sozinha, ela passa.
Hoje esse tipo de defeito só é pego quando, por acaso, alguém monta uma atividade
que usa aquela mecânica. Se a mecânica não é usada por um tempo, o defeito dorme.

A cobaia acorda todas de uma vez: uma atividade só, com UMA fase de CADA mecânica
(em "modo exemplo" — sem `dados`, cada peça roda o exemplo dela). O
`_qa/cobaia.sh` monta ela e roda `leiaute` (layout/colapso) + `jogador-par`
(joga tudo, mede erro de JS) — assim, uma mudança no MOTOR (`pecas.js`,
`pecas.css`, `montar.py`) é testada em TODAS as mecânicas ANTES de chegar em
qualquer atividade de verdade. O pote e o dinheiro teriam sido pegos aqui, sem
depender de sorte.

Gera `_cobaia/conteudo.json`. Uso: `python3 _qa/cobaia.py` (ou `bash _qa/cobaia.sh`).
"""
import io
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PECAS_JSON = os.path.join(RAIZ, "_padrao", "ESQUELETO", "pecas.json")
DEST = os.path.join(RAIZ, "_cobaia")

# mecânicas que NÃO entram na cobaia automática e por quê (cada uma testada à
# parte, ou sem "vitória" que o jogador saiba fechar sozinho):
#   pintar/pintar-canvas/pintar-desenho/criar-desafio = PRODUÇÃO livre (a criança
#     CRIA; não há resposta certa — o jogador não tem o que fechar).
PULAR = {u"pintar", u"pintar-canvas", u"pintar-desenho", u"criar-desafio"}


def mecanicas():
    g = json.load(io.open(PECAS_JSON, encoding="utf-8")).get("gavetas") or {}
    return [k for k in sorted(g)
            if isinstance(g[k], dict) and "exemplo" in g[k] and k not in PULAR]


def build():
    mecs = mecanicas()
    fases = []
    for i, m in enumerate(mecs):
        fases.append({
            u"id": u"cb%02d" % i,
            u"mec": m,
            u"selo": m.upper().replace(u"-", u" "),
            u"conceito": u"objetivo1",
            u"enunciado": u"Fixture de motor: a mecânica <b>%s</b> no exemplo dela." % m,
            u"dica": u"Cobaia do motor — testa a peça %s dentro do motor." % m,
        })
    conteudo = {
        u"titulo": u"Cobaia do Motor",
        u"sub": u"Fixture interno — todas as mecânicas em modo exemplo",
        u"ano": u"3º ano",
        u"prefixo": u"cb",
        u"mascote": u"coruja",
        u"mascoteNome": u"Byte",
        u"voz": u"feminina",
        u"crachas": 4,
        u"fundo": u"cb_fundo.png",
        u"arte": {
            u"cenario": u"a plain neutral studio backdrop, soft even light",
            u"mascote": u"a simple friendly round owl, neutral pose",
        },
        u"mesa": (u"FIXTURE INTERNO (nao vai para a crianca): o PEDAGOGO na "
                  u"cabeceira, so para satisfazer o contrato do montador. Esta "
                  u"atividade existe para TESTAR o motor, nao para ensinar."),
        u"convite": u"<b>Cobaia do motor</b> — testando todas as peças.",
        u"abertura": u"Isto é um teste interno do motor, não uma atividade.",
        u"fim": u"Fim do teste do motor.",
        u"conceitos": {
            u"objetivo1": u"Testar cada mecânica do motor dentro da atividade montada",
        },
        u"curriculo": {
            u"objetivo1": (u"Fixture de engenharia: exercitar todas as peças do "
                           u"motor no ambiente real (integradas), para pegar o "
                           u"defeito que só existe fora da bancada."),
        },
        u"fases": fases,
    }
    return conteudo, mecs


def main():
    conteudo, mecs = build()
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    out = os.path.join(DEST, "conteudo.json")
    io.open(out, "w", encoding="utf-8").write(
        json.dumps(conteudo, ensure_ascii=False, indent=1))
    print(u"cobaia: %d mecânica(s) -> %s" % (len(mecs), out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
