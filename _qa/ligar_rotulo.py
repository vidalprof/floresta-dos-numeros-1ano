# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO — LIGAR COM O MESMO ROTULO DUAS VEZES  (1l2)

 ⭐ DE ONDE ELE NASCEU (14/set/2026, A Coroa dos Cinco Reinos): a primeira
    versao das folhas de ligar punha TRES BICHOS num item so, e a coluna da
    direita saia com a palavra **ANIMAIS escrita tres vezes**. O motor de ligar
    casa por CHAVE DA FIGURA, nao pelo texto que aparece — entao a crianca que
    ligasse o cachorro na segunda caixa "ANIMAIS" levaria ERRO por ter acertado.

 ⚠️ E NENHUM PORTAO PEGAVA ISSO. Apareceu de raspao, porque o jogador da banca
    nao conseguiu resolver a folha e eu fui ver por que. Item de ligar com rotulo
    repetido nao e exercicio: e armadilha, e a crianca nao tem como saber.

 ⚠️ ELE NAO MEDE SE A LIGACAO ESTA CERTA — isso e o `_qa/joga_folha.js`. Aqui a
    pergunta e uma so: **dentro do mesmo item, dois pares mostram a mesma coisa
    na coluna da direita?**

 COMO MEDE: le o bloco `/*ITENS-INI*/ var ITENS = {...}` do `index.html` e
 procura os potes de LIGAR — os que tem itens no formato `{"g": [[chave,
 rotulo], ...]}`, que e o contrato do `montaLigar` na folha viva. Reprova se
 algum item repetir o `rotulo`.

 ⚠️ MUITOS-PARA-UM DE PROPOSITO: ha folhas em que o mesmo rotulo VALE para dois
    pares (o cubo e a piramide que "ficam firmes"). Quando for de proposito,
    declare em `<pasta>/LIGAR-OK.json` uma lista com os potes liberados e o
    motivo — como no HALO-OK.json. Declarado e olhado, nunca desligado.

 ⚠⚠ ELE PASSOU MESES CEGO, e quem percebeu foi a banca do decimo caderno do
    2o ano (19/set/2026): em TODO caderno de folha viva ele imprimia
    "NAO MEDI: nao achei o bloco ITENS" — e "nao medi" nao e "passou". Duas
    causas, as duas consertadas aqui:
      1. a expressao pedia `/*ITENS-INI*/ var ITENS =` COLADOS, e o esqueleto
         da folha viva tem um comentario de dez linhas entre os dois;
      2. mesmo achando, ele so entendia o formato `{"g": [[chave, rotulo]]}`,
         que e o da Coroa dos Cinco Reinos (motor). Na folha viva o pote e
         `[["c1","c2","c3"]]` e o ROTULO nem mora ali — mora num bloco de
         DADOS que o portao nao tem como adivinhar.
    O conserto da segunda foi parar de adivinhar: em folha viva ele ABRE A
    ATIVIDADE NO NAVEGADOR e le a coluna da direita como a crianca a ve
    (`[data-qa*="-d-"]`), que e a unica fonte que nao mente.

 Uso:  python3 _qa/ligar_rotulo.py <pasta>
 Codigo 0 = ok · 1 = REPROVADO · 2 = nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys


def potes_de_ligar(itens):
    u"""devolve {chave do pote: [lista de itens]} so dos potes de LIGAR."""
    fora = {}
    for chave in sorted(itens):
        lista = itens[chave]
        if not isinstance(lista, list) or not lista:
            continue
        it = lista[0]
        if not isinstance(it, dict) or not isinstance(it.get(u"g"), list):
            continue
        if not it[u"g"] or not isinstance(it[u"g"][0], list) or len(it[u"g"][0]) < 2:
            continue
        fora[chave] = lista
    return fora


JS_FOLHA = u"""
const { chromium } = require('%(pw)s');
const pasta = process.argv[2], porta = process.argv[3];
(async () => {
  const b = await chromium.launch({ executablePath: '%(cromo)s', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 412, height: 900 } });
  await p.goto('http://127.0.0.1:' + porta + '/' + pasta + '/index.html');
  await p.waitForTimeout(1200);
  const ok = await p.evaluate(() => typeof PAGEL !== 'undefined' && PAGEL.length > 1);
  if (!ok) { console.log(JSON.stringify({semCaderno: true})); await b.close(); return; }
  const out = await p.evaluate(() => {
    const r = [];
    for (let pi = 1; pi < PAGEL.length; pi++) {
      vaiPara(pi);
      const dir = PAGEL[pi].querySelectorAll('[data-qa*="-d-"]');
      if (!dir.length) continue;
      /* o rotulo como a crianca o ve: o texto, e o aria-label quando for figura */
      const rots = [].map.call(dir, e =>
        ((e.innerText || e.textContent || '').trim() || e.getAttribute('aria-label') || ''));
      r.push({ pi: pi, nome: (typeof NOMES !== 'undefined' ? NOMES[pi - 1] : ('folha ' + pi)),
               rots: rots });
    }
    return r;
  });
  console.log(JSON.stringify(out));
  await b.close();
})().catch(e => { console.log(JSON.stringify({erro: String(e)})); process.exit(3); });
"""

CROMO = u"/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PW = u"/opt/node22/lib/node_modules/playwright/index.js"


