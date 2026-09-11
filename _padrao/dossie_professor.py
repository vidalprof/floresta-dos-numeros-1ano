# -*- coding: utf-8 -*-
u"""
============================================================
 APLICA O DOSSIÊ PEDAGÓGICO num caderno de folha viva.

 Uso: python3 _padrao/dossie_professor.py <pasta> [<pasta> ...]

 Injeta quatro coisas, sempre entre marcas, sempre idempotente (rodar de novo
 SUBSTITUI o bloco antigo em vez de duplicar):

   1. o CSS da janela do dossiê          -> index.html, antes de </style>
   2. a janela em si                     -> index.html, antes de </body>
   3. o botão no menu do professor       -> index.html, dentro de #menuProf
   4. `var CURRICULO = {...}`            -> index.html, depois de `var NOMES`
   5. o código de `_padrao/dossie-professor.js`    -> fim de folhas.js

 O CONTEÚDO do item 4 vem do `<pasta>/curriculo.json`, que é a fonte da
 verdade e o que o portão `_qa/pedagogo.py` confere contra o currículo.
============================================================
"""
import io
import json
import os
import re
import sys

CSS = u"""/*<dossie-css>*/
#dossie{display:none;position:fixed;inset:0;z-index:70;background:rgba(20,16,45,.72);
  align-items:center;justify-content:center;padding:12px}
#dossie.aberto{display:-webkit-box;display:-ms-flexbox;display:flex}
#dossie .cx{background:#fff;border:4px solid #6d5ae6;border-radius:20px;padding:14px;
  max-width:720px;width:100%;max-height:88vh;display:flex;flex-direction:column}
#dossie h3{margin:0 0 6px;color:#6d5ae6;font-size:20px}
#dsCorpo{overflow:auto;text-align:left;font-size:13px;line-height:1.5;color:var(--texto,#1e2334)}
#dsCorpo table{border-collapse:collapse;width:100%;margin:8px 0}
#dsCorpo th,#dsCorpo td{border:1px solid #d9ddf2;padding:6px 8px;text-align:left;vertical-align:top}
#dsCorpo th{background:#eceefa;color:var(--texto2,#2c3350)}
#dsCorpo .dobj{display:block;margin-top:4px;font-size:11.5px;color:var(--texto3,#3b4064)}
#dsCorpo .dfonte{margin:0 0 6px}
#dsCorpo .dsub{margin:12px 0 4px}
#dsCorpo .dtxt{margin:0}
#dsCorpo .descada,#dsCorpo .dev{margin:4px 0 0 18px;padding:0}
#dossie #dsFechar{margin-top:10px;min-height:46px}
.bdossie{display:block;width:100%;margin-top:10px;min-height:46px}
/*</dossie-css>*/"""

JANELA = u"""<!--<dossie-html>-->
<div id="dossie" role="dialog" aria-label="Dossiê pedagógico" aria-modal="true">
  <div class="cx">
    <h3>Dossiê pedagógico</h3>
    <div id="dsCorpo"></div>
    <button class="bt cinza" id="dsFechar">Fechar</button>
  </div>
</div>
<!--</dossie-html>-->"""

BOTAO = (u'<!--<dossie-bt>--><button class="bt" id="bDossie">'
         u'Dossiê pedagógico (currículo da rede)</button><!--</dossie-bt>-->')


def troca(txt, marca, novo, onde):
    u"""põe `novo` entre as marcas; se não houver marcas, insere antes de `onde`."""
    ini, fim = marca
    if ini in txt:
        return re.sub(re.escape(ini) + u".*?" + re.escape(fim), lambda _: novo,
                      txt, flags=re.S)
    if onde not in txt:
        raise SystemExit(u"não achei onde encaixar (%s)" % onde)
    return txt.replace(onde, novo + u"\n" + onde, 1)


def aplica(pasta):
    pasta = pasta.rstrip("/")
    cam = os.path.join(pasta, "curriculo.json")
    if not os.path.exists(cam):
        print(u"%s -> sem curriculo.json: nada a injetar" % pasta)
        return 1
    dados = json.load(io.open(cam, encoding="utf-8"))

    ih = os.path.join(pasta, "index.html")
    t = io.open(ih, encoding="utf-8").read()
    t = troca(t, (u"/*<dossie-css>*/", u"/*</dossie-css>*/"), CSS, u"</style>")
    # ⚠️ ANTES do <script src="folhas.js">, nunca antes de </body>. O código do
    #    dossiê amarra o botão Fechar e o clique no fundo no momento em que
    #    carrega; se a janela ainda não existisse no DOM, os dois sairiam nulos e
    #    o dossiê abriria SEM COMO FECHAR — e no print isso não aparece.
    t = troca(t, (u"<!--<dossie-html>-->", u"<!--</dossie-html>-->"), JANELA,
              u'<script src="folhas.js"></script>')
    t = troca(t, (u"<!--<dossie-bt>-->", u"<!--</dossie-bt>-->"), BOTAO,
              u'<button class="bt cinza" id="mpFechar">')

    dec = (u"/*<dossie-dados>*/\nvar CURRICULO = " +
           json.dumps(dados, ensure_ascii=False, indent=1) +
           u";\n/*</dossie-dados>*/")
    if u"/*<dossie-dados>*/" in t:
        t = re.sub(re.escape(u"/*<dossie-dados>*/") + u".*?" +
                   re.escape(u"/*</dossie-dados>*/"), lambda _: dec, t, flags=re.S)
    else:
        m = re.search(r"^var NOMES = .*?\];$", t, re.M | re.S)
        if not m:
            raise SystemExit(u"%s: não achei `var NOMES`" % pasta)
        t = t[:m.end()] + u"\n" + dec + t[m.end():]
    io.open(ih, "w", encoding="utf-8").write(t)

    fj = os.path.join(pasta, "folhas.js")
    j = io.open(fj, encoding="utf-8").read()
    codigo = io.open("_padrao/dossie-professor.js", encoding="utf-8").read().rstrip()
    bloco = u"/*<dossie-js>*/\n" + codigo + u"\n/*</dossie-js>*/\n"
    if u"/*<dossie-js>*/" in j:
        j = re.sub(re.escape(u"/*<dossie-js>*/") + u".*?" +
                   re.escape(u"/*</dossie-js>*/") + u"\n?", lambda _: bloco, j, flags=re.S)
    else:
        j = j.rstrip() + u"\n\n" + bloco
    io.open(fj, "w", encoding="utf-8").write(j)

    print(u"%s -> dossiê injetado (%d objetivos)" % (pasta, len(dados["objetivos"])))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _padrao/dossie_professor.py <pasta> [<pasta> ...]")
        sys.exit(2)
    ruim = 0
    for p in sys.argv[1:]:
        ruim |= aplica(p)
    sys.exit(ruim)
