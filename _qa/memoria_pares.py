# -*- coding: utf-8 -*-
u"""
============================================================
PORTÃO — "os pares do jogo da memória fecham mesmo?"

⚠️ LIÇÃO PAGA (ago/2026, na Oficina da Lina). Ao aumentar a memória de 8 para
10 pares eu escrevi DUAS cartas com a MESMA chave:

    {k:"campo", a:"CAMPO", b:"M, porque depois vem P"}
    {k:"campo", a:"LIMPO", b:"M, porque depois vem P"}     <-- chave repetida

O motor casa duas cartas quando `a.k === b.k` e os tipos são diferentes. Com a
chave repetida, a carta CAMPO casa com o motivo de LIMPO — e sobram cartas
órfãs que **nunca fecham**. A criança vira, vira, vira e a fase não acaba.

E nenhum portão via:
  · o `node --check` passa (é dado, não sintaxe);
  · o de imagem quebrada não pega, porque a figura da carta só aparece DEPOIS
    que a criança vira — a tela parada não a mostra;
  · o jogador automático acusa "PRESO", mas só depois de 15 minutos de partida,
    e sem dizer o motivo.

O QUE ESTE PORTÃO FAZ, em dois segundos e sem abrir o navegador:
  1. toda chave `k` é ÚNICA (senão o par se confunde);
  2. todo par tem os dois lados (o `a` e o `b`);
  3. a figura de cada carta existe na pasta `img/` — quando a peça usa figura.

Uso:  python3 _qa/memoria_pares.py _lina
============================================================
"""
import io
import os
import re
import sys


