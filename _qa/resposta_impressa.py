#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a resposta está IMPRESSA no enunciado?"  (caderno de folha viva)

 ⚠️ O DEFEITO, achado em set/2026 na Roda das Sílabas — e ele JÁ ESTAVA NO AR.

    A folha dos quadradinhos mostrava assim:

         [figura de mola]
             MOLA              ← a legenda da figura
         [ ][ ] L  A           ← e a criança tinha de escrever MO

    A resposta estava impressa dois centímetros acima da pergunta. Quem já lê um
    pouco resolvia o caderno inteiro COPIANDO, sem ouvir nada — e a folha, que
    existe para medir se a criança isola o começo da palavra, media zero.

    ⚠️ E NENHUM PORTÃO VIA ISSO. O app abre, a figura carrega, o `node --check`
       passa, a fala está certa, o leiaute está certo. O defeito só existe no
       SENTIDO — e só aparece olhando a tela com a pergunta na cabeça. Foi uma
       FOTO que o pegou, não um portão. Este arquivo é para não depender disso.

    ⚠️ Vale para a LEGENDA e para qualquer texto de apoio. Foi encontrado em
       NOVE folhas do mesmo caderno de uma vez: todas herdavam o mesmo
       `figComSom`, que escrevia o nome da figura por baixo dela.

 O QUE ELE MEDE, jogando de verdade no navegador:
   para cada item ainda NÃO respondido, olha o texto VISÍVEL do item, tira o que
   é resposta (todo `button`) e o que é alvo declarado (`[data-alvo]`), e
   reprova se o que sobrar — que é enunciado, legenda, apoio — contiver a
   resposta certa que o próprio caderno declara no `RESP[id].certo`.

 ⚠️ O QUE É "ALVO" SE DECLARA NO CÓDIGO. A gaveta precisa mostrar "LA" escrito
    na testa, senão não há onde classificar; a tira da roda precisa mostrar as
    cinco sílabas, senão não há modelo. Esses ganham `data-alvo="1"`. Tudo o que
    não se declarar é tratado como enunciado — e no enunciado a resposta não
    entra. É de propósito que o padrão seja o mais severo.

 ⚠️ TEXTO INVISÍVEL NÃO CONTA, e é por isso que o conserto funciona: a legenda
    continua no HTML, escondida por `visibility`, e aparece no instante do
    acerto. O portão usa o texto que o navegador REALMENTE mostra
    (`innerText` + checagem de `visibility`), não o `textContent` do código.

 Uso:  python3 _qa/resposta_impressa.py <pasta> [porta]
 Código 0 = nenhuma resposta impressa · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import json
import os
import re
import subprocess
import sys
import time

CROMO = u"/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PW = u"/opt/node22/lib/node_modules/playwright/index.js"

JS = u"""
const { chromium } = require('%(pw)s');
const pasta = process.argv[2], porta = process.argv[3];
(async () => {
  const b = await chromium.launch({ executablePath: '%(cromo)s', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 412, height: 900 } });
  await p.goto('http://127.0.0.1:' + porta + '/' + pasta + '/index.html');
  await p.waitForTimeout(1200);
  const temPagel = await p.evaluate(() => typeof PAGEL !== 'undefined' && PAGEL.length > 1);
  if (!temPagel) { console.log(JSON.stringify({semCaderno: true})); await b.close(); return; }
  const achados = await p.evaluate(() => {
    const out = [];
    const total = PAGEL.length;
    for (let pi = 1; pi < total; pi++) {
      vaiPara(pi);
      const pag = PAGEL[pi];
      const itens = pag.querySelectorAll('[data-qa^="item-"]');
      const caixas = itens.length ? itens : [pag];
      for (const cx of caixas) {
        /* que ids desta caixa ainda não foram respondidos */
        const ids = Object.keys(RESP).filter(id => RESP[id].pag === pi && !ST.resp[id]);
        if (!ids.length) continue;
        const marca = cx.getAttribute && cx.getAttribute('data-qa');
        const meus = marca ? ids.filter(id => marca === 'item-' + id) : ids;
        if (!meus.length) continue;
        /* o texto que a criança VÊ, tirando botões e alvos declarados */
        const clone = cx.cloneNode(true);
        clone.querySelectorAll('button,[data-alvo]').forEach(e => e.remove());
        /* e tirando o que está invisível de verdade na tela */
        const escondidos = [];
        cx.querySelectorAll('*').forEach(e => {
          const st = getComputedStyle(e);
          if (st.visibility === 'hidden' || st.display === 'none' || +st.opacity === 0)
            escondidos.push((e.textContent || '').trim());
        });
        let txt = (clone.innerText || clone.textContent || '');
        for (const esc of escondidos) if (esc) txt = txt.split(esc).join(' ');
        out.push({ pi: pi, nome: NOMES[pi - 1], ids: meus,
                   certos: meus.map(id => RESP[id].certo), txt: txt,
                   /* as palavras QUE ESTE CADERNO usa — ver o filtro no Python */
                   palavras: Object.keys(PAL).map(k => PAL[k][0]) });
      }
    }
    return out;
  });
  console.log(JSON.stringify(achados));
  await b.close();
})().catch(e => { console.log(JSON.stringify({erro: String(e)})); process.exit(3); });
"""


