#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PROCURA NO BANCO — "isso já existe?"

O passo que economiza dinheiro de verdade: **antes de gerar qualquer imagem,
perguntar ao banco.** A cartografia gastou R$9,00 gerando 45 imagens uma a uma; e
o Jardim e a Terra dos Papagaios pagaram DUAS vezes pela mesma cana, o mesmo milho
e a mesma batata, porque ninguém sabia que a outra já existia.

Uso:
  python3 _banco/procurar.py cenoura bussola martelo
      → diz o que já existe (e o caminho para copiar) e o que falta gerar.

  python3 _banco/procurar.py --lista _gerar_imagens.json
      → lê a lista de geração e separa: já tem × precisa gerar.
        Assim a cartela só leva o que falta de verdade.
"""
import io
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDICE = os.path.join(RAIZ, "_banco", "index.json")


def simples(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def main():
    if not os.path.exists(INDICE):
        print(u"banco vazio — rode antes: python3 _banco/montar.py")
        return 2
    banco = json.load(io.open(INDICE, encoding="utf-8"))["objetos"]
    chaves = dict((simples(n), n) for n in banco)

    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "--lista":
        cam = args[1]
        dados = json.load(io.open(cam, encoding="utf-8"))
        itens = dados if isinstance(dados, list) else dados.get("imagens", [])
        pedidos = [(i.get("nome") or i.get("arquivo") or "") for i in itens] \
            if itens and isinstance(itens[0], dict) else list(itens)
    else:
        pedidos = args

    tem, falta = [], []
    for p in pedidos:
        k = simples(re.sub(r"^[a-z]{2,3}_", "", p))
        achou = chaves.get(k)
        if not achou:                       # busca por pedaço do nome
            perto = [n for kk, n in chaves.items() if k and (k in kk or kk in k)]
            achou = perto[0] if len(perto) == 1 else None
        if achou:
            tem.append((p, achou, banco[achou]))
        else:
            falta.append(p)

    print(u"BANCO: %d objeto(s) | pedido: %d" % (len(banco), len(pedidos)))
    if tem:
        print(u"\n  JA EXISTE (%d) — copie, nao gere:" % len(tem))
        for p, n, v in tem:
            print(u"    %-16s -> _banco/img/%-22s %s"
                  % (p, v["arquivo"], "(fundo transparente)" if v["transparente"] else ""))
    if falta:
        print(u"\n  PRECISA GERAR (%d):" % len(falta))
        print(u"    " + ", ".join(falta))
        print(u"\n  ⚠️ gere estes EM CARTELA (`python3 _padrao/cartela.py plano`) e depois")
        print(u"     rode `python3 _banco/montar.py` para eles entrarem no banco.")
    else:
        print(u"\n  nada a gerar: o banco cobre a lista inteira.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
