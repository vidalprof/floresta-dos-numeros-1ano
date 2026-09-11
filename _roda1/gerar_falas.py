# -*- coding: utf-8 -*-
u"""
============================================================
 A RODA DAS SÍLABAS — gerador das falas (degrau 9: a vogal que muda a sílaba)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ E AQUI A VOZ É O CONTEÚDO INTEIRO — mais ainda que no degrau 3. Ali as
    palavras comparadas começavam com CONSOANTES diferentes, e no papel isso
    ainda se vê. Aqui LATA, LEÃO, LIMÃO, LOBO e LUPA começam todas com a MESMA
    letra: a diferença mora só na vogal, e só no OUVIDO. Sem voz esta folha não
    ensina nada — vira leitura disfarçada.

 ⚠️⚠️ A SÍLABA SAI RECORTADA DA PALAVRA INTEIRA (`silabas.json` +
    `_padrao/silabas_voz.py`). Lição paga em 10/set/2026: sintetizar a sílaba
    solta faz a voz SOLETRAR ("va" vira "vê-á"), porque ela não lê som, lê
    palavra. Aqui a voz lê "cavalo" e o alinhamento forçado corta o "ca" de
    dentro. O portão `_qa/silabas.py` mede e reprova se sair soletrado.

 Uso:  python3 _roda1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"ro_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\]', bloco):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])
DISTRA = json.loads(re.search(r"var DISTRA = (\{.*?\});",
                              io.open(os.path.join(AQUI, u"folhas.js"),
                                      encoding=u"utf-8").read(), re.S).group(1))


def esc(w):
    return PAL[w][0]


def sil(w):
    return PAL[w][1]


def ini(w):
    return sil(w)[0]


DIZ = {u"maca": u"maçã", u"piao": u"pião", u"jacare": u"jacaré", u"celular": u"celular"}


def falado(w):
    return DIZ.get(w, esc(w).lower())


def empedacos(w):
    return u"... ".join(s.lower() for s in sil(w))


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"A Roda das Sílabas. Dez folhas para descobrir uma coisa muito útil: o "
              u"éle sozinho não fala. Quando a vogal chega, nasce um pedacinho — e com "
              u"cinco vogais nascem cinco pedacinhos. Escreva o seu nome ali embaixo e "
              u"toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim! Agora você sabe montar a roda: uma letra parada e as "
             u"cinco vogais girando. Existe uma roda para cada letra — quantas você "
             u"consegue montar? Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva o pedacinho do começo."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Escute o começo de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois no pedacinho com que ela começa."
F[u"rodaLivre"] = u"Esta é a roda do éle. Toque numa vogal e escute o que nasce."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram."

F[u"p1enun"] = (u"Folha um: a roda do éle. Toque nas vogais e escute. O éle fica parado "
                u"no meio; a vogal é que muda. Brinque à vontade primeiro; os pedidos "
                u"vêm depois.")
F[u"p2enun"] = u"Folha dois: ouça a palavra. Com que pedacinho ela começa?"
F[u"p3enun"] = (u"Folha três: toque em todas as figuras que começam com o pedacinho "
                u"mostrado. Cuidado: as outras começam com a mesma letra, mas com outra "
                u"vogal. Depois toque em Conferir.")
F[u"p4enun"] = u"Folha quatro: ligue cada figura ao pedacinho com que ela começa."
F[u"p5enun"] = (u"Folha cinco: nesta grade há duas que começam com o mesmo pedacinho. "
                u"Ache as duas.")
F[u"p6enun"] = u"Folha seis: falta o começo da palavra. Ponha o pedacinho certo no lugar."
F[u"p7enun"] = (u"Folha sete: três são da mesma roda e uma não é. Circule quem não é da "
                u"roda. Preste atenção: às vezes a intrusa começa com a mesma letra.")
F[u"p8enun"] = u"Folha oito: ponha cada figura na gaveta do começo dela."
F[u"p9enun"] = u"Folha nove: ouça a palavra e escreva o pedacinho com que ela começa."
F[u"p10enun"] = u"Folha dez: toque nas palavras que você quer no mural das rodas."

# ---- toda palavra que aparece --------------------------------------------------
usadas = set()
for chave, lista in IT.items():
    for x in lista:
        if isinstance(x, dict):
            usadas.update(x[u"g"])
        elif isinstance(x, list):
            usadas.update(x)
        else:
            usadas.add(x)
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: ouvir o começo ---------------------------------------------------
for w in IT[u"p1"]:
    F[u"certo1_%s" % w] = (u"Isso! %s começa com %s. %s."
                           % (falado(w).capitalize(), ini(w).lower(), empedacos(w)))
    # ⚠️ tocar no pedaço do meio não é erro: é a pergunta errada
    F[u"volte1_%s" % w] = u"Esse é um pedaço do meio. O COMEÇO é o primeiro de todos."

# ---- folha 2: qual é o começo --------------------------------------------------
for w in IT[u"p2"]:
    F[u"certo2_%s" % w] = u"Muito bem! %s começa com %s." % (falado(w).capitalize(),
                                                             ini(w).lower())
    F[u"dica2_%s" % w] = (u"Fale a palavra bem devagar: %s. Escute só o comecinho."
                          % empedacos(w))

# ---- folha 3: circule quem começa igual ----------------------------------------
for it in IT[u"p3"]:
    s, g = it[u"s"], it[u"g"]
    certas = [w for w in g if ini(w) == s]
    F[u"certo3_%s" % s] = (u"Isso! %s começam com %s."
                           % (u", ".join(falado(w) for w in certas), s.lower()))
    F[u"dica3_%s" % s] = (u"Ouça cada figura e compare só o começo com %s. "
                          u"Não se esqueça: pode ser mais de uma." % s.lower())

# ---- folha 4: ligar --------------------------------------------------------------
for g in IT[u"p4"]:
    for w in g:
        F[u"certo4_%s" % w] = u"Isso! %s começa com %s." % (falado(w).capitalize(),
                                                            ini(w).lower())
        F[u"dica4_%s" % w] = (u"Escute o comecinho: %s. Procure esse pedacinho do outro "
                              u"lado." % empedacos(w))

# ---- folha 5: achar as duas ------------------------------------------------------
for g in IT[u"p5"]:
    conta = {}
    for w in g:
        conta[ini(w)] = conta.get(ini(w), 0) + 1
    par = [k for k in conta if conta[k] == 2][0]
    certas = [w for w in g if ini(w) == par]
    F[u"certo5_%s" % certas[0]] = (u"Muito bem! %s e %s começam as duas com %s."
                                   % (falado(certas[0]).capitalize(), falado(certas[1]),
                                      par.lower()))
    # ⭐ a dica ENSINA O MÉTODO, que é o que falta a quem compara ao acaso
    F[u"dica5_%s" % certas[0]] = (u"Vá uma por uma: fale o nome e guarde só o comecinho. "
                                  u"Quando dois comecinhos forem iguais, achou.")

# ---- folha 6: completar o começo -------------------------------------------------
for w in IT[u"p6"]:
    F[u"certo6_%s" % w] = u"Isso! %s. O começo é %s." % (empedacos(w), ini(w).lower())
    F[u"dica6_%s" % w] = (u"Escute a palavra inteira: %s. Qual pedacinho falta lá no "
                          u"começo?" % falado(w))

# ---- folha 7: o intruso -----------------------------------------------------------
for it in IT[u"p7"]:
    c = it[u"c"]
    fam = [w for w in it[u"g"] if w != c]
    F[u"certo7_%s" % c] = (u"Isso! %s começam com %s, e %s não."
                           % (u", ".join(falado(w) for w in fam), ini(fam[0]).lower(),
                              falado(c)))
    F[u"dica7_%s" % c] = (u"Escute as quatro e guarde só o comecinho de cada uma. "
                          u"Três são iguais; uma é diferente.")

# ---- folha 8: as gavetas ----------------------------------------------------------
for w in IT[u"p8"]:
    F[u"certo8_%s" % w] = u"Boa! %s vai na gaveta do %s." % (falado(w).capitalize(),
                                                             ini(w).lower())
    F[u"dica8_%s" % w] = (u"Escute o começo: %s. Procure a gaveta com esse pedacinho."
                          % empedacos(w))

# ---- folha 9: escrever o começo ----------------------------------------------------
for w in IT[u"p9"]:
    F[u"certo9_%s" % w] = u"Muito bem! %s começa com %s." % (falado(w).capitalize(),
                                                             ini(w).lower())
    F[u"dica9_%s" % w] = (u"Escute devagar: %s. Escreva só o primeiro pedaço."
                          % empedacos(w))

# ---- folha 10: o mural --------------------------------------------------------------
for w in IT[u"p10"]:
    F[u"certo10_%s" % w] = u"%s, da família do %s. Foi para o seu mural!" % (
        falado(w).capitalize(), ini(w).lower())

# ══════════════════════════════════════════════════════════════════════
#  O MAPA DAS SÍLABAS INICIAIS — de qual palavra cada uma é recortada
#
#  ⚠️ Toda sílaba que o app fala sozinha (`sb1_CA`) precisa de uma PALAVRA de
#     onde ser cortada. Sintetizá-la solta faz a voz soletrar — foi o defeito
#     que o Marcos ouviu duas vezes. Aqui se escolhe, para cada sílaba inicial,
#     uma palavra do caderno que começa com ela.
# ══════════════════════════════════════════════════════════════════════
PALAVRAS_SIL, MAPA_SIL = {}, {}
precisa = set()
for w in IT[u"p1"] + IT[u"p6"] + IT[u"p8"] + IT[u"p10"]:
    precisa.add(ini(w))
for it in IT[u"p3"]:
    precisa.add(it[u"s"])
for g in IT[u"p4"]:
    for w in g:
        precisa.add(ini(w))
for lista in DISTRA.values():
    precisa.update(lista)

# ⚠️⚠️ DE QUAL PALAVRA SAI CADA SÍLABA — O DEFEITO QUE O MARCOS OUVIU (set/2026).
#    Palavras dele: *"não entendi muito o sentido da primeira atividade, pois
#    cita laranja e aparece lata"*. A folha 1 mostrava LATA e o alto-falante
#    dizia LARANJA. A causa estava AQUI: a fonte da sílaba era a primeira palavra
#    em ordem ALFABÉTICA que começa com ela — e "laranja" vem antes de "lata".
#    Num caderno de roda isso é fatal: a criança vê uma figura e ouve outra
#    palavra, e o pedaço que ela devia guardar chega grudado na palavra errada.
#
#    A regra agora: **a sílaba sai da palavra DA RODA**. Se LA é a sílaba da
#    roda do L e a palavra da roda é LATA, o recorte vem de LATA. Só quando a
#    sílaba não pertence a nenhuma roda é que se cai na ordem antiga.
import re as _re
_mr = _re.search(r"/\*RODAS-INI\*/\s*var RODAS = (\{.*?\});", html, _re.S)
DA_RODA = {}
if _mr:
    for _k, _r in json.loads(_mr.group(1)).items():
        for _s, _w in zip(_r["s"], _r["w"]):
            DA_RODA.setdefault(_s, _w)

for s in sorted(precisa):
    fonte = DA_RODA.get(s)
    if fonte and fonte not in PAL:
        fonte = None
    if not fonte:
        for w in sorted(usadas) + sorted(set(PAL) - usadas):
            if ini(w) == s:
                fonte = w
                break
    if not fonte:
        continue
    MAPA_SIL[s] = [fonte, 0]
    PALAVRAS_SIL[fonte] = sil(fonte)
# e as palavras cujas sílabas o app fala uma a uma
for w in IT[u"p1"]:
    PALAVRAS_SIL[w] = sil(w)

# a fala `sb1_<S>` é a MESMA coisa que a sílaba recortada: o app resolve pelo
# SILMAP e toca o mp3 da palavra-fonte. Nenhum texto solto é gravado aqui.


def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    t = F[k]
    if not t:
        continue
    c = chave(t)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": t, u"voz": VOZ})

io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ, u"palavras": PALAVRAS_SIL},
               ensure_ascii=False, indent=1))

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
blocoS = (u"/*SILMAP-INI*/var SILMAP = "
          + json.dumps(MAPA_SIL, ensure_ascii=False, sort_keys=True) + u";/*SILMAP-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/", lambda m: blocoS, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d palavra(s) com sílaba recortada"
      % (len(F), len(falas), len(PALAVRAS_SIL)))
