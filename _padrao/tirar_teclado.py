# -*- coding: utf-8 -*-
u"""
============================================================
 TIRAR O TECLADO DESENHADO — so o teclado REAL fica

 ⭐ ORDEM DO MARCOS (17/set/2026): *"precisamos remover o teclado das atividades,
    deixar so a digitacao pelo teclado real, isso precisa ser trocado nos
    cadernos de sequencia didatica"*.

    Ele ja tinha dito isso em 15/set — *"pode remover o teclado das atividades,
    melhor digitar com teclado normal"* — e a ordem foi cumprida PELA METADE:
    nos cadernos do 2º ano o teclado de 41 teclas saiu e no lugar entrou a
    fileira de letras embaralhadas (ideia dele). Nos do 1º ano ele ficou.
    Este script termina o serviço.

 ⚠️⚠️ O QUE NAO SE PODE TIRAR JUNTO, e e a razao de este arquivo existir em vez
    de um `sed`: **sem o teclado desenhado, quem abre no CELULAR fica sem como
    escrever.** Nao ha teclado para tocar e nao ha teclado fisico. Medido antes
    de mexer: nao existe, em caderno nenhum, campo que chame o teclado do
    aparelho — no `_sil2` ha ate um comentario de CSS descrevendo esse campo,
    mas a regra foi apagada e o elemento nunca existiu.

    Entao a troca e DUPLA:
      sai  o teclado desenhado (39 teclas presas no pe da tela);
      entra um campo de 1 px, transparente, que ao receber FOCO faz o teclado
            DO APARELHO subir. No PC nada sobe e vale o teclado de verdade.

    ⚠️ O campo NAO pode ser `display:none`, `visibility:hidden` nem `hidden`:
       campo escondido nao recebe foco, e sem foco o teclado do celular nao
       abre. Por isso ele e `opacity:0` — invisivel e focavel.
    ⚠️ E a fonte dele e 16px: abaixo disso o Safari do iPhone DA ZOOM na pagina
       inteira quando o campo recebe foco.

 ⚠️ A LETRA VEM POR DOIS CAMINHOS, e os dois sao necessarios:
      · `keydown` no documento -> teclado de verdade, no PC da escola;
      · `input` no campo       -> teclado do aparelho, no celular (onde muitos
                                  teclados Android mandam `key: "Unidentified"`
                                  e a letra so aparece no VALOR do campo).
    E o `keydown` do documento passa a IGNORAR o que acontece com o campo em
    foco, senao cada tecla sairia DOBRADA.

 ⚠️ O QUE FICA: a fileira de letras embaralhadas do 2º ano (escolha do Marcos,
    17/set: *"a fileira FICA"* — nao e teclado, sao as letras da propria
    palavra) e o teclado DESENHADO DENTRO da folha 13 do `_abc1`, que e o
    conteudo daquela folha ("O teclado fora de ordem") e monta o proprio
    `div.teclas`, sem tocar no teclado compartilhado.

 Uso:  python3 _padrao/tirar_teclado.py <pasta> [<pasta2> ...]
 Codigos: 0 trocou · 1 nao deu · 2 nao tinha teclado
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

MARCA_HTML = u'''<div id="teclado" aria-label="Teclado de letras">'''

CAMPO = u'''<!-- ⌨️ O TECLADO DESENHADO SAIU (Marcos, 17/set/2026): *"remover o teclado das
     atividades, deixar so a digitacao pelo teclado real"*. No lugar dele fica
     ESTE CAMPO, que a crianca nunca ve mas que recebe FOCO — e e o foco que faz
     o teclado DO APARELHO abrir no celular e no tablet.
     ⚠️ Ele nao pode ser `display:none` nem `hidden`: campo escondido NAO recebe
        foco, e sem foco o teclado do aparelho nao abre. -->
<label for="tecReal" id="tecDica" class="tecdica" aria-live="polite"></label>
<input id="tecReal" type="text" autocomplete="off" autocorrect="off"
       autocapitalize="characters" spellcheck="false" aria-label="Escreva aqui">'''

CSS = u'''
/* ---- o campo que chama o TECLADO DO APARELHO (17/set/2026) ----
   ⚠️ 1 px e transparente, mas VISIVEL para o navegador: `display:none`,
      `visibility:hidden` e `hidden` tiram o foco, e sem foco o teclado do
      celular nao abre. `opacity:0` mantem o foco e some da tela.
   ⚠️ `font-size:16px` de proposito: abaixo disso o Safari do iPhone DA ZOOM na
      pagina inteira quando o campo recebe foco. */
#tecReal{position:fixed;left:-2px;bottom:0;width:1px;height:1px;opacity:0;
  border:0;padding:0;margin:0;font-size:16px;z-index:1}
.tecdica{position:fixed;left:50%;transform:translateX(-50%);bottom:10px;z-index:32;
  background:#2b2440;color:#fff;font-weight:800;font-size:clamp(13px,3.6vw,16px);
  padding:10px 16px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.28);
  display:none;max-width:92vw;text-align:center}
.tecdica.aberta{display:block}
'''

PECA_JS = u'''/* ⌨️ AQUI MORAVA O CONSTRUTOR DO TECLADO DESENHADO — 39 teclas presas no pe da
   tela. Saiu em 17/set/2026, por ordem do Marcos.
   ⚠️ O QUE NAO SUMIU JUNTO: a `digita()` continua sendo o unico caminho de
      escrita, alimentada por DOIS lugares — o `keydown` do documento (teclado
      de verdade, no PC) e o `input` do campo invisivel (teclado do aparelho, no
      celular). Sem o segundo, quem abre no telefone fica sem como escrever. */
(function(){
  var tr = document.getElementById("tecReal");
  if(!tr) return;
  /* o celular manda `input`, nao `keydown` com a letra — em muitos teclados
     Android o `key` chega como "Unidentified". Entao a letra se le do VALOR. */
  tr.addEventListener("input", function(){
    var v = tr.value || "";
    tr.value = "";
    if(!ATIVA) return;
    for(var i = 0; i < v.length; i++){
      var k = v.charAt(i).toUpperCase();
      if("ABCDEFGHIJKLMNOPQRSTUVWXYZ\\u00c1\\u00c0\\u00c2\\u00c3\\u00c9\\u00ca\\u00cd\\u00d3\\u00d4\\u00d5\\u00da\\u00dc\\u00c7".indexOf(k) > -1) digita(k);
    }
  });
  tr.addEventListener("keydown", function(ev){
    if(!ATIVA) return;
    if(ev.key === "Backspace"){ ev.preventDefault(); digita("ap"); }
    else if(ev.key === "Enter"){ ev.preventDefault(); digita("ok"); }
    else if(ev.key === "Escape"){ ev.preventDefault(); fechaAtiva(); }
  });
})();'''


def troca(pasta):
    ih = os.path.join(pasta, u"index.html")
    fj = os.path.join(pasta, u"folhas.js")
    if not (os.path.exists(ih) and os.path.exists(fj)):
        return 2, u"nao e caderno de folha viva"
    h = io.open(ih, encoding=u"utf-8").read()
    s = io.open(fj, encoding=u"utf-8").read()
    if MARCA_HTML not in h:
        return 2, u"nao tem teclado desenhado"

    # ---- 1. HTML: fora o teclado, dentro o campo --------------------------
    i = h.index(MARCA_HTML)
    j = h.index(u"</div>", h.index(u'<div id="tk">', i)) + len(u"</div>")
    j = h.index(u"</div>", j) + len(u"</div>")
    h = h[:i] + CAMPO + h[j:]
    h = h.replace(u"</style>", CSS + u"</style>", 1)

    # ---- 2. JS: ativa()/fechaAtiva()/confereSil() -------------------------
    s = s.replace(
        u'  document.getElementById("teclado").className = "aberto";',
        u'''  /* ⌨️ so o teclado REAL: da-se FOCO no campo invisivel, e e o foco que faz
     o teclado DO APARELHO subir no celular. No PC nada sobe. */
  var _tr = document.getElementById("tecReal");
  if(_tr){ _tr.value = ""; try{ _tr.focus({preventScroll: true}); }catch(e){ _tr.focus(); } }''')
    # ⚠️ A LINHA INTEIRA, e nao so o prefixo: trocar so o comeco deixava
    #    `_dicaTec("...";` — sem o parentese de fecho. Foi o erro da 1a rodada.
    s = re.sub(u'document\\.getElementById\\("tkDica"\\)\\.textContent = ([^;]+);',
               lambda m: u'_dicaTec(' + m.group(1) + u');', s)
    s = s.replace(
        u'    ATIVA = null; document.getElementById("teclado").className = "";',
        u'    ATIVA = null; _fechaTec();')
    s = s.replace(
        u'  ATIVA = null; document.getElementById("teclado").className = "";',
        u'  ATIVA = null; _fechaTec();')

    # ---- 3. o construtor do teclado sai ----------------------------------
    marca = u'(function(){\n  var tk = document.getElementById("tk");'
    if marca in s:
        a = s.index(marca)
        b = s.index(u"})();", a) + len(u"})();")
        s = s[:a] + PECA_JS + s[b:]

    # ---- 4. o keydown do documento nao dobra a letra ----------------------
    s = s.replace(
        u'  if(document.activeElement && document.activeElement.id === "nomeIn") return;',
        u'''  if(document.activeElement && document.activeElement.id === "nomeIn") return;
  /* ⚠️ Com o campo invisivel em foco a letra chega pelo `input` DELE. Se este
     ouvinte tambem escrevesse, cada tecla sairia DOBRADA. */
  if(document.activeElement && document.activeElement.id === "tecReal") return;''')

    # ---- 5. as duas ajudantes ---------------------------------------------
    s = (u'''/* ⌨️ as duas ajudantes do campo invisivel (17/set/2026) */
function _dicaTec(txt){
  var e = document.getElementById("tecDica");
  if(e){ e.textContent = txt; e.className = "tecdica aberta"; }
}
function _fechaTec(){
  var t = document.getElementById("tecReal"); if(t) t.blur();
  var e = document.getElementById("tecDica"); if(e) e.className = "tecdica";
}
''' + s)

    # ---- 6. a rolagem: sem teclado desenhado, centraliza ------------------
    if u'var tkel = document.getElementById("teclado");' in s:
        a = s.index(u'  var tkel = document.getElementById("teclado");')
        alvo = u'document.documentElement.style.setProperty("--tech"'
        if alvo in s[a:]:
            b = s.index(u"\n}", s.index(alvo, a))
            s = s[:a] + u'''  /* ⌨️ sem teclado desenhado nao ha altura para descontar; mas no celular o
     teclado DO APARELHO cobre a metade de baixo do mesmo jeito. Entao leva-se
     a casinha para o MEIO — serve nos dois casos e nao mede nada. */
  try{ cs[0].scrollIntoView({block: "center", behavior: "smooth"}); }
  catch(e){ try{ cs[0].scrollIntoView(); }catch(e2){} }''' + s[b:]

    # ⚠️ E NAO PODE SOBRAR REFERENCIA AO `#teclado`: o portao 1u reprova, e com
    #    razao — `getElementById` devolveria null. O `_roda1` tinha DUAS.
    s = s.replace(u'document.getElementById("teclado").className = "aberto";',
                  u'_fechaTec();  /* o teclado desenhado nao existe mais */')
    s = s.replace(u'document.getElementById("teclado").className = "";', u'_fechaTec();')
    io.open(ih, u"w", encoding=u"utf-8").write(h)
    io.open(fj, u"w", encoding=u"utf-8").write(s)
    return 0, u"teclado desenhado fora; campo do aparelho dentro"


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _padrao/tirar_teclado.py <pasta> [...]")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, msg = troca(pasta.rstrip(u"/"))
        print(u"%-9s -> %s" % (pasta.rstrip(u"/"), msg))
        pior = max(pior, cod) if cod != 2 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