def confere(pasta):
    pasta = pasta.rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html. NAO MEDI." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()

    # o baralho da memoria: uma lista de {k:..., a:..., b:...}
    achou = re.findall(r'var\s+(\w*MEM\w*)\s*=\s*\[(.*?)\];', html, re.S)
    if not achou:
        # ⚠️ FORMATO MONTADO (esqueleto, ago/2026): na atividade gerada por
        # montar.py o baralho NAO e um `var ...MEM...` — mora nos DADOS da fase,
        # dentro de `FASES = [...]`. Sem esta ponte o portao rodava CEGO em toda
        # atividade montada (a Lojinha caiu nisso). Aqui ele le as fases de
        # mecanica "memoria" e confere o mesmo que confere no formato antigo.
        return confere_montada(pasta, html)

    ruim = 0
    for nome, corpo in achou:
        # ⚠️ o baralho pode ter campos NO MEIO (a palavra com a lacuna, por ex.):
        #    ler campo a campo, nunca exigir que `a` venha colado em `b`.
        cartas, todos = [], {}
        for bloco in re.findall(r'\{([^{}]*)\}', corpo):
            d = dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', bloco))
            if u"k" in d:
                cartas.append((d[u"k"], d.get(u"a", u""), d.get(u"b", u"")))
                todos[d[u"k"]] = d
        if not cartas:
            print(u"   %s: nao consegui ler as cartas. NAO MEDI." % nome)
            continue
        print(u"%s -> %s: %d par(es)" % (pasta, nome, len(cartas)))

        # 1) chave repetida = par que nunca fecha
        vistas, repetidas = {}, []
        for (k, a, b) in cartas:
            if k in vistas:
                repetidas.append((k, vistas[k], a))
            vistas[k] = a
        if repetidas:
            ruim += 1
            print(u"   !! %d CHAVE(S) REPETIDA(S) — os pares se confundem e "
                  u"cartas ficam orfas:" % len(repetidas))
            for (k, a1, a2) in repetidas:
                print(u"      k=\"%s\" serve a \"%s\" E a \"%s\"" % (k, a1, a2))
            print(u"   a crianca vira, vira, e a fase NAO ACABA. Cada par precisa")
            print(u"   da sua propria chave.")

        # 1b) CARTA IRMA RECONHECIVEL
        # ⚠️ LIÇÃO PAGA (ago/2026, na Oficina da Lina, o MESMO baralho de novo).
        # O verso da carta era o MOTIVO da letra — e motivo se repete: CAMPO,
        # SEMPRE e LÂMPADA tinham a carta "M, porque depois vem P" escrita
        # exatamente igual. O motor casa pela chave `k`, então a criança virava
        # duas cartas VISIVELMENTE certas e ouvia som de erro. Não é bug de
        # código nem chave repetida (o portão acima passa): é o jogo pedindo
        # adivinhação. Num jogo da memória a carta irmã tem que dar para
        # reconhecer — se dois pares mostram o mesmo texto, o jogo é sorte.
        # o que a crianca VE nao e o campo cru: e a `face:` que o codigo monta.
        # cada `push({...face:'...'+lista[i].campo...})` diz quais campos entram
        # naquele lado. Sem isto o portao acusaria repeticao onde a face ja se
        # distingue (a palavra inteira + o motivo embaixo).
        lados = []
        for bloco in re.findall(r'baralho\.push\(\{(.*?)\}\);', html, re.S):
            # ⚠️ so vale o que entra na `face:` — o `tx:` e reserva interna e nao
            #    aparece quando ha face. Contar o `tx` fazia o portao achar que
            #    duas cartas gemeas eram diferentes (foi assim no teste de fogo).
            cara = re.search(r'face:(.*)$', bloco, re.S)
            campos = re.findall(r'\w+\[i\]\.(\w+)', cara.group(1) if cara else bloco)
            campos = [c for c in campos if c != u"k"]
            if campos:
                lados.append(campos)
        if not lados:
            lados = [[u"a"], [u"b"]]
        texto_igual = {}
        for (k, a, b) in cartas:
            for campos in lados:
                visto_txt = u" ".join(todos[k].get(c, u"") for c in campos).strip()
                if visto_txt:
                    texto_igual.setdefault(visto_txt, []).append(k)
        gemeas = [(t, ks) for (t, ks) in texto_igual.items() if len(ks) > 1]
        if gemeas:
            ruim += 1
            print(u"   !! %d CARTA(S) COM O MESMO TEXTO EM PARES DIFERENTES —"
                  u" a crianca vira duas certas e ouve que errou:" % len(gemeas))
            for (t, ks) in gemeas[:5]:
                print(u"      \"%s\" aparece em: %s" % (t[:52], u", ".join(ks)))
            print(u"   a carta irma tem que ser RECONHECIVEL. Se o motivo se repete,")
            print(u"   ponha no verso algo proprio da palavra (ela inteira, a lacuna)")
            print(u"   e deixe o motivo como linha de apoio.")

        # 2) os dois lados escritos
        vazias = [k for (k, a, b) in cartas if not a.strip() or not b.strip()]
        if vazias:
            ruim += 1
            print(u"   !! %d par(es) com um lado vazio: %s" % (len(vazias), vazias[:5]))

        # 3) a figura de cada carta existe?
        #    (so cobra quando a peca monta o nome da figura a partir da chave)
        usa_fig = re.search(r'"img/(\w*)_?"\s*\+\s*\w+\[i\]\.k|img/\'\+\w+\[i\]\.k', html)
        pre = re.search(r'var\s+IMGS\s*=\s*\["(\w+?)_', html)
        if usa_fig and pre:
            p = pre.group(1)
            faltam = [k for (k, a, b) in cartas
                      if not os.path.exists(os.path.join(pasta, u"img",
                                                         u"%s_%s.png" % (p, k)))]
            if faltam:
                ruim += 1
                print(u"   !! %d carta(s) sem figura na pasta: %s"
                      % (len(faltam), [u"%s_%s.png" % (p, k) for k in faltam[:5]]))
                print(u"   ⚠️ o portao da imagem quebrada NAO pega essas: a figura")
                print(u"   da carta so aparece DEPOIS que a crianca vira.")

    if ruim:
        return 1
    print(u"   memoria ok: cada par tem chave propria, os dois lados e a figura dele")
    return 0


