#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO "A FASE DIZ O QUE ELA QUER?" — o enunciado explica a regra de fechar?

Defeito que o Marcos pegou (ago/2026), no Jardim do Broto, fase "Monte o seu
prato": *"mesmo colocando os cinco alimentos que se pede, não passa a fase.
Deveria ser qualquer cinco alimentos, não?"* — e, depois de ver a regra por
dentro: *"certo, se está certo então deixe, os áudios e dicas e textos explicam
isso?"*.

A regra da fase estava CERTA: o prato tem 5 lugares e só fecha com 5 partes
DIFERENTES da planta (raiz, caule, folha, flor, fruto, semente) — é isso que ela
ensina. O que estava errado era o ENUNCIADO:

    "O prato tem <b>5 lugares</b>. Escolha alimentos de <b>5 partes
     diferentes</b> da planta."

Dois números na mesma frase, os dois valendo 5, dizendo coisas diferentes. A
criança de 2º ano segue o número que ela VÊ acontecer — os cinco lugares
enchendo — e põe cinco comidas. Medido no navegador sobre o cardápio real: das
3003 escolhas possíveis de 5 alimentos, só 540 (18%) têm 5 partes distintas.
**82% das crianças que fazem o que a tela parece pedir ficam paradas** — sem erro
de JS, sem tela quebrada, sem nada que um print ou o `node --check` enxergue. O
auditor jogador também não pega: ele clica 5200 vezes ao acaso e acerta por
sorte; a criança não tem essa paciência.

A LIÇÃO, que vale muito além do prato: quando a condição de fechar uma fase
depende de um ATRIBUTO dos itens (a parte da planta, a categoria, o grupo, a
cor) e não da QUANTIDADE deles, o enunciado tem que dizer isso com todas as
letras — e a VOZ junto, porque quem mais precisa da explicação é justamente
quem ainda não lê.

O QUE ESTE PORTÃO MEDE, em cada fase que conta atributo distinto:

  R1 — ATRIBUTO NOMEADO. A palavra do campo que a fase conta (`it.parte` ->
       "parte") tem que aparecer no texto do enunciado E no texto que a voz dele
       fala, no `falas.json`. Fase que exige "partes diferentes" sem nunca dizer
       "parte" é adivinhação.

  R2 — UM NÚMERO SÓ. O enunciado não pode trazer duas quantidades. "5 lugares" e
       "5 partes diferentes" na mesma frase é a assinatura exata do defeito: a
       capacidade da zona brigando com a meta. Se a fase precisa dos dois
       números, um deles vai para o placar, não para o enunciado.
       (Artigos "um"/"uma" não contam como quantidade.)

COMO ELE ACHA A FASE: procura o molde de contagem de atributo distinto — um
conjunto indexado pelo campo do item (`vis[algo.parte]`) marcado dentro de um
`if(!...)` com um contador subindo (`n++`). É o jeito que o motor da casa
escreve "quantos DIFERENTES já entraram".