def limpa(t):
    t = (t or u"").upper()
    for a, b in ((u"ÁÀÂÃ", u"A"), (u"ÉÊ", u"E"), (u"Í", u"I"), (u"ÓÔÕ", u"O"),
                 (u"Ú", u"U"), (u"Ç", u"C")):
        for ch in a:
            t = t.replace(ch, b)
    return t


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/resposta_impressa.py <pasta> [porta]")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    porta = sys.argv[2] if len(sys.argv) > 2 else u"8793"
    if not os.path.exists(os.path.join(pasta, u"index.html")):
        print(u"%s -> sem index.html: NAO MEDI NADA." % pasta)
        return 2
    if not os.path.exists(CROMO) or not os.path.exists(PW):
        print(u"NAO MEDI: Playwright/Chromium nao estao aqui.")
        return 2

    js = os.path.join(u"/tmp", u"_qa_resp_impressa.js")
    with open(js, u"w") as f:
        f.write(JS % {u"pw": PW, u"cromo": CROMO})
    srv = subprocess.Popen([u"python3", u"-m", u"http.server", porta],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.1)
    try:
        saida = subprocess.check_output([u"node", js, pasta, porta]).decode(u"utf-8")
    except Exception as e:
        srv.kill()
        print(u"NAO MEDI: o navegador nao abriu (%s)." % e)
        return 2
    srv.kill()
    linha = [x for x in saida.strip().split(u"\n") if x.startswith(u"[") or x.startswith(u"{")]
    if not linha:
        print(u"NAO MEDI: o navegador nao devolveu nada.")
        return 2
    dados = json.loads(linha[-1])
    if isinstance(dados, dict):
        if dados.get(u"semCaderno"):
            print(u"%s -> NAO SE APLICA: nao e caderno de folha viva (sem PAGEL)." % pasta)
            return 2
        print(u"NAO MEDI: %s" % dados.get(u"erro"))
        return 2

    erros, conferidos = [], 0
    for bloco in dados:
        fora = [w for w in re.split(r"[^\wÀ-ÿ]+", limpa(bloco[u"txt"])) if len(w) >= 3]
        for certo in bloco[u"certos"]:
            c = limpa(certo)
            if not c or u"," in certo:
                continue           # resposta que é uma lista (marcar vários)
            conferidos += 1
            # ⚠️ O PREFIXO SÓ VALE PARA PALAVRA DO CADERNO. Sem isto o portão
            #    acusa coincidência do português: o enunciado da folha 14 diz
            #    "some a LETRA com a vogal", a resposta de um item é LE, e
            #    "LETRA" começa com LE. Portão que acusa inocente é portão que
            #    se aprende a ignorar — a casa já pagou essa lição no
            #    `silaba_fonte.py`, que reprovou 21 recortes legítimos.
            doCaderno = set(limpa(x) for x in bloco.get(u"palavras", []))
            for w in fora:
                # a resposta inteira impressa, ou a PALAVRA DO CADERNO que
                # começa por ela (o caso da MOLA: resposta MO, legenda "MOLA")
                if w == c or (2 <= len(c) <= 3 and w.startswith(c) and w in doCaderno):
                    erros.append((bloco[u"pi"], bloco[u"nome"], certo, w))
                    break

    print(u"%s -> resposta impressa: %d item(ns) conferido(s) em %d folha(s)"
          % (pasta, conferidos, len(set(b[u"pi"] for b in dados))))
    if erros:
        print(u"   %d ITEM(NS) COM A RESPOSTA IMPRESSA NO ENUNCIADO:" % len(erros))
        for pi, nome, certo, w in erros[:14]:
            print(u'    - folha %d (%s): a resposta e "%s" e a tela ja mostra "%s"'
                  % (pi, nome, certo, w))
        print(u"   conserto: esconder o texto (visibility) ate o item ser respondido")
        print(u"   — ver `nomeSecreto`/`rotuloSecreto` no folhas.js da Roda — ou,")
        print(u"   se aquele texto for MESMO o alvo (a testa da gaveta, o modelo),")
        print(u'   declarar `data-alvo="1"` no elemento.')
        return 1
    print(u"   ok: em nenhum item a resposta aparece antes de a crianca responder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