def _fatia_fases(html):
    u"""tira o `FASES = [ ... ]` do index montado por casamento de colchetes
    (json.loads direto quebra porque ha `;` e codigo depois).
    ⚠️ ha DOIS: o `var FASES = [];` vazio (declaracao) e o `FASES = [{...}]`
    populado (o montador escreve no fim). Percorre TODOS e fica com o 1o que
    tiver conteudo — senao o portao le a lista vazia e diz "sem memoria"."""
    import json
    melhor = None
    for m in re.finditer(r'FASES\s*=\s*\[', html):
        i = m.end() - 1               # aponta para o '['
        prof, j, dentro_str, esc, aspa = 0, i, False, False, u""
        while j < len(html):
            ch = html[j]
            if dentro_str:
                if esc:
                    esc = False
                elif ch == u"\\":
                    esc = True
                elif ch == aspa:
                    dentro_str = False
            else:
                if ch in u'"\'':
                    dentro_str = True; aspa = ch
                elif ch == u"[":
                    prof += 1
                elif ch == u"]":
                    prof -= 1
                    if prof == 0:
                        break
            j += 1
        try:
            arr = json.loads(html[i:j + 1])
        except Exception:
            arr = None
        if arr:                       # achou uma lista com conteudo
            return arr
        if melhor is None:
            melhor = arr
    return melhor


def confere_montada(pasta, html):
    fases = _fatia_fases(html)
    if fases is None:
        print(u"%s -> nao achei baralho (nem `var ...MEM...` nem `FASES=[...]`). NAO MEDI."
              % pasta)
        return 2
    mem = [f for f in fases if isinstance(f, dict) and f.get(u"mec") == u"memoria"]
    if not mem:
        print(u"%s -> NAO SE APLICA: montada sem fase de memoria. Nada a conferir." % pasta)
        return 2
    ruim = 0
    for f in mem:
        cartas = f.get(u"dados") or []
        fid = f.get(u"id", u"?")
        if not cartas:
            print(u"   fase %s: memoria sem cartas. NAO MEDI." % fid); continue
        print(u"%s -> fase %s: %d par(es)" % (pasta, fid, len(cartas)))
        # 1) chave repetida = par que nunca fecha
        vistas, rep = {}, []
        for c in cartas:
            k = c.get(u"k", u"")
            if k in vistas:
                rep.append(k)
            vistas[k] = 1
        if rep:
            ruim += 1
            print(u"   !! CHAVE(S) REPETIDA(S) — os pares se confundem: %s" % rep)
        # 2) pares distinguiveis: duas chaves NAO podem mostrar a MESMA figura
        #    (senao a crianca vira duas cartas de pares diferentes que sao
        #    identicas e ouve que errou — a versao "imagem" do defeito da Lina).
        porimg = {}
        for c in cartas:
            im = c.get(u"img", u"")
            if im:
                porimg.setdefault(im, []).append(c.get(u"k", u"?"))
        gem = [(im, ks) for im, ks in porimg.items() if len(ks) > 1]
        if gem:
            ruim += 1
            print(u"   !! MESMA FIGURA em pares diferentes (jogo vira sorte):")
            for im, ks in gem[:5]:
                print(u"      %s em %s" % (im, u", ".join(ks)))
        # 3) a figura de cada carta existe na pasta?
        faltam = []
        for c in cartas:
            for campo in (u"img", u"imgsen"):
                im = c.get(campo, u"")
                if im and not (im.startswith(u"data:") or u"/" in im):
                    if not os.path.exists(os.path.join(pasta, u"img", im + u".png")):
                        faltam.append(im)
        if faltam:
            ruim += 1
            print(u"   !! carta(s) sem figura na pasta: %s" % sorted(set(faltam))[:5])
    if ruim:
        return 1
    print(u"   memoria ok (montada): cada par tem chave propria, figura propria e o arquivo existe")
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/memoria_pares.py <pasta-da-atividade>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1]))
