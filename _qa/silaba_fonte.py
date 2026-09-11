# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a sílaba sai da palavra CERTA?"

 ⚠️ O DEFEITO QUE O MARCOS OUVIU (set/2026, A Roda das Sílabas). Palavras dele:
    *"não entendi muito o sentido da primeira atividade, pois cita laranja e
    aparece lata"*.

    A folha 1 mostrava a figura da LATA e o alto-falante dizia LARANJA.

 COMO ISSO ACONTECE, e por que nenhum portão pegava: a sílaba nunca é
 sintetizada solta — ela é RECORTADA de dentro de uma palavra gravada (senão a
 voz soletra: "la" vira "éle-á"). Quem diz de qual palavra cada sílaba sai é o
 `var SILMAP`. E o gerador escolhia a fonte pela ordem ALFABÉTICA da lista de
 palavras: para LA, entre "laranja" e "lata", ganhava "laranja".

 Num caderno comum isso passa despercebido. Num caderno de RODA é fatal: a folha
 inteira é "esta figura começa com este pedacinho", e a criança ouve o pedacinho
 grudado numa palavra que não é a da tela. Ela não aprende a sílaba: aprende que
 o app fala coisas que não têm a ver com o desenho.

 ⚠️ E é um defeito MUDO. O app não dá erro, o `node --check` passa, a figura
    carrega, o mp3 existe e toca. Só existe no OUVIDO, com a tela na frente.

 O QUE ESTE PORTÃO MEDE
 1. Se a atividade declara `var RODAS`, cada sílaba de uma roda tem de ser
    recortada da PALAVRA DAQUELA RODA. (LA da roda do L cujo par é LATA → a
    fonte tem de ser "lata", nunca "laranja".)
 2. A sílaba tem de estar MESMO na posição que o SILMAP diz. O SILMAP guarda
    `[palavra, índice]`, e o índice existe porque há cadernos que recortam a
    sílaba do MEIO de propósito — o "BE" de aBElha, o "LO" de cavaLO. O erro é
    o índice apontar para uma sílaba que não é aquela.
    ⚠️ Na primeira versão deste portão eu conferi só a PRIMEIRA sílaba e ele
       acusou 21 recortes legítimos do `_sil1`. Portão que acusa inocente é
       portão que se aprende a ignorar — a casa já pagou por essa lição.
 3. AVISO (não reprova): quando há mais de uma palavra candidata para a mesma
    sílaba, diz quais são, porque é aí que a escolha importa.

 Uso: python3 _qa/silaba_fonte.py <pasta>
============================================================
"""
import json
import os
import re
import sys


def bloco(texto, nome):
    m = re.search(r"var " + nome + r"\s*=\s*(\{.*?\});", texto, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/silaba_fonte.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip("/")
    cam = os.path.join(pasta, "index.html")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html: NAO MEDI NADA." % pasta)
        return 2
    with open(cam, encoding="utf-8") as f:
        t = f.read()

    silmap = bloco(t, "SILMAP")
    if not silmap:
        print(u"%s -> NAO SE APLICA: esta atividade nao recorta silaba "
              u"(sem SILMAP)." % pasta)
        return 2

    # PAL: palavra -> [ESCRITA, [silabas]]
    mp = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", t, re.S)
    pal = {}
    if mp:
        for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)",\s*\[([^\]]*)\]\]', mp.group(1)):
            pal[m.group(1)] = [x.strip().strip('"') for x in m.group(3).split(",")]

    rodas = None
    mr = re.search(r"/\*RODAS-INI\*/\s*var RODAS = (\{.*?\});", t, re.S)
    if mr:
        try:
            rodas = json.loads(mr.group(1))
        except Exception:
            rodas = None

    da_roda = {}
    if rodas:
        for r in rodas.values():
            for s, w in zip(r["s"], r["w"]):
                da_roda.setdefault(s, w)

    erros, avisos, ok = [], [], 0
    for s, par in sorted(silmap.items()):
        fonte = par[0] if isinstance(par, list) else par
        idx = par[1] if isinstance(par, list) and len(par) > 1 else 0
        # 2. a sílaba tem de estar na posição declarada
        ss = pal.get(fonte) or []
        if ss and (idx >= len(ss) or ss[idx] != s):
            erros.append(u'a sílaba "%s" é recortada de "%s" na posição %d, '
                         u'onde está "%s"'
                         % (s, fonte, idx, ss[idx] if idx < len(ss) else u"nada"))
            continue
        # 1. numa roda, a fonte é a palavra da roda
        if s in da_roda and fonte != da_roda[s]:
            erros.append(u'a sílaba "%s" é da roda e a palavra dela é "%s", mas o '
                         u'recorte vem de "%s" — a criança vê uma figura e ouve outra'
                         % (s, da_roda[s], fonte))
            continue
        ok += 1
        cands = sorted(w for w in pal if s in (pal[w] or []))
        if len(cands) > 1 and s not in da_roda:
            avisos.append(u'"%s" sai de "%s"; também serviriam: %s'
                          % (s, fonte, ", ".join(x for x in cands if x != fonte)))

    print(u"%s -> fonte das silabas: %d silaba(s) conferida(s)%s"
          % (pasta, len(silmap), u" (roda declarada)" if rodas else u""))
    for a in avisos:
        print(u"   aviso: %s" % a)
    if erros:
        print(u"   %d SILABA(S) SAINDO DA PALAVRA ERRADA:" % len(erros))
        for e in erros:
            print(u"    - %s" % e)
        print(u"   conserto: no `gerar_falas.py`, escolher a fonte pela palavra da")
        print(u"   RODA (ou pela palavra que a folha mostra), nunca pela ordem")
        print(u"   alfabetica. E, na folha que sabe a palavra, chamar")
        print(u"   `falarSilaba(palavra, 0, silaba)` em vez de `falar('sb1_'+s)`.")
        return 1
    print(u"   ok: toda silaba e recortada da palavra que a crianca ve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
