# -*- coding: utf-8 -*-
u"""
============================================================
 A MÁQUINA DE JUNTAR PALAVRAS — gerador das falas

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ E NESTE CADERNO A VOZ **É** O CONTEÚDO, não apoio.
    Juntar pedaços para formar palavra (síntese silábica) é operação de OUVIDO —
    é o que a criança faz por dentro quando lê BOLA sem soletrar. Uma folha de
    juntar sílabas sem voz não ensina a juntar nada: vira quebra-cabeça de
    desenho, que é outra coisa e não serve para ler.

 ⚠️⚠️ CADA PEDAÇO É RECORTADO DA PRÓPRIA PALAVRA.
    Beco já pago nesta casa (set/2026, o Marcos ouviu): mandar o sintetizador ler
    a sílaba SOLTA nunca fecha, porque ele não lê som, lê PALAVRA — e "VA"
    sozinho ele SOLETRA ("vê-á"). O `_padrao/silabas_voz.py` grava a palavra
    INTEIRA, alinha letra a letra (alinhamento forçado, modelo MMS) e corta o
    mp3 nas fronteiras. A criança ouve o pedaço na voz, no ritmo e na altura
    daquela palavra. O que sai daqui é o mapa que a ferramenta lê
    (`silabas.json`) e o `SILMAP` que o app usa para as opções soltas.

 Lê do próprio `index.html` os dois blocos que são a verdade do conteúdo:
   · `/*ITENS-INI*/ var ITENS = {...}` — o que cada folha sorteia;
   · `var PAL = { bola:["BOLA",["BO","LA"]], ... }` — a escrita e as SÍLABAS.

 Uso:  python3 _mont1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"mo_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\]', bloco):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])


def esc(w):
    return PAL[w][0] if w in PAL else w.upper()


def sil(w):
    return PAL[w][1] if w in PAL else [w.upper()]


# ⚠️ A palavra COMO SE FALA. A voz lê a minúscula melhor que a caixa alta, e
#    algumas o TTS erra na forma escrita — aqui elas vão consertadas, uma a uma.
DIZ = {u"maca": u"maçã", u"balao": u"balão", u"leao": u"leão", u"limao": u"limão",
       u"onibus": u"ônibus", u"xicara": u"xícara", u"jacare": u"jacaré",
       u"chapeu": u"chapéu", u"pao": u"pão", u"navio": u"navio"}


def falado(w):
    return DIZ.get(w, esc(w).lower())


def empedacos(w):
    u"""'ba... na... na' — as reticências fazem a voz separar de verdade"""
    return u"... ".join(s.lower() for s in sil(w))


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"A Máquina de Juntar Palavras. Dez folhas para juntar pedaços e formar "
              u"palavras. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim da Máquina de Juntar! Agora você sabe juntar os pedaços e "
             u"descobrir a palavra. Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva o pedaço que falta."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Escute de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois nos pedaços do nome dela."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram."

F[u"p1enun"] = (u"Folha um: junte os dois pedaços. Toque no primeiro pedaço, "
                u"depois no segundo, e aperte JUNTAR.")
F[u"p2enun"] = u"Folha dois: escute a palavra. Qual pedaço falta no fim?"
F[u"p3enun"] = (u"Folha três: agora o buraco muda de lugar. Primeiro no começo — e, no fim da folha, no meio da palavra.")
F[u"p4enun"] = (u"Folha quatro: os pedaços saíram fora de ordem. "
                u"Ponha cada um no seu lugar.")
F[u"p5enun"] = (u"Folha cinco: agora são três pedaços, e um deles sobra. "
                u"Monte a palavra da figura.")
F[u"p6enun"] = (u"Folha seis: aperte o alto-falante e escute os pedaços. "
                u"Que palavra eles formam?")
F[u"p7enun"] = u"Folha sete: ligue cada figura aos pedaços que formam o nome dela."
F[u"p8enun"] = (u"Folha oito: as duas começam igual! Escute até o fim e toque na certa.")
F[u"p9enun"] = u"Folha nove: escute a palavra e escreva o pedaço que falta."
F[u"p10enun"] = u"Folha dez: toque nas palavras que você montou e quer no seu mural."

# ---- toda palavra que aparece no caderno --------------------------------------
usadas = set()
for chave, lista in IT.items():
    for x in lista:
        if isinstance(x, list):
            for y in x:
                if isinstance(y, int):
                    continue
                if y in PAL:
                    usadas.add(y)
        else:
            usadas.add(x)
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: juntar os dois pedaços -------------------------------------------
for w in IT[u"p1"]:
    a, b = sil(w)
    F[u"certo1_%s" % w] = (u"Muito bem! %s com %s faz %s."
                           % (a.lower(), b.lower(), falado(w)))
    # ⚠️ pular NÃO é "errou": a voz diz o que fazer, sem a palavra errado
    F[u"volte1_%s" % w] = u"Espere! Comece pelo primeiro pedaço e vá seguindo."

# ---- folhas 2 e 3: o pedaço que falta ------------------------------------------
for reg in IT[u"p2"]:
    w = reg[0]
    ss = sil(w)
    F[u"certo2_%s" % w] = (u"Isso! %s mais %s faz %s."
                           % (ss[0].lower(), ss[1].lower(), falado(w)))
    F[u"dica2_%s" % w] = (u"Escute a palavra devagar: %s. Agora escute só o começo: %s. "
                          u"O que vem depois?" % (empedacos(w), ss[0].lower()))
for reg in IT[u"p3"]:
    w = reg[0]
    ss = sil(w)
    F[u"certo3_%s" % w] = (u"Isso! %s mais %s faz %s."
                           % (ss[0].lower(), ss[1].lower(), falado(w)))
    F[u"dica3_%s" % w] = (u"Escute a palavra devagar: %s. O fim você já tem: %s. "
                          u"Qual pedaço vem ANTES?" % (empedacos(w), ss[1].lower()))
# ⭐ o pedaço do MEIO (folha d18 da colheita: CA__LO, GI__FA) — o degrau mais alto
#    da série do buraco, porque a criança tem que segurar o começo E o fim de uma
#    vez. Entra no FIM da folha 3, nunca espalhado.
for reg in IT[u"p3b"]:
    w = reg[0]
    ss = sil(w)
    onde = reg[3] if len(reg) > 3 else 1
    F[u"certo3_%s" % w] = (u"Muito bem! %s: %s." % (falado(w).capitalize(), empedacos(w)))
    F[u"dica3_%s" % w] = (u"Este é do MEIO. Você já tem o começo, %s, e o fim, %s. "
                          u"Escute a palavra inteira devagar: %s. O que falta no meio?"
                          % (ss[0].lower(), ss[-1].lower(), empedacos(w)))

# ---- folhas 4 e 5: pôr os pedaços na ordem --------------------------------------
for w in IT[u"p4"]:
    F[u"certo4_%s" % w] = u"Muito bem! %s: %s." % (falado(w).capitalize(), empedacos(w))
    F[u"dica4_%s" % w] = (u"Escute a palavra devagar: %s. Qual é o pedaço que vem agora?"
                          % empedacos(w))
for w in IT[u"p5"]:
    F[u"certo5_%s" % w] = (u"Muito bem! %s: %s. E o pedaço que sobrou não era desta palavra."
                           % (falado(w).capitalize(), empedacos(w)))
    F[u"dica5_%s" % w] = (u"Escute a palavra devagar: %s. Um dos pedaços do banco não é "
                          u"dela — escute bem antes de pôr." % empedacos(w))

# ---- folha 6: que palavra é esta (só o ouvido) ----------------------------------
for reg in IT[u"p6"]:
    w = reg[0]
    F[u"certo6_%s" % w] = u"Isso! %s juntos fazem %s." % (empedacos(w), falado(w))
    F[u"dica6_%s" % w] = (u"Aperte o alto-falante e escute de novo, bem devagar. "
                          u"Junte os pedaços na cabeça antes de escolher.")

# ---- folha 7: ligar a figura aos pedaços ----------------------------------------
for g in IT[u"p7"]:
    for w in g:
        F[u"certo7_%s" % w] = (u"Isso! %s se escreve %s."
                               % (falado(w).capitalize(), empedacos(w)))
        F[u"dica7_%s" % w] = (u"Fale o nome da figura em pedaços: %s. Agora procure "
                              u"esses pedaços escritos." % empedacos(w))

# ---- folha 8: as duas começam igual ---------------------------------------------
for par in IT[u"p8"]:
    w, outra = par
    F[u"certo8_%s" % w] = (u"Isso! %s e %s começam igual, mas o fim é diferente. "
                           u"Você escutou até o fim!"
                           % (falado(w).capitalize(), falado(outra)))
    # ⭐ a dica ENSINA O TRUQUE: não é o começo, é o que vem DEPOIS dele
    F[u"dica8_%s" % w] = (u"As duas começam com %s. Não decida pelo começo! "
                          u"Escute o que vem DEPOIS: %s."
                          % (sil(w)[0].lower(), empedacos(w)))

# ---- folha 9: escrever o pedaço que falta ----------------------------------------
for reg in IT[u"p9"]:
    w, qual = reg[0], reg[1]
    F[u"certo9_%s" % w] = (u"Muito bem! %s: %s." % (falado(w).capitalize(), empedacos(w)))
    F[u"dica9_%s" % w] = (u"Escute a palavra em pedaços: %s. Agora escreva só o pedaço "
                          u"que está faltando no quadradinho." % empedacos(w))

# ---- folha 10: o mural ------------------------------------------------------------
for w in IT[u"p10"]:
    F[u"certo10_%s" % w] = (u"%s: %s. Foi para o seu mural!"
                            % (falado(w).capitalize(), empedacos(w)))

# ==============================================================================
#  O MAPA DAS SÍLABAS — quem recorta o quê de qual palavra
#
#  ⚠️ AQUI O CADERNO INTEIRO FALA EM PEDAÇOS: as folhas 1, 2, 3, 4, 5 e 9 tocam
#     pedaço por pedaço, e as folhas 6, 7, 8 e 10 tocam a palavra inteira PARTIDA
#     (`falarPedacos`). Então TODA palavra do caderno precisa de recorte — não dá
#     para escolher um subconjunto sem deixar um botão mudo em alguma folha.
#  ⚠️ E as opções soltas das folhas 2 e 3 (`sb1_TA`) são pedaços SEM palavra: o
#     `SILMAP` diz de qual palavra cada um deles sai, preferindo a palavra em que
#     ele está na MESMA posição (o "TA" do fim de BOTA soa diferente do "TA" do
#     meio de BATATA).
# ==============================================================================
PALAVRAS_SIL = {}
for w in sorted(usadas):
    PALAVRAS_SIL[w] = sil(w)

# os pedaços que aparecem SOZINHOS como opção (folhas 2 e 3)
soltos = {}
for tag, qual in ((u"p2", 1), (u"p3", 0), (u"p3b", 1)):
    for reg in IT[tag]:
        w = reg[0]
        onde = reg[3] if len(reg) > 3 else qual
        soltos.setdefault(sil(w)[onde], qual)
        for dist in reg[1:3]:
            soltos.setdefault(dist, qual)

MAPA_SIL = {}
faltando = []
for s in sorted(soltos):
    qual = soltos[s]
    achou = None
    # 1ª escolha: uma palavra do caderno em que o pedaço está na MESMA posição
    for w in sorted(PALAVRAS_SIL):
        ss = sil(w)
        pos = len(ss) - 1 if qual == 1 else 0
        if pos < len(ss) and ss[pos] == s:
            achou = (w, pos)
            break
    # 2ª: qualquer palavra do caderno
    if not achou:
        for w in sorted(PALAVRAS_SIL):
            if s in sil(w):
                achou = (w, sil(w).index(s))
                break
    # 3ª: qualquer palavra do pote (entra no recorte de propósito)
    if not achou:
        for w in sorted(set(PAL) - set(PALAVRAS_SIL)):
            if s in sil(w):
                achou = (w, sil(w).index(s))
                PALAVRAS_SIL[w] = sil(w)
                break
    if not achou:
        faltando.append(s)
        continue
    MAPA_SIL[s] = [achou[0], achou[1]]

if faltando:
    raise SystemExit(u"pedaço sem palavra de onde recortar: %s" % u", ".join(faltando))


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

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d palavra(s) com sílaba recortada; "
      u"%d pedaço(s) solto(s) no SILMAP"
      % (len(F), len(falas), len(PALAVRAS_SIL), len(MAPA_SIL)))
