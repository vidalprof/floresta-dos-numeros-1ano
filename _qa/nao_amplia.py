# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — A FIGURA NUNCA É MOSTRADA MAIOR QUE O ARQUIVO  (1i9)

 ⭐ REGRA DO MARCOS, 14/set/2026: ***"procure na internet, nada de imagem
    gerada por IA, utilize das atividades"*** — e, junto com ela, a saída
    honesta quando a internet não dá versão maior: **mostrar a figura no
    tamanho dela. Nunca ampliar, nunca gerar.**

 ⚠️ POR QUE ELE EXISTE — medido em 21/set/2026, e é uma regra da casa que
    tinha CÓDIGO e não tinha CONTA. O guarda `naoAmplia()` foi escrito para o
    esqueleto e nasceu junto com os cadernos novos; os VINTE E TRÊS cadernos
    anteriores nunca o receberam e foram ao ar sem ele. Resultado: nove
    cadernos mostravam a mesma faca de 260x71 px esticada até **1,80x**, e o
    anzol do `_ort5`, que tem 35x74 px no arquivo, aparecia a 59x124 px.
    Quem pegou foi o `leiaute_mao.js`, que abre o navegador e mede — dez
    minutos por caderno. Este portão faz a mesma pergunta em MILISSEGUNDOS,
    lendo o texto: o guarda existe? ele está amarrado em toda figura?

 ⚠️ O QUE ELE MEDE, e são três coisas:
    1. a função `naoAmplia` existe no `index.html`;
    2. ela segura os DOIS lados (largura e altura) e a largura com
       `min(100%, ...)` — sem isso o estilo de linha vence o `max-width:100%`
       da folha de estilo e a figura ESTOURA a lateral da tela no celular
       (medido no `_casa1`, folha 19, no dia em que este portão nasceu);
    3. toda figura desenhada — as de `img()` e as da CAPA (`capfig`) — chama
       o guarda no `onload`.

 ⚠️ O QUE ELE NÃO MEDE: se a figura, mostrada no tamanho dela, ficou GRANDE o
    bastante para a criança ver. Isso é juízo, e é do Marcos. Ele também não
    mede a nitidez em si — quem faz isso é a regra de resolução do
    `_qa/leiaute_mao.js`, que abre o navegador. Este aqui é o pré-voo: pega o
    erro barato antes de gastar os dez minutos da banca.

 Uso:  python3 _qa/nao_amplia.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não se aplica
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/nao_amplia.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam_html = os.path.join(pasta, u"index.html")
    cam_js = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(cam_js) or not os.path.exists(cam_html):
        print(u"%s -> NAO SE APLICA: nao ha folhas.js (nao e folha viva)." % pasta)
        return 2

    html = io.open(cam_html, encoding=u"utf-8").read()
    js = io.open(cam_js, encoding=u"utf-8").read()
    print(u"%s -> a figura nunca e mostrada maior que o arquivo" % pasta)

    faltas = []

    # 1 — o guarda existe?
    if u"function naoAmplia" not in html:
        print(u"   REPROVADO: o guarda `naoAmplia()` NAO existe neste caderno.")
        print(u"   Sem ele o teto da figura e so o `clamp` do CSS, que nao sabe")
        print(u"   quantos pixels o arquivo tem — e um recorte de 71 px de altura")
        print(u"   sai a 104 px e borrado.")
        print(u"   Conserto: copiar a funcao do `_padrao/FOLHA-VIVA/index.html`")
        print(u"   e amarra-la no `onload` de toda figura.")
        return 1

    # 2 — ela segura os dois lados, e a largura sem atropelar o `max-width:100%`?
    corpo = u""
    i = html.find(u"function naoAmplia")
    if i >= 0:
        j = html.find(u"\n}", i)
        corpo = html[i:j + 2] if j > 0 else html[i:i + 2000]
    # ⚠️ O COMENTÁRIO SAI ANTES DA CONTA, e isto é lição paga na hora de
    #    escrever este portão: a nota que explica o `min(100%, ...)` cita o
    #    próprio `min(100%` em português. Medindo o texto cru, o portão via a
    #    frase e dava a linha por escrita — aprovava exatamente o caderno em
    #    que eu tinha apagado a linha. Portão que lê o próprio comentário não
    #    mede nada.
    corpo = re.sub(r"/\*.*?\*/", u" ", corpo, flags=re.S)
    corpo = re.sub(r"//[^\n]*", u" ", corpo)
    if u"maxHeight" not in corpo:
        faltas.append(u"o guarda nao segura a ALTURA (`maxHeight`): numa peca em "
                      u"que a altura manda, a figura continua esticando")
    if u"maxWidth" not in corpo:
        faltas.append(u"o guarda nao segura a LARGURA (`maxWidth`): numa peca em "
                      u"que a LARGURA manda (`width:clamp(), height:auto`) segurar "
                      u"so a altura quebra a proporcao e a figura sai ESTICADA "
                      u"(medido no _sinon2, folha 5, ate 71%)")
    elif u"min(100%" not in corpo:
        faltas.append(u"a largura e travada no valor cru, sem `min(100%, ...)`: "
                      u"`max-width` em estilo de LINHA vence o `max-width:100%` da "
                      u"folha de estilo, e af a figura larga deixa de encolher e "
                      u"ESTOURA a lateral da tela no celular (medido no _casa1, "
                      u"folha 19)")

    # 3 — toda figura desenhada chama o guarda?
    m = re.search(r"function img\s*\([^)]*\)\s*\{(.{0,600}?)\n?\}", html, re.S)
    if not m:
        faltas.append(u"nao achei a funcao `img()` para conferir o `onload`")
    elif u"naoAmplia" not in m.group(1):
        faltas.append(u"a funcao `img()` desenha a figura SEM "
                      u"`onload=\"naoAmplia(this)\"` — o guarda existe e nunca e "
                      u"chamado, que e o mesmo que nao existir")

    capas = len(re.findall(r'img class="capfig"', js))
    soltas = len(re.findall(r'img class="capfig"(?![^>]*naoAmplia)', js))
    if capas and soltas:
        faltas.append(u"%d de %d figura(s) da CAPA sem `onload=\"naoAmplia(this)\"` "
                      u"— a capa nao passa pelo `img()`, entao ela precisa chamar o "
                      u"guarda por conta propria (medido no _mult2 e no _subst5, "
                      u"onde a capa mostrava a figura a 1,49x)" % (soltas, capas))

    if not faltas:
        print(u"   ok: o guarda existe, segura os dois lados com `min(100%%, ...)` "
              u"e e chamado em toda figura (%d na capa)." % capas)
        return 0

    print(u"   REPROVADO:")
    for f in faltas:
        print(u"   - %s" % f)
    return 1


if __name__ == u"__main__":
    sys.exit(main())