Uso:  python3 _qa/explica.py _jardim/index.html
Sai com 1 se alguma fase exigir atributo sem explicar.
"""
import io
import json
import os
import re
import sys

# a familia de palavras de cada campo: a crianca nao precisa ouvir o nome exato
# da variavel, precisa ouvir a PALAVRA. "parte" cobre "partes", "grupo" cobre
# "grupos". Campo desconhecido cai no proprio nome + o plural simples.
FAMILIA = {
    "parte":     [u"parte", u"partes"],
    "categoria": [u"categoria", u"categorias"],
    "grupo":     [u"grupo", u"grupos"],
    "tipo":      [u"tipo", u"tipos"],
    "familia":   [u"familia", u"familias"],
    "classe":    [u"classe", u"classes"],
    "cor":       [u"cor", u"cores"],
    "letra":     [u"letra", u"letras"],
    "silaba":    [u"silaba", u"silabas"],
}

# campos que NAO sao atributo de classificacao (sao identidade/posicao do item):
# contar "quantos ids diferentes" e so contar itens, nao pede explicacao nenhuma
IGNORA = set(["id", "idx", "i", "n", "k", "img", "nome", "src", "key", "chave"])

# quantidades escritas por extenso (artigos um/uma ficam de fora de proposito)
NUMPAL = (u"dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|"
          u"todos|todas|ambos")


def texto_limpo(s):
    u"""tira tags, entidades e acentos: o que sobra e a PALAVRA que a crianca ouve"""
    s = re.sub(r"<[^>]+>", " ", s)
    for ent, ch in ((u"&#225;", u"a"), (u"&#227;", u"a"), (u"&#226;", u"a"),
                    (u"&#233;", u"e"), (u"&#234;", u"e"), (u"&#237;", u"i"),
                    (u"&#243;", u"o"), (u"&#244;", u"o"), (u"&#245;", u"o"),
                    (u"&#250;", u"u"), (u"&#231;", u"c"), (u"&#186;", u"o"),
                    (u"&nbsp;", u" ")):
        s = s.replace(ent, ch)
    s = re.sub(r"&#\d+;", " ", s)
    tab = {u"á": u"a", u"à": u"a", u"ã": u"a", u"â": u"a", u"é": u"e", u"ê": u"e",
           u"í": u"i", u"ó": u"o", u"ô": u"o", u"õ": u"o", u"ú": u"u", u"ç": u"c"}
    for a, b in tab.items():
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return re.sub(r"\s+", " ", s).strip().lower()


def corpos(js):
    u"""devolve (nome, corpo) de cada `function telaXxx`, casando as chaves.

    Só as funções de TELA, e o corpo vem inteiro (com as funções de dentro —
    `conta()`, `repinta()`, `passo()`). É de propósito: quem conta o atributo é
    uma ajudante lá dentro, mas quem tem que EXPLICAR é a tela."""
    for m in re.finditer(r"function\s+(tela\w*)\s*\([^)]*\)\s*\{", js):
        i = m.end() - 1
        nivel, j = 0, i
        while j < len(js):
            if js[j] == "{":
                nivel += 1
            elif js[j] == "}":
                nivel -= 1
                if nivel == 0:
                    break
            j += 1
        yield m.group(1), js[i:j + 1]


def campo_contado(corpo):
    u"""acha o campo do molde `if(!vis[x.CAMPO]){ vis[x.CAMPO]=1; n++; }`

    ⚠️ O ÍNDICE TEM COLCHETE DENTRO. A chave real é `vis[noPrato[z].it.parte]`,
    e um `[^\\]]*` ingênuo para no `]` do `noPrato[z]` — foi assim que a primeira
    versão deste portão mediu ZERO fase e se aprovou sozinha. Portão que mede
    zero não é "passou": é cego. Por isso o miolo aceita um nível de colchete."""
    MIOLO = r"(?:[^\[\]]|\[[^\[\]]*\])*"
    for m in re.finditer(r"if\s*\(\s*!\s*(\w+)\[(" + MIOLO + r"\.(\w+))\]\s*\)?\s*\{?([^}]{0,160})",
                         corpo):
        conj, _, campo, resto = m.groups()
        if campo in IGNORA:
            continue
        # tem que MARCAR o conjunto e SUBIR um contador: e isso que faz dele
        # "quantos diferentes", e nao um simples "ja vi este"
        if re.search(re.escape(conj) + r"\[[^\]]*\]\s*=", resto) and "++" in resto:
            return campo
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    pasta = os.path.dirname(os.path.abspath(alvo))
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)
    js = re.sub(r"(?m)^\s*//.*$", "", js)

    falas = {}
    cam = os.path.join(pasta, "falas.json")
    if os.path.exists(cam):
        try:
            falas = dict((x["id"], x["texto"])
                         for x in json.load(io.open(cam, encoding="utf-8")))
        except Exception:
            falas = {}

    medidas, problemas = 0, []
    for nome, corpo in corpos(js):
        campo = campo_contado(corpo)
        if not campo:
            continue
        medidas += 1
        palavras = FAMILIA.get(campo, [campo, campo + u"s"])

        # o enunciado da fase = o primeiro balao que ela cria
        m = re.search(r'el\(\s*"div"\s*,\s*"balao"\s*,\s*"((?:[^"\\]|\\.)*)"', corpo)
        enunc = m.group(1) if m else u""
        # a voz do enunciado: o `_intro` da fase (senao, a 1a narracao literal)
        vid = None
        vm = re.search(r'falar\("([a-z0-9_]+_intro)"\)', corpo)
        if vm:
            vid = vm.group(1)
        else:
            vm = re.search(r'(?:falaDaTela|falar)\("([a-z0-9_]+)"\)', corpo)
            vid = vm.group(1) if vm else None
        voz = falas.get(vid, u"") if vid else u""

        et, vt = texto_limpo(enunc), texto_limpo(voz)
        if not enunc:
            problemas.append((nome, campo, u"a fase nao tem enunciado nenhum no balao"))
            continue

        # R1 — o atributo tem que ser NOMEADO, na tela e na voz
        na_tela = any(re.search(r"\b" + p + r"\b", et) for p in palavras)
        na_voz = any(re.search(r"\b" + p + r"\b", vt) for p in palavras)
        if not na_tela:
            problemas.append((nome, campo,
                              u'o enunciado nao diz "%s": "%s"' % (palavras[0], et[:88])))
        elif not na_voz:
            problemas.append((nome, campo,
                              u'a VOZ do enunciado (%s) nao diz "%s": "%s"'
                              % (vid or u"?", palavras[0], vt[:88] or u"(sem texto no falas.json)")))

        # R2 — um numero so: capacidade da zona nao pode brigar com a meta
        nums = re.findall(r"\d+", et) + re.findall(NUMPAL, et)
        if len(nums) >= 2:
            problemas.append((nome, campo,
                              u'o enunciado traz DUAS quantidades (%s) — a crianca segue '
                              u'a errada: "%s"' % (u", ".join(nums[:4]), et[:88])))

    print(u"%s -> %d fase(s) que fecham por ATRIBUTO distinto" % (alvo, medidas))
    if not medidas:
        print(u"   nenhuma fase conta atributo distinto. Nada a conferir.")
        return 0
    if problemas:
        print(u"   %d FASE(S) QUE EXIGEM SEM EXPLICAR (a crianca que cumpre o "
              u"enunciado literal fica presa):" % len(problemas))
        for nome, campo, por in problemas:
            print(u"     - %s (conta `%s` distinto): %s" % (nome, campo, por))
        print(u"   CONSERTO: diga no enunciado, em uma linha e com a MESMA frase na")
        print(u"   voz, que cada item precisa vir de um(a) %s diferente — e deixe o"
              % (u"/".join(sorted(set(p for _, c, _ in problemas
                                      for p in [FAMILIA.get(c, [c])[0]])))))
        print(u"   numero da capacidade fora do enunciado (ele vai para o placar).")
        return 1
    print(u"   todas explicam o atributo, na tela e na voz, sem numero brigando.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
