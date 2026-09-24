# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 0w — `cmd; rc=$?` DENTRO DE `shell: bash -e` MATA O PASSO

 NASCEU DE UM DEFEITO QUE PAROU A FABRICA INTEIRA (24/set/2026). Duas entregas
 seguidas do 3o ano terminaram com o carimbo em `"estado":"rodando"`: o
 `entregar.yml` gravava as vozes, conferia a pronuncia, guardava tudo no repo —
 e NAO PUBLICAVA. O site continuava servindo a versao velha e o workflow
 terminava em "failure" sem uma linha dizendo o que havia de errado com o
 caderno. Nao havia nada errado com o caderno. A linha era esta:

     python3 _qa/voz_gravada.py "$p"; c=$?

 Os passos do Actions rodam com `shell: bash -e`. O `;` separa DOIS comandos, e
 o `set -e` derruba o passo no primeiro que devolve != 0 — antes de `c=$?`
 existir. Quem escreve assim ACHA que esta guardando o codigo para decidir
 depois; o que esta fazendo e garantir que nunca vai decidir.

 E o estrago foi grande porque o `entregar.yml` ACRESCENTA `_painel` a toda
 lista de entrega: o painel nao tem `falas.json`, o portao devolvia 2 ("nao
 medi") no ULTIMO alvo, e TODA corrida morria ali.

 ⚠️ A LICAO JA ESTAVA ESCRITA no proprio `entregar.yml`, num passo anterior
    ("o `|| rc=$?` protege"). Foi paga de novo no passo seguinte, escrito um mes
    depois. **Licao registrada num passo nao protege o passo vizinho** — por
    isso ela virou portao.

 A FORMA CERTA, e as tres que funcionam:
     rc=0; cmd || rc=$?
     if cmd; then rc=0; else rc=$?; fi
     set +e; cmd; rc=$?; set -e

 ⚠️ O QUE ELE NAO MEDE: um `cmd; rc=$?` dentro de um passo que declare outro
    shell (`shell: bash` sem `-e`, `shell: python`) e legitimo. Por isso ele
    olha o `shell:` do passo e so cobra quem esta em `bash -e` — que e o
    PADRAO do Actions quando nada e declarado.

 Uso:  python3 _qa/bash_e.py [<pasta com os workflows>]
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# a armadilha: um comando qualquer, `;`, e a captura do codigo de saida.
# ⚠️ `^\s*\w+=\$\?` (o `rc=$?` sozinho numa linha) e SEGURO e nao entra aqui:
#    ali o comando anterior ja terminou a linha dele.
ARMADILHA = re.compile(r"[^;&|\s][^;&|]*;\s*\w+=\$\?")


def passos(texto):
    u"""Quebra o yml em passos (`- name:` / `- id:`) e devolve
    [(linha_inicial, linhas do passo)]. Quebra boba de proposito: o que
    importa e saber qual `shell:` vale para cada linha."""
    linhas = texto.split(u"\n")
    marcas = [i for i, l in enumerate(linhas)
              if re.match(r"\s*-\s+(name|id|uses|run):", l)]
    saida = []
    for n, ini in enumerate(marcas):
        fim = marcas[n + 1] if n + 1 < len(marcas) else len(linhas)
        saida.append((ini, linhas[ini:fim]))
    return saida


def olha(cam):
    texto = io.open(cam, encoding=u"utf-8").read()
    achados = []
    for ini, bloco in passos(texto):
        junto = u"\n".join(bloco)
        m = re.search(r"^\s*shell:\s*(.+)$", junto, re.M)
        # o padrao do Actions para `run:` e `bash -e {0}`
        shell = (m.group(1).strip() if m else u"bash -e")
        if u"bash" not in shell or u"-e" not in shell:
            continue
        dentro = False
        for k, l in enumerate(bloco):
            if re.match(r"\s*run:\s*\|", l):
                dentro = True
                continue
            if not dentro:
                continue
            corpo = l.split(u"#")[0]
            if ARMADILHA.search(corpo):
                achados.append((ini + k + 1, l.strip()))
    return achados


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else u".github/workflows"
    if not os.path.isdir(raiz):
        print(u"NAO MEDI: nao achei a pasta `%s`." % raiz)
        return 2
    arquivos = sorted(f for f in os.listdir(raiz) if f.endswith((u".yml", u".yaml")))
    if not arquivos:
        print(u"NAO MEDI: nenhum workflow em `%s`." % raiz)
        return 2
    ruins, vistos = [], 0
    for f in arquivos:
        vistos += 1
        for linha, txt in olha(os.path.join(raiz, f)):
            ruins.append((f, linha, txt))
    print(u"bash -e: %d workflow(s) conferido(s)" % vistos)
    if not ruins:
        print(u"   ok: nenhum `cmd; rc=$?` dentro de passo com `bash -e`.")
        return 0
    print(u"   %d LINHA(S) QUE DERRUBAM O PASSO EM SILENCIO:" % len(ruins))
    for f, linha, txt in ruins:
        print(u"    x %s:%d" % (f, linha))
        print(u"        %s" % txt[:110])
    print(u"   conserto: `rc=0; cmd || rc=$?` (ou `if cmd; then ... else rc=$?; fi`).")
    print(u"   Com `;` o `set -e` mata o passo ANTES de a variavel existir — e o")
    print(u"   workflow termina em failure sem dizer o que estava errado.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