def folha_viva(pasta):
    u"""abre o caderno e confere, folha a folha, se a coluna da direita mostra a
    mesma coisa duas vezes. ⚠️ O motor de ligar casa por CHAVE, nao pelo texto:
    dois rotulos iguais fazem a crianca levar ERRO por ter acertado."""
    import subprocess, tempfile, time
    if not os.path.exists(CROMO) or not os.path.exists(PW):
        print(u"%s -> NAO MEDI: Playwright/Chromium nao estao aqui." % pasta)
        return 2
    js = os.path.join(tempfile.gettempdir(), u"_qa_ligar_rotulo.js")
    io.open(js, u"w", encoding=u"utf-8").write(JS_FOLHA % {u"pw": PW, u"cromo": CROMO})
    porta = u"8794"
    srv = subprocess.Popen([u"python3", u"-m", u"http.server", porta],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.1)
    try:
        saida = subprocess.check_output([u"node", js, pasta, porta]).decode(u"utf-8")
    except Exception as e:
        srv.kill()
        print(u"%s -> NAO MEDI: o navegador nao abriu (%s)." % (pasta, e))
        return 2
    srv.kill()
    linhas = [x for x in saida.strip().split(u"\n") if x.startswith(u"[") or x.startswith(u"{")]
    if not linhas:
        print(u"%s -> NAO MEDI: o navegador nao devolveu nada." % pasta)
        return 2
    dados = json.loads(linhas[-1])
    if isinstance(dados, dict):
        print(u"%s -> NAO MEDI: %s" % (pasta, dados.get(u"erro") or u"sem caderno"))
        return 2
    if not dados:
        print(u"%s -> NAO SE APLICA: nenhuma folha de ligar." % pasta)
        return 2
    erros, total = [], 0
    for f in dados:
        rots = [r for r in f[u"rots"]]
        total += len(rots)
        rep = sorted(set(r for r in rots if rots.count(r) > 1 and r))
        if rep:
            erros.append((f[u"pi"], f[u"nome"],
                          u" e ".join(u'"%s"' % r[:40] for r in rep)))
    print(u"%s -> ligar: %d rotulo(s) conferido(s) em %d folha(s) de ligar"
          % (pasta, total, len(dados)))
    if erros:
        print(u"   REPROVADO — a crianca leva erro por acertar:")
        for pi, nome, rep in erros[:10]:
            print(u"    x folha %d (%s) mostra %s duas ou mais vezes na coluna da direita"
                  % (pi, nome, rep))
        print(u"   conserto: um rotulo por par. O motor casa por CHAVE, nao pelo texto.")
        return 1
    print(u"   ok: nenhuma folha mostra o mesmo rotulo duas vezes.")
    return 0


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/ligar_rotulo.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam) or not os.path.exists(os.path.join(pasta, u"folhas.js")):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()

    # ---- folha viva: mede NO NAVEGADOR, que e onde o rotulo existe de verdade
    if os.path.exists(os.path.join(pasta, u"folhas.js")):
        return folha_viva(pasta)

    m = re.search(r"/\*ITENS-INI\*/.*?var\s+ITENS\s*=\s*(\{.*?\})\s*;", html, re.S)
    if not m:
        print(u"%s -> NAO MEDI: nao achei o bloco ITENS." % pasta)
        return 2
    try:
        itens = json.loads(m.group(1))
    except ValueError as e:
        print(u"%s -> NAO MEDI: o bloco ITENS nao e JSON valido (%s)." % (pasta, e))
        return 2

    potes = potes_de_ligar(itens)
    if not potes:
        print(u"%s -> NAO SE APLICA: nenhum pote de ligar (itens com `g`)." % pasta)
        return 2

    liberados = {}
    cam_ok = os.path.join(pasta, u"LIGAR-OK.json")
    if os.path.exists(cam_ok):
        try:
            liberados = json.load(io.open(cam_ok, encoding=u"utf-8"))
        except Exception as e:
            print(u"%s -> NAO MEDI: %s nao e JSON valido (%s)." % (pasta, cam_ok, e))
            return 2

    erros, olhados, total = [], [], 0
    for chave in sorted(potes):
        for i, it in enumerate(potes[chave]):
            total += 1
            rots = [par[1] for par in it[u"g"]]
            if len(set(rots)) == len(rots):
                continue
            repetidos = sorted(set(r for r in rots if rots.count(r) > 1))
            recado = (u"%s item %d mostra %s duas ou mais vezes na coluna da direita"
                      % (chave, i, u" e ".join(u'"%s"' % r for r in repetidos)))
            if chave in liberados:
                olhados.append((recado, liberados[chave]))
            else:
                erros.append(recado)

    print(u"%s -> ligar: %d item(ns) em %d pote(s) conferido(s)"
          % (pasta, total, len(potes)))
    if olhados:
        print(u"   %d item(ns) de muitos-para-um, declarados em LIGAR-OK.json:" % len(olhados))
        for r, por in olhados:
            print(u"    - %s  (%s)" % (r, por))
    if erros:
        print(u"   REPROVADO — a crianca leva erro por acertar:")
        for e in erros[:12]:
            print(u"    x %s" % e)
        print(u"   conserto: um rotulo por item. Se o muitos-para-um for de")
        print(u"   proposito, declare o pote em %s com o motivo." % cam_ok)
        return 1
    print(u"   ✓ nenhum item de ligar repete rotulo na coluna da direita")
    return 0


if __name__ == "__main__":
    sys.exit(main())
