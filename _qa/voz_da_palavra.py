# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — A PALAVRA QUE A CRIANÇA VÊ TEM VOZ, E É A DELA  (1p)

 ⭐ DEFEITO QUE CHEGOU À SALA (21/set/2026). O Marcos trouxe o que os
    estudantes disseram: ***"na atividade do 2º ano, a máquina de trocar
    sílabas, as palavras estão sendo ditas erradas"*** e, logo depois,
    ***"tem palavras sendo ditas diferente do que é mostrado"*** ·
    ***"isso não pode acontecer em atividade nenhuma"***.

 ⚠️ O QUE ERA, e é pequeno e fundo: a chave da fala de uma palavra é o nome
    dela sem acento. **Os dois lados tiravam o acento de jeitos diferentes.**
      · quem GRAVA (`gerar_falas.py`, função `ch`) usa NFKD: `ã` vira `a`,
        `ç` vira `c` — e arquiva em `pal_aviao`, `pal_laco`;
      · quem PEDE (`chaveQuadro`, no `folhas.js`) APAGAVA a letra acentuada —
        e pedia `pal_avio`, `pal_lao`, que não existem.
    O `falar()` volta calado quando a chave não existe. Resultado medido:
    **17 palavras mudas** em três cadernos no ar — AVIÃO, CAMALEÃO, CARROÇA,
    CHORÃO, DOMINÓ, DRAGÃO, LAÇO, LEÃO, POÇO (`_troca2`), CÃO, MÃO, PÃO, PÉ,
    SABÃO, SOFÁ, CAÇA (`_sil2`) e TAMBÉM (`_nasal2`). A criança tocava o
    alto-falante e não ouvia nada — justamente nas palavras com til e cedilha,
    que são as que ela mais precisa ouvir.

 ⚠️⚠️ E JÁ TINHA SIDO CONSERTADO UMA VEZ. No `_aumdim2` existe a `chavePal()`,
    correta, com o comentário certo: *"as pontas têm de casar, senão a voz
    procura um mp3 que não existe"*. Consertei num caderno e não levei aos
    outros dezesseis. **Defeito medido em código gêmeo se conserta em TODOS os
    lugares na mesma rodada** — e é a segunda vez que a casa paga por isso.

 O QUE ELE MEDE, para cada palavra que tem sílaba gravada (`silabas.json`):
   1. a chave que o APP vai pedir existe no `FALAS`;
   2. o texto dessa fala é a PRÓPRIA palavra (e não outra);
   3. duas palavras diferentes não caem na mesma chave — senão a criança vê
      uma e ouve a outra, que é exatamente a queixa dele.

 ⚠️ O QUE ELE NÃO MEDE: se o mp3 foi gravado (isso é do `entregar.yml` e do
    carimbo) e se a voz PRONUNCIA bem (isso é o `ouvir.yml`, que escuta).
    Ele mede o encontro das pontas — que era onde estava o buraco.

 Uso:  python3 _qa/voz_da_palavra.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

# a mesma tabela que o motor usa no `chaveQuadro` — se uma mudar, a outra muda
SEMACENTO = {
    u"á": u"a", u"à": u"a", u"â": u"a", u"ã": u"a", u"ä": u"a",
    u"é": u"e", u"è": u"e", u"ê": u"e", u"ë": u"e",
    u"í": u"i", u"ì": u"i", u"î": u"i", u"ï": u"i",
    u"ó": u"o", u"ò": u"o", u"ô": u"o", u"õ": u"o", u"ö": u"o",
    u"ú": u"u", u"ù": u"u", u"û": u"u", u"ü": u"u",
    u"ç": u"c", u"ñ": u"n",
}


def chave_do_app(pasta_js, palavra):
    u"""a chave EXATAMENTE como o `chaveQuadro` daquele caderno a monta.

    ⚠️ Lê a tabela do próprio `folhas.js` em vez de supor a daqui: um caderno
    pode ficar para trás no conserto, e é justamente esse que tem de reprovar.
    """
    tabela = SEMACENTO if pasta_js is None else pasta_js
    fora = []
    for c in palavra.lower():
        if u"a" <= c <= u"z":
            fora.append(c)
        elif c in tabela:
            fora.append(tabela[c])
    return u"".join(fora)


