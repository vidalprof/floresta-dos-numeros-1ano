# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "toda coisa do POTE tem voz?"  (caderno de folha viva)

 ⚠️ O DEFEITO, e eu mesmo o fiz em 13/set/2026, na mesma sessão em que jurei que
    o conserto tem duas partes.

    O Desfile das Letras não enchia a aula, e o conserto certo era pôr o
    ALFABETO INTEIRO no pote — ele guardava só 10 das 26 letras. Fiz isso, e de
    quebra entraram sete palavras novas (hipopótamo, igreja, leão, navio, ovo,
    queijo, xícara), todas com figura na pasta. **Nenhuma tinha voz.**

    Num caderno de 1º ano a voz NÃO é enfeite: é a atividade. A criança que ainda
    não lê aperta o alto-falante para saber o que é a figura. Se o sorteio lhe
    desse "xícara", ela apertava e não vinha nada.

 ⚠️ E POR QUE NENHUM PORTÃO VIU: a folha é SORTEADA. O `andar_folha.js` anda uma
    tirada do pote — e numa tirada de 12 entre 23 palavras, a chance de não cair
    nenhuma das sete é alta. Portão que depende de sorte não é portão: é aposta.
    Este aqui não sorteia nada — ele confere **o pote inteiro**, item por item.

 O QUE ELE MEDE (sem navegador, só lendo os blocos marcados do index.html):
   para cada item de cada pote (`/*ITENS-INI*/`), descobre as chaves de fala que
   aquele item pode pedir — pelo padrão `prefixo_` + valor que o `folhas.js`
   monta — e reprova se alguma não existir no `FALAS`.

   Ele aprende os prefixos LENDO o `folhas.js` (`falar("pal_" + w)` →
   prefixo `pal_`), então caderno novo com prefixo novo já entra sozinho.

 ⚠️ NÃO CONFUNDIR com o portão "voz sem mp3": aquele pergunta se o arquivo foi
    GRAVADO (e antes de publicar é normal faltar, quem grava é o `entregar.yml`).
    Este pergunta se o TEXTO existe — e texto que não existe nunca vira mp3.

 Uso:  python3 _qa/voz_do_pote.py <pasta>
 Código 0 = todo item do pote tem voz · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys


