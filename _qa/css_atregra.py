# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO — A REGRA-@ QUE SUMIU DO CSS  (4c3)

 ⭐ A DIVIDA QUE ESTE ARQUIVO PAGA (14/set/2026). O Desfile das Letras foi ao ar
    com **36 regras-@ sem o arroba**: `@keyframes` virou `keyframes`, `@media`
    virou `media`. Uma edicao minha, em massa, comeu o caracter — e NADA
    reclamou. O `node --check` nao olha CSS; o contraste mede o pixel, e o pixel
    continuava certo; o leiaute mede a caixa, e a caixa continuava certa; a foto
    de regressao pegou a tela parada, e o que morreu foi o MOVIMENTO. O app
    abria bonito.

    O que a crianca perdeu: toda animacao (o confete, o tremor do erro, a letra
    que entra no desfile) e **todas as regras de tela pequena** — no celular da
    escola o leiaute ficou o da tela larga.

 ⚠️ POR QUE ISTO PRECISA DE PORTAO E NAO DE CUIDADO: o navegador nao da erro
    nenhum. `keyframes pulsa{...}` sem arroba nao e sintaxe invalida — vira uma
    REGRA DE ESTILO com o seletor "keyframes pulsa", que nunca casa com nada.
    O CSS segue valido, a pagina segue abrindo, e o defeito e invisivel em
    print. Defeito que so existe em movimento tem que ser MEDIDO (a mesma licao
    do tremor do mascote).

 O QUE ELE MEDE, em texto puro (milissegundos):

 1. **Regra-@ sem o arroba:** linha que comeca com `keyframes `,
    `-webkit-keyframes `, `media `, `supports ` ou `font-face` e nao tem `@`.
 2. **Animacao orfa:** todo nome usado em `animation:` / `animation-name:` tem
    um `@keyframes` (ou `@-webkit-keyframes`) com esse nome no arquivo.

 ⚠️ O QUE ELE NAO MEDE, E EU NAO VOU FINGIR QUE MEDE: se a animacao FICA BONITA,
    se a duracao esta boa, se ela respeita `prefers-reduced-motion` no gosto do
    professor. Isto aqui so responde "existe?".

 Uso:  python3 _qa/css_atregra.py <arquivo.html|pasta>
 Codigo 0 = ok · 1 = REPROVADO · 2 = nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# as palavras que, no comeco de uma linha, so podem ser regra-@
ATS = (u"keyframes ", u"-webkit-keyframes ", u"-moz-keyframes ", u"-o-keyframes ",
       u"media ", u"media(", u"supports ", u"font-face", u"import ")

# valores de `animation:` que sao propriedade, e nao nome de keyframes
PALAVRAS = set(u"""none infinite alternate reverse normal forwards backwards both
    linear ease ease-in ease-out ease-in-out step-start step-end running paused
    important initial inherit unset alternate-reverse""".split())


def css_do_html(html):
    return u"\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))


def sem_comentario(css):
    u"""apaga os comentarios /* ... */ mantendo as quebras de linha.

    ⚠️ LICAO PAGA NA PRIMEIRA HORA DESTE ARQUIVO: a Padaria tem um comentario de
       varias linhas em que uma delas comeca com a palavra `media` ("media 400x55
       = 7,3 vezes mais larga..."). Sem apagar o comentario, o portao acusou um
       texto explicativo de ser uma regra-@ quebrada. Quando o portao reprova,
       a primeira suspeita e a regua."""
    def branco(m):
        return u"".join(c if c == u"\n" else u" " for c in m.group(0))
    return re.sub(r"/\*.*?\*/", branco, css, flags=re.S)


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/css_atregra.py <arquivo.html|pasta>")
        return 2
    alvo = sys.argv[1].rstrip(u"/")
    if os.path.isdir(alvo):
        alvo = os.path.join(alvo, u"index.html")
    if not os.path.exists(alvo):
        print(u"NAO MEDI: nao achei %s" % alvo)
        return 2

    html = io.open(alvo, encoding=u"utf-8").read()
    css = sem_comentario(css_do_html(html))
    if not css.strip():
        print(u"%s -> NAO MEDI: nao achei <style> nenhum." % alvo)
        return 2

    linhas = css.split(u"\n")
    sem_arroba = []
    for n, l in enumerate(linhas, 1):
        s = l.lstrip()
        if not s or s.startswith(u"@") or s.startswith(u"/*") or s.startswith(u"*"):
            continue
        for a in ATS:
            if s.startswith(a):
                sem_arroba.append((n, s[:72]))
                break

    # os nomes que existem de verdade
    tem = set(re.findall(r"@(?:-webkit-|-moz-|-o-)?keyframes\s+([A-Za-z_][\w-]*)", css))
    # os nomes usados
    usados = {}
    for m in re.finditer(r"animation(?:-name)?\s*:\s*([^;}!]+)", css):
        for tok in re.split(r"[\s,]+", m.group(1).strip()):
            tok = tok.strip()
            if not tok or tok in PALAVRAS:
                continue
            if re.match(r"^[-.\d]", tok) or tok.endswith(u"s") and re.match(r"^[\d.]+m?s$", tok):
                continue
            if re.match(r"^(cubic-bezier|steps)\(", tok):
                continue
            if re.match(r"^[A-Za-z_][\w-]*$", tok):
                usados.setdefault(tok, 0)
                usados[tok] += 1
    orfas = sorted(k for k in usados if k not in tem)

    print(u"%s -> regra-@ do CSS: %d bloco(s) @keyframes, %d nome(s) de animacao usado(s)"
          % (alvo, len(tem), len(usados)))

    if not sem_arroba and not orfas:
        print(u"   ✓ nenhuma regra-@ sem o arroba e nenhuma animacao orfa")
        return 0

    print(u"   REPROVADO:")
    if sem_arroba:
        print(u"    - %d linha(s) de regra-@ SEM o arroba (o navegador nao reclama, "
              u"e a regra nunca vale):" % len(sem_arroba))
        for n, s in sem_arroba[:12]:
            print(u"        linha %d do <style>: %s" % (n, s))
        if len(sem_arroba) > 12:
            print(u"        ... e mais %d" % (len(sem_arroba) - 12))
        print(u"      conserto: por o `@` de volta no comeco da linha.")
    if orfas:
        print(u"    - %d animacao(oes) sem `@keyframes` com esse nome: %s"
              % (len(orfas), u", ".join(orfas[:10])))
        print(u"      conserto: criar o bloco, ou tirar o `animation:` que aponta "
              u"para o vazio (elemento com `opacity:0` esperando animacao que nao "
              u"existe fica INVISIVEL para sempre).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
