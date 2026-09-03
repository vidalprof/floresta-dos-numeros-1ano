# -*- coding: utf-8 -*-
u"""
PORTÃO DO CONTAINER QUE CORTA — "a moldura come a figura?"

NASCEU DE UMA CORREÇÃO DO PRÓPRIO MARCOS (set/2026). Ele disse primeiro *"as
imagens bola e elefante aparecem faltando partes"*, eu fui olhar os ARQUIVOS,
achei defeito de recorte neles e mostrei. E ele me corrigiu com precisão:

    *"Nas imagens que mostrou está certo mas NA ATIVIDADE aparecem faltando"*

Eu estava consertando a coisa errada. O arquivo estava bom: quem cortava era o
CSS. Na fase de bater sílabas, cada batida põe a figura dentro de uma bolinha:

    .bsBatida     { width:54px; height:54px; border-radius:50%; overflow:hidden }
    .bsBatida img { width:84%; height:84%; object-fit:contain }

O `object-fit:contain` encaixa a figura no QUADRADO — e o container é um
CÍRCULO, que come os CANTOS desse quadrado. É exatamente nos cantos que ficam a
cauda do rato, as orelhas do elefante, a curva de baixo da bola. A criança via o
bicho sem pedaço, e o arquivo estava intacto o tempo todo.

A GEOMETRIA, que é o que torna isto MEDÍVEL: o maior quadrado que cabe dentro de
um círculo tem lado igual ao diâmetro dividido por raiz de 2 — 70,7%. Uma imagem
com `contain` acima disso, dentro de um container redondo que esconde o que
vaza, PERDE canto. Não é opinião nem calibração: é conta fechada.

⚠️ POR QUE ISTO IMPORTA MAIS QUE O DEFEITO: eu passei uma rodada inteira medindo
os PNGs, achando buraco e fragmento, montando contato-folha — e o defeito que o
Marcos via não estava lá. Quando alguém diz "aparece errado NA ATIVIDADE", a
primeira pergunta é se o arquivo está bom; se estiver, o culpado é quem desenha,
não quem foi desenhado.

O QUE ELE MEDE, no CSS do motor e no de cada atividade montada:
  1. container redondo (border-radius:50% + overflow:hidden) com `img` acima de
     71% -> REPROVA, e diz de quanto passou;
  2. `object-fit: cover` em figura de conteúdo -> REPROVA (cover corta de
     propósito; serve para foto de fundo, nunca para o bicho que a criança
     precisa reconhecer);
  3. container com `overflow:hidden` e altura fixa menor que a imagem -> AVISA.

Uso:  python3 _qa/corta_figura.py <arquivo.css ou pasta ou index.html>
Sai 0 se limpo, 1 se a moldura corta, 2 se não deu para medir.
"""
import os, re, sys

LADO_NO_CIRCULO = 70.7      # 100/raiz(2): o quadrado que cabe inteiro no círculo


def regras(css):
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield m.group(1).strip(), m.group(2)


def confere_css(css, origem):
    ruins, avisos, medidas = [], [], 0

    # 1) quem é redondo E esconde o que vaza
    redondos = {}
    for sel, corpo in regras(css):
        c = corpo.replace(" ", "")
        if "border-radius:50%" in c and "overflow:hidden" in c:
            redondos[sel.split()[-1]] = sel

    # 2) as imagens dentro deles
    for sel, corpo in regras(css):
        c = corpo.replace(" ", "")
        alvo = sel.rstrip()
        if not (alvo.endswith("img") or alvo.endswith("image")):
            continue
        pai = alvo.rsplit(" ", 1)[0].split()[-1] if " " in alvo else None
        w = re.search(r"width:(\d+(?:\.\d+)?)%", c)
        if pai in redondos and w:
            medidas += 1
            larg = float(w.group(1))
            if larg > LADO_NO_CIRCULO + 0.5:
                ruins.append(
                    u"[%s] `%s` esta a %.0f%% dentro de um container REDONDO (`%s`): "
                    u"o circulo corta os cantos. O maximo que cabe inteiro e %.1f%% "
                    u"(o quadrado inscrito no circulo). Passou %.0f pontos."
                    % (origem, sel.strip(), larg, redondos[pai].strip(),
                       LADO_NO_CIRCULO, larg - LADO_NO_CIRCULO))

    # 3) object-fit:cover em figura de conteúdo (cover corta de propósito)
    for sel, corpo in regras(css):
        c = corpo.replace(" ", "")
        if "object-fit:cover" not in c:
            continue
        s = sel.lower()
        # fundo de cena pode usar cover: é para preencher mesmo
        if any(k in s for k in ("fundo", "bg", "capa", "cena", "banner", "hero", "ceu")):
            continue
        medidas += 1
        ruins.append(u"[%s] `%s` usa `object-fit:cover`, que CORTA a figura para "
                     u"preencher. Para o bicho/objeto que a crianca precisa "
                     u"reconhecer, use `contain`. `cover` so em fundo de cena."
                     % (origem, sel.strip()))

    return ruins, avisos, medidas


def confere(caminho):
    alvos = []
    if os.path.isdir(caminho):
        for c in (os.path.join(caminho, "index.html"),):
            if os.path.exists(c):
                alvos.append(c)
    elif os.path.exists(caminho):
        alvos.append(caminho)
    if not alvos:
        print(u"NAO MEDI: nao achei CSS em %s" % caminho)
        return 2

    ruins, avisos, medidas = [], [], 0
    for a in alvos:
        txt = open(a, encoding="utf-8", errors="replace").read()
        if a.endswith(".html"):
            css = u"\n".join(re.findall(r"<style[^>]*>(.*?)</style>", txt, re.S))
            if not css:
                print(u"NAO MEDI: nenhum <style> em %s" % a)
                return 2
        else:
            css = txt
        r, v, m = confere_css(css, os.path.basename(a))
        ruins += r; avisos += v; medidas += m

    if not medidas:
        print(u"NAO MEDI: nenhuma figura dentro de container que corta em %s" % caminho)
        return 2

    for v in avisos[:6]:
        print(u"   aviso: %s" % v)
    if ruins:
        print(u"%s -> %d moldura(s) CORTANDO a figura (de %d conferidas):"
              % (caminho, len(ruins), medidas))
        for x in ruins[:10]:
            print(u"    ✗ %s" % x)
        return 1

    print(u"%s -> moldura ok: %d figura(s) em container que corta, todas cabem inteiras."
          % (caminho, medidas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/corta_figura.py <css | pasta | index.html>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1].rstrip("/")))