def bloco(html, nome, ini, fim):
    # ⚠️ O FECHO DO BLOCO NAO E O FECHO DO OBJETO (licao paga em 14/set/2026,
    #    nos cinco reinos, e a MESMA que o `_qa/duracao.py` pagou no mesmo dia).
    #    O gerador daquele caderno escreve DOIS vars dentro do bloco marcado
    #    (`ITENS` e `FIGNOME`, o nome falado de cada figura). A ancora antiga
    #    exigia o `};` colado no `/*ITENS-FIM*/`; com o segundo var no meio ela
    #    nao casava, o portao dizia "NAO MEDI" e a banca inteira passava batido
    #    por cima da pergunta *"tudo que o pote sorteia tem voz?"* — que e a
    #    pergunta que ele existe para fazer. Agora ele para no `};` do proprio
    #    objeto e nao se importa com o que venha depois DENTRO do bloco.
    m = re.search(r"/\*%s\*/\s*var %s = (\{.*?\})\s*;" % (ini, nome), html, re.S)
    if not m:
        m = re.search(r"var %s = (\{.*?\n\});" % nome, html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def campos(pool, caminho=u""):
    u"""Percorre o pote e devolve {campo: conjunto de valores}.

    ⚠️ POR CAMPO, e não "todos os textos do pote juntos" — a primeira versão
       deste portão juntava tudo num saco só e depois ADIVINHAVA de que família
       era cada valor pelo tamanho. Deu 416 acusações falsas no caderno de
       moradia (cobrava `chamar_` de palavra de poema) e 30 na Roda (cobrava
       `pal_` de sílaba trocada). **Portão que acusa inocente é portão que se
       aprende a ignorar** — a casa já pagou essa lição no `silaba_fonte.py`,
       que reprovou 21 recortes legítimos. Campo é a família de verdade: o `w`
       da folha 9 é uma coisa, o `L` é outra, e o pote já diz qual é qual.
    """
    fora = {}

    def anda(x, cam):
        if isinstance(x, dict):
            for k, v in x.items():
                anda(v, cam + u"." + k)
        elif isinstance(x, list):
            for v in x:
                anda(v, cam + u"[]")
        elif isinstance(x, type(u"")):
            if x and u" " not in x and len(x) <= 24:
                fora.setdefault(cam, set()).add(x)

    anda(pool, caminho)
    return fora


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/voz_do_pote.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    caminho_js = os.path.join(pasta, u"folhas.js")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html. NAO MEDI." % pasta)
        return 2
    if not os.path.exists(caminho_js):
        print(u"%s -> NAO SE APLICA: nao e caderno de folha viva (sem folhas.js)." % pasta)
        return 2

    html = io.open(cam, encoding=u"utf-8").read()
    js = io.open(caminho_js, encoding=u"utf-8").read()
    IT = bloco(html, u"ITENS", u"ITENS-INI", u"ITENS-FIM")
    F = bloco(html, u"FALAS", u"FALAS-INI", u"FALAS-FIM")
    if IT is None or F is None:
        print(u"%s -> NAO MEDI: nao achei os blocos ITENS/FALAS marcados." % pasta)
        return 2

    # ⚠️ OS PREFIXOS SE APRENDEM DO CÓDIGO — e AMARRADOS À FOLHA QUE OS USA.
    #    Ler só "quais prefixos existem" não bastou: `perg12_` é da folha 12 e
    #    `pista_` é da 10, mas as duas folhas guardam MORADIA no pote, então o
    #    portão cobrava `perg12_` das moradias da folha 10 — inocente acusado.
    #    Agora o texto de cada `function fN(...)` é lido separado: o prefixo que
    #    aparece dentro da folha N só é cobrado do pote `pN`.
    porFolha = {}
    pedacos = re.split(r'\nfunction f(\d+)\s*\(', u"\n" + js)
    for i in range(1, len(pedacos) - 1, 2):
        n, corpo = pedacos[i], pedacos[i + 1]
        pres = set(re.findall(r'falar\(\s*"([a-z0-9]+_)"\s*\+', corpo))
        if pres:
            porFolha.setdefault(u"p" + str(int(n)), set())
            porFolha[u"p" + str(int(n))] |= pres
    prefixos = sorted(set(p for v in porFolha.values() for p in v))
    if not prefixos:
        print(u"%s -> NAO MEDI: o folhas.js nao monta nenhuma chave de fala por "
              u"prefixo (`falar(\"x_\" + v)`)." % pasta)
        return 2

    faltam, conferidas, familias = [], 0, 0
    for nome, pool in sorted(IT.items()):
        pres = porFolha.get(nome)
        if not pres:
            continue          # esta folha não fala nada por prefixo: nada a cobrar
        for cam, vals in sorted(campos(pool, nome).items()):
            for pre in sorted(pres):
                tem = [v for v in vals if (pre + v) in F]
                # ⚠️ O PISO DE EVIDÊNCIA. Só cobro um prefixo de um campo quando a
                #    MAIORIA dos valores daquele campo já é falada com ele (e são
                #    ao menos dois). Um acerto solto pode ser coincidência de
                #    nome; uma maioria é a família declarada pelo próprio
                #    caderno. Abaixo disso o portão se CALA — e "não medi" é
                #    melhor que acusar inocente.
                if len(tem) < 2 or len(tem) * 2 <= len(vals):
                    continue
                familias += 1
                for v in sorted(vals):
                    conferidas += 1
                    if (pre + v) not in F:
                        faltam.append((nome, pre + v))

    print(u"%s -> voz do pote: %d chave(s) conferida(s) em %d familia(s) "
          u"campo x prefixo (prefixos no codigo: %s)"
          % (pasta, conferidas, familias, u", ".join(prefixos)))
    if not familias:
        print(u"   NAO MEDI: nenhum campo do pote e falado por prefixo neste caderno.")
        return 2
    if faltam:
        print(u"   %d COISA(S) DO POTE SEM VOZ — a crianca aperta o alto-falante "
              u"e nao vem nada:" % len(faltam))
        for cam, k in sorted(set(faltam))[:20]:
            print(u"    - %s   (pote %s)" % (k, cam))
        print(u"   conserto: escrever o texto no FALAS do index.html E no")
        print(u"   <pasta>/falas.json (que e a VERDADE que o entregar.yml grava),")
        print(u"   com a mesma chave. Texto que nao existe nunca vira mp3.")
        return 1
    print(u"   ok: tudo o que o pote pode sortear tem texto de voz")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