def _tabela_do_caderno(js):
    u"""a tabela de acentos escrita no `folhas.js`; vazia se ele ainda APAGA."""
    m = re.search(r"var SEMACENTO\s*=\s*\{(.*?)\};", js, re.S)
    if not m:
        return {}
    return dict(re.findall(u'"([^"])"\\s*:\\s*"([^"])"', m.group(1)))


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/voz_da_palavra.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam_sil = os.path.join(pasta, u"silabas.json")
    cam_js = os.path.join(pasta, u"folhas.js")
    cam_html = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam_js) or not os.path.exists(cam_html):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva." % pasta)
        return 2
    if not os.path.exists(cam_sil):
        print(u"%s -> NAO SE APLICA: este caderno nao grava silaba de palavra."
              % pasta)
        return 2

    js = io.open(cam_js, encoding=u"utf-8").read()
    html = io.open(cam_html, encoding=u"utf-8").read()
    try:
        palavras = json.load(io.open(cam_sil, encoding=u"utf-8"))[u"palavras"]
    except Exception as e:                                   # noqa: BLE001
        print(u"%s -> NAO MEDI: o silabas.json nao le (%s)." % (pasta, e))
        return 2
    m = re.search(r"var FALAS = (\{.*?\});", html, re.S)
    if not m:
        print(u"%s -> NAO MEDI: nao achei o `var FALAS` no index.html." % pasta)
        return 2
    falas = json.loads(m.group(1))

    tabela = _tabela_do_caderno(js)
    mudas, trocadas, colisao = [], [], {}
    for w in sorted(palavras):
        k = u"pal_" + chave_do_app(tabela, w)
        colisao.setdefault(k, []).append(w)
        t = falas.get(k)
        if t is None:
            certa = u"pal_" + chave_do_app(SEMACENTO, w)
            mudas.append((w, k, certa if certa in falas else u""))
        # ⚠️ A COMPARAÇÃO É SEM ACENTO, e isto é lição de cinco minutos atrás:
        #    o `silabas.json` guarda a palavra JÁ sem acento (`maca`, `jacare`,
        #    `leao`) porque é dali que sai o nome do arquivo de recorte, e o
        #    `falas.json` guarda o texto que a voz lê, COM acento (`maçã.`,
        #    `jacaré.`, `leão.`). Comparando letra a letra, o portão acusava
        #    doze palavras corretas em cinco cadernos. Quem diz que são a MESMA
        #    palavra é a chave — e é exatamente por isso que a colisão de chave
        #    (logo abaixo) é a pergunta que importa.
        elif chave_do_app(SEMACENTO, t.strip().rstrip(u".")) != chave_do_app(SEMACENTO, w):
            trocadas.append((w, k, t))
    juntas = [(k, ws) for k, ws in colisao.items() if len(ws) > 1]

    print(u"%s -> a palavra que a crianca ve tem voz: %d palavra(s)"
          % (pasta, len(palavras)))
    if not mudas and not trocadas and not juntas:
        print(u"   ok: toda palavra tem a sua fala, e nenhuma cai na chave de outra.")
        return 0

    print(u"   REPROVADO:")
    for w, k, certa in mudas:
        extra = (u" — a fala EXISTE em `%s`: o acento some de um jeito aqui e "
                 u"de outro no gravador" % certa) if certa else u""
        print(u"   - %s e MUDA: o app pede `%s`, que nao existe%s"
              % (w.upper(), k, extra))
    for w, k, t in trocadas:
        print(u"   - %s pede `%s`, e essa fala DIZ %r — a crianca ve uma "
              u"palavra e ouve outra" % (w.upper(), k, t))
    for k, ws in juntas:
        print(u"   - `%s` serve a DUAS palavras (%s): uma delas vai ser dita no "
              u"lugar da outra" % (k, u", ".join(x.upper() for x in ws)))
    print(u"   Conserto: a tabela `SEMACENTO` do `folhas.js` tem de tirar o "
          u"acento do MESMO jeito que o `ch()` do `gerar_falas.py` (NFKD: "
          u"a com til vira A, c cedilha vira C) — trocar a letra, nunca apaga-la.")
    return 1


if __name__ == u"__main__":
    sys.exit(main())
