# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "toda palavra que a folha pode sortear tem figura no disco?"

 ⚠️⚠️ LIÇÃO PAGA (11/set/2026), e ela é minha do mesmo dia.

 Horas antes eu tinha renomeado o selo dourado da medalha de `<pref>_estrela.png`
 para `<pref>_selo.png` — o conserto certo, porque o nome batia com a PALAVRA
 "estrela" do pote e a criança via o selo da medalha no lugar do desenho. Só que
 em três cadernos (`_sil1`, `_ini1`, `_som1`) a palavra ESTRELA **é** do pote, e
 ao renomear o arquivo eu deixei a palavra sem figura nenhuma. Publiquei assim.

 Nenhum dos ~70 portões viu, e o motivo é instrutivo: o `index.html` continuou
 válido, o `node --check` passou, o `clone.py` não tinha o que reprovar, e o
 `_qa/imagens.js` (que abre o navegador e cobra figura quebrada) só olha a
 PRIMEIRA tela — a palavra podia estar na folha 9. Quem achou foi o
 `_qa/andar_folha.js`, andando folha por folha. Este portão aqui faz a mesma
 pergunta sem abrir navegador nenhum, em milissegundos, e por isso cabe no
 pré-voo: **cruza o que os potes sorteiam com o que existe em `<pasta>/img/`**.

 ⚠️ E ele confere o POTE INTEIRO, não a folha sorteada. Uma palavra que só
    aparece em 1 sorteio a cada 5 é pior que uma que aparece sempre: vai ao ar,
    passa em todo teste, e quebra na aula de uma turma só.

 Uso:  python3 _qa/figura_pote.py <pasta> [<pasta> ...]
 Código 0 = passou · 1 = REPROVADO · 2 = não deu para medir (não é "passou").
============================================================
"""
import io
import json
import os
import re
import sys


def colhe(o, fora):
    if isinstance(o, str):
        fora.add(o)
    elif isinstance(o, list):
        for x in o:
            colhe(x, fora)
    elif isinstance(o, dict):
        for x in o.values():
            colhe(x, fora)


def confere(pasta):
    pasta = pasta.rstrip("/")
    cam = os.path.join(pasta, "index.html")
    if not os.path.exists(cam):
        return 2, [u"   sem index.html: NAO MEDI"]
    t = io.open(cam, encoding="utf-8").read()

    mi = re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\n\});\s*/\*ITENS-FIM\*/",
                   t, re.S)
    mp = re.search(r"var PAL = \{(.*?)\n\};", t, re.S)
    if not mi or not mp:
        return 2, [u"   nao e caderno de folha viva (sem ITENS + PAL): NAO MEDI"]

    try:
        itens = json.loads(mi.group(1))
    except ValueError as e:
        return 2, [u"   o bloco ITENS nao e JSON valido (%s): NAO MEDI" % e]

    pal = set(re.findall(r'(?m)(?:^|[\s,])(\w+)\s*:\s*\[', mp.group(1)))
    sorteaveis = set()
    colhe(itens, sorteaveis)
    sorteaveis &= pal          # só o que é palavra: rótulos e letras ficam fora

    # o prefixo é o que o próprio código escreve em img/<pref>_
    prefs = sorted(set(re.findall(r'"img/([a-z]{2,3})_', t)))
    if not prefs:
        return 2, [u"   nao achei o prefixo das figuras: NAO MEDI"]
    pref = prefs[0]

    dirimg = os.path.join(pasta, "img")
    faltam = sorted(w for w in sorteaveis
                    if not os.path.exists(os.path.join(dirimg, "%s_%s.png" % (pref, w))))
    if faltam:
        return 1, [u"   REPROVADO: %d palavra(s) que o pote sorteia SEM figura em "
                   u"%s/ (a crianca ve o quadradinho vazio):" % (len(faltam), dirimg),
                   u"      " + u", ".join(u"%s (falta %s_%s.png)" % (w, pref, w)
                                          for w in faltam)]
    return 0, [u"   ✓ as %d palavras sorteaveis tem figura em %s/" % (len(sorteaveis), dirimg)]


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/figura_pote.py <pasta> [<pasta> ...]")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        c, linhas = confere(pasta)
        marca = u"OK" if c == 0 else (u"REPROVADO" if c == 1 else u"NAO MEDI")
        print(u"%s -> %s" % (pasta.rstrip("/"), marca))
        for l in linhas:
            print(l)
        pior = 1 if (pior == 1 or c == 1) else max(pior, c)
    return pior


if __name__ == "__main__":
    sys.exit(main())
